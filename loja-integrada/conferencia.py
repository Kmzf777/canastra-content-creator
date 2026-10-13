# -*- coding: utf-8 -*-
"""Monta uma folha de conferência por produto: packshot gerado x foto real.

Rode a partir do diretório principal do repositório (as pastas pesadas são
gitignored e só existem lá):

    .venv/Scripts/python.exe loja-integrada/conferencia.py
"""
import os, sys, glob
from PIL import Image, ImageOps, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogo import PRODUTOS

GERADO = "saida-teste/catalogo-estudio"
REAL = "fotos produtos cru"
SAIDA = "saida-teste/_li-conferencia"
ALTURA = 1100


def abre(caminho):
    return ImageOps.exif_transpose(Image.open(caminho)).convert("RGB")


def escala(im, altura):
    return im.resize((max(1, round(im.width * altura / im.height)), altura), Image.LANCZOS)


def main():
    os.makedirs(SAIDA, exist_ok=True)
    faltando = []
    for sku, tray, pasta_g, pasta_r, _cat, _fmt, _ean in PRODUTOS:
        n = pasta_g.split("-")[0]
        g = os.path.join(GERADO, pasta_g, f"{n}.1-frente-branco.png")
        reais = sorted(glob.glob(os.path.join(REAL, pasta_r, "*frente*.jpg")))
        if not os.path.exists(g) or not reais:
            faltando.append((sku, os.path.exists(g), len(reais)))
            continue
        im_g = escala(abre(g), ALTURA)
        # a melhor foto real costuma ser a primeira frente do shoot
        im_r = escala(abre(reais[0]), ALTURA)
        # zoom da faixa de texto do gerado: metade de baixo, 1,6x
        faixa = abre(g)
        faixa = faixa.crop((0, int(faixa.height * 0.52), faixa.width, faixa.height))
        faixa = faixa.resize((round(faixa.width * 1.6), round(faixa.height * 1.6)), Image.LANCZOS)

        larg = im_g.width + im_r.width + 24
        larg = max(larg, faixa.width)
        folha = Image.new("RGB", (larg, ALTURA + faixa.height + 36), "white")
        folha.paste(im_g, (0, 0))
        folha.paste(im_r, (im_g.width + 24, 0))
        folha.paste(faixa, (0, ALTURA + 36))
        d = ImageDraw.Draw(folha)
        d.text((8, ALTURA + 8), f"{sku}  |  esquerda GERADO {n}.1  |  direita REAL {os.path.basename(reais[0])}", fill="black")
        destino = os.path.join(SAIDA, f"{sku}.jpg")
        folha.save(destino, quality=88)
        print(f"{sku:<16} {folha.size} <- {os.path.basename(reais[0])}")
    for f in faltando:
        print("FALTANDO:", f)
    return 1 if faltando else 0


if __name__ == "__main__":
    sys.exit(main())
