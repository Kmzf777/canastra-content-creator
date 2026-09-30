# -*- coding: utf-8 -*-
"""Recálculo com os custos de envio REAIS da conta Canastra.

Fonte dos custos de envio: coluna "A pagar" da Central de Vendedores, lida em
28/09/2026. Substitui as estimativas de blog que estavam em uso.

Observado na conta (cápsulas):
  comprador paga  : 10un@18,70 -> 1,40 | 40un@40,00 -> 2,40 | 40un@83,10 -> 4,80
  frete grátis    : 10un@28,90 -> 14,45 | 60un@109,99 -> 29,90 / 33,70 / 34,30
"""
CPV_CAIXA = 15.10


def envio_comprador_paga(preco):
    """~6% do preço, calibrado em 1,40@18,70 / 2,40@40 / 4,80@83,10."""
    return round(preco * 0.06, 2)


def envio_gratis(caixas):
    """Observado na conta, por tamanho de kit."""
    if caixas <= 1:
        return 14.45          # medido: 10un @ 28,90
    if caixas <= 4:
        return 20.00          # interpolado entre 14,45 e 29,90 — A CONFIRMAR
    return 32.00              # medido: 60un @ 109,99 deu 29,90–34,30


def linha(caixas, preco, comissao=14, frete_gratis=None, dias=60):
    caps = caixas * 10
    if frete_gratis is None:
        frete_gratis = preco >= 79
    com = preco * comissao / 100
    env = envio_gratis(caixas) if frete_gratis else envio_comprador_paga(preco)
    cpv = caixas * CPV_CAIXA
    arm = (0.007 if caixas <= 2 else 0.015) * dias
    lucro = preco - com - env - cpv - arm
    return dict(caps=caps, preco=preco, rs_cap=preco / caps, com=com, env=env,
                cpv=cpv, arm=arm, lucro=lucro, margem=lucro / preco * 100,
                fg=frete_gratis)


def mostra(titulo, linhas):
    print('\n=== %s ===' % titulo)
    print('%5s %8s %7s %8s %8s %8s %8s %7s %6s' %
          ('caps', 'preco', 'R$/cap', 'comis', 'envio', 'CPV', 'lucro', 'margem', 'frete'))
    for r in linhas:
        print('%5d %8.2f %7.2f %8.2f %8.2f %8.2f %8.2f %6.1f%% %6s' % (
            r['caps'], r['preco'], r['rs_cap'], r['com'], r['env'], r['cpv'],
            r['lucro'], r['margem'], 'GRATIS' if r['fg'] else 'compr.'))


mostra('10 un - comprador paga o frete',
       [linha(1, p, frete_gratis=False) for p in (28.90, 32.90, 34.90, 36.90)])
mostra('40 un - frete gratis obrigatorio',
       [linha(4, p) for p in (119.90, 129.90, 139.90, 149.90)])
mostra('60 un - frete gratis obrigatorio',
       [linha(6, p) for p in (179.90, 189.90, 199.90, 209.90)])

print('\n=== PRECO PARA 25%% E 30%% DE MARGEM ===')
for cx in (1, 4, 6):
    for alvo in (25, 30):
        lo, hi = 10.0, 900.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if linha(cx, mid)['margem'] < alvo:
                lo = mid
            else:
                hi = mid
        print('%3d caps: %d%% de margem exige R$ %7.2f  (R$ %.2f/cap)' % (
            cx * 10, alvo, hi, hi / (cx * 10)))

print('\n=== COMPARADO COM O QUE EU TINHA DITO (estimativa de blog) ===')
antigos = {40: (129.90, 27.3), 60: (179.90, 26.8), 10: (32.90, 18.9)}
for cx, caps in ((1, 10), (4, 40), (6, 60)):
    preco, margem_antiga = antigos[caps]
    r = linha(cx, preco, frete_gratis=(caps != 10))
    print('%3d caps R$%.2f: eu disse %.1f%% | real %.1f%% | diferenca %+.1f pontos' % (
        caps, preco, margem_antiga, r['margem'], r['margem'] - margem_antiga))

print('\n=== ROAS OBJETIVO (ACOS = metade da margem) ===')
for cx, p in ((1, 34.90), (4, 139.90), (6, 199.90)):
    r = linha(cx, p, frete_gratis=(cx != 1))
    acos = r['margem'] / 2
    print('%3d caps R$%.2f -> margem %.1f%% | ACOS teto %.1f%% | ROAS %.1fx | banda %.1f-%.1fx' % (
        r['caps'], p, r['margem'], acos, 100 / acos, 100 / acos * 0.8, 100 / acos * 1.2))
