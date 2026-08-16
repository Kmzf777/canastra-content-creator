"""Composicao do prompt final, com trilha de auditoria.

A ordem da concatenacao e fixa e tem motivo. O corpo do template diz *o que* a
cena e; o Style DNA diz *como* a marca fotografa; as ancoras tecnicas prendem o
resultado a fisica de uma camera real; o negative fecha os modos de falha
conhecidos. Quem abrir `jobs.resolved_prompt` seis meses depois consegue
reconstruir peca por peca de onde veio cada trecho.

  1. corpo do template com as variaveis resolvidas
  2. prompt_fragment do Style DNA
  3. ancoras tecnicas fotograficas
  4. negative prompt

Sobre o negative: este ambiente nao tem egress para api.x.ai nem docs.x.ai,
entao nao existe prova de que a API de imagem aceite um campo `negative_prompt`
separado. A suposicao conservadora vale - o negative entra anexado ao proprio
texto, prefixado por `NEGATIVE_PREFIX`. `ComposedPrompt.negative_prompt` guarda
os termos isolados, prontos para migrar para um campo nativo no dia em que a
sondagem (`cie/capabilities.py`) provar que ele existe.

Nada aqui chama rede: composicao e string pura e deterministica.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

from .errors import TemplateError
from .models import StyleDescriptor, StyleDna, Template

# O que conta como placeholder tem que ser exatamente o mesmo aqui e na
# validacao do YAML: um regex proprio abriria a porta para um template passar em
# `templates sync` e quebrar na hora de compor. Fonte unica, mesmo sendo privada.
from .template_loader import _PLACEHOLDER_RE, required_variables

#: Teto de caracteres do prompt final. NAO e um limite documentado pela xAI:
#: docs.x.ai e inalcancavel deste ambiente, entao 3800 e uma escolha de
#: seguranca - folga confortavel abaixo do teto tipico (~4000) das APIs de
#: imagem que publicam esse numero. E configuravel por
#: `PromptComposer(max_chars=...)`; quando a sondagem confirmar o valor real,
#: basta corrigir aqui, num lugar so.
MAX_PROMPT_CHARS = 3800

#: A API nao expoe campo de negative prompt confirmado, entao ele vai anexado ao
#: texto positivo com este prefixo.
NEGATIVE_PREFIX = "Avoid: "

#: Abre o trecho de Style DNA. Deixa explicito para o modelo que o que vem a
#: seguir e assinatura visual a ser reproduzida, nao conteudo novo de cena.
STYLE_DNA_LEAD = "Match the visual signature of the reference set: "

#: Ancoras fotograficas reais: camera, lente, luz, filme. Sao o contrapeso do
#: "look de IA" - descrevem uma captura fisicamente possivel, com as
#: imperfeicoes que uma foto de verdade tem e que a difusao tende a limpar.
TECHNICAL_ANCHORS: tuple[str, ...] = (
    "Shot on a full frame camera, RAW capture at ISO 200, natural optical falloff "
    "toward the corners and no digital sharpening halo.",
    "Physically plausible depth of field: a single focal plane, gradual defocus, "
    "optical bokeh from the aperture blades rather than a uniform blur.",
    "Daylight balanced colour rendition with true blacks and retained highlight "
    "detail; contrast from the lighting itself, never from HDR tone mapping.",
    "Fine organic film grain, honest surface texture, dust and small imperfections "
    "left where they fell.",
    "Documentary framing from a handheld working distance, slightly off axis, "
    "without staged prop symmetry.",
)

#: Nomes das secoes, na ordem em que aparecem no texto final.
SECTION_BODY = "body"
SECTION_STYLE_DNA = "style_dna"
SECTION_ANCHORS = "anchors"
SECTION_NEGATIVE = "negative"
SECTION_ORDER: tuple[str, ...] = (
    SECTION_BODY,
    SECTION_STYLE_DNA,
    SECTION_ANCHORS,
    SECTION_NEGATIVE,
)

#: Chave de aviso em `ComposedPrompt.sections`: variaveis que ninguem usou.
SECTION_UNUSED_VARIABLES = "unused_variables"

#: Sufixo em `dropped_sections` quando a secao foi encurtada, nao removida.
PARTIAL_SUFFIX = ":partial"

#: Separador entre as secoes do prompt final.
_JOIN = "\n\n"


@dataclass
class ComposedPrompt:
    """Resultado da composicao, ja pronto para `jobs.resolved_prompt`.

    `text` e o que vai para a API (negative incluso, com prefixo).
    `negative_prompt` guarda so os termos, sem prefixo, como foram efetivamente
    enviados - se o truncamento cortou termos, `negative_prompt` reflete o
    corte, para o registro de auditoria bater com o que a API recebeu.
    `sections` traz cada trecho como entrou no texto; secao cortada nao aparece.
    """

    text: str
    negative_prompt: str = ""
    sections: dict[str, str] = field(default_factory=dict)
    char_count: int = 0
    truncated: bool = False
    dropped_sections: list[str] = field(default_factory=list)


def _squeeze(value: str) -> str:
    """Colapsa espacos e quebras de linha; o YAML entrega texto com hard wrap."""
    return " ".join(str(value).split()).strip()


def _clean(value: str) -> str:
    """Normaliza um item de descritor/negative para entrar numa lista com `;` ou `,`."""
    return _squeeze(value).rstrip(".").strip()


def _clean_all(values: Iterable[str]) -> list[str]:
    return [cleaned for cleaned in (_clean(item) for item in values) if cleaned]


def _sentences(values: Iterable[str]) -> list[str]:
    """Ancoras sao frases: mantem a pontuacao final, so normaliza o espaco."""
    return [squeezed for squeezed in (_squeeze(item) for item in values) if squeezed]


def build_prompt_fragment(descriptor: StyleDescriptor) -> str:
    """Transforma o Style DNA em uma frase densa em ingles.

    Os rotulos sao em ingles porque o prompt e em ingles, mas os valores saem
    exatamente como o modelo de visao os devolveu (em geral, em portugues): sao
    a descricao das fotos reais da operacao e traduzir seria reescrever o dado.

    `descriptor.avoid` NAO entra aqui - ele e negative, e `PromptComposer` o
    coloca no lugar certo. Descritor vazio devolve string vazia, nunca um rotulo
    solto sem conteudo.
    """
    parts: list[str] = []

    palette = _clean_all(descriptor.palette)
    if palette:
        parts.append("palette " + ", ".join(palette))
    if _clean(descriptor.light_quality):
        parts.append("light " + _clean(descriptor.light_quality))
    if _clean(descriptor.lens):
        parts.append("lens " + _clean(descriptor.lens))
    if _clean(descriptor.texture):
        parts.append("texture " + _clean(descriptor.texture))
    if _clean(descriptor.framing):
        parts.append("framing " + _clean(descriptor.framing))
    materials = _clean_all(descriptor.recurring_materials)
    if materials:
        parts.append("recurring materials " + ", ".join(materials))
    if _clean(descriptor.mood):
        parts.append("mood " + _clean(descriptor.mood))

    if not parts:
        return ""
    return STYLE_DNA_LEAD + "; ".join(parts) + "."


def split_negative_terms(*sources: str | Sequence[str] | None) -> list[str]:
    """Junta negative prompts e listas de `avoid` num unico conjunto ordenado.

    Dedupe e case-insensitive e preserva a primeira ocorrencia: os termos do
    template vem antes dos do Style DNA, que vem antes dos extras do chamador.
    """
    terms: list[str] = []
    seen: set[str] = set()
    for source in sources:
        if not source:
            continue
        raw = [source] if isinstance(source, str) else list(source)
        for chunk in raw:
            for piece in str(chunk).split(","):
                term = _clean(piece)
                if not term or term.lower() in seen:
                    continue
                seen.add(term.lower())
                terms.append(term)
    return terms


def _dropped(name: str, before: Sequence[str], after: Sequence[str]) -> list[str]:
    """Como a secao saiu do truncamento: inteira, encurtada, ou intacta."""
    if before and not after:
        return [name]
    if len(after) < len(before):
        return [name + PARTIAL_SUFFIX]
    return []


def _assemble(body: str, fragment: str, anchors: Sequence[str], negative: Sequence[str]) -> str:
    blocks = [body]
    if fragment:
        blocks.append(fragment)
    if anchors:
        blocks.append(" ".join(anchors))
    if negative:
        blocks.append(NEGATIVE_PREFIX + ", ".join(negative))
    return _JOIN.join(blocks)


class PromptComposer:
    """Monta o prompt final. Sem estado entre chamadas: da para reusar a vontade."""

    def __init__(
        self,
        max_chars: int = MAX_PROMPT_CHARS,
        anchors: Sequence[str] = TECHNICAL_ANCHORS,
    ) -> None:
        self.max_chars = max_chars
        self.anchors: tuple[str, ...] = tuple(anchors)

    # ----------------------------------------------------------------- #
    # corpo do template
    # ----------------------------------------------------------------- #

    def resolve_body(
        self, template: Template, variables: dict[str, str] | None = None
    ) -> str:
        """Substitui os placeholders `{assim}` do corpo do template.

        `template.variables` sao o default; o que vier em `variables` sobrescreve.
        Placeholder sem valor e erro duro: gerar imagem com `{roast_level}`
        literal no prompt e credito jogado fora.
        """
        merged = self.merge_variables(template, variables)
        missing = sorted(required_variables(template) - set(merged))
        if missing:
            raise TemplateError(
                f"template '{template.name}': placeholder sem valor: "
                f"{', '.join(missing)}; defina um default em `variables:` no YAML "
                f"ou passe --var {missing[0]}=<valor>"
            )
        # Substituicao dirigida pelo placeholder (e nao str.format) para que
        # chave solta no corpo - uma medida escrita a mao entre chaves, por
        # exemplo - nao derrube a composicao inteira.
        resolved = _PLACEHOLDER_RE.sub(lambda m: merged[m.group(1)], template.body)
        return resolved.strip()

    @staticmethod
    def merge_variables(
        template: Template, variables: dict[str, str] | None = None
    ) -> dict[str, str]:
        merged = {key: str(value) for key, value in template.variables.items()}
        merged.update({key: str(value) for key, value in (variables or {}).items()})
        return merged

    @staticmethod
    def unused_variables(
        template: Template, variables: dict[str, str] | None = None
    ) -> list[str]:
        """Chaves definidas que o corpo nao usa. Aviso, nunca erro."""
        merged = PromptComposer.merge_variables(template, variables)
        return sorted(set(merged) - required_variables(template))

    # ----------------------------------------------------------------- #
    # composicao
    # ----------------------------------------------------------------- #

    def compose(
        self,
        template: Template,
        *,
        variables: dict[str, str] | None = None,
        style_dna: StyleDna | None = None,
        extra_anchors: Sequence[str] | None = None,
        extra_avoid: Sequence[str] | None = None,
    ) -> ComposedPrompt:
        body = self.resolve_body(template, variables)
        if len(body) > self.max_chars:
            raise TemplateError(
                f"template '{template.name}': o corpo resolvido tem {len(body)} "
                f"caracteres e o teto e {self.max_chars}. O corpo nunca e cortado "
                "(cortar cena e mudar a foto): encurte o body no YAML ou suba "
                "max_chars conscientemente."
            )

        fragment = ""
        descriptor_avoid: list[str] = []
        if style_dna is not None:
            # `prompt_fragment` e persistido junto do DNA; se veio vazio (perfil
            # antigo, importacao manual), reconstroi do descriptor na hora.
            fragment = style_dna.prompt_fragment.strip() or build_prompt_fragment(
                style_dna.descriptor
            )
            descriptor_avoid = list(style_dna.descriptor.avoid)

        anchors = list(self.anchors) + _sentences(extra_anchors or [])
        negative = split_negative_terms(
            template.negative_prompt, descriptor_avoid, extra_avoid
        )

        kept_anchors, kept_fragment, kept_negative = self._truncate(
            body, fragment, anchors, negative
        )

        text = _assemble(body, kept_fragment, kept_anchors, kept_negative)
        # Relatado na ordem em que o corte acontece: ancoras, DNA, negative.
        dropped = [
            *_dropped(SECTION_ANCHORS, anchors, kept_anchors),
            *([SECTION_STYLE_DNA] if fragment and not kept_fragment else []),
            *_dropped(SECTION_NEGATIVE, negative, kept_negative),
        ]

        sections: dict[str, str] = {SECTION_BODY: body}
        if kept_fragment:
            sections[SECTION_STYLE_DNA] = kept_fragment
        if kept_anchors:
            sections[SECTION_ANCHORS] = " ".join(kept_anchors)
        if kept_negative:
            sections[SECTION_NEGATIVE] = NEGATIVE_PREFIX + ", ".join(kept_negative)
        unused = self.unused_variables(template, variables)
        if unused:
            sections[SECTION_UNUSED_VARIABLES] = (
                "variaveis ignoradas (nao aparecem no corpo): " + ", ".join(unused)
            )

        return ComposedPrompt(
            text=text,
            negative_prompt=", ".join(kept_negative),
            sections=sections,
            char_count=len(text),
            truncated=bool(dropped),
            dropped_sections=dropped,
        )

    # ----------------------------------------------------------------- #
    # truncamento
    # ----------------------------------------------------------------- #

    def _truncate(
        self,
        body: str,
        fragment: str,
        anchors: Sequence[str],
        negative: Sequence[str],
    ) -> tuple[list[str], str, list[str]]:
        """Corta na ordem: ancoras tecnicas, depois DNA, depois negative.

        As ancoras saem primeiro porque sao genericas e reconstrutiveis; o DNA
        sai depois porque perde consistencia de marca mas nao a cena; o negative
        e o ultimo a ceder porque e ele que segura texto deformado e mao com seis
        dedos. O corpo nunca entra na fila de corte.
        """
        kept_anchors = list(anchors)
        kept_fragment = fragment
        kept_negative = list(negative)

        while len(_assemble(body, kept_fragment, kept_anchors, kept_negative)) > self.max_chars:
            if kept_anchors:
                kept_anchors.pop()
            elif kept_fragment:
                # Frase unica: encurtar pelo meio viraria instrucao truncada.
                kept_fragment = ""
            elif kept_negative:
                kept_negative.pop()
            else:
                break  # so restou o corpo, e ele ja foi validado contra o teto

        return kept_anchors, kept_fragment, kept_negative
