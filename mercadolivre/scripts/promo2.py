# -*- coding: utf-8 -*-
"""Cenarios de 3 meses, corrigidos.

O erro da 1a versao: fixei a rampa de Ads (ate R$150/dia) sem checar se o volume
deste nicho a sustenta. Nao sustenta. A rampa so abre se o ROAS bater a meta, e
ROAS 7 a R$40/dia exigiria R$8.400/mes de receita — acima de todos os cenarios.
Aqui o Ads fica em R$20/dia (piso de aprendizado) e o que varia e por QUANTOS MESES
antes de cortar.
"""
CPV = 15.10
COM = 0.14


def lucro_caixa(p):
    return p - p * COM - round(p * 0.06, 2) - CPV


def lucro_kit(p):
    return p - p * COM - 20.00 - 4 * CPV


# 60% das vendas no promocional, 40% no cheio
LC = 0.6 * lucro_caixa(28.90) + 0.4 * lucro_caixa(34.90)
LK = 0.6 * lucro_kit(124.90) + 0.4 * lucro_kit(139.90)
PC = 0.6 * 28.90 + 0.4 * 34.90
PK = 0.6 * 124.90 + 0.4 * 139.90

print('lucro medio por caixa vendida : R$ %.2f   (preco medio R$ %.2f)' % (LC, PC))
print('lucro medio por kit vendido   : R$ %.2f   (preco medio R$ %.2f)' % (LK, PK))

ENV_C, ENV_K = 90, 80
CAPITAL = ENV_C * CPV + ENV_K * 4 * CPV
print('\nEstoque enviado: %d caixas + %d kits  |  capital em CPV: R$ %.2f' % (ENV_C, ENV_K, CAPITAL))
print('Ads: R$ 20/dia (piso de aprendizado). O que muda e por quantos meses roda.\n')

CEN = [
    ('PREJUIZO',  15,  8, 1, 'ROAS ruim, corta o Ads no fim do mes 1. Estoque encalha'),
    ('SE PAGOU',  45, 25, 2, 'Roda 2 meses, empata. Nem ganhou nem perdeu'),
    ('LUCRO',     75, 45, 3, 'Roda os 3 meses e o giro cobre a verba'),
    ('PERFEITO',  90, 75, 3, 'Esgota as caixas e quase todos os kits'),
]

print('%-10s %7s %5s %8s %11s %11s %9s %11s %8s %7s' % (
    'cenario', 'caixas', 'kits', 'Ads', 'faturamento', 'lucro bruto', 'encalhe',
    'RESULTADO', 'TACOS', 'giro'))
linhas = []
for nome, nc, nk, meses, obs in CEN:
    ads = 20 * 30 * meses
    fat = nc * PC + nk * PK
    bruto = nc * LC + nk * LK
    sobra = (ENV_C - nc) + (ENV_K - nk)
    encalhe = sobra * 1.00            # estoque antigo: Supermercado cobra a partir de 2 meses
    res = bruto - ads - encalhe
    tacos = ads / fat * 100
    giro = (nc + nk) / (ENV_C + ENV_K) * 100
    linhas.append((nome, nc, nk, ads, fat, bruto, encalhe, res, tacos, giro, obs))
    print('%-10s %7d %5d %8.0f %11.2f %11.2f %9.0f %11.2f %7.1f%% %6.0f%%' % (
        nome, nc, nk, ads, fat, bruto, encalhe, res, tacos, giro))

print()
for l in linhas:
    print('%-10s %s' % (l[0], l[10]))

print('\n=== O QUE O TACOS DENUNCIA ===')
print('A regra do mercado e 5-6% de TACOS no regime permanente.')
for l in linhas:
    ads_ideal = l[4] * 0.06
    print('%-10s TACOS real %5.1f%% | a 6%% o Ads caberia em R$ %7.2f (R$ %5.2f/dia)' % (
        l[0], l[8], ads_ideal, ads_ideal / 90))
print('\n-> Em TODOS os cenarios o Ads a R$20/dia fica acima do teto de 6%.')
print('-> No lancamento isso e INVESTIMENTO DE ENTRADA, nao custo operacional:')
print('   compra review e historico. Mas precisa de teto de tempo, nao de infinito.')

print('\n=== PONTO DE EQUILIBRIO DO ADS ===')
for l in linhas:
    nome, nc, nk = l[0], l[1], l[2]
    bruto, encalhe = l[5], l[6]
    teto = bruto - encalhe
    print('%-10s o Ads so se paga ate R$ %7.2f (R$ %5.2f/dia). Gastou R$ %.0f' % (
        nome, teto, teto / 90, l[3]))
