# -*- coding: utf-8 -*-
"""Matriz estoque x Ads: o estoque aguenta a verba?

Mecanica central: o Ads gera demanda; o estoque e o teto. Se a demanda do Ads passa
do estoque, o anuncio ESGOTA e para de vender antes do fim do mes.

Custo da ruptura (Milton P Rabello 27/08, swCx36qRg0w):
  "Cada um dia de anuncio pausado, voce perde DOIS dias de ranqueamento."
"""
CPV_C, CPV_K = 15.10, 60.40
P_C, P_K = 34.90, 139.90         # precos cheios
L_C, L_K = 12.82, 39.91          # lucro por venda
MIX_C = 0.55                      # fatia das VENDAS que sai em caixa de 10

# 3 anuncios de caixa + 4 de kit
N_ANUN_C, N_ANUN_K = 3, 4

PRECO_MEDIO = MIX_C * P_C + (1 - MIX_C) * P_K
LUCRO_MEDIO = MIX_C * L_C + (1 - MIX_C) * L_K


def lote(n_por_anuncio):
    """n unidades de cada um dos 7 anuncios."""
    uc = n_por_anuncio * N_ANUN_C
    uk = n_por_anuncio * N_ANUN_K
    return uc, uk, uc * CPV_C + uk * CPV_K


def simula(n_por_anuncio, ads_dia, roas, dias=30):
    uc, uk, capital = lote(n_por_anuncio)
    # demanda que a verba gera no periodo, se houvesse estoque infinito
    receita_pot = ads_dia * dias * roas
    vendas_pot = receita_pot / PRECO_MEDIO
    # divide pelo mix e trava no estoque de cada tipo
    pot_c, pot_k = vendas_pot * MIX_C, vendas_pot * (1 - MIX_C)
    vc, vk = min(pot_c, uc), min(pot_k, uk)
    vendas = vc + vk
    # dia em que o primeiro tipo esgota
    dia_esg_c = dias * uc / pot_c if pot_c > 0 else 999
    dia_esg_k = dias * uk / pot_k if pot_k > 0 else 999
    dia_esg = min(dia_esg_c, dia_esg_k)
    esgotou = dia_esg < dias
    # Ads so trabalha ate esgotar; depois seria desperdicio (assumimos corte no dia)
    ads_gasto = ads_dia * min(dias, dia_esg)
    fat = vc * P_C + vk * P_K
    bruto = vc * L_C + vk * L_K
    return dict(uc=uc, uk=uk, capital=capital, vendas=vendas, vc=vc, vk=vk,
                fat=fat, bruto=bruto, ads=ads_gasto, res=bruto - ads_gasto,
                dia_esg=dia_esg if esgotou else None,
                dias_parado=max(0, dias - dia_esg) if esgotou else 0,
                roas_real=fat / ads_gasto if ads_gasto else 0)


print('preco medio da venda: R$ %.2f | lucro medio: R$ %.2f' % (PRECO_MEDIO, LUCRO_MEDIO))
print('mix suposto: %d%% caixa de 10, %d%% kit de 40' % (MIX_C * 100, (1 - MIX_C) * 100))
print()
print('=' * 100)
print('MATRIZ: quantos de CADA um dos 7 anuncios  x  verba diaria   (ROAS 4, realista no lancamento)')
print('=' * 100)
print('%6s %7s %9s | %9s %8s %9s %9s %10s %12s' % (
    'de cada', 'unid.', 'capital', 'Ads/dia', 'vendas', 'faturam.', 'Ads gasto',
    'resultado', 'esgota em'))
for n in (5, 10, 20, 40, 80):
    for ads in (20, 40, 80):
        r = simula(n, ads, 4)
        esg = ('dia %.0f' % r['dia_esg']) if r['dia_esg'] else 'nao esgota'
        marca = '  <-- ' if r['dia_esg'] and r['dia_esg'] < 10 else ''
        print('%6d %7d %9.0f | %9d %8.1f %9.0f %9.0f %10.0f %12s%s' % (
            n, r['uc'] + r['uk'], r['capital'], ads, r['vendas'], r['fat'],
            r['ads'], r['res'], esg, marca))
    print()

print('=' * 100)
print('O QUE ACONTECE DEPOIS DE ESGOTAR (custo escondido da agressividade)')
print('=' * 100)
print('Regra: 1 dia de anuncio parado = 2 dias de ranqueamento perdidos.')
print('%6s %9s %12s %14s %18s' % ('de cada', 'Ads/dia', 'esgota em', 'dias parado', 'ranqueam. perdido'))
for n in (5, 10, 20):
    for ads in (40, 80):
        r = simula(n, ads, 4)
        if r['dia_esg']:
            print('%6d %9d %11.0f %14.0f %16.0f dias' % (
                n, ads, r['dia_esg'], r['dias_parado'], r['dias_parado'] * 2))
print()

print('=' * 100)
print('REPOSICAO: quanto precisa repor por SEMANA para sustentar cada verba')
print('=' * 100)
print('(voces tem reposicao rapida — e isto que torna o Full raso viavel)')
print('%9s %8s %14s %16s %16s' % ('Ads/dia', 'ROAS', 'vendas/mes', 'caixas/semana', 'kits/semana'))
for ads in (20, 40, 80):
    for roas in (4, 7, 10):
        v = ads * 30 * roas / PRECO_MEDIO
        print('%9d %8d %14.1f %16.1f %16.1f' % (
            ads, roas, v, v * MIX_C / 4.3, v * (1 - MIX_C) / 4.3))
    print()

print('=' * 100)
print('COBERTURA MINIMA: quanto enviar para NAO esgotar em 30 dias')
print('=' * 100)
print('%9s %8s %14s %16s %14s %12s' % (
    'Ads/dia', 'ROAS', 'vendas/mes', 'de cada anuncio', 'unidades', 'capital'))
for ads in (20, 40, 80):
    for roas in (4, 7, 10):
        v = ads * 30 * roas / PRECO_MEDIO
        nc = v * MIX_C / N_ANUN_C
        nk = v * (1 - MIX_C) / N_ANUN_K
        n = max(nc, nk)
        uc, uk, cap = lote(n)
        print('%9d %8d %14.1f %16.1f %14.0f %12.0f' % (ads, roas, v, n, uc + uk, cap))
    print()
