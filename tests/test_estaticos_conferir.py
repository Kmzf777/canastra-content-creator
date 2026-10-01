import pytest
from PIL import Image

from instagram.estaticos.conferir import VEREDITOS, bloqueia, recortes


def _png(tmp_path, nome, tamanho=(400, 500), cor=(120, 90, 60)):
    p = tmp_path / nome
    Image.new("RGB", tamanho, cor).save(p)
    return p


def test_grava_um_par_de_recortes_por_string(tmp_path):
    gerada = _png(tmp_path, "g.png")
    ref = _png(tmp_path, "r.png")
    faixas = {"SCA 80+": (10, 20, 110, 60), "250g": (10, 80, 90, 120)}

    pares = recortes(gerada, ref, faixas, tmp_path / "out")

    assert set(pares) == {"SCA 80+", "250g"}
    for nome, (a, b) in pares.items():
        assert a.exists() and b.exists(), f"{nome}: faltou um dos lados"
        assert a != b


def test_amplia_pelo_fator_declarado(tmp_path):
    gerada = _png(tmp_path, "g.png")
    ref = _png(tmp_path, "r.png")
    pares = recortes(gerada, ref, {"x": (0, 0, 50, 25)}, tmp_path / "out", fator=4)

    with Image.open(pares["x"][0]) as im:
        assert im.size == (200, 100)


def test_nome_de_arquivo_e_seguro_para_string_com_simbolo(tmp_path):
    """`SCA 80+` nao pode virar caminho invalido no Windows."""
    gerada = _png(tmp_path, "g.png")
    ref = _png(tmp_path, "r.png")
    pares = recortes(gerada, ref, {"SCA 80+": (0, 0, 50, 25)}, tmp_path / "out")
    for p in pares["SCA 80+"]:
        assert "+" not in p.name
        assert " " not in p.name


def test_faixa_fora_da_imagem_levanta_em_vez_de_recortar_vazio(tmp_path):
    gerada = _png(tmp_path, "g.png", tamanho=(100, 100))
    ref = _png(tmp_path, "r.png", tamanho=(100, 100))
    with pytest.raises(ValueError, match="fora"):
        recortes(gerada, ref, {"x": (50, 50, 300, 300)}, tmp_path / "out")


def test_vereditos_sao_os_tres_de_canastra_conteudo():
    assert VEREDITOS == ("ok", "errado", "nao-verificavel")


def test_nao_verificavel_bloqueia_e_ok_nao():
    """Licao 18: ilegivel nao e 'confere'. Nao verificavel barra a peca."""
    assert bloqueia({"a": "ok", "b": "ok"}) == ()
    assert bloqueia({"a": "ok", "b": "nao-verificavel"}) == ("b",)
    assert bloqueia({"a": "errado"}) == ("a",)
    assert bloqueia({"a": "errado", "b": "nao-verificavel"}) == ("a", "b")


def test_veredito_invalido_levanta():
    with pytest.raises(ValueError, match="confere"):
        bloqueia({"a": "confere"})
