# Rodada 2 · Frente EVIDÊNCIA E CASES (Mercado Livre)

Data de coleta e acesso: 2026-10-15 · Lacunas-alvo: LACUNAS §0.5 (causalidade zero), §0.7 (nenhum case auditável), §4 itens 34, 35 e 36 · Notas de apoio lidas: `cases-grandes/notas.md` (§1, §3, §9) e `alimentos-marca-propria/notas.md` (§2.7, §5.9, §9).

**Método e limites desta rodada.**
- Foram usadas 20 buscas na web (o teto). O resto foi leitura direta por curl ou WebFetch: NBER, arXiv, RePEc, Amazon Science, a base de resumos da SUFE, Mercado&Consumo, Baguete, Diário do Comércio, o release da MELI e as páginas públicas de lojas oficiais do ML.
- Bloqueios encontrados, todos registrados e não contornados:
  - Columbia Business School e INFORMS: verificação Cloudflare.
  - pubsonline.informs.org e o blog técnico da Instacart: 403.
  - PDF de Moshary em Berkeley: 404.
  - ML: listagens `lista.mercadolivre.com.br/_Loja_*` e páginas de produto redirecionam para `account-verification`.
  - API `api.mercadolibre.com/users/<id>`: 403 (PolicyAgent).
  - `ads.mercadolivre.com.br`: redireciona para verificação de conta.
- Pesquisa neutra: nada aqui se refere à situação de uma empresa específica nem recomenda algo a alguém.
- Tipos usados: [DADO] estudo com desenho e amostra declarados; [N2] balanço ou release regulatório; [OFICIAL]; [CASE] resultado de empresa com período e alguma base; [PRÁTICA]; [OBS] observação direta desta rodada.

---

## Resumo

1. **A literatura de campo responde em parte à pergunta "Ads × orgânico" (ADS Q5/Q6), e a resposta não é a dos praticantes.**
   - Em três experimentos com grupo de controle, uma parte relevante das vendas atribuídas ao anúncio teria acontecido pelo orgânico:
     - eBay, 2014/2015: ROI de −63% em palavras genéricas e 99,5% dos cliques de marca recuperados pelo orgânico;
     - holdout de 3% numa plataforma de e-commerce, Management Science, 2025: os anúncios "roubam" do orgânico e reduzem o volume total;
     - app store, 2026: até 5% menos conversões com mais vagas pagas.
   - A exceção documentada é o produto **novo**. Na Flipkart, em moda, e na JD.com, com produtos sem histórico, o anúncio ajuda a plataforma a descobrir itens relevantes. Num ranking movido por vendas (app store), pausar anúncios derrubou de 20% a 30% dos downloads orgânicos.
   - Isso substitui a "prova por TACOS" [ads §3.5, linha 249 da nota] por um padrão com desenho experimental. Nenhum desses estudos é do ML. R2-EVC-1 a 6.
2. **O tamanho do efeito da entrega rápida é de cerca de 1,5% de vendas por dia útil a menos, não "2x" ou "5x" (LOG Q3, [log A17]).** No único quase-experimento com desenho limpo (novo CD de um varejista de vestuário dos EUA, JMR 2019), cada dia útil a menos no prazo elevou as vendas online em cerca de 1,45%, a partir de 7 dias. A Amazon publicou um A/B com +79 bps de receita ao acelerar o envio de produtos selecionados num marketplace emergente. Não há estudo publicado sobre o "selo Full" em si. R2-EVC-10, 11.
3. **Posição no ranking muda o que o comprador examina, não a decisão depois do clique (RANK Q8, parcial).** O experimento com ranking aleatório da Expedia (Marketing Science 2018) e o experimento do eBay que promoveu vendedores de melhor qualidade (NBER 2015) mostram dois pontos:
   - a posição atua sobretudo sobre a busca;
   - plataformas ganham retenção ao premiar qualidade no ranking (+0,3 p.p. na volta do comprador).

   Isso sustenta, com evidência externa, a lógica de o ML pesar reputação e experiência. Não diz quanto tempo um anúncio leva para ranquear: a RANK Q8 segue S. R2-EVC-7 a 9.
4. **O "efeito do frete grátis desde R$19" no Brasil é antes/depois, não causal (CASES A5).** O release do 3T25 atribui à redução do limite a aceleração no Brasil: itens +42% e GMV +34% a/a. O mesmo release dá ao México itens +42% e GMV +34% a/a, sem essa mudança. A atribuição causal fica rebaixada para confiança baixa; os números seguem [N2] A. Para comparação, a literatura acadêmica sobre frete grátis estima ganhos de conversão de cerca de 2% (teste aleatório). R2-EVC-13 a 15.
5. **O ML não publicou nenhum experimento sobre busca, Ads ou Full.** Os 10 posts mais recentes do MELI Tech no Medium (ago/2025 a mar/2026) tratam de infraestrutura. Nenhuma das buscas achou paper com experimento aleatório no ML. R2-EVC-16. Isso fecha a lacuna §0.5 como "procurado e não existe em público", não como "sem busca".
6. **Cases com período e base (CASES Q3, §0.7): achados 3, nenhum auditado e nenhum com recorte só do ML.**
   - 3 Corações + Lett: +11% de sell-out em cápsulas e +81% em um modelo de cafeteira em 5 meses, sem canal nem base declarados.
   - Categoria Supermercado do ML no BBB25: GMV +82% contra o mesmo período de 2024, dado da própria plataforma.
   - Orfeu: +40% de volume projetado para 2025, sem recorte por canal.

   O Effie não tem case de vendedor do ML, e o Mercado Ads não tem página pública de cases. R2-EVC-17 a 22. A lacuna §0.7 fica **parcialmente fechada**: o case 3 Corações/Lett que o protocolo cita foi localizado, mas segue [CASE] C.
7. **Como as indústrias de alimentos se organizam no ML (ALIM Q9).** Na observação direta (código das páginas públicas de loja oficial, 2026-10-15), o padrão é **uma conta de vendedor por grupo, com várias lojas oficiais, uma por marca**:
   - Nestlé: uma conta para Nestlé, Nescafé, Dolce Gusto, Nescau e Garoto. A Nespresso tem conta própria.
   - 3 Corações: uma conta para 3 Corações e Tres.
   - JDE: uma conta para Pilão e L'OR.
   - M. Dias Branco: uma conta para Vitarella e Adria.
   - Melitta, Italle e Orfeu: cada uma tem sua loja.

   Não foi possível ver quem opera cada conta (a marca ou um parceiro de *full commerce*). A API e as páginas de produto pediram verificação de conta. A única operação terceirizada documentada continua sendo a Nestlé com a Brasil CT, em 2019, mais a Infracommerce no site próprio da 3Corações/TRES em 2017 (fora do ML). R2-EVC-23 a 29.

---

## Achados

### A. Experimentos publicados (item 34; fecha ou qualifica ADS Q5/Q6, LOG Q3, RANK Q8)

#### A.1 Anúncios patrocinados × orgânico

| Estudo | Plataforma | Desenho | Tamanho do efeito | O que transfere para o ML |
|---|---|---|---|---|
| Blake, Nosko e Tadelis, NBER w20171 (mai/2014); Econometrica 83, 2015 | eBay (EUA), busca paga no Google | (i) desligou anúncios de palavra de marca; (ii) geo-experimento que suspendeu anúncios genéricos em cerca de 30% das DMAs | (i) 99,5% dos cliques perdidos voltaram pelo orgânico; (ii) ROI de **−63%** (IC 95% de −124% a −3%), contra ROI "ingênuo" acima de 4.100% em MQO; a busca paga somou só 0,66% às vendas. Compradores frequentes respondem por quase todo o gasto e não mudam a compra; novos e infrequentes respondem. | O anúncio em termo da própria marca tende a comprar venda que já viria. O ML não expõe o termo de busca no Product Ads [ads §9], então a fatia de "marca" do gasto segue não mensurável. |
| Moshary, Management Science 2025 (DOI 10.1287/mnsc.2024.04792); WP de 2021 | Plataforma de e-commerce não identificada | Holdout: **3%** dos visitantes sem nenhum anúncio patrocinado | Quem vê anúncios gasta mais nos itens patrocinados e menos nos orgânicos. No total, o volume intermediado **cai**. Para a plataforma, o anúncio ainda dá lucro, porque a receita de Ads mais que compensa a comissão perdida. A magnitude não foi lida (PDF deu 404). | Do lado da plataforma, a receita de Ads pode crescer mesmo com efeito líquido nulo ou negativo em vendas. Isso é coerente com a receita de Ads da MELI crescendo acima do GMV [cases A22], mas não prova que o mesmo aconteça no ML. |
| Abhishek, Jerath e Sharma, Information Systems Research 2025 (DOI 10.1287/isre.2022.0188) | Flipkart (Índia) | Experimento de campo que varia a fração de anúncios nas posições mais salientes | Eletrônicos: o anúncio converte **pior** que o orgânico que desloca, e os orgânicos vizinhos melhoram. Roupa e calçado: o anúncio converte **melhor**. +10 p.p. de anúncios **não altera** cliques nem conversões no nível da busca. O resumo da Columbia, lido só via busca porque o site exigiu verificação, fala em cerca de 1,2 milhão de usuários em 8 dias. | O efeito depende da categoria. Onde a plataforma sabe pouco sobre a relevância do item (moda, itens novos), o anúncio informa; onde sabe muito (eletrônicos padronizados), desloca. |
| Yang, Sahni e Nair, working paper da Stanford GSB (listagem de 2023, data provável) | JD.com (China) | Experimento em larga escala que usa a propensão a anunciar como sinal no ranking de **produtos novos** | Beneficia plataforma e consumidor ("cold start"). A magnitude não foi lida. | É o único mecanismo documentado pelo qual o anúncio pode melhorar o ranqueamento orgânico de item novo. É um teste da plataforma, não do vendedor. |
| Ju, Zhao e Aral, arXiv 2504.16151 (v2 de 10/07/2026) | App store (desenvolvedor de jogos dos EUA) | Desligamento global de anúncios (event study) mais painel | O desligamento derrubou de **20% a 30%** dos downloads orgânicos. Cada US$100 dão 32 downloads pagos e 2,2 orgânicos. O canal é o **ranking por categoria**: com ele no modelo, a relação some. | É a melhor evidência pública de que venda paga sobe o ranking quando o ranking é movido por volume. A transferência para busca de marketplace é por analogia (confiança média). |
| Rashid e Yoganarasimhan, arXiv 2607.14418 (15/07/2026) | App store Android | Experimento com mais de 5 milhões de usuários expostos a 1 a 6 vagas patrocinadas | Receita até **+43%**, conversões totais até **−5%**, engajamento diário até −2,2%. O ganho se concentra em buscas de alta conversão de anúncio e muda com a presença de anunciante de marca. | Mostra o *trade-off* da plataforma: mais vagas pagas rendem mais receita e menos conversão total. Em mercados maduros, a carga de anúncios tende a variar por termo. |
| Pauwels e outros (Amazon), Applied Marketing Analytics 2023 | Amazon.com | Inferência causal observacional, horizontes de 1 mês e 1 ano | Marcas que somaram vídeo do Sponsored Brands aos anúncios estáticos: **CTR +25%** e crescimento a/a das vendas **+10%** | Autores da Amazon (conflito de interesse) e desenho não aleatório. É sinal de formato, não de incrementalidade do Ads como um todo. |

**Leitura transversal.**
- **Consenso:** atribuição superestima, e a magnitude depende de o comprador já conhecer o produto ou a marca.
- **Divergência:** só há efeito positivo sobre o orgânico com mecanismo explícito: (a) ranking movido por volume de vendas e (b) item novo sem histórico.
- **Falta, e segue faltando:** teste de pausa ou holdout publicado por vendedor no ML, ou pelo próprio ML.
- **Instacart:** publicou a metodologia de incrementalidade do Sponsored Products (holdout contínuo). A página deu 403 e não foi lida; está citada apenas como referência de desenho.

#### A.2 Fulfillment, prazo e frete

| Estudo | Desenho | Tamanho do efeito |
|---|---|---|
| Fisher, Gallino e Xu, Journal of Marketing Research 2019 (resumo da AMA lido) | Quase-experimento: um novo CD de um varejista de vestuário dos EUA acelerou, sem anúncio, as entregas para o oeste; diferenças em diferenças | **+1,45% (≈1,5%) nas vendas online por dia útil a menos**, a partir de 7 dias úteis. No oeste: online +3,8% e lojas físicas +1,8%. O efeito cresce no curto e médio prazo; clientes novos respondem antes e experientes depois. |
| Mondal, Majumder e Chaoji (Amazon), KDD 2022, "ASPIRE" | Modelo causal (*doubly robust*) que escolhe quais produtos vão por avião, testado em A/B | **+79 bps de receita** num marketplace emergente da Amazon, comparando com a política anterior |
| Li, Tsekouras e Cheng, ICIS 2018 (LSE) | Experimento aleatório de campo num varejista online | Frete grátis incondicional: conversão **≥2,2%** maior que com limite mínimo. Receita estimada +18%. Informação de escassez ajuda mais que a de popularidade. |
| Hirche, Gijsenberg e Bijmolt, SOM Groningen 2021 | Experimento natural num varejista europeu (26,21 milhões de pedidos, 3,81 milhões de clientes) | Frete grátis acima de um valor mínimo gera mais vendas e mais pedidos que taxa fixa, e também mais devoluções. Na simulação, o ganho supera a perda na maioria dos cenários. |
| MELI, release do 3T25 (29/10/2025), [N2] | Antes e depois, sem grupo de controle | Brasil: após a redução do limite, itens +42%, GMV +34% em moeda constante e compradores únicos +29% a/a. **México, no mesmo trimestre, sem essa mudança:** itens +42% e GMV +34% a/a. A própria MELI cita ao mesmo tempo investimentos em fulfillment, experiência e sortimento. |

**Não encontrado:** um estudo empírico com diferenças em diferenças sobre a adesão ao Fulfillment by Amazon (FBA) e as vendas do vendedor. O que existe são modelos teóricos (Lai, Liu e Xiao, 2022), um *survey* de confiança no selo Prime (HICSS-56) e uma base de 1.166 SKUs que migraram para o FBA (MSOM, 2015–2017) sem estimativa causal lida. O "selo Full" segue sem estimativa causal publicada; [log A17] ("2x", "+150%", "5x") continua sem método.

#### A.3 Ranqueamento e reputação

| Estudo | Desenho | Achado |
|---|---|---|
| Ursu, Marketing Science 37(4), 2018 | Experimento da Expedia: cerca de 1/3 das buscas com ranking **aleatório** | A posição afeta **o que o consumidor examina**, mas, condicionada à busca, não afeta a compra. O efeito médio de posição é de US$1,92, menor que as estimativas sem variação experimental. |
| Dinerstein, Einav, Levin e Sundaresan, AER 2018 (NBER w20415) | Modelo estrutural validado por um redesenho da busca do eBay e por um A/B posterior | Margens de varejo da ordem de 10%. Estreitar o conjunto de escolhas (destacar o melhor preço em bem homogêneo) pode ser **pró-competitivo**. Em produto diferenciado, desenhar o ranking é mais difícil porque preço é só um atributo. |
| Nosko e Tadelis, NBER w20830 (jan/2015; versão publicada listada em 2026) | Experimento: 10% dos GUIDs com ranking que promove vendedores com maior "EPP" (qualidade não observável pelo comprador) | Compradores tratados voltam a comprar mais: diferença de **0,3 p.p.**, significativa. No observacional, passar do vendedor do quartil inferior de EPP para o superior eleva em cerca de 4 p.p. a chance de nova compra em 180 dias. A nota positiva média é de 99,3%, por isso a reputação visível discrimina pouco. |

**Para o ML.**
- Os três estudos explicam *por que* marketplaces incorporam preço (catálogo), qualidade e experiência ao ranking. Isso é coerente com as regras oficiais já registradas [rank, rep].
- Nenhum mede o tempo para ranquear nem o peso de cada fator no ML.

### B. Cases com período e base (item 35; CASES Q3)

| Case | Período e base | Fonte | Avaliação |
|---|---|---|---|
| 3 Corações + Lett (Neogrid) | Sell-out de cápsulas **+11%** e de um modelo de cafeteira **+81%**, em **5 meses**. A causa declarada é a reformulação da presença digital (página de produto, conteúdo, disponibilidade). | Mundo do Marketing, "como a 3 Corações elevou vendas de cápsulas em 11%…" (página carrega por JavaScript; números lidos só no trecho da busca; sem data lida; o protocolo cita 2025) | [CASE] C. Sem canal, sem base absoluta, sem grupo de comparação e medido pelo próprio fornecedor. Não se sabe se inclui o ML. |
| ML Supermercado no BBB25 | GMV da categoria **+82%** na estreia do BBB25 contra o mesmo período de 2024 (o título diz 84%, o que é inconsistente). Usuários impactados: ticket +14% e itens por carrinho +30%. Vendas da categoria: +77% em 2024 contra 2023. | Mercado&Consumo, 25/02/2025, com fala da diretora de marketplace do ML | [OFICIAL via terceiro] B. É número da plataforma, com período, sem base absoluta e sem marca. |
| Orfeu Cafés Especiais | Volume **+40%** projetado para 2025, num mercado de especiais que cresce cerca de 15% ao ano contra 2% do tradicional (fala do diretor de marketing). Mais de 50 itens em supermercado, e-commerce próprio, Amazon e ML. | Diário do Comércio, 11/09/2025 | [CASE] C. É projeção, sem recorte por canal. |
| M. Dias Branco (Vitarella, Piraquê, Adria) | Abertura de lojas oficiais no ML em dez/2021. Sem número de resultado. | Mercado&Consumo, 10/12/2021 | [CASE] de estrutura, sem métrica. É o único release de indústria de alimentos sobre loja oficial no ML com motivação declarada. |
| Effie Brasil | A lista de finalistas de 2026 não tem case de vendedor no ML. Os cases do ML no Effie são campanhas da própria marca ML (por exemplo, "Parada no Feed", de 2021, e "Ballboards", de 2024, só via busca). | Meio & Mensagem, finalistas de 2026 (lido); edições anteriores via busca | Não serve para CASES Q3. O Effie não publica a ficha de métricas aberta. |
| Mercado Ads | Não há página pública de cases (`ads.mercadolivre.com.br` pede verificação de conta; `/cases` dá 404). O número que circula ("full-funnel converte até 9x mais", case de eletrônicos) é declarado com base em dados internos. | Busca (Motorola News; Meio & Mensagem, conteúdo patrocinado) | [PRÁTICA/OFICIAL autodeclarado] C. Sem método. |

**Conclusão do item 35.**
- Continua não existindo case de vendedor no ML com período, base e medição de terceiro.
- O melhor disponível tem medição de fornecedor (Lett) ou da plataforma (BBB25).
- A regra das notas se mantém: todo faturamento de case é [PRÁTICA] C [cases A9].

### C. Organização das indústrias de alimentos no ML (item 36; ALIM Q9)

**Observação direta [OBS], 2026-10-15.**
- Fonte: código-fonte das páginas públicas `mercadolivre.com.br/loja/<slug>`, sem login. Os campos `seller_id` e `official_store_id` aparecem no HTML; o CEP exibido foi o de Uberlândia.

| Grupo | Lojas oficiais (official_store_id) | Conta de vendedor (seller_id) |
|---|---|---|
| Nestlé | Nestlé (430144), Nescafé (202144), Nescafé Dolce Gusto (429942), Nescau (202348), Garoto (428984) | **1034651316, a mesma nas 5** |
| Nestlé (Nespresso) | Nespresso (3241) | 2141839850 (conta separada) |
| 3 Corações | 3 Corações (1067), Tres (151044) | **1332903562, a mesma nas 2** |
| JDE Peet's | Pilão (364302), L'OR (377084) | **1392082999, a mesma nas 2** |
| M. Dias Branco | Vitarella (4131), Adria (4130) | **1332357893, a mesma nas 2** |
| Melitta | Melitta (2919) | 2026710759 |
| Italle | Café Italle (3547) | 568674447 |
| Orfeu | Orfeu Cafés Especiais (121248) | 1365272364 |
| Santa Monica | `/loja/cafe-santa-monica` respondeu HTTP 203 sem esses campos | não determinado |

**O que isso mostra.**
- Grupos multimarca usam **uma conta de vendedor com várias lojas oficiais**, uma por marca.
- A exceção é a Nespresso, que tem operação comercial própria também fora do ML.
- Como reputação, Full e faturamento são da conta [rep], as marcas de um mesmo grupo dividem a mesma reputação. Isso é uma inferência a partir da regra de que a reputação é por vendedor, não verificada por marca.

**O que não foi possível ver.**
- Quem opera cada conta: a própria indústria, um distribuidor ou uma agência de *full commerce*.
- O apelido do vendedor, o % de Full e se o ML vende as mesmas marcas em 1P. A API respondeu 403 e as listagens e páginas de produto pediram verificação de conta; não houve contorno.

**Imprensa.**
- **Nestlé:** loja oficial aberta em abr/2019 com a Brasil CT operando pedidos e logística (Mercado&Consumo, 18/04/2019, já nas notas). As buscas não acharam notícia de 2025–2026 sobre o operador atual. **A conta atual (1034651316) também abriga Garoto e Nescau**, portanto a operação foi ampliada depois de 2019. Não se sabe se segue com a Brasil CT.
- **3Corações:** a Infracommerce passou a operar o canal online próprio do grupo (plataforma, operação, logística e SAC), começando pela TRES (Baguete, 13/02/2017). Isso se refere ao site próprio, não ao ML, e pode estar superado.
- **JDE/Pilão:** a Keurig Dr Pepper fechou acordo para comprar a JDE Peet's por cerca de US$18 bilhões (Mercado&Consumo, 25/08/2025, só via busca); a conclusão não foi confirmada. A JDE comprou os ativos de café da Maratá (via busca). As buscas não acharam nada sobre a operação no ML.
- **Melitta e Italle:** nenhuma entrevista ou release sobre marketplace foi encontrado nas buscas.
- **Orfeu:** declara presença no ML e na Amazon, ao lado do e-commerce próprio e do supermercado (Diário do Comércio, 11/09/2025).
- **Agências de *full commerce*:**
  - Nenhuma fonte confirma qual agência opera lojas oficiais de alimentos no ML em 2026.
  - O setor se consolidou: a Infracommerce comprou a Synapcom (Brazil Journal, via busca). A Synapcom atende indústrias de outros setores (Samsung, Philips, Hypera, Goodyear), sem menção a alimentos.

**ID da loja não é data.** Vitarella e Adria têm IDs 4130–4131 e abriram em dez/2021, mas a loja da Nestlé de 2019 hoje tem ID 430144. Ou a loja foi recriada ou a numeração não é cronológica. Não usar o ID para datar.

---

## Tabela de afirmações novas

| id | Afirmação | Tipo | Fonte | Data da fonte | Confiança | Fecha qual lacuna |
|---|---|---|---|---|---|---|
| R2-EVC-1 | No eBay, desligar anúncios de palavra de marca manteve 99,5% dos cliques via orgânico. Anúncio genérico: ROI de −63% (IC 95% de −124% a −3%); a busca paga somou 0,66% às vendas. | DADO | nber.org/papers/w20171 e PDF w20171 | mai/2014 (Econometrica, 2015) | alta | §0.5; ADS Q5 (externo); qualifica [ads §3.5 TACOS] |
| R2-EVC-2 | Holdout de 3% sem anúncios numa plataforma de e-commerce: o anúncio desvia venda do orgânico e reduz o volume total, mas dá lucro à plataforma pela receita de Ads | DADO | Management Science, DOI 10.1287/mnsc.2024.04792 (resumo via academicnewsletter.sufe.edu.cn/info/386659) | 2025 | alta (direção); magnitude não lida | §0.5; ADS Q5/Q6 |
| R2-EVC-3 | Flipkart: o anúncio converte pior que o orgânico deslocado em eletrônicos e melhor em moda; +10 p.p. de anúncios não muda cliques nem conversões no nível da busca | DADO | ISR, DOI 10.1287/isre.2022.0188 (resumo via sufe.edu.cn/info/406211) | 2025 | alta (resumo); amostra de 1,2 milhão em 8 dias: média (só via busca) | ADS Q5/Q6 |
| R2-EVC-4 | JD.com: usar a propensão a anunciar no ranking de produtos novos beneficia plataforma e consumidor (cold start) | DADO | gsb.stanford.edu (node 622893), Yang, Sahni e Nair | c. 2023 | média | RANK Q8 (mecanismo); ADS Q6 |
| R2-EVC-5 | App store: desligar anúncios reduziu de 20% a 30% dos downloads orgânicos, via ranking por categoria; US$100 dão 32 downloads pagos e 2,2 orgânicos | DADO | arxiv.org/abs/2504.16151 | v2 de 10/07/2026 | alta (no contexto); média (transferência ao ML) | ADS Q6 (mecanismo "venda paga sobe ranking") |
| R2-EVC-6 | App store, mais de 5 milhões de usuários, 1 a 6 vagas pagas: receita até +43%, conversões totais até −5%, engajamento até −2,2%; efeito heterogêneo por termo | DADO | arxiv.org/abs/2607.14418 | 15/07/2026 | alta (no contexto) | ADS Q9 (carga de anúncios na busca) |
| R2-EVC-7 | Expedia, ranking aleatório: a posição afeta o que é examinado, não a compra condicionada à busca; efeito médio de posição de US$1,92 | DADO | ideas.repec.org (Marketing Science 37(4):530-552) | 2018 | alta | RANK Q8 (parcial) |
| R2-EVC-8 | eBay: margens de cerca de 10%; destacar a melhor oferta em bem homogêneo pode ser pró-competitivo; em produto diferenciado o ranking é mais difícil | DADO | NBER w20415 / AER 2018 (resumo via causalclaims.trfetzer.com) | 2018 | alta | RANK (lógica do catálogo/buy box) |
| R2-EVC-9 | eBay: ranking que promove vendedores de maior qualidade (10% dos GUIDs) elevou em 0,3 p.p. a volta do comprador; a nota positiva média de 99,3% discrimina pouco | DADO | nber.org/papers/w20830 e PDF | jan/2015 | alta | REP/RANK (por que a plataforma pesa experiência) |
| R2-EVC-10 | Cada dia útil a menos no prazo elevou as vendas online em cerca de 1,45% (base de 7 dias); online +3,8% e loja física +1,8% na região tratada; o efeito cresce com o tempo | DADO | ama.org (resumo de Fisher, Gallino e Xu, JMR 2019) | 2019 | alta | LOG Q3 (ordem de grandeza externa); rebaixa [log A17] |
| R2-EVC-11 | Amazon: política causal de envio aéreo gerou +79 bps de receita em A/B num marketplace emergente | DADO (autores da plataforma) | amazon.science/publications/aspire-… (KDD 2022) | 2022 | média | LOG Q3 |
| R2-EVC-12 | Amazon: marcas com vídeo do Sponsored Brands somado ao estático tiveram CTR +25% e crescimento a/a de vendas +10% | DADO (observacional, autores da Amazon) | amazon.science/publications/sponsored-brands-video-… | 2023 | média-baixa | ADS Q1/Q6 (formato) |
| R2-EVC-13 | Experimento aleatório: frete grátis incondicional eleva a conversão em ≥2,2% contra frete grátis com mínimo | DADO | researchonline.lse.ac.uk/id/eprint/102913 (ICIS 2018) | 2018 | alta (no contexto) | PRE/LOG (efeito de frete) |
| R2-EVC-14 | Experimento natural (26,21 milhões de pedidos): frete grátis acima de um mínimo gera mais vendas e pedidos que taxa fixa, e mais devoluções | DADO | rug.nl SOM 2021012-MARK | jun/2021 | alta (no contexto) | PRE/LOG |
| R2-EVC-15 | O release do 3T25 atribui ao limite de R$19 a aceleração no Brasil (itens +42%, GMV +34%, compradores únicos +29%), mas o México teve os mesmos +42% e +34% sem essa mudança: é antes/depois, não causal | N2 | release da MELI de 29/10/2025 (placera.se) | 29/10/2025 | alta (números); baixa (causalidade) | qualifica CASES A5 |
| R2-EVC-16 | O MELI Tech (Medium) não publicou experimento de busca, Ads ou Full nos 10 posts de ago/2025 a mar/2026; as buscas não acharam paper com experimento aleatório no ML | OFICIAL (ausência) | medium.com/feed/mercadolibre-tech; buscas desta rodada | 2025–2026 | média | §0.5 (procurado; inexistente em público) |
| R2-EVC-17 | 3 Corações + Lett: sell-out de cápsulas +11% e de um modelo de cafeteira +81% em 5 meses, sem canal e sem base | CASE | mundodomarketing.com.br/como-a-3-coracoes-elevou-vendas-de-capsulas-em-11-… (trecho via busca) | não lida (protocolo: 2025) | baixa (C) | ALIM Q3 e §4 item 27 (case localizado, não auditado) |
| R2-EVC-18 | ML Supermercado: GMV +82% na estreia do BBB25 contra o mesmo período de 2024; ticket +14% e itens por carrinho +30% entre impactados; categoria +77% em 2024 contra 2023 | OFICIAL via terceiro | mercadoeconsumo.com.br, 25/02/2025 | 25/02/2025 | média (título diz 84%) | CASES Q3 (dado de categoria) |
| R2-EVC-19 | Orfeu projeta volume +40% em 2025 e vende em supermercado, e-commerce próprio, Amazon e ML, sem recorte por canal | CASE | diariodocomercio.com.br, 11/09/2025 | 11/09/2025 | baixa (C) | ALIM Q9; CASES Q3 |
| R2-EVC-20 | A M. Dias Branco abriu lojas oficiais de Vitarella, Piraquê e Adria no ML em dez/2021 para captar a busca por itens do dia a dia | CASE (estrutura) | mercadoeconsumo.com.br, 10/12/2021 | 10/12/2021 | média (pode estar superada) | ALIM Q9 |
| R2-EVC-21 | O Effie Brasil 2026 não tem case de vendedor no ML; os cases do ML no Effie são campanhas da própria marca | OBS/DADO | meioemensagem.com.br, finalistas do Effie 2026 | 2026 | média | CASES Q3 (fonte descartada com motivo) |
| R2-EVC-22 | O Mercado Ads não tem página pública de cases; o número "9x" é declarado com base em dados internos | OBS | ads.mercadolivre.com.br (verificação de conta), /cases (404); Motorola News via busca | 2026-10-15 | média | ADS Q7 (benchmark segue S) |
| R2-EVC-23 | A Nestlé opera 5 lojas oficiais (Nestlé, Nescafé, Dolce Gusto, Nescau, Garoto) numa única conta de vendedor; a Nespresso tem conta própria | OBS | código de mercadolivre.com.br/loja/{nestle, nescafe, nescafe-dolce-gusto, nescau, garoto, nespresso} | 2026-10-15 | alta | ALIM Q9 |
| R2-EVC-24 | A 3 Corações opera 3 Corações e Tres numa única conta; a JDE opera Pilão e L'OR numa única conta; a M. Dias Branco, Vitarella e Adria numa única conta | OBS | código de /loja/{3-coracoes, tres, pilao, lor, vitarella, adria} | 2026-10-15 | alta | ALIM Q9 |
| R2-EVC-25 | Melitta (loja 2919), Café Italle (3547) e Orfeu Cafés Especiais (121248) têm loja oficial própria, cada uma com sua conta | OBS | código de /loja/{melitta, cafe-italle, orfeu-cafes-especiais} | 2026-10-15 | alta | ALIM Q9; confirma [alim A11] na prática |
| R2-EVC-26 | Quem opera cada conta (indústria ou parceiro) não é visível sem login: a API deu 403 e as listagens e páginas de produto pediram verificação | OBS (limite) | api.mercadolibre.com/users; lista.mercadolivre.com.br | 2026-10-15 | alta | ALIM Q9 (motivo do P) |
| R2-EVC-27 | A Infracommerce passou a operar o canal online próprio da 3Corações (TRES) em fev/2017: plataforma, logística e SAC. Refere-se ao site próprio, não ao ML. | CASE (estrutura) | baguete.com.br, 13/02/2017 | 13/02/2017 | média (pode estar superada) | ALIM Q9 (padrão de terceirização) |
| R2-EVC-28 | Nenhuma notícia de 2025–2026 sobre o operador atual da loja Nestlé no ML; o caso Brasil CT (2019) segue sem atualização | OBS (ausência) | buscas desta rodada | 2026-10-15 | média | ALIM Q9 |
| R2-EVC-29 | O `official_store_id` não serve para datar lojas (Vitarella e Adria têm 4130–4131 em dez/2021; a Nestlé, de 2019, tem 430144) | OBS | lojas acima mais Mercado&Consumo de 10/12/2021 | 2026-10-15 | média | método |

---

## O que segue aberto e por quê

1. **Incrementalidade do Ads no próprio ML (ADS Q5/Q6): segue S para o ML.**
   - Agora há evidência externa forte: R2-EVC-1 a 6. Falta um teste de pausa, holdout ou geo publicado por vendedor ou pelo ML.
   - Isso só se fecha com dado de conta (o vendedor pausa e mede) ou com publicação do ML, que não existe (R2-EVC-16).
   - Não leio o PDF de Moshary (404) nem o artigo completo da Flipkart (403/Cloudflare). As magnitudes do holdout ficam sem número.
2. **Efeito causal do Full ou do selo (LOG Q3): segue S para o ML.** A ordem de grandeza externa é de cerca de 1,5% por dia útil (R2-EVC-10), mas o selo junta prazo, frete, confiança e peso no ranking. Não há estudo com diferenças em diferenças sobre FBA nem sobre Full. Um caminho seria uma base pública de entrada no Full por SKU, que não existe; outro, a série da própria conta.
3. **Tempo para ranquear (RANK Q8): segue S.** A literatura explica o mecanismo de posição (R2-EVC-7 a 9), não o prazo.
4. **Case auditável (CASES Q3, §0.7): segue sem case de vendedor do ML com medição de terceiro.**
   - O case 3 Corações/Lett não traz canal nem base. A página carrega por JavaScript e a data não foi lida; um leitor que renderize JS pode ler o texto completo.
   - A ficha do Effie não é pública.
   - O Mercado Ads não tem página aberta de cases.
5. **Organização 1P/3P (ALIM Q9): passou de S para P.** A estrutura de contas e lojas está observada (R2-EVC-23 a 25). Faltam três respostas:
   - (a) quem opera cada conta, que exige login ou a API autenticada (fora do escopo);
   - (b) se o ML vende essas marcas em 1P, o que exige ver "Vendido por" na página de produto (bloqueada por verificação nesta rodada; tentar pelo navegador integrado sem login em outro horário);
   - (c) qual agência de *full commerce* atende indústrias de alimentos no ML, o que exige releases e LinkedIn das agências, não alcançados com a cota de 20 buscas.
6. **Melitta, Italle e Pilão/JDE na imprensa.** Nenhuma entrevista sobre marketplace foi encontrada. A aquisição da JDE pela KDP pode mudar a operação, e a conclusão não foi confirmada.
7. **Amazon Vendor no Brasil (termos públicos do 1P), citado no item 36:** não pesquisado nesta frente por falta de cota de busca.
