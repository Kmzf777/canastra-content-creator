# Mapa de dados e viabilidade de análises — Café Canastra (banco de produção, schema `public`)

Fontes: catálogo `schema-public.txt` (69 objetos, tabela|coluna:tipo) e código local, só leitura, sem conexão a banco.
Abreviações de caminho:
- `V/` = `Agentes AI/ValerIA/`
- `VW/` = `Agentes AI/ValerIA-agente-1b4e178b/`, worktree com migrations mais novas (out/2026). Elas já estão refletidas no catálogo: existem `ja_era_cliente`, `campanha_manual_*`, `occurred_at`, `meta_referrals_arquivo` e `sales.freight`.
- `mig/` = `V/supabase/migrations/`

Ressalvas gerais:
- Todas as afirmações abaixo vêm do código. Não houve consulta a dados reais, então volumes, preenchimento e qualidade de cada coluna **não foram verificados**.
- O repositório `beeinside` usa **outro banco**. As tabelas dele (`product_cmv`, `monthly_results`, `daily_sales_cache`, `bling_tokens`) não aparecem no catálogo `public` de produção.

---

## 1. Inventário de dados por área

### Takeaway
O banco cobre bem a jornada **anúncio → lead → conversa (IA/vendedor) → card de funil → orçamento → venda (CRM + pedidos Bling)**. Os pontos fracos são três:
- custo de produto e margem não existem;
- não há histórico de estoque;
- o vendedor está identificado de formas inconsistentes (uuid, e-mail ou texto).

### Cited Findings

**A. Aquisição / marketing**
- **`ad_spend`:** uma linha por (platform, campaign_id, date), com `cost` em BRL. É preenchida por sync diário que faz upsert idempotente dos **últimos 30 dias** do Google Ads e do Meta Ads.
  - Granularidade: **campanha × dia**. Não há conjunto de anúncios, anúncio, impressões, cliques nem conversões da plataforma.
  - Fontes: `mig/20260805_ad_spend.sql:3-13`; `V/backend/app/campaigns/ad_spend_sync.py:1,24-26,42-127`.
  - Google: Ads API v22, `metrics.cost_micros` por campaign × `segments.date` — `google_ads.py:104-105`.
  - Meta: Insights com `level=campaign` e `time_increment=1` — `meta_ads.py:62-67`.
  - O worker roda a cada 3h, sempre com janela de 30 dias — `worker/main.py:62-64,100`. Há também um botão manual `POST /api/traffic/sync-ads`.
- **`meta_ad_campaigns`:** mapa ad_id → campaign_id/campaign_name, gravado pelo mesmo sync do Meta (Insights `level=ad`) — `ad_spend_sync.py:99-118`, `meta_ads.py:112-119`. **Só cobre anúncios com entrega nos últimos 30 dias em cada execução.** Anúncios antigos só aparecem se já tiverem sido mapeados antes.
- **Atualização de `ctwa_clid`:** é gravado na criação do lead (primeiro toque) e **sobrescrito** por um novo clique (último toque) — `V/backend/app/webhook/meta_router.py:67,87-96`.
- **Botão de WhatsApp do anúncio Google:** uma mensagem "encontrei vocês pelo Google" grava `utm_campaign='WhatsApp do Google'` — `V/backend/app/leads/google_message_asset.py:1-59`.
- **`campanha_manual_*`:** é **só de admin** (`PATCH /api/traffic/leads/{id}/campanha`) e gera o evento `atribuicao_manual` — `traffic_router.py:63-92`, `traffic_attribution.py:79-138`.
- **Atribuição gravada em `leads`:**
  - colunas: `utm_source/medium/campaign`, `gclid`, `gbraid`, `wbraid`, `fbclid`, `ctwa_clid` (Click-to-WhatsApp), `meta_ad_id`, `traffic_type`, `channel` e `metadata.origem` (funil de landing page / importação);
  - `campanha_manual_canal/id/nome/por/em`: atribuição manual que **vence** meta_ad_id e UTMs — `VW/supabase/migrations/20261006_call_semanal_base.sql:76-86`;
  - regras de canal (12 regras, a primeira que casar vence: gclid → Google; fbclid/ctwa/meta_ad_id → Meta; utm paga; reativação Bling; Bling; orgânico IG/FB; LP; manual; importação; WhatsApp direto; sem rastreio) — `V/docs/superpowers/specs/2026-09-23-origem-do-lead-design.md`;
  - a mesma lógica existe em Python em `V/backend/app/campaigns/traffic_report.py:115` (`derive_channel`) e em SQL em `fn_lead_canal` — `VW/supabase/migrations/20261006b_lead_timeline_triggers.sql:33-60`.
- **Campanha do Google:** o lead não guarda campaign_id. O nome é resolvido por *matching* de `utm_campaign` com os nomes em `ad_spend`: primeiro nome idêntico normalizado, depois subconjunto único de tokens, depois desempate por utm_medium; sem candidato, fica null — `traffic_report.py:45` (`resolve_campaign_id`).
- **`lead_primeira_origem`** é uma **VIEW**: o primeiro evento `entrada` de cada lead em `lead_events`, com `metadata->>'canal'`, `campanha_id` e `campanha_nome` — `20261006_call_semanal_base.sql:180-190`.
- **`meta_referrals_arquivo`:** cópia permanente dos referrals CTWA (ctwa_clid, source_id = id do anúncio, source_type). Existe porque `meta_webhook_logs` tem retenção de 15 dias — `20261006_call_semanal_base.sql:108-170`.
- **Conversões offline (Meta CAPI / Google):**
  - O mecanismo no código é `pipeline_stages.conversion_event` (lead/qualified/opportunity/purchase) + `conversion_value` (BRL fixo; `purchase` usa `deals.value`). A tabela `conversion_events` registra o envio, com unique (deal_id, event), `sent_meta` e `exported_at` — `mig/20260702_conversion_attribution.sql:11-45`; `V/backend/app/campaigns/conversions.py`; `capi_dispatcher.py:41-130`.
  - A Meta CAPI é automática: usa ctwa_clid (business_messaging) ou fbclid (website).
  - O Google é exportado manualmente em CSV, só para leads com gclid — `V/backend/app/campaigns/google_export.py:20-30`.
  - **Não está em uso:** em 09/09/2026, `conversion_events` tinha 0 linhas e nenhuma etapa tinha `conversion_event` — `mig/20260909_recuperacao_stages_optout.sql:64-65`. Em 10/09 foi deixado NULL de propósito — `mig/20260910_contrato_etapas_joao.sql:39-40`.
  - **`ad_conversions` e `ad_conversion_values` existem no catálogo de produção, mas em nenhum repositório local nem no histórico git.** A semântica (fila por lead/estágio/segmento com click_id, status, tentativas e valor) é **inferida só pelos nomes de coluna**. Provavelmente vêm de um branch ainda não visível localmente.
- **Landing page:** `POST /webhook/landing-page` grava UTMs, fbclid, gclid, meta_ad_id e `metadata.origem` — `V/backend/app/lp_webhook/router.py:12-54`, `service.py:150-300`.
  - `lp_email_jobs` não tem migration nem código que a escreva: parece tabela legada.
- **Discrepâncias entre catálogo e código:**
  - `leads.gbraid` e `wbraid` existem no catálogo, mas não aparecem no código.
  - O checkout local de `ValerIA` está num branch antigo; a verificação foi feita em `origin/master` e no worktree `VW/`.
  - Há migrations aplicadas à mão (P0/P3 de 06/10), então produção pode divergir do repositório.

**B. Leads, conversa e IA (Valeria)**
- **`leads.stage`** é o **segmento/etapa da Valeria**, não o funil do vendedor. Valores no código: `secretaria`, `atacado`, `private_label`/terceirização, `consumo`, `perdido`.
  - A view de score filtra `l.stage = 'atacado'` — `mig/20260921_valeria_score.sql:164`.
  - O segmento define o dono: `vendor_user_id_for_segment` em `V/backend/app/agent/tools.py:800-806`.
- **Handoff (`encaminhar_humano`):**
  - grava `status='converted'`, `human_control=true`, `ai_enabled=false` e `assigned_to = dono do pipeline do segmento`;
  - cancela os follow-ups com reason `handoff` — `tools.py:790-830`;
  - **carimba `leads.metadata.handoff{vendedor_id, vendedor, segmento, motivo, at}`** — `tools.py:861-866`;
  - grava a mensagem de sistema `[encaminhar_humano] Lead encaminhado para …` — `V/backend/app/agent/handoff.py:17-48`;
  - move ou cria o deal na 1ª etapa não protegida do pipeline do vendedor — `service.py:934-982`;
  - envia a despedida (`sent_by='handoff'`) e agenda `handoff_rescue`.
  - O dashboard conta handoffs por essa mensagem de sistema — `mig/20260712_dashboard_rpcs.sql:112-117`.
  - O fluxo de botões também grava `metadata.handoff` com `origem='button_flow'` — `V/backend/app/button_flow/effects.py:455-529`.
- **Roteamento por segmento:** atacado → "João - Atacado"; private_label → "João - Private Label"; exportacao → "Arthur - Exportação" — `service.py:927-931`.
- **`leads.status`:** `imported`, `active` ou `converted` (handoff).
- **`leads.first_response_at`:** é lido pela UI, mas **nunca é escrito** (sempre NULL).
- **`channels.mode`:** `ai` ou `human` (o número pessoal do vendedor) — `V/backend/app/channels/router.py:61`. O vendedor muitas vezes responde pelo próprio canal, o que gera **outra conversa** — `mig/20260712_dashboard_rpcs.sql:13-15`.
- **`messages`:**
  - `role` (user/assistant/system);
  - `sent_by`: `agent` (IA), `seller` (vendedor no CRM), `followup`, `broadcast`, `campaign`, `automation`, `button_flow`/`valeria_botoes` (fluxo de botões), `bridge` e `handoff` (mensagens de ponte do handoff), `user`;
  - também `wamid`, `delivery_status`, `agent_persona`, `created_at`.
  - Fonte: grep de `sent_by=` em `V/backend/app`.
- **`conversations.first_seller_response_at` / `last_seller_response_at`:** preenchidas por trigger a cada mensagem com `sent_by='seller'` — `mig/20260525_sla_seller_columns.sql:7-24`. Também guarda `last_customer_message_at`.
- **SLA:** `sla_settings.target_minutes` (padrão 20), `sla_seller_config` (janela de atendimento e dias da semana por vendedor/canal; um canal por vendedor) e `sla_overrides` (folgas) — `mig/20260611_sla_per_seller.sql`.
  - Existe a função de horas úteis `dashboard_business_seconds` — `mig/20260712_dashboard_rpcs.sql:29`.
  - O atraso é calculado **no front** (`V/frontend/src/lib/sla-rounds.ts:19-93`). A "rodada" fecha com uma resposta `seller` **ou** `agent`, então não é um SLA puramente humano.
- **RPCs de dashboard existentes** (`mig/20260712_dashboard_rpcs.sql`):
  - `dashboard_kpis`: leads novos, conversas atendidas, handoffs, taxa de qualificação (mensagem `[qualificar_lead]`), SLA handoff→vendedor (mediana e p95 em segundos úteis, mesma conversa) e custo por handoff;
  - `dashboard_funnel_conversion`: lead → handoff → deal com key `fechado_ganho`;
  - `dashboard_outbound_frio`;
  - `dashboard_followups`.
  - Também existe `get_broadcast_reply_metrics`.
- **`lead_qualification_scores`:** segmento B2B (cafeteria, empório, …), `monthly_volume_kg`, `supplier_reason`, `purchase_timing`, `purchase_intent`.
  - O score é **regra determinística em constraint**: normal_score de 0 a 8; final_score = 10 se trocar fornecedor + intenção clara; prioridade low/moderate/high/maximum; `is_provisional` se faltar algum campo.
  - `source` = live/backfill.
  - Fonte: `mig/20260921_valeria_score.sql:30-95`.
  - Views relacionadas: `valeria_score_directory` e `valeria_score_recent_leads`, só para leads `atacado`.
- **`lead_seller_feelings`:** sentimento do vendedor sobre o lead, com justificativa — `V/frontend/src/app/api/valeria-score/[leadId]/feeling/route.ts`.
- **`token_usage`:** tokens (prompt, completion, thoughts, cached) e `total_cost` por chamada, com `lead_id`, `stage`, `model` e `call_type` (followup, rolling_summary, media_transcription, button_flow_classify, …).
  - Custo em **USD**: o teto diário é `LLM_DAILY_COST_LIMIT_USD` — `V/backend/app/agent/budget_guard.py:9-72`.
  - Gravação: `V/backend/app/agent/token_tracker.py:51-136`.
  - Preços: `model_pricing`.
  - Já existem RPCs `stats_costs_summary/daily/breakdown/top_leads` — `mig/20260711_stats_aggregation_rpcs.sql:38-137`.

**C. Funil comercial (CRM)**
- **Estrutura:** `pipelines` (por vendedor via `owner_user_id`; "esteiras" do João: Atacado, Private Label, Reposição, Recuperação, Reposição PL), `pipeline_stages` (com `key`, que é o contrato estável usado pelo código, e `label`, editável), e `deals` (stage_id, `entered_stage_at` só da etapa atual, closed_at, lost_reason, value).
  - Fontes: `mig/20260910_contrato_etapas_joao.sql:1-140`; `V/backend/app/leads/service.py:1278-1300`.
- **Keys conhecidas:**
  - funil frio da Valeria: `disparo_feito`, `respondeu`, `qualificado`, `encerrado`;
  - João: `novo`, `respondeu`, `chamado_reposicao`, `em_atencao`, `proposta_enviada`, `entrada`, `em_followup`, `recuperado`;
  - terminais: `fechado_ganho` / `perdido`.
- **`mark_deal_qualificado`** cria o card se necessário e o move para a key `qualificado` — `service.py:1450-1470`.
- **Histórico de etapas:** `lead_events` passou a ser a **linha do tempo**, com tipos `entrada`, `etapa` (trigger em `deals.stage_id`, metadata de_stage_id/para_stage_id e labels), `venda`, `venda_cancelada`, `disparo`, `mesclagem` e `atribuicao_manual`. Traz `occurred_at`, `source` e `dedupe_key`, com backfill idempotente — `VW/supabase/migrations/20261006b_lead_timeline_triggers.sql:6-20,247-296`.
- **`lost_reason`** é **texto livre** passado pelo chamador (IA ou tela) — `service.py:1630-1670`.
- **`quotes` / `quote_items`:** status rascunho, enviado, aprovado, nao_aprovado, convertido, cancelado. Na conversão viram `sales` com `origin='crm'` e pedido no Bling (`converted_at`, `sale_id`) — `V/backend/app/quotes/router.py:492,708-846`; `mig/20260825_quotes.sql`.

**D. Vendas / ERP Bling**
- **`sales`** é criada por três caminhos:
  - `manual`: no CRM, exige lead e deal;
  - `crm`: o CRM cria o pedido no Bling;
  - `bling`: webhook ou backfill de pedido do ERP, **sem deal**.
  - Fontes: `V/backend/app/bling/orders.py:426-427,581-634`; `mig/20260818_bling_integration.sql:146-173`.
- **`status`:** `registrada` ou `cancelada` (pedido apagado no Bling) — `orders.py:656`.
- **Clientes do Bling viram leads:** o pedido de um cliente que não estava em `leads` **cria um lead** (`channel='bling'`, `metadata.origem='bling_webhook'`) — `V/backend/app/bling/contacts.py:508-581`.
- **Backfill:** 12 meses, só a conta `default` — `V/backend/app/bling/backfill.py`.
- **Contas Bling:** `default` = Café Canastra e `secundaria` = Café Rural — `V/backend/app/bling/config.py:27-30`.
- **`sold_by`** é o e-mail do usuário do CRM — `mig/20260818_bling_integration.sql:108`.
  - **Vendas `origin='bling'` nunca têm `sold_by`**: eram 1.012 vendas sem vendedor em 24/08.
  - As vendas manuais anteriores foram normalizadas para joao@ (`sold_by_source='normalizacao_joao'`) — `mig/20260824_sales_sold_by_normalizacao.sql:4-42`.
- **`sale_items`** só existe para vendas ligadas ao Bling. A venda manual tem apenas o texto `product`.
- **`bling_products`:** `preco` (preço de venda) e `saldo_virtual` (estoque virtual **atual**). **Não sincroniza preço de custo** — `V/backend/app/bling/products.py:23-41`.
- **Espelhos:** `bling_contacts` (com `vendedor_id`), `bling_sellers`, `bling_seller_map` (e-mail → vendedor Bling), `bling_situacoes` e `bling_payment_methods`. Webhooks tratados: só `order.*` e `product.*`.
- **`products`:** catálogo da IA (setor, preço em texto, lote mínimo), **sem ligação** com `bling_products`.
- **RPC de recompra:** `get_avg_repurchase_cycle_days(p_sold_by)` — `mig/20260824_repurchase_por_vendedor.sql:17-44`.
- **"Já era cliente":** a trigger `trg_sales_marca_ja_era_cliente` marca `leads.ja_era_cliente=true` quando há venda não cancelada em data anterior à criação do lead — `20261006_call_semanal_base.sql:22-70`.

**E. Relacionamento / follow-up / disparos**
- **`follow_up_jobs`:**
  - `job_type`: padrão da IA, `handoff_rescue`, `ai_scheduled_return`, `lp_welcome`, `joao_reposicao`;
  - também `sequence` (número do toque), `status`, `cancel_reason` e `wamid`;
  - valores de `cancel_reason`: `client_replied`, `handoff`, `ai_disabled`, `rescheduled`, `wrong_number`, `optout`, `manual`, …
  - Fonte: grep em `V/backend/app`.
  - `follow_up_jobs_incidente_20261003` parece um backup de incidente: deve ser excluída das análises.
  - Cadências do João ficam em `followup_joao_cadencia/toque/ajustes` (funil × cadência × toque × dias × template).
- **Detalhes de `follow_up_jobs`:**
  - `status`: `pending`, `processing`, `sent`, `cancelled`, `awaiting_reopen` — `mig/20260704_followup_atomic_claim.sql:14-15`;
  - `job_type`: `standard` (4 toques da IA — `V/backend/app/follow_up/cadence.py:66-119`), `handoff_rescue`, `lp_welcome`, `ai_reengage`, `ai_scheduled_return` e `joao_*` (`joao_novo`, `joao_em_conversa`, `joao_proposta`, `joao_reposicao`, `joao_em_atencao`) — `scheduler.py:103-110,724-738`;
  - o `metadata` do João traz funil, cadência, toque, template, deal e etapa;
  - **não existe coluna de resposta**: medir pela 1ª `messages.role='user'` após `sent_at`.
- **`broadcasts` / `broadcast_leads`:**
  - `broadcast_leads.status`: pending, processing, sent, delivered, failed, `marketing_capped` (erro Meta 131049);
  - `delivered_at` vem do webhook de status (por wamid);
  - `first_replied_at` é gravado na resposta do lead dentro de 48h após o envio (mais um job de catch-up);
  - **`deal_moved_at` é gravado no ENVIO, quando o worker move o card para `move_to_stage_id`. Não é sinal de conversão.**
  - Fontes: `V/backend/app/broadcast/service.py:255-304`, `worker.py:542-614,1824-1858`.
- **`campaigns` / `campaign_nodes` / `campaign_enrollments` / `campaign_execution_log`:** cadências de automação de WhatsApp (**não** campanhas de anúncio). Os nós são gatilho/ação/condição — `V/backend/app/campaigns/node_registry.py:217-667`.
  - `lead_daily_sends` controla o limite de frequência.
  - `conversations.campaign_id` é legado (aponta para a tabela antiga, que foi apagada).
- **`env_tag`** = `production` | `dev`. Existe em `broadcasts`, `campaigns`, `follow_up_jobs` e `campaign_enrollments`. Filtrar `production`; `broadcast_leads` filtra via o `broadcasts` pai.
- **Templates:** a categoria (MARKETING/UTILITY) define o preço Meta, mas o custo **não é armazenado**.
- **Fluxo de botões:** `agent_profiles.kind` = `llm` | `button_flow`.
- **`system_alerts`:** inclui `handoff_sla_breach`, `ai_unresponsive`, `llm_budget_exceeded`, etc.

### Inferences
- Sem tabela `users` no `public`, a identidade do vendedor está em `auth.users`: e-mail, `raw_user_meta_data.full_name` e `app_metadata.role`. Vendas e orçamentos usam **e-mail**; `leads.assigned_to`, `channels.owner_user_id` e `pipelines.owner_user_id` usam **uuid**; `deals.assigned_to` é **texto** de conteúdo incerto. A camada semântica precisa de uma dimensão `dim_vendedor` montada a partir de `auth.users`, ou de uma tabela de-para manual se o agente de análise não tiver acesso ao schema `auth`.
- Como todo pedido Bling vira lead, `leads` mistura leads de marketing com clientes históricos importados (`channel='bling'`, `metadata.origem` ∈ {bling_webhook, reativacao_bling}). Taxas de conversão de marketing precisam excluir esses leads.

### Gaps
- `ad_conversions` e `ad_conversion_values` não têm código-fonte local: semântica não verificada.
- `follow_up_jobs_incidente_20261003` não aparece no repositório. Presume-se que seja um backup manual de incidente.
- Valores reais (distribuição) de `traffic_type` (código: paid/organic/NULL — `V/backend/app/leads/service.py:441-463`), `deals.category` e `deals.assigned_to` não foram verificados com dados.
- O `entrada` em `lead_events` só é gerado para leads **com algum sinal de rastreio**. Leads de WhatsApp direto sem rastreio não aparecem em `lead_primeira_origem`. As entradas do Google não trazem `campanha_id`/`campanha_nome` (a campanha só é preenchida via `meta_ad_campaigns`).
- `deals.closed_at` é inconsistente: o Kanban só preenche em `fechado_ganho`/`fechado_perdido`, e 38 deals tinham `closed_at` em etapa não terminal (nota de 10/09, `mig/20260904_esteiras_vendedor.sql`). `deals.stage` (texto) é coluna morta: usar `stage_id`.

---

## 2. Matriz de viabilidade

Legenda:
- ✅ viável agora
- 🟡 parcial (falta algo ou há ambiguidade)
- ❌ inviável sem nova fonte

| Análise | Status | Tabelas/colunas | O que falta / ressalva |
|---|---|---|---|
| **CPL** (custo por lead) por canal/campanha/dia | ✅ (Meta/Google) | `ad_spend.cost` por campaign×date; leads pagos via `lead_primeira_origem` ou atribuição (`campanha_manual_*` > `meta_ad_id`→`meta_ad_campaigns` > `utm_campaign`→match em `ad_spend`) | Google depende de matching por nome (pode dar null). Sem custo por anúncio ou conjunto. `ad_spend` só tem histórico desde que o sync roda, com janela de 30 dias de upsert. Já existe cálculo em `traffic_report.py:378` (`cpl` = investimento / leads pagos). |
| **CAC** | 🟡 | `ad_spend` + primeira venda do lead (`sales` não cancelada) | Só CAC de **mídia**: não há custo de time, ferramenta ou IA (a IA dá para somar via `token_usage`). É preciso decidir: o cliente que "já era cliente" conta? (`ja_era_cliente`). O código atual usa `cac = investimento / clientes pagos` (`traffic_report.py:379`). |
| **ROAS** | 🟡 | `sales.value` por lead atribuído / `ad_spend` | `traffic_report.py:278,304` faz receita/investimento. **Não filtra `status='cancelada'`** (`traffic_report.py:573-604`). `sales.value` inclui frete (e agora há `sales.freight`). Venda Bling de lead pago só casa se o contato Bling for ligado ao mesmo lead (match por documento/telefone). |
| **Lead → venda por campanha** | ✅/🟡 | `lead_primeira_origem` + `sales` | Janela de atribuição não definida no código (modo "sale" × "lead" no relatório). Atribuição é por primeira origem; multi-toque só pela timeline `entrada`. |
| **Speed-to-lead** (1º contato) | ✅ IA / 🟡 humano | `messages` (1ª `role='user'` × 1ª `sent_by='agent'`); `conversations.first_seller_response_at`; marco do handoff (mensagem de sistema) | `leads.first_response_at` nunca é escrito (ignorar). Para o humano, medir a partir do handoff. O vendedor costuma responder no canal próprio (`channels.mode='human'`, outra conversa), e o `dashboard_kpis` só mede na mesma conversa. Horário útil via `dashboard_business_seconds` + `sla_seller_config`. |
| **Tempo de 1ª resposta / SLA** do vendedor | ✅ | `conversations.first_seller_response_at`, `last_customer_message_at`, `messages.sent_by='seller'`, `sla_*` | Cada resposta exige uma window function sobre `messages`. `first_seller_response_at` vale para a conversa inteira, não para cada pergunta. |
| **Conversão e ticket por vendedor** | 🟡 | `sales.sold_by` (e-mail), `leads.assigned_to` (uuid), `deals` | Vendas `origin='bling'` **sem sold_by**. É preciso atribuir por `leads.assigned_to` ou por `bling_contacts.vendedor_id`→`bling_seller_map`. Mapear uuid↔e-mail exige `auth.users`. |
| **Conversão entre etapas do funil** | 🟡 | `lead_events` tipo `etapa` (de/para stage_id); `pipeline_stages.key/order_index` | A timeline só existe desde a migration P3 (out/2026) e do backfill que ela trouxe. Antes disso só há a etapa atual. Etapas foram renomeadas, apagadas e fundidas em 10/09: usar `key`, nunca `label`. |
| **Tempo em etapa** | 🟡 | `lead_events` `etapa` (occurred_at consecutivos); `deals.entered_stage_at` (só atual) | Igual ao item acima. O PATCH do Kanban não escreve `deals.stage` (só `stage_id`), então use `stage_id`. |
| **Motivos de perda** | 🟡 | `deals.lost_reason`, `closed_at`; `follow_up_jobs.cancel_reason`; `leads.opt_out*` | `lost_reason` é texto livre; precisa de categorização (LLM ou regex). Opt-out vai para o pipeline Blacklist. |
| **Ticket médio** | ✅ | `sales.value` (status ≠ cancelada) | Separar frete (`sales.freight`, recente). Separar por conta Bling (`bling_account`) e por canal. |
| **Receita por canal / vendedor / conta** | ✅ canal e conta / 🟡 vendedor | `sales` + atribuição do lead; `sales.bling_account`, `origin` | Vendedor: ver acima. Pedido Bling sem lead não entra (`sales.lead_id` NOT NULL). |
| **Recompra** (taxa e ciclo) | ✅ | `sales` por `lead_id` (e `lead_bling_contacts` / `bling_contact_id`); RPC `get_avg_repurchase_cycle_days` | O backfill Bling cobre só 12 meses e só a conta `default`. Duplicidade de lead para o mesmo cliente (há merges: `mesclagem`) pode quebrar a contagem. |
| **Coortes** (por mês da 1ª compra ou entrada) | ✅/🟡 | `sales.sold_at`, `leads.created_at`, `lead_primeira_origem.occurred_at` | Histórico limitado pela janela do backfill. Para leads importados do Bling, `leads.created_at` é a data de importação, não a de aquisição. |
| **LTV** | 🟡 | soma de `sales.value` por cliente | Histórico curto (12 meses na conta default). Sem margem não dá LTV de contribuição. |
| **RFM** | ✅ | `sales` (recência, frequência, valor) + `lead_qualification_scores.segment` | Ressalva de histórico. Unificar cliente entre as duas contas Bling (documento em `bling_contacts.doc_digits`). |
| **Churn B2B** | 🟡 | intervalo de recompra por cliente (atacado/PL); pipelines Reposição/Recuperação | Não há definição formal de "ativo". Proxy: sem compra há mais de N × ciclo médio. Segmento B2B depende de `leads.stage` / score / pipeline. |
| **Curva ABC** (produto) | 🟡 | `sale_items` (codigo, quantidade, total) + `bling_products` | Só vendas com itens, ou seja, as ligadas ao Bling. Vendas manuais só têm texto. Não há categoria nem família de produto além de `id_produto_pai`. |
| **Cobertura de estoque** | ❌/🟡 | `bling_products.saldo_virtual` (foto atual) + giro por `sale_items` | Sem histórico de saldo, sem movimentações, sem depósitos, sem pedido de compra ou lead time. Dá para fazer um snapshot de cobertura (saldo / venda média diária), mas não uma série. |
| **Margem** | ❌ | — | Custo (`precoCusto`) não é sincronizado. CMV manual existe só no beeinside (`product_cmv`, por nome de produto), em outro banco. Sem impostos, taxas de pagamento nem custo de frete. |
| **Performance de follow-up / disparo** | ✅ | `follow_up_jobs` (sent_at, sequence, cancel_reason `client_replied`), `messages`; `broadcast_leads` (delivered_at, first_replied_at, deal_moved_at) → `sales` | Resposta ao follow-up: inferir pela próxima `messages.role='user'` após `sent_at`. Filtrar `env_tag` de produção. Excluir a tabela de incidente. |
| **Qualificação e handoff da IA** | ✅/🟡 | `leads.metadata->'handoff'->>'at'` (+ vendedor, segmento, motivo); mensagem de sistema `[encaminhar_humano] Lead encaminhado%`; `[qualificar_lead]`; `lead_qualification_scores`; `dashboard_kpis` já calcula | Não há evento em `lead_events`. O carimbo do metadata guarda só o **último** handoff. Para o histórico, usar as mensagens de sistema. "Qualificado" tem 3 sentidos concorrentes (mensagem `[qualificar_lead]`, key `qualificado`, score). Score só para `atacado`. |
| **Custo de tokens** (por lead, por venda, por etapa) | ✅ | `token_usage.total_cost` (USD), `model`, `call_type`, `stage`, `lead_id` | Conversão para BRL: há módulo `backend/app/fx`, mas não há tabela de câmbio no `public`. Chamadas sem `lead_id` (resumos, classificações) precisam de rateio. |
| **Custo de mensagens WhatsApp** (Meta) | ❌ | `message_templates.category` (MARKETING/UTILITY), `broadcast_leads` | Preço por conversa/template não é armazenado. Exige tabela de preço Meta ou billing da WABA. |
| **Origem orgânica × paga e "já era cliente"** | ✅ | `fn_lead_canal`, `leads.ja_era_cliente*` | `ja_era_cliente` null = desconhecido. O sistema só grava TRUE. |

### Inferences
- O que está mais pronto: **CPL, ROAS bruto, ticket, receita por canal, recompra/RFM, follow-up/disparo e custo de IA**. Os bloqueios reais são **margem, estoque histórico, custo de WhatsApp e vendedor nas vendas Bling**.
- O relatório de tráfego existente define "closer" pela key `qualificado` (`traffic_report.py:93,552-570`). Os funis do João não têm essa key (usam `novo`/`respondeu`/…), então a métrica "custo por closer" pode subcontar leads que foram direto para as esteiras. **Inferência a confirmar com dados.**

### Gaps
- Sem acesso ao banco, não sei a data de início do `ad_spend` nem o grau de preenchimento de `meta_ad_id`, `gclid` e `utm_campaign`.

---

## 3. Definições de negócio implícitas no código

### Takeaway
O código já tem definições operacionais para quase todos os conceitos. Os únicos sem marco temporal explícito são o **handoff** e o **"cliente ativo"**.

### Cited Findings
- **Lead** = linha em `leads` (um por telefone/wa_id; há merges registrados como `mesclagem`). Inclui contatos inbound de WhatsApp, LP, importações e clientes Bling auto-criados (`contacts.py:508-581`).
  - Para marketing, considerar "lead novo" = evento `entrada` (o insert do lead com rastreio, ou a mudança de ctwa_clid/gclid/fbclid/utm) — `20261006b_lead_timeline_triggers.sql:8-11`.
- **Lead que conversou** = conversa com `last_customer_message_at` não nulo (`traffic_report.py:541-550`).
- **Lead qualificado**, com duas noções:
  1. operacional: o card movido para a key `qualificado` (`mark_deal_qualificado`, `service.py:1450`), também usada como marco "closer" no relatório (`traffic_report.py:93`);
  2. score: `lead_qualification_scores.priority` ∈ {high, maximum} ou `final_score >= 5`, `is_provisional=false` (`mig/20260921_valeria_score.sql:30-95`).
- **Handoff para o closer** = a tool `encaminhar_humano`, também chamada em cascata por `qualificar_lead`:
  - `human_control=true`, `ai_enabled=false`, `status='converted'`;
  - `assigned_to` = dono do pipeline do segmento;
  - card criado ou movido no funil do vendedor;
  - `metadata.handoff.at`;
  - mensagem de sistema `[encaminhar_humano] …`;
  - cancelamento dos follow-ups com reason `handoff`.
  - Fontes: `tools.py:690-989`; `handoff.py:17-48`.
  - Não grava evento próprio em `lead_events`.
  - O dashboard oficial usa a mensagem de sistema como marco (`mig/20260712_dashboard_rpcs.sql:112-117`).
- **Venda** = linha em `sales` com `status <> 'cancelada'`. A data é `sold_at`: para o Bling é a data do pedido às 12:00 UTC; para a venda manual é 12:00 local (`20261006_call_semanal_base.sql:30-34`). `origin` ∈ {manual, crm, bling}.
- **Atribuição de campanha** = `campanha_manual_*` (vence tudo) → `meta_ad_id`→`meta_ad_campaigns` → gclid/UTM Google com match de nome em `ad_spend` → UTM → orgânico/sem rastreio. Modelo **primeiro toque** via `lead_primeira_origem`.
- **Vendedor:**
  - em vendas e orçamentos: e-mail (`sold_by`, `created_by`);
  - no lead: `assigned_to` uuid (dono do pipeline do segmento, com fallback para o João — `service.py:987-1017`);
  - no Bling: `bling_seller_map` e `bling_contacts.vendedor_id`.
- **Já era cliente** = venda não cancelada em data anterior à criação do lead (automático) ou marcação do vendedor.

### Inferences
- Recomendo fixar na camada semântica:
  - `handoff_at` = 1ª mensagem `role='system'` com `content LIKE '[encaminhar\_humano] Lead encaminhado%'` (marco do dashboard). Fallbacks, nesta ordem: `metadata.handoff.at` (só o último handoff), 1ª mensagem `sent_by='handoff'`;
  - `cliente_ativo_b2b` = compra nos últimos max(60 dias, 1,5 × ciclo médio do cliente).

### Gaps
- `leads.first_response_at` não é escrito por nenhum código: não serve como métrica.
- `deals.assigned_to` (texto) tem conteúdo incerto, editado só na UI. Para o vendedor do lead, usar `leads.assigned_to`.
- `sales.status` também pode ser `pendente_bling` (exibido no front), mas não achei código que o grave. `sales.lead_id` é NOT NULL. A venda manual exige deal; a venda `bling` não tem deal.

---

## 4. Camada semântica proposta (views)

Convenções:
- excluir `sales.status='cancelada'`;
- filtrar `env_tag` de produção;
- converter datas para `America/Sao_Paulo`;
- usar `pipeline_stages.key`, não `label`.

1. **`dim_vendedor`** — de-para uuid ↔ e-mail ↔ nome ↔ papel ↔ id de vendedor Bling.
   - Fontes: `auth.users` (ou tabela manual) ⨝ `bling_seller_map` (user_email) ⨝ `bling_sellers`; `sla_seller_config.display_name`.
2. **`dim_campanha`** — campanhas únicas por plataforma.
   - Fontes: `ad_spend` (distinct platform, campaign_id, campaign_name) ∪ `meta_ad_campaigns`.
3. **`vw_lead_atribuicao`** — canal, plataforma, campaign_id e nome por lead, com uma flag de qualidade (manual/ad_id/clid/utm-match/sem).
   - Ordem: `campanha_manual_*` > `meta_ad_id`→`meta_ad_campaigns` > `lead_primeira_origem` > `fn_lead_canal(...)` + match de `utm_campaign` em `dim_campanha`.
   - Também traz as flags `is_importado_bling` (`channel='bling'` ou `metadata.origem` em bling_webhook/reativacao_bling) e `ja_era_cliente`.
4. **`fct_spend_diario`** — `ad_spend` por platform × campaign × date (BRL).
5. **`fct_leads_diario`** — contagem de entradas (`lead_events` `entrada`, occurred_at) por dia × canal × campanha, excluindo importados.
6. **`vw_cpl_campanha`** — fct_spend_diario ⨝ fct_leads_diario por (platform, campaign_id, data/semana/mês).
7. **`fct_vendas`** — uma linha por venda válida.
   - Fonte: `sales` (status ≠ cancelada), com `valor_liquido_frete = value - coalesce(freight,0)`, `bling_account` e `origin`.
   - `vendedor_email` = coalesce(sold_by, e-mail via `bling_contacts.vendedor_id`→`bling_seller_map`, e-mail de `leads.assigned_to`), com coluna `vendedor_fonte`.
   - Também traz o número da compra do cliente (row_number por lead) e a flag `primeira_compra`.
8. **`vw_cliente`** — cliente unificado.
   - Fontes: `leads` ⨝ `lead_bling_contacts` / `bling_contacts` (doc_digits) para juntar contas e merges.
   - Traz 1ª e última compra, nº de pedidos, receita total e segmento (`lead_qualification_scores.segment`, `leads.stage`).
9. **`vw_roas_campanha`** — vw_lead_atribuicao ⨝ fct_vendas (janela configurável a partir da `entrada`) ⨝ fct_spend: receita, ROAS e CAC de mídia por campanha/mês.
10. **`vw_funil_marketing`** — por lead pago: entrada → conversou (`conversations.last_customer_message_at`) → qualificado (score ≥5 ou etapa key `qualificado`) → handoff → proposta (`quotes`, ou etapa `proposta_enviada`) → venda; por campanha.
11. **`vw_handoff`** — uma linha por handoff: lead_id, `handoff_at` (definição da seção 3), vendedor, segmento, motivo, origem (IA ou button_flow) e score.
    - Fontes: `messages` (sistema `[encaminhar_humano]…`, `sent_by='handoff'`), `leads.metadata->'handoff'`, `leads.assigned_to`, `lead_qualification_scores`.
12. **`vw_tempo_resposta`** — por lead: 1ª mensagem do cliente, 1ª resposta da IA (`sent_by='agent'`) e 1ª resposta do vendedor após o handoff, em minutos corridos e úteis.
    - A resposta do vendedor (`sent_by='seller'`) deve ser buscada **em qualquer conversa do lead**, inclusive no canal `mode='human'` do vendedor, não só na conversa da IA.
    - Fontes: `messages`, `conversations`, `channels.mode/owner_user_id`, `dashboard_business_seconds`, `sla_seller_config`, `sla_overrides`, `sla_settings`.
13. **`vw_tempo_resposta_mensagem`** — para cada mensagem `role='user'`, a próxima resposta `seller`/`agent` (lead/window), para medir o SLA contínuo.
14. **`fct_transicoes_etapa`** — `lead_events` `etapa` com de/para `stage_id` ⨝ `pipeline_stages` (key, order_index) ⨝ `pipelines`, e `lead(occurred_at)` para a duração na etapa.
15. **`vw_conversao_etapas`** — taxas key→key por pipeline e coorte de entrada no funil (a partir da 14).
16. **`vw_perdas`** — deals com `closed_at`, `lost_reason` bruto e `lost_reason_categoria` (CASE/regex inicial), pipeline e vendedor; mais opt-outs (`leads.opt_out_at`, `opt_out_channel`).
17. **`vw_vendedor_desempenho`** — por vendedor e mês: leads atribuídos, handoffs, propostas (`quotes.created_by`), vendas, receita, ticket, conversão e tempo de resposta.
18. **`vw_rfm_cliente`** — recência, frequência e valor com quintis, a partir de `vw_cliente` / `fct_vendas`.
19. **`vw_coorte_compra`** — mês da 1ª compra × meses desde então: retenção e receita (`fct_vendas`).
20. **`vw_churn_b2b`** — clientes B2B (segmento atacado/PL/pipelines Reposição) com ciclo médio próprio (LAG em `sold_at`), dias desde a última compra e status ativo, em risco ou churn.
21. **`fct_itens_vendidos`** — `sale_items` ⨝ `fct_vendas` ⨝ `bling_products` (account, id), com nome, `id_produto_pai` e preço de tabela × praticado (desconto).
22. **`vw_curva_abc`** — receita acumulada por produto (pai/SKU) a partir da 21, classes A/B/C.
23. **`vw_cobertura_estoque`** — `bling_products.saldo_virtual` / média diária vendida em 30/90 dias (fct_itens_vendidos). É uma foto do momento.
24. **`vw_followup_desempenho`** — `follow_up_jobs` (status sent, prod; sem a tabela de incidente) por job_type × sequence: enviados, respondidos (próxima `messages.role='user'` em até 72h ou `cancel_reason='client_replied'`) e vendas em até 30 dias.
25. **`vw_disparo_desempenho`** — `broadcasts` (env_tag='production') ⨝ `broadcast_leads`: enviado, entregue, capado (`marketing_capped`), respondeu (`first_replied_at`), avanço real do card depois da resposta (`lead_events` `etapa` com occurred_at > first_replied_at), venda em até N dias (fct_vendas); por template e categoria.
    - Não usar `deal_moved_at` como conversão: ele é gravado no envio.
26. **`vw_custo_ia`** — `token_usage` por dia × model × call_type × stage, e por lead; custo por lead qualificado, por handoff e por venda (⨝ vw_handoff, fct_vendas). Em USD, com BRL opcional via tabela de câmbio a criar.

### Inferences
- As views 3, 7 e 11 são a base: concentram as ambiguidades de atribuição, vendedor e handoff. Convém criá-las antes das demais e validá-las com amostras manuais.

### Gaps
- Não sei se o agente de análise tem acesso ao schema `auth`. Se não tiver, `dim_vendedor` precisa ser uma tabela mantida à mão.

---

## 5. Lacunas de dados e integrações necessárias

### Takeaway
Para fechar o quadro financeiro faltam custo de produto, histórico de estoque e o vendedor nas vendas Bling. No marketing, falta granularidade de anúncio e métricas de entrega.

### Cited Findings
- **Custo e margem:** `bling_products` não traz `precoCusto` (`products.py:23-41`). O CMV manual vive só no beeinside (`product_cmv`, chaveado por nome), em outro banco.
- **Estoque:** só o `saldo_virtual` atual. Não há movimentações, depósitos, compras nem lead time.
- **Vendedor em pedido Bling:** o import não preenche `sold_by` (`mig/20260824_sales_sold_by_normalizacao.sql:4`).
- **Histórico Bling:** o backfill é de 12 meses e só da conta `default`; a conta `secundaria` (Café Rural) não tem histórico (`backfill.py`).
- **Quotes do ERP:** propostas criadas direto no Bling não são sincronizadas.
- **Ads:** `ad_spend` só tem campanha × dia e custo. Faltam conjunto, anúncio, impressões, cliques e o próprio campaign_id no lead Google. `meta_webhook_logs` tem retenção de 15 dias, mitigada por `meta_referrals_arquivo`.
- **WhatsApp:** não há custo por conversa/template.
- **Câmbio:** não há tabela de câmbio para converter `token_usage` (USD).
- **Loja online:** `loja_api` usa outro banco, indisponível. A receita do e-commerce B2C fica fora, salvo se o pedido passar pelo Bling.
- **Notas fiscais:** NF-e (faturamento real, impostos) só é lida pelo beeinside, direto da API Bling.

### Inferences — integrações recomendadas (por prioridade)
1. **Custo de produto:** sincronizar `precoCusto` (ou custo médio) do Bling para `bling_products`, ou ler o `product_cmv` do beeinside com de-para por SKU.
2. **Vendedor nas vendas Bling:** gravar `pedido.vendedor.id` no import e mapear via `bling_seller_map`.
3. **Backfill Bling:** cobrir a conta `secundaria` e estender para mais de 24 meses (coortes, LTV, churn).
4. **Snapshot diário de estoque:** tabela `bling_estoque_diario` (produto × depósito × saldo).
5. **Ads mais granulares:** ampliar o sync para ad set/ad, impressões, cliques e conversões da plataforma; no Google, o campaign_id via ValueTrack (`{campaignid}` nas UTMs) para não depender de match por nome.
6. **Evento explícito de handoff:** gravar `lead_events.event_type='handoff'` em `encaminhar_humano`, com vendedor e motivo.
7. **Motivo de perda:** padronizar `lost_reason` em enum + texto livre.
8. **Custos fixos:** tabela de câmbio diário (USD/BRL) e tabela de preço Meta por categoria de template.
9. **E-commerce:** acesso de leitura ao banco da loja, ou garantir que todos os pedidos da loja entrem no Bling com origem identificável.
10. **Unificação de cliente:** chave de documento (CNPJ/CPF) entre contas Bling e leads mesclados.

### Gaps
- Não foi possível quantificar, sem consulta, quanto da base de vendas tem `lead_id` atribuível a campanha, nem quanto do spend é Meta × Google.
