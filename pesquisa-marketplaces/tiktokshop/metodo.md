# Estado da arte: como os profissionais pesquisam e diagnosticam o TikTok Shop

Frente: MÉTODO · Data da pesquisa: 2026-10-15 · Escopo: TikTok Shop Brasil, com referências de EUA, Reino Unido e Sudeste Asiático quando a mecânica é a mesma (sempre marcadas com o país).

Este documento complementa `metodo/estado-da-arte.md` (ML, Shopee, Amazon). O que vale lá e vale aqui é só referido. Aqui entra o que é próprio do social commerce.

**Como ler**
- Cada afirmação traz fonte, data da fonte e TIPO: [OFICIAL] regra, tarifa, política ou número dito pela plataforma · [PRÁTICA] tática de praticante · [CASE] números de uma operação · [DADO] estudo, relatório ou ferramenta · [OBS] observação ou cálculo desta frente.
- "s/d" = sem data na fonte; vale a data de acesso (2026-10-15).
- Regra de plataforma com mais de 6 meses (anterior a 2026-04-15) ou sem data leva **(pode estar superada)**. O TikTok Shop BR abriu em 2025-05-08; regra do BR antiga é ainda mais instável.
- País: sem marcação = Brasil. Outro país vem entre parênteses: (EUA), (Reino Unido), (Sudeste Asiático).
- **[REVENDA]** = revenda, dropshipping, importação ou afiliado puro. **[MARCA]** = indústria e marca própria. Sem marcador, vale para os dois.
- Nada aqui é recomendação para empresa alguma. É descrição de como o mercado opera e pesquisa.
- Páginas da TikTok Shop Academy Brasil (`seller-br.tiktok.com/university/essay?knowledge_id=...`) abrem sem login; o índice da Academy exige JavaScript. Citadas abaixo como "Academy BR, kid=<knowledge_id>".

---

## 1. O que muda em relação ao marketplace de busca

### 1.1 A unidade de análise
No ML, na Shopee e na Amazon o profissional analisa **anúncio × palavra-chave**. No TikTok Shop a venda nasce de uma peça de conteúdo, e a análise passa a ter quatro eixos que se cruzam (síntese desta frente, a partir das seções 2 a 7):

| Eixo | Pergunta | Onde se mede |
|---|---|---|
| Produto | O que vende, a que preço, com que margem depois de comissão? | Seller Center (Data Compass / Análise de dados), ferramentas N5 |
| Criador | Quem vende esse produto, com que constância, com que taxa de entrega de amostra? | Central de Afiliados, filtros de criador, rankings N5 |
| Peça (vídeo ou LIVE) | Qual vídeo ou LIVE converteu, com que CTR, CTOR e GPM? | Análise de vídeo e LIVE do Seller Center, Central de Criativos do GMV Max, N5 |
| Superfície e fonte | A venda veio do feed, da LIVE, da aba Loja, da busca ou da vitrine? De conteúdo próprio, de afiliado ou de Ads? | Seller Center e painel GMV Max (com atribuição sobreposta, ver §6) |

Uma agência dos EUA organiza o painel da mesma forma: separar vídeo, LIVE e cartão de produto/aba Loja, e responder se o conteúdo converte, se os criadores repetem venda e se o canal dá lucro depois de todos os custos. [PRÁTICA] salesduo.com/blog/tiktok-shop-analytics, 2026-09-29 (EUA).

### 1.2 As quatro camadas de dado, adaptadas
A estrutura de `metodo/estado-da-arte.md` §1 vale, com outro conteúdo:

| Camada | No TikTok Shop | Confiabilidade |
|---|---|---|
| 1. Dado próprio (1ª parte) | Seller Center: Data Compass (visão geral, produto, vídeo, LIVE, clientes novos e recorrentes); Central de Afiliados; painel GMV Max e Central de Criativos; relatórios de transbordamento; Off-site Performance Analysis (Pixel) | Alta para a própria conta. Atribuição sobreposta entre orgânico, afiliado e Ads (§6) |
| 2. Estimativa de ferramenta (3ª parte) | Kalodata, FastMoss, EchoTik, Shoplus, Tabcut, Cruva, Hubfluence | Direcional. Erro autodeclarado de ±30% (Cruva); as demais não publicam erro |
| 3. Prateleira e mídia | Flywheel (Share of Search inclui TikTok Shop, ver estado-da-arte §4); TikTok Creative Center | Pouco desenvolvida para o BR |
| 4. Estudos e releases | Newsroom TikTok BR, Momentum Works, eMarketer, estudos da própria TikTok | **Não existe balanço público do TikTok Shop.** Números de escala vêm de release, sem auditoria |

Diferença de método mais importante: no ML e na Shopee há um 8-K ou um relatório da Sea para ancorar. No TikTok Shop BR a plataforma divulga **multiplicadores** (GMV médio diário 102× em um ano), não valores absolutos (§8).

---

## 2. Regras do TikTok Shop Brasil que entram em qualquer diagnóstico [OFICIAL]

Todas lidas na Academy BR em 2026-10-15, com a data que a página mostra.

### 2.1 Custo de vender
- **Comissão da plataforma** (atualizada em 2026-06-12, vigente desde 2026-07-15):
  - item abaixo de R$ 50: 10% + R$ 4 por item (antes: 6% + R$ 4);
  - item de R$ 50 ou mais: 6% + R$ 6 por item (antes: 6% + R$ 4);
  - base: preço depois do desconto do vendedor, sem considerar o desconto da plataforma;
  - incentivo de loja nova: 0% de comissão por 60 dias, teto de R$ 17 mil, condicionado a "missão", vigente desde 2026-03-01.
  [OFICIAL] Academy BR, kid=24428156307201, 2026-06-12. Confirmado por imprensa: economicnewsbrasil.com.br, 2026-09-30; viniensina.com.br/taxas-tiktok-shop, 2026-07-08.
- **Programa de Taxas de Envio** (2026-08-31): 6% sobre pedidos entregues, teto de R$ 50 por produto; inscrição automática, saída opcional; dá selo de frete grátis em vídeo, aba Loja e LIVE e, para qualificados, "tráfego gratuito de anúncios"; a taxa não volta em devolução de pedido enviado; amostras ficam fora. A própria página cita o México numa FAQ, sinal de texto adaptado. [OFICIAL] Academy BR, kid=5665577566734097, 2026-08-31.
- **Comissão de afiliado**, para o criador (2026-07-01): base = preço pago pelo comprador + reembolso do subsídio da plataforma; reembolso parcial reduz a base; pedido cancelado antes do envio ou reembolsado não paga; pagamento depois da liquidação (7, 3 ou 15 dias). [OFICIAL] Academy BR, kid=1517752301717265, 2026-07-01.
- **Comissão de afiliado**, para o vendedor (2026-02-10): taxa definida por produto; **aumento vale na hora, redução só depois de 30 dias** para produto já vinculado; pagamento às quartas. [OFICIAL] Academy BR, kid=2850789359355649, 2026-02-10 **(pode estar superada)**.
- Taxas padrão de colaboração aberta por categoria no BR, vigentes desde 2026-09-23 (exemplo de 4% em celulares e computadores): só em resumo de busca, página oficial não lida. [OFICIAL via terceiro] Tratar como não confirmado.

### 2.2 Take rate efetivo: cálculo desta frente [OBS]
Só com as tabelas acima, sem Ads, sem cupom, sem imposto e sem frete do vendedor:

| Preço do item | Comissão | Tarifa fixa | Programa de envio (6%) | Total da plataforma | % do preço | + afiliado de 15% | % do preço |
|---|---|---|---|---|---|---|---|
| R$ 20 | R$ 2,00 | R$ 4,00 | R$ 1,20 | R$ 7,20 | 36,0% | R$ 10,20 | 51,0% |
| R$ 40 | R$ 4,00 | R$ 4,00 | R$ 2,40 | R$ 10,40 | 26,0% | R$ 16,40 | 41,0% |
| R$ 49,90 | R$ 4,99 | R$ 4,00 | R$ 2,99 | R$ 11,98 | 24,0% | R$ 19,47 | 39,0% |
| R$ 50 | R$ 3,00 | R$ 6,00 | R$ 3,00 | R$ 12,00 | 24,0% | R$ 19,50 | 39,0% |
| R$ 80 | R$ 4,80 | R$ 6,00 | R$ 4,80 | R$ 15,60 | 19,5% | R$ 27,60 | 34,5% |
| R$ 150 | R$ 9,00 | R$ 6,00 | R$ 9,00 | R$ 24,00 | 16,0% | R$ 46,50 | 31,0% |

Leitura de método: a tarifa fixa pesa muito no ticket baixo, e a comissão de afiliado é, de longe, o maior custo variável. Por isso as agências trabalham com margem **depois de comissão de afiliado**, não com a margem de marketplace. A base do Programa de Envio aparece na página ora como "GMV", ora como "preço de venda"; o cálculo usa o preço.

### 2.3 Afiliados, amostras e criadores
- **Colaborações** (2025-04-14): aberta (todos os criadores veem) e direcionada (convite); a plataforma sugere uma porcentagem, a decisão é do vendedor; se o produto está nas duas, vale a comissão da direcionada; até 50 criadores e 100 produtos por convite e 1.000 convites em 24 h. [OFICIAL] Academy BR, kid=6580476438529809, 2025-04-14 **(pode estar superada)**.
- **Amostras grátis** (2026-02-05): custo 100% do vendedor; na aberta, aprovação manual com 7 dias para decidir; na direcionada, manual ou automática; criador tem 14 dias para publicar, vídeo público por pelo menos 3 dias ou LIVE de pelo menos 10 minutos; filtros por GMV de 30 dias, views médias, espectadores de LIVE, tipo de conteúdo, agência ou independente, público; filtro "Criadores confiáveis" = top 20% em proporção de amostra recebida que virou conteúdo. [OFICIAL] Academy BR, kid=6589441682917136, 2026-02-05 **(pode estar superada)**.
- **Classificação de integridade do criador** (CHR, vigente desde 2025-12): 0 a 1.000, começa em 200; a 150 ou menos o criador fica 3 dias sem vídeo ou LIVE com produto e sem campanhas; a 0 perde o comércio. Só o criador vê a nota. [OFICIAL] Academy BR, kid=974093010454289, 2026-01-23 **(pode estar superada)**.
- Requisitos de afiliado: no lançamento, 18 anos, 5 mil seguidores, conteúdo nos últimos 180 dias. [OFICIAL via terceiro] meioemensagem.com.br/midia/tiktok-shop-brasil, 2025-05-08 **(pode estar superada)**. Em 2026-09, uma criadora mostra na tela do app: com 0 seguidores já se gera link de afiliado para compartilhar fora do vídeo; vitrine e produto dentro de vídeo ou LIVE exigem 1.000 seguidores e um vídeo nos últimos 180 dias (antes, 2.000). [PRÁTICA] Mayara Prado, YouTube jkD2gQ5uR-E, 2026-09-09 (mostra tela). Confirmar em N1: as três versões (5 mil, 2 mil, 1 mil) mostram como a regra muda rápido.
- Comissão em outro país: o vendedor define de 1% a 80% nos planos aberto e direcionado (EUA), segundo a Seller University citada por syncly.app, s/d (EUA).

### 2.4 Saúde da conta
- **SPS (Pontuação de desempenho da loja)**, 0 a 5, em Central do vendedor > Integridade da conta. No BR:
  - campanhas exigem SPS de 3,0 ou mais desde abril de 2026; desde agosto de 2026, loja sem SPS precisa não estar penalizada por LDR (entrega atrasada) ou SFCR (cancelamento por culpa do vendedor); duas violações seguidas de SFCR em campanha geram período de cancelamento obrigatório. [OFICIAL] Academy BR, kid=2996214162966289 (FAQ de campanhas), 2026-07-24;
  - um ajuste das regras de cálculo do SPS foi anunciado em março de 2026; o texto não foi lido.
- **SPS nos EUA** (para comparação, não vale como regra BR): seis métricas em três dimensões (avaliação negativa, devolução sem culpa do comprador, cancelamento por culpa do vendedor, entrega no prazo, insatisfação no chat, tempo de pós-venda); nota só depois de 30 pedidos em 90 dias; abaixo de 3,0 a loja perde afiliados e campanhas ativas e só volta a 3,5; CRM congelado entre 3,0 e 3,5. [OFICIAL via terceiro] ppc.land, 2026-06-22 (EUA). Benchmarks relativos à categoria desde 2025-03-13 (EUA/UK) [OFICIAL via terceiro] channelx.world, 2025-03 **(pode estar superada)**.
- Um praticante brasileiro confirma que o acesso ao CRM depende do SPS (acima de 3,5 "elegível") e que loja nova bem operada costuma ter nota 4 nos primeiros 30 dias. [PRÁTICA] Gustavo Cavalini, YouTube wS2Lbc7XSBo, 2026-08-28. Ele também mostra a confusão comum entre o SPS (0 a 5) e a pontuação de violação (0 a 1.000).
- **Pontos de violação do vendedor**: 0 a 1.000, começa em 200; marcos de 150 (7 dias sem novas megacampanhas, listagens e saques), 100 (14 dias), 50 (28 dias + limite de pedidos) e 0 (desativação); pontos deduzidos zeram em 180 dias; ganha 1 ponto a cada 300 pedidos concluídos; retenção de fundos de 90 dias, permanente em fraude; recurso em 30 e 15 dias. [OFICIAL] Academy BR, kid=1444948508641040, s/d **(pode estar superada)**.
- **Loja nova** (2026-04-02): níveis Iniciante (50 pedidos/dia, 1.000 anúncios), Padrão (100), Premium (200), Profissional (ilimitado); pelo menos 30 dias; SPS entre 3,0 e 3,5 em 60 dias; menos de 4 violações em 30 dias; 50 a 100 pedidos entregues e 10 a 20 compradores únicos nos níveis superiores; empresa pode ter 1 conta oficial e 4 de marketing. [OFICIAL] Academy BR, kid=1444948507379472, 2026-04-02 **(pode estar superada)**.

### 2.5 Promoção e LIVE
- **LIVE Flash Sale** (2026-07-18): só conta oficial cria; preço igual ou abaixo do menor preço dos últimos 14 dias (era 30 dias até 2026-01-28); 1 a 180 minutos para conta oficial, 10 minutos a 3 dias para criador; contagem regressiva de 5 minutos obrigatória; prioridade de preço: LIVE Flash Sale > preço de campanha > Flash Sale do vendedor > desconto de produto; exige critério de nota da loja e de pontos de violação. [OFICIAL] Academy BR, kid=5696139560355601, 2026-07-18.
- **Vitrine** do criador: até 2.000 produtos; "organização inteligente" prioriza o que deve vender mais; selos de risco (avaliação negativa, preço acima de concorrentes), benefício (amostra, bônus de comissão) e prazo (proteção de comissão de 30 dias). [OFICIAL] Academy BR, kid=6825383530710785, 2025-04-14 **(pode estar superada)**.

### 2.6 Alimentos e bebidas
- Categoria **só para convidados** pela equipe do TikTok Shop: snacks, laticínios, instantâneos, frescos e congelados, bebidas não alcoólicas, confeitaria; anúncio de vendedor não qualificado é rejeitado; cumprimento da regulação local é responsabilidade do vendedor. Alimento e suplemento infantil (menos de 36 meses) e de gestante também são só para convidados. A página não detalha Anvisa para alimentos (só para cosméticos). [OFICIAL] Academy BR, kid=6504327061473040, 2026-04-30.
- Resumo de busca do domínio oficial indica proibição de perecíveis, alimentos com temperatura controlada, caseiros, aditivos e alcoólicos, e regras de conteúdo (proibido atribuir propriedade medicinal; "superalimento" e "detox" exigem comprovação). [OFICIAL via terceiro] resumo de WebSearch sobre seller-br.tiktok.com (Política de Produtos Proibidos kid=6483182812481296; Política de Conteúdo kid=1413208980588305), não lido na íntegra.
- Categorias do lançamento: beleza e saúde, moda, casa e decoração, eletrônicos e esportes; alimentos não estavam. [OFICIAL via terceiro] mobiletime.com.br, 2025-05-08. Marcas de bebida e suplemento funcional (Desinchá, Guday, Power Focus) aparecem convidadas para a vitrine no lançamento. [DADO] abcdacomunicacao.com.br, 2025-05-21. **[MARCA]**

---

## 3. Como agências, MCNs e ferramentas pesquisam produto, criador, vídeo e LIVE

### 3.1 O que as ferramentas são e o que declaram
| Ferramenta | Módulos declarados | Cobertura e atualização | O que diz da precisão |
|---|---|---|---|
| Kalodata | Produto, loja, criador, vídeo, LIVE; filtro de país (BR disponível, ver 3.3) | Planos com 90, 180 e até 1.000 dias de histórico (Hubfluence, 2026-10-08) | Coleta de "canais públicos" + modelos de IA retreinados diariamente; valores de transação e de gasto em Ads podem divergir do real. [DADO] g2.com/sellers/kalodata, s/d. Site oficial bloqueou a leitura (403) |
| FastMoss | Produto, loja, criador, LIVE, vídeo, Ads (Creative Center), análise de roteiro, otimização de título; API e MCP | "20+ países"; 620 milhões de produtos, 380 milhões de criadores, 1.500 dias de histórico | Só alegação de marketing ("mais precisa"), sem método. [DADO] fastmoss.com, 2026-10-15 |
| EchoTik | Produto, criador, GMV de concorrente | Atualização varia por métrica | Concorrente estimado por sinais de mercado; não vê pedido, reembolso nem taxa alheios. [DADO] echotik.live/blog/how-accurate-is-tiktok-shop-data, 2026-08-07 |
| Shoplus | Produto, criador, vídeo, hashtag e som, loja | Vendas "atualizadas de hora em hora"; país não informado | Só alegação de marketing. [DADO] shoplus.net, 2026-10-15 |
| Tabcut | Produto, criador, vídeo, LIVE, Ads, listas de 1/3/7 dias | Atualização a cada 24 h; países não listados; BR não citado | Diz espelhar "mais de 90%" dos dados do TikTok Shop, sem método. [DADO] tabcut.com, 2026-10-15 |
| Cruva | Produto, marca, criador | Observação diária de links públicos | **±30%** de erro "normalmente", maior conforme a estratégia de afiliados; sub-representa criadores pequenos e vídeos sem link. [DADO] cruva.com/help-center/social-intelligence, s/d |
| Hubfluence | Inteligência social + CRM de afiliados, amostras, campanhas | — | Vende produto concorrente e escreveu o comparativo Kalodata × FastMoss. [DADO] hubfluence.io/blog/kalodata-vs-fastmoss, 2026-10-08 (conflito de interesse) |

Nenhuma ferramenta publica fórmula de estimativa nem erro auditado, como no caso de ML e Amazon (estado-da-arte §9.1).

### 3.2 Fluxo de pesquisa que se repete nos tutoriais
Os tutoriais de ferramenta (EUA e BR) seguem quase sempre a mesma ordem: **produto → criador → vídeo → LIVE → loja concorrente**.
1. **Produto:** ranking por GMV ou unidades em 7 ou 30 dias, filtro de categoria e país; depois a curva diária do produto. [PRÁTICA] [REVENDA] kayomarcellusmkt, YouTube sejE9lVCO1M, 2026-06-26; Carlos Disraeli, MFNkRTC-tzo, 2025-11-16.
2. **Criador:** dentro do produto, ranking de criadores que mais vendem aquele item; depois o perfil do criador (GMV, produtos, vídeos). FastMoss tem ranking de criadores por vendas e ranking de crescimento. [PRÁTICA] Jon Mac, YouTube PsXe_56rr5c, 2026-07-22 (EUA).
3. **Vídeo:** vídeos do produto ordenados por venda; selo "AD" indica que o vídeo roda como anúncio, lido como sinal de que já foi validado. [PRÁTICA] MFNkRTC-tzo.
4. **LIVE:** FastMoss mostra LIVEs com vendas, espectadores e conversão em tempo real. [PRÁTICA] PsXe_56rr5c (EUA).
5. **Loja:** ranking de lojas e página da loja (top produtos, preços, criadores, curva de vendas) para "desmontar" um pico, por exemplo um Super Brand Day. [PRÁTICA] PsXe_56rr5c (EUA).

Critérios explícitos que aparecem:
- **Volume mínimo:** um instrutor brasileiro de afiliados só trabalha produto com pelo menos R$ 200 mil de GMV em 30 dias na ferramenta. [PRÁTICA] [REVENDA] sejE9lVCO1M, 2026-06-26.
- **Janela curta:** preferir 7 dias a 30 dias para não copiar o que já esfriou. [PRÁTICA] MFNkRTC-tzo; sejE9lVCO1M. No exemplo ao vivo, o top 1 de 30 dias caiu para 5º em 7 dias.
- **Curva:** produto "escalado" oscila, mas segue vendendo; pico isolado seguido de queda pode ser ruptura ou fim de viral, e a ferramenta não diz qual. [PRÁTICA] sejE9lVCO1M.
- **Anúncios duplicados:** o mesmo produto aparece em vários anúncios de lojas diferentes; somar ou escolher errado distorce a leitura. [PRÁTICA] sejE9lVCO1M.
- **Quatro filtros para escolher o que estudar:** venda real (não seguidores), momento (subindo), alcançável (não o líder absoluto) e adjacente ao próprio nicho; sinal forte = nº de criadores e vendas subindo juntos. [PRÁTICA] PsXe_56rr5c (EUA).
- **Cadência:** lista de observação semanal de lojas em ascensão; diária durante evento. [PRÁTICA] PsXe_56rr5c (EUA).

### 3.3 O que as ferramentas mostram do Brasil
- Kalodata tem filtro "Brasil". Na tela de 2026-06-26, os cinco produtos de maior GMV em 30 dias (envelopes de figurinha, jogo de panelas, edredom, jaqueta, bicicleta ergométrica) somavam mais de R$ 15 milhões, de ≈ R$ 2,7 a 3,8 milhões cada; o 1º criador em 30 dias, ≈ R$ 2,75 milhões de GMV; o 10º, ≈ R$ 1,46 milhão. [DADO] estimativa Kalodata mostrada em sejE9lVCO1M, 2026-06-26. Faixa N5, com divergência ao vivo entre alunos (um via "1 milhão", outro "3,7 milhões" no mesmo produto).
- Leitura de método vista no mesmo vídeo: o instrutor estima a comissão do criador como GMV × 15% ("média 10% a 15%, alguns 20%"). É regra de bolso sem fonte (N7).

### 3.4 Como agências selecionam criadores
- Na Central de Afiliados, ao aprovar amostra, uma agência dos EUA olha: nota de amostra do criador (posts com amostra, vendas geradas, frequência, qualidade), **taxa estimada de postagem** (só aprova acima de 80%; nunca abaixo de 50%), GMV de 30 dias e views médias; e qual produto precisa de conteúdo nos próximos 30 dias, porque o ciclo amostra → vídeo leva cerca de 4 semanas (3 dias para enviar, 2 semanas para postar, extensão de 1 semana, entrega). [PRÁTICA] BAD Marketing, YouTube 8Ds2F16cGr4, 2026-08-26 (EUA).
- Mesma fonte: colaboração direcionada a 20% é "padrão"; comissão de anúncio (Shop Ads) costuma ser metade da comissão orgânica; loja nova não alcança criador acima de ≈ 20 mil seguidores; o limite de convites semanais cresce até "ilimitado" (≈ 10 mil por semana) e renova no domingo; marca grande (Ninja, EUA) teria enviado 19 mil amostras com aprovação automática no lançamento e mantém mais de 1.000 por mês em manual. [PRÁTICA] 8Ds2F16cGr4 (EUA). Os números de convite e de seguidores não foram confirmados em N1.
- O limite semanal de convites "first-touch" escala com o GMV dos últimos 30 dias, qualquer que seja o software. [PRÁTICA] hubfluence.io, 2026-10-08 (EUA, com conflito de interesse).
- Oferta de taxa fixa por vídeo na colaboração direcionada (EUA): ≈ US$ 100 seria o piso para ter resposta. [PRÁTICA] 8Ds2F16cGr4 (EUA).
- Outra agência dos EUA descreve um sistema em quatro camadas (AD32WdQGXRY, 5x Dashboard, 2026-08-20, EUA):
  - **colaboração aberta como "ímã"**, com amostra **reembolsável** (o criador compra e é reembolsado depois de 2 a 3 pedidos gerados) e comissão de 15% a 20%, calibrada pela comissão que concorrentes pagam (vista em ferramenta);
  - **colher os criadores dos concorrentes:** abrir vídeos de 10 a 15 produtos concorrentes, ou a "análise de afiliados" da loja concorrente numa ferramenta (7, 28 ou 90 dias, ordenada por GMV), e convidar em lote com aprovação manual; a própria fonte diz que raspagem automática viola política;
  - **filtros na Central:** categoria, GMV de 30 dias (ex.: ≥ US$ 1 mil a 5 mil), views médias (≥ 5 mil), taxa de postagem (≥ 70%), nota de amostra (ex.: 92% das amostras viram post);
  - **checagem de 30 segundos por criador:** sinais verdes (vídeo comprável nas últimas 2 semanas, demonstração real, já vendeu na categoria) e vermelhos (último post há mais de 1 mês, views sem curtida ou comentário, "colecionador de amostra" que posta o mesmo formato para 10 marcas na semana).
  - Para amostra, prefere vídeo a LIVE (na LIVE o criador mostra dezenas de produtos); automação de convites só faz sentido no 3º nível de alcance (≈ 7 mil criadores por semana).
  [PRÁTICA] AD32WdQGXRY (EUA). Limites de convite não confirmados em N1; o vídeo termina promovendo ferramentas parceiras.

### 3.5 Como analisam vídeo concorrente
- Fluxo visto no BR: baixar o vídeo top do produto pela ferramenta, pedir a uma IA a estrutura (formato UGC, gancho, ancoragem de preço "menos de R$ 200" contra "R$ 400", demonstração, CTA para o carrinho laranja) e reescrever o roteiro. [PRÁTICA] [REVENDA] sejE9lVCO1M, 2026-06-26. FastMoss vende "análise de roteiro" e "reescrita" como módulo. [DADO] fastmoss.com.
- Sinal de conteúdo fraco no mesmo material: os dois tutoriais brasileiros ensinam a burlar o limite gratuito da ferramenta (e-mail temporário, apagar o bloqueio pelo inspetor do navegador). Isso é violação de termos e rebaixa a fonte, mesmo que o fluxo de pesquisa seja útil (sejE9lVCO1M; MFNkRTC-tzo).

### 3.6 Conteúdo fraco é a maioria
Na busca por tutoriais de ferramenta de 2025-10 a 2026-10, quase todos os títulos prometem "winning products" ou renda: "$90K From 1 Video" (Kalodata US, vR1kLuCNDOo, 2026-07-16); "Brand Grew 706% in One Week" (PsXe_56rr5c); "R$300 Mil de GMV como afiliado em 30 dias" (3nMDgmQSmIg, 2026-06-05); "fiz R$ 20.395,70 em 7 dias só usando IA" (kv99XdyC3bw, 2026-04-24). [OBS] `buscar_youtube.py`, 2026-10-15. O "706%" do vídeo da FastMoss se refere a um Super Brand Day da Free Soul (Reino Unido), não a uma semana orgânica.

---

## 4. Métricas: definições e onde divergem

### 4.1 Tabela de métricas
| Métrica | Definição usada por profissionais | Cuidado |
|---|---|---|
| GMV | Valor bruto transacionado, **antes** de devolução e cancelamento [DADO] echotik.live/blog/tiktok-gmv-tracking, 2026-04-28 | Não é receita. Ferramentas e plataforma às vezes chamam de "receita" (Newsroom BR mistura os termos) |
| Vendas líquidas | GMV − devoluções − cancelamentos | O EchoTik recomenda acompanhar líquido para lucro |
| GPM | GMV por mil visualizações (vídeo) [PRÁTICA] salesduo.com, 2026-09-29 | Há três denominadores em circulação: views, espectadores de LIVE, impressões. Sempre dizer qual |
| CTR do vídeo | % de quem viu que clicou no produto | Views altas com CTR baixo = interesse de compra fraco (salesduo) |
| CTOR | % de cliques no produto que viraram pedido; nome do TikTok em 2026 para a conversão na Análise de tráfego do produto [PRÁTICA] salesduo.com, 2026-09-29 (EUA) | Não confundir com conversão de visita de marketplace |
| Conversão da LIVE | Pedidos ÷ espectadores (ou ÷ cliques no produto, conforme a fonte) | Benchmarks públicos não têm fonte por número (4.4) |
| AOV | GMV ÷ pedidos | — |
| Comissão efetiva | Comissão paga ÷ GMV atribuído ao afiliado; no BR a base inclui o reembolso de subsídio da plataforma e exclui reembolso ao comprador (§2.1) | A taxa anunciada não é a efetiva quando há cupom da plataforma |
| ROI do GMV Max | GMV atribuído à campanha ÷ gasto | Inclui pedidos orgânicos e de afiliado do produto promovido (§6). Não é ROAS de mídia comparável ao Meta |
| ROI de equilíbrio | Preço ÷ margem antes de Ads (margem depois de custo, tarifa, frete e comissão) | Ver 4.2 |
| Custo por pedido (GMV Max) | Gasto ÷ pedidos atribuídos | Mesma sobreposição de atribuição |
| Custo por amostra | Custo do produto + frete de envio (100% do vendedor) | O útil é **custo por amostra que virou conteúdo** = custo das amostras ÷ amostras com post |
| Taxa amostra → post | Amostras com conteúdo publicado ÷ amostras enviadas | A Central mostra "taxa estimada de postagem" por criador (8Ds2F16cGr4, EUA) |
| Criadores ativos | Com ao menos uma venda no dia (definição do TikTok BR) ou com post nos últimos 7 dias ÷ total de afiliados (SFN, EUA) | Duas definições diferentes; sempre dizer qual |
| Concentração | % do GMV de afiliados nos top 1, 5, 10 criadores | Um criador dominante é sinal vermelho (salesduo) |
| ROAS do programa de afiliados | GMV de afiliados ÷ custos do programa (comissão, gestão, amostras, ferramentas) [PRÁTICA] shortformnation.com, 2026-04-24 (EUA) | Metas citadas (5:1, 8:1) sem fonte |
| Margem de contribuição por SKU | Receita − CPV − tarifa − comissão − custo de criador − Ads − promoção − frete − devoluções [PRÁTICA] salesduo; shortformnation | Mesma escada CM1 a CM3 de estado-da-arte §6.1, com uma linha a mais (afiliado) |

### 4.2 Como os praticantes calculam o ROI-alvo do GMV Max
- Método (EUA): calcular o ROI de equilíbrio antes de definir a meta; meta "equilibrada" ≈ 1,5× o equilíbrio e "agressiva" maior. No exemplo do vídeo (preço US$ 30, CPV US$ 6, frete repassado, tarifa de 6%, comissão de anúncio de 10%), as metas foram 2,3 e 3,1. [PRÁTICA] Jon Reiter, YouTube p7BZwvm2Y_c, 2026-07-09 (EUA). Refazendo a conta: margem antes de Ads = 30 − 6 − 1,80 − 3,00 = US$ 19,20; equilíbrio = 30 ÷ 19,20 ≈ 1,56; 1,5 × 1,56 ≈ 2,3; 3,1 ≈ 2× o equilíbrio. [OBS]
- Alternativas que aparecem:
  - usar o ROAS combinado dos últimos 30 dias, ou o valor sugerido pelo TikTok (1,8 no exemplo) [PRÁTICA] ZoCo Marketing, YouTube ciyEKKJPT8c, 2026-08-25 (EUA);
  - aceitar ROI de 1,5 a 2 no início por volume, sabendo que meta alta (10) trava a entrega [PRÁTICA] Gustavo Cavalini, YouTube if50ecS9baI, 2026-02-02 (BR, recorte de mentoria);
  - meta de ROI **por criativo** (ex.: 10) e exclusão dos vídeos abaixo dela com gasto relevante [PRÁTICA] Solum Ecommerce, YouTube EgC3pol8iV4, 2026-07-02 (BR).
- Orçamento mínimo de bolso no BR: preço ÷ 2,5 × 2 (custo de duas vendas por dia a ROAS 2,5). [PRÁTICA] wS2Lbc7XSBo, 2026-08-28. Regra pessoal, sem base.

### 4.3 Divergência sobre o que o ROI do GMV Max desconta
- Um praticante brasileiro afirma que o ROI do GMV Max já desconta tarifa e comissão de afiliado. [PRÁTICA] if50ecS9baI, 2026-02-02.
- O blog oficial pt-BR (2026-05-13) apresenta como recurso **"Pro" em teste** o ROI que considera custo de afiliado, cupom e tarifa, o que sugere que o padrão não desconta. [OFICIAL] ads.tiktok.com/business/pt-BR/blog/gmv-max-automate-shop-roi, 2026-05-13.
- Registro: **contestado**. Conferir a definição na lupa do painel antes de usar o número.

### 4.4 Benchmarks que circulam e por que não usar
- Conversão de LIVE "7,8%" contra 2,1% de anúncio de feed, tempo médio de 22 minutos, tabela por formato de LIVE: aparecem num resumo de busca atribuído ao dashboardly.io, com fonte genérica ("Kalodata, FastMoss, pesquisas com vendedores"). A página aberta em 2026-10-15 não traz esses números e diz que horas de LIVE não equivalem a receita ou conversão. [OBS] dashboardly.io/statistics/tiktok-shop-live-shopping-statistics, 2026-08-08.
- "GPM ideal de US$ 50 a 150 em LIVE": FAQ de blog de ferramenta, sem amostra. [DADO] echotik.live, 2026-04-28.
- Afiliados com "20% a 40% do GMV", "3 a 5× de ROAS", "top 0,5% dos criadores com 38% do GMV": sem fonte rastreável, segundo o próprio artigo que os reúne. [DADO] syncly.app, s/d (EUA).
- Ativação de 12% a 18% de criadores em colaboração aberta, CTR de vídeo de 1,5% a 3,5%, conversão clique → compra de 4,7%: sem fonte. [DADO] shortformnation.com, 2026-04-24 (EUA).
- Posição honesta de uma agência: não existe benchmark único de conversão ou GPM que sirva a todo produto; o ponto de equilíbrio é por SKU. [PRÁTICA] salesduo.com, 2026-09-29 (EUA).

---

## 5. Auditoria de loja TikTok Shop: como as agências estruturam

### 5.1 Frameworks públicos
- **Mapa de métricas** (salesduo, EUA, 2026-09-29): Vendas, Conteúdo, Criador, Atribuição, Eficiência e Halo entre canais.
  - Sinais verdes: GPM cobre o custo do conteúdo na margem-alvo; CTOR acima do equilíbrio do SKU em vários períodos; vários criadores e peças contribuem; contribuição positiva; sabe-se qual superfície está escalando e por quê.
  - Sinais vermelhos: GMV sobe só porque desconto, comissão ou Ads sobem mais rápido que a contribuição; views crescem com CTR, CTOR ou GPM fracos; um criador concentra as vendas; "halo" usado para justificar prejuízo sem base ou holdout; devolução, cancelamento ou ruptura sobem com o volume.
  - Relatório semanal por superfície; checar "vários períodos parecidos", não um pico.
  [PRÁTICA] salesduo.com/blog/tiktok-shop-analytics.
- **Três camadas de afiliados** (SFN, EUA, 2026-04-24): (1) instrumentar (criadores ativos, posts), (2) eficiência (ROAS do programa, margem por SKU, LTV:CAC), (3) atribuição e halo; erro mais comum é acompanhar só GMV e calcular ROAS sobre dado sujo. [PRÁTICA] shortformnation.com.
- **"Não escale Ads antes de arrumar a base"**: tema de auditorias recentes em vídeo (EUA): VGNbKxg9VxY, 2026-10-06; DLWchGwGIZU (loja que gastou US$ 14 mil a ROI 0,5), 2026-10-07. Não transcritos nesta rodada.

### 5.2 Checklist de auditoria (síntese desta frente)
Formato de achado reaproveitado de estado-da-arte §6.1: **evidência → diagnóstico → risco de não agir → próximo passo**, priorizado por risco e impacto.

| Bloco | O que se verifica | Fonte do critério |
|---|---|---|
| 1. Saúde | SPS e subindicadores; pontos de violação; nível de loja nova e limite de pedidos; CHR dos criadores principais (indireto) | §2.4 |
| 2. Economia unitária | Take rate efetivo por faixa de preço; margem depois de afiliado; ROI de equilíbrio; custo por amostra que virou conteúdo | §2.2, §4.2 |
| 3. Mix de fontes do GMV | % de GMV por conta própria (vídeo e LIVE), afiliado (vídeo e LIVE), Ads, cartão/aba Loja | salesduo |
| 4. Conteúdo | Volume de vídeos por produto, % com venda, CTR, CTOR, GPM; fadiga | §4.1; praticantes de GMV Max (25 a 50 vídeos por produto, ver §7.1) |
| 5. Afiliados | Criadores ativos, taxa amostra → post, concentração, comissão efetiva, comissão de anúncio separada da orgânica | §2.3, §3.4 |
| 6. LIVE | Horas, espectadores, conversão, GPM, uso de LIVE Flash Sale | §2.5, §7.3 |
| 7. Ads | Estrutura do GMV Max (produtos por campanha, meta, dias promocionais, aumento automático), exclusão e boost de criativos | §7.1 |
| 8. Catálogo e preço | Faixa de R$ 50, preço contra concorrente (selo de risco na vitrine), conflito com outros canais, regra de 14 dias | §2.1, §2.5 |
| 9. Logística | Entrega no prazo, LDR, SFCR, estoque para pico viral | §2.4 |
| 10. Incrementalidade | O que do GMV atribuído é incremental (holdout, pausa, transbordamento) | §6 |

---

## 6. Incrementalidade entre afiliado, Ads e orgânico

### 6.1 Por que é difícil no TikTok Shop
- **Regra oficial de atribuição do GMV Max:** todos os pedidos de produtos promovidos são atribuídos à campanha, **inclusive os vindos de conteúdo orgânico e de afiliado**; janela de 1 dia para pedido no mesmo dia; vídeos de afiliado autorizados entram automaticamente e recebem rótulo de conteúdo comercial. [OFICIAL] ads.tiktok.com/help/article/about-product-gmv-max, atualizado em 2026-09 (global).
- O próprio TikTok diz que o GMV Max otimiza orgânico e pago "para GMV incremental" e oferece relatórios de transbordamento. [OFICIAL] blog pt-BR, 2026-05-13. Alegação da plataforma, sem desenho de teste publicado.
- Seller Center separa clientes novos e recorrentes por semana ou mês, mas **não por criador, vídeo ou campanha**. [PRÁTICA] Jackie He, tiktok-shop-playbook.beehiiv.com, 2025-04-17 (EUA) **(pode estar superada)**.
- Seller Center, Ads Manager e Central de Afiliados usam janelas e horários diferentes, e o mesmo período mostra ROI diferente em cada painel. [DADO] resumo de busca sobre syncly.app, s/d (EUA).

### 6.2 Evidência disponível (toda de parte interessada)
| Fonte | Desenho | Resultado | Ressalva |
|---|---|---|---|
| TikTok, blog pt-BR, 2026-05-13 | Testes internos de 2025 | "+20% de GMV" com GMV Max | Sem método publicado |
| TikTok, Reino Unido, 2025-11-19 | Impacto causal (contrafactual modelado), 11 clientes de beleza e saúde, gasto ≥ US$ 30 mil, jan/2024 a jun/2025 | +15% de receita média; casos acima de +100% | Sem grupo de controle real, sem intervalo de confiança; não diz se é receita total da loja [DADO] ads.tiktok.com/business/en-GB/blog/how-gmv-max-drives-revenue-gains-tiktok-shop-uk |
| Haus, s/d | Conversion Lift e geo-experimentos (não específicos de TikTok Shop) | Ritual: 0% de lift no 1º teste com atribuição positiva, 8% depois; Newton Baby: +4,14% no DTC e +5,11% na Amazon da mesma região | Fornecedor de testes; casos escolhidos [DADO] haus.io/article/understanding-tiktok-incrementality-testing (EUA) |
| ChannelX, 2026-03-16 | Off-site Performance Analysis do TikTok | Mede vendas no site DTC/Shopify via Pixel; não cobre Amazon nem Walmart | Subestima o transbordamento para marketplace [DADO] channelx.world (país não informado) |
| Newsroom BR, 2026-06-04 | Pesquisa in-app com 17 mil usuários | 57,8% concluem compra no TikTok Shop após descobrir produto no app | Autodeclarado [OFICIAL] |

### 6.3 Desenhos de teste que os profissionais usam
1. **Holdout de produto ou de criativo:** Spark Ads em só metade dos vídeos top, comparando com a outra metade. [PRÁTICA] beehiiv, 2025-04-17 (EUA).
2. **Pausa (switchback):** desligar o GMV Max por alguns dias quando o produto viraliza organicamente (ROI de 70 a 80), para não pagar por venda orgânica. [PRÁTICA] p7BZwvm2Y_c, 2026-07-09 (EUA). Diagnóstico de canibalização: GMV do GMV Max sobe enquanto o total da conta fica parado. [PRÁTICA] coupler.io (resumo de busca), s/d.
3. **Cupom por metade da base:** enviar cupom só para metade da lista quente e comparar. [PRÁTICA] beehiiv.
4. **Conversion Lift Study** do TikTok (controle aleatório no nível de usuário) e **geo-experimento** (regiões; captura também Amazon e loja física, exige dado de venda próprio). Planejar 2 a 4 semanas de teste + 1 a 3 de pós-período; medir só durante a campanha subestima o efeito de vídeo. [DADO] haus.io.
5. **Incrementalidade %** = vendas incrementais estimadas ÷ vendas atribuídas. Exemplo didático: criador com US$ 10 mil atribuídos, 70% dos compradores já seguiam a marca e 50% já tinham comprado → lift estimado ≈ US$ 2 mil. [PRÁTICA] beehiiv (EUA).
6. **Comissão de anúncio menor que a orgânica:** evita pagar mídia e comissão cheia na mesma venda; praticantes usam ≈ metade (ex.: 20% orgânica, 10% em Shop Ads). [PRÁTICA] p7BZwvm2Y_c; 8Ds2F16cGr4 (EUA).
7. **Ruído a controlar:** sazonalidade, mudança de Ads e de CPM produzem o mesmo padrão que canibalização; testar antes de concluir. [DADO] resumo de busca sobre hubfluence.io, 2026-09-29.

Lacuna: não foi achado estudo independente de incrementalidade do GMV Max nem nenhum teste publicado no BR.

---

## 7. O que é próprio de cada alavanca (método dos praticantes)

### 7.1 Ads (GMV Max)
- Hoje toda campanha de venda no TikTok Shop passa pelo GMV Max (Produto ou LIVE); a campanha tradicional com objetivo de venda redireciona para ele. [PRÁTICA] wS2Lbc7XSBo, 2026-08-28. Afiliados também compram tráfego para os próprios vídeos pelo mesmo algoritmo (mesma fonte).
- O GMV Max "puxa" automaticamente todos os vídeos marcados com o produto (próprios e de afiliados autorizados); vídeo de afiliado sem autorização entra por código Spark; um produto só pode estar em uma campanha. [PRÁTICA] if50ecS9baI, 2026-02-02.
- **Volume de criativo antes de ligar:** 25 vídeos na última semana e algum com milhares de views (Jon Reiter, EUA); 3 a 5 ativos por produto no mínimo (ZoCo, EUA); 50 vídeos por produto (Cavalini, BR). Dispersão grande, mesmo princípio: sem vídeos no "pool" a campanha não gasta ou gasta mal.
- **Estrutura:** 1 a 5 produtos por campanha, mesmo nicho/comprador (p7BZwvm2Y_c, EUA); orçamento é teto e só é gasto quando a meta é atingível, por isso praticantes colocam valores altos (if50ecS9baI; ciyEKKJPT8c).
- **Configurações que queimam verba** (ciyEKKJPT8c, EUA): "dias promocionais" vem ligado e pode multiplicar o orçamento (até 10× com +50%); aumento automático de orçamento; proteção de ROI exige ≈ 20 conversões por dia; cupom automático de 3% a 10% deve ficar desligado até haver linha de base.
- **Ciclo de vida do criativo:** em análise → aprendizado → entrega → não entrega (fadiga); a campanha "seca" sem vídeos novos diários. [PRÁTICA] p7BZwvm2Y_c (EUA).
- **Otimização por criativo:** excluir vídeos com gasto relevante abaixo do ROI-alvo; dar "boost" (verba mínima por vídeo) aos de ROI alto e gasto baixo. Case citado: R$ 12 mil de gasto em 3 meses, ≈ 3.600 vendas, ≈ R$ 194 mil de GMV, ROI ≈ 15, 367 criativos num produto de ≈ R$ 50. [CASE] EgC3pol8iV4, 2026-07-02 (sem base de comparação e com oferta de agência: tratar como [PRÁTICA]).
- **Regra de manutenção:** mudar orçamento com frequência, meta raramente, produtos quase nunca; se não gasta, baixar a meta e postar mais. [PRÁTICA] p7BZwvm2Y_c (EUA).

### 7.2 Afiliados
- Os profissionais tratam afiliados como o motor de criativos do GMV Max, não só como canal de venda (p7BZwvm2Y_c; ciyEKKJPT8c, ambos EUA).
- Sequência típica de marca nova (EUA): aprovação automática nas primeiras centenas de amostras, depois manual e seletiva; um produto principal por vez; 20% de comissão direcionada; comissão de anúncio separada. [PRÁTICA] 8Ds2F16cGr4.
- Escala vista no BR: BigHome com média de 300 afiliados ativos com venda nos últimos 28 dias; Moderna com mais de 9 mil afiliados ativos. [CASE] newsroom.tiktok.com, 2026-06-04 (dado da plataforma, sem auditoria).
- Contraponto de praticante: 85% a 90% do conteúdo orgânico de TikTok Shop rende pouco GMV direto, e o valor estaria no transbordamento e na biblioteca de criativos. [PRÁTICA] Dan Albert (456 Growth), superfiliate.com, s/d. Opinião, não medida.

### 7.3 LIVE
- No BR, GMV médio diário de LIVEs cresceu 161× e o nº diário de LIVEs 20× entre maio de 2025 e maio de 2026; LIVEs que mais vendem se concentram em cosméticos e cozinha. [OFICIAL] newsroom.tiktok.com, 2026-06-04.
- Cases do BR (todos da plataforma, sem base independente): Natura com 52 mil LIVEs em 2025, 60% feitas por consultoras; mega LIVE de 12 horas com +228% de conversão de carrinho abandonado; Johnson's Baby com 727 horas de LIVE de afiliados; criadora com R$ 2,4 milhões de R$ 2,8 milhões de GMV vindos de LIVE; recorde latino-americano de US$ 100 mil numa LIVE (BigHome). [CASE] newsroom.tiktok.com, 2026-06-04. Criador especialista com R$ 1,2 milhão de GMV acumulado e LIVE de 12 horas com R$ 108 mil. [CASE] consumidormoderno.com.br, 2025-11-05.
- Ferramentas de LIVE usadas no método: LIVE Flash Sale (regra de 14 dias, §2.5), LIVE GMV Max (Controle de LIVE, Modo Mega LIVE, Vídeo para LIVE) [OFICIAL] blog pt-BR, 2026-05-13; lembrete de LIVE e evento de LIVE pelo CRM. [PRÁTICA] wS2Lbc7XSBo.
- Referência de escala fora do BR: QVC com cerca de 220 horas de LIVE por semana no TikTok Shop (EUA). [PRÁTICA] PsXe_56rr5c, 2026-07-22. Momentum Works publica "Live Commerce in Southeast Asia 2026" (pago, não lido). [DADO] momentum.asia, 2026-09.

### 7.4 Conteúdo de marca para venda por descoberta
- Uma empresária de moda brasileira (vende em ML, TikTok Shop, site, afiliados) resume o método de seleção de produto para o TikTok em seis perguntas: prende atenção?, resolve uma dor de forma visual?, que cena mostra o valor em segundos?, que objeção impede a compra?, que criador demonstraria com naturalidade?, a operação aguenta se o vídeo vender? Critério que ela acrescenta e que não aparece em marketplace de busca: **capacidade de repetição** (o produto rende muitos vídeos e ângulos, para a marca e para os afiliados). [PRÁTICA] [MARCA] LV Talks (Letícia Vaz), YouTube j2QrA7_x45w, 2026-05-07.
- Mesma fonte: estrutura de vídeo em três funções (parar a rolagem nos primeiros segundos, tornar o benefício visível, derrubar a objeção no próprio vídeo); "10 ângulos" (transformação, dor cotidiana, demonstração, prova social, comparação, objeção, ocasião de uso, bastidor, curiosidade, oferta); comentários como "laboratório" (objeção, desejo, comparação, uso viram vídeos novos); volume próprio de vídeos e de vendas atrai afiliados ("bola de neve"); atraso de entrega gera punição e menos exposição. Afirma que 1 em cada 20 vídeos dá certo, sem dado. O episódio é patrocinado por um banco (conflito declarado no próprio vídeo).

### 7.5 CRM e avaliações
- O CRM do TikTok Shop dispara mensagens no chat do Shop (não no direct): 4 disparos manuais por semana, públicos não reutilizáveis, planos automáticos (carrinho, LIVE, pós-compra) que expiram em ≈ 30 dias; acesso depende do SPS. [PRÁTICA] wS2Lbc7XSBo, 2026-08-28.
- Mesma fonte: o uso de maior efeito foi pedir avaliação com cupom; a recuperação de carrinho mostrava dezenas de milhares "recuperados" sem mudar o GMV do mês. Exemplo de **atribuição sem incrementalidade** relatado pelo próprio praticante.

---

## 8. Contexto de mercado (o pano de fundo que os profissionais usam)

- **Lançamento:** 2025-05-08, com cinco categorias, checkout no app (cartão, Pix, boleto), logística supervisionada pelo TikTok com parceiros como os Correios, abertura de loja sem custo. Divergência: 12º país (Meio & Mensagem) ou "14 países" (Mobile Time). [OFICIAL via terceiro] meioemensagem.com.br e mobiletime.com.br, 2025-05-08.
- **Primeiro ano (maio/2025 a maio/2026):** GMV médio diário mensal 102×; criadores afiliados ativos (com venda no dia) 46×; 134 milhões de usuários no BR; mais vendidos por subcategoria (calças femininas, bodysplash, panelas, fones). [OFICIAL] newsroom.tiktok.com/tiktok-shop-cresce-102-vezes-em-seu-primeiro-ano-no-brasil, 2026-06-04. Sem valor absoluto.
- **Maio a setembro de 2025:** GMV médio diário 26×, vendedores com venda mensal 11×, criadores 12×; cinco transportadoras homologadas. [OFICIAL via terceiro] consumidormoderno.com.br, 2025-11-05.
- **Black Friday 2025:** GMV de 28/11 +129% contra o 10/10; GMV de LIVE +143%. [OFICIAL via terceiro] resumo de busca (Meio & Mensagem e Mercado & Consumo), 2025-12.
- **Black Friday 2026:** de 27/10 a 12/12, etapa principal de 19 a 30/11, R$ 100 milhões em cupons, até 12× sem juros. [DADO] economicnewsbrasil.com.br, 2026-09-30.
- **EUA, para escala:** vendas de US$ 15,82 bilhões em 2025, +108%, 18,2% do social commerce (eMarketer, via syncly.app); US$ 11,8 bilhões no 1º semestre de 2026, +103% (Momentum Works, via salesduo). Fontes divergem muito sobre o GMV global. [DADO] (EUA)
- **Relatório pago com BR:** "TikTok Shop in the U.S. & Brazil H1 2026" (Momentum Works, 2026-08). Não lido. [DADO]

---

## 9. Revenda × marca própria no TikTok Shop

| Tema | **[REVENDA]** (revenda, dropshipping, afiliado puro) | **[MARCA]** (indústria, marca própria) |
|---|---|---|
| Pergunta central | "Que produto está estourando e como pego a onda?" | "Como faço criadores e LIVE venderem a minha marca com margem, e o que é incremental?" |
| Ferramentas | Kalodata, FastMoss, Tabcut, Shoplus em modo "produto vencedor" | Seller Center (Data Compass, Afiliados, GMV Max), Central de Criativos, rankings N5 para concorrência, testes de lift |
| Métricas de entrada | GMV de 7 e 30 dias do produto, curva, nº de criadores, vídeo com selo AD, comissão oferecida | Margem depois de afiliado, taxa amostra → post, concentração de criadores, % de novos clientes, transbordamento |
| Unidade de análise | Produto e vídeo | Marca, SKU herói, programa de afiliados, LIVE própria |
| Ads | GMV Max para "pegar" um viral; afiliado comprando tráfego para o próprio vídeo | GMV Max com ROI de equilíbrio por SKU, comissão de anúncio separada, holdout |
| Risco típico | Fim do viral, ruptura, anúncio duplicado, violação de termos | Canibalização com outros canais, dependência de um criador, alegação de conteúdo (alimentos, cosméticos), categoria só para convidados |
| Fontes | §3.2, §3.3, §3.5 | §2, §5, §6, §7 |

Vale para os dois: take rate efetivo (§2.2), SPS e pontos de violação, ciclo amostra → vídeo de ≈ 4 semanas, atribuição sobreposta do GMV Max.

---

## 10. Lacunas e cuidados desta frente
1. Nenhuma ferramenta publica método de estimativa; só a Cruva declara erro (±30%). Cobertura e histórico do BR nas ferramentas não foram confirmados em página oficial (só em tela de tutorial).
2. A regra de cálculo do SPS no BR (ajuste de março de 2026) não foi lida; o que se sabe de subindicadores e limites é dos EUA.
3. Tabela de taxas padrão de comissão por categoria (2026-09-23) não lida na fonte.
4. Não há benchmark com fonte de CTR, CTOR, GPM, conversão de LIVE ou ROI de GMV Max para o BR, nem robusto para outro país.
5. Nenhum teste de incrementalidade do TikTok Shop publicado no BR; os estudos existentes são da plataforma ou de fornecedores.
6. O TikTok não divulga GMV absoluto do BR; relatórios independentes (Momentum Works) são pagos.
7. A definição do ROI do GMV Max (desconta ou não tarifa e afiliado) é contestada entre praticante e blog oficial.
8. Kalodata (site) e eMarketer bloquearam a leitura (403). Índice da Academy BR exige JavaScript.
9. Vídeos de auditoria (DLWchGwGIZU, VGNbKxg9VxY) não foram baixados; os de LIVE (3rEXumkmN30), de agência (U3-7SyOleMM) e dois tutoriais de Kalodata (Q2m0gPCQxAg, rA2nsDx7-Jg) ficaram sem legenda em português (limite 429 do YouTube). LIVE é a frente com menos método documentado nesta rodada.

---

## 11. Índice de fontes (por tipo)

[OFICIAL]
- TikTok Shop Academy BR (`seller-br.tiktok.com/university/essay?knowledge_id=`): 24428156307201 (tarifa, 2026-06-12); 5665577566734097 (Programa de Taxas de Envio, 2026-08-31); 2850789359355649 (regras de comissão, 2026-02-10); 1517752301717265 (comissão para criadores, 2026-07-01); 6580476438529809 (colaborações, 2025-04-14); 6589441682917136 (amostras, 2026-02-05); 974093010454289 (integridade do criador, 2026-01-23); 1444948508641040 (fiscalização, s/d); 1444948507379472 (loja nova, 2026-04-02); 2996214162966289 (FAQ de campanhas, 2026-07-24); 5696139560355601 (LIVE Flash Sale, 2026-07-18); 6825383530710785 (vitrine, 2025-04-14); 6504327061473040 (produtos restritos, 2026-04-30)
- ads.tiktok.com/help/article/about-product-gmv-max (2026-09)
- ads.tiktok.com/business/pt-BR/blog/gmv-max-automate-shop-roi (2026-05-13)
- newsroom.tiktok.com/tiktok-shop-cresce-102-vezes-em-seu-primeiro-ano-no-brasil (2026-06-04)

[OFICIAL via terceiro]
- ppc.land/tiktok-shops-hidden-score-that-can-freeze-your-affiliate-access (2026-06-22, EUA)
- meioemensagem.com.br/midia/tiktok-shop-brasil (2025-05-08); mobiletime.com.br/noticias/08/05/2025/tiktok-shop-no-brasil (2025-05-08); consumidormoderno.com.br/tiktok-shop-brasil-operacao (2025-11-05)
- channelx.world/2025/03/tiktok-shop-launch-product-listing-category-based-benchmarks (2025-03)

[DADO]
- ads.tiktok.com/business/en-GB/blog/how-gmv-max-drives-revenue-gains-tiktok-shop-uk (2025-11-19, Reino Unido)
- haus.io/article/understanding-tiktok-incrementality-testing (s/d, EUA)
- channelx.world/2026/03/tiktok-off-site-performance-analysis-to-measure-incremental-sales (2026-03-16)
- cruva.com/help-center/social-intelligence/social-intelligence-data (s/d)
- echotik.live/blog/how-accurate-is-tiktok-shop-data (2026-08-07); echotik.live/blog/tiktok-gmv-tracking (2026-04-28)
- g2.com/sellers/kalodata (s/d); fastmoss.com; shoplus.net; tabcut.com (acesso 2026-10-15)
- hubfluence.io/blog/kalodata-vs-fastmoss (2026-10-08, conflito de interesse)
- syncly.app/blog/tiktok-shop-affiliate-roi-in-what-the-data-actually-shows (s/d, EUA)
- dashboardly.io/statistics/tiktok-shop-live-shopping-statistics (2026-08-08)
- economicnewsbrasil.com.br/2026/09/30/taxas-tiktok-shop-black-friday-lojistas (2026-09-30); viniensina.com.br/taxas-tiktok-shop (2026-07-08)
- abcdacomunicacao.com.br/tik-tok-shop-mira-no-segmento-de-saude-e-bem-estar-no-brasil (2025-05-21)
- momentum.asia (listagem de relatórios, 2026-10-15)

[PRÁTICA]
- salesduo.com/blog/tiktok-shop-analytics (2026-09-29, EUA)
- shortformnation.com/blog/tiktok-shop-affiliate-analytics-what-to-track-and-why-most-programs-get-it-wrong (2026-04-24, EUA)
- tiktok-shop-playbook.beehiiv.com/p/are-your-tiktok-shop-sales-actually-incremental (2025-04-17, EUA)
- superfiliate.com/field-guide/video/measuring-tiktok-shop-performance-by-dan-albert (s/d)
- YouTube: p7BZwvm2Y_c (Jon Reiter, 2026-07-09, EUA); ciyEKKJPT8c (ZoCo Marketing, 2026-08-25, EUA); 8Ds2F16cGr4 (BAD Marketing, 2026-08-26, EUA); AD32WdQGXRY (5x Dashboard, 2026-08-20, EUA); j2QrA7_x45w (LV Talks, 2026-05-07); jkD2gQ5uR-E (Mayara Prado, 2026-09-09); PsXe_56rr5c (Jon Mac/FastMoss, 2026-07-22, EUA); if50ecS9baI (Gustavo Cavalini, 2026-02-02); wS2Lbc7XSBo (Gustavo Cavalini, 2026-08-28); EgC3pol8iV4 (Solum Ecommerce, 2026-07-02); sejE9lVCO1M (kayomarcellusmkt, 2026-06-26); MFNkRTC-tzo (Carlos Disraeli, 2025-11-16)

[CASE]
- newsroom.tiktok.com (2026-06-04): Natura, Johnson's Baby, Riachuelo, BigHome, Moderna, criadoras
- consumidormoderno.com.br (2025-11-05): Granado, Vittare Home, Diogo Bottino

[OBS]
- Cálculo de take rate (§2.2) e de ROI de equilíbrio (§4.2) a partir das fontes citadas
- Busca de YouTube por `buscar_youtube.py` (365 dias, 2026-10-15): títulos usados como exemplos de conteúdo fraco (vR1kLuCNDOo, 3nMDgmQSmIg, kv99XdyC3bw, vrRXBSD-jRg)
