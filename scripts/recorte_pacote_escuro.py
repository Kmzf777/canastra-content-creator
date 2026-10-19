"""Recorta um pacote ESCURO fotografado sobre fundo claro e o põe sobre branco.

Composição local de pixel real (fluxo 3 do CLAUDE.md): nada é gerado, o rótulo
é o da foto. Feito para os sacos pretos de 1 kg do shoot de 11/09/2026, onde o
pacote é preto fosco e o fundo é parede branca + mesa bege.

Método: máscara por luminância dentro de uma caixa que contém o pacote; em cada
linha, preenche do primeiro ao último pixel escuro (o saco é convexo por linha,
então o texto branco do rótulo fica dentro). Depois fecha a borda e suaviza 1 px.

    python scripts/recorte_pacote_escuro.py ENTRADA SAIDA --caixa x0 y0 x1 y1 [--limiar 105] [--fracao 0.5]

A caixa é em pixels da imagem já orientada pelo EXIF.
"""
import argparse

import numpy as np
from PIL import Image, ImageFilter, ImageOps


def recorta(entrada, saida, caixa, limiar, fracao=0.0, tol=12, reto=False, neutro=0, kraft=0, ajuste_ate=0, ajuste_de=0, margem=0.08, lado=2000):
    im = ImageOps.exif_transpose(Image.open(entrada)).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2])
    x0, y0, x1, y1 = caixa
    escuro = np.zeros(lum.shape, bool)
    escuro[y0:y1, x0:x1] = lum[y0:y1, x0:x1] < limiar
    if kraft:
        # saco kraft (claro) contra parede azulada: o critério é cor, não brilho
        escuro[:] = False
        escuro[y0:y1, x0:x1] = (a[y0:y1, x0:x1, 0] - a[y0:y1, x0:x1, 2]) > kraft
    if neutro:
        # a mesa/sombra é marrom (R bem acima de B); o saco preto é neutro
        escuro &= (a[..., 0] - a[..., 2]) < neutro

    # bordas por linha; linha só vale se o vão entre elas for majoritariamente
    # escuro (o sulco da mesa e a lasca de sombra são escuros mas esparsos)
    esq = np.full(lum.shape[0], -1)
    dir_ = np.full(lum.shape[0], -1)
    for y in range(y0, y1):
        xs = np.flatnonzero(escuro[y, x0:x1])
        if xs.size > 20 and xs.size / (xs[-1] - xs[0] + 1) >= fracao:
            esq[y], dir_[y] = x0 + xs[0], x0 + xs[-1]
    # linha de brilho descartada no MEIO do saco vira buraco: interpola as bordas
    # entre a última e a próxima linha válida (buracos de até 120 linhas)
    ys = np.flatnonzero(esq >= 0)
    for a_, b_ in zip(ys[:-1], ys[1:]):
        if 1 < b_ - a_ <= 120:
            for y in range(a_ + 1, b_):
                f = (y - a_) / (b_ - a_)
                esq[y] = round(esq[a_] + f * (esq[b_] - esq[a_]))
                dir_[y] = round(dir_[a_] + f * (dir_[b_] - dir_[a_]))
    ys = np.flatnonzero(esq >= 0)
    if reto:
        # foto frontal: lados do saco são retas. Ajuste robusto (2 passadas,
        # descarta o que se afasta > 8 px da 1ª reta) e preenche entre elas
        # ajuste_ate: só as linhas acima desse y entram no ajuste (abaixo, a mesa tem a cor do saco)
        ya = ys[ys < ajuste_ate] if ajuste_ate else ys
        ya = ya[ya >= ajuste_de]
        def reta(v):
            c = np.polyfit(ya, v[ya], 1)
            ok = np.abs(np.polyval(c, ya) - v[ya]) < 8
            return np.polyfit(ya[ok], v[ya][ok], 1)
        ce, cd = reta(esq), reta(dir_)
        mask = np.zeros_like(escuro)
        for y in range(ys[0], (y1 if ajuste_ate else ys[-1] + 1)):
            mask[y, int(np.polyval(ce, y)):int(np.polyval(cd, y)) + 1] = True
        if kraft:
            # topo ondulado: em cada coluna, nada acima do primeiro pixel do saco
            for x in range(x0, x1):
                col = np.flatnonzero(escuro[y0:y1, x])
                topo = y0 + col[0] if col.size else y1
                mask[:topo, x] = False
        ys = np.array([], int)
    else:
        mask = np.zeros_like(escuro)
    # borda presa à mediana de ±40 linhas: some a lasca isolada de uma linha
    for y in ys:
        viz = ys[(ys >= y - 40) & (ys <= y + 40)]
        me, md = np.median(esq[viz]), np.median(dir_[viz])
        l = int(max(esq[y], me - tol))
        r = int(min(dir_[y], md + tol))
        if r > l:
            mask[y, l:r + 1] = True

    m = Image.fromarray((mask * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))  # fecha
    m = m.filter(ImageFilter.GaussianBlur(1.2))

    bb = m.getbbox()
    corte = im.crop(bb)
    mc = m.crop(bb)
    w, h = corte.size
    alt = int(lado * (1 - 2 * margem))
    esc = alt / h
    corte = corte.resize((int(w * esc), alt), Image.LANCZOS)
    mc = mc.resize(corte.size, Image.LANCZOS)
    larg = int(lado * 0.75)  # quadro 3:4, igual ao catálogo
    tela = Image.new('RGB', (larg, lado), 'white')
    tela.paste(corte, ((larg - corte.width) // 2, (lado - corte.height) // 2), mc)
    tela.save(saida, quality=95)
    return bb, tela.size


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('entrada')
    p.add_argument('saida')
    p.add_argument('--caixa', type=int, nargs=4, required=True)
    p.add_argument('--limiar', type=int, default=105)
    p.add_argument('--fracao', type=float, default=0.0,
                   help='fração mínima de pixels escuros na linha (0 desliga; 0.5 tira sulco de mesa, mas também tira linha com brilho)')
    p.add_argument('--tol', type=int, default=12, help='px que a borda pode sair da mediana das linhas vizinhas')
    p.add_argument('--reto', action='store_true', help='foto frontal: ajusta retas aos lados do saco')
    p.add_argument('--neutro', type=int, default=0, help='descarta pixel com R-B >= N (sombra marrom de mesa); 0 desliga')
    p.add_argument('--kraft', type=int, default=0, help='saco claro: pixel do saco tem R-B > N (parede azulada fica fora)')
    p.add_argument('--ajuste-ate', dest='ajuste_ate', type=int, default=0, help='com --reto: ajusta as laterais só acima deste y e estende até o y1 da caixa')
    p.add_argument('--ajuste-de', dest='ajuste_de', type=int, default=0, help='com --reto: ignora no ajuste as linhas acima deste y (topo franzido)')
    a = p.parse_args()
    print(recorta(a.entrada, a.saida, a.caixa, a.limiar, a.fracao, a.tol, a.reto, a.neutro, a.kraft, a.ajuste_ate, a.ajuste_de))
