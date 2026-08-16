"""A fila de geracao: politica, prompt, referencia e API num unico caminho.

Este modulo e o ponto onde o dinheiro sai. Por isso ele tem duas travas, nesta
ordem, e nenhuma das duas e opcional:

  1. `guardrails.enforce` roda ANTES de qualquer chamada a API. Job bloqueado
     vira `BLOCKED` com a regra e o remedio em `blocked_reason` e nao consome um
     centavo do orcamento.
  2. `--budget-usd` e teto RIGIDO. Antes de cada job a fila soma o gasto
     acumulado com o custo estimado do proximo; se passar do teto, ela PARA e
     reporta quantos jobs ficaram na fila. Nunca "tenta o ultimo".

O plano semanal (`plans/*.yaml`) e resolvido na hora em que entra na fila: o
prompt final e composto e persistido em `jobs.resolved_prompt`, e os guardrails
sao avaliados ali mesmo. Um job que ja nasce bloqueado nasce com status
`BLOCKED`; ele nunca chega a ser candidato a uma chamada de API.

Sobre custo: a API da xAI nao devolve o valor cobrado na resposta de imagem (e
este ambiente nao tem egress para confirmar o contrario). Enquanto isso,
`generations.cost_usd` e `jobs.cost_usd` guardam a ESTIMATIVA de
`cie.pricing`, calculada por imagem efetivamente devolvida. No dia em que a
sondagem (`scripts/probe_api.py`) provar que existe um campo de custo na
resposta, e so trocar `_image_cost` por ele - o resto do sistema ja le o custo
do banco, nao do catalogo.

A composicao local com recorte real (`cie.compositor`) NAO passa por aqui: a
tabela `jobs` e contrato fechado e nao tem coluna para a intencao de compor,
entao a fila reavalia cada job no modo estrito (`use_compositor=False`). Isso e
deliberado: sem prova persistida de que o rotulo real vem de um PNG recortado,
a fila nao pode liberar uma embalagem para a difusao inventar.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, Sequence

import yaml

from . import capabilities as capabilities_module
from . import guardrails, pricing, repository
from .capabilities import ApiCapabilities
from .compositor import list_cutouts, suggest_cutout_for_sku
from .config import Settings, redact
from .enums import AspectRatio, JobStatus
from .errors import CieError, GuardrailViolation, XaiApiError
from .guardrails import GuardrailContext, GuardrailReport
from .imaging import sha256_bytes
from .models import Asset, Generation, Job, StyleDna, Template
from .prompt import PromptComposer
from .reference import RequestPayload, choose_strategy
from .utils import utcnow
from .xai import ImageRequest, ImageResponse, XaiClient

#: Chaves aceitas na raiz do YAML do plano.
PLAN_ROOT_KEYS: frozenset[str] = frozenset({"name", "notes", "jobs"})

#: Chaves aceitas em cada entrada do plano. Chave desconhecida e erro: um
#: `referece_assets` com typo viraria job sem referencia nenhuma, silenciosamente.
PLAN_ENTRY_KEYS: frozenset[str] = frozenset(
    {
        "template",
        "dna",
        "n",
        "aspect_ratio",
        "model",
        "variables",
        "reference_assets",
        "use_compositor",
        "notes",
    }
)

#: Teto do texto guardado em `jobs.blocked_reason` quando a API falha. O corpo
#: bruto ja chega truncado do cliente; isto so evita que uma pilha de mensagens
#: encadeadas vire um campo de banco gigante.
MAX_FAILURE_CHARS = 4000

#: Tolerancia do teto de orcamento. Sem ela, tres jobs de US$ 0.02 somariam
#: 0.060000000000000005 em ponto flutuante e a fila recusaria o terceiro job
#: contra um teto de exatamente US$ 0.06.
BUDGET_EPSILON = 1e-9

#: Assinaturas de arquivo que a fila reconhece ao gravar o que a API devolveu.
_IMAGE_MAGIC: tuple[tuple[bytes, str], ...] = (
    (b"\x89PNG\r\n\x1a\n", ".png"),
    (b"\xff\xd8\xff", ".jpg"),
    (b"GIF87a", ".gif"),
    (b"GIF89a", ".gif"),
)

_HEIF_BRANDS: frozenset[bytes] = frozenset({b"heic", b"heix", b"hevc", b"mif1", b"msf1"})


class ImageClient(Protocol):
    """O que a fila precisa de um cliente da API. `XaiClient` satisfaz;
    o teste injeta um duble com a mesma assinatura e nada de rede."""

    async def generate_images(self, request: ImageRequest) -> ImageResponse: ...


# --------------------------------------------------------------------------- #
# plano semanal
# --------------------------------------------------------------------------- #


@dataclass
class PlanEntry:
    """Uma linha do plano: a cena, o estilo e a tiragem pretendidos."""

    template: str
    dna: str | None = None
    n: int = 1
    aspect_ratio: str | None = None
    model: str | None = None
    variables: dict[str, str] = field(default_factory=dict)
    reference_assets: list[int] = field(default_factory=list)
    #: Trilha de composicao local (rotulo real por cima de fundo gerado). Vale
    #: para os guardrails na hora de montar o job; ver a nota no topo do modulo.
    use_compositor: bool = False


def _plan_error(path: Path, message: str) -> CieError:
    """Todo erro de plano carrega o caminho: quem edita o YAML precisa saber qual."""
    return CieError(f"{path}: {message}")


def _entry_int(value: Any, name: str, path: Path, index: int) -> int:
    # `bool` e subclasse de int em Python; aceitar `n: true` seria silencio.
    if isinstance(value, bool) or not isinstance(value, int):
        raise _plan_error(
            path, f"entrada {index}: {name} precisa ser inteiro, veio {value!r}"
        )
    return value


def _entry_text(value: Any, name: str, path: Path, index: int) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise _plan_error(
            path, f"entrada {index}: {name} precisa ser texto nao vazio, veio {value!r}"
        )
    return value.strip()


def _entry_variables(value: Any, path: Path, index: int) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise _plan_error(
            path,
            f"entrada {index}: variables precisa ser um mapeamento, "
            f"veio {type(value).__name__}",
        )
    resolved: dict[str, str] = {}
    for key, item in value.items():
        if item is None:
            raise _plan_error(
                path, f"entrada {index}: variables[{key!r}] esta vazio"
            )
        resolved[str(key)] = str(item)
    return resolved


def _entry_reference_assets(value: Any, path: Path, index: int) -> list[int]:
    if value is None:
        return []
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
        raise _plan_error(
            path,
            f"entrada {index}: reference_assets precisa ser uma lista de ids, "
            f"veio {type(value).__name__}",
        )
    ids: list[int] = []
    for item in value:
        if isinstance(item, bool) or not isinstance(item, int):
            raise _plan_error(
                path,
                f"entrada {index}: reference_assets aceita so id inteiro, veio {item!r}",
            )
        ids.append(item)
    return ids


def _build_entry(data: Any, path: Path, index: int) -> PlanEntry:
    if not isinstance(data, dict):
        raise _plan_error(
            path,
            f"entrada {index}: cada job precisa ser um mapeamento, "
            f"veio {type(data).__name__}",
        )
    unknown = sorted(set(map(str, data)) - PLAN_ENTRY_KEYS)
    if unknown:
        raise _plan_error(
            path,
            f"entrada {index}: chaves desconhecidas: {', '.join(unknown)} "
            f"(aceitas: {', '.join(sorted(PLAN_ENTRY_KEYS))})",
        )

    template = _entry_text(data.get("template"), "template", path, index)
    if not template:
        raise _plan_error(path, f"entrada {index}: campo obrigatorio ausente: template")

    aspect_ratio = _entry_text(data.get("aspect_ratio"), "aspect_ratio", path, index)
    if aspect_ratio is not None:
        try:
            AspectRatio(aspect_ratio)
        except ValueError:
            accepted = ", ".join(item.value for item in AspectRatio)
            raise _plan_error(
                path,
                f"entrada {index}: aspect_ratio invalido: {aspect_ratio!r} "
                f"(aceitos: {accepted})",
            ) from None

    use_compositor = data.get("use_compositor", False)
    if not isinstance(use_compositor, bool):
        raise _plan_error(
            path,
            f"entrada {index}: use_compositor precisa ser true ou false, "
            f"veio {use_compositor!r}",
        )

    n = _entry_int(data.get("n", 1), "n", path, index)
    if n < 1:
        raise _plan_error(path, f"entrada {index}: n precisa ser pelo menos 1, veio {n}")

    return PlanEntry(
        template=template,
        dna=_entry_text(data.get("dna"), "dna", path, index),
        n=n,
        aspect_ratio=aspect_ratio,
        model=_entry_text(data.get("model"), "model", path, index),
        variables=_entry_variables(data.get("variables"), path, index),
        reference_assets=_entry_reference_assets(
            data.get("reference_assets"), path, index
        ),
        use_compositor=use_compositor,
    )


def load_plan(path: Path | str) -> list[PlanEntry]:
    """Le o YAML do plano semanal. Aceita `{jobs: [...]}` ou uma lista na raiz."""
    path = Path(path)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise _plan_error(path, f"nao foi possivel ler o plano: {exc}") from exc

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise _plan_error(path, f"YAML malformado: {exc}") from exc

    if data is None:
        raise _plan_error(path, "plano vazio")

    if isinstance(data, list):
        items: Any = data
    elif isinstance(data, dict):
        unknown = sorted(set(map(str, data)) - PLAN_ROOT_KEYS)
        if unknown:
            raise _plan_error(
                path,
                f"chaves desconhecidas na raiz: {', '.join(unknown)} "
                f"(aceitas: {', '.join(sorted(PLAN_ROOT_KEYS))})",
            )
        if "jobs" not in data:
            raise _plan_error(path, "falta a lista 'jobs' na raiz do plano")
        items = data["jobs"]
    else:
        raise _plan_error(
            path,
            f"a raiz do plano precisa ser um mapeamento com 'jobs' ou uma lista, "
            f"veio {type(data).__name__}",
        )

    if not isinstance(items, list):
        raise _plan_error(
            path, f"'jobs' precisa ser uma lista, veio {type(items).__name__}"
        )
    if not items:
        raise _plan_error(path, "'jobs' esta vazio: nao ha o que enfileirar")

    return [_build_entry(item, path, index) for index, item in enumerate(items, start=1)]


# --------------------------------------------------------------------------- #
# montagem de um job
# --------------------------------------------------------------------------- #


def _require_template(conn: sqlite3.Connection, name: str) -> Template:
    template = repository.get_template_by_name(conn, name)
    if template is None:
        known = ", ".join(item.name for item in repository.list_templates(conn))
        raise CieError(
            f"template '{name}' nao existe no catalogo. "
            f"Rode `cie templates sync` e escolha entre: {known or '(nenhum)'}"
        )
    return template


def _require_dna(conn: sqlite3.Connection, name: str | None) -> StyleDna | None:
    if not name:
        return None
    dna = repository.get_style_dna_by_name(conn, name)
    if dna is None:
        known = ", ".join(item.name for item in repository.list_style_dna(conn))
        raise CieError(
            f"Style DNA '{name}' nao existe. Destile um com `cie dna build` "
            f"ou escolha entre: {known or '(nenhum)'}"
        )
    return dna


def _require_assets(conn: sqlite3.Connection, ids: Sequence[int]) -> list[Asset]:
    if not ids:
        return []
    assets = repository.list_assets(conn, ids=list(ids))
    missing = sorted(set(ids) - {a.id for a in assets if a.id is not None})
    if missing:
        raise CieError(
            "asset(s) de referencia inexistente(s): "
            f"{', '.join(str(i) for i in missing)}. "
            "Confira os ids com `cie assets list --reference`."
        )
    return assets


def _resolve_aspect_ratio(value: str | None, template: Template) -> AspectRatio:
    if not value:
        return template.default_aspect_ratio
    try:
        return AspectRatio(value)
    except ValueError:
        accepted = ", ".join(item.value for item in AspectRatio)
        raise CieError(
            f"aspect ratio invalido: {value!r} (aceitos: {accepted})"
        ) from None


def _cutout_available(
    settings: Settings, assets: Sequence[Asset], variables: dict[str, str]
) -> bool:
    """Existe recorte PNG real para o SKU em jogo?

    O SKU nao mora no template: vem da variavel `sku` do plano ou do asset de
    referencia. Sem nenhum dos dois, a pergunta vira "existe algum recorte?" -
    o suficiente para o guardrail sugerir a trilha de composicao local.
    """
    sku = variables.get("sku") or next(
        (asset.sku for asset in assets if asset.sku), None
    )
    if sku:
        return suggest_cutout_for_sku(settings, sku) is not None
    return bool(list_cutouts(settings))


def _context(
    settings: Settings,
    *,
    template: Template,
    assets: Sequence[Asset],
    style_dna: StyleDna | None,
    capabilities: ApiCapabilities,
    model: str,
    n: int,
    aspect_ratio: AspectRatio,
    use_compositor: bool,
    variables: dict[str, str],
) -> GuardrailContext:
    return GuardrailContext(
        template=template,
        assets=list(assets),
        style_dna=style_dna,
        capabilities=capabilities,
        model=model,
        n=n,
        aspect_ratio=aspect_ratio,
        use_compositor=use_compositor,
        has_cutout_available=_cutout_available(settings, assets, variables),
    )


def blocked_reason(report: GuardrailReport) -> str:
    """Texto de `jobs.blocked_reason`: regra, motivo e remedio, como na excecao."""
    blocks: list[str] = []
    for result in report.blocking:
        text = f"[{result.rule}] {result.message}"
        if result.remedy:
            text += f"\n  como resolver: {result.remedy}"
        blocks.append(text)
    return "\n".join(blocks)


def build_job(
    conn: sqlite3.Connection,
    settings: Settings,
    entry: PlanEntry,
    *,
    capabilities: ApiCapabilities | None = None,
) -> tuple[Job, GuardrailReport, RequestPayload]:
    """Resolve prompt, estrategia e politica de uma entrada, sem gravar nada.

    E o mesmo caminho do `--dry-run` do `cie generate` e do `cie queue add`:
    o que a fila executa depois e exatamente o que este passo mostrou.
    """
    caps = capabilities if capabilities is not None else capabilities_module.load(settings)

    template = _require_template(conn, entry.template)
    style_dna = _require_dna(conn, entry.dna)
    assets = _require_assets(conn, entry.reference_assets)
    model = (entry.model or pricing.DEFAULT_MODEL).strip()
    aspect_ratio = _resolve_aspect_ratio(entry.aspect_ratio, template)

    composed = PromptComposer().compose(
        template, variables=entry.variables, style_dna=style_dna
    )

    report = guardrails.evaluate(
        _context(
            settings,
            template=template,
            assets=assets,
            style_dna=style_dna,
            capabilities=caps,
            model=model,
            n=entry.n,
            aspect_ratio=aspect_ratio,
            use_compositor=entry.use_compositor,
            variables=entry.variables,
        )
    )

    strategy = choose_strategy(caps, style_dna)
    try:
        payload = strategy.apply(
            composed,
            assets,
            model=model,
            n=entry.n,
            aspect_ratio=str(aspect_ratio),
        )
    except CieError:
        # Referencia ilegivel ou sondagem incoerente. Se o job ja estava
        # bloqueado por politica, a violacao explica melhor o que fazer.
        report.raise_if_blocked()
        raise

    job = Job(
        template_id=template.id,
        style_dna_id=style_dna.id if style_dna else None,
        reference_asset_ids=list(payload.reference_asset_ids),
        resolved_prompt=payload.prompt,
        model=model,
        aspect_ratio=aspect_ratio,
        n=entry.n,
        status=JobStatus.BLOCKED if report.blocked else JobStatus.QUEUED,
        blocked_reason=blocked_reason(report) if report.blocked else None,
    )
    return job, report, payload


def add_jobs_from_plan(
    conn: sqlite3.Connection,
    settings: Settings,
    path: Path | str,
    *,
    dry_run: bool = False,
) -> list[Job]:
    """Enfileira o plano inteiro. Job bloqueado entra como `BLOCKED`, nunca some.

    Todos os jobs sao montados antes de qualquer INSERT: um plano com uma
    entrada torta nao deixa metade da semana no banco.
    """
    entries = load_plan(path)
    caps = capabilities_module.load(settings)

    built: list[Job] = []
    for index, entry in enumerate(entries, start=1):
        try:
            job, _report, _payload = build_job(conn, settings, entry, capabilities=caps)
        except CieError as exc:
            raise _plan_error(
                Path(path),
                f"entrada {index} (template '{entry.template}'): {exc}",
            ) from exc
        built.append(job)

    if dry_run:
        return built

    stored: list[Job] = []
    for job in built:
        job_id = repository.insert_job(conn, job)
        # Reler garante que quem chamou ve exatamente o que ficou no banco
        # (id, created_at e o status ja normalizado).
        saved = repository.get_job(conn, job_id)
        stored.append(saved if saved is not None else job)
    return stored


def estimate_queue_cost(conn: sqlite3.Connection, *, limit: int | None = None) -> float:
    """Quanto custaria esvaziar a fila hoje, pelo catalogo de precos."""
    jobs = repository.list_jobs(conn, status=JobStatus.QUEUED, limit=limit)
    return round(sum(pricing.estimate_cost(job.model, job.n) for job in jobs), 6)


# --------------------------------------------------------------------------- #
# execucao
# --------------------------------------------------------------------------- #


@dataclass
class RunResult:
    """Resumo de uma passada da fila.

    `attempted` conta os jobs que chegaram (ou chegariam, em modo seco) a API;
    job bloqueado por guardrail nao e tentativa, porque nunca gasta credito.
    """

    attempted: int = 0
    done: int = 0
    failed: int = 0
    blocked: int = 0
    skipped_budget: int = 0
    spent_usd: float = 0.0
    pending: int = 0
    stopped_by_budget: bool = False
    #: Campos de apoio ao modo seco, onde `spent_usd` fica zerado por definicao.
    dry_run: bool = False
    estimated_usd: float = 0.0

    def summary_lines(self) -> list[str]:
        """Linhas prontas para a CLI. Sem colchetes: a saida passa pelo rich."""
        lines: list[str] = []
        if self.dry_run:
            lines.append("modo seco: a API nao foi chamada e nada foi gravado")
            lines.append(f"jobs que iriam para a API: {self.attempted}")
            lines.append(f"custo estimado: US$ {self.estimated_usd:.4f}")
        else:
            lines.append(f"jobs tentados: {self.attempted}")
            lines.append(
                f"concluidos: {self.done}   falhos: {self.failed}   "
                f"bloqueados: {self.blocked}"
            )
            lines.append(f"gasto: US$ {self.spent_usd:.4f}")
        lines.append(f"pendentes na fila: {self.pending}")
        if self.stopped_by_budget:
            lines.append(
                f"teto de orcamento atingido: {self.skipped_budget} job(s) nao "
                "foram tentados nesta rodada"
            )
        return lines


def _failure_reason(exc: BaseException) -> str:
    """Preserva a resposta bruta da API, sempre passada por `config.redact`."""
    parts = [f"{type(exc).__name__}: {exc}"]
    raw = getattr(exc, "raw", "")
    if isinstance(raw, str) and raw.strip():
        parts.append(raw)
    return redact("\n".join(parts))[:MAX_FAILURE_CHARS]


def _image_extension(data: bytes) -> str:
    """Extensao pela assinatura do arquivo, nunca por chute.

    Bytes que nao sao imagem reconhecida viram falha: gravar `.png` por cima de
    um corpo de erro esconderia o problema atras de um arquivo ilegivel.
    """
    for magic, suffix in _IMAGE_MAGIC:
        if data.startswith(magic):
            return suffix
    if len(data) >= 12:
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            return ".webp"
        if data[4:8] == b"ftyp":
            brand = data[8:12].lower()
            if brand.startswith(b"avi"):
                return ".avif"
            if brand in _HEIF_BRANDS:
                return ".heic"
    raise XaiApiError(
        "a API devolveu bytes que nao sao uma imagem reconhecida "
        "(png, jpeg, webp, gif, avif ou heic); nada foi gravado",
        raw=data[:16].hex(),
    )


def _store_image(settings: Settings, data: bytes, suffix: str) -> tuple[Path, str]:
    """Grava a imagem com nome derivado do sha256 (enderecamento por conteudo).

    Bytes identicos viram o mesmo arquivo: a API repetindo uma imagem nao
    duplica disco, e o nome ja e a prova de integridade do que foi baixado.
    """
    digest = sha256_bytes(data)
    directory = settings.generations_dir
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{digest}{suffix}"
    if not path.exists():
        path.write_bytes(data)
    return path, digest


def _reference_assets_for_policy(
    conn: sqlite3.Connection, job: Job, style_dna: StyleDna | None
) -> list[Asset]:
    """Assets que contam como referencia PEDIDA, e nao como rastro herdado.

    A estrategia descritiva copia para o job os assets que originaram o Style
    DNA - proveniencia, nao pixel enviado. Reavaliar as regras de referencia em
    cima desse rastro bloquearia um job que nasceu limpo (um DNA com quatro
    fotos estouraria `MAX_REFERENCE_IMAGES` na hora de rodar), entao a lista
    herdada por inteiro sai da conta. Qualquer outra combinacao e pedido
    explicito e volta para o crivo dos guardrails.
    """
    ids = list(job.reference_asset_ids)
    if not ids:
        return []
    if style_dna is not None and set(ids) == set(style_dna.source_asset_ids):
        return []
    return repository.list_assets(conn, ids=ids)


def _image_cost(model: str) -> float:
    """Custo de UMA imagem. Estimativa do catalogo ate a sondagem confirmar o
    preco real; a resposta da API de imagem nao traz valor cobrado hoje."""
    return pricing.estimate_cost(model, 1)


async def run_queue(
    conn: sqlite3.Connection,
    settings: Settings,
    *,
    limit: int = 20,
    budget_usd: float | None = None,
    client: ImageClient | None = None,
    capabilities: ApiCapabilities | None = None,
    dry_run: bool = False,
) -> RunResult:
    """Executa a fila respeitando politica e teto de orcamento.

    Em `dry_run` nada e gravado e nada e chamado: a passada existe para mostrar
    quais jobs iriam para a API, quanto custariam e o que os guardrails dizem.
    """
    caps = capabilities if capabilities is not None else capabilities_module.load(settings)
    jobs = repository.list_jobs(conn, status=JobStatus.QUEUED, limit=limit)
    result = RunResult(dry_run=dry_run)

    #: Gasto que conta para o teto: custo real dos jobs executados, ou a
    #: estimativa em modo seco (onde nada e cobrado, mas a simulacao precisa
    #: parar no mesmo ponto que a execucao pararia).
    committed = 0.0
    owned_client: Any = None
    active = client

    try:
        for index, job in enumerate(jobs):
            if job.id is None:  # pragma: no cover - linha vinda do banco sempre tem id
                continue

            # 1. politica, sempre antes de qualquer chamada e de qualquer gasto.
            try:
                template = _require_template_by_id(conn, job)
                style_dna = (
                    repository.get_style_dna(conn, job.style_dna_id)
                    if job.style_dna_id
                    else None
                )
                assets = _reference_assets_for_policy(conn, job, style_dna)
                guardrails.enforce(
                    _context(
                        settings,
                        template=template,
                        assets=assets,
                        style_dna=style_dna,
                        capabilities=caps,
                        model=job.model,
                        n=job.n,
                        aspect_ratio=job.aspect_ratio,
                        # A intencao de compor localmente nao e persistivel no
                        # esquema; a fila reavalia no modo estrito (ver o topo).
                        use_compositor=False,
                        variables={},
                    )
                )
            except GuardrailViolation as exc:
                result.blocked += 1
                if not dry_run:
                    repository.update_job(
                        conn,
                        job.id,
                        status=JobStatus.BLOCKED,
                        blocked_reason=str(exc),
                        finished_at=utcnow(),
                    )
                continue
            except CieError as exc:
                # Template apagado, asset ilegivel: o job nao tem como rodar, mas
                # tambem nao chegou a API - nao houve tentativa nem custo.
                result.failed += 1
                if not dry_run:
                    repository.update_job(
                        conn,
                        job.id,
                        status=JobStatus.FAILED,
                        blocked_reason=_failure_reason(exc),
                        finished_at=utcnow(),
                    )
                continue

            # 2. teto rigido: nunca estoura, nunca "tenta o ultimo".
            estimated = pricing.estimate_cost(job.model, job.n)
            if budget_usd is not None and committed + estimated > budget_usd + BUDGET_EPSILON:
                result.stopped_by_budget = True
                result.skipped_budget = len(jobs) - index
                break

            result.attempted += 1
            result.estimated_usd = round(result.estimated_usd + estimated, 6)

            if dry_run:
                committed += estimated
                continue

            if active is None:
                # Construido so agora: fila vazia ou toda bloqueada nao exige chave.
                owned_client = XaiClient()
                active = owned_client

            strategy = choose_strategy(caps, style_dna)
            repository.update_job(
                conn, job.id, status=JobStatus.RUNNING, attempts=job.attempts + 1
            )

            try:
                payload = strategy.apply(
                    job.resolved_prompt,
                    assets,
                    model=job.model,
                    n=job.n,
                    aspect_ratio=str(job.aspect_ratio),
                )
                request = payload.to_image_request()
                # Seed so viaja depois que a sondagem provar que o campo existe;
                # o id do job mantem a mesma fila reproduzivel.
                request.seed = job.id if caps.supports_seed else None

                response = await active.generate_images(request)
                spent = _persist_generations(conn, settings, job, payload, request, response)
            except Exception as exc:  # noqa: BLE001 - a falha vira estado, nunca silencio
                repository.update_job(
                    conn,
                    job.id,
                    status=JobStatus.FAILED,
                    blocked_reason=_failure_reason(exc),
                    finished_at=utcnow(),
                )
                result.failed += 1
                continue

            repository.update_job(
                conn,
                job.id,
                status=JobStatus.DONE,
                cost_usd=spent,
                finished_at=utcnow(),
            )
            committed += spent
            result.spent_usd = round(result.spent_usd + spent, 6)
            result.done += 1
    finally:
        if owned_client is not None:
            await owned_client.aclose()

    pending = repository.count_jobs(conn, JobStatus.QUEUED)
    # Modo seco nao move nada no banco; o pendente reportado desconta o que a
    # simulacao teria tirado da fila.
    result.pending = max(0, pending - result.attempted) if dry_run else pending
    return result


def _require_template_by_id(conn: sqlite3.Connection, job: Job) -> Template:
    template = repository.get_template(conn, job.template_id)
    if template is None:
        raise CieError(
            f"job {job.id}: o template {job.template_id} nao existe mais no "
            "catalogo; rode `cie templates sync` antes de reenfileirar"
        )
    return template


def _persist_generations(
    conn: sqlite3.Connection,
    settings: Settings,
    job: Job,
    payload: RequestPayload,
    request: ImageRequest,
    response: ImageResponse,
) -> float:
    """Grava as imagens e as linhas de `generations`. Devolve o custo do job.

    O custo e contado por imagem efetivamente devolvida: se a API entregar
    menos que `n`, o job nao debita o que nao veio.

    Todos os corpos sao decodificados e reconhecidos ANTES de qualquer gravacao:
    assim uma resposta meio quebrada falha o job inteiro, em vez de deixar
    metade da tiragem no disco e a outra metade num erro.
    """
    model = response.model or job.model
    per_image = _image_cost(job.model)
    blobs = [image.to_bytes() for image in response.images]
    decoded = [(data, _image_extension(data)) for data in blobs]

    total = 0.0
    for data, suffix in decoded:
        path, digest = _store_image(settings, data, suffix)
        repository.insert_generation(
            conn,
            Generation(
                job_id=job.id,
                path=str(path),
                sha256=digest,
                model=model,
                prompt=payload.prompt,
                seed=request.seed,
                cost_usd=per_image,
                # Politica da casa: nenhuma saida do CIE dispensa rotulagem de IA.
                disclosure_required=True,
            ),
        )
        total += per_image
    return round(total, 6)


__all__ = [
    "BUDGET_EPSILON",
    "MAX_FAILURE_CHARS",
    "ImageClient",
    "PlanEntry",
    "RunResult",
    "add_jobs_from_plan",
    "blocked_reason",
    "build_job",
    "estimate_queue_cost",
    "load_plan",
    "run_queue",
]
