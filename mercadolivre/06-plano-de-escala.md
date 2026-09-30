# Plano de escala — duas fases

> Script: [`../scripts/escala.py`](scripts/escala.py).
> Artefato: [Testar e Abrir a Torneira](https://claude.ai/artifact/UrAEBFZ7gNsFRDa7wZkVgM).

---

## A premissa que se inverteu

O Rafael informou **5 a 15 mil cápsulas com reposição rápida**, descrevendo como "muito
estoque". No ponto médio (10.000 cápsulas = 1.000 caixas de 10), isso comporta
**426 vendas** no mix projetado — cerca de **um ano de estoque** a 35 vendas/mês.
A conta vende **6 por mês** hoje.

**Não é muito estoque para pouca demanda. É estoque demais para a demanda que existe.**

Consequência direta: **quem dita o ritmo é o Ads, não o estoque.** E mandar tudo ao Full
seria a pior decisão possível.

### Por que não mandar tudo ao Full

| Unidades paradas | Mês 1 | Mês 5 | Mês 7 |
|---:|---:|---:|---:|
| 100 | R$ 21 | R$ 121 | **R$ 1.221** |
| 300 | R$ 63 | R$ 363 | **R$ 3.663** |
| 600 | R$ 126 | R$ 726 | **R$ 7.326** |

> *"Mande para o Full só o que vende antes dos quatro meses: use as vendas dos últimos
> trinta dias como medida."*
> — Milewa, 25/09/2026, `7h4R4KPK9bw`

**Em Supermercado o relógio começa aos 2 meses, não aos 4.**

---

## Fase 1 — Descoberta · 30 dias · R$ 1.810 em jogo

Comprar a informação que falta pelo menor preço possível.

| Decisão | Valor | Por quê |
|---|---|---|
| **Enviar ao Full** | 100 caixas · R$ 1.510 | Comporta **43 vendas** — o triplo do esperado. Folga para nunca faltar, pequeno o bastante para o estoque antigo não morder. Sobram 900 caixas na torrefação, onde custam zero |
| **Ads** | **R$ 10/dia** · R$ 300 no mês | O valor em que **o equilíbrio coincide com o portão**: empata em ~15 vendas, que é exatamente ROAS 4 |
| **Onde** | Só o Kit 40 · 3 Sabores (`2691974682`) | Concentra histórico num anúncio em vez de espalhar em sete |
| **Medir** | CPC real · conversão real · ROAS | São premissas em todo cálculo até aqui. Esta fase os transforma em fato |
| **Não fazer** | Nada por 28 dias | Cada alteração reinicia o aprendizado que você está pagando para fazer |

### Projeção da fase 1 com R$ 300 de Ads

| Vendas no mês | Faturamento | Lucro bruto | Resultado | ROAS | Leitura |
|---:|---:|---:|---:|---:|---|
| 5 | 381 | 100 | −200 | 1,3 | o anúncio não converte |
| 10 | 761 | 199 | −101 | 2,5 | converte, mas não paga |
| **15** | **1.142** | **299** | **−1** | **3,8** | **o portão** |
| 20 | 1.522 | 399 | +99 | 5,1 | passa com folga |
| 30 | 2.284 | 598 | +298 | 7,6 | escalar sem medo |

*(lucro bruto de R$ 19,94 por venda média do mix: 55% caixa / 45% kit, 60% em promoção)*

---

## O portão

> **Passa para a Fase 2 se o Ads se pagou: 15 vendas ou mais no primeiro mês.**

É ROAS 4 e é o ponto de equilíbrio ao mesmo tempo. Um critério, sem interpretação.

| Resultado | O que fazer | Por quê |
|---|---|---|
| **15+ vendas** | Abrir a Fase 2 no giro medido | A demanda existe e o anúncio converte |
| **10 a 14** | Mais 30 dias no mesmo orçamento | Anúncio novo sem avaliação converte abaixo do que vai converter. Falta prova social, não demanda |
| **menos de 10** | Cortar o Ads, revisar foto, preço e ficha | Mais verba não conserta anúncio que não converte |

### O que o portão não mede
**A reputação.** Se a conta ainda estiver vermelha na Fase 1, o resultado vem contaminado
e você conclui erroneamente que a demanda não existe. **Os R$ 75 de garantia e o Full vêm
antes da Fase 1**, não depois.

---

## Fase 2 — Escala · 60 dias · alvo Produto Estrela

Full raso, Ads fundo, reposição curta. Cada peça resolve um risco.

| Decisão | Regra | Por quê |
|---|---|---|
| **Full raso** | 2 meses do giro **medido** | Em Supermercado a multa começa aos 2 meses. É o teto exato antes de o relógio virar |
| **Ads fundo** | 50% do lucro bruto do volume medido | Permite o Ads **puxar acima do ritmo natural** sem virar prejuízo |
| **Reposição semanal** | lotes pequenos | É o que torna o Full raso seguro. **Profundidade de estoque vira frequência de envio** |
| **Corrida ao Estrela** | 60 dias | É o objetivo real, mais que o lucro do período |

### Tudo derivado do giro medido — nada escolhido

| Giro medido | Enviar ao Full | Capital | Ads/mês | Ads/dia | Repor/semana |
|---:|---:|---:|---:|---:|---:|
| 20/mês | 94 cx | 1.419 | 199 | 6,65 | ~10 cx |
| **35/mês** | **164 cx** | **2.484** | **349** | **11,63** | **~20 cx** |
| 60/mês | 282 cx | 4.258 | 598 | 19,94 | ~30 cx |
| 100/mês | 470 cx | 7.097 | 997 | 33,23 | ~50 cx |
| 150/mês | 705 cx | 10.646 | 1.496 | 49,85 | ~80 cx |

---

## O alvo: Produto Estrela

**É o mecanismo que transforma estoque parado em vantagem.**

> *"São os produtos mais vendidos na sua categoria **nos últimos 60 dias dentro de Full**.
> Seus produtos mais vendidos **não impactam nem nas métricas de excedente, nem nas
> métricas de estoque antigo**. Você pode enviar mais unidades dos seus produtos estrela
> com total tranquilidade."*
>
> *"Se você enviar o estoque sugerido ou mais, a gente **distribui seus produtos pelos
> nossos centros de distribuição** e você pode vender com envio rápido por todo o país.
> Além disso, você também pode ganhar **bonificação por custos de estoque antigo**."*
>
> — Vendedores Mercado Livre Brasil (canal oficial), 10/08/2026, `qPVIEY_Fg_E`

**Três coisas destravam de uma vez:** o teto de estoque some, o ML espalha o produto por
vários CDs (encurta prazo no país inteiro e alimenta a Buy Box), e o custo que mais
assusta neste plano pode virar bonificação.

### Onde acompanhar
`Anúncios → Gestão de estoque Full → Planejamento de envios`.
A etiqueta azul **"estrela"** fica no canto superior esquerdo do produto, junto da
quantidade recomendada de reposição.

### O alvo

| Alvo em 60 dias | Por mês | Estoque necessário | Faturamento no período |
|---:|---:|---:|---:|
| 40 vendas | 20 | 94 cx | R$ 3.045 |
| **60 vendas** | **30** | **141 cx** | **R$ 4.567** |
| 80 vendas | 40 | 188 cx | R$ 6.090 |

**Âncora de realidade:** os selos acumulados dos concorrentes de especial são Coffee++
+25, "Serra Canastra" +5 e Orfeu Arara +100. O patamar de "mais vendido do especial" é da
ordem de **dezenas em 60 dias** — alcançável.

---

## Os três freios

### Freio 1 — preço, nunca pausa
Se o Ads vender mais rápido que a reposição, **sobe o preço**. De R$ 34,90 para R$ 39,90
a margem vai de 36,7% para 42,2% e a venda desacelera sozinha.

> *"É muito pior você ter anúncio pausado do que perder venda porque o seu preço subiu.
> **Cada um dia de anúncio pausado, você perde dois dias de ranqueamento** que você
> construiu às vezes ao longo de meses. Não deixe pausar. Vê que vai acabar a mercadoria,
> suba o preço."*
> — Milton P Rabello, 27/08/2026, `swCx36qRg0w`

Ele narra o método: subiu o preço progressivamente, a venda se manteve, até bater um
patamar em que oscilou — aí voltou um estágio. **Serve como descoberta do teto de preço e
como freio de estoque ao mesmo tempo.**

| Preço da caixa | Lucro | Margem | Efeito |
|---:|---:|---:|---|
| 34,90 | 12,82 | 36,7% | preço base |
| 37,90 | 15,22 | 40,2% | freio leve |
| 39,90 | 16,82 | 42,2% | freio leve |
| 42,90 | 19,22 | 44,8% | freio forte |

### Freio 2 — teto de Ads derivado
Nunca mais de **50% do lucro bruto do volume medido**. Recalcula todo mês.

### Freio 3 — teto de estoque no Full
Nunca mais de **2 meses de cobertura** enquanto não houver Estrela. O que sobra fica na
torrefação, onde custa zero. **Depois do Estrela, este freio pode ser solto — e é por
isso que ele é o alvo.**

---

## Onde isto pode falhar

| Risco | Sinal | Resposta |
|---|---|---|
| **Reputação vermelha na Fase 1** | ROAS baixo com CTR normal | Resolver antes: R$ 75 e Full. Senão a medição não vale |
| **CPC muito acima de R$ 1** | Poucos cliques para R$ 10/dia | Subir para R$ 15/dia e refazer o portão nesse patamar |
| **Nicho menor que o esperado** | Impressões baixas mesmo com verba | O teto é de dezenas/mês. O plano funciona, só num patamar menor |
| **Estrela não vem em 60 dias** | Sem etiqueta azul no planejamento | Manter Full raso e seguir. O Estrela acelera, não é pré-requisito |
| **Frete do kit acima de R$ 20** | Fatura do ML acima do previsto | Único número estimado do modelo. Confirmar no simulador |

---

## Cenários de 3 meses — para calibrar expectativa

Lote de 90 caixas + 80 kits (R$ 6.191 de capital), Ads a R$ 20/dia rodando de 1 a 3 meses
conforme o cenário. Simulador interativo:
[link](https://claude.ai/artifact/24vpdusJGx3ojTFMPuPRjV).

| Cenário | Giro | Faturamento | Ads | Resultado |
|---|---:|---:|---:|---:|
| Prejuízo | 15% | 1.517 | 600 | **−340** |
| Se pagou | 35% | 4.651 | 1.200 | **−97** |
| Lucro | 65% | 8.638 | 1.800 | **+395** |
| Perfeito | 95% | 12.625 | 1.800 | **+1.487** |

**A linha que separa perder de ganhar é vender ~17 unidades a mais por mês.** É esse o
alvo, não os R$ 12 mil do cenário Perfeito.
