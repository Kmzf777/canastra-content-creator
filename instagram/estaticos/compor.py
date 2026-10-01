"""Degrau 6: cola o pixel real do rotulo e PROVA que ele chegou intacto.

ATENCAO AO LAUDO -- leia antes de mexer. `instagram/recorte/verificar.py`
documenta, em comentario proprio, que o `pixels_alterados` dele da 0 por
construcao no fluxo de recorte: `matte.recortar` devolve o RGB de entrada sem
tocar em nada, entao comparar entrada com saida nao pode acusar nada. Foi
assim que um SKU saiu `aprovado=true` carregando um naco de parede.

AQUI A COMPARACAO VALE, e vale por um motivo especifico: origem e o recorte
real JA REAMOSTRADO para o tamanho da caixa, e saida e a regiao correspondente
da peca final. Sao dois arrays de proveniencia diferente. Se alguem trocar a
origem pela propria peca, o laudo volta a ser teatro -- e o teste
`test_o_laudo_NAO_e_tautologico` existe para pegar exatamente isso.
"""

from __future__ import annotations

import numpy as np
from PIL import Image

from instagram.recorte.verificar import laudo_preservacao


def colar_rotulo(
    peca: Image.Image,
    recorte: Image.Image,
    caixa: tuple[int, int, int, int],
    _sabotar: bool = False,
) -> tuple[Image.Image, dict]:
    """Cola `recorte` (RGBA) em `caixa` da `peca` e devolve `(final, laudo)`.

    `_sabotar` corrompe a colagem de proposito e existe so para o teste que
    prova que o laudo nao e tautologico. Nunca use em producao.
    """
    x0, y0, x1, y1 = caixa
    if x0 < 0 or y0 < 0 or x1 > peca.width or y1 > peca.height:
        raise ValueError(
            f"caixa {caixa} cai fora da peca ({peca.width}x{peca.height})"
        )

    largura, altura = x1 - x0, y1 - y0
    origem_tamanho = list(recorte.size)

    fonte = recorte
    if fonte.size != (largura, altura):
        fonte = fonte.resize((largura, altura), Image.Resampling.LANCZOS)

    final = peca.convert("RGBA").copy()
    final.alpha_composite(fonte, dest=(x0, y0))

    if _sabotar:
        px = final.load()
        for i in range(x0, x1):
            for j in range(y0, y1):
                px[i, j] = (0, 0, 0, 255)

    # ORIGEM = o recorte reamostrado. SAIDA = a regiao da peca final.
    # Sao arrays distintos; o laudo tem o que comparar.
    rgb_origem = np.array(fonte.convert("RGB"))
    rgb_saida = np.array(final.crop(caixa).convert("RGB"))
    alfa = np.array(fonte.split()[-1])

    laudo = laudo_preservacao(
        rgb_origem,
        rgb_saida,
        alfa,
        tolerancia=0,
        retangulo_rotulo=(0, 0, largura, altura),
    )
    laudo["reamostrado"] = origem_tamanho + [largura, altura]
    return final, laudo
