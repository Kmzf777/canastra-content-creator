# -*- coding: utf-8 -*-
"""Projecao de envio ao Full: 1, 2 e 3 meses x 3 posturas x 3 estrategias de preco.

MEDIDO (nao inferido):
  CPV ................ R$ 15,10/caixa de 10 | R$ 60,40/kit de 40
  Comissao Classico .. 14% sobre o preco EFETIVO
  Envio .............. MEDIDO no formulario 30/09, Classico, Full:
                       frete gratis = R$ 14,45 na CAIXA e no KIT (valor unico, nao escala)
                       comprador paga = R$ 1,40 @18,70 | 7,20 @139,90 (escala ~5-7% do preco)
                       frete gratis NAO e obrigatorio acima de R$ 79
  Categoria .......... Alimentos e Bebidas > Mercearia > Infusoes > Capsulas
                       (LIDO no formulario 30/09 -- NAO e Supermercado, como se supunha)
  Armazenagem Full ... A&B: R$ 0,007/dia caixa, R$ 0,015/dia kit, por unidade parada
  Estoque antigo ..... A&B dispara aos 4 MESES -> nao incide em 3 meses
  Reputacao .......... 26 envios incorretos em 69 envios = 37,68%. Janela de 365 dias.
                       Teto para verde: 13%.
  Trafego organico ... 12 visitas/dia no unico anuncio ativo, no vermelho e sem Ads.

PREMISSA (o que a Fase 1 existe para medir):
  ROAS base 4,50x a R$ 10/dia, caindo com a verba por retorno decrescente de leilao:
      roas = 4,50 * (10/ads)^0,25 * maturidade * lift_da_estrategia
  Ancora: os videos dizem "ROAS 3 a 5 nas primeiras semanas" para anuncio sem avaliacao.
  Maturidade: mes 1 = 1,00 | mes 2 = 1,10 | mes 3 = 1,20 (review e historico acumulam).
  Lift do verdinho: 1,35 na caixa de 10 (item de comparacao de preco), 1,00 no kit.
"""
import math

CPV_C, CPV_K = 15.10, 60.40
FRETE_GRATIS = 14.45      # MEDIDO no formulario em 30/09: igual na caixa e no kit
COM = 0.14
MIX_C = 0.55                     # fatia das VENDAS que sai em caixa de 10
N_ANUN_C, N_ANUN_K = 3, 4        # 3 anuncios de caixa, 4 de kit
DIAS = 30

# reputacao medida
ERROS, ENVIOS, TETO_VERDE = 26, 69, 0.13


def lucro_caixa(p):
    return p - p * COM - round(p * 0.06, 2) - CPV_C


def lucro_kit(p):
    return p - p * COM - FRETE_GRATIS - CPV_K


# --- as 3 estrategias de preco no Ads -------------------------------------
# o lift so se aplica a quem recebe o verdinho
ESTRATEGIAS = {
    '1-cheio':    dict(pc=34.90, pk=139.90, promo_c=False, promo_k=False,
                       nome='Preco cheio nos dois'),
    '2-verdinho': dict(pc=28.90, pk=124.90, promo_c=True,  promo_k=True,
                       nome='Verdinho nos dois'),
    '3-misto':    dict(pc=28.90, pk=139.90, promo_c=True,  promo_k=False,
                       nome='Verdinho na caixa, cheio no kit'),
}
LIFT_VERDINHO = 1.35


def perfil(e):
    d = ESTRATEGIAS[e]
    lc, lk = lucro_caixa(d['pc']), lucro_kit(d['pk'])
    pm = MIX_C * d['pc'] + (1 - MIX_C) * d['pk']
    lm = MIX_C * lc + (1 - MIX_C) * lk
    lift = (MIX_C * (LIFT_VERDINHO if d['promo_c'] else 1.0)
            + (1 - MIX_C) * (LIFT_VERDINHO if d['promo_k'] else 1.0))
    return dict(nome=d['nome'], pc=d['pc'], pk=d['pk'], lc=lc, lk=lk,
                pm=pm, lm=lm, roas_eq=pm / lm, lift=lift)


# --- custo de estoque parado no Full -------------------------------------
# CORRIGIDO 30/09: a categoria real do anuncio e
#   Alimentos e Bebidas > Mercearia > Infusoes > Capsulas  (lido no formulario),
# NAO Supermercado. Logo o estoque antigo dispara aos 4 MESES, nao aos 2 --
# ou seja, NAO dispara dentro do horizonte de 3 meses desta projecao.
# O que sobra e a armazenagem diaria de Alimentos e Bebidas.
ARM_C, ARM_K = 0.007, 0.015       # R$/dia por unidade parada (pequeno / medio)


def custo_parada(mes, un_c, un_k):
    arm = (un_c * ARM_C + un_k * ARM_K) * DIAS
    antigo = 0.0 if mes <= 3 else (un_c + un_k) * 1.21   # so a partir do mes 4
    return arm + antigo


# --- posturas -------------------------------------------------------------
MATURIDADE = {1: 1.00, 2: 1.10, 3: 1.20}
ROAS_REF, ADS_REF, ELAST = 4.50, 10.0, 0.25

POSTURAS = {
    'conservadora': dict(ads=[10, 10, 15], cobertura=1.3,
                         nome='Conservadora', regra='envia 1,3x a demanda do mes'),
    'ideal':        dict(ads=[20, 30, 40], cobertura=2.0,
                         nome='Ideal', regra='envia 2 meses de demanda (teto do Supermercado)'),
    'agressiva':    dict(ads=[60, 80, 80], cobertura=1.8,
                         nome='Agressiva', regra='envia 1,8x a demanda; reposicao semanal'),
}


def roas(ads, mes, lift):
    return ROAS_REF * (ADS_REF / ads) ** ELAST * MATURIDADE[mes] * lift


def projeta(est, post, meses):
    p, q = perfil(est), POSTURAS[post]
    linhas, vend_ac, res_ac, ads_ac, cap_ac = [], 0.0, 0.0, 0.0, 0.0
    env_c = env_k = 0.0          # estoque JA no Full
    for mes in range(1, meses + 1):
        ads_dia = q['ads'][mes - 1]
        r = roas(ads_dia, mes, p['lift'])
        ads = ads_dia * DIAS
        dem = ads * r / p['pm']                        # vendas que a verba gera
        # estoque que essa demanda exige, com a folga da postura
        alvo = dem * q['cobertura']
        n = max(alvo * MIX_C / N_ANUN_C, alvo * (1 - MIX_C) / N_ANUN_K)
        n = math.ceil(round(n, 6))
        prec_c, prec_k = N_ANUN_C * n, N_ANUN_K * n     # estoque alvo no Full
        remessa_c = max(0.0, prec_c - env_c)            # so o que falta repor
        remessa_k = max(0.0, prec_k - env_k)
        env_c += remessa_c
        env_k += remessa_k
        cap = remessa_c * CPV_C + remessa_k * CPV_K
        # vendas travadas pelo estoque disponivel
        vc = min(dem * MIX_C, env_c)
        vk = min(dem * (1 - MIX_C), env_k)
        esgotou = (dem * MIX_C > vc + 1e-9) or (dem * (1 - MIX_C) > vk + 1e-9)
        env_c -= vc
        env_k -= vk
        vend = vc + vk
        fat = vc * p['pc'] + vk * p['pk']
        bruto = vc * p['lc'] + vk * p['lk']
        parado = custo_parada(mes, env_c, env_k)
        res = bruto - ads - parado
        vend_ac += vend
        res_ac += res
        ads_ac += ads
        cap_ac += cap
        linhas.append(dict(mes=mes, ads_dia=ads_dia, ads=ads, roas=r, dem=dem,
                           remessa_c=remessa_c, remessa_k=remessa_k, n=n, cap=cap,
                           vend=vend, fat=fat, bruto=bruto, parado=parado, res=res,
                           esgotou=esgotou, sobra=env_c + env_k,
                           vend_ac=vend_ac, res_ac=res_ac, ads_ac=ads_ac, cap_ac=cap_ac,
                           rep=ERROS / (ENVIOS + vend_ac) * 100))
    return linhas


# ==========================================================================
print('=' * 108)
print('PERFIL DAS 3 ESTRATEGIAS DE PRECO')
print('=' * 108)
print('%-12s %-34s %8s %8s %8s %8s %9s %7s' % (
    'chave', 'o que e', 'caixa', 'kit', 'preco m', 'lucro m', 'ROAS eq', 'lift'))
for k in ESTRATEGIAS:
    p = perfil(k)
    print('%-12s %-34s %8.2f %8.2f %8.2f %8.2f %8.2fx %6.2fx' % (
        k, p['nome'], p['pc'], p['pk'], p['pm'], p['lm'], p['roas_eq'], p['lift']))

base = perfil('1-cheio')
print('\nLIFT DE CONVERSAO NECESSARIO para a estrategia empatar com o preco cheio:')
for k in ('2-verdinho', '3-misto'):
    p = perfil(k)
    nec = base['lm'] / p['lm']
    print('  %-12s precisa converter %+6.1f%% mais  | lift suposto %+6.1f%%  -> %s' % (
        k, (nec - 1) * 100, (p['lift'] - 1) * 100,
        'PAGA' if p['lift'] >= nec else 'NAO paga'))

print('\nREPUTACAO: %d erros em %d envios = %.2f%%. Teto do verde = %.0f%%.' % (
    ERROS, ENVIOS, ERROS / ENVIOS * 100, TETO_VERDE * 100))
print('  vendas limpas necessarias = %d   (26/(69+V) <= 0,13)' % (
    math.ceil(ERROS / TETO_VERDE - ENVIOS)))

for est in ESTRATEGIAS:
    print('\n' + '=' * 108)
    print('ESTRATEGIA %s  --  %s' % (est, perfil(est)['nome']))
    print('=' * 108)
    for post in POSTURAS:
        q = POSTURAS[post]
        print('\n  %s  (%s)  Ads/dia: %s' % (q['nome'].upper(), q['regra'], q['ads']))
        print('  %4s %8s %7s %8s %8s %8s %9s %10s %10s %10s %10s %8s' % (
            'mes', 'Ads/dia', 'ROAS', 'demanda', 'vendas', 'de cada', 'capital',
            'faturam.', 'lucro br.', 'resultado', 'acum.', 'rep.%'))
        for l in projeta(est, post, 3):
            print('  %4d %8.0f %6.2fx %8.1f %8.1f %8d %9.0f %10.0f %10.0f %10.0f %10.0f %7.1f%%%s' % (
                l['mes'], l['ads_dia'], l['roas'], l['dem'], l['vend'], l['n'], l['cap'],
                l['fat'], l['bruto'], l['res'], l['res_ac'], l['rep'],
                '  ESGOTOU' if l['esgotou'] else ''))


# ==========================================================================
# CONSOLIDADO POR PERIODO — o que o artefato mostra
# ==========================================================================
print('\n\n' + '=' * 108)
print('CONSOLIDADO: 1, 2 e 3 MESES')
print('=' * 108)
print('%-11s %-13s %4s %7s %8s %8s %9s %10s %10s %9s %9s %8s' % (
    'estrategia', 'postura', 'per', 'vendas', 'caixas', 'kits', 'unid.',
    'capital', 'faturam.', 'Ads', 'RESULT.', 'rep.%'))
CONSOL = {}
for est in ESTRATEGIAS:
    for post in POSTURAS:
        ls = projeta(est, post, 3)
        for per in (1, 2, 3):
            sub = ls[:per]
            cx = sum(l['remessa_c'] for l in sub)
            kt = sum(l['remessa_k'] for l in sub)
            d = dict(vendas=sum(l['vend'] for l in sub),
                     caixas=cx, kits=kt, unid=cx + kt,
                     capital=sum(l['cap'] for l in sub),
                     fat=sum(l['fat'] for l in sub),
                     ads=sum(l['ads'] for l in sub),
                     bruto=sum(l['bruto'] for l in sub),
                     parado=sum(l['parado'] for l in sub),
                     res=sub[-1]['res_ac'], rep=sub[-1]['rep'],
                     pico=ls[0]['cap'])
            CONSOL[(est, post, per)] = d
            print('%-11s %-13s %4d %7.0f %8.0f %8.0f %9.0f %10.0f %10.0f %9.0f %9.0f %7.1f%%' % (
                est, post, per, d['vendas'], cx, kt, cx + kt, d['capital'],
                d['fat'], d['ads'], d['res'], d['rep']))
    print()

print('=' * 108)
print('QUANDO A REPUTACAO VIRA VERDE (precisa de %d vendas limpas)' % 131)
print('=' * 108)
for est in ESTRATEGIAS:
    for post in POSTURAS:
        ls = projeta(est, post, 3)
        mes_verde = next((l['mes'] for l in ls if l['vend_ac'] >= 131), None)
        print('  %-11s %-13s vendas em 3 meses: %5.0f  ->  %s' % (
            est, post, ls[-1]['vend_ac'],
            ('VERDE no mes %d' % mes_verde) if mes_verde else 'NAO chega ao verde'))

print('\n' + '=' * 108)
print('CAPITAL: entrada vs reposicao')
print('=' * 108)
print('O capital do mes 1 e o unico que sai do bolso. Do mes 2 em diante, a receita repoe.')
print('%-11s %-13s %14s %16s %16s' % (
    'estrategia', 'postura', 'mes 1 (pico)', 'faturam. mes 1', 'cobre a reposicao?'))
for est in ESTRATEGIAS:
    for post in POSTURAS:
        ls = projeta(est, post, 3)
        print('  %-11s %-11s %12.0f %16.0f %16s' % (
            est, post, ls[0]['cap'], ls[0]['fat'],
            'sim' if ls[0]['fat'] >= ls[1]['cap'] else 'NAO, falta %.0f' % (ls[1]['cap'] - ls[0]['fat'])))

print('\n' + '=' * 108)
print('O QUE OS R$ 75 DE GARANTIA COMPRAM')
print('=' * 108)
print('Sem verde/amarelo a Central de promocoes esta bloqueada (medido em 30/09/2026),')
print('logo as estrategias 2 e 3 nao existem -- so resta a 1.')
for post in POSTURAS:
    a = CONSOL[('1-cheio', post, 3)]['res']
    b = CONSOL[('3-misto', post, 3)]['res']
    print('  %-13s estrategia 1: %+8.0f  |  estrategia 3: %+8.0f  |  diferenca: %+8.0f em 3 meses' % (
        post, a, b, b - a))
