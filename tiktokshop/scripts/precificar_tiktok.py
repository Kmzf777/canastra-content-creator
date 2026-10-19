# -*- coding: utf-8 -*-
"""Precificação no TikTok Shop BR com o CMV real, em escada CM1 → CM2 → CM3.

Fontes das constantes (conferidas contra pesquisa-marketplaces/tiktokshop/CONSOLIDADO.md §0, §1.1 e
§6.3 em 16/10/2026; nenhuma medida ainda num pedido da Canastra):

- Tarifa da plataforma, vigente desde 15/07/2026 — Academy BR kid=24428156307201 (atualizada 12/06/2026):
  abaixo de R$ 50: 10% + R$ 4 POR ITEM; de R$ 50 em diante: 6% + R$ 6 POR ITEM. Base = preço depois do
  desconto do VENDEDOR (cupom do vendedor reduz a base e pode mudar a faixa); o desconto bancado pela
  plataforma não entra. Igual para todas as categorias.
- Programa de Taxas de Envio (SFP) — kid=5665577566734097 (31/08/2026): 6% do preço depois do desconto
  do vendedor e antes do subsídio da plataforma, teto de R$ 50 por produto, só em pedido entregue; não
  volta em devolução de pedido enviado. Com o SFP o frete grátis ao comprador é coberto (o vendedor não
  paga frete à parte no Envio pelo TikTok). Amostra fica FORA do SFP (frete da amostra é do vendedor).
- Comissão de afiliado — padrão da colaboração aberta em Alimentos e bebidas: 8% (kid=3355295847515925,
  vigência 23/09/2026). Base = preço pago + reembolso do subsídio da plataforma (kid=1517752301717265),
  ou seja, o preço depois do desconto do vendedor.
- Loja nova: 0% de comissão por 60 dias, teto de R$ 17 mil de economia, com missão (kid=24428156307201).
  A página fala só em "taxa de comissão": se cobre a parte fixa e o SFP está ABERTO. `--loja-nova` zera só
  a parte percentual; `--loja-nova-fixa` zera também a fixa (otimista).
- GMV Max: custo = GMV ÷ ROI. Em campanha da plataforma sem forma de pagamento, a plataforma cria o
  anúncio com ROI 50 (= 2% do pedido) — kid=3355910447433489 (19/05/2026). O ROI do painel inclui pedidos
  orgânicos e de afiliado (OFICIAL, global): o ROI de equilíbrio daqui é o do pedido marginal.
- Amostra: produto + frete 100% do vendedor (kid=6589441682917136).
- CMV e imposto (9% sobre o preço de venda): mercadolivre/custos.md (fonte única).

NÃO MEDIDO (hipóteses que o script deixa explícitas, todas ajustáveis por argumento):
- "Por item" = unidade, SKU ou kit? Nenhuma página diz (CONSOLIDADO §1.1, "SEM FONTE (aberto)").
  O padrão trata o kit como 1 item (1 tarifa fixa, faixa pelo preço do kit). `--itens N` simula o kit
  pagando N tarifas fixas, com a faixa de cada item pelo preço do kit ÷ N.
- Frete de amostra (`--frete-amostra`, padrão R$ 20) e quantos pedidos cada amostra gera
  (`--pedidos-por-amostra`, padrão 10). A amostra é o 1 kg ou o 500 g inteiro, pelo CMV.
- Perdas (avaria, extravio, reembolso sem devolução que a plataforma não cubra, 6% do SFP perdido em
  devolução): `--perda`, padrão 1% do preço.
- Embalagem de envio (caixa, fita, etiqueta): `--embalagem`, padrão R$ 0 (não informada em custos.md).

Escada:
    CM1 = receita − CMV − tarifa (% + fixa) − SFP − imposto − embalagem      (receita = preço − cupom)
    CM2 = CM1 − afiliado − GMV Max
    CM3 = CM2 − amostra rateada − perdas

    python tiktokshop/scripts/precificar_tiktok.py                         # tabela da entrada
    python tiktokshop/scripts/precificar_tiktok.py --preco 89.90 --cmv 47
    python tiktokshop/scripts/precificar_tiktok.py --preco 89.90 --cmv 47 --afiliado 8 --roi 6 --cupom 5
    python tiktokshop/scripts/precificar_tiktok.py --margem 15 --cmv 47 --afiliado 8
"""
import argparse
import sys

IMPOSTO = 0.09   # sobre o preço de venda (mercadolivre/custos.md)
CMV = {'1kg': 47.00, '500g': 26.00, '250g': 14.00}

# (preço mínimo da faixa, comissão %, tarifa fixa por item) — kid=24428156307201, vigência 15/07/2026
FAIXAS = [(0.00, 0.10, 4.00), (50.00, 0.06, 6.00)]
SFP_PCT, SFP_TETO = 0.06, 50.00            # kid=5665577566734097
AFILIADO_PADRAO = 8.0                      # % — Alimentos e bebidas, kid=3355295847515925
ROI_CAMPANHA = 50.0                        # GMV Max criado pela plataforma em campanha (2%), kid=3355910447433489
TETO_LOJA_NOVA = 17000.00                  # R$ de comissão isenta em 60 dias, kid=24428156307201

# hipóteses NÃO MEDIDAS (padrões; mude por argumento)
FRETE_AMOSTRA = 20.00
PEDIDOS_POR_AMOSTRA = 10
PERDA_PCT = 1.0
EMBALAGEM = 0.00


def faixa(preco_item):
    for minimo, pct, fixa in reversed(FAIXAS):
        if preco_item >= minimo:
            return pct, fixa
    raise ValueError(preco_item)


def resultado(preco, cmv, itens=1, cupom=0.0, afiliado_pct=0.0, roi=None, loja_nova=False,
              loja_nova_fixa=False, frete_amostra=FRETE_AMOSTRA, pedidos_por_amostra=PEDIDOS_POR_AMOSTRA,
              cmv_amostra=None, perda_pct=PERDA_PCT, embalagem=EMBALAGEM):
    """Escada de margem de UM pedido de um anúncio de preço `preco` (um kit é um anúncio).

    `itens` = quantas tarifas fixas o pedido paga (1 = kit conta como 1 item, a hipótese padrão).
    `roi` = ROI do GMV Max atribuído a este pedido (None = sem Ads).
    """
    receita = round(preco - cupom, 2)                 # base da tarifa, do SFP e do afiliado
    pct, fixa = faixa(receita / itens)
    if loja_nova:
        pct = 0.0
    tarifa_pct = round(receita * pct, 2)
    tarifa_fixa = 0.0 if loja_nova_fixa else round(fixa * itens, 2)
    sfp = round(min(receita * SFP_PCT, SFP_TETO * itens), 2)
    imposto = round(receita * IMPOSTO, 2)
    cm1 = round(receita - cmv - tarifa_pct - tarifa_fixa - sfp - imposto - embalagem, 2)
    afil = round(receita * afiliado_pct / 100, 2)
    ads = round(receita / roi, 2) if roi else 0.0
    cm2 = round(cm1 - afil - ads, 2)
    cmv_a = cmv if cmv_amostra is None else cmv_amostra
    amostra = round((cmv_a + frete_amostra) / pedidos_por_amostra, 2) if pedidos_por_amostra else 0.0
    perda = round(receita * perda_pct / 100, 2)
    cm3 = round(cm2 - amostra - perda, 2)
    antes_ads = cm1 - afil - amostra - perda          # o que sobra para pagar GMV Max
    return dict(preco=preco, cupom=cupom, receita=receita, tarifa_pct=tarifa_pct, tarifa_fixa=tarifa_fixa,
                sfp=sfp, imposto=imposto, cmv=cmv, embalagem=embalagem, cm1=cm1,
                cm1_pct=round(cm1 / receita * 100, 1), afiliado=afil, gmv_max=ads, cm2=cm2,
                cm2_pct=round(cm2 / receita * 100, 1), amostra=amostra, perda=perda, cm3=cm3,
                cm3_pct=round(cm3 / receita * 100, 1),
                plataforma_pct=round((tarifa_pct + tarifa_fixa + sfp) / receita * 100, 1),
                roi_eq=round(receita / antes_ads, 2) if antes_ads > 0 else None)


def preco_para_margem(margem_pct, cmv, **kw):
    """Menor preço cuja CM3 atinge a margem pedida, varrendo de centavo em centavo."""
    p = 10.00
    while p < 1500:
        if resultado(round(p, 2), cmv, **kw)['cm3_pct'] >= margem_pct:
            return round(p, 2)
        p += 0.01
    return None


# (nome, CMV do anúncio, kg, preços a testar, CMV da amostra que se manda)
SKUS = [
    ('1 kg', CMV['1kg'], 1.0, (69.90, 79.90, 89.90, 99.90, 109.90, 119.90), CMV['1kg']),
    ('500 g', CMV['500g'], 0.5, (39.90, 44.90, 49.90, 54.90, 59.90, 64.90), CMV['500g']),
    ('Kit 2 × 500 g', 2 * CMV['500g'], 1.0, (79.90, 89.90, 99.90, 109.90), CMV['500g']),
    ('Kit 2 × 1 kg', 2 * CMV['1kg'], 2.0, (159.90, 179.90, 199.90, 219.90), CMV['1kg']),
    ('Kit 3 × 500 g', 3 * CMV['500g'], 1.5, (119.90, 134.90, 149.90), CMV['500g']),
]

CENARIOS = [
    ('orgânico (conta própria)', dict()),
    ('afiliado 8%', dict(afiliado_pct=AFILIADO_PADRAO)),
    ('afiliado 8% + campanha (ROI 50)', dict(afiliado_pct=AFILIADO_PADRAO, roi=ROI_CAMPANHA)),
]


def _fmt(v):
    return 'sem margem' if v is None else '%.2f' % v


def tabela():
    print('Escada de margem por pedido — TikTok Shop BR, tarifa de 15/07/2026, SFP 6%, imposto 9%.')
    print('Hipóteses NÃO MEDIDAS: kit = 1 item; amostra (CMV + R$ %.2f de frete) a cada %d pedidos; '
          'perda %.1f%%; embalagem R$ %.2f.\n' % (FRETE_AMOSTRA, PEDIDOS_POR_AMOSTRA, PERDA_PCT, EMBALAGEM))
    print('| SKU | preço | R$/kg | tarifa+SFP | % plataf. | CM1 | CM1% | CM2 afil. 8% | CM3 afil. 8% | CM3% '
          '| ROI eq. (sem afil.) | ROI eq. (afil. 8%) |')
    print('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for nome, cmv, kg, precos, cmv_a in SKUS:
        for p in precos:
            o = resultado(p, cmv, cmv_amostra=cmv_a)
            a = resultado(p, cmv, afiliado_pct=AFILIADO_PADRAO, cmv_amostra=cmv_a)
            print('| %s | %.2f | %.2f | %.2f | %.1f%% | %.2f | %.1f%% | %.2f | %.2f | %.1f%% | %s | %s |' % (
                nome, p, p / kg, o['tarifa_pct'] + o['tarifa_fixa'] + o['sfp'], o['plataforma_pct'],
                o['cm1'], o['cm1_pct'], a['cm2'], a['cm3'], a['cm3_pct'], _fmt(o['roi_eq']), _fmt(a['roi_eq'])))

    print('\nKit × avulso (CM1 por pedido; a dúvida "por item" decide):')
    for nome, cmv, p_kit, p_un, n in (('2 × 1 kg', CMV['1kg'], 179.90, 89.90, 2),
                                      ('2 × 500 g', CMV['500g'], 89.90, 44.90, 2),
                                      ('3 × 500 g', CMV['500g'], 134.90, 44.90, 3)):
        k1 = resultado(p_kit, n * cmv)['cm1']
        kn = resultado(p_kit, n * cmv, itens=n)['cm1']
        av = n * resultado(p_un, cmv)['cm1']
        print('- %s a R$ %.2f: kit = 1 tarifa fixa %.2f · kit = %d tarifas %.2f · %d avulsos a R$ %.2f em %d pedidos %.2f'
              % (nome, p_kit, k1, n, kn, n, p_un, n, av))

    print('\nPisos de preço (CM3 com afiliado de 8%, sem Ads):')
    for nome, cmv, _, _, cmv_a in SKUS:
        print('- %s: zero %s · 10%% %s · 15%% %s · 20%% %s' % (
            nome, *[preco_para_margem(m, cmv, afiliado_pct=AFILIADO_PADRAO, cmv_amostra=cmv_a)
                    for m in (0, 10, 15, 20)]))
    print('\nPisos de preço (CM3 só conta própria, sem afiliado e sem Ads):')
    for nome, cmv, _, _, cmv_a in SKUS:
        print('- %s: zero %s · 10%% %s · 15%% %s · 20%% %s' % (
            nome, *[preco_para_margem(m, cmv, cmv_amostra=cmv_a) for m in (0, 10, 15, 20)]))

    print('\nEstresse no 1 kg a R$ 89,90:')
    for rot, kw in (('orgânico', {}),
                    ('loja nova (0% da parte %, fixa e SFP mantidas)', dict(loja_nova=True)),
                    ('loja nova cobrindo também a fixa (otimista)', dict(loja_nova=True, loja_nova_fixa=True)),
                    ('afiliado 8%', dict(afiliado_pct=8)),
                    ('afiliado 12%', dict(afiliado_pct=12)),
                    ('afiliado 8% + campanha ROI 50', dict(afiliado_pct=8, roi=ROI_CAMPANHA)),
                    ('afiliado 8% + GMV Max ROI 8', dict(afiliado_pct=8, roi=8)),
                    ('afiliado 8% + GMV Max ROI 5', dict(afiliado_pct=8, roi=5)),
                    ('cupom do vendedor R$ 10 + afiliado 8%', dict(cupom=10, afiliado_pct=8)),
                    ('amostra a cada 3 pedidos', dict(pedidos_por_amostra=3)),
                    ('perda 5%', dict(perda_pct=5))):
        r = resultado(89.90, CMV['1kg'], **kw)
        print('- %s: CM1 %.2f · CM3 %.2f (%.1f%%) · ROI eq. %s' % (rot, r['cm1'], r['cm3'], r['cm3_pct'], _fmt(r['roi_eq'])))

    economia = resultado(89.90, CMV['1kg'])['tarifa_pct']
    print('\nIsenção de loja nova: a R$ 89,90, a parte %% isenta é R$ %.2f por pedido; o teto de R$ %.0f '
          'seria atingido em %d pedidos (mais que 60 dias × 50 pedidos/dia do nível Iniciante = 3.000).'
          % (economia, TETO_LOJA_NOVA, TETO_LOJA_NOVA / economia))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--preco', type=float)
    ap.add_argument('--margem', type=float, help='margem CM3 desejada (%%) → menor preço')
    ap.add_argument('--cmv', type=float, default=CMV['1kg'])
    ap.add_argument('--itens', type=int, default=1, help='tarifas fixas cobradas no pedido (kit por unidade)')
    ap.add_argument('--cupom', type=float, default=0.0, help='cupom/desconto do vendedor em R$')
    ap.add_argument('--afiliado', type=float, default=0.0, help='comissão de afiliado (%%)')
    ap.add_argument('--roi', type=float, default=None, help='ROI do GMV Max (GMV ÷ custo); 50 = campanha')
    ap.add_argument('--loja-nova', action='store_true', help='0%% da parte percentual da tarifa (60 dias)')
    ap.add_argument('--loja-nova-fixa', action='store_true', help='isenção cobre também a tarifa fixa (otimista)')
    ap.add_argument('--frete-amostra', type=float, default=FRETE_AMOSTRA)
    ap.add_argument('--pedidos-por-amostra', type=float, default=PEDIDOS_POR_AMOSTRA)
    ap.add_argument('--cmv-amostra', type=float, default=None, help='CMV do que vai como amostra (padrão: o anúncio)')
    ap.add_argument('--perda', type=float, default=PERDA_PCT, help='perdas em %% do preço')
    ap.add_argument('--embalagem', type=float, default=EMBALAGEM, help='embalagem de envio em R$ por pedido')
    a = ap.parse_args(argv)
    kw = dict(itens=a.itens, cupom=a.cupom, afiliado_pct=a.afiliado, roi=a.roi, loja_nova=a.loja_nova,
              loja_nova_fixa=a.loja_nova_fixa, frete_amostra=a.frete_amostra,
              pedidos_por_amostra=a.pedidos_por_amostra, cmv_amostra=a.cmv_amostra, perda_pct=a.perda,
              embalagem=a.embalagem)
    if a.preco is not None:
        for k, v in resultado(a.preco, a.cmv, **kw).items():
            print('%-15s %s' % (k, v))
    elif a.margem is not None:
        print(preco_para_margem(a.margem, a.cmv, **kw))
    else:
        tabela()
    return 0


if __name__ == '__main__':
    sys.exit(main())
