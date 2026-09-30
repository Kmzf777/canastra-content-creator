# -*- coding: utf-8 -*-
"""Plano de escala: caminho ate Produto Estrela, cobertura de estoque e freio de preco.

Fontes (canal, data, id em docs/pesquisa-ml/ACHADOS.md):
  Estrela .... Vendedores Mercado Livre Brasil 10/08 (qPVIEY_Fg_E):
               "mais vendidos na sua categoria nos ultimos 60 dias dentro de Full";
               nao impactam metricas de excedente NEM de estoque antigo; ML distribui
               entre CDs; pode dar bonificacao por estoque antigo.
  Teto Full .. Milewa 25/08 (7h4R4KPK9bw): 100 un paradas = R$21/mes no 1o, R$121 no 5o,
               R$1.221 no 7o. "Mande so o que vende antes dos 4 meses; use as vendas
               dos ultimos 30 dias como medida."
  Ruptura .... Milton P Rabello 27/08 (swCx36qRg0w): "cada 1 dia de anuncio pausado,
               voce perde 2 dias de ranqueamento". Antes de faltar, SUBA O PRECO.
"""
CPV = 15.10
CAP_CAIXAS = 1000          # 10.000 capsulas = 1.000 caixas de 10 (meio da faixa informada)

# produtos, em caixas de 10 por unidade vendida
PROD = {
    'caixa10': dict(caixas=1, preco=34.90, promo=28.90, lucro=12.82, lucro_promo=8.02),
    'kit40':   dict(caixas=4, preco=139.90, promo=124.90, lucro=39.91, lucro_promo=27.01),
}
MIX = {'caixa10': 0.55, 'kit40': 0.45}   # vendas, nao caixas


def por_venda(promo=0.6):
    """Caixas consumidas, faturamento e lucro por VENDA media do mix."""
    cx = fat = luc = 0.0
    for k, w in MIX.items():
        p = PROD[k]
        cx += w * p['caixas']
        fat += w * (promo * p['promo'] + (1 - promo) * p['preco'])
        luc += w * (promo * p['lucro_promo'] + (1 - promo) * p['lucro'])
    return cx, fat, luc


CX, FAT, LUC = por_venda()
print('Por venda media do mix (55%% caixa / 45%% kit, 60%% em promo):')
print('  consome %.2f caixas | fatura R$ %.2f | lucro R$ %.2f' % (CX, FAT, LUC))
print('  capacidade de %d caixas = %.0f vendas possiveis' % (CAP_CAIXAS, CAP_CAIXAS / CX))

print('\n=== COBERTURA: quantos meses o estoque dura em cada ritmo ===')
print('%10s %12s %14s %14s' % ('vendas/mes', 'caixas/mes', 'meses de estoque', 'veredito'))
for v in (10, 20, 35, 60, 100, 150):
    cxm = v * CX
    meses = CAP_CAIXAS / cxm
    if meses > 4:
        vd = 'estoque demais p/ enviar tudo'
    elif meses >= 2:
        vd = 'saudavel'
    else:
        vd = 'risco de ruptura'
    print('%10d %12.0f %14.1f  %s' % (v, cxm, meses, vd))

print('\n=== QUANTO ENVIAR AO FULL — regra do "vende antes de N meses" ===')
print('Supermercado cobra estoque antigo a partir de 2 MESES. Sem Estrela, esse e o teto.')
print('%10s %16s %16s %16s' % ('vendas/mes', 'envio 2 meses', 'envio 4 meses', 'sobra em casa (2m)'))
for v in (20, 35, 60, 100):
    e2, e4 = v * CX * 2, v * CX * 4
    print('%10d %16.0f %16.0f %16.0f' % (v, e2, e4, CAP_CAIXAS - e2))

print('\n=== CUSTO DE ERRAR PARA CIMA (estoque parado no Full) ===')
print('Escala medida: 100 un paradas custam R$21 no 1o mes, R$121 no 5o, R$1.221 no 7o.')
for un in (100, 300, 600):
    print('  %3d un paradas -> mes 1: R$%6.0f | mes 5: R$%7.0f | mes 7: R$%8.0f' % (
        un, 21 * un / 100, 121 * un / 100, 1221 * un / 100))
print('  -> e exatamente isso que o status ESTRELA desliga.')

print('\n=== CAMINHO ATE O ESTRELA ===')
print('Estrela = estar entre os mais vendidos da categoria no Full, janela de 60 dias.')
print('Referencia medida dos concorrentes de cafe ESPECIAL (selo acumulado):')
print('  Coffee++ +25 | "Serra Canastra" +5 | Orfeu Arara 10un +100')
print('Logo, o patamar de "mais vendido do especial" e da ordem de dezenas em 60 dias.')
print()
for alvo in (40, 60, 80, 120):
    mes = alvo / 2
    cx_nec = alvo * CX
    ads_6 = alvo / 2 * FAT * 0.06
    print('  alvo %3d vendas em 60 dias (%4.0f/mes) -> %4.0f caixas | fatura R$%8.0f/mes | Ads a 6%% = R$%6.0f/mes'
          % (alvo, mes, cx_nec, mes * FAT, ads_6))

print('\n=== ADS ACIMA DO ESTOQUE: ate onde da para forcar ===')
print('Teto absoluto: o Ads nao pode passar do lucro bruto do volume que ele traz.')
print('%12s %13s %14s %15s %14s' % ('vendas/mes', 'lucro bruto', 'Ads no limite', 'Ads a 50% dele', 'por dia'))
for v in (20, 35, 60, 100, 150):
    bruto = v * LUC
    print('%12d %13.0f %14.0f %15.0f %14.2f' % (v, bruto, bruto, bruto * 0.5, bruto * 0.5 / 30))

print('\n=== FREIO DE PRECO (tecnica do Milton) ===')
print('Se o Ads vender mais rapido que a reposicao, SOBE O PRECO em vez de pausar.')
print('Custo de pausar: 1 dia pausado = 2 dias de ranqueamento perdidos.')
print('%10s %12s %12s %12s' % ('preco cx', 'lucro', 'margem', 'efeito'))
for p in (34.90, 37.90, 39.90, 42.90):
    l = p - p * 0.14 - p * 0.06 - CPV
    print('%10.2f %12.2f %11.1f%%  %s' % (
        p, l, l / p * 100,
        'preco base' if p == 34.90 else 'freio leve' if p < 40 else 'freio forte'))
