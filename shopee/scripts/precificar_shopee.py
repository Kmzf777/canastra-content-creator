# -*- coding: utf-8 -*-
"""Precificação na Shopee com o CMV real, em escada CM1 → CM2 → CM3.

Fontes das constantes (conferidas contra pesquisa-marketplaces/shopee/CONSOLIDADO.md §1 e §8
em 15/10/2026; nenhuma medida ainda num pedido da Canastra):

- Comissão + taxa fixa POR ITEM, faixas de 01/10/2026 — seller.shopee.com.br/edu/article/18483
  (confirmado no navegador em 15/10/2026). Já inclui a taxa de transação.
- Vendedor CPF: +R$ 3 por item depois de 450 pedidos em 90 dias — edu/article/18484.
- Subsídio Pix: 5% de R$ 80 a R$ 499,99, PAGO PELA SHOPEE, repasse igual ao vendedor —
  edu/article/18483. Não entra no custo do vendedor; o script só mostra o preço que o comprador vê.
- Frete grátis: subsídio da Shopee até R$ 20 / 30 / 40 por faixa; coparticipação do vendedor de
  25% do desconto de frete (teto R$ 10) SÓ na logística própria / Intelipost / API de Frete —
  edu/article/23431 e 25794. Na logística da Shopee (coleta, ponto, Full) a coparticipação é 0.
- Campanhas de Destaque: 3,5% sobre TODAS as vendas da loja desde 23/04/2026, renovação
  automática — edu/article/18712 (atualizado em 22/09/2026).
- Devolução Fácil: R$ 0,49 por pedido confirmado, ativação automática — edu/article/26700.
- Full+: −0,5 a −2 p.p. de comissão em itens ≥ R$ 50 via Full — edu/article/27600.
- CMV e imposto (9% sobre o preço): mercadolivre/custos.md (fonte única).

NÃO MEDIDO (hipóteses que o script deixa explícitas):
- Kit conta como 1 item para a taxa fixa (D18 do CONSOLIDADO; nenhum artigo oficial trata).
  `--itens` simula o kit pagando N taxas.
- Base da comissão quando há cupom do vendedor: o script cobra comissão sobre o preço cheio
  (conservador).
- Valor do desconto de frete por pedido (só importa na logística própria): `--frete-desc`.

    python shopee/scripts/precificar_shopee.py                       # tabela da entrada (1 kg, 500 g, kits)
    python shopee/scripts/precificar_shopee.py --preco 99.99 --cmv 47
    python shopee/scripts/precificar_shopee.py --preco 99.99 --cmv 47 --campanha --ads 8 --cupom 5
    python shopee/scripts/precificar_shopee.py --margem 15 --cmv 47
"""
import argparse
import sys

IMPOSTO = 0.09   # sobre o preço de venda (mercadolivre/custos.md)
CMV = {'1kg': 47.00, '500g': 26.00, '250g': 14.00, 'capsula10': 15.10}

# (preço mínimo da faixa, comissão %, taxa fixa por item) — edu/article/18483, 01/10/2026
FAIXAS = [(0.00, 0.20, 4.50), (80.00, 0.14, 16.00), (100.00, 0.14, 20.00), (200.00, 0.14, 26.00)]
ADICIONAL_CPF = 3.00          # por item, depois de 450 pedidos em 90 dias (18484)
TAXA_CAMPANHA = 0.035         # Campanhas de Destaque, sobre todas as vendas da loja (18712)
DEVOLUCAO_FACIL = 0.49        # por pedido (26700)
COPART_FRETE, COPART_TETO = 0.25, 10.00   # só logística própria (25794)
TETO_FRETE = [(0.00, 20.00), (80.00, 30.00), (200.00, 40.00)]   # subsídio da Shopee (23431)
PIX = [(80.00, 0.05), (500.00, 0.08)]     # pago pela Shopee (18483)


def faixa(preco):
    for minimo, pct, fixa in reversed(FAIXAS):
        if preco >= minimo:
            return pct, fixa
    raise ValueError(preco)


def _degrau(tabela, preco, padrao=0.0):
    v = padrao
    for minimo, x in tabela:
        if preco >= minimo:
            v = x
    return v


def resultado(preco, cmv, itens=1, cpf=False, logistica='shopee', frete_desc=0.0,
              ads_pct=0.0, cupom=0.0, campanha=False, afiliado_pct=0.0, full_mais_pp=0.0):
    """Escada de margem de UM pedido de preço `preco` (um anúncio; `itens` = taxas fixas cobradas).

    CM1 = preço − CMV − comissão − taxa fixa × itens − adicional CPF − coparticipação − imposto
    CM2 = CM1 − Ads − cupom do vendedor − afiliado do vendedor − taxa de campanha
    CM3 = CM2 − Devolução Fácil (custos do Full por ociosidade ficam fora: dependem do giro)
    """
    pct, fixa = faixa(preco)
    pct = max(pct - full_mais_pp / 100, 0)
    comissao = round(preco * pct, 2)
    fixas = round(fixa * itens + (ADICIONAL_CPF * itens if cpf else 0), 2)
    copart = 0.0
    if logistica == 'propria':
        copart = round(min(frete_desc * COPART_FRETE, COPART_TETO), 2)
    receita = preco - cupom
    imposto = round(receita * IMPOSTO, 2)
    cm1 = round(receita - cmv - comissao - fixas - copart - imposto, 2)
    ads = round(preco * ads_pct / 100, 2)
    camp = round(receita * TAXA_CAMPANHA, 2) if campanha else 0.0
    afil = round(receita * afiliado_pct / 100, 2)
    cm2 = round(cm1 - ads - camp - afil, 2)
    cm3 = round(cm2 - DEVOLUCAO_FACIL, 2)
    antes_ads = cm1 - camp - afil - DEVOLUCAO_FACIL   # margem disponível para Ads (CM3 sem Ads)
    acos_eq = antes_ads / preco * 100 if antes_ads > 0 else 0.0
    return dict(preco=preco, comissao=comissao, fixas=fixas, copart=copart, imposto=imposto,
                cmv=cmv, cm1=cm1, cm1_pct=round(cm1 / preco * 100, 1), ads=ads, campanha=camp,
                afiliado=afil, cupom=cupom, cm2=cm2, cm3=cm3, cm3_pct=round(cm3 / preco * 100, 1),
                acos_eq=round(acos_eq, 1),
                roas_eq=round(preco / antes_ads, 1) if antes_ads > 0 else None,
                taxa_efetiva=round((comissao + fixas) / preco * 100, 1),
                pix_comprador=round(preco * (1 - _degrau(PIX, preco)), 2),
                teto_frete_shopee=_degrau(TETO_FRETE, preco))


def preco_para_margem(margem_pct, cmv, **kw):
    """Menor preço cuja CM3 atinge a margem pedida, varrendo de centavo em centavo (degraus!)."""
    p = 10.00
    while p < 1000:
        if resultado(round(p, 2), cmv, **kw)['cm3_pct'] >= margem_pct:
            return round(p, 2)
        p += 0.01
    return None


def zonas_mortas(cmv, **kw):
    """Faixas onde cobrar mais deixa menos CM3: logo acima de cada degrau da taxa fixa."""
    out = []
    for i in range(1, len(FAIXAS)):
        degrau = FAIXAS[i][0]
        antes = resultado(round(degrau - 0.01, 2), cmv, **kw)['cm3']
        p = degrau
        while resultado(round(p, 2), cmv, **kw)['cm3'] < antes and p < degrau + 200:
            p += 0.01
        out.append((degrau, round(p, 2), antes))
    return out


SKUS = [
    ('1 kg', CMV['1kg'], (69.90, 79.90, 79.99, 89.90, 99.90, 99.99, 109.90, 119.90, 129.90)),
    ('500 g', CMV['500g'], (39.90, 44.90, 49.90, 54.90, 59.90, 64.90)),
    ('Kit 2 × 500 g', 2 * CMV['500g'], (69.90, 79.90, 79.99, 89.90, 99.90, 99.99)),
    ('Kit 2 × 1 kg', 2 * CMV['1kg'], (159.90, 179.90, 189.90, 199.90, 199.99, 219.90)),
]


def tabela():
    print('Escada de margem por pedido (logística da Shopee, CNPJ, sem cupom; kit = 1 taxa fixa, NÃO MEDIDO)\n')
    print('| SKU | preço | R$/kg | Pix comprador | tarifa efet. | CM1 | CM1% | ACOS eq. | ROAS eq. '
          '| CM3 c/ campanha 3,5% | ROAS eq. c/ campanha |')
    print('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for nome, cmv, precos in SKUS:
        kg = {'1 kg': 1, '500 g': 0.5, 'Kit 2 × 500 g': 1, 'Kit 2 × 1 kg': 2}[nome]
        for p in precos:
            r = resultado(p, cmv)
            c = resultado(p, cmv, campanha=True)
            print('| %s | %.2f | %.2f | %.2f | %.1f%% | %.2f | %.1f%% | %.1f%% | %s | %.2f | %s |' % (
                nome, p, p / kg, r['pix_comprador'], r['taxa_efetiva'], r['cm1'], r['cm1_pct'],
                r['acos_eq'], r['roas_eq'] or 'sem margem', c['cm3'], c['roas_eq'] or 'sem margem'))
    print('\nKit × avulso (CM3 por pedido, sem campanha):')
    for nome, cmv, p_kit, p_un in (('2 × 1 kg', CMV['1kg'], 199.90, 99.99),
                                   ('2 × 500 g', CMV['500g'], 79.99, 44.90)):
        k1 = resultado(p_kit, 2 * cmv)['cm3']
        k2 = resultado(p_kit, 2 * cmv, itens=2)['cm3']
        av = 2 * resultado(p_un, cmv)['cm3']
        print('- %s a R$ %.2f: kit = 1 taxa %.2f · kit = 2 taxas %.2f · 2 avulsos a R$ %.2f em 2 pedidos %.2f'
              % (nome, p_kit, k1, k2, p_un, av))
    print('\nPisos de preço (CM3, sem campanha):')
    for nome, cmv, _ in SKUS:
        print('- %s: zero %s · 10%% %s · 15%% %s · 20%% %s' % (
            nome, *[preco_para_margem(m, cmv) for m in (0, 10, 15, 20)]))
    print('\nZonas mortas (cobrar mais rende menos CM3):')
    for nome, cmv, precos in SKUS:
        for d, ate, antes in zonas_mortas(cmv):
            if ate > d and min(precos) <= d <= max(precos) + 10:
                print('- %s: R$ %.2f a %.2f rende menos que R$ %.2f (CM3 %.2f)' % (nome, d, ate, d - 0.01, antes))
    print('\nEstresse no 1 kg a R$ 99,99:')
    for rot, kw in (('base', {}), ('campanha 3,5%', dict(campanha=True)),
                    ('Ads ACOS 8%', dict(ads_pct=8)), ('cupom seguidor R$ 5', dict(cupom=5)),
                    ('campanha + Ads 8% + cupom R$ 5', dict(campanha=True, ads_pct=8, cupom=5)),
                    ('vendedor CPF após 450 pedidos', dict(cpf=True)),
                    ('logística própria, desconto de frete R$ 30', dict(logistica='propria', frete_desc=30)),
                    ('Full+ −1 p.p.', dict(full_mais_pp=1))):
        r = resultado(99.99, CMV['1kg'], **kw)
        print('- %s: CM3 %.2f (%.1f%%), ROAS eq. %s' % (rot, r['cm3'], r['cm3_pct'], r['roas_eq'] or '∞'))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--preco', type=float)
    ap.add_argument('--margem', type=float, help='margem CM3 desejada (%%) → menor preço')
    ap.add_argument('--cmv', type=float, default=CMV['1kg'])
    ap.add_argument('--itens', type=int, default=1, help='taxas fixas cobradas no pedido')
    ap.add_argument('--cpf', action='store_true', help='adicional de R$ 3/item do vendedor CPF')
    ap.add_argument('--logistica', choices=('shopee', 'propria'), default='shopee')
    ap.add_argument('--frete-desc', type=float, default=0.0, help='desconto de frete do pedido (logística própria)')
    ap.add_argument('--ads', type=float, default=0.0, help='ACOS (%% do preço)')
    ap.add_argument('--cupom', type=float, default=0.0, help='cupom do vendedor em R$')
    ap.add_argument('--campanha', action='store_true', help='loja inscrita em Campanhas de Destaque (3,5%%)')
    ap.add_argument('--afiliado', type=float, default=0.0, help='comissão extra do afiliado do vendedor (%%)')
    ap.add_argument('--full-mais', type=float, default=0.0, help='desconto Full+ em p.p.')
    a = ap.parse_args(argv)
    kw = dict(itens=a.itens, cpf=a.cpf, logistica=a.logistica, frete_desc=a.frete_desc, ads_pct=a.ads,
              cupom=a.cupom, campanha=a.campanha, afiliado_pct=a.afiliado, full_mais_pp=a.full_mais)
    if a.preco is not None:
        for k, v in resultado(a.preco, a.cmv, **kw).items():
            print('%-18s %s' % (k, v))
    elif a.margem is not None:
        print(preco_para_margem(a.margem, a.cmv, **kw))
    else:
        tabela()
    return 0


if __name__ == '__main__':
    sys.exit(main())
