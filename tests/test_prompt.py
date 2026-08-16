"""Testes do PromptComposer.

Os testes de snapshot comparam o prompt final BYTE A BYTE com os arquivos em
`tests/snapshots/`. E de proposito: o prompt e o artefato que gasta credito e
que vai parar em `jobs.resolved_prompt`; qualquer mudanca de redacao, de ordem
ou de pontuacao precisa ser uma decisao consciente, revisada no diff.

Para regravar os snapshots depois de uma mudanca intencional:

    CIE_UPDATE_SNAPSHOTS=1 uv run pytest tests/test_prompt.py -q

e depois confira o diff dos .txt antes de commitar. Sem a variavel, snapshot
ausente ou divergente falha o teste.

Nenhum teste aqui toca a rede: composicao de prompt e string pura.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from cie.enums import AspectRatio, TemplateKind
from cie.errors import TemplateError
from cie.models import StyleDescriptor, StyleDna, Template
from cie.prompt import (
    MAX_PROMPT_CHARS,
    NEGATIVE_PREFIX,
    PARTIAL_SUFFIX,
    SECTION_ANCHORS,
    SECTION_BODY,
    SECTION_NEGATIVE,
    SECTION_STYLE_DNA,
    SECTION_UNUSED_VARIABLES,
    TECHNICAL_ANCHORS,
    ComposedPrompt,
    PromptComposer,
    build_prompt_fragment,
    split_negative_terms,
)
from cie.template_loader import DEFAULT_NEGATIVE_TERMS, load_templates_dir

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
SNAPSHOT_DIR = Path(__file__).resolve().parent / "snapshots"
UPDATE_ENV = "CIE_UPDATE_SNAPSHOTS"

#: Cenas com snapshot: uma de risco baixo, uma de embalagem, uma com pessoa.
SNAPSHOT_TEMPLATES = (
    "macro_grao_torrado",
    "pacote_madeira_rustica",
    "maos_colheita_seletiva",
)

#: Descritor congelado. Mudar isto invalida os snapshots de proposito.
SNAPSHOT_DESCRIPTOR = StyleDescriptor(
    palette=["ocre queimado", "verde-cafeeiro profundo", "ambar de amanhecer"],
    light_quality="luz natural lateral suave, sombras longas de golden hour",
    lens="50mm equivalente, profundidade de campo rasa, bokeh cremoso",
    texture="grain fino de filme, microcontraste alto, sem saturacao artificial",
    framing="sujeito descentralizado, respiro negativo a direita",
    recurring_materials=["madeira rustica de lei", "aco inox escovado", "juta"],
    mood="elegancia rustica e cientifica, calma, artesanal",
    avoid=["saturacao HDR", "reflexos plasticos", "iluminacao de estudio dura"],
)


# --------------------------------------------------------------------------- #
# apoio
# --------------------------------------------------------------------------- #


@pytest.fixture(scope="module")
def templates() -> dict[str, Template]:
    """Os 12 YAML reais do repositorio, indexados por nome."""
    return {t.name: t for t in load_templates_dir(TEMPLATES_DIR)}


@pytest.fixture(scope="module")
def dna() -> StyleDna:
    return StyleDna(
        name="laboratorio-uberlandia",
        descriptor=SNAPSHOT_DESCRIPTOR,
        prompt_fragment=build_prompt_fragment(SNAPSHOT_DESCRIPTOR),
    )


def toy_template(**overrides) -> Template:
    """Template minimo em codigo, para os casos de borda."""
    data = {
        "name": "toy",
        "kind": TemplateKind.MACRO,
        "body": "Macro photograph of {subject} on {surface}.",
        "negative_prompt": "warped text, plastic skin",
        "default_aspect_ratio": AspectRatio.R1_1,
        "variables": {"subject": "one roasted bean", "surface": "steel tray"},
    }
    data.update(overrides)
    return Template(**data)


def snapshot_path(name: str) -> Path:
    return SNAPSHOT_DIR / f"{name}.txt"


# --------------------------------------------------------------------------- #
# build_prompt_fragment
# --------------------------------------------------------------------------- #


def test_fragment_carries_every_descriptor_field() -> None:
    fragment = build_prompt_fragment(SNAPSHOT_DESCRIPTOR)

    for label in ("palette", "light", "lens", "texture", "framing", "recurring materials", "mood"):
        assert label in fragment
    assert "ocre queimado" in fragment
    assert "aco inox escovado" in fragment
    assert "elegancia rustica e cientifica" in fragment
    assert fragment.endswith(".")


def test_fragment_never_carries_the_avoid_list() -> None:
    """`avoid` e negative: no positivo ele viraria instrucao de desenhar aquilo."""
    fragment = build_prompt_fragment(SNAPSHOT_DESCRIPTOR)

    for term in SNAPSHOT_DESCRIPTOR.avoid:
        assert term not in fragment


def test_fragment_of_empty_descriptor_is_empty() -> None:
    assert build_prompt_fragment(StyleDescriptor()) == ""


def test_fragment_skips_missing_fields_without_dangling_labels() -> None:
    fragment = build_prompt_fragment(StyleDescriptor(mood="calma", palette=["ocre"]))

    assert "mood calma" in fragment
    assert "lens" not in fragment
    assert "texture" not in fragment
    assert ";;" not in fragment


# --------------------------------------------------------------------------- #
# resolve_body
# --------------------------------------------------------------------------- #


def test_resolve_body_uses_template_defaults(templates) -> None:
    body = PromptComposer().resolve_body(templates["macro_grao_torrado"])

    assert "Arara" in body
    assert "{" not in body and "}" not in body


def test_resolve_body_override_wins(templates) -> None:
    body = PromptComposer().resolve_body(
        templates["macro_grao_torrado"], {"bean_variety": "Catuai 2SL"}
    )

    assert "Catuai 2SL" in body
    assert "Arara" not in body


def test_missing_placeholder_names_the_offender() -> None:
    template = toy_template(variables={"subject": "one roasted bean"})

    with pytest.raises(TemplateError) as excinfo:
        PromptComposer().resolve_body(template)

    message = str(excinfo.value)
    assert "surface" in message
    assert "toy" in message
    # Aponta o que falta, nao um "erro de template" generico.
    assert "placeholder" in message


def test_extra_variables_are_ignored_with_a_warning_in_sections(templates) -> None:
    composed = PromptComposer().compose(
        templates["macro_grao_torrado"], variables={"roast_level": "light", "colher": "x"}
    )

    assert "light" in composed.text
    assert "colher" in composed.sections[SECTION_UNUSED_VARIABLES]
    # Aviso e aviso: nao vira erro nem contamina o prompt.
    assert "colher" not in composed.text


def test_all_repository_templates_resolve(templates) -> None:
    composer = PromptComposer()
    for template in templates.values():
        body = composer.resolve_body(template)
        assert body and "{" not in body


# --------------------------------------------------------------------------- #
# ordem das secoes
# --------------------------------------------------------------------------- #


def test_sections_appear_in_the_contracted_order(templates, dna) -> None:
    composed = PromptComposer().compose(templates["macro_grao_torrado"], style_dna=dna)
    text = composed.text

    body_at = text.index(composed.sections[SECTION_BODY][:40])
    dna_at = text.index(composed.sections[SECTION_STYLE_DNA])
    anchors_at = text.index(composed.sections[SECTION_ANCHORS])
    negative_at = text.index(composed.sections[SECTION_NEGATIVE])

    assert body_at < dna_at < anchors_at < negative_at
    assert composed.char_count == len(text)
    assert not composed.truncated
    assert composed.dropped_sections == []


def test_compose_without_dna_has_no_style_section(templates) -> None:
    composed = PromptComposer().compose(templates["macro_grao_torrado"])

    assert SECTION_STYLE_DNA not in composed.sections
    assert composed.sections[SECTION_ANCHORS] in composed.text
    assert not composed.truncated


def test_dna_without_fragment_falls_back_to_the_descriptor(templates) -> None:
    """Perfil importado a mao pode nao ter `prompt_fragment` gravado."""
    bare = StyleDna(name="sem-fragmento", descriptor=SNAPSHOT_DESCRIPTOR, prompt_fragment="")

    composed = PromptComposer().compose(templates["macro_grao_torrado"], style_dna=bare)

    assert composed.sections[SECTION_STYLE_DNA] == build_prompt_fragment(SNAPSHOT_DESCRIPTOR)


def test_extra_anchors_are_appended_after_the_defaults(templates) -> None:
    composed = PromptComposer().compose(
        templates["macro_grao_torrado"], extra_anchors=["Tungsten practical in the background."]
    )
    anchors = composed.sections[SECTION_ANCHORS]

    assert anchors.startswith(TECHNICAL_ANCHORS[0])
    assert anchors.endswith("Tungsten practical in the background.")


# --------------------------------------------------------------------------- #
# negative
# --------------------------------------------------------------------------- #


def test_negative_is_always_present_and_carries_the_template_terms(templates, dna) -> None:
    for name in SNAPSHOT_TEMPLATES:
        composed = PromptComposer().compose(templates[name], style_dna=dna)

        assert composed.negative_prompt
        assert NEGATIVE_PREFIX in composed.text
        for term in DEFAULT_NEGATIVE_TERMS:
            assert term in composed.negative_prompt, f"{name}: faltou '{term}'"
        # Termos especificos da cena tambem sobrevivem.
        for term in templates[name].negative_prompt.split(","):
            assert term.strip() in composed.negative_prompt


def test_negative_absorbs_descriptor_avoid_and_extra_avoid(templates, dna) -> None:
    composed = PromptComposer().compose(
        templates["macro_grao_torrado"], style_dna=dna, extra_avoid=["confetti"]
    )

    assert "saturacao HDR" in composed.negative_prompt
    assert "confetti" in composed.negative_prompt
    assert composed.text.rstrip().endswith("confetti")


def test_negative_terms_are_deduped_case_insensitively() -> None:
    terms = split_negative_terms("warped text, Watermark", ["WARPED TEXT"], ["watermark", "blur"])

    assert terms == ["warped text", "Watermark", "blur"]


# --------------------------------------------------------------------------- #
# truncamento
# --------------------------------------------------------------------------- #


def _budget(*blocks: str) -> int:
    """Teto que cabe exatamente estes blocos separados por linha em branco."""
    return sum(len(block) for block in blocks) + 2 * len(blocks)


def test_truncation_drops_anchors_before_the_dna(templates, dna) -> None:
    template = templates["macro_grao_torrado"]
    full = PromptComposer().compose(template, style_dna=dna)
    negative_block = full.sections[SECTION_NEGATIVE]
    budget = _budget(full.sections[SECTION_BODY], dna.prompt_fragment, negative_block)

    composed = PromptComposer(max_chars=budget).compose(template, style_dna=dna)

    assert composed.truncated
    assert composed.dropped_sections == [SECTION_ANCHORS]
    assert SECTION_ANCHORS not in composed.sections
    # O DNA e o negative continuam inteiros.
    assert composed.sections[SECTION_STYLE_DNA] == dna.prompt_fragment
    assert composed.sections[SECTION_NEGATIVE] == negative_block
    assert composed.char_count <= budget


def test_truncation_drops_the_dna_before_the_negative(templates, dna) -> None:
    template = templates["macro_grao_torrado"]
    full = PromptComposer().compose(template, style_dna=dna)
    budget = _budget(full.sections[SECTION_BODY], full.sections[SECTION_NEGATIVE])

    composed = PromptComposer(max_chars=budget).compose(template, style_dna=dna)

    assert composed.dropped_sections == [SECTION_ANCHORS, SECTION_STYLE_DNA]
    assert composed.negative_prompt == full.negative_prompt
    assert composed.char_count <= budget


def test_negative_is_the_last_to_yield_and_yields_term_by_term(templates, dna) -> None:
    template = templates["macro_grao_torrado"]
    body = PromptComposer().resolve_body(template)

    composed = PromptComposer(max_chars=len(body) + 60).compose(template, style_dna=dna)

    assert composed.dropped_sections == [
        SECTION_ANCHORS,
        SECTION_STYLE_DNA,
        SECTION_NEGATIVE + PARTIAL_SUFFIX,
    ]
    assert composed.negative_prompt.startswith("warped text")
    assert composed.char_count <= len(body) + 60
    # O corpo sai intacto mesmo no aperto maximo.
    assert composed.text.startswith(body)


def test_body_alone_can_consume_the_whole_budget(templates, dna) -> None:
    template = templates["macro_grao_torrado"]
    body = PromptComposer().resolve_body(template)

    composed = PromptComposer(max_chars=len(body) + 1).compose(template, style_dna=dna)

    assert composed.text == body
    assert composed.negative_prompt == ""
    assert composed.dropped_sections == [
        SECTION_ANCHORS,
        SECTION_STYLE_DNA,
        SECTION_NEGATIVE,
    ]


def test_body_over_the_limit_raises_instead_of_cutting_the_scene(templates) -> None:
    with pytest.raises(TemplateError) as excinfo:
        PromptComposer(max_chars=200).compose(templates["macro_grao_torrado"])

    assert "corpo" in str(excinfo.value)
    assert "200" in str(excinfo.value)


def test_every_real_template_fits_the_default_budget(templates, dna) -> None:
    """Regressao: nenhuma das 12 cenas pode nascer ja truncada."""
    composer = PromptComposer()
    for name, template in templates.items():
        composed = composer.compose(template, style_dna=dna)
        assert not composed.truncated, f"{name} estourou {MAX_PROMPT_CHARS} caracteres"
        assert composed.char_count <= MAX_PROMPT_CHARS


# --------------------------------------------------------------------------- #
# snapshots
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("name", SNAPSHOT_TEMPLATES)
def test_prompt_snapshot(name: str, templates, dna) -> None:
    """Compara byte a byte. `CIE_UPDATE_SNAPSHOTS=1` regrava os arquivos."""
    composed = PromptComposer().compose(templates[name], style_dna=dna)
    path = snapshot_path(name)

    if os.environ.get(UPDATE_ENV) == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(composed.text, encoding="utf-8")

    assert path.exists(), (
        f"snapshot ausente: {path}. Rode {UPDATE_ENV}=1 uv run pytest tests/test_prompt.py"
    )
    expected = path.read_text(encoding="utf-8")
    assert composed.text == expected, (
        f"o prompt de '{name}' mudou. Se foi intencional, rode "
        f"{UPDATE_ENV}=1 uv run pytest tests/test_prompt.py e revise o diff."
    )


def test_snapshots_are_self_consistent(templates, dna) -> None:
    """O snapshot precisa terminar no negative e nao conter placeholder solto."""
    for name in SNAPSHOT_TEMPLATES:
        text = snapshot_path(name).read_text(encoding="utf-8")
        assert NEGATIVE_PREFIX in text
        assert "{" not in text
        assert "warped text" in text


def test_composition_is_deterministic(templates, dna) -> None:
    first = PromptComposer().compose(templates["maos_colheita_seletiva"], style_dna=dna)
    second = PromptComposer().compose(templates["maos_colheita_seletiva"], style_dna=dna)

    assert isinstance(first, ComposedPrompt)
    assert first.text == second.text
