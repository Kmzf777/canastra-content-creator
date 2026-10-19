# Marketing e aquisição: análises para uma torrefação de café especial que vende via WhatsApp (Meta CTWA + Google Search/PMax)

Data da pesquisa: outubro de 2026. Benchmarks marcados como [BR] (Brasil), [GLOBAL] ou [EUA]. Quase não existe benchmark público de qualidade para "café / alimentos e bebidas no Brasil". Onde não há dado, isso está dito em Lacunas.

## 1. Quais métricas importam, fórmulas exatas e como resolver a atribuição do WhatsApp (CTWA, ctwa_clid, gclid, upload offline)

### Takeaway
O conjunto essencial é: CPL / custo por conversa iniciada, taxa lead→venda por campanha, CAC pago e CAC blended, receita e ROAS por campanha, MER (eficiência total) e payback. Mas com venda no WhatsApp o ROAS "da plataforma" fica perto de zero se ninguém devolver a venda às plataformas. Por isso o elo crítico é guardar o `ctwa_clid` (Meta) e o `gclid` / ID do chat (Google) de cada conversa e mandar de volta as vendas (Purchase / QualifiedLead) pela Conversions API for Business Messaging e pelo import offline / enhanced conversions for leads do Google. Isso dá ROAS real por campanha e deixa os algoritmos otimizarem para compra, não para "conversa".

### Cited Findings
**Atribuição Meta (CTWA)**
- Quando a conversa começa de um anúncio Click-to-WhatsApp, o `ctwa_clid` vem no objeto `referral` do webhook de mensagens. Ele é único por clique e deve ser armazenado com a conversa para depois ser enviado com o evento de conversão. — [Meta for Developers: Conversions API for Business Messaging](https://developers.facebook.com/docs/marketing-api/conversions-api/business-messaging)
- Campos obrigatórios: `event_name`, `event_time`, `action_source = business_messaging`, `messaging_channel = whatsapp`, e `user_data` com `whatsapp_business_account_id` e `ctwa_clid`. O `dataset_id` vai na URL. — [Meta for Developers](https://developers.facebook.com/docs/marketing-api/conversions-api/business-messaging)
- Eventos aceitos: Purchase, LeadSubmitted, QualifiedLead, InitiateCheckout, AddToCart, ViewContent, OrderCreated, OrderShipped, OrderDelivered, OrderCanceled, OrderReturned, CartAbandoned, RatingProvided, ReviewProvided. — [Meta for Developers](https://developers.facebook.com/docs/marketing-api/conversions-api/business-messaging)
- Fornecedores relatam que eventos padrão do pixel, como `Lead` e `CompleteRegistration`, são rejeitados nesse canal. Também relatam que, sem `ctwa_clid` capturado, o envio falha. — [Zernio docs](https://docs.zernio.com/platforms/whatsapp/ctwa) (fonte de fornecedor)
- O `referral` só vem na primeira mensagem depois do clique. Mensagens seguintes não trazem o `ctwa_clid`, então ele precisa ser gravado na hora ("one-shot"). — [Zernio docs](https://docs.zernio.com/platforms/whatsapp/ctwa) (fornecedor)
- Se `action_source` ficar como "website", a Meta não associa a conversão ao anúncio CTWA. — [WATI](https://www.wati.io/en/blog/click-to-whatsapp-ads-instagram/) (fornecedor)
- Requisitos: Cloud API (recomendada) ou On-Premises 2.45.1+, permissões `whatsapp_business_management` e `whatsapp_business_manage_events`, e nível de acesso da Marketing API. A página traz limiares conflitantes (500 vs 1.500 chamadas em 15 dias). A versão On-Premises expirou em 23/10/2025. — [Meta for Developers](https://developers.facebook.com/docs/marketing-api/conversions-api/business-messaging)
- Com eventos de compra enviados, fica disponível a otimização para compras em anúncios click-to-WhatsApp. — [Meta for Developers](https://developers.facebook.com/docs/marketing-api/conversions-api/business-messaging)
- Testes A/B publicados pela Meta (cases, alguns autodeclarados) mostram queda do custo por resultado ao otimizar para compra/lead em vez de conversa. Exemplos: Confer On (ID) −79% no custo por compra, Braip (BR) −30% no custo por lead com otimização de lead vs mensagem, Engelife (BR) −37% no custo por lead qualificado com WhatsApp Flows (autodeclarado). — compilado por [Spur](https://www.spurnow.com/en/blogs/click-to-whatsapp-ads-benchmarks) a partir dos cases da Meta. A página da Braip mostra 44% no resumo e 30% nos resultados.

**Métrica "conversas por mensagem iniciadas" (Meta)**
- A Meta conta pessoas que mandam mensagem pela primeira vez, ou depois de pelo menos 7 dias de inatividade, atribuídas ao anúncio. No WhatsApp, conta só conversas vindas de clique no anúncio. Cliente recorrente que manda mensagem dentro de 7 dias não conta. — [Spur](https://www.spurnow.com/en/blogs/click-to-whatsapp-ads-benchmarks) (resumo de fornecedor sobre a definição da Meta; não achei a página oficial)
- A "conversa" do Gerenciador de Anúncios não é a mesma "conversa" de cobrança da WhatsApp Business API. — [BuyerBridge](https://support.buyerbridge.com/knowledge/messenger-calls-leads-reporting); [Spur](https://www.spurnow.com/en/blogs/click-to-whatsapp-ads-benchmarks)

**Custos de mensagem do WhatsApp (somam ao custo de mídia)**
- Desde 1º/07/2025 a Meta cobra por mensagem entregue, não por conversa de 24h. Números antigos de "custo por conversa" (cobrança) não são comparáveis. — [Message Central](https://www.messagecentral.com/pt-br/blog/click-to-whatsapp-ads-brasil) (fornecedor)
- Conversas iniciadas por anúncio CTWA têm janela gratuita de 72 horas. — [Message Central](https://www.messagecentral.com/pt-br/blog/click-to-whatsapp-ads-brasil)
- Tabela Brasil (verificada em 01/10/2026): mensagem de Marketing US$ 0,0625, Utilidade US$ 0,0068. — [Spur](https://www.spurnow.com/en/blogs/click-to-whatsapp-ads-benchmarks) citando a tabela de preços da Meta

**Atribuição Google (Search / PMax → WhatsApp)**
- Os message assets do Google Ads (botão que abre o WhatsApp) funcionam em campanhas de Pesquisa e Performance Max no Brasil e na Índia. — [Google Ads Help](https://support.google.com/google-ads/answer/14888522?hl=en)
- O Google criou a ação de conversão "conversation started" (conversa iniciada) para cliques em message assets. Ela está em beta. — [Search Engine Land](https://searchengineland.com/google-whatsapp-conversation-started-conversion-action-448608)
- Para atribuir a venda (não só a conversa), um guia de integração captura o GCLID mais um ID único do chat e importa as conversões via Data Manager com webhook. — [Infobip](https://www.infobip.com/docs/integrations/google-click-to-whatsapp) (fornecedor)
- Alternativa simples: evento no GA4/GTM em cliques em links wa.me. — [Cliengo](https://guiawabusiness.cliengo.com/google-ads-whatsapp)
- O Google recomenda começar por enhanced conversions for leads (dados first-party com hash, como e-mail ou telefone) em vez do import só por GCLID. Ele também recomenda mandar o GCLID sempre que possível. — [Google Ads Help: enhanced conversions for leads](https://support.google.com/google-ads/answer/15713840?hl=en); [Google: offline conversion imports](https://support.google.com/google-ads/answer/2998031?hl=en-GB)
- Janelas: upload por GCLID em até 90 dias após o clique; enhanced conversions for leads em até 63 dias. Espere 4–6 h após criar a ação de conversão. Os dados aparecem em 24–48 h. Ajustes (retratar ou reapresentar) podem ser feitos em até 55 dias. — [Relevant Audience](https://www.relevantaudience.com/google-ads-en/google-ads-offline-conversion-import-guide/)
- Desde 15/06/2026, uploads de import offline e enhanced conversions for leads migraram para a Data Manager API e estão bloqueados na Google Ads API, exceto tokens legados em allowlist. — [Relevant Audience](https://www.relevantaudience.com/google-ads-en/google-ads-offline-conversion-import-guide/) (fonte única, confirmar na documentação do Google)
- Por que importa: com dados offline, o Smart Bidding otimiza para lead qualificado ou venda, não para clique. Boas práticas: uma ação de conversão por etapa do funil, upload ao menos diário, envio de valor para usar tCPA/tROAS. O tROAS precisa de cerca de 6 semanas de dados de valor estáveis. Só o import por GCLID aceita crédito fracionado de atribuição externa. — [Relevant Audience](https://www.relevantaudience.com/google-ads-en/google-ads-offline-conversion-import-guide/)
- No Google, o CPC médio é o custo total dividido pelo número de cliques. — [Google Ads Help](https://support.google.com/google-ads/answer/14074?hl=pt-br)

**ROAS, MER e eficiência blended**
- ROAS = receita atribuída pela plataforma ÷ gasto naquela plataforma (decisão diária por canal). MER = receita total da empresa ÷ gasto total de marketing (pega efeito halo e lacunas de atribuição). — [Admetrics](https://www.admetrics.io/post/mer-vs-roas-dtc-ecommerce-31983); [Segwise](https://segwise.ai/blog/mer-the-right-way-marketing-efficiency)
- Atenção à convenção: a Triple Whale define MER invertido (gasto ÷ receita, em %, quanto menor melhor) e inclui salários, produção criativa, agência e software. — [Triple Whale](https://www.triplewhale.com/blog/marketing-efficiency-ratio.md) (via resumo de busca; a página deu 403 no fetch)
- MER de equilíbrio = 1 ÷ margem de contribuição antes de marketing. Exemplo: margem de 50% dá equilíbrio de 2,0x. — [Eightx](https://eightx.co/blog/blended-roas-vs-breakeven-mer)
- A Segwise recomenda nunca olhar o MER isolado, e sim junto com ROAS, margem de contribuição e contribuição líquida em R$. — [Segwise](https://segwise.ai/blog/mer-the-right-way-marketing-efficiency)

### Inferences
- **Fórmulas operacionais (definições padrão de mercado, adaptadas ao fluxo WhatsApp):**
  - CPL (Meta CTWA) = gasto ÷ conversas por mensagem iniciadas. No Google = gasto ÷ (conversas iniciadas + leads de formulário/ligação).
  - Taxa lead→venda (por campanha) = nº de clientes com 1ª compra cuja conversa tem `ctwa_clid` ou `gclid` da campanha ÷ nº de conversas da campanha (mesma coorte, janela fixa, por exemplo 30 dias).
  - CPA / CAC pago (por campanha) = gasto da campanha ÷ novos clientes atribuídos a ela. CAC blended = gasto total de marketing (mídia + agência + ferramentas + custo de mensagens WhatsApp) ÷ todos os novos clientes do período, incluindo orgânicos e indicações. nCAC = foco só em clientes novos.
  - Receita por campanha = soma dos pedidos (1º pedido + recompras em X dias) dos clientes atribuídos. ROAS = receita ÷ gasto. Vale olhar ROAS de 1ª compra e ROAS de 90 dias separadamente.
  - MER = receita total ÷ gasto total de marketing. Comparar com MER de equilíbrio = 1 ÷ margem de contribuição.
  - Payback (meses) = CAC ÷ margem de contribuição mensal por cliente (ticket × frequência × margem bruta menos frete e embalagem). Café é recorrente, então o payback tende a vir de recompras.
- Custo real por conversa no CTWA = gasto de mídia ÷ conversas + custo das mensagens de marketing e utilidade enviadas fora da janela grátis de 72 h.
- Sem a CAPI for Business Messaging, a Meta só "vê" conversas e tende a otimizar para gente que conversa mas não compra. Para uma torrefação, mandar `Purchase` com valor (e `QualifiedLead` para atacado) é o maior ganho estrutural de otimização.
- Na prática a atribuição precisa de uma tabela de conversas com: telefone, data, origem (`ctwa_clid` / `source_id` do anúncio / `gclid` / orgânico), status (lead, qualificado, cliente) e valor. É a base para todo o resto.

### Gaps
- Não achei a página oficial da Meta que define "messaging conversations started" nem a janela de atribuição padrão aplicada a CTWA. Os dados vêm de resumos de fornecedores.
- A data de 15/06/2026 da migração para a Data Manager API vem de uma única fonte não oficial.
- A disponibilidade de "conversation started" no Google para todas as contas BR (beta e requisitos de verificação) não está confirmada.

## 2. Benchmarks: CPL, CPC, CTR, conversão, custo por conversa CTWA e ROAS (Brasil / alimentos e bebidas / D2C)

### Takeaway
Não existe benchmark público confiável específico de café ou alimentos e bebidas no Brasil. O que há: CPL Meta Brasil multissetorial bem abaixo da média global (ferramenta SuperAds), faixas de CPC Brasil de agências sem metodologia, e benchmarks dos EUA (WordStream) para restaurantes e comida. Para uma marca pequena, a melhor régua é o próprio histórico mais o ROAS / MER de equilíbrio, calculado pela margem.

### Cited Findings
**Meta (Facebook/Instagram)**
- [BR, multissetor] O CPL médio no Brasil caiu de cerca de 22,71 para 12,65 ao longo de 2025 (−44%), bem abaixo da média global. A base é de cerca de US$ 3 bi em gasto, sem recorte setorial. A moeda não fica clara no resumo. — [SuperAds](https://www.superads.ai/facebook-ads-costs/cost-per-lead/brazil)
- [GLOBAL, 2025] Triple Whale (cerca de 35 mil contas): CTR médio de 2,19% e CPM médio de US$ 14,19. O CPM subiu 20% e o CTR 13,5% no ano. — citado em [busca/Trendtrack/Influee](https://influee.co/br/blog/facebook-ads-benchmarks)
- [EUA, 2025] WordStream: restaurantes e comida em campanhas de tráfego têm CTR de 1,67%, com queda de cerca de 25% sobre 2024. — [WordStream Facebook Ads Benchmarks 2025](https://www.wordstream.com/blog/facebook-ads-benchmarks-2025)
- [EUA, 2025] LocaliQ, campanhas de lead (formulário nativo), restaurantes: CPC US$ 0,74, CPL US$ 3,16, CTR 2,97%, conversão 18,25%. A média geral das campanhas de lead foi CPL US$ 27,66 (+21% a/a). — [LocaliQ](https://localiq.com/blog/facebook-advertising-benchmarks/); [PPC Land](https://ppc.land/facebook-ad-costs-jump-21-as-lead-campaigns-struggle-while-traffic-ads-thrive/). Um comentarista chama o CPL de restaurante de "too good to be true". — [TheAdSpend](https://theadspend.com/blog/facebook-leads-restaurants)

**CTWA (custo por conversa)**
- [GLOBAL/Europa, fornecedor] Custo por conversa entre €1,50 e €8,00 conforme o setor, sem amostra declarada. A Meta não publica benchmark. — [Spur](https://www.spurnow.com/en/blogs/click-to-whatsapp-ads-benchmarks)
- [GLOBAL, Meta] Experimento da Meta com 734 mil empresas (2º semestre de 2024): anúncios com múltiplos destinos de mensagem tiveram custo mediano por mensagem 9,5% menor que anúncios só WhatsApp. — [Spur](https://www.spurnow.com/en/blogs/click-to-whatsapp-ads-benchmarks) citando a Meta
- [BR] Não encontrei média publicada de custo por conversa CTWA no Brasil em 2025–2026. A métrica "Taxa de conversas iniciadas" (conversas ÷ cliques no link) é sugerida por agência BR como diagnóstico. — [Trafius](https://trafius.com.br/blog/campanha-de-mensagens-no-whatsapp-fluxo-e-metricas)

**Google Ads**
- [EUA, 2025] WordStream Search Benchmarks (16.446 campanhas, abr/2024 a mar/2025, medianas), restaurantes e comida: CPC US$ 2,05, CTR 7,58%, conversão 7,09%, CPL US$ 30,27. A ordem das colunas foi inferida em reprodução de terceiros. — [Christoph Olivier Consulting (reproduz WordStream)](https://christopholivierconsulting.com/?p=5961)
- [EUA, 2026] Média geral WordStream 2026: CPL US$ 66,69 e conversão 8,18%, segundo resumo de terceiros. — [Hawky](https://hawky.ai/blog/google-ads-benchmarks)
- [BR, agências, sem metodologia] CPC de e-commerce entre R$ 1,50 e R$ 5,00. Pesquisa no Google entre R$ 1,00 e R$ 5,00. Outra fonte diz que o CPC no Brasil é 40–60% menor que nos EUA, sem dado primário. — [Novoads](https://novoads.ai/pt-br/blog/quanto-custa-publicidade-no-google-ads); [Stone](https://conteudo.stone.com.br/quanto-custa-investir-em-trafego-pago/)
- [BR, 2024] A Conversion publicou adaptação do benchmark WordStream 2024. — [Conversion](https://www.conversion.com.br/blog/google-ads-benchmarks-2024) (dados de 2024, EUA)

**Conversão de e-commerce e ticket**
- [BR] Conversão média do e-commerce brasileiro entre 1,5% e 1,65% (Experian Hitwise / NeoTrust, sem metodologia detalhada). — [Babitonhela](https://babitonhela.com/blog/taxa-conversao-ecommerce-estrategias)
- [GLOBAL Shopify, 2026] Alimentos e bebidas convertem entre 4,2% e 6,22%, contra 1,4–1,8% na média da plataforma. Top performers passam de 6,8%. — [LaunchTip](https://www.launchtip.com/pt-BR/blog/benchmarks-taxa-de-conversao-shopify-por-setor-2026)
- [BR, 2025] ABIACOM: e-commerce faturou R$ 235,5 bi (+15,3%), 438,9 mi de pedidos, ticket médio de R$ 536,6, para todos os setores. Projeção de 2026: ticket de R$ 562,15. — [Mundo do Marketing](https://mundodomarketing.com.br/e-commerce-brasileiro-cresce-15-3-e-fatura-r-235-5-bilhoes-em-2025); [Central do Varejo](https://centraldovarejo.com.br/e-commerce-deve-faturar-r-2598-bilhoes-em-2026-projeta-abiacom/)
- [BR] 55% dos lojistas Nuvemshop citam a baixa conversão como obstáculo. — [Central do Varejo / NuvemCommerce 2025](https://centraldovarejo.com.br/nuvemcommerce-2025-revela-desafios-do-e-commerce-brasileiro/)

**ROAS / MER**
- [GLOBAL D2C] MER blended saudável fica entre 3,0x e 5,0x (receita ÷ gasto) para a maioria das marcas, dependendo da margem, recompra e AOV. — [Eightx](https://eightx.co/blog/average-ecommerce-mer-by-vertical-2026)
- [GLOBAL, 2025] Mediana Triple Whale de MER de 41% (gasto ÷ receita), o que dá cerca de 2,4x na convenção receita ÷ gasto. É informação de segunda mão. — [Segwise](https://segwise.ai/blog/mer-the-right-way-marketing-efficiency)

### Inferences
- Benchmarks de "lead" dos EUA (formulário) não se comparam com "conversa iniciada" no WhatsApp: conversa é mais barata e menos qualificada. A taxa conversa→venda é o que define a eficiência.
- Para uma torrefação pequena, "bom" se mede pela própria margem. Exemplo: com margem de contribuição de 45%, o ROAS / MER de equilíbrio é cerca de 2,2x na 1ª compra. Se a recompra em 90 dias é relevante (café é consumível), um ROAS de 1ª compra perto de 1,5–2x ainda pode valer, desde que o payback seja de no máximo 2–3 meses. É uma inferência, não um benchmark publicado.
- O ticket médio de café especial D2C deve ficar bem abaixo do ticket médio geral do e-commerce BR (R$ 536), então o CAC tolerável é proporcionalmente menor. É inferência, sem dado de café.

### Gaps
- Nenhum benchmark publicado de CPL, CPC, CTR ou custo por conversa para café ou alimentos e bebidas no Brasil em 2024–2026. RD Station, Opinion Box e E-commerce Brasil não retornaram números setoriais nas buscas.
- Nenhum custo médio por conversa CTWA no Brasil com metodologia.
- Nenhum ROAS mediano de alimentos e bebidas no Brasil.

## 3. Como times SMB/D2C estruturam dashboards, rotinas semanais e alertas

### Takeaway
A estrutura comum tem três camadas. Primeiro, o negócio: MER, receita, novos clientes, CAC blended. Segundo, o canal / campanha: gasto, CPL, lead→venda, CAC pago, ROAS. Terceiro, o criativo e a busca: CTR, frequência, termos de pesquisa, canais do PMax. A rotina é semanal, com alertas automáticos para custo subindo, gasto sem resultado e fadiga. O PMax ganhou relatórios de canal e termos de pesquisa em 2025, o que permite auditar onde o dinheiro vai.

### Cited Findings
- O relatório de desempenho por canal do PMax foi anunciado em 30/04/2025, com beta a partir de 30/05/2025. Ele separa Pesquisa, YouTube, Display, Discover, Maps e Gmail, filtra por formato e tem dados a partir de 06/06/2025, sem histórico anterior. — [PPC Land](https://ppc.land/google-ads-performance-max-channel-reporting-now-live-in-select-accounts/); [The Media Image](https://the-media-image.com/insights/tactical-guidance/performance-max-transparency-arrives-how-to-use-channel-reporting-search-terms)
- O relatório de termos de pesquisa agora cobre todas as campanhas PMax. A coluna "Source" mostra se o termo veio dos Search themes ou da expansão sem palavra-chave. Na API, o recurso é `campaign_search_term_view`, com custo. — [The Media Image](https://the-media-image.com/insights/tactical-guidance/performance-max-transparency-arrives-how-to-use-channel-reporting-search-terms)
- Também vieram métricas por asset e diagnósticos, como alerta de locais de loja ausentes que limitam Maps. — [PPC Land](https://ppc.land/google-unveils-major-transparency-boost-for-performance-max-campaigns/)
- Regras automáticas da Meta (Ads Manager → Regras) têm condição, ação e escopo. Há a ação "só notificar", condições combinadas com E, agendamento contínuo, diário ou personalizado, e limite de 250 regras por conta. — [Netpeak](https://netpeak.net/blog/how-to-set-up-automated-rules-in-meta-ads); [Cropink](https://cropink.com/meta-automated-rules)
- Exemplo de regra: custo por resultado sobe 25% em 3 dias, então pausa ou notifica. É bom sempre combinar com gasto mínimo para não reagir a amostra pequena. — [KlientBoost](https://klientboost.com/facebook/facebook-ads-automated-rules/); [Cropink](https://cropink.com/meta-automated-rules)
- Exemplo de alerta de fadiga: notificação por frequência alta. — [TopGrowthMarketing](https://topgrowthmarketing.com/facebook-automated-rules/)
- O ROAS de plataforma serve para decisões diárias por canal. O MER captura o halo entre canais. Use os dois juntos. — [Admetrics](https://www.admetrics.io/post/mer-vs-roas-dtc-ecommerce-31983)
- O CTR das campanhas de restaurante e comida na Meta caiu cerca de 25% a/a, um sinal da necessidade de rodízio criativo. — [WordStream](https://www.wordstream.com/blog/facebook-ads-benchmarks-2025)

### Inferences (proposta de painel e rotina para a Café Canastra)
- **Painel semanal (visão do dono):** gasto total e por canal (Meta CTWA, Google Search, PMax); conversas iniciadas; CPL; % qualificadas; novos clientes; taxa lead→venda; CAC pago e blended; receita de 1ª compra e de 30/90 dias por campanha; ROAS por campanha; MER versus MER de equilíbrio; pacing do orçamento (gasto acumulado ÷ orçamento do mês contra % do mês decorrido).
- **Análise de criativo (Meta):** por anúncio, olhar CTR, custo por conversa, frequência, taxa conversa→venda e receita. Considerar fadiga quando a frequência sobe e o CTR cai semana após semana.
- **Google:** termos de pesquisa semanais (negativar termos irrelevantes como "café grátis", "emprego", "cafeteria perto de mim" se não houver loja física), relatório de canais do PMax (quanto vai para Display/YouTube contra Pesquisa/Shopping), separar marca de não-marca.
- **Alertas sugeridos:**
  - CPL de 3 dias 30% acima da média de 14 dias, com gasto mínimo.
  - Gasto acima de R$ X em 24–48 h sem nenhuma conversa ou lead.
  - ROAS de 7 dias abaixo do ROAS de equilíbrio.
  - Frequência acima de 3–4 em público frio.
  - Pacing fora de ±15%.
  - Conversas sem resposta em mais de X horas: perder a janela de 72 h encarece e derruba a conversão.
  - Queda brusca de conversas iniciadas, que pode indicar anúncio reprovado ou número do WhatsApp com problema.
  - Os limiares são sugestões, não benchmarks publicados.

### Gaps
- Não achei a documentação oficial do Google sobre o relatório de canais e termos de pesquisa do PMax nesta rodada. As fontes são blogs especializados.
- Não achei fonte brasileira (RD Station, Resultados Digitais) com template de dashboard para venda via WhatsApp.

## 4. B2B / atacado / private label versus B2C

### Takeaway
No B2B (cafeterias, empórios, escritórios, marca própria), o lead é mais caro e o ciclo mais longo. O que importa é qualificação (fit e intenção) e pipeline, não o CPL. Os benchmarks gerais de B2B ficam em torno de 13% de MQL→SQL e ciclos de 30–120 dias conforme o ticket. Não há benchmark específico de atacado de alimentos ou café.

### Cited Findings
- [GLOBAL, B2B geral] MQL→SQL mediano de cerca de 13% (outra base dá 13,7%, com quartil superior em 28,4%). Faixas citadas de 13–26%, e times top acima de 35%. — [Prospeo](https://prospeo.io/s/average-b2b-lead-conversion-rate); [Landbase](https://landbase.com/blog/lead-qualification-statistics); [SyncGTM](https://syncgtm.com/blog/b2b-sales-funnel-conversion-rates)
- A origem do lead pesa muito. Numa base, leads de site converteram 31,3% (MQL→SQL), indicações 24,7%, webinars 17,8%, eventos 4,2%, listas 2,5% e e-mail 0,9%. — [SyncGTM](https://syncgtm.com/blog/how-many-qualified-leads-convert-into-sales-in-b2b)
- MQL→SQL abaixo de 15% costuma indicar problema na definição de MQL (scoring frouxo), não na qualidade do lead. — [Abstrakt](https://www.abstraktmg.com/lead-conversion-rate-benchmark/); [Geckoboard](https://www.geckoboard.com/resources/kpi-examples/mql-to-sql-conversion-rate/)
- Ciclo B2B mid-market de 60–120 dias (mediana de 92 dias em 2026, contra 68 em 2019). Negócios SMB de US$ 5–15 mil fecham em 30–45 dias, e cada 5x no ACV dobra o ciclo, aproximadamente. — [Abmatic](https://abmatic.ai/blog/b2b-sales-cycle-length-benchmarks-2026); [Zeliq](https://www.zeliq.com/blog/sales-cycle)
- Definições de início do ciclo variam (criação do lead, 1ª reunião, oportunidade), o que torna benchmarks pouco comparáveis. — [SyncGTM](https://syncgtm.com/blog/b2b-sales-cycles)
- Case BR (Meta): Engelife usou WhatsApp Flows para qualificar e teve custo por lead qualificado 37% menor e taxa de qualificação +26 p.p. (autodeclarado). Braip (BR) otimizou para lead em vez de mensagem e teve −30% no CPL e +45% em leads qualificados. — [Spur (cases Meta)](https://www.spurnow.com/en/blogs/click-to-whatsapp-ads-benchmarks)
- O evento `QualifiedLead` existe na CAPI for Business Messaging, o que permite otimizar campanhas B2B para lead qualificado em vez de conversa. — [Meta for Developers](https://developers.facebook.com/docs/marketing-api/conversions-api/business-messaging)
- No Google, crie uma ação de conversão por etapa do funil (lead, qualificado, venda) e defina como primária a etapa que se quer otimizar. — [Relevant Audience](https://www.relevantaudience.com/google-ads-en/google-ads-offline-conversion-import-guide/)

### Inferences
- **Separar B2B de B2C em campanhas e em métricas.** No B2B, o painel deve mostrar custo por lead qualificado, taxa qualificado→1º pedido, tempo até o 1º pedido, valor do 1º pedido e valor recorrente mensal da conta (LTV de atacado), e CAC ÷ margem mensal da conta (payback).
- **Scoring sugerido para atacado / private label** (perguntas no WhatsApp ou Flow): tipo de negócio (cafeteria, empório, restaurante, escritório, revenda, marca própria); volume mensal estimado (kg/mês); cidade e logística; se já compra café especial; prazo para começar; decisor ou não. Pontuar fit e intenção. Private label exige MOQ e ciclo maior (desenvolvimento de rótulo e blend).
- **Janela de atribuição maior no B2B.** Com ciclos de semanas, o upload offline por GCLID (até 90 dias) é melhor que o enhanced conversions for leads (63 dias) para fechamentos tardios. É inferência baseada nas janelas citadas.
- B2B com CPL alto mas ticket recorrente alto pode ter CAC muito mais tolerável que o B2C. Comparar as duas frentes por payback, não por CPL.

### Gaps
- Nenhum benchmark de ciclo de venda, conversão ou CPL específico para atacado de café ou alimentos (food service) no Brasil.
- Nenhum dado público de MOQ ou ciclo típico de private label de café no Brasil nesta rodada.
