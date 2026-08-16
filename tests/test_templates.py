"""Testes do catalogo de templates e do carregador YAML.

Nenhum acesso a rede: tudo e arquivo local mais SQLite em tmp_path.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import pytest
import yaml

from cie import repository, template_loader
from cie.config import PROJECT_ROOT
from cie.enums import AspectRatio, Pillar, RiskFlag, TemplateKind
from cie.errors import TemplateError
from cie.models import Template
from cie.template_loader import (
    DEFAULT_NEGATIVE_TERMS,
    load_template_file,
    load_templates_dir,
    required_variables,
    sync_templates,
    validate_template,
)

TEMPLATES_DIR = PROJECT_ROOT / "templates"

#: Contrato do catalogo: nome -> (pilar, tipo, proporcao padrao).
EXPECTED: dict[str, tuple[Pillar | None, TemplateKind, AspectRatio]] = {
    "bloom_v60": (Pillar.P4, TemplateKind.MACRO, AspectRatio.R3_4),
    "cafezal_encosta": (Pillar.P1, TemplateKind.SCENE, AspectRatio.R3_2),
    "drip_coffee_escritorio": (Pillar.P4, TemplateKind.LIFESTYLE, AspectRatio.R4_3),
    "harmonizacao_queijo_canastra": (Pillar.P4, TemplateKind.LIFESTYLE, AspectRatio.R3_2),
    "macro_grao_torrado": (Pillar.P3, TemplateKind.MACRO, AspectRatio.R1_1),
    "maos_colheita_seletiva": (Pillar.P1, TemplateKind.SCENE, AspectRatio.R4_3),
    "pacote_madeira_rustica": (Pillar.PRODUCT, TemplateKind.PRODUCT_SHOT, AspectRatio.R3_4),
    "paineis_solares_amanhecer": (Pillar.P2, TemplateKind.SCENE, AspectRatio.R16_9),
    "tambor_torra": (Pillar.P3, TemplateKind.SCENE, AspectRatio.R4_3),
    "terreiro_secagem": (Pillar.P1, TemplateKind.SCENE, AspectRatio.R3_2),
    "textura_juta_saco": (None, TemplateKind.TEXTURE, AspectRatio.R1_1),
    "vapor_xicara": (Pillar.P4, TemplateKind.MACRO, AspectRatio.R9_16),
}


@pytest.fixture
def catalog() -> list[Template]:
    return load_templates_dir(TEMPLATES_DIR)


def _payload(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "name": "cena_de_teste",
        "pillar": "3",
        "kind": "macro",
        "default_aspect_ratio": "1:1",
        "requires_reference": False,
        "risk_flags": [],
        "variables": {"mood": "calm"},
        "body": "A stoneware cup on a worn table, {mood} side light.\n",
        "negative_prompt": template_loader.default_negative_prompt(),
        "notes": "cena de teste",
    }
    payload.update(overrides)
    return payload


def _write(path: Path, payload: dict[str, Any] | str) -> Path:
    text = (
        payload
        if isinstance(payload, str)
        else yaml.safe_dump(payload, allow_unicode=False, sort_keys=False)
    )
    path.write_text(text, encoding="utf-8")
    return path


# --------------------------------------------------------------------------- #
# catalogo real
# --------------------------------------------------------------------------- #


def test_directory_has_exactly_the_twelve_templates(catalog: list[Template]) -> None:
    assert [t.name for t in catalog] == sorted(EXPECTED)


def test_file_name_matches_template_name() -> None:
    for file in sorted(TEMPLATES_DIR.glob("*.yaml")):
        assert load_template_file(file).name == file.stem


def test_every_real_template_validates(catalog: list[Template]) -> None:
    problems = {t.name: validate_template(t) for t in catalog}
    assert {name: issues for name, issues in problems.items() if issues} == {}


def test_negative_prompt_carries_all_default_terms(catalog: list[Template]) -> None:
    for template in catalog:
        lowered = template.negative_prompt.lower()
        missing = [term for term in DEFAULT_NEGATIVE_TERMS if term.lower() not in lowered]
        assert not missing, f"{template.name} sem: {missing}"
    assert len(DEFAULT_NEGATIVE_TERMS) == 8


def test_pillar_kind_and_aspect_ratio_match_the_contract(catalog: list[Template]) -> None:
    actual = {
        t.name: (t.pillar, t.kind, t.default_aspect_ratio) for t in catalog
    }
    assert actual == EXPECTED


def test_packaging_text_implies_requires_reference(catalog: list[Template]) -> None:
    touching = [t for t in catalog if t.touches_packaging]
    assert {t.name for t in touching} == {
        "drip_coffee_escritorio",
        "pacote_madeira_rustica",
    }
    for template in touching:
        assert template.requires_reference is True


def test_every_placeholder_has_a_default(catalog: list[Template]) -> None:
    for template in catalog:
        assert template.body.strip()
        assert required_variables(template) <= set(template.variables)
        assert required_variables(template), f"{template.name} sem variaveis de cena"


def test_yaml_files_are_pure_ascii() -> None:
    # Comentario e notas em portugues, mas sem acento: o texto viaja por CLI,
    # SQLite e prompt sem risco de mojibake.
    for file in sorted(TEMPLATES_DIR.glob("*.yaml")):
        file.read_bytes().decode("ascii")


def test_people_template_carries_the_strict_policy(catalog: list[Template]) -> None:
    template = next(t for t in catalog if t.name == "maos_colheita_seletiva")
    assert set(template.risk_flags) == {RiskFlag.HANDS, RiskFlag.HUMAN_FACE}
    assert template.touches_faces is True
    assert template.requires_reference is True
    assert template.notes and "POLITICA" in template.notes
    # O enquadramento e parte da regra: rosto fora do quadro, dito no proprio corpo.
    assert "outside the frame" in template.body
    assert "no face" in template.body.lower()


def test_no_template_regenerates_faces(catalog: list[Template]) -> None:
    for template in catalog:
        assert RiskFlag.FACE_REGENERATION not in template.risk_flags


def test_composer_is_preferred_for_the_packshot(catalog: list[Template]) -> None:
    template = next(t for t in catalog if t.name == "pacote_madeira_rustica")
    assert template.notes and "compositor" in template.notes.lower()


# --------------------------------------------------------------------------- #
# sincronizacao com o banco
# --------------------------------------------------------------------------- #


def test_sync_templates_writes_all_and_is_idempotent(conn: sqlite3.Connection) -> None:
    first = sync_templates(conn, TEMPLATES_DIR)
    assert len(first) == len(EXPECTED)
    assert len(set(first)) == len(first)

    second = sync_templates(conn, TEMPLATES_DIR)
    assert second == first
    assert len(repository.list_templates(conn)) == len(EXPECTED)


def test_sync_templates_round_trips_the_content(conn: sqlite3.Connection) -> None:
    sync_templates(conn, TEMPLATES_DIR)
    stored = repository.get_template_by_name(conn, "drip_coffee_escritorio")
    loaded = load_template_file(TEMPLATES_DIR / "drip_coffee_escritorio.yaml")

    assert stored is not None
    assert stored.body == loaded.body
    assert stored.negative_prompt == loaded.negative_prompt
    assert stored.risk_flags == [RiskFlag.PACKAGING_TEXT]
    assert stored.requires_reference is True
    assert stored.variables == loaded.variables
    assert stored.default_aspect_ratio is AspectRatio.R4_3

    untied = repository.get_template_by_name(conn, "textura_juta_saco")
    assert untied is not None and untied.pillar is None


def test_sync_templates_updates_an_edited_file(
    conn: sqlite3.Connection, tmp_path: Path
) -> None:
    directory = tmp_path / "templates"
    directory.mkdir()
    _write(directory / "cena_de_teste.yaml", _payload())
    first = sync_templates(conn, directory)

    _write(
        directory / "cena_de_teste.yaml",
        _payload(body="A second version of the scene, {mood} light.\n"),
    )
    second = sync_templates(conn, directory)

    assert second == first  # upsert por `name`, nao insercao nova
    stored = repository.get_template_by_name(conn, "cena_de_teste")
    assert stored is not None and "second version" in stored.body


# --------------------------------------------------------------------------- #
# erros de carregamento
# --------------------------------------------------------------------------- #


def test_malformed_yaml_raises_with_the_path(tmp_path: Path) -> None:
    bad = _write(tmp_path / "quebrado.yaml", "name: x\nbody: [nao fecha\n")
    with pytest.raises(TemplateError) as excinfo:
        load_template_file(bad)
    assert str(bad) in str(excinfo.value)
    assert "YAML malformado" in str(excinfo.value)


def test_empty_file_raises(tmp_path: Path) -> None:
    empty = _write(tmp_path / "vazio.yaml", "# so um comentario\n")
    with pytest.raises(TemplateError, match="vazio"):
        load_template_file(empty)


def test_scalar_root_raises(tmp_path: Path) -> None:
    scalar = _write(tmp_path / "escalar.yaml", "apenas um texto solto\n")
    with pytest.raises(TemplateError, match="mapeamento"):
        load_template_file(scalar)


def test_unknown_key_is_rejected(tmp_path: Path) -> None:
    path = _write(tmp_path / "typo.yaml", _payload(requires_referece=True))
    with pytest.raises(TemplateError, match="chaves desconhecidas: requires_referece"):
        load_template_file(path)


def test_missing_kind_is_rejected(tmp_path: Path) -> None:
    payload = _payload()
    del payload["kind"]
    path = _write(tmp_path / "sem_kind.yaml", payload)
    with pytest.raises(TemplateError, match="campo obrigatorio ausente: kind"):
        load_template_file(path)


def test_invalid_kind_lists_the_accepted_values(tmp_path: Path) -> None:
    path = _write(tmp_path / "kind_ruim.yaml", _payload(kind="poster"))
    with pytest.raises(TemplateError) as excinfo:
        load_template_file(path)
    assert "kind invalido" in str(excinfo.value)
    assert "product_shot" in str(excinfo.value)


def test_invalid_aspect_ratio_is_rejected(tmp_path: Path) -> None:
    path = _write(tmp_path / "ratio.yaml", _payload(default_aspect_ratio="4:5"))
    with pytest.raises(TemplateError, match="default_aspect_ratio invalido"):
        load_template_file(path)


def test_invalid_pillar_is_rejected(tmp_path: Path) -> None:
    path = _write(tmp_path / "pilar.yaml", _payload(pillar="5"))
    with pytest.raises(TemplateError, match="pillar invalido"):
        load_template_file(path)


def test_requires_reference_must_be_boolean(tmp_path: Path) -> None:
    path = _write(tmp_path / "bool.yaml", _payload(requires_reference="false"))
    with pytest.raises(TemplateError, match="requires_reference precisa ser true ou false"):
        load_template_file(path)


def test_variable_without_default_is_rejected(tmp_path: Path) -> None:
    path = _write(tmp_path / "var.yaml", _payload(variables={"mood": None}))
    with pytest.raises(TemplateError, match="precisa de default"):
        load_template_file(path)


def test_load_template_file_can_skip_validation(tmp_path: Path) -> None:
    path = _write(tmp_path / "sem_negativo.yaml", _payload(negative_prompt="nada"))
    with pytest.raises(TemplateError, match="negative_prompt"):
        load_template_file(path)
    template = load_template_file(path, validate=False)
    assert template.negative_prompt == "nada"
    assert validate_template(template)


def test_load_templates_dir_aggregates_every_error(tmp_path: Path) -> None:
    directory = tmp_path / "templates"
    directory.mkdir()
    _write(directory / "ok.yaml", _payload(name="ok"))
    _write(directory / "ruim_a.yaml", _payload(name="ruim_a", kind="poster"))
    _write(directory / "ruim_b.yaml", "body: [nao fecha\n")

    with pytest.raises(TemplateError) as excinfo:
        load_templates_dir(directory)
    message = str(excinfo.value)
    assert "ruim_a.yaml" in message
    assert "ruim_b.yaml" in message
    assert "2 template(s) invalido(s)" in message


def test_duplicate_names_are_rejected(tmp_path: Path) -> None:
    directory = tmp_path / "templates"
    directory.mkdir()
    _write(directory / "a.yaml", _payload(name="mesmo_nome"))
    _write(directory / "b.yaml", _payload(name="mesmo_nome"))
    with pytest.raises(TemplateError, match="nome duplicado"):
        load_templates_dir(directory)


def test_missing_directory_raises(tmp_path: Path) -> None:
    with pytest.raises(TemplateError, match="nao encontrado"):
        load_templates_dir(tmp_path / "nao_existe")


def test_directory_ignores_non_yaml_files(tmp_path: Path) -> None:
    directory = tmp_path / "templates"
    directory.mkdir()
    _write(directory / "ok.yaml", _payload(name="ok"))
    (directory / "README.md").write_text("nao e template\n", encoding="utf-8")
    (directory / "sub").mkdir()
    assert [t.name for t in load_templates_dir(directory)] == ["ok"]


def test_name_falls_back_to_the_file_stem(tmp_path: Path) -> None:
    payload = _payload()
    del payload["name"]
    path = _write(tmp_path / "cena_sem_nome.yaml", payload)
    assert load_template_file(path).name == "cena_sem_nome"


# --------------------------------------------------------------------------- #
# validacao pura
# --------------------------------------------------------------------------- #


def _template(**overrides: Any) -> Template:
    base: dict[str, Any] = {
        "name": "unitario",
        "kind": TemplateKind.MACRO,
        "body": "A cup, {mood} light.",
        "variables": {"mood": "calm"},
        "negative_prompt": template_loader.default_negative_prompt(),
    }
    base.update(overrides)
    return Template(**base)


def test_validate_accepts_a_minimal_template() -> None:
    assert validate_template(_template()) == []


def test_validate_flags_missing_negative_terms() -> None:
    issues = validate_template(_template(negative_prompt="warped text, watermark"))
    assert len(issues) == 1
    assert "plastic skin" in issues[0]
    assert "uncanny faces" in issues[0]


def test_validate_is_case_insensitive_about_negative_terms() -> None:
    loud = template_loader.default_negative_prompt().upper()
    assert validate_template(_template(negative_prompt=loud)) == []


def test_validate_flags_empty_body() -> None:
    issues = validate_template(_template(body="   "))
    assert issues == ["body vazio"]


def test_validate_flags_placeholder_without_default() -> None:
    issues = validate_template(_template(body="A cup, {mood} light on {surface}."))
    assert len(issues) == 1
    assert "surface" in issues[0]


def test_validate_flags_packaging_without_reference() -> None:
    issues = validate_template(
        _template(risk_flags=[RiskFlag.PACKAGING_TEXT], requires_reference=False)
    )
    assert len(issues) == 1
    assert "requires_reference" in issues[0]
    assert validate_template(
        _template(risk_flags=[RiskFlag.PACKAGING_TEXT], requires_reference=True)
    ) == []


def test_required_variables_reads_the_body_only() -> None:
    template = _template(
        body="{a} and {b_2} and {a} again, but not { spaced } nor {}",
        variables={"a": "x", "b_2": "y", "unused": "z"},
    )
    assert required_variables(template) == {"a", "b_2"}
    assert validate_template(template) == []
