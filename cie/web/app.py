"""As duas UIs locais do CIE: curadoria da base real e revisao do que a IA gerou.

O humano e o gargalo deste sistema - e isso e proposital. As telas existem para
que ele decida rapido, nao para impressionar: grid denso, atalhos de teclado,
fragmento de HTML no lugar de JSON e nenhum passo de build.

Decisoes que valem registro:

  * uma conexao SQLite por request. As rotas sao sincronas, logo rodam no
    threadpool do Starlette, e conexao de sqlite3 nao atravessa thread com
    seguranca. Abrir e fechar por request e barato num banco local e elimina a
    classe inteira de bug de concorrencia.
  * progressive enhancement de verdade. Todo formulario tem `action`/`method`
    nativos alem dos atributos do HTMX: se a maquina estiver sem internet (o
    HTMX vem de CDN), a UI continua funcionando por POST + redirect 303. O
    fragmento so e devolvido quando o request veio com o cabecalho `HX-Request`.
  * o CSS embutido em `base.html` e a fonte da verdade do visual; o Tailwind do
    CDN so acrescenta utilitarios. Ferramenta interna nao pode depender de rede
    para ficar legivel.
  * `has_identifiable_person` e `consent_on_file` chegam aqui com o default
    restritivo da ingestao e a tela grita isso. Nenhuma inferencia de maquina
    encosta nesses dois campos - a UI e o unico lugar onde eles mudam.

Convencao dos formularios (a mesma em `/assets/{id}/curate` e `/assets/bulk`):
campo ausente ou vazio nao altera nada, `__clear__` grava NULL, o resto grava o
valor. Assim um form de card (que manda o estado atual inteiro) e um form de
marcacao multipla (que manda so o que o humano escolheu) passam pelo mesmo
parser. `notes` e a excecao explicita - ver `_notes_update`.
"""

from __future__ import annotations

import mimetypes
import sqlite3
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
    Response,
)
from fastapi.templating import Jinja2Templates

from .. import capabilities, repository
from ..capabilities import ApiCapabilities
from ..config import Settings, get_settings
from ..db import connect, open_db
from ..enums import JobStatus, Location, Pillar, ReviewStatus, Sku
from ..models import Asset, Generation, Job, Template
from ..reports import PILLAR_LABELS

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

#: Tamanho da pagina do grid. Denso de proposito: curadoria e trabalho de lote.
PAGE_SIZE = 60
MAX_PAGE_SIZE = 240

#: Sentinelas do protocolo de formulario descrito no docstring do modulo.
UNCHANGED = ""
CLEAR = "__clear__"

#: Marca "nao mexa neste campo" no resultado dos parsers (None ja significa NULL).
_KEEP: Any = object()

POLICY_NOTICE = (
    "Pessoa identificavel e consentimento nunca sao inferidos pela maquina: "
    "entram no default restritivo (pessoa presente, consentimento ausente) e so "
    "mudam aqui, por decisao humana. Asset com pessoa e sem consentimento nunca "
    "vira referencia."
)

PACKAGING_WARNING = (
    "ATENCAO: esta cena toca texto de embalagem. Confira o logotipo e a "
    "tipografia do rotulo letra por letra antes de aprovar - modelo de difusao "
    "erra texto com naturalidade. Se a arte nao for identica a do rotulo real, "
    "rejeite."
)

FACE_WARNING = (
    "ATENCAO: esta cena envolve rosto humano. Rosto de pessoa real nunca e "
    "sintetizado; confirme que o rosto veio da foto original antes de aprovar."
)

DISCLOSURE_LABEL = "exige rotulo de conteudo de IA no Instagram/Meta"

REJECT_REASON_REQUIRED = (
    "rejeicao exige motivo: ele alimenta o relatorio de custo e a proxima versao "
    "do template."
)

CORE_PRINCIPLE = "A IA edita e estende o real; a IA nao inventa o real."

SKU_LABELS: dict[str, str] = {
    Sku.CLASSICO.value: "Classico",
    Sku.SUAVE.value: "Suave",
    Sku.CANELA.value: "Canela",
    Sku.MICROLOTE.value: "Microlote",
    Sku.GEISHA.value: "Geisha",
    Sku.DRIP.value: "Drip coffee",
    Sku.CAPSULA.value: "Capsula",
}

LOCATION_LABELS: dict[str, str] = {
    Location.FAZENDA_MEDEIROS.value: "Fazenda - Medeiros/MG",
    Location.TORREFACAO_UBERLANDIA.value: "Torrefacao - Uberlandia",
    Location.ESTUDIO.value: "Estudio",
    Location.OUTRO.value: "Outro",
}

JOB_STATUS_LABELS: dict[str, str] = {
    JobStatus.QUEUED.value: "na fila",
    JobStatus.RUNNING.value: "rodando",
    JobStatus.DONE.value: "concluido",
    JobStatus.FAILED.value: "falhou",
    JobStatus.BLOCKED.value: "bloqueado",
}


# --------------------------------------------------------------------------- #
# infraestrutura: templates, conexao, helpers de request
# --------------------------------------------------------------------------- #

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
templates.env.filters["basename"] = lambda value: Path(str(value)).name
templates.env.globals.update(
    PILLARS=list(Pillar),
    SKUS=list(Sku),
    LOCATIONS=list(Location),
    PILLAR_LABELS=PILLAR_LABELS,
    SKU_LABELS=SKU_LABELS,
    LOCATION_LABELS=LOCATION_LABELS,
    JOB_STATUS_LABELS=JOB_STATUS_LABELS,
    POLICY_NOTICE=POLICY_NOTICE,
    PACKAGING_WARNING=PACKAGING_WARNING,
    FACE_WARNING=FACE_WARNING,
    DISCLOSURE_LABEL=DISCLOSURE_LABEL,
    CORE_PRINCIPLE=CORE_PRINCIPLE,
    CLEAR=CLEAR,
)

router = APIRouter()


def _settings_of(request: Request) -> Settings:
    return request.app.state.settings


def _conn(request: Request) -> Iterator[sqlite3.Connection]:
    """Conexao dedicada ao request; ver nota de thread-safety no topo."""
    connection = connect(_settings_of(request).db_path)
    try:
        yield connection
    finally:
        connection.close()


def _is_htmx(request: Request) -> bool:
    return request.headers.get("HX-Request", "").lower() == "true"


def _back(request: Request, fallback: str) -> RedirectResponse:
    """Sem HTMX o navegador espera navegacao: volta para a tela de origem.

    `Referer` e cabecalho de cliente, entao so o aceitamos quando aponta para a
    propria UI - redirecionar para fora daqui nunca e o que a curadoria quer.
    """
    referer = request.headers.get("referer", "")
    inside = referer.startswith(str(request.base_url))
    return RedirectResponse(referer if inside else fallback, status_code=303)


def _file_response(path_str: str | None, missing: str) -> FileResponse:
    if not path_str:
        raise HTTPException(status_code=404, detail=missing)
    path = Path(path_str)
    if not path.is_file():
        raise HTTPException(status_code=404, detail=missing)
    media_type, _ = mimetypes.guess_type(path.name)
    return FileResponse(path, media_type=media_type or "application/octet-stream")


# --------------------------------------------------------------------------- #
# parsers de formulario e de querystring
# --------------------------------------------------------------------------- #


def _parse_bool(raw: str | None, field: str) -> Any:
    value = (raw or "").strip().lower()
    if value == UNCHANGED:
        return _KEEP
    if value in ("1", "true", "on", "sim"):
        return True
    if value in ("0", "false", "off", "nao"):
        return False
    raise HTTPException(status_code=400, detail=f"valor invalido para {field}: {raw!r}")


def _parse_enum(enum_cls: Any, raw: str | None, field: str) -> Any:
    value = (raw or "").strip()
    if value == UNCHANGED:
        return _KEEP
    if value == CLEAR:
        return None
    try:
        return enum_cls(value)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"valor invalido para {field}: {raw!r}")


def _notes_update(notes: str, notes_present: str) -> dict[str, Any]:
    """`notes` e texto livre, entao a regra do vazio nao serve: apagar a
    anotacao na tela precisa chegar ao banco. O form que edita o campo declara
    isso mandando `notes_present=1`; quem nao manda simplesmente nao mexe.
    """
    if _parse_bool(notes_present, "notes_present") is not True:
        return {}
    return {"notes": notes.strip() or None}


def _curation_payload(
    *,
    pillar: str,
    sku: str,
    location: str,
    has_identifiable_person: str,
    consent_on_file: str,
    has_readable_packaging: str,
    is_reference_grade: str,
    needs_review: str,
) -> dict[str, Any]:
    """Traduz o formulario para o kwargs de `repository.update_asset_curation`."""
    candidates: dict[str, Any] = {
        "pillar": _parse_enum(Pillar, pillar, "pillar"),
        "sku": _parse_enum(Sku, sku, "sku"),
        "location": _parse_enum(Location, location, "location"),
        "has_identifiable_person": _parse_bool(
            has_identifiable_person, "has_identifiable_person"
        ),
        "consent_on_file": _parse_bool(consent_on_file, "consent_on_file"),
        "has_readable_packaging": _parse_bool(
            has_readable_packaging, "has_readable_packaging"
        ),
        "is_reference_grade": _parse_bool(is_reference_grade, "is_reference_grade"),
        "needs_review": _parse_bool(needs_review, "needs_review"),
    }
    return {k: v for k, v in candidates.items() if v is not _KEEP}


def _filter_bool(raw: str | None, field: str) -> bool | None:
    value = _parse_bool(raw, field)
    return None if value is _KEEP else bool(value)


def _filter_enum(enum_cls: Any, raw: str | None, field: str) -> Any:
    value = _parse_enum(enum_cls, raw, field)
    return None if value is _KEEP else value


# --------------------------------------------------------------------------- #
# leitura agregada para as telas
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class DashboardStats:
    """Retrato do sistema numa tela. Numeros vem todos do banco, nunca de cache."""

    assets_total: int
    assets_needs_review: int
    assets_reference_grade: int
    assets_reference_ready: int
    assets_by_pillar: list[tuple[Pillar, int]]
    jobs_by_status: list[tuple[JobStatus, int]]
    generations_pending: int
    generations_approved: int
    generations_rejected: int
    total_cost_usd: float
    capabilities: ApiCapabilities

    @property
    def probe_pending(self) -> bool:
        return not self.capabilities.probed


def collect_stats(conn: sqlite3.Connection, settings: Settings) -> DashboardStats:
    # Uma passada so pela base: local e da ordem de milhares de linhas, e assim
    # os recortes (pilar, referencia utilizavel) saem coerentes entre si.
    assets = repository.list_assets(conn)
    by_pillar = Counter(asset.pillar for asset in assets if asset.pillar is not None)

    return DashboardStats(
        assets_total=repository.count_assets(conn),
        assets_needs_review=sum(1 for a in assets if a.needs_review),
        assets_reference_grade=sum(1 for a in assets if a.is_reference_grade),
        # A diferenca entre grade e "ready" e exatamente o custo do consentimento.
        assets_reference_ready=sum(1 for a in assets if a.is_usable_as_reference),
        assets_by_pillar=[(p, by_pillar.get(p, 0)) for p in Pillar],
        jobs_by_status=[(s, repository.count_jobs(conn, s)) for s in JobStatus],
        generations_pending=len(
            repository.list_generations(conn, review_status=ReviewStatus.PENDING)
        ),
        generations_approved=len(
            repository.list_generations(conn, review_status=ReviewStatus.APPROVED)
        ),
        generations_rejected=len(
            repository.list_generations(conn, review_status=ReviewStatus.REJECTED)
        ),
        total_cost_usd=repository.total_cost(conn),
        capabilities=capabilities.load(settings),
    )


@dataclass(frozen=True)
class ReviewItem:
    """Uma imagem gerada com toda a proveniencia que a decisao humana exige."""

    generation: Generation
    job: Job | None
    template: Template | None
    references: list[Asset]
    focal: tuple[float, float] | None

    @property
    def packaging_warning(self) -> bool:
        return bool(self.template and self.template.touches_packaging)

    @property
    def face_warning(self) -> bool:
        return bool(self.template and self.template.touches_faces)


def build_review_item(conn: sqlite3.Connection, generation: Generation) -> ReviewItem:
    job = repository.get_job(conn, generation.job_id)
    template = repository.get_template(conn, job.template_id) if job else None
    references: list[Asset] = []
    if job and job.reference_asset_ids:
        references = repository.list_assets(conn, ids=job.reference_asset_ids)
    focal = (
        repository.get_focal_point(conn, generation.id)
        if generation.id is not None
        else None
    )
    return ReviewItem(
        generation=generation,
        job=job,
        template=template,
        references=references,
        focal=focal,
    )


# --------------------------------------------------------------------------- #
# painel
# --------------------------------------------------------------------------- #


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, conn: sqlite3.Connection = Depends(_conn)) -> Response:
    stats = collect_stats(conn, _settings_of(request))
    return templates.TemplateResponse(
        request, "dashboard.html", {"stats": stats, "active": "dashboard"}
    )


# --------------------------------------------------------------------------- #
# curadoria
# --------------------------------------------------------------------------- #


@router.get("/assets", response_class=HTMLResponse)
def assets_page(
    request: Request,
    conn: sqlite3.Connection = Depends(_conn),
    pillar: str = "",
    sku: str = "",
    location: str = "",
    needs_review: str = "",
    reference_grade: str = "",
    page: int = 1,
    per_page: int = PAGE_SIZE,
) -> Response:
    filters: dict[str, str] = {
        "pillar": pillar,
        "sku": sku,
        "location": location,
        "needs_review": needs_review,
        "reference_grade": reference_grade,
    }
    page = max(1, page)
    per_page = min(max(1, per_page), MAX_PAGE_SIZE)
    offset = (page - 1) * per_page

    # `list_assets` nao oferece OFFSET; pedimos uma pagina a mais e cortamos aqui.
    # A base e local e pequena, e o SQL do repositorio continua sem gambiarra.
    rows = repository.list_assets(
        conn,
        pillar=_filter_enum(Pillar, pillar, "pillar"),
        sku=_filter_enum(Sku, sku, "sku"),
        location=_filter_enum(Location, location, "location"),
        needs_review=_filter_bool(needs_review, "needs_review"),
        reference_grade=_filter_bool(reference_grade, "reference_grade"),
        limit=offset + per_page + 1,
    )
    window = rows[offset : offset + per_page]
    has_next = len(rows) > offset + per_page

    def page_url(target: int) -> str:
        query = {k: v for k, v in filters.items() if v}
        query["page"] = str(target)
        if per_page != PAGE_SIZE:
            query["per_page"] = str(per_page)
        return f"/assets?{urlencode(query)}"

    return templates.TemplateResponse(
        request,
        "assets.html",
        {
            "active": "assets",
            "assets": window,
            "filters": filters,
            "page": page,
            "per_page": per_page,
            "has_next": has_next,
            "prev_url": page_url(page - 1) if page > 1 else None,
            "next_url": page_url(page + 1) if has_next else None,
            "total": repository.count_assets(conn),
        },
    )


@router.post("/assets/{asset_id}/curate", response_class=HTMLResponse)
def curate_asset(
    request: Request,
    asset_id: int,
    conn: sqlite3.Connection = Depends(_conn),
    pillar: str = Form(UNCHANGED),
    sku: str = Form(UNCHANGED),
    location: str = Form(UNCHANGED),
    has_identifiable_person: str = Form(UNCHANGED),
    consent_on_file: str = Form(UNCHANGED),
    has_readable_packaging: str = Form(UNCHANGED),
    is_reference_grade: str = Form(UNCHANGED),
    needs_review: str = Form(UNCHANGED),
    notes: str = Form(UNCHANGED),
    notes_present: str = Form(UNCHANGED),
    mark_reviewed: str = Form(UNCHANGED),
) -> Response:
    if repository.get_asset(conn, asset_id) is None:
        raise HTTPException(status_code=404, detail=f"asset {asset_id} nao existe")

    payload = _curation_payload(
        pillar=pillar,
        sku=sku,
        location=location,
        has_identifiable_person=has_identifiable_person,
        consent_on_file=consent_on_file,
        has_readable_packaging=has_readable_packaging,
        is_reference_grade=is_reference_grade,
        needs_review=needs_review,
    )
    payload.update(_notes_update(notes, notes_present))
    # O botao "salvar + revisado" vence o checkbox: e o gesto explicito de quem
    # acabou de olhar para a foto.
    if _parse_bool(mark_reviewed, "mark_reviewed") is True:
        payload["needs_review"] = False
    if payload:
        repository.update_asset_curation(conn, asset_id, **payload)

    if not _is_htmx(request):
        return _back(request, "/assets")
    asset = repository.get_asset(conn, asset_id)
    return templates.TemplateResponse(
        request, "_fragment_asset_card.html", {"asset": asset}
    )


@router.post("/assets/bulk", response_class=HTMLResponse)
def curate_bulk(
    request: Request,
    conn: sqlite3.Connection = Depends(_conn),
    ids: list[int] = Form(default_factory=list),
    pillar: str = Form(UNCHANGED),
    sku: str = Form(UNCHANGED),
    location: str = Form(UNCHANGED),
    has_identifiable_person: str = Form(UNCHANGED),
    consent_on_file: str = Form(UNCHANGED),
    has_readable_packaging: str = Form(UNCHANGED),
    is_reference_grade: str = Form(UNCHANGED),
    needs_review: str = Form(UNCHANGED),
) -> Response:
    # `notes` fica de fora de proposito: anotacao e por foto, repetir o mesmo
    # texto em quarenta assets so polui o rastro da ingestao.
    if not ids:
        raise HTTPException(status_code=400, detail="selecione ao menos um asset")

    payload = _curation_payload(
        pillar=pillar,
        sku=sku,
        location=location,
        has_identifiable_person=has_identifiable_person,
        consent_on_file=consent_on_file,
        has_readable_packaging=has_readable_packaging,
        is_reference_grade=is_reference_grade,
        needs_review=needs_review,
    )
    if not payload:
        raise HTTPException(
            status_code=400, detail="nenhum campo escolhido para a marcacao multipla"
        )

    updated: list[Asset] = []
    missing: list[int] = []
    for asset_id in dict.fromkeys(ids):  # dedupe preservando a ordem do form
        if repository.get_asset(conn, asset_id) is None:
            missing.append(asset_id)
            continue
        repository.update_asset_curation(conn, asset_id, **payload)
        asset = repository.get_asset(conn, asset_id)
        if asset is not None:
            updated.append(asset)

    if not _is_htmx(request):
        return _back(request, "/assets")
    return templates.TemplateResponse(
        request,
        "_fragment_bulk.html",
        {"assets": updated, "missing": missing, "fields": sorted(payload)},
    )


@router.get("/assets/thumb/{asset_id}")
def asset_thumb(
    asset_id: int, conn: sqlite3.Connection = Depends(_conn)
) -> FileResponse:
    asset = repository.get_asset(conn, asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"asset {asset_id} nao existe")
    return _file_response(asset.thumb_path, f"asset {asset_id} sem thumbnail em disco")


# --------------------------------------------------------------------------- #
# revisao
# --------------------------------------------------------------------------- #


@router.get("/review", response_class=HTMLResponse)
def review_page(
    request: Request, conn: sqlite3.Connection = Depends(_conn), limit: int = 50
) -> Response:
    pending = repository.list_generations(
        conn, review_status=ReviewStatus.PENDING, limit=max(1, limit)
    )
    items = [build_review_item(conn, generation) for generation in pending]
    return templates.TemplateResponse(
        request, "review.html", {"items": items, "active": "review"}
    )


def _decided(
    request: Request, conn: sqlite3.Connection, generation_id: int
) -> Response:
    if not _is_htmx(request):
        return _back(request, "/review")
    generation = repository.get_generation(conn, generation_id)
    return templates.TemplateResponse(
        request, "_fragment_decided.html", {"generation": generation}
    )


@router.post("/generations/{generation_id}/approve", response_class=HTMLResponse)
def approve_generation(
    request: Request, generation_id: int, conn: sqlite3.Connection = Depends(_conn)
) -> Response:
    if repository.get_generation(conn, generation_id) is None:
        raise HTTPException(status_code=404, detail=f"generation {generation_id} nao existe")
    # Aprovar limpa qualquer motivo de rejeicao anterior: o historico util fica
    # no relatorio de custo, nao num campo que contradiz o status atual.
    repository.set_review_status(conn, generation_id, ReviewStatus.APPROVED, None)
    return _decided(request, conn, generation_id)


@router.post("/generations/{generation_id}/reject", response_class=HTMLResponse)
def reject_generation(
    request: Request,
    generation_id: int,
    conn: sqlite3.Connection = Depends(_conn),
    reject_reason: str = Form(""),
) -> Response:
    if repository.get_generation(conn, generation_id) is None:
        raise HTTPException(status_code=404, detail=f"generation {generation_id} nao existe")
    reason = reject_reason.strip()
    if not reason:
        raise HTTPException(status_code=400, detail=REJECT_REASON_REQUIRED)
    repository.set_review_status(conn, generation_id, ReviewStatus.REJECTED, reason)
    return _decided(request, conn, generation_id)


@router.post("/generations/{generation_id}/focal")
def set_focal(
    generation_id: int,
    conn: sqlite3.Connection = Depends(_conn),
    x: float = Form(...),
    y: float = Form(...),
) -> JSONResponse:
    if repository.get_generation(conn, generation_id) is None:
        raise HTTPException(status_code=404, detail=f"generation {generation_id} nao existe")
    if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
        raise HTTPException(
            status_code=400,
            detail="ponto focal e relativo: x e y precisam estar entre 0 e 1",
        )
    repository.set_focal_point(conn, generation_id, x, y)
    return JSONResponse({"ok": True, "focal_x": x, "focal_y": y})


@router.get("/generations/image/{generation_id}")
def generation_image(
    generation_id: int, conn: sqlite3.Connection = Depends(_conn)
) -> FileResponse:
    generation = repository.get_generation(conn, generation_id)
    if generation is None:
        raise HTTPException(status_code=404, detail=f"generation {generation_id} nao existe")
    return _file_response(
        generation.path, f"generation {generation_id} sem arquivo em disco"
    )


# --------------------------------------------------------------------------- #
# fabrica
# --------------------------------------------------------------------------- #


def create_app(settings: Settings | None = None) -> FastAPI:
    """Monta o app com o banco ja migrado. `settings` existe para os testes."""
    resolved = settings or get_settings()
    open_db(resolved).close()

    app = FastAPI(
        title="Canastra Image Engine",
        description=CORE_PRINCIPLE,
        version="0.1.0",
        redoc_url=None,
    )
    app.state.settings = resolved
    app.include_router(router)
    return app
