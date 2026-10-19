# -*- coding: utf-8 -*-
"""Precificação de anúncio no ML com o CMV real — a calculadora oficial do agente.

Fonte dos números: `mercadolivre/custos.md` (CMV informado pelo Rafael em 14/10/2026,
tarifas e fretes medidos no formulário da conta). Mudou um custo? Mude lá e aqui.

    python mercadolivre/scripts/precificar.py                 # tabela 1 kg e kit 2 kg
    python mercadolivre/scripts/precificar.py --conferir      # bate a fórmula com o ML
    python mercadolivre/scripts/precificar.py --escada        # 1 kg / 500 g / kits por faixa de envio
    python mercadolivre/scripts/precificar.py --preco 119.90 --cmv 47 --frete 34.30
    python mercadolivre/scripts/precificar.py --margem 15 --cmv 47 --frete 34.30 --tipo premium
"""
import argparse
import sys

CMV = {'1kg': 47.00, '500g': 26.00, '250g': 14.00}
IMPOSTO = 0.09                      # sobre o preço de venda
TARIFA = {'classico': 0.14, 'premium': 0.19}
FRETE_GRATIS_MIN = 79.00            # frete grátis obrigatório a partir daqui
FRETE = {'1kg': 34.30, 'kit2kg': 54.10}   # frete grátis medido, reputação vermelha


def resultado(preco, cmv, frete, tipo='classico', desconto_vendedor=0.0):
    """Quanto cada venda deixa. `desconto_vendedor` = R$ que o vendedor banca (cupom, Pix)."""
    tarifa = round(preco * TARIFA[tipo], 2)
    imposto = round(preco * IMPOSTO, 2)
    recebe_ml = round(preco - tarifa - frete - desconto_vendedor, 2)   # o "Você recebe" do ML
    lucro = round(recebe_ml - imposto - cmv, 2)
    return dict(preco=preco, tipo=tipo, tarifa=tarifa, frete=frete, imposto=imposto,
                cmv=cmv, recebe_ml=recebe_ml, lucro=lucro,
                margem=round(lucro / preco * 100, 1))


def preco_para_margem(margem_pct, cmv, frete, tipo='classico'):
    """Preço que entrega `margem_pct`% de lucro sobre o preço. 0 = ponto de equilíbrio."""
    divisor = 1 - TARIFA[tipo] - IMPOSTO - margem_pct / 100
    if divisor <= 0:
        raise ValueError('margem impossível com essa tarifa')
    return round((cmv + frete) / divisor, 2)


def teto_atacado(preco, economia_frete_un):
    """O ML obriga o atacado a repassar a economia de frete: teto = preço − economia/un."""
    return round(preco - economia_frete_un, 2)


def conferir():
    """Bate a fórmula com o 'Você recebe' lido no formulário do ML. Falhou = custo mudou."""
    medidos = [
        # (preço, frete, tipo, recebe medido, onde)
        (109.90, 34.30, 'classico', 60.21, 'Suave 1 kg MLB5903454718'),
        (219.80, 54.10, 'classico', 134.93, 'Kit 2 kg Clássico 7791312402'),
        (99.90, 28.90, 'classico', 57.01, 'Néctar Gourmet 1 kg 7791161926'),
    ]
    ok = True
    for preco, frete, tipo, esperado, onde in medidos:
        r = resultado(preco, 0, frete, tipo)
        bate = abs(r['recebe_ml'] - esperado) <= 0.01
        ok &= bate
        print('%-34s calculado %7.2f  medido %7.2f  %s' % (
            onde, r['recebe_ml'], esperado, 'OK' if bate else 'DIVERGE'))
    eq = preco_para_margem(0, CMV['1kg'], FRETE['1kg'])
    bate = abs(resultado(eq, CMV['1kg'], FRETE['1kg'])['lucro']) <= 0.02
    ok &= bate
    print('%-34s %7.2f -> lucro ~0  %s' % ('equilíbrio 1 kg Clássico', eq, 'OK' if bate else 'DIVERGE'))
    return ok


def linha(r):
    return '%8.2f %-8s %7.2f %6.2f %7.2f %6.2f %8.2f %8.2f %6.1f%%' % (
        r['preco'], r['tipo'], r['tarifa'], r['frete'], r['imposto'], r['cmv'],
        r['recebe_ml'], r['lucro'], r['margem'])


CAB = '%8s %-8s %7s %6s %7s %6s %8s %8s %7s' % (
    'preço', 'tipo', 'tarifa', 'frete', 'imposto', 'CMV', 'recebeML', 'lucro', 'margem')


def tabela_padrao():
    for nome, cmv, frete, precos in (
        ('1 kg avulso (Suave/Clássico)', CMV['1kg'], FRETE['1kg'],
         (105.58, 109.90, 114.90, 119.90, 124.90, 129.90, 134.90, 139.90)),
        ('Kit 2 x 1 kg', 2 * CMV['1kg'], FRETE['kit2kg'],
         (199.90, 219.80, 229.90, 239.90, 249.90)),
    ):
        print('\n=== %s — CMV %.2f, frete %.2f ===' % (nome, cmv, frete))
        print(CAB)
        for tipo in ('classico', 'premium'):
            for p in precos:
                print(linha(resultado(p, cmv, frete, tipo)))
        print('preço por margem:', '  '.join(
            '%s %d%%=%.2f' % (t[:4], m, preco_para_margem(m, cmv, frete, t))
            for t in ('classico', 'premium') for m in (0, 10, 15, 20)))


# --- Escada 1 kg / 500 g por faixa de envio (15/10/2026) --------------------------------
# Faixas de preço da tabela de envio (ajuda/40538). O frete grátis muda de valor ao cruzar uma.
FAIXAS = ((0, 18.99), (19, 48.99), (49, 78.99), (79, 99.99), (100, 119.99),
          (120, 149.99), (150, 199.99), (200, 10**6))

# (classe de peso, início da faixa) -> (frete, origem). M = medido no formulário/lista da conta
# (reputação vermelha); E = estimado, NÃO usar como fato — medir no formulário antes de decidir.
FRETE_FAIXA = {
    ('1kg', 79): (29.50, 'M'),     # Néctar 1 kg a 99,90, lista 15/10
    ('1kg', 100): (34.30, 'M'),    # Suave 1 kg a 109,90, formulário 15/10
    ('1kg', 120): (39.10, 'E'),    # extrapolado: +4,80 por faixa, como de 79 para 100
    ('1kg', 150): (43.90, 'E'),    # idem
    ('2kg', 200): (54.10, 'M'),    # Kit 2 kg a 219,80, formulário 11/10
    ('2x500g', 100): (34.30, 'E'),  # supõe pacote de ~1,1 kg igual ao 1 kg; medir
    ('2x500g', 120): (39.10, 'E'),
    ('500g', 49): (16.90, 'E'),    # tabela 40538 0,5–1 kg R$ 8,45 com 50% embutido, x2 no vermelho
    ('500g', 79): (28.90, 'E'),    # tabela 40538 0,5–1 kg R$ 14,45 x2 no vermelho
}


def faixa(preco):
    for ini, fim in FAIXAS:
        if ini <= preco <= fim:
            return ini
    return FAIXAS[-1][0]


ROAS_ADS = 10.0   # ROAS de partida para o CM2 (prática 8–15, fala oficial 10 [ads A24])

SKUS = (
    # nome, classe de frete, CMV, kg, preços a testar
    ('1 kg avulso', '1kg', CMV['1kg'], 1.0, (109.90, 119.90, 124.90, 129.90, 134.90, 139.90)),
    ('Kit 2 x 1 kg', '2kg', 2 * CMV['1kg'], 2.0, (219.80, 229.90, 239.80, 249.90, 259.80)),
    ('500 g avulso', '500g', CMV['500g'], 0.5, (59.90, 65.70, 69.90, 74.90, 79.90)),
    ('Kit 2 x 500 g', '2x500g', 2 * CMV['500g'], 1.0, (119.90, 124.90, 129.90)),
)


def escada():
    print('CM1 = preço − tarifa − frete − imposto 9%% − CMV (antes de Ads). ACOS eq = CM1%%;'
          ' ROAS eq = 1/ACOS. CM2 = CM1 − Ads a ROAS %.0f (ACOS %.0f%%).'
          ' Frete M = medido, E = ESTIMADO.' % (ROAS_ADS, 100 / ROAS_ADS))
    print('%-14s %8s %7s %-5s %7s %6s %7s %6s %7s %6s %7s %6s' % (
        'SKU', 'preço', 'R$/kg', 'tipo', 'frete', 'orig', 'CM1', 'CM1%', 'ROASeq', 'CM2', 'CM2%', 'eq.'))
    for nome, classe, cmv, kg, precos in SKUS:
        for p in precos:
            tipo = 'premium' if p >= 150 else 'classico'
            fr = FRETE_FAIXA.get((classe, faixa(p)))
            if fr is None:
                print('%-14s %8.2f  — frete da faixa %s sem medida nem estimativa' % (nome, p, faixa(p)))
                continue
            frete, orig = fr
            r = resultado(p, cmv, frete, tipo)
            cm1 = r['lucro']
            roas_eq = (p / cm1) if cm1 > 0 else float('inf')
            cm2 = round(cm1 - p / ROAS_ADS, 2)
            eq = preco_para_margem(0, cmv, frete, tipo)
            print('%-14s %8.2f %7.2f %-5s %7.2f %6s %7.2f %5.1f%% %7.1f %6.2f %5.1f%% %6.2f' % (
                nome, p, p / kg, tipo[:5], frete, orig, cm1, r['margem'],
                roas_eq, cm2, cm2 / p * 100, eq))
        print()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--conferir', action='store_true')
    ap.add_argument('--escada', action='store_true', help='1 kg, kit 2 kg, 500 g e kit 2x500 g por faixa de envio')
    ap.add_argument('--preco', type=float)
    ap.add_argument('--margem', type=float)
    ap.add_argument('--cmv', type=float, default=CMV['1kg'])
    ap.add_argument('--frete', type=float, default=FRETE['1kg'])
    ap.add_argument('--tipo', choices=TARIFA, default='classico')
    ap.add_argument('--desconto', type=float, default=0.0, help='R$ bancado pelo vendedor')
    a = ap.parse_args(argv)
    if a.conferir:
        return 0 if conferir() else 1
    if a.escada:
        escada()
        return 0
    if a.preco is not None:
        print(CAB)
        print(linha(resultado(a.preco, a.cmv, a.frete, a.tipo, a.desconto)))
        return 0
    if a.margem is not None:
        print('%.2f' % preco_para_margem(a.margem, a.cmv, a.frete, a.tipo))
        return 0
    tabela_padrao()
    return 0


if __name__ == '__main__':
    sys.exit(main())
