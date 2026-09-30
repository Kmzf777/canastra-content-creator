# -*- coding: utf-8 -*-
"""Orçamento de Ads para as cápsulas, a partir da margem real.

Âncoras vindas dos vídeos (canal, data, id em docs/pesquisa-ml/ACHADOS.md):
  - Bruno Maciel 31/08: "até 5 a 6% de investimento em publicidade, proporcional
    ao faturamento, tá lindo"  -> TACOS de 5-6% como regime permanente
  - Bruno Maciel 31/08: contas de cliente rodando ROAS 15, 19, 20, 25, 26
  - Fabio Ludke 10/08: começa em ROAS 10-12, orçamento R$50/dia, desliga o
    ajuste automático de orçamento
  - Fabio Ludke 10/08: o ML sugere R$60/dia por padrão na primeira campanha
"""

PRODUTOS = {
    'Caixa 10':  dict(preco=34.90,  lucro=12.40, margem=35.5),
    'Kit 40':    dict(preco=139.90, lucro=39.01, margem=27.9),
    'Kit 60':    dict(preco=199.90, lucro=48.41, margem=24.2),
}


def por_venda(p, roas):
    """Quanto se gasta de Ads por venda, e o que sobra."""
    gasto = p['preco'] / roas
    return gasto, p['lucro'] - gasto


print('=== QUANTO SOBRA POR VENDA, EM CADA ROAS ===')
print('%-10s %8s | %s' % ('', 'lucro', ' | '.join('ROAS %2d' % r for r in (4, 7, 10, 12, 15, 20))))
for nome, p in PRODUTOS.items():
    cels = []
    for r in (4, 7, 10, 12, 15, 20):
        _, sobra = por_venda(p, r)
        cels.append('%7.2f' % sobra)
    print('%-10s %8.2f | %s' % (nome, p['lucro'], ' | '.join(cels)))

print('\n=== ROAS DE EQUILIBRIO (gasto de Ads = lucro inteiro) ===')
for nome, p in PRODUTOS.items():
    roas_eq = p['preco'] / p['lucro']
    print('%-10s empata em ROAS %.1fx  (ACOS %.1f%%) -> nunca operar abaixo disso' % (
        nome, roas_eq, 100 / roas_eq))

print('\n=== O QUE EU TINHA RECOMENDADO vs A PRATICA ===')
for nome, p in PRODUTOS.items():
    teto = p['preco'] / (p['lucro'] / 2)      # ACOS = metade da margem
    print('%-10s eu disse ROAS %.1fx (metade da margem) | pratica dos videos: 10-12x no inicio' % (
        nome, teto))
print('-> o meu numero era o TETO tolerado, nao o alvo. Apresentei um como o outro.')

print('\n=== RAMPA DE ORCAMENTO — so o Kit 40 recebe Ads no inicio ===')
kit = PRODUTOS['Kit 40']
for fase, dia, roas_real in [
        ('Semana 1-2  descoberta', 20, 4),
        ('Semana 3-4  se ROAS>=7', 40, 7),
        ('Mes 2       se ROAS>=10', 80, 10),
        ('Mes 3       se ROAS>=12', 150, 12)]:
    mes = dia * 30
    receita = mes * roas_real
    vendas = receita / kit['preco']
    bruto = vendas * kit['lucro']
    print('%-24s R$%3d/dia = R$%5d/mes | ROAS %2d -> receita R$%7.0f | %5.1f vendas | lucro bruto R$%7.0f | liquido R$%7.0f'
          % (fase, dia, mes, roas_real, receita, vendas, bruto, bruto - mes))

print('\n=== REGIME PERMANENTE: TACOS 5-6% (regra do Bruno Maciel) ===')
for fat in (5000, 10000, 20000, 40000):
    print('faturamento total R$%6d/mes -> orcamento de Ads R$%4d a R$%4d/mes (R$%3d a R$%3d/dia)' % (
        fat, fat * 0.05, fat * 0.06, fat * 0.05 / 30, fat * 0.06 / 30))

print('\n=== PISO DE APRENDIZADO (o algoritmo precisa de cliques) ===')
for cpc in (0.50, 1.00, 1.50, 2.00):
    for dia in (20, 40):
        print('CPC R$%.2f, R$%d/dia -> %4.0f cliques/dia, %4.0f/semana' % (
            cpc, dia, dia / cpc, dia / cpc * 7))
    print()
