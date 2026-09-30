"""Trimap por limiar: fundo 0.0, objeto 1.0, incerteza so na borda.

Tarefa 1 do plano docs/superpowers/plans/2026-09-30-assets-recorte-e-geracao.md.
Arquivo separado de tests/test_recorte.py de proposito: outro agente escreve
naquele em paralelo.
"""

import numpy as np

from instagram.recorte.trimap import gerar_trimap


def _quadrado_em_fundo_claro():
    """Objeto escuro 40x40 centrado num fundo claro 100x100."""
    img = np.full((100, 100, 3), 235, dtype=np.uint8)
    img[30:70, 30:70] = (60, 45, 30)
    return img


def test_trimap_marca_fundo_como_zero():
    t = gerar_trimap(_quadrado_em_fundo_claro(), banda=3)
    assert t[0, 0] == 0.0
    assert t[99, 99] == 0.0


def test_trimap_marca_interior_do_objeto_como_um():
    t = gerar_trimap(_quadrado_em_fundo_claro(), banda=3)
    assert t[50, 50] == 1.0


def test_faixa_desconhecida_so_existe_na_borda():
    t = gerar_trimap(_quadrado_em_fundo_claro(), banda=3)
    desconhecido = (t > 0.0) & (t < 1.0)
    # nenhuma incerteza no centro do objeto
    assert not desconhecido[45:55, 45:55].any()
    # mas existe incerteza em volta da borda
    assert desconhecido.any()


def test_banda_maior_alarga_a_faixa_desconhecida():
    img = _quadrado_em_fundo_claro()
    estreita = ((gerar_trimap(img, banda=2) > 0) & (gerar_trimap(img, banda=2) < 1)).sum()
    larga = ((gerar_trimap(img, banda=8) > 0) & (gerar_trimap(img, banda=8) < 1)).sum()
    assert larga > estreita
