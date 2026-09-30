"""Laudo automatico: o recorte alterou algum pixel do objeto?

A pergunta nao se responde no olho. Se responde comparando o RGB original
com o de saida EXATAMENTE onde o alfa e 255 -- ou seja, so onde o pixel e
totalmente opaco e, portanto, tem que ter sobrevivido intacto.

Por que isso e um portao e nao um relatorio: alfa 253 no miolo de uma letra
e invisivel na conferencia visual, mas muda a cor real quando o recorte e
composto sobre um fundo novo. E o `Doodo 1985` do CLAUDE.md outra vez, em
opacidade em vez de forma. Plano:
docs/superpowers/plans/2026-09-30-assets-recorte-e-geracao.md
"""

from __future__ import annotations

import numpy as np


def laudo_preservacao(rgb_origem: np.ndarray, rgb_saida: np.ndarray,
                      alfa: np.ndarray, tolerancia: int = 0,
                      retangulo_rotulo: tuple | None = None) -> dict:
    """Compara origem e saida onde `alfa == 255` e devolve o laudo.

    `tolerancia` e o delta maximo por canal que ainda conta como preservado;
    o padrao 0 exige igualdade exata. `retangulo_rotulo` e `(x0, y0, x1, y1)`
    em coordenadas de pixel: dentro dele, qualquer alfa abaixo de 255 reprova,
    porque tipografia impressa nao admite transparencia parcial.
    """
    opaco = alfa == 255
    a = rgb_origem[opaco].astype(np.int16)
    b = rgb_saida[opaco].astype(np.int16)
    delta = np.abs(a - b).max(axis=1) if a.size else np.zeros(0, dtype=np.int16)

    alterados = int((delta > tolerancia).sum())
    maior = int(delta.max()) if delta.size else 0

    alfa_min_rotulo = None
    if retangulo_rotulo is not None:
        x0, y0, x1, y1 = retangulo_rotulo
        alfa_min_rotulo = int(alfa[y0:y1, x0:x1].min())

    # `pixels_alterados` e `maior_delta` sao TAUTOLOGICOS no fluxo de hoje, e
    # e preciso saber disso para nao confiar neles: `matte.recortar` devolve o
    # RGB de ENTRADA sem tocar em nada, entao comparar entrada com saida da 0
    # por construcao, sempre, inclusive num recorte que pegou a parede junto.
    # Foi assim que um dos 3 SKUs saiu `aprovado=true` em 30/09/2026 carregando
    # um naco de parede clara.
    #
    # Os campos ficam: eles sao o alarme para o dia em que alguem trocar o RGB
    # de saida por `estimate_foreground` -- ai deixam de dar 0 e o portao passa
    # a valer. Mas quem DISCRIMINA recorte bom de recorte ruim aqui e
    # `alfa_minimo_no_rotulo` (tipografia impressa nao admite transparencia
    # parcial) e, antes disso, o portao geometrico de
    # `trimap.PremissaDeRecorteViolada` -- fotometria nenhuma pega parede que
    # veio junto, porque a parede tambem e pixel intacto da origem.
    aprovado = (alterados == 0) and (
        alfa_min_rotulo is None or alfa_min_rotulo == 255
    )
    return {
        "pixels_alterados": alterados,
        "maior_delta": maior,
        "pixels_opacos": int(opaco.sum()),
        "alfa_minimo_no_rotulo": alfa_min_rotulo,
        "aprovado": aprovado,
    }
