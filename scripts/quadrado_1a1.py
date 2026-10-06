# -*- coding: utf-8 -*-
"""Transforma um packshot 3:4 do catalogo em 1:1, para a grade do Mercado Livre.

Por que nao e so colar branco nas laterais: o ciclorama do catalogo nao e
`#FFFFFF` chapado - tem gradiente vertical e queda nos cantos. Uma tarja branca
ao lado criaria uma emenda visivel bem no meio da miniatura. A receita que
funciona (licao 23 do CLAUDE.md, usada antes na vitrine da Tray) e ESTICAR a
coluna da borda: `crop(x,0,x+1,H).resize(pad,H)` repete o gradiente daquela
coluna, entao a emenda nao existe.

Antes de esticar, o script PROVA que a borda esta vazia: se qualquer pixel de
conteudo (limiar 200 em luminancia) estiver a menos de `FOLGA` px da borda,
ele aborta - esticar uma coluna que contem produto esfrega o produto pela
lateral inteira.

    python scripts/quadrado_1a1.py <entrada.png> [<entrada.png> ...]

Saida: `<pasta>/1a1/<nome>.jpg`, quadrado, lado = altura da origem.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
LIMIAR = 200   # abaixo disso e conteudo; a sombra de contato fica por volta de 233
FOLGA = 24     # px de branco exigidos em cada borda antes de esticar


def medir_bordas(im: Image.Image) -> tuple[int, int]:
    a = np.asarray(im.convert("L")).astype(int)
    xs = np.where((a < LIMIAR).any(axis=0))[0]
    return int(xs.min()), int(xs.max())


def quadrar(origem: Path) -> Path:
    im = Image.open(origem).convert("RGB")
    w, h = im.size
    if w == h:
        raise SystemExit(f"{origem.name} ja e quadrada")
    if w > h:
        raise SystemExit(f"{origem.name} e paisagem; esta receita e para retrato")

    x0, x1 = medir_bordas(im)
    if x0 < FOLGA or (w - 1 - x1) < FOLGA:
        raise SystemExit(
            f"ABORTADO: {origem.name} tem conteudo a {x0}px da borda esquerda e "
            f"{w - 1 - x1}px da direita, menos que a folga de {FOLGA}px. Esticar a "
            "coluna da borda arrastaria o produto pela lateral."
        )

    falta = h - w
    esq, dir_ = falta // 2, falta - falta // 2
    folha = Image.new("RGB", (h, h), (255, 255, 255))
    folha.paste(im.crop((0, 0, 1, h)).resize((esq, h), Image.BILINEAR), (0, 0))
    folha.paste(im.crop((w - 1, 0, w, h)).resize((dir_, h), Image.BILINEAR), (esq + w, 0))
    folha.paste(im, (esq, 0))

    destino = origem.parent / "1a1" / (origem.stem + ".jpg")
    destino.parent.mkdir(parents=True, exist_ok=True)
    folha.save(destino, quality=94, subsampling=0)
    kb = destino.stat().st_size / 1024
    print(
        f"{origem.name} {w}x{h}  conteudo x{x0}-{x1}  ->  "
        f"{destino.relative_to(RAIZ)}  {folha.size[0]}x{folha.size[1]}  {kb:.0f} KB"
    )
    return destino


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    for arg in sys.argv[1:]:
        quadrar(Path(arg).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
