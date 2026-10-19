# Método de produção: agentes de IA que operam conta de marketplace

Frente: blogs técnicos, estudos de caso e guias de construção de agentes em produção
Data da pesquisa: 2026-10-19 · Ferramentas: WebSearch, WebFetch e curl em páginas públicas (sem navegador, sem login)
Base de leitura prévia (não repetida aqui): `metodo/estado-da-arte.md` (§6.3 tem a rotina diária, semanal, mensal e trimestral) e `metodo/protocolo.md`. Os CONSOLIDADO.md das quatro plataformas não têm uma seção chamada "Rotina". Os itens de cadência deles estão espalhados (ML §2.6, Shopee §2.6, Amazon §2.3) e foram usados só para não repetir.

Tipos, como no protocolo: [OFICIAL] texto da plataforma ou do fabricante do modelo · [PRÁTICA] guia de praticante ou agência · [CASE] números de uma operação · [DADO] pesquisa ou estatística · [OBS] observação direta desta frente.
Regra temporal do protocolo: regra de plataforma anterior a 2026-04-19 ou sem data leva **(pode estar superada)**. Princípio e método valem sem corte.

---

## (a) Resumo em 10 linhas

1. **O Mercado Livre proíbe, desde os termos de 15/10/2026, agentes de IA "autônomos ou semiautônomos" sem autorização expressa**, inclusive para ler área logada e "por conta própria". Isso atinge de frente o modelo "agente lê o painel pelo Chrome" (cláusula 12, lida na fonte).
2. A Amazon tem uma Agent Policy no contrato do vendedor (BSA) desde 04/03/2026: o agente precisa se identificar como automação e parar quando a Amazon pedir. A Amazon processou a Perplexity em nov/2025 por um agente que se passava por Chrome comum.
3. O caminho aceito pelas três plataformas é a **API oficial** (SP-API, API do ML, Open Platform do TikTok). Navegador com sessão do dono é zona cinzenta, e na Amazon e no ML é zona de risco.
4. Os guias de quem constrói agentes (Anthropic, OpenAI, HumanLayer) convergem: comece simples, faça agentes pequenos e focados, deixe o fluxo de controle no código e não no LLM, guarde o estado em arquivo e peça ok humano por chamada de ferramenta.
5. O que é determinístico vai para script (preço, margem, limites, cálculo de reposição). O LLM interpreta, prioriza e redige.
6. Toda ação recebe uma classificação de risco (leitura, escrita reversível, escrita com dinheiro). As de risco alto passam por aprovação humana; esse é o padrão também da Shopify (Sidekick propõe, lojista salva) e da Amazon (Seller Assistant age "com permissão").
7. Os experimentos de varejo com agente (Project Vend 1 e 2, Andon Market) mostram as mesmas falhas: o agente vende abaixo do custo, dá desconto quando pedem, alucina conta e contato, compra estoque errado. O que corrigiu foi **procedimento obrigatório** ("bureaucracy matters"), CRM e um registro de custo, não um agente "chefe".
8. A Klarna é o caso clássico de atendimento: 2/3 dos chats e o equivalente a 700 pessoas em 2024, mas voltou a contratar humanos em 2025 porque a qualidade caiu. Atendimento ao cliente final fica com humano disponível.
9. A rotina humana que o agente vai imitar é um ciclo diário curto de alarmes (saúde, ruptura, Buy Box ou preço, ritmo de Ads, casos), um semanal de otimização e um mensal de margem e estratégia, cada passo com limites escritos num SOP versionado.
10. Avaliação: comece com 20 a 50 casos tirados de falhas reais e julgue o estado final, não o caminho. Meça a taxa de aprovação humana sem edição: acima de 90% justifica soltar a revisão, abaixo de 70% pede que se reveja o prompt.

---

## (b) Princípios de construção aplicáveis (cada um com fonte)

### B1. Simplicidade primeiro: fluxo fixo antes de agente autônomo
- Ache "the simplest solution possible" e só acrescente complexidade quando ela comprovadamente melhora o resultado. Agentes custam mais e acumulam erros, por isso servem para ambientes de confiança, com teste em sandbox e guardrails. [OFICIAL] Anthropic, *Building effective agents*, 2024-12-19, https://www.anthropic.com/engineering/building-effective-agents
- Antes de ir para vários agentes, aumente um agente só com mais ferramentas, e use um prompt-base com variáveis de política em vez de muitos prompts. [OFICIAL] OpenAI, *A practical guide to building agents*, 2025, https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- **Aplicação:** a rotina diária de uma conta (ler o painel, comparar com limites, gerar alerta) é *prompt chaining* com checagens programáticas entre os passos, não um agente aberto. Agente aberto fica para o diagnóstico ("por que a venda caiu?").

### B2. Os cinco padrões e onde cada um cabe numa conta de marketplace
Fonte dos padrões: Anthropic, *Building effective agents* (B1).
| Padrão | Definição curta | Uso em marketplace |
|---|---|---|
| Encadeamento (*prompt chaining*) | passos fixos com checagem entre eles | rotina diária: coletar → validar números → comparar com limites → relatório |
| Roteamento | classifica a entrada e manda ao especialista | o bot do Discord manda "pergunta de ML" ao agente do ML; pergunta de comprador vs. reclamação vs. devolução |
| Paralelização (seções ou votação) | subtarefas independentes, ou a mesma tarefa várias vezes | auditar 4 marketplaces em paralelo; "votação" de 3 leituras antes de propor mudança de preço |
| Orquestrador e trabalhadores | o LLM central divide o trabalho e sintetiza | estratégia multimarketplace: um orquestrador e um trabalhador por plataforma |
| Avaliador e otimizador | um gera, outro critica, em laço com critério claro | título e ficha de anúncio contra checklist da plataforma; revisão de resposta ao cliente |

### B3. Agentes pequenos e focados, e o orquestrador não é um "chefe"
- Fator 10 dos 12-factor agents: "Small, Focused Agents". O fator 8, "Own your control flow", diz que a lógica fica no seu código. [PRÁTICA] HumanLayer, https://github.com/humanlayer/12-factor-agents (s/d; repositório ativo em 2026)
- No Project Vend 2, um agente "CEO" (Seymour Cash) reduziu os descontos em cerca de 80%, mas aprovou pedidos lenientes cerca de 8 vezes mais do que negou e triplicou os reembolsos. A conclusão da Anthropic é que ele tinha os mesmos pontos cegos do subordinado. A separação de papéis (um agente só para merch, o Clothius) ajudou. [CASE] Anthropic, *Project Vend: Phase Two*, 2025-12-18, https://www.anthropic.com/research/project-vend-2
- Sistemas multiagente rendem mais em tarefa paralelizável: +90,2% contra agente único em pesquisa interna, ao custo de cerca de 15 vezes os tokens de um chat. **Não** servem quando todos precisam do mesmo contexto ou há muita dependência entre as partes. [OFICIAL] Anthropic, *How we built our multi-agent research system*, 2025-06-13, https://www.anthropic.com/engineering/multi-agent-research-system
- **Aplicação:** um agente por marketplace (contexto próprio, regras próprias) com um orquestrador fino que só sintetiza. Supervisão de dinheiro com humano, não com outro LLM.

### B4. Memória e estado em arquivos, com rotina de abertura de sessão
- Anotações estruturadas fora da janela de contexto (NOTES.md, lista de tarefas), recarregadas depois. Recuperação "just-in-time": guardar caminhos e consultas leves e carregar sob demanda. Compactação quando a janela enche. [OFICIAL] Anthropic, *Effective context engineering for AI agents*, 2025-09-29, https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Agentes de longa duração começam cada sessão sem memória. A solução é um arquivo de progresso, uma lista de tarefas em **JSON** (o modelo sobrescreve Markdown com mais facilidade) e commits descritivos. A rotina de início: ler o log e o progresso, pegar a prioridade mais alta, rodar uma checagem de ponta a ponta antes de mexer. [OFICIAL] Anthropic, *Effective harnesses for long-running agents*, 2025-11-26, https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Fator 5, "Unify execution state and business state", e fator 12, "stateless reducer": cada passo leva estado mais entrada a novo estado. [PRÁTICA] HumanLayer (B3)
- **Aplicação:** LEIA-ME.md e custos.md seguem como estão (texto para humano), mas o estado operacional (limites, último snapshot do painel, pendências de aprovação) deve ficar em JSON ou TSV que o agente só atualiza campo a campo. Snapshot diário datado permite comparar com o dia anterior sem reler tudo.

### B5. Ferramenta determinística para tudo que é conta, e o LLM para o resto
- As skills podem trazer scripts para operações que custam mais caras em geração de texto e dão resultado consistente e repetível. Carga progressiva: só nome e descrição no início, o corpo quando for relevante. [OFICIAL] Anthropic, *Equipping agents for the real world with Agent Skills*, 2025-10-16 (atualizado 2025-12-18), https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Hooks são determinísticos e garantem a ação; instruções no CLAUDE.md são só consultivas. CLAUDE.md curto: "Would removing this cause Claude to make mistakes?" [OFICIAL] Claude Code, *Best practices*, https://code.claude.com/docs/en/best-practices (s/d, lido 2026-10-19)
- No Project Vend 2, o que mais melhorou o resultado foi obrigar o agente a verificar preço e prazo com ferramenta antes de prometer, além de manter um registro do custo de cada item. [CASE] Anthropic, Project Vend 2 (B3)
- **Aplicação:** preço mínimo, margem por SKU e ACOS de equilíbrio saem de script (os scripts de preço já existentes). O agente nunca escreve um preço que o script não validou. Um hook pode bloquear qualquer escrita em formulário de preço se o valor estiver abaixo do piso.

### B6. Projetar as ferramentas para o modelo (ACI)
- Poucas ferramentas de alto impacto, que consolidam passos. Prefixos por serviço. Retornos com nomes legíveis, paginados e truncados. Mensagens de erro que orientam a correção. [OFICIAL] Anthropic, *Writing effective tools for agents*, 2025-09-11, https://www.anthropic.com/engineering/writing-tools-for-agents
- *Poka-yoke* nos argumentos: caminho absoluto em vez de relativo eliminou uma classe de erro. [OFICIAL] Anthropic, *Building effective agents* (B1)
- **Aplicação:** em vez de "o agente navega e lê a tela", ferramentas como `ml_ler_reputacao()`, `amz_ler_saude_conta()` e `preco_validar(sku, preco)`, que devolvem JSON pequeno.

### B7. Aprovação humana por risco da ferramenta, não por agente
- Dê a cada ferramenta uma classificação baixa, média ou alta, considerando leitura ou escrita, reversibilidade, permissão exigida e impacto financeiro. As de risco alto pausam para checagem ou escalam para humano. Os dois gatilhos de intervenção são estourar o limite de falhas e fazer uma ação sensível, irreversível ou de alto impacto. [OFICIAL] OpenAI, guia prático (B1)
- Três padrões de humano no laço: **notificar** (avisa, não age), **perguntar** (pede dado que falta, não chuta) e **revisar** (aprovar, editar ou comentar a ação proposta). Use uma "caixa de entrada" de pendências em vez de notificação de chat, que se perde com facilidade. [OFICIAL-fornecedor] LangChain, *Introducing ambient agents*, 2025-01-14, https://www.langchain.com/blog/introducing-ambient-agents
- Fator 7, "Contact humans with tool calls": pedir aprovação é uma chamada de ferramenta estruturada, não um texto solto. [PRÁTICA] HumanLayer (B3)
- Para Amazon: revisão humana de toda saída, aprovação obrigatória para qualquer escrita na conta (anúncio, preço, lance), rejeições registradas e devolvidas ao prompt. [PRÁTICA] Seller Labs, *Building an AI agent for Amazon tasks*, atualizado 2026-08-03, https://www.sellerlabs.com/knowledge-base/building-an-ai-agent-for-amazon-tasks-whats-possible-today/
- **Aplicação no bot do Discord:** cada pedido de ok vira um cartão com botões (aprovar, editar, recusar) e um id. O que está pendente fica num arquivo de pendências, não só na mensagem.

### B8. Verificação e avaliação contínuas
- Comece com "20-50 simple tasks drawn from real failures". Julgue o estado final, não o caminho. Use pass^k para agente que precisa acertar sempre: 75% por tentativa dá cerca de 42% de acertar 3 seguidas. Separe avaliação de capacidade de avaliação de regressão. Leia as transcrições. [OFICIAL] Anthropic, *Demystifying evals for AI agents*, 2026-01-09, https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Juiz LLM com uma nota de 0 a 1 e aprovado ou reprovado concordou melhor com humanos. O teste humano pegou viés por fonte de SEO fraca. [OFICIAL] Anthropic, multiagente (B3)
- Dê ao agente uma checagem que ele mesmo rode e mostre evidência (print, saída de comando) em vez de afirmar sucesso. Um revisor em contexto limpo encontra mais, mas é preciso mandá-lo apontar só o que afeta a correção. [OFICIAL] Claude Code, *Best practices* (B5)
- Comece estreito (uma tarefa, um revisor, cerca de 30 dias) e acompanhe a taxa de aprovação sem edição (acima de 90% justifica afrouxar, abaixo de 70% pede revisão do prompt). [PRÁTICA] Seller Labs (B7)
- **Aplicação:** um conjunto de casos por marketplace, como print do painel do dia X e alerta esperado, ou pergunta de comprador e resposta aceitável, rodado a cada mudança de CLAUDE.md ou skill.

### B9. Observabilidade e retomada
- Rastreamento completo em produção para diagnosticar. Retomar do checkpoint em vez de recomeçar. Tentar de novo com regra determinística e deixar o agente se adaptar quando a ferramenta falha. Implantar versões aos poucos ("rainbow deployment") porque há agentes no meio de execução. [OFICIAL] Anthropic, multiagente (B3)
- Fator 9, "Compact Errors into Context Window": o erro resumido volta ao modelo para ele se corrigir. [PRÁTICA] HumanLayer (B3)
- **Aplicação:** cada turno grava em log o que leu (URL e hora), o que concluiu e o que propôs. O `dados/bot.log` da central já é a base. Falta um log de decisões por marketplace.

### B10. Custo
- Agentes gastam cerca de 4 vezes os tokens de um chat, e multiagente cerca de 15 vezes. O uso de tokens explicou cerca de 80% da variação de desempenho no BrowseComp. Multiagente só vale para tarefa de valor alto. [OFICIAL] Anthropic, multiagente (B3)
- Comece com o modelo mais capaz para fixar a linha de base e troque por um menor onde ele ainda passar nas avaliações. [OFICIAL] OpenAI, guia prático (B1)
- Os relatos de agente em laço infinito (um pipeline de 4 agentes que teria custado US$ 47 mil em 11 dias, nov/2025) apontam como causa a falta de teto por sessão e de um corte antes da próxima chamada. [PRÁTICA, fornecedor, não verificado] https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i
- **Aplicação:** teto de turnos e de tempo por sessão disparada pelo bot. A rotina diária usa modelo menor, e o diagnóstico e a estratégia usam o maior.

### B11. Conteúdo lido é dado, nunca instrução (injeção de prompt)
- O Claude in Chrome tem classificadores contra injeção de prompt e pede confirmação em ações de risco alto. A própria Anthropic diz que o risco "não é zero" (cerca de 1% de sucesso de ataque nos testes internos). [OFICIAL] https://support.claude.com/en/articles/12902428 (s/d, lido 2026-10-19)
- Skills de terceiros podem induzir vazamento de dados; leia os arquivos antes de usar. [OFICIAL] Anthropic, Agent Skills (B5)
- **Aplicação:** pergunta de comprador, avaliação e anúncio de concorrente são texto hostil em potencial. O agente de marketplace nunca executa instrução que venha dali. Isso já está no protocolo (regra 1); vale estender aos agentes operacionais.

### B12. O agente prestativo demais é risco de negócio
- O Claudius (Project Vend 1) vendeu abaixo do custo, deu códigos de desconto e itens grátis quando pediram, recusou US$ 100 por um item de cerca de US$ 15, inventou uma conta de pagamento e um contato, e voltou a dar desconto dias depois de concordar em parar. [CASE] Anthropic, *Project Vend*, 2025-06-27, https://www.anthropic.com/research/project-vend-1
- No Project Vend 2, o agente ainda queria ser "a friend who just wants to be nice". Um funcionário o convenceu de que tinha sido eleito CEO. [CASE] Project Vend 2 (B3)
- **Aplicação:** a política de preço, de desconto e de reembolso fica escrita como regra dura com piso numérico, e o agente não tem autoridade para criar exceção. Exceção é sempre pedido de ok.

---

## (c) Casos de e-commerce e varejo com agentes

| Caso | O que foi automatizado | O que ficou humano | Números | Fonte |
|---|---|---|---|---|
| **Amazon Seller Assistant (agêntico)**, EUA, set/2025 | monitora a conta continuamente, define metas e estratégias, estoque (sinaliza item parado, sugere remarcar ou remover, agenda envio), conta e anúncios; roda em Bedrock com Nova e Claude | "com permissão, age em nome do vendedor"; "o vendedor mantém o controle da decisão final" | sem números de adoção | [OFICIAL] https://sellingpartners.aboutamazon.com/amazon-accelerate-2025-a-new-era-of-tools-and-technology-for-independent-sellers (2025-09-18); [PRÁTICA] Forrester, https://www.forrester.com/blogs/amazon-accelerate-2025-seller-event-takeaways-agentic-ai-supply-chain-mcf-retail-ads/ |
| **Amazon Brasil**, Conecta 2026 | Creative Studio (gera anúncio) e assistente do vendedor (dúvidas, métricas do Seller Central, sugestões) | não informado | 100 mil vendedores no BR; anunciado como "em breve" | [PRÁTICA, imprensa] Itatiaia, 2026-05-20, https://www.itatiaia.com.br/economia/negocios/amazon-brasil-anuncia-ferramentas-de-ia-para-auxiliar-vendedores-parceiros |
| **Shopify Sidekick** | assistente dentro do admin; lê dados de apps e **propõe** ações | o lojista confirma antes de salvar (modelo "propõe e aprova") | Q2/2026: cerca de 34 milhões de conversas no trimestre, uso diário 3,6 vezes maior em um ano, mais de 36 mil apps criados | [OFICIAL] https://shopify.dev/docs/apps/build/ai (s/d); [PRÁTICA, imprensa] Retail TouchPoints, https://www.retailtouchpoints.com/topics/retail-technology/ai-ar-vr/shopify-credits-ai-for-34-revenue-growth-in-q2-2026 |
| **Klarna**, atendimento | assistente de IA no chat de atendimento | em 2025, voltou a contratar humanos e garante "sempre haverá um humano" | 1º mês (2024): 2,3 milhões de conversas, 2/3 dos chats, equivalente a 700 pessoas, resolução de 11 para menos de 2 minutos, 25% menos recontato, ganho estimado de US$ 40 milhões; em 2025 o CEO admitiu que o custo pesou demais e a qualidade caiu | [OFICIAL] https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/ (2024-02-27); [PRÁTICA, imprensa] https://www.maginative.com/article/klarna-dials-back-its-ai-customer-service-strategy-now-its-hiring-humans-again/ (2025-05) |
| **Project Vend 1** (Anthropic e Andon Labs), loja no escritório | escolha de produto, preço, reposição, atendimento por Slack | compra física e reposição por humanos | prejuízo no período; a maior queda veio dos cubos de metal vendidos abaixo do custo | [CASE] https://www.anthropic.com/research/project-vend-1 (2025-06-27) |
| **Project Vend 2** | o mesmo, mais CRM, registro de custo por item, link de pagamento antes do pedido, lembretes, agente "CEO" e agente de merch | aprovação de compra por humano | semanas de margem negativa "em grande parte" eliminadas; 3 cidades; descontos cerca de 80% menores, reembolsos 3 vezes maiores | [CASE] https://www.anthropic.com/research/project-vend-2 (2025-12-18) |
| **Andon Market** (SF, abr/2026) | o agente Luna (Sonnet 4.6) escolhe conceito, preço, estoque e contrata pessoas | equipe física | orçamento de US$ 100 mil; relatos de prejuízo de US$ 13 mil nas primeiras semanas e de caixa caindo a cerca de US$ 60 mil em 5 meses; excesso de velas no estoque | [PRÁTICA, imprensa secundária, não verificado] https://www.retailcustomerexperience.com/news/andon-launches-ai-run-store-in-san-francisco/ ; https://completeaitraining.com/news/san-franciscos-first-ai-run-store-loses-13000-in-its-first/ |
| **Mercado Livre Verdi** | agente de atendimento ao *vendedor*: qualidade de anúncio, rotulagem de produto, dúvida tributária (AR e MX) | não informado | "mais da metade" do suporte a vendedores no Chile resolvido de forma autônoma (fonte secundária) | [PRÁTICA, imprensa] https://www.mobiletime.com.br/?p=836618 ; https://www.descubre.vc/noticia/mercado-libre-proyecta-un-futuro-de-compras-aut-nomas-con-ia-para-2026-2026-07-16 |
| **Grupo OLX**, BR | mais de 300 agentes de IA, a maioria de eficiência operacional | não informado | R$ 440 milhões de investimento com foco em IA | [PRÁTICA, imprensa] https://www.baguete.com.br/noticias/olx-investe-r-440-mi-com-foco-em-ia (2026-05-18) |
| **Contraexemplo de automação de preço**: RepricerExpress, Amazon UK | reprecificador em laço baixou preços para 1 centavo de libra durante cerca de 1 hora | ninguém olhando | um vendedor relatou 1.600 pedidos na primeira hora; perdas de dezenas de milhares de libras; a Amazon não reembolsou | [CASE, imprensa] https://www.channel4.com/news/amazon-glitch-repricerexpress-friday-online-retailers (2014-12-15) **(antigo, vale como modo de falha)** |

**O que os casos têm em comum:**
- a plataforma automatiza leitura, diagnóstico e proposta, e a escrita fica com aprovação do dono (Amazon e Shopify);
- atendimento ao comprador escala com IA, mas a marca precisa de um humano disponível (Klarna);
- agente com autonomia sobre preço e desconto perde dinheiro até ganhar procedimento obrigatório e um registro de custo (Vend);
- preço automático sem limite rígido gera perda em minutos (RepricerExpress).

**Agências de marketplace no Brasil:** não achei nenhum caso publicado com números de agência que opere ML ou Shopee com agentes de IA (ver lacunas). O que circula é ferramenta de análise com IA (JoomPulse: parceria exclusiva de analytics com a Shopee em ago/2026 e mais de 30 mil vendedores de ML, segundo a própria empresa) e agentes de venda por WhatsApp (Fórum E-Commerce Brasil 2026). [PRÁTICA, imprensa] https://nossomeio.com.br/joompulse-fecha-parceria-com-shopee-e-amplia-acesso-a-inteligencia-de-mercado-para-mais-de-100-mil-vendedores-brasileiros/ ; https://olhardigital.com.br/2026/08/16/colunistas/os-agentes-de-ia-estao-revolucionando-o-e-commerce

---

## (d) Rotina do gestor humano, em checklist (só o que acrescenta à §6.3 do estado-da-arte)

A §6.3 já traz a cadência em tabela. O que segue acrescenta **itens concretos, tempo por tarefa, gatilhos de escalada e a forma do SOP**, que é o que o agente precisa para imitar a rotina. Para cada item, marquei entre colchetes o risco da ação (L = leitura, E = escrita reversível, $ = escrita que mexe com dinheiro).

### Comum a todos os marketplaces: o formato do SOP [PRÁTICA]
- [ ] Cabeçalho: data da última revisão, data da próxima, versão e dono.
- [ ] Corpo: caminho exato de cliques, prints anotados, árvore de decisão e tempo estimado por tarefa.
- [ ] Revisão a cada 90 dias, ou antes se a plataforma mudar a interface. Quem revisa é alguém que não escreveu o SOP e segue o passo a passo.
Fonte: Jarvio, 2026-02-25, https://jarvio.io/blog/amazon-business-sops
- [ ] Toda mudança de risco alto tem regra de aprovação escrita. O controle da conta principal fica com a marca. Acessos externos são revistos periodicamente. Fonte: SalesDuo, https://salesduo.com/blog/amazon-account-management-agency-checklist (s/d)
→ **Para o agente:** isso é, literalmente, uma skill por marketplace com cabeçalho de versão, e o "caminho de cliques" vira a ferramenta de leitura.

### Amazon
**Diário** (fonte: SalesDuo, atualizado 2026-09-22, https://salesduo.com/blog/amazon-account-manager-daily-checklist; Jarvio)
- [ ] [L] Saúde da conta (AHR) e Policy Compliance: violações ou avisos novos.
- [ ] [L] Preço dos ASINs principais; vendedor não autorizado no anúncio.
- [ ] [L] Anúncios campeões no ar, com imagem e título corretos e sem supressão.
- [ ] [L] Casos abertos no Seller Support: cobrar os urgentes e os parados.
- [ ] [L] Buy Box (Oferta em Destaque) nos campeões, ao menos uma vez por dia.
- [ ] [L] Ads: ritmo de gasto e campanha fora do ar. Lance não se mexe no diário. Leva de 5 a 10 minutos.
- [ ] [L] Risco de ruptura urgente.
- [ ] [L] Feedback de vendedor novo.
- **Não espera a semana:** ruptura súbita, perda grande de Buy Box, gasto de Ads disparado, margem despencando (SalesDuo).

**Semanal**
- [ ] [L] Perda sustentada de Buy Box; cobertura em semanas; inbound atrasado.
- [ ] [E] Termos de busca: 30 a 45 minutos. Termo com 20 ou mais cliques e zero conversão vira negativa exata, registrada com termo, cliques e gasto (Jarvio).
- [ ] [$] Ajuste de lance e de segmentação (SupplyKick, 2026-05-19, atualizado 2026-09-14, https://www.supplykick.com/blog/amazon-account-management-services).
- [ ] [L] Avaliações negativas novas e queixa repetida; idade dos casos.
- [ ] [L] Margem: vendas, unidades, tarifas, devoluções e margem de contribuição contra o plano ("margem caindo com venda estável" é gatilho).
- [ ] [L] Reposição: pedir quando os dias de estoque caírem abaixo do prazo de reposição + 14 dias. Quantidade = velocidade média diária × (prazo + 21) (Jarvio).
- [ ] [L] Resumo por e-mail ao cliente, sem reunião (SupplyKick).

**Mensal**
- [ ] Revisão de negócio e estratégia; auditoria de catálogo; lucratividade; prioridades do portfólio; previsão; plano de testes dos próximos 30 dias (SalesDuo; SupplyKick).
- [ ] [L] IPI: abaixo de 400, remover o que tem mais de 365 dias de estoque; entre 400 e 500, considerar reposição 20% menor (Jarvio, prática; o estado-da-arte já aponta divergência sobre o limite do IPI).
- [ ] Ligação de 30 a 45 minutos com o cliente. KPIs do relatório: receita e lucro, gasto e ROAS, conversão e tráfego, BSR, giro de estoque, sempre semana contra semana, mês contra mês e ano contra ano (SupplyKick).
- [ ] [E] Renovar criativos (A+, vídeo, imagem) e reestruturar campanhas.

**Trimestral:** auditoria lenta do estoque parado (Jarvio); revisão dos SOPs.

### Mercado Livre
Acréscimos ao que já está no ML CONSOLIDADO §2.6 (rotina diária da reputação com alerta a 50% do limite):
- [ ] [L] **Diário:** perguntas sem resposta e tempo de resposta; reclamações e mediações abertas; envios atrasados ou a despachar; ruptura dos campeões e Full; orçamento de Ads esgotado; experiência de compra por anúncio (API /purchase_experience, já citada no estado-da-arte).
- [ ] [L] **Semanal:** qualidade das publicações (/health → /performance); preço contra concorrente direto e price matching; ROAS e ACOS por campanha.
- [ ] [L] **Mensal:** análise de mercado (Métricas > Análise de mercado), já descrita no estado-da-arte §2.1.
- KPIs operacionais citados por praticantes BR: tempo médio de despacho, % de perguntas respondidas em até 1 hora, cancelamento por ruptura. Revisão semanal, metas mensais e alerta quando o indicador cai abaixo da meta. [PRÁTICA] YAV, https://yav.com.br/blog/kpis-ecommerce-marketplace/ (s/d)
- **Sem fonte primária de rotina de agência brasileira** (ver lacunas). Estes itens são síntese das notas existentes mais as fontes acima.

### Shopee
- [ ] [L] **Diário:** pedidos a enviar dentro do prazo (a taxa de não cumprimento pesa); chat sem resposta; pontos de penalidade novos.
- [ ] [L] **Semanal:** métricas do Vendedor Indicado, que é reavaliado toda semana e cuja punição chega na semana seguinte (Shopee CONSOLIDADO §2.6); ROAS semanal das campanhas.
- [ ] [L] **Trimestral:** os pontos zeram por trimestre (estado-da-arte §6.2); planejar com folga.

### TikTok Shop
- [ ] [L] **Diário:** SPS, que é atualizado todo dia e relativo à categoria (TikTok CONSOLIDADO §1.1); resposta em até 24 horas; pedidos atrasados (LDR).
- [ ] [L] **Semanal:** GMV Max (ROI contra meta), vídeos e afiliados que puxaram venda.

### Como a rotina vira agente (síntese desta frente)
| Cadência | Padrão de agente | Humano no laço |
|---|---|---|
| Diário | encadeamento fixo (B1): ler, comparar com os limites do JSON e soltar alerta | notificar |
| Semanal | trabalhador por marketplace, mais um avaliador para as propostas | revisar (aprovar ou editar) |
| Mensal | orquestrador multimarketplace (B2), com diagnóstico aberto | perguntar e revisar |
| Trimestral | auditoria (evidência → diagnóstico → risco → ação, como na §6.1) | decisão do dono |

---

## (e) Riscos e políticas

### E1. Políticas oficiais sobre automação
| Plataforma | O que diz | Tipo e data | Efeito para agente que lê o painel pelo Chrome |
|---|---|---|---|
| **Mercado Livre**, Termos e condições gerais, cláusula 12, "Uso Automatizado do Site e Acesso à Informação" | Proíbe "bots, spiders, scrapers ou crawlers, agentes" e software "inclusive os baseados em inteligência artificial, que atuem de forma autônoma ou semiautônoma" para "acessar, interagir, executar operações", "por conta própria ou de terceiros, sem a correspondente autorização expressa". Vale em especial para (b) informação "disponível apenas mediante autenticação prévia" e (d) a "tentativa de contornar medidas técnicas de proteção". Prevê bloqueio, suspensão e medidas judiciais. | [OFICIAL] última modificação em **2026-10-15**, https://www.mercadolivre.com.br/ajuda/Termos-e-condicoes-gerais-de-uso_1409 (lido via curl em 2026-10-19) | **Risco alto.** O texto cobre literalmente um agente de IA semiautônomo lendo a área logada da própria conta. A via autorizada é a API com app registrado (developers.mercadolivre.com.br). Não achei a versão anterior para saber se a cláusula é nova. |
| ML, mesmos termos, conta e acesso | Proíbe compartilhar "login, senha, token, códigos de verificação" com terceiros. As Contas Colaboradoras servem só à gestão operacional pelo titular, que responde por tudo. | [OFICIAL] idem | O agente deve usar sessão ou conta colaboradora do próprio titular, nunca uma credencial repassada. |
| ML API | 429 = excesso de requisições; limite por Client ID e por endpoint; usar *backoff* exponencial com *jitter*; pedir aumento de RPM com evidência de uso | [OFICIAL] https://developers.mercadolivre.com.br/pt-br/rate-limit-erro-429 (atualizado em 2026-05-05, segundo a busca) | Sem número público de RPM. |
| **Amazon**, BSA com Agent Policy | Em vigor desde 2026-03-04 (anunciada em 2026-02-17). Define "Agent". O agente deve se identificar como sistema automatizado o tempo todo, seguir a Agent Policy e parar o acesso na hora se a Amazon pedir. Proíbe usar materiais da Amazon para desenvolver IA. O uso contínuo conta como aceite. | [PRÁTICA, resumos de terceiros; o texto oficial exige login] https://ppc.land/amazons-new-ai-agent-rules-shake-up-sellers-before-march-4-deadline/ ; https://canopymanagement.com/amazon-bsa-agent-policy-march-2026/ ; página oficial: https://sellercentral.amazon.com/help/hub/reference/GS83KH2MA7HM69PH | **Risco alto e sem resposta.** Um agente rodando no Chrome do dono não se identifica como automação. Os comentaristas incluem automação de navegador e "assistentes de IA operando o Seller Central" no escopo e os classificam como o caso de maior risco. Não confirmei se vale para a Amazon.com.br. |
| Amazon, Conditions of Use (Agent Terms) | "No Agent may access, use, or interact with Amazon Services unless, at all times, it identifies itself" | [PRÁTICA, rastreador de cláusulas; captura de 2026-09-14] https://conductatlas.com/platform/amazon/amazon-conditions-of-use/provision/CA-P-018576/agent-must-identify-itself-in-all-requests/ | Vale para o lado do comprador (pesquisa de concorrente na vitrine). |
| Amazon contra Perplexity | Processo de 2025-11-04 (N.D. Cal.) com base na CFAA e na lei da Califórnia. O agente Comet se apresentava como Chrome comum e burlou um bloqueio técnico em 24 horas. | [PRÁTICA, imprensa] https://the-decoder.com/a-court-battle-over-perplexitys-comet-agent-could-define-how-ai-is-allowed-to-shop-online-for-users/ | Mostra que a Amazon detecta e bloqueia agentes, e processa quem insiste. |
| Amazon, recomendação de praticante | Usar SP-API e Ads API. Automação de navegador que imita login humano viola as Conditions of Use e pode levar a suspensão. Permissão mínima, credencial guardada com segurança, *backoff*. | [PRÁTICA] Seller Labs, 2026-08-03 (B7) | |
| **TikTok**, Termos de Serviço (BR) | Proíbe "usar scripts automatizados para colher informações", usar a conta de outra pessoa e burlar medidas que limitam acesso | [OFICIAL] https://www.tiktok.com/legal/page/row/terms-of-service/pt-BR, versão de set/2020 **(pode estar superada)** | Não achei o texto oficial dos termos do vendedor do TikTok Shop sobre ferramentas de terceiros. Um guia de fornecedor (UE) lista como proibidos scraping e ferramenta de terceiro não autorizada, e diz que resposta de bot deve vir rotulada. |
| TikTok, API | Limite por API em janela deslizante de 1 minuto; 429 `rate_limit_exceeded` | [OFICIAL] https://developers.tiktok.com/doc/tiktok-api-v2-rate-limit (é a API geral, não a do Shop) | |
| **Shopee** | Não achei a cláusula. As páginas usam um SDK "anti_crawler" ([OBS] no HTML de shopee.com.br/docs/3612, 2026-10-19) | — | É lacuna. |

### E2. Riscos operacionais e mitigação
| Risco | Evidência | Mitigação |
|---|---|---|
| Bloqueio ou suspensão da conta por automação | cláusula 12 do ML; Agent Policy da Amazon; detecção ativa (Perplexity) | 1) API oficial sempre que existir; 2) agente no navegador só lê, em ritmo humano, sem contornar captcha nem proteção, que é exatamente o item (d) do ML; 3) pedir à plataforma uma autorização expressa ou usar app registrado; 4) registrar a decisão de risco com o dono |
| Captcha ou desafio | o ML proíbe contornar medida técnica; o Claude in Chrome pausa ações de risco | captcha é parada obrigatória: o agente para e notifica o humano, nunca tenta resolver |
| Limite de API (429) | ML e TikTok (E1) | *backoff* com *jitter*, cache do snapshot do dia, consultas agrupadas |
| Preço alucinado ou errado | Project Vend (preço sem pesquisa, abaixo do custo); RepricerExpress (laço até 1 centavo) | preço só via script com piso (custo + tarifa + frete + margem mínima); dupla leitura antes de propor; humano aprova toda escrita de preço; limite de variação por dia (ex.: no máximo 10% sem ok, a definir) |
| Gasto de Ads disparado | gasto disparado é o gatilho de escalada mais citado pelas agências; os relatos de agente em laço vêm de falta de teto | o agente não mexe em orçamento nem lance sem ok; alerta diário de ritmo de gasto; teto escrito por campanha |
| Desconto ou exceção concedidos por persuasão | Vend 1 e 2 | regra dura sem autoridade de exceção; mensagem de comprador é dado, não ordem (B11) |
| Injeção de prompt por pergunta, avaliação ou anúncio | Anthropic: risco "não é zero" (cerca de 1%) | ler conteúdo de terceiro em contexto sem ferramentas de escrita; separar o leitor de quem age |
| Política inventada ou mal lida pelo LLM | Seller Labs: anúncio fora da regra, supressão, alerta de saúde | toda regra citada pelo agente leva URL e data (como no protocolo); avaliador confere contra o CONSOLIDADO |
| Agente "chefe" que aprova tudo | Vend 2 (Seymour Cash) | aprovação de dinheiro sempre com humano |
| Atendimento ao comprador só com IA | Klarna em 2025 | rascunho com IA e envio humano, ou humano sempre disponível; nas plataformas que exigem, rotular a automação |
| Custo de tokens | 4 vezes (agente) e 15 vezes (multiagente) | rotina diária com modelo menor; teto de turnos por sessão |

---

## (f) Tabela de afirmações

| id | afirmação | tipo | URL | data |
|---|---|---|---|---|
| MP01 | Cinco padrões de fluxo (encadeamento, roteamento, paralelização, orquestrador e trabalhadores, avaliador e otimizador); começar pelo mais simples | OFICIAL | https://www.anthropic.com/engineering/building-effective-agents | 2024-12-19 |
| MP02 | Agentes acumulam erros e pedem teste em sandbox e guardrails; o agente pode pausar para feedback humano em pontos de checagem | OFICIAL | idem | 2024-12-19 |
| MP03 | Anotações estruturadas fora do contexto, recuperação just-in-time, compactação; subagentes devolvem resumos de 1.000 a 2.000 tokens | OFICIAL | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 2025-09-29 |
| MP04 | Multiagente +90,2% contra agente único; cerca de 15 vezes os tokens; tokens explicam cerca de 80% da variação no BrowseComp | OFICIAL | https://www.anthropic.com/engineering/multi-agent-research-system | 2025-06-13 |
| MP05 | Multiagente não serve com contexto compartilhado e muita dependência entre as partes | OFICIAL | idem | 2025-06-13 |
| MP06 | Avaliação com cerca de 20 consultas no começo; juiz LLM de 0 a 1 concorda com humanos; julgar o estado final | OFICIAL | idem | 2025-06-13 |
| MP07 | Lista de tarefas em JSON (o Markdown é sobrescrito mais), arquivo de progresso, rotina de início de sessão | OFICIAL | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | 2025-11-26 |
| MP08 | Skills com scripts para operação determinística; carga progressiva | OFICIAL | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | 2025-10-16 |
| MP09 | Poucas ferramentas consolidadas, prefixos, retorno enxuto, erro que orienta | OFICIAL | https://www.anthropic.com/engineering/writing-tools-for-agents | 2025-09-11 |
| MP10 | Avaliações: 20 a 50 tarefas tiradas de falhas reais; pass^k; capacidade contra regressão; ler transcrições | OFICIAL | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | 2026-01-09 |
| MP11 | Hooks são determinísticos e o CLAUDE.md é consultivo; CLAUDE.md curto; checagem que o agente roda sozinho | OFICIAL | https://code.claude.com/docs/en/best-practices | s/d (lido 2026-10-19) |
| MP12 | Classificar o risco de cada ferramenta (baixo, médio, alto) por escrita, reversibilidade, permissão e impacto financeiro; intervenção humana por limite de falhas e por ação de risco alto | OFICIAL | https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf | 2025 |
| MP13 | Linha de base com o modelo mais capaz e depois troca por modelos menores; padrões gerente e descentralizado | OFICIAL | idem | 2025 |
| MP14 | Humano no laço: notificar, perguntar, revisar; caixa de entrada de agente melhor que o Slack | OFICIAL (fornecedor) | https://www.langchain.com/blog/introducing-ambient-agents | 2025-01-14 |
| MP15 | 12 fatores: agentes pequenos, controle do fluxo no código, contatar humano por chamada de ferramenta, estado unificado | PRÁTICA | https://github.com/humanlayer/12-factor-agents | s/d |
| MP16 | Claudius vendeu abaixo do custo, deu desconto quando pediram, alucinou conta e contato, não aprendeu | CASE | https://www.anthropic.com/research/project-vend-1 | 2025-06-27 |
| MP17 | Vend 2: procedimento obrigatório e ferramentas (CRM, custo por item) trouxeram o lucro; o agente CEO aprovava pedido leniente cerca de 8 vezes mais do que negava | CASE | https://www.anthropic.com/research/project-vend-2 | 2025-12-18 |
| MP18 | Andon Market: US$ 100 mil de orçamento e prejuízos relatados | PRÁTICA (imprensa, não verificado) | https://completeaitraining.com/news/san-franciscos-first-ai-run-store-loses-13000-in-its-first/ | 2026-04 |
| MP19 | Seller Assistant agêntico age "com permissão"; o vendedor mantém a decisão final | OFICIAL | https://sellingpartners.aboutamazon.com/amazon-accelerate-2025-a-new-era-of-tools-and-technology-for-independent-sellers | 2025-09-18 |
| MP20 | Amazon BR anunciou Creative Studio e assistente do vendedor (ainda "em breve") | PRÁTICA (imprensa) | https://www.itatiaia.com.br/economia/negocios/amazon-brasil-anuncia-ferramentas-de-ia-para-auxiliar-vendedores-parceiros | 2026-05-20 |
| MP21 | Sidekick propõe a ação e o lojista confirma antes de salvar | OFICIAL | https://shopify.dev/docs/apps/build/ai | s/d |
| MP22 | Sidekick: cerca de 34 milhões de conversas no Q2/2026; uso diário 3,6 vezes maior | PRÁTICA (imprensa sobre resultado) | https://www.retailtouchpoints.com/topics/retail-technology/ai-ar-vr/shopify-credits-ai-for-34-revenue-growth-in-q2-2026 | 2026-08 |
| MP23 | Klarna: 2/3 dos chats, equivalente a 700 pessoas, de 11 para menos de 2 minutos, US$ 40 milhões | OFICIAL | https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/ | 2024-02-27 |
| MP24 | Klarna volta a contratar humanos porque a qualidade caiu | PRÁTICA (imprensa) | https://www.maginative.com/article/klarna-dials-back-its-ai-customer-service-strategy-now-its-hiring-humans-again/ | 2025-05 |
| MP25 | RepricerExpress levou preços a 1 centavo de libra em cerca de 1 hora; a Amazon não reembolsou | CASE (imprensa) | https://www.channel4.com/news/amazon-glitch-repricerexpress-friday-online-retailers | 2014-12-15 |
| MP26 | Cláusula 12 do ML proíbe agentes de IA autônomos ou semiautônomos sem autorização expressa, inclusive em área logada e por conta própria | OFICIAL | https://www.mercadolivre.com.br/ajuda/Termos-e-condicoes-gerais-de-uso_1409 | 2026-10-15 |
| MP27 | O ML proíbe compartilhar login, senha ou token; as Contas Colaboradoras servem só à gestão pelo titular | OFICIAL | idem | 2026-10-15 |
| MP28 | API do ML: limite por Client ID e por endpoint; backoff com jitter | OFICIAL | https://developers.mercadolivre.com.br/pt-br/rate-limit-erro-429 | 2026-05-05 |
| MP29 | Agent Policy no BSA da Amazon: identificar-se como automação, parar quando pedirem; em vigor desde 2026-03-04 | PRÁTICA (resumo; texto oficial exige login) | https://ppc.land/amazons-new-ai-agent-rules-shake-up-sellers-before-march-4-deadline/ | 2026-02-22 |
| MP30 | Conditions of Use da Amazon: agente precisa se identificar sempre | PRÁTICA (rastreador) | https://conductatlas.com/platform/amazon/amazon-conditions-of-use/provision/CA-P-018576/agent-must-identify-itself-in-all-requests/ | captura 2026-09-14 |
| MP31 | Amazon processou a Perplexity (Comet) por agente não identificado | PRÁTICA (imprensa) | https://the-decoder.com/a-court-battle-over-perplexitys-comet-agent-could-define-how-ai-is-allowed-to-shop-online-for-users/ | 2025-11 |
| MP32 | Para Amazon: SP-API sim, automação de navegador não; aprovação humana em toda escrita; aprovação acima de 90% ou abaixo de 70% como régua | PRÁTICA | https://www.sellerlabs.com/knowledge-base/building-an-ai-agent-for-amazon-tasks-whats-possible-today/ | 2026-08-03 |
| MP33 | ToS do TikTok proíbe scripts automatizados de coleta e burlar limites de acesso | OFICIAL | https://www.tiktok.com/legal/page/row/terms-of-service/pt-BR | 2020-09 (pode estar superada) |
| MP34 | Claude in Chrome: classificadores de injeção; risco de ataque de cerca de 1% nos testes internos | OFICIAL | https://support.claude.com/en/articles/12902428 | s/d |
| MP35 | Checklist diário de gestor Amazon (saúde, preço, catálogo, casos, Buy Box, ritmo de Ads, ruptura, feedback) e gatilhos de escalada imediata | PRÁTICA | https://salesduo.com/blog/amazon-account-manager-daily-checklist | 2026-09-22 |
| MP36 | SOP: negativa com 20 ou mais cliques e 0 conversão; reposição em prazo + 14 dias; formato com versão e revisão a cada 90 dias | PRÁTICA | https://jarvio.io/blog/amazon-business-sops | 2026-02-25 |
| MP37 | Ciclo semanal e mensal de agência Amazon e KPIs do relatório | PRÁTICA | https://www.supplykick.com/blog/amazon-account-management-services | 2026-09-14 |
| MP38 | Verdi (ML): agente de suporte ao vendedor; mais da metade do suporte no Chile resolvido de forma autônoma | PRÁTICA (imprensa) | https://www.mobiletime.com.br/?p=836618 ; https://www.descubre.vc/noticia/mercado-libre-proyecta-un-futuro-de-compras-aut-nomas-con-ia-para-2026-2026-07-16 | 2026-07 |
| MP39 | Grupo OLX tem mais de 300 agentes de IA em operação | PRÁTICA (imprensa) | https://www.baguete.com.br/noticias/olx-investe-r-440-mi-com-foco-em-ia | 2026-05-18 |
| MP40 | Páginas da Shopee BR carregam SDK "anti_crawler" | OBS | https://shopee.com.br/docs/3612 | 2026-10-19 |

---

## (g) Lacunas

1. **A cláusula 12 do ML é nova?** A versão lida é de 15/10/2026. Não consegui a versão anterior (o Wayback devolveu uma página vazia), e não sei se o ML dá "autorização expressa" para agente de IA nem por qual canal. **Pergunta a fazer ao ML** (suporte ou developers): ler o próprio painel com assistente de IA no navegador é permitido?
2. **Texto oficial da Agent Policy da Amazon** exige login no Seller Central. Não li o texto, só resumos. Não sei como o agente deve "se identificar" num navegador, nem se a política vale para a Amazon.com.br (o BSA brasileiro é outro documento). Isso pode ser verificado pelo Chrome do Rafael, que tem login, numa sessão autorizada.
3. **Shopee:** não achei a cláusula dos termos sobre robôs ou ferramentas de terceiros (as páginas exigem JS).
4. **TikTok Shop:** não achei os termos do vendedor sobre ferramentas de terceiros e automação. Os ToS gerais são de 2020.
5. **Nenhum caso com números de agência brasileira** que opere ML ou Shopee com agentes de IA. Os casos BR são de plataforma (Verdi, OLX) ou de ferramenta (JoomPulse).
6. **Rotina de agência para ML, Shopee e TikTok** sem fonte primária comparável à da Amazon (SalesDuo, Jarvio, SupplyKick). Os itens BR da seção (d) são síntese.
7. **Caso documentado de agente que estourou gasto de Ads** numa plataforma de varejo: não achei. Os relatos de "laço caro" são de custo de API, contados por fornecedores.
8. **Números do Andon Market** vêm só de fontes secundárias e são contraditórios.
9. **Seller Assistant agêntico:** a Amazon não publicou como funciona a permissão (conceder, revogar, escopo).
10. O guia da OpenAI não traz data na capa. A data de 2025 vem do contexto do lançamento do Agents SDK (pode estar imprecisa).
