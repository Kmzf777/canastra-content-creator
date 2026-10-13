# -*- coding: utf-8 -*-
"""Troca o selo errado do packshot do Microlote moído pelo selo real.

O packshot gerado 13.1 desenhou um selo que diz só "PARA / COADOR" em tinta
preta. O selo impresso de verdade diz "CAFÉ MOÍDO" no arco de cima e "PARA
COADOR" no de baixo, em tinta roxa, com dois grãos nas laterais — lido em
`fotos produtos cru/Microlote-250g-Moido/microlote-250g-moido-frente-03.jpg`.

Texto em arco não converge por prompt (lição 46): a correção é composição do
pixel real. Rode a partir do diretório principal do repositório.
"""
import os, sys
import numpy as np
from PIL import Image, ImageOps, ImageFilter

GERADO = "saida-teste/catalogo-estudio/13-microlote-250g-moido/13.1-frente-branco.png"
REAL = "fotos produtos cru/Microlote-250g-Moido/microlote-250g-moido-frente-03.jpg"
SAIDA = "saida-teste/_li-correcao/13.1-frente-branco-selo-real.png"

# medidos no pixel, não estimados
SELO_REAL = (1653, 1766, 1834, 1972)      # bbox do adesivo na foto real
CENTRO_G, DIAM_G = (730, 487), 114          # centro e diâmetro do selo no gerado


def disco(tamanho, suavidade=1.6):
    n = tamanho * 4
    m = Image.new("L", (n, n), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(m).ellipse((0, 0, n - 1, n - 1), fill=255)
    return m.resize((tamanho, tamanho), Image.LANCZOS).filter(ImageFilter.GaussianBlur(suavidade))


def main():
    g = Image.open(GERADO).convert("RGB")
    antes = np.asarray(g).astype(np.int16)

    r = ImageOps.exif_transpose(Image.open(REAL)).convert("RGB")
    selo = r.crop(SELO_REAL).resize((DIAM_G, DIAM_G), Image.LANCZOS)

    # casa o nível de branco: compara o anel claro de cada disco
    m = disco(DIAM_G, 0.6)
    mask_np = np.asarray(m) > 200
    cx, cy = CENTRO_G
    cai = (cx - DIAM_G // 2, cy - DIAM_G // 2)
    alvo = np.asarray(g.crop((cai[0], cai[1], cai[0] + DIAM_G, cai[1] + DIAM_G))).astype(float)
    fonte = np.asarray(selo).astype(float)
    # percentil 90 = o branco do adesivo nos dois
    p_alvo = np.percentile(alvo[mask_np], 90)
    p_fonte = np.percentile(fonte[mask_np], 90)
    ganho = p_alvo / p_fonte
    print(f"branco alvo {p_alvo:.1f} · fonte {p_fonte:.1f} · ganho {ganho:.3f}")
    selo = Image.fromarray(np.clip(fonte * ganho, 0, 255).astype(np.uint8))

    g.paste(selo, cai, disco(DIAM_G))

    depois = np.asarray(g).astype(np.int16)
    mudou = np.abs(depois - antes).max(axis=2) > 0
    fora = mudou.copy()
    fora[cai[1]:cai[1] + DIAM_G, cai[0]:cai[0] + DIAM_G] = False
    assert fora.sum() == 0, f"{fora.sum()} pixels alterados FORA da caixa do selo"
    print(f"pixels alterados dentro da caixa: {mudou.sum()} · fora: {fora.sum()}")

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    g.save(SAIDA)
    # recorte de conferência, 5x
    c = g.crop((cx - 90, cy - 90, cx + 90, cy + 90))
    c.resize((c.width * 5, c.height * 5), Image.LANCZOS).save("saida-teste/_li-correcao/_zoom-selo.jpg", quality=95)
    print("gravado", SAIDA)


if __name__ == "__main__":
    sys.exit(main())
