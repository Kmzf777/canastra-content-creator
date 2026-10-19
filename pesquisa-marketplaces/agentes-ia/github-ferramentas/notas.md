# Agentes de IA para contas de marketplace: código aberto, MCP e produtos comerciais

Pesquisa feita em 19/10/2026 com WebSearch, WebFetch e a API pública do GitHub (estrelas e datas
lidas nesse dia). Não usei o navegador. Legenda de confiança usada no texto:
**[E]** evidência (documentação oficial, código, README, página do próprio marketplace);
**[M]** marketing (blog de fornecedor, review de afiliado, imprensa repetindo release).

---

## (a) Resumo em 10 linhas

1. Em 2026 os marketplaces passaram a oferecer o próprio MCP: a Amazon tem o **Amazon Ads MCP** (beta aberto em 02/02/2026) e o **Amazon Selling Partner Connector** (23/09/2026, beta só nos EUA, dentro do Claude).
2. O Mercado Livre tem um MCP oficial (`mcp.mercadolibre.com/mcp`), mas ele só **busca documentação** (2 ferramentas). Não opera a conta.
3. Shopee, TikTok Shop, Walmart e eBay não têm MCP oficial confirmado. O que existe são servidores de terceiros por cima das APIs oficiais.
4. O padrão que Amazon, Bling, Shopify e os bons projetos abertos adotaram é o mesmo: **ler é livre, escrever vira rascunho e só roda com aprovação**, e ainda vem com log.
5. A arquitetura que dá certo é **um conector (MCP) mais várias skills por função**, não um agente gigante. O toolkit oficial da Amazon tem 12 skills, uma para cada problema.
6. As funções em que todo mundo divide são preço, conteúdo de anúncio, ads, estoque, atendimento, reputação ou saúde da conta, concorrência e relatórios ou finanças.
7. Os comerciais da gringa (Helium 10, Pacvue, Jungle Scout, Intentwise) viraram "dados + MCP" e cobram pelo plano alto. Helium 10 Diamond custa US$ 279/mês no anual.
8. No Brasil, o que existe de concreto é o **Bling MCP** (05/10/2026, conector verificado no Claude, escrita só com confirmação), o JoomAI/JoomPulse (ML e Shopee) e automações por regra (UpSeller).
9. A autonomia real que existe hoje é estreita. Rodam sozinhos: alertas, monitoramento, pedido de avaliação e respostas por regra. Preço e texto publicado ficam no manual em quase todos.
10. Para o Canastra: um conector por marketplace (API oficial ou, sem API, o Chrome) e as mesmas skills por função em todos, com a trava "rascunho → ok do Rafael → executa → confere".

---

## (b) Repositórios e servidores MCP

Estrelas e último push lidos pela API do GitHub em 19/10/2026. "Sério" quer dizer mantido, com
trava de escrita e uso real declarado. "Brinquedo" quer dizer demo, só lista ou zero manutenção.

| Projeto | Marketplace | ★ | Último push | O que faz | Arquitetura | Aprovação humana | Sério? | URL |
|---|---|---|---|---|---|---|---|---|
| amzn/selling-partner-agentic-toolkit (**oficial Amazon**) | Amazon SP-API | 30 | 15/10/2026 | 12 skills + 3 comandos sobre o Selling Partner Connector: analytics, fechamento do mês, ruptura, FBA inbound, 4 skills de anúncio, compliance, chamado de suporte | 1 MCP remoto + skills especialistas, com uma "roteadora" (`listing-troubleshooter`) | "Write actions are always human-in-the-loop (drafted for your approval)" [E]. Finanças só lê; compliance só aconselha | Sim (oficial, recente) | https://github.com/amzn/selling-partner-agentic-toolkit |
| amzn/selling-partner-api-samples (`sp-api-dev-mcp`) | Amazon SP-API | 211 | 16/10/2026 | MCP local para desenvolvedor: Dev Assistant e Workflow Builder | Ferramenta de dev, não opera conta | n/a | Sim (para dev) | https://github.com/amzn/selling-partner-api-samples |
| mercadolibre/mercadolibre-mcp-server (**oficial ML**) | Mercado Livre | 13 | 01/10/2025 | Só o README de configuração do MCP remoto; as ferramentas são `search_documentation` e `get_documentation_page` | MCP remoto de documentação | n/a (não escreve) | Oficial, mas raso | https://github.com/mercadolibre/mercadolibre-mcp-server · doc: https://developers.mercadolivre.com.br/pt-br/server-mcp |
| MarcosNahuel/mercadolibre-mcp | Mercado Livre | 6 | 23/09/2026 | Envolve o MCP oficial e acrescenta operações de vendedor: preço, estoque, perguntas, ads, reputação, concorrência, `price_to_win`, `stockout_risk` | 5 camadas (oficial, endpoints, conhecimento, fluxos, meta) | As 4 ferramentas de escrita **só existem** com `ML_WRITES_ENABLED=1`; há um pacote `-read` só leitura [E] | Médio (1 autor, bem desenhado) | https://github.com/MarcosNahuel/mercadolibre-mcp |
| joomcode/joompulse-skills | ML e Shopee BR | 54 | 28/09/2026 | Skills do Claude sobre dados de mercado da JoomPulse: produto vs concorrentes, monitor de mudança semanal, nichos, mesmo produto | MCP pago (JoomPulse) + skills | Só leitura (dados de mercado) | Sim (empresa por trás) | https://github.com/joomcode/joompulse-skills |
| newerton/mcp-mercado-livre | Mercado Livre | 13 | 15/10/2026 | Busca produtos, preços e disponibilidade (lado comprador) | MCP local | n/a | Brinquedo útil | https://github.com/newerton/mcp-mercado-livre |
| EbrahimElbagory/claude-fba | Amazon | 17 | 24/07/2026 | 5 skills do Claude Code: auditoria da loja, pedido de avaliação, `listing-guard`, `impact-tracker`, palavra-chave | Claude Code como cérebro + SP-API própria + Helium 10 MCP + cron | Somente leitura por padrão; o que o comprador vê passa por rascunho → aprovação → execução, com backup e "undo" [E] | Sim (feito por vendedor, em loja real) | https://github.com/EbrahimElbagory/claude-fba |
| ferrants/amazon-seller-agent-claude-code | Amazon | 8 | 18/05/2026 | Modelo de Claude Code como "gerente de marca": 10 skills (ads, otimização, listing audit, reposição, experimentos, dashboards) + pastas `data/brands`, `initiatives`, `reports` | 1 agente (Claude Code) + MCP comercial (Marketplace Ad Pros) + memória em arquivo | Depende do MCP | Médio (amarrado a fornecedor) | https://github.com/ferrants/amazon-seller-agent-claude-code |
| nospicyplease/amazon-ppc-advanced-skills | Amazon Ads | 14 | 28/05/2026 | Skills de PPC: diagnóstico de queda, oportunidades, colheita de termos, fila de ações para aprovar | Skills + MCP Rocketcart | Escrever exige aprovação explícita, preflight, IDs exatos, valor atual/proposto, readback e monitoramento [E] | Sim (melhor descrição de trava encontrada) | https://github.com/nospicyplease/amazon-ppc-advanced-skills |
| christian-ramos/mcp-amazon-sp-api | Amazon SP-API | 4 | 01/10/2026 | Mais de 55 ferramentas em 19 escopos (catálogo, pedidos, listings, preço, A+, feeds, mensagens) | MCP local Python | Ferramentas que mudam algo exigem `confirm=True`; sem ele, devolvem um preview do plano [E] | Sim (o autor diz ~400 testes) | https://github.com/christian-ramos/mcp-amazon-sp-api |
| mansournorouzi/amazon-sp-mcp | Amazon SP-API | 47 | 17/10/2026 | Pedidos, estoque, vendas, reembolsos, settlements, taxas, Brand Analytics | MCP local Node, só leitura | n/a (lê) | Sim | https://github.com/mansournorouzi/amazon-sp-mcp |
| KuudoAI/amazon_ads_mcp (Openbridge) | Amazon Ads | 73 | 14/10/2026 | Passa a Ads API por MCP (campanhas, relatórios, DSP, AMC) | "Camada de ferramentas"; as skills da plataforma "esperam um humano antes de qualquer coisa ir ao ar" [M] | Na camada de skills paga | Sim | https://github.com/KuudoAI/amazon_ads_mcp |
| MarketplaceAdPros/amazon-ads-mcp-server | Amazon Ads | 29 | 21/05/2025 | Cliente do MCP hospedado da MAP | MCP remoto comercial | Só leitura por padrão; edição opcional, confirmada a cada mudança [M] | Parado no GitHub (o produto é hospedado) | https://github.com/MarketplaceAdPros/amazon-ads-mcp-server |
| Deltologic/datadoe-mcp | Amazon Seller/Vendor/Ads | 16 | 15/10/2026 | MCP hospedado de dados Amazon | Comercial, ~US$ 97/mês [M] | Escrita limitada | Comercial | https://github.com/Deltologic/datadoe-mcp |
| Buer2333/tiktok-shop-mcp | TikTok Shop | 7 | 19/10/2026 | MCP sobre a Partner API | MCP local | não documentado | Brinquedo / início | https://github.com/Buer2333/tiktok-shop-mcp |
| Mintive TikTok Shop MCP (hospedado) | TikTok Shop | — | doc 2026 | Pedidos, produtos, estoque, logística, devoluções, finanças, promoções, SAC | MCP hospedado sobre a Open API | **Só leitura até um admin ligar** `TIKTOK_SHOP_ENABLE_WRITES`; lista de lojas permitidas; `idempotency_key` [E/doc] | Sim (doc detalhada) | https://www.mintmcp.com/docs/tiktok-shop-mcp-setup |
| aronhy/tiktok-agent-skills | TikTok Shop | 171 | 03/08/2026 | Skills de seleção de produto, análise de loja e vídeos virais (dados KSS MCP) | Skills + MCP de dados | Só leitura | Médio (China) | https://github.com/aronhy/tiktok-agent-skills |
| Maz1n0-zzz/shopee-mcp-server | Shopee | 1 | 28/07/2026 | Open Platform v2: loja, produtos, pedidos, preço, estoque | MCP local | não documentado | Brinquedo | https://github.com/Maz1n0-zzz/shopee-mcp-server |
| gaganggoyal/marketplace_seller_agent | Amazon.in, Flipkart, Meesho, Myntra | 0 | 27/09/2026 | "Store Manager" raiz + 4 especialistas (preço, estoque, listings, devoluções); abre todo dia com um digest de saúde | Multiagente (Google ADK), coordenador + especialistas | Preço, estoque e status mostram antigo → novo e esperam "sim" [E] | Brinquedo, mas com desenho bom | https://github.com/gaganggoyal/marketplace_seller_agent |
| nexscope-ai/Amazon-Skills / eCommerce-Skills | Multi | 778 / 1181 | 26/08/2026 | 53 / 142 skills em markdown (palavra-chave, listing, FBA, PPC) | Só prompts, sem conector | n/a | Isca de marketing (popular, raso) | https://github.com/nexscope-ai/Amazon-Skills |
| Walmart (luke-nielsen/walmart-mcp, alyiox/mcp-walmart-marketplace) | Walmart | — | 2026 | Itens, estoque, preço, pedidos | Comunitários | não verificado | Não verificado | https://e-tailize.com/blog/best-ecommerce-mcp-servers/ |
| Shopify (Storefront, Catalog, Checkout e Dev MCP; extensões do Sidekick) | Shopify (referência) | — | 2026 | Os MCPs oficiais são da **loja/comprador** e de dev; as extensões do Sidekick **propõem** ações do app | Plataforma | "agents propose, merchants approve" [M, Weaverse]; docs: https://shopify.dev/docs/apps/build/ai.md | Referência | https://weaverse.io/blogs/shopify-sidekick-agents-propose-merchants-approve-2026 |

Observação: repricers abertos de verdade praticamente não existem. Os que aparecem são de 2017–2020
ou "skills" de prompt (alphaparkinc). Ninguém publica um repricer LLM com histórico, e preço
continua sendo regra mais trava de margem.

---

## (c) Produtos comerciais: função × autonomia × preço

| Produto | Funções / "agentes" | Faz sozinho | Pede aprovação | Preço | Tipo | URL |
|---|---|---|---|---|---|---|
| **Amazon Seller Assistant (agêntico)** | Estoque (giro lento, remarcação, remoção), planejamento sazonal FBA/AWD, compliance e saúde da conta, crescimento | Monitora e alerta; segundo a PPC Land, aplica "soluções aprovadas" de compliance | Ações na conta: "with permission, take action" | Sem custo adicional | [E] Amazon | https://sellingpartners.aboutamazon.com/amazon-accelerate-2025-a-new-era-of-tools-and-technology-for-independent-sellers · https://ppc.land/amazon-introduces-agentic-ai-across-seller-platform/ |
| **Amazon Seller Assistant workflows + plugin (Quick/Claude)** | Memória do negócio, workflows contínuos (reposição, ajuste de preço), canvas de cenários | Workflows rodam com o vendedor deslogado, dentro de guardrails | Para cada workflow o vendedor escolhe "só recomenda" ou "também age"; ação só depois de revisar e aprovar; log completo | Grátis; Quick Plus grátis por 12 meses até 31/12/2026 | [E] | https://www.aboutamazon.com/news/innovation-at-amazon/seller-assistant-plugin-amazon-quick-claude |
| Amazon Enhance My Listing | Título, bullets, atributos e descrição a partir do comportamento do cliente | Gera a sugestão | O vendedor revisa, edita ou recusa cada sugestão | Grátis | [E] | https://aboutamazon.com/news/innovation-at-amazon/amazon-generative-ai-seller-growth-shopping-experience |
| Amazon Project Amelia | "Especialista de vendas" pessoal, com recomendações | Responde e recomenda | — | Grátis, beta nos EUA (2024) | [E] | mesma URL acima |
| Amazon Ads Agent / Creative Agent / AMC Ads Agent Skill | Segmentos de DSP, criativos de display e vídeo, SQL de AMC | Gera | Não descrito | Grátis (beta aberto, unBoxed nov/2025) | [M, Perpetua] | https://perpetua.io/blog-amazon-unboxed-2025-announcements/ |
| Helium 10 "Helium" + MCP | Pergunta e resposta sobre ads, palavras-chave, P&L, listings e estoque; "devolve uma decisão" | Analisa e recomenda; o MCP lê e escreve campanhas, lances e listings (segundo a MAP) | A página do agente não fala de aprovação | Só no Diamond: US$ 279/mês (anual) ou US$ 359 (mensal) | [M] | https://www.helium10.com/blog/meet-helium-helium-10s-new-ai-agent/ · https://marketplaceadpros.com/guides/top-amazon-mcp-servers-2026/ |
| Pacvue Agent | Análise de campanha, SQL de AMC, relatórios, ajuste de campanha por meta | "automatically adjusts campaigns based on defined goals" | Uma análise de terceiro fala em "Governed Execution" com aprovação e auditoria, sem confirmação oficial | Enterprise, sob consulta | [M] | https://www.contentgrip.com/pacvue-ai-agent-amazon-ads · https://stellagent.ai/insights/pacvue-agent-ai-commerce-media |
| Jungle Scout Cobalt + MCP | Inteligência de mercado: categoria, concorrente, preço, palavra-chave | Lê | n/a | Enterprise | [M] | https://caylent.com/case-study/jungle-scout · https://marketplaceadpros.com/guides/top-amazon-mcp-servers-2026/ |
| Intentwise AI Gateway | Dados de ads de Amazon, Walmart, TikTok e outros | Só leitura | n/a | Incluso no plano | [M] | https://marketplaceadpros.com/guides/top-amazon-mcp-servers-2026/ |
| Teikametrics (Flywheel / ARI) | Lance de ads por margem, demanda e estoque (Amazon, Walmart, TikTok Shop) | Ajusta lances (bidder) | Escopo do MCP não publicado | Sob consulta | [M] | https://www.getapp.com/all-software/a/teikametrics-flywheel-1/ |
| Perpetua | Motor de lances; otimiza campanhas criadas pelo Creative Agent | Lances automáticos | — | Sob consulta | [M] | https://perpetua.io/blog-amazon-unboxed-2025-announcements/ |
| Feedvisor (Agentis?) | Repricing por IA; "Agentis" juntaria ads, preço e estoque (maio/2026, fonte única) | Reprecifica em tempo real | — | Repricing a partir de ~US$ 100/mês; 360 a partir de US$ 1.500/mês | [M] | https://hackceleration.com/labs/review/feedvisor |
| Carbon6 | Reembolsos FBA (serviço gerenciado) | Abre a disputa | — | 25% do valor recuperado | [M] | https://hackceleration.com/labs/compare/feedvisor-vs-carbon6 |
| Marketplace Ad Pros | Ads, SP, DSP e AMC + recomendações + experimentos | Lê | Edição opcional, confirmada a cada mudança | US$ 10/semana a US$ 999/mês | [M] | https://marketplaceadpros.com/guides/top-amazon-mcp-servers-2026/ |
| Quartile, SellerApp | — | — | — | — | Sem dado 2026 encontrado | (lacuna) |
| **Mercado Livre: Verdi** | Atende vendedores, avalia a qualidade do anúncio, rotula produtos, sugere resposta ao comprador pelo histórico | "10% das mediações já são feitas de forma autônoma" | — | Grátis (nativo) | [E-imprensa] | https://www.mobiletime.com.br/?p=836618 (26/09/2025) |
| Mercado Livre: editor de imagens com IA | Gera ambientação ou modelo a partir da foto | Gera | O vendedor escolhe | Grátis; "mais de 1 milhão de imagens" | [E-imprensa] | mesma URL |
| Mercado Livre: títulos, descrições e respostas | Sugestão de título e descrição; respostas automáticas por palavra-chave | Respostas por regra | Sugestões | Grátis | [M] (blogs) | https://mambadigital.com.br/blog/inteligencia-artificial-mercado-livre/ · https://upseller.com/pt/help-doc-article-501 |
| **Bling MCP** (ERP, conector verificado no Claude) | Resumo do dia, fluxo de caixa, lucro real depois de frete e taxa, pedidos travados, 18 rotinas prontas | Lê e analisa à vontade | "Faturar pedidos em lote ou emitir nota" só depois de clicar para confirmar | Incluso em todos os planos (limite da API) | [E] blog oficial, 05/10/2026 | https://blog.bling.com.br/?p=21609 |
| JoomAI (Joom Group) | Mais de 100 agentes: preço, anúncios, concorrência, estoque, oportunidades, conteúdo; conector para Claude/ChatGPT | Monitora 24h e manda relatório | Não informado | Não informado | [M] (lançado em 28/07/2026) | https://www.dgabc.com.br/Noticia/4343205/joom-group-lanca-o-joomai-primeiro-servico-de-ia-criado-para-vendedores-e-lojistas-de-marketplaces |
| JoomPulse | Dados de mercado de ML e Shopee BR (exclusivo da Shopee BR desde 27/08/2026) | Lê | n/a | Não informado | [M] | https://nossomeio.com.br/joompulse-fecha-parceria-com-shopee-e-amplia-acesso-a-inteligencia-de-mercado-para-mais-de-100-mil-vendedores-brasileiros/ |
| UpSeller (ERP) | Título e descrição por IA, resposta automática ML (regras), resposta à avaliação Shopee por estrela | Responde por regra | — | Plano + "UpCoins" para a IA; resposta ML grátis | [E] central de ajuda | https://www.upseller.com/pt/help-doc-article-1943 |
| Nubimetrics | Inteligência de ML (Market, Competitor, My Business) | Lê | n/a | Pack 360 mensal ou anual, preço sob consulta; 14 dias grátis | [M] | https://testdev.nubimetrics.com/en/?p=392 |
| Real Trends | Responder perguntas, posicionamento, concorrência, operadores (ML) | — | — | Assinatura; preço não achado | [M] (antigo) | https://coronavirus.startupblink.com/innovations/buenos-aires+argentina/real-trends |
| Magis5, Ideris, Anymarket, Hub2b, Olist, Tiny, Lexos | Hubs e ERPs de integração (catálogo, estoque, pedido) | Sincronizam | — | — | Nenhum agente de IA confirmado | https://blog.bling.com.br/ideris-o-que-e/ · https://canaltech.com.br/startup/startup-do-interior-de-sp-conecta-pequenas-lojas-online-a-marketplaces-217154/ |
| TikTok Shop Seller Assistant | Chatbot no Seller Center: dúvidas de listing, métricas, sugestões, passa para humano | Responde | — | Grátis (maio/2025) | [M] imprensa | https://www.socialmediatoday.com/news/tiktok-adds-seller-assistant-ai-chatbot/748785/ |
| Shopee Shop AI Assistant / Product AI Optimiser | Chatbot de pré e pós-venda; auditoria de listing em lote | Chatbot responde | — | — | [M] (Malásia; Brasil não confirmado) | https://www.growthhq.io/our-thinking/unlocking-shopees-ai-power-step-by-step-guide-for-malaysian-smes-to-boost-sales-and-exports-in-2026 |

---

## (d) Mapa das funções que o mercado separa em agentes

| Função | Quem separa assim (exemplos) | Roda sozinho (consenso) | Sempre com aprovação | Fonte de dado |
|---|---|---|---|---|
| **Saúde da conta / compliance / reputação** | Seller Assistant (compliance), toolkit Amazon (`listing-compliance`), agente indiano (account-health guardian), MCP ML (`get_reputation`) | Monitorar, alertar e explicar a causa | Qualquer correção publicada; o compliance da Amazon só aconselha | Painel / API de métricas |
| **Anúncio: diagnóstico e correção** | Toolkit Amazon (troubleshooter → issues / buyability / searchability), claude-fba (`store-audit`, `listing-guard`), Verdi (qualidade) | Auditar, comparar com a auditoria anterior, rascunhar | Mudar texto, atributo ou foto publicados (com backup e undo) | Listings + dados de busca |
| **Conteúdo / SEO do anúncio** | Enhance My Listing, Helium 10, UpSeller, editor de imagem do ML | Gerar sugestão | Aceitar ou publicar | Comportamento de busca |
| **Preço / buy box** | Feedvisor, Seller Assistant workflows, `price_to_win` (ML), especialista de preço (agente indiano) | Repricer por regra com piso de margem (comerciais) | No modo agente, preço é **manual ou aprovado** em quase todos (o toolkit Amazon "não dá conselho de preço") | Concorrência + custo/taxa |
| **Ads / PPC** | Amazon Ads Agent e MCP, Pacvue, Perpetua, Teikametrics, Helium 10, skills de PPC | Lance dentro de meta (bidders), relatório, colheita de termos | Criar campanha ("só precisa de revisão e aprovação"), mudar orçamento | Ads API + AMC |
| **Estoque / reposição / logística** | `stockout-prevention`, `fba-inbound-management`, Seller Assistant (giro lento), `stockout_risk` (ML) | Dias de cobertura, alerta de ruptura | Plano de envio, remoção, remarcação | Estoque + velocidade |
| **Atendimento (perguntas, mensagens, mediação)** | Verdi (10% das mediações sozinho), UpSeller (regras), Shopee AI Assistant, TikTok Shop Chat | Respostas por regra ou FAQ; mediação simples (ML) | Resposta livre gerada por LLM (nos projetos abertos) | Perguntas + histórico |
| **Avaliações / reviews** | claude-fba (`review-automation`), UpSeller (resposta por estrela) | Pedido oficial de avaliação, todo dia | — | API de solicitação |
| **Concorrência / mercado / oportunidades** | Jungle Scout, JoomPulse, Helium 10, Opportunity Explorer, Nubimetrics | Coletar e comparar semana a semana | n/a (só lê) | Dados de mercado (normalmente pagos) |
| **Relatórios / finanças** | `finance-month-end-closer`, Bling MCP (cockpit diário, lucro real), `impact-tracker` | Digest diário, fechamento do mês, baseline antes e depois | Nunca mexe em dinheiro (o toolkit Amazon "never files, submits, pays") | Settlements, ERP |
| **Suporte da plataforma** | `support-case-helper` | Montar o resumo do chamado sem dado pessoal | Abrir o chamado | — |

**A rotina que se repete** (claude-fba, agente indiano, Amazon workflows, JoomAI):
digest diário de saúde (vendas vs ontem, pendências, ruptura, alertas) → auditoria semanal
comparada com a anterior → fila de ações propostas → aprovação → execução → leitura de volta →
medição de impacto contra o baseline.

**As travas que se repetem:**
1. Leitura por padrão; ferramentas de escrita desligadas por variável (`ML_WRITES_ENABLED`, `TIKTOK_SHOP_ENABLE_WRITES`) ou exigindo `confirm=True`.
2. Escrever vira um rascunho com valor antigo → novo, IDs exatos e preview.
3. Aprovação explícita por ação, ou por tipo de workflow ("só sugere" vs "pode agir") no caso da Amazon.
4. Backup antes e readback depois, com undo de um comando.
5. Log e auditoria de toda ação.
6. Permissão herdada do papel do usuário no painel ("Manage Agents" na Amazon; permissões do Bling).
7. Dinheiro, chamado e envio de mensagem nunca rodam sem confirmação.
8. Começar em "só sugere" e liberar o automático por tipo de ação depois de semanas ([M] SellerSprite sugere 30 dias).

---

## (e) Anúncios oficiais (2025–2026)

| Data | Marketplace | Anúncio | URL | Observação |
|---|---|---|---|---|
| 17–18/09/2025 | Amazon | Seller Assistant ganha capacidades agênticas no Accelerate 2025, mais Opportunity Explorer e Unmet Demand Insights | https://sellingpartners.aboutamazon.com/amazon-accelerate-2025-a-new-era-of-tools-and-technology-for-independent-sellers | Oficial. "with permission, take action on behalf of sellers" |
| 11/2025 | Amazon Ads | Ads Agent, Creative Agent e AMC Ads Agent Skill (beta aberto, unBoxed) | https://perpetua.io/blog-amazon-unboxed-2025-announcements/ | Via parceiro |
| 02/02/2026 | Amazon Ads | Amazon Ads MCP Server em beta aberto | https://advertising.amazon.com/library/news/amazon-ads-mcp-server-open-beta | Oficial. Cria, edita e apaga campanhas, relatórios e billing |
| 23/09/2026 | Amazon | Seller Assistant workflows + plugin no Amazon Quick e no Claude (beta EUA) | https://www.aboutamazon.com/news/innovation-at-amazon/seller-assistant-plugin-amazon-quick-claude · https://thenextweb.com/news/amazon-seller-assistant-plugin-claude-quick | Oficial |
| 09/2026 | Amazon | Conector "Amazon Selling Partner" no diretório do Claude (beta) + toolkit no GitHub | https://claude.com/marketplace/connectors/amazon-selling-partner · https://github.com/amzn/selling-partner-agentic-toolkit | 8 ferramentas: `call_read_only_tool`, `call_write_tool`, `search_tools`, `sellerAssistant_*`… |
| 2024 | Amazon | Enhance My Listing e Project Amelia | https://aboutamazon.com/news/innovation-at-amazon/amazon-generative-ai-seller-growth-shopping-experience | Oficial |
| 30/09/2025 (repo) e 20/05/2026 (doc) | Mercado Livre | MCP Server oficial: só documentação; OAuth no cliente | https://developers.mercadolivre.com.br/pt-br/server-mcp · https://github.com/mercadolibre/mercadolibre-mcp-server | Oficial. **Não opera a conta** |
| 26/09/2025 | Mercado Livre | Verdi (agente para vendedores) e editor de imagens com IA | https://www.mobiletime.com.br/?p=836618 | Entrevista com o diretor de engenharia, sem release |
| 24–25/09/2026 | Mercado Livre | MLXP 2026: IA em atendimento e marketing para vendedores | https://brasilinovador.com.br/mercado-livre-experience-2026-reune-ecossistema-de-e-commerce-e-consolida-avancos-em-logistica-ia-e-servicos-financeiros/ | Imprensa, sem detalhe de produto |
| 05/2025 | TikTok Shop | Seller Assistant (chatbot no Seller Center) | https://www.socialmediatoday.com/news/tiktok-adds-seller-assistant-ai-chatbot/748785/ | Imprensa; não achei post oficial |
| 14/05/2026 | TikTok (Ads, não Shop) | API de Ads aberta a agentes por MCP | https://botoi.com/zh/blog/tiktok-mcp-server-ad-agents/ | Fonte única, não confirmada |
| 05/10/2026 | Bling (ERP) | Bling MCP, conector verificado no Claude | https://blog.bling.com.br/?p=21609 | Oficial do Bling |

---

## (f) Afirmações

| id | Afirmação | Tipo | URL | Data |
|---|---|---|---|---|
| A1 | O Amazon Ads MCP cria, atualiza e apaga campanhas, roda relatórios e acessa billing; a campanha SP gerada "only needs review and approval" | Evidência (oficial) | https://advertising.amazon.com/library/news/amazon-ads-mcp-server-open-beta | 02/02/2026 |
| A2 | O toolkit SP da Amazon: "Write actions are always human-in-the-loop (drafted for your approval)"; o assistente só usa as ferramentas que o papel do usuário no Seller Central permite | Evidência (código oficial) | https://github.com/amzn/selling-partner-agentic-toolkit | 15/10/2026 |
| A3 | O plugin do Seller Assistant está em beta só nas lojas dos EUA, sem Ads, Vendor nem finanças | Evidência (Amazon) + marketing (DataDoe, para o recorte) | https://www.aboutamazon.com/news/innovation-at-amazon/seller-assistant-plugin-amazon-quick-claude · https://www.datadoe.com/blog-posts/amazon-selling-partner-plugin-claude | 23/09/2026 |
| A4 | Workflows da Amazon: o vendedor escolhe "só recomenda" ou "também age"; ação só depois de revisar e aprovar; "complete audit trail" | Evidência (oficial) | https://www.aboutamazon.com/news/innovation-at-amazon/seller-assistant-plugin-amazon-quick-claude | 09/2026 |
| A5 | O Seller Assistant agêntico vem "with permission, take action"; o vendedor fica com "final decision making" | Evidência (oficial) | https://sellingpartners.aboutamazon.com/amazon-accelerate-2025-a-new-era-of-tools-and-technology-for-independent-sellers | 18/09/2025 |
| A6 | Permissões por tipo de ação (só sugere / auto-aprova); recomenda manter preço e conteúdo publicado no manual | Marketing (fornecedor terceiro) | https://www.sellersprite.com/en/blog/amazon-ai-seller-assistant-agentic-2026 | 17/07/2026 |
| A7 | O MCP oficial do ML tem só `search_documentation` e `get_documentation_page` | Evidência (doc oficial, via busca; o WebFetch deu 403) | https://developers.mercadolibre.com.ar/en_us/mcp-server | 2025–2026 |
| A8 | O MCP comunitário do ML só registra as 4 ferramentas de escrita com `ML_WRITES_ENABLED=1` | Evidência (README) | https://github.com/MarcosNahuel/mercadolibre-mcp | 23/09/2026 |
| A9 | O Verdi faz 10% das mediações de forma autônoma, e o NPS dele supera o do atendimento humano | Afirmação da empresa (imprensa) | https://www.mobiletime.com.br/?p=836618 | 26/09/2025 |
| A10 | O editor de imagens com IA do ML já gerou mais de 1 milhão de imagens | Afirmação da empresa | https://www.mobiletime.com.br/?p=836618 | 26/09/2025 |
| A11 | O Bling MCP lê à vontade, e escrita (faturar, emitir NF) só roda com clique de confirmação; incluso em todos os planos | Evidência (blog oficial do Bling) | https://blog.bling.com.br/?p=21609 | 05/10/2026 |
| A12 | O agente e o MCP da Helium 10 só vêm no Diamond (US$ 279/mês anual) | Marketing (Helium 10) | https://www.helium10.com/blog/meet-helium-helium-10s-new-ai-agent/ | 24/08/2026 |
| A13 | Pacvue Agent "automatically adjusts campaigns based on defined goals" | Marketing (imprensa) | https://www.contentgrip.com/pacvue-ai-agent-amazon-ads | 04/05/2026 |
| A14 | Na data do guia, a Perpetua não tinha MCP; Intentwise e Jungle Scout têm MCP só de leitura | Marketing (concorrente) | https://marketplaceadpros.com/guides/top-amazon-mcp-servers-2026/ | 26/08/2026 |
| A15 | O JoomAI tem mais de 100 agentes (preço, anúncios, concorrência, estoque, conteúdo) e monitora 24h | Marketing (release) | https://www.dgabc.com.br/Noticia/4343205/joom-group-lanca-o-joomai-primeiro-servico-de-ia-criado-para-vendedores-e-lojistas-de-marketplaces | 28/07/2026 |
| A16 | O MCP TikTok Shop da Mintive é só leitura até o admin ligar a escrita; as decisões usam `idempotency_key` | Evidência (doc de produto) | https://www.mintmcp.com/docs/tiktok-shop-mcp-setup | 2026 |
| A17 | O claude-fba enviou 437 pedidos de avaliação e corrigiu 4 listings com rascunho → aprovação → rollback, no primeiro dia | Afirmação do autor (README) | https://github.com/EbrahimElbagory/claude-fba | 07/2026 |
| A18 | Skills de PPC: escrita ao vivo exige aprovação, preflight, IDs exatos, valor atual e proposto, readback e monitoramento | Evidência (README) | https://github.com/nospicyplease/amazon-ppc-advanced-skills | 05/2026 |
| A19 | Mais de 900 mil vendedores usaram as ferramentas de listing com IA da Amazon | Afirmação da empresa | https://aboutamazon.com/news/innovation-at-amazon/amazon-generative-ai-seller-growth-shopping-experience | 2024 |
| A20 | A Carbon6 foi comprada pela SPS Commerce por US$ 210 milhões (02/2025) | Marketing (review) | https://hackceleration.com/labs/compare/feedvisor-vs-carbon6 | 2026 |

---

## (g) Lacunas

- **Shopee:** não achei MCP oficial, nem anúncio oficial de IA para o vendedor brasileiro. O que existe vem da Malásia e de blogs. Falta conferir no Seller Centre BR e no open.shopee.com.
- **TikTok Shop:** não achei MCP oficial nem post oficial do Seller Assistant (só imprensa). O MCP de Ads de 14/05/2026 tem fonte única.
- **Mercado Livre:** a página de desenvolvedores deu 403 no WebFetch; os dados vieram dos snippets de busca e do GitHub oficial. Não achei release oficial do Verdi para vendedores do Brasil, nem um "Gestor de Anúncios" com IA. Não confirmei se as respostas automáticas nativas usam LLM ou só regra.
- **Amazon Brasil:** o plugin e o conector são só dos EUA. Não achei data para amazon.com.br.
- **Preços** de Nubimetrics, Real Trends, JoomAI, Pacvue, Teikametrics, Quartile e SellerApp não são públicos ou não foram achados.
- **Quartile, SellerApp, Magis5, Ideris, Lexos, Hub2b, Anymarket, Olist, Tiny:** nenhum agente de IA confirmado em 2025–2026.
- **Feedvisor "Agentis"** (maio/2026) tem uma fonte só.
- Os números de impacto (338% de CTR do Creative Studio, 40% de qualidade de listing, 20–30% de GMV na Shopee) são todos do fornecedor, sem auditoria.
- Não testei nenhum MCP; o "sério ou brinquedo" vem de README, estrelas e data de push.
- O Selling Partner Connector lista `call_write_tool` genérico; não vi a documentação de quais escritas ele cobre além de listing, preço e FBA inbound.
