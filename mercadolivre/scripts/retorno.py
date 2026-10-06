# -*- coding: utf-8 -*-
"""Nossos precos x concorrencia x promocao x Ads x retorno.

MEDIDO no formulario do ML em 30/09/2026, Classico, Full:
  Comissao Classico 14% | Premium 19%
  Caixa 10 @ 34,90 -> comprador paga envio: vendedor paga R$ 2,40
  Kit 40  @ 139,90 -> frete gratis: vendedor paga R$ 14,45
                      (comprador paga custaria R$ 7,20 -- nao aplicado)
  CPV com impostos: R$ 15,10/caixa | R$ 60,40/kit

CONCORRENCIA (busca logada 25/09/2026, R$/capsula):
  generico em kit 1,40-1,56 | massa 1,44-2,00
  ESPECIAL 2,29-3,14 <- onde competimos
  premium/importado 3,44-4,20
  "Serra Canastra" de terceiro: 3,80-5,03
"""
COM = 0.14
CPV_C, CPV_K = 15.10, 60.40
ENV_C, ENV_K = 2.40, 14.45      # medidos


def lucro_c(p, env=ENV_C):
    return p - p*COM - env - CPV_C


def lucro_k(p, env=ENV_K):
    return p - p*COM - env - CPV_K


print('=' * 92)
print('NOSSOS ANUNCIOS — aplicado em 30/09')
print('=' * 92)
print('%-26s %9s %9s %9s %9s %9s %9s' % (
    'anuncio', 'preco', 'R$/cap', 'comissao', 'envio', 'lucro', 'margem'))
for nome, p, f in [('Caixa 10 (3 anuncios)', 34.90, 'c'), ('Kit 40 (4 anuncios)', 139.90, 'k')]:
    l = lucro_c(p) if f == 'c' else lucro_k(p)
    n = 10 if f == 'c' else 40
    env = ENV_C if f == 'c' else ENV_K
    print('%-26s %9.2f %9.2f %9.2f %9.2f %9.2f %8.1f%%' % (
        nome, p, p/n, p*COM, env, l, l/p*100))

print('\n' + '=' * 92)
print('ONDE ISSO NOS COLOCA (R$/capsula)')
print('=' * 92)
ref = [('Generico em kit (Italle, Capresso)', 1.40, 1.56),
       ('Massa (Pilao, 3 Coracoes, Nescafe)', 1.44, 2.00),
       ('ESPECIAL (Orfeu, Coffee++, Sebastian)', 2.29, 3.14),
       ('Premium/importado (Nespresso, Illy)', 3.44, 4.20),
       ('"Serra Canastra" de terceiro', 3.80, 5.03)]
for nome, a, b in ref:
    print('  %-40s %4.2f - %4.2f' % (nome, a, b))
print()
print('  %-40s %4.2f  (caixa cheia)' % ('NOSSO', 3.49))
print('  %-40s %4.2f  (kit cheio)' % ('NOSSO', 3.50))
print('  %-40s %4.2f  (caixa em promo 28,90)' % ('NOSSO', 2.89))
print('  %-40s %4.2f  (kit em promo 124,90)' % ('NOSSO', 3.12))

print('\n' + '=' * 92)
print('PROMOCAO — o que custa cada degrau')
print('=' * 92)
print('BLOQUEADA ate a reputacao virar verde ou amarela (Central de promocoes: 0 anuncios).')
print()
print('%-10s %9s %9s %9s %9s  %s' % ('preco', 'R$/cap', 'lucro', 'margem', 'vs cheio', 'posicao'))
print('  CAIXA DE 10')
for p, nota in [(34.90, 'cheio'), (31.90, ''), (29.90, ''),
                (28.90, 'empata Coffee++'), (27.90, 'empata Orfeu Classico')]:
    l = lucro_c(p)
    print('  %-8.2f %9.2f %9.2f %8.1f%% %9.2f  %s' % (
        p, p/10, l, l/p*100, l - lucro_c(34.90), nota))
print('  KIT DE 40')
for p, nota in [(139.90, 'cheio'), (134.90, ''), (129.90, ''),
                (124.90, 'empata kit 50 do Orfeu (3,14)')]:
    l = lucro_k(p)
    print('  %-8.2f %9.2f %9.2f %8.1f%% %9.2f  %s' % (
        p, p/40, l, l/p*100, l - lucro_k(139.90), nota))

print('\n' + '=' * 92)
print('ADS — quanto cada venda aguenta')
print('=' * 92)
MIX_C = 0.55
for nome, pc, pk in [('preco cheio', 34.90, 139.90), ('com promocao', 28.90, 124.90)]:
    pm = MIX_C*pc + (1-MIX_C)*pk
    lm = MIX_C*lucro_c(pc) + (1-MIX_C)*lucro_k(pk)
    print('%-14s preco medio R$ %6.2f | lucro medio R$ %5.2f | ROAS de equilibrio %.2fx'
          % (nome, pm, lm, pm/lm))
print()
print('Equilibrio = onde o Ads come o lucro inteiro da venda. Alvo pratico: 10-12x.')
print()
print('%10s %12s %12s %12s %12s' % ('Ads/dia', 'Ads/mes', 'ROAS 4', 'ROAS 7', 'ROAS 10'))
pm = MIX_C*34.90 + (1-MIX_C)*139.90
lm = MIX_C*lucro_c(34.90) + (1-MIX_C)*lucro_k(139.90)
for ads in (10, 20, 40, 80):
    m = ads*30
    linha = '%10d %12d' % (ads, m)
    for roas in (4, 7, 10):
        v = m*roas/pm
        linha += ' %12.0f' % (v*lm - m)
    print(linha + '   <- resultado em R$')
print()
print('vendas/mes que cada combinacao gera:')
print('%10s %12s %12s %12s' % ('Ads/dia', 'ROAS 4', 'ROAS 7', 'ROAS 10'))
for ads in (10, 20, 40, 80):
    m = ads*30
    print('%10d %12.0f %12.0f %12.0f' % (ads, m*4/pm, m*7/pm, m*10/pm))

print('\n' + '=' * 92)
print('O TETO DO NICHO — a ancora de realidade')
print('=' * 92)
print('Selos ACUMULADOS dos concorrentes de capsula especial:')
print('  Orfeu Arara 10un .... +100 vendidos')
print('  Coffee++ (Cafezale) . +25 vendidos')
print('  "Serra Canastra" .... +5 vendas')
print()
print('-> O nicho de capsula ESPECIAL e de dezenas por mes, nao de milhares.')
print('-> Quem faz milhares e o generico a R$ 1,48/capsula. Outro negocio.')
print('-> Nenhum orcamento de Ads cria demanda que nao existe.')
