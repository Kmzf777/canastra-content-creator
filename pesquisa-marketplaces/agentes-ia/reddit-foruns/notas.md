# Agentes de IA em contas de marketplace: Reddit e fóruns

Pesquisa de 19/10/2026. Frente: Reddit, Hacker News, fóruns de vendedores e Indie Hackers.

**Como foi feita.** O Reddit bloqueia o WebSearch e o WebFetch (`reddit.com` e `old.reddit.com` dão
403). Os posts e comentários vieram do arquivo público Arctic Shift
(`arctic-shift.photon-reddit.com`), que espelha o Reddit; os links abaixo apontam para o Reddit
original. A busca no arquivo ficou lenta e com limite de requisições, então a cobertura é
parcial: entraram bem r/FulfillmentByAmazon, r/AmazonFBA, r/AmazonSeller, r/AI_Agents,
r/ecommerce, r/n8n, r/TikTokShop, r/brdev e r/empreendedorismo; ficaram de fora ou quase
r/ClaudeAI, r/shopify, r/Etsy, r/eBay, r/Walmart e r/LocalLLaMA (a busca expirou). Os fóruns
entraram por WebSearch e WebFetch. ecomcrew.com e indiehackers.com bloquearam (520 e 403).

**Legenda.** [PRÁTICA] = alguém conta como faz. [CASE] = relato de resultado de quem fez.
[DADO] = número. [OFICIAL] = da plataforma. [OPINIÃO] = juízo sem experiência relatada.
**MKT** = quem escreve vende ferramenta ou serviço ligado ao assunto (o r/FulfillmentByAmazon
bane autopromoção, e mesmo assim boa parte dos posts é isso).

---

## (a) Resumo: o que mais se repete

1. Quase ninguém deixa o agente mexer sozinho na conta. Primeiro ele só lê e sugere, você aprova cada mudança, e só depois de semanas (2 a 4, ou "um bom tempo") a automação se solta, e só nas ações baratas de desfazer.
2. Ninguém divide os agentes por marketplace: divide por função (lances, estoque, estratégia, listing, atendimento). Por cima vai uma única base de fatos (SOPs, metas, margens, voz da marca) que todos leem, e o "cérebro único gigante" é apontado como erro.
3. A trava que mais se recomenda é o tamanho do estrago, não a porcentagem: quanto dinheiro sai se a mudança estiver errada por 24 h. Negativar termo, pausar o que não converte e dayparting podem ser automáticos. Subir lance ou verba passa sempre por aprovação.
4. Os dados vêm de API oficial (SP-API, Ads API, MCP da Amazon Ads) ou de CSV exportado. Quem já construiu diz que a API deve alimentar um banco local com o histórico, e o agente lê esse banco; o agente consultando a API ao vivo não funciona (limite de requisições, relatórios espalhados, timeouts).
5. Faltam duas coisas ao agente: memória e contexto do negócio. Sem um log do que já mudou, ele mexe de novo no lance de três dias atrás. Sem margem e estoque, ele propõe lance que bate o ACoS mas quebra o estoque. A janela de atribuição atrasada faz o agente cortar demais.
6. O que funciona é o descritivo: resumir relatório de termos, achar gasto sem conversão, auditar listing, relatório semanal, alerta de estoque. O que derrapa é o prescritivo: lances, negativos em broad (houve caso de propor matar um termo que trazia 30% das conversões) e reestruturação de campanhas.
7. O que mais quebra é a manutenção, não a capacidade do modelo: a Amazon muda o formato de um relatório, o token OAuth expira à noite, o endpoint muda sem aviso. O sistema "funciona na semana 1 e encolhe em silêncio". Vários migram cada vez mais lógica para regras fixas e deixam o modelo com menos.
8. A stack mais citada: Claude (Cowork, Claude Code, Claude in Chrome) com MCP (oficial da Amazon Ads, Helium 10, agentcentral, Seller Labs) e n8n ou Zapier para agendar, com aviso no Slack e aprovação num clique. Custo relatado de US$ 20 a 117 por mês (assinatura + MCP) para um operador e de US$ 200 a 500 por mês para um agente próprio via API.
9. Regra nova: desde 4/3/2026 o contrato da Amazon (BSA, Seção 19, "Agent Policy") obriga todo software automatizado ou agente de IA que acessa a Amazon a se identificar como automatizado e a parar quando a Amazon pedir. Comentaristas incluem nisso automação de navegador e scraping, que é o caminho do Claude in Chrome. Em 23/9/2026 a Amazon lançou um plugin oficial Selling Partner para o Claude (beta nos EUA).
10. Os números de resultado que circulam (ACoS de 25% para 14%, CVR 19%, +17% orgânico, 15% de economia em ads) são quase todos autodeclarados, muitos por quem vende o serviço. Brasil (Mercado Livre e Shopee): quase não há relato de agente operando conta. O que aparece são dúvidas de OAuth e API, bots de afiliado e respondedores de perguntas vendidos como SaaS. É uma lacuna.

---

## (b) Os 6 temas

### 1. Arquitetura

- **Por função, não por canal.** O relato mais detalhado vem de um vendedor que roda há meses um
  sistema com agentes separados de lances, estoque e estratégia, com regras de prioridade para
  resolver conflito entre eles (u/ScribbleSpark,
  [r/FulfillmentByAmazon](https://www.reddit.com/r/FulfillmentByAmazon/comments/1v93na7/codex_vs_claude_code_for_ppc/)).
  Outro diz que roda "11 agentes" para a própria conta, que decidem juntos e priorizam pelo
  impacto projetado (u/k_abderezak,
  [r/AmazonFBA](https://www.reddit.com/r/AmazonFBA/comments/1vksrdx/almost_300kmo_claude_automations/)).
  Um terceiro tem 2 lojas Shopify com cerca de 11 agentes em Claude Code e MCP (e-mail, PR, SEO,
  atendimento) ([r/AI_Agents](https://www.reddit.com/r/AI_Agents/comments/1tje1aq/help_ai_agents_for_ecommerce_whats_actually/)).
- **O "cérebro" é compartilhado e a execução é estreita.** "Uma base única (SOPs, voz da marca,
  avatares, decisões passadas) que todo agente lê, e cada agente dono de um domínio estreito." A
  análise de ads roda como tarefa diária agendada e grava as conclusões na base; o agente
  criativo lê essas conclusões depois (mesma thread). O contraponto: "o cérebro gigante virou
  pesadelo de manutenção; cada fluxo com só o contexto de que precisa" (u/Winter_Hovercraft438).
- **Orquestração com regras fixas, não agente livre.** "Arquiteturas de orquestração de workflow
  (passos agendados e limitados, cola determinística em volta do modelo) ganham de agentes
  autônomos na maioria dos casos reais" (u/PrismByCI, que diz construir produto,
  [r/AmazonFBA](https://www.reddit.com/r/AmazonFBA/comments/1smcv6q/what_we_learned_trying_to_build_the_nondiy/)).
- **Memória e estado.** Uma planilha de metas por conta (ACoS, TACoS, vendas, verba) que o agente
  sempre consulta, mais o Asana para ver a última conversa com o cliente (u/mazescale,
  [r/AmazonFBA](https://www.reddit.com/r/AmazonFBA/comments/1wam54y/claude_for_ppc/)). Um log de
  mudanças que o agente lê antes de decidir (u/Anis-SellerPPC, mesma thread). O CLAUDE.md como
  "constituição", com arquivo de contexto do negócio, log de decisões e rotina de manutenção
  ([r/ecommerce](https://www.reddit.com/r/ecommerce/comments/1u43jbb/ecommerce_owners_running_their_store_on_cowork/),
  post que foi acusado de captar leads). Uma pasta por função de negócio, cada uma com seu
  CLAUDE.md e um .md por SOP (u/Milan_SmoothWorkAI, r/AI_Agents 1tje1aq). Memória numa célula
  de planilha que o fluxo reescreve todo dia a partir das métricas do que publicou
  ([r/n8n](https://www.reddit.com/r/n8n/comments/1w14m58/a_selfimproving_tiktok_workflow_that_rewrites_its/)).
- **Rotina e gatilhos.** Auditoria semanal com sugestões para aprovar (u/mazescale). Negativar
  termos passou de "tarefa de sexta" a diária; lances em passadas menores e mais frequentes
  ([agência, r/FulfillmentByAmazon](https://www.reddit.com/r/FulfillmentByAmazon/comments/1ti5a9c/anyone_elses_agency_or_inhouse_team_moving_to/)).
  Busca mensal no relatório Search Query Performance (u/Working_Attention_66). Alerta de estoque
  que rascunha o pedido de compra no Slack para aprovação num clique
  ([r/FulfillmentByAmazon](https://www.reddit.com/r/FulfillmentByAmazon/comments/1thu9ni/inventory_management_automation_to_prevent_fba/)).
  Plano específico de BFCM: o Claude calcula vendas por sessão de cada ASIN em cada dia e mostra
  as exceções antes da subida em massa
  ([r/FulfillmentByAmazon](https://www.reddit.com/r/FulfillmentByAmazon/comments/1wy6nr3/bfcm_is_coming_heres_how_we_plan_to_claude_our/)).
- **"Isso não é agente."** No r/AmazonFBA, um fluxo n8n + GPT que reescreve listings toda semana
  foi corrigido: "isso é automação de workflow; agente decide sozinho"
  ([thread](https://www.reddit.com/r/AmazonFBA/comments/1luu1uo/17_jump_in_organic_sales_in_4_weeks_using/)).

### 2. Acesso aos dados

- **API oficial.** SP-API e Ads API, cujo acesso é gratuito para uso próprio de marca registrada.
  Um vendedor diz que app para revenda custa US$ 1.400 por mês (não confirmado,
  [r/AmazonFBA](https://www.reddit.com/r/AmazonFBA/comments/1sk2dxx/claude_to_seller_central/)).
  O SQP do Brand Analytics pede um papel de API à parte e é um ASIN por chamada; tudo divide a
  mesma cota, e o estouro aparece como timeout silencioso (u/ScribbleSpark). Um aviso de que os
  relatórios antigos da Ads API saem em dezembro em favor da "unified ads API" (u/LostMyMilk,
  r/FulfillmentByAmazon 1v93na7).
- **MCP da Amazon Ads.** Open beta em 2/2/2026; cobre campanhas, relatórios e lances, mas só para
  quem tem credencial ativa da Ads API. "A barreira é a aprovação, não o preço"
  ([r/FulfillmentByAmazon](https://www.reddit.com/r/FulfillmentByAmazon/comments/1w3j3tm/mcp_connection_for_adspend_via_claude/)).
  Avaliação de usuário: "o MCP da Amazon é grátis mas péssimo; uso o agentcentral" (mesma thread).
  MCPs de terceiros citados: Helium 10, Seller Labs, agentcentral, Clickstera, HectorAI, sellerppc
  (MKT) e dragonbot (MKT).
- **Banco local antes do agente.** "A SP-API é fonte de dados, não camada de consulta ao vivo
  para um agente"; quem montou um data warehouse com SP-API, Ads API e Marketing Stream diz que
  "é MUITO" (u/Chrolm, r/FulfillmentByAmazon 1v93na7; repete em
  [r/AmazonFBA](https://www.reddit.com/r/AmazonFBA/comments/1th4777/10k_to_74kmo_in_11_months_claude_automation_for/)).
  Outro: "bater direto nas APIs da Amazon não funciona, os dados não ficam num lugar só; ou
  espelha um CSV, ou um MCP onde você guarda os dados" (r/AmazonFBA 1vksrdx).
- **CSV exportado.** Para quem só quer gasto e ACoS, basta exportar e apontar o Claude para o CSV
  ("você tem isso esta semana", r/FulfillmentByAmazon 1w3j3tm). É o caminho de quem começa.
- **Navegador e computer use.** Um vendedor no plano Pro usou a extensão do Claude com o Claude
  Desktop: "auditou inventário, listings, PPC e relatórios… pedi para corrigir e ele literalmente
  assumiu meu computador e foi editando a conta"
  ([r/AmazonFBA](https://www.reddit.com/r/AmazonFBA/comments/1sk2dxx/claude_to_seller_central/)).
  A pergunta que veio logo em seguida ficou sem resposta: "é seguro ligar isso ao computador
  inteiro e à conta?". Outro relata a API "quebrando sem parar" ao usar o Amazon Pi (Índia) com a
  extensão do Chrome
  ([r/FulfillmentByAmazon](https://www.reddit.com/r/FulfillmentByAmazon/comments/1vl9yvv/has_anyone_used_amazon_pi_with_claude_chrome/)).
  E alguém afirma, sem fonte, que "é contra os termos usar o Claude Cowork ali"
  ([r/FulfillmentByAmazon](https://www.reddit.com/r/FulfillmentByAmazon/comments/1vacdxx/how_are_you_using_ai_on_amazon_ive_been_using/)).
  Ver a Agent Policy no tema 3.
- **Mercado Livre.** No r/n8n e no r/brdev só aparece dificuldade: OAuth2 com PKCE quebrando no
  n8n ([thread](https://www.reddit.com/r/n8n/comments/1qyruuf/ajuda_erro_de_oauth2_no_n8n_com_mercado_livre_pkce/)),
  sessão por cookie que expira no Browserless numa VPS no exterior, com a recomendação de usar a
  API oficial ([thread](https://www.reddit.com/r/n8n/comments/1wp2uzp/n8n_mercado_livre_browserless_api/)),
  erro 403 e atributos obrigatórios que não vêm marcados
  ([r/brdev](https://www.reddit.com/r/brdev/comments/1sz5tyd/)) e mapeamento de atributos entre
  ML e Shopee num integrador de "anúncio mestre"
  ([r/brdev](https://www.reddit.com/r/brdev/comments/1skab8n/)). O MCP "oficial" do ML só busca na
  documentação; não lê pedidos nem campanhas
  ([Kondado, MKT](https://kondado.com.br/blog/a/mercado-livre-no-chatgpt-e-claude-mcp)). Existe um
  MCP comunitário (Algoritmo Digital, Argentina) com 33 ferramentas, 3 de escrita (preço,
  estoque, título, responder pergunta) que exigem confirmação, e `ALLOW_WRITE=0` para deixar só
  leitura; tinha 0 estrelas ([GitHub](https://github.com/kokesaurio/mercadolibre-algoritmodigital)).

### 3. Autonomia e travas

- **Primeiro só sugere, depois soltar aos poucos** (consenso). "Não deixe executar sozinho no
  começo; o histórico de aprovar e descartar é a parte mais valiosa, porque é com ele que você
  ajusta as regras" (u/ScribbleSpark). "Use semanas lado a lado, depois transforme as decisões
  repetidas num livro de regras, inclusive de quando ele deve te perguntar" (u/Chrolm). "Deixe
  ler tudo, inclusive ads. Nunca deixe aplicar. Se aplicar for um passo que ele fisicamente não
  pode pular, uma leitura errada custa uma sugestão ruim, não uma conta ruim" (u/Gold-Carpenter-4066,
  r/AmazonFBA 1vksrdx).
- **Travas concretas relatadas.** Humano aprova acima de certo delta de lance ou mudança de verba
  (agência, r/FulfillmentByAmazon 1ti5a9c); aprovação manual de mudança de lance acima de 15%
  (Google Ads, mesma thread). Gatilho pelo raio de estrago (US$ expostos em 24 h) e pelo tipo de
  ação: negativos, pausas e dayparting são reversíveis e automáticos; subir lance ou verba,
  sempre com portão. "Logue toda decisão com o motivo, não para o agente, para você"
  (u/AttentionMediocre537, mesma thread). Preço mínimo nunca é decidido pelo Claude: custo +
  taxas + lucro mínimo, calculado em planilha; "não siga o mercado para baixo do piso"
  ([r/FulfillmentByAmazon](https://www.reddit.com/r/FulfillmentByAmazon/comments/1wgm6kn/how_do_you_calculate_min_prices_in_bulk_for/)).
  Atendimento no modelo rascunho e fila: o agente nunca envia sem o "aprovar" humano. São 6
  clientes por dia × 2 min = 12 min, contra 1 h escrevendo do zero (u/BrightExcitement9454,
  r/AI_Agents 1tje1aq). Exigir 2 ou mais fontes que confirmem antes de aceitar um padrão que o
  agente diz ter achado (mesmo relato).
- **[OFICIAL] Agent Policy da Amazon (BSA, Seção 19), em vigor desde 4/3/2026.** "Todos os
  agentes de IA devem identificar-se claramente como sistemas automatizados, cumprir a nova Agent
  Policy o tempo todo e cessar o acesso se a Amazon pedir"
  ([anúncio no Seller Forums](https://sellercentral.amazon.com/seller-forums/discussions/t/84e3f6b1-42f7-4cf3-a189-a5cc8d78d838)).
  "Agent" quer dizer qualquer software automatizado ou sistema de IA que acessa os Amazon
  Services ([Canopy](https://canopymanagement.com/amazon-bsa-agent-policy-march-2026/)). Análises
  de terceiros incluem automação de navegador e scraping como risco maior do que a SP-API
  ([SellerSprite, MKT](https://sellersprite.ai/en/blog/amazon-bsa-agent-policy-2026);
  [PPC Land](https://ppc.land/amazons-new-ai-agent-rules-shake-up-sellers-before-march-4-deadline/)).
  No fórum, vendedores perguntaram se até o software que puxa pedidos e sobe rastreio conta como
  agente; não houve resposta oficial. O post do r/FulfillmentByAmazon que analisava a cláusula de
  "kill switch" foi removido ([link](https://www.reddit.com/r/FulfillmentByAmazon/comments/1rj9lfc/)).
  **Implicação para o Canastra:** ler o Seller Central da Amazon pelo Claude in Chrome tende a
  cair nessa definição. O caminho que a Amazon declara aceitar é a API ou o plugin oficial.
- **[OFICIAL] O caminho que a Amazon abençoa.** Plugin Selling Partner para o Claude (Accelerate,
  23/9/2026), com o vendedor aprovando as ações; beta nos EUA, expansão internacional
  "a seguir" ([GeekWire](https://geekwire.com/2026/amazon-opens-its-seller-tools-to-outside-ai-agents-starting-with-anthropics-claude);
  [MediaPost](https://www.mediapost.com/publications/article/418249/amazon-opens-seller-tools-to-anthropic-agent-supp.html)).
  Na mesma época, a Amazon passou a bloquear agentes de compra de terceiros, como o Muse da Meta,
  com a mensagem "unauthorized AI agent"
  ([r/AI_Agents](https://www.reddit.com/r/AI_Agents/comments/1wn27g9/amazon_blocking_metas_muse_is_the_first_agent/)).
  O eBay proibiu agentes de "compre para mim" no contrato de usuário em janeiro de 2026
  ([HN](https://news.ycombinator.com/item?id=46734080)); isso é do lado do comprador, mas mostra a
  tendência.

### 4. Resultados medidos e custos

Ver a tabela (c). Em resumo: os números de resultado são quase todos autodeclarados e vários vêm
de quem vende o serviço. Custos que alguém relatou pagar:
- US$ 20 por mês de Claude + US$ 97 por mês de MCP para um gestor de PPC com relatório de 3
  páginas por cliente (u/mazescale, r/AmazonFBA 1wam54y).
- Claude Pro (£ 18 por mês) para a auditoria via extensão e desktop (u/Davydi, r/AmazonFBA 1sk2dxx).
- Scanner de atacado próprio com SP-API num servidor de US$ 6 por mês, montado em 2 dias por uma
  vendedora que não programa
  ([r/AmazonFBA](https://www.reddit.com/r/AmazonFBA/comments/1te4hy5/i_built_a_0_wholesale_bulk_scanner_using_claude/)).
- Cerca de uma semana de "3 h de sono por noite" mais um mês de Claude Max para ligar SP-API e Ads
  API (u/ScribbleSpark).
- Estimativa de fornecedor para um agente próprio: Claude API US$ 100 a 300 + hospedagem US$ 20 a
  100 + Keepa e SmartScout = US$ 200 a 500 por mês, mais 5 a 10 h por mês de manutenção
  ([Jarvio, MKT](https://jarvio.io/blog/build-amazon-ai-agent-with-claude)).
- Recomendação recorrente: abaixo de US$ 5 mil por mês em ads, ferramenta e automação não têm
  dados suficientes e o manual ganha
  ([r/AmazonFBA](https://www.reddit.com/r/AmazonFBA/comments/1p9qf4t/what_can_i_replace_helium_10_ai_advertising_with/)).

### 5. Stack

- **Modelo:** Claude é o mais citado entre os vendedores Amazon, via Cowork, Claude Code, Desktop
  e a extensão do Chrome. Codex e ChatGPT aparecem como equivalentes ("a escolha do modelo importa
  pouco; o que importa é o setup", vários em r/FulfillmentByAmazon 1v93na7). Há quem use
  Gemini 3.5 Flash para rodar contínuo pelo custo, e DeepSeek por ser barato.
- **Agendamento:** n8n, Zapier e tarefas agendadas do Claude. Aviso e aprovação: Slack (vários),
  Google Sheets como fila de revisão, Asana para contexto.
- **MCP:** Amazon Ads MCP (oficial), Helium 10 MCP, Seller Labs MCP (só leitura, MKT), agentcentral,
  Kondado para o Mercado Livre (só leitura, MKT).
- **Frameworks:** LangChain e LangGraph aparecem em agência
  ([r/AI_Agents](https://www.reddit.com/r/AI_Agents/comments/1tahzo7/created_our_first_agent_for_ecommerce_and_im/)).
  Uma montagem Ads API → Claude API → OpenClaw → Slack é relatada como "tudo roda sozinho todo
  dia" (u/goldman21, r/AmazonFBA 1sk2dxx). CrewAI e Make não apareceram em relatos de marketplace.
- **Ferramentas de "piloto automático" comparadas:** Perpetua, Teikametrics, Pacvue, BidX, Scale
  Insights, m19, Sellerboard Smart Portfolios e Helium 10 AI Advertising. Há relatos bons e ruins
  para todas ("para cada recomendação brilhante há alguém com experiência desastrosa", OP de
  r/FulfillmentByAmazon 1v93na7).

### 6. O que deu errado e de que desistiram

Ver a seção (e). Coisas que pessoas dizem ter parado ou recusado automatizar:
- **Lances e lançamento de campanha:** "para relatório é ótimo; para gestão e lançamento, fico
  longe; todo software que testamos foi um desastre" (r/AmazonFBA 1vksrdx). Uma empresa com cerca
  de US$ 7 milhões por ano em ads: "um cara em tempo integral com flat files superou todos os
  softwares de IA de ads que testamos"
  ([r/FulfillmentByAmazon](https://www.reddit.com/r/FulfillmentByAmazon/comments/1rq9fz9/which_amazon_ad_automation_software_is_actually_worth_it/)).
- **Ponta a ponta no Seller Central:** "não consigo nada ponta a ponta que fique estável; sempre
  quebra algo" ([r/FulfillmentByAmazon](https://www.reddit.com/r/FulfillmentByAmazon/comments/1subtbh/what_is_the_most_boring_but_useful_automation_you/)).
- **Agente de marketing e criativo e "cérebro" único:** "um monte de fluxos caros gerando
  relatório que ninguém lia" (u/Winter_Hovercraft438). A leitura de linguagem do cliente
  "inventa padrões em 20% das execuções" (u/BrightExcitement9454). Assistente de redes sociais é
  "superestimado" (mesmo relato).
- **Mudar listing toda semana em automático:** critica-se o risco de desindexar e a
  ("trocar SEO por babá de IA", r/AmazonFBA 1luu1uo).

---

## (c) Tabela de afirmações

| id | afirmação | tipo | fonte | data | país |
|---|---|---|---|---|---|
| A1 | Sistema com agentes de lance, estoque e estratégia e regras de prioridade entre eles; o pior erro veio de um agente reagindo a um dia ruim e de dois agentes em conflito | [CASE] | https://www.reddit.com/r/FulfillmentByAmazon/comments/1v93na7/codex_vs_claude_code_for_ppc/ | 2026-07-28 | n/i |
| A2 | Ligar SP-API e Ads API levou cerca de 1 semana com Claude Max; SQP pede papel à parte e é um ASIN por chamada, numa cota compartilhada | [PRÁTICA] | mesma thread (u/ScribbleSpark) | 2026-07 | n/i |
| A3 | Ferramentas de PPC prontas não conhecem o estoque; lance bom para o ACoS seria desastre para o estoque, por isso montou o próprio sistema | [CASE] | mesma thread | 2026-07 | n/i |
| A4 | SP-API é fonte de dados, não camada de consulta ao vivo; faça um data warehouse; semanas lado a lado, depois um livro de regras | [PRÁTICA] | mesma thread (u/Chrolm) | 2026-07 | n/i |
| A5 | Interface própria sobre a Ads API calcula por regras e só mostra recomendações para aprovar; "alucinar não é problema" | [PRÁTICA] | mesma thread (u/MormonBarMitzfah) | 2026-07 | n/i |
| A6 | Agência: negativos passaram de semanal a quase diário; relatório de mais de 10 contas deixou de tomar meio dia; humano aprova acima de certo delta | [CASE] | https://www.reddit.com/r/FulfillmentByAmazon/comments/1ti5a9c/anyone_elses_agency_or_inhouse_team_moving_to/ | 2026-05-20 | n/i |
| A7 | Trava pelo raio de estrago (US$ em 24 h) e pelo tipo de ação; logar toda decisão com o motivo | [PRÁTICA] | mesma thread (u/AttentionMediocre537) | 2026-05 | n/i |
| A8 | MCP da Amazon Ads: open beta em fevereiro, cobre campanhas, relatórios e lances, exige credencial da Ads API; manter o agente só leitura no começo | [OFICIAL]+[OPINIÃO] (MKT sellerppc) | https://www.reddit.com/r/FulfillmentByAmazon/comments/1w3j3tm/mcp_connection_for_adspend_via_claude/ | 2026-08-31 | n/i |
| A9 | "O MCP da Amazon Ads é grátis mas péssimo" | [OPINIÃO] | mesma thread | 2026-08 | n/i |
| A10 | Gestor de PPC: 6 meses com Claude; hoje ele executa a maior parte das ações; planilha de metas + Asana + auditoria semanal com aprovação; US$ 20 + US$ 97 por mês | [CASE] | https://www.reddit.com/r/AmazonFBA/comments/1wam54y/claude_for_ppc/ | 2026-09-08 | n/i |
| A11 | Atribuição atrasada faz a auditoria de 7 dias cortar demais (desloque a janela uma semana); sem log de mudanças, o agente refaz o lance de 3 dias atrás | [PRÁTICA] (MKT sellerppc) | mesma thread (u/Anis-SellerPPC) | 2026-09 | n/i |
| A12 | Regra de "subir lance se 0 impressões em 7 dias" sobe o lance de campanhas pausadas por falta de estoque | [PRÁTICA] | mesma thread (u/Heath-Thompson) | 2026-09 | n/i |
| A13 | Extensão do Claude + Desktop auditou a conta e, quando pedido, "assumiu o computador" e editou a conta; plano Pro £ 18 | [CASE] | https://www.reddit.com/r/AmazonFBA/comments/1sk2dxx/claude_to_seller_central/ | 2026-04-13 | UK (pela moeda) |
| A14 | Ads API → Claude API → OpenClaw → Slack: vendas +23%, ACoS de 25% para 14%, TACoS de 10% para 8%, roda todo dia | [CASE] não verificado | mesma thread (u/goldman21) | 2026-04 | n/i |
| A15 | Claude ajudou a cortar cerca de 15% do gasto em ads com sugestões de negativos | [CASE] | https://www.reddit.com/r/FulfillmentByAmazon/comments/1t7g843/claude_can_save_you_wasted_ad_dollars/ | 2026-05-08 | n/i |
| A16 | Claude sugeriu negativar palavras super relevantes porque eram caras e sem conversão | [CASE] erro | mesma thread | 2026-05 | n/i |
| A17 | Claude recomendou matar um termo responsável por 30% das conversões de uma marca | [CASE] erro (autor constrói produto) | https://www.reddit.com/r/AmazonFBA/comments/1smcv6q/what_we_learned_trying_to_build_the_nondiy/ | 2026-04-15 | n/i |
| A18 | Setups faça-você-mesmo morrem na manutenção: formato de relatório muda, catálogo cresce, novo tipo de anúncio surge, e o prompt para de funcionar em silêncio | [PRÁTICA] | mesma thread | 2026-04 | n/i |
| A19 | Freelancer de PPC: tarefa agendada lê o SQP e põe palavras com taxa de compra crescente nos bullets; revisou 1 mês em planilha antes de automatizar; CVR 19%, de US$ 13 mil para 74 mil por mês | [CASE] (MKT, vende o serviço a cerca de US$ 800 por mês) | https://www.reddit.com/r/AmazonFBA/comments/1th4777/10k_to_74kmo_in_11_months_claude_automation_for/ | 2026-05-18 | n/i |
| A20 | Mesmo autor: Claude Cowork para pesquisa de palavras (relatório Magnet), painéis, tarefas agendadas no Slack; "mantenho a IA longe dos ads" | [PRÁTICA] (MKT) | https://www.reddit.com/r/AmazonFBA/comments/1vksrdx/almost_300kmo_claude_automations/ | 2026-08-10 | n/i |
| A21 | "Deixe ler tudo, inclusive ads; nunca deixe aplicar; aplicar tem de ser um passo que ele não pode pular" | [OPINIÃO] | mesma thread (u/Gold-Carpenter-4066) | 2026-08 | n/i |
| A22 | 11 agentes para a própria conta; alguns dias de setup e semanas para "construir a máquina"; visualizar a lógica em mermaid | [CASE] | mesma thread (u/k_abderezak) | 2026-08 | n/i |
| A23 | Empresa com cerca de US$ 7 milhões por ano em ads, TACoS de 8%: um analista com flat files superou todos os softwares de IA de ads testados | [CASE] | https://www.reddit.com/r/FulfillmentByAmazon/comments/1rq9fz9/which_amazon_ad_automation_software_is_actually_worth_it/ | 2026-03-10 | n/i |
| A24 | Helium 10 AI Advertising: US$ 2,25 mil em 3 meses, ACoS de 37% contra meta de 20%; abaixo de US$ 5 mil por mês, manual | [CASE] | https://www.reddit.com/r/AmazonFBA/comments/1p9qf4t/what_can_i_replace_helium_10_ai_advertising_with/ | 2025-12 | n/i |
| A25 | Pedido de compra rascunhado no Slack com aprovação num clique; "4 meses sem ruptura nem limite" | [CASE] (cita a ferramenta wrk, possível MKT) | https://www.reddit.com/r/FulfillmentByAmazon/comments/1thu9ni/inventory_management_automation_to_prevent_fba/ | 2026-05-19 | n/i |
| A26 | Preço mínimo do repricer = custo + taxas (Fee Preview) + lucro mínimo; não deixe o Claude decidir o piso | [PRÁTICA] | https://www.reddit.com/r/FulfillmentByAmazon/comments/1wgm6kn/how_do_you_calculate_min_prices_in_bulk_for/ | 2026-09-15 | n/i |
| A27 | Agente de SEO (n8n + GPT) semanal com CSV para revisar: +17% em vendas orgânicas em 4 semanas, 20 h por semana poupadas | [CASE] (MKT tryclair) | https://www.reddit.com/r/AmazonFBA/comments/1luu1uo/17_jump_in_organic_sales_in_4_weeks_using/ | 2025-07-08 | n/i |
| A28 | Atendimento em rascunho e fila: 12 min por dia contra 1 h; o agente de marketing inventa padrões em 20% das execuções; teardown de CRO deu +23% de conversão em 6 semanas | [CASE] | https://www.reddit.com/r/AI_Agents/comments/1tje1aq/help_ai_agents_for_ecommerce_whats_actually/ | 2026-05-21 | n/i |
| A29 | Base única de fatos + agentes estreitos; ads como tarefa diária que grava na base | [PRÁTICA] | mesma thread | 2026-05 | n/i |
| A30 | Agent Policy (BSA Seção 19): agentes se identificam, cumprem a política e param a pedido; em vigor em 4/3/2026 | [OFICIAL] | https://sellercentral.amazon.com/seller-forums/discussions/t/84e3f6b1-42f7-4cf3-a189-a5cc8d78d838 | 2026-02-17/03-04 | EUA |
| A31 | Automação de navegador e scraping têm risco maior sob a Agent Policy do que a SP-API | [OPINIÃO] (MKT) | https://sellersprite.ai/en/blog/amazon-bsa-agent-policy-2026 | 2026-02 | — |
| A32 | Plugin Selling Partner no Claude: estoque, preço, listings, com o vendedor aprovando; beta nos EUA | [OFICIAL] (imprensa) | https://geekwire.com/2026/amazon-opens-its-seller-tools-to-outside-ai-agents-starting-with-anthropics-claude | 2026-09-23 | EUA |
| A33 | O Seller Assistant ganhou memória e fluxos em segundo plano (ex.: alerta se um top-10 cair abaixo de 4 estrelas) | [OFICIAL] (imprensa) | mesma | 2026-09-23 | EUA |
| A34 | Agente próprio com Claude: OAuth expirado parou o agente à noite; endpoint mudou e deixou 3 dias sem dados de PPC; erro 429 derrubava em vez de esperar | [CASE] (MKT Jarvio) | https://jarvio.io/blog/build-amazon-ai-agent-with-claude | 2026-03-06 | — |
| A35 | Ferramenta de anúncios por email/Slack com aprovar e rejeitar cada sugestão; estratégia e verba-alvo no onboarding | [PRÁTICA] (MKT) | https://news.ycombinator.com/item?id=44634593 | 2025-07-21 | — |
| A36 | "72% dos vendedores Amazon que testaram IA abandonaram em 60 dias (Jungle Scout 2025)" | [DADO] **não verificado**: não achei a fonte primária | https://epinium.com/en/blog/claude-for-amazon-sellers/ | 2026-06 | — |
| A37 | 4 a 6 semanas de uso só leitura antes de dar escrita; guardrails não vêm no Claude nem no MCP | [OPINIÃO] (MKT Trellis) | https://gotrellis.com/resources/blog/can-claude-manage-amazon-ads | 2026-05-15 | — |
| A38 | MCP "oficial" do Mercado Livre só busca na documentação; não lê pedidos nem campanhas | [DADO] (MKT Kondado) | https://kondado.com.br/blog/a/mercado-livre-no-chatgpt-e-claude-mcp | 2026-06/10 | BR |
| A39 | n8n + Mercado Livre: falhas de OAuth/PKCE e cookies que expiram no Browserless; recomendação de usar a API oficial | [PRÁTICA] | https://www.reddit.com/r/n8n/comments/1wp2uzp/n8n_mercado_livre_browserless_api/ | 2026-09-24 | BR |
| A40 | Agente de listing completo (Genspark) a partir de um briefing; imagens divergem entre si; "não subiria sem revisar" | [CASE] | https://www.reddit.com/r/AI_Agents/comments/1vu8sle/tried_letting_an_ai_agnt_build_an_entire_amazon/ | 2026-08-21 | n/i |

n/i = não informado. Quase ninguém no Reddit diz o país.

---

## (d) Casos detalhados

1. **u/ScribbleSpark, vendedor Amazon, conta própria.** Montou um sistema com vários agentes
   (lances, estoque, estratégia) sobre SP-API e Ads API, com regras de prioridade para conflitos.
   Começou em modo sugestão, guardando o histórico de aprovações e descartes para calibrar as
   regras; lances ficam "na coleira curta" e negativar termos foi automatizado primeiro. Erros
   relatados: reação a um único dia ruim, dois agentes em conflito e, no pior caso, mexer à mão
   enquanto o sistema rodava, o que "derrubou tudo" e custou margem no mês. Motivo para não usar
   Perpetua ou Teikametrics: elas não conhecem o estoque.
   https://www.reddit.com/r/FulfillmentByAmazon/comments/1v93na7/codex_vs_claude_code_for_ppc/
2. **u/mazescale, gestor de PPC para clientes.** Seis meses com Claude: começou só analisando e
   hoje o Claude executa a maior parte das ações. Planilha de metas por conta, Asana como contexto
   recente, auditoria semanal com aprovar ou recusar, relatório de 3 páginas em PDF por cliente.
   Custa US$ 20 + US$ 97 por mês.
   https://www.reddit.com/r/AmazonFBA/comments/1wam54y/claude_for_ppc/
3. **Agência pequena de Amazon Ads (OP anônimo).** Migrou para automação de PPC via MCP:
   negativos quase diários, lances em passadas menores, relatório de mais de 10 contas virou etapa
   de revisão. Um humano aprova acima de certo delta. A pergunta em aberto é a camada de confiança.
   https://www.reddit.com/r/FulfillmentByAmazon/comments/1ti5a9c/anyone_elses_agency_or_inhouse_team_moving_to/
4. **u/Working_Attention_66, freelancer de PPC (vende o serviço).** Claude API + Zapier ou n8n leem
   o SQP de clientes com mais de US$ 5 mil por mês em ads. As palavras vão para revisão num Google
   Sheet; depois de um mês revisando, uma tarefa agendada passou a inserir algumas nos bullets.
   Reporta CVR de 19% e de US$ 13 mil para 74 mil por mês, mas atribui boa parte à reestruturação
   manual das campanhas. Diz manter a IA longe da gestão de ads.
   https://www.reddit.com/r/AmazonFBA/comments/1th4777/10k_to_74kmo_in_11_months_claude_automation_for/
5. **u/Davydi, vendedor (Reino Unido).** Extensão do Claude no Chrome + Claude Desktop (Cowork),
   plano Pro: auditoria de listings, PPC, avaliações e relatórios; depois mandou corrigir e "ele
   assumiu o computador e foi editando a conta". É o caso mais parecido com o setup do Canastra, e
   sem nenhuma trava descrita.
   https://www.reddit.com/r/AmazonFBA/comments/1sk2dxx/claude_to_seller_central/
6. **Vendedora "dona de casa" (u/Longjumping-Fall8405), Amazon e eBay.** Sem saber programar, fez
   em 2 dias com o Claude um scanner de listas de atacado: SP-API num servidor de US$ 6 por mês,
   calcula lucro, ROI e taxas e sinaliza COMPRAR, REVISAR ou PULAR. Só leitura e decisão humana.
   https://www.reddit.com/r/AmazonFBA/comments/1te4hy5/i_built_a_0_wholesale_bulk_scanner_using_claude/
7. **Contador e dono de e-commerce (Irlanda), Shopify.** Um ano de Claude Cowork e Claude Code
   com CLAUDE.md "constituição", arquivo de contexto, log de decisões e rotina de manutenção.
   Conecta Shopify, Gmail e ads por MCP; o Claude rascunha e ele aprova; o pesado roda no n8n. O
   post foi acusado de captar leads.
   https://www.reddit.com/r/ecommerce/comments/1u43jbb/ecommerce_owners_running_their_store_on_cowork/
8. **Empresa com cerca de US$ 7 milhões por ano em ads (u/binarysolo).** Testou vários softwares
   de IA de ads ao longo dos anos; todos perderam para um analista com flat files e regras simples
   (confiança estatística, teto de cliques para testar cauda longa, razões fixas por posição).
   https://www.reddit.com/r/FulfillmentByAmazon/comments/1rq9fz9/which_amazon_ad_automation_software_is_actually_worth_it/
9. **u/BrightExcitement9454, e-commerce.** Construiu 3 de 4 agentes em 8 meses. O de atendimento
   funciona por causa do portão de aprovação; o de marketing inventa padrões em 20% das vezes, e
   por isso exige 2 fontes; o de social media é superestimado; o de CRO deu +23% de conversão em
   6 semanas em 4 páginas. Conselho: "escolha UM, entregue, meça".
   https://www.reddit.com/r/AI_Agents/comments/1tje1aq/help_ai_agents_for_ecommerce_whats_actually/

---

## (e) Erros e desastres relatados

- **Negativo que mataria o melhor termo:** recomendação de cortar um termo com 30% das
  conversões (r/AmazonFBA 1smcv6q); negativos sugeridos para palavras super relevantes
  (r/FulfillmentByAmazon 1t7g843).
- **Agente reagindo a ruído:** a decisão tomada por um dia ruim e dois agentes com movimentos
  conflitantes; intervir à mão com o sistema rodando "derrubou o sistema inteiro" e custou margem
  no mês (r/FulfillmentByAmazon 1v93na7).
- **Atribuição e memória:** a auditoria de 7 dias compara gasto completo com vendas incompletas e
  "corta"; sem log, o agente faz o lance subir e descer (r/AmazonFBA 1wam54y).
- **Regra cega a pausa:** a regra de "0 impressões, sobe lance" pega campanha pausada por falta de
  estoque, e ao reativar os lances estão outros (mesma thread).
- **Software de IA de ads abaixo da meta:** Helium 10 AI Advertising com ACoS de 37% contra meta
  de 20% (r/AmazonFBA 1p9qf4t); "todo software que testamos foi um desastre" (r/AmazonFBA
  1vksrdx); para cada elogio a uma ferramenta de PPC há um relato de desastre (r/FulfillmentByAmazon 1v93na7).
- **Quebras técnicas:** token OAuth expirado à noite, mudança de endpoint deixou 3 dias sem dados
  de PPC sem ninguém perceber, 429 derrubando o agente (Jarvio, MKT); SQP e relatório de termos
  com timeout por cota compartilhada; cron da Vercel corta em 300 s e uma extração da Amazon leva
  10 min (r/FulfillmentByAmazon 1v93na7); a API do Amazon Pi quebrando com a extensão do Chrome
  (1vl9yvv); a sessão do Mercado Livre expirando no navegador automatizado (r/n8n 1wp2uzp).
- **Repricer:** um post "alguém mais se queimou com repricer que falhou em silêncio?" foi
  removido ([link](https://www.reddit.com/r/FulfillmentByAmazon/comments/1up8sii/)). O caso
  clássico é de dezembro de 2014 (RepricerExpress, Reino Unido): um laço levou preços a 1 centavo
  e um vendedor perdeu US$ 15 mil em estoque em 40 minutos
  ([Fortune](https://fortune.com/2014/12/15/businesses-livid-as-software-glitch-causes-their-stock-to-sell-for-a-penny-on-amazon)).
  É antigo, mas é o modelo do desastre de preço sem piso.
- **Conta e política:** o TikTok Shop baniu uma conta nova antes do primeiro produto, num caso
  atribuído pelo vendedor a moderação por IA
  ([r/TikTokShop](https://www.reddit.com/r/TikTokShop/comments/1t07kzv/)). Há críticas ao
  outreach de afiliados em massa com IA antes de o listing converter
  ([r/TikTokShop](https://www.reddit.com/r/TikTokShop/comments/1vtamas/)). A Amazon passou a exigir
  identificação e kill switch de agentes (A30).
- **Desastre de banimento por agente ou de verba torrada por agente LLM em marketplace:** não
  achei relato concreto. É uma lacuna. Os desastres relatados são de ferramentas de regras ou de
  IA de ads e de recomendações que o humano quase aplicou.

---

## (f) Perfis e hashtags para conferir no navegador

Ninguém nas threads citou perfil de TikTok ou Instagram de quem opera agente em marketplace. O que
apareceu e vale checar:
- **Reddit (usuários que relatam montagem própria, para ver o histórico de posts):** u/ScribbleSpark,
  u/Chrolm, u/mazescale, u/k_abderezak, u/Anis-SellerPPC (sellerppc, MKT), u/Working_Attention_66
  (freelancer de PPC, MKT), u/PrismByCI, u/binarysolo.
- **Podcast:** Seller Sessions (Danny McMillan), episódios "Claude on Steroids: Skills + Sub-Agents +
  MCPs for 7- and 8-Figure Amazon" (23/10/2025) e "Unlocking the power of MCPs for Amazon sellers"
  (8/10/2025): https://sellersessions.libsyn.com/claude-on-steroids-skills-subagents-mcps-for-7-and-8figure-amazon
- **Instagram:** reel citado num comentário de r/AI_Agents sobre o bloqueio do Muse:
  https://www.instagram.com/reel/DdlQ_KKjKo2/ (autopromoção, valor baixo).
- **Hashtags sugeridas para buscar** (não vieram das fontes, são palpite de busca): #amazonfba +
  "claude", #amazonppc, #agentesdeia, #mercadolivre + "n8n", #vendedormercadolivre, #tiktokshopseller.
- **YouTube BR** (tutoriais, não relatos): agente n8n que responde perguntas de anúncio do ML
  (https://www.youtube.com/watch?v=114MFt-ZnO4) e IA do Responso para perguntas do ML
  (https://www.youtube.com/watch?v=HDCmopC2H44).

---

## Lacunas

- Mercado Livre, Shopee e TikTok Shop: nenhum relato no Reddit ou em fóruns de agente de IA
  operando ou gerenciando a conta do vendedor (preço, ads, estoque). O r/brdev e o r/n8n só têm
  dúvidas de integração. O Fórum E-Commerce Brasil, a comunidade do ML e o Clube do Vendedor não
  apareceram na busca.
- Etsy, eBay e Walmart: a busca expirou; nada substantivo coletado.
- r/ClaudeAI e r/shopify: a busca por "Amazon" e "Shopify" expirou.
- Texto oficial completo da Agent Policy da Amazon: só o anúncio e resumos de terceiros. Falta
  confirmar se cobre explicitamente extensões de navegador logadas pelo próprio vendedor.
- Custo real de tokens por agente em produção: ninguém deu número além das assinaturas.
