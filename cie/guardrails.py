"""Camada de politica: decide o que NAO pode ser gerado, antes de gastar credito.

Este modulo e a traducao executavel do principio do projeto: "a IA edita e
estende o real; a IA nao inventa o real". Toda chamada de geracao passa por
`enforce()` antes de tocar a API - se uma regra bloqueia, o credito nunca e
gasto e a mensagem diz QUAL regra caiu e COMO resolver.

Convencao de emissao adotada aqui:
  * regras de severidade BLOCK sempre emitem um resultado, mesmo quando passam
    (o `--dry-run` da CLI mostra a checagem inteira, nao so o que falhou);
  * regras WARN/INFO so emitem quando tem algo a dizer, entao a presenca de uma
    linha WARN no relatorio ja significa "olhe para isto".

A ordem de `RULES` e deliberada: as regras de politica de pessoas vem primeiro,
para que `raise_if_blocked()` levante sempre a violacao mais grave.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Callable

from . import pricing
from .capabilities import ApiCapabilities
from .enums import AspectRatio, RiskFlag, TemplateKind
from .errors import GuardrailViolation
from .models import Asset, StyleDna, Template

#: Teto de referencias por job. Acima disto o modelo mistura as fotos e o
#: resultado deixa de ser rastreavel a uma imagem real especifica.
MAX_REFERENCE_IMAGES = 3
#: Teto duro de imagens por job, independente do que o catalogo prometer.
MAX_IMAGES_PER_JOB = 10

#: Onde a sondagem empirica da API mora (citado nos remedies).
PROBE_SCRIPT = "scripts/probe_api.py"


class Severity(StrEnum):
    """BLOCK impede a geracao; WARN vai para a revisao humana; INFO e rastro."""

    BLOCK = "block"
    WARN = "warn"
    INFO = "info"


@dataclass
class GuardrailContext:
    """Tudo que as regras precisam saber sobre a geracao pretendida."""

    template: Template
    #: Assets pretendidos como referencia (ja carregados do catalogo).
    assets: list[Asset] = field(default_factory=list)
    style_dna: StyleDna | None = None
    capabilities: ApiCapabilities | None = None
    model: str = pricing.DEFAULT_MODEL
    n: int = 1
    aspect_ratio: AspectRatio = AspectRatio.R1_1
    #: Trilha de composicao local (Pillow): o rotulo real vem de um recorte PNG.
    use_compositor: bool = False
    #: Existe recorte do SKU em assets/cutouts/ para essa composicao.
    has_cutout_available: bool = False


@dataclass
class GuardrailResult:
    rule: str
    severity: Severity
    passed: bool
    message: str
    remedy: str = ""


@dataclass
class GuardrailReport:
    results: list[GuardrailResult] = field(default_factory=list)

    @property
    def blocking(self) -> list[GuardrailResult]:
        return [r for r in self.results if r.severity is Severity.BLOCK and not r.passed]

    @property
    def warnings(self) -> list[GuardrailResult]:
        return [r for r in self.results if r.severity is Severity.WARN and not r.passed]

    @property
    def infos(self) -> list[GuardrailResult]:
        return [r for r in self.results if r.severity is Severity.INFO]

    @property
    def blocked(self) -> bool:
        return bool(self.blocking)

    @property
    def disclosure_required(self) -> bool:
        """Constante por politica: nenhuma saida do CIE dispensa rotulagem de IA.

        E propriedade (e nao um literal solto no chamador) para que o pipeline e
        a CLI leiam a regra de um lugar so; o default seguro e "exige".
        """
        return True

    @property
    def typography_review_required(self) -> bool:
        """A aprovacao precisa conferir logotipo e texto do rotulo letra a letra."""
        return any(r.rule == "packaging_typography_review" for r in self.results)

    def raise_if_blocked(self) -> None:
        for result in self.blocking:
            raise GuardrailViolation(result.rule, result.message, result.remedy)

    def as_rows(self) -> list[dict[str, object]]:
        """Linhas prontas para a tabela do `--dry-run` (chaves em portugues,
        como em `pricing.catalog_rows`)."""
        return [
            {
                "regra": r.rule,
                "severidade": str(r.severity),
                "ok": r.passed,
                "mensagem": r.message,
                "como_resolver": r.remedy,
            }
            for r in self.results
        ]


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #


def _block(rule: str, *, passed: bool, message: str, remedy: str = "") -> GuardrailResult:
    return GuardrailResult(
        rule=rule, severity=Severity.BLOCK, passed=passed, message=message, remedy=remedy
    )


def _warn(rule: str, message: str, remedy: str = "") -> GuardrailResult:
    return GuardrailResult(
        rule=rule, severity=Severity.WARN, passed=False, message=message, remedy=remedy
    )


def _info(rule: str, message: str, remedy: str = "") -> GuardrailResult:
    return GuardrailResult(
        rule=rule, severity=Severity.INFO, passed=True, message=message, remedy=remedy
    )


def _label(asset: Asset) -> str:
    name = Path(asset.path).name
    return f"#{asset.id} {name}" if asset.id is not None else name


def _labels(assets: list[Asset]) -> str:
    return ", ".join(_label(a) for a in assets)


# --------------------------------------------------------------------------- #
# regras
# --------------------------------------------------------------------------- #


def rule_no_synthetic_identifiable_faces(ctx: GuardrailContext) -> GuardrailResult:
    """1. Pessoa real identificavel so entra no pipeline com consentimento em arquivo."""
    offenders = [
        a for a in ctx.assets if a.has_identifiable_person and not a.consent_on_file
    ]
    if offenders:
        return _block(
            "no_synthetic_identifiable_faces",
            passed=False,
            message=(
                "referencia com pessoa identificavel e sem consentimento registrado: "
                f"{_labels(offenders)}. A IA nao sintetiza rosto de pessoa real."
            ),
            remedy=(
                "registre o termo assinado com `cie assets curate <id> --consent`; "
                "se a foto nao tem rosto identificavel, corrija com "
                "`cie assets curate <id> --no-person`; ou troque a referencia."
            ),
        )
    return _block(
        "no_synthetic_identifiable_faces",
        passed=True,
        message="nenhuma referencia com pessoa identificavel sem consentimento",
    )


def rule_face_regeneration_forbidden(ctx: GuardrailContext) -> GuardrailResult:
    """2. Regeneracao de rosto e proibida mesmo com consentimento assinado.

    Consentimento autoriza usar a foto, nao autoriza recriar o rosto da pessoa:
    por isso esta regra ignora `consent_on_file` e olha so para a presenca de
    pessoa identificavel.
    """
    rule = "face_regeneration_forbidden"
    if RiskFlag.FACE_REGENERATION not in ctx.template.risk_flags:
        return _block(
            rule, passed=True, message="template nao pede regeneracao de rosto"
        )
    people = [a for a in ctx.assets if a.has_identifiable_person]
    if people:
        return _block(
            rule,
            passed=False,
            message=(
                f"o template '{ctx.template.name}' tem a risk_flag "
                f"{RiskFlag.FACE_REGENERATION} e recebeu referencia com pessoa "
                f"identificavel: {_labels(people)}. Rosto de pessoa real nunca e "
                "regenerado, nem com consentimento assinado."
            ),
            remedy=(
                "refotografe a cena, ou use enquadramento sem rosto (de costas, "
                "maos, silhueta, sombra), ou retire a flag face_regeneration do "
                "template se ele de fato nao mexe em rosto."
            ),
        )
    return _block(
        rule,
        passed=True,
        message="template de regeneracao sem nenhuma referencia com pessoa identificavel",
    )


def rule_packaging_requires_reference(
    ctx: GuardrailContext,
) -> GuardrailResult | list[GuardrailResult]:
    """3. Rotulo e logotipo vem do real: exige referencia ou composicao local."""
    rule = "packaging_requires_reference"
    template = ctx.template

    if not (template.requires_reference or template.touches_packaging):
        return _block(rule, passed=True, message="template nao exige referencia real")

    if ctx.use_compositor:
        # O rotulo entra por cima, vindo do recorte PNG; a difusao so faz o fundo.
        note = (
            "trilha de composicao local (Pillow): o rotulo real vem do recorte em "
            "assets/cutouts/, a difusao gera apenas o fundo/cena"
        )
        if not ctx.has_cutout_available:
            note += " - atencao: nenhum recorte disponivel para este SKU ainda"
        return [
            _block(
                rule,
                passed=True,
                message="composicao local dispensa referencia dentro da difusao",
            ),
            _info(rule, note),
        ]

    if not ctx.assets:
        return _block(
            rule,
            passed=False,
            message=(
                f"o template '{template.name}' exige referencia real e nenhum asset "
                "foi informado; embalagem com texto legivel nunca e gerada do zero"
            ),
            remedy=(
                "escolha referencias com `cie assets list --reference` e passe "
                "`--ref <id>`; ou rode a trilha de composicao local com `--compositor`."
            ),
        )

    if template.touches_packaging and not any(a.has_readable_packaging for a in ctx.assets):
        return _block(
            rule,
            passed=False,
            message=(
                f"o template '{template.name}' mexe em embalagem, mas nenhuma das "
                f"referencias tem embalagem legivel: {_labels(ctx.assets)}"
            ),
            remedy=(
                "inclua um packshot real do SKU (marque com "
                "`cie assets curate <id> --packaging`) ou use `--compositor` para "
                "colar o recorte real sobre o fundo gerado."
            ),
        )

    return _block(rule, passed=True, message="referencia real presente para o rotulo")


def rule_packaging_typography_review(ctx: GuardrailContext) -> GuardrailResult | None:
    """4. Difusao erra tipografia: a aprovacao humana confere o rotulo."""
    if not ctx.template.touches_packaging:
        return None
    return _warn(
        "packaging_typography_review",
        "o template mexe em texto de embalagem: modelo de difusao deforma "
        "logotipo e tipografia mesmo com referencia",
        remedy=(
            "na revisao, confira letra a letra o logotipo Cafe Canastra e o texto "
            "do rotulo; rejeite qualquer glifo estranho e prefira `--compositor` "
            "quando houver recorte do SKU."
        ),
    )


def rule_reference_quality(ctx: GuardrailContext) -> GuardrailResult:
    """5. Referencia ruim contamina a saida inteira."""
    rule = "reference_quality"
    weak = [a for a in ctx.assets if not a.is_reference_grade]
    if weak:
        return _block(
            rule,
            passed=False,
            message=(
                "referencia abaixo do padrao (is_reference_grade=0): "
                f"{_labels(weak)}"
            ),
            remedy=(
                "escolha assets de `cie assets list --reference`, ou promova o asset "
                "com `cie assets curate <id> --reference` depois de conferir nitidez "
                "e resolucao."
            ),
        )
    return _block(rule, passed=True, message="todas as referencias sao reference-grade")


def rule_max_reference_images(ctx: GuardrailContext) -> GuardrailResult:
    """6. Muitas referencias diluem o real e tiram a rastreabilidade."""
    rule = "max_reference_images"
    count = len(ctx.assets)
    if count > MAX_REFERENCE_IMAGES:
        return _block(
            rule,
            passed=False,
            message=(
                f"{count} referencias no mesmo job; o maximo aceito e "
                f"{MAX_REFERENCE_IMAGES}"
            ),
            remedy=(
                f"reduza para no maximo {MAX_REFERENCE_IMAGES} imagens (as mais "
                "proximas do enquadramento desejado) e quebre o resto em outro job."
            ),
        )
    return _block(rule, passed=True, message=f"{count} referencia(s), dentro do limite")


def rule_hands_risk(ctx: GuardrailContext) -> GuardrailResult | None:
    """7. Maos sao a deformacao classica de difusao."""
    if RiskFlag.HANDS not in ctx.template.risk_flags:
        return None
    return _warn(
        "hands_risk",
        "o template mostra maos: dedos a mais, junta invertida e unha derretida "
        "sao falhas comuns",
        remedy=(
            "prefira enquadramento que corte o pulso, mao parcialmente fora de "
            "quadro ou em movimento; confira dedo a dedo na revisao."
        ),
    )


def rule_human_face_risk(ctx: GuardrailContext) -> GuardrailResult | None:
    """8. Aviso para enquadramentos onde o rosto aparece de raspao.

    O caso duro (pessoa identificavel sem consentimento) ja cai na regra 1; aqui
    o objetivo e lembrar a revisao de olhar rosto parcial, reflexo e fundo.
    """
    if RiskFlag.HUMAN_FACE not in ctx.template.risk_flags:
        return None
    return _warn(
        "human_face_risk",
        "o template pode mostrar rosto humano: a IA nao inventa rosto de pessoa "
        "real, e rosto parcial/desfocado ainda pode parecer alguem",
        remedy=(
            "mantenha o rosto fora de quadro, de costas ou fora de foco; se o rosto "
            "for o assunto, trabalhe a partir de foto real com consentimento."
        ),
    )


def rule_aspect_ratio_supported(ctx: GuardrailContext) -> GuardrailResult:
    """9. Proporcao fora do catalogo do modelo e erro 400 pago."""
    rule = "aspect_ratio_supported"
    model = pricing.get_model(ctx.model)
    if str(ctx.aspect_ratio) not in model.aspect_ratios:
        return _block(
            rule,
            passed=False,
            message=(
                f"aspect ratio {ctx.aspect_ratio} nao consta no modelo "
                f"'{model.name}'; suportados: {', '.join(model.aspect_ratios)}"
            ),
            remedy=(
                "escolha uma proporcao da lista do modelo; proporcoes de publicacao "
                "que a API nao tem (4:5, por exemplo) saem do recorte local no export."
            ),
        )
    return _block(
        rule, passed=True, message=f"{ctx.aspect_ratio} suportado por '{model.name}'"
    )


def rule_n_within_limits(ctx: GuardrailContext) -> GuardrailResult:
    """10. n fora da faixa queima credito ou volta erro."""
    rule = "n_within_limits"
    model = pricing.get_model(ctx.model)
    limit = min(MAX_IMAGES_PER_JOB, model.max_n)
    if ctx.n < 1 or ctx.n > limit:
        return _block(
            rule,
            passed=False,
            message=(
                f"n={ctx.n} fora da faixa 1..{limit} para o modelo '{model.name}'"
            ),
            remedy=f"use um n entre 1 e {limit}, ou divida a tiragem em varios jobs.",
        )
    return _block(rule, passed=True, message=f"n={ctx.n} dentro de 1..{limit}")


def rule_prompt_body_present(ctx: GuardrailContext) -> GuardrailResult:
    """11. Prompt vazio e credito jogado fora."""
    rule = "prompt_body_present"
    if not ctx.template.body.strip():
        return _block(
            rule,
            passed=False,
            message=f"o template '{ctx.template.name}' esta com o corpo vazio",
            remedy=(
                "escreva o corpo do template (cena, luz, lente, materiais) no YAML "
                "em templates/ e recarregue com `cie templates load`."
            ),
        )
    return _block(rule, passed=True, message="corpo do template preenchido")


def rule_native_reference_capability(ctx: GuardrailContext) -> GuardrailResult | None:
    """12. Nunca bloqueia: avisa que a referencia vai virar descricao.

    Enquanto a sondagem nao provar que a API aceita imagem de referencia, o
    sistema opera em modo descritivo - o asset guia o texto do prompt, nao entra
    como pixel.
    """
    if not ctx.assets:
        return None
    caps = ctx.capabilities
    if caps is not None and caps.native_reference_supported:
        return None
    detail = caps.summary() if caps is not None else (
        f"capabilities nao carregado; a sondagem ({PROBE_SCRIPT}) nunca rodou"
    )
    return _warn(
        "native_reference_capability",
        (
            f"{len(ctx.assets)} referencia(s) informada(s), mas nao ha suporte "
            f"confirmado a imagem de referencia nativa: {detail}. O job cai na "
            "estrategia descritiva (Style DNA em texto)."
        ),
        remedy=(
            f"rode `python {PROBE_SCRIPT}` numa maquina com XAI_API_KEY e acesso a "
            "api.x.ai; ate la, confira se a descricao do Style DNA basta e use "
            "`--compositor` quando o rotulo real precisar aparecer."
        ),
    )


def rule_compositor_preferred_for_product_shot(
    ctx: GuardrailContext,
) -> GuardrailResult | None:
    """13. Havendo recorte real do SKU, compor localmente preserva o rotulo."""
    if ctx.template.kind is not TemplateKind.PRODUCT_SHOT:
        return None
    if not ctx.has_cutout_available or ctx.use_compositor:
        return None
    return _warn(
        "compositor_preferred_for_product_shot",
        "existe recorte PNG do SKU e o template e product_shot: a composicao "
        "local mantem o rotulo real intacto, a difusao nao",
        remedy="repita o comando com `--compositor` e deixe a difusao so no fundo.",
    )


def rule_disclosure_required(ctx: GuardrailContext) -> GuardrailResult:
    """14. Marca de proveniencia: sempre passa, sempre aparece no relatorio."""
    return _info(
        "disclosure_required",
        "a saida nasce com disclosure_required=1: rotule como conteudo gerado por "
        "IA no Instagram/Meta antes de publicar",
        remedy=(
            "use a marcacao de conteudo de IA da propria plataforma e mantenha a "
            "proveniencia do job (template, referencias, prompt) no registro."
        ),
    )


def rule_model_not_verified(ctx: GuardrailContext) -> GuardrailResult | None:
    """15. Preco e limites nao confirmados na doc da xAI."""
    model = pricing.get_model(ctx.model)
    if model.verified:
        return None
    return _warn(
        "model_not_verified",
        (
            f"preco e limites do modelo '{model.name}' nao verificados "
            f"(fonte: {model.source}); a estimativa de custo pode estar errada"
        ),
        remedy=(
            f"rode `python {PROBE_SCRIPT}` para gravar .cie/models.yaml; o custo "
            "real cobrado continua vindo de generations.cost_usd."
        ),
    )


#: Assinatura de uma regra. `None` significa "nada a relatar neste contexto".
Rule = Callable[[GuardrailContext], GuardrailResult | list[GuardrailResult] | None]

RULES: tuple[Rule, ...] = (
    rule_no_synthetic_identifiable_faces,
    rule_face_regeneration_forbidden,
    rule_packaging_requires_reference,
    rule_packaging_typography_review,
    rule_reference_quality,
    rule_max_reference_images,
    rule_hands_risk,
    rule_human_face_risk,
    rule_aspect_ratio_supported,
    rule_n_within_limits,
    rule_prompt_body_present,
    rule_native_reference_capability,
    rule_compositor_preferred_for_product_shot,
    rule_disclosure_required,
    rule_model_not_verified,
)


def evaluate(ctx: GuardrailContext) -> GuardrailReport:
    """Roda todas as regras e devolve o relatorio, sem levantar excecao."""
    results: list[GuardrailResult] = []
    for rule in RULES:
        outcome = rule(ctx)
        if outcome is None:
            continue
        if isinstance(outcome, GuardrailResult):
            results.append(outcome)
        else:
            results.extend(outcome)
    return GuardrailReport(results=results)


def enforce(ctx: GuardrailContext) -> GuardrailReport:
    """`evaluate` + parada dura. E este que o pipeline chama antes da API."""
    report = evaluate(ctx)
    report.raise_if_blocked()
    return report
