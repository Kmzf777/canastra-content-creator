"""Produz o material da conferencia. Nao emite veredito -- quem le e o agente.

POR QUE SO OS RECORTES. O que falha hoje nao e a leitura, e a oportunidade de
ler: em miniatura, erro de letra desaparece. `canastra-conteudo` fase 4 manda
recortar a faixa de texto e ampliar com LANCZOS antes de opinar, e manda
ampliar A REFERENCIA TAMBEM -- conferencia e comparacao entre dois recortes,
nunca entre um recorte e a memoria de quem olha.

Este modulo automatiza exatamente essa mecanica, e nada alem dela. Decidir se
`SCA 80+` saiu certo continua sendo trabalho de olho.
"""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

VEREDITOS: tuple[str, ...] = ("ok", "errado", "nao-verificavel")

FATOR_PADRAO = 4


def _slug(s: str) -> str:
    """`SCA 80+` -> `sca-80`. Windows nao aceita todo simbolo em nome de arquivo."""
    limpo = re.sub(r"[^0-9a-zA-Z]+", "-", s).strip("-").lower()
    return limpo or "campo"


def recortes(
    gerada: Path,
    referencia: Path,
    faixas: dict[str, tuple[int, int, int, int]],
    destino: Path,
    fator: int = FATOR_PADRAO,
) -> dict[str, tuple[Path, Path]]:
    """Para cada string, grava o recorte ampliado da gerada E da referencia.

    `faixas` mapeia a string declarada para `(x0, y0, x1, y1)`. Devolve
    `{string: (caminho_gerada, caminho_referencia)}`.
    """
    destino.mkdir(parents=True, exist_ok=True)
    saida: dict[str, tuple[Path, Path]] = {}

    with Image.open(gerada) as g, Image.open(referencia) as r:
        for nome, caixa in faixas.items():
            x0, y0, x1, y1 = caixa
            for rotulo, im in (("gerada", g), ("referencia", r)):
                if x1 > im.width or y1 > im.height or x0 < 0 or y0 < 0:
                    raise ValueError(
                        f"faixa de '{nome}' {caixa} cai fora da {rotulo} "
                        f"({im.width}x{im.height})"
                    )

            par = []
            for rotulo, im in (("gerada", g), ("referencia", r)):
                c = im.crop(caixa)
                c = c.resize(
                    (c.width * fator, c.height * fator), Image.Resampling.LANCZOS
                )
                p = destino / f"{_slug(nome)}-{rotulo}.png"
                c.save(p)
                par.append(p)
            saida[nome] = (par[0], par[1])

    return saida


def bloqueia(vereditos: dict[str, str]) -> tuple[str, ...]:
    """Quais campos barram a peca. `nao-verificavel` barra junto com `errado`.

    Isto e a licao 18 virada em codigo: um agente aprovou campo fisicamente
    ilegivel dizendo que "bate com a foto real". Ilegivel nao e aprovacao, e
    ausencia de leitura -- entao nao pode sair pela mesma porta que `ok`.
    """
    for campo, v in vereditos.items():
        if v not in VEREDITOS:
            raise ValueError(
                f"veredito '{v}' no campo '{campo}' nao existe. "
                f"Validos: {', '.join(VEREDITOS)}. "
                "Em particular 'confere' nao e veredito: use 'ok'."
            )
    return tuple(sorted(c for c, v in vereditos.items() if v != "ok"))
