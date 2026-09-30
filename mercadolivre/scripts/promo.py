# -*- coding: utf-8 -*-
"""Promocao, troca de categoria e 4 cenarios de 3 meses.

Bases medidas:
  CPV .................. R$ 15,10 por caixa de 10
  Comissao Classico .... 14% sobre o preco EFETIVO de venda (o promocional)
  Envio comprador paga . ~6% do preco (medido: 1,40@18,70 | 2,40@40 | 4,80@83,10)
  Frete gratis kit 40 .. R$ 20,00 (ESTIMADO — unico numero mole)
  Armazenagem Full ..... Supermercado pequeno R$0,000/dia | Alim.e Bebidas R$0,007/dia
  Estoque antigo ....... Supermercado a partir de 2 meses | demais a partir de 4
"""
CPV = 15.10
COM = 0.14


def caixa(preco, dias_estoque=60, cat='super'):
    com = preco * COM
    env = round(preco * 0.06, 2)
    arm = (0.000 if cat == 'super' else 0.007) * dias_estoque
    l = preco - com - env - CPV - arm
    return com, env, arm, l, l / preco * 100


def kit(preco, dias_estoque=60, cat='super'):
    com = preco * COM
    env = 20.00
    arm = (0.000 if cat == 'super' else 0.015) * dias_estoque
    cpv = 4 * CPV
    l = preco - com - env - cpv - arm
    return com, env, arm, l, l / preco * 100


print('=== CAIXA DE 10 — escada de promocao (de R$ 34,90) ===')
print('%9s %7s %8s %8s %8s %8s  %s' % ('por', 'desc', 'comis', 'envio', 'lucro', 'margem', 'posicao'))
for p, nota in [(34.90, 'cheio'), (31.90, ''), (29.90, ''), (28.90, 'empata Coffee++'),
                (27.90, 'empata Orfeu'), (26.90, 'abaixo do Orfeu')]:
    com, env, arm, l, m = caixa(p)
    print('%9.2f %6.1f%% %8.2f %8.2f %8.2f %7.1f%%  %s' % (
        p, (34.90 - p) / 34.90 * 100, com, env, l, m, nota))

print('\n=== KIT 40 — escada de promocao (de R$ 139,90) ===')
print('%9s %7s %8s %8s %8s %8s  %s' % ('por', 'desc', 'comis', 'frete', 'lucro', 'margem', 'R$/cap'))
for p in (139.90, 129.90, 124.90, 119.90, 114.90):
    com, env, arm, l, m = kit(p)
    print('%9.2f %6.1f%% %8.2f %8.2f %8.2f %7.1f%%  %.2f' % (
        p, (139.90 - p) / 139.90 * 100, com, env, l, m, p / 40))

print('\n=== CUSTO DE TROCAR SUPERMERCADO -> ALIMENTOS E BEBIDAS ===')
print('Comissao: IGUAL nas duas (14% Classico) — confirmado na conta')
print('A diferenca e SO a armazenagem e o gatilho de estoque antigo.\n')
print('%-22s %12s %12s %12s' % ('', 'Supermercado', 'Alim.e Beb.', 'diferenca'))
for nome, tarifa_s, tarifa_a, un in [('caixa 10 (pequeno)', 0.000, 0.007, 90),
                                     ('kit 40 (medio)', 0.000, 0.015, 80)]:
    for dias in (90,):
        cs = tarifa_s * dias * un
        ca = tarifa_a * dias * un
        print('%-22s %12.2f %12.2f %12.2f   (%d un x %d dias)' % (
            nome, cs, ca, ca - cs, un, dias))
tot_s = 0.000 * 90 * 90 + 0.000 * 90 * 80
tot_a = 0.007 * 90 * 90 + 0.015 * 90 * 80
print('%-22s %12.2f %12.2f %12.2f' % ('TOTAL 3 meses', tot_s, tot_a, tot_a - tot_s))
print('\nEm troca: o custo de estoque antigo comeca aos 4 meses em vez de 2.')
print('Por unidade encalhada, o gatilho antecipado custa ~R$1/mes (valor do Full padrao).')

print('\n' + '=' * 78)
print('=== 4 CENARIOS — 3 MESES ===')
print('Estoque enviado: 90 caixas de 10 (30 por sabor) + 80 kits de 40 (20 por anuncio)')
CAIXAS_ENV, KITS_ENV = 90, 80
CAPITAL = CAIXAS_ENV * CPV + KITS_ENV * 4 * CPV
print('Capital em CPV: R$ %.2f' % CAPITAL)
print('Premissa: 60%% das vendas saem no preco promocional.\n')

CENARIOS = [
    ('PREJUIZO',  20, 10, 1200, 'Ads nao destrava, corta no 2o mes. Estoque encalha'),
    ('SE PAGOU',  45, 25, 1800, 'Rampa abre so o 1o portao'),
    ('LUCRO',     80, 45, 2400, 'Rampa abre ate o mes 2'),
    ('PERFEITO', 140, 80, 4200, 'Rampa completa, ROAS >= 12'),
]

print('%-10s %7s %6s %9s %11s %11s %10s %11s %9s' % (
    'cenario', 'caixas', 'kits', 'Ads', 'faturamento', 'lucro bruto', 'encalhe', 'resultado', 'TACOS'))
for nome, nc, nk, ads, obs in CENARIOS:
    # 60% promo, 40% cheio
    lc_promo = caixa(28.90)[3]; lc_cheio = caixa(34.90)[3]
    lk_promo = kit(124.90)[3];  lk_cheio = kit(139.90)[3]
    lucro_c = nc * (0.6 * lc_promo + 0.4 * lc_cheio)
    lucro_k = nk * (0.6 * lk_promo + 0.4 * lk_cheio)
    fat = nc * (0.6 * 28.90 + 0.4 * 34.90) + nk * (0.6 * 124.90 + 0.4 * 139.90)
    bruto = lucro_c + lucro_k
    # encalhe: sobra que passa de 2 meses em Supermercado, ~R$1/un/mes no 3o mes
    sobra_c = max(0, CAIXAS_ENV - nc); sobra_k = max(0, KITS_ENV - nk)
    encalhe = (sobra_c + sobra_k) * 1.00
    res = bruto - ads - encalhe
    tacos = ads / fat * 100 if fat else 0
    print('%-10s %7d %6d %9.2f %11.2f %11.2f %10.2f %11.2f %8.1f%%' % (
        nome, nc, nk, ads, fat, bruto, encalhe, res, tacos))

print('\n%-10s %s' % ('', 'observacao'))
for nome, nc, nk, ads, obs in CENARIOS:
    print('%-10s %s' % (nome, obs))

print('\n=== GIRO: quanto do estoque saiu em cada cenario ===')
for nome, nc, nk, ads, obs in CENARIOS:
    print('%-10s caixas %3d/%d (%3.0f%%) | kits %3d/%d (%3.0f%%)' % (
        nome, nc, CAIXAS_ENV, nc / CAIXAS_ENV * 100, nk, KITS_ENV, nk / KITS_ENV * 100))
