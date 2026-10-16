# Rodada 2 · Frente "balancos-api" (Mercado Livre)

Data de acesso de todas as fontes: 2026-10-15. Itens tratados: LACUNAS §4 itens 11 e 19, §1.2 (Q1, custo fixo abaixo de R$79), §1.8 (pacote de abril/2026, MELI+, restrição de API) e §1.1 (Ads/GMV). Sem login, sem formulário, sem aceite de termos. Sem navegador Chrome. Leituras feitas com curl, WebFetch e WebSearch (4 buscas).

Siglas usadas na tabela: [OFICIAL] = N1, página ou API do ML; [N2] = balanço ou documento na SEC; [DADO] = resposta de API ou contagem medida por nós.

---

## Resumo

1. **A API `listing_prices` deixou de ser pública. Sem token, a tarifa percentual exata por categoria não pode ser lida.** As 6 chamadas de teste (café moído/grão MLB247538 e Alimentos e Bebidas MLB1403, a R$50, R$100 e R$200) voltaram HTTP 403 com `"blocked_by":"PolicyAgent"`. O resultado se repetiu com `listing_type_id` e `logistic_type`. O simulador de custos e a landing `/landing/custos-de-venda/tarifas-de-venda` redirecionam para o login. **Item 11 fica PARCIAL**: o percentual-base da categoria café continua sem leitura oficial (exige token ou login). [R2-BA-1, R2-BA-2]
2. **Tabela 51251 relida em texto, agora com as subcategorias de café.** A redução vale entre R$150 e R$700 para Mercearia > Café, Café Moído e em Grão, Café Solúvel, **Cápsulas**, Infusões e Cremes para Café, com −5 pp no Premium e −3 pp no Clássico. Fecha [pre R6/A8], incluindo Cápsulas, que não estava explícito antes. [R2-BA-4]
3. **Custo fixo abaixo do limite: há regra oficial nova.** Segundo o developers "Custos por vender" (atualizado em 03/09/2026), o Brasil ativou a nova estrutura em 02/03. Abaixo do limite (TH), só o Flex cobra custo fixo entre os modos ME2. Coleta, Places, Drop off, Turbo e Full não cobram. ME1 e envio personalizado sempre cobram. Acima do limite, ninguém paga custo fixo. Isso **fecha** a divergência [pre §6.1] e [mix R12] ("custo fixo de R$6,25–6,75" ou "corte de R$12,50"): esses números de blog descrevem a regra anterior a 02/03/2026. [R2-BA-5]
4. **MELI+ e frete abaixo de R$79 confirmados em N2, com a data.** Na Carta 3T25 (29/10/2025), MELI+ dá entrega **rápida** a partir de R$19, anunciada em outubro. Quem não é assinante recebe entrega **lenta** na faixa de R$19 a R$79. Na Carta 4T25 (24/02/2026), o Essencial custa R$9,90 por mês. Na Carta 1T26 (07/05/2026), os assinantes cresceram 49% desde o 3T25. Na Carta 2T26, o crescimento é de +72% a/a. **Fecha [cases A31]** (antes SEM FONTE OFICIAL). [R2-BA-8 a R2-BA-11]
5. **Pacote de preço competitivo de abril/2026: o N2 confirma o formato, mas não os detalhes do InfoMoney.** Na call do 1T26, o CEO diz que o corte de take rate é por categoria e faixa de preço, "not a platform-wide take rate cut", e condicionado a preço competitivo. O CFO acrescenta que a redução da tarifa de **envio** para vendedores entrou no fim do 1T26. A Carta 2T26 diz que o pacote reduziu receita e margem bruta, melhorou o índice de competitividade de preço e acelerou vendedores ativos (+29% a/a). Nenhum documento N2 cita "armazenagem grátis no Full" nem "−1 p.p.". **[cases A2] segue PARCIAL**: a parte oficial é o desconto no Pix, o desconto de take rate e o corte de tarifa de envio. [R2-BA-12 a R2-BA-14]
6. **Ads/GMV não é divulgado.** Na call do 4T25, a empresa diz só que a receita de Ads como % do GMV "is still small compared to its potential". O número de ~2,6% [ads §1.1] segue sem fonte N2. Os crescimentos de Ads em moeda constante foram +63% (3T25), +63% (1T26) e +62% (2T26), e a empresa passou de 10% de share da publicidade digital na América Latina. [R2-BA-15, R2-BA-16]
7. **Full no Brasil não é divulgado separadamente.** Os balanços dão: 55% dos envios regionais pela rede de fulfillment (1T26, mais de 50 instalações); "mais da metade dos envios" (10-Q 2T26); quase 80% no México (4T25). O número próprio do Brasil não aparece em nenhuma carta nem call de 3T25 a 2T26. **Lacuna fica S, com motivo: não divulgado.** [R2-BA-17]
8. **1P abaixo de 10% do GMV (10-Q 2T26).** O 1P fez "almost $5bn" de GMV em 12 meses (1T26) e mais de US$4 bi em 2025, com +80%. Ele preenche lacunas de seleção ou preço que os vendedores 3P não preenchem (call 3T25). [R2-BA-18, R2-BA-19]
9. **Restrições de API para ferramentas externas: agora há fonte oficial** (antes só relato N8, [cases A56/§9.9]). Os pontos são:
   - endpoints de tendências, mais vendidos, visitas e busca exigem token e permissão funcional "Métricas do negócio";
   - o app pode ser bloqueado por "INTEGRATORS_DATA_INFRACTION" quando faz só leitura, sem consumir APIs que gerem valor (página de 15/04/2026);
   - os Termos proíbem scraping e uso do conteúdo para concorrer com o ML, e exigem atualizar as listagens a cada 6 h;
   - os recursos públicos mostram o estoque só em faixas;
   - o Developer Partner Program exige GMV mensal de US$2,5 milhões no Brasil (página de 14/10/2026).

   [R2-BA-20 a R2-BA-27]
10. **Correção interna:** o "+1,1 p.p. de conversão" do 2T26, que [cases] registrou como empresa toda, é do **Brasil** pela call (o CEO diz "Conversion in Brazil is up 1.1 percentage points"). [R2-BA-28]

---

## Achados

### (a) Tarifa percentual por categoria via API pública

**IDs das categorias de café** (API `domain_discovery` e `/categories`, ambas públicas, HTTP 200):

| Categoria | id | Caminho | Itens na categoria | `listing_allowed` | `minimum_price` | `max_title_length` |
|---|---|---|---|---|---|---|
| Café Moído e em Grão | MLB247538 | Alimentos e Bebidas > Mercearia > Infusões > Café > Café Moído e em Grão | 28.692 | true | 8 | 60 |
| Cápsulas | MLB247540 | Alimentos e Bebidas > Mercearia > Infusões > Cápsulas | 17.231 | true | 8 | 60 |
| Café Solúvel | MLB247537 | Alimentos e Bebidas > Mercearia > Infusões > Café > Café Solúvel | 8.074 | true | 8 | 60 |
| Café (nó pai) | MLB247520 | … > Infusões > Café | 39.782 | **false** (não aceita anúncio direto) | 8 | 60 |

As consultas "cafe em graos" e "cafe moido" levam a MLB247538 (domínio `MLB-GROUND_AND_WHOLE_BEANS_COFFEE`). "Cafe em capsulas", "capsula nespresso" e "cafe dolce gusto" levam a MLB247540 (`MLB-INFUSION_CAPSULES`). "Cafe soluvel" leva a MLB247537. Note que Cápsulas fica fora do nó "Café", direto sob Infusões. As três folhas têm `item_conditions: ["new"]`, `immediate_payment: required` e `buying_modes` com `buy_it_now` e `auction`.

**Teste de `listing_prices`** (curl sem token, 2026-10-15):

```
GET https://api.mercadolibre.com/sites/MLB/listing_prices?price={50|100|200}&category_id={MLB247538|MLB1403}
→ HTTP 403
{"status":403,"blocked_by":"PolicyAgent","code":"PA_UNAUTHORIZED_RESULT_FROM_POLICIES","message":"At least one policy returned UNAUTHORIZED."}
```

A mesma resposta veio com `listing_type_id=gold_special|gold_pro`, `currency_id=BRL`, `logistic_type=fulfillment&shipping_mode=me2` e sem categoria (`?price=100`).

**Mapa do que segue público e do que fechou** (curl sem token, mesma data):

| Endpoint | HTTP |
|---|---|
| `/sites/MLB/domain_discovery/search` | 200 |
| `/categories/{id}` e `/categories/{id}/attributes` | 200 |
| `/sites/MLB/listing_prices`, `/sites/MLB/listing_types`, `/sites/MLB/listing_exposures` | 403 PolicyAgent |
| `/sites/MLB`, `/sites/MLB/categories`, `/currencies/BRL`, `/sites/MLB/shipping_methods`, `/categories/{id}/sale_terms`, `/categories/{id}/shipping_preferences` | 403 PolicyAgent |
| `/trends/MLB/{cat}` | 403 |
| `/sites/MLB/search?q=` | 403 `forbidden` |
| `/products/{id}`, `/items?ids=`, `/highlights/MLB/category/{cat}` | 401 "authorization value not present" |

Isso muda dois pontos anteriores:
- [rank A14] dizia que `/categories` "seguiu pública". Segue, mas `/sites/MLB/categories` e `/trends` fecharam.
- A ficha `/trends` de 27/05/2025 (§0 item 8) não pode mais ser relida sem token.

**O que a documentação oficial diz do recurso** (developers "Custos por vender", `developers.mercadolivre.com.br/pt_br/comissao-por-vender`, atualizado em 03/09/2026):
- Todos os exemplos usam `Authorization: Bearer $ACCESS_TOKEN`.
- O `percentage_fee` no MLB "pode ter variações". Ele depende da categoria, do tipo de anúncio e de "outros parâmetros objetivos definidos pelo Mercado Livre".
- O mesmo produto "pode ter comissões diferentes em momentos distintos" na faixa com redução.
- Os campos são `sale_fee_amount`, `sale_fee_details.percentage_fee`, `fixed_fee`, `financing_add_on_fee` e `gross_amount`. Há uma consulta específica para Supermercado com `tags=supermarket_eligible`, também com token.
- A página "Desenvolvimento seguro" (30/12/2025) manda enviar o token em todas as chamadas, públicas ou privadas. A página "Permissões funcionais" (21/11/2025) define o 403 PolicyAgent como falta da permissão funcional do app.

**Nova lógica de custo fixo** (mesma página). Datas de ativação: Brasil 02/03, Argentina 12/03, Colômbia 23/03, Chile 06/04 e México 08/04. O ano não está escrito; pela data da página e pelos blogs de 2026, é 2026. Para Brasil, Colômbia, Chile e México:
- **Preço < TH com ME2:** só o Flex (`self_service`) cobra custo fixo. "Os demais modelos não geram cobrança" (Drop off, Coleta, Places, Turbo, Full).
- **ME1, envio personalizado ou não especificado:** sempre cobram custo fixo quando o preço está abaixo do TH.
- **Preço ≥ TH:** não há custo fixo.
- **Tarifa de venda:** sempre uma porcentagem conforme a categoria.

TH é o limite de envio grátis obrigatório do site. A página não dá o valor e remete às FAQs de pricing, que não foram lidas. O custo de **envio** é outra linha e continua existindo: o `fixed_fee` é só o componente "custo fixo".

Um blog de ERP (tecnospeed, via busca) descreve a mesma mudança: a tarifa fixa abaixo de R$79 virou custo operacional variável a partir de mar/2026. Isso é coerente, mas é N5.

O 10-Q 2T26 continua definindo "flat fees" como cobrança fixa quando a venda fica abaixo de certo valor. É a definição contábil genérica e não contradiz a regra por modo logístico.

**O que dá para afirmar nas 3 faixas de preço sem a API** (fontes N1 em texto):

| Preço | Tarifa de venda (Clássico / Premium) | Redução 51251 (café) | Custo fixo (ME2 não Flex) | Parcelas sem juros no Premium (outros meios / Cartão MP) |
|---|---|---|---|---|
| R$50 | 10–14% / 15–19% (faixa geral; % da categoria não lido) | não se aplica (< R$150) | zero (regra de 02/03); Flex e ME1 pagam | 2x / 4x |
| R$100 | idem | não se aplica | zero; Flex e ME1 pagam se < TH | 4x / 6x |
| R$200 | idem | −3 pp Clássico / −5 pp Premium | zero (provavelmente ≥ TH) | 6x / 8x |

Fontes:
- Tarifa: ajuda/870, lida em 2026-10-15. Diz que a tarifa varia "dependendo se o anúncio é Clássico ou Premium, do valor e da categoria". Supermercado "paga outras tarifas" (link para a ajuda/16449). Kit mantém a tarifa.
- Parcelas: ajuda/22737. Também diz que o MELI+ dá até 3 parcelas extras sem juros em produtos abaixo de R$900.

A ajuda/16449 (Full Super), relida em texto, dá:
- preço mínimo de R$8 e reputação verde;
- armazenagem diária só para itens G e XG;
- frete grátis na loja a partir de R$199;
- a frase "Fora da loja, o frete é grátis a partir de R$ 79", que **conflita** com o R$19 da ajuda/40538. Pode ser texto antigo ou uma regra específica de Supermercado; fica registrado como divergência oficial interna.

### (b) Balanços (SEC EDGAR, CIK 0001099590) e calls

Documentos lidos, em texto, baixados da SEC com User-Agent declarado:

| Documento | Data | URL |
|---|---|---|
| 8-K Ex-99.1, Carta 3T25 | 29/10/2025 | sec.gov/Archives/edgar/data/1099590/000109959025000048/meli-20251029xex991.htm |
| 8-K Ex-99.1, Carta 4T25 | 24/02/2026 | …/000109959026000003/meli-20260224xex991.htm |
| 8-K Ex-99.1, Carta 1T26 | 07/05/2026 | …/000109959026000014/meli-20260507xex991.htm |
| 8-K Ex-99.1, Carta 2T26 | 05/08/2026 | …/000109959026000021/meli-20260805xex991.htm |
| 10-Q 2T26 | 06/08/2026 | …/000109959026000023/meli-20260630.htm |
| Transcrições das calls 3T25, 4T25, 1T26, 2T26 | 30/10/2025; 24/02/2026; 07/05/2026; 05/08/2026 | roic.ai/quote/MELI/transcripts/{ano}-year/{n}-quarter (N2 via terceiro; transcrição não oficial) |

O 3T26 ainda não saiu: o último 8-K de resultados é de 05/08/2026, e os 8-K de 10/09 e 14/09/2026 são dos itens 1.01, 7.01 e 8.01, não de resultados.

**MELI+ e frete abaixo de R$79**
- Carta 3T25: "In October, we announced that MELI+ subscribers in Brazil will be eligible for fast shipping … from R$19". Na faixa de R$19 a R$79, quem não é MELI+ recebe frete lento. A carta chama isso de reintrodução de um benefício diferenciado, depois da extensão do frete grátis a todos em junho.
- Carta 4T25: o churn caiu e a conversão subiu quando o Essencial (R$9,90 por mês) custa igual ou menos que o frete de uma compra.
- Carta 1T26: frete grátis e rápido abaixo de R$79 para membros desde outubro, com +49% de assinantes desde o 3T25. Algumas faixas de ASP abaixo de R$79 já estão no ponto de equilíbrio.
- Carta 2T26: assinantes +72% a/a. Os envios grátis e lentos têm contribuição variável positiva em metade das faixas de ASP entre R$19 e R$79.

**Pacote de preço competitivo (abril/2026)**
- Carta 2T26: "in April we introduced PIX discounts for buyers and discounts on take rates for sellers in certain categories and ASP ranges". O pacote é condicionado a preço competitivo e trouxe melhora "meaningful" no índice de competitividade de preço. Vendedores ativos cresceram 29% a/a. A compressão de margem bruta trimestral vem primeiro dessas iniciativas.
- Call 1T26 (CEO): o corte é dirigido onde há maior elasticidade de demanda e de oferta. Todos os descontos dependem de manter preço competitivo. Os cortes de take rate começaram em 2024.
- Call 1T26 (CFO): a redução da tarifa de envio para vendedores entrou no fim do 1T26 e passa a pesar no 2T26.
- Call 2T26: o corte foi em "certain verticals" e repete o que se fez em 2024 e 2025. Parte do aumento de custo de energia na logística foi repassada aos usuários e parte foi absorvida. Esse repasse é coerente com o reajuste de envio de 24/08/2026 [pre A7], mas a call não dá número.
- Carta 4T25: em 2025 houve "more flexible take rate structures for sellers".
- Nenhum dos 4 documentos nem das 4 calls cita armazenagem grátis no Full ou "1 p.p.".

**Ads**
- Crescimento em moeda constante: +63% a/a no 3T25 (+56% em US$); +63% no 1T26 (+73% em US$); +62% no 2T26.
- Carta 2T26: o ML passou de 10% de share da publicidade digital na América Latina.
- Carta 4T25: Search Ads é a principal fonte de receita de Ads.
- Call 4T25: há orquestrador de orçamento entre campanhas, "budget boost" sazonal e agentes de IA para a cauda média e longa. A penetração de Ads como % do GMV é "still small".
- O 10-Q descreve a cobrança: Product Ads e Brand Ads por clique; display e vídeo por impressão.
- Nenhum documento dá Ads/GMV numérico.

**Full**
- Carta 1T26: mais de 50 instalações, 55% dos envios, volume +39% a/a.
- 10-Q 2T26: os centros de fulfillment respondem por "more than half of shipments". A receita de armazenagem ("storage fees") é cobrada do vendedor.
- Carta 4T25: México perto de 80%. O dado do Brasil não é publicado.
- Custo unitário de envio no Brasil: −8% (3T25, call), −11% (4T25) e −17% (1T26, já em [cases A32]).
- O centro de fulfillment na China cresceu 170% contra o trimestre anterior (2T26).

**1P**
- 10-Q 2T26: "less than 10% of GMV".
- Carta 4T25: GMV de mais de US$4 bi em 2025, com +80%.
- Carta 1T26: quase US$5 bi em 12 meses, +69% a/a no 1T26. A contribuição direta já era positiva em 2024.
- Call 3T25: o 1P preenche lacunas de seleção ou preço que o 3P não preenche. A Casas Bahia entrou como vendedora em categoria onde o ML tem pouco share.

**Brasil, outros números do 2T26:** GMV +39% (moeda constante), itens +56%, itens por comprador +19% e usuários ecossistêmicos perto de +50% a/a (Carta 2T26). Conversão no Brasil +1,1 p.p. a/a (call 2T26).

### (c) Restrições de API para ferramentas externas

Fontes, todas em developers.mercadolivre.com.br/pt_br/…, lidas em texto:

1. **Permissões funcionais** (`/permissoes-funcionais`, 21/11/2025). A permissão "Métricas do negócio" dá acesso a trends, highlights (mais vendidos) e visits. "Publicidade" dá acesso a Product Ads e Brand Ads. Sem a permissão, a API devolve 403 `blocked_by: PolicyAgent`. É o mesmo erro que obtivemos sem token.
2. **Bloqueio de aplicações** (`/bloqueio-de-aplicacoes`, 15/04/2026). Os motivos são NOT_COMPLY_KYC, NOT_COMPLY_T&C_RULES, EXCESSIVE_API_CALL e **INTEGRATORS_DATA_INFRACTION**, aplicado "quando usar apenas dados de leitura, sem consumo de apis que gerem valor". Um app bloqueado deixa de operar todas as APIs do ML e do Mercado Pago, e os vendedores que o usam passam a operar pelas ferramentas do ML.
3. **Termos e condições do Programa de Desenvolvedores MLB** (`/termos-e-condicoes`, sem data visível):
   - a licença pode ser revogada "sem justificativa e a qualquer momento";
   - o ML pode limitar chamadas e cobrar pelo excedente;
   - é proibido usar robôs, spiders ou scraping;
   - é proibido usar a API ou o conteúdo para desenvolver serviços que concorram com os do ML;
   - é proibido divulgar a terceiros que não são usuários do ML;
   - é proibido revender a API;
   - o conteúdo deve ser atualizado a cada 24 h, e as **listagens a cada 6 h**;
   - o ML pode desenvolver produtos que concorram com os apps.
4. **Itens e buscas** (`/itens-e-buscas`, 31/08/2026). Nos recursos públicos, `available_quantity` vem em faixas: 1–50 aparece como 1; 51–100 como 50; e assim até 50.001–99.999, que aparece como 50.000. Todos os exemplos de busca por vendedor usam token.
5. **Developer Partner Program** (`/developer-partner-program`, 14/10/2026). Para se candidatar é preciso:
   - GMVe mensal mínimo dos usuários ativos da ferramenta de US$2,5 milhões no Brasil;
   - assessment de segurança com nota de 65% ou mais;
   - análise trimestral das candidaturas.
6. **Erro 403** (`/erro-403`, 02/04/2025). As causas são token de outro usuário, IP não permitido, scopes desabilitados, app bloqueado ou validação de dados incompleta.
7. A página de novidades (`/devcenter/news/`) **exige login**. O changelog não foi lido.

**Leitura neutra.** Ferramentas externas de inteligência de mercado (ranking, vendas estimadas, tendências) dependem hoje de endpoints que exigem token de um vendedor que autorizou o app. Também dependem de não serem enquadradas como uso só de leitura. O estoque público vem arredondado em faixas. Isso explica, sem confirmar, os relatos de "perda de dados após mudança na API" [cases §9.9]: a data exata de cada fechamento não está em página pública lida.

---

## Tabela de afirmações novas

| id | Afirmação | Tipo | Fonte | Data da fonte | Confiança | Fecha qual lacuna |
|---|---|---|---|---|---|---|
| R2-BA-1 | `GET /sites/MLB/listing_prices` sem token retorna 403 PolicyAgent para café (MLB247538) e Alimentos (MLB1403) a R$50, R$100 e R$200, com ou sem listing_type e logistic_type | [DADO] | curl api.mercadolibre.com (resposta registrada acima) | 2026-10-15 | alta | Item 11: muda o método (API exige token) |
| R2-BA-2 | O simulador de custos e a landing de tarifas por categoria redirecionam para o login | [DADO] | mercadolivre.com.br/simulador-de-custos; /landing/custos-de-venda/tarifas-de-venda | 2026-10-15 | alta | Item 11: "exige login" registrado |
| R2-BA-3 | IDs: Café Moído e em Grão MLB247538; Cápsulas MLB247540 (fora do nó Café); Café Solúvel MLB247537; nó Café MLB247520 não aceita anúncio; preço mínimo de R$8 e título de até 60 caracteres nas três folhas | [OFICIAL] API | api.mercadolibre.com/categories/{id}; /sites/MLB/domain_discovery/search | 2026-10-15 | alta | Base para o item 11 e para ALIM |
| R2-BA-4 | Redução de −5 pp no Premium e −3 pp no Clássico entre R$150 e R$700 também em Cápsulas, Café Solúvel, Infusões e Cremes para Café, além de Café Moído e em Grão | [OFICIAL] | mercadolivre.com.br/ajuda/51251 (texto embutido lido por curl) | sem data | alta (pode estar superada) | [pre R6/A8] confirmado e ampliado |
| R2-BA-5 | Desde 02/03/2026 no Brasil, abaixo do limite (TH), só o Flex cobra custo fixo entre os modos ME2; Coleta, Places, Drop off, Turbo e Full não cobram; ME1 e personalizado cobram; acima do TH não há custo fixo | [OFICIAL] | developers.mercadolivre.com.br/pt_br/comissao-por-vender | 03/09/2026 | alta | [pre §6.1], [mix R12] e §1.2 "custo fixo abaixo de R$79" |
| R2-BA-6 | O `percentage_fee` do MLB varia por "outros parâmetros objetivos" além de categoria e tipo; o mesmo produto pode ter comissão diferente em momentos distintos | [OFICIAL] | idem | 03/09/2026 | alta | §1.2 Q1 (explica a ausência de tabela fixa) |
| R2-BA-7 | Parcelas sem juros do Premium por preço: R$30–59,99 dá 2x (4x com Cartão MP); R$60–99,99 dá 3x (5x); R$100–149,99 dá 4x (6x); R$180–299,99 dá 6x (8x); MELI+ dá até 3 parcelas extras abaixo de R$900 | [OFICIAL] | mercadolivre.com.br/ajuda/22737 | sem data | alta (pode estar superada) | §1.2 (custo do Premium por faixa) |
| R2-BA-8 | Em out/2025, MELI+ passou a ter entrega rápida a partir de R$19 no Brasil; quem não é MELI+ recebe entrega lenta entre R$19 e R$79 | [N2] | Carta 3T25, 8-K Ex-99.1 | 29/10/2025 | alta | [cases A31] fechado |
| R2-BA-9 | MELI+ Essencial custa R$9,90 por mês; a extensão a partir de R$19 reduziu o churn e aumentou a conversão | [N2] | Carta 4T25 | 24/02/2026 | alta | [cases A31] |
| R2-BA-10 | Assinantes MELI+ +49% desde o 3T25 (1T26) e +72% a/a (2T26) | [N2] | Cartas 1T26 e 2T26 | 07/05 e 05/08/2026 | alta | [cases A31] |
| R2-BA-11 | Envio grátis e lento com contribuição variável positiva em metade das faixas de ASP de R$19 a R$79 (2T26); algumas faixas no ponto de equilíbrio (1T26) | [N2] | Cartas 1T26 e 2T26 | 2026 | alta | Contexto de §1.2 e §1.3 |
| R2-BA-12 | O corte de take rate de 2026 é por categoria e faixa de preço, não da plataforma toda, e condicionado a preço competitivo; os cortes começaram em 2024 | [N2 via transcrição] | call 1T26 (CEO), roic.ai | 07/05/2026 | média-alta (transcrição não oficial) | [cases A2] parcial |
| R2-BA-13 | Houve redução da tarifa de envio para vendedores no fim do 1T26 | [N2 via transcrição] | call 1T26 (CFO) | 07/05/2026 | média-alta | [cases A2] parcial; [pre A7] contexto |
| R2-BA-14 | O pacote de abril reduziu receita e margem bruta, melhorou o índice de competitividade de preço e acelerou vendedores ativos (+29% a/a); nenhum N2 cita armazenagem grátis no Full nem "−1 p.p." | [N2] | Carta 2T26; calls 1T26 e 2T26 | 05/08/2026 | alta | [cases A2]: parte InfoMoney segue sem N2 |
| R2-BA-15 | Ads/GMV não é divulgado; a empresa diz só que é "still small" | [N2 via transcrição] | call 4T25 | 24/02/2026 | alta | §1.1 "Ads/GMV ~2,6%": segue sem N2 |
| R2-BA-16 | Receita de Ads +63% (3T25), +63% (1T26) e +62% (2T26) em moeda constante; mais de 10% de share da publicidade digital na América Latina; Search Ads é a principal fonte | [N2] | Cartas 3T25, 4T25, 1T26 e 2T26 | 2025–2026 | alta | §1.1 contexto |
| R2-BA-17 | Penetração do Full no Brasil não divulgada; regional de 55% (1T26), "mais da metade" (10-Q 2T26), México perto de 80% (4T25) | [N2] | Cartas 4T25 e 1T26; 10-Q 2T26 | 2026 | alta | §1.3 "penetração do Full no Brasil": S por não divulgação |
| R2-BA-18 | 1P é menos de 10% do GMV | [N2] | 10-Q 2T26 | 06/08/2026 | alta | §1.8 e ALIM Q9 contexto |
| R2-BA-19 | O 1P preenche lacunas de seleção ou preço que o 3P não preenche; GMV de mais de US$4 bi em 2025 (+80%) | [N2] | call 3T25; Carta 4T25 | 2025–2026 | alta | §1.8 |
| R2-BA-20 | Trends, highlights (mais vendidos) e visits exigem a permissão funcional "Métricas do negócio"; sem ela, 403 PolicyAgent | [OFICIAL] | developers …/permissoes-funcionais | 21/11/2025 | alta | [cases A56/§9.9] restrição de API |
| R2-BA-21 | Um app pode ser bloqueado por INTEGRATORS_DATA_INFRACTION quando usa só dados de leitura; o bloqueio para todas as APIs do ML e do MP e afeta os vendedores do app | [OFICIAL] | developers …/bloqueio-de-aplicacoes | 15/04/2026 | alta | [cases §9.9] |
| R2-BA-22 | Os termos proíbem scraping, uso para concorrer com o ML, revenda da API e divulgação a quem não é usuário; a licença é revogável sem justificativa; o ML pode cobrar pelo excedente de chamadas | [OFICIAL] | developers …/termos-e-condicoes | sem data visível | alta | [cases §9.9] |
| R2-BA-23 | O conteúdo do ML em apps deve ser atualizado a cada 24 h, e as listagens a cada 6 h | [OFICIAL] | idem | sem data visível | alta | [cases §9.9] |
| R2-BA-24 | Nos recursos públicos, `available_quantity` vem em faixas (por exemplo, 1–50 aparece como 1; 51–100 como 50) | [OFICIAL] | developers …/itens-e-buscas | 31/08/2026 | alta | Limita estimativas N5 de vendas e estoque (§1.8 Q1) |
| R2-BA-25 | Developer Partner Program: GMVe mensal mínimo de US$2,5 mi no Brasil, assessment de segurança ≥ 65% e análise trimestral | [OFICIAL] | developers …/developer-partner-program | 14/10/2026 | alta | [cases §9.9] (ecossistema de ferramentas) |
| R2-BA-26 | `/sites/MLB/search`, `/trends`, `/sites/MLB/categories`, `/products`, `/items` e `/highlights` não respondem sem token (401/403); `/categories/{id}` e `domain_discovery` seguem abertos | [DADO] | curl api.mercadolibre.com | 2026-10-15 | alta | [rank A14] atualizado; §0 item 8 (/trends) |
| R2-BA-27 | A página de novidades do DevCenter (changelog) exige login | [DADO] | developers.mercadolivre.com.br/devcenter/news/ | 2026-10-15 | alta | Registro de "exige login" |
| R2-BA-28 | O +1,1 p.p. de conversão no 2T26 é do Brasil, segundo a call | [N2 via transcrição] | call 2T26 | 05/08/2026 | média-alta | Corrige [cases §3.3] ("empresa toda") |
| R2-BA-29 | A ajuda/16449 (Full Super) diz "Fora da loja, o frete é grátis a partir de R$ 79", contra os R$19 da ajuda/40538 | [OFICIAL] | mercadolivre.com.br/ajuda/16449 | sem data | média (divergência interna) | Nova divergência para ALIM/LOG |
| R2-BA-30 | Custo unitário de envio no Brasil −8% no 3T25 | [N2 via transcrição] | call 3T25 | 30/10/2025 | média-alta | Complementa [cases A32] |

---

## O que segue aberto e por quê

1. **Percentual-base de tarifa da categoria café** (Clássico e Premium, sem a redução da 51251). Ele exige token OAuth (`listing_prices`) ou login (simulador e landing de tarifas). Há duas saídas que respeitam as regras:
   - o usuário roda a chamada com o token de uma conta própria, se quiser;
   - observar um anúncio próprio já publicado.

   Sem isso, a resposta é "entre 10% e 14% / entre 15% e 19%, conforme a categoria" (ajuda/870).
2. **Valor numérico do TH** (limite de envio grátis obrigatório) usado na regra de custo fixo de 02/03/2026. O developers remete às "FAQs de pricing", que não foram localizadas em página pública. Somam-se a divergência R$19 (40538) × R$79 (16449) e o fato de o MELI+ separar entrega rápida e lenta na faixa de R$19 a R$79. É preciso reconciliar qual limite é o TH do Brasil.
3. **Tarifa da seção Supermercado** ("pagam outras tarifas", ajuda/870 → 16449). A página 16449 não dá o percentual, e a consulta via API (`tags=supermarket_eligible`) exige token.
4. **Pacote de abril/2026 no detalhe** (−1 p.p., armazenagem grátis no Full, campanhas bancadas, % do Pix e lista de categorias). Nenhum N2 traz isso, e o comunicado oficial ao vendedor não foi localizado em página pública. A única fonte segue sendo o InfoMoney de 09/04/2026.
5. **Ads/GMV numérico e Full no Brasil.** A empresa não divulga, e as 4 calls não dão número. O que resta é estimativa de sell-side, que não foi buscada porque fica atrás de paywall.
6. **Data de cada fechamento da API pública** (search, trends, listing_prices). O changelog do DevCenter exige login, e as páginas públicas dão só a data da última atualização. Não há comunicado público lido com a data em que a busca e `listing_prices` passaram a exigir token. Uma fonte de terceiros (guia de conector MCP, via busca) fala em 2025, sem confirmação.
7. **Resultados do 3T26.** Ainda não publicados em 2026-10-15; o histórico sugere fim de outubro. Uma relida trará dados mais novos sobre o pacote de preço, o MELI+ e o Full.
8. **Transcrições das calls** são de terceiro (roic.ai), sem revisão da empresa. As frases citadas devem ser conferidas no webcast oficial (investor.mercadolibre.com) se forem usadas como base de regra.
