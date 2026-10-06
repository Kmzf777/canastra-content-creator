"""A CLI: conferir devolve 1 de proposito, para quebrar script que ignora."""
import pytest

from instagram.carrossel import catalogo, cli, tipos


def test_conferir_ok(capsys):
    assert cli.main(["conferir"]) == 0
    assert "nenhum problema" in capsys.readouterr().out


def test_conferir_devolve_1_com_deck_invalido(monkeypatch, capsys):
    ruim = tipos.Deck(slug="ruim", slides=())
    monkeypatch.setattr(cli, "DECKS", [ruim])
    assert cli.main(["conferir"]) == 1
    assert "ruim" in capsys.readouterr().err


def test_listar(capsys):
    assert cli.main(["listar"]) == 0
    saida = capsys.readouterr().out
    assert "capsulas-qual-e-a-sua" in saida
    assert "tipos:" in saida and "fundos:" in saida


def test_prompt_traz_theme_lock(capsys):
    assert cli.main(["prompt", "capsulas-qual-e-a-sua"]) == 0
    saida = capsys.readouterr().out
    assert cli.THEME_LOCK in saida
    assert "ANCORA" in saida, "a capa tem que ser nomeada como ancora"


def test_slug_inexistente(capsys):
    assert cli.main(["prompt", "nao-existe"]) == 2
