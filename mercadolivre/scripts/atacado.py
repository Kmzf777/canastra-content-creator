# -*- coding: utf-8 -*-
"""Preco de atacado (ML Negocios): vale a pena, e em que faixas.

MEDIDO
  Formulario do ML, 30/09/2026: o bloco chama-se "Precos de atacado | EXCLUSIVO NEGOCIOS".
  Faixas ja em uso na conta, no cafe em graos MLB5903454718 (R$ 109,90):
      5+ un -> R$ 99,99   (-9,0%)
     10+ un -> R$ 94,99   (-13,6%)
  Comissao Classico 14% sobre o preco efetivo.
  Frete gratis por ENVIO: R$ 14,45 (caixa 10 e kit 40, medido).
  Comprador paga: custo operacional ~5-7% do valor do PEDIDO
      (1,40 @18,70 | 2,40 @40 | 4,80 @83,10 | 7,20 @139,90).

PESQUISA
  "Isso aqui so serve para empresas. So conta CNPJ tem disponivel a opcao de precos por
   atacado. CPFs vao entrar no anuncio mas nao vai ter essa opcao disponivel la dentro.
   Pode adicionar ate CINCO opcoes."                  -- BSNDMsezcbc
  "Nao vou colocar preco atacado, mas RECOMENDO que voce utilize. (...) Ah, nao vai deixar
   porque eu nao tenho estoque suficiente. (...) Ele so avisou."   -- Fabio Ludke, -javeW5ePCg

PREMISSA NAO MEDIDA (marcada): como o frete gratis escala com o peso do pedido.
  Calculo os dois extremos e mostro que a conclusao nao muda entre eles.
"""
CPV_C, CPV_K = 15.10, 60.40
COM = 0.14
FRETE_GRATIS_1 = 14.45      # por ENVIO, medido para 1 unidade
OP_PCT = 0.06               # custo operacional quando o comprador paga o frete


def lucro_caixa_lote(preco_un, n, op_pct=OP_PCT):
    """Caixa de 10: comprador paga o frete. Custo operacional e % do PEDIDO."""
    receita = preco_un * n
    return receita - receita * COM - receita * op_pct - n * CPV_C


def lucro_kit_lote(preco_un, n, frete_modo='dilui'):
    """Kit 40: frete gratis, pago pelo vendedor, POR ENVIO.

    frete_modo='dilui'  -> um envio so; custo cresce com o peso, nao linear.
                           Aproximo por 14,45 * n**0.5 (dobrar o peso nao dobra o frete).
    frete_modo='linear' -> pior caso: o ML cobra 14,45 por unidade.
    """
    receita = preco_un * n
    frete = FRETE_GRATIS_1 * (n ** 0.5) if frete_modo == 'dilui' else FRETE_GRATIS_1 * n
    return receita - receita * COM - frete - n * CPV_K


print('=' * 96)
print('CAIXA DE 10 — R$ 34,90 avulso (comprador paga o frete)')
print('=' * 96)
base = lucro_caixa_lote(34.90, 1)
print('avulso: lucro R$ %.2f/caixa | margem %.1f%%\n' % (base, base / 34.90 * 100))
print('%6s %10s %8s %12s %12s %10s' % ('qtd', 'preco un', 'desc', 'lucro total', 'lucro/un', 'margem'))
for n, p in [(1, 34.90), (3, 32.90), (5, 31.90), (10, 29.90), (20, 28.90)]:
    l = lucro_caixa_lote(p, n)
    print('%6d %10.2f %7.1f%% %12.2f %12.2f %9.1f%%' % (
        n, p, (34.90 - p) / 34.90 * 100, l, l / n, l / (p * n) * 100))

print('\n' + '=' * 96)
print('KIT DE 40 — R$ 139,90 avulso (frete gratis, R$ 14,45 por ENVIO)')
print('=' * 96)
b2 = lucro_kit_lote(139.90, 1)
print('avulso: lucro R$ %.2f/kit | margem %.1f%%\n' % (b2, b2 / 139.90 * 100))
print('%6s %10s %8s %12s %12s %10s   %12s %10s' % (
    'qtd', 'preco un', 'desc', 'lucro tot', 'lucro/un', 'margem', 'PIOR lucro/un', 'margem'))
for n, p in [(1, 139.90), (2, 132.90), (3, 129.90), (5, 124.90), (10, 119.90)]:
    l = lucro_kit_lote(p, n)
    lp = lucro_kit_lote(p, n, 'linear')
    print('%6d %10.2f %7.1f%% %12.2f %12.2f %9.1f%%   %12.2f %9.1f%%' % (
        n, p, (139.90 - p) / 139.90 * 100, l, l / n, l / (p * n) * 100,
        lp / n, lp / (p * n) * 100))

print('\n' + '=' * 96)
print('QUANTO ESTOQUE CADA FAIXA EXIGE (1 pedido daquele tamanho)')
print('=' * 96)
print('O ML avisa quando o estoque nao comporta a faixa. Faixa maior que o estoque e inutil.')
print('%8s %20s %20s' % ('faixa', 'caixas necessarias', 'kits necessarios'))
for n in (2, 3, 5, 10, 20):
    print('%8d %20d %20d' % (n, n, n))

print('\n' + '=' * 96)
print('EFEITO NA REPUTACAO — o ponto contra-intuitivo')
print('=' * 96)
print('A metrica de envios incorretos e por ENVIO, nao por unidade.')
print('Faltam 131 ENVIOS limpos para o verde (26/(69+V) <= 0,13).')
print()
print('%10s %14s %16s %18s' % ('unidades', 'se avulso', 'se em lotes de 5', 'envios a menos'))
for un in (100, 200, 300):
    print('%10d %14d %16d %18d' % (un, un, un // 5, un - un // 5))
print()
print('-> Atacado vende MAIS unidades com MENOS envios.')
print('-> Enquanto a conta estiver vermelha, isso ATRASA a chegada ao verde.')
