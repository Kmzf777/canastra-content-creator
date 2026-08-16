"""Teste de integracao ponta a ponta, sem tocar a rede.

Percorre o caminho real de trabalho: ingerir -> curar -> sincronizar cenas ->
Style DNA -> dry-run -> fila com cliente falso -> aprovar -> exportar -> custo.

Este arquivo e o contrato vivo entre os modulos: se alguem mudar uma assinatura,
e aqui que quebra primeiro.
"""

from __future__ import annotations

import asyncio
import base64
import io
import json
from pathlib import Path

import pytest
from PIL import Image

from cie import repository
from cie.capabilities import ApiCapabilities
from cie.enums import Pillar, ReviewStatus, Sku
from cie.errors import GuardrailViolation
from cie.ingest import ingest_directory
from cie.models import StyleDescriptor, StyleDna

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


# --------------------------------------------------------------------------- #
# apoio
# --------------------------------------------------------------------------- #


def _png_b64(size: tuple[int, int] = (1024, 1024), color: str = "#6b4423") -> str:
    """Imagem que o cliente falso devolve no lugar da API."""
    buffer = io.BytesIO()
    image = Image.new("RGB", size, color)
    # Um pouco de estrutura para o detector de ponto focal ter o que medir.
    for x in range(0, size[0] // 2, 8):
        for y in range(0, size[1], 8):
            image.putpixel((x, y), (240, 220, 180))
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


class FakeClient:
    """Cliente da xAI falso: conta chamadas e devolve imagens deterministicas."""

    def __init__(self, *, fail_with: Exception | None = None) -> None:
        self.calls: list = []
        self.fail_with = fail_with

    async def generate_images(self, request):
        from cie.xai import GeneratedImage, ImageResponse

        self.calls.append(request)
        if self.fail_with:
            raise self.fail_with
        images = [
            GeneratedImage(b64=_png_b64(), url=None, revised_prompt=None)
            for _ in range(request.n)
        ]
        return ImageResponse(images=images, model=request.model, raw={"data": []})

    async def aclose(self) -> None:
        return None


class ExplodingClient:
    """Se a fila chamar isto, o guardrail falhou em bloquear antes de gastar credito."""

    async def generate_images(self, request):  # pragma: no cover - nao deve rodar
        raise AssertionError("a API foi chamada apesar do guardrail bloqueante")

    async def aclose(self) -> None:
        return None


DESCRIPTOR = StyleDescriptor(
    palette=["ocre queimado", "verde-cafeeiro profundo", "ambar de amanhecer"],
    light_quality="luz natural lateral suave, sombras longas de golden hour",
    lens="50mm equivalente, profundidade de campo rasa, bokeh cremoso",
    texture="grain fino de filme, microcontraste alto, sem saturacao artificial",
    framing="sujeito descentralizado, respiro negativo a direita",
    recurring_materials=["madeira rustica de lei", "aco inox escovado", "juta"],
    mood="elegancia rustica e cientifica, calma, artesanal",
    avoid=["saturacao HDR", "reflexos plasticos", "iluminacao de estudio dura"],
)


@pytest.fixture
def catalog(conn, settings, photo_factory):
    """Base ingerida, curada e com templates sincronizados."""
    from cie.prompt import build_prompt_fragment
    from cie.template_loader import sync_templates

    base = settings.root / "base"
    photo_factory(base / "CANASTRA_3_TORREFACAO_TAMBOR_001.jpg", size=(2400, 1600), seed=31)
    photo_factory(base / "CANASTRA_3_TORREFACAO_CUPPING_002.jpg", size=(2400, 1600), seed=32)
    photo_factory(
        base / "CANASTRA_PRODUCT_ESTUDIO_GEISHA_PACOTE_003.jpg", size=(2400, 1600), seed=33
    )
    ingest_directory(conn, settings, base)

    # Curadoria humana: sem pessoa identificavel, serve de referencia.
    for asset in repository.list_assets(conn):
        repository.update_asset_curation(
            conn,
            asset.id,
            has_identifiable_person=False,
            is_reference_grade=True,
            needs_review=False,
        )

    sync_templates(conn, TEMPLATES_DIR)

    dna_id = repository.upsert_style_dna(
        conn,
        StyleDna(
            name="laboratorio-uberlandia",
            pillar=Pillar.P3,
            source_asset_ids=[a.id for a in repository.list_assets(conn)],
            descriptor=DESCRIPTOR,
            prompt_fragment=build_prompt_fragment(DESCRIPTOR),
        ),
    )
    return {"dna_id": dna_id}


# --------------------------------------------------------------------------- #
# fluxo completo
# --------------------------------------------------------------------------- #


def test_templates_are_all_loadable(conn, catalog):
    """As 12 cenas entram no banco e cobrem os quatro pilares."""
    templates = repository.list_templates(conn)

    assert len(templates) >= 12
    pillars = {str(t.pillar) for t in templates if t.pillar}
    assert {"1", "2", "3", "4"} <= pillars


def test_dry_run_resolves_prompt_without_touching_api(conn, settings, catalog):
    from cie.queue import PlanEntry, build_job

    entry = PlanEntry(template="macro_grao_torrado", dna="laboratorio-uberlandia", n=2)
    job, report, payload = build_job(conn, settings, entry, capabilities=ApiCapabilities())

    assert job.resolved_prompt
    # Ordem da composicao: corpo do template, depois o DNA, depois o negative.
    assert "elegancia rustica" in job.resolved_prompt.lower() or "rustic" in job.resolved_prompt.lower()
    assert "warped text" in job.resolved_prompt.lower()
    assert not report.blocked
    # Sem sondagem confirmada, a estrategia tem que ser a descritiva.
    assert payload.strategy == "descriptor"
    assert payload.extra.get("image") is None


def test_packaging_template_without_reference_is_blocked(conn, settings, catalog):
    """A regra que protege o rotulo: bloqueia antes de gastar credito."""
    from cie.queue import PlanEntry, build_job

    entry = PlanEntry(template="pacote_madeira_rustica", n=1)
    _, report, _ = build_job(conn, settings, entry, capabilities=ApiCapabilities())

    assert report.blocked
    rules = {r.rule for r in report.blocking}
    assert "packaging_requires_reference" in rules


def test_blocked_job_never_reaches_the_api(conn, settings, catalog):
    from cie.queue import PlanEntry, add_jobs_from_plan, run_queue
    import yaml

    plan = settings.root / "plano.yaml"
    plan.write_text(
        yaml.safe_dump({"jobs": [{"template": "pacote_madeira_rustica", "n": 1}]}),
        encoding="utf-8",
    )
    add_jobs_from_plan(conn, settings, plan)

    result = asyncio.run(
        run_queue(conn, settings, limit=10, budget_usd=1.0, client=ExplodingClient())
    )

    assert result.done == 0
    assert repository.count_jobs(conn, "blocked") >= 1


def test_full_pipeline_generate_review_export_report(conn, settings, catalog):
    from cie.export import export_approved
    from cie.queue import PlanEntry, add_jobs_from_plan, run_queue
    from cie.reports import cost_report
    import yaml

    plan = settings.root / "plano.yaml"
    plan.write_text(
        yaml.safe_dump(
            {
                "jobs": [
                    {"template": "macro_grao_torrado", "dna": "laboratorio-uberlandia", "n": 2},
                    {"template": "terreiro_secagem", "n": 1},
                ]
            }
        ),
        encoding="utf-8",
    )
    jobs = add_jobs_from_plan(conn, settings, plan)
    assert len(jobs) == 2

    client = FakeClient()
    result = asyncio.run(
        run_queue(conn, settings, limit=10, budget_usd=5.00, client=client)
    )

    assert result.done == 2
    assert client.calls, "a fila deveria ter chamado o cliente"
    assert result.spent_usd > 0

    generations = repository.list_generations(conn)
    assert len(generations) == 3  # n=2 + n=1
    for generation in generations:
        assert Path(generation.path).exists()
        assert generation.disclosure_required is True
        assert generation.prompt
        assert generation.cost_usd >= 0

    # Revisao humana: aprova duas, rejeita uma.
    repository.set_review_status(conn, generations[0].id, ReviewStatus.APPROVED)
    repository.set_review_status(conn, generations[1].id, ReviewStatus.APPROVED)
    repository.set_review_status(
        conn, generations[2].id, ReviewStatus.REJECTED, "tipografia do rotulo errada"
    )

    batch = export_approved(
        conn, settings, formats=("9:16", "4:5", "1:1"), out_dir=settings.root / "export"
    )

    assert len(batch.variants) == 6  # 2 aprovadas x 3 proporcoes
    for variant in batch.variants:
        assert Path(variant.path).exists()
        assert Path(variant.path).suffix == ".jpg"
        assert Path(variant.path).name.startswith("CANASTRA_")

    manifest = json.loads(Path(batch.manifest_path).read_text(encoding="utf-8"))
    assert manifest, "manifesto vazio"

    report = cost_report(conn)
    assert report.images == 3
    assert report.total_usd == pytest.approx(
        sum(g.cost_usd for g in generations), rel=1e-6
    )
    assert report.rejected_usd > 0


def test_budget_ceiling_stops_before_overspending(conn, settings, catalog):
    from cie.queue import add_jobs_from_plan, run_queue
    import yaml

    plan = settings.root / "plano.yaml"
    plan.write_text(
        yaml.safe_dump(
            {"jobs": [{"template": "macro_grao_torrado", "n": 1} for _ in range(10)]}
        ),
        encoding="utf-8",
    )
    add_jobs_from_plan(conn, settings, plan)

    # Teto que cabe so uma fracao dos jobs.
    client = FakeClient()
    result = asyncio.run(
        run_queue(conn, settings, limit=10, budget_usd=0.05, client=client)
    )

    assert result.spent_usd <= 0.05
    assert result.stopped_by_budget is True
    assert result.pending > 0
    assert len(client.calls) < 10


def test_api_failure_marks_job_failed_with_raw_body(conn, settings, catalog):
    from cie.errors import XaiApiError
    from cie.queue import add_jobs_from_plan, run_queue
    import yaml

    plan = settings.root / "plano.yaml"
    plan.write_text(
        yaml.safe_dump({"jobs": [{"template": "macro_grao_torrado", "n": 1}]}),
        encoding="utf-8",
    )
    add_jobs_from_plan(conn, settings, plan)

    client = FakeClient(
        fail_with=XaiApiError("erro do servidor", status_code=500, raw='{"error":"boom"}')
    )
    result = asyncio.run(
        run_queue(conn, settings, limit=5, budget_usd=1.0, client=client)
    )

    assert result.failed == 1
    failed = repository.list_jobs(conn, status="failed")
    assert failed
    assert "boom" in (failed[0].blocked_reason or "")


def test_dry_run_queue_writes_nothing(conn, settings, catalog):
    from cie.queue import add_jobs_from_plan, run_queue
    import yaml

    plan = settings.root / "plano.yaml"
    plan.write_text(
        yaml.safe_dump({"jobs": [{"template": "macro_grao_torrado", "n": 2}]}),
        encoding="utf-8",
    )
    add_jobs_from_plan(conn, settings, plan)

    result = asyncio.run(
        run_queue(conn, settings, limit=5, budget_usd=1.0, client=ExplodingClient(), dry_run=True)
    )

    assert repository.list_generations(conn) == []
    assert result.spent_usd == 0.0
