# -*- coding: utf-8 -*-
"""Precificação de café na Amazon Brasil com o CMV real — calculadora do estudo de 10/2026.

CMV e imposto vêm de `mercadolivre/custos.md` (mesma fonte do ML). As tarifas da Amazon
AINDA NÃO FORAM MEDIDAS no Seller Central (a Canastra não vende lá): os padrões abaixo são
os números AFIRMADOS nos vídeos da pesquisa (`amazon/pesquisa/2026-10-estrategia/notas/`),
cada um com a fonte. Quando medir, troque aqui e anote a data.

    python amazon/scripts/precificar_amazon.py                  # tabela padrão
    python amazon/scripts/precificar_amazon.py --preco 119.90 --sku 1kg --canal fba
    python amazon/scripts/precificar_amazon.py --margem 20 --sku 250g --canal fba
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mercadolivre', 'scripts'))
from precificar import CMV as CMV_ML, IMPOSTO, resultado as resultado_ml  # noqa: E402

CMV = dict(CMV_ML, kit2kg=2 * CMV_ML['1kg'], kit4x250=4 * CMV_ML['250g'])

# ── AFIRMADO nos vídeos, não medido (ver notas/custos-precificacao.md e notas/fba.md) ──
COMISSAO = 0.10              # alimentos e bebidas 10% (0KERUmnBrf4); faixa geral 10–15% (l9MMfiAAWqo)
VANTAGENS = 0.015            # Programa Amazon Vantagens: 1,5% do preço em itens >= R$ 40 (H0ab_x1YIBY, oficial, 14/10/2026)
FBA_ACIMA_79 = 6.00          # tarifa fixa por unidade a partir de R$ 79,90 (Summit oficial PbfiOlFMXqc), campanha até 31/01/2027, exige 3,5% em Ads (bxI6hlj4Dmc, l9MMfiAAWqo, notas/fba.md)
FBA_30_79 = 5.85             # R$ 5,65–6,50 entre R$ 30 e R$ 78,99 (notas/fba.md); 5,85 citado para 250 g
ADS_EXIGIDO_CAMPANHA = 0.035 # investimento em Ads exigido pela tarifa fixa
DBA_1KG_SUPOSTO = 17.45      # único valor legível de DBA (2–3 kg); usado como teto pessimista para 1 kg
FBA_POS_CAMPANHA_SUPOSTO = 15.00  # tabela por peso sem campanha não foi lida; cenário de estresse


def tarifa_logistica(preco, canal, sku):
    if canal == 'fba':
        return FBA_ACIMA_79 if preco >= 79.90 else FBA_30_79
    if canal == 'fba_pos':
        return FBA_POS_CAMPANHA_SUPOSTO if preco >= 79.90 else FBA_30_79
    if canal == 'dba':
        return DBA_1KG_SUPOSTO if sku in ('1kg', 'kit2kg', 'kit4x250') else 6.50
    raise ValueError(canal)


def resultado(preco, sku, canal='fba', comissao=COMISSAO, ads=None):
    """Margem de contribuição por venda. `ads` = TACOS; padrão: 3,5% quando a tarifa fixa do FBA exige."""
    if ads is None:
        ads = ADS_EXIGIDO_CAMPANHA if canal == "fba" and preco >= 79.90 else 0.0
    com = preco * comissao
    van = preco * VANTAGENS if preco >= 40 else 0.0
    log = tarifa_logistica(preco, canal, sku)
    imp = preco * IMPOSTO
    ad = preco * ads
    mc = preco - com - van - log - imp - ad - CMV[sku]
    return dict(preco=preco, sku=sku, canal=canal, comissao=round(com, 2), vantagens=round(van, 2),
                logistica=log, imposto=round(imp, 2), ads=round(ad, 2), cmv=CMV[sku],
                mc=round(mc, 2), margem=round(mc / preco * 100, 1))


def preco_para_margem(m, sku, canal='fba', comissao=COMISSAO):
    """Busca o menor preço (passo de R$ 0,10) que entrega margem m% — a tarifa muda de faixa em R$ 79."""
    p = 10.0
    while p < 1000:
        if resultado(round(p, 2), sku, canal, comissao)['margem'] >= m:
            return round(p, 2)
        p += 0.10
    return None


def tabela():
    print('| SKU | preço | canal | comissão | Vantagens | logística | imposto | Ads | CMV | **MC** | margem |')
    print('|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|')
    casos = [('1kg', p) for p in (109.90, 119.90, 129.90)] + [('250g', p) for p in (39.90, 44.90, 48.70)] + \
            [('500g', 69.90), ('kit2kg', 219.80), ('kit4x250', 159.90)]
    for sku, p in casos:
        for canal in ('fba', 'fba_pos', 'dba'):
            r = resultado(p, sku, canal)
            print('| %s | %.2f | %s | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f | **%.2f** | %.1f%% |' % (
                sku, p, canal, r['comissao'], r['vantagens'], r['logistica'], r['imposto'], r['ads'], r['cmv'], r['mc'], r['margem']))
    ml = resultado_ml(109.90, CMV_ML['1kg'], 34.30)
    print('\nReferência ML: 1 kg a R$ 109,90 deixa R$ %.2f (%.1f%%).' % (ml['lucro'], ml['margem']))
    print('\nPreço para 20%% de margem (FBA com campanha): 1 kg R$ %s · 250 g R$ %s · kit 2 kg R$ %s' % (
        preco_para_margem(20, '1kg'), preco_para_margem(20, '250g'), preco_para_margem(20, 'kit2kg')))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--preco', type=float)
    ap.add_argument('--margem', type=float)
    ap.add_argument('--sku', choices=CMV, default='1kg')
    ap.add_argument('--canal', choices=('fba', 'fba_pos', 'dba'), default='fba')
    ap.add_argument('--comissao', type=float, default=COMISSAO * 100, help='%')
    a = ap.parse_args(argv)
    if a.preco is not None:
        print(resultado(a.preco, a.sku, a.canal, a.comissao / 100))
    elif a.margem is not None:
        print(preco_para_margem(a.margem, a.sku, a.canal, a.comissao / 100))
    else:
        tabela()


if __name__ == '__main__':
    main()
