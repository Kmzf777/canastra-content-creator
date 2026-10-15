# Frente: Ranqueamento e construção do anúncio (Mercado Livre Brasil)

Data da nota: 2026-10-14. Analista da frente ranqueamento-anuncio.

**Escopo.** Busca e ranqueamento, título, ficha e atributos, catálogo e buy box, fotos, vídeo/clips, descrição, perguntas, conversão, qualidade do anúncio e testes A/B.

**Fontes lidas.**
- **Oficiais, 11 páginas N1:**
  - 6 páginas de developers.mercadolivre.com.br: qualidade das publicações, concorrência em catálogo, experiência de compra, diagnóstico de imagens, imagens, elegibilidade de catálogo;
  - 4 notas da Central de Vendedores: posicionamento na busca, experiência de compra, catálogo, anúncios duplicados;
  - API pública de categorias, consultada hoje.
- **Webinars oficiais:** 4 do canal "Vendedores Mercado Livre Brasil" (MFYKfOYs0iE, QuOP9KeKnk8, JzejZyVeauE, W1hgC6snin4) e trechos do webinar de Natal (-NK3VLYm0q0).
- **Praticantes:** 10 transcrições da lista da frente e 6 transcrições correlatas da pasta.
- **Dados:** 3 fontes de ferramentas ou blogs (Hunter HUB, Nubimetrics, Bling).
- **Observação:** a de líderes, em observacao/lideres.md.

**Limites da coleta.**
- A cota de busca na web acabou durante a coleta. Por isso, Amazon e Shopee ficaram quase sem evidência N1 (ver seção 9).
- A Central de Ajuda (mercadolivre.com.br/ajuda) carrega por JavaScript e não pôde ser lida diretamente. A regra de anúncios duplicados da ajuda 2518 chegou só via resumo de busca.

**Convenções desta nota.**
- **Tipos:** [OFICIAL], [OFICIAL via terceiro], [PRÁTICA], [CASE], [DADO], [OBS].
- **Separação de público:** [REVENDA] e [MARCA].
- **Regra antiga:** regra de plataforma anterior a 2026-04-14, ou sem data, leva "(pode estar superada)".
- **Datas dos vídeos:** é a data de publicação no YouTube. O webinar MFYKfOYs0iE foi gravado em 27/05/2026 e o QuOP9KeKnk8 em 19/05/2026.

---

## 1. Resumo executivo

1. **O ML não publica fórmula nem pesos do ranqueamento.**
   - O que declara oficialmente: os anúncios mais completos sobem na busca. Isso vale para ficha técnica preenchida, categoria certa, fotos dentro dos requisitos, uso do catálogo, preço competitivo, reputação verde e boa experiência de compra.
   - Fonte: nota "Como posicionar seus produtos nos resultados de busca", vendedores.mercadolivre.com.br, sem data (pode estar superada). [OFICIAL]
2. **Anúncios de catálogo "sempre aparecem primeiro nos resultados da pesquisa".** Fonte: a mesma nota oficial (pode estar superada). [OFICIAL]
3. **No catálogo, um algoritmo escolhe o vencedor e ele leva todas as vendas e a visibilidade.**
   - Fatores: preço, parcelamento sem juros, Full, frete grátis e envio no mesmo dia, além da reputação do vendedor.
   - Quem ganha tem `visit_share` "maximum" e quem perde tem "minimum".
   - Fonte: developers "Concorrência em catálogo", atualizada em 21/07/2026. [OFICIAL]
4. **A experiência de compra é medida por anúncio e é "essencial para a exposição".**
   - Faixas: Boa (75 a 100), Mediana (50 a 74) e Ruim (30 ou menos).
   - Anúncio Mediano perde exposição e pode ser pausado. Anúncio Ruim pode ser cancelado, sem recuperação.
   - Fonte: nota "Como oferecer a melhor experiência de compra", sem data (pode estar superada). [OFICIAL]
5. **Título e descrição inconsistentes com o produto entram no cálculo da experiência de compra.** Exemplos: falta de tamanho ou modelo, ou acessório prometido que não vem. Ou seja, a construção do anúncio afeta a exposição também pelo pós-venda. Fonte: mesma nota (pode estar superada). [OFICIAL]
6. **A qualidade das publicações tem score de 0 a 100, com níveis Básica, Satisfatória e Profissional.**
   - O score é medido por blocos: dados do produto (GTIN, ficha principal e campos obrigatórios), fotos (mínimo de 3), título (mínimo de 3 palavras) e condições de venda (frete grátis, parcelas, estoque de 2 ou mais unidades, Mercado Envios).
   - Fonte: developers "Qualidade das publicações", 31/01/2025 (pode estar superada). [OFICIAL]
7. **O título tem limite de 60 caracteres** nas 5 categorias consultadas (café em grão, gamepads, fones, camisetas, azeite). Fonte: API pública `/categories`, consultada em 14/10/2026. [OBS sobre dado N1]
   - O webinar oficial recomenda até 60 caracteres e o nome do produto nas primeiras palavras (MFYKfOYs0iE, 03/06/2026). [OFICIAL]
8. **O máximo é de 12 fotos por anúncio e 10 por variação.**
   - Tamanho recomendado: 1200x1200 px. Mínimo: 500x500 px.
   - O diagnóstico automático checa fundo branco, tamanho mínimo, texto/logo e marca d'água, conforme a categoria.
   - Fontes: API de categorias (14/10/2026) e developers "Imagens" (24/03/2026). [OFICIAL]
9. **Clips (agora "Vídeos") contam como critério de qualidade do anúncio**, segundo o ML.
   - Números divulgados pela plataforma, sem método publicado e com provável viés de seleção: anúncio com clipe teria 3x mais visitas e 2x mais vendas.
   - Em teste, o clipe na 1ª posição da galeria deu +10 a 15% de conversão.
   - Fonte: webinar oficial QuOP9KeKnk8 (25/05/2026). [OFICIAL] + [DADO]
10. **Anúncios duplicados não são permitidos.** São cancelados ou ocultados, e o ML mantém o de melhor visibilidade.
    - A forma certa é usar variações (cor, tamanho), que acumulam visitas e vendas num só anúncio.
    - Fonte: nota "Anúncios duplicados", sem data (pode estar superada). [OFICIAL]
11. **Alterar título ou fotos de um anúncio que já vende pode derrubar a performance**, porque "o algoritmo vai ler como um novo anúncio". Fonte: webinar oficial MFYKfOYs0iE (03/06/2026). [OFICIAL]
12. **Diagnóstico pelo funil, consenso entre praticantes:**
    - impressão baixa aponta para problema de relevância ou palavra-chave;
    - CTR baixo aponta para capa, preço, frete ou título;
    - visitas sem venda apontam para descrição, preço total, parcelamento ou confiança.
    - Fontes: tPmQZJBgWVY (13/05/2026), 5OALEDEnI1Q (08/06/2026). [PRÁTICA]
13. **Ganhar catálogo não é ter o menor preço.**
    - O doc oficial lista "boosts" (Full, frete grátis, parcelas) e motivos de exclusão (reputação abaixo do limite, envio inferior, manufacturing time).
    - Observação de praticante: uma oferta de R$141 no Full ganhava de uma de R$139 sem a melhor logística (WF333Qri_i8, 24/06/2026).
    - Tipos: [OFICIAL] + [PRÁTICA com tela].
14. **No café, 26 dos 40 primeiros resultados de "cafe em graos" tinham selo FULL.**
    - O catálogo concentra a disputa: Pilão 1kg tinha 72 vendedores e quem ganhava era um supermercado revendedor.
    - Fonte: observacao/lideres.md (14/10/2026). [OBS]
15. **Não há fonte que publique o tempo para um anúncio novo ganhar posição.**
    - O que existe são táticas de praticantes: preço de entrada baixo com alta gradual, Ads e logística melhor. É evidência fraca (N7).
    - Fontes: ZAa89f0ERE8 (08/07/2026) e TgqKYHoFIXs (06/07/2026). [PRÁTICA]

---

## 2. Como funciona (mecânica e regras oficiais)

### 2.1 Ordenação da busca (ML)

**Fatores declarados.** A nota oficial de posicionamento (sem data, pode estar superada) lista estas alavancas, sem pesos:
- **Dados do produto:** "Quanto mais informações precisas", mais fácil achar pelos filtros, e isso melhora a qualidade do anúncio.
- **Categoria certa:** a errada faz perder visibilidade. Exemplo oficial: celular em "Informática".
- **Fotos:** se não forem nítidas e fora dos requisitos, o anúncio "não vai estar entre os primeiros resultados".
- **Catálogo:** anúncios de catálogo aparecem primeiro.
- **Preço:** comparar com a concorrência. O desconto pode dar acesso à seção Ofertas, e há ajuste automático de preço com mínimo e máximo.
- **Reputação:** manter o verde, com despacho em menos de 24h, poucos cancelamentos e poucas reclamações. Vendedor com reputação vermelha tem menor exposição.
- **Experiência de compra:** responder dúvidas e evitar reclamações.
- **Programa Decola:** indicado para vendedores novos.

**Descrição oficial em webinar.**
- O ML diz que o algoritmo "vai fazer a leitura do comportamento do comprador".
- Ter mais alavancas de visibilidade (clips, afiliados, Ads, Minha Página) "permite que você chegue mais vezes" ao comprador.
- Fonte: QuOP9KeKnk8, 25/05/2026. [OFICIAL]

**Busca na API pública.** O endpoint `sites/MLB/search` e o de tendências retornam 403/401 sem token. Isso é coerente com a restrição da API para ferramentas externas (consulta de 14/10/2026). [OBS]

### 2.2 Qualidade das publicações (/performance)

Fonte: developers "Qualidade das publicações", atualizada em 31/01/2025 (pode estar superada). [OFICIAL]

- **Endpoint:** o antigo `/health` foi descontinuado e substituído por `/performance`.
- **Score e níveis:** score de 0 a 100. No Brasil, os níveis são Básica, Satisfatória e Profissional.
- **Função declarada:** o score mede o atingimento de objetivos e melhora "a exposição do item".
- **Estrutura:** buckets, que se dividem em variáveis, que se dividem em regras. Cada regra é OPPORTUNITY (oportunidade) ou WARNING (problema que "reduz o score até que seja resolvido").

Regras que aparecem no exemplo do doc:

| Bloco | Regra | Texto do ML (resumido) |
|---|---|---|
| Dados do produto | HAS_GTIN | Completar o código universal para estar mais acima na busca |
| Dados do produto | TS_MAIN_QUANTITY / TS_MAIN_QUALITY_INCOMPLETE_REQUIRED | Completar características principais e dados marcados como requeridos |
| Fotos | PICTURES_QUANTITY_MIN | Mínimo de 3 fotos, de ângulos diferentes |
| Título | TITLE_LENGTH_MIN | Título com pelo menos 3 palavras |
| Condições de venda | FREE_SHIPPING, FINANCING/BEST_FINANCING | Frete grátis e parcelas ao mesmo preço |
| Condições de venda | STOCK_DEPOSITO, STOCK_AVAILABILITY_TIME | Ao menos 2 unidades e menor prazo de disponibilidade |
| Condições de venda | ME | Envios por Mercado Envios |

Implicação de mecânica: o score de qualidade mistura conteúdo (ficha, fotos, título) com oferta (frete, parcelas, estoque, logística).

### 2.3 Experiência de compra por anúncio

**Faixas.**
- Boa (75 a 100): desempenho que se destaca.
- Mediana (50 a 74): pelo menos 2x pior que a média da categoria.
- Ruim (30 ou menos): pelo menos 3x pior.

**Efeito na exposição.**
- Abaixo de 100, o anúncio "pode começar a perder exposição".
- Mediano: perde exposição e corre risco de pausa.
- Ruim: "muito pouca exposição", risco de cancelamento sem recuperação, e o ML pode avisar compradores sobre muitas devoluções.

**Janela de cálculo.**
- Com 100 ou mais vendas em 60 dias, usa essas vendas. Se não atingir o mínimo, usa o último ano.
- Com menos de 100 vendas, completa com os outros anúncios do vendedor na mesma categoria, que precisam somar 200 ou mais vendas. Abaixo disso, o anúncio fica sem indicador.
- O período é atualizado diariamente.

**Insumos.**
- Reclamações de responsabilidade do vendedor, inclusive as excluídas da reputação.
- Atrasos e envio a partir de depósito incorreto.
- Cancelamentos feitos pelo vendedor.
- Perguntas e respostas, e opiniões sobre o produto.
- Mensagens com o comprador.
- Título e descrição incompletos ou inconsistentes.

**Outros pontos.**
- O ML aplica mudanças por IA no anúncio a partir das perguntas recebidas, avisa por e-mail e o vendedor pode reverter.
- Benefício de Reputação e Programa Decola protegem contra perda de exposição, pausa ou cancelamento.

Fonte: nota oficial, sem data (pode estar superada). [OFICIAL]

**Divergência.** O doc developers "Experiência de compra" (03/02/2026) fala em janela de 180 dias e em pausa ou anulação por experiência ruim. A Hunter HUB (12/10/2026) diz que os 180 dias são o "cálculo antigo". Prevalece a nota atual de 60/365 dias, com cautela.

**Contestação de praticantes.**
- Reclamam do cálculo "por categoria" para anúncios com poucas vendas. Um deles relata 151 anúncios "perdendo relevância" sem reclamação própria.
- Fontes: KvVyJlYt6w0 (12/08/2026), 9GJUi32R5sc (10/09/2026). [PRÁTICA]

### 2.4 Catálogo e buy box (ML)

Fonte principal: developers "Concorrência em catálogo", 21/07/2026. [OFICIAL]

**Quem decide.** "Um algoritmo determina quem será o vencedor" com base no anúncio e no vendedor: preço, parcelamento sem juros, Full, frete grátis, envio no mesmo dia.

**Status e visibilidade.**
- winning: ganha; `visit_share` maximum; leva "todas as vendas e visibilidade".
- sharing_first_place: divide o primeiro lugar; medium.
- competing: perdendo; minimum.
- listed: não compete, mas pode ser comprado pela busca geral.

**Boosts.**
- Tipos: fulfillment, free_installments, free_shipping, shipping_collect, same_day_shipping.
- Estados: boosted, not_boosted, opportunity e not_apply.

**`price_to_win`.** É o preço sugerido para ficar competitivo.

**Motivos de não competir:**
- vendedor não confiável;
- `reputation_below_threshold`;
- `winner_has_better_reputation` (aparece só na lista);
- `manufacturing_time` (perde para quem tem estoque imediato);
- `shipping_mode`, na ordem ME2 > ME1 > envio próprio > não especificado;
- limite do programa Decola;
- anúncio pausado.

Os exemplos do doc são de Argentina e México, mas o texto está no portal brasileiro.

**Regras complementares** (nota "Como o catálogo e a concorrência funcionam", sem data, pode estar superada) [OFICIAL]:
- O vendedor com "as melhores condições de venda e experiência" é o destaque. Quem clica em "Comprar" compra dele.
- Cada variação e cada opção de venda compete separadamente.
- Ao criar o anúncio de catálogo a partir de um tradicional, os dois sincronizam estoque e condições, e o original pode ficar inativo.
- O ML pode criar o anúncio de catálogo pelo vendedor.

**Clips no catálogo.** Aparece o clipe do ganhador, mas "a gente vai priorizar o clipe da marca" quando a marca sobe vídeo. Fonte: QuOP9KeKnk8, 25/05/2026. [OFICIAL]

**Campanha co-participada de preço competitivo (Smart Price Matching).**
- O ML co-financia a redução para igualar a concorrência externa e diz que isso pode ajudar a "ganhar catálogo, não é uma garantia".
- O aporte só muda sozinho para baixo. As ofertas são recalculadas diariamente.
- Fonte: W1hgC6snin4, 03/06/2026. [OFICIAL]

**Elegibilidade.**
- Só `condition: new`. Há a tag `catalog_listing_eligible`.
- Status possíveis: READY_FOR_OPTIN, ALREADY_OPTED_IN, PRODUCT_INACTIVE, COMPETING.
- Fonte: developers "Elegibilidade", 29/12/2025 (pode estar superada). [OFICIAL]

### 2.5 Título, atributos, descrição, variações

**Título.**
- Limite de 60 caracteres nas categorias consultadas (API, 14/10/2026). [OBS sobre N1]
- O webinar oficial (MFYKfOYs0iE, 03/06/2026) recomenda [OFICIAL]:
  - nome do produto nas 2 primeiras palavras, depois marca, modelo e especificação (cor, material);
  - nada de emoji;
  - a palavra-chave precisa estar no título e pode ser repetida na descrição;
  - variações de grafia ("guarda-chuva" com ou sem hífen) são lidas como iguais;
  - sinônimos regionais (mandioca/macaxeira) exigem escolha do termo mais buscado.
- O título longo (~200 caracteres) visto no líder de Gamepads está numa página de produto de catálogo (/p/). O nome é do catálogo, não um título livre do vendedor (lideres.tsv, 14/10/2026). [OBS]

**Atributos e ficha.**
- A ficha alimenta filtros e qualidade (nota oficial).
- No webinar de Natal, o ML disse que puxa atributos (estilo, formato de uso, instalação) para "segmentar uma campanha, um banner" (-NK3VLYm0q0, 01/06/2026). [OFICIAL]

**Descrição.**
- Até 50.000 caracteres (API, 14/10/2026).
- O ML oferece "Sugerir descrição" por IA. A praticante recomenda preencher atributos, fotos e vídeo antes de usar a sugestão (QANPOYRNZsI, 07/08/2026). [PRÁTICA]
- Segundo a mesma praticante, o editor não aceita bullets nem formatação markdown. [PRÁTICA, não confirmado em N1]

**Variações e kits.**
- O mesmo produto que muda só cor ou tamanho fica num anúncio. Modelos diferentes ficam em anúncios diferentes. Kits (ex.: caneta + 2 balas) são anúncios distintos.
- Kits virtuais podem misturar estoque Full e estoque próprio.
- Fontes: webinar MFYKfOYs0iE [OFICIAL]; nota de duplicados, "desde que isso não implique no aumento de preço" (sem data, pode estar superada) [OFICIAL].
- Divergência: no mesmo webinar aparece a função "anúncio com preço por variação". A regra de preço igual pode estar superada.

### 2.6 Fotos

**Limites técnicos** (developers "Imagens", 24/03/2026) [OFICIAL]:
- até 10 MB;
- recomendado 1200x1200 px;
- máximo de 1920x1920 px e mínimo de 500x500 px;
- zoom ativado acima de 800 px de largura;
- quantidade máxima conforme a categoria (`max_pictures_per_item` = 12 nas categorias consultadas).

**Diagnóstico** (14/07/2025, pode estar superada) [OFICIAL]:
- checa `white_background`, `minimum_size`, `text_logo` e `watermark` conforme a categoria;
- a capa ("thumbnail") tem as regras mais rígidas.

**Moderação** (21/07/2025, pode estar superada) [OFICIAL]: a tag `poor_quality_thumbnail` pode moderar anúncios ativos ou pausados.

**Webinar oficial** (MFYKfOYs0iE) [OFICIAL]:
- capa clara, fundo branco, sem texto nem marca d'água;
- texto na capa "vai realmente atrapalhar o algoritmo de fazer a leitura do seu anúncio";
- fundos ambientados (inclusive os gerados pela IA do ML) a partir da 2ª foto;
- várias fotos e ângulos;
- a frase "não existe limite" de fotos contradiz a API (12). Vale o N1 da API.

### 2.7 Clips / Vídeos

Fonte: webinar oficial QuOP9KeKnk8, 25/05/2026. [OFICIAL]

**Formato.**
- Vertical, de 10 a 60 segundos, com boa luz e som, em MP4/MOV.
- Gratuito e ilimitado por anúncio.
- Cada usuário vê um clipe uma única vez no feed. Por isso, mais clipes por produto significam mais alcance.

**Onde aparece.**
- Feed "Vídeos" e home (formato "rabbit").
- 2ª posição da galeria. A 1ª posição está em teste no Android, com +10 a 15% de conversão.
- Carrossel da Minha Página.
- Tráfego externo pelas contas oficiais (Instagram) e resultados de vídeo do Google.

**Moderação.**
- IA mais revisão manual, em até 48h.
- Vídeo reprovado por engano não deve ser excluído: o caminho é reclamar.

**Flexibilizações.**
- Logo permitido se ocupar menos de 10% do tempo ou menos de 10% da tela.
- Vídeo horizontal adaptado com bordas é aceito.
- O mesmo clipe pode ir para vários anúncios do mesmo produto.
- Um clipe pode valer para todas as variantes.
- Há upload múltiplo e clipe na criação do anúncio.

**Proibido** (lista citada por praticante a partir da regra do ML, 7fkFXNudq0Q, 06/05/2026) [OFICIAL via terceiro]:
- marca d'água;
- dados de contato;
- preços, ofertas, cupons e promoções por tempo limitado;
- sorteios;
- telas do ML;
- comparações sem critério objetivo;
- menores de idade;
- conteúdo de terceiros;
- slideshow de imagens estáticas.

Bebidas alcoólicas exigem a legenda de venda proibida a menores de 18 anos. Produtos de sex shop não podem ter clipe.

**Clips com IA (só no celular).** Gera 3 roteiros a partir da descrição do anúncio, com narração, legenda e música, em cerca de 2 a 5 minutos. Está liberado para colaboradores da conta.

### 2.8 Mercado Ads e qualidade

**Fórmula do leilão** (gestor de Ads do ML, webinar oficial JzejZyVeauE, 21/05/2026) [OFICIAL]:
- vence quem tem o maior "rank" = Adscore × CPC máximo;
- o CPC máximo deriva do ROAS objetivo;
- o Adscore usa título, avaliação, Full, qualidade da foto e posicionamento do produto;
- o Adscore é diferente da nota de qualidade de Métricas e não é exibido.

**Painel.** Mostra impressões "perdidas por qualidade do anúncio" (webinar de Natal, -NK3VLYm0q0). [OFICIAL]

**Recomendação do ML.** Entre 15 e 30 produtos por campanha.

**Exibição duplicada.** O anúncio patrocinado aparece também na posição orgânica. Praticantes chamam isso de "anúncio duplicado" e usam para "blindagem" da 1ª página (Y5e1hvRvGEo, 08/09/2026; qMRuA4FGYfQ, 19/07/2026). [PRÁTICA]

---

## 3. O que os melhores fazem

### 3.1 Consenso (3 ou mais fontes independentes)

- **Cadastro completo antes de investir em tráfego.**
  - Recomendam ficha 100% preenchida, 5 a 8 fotos estratégicas, vídeo e descrição em blocos.
  - Fontes: D21_ErqP09E, ZAa89f0ERE8, tPmQZJBgWVY (Universidade Ecommerce, curso; N7), MFYKfOYs0iE (oficial), QANPOYRNZsI (praticante com tela).
  - Para um anúncio de nível médio, o ML cita "ficha técnica 100% preenchida", "sequência de fotos", variações e vídeos por variação. [PRÁTICA]+[OFICIAL]
- **Sequência de fotos com função definida.** Capa limpa. 2ª foto com benefícios. 3ª respondendo às objeções tiradas das perguntas do anúncio líder. 4ª com itens inclusos. 5ª ambientada. Também usam infográficos e detalhes.
  - Fontes: -lbL_uX9eSA (Margem Club, 11/06/2026, mentoria), tPmQZJBgWVY, XT-4sPZqVEE (8 prompts: capa, ambientada, antes e depois, infográfico técnico, infográfico de benefícios, detalhes, tabela comparativa, embalagem). [PRÁTICA]
- **Pesquisa de palavra-chave no próprio ML:**
  - barra de busca e autocomplete (7AVp0IvEc4g, Avantpro, 22/05/2026);
  - "palavras mais buscadas" no painel e no Assistente (MFYKfOYs0iE, oficial);
  - tendencias.mercadolivre.com.br (HdlFbwdB0Vk, 18/07/2026);
  - "Métricas > Análise de mercado > Tendências por categoria" com top 100 (UFWhBBSAQ8U, 29/07/2026; xEU0AIoVdqg, oficial EnviosCast, 22/09/2026);
  - os 5 primeiros resultados da busca como referência (MFYKfOYs0iE).
  - Tipo: [PRÁTICA]+[OFICIAL]
- **Engenharia reversa do líder:** abrir os 3 a 5 anúncios mais vendidos do mesmo produto e extrair perguntas, reclamações e objeções para fotos e descrição.
  - Fontes: XT-4sPZqVEE (ferramenta AutoVenda, com conflito de interesse), -lbL_uX9eSA, 5OALEDEnI1Q, MFYKfOYs0iE. [PRÁTICA]
- **Clipe próprio gravado com o produto em mãos, e não gerado por IA.**
  - O ML diz que o conteúdo estilo UGC funciona melhor que o institucional.
  - Fontes: QuOP9KeKnk8 (oficial), 7fkFXNudq0Q (Empresa em Ação, 06/05/2026), -lbL_uX9eSA. [OFICIAL]+[PRÁTICA]
- **Monitorar a concorrência no catálogo e reagir com preço e logística.**
  - Fontes: WF333Qri_i8 (Alex Moro com ferramenta Nubimetrics, afiliado), W1hgC6snin4 (oficial: entrar todo dia nas ofertas). [PRÁTICA]+[OFICIAL]
- **Revisar anúncios curva A pelo menos a cada 1 a 2 meses.** Fonte: MFYKfOYs0iE, oficial. [OFICIAL, recomendação]
- **Não mexer em anúncio vencedor.** Se o anúncio parou, avaliar pausar e recriar em vez de reformar tudo. O ML recomenda ver visitas e cliques antes de decidir. Fonte: MFYKfOYs0iE, oficial. [OFICIAL]

### 3.2 Divergências

- **Preço de entrada.**
  - Universidade Ecommerce recomenda o menor preço na largada, como "fase de investimento", e subir aos poucos (ZAa89f0ERE8).
  - Alex Moro diz que o menor preço pode sinalizar produto ruim em categorias que pedem qualidade (TgqKYHoFIXs).
  - No catálogo, ele ensina "precificação dinâmica" e que baixar preço "por pânico" ensina ao algoritmo que o produto vale menos (WF333Qri_i8).
  - Não há N1 sobre "preço baixo deixa sinal permanente". Tipo: [PRÁTICA] × [PRÁTICA]
- **Capa com fundo branco ou ambientada.**
  - O ML recomenda branco, mas admite que é "critério do vendedor" e que há anúncios com capa por IA vendendo bem (MFYKfOYs0iE).
  - A regra rígida é: sem texto na capa e fundo branco onde a categoria exige (diagnóstico de imagens).
- **Ads como alavanca de ranqueamento orgânico.**
  - Alex Moro: "o Ads é para você rankear o teu produto" (TgqKYHoFIXs).
  - Universidade Ecommerce: o Ads garante posição, mas "não garante vendas" (tPmQZJBgWVY).
  - Nenhuma fonte N1 diz que o Ads melhora a posição orgânica. Fica como hipótese (N7).
- **Avaliações recentes pesam mais.** Afirmado por D21_ErqP09E (curso), sem fonte. O N1 só diz que as opiniões entram na experiência de compra.
- **Participar de todas as campanhas oficiais aumenta a relevância.** Afirmado por D21_ErqP09E. O N1 diz apenas que os descontos dão acesso à seção Ofertas (nota de posicionamento).
- **Título com ou sem marca no início.**
  - O ML pede marca no título (MFYKfOYs0iE).
  - O líder em café em grão usa título genérico sem marca no início. Marcas tradicionais usam "marca + formato + peso + torra" (lideres.md, 14/10/2026).
  - Tipo: [OFICIAL] × [OBS]

### 3.3 Testes A/B

- O ML não oferece ferramenta de teste A/B de anúncio nas fontes lidas. Sem evidência.
- Na prática, testam variação de clipe, de capa entre anúncios diferentes e de preço via campanhas.
- O alerta oficial de que trocar título e fotos derruba a performance (MFYKfOYs0iE) torna o A/B sequencial no mesmo anúncio arriscado.
- Nenhuma fonte publicou teste com holdout para fotos ou título. A única métrica de teste com base declarada é a do próprio ML: clipe na 1ª posição deu +10 a 15% de conversão (QuOP9KeKnk8).

---

## 4. Números de referência

| Indicador | Valor | Fonte | Data | Tipo |
|---|---|---|---|---|
| Título máximo | 60 caracteres (5 categorias) | API /categories | 14/10/2026 | [OBS] sobre N1 |
| Título mínimo para a regra de qualidade | 3 palavras | developers /performance | 31/01/2025 (pode estar superada) | [OFICIAL] |
| Fotos máximas | 12 por anúncio; 10 por variação | API /categories | 14/10/2026 | [OBS] sobre N1 |
| Fotos mínimas para a regra de qualidade | 3 | developers /performance | 31/01/2025 (pode estar superada) | [OFICIAL] |
| Tamanho de foto | 1200x1200 recomendado; mín. 500x500; máx. 1920x1920; até 10 MB; zoom >800 px | developers Imagens | 24/03/2026 | [OFICIAL] |
| Descrição máxima | 50.000 caracteres | API /categories | 14/10/2026 | [OBS] sobre N1 |
| Estoque mínimo para a regra de qualidade | 2 unidades | developers /performance | 31/01/2025 (pode estar superada) | [OFICIAL] |
| Score de qualidade | 0 a 100; Básica/Satisfatória/Profissional | developers | 31/01/2025 (pode estar superada) | [OFICIAL] |
| Experiência de compra | Boa 75–100; Mediana 50–74; Ruim ≤30 | Nota Central de Vendedores | sem data (pode estar superada) | [OFICIAL] |
| Janela da experiência | 100 vendas/60 dias; se não, 365 dias; categoria ≥200 vendas | idem | sem data (pode estar superada) | [OFICIAL] |
| Clipe: duração | 10 a 60 s, vertical | webinar oficial | 25/05/2026 | [OFICIAL] |
| Clipe: logo permitido | <10% do tempo ou <10% da tela | webinar oficial | 25/05/2026 | [OFICIAL] |
| Clipe: moderação | até 48h | webinar oficial | 25/05/2026 | [OFICIAL] |
| Clipe: efeito declarado | 3x visitas; 2x vendas | webinar oficial (dado do ML, método não publicado) | 25/05/2026 | [DADO] |
| Clipe: efeito (outro webinar) | 5x visitas; 2x vendas; +143% vendas 30 dias antes/depois; +11% conversão | webinar oficial de Natal (método não publicado) | 01/06/2026 | [DADO] |
| Clipe na 1ª posição | +10 a 15% conversão (teste) | webinar oficial | 25/05/2026 | [DADO] |
| Conversão de quem assiste clipe | ">38%" | webinar oficial (2025, métrica não definida) | 25/05/2026 | [DADO] |
| Consumo de clipes | 5,9 bi views; ~204 mi espectadores; >10 mi horas (América Latina, 2025) | webinar oficial | 25/05/2026 | [DADO] |
| Assistente ML | +47% visitas; +2 p.p. de vendas | webinar oficial (método não publicado) | 03/06/2026 | [DADO] |
| Data dupla 6/6/2025 | vendeu mais que a Black Friday 2024 | webinar oficial | 03/06/2026 | [DADO] |
| Ads: produtos por campanha | 15 a 30 | webinar oficial | 21/05/2026 | [OFICIAL] (recomendação) |
| Conversão "boa" (praticante) | R$19–78,99: 3–6%; R$79–250: 1,5–5%; >R$250: frequentemente <1% | Margem Club -lbL_uX9eSA (mentoria, sem base) | 11/06/2026 | [PRÁTICA], confiança baixa |
| Fotos no top 100 | "média de oito" em algumas categorias | convidado, EnviosCast oficial xEU0AIoVdqg | 22/09/2026 | [PRÁTICA] |
| Café: FULL na 1ª página | 26/40 (grãos), 21/30 (moído), 22/25 (cápsulas) | lideres.md | 14/10/2026 | [OBS] |
| Café: miniaturas nos líderes | 6 a 9 | lideres.md | 14/10/2026 | [OBS] |
| Catálogo Pilão 1kg | 72 vendedores; vencedor revendedor | lideres.md | 14/10/2026 | [OBS] |
| Mensagem proativa pós-venda | 350 caracteres | webinar oficial Ag1UXXB1fec | 25/05/2026 | [OFICIAL] |

---

## 5. Alimentos, perecíveis e marca própria/indústria

- **Logística pesa mais no café.** 26/40, 21/30 e 22/25 dos primeiros resultados de café têm FULL. Os sem FULL no topo são, em geral, cafés especiais de nicho com poucas vendas (lideres.md, 14/10/2026). [OBS]
  - O catálogo oficial lista Full, frete grátis e envio no mesmo dia como boosts (developers, 21/07/2026). [OFICIAL]
- **Catálogo de marca conhecida vira arena de revenda.** Pilão 1kg tinha 72 ofertas e o vencedor era um supermercado revendedor. No Café Italle, quem ganhava era a loja oficial de outra empresa, com a loja oficial da própria Italle mais cara. Nota, opiniões e "vendidos" pertencem ao produto de catálogo, não ao vendedor (lideres.md). [OBS]
  - Para quem tem marca, defender o próprio catálogo exige competir nas mesmas variáveis: preço total, Full, parcelas e reputação.
  - Risco relatado: um catálogo "genérico, sem marca que defendia", foi tomado por concorrentes com preço menor. O relato fala em queda de 30 a 40% do faturamento no ML (Pv0wKI4OOMQ, 30/04/2026). Sem período e sem base, foi rebaixado de [CASE] para [PRÁTICA].
- **Clipe da marca tem prioridade no catálogo.** Quando a marca sobe vídeo, ele substitui o do ganhador (QuOP9KeKnk8). Para a indústria, é uma alavanca de conteúdo que a revenda não controla. [OFICIAL]
- **GTIN/EAN.** O código universal é regra de qualidade ("para estar mais arriba en los resultados de búsqueda", texto do doc em espanhol). Também é requisito citado para o estoque compartilhado, junto com "não ter data de validade" (SFvw5IWL4_Y, 17/06/2026, praticante lendo a regra). Para perecíveis, isso sugere exclusão do estoque compartilhado. [OFICIAL] + [PRÁTICA, não confirmado em N1]
- **Ficha e título no café:**
  - a categoria "Café Moído e em Grão" (MLB247538) usa atributos como "Formato do café", "Formato de venda" e "Quantidade de embalagens" (API domain_discovery, 14/10/2026) [OBS sobre N1];
  - os líderes expõem preço por kg na página, desconto por quantidade (5 un, 10 un, 100 un) e kits como anúncios separados (lideres.md) [OBS];
  - títulos de marca tradicional seguem "marca + formato + peso + torra" [OBS].
- **Fotos de alimentos.** Supermercado e saúde costumam exigir fundo branco na capa (blogs, sem N1 por categoria). O diagnóstico oficial aplica `white_background` "conforme a categoria". A lista exata por categoria não foi achada.
- **Experiência de compra em alimentos.** Produto que chega aberto ou danificado ("POOR_CONDITION", "BROKEN_PRODUCT") aparece como motivo típico no exemplo do doc de experiência de compra (developers, 03/02/2026). Embalagem de transporte entra no ranqueamento por esse canal. [OFICIAL]
- **Bebidas alcoólicas.** O clipe precisa trazer a legenda de proibido para menores de 18 anos (7fkFXNudq0Q, citando regra do ML). [OFICIAL via terceiro]
- **Topo da categoria.** No top 20 de Alimentos e Bebidas só há marcas nacionais muito conhecidas, com preço de supermercado (lideres.md). [OBS]

---

## 6. Erros comuns e mitos

| Afirmação (fonte fraca) | O que dizem as fontes fortes |
|---|---|
| "Quem tem o menor preço ganha o catálogo" (senso comum citado em WF333Qri_i8) | O N1 lista boosts (Full, parcelas, frete grátis, mesmo dia) e motivos de exclusão por reputação e modo de envio (developers, 21/07/2026). Observação: R$141 no Full ganhava de R$139 (WF333Qri_i8). |
| "Vários anúncios iguais aparecem mais" (pergunta de vendedor no webinar) | Duplicados são proibidos e cancelados ou ocultados. Dividem visitas e reputação (nota oficial; MFYKfOYs0iE). |
| "Não há limite de fotos" (webinar oficial MFYKfOYs0iE) | A API da categoria limita a 12 por anúncio e 10 por variação (14/10/2026). Fonte oficial contra fonte oficial: vale a regra técnica. |
| "Envie o clipe apenas uma vez; não pode reutilizar em outros anúncios" (regra citada em 7fkFXNudq0Q, 06/05/2026) | Flexibilizada: o mesmo clipe pode ir para vários anúncios do mesmo produto (QuOP9KeKnk8, 25/05/2026). |
| "O título pode ter 200 caracteres como o do líder" (leitura de lideres.md) | O título do vendedor tem limite de 60. O nome longo é da página de catálogo /p/ (API e OBS). |
| "Avaliações recentes valem mais que muitas avaliações" e "participar de todas as campanhas dá relevância" (D21_ErqP09E, curso com CTA) | Sem N1. O oficial só cita as opiniões dentro da experiência de compra e o acesso à seção Ofertas. |
| "Ads serve para ranquear o orgânico; depois o Ads fica mais barato" (TgqKYHoFIXs, mentoria) | Sem N1 nem teste de pausa ou holdout. O oficial diz que o Adscore usa o posicionamento do produto, ou seja, a relação inversa (JzejZyVeauE). |
| "90% das vendas são na 1ª página" (Avantpro, citado no protocolo) | Número sem base. Não encontrado em N1. |
| Números de clipe "3x visitas, 2x vendas" usados como causalidade | São do próprio ML, sem método. Quem coloca clipe tende a ser o vendedor mais estruturado (viés de seleção). Só o teste de posição (+10 a 15%) tem desenho experimental declarado. |
| "Mexer no anúncio não muda nada" | O ML diz que trocar a estrutura faz o algoritmo ler como anúncio novo e a performance cair (MFYKfOYs0iE). |
| Panfleto pedindo avaliação "não é penalizado" (Margem Club, 11/06/2026, "pode mudar amanhã") | Não confirmado em N1. Levar o cliente para fora do ML (WhatsApp, QR code) é penalizável (XT-4sPZqVEE; -lbL_uX9eSA). |

**Erros operacionais citados com frequência:**
- copiar título, fotos e descrição do fornecedor (QANPOYRNZsI, D21_ErqP09E);
- categoria errada (nota oficial);
- variação curva A sem estoque, que derruba a conversão e o ranqueamento (-lbL_uX9eSA);
- estoque de Full concentrado num só CD, que tira o "chega amanhã" de outras regiões (-lbL_uX9eSA);
- foto gerada por IA infiel ao produto, que gera devolução e afeta a experiência (XT-4sPZqVEE);
- atributo errado vindo do fornecedor, como USB-A no lugar de USB-C (QANPOYRNZsI).

---

## 7. Revenda/importação x indústria/marca própria

**[REVENDA] (revenda, dropshipping, importação):**
- **Catálogo.** O revendedor disputa a buy box de catálogos existentes e não controla título, fotos nem opiniões, que são do catálogo (lideres.md; nota oficial de catálogo).
  - A disputa é de preço total, boosts logísticos e reputação. `price_to_win` e a campanha de preço competitivo são as ferramentas oficiais.
  - O "manufacturing time" impede ganhar quando o vencedor tem estoque imediato (developers).
- **Dropshipping.** O prazo de disponibilidade e a falta de Full reduzem o score de qualidade (STOCK_AVAILABILITY_TIME) e tiram boosts.
  - Descrição e atributos do fornecedor costumam ter erros, que viram reclamação e pioram a experiência de compra (QANPOYRNZsI, praticante de dropshipping que fatura cerca de R$30 mil desde maio).
- **Marca própria de importado.** Usa títulos de catálogo longos com compatibilidades e "de/por" agressivo. Exemplos: Redfin e Woosh (lideres.md). [OBS]

**[MARCA] (indústria, marca própria):**
- Pode criar e defender o próprio catálogo, ter clipe priorizado e loja oficial. Segundo praticante, a loja oficial exige marca registrada, sem classe específica obrigatória (Pv0wKI4OOMQ). [PRÁTICA]
- Controla a ficha técnica e o GTIN, o que conta na qualidade.
- Sem defesa de preço, o catálogo próprio pode ser ganho por revendedores (lideres.md: Italle e Pilão).
- Os padrões de líder de marca em café estão na seção 5: linha completa de formatos e tamanhos, várias posições na busca, loja oficial Platinum e FULL.

**[AMBOS]:**
- experiência de compra por anúncio;
- duplicados proibidos;
- limites de título e fotos;
- regras de clipe;
- funil impressão → clique → conversão.

---

## 8. Tabela de afirmações

| id | Afirmação | Tipo | Fonte | Data | Confiança |
|---|---|---|---|---|---|
| A1 | O ML não publica pesos; lista ficha completa, categoria certa, fotos nos requisitos, catálogo, preço, reputação e experiência como fatores de posição | [OFICIAL] | vendedores.mercadolivre.com.br/nota/como-posicionar-seus-produtos-nos-resultados-de-busca-nuevo | sem data (pode estar superada) | alta |
| A2 | Anúncios de catálogo sempre aparecem primeiro nos resultados | [OFICIAL] | idem A1 | sem data (pode estar superada) | média |
| A3 | Reputação vermelha tem menor exposição; despachar em menos de 24h | [OFICIAL] | idem A1 | sem data (pode estar superada) | alta |
| A4 | O vencedor do catálogo é decidido por algoritmo: preço, parcelas sem juros, Full, frete grátis, mesmo dia | [OFICIAL] | developers.mercadolivre.com.br/pt_br/concorrencia-em-catalogo | 21/07/2026 | alta |
| A5 | O vencedor leva todas as vendas e visibilidade (visit_share maximum); quem perde fica com minimum | [OFICIAL] | idem A4 | 21/07/2026 | alta |
| A6 | Não compete: reputação abaixo do limite, vencedor com reputação melhor, manufacturing time, modo de envio inferior (ME2>ME1>próprio), limite do Decola | [OFICIAL] | idem A4 | 21/07/2026 | alta |
| A7 | Cada variação e opção de venda compete separadamente no catálogo; o anúncio original pode ficar inativo | [OFICIAL] | vendedores.mercadolivre.com.br/nota/com-o-catalogo-o-primeiro-lugar-dos-resultados-de-busca-pode-ser-seu | sem data (pode estar superada) | média |
| A8 | Experiência de compra: Boa 75–100, Mediana 50–74, Ruim ≤30; Mediana perde exposição e risco de pausa; Ruim, risco de cancelamento definitivo | [OFICIAL] | vendedores.mercadolivre.com.br/nota/como-proporcionar-a-melhor-experiencia-de-compra | sem data (pode estar superada) | alta (dupla: Hunter HUB 12/10/2026 repete) |
| A9 | Experiência usa 100 vendas/60 dias, ou 365 dias; abaixo de 100 vendas completa com a categoria (≥200 vendas) | [OFICIAL] | idem A8 | sem data (pode estar superada) | média (diverge do doc de 180 dias) |
| A10 | Título e descrição inconsistentes, perguntas, opiniões e mensagens entram na experiência de compra | [OFICIAL] | idem A8 | sem data (pode estar superada) | alta |
| A11 | Decola e Benefício de Reputação protegem anúncios da perda de exposição por experiência ruim | [OFICIAL] | idem A8; developers experiência de compra | 03/02/2026 | alta |
| A12 | Score de qualidade 0–100; níveis Básica/Satisfatória/Profissional; melhora a exposição | [OFICIAL] | developers.mercadolivre.com.br/pt_br/qualidade-das-publicacoes | 31/01/2025 (pode estar superada) | alta |
| A13 | Regras de qualidade: GTIN, características principais, ≥3 fotos, título ≥3 palavras, frete grátis, parcelas, ≥2 unidades, Mercado Envios | [OFICIAL] | idem A12 | 31/01/2025 (pode estar superada) | média |
| A14 | Título máximo de 60 caracteres (café, gamepads, fones, camisetas, azeite) | [OBS] sobre N1 | api.mercadolibre.com/categories/MLB247538 etc. | 14/10/2026 | alta |
| A15 | Máximo de 12 fotos por anúncio e 10 por variação; descrição até 50.000 caracteres | [OBS] sobre N1 | idem A14 | 14/10/2026 | alta |
| A16 | Foto: 1200x1200 recomendado; mín. 500x500; máx. 1920; 10 MB; zoom >800 px | [OFICIAL] | developers.mercadolivre.com.br/pt_br/trabalhar-com-imagens | 24/03/2026 | alta |
| A17 | O diagnóstico de imagem checa fundo branco, tamanho mínimo, texto/logo e marca d'água conforme a categoria; a capa tem regras mais rígidas | [OFICIAL] | developers.mercadolivre.com.br/pt_br/diagnostico-de-imagens | 14/07/2025 (pode estar superada) | alta |
| A18 | Capa sem texto; texto na capa atrapalha a leitura do algoritmo; ambientada a partir da 2ª foto | [OFICIAL] | YouTube MFYKfOYs0iE | 03/06/2026 | média |
| A19 | Título até 60 caracteres, produto nas primeiras palavras, marca e modelo, sem emoji; palavra-chave obrigatória no título | [OFICIAL] | MFYKfOYs0iE | 03/06/2026 | alta (A14 confirma o limite) |
| A20 | Trocar título e fotos de um anúncio que vende derruba a performance ("lê como novo anúncio") | [OFICIAL] | MFYKfOYs0iE | 03/06/2026 | média |
| A21 | Duplicados não são permitidos; cancelados ou ocultados mantendo o de melhor visibilidade; usar variações | [OFICIAL] | vendedores.mercadolivre.com.br/nota/anuncios-duplicados-o-que-sao-e-como-evita-los | sem data (pode estar superada) | alta (MFYKfOYs0iE concorda) |
| A22 | O mesmo produto pode ter mais de um anúncio se mudar forma de envio ou de pagamento | [OFICIAL via terceiro] | mercadolivre.com.br/ajuda/An-ncios-duplicados_2518 (via resumo de busca) | sem data (pode estar superada) | média |
| A23 | Clipe: 10–60 s vertical; ilimitado; cada usuário o vê uma vez no feed; moderação de até 48h | [OFICIAL] | QuOP9KeKnk8 | 25/05/2026 | alta |
| A24 | Clipe é critério de qualidade do anúncio e melhora o ranqueamento | [OFICIAL] | QuOP9KeKnk8 | 25/05/2026 | média |
| A25 | Anúncio com clipe: 3x visitas e 2x vendas | [DADO] (ML, método não publicado) | QuOP9KeKnk8 | 25/05/2026 | baixa (viés de seleção) |
| A26 | Clipe na 1ª posição da galeria: +10–15% de conversão em teste | [DADO] | QuOP9KeKnk8 | 25/05/2026 | média |
| A27 | Logo no clipe <10% do tempo ou da tela; mesmo clipe permitido em vários anúncios do mesmo produto | [OFICIAL] | QuOP9KeKnk8 | 25/05/2026 | alta |
| A28 | No catálogo, o clipe da marca é priorizado sobre o do ganhador | [OFICIAL] | QuOP9KeKnk8 | 25/05/2026 | média |
| A29 | Clipe não pode ter preço, cupom, contato, tela do ML, slideshow estático nem conteúdo de terceiros | [OFICIAL via terceiro] | 7fkFXNudq0Q | 06/05/2026 | média |
| A30 | Leilão de Ads: rank = Adscore × CPC máximo (derivado do ROAS objetivo); Adscore usa título, avaliação, Full, foto e posicionamento | [OFICIAL] | JzejZyVeauE | 21/05/2026 | média |
| A31 | A campanha de preço competitivo co-financiada pode ajudar a ganhar catálogo, sem garantia; ofertas recalculadas diariamente | [OFICIAL] | W1hgC6snin4 | 03/06/2026 | média |
| A32 | Atributos (estilo, uso, instalação) são usados pelo ML para segmentar campanhas e banners | [OFICIAL] | -NK3VLYm0q0 | 01/06/2026 | média |
| A33 | O ML aplica mudanças por IA no anúncio com base nas perguntas recebidas | [OFICIAL] | nota experiência de compra | sem data (pode estar superada) | média |
| A34 | API de busca e de tendências fechada sem token (403/401) | [OBS] | api.mercadolibre.com/sites/MLB/search; /trends/MLB | 14/10/2026 | alta |
| A35 | Café: 26/40, 21/30 e 22/25 dos primeiros resultados com FULL | [OBS] | observacao/lideres.md | 14/10/2026 | média (1 CEP, MG) |
| A36 | Catálogo Pilão 1kg com 72 vendedores e vencedor revendedor; nota e vendidos pertencem ao catálogo | [OBS] | lideres.md (MLB35944622) | 14/10/2026 | média |
| A37 | O líder em café em grão usa título genérico, sem marca no início | [OBS] | lideres.md (MLB26184226) | 14/10/2026 | média |
| A38 | Funil: impressão baixa → relevância; CTR baixo → capa, preço, título; visita sem venda → descrição, preço total, confiança | [PRÁTICA] | tPmQZJBgWVY; 5OALEDEnI1Q | 13/05/2026; 08/06/2026 | média |
| A39 | Conversão "boa": 3–6% (R$19–78,99); 1,5–5% (R$79–250) | [PRÁTICA] | -lbL_uX9eSA | 11/06/2026 | baixa |
| A40 | R$141 no Full ganhava o catálogo de R$139 sem melhor logística | [PRÁTICA com tela] | WF333Qri_i8 | 24/06/2026 | média (N1 A4 coerente) |
| A41 | Fase de entrada com preço baixo e alta gradual para ranquear | [PRÁTICA] | ZAa89f0ERE8 | 08/07/2026 | baixa (curso, N7) |
| A42 | Ads é para ranquear o orgânico | [PRÁTICA] | TgqKYHoFIXs | 06/07/2026 | baixa (mentoria, sem teste) |
| A43 | Catálogo genérico sem marca tomado por concorrentes: −30 a 40% de faturamento | [PRÁTICA] (rebaixado de CASE) | Pv0wKI4OOMQ | 30/04/2026 | baixa |
| A44 | O estoque compartilhado exige GTIN impresso, catálogo e produto sem data de validade | [PRÁTICA] lendo regra | SFvw5IWL4_Y | 17/06/2026 | baixa (sem N1) |
| A45 | Amazon (Brasil): Conteúdo A+ básico até +8% e premium até +20% de vendas; Brand Analytics mostra tendências de busca e compra | [OFICIAL] | venda.amazon.com.br/brand-registry | sem data (pode estar superada) | baixa (dado interno, sem método) |

---

## 9. Lacunas

**Amazon e Shopee.** A busca foi encerrada por limite de cota e as ajudas oficiais exigem login ou carregam por JavaScript. Por isso, ficaram sem evidência N1 nesta nota:
- critérios da Oferta em Destaque (Buy Box);
- listing quality e supressão;
- Brand Analytics/SQP em detalhe;
- ordenação da busca e violações da Shopee.

Única exceção é A45. Esses pontos devem vir das frentes específicas ou de nova coleta.

**ML:**
- **Pesos do ranqueamento:** nenhuma fonte, oficial ou de ferramenta, publica fórmula ou peso.
- **Tempo para ganhar posição:** sem fonte. A Hunter HUB diz que o ML "não informa prazo".
- **Teste A/B:** não há ferramenta oficial de A/B de anúncio nem estudo público com holdout de título ou foto.
- **Efeito causal de clipes, avaliações e respostas rápidas:** só dados agregados do ML sem método. O efeito da velocidade de resposta a perguntas no ranqueamento não tem N1, só a inclusão de "perguntas e respostas" na experiência de compra.
- **Avaliações dentro das regras:** não foi achada página oficial sobre incentivo a avaliações (cartão na embalagem, brinde). A prática de pedir avaliação por cartão é afirmada por um praticante e não verificada.
- **Fotos por categoria:** não foi encontrada lista N1 de quais categorias exigem fundo branco na capa (Supermercado/Alimentos).
- **Preço por variação:** a regra de variações "sem aumento de preço" (nota sem data) diverge da existência de "preço por variação" citada no webinar.
- **Datas:** as notas da Central de Vendedores não exibem data, o que impede confirmar a vigência. Isso vale em especial para as faixas de experiência de compra e para a regra de catálogo "sempre primeiro".
- **Benchmarks de conversão por categoria no Brasil:** só o painel "Análise de mercado/Concorrência" de cada vendedor. Sem dado público. O número de praticante (A39) não tem base.
- **Peso real do Full contra preço:** sem fonte quantitativa.


---

## 10. Verificação (2026-10-14)

Método: leitura direta das páginas oficiais (developers.mercadolivre.com.br, Central de aprendizagem de vendedores, API pública api.mercadolibre.com) em 14/10/2026, tentando refutar cada afirmação contra o texto atual. Não foi possível ver os vídeos dos webinars nem abrir a Central de ajuda (carrega por JavaScript); a cota de busca na web esgotou, então não houve busca por fonte adicional. Todas as fontes da tabela são [OFICIAL].

| id | veredito | fonte oficial (URL) | observação |
|---|---|---|---|
| A4 | CONFIRMADA | https://developers.mercadolivre.com.br/pt_br/concorrencia-em-catalogo (atualizada em 21/07/2026) | O algoritmo decide com base na publicação e no vendedor: preço, parcelamento sem juros, Full, frete grátis e envio no mesmo dia. Winning = visit_share maximum; competing = minimum. Ressalva: existe um terceiro estado, sharing_first_place, com visit_share medium (primeiro lugar compartilhado). "Leva todas as vendas" vale quando não há compartilhamento (competitors_sharing_first_place = 0). O vencedor pode valer só para o público geral, não para segmentos minoritários (ex.: quem não aproveita envio no mesmo dia). |
| A6 | CONFIRMADA | https://developers.mercadolivre.com.br/pt_br/concorrencia-em-catalogo (21/07/2026) | Todos os motivos citados constam no campo reason de price_to_win: reputation_below_threshold, winner_has_better_reputation, manufacturing_time, shipping_mode (ME2 > ME1 > Custom Shipping > Not Specified), newbie_program_seller (limite do programa de dosagem de decolagem), item_paused. Lista incompleta na nota: faltam non_trusted_seller, item_not_opted_in e os estados temporários (temporarily_winning/competing_manufacturing_time e ..._best_reputation_available), em que o vendedor sem reputação verde ou com manufacturing time ganha temporariamente se não houver concorrente melhor. |
| A8 | CONFIRMADA (com ressalvas) | https://vendedores.mercadolivre.com.br/nota/como-proporcionar-a-melhor-experiencia-de-compra (sem data; rodapé 2026, página ativa) | Faixas e consequências batem: Boa 75-100, Mediana 50-74, Ruim 30 ou menos; abaixo de 100 pode começar a perder exposição; mediana perde exposição e pode ser pausada; ruim tem pouca exposição e pode ser cancelada; anúncio cancelado não se recupera. Ressalvas: a faixa 31-49 não está definida na página; vendedores com Benefício de reputação ou Programa Decola ativo não perdem exposição nem são pausados/cancelados por experiência ruim ou mediana. Página sem data: pode estar superada. |
| A9 | CONFIRMADA (divergência persiste) | https://vendedores.mercadolivre.com.br/nota/como-proporcionar-a-melhor-experiencia-de-compra (sem data); https://developers.mercadolivre.com.br/pt_br/experiencia-de-compra (03/02/2026) | A Central descreve: 100 vendas em 60 dias usa esse período, senão o último ano; com menos de 100 vendas completa com outros anúncios da mesma categoria, que precisam somar 200 vendas, senão o anúncio fica sem experiência de compra. O fluxograma da própria página é mais permissivo que o texto: usa 60 dias se o anúncio tem 100 vendas OU a categoria soma 200 em 60 dias; senão 365 dias. O doc developers (03/02/2026) cita 180 dias de vendas e problemas exibidos ao vendedor; a divergência continua sem explicação oficial (pode ser janela de exibição, não de cálculo; não confirmado). |
| A2 | CONFIRMADA (com ressalva) | https://vendedores.mercadolivre.com.br/nota/como-posicionar-seus-produtos-nos-resultados-de-busca-nuevo (sem data; rodapé 2026, página ativa) | O texto diz que anúncios do catálogo sempre aparecem primeiro nos resultados. É frase de dica, sem critério técnico. Não concilia com A4: na página de produto só o vencedor leva a visibilidade máxima e os demais ficam listados (visit_share minimum). Sem data: pode estar superada; não tratar como regra mecânica. |
| A13 | CONFIRMADA (pode estar superada) | https://developers.mercadolivre.com.br/pt_br/qualidade-das-publicacoes (31/01/2025) | Níveis MLB: Básica, Satisfatória, Profissional; score 0-100. Regras vistas no exemplo da API /performance: GTIN, características principais e obrigatórias, mínimo de 3 fotos, título com pelo menos 3 palavras, frete grátis, parcelas ao mesmo preço, 2 ou mais unidades de estoque, Mercado Envios, tempo de disponibilidade do estoque. Modo WARNING = problema que reduz o score até ser resolvido; OPPORTUNITY = oportunidade. A página é de janeiro de 2025 (mais de 6 meses) e o exemplo é de outro site (MLA); a lista pode variar por categoria. A nota não cita o tempo de disponibilidade (manufacturing time), que também pontua. |
| A14 | CONFIRMADA | https://api.mercadolibre.com/categories/{id} (API pública, consultada em 14/10/2026) | Reconferido em Alimentos e Bebidas (MLB1403), Celulares (MLB1055), Televisores (MLB1002) e Calçados, Roupas e Bolsas (MLB1430): max_title_length 60, max_pictures_per_item 12, max_pictures_per_item_var 10, max_description_length 50.000. O limite vem das settings da categoria e pode variar; conferir por categoria antes de assumir. |
| A16 | CONFIRMADA | https://developers.mercadolivre.com.br/pt_br/trabalhar-com-imagens (24/03/2026); https://developers.mercadolivre.com.br/pt_br/diagnostico-de-imagens (14/07/2025) | Recomendado 1200x1200; máximo aceito 1920x1920; mínimo 500x500; até 10 MB; widget de zoom quando a largura passa de 800 px; formatos JPG, JPEG e PNG; a imagem deve ocupar 95% do espaço. O diagnóstico checa white_background, minimum_size, text_logo e watermark conforme a categoria; sem categoria válida, só avalia o tamanho mínimo. A lista de categorias que exigem fundo branco continua não publicada nessas páginas. |
| A21 | CONFIRMADA (parte final sem fonte) | https://vendedores.mercadolivre.com.br/nota/anuncios-duplicados-o-que-sao-e-como-evita-los (sem data; rodapé 2026) | Duplicado = mesmo produto com as mesmas condições de venda; não é permitido e é cancelado automaticamente por descumprir as Políticas de Cadastro; a mesma página diz também que o ML oculta o duplicado e deixa ativo o de melhor visibilidade (dois tratamentos no mesmo texto). Cor, tamanho e material devem ser variações em um só anúncio, desde que não impliquem aumento de preço. Ao criar via "Anunciar semelhante" ou "Vender um igual", o ML pede para mudar as condições de venda. NÃO verificado: a ajuda 2518 (um anúncio a mais quando muda envio ou pagamento) carrega por JavaScript e não pôde ser lida. |
| A23 | SEM FONTE OFICIAL (escrita) | nenhuma página escrita localizada; webinar YouTube QuOP9KeKnk8 não reverificado | Não foi achada página oficial (developers, Central de vendedores ou ajuda) com as especificações de Clips: duração, moderação em 48h, regra de logo, critério de qualidade. Os endereços tentados retornaram 404 ou página vazia. Dados do webinar não foram refutados nem confirmados; é fala em vídeo de 25/05/2026. |
| A30 | SEM FONTE OFICIAL (escrita) | https://developers.mercadolivre.com.br/pt_br/product-ads-para-catalogo-e-user-products-leitura (parcial); webinar JzejZyVeauE não reverificado | A documentação escrita só confirma que o ROAS objetivo (roas_target) substituiu o ACOS objetivo como indicador padrão (ACOS = 1/ROAS x 100) e que há CPC. Em nenhuma página lida aparecem a fórmula rank = Adscore x CPC máximo, os fatores do Adscore nem a recomendação de 15 a 30 produtos por campanha. Depende só da fala do gestor de Ads no webinar de 21/05/2026. |
| A20 | SEM FONTE OFICIAL (escrita) | nenhuma; webinar MFYKfOYs0iE não reverificado | Nenhuma página oficial lida diz que alterar título, fotos ou estrutura faz o algoritmo tratar o anúncio como novo. A doc developers de imagens só avisa que, ao substituir uma foto, é preciso usar novo nome de source para a imagem atualizar. A página de experiência de compra até recomenda melhorar título, fotos e ficha técnica quando o anúncio perdeu exposição, o que não sustenta nem refuta A20. Tratar como [PRÁTICA] ou fala de webinar, sem regra publicada. |

Resumo: 9 confirmadas (A4, A6, A8, A9, A2, A13, A14, A16, A21; várias com ressalvas relevantes), 0 contestadas, 3 sem fonte oficial escrita (A23, A30, A20).
