"""Os tres portoes: declarado, medido, e medido contra piso declarado."""
from pathlib import Path

import pytest
from PIL import Image

from instagram.carrossel import portoes, tipos
from instagram.carrossel.molde import PISO_QUADRO_PX


@pytest.fixture
def foto(tmp_path) -> Path:
    p = tmp_path / "f.png"
    Image.new("RGB", (8, 10), "black").save(p)
    return p


@pytest.fixture
def deck(foto):
    return tipos.Deck(slug="d", slides=(
        tipos.Slide("capa", "foto", {"manchete": "Oi"}, foto),
        tipos.Slide("prova", "creme", {"afirmacao": "a", "evidencia": "b", "fonte": "c"}),
        tipos.Slide("fecho", "terra", {"manchete": "Tchau"}),
    ))


def _medicao(**kw):
    base = {"slide": 1, "transbordos": [], "textos": [], "fora_da_area_segura": []}
    base.update(kw)
    return base


def test_deck_valido_passa_nos_tres(deck):
    r = portoes.todos(deck, [_medicao()])
    assert r["ok"] is True
    assert r["orcamento"] == [] and r["transbordo"] == [] and r["legibilidade"] == []


def test_orcamento_pega_campo_acima_do_teto(foto):
    d = tipos.Deck(slug="d", slides=(
        tipos.Slide("capa", "foto", {"manchete": "x" * 61}, foto),
        tipos.Slide("prova", "creme", {"afirmacao": "a", "evidencia": "b", "fonte": "c"}),
        tipos.Slide("fecho", "terra", {"manchete": "T"}),
    ))
    problemas = portoes.orcamento(d)
    assert any("61 caracteres" in x for x in problemas)


def test_transbordo_reprova_caixa_estourada():
    problemas = portoes.transbordo([_medicao(slide=3, transbordos=["corpo"])])
    assert len(problemas) == 1
    assert "slide 3" in problemas[0] and "corpo" in problemas[0]
    assert "TRANSBORDA" in problemas[0]


def test_transbordo_reprova_area_segura():
    problemas = portoes.transbordo([_medicao(slide=2, fora_da_area_segura=["titulo"])])
    assert len(problemas) == 1
    assert "area segura" in problemas[0]


def test_legibilidade_fronteira_do_piso():
    abaixo = portoes.legibilidade(
        [_medicao(textos=[{"campo": "sub", "px": PISO_QUADRO_PX - 1}])])
    assert len(abaixo) == 1, "32px tem que reprovar"
    assert "no feed" in abaixo[0], "a mensagem mostra o px no feed, nao so no quadro"

    no_piso = portoes.legibilidade(
        [_medicao(textos=[{"campo": "sub", "px": PISO_QUADRO_PX}])])
    assert no_piso == [], "33px tem que passar"


def test_todos_devolve_nao_ok_quando_um_reprova(deck):
    r = portoes.todos(deck, [_medicao(transbordos=["corpo"])])
    assert r["ok"] is False
    assert r["transbordo"] and not r["orcamento"]
