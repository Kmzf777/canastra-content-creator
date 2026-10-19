# -*- coding: utf-8 -*-
"""Precificação de café na Amazon Brasil com o CMV real — escada CM1/CM2, ACOS e ROAS de equilíbrio.

Reescrito em 15/10/2026. A versão anterior usava tarifas afirmadas em vídeo e um FBA "suposto" de
R$ 15; esta usa a tabela de /precos lida no DOM e conferida contra as tarifas que a própria conta
mostra em "Gerenciar todo o inventário" (ver `amazon/02-auditoria-2026-10.md` §1).

CMV e imposto vêm de `mercadolivre/custos.md` (fonte única), pelo `mercadolivre/scripts/precificar.py`.

    python amazon/scripts/precificar_amazon.py                       # tabela padrão (1 kg e 500 g)
    python amazon/scripts/precificar_amazon.py --preco 119.90 --sku 1kg
    python amazon/scripts/precificar_amazon.py --preco 69.90 --sku 500g --programa nenhum
    python amazon/scripts/precificar_amazon.py --margem 15 --sku 1kg --ads 3.5
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'mercadolivre', 'scripts'))
from precificar import CMV as CMV_ML, IMPOSTO  # noqa: E402

CMV = dict(CMV_ML, kit2x1kg=2 * CMV_ML['1kg'], kit2x500g=2 * CMV_ML['500g'])

# Peso de envio por unidade (kg), ANTES dos 20 g de embalagem que a Amazon soma.
# NÃO MEDIDO: peso real e dimensões do pacote não foram pesados. O peso cúbico (C×L×A÷6000) pode
# passar o real se a embalagem for grande. Troque quando pesar/medir e anote a data.
PESO_KG = {'1kg': 1.05, '500g': 0.53, '250g': 0.27, 'kit2x1kg': 2.12, 'kit2x500g': 1.08}

# ── Comissão: "Comidas e bebidas" 10%, mínimo R$ 1 (venda.amazon.com.br/precos, comissões de 20/01/2025)
COMISSAO = 0.10
COMISSAO_MIN = 1.00

# ── Programas de pagamento (sobre o preço, itens a partir de R$ 40). Excludentes entre si.
#    Mais Vantagens: 1,5% promocional até 30/10/2026, 2,5% a partir de 31/10/2026; Pix 5% pago pela Amazon
#    (vendedor recebe o cheio). Vantagens: 1,5%. Parcelamento sem juros: 1,5%.
#    Fontes: sellercentral .../GR467L2LLXHTQMYP e /precos, lidas em 15/10/2026 (CONSOLIDADO §1, §8).
PROGRAMAS = {'nenhum': 0.0, 'parcelamento': 0.015, 'vantagens': 0.015,
             'mais_vantagens': 0.025, 'mais_vantagens_promo': 0.015}
PROGRAMA_MIN_PRECO = 40.0

# ── Tarifa de logística FBA, tabela padrão (/precos, "atualizadas em 01/08/2025", lida no DOM em 15/10/2026).
# Abaixo de R$ 79 a tarifa é FIXA, independente do peso: a página mostra os três valores numa célula
# mesclada, e a conta confirma — drip 10 un. (~R$ 31,90, leve) paga R$ 5,85 (Gerenciar inventário, 15/10/2026).
FBA_ABAIXO_79 = [(30.00, 5.65), (50.00, 5.85), (79.00, 6.05)]   # (preço até, tarifa)
FAIXAS_79 = [100.00, 120.00, 150.00, 200.00, float('inf')]     # R$79–99,99 | 100–119,99 | 120–149,99 | 150–199,99 | 200+
FBA_TABELA = [  # (peso até kg, [tarifa por faixa de preço a partir de R$ 79])
    (0.1, [10.05, 12.05, 14.05, 15.05, 15.55]),
    (0.2, [10.45, 12.45, 14.45, 15.45, 16.05]),
    (0.3, [10.95, 12.95, 14.95, 15.95, 16.55]),
    (0.4, [11.45, 13.45, 15.45, 16.95, 17.15]),
    (0.5, [11.95, 13.95, 15.95, 17.05, 17.85]),
    (0.75, [12.05, 14.05, 16.05, 18.45, 18.55]),
    (1.0, [12.45, 14.45, 16.45, 19.05, 19.25]),
    (1.5, [12.95, 14.95, 16.95, 19.45, 20.35]),
    (2.0, [13.05, 15.05, 17.05, 19.95, 21.35]),
    (3.0, [14.05, 16.05, 18.05, 20.05, 22.35]),
    (4.0, [15.05, 17.05, 19.05, 21.95, 23.35]),
    (5.0, [16.05, 18.05, 20.05, 22.95, 24.35]),
]
# Conferência na conta (15/10/2026): kit 30 drip (~R$ 89,90, faixa 500–750 g) paga R$ 12,05 = linha 0,75 kg. Bate.

# ── Experimente FBA 3.0 (venda.amazon.com.br/termos/experimente-fba, 01/07/2026 a 31/01/2027):
#    R$ 6/un. a partir de R$ 79; coleta e armazenagem R$ 0. Condição: gasto efetivo em Ads >= 3,5% da
#    receita dos 30 dias anteriores, OU (conta ativada no FBA antes de 01/04/2026) +1 p.p. sobre abril/2026.
#    Validação no dia 20; última em 20/12/2026.
EXPERIMENTE_TARIFA = 6.00
EXPERIMENTE_PRECO_MIN = 79.00
EXPERIMENTE_ADS_MIN = 0.035


def comissao(preco):
    return max(preco * COMISSAO, COMISSAO_MIN)


def tarifa_fba_padrao(preco, peso_kg):
    """Tabela padrão de /precos. Peso cobrado = peso informado + 20 g."""
    if preco < 79.00:
        return next(t for teto, t in FBA_ABAIXO_79 if preco < teto)
    p = peso_kg + 0.020
    col = next(i for i, teto in enumerate(FAIXAS_79) if preco < teto)
    for teto_peso, linha in FBA_TABELA:
        if p <= teto_peso:
            return linha[col]
    raise ValueError('peso acima de 5 kg: estenda FBA_TABELA a partir de /precos')


def resultado(preco, sku, ads=0.0, programa='mais_vantagens', experimente=None):
    """Escada por venda. `ads` = gasto em Ads ÷ receita (TACOS), fração.
    `experimente`: None = aplica R$ 6 só se preço >= R$ 79 E ads >= 3,5%; True/False força."""
    peso = PESO_KG[sku]
    padrao = tarifa_fba_padrao(preco, peso)
    if experimente is None:
        experimente = preco >= EXPERIMENTE_PRECO_MIN and ads >= EXPERIMENTE_ADS_MIN
    fba = EXPERIMENTE_TARIFA if (experimente and preco >= EXPERIMENTE_PRECO_MIN) else padrao
    com = comissao(preco)
    prog = preco * PROGRAMAS[programa] if preco >= PROGRAMA_MIN_PRECO else 0.0
    imp = preco * IMPOSTO
    cmv = CMV[sku]
    cm1 = preco - cmv - com - fba - imp - prog
    ad = preco * ads
    cm2 = cm1 - ad
    acos_eq = cm1 / preco
    return dict(preco=preco, sku=sku, cmv=cmv, comissao=round(com, 2), fba=fba, fba_padrao=padrao,
                imposto=round(imp, 2), programa=round(prog, 2), cm1=round(cm1, 2),
                cm1_pct=round(cm1 / preco * 100, 1), ads=round(ad, 2), cm2=round(cm2, 2),
                cm2_pct=round(cm2 / preco * 100, 1), acos_eq=round(acos_eq * 100, 1),
                roas_eq=round(1 / acos_eq, 2) if acos_eq > 0 else None,
                preco_kg=round(preco / {'1kg': 1, '500g': .5, '250g': .25, 'kit2x1kg': 2, 'kit2x500g': 1}[sku], 2))


def preco_para_margem(m, sku, ads=0.0, programa='mais_vantagens', experimente=None):
    """Menor preço (passo R$ 0,10) com CM2 >= m% — a tarifa muda de degrau em R$ 79, 100, 120…"""
    p = 20.0
    while p < 1000:
        if resultado(round(p, 2), sku, ads, programa, experimente)['cm2_pct'] >= m:
            return round(p, 2)
        p += 0.10
    return None


def tabela():
    print('Programa: Mais Vantagens 2,5% (vale a partir de 31/10/2026). Peso NÃO MEDIDO (PESO_KG).\n')
    print('| SKU | preço | R$/kg | FBA | comissão | imposto | M.Vant. | CMV | **CM1** | CM1% | ACOS eq. | ROAS eq. | Ads 3,5% → CM2 | CM2% |')
    print('|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    casos = [('1kg', p) for p in (99.90, 109.90, 119.90, 129.90)] + \
            [('500g', p) for p in (59.90, 69.90, 79.90)] + [('kit2x500g', 119.90), ('kit2x1kg', 219.90)]
    for sku, p in casos:
        sem = resultado(p, sku, ads=0.0)
        com = resultado(p, sku, ads=0.035)
        fba = 'R$ %.2f' % sem['fba'] + (' (Exp. R$ 6)' if com['fba'] != sem['fba'] else '')
        print('| %s | %.2f | %.2f | %s | %.2f | %.2f | %.2f | %.2f | **%.2f** | %.1f%% | %.1f%% | %.2f | %.2f | %.1f%% |' % (
            sku, p, sem['preco_kg'], fba, sem['comissao'], sem['imposto'], sem['programa'], sem['cmv'],
            sem['cm1'], sem['cm1_pct'], sem['acos_eq'], sem['roas_eq'] or 0, com['cm2'], com['cm2_pct']))
    print('\nCM1 sem Ads usa a tarifa padrão; a coluna "Ads 3,5%" aplica o Experimente FBA (R$ 6) quando preço >= R$ 79.')
    print('CM3 (armazenagem, remoção, devolução) fora: no Experimente FBA a armazenagem é R$ 0 até 31/01/2027.')
    print('\nPreço para CM2 de 15%% com Ads de 3,5%%: 1 kg R$ %s · 500 g R$ %s' % (
        preco_para_margem(15, '1kg', 0.035), preco_para_margem(15, '500g', 0.035)))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--preco', type=float)
    ap.add_argument('--margem', type=float, help='CM2 alvo, %%')
    ap.add_argument('--sku', choices=sorted(PESO_KG), default='1kg')
    ap.add_argument('--ads', type=float, default=0.0, help='TACOS, %%')
    ap.add_argument('--programa', choices=sorted(PROGRAMAS), default='mais_vantagens')
    a = ap.parse_args(argv)
    if a.preco is not None:
        print(resultado(a.preco, a.sku, a.ads / 100, a.programa))
    elif a.margem is not None:
        print(preco_para_margem(a.margem, a.sku, a.ads / 100, a.programa))
    else:
        tabela()


if __name__ == '__main__':
    main()
