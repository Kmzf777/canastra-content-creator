"""HTML por tipo, render no Chrome e medicao real."""
from pathlib import Path

import pytest
from PIL import Image

from instagram.carrossel import render, tipos
from instagram.carrossel.molde import ALTURA, LARGURA, PISO_QUADRO_PX, SEGURO_BASE, SEGURO_TOPO

TEM_CHROME = Path(render.CHROME_PADRAO).exists()
precisa_chrome = pytest.mark.skipif(not TEM_CHROME, reason="Chrome nao instalado")


@pytest.fixture
def foto(tmp_path) -> Path:
    p = tmp_path / "f.png"
    Image.new("RGB", (1080, 972), (40, 80, 40)).save(p)
    return p


def _um_de_cada(foto) -> dict[str, tipos.Slide]:
    return {
        "capa": tipos.Slide("capa", "foto", {"manchete": "Manchete", "badge": "ARRASTE"}, foto),
        "conceito": tipos.Slide("conceito", "terra", {"titulo": "Titulo", "corpo": "Corpo."}),
        "lista": tipos.Slide("lista", "creme", {"titulo": "T", "itens": ["um", "dois"]}),
        "passo": tipos.Slide("passo", "terra", {"titulo": "T", "passos": [
            {"titulo": "Primeiro", "texto": "x"}, {"titulo": "Segundo"}]}),
        "comparacao": tipos.Slide("comparacao", "creme", {
            "rotulo_esq": "Antes", "itens_esq": ["a", "b"],
            "rotulo_dir": "Depois", "itens_dir": ["c", "d"]}),
        "numero": tipos.Slide("numero", "terra", {"numero": "1.250 m", "rotulo": "Altitude"}),
        "citacao": tipos.Slide("citacao", "creme", {"frase": "Uma frase.", "autor": "Arthur"}),
        "produto": tipos.Slide("produto", "foto", {"nome": "Classico", "descritor": "Corpo firme."}, foto),
        "prova": tipos.Slide("prova", "creme", {
            "afirmacao": "Especial nao e adjetivo.", "evidencia": "SCAA 80+ na caixa.",
            "fonte": "Arte da embalagem"}),
        "fecho": tipos.Slide("fecho", "terra", {"manchete": "Fim", "destino": "site"}),
    }


def test_todos_os_tipos_produzem_html(foto):
    for nome, s in _um_de_cada(foto).items():
        h = render.html_do_slide(s, 1, 5)
        assert h.startswith("<!doctype html>"), nome
        assert f"{LARGURA}px" in h and f"{ALTURA}px" in h, nome


def test_cada_tipo_pinta_diferente(foto):
    """A razao de existir do motor: a versao anterior usava um layout so."""
    corpos = {n: render._corpo_do_tipo(s) for n, s in _um_de_cada(foto).items()}
    assert len(set(corpos.values())) == len(corpos), "dois tipos renderizaram igual"


def test_texto_declarado_aparece_no_html(foto):
    s = _um_de_cada(foto)["prova"]
    h = render.html_do_slide(s, 2, 7)
    assert "Especial nao e adjetivo." in h
    assert "SCAA 80+ na caixa." in h
    assert "Arte da embalagem" in h, "a fonte da prova tem que aparecer"


def test_area_segura_entra_no_css(foto):
    h = render.html_do_slide(_um_de_cada(foto)["conceito"], 1, 3)
    assert f"top:{SEGURO_TOPO}px" in h
    assert f"bottom:{SEGURO_BASE}px" in h


def test_nenhum_tamanho_abaixo_do_piso():
    """Se a escala violar o piso, o portao de legibilidade reprovaria todo deck."""
    assert min(render.ESCALA.values()) >= PISO_QUADRO_PX


def test_escrever_html_grava_um_por_slide(foto, tmp_path):
    d = tipos.Deck(slug="d", slides=(
        _um_de_cada(foto)["capa"],
        _um_de_cada(foto)["prova"],
        _um_de_cada(foto)["fecho"],
    ))
    paths = render.escrever_html(d, tmp_path / "html")
    assert len(paths) == 3
    assert all(p.exists() for p in paths)
    assert "3 / 3" in paths[2].read_text(encoding="utf-8")


@precisa_chrome
def test_render_sai_em_1080x1350(foto, tmp_path):
    d = tipos.Deck(slug="d", slides=(
        _um_de_cada(foto)["capa"],
        _um_de_cada(foto)["prova"],
        _um_de_cada(foto)["fecho"],
    ))
    htmls = render.escrever_html(d, tmp_path / "html")
    pngs = render.render(htmls[:1], tmp_path / "png")
    with Image.open(pngs[0]) as im:
        assert im.size == (LARGURA, ALTURA)


@precisa_chrome
def test_medir_devolve_medicao_de_verdade(foto, tmp_path):
    d = tipos.Deck(slug="d", slides=(
        _um_de_cada(foto)["capa"],
        _um_de_cada(foto)["prova"],
        _um_de_cada(foto)["fecho"],
    ))
    htmls = render.escrever_html(d, tmp_path / "html")
    m = render.medir(htmls[1])
    assert m["slide"] == 2
    assert m["textos"], "nenhum campo medido"
    campos = {t["campo"] for t in m["textos"]}
    assert {"afirmacao", "evidencia", "fonte"} <= campos
    for t in m["textos"]:
        assert t["px"] > 0


@precisa_chrome
def test_miniaturas_nas_larguras_do_feed(foto, tmp_path):
    d = tipos.Deck(slug="d", slides=(
        _um_de_cada(foto)["capa"],
        _um_de_cada(foto)["prova"],
        _um_de_cada(foto)["fecho"],
    ))
    htmls = render.escrever_html(d, tmp_path / "html")
    png = render.render(htmls[:1], tmp_path / "png")[0]
    minis = render.miniaturas(png, tmp_path / "_feed")
    assert set(minis) == {360, 320}
    with Image.open(minis[360]) as im:
        assert im.width == 360
