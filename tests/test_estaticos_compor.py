import numpy as np
import pytest
from PIL import Image

from instagram.estaticos.compor import colar_rotulo


def _rgba(tamanho, cor, alfa=255):
    return Image.new("RGBA", tamanho, (*cor, alfa))


def test_cola_o_recorte_na_caixa_e_o_laudo_aprova():
    peca = Image.new("RGB", (200, 250), (10, 10, 10))
    recorte = _rgba((40, 50), (200, 150, 100))

    final, laudo = colar_rotulo(peca, recorte, caixa=(20, 30, 60, 80))

    assert final.size == (200, 250)
    assert laudo["aprovado"] is True
    assert laudo["pixels_alterados"] == 0
    assert laudo["alfa_minimo_no_rotulo"] == 255
    assert final.convert("RGB").getpixel((21, 31)) == (200, 150, 100)


def test_fora_da_caixa_nada_muda():
    peca = Image.new("RGB", (200, 250), (10, 20, 30))
    antes = np.array(peca)
    final, _ = colar_rotulo(peca, _rgba((40, 50), (9, 9, 9)), caixa=(20, 30, 60, 80))
    depois = np.array(final.convert("RGB"))

    mascara = np.ones(antes.shape[:2], bool)
    mascara[30:80, 20:60] = False
    assert np.array_equal(antes[mascara], depois[mascara])


def test_o_laudo_NAO_e_tautologico():
    """O portao que protege contra o bug de verificar.py.

    Se alguem implementar comparando a peca consigo mesma, este teste passa a
    aprovar uma colagem corrompida. Aqui a colagem e sabotada de proposito: o
    laudo TEM que reprovar.
    """
    peca = Image.new("RGB", (100, 100), (0, 0, 0))
    recorte = _rgba((20, 20), (255, 255, 255))

    final, laudo = colar_rotulo(peca, recorte, caixa=(10, 10, 30, 30), _sabotar=True)
    assert laudo["aprovado"] is False
    assert laudo["pixels_alterados"] > 0


def test_recorte_com_alfa_parcial_no_rotulo_reprova():
    """Tipografia impressa nao admite transparencia parcial."""
    peca = Image.new("RGB", (100, 100), (0, 0, 0))
    recorte = _rgba((20, 20), (255, 255, 255), alfa=200)
    _, laudo = colar_rotulo(peca, recorte, caixa=(10, 10, 30, 30))
    assert laudo["alfa_minimo_no_rotulo"] == 200
    assert laudo["aprovado"] is False


def test_reamostragem_e_comparada_contra_a_mesma_reamostragem():
    """Se o recorte precisa encolher, o laudo compara contra o recorte JA
    encolhido -- nao contra o original, que daria falso negativo garantido."""
    peca = Image.new("RGB", (100, 100), (0, 0, 0))
    recorte = _rgba((80, 80), (123, 45, 67))
    _, laudo = colar_rotulo(peca, recorte, caixa=(10, 10, 30, 30))
    assert laudo["aprovado"] is True
    assert laudo["reamostrado"] == [80, 80, 20, 20]


def test_caixa_fora_da_peca_levanta():
    peca = Image.new("RGB", (50, 50), (0, 0, 0))
    with pytest.raises(ValueError, match="fora"):
        colar_rotulo(peca, _rgba((10, 10), (1, 2, 3)), caixa=(40, 40, 90, 90))
