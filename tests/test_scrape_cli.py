"""CLI do scrape. Nenhum teste aqui abre browser nem toca a rede."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from cie.cli import app

runner = CliRunner()


def _envelope(slug="cafecanastra") -> dict:
    return {
        "target": {"kind": "profile", "slug": slug, "handle": slug},
        "harvested_at": "2026-08-18T21:30:00+00:00",
        "source": "feed_user",
        "pages": [
            {
                "items": [
                    {
                        "code": "AAA111",
                        "taken_at": 1786000000,
                        "media_type": 1,
                        "user": {"username": slug},
                        "caption": {"text": "legenda"},
                        "image_versions2": {
                            "candidates": [
                                {
                                    "url": "https://cdn.example/AAA111.jpg",
                                    "width": 1080,
                                    "height": 1350,
                                }
                            ]
                        },
                    }
                ]
            }
        ],
    }


def test_scrape_aparece_no_help():
    resultado = runner.invoke(app, ["--help"])
    assert resultado.exit_code == 0
    assert "scrape" in resultado.stdout


def test_help_do_scrape_lista_os_comandos():
    resultado = runner.invoke(app, ["scrape", "--help"])
    assert resultado.exit_code == 0
    for comando in ("login", "status", "harvest", "collect", "run"):
        assert comando in resultado.stdout


def test_link_invalido_falha_com_mensagem_e_nao_stacktrace():
    resultado = runner.invoke(app, ["scrape", "run", "https://example.com/x", "--dry-run"])
    assert resultado.exit_code != 0
    assert "instagram.com" in resultado.stdout


def test_reel_e_recusado_pela_cli():
    resultado = runner.invoke(
        app, ["scrape", "run", "https://www.instagram.com/reel/AAA111/", "--dry-run"]
    )
    assert resultado.exit_code != 0
    assert "reel" in resultado.stdout.lower()


def test_collect_em_dry_run_nao_escreve_imagem(tmp_path: Path):
    arquivo = tmp_path / "colheita.json"
    arquivo.write_text(json.dumps(_envelope()), encoding="utf-8")

    resultado = runner.invoke(
        app,
        ["scrape", "collect", str(arquivo), "--out", str(tmp_path / "saida"), "--dry-run"],
    )

    assert resultado.exit_code == 0
    assert list((tmp_path / "saida").rglob("*.jpg")) == []
    assert "1" in resultado.stdout


def test_collect_de_arquivo_inexistente_falha_com_mensagem(tmp_path: Path):
    resultado = runner.invoke(app, ["scrape", "collect", str(tmp_path / "nao-existe.json")])
    assert resultado.exit_code != 0
    assert "nao-existe.json" in resultado.stdout


def test_collect_de_json_invalido_falha_com_mensagem(tmp_path: Path):
    arquivo = tmp_path / "quebrado.json"
    arquivo.write_text("{isto nao e json", encoding="utf-8")

    resultado = runner.invoke(app, ["scrape", "collect", str(arquivo)])
    assert resultado.exit_code != 0
    assert "json" in resultado.stdout.lower()


def test_falha_nao_vaza_stacktrace_no_console(tmp_path: Path):
    """`_falha` e chamada de dentro de um `except CieError`; o usuario deve ver
    so a mensagem amigavel, nunca um traceback do Python."""
    arquivo = tmp_path / "quebrado.json"
    arquivo.write_text("{isto nao e json", encoding="utf-8")

    resultado = runner.invoke(app, ["scrape", "collect", str(arquivo)])

    assert resultado.exit_code != 0
    assert "Traceback" not in resultado.stdout
    assert "Traceback" not in resultado.stderr if resultado.stderr else True


def test_out_root_none_nao_vira_string_none():
    """`--out` omitido deve resultar em `None` de verdade, nao na string 'None'
    (risco de `Path = typer.Option(None, ...)` sem `Optional`)."""
    from cie.scrape.cli import _out_root

    assert _out_root(None) is not None
    assert "None" not in str(_out_root(None))

    escolhido = Path("qualquer/lugar")
    assert _out_root(escolhido) == escolhido


def test_status_sem_login_falha_com_mensagem_util_e_sem_abrir_browser(settings):
    """Perfil nunca criado (nunca logou): a mensagem deve orientar 'cie scrape
    login', e o comando nao pode tentar abrir o Playwright para chegar la."""
    resultado = runner.invoke(app, ["scrape", "status"])

    assert resultado.exit_code != 0
    assert "cie scrape login" in resultado.stdout


def test_mensagem_de_erro_longa_nao_quebra_substring_no_meio(tmp_path: Path, monkeypatch):
    """Reproduz o cenario do weak spot 3: um caminho longo o bastante para
    estourar a largura padrao do console (79 colunas fora de um terminal real)
    nao pode partir o nome do arquivo ao meio."""
    pasta_funda = tmp_path
    for _ in range(6):
        pasta_funda = pasta_funda / ("x" * 20)
    arquivo = pasta_funda / "nao-existe.json"

    resultado = runner.invoke(app, ["scrape", "collect", str(arquivo)])

    assert resultado.exit_code != 0
    assert "nao-existe.json" in resultado.stdout


def test_collect_com_erro_de_leitura_falha_com_mensagem_e_nao_stacktrace(
    tmp_path: Path, monkeypatch
):
    """Arquivo existe e passa em `is_file()`, mas a leitura falha (ex.: permissao
    negada). Isso deve virar mensagem amigavel, nao uma excecao nao tratada."""
    arquivo = tmp_path / "sem-permissao.json"
    arquivo.write_text("{}", encoding="utf-8")

    def _read_text_falho(self, *args, **kwargs):
        raise PermissionError("acesso negado (simulado)")

    monkeypatch.setattr(Path, "read_text", _read_text_falho)

    resultado = runner.invoke(app, ["scrape", "collect", str(arquivo)])

    assert resultado.exit_code != 0
    assert "Traceback" not in resultado.stdout
    assert "sem-permissao.json" in resultado.stdout
