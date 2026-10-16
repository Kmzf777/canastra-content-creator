---
name: canastra-ml-ads
description: Use when planning or reviewing Mercado Ads (Product Ads) for Café Canastra — daily budget, target ROAS/ACOS, which listing gets budget, when to exceed the profitability ceiling, reading campaign results. Never activates or changes a campaign by itself.
---

# Mercado Ads

Estratégia completa e as fontes: [`mercadolivre/05-ads.md`](../../../mercadolivre/05-ads.md).
Scripts: `scripts/ads.py`, `scripts/teto.py` (rentabilidade), `scripts/matriz.py` (estoque).

**Ativar, pausar ou mudar a verba de campanha é ação do Rafael.** O agente propõe números e
o passo a passo; ele clica.

## As regras

1. **Orçamento é derivado, nunca escolhido:** Ads = **50% do lucro bruto** do volume medido
   no mês anterior. Recalcula todo mês.
2. **Três números por anúncio**, todos do `precificar.py`:
   - **Piso (ROAS de equilíbrio)** = preço ÷ lucro por venda. Abaixo dele o Ads come o lucro todo.
   - **Alvo inicial ROAS 10–12×**; contas maduras rodam 15–26×.
   - ROAS 7 era o teto tolerável, **não** o alvo — erro já cometido.
3. **Anúncio novo converte mal:** espere ROAS 3–5 nas primeiras semanas.
4. **Dois tetos de natureza oposta:** o de **estoque** não se fura (se levanta enviando
   estoque); o de **rentabilidade** pode ser furado **só para comprar um ativo** (avaliação,
   histórico, Produto Estrela), com stop-loss em reais **e** em dias, e nunca abaixo de ROAS 2.
5. **Pré-condições para gastar:** estoque que cubra o volume, envio sem atraso, e de
   preferência reputação verde. Em vermelho, clique caro converte mal por motivo que verba
   não conserta.
6. **Margem fina = Ads quase proibido.** Com lucro de R$ 3 por venda o piso é ROAS ~33×:
   qualquer campanha perde dinheiro. Conserte o preço antes de pensar em Ads.
7. Brand Ads foi extinto. Ciclo de 28 dias de aprendizado e ROAS dinâmico: **não verificados**.

## Como entregar

Por anúncio: lucro/venda, piso, alvo, verba diária derivada do volume, e a condição de
parada. Sem volume medido, a recomendação é **R$ 10/dia** de descoberta, não o padrão do ML.
