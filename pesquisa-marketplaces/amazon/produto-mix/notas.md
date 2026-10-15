# Frente produto-mix: seleção de produto e mix na Amazon (Brasil)

Data da análise: 2026-10-14. Escopo: Amazon Brasil, com referência à Amazon dos EUA quando a mecânica é a mesma.
Pesquisa neutra: descreve como os melhores operam. Não traz recomendação para nenhuma empresa.
Corte de 6 meses: regra de plataforma anterior a **2026-04-14**, ou sem data, leva "(pode estar superada)".
Rótulos: **[REVENDA]** revenda, dropshipping, importação · **[MARCA]** indústria, marca própria · **[AMBOS]**.

## Mapa de fontes (ids)

**Transcrições da frente (lidas na íntegra; nível e sinais fracos):** m4WQtEMVfjE (Arthur Mundim, 2026-06-07, N6 tela); vZjq7xV4DB0 (Jess Empreendedora, 2026-07-23, N7: CTA, afiliado, número sem base); 1fXOj1mcRuU (Ariadne Sousa, 2026-08-20, N7: CTA, promessa, case sem base e do ML); xr-i6O8kxI8 (Jess, 2026-05-06, N7: CTA, afiliado); dJLRqoodacM (Ronny, 2026-07-17, N6 tela); TkQHhJ8DyRc (Radar Scout, 2026-07-10, dado N5 em tela, afirmações N7: teste grátis, conflito, número sem base, índice proprietário); CpeAKSyctRg (Seller Pro/B. Capellete, 2026-10-02, N6/N7); O_kXw3vvD8s (Venda com a Amazon Brasil, 2026-10-13, webinar oficial de variações); kDF4gtMCAdo (podcast L. Vedovoto, 2026-06-09, N7: oferta de escritório); yeN1TYy2LoE (Ariadne, 2026-10-14, N7: CTA de imersão); pAOzjHI4UF0 (Ariadne, 2026-06-17, N6: Explorador em tela).

**Outras transcrições da pasta:** nDtHI8fUEAA (oficial, listagem, 2026-08-20); 7ILvtU6GcPo (oficial, "Cresça sua marca", 2026-09-11); VvcswcsjuUw (oficial, Head de FBA, 2026-09-24); VH7Q5FddoRY (Smollan, agência, 2026-08-19); SqoNj2DDRSU (racionalização pelo financeiro, 2026-06-02); tpS__DSMMqo (operação Amazon EUA, 2026-07-23, números autodeclarados); rN4j4kZvkDg (importação, 2026-10-06); 78sSkRh2crI (consumível e recompra, 2026-08-18); 4Vvrft5eTDo (teste com 3 produtos, 2026-09-18); cZysnqICrkY (preço por canal, 2026-05-14). Webinars do canal da Amazon contam como [OFICIAL].

**Camada oficial (WebFetch, lidas em 2026-10-14)**
- O1 venda.amazon.com.br/precos (comissões "atualizadas em 20/01/2025"; FBA "atualizadas em 01/08/2025").
- O2 venda.amazon.com.br/cresca/fba (página de 2026; tarifas de 01/08/2025).
- O3 venda.amazon.com.br/brand-registry (2026).
- O4 sell.amazon.com/brand-registry (EUA, 2026).
- O5 sell.amazon.com/tools/product-opportunity-explorer (EUA, 2026).
- O6 developer-docs.amazon/sp-api/docs/report-type-values-analytics (relatórios do Brand Analytics, atualizada 2026-10-06; lista o BR entre 18 lojas).
- O7 venda.amazon.com.br/sellerblog/descubra-como-se-planejar-melhor-para-vender-em-datas-sazonais (2026-09-16).
- Webinars oficiais acima (O_kXw3vvD8s, nDtHI8fUEAA, 7ILvtU6GcPo, VvcswcsjuUw) contam como [OFICIAL] por virem do canal da Amazon Brasil.

**Camada de dados**
- D1 junglescout.com/resources/reports/amazon-seller-report-2025 (pesquisa de 10 a 27/01/2025).
- D2 junglescout.com/blog/amazon-sales-rank (2023-12-08).
- D3 helium10.com/blog/how-to-find-products-to-sell-on-amazon (2024-09-04).
- D4 smartscout.com/smartscouts-accuracy-vs-amazons-reliability (s/d).
- D5 marketplacepulse.com/articles/china-won-amazons-top-10000-america-kept-its-top-100 (2026-07-09).
- D6 marketplacepulse.com/articles/amazons-ai-doesnt-read-the-rankings (2026-07-16).
- D7 SmartScout, guia de market share por categoria (2025-12-03), **via frente método** (metodo/estado-da-arte.md, seção 3.3).

**Observação direta:** `observacao/lideres.md` não existe; usei `observacao/lideres.tsv` (11 linhas, 2026-10-14) [OBS].

**Limite desta rodada:** o orçamento de buscas na web da sessão acabou no início do trabalho. Usei só WebFetch em URLs conhecidas. As páginas de ajuda do Seller Central (variações, kits virtuais, alimentos) pedem login e não puderam ser lidas.

---

## 1. Resumo executivo

1. **O teto da categoria é medido em três camadas que não se somam.** Primeiro o dado da própria Amazon (Explorador de Oportunidades de Produto e Brand Analytics). Depois a estimativa de ferramenta (SmartScout, Jungle Scout, RadarScout, Genius Pro). Por último a conta de prateleira (preço × selo "mais de X compras no mês passado"). (O5, O6, TkQHhJ8DyRc, m4WQtEMVfjE)
2. **O dado oficial de mercado mais rico é o Brand Analytics, e ele chega ao Brasil.** A documentação da API lista o BR entre 18 lojas com Search Query Performance, Market Basket e Repeat Purchase. O acesso exige Brand Registry e o papel Brand Analytics. [OFICIAL] (O6, 2026-10-06) **[MARCA]**
3. **O Explorador de Oportunidades agrupa a demanda em "nichos" pelo que o comprador vê e compra depois de buscar.** Mostra volume de busca, crescimento, unidades em faixa, devolução e temas de review. A versão BR mostrada em junho de 2026 não tinha "demandas não atendidas". [OFICIAL] O5; [PRÁTICA] pAOzjHI4UF0
4. **Critérios de entrada repetidos pelos praticantes:** demanda já provada (avaliações e selo de compras), margem conferida na calculadora, concorrência avaliada pela maturidade dos anúncios líderes e fuga da Buy Box com a Amazon varejo (1P). (1fXOj1mcRuU, dJLRqoodacM, TkQHhJ8DyRc, vZjq7xV4DB0)
5. **Faixa de preço é critério, não detalhe.** Praticantes filtram acima de R$ 50 a R$ 80. A régua oficial de incentivo do FBA (tarifa fixa de R$ 6) começa em **R$ 79**. [OFICIAL] O2; [PRÁTICA] vZjq7xV4DB0
6. **Concentração se lê pelo share da Amazon 1P e das top marcas.** Exemplo de ferramenta: na Cozinha, a Amazon teria 18,5% das vendas; num pote Electrolux, 100%. A SmartScout trata uma marca com cerca de 70% como entrada difícil. [DADO, estimativa] (TkQHhJ8DyRc; D7)
7. **Variação oficial:** temas por cor, tamanho e quantidade; o SKU pai não controla estoque; não há limite de variações; kits podem ser variações. A versão personalizada vai em anúncio separado. [OFICIAL] (O_kXw3vvD8s, 2026-10-13)
8. **Kits:** o FBA aceita kit físico (itens juntos, uma etiqueta; o CD não prepara). Dono de marca pode criar **kit virtual** sem preparação. Kit sem GTIN pede isenção, e o Listing Hub gratuito faz o pedido. [OFICIAL] (VvcswcsjuUw, 7ILvtU6GcPo, nDtHI8fUEAA)
9. **O curva A de outros marketplaces não é o curva A da Amazon.** A agência leva o catálogo inteiro (200 SKUs no exemplo) e só depois corta. A Head de FBA manda poucas unidades do curva A até a ferramenta de recomendação ter cerca de 3 meses de dados. (VH7Q5FddoRY; VvcswcsjuUw [OFICIAL])
10. **A racionalização de SKU é feita pelo financeiro**, não pelo faturamento: margem por SKU, giro, dependência, devolução e custo de recompra. A armazenagem de longo prazo (R$ 525/m³ acima de 365 dias) pune a cauda parada. (SqoNj2DDRSU, 4Vvrft5eTDo; O2 [OFICIAL])
11. **Para expandir o mix, o dado oficial é o Market Basket** (ASIN comprado junto, rank e % de combinação) e o Repeat Purchase (clientes recorrentes, receita de recompra). Nenhum praticante brasileiro do conjunto mostrou esses relatórios em tela. [OFICIAL] O6; lacuna de prática
12. **Tendência cedo:** o Explorador olha outros países ("uma hora vem para cá"), mostra crescimento em 90/180/360 dias e o movimento de ranking nas ferramentas. O ML aparece como fonte antecedente para o próprio Brasil. (pAOzjHI4UF0, xr-i6O8kxI8, 1fXOj1mcRuU)
13. **Revenda** compete por custo e Buy Box (margem média citada de 8%); **marca própria** compete por ranqueamento e ferramentas de marca (aporte citado de R$ 10 mil a R$ 50 mil por SKU). Ambos os números são N7 (CpeAKSyctRg).
14. **Para consumíveis, o desenho do mix gira em torno de recompra.** Programe e Poupe com 10% a 15% de desconto rende "até 1,8x" de conversão, segundo dado interno sem data. No café, os líderes são 1P com variações de sabor e tamanho no mesmo anúncio. [OFICIAL] O3/O4; [OBS] lideres.tsv
15. **Os praticantes brasileiros quase não reportam incerteza:** número de ferramenta aparece como fato. Só as ferramentas admitem erro: a SmartScout fala em 80% a 90% de acerto, com marca "fora" em mais de 20% (D4, D2).

---

## 2. Como funciona (mecânica e regras oficiais, com data)

### 2.1 Ferramentas oficiais de seleção

**Explorador de Oportunidades de Produto (Product Opportunity Explorer, POE)** [OFICIAL] O5 (EUA, 2026); tela BR em pAOzjHI4UF0 (2026-06-17)
- Fica em Seller Central > Crescimento. É gratuito para quem tem conta de vendedor.
- Agrupa termos de busca em **nichos** pelo que o cliente vê ou compra depois de buscar, e não pela árvore de categorias.
- "Demanda não atendida" é um grupo de termos com conversão abaixo da referência. Na tela BR de junho de 2026, esse bloco ainda não estava disponível (pAOzjHI4UF0).
- Blocos descritos: demanda e compra, competição e saturação, termos e volume, reviews e devolução, preço e tendência de vendas.
- Na tela BR: volume de busca em 360 e 90 dias com crescimento, unidades vendidas por produto **em faixa** (ex.: "500 a 750"), índice de devolução, preço médio, produtos mais clicados, resumo de reviews positivos e negativos e motivos de devolução (no exemplo da garrafa térmica, vazamento). É possível salvar a oportunidade com a intenção de lançamento "em 1 a 4 meses".
- Dado de 1ª parte, mas agregado e em faixas. Não dá receita exata.

**Brand Analytics** [OFICIAL] O6 (developer docs, 2026-10-06); O3/O4
- Elegibilidade: vendedor ou fornecedor com o papel Brand Analytics e marca no Brand Registry. Para o Amazon Search Terms, também é preciso ser representante da marca.
- Lojas: 18, incluindo **BR**, para Search Catalog Performance, Search Query Performance (SQP), Market Basket e Repeat Purchase.
- **SQP:** por ASIN e termo, com volume da busca e impressões, cliques, carrinho e compras. Traz totais e o share do ASIN em cada etapa. Histórico de até **17 meses** no recorte mensal.
- **Market Basket:** ASIN, item comprado junto ("purchasedWithAsin", que pode não ser seu), rank e % de combinação. Períodos de dia, semana, mês e trimestre.
- **Repeat Purchase:** pedidos, clientes únicos, % de clientes recorrentes, receita de recompra e % da receita. Períodos de semana, mês e trimestre.
- **Amazon Search Terms:** termo, rank de frequência, ASINs mais clicados, click share e conversion share.

**Registro de marca (Brand Registry)** [OFICIAL] O3 (BR, 2026); 7ILvtU6GcPo (2026-09-11)
- Requisitos: logotipo com o nome da marca fixado no produto ou na embalagem, e marca registrada ou "em processo de registro". O titular cadastra; agente não.
- No webinar BR, o protocolo do INPI basta para o cadastro. Com protocolo só não se pode **denunciar** violação. Conteúdo A+, loja, Sponsored Brands/Display e kits virtuais funcionam.
- É preciso ter produto: o cadastro pede foto do produto com a logo.
- Ferramentas citadas: Brand Analytics, A+, Brand Store gratuita, Patrocinados, Project Zero e Programe e Poupe.

### 2.2 Variações e kits (o "formato" do produto)

**Variações** [OFICIAL] O_kXw3vvD8s (2026-10-13)
- Família pai/filho. O **SKU pai** só agrupa a família e não controla estoque; o estoque é dos SKUs filhos.
- Temas: cor, tamanho, quantidade, ou cor e tamanho juntos. "Tem limite de variação? Não, não tem."
- **Kit como variação:** kits de 3 camisetas pretas, brancas ou mistas podem ser filhos do mesmo pai.
- **Quantidade:** cada filho tem dimensão e peso próprios, o que muda a tarifa de envio de cada um.
- **Personalizado:** recomendado como produto novo, não como variação, para não confundir o cliente.
- Produtos soltos podem ser agrupados depois (efeito em até 24 a 48 h). Em produto por "match" (catálogo de outra marca), o agrupamento pode exigir ticket.

**Kits** [OFICIAL]
- Kit físico no FBA é permitido e "muito recomendado". Os itens vão juntos numa embalagem com **uma etiqueta**, e o CD não faz preparação (VvcswcsjuUw, 2026-09-24).
- **Kit virtual (virtual bundle):** combo criado sem preparação prévia para o CD, para dono de marca em FBA (7ILvtU6GcPo, 2026-09-11; O4).
- Kit sem EAN da GS1 pede **isenção de GTIN**. O Listing Hub (time da Amazon BR, gratuito) faz o pedido e cadastra, com prazo-alvo de 10 dias úteis (nDtHI8fUEAA, 2026-08-20).
- Um EAN se vincula a um único ASIN; cada variação tem o seu (nDtHI8fUEAA).
- Produto de marca alheia entra por "match" no anúncio existente, sem trocar título e imagem. Só o dono da marca edita (nDtHI8fUEAA).

### 2.3 Tarifas e limites que mudam a conta do mix

| Regra | Valor | Fonte | Data | Observação |
|---|---|---|---|---|
| Comissão Comidas e bebidas | 10% (mínimo R$ 1,00) | O1 | 20/01/2025 | (pode estar superada) |
| Comissão Cozinha, Casa, Pets, Saúde | 12% | O1 | 20/01/2025 | (pode estar superada) |
| Faixa geral de comissão | 10% a 15% | O1 | 20/01/2025 | praticante fala em "10 a 20%", divergente (vZjq7xV4DB0) |
| Plano Profissional | grátis no 1º ano; R$ 19/mês a partir do 13º mês | O1 | 2026 | a página cita R$ 2,00 por item também no Profissional; conferir |
| FBA tarifa fixa | R$ 6 para produto a partir de R$ 79, com Ads ≥ 3,5% da receita elegível | O2 | 2026 | a frente social viu a mesma regra em vídeo oficial de 2026-07-16 |
| Comissão reduzida FBA | 5% nas primeiras 100 unidades (50 extragrandes) de novo produto Prime, até 120 dias | O2 | 2026 | incentivo de lançamento |
| FBA grátis | 30 dias sem tarifa de logística, coleta e armazenagem | O1/O2 | 2026 | — |
| Armazenagem mensal | R$ 75/m³ (< 10 mil cm³); R$ 37,50/m³ (maiores) | O2 | 01/08/2025 | (pode estar superada) |
| Armazenagem de longo prazo | R$ 525/m³ acima de 365 dias | O2 | 01/08/2025 | (pode estar superada) |
| Invendável no CD | descartado 30 dias após marcado, sem reembolso | O2 | 2026 | — |
| Tamanho FBA | até 22 kg; nenhum lado acima de 100 cm; soma até 200 cm | O2 | 2026 | a página também cita 105 cm: conflito interno; confirmar |
| DBA por unidade | R$ 4,50 (< R$ 30); R$ 6,50 (R$ 30 a 49,99); R$ 6,75 (R$ 50 a 78,99) | O1 | 2026 | varia por estado e peso |

---

## 3. O que os melhores fazem

### 3.1 Tamanho e teto da categoria (e como reportam a incerteza)

**Consenso**
- **De cima para baixo:** categoria → subcategoria → nicho → produto. O motivo é saber se dá para escalar: um produto que vende R$ 5 mil por mês num mercado pequeno obriga a ampliar muito o portfólio, e cada concorrente novo fatia esse teto. [PRÁTICA] TkQHhJ8DyRc (com tela da ferramenta; N7 nas afirmações por CTA)
- **Conta de prateleira:** preço × selo de compras. Exemplo: adaptador de cápsula a R$ 49,49 com "mais de 100 compras no mês passado", logo "pelo menos R$ 5.000 por mês" e 13 ofertas no ASIN. [PRÁTICA] m4WQtEMVfjE (tela)
  - Nota de método: o selo é um piso em degraus (100+, 500+, 1 mil+, 10 mil+, como visto em lideres.tsv). A conta dá **limite inferior**, não estimativa central.
- **Contagem de selos nos resultados orgânicos,** pulando os patrocinados. Em "carregador de iPhone": 1 mil, 2 mil, 500... compras por anúncio, logo "alta demanda". [PRÁTICA] dJLRqoodacM (tela)
- **Soma de mercado por palavra-chave na ferramenta** (Genius Pro, "Keyword Scan"): faturamento estimado somado e número de anúncios com tag de 50+ vendas no mês. [PRÁTICA] xr-i6O8kxI8 (N7; afiliado)

**Exemplo de números de ferramenta (estimativa, método não publicado)** [DADO] TkQHhJ8DyRc (RadarScout, 2026-07-10, últimos 12 meses):
- Cozinha: R$ 1,9 bilhão, ticket R$ 141,86, Amazon com 18,5% de share, 42% das ofertas em FBA.
- Organizadores: R$ 237 milhões, ticket R$ 73, Amazon com 15%.
- Armazenamento de alimentos: tendência de +18,6%, "3,6 milhões de vendas".
- Pote Electrolux: Amazon com 100% das vendas, cerca de R$ 600 mil por mês estimados.

**Como a incerteza é reportada**
- Praticantes brasileiros do conjunto: **não reportam**. Os números de RadarScout e Genius Pro aparecem como fato (TkQHhJ8DyRc, xr-i6O8kxI8).
- As próprias ferramentas:
  - SmartScout: acerto de 80% a 90% "na maioria das marcas"; uma marca pode errar em mais de 20%, mas o share e a tendência seriam "directionally correct". [DADO] D4, s/d.
  - Jungle Scout: o BSR não tem fórmula pública e muda de hora em hora. O mesmo rank 100.000 equivale a cerca de 30 vendas/mês em Cozinha e a cerca de 200 em Livros. [DADO] D2, 2023-12-08 (EUA).
- Método dos profissionais (frente método): estimativa serve para **eliminar e priorizar**, não para projetar receita. Reportar sempre em faixa e com o nome da ferramenta.

### 3.2 Critérios para entrar ou não

**Consenso (com ids)**
1. **Demanda já provada:** avaliações na 1ª página, "quem valida o produto para mim é meu concorrente" (1fXOj1mcRuU); selos de compra altos nos orgânicos (dJLRqoodacM); 4 a 6 meses de venda contínua (rN4j4kZvkDg, contexto ML).
2. **Margem antes de comprar:** calculadora da Amazon com o ASIN do concorrente (dJLRqoodacM, tela); custo-alvo reverso, ex. até R$ 25 para vender a R$ 49,49 (m4WQtEMVfjE); preço com imposto (Simples "pelo menos 4%"), comissão, frete, prep e cerca de 3% de perdas (vZjq7xV4DB0, N7).
3. **Concorrência pela qualidade:** o critério "matador" é a maturidade dos líderes (anúncio, preço, avaliações) (1fXOj1mcRuU); muitos vendedores a R$ 17 num item de R$ 28,90 levam a sair (dJLRqoodacM).
4. **Fugir de Buy Box com a Amazon varejo (1P)** e de produto que a Amazon domina (vZjq7xV4DB0; TkQHhJ8DyRc filtra "vendido pela Amazon: não" e no mínimo 3 ofertas).
5. **Faixa de preço:** acima de R$ 50, de preferência acima de R$ 80, porque um produto de R$ 19 "fica muito esmagado" (vZjq7xV4DB0). Filtro de ticket a partir de R$ 60 na Cozinha, ou teto por incentivo de frete (TkQHhJ8DyRc).
6. **Sem bloqueio de categoria (gating):** evitar eletrônicos, bebê e alimentos que exigem Anvisa ou licença sanitária (vZjq7xV4DB0, N7). Contraponto: categoria difícil de entrar é "oceano azul" por ter menos concorrência, como no exemplo de airsoft com autorização do Exército (kDF4gtMCAdo).
7. **Cabe no FBA:** 22 kg, lado até 100 cm, soma até 200 cm. "Só eu no FBA" num produto que não cabe no FBA é armadilha (vZjq7xV4DB0; regra em O2).
8. **Tendência e sazonalidade:** não entrar em curva de demanda caindo e olhar o substituto (rN4j4kZvkDg). Crescimento de 90/180/360 dias no Explorador (pAOzjHI4UF0).
9. **Devolução:** índice e motivos de devolução do nicho no Explorador (pAOzjHI4UF0). Um "curva A" com devolução alta deixou de fazer sentido (SqoNj2DDRSU).
10. **Existir palavra-chave:** produto novo demais, sem termo de busca, é difícil num marketplace de busca. "Vender o que está vendendo" (tpS__DSMMqo, EUA).

**Divergências**
- **Nicho pouco disputado ou produto muito disputado.**
  - De um lado: fugir do óbvio e ir para a subcategoria funda, como adaptador de cápsula com 13 ofertas (m4WQtEMVfjE); demanda alta com baixa competitividade (1fXOj1mcRuU).
  - Do outro: entrar no produto com mais de 100 vendedores, porque o alvo vira só preço de custo (yeN1TYy2LoE, N7). Na mesma fonte, a ressalva: para quem começa com pouco caixa, nicho com menos gente.
  - Leitura: a divergência é de **porte e caixa**, não de método. Fontes N6/N7, sem teste.
- **Genérico sem Buy Box.** Para um praticante, genérico "não participa" de Buy Box por regra (CpeAKSyctRg). A observação mostra um genérico de marca de importador com **53 ofertas** no mesmo ASIN (lideres.tsv, suporte de notebook). O webinar oficial recomenda evitar listar como genérico (nDtHI8fUEAA). A afirmação do praticante fica sem confirmação.
- **Validar ou ser pioneiro.** Esperar o concorrente validar (1fXOj1mcRuU) contra "lance quatro, não um", porque um pode pegar (tpS__DSMMqo, citando o fundador da Zulay). Os dois aceitam taxa alta de erro por produto.

### 3.3 Concentração

- **O que medem:** share da Amazon 1P na categoria (18,5% na Cozinha, RadarScout), share da marca no produto (100% Electrolux), número de ofertas no ASIN e taxa de Buy Box por vendedor (TkQHhJ8DyRc, tela).
- **Como leem para entrada:**
  - Amazon com share alto no produto: não revender. Isso não impede lançar produto **similar** com marca própria ou genérico, porque o tamanho de mercado está provado (TkQHhJ8DyRc). **[REVENDA]** x **[MARCA]**
  - Campo fragmentado sugere abertura; uma marca com cerca de 70% sugere entrada difícil (D7, via frente método; SmartScout, 2025-12-03).
  - Oficial com marca: no **Amazon Search Terms**, click share e conversion share dos 3 ASINs mais clicados por termo (O6). É o recorte oficial de concentração por busca.
- **Rotatividade dos líderes (EUA):** 68,6% dos top 10 mil vendedores já estavam no topo um ano antes (67% em 2019). O topo é estável, e quem entra disputa com incumbentes que acumulam reviews e posição (D5, 2026-07-09; tpS__DSMMqo).
- **Lacuna:** nenhum praticante brasileiro do conjunto calcula o share das top 3 a 5 marcas de forma explícita.

### 3.4 Sortimento por canal e formato

- **Catálogo inteiro primeiro, corte depois:** o curva A de outro marketplace "às vezes não é a mesma coisa" na Amazon; ampliar com variações e kits e usar o Explorador (VH7Q5FddoRY, agência, 2026-08-19). **[AMBOS]**
- **Variação de tamanho e pack como motor de crescimento:** fita 2×30 virou 2×10, 2×60, 3×20 e pack de 6. A operação tem cerca de 500 SKUs e "mais de US$ 1 milhão por mês" nos EUA, números autodeclarados sem período (tpS__DSMMqo). **[MARCA]**
- **Kits:** kit de 4 refis de mop (4Vvrft5eTDo). Bundling de item muito procurado com item de giro lento sobe o ticket e dilui o frete (O7, oficial, 2026-09-16).
- **Preço por canal:** "omnicanal não é omnipreço". O preço sai da margem de contribuição de cada canal, porque comissão, imposto e frete variam. Fórmula: preço = (custo + lucro) ÷ (1 − taxas), ou custo ÷ (1 − taxas − margem-alvo) (cZysnqICrkY, tela). Persona por canal: a Shopee pede preço; o ML aceita credibilidade (SqoNj2DDRSU).
- **Faixas impostas pela tarifa:** os degraus do DBA (R$ 30, R$ 50, R$ 79) e a régua de R$ 79 do FBA criam faixas de preço próprias da Amazon. Ferramentas oferecem filtro de preço para caber no incentivo (TkQHhJ8DyRc, xr-i6O8kxI8). [OFICIAL] O1/O2
- **SKU exclusivo de canal:** sem evidência direta para a Amazon no conjunto. O kit montado "exclusivo meu", com preço próprio, aparece em fonte multicanal (SqoNj2DDRSU).

### 3.5 Racionalização de SKU

- **Curva ABC por papel no portfólio:** o curva A vende "100, 200, 300, 500 unidades dia" e passa por todos os critérios; o B/C entra por margem e compõe "20%, 30%" do portfólio (1fXOj1mcRuU, N7).
- **SKU "com propósito":** cada SKU justifica margem, giro ou facilidade de embalar; olha-se margem por SKU, dependência do faturamento, giro e devolução. Uma cliente dependente de um SKU de margem baixa viu o faturamento cair pela metade (SqoNj2DDRSU, sem números auditáveis). O custo de cauda parada no FBA está na seção 2.3.
- **Cortar quando a recompra não fecha:** a tampa de micro-ondas zerou o estoque, mas o preço do fornecedor na recompra já não dava margem, e o produto foi descartado (4Vvrft5eTDo). No revendido: "até enquanto tá te dando lucro" (1fXOj1mcRuU).
- **CM2 negativa (margem depois de Ads):** sem demonstração brasileira no conjunto. A "variável" Ads come a margem de produto que "fatura bem" (vZjq7xV4DB0). Método formal na frente método: ACOS de equilíbrio = margem antes de Ads ÷ preço.
- **Canibalização entre variações:** sem evidência de praticante. Mecânica relevante: a SmartScout divide a receita do rank entre os filhos da família pelo peso das reviews (D4). Por isso a estimativa por filho é ainda mais incerta que a da família.

### 3.6 Market Basket, recompra e Traffic Graph

- **Oficial:** Market Basket com o ASIN comprado junto e a % de combinação; Repeat Purchase com % de clientes recorrentes e receita de recompra, ambos no BR (O6). **[MARCA]**
- **Uso descrito por profissionais (frente método):** Market Basket indica o próximo SKU ou kit; a SmartScout usa o Traffic Graph para achar vizinhos e variações que ampliam share (metodologia não publicada). Uma agência dos EUA trata 30% ou mais de compradores recorrentes como alvo em consumíveis, com dado autocompilado.
- **No Brasil, nesta base:** só o Explorador aparece em tela, com o bloco "produto mais clicado" (pAOzjHI4UF0). Nenhum vídeo brasileiro mostrou Market Basket ou Repeat Purchase.
- **Recompra como critério de categoria:** consumível ("fralda acaba, refrigerante acaba") daria previsibilidade e "tem validado muito na Amazon" (78sSkRh2crI, PRÁTICA sem número).

### 3.7 Tendência cedo

- **Outros países no Explorador:** "o que tá estourado lá fora... uma hora vem para cá" (pAOzjHI4UF0). Hipótese de praticante, sem teste de defasagem.
- **Crescimento de busca em 90/180/360 dias** no Explorador. Exemplo: garrafa de café caiu um pouco e caneca térmica cresceu (pAOzjHI4UF0).
- **Outro marketplace como antecedente:** o produto de "5 milhões" foi achado no ML, sem estar na Amazon, filtrando Full na 1ª página (1fXOj1mcRuU). A Shopee e o Google aparecem como fonte de fornecedor, não de tendência (m4WQtEMVfjE).
- **Busca por IA:** nos EUA, 63,9% das escolhas do assistente de compras ficaram fora do top 10 orgânico do termo, e 40,9% nem apareciam na página de busca. Amostra de uma conta, maio e junho de 2026 (D6). Pode mudar a lógica de "1ª página" como critério.
- **Share of search no Google:** **sem evidência** nas fontes desta frente.

---

## 4. Números de referência

| Métrica | Valor ou faixa | Fonte | Data | Tipo | Observação |
|---|---|---|---|---|---|
| Recomendação de envio ao FBA | aparece após cerca de 3 meses de dados | VvcswcsjuUw | 2026-09-24 | OFICIAL (fala) | "eu acredito" |
| Pico em datas | 3 a 10 vezes a venda diária; estoque de segurança de 15% a 20% | O7 | 2026-09-16 | OFICIAL (blog) | — |
| Catálogo com índice de qualidade alto | 4x mais visitas, 36% mais vendas | nDtHI8fUEAA | 2026-08-20 | OFICIAL, sem base | pesquisa interna sem método |
| A+ básico / premium | até 8% / até 20% de vendas | O3/O4 | s/d | OFICIAL, dado interno | "até": teto, não média |
| Programe e Poupe | 10% a 15% de desconto, até 1,8x de conversão | O3/O4 | s/d | OFICIAL, dado interno | — |
| Brand Store | compra 53,9% mais frequente; ticket 71,3% maior | O3/O4 | ago/2024 | OFICIAL, dado interno | correlação, não causa |
| Preço-alvo de praticante | acima de R$ 50, ideal acima de R$ 80 | vZjq7xV4DB0 | 2026-07-23 | PRÁTICA (N7) | — |
| Custo-alvo | cerca de 50% do preço (R$ 25 para R$ 49,49) | m4WQtEMVfjE | 2026-06-07 | PRÁTICA (N6) | exemplo único |
| Critérios EUA (Helium 10) | 300 vendas/mês ou mais; US$ 10 a 70; menos de 400 reviews; menos de 5 lb; custo de 25% do preço | D3 | 2024-09-04 | DADO (blog de ferramenta) | regra de bolso dos EUA, antiga |
| Margem média em revenda | 8% (raros 20% a 22%, temporários) | CpeAKSyctRg | 2026-10-02 | PRÁTICA (N7) | número sem base |
| Margem de contribuição em importação | acima de 25%; +10 a 15 p.p. contra compra nacional | rN4j4kZvkDg | 2026-10-06 | PRÁTICA (N7) | clientes da própria consultoria |
| Case "5 milhões, um produto" | margem de 25%, 2023 | 1fXOj1mcRuU | 2026-08-20 | PRÁTICA (rebaixado de CASE) | sem base; produto do **ML** |
| Aporte de marca própria | R$ 10 mil a 15 mil por SKU (suplemento BR); R$ 50 mil ou mais (China) | CpeAKSyctRg | 2026-10-02 | PRÁTICA (N7) | — |
| Mix B/C | 20% a 30% do portfólio | 1fXOj1mcRuU | 2026-08-20 | PRÁTICA (N7) | — |
| Cozinha BR (12 meses) | R$ 1,9 bi; ticket R$ 141,86; Amazon 1P 18,5%; 42% das ofertas FBA | TkQHhJ8DyRc | 2026-07-10 | DADO (RadarScout, método não publicado) | faixa de erro desconhecida |
| Acerto declarado | 80% a 90%; marca pode errar mais de 20% | D4 | s/d | DADO (SmartScout) | autodeclarado |
| BSR × vendas (EUA) | rank 100 mil ≈ 30/mês em Cozinha ou ≈ 200/mês em Livros | D2 | 2023-12-08 | DADO (Jungle Scout) | exemplo |
| Estabilidade do topo (EUA) | 68,6% dos top 10 mil já no topo 1 ano antes | D5 | 2026-07-09 | DADO | Amazon.com |
| Desafios do vendedor | frete 38%, custo do produto 34%, Ads 32% | D1 | jan/2025 | DADO | cerca de 1.500 respostas, 20+ países |
| Operação EUA | cerca de 500 SKUs, "mais de US$ 1 mi/mês" | tpS__DSMMqo | 2026-07-23 | PRÁTICA | autodeclarado, sem período |
| INPI exame prioritário | 90 a 180 dias contra cerca de 24 meses; 1.500 cotas por quadrimestre; taxa R$ 445 (até EPP) ou R$ 890 | kDF4gtMCAdo | 2026-06-09 | OFICIAL via terceiro (Portaria INPI 66/2026) | confirmar no INPI |

---

## 5. Alimentos, perecíveis e marca própria/indústria

**O que muda neste tema**
- **Categoria com gating:** praticantes evitam alimentos por exigir Anvisa ou licença sanitária (vZjq7xV4DB0, N7). Para quem já é indústria regularizada, esse filtro vira barreira contra revendedores, a lógica do "mais difícil, menos concorrência" (kDF4gtMCAdo, outro setor). A página oficial de produtos restritos e alimentos não pôde ser lida (exige login). **Lacuna.**
- **Comissão de Comidas e bebidas de 10%** é a menor da tabela, contra 12% em Cozinha e Casa (O1, pode estar superada).
- **Formato e variação no café [OBS]** lideres.tsv (2026-10-14):
  - O #1 da categoria (Orfeu Clássico Grãos 1 kg) é 1P, com sabor (Clássico, Intenso, Orgânico) e tamanho como variações num só anúncio, "mais de 10 mil compras no mês passado" e 16.737 avaliações.
  - Na busca "café em grãos", dominam 1 kg e 250 g, com kits de 4 pacotes e lata de 250 g.
  - Na Alimentos e Bebidas geral, os mais vendidos são packs: 2 maioneses, 12 YoPRO, 4 latas.
  - Café especial de 250 g (Coffee Mais, 1P) aparece no top 20 com selo "Escolha da Amazon".
- **Recompra e assinatura:** Programe e Poupe em café de marca 3P com FBA (Italle) e em produto de limpeza (Lysoform) (lideres.tsv). Para consumíveis, Repeat Purchase (O6) e Programe e Poupe (O3) são as alavancas oficiais de mix. O dado interno de "até 1,8x" não tem data.
- **Validade e FBA:** o conjunto não traz regra oficial de validade mínima no envio ao FBA para alimentos. A frente social registrou só um caso de cosmético, com validade e código de barras visíveis. **Lacuna.**
- **1P como concorrente e canal:** no café, os líderes são vendidos e enviados pela Amazon.com.br. Ser convidado a vender como fornecedor (Vendor) é descrito como "o sonho" por praticante (vZjq7xV4DB0). Para a marca, a Amazon 1P pode ser canal; para o revendedor, é a Buy Box a evitar.
- **Proteção de marca para indústria:** registro no INPI por classe NCL, só com itens vendidos ou pretendidos; vale só no Brasil; desenho industrial protege forma ou embalagem original (kDF4gtMCAdo, opinião jurídica, N7).

---

## 6. Erros comuns e mitos

| Afirmação (fonte fraca ou comum) | O que as fontes fortes mostram | ids |
|---|---|---|
| "2 em cada 3 produtos que o seller escolhe não vendem" | Número sem base, dito por ferramenta que vende teste grátis | TkQHhJ8DyRc (N7) |
| Estimativa de ferramenta como receita certa | As ferramentas admitem erro acima de 20% por marca e servem para direção | D4, D2 |
| Selo "100+ compras" × preço = receita | É piso em degraus; dá limite inferior | m4WQtEMVfjE; lideres.tsv |
| "Genérico não tem Buy Box, é regra da Amazon" | Genérico de importador com 53 ofertas no mesmo ASIN; oficial recomenda evitar genérico | CpeAKSyctRg; lideres.tsv; nDtHI8fUEAA |
| Incentivo FBA "a partir de R$ 100" (mai/2026) | Página oficial atual: R$ 6 fixo a partir de R$ 79, com Ads ≥ 3,5% | xr-i6O8kxI8; O2 |
| "Comissão zero por 6 meses se gastar 3,5% em Ads" | Página oficial de FBA cita 5% nas 100 primeiras unidades por até 120 dias; a regra dita na live não foi achada | vZjq7xV4DB0; O2 |

---

## 7. Revenda/importação x indústria/marca própria

| Tema | **[REVENDA]** revenda, importação, genérico | **[MARCA]** indústria, marca própria |
|---|---|---|
| Fonte do produto | Mais Vendidos, ferramenta, fornecedor e importador achados via Shopee, Google e Instagram (m4WQtEMVfjE) | Portfólio próprio; expansão por Market Basket e variação de tamanho ou pack (O6; tpS__DSMMqo) |
| Critério central | Preço de custo competitivo; "o alvo se torna só um preço de custo" (yeN1TYy2LoE) | Share de busca e conversão (SQP), recompra, ferramentas de marca (O6) |
| 1ª página e FBA | Ser o 1º vendedor FBA do ASIN dá selo Prime (VvcswcsjuUw); ML Full na 1ª página como sinal (1fXOj1mcRuU, ML) | Ranqueamento do ASIN próprio por Ads e SEO; genérico ou marca nova "começa mal posicionado" (CpeAKSyctRg) |
| Buy Box | Disputa por preço, prazo e avaliação; risco com a Amazon 1P e marcas grandes (CpeAKSyctRg; vZjq7xV4DB0) | Buy Box aberta, mas com denúncia de falsificação (Brand Registry; com protocolo, sem denúncia) (7ILvtU6GcPo) |
| Concentração | Evitar produto com Amazon 1P dominante; mínimo de 3 ofertas para indicar revenda possível (TkQHhJ8DyRc) | Concentração alta no produto mostra mercado provado para lançar similar (TkQHhJ8DyRc) |
| Margem típica citada | 8% em revenda de marca (CpeAKSyctRg, N7); acima de 25% em importação (rN4j4kZvkDg, N7) | Sem número confiável; investimento de R$ 10 mil a 50 mil por SKU (CpeAKSyctRg, N7) |
| Ciclo do SKU | Sem apego: troca quando o preço cai ou falta fornecedor (1fXOj1mcRuU) | Ativo de longo prazo; reviews e posição são o principal ativo (tpS__DSMMqo) |
| Kits | Kit físico no FBA (VvcswcsjuUw); kit sem GTIN com isenção (nDtHI8fUEAA) | Kit virtual sem preparação (7ILvtU6GcPo) |
| Variações | Em produto por "match", o agrupamento pode exigir ticket; não edita título e imagem (O_kXw3vvD8s; nDtHI8fUEAA) | Controle total da família; prioridade de edição como dono da marca (7ILvtU6GcPo) |

**Vale para os dois:** começar pela demanda provada, conferir margem com todas as tarifas, olhar a qualidade dos líderes, respeitar os limites do FBA e ler a devolução do nicho.

---

## 8. Tabela de afirmações

| id | afirmação | tipo | fonte | data | confiança |
|---|---|---|---|---|---|
| A1 | Relatórios SQP, Search Catalog Performance, Market Basket e Repeat Purchase estão disponíveis no BR para quem tem Brand Registry e papel Brand Analytics | OFICIAL | O6 | 2026-10-06 | alta (B; N1 único) |
| A2 | SQP traz share do ASIN em impressão, clique, carrinho e compra, com histórico de até 17 meses | OFICIAL | O6 | 2026-10-06 | alta |
| A3 | Market Basket traz o ASIN comprado junto, o rank e a % de combinação | OFICIAL | O6 | 2026-10-06 | alta |
| A4 | O Explorador agrupa nichos pelo que o cliente vê ou compra após a busca e mostra devolução e reviews | OFICIAL + PRÁTICA (tela BR) | O5; pAOzjHI4UF0 | 2026 / 2026-06-17 | alta (A) |
| A5 | A versão BR do Explorador não tinha "demandas não atendidas" em jun/2026 | PRÁTICA | pAOzjHI4UF0 | 2026-06-17 | média (C) |
| A6 | Brand Registry BR aceita protocolo INPI; com protocolo não se denuncia violação | OFICIAL | 7ILvtU6GcPo; O3 | 2026-09-11 | alta (A) |
| A7 | Kit virtual para dono de marca, sem preparação prévia no CD | OFICIAL | 7ILvtU6GcPo; O4 | 2026-09-11 | alta (A) |
| A8 | Kit físico no FBA: itens juntos, uma etiqueta; o CD não prepara | OFICIAL | VvcswcsjuUw | 2026-09-24 | média (B) |
| A9 | Kit sem GTIN exige isenção; o Listing Hub gratuito pede e cadastra | OFICIAL | nDtHI8fUEAA | 2026-08-20 | média (B) |
| A10 | SKU pai não controla estoque; sem limite de variações; temas cor, tamanho e quantidade; kit pode ser variação | OFICIAL | O_kXw3vvD8s | 2026-10-13 | média (B) |
| A11 | Versão personalizada: recomendado anúncio separado, não variação | OFICIAL | O_kXw3vvD8s | 2026-10-13 | média (B) |
| A12 | Comissão Comidas e bebidas 10%, mínimo R$ 1 | OFICIAL | O1 | 20/01/2025 (pode estar superada) | média (B) |
| A13 | FBA: R$ 6 fixo para produto a partir de R$ 79, condicionado a Ads ≥ 3,5% | OFICIAL | O2; frente social (vídeo oficial 2026-07-16) | 2026 | alta (A) |
| A14 | FBA: comissão de 5% nas 100 primeiras unidades de novo produto Prime, até 120 dias | OFICIAL | O2 | 2026 | média (B) |
| A15 | Armazenagem de longo prazo R$ 525/m³ acima de 365 dias; invendável descartado em 30 dias | OFICIAL | O2 | 01/08/2025 (pode estar superada) | média (B) |
| A16 | Limite FBA: 22 kg, lado até 100 cm, soma até 200 cm | OFICIAL + PRÁTICA | O2; vZjq7xV4DB0 | 2026 | alta (A), com conflito de 105 cm na página |
| A17 | Recomendações de envio ao FBA aparecem após cerca de 3 meses; começar com o curva A em poucas unidades | OFICIAL (fala) | VvcswcsjuUw | 2026-09-24 | média (B) |
| A18 | O curva A de outros canais difere na Amazon; trazer o catálogo inteiro e expandir com kits e variações | PRÁTICA (agência) | VH7Q5FddoRY | 2026-08-19 | média (C+; converge com A17) |
| A19 | Critério decisivo de entrada é a maturidade dos concorrentes (listagem, preço, avaliações) | PRÁTICA | 1fXOj1mcRuU | 2026-08-20 | baixa (C, N7) |
| A20 | Demanda medida por selos de compra nos orgânicos; margem pela calculadora com o ASIN do concorrente | PRÁTICA | dJLRqoodacM; m4WQtEMVfjE | 2026-07 / 2026-06 | média (duas N6 concordantes) |
| A21 | Selo "mais de X compras" × preço dá piso de receita, não estimativa central | OBS + método | lideres.tsv; m4WQtEMVfjE | 2026-10-14 | média |
| A22 | Evitar Buy Box com a Amazon 1P; filtro de no mínimo 3 ofertas e "não vendido pela Amazon" | PRÁTICA | vZjq7xV4DB0; TkQHhJ8DyRc | 2026-07 | média (duas fontes, ambas N7) |
| A23 | Cozinha BR: R$ 1,9 bi em 12 meses, Amazon 1P com 18,5% | DADO (estimativa RadarScout) | TkQHhJ8DyRc | 2026-07-10 | baixa (C) |
| A24 | Uma marca com cerca de 70% de share indica entrada difícil | DADO | D7 (via frente método) | 2025-12-03 | baixa (C) |
| A25 | SmartScout: acerto de 80% a 90%; marca pode errar mais de 20% | DADO | D4 | s/d | média (autodeclarado) |
| A26 | Top 10 mil dos EUA: 68,6% já estavam no topo um ano antes | DADO | D5 | 2026-07-09 | média (B) |
| A27 | Assistente de IA (EUA): 63,9% das escolhas fora do top 10 orgânico | DADO | D6 | 2026-07-16 | baixa (amostra de uma conta) |
| A28 | Margem média em revenda de marca de 8% | PRÁTICA | CpeAKSyctRg | 2026-10-02 | baixa (N7) |
| A29 | Marca própria custa R$ 10 mil a 15 mil por SKU (suplemento BR) e R$ 50 mil ou mais (China) | PRÁTICA | CpeAKSyctRg | 2026-10-02 | baixa (N7) |
| A30 | Curva B/C compõe 20% a 30% do portfólio, escolhida por margem | PRÁTICA | 1fXOj1mcRuU | 2026-08-20 | baixa (N7) |
| A31 | Racionalizar por margem, giro, dependência e devolução por SKU | PRÁTICA | SqoNj2DDRSU; 4Vvrft5eTDo | 2026-06 / 2026-09 | média (duas N6/N7 concordantes) |
| A32 | Variações de tamanho e pack impulsionaram uma operação de cerca de 500 SKUs nos EUA | PRÁTICA | tpS__DSMMqo | 2026-07-23 | baixa (autodeclarado) |
| A33 | Bundling de item de alta procura com item de giro lento sobe o ticket e dilui o frete | OFICIAL (blog) | O7 | 2026-09-16 | média (B) |
| A34 | Programe e Poupe com 10% a 15% de desconto: até 1,8x de conversão | OFICIAL (dado interno) | O3; O4 | s/d (pode estar superada) | média |
| A35 | No café, os líderes são 1P com variação de sabor e tamanho no mesmo anúncio; 1 kg e 250 g dominam | OBS | lideres.tsv | 2026-10-14 | média (observação única) |
| A36 | Preço por canal deve sair da margem de contribuição de cada canal | PRÁTICA | cZysnqICrkY | 2026-05-14 | média (método padrão) |
| A37 | INPI prioritário para vendedor de marketplace: 90 a 180 dias, 1.500 cotas por quadrimestre | OFICIAL via terceiro | kDF4gtMCAdo | 2026-06-09 | baixa (confirmar Portaria 66/2026) |

---

## 9. Lacunas

1. **Páginas de ajuda do Seller Central BR** (variações, kits virtuais com mínimo e máximo de componentes, produtos restritos, alimentos e validade no FBA) exigem login. As regras vieram de webinars oficiais e precisam de checagem na ajuda escrita.
2. **Busca na web esgotada nesta rodada:** não foi possível achar estudos de Pacvue, Perpetua ou Nubimetrics específicos de Amazon BR. Os relatórios Jungle Scout 2024 e 2025 só liberam no PDF a divisão por modelo de negócio (marca própria x revenda) e as faixas de margem.
3. **Incerteza das estimativas no Brasil:** nenhuma ferramenta brasileira (RadarScout, Genius Pro, Avantpro) publica método ou erro para a Amazon BR.
4. **Concentração top 3 a 5:** nenhum praticante brasileiro mostra o cálculo. O recorte oficial possível é o Amazon Search Terms (click share e conversion share dos 3 primeiros ASINs), não demonstrado em vídeo brasileiro.
5. **Market Basket e Repeat Purchase em uso real no BR:** sem demonstração em tela. Sem benchmark brasileiro de taxa de recompra por categoria.
6. **CM2 negativa e canibalização entre variações:** sem caso brasileiro com números.
7. **Share of search no Google** como sinal antecedente: sem evidência nas fontes.
8. **Defasagem EUA → Brasil** de tendências (premissa do Explorador global): hipótese sem medição.
9. **Kits de alimentos e GTIN:** sem regra específica nas fontes lidas.
10. **Incentivos que mudam rápido** (comissão reduzida, R$ 6 fixo, isenções): versões divergentes entre lives de maio a julho de 2026 e a página oficial atual. Confirmar a vigência na data de uso.
11. **Portaria INPI 66/2026** (exame prioritário para marketplace): vista só via advogada em podcast com oferta comercial. Confirmar no site do INPI.


## 10. Verificação (2026-10-14)

Método: leitura das páginas oficiais por WebFetch em 2026-10-14. Orçamento de WebSearch esgotado na rodada, então R9 a R11 (páginas de ajuda do Seller Central, com login) não puderam ser checadas em texto escrito. Regras de tarifa/política com mais de 6 meses: pode estar superada.

| id | veredito | fonte oficial (URL) | observação |
|---|---|---|---|
| R1 | CONFIRMADA | https://venda.amazon.com.br/precos | [OFICIAL] 10% com mínimo de R$ 1,00 por item; faixa geral 10% a 15% ("Demais categorias" 15%). Comissões atualizadas em 20/01/2025: pode estar superada. |
| R2 | CONFIRMADA (com ressalva) | https://venda.amazon.com.br/precos | [OFICIAL] 1º ano grátis e R$ 19/mês a partir do 13º mês confirmados. A página também lista R$ 2,00 por item vendido além da comissão; a leitura automática não separa se vale para o Profissional ou só para o plano Individual. Conferir na tabela de planos antes de usar o R$ 2. |
| R3 | CONFIRMADA | https://venda.amazon.com.br/cresca/fba | [OFICIAL] R$ 6 por unidade para preço de venda a partir de R$ 79, com Amazon Ads mínimo de 3,5% da receita elegível; isenção de coleta e armazenagem. Vale para contas existentes; contas novas têm 30 dias de isenção. Sem data de vigência (tarifas de 01/08/2025): pode estar superada. Vídeo não revisto. |
| R4 | CONFIRMADA | https://venda.amazon.com.br/cresca/fba | [OFICIAL] 5% nas primeiras 100 unidades (50 extragrandes), por até 120 dias, em novos produtos com Entrega Prime. Sem data de vigência na página. |
| R5 | CONFIRMADA | https://venda.amazon.com.br/cresca/fba ; https://venda.amazon.com.br/precos | [OFICIAL] R$ 75/m³ (< 10 mil cm³), R$ 37,50/m³ (maiores), R$ 525/m³ acima de 365 dias; não aptos descartados sem reembolso 30 dias após a classificação. Tarifas de 01/08/2025: pode estar superada. |
| R6 | CONFIRMADA (conflito interno persiste) | https://venda.amazon.com.br/cresca/fba | [OFICIAL] 22 kg, lado até 100 cm, soma C+L+A até 200 cm. A página também diz pacote máximo 105x105x105 cm e circunferência (C+2L+2A) até 295 cm, o que contradiz o limite de 100 cm por lado. Não resolvido; tratar 100 cm como o limite conservador. |
| R7 | CONFIRMADA | https://venda.amazon.com.br/precos | [OFICIAL] R$ 4,50 (< R$ 30), R$ 6,50 (R$ 30 a 49,99), R$ 6,75 (R$ 50 a 78,99), para produtos até R$ 79. Variação por estado de origem e peso está em arquivo para download, não na página. Pode estar superada. |
| R8 | CONTESTADA | https://developer-docs.amazon/sp-api/docs/report-type-values-analytics (atualizada 2026-10-06) | [OFICIAL] Os quatro relatórios existem nas 18 lojas, incluindo BR, com role Brand Analytics + Brand Registry. Correção: "17 meses" é o máximo de períodos por requisição no recorte MONTH; a página não diz por quanto tempo o histórico fica disponível. Um pedido não pode abranger mais de um período. |
| R9 | SEM FONTE OFICIAL | https://venda.amazon.com.br/brand-registry (parcial) | A página aceita marca "registrada (ou em processo de registro)" e pedido pendente "em alguns casos", sem citar INPI nem "protocolo". Foto/embalagem com marca fixada de forma permanente confirmada. Lista de funções liberadas com protocolo e a proibição de denunciar violação só aparecem no webinar; a página, ao contrário, convida a denunciar violações. Não confirmar. |
| R10 | SEM FONTE OFICIAL | (nenhuma acessível; páginas do Listing Hub e de ferramentas de marca retornaram 404) | Regras de kit físico, kit virtual e isenção de GTIN só em webinars. Conferir na ajuda do Seller Central (exige login). |
| R11 | SEM FONTE OFICIAL | (nenhuma acessível) | Regras de variações (pai sem estoque, temas, tarifa por variação de quantidade, selo Black Friday) só no webinar de 2026-10-13. Conferir na ajuda do Seller Central (exige login). |
| R12 | CONFIRMADA | https://venda.amazon.com.br/brand-registry | [OFICIAL, dado interno] Programe e Poupe com 10% a 15% de desconto: média de até 1,8x de conversão. Brand Store: compra 53,9% mais frequente e ticket 71,3% maior, dado interno de ago/2024. É material promocional da Amazon, sem metodologia. |
