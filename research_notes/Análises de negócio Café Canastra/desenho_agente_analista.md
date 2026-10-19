# Desenho de um agente "analista de negócios" (text-to-SQL sobre Postgres, via Discord, com Claude)

## Semantic layer / catálogo de métricas: como os produtos definem métricas, dimensões, joins, sinônimos e verified queries, e quanto isso melhora a acurácia

### Takeaway
Todos os produtos líderes (Snowflake Cortex Analyst, Databricks Genie, Looker, Power BI Copilot, dbt/MetricFlow, Cube) convergem no mesmo pacote: entidades lógicas com descrições, métricas definidas uma única vez, joins/chaves explícitos, sinônimos e valores de exemplo, instruções de domínio em texto e um repositório de perguntas com SQL verificado. Os números publicados mostram ganhos de +17 a +23 p.p. (paper independente de 2026), de 64,5% para 72,7–100% (dbt 2026) e de 0% para 100% em um caso guiado da Databricks. Em todos os casos, a qualidade da modelagem pesa mais do que a escolha do modelo.

### Cited Findings
**Estrutura do semantic model (Snowflake Cortex Analyst / semantic views)**
- O YAML tem `tables` (entidades lógicas com `description`, `synonyms` e `base_table`, que pode ser uma tabela ou uma `definition` SQL), `primary_key`/`unique_keys`, `dimensions`, `time_dimensions`, `facts`, `metrics`, `filters`, `relationships`, `verified_queries`, `module_custom_instructions` (`sql_generation`, `question_categorization`) e `variables` — [Snowflake semantic view YAML spec](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec)
- Cada dimensão aceita `synonyms`, `sample_values`, `is_enum` (se for `true`, os sample values passam a ser a lista completa e o modelo só filtra por eles) e `cortex_search_service`, um índice de busca para colunas com valores de alta cardinalidade — [Snowflake YAML spec](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec)
- Os sinônimos devem ser únicos no modelo inteiro. As descrições devem ser curtas e úteis, e a doc pede explicitamente que a descrição de cada time dimension diga o fuso horário de referência — [Snowflake YAML spec](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec)
- `facts` são atributos numéricos por linha; `metrics` são agregações de KPI; `dimensions` servem para agrupar e filtrar. A recomendação é começar por um star schema simples — [Snowflake semantic views overview](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst/semantic-model-spec)
- Cada entrada de verified query tem `name`, `question`, `sql`, `verified_by`, `verified_at` e `use_as_onboarding_question` (a pergunta aparece como sugestão para novos usuários). O SQL usa os nomes lógicos do modelo. Quando a pergunta do usuário é parecida com uma verificada, o Analyst reaproveita aquele SQL, e o Snowsight sugere novas verified queries a partir do uso real — [Snowflake VQR](https://docs.snowflake.com/user-guide/snowflake-cortex/cortex-analyst/verified-query-repository)

**Databricks Genie**
- Recomendações: nomes de tabela e coluna com sentido de negócio (nada de `cmp` ou `uid_seq`); descrições que avisem quando uma coluna parece chave de join mas não é; PK/FK declaradas; joins complexos registrados no knowledge store; example values e value dictionaries para mapear o termo do usuário ao valor gravado; example SQL comentado para métricas customizadas; instruções em texto para regras de domínio (limiares de rótulos, filtros globais como "excluir campanhas de teste", calendário fiscal); views ou metric views como fonte única de métricas — [Databricks blog: production-ready Genie spaces](https://www.databricks.com/blog/how-build-production-ready-genie-spaces-and-build-trust-along-way)
- Progressão de acurácia no benchmark do blog: baseline com nomes crípticos, 0%; com nomes, descrições, joins e valores, 54%; com example SQL para métricas customizadas, 77% ("o maior ganho isolado"); com instruções de domínio, 100%; com views ou metric views, também 100% — [Databricks blog](https://www.databricks.com/blog/how-build-production-ready-genie-spaces-and-build-trust-along-way)
- Não pré-computar agregados ou segmentos em tabelas: calculá-los on the fly preserva os filtros de período e de segmento — [Databricks blog](https://www.databricks.com/blog/how-build-production-ready-genie-spaces-and-build-trust-along-way)
- Uma resposta recebe o selo "Trusted" quando usa exatamente uma example query parametrizada ou uma SQL function — [Databricks Genie docs](https://docs.databricks.com/gcp/genie)

**Looker (LookML + Gemini Conversational Analytics)**
- Usar sinônimos e descrições; definir os cálculos frequentes como dimensions/measures em LookML (fonte única e menor latência); esconder do agente as colunas técnicas (FKs, IDs crus), porque menos ruído melhora a escolha de campos; usar o parâmetro `suggestions` com valores fixos; começar com 1–2 Explores curados e um grupo pequeno de usuários que conhecem os dados — [Google Looker best practices](https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-best-practices)

**Power BI Copilot ("Prep data for AI")**
- Três ferramentas: AI data schema (subconjunto do modelo que o Copilot enxerga), Verified answers (respostas e visuais aprovados pelo autor, disparados por trigger phrases) e AI instructions (por exemplo, definir o que é "busy season"). Também há descrições de tabela e coluna. Tudo isso vive no semantic model, não no relatório. A Microsoft avisa que as saídas são não determinísticas — [Microsoft Learn: Prepare data for AI](https://learn.microsoft.com/en-gb/power-BI/create-reports/copilot-prepare-data-ai-faq)

**Cube**
- Os agentes consultam métricas certificadas por interfaces governadas (REST, GraphQL, SQL e um MCP server), com as regras de acesso aplicadas no compilador antes da execução. O modelo semântico é tratado como código (Git, PR, CI/CD, ambientes) — [Cube: semantic layer architecture](https://cube.dev/articles/semantic-layer-architecture); [Cube blog GigaOm](https://cube.dev/blog/cube-cloud-named-leader-and-outperformer-in-2025-gigaom-radar-for-semantic)

**Números publicados: semantic layer vs. schema cru**
- dbt Labs, benchmark de abril de 2026 (ACME Insurance, 3NF, 11 perguntas × 20 execuções): text-to-SQL no schema cru foi de 32,7% (GPT-4, 2023) para 64,5% (Sonnet 4.6 / GPT-5.3 Codex); o Semantic Layer foi de 60,5% para 72,7%. Dentro do escopo do Semantic Layer a acurácia foi de 100%; perguntas com muitos saltos entre entidades tiveram 0% até receberem mais modelagem. Depois de 3 modelos dbt novos (gerados por LLM), os resultados foram: Sonnet 4.6 com 90,0% em text-to-SQL e 98,2% com Semantic Layer; GPT-5.3 Codex com 84,1% e 100% — [dbt: Semantic Layer vs Text-to-SQL 2026](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)
- No mesmo estudo do dbt, o nível de reasoning effort quase não mudou a acurácia do Semantic Layer, e o Sonnet 4.6 superou o Opus 4.6 nesse caso de uso. Falhas típicas do text-to-SQL: join errado, coluna mal interpretada, query que roda mas devolve resultado errado e números inconsistentes entre execuções. O MetricFlow, por outro lado, devolve erro em vez de dado inválido quando a pergunta está fora do escopo — [dbt 2026](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)
- A recomendação do dbt é usar o Semantic Layer para KPIs recorrentes e de alto risco (board, OKRs, relatórios semanais) e text-to-SQL para exploração ad hoc, nesta ordem: tentar o SL, depois uma pequena mudança de modelagem, e só então text-to-SQL — [dbt 2026](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)
- Paper independente (Rumiantsau & Fokeev, arXiv, abril de 2026): 100 perguntas sobre o Contoso Retail em ClickHouse, com Claude Opus 4.7, Claude Sonnet 4.6 e GPT-5.4. Sem semantic layer a acurácia ficou entre 45,5% e 50,5%; com um documento markdown de cerca de 4 KB (medidas, convenções e regras de desambiguação), entre 67,7% e 68,7%. O ganho foi de +17 a +23 p.p., com p < 0,01, e a escolha do modelo dentro do mesmo tier não fez diferença significativa — [arXiv 2604.25149](https://arxiv.org/abs/2604.25149)
- BIRD: a "evidence" (conhecimento externo de domínio, escrito por pergunta) levou o GPT-4 de 34,88% para 54,89% de execution accuracy e melhorou todos os modelos testados (fonte secundária) — [beancount.io sobre BIRD](https://beancount.io/bean-labs/research-logs/2026/06/06/bird-benchmark-text-to-sql-real-database-gap)

### Inferences
- Para uma pequena empresa em Postgres, não é preciso adotar dbt/Cube: o paper de 2026 mostra que um documento markdown de cerca de 4 KB com medidas, convenções e regras de desambiguação já rende +17–23 p.p. O formato mais barato é um "catálogo" em YAML ou markdown no repositório, inspirado no spec da Snowflake (tabelas lógicas, métricas com SQL canônico, sinônimos, sample values ou enums, fuso horário, verified queries), somado a views SQL curadas (`vw_vendas_diarias`, `vw_leads`) que fazem o papel de metric views.
- Como métricas recorrentes (faturamento, ticket médio, conversão) precisam ser determinísticas, convém expô-las como SQL parametrizado ou view, com um selo de "resposta verificada" no estilo do Genie, e deixar o SQL livre só para perguntas exploratórias. A resposta deve sinalizar qual dos dois caminhos foi usado.
- O Sonnet tende a ser suficiente: o dbt viu Sonnet 4.6 ≥ Opus 4.6, e o paper viu os modelos empatados. O esforço deve ir para o contexto.

### Gaps
- Não encontrei números publicados de acurácia para ThoughtSpot, Hex Magic, Looker + Gemini, nem dados independentes sobre Cube (os 100% citados pela Cube vêm do parceiro Delphi, sobre um subconjunto, ou seja, são marketing).
- Não consegui ler a doc oficial de Cube views/AI API nem a de Hex Magic. O post original da OpenAI deu 403 e foi usado via resumo secundário (ByteByteGo).
- Não encontrei taxas de alucinação por modelo no paper arXiv 2604.25149; apenas o abstract foi lido.

## Práticas que aumentam a correção: views curadas, golden queries, glossário, few-shot, descrições, perguntas de esclarecimento, explicitar premissas, sanity checks, fuso horário, termos ambíguos

### Takeaway
A ordem de impacto relatada é: dados e nomes limpos, depois descrições, joins e valores, depois exemplos SQL verificados para métricas customizadas, depois instruções de domínio em texto (glossário). Em execução, o agente deve iterar (rodar, inspecionar, corrigir), mostrar o SQL e as tabelas usadas e guardar em memória as correções do usuário. A ambiguidade continua sendo um ponto fraco dos LLMs, então termos como "lead qualificado" precisam de definição explícita no glossário ou de uma pergunta de esclarecimento.

### Cited Findings
- Example SQL para métricas customizadas, com comentários, foi o maior ganho isolado no Genie: um único exemplo bem escrito corrige uma categoria inteira de perguntas, e o Genie generaliza para variações. As instruções em texto devem cobrir o que sobrar, sem ser a única alavanca — [Databricks blog](https://www.databricks.com/blog/how-build-production-ready-genie-spaces-and-build-trust-along-way)
- O cookbook da Anthropic (setembro de 2024) recomenda: schema em tags `<schema>`; few-shot com padrões de join e agregação; raciocínio em `<thought_process>` antes de `<sql>`; RAG sobre descrições de colunas quando o schema é grande; loop de autocorreção em que o erro de execução volta para o Claude, com no máximo 3 tentativas; `temperature=0`; algumas linhas de exemplo por tabela; estatísticas de coluna (% de nulos, min/max, valores comuns); documentar problemas de qualidade, definições de negócio (ex.: "funcionário ativo"), relações e frequência de atualização. O próprio guia avisa que o loop de erro só garante que a query roda, não que ela está certa — [Claude Cookbook: Text-to-SQL](https://platform.claude.com/cookbook/capabilities-text-to-sql-guide)
- O agente de dados interno da OpenAI (janeiro de 2026) usa seis camadas de contexto: uso das tabelas (queries de dashboards populares pesam mais que queries ad hoc), anotações humanas, enriquecimento feito pelo Codex a partir do código do pipeline (conteúdo, derivação, freshness, quando preferir uma tabela similar), conhecimento institucional (Slack, Docs, Notion, com controle de acesso), memória de correções (escopo global ou pessoal) e contexto em runtime (consulta o warehouse quando os metadados estão velhos) — [ByteByteGo sobre o agente da OpenAI](https://blog.bytebytego.com/p/how-openai-built-its-data-agent); [OpenAI](https://openai.com/index/inside-our-in-house-data-agent/)
- Outras lições do agente da OpenAI: ele roda em loop (escreve SQL, inspeciona o resultado, revisa); as respostas trazem o SQL executado e as tabelas usadas; cerca de 40 ferramentas geravam respostas conflitantes, e cortar para cerca de 13 sem sobreposição resolveu; descrever o objetivo e dar bom contexto funcionou melhor do que prompts passo a passo; usar todas as queries históricas como contexto funcionou mal, então é preciso ranquear por confiabilidade. A memória sozinha reduziu um caminho de pergunta de 22 minutos para 1 — [ByteByteGo](https://blog.bytebytego.com/p/how-openai-built-its-data-agent); [OpenAI via busca](https://openai.com/index/inside-our-in-house-data-agent/)
- Ambiguidade: o AMBROSIA (NeurIPS 2024) mostra que mesmo os modelos mais avançados têm dificuldade em identificar e interpretar ambiguidade de escopo, de attachment e vagueza. O PRACTIQ (NAACL 2025) define 4 categorias de perguntas ambíguas e 4 de não respondíveis e mostra que os sistemas state-of-the-art lidam mal com elas. O AmbiSQL (2025) dá o exemplo "Fresno", que pode ser cidade ou condado, e propõe detecção e resolução interativa — [AMBROSIA](https://papers.neurips.cc/paper_files/paper/2024/hash/a4c942a8405cc910f0a833d28d2573cc-Abstract-Datasets_and_Benchmarks_Track.html); [PRACTIQ](https://aclanthology.org/2025.naacl-long.13); [AmbiSQL](https://arxiv.org/html/2508.15276v1)
- Regras de domínio, como o limiar que define um rótulo ("high-engagement"), filtros globais (excluir testes) e calendário fiscal, devem ficar em instruções explícitas — [Databricks blog](https://www.databricks.com/blog/how-build-production-ready-genie-spaces-and-build-trust-along-way). No Power BI, o exemplo canônico é definir "busy season" nas AI instructions — [Microsoft Learn](https://learn.microsoft.com/en-gb/power-BI/create-reports/copilot-prepare-data-ai-faq)
- Fuso horário: a spec da Snowflake pede que a descrição de cada time dimension diga o fuso de referência — [Snowflake YAML spec](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec)
- Valores "sujos" e mapeamento de valores: o BIRD mostra falhas (dirty values, conhecimento externo) que benchmarks limpos não revelam. Na prática, isso se resolve com sample values, value dictionaries e enums — [beancount.io sobre BIRD](https://beancount.io/bean-labs/research-logs/2026/06/06/bird-benchmark-text-to-sql-real-database-gap); [Databricks blog](https://www.databricks.com/blog/how-build-production-ready-genie-spaces-and-build-trust-along-way)

### Inferences
- Implementação sugerida para Claude e Postgres:
  1. Um glossário com as definições canônicas da empresa, por exemplo "lead qualificado = …", "closer = vendedor que fecha a venda (coluna X)" e "faturamento = soma de pedidos pagos, excluindo cancelados/teste, em America/Sao_Paulo". Cada termo deve trazer o SQL canônico.
  2. Views `analytics.*` com nomes em português de negócio, comentadas via `COMMENT ON` para que o agente leia as descrições do próprio catálogo.
  3. De 20 a 50 golden queries (pergunta e SQL) usadas como few-shot e recuperadas por similaridade.
  4. Ferramentas poucas e sem sobreposição (ex.: `listar_catalogo`, `rodar_sql_readonly`, `metricas_verificadas(nome, periodo)`).
  5. Memória de correções: quando o dono corrigir uma definição, ela é gravada no glossário, com revisão humana.
- Política de ambiguidade: se o termo está no glossário, aplicar a definição e explicitá-la na resposta ("considerei lead qualificado = …"). Se não está e há mais de uma interpretação plausível com resultados materialmente diferentes, fazer uma única pergunta curta com opções. Nos demais casos, responder com a premissa declarada e oferecer a alternativa. Isso reduz o atrito no Discord.
- Sanity checks baratos antes de responder: contagem de linhas (zero ou uma explosão de linhas indica join errado); total da quebra por dimensão igual ao total geral; período efetivamente coberto pelos dados (min/max de data); comparação com a métrica verificada quando ela existir; checagem de NULLs nas colunas de filtro. Toda conversão de timestamps deve usar `AT TIME ZONE 'America/Sao_Paulo'` antes de `date_trunc`, e "hoje", "ontem" e "semana passada" devem ser resolvidos explicitamente nesse fuso.

### Gaps
- Não achei estudos quantificando o ganho específico de sanity checks (row counts, cross-check de totais) nem de "mostrar premissas" na confiança e na acurácia; essas recomendações são práticas inferidas.
- Não li os métodos completos do AmbiSQL e do PRACTIQ (taxas de acerto com e sem clarificação).

## Como bons assistentes de análise respondem: resposta primeiro, comparação com o período anterior, drivers/decomposição, anomalias, próximas perguntas; digests executivos e alertas proativos

### Takeaway
Os produtos comerciais implementam o "por quê?" como change analysis: pegam uma métrica, comparam dois pontos no tempo (ou dois segmentos) e ranqueiam as dimensões que mais explicam a variação, com resumo em linguagem natural. Para alertas proativos, a lição principal é comparar com uma baseline sazonal (mesmo dia da semana) e filtrar por materialidade, para não gerar fadiga. Há pouca literatura formal sobre o formato da resposta executiva; o formato abaixo é inferência a partir dos produtos.

### Cited Findings
- No ThoughtSpot Spotter, uma pergunta como "Why did sales drop in Q2?" faz o sistema identificar os atributos relevantes, rodar o change analysis engine e devolver um resumo em linguagem natural dos principais drivers, com visualizações. Para "por que a receita caiu?", ele compara os dois últimos pontos de data. A limitação é trabalhar com uma métrica por vez em gráficos simples, sem slicing, mas comparações entre categorias (ex.: churn East vs. West) também são suportadas — [ThoughtSpot docs: Why questions in Spotter](https://docs.thoughtspot.com/cloud/latest/spotter-why)
- O antecessor, SpotIQ change analysis, compara quaisquer dois pontos de uma visualização, identifica os drivers entre as colunas de atributo e permite drill numa categoria e recalcular — [ThoughtSpot change analysis](https://docs.thoughtspot.com/software/9.8.0.sw/spotiq-change)
- O roadmap de fevereiro de 2026 do ThoughtSpot lista "Why Questions", AI summaries, deep research e análise avançada via código como elementos do Spotter 3 — [ThoughtSpot SpotMap Feb 2026](https://media.thoughtspot.com/pdf/ThoughtSpot-SpotMap-Slides-February-2026.pdf)
- No Snowflake VQR, `use_as_onboarding_question` faz perguntas verificadas aparecerem como sugestões ao usuário, um padrão de "próximas perguntas" ancorado em queries confiáveis — [Snowflake YAML spec](https://docs.snowflake.com/en/user-guide/views-semantic/semantic-view-yaml-spec)
- Alertas: a sazonalidade semanal é a maior fonte de falsos positivos, e a correção é um z-score por dia da semana (sábado comparado com sábados), com fallback para a janela inteira quando há poucas amostras — [Tracely: Detecting anomalies without crying wolf](https://tracely.cloud/blog/anomaly-detection-and-alerts). Limiares fixos funcionam mal para KPIs sazonais, mas servem para limites "físicos" — [New Relic anomaly detection](https://docs.newrelic.com/docs/alerts/create-alert/set-thresholds/anomaly-detection.md). A detecção precisa de 1–4 semanas de histórico para estabilizar a baseline — [OpenObserve](https://openobserve.ai/blog/ai-anomaly-detection-guide.md)
- Para reduzir a fadiga de alertas, o score de anomalia deve ser lido junto com a materialidade de negócio, e mudanças legítimas esperadas devem ser documentadas: campanhas, feriados, ciclos de cobrança, lançamentos, efeitos de fuso — [geosurge corpus, fonte de qualidade incerta](https://thisisatest.geosurge.ai/corpus/gen-3029/real-time-business-intelligence/real-time-kpi-alerting-and-anomaly-detection-for-executive-decision-making.html)

### Inferences
- Formato de resposta no Discord, para caber em uma mensagem:
  1. Resposta direta em 1 linha com o número e a unidade, ex.: "Faturamento em setembro: R$ 182,4 mil".
  2. Comparação com o período anterior e com o mesmo período do ano anterior, em % e em valor absoluto.
  3. Até 3 drivers da variação, decompostos por dimensão (produto, canal, vendedor) ou por fórmula (receita = pedidos × ticket médio), ranqueados por contribuição absoluta.
  4. Anomalia ou alerta, se houver.
  5. Premissas e definição usadas, em uma linha.
  6. 2–3 próximas perguntas sugeridas.
  7. O SQL e a "fonte" ficam disponíveis sob demanda, em bloco de código ou anexo, como faz a OpenAI.
- Para o "por quê", implementar uma decomposição simples em SQL: para cada dimensão candidata, Δ por categoria e participação no Δ total, mostrando o top-N. Isso replica a ideia do change analysis sem infraestrutura.
- Digest diário ou semanal: KPIs fixos (vendas, ticket, novos leads, conversão, top produtos) com variação contra a mesma janela da semana anterior. Só disparar alerta fora do digest quando houver |z| alto contra uma baseline do mesmo dia da semana E uma variação absoluta mínima (materialidade) E persistência em mais de um período. Os valores iniciais citados na busca (|z| ≥ 3) são sugestão, não achado, e devem ser calibrados reexecutando o histórico. Feriados e campanhas devem ser anotados num calendário consultado pelo agente.

### Gaps
- Não encontrei guidelines publicadas (Microsoft, Google, Databricks) sobre o formato textual ideal de uma resposta executiva nem sobre cadência e formato de digests; o formato acima é inferência.
- Não encontrei limiares de anomalia validados por fontes primárias, nem dados medidos de redução de fadiga de alertas.
- Não pesquisei Hex Magic nem os recursos de "Deep Research" do Genie e do Spotter em detalhe.

## Avaliação: como montar um conjunto de testes de perguntas de negócio, medir acurácia e manter o catálogo atualizado

### Takeaway
O consenso dos fornecedores é ter de 10 a 20 perguntas reais (escritas pelo usuário final) com SQL esperado, medir uma baseline, mudar uma coisa por vez, rodar a suíte inteira de novo e acompanhar regressões, comparando resultados de execução em vez do texto do SQL. Os benchmarks acadêmicos (BIRD, Spider 2.0) mostram que dados reais, valores sujos e conhecimento de domínio derrubam muito a acurácia, de modo que os números de benchmarks limpos não se transferem para a sua base.

### Cited Findings
- Genie: suíte de 10–20 perguntas com SQL validado, escritas por SMEs e usuários finais, de preferência antes do desenvolvimento. Medir a baseline, mudar uma coisa por vez e rodar a suíte inteira de novo. O SQL do benchmark não entra no contexto, ficando como teste independente. Cerca de 80% de acurácia é o limiar antes do UAT, com as lacunas restantes documentadas — [Databricks blog](https://www.databricks.com/blog/how-build-production-ready-genie-spaces-and-build-trust-along-way). Perguntas sem SQL esperado ficam marcadas para revisão manual — [Databricks Genie docs](https://docs.databricks.com/gcp/genie)
- Cortex Analyst evaluations: executam o SQL gerado e comparam o resultado com o das verified queries, reportando accuracy, regressões (o que passava e agora falha) e latência, por pergunta — [Snowflake Cortex Analyst evaluations](https://docs.snowflake.com/de/user-guide/snowflake-cortex/cortex-analyst-evaluations)
- O cookbook da Anthropic usa Promptfoo com testes de sintaxe (executa), semântica (tabelas, joins, agregações), correção do resultado (linhas esperadas num banco de teste) e complexidade — [Claude Cookbook](https://platform.claude.com/cookbook/capabilities-text-to-sql-guide)
- O dbt rodou cada uma das 11 perguntas 20 vezes para medir a consistência entre execuções; a inconsistência é um modo de falha do text-to-SQL — [dbt 2026](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)
- O BIRD tem 12.751 pares em 95 bancos (33,4 GB) de 37 domínios e enfatiza dirty values, conhecimento externo e eficiência (Valid Efficiency Score). O Spider 2.0 tem 632 problemas de workflow enterprise com mais de 1.000 colunas; um agente com o1-preview fez 21,3% contra 73,0% no BIRD e 91,2% no Spider 1.0 (números via fonte secundária) — [beancount.io](https://beancount.io/bean-labs/research-logs/2026/06/06/bird-benchmark-text-to-sql-real-database-gap); [arXiv survey 2412.05208](https://arxiv.org/pdf/2412.05208)
- Manutenção: o agente da OpenAI regera as descrições das tabelas todo dia, com o Codex lendo o código dos pipelines, e cai para consulta em runtime quando os metadados estão velhos — [ByteByteGo](https://blog.bytebytego.com/p/how-openai-built-its-data-agent). O Snowsight sugere novas verified queries a partir do uso — [Snowflake VQR](https://docs.snowflake.com/user-guide/snowflake-cortex/cortex-analyst/verified-query-repository). A Cube recomenda tratar o modelo semântico como código (Git, PR, CI/CD) — [Cube blog](https://cube.dev/blog/cube-cloud-named-leader-and-outperformer-in-2025-gigaom-radar-for-semantic). A rollout do Looker sugere atribuir um dono e um ciclo de revisão começando com usuários que conhecem os dados — [Google Looker best practices](https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-best-practices)

### Inferences
- Plano prático:
  1. Coletar 20–40 perguntas reais do dono (as que ele de fato faz), incluindo ambíguas ("quantos leads qualificados?") e não respondíveis (dados que não existem), cujo comportamento esperado é perguntar ou recusar.
  2. Escrever o SQL de referência e salvar o resultado esperado.
  3. Um script que roda o agente N vezes por pergunta e compara o resultado (conjunto de linhas, com tolerância numérica), não o texto do SQL.
  4. Rodar em CI a cada mudança no catálogo, no prompt ou no modelo, e após migrações de schema.
  5. Cada correção do dono vira um caso novo da suíte.
- Para perguntas relativas ("semana passada"), congelar a data de referência ou usar um snapshot, para o gabarito não envelhecer.
- Detectar drift de schema: um job compara `information_schema` ou `pg_catalog` com o catálogo e alerta sobre colunas ou tabelas novas e removidas sem descrição. Vale também falhar o CI se uma view curada quebrar.

### Gaps
- Não encontrei um estudo que quantifique o tamanho ideal da suíte de avaliação para pequenas empresas. Os 10–20 itens do Genie são recomendação de fornecedor.
- O detalhamento das evals do agente da OpenAI (Evals API com respostas verificadas) só aparece em fonte secundária, sem confirmação no post original.

## Segurança: roles read-only, PII, limites de linhas, custo e timeouts

### Takeaway
A fronteira real é o próprio banco: um role dedicado só com SELECT nas views curadas, `default_transaction_read_only`, `statement_timeout` curto e REVOKE explícito em tabelas sensíveis. Filtros de texto no SQL ("bloquear DELETE") e limites de linhas na aplicação são defesa adicional. Também é preciso considerar que os dados enviados ao LLM saem do banco.

### Cited Findings
- Usar um role dedicado com CONNECT, apenas os SELECTs escolhidos e timeout curto, nunca o superuser nem o role da aplicação. O read-only deve ser imposto pelo banco (`default_transaction_read_only = on` no role), porque filtros por palavra-chave no texto do SQL podem ser contornados. Configurar `ALTER ROLE agent_reader SET statement_timeout = '30s'`. Grants em tabelas existentes não cobrem tabelas futuras (usar `ALTER DEFAULT PRIVILEGES`). Fazer REVOKE em tabelas sensíveis com PII ou segredos. Limitar o número de linhas devolvidas e sanitizar as mensagens de erro, que podem servir de oráculo de enumeração do schema. Não usar `BYPASSRLS` — [C# Corner: read-only PostgreSQL access for AI agents](https://www.c-sharpcorner.com/article/giving-ai-agents-read-only-postgresql-access-without-touching-production); [Tessl: create readonly db role](https://tessl.io/registry/skills/github/mishatojk/davidskills/create-readonly-db-role); [postgres-mcp guide](https://agents.aguidetocloud.com/mcp/postgres-mcp/)
- O Genie recomenda conceder SELECT apenas nos schemas e tabelas necessários — [querio.ai, terceiro](https://querio.ai/articles/setup-databricks-genie-ai-bi-step-by-step-guide). O Looker recomenda esconder do agente as colunas técnicas e internas — [Google Looker](https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-best-practices). Na Cube, as regras de acesso são aplicadas no compilador antes de a query rodar — [Cube](https://cube.dev/articles/semantic-layer-architecture)
- Dados enviados ao LLM: o ThoughtSpot exige que um admin habilite o recurso, porque dados da query vão para o LLM, e declara zero data retention com os provedores. A recomendação é confirmar a conformidade com as políticas da empresa — [ThoughtSpot docs](https://docs.thoughtspot.com/cloud/latest/spotter-why)
- O conhecimento institucional do agente da OpenAI passa por um serviço com controle de acesso, para nunca mostrar ao usuário algo que ele não poderia ver — [ByteByteGo](https://blog.bytebytego.com/p/how-openai-built-its-data-agent)
- O BIRD penaliza queries corretas porém lentas (VES), um lembrete de que custo e latência fazem parte da qualidade — [beancount.io](https://beancount.io/bean-labs/research-logs/2026/06/06/bird-benchmark-text-to-sql-real-database-gap)

### Inferences
- Receita para Postgres:
  - `CREATE ROLE analista_ro LOGIN;` com `GRANT USAGE ON SCHEMA analytics` e `GRANT SELECT` apenas nas views curadas, sem acesso a tabelas brutas que tenham PII (telefone, CPF, e-mail de clientes).
  - `ALTER ROLE analista_ro SET default_transaction_read_only = on;` e `ALTER ROLE ... SET statement_timeout = '15s';`, mais `idle_in_transaction_session_timeout` e `CONNECTION LIMIT` baixo.
  - Na aplicação, envolver a query em `BEGIN READ ONLY; ... ROLLBACK;`, aplicar um `LIMIT` automático (ex.: 500 linhas para o modelo, top-20 para o Discord) e aceitar um único statement por chamada.
- Observação técnica, a partir de conhecimento geral de Postgres e não das fontes: `default_transaction_read_only` pode ser alterado pela própria sessão (`SET`). A garantia real vem de o role não ter privilégios de escrita. Também vale considerar uma réplica de leitura ou `pg_stat_statements` para monitorar custo.
- PII: as views devem expor dados agregados ou pseudonimizados (nome do cliente só quando necessário, sem documentos). No Discord, a resposta não deve expor dados pessoais em canais compartilhados, e convém registrar em log as perguntas e os SQL executados para auditoria.

### Gaps
- As fontes de segurança encontradas são guias de praticantes e projetos MCP, não documentação oficial do PostgreSQL nem da Anthropic. Não encontrei orientação oficial da Anthropic específica para agentes SQL read-only.
- Não pesquisei a LGPD especificamente (base legal para enviar dados de clientes a um LLM externo); isso fica como lacuna relevante para uma empresa brasileira.
