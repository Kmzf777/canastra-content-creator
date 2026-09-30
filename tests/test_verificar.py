"""Laudo de preservacao de pixel: o portao que impede o motor de comer o rotulo.

Vive em arquivo proprio (e nao em tests/test_recorte.py, como o plano escreveu)
porque a Tarefa 1 do mesmo plano escreve nesse arquivo em paralelo.
Plano: docs/superpowers/plans/2026-09-30-assets-recorte-e-geracao.md, Tarefa 2.
"""

import numpy as np

from instagram.recorte.verificar import laudo_preservacao


def test_alfa_cheio_e_rgb_igual_nao_acusa_diferenca():
    rgb = np.full((50, 50, 3), 128, dtype=np.uint8)
    alfa = np.full((50, 50), 255, dtype=np.uint8)
    r = laudo_preservacao(rgb, rgb.copy(), alfa)
    assert r["pixels_alterados"] == 0
    assert r["maior_delta"] == 0
    assert r["aprovado"] is True


def test_um_pixel_alterado_no_opaco_reprova():
    rgb = np.full((50, 50, 3), 128, dtype=np.uint8)
    saida = rgb.copy()
    saida[10, 10] = (120, 128, 128)
    alfa = np.full((50, 50), 255, dtype=np.uint8)
    r = laudo_preservacao(rgb, saida, alfa)
    assert r["pixels_alterados"] == 1
    assert r["aprovado"] is False


def test_retangulo_do_rotulo_precisa_de_alfa_cheio():
    rgb = np.full((50, 50, 3), 128, dtype=np.uint8)
    alfa = np.full((50, 50), 255, dtype=np.uint8)
    alfa[20, 20] = 250          # quase opaco -- e o bastante para reprovar
    r = laudo_preservacao(rgb, rgb.copy(), alfa,
                          retangulo_rotulo=(15, 15, 30, 30))
    assert r["aprovado"] is False
    assert r["alfa_minimo_no_rotulo"] == 250
