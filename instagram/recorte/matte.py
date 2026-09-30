"""Matting classico com pymatting.

Importante: o RGB de saida e o RGB ORIGINAL, nao o primeiro plano estimado.
Estimar primeiro plano muda a cor do interior, e o requisito aqui e preservar
pixel. O alfa resolve a borda; o miolo fica intacto.

As duas linhas que travam `tri == 0.0` e `tri == 1.0` garantem que o solver so
decida na faixa desconhecida: alfa 254 no miolo de uma letra e invisivel na
conferencia visual, mas muda a cor real ao compor sobre fundo novo.

Medido em 30/09/2026 nos dois fixtures deste repo (quadrado uniforme e
packshot com gradiente + ruido + rotulo texturizado): o `estimate_alpha_cf`
ja devolveu exatamente 0 e 255 nas regioes conhecidas, ou seja o travamento
foi no-op nos dois. Ele fica porque converter "convergiu para 0/1" em "e 0/1"
custa duas linhas -- o arredondamento a uint8 perdoa erro de so 0,002, e
nenhum teste aqui prova que o solver sempre cabe nessa margem. Nao e conserto
observado, e garantia por construcao.

Plano: docs/superpowers/plans/2026-09-30-assets-recorte-e-geracao.md
"""

from __future__ import annotations

import numpy as np
from pymatting import estimate_alpha_cf
from pymatting.preconditioner.ichol import ichol

from .trimap import gerar_trimap_detalhado

# Teto do proprio pymatting; nunca pedimos mais memoria que o default dele.
_MAX_NNZ_PYMATTING = 250_000_000


def _precondicionador(A):
    """`ichol` com `max_nnz` dimensionado ao problema, nao fixo.

    O default do pymatting e `max_nnz=250_000_000` **independente do tamanho da
    imagem**, e o `ichol` faz `np.empty(max_nnz)` em float64 *e* em int64: 3,7 GiB
    de alocacao para recortar um quadrado de 100x100. Com varios processos na
    mesma maquina isso vira `_ArrayMemoryError` intermitente -- medido aqui em
    30/09/2026, 1 falha em 5 execucoes do mesmo teste.

    Medido nesta base: o laplaciano de closed-form tem 25 nao-zeros por pixel e
    o `ichol` consumiu 0,81 x `nnz(A)`, logo folga 4x sobra. Com o teto acima a
    conta nunca fica pior que o default para imagem grande, e o alfa uint8 sai
    **identico** ao do default (medido: diferenca maxima 0).

    Mas 4x **nao** e universal: medido em 30/09/2026, o packshot Canela de
    4096x2304 estourou a folga de 4x e o `ichol` levantou `ValueError`. Os dois
    fixtures em que o 4x foi medido sao pequenos e de borda curta; a faixa
    desconhecida de uma foto real e muito maior, e o enchimento do ichol cresce
    com ela. Por isso a folga agora **cresce** ate o teto do proprio pymatting
    em vez de desistir: economizar memoria nao pode custar um recorte que o
    default da biblioteca faria. Se nem o teto bastar, a `ValueError` sobe --
    falha alta, nao silenciosa, e nunca um alfa pela metade.
    """
    folga = min(_MAX_NNZ_PYMATTING, max(2_000_000, A.nnz * 4))
    while True:
        try:
            return ichol(A, max_nnz=folga)
        except ValueError:
            if folga >= _MAX_NNZ_PYMATTING:
                raise
            folga = min(_MAX_NNZ_PYMATTING, folga * 4)


def recortar(img_rgb: np.ndarray, banda: int = 6,
             modo: str = "auto") -> np.ndarray:
    """Devolve RGBA uint8 do mesmo tamanho, com o RGB de entrada preservado.

    `banda` e a largura em pixels da faixa de incerteza do trimap -- a unica
    regiao em que o solver tem permissao de decidir. `modo` e o metodo de
    trimap; ver `instagram.recorte.trimap.MODOS`.
    """
    return recortar_detalhado(img_rgb, banda=banda, modo=modo)[0]


def recortar_detalhado(img_rgb: np.ndarray, banda: int = 6,
                       modo: str = "auto") -> tuple[np.ndarray, dict]:
    """Mesmo recorte, mais o diagnostico de qual modo de trimap rodou.

    Levanta `trimap.PremissaDeRecorteViolada` quando a foto nao satisfaz a
    premissa de nenhum modo -- e melhor nao ter PNG do que ter PNG com parede.
    """
    tri, diag = gerar_trimap_detalhado(img_rgb, banda=banda, modo=modo)
    img_f = img_rgb.astype(np.float64) / 255.0
    alfa = estimate_alpha_cf(img_f, tri.astype(np.float64),
                             preconditioner=_precondicionador)

    # trava as regioes certas: o solver so decide na faixa desconhecida
    alfa = np.clip(alfa, 0.0, 1.0)
    alfa[tri == 0.0] = 0.0
    alfa[tri == 1.0] = 1.0

    rgba = np.dstack([img_rgb, (alfa * 255.0).round().astype(np.uint8)])
    return rgba, diag
