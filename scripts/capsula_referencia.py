# -*- coding: utf-8 -*-
"""Monta a referencia de capsula que vai anexada aos prompts 16.6-16.8 e 17.6-17.8.

Por que existe: a foto crua da capsula (`*-detalhe-*.jpg`, 3072x4096) e quase toda
mesa de madeira e parede - a capsula ocupa por volta de 3% da area. Anexada
inteira, ela nao serve de guidance: o modelo le melhor a mesa do que o produto.
Aqui cada SKU vira UMA imagem com as DUAS vistas reais lado a lado, em recorte
apertado: a capsula em pe (mostra a cupula e o corpo) e a capsula deitada (mostra
a tampa de aluminio e o flange).

Nada e gerado nem redesenhado - sao dois `crop` da foto original colados sobre
branco. A proveniencia continua sendo `fotos produtos cru/`.

    python scripts/capsula_referencia.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parent.parent
CRU = RAIZ / "fotos produtos cru"
DESTINO = RAIZ / "saida-teste" / "catalogo-estudio" / "_capsulas-recorte"

MARGEM = 40     # px de branco entre os dois recortes e nas bordas
ALTURA = 900    # altura de cada vista na imagem final

#: (slug, foto em pe, caixa, foto deitada, caixa). As caixas foram medidas
#: ampliando a foto crua 3x, nao estimadas no olho.
SETS = [
    (
        "classico",
        "Capsulas-Classico-10un-5g/capsulas-classico-detalhe-06.jpg", (1150, 2700, 1950, 3380),
        "Capsulas-Classico-10un-5g/capsulas-classico-detalhe-07.jpg", (1150, 2700, 2000, 3380),
    ),
    (
        "canela",
        "Capsulas-Canela-10un-5g/capsulas-canela-detalhe-07.jpg", (1150, 2680, 1950, 3330),
        "Capsulas-Canela-10un-5g/capsulas-canela-detalhe-08.jpg", (1150, 2800, 1800, 3350),
    ),
]


def recorte(rel: str, caixa: tuple[int, int, int, int]) -> Image.Image:
    im = ImageOps.exif_transpose(Image.open(CRU / rel)).convert("RGB").crop(caixa)
    escala = ALTURA / im.height
    return im.resize((round(im.width * escala), ALTURA), Image.LANCZOS)


def main() -> int:
    DESTINO.mkdir(parents=True, exist_ok=True)
    for slug, f_pe, c_pe, f_dt, c_dt in SETS:
        a, b = recorte(f_pe, c_pe), recorte(f_dt, c_dt)
        larg = MARGEM * 3 + a.width + b.width
        folha = Image.new("RGB", (larg, ALTURA + MARGEM * 2), (255, 255, 255))
        folha.paste(a, (MARGEM, MARGEM))
        folha.paste(b, (MARGEM * 2 + a.width, MARGEM))
        saida = DESTINO / f"capsula-{slug}-ref.jpg"
        folha.save(saida, quality=95)
        print(f"{saida.relative_to(RAIZ)}  {folha.size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
