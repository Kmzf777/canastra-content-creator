# -*- coding: utf-8 -*-
"""Modelo de margem das capsulas Canastra no ML. CPV real: R$15,10/caixa de 10."""

CPV_CAIXA = 15.10          # custo da caixa de 10, impostos inclusos
CPV_CAP = CPV_CAIXA / 10   # 1,51

def op_cost(preco, caixas):
    """Custo operacional/frete por pedido. Faixa ate 0,3kg ate 3 caixas; 0,3-0,5 ate 6; 1-2kg acima.
    Valores <=99,99 sao os publicados; acima e ESTIMATIVA a confirmar no simulador."""
    if preco < 19:    return 5.65
    if preco < 49:    return 6.55
    if preco < 79:    return 7.75
    if preco < 100:   return 12.35
    if preco < 200:   return 15.00   # estimativa
    if preco < 300:   return 20.00   # estimativa
    return 23.00                      # estimativa

def armazenagem(caixas, dias=60):
    tarifa = 0.007 if caixas <= 2 else 0.015   # pequeno vs medio
    return tarifa * dias

def linha(caixas, preco, comissao_pct=14, dias=60):
    caps = caixas * 10
    com = preco * comissao_pct / 100
    op = op_cost(preco, caixas)
    cpv = caixas * CPV_CAIXA
    arm = armazenagem(caixas, dias)
    custo = com + op + cpv + arm
    lucro = preco - custo
    return {
        'caixas': caixas, 'caps': caps, 'preco': preco,
        'rs_cap': preco / caps,
        'com': com, 'op': op, 'cpv': cpv, 'arm': arm,
        'take_ml': com + op, 'take_pct': (com + op) / preco * 100,
        'lucro': lucro, 'margem': lucro / preco * 100,
        'acos_max': lucro / preco * 100 / 2,
    }

def show(rows, titulo):
    print('\n=== ' + titulo + ' ===')
    print('%-7s %-8s %-8s %8s %8s %8s %8s %9s %8s %7s' % (
        'caixas','caps','preco','R$/cap','comis','oper','CPV','take ML%','lucro','marg%'))
    for r in rows:
        print('%-7d %-8d %-8.2f %8.2f %8.2f %8.2f %8.2f %8.1f%% %8.2f %6.1f%%' % (
            r['caixas'], r['caps'], r['preco'], r['rs_cap'],
            r['com'], r['op'], r['cpv'], r['take_pct'], r['lucro'], r['margem']))

print('CPV caixa de 10: R$ %.2f  |  por capsula: R$ %.2f' % (CPV_CAIXA, CPV_CAP))

show([linha(1, p) for p in (24.90, 27.90, 29.90, 32.90, 34.90, 39.90)], '1 caixa - 10 capsulas')
show([linha(2, p) for p in (54.90, 59.90, 64.90, 69.90)], '2 caixas - 20 capsulas')
show([linha(4, p) for p in (99.90, 109.90, 119.90, 129.90, 139.90, 149.90)], '4 caixas - 40 capsulas')
show([linha(6, p) for p in (169.90, 179.90, 189.90, 199.90)], '6 caixas - 60 capsulas')
show([linha(10, p) for p in (259.90, 279.90, 289.90, 299.90, 319.90)], '10 caixas - 100 capsulas')

print('\n=== CLASSICO (14%) vs PREMIUM (19%) ===')
for cx, p in ((4, 129.90), (10, 289.90)):
    c = linha(cx, p, 14); pr = linha(cx, p, 19)
    print('%d caps a R$%.2f: Classico margem %.1f%% (R$%.2f) | Premium %.1f%% (R$%.2f) | custo do parcelamento: %.1f pontos, R$%.2f' % (
        cx*10, p, c['margem'], c['lucro'], pr['margem'], pr['lucro'],
        c['margem']-pr['margem'], c['lucro']-pr['lucro']))
    print('   12x sem juros = R$%.2f/mes' % (p/12))

print('\n=== ROAS OBJETIVO (ACOS = metade da margem) ===')
for cx, p in ((1, 32.90), (4, 129.90), (10, 289.90)):
    r = linha(cx, p)
    acos = r['acos_max']
    roas = 100 / acos if acos > 0 else 0
    lucro_pos_ads = r['lucro'] - p * acos / 100
    print('%3d caps R$%.2f -> margem %.1f%% | ACOS max %.1f%% | ROAS objetivo %.1fx | lucro pos-Ads R$%.2f (%.1f%%)' % (
        cx*10, p, r['margem'], acos, roas, lucro_pos_ads, lucro_pos_ads/p*100))

print('\n=== PRECO MINIMO para 25%% e 30%% de margem ===')
for cx in (1, 2, 4, 6, 10):
    for alvo in (25, 30):
        lo, hi = 10.0, 900.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if linha(cx, mid)['margem'] < alvo: lo = mid
            else: hi = mid
        r = linha(cx, hi)
        print('%3d caps: margem %d%% exige R$ %.2f (R$ %.2f/cap)' % (cx*10, alvo, hi, hi/(cx*10)))

print('\n=== ESTOQUE FULL - capital e armazenagem (60 dias) ===')
for cx, unidades in ((4, 100), (4, 200), (10, 40)):
    capital = unidades * cx * CPV_CAIXA
    arm = unidades * armazenagem(cx, 60)
    print('%d unidades do kit de %d caps: capital R$ %.2f | armazenagem 60d R$ %.2f' % (
        unidades, cx*10, capital, arm))

print('\n=== TITULOS - contagem de caracteres (limite ML = 60) ===')
for t in [
    'Kit 40 Cápsulas Café Especial Canastra Compatível Nespresso',
    'Kit 100 Cápsulas Café Especial Canastra Nespresso Serra MG',
    'Cápsulas Café Especial Canastra Compatível Nespresso 10un',
    'Kit 40 Cápsulas Café Especial Canastra Nespresso Serra MG',
    'Café Especial Canastra 40 Cápsulas Compatível Nespresso MG',
]:
    print('%3d  %s' % (len(t), t))
