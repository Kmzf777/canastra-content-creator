"""Relatorios de custo: agregacao, filtros de janela e projecao de orcamento."""

from __future__ import annotations

import itertools
import sqlite3
from datetime import datetime, timezone

import pytest

from cie import repository
from cie.enums import Pillar, ReviewStatus, TemplateKind
from cie.models import Generation, Job, Template
from cie.reports import (
    EMPTY_MESSAGE,
    NO_PILLAR_KEY,
    UNKNOWN_KEY,
    CostBucket,
    budget_forecast,
    cost_report,
    render_cost_report,
    render_cost_report_text,
)

_SEQUENCE = itertools.count(1)


def _at(day: int, hour: int = 12) -> datetime:
    return datetime(2026, 8, day, hour, 0, tzinfo=timezone.utc)


def _template(
    conn: sqlite3.Connection,
    name: str,
    pillar: Pillar | None = Pillar.P3,
    kind: TemplateKind = TemplateKind.MACRO,
) -> int:
    return repository.upsert_template(
        conn,
        Template(name=name, pillar=pillar, kind=kind, body="grao de {variedade} na esteira"),
    )


def _job(conn: sqlite3.Connection, template_id: int, model: str = "grok-imagine-image") -> int:
    return repository.insert_job(
        conn,
        Job(template_id=template_id, model=model, resolved_prompt="prompt resolvido"),
    )


def _generation(
    conn: sqlite3.Connection,
    job_id: int,
    *,
    cost: float,
    status: ReviewStatus = ReviewStatus.PENDING,
    model: str = "grok-imagine-image",
    created_at: datetime | None = None,
) -> int:
    index = next(_SEQUENCE)
    return repository.insert_generation(
        conn,
        Generation(
            job_id=job_id,
            path=f"/gen/{index:04d}.png",
            sha256=f"{index:064d}",
            model=model,
            prompt="prompt resolvido",
            cost_usd=cost,
            review_status=status,
            created_at=created_at or _at(1),
        ),
    )


@pytest.fixture
def populated(conn: sqlite3.Connection) -> sqlite3.Connection:
    """Cinco geracoes em tres dias, dois modelos, tres templates, tres status.

    Total 0.41 USD: aprovadas 0.14, rejeitadas 0.17, pendentes 0.10.
    """
    macro = _template(conn, "macro-torra", Pillar.P3)
    fazenda = _template(conn, "fazenda-amanhecer", Pillar.P1, TemplateKind.SCENE)
    orfao = _template(conn, "estudo-textura", None, TemplateKind.TEXTURE)

    macro_job = _job(conn, macro)
    fazenda_job = _job(conn, fazenda)
    orfao_job = _job(conn, orfao)

    _generation(conn, macro_job, cost=0.07, status=ReviewStatus.APPROVED, created_at=_at(1))
    _generation(conn, macro_job, cost=0.07, status=ReviewStatus.REJECTED, created_at=_at(1))
    _generation(conn, fazenda_job, cost=0.07, status=ReviewStatus.APPROVED, created_at=_at(2))
    _generation(
        conn,
        macro_job,
        cost=0.10,
        status=ReviewStatus.PENDING,
        model="grok-2-image",
        created_at=_at(3),
    )
    _generation(
        conn,
        orfao_job,
        cost=0.10,
        status=ReviewStatus.REJECTED,
        model="grok-2-image",
        created_at=_at(3),
    )
    return conn


def _keyed(buckets: list[CostBucket]) -> dict[str, CostBucket]:
    return {bucket.key: bucket for bucket in buckets}


# --------------------------------------------------------------------------- #
# totais e agrupamentos
# --------------------------------------------------------------------------- #


def test_total_matches_sum_of_generations(populated):
    report = cost_report(populated)

    assert report.images == 5
    assert report.total_usd == pytest.approx(0.41)
    assert report.approved_usd == pytest.approx(0.14)
    assert report.rejected_usd == pytest.approx(0.17)
    assert report.pending_usd == pytest.approx(0.10)
    assert report.approved_usd + report.rejected_usd + report.pending_usd == pytest.approx(
        report.total_usd
    )


@pytest.mark.parametrize("attribute", ["by_model", "by_template", "by_pillar", "by_day"])
def test_every_grouping_partitions_the_total(populated, attribute):
    report = cost_report(populated)
    buckets: list[CostBucket] = getattr(report, attribute)

    assert sum(b.cost_usd for b in buckets) == pytest.approx(report.total_usd)
    assert sum(b.images for b in buckets) == report.images


def test_group_by_model_sorted_by_cost(populated):
    report = cost_report(populated)

    assert [b.key for b in report.by_model] == ["grok-imagine-image", "grok-2-image"]
    imagine, grok2 = report.by_model
    assert imagine.images == 3
    assert imagine.cost_usd == pytest.approx(0.21)
    assert (imagine.approved, imagine.rejected, imagine.pending) == (2, 1, 0)
    assert grok2.cost_usd == pytest.approx(0.20)
    assert (grok2.approved, grok2.rejected, grok2.pending) == (0, 1, 1)


def test_group_by_template(populated):
    buckets = _keyed(cost_report(populated).by_template)

    assert set(buckets) == {"macro-torra", "fazenda-amanhecer", "estudo-textura"}
    assert buckets["macro-torra"].images == 3
    assert buckets["macro-torra"].cost_usd == pytest.approx(0.24)
    assert buckets["fazenda-amanhecer"].cost_usd == pytest.approx(0.07)


def test_group_by_pillar_uses_enum_values_and_fallback(populated):
    buckets = _keyed(cost_report(populated).by_pillar)

    assert set(buckets) == {Pillar.P3.value, Pillar.P1.value, NO_PILLAR_KEY}
    assert buckets[Pillar.P3.value].cost_usd == pytest.approx(0.24)
    assert buckets[Pillar.P1.value].approved == 1
    # Template sem pilar nao some do relatorio: vai para o balde nomeado.
    assert buckets[NO_PILLAR_KEY].cost_usd == pytest.approx(0.10)


def test_group_by_day_is_chronological(populated):
    report = cost_report(populated)

    assert [b.key for b in report.by_day] == ["2026-08-01", "2026-08-02", "2026-08-03"]
    assert [b.images for b in report.by_day] == [2, 1, 2]
    assert [b.cost_usd for b in report.by_day] == pytest.approx([0.14, 0.07, 0.20])


def test_missing_model_falls_back_to_unknown_key(conn):
    job = _job(conn, _template(conn, "sem-modelo"))
    _generation(conn, job, cost=0.05, model="")

    assert _keyed(cost_report(conn).by_model)[UNKNOWN_KEY].images == 1


# --------------------------------------------------------------------------- #
# janela de tempo
# --------------------------------------------------------------------------- #


def test_since_excludes_older_generations(populated):
    report = cost_report(populated, since="2026-08-02")

    assert report.since == "2026-08-02"
    assert report.images == 3
    assert report.total_usd == pytest.approx(0.27)
    assert [b.key for b in report.by_day] == ["2026-08-02", "2026-08-03"]
    # A janela nao apaga o historico: o total de sempre continua visivel.
    assert report.lifetime_usd == pytest.approx(0.41)


def test_until_excludes_newer_generations(populated):
    report = cost_report(populated, until="2026-08-02T23:59:59+00:00")

    assert report.images == 3
    assert report.total_usd == pytest.approx(0.21)
    assert [b.key for b in report.by_day] == ["2026-08-01", "2026-08-02"]


def test_since_and_until_narrow_to_a_single_day(populated):
    report = cost_report(populated, since="2026-08-02", until="2026-08-02T23:59:59+00:00")

    assert report.images == 1
    assert report.observed_days == 1
    assert report.total_usd == pytest.approx(0.07)


# --------------------------------------------------------------------------- #
# desperdicio e custo por aprovada
# --------------------------------------------------------------------------- #


def test_waste_ratio_and_cost_per_approved(populated):
    report = cost_report(populated)

    assert report.waste_ratio == pytest.approx(0.17 / 0.41)
    assert report.approved_images == 2
    # Custo por aprovada usa o custo TOTAL, nao so o das aprovadas.
    assert report.cost_per_approved == pytest.approx(0.41 / 2)


def test_waste_ratio_is_one_when_everything_was_rejected(conn):
    job = _job(conn, _template(conn, "so-lixo"))
    for _ in range(3):
        _generation(conn, job, cost=0.07, status=ReviewStatus.REJECTED)

    report = cost_report(conn)

    assert report.waste_ratio == pytest.approx(1.0)
    assert report.cost_per_approved is None


def test_empty_database_does_not_divide_by_zero(conn):
    report = cost_report(conn)

    assert report.images == 0
    assert report.total_usd == pytest.approx(0.0)
    assert report.waste_ratio == 0.0
    assert report.cost_per_approved is None
    assert report.observed_days == 0
    assert report.by_model == report.by_template == report.by_pillar == report.by_day == []


def test_cost_per_approved_is_none_without_approved(conn):
    job = _job(conn, _template(conn, "fila-parada"))
    _generation(conn, job, cost=0.07, status=ReviewStatus.PENDING)
    _generation(conn, job, cost=0.07, status=ReviewStatus.REJECTED)

    report = cost_report(conn)

    assert report.cost_per_approved is None
    assert report.by_model[0].cost_per_approved is None


def test_approval_rate_ignores_pending(conn):
    job = _job(conn, _template(conn, "revisao-parcial"))
    _generation(conn, job, cost=0.07, status=ReviewStatus.APPROVED)
    _generation(conn, job, cost=0.07, status=ReviewStatus.APPROVED)
    _generation(conn, job, cost=0.07, status=ReviewStatus.REJECTED)
    for _ in range(5):
        _generation(conn, job, cost=0.07, status=ReviewStatus.PENDING)

    bucket = cost_report(conn).by_model[0]

    assert bucket.reviewed == 3
    assert bucket.approval_rate == pytest.approx(2 / 3)


def test_bucket_without_review_has_zero_rate():
    bucket = CostBucket(key="vazio")

    assert bucket.approval_rate == 0.0
    assert bucket.cost_per_approved is None


# --------------------------------------------------------------------------- #
# projecao de orcamento
# --------------------------------------------------------------------------- #


def test_budget_forecast_projects_from_calendar_span(conn):
    """Gasto de 10 USD entre 01/08 e 05/08: 5 dias observados, 2 USD/dia."""
    job = _job(conn, _template(conn, "campanha-agosto"))
    _generation(conn, job, cost=2.5, status=ReviewStatus.APPROVED, created_at=_at(1))
    _generation(conn, job, cost=2.5, status=ReviewStatus.APPROVED, created_at=_at(1))
    _generation(conn, job, cost=2.5, status=ReviewStatus.REJECTED, created_at=_at(5))
    _generation(conn, job, cost=2.5, status=ReviewStatus.PENDING, created_at=_at(5))

    report = cost_report(conn)
    forecast = budget_forecast(report, 100.0)

    # Dois dias com geracao, mas cinco dias de calendario cobertos.
    assert report.observed_days == 5
    assert forecast["dias_observados"] == 5
    assert forecast["media_diaria"] == pytest.approx(2.0)
    assert forecast["projecao_mensal"] == pytest.approx(60.0)
    assert forecast["folga_ou_estouro"] == pytest.approx(40.0)
    assert forecast["imagens_aprovadas_por_dolar"] == pytest.approx(0.2)


def test_budget_forecast_flags_overrun_with_negative_slack(conn):
    job = _job(conn, _template(conn, "campanha-cara"))
    _generation(conn, job, cost=9.0, status=ReviewStatus.APPROVED, created_at=_at(1))

    forecast = budget_forecast(cost_report(conn), 100.0)

    assert forecast["dias_observados"] == 1
    assert forecast["projecao_mensal"] == pytest.approx(270.0)
    assert forecast["folga_ou_estouro"] == pytest.approx(-170.0)


def test_budget_forecast_on_empty_report(conn):
    forecast = budget_forecast(cost_report(conn), 50.0)

    assert forecast == {
        "dias_observados": 0,
        "media_diaria": 0.0,
        "projecao_mensal": 0.0,
        "folga_ou_estouro": 50.0,
        "imagens_aprovadas_por_dolar": 0.0,
    }


# --------------------------------------------------------------------------- #
# renderizacao
# --------------------------------------------------------------------------- #


def test_render_cost_report_returns_five_tables(populated):
    tables = render_cost_report(cost_report(populated))

    assert [str(table.title) for table in tables] == [
        "Custo CIE - resumo",
        "Custo por modelo",
        "Custo por template",
        "Custo por pilar",
        "Custo por dia",
    ]
    assert tables[1].row_count == 2  # dois modelos
    assert tables[4].row_count == 3  # tres dias


def test_render_cost_report_handles_empty_report(conn):
    tables = render_cost_report(cost_report(conn))

    assert len(tables) == 5
    assert tables[0].row_count > 0  # o resumo existe mesmo sem gasto
    # Os quatro recortes vazios avisam por legenda, em vez de sair so o cabecalho.
    assert all(table.row_count == 0 for table in tables[1:])
    assert all(table.caption == EMPTY_MESSAGE for table in tables[1:])


def test_render_cost_report_text_carries_the_numbers(populated):
    text = render_cost_report_text(cost_report(populated))

    assert "Custo CIE - resumo" in text
    assert "grok-imagine-image" in text
    assert "macro-torra" in text
    assert "2026-08-03" in text
    assert "0.4100" in text  # custo total formatado
    # O pilar ganha rotulo editorial na saida legivel.
    assert "Laboratorio de Torrefacao e Sensorialidade" in text


def test_render_cost_report_text_on_empty_report(conn):
    text = render_cost_report_text(cost_report(conn))

    assert EMPTY_MESSAGE in text
    assert "0.0000" in text
