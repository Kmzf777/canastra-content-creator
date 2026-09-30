# Base de estratégia de conteúdo

Esta base decide **o que gravar**, antes de alguém abrir a câmera e antes de o motor de
vídeo renderizar qualquer coisa. Ela existe porque a Canastra não tem problema de
audiência — tem problema de *decisão*: a conta publica **1 post a cada 42 dias** com
taxa de engajamento de **0,50%**, melhor que a do Coffee++, que tem 269 mil seguidores
**[medido]**. Não falta gente olhando. Falta peça pronta para publicar.

O motor em `instagram/remotion/` consome esta base como **briefing**: o catálogo de
formatos (`05-formatos.md`) declara, formato por formato, qual matéria-prima o vídeo
exige e o que o motor precisa fazer com ela.

---

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

### Por que a marcação vem antes do conteúdo

Porque as cinco camadas se parecem muito quando estão na mesma frase, e a confusão tem
consequência prática:

- **[oficial]** pode virar meta. *Tempo médio assistido* é o sinal principal de ranking
  **[oficial]** — otimizar por isso é apostar no que a plataforma declarou.
- **[terciário]** não pode virar meta. *"Rosto humano nos primeiros 3 s rende +10% de
  retenção"* **[terciário]** veio de um canal citando um estudo que não abrimos. Serve
  para gerar hipótese de teste, nunca para cobrar resultado.
- **[folclore]** tem que ser reconhecido de longe. *"Dopamina"* como mecanismo causal de
  retenção **[folclore]** aparece em fonte após fonte sem um único estudo citado, e quem
  escreve a partir dela acha que está fazendo ciência. **A refutação inteira fica em
  [`07-nao-fazer.md`](07-nao-fazer.md) §1.1** — é lá, e só lá, que esta base discute o
  mecanismo. Se a palavra aparecer em qualquer outro documento como explicação de por que algo
  funciona, é erro de redação.

Uma base que apaga essa diferença não é base, é folclore com sumário.

### Quando a afirmação é leitura, não medida

A marca descreve a **origem do fato**, não a conclusão tirada dele. Interpretação
empilhada sobre um fato medido mantém a marca do fato e diz, na própria frase, que é
interpretação — é a convenção que `instagram/01-concorrencia.md` já usa:

> @coffeemais tem 269 mil seguidores e mediana de 96 curtidas **[medido]**. *(Leitura
> minha, não medição: uma base construída por sorteio explicaria os dois números ao
> mesmo tempo. Não dá para provar isso de fora.)*

Não invente uma sexta marca para isso. Cinco marcas, mais a frase explícita.

### Estado do repositório não é [medido]

**[medido]** é para número que não muda sozinho: a dimensão de um arquivo, a mediana de
curtidas de um perfil, o dB médio de um áudio. **Estado do repositório muda** — um agente
constrói o motor na hora seguinte e a frase vira mentira sem que ninguém a tenha editado.

Por isso: **afirmação sobre o que existe no disco não leva [medido] no meio de um documento
de estratégia.** Estratégia descreve *o que fazer*, não *o que existe hoje*. Quem quiser
saber o que existe roda `ls` — e a resposta de hoje não é a de amanhã.

Onde citar estado for indispensável — porque um formato depende de uma capacidade que ainda
não existe, por exemplo — escreva assim:

> *Retrato de 30/09/2026:* `Raiz.tsx` registra três composições. Confira antes de usar.

Três exigências: a **data**, a palavra **retrato** (ou equivalente que diga "isto envelhece")
e **nenhuma marca de origem**. A marca [medido] promete reconferibilidade estável, e um
caminho de arquivo não entrega isso.

Esta regra nasceu de um erro real: `05-formatos.md` teve uma seção intitulada *"O que o motor
sabe fazer hoje: nada"* marcada **[medido]**, e ela já estava falsa no mesmo dia em que foi
escrita — o motor tinha função de zonas, camada de legenda, sondagem, transcrição e testes
passando. Uma afirmação marcada [medido] que envelhece em minutos é pior que nenhuma
afirmação: ela convida a próxima sessão a confiar sem conferir.

---

## Os oito documentos

| Arquivo | O que decide |
|---|---|
| `LEIA-ME.md` | índice e a convenção de marcação — **este arquivo** |
| `01-ranking.md` | o que a plataforma premia, oficial separado de inferência |
| `02-ganchos.md` | taxonomia de gancho e o banco de ganchos da Canastra |
| `03-roteiro.md` | estruturas de roteiro e o relógio comportamental |
| `04-arquetipos.md` | moldes de marca de produto, com os casos fora do café |
| `05-formatos.md` | **o catálogo que o motor consome**, com matéria-prima exigida |
| `06-cadencia.md` | calendário, séries nomeadas e a meta numérica |
| `07-nao-fazer.md` | pseudociência, o que não transfere, as contradições |
| `08-fontes.md` | de onde veio cada afirmação |

A coluna *Estado* que existia aqui foi removida: ela dizia "a escrever" para sete arquivos que
já estavam escritos, e é exatamente o erro que a regra *Estado do repositório não é [medido]*
descreve. Quem quiser saber o que existe lista a pasta. **Quem acrescentar um nono documento
acrescenta a linha** — essa parte não envelhece.

### Em que ordem ler

- **Vai gravar?** `05-formatos.md` escolhe a peça, `02-ganchos.md` dá a primeira frase,
  `03-roteiro.md` dá o esqueleto e os segundos.
- **Vai decidir o que priorizar?** `06-cadencia.md` e `01-ranking.md`.
- **Vai avaliar uma ideia que alguém trouxe?** `07-nao-fazer.md` primeiro. Boa parte das
  ideias que chegam prontas já está catalogada ali como o que não transfere.
- **Vai discordar de um número?** `08-fontes.md` diz de onde ele veio e quão frágil é.

---

## O que esta base não é

**Não é promessa de viralização.** Ela produz hipótese testável. A frase certa tem esta
forma — *"este clipe tem proposta em 1,8 s, primeiro valor em 4,9 s e nenhuma dívida de
contexto; é publicável e serve para teste A/B"* (segundos de exemplo, não medição de um
clipe real). A errada é *"este vídeo vai viralizar"*.

**Não é pesquisa em andamento.** A pesquisa foi feita, e o plano
`docs/superpowers/plans/2026-09-30-base-estrategia-viral.md` registra o esforço como
4 agentes, ~36 transcrições de YouTube, 11 perfis de Instagram lidos no DOM e a mineração
de um harness open source. **Esses números são registro interno e não são
reconferíveis:** as transcrições não estão no repositório e a contagem de perfis não fecha
com os perfis efetivamente nomeados — conferido em 30/09/2026 **[medido]**, detalhado em
`08-fontes.md` §5 e §7. O insumo aproveitável está catalogado em `08-fontes.md`. Escrever
estes documentos é redação, não coleta.

**Não guarda a matéria-prima bruta.** As ~36 transcrições **não estão neste
repositório** — `instagram/pesquisa/` está vazio em 30/09/2026, e os IDs dos vídeos não
foram registrados. Verificado nesta data **[medido]**. Consequência: nenhuma afirmação
marcada **[criador]** ou **[terciário]** pode ser reconferida na fonte. Ver a seção *O
que não foi possível reconstruir* em `08-fontes.md`.

---

## Três números que enquadram todo o resto

1. **1 post a cada 42 dias, contra 2,9 do Orfeu** **[medido]**. É 14× menos frequência no
   mesmo nicho e na mesma faixa de preço. Entre 23/05 e 25/09/2026 saiu um único post.
2. **69% do feed da Canastra é estático, e reel bate estático em todo perfil da amostra**
   — 5,2× no @sebastianspecialtycoffee, que tem um terço dos seguidores **[medido]**.
3. **Conteúdo novo recebe ~100 impressões; performando acima do esperado, gradua para
   1.000 e depois 10.000** **[oficial]**. Ou seja: cada post é um bilhete nessa loteria, e
   a 1 post a cada 42 dias a marca compra pouquíssimos bilhetes.

O número 3 é o que transforma o número 1 em urgência. Cadência não é higiene de
marketing; é quantidade de tentativa de exploração.

---

## Lacunas conhecidas

Registradas para não serem confundidas com omissão:

- **Nenhuma fonte da amostra deu dado sobre capa de Reels.** A pesquisa não cobriu isso.
- **Views, salvamentos, compartilhamentos e alcance da própria conta não foram medidos** —
  curtida é o único sinal público, e ela subestima reel, que roda por view **[medido]**.
  As taxas de `01-concorrencia.md` são *curtidas medianas ÷ seguidores*: servem para
  comparar perfis entre si, não são taxa de engajamento de plataforma.
- **Metade dos números de retenção é [terciário].** Não vire meta com eles.
- **O que funciona para @getgraza pode não funcionar aqui.** É marca de Nova York, tom
  irônico, público urbano. A leitura *"quase não mostra a origem"* é achado para
  **testar**, não regra para adotar.
