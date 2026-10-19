# Funil de vendas, desempenho de vendedores e analytics de atendimento no WhatsApp (Café Canastra)

Contexto: torrefação de café especial; IA qualifica leads no WhatsApp e passa para closers humanos (B2C e B2B atacado/private label). Pesquisa feita em out/2026. Observação geral: a maior parte dos "benchmarks" públicos de vendas e chatbot vem de blogs de fornecedores sem metodologia; quando é o caso, isso está marcado. Fórmulas sem fonte estão em "Inferências" (são definições padrão propostas para o painel, não números de mercado).

## 1. Funil: conversão por etapa, tempo na etapa, velocidade do pipeline, win rate, motivos de perda, negócios parados, cobertura, leads sem resposta

### Takeaway
A fórmula de mercado para velocidade do pipeline é (oportunidades qualificadas × ticket médio × win rate) ÷ ciclo de vendas em dias, e o próprio Pipedrive aponta que encurtar o ciclo costuma ser a alavanca mais rápida. No Brasil, as dores declaradas pelas equipes de vendas são exatamente as que esse painel ataca: conversão (22%), tempo de primeiro contato (12%) e entender os motivos de perda (11%). Win rate só se compara entre empresas quando o denominador é definido do mesmo jeito; para a Canastra, o painel deve medir o win rate separado por segmento (B2C, atacado, private label).

### Cited Findings
- Fórmula do Pipedrive: velocidade = (oportunidades qualificadas × ticket médio × win rate) ÷ duração do ciclo. No exemplo, 40 oportunidades × US$8.000 × 25% ÷ 45 dias dá ≈ US$1.778/dia. Subir o win rate de 25% para 30% leva a ≈ US$2.133/dia, e cortar o ciclo de 45 para 36 dias leva a ≈ US$2.222/dia. O guia diz que o ciclo costuma ser a alavanca mais rápida. Ticket médio = receita dos negócios ganhos ÷ número de negócios ganhos no período — [Pipedrive, sales pipeline metrics](https://www.pipedrive.com/en/blog/sales-pipeline-metrics)
- Um win rate "misturado" esconde problemas; o recomendado é segmentar por tipo de negócio, região ou nível do vendedor. Também é preciso documentar onde o ciclo começa e não mudar essa definição no meio do período (blogs de fornecedores) — [Prospeo, sales velocity](https://prospeo.io/s/sales-velocity); [Salesmotion](https://salesmotion.io/blog/pipeline-velocity)
- Win rate de referência (fornecedor, metodologia fraca): média de 17–21%, com os melhores acima de 30%. Outra leitura diz que a faixa mais comum caiu para 21–25% em 2025, ante 31–40% no ano anterior. As fontes divergem porque usam denominadores diferentes — [Prospeo, win rate by industry](https://prospeo.io/s/sales-win-rate-by-industry)
- Panorama RD Station 2025 (1.504 respondentes, Brasil):
  - 72% das empresas não bateram a meta de vendas em 2024 (74% em 2023, 71% em 2022).
  - Atingimento médio de meta: 28%. Por porte: pequenas 28%, empresas de até 3 funcionários 12%, grandes 52%.
  - Maior dor em vendas: aumentar a taxa de conversão (22%), melhorar o tempo de primeiro contato e perder menos oportunidades (12%), automatizar e escalar (11%), entender os motivos de perda e ter um processo de recuperação (11%), ter etapas de funil claras (8%), ter dados confiáveis (8%), encurtar o ciclo (5%).
  - Oportunidades de melhoria citadas: mais treinamento (41%), rever a metodologia (35%), usar IA (33%) e integrar ferramentas e dados (24%) — [RD Station, Panorama 2025, Vendas/Cenário](https://www.rdstation.com/pesquisas/panoramas-rdstation-2025/vendas/cenario/)
- 58% das empresas brasileiras ainda não usam CRM (Panorama RD Station, citado no blog do Sales Day 2025) — [RD Station, Sales Day 2025](https://www.rdstation.com/blog/vendas/sales-day-2025/)
- Leads que nunca recebem resposta: na auditoria do HBR (2011, dado antigo) com 2.241 empresas dos EUA, 23% nunca responderam ao lead. O tempo médio de primeira resposta foi de 42 h. Distribuição: 37% responderam em até 1 h, 16% entre 1 e 24 h e 24% em mais de 24 h. Esses números vêm de resumos secundários, porque a página do HBR fica atrás de paywall — [ainora.lt, compilação](https://ainora.lt/blog/lead-response-time-statistics-every-study-2026); [HBR, The Short Life of Online Sales Leads (2011)](https://hbr.org/2011/03/the-short-life-of-online-sales-leads)

### Inferências
- Painel de funil sugerido (definições do painel, não de mercado):
  - **Conversão por etapa** = leads que chegaram à etapa N+1 ÷ leads que entraram na etapa N, numa coorte por semana de entrada. Etapas propostas: lead novo → respondido pela IA → qualificado → passado ao closer → proposta/orçamento → ganho/perdido.
  - **Tempo na etapa:** mediana e P90 de (data de saída − data de entrada) por etapa. A mediana é preferível à média, porque no WhatsApp a distribuição tem cauda longa.
  - **Negócios envelhecidos/parados** = negócios abertos sem mensagem nem mudança de etapa há mais de X dias. Sugestão: B2C acima de 3 dias e B2B acima de 7–14 dias. Gerar uma lista diária por closer.
  - **Cobertura do pipeline** = valor ponderado do pipeline aberto ÷ meta restante do período (multiplicadores típicos de 3x valem para B2B; não encontrei fonte sólida para esse número e ele não foi verificado).
  - **Previsão de receita** = Σ (valor do negócio × win rate histórico da etapa).
  - **Leads nunca respondidos** = leads com mensagem de entrada e sem nenhuma saída (da IA ou de humano) em 24 h. Com a IA respondendo, o alvo é ~0%; o risco real passa a ser o lead que a IA qualificou e nenhum humano assumiu.
  - **Motivos de perda:** campo obrigatório ao marcar "perdido", com lista fechada (preço, frete/prazo, pedido mínimo, sumiu/sem resposta, comprou do concorrente, não era o perfil, produto indisponível). Cruzar com o motivo que a IA extrai do chat (seção 5).
- Calcular a velocidade do pipeline separadamente para B2C (ticket baixo, ciclo de horas a dias) e B2B/private label (ticket alto, ciclo de semanas). Misturar os dois gera um número sem significado.

### Gaps
- Não encontrei benchmark público brasileiro de conversão lead→venda por etapa, nem de ciclo de vendas, para varejo de café, alimentos ou atacado. O Panorama RD Station traz a conversão só como "dor", sem a taxa medida no capítulo aberto.
- Não encontrei fonte confiável para o múltiplo de cobertura de pipeline (3x) aplicado a PMEs.

## 2. Speed-to-lead e tempo de resposta

### Takeaway
A evidência clássica é forte na direção, mas antiga e em parte feita por fornecedor. Responder em até 5 min em vez de 30 min aumentou em ~21x a chance de qualificar o lead (InsideSales/Oldroyd, 2007, dado de fornecedor). Responder em até 1 h tornou a empresa ~7x mais propensa a qualificar o lead do que esperar mais uma hora (HBR, 2011). No Brasil, o tempo de primeiro contato é a segunda maior dor das equipes de vendas, e ~25% das mensagens no WhatsApp chegam fora do horário comercial. Por isso a IA 24/7 cobre um buraco real, desde que o repasse noturno para o closer também tenha SLA.

### Cited Findings
- **Estudo InsideSales.com com o Dr. James Oldroyd (2007):**
  - Dados: 3 anos, 6 empresas, mais de 15.000 leads e mais de 100.000 tentativas de ligação.
  - A chance de qualificar o lead foi 21x maior com contato em 5 min do que em 30 min. A chance de contatar o lead foi 100x maior.
  - Foi apresentado em evento, não publicado em periódico revisado, e é frequentemente atribuído por engano ao MIT/HBR. Trate como evidência direcional — [ainora.lt, 5-minute study](https://ainora.lt/blog/lead-response-time-5-minutes-study-2026); [Retell AI, speed to lead](https://www.retellai.com/blog/speed-to-lead)
- **HBR, "The Short Life of Online Sales Leads" (Oldroyd, McElheran, Elkington, mar/2011):** empresas que tentaram contato em até 1 h foram ~7x mais propensas a qualificar o lead do que as que esperaram uma hora a mais. A base citada é de 1,25 milhão de leads em 42 empresas (29 B2C e 13 B2B). As fontes secundárias divergem no tamanho da amostra (1,25 mi vs. 2,24 mi), e não consegui confirmar no original, que está atrás de paywall — [HBR](https://hbr.org/2011/03/the-short-life-of-online-sales-leads); [pipl.ai, glossário](https://pipl.ai/glossary/lead-response-time)
- A afirmação de "+400% de conversão respondendo em 5 min" e a frase "78% compram de quem responde primeiro" não têm fonte primária rastreável. Não usar — [pipl.ai](https://pipl.ai/glossary/lead-response-time); [Huble](https://huble.com/blog/hubspot-lead-reaction)
- **Chat Commerce Report 2026 (OmniChat; mais de 1 bi de mensagens e 51 mi de conversas em 2025, 96% no WhatsApp, Brasil):**
  - ~25% das mensagens enviadas a marcas chegaram fora do horário comercial (noites e fins de semana).
  - 19,5% do volume semanal cai na segunda-feira.
  - O volume de conversas cresceu 71% entre 2023 e 2025, enquanto o número de atendentes cresceu 18% — [ABC da Comunicação](https://www.abcdacomunicacao.com.br/sem-horario-comercial-vendas-migram-para-o-whatsapp-e-ia-impulsiona-resultados-aponta-chat-commerce-report-2026/)
- **Consumidor brasileiro:**
  - 83% deixariam uma marca após uma única experiência ruim (Zendesk CX Trends 2025), contra 58% na Europa e 51% na América do Norte — [Folha PE](https://www.folhape.com.br/economia/cx-trends-2025-america-latina/401720/); [TI Inside](https://tiinside.com.br/14/01/2025/america-latina-lidera-em-experiencia-do-cliente-e-adocao-de-ia/)
  - "Falta de retorno sobre reclamações e solicitações" foi citada por 18% como queixa, e "resolução rápida" é a ação mais desejada, com 37% (CX Trends 2025 Octadesk/Opinion Box) — [Propmark](https://propmark.com.br/?p=124860)
- WhatsApp no Brasil: está em 99% dos smartphones e 97% dos usuários o abrem ao menos uma vez por dia (Panorama Mobile Time/Opinion Box; pesquisa de jun/2025 com 1.126 usuários) — [Consumidor Moderno](https://consumidormoderno.com.br/whatsapp-brasileiro-tempo-uso/); [Canaltech](https://canaltech.com.br/apps/o-que-os-brasileiros-mais-fazem-no-whatsapp-segundo-pesquisa/)

### Inferências
- **Métricas de tempo:**
  - **FRT da IA** (primeira resposta) = mediana de (1ª mensagem de saída − 1ª mensagem de entrada). Deve ficar em segundos.
  - **FRT humano após o repasse** = mediana de (1ª mensagem do closer − horário do repasse). Esta é a métrica que mais importa no modelo da Canastra.
  - **Tempo de resposta durante a conversa** = mediana dos intervalos entre a mensagem do cliente e a resposta do closer.
  - **AHT/tempo de conversa** = da 1ª à última mensagem da conversa (no WhatsApp é assíncrono; usar mais como sinal de esforço do que como meta).
- **SLA proposto:** repasse de lead quente atendido por humano em até 5–15 min no horário comercial. Repasse feito fora do horário: primeiro contato humano até 30–60 min após a abertura (por exemplo, 9h). Medir a % de violação do SLA por closer e por faixa horária.
- **Relatório de leads fora do horário:** % de leads que entram à noite ou no fim de semana, conversão desses leads em comparação com os do horário comercial, e tempo até o primeiro contato humano.
- Correlacionar FRT humano com win rate nos próprios dados (curva de conversão por faixa de 0–5 min, 5–30 min, 30 min–2 h, 2–24 h e mais de 24 h). Esse é o "estudo dos 5 minutos" interno, mais confiável que o de 2007.

### Gaps
- Não encontrei estudo brasileiro, nem específico de WhatsApp, que meça a conversão em função do tempo de resposta (só pesquisas de preferência). O PDF completo do CX Trends 2025 (Octadesk/Opinion Box) talvez traga o tempo de resposta esperado, mas a cobertura da imprensa não traz.
- Não encontrei benchmark público de FRT no WhatsApp para PMEs brasileiras.

## 3. Scorecard dos closers (vendedores)

### Takeaway
Não há benchmark público confiável de atividade por vendedor em WhatsApp. O mercado recomenda segmentar o win rate por vendedor e por tipo de negócio, e medir disciplina de follow-up com os dados do próprio CRM. Estatísticas populares sobre follow-up ("80% das vendas exigem 5 follow-ups", "44% desistem após 1") não têm fonte primária válida.

### Cited Findings
- A estatística "80% das vendas exigem 5 follow-ups" remonta a uma listicle sem estudo (Brevet Group). Outra versão atribui o número a uma pesquisa de 1942 de um capítulo local da NSEA com menos de 40 pessoas (informação de segunda mão). "44% dos vendedores desistem após 1 follow-up" também não tem origem primária — [Cirrus Insight](https://www.cirrusinsight.com/blog/sales-follow-up-statistics); [Instantly](https://instantly.ai/blog/how-many-times-should-you-really-follow-up-with-a-prospect/?lng=en); [usecarly](https://www.usecarly.com/blog/sales-follow-up-statistics/)
- Velocify (citado de forma secundária, ~3,5 mi de leads): 93% dos leads convertidos foram contatados até a 6ª ligação (dado antigo, contexto de telefone, não WhatsApp) — [Prospeo](https://prospeo.io/s/how-many-times-should-you-follow-up-with-a-prospect)
- Gong Labs analisou 304.174 e-mails de follow-up de prospecção (tamanho ideal e frases que ajudam ou atrapalham). CTAs de "interesse" (perguntar se o problema faz sentido) superam o pedido direto de reunião (Gong Labs, 2020, citado secundariamente) — [usecarly](https://www.usecarly.com/blog/sales-follow-up-statistics/); [Gong Labs](https://www.gong.io/gong-labs)
- Panorama RD Station 2025: "mais treinamento" (41%) e "rever a metodologia" (35%) são as maiores oportunidades citadas, e "ter um playbook" é a dor principal de 7% — [RD Station](https://www.rdstation.com/pesquisas/panoramas-rdstation-2025/vendas/cenario/)
- Recomendação de segmentar o win rate por nível de vendedor em vez de usar a taxa "misturada" — [Prospeo](https://prospeo.io/s/sales-velocity)

### Inferências
- **Scorecard semanal por closer** (definições propostas):
  - **Volume:** leads recebidos da IA, leads assumidos (com 1ª mensagem) e % assumidos.
  - **Velocidade:** FRT após o repasse (mediana e P90), % de violação do SLA e tempo médio de resposta durante a conversa.
  - **Atividade:** mensagens enviadas e follow-ups enviados (mensagem de saída após mais de 24 h sem resposta do cliente).
  - **Disciplina de follow-up:** % de negócios abertos com próximo passo/data marcado e % de leads "sumidos" com ao menos N follow-ups antes de serem marcados como perdidos.
  - **Resultado:** win rate (ganhos ÷ leads assumidos, separando B2C e B2B), ticket médio, receita por lead recebido (receita ÷ leads recebidos, a métrica que combina conversão e ticket) e ciclo médio.
  - **Qualidade:** % de perdas com motivo preenchido, distribuição dos motivos de perda comparada à média do time, recompra ou 2º pedido dos clientes do closer (importante no B2B de café, porque é recorrente).
  - **Coaching:** sentimento médio das conversas, objeções mal tratadas (extraídas pela IA) e conversas em que o cliente parou de responder logo após o envio do preço.
- **Justiça na distribuição de leads:** comparar por closer o número de leads e o "score médio" dos leads recebidos (distribuição de qualidade, não só de volume). Usar round-robin ponderado e checar se as diferenças de win rate não são só efeito do mix de leads.
- **Roteiro de 1:1 semanal (prática comum de gestão; sem fonte específica encontrada):**
  1. Números da semana em comparação à meta e à média do time.
  2. Revisão de 2–3 conversas reais (uma ganha, uma perdida).
  3. Pipeline parado: próximos passos negócio a negócio.
  4. Uma habilidade para treinar na semana.
  5. Compromissos.
- Com equipe pequena (2–4 closers), as amostras semanais são pequenas. Olhar o win rate em janela móvel de 4–8 semanas para não "punir" ruído.

### Gaps
- Não encontrei pesquisa com dados (2023–2026) sobre como gestores de PMEs brasileiras conduzem 1:1 com números, nem benchmark de mensagens ou follow-ups por vendedor em WhatsApp.
- Não encontrei o relatório original da HubSpot (State of Sales 2024) nos resultados. As estatísticas atribuídas a ele circulam só via blogs secundários.

## 4. Métricas de IA + repasse para humano (handoff)

### Takeaway
"Containment" (a IA resolve sem humano) é a métrica padrão de chatbot, mas no modelo da Canastra o objetivo da IA não é conter: é qualificar e repassar bem. As métricas certas são taxa de qualificação, taxa de repasse, conversão pós-repasse e precisão do score. Os benchmarks públicos são quase todos de fornecedores. O dado brasileiro mais útil (OmniChat 2025): conversas conduzidas por agentes de IA converteram 9%, igual ao atendimento só humano.

### Cited Findings
- **Fórmulas de fornecedor:**
  - Containment = conversas resolvidas pelo bot ÷ conversas totais do bot × 100.
  - Deflection = solicitações resolvidas pela IA ÷ total de solicitações recebidas × 100.
  - Faixas de containment (sem fontes citadas): iniciante 20–40%, intermediário 40–70%, avançado 70–90%; e-commerce 70–80% — [Alhena AI](https://alhena.ai/blog/what-is-ai-containment-vs-deflection-rate-2025-benchmarks/)
- Comm100 Live Chat Benchmark 2025 (dados de 2024): chatbots atenderam 73,8% dos chats (62,7% em 2023), e a resolução pelo chatbot foi de 45,8% (46,0% em 2023) — [Alhena AI, resumo](https://alhena.ai/blog/ai-chatbot-containment-vs-deflection-rate/); [eesel.ai](https://eesel.ai/blog/measuring-ai-containment-rate-and-escalation-quality)
- Containment não mede se o cliente conseguiu o que queria. A taxa de repasse não pode ser inferida a partir do containment (sessões não contidas incluem transferências, abandono etc.). A recomendação é acompanhar a qualidade do repasse (o humano recebe o contexto?) e o recontato em 7 dias — [eesel.ai](https://eesel.ai/blog/measuring-ai-containment-rate-and-escalation-quality)
- Compilação 2026 (fornecedor): containment de 28% a 68% conforme o setor, escalonamento de 32% a 45%, CSAT de interações contidas pelo bot ~10–14 pontos abaixo das resolvidas por humanos (metodologia não verificada) — [Stealth Agents](https://stealthagents.com/research/customer-support-chatbot-containment-statistics-2026)
- **Brasil, Chat Commerce Report 2026 (OmniChat, dados de 2025):**
  - Conversas conduzidas por agentes de IA autônomos tiveram 9% de conversão, equivalente à dos atendimentos só humanos.
  - 76% das conversas com IA estavam associadas a intenção de compra.
  - O relatório diz que a IA "pode reduzir em até 4x" o custo por conversa.
  - O artigo não define conversão nem metodologia — [ABC da Comunicação](https://www.abcdacomunicacao.com.br/sem-horario-comercial-vendas-migram-para-o-whatsapp-e-ia-impulsiona-resultados-aponta-chat-commerce-report-2026/)
- **Consumidor brasileiro e IA (Zendesk CX Trends 2025):**
  - 74% dizem que não importa se é IA ou humano, desde que o problema seja resolvido.
  - 81% dizem que simpatia é crucial para agentes de IA.
  - 78% aceitariam conversar com agentes de IA que melhorem a experiência — [Folha PE](https://www.folhape.com.br/economia/cx-trends-2025-america-latina/401720/)
- Na pesquisa da Opinion Box, 59% dos usuários dizem não gostar de respostas automáticas. É um alerta contra respostas engessadas — [Mundo do Marketing](https://mundodomarketing.com.br/whatsapp-e-o-canal-mais-usado-pelos-brasileiros-em-contatos-pos-compra)
- **Custo do WhatsApp (Meta), relevante para custo por conversa:**
  - Desde 01/07/2025 a cobrança é por mensagem-template entregue, não mais por conversa de 24 h.
  - Mensagens de serviço (resposta livre dentro da janela de 24 h aberta pelo cliente) são gratuitas. Templates de utilidade dentro da janela também são gratuitos; marketing e autenticação são sempre cobrados.
  - Leads vindos de anúncio Click-to-WhatsApp abrem janela gratuita de 72 h para qualquer mensagem, se a empresa responder dentro das 24 h.
  - Utilidade tem desconto por volume de 5–20%.
  - No Brasil a tarifa de utilidade caiu 15% e a de autenticação 78%. O valor em USD por mensagem de marketing no Brasil precisa ser conferido na tabela oficial da Meta — [YCloud](https://www.ycloud.com/pt/blog/whatsapp-api-pricing-update); [SleekFlow](https://help.sleekflow.io/pt_BR/whatsapp/pricing)

### Inferências
- **Métricas propostas para IA → closer:**
  - **Taxa de resposta da IA** = conversas com ao menos 1 resposta da IA ÷ conversas iniciadas.
  - **Taxa de qualificação** = leads marcados como qualificados ÷ leads que interagiram.
  - **Taxa de repasse** = leads repassados ao humano ÷ leads que interagiram. Separar repasse por qualificação de repasse por "IA não soube responder" ou "cliente pediu humano".
  - **Resolução pela IA sem humano:** dúvidas simples, B2C com link de compra direto. É o "containment" adaptado.
  - **Abandono na IA** = conversas em que o cliente parou de responder antes da qualificação ÷ conversas iniciadas, com a etapa do roteiro em que parou.
  - **Qualidade do repasse:**
    - % de repasses com resumo completo (nome, tipo B2C/B2B, volume, cidade, interesse).
    - % em que o closer precisou repetir perguntas que a IA já fez.
    - % de repasses que o closer "devolveu" como não qualificado.
  - **Precisão do score:** win rate por faixa de score (o score alto precisa converter mais que o baixo). Na prática, AUC simples ou uma tabela de calibração mensal.
  - **Custo por conversa da IA** = (tokens de entrada × preço + tokens de saída × preço) ÷ conversas, somado ao custo de templates Meta. Medir também o custo por lead qualificado e o custo por venda.
- Comparar a conversão de leads atendidos pela IA e repassados com a de leads atendidos direto por humano (se houver grupo de controle) é o equivalente interno do dado OmniChat de 9% contra 9%.

### Gaps
- Não encontrei benchmark público de "taxa de qualificação por IA" nem de "precisão de lead scoring" para PMEs. Os números de containment não se aplicam diretamente a um fluxo de qualificação de vendas.
- Não confirmei a tarifa oficial em USD da mensagem de marketing no Brasil em 2025/2026.

## 5. Analytics de conversa: sentimento, perguntas e objeções, motivos de perda, abandono, campanhas/templates, opt-out

### Takeaway
A Meta não publica uma meta numérica de taxa de leitura. O benchmark oficial é o percentil 75 da taxa de leitura entre empresas parecidas (mesmo país, setor e categoria de template), visível no WhatsApp Manager. A taxa de leitura e os bloqueios/denúncias afetam a qualidade do template e podem levar à suspensão. Para resposta a campanhas, não há benchmark confiável; o dado brasileiro OmniChat indica que 1 em cada 3 respostas a campanhas virou venda.

### Cited Findings
- **Benchmark oficial da Meta:**
  - É o percentil 75 da taxa de leitura (lidas ÷ entregues) de empresas similares por país/região, setor e categoria de template, nos últimos 30 dias, com até 2 dias de atraso.
  - Aparece em WhatsApp Manager > Gerenciar templates (Marketing Messages API).
  - Usuários com confirmação de leitura desligada não entram na conta — [Meta for Developers](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/view-metrics/); [Wazzup](https://wazzup24.com/help/how-to-use-en/what-is-read-rate-in-waba-and-how-to-maintain-a-high-score/)
- Desde 01/04/2024, a nota de qualidade dos templates de marketing considera a taxa de leitura além de bloqueios e denúncias. Template com leitura baixa ou denunciado como spam pode ser suspenso — [Wazzup](https://wazzup24.com/help/how-to-use-en/what-is-read-rate-in-waba-and-how-to-maintain-a-high-score/); [Clickatell](https://clickatell.com/help-center/whatsapp/message-templates/how-do-i-improve-my-whatsapp-template-s-read-rates)
- **Faixas de terceiros (não oficiais):**
  - Taxa de leitura de 65–80% em templates de marketing é "satisfatória" (Clickatell) — [Clickatell](https://clickatell.com/help-center/whatsapp/message-templates/how-do-i-improve-my-whatsapp-template-s-read-rates)
  - Entrega acima de 95%, leitura acima de 85%, CTR de 15–25% e resposta de 5–10% (blog de fornecedor, aspiracional) — [Message Central](https://www.messagecentral.com/blog/whatsapp-marketing-business-2026)
- **Brasil, OmniChat 2025:**
  - 1 em cada 3 respostas a campanhas via WhatsApp resultou em venda.
  - Recuperação de carrinho abandonado com ticket médio de R$619 e "ROI de 176x".
  - Números de fornecedor, sem metodologia detalhada — [ABC da Comunicação](https://www.abcdacomunicacao.com.br/sem-horario-comercial-vendas-migram-para-o-whatsapp-e-ia-impulsiona-resultados-aponta-chat-commerce-report-2026/); [Diário do Comércio](https://diariodocomercio.com.br/?p=579748)
- **Brasil, preferência pelo canal:**
  - 65% das empresas dizem que o WhatsApp é o canal que mais gera conversões em vendas, e 88% o usam na estratégia comercial (Panorama Zenvia com Opinion Box).
  - Principais obstáculos: dificuldade de localizar dados (27%) e falta de integração entre ferramentas (26%) — [Central do Varejo](https://centraldovarejo.com.br/whatsapp-lidera-conversoes-no-brasil-mas-falta-de-integracao-de-dados-limita-avanco-das-vendas/)
  - 30% dos consumidores já compram pelo WhatsApp, 33% preferem o app no pós-venda e 51% preferem receber atualizações de pedido por ele (CX Trends 2025 Octadesk/Opinion Box) — [Propmark](https://propmark.com.br/?p=124860)
  - O WhatsApp foi o canal mais usado no pós-compra por 54% (CX Trends 2024) — [Mundo do Marketing](https://mundodomarketing.com.br/whatsapp-e-o-canal-mais-usado-pelos-brasileiros-em-contatos-pos-compra)

### Inferências
- **Analytics de conversa propostos (extraídos por LLM do histórico):**
  - **Sentimento** por conversa (positivo/neutro/negativo) e por closer, com variação ao longo da conversa (piorou depois do preço?).
  - **Top perguntas:** frete, prazo, pedido mínimo, moagem, preço de atacado, private label (MOQ, rótulo, prazo).
  - **Top objeções:** preço, frete, prazo, quantidade mínima, "vou pensar".
  - **Motivo de perda inferido do chat**, comparado ao motivo marcado pelo closer. A divergência é um sinal de coaching e de qualidade do dado.
  - **Abandono:** conversa sem resposta do cliente por mais de 48–72 h, com a última etapa e a última mensagem da empresa (preço? link? pergunta?).
  - **Conversas "fantasmas" do lado da empresa:** cliente perguntou e ninguém respondeu.
- **Painel de campanhas/templates:** por template, mostrar
  - enviadas → entregues → lidas → respondidas → convertidas (venda em até 7 dias);
  - opt-outs (pedido de "parar" ou "sair") e bloqueios/denúncias;
  - custo do template e receita atribuída.
  O alvo de leitura é o percentil 75 que a Meta mostra no WhatsApp Manager. Opt-out/bloqueio alto deve pausar o template.
- **Recompra B2B:** campanhas de lembrete de reposição para clientes de atacado (ciclo de consumo de café) costumam ser o template de maior retorno. Medir a taxa de recompra em 30/60/90 dias (hipótese a validar nos dados próprios).

### Gaps
- Não encontrei benchmark público confiável de taxa de resposta a templates, nem de taxa de opt-out no WhatsApp, por setor no Brasil.
- Não encontrei estudo público sobre a distribuição típica de motivos de perda em vendas por WhatsApp de alimentos/bebidas.
