# Amazon: ranqueamento e construção do anúncio (notas do analista)

Frente: ranqueamento-anuncio · Plataforma: Amazon Brasil (com referências da Amazon global quando a mecânica é a mesma) · Data da nota: 2026-10-14 · Pesquisa neutra: estuda como os melhores operam, sem recomendar nada a empresa específica.

**Como ler.** Toda afirmação leva tipo ([OFICIAL], [OFICIAL via terceiro], [PRÁTICA], [CASE], [DADO], [OBS]), fonte (URL ou id de vídeo do YouTube), data e confiança (A, B ou C). Para achar um vídeo, use `youtube.com/watch?v=<id>`. Regra de plataforma com data anterior a 2026-04-14, ou sem data, leva "(pode estar superada)". [REVENDA] marca o que vale para revenda, importação e genérico. [MARCA] marca o que vale para indústria e marca própria.

**Limites desta rodada.**
- A busca na web atingiu a cota da sessão (200 buscas por turno, divididas entre todos os agentes). Por isso as páginas oficiais foram lidas por URL direta.
- A ajuda do Seller Central Brasil (`sellercentral.amazon.com.br/help/...`) exige login e redireciona para a página inicial. Nenhuma página de ajuda brasileira pôde ser lida.
- A camada oficial brasileira vem de quatro fontes: webinars oficiais do canal "Venda com a Amazon Brasil" (N1 em vídeo), `venda.amazon.com.br`, `advertising.amazon.com/pt-br` e páginas americanas de `sell.amazon.com`. Estas últimas cobrem a mecânica global e foram anotadas como EUA.
- Pedidos embutidos nos vídeos foram ignorados e anotados como sinal fraco: "clica aqui", cupom de ferramenta, link de afiliado, imersão paga.

---

## 1. Resumo executivo

1. **A Amazon não publica fórmula de ranqueamento.** A página oficial de SEO cita, sem pesos, estes fatores: palavra-chave e relevância, preço, qualidade do anúncio, saúde da conta, Ads e vendas (BSR em tempo real). Diz que preço competitivo pode fazer a oferta subir "organicamente" na busca. Fonte: [OFICIAL] sell.amazon.com/blog/amazon-seo, EUA, 2025-09-03 (pode estar superada). Confiança B.
2. **Praticantes brasileiros convergem numa regra empírica.** Quem converte mais em menos tempo sobe no orgânico. Venda feita por Ads alimenta o orgânico. Fontes: [PRÁTICA] 9Hlvkfh1Eow (2026-07-21), VK7jalYzwxc (2026-08-03), 78sSkRh2crI (2026-08-18). Confiança B, por serem três N6/N7 concordantes. Ninguém mostra teste de causalidade.
3. **A busca é ordenada por um conjunto de modelos de aprendizado de máquina por categoria, e não por uma fórmula única.** Fonte: [DADO] Sorokina e Cantú-Paz, Amazon Science, SIGIR 2016 (amazon.science/publications/amazon-search-the-joy-of-ranking-products). Confiança B. É antigo, mas serve como princípio.
4. **Sem oferta em destaque (Buy Box) não há Produtos Patrocinados.** O produto precisa se qualificar para a oferta em destaque e ter estoque para ser anunciado. Fonte: [OFICIAL] advertising.amazon.com/pt-br/solutions/products/sponsored-products, BR, sem data na página (estatísticas de jun/2026). Confiança B.
5. **Oferta em destaque não é só preço.** Pesam prazo e custo de entrega, métricas de saúde da conta, preço frente a outros marketplaces e região do comprador. A logística da Amazon (FBA, DBA, FBA Onsite) ajuda. Fonte: [OFICIAL] webinar nDtHI8fUEAA, 2026-08-20. Confiança A, com confirmação prática em GBnC2vqmRQo: oferta 10% a 20% mais barata perdendo a Buy Box.
6. **O preço Pix entra na disputa desde 30/09/2026.** No plano "Amazon Mais Vantagens" (5% de desconto Pix custeado pela Amazon), a oferta em destaque considera o preço com Pix. Os planos criam uma "segunda Buy Box" para parcelamento sem juros. A taxa vai de 1,5% para 2,5% em 31/10/2026, para itens de R$40 a R$10.000. Fonte: [OFICIAL] webinar H0ab_x1YIBY, 2026-10-14. Confiança B.
7. **O conteúdo da página tem dono, nesta ordem:** dono da marca registrada, depois o sistema interno (cruza GS1 e outras fontes), depois a maioria dos vendedores. O revendedor que entra no catálogo não troca título nem foto. Fontes: [OFICIAL] nDtHI8fUEAA (2026-08-20) e 7ILvtU6GcPo (2026-09-11). Confiança A.
8. **Anúncio com índice de qualidade alto, segundo a Amazon Brasil:** "quatro vezes mais visitas" e cerca de 36% mais vendas. A pesquisa citada não tem metodologia. Fonte: [OFICIAL] nDtHI8fUEAA, 2026-08-20. Confiança C pelo número, B pela direção.
9. **Título de 75 caracteres no Brasil.** Segundo praticante que mostra o Seller News na tela, a partir de 27/07/2026 títulos acima de 75 caracteres deixam de ser aceitos. A Amazon reescreve por IA o que não for ajustado, sem pausar o anúncio. A página americana fala em limite de 200 e recomenda até 60. Fontes: [OFICIAL via terceiro] cNn3iConWSw (2026-07-23); [OFICIAL] sell.amazon.com/blog/amazon-seo. Confiança C. É a regra que mais precisa de checagem no Seller Central BR.
10. **Avaliações movem conversão, não ranqueamento declarado.**
    - A Amazon (EUA) afirma que cinco avaliações dão cerca de 270% a mais de conversão do que zero, e que nota entre 4,2 e 4,5 converte melhor que 5,0. Fonte: [OFICIAL] sell.amazon.com/blog/customer-reviews-social-proof, 2026-08-18. Confiança B.
    - É proibido tentar influenciar notas e avaliações. Fonte: [OFICIAL] sell.amazon.com/tools/customer-reviews.
11. **Vine (EUA): até 30 unidades, para produtos com menos de 30 avaliações.**
    - Custo por produto pai: grátis até 2 unidades, US$75 de 3 a 10, US$200 de 11 a 30.
    - A Amazon declara "média de 30%" a mais de vendas, com dado interno.
    - Recomenda estoque no CD três semanas antes do lançamento.
    - Fonte: [OFICIAL] sell.amazon.com/tools/vine, sem data (pode estar superada). Confiança B. Taxas e disponibilidade no Brasil não foram confirmadas.
12. **Teste A/B oficial: "Gerenciar seus experimentos".** Exige Brand Registry e tráfego suficiente. Testa título, imagem, bullets, descrição e A+. Leva no mínimo cerca de 4 semanas; a Amazon recomenda 8 a 10 semanas em duração fixa e declara "até 20%" de ganho. Fonte: [OFICIAL] sell.amazon.com/tools/manage-your-experiments, sem data. Confiança B.
13. **Conteúdo A+ e loja oficial.** A Amazon declara até 8% de vendas com A+ básico e até 20% com A+ Premium. A Brand Store é gratuita. Clientes que visitam a loja compram com frequência 53,9% maior e ticket 71,3% maior. Tudo vem de "dados internos" de ago/2024, sem método. Fonte: [OFICIAL] venda.amazon.com.br/brand-registry. Confiança C nos números.
14. **Ruptura derruba relevância, e recuperar a posição é difícil.** A Amazon orienta oferta híbrida (FBA mais DBA ou envio próprio) e não baixar preço "na mão", e sim por oferta ou cupom, para manter histórico de preço saudável. O "preço cortado" das ofertas é a mediana do preço de venda dos últimos 90 dias. Fontes: [OFICIAL] q0-Y5gG6Q2w (2026-09-15) e K7a4jlTP9ME (2026-09-04); [PRÁTICA] VH7Q5FddoRY (Smollan, 2026-08-19). Confiança A.
15. **A IA de compras da Amazon (Alexa for Shopping, ex-Rufus) já é uma "terceira prateleira".** Num estudo nos EUA, 63,9% dos produtos recomendados estavam fora do top 10 orgânico e 40,9% nem apareciam na página de busca. Fonte: [DADO] marketplacepulse.com/articles/amazons-ai-doesnt-read-the-rankings, 2026-07-16 (estudo de fornecedor, 1.963 consultas, maio e junho de 2026, uma conta). Confiança C.

---

## 2. Como funciona (mecânica e regras oficiais, com data)

### 2.1 Catálogo: um ASIN por produto, ofertas disputando

- **Um ASIN por produto.** Todo produto tem um código interno único (ASIN). Produto com EAN já cadastrado recebe ofertas de vários vendedores no mesmo ASIN ("dar match"), que disputam a oferta em destaque. Produto genérico sem marca pode ter mais de um ASIN. Produto com marca e EAN criado de novo "em algum momento vai cair" e "impacta sua conta". Fontes: [OFICIAL] yutQ_7zR4Eo (2026-10-02); [PRÁTICA] 02Bn3HyAYqk (2026-07-30).
- **Cada EAN se vincula a um único ASIN**, inclusive em variações. Fonte: [OFICIAL] nDtHI8fUEAA.
- **SKU não se altera e não se reutiliza**, mesmo com o item inativo. Reusar um SKU em outro produto sobrescreve o anúncio. Fontes: [OFICIAL] nDtHI8fUEAA e yutQ_7zR4Eo.
- **Mesmo ASIN, duas ofertas próprias.** O vendedor pode ter um SKU em FBA e outro em DBA ou envio próprio no mesmo ASIN. As duas ofertas disputam entre si, e a DBA assume quando o FBA zera. Fonte: [PRÁTICA] 02Bn3HyAYqk, com tela.

### 2.2 Precedência do conteúdo da página

Quem preenche a página, segundo a Amazon Brasil:
1. o dono da marca;
2. o sistema interno, quando os vendedores divergem (cruza GS1 e sites);
3. a maioria dos vendedores.

O dono da marca registrada "sempre" tem prioridade de edição. Se um revendedor cadastrou o produto com outra grafia de marca, o caminho é denúncia no portal do Brand Registry. Fontes: [OFICIAL] nDtHI8fUEAA (2026-08-20) e 7ILvtU6GcPo (2026-09-11). Confiança A.

### 2.3 Oferta em destaque (Buy Box)

**O que a Amazon Brasil declara (webinar nDtHI8fUEAA, 2026-08-20; H0ab_x1YIBY, 2026-10-14):**
- **Critérios não abertos.** Nem o time interno abre "100%" dos critérios exatos.
- **Fatores citados:**
  - preço ao consumidor;
  - prazo de entrega e valor do frete;
  - métricas de saúde da conta, que podem fazer perder a Buy Box mesmo quando o vendedor está sozinho no ASIN;
  - preço frente a marketplaces externos;
  - região: um concorrente pode ganhar na Bahia por ter frete melhor lá;
  - qualidade do cadastro, como fator auxiliar.
- **Logística.** FBA dá "a mesma experiência" de quando a própria Amazon vende e ajuda a ganhar.
- **Plano Mais Vantagens.** Dá "melhor qualificação" para a oferta em destaque, e o preço considerado é o preço com Pix. Exemplo da Amazon: produto de R$100 aparece a R$95 na Buy Box, mas o repasse é calculado sobre R$100.
- **Buy Box secundária.** Quando a oferta vencedora só parcela com juros, aparece uma Buy Box secundária para quem está em um dos planos de parcelamento sem juros.
- **Pagamentos e tráfego** (dados internos, sem método):
  - 55% dos clientes pagam parcelado e 20% pagam com Pix;
  - 40% dos clientes chegam às páginas via Google Shopping, que mostra o preço Pix.

**Ligação com Ads.** Produtos Patrocinados exigem que o item se qualifique para a oferta em destaque e esteja em estoque. Fonte: [OFICIAL] advertising.amazon.com/pt-br. Na prática, quem perde a Buy Box perde também o anúncio patrocinado daquele ASIN.

### 2.4 Busca orgânica e paga

- **Fatores oficiais (EUA).** Relevância por palavra-chave (título, bullets, descrição, campos de backend), preço, qualidade do anúncio, saúde da conta, Ads e BSR. Fonte: [OFICIAL] sell.amazon.com/blog/amazon-seo, 2025-09-03 (pode estar superada).
- **Leilão de Ads.** Combina o lance com a relevância do anúncio. O lance dinâmico pode subir até 100%. A Amazon recomenda campanha automática por cerca de um mês antes da manual, negativar termos após cerca de 14 dias e não pôr data de término, porque a campanha "pode perder histórico". Fonte: [OFICIAL] 06XpeVMN7ek, 2026-08-17.
- **Aprendizado do algoritmo.** Cada campanha nova ou alterada leva de uma a duas semanas para o algoritmo aprender, por isso a Amazon recomenda montar campanhas de evento 14 dias antes. Item sem estoque não é impulsionado. Fonte: [OFICIAL] q0-Y5gG6Q2w, 2026-09-15.
- **Posições patrocinadas.** No topo da busca, um bloco é reservado a campanhas; segundo a palestrante, "do quinto anúncio para baixo" vêm os orgânicos. Ela disse "se eu não me engano", por isso confiança C. Observação direta: 8 dos 30 primeiros resultados de "café em grãos" eram patrocinados (posições 1 a 4 e 21 a 24), além de um banner de marca no topo. Fonte: [OBS] observacao/lideres.tsv, amazon.com.br/s?k=café+em+grãos, 2026-10-14.

### 2.5 Construção do anúncio: regras oficiais

| Elemento | Regra ou orientação oficial | Fonte e data |
|---|---|---|
| Título (BR) | Claro e objetivo, com marca e características principais. Palavras proibidas são avisadas na hora; exemplo citado: "venda de atacado". | [OFICIAL] yutQ_7zR4Eo, 2026-10-02 |
| Título (BR) | Máximo de 75 caracteres a partir de 27/07/2026; a IA da Amazon reescreve se o vendedor não ajustar. Em produto de marca antiga, só o criador do anúncio ou o dono da marca editam; senão a Amazon altera. | [OFICIAL via terceiro] cNn3iConWSw, 2026-07-23 (Seller News mostrado na tela) |
| Título (EUA) | Limite de 200 caracteres, recomendação de até 60; tipo de produto, marca, cor e tamanho. | [OFICIAL] sell.amazon.com/blog/amazon-seo, 2025-09-03 (pode estar superada) |
| Bullets | Até 5. Cada um com rótulo de 1 ou 2 palavras e até 100 caracteres de explicação (EUA). | [OFICIAL] sell.amazon.com/blog/amazon-product-listings (2026-04-29); amazon-seo |
| Imagens | Até 9. Principal com fundo branco; produto ocupando 85% ou mais do quadro (EUA). No BR: PNG, JPG, GIF ou TIF, até 10 MB; a primeira imagem é sempre a principal. | [OFICIAL] amazon-seo; product-listings; O_kXw3vvD8s (2026-10-13) |
| Selos na imagem | Selo "Black Friday" na foto pode suprimir o item, porque foge das diretrizes de imagem. | [OFICIAL] O_kXw3vvD8s, 2026-10-13 |
| Vídeo | Upload por produto direto no Seller Central (pela integração, "acredito que não"). | [OFICIAL] nDtHI8fUEAA |
| Palavras de backend | Campo "Generic keyword": tudo em minúsculas, separado por espaço, sem artigos e preposições, sem repetir termo. O limite em bytes não foi confirmado nesta rodada. | [OFICIAL] amazon-seo (EUA) |
| Atributos | Obrigatórios mudam por categoria. Atributos secundários (ocasião, estilo) não são obrigatórios, mas "podem diferenciar". | [OFICIAL] nDtHI8fUEAA; yutQ_7zR4Eo |
| Variações | Precisa haver um atributo diferenciador (o tema). O SKU pai só agrupa a família; o estoque é controlado pelos SKUs filhos. Não há limite de variações. Cada filho tem sua imagem com fundo branco. O cadastro reflete em cerca de 15 minutos; agrupar SKU solto leva até 24 horas (48 horas em lote). Variação personalizada: recomendado criar produto novo. | [OFICIAL] O_kXw3vvD8s, 2026-10-13 |
| Personagens e licenças | Usar Disney, Batman e similares exige carta de autorização; senão há violação de propriedade intelectual. | [OFICIAL] O_kXw3vvD8s |
| Kits | Kit sem EAN da GS1 exige pedido de isenção de GTIN. Se todos os itens são da mesma marca, o kit pode sair com a marca; marcas diferentes viram genérico. Genérico não pode citar marca na foto, no título ou na descrição. | [OFICIAL] nDtHI8fUEAA; yutQ_7zR4Eo |
| Marca no cadastro | Grafia idêntica à aprovada no Brand Registry, incluindo maiúsculas. Produto publicado como genérico pode ser convertido para a marca via suporte; recadastrar do zero não leva o histórico. | [OFICIAL] nDtHI8fUEAA |

### 2.6 Indicadores de qualidade e supressão

- **"Suprimido"** significa item inativo por violação de política ou erro, como imagem de baixa qualidade removida de forma automática, atributo faltando ou documento pendente. O caminho para resolver está em "Notificações de desempenho". Fonte: [OFICIAL] nDtHI8fUEAA, 2026-08-20.
- **"Melhorar oferta" por IA.** O Seller Central tem esse recurso (Inventário > editar oferta > ver sugestões de IA), que reescreve título, bullets e atributos. Fontes: [OFICIAL] yutQ_7zR4Eo; [PRÁTICA com tela] cNn3iConWSw.
- **Códigos de erro de cadastro** (fonte: [OFICIAL] yutQ_7zR4Eo, 2026-10-02):

| Código | Significado | Como se resolve |
|---|---|---|
| 5665 | Marca ainda não existe na Amazon | Fotos com a marca visível; resposta em 1 a 5 dias úteis |
| 5461 | Autorização da marca para listar | Fotos e carta de autorização |
| 8541 e 8542 | Conflito: o EAN já existe com atributos diferentes | Ajustar atributos ao ASIN existente |
| 8560 | Atributo faltando ou falta de isenção de GTIN | Preencher o atributo ou pedir a isenção |
| 6024 | Aprovação para vender a marca | Nota fiscal de até 180 dias, com CNPJ |
| 6039 | Aprovação de subcategoria regulada (suplementos, bebidas alcoólicas, "perigosos") | Licença sanitária e documentos |

- **Autorização de marca não é vitalícia.** O prazo varia por marca, de três dias a três meses, e precisa ser renovada. Fonte: [OFICIAL] nDtHI8fUEAA.
- **Listing Hub.** Time interno gratuito da Amazon Brasil que cadastra em lote a partir de qualquer planilha, em até 10 dias úteis. Os itens sobem inativos até o vendedor informar estoque. Pedidos de documentos têm prazo de 72 horas úteis. Fontes: [OFICIAL] nDtHI8fUEAA e yutQ_7zR4Eo.
- **Cadastro com IA.** Funciona por texto, imagem, URL ou planilha de outro marketplace. Aceita descrição de até 500 palavras, mais até 3 imagens de referência (pode ser foto caseira ou tabela nutricional) e cria o anúncio "em menos de 15 minutos". Fontes: [OFICIAL] O_kXw3vvD8s e yutQ_7zR4Eo.

### 2.7 Avaliações: regras

- **Permitido:** o botão "Solicitar uma avaliação" na página do pedido, o programa Vine e um bom atendimento. **Proibido:** tentar influenciar notas e avaliações, pedir remoção de avaliação negativa ou pedir avaliação positiva. Avaliações que violam a política são removidas. Fonte: [OFICIAL] sell.amazon.com/tools/customer-reviews, sem data.
- **Avaliações falsas em escala.** A Amazon diz ter bloqueado mais de 200 milhões de avaliações suspeitas em 2022 e processado mais de 90 agentes. Detecta por aprendizado de máquina, olhando vínculos entre contas, login e histórico. Fonte: [OFICIAL] aboutamazon.com, por volta de meados de 2023 (pode estar superada).

---

## 3. O que os melhores fazem

### 3.1 Consenso (três ou mais fontes concordam)

- **Primeira foto e título decidem o clique; página e preço decidem a conversão.** O funil é impressão → clique (CTR) → visita → venda. O painel de Ads não mostra a conversão; calcula-se pedidos ÷ cliques. Se Ads trazem cliques sem venda, o problema costuma estar na "etapa B" (anúncio, preço, avaliações), e não na campanha. Fontes: [PRÁTICA] ekW57cfZ8dc (Ariadne, 2026-06-01), VK7jalYzwxc (Caio Andrade, 2026-08-03), 78sSkRh2crI (2026-08-18); [OFICIAL] 06XpeVMN7ek ("listagem fraca" como causa de Ads ruins).
- **Ads como acelerador do orgânico.** A lógica é tolerar ACOS próximo da margem no lançamento e acompanhar o TACOS (Ads ÷ faturamento total) como métrica de portfólio. Fontes: [PRÁTICA] 9Hlvkfh1Eow (Bruno Capellete) e VK7jalYzwxc ("ACOS empatado" com Vine no lançamento); [OFICIAL] VvcswcsjuUw (Head de FBA: anúncio "acelera a conversão" de produto novo). Nenhuma fonte apresenta pausa ou holdout, então isto é atribuição, não causalidade.
- **Título com marca, atributo e uso, sem palavras sensacionalistas e sem especificação omitida.** O cliente que clica por engano derruba a conversão. Fontes: [PRÁTICA] VH7Q5FddoRY (Smollan), ekW57cfZ8dc; [OFICIAL] yutQ_7zR4Eo.
- **Não ficar sem estoque e ter oferta híbrida** (FBA mais DBA ou envio próprio). Fontes: [OFICIAL] q0-Y5gG6Q2w e VvcswcsjuUw; [PRÁTICA] VH7Q5FddoRY e 02Bn3HyAYqk.
- **Baixar preço via oferta ou cupom, e não editando o preço base.** Isso preserva o histórico e mostra preço cortado; produto sem histórico não mostra preço cortado. Fontes: [OFICIAL] q0-Y5gG6Q2w e K7a4jlTP9ME; [PRÁTICA] VH7Q5FddoRY.
- **Usar a logística da Amazon na disputa de Buy Box.** Fontes: [OFICIAL] nDtHI8fUEAA; [PRÁTICA] 02Bn3HyAYqk e 78sSkRh2crI.

### 3.2 Pesquisa de palavra-chave

- **Oficial, para marca registrada.** O Brand Analytics traz:
  - Search Query Performance: volume, impressões, cliques, carrinho e compra por termo;
  - Top Search Terms: os 3 produtos, categorias e marcas por termo;
  - Search Catalog Performance: o mesmo funil, por ASIN;
  - Market Basket e Repeat Purchase.
  
  Exige conta profissional e papel de representante da marca no Brand Registry. Fontes: [OFICIAL] sell.amazon.com/tools/amazon-brand-analytics (EUA, sem data); venda.amazon.com.br/brand-registry (BR, cita Brand Analytics). A página não diz se o SQP no Brasil mostra "share" por etapa: verificar.
- **Relatório de termos de pesquisa da campanha automática.** É o método mais citado por praticantes brasileiros para descobrir os termos que vendem. Roda-se a campanha automática por cerca de 14 a 30 dias, colhem-se os termos que converteram, levam-se para a campanha manual e negativam-se os que não convertem. Fontes: [OFICIAL] 06XpeVMN7ek; [PRÁTICA] ekW57cfZ8dc e 9Hlvkfh1Eow.
- **Barra de busca e "IA vê imagem".** São citadas como auxílio, sem método publicado. Ferramentas como Helium 10 Cerebro não aparecem nas transcrições brasileiras desta frente. Fica como lacuna para o Brasil: o volume de busca dessas ferramentas é estimado nos EUA.
- **Palavra de marca concorrente em Ads.** Praticante desaconselha anunciar seu produto para a marca de outro, por quebra de expectativa e perda de dinheiro, mas trata como tática e não como proibição. Fonte: [PRÁTICA] ekW57cfZ8dc. Não se achou regra oficial brasileira sobre segmentar marca alheia em Ads (ver seção 9).

### 3.3 Avaliações dentro das regras

- **Vine no lançamento** (marca registrada ou genérico, FBA). Fontes: [PRÁTICA] VK7jalYzwxc; [OFICIAL] sell.amazon.com/tools/vine.
- **Pedido de avaliação automatizado.** Praticante usa ferramenta (SellerBoard) que dispara a solicitação pelo canal da Amazon cerca de 10 dias após a entrega, excluindo pedidos FBM, pedidos com promoção e clientes com feedback negativo. Fonte: [PRÁTICA] AuWtJJ_708Q (Ariadne, 2026-06-24), com tela.
  - A mesma fonte diz que a Amazon já pede avaliação 5 a 6 dias após a entrega.
  - Há conflito de interesse: link de afiliado e "2 meses grátis". Três sinais fracos (CTA, número sem base, conflito), então N7 no número.
  - A janela oficial do botão "Solicitar uma avaliação" não foi confirmada nesta rodada.
- **Evento como acelerador de avaliações.** Picos de venda como a Black Friday geram avaliações e "relevância" para conta nova. Limitar quantidade por cliente em descontos agressivos: "melhor ter 50 pedidos e 50 avaliações". Fontes: [OFICIAL] K7a4jlTP9ME (2026-09-04); [PRÁTICA] VH7Q5FddoRY.

### 3.4 Teste A/B e conteúdo de marca

- **Teste oficial.** O "Gerenciar seus experimentos" divide visitantes aleatoriamente e, por padrão, publica o vencedor. Os praticantes brasileiros desta frente não o citam; é mais uma lacuna de prática do que de regra. Fonte: [OFICIAL] sell.amazon.com/tools/manage-your-experiments.
- **Brand Store e Sponsored Brands.** Abas por linha de produto (exemplo dado pela própria Amazon: cápsulas e café em pacote). Sponsored Brands pode ir para uma aba específica. O objetivo "parcela de impressão no topo" é cobrado por CPM e medido pela parcela de impressões no topo da busca. O painel de insights da loja separa vendas de origem paga e orgânica. Fonte: [OFICIAL] 7ILvtU6GcPo, 2026-09-11.
- **Criativos por IA.** O "Estúdio de criativos" do console de Ads gera imagem e vídeo de 5 a 10 segundos grátis, para Sponsored Brands, Display, A+ e loja. Fontes: [OFICIAL] 7ILvtU6GcPo e O5sTGf_Rtic; [PRÁTICA com tela] xnQcZ_7-6lQ (2026-08-14).

### 3.5 Divergências entre fontes

| Tema | Posição A | Posição B | Leitura |
|---|---|---|---|
| Limite de título | 75 caracteres no BR desde 27/07/2026 (cNn3iConWSw, Seller News na tela) | 200 caracteres com recomendação de até 60 (EUA, set/2025) | Tratar como faixa de 60 a 75 caracteres úteis; checar a ajuda BR logada |
| Preço baixo para ranquear | Funciona e é "o melhor dos mundos" com estoque profundo (9Hlvkfh1Eow) | Preferir margem maior e Ads para empatar nos primeiros meses (mesma fonte) | Escolha de caixa, não de regra |
| Oferta em destaque | "Nem sempre o melhor preço ganha" (GBnC2vqmRQo) | Preço é o primeiro fator citado (nDtHI8fUEAA) | Compatíveis: preço pesa, mas entrega, métricas e região também |
| Ads indispensável | "Na Amazon ainda vende no orgânico" (9Hlvkfh1Eow) | Ads é "indispensável" (78sSkRh2crI) | Divergência de praticantes; sem dado de share orgânico por categoria no BR |

---

## 4. Números de referência

| Indicador | Valor ou faixa | Tipo | Fonte | Data | Observação |
|---|---|---|---|---|---|
| Título BR | máx. 75 caracteres | OFICIAL via terceiro | cNn3iConWSw | 2026-07-23 | checar |
| Título EUA | máx. 200, recomenda ≤60 | OFICIAL | sell.amazon.com/blog/amazon-seo | 2025-09-03 | pode estar superada |
| Bullets | até 5; ≤100 caracteres de explicação | OFICIAL | product-listings; amazon-seo | 2026-04-29 / 2025-09 | EUA |
| Imagens | até 9; produto ≥85% do quadro; ≤10 MB | OFICIAL | product-listings; amazon-seo; O_kXw3vvD8s | 2025-2026 | |
| Índice de qualidade alto | 4x visitas, cerca de +36% vendas | OFICIAL (sem método) | nDtHI8fUEAA | 2026-08-20 | confiança C no número |
| A+ básico / Premium | até +8% / até +20% vendas | OFICIAL (dado interno) | venda.amazon.com.br/brand-registry; sell.amazon.com/tools/a-content | ref. ago/2024 | pode estar superada |
| Brand Store | +53,9% frequência; +71,3% ticket | OFICIAL (dado interno) | venda.amazon.com.br/brand-registry | ref. ago/2024 | correlação, não causa |
| Programe e Poupe | desconto de 10% a 15% → até 1,8x conversão | OFICIAL (dado interno) | venda.amazon.com.br/brand-registry | ref. ago/2024 | relevante para recompra |
| Experimentos A/B | mínimo de cerca de 4 semanas; recomendado 8 a 10; até +20% | OFICIAL | manage-your-experiments | sem data | EUA |
| Vine | <30 avaliações; ≤30 unidades; US$0/75/200; +30% vendas | OFICIAL | sell.amazon.com/tools/vine | sem data | EUA; BR não confirmado |
| Conversão com avaliações | 5 avaliações ≈ +270% vs 0; nota 4,2 a 4,5 > 5,0 | OFICIAL | customer-reviews-social-proof | 2026-08-18 | EUA |
| Conversão média Amazon BR | 4% a 5% (sessões → vendas) | PRÁTICA (sem base) | 9Hlvkfh1Eow | 2026-07-21 | N7; só hipótese |
| Avaliação por venda | cerca de 1 a cada 100 vendas | PRÁTICA (sem base) | AuWtJJ_708Q | 2026-06-24 | N7; só hipótese |
| CTR "típico" | 0,3 a 0,4 (unidade incerta) | DADO fraco | helium10.com/blog/amazon-conversion-rate | 2025-02-18 | lido do Perplexity ao vivo; descartável |
| Aprendizado de campanha de Ads | 1 a 2 semanas (14 dias) | OFICIAL | q0-Y5gG6Q2w | 2026-09-15 | |
| Negativar termos | após cerca de 14 dias; automática por cerca de 1 mês antes da manual | OFICIAL | 06XpeVMN7ek | 2026-08-17 | |
| Preço cortado (preço "De") | mediana do preço de venda em 90 dias | OFICIAL | q0-Y5gG6Q2w | 2026-09-15 | |
| Promoção Pix própria | entra no ar em cerca de 4 horas | OFICIAL | H0ab_x1YIBY | 2026-10-14 | |
| Planos Vantagens | 1,5% (parcelamento); Mais Vantagens 2,5% a partir de 31/10/2026; itens de R$40 a R$10.000 | OFICIAL | H0ab_x1YIBY | 2026-10-14 | taxa sobre o preço listado, mesmo em venda com Pix |
| Pagamentos | 55% parcelado; 20% Pix; 40% do tráfego via Google Shopping | OFICIAL (dado interno) | H0ab_x1YIBY | 2026-10-14 | |
| Listing Hub | até 10 dias úteis; documentos em 72 h úteis | OFICIAL | nDtHI8fUEAA; yutQ_7zR4Eo | 2026 | |
| Erro 5665 (marca nova) | 1 a 5 dias úteis | OFICIAL | yutQ_7zR4Eo | 2026-10-02 | |
| NF para erro 6024 | emitida até 180 dias antes | OFICIAL | yutQ_7zR4Eo | 2026-10-02 | |
| Patrocinados na busca "café em grãos" | 8 de 30 (posições 1-4 e 21-24) | OBS | lideres.tsv | 2026-10-14 | uma busca, sem CEP registrado |
| Case de lançamento (marca nova) | de cerca de 20.000 para posição 17 na palavra-chave; 20 a 60 un./dia; 50% orgânico; R$10 a 15 mil de Ads; lucro no 3º ou 4º mês | PRÁTICA (rebaixado de CASE: sem base nem período exatos) | 9Hlvkfh1Eow | 2026-07-21 | conflito de interesse (vende consultoria) |
| Recomendações da IA de compras | 63,9% fora do top 10; 40,9% fora da página | DADO | Marketplace Pulse | 2026-07-16 | EUA; estudo de fornecedor |
| Fatores de compra (EUA) | 63% priorizam preço; cerca de 1/3 avaliações, frete e marca | DADO | Jungle Scout Consumer Trends 2025 (n≈1.000, dez/2024) | 2025 | EUA |
| Desafios do vendedor | 32% citam alta de custo de Ads | DADO | Jungle Scout State of the Amazon Seller 2025 (n≈1.500, jan/2025, 20+ países) | 2025 | global |
| Comissão Alimentos e Bebidas | 10% (mínimo R$1) | OFICIAL | venda.amazon.com.br/precos | atualizada em 20/01/2025 | pode estar superada; detalhe na frente preco-promocao |

---

## 5. Alimentos, perecíveis e marca própria/indústria

- **O que os líderes mostram** (observação direta, 2026-10-14, lideres.tsv):
  - O #1 em Café (Orfeu em grãos 1 kg) é 1P (vendido e enviado pela Amazon). Tem 16.737 avaliações, 6 fotos, 1 vídeo, 5 bullets e A+, e variações de sabor e tamanho no mesmo anúncio. Na página dele aparece banner patrocinado de concorrente.
  - Coffee Mais 250 g tem o selo "Escolha da Amazon". O título usa separadores e atributos (100% arábica, torra média, peso), com 4 fotos e sem A+.
  - Baggio aromatizado tem 10,9 mil avaliações e A+.
  - Italle (marca 3P com FBA) compra a 1ª posição patrocinada e banners nas páginas de concorrentes, e tem "Programe e Poupe".
  - Leitura: em café, quem lidera combina volume de avaliações (milhares), A+, variações agrupadas e, no caso de quem está entrando, mídia agressiva de marca.
- **Variação por tamanho e quantidade.** Em alimentos, "pacote 250 g / 500 g / 1 kg" e "kit com 2 ou 4" são variações de quantidade. Peso e dimensão de cada filho mudam o frete. Fonte: [OFICIAL] O_kXw3vvD8s (exemplo de potes de vidro).
- **Tabela nutricional e embalagem como insumo.** A IA de cadastro lê imagem "caseira" da embalagem para preencher atributos de produto comestível; depois troca-se pela foto oficial. Fonte: [OFICIAL] O_kXw3vvD8s.
- **Categorias reguladas.** Suplementos pedem documentos Anvisa, tabela nutricional, fotos e nota fiscal. Bebidas alcoólicas pedem licença sanitária (72 horas úteis para enviar). Usam os erros 6039 ou 6024. Fontes: [OFICIAL] nDtHI8fUEAA e yutQ_7zR4Eo. Para café e alimentos comuns, nenhuma fonte desta rodada descreveu exigência específica de aprovação. Regras de validade mínima no FBA não foram obtidas (ver seção 9).
- **Recompra.** "Programe e Poupe" (assinatura) aparece em líderes de produto de recompra, como Italle e Lysoform. A Amazon declara até 1,8x de conversão com desconto de 10% a 15%. Fontes: [OFICIAL] venda.amazon.com.br/brand-registry; [OBS] lideres.tsv.
- **Marca própria e indústria.** Conta como "dono do ASIN": controla o conteúdo e tem acesso a A+, Brand Store, Sponsored Brands, Brand Analytics, Vine e experimentos. Com protocolo do INPI já aberto, consegue registrar a marca e usar quase todas as ferramentas, exceto denúncia. Fonte: [OFICIAL] 7ILvtU6GcPo, 2026-09-11. A Amazon cita uma marca de café como exemplo de loja com abas.
- **Kits de café da mesma marca** podem sair com a marca e com isenção de GTIN se não houver EAN de kit. O dono da marca no Brand Registry pode declarar "sem EAN" para kits específicos. Fontes: [OFICIAL] nDtHI8fUEAA e yutQ_7zR4Eo.

---

## 6. Erros comuns e mitos

| Afirmação fraca ou erro | O que as fontes fortes dizem | Fontes |
|---|---|---|
| "Quem tem o menor preço ganha a Buy Box." | Falso como regra: entrega, frete, métricas de conta, preço externo e região também pesam. | nDtHI8fUEAA [OFICIAL]; GBnC2vqmRQo [PRÁTICA] |
| "Basta ligar Ads que vende." | Ads levam o cliente até a página; a conversão depende da página, do preço e das avaliações. A Amazon cita "listagem fraca" como causa. | ekW57cfZ8dc; 06XpeVMN7ek [OFICIAL] |
| "Revendedor deve melhorar o título e as fotos do ASIN." | Revendedor não edita: a precedência é marca, depois sistema, depois maioria. | nDtHI8fUEAA [OFICIAL] |
| "Criar outro ASIN para o mesmo produto de marca e fugir da Buy Box." | Cai e impacta a conta; só genérico admite mais de um ASIN. | yutQ_7zR4Eo [OFICIAL] |
| "Selo de Black Friday na foto aumenta o clique." | Pode suprimir o item. | O_kXw3vvD8s [OFICIAL] |
| "Baixar o preço na mão antes do evento." | Quebra o histórico e o preço cortado (mediana de 90 dias); usar oferta ou cupom. | q0-Y5gG6Q2w; K7a4jlTP9ME [OFICIAL] |
| "1 avaliação a cada 100 vendas." | Número sem base, em vídeo com CTA de ferramenta afiliada (N7). Usar só como pergunta. | AuWtJJ_708Q |
| "Conversão média da Amazon é 4% a 5%." | Sem amostra nem período; vem de quem vende software e consultoria (N7). | 9Hlvkfh1Eow |
| "Mudar preço muitas vezes não afeta o algoritmo." | Afirmação de quem vende o repricer (952 alterações em 30 dias num SKU); sem teste. | GBnC2vqmRQo (conflito de interesse) |
| "Pedir avaliação por ferramenta externa é hack que ninguém conta." | O canal oficial é o botão "Solicitar uma avaliação"; influenciar avaliação é proibido. Ferramentas que só automatizam o pedido padrão são prática comum, mas o texto da mensagem precisa seguir a política. | AuWtJJ_708Q; sell.amazon.com/tools/customer-reviews |
| "Em ACOS, o que importa é ACOS baixo." | Confunde métricas: com lançamento, o que pesa é o TACOS e o efeito no orgânico; sem holdout não se prova o efeito. | VK7jalYzwxc; 9Hlvkfh1Eow |
| "Rank orgânico garante aparecer na IA de compras." | Estudo nos EUA: o rank é o preditor mais fraco das recomendações da IA. | Marketplace Pulse 2026-07-16 [DADO] |
| Fonte americana (200 caracteres) usada como regra brasileira | Há sinal de regra BR mais curta (75); não importar regra dos EUA sem checar. | cNn3iConWSw vs amazon-seo |

---

## 7. Revenda/importação x indústria/marca própria

**[REVENDA] revenda de marca de terceiros e genérico importado**
- **O jogo é a oferta em destaque**, e não o conteúdo. Pesam preço (inclusive Pix), FBA ou DBA, métricas de conta e região. Fonte: nDtHI8fUEAA.
- **Ferramentas de precificação automática** (Amazon ou terceiros) disputam a Buy Box mantendo o maior preço que ainda vence. Fonte: GBnC2vqmRQo, com conflito de interesse.
- **Autorizações de marca.** O erro 5461 é para listar e o 6024 para vender; a autorização expira e precisa ser renovada. Fontes: nDtHI8fUEAA e yutQ_7zR4Eo.
- **"Buy Box é jogo de relacionamento;** listagem própria é jogo de ranqueamento." Fonte: [PRÁTICA] 78sSkRh2crI.
- **Genérico importado.** Cria ASIN próprio, sem disputa no próprio ASIN, mas também sem Brand Registry, o que significa sem A+, sem Brand Analytics e sem experimentos. Exceção: o Vine aceita "produtos genéricos" do catálogo. Fontes: 02Bn3HyAYqk; sell.amazon.com/tools/vine; sell.amazon.com/tools/a-content (A+ para genérico em alguns casos: verificar no BR).
- **Ao entrar num ASIN existente**, o produto novo aproveita "todo o histórico" e pode receber oferta sugerida sem esperar. Fonte: K7a4jlTP9ME.
- **Exemplo de genérico importado observado:** suporte de notebook com 53 ofertas no mesmo ASIN. Fonte: [OBS] lideres.tsv.

**[MARCA] indústria e marca própria**
- **Controle do conteúdo (precedência)**, mais A+ (até +8% ou +20% declarados), Brand Store, Sponsored Brands (CPC ou CPM de topo), Brand Analytics com funil por termo, experimentos A/B e denúncia de propriedade intelectual, além do Project Zero. Fontes: venda.amazon.com.br/brand-registry; 7ILvtU6GcPo.
- **Produto novo começa sem histórico.** Não entra em ofertas sugeridas nem mostra preço cortado, e precisa gerar tração com desconto, Ads e Vine. Fontes: K7a4jlTP9ME e q0-Y5gG6Q2w.
- **Revendedores no ASIN da marca.** A marca disputa a Buy Box com revendedores no próprio ASIN, mas mantém o conteúdo. Revendedor que cadastrou com grafia errada da marca: o caminho é denúncia no Brand Registry. Fonte: 7ILvtU6GcPo.

**Vale para ambos:** imagem principal com fundo branco, atributos completos, variações agrupadas, estoque sem ruptura, oferta híbrida e Ads para acelerar a conversão no lançamento.

---

## 8. Tabela de afirmações

| id | Afirmação | Tipo | Fonte | Data | Confiança |
|---|---|---|---|---|---|
| A1 | A Amazon não publica fórmula; cita relevância, preço, qualidade do anúncio, saúde da conta, Ads e vendas | OFICIAL | sell.amazon.com/blog/amazon-seo | 2025-09-03 | média |
| A2 | Preço competitivo pode fazer a oferta subir organicamente | OFICIAL | idem | 2025-09-03 | média |
| A3 | A busca usa modelos de aprendizado de máquina por categoria | DADO | amazon.science (SIGIR 2016) | 2016 | média |
| A4 | Produtos Patrocinados exigem elegibilidade à oferta em destaque e estoque | OFICIAL | advertising.amazon.com/pt-br | 2026 | alta |
| A5 | Fatores da Buy Box: preço, prazo e custo de entrega, métricas da conta, preço externo, região; FBA ajuda | OFICIAL | nDtHI8fUEAA | 2026-08-20 | alta |
| A6 | Oferta 10% a 20% mais barata pode não ganhar a Buy Box | PRÁTICA | GBnC2vqmRQo | 2026-08-27 | média |
| A7 | Mais Vantagens: Buy Box usa o preço com Pix; taxa de 2,5% a partir de 31/10/2026; itens de R$40 a R$10.000 | OFICIAL | H0ab_x1YIBY | 2026-10-14 | média |
| A8 | Há Buy Box secundária para parcelamento sem juros | OFICIAL | H0ab_x1YIBY | 2026-10-14 | média |
| A9 | Precedência do conteúdo: marca, depois sistema, depois maioria | OFICIAL | nDtHI8fUEAA; 7ILvtU6GcPo | 2026 | alta |
| A10 | Índice de qualidade alto: 4x visitas, cerca de +36% vendas | OFICIAL (sem método) | nDtHI8fUEAA | 2026-08-20 | baixa |
| A11 | Título BR limitado a 75 caracteres desde 27/07/2026; a IA reescreve | OFICIAL via terceiro | cNn3iConWSw | 2026-07-23 | baixa |
| A12 | Título EUA: 200 caracteres de limite, recomendação de ≤60 | OFICIAL | amazon-seo | 2025-09-03 | média |
| A13 | Até 5 bullets e até 9 imagens; imagem principal com fundo branco | OFICIAL | product-listings; O_kXw3vvD8s | 2026 | alta |
| A14 | Selo promocional na imagem pode suprimir | OFICIAL | O_kXw3vvD8s | 2026-10-13 | média |
| A15 | Produto com marca duplicado em outro ASIN cai e impacta a conta; genérico pode duplicar | OFICIAL | yutQ_7zR4Eo | 2026-10-02 | média |
| A16 | SKU não se altera nem se reutiliza; EAN vinculado a um ASIN | OFICIAL | nDtHI8fUEAA | 2026-08-20 | alta |
| A17 | Erros 5665, 5461, 8541/8542, 8560, 6024, 6039 e soluções | OFICIAL | yutQ_7zR4Eo | 2026-10-02 | média |
| A18 | Autorização de marca expira (de dias a meses) | OFICIAL | nDtHI8fUEAA | 2026-08-20 | média |
| A19 | Variações: tema obrigatório, sem limite; agrupamento em até 24 a 48 horas | OFICIAL | O_kXw3vvD8s | 2026-10-13 | média |
| A20 | Campanha de Ads leva de 1 a 2 semanas para aprender; item sem estoque não é impulsionado | OFICIAL | q0-Y5gG6Q2w | 2026-09-15 | média |
| A21 | Leilão de Ads = lance x relevância; automática por cerca de 1 mês; negativar após cerca de 14 dias; sem data de término | OFICIAL | 06XpeVMN7ek | 2026-08-17 | média |
| A22 | Preço cortado = mediana de 90 dias; produto sem histórico não tem preço cortado | OFICIAL | q0-Y5gG6Q2w | 2026-09-15 | média |
| A23 | Ruptura faz perder Buy Box e relevância, e recuperar a posição é difícil | OFICIAL + PRÁTICA | VvcswcsjuUw; VH7Q5FddoRY | 2026 | alta |
| A24 | Mais conversão em menos tempo leva a mais rank orgânico; Ads alimenta o orgânico | PRÁTICA | 9Hlvkfh1Eow; VK7jalYzwxc; 78sSkRh2crI | 2026 | média |
| A25 | Conversão média de 4% a 5% | PRÁTICA (N7) | 9Hlvkfh1Eow | 2026-07-21 | baixa |
| A26 | Cerca de 1 avaliação a cada 100 vendas | PRÁTICA (N7) | AuWtJJ_708Q | 2026-06-24 | baixa |
| A27 | É proibido influenciar avaliações ou pedir avaliação positiva ou remoção | OFICIAL | sell.amazon.com/tools/customer-reviews | sem data | alta |
| A28 | 5 avaliações ≈ +270% de conversão vs 0; nota 4,2 a 4,5 converte melhor que 5,0 | OFICIAL | customer-reviews-social-proof | 2026-08-18 | média |
| A29 | Vine: <30 avaliações, ≤30 unidades, US$0/75/200, +30% vendas | OFICIAL | sell.amazon.com/tools/vine | sem data | média |
| A30 | Experimentos A/B: Brand Registry; mínimo de cerca de 4 semanas; 8 a 10 recomendadas; até +20% | OFICIAL | manage-your-experiments | sem data | média |
| A31 | A+ até +8% (básico) / +20% (Premium); Brand Store +53,9% frequência | OFICIAL (dado interno) | venda.amazon.com.br/brand-registry | ref. 2024 | baixa |
| A32 | Brand Analytics: SQP, TST, SCP, Market Basket, Repeat Purchase | OFICIAL | sell.amazon.com/tools/amazon-brand-analytics | sem data | alta |
| A33 | Com protocolo do INPI, todas as ferramentas de marca menos denúncia | OFICIAL | 7ILvtU6GcPo | 2026-09-11 | média |
| A34 | Sponsored Brands com objetivo de parcela de impressão no topo cobra por CPM | OFICIAL | 7ILvtU6GcPo | 2026-09-11 | média |
| A35 | Mais de 200 milhões de avaliações falsas bloqueadas em 2022 | OFICIAL | aboutamazon.com | cerca de 2023 | média |
| A36 | 8 de 30 resultados patrocinados em "café em grãos" | OBS | lideres.tsv | 2026-10-14 | média |
| A37 | IA de compras recomenda 63,9% de produtos fora do top 10 orgânico | DADO | Marketplace Pulse | 2026-07-16 | baixa |
| A38 | 63% dos consumidores dos EUA priorizam preço; cerca de 1/3 avaliações | DADO | Jungle Scout Consumer Trends 2025 | 2025 | média |
| A39 | Listing Hub: cadastro gratuito em até 10 dias úteis, itens sobem inativos | OFICIAL | nDtHI8fUEAA; yutQ_7zR4Eo | 2026 | alta |
| A40 | Programe e Poupe: desconto de 10% a 15% → até 1,8x conversão | OFICIAL (dado interno) | venda.amazon.com.br/brand-registry | ref. 2024 | baixa |

---

## 9. Lacunas

- **Ajuda do Seller Central Brasil não lida** (exige login). Seguem sem N1 brasileiro escrito:
  - limite oficial de título (75 contra 200);
  - limite de bytes do campo de palavras de backend (o valor de 250 bytes circula, mas não foi verificado);
  - janela do botão "Solicitar uma avaliação" (o valor de 5 a 30 dias após a entrega circula, mas não foi verificado);
  - página "Como se tornar a oferta em destaque";
  - painel de qualidade das publicações e supressão.
- **Busca na web esgotada nesta sessão.** Ficaram sem busca: blogs brasileiros de ferramentas (Nubimetrics para Amazon BR, SmartScout, Helium 10 em PT), relatórios da Pacvue e da Perpetua, e notícias do Seller News sobre títulos.
- **Share da Buy Box nas vendas.** O número "80%+" circula em blogs e não teve fonte verificada nesta rodada.
- **Tempo até um anúncio novo ganhar posição.** Só há um relato de praticante (lucro no 3º ou 4º mês) e prazos de aprendizado de Ads (1 a 2 semanas). Não há estudo com metodologia.
- **Benchmarks de conversão, CTR e avaliação por venda na Amazon BR, por categoria.** Não há fonte pública com método; os números circulantes são N7.
- **Regra brasileira sobre palavra-chave de marca alheia.** Não se achou regra para Ads (segmentar marca concorrente) nem para backend (inserir marca alheia nos termos). Só há orientação de praticante.
- **Vine no Brasil.** Disponibilidade, taxas em reais e se o crédito vale no BR não foram confirmados.
- **Experimentos A/B no Brasil.** Não há confirmação de que "Gerenciar seus experimentos" esteja ativo no BR; nenhum praticante brasileiro o cita.
- **Alimentos.** Não foram obtidas regras de validade mínima e de lote no FBA, nem regras de rotulagem exigidas no anúncio (tabela nutricional, alergênicos) para alimentos comuns e café no BR.
- **Perguntas e respostas.** Não há fonte sobre o papel das perguntas e respostas no ranqueamento brasileiro. A Amazon cita "pergunta ativa" só como prova social (VH7Q5FddoRY).
- **Mercado Livre e Shopee.** Fora do escopo desta nota; ver as notas das plataformas.
- **Sem auditoria das ferramentas.** Nenhuma ferramenta publicou fórmula ou erro auditado; nenhum dado de ferramenta N5 foi somado.

**Fontes desta nota.**
- **Oficiais lidas (13 páginas):**
  - sell.amazon.com/blog/amazon-seo;
  - sell.amazon.com/tools/vine;
  - sell.amazon.com/tools/manage-your-experiments;
  - sell.amazon.com/tools/amazon-brand-analytics;
  - sell.amazon.com/tools/customer-reviews;
  - sell.amazon.com/blog/amazon-product-listings;
  - sell.amazon.com/tools/a-content;
  - sell.amazon.com/blog/customer-reviews-social-proof;
  - venda.amazon.com.br/brand-registry;
  - venda.amazon.com.br/precos;
  - venda.amazon.com.br/guia-cadastro-vendedor-amazon;
  - advertising.amazon.com/pt-br/solutions/products/sponsored-products;
  - aboutamazon.com (avaliações falsas).
- **Webinars oficiais em vídeo:** nDtHI8fUEAA, yutQ_7zR4Eo, O_kXw3vvD8s, H0ab_x1YIBY, 7ILvtU6GcPo, q0-Y5gG6Q2w, K7a4jlTP9ME, 06XpeVMN7ek, VvcswcsjuUw.
- **Dados:** Jungle Scout (State of the Amazon Seller 2025; Consumer Trends 2025), Marketplace Pulse (16/07/2026), Amazon Science (2016), Helium 10 (fraco).
- **Observação:** observacao/lideres.tsv (2026-10-14).

## 10. Verificação (2026-10-14)

Método: releitura das páginas oficiais em texto (sell.amazon.com, venda.amazon.com.br, advertising.amazon.com/pt-br). A busca na web estava esgotada nesta rodada, então os webinars em vídeo não foram reassistidos e nada novo foi buscado. Afirmações que dependem só de vídeo ficam "SEM FONTE OFICIAL (texto)": não é refutação, é falta de página oficial em texto para conferir. Na dúvida, não confirmado.

| id | veredito | fonte oficial (URL) | observação |
|---|---|---|---|
| R1 | SEM FONTE OFICIAL (texto) | https://sell.amazon.com/blog/amazon-seo (2025-09-03) | A página dos EUA diz limite de 200 caracteres e recomenda até 60, como na nota. Não achei página oficial em texto sobre 75 caracteres no BR a partir de 27/07/2026 nem sobre reescrita por IA. Sustentado só pelo vídeo cNn3iConWSw. |
| R2 | CONFIRMADA | https://advertising.amazon.com/pt-br/solutions/products/sponsored-products (sem data) | A página diz que o item precisa estar qualificado para a oferta em destaque e que o anúncio só aparece com estoque. O termo "Buy Box" não aparece; equivale à oferta em destaque. |
| R3 | SEM FONTE OFICIAL (texto) | https://venda.amazon.com.br/precos (tarifas de 20/01/2025 e 01/08/2025) | A página não cita Amazon Mais Vantagens, Pix, taxa de 2,5% nem teto de R$10.000. Cita só o parcelamento sem juros com tarifa de 1,5% a partir de R$40, o que bate com a parte do "Amazon Vantagens". Sustentado só pelo webinar H0ab_x1YIBY. A página parece anterior ao anúncio. |
| R4 | SEM FONTE OFICIAL (texto) | https://sell.amazon.com/blog/amazon-buy-box (404 na leitura) | Não consegui ler página oficial em texto com os fatores da oferta em destaque no BR. Sustentado só pelo webinar nDtHI8fUEAA. |
| R5 | SEM FONTE OFICIAL (texto) | https://venda.amazon.com.br/brand-registry (sem data) | A página só fala de conteúdo aprimorado e proteção da marca. Não traz a ordem de precedência de edição. Sustentado só pelos webinars. |
| R6 | SEM FONTE OFICIAL (texto) | nenhuma página lida | Regra do preço De como mediana de 90 dias só aparece em webinars. Sem texto oficial para conferir. |
| R7 | SEM FONTE OFICIAL (texto) | https://advertising.amazon.com/pt-br/library/guides/sponsored-products (404 na leitura) | Prazos de aprendizado, negativação e data de término sem texto oficial verificado. Sustentado só pelos webinars. |
| R8 | SEM FONTE OFICIAL (texto) | nenhuma página lida | Regras de ASIN duplicado e de SKU sem texto oficial verificado. Sustentado só pelos webinars. |
| R9 | SEM FONTE OFICIAL (texto) | https://sell.amazon.com/blog/amazon-product-listings (2026-04-29) | A página confirma até 9 imagens. Não exige fundo branco (só recomenda fundo simples e bem iluminado), não traz formatos nem o limite de 10 MB e não trata de selo promocional. O resto da afirmação vem só do webinar O_kXw3vvD8s. |
| R10 | CONFIRMADA | https://sell.amazon.com/tools/vine (sem data; pode estar superada) | Menos de 30 avaliações, inscrição limitada a 30 unidades, taxa por ASIN pai: US$0 até 2, US$75 de 3 a 10, US$200 de 11 a 30. Acréscimos da página: exige listagem FBA, não vale para itens adultos, digitais ou kits, e a cobrança só ocorre após a primeira avaliação (sem avaliação em 90 dias, sem cobrança). Valor no BR segue não confirmado. |
| R11 | CONFIRMADA | https://sell.amazon.com/tools/customer-reviews (sem data) | Proibido tentar influenciar avaliações, pedir avaliação positiva ou pedir remoção de negativa. Canal permitido: botão "Solicitar uma avaliação" nos detalhes do pedido. A página não traz janela de dias após a entrega. |
| R12 | CONTESTADA | https://sell.amazon.com/tools/manage-your-experiments (sem data; rodapé 2026) | A página diz que 8 a 10 semanas são recomendadas quando o vendedor define a duração. "Cerca de 4 semanas" é um resultado possível na opção "até a significância", não um mínimo. Exige conta Profissional, papel de representante de marca no Brand Registry e tráfego suficiente. Testa imagens, título, bullets, descrição e A+ (inclui Brand Story). Não lista marketplaces; links apontam para os EUA, então a vigência no BR segue não confirmada. |

Placar: 3 confirmadas (R2, R10, R11), 1 contestada (R12), 8 sem fonte oficial em texto (R1, R3 a R9).
