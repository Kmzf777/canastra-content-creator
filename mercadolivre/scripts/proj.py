# -*- coding: utf-8 -*-
"""Projeções ancoradas em número observado, não em desejo.

Âncoras (todas medidas, nenhuma inventada):
  - Canastra hoje: 73 vendas em 365 dias = 6,1/mês, reputação VERMELHA,
    R$ 0 nos últimos 7 dias, 13 anúncios de cápsula fora do ar.
  - Concorrentes de cápsula ESPECIAL no ML, selo de vendas acumulado:
      Coffee++ Arara (Cafezale) ...... +25 vendidos
      "Serra Canastra" (terceiro) .... +5 vendas
      Orfeu Arara 10un (revenda) ..... +100 vendidos
    Esses selos são ACUMULADOS, não mensais. É um nicho de dezenas, não de milhares.
  - Genérico de volume (Café Italle 50un) leva o selo "MAIS VENDIDO" da categoria
    inteira — mas a R$ 1,48/cápsula, outro negócio.
"""

PROD = {
    'Caixa 10': dict(preco=34.90, lucro=12.40),
    'Kit 40':   dict(preco=139.90, lucro=39.01),
    'Kit 60':   dict(preco=199.90, lucro=48.41),
}
MIX = {'Caixa 10': 0.45, 'Kit 40': 0.40, 'Kit 60': 0.15}  # mais volume no baixo ticket

CENARIOS = {
    'Conservador': 18,
    'Realista': 35,
    'Agressivo': 70,
    'Teto do nicho': 120,
}


def mes(total_vendas, ads_mes=0.0):
    receita = lucro = 0.0
    for nome, peso in MIX.items():
        n = total_vendas * peso
        receita += n * PROD[nome]['preco']
        lucro += n * PROD[nome]['lucro']
    return receita, lucro, lucro - ads_mes


print('=== HOJE ===')
print('73 vendas / 365 dias = %.1f vendas/mes | reputacao VERMELHA | R$0 nos ultimos 7 dias' % (73 / 12))

print('\n=== CENARIOS AOS 90 DIAS (mix 45%% caixa10 / 40%% kit40 / 15%% kit60) ===')
print('%-16s %7s %11s %11s %10s %11s %9s' % (
    'cenario', 'vendas', 'receita', 'lucro bruto', 'Ads (6%)', 'lucro liq.', 'TACOS'))
for nome, v in CENARIOS.items():
    receita, bruto, _ = mes(v)
    ads = receita * 0.06
    print('%-16s %7d %11.2f %11.2f %10.2f %11.2f %8.1f%%' % (
        nome, v, receita, bruto, ads, bruto - ads, 6.0))

print('\n=== QUANTO CADA CENARIO EXIGE DE TRAFEGO ===')
print('(a 3%% de conversao, que e a mediana citada como boa para nicho concorrido)')
for nome, v in CENARIOS.items():
    for cvr in (0.02, 0.03, 0.05):
        visitas = v / cvr
        print('  %-14s %3d vendas @ CVR %.0f%% -> %5.0f visitas/mes (%4.0f/dia)' % (
            nome, v, cvr * 100, visitas, visitas / 30))
    print()

print('=== O QUE O ADS PRECISA ENTREGAR ===')
print('(supondo que metade das visitas venha de Ads no inicio)')
for nome, v in CENARIOS.items():
    receita, _, _ = mes(v)
    visitas = v / 0.03
    cliques_ads = visitas * 0.5
    for cpc in (1.00, 1.50):
        custo = cliques_ads * cpc
        roas = receita / custo if custo else 0
        print('  %-14s %4.0f cliques pagos @ CPC R$%.2f = R$%7.2f/mes -> ROAS implicito %.1fx' % (
            nome, cliques_ads, cpc, custo, roas))
    print()

print('=== RECUPERACAO DA REPUTACAO — a matematica dos envios incorretos ===')
print('hoje: 26 envios incorretos em 69 vendas com envio = 37,68% (limite 13%)')
for novas in (20, 40, 60, 100, 150):
    total = 69 + novas
    pct = 26 / total * 100
    ok = 'OK' if pct < 13 else '--'
    print('  + %3d vendas novas SEM erro -> %3d vendas, %5.2f%% de envios incorretos  %s' % (
        novas, total, pct, ok))
print('\n-> a janela e de 365 dias: os 26 erros tambem saem da conta conforme envelhecem.')
print('-> com Full, o vendedor nao despacha: o erro de envio deixa de ser possivel.')
