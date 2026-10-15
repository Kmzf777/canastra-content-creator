# Estado da arte: como os profissionais pesquisam e diagnosticam marketplaces

Frente: MÉTODO · Data da pesquisa: 2026-10-14 · Escopo: Mercado Livre, Shopee e Amazon (Brasil), com referência a métodos consolidados na Amazon dos EUA.

Como ler este documento
- Cada afirmação traz fonte, data da fonte e TIPO: [OFICIAL] regra/tarifa/política dita pela plataforma · [PRÁTICA] tática de praticante · [CASE] números de uma operação · [DADO] estudo, relatório ou ferramenta · [OBS] observação direta.
- "s/d" = a fonte não mostra data; vale a data de acesso (2026-10-14).
- Regras de plataforma com mais de 6 meses (anteriores a 2026-04-14) ou sem data levam o aviso **(pode estar superada)**. Princípios e métodos valem sem corte, com a data anotada.
- O marcador **[REVENDA]** indica o que é específico de revenda, dropshipping ou importação. **[MARCA]** indica o que vale para indústria e marca própria. Sem marcador, vale para os dois.
- Este documento descreve como o mercado faz pesquisa. Não traz recomendação para nenhuma empresa.

---

## 1. Visão geral: as quatro camadas de dado que todo profissional combina

A leitura das fontes mostra que ninguém sério depende de uma camada só. Os profissionais cruzam quatro camadas (síntese desta frente a partir das seções 2 a 7):

| Camada | O que é | Exemplos | Confiabilidade |
|---|---|---|---|
| 1. Dado próprio da plataforma (1ª parte) | Painéis do vendedor e relatórios da plataforma, com números reais | ML "Métricas > Análise de mercado"; Amazon Brand Analytics (SQP, Top Search Terms, Market Basket, Repeat Purchase); Shopee Business Insights; Product Opportunity Explorer | Alta para a própria conta; parcial para o mercado (a plataforma mostra só o que quer, e muitas vezes exige vender na categoria) |
| 2. Estimativa de ferramenta (3ª parte) | Modelos que inferem vendas a partir de sinais públicos (BSR, contador de vendidos, visitas, estoque) | Jungle Scout, Helium 10, SmartScout; Nubimetrics, Avantpro, JoomPulse, UpSeller, RadarSeller | Direcional; erro declarado de 10% a 40% conforme categoria e fonte |
| 3. Prateleira digital e mídia (indústria) | Raspagem sistemática de buscas e páginas: share of search, preço, ruptura, conteúdo; dados de Ads | Profitero, Lett (Neogrid), Flywheel, Pacvue, Perpetua | Boa para tendência; mede a página, não o comprador |
| 4. Estudos de mercado e balanços | Relatórios com metodologia, cartas a acionistas, painéis de consumo | MELI e Sea (relatórios trimestrais), NIQ Ebit Webshoppers, Pacvue/Jungle Scout benchmarks, ABComm | Alta quando há metodologia publicada; agregada demais para decisão de SKU |

Ponto de método que se repete em todas as fontes: **estimativa serve para eliminar e priorizar, não para projetar receita** (Jungle Scout e SmartScout dizem isso dos próprios números; ver 3.1 e 3.3).

---

## 2. Mercado Livre e Shopee: ferramentas de inteligência e como são usadas

### 2.1 A ferramenta oficial do Mercado Livre: "Métricas > Análise de mercado"
- Fica em Vendas > Métricas, aba "Análise de mercado", com duas abas: Concorrência e Oportunidades de venda. [PRÁTICA] demonstração em tela, Hugo Vasconcelos, YouTube S4jpAl3b4l0, 2025-10-20; [PRÁTICA] Gabriel Paiova (Mamba Digital), YouTube 5VxP5E6H6T0, 2025-12-23. A ferramenta é oficial; a descrição vem de demonstrações de praticantes **(pode estar superada)**.
- **Concorrência:** ranking dos vendedores da categoria por faturamento, com o vendedor mostrado por apelido, não pelo nome. O usuário vê os concorrentes próximos da sua posição e os "melhores vendedores" (cerca de top 50). A opção "comparar-me" mostra o mix do concorrente, as vendas por anúncio, a conversão e as visitas. Mostra também a proporção de uso de alavancas: Full, publicidade, frete grátis, cupons, Premium, parcelado, catálogo. [PRÁTICA] 5VxP5E6H6T0 e S4jpAl3b4l0.
- Técnica de praticante para estimar o gasto em Ads do concorrente: o painel mostra a participação de cada loja no investimento em publicidade da categoria. Com o próprio gasto conhecido, uma regra de três dá a ordem de grandeza do gasto alheio. [PRÁTICA] 5VxP5E6H6T0, 2025-12-23.
- **Oportunidades de venda:** tendência de vendas brutas por categoria e subcategoria, que serve como teto de mercado ("tamanho da categoria"). Mostra a distribuição de vendedores por medalha e a participação das condições de venda: % no Full, % em promoção, % parcelado, % com clips. Mostra também a sazonalidade anual, os top 100 anúncios com experiência de compra e qualidade, e os "mais vendidos em outras plataformas". [PRÁTICA] 5VxP5E6H6T0.
- Restrição de acesso: o detalhe só aparece em categorias onde o vendedor já vende. As exigências citadas divergem. Paiova fala em R$ 300 em vendas. Vasconcelos fala em cerca de R$ 1.500 a R$ 2.000 em 60 dias, ou 10 vendas num anúncio. Fora disso, a ferramenta mostra o ranking sem números. [PRÁTICA] 5VxP5E6H6T0; S4jpAl3b4l0 **(pode estar superada)**.
- Contexto: praticantes relatam que o ML restringiu a API usada por ferramentas de terceiros. A Nubimetrics passou a mostrar "share" em vez de valores absolutos, a não ser que o usuário "siga" o anúncio ou o vendedor. [PRÁTICA] Roderjan Svolinski, YouTube l8q-Rkw26vM, 2026-01-17; S4jpAl3b4l0.
- Fonte oficial gratuita complementar: **tendencias.mercadolivre.com.br**. Mostra as buscas que mais cresceram, as mais desejadas e as mais populares, por categoria, com atualização semanal. A descrição vem de terceiros: [PRÁTICA] gosmarter.com.br/mercado-livre-tendencias-como-usar/, s/d.

### 2.2 Nubimetrics (ML; Argentina, no Brasil desde 2016)
- Lógica de oportunidade publicada pela própria empresa: cruzar **crescimento de vendas** com **saturação**, isto é, número de vendedores e proporção de MercadoLíderes Gold e Platinum. Poucas medalhas altas indicariam uma entrada mais fácil. A empresa olha também sazonalidade, ranking de palavras buscadas, títulos dos top sellers e benchmarking. [DADO] academia.nubimetrics.com/pt/como-detectar-oportunidades-no-mercado-livre, 2022-05-24.
- Market share, segundo a empresa: comparar o crescimento próprio (receita e unidades) com o da categoria no mesmo período. Crescer menos que a categoria significa perder participação. A empresa acompanha também a posição no ranking de vendedores. [DADO] academia.nubimetrics.com/pt/market-share-aumente-sua-participacao-nos-marketplaces, 2022-02-15.
- Os termos de uso dizem que os números são estimativas e tendências, não dados exatos. [DADO] nubimetrics.com/pdf/terminos_pt.pdf, s/d.
- Crítica de praticante, útil como método: o semáforo "oportunidade alta" costuma apontar nichos de volume baixo. O praticante ignora o score e olha volume absoluto, preço, margem possível e qualidade dos anúncios líderes (Full, catálogo, estoque, título). Os módulos mais úteis, para ele, são o "explorador de anúncios" e o "seguir anúncio/vendedor": vendas semanais e mensais, histórico de preço e de estoque, data de criação do anúncio. [PRÁTICA] [REVENDA] l8q-Rkw26vM, 2026-01-17.
- Exemplo de conteúdo fraco no próprio canal da ferramenta: um podcast afirma que empresas com IA crescem "15% nas vendas" e que "75%" das grandes já usam algoritmos, sem metodologia, e fecha com chamada para baixar material. [OBS] YouTube Qz5h-uGRRI0 (Nubimetrics), 2026-03-04.

### 2.3 Avantpro (extensão de navegador; ML, com combos para outros marketplaces)
- Função declarada: acompanhar vendas diárias, conversão e visitas mensais de anúncios concorrentes no ML. [DADO] mwm.ai/apps/avantpro/1620213822, s/d. A cobertura de Shopee e Amazon aparece em vídeos do próprio canal (MrUxBGCSXiE, kNSL7_c8MLM). Não foi confirmada em página oficial.
- **Método de análise da primeira página**, ensinado pela empresa ([PRÁTICA] [REVENDA], YouTube KdwwoYN4S4s, 2025-11-21, e 4Ygmkz4y5Sk, 2025-12-26). Para cada termo de busca, monta-se uma planilha que pontua +1 ou -1 por critério e soma o total:
  - número total de resultados da busca (quantas páginas o anúncio novo terá de subir);
  - presença de vendedores sem medalha ou "Líder" na 1ª página (competir "de igual para igual");
  - número de anúncios no Full;
  - número de anúncios em promoção, frete grátis, catálogo e patrocinados;
  - número de anúncios internacionais (prazo longo vira vantagem para quem tem estoque local);
  - número de vendedores distintos na 1ª página;
  - idade do anúncio contra vendas acumuladas, e histórico de 12 meses de visitas e vendas estimadas, para separar demanda atual de demanda passada.
- O método é pensado para quem entra como novato e revende produto existente. Para marca própria, a lógica de "competir com quem não tem Full" tem pouco uso.
- Recurso "Hype": agrupa anúncios (por exemplo, todos os de um concorrente) para acompanhar vendas de 30 dias, visitas, troca de share entre vendedores, catálogo ou não, loja oficial e margem de contribuição estimada. [PRÁTICA] YouTube jzHBIQoiLg8, 2026-08-07.
- Os vídeos repetem afirmações sem base: "90% das vendas" na 1ª página e "promoção mostra o anúncio para 100 pessoas em vez de 10". São bons exemplos de número sem fonte (ver protocolo).

### 2.4 Outras ferramentas de ML e Shopee citadas por praticantes
- **UpSeller (ERP):** monitora lojas concorrentes (preço, unidades, faturamento, visitas, conversão por anúncio), com limite de lojas por plano. Tem sugestão e ajuste automático de preço no ML. [DADO] upseller.com/pt/help-doc-article-535 e -1800, s/d.
- **RadarSeller (Shopee):** vendas de 1, 7 e 30 dias por anúncio, top 10 por categoria, um índice próprio ("radar de vendas") sem fórmula publicada e análise de variações (qual cor ou tamanho vende). [PRÁTICA] [REVENDA] YouTube u_TBZZhXBrI, 2026-03-05. Índice proprietário, sem método divulgado: tratar como caixa-preta.
- **JoomPulse, GoSmarter, Hunter Spy, Real Trends:** citados como alternativas. Nenhuma publica metodologia de estimativa. Comparativos entre elas vêm de concorrentes (por exemplo, gosmarter.com.br compara-se com a Avantpro), o que é conflito de interesse.
- **Shopee, painel próprio (Business Insights):** visitantes, cliques em produto, pedidos, conversão (pedidos ÷ cliques em produto), ticket médio, cancelados e devolvidos, ranking de produtos e funil visualização → carrinho → pedido. [PRÁTICA] bigseller.pro/blog/articleDetails/3631, s/d (descrição de terceiro, nomes podem variar no BR) **(pode estar superada)**.
- **Shopee Ads:** desde 2026-01-16, em pelo menos um mercado, a métrica "GMV" virou "Sales", que exclui taxas pagas pelo comprador. Há atribuição "direta" (só o item anunciado) e "ampla" (qualquer item da loja). [PRÁTICA] bigseller.pro (Malásia), 2026; não confirmado para o Brasil. No GMV Max, a Shopee sugere faixas de ROAS-alvo, e metas altas demais travam a entrega. [OFICIAL] ads.shopee.sg/learn/faq/471/1787, s/d (Singapura) **(pode estar superada)**.

---

## 3. Amazon: ferramentas de pesquisa e o que medem

### 3.1 Jungle Scout
- Estimativa de vendas ("AccuSales") a partir de BSR e de dados de "milhões de produtos". O BSR pesa vendas recentes e históricas e muda de hora em hora. Um mesmo BSR rende volumes diferentes conforme o mês e a categoria. [DADO] junglescout.com/blog/amazon-sales-rank, s/d.
- Filtros de pesquisa de produto: categoria, demanda mensal, preço, número de reviews e nível de competição. O Opportunity Score acima de 7 seria sinal forte, e o Niche Score combina demanda e competição. A fórmula não é publicada. [DADO] junglescout.com (?p=3945), s/d; [PRÁTICA] gorillaroi.com/compare/jungle-scout-review, s/d.
- Acurácia autodeclarada de 84%, e "20% mais preciso que o concorrente mais próximo". Sem auditoria independente. [DADO] junglescout.com/enterprise/products/cobalt/, s/d.
- **Cobalt (enterprise):** share de mercado por marca e categoria, crescimento da categoria, share de Buy Box, share of voice, preço e disputa 1P/3P, para marcas com mais de US$ 1 milhão por ano. [DADO] junglescout.com/enterprise/, s/d. **[MARCA]**
- Relatório "Amazon Benchmark Report 2026" (14 categorias): unidades crescem mais rápido que receita, o CPC sobe e a vantagem vem de execução (busca, preço, sortimento), não de escala. Números atrás de formulário. [DADO] junglescout.com/resources/reports/amazon-benchmark-report-2026, 2026.
- Alerta de praticante: nicho com "demanda alta e baixa competição" pode ter conversão baixa. O score não mede conversão nem margem. [PRÁTICA] closo.co, s/d.

### 3.2 Helium 10
- Sequência descrita pela empresa: **Black Box** para descobrir ideias (filtros de preço, receita mensal, vendas, reviews, tamanho, competição; refinar se passar de 200 resultados). **Cerebro** para engenharia reversa de palavras-chave a partir do ASIN do concorrente. **Market Tracker** para monitorar depois do lançamento. [DADO] helium10.com/blog/competitor-amazon-research-with-market-tracker, s/d; kb.helium10.com/hc/en-us/articles/6710274045339, s/d.
- No Market Tracker, "mercado" é o conjunto de concorrentes e produtos, com a receita total do grupo, a sua incluída. As 5 palavras-chave iniciais não podem ser trocadas depois. [DADO] helium10.com (?p=15400), s/d.
- **TACoS** = gasto total em Ads ÷ receita total (orgânica + paga). A Helium 10 não dá benchmark universal. Um TACoS estável ou em queda enquanto as vendas sobem indica que o Ads alimenta o orgânico. [DADO] helium10.com/blog/what-is-amazon-tacos/, 2024-03-18. Faixas de 7% a 15% para produto maduro aparecem em blogs, sem base metodológica. [PRÁTICA] adbadger.com, s/d.

### 3.3 SmartScout
- Unidade de análise: **marca** e **subcategoria**. Cobre mais de 42 mil subcategorias em 11 marketplaces. Por subcategoria mostra receita mensal, número de vendedores, preço médio, share da Amazon varejista, top marcas com share de receita, crescimento em 12 meses e **Ad Spend Share** (investimento em Ads contra share de vendas, usado como indicador antecedente). [DADO] smartscout.com/amazon-selling-guides/how-to-know-amazon-market-share-by-category..., 2025-12-03.
- Leitura de concentração: campo fragmentado sugere abertura; uma marca com cerca de 70% sugere entrada difícil. [DADO] mesma fonte.
- Método de estimativa: BSR por produto, receita do rank dividida entre os ASINs filhos com peso por reviews, validação com Keepa e com dados reais de parceiros, e uso do selo "x+ comprados no mês". Acurácia declarada pelo fundador de 80% a 90% na maioria das marcas. [DADO] smartscout.com/smartscouts-accuracy-vs-amazons-reliability, s/d.
- Traffic Graph: mostra como o comprador navega entre produtos e é usado para achar vizinhos e variações que ampliem share. Metodologia não publicada. [DADO] mesma família de páginas, s/d. **[MARCA]**

### 3.4 Dado de 1ª parte da Amazon (o que agências usam primeiro)
- **Brand Analytics** (exige conta Profissional e Brand Registry). [OFICIAL] sell.amazon.com/tools/amazon-brand-analytics, s/d:
  - Search Query Performance: volume da busca, impressões, cliques, carrinho e compras, com o share da marca em cada etapa;
  - Search Catalog Performance: onde o comprador abandona, por ASIN;
  - Top Search Terms: os top 3 produtos, categorias e marcas por termo, com click share e conversion share;
  - Market Basket: o que é comprado junto;
  - Repeat Purchase Behavior: pedidos, vendas de recompra e clientes recorrentes;
  - Demographics e Customer Loyalty Analytics.
- Método diagnóstico baseado no SQP: comparar os shares ao longo do funil. Exemplo de agência: 12% de share de impressão com 3% de share de clique aponta problema de apresentação do anúncio (imagem, preço, título, nota). [PRÁTICA] perpetua.io/blog-amazon-search-query-performance e adbadger.com, s/d.
- **Product Opportunity Explorer:** agrupa "nichos" por comportamento de busca e compra, não por categoria. Mostra volume de busca e crescimento em 90 dias, unidades vendidas (em faixa), temas de reviews, motivos de devolução, taxa de ruptura e qualidade de listing. Gratuito no Seller Central. [PRÁTICA] amalytix.com e ecombrainly.com, 2026 (descrição de terceiros) **(pode estar superada)**.

---

## 4. Mídia de varejo (Ads): como plataformas e agências avaliam

- **Pacvue:** acompanha Share of Shelf, SOV pago, SOV de Sponsored Products, SOV de Sponsored Brands e SOV orgânico. Publica benchmarks trimestrais (Q1 e Q2 2026) de CPC, ROAS e CVR por retailer, com números atrás de formulário. No Q1 2026, o CVR de Sponsored Brands subiu 25,6% e o de Sponsored Products 3,9% na comparação anual. [DADO] pacvue.com/guides-reports/2026-q1-retail-media-benchmark-report/, 2026. Pelo resumo de terceiro do relatório de meio de ano, o gasto diário em SB subiu 26,1% e em SP 21,2% no ano. [DADO] bebolddigital.com/news/amazon-q2-2026-retail-media-benchmarks, 2026.
- **Perpetua (Flywheel/Omnicom):** otimização por objetivo, com metas de ACOS e orçamento separadas para segmentos de marca, concorrente e categoria. Usa SOV e rank orgânico por hora para ajustar lances (dayparting) e protege termos de marca. [PRÁTICA] perpetua.io/blog/increase-amazon-share-of-voice/, 2022-04-07; help.perpetua.io/en/articles/6337493, s/d.
- **Flywheel no Mercado Livre:** integrou dados do Mercado Ads (Brasil e México) com visão de share of voice pago e orgânico, consolidação de investimento e dados para lances. O módulo de Share of Search cobre Amazon, ML, Magalu e TikTok Shop. [DADO] propmark.com.br (?p=121386 e ?p=133720), s/d. **[MARCA]**
- **Mercado Ads, regras públicas:** Product Ads cobra por clique. A elegibilidade citada é de 15 dias de cadastro, vendas mínimas e reputação amarela ou melhor. Brand Ads exige loja oficial ou "Minha página", reputação verde e 3 anúncios, e o leilão combina CPC máximo com a probabilidade de conversão. Em junho de 2026, a Argentina anunciou a migração de parte das campanhas de Brand Ads para Product Ads. [OFICIAL] developers.mercadolivre.com.br/introducao-ao-mercado-ads e developers.mercadolibre.com.ar, s/d e 2026-06 **(pode estar superada; confirmar no BR)**.
- Agências latino-americanas relatam a troca de "ACOS objetivo" por "ROAS objetivo" no Product Ads (AR, MX, CO, CL). Guias brasileiros de 2026 ainda falam em ACOS-alvo de 10% a 25% conforme margem. [PRÁTICA] algoritmodigital.com.ar, 2025; gosmarter.com.br/mercado-ads-product-ads-guia-2026/, 2026. Ponto aberto: verificar no painel brasileiro.
- **Escala do Mercado Ads:** receita +62% no ano (sem efeito câmbio) no 2T26, primeira vez acima de 10% do mercado de publicidade digital da América Latina. Adoção do orquestrador de orçamento por IA +63% no trimestre. [OFICIAL] MELI 8-K, sec.gov ...meli-20260805xex991.htm, 2026-08-05.
- **Shopee Ads:** receita de Ads +70% e take rate de Ads +90 bps no ano no 2T26 (dado global). [OFICIAL] Sea, transcrição 2T26, cdn.sea.com, 2026-08-11.
- **Incrementalidade (o que separa agência boa de agência média):**
  - ROAS, ACOS, TACOS e new-to-brand não provam causalidade;
  - o teste é a pausa ou o holdout de termos de marca, medindo a receita **total**;
  - num caso de agência, pausar Sponsored Products de marca derrubou as vendas totais em 8%, contra os 40% que o relatório anterior sugeria [CASE] neato.com/blog/amazon-advertising-transparency..., s/d;
  - Amazon Marketing Cloud permite grupos de teste [DADO] adexchanger.com, s/d;
  - canibalização é mais aguda quando o ASIN já é 1º no orgânico e também paga topo de busca [PRÁTICA] perpetua.io/blog-branded-traffic-strategy-amazon-ads/, s/d.
- **Pré-requisito antes de investir ("retail readiness"):** imagens completas, título e bullets, nota e quantidade de reviews mínimas, Buy Box e estoque para aguentar o pico. Sem isso, o gasto em Ads se perde. As faixas mais citadas são 15 reviews e nota 3,5 ou mais, ambas de agências, não da Amazon. [PRÁTICA] perpetua.io/blog-how-to-succeed-on-amazon-retail-readiness-checklist/, s/d; adspert.net/retail-readiness/, s/d.

---

## 5. Prateleira digital (digital shelf): o método da indústria **[MARCA]**

- **Métricas-padrão:**
  - Share of Search: % das posições de uma busca ocupadas pela marca, separado em orgânico e patrocinado, por termo, posição e varejista;
  - Content Score: completude e qualidade de título, imagens, bullets, A+ e especificações;
  - Availability: ruptura, que derruba venda e rank orgânico;
  - Price: índice de preço e Buy Box;
  - Ratings & Reviews.
  [DADO] profitero.com/blog/what-is-digital-shelf-analytics, s/d; koji.so/blog/share-of-search-digital-shelf-2026, 2026; priceva.com, 2026.
- Variante: "Share of Shelf" medido pelo número de resultados da marca entre os top 20 das palavras relevantes. [DADO] y1.de, s/d.
- Limite metodológico: o share of search mede a página raspada, não o comprador. Resultados personalizados e experimentos da plataforma fazem a raspagem diferir do que cada pessoa vê. [DADO] koji.so, 2026.
- Afirmação muito repetida, "1 ponto de share of search ≈ 0,5 ponto de market share", atribuída à Profitero. Não verificada na fonte original. [DADO] 42signals.com, 2025. Tratar como não confirmada.
- Origem do conceito fora do marketplace: Les Binet (IPA, 2020) mostrou que o share de buscas orgânicas de marca no Google antecede o market share. A antecedência foi de cerca de 6 meses em celulares, 0 a 3 meses em energia e 9 a 12 meses em automóveis. "Extra share of search" (busca acima do market share) indica crescimento futuro. Binet avisa que preço e conversão interferem. [DADO] ipa.co.uk/news/binet-presents-fast-cheap-predictive-share-of-search-metric, 2020; warc.com, 2020.
- **Brasil:**
  - Lett, adquirida pela Neogrid em 2021, atende PepsiCo, Danone, Mondelez, P&G, Ambev e Reckitt [DADO] baguete.com.br, s/d;
  - caso 3 Corações: o diagnóstico apontou descrições faltando, pouca oferta nos varejistas parceiros e baixa visibilidade em busca; em 5 meses vieram +11% em vendas de cápsulas ao consumidor, +27% no uso de imagens secundárias e +56% em máquinas no Carrefour [CASE] baguete.com.br/noticias/3-coracoes-reformula-presenca-digital-com-lett, 2025-06-16 (números da reportagem, sem auditoria).
- **Índice de preço, método:**
  - índice par a par = (preço próprio ÷ preço do concorrente) × 100, em produtos casados por GTIN, marca e tamanho de embalagem;
  - o índice da categoria pondera por venda, giro ou popularidade de busca, porque o índice sem peso supervaloriza item parado;
  - para série temporal, usar o índice de Lowe, com cesta fixa do período-base: Σ(pₜ·q₀) ÷ Σ(p₀·q₀) × 100;
  - na média sem peso, usar a geométrica;
  - não misturar canais na mesma série.
  [DADO] abs.gov.au, metodologia de índices de preço, 2022; priceshape.com/resources/glossary/competitor-price-index, s/d.

---

## 6. Agências e consultorias: como estruturam auditoria e diagnóstico

### 6.1 Amazon (agências dos EUA, método mais documentado)
- **Escopo típico de auditoria completa (9 áreas):** Ads, SEO, listings, Brand Registry, saúde da conta, estoque, expansão internacional, atendimento e lucratividade. Cada achado é registrado como **evidência → diagnóstico → risco de não agir → próximo passo**, e os achados são priorizados por risco e impacto financeiro. [PRÁTICA] salesduo.com/blog/amazon-account-management-services-checklist-audit, s/d; estorefactory.com/blog/amazon-account-audit-checklist/, s/d.
- **Ads na auditoria:**
  - cruzar Ads com margem, estoque, conversão, venda orgânica e qualidade da oferta;
  - separar gasto de marca e gasto genérico;
  - verificar se o pago está só substituindo o orgânico;
  - checar se há Ads escalando em produto sem estoque;
  - julgar o ACOS contra a margem, não sozinho.
  [PRÁTICA] myamazonguy.com/advertising/amazon-ppc-audit-checklist/, s/d.
- **Saúde da conta (limites mais citados, fonte de terceiros):**
  - ODR abaixo de 1%;
  - atraso de envio abaixo de 4% (só FBM);
  - cancelamento pré-envio abaixo de 2,5%;
  - rastreio válido de 95% ou mais;
  - Account Health Rating de 0 a 1.000, com "saudável" a partir de 200.
  Praticantes usam alerta interno em cerca de 50% do limite. [PRÁTICA] sellersprite.com/en/blog/amazon-account-health-rating-2026, 2026; blog.adnabu.com, s/d **(confirmar no Seller Central; não é texto oficial)**.
- **Estoque FBA, IPI:** escala de 0 a 1.000, atualizado semanalmente. Componentes: estoque excedente, sell-through, estoque encalhado e in-stock dos itens principais. O limite mais citado é 400, com uma fonte falando em 350 em 2026. Abaixo dele vêm limite de armazenagem e restrição de envio. [PRÁTICA] sellerlabs.com/blog/amazon-ipi-score-2026/, 2026; webgility.com, 2026 **(conflito entre fontes; confirmar)**.
- **Lucratividade por SKU (escada de margem de contribuição):**
  - CM1 = receita − CPV − comissão − fulfillment;
  - CM2 = CM1 − Ads;
  - CM3 = CM2 − devoluções, armazenagem e outros variáveis (a definição varia entre fontes).
  ACOS de equilíbrio = margem antes de Ads ÷ preço; SKU com ACOS real acima disso perde dinheiro em cada venda via Ads. Uma referência de mercado sugere CM1 de 35% ou mais para produtos dependentes de Ads. [PRÁTICA] novadata.io/resources/blog/amazon-contribution-margin-calculator, 2026; eightx.co, 2026. Benchmark de margem por vertical (Grocery & Gourmet com mediana de 11%) vem de base de clientes da ferramenta, sem auditoria. [DADO] novadata.io, 2026.
- **Recompra (consumíveis):** benchmark de agência de 30% ou mais de compradores recorrentes como alvo. A agência diz não ter visto marca de 7 dígitos lucrativa abaixo de 25%. Dado autocompilado. [PRÁTICA] amazondigest.beehiiv.com/p/the-case-for-repeat-buyers, 2024. **[MARCA]**
- **Avaliação da própria agência:** quem é dono de cada função, se o relatório mostra decisões e riscos (não só prints de venda), quem é dono dos dados, cláusulas de saída. [PRÁTICA] salesduo.com/blog/amazon-account-management-agency-checklist, s/d.
- **Selos:** a Amazon Ads Partner Network tem os níveis Registered, Verified e Advanced. Os critérios incluem certificações e gasto gerido, sem limites públicos. [PRÁTICA] supplykick.com/blog/amazon-ads-partner-network, s/d. Não foi achada lista de critérios para o Brasil.

### 6.2 Mercado Livre e Shopee (agências e consultorias brasileiras)
- **Mamba Digital** (Mamba Consultoria de Marketplace Ltda, Santos-SP; atende ML, Shopee e Amazon, conforme o perfil no Reclame Aqui, s/d) apresenta "consultor oficial do Mercado Livre". O método público visto é a leitura do painel oficial de Análise de mercado. Primeiro define-se o objetivo (concorrentes, tendência, produtos em alta, novos produtos do concorrente). Depois vêm concorrentes do mesmo porte, top vendedores e sua evolução, teto da categoria contra a meta, mix de medalhas, % de condições de venda, sazonalidade e experiência de compra dos top 100. O vídeo é peça de captação: oferece "análise 100% gratuita" por QR code. Separar o método (útil) da oferta. [PRÁTICA] YouTube 5VxP5E6H6T0, 2025-12-23.
- **Certificação de parceiros do ML:** não foi achada página oficial brasileira. Uma agência argentina relata um programa de certificação de consultorias e agências, com critérios de contas geridas, resultados, domínio de Ads, catálogo e logística, e conformidade. Uma consultoria brasileira nega haver certificação pública individual. [PRÁTICA] algoritmodigital.com.ar/consultor-certificado-de-mercado-libre-que-es/, s/d; gosmarter.com.br/consultor-oficial-mercado-livre/, s/d. Ponto aberto: verificar com o Mercado Ads.
- **Indicadores de saúde oficiais do ML:**
  - reputação (termômetro de cores) medida por reclamações, cancelamentos pelo vendedor e atrasos de despacho, em janela de 60 dias ou 365 dias para volume baixo [OFICIAL] developers.mercadolivre.com.br/pt-br/reputacao-de-vendedores, s/d **(pode estar superada)**;
  - os limites percentuais citados divergem entre blogs (reclamações de 1% a 3%, cancelamentos de 0,5% a 1,5%, atrasos de 6% a 10%) [PRÁTICA] academia.nubimetrics.com/pt/reputacao-mercado-livre, s/d; tecnoblog.net, s/d **(pode estar superada)**;
  - API **/purchase_experience** de "Experiência de compra" por anúncio (reclamações e cancelamentos, com níveis e ações), atualizada em 2026-02-03 [OFICIAL] developers.mercadolivre.com.br/pt-br/experiencia-de-compra;
  - API de **Qualidade das publicações**: /health migrando para /performance, com ações pendentes como fotos, ficha técnica e vídeo [OFICIAL] developers.mercadolivre.com.br/pt-br/qualidade-das-publicacoes, 2025-01-31 **(pode estar superada)**.
- **Shopee:** o painel de desempenho da loja agrupa violações de anúncio, cumprimento (taxa de não cumprimento), atendimento e satisfação, com metas e pontos de penalidade. Os pontos zeram por trimestre. O programa Vendedor Indicado reavalia semanalmente o prazo de envio, a resposta e o cancelamento. [PRÁTICA] upseller.com/pt/help-doc-article-1423, s/d; ecommercenapratica.com/blog/vendedor-indicado-shopee/, s/d **(pode estar superada; limites numéricos não confirmados em fonte oficial BR)**.

### 6.3 Rotina típica (síntese desta frente a partir das fontes acima)
| Cadência | O que os profissionais olham | Base |
|---|---|---|
| Diária | Ruptura e estoque dos campeões; preço contra concorrente direto (reprecificador); orçamento de Ads esgotado; pedidos atrasados | IPI e retail readiness (6.1); UpSeller/Base (2.4) |
| Semanal | ACOS, ROAS e TACOS por campanha e por SKU; posição e share em termos-chave; pontos da Shopee; IPI | gosmarter (revisão semanal), Shopee (avaliação semanal), IPI (semanal) |
| Mensal | Share de categoria contra crescimento da categoria; top vendedores e quem subiu; CM1 a CM3 por SKU; sazonalidade do próximo trimestre | Nubimetrics (2022), ML Análise de mercado, novadata |
| Trimestral | Auditoria completa (evidência → diagnóstico → risco → ação); revisão de sortimento (racionalização de SKU); teste de incrementalidade | salesduo, neato |

---

## 7. Contexto de mercado que os profissionais usam como pano de fundo (2026)

- **Mercado Livre Brasil, 2T26:**
  - GMV +39% e itens vendidos +56% no ano (sem efeito câmbio);
  - itens por comprador +19%; conversão +1,1 ponto percentual no ano;
  - o limite de frete grátis caiu em junho de 2025, e envios grátis e lentos já têm contribuição positiva em cerca de metade das faixas de preço entre R$ 19 e R$ 79;
  - em abril de 2026 vieram descontos PIX para comprador e desconto de take rate para vendedor, condicionados a preço competitivo.
  [OFICIAL] MELI 8-K, 2026-08-05.
- **Shopee, 2T26:** GMV global +28%, com o Brasil como mercado de crescimento mais rápido. A assinatura VIP no Brasil passou de 1 milhão. [OFICIAL] Sea, 2026-08-11. A comissão no Brasil passou em março de 2026 a modelo híbrido, que varia por preço, perfil do vendedor e meio de pagamento. [PRÁTICA] euqueroinvestir.com, 2026 **(confirmar na tabela oficial)**.
- **Amazon Brasil:** lançou o "Programe e Poupe" (recorrência com desconto) e a loja "Amazon Mercado" para itens do dia a dia, em outubro de 2025. [DADO] mercadoeconsumo.com.br/14/10/2025/..., 2025-10-14; canaltech.com.br, s/d. **[MARCA]**
- **Regulação de alimentos em marketplace:** a Anvisa inspecionou um CD Full do ML em Cajamar-SP em 2026-03-18 e retirou itens sem registro, com rotulagem estrangeira ou alegações de saúde não aprovadas (suplementos e probióticos). A agência chamou a fiscalização de marketplace de "nova frente" de vigilância. [DADO] mercadoeconsumo.com.br/19/03/2026/...; agenciabrasil.ebc.com.br, 2026-03.
- **Painéis de e-commerce:** NIQ Ebit Webshoppers é a série mais longa (desde 2001). Incluiu marketplaces a partir da 45ª edição, mas por anos excluiu operações cross-border como a Shopee. Na edição 51 (2025), o capítulo de giro rápido é Premium. [DADO] nielseniq (Ed. 51, PDF), 2025. Cuidado ao comparar séries com escopos diferentes.

---

## 8. O que é de revenda e o que é de marca própria

| Tema | Revenda / dropshipping / importação **[REVENDA]** | Indústria / marca própria **[MARCA]** |
|---|---|---|
| Pergunta central | "Que produto já vende e onde consigo entrar?" | "Como ganho share na minha categoria e defendo a marca?" |
| Ferramentas típicas | Avantpro, Nubimetrics (explorador), JoomPulse, RadarSeller, Jungle Scout e Helium 10 no modo descoberta | ML Análise de mercado, Brand Analytics, SmartScout, Cobalt, digital shelf (Lett, Profitero, Flywheel) |
| Métricas de entrada | Nº de resultados, medalhas na 1ª página, % no Full, internacionais, idade do anúncio contra vendas, margem sobre custo China | Share de categoria e de busca, conversion share, recompra, ruptura, content score, índice de preço |
| Unidade de análise | Anúncio e palavra-chave | Marca, subcategoria, termo de busca e portfólio de SKU |
| Ads | Ads para "subir" anúncio novo; ACOS contra margem | Separar marca e genérico, defesa de marca, incrementalidade, Brand Ads/SB, TACOS de portfólio |
| Risco típico | Concorrência por preço, cópia, produto sem registro | Canibalização, conflito de preço entre canais, regulação (Anvisa), recompra baixa |
| Fontes | 2.3, 2.4, 3.1, 3.2 | 3.3, 3.4, 4, 5, 6.1 |

Vale para os dois: escada de margem (CM1 a CM3), ACOS de equilíbrio, saúde da conta, funil impressão → clique → venda e sazonalidade.

---

## 9. Lacunas e cuidados encontrados nesta frente
1. Nenhuma ferramenta de terceiros publica fórmula de estimativa ou erro auditado. Todas as acurácias (84%, 80% a 90%, "20% mais preciso") são autodeclaradas.
2. O Mercado Livre restringiu dados de API para terceiros. Em ML, o painel oficial passou a ser a fonte mais quente para quem já vende na categoria, e as ferramentas externas perderam granularidade (relato de praticantes).
3. Limites de reputação e penalidade (ML e Shopee) circulam em blogs com números divergentes. A fonte final é o painel da conta.
4. Não foi achada página oficial de critérios de "consultoria certificada" do ML no Brasil.
5. A métrica-alvo do Product Ads (ACOS contra ROAS objetivo) muda por país. Confirmar no painel brasileiro.
6. Benchmarks de Ads (CPC, CVR, ROAS por categoria) existem para a Amazon dos EUA (Pacvue, Jungle Scout), mas não foram achados públicos para ML e Shopee no Brasil.

---

## 10. Índice de fontes (por tipo)
[OFICIAL]
- sec.gov/Archives/edgar/data/0001099590/000109959026000021/meli-20260805xex991.htm (2026-08-05)
- cdn.sea.com/investor/2Q2026/... Earnings Call Transcript (2026-08-11)
- sell.amazon.com/tools/amazon-brand-analytics (s/d)
- developers.mercadolivre.com.br: reputacao-de-vendedores, experiencia-de-compra (2026-02-03), qualidade-das-publicacoes (2025-01-31), introducao-ao-mercado-ads (s/d)
- ads.shopee.sg/learn/faq/471/1787 (s/d)

[DADO]
- academia.nubimetrics.com (2022)
- nubimetrics.com/pdf/terminos_pt.pdf
- junglescout.com: blog/amazon-sales-rank, enterprise/products/cobalt, resources/reports/amazon-benchmark-report-2026
- helium10.com: blog/what-is-amazon-tacos (2024-03-18), Market Tracker
- smartscout.com: guia de market share (2025-12-03), página de acurácia
- pacvue.com/guides-reports/2026-q1-retail-media-benchmark-report
- bebolddigital.com (2026)
- profitero.com/blog/what-is-digital-shelf-analytics
- koji.so (2026)
- ipa.co.uk e warc.com (2020)
- abs.gov.au (2022)
- priceshape.com
- novadata.io (2026)
- nielseniq Webshoppers Ed. 51 (2025)
- mercadoeconsumo.com.br (2025-10-14; 2026-03-19)
- agenciabrasil.ebc.com.br (2026-03)
- propmark.com.br
- adexchanger.com

[PRÁTICA]
- YouTube: S4jpAl3b4l0 (2025-10-20), 5VxP5E6H6T0 (2025-12-23), l8q-Rkw26vM (2026-01-17), KdwwoYN4S4s (2025-11-21), 4Ygmkz4y5Sk (2025-12-26), jzHBIQoiLg8 (2026-08-07), u_TBZZhXBrI (2026-03-05), MrUxBGCSXiE (2026-06-12), kNSL7_c8MLM (2026-01-23)
- perpetua.io (2022-04-07 e s/d)
- salesduo.com, estorefactory.com, myamazonguy.com
- sellersprite.com (2026), sellerlabs.com (2026)
- amazondigest.beehiiv.com (2024)
- algoritmodigital.com.ar (2025), gosmarter.com.br (2026)
- upseller.com, bigseller.pro, ecommercenapratica.com
- supplykick.com, adspert.net

[CASE]
- baguete.com.br/noticias/3-coracoes-reformula-presenca-digital-com-lett (2025-06-16)
- neato.com/blog/amazon-advertising-transparency... (s/d)

[OBS]
- YouTube Qz5h-uGRRI0 (2026-03-04), usado como exemplo de conteúdo fraco
