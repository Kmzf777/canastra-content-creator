from __future__ import annotations

import re

import pytest
from typer.testing import CliRunner

from cie.cli import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def wide_terminal(monkeypatch: pytest.MonkeyPatch) -> None:
    """Rich trunca colunas em 80 caracteres; nos testes queremos a saida inteira."""
    monkeypatch.setenv("COLUMNS", "200")
    monkeypatch.setenv("TERM", "dumb")


def flat(text: str) -> str:
    """Normaliza espacos/quebras que o rich insere ao formatar tabelas."""
    return re.sub(r"\s+", " ", text)


def test_version_command(settings):
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "Canastra Image Engine" in result.stdout


def test_ingest_then_list(settings, tmp_path, photo_factory):
    base = tmp_path / "base"
    photo_factory(base / "CANASTRA_3_TORREFACAO_TAMBOR_001.jpg", seed=21)

    ingest_result = runner.invoke(app, ["ingest", str(base), "--verbose"])
    assert ingest_result.exit_code == 0, ingest_result.stdout
    assert "ingeridos" in ingest_result.stdout

    list_result = runner.invoke(app, ["assets", "list"])
    assert list_result.exit_code == 0
    assert "CANASTRA_3_TORREFACAO_TAMBOR_001.jpg" in flat(list_result.stdout)
    assert "torrefacao_uberlandia" in flat(list_result.stdout)


def test_list_filters_by_pillar(settings, tmp_path, photo_factory):
    base = tmp_path / "base"
    photo_factory(base / "CANASTRA_1_FAZENDA_CAFEZAL_001.jpg", seed=23)
    runner.invoke(app, ["ingest", str(base)])

    hit = runner.invoke(app, ["assets", "list", "--pillar", "1"])
    miss = runner.invoke(app, ["assets", "list", "--pillar", "4"])

    assert "CANASTRA_1_FAZENDA_CAFEZAL_001.jpg" in flat(hit.stdout)
    assert "nenhum asset encontrado" in miss.stdout


def test_curate_sets_human_only_fields(settings, tmp_path, photo_factory):
    base = tmp_path / "base"
    photo_factory(base / "CANASTRA_1_FAZENDA_COLHEITA_001.jpg", seed=22)
    runner.invoke(app, ["ingest", str(base)])

    show_before = runner.invoke(app, ["assets", "show", "1"])
    assert "has_identifiable_person True" in flat(show_before.stdout)

    result = runner.invoke(app, ["assets", "curate", "1", "--no-person", "--consent", "--done"])
    assert result.exit_code == 0

    show_after = runner.invoke(app, ["assets", "show", "1"])
    assert "has_identifiable_person False" in flat(show_after.stdout)
    assert "consent_on_file True" in flat(show_after.stdout)
    assert "needs_review False" in flat(show_after.stdout)


def test_curate_unknown_asset_fails(settings):
    runner.invoke(app, ["db", "migrate"])
    result = runner.invoke(app, ["assets", "curate", "999", "--no-person"])

    assert result.exit_code == 1


def test_db_status_lists_applied_migrations(settings):
    runner.invoke(app, ["db", "migrate"])
    result = runner.invoke(app, ["db", "status"])

    assert result.exit_code == 0
    assert "0001_initial.sql" in result.stdout
