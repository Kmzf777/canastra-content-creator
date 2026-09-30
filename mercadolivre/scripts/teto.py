# -*- coding: utf-8 -*-
"""Furar o teto de Ads: quanto custa comprar o Produto Estrela.

Ha DOIS tetos e eles tem naturezas opostas:
  - teto de ESTOQUE      -> nao se fura, se levanta enviando mais
  - teto de RENTABILIDADE -> se fura, e as vezes deve

Este script calcula o segundo. Companheiro de matriz.py, que calcula o primeiro.
"""
import math

P_C, P_K = 34.90, 139.90        # precos cheios
L_C, L_K = 12.82, 39.91         # lucro bruto por venda
CPV_C, CPV_K = 15.10, 60.40
MIX_C = 0.55                    # fatia das vendas que sai em caixa de 10
N_ANUN_C, N_ANUN_K = 3, 4

PM = MIX_C * P_C + (1 - MIX_C) * P_K      # preco medio da venda
LM = MIX_C * L_C + (1 - MIX_C) * L_K      # lucro medio da venda
ROAS_EQ = PM / LM                          # onde o Ads come o lucro inteiro

ALVO, DIAS = 60, 60                        # 60 vendas em 60 dias -> patamar do Estrela

print('preco medio R$ %.2f | lucro medio R$ %.2f | ROAS de equilibrio %.2fx'
      % (PM, LM, ROAS_EQ))

fat = ALVO * PM
bruto = ALVO * LM
# estoque necessario: o tipo mais exigente dita o n por anuncio
n = max(ALVO * MIX_C / N_ANUN_C, ALVO * (1 - MIX_C) / N_ANUN_K)
n = math.ceil(round(n, 6))   # round() antes: 11.0000001 nao vira 12
uc, uk = N_ANUN_C * n, N_ANUN_K * n
print('alvo %d vendas / %d dias | faturamento R$ %.0f | lucro bruto R$ %.0f'
      % (ALVO, DIAS, fat, bruto))
print('estoque: %d de cada anuncio = %d unidades = R$ %.0f de CPV'
      % (n, uc + uk, uc * CPV_C + uk * CPV_K))
print()

print('%8s %10s %9s %12s' % ('ROAS', 'Ads total', 'Ads/dia', 'resultado'))
for roas in (5.0, 4.0, ROAS_EQ, 3.0, 2.5, 2.0, 1.5):
    ads = fat / roas
    print('%7.2fx %10.0f %9.0f %+12.0f' % (roas, ads, ads / DIAS, bruto - ads))
print()

print('perda POR VENDA abaixo do equilibrio, e acumulada')
print('%8s %10s %9s %9s %9s' % ('ROAS', 'por venda', '30 vendas', '60', '120'))
for roas in (3.0, 2.5, 2.0, 1.5):
    perda = PM / roas - LM          # custo de Ads por venda menos o lucro da venda
    print('%7.2fx %10.2f %9.0f %9.0f %9.0f'
          % (roas, perda, perda * 30, perda * 60, perda * 120))
print()

print('custo de estoque antigo no Full no mes 7 (o ativo que o Estrela destrava)')
for un in (150, 300, 600):
    print('  %4d unidades: R$ %.0f/mes sem Estrela  |  R$ 0 com Estrela'
          % (un, un * 12.21))
print()

print('stop-loss: quantos dias cada bolso aguenta')
print('%12s %12s %12s' % ('reservado', 'a 40/dia', 'a 80/dia'))
for v in (1000, 2000, 3000, 5000):
    print('%12d %10.0f d %10.0f d' % (v, v / 40, v / 80))
