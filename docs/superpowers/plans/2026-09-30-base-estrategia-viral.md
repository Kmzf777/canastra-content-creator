# Base de estratégia de conteúdo viral — Plano de implementação

> **Para trabalhadores agênticos:** SUB-SKILL OBRIGATÓRIA: use `superpowers:subagent-driven-development` (recomendado) ou `superpowers:executing-plans` para implementar tarefa a tarefa. Os passos usam caixa (`- [ ]`) para acompanhamento.

**Objetivo:** construir em `instagram/estrategia/` a base escrita que decide *o que* gravar, com viés deliberado em marcas de produto físico fora do café, e que o motor de vídeo consome como briefing.

**Arquitetura:** oito documentos, cada um com uma função. A disciplina que atravessa todos: **separar sinal oficial de inferência de criador, e marcar pseudociência como pseudociência.** Uma base que repete "dopamina" como mecanismo causal não é base, é folclore.

**Entregável:** arquivos `.md`. Não há código. A verificação é de conteúdo: toda afirmação numérica tem fonte nomeada, e toda afirmação sem fonte está marcada como tal.

---

## A pesquisa já está feita

Este plano **não pede nova pesquisa**. Foram 4 agentes, ~36 transcrições de YouTube baixadas e limpas, 11 perfis de Instagram lidos no DOM, e a mineração de um motor open source. Os fatos abaixo são o insumo; as tarefas são de redação.

### Sinais de ranking — oficial

Da série do próprio Instagram/Mosseri, e de entrevista dele à Semafor:

- Os **três sinais mais importantes**, tanto para alcance em seguidores quanto em recomendação: **tempo médio assistido** (o principal nos dois), **curtidas por alcance** (pesa mais no conectado), **envios por alcance** (pesa mais no não-conectado).
- Mosseri, textualmente: *"sends são uma parte enorme do sucesso dos Reels"*.
- **Ranking por exploração:** conteúdo novo recebe ~100 impressões; performando acima do esperado, gradua para 1.000, depois 10.000. É assim que conta pequena estoura.
- Elegibilidade para não-seguidores: sem marca d'água, com áudio, ≤3 minutos, substancialmente original, conta em bom status.
- A grade do perfil virou vertical porque a maioria dos uploads já é vertical.

### Inferência de criador — útil, não oficial

- Rosto humano visível nos primeiros 3 s por ≥1 s → +10% retenção; vídeo com voz → engajamento 5,6% maior que só-música; falar aumenta o tempo assistido em ~25%. *(Build Your Tribe, citando estudo do Social Media Today com ~10 mil reels — fonte terciária, o estudo original não foi verificado.)*
- Engajamento mediano: **carrossel 6,9% · foto única 4,4% · reels 3,3%**. Reels têm 36% mais alcance; carrosséis, 12% mais engajamento. *(análise do próprio canal, sem estudo nomeado.)*
- Gancho tem em média 7,7 palavras; faixa boa 5–8.
- Velocidade de curtidas nas primeiras 24 h como sinal do Explore *(Jade Beason — sem confirmação oficial.)*

### Gancho

- Três camadas: **visual** (o que se vê no frame 1), **textual** (o que está escrito na tela), **verbal** (o que se fala). Regra prática: **o texto não repete a fala** — funcionam como manchete e legenda, se complementam.
- Fórmula de 6 elementos *(Kallaway)*: Sujeito + Ação + Resultado + Contraste + [Prova] + [Tempo].
- O gancho é uma **resposta de orientação**: responde "do que se trata" e "o que eu ganho continuando".
- **Teste da imagem parada:** um frame a 0,5 s tem que fazer sentido sozinho.
- Zona do meio: revelar pouco demais confunde, revelar demais mata a curiosidade.

### Estrutura de roteiro

- Esqueleto AIDA adaptado *(Sandy Moraes, 218 mil inscritos)*: **Gancho → Promessa → Outro lado → Virada → Entrega.** Uma ideia boa vira gancho fraco se não soar como promessa: *"3 perguntas boas de entrevista"* perde para *"3 perguntas para você ser aprovado"*.
- Três estruturas válidas, escolhidas pelo tipo de valor e não por reflexo de suspense: **resposta primeiro** (tutorial), **prévia da resposta** (mantém curiosidade sem frustrar), **stakes primeiro** (história).

### Relógio comportamental

Defaults operacionais, não leis. Vindos do harness `corte-viral`:

| Evento | Resposta rápida | Contradição | História |
|---|---:|---:|---:|
| Orientação | 0–1,5 s | 0–1,5 s | 0–2,0 s |
| Proposta | até 2,5 s | até 2,5 s | stakes até 5,0 s |
| Primeiro valor | até 6,0 s | razão até 8,0 s | virada até 12 s |
| Novo beat | 3–7 s | 3–7 s | 5–10 s |
| Duração típica | 15–45 s | 20–60 s | 35–90 s |

### Arquétipos de conteúdo de marca de produto

Origem/procedência · herança e ofício · ritual de uso · ranking honesto · breakdown que ensina tudo · cenário hipotético · jornada do fundador · objeção derrubada.

### O que as marcas virais fora do café realmente fazem

- **@getgraza** (222 mil): legenda-meme sobre foto simples do produto no cotidiano; produto sempre herói, estética de celular, tom irônico. **A origem agrícola quase não aparece** — a prova de autenticidade vem do bastidor da empresa, não da fazenda.
- **@flybyjing** (143 mil): **cápsulas com parceiro local por tempo limitado**, anunciadas nos dois perfis. É a resposta mais direta ao problema "como ter frequência sem virar institucional".
- **@omsom** (74,9 mil): reposta piada relatable **sem o produto aparecer**, só para reforçar identidade. Custo de produção zero.
- **@drinkpoppi** (706 mil): flat-lay de lista relatable, produto pequeno entre objetos de estilo de vida.
- **@chamberlaincoffee** (541 mil): preparo em câmera lenta com legenda emocional curta.
- **@liquiddeath** (7,2 mi): comédia roteirizada com ator. **Não transfere** — fracassou no Reino Unido porque o humor não atravessa, e é bancado por US$ 195 milhões levantados.
- **Stanley**: a comunidade vendeu pela marca; receita de US$ 74 mi (2019) para US$ 750 mi (2023). Mas é empresa de **110 anos** — a "viralização da noite para o dia" levou décadas de consistência.

### Cadência

Receita testada: escolher **2–3 combinações de tipo × formato**, postar **2× por semana cada**, e **só avaliar depois de 30 dias**. O erro comum é repetir o *tema* ("somos uma fazenda de família") em vez de repetir o *formato*.

### Pseudociência a marcar como tal

- **"Dopamina"** aparece repetidamente como explicação causal para curiosidade e retenção, **sem um único estudo citado**. Não existe regra do tipo "um corte a cada dois segundos libera dopamina".
- **"O cérebro processa imagem 60.000× mais rápido que texto"** é número de marketing sem fonte rastreável. O reconhecimento em ~13 ms tem base real (MIT, 2014); o multiplicador não.
- "PCR", "trust score", "hook layering", "freezing point" são frameworks autorais de criador, não terminologia do Instagram.

### Contradições a registrar, não resolver

1. **Frequência:** uma fonte diz que postar em sequência suprime alcance; mas o recurso oficial "Trial Reels" existe justamente para postar mais sem esse risco.
2. **Peso de envios:** a fonte oficial trata como sinal distinto e decisivo no alcance não-conectado; criadores generalizam tudo em "taxa de engajamento".
3. **Loop:** nenhuma fonte da amostra explicou com dado por que o loop pesaria no ranking.
4. **"Estudei 1.000 ganchos"** é, ele próprio, uma técnica de gancho — o que deveria aumentar o ceticismo com títulos assim.

---

## Estrutura de arquivos

```
instagram/estrategia/
  LEIA-ME.md               índice, e como esta base é usada
  01-ranking.md            sinais oficiais vs inferência
  02-ganchos.md            taxonomia e fórmulas
  03-roteiro.md            estruturas e relógio comportamental
  04-arquetipos.md         moldes de marca de produto, com os casos fora do café
  05-formatos.md           o catálogo Canastra, com matéria-prima exigida
  06-cadencia.md           calendário, séries nomeadas, metas
  07-nao-fazer.md          pseudociência, o que não transfere, contradições
  08-fontes.md             de onde veio cada afirmação
```

---

### Tarefa 1: O índice e a regra de sourcing

**Arquivos:**
- Criar: `instagram/estrategia/LEIA-ME.md`, `instagram/estrategia/08-fontes.md`

- [ ] **Passo 1: Escrever o `LEIA-ME.md`**

Deve conter: para que serve a base, a tabela dos 8 arquivos, e — o mais importante — **a convenção de marcação** que todos os outros arquivos seguem:

```markdown
## Como ler esta base

Toda afirmação carrega sua origem:

| Marca | Significa |
|---|---|
| **[oficial]** | o Instagram ou o Mosseri disse, publicamente |
| **[medido]** | número que nós mesmos medimos, no pixel ou no arquivo |
| **[criador]** | inferência de quem testa, sem confirmação da plataforma |
| **[terciário]** | alguém citou um estudo que não verificamos |
| **[folclore]** | circula como verdade e não tem base — está aqui para ser reconhecido e recusado |

Afirmação sem marca é erro de redação. Corrija em vez de confiar.
```

- [ ] **Passo 2: Escrever `08-fontes.md`**

Uma linha por fonte: canal ou conta, tamanho, o que foi usado dela, e a marca de confiabilidade. Inclua as transcrições baixadas nesta sessão e os perfis lidos. **Não invente URL** — se não anotou, escreva o nome e diga que a URL não foi registrada.

- [ ] **Passo 3: Verificar**

Abra os dois e confirme que a tabela de marcação está lá e que nenhuma afirmação do `LEIA-ME` está sem marca.

- [ ] **Passo 4: Commit**

```bash
git add instagram/estrategia/LEIA-ME.md instagram/estrategia/08-fontes.md
git commit -m "docs(estrategia): indice e convencao de sourcing"
```

---

### Tarefa 2: Ranking

**Arquivos:**
- Criar: `instagram/estrategia/01-ranking.md`

- [ ] **Passo 1: Escrever**

Conteúdo obrigatório, tudo já levantado e listado na seção "A pesquisa já está feita" deste plano: os três sinais oficiais, a citação do Mosseri sobre envios, o **ranking por exploração** (~100 → 1.000 → 10.000), os critérios de elegibilidade para não-seguidores, e as inferências de criador **separadas em seção própria**.

Feche com a leitura para a Canastra, que é o ponto:

> A conta tem 10,3 mil seguidores e engajamento de 0,50% — saudável, acima do Coffee++ com 269 mil. O gargalo não é a audiência, é a frequência: a 1 post a cada 42 dias, a marca compra pouquíssimos bilhetes na loteria de exploração. **[medido]**

- [ ] **Passo 2: Verificar**

Confirme que cada afirmação tem marca, e que nenhuma inferência de criador está redigida como se fosse oficial.

- [ ] **Passo 3: Commit**

```bash
git add instagram/estrategia/01-ranking.md
git commit -m "docs(estrategia): sinais de ranking, oficial separado de inferencia"
```

---

### Tarefa 3: Ganchos

**Arquivos:**
- Criar: `instagram/estrategia/02-ganchos.md`

- [ ] **Passo 1: Escrever**

As três camadas (visual, textual, verbal) com a regra de que **o texto não repete a fala**; a fórmula de 6 elementos; o gancho como resposta de orientação; o teste da imagem parada a 0,5 s; a faixa de 5–8 palavras.

Depois, a parte que só a Canastra pode escrever: **10 a 15 ganchos concretos**, escritos por extenso, usando o que a marca realmente tem. Exemplos do tipo certo — cada um ancorado num fato da fazenda, não em suspense vazio:

- *"Esse café custa três vezes o do mercado. Vou te mostrar a conta."* (objeção, stakes)
- *"Tem um jeito de saber se o café é especial sem provar. Está escrito no pacote."* (breakdown, lacuna específica)
- *"Colhemos esse lote no dia mais quente do ano. Mudou o gosto."* (contradição com mecanismo)

Cada gancho deve declarar a estrutura que pede (resposta primeiro / prévia / stakes) e a matéria-prima que exige.

- [ ] **Passo 2: Verificar**

Rode cada gancho escrito contra o teste da imagem parada: descreva em uma linha qual seria o frame 1, e se ele faz sentido sozinho. Gancho que falhar aqui, reescreva.

- [ ] **Passo 3: Commit**

```bash
git add instagram/estrategia/02-ganchos.md
git commit -m "docs(estrategia): taxonomia de gancho e banco de ganchos da Canastra"
```

---

### Tarefa 4: Roteiro e relógio

**Arquivos:**
- Criar: `instagram/estrategia/03-roteiro.md`

- [ ] **Passo 1: Escrever**

O esqueleto Gancho → Promessa → Outro lado → Virada → Entrega; as três estruturas (resposta primeiro, prévia, stakes primeiro) com o critério de escolha; a tabela do relógio comportamental reproduzida deste plano; e a lista de padrões linguísticos que sinalizam potencial (contradição, número com escala, causalidade, transformação, risco, aplicação).

Inclua a advertência que vem do próprio harness pesquisado:

> Esta base produz hipótese testável, não promessa. O certo é dizer *"este clipe tem proposta em 1,8 s, primeiro valor em 4,9 s e nenhuma dívida de contexto; é publicável e serve para teste A/B"*. O errado é dizer *"este vídeo vai viralizar"*.

- [ ] **Passo 2: Verificar**

Pegue o `pl.mp4` já medido (ar morto até 1,14 s; silêncios em 5,08 · 6,78 · 9,55 · 13,99 · 16,02 · 17,50 · 21,52) e **escreva o laudo dele contra o relógio**: em que segundo está a orientação, a proposta e o primeiro valor. Se não houver proposta até 2,5 s, diga isso. É o primeiro uso real da base.

- [ ] **Passo 3: Commit**

```bash
git add instagram/estrategia/03-roteiro.md
git commit -m "docs(estrategia): estruturas de roteiro e relogio comportamental"
```

---

### Tarefa 5: Arquétipos e os casos fora do café

**Arquivos:**
- Criar: `instagram/estrategia/04-arquetipos.md`

- [ ] **Passo 1: Escrever**

Os oito arquétipos, cada um com estrutura em duas linhas. Depois, uma seção por marca estudada — @getgraza, @flybyjing, @omsom, @drinkpoppi, @chamberlaincoffee, @liquiddeath, Stanley — com **o mecanismo, não o elogio**, e uma linha final explícita de *transfere / não transfere*.

Três leituras que precisam estar escritas, porque são contraintuitivas:

- **@getgraza quase não mostra a origem.** Vende azeite de origem e a prova de autenticidade vem do bastidor da empresa, não da oliveira. Isso contradiz o instinto de "mostrar a fazenda" e merece teste.
- **@flybyjing resolve a frequência com parceiro local**, não com mais conteúdo próprio. Padaria, queijaria e cafeteria mineira são o equivalente disponível.
- **@omsom posta piada sem o produto aparecer.** Custo de produção zero e serve à identidade.

E a advertência dura: **humor irreverente não transfere.** A Liquid Death fracassou no Reino Unido por isso, e a Canastra é marca de fazenda de família — o tom é procedência, não piada.

- [ ] **Passo 2: Verificar**

Confirme que cada marca tem a linha *transfere / não transfere* e que nenhuma recomendação depende de verba que a Canastra não tem.

- [ ] **Passo 3: Commit**

```bash
git add instagram/estrategia/04-arquetipos.md
git commit -m "docs(estrategia): arquetipos e casos de marca fora do cafe"
```

---

### Tarefa 6: O catálogo de formatos

O documento que o motor de vídeo consome como briefing.

**Arquivos:**
- Criar: `instagram/estrategia/05-formatos.md`

- [ ] **Passo 1: Escrever a tabela mestra**

Cada formato uma linha, com estas colunas exatas:

`nome da série · estrutura em 1 linha · formato (reel / carrossel / estático) · duração alvo · matéria-prima · esforço (baixo/médio/alto) · o que o motor precisa fazer`

Inclua, no mínimo, os que saíram da pesquisa de concorrentes e de marcas fora do café:

| Série | Origem da ideia |
|---|---|
| "Você sabia que" | @sebastianspecialtycoffee — o perfil mais parecido, 6,2 mil seguidores |
| Infográfico sobre foto real | idem — setas e rótulos apontando cereja vs bóia |
| "Arraste para entender" | @cafezale.com.br — carrossel educativo |
| Jornada do grão | @orfeucafes — 5 slides em tela dividida, vídeo mudo real |
| Cápsula com parceiro local | @flybyjing — a saída para frequência sem institucional |
| Piada relatable sem produto | @omsom — custo zero |
| Meme de legenda com o pacote no cotidiano | @getgraza |
| Preparo em câmera lenta com legenda curta | @chamberlaincoffee |
| Bastidor-comemoração da família | @getgraza — prova de real sem roteiro |
| Objeção: por que custa mais | arquétipo de objeção derrubada |
| Edição limitada real da safra | drop com número real de sacas, nunca escassez falsa |

- [ ] **Passo 2: Marcar os três primeiros**

Escolha três para começar, e escreva **por que esses três**. Critério sugerido: o que usa matéria-prima que já existe, o que o motor já sabe fazer, e o que ataca o gargalo de cadência.

- [ ] **Passo 3: Verificar**

Toda linha tem matéria-prima declarada, e nenhuma exige coisa que a marca não tem. Formato que exija estúdio ou celebridade sai da tabela ou vai para uma seção "mais tarde".

- [ ] **Passo 4: Commit**

```bash
git add instagram/estrategia/05-formatos.md
git commit -m "docs(estrategia): catalogo de formatos com materia-prima exigida"
```

---

### Tarefa 7: Cadência

**Arquivos:**
- Criar: `instagram/estrategia/06-cadencia.md`

- [ ] **Passo 1: Escrever**

A receita de 2–3 combinações de tipo × formato, 2× por semana cada, avaliadas só depois de 30 dias. A regra de repetir **formato**, não tema. A comparação medida: Canastra 1 post a cada 42 dias contra Orfeu a cada 2,9 e Coffee++ a cada 2,1. **[medido]**

O calendário que todos os concorrentes cumpriram e a Canastra não: Dia do Cliente (15/09), Dia dos Pais, Dia do Amigo, 7 de Setembro, Dia Nacional do Café (24/05).

E a meta, escrita como número: sair de 0,17 post por semana para o piso da categoria, ~2 por semana.

- [ ] **Passo 2: Verificar**

A meta é um número, não um adjetivo. Se estiver escrito "postar mais", reescreva.

- [ ] **Passo 3: Commit**

```bash
git add instagram/estrategia/06-cadencia.md
git commit -m "docs(estrategia): cadencia com meta numerica e calendario"
```

---

### Tarefa 8: O que não fazer

**Arquivos:**
- Criar: `instagram/estrategia/07-nao-fazer.md`

- [ ] **Passo 1: Escrever**

Três seções.

**Pseudociência**, reproduzida da seção deste plano: dopamina como mecanismo causal, o multiplicador de 60.000×, os frameworks autorais tratados como terminologia da plataforma. Cada item com a explicação de *por que* não se sustenta.

**O que não transfere**: humor irreverente, verba de experimentação, reação generosa a viral que custa um carro, envio pago a criador de um milhão de seguidores.

**O que não funciona apesar de parecer**: gritar sem entregar; mistério sem pergunta definida; cortes a cada meio segundo sem mudança semântica; começar com "fica até o final"; apagar as pausas que dão peso; empilhar 5–7 elementos simultâneos na tela.

**As quatro contradições** registradas como contradições, sem escolher um lado.

- [ ] **Passo 2: Verificar**

Nenhum item está escrito como opinião. Cada um tem o motivo.

- [ ] **Passo 3: Commit**

```bash
git add instagram/estrategia/07-nao-fazer.md
git commit -m "docs(estrategia): pseudociencia, o que nao transfere, contradicoes"
```

---

## Verificação final

- [ ] os 8 arquivos existem
- [ ] **nenhuma afirmação numérica sem fonte nomeada** — varra à mão
- [ ] nenhuma inferência de criador redigida como oficial
- [ ] "dopamina" só aparece na seção de pseudociência
- [ ] o catálogo de formatos tem matéria-prima em toda linha
- [ ] a meta de cadência é um número
- [ ] o laudo do `pl.mp4` contra o relógio está escrito na Tarefa 4

## Riscos assumidos

1. **Metade dos números de retenção é terciária.** Vieram de um canal citando um estudo que não verificamos. Estão marcados `[terciário]` e não devem virar meta.
2. **O que funciona para @getgraza pode não funcionar aqui.** Marca de Nova York com tom irônico e público urbano. A leitura "quase não mostra a origem" é um achado para **testar**, não uma regra para adotar.
3. **Nenhuma fonte deu dado sobre capa de Reels.** É lacuna conhecida da pesquisa, não omissão.
