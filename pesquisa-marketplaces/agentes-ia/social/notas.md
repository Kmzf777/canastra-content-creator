# Agentes de IA que operam contas de marketplace: o que mostram no TikTok e no Instagram

Analista social. Data da análise: 2026-10-19. Pesquisa neutra sobre como as pessoas montam agentes que operam
Mercado Livre, Amazon, Shopee e TikTok Shop. Não traz recomendação para o Café Canastra.

## Como ler

- **Base.** 89 vídeos do TikTok (`tiktok.txt` → `tiktok.tsv`) e 44 posts do Instagram (`posts.txt` → `posts.tsv`).
  Os dois TSV têm as colunas `triagem` e `motivo`: 50 relevantes, 79 descartados pela legenda, 4 sem metadados.
- **Transcrições.** 27 em `transcricoes/<id>.txt`: 23 do TikTok e 4 do Instagram. Três não têm fala (só música ou tela):
  7666196697839734024, 7667754347379395860 e 7647767294214425869.
  Motor: **faster-whisper small** (CPU, int8, VAD), o mesmo modelo da rodada do TikTok Shop, que usou WhisperX small
  pela skill `watch`. Erros típicos de fala: "Cloud" = Claude, "Chopi/xopi" = Shopee, "SPAPI" = SP-API.
- **Corte de tempo.** O coordenador limitou a rodada. Ficaram **sem transcrição** 19 relevantes, que entram só pela
  legenda, marcados "(só legenda)". O vídeo de 35 min de @ratosdeia (time de agentes no Claude Code) foi pulado de
  propósito por ser longo. A lista está em (f).
- **Datas.** TikTok: decodificadas do id (os 32 bits altos são o timestamp). Instagram: `upload_date` do yt-dlp.
- **Views.** Só o TikTok entrega views sem login. No Instagram a coluna fica "—".
- **Como foi coletado.** yt-dlp como módulo Python, com `impersonate=chrome` (precisou instalar `curl_cffi` no
  site-packages do usuário: sem ele o TikTok devolve "Unexpected response" ou "ratelimit triggered"). Pausa de 4 s
  entre metadados e 6 s entre downloads. Scripts no scratchpad da sessão (`meta_tiktok.py`, `transcrever.py`,
  `aplicar_triagem.py`); Instagram com `ferramentas/meta_instagram.py`.
- **Tipos.** [PRÁTICA] o que o autor diz que faz · [CASE] resultado com número · [DADO] fato de mercado ou de
  plataforma (não conferido em fonte oficial nesta rodada) · [OPINIÃO] · [PROMESSA] o que vende sem mostrar.
- **"Demo real"** = a tela mostra o agente lendo ou mudando a conta de verdade. "Parcial" = tela do chat com dados,
  sem ver a conta. "Não" = fala ou propaganda.

---

## (a) Resumo em 10 linhas

1. Quase ninguém mostra "um agente por marketplace". O padrão real é **um assistente (Claude) com vários conectores**, um por canal, e o dono pedindo tarefas pontuais.
2. O acesso aos dados é por **conector/MCP sobre a API**, não por navegador: Hunter (SaaS) para ML/Shopee, extensão Shopee no Claude, app tiops, MCP de documentação do ML, SP-API da Amazon.
3. Ninguém na amostra mostra Claude in Chrome lendo o painel do vendedor. O único "abre o navegador e preenche o anúncio" é um post de ChatGPT agent (só legenda).
4. O melhor caso operacional é o de @fisgar.vendas: ERP próprio feito com Claude Code para ML, Shopee e Shein, com 4 CNPJs, precificação por canal, CLAUDE.md com "leis", revisor às cegas e **deploy só com autorização**.
5. A aprovação humana aparece em quase toda demo séria: responder pergunta só depois do "pode responder?" (Itamar), anúncio só com "aprovar" (Tom Teles), deploy só com "autorizado" (fisgar).
6. A exceção é perigosa: @lucas.ecom87 mandou, pelo conector da Shopee, mensagem promocional para os 369 compradores de dois dias, sem revisão. É a demo mais "autônoma" e a mais arriscada.
7. Rotina com gatilho aparece só lá fora: planilha observada que dispara criação de listing via SP-API, 1x por dia para poupar tokens; Claude agendado 2x por dia (10h e 22h) cruzando pedidos, e-mail e planilhas.
8. Números são poucos e do próprio autor: "5 a 6 horas viraram 5 minutos" (Hunter), "1 hora por dia por £20/mês" (UK), "5 horas viraram minutos" (Tom Teles).
9. Erros e riscos citados: loop de requisições derrubando a integração do ML, editar variação em massa e perder histórico; Amazon bloqueando agentes que não se identificam.
10. A maior parte vende algo: SaaS com teste grátis (Hunter), mentoria (Itamar), curso (Algoritmo Expert IA, Gestorecom, Rodrigo Garcia), template no direct ("comenta X"). O crítico @ruanmachado.sk chama "loja inteira sem intervenção humana" de papo de guru.

---

## (b) Tabela dos analisados

Legenda de país: BR, salvo indicação. "T" = transcrito, "L" = só legenda, "D-T" = descartado depois de transcrever.

| id | autor | data | views | país | o que mostra | demo real? | base |
|---|---|---|---|---|---|---|---|
| 7634743569223306516 | @itamarfrombrazil | 2026-05-01 | 11 000 | BR | Claude + skill/app tiops copia anúncio de catálogo do ML pelo link e publica na conta dele, perguntando preço, estoque e tipo | sim | T |
| 7637318212664757525 = DYC219kRxyX | @itamarfrombrazil / Itamar Santos | 2026-05-08 | 3 204 | BR | Claude no celular lista perguntas abertas no ML e na Shopee, sugere resposta, ele ajusta por áudio e aprova o envio | sim | T |
| 7665484979094244629 | @itamarfrombrazil | 2026-07-22 | 1 159 | BR | "IA nos marketplaces com Claude" | ? | L (403) |
| 7694407419677592840 | @hunterhub.br | 2026-10-08 | 465 | BR | conector personalizado do Hunter no Claude; lista concorrentes do catálogo com dados reais do ML | parcial | T |
| 7683644230685707541 | @hunterhub.br | 2026-09-09 | 1 780 | BR | prompt: curva ABC por lucro, vazamentos e 3 ações urgentes, via Hunter | parcial | T |
| 7656957465732467975 | @fisgar.vendas | 2026-06-29 | 1 352 | BR | ERP próprio feito com Claude Code (17 min): tela de criar anúncio, precificação por canal, revisor às cegas, deploy autorizado | sim | T |
| 7675073784562552085 | @diegorojas.seller | 2026-08-17 | 7 057 | BR | Claude Desktop "faz a gestão completa das promoções" no ML e Shopee | não | T |
| 7645553584024587540 | @marketfacil | 2026-05-30 | 520 | BR | automação Claude + n8n para anúncios novos no ML; riscos da API | não | T |
| 7662170893203803393 | @ruanmachado.sk | 2026-07-14 | 21 900 | BR | crítica a quem promete loja do ML tocada só por agentes | não (opinião) | T |
| Dc1Z-qUpAP9 | Tom Teles | 2026-09-03 | — | BR | tela dupla: agente cria anúncio no ML (título, ficha, descrição, preço, promoção, ads); dono só aprova | sim (editado) | T |
| DccPQL3tcHK | Henrique Niada | 2026-08-24 | — | BR | instala o MCP de documentação do ML como conector do Claude e consulta | sim | T |
| DatnN-ppohI | Eduardo Caparelli | 2026-07-13 | — | BR | "primeiro passo": usar o Claude Desktop/Cowork na operação de marketplace | não | T |
| 7692231684636396821 | @lucas.ecom87 | 2026-10-03 | 5 127 | BR | extensão da Shopee no Claude; mensagem de promoção para 369 pedidos | sim | T |
| 7696353016726818055 | @luanepinheirof | 2026-10-14 | 2 799 | BR | Amazon bloqueia agente de compras da Meta; protocolo de identificação de agentes | não (notícia) | T |
| 7688847592922336526 | @ai.labs.wire | 2026-09-23 | 129 | EN | Seller Assistant da Amazon com fluxos agênticos 24/7 (voz e imagem de IA) | não (notícia) | T |
| 7696978686809066755 | @stayingaheadofyou | 2026-10-15 | 231 | EN | SellerAmp → Google Sheet → agente cria listing via SP-API → marca a linha de verde | parcial | T |
| 7687295811037744416 | @chris.amzn | 2026-09-19 | 1 433 | UK | Claude agendado 2x/dia cruza SKU, pedidos do e-mail, buy sheet e prep sheet; Apps Script de OTP | parcial | T |
| 7697326780104838431 | @lukebasha | 2026-10-16 | 738 | EN | não deixa a IA escolher produto nem rodar ads; usa para P&D e análise de relatórios | não | T |
| 7524106125290114360 | @michael.ejm | 2025-07-06 | 2 368 | EN | ChatGPT para diferenciação, mockup, marca, fornecedor e listing | não | T |
| 7524763039619468557 | @rockitseller | 2025-07-08 | 1 671 | EN | n8n + GPT classifica keywords do relatório de PPC em 4 baldes | parcial | T |
| 7631787081139817746 | @ratosdeia | 2026-04-23 | 8 505 | BR | Shopify AI Toolkit: loja gerida pelo Claude Code, Codex, Cursor | não (notícia) | T |
| 7666196697839734024 | @alexmorooficial | 2026-07-24 | 424 | BR | 10 agentes prontos para ML (ChatGPT, Gemini, Claude) no curso Algoritmo Expert IA 3.0 | não | L (sem fala) |
| 7667754347379395860 | @salvianogabrieel | 2026-07-29 | 1 588 | BR | pesquisa de mercado no ML com Claude Code (tela com música) | ? | L (sem fala) |
| 7629003020214209822 | @robscalesfba | 2026-04-15 | 2 739 | EN | ChatGPT e Claude em FBA private label | ? | L (403) |
| 7641380554956442911 | @carter.braydon | 2026-05-18 | 169 900 | EN | "Claude lançou um agente de pequeno negócio no app desktop" | ? | L (403) |
| 7660571492547087636 | @restructureai | 2026-07-09 | 120 600 | EN | sistema de agentes Claude para loja de e-commerce | ? | L (403) |
| 7557110998960868626 | @michael.ejm | 2025-10-03 | 863 | EN | como usar IA no FBA | ? | L |
| 7620066826218687762 | @ratosdeia | 2026-03-22 | 101 700 | BR | time de agentes no Claude Code, passo a passo (35 min, marketing) | ? | L |
| 7621687561907375380 | @biel_seller | 2026-03-26 | 28 500 | BR | lançamento "Seller Lab" com IA | ? | L |
| 7676235218491034888 | @brunocapellete | 2026-08-20 | 270 | BR | ganhar tempo na gestão de marketplaces com IA | ? | L |
| 7655809839712619796 | @david.do.marketpl | 2026-06-26 | 154 | BR | IA para descrição, título, resposta a cliente; "a estratégia continua humana" | não | L |
| 7661671055731264786 | @jean_gestorecom | 2026-07-12 | 301 | BR | módulo de IA no treinamento da Gestorecom | não | L |
| 7651759303459638549 | @prado.ai | 2026-06-15 | 156 900 | BR | legenda vazia | ? | L |
| 7677571436566809876 | @aurenconsultoria | 2026-08-24 | 97 | BR | escolher tarefa repetitiva e fácil de conferir; preço só com estratégia definida | não | L |
| DXXGDT5Aod- | Westack | 2026-04-20 | — | BR | "1ª IA que opera de ponta a ponta seu marketplace", inclusive pedido ao fornecedor | não | L |
| DcoO0I2RLT9 | Lucas Schwichtemberg | 2026-08-29 | — | BR | agente "em teste" para retirar reclamações que afetam a reputação no ML | ? | L |
| DPmi1vCEozz | Chatvolt | 2025-10-09 | — | BR | agente responde perguntas, DMs de pós-venda e recomenda produto no ML | ? | L |
| DbdiUNARG0S | Gabriel Bollico | 2026-07-31 | — | BR | IA de otimização no Mercado Ads | não | L |
| DctV0TCCDo4 | Alex Moro | 2026-08-31 | — | BR | engenharia reversa dos anúncios que mais vendem + IA para recriar | ? | L |
| DZFFHCWnCLp / DYuDxJ3HDnu | Rodrigo Garcia | 2026-06-02 / 05-24 | — | BR | curso: IA para anúncios, indicadores, preço e "automação de API" no ML | não | L |
| Dd9wMyhvUrW | Bruno Maciel | 2026-10-01 | — | BR | recurso do próprio ML para anúncios | ? | L |
| DZB7xCOu7aT | Breno Cunha | 2026-06-01 | — | BR | "um dos projetos mais absurdos" (Marketplace & IA) | ? | L |
| DXJmMzZirGQ | Roy Alfred | 2026-04-15 | — | BR | ChatGPT abre o navegador, pesquisa preço e preenche o anúncio | ? | L |
| 7674392800653249810 | @central_premium1 | 2026-08-15 | 47 200 | BR | afiliado ML + MCP do Higgsfield para vídeo de influencer IA | — | D-T |
| 7613526194658512146 / 7524033298394320134 | @gabmirandamkt | 2026-03-04 / 2025-07-06 | 3 107 / 29 600 | BR | cobrança de agência de automação; prospecção no Google Maps | — | D-T |
| 7696247356919975186 | @victor_orsolin | 2026-10-13 | 798 | BR | afiliado com texto do ChatGPT em grupos | — | D-T |
| 7647767294214425869 | @eric.ai.builder | 2026-06-05 | 823 | EN | sem fala, afiliado TikTok Shop | — | D-T |

Os 79 descartes pela legenda e o motivo de cada um estão nas colunas `triagem`/`motivo` de `tiktok.tsv` e `posts.tsv`.
Os mais comuns: afiliado ou criador de conteúdo com IA (TikTok Shop e Shopee, 17), Claude Code ou n8n genérico sem
marketplace (19), lado do comprador (agentes de compra, cupom, Rufus: 6), prospecção e WhatsApp (8), imagem ou vídeo
de anúncio sem operar a conta (5), renda extra (4).

---

## (c) Seções por tema

### 1. Arquitetura: um agente por canal ou por função?

- **Ninguém mostra um agente por marketplace.** O que se vê é **um assistente central (Claude Desktop, celular ou Code) com um conector por canal**. Itamar consulta ML e Shopee na mesma conversa (7637318212664757525, 00:00-00:36). [PRÁTICA]
- **Por função aparece no vocabulário de quem vende.** "10 agentes" para criar anúncio, analisar concorrente, achar oportunidade (7666196697839734024, só legenda). O vídeo que @ruanmachado.sk critica descreve "um gestor de IA que distribui funções": um cria imagem, outro sobe anúncio, outro ajusta preço (7662170893203803393, 00:11-00:34). [PROMESSA]
- **Separação executor x revisor é a única arquitetura multiagente demonstrada.** @fisgar.vendas usa um agente que executa e outro, "revisor às cegas", que não viu o plano e só olha o resultado; ele aprova ou barra a entrega (7656957465732467975, 09:20-10:15). [PRÁTICA]
- **Continuidade entre sessões por documento.** O mesmo autor mantém um "doc de continuidade"/handoff e abre cada sessão com um "gatilho" ("continue a UI-A1 da unificação do criar anúncio") para o Claude achar o arquivo e retomar (04:50-06:28). [PRÁTICA]
- **Fora do Brasil o desenho é por tarefa, não por canal:** um agente que só cria listing a partir da planilha (7696978686809066755), um job agendado que só concilia pedidos (7687295811037744416), um workflow que só classifica keywords de PPC (7524763039619468557). [PRÁTICA]

### 2. Acesso aos dados

- **API por conector/MCP é o padrão.** Hunter (SaaS que já tem a API do ML e da Shopee) vira "conector personalizado" no Claude colando uma URL (7694407419677592840, 00:05-00:23). Extensão da Shopee no Claude, com tela de permissão (7692231684636396821, 00:46-00:58). App tiops para ML e Shopee (7634743569223306516, legenda). [PRÁTICA]
- **MCP de documentação além do MCP de dados.** Henrique Niada: "conectar a API te conecta aos dados; conectar a documentação ensina a IA a encontrar os dados". Ele diz que é um MCP "que o Mercado Livre mesmo fornece" (DccPQL3tcHK, 00:40-01:46). Não conferido em fonte oficial nesta rodada. [PRÁTICA/DADO]
- **API direta dentro de sistema próprio.** O ERP de @fisgar.vendas puxa categoria e ficha técnica "direto da API do Mercado Livre" e busca termos mais buscados e concorrentes para gerar título (7656957465732467975, 12:43-14:55). [PRÁTICA]
- **Planilha como fila.** Google Sheet com ASIN, custo, quantidade, perigosos, condição e SKU; o agente acorda quando entra linha nova e grava o resultado de volta (7696978686809066755, 00:15-00:44). Buy sheet e prep sheet no caso UK (7687295811037744416). [PRÁTICA]
- **E-mail como fonte.** Claude preenche números de pedido a partir do e-mail; um Apps Script lê códigos OTP e envia ao prep center (7687295811037744416, 00:26-01:22). [PRÁTICA]
- **Navegador: quase ausente.** Só Roy Alfred diz que o ChatGPT "abre o navegador, pesquisa o preço e preenche o anúncio" (DXJmMzZirGQ, só legenda). Nenhum vídeo mostra Claude in Chrome no painel do vendedor.
- **Plataformas começam a barrar agente não identificado.** A Amazon bloqueou o agente de compras da Meta 12 dias após o lançamento, alegando que ele não avisou, não se identificava como agente e parecia guardar login. Em 06/10/2026 teria saído um "Personal Agent Protocol" com Walmart, Shopify e Stripe (7696353016726818055, 00:45-02:09). É lado comprador, mas é o sinal mais claro de como os marketplaces tratam automação por navegador. [DADO, não conferido]

### 3. Stack

- **Claude domina a amostra brasileira de 2026.** Claude Desktop e Cowork (DatnN-ppohI; 7675073784562552085), Claude no celular (7637318212664757525), Claude Code para construir sistema (7656957465732467975), conectores personalizados (Hunter, Shopee, MCP do ML).
- **"Use o Desktop, não o navegador"** é o primeiro conselho de quem opera: a versão desktop "dá autonomia para acessar sua máquina e executar tarefas", ler arquivos, mandar WhatsApp (DatnN-ppohI, 00:17-01:13). [OPINIÃO]
- **n8n aparece como cola de automação**, com Claude ou GPT dentro: anúncios novos no ML (7645553584024587540) e PPC na Amazon (7524763039619468557). Fora disso, n8n na amostra é quase sempre agência genérica (descartados).
- **Ferramentas de terceiros por cima:** Hunter (ML/Shopee), tiops (ML/Shopee), SellerAmp, ProfitPath (Amazon), Data Dive AI (Amazon), Chatvolt (atendimento ML), Westack (promete operação completa).
- **Plataformas oferecendo o próprio agente:** Seller Assistant da Amazon com fluxos agênticos, "plugado no Amazon Quick e no Claude" (7688847592922336526); IA de otimização no Mercado Ads (DbdiUNARG0S); Shopify AI Toolkit para Claude Code, Codex e Cursor (7631787081139817746). [DADO]

### 4. Rotina e gatilhos

- **Agendado:** 2x por dia, 10h e 22h, para pegar compras feitas cedo ou tarde (7687295811037744416, 00:43-00:51). [PRÁTICA]
- **Por evento:** linha nova na planilha acorda o agente; o autor recomenda revisar só 1x por dia "para não queimar tokens" (7696978686809066755, 00:22-00:56). [PRÁTICA]
- **Atraso proposital:** a fila de criação de listing do ProfitPath tem 24 h de espera, tempo para o Claude conferir o SKU com a buy sheet (7687295811037744416, 00:12-00:30). [PRÁTICA]
- **Sob demanda é o padrão no Brasil:** o dono pergunta ("quais perguntas estão abertas hoje?", "liste meus concorrentes", "envie promoção a quem comprou ontem"). Itamar diz que "poderia deixar numa memória do Claude" para olhar e responder todo dia, mas não faz (7637318212664757525, 01:16-01:25). [PRÁTICA]

### 5. O que faz sozinho e o que pede aprovação

- **Pede aprovação antes de escrever na conta:**
  - resposta a pergunta: o Claude formata e pergunta se pode responder (7637318212664757525, 01:08-01:16);
  - anúncio completo: "o que eu preciso fazer é somente aprovar" (Dc1Z-qUpAP9, 00:17-00:22);
  - deploy do sistema: "pela regra não subo sem sua autorização" (7656957465732467975, 10:15-10:33).
- **Pergunta o que falta, em vez de chutar:** para copiar o anúncio, o Claude pediu preço, estoque, tipo de anúncio e condição (7634743569223306516, 00:52-01:12).
- **Regras escritas que o agente não pode violar:** "leis" no CLAUDE.md, entre elas "não confia, confere" e "nada de achismo, só evidência" (7656957465732467975, 08:00-09:17). O agente achou sozinho uma "armadilha": subir os arquivos como estavam reverteria produção por causa de outro projeto commitado e não publicado (07:31-08:25). [PRÁTICA]
- **Regra de privacidade no prompt:** não mostrar os produtos na resposta (7683644230685707541, 00:17). [PRÁTICA]
- **Faz sozinho, sem revisão:** disparo de mensagem promocional para 369 compradores da Shopee (7692231684636396821, 00:58-01:35). E o Seller Assistant da Amazon "vigia estoque, preço e avaliações enquanto você dorme", "com guardrails que você define" (7688847592922336526).
- **Quem não delega:** @lukebasha não deixa a IA escolher produto, rodar ads nem "operar o negócio"; usa para ideias e análise (7697326780104838431, 00:04-00:43). @aurenconsultoria: comece por tarefa repetitiva com resultado fácil de conferir; mexer em preço exige estratégia definida antes (só legenda). [OPINIÃO]

### 6. Resultados e números

Todos são do próprio autor e sem prova independente.
- Análise de "5, 6 horas" respondida "em 5 minutos" (7683644230685707541, 00:28). [CASE, do vendedor da ferramenta]
- "Um trabalho de 5 horas no mínimo ele fez em minutos" (Dc1Z-qUpAP9, 00:24). [CASE, sem número de vendas na fala]
- "Provavelmente 1 hora por dia" economizada, custo de £20/mês do Claude (7687295811037744416, 00:57-01:07). [CASE]
- 369 pedidos receberam mensagem; "várias já responderam" (7692231684636396821, 01:05-01:35). [CASE]
- ERP em produção desde 22/06/2026, vendendo em Shein, Shopee e ML com 4 CNPJs, sem programador (7656957465732467975, 00:13-00:45; 13:59). [CASE]
- Mais de 90% dos vendedores da Amazon já têm o Seller Assistant (7688847592922336526, 00:09). [DADO, não conferido]

### 7. Erros e riscos citados

- **Loop de requisições** que trava a integração com o ML, e **mudar campo de variação em massa** e perder histórico. "Testa exaustivamente antes de deixar rodando no automático" (7645553584024587540, 00:11-00:43). [PRÁTICA]
- Detalhes que o ML "deixa só numa linha da documentação" (mesmo vídeo, 00:26-00:33); daí o MCP de documentação de DccPQL3tcHK.
- Sessão longa "fica bugada": o autor abre sessão nova e passa o contexto por documento (7656957465732467975, 04:22-04:31).
- Conflito de deploy evitado pelo próprio agente (mesmo vídeo, 07:43-08:25).
- Configurar o conector da Shopee levou 12 horas a quem não é técnico (7692231684636396821, 00:26-00:36).
- Bloqueio da plataforma a agentes não identificados (7696353016726818055).
- "IA de nada serve se não tem uma operação organizada antes", com ERP (Bling, Tiny) arrumado (7662170893203803393, 00:43-00:51). [OPINIÃO]

### 8. O que vendem

- **SaaS com teste grátis:** Hunter (7 dias), Westack, Chatvolt, Marketfacil, tiops (app de Itamar).
- **Mentoria:** Itamar, com atendimento por uma IA chamada "Sofia" no WhatsApp (7637318212664757525, 01:30).
- **Curso:** Algoritmo Expert IA 3.0 (Alex Moro), Gestorecom (Jean), Rodrigo Garcia (anúncio pago), módulos para alunos (@lukebasha, @michael.ejm).
- **Funil "comenta X que eu mando no direct":** Tom Teles ("GESTOR"), Diego Rojas ("CLOUD"), Niada ("MCP"), Lucas Schwichtemberg ("AGENTE"), rockitseller ("VAULT"), stayingaheadofyou ("agent").
- **Não vendem nada visível:** @fisgar.vendas (só seguidores), @lucas.ecom87, @chris.amzn.

### 9. Quem mostra funcionando e quem só promete

- **Mostra (demo real):** fisgar.vendas (ERP), Itamar (copiar anúncio; responder perguntas), Niada (MCP), lucas.ecom87 (Shopee), Tom Teles (editado em tela dupla).
- **Mostra parcial (chat com dados, sem a conta):** hunterhub.br, stayingaheadofyou, chris.amzn, rockitseller.
- **Só promete:** Westack ("opera de ponta a ponta, faz pedido ao fornecedor"), Diego Rojas ("trabalha até quando tu tá dormindo"), Alex Moro ("10 agentes"), Rodrigo Garcia, Chatvolt, o vídeo criticado por @ruanmachado.sk.

---

## (d) Tabela de afirmações

| # | afirmação | tipo | fonte | minuto |
|---|---|---|---|---|
| 1 | Claude copiou anúncio de catálogo do ML pelo link e publicou na conta, perguntando preço, estoque e tipo | [PRÁTICA] | 7634743569223306516 | 00:52-01:52 |
| 2 | O Claude no celular lista as perguntas abertas do ML e da Shopee e sugere resposta | [PRÁTICA] | 7637318212664757525 | 00:12-00:31 |
| 3 | Antes de responder, o Claude pergunta se já pode enviar | [PRÁTICA] | 7637318212664757525 | 01:08-01:16 |
| 4 | Dá para deixar numa memória para responder todo dia com base em título e descrição | [OPINIÃO] | 7637318212664757525 | 01:16-01:25 |
| 5 | Conector personalizado do Hunter dá ao Claude dados reais da loja do ML | [PRÁTICA] | 7694407419677592840 | 00:05-00:38 |
| 6 | Prompt de curva ABC por lucro, vazamentos e 3 ações urgentes; 5-6 h viram 5 min | [CASE] | 7683644230685707541 | 00:14-00:28 |
| 7 | ERP próprio com Claude Code em produção desde 22/06/2026, sem saber programar | [CASE] | 7656957465732467975 | 00:13-00:24 |
| 8 | Precificação por canal: ML 14% + taxa fixa R$ 5,65; Shopee 20% + R$ 4 por pedido; imposto por CNPJ | [DADO] | 7656957465732467975 | 13:22-14:12 |
| 9 | Doc de continuidade e "gatilho" para retomar a tarefa em sessão nova | [PRÁTICA] | 7656957465732467975 | 04:50-05:32 |
| 10 | "Leis" no CLAUDE.md: não confia, confere; nada de achismo | [PRÁTICA] | 7656957465732467975 | 08:00-09:17 |
| 11 | Revisor às cegas: segundo agente que não viu o plano aprova ou barra | [PRÁTICA] | 7656957465732467975 | 09:20-10:15 |
| 12 | Deploy só com autorização explícita | [PRÁTICA] | 7656957465732467975 | 10:15-10:33 |
| 13 | Risco de loop de requisições e de editar variação em massa via API do ML | [PRÁTICA] | 7645553584024587540 | 00:11-00:43 |
| 14 | O ML fornece um MCP com a documentação da API | [DADO] | DccPQL3tcHK | 00:40-00:44 |
| 15 | API conecta aos dados; a documentação ensina a IA a achar os dados | [OPINIÃO] | DccPQL3tcHK | 01:36-01:46 |
| 16 | Agente cria anúncio completo no ML, com promoção e ads; dono só aprova | [PRÁTICA] | Dc1Z-qUpAP9 | 00:10-00:22 |
| 17 | Mensagem promocional enviada a 369 compradores pela extensão da Shopee no Claude | [CASE] | 7692231684636396821 | 00:58-01:35 |
| 18 | Claude Desktop faz a gestão completa das promoções, "com você assistindo ou não" | [PROMESSA] | 7675073784562552085 | 00:02-00:10 |
| 19 | Usar a versão Desktop/Cowork, que tem acesso à máquina | [OPINIÃO] | DatnN-ppohI | 00:17-00:52 |
| 20 | Planilha nova → agente cria listing via SP-API → marca a linha; revisar 1x/dia para poupar tokens | [PRÁTICA] | 7696978686809066755 | 00:22-00:56 |
| 21 | Claude agendado 10h e 22h concilia pedidos, e-mail e planilhas; ~1 h/dia por £20/mês | [CASE] | 7687295811037744416 | 00:43-01:07 |
| 22 | Fila de listing com atraso de 24 h para o Claude conferir o SKU | [PRÁTICA] | 7687295811037744416 | 00:12-00:30 |
| 23 | Não deixa a IA escolher produto, rodar ads ou operar a conta | [OPINIÃO] | 7697326780104838431 | 00:04-00:12 |
| 24 | Workflow GPT classifica keywords de PPC em smart target, hidden gem, bleeder, cleanup | [PRÁTICA] | 7524763039619468557 | 00:00-00:14 |
| 25 | Seller Assistant da Amazon com fluxos 24/7; >90% dos vendedores têm; integra com Claude | [DADO] | 7688847592922336526 | 00:00-00:17 |
| 26 | Shopify AI Toolkit deixa o Claude Code editar produto, desconto e páginas | [DADO] | 7631787081139817746 | 00:08-00:32 |
| 27 | Amazon bloqueou agente da Meta por não se identificar; protocolo de agentes em 06/10/2026 | [DADO] | 7696353016726818055 | 00:59-02:09 |
| 28 | "Loja sem intervenção humana" é papo de guru; IA elimina o repetitivo, não a gestão | [OPINIÃO] | 7662170893203803393 | 00:19-00:43 |
| 29 | IA opera o marketplace de ponta a ponta e faz pedido ao fornecedor | [PROMESSA] | DXXGDT5Aod- | só legenda |
| 30 | Comece por tarefa repetitiva e fácil de conferir; preço só com estratégia definida | [OPINIÃO] | 7677571436566809876 | só legenda |

---

## (e) Criadores e ferramentas que aparecem mais de uma vez

**Criadores**
- **Itamar Santos** (@itamarfrombrazil): 3 TikToks + 1 reel (o reel repete o TikTok 7637318212664757525). Claude + ML/Shopee; vende mentoria e o app tiops.
- **@hunterhub.br**: 2. Conector do Hunter no Claude; SaaS.
- **Diego Rojas** (@diegorojas.seller): 1 TikTok + 2 reels. Claude Desktop para promoções; os reels (imagem e vídeo de anúncio com IA) foram descartados.
- **Alex Moro**: 1 TikTok + 1 reel. Curso com "10 agentes"; engenharia reversa de anúncios.
- **Rodrigo Garcia**: 2 posts (anúncio de curso e carrossel). Só legenda.
- **@michael.ejm**: 2 (Amazon FBA + ChatGPT).
- **@ratosdeia**: 2 (Shopify AI Toolkit; time de agentes no Claude Code).
- Recorrentes mas fora do tema: @gabmirandamkt (7, agência n8n), @fabianocarvalhojr (4 + 1 reel, Claude Code genérico), @gabrieladamuchi (4, ferramentas de IA), Gabriel Fialho (2, MailerFind), Castilho (2), @igao.ia (2, afiliado), @canalsegredosdodigital (2).

**Ferramentas**
- **Claude** (Desktop, Cowork, celular, Code, conectores personalizados): ferramenta central em 14 dos analisados.
- **Conector/MCP**: Hunter, extensão Shopee, MCP de documentação do ML, tiops, Higgsfield (descartado), Amazon Quick.
- **n8n**: 2 relevantes (ML e PPC Amazon) e vários genéricos descartados.
- **Google Sheets / planilha como fila**: 2 (Amazon).
- **API oficial**: API do Mercado Livre (3), SP-API da Amazon (1).
- **ChatGPT**: 4 (mockup, listing, PPC, preencher anúncio pelo navegador).
- **Agentes da própria plataforma**: Seller Assistant (Amazon), IA do Mercado Ads, Shopify AI Toolkit.

---

## (f) Falhas e lacunas

Detalhe técnico em `transcricoes/_falhas.txt`.

**Falharam no download (HTTP 403 do TikTok, mesmo com impersonate):**
7629003020214209822 (@robscalesfba), 7641380554956442911 (@carter.braydon), 7660571492547087636 (@restructureai),
7665484979094244629 (@itamarfrombrazil).

**Sem metadados:** 7638748995229076756 (@gabrieladamuchi); DTTTrHbAXC8 e DYmtoVoj50g (prováveis posts só de imagem);
DWeHxd9gFs8 (o Instagram pede login).

**Sem fala (transcrição vazia):** 7666196697839734024, 7667754347379395860, 7647767294214425869.

**Relevantes não transcritos por corte de tempo** (entram só pela legenda): 7557110998960868626,
7620066826218687762 (35 min), 7621687561907375380, 7676235218491034888, 7655809839712619796, 7661671055731264786,
7651759303459638549, 7677571436566809876, DXXGDT5Aod-, DcoO0I2RLT9, DPmi1vCEozz, DZB7xCOu7aT, Dd9wMyhvUrW,
DZFFHCWnCLp, DbdiUNARG0S, DctV0TCCDo4, DXJmMzZirGQ, DYuDxJ3HDnu (carrossel, sem áudio). DYC219kRxyX não foi
transcrito porque repete o TikTok 7637318212664757525.

**Bloqueio no início:** a primeira passada de metadados do TikTok falhou inteira ("Unexpected response",
"ratelimit triggered"). Resolveu com `curl_cffi` + `impersonate=chrome`. Nenhum login nem captcha foi pedido.
