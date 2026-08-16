"""Testes da fila de geracao.

Nenhum teste toca a rede: ou o cliente e um duble com a mesma assinatura de
`XaiClient.generate_images`, ou e o `XaiClient` de verdade com
`httpx.MockTransport` por baixo.

O que este arquivo protege, em ordem de gravidade:
  * job bloqueado por guardrail NUNCA chega a API (o duble falha o teste se for
    chamado);
  * o teto de orcamento para exatamente antes de estourar e diz quantos jobs
    ficaram na fila;
  * erro da API vira FAILED com o corpo bruto preservado;
  * modo seco nao grava nada e nao chama nada.
"""

from __future__ import annotations

import asyncio
import base64
import io
import sqlite3
from pathlib import Path
from typing import Any

import httpx
import pytest
import yaml
from PIL import Image

from cie import pricing, repository
from cie.capabilities import ApiCapabilities
from cie.config import Settings
from cie.enums import AspectRatio, JobStatus, Pillar
from cie.errors import CieError, GuardrailViolation, XaiApiError
from cie.models import Asset, Job, StyleDescriptor, StyleDna
from cie.prompt import build_prompt_fragment
from cie.queue import (
    PlanEntry,
    RunResult,
    add_jobs_from_plan,
    build_job,
    estimate_queue_cost,
    load_plan,
    run_queue,
)
from cie.template_loader import load_templates_dir, sync_templates
from cie.xai import GeneratedImage, ImageResponse, XaiClient

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
WEEK_PLAN = ROOT / "plans" / "semana-01.yaml"

#: Custo de uma imagem no modelo padrao. Os tetos dos testes sao multiplos
#: disto para o catalogo poder mudar de preco sem invalidar a aritmetica.
UNIT = pricing.estimate_cost(pricing.DEFAULT_MODEL, 1)

DESCRIPTOR = StyleDescriptor(
    palette=["ocre queimado", "verde-cafeeiro profundo"],
    light_quality="luz natural lateral suave",
    lens="50mm, profundidade de campo rasa",
    texture="grain fino de filme",
    framing="sujeito descentralizado",
    recurring_materials=["madeira rustica", "aco inox escovado"],
    mood="elegancia rustica e cientifica",
    avoid=["saturacao HDR", "reflexos plasticos"],
)


# --------------------------------------------------------------------------- #
# apoio
# --------------------------------------------------------------------------- #


def _png_bytes(color: str = "#6b4423") -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (64, 64), color).save(buffer, format="PNG")
    return buffer.getvalue()


def _png_b64(color: str = "#6b4423") -> str:
    return base64.b64encode(_png_bytes(color)).decode("ascii")


class FakeClient:
    """Duble do cliente da xAI: registra os pedidos e devolve PNG deterministico."""

    def __init__(self, *, fail_with: Exception | None = None, images: int | None = None,
                 payload: str | None = None) -> None:
        self.calls: list[Any] = []
        self.fail_with = fail_with
        self.images = images
        self.payload = payload

    async def generate_images(self, request: Any) -> ImageResponse:
        self.calls.append(request)
        if self.fail_with is not None:
            raise self.fail_with
        count = self.images if self.images is not None else request.n
        body = self.payload if self.payload is not None else _png_b64()
        return ImageResponse(
            images=[GeneratedImage(b64=body) for _ in range(count)],
            model=request.model,
            raw={"data": []},
        )

    async def aclose(self) -> None:
        return None


class ExplodingClient:
    """Se a fila chamar isto, o guardrail falhou em bloquear antes do credito."""

    def __init__(self) -> None:
        self.calls: list[Any] = []

    async def generate_images(self, request: Any) -> ImageResponse:
        self.calls.append(request)
        raise AssertionError("a API foi chamada apesar do guardrail bloqueante")

    async def aclose(self) -> None:
        return None


def _insert_asset(conn: sqlite3.Connection, index: int, **overrides: Any) -> int:
    """Asset ja curado: sem pessoa identificavel e bom para referencia."""
    data: dict[str, Any] = {
        "path": f"/base/CANASTRA_3_TORREFACAO_TAMBOR_{index:03d}.jpg",
        "sha256": f"{index:064d}",
        "width": 2400,
        "height": 1600,
        "has_identifiable_person": False,
        "consent_on_file": False,
        "has_readable_packaging": False,
        "quality_score": 90 - index,
        "is_reference_grade": True,
        "needs_review": False,
    }
    data.update(overrides)
    return repository.insert_asset(conn, Asset(**data))


def write_plan(settings: Settings, jobs: list[dict[str, Any]], name: str = "plano.yaml") -> Path:
    path = settings.root / name
    path.write_text(yaml.safe_dump({"jobs": jobs}, sort_keys=False), encoding="utf-8")
    return path


@pytest.fixture
def catalog(conn: sqlite3.Connection, settings: Settings) -> dict[str, Any]:
    """Cenas sincronizadas, tres assets curados e um Style DNA do pilar 3."""
    sync_templates(conn, TEMPLATES_DIR)
    asset_ids = [_insert_asset(conn, index) for index in range(1, 4)]
    dna_id = repository.upsert_style_dna(
        conn,
        StyleDna(
            name="laboratorio-uberlandia",
            pillar=Pillar.P3,
            source_asset_ids=asset_ids,
            descriptor=DESCRIPTOR,
            prompt_fragment=build_prompt_fragment(DESCRIPTOR),
        ),
    )
    return {"asset_ids": asset_ids, "dna_id": dna_id}


def queue_many(conn: sqlite3.Connection, settings: Settings, count: int) -> Path:
    """Enfileira `count` jobs identicos de risco baixo (n=1 cada)."""
    plan = write_plan(settings, [{"template": "macro_grao_torrado", "n": 1}] * count)
    add_jobs_from_plan(conn, settings, plan)
    return plan


# --------------------------------------------------------------------------- #
# leitura do plano
# --------------------------------------------------------------------------- #


def test_load_plan_reads_every_field(settings: Settings) -> None:
    path = write_plan(
        settings,
        [
            {
                "template": "macro_grao_torrado",
                "dna": "laboratorio-uberlandia",
                "n": 3,
                "aspect_ratio": "9:16",
                "model": "grok-imagine-image-2.0",
                "variables": {"roast_level": "light"},
                "reference_assets": [1, 2],
                "use_compositor": True,
                "notes": "so documentacao",
            }
        ],
    )

    entries = load_plan(path)

    assert entries == [
        PlanEntry(
            template="macro_grao_torrado",
            dna="laboratorio-uberlandia",
            n=3,
            aspect_ratio="9:16",
            model="grok-imagine-image-2.0",
            variables={"roast_level": "light"},
            reference_assets=[1, 2],
            use_compositor=True,
        )
    ]


def test_load_plan_accepts_a_bare_list_and_fills_defaults(settings: Settings) -> None:
    path = settings.root / "lista.yaml"
    path.write_text(yaml.safe_dump([{"template": "terreiro_secagem"}]), encoding="utf-8")

    entry = load_plan(path)[0]

    assert entry.template == "terreiro_secagem"
    assert entry.n == 1
    assert entry.dna is None
    assert entry.variables == {}
    assert entry.reference_assets == []
    assert entry.use_compositor is False


@pytest.mark.parametrize(
    ("content", "fragment"),
    [
        ("", "vazio"),
        ("jobs: [\n", "malformado"),
        ("semana: 1\njobs: []\n", "desconhecidas"),
        ("jobs: []\n", "vazio"),
        ("outra_coisa: 1\n", "desconhecidas"),
        ("jobs:\n  - n: 2\n", "template"),
        ("jobs:\n  - template: x\n    n: 0\n", "n precisa"),
        ("jobs:\n  - template: x\n    n: dois\n", "inteiro"),
        ('jobs:\n  - template: x\n    aspect_ratio: "4:5"\n', "aspect_ratio invalido"),
        ("jobs:\n  - template: x\n    referece_assets: [1]\n", "desconhecidas"),
        ("jobs:\n  - template: x\n    reference_assets: 3\n", "reference_assets"),
        ("jobs:\n  - template: x\n    use_compositor: talvez\n", "use_compositor"),
        ("jobs:\n  - template: x\n    variables: [1, 2]\n", "variables"),
        ("jobs: 3\n", "precisa ser uma lista"),
        ("- so uma string\n", "mapeamento"),
        ("name: plano sem jobs\n", "falta a lista"),
        ("42\n", "precisa ser um mapeamento"),
        ("jobs:\n  - template: 42\n", "texto nao vazio"),
        ("jobs:\n  - template: x\n    variables:\n      roast_level:\n", "esta vazio"),
        ('jobs:\n  - template: x\n    reference_assets: ["um"]\n', "id inteiro"),
    ],
)
def test_load_plan_invalid_raises_cie_error_with_path(
    settings: Settings, content: str, fragment: str
) -> None:
    path = settings.root / "plano-torto.yaml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(CieError) as excinfo:
        load_plan(path)

    message = str(excinfo.value)
    # O caminho sempre aparece: quem edita o YAML precisa saber qual arquivo caiu.
    assert str(path) in message
    assert fragment in message


def test_load_plan_missing_file_names_the_path(settings: Settings) -> None:
    missing = settings.root / "nao-existe.yaml"

    with pytest.raises(CieError) as excinfo:
        load_plan(missing)

    assert str(missing) in str(excinfo.value)


def test_week_plan_shipped_with_the_repo_is_valid(conn: sqlite3.Connection) -> None:
    """O plano de exemplo tem que abrir, cobrir os quatro pilares e so citar
    cenas que existem em templates/."""
    entries = load_plan(WEEK_PLAN)
    templates = {t.name: t for t in load_templates_dir(TEMPLATES_DIR)}

    assert len(entries) >= 6
    for entry in entries:
        assert entry.template in templates, f"cena inexistente no plano: {entry.template}"
        assert entry.n >= 1

    pillars = {
        str(templates[entry.template].pillar)
        for entry in entries
        if templates[entry.template].pillar
    }
    assert {"1", "2", "3", "4"} <= pillars


def test_week_plan_queues_without_any_block(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """Rodar o plano da casa nao pode produzir job bloqueado: se produzir, o
    plano esta pedindo algo que a politica nao deixa passar."""
    jobs = add_jobs_from_plan(conn, settings, WEEK_PLAN)

    assert len(jobs) >= 6
    assert all(job.status is JobStatus.QUEUED for job in jobs), [
        (job.id, job.blocked_reason) for job in jobs if job.status is not JobStatus.QUEUED
    ]


# --------------------------------------------------------------------------- #
# montagem do job
# --------------------------------------------------------------------------- #


def test_build_job_resolves_prompt_and_keeps_provenance(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    entry = PlanEntry(template="macro_grao_torrado", dna="laboratorio-uberlandia", n=2)

    job, report, payload = build_job(
        conn, settings, entry, capabilities=ApiCapabilities()
    )

    assert job.status is JobStatus.QUEUED
    assert job.blocked_reason is None
    assert job.aspect_ratio is AspectRatio.R1_1  # default do template
    # Corpo do template, DNA e negative, nesta ordem, ja resolvidos.
    assert "roasted Arara coffee bean" in job.resolved_prompt
    assert "elegancia rustica" in job.resolved_prompt
    assert "warped text" in job.resolved_prompt
    assert not report.blocked
    # Sem sondagem, a estrategia e descritiva e nenhuma imagem viaja.
    assert payload.strategy == "descriptor"
    assert payload.extra == {}
    # Proveniencia herdada do DNA: de quais fotos reais este estilo veio.
    assert job.reference_asset_ids == catalog["asset_ids"]


def test_build_job_blocks_packaging_template_without_reference(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    entry = PlanEntry(template="pacote_madeira_rustica", n=1)

    job, report, _payload = build_job(conn, settings, entry)

    assert report.blocked
    assert job.status is JobStatus.BLOCKED
    assert "packaging_requires_reference" in (job.blocked_reason or "")
    assert "como resolver" in (job.blocked_reason or "")


def test_build_job_rejects_unknown_template_dna_and_asset(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    with pytest.raises(CieError, match="template 'nao_existe'"):
        build_job(conn, settings, PlanEntry(template="nao_existe"))

    with pytest.raises(CieError, match="Style DNA 'fantasma'"):
        build_job(conn, settings, PlanEntry(template="macro_grao_torrado", dna="fantasma"))

    with pytest.raises(CieError, match="inexistente"):
        build_job(
            conn,
            settings,
            PlanEntry(template="macro_grao_torrado", reference_assets=[9999]),
        )


def test_build_job_rejects_aspect_ratio_the_api_does_not_have(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """4:5 e recorte de feed, nao proporcao de geracao: sai no export."""
    entry = PlanEntry(template="macro_grao_torrado", aspect_ratio="4:5")

    with pytest.raises(CieError, match="aspect ratio invalido"):
        build_job(conn, settings, entry)


def test_incoherent_probe_raises_instead_of_guessing_the_field(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """Sondagem dizendo "suporta" sem dizer QUAL campo nao vira chute."""
    caps = ApiCapabilities(
        probed_at="2026-08-16T12:00:00+00:00", native_reference_supported=True
    )

    with pytest.raises(CieError, match="reference_field"):
        build_job(
            conn,
            settings,
            PlanEntry(template="macro_grao_torrado"),
            capabilities=caps,
        )


def test_policy_violation_wins_over_a_broken_probe(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """Com os dois problemas juntos, quem fala e a regra de politica."""
    caps = ApiCapabilities(
        probed_at="2026-08-16T12:00:00+00:00", native_reference_supported=True
    )

    with pytest.raises(GuardrailViolation) as excinfo:
        build_job(
            conn,
            settings,
            PlanEntry(template="pacote_madeira_rustica"),
            capabilities=caps,
        )

    assert "packaging_requires_reference" in str(excinfo.value)


def test_add_jobs_from_plan_dry_run_writes_nothing(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    plan = write_plan(settings, [{"template": "macro_grao_torrado", "n": 2}])

    jobs = add_jobs_from_plan(conn, settings, plan, dry_run=True)

    assert len(jobs) == 1
    assert jobs[0].id is None
    assert repository.count_jobs(conn) == 0


def test_add_jobs_from_plan_persists_blocked_job_without_api(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    plan = write_plan(
        settings,
        [
            {"template": "macro_grao_torrado", "n": 1},
            {"template": "pacote_madeira_rustica", "n": 1},
        ],
    )

    jobs = add_jobs_from_plan(conn, settings, plan)

    assert [job.status for job in jobs] == [JobStatus.QUEUED, JobStatus.BLOCKED]
    assert all(job.id is not None for job in jobs)
    assert repository.count_jobs(conn, JobStatus.BLOCKED) == 1


def test_add_jobs_from_plan_is_all_or_nothing(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """Entrada torta no meio do plano nao deixa meia semana no banco."""
    plan = write_plan(
        settings,
        [
            {"template": "macro_grao_torrado", "n": 1},
            {"template": "cena_que_nao_existe", "n": 1},
        ],
    )

    with pytest.raises(CieError) as excinfo:
        add_jobs_from_plan(conn, settings, plan)

    assert "entrada 2" in str(excinfo.value)
    assert str(plan) in str(excinfo.value)
    assert repository.count_jobs(conn) == 0


def test_estimate_queue_cost_sums_only_queued_jobs(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    plan = write_plan(
        settings,
        [
            {"template": "macro_grao_torrado", "n": 2},
            {"template": "terreiro_secagem", "n": 1},
            {"template": "pacote_madeira_rustica", "n": 5},  # nasce BLOCKED
        ],
    )
    add_jobs_from_plan(conn, settings, plan)

    assert estimate_queue_cost(conn) == pytest.approx(UNIT * 3)
    assert estimate_queue_cost(conn, limit=1) == pytest.approx(UNIT * 2)


# --------------------------------------------------------------------------- #
# execucao: sucesso
# --------------------------------------------------------------------------- #


def test_run_queue_writes_generations_with_disclosure_and_cost(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    plan = write_plan(
        settings,
        [{"template": "macro_grao_torrado", "dna": "laboratorio-uberlandia", "n": 2}],
    )
    add_jobs_from_plan(conn, settings, plan)
    client = FakeClient()

    result = asyncio.run(run_queue(conn, settings, limit=10, budget_usd=1.0, client=client))

    assert result.done == 1
    assert result.attempted == 1
    assert result.failed == 0
    assert result.spent_usd == pytest.approx(UNIT * 2)
    assert len(client.calls) == 1
    assert client.calls[0].n == 2
    assert client.calls[0].seed is None  # sondagem nao confirmou o campo

    generations = repository.list_generations(conn)
    assert len(generations) == 2
    for generation in generations:
        path = Path(generation.path)
        assert path.exists()
        assert path.parent == settings.generations_dir
        # Nome derivado do sha256: o proprio arquivo prova sua integridade.
        assert path.stem == generation.sha256
        assert generation.disclosure_required is True
        assert generation.cost_usd == pytest.approx(UNIT)
        assert generation.prompt == repository.get_job(conn, generation.job_id).resolved_prompt
        assert generation.model == pricing.DEFAULT_MODEL

    job = repository.list_jobs(conn)[0]
    assert job.status is JobStatus.DONE
    assert job.attempts == 1
    assert job.cost_usd == pytest.approx(UNIT * 2)
    assert job.finished_at is not None
    assert result.pending == 0


def test_run_queue_charges_only_for_images_actually_returned(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """API entregou menos que `n`: o job nao debita o que nao veio."""
    plan = write_plan(settings, [{"template": "macro_grao_torrado", "n": 3}])
    add_jobs_from_plan(conn, settings, plan)

    result = asyncio.run(
        run_queue(conn, settings, budget_usd=1.0, client=FakeClient(images=1))
    )

    assert result.done == 1
    assert result.spent_usd == pytest.approx(UNIT)
    assert len(repository.list_generations(conn)) == 1


def test_identical_bytes_land_on_a_single_file(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    plan = write_plan(settings, [{"template": "macro_grao_torrado", "n": 4}])
    add_jobs_from_plan(conn, settings, plan)

    asyncio.run(run_queue(conn, settings, budget_usd=1.0, client=FakeClient()))

    generations = repository.list_generations(conn)
    assert len(generations) == 4
    assert len({g.path for g in generations}) == 1
    assert len(list(settings.generations_dir.iterdir())) == 1


def test_limit_is_respected(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    queue_many(conn, settings, 5)
    client = FakeClient()

    result = asyncio.run(run_queue(conn, settings, limit=2, budget_usd=1.0, client=client))

    assert result.done == 2
    assert len(client.calls) == 2
    assert result.pending == 3
    assert repository.count_jobs(conn, JobStatus.QUEUED) == 3
    assert result.stopped_by_budget is False


# --------------------------------------------------------------------------- #
# execucao: teto de orcamento
# --------------------------------------------------------------------------- #


def test_budget_stops_exactly_before_overspending(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    queue_many(conn, settings, 10)
    client = FakeClient()
    budget = round(UNIT * 2.5, 6)  # cabem dois jobs; o terceiro estouraria

    result = asyncio.run(
        run_queue(conn, settings, limit=10, budget_usd=budget, client=client)
    )

    assert len(client.calls) == 2
    assert result.done == 2
    assert result.spent_usd == pytest.approx(UNIT * 2)
    assert result.spent_usd <= budget
    assert result.stopped_by_budget is True
    assert result.skipped_budget == 8
    assert result.pending == 8
    assert repository.count_jobs(conn, JobStatus.QUEUED) == 8
    # Nenhum job intermediario ficou preso em RUNNING.
    assert repository.count_jobs(conn, JobStatus.RUNNING) == 0


def test_budget_that_fits_exactly_runs_every_job(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """Tres jobs de US$ 0.02 somam 0.060000000000000005 em ponto flutuante: o
    teto de US$ 0.06 tem que aceitar os tres mesmo assim."""
    queue_many(conn, settings, 3)
    client = FakeClient()

    result = asyncio.run(
        run_queue(conn, settings, budget_usd=round(UNIT * 3, 6), client=client)
    )

    assert result.done == 3
    assert result.stopped_by_budget is False
    assert result.pending == 0


def test_budget_smaller_than_one_job_calls_nothing(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    queue_many(conn, settings, 2)
    client = FakeClient()

    result = asyncio.run(run_queue(conn, settings, budget_usd=UNIT / 2, client=client))

    assert client.calls == []
    assert result.done == 0
    assert result.attempted == 0
    assert result.stopped_by_budget is True
    assert result.pending == 2


def test_without_budget_the_queue_runs_to_the_limit(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    queue_many(conn, settings, 3)
    client = FakeClient()

    result = asyncio.run(run_queue(conn, settings, client=client))

    assert result.done == 3
    assert result.stopped_by_budget is False


# --------------------------------------------------------------------------- #
# execucao: guardrails antes da API
# --------------------------------------------------------------------------- #


def test_job_blocked_at_run_time_never_reaches_the_api(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """Curadoria mudou depois do enfileiramento: a fila reavalia e bloqueia."""
    asset_id = catalog["asset_ids"][0]
    plan = write_plan(
        settings,
        [{"template": "macro_grao_torrado", "n": 1, "reference_assets": [asset_id]}],
    )
    jobs = add_jobs_from_plan(conn, settings, plan)
    assert jobs[0].status is JobStatus.QUEUED

    # Revisao humana descobriu uma pessoa identificavel na foto, sem termo assinado.
    repository.update_asset_curation(conn, asset_id, has_identifiable_person=True)

    client = ExplodingClient()
    result = asyncio.run(run_queue(conn, settings, budget_usd=1.0, client=client))

    assert client.calls == [], "a API foi chamada apesar do guardrail"
    assert result.blocked == 1
    assert result.attempted == 0
    assert result.spent_usd == 0.0
    blocked = repository.list_jobs(conn, status=JobStatus.BLOCKED)
    assert len(blocked) == 1
    assert "no_synthetic_identifiable_faces" in (blocked[0].blocked_reason or "")
    assert "como resolver" in (blocked[0].blocked_reason or "")
    assert blocked[0].attempts == 0  # bloqueio nao e tentativa
    assert repository.list_generations(conn) == []


def test_packaging_job_queued_by_hand_is_blocked_before_the_api(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """Job inserido direto no banco tambem passa pelo crivo antes de rodar."""
    template = repository.get_template_by_name(conn, "pacote_madeira_rustica")
    repository.insert_job(
        conn,
        Job(
            template_id=template.id,
            resolved_prompt="packshot do Microlote sobre madeira",
            model=pricing.DEFAULT_MODEL,
            aspect_ratio=AspectRatio.R3_4,
            n=1,
            status=JobStatus.QUEUED,
        ),
    )
    client = ExplodingClient()

    result = asyncio.run(run_queue(conn, settings, budget_usd=1.0, client=client))

    assert client.calls == []
    assert result.blocked == 1
    assert repository.count_jobs(conn, JobStatus.BLOCKED) == 1


def test_inherited_dna_provenance_does_not_block_at_run_time(
    conn: sqlite3.Connection, settings: Settings
) -> None:
    """Cinco fotos originaram o DNA. Isso e rastro, nao referencia enviada:
    o teto de tres referencias nao pode bloquear o job na hora de rodar."""
    sync_templates(conn, TEMPLATES_DIR)
    asset_ids = [_insert_asset(conn, index) for index in range(1, 6)]
    repository.upsert_style_dna(
        conn,
        StyleDna(
            name="terroir-medeiros",
            pillar=Pillar.P1,
            source_asset_ids=asset_ids,
            descriptor=DESCRIPTOR,
            prompt_fragment=build_prompt_fragment(DESCRIPTOR),
        ),
    )
    plan = write_plan(
        settings, [{"template": "terreiro_secagem", "dna": "terroir-medeiros", "n": 1}]
    )
    jobs = add_jobs_from_plan(conn, settings, plan)
    assert jobs[0].reference_asset_ids == asset_ids

    result = asyncio.run(run_queue(conn, settings, budget_usd=1.0, client=FakeClient()))

    assert result.blocked == 0
    assert result.done == 1


def test_compositor_track_passes_the_packaging_rule_at_build_time(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """Com recorte real do SKU, a difusao so faz o fundo e o rotulo continua real."""
    cutout = settings.cutouts_dir / "microlote_frente.png"
    cutout.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", (800, 1200), (120, 80, 40, 255)).save(cutout)

    entry = PlanEntry(
        template="pacote_madeira_rustica",
        n=1,
        variables={"sku": "microlote"},
        use_compositor=True,
    )

    job, report, _payload = build_job(conn, settings, entry)

    assert job.status is JobStatus.QUEUED
    assert not report.blocked
    assert any("composicao local" in r.message for r in report.infos)


def test_seed_travels_only_after_the_probe_confirms_the_field(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    queue_many(conn, settings, 1)
    client = FakeClient()
    probed = ApiCapabilities(probed_at="2026-08-16T12:00:00+00:00", supports_seed=True)

    asyncio.run(
        run_queue(
            conn, settings, budget_usd=1.0, client=client, capabilities=probed
        )
    )

    job = repository.list_jobs(conn)[0]
    assert client.calls[0].seed == job.id
    assert repository.list_generations(conn)[0].seed == job.id


def test_too_many_explicit_references_are_blocked(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    extra = [_insert_asset(conn, index) for index in range(10, 13)]
    entry = PlanEntry(
        template="macro_grao_torrado", reference_assets=catalog["asset_ids"] + extra
    )

    job, report, _payload = build_job(conn, settings, entry)

    assert job.status is JobStatus.BLOCKED
    assert "max_reference_images" in (job.blocked_reason or "")
    assert report.blocked


# --------------------------------------------------------------------------- #
# execucao: falha da API
# --------------------------------------------------------------------------- #


def test_api_error_marks_job_failed_and_keeps_the_raw_body(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    queue_many(conn, settings, 1)
    client = FakeClient(
        fail_with=XaiApiError("erro do servidor", status_code=500, raw='{"error":"boom"}')
    )

    result = asyncio.run(run_queue(conn, settings, budget_usd=1.0, client=client))

    assert result.failed == 1
    assert result.done == 0
    assert result.attempted == 1
    assert result.spent_usd == 0.0
    failed = repository.list_jobs(conn, status=JobStatus.FAILED)
    assert len(failed) == 1
    assert "boom" in (failed[0].blocked_reason or "")
    assert "XaiApiError" in (failed[0].blocked_reason or "")
    assert failed[0].attempts == 1
    assert failed[0].finished_at is not None
    assert repository.list_generations(conn) == []


def test_http_500_through_the_real_client_marks_job_failed(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """Mesmo caminho do teste acima, mas com o `XaiClient` de verdade por cima
    de um transporte falso: prova que a fila e o cliente se encaixam."""
    queue_many(conn, settings, 1)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": {"message": "boom interno"}})

    async def no_sleep(seconds: float) -> None:
        return None

    client = XaiClient(
        api_key="chave-de-teste",
        base_url="https://api.exemplo.invalido/v1",
        transport=httpx.MockTransport(handler),
        max_retries=1,
        sleeper=no_sleep,
    )

    async def main() -> RunResult:
        try:
            return await run_queue(conn, settings, budget_usd=1.0, client=client)
        finally:
            await client.aclose()

    result = asyncio.run(main())

    assert result.failed == 1
    failed = repository.list_jobs(conn, status=JobStatus.FAILED)
    assert "boom interno" in (failed[0].blocked_reason or "")
    assert "500" in (failed[0].blocked_reason or "")


def test_response_that_is_not_an_image_fails_the_job(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """Bytes irreconheciveis nao viram `.png` por chute: viram falha visivel."""
    queue_many(conn, settings, 1)
    client = FakeClient(payload=base64.b64encode(b"nao sou uma imagem").decode("ascii"))

    result = asyncio.run(run_queue(conn, settings, budget_usd=1.0, client=client))

    assert result.failed == 1
    assert repository.list_generations(conn) == []
    assert list(settings.generations_dir.iterdir()) == []
    failed = repository.list_jobs(conn, status=JobStatus.FAILED)
    assert "nao sao uma imagem reconhecida" in (failed[0].blocked_reason or "")


def test_url_only_response_fails_instead_of_losing_provenance(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    queue_many(conn, settings, 1)

    class UrlOnlyClient(FakeClient):
        async def generate_images(self, request: Any) -> ImageResponse:
            self.calls.append(request)
            return ImageResponse(
                images=[GeneratedImage(url="https://exemplo.invalido/img.png")],
                model=request.model,
                raw={"data": []},
            )

    result = asyncio.run(run_queue(conn, settings, budget_usd=1.0, client=UrlOnlyClient()))

    assert result.failed == 1
    assert repository.list_generations(conn) == []


def test_missing_template_fails_the_job_without_calling_the_api(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """Catalogo mexido por fora: o job nao roda, mas tambem nao gasta nada."""
    queue_many(conn, settings, 1)
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.execute("DELETE FROM templates")
    conn.commit()
    client = ExplodingClient()

    result = asyncio.run(run_queue(conn, settings, budget_usd=1.0, client=client))

    assert client.calls == []
    assert result.failed == 1
    assert result.attempted == 0
    failed = repository.list_jobs(conn, status=JobStatus.FAILED)
    assert "templates sync" in (failed[0].blocked_reason or "")
    assert failed[0].attempts == 0


@pytest.mark.parametrize(
    ("data", "suffix"),
    [
        (b"\x89PNG\r\n\x1a\n" + b"resto", ".png"),
        (b"\xff\xd8\xff\xe0" + b"resto", ".jpg"),
        (b"GIF89a" + b"resto", ".gif"),
        (b"RIFF\x00\x00\x00\x00WEBPVP8 ", ".webp"),
        (b"\x00\x00\x00\x18ftypavif\x00\x00\x00\x00", ".avif"),
        (b"\x00\x00\x00\x18ftypheic\x00\x00\x00\x00", ".heic"),
    ],
)
def test_extension_comes_from_the_file_signature(data: bytes, suffix: str) -> None:
    from cie.queue import _image_extension

    assert _image_extension(data) == suffix


def test_webp_response_is_stored_with_the_right_extension(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    queue_many(conn, settings, 1)
    buffer = io.BytesIO()
    Image.new("RGB", (64, 64), "#6b4423").save(buffer, format="WEBP")
    client = FakeClient(payload=base64.b64encode(buffer.getvalue()).decode("ascii"))

    asyncio.run(run_queue(conn, settings, budget_usd=1.0, client=client))

    generation = repository.list_generations(conn)[0]
    assert Path(generation.path).suffix == ".webp"


def test_queue_builds_and_closes_the_client_it_owns(
    conn: sqlite3.Connection,
    settings: Settings,
    catalog: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    queue_many(conn, settings, 1)
    built: list[Any] = []

    class OwnedClient(FakeClient):
        def __init__(self) -> None:
            super().__init__()
            self.closed = False
            built.append(self)

        async def aclose(self) -> None:
            self.closed = True

    monkeypatch.setattr("cie.queue.XaiClient", OwnedClient)

    result = asyncio.run(run_queue(conn, settings, budget_usd=1.0))

    assert result.done == 1
    assert len(built) == 1
    assert built[0].closed is True


def test_injected_client_is_not_closed_by_the_queue(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """Quem emprestou o cliente decide quando fechar."""
    queue_many(conn, settings, 1)

    class TrackingClient(FakeClient):
        def __init__(self) -> None:
            super().__init__()
            self.closed = False

        async def aclose(self) -> None:
            self.closed = True

    client = TrackingClient()
    asyncio.run(run_queue(conn, settings, budget_usd=1.0, client=client))

    assert client.closed is False


def test_failure_does_not_stop_the_rest_of_the_queue(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    queue_many(conn, settings, 3)

    class FlakyClient(FakeClient):
        """Falha so na primeira chamada."""

        async def generate_images(self, request: Any) -> ImageResponse:
            first = not self.calls
            self.fail_with = (
                XaiApiError("500 interno", status_code=500, raw="boom") if first else None
            )
            return await FakeClient.generate_images(self, request)

    client = FlakyClient()
    # O primeiro job falha; os dois seguintes precisam rodar assim mesmo.
    result = asyncio.run(run_queue(conn, settings, budget_usd=1.0, client=client))

    assert result.failed == 1
    assert result.done == 2
    assert len(client.calls) == 3
    assert result.spent_usd == pytest.approx(UNIT * 2)
    assert repository.count_jobs(conn, JobStatus.QUEUED) == 0


# --------------------------------------------------------------------------- #
# modo seco
# --------------------------------------------------------------------------- #


def test_dry_run_writes_nothing_and_calls_nothing(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    plan = write_plan(settings, [{"template": "macro_grao_torrado", "n": 2}])
    add_jobs_from_plan(conn, settings, plan)
    client = ExplodingClient()

    result = asyncio.run(
        run_queue(conn, settings, budget_usd=1.0, client=client, dry_run=True)
    )

    assert client.calls == []
    assert repository.list_generations(conn) == []
    assert result.spent_usd == 0.0
    assert result.done == 0
    assert result.attempted == 1
    assert result.estimated_usd == pytest.approx(UNIT * 2)
    assert result.pending == 0  # o unico job da fila teria saido dela
    # Nada mudou no banco: o job continua enfileirado.
    assert repository.count_jobs(conn, JobStatus.QUEUED) == 1
    assert any("modo seco" in line for line in result.summary_lines())


def test_dry_run_needs_no_api_key_and_no_client(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    """A fixture `settings` remove XAI_API_KEY: construir cliente aqui levantaria."""
    queue_many(conn, settings, 2)

    result = asyncio.run(run_queue(conn, settings, budget_usd=1.0, dry_run=True))

    assert result.attempted == 2
    assert result.spent_usd == 0.0


def test_dry_run_reports_blocked_jobs_without_touching_them(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    template = repository.get_template_by_name(conn, "pacote_madeira_rustica")
    repository.insert_job(
        conn,
        Job(
            template_id=template.id,
            resolved_prompt="packshot",
            model=pricing.DEFAULT_MODEL,
            n=1,
            status=JobStatus.QUEUED,
        ),
    )

    result = asyncio.run(run_queue(conn, settings, budget_usd=1.0, dry_run=True))

    assert result.blocked == 1
    assert result.attempted == 0
    # Modo seco nao mexe em status: o job continua QUEUED para o operador decidir.
    assert repository.count_jobs(conn, JobStatus.QUEUED) == 1


def test_dry_run_honours_the_budget_ceiling(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    queue_many(conn, settings, 5)

    result = asyncio.run(
        run_queue(conn, settings, budget_usd=round(UNIT * 2, 6), dry_run=True)
    )

    assert result.attempted == 2
    assert result.stopped_by_budget is True
    assert result.skipped_budget == 3
    assert result.pending == 3


def test_empty_queue_is_a_no_op(conn: sqlite3.Connection, settings: Settings) -> None:
    result = asyncio.run(run_queue(conn, settings, budget_usd=1.0))

    assert result == RunResult()


def test_summary_lines_report_the_run(
    conn: sqlite3.Connection, settings: Settings, catalog: dict[str, Any]
) -> None:
    queue_many(conn, settings, 3)

    result = asyncio.run(
        run_queue(conn, settings, budget_usd=round(UNIT * 2, 6), client=FakeClient())
    )
    lines = result.summary_lines()

    assert any("concluidos: 2" in line for line in lines)
    assert any("pendentes na fila: 1" in line for line in lines)
    assert any("teto de orcamento" in line for line in lines)
    # Sem colchetes: a saida passa pelo rich, que trataria isso como markup.
    assert all("[" not in line for line in lines)
