"""Matting: alfa resolve a borda, o RGB do miolo fica intacto.

Tarefa 3 do plano docs/superpowers/plans/2026-09-30-assets-recorte-e-geracao.md.
Arquivo separado de tests/test_recorte.py de proposito: outro agente escreve
naquele em paralelo.

O teste que importa e `test_recorte_nao_altera_o_rgb_do_interior`. Se ele
falhar, o motor nao pode ser usado em embalagem: significa que o solver mexeu
em pixel de rotulo.
"""

import numpy as np

from instagram.recorte.matte import recortar
from instagram.recorte.verificar import laudo_preservacao


def _quadrado_em_fundo_claro():
    """Objeto escuro 40x40 centrado num fundo claro 100x100."""
    img = np.full((100, 100, 3), 235, dtype=np.uint8)
    img[30:70, 30:70] = (60, 45, 30)
    return img


def test_recorte_devolve_rgba_do_mesmo_tamanho():
    img = _quadrado_em_fundo_claro()
    rgba = recortar(img)
    assert rgba.shape == (100, 100, 4)
    assert rgba.dtype == np.uint8


def test_interior_do_objeto_fica_totalmente_opaco():
    rgba = recortar(_quadrado_em_fundo_claro())
    assert rgba[50, 50, 3] == 255


def test_canto_do_fundo_fica_totalmente_transparente():
    rgba = recortar(_quadrado_em_fundo_claro())
    assert rgba[0, 0, 3] == 0


def test_recorte_nao_altera_o_rgb_do_interior():
    img = _quadrado_em_fundo_claro()
    rgba = recortar(img)
    r = laudo_preservacao(img, rgba[:, :, :3], rgba[:, :, 3])
    assert r["aprovado"] is True, r
