# -*- coding: utf-8 -*-
"""Precificação na Shopee com o CMV real — par do `mercadolivre/scripts/precificar.py`.

Tabela de comissão a partir de 01/10/2026: AFIRMADA em 6 vídeos (hEkVpRw_vNg, 9VOoazXt_aE,
IYi2eifHqSY, M37L89O1dng, jZeOeA6yA20, 7Q1J56HVVbw), NÃO medida num pedido da Canastra.
Frete do vendedor: 0 por padrão (os vídeos dizem que a Shopee banca o frete grátis); o
"programa de frete grátis extra" é ambíguo — use --frete para simular. Meça num extrato real
e corrija aqui.

    python shopee/scripts/precificar_shopee.py              # tabela dos SKUs, pisos e zonas mortas
    python shopee/scripts/precificar_shopee.py --preco 109.90 --cmv 47
    python shopee/scripts/precificar_shopee.py --margem 15 --cmv 47
"""
import argparse
import os
import sys

IMPOSTO = 0.09   # sobre o preço de venda (mercadolivre/custos.md)
CMV = {'1kg': 47.00, '500g': 26.00, '250g': 14.00, 'capsula10': 15.10}

# (preço mínimo da faixa, comissão %, taxa fixa por item) — regra de 01/10/2026
FAIXAS = [(0.00, 0.20, 4.50), (80.00, 0.14, 16.00), (100.00, 0.14, 20.00), (200.00, 0.14, 26.00)]


def faixa(preco):
    for minimo, pct, fixa in reversed(FAIXAS):
        if preco >= minimo:
            return pct, fixa
    raise ValueError(preco)


def resultado(preco, cmv, frete=0.0, ads_pct=0.0):
    pct, fixa = faixa(preco)
    comissao = round(preco * pct, 2)
    imposto = round(preco * IMPOSTO, 2)
    lucro = round(preco - comissao - fixa - frete - imposto - cmv - preco * ads_pct, 2)
    return dict(preco=preco, comissao=comissao, fixa=fixa, frete=frete, imposto=imposto, cmv=cmv,
                lucro=lucro, margem=round(lucro / preco * 100, 1))


def preco_para_margem(margem_pct, cmv, frete=0.0):
    """Menor preço com a margem pedida, conferindo a faixa (a taxa fixa muda de degrau)."""
    for minimo, pct, fixa in FAIXAS:
        p = (cmv + fixa + frete) / (1 - pct - IMPOSTO - margem_pct / 100)
        if p >= minimo and faixa(p) == (pct, fixa):
            return round(p, 2)
    return None


def zonas_mortas(cmv, frete=0.0):
    """Faixas onde cobrar mais deixa menos: logo acima de cada degrau da taxa fixa."""
    out = []
    for i in range(1, len(FAIXAS)):
        degrau = FAIXAS[i][0]
        antes = resultado(round(degrau - 0.01, 2), cmv, frete)['lucro']
        p = degrau
        while resultado(round(p, 2), cmv, frete)['lucro'] < antes:
            p += 0.01
        out.append((degrau, round(p, 2), antes))
    return out


def tabela():
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mercadolivre', 'scripts'))
    try:
        import precificar as ml
    except ImportError:
        ml = None
    skus = [('1 kg', CMV['1kg'], (99.90, 109.90, 119.90, 129.90), 34.30),
            ('Kit 2 × 1 kg', 2 * CMV['1kg'], (199.90, 209.90, 219.80, 239.80), 54.10),
            ('Moído 500 g', CMV['500g'], (44.90, 49.90, 54.90, 59.90), None),
            ('Moído 250 g', CMV['250g'], (29.90, 34.90, 39.90), None),
            ('Cápsulas 10', CMV['capsula10'], (29.90, 34.90, 39.90), None),
            ('Cápsulas kit 40', 4 * CMV['capsula10'], (119.90, 139.90), None)]
    print('| SKU | preço | comissão | fixa | imposto | CMV | lucro Shopee | margem | lucro ML (frete medido) |')
    print('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
    for nome, cmv, precos, frete_ml in skus:
        for p in precos:
            r = resultado(p, cmv)
            l_ml = '—'
            if ml and frete_ml is not None:
                l_ml = '%.2f' % ml.resultado(p, cmv, frete_ml)['lucro']
            print('| %s | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f | %.1f%% | %s |' % (
                nome, p, r['comissao'], r['fixa'], r['imposto'], cmv, r['lucro'], r['margem'], l_ml))
    print('\nPisos (frete do vendedor = 0):')
    for nome, cmv, _, _ in skus:
        print('- %s: zero %s · 10%% %s · 15%% %s · 20%% %s' % (nome, *[
            preco_para_margem(m, cmv) for m in (0, 10, 15, 20)]))
    print('\nZonas mortas (de → até; lucro do degrau anterior) no 1 kg:')
    for d, ate, antes in zonas_mortas(CMV['1kg']):
        print('- R$ %.2f a %.2f rende menos que R$ %.2f (lucro %.2f)' % (d, ate, d - 0.01, antes))
    print('\nEstresse: frete pago pelo vendedor (hipótese) no 1 kg a R$ 109,90:')
    for f in (0, 10, 15, 20, 30):
        r = resultado(109.90, CMV['1kg'], f)
        print('- frete R$ %d: lucro %.2f (%.1f%%), ROAS de equilíbrio %s' % (
            f, r['lucro'], r['margem'], '%.1f' % (109.90 / r['lucro']) if r['lucro'] > 0 else '∞'))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--preco', type=float)
    ap.add_argument('--margem', type=float)
    ap.add_argument('--cmv', type=float, default=CMV['1kg'])
    ap.add_argument('--frete', type=float, default=0.0, help='R$ de frete pago pelo vendedor (hipótese)')
    a = ap.parse_args(argv)
    if a.preco is not None:
        print(resultado(a.preco, a.cmv, a.frete))
    elif a.margem is not None:
        print(preco_para_margem(a.margem, a.cmv, a.frete))
    else:
        tabela()
    return 0


if __name__ == '__main__':
    sys.exit(main())
