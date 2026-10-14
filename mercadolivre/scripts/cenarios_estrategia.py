# -*- coding: utf-8 -*-
"""Cenários de estratégia do ML com o CMV real — base do `16-estrategia-competir.md`.

Usa as funções de `precificar.py` (mesma fórmula, conferida com o "Você recebe" da conta).
Tudo que NÃO foi medido na conta entra como parâmetro com o nome "_SUPOSTO" e aparece
marcado na saída: frete com reputação verde, custos do Full, frete abaixo de R$ 79.

    python mercadolivre/scripts/cenarios_estrategia.py            # todas as seções
    python mercadolivre/scripts/cenarios_estrategia.py frete      # uma seção

Princípios de administração usados (os nomes aparecem na saída):
  - margem de contribuição (MC) = preço − custos variáveis (tarifa, imposto, frete, CMV, Ads)
  - markup divisor: preço = custo variável fixo em R$ / (1 − % variáveis − margem alvo)
  - ACOS máx = MC antes de Ads / preço; ROAS de equilíbrio = 1 / ACOS máx
  - ponto de equilíbrio em unidades = custo fixo do canal / MC unitária
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from precificar import CMV, FRETE, IMPOSTO, TARIFA, preco_para_margem, resultado  # noqa: E402

# ── suposições (não medidas na conta; troque quando medir) ──
FRETE_1KG_VERDE_SUPOSTO = (17.15, 24.01)   # 50% e 30% de desconto sobre os R$ 34,30 vermelhos
FULL_ARMAZENAGEM_DIA_SUPOSTO = (0.007, 0.07)   # R$/un/dia; legenda dos vídeos é ambígua
FULL_ENTRADA_LOTE_SUPOSTO = 250.00             # R$ mínimo de transporte até o CD (XETb71Rn4dM)
CUSTO_FIXO_CANAL_MES_SUPOSTO = 3000.00         # pessoa/hora dedicada + ferramentas; ajuste


def mc(preco, cmv, frete, tipo='classico', ads_pct=0.0, desconto_pct=0.0, rebate=0.0):
    """Margem de contribuição em R$ por venda. `desconto_pct` sobre o preço, bancado pelo vendedor;
    `rebate` = R$ que o ML devolve numa promoção co-participada; `ads_pct` = TACOS sobre o preço."""
    p = preco * (1 - desconto_pct)
    r = resultado(round(p, 2), cmv, frete, tipo)
    return round(r['lucro'] - p * ads_pct + rebate, 2), round(p, 2)


def secao_preco():
    print('\n## 1. Preço do 1 kg (Clássico, frete grátis vermelho R$ %.2f)\n' % FRETE['1kg'])
    print('| preço | MC R$ | MC % | ACOS máx | ROAS equilíbrio | Ads cabível a ROAS 15 (R$/venda) |')
    print('|---:|---:|---:|---:|---:|---:|')
    for p in (105.58, 109.90, 114.90, 119.90, 124.90, 129.90, 139.90):
        m, _ = mc(p, CMV['1kg'], FRETE['1kg'])
        acos = m / p
        roas = (1 / acos) if acos > 0 else float('inf')
        sobra15 = m - p / 15
        print('| %.2f | %.2f | %.1f%% | %.1f%% | %s | %.2f |' % (
            p, m, acos * 100, acos * 100, '%.1f' % roas if roas != float('inf') else '∞', sobra15))
    print('\nMarkup divisor (preço para a margem alvo, antes de Ads):')
    for alvo in (10, 12, 15, 20):
        print('- %d%%: Clássico R$ %.2f · Premium R$ %.2f' % (
            alvo, preco_para_margem(alvo, CMV['1kg'], FRETE['1kg'], 'classico'),
            preco_para_margem(alvo, CMV['1kg'], FRETE['1kg'], 'premium')))


def secao_frete():
    print('\n## 2. O frete é a maior alavanca (1 kg a R$ 109,90 e R$ 119,90, Clássico)\n')
    print('| frete | origem | MC a 109,90 | MC a 119,90 | equilíbrio |')
    print('|---:|---|---:|---:|---:|')
    linhas = [(FRETE['1kg'], 'medido, vermelha')] + [
        (f, 'SUPOSTO verde (−%d%%)' % round((1 - f / FRETE['1kg']) * 100)) for f in FRETE_1KG_VERDE_SUPOSTO]
    for f, origem in linhas:
        a, _ = mc(109.90, CMV['1kg'], f)
        b, _ = mc(119.90, CMV['1kg'], f)
        print('| %.2f | %s | %.2f | %.2f | %.2f |' % (f, origem, a, b, preco_para_margem(0, CMV['1kg'], f)))
    print('\nPeso do frete no preço de R$ 109,90: %.0f%%; do CMV: %.0f%%; tarifa+imposto: %.0f%%.' % (
        FRETE['1kg'] / 109.90 * 100, CMV['1kg'] / 109.90 * 100, (TARIFA['classico'] + IMPOSTO) * 100))


def secao_kit():
    print('\n## 3. Kit 2 × 1 kg dilui o frete (frete medido R$ %.2f contra 2 × R$ %.2f)\n' % (FRETE['kit2kg'], FRETE['1kg']))
    print('| oferta | preço | R$/kg | tipo | MC R$ | MC % |')
    print('|---|---:|---:|---|---:|---:|')
    m1, _ = mc(109.90, CMV['1kg'], FRETE['1kg'])
    print('| 2 vendas avulsas de 1 kg | 219,80 | 109,90 | Clássico | %.2f | %.1f%% |' % (2 * m1, 2 * m1 / 219.80 * 100))
    for p in (199.90, 209.90, 219.80, 229.90):
        for t in ('classico', 'premium'):
            m, _ = mc(p, 2 * CMV['1kg'], FRETE['kit2kg'], t)
            print('| kit 2 × 1 kg | %.2f | %.2f | %s | %.2f | %.1f%% |' % (p, p / 2, t, m, m / p * 100))


def secao_full():
    print('\n## 4. Full: custo extra por unidade (frete e tarifa são os mesmos dentro e fora — XETb71Rn4dM)\n')
    print('Entrada (transporte até o CD) SUPOSTA em R$ %.0f por lote; armazenagem SUPOSTA.\n' % FULL_ENTRADA_LOTE_SUPOSTO)
    print('| lote (un) | dias de cobertura | entrada/un | armazenagem/un (0,007 → 0,07/dia) | total/un |')
    print('|---:|---:|---:|---:|---:|')
    for lote, dias in ((10, 60), (30, 30), (60, 30), (120, 30)):
        ent = FULL_ENTRADA_LOTE_SUPOSTO / lote
        a0, a1 = (d * dias / 2 for d in FULL_ARMAZENAGEM_DIA_SUPOSTO)   # média: metade da cobertura
        print('| %d | %d | %.2f | %.2f → %.2f | %.2f → %.2f |' % (lote, dias, ent, a0, a1, ent + a0, ent + a1))
    print('\nCom MC de R$ 3,32 (preço de hoje), o Full só se paga se trouxer volume ou permitir subir o preço.')


def secao_ads():
    print('\n## 5. Verba de Ads derivada da margem (regra: TACOS ≤ metade da MC)\n')
    print('| preço | MC antes de Ads | TACOS teto (½ MC) | MC depois de Ads | vendas/mês p/ pagar R$ %.0f de fixo |' % CUSTO_FIXO_CANAL_MES_SUPOSTO)
    print('|---:|---:|---:|---:|---:|')
    for p in (109.90, 119.90, 129.90, 139.90):
        m, _ = mc(p, CMV['1kg'], FRETE['1kg'])
        teto = m / 2 / p
        m2, _ = mc(p, CMV['1kg'], FRETE['1kg'], ads_pct=teto)
        pe = CUSTO_FIXO_CANAL_MES_SUPOSTO / m2 if m2 > 0 else float('inf')
        print('| %.2f | %.2f | %.1f%% | %.2f | %s |' % (p, m, teto * 100, m2, '%.0f' % pe if pe != float('inf') else '∞'))


def secao_promo():
    print('\n## 6. Promoção: desconto bancado × rebate do ML (1 kg, preço cheio R$ 129,90)\n')
    print('| desconto | preço final | rebate do ML | MC R$ |')
    print('|---:|---:|---:|---:|')
    for d in (0.0, 0.05, 0.07, 0.10, 0.15):
        for reb in (0.0, 5.0):
            m, pf = mc(129.90, CMV['1kg'], FRETE['1kg'], desconto_pct=d, rebate=reb)
            print('| %d%% | %.2f | %.2f | %.2f |' % (d * 100, pf, reb, m))


def secao_revenda():
    print('\n## 7. A vantagem de fábrica contra o revendedor (mesmo café, mesmo frete)\n')
    print('Revendedor compraria o 1 kg especial no atacado; o custo dele é o preço de atacado, o seu é o CMV.\n')
    print('| custo do produto | quem | MC a 109,90 | preço para 15% |')
    print('|---:|---|---:|---:|')
    for custo, quem in ((CMV['1kg'], 'Canastra (CMV)'), (60.0, 'revenda, atacado R$ 60'), (70.0, 'revenda, atacado R$ 70')):
        m, _ = mc(109.90, custo, FRETE['1kg'])
        print('| %.2f | %s | %.2f | %.2f |' % (custo, quem, m, preco_para_margem(15, custo, FRETE['1kg'])))


SECOES = {'preco': secao_preco, 'frete': secao_frete, 'kit': secao_kit, 'full': secao_full,
          'ads': secao_ads, 'promo': secao_promo, 'revenda': secao_revenda}

if __name__ == '__main__':
    escolha = sys.argv[1:] or list(SECOES)
    for nome in escolha:
        SECOES[nome]()
