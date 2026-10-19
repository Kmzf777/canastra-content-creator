# Análises de vendas, clientes, produtos/estoque e financeiro para uma torrefação de café especial (B2C + B2B) com dados do Bling

Notas de pesquisa (out/2026). Convenção: [BR] = dado brasileiro; [GLOBAL/EUA] = benchmark estrangeiro, usar só como referência de direção; [antigo] = anterior a 2023. Boa parte dos benchmarks de unit economics de café vem de blogs de consultoria (eightx, beancount), não de estudos auditados. Trate como faixas, não como verdades.

## 1. Receita: período, canal, vendedor, tipo de cliente, ticket, MoM/YoY, sazonalidade, mix B2C x B2B

### Takeaway
O painel de receita deve separar sempre B2C e B2B (o B2B distorce ticket, frequência e RFM). Mostre receita líquida, pedidos, ticket médio e itens/kg por pedido, quebrados por canal (loja, marketplace, venda direta), vendedor e tipo de cliente, com MoM e YoY. No varejo online brasileiro o pico é a Black November e o Natal. Para café, existe um leve efeito de inverno nas cafeterias, e em 2025 a inflação do café fez a receita subir enquanto o volume caiu. Por isso convém acompanhar também kg vendidos, não só R$.

### Cited Findings
- [BR] O e-commerce D2C de PMEs da Nuvemshop movimentou R$ 5,8 bi em 2025: 22 mi de pedidos, ticket médio de R$ 263, ~4 produtos por pedido, 88% dos pedidos via smartphone. — [Central do Varejo / Nuvemshop](https://centraldovarejo.com.br/lojistas-d2c-movimentam-r-58-bilhoes-em-2025-aponta-nuvemshop/?amp=1)
- [BR] A Black November foi, pelo 3º ano seguido, o principal período do D2C, com 14% do GMV anual (Nuvemshop 2025). — [Central do Varejo](https://centraldovarejo.com.br/lojistas-d2c-movimentam-r-58-bilhoes-em-2025-aponta-nuvemshop/?amp=1)
- [BR] Black Friday e Natal podem somar mais de 30% da receita anual de muitas lojas online. É estimativa de material de logística, não estudo. — [Loggi](https://www.loggi.com/conteudos/empreendedorismo/calendario-sazonal/)
- [BR] Na Black Friday 2024, as vendas de café torrado subiram 98% no período, com mais unidades por transação (Neogrid, atacarejo/café torrado em geral, não especial). — [Gironews](https://gironews.com/negocios/brasileiro-antecipa-compras-de-natal-na-black-friday/)
- [BR] Cafeterias de BH registram ~20% de alta em bebidas quentes no inverno, mas a procura geral por café fica estável no ano. Algumas redes não sentem alta porque o inverno coincide com férias. A matéria não é datada com precisão; parte das fontes sobre inverno é antiga. — [Diário do Comércio](https://diariodocomercio.com.br/negocios/inverno-ajuda-a-impulsionar-os-resultados-das-cafeterias/)
- [BR] ABIC (nov/24 a out/25): o consumo caiu 2,31%, para 21,4 mi de sacas, enquanto o faturamento da indústria subiu 25,6%, para R$ 46,24 bi. Efeito preço: o consumidor reduziu desperdício e comprou menos. — [InfoMoney](https://www.infomoney.com.br/?p=3192794); [Safras](https://safras.com.br/consumo-total-de-cafe-no-brasil-cai-231-e-soma-214-milhoes-de-sacas-em-2025-aponta-abic/)
- [BR] O café torrado no varejo do Sudeste passou de R$ 70/kg em jul/2025 e recuou para perto de R$ 60/kg no fim do ano. — [Diário de Pernambuco / ABIC](https://www.diariodepernambuco.com.br/economia/2026/01/11706457-alta-nos-precos-derruba-consumo-de-cafe-no-brasil-em-2025-diz-abic.html)
- [BR] Início de 2026: o varejo de café voltou a crescer (+2,44% no quadrimestre). O café especial chegou a R$ 161,26/kg em abril (+17% em 12 meses), mas o ganho de volume veio do café mais barato. — [Folha Vitória](https://www.folhavitoria.com.br/folha-business/cafe-tradicional-fica-mais-barato-e-especial-tem-alta-no-inicio-do-ano/)
- [BR] A colheita avança a partir de abril e pressiona sazonalmente o preço do café para baixo (ABIC, mar/2025). Isso afeta o custo do verde, não a demanda. — [ABIC](https://www.abic.com.br/wp-content/uploads/2025/03/2025.03.14.pdf)
- [BR] Q1/2025: o faturamento da categoria bebidas no e-commerce cresceu 20,3%, puxado pela alta de 77,87% no preço do café em 12 meses (Neotrust). — busca agregada, ver [Gironews tag Neotrust](https://gironews.com/tag/neotrust/)

### Inferences
- Fórmulas do painel:
  - Receita líquida = Σ(total dos pedidos faturados) − cancelamentos/devoluções.
  - Ticket médio = receita / nº de pedidos, calculado separado para B2C e B2B.
  - Preço médio por kg = receita / kg vendidos.
  - MoM % = (mês − mês anterior) / mês anterior.
  - YoY % = (mês − mesmo mês do ano anterior) / mesmo mês do ano anterior.
  - Mix B2B % = receita B2B / receita total.
  - Decomposição da variação: Δreceita = efeito volume (Δkg × preço antigo) + efeito preço (Δpreço × kg novo). É essencial em 2025-26, com a inflação do café.
- Calendário a marcar no gráfico: Black November/Natal (pico D2C), Dia dos Pais (agosto, presente), inverno (junho a agosto, B2B cafeterias), safra (abril em diante, custo).
- O ticket do e-commerce D2C (R$ 263) mistura categorias e não serve como meta de café. É melhor comparar o ticket por kg e o próprio YoY.
- Classifique o tipo de cliente pelo campo do Bling (PF/PJ ou tipo de contato), com regra de fallback CPF = B2C e CNPJ = B2B.

### Gaps
- Não encontrei série mensal pública de vendas de café especial (online ou B2B) no Brasil, nem dados de Dia dos Pais para torrefações.
- Não há benchmark brasileiro de mix B2C/B2B para torrefações pequenas.

## 2. Clientes: recompra, intervalo entre pedidos, coortes, LTV, LTV:CAC, RFM, churn B2B, contas em risco, Pareto

### Takeaway
No B2C, meça a taxa de recompra em janelas fixas (90 e 365 dias), o intervalo mediano entre o 1º e o 2º pedido e as coortes mensais de primeira compra. Use RFM em quartis, só com clientes B2C. No B2B, o churn é "silencioso": a conta deixa de pedir, sem cancelamento formal. A regra prática é sinalizar uma conta quando os dias desde o último pedido passam de cerca de 2x a mediana do intervalo dela. Para cafeterias, um intervalo de recompra saudável fica em 14 a 28 dias, e acima de 45 dias já indica risco (benchmark citado como SCA, EUA).

### Cited Findings
- [GLOBAL] A recompra em consumíveis fica em 30-45% (média DTC ~28%) ou 35-55% em base de 365 dias, conforme o artigo. Para bebidas sem assinatura, 30% é uma boa meta. As fontes da eightx divergem entre si. — [eightx repeat rate](https://eightx.co/blog/average-ecommerce-repeat-purchase-rate-by-vertical-2026)
- [GLOBAL] Estudo de fev/2026 com 156 mil clientes DTC: recompra agregada de 18,8%. Metade dos 2º pedidos acontece em até 30 dias e três quartos em até 90 dias. A janela muda a taxa em 15 p.p. ou mais. — [Taylor Sicard](https://taylorsicard.com/blog/dtc-retention-benchmarks-2026)
- [GLOBAL] Assinatura de café: churn mensal saudável de 4-7% (top: 3-4%), ~35% ao ano. ~28% dos cancelamentos ocorrem nos 3 primeiros meses e 25-40% do churn é involuntário (falha de pagamento). — [eightx unit economics, jun/2026](https://eightx.co/blog/coffee-brand-unit-economics); [eightx churn](https://eightx.co/blog/coffee-subscription-churn-rate-benchmark)
- [GLOBAL] Outra referência, atribuída à SCA: churn mensal de assinatura abaixo de 8% é excelente, 12-15% é a média do setor e acima de 20% é problema. Conflita com a eightx, então use as faixas como ordem de grandeza. — [beancount](https://beancount.io/pt/blog/2026/06/02/specialty-coffee-roaster-wholesale-bean-supplier-bookkeeping-green-coffee-lot-cost-roast-yield-loss-asc-606-subscription-deferred-revenue-section-263a-section-179-drum-roaster-sca-benchmarks-kpi-guide)
- [GLOBAL] Intervalo de recompra no atacado: 14-28 dias é saudável e acima de 45 dias é risco de churn ("SCA benchmarking", sem publicação específica identificada). — [beancount](https://beancount.io/pt/blog/2026/06/02/specialty-coffee-roaster-wholesale-bean-supplier-bookkeeping-green-coffee-lot-cost-roast-yield-loss-asc-606-subscription-deferred-revenue-section-263a-section-179-drum-roaster-sca-benchmarks-kpi-guide)
- [GLOBAL] LTV de café: programas fortes de assinatura geram US$ 400-900 em 12 meses, a média fica em US$ 200-400. A meta de LTV:CAC é de 3:1 a 6:1, e o CAC blended de A&B fica em US$ 35-55. No exemplo do artigo, o 1º pedido dá prejuízo (−US$ 17,80) e o LTV:CAC de 12 meses é ~2,2x. — [eightx](https://eightx.co/blog/coffee-brand-unit-economics)
- Fórmulas de LTV:
  - LTV receita = AOV × frequência × períodos ativos (soma da curva de retenção).
  - LTV contribuição = LTV receita × margem bruta.
  - Payback do CAC = CAC ÷ contribuição por período.
  - LTV:CAC acima de 3 é saudável e abaixo de 1 destrói valor.
  - Segmente por canal de aquisição e não extrapole 5 anos com poucos meses de dados.
  — [MetricGate](https://metricgate.com/docs/ltv-cac-ratio); [Retentionly](https://retentionly.io/post/ltv-cac-ratio-for-ecommerce)
- RFM, cálculo:
  - Dê nota de 1 a 5 em Recência (invertida: mais recente = 5), Frequência e Valor, por quintis. Com menos de ~500 clientes, use quartis.
  - Exclua contas B2B/atacado, porque uma única conta distorce F e M.
  - Recalcule pelo menos a cada trimestre (ideal: mensal).
  - RFM é descritivo, não preditivo.
  — [MetricGate RFM](https://metricgate.com/docs/rfm-segmentation/); [Bloomreach](https://documentation.bloomreach.com/engagement/docs/rfm-segmentation-explained)
- RFM, segmentos e ações (as faixas variam por ferramenta):

  | Segmento | Notas R/F/M | Ação |
  |---|---|---|
  | Champions | R, F e M 4-5 | VIP e lançamentos antecipados, sem desconto |
  | Loyal | 3-5 em tudo | Fidelidade, indicação, upsell |
  | Potential Loyalists | R 4-5, F e M 2-3 | Nutrição |
  | New | R 4-5, F 1 | Onboarding e educação |
  | Promising | R 3-4, F e M 1-2 | — |
  | Needs Attention | 2-3 em tudo | — |
  | About to Sleep | R 2-3, F e M 1-2 | — |
  | At Risk | R 1-2, F e M 3-5 | Contato pessoal e incentivo forte |
  | Cannot Lose Them | R 1-2, F e M 4-5 | Atenção individual prioritária |
  | Hibernating / Lost | Notas baixas | Automação barata ou parar de investir |

  — [ClawHub rfm-segmenter](https://clawhub.ai/leooooooow/rfm-segmenter); [Vellir](https://vellir.tech/blog/rfm-analysis-for-shopify)
- Churn B2B por cadência:
  - Sinalize quando os dias desde o último pedido passam de 2x a mediana do intervalo da conta. O padrão de uma ferramenta é 2x para contas B2B/atacado/distribuidor.
  - Exija no mínimo 3 pedidos e um piso de receita (ex.: receita dos últimos 12 meses).
  - Exclua pedidos cancelados e use lookback de 365 dias.
  - O multiplicador 2x é regra de bolso, não padrão do setor.
  — [Vortex IQ NetSuite](https://docs.vortexiq.ai/nerve-centre/kpi-cards/netsuite/customer-churn-signals); [Vortex IQ Shopify](https://docs.vortexiq.ai/nerve-centre/kpi-cards/shopify/customer-churn-risk)
- Sinais de churn no atacado: frequência caindo, pedidos menores, compra abaixo do ritmo histórico, categorias abandonadas, atrito de pagamento. A conta "vai apagando" sem cancelar. — [RepSpark](https://www.repspark.com/blog/using-data-to-prevent-b2b-buyer-churn); [Qymatix](https://qymatix.de/en/define-customer-churn-b2b/)
- [BR] Consumo per capita (nov/24 a out/25): 4,82 kg/ano de torrado e moído, ou seja, ~400 g/mês por pessoa. — [Safras/ABIC](https://safras.com.br/consumo-total-de-cafe-no-brasil-cai-231-e-soma-214-milhoes-de-sacas-em-2025-aponta-abic/); [CNN Brasil](https://www.cnnbrasil.com.br/economia/cnn-money/consumo-de-cafe-no-brasil-cai-quase-3-em-2025-diz-industria/)

### Inferences
- Ciclo de consumo B2C: a ~400 g/mês per capita, um pacote de 250 g dura ~2-3 semanas para uma pessoa e 500 g dura ~1 mês. Isso sugere marcar "atraso" no B2C quando o intervalo passa de ~1,5-2x o intervalo esperado pelo tamanho do último pedido (kg comprados ÷ consumo estimado). É inferência, para calibrar com o intervalo mediano real da base.
- Pacote de análises de cliente:
  1. Recompra 90/180/365 dias.
  2. Distribuição do intervalo 1º→2º pedido.
  3. Matriz de coortes (mês da 1ª compra × mês) em % de clientes ativos e em receita acumulada por cliente.
  4. LTV de contribuição em 12 meses por coorte e por canal.
  5. RFM B2C em quartis.
  6. Lista B2B de contas em risco: dias desde o último pedido ÷ mediana do intervalo ≥ 1,5 (atenção) ou ≥ 2 (risco), ordenada por receita dos últimos 12 meses.
  7. Pareto: % da receita nos top 10/20% clientes e participação do maior cliente.
- Concentração: com B2B, é comum poucos cafés/atacadistas responderem por grande parte da receita. Mostre a curva acumulada e um alerta quando um único cliente passar de X% (ex.: 10-15%). O limiar é inferência e não tem fonte.
- O CAC só existe se houver dado de mídia fora do Bling (Meta/Google Ads). O Bling não guarda custo de aquisição.

### Gaps
- Não há benchmark brasileiro público de churn ou ticket de clubes de assinatura de café (busca sem resultado; apenas casos como Boden Club, adquirida pela Tegrus em 2024). — [A Gazeta](https://www.agazeta.com.br/colunas/abdo-filho/boden-club-clube-capixaba-de-cafes-por-assinatura-e-vendido-0924)
- Não há dado público sobre consumo médio semanal de kg por cafeteria no Brasil, o que daria o volume esperado por conta B2B.
- Não há fonte para o limiar de concentração de cliente (Pareto).

## 3. Produtos e estoque: curva ABC, sell-through, cobertura, ruptura, frescor, desempenho de SKU, private label

### Takeaway
Faça a curva ABC duas vezes, por receita e por margem, porque um item de margem alta pode cair em B ou C na curva por receita. Combine com giro, cobertura em dias e ruptura. Café torrado é perecível sensorialmente: o estoque torrado deve ficar em poucos dias (meta citada: menos de 7 dias para grão e menos de 3 para moído), e o estoque relevante a planejar é o de café verde (giro de 4-6x ao ano).

### Cited Findings
- Fórmulas de giro e dias de estoque:
  - Giro = CMV do período ÷ estoque médio a custo.
  - Estoque médio = (estoque inicial + estoque final) / 2.
  - Dias de estoque = dias do período ÷ giro.
  - O giro deve ser lido junto com cobertura, ruptura e margem, porque giro alto demais pode indicar falta.
  — [Cursa](https://cursa.app/pt/pagina/giro-de-estoque-e-curva-abc-priorizacao-de-compras-e-mix); [E-Commerce Brasil](https://www.ecommercebrasil.com.br/artigos/fulfillment-estoque)
- Curva ABC: classificação por Pareto das saídas (quantidade e valor vendido no período). Os itens A giram mais que os C. Faça a curva por receita e também por lucro. — [Stone](https://conteudo.stone.com.br/curva-abc-estoque/); [Transfeera](https://transfeera.com/blog/curva-abc/)
- [GLOBAL] Benchmarks atribuídos à SCA:
  - Giro do café verde de 4-6x/ano é saudável; abaixo de 3 preocupa.
  - Estoque torrado: menos de 7 dias para grão e menos de 3 para moído.
  - Vida útil em política interna: 30 dias para grão e 14 dias para moído.
  - Perda de peso na torra: torra clara retém 85-87% do peso, média ~84%, escura perde 18-20%.
  - Sobrepeso na embalagem custa 1-2,5% de rendimento.
  — [beancount](https://beancount.io/pt/blog/2026/06/02/specialty-coffee-roaster-wholesale-bean-supplier-bookkeeping-green-coffee-lot-cost-roast-yield-loss-asc-606-subscription-deferred-revenue-section-263a-section-179-drum-roaster-sca-benchmarks-kpi-guide)
- Janela de frescor:
  - Desgaseificação rápida nas primeiras ~72 h.
  - Pico de sabor em ~4-5 a 14 dias pós-torra; consumir em até ~30 dias (Breville).
  - Moído fica "velho" em 7-14 dias; pacote de grão aberto, em 3-4 semanas.
  - A queda perceptível começa em 2-3 meses.
  - Use data de torra, não "melhor antes de".
  — [Breville](https://www.breville.com/us/en/blog/coffee-and-espresso/why-is-coffee-freshness-important.html); [Methodical Coffee](https://methodicalcoffee.com/blogs/coffee-culture/freshly-roasted-coffee-explained-degassing-rest-and-flavor); [1Zpresso](https://1zpresso.coffee/how-long-do-coffee-beans-last/)
- Fórmulas sem confirmação na busca (conhecimento geral):
  - Cobertura (dias) = estoque atual ÷ venda média diária recente.
  - Sell-through % = unidades vendidas ÷ unidades disponíveis ou recebidas no período.
  — [Cursa](https://cursa.app/pt/pagina/giro-de-estoque-e-curva-abc-priorizacao-de-compras-e-mix)

### Inferences
- Painel de SKUs:
  1. ABC por receita e por margem bruta, com matriz A/B/C × A/B/C.
  2. Desempenho por gramatura (250 g, 500 g, 1 kg), formato (grão/moído/drip/cápsula) e blend/origem, medido em kg, receita, margem e recompra de quem comprou o SKU.
  3. Cobertura em dias por SKU de torrado contra a meta de frescor (ex.: cobertura acima de ~14-21 dias em torrado sinaliza risco de café envelhecido).
  4. Cobertura do café verde em dias contra o lead time de compra e a safra.
  5. Ruptura: dias com saldo zero e pedidos perdidos ou atrasados.
- O Bling dá saldo por depósito (`/estoques/saldos`) e movimentações. A data de torra/lote normalmente não existe no Bling, a menos que se use lote, campo customizado ou ordem de produção. Sem isso, a idade do estoque só pode ser aproximada pela data da entrada no estoque.
- Private label: trate cada projeto como "cliente + SKU exclusivo", com receita, margem, volume mínimo, frequência de pedido e concentração. Benchmark citado: SKUs exclusivos de atacado com margem bruta acima de 40% (ver seção 4).
- Ordens de produção e "produtos - estruturas" (ficha técnica) do Bling podem modelar café verde → torrado → embalado e dar o CMV por SKU, se forem usados.

### Gaps
- Não encontrei fonte brasileira para benchmarks de ruptura ou cobertura de café torrado.
- Não encontrei dados públicos sobre o desempenho típico de gramaturas/formatos no mercado de especiais no Brasil.

## 4. Financeiro: margem por SKU/canal, margem de contribuição após mídia, frete, descontos, meios de pagamento, contas a receber B2B, ciclo de caixa

### Takeaway
A margem bruta deve partir do custo do café verde ajustado pela quebra de torra, mais torra, embalagem e mão de obra direta. Mostre margem bruta → margem de contribuição (− frete subsidiado, taxas de pagamento e marketplace, comissões) → contribuição após mídia. Referências estrangeiras: DTC de café com margem bruta de ~45-55%, CM após mídia de ~20-25%, torrefador focado em atacado com margem bruta de ~44%. No B2B, acompanhe contas a receber por idade (aging) e o prazo médio de recebimento.

### Cited Findings
- [GLOBAL] DTC de café:
  - Margem bruta "fully loaded" de 45-55% (típica 52%; top 55-60%+). CMV ≈ 45-55% da receita.
  - CM2 (antes de mídia) ~40%; CM3 (após mídia) ~20-25%, numa faixa DTC de 18-30%.
  - Taxas e fulfillment ~15% da receita.
  - AOV típico de US$ 45-85.
  — [eightx, jun/2026](https://eightx.co/blog/coffee-brand-unit-economics)
- [GLOBAL] Margens de empresas abertas: a margem bruta da Black Rifle caiu de 41,2% (FY24) para 34,6% (FY25), pressionada pelo verde caro e pelo mix de atacado. — [eightx](https://eightx.co/blog/coffee-brand-unit-economics)
- [GLOBAL] Margens atribuídas à SCA:
  - Torrefador focado em atacado: margem bruta ~44%. Torrefador com cafeteria própria: ~65%.
  - Lucro líquido: 5-8% no só-atacado e 11,92% no misto.
  - Metas de margem bruta: blends exclusivos acima de 55%, single origins acima de 50%, SKUs exclusivos de atacado acima de 40%.
  - Exemplo de prazo para atacado: 30 dias.
  — [beancount](https://beancount.io/pt/blog/2026/06/02/specialty-coffee-roaster-wholesale-bean-supplier-bookkeeping-green-coffee-lot-cost-roast-yield-loss-asc-606-subscription-deferred-revenue-section-263a-section-179-drum-roaster-sca-benchmarks-kpi-guide)
- CMV por kg: custo do verde ÷ rendimento da torra (0,80-0,88). Some embalagem (saco, válvula, rótulo), mão de obra, energia/gás, depreciação do torrador e perdas. Amostras de prova e descarte por validade vão para despesa separada. — [beancount](https://beancount.io/pt/blog/2026/08/12/specialty-coffee-roaster-bookkeeping-green-to-roasted-guide); [Wholesale Helper](https://wholesalehelper.io/pt/blog/wholesale-pricing-for-coffee-business/)
- [BR, anúncio de 2024] Torra terceirizada a ~R$ 12/kg, com mínimo de 10 kg por batelada. É um único anúncio. — [MF Rural](https://www.mfrural.com.br/detalhe/667072/torrefacao-de-cafe-especial)
- Precificação de atacado: a cafeteria pensa em custo por xícara, o varejo pensa em margem do revendedor, giro e validade. É preciso deixar margem para o revendedor. — [Wholesale Helper](https://wholesalehelper.io/pt/blog/wholesale-pricing-for-coffee-business/)
- [BR] Meios de pagamento:
  - 49% dos lojistas D2C da Nuvemshop usam Pix como principal forma de recebimento; o cartão de crédito respondeu por 42% das transações (2025).
  - Global Payments Report: Pix com 38% das transações de e-commerce no Brasil em 2025, mas cartão lidera em valor (40%).
  - As métricas das duas fontes não são comparáveis.
  — [Central do Varejo](https://centraldovarejo.com.br/lojistas-d2c-movimentam-r-58-bilhoes-em-2025-aponta-nuvemshop/?amp=1); [Let's Money](https://www.letsmoney.com.br/pagamentos/pix-ecommerce-38-global-payments-report/)
- [GLOBAL] Assinaturas: 25-40% do churn é involuntário (falha de cobrança). Isso importa para a análise de meio de pagamento e recorrência. — [eightx](https://eightx.co/blog/coffee-brand-unit-economics)

### Inferences
- Cascata por pedido/canal:
  1. Receita bruta − descontos = receita líquida.
  2. Receita líquida − impostos sobre venda (Simples/DAS ou ICMS/PIS/COFINS conforme o regime) = receita após impostos.
  3. Receita após impostos − CMV = margem bruta.
  4. Margem bruta − frete não repassado − taxas de gateway/cartão/Pix − comissão de marketplace − comissão de vendedor = margem de contribuição.
  5. Margem de contribuição − mídia = contribuição após mídia.
- Indicadores derivados:
  - Impacto do frete = frete pago pela empresa − frete cobrado do cliente, em % da receita.
  - Desconto médio % = descontos / receita bruta, por canal e por cupom.
- Contas a receber B2B (Bling `contas/receber`):
  - Aging (a vencer, vencido 1-30, 31-60, mais de 60 dias).
  - PMR/DSO = contas a receber ÷ receita a prazo × dias.
  - Inadimplência % por cliente.
- Ciclo de conversão de caixa = dias de estoque (verde + torrado) + PMR − PMP (prazo médio de pagamento a fornecedores, via contas a pagar). Café verde comprado na safra alonga o ciclo.
- Mix B2B: o B2B tende a ter margem bruta menor (~40-44% nas referências estrangeiras) e prazo, mas frete e CAC baixos. Compare o B2B pela margem de contribuição, não pela margem bruta.

### Gaps
- Não encontrei benchmarks brasileiros de margem de torrefação de especiais, nem tabela atual de preço de atacado de café torrado no Brasil.
- Não encontrei o custo atual do café verde especial no Brasil (indicador Cepea/arábica) nesta rodada.
- Não verifiquei taxas de MDR, Pix e boleto de 2025-26.

## 5. O que o Bling expõe (API v3) e dashboards típicos de PMEs com Bling

### Takeaway
A API v3 do Bling usa OAuth 2.0 e cobre tudo o que essas análises pedem: pedidos de venda, NF-e/NFC-e, produtos e variações, estoques/depósitos, contatos e tipos, vendedores, formas de pagamento, contas a receber e a pagar, canais de venda, ordens de produção, entre outros. Os limites são 3 requisições/s e 120 mil/dia, e filtros de data não podem passar de 1 ano. O dashboard típico de PME é um conector (ex.: Kondado) levando dados ao Looker Studio ou Power BI.

### Cited Findings
- Recursos v3 (lista de um SDK comunitário):
  - Vendas e fiscal: pedidos de venda, pedidos de compra, NF-e, NFC-e, NFS-e, propostas comerciais, contratos, canais de venda, naturezas de operação, situações.
  - Produtos e estoque: produtos, variações, estruturas, fornecedores, produtos por loja, grupos de produtos, categorias de produtos e lojas, depósitos, estoques, ordens de produção.
  - Cadastros: contatos, tipos de contato, vendedores, usuários, empresas, campos customizados.
  - Financeiro: formas de pagamento, contas a receber, contas a pagar, borderôs, categorias de receitas/despesas, contas contábeis.
  - Logística: serviços, remessas, etiquetas.
  — [Packagist alebatistella/bling-erp-api](https://packagist.org/packages/alebatistella/bling-erp-api)
- Endpoints e filtros:
  - `GET /pedidos/vendas` com filtros `dataInicial/dataFinal`, `idContato`, `numero`, e `GET /pedidos/vendas/{id}` para o detalhe. A rota `/pedidos` virou `/pedidos/vendas` na v3.
  - `GET /nfe` com filtros de data de emissão, situação e tipo.
  - `GET /produtos`.
  - `GET /estoques/saldos` por id ou SKU.
  - `GET /formas-pagamentos`.
  — [Bling MCP (getdrio)](https://www.getdrio.com/mcp/io-github-mcp-dir-bling-mcp/md); [Blog Bling: nova API](https://blog.bling.com.br/?p=14750)
- `GET /contas/receber` aceita filtros de emissão, vencimento, situação e contato. Também existem `GET /contas/receber/{id}` e `POST /contas/receber/{id}/baixar`. A listagem de contatos aceita filtro por `idVendedor` e `uf`. — [Koncili](https://developers.koncili.com/en/docs/direct-erp-integration/bling/technical-information/)
- OAuth 2.0: autenticação em www.bling.com.br e API em api.bling.com.br. Não há sandbox (tudo é produção). — [Koncili](https://developers.koncili.com/en/docs/direct-erp-integration/bling/technical-information/); [Blog Bling](https://blog.bling.com.br/?p=14750)
- Limites oficiais:
  - 3 req/s e 120.000 req/dia por conta; acima disso, HTTP 429.
  - Filtro de período acima de 1 ano retorna 400.
  - Bloqueios de IP de 10 min (300 erros em 10 s ou 600 req em 10 s) e de 60 min (20 chamadas a /oauth/token em 60 s).
  — [Bling Developer – Limites](https://developer.bling.com.br/limites)
- Dashboards: a Kondado oferece um template Bling → Looker Studio. O Looker Studio é gratuito e aguenta ~5 mi de linhas; acima disso, Power BI ou BigQuery. — [Kondado](https://kondado.io/en/reports/dashboard-bling-looker-studio.html); [Piotr Litwa](https://piotrlitwa.com/articles/en/looker-studio-what-is-it-guide.html)

### Inferences
- Pelo limite de 1 ano por filtro e 3 req/s, a carga histórica deve ser incremental, mês a mês, com cache local (ex.: Postgres). A listagem de pedidos não traz itens, então é preciso chamar o detalhe de cada pedido (`/pedidos/vendas/{id}`).
- Campos do pedido v3, por conhecimento geral e não verificados nesta pesquisa: número, data, data de saída, contato (id/nome/documento), situação, loja/canal, vendedor, itens (código/SKU, quantidade, valor, desconto), totalProdutos, total, desconto, transporte/frete, parcelas com forma de pagamento, intermediador/taxas de marketplace e nota fiscal vinculada. Confirmar no schema oficial.
- Para CMV, o Bling tem preço de custo no produto e pode ter custo nas estruturas e ordens de produção. A qualidade da margem depende de o custo estar cadastrado e atualizado (o café verde varia muito).
- Use o pedido de venda para a visão comercial (inclui não faturados) e a NF-e para a visão fiscal/faturada. Escolha uma como fonte oficial da receita e trate cancelamentos e devoluções (NF-e de entrada).

### Gaps
- Não consegui ler o schema oficial do pedido de venda (a página de referência é renderizada em JS). Os campos acima ficam pendentes de verificação.
- Não encontrei a lista de relatórios nativos do Bling (ex.: curva ABC nativa) nem pesquisas sobre quais dashboards as PMEs brasileiras mais usam.
