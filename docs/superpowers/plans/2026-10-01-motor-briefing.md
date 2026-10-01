# Motor de vídeo dirigido por briefing — plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recomendado) ou superpowers:executing-plans para executar tarefa por tarefa. Os passos
> usam caixa de marcação (`- [ ]`) para rastreio.

**Goal:** transformar `instagram/remotion/` de renderizador de UMA peça em motor dirigido por
`briefing.json` — cenas, fonte que pode ser foto, eventos de texto em lista, trilha de áudio,
compilador puro, portão de ritmo e uma skill que coleta a informação.

**Architecture:** `briefing.json` (verdade humana, um relógio: segundos por cena) →
`esquema.ts` (zod, valida FORMA) → `refinar.ts` + `compilar.ts` (puros, validam SENTIDO e fazem
toda a aritmética de tempo) → `plano.json` (gerado, com `_sha256Briefing`) →
`<Composition schema>` → `Peca` = `AbsoluteFill(terra){ TransitionSeries[Sequence → Cena{Fonte
+ eventos}] , Legenda FORA, Trilha FORA }` → render por formato → normalizar áudio → 6 portões.
A fronteira é rígida: nada que precise de prova mora num `.tsx`, porque `tipografia.ts` faz
`loadFont` no topo do módulo e derruba o vitest com `TypeError: Invalid URL`.

**Tech Stack:** Remotion 4.0.530 · React 19 · TypeScript 7 · vitest 5 · zod 4.5.4 (a declarar)
· `@remotion/transitions@4.0.530` (a instalar) · Node 22.16 com `--experimental-strip-types`
para os portões.

**Spec:** `docs/superpowers/specs/2026-09-30-motor-briefing-design.md` (**1.934 linhas**, revisada
em 01/10/2026). Lida inteira antes deste plano. Onde este plano e a spec divergirem, a spec manda
— exceto nos pontos listados em **Riscos assumidos**, onde a spec deixou a decisão aberta ou onde
uma medição deste plano contradisse a spec, e nesse caso a medição está escrita ao lado.

---

## O que mudou na spec em 01/10/2026, e onde este plano acompanhou

A spec foi corrigida depois da primeira escrita deste plano (773 → 1.704 → 1.934 linhas). Cinco correções
de gravidade alta mexem no contrato, e **cada uma tem tarefa aqui**. Esta tabela existe para que
ninguém releia 1.934 linhas para descobrir o que mudou:

| correção da spec | o que muda neste plano |
|---|---|
| **§3.3.3** — `sondar()` não serve para foto: devolve `1,7778` onde a razão de exibição é `0,5625`, `rotacao: 0` num `Orientation 6`, e **inventa** `fps: 25`/`duracao: 0.04` para foto parada | **Tarefa 4A (nova)**: `sondar()` passa a ler EXIF `Orientation` pelo mesmo `ffprobe`, `rotacao` vira `{fonte, graus}`, e `fps`/`duracao` viram `null` num fluxo de um frame. O portão de ritmo confere `razaoExibicao` declarada contra a medida, tolerância 0,005 |
| **§2.3 + §3.6** — não existia campo de locução; `audio` passa a ser **obrigatório**, com `locucao` e `trilha` que podem ser `null` mas não os dois | **Tarefa 5** (esquema), **Tarefa 6** (recusa `audio-mudo`), **Tarefa 7** (o plano carrega `audio`), **Tarefa 9** (`Trilha.tsx` monta as duas faixas), **Tarefa 13** (briefing da prova) |
| **§2.2.1** — o rebase da legenda com N cenas ganhou fórmula e `ancora` de três casos | **Tarefa 5** (`zLegenda` reescrito), **Tarefa 6** (recusa `legenda-sem-ancora`), **Tarefa 7** (`compilarLegenda` com a fórmula, e os dois contadores de diagnóstico) |
| **§3.4.2** — `encaixe` **sai do briefing** e passa a ser derivado de `(pista, formato)`; a geometria de pista ganhou números; e a causa mecânica dos 90,20 px é `layout.ts:68-73` | **Tarefa 3** (`ENCAIXE_PADRAO` deixa de existir), **Tarefa 4** (geometria nova + o conserto de uma linha na largura da legenda), **Tarefa 5** (campo fora do esquema), **Tarefa 6/7/9** (ninguém mais passa lista de preferência) |
| **§3.4.2** — `PISO_DE_DOMINANCIA` é de **área**, não de corpo, e vale **1,25 ×** a dominância da legenda | **Tarefa 4** (`encaixe.ts` mede área), **Tarefa 10** (o piso é recusa do portão, não aviso) |

E duas correções de rótulo que este plano repetia: **a sobreposição manchete × legenda é 90,20 px
de interseção em x no 1:1** (não 353,20 px, que era `manchete.fim − legenda.y`, uma grandeza
diferente), e **no 9:16 não há sobreposição nenhuma** — interseção 0,00. Onde o plano dizia 353,20
ele agora diz 90,20, com o eixo nomeado.

### Segunda rodada de correção da spec, 01/10/2026 — três na spec, uma aqui

| correção | onde | o que muda neste plano |
|---|---|---|
| **§3.4.2** — a geometria de pista descrevia caixas que o motor não tem: `rodape` não é a faixa 0,76–1,00 da coluna (é `zonas.legenda`), `tela` não é a coluna (é `zonas.seguro`), a coluna não é "a caixa da sobra" (é `intersecao(zonas.manchete, zonas.seguro)`), e a invariante "as quatro pistas partilham o x" é **falsa** nos três formatos de coluna | spec | **nada a implementar: o plano já estava certo** e a spec o contradizia. A Tarefa 4, Step 4 ganhou a nota de que a spec agora concorda, e o teste de pistas ganhou o aviso de que a invariante depende do **§0** — medido: com o conserto da largura mas sem `MARGEM` em fração, 1:1 × paisagem ainda dá 22.429,50 px², porque ali a sobreposição é em **y** |
| **§3.4.2** — *"ligado hoje, o piso de dominância reprova o `01-private-label` no 1:1 e no 4:5"* era falso e estava sem marca de procedência: a peça renderiza em `cartela` e ali a mancha é 4,4× a 7,8× a dominância da legenda, contra um piso de 1,25×. O que reprova é a manchete em **coluna** (`sobreImagem`): 0,866× no 1:1 e 0,149× no 4:5 — medido na árvore pós-§0 | spec | nada: a Tarefa 13 já declara `pista: "tela"` pelo mesmo motivo medido. A spec passou a dizer o que o plano já fazia |
| **§2.2.1 + §7.1** — a spec dizia *"grudado em 0, **nunca** descartado"* e este plano já descartava bloco sem frame visível, com contador e teste; e §7.1 não dizia que o portão de ritmo **reprova** o único briefing concreto dela | spec | nada: `descartadosAntesDoInicio`, os 14 frames de recuo e a reprovação de `legenda-recuada` já estavam aqui (Tarefa 7 Step 2c/6, Tarefa 10 Step 6). A spec parou de contradizer |
| **`razaoDaPeca()` ignorava `enquadramento`** — ela empurrava `f.razaoExibicao` de todo `video` e toda `foto`, então uma cena `telaCheia`/`recorte` ou `preencher` restringia o quadro e **não conseguia preenchê-lo**: no 9:16 com razão 1,3333 a faixa é 1080×810 e sobram 57,81% de terra | **este plano** | **Tarefa 7** (a função passa a contar só `enquadramento: 'faixa'`, e dois testes novos — o antigo passava com a função errada porque o fixture punha a razão menor justamente na cena `preencher`) e **Tarefa 9** (`Cena.tsx` dá a caixa do **quadro** à cena que preenche, e `zonas.video` à que está em contain). `compilar.test.ts` vai de 20 para **22** |

---

## Estado medido da máquina, que os passos abaixo assumem

Medido nesta sessão, com `find`, `cat`, `grep` e `ls` nos arquivos reais:

| fato | evidência |
|---|---|
| `src/` tem 28 arquivos; nenhum `Series`/`TransitionSeries`/`Sequence` fora de comentário | `grep -rn "TransitionSeries\|<Series\|Sequence" src/` = 5 ocorrências, todas comentário |
| `Fonte.tsx` só monta `<Video>` de `@remotion/media` | `src/motor/camadas/Fonte.tsx:48` |
| `manchete?: Manchete \| null` é objeto único | `src/motor/PecaVideo.tsx:93` |
| nenhum `<Audio>` na árvore | `grep -rn "Audio" src/` acha só `motor/audio/normalizar.ts` |
| `useVideoConfig` em UM arquivo, só `width`/`height` | `PecaVideo.tsx:58` e `:97` |
| `FPS = 30` chumbado, `CORTAR_ANTES_FRAMES` e `DURACAO_FRAMES` derivados em tempo de módulo | `Raiz.tsx:22,25,28` |
| `zod` e `@remotion/zod-types` ausentes do `package.json` | `cat package.json` — `dependencies` tem 8 entradas, nenhuma é zod |
| `@remotion/transitions` ausente do `package.json` | idem |
| `conferir.mjs` conhece 5 portões: `todos, folha, telefone, determinismo, loop` | `scripts/conferir.mjs:77` |
| `src/verificacao/preservacao.ts` existe, exporta `compararRegiao` e `Laudo`, e ninguém o chama | `grep -n "export" src/verificacao/preservacao.ts` |
| suíte: 6 arquivos, 91 chamadas `it(` (5 + 4 + 16 + 9 + 6 + 51) | `grep -c 'it(' tests/*.test.ts` |
| **a suíte não foi rodada nesta sessão** | o plano de qualidade registra `85 passed`; não concilio os dois números |

**Por isso nenhum passo deste plano diz "Expected: 124 passed".** Onde a suíte inteira é
rodada, o passo manda **anotar o número antes** e conferir o delta. Número que eu não medi não
entra num `Expected:`.

---

## Como este plano se relaciona com o plano de qualidade de 99 KB

`docs/superpowers/plans/2026-09-30-motor-video-qualidade.md` (2.327 linhas, 7 tarefas)
**continua valendo e não é duplicado aqui.** Copiar as tarefas dele para dentro deste arquivo
criaria os dois planos concorrentes que a spec proíbe. A relação, tarefa por tarefa:

| tarefa do plano de qualidade | o que fazer com ela |
|---|---|
| **1** — ponta de entrada/saída na legenda + contorno | **continua valendo, em separado, e está agendada no §0.6.** Não é pré-requisito: a legenda fica FORA da `TransitionSeries`, então o escopo dela não muda com cena. Mas sem ela a **Regra 6** (a legenda é a camada mais vista e não tem nenhuma propriedade dependente de frame; entra e sai por corte) continua violada depois deste plano inteiro |
| **2** — saída chega a zero no último frame desenhado | **PRÉ-REQUISITO.** Executar antes da Tarefa 1 deste plano (ver §0) |
| **3** — margem em fração do eixo próprio, topo em 5% | **PRÉ-REQUISITO.** Executar antes da Tarefa 1 (ver §0). A Tarefa 4 deste plano lê `MARGEM` como fração — ela não compila sem a 3 |
| **4** — push como propriedade `scale`, sem mover o canto | **continua valendo, em separado, e está agendada no §0.6.** Não é pré-requisito mecânico de cena: `push()` não lê fps nem cena |
| **5** — `premountFor={fps}` + schema zod | **ABSORVIDA.** O `premountFor` entra na Tarefa 8 (`Fonte` polimórfica) e na Tarefa 9 (`TransitionSeries.Sequence`); o zod entra na Tarefa 5, validando o **briefing** e não só as props. **Não execute a Tarefa 5 do plano de qualidade** — ela cria `src/motor/esquema.ts`, que a Tarefa 5 deste plano substitui por `src/briefing/esquema.ts` |
| **6** — portão de fps (`exigirFpsDeReferencia`) | **NÃO EXECUTAR.** Ela é a alternativa honesta enquanto `fps` não é campo; a Tarefa 2 deste plano faz `fps` ser campo. Criar o portão agora seria escrever uma função para deletá-la na mesma sessão. O piso da legenda em SEGUNDOS (`LEGENDA.duracaoMinSegundos = 0.333`, Steps 3 e 5 daquela tarefa) **entra aqui**, na Tarefa 2 |
| **7** — invariante de duas linhas na legenda | **continua valendo, é promovida, e está agendada no §0.6:** a pista `rodape` (Tarefa 4) **é** a caixa de legenda, e a Tarefa 4 depende dessa invariante duas vezes — a fração 0,24 da folga da coluna e o `PISO_DE_DOMINANCIA`, que mede a legenda como **duas linhas cheias**. Executar depois da Tarefa 4 deste plano, não antes |

**A §5 do plano de qualidade ("o que NÃO mudar") é respeitada item por item.** Nada aqui toca
`bezierDeCss`, `POUSO`, `fases()` (só ganha um parâmetro), o `push` linear, a busca binária de
corpo, `intersecao`, `alinhaHorizontal: 'flex-start'`, `linhasDeFolga = 1` na cartela, o fundo
terra, `SUB.fonte`, ou a ordem de árvore.

**`tests/manchete-props.test.ts` É tocado, e a versão anterior deste plano afirmava o contrário.**
Medido agora: ele chama `formaTextoTela` sem `cadencia` nas linhas **63**, **186** e **211**, e
`duracaoDaFrase` sem `cadencia` nas linhas **65** e **176**. A Tarefa 2 torna o parâmetro
obrigatório, então esse arquivo entra na varredura dela (Files e Step 12), e a Tarefa 12 o migra
para o briefing. Prometer que ele não seria tocado fazia o executor descobrir cinco erros de `tsc`
num arquivo marcado como intocado.

---

## As 12 licenças: a decisão fica explícita e parametrizável, nunca em silêncio

Dez técnicas de reel viral colidem com `src/identidade/proibicoes.md`. Este plano **não
escolhe**. Ele faz três coisas e para:

1. O bloco `licencas` entra no esquema (Tarefa 5) com **os 12 booleanos em `false`**, cada um
   com a linha de `proibicoes.md` que ele derruba escrita no comentário do campo.
2. Ligar qualquer um **exige `justificativa` com ≥ 12 caracteres**, e `refinar.ts` reprova
   licença ligada sem justificativa (Tarefa 6).
3. **Nenhuma técnica ligada por licença é implementada neste plano.** O portão de ritmo
   (Tarefa 11) **avisa, sem reprovar**, nomeando cada licença ligada, a linha de proibição e a
   frase "nenhuma técnica de licença está implementada — o campo registra a decisão, o código
   vem depois dela". Um booleano que ligasse um efeito inexistente seria a lição 3 do
   `CLAUDE.md` outra vez: HTTP 200 ignorando o parâmetro.

Isso é **D1** da spec, e continua com o Rafael. A spec pede que ele decida **por série**, não
por peça, senão a coesão de série vira acidente.

---

## Mapa de arquivos

**Criados:**

| arquivo | responsabilidade | puro? |
|---|---|:---:|
| `src/motor/relogio.ts` | a ÚNICA conversão segundo↔frame do sistema | sim |
| `src/motor/cadencia.ts` | `TEMPO_S` em segundos e a tabela de frames derivada de `fps` | sim |
| `src/motor/pista.ts` | os NOMES das pistas e os conflitos (Tarefa 3) + a geometria de pista, coluna de texto e derivação de encaixe (Tarefa 4) | sim |
| `src/motor/registro.ts` | a geometria dos três registros de foto e o recorte em porcento | sim |
| `src/motor/evento.ts` | `FAMILIA_DO_PAPEL`, `CADENCIA_DO_PAPEL`, `PISTA_PADRAO` | sim |
| `src/motor/encaixe.ts` | mede o corpo na caixa da pista e compara com o `PISO_DE_DOMINANCIA` | sim |
| `src/briefing/esquema.ts` | zod: a FORMA do briefing e do plano | sim (zod puro, sem `@remotion/zod-types`) |
| `src/briefing/refinar.ts` | as recusas de SENTIDO que zod não expressa | sim |
| `src/briefing/compilar.ts` | briefing → plano: aritmética de tempo e rebase da legenda | sim |
| `src/briefing/impressao.ts` | `sha256Do` canônico e `selarPlano`. **Único arquivo de `src/briefing/` que importa `node:crypto`** | não (Node) |
| `src/motor/tempo-de-cena.ts` | `janelaDaCenaNaPeca` e `frameDaCenaNoFrameDaPeca` — puras, fora do `.tsx` | sim |
| `src/motor/Cena.tsx` | fiação de uma cena: fonte + eventos | não |
| `src/motor/Peca.tsx` | fiação da peça: `TransitionSeries` + legenda + áudio | não |
| `src/motor/camadas/Trilha.tsx` | fiação do `<Audio>` de `@remotion/media` — locução **e** trilha, a ausência A4 | não |
| `src/verificacao/ritmo.ts` | o portão de ritmo, roda antes do render | sim (o disco entra injetado) |
| `scripts/compilar.mjs` | CLI: `briefing.json` → `plano.json` | não |
| `.claude/skills/canastra-briefing/SKILL.md` | a entrada: coleta, esquema, recusas, registro | — |

**Por que `pista.ts` e `encaixe.ts` são dois arquivos, quando a spec §2.4 nomeia um.** A spec põe
"a geometria de pista e a derivação de encaixe" em `src/motor/pista.ts`. Aqui a geometria fica em
`pista.ts` e a **medição** fica em `encaixe.ts`, porque medir o corpo exige `formaTextoTela`, que
importa `identidade/glifos` e `identidade/tokens`. Mantendo `pista.ts` livre dessa dependência,
`evento.ts` pode importar o tipo `Pista` dele sem arrastar tipografia — e é exatamente essa
importação que quebrava a ordem das tarefas (ver Tarefa 3). Divergência registrada nos **Riscos
assumidos**.

**Modificados:** `src/identidade/tokens.ts` · `src/motor/movimento.ts` ·
`src/motor/camadas/texto-forma.ts` · `src/motor/camadas/TextoTela.tsx` ·
`src/motor/camadas/Fonte.tsx` · `src/motor/layout.ts` · `src/motor/Raiz.tsx` ·
`src/legenda/agrupar.ts` · `scripts/conferir.mjs` · `package.json` ·
`.claude/skills/canastra-video/SKILL.md` · os arquivos de `tests/` atingidos pela varredura.

**Retirados:** `scripts/gerar-props.mjs` (Tarefa 12, no mesmo commit em que o compilador passa a
escrever o plano — dois escritores disputando um arquivo é pior que um) ·
`src/motor/PecaVideo.tsx` (Tarefa 9, substituído por `Peca.tsx` + `Cena.tsx`).

---

## Em que shell rodar os comandos deste plano

**Rode tudo no Git Bash**, não no PowerShell. O ambiente desta máquina declara *"Shell: PowerShell
(primary); Bash tool also available"*, e os comandos abaixo usam sintaxe POSIX em cinco
lugares, medidos e localizados:

| construção POSIX | onde | por que quebra no PowerShell |
|---|---|---|
| `mkdir -p` | Tarefa 8 Step 9, Tarefa 13 Step 1 | `-p` não é flag de `New-Item`; o equivalente é `New-Item -ItemType Directory -Force` |
| `cp origem destino` com continuação por `\` | Tarefa 8 Step 9, Tarefa 13 Steps 1 e 5 | a continuação de linha do PowerShell é backtick, não barra invertida |
| `for FR in 60 258 ...; do ... done` | Tarefa 13 Step 8 | erro de parse; o equivalente é `foreach ($FR in 60,258,...) { ... }` |
| `for P in folha telefone ...; do ... done` | Verificação final, item 3 | idem |
| `mv` e `rm` | Tarefa 10 Step 6 e 6b, Tarefa 12 Step 4 | são aliases de `Move-Item`/`Remove-Item` e funcionam, mas `rm -rf` não |

Onde o equivalente em PowerShell é curto, ele está escrito ao lado do comando. Onde não é, a
instrução é abrir o Git Bash: manter duas versões de um laço de cinco frames é pior que nomear o shell.
Os `node -e` e `npx` são iguais nos dois.

---

## §0 — Pré-requisito: as Tarefas 2 e 3 do plano de qualidade

Elas estão escritas por inteiro, com código e comando, em
`docs/superpowers/plans/2026-09-30-motor-video-qualidade.md` linhas **825–937** (Tarefa 2) e
**939–1089** (Tarefa 3). **Não as reescrevo aqui de propósito:** a spec §6 manda absorver aquele
plano, não duplicá-lo, e trecho de código copiado para dois arquivos diverge no primeiro
conserto.

- [ ] **Passo 0.1: anotar o estado da suíte ANTES de tudo**

Run:
```
cd instagram/remotion
npx vitest run
```
Anote as linhas `Test Files` e `Tests` num rascunho. Todo passo deste plano que roda a suíte
inteira se refere a esse número como **BASE**. (`grep -c 'it(' tests/*.test.ts` dá 91 chamadas
em 6 arquivos; o plano de qualidade registra `85 passed`. Ninguém conciliou os dois — use o que
a sua execução imprimir.)

- [ ] **Passo 0.2: executar a Tarefa 2 do plano de qualidade** (linhas 825–937 daquele arquivo)

Muda 4 linhas de `src/motor/movimento.ts` (o `+1` que normaliza a saída pelo último frame
desenhado) e ajusta 2 testes. Ordem obrigatória: **antes** da Tarefa 3, porque com N cenas o
resíduo de 18,85% aparece N vezes e, na janela de crossfade, fica *sobre* a cena seguinte.

Expected ao fim: `npx vitest run` com BASE + 1 teste.

- [ ] **Passo 0.3: executar a Tarefa 3 do plano de qualidade** (linhas 939–1089)

Troca `MARGEM` de pixels a 1080×1920 para **fração do eixo que cada margem corta**:
`{topo: 0.05, base: 0.16, lado: 160/1080}`, e renomeia `k` para `kx` nas folgas em pixel da
caixa de legenda. **A Tarefa 4 deste plano importa `MARGEM` como fração e não compila sem
isto.**

Expected ao fim: `npx vitest run` com BASE + 3 testes. Efeito colateral medido e desejado,
registrado lá: o corpo da cartela sobe de 104 para 123 px no Feed 1:1.

- [ ] **Passo 0.4: conferir que o §0 está fechado**

Run:
```
cd instagram/remotion
grep -n "MARGEM = " src/motor/layout.ts
grep -n "inicioSaida + 1" src/motor/movimento.ts
```
Expected: a primeira imprime `const MARGEM = {topo: 0.05, base: 0.16, lado: 160 / 1080};`; a
segunda imprime a linha do `pSaida` contendo `(t - inicioSaida + 1) / f.saida`. Se qualquer uma
falhar, o §0 não está feito e as tarefas abaixo vão quebrar longe da causa.

- [ ] **Passo 0.5: o CONTROLE de determinismo, antes de qualquer prova por sha256**

A Tarefa 2 prova que "a 30 fps não muda um pixel" comparando o sha256 do mesmo still antes e
depois. Essa prova só vale se o still for **byte-reproduzível nesta máquina** — senão um `MUDOU` é
ambíguo entre regressão da migração e não-determinismo do render, e o plano não teria como
distinguir os dois.

O repositório já tem o portão que mede isso: `scripts/conferir.mjs:181-211` chama
`conferirDeterminismo`, que renderiza o mesmo frame duas vezes e compara hash **e** pixel. Ele não
era chamado por nenhum passo deste plano. Neste momento ele ainda lê `props.json`, que existe — a
troca para `plano.json` é a Tarefa 9.

Run:
```
cd instagram/remotion
node scripts/conferir.mjs --projeto=projetos/01-private-label --portao=determinismo --frame=120
node scripts/conferir.mjs --projeto=projetos/01-private-label --portao=determinismo --frame=300
```
Expected: os dois blocos `== portao 3: determinismo ==` com veredito OK — dois renders do mesmo
frame, byte a byte iguais.

**Se algum reprovar, PARE.** Sem determinismo, a comparação de sha256 dos Steps 1 e 15 da Tarefa 2
não é prova de nada, e a tarefa inteira perde o portão. Nesse caso a alternativa é comparar as
métricas do frame (o `maiorDelta` que `determinismo.ts` já devolve) em vez do hash — e isso é uma
mudança de método que precisa ser decidida antes, não depois de ver um `MUDOU`.

- [ ] **Passo 0.6: agendar as Tarefas 1, 4 e 7 do plano de qualidade, que NÃO são absorvidas**

Três tarefas daquele plano continuam valendo em separado, e sem uma caixa de marcação aqui elas
somem — que é como a **Regra 6** (a legenda não tem nenhuma propriedade dependente de frame)
continuaria violada depois de executar este plano inteiro.

| tarefa | linhas em `2026-09-30-motor-video-qualidade.md` | quando |
|---|---|---|
| **1** — ponta de entrada/saída na legenda + contorno | **388–823** | a qualquer momento. **É ela, e só ela, que fecha a Regra 6** |
| **4** — push como propriedade `scale` | **1091–1341** | a qualquer momento. Toca uma linha da `Fonte.tsx` desta Tarefa 8 |
| **7** — invariante de duas linhas na legenda | **1931–2218** | **depois da Tarefa 4 deste plano**, porque a Tarefa 4 usa a caixa de legenda em dois lugares: a folga de 24% da coluna e o `PISO_DE_DOMINANCIA` |

- [ ] executar a **Tarefa 1** do plano de qualidade
- [ ] executar a **Tarefa 4** do plano de qualidade
- [ ] executar a **Tarefa 7** do plano de qualidade — **só depois da Tarefa 4 deste plano**

(As três estão escritas por inteiro lá, com código e conferência no pixel. Não as reescrevo aqui
pelo mesmo motivo das Tarefas 2 e 3: trecho copiado para dois arquivos diverge no primeiro
conserto.)

---

### Tarefa 1: o relógio — a única conversão segundo↔frame do sistema

Primeira tarefa porque é a peça que todas as outras importam, e porque a 30 fps ela **não muda
um pixel**: `emFrames(0.4, 30)` devolve os mesmos 12 frames que `TEMPO.entrada` tem hoje.

**Files:**
- Create: `instagram/remotion/src/motor/relogio.ts`
- Test: `instagram/remotion/tests/relogio.test.ts`

- [ ] **Step 1: escrever o teste que falha**

Criar `instagram/remotion/tests/relogio.test.ts`:

```ts
import {describe, expect, it} from 'vitest';
import {emFrames, emSegundos} from '../src/motor/relogio';

describe('emFrames', () => {
  it('reproduz EXATAMENTE os tokens medidos a 30 fps', () => {
    // Os quatro numeros que hoje estao chumbados em frames em tokens.ts:
    //   TEMPO.entrada 12 · TEMPO.stagger 3 · TEMPO.holdFinal 12
    //   LEGENDA.duracaoMinFrames 10
    // Este teste e a prova de que declarar em SEGUNDOS nao muda a peca a 30 fps.
    expect(emFrames(0.4, 30)).toBe(12);
    expect(emFrames(0.1, 30)).toBe(3);
    expect(emFrames(0.333, 30)).toBe(10);
  });

  it('a 60 fps dobra, a 24 fps encurta -- e e por isso que a funcao existe', () => {
    expect(emFrames(0.4, 60)).toBe(24);
    expect(emFrames(0.1, 60)).toBe(6);
    expect(emFrames(0.4, 24)).toBe(10);
    // 0,1 s a 24 fps da 2,4 -> 2 frames, que continua dentro da faixa util de
    // stagger (2 a 4 frames) que tokens.ts registra.
    expect(emFrames(0.1, 24)).toBe(2);
  });

  it('arredonda, nao trunca: 2,5 frames vira 3 e nao 2', () => {
    // Truncar acumularia erro sempre para baixo e uma peca de 12 cenas sairia
    // mais curta que o briefing -- o defeito que o pedido do Rafael nomeia.
    expect(emFrames(1 / 12, 30)).toBe(3); // 2,5 -> 3
  });

  it('recusa fps que nao seja inteiro positivo, em vez de devolver NaN', () => {
    expect(() => emFrames(1, 0)).toThrow(/fps/);
    expect(() => emFrames(1, -30)).toThrow(/fps/);
    expect(() => emFrames(1, 29.97)).toThrow(/inteiro/);
  });

  it('recusa segundo negativo', () => {
    expect(() => emFrames(-0.1, 30)).toThrow(/negativo/);
  });

  it('emSegundos e a volta, e a ida e volta a 30 fps nao perde os tokens', () => {
    expect(emSegundos(12, 30)).toBeCloseTo(0.4, 9);
    expect(emFrames(emSegundos(12, 30), 30)).toBe(12);
    expect(emFrames(emSegundos(3, 30), 30)).toBe(3);
  });
});
```

- [ ] **Step 2: rodar o teste e conferir que falha**

Run: `cd instagram/remotion && npx vitest run tests/relogio.test.ts`
Expected: FALHA no carregamento — `Failed to resolve import "../src/motor/relogio"`.

- [ ] **Step 3: criar `src/motor/relogio.ts`**

```ts
// O RELOGIO. A unica conversao segundo <-> frame do motor.
//
// POR QUE UM ARQUIVO SO PARA DUAS CONTAS
//
// Antes de 01/10/2026 a conversao estava escrita em quatro lugares diferentes,
// cada um com o seu `Math.round(x * 30)`: `Raiz.tsx:25` e `:28`,
// `scripts/gerar-props.mjs`, e `agrupar.ts` recebia `fps` mas comparava contra
// `LEGENDA.duracaoMinFrames`, que e um literal de 30 fps. O 30 aparecia como
// numero em uns e como parametro em outros, e ninguem conseguia dizer de fora
// quais partes da peca respeitavam o fps da composicao.
//
// Com uma funcao so, a resposta e mecanica: respeita quem chama daqui.
//
// ARREDONDA, NAO TRUNCA. Truncar erra sempre para baixo, e o erro ACUMULA por
// cena: uma peca de 12 cenas sairia sistematicamente mais curta que o briefing.
// Arredondar erra para os dois lados e o erro nao se soma.
//
// FALHA ALTA EM VEZ DE NaN. `Math.round(x * undefined)` devolve NaN, e NaN
// atravessa `durationInFrames` sem reclamar ate o render sair vazio com exit 0 --
// a licao 3 do CLAUDE.md aplicada ao tempo. Entao aqui se lanca.

/** Converte segundos em frames inteiros, no fps dado. */
export function emFrames(segundos: number, fps: number): number {
  exigirFps(fps);
  if (!Number.isFinite(segundos)) {
    throw new Error(`emFrames: segundos tem que ser finito, recebi ${segundos}`);
  }
  if (segundos < 0) {
    throw new Error(
      `emFrames: segundo negativo (${segundos}). Tempo de briefing e contado do ` +
        'inicio DA CENA, entao nao existe evento antes do frame 0 dela.',
    );
  }
  return Math.round(segundos * fps);
}

/** A volta: quantos segundos sao `frames` frames no fps dado. */
export function emSegundos(frames: number, fps: number): number {
  exigirFps(fps);
  if (!Number.isFinite(frames)) {
    throw new Error(`emSegundos: frames tem que ser finito, recebi ${frames}`);
  }
  return frames / fps;
}

function exigirFps(fps: number): void {
  if (!Number.isFinite(fps)) {
    throw new Error(`fps tem que ser finito, recebi ${fps}`);
  }
  if (!Number.isInteger(fps)) {
    throw new Error(
      `fps tem que ser inteiro, recebi ${fps}. O container de video mente: ` +
        '`pl.mp4` declara 29,96 fps de media e o Remotion renderiza num fps ' +
        'INTEIRO declarado na composicao. Sonde a fonte para saber o que ela e, ' +
        'mas renderize num inteiro.',
    );
  }
  if (fps <= 0) {
    throw new Error(`fps tem que ser > 0, recebi ${fps}`);
  }
}
```

- [ ] **Step 4: rodar o teste e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/relogio.test.ts`
Expected: `Tests 6 passed (6)`.

- [ ] **Step 5: commit**

```bash
git add instagram/remotion/src/motor/relogio.ts instagram/remotion/tests/relogio.test.ts
git commit -m "$(cat <<'MSG'
Motor: o relogio, unica conversao segundo-frame do sistema

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 2: a cadência passa a sair de `fps`, e a 30 fps nada muda

O coração mecânico do plano. Hoje `TEMPO` está em **frames medidos a 30 fps** e nenhuma camada
de texto chama `useVideoConfig` — a 60 fps tudo encurtaria pela metade com exit 0. Esta tarefa
declara os tempos em **segundos**, deriva os frames de `fps`, e prova que **a 30 fps o pixel é
byte-idêntico**.

A prova de não-regressão é a mais forte que existe neste repositório: o still do mesmo frame
antes e depois tem o **mesmo sha256**. Laudo numérico já aprovou recorte visivelmente errado
aqui (lição do `CLAUDE.md`), então a igualdade de bytes é o que fecha a questão.

**Files:**
- Create: `instagram/remotion/src/motor/cadencia.ts`
- Create: `instagram/remotion/tests/cadencia.test.ts`
- Modify: `instagram/remotion/src/identidade/tokens.ts` (blocos `TEMPO` e `LEGENDA`)
- Modify: `instagram/remotion/src/motor/movimento.ts` (5 funções ganham um parâmetro)
- Modify: `instagram/remotion/src/motor/camadas/texto-forma.ts` (3 funções)
- Modify: `instagram/remotion/src/motor/camadas/TextoTela.tsx` (lê `useVideoConfig().fps`)
- Modify: `instagram/remotion/src/legenda/agrupar.ts:20-21`
- Modify: `instagram/remotion/tests/textotela.test.ts` (varredura mecânica — **51 `it`**, medido)
- Modify: `instagram/remotion/tests/manchete-props.test.ts` (**5 chamadas à mão**: `formaTextoTela` nas linhas 63, 186 e 211; `duracaoDaFrase` nas linhas 65 e 176 — medido)
- **NÃO modify:** `instagram/remotion/tests/agrupar.test.ts`. Medido: os 5 `it` dele usam só
  `agrupar(palavras, {fps: 30})` e o literal `10`, e `emFrames(0.333, 30)` = 10. Nenhuma das
  funções que ganham parâmetro aparece lá —
  `grep -c "duracaoDaFrase\|formaTextoTela\|progresso(\|duracaoComIrmaos\|duracaoDeIrmao\|atrasoDoIrmao\|fases(\|DURACAO_MINIMA\|TEMPO\.\|duracaoMinFrames" tests/agrupar.test.ts` = **0**. A versão
  anterior deste plano o listava como modificado e o punha na varredura: uma varredura no-op faz o
  executor procurar um erro que não existe

- [ ] **Step 1: gravar o still de referência ANTES de mudar qualquer linha**

Este passo é o portão da tarefa inteira. Sem ele não existe prova de que nada mudou.

**Pré-requisito: o Passo 0.5 tem que estar feito.** Ele é o controle: prova que o still é
byte-reproduzível nesta máquina. Sem o controle, um `MUDOU` no Step 15 é ambíguo entre regressão da
migração e não-determinismo do render, e a prova da tarefa inteira vira opinião.

Run:
```
cd instagram/remotion
npx remotion still src/index.ts Reel out/antes-f300.png --frame=300 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
npx remotion still src/index.ts Reel out/antes-f120.png --frame=120 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
node -e "const c=require('node:crypto'),f=require('node:fs');for(const n of ['antes-f300','antes-f120'])console.log(n, c.createHash('sha256').update(f.readFileSync('out/'+n+'.png')).digest('hex'))"
```
Expected: dois sha256 impressos. **Anote os dois.** O frame 120 está dentro da cena da manchete
(`manchete.inicioFrame` 104 − `cortarAntesFrames` 34 = frame 70 da peça, e
`duracaoDaFrase('SUA PRÓPRIA MARCA DE CAFÉ')` = 60 frames a 30 fps → a cena vai do frame 70 ao
129), então ele exercita stagger, entrada, hold e push. O 300 exercita só legenda e vídeo.

- [ ] **Step 2: escrever o teste que falha**

Criar `instagram/remotion/tests/cadencia.test.ts`:

```ts
import {describe, expect, it} from 'vitest';
import {cadencia, TEMPO_S} from '../src/motor/cadencia';

describe('cadencia', () => {
  it('a 30 fps reproduz EXATAMENTE a tabela que estava chumbada em tokens.ts', () => {
    // Os valores de antes de 01/10/2026, lidos de src/identidade/tokens.ts:16-23:
    //   entrada 12 · stagger 3 · holdFinal 12  -> DURACAO_MINIMA = 36
    // Se este teste falhar, a migracao para segundos MUDOU a peca a 30 fps, e o
    // pixel vai mudar junto.
    const c = cadencia(30);
    expect(c.entrada).toBe(12);
    expect(c.stagger).toBe(3);
    expect(c.holdFinal).toBe(12);
    expect(c.duracaoMinima).toBe(36);
    expect(c.fps).toBe(30);
  });

  it('duracaoMinima e SEMPRE entrada + holdFinal + entrada, em todo fps', () => {
    // E a espinha do portao de ritmo: 1,2 s de piso por elemento. Derivada, nao
    // escolhida -- se ela deixar de ser a soma, o portao passa a medir outra coisa.
    for (const fps of [24, 25, 30, 50, 60]) {
      const c = cadencia(fps);
      expect(c.duracaoMinima).toBe(c.entrada + c.holdFinal + c.entrada);
    }
  });

  it('a 60 fps os frames dobram e a DURACAO EM SEGUNDOS nao muda', () => {
    const c = cadencia(60);
    expect(c.entrada).toBe(24);
    expect(c.stagger).toBe(6);
    expect(c.holdFinal).toBe(24);
    expect(c.duracaoMinima).toBe(72);
    // 72 frames a 60 fps = 1,2 s = os 36 frames a 30 fps. E o ponto inteiro.
    expect(c.duracaoMinima / 60).toBeCloseTo(cadencia(30).duracaoMinima / 30, 9);
  });

  it('o que NAO e tempo nao escala: expoente de saida, overshoot e a curva', () => {
    const a = cadencia(30);
    const b = cadencia(60);
    expect(a.saidaExpoente).toBe(b.saidaExpoente);
    expect(a.overshoot).toBe(b.overshoot);
    expect(a.saidaExpoente).toBe(2.4);
    expect(a.overshoot).toBe(0.03);
  });

  it('TEMPO_S declara os tempos em SEGUNDOS, e os segundos batem com os frames medidos', () => {
    expect(TEMPO_S.entrada).toBeCloseTo(12 / 30, 9);
    expect(TEMPO_S.stagger).toBeCloseTo(3 / 30, 9);
    expect(TEMPO_S.holdFinal).toBeCloseTo(12 / 30, 9);
  });

  it('herda a recusa do relogio: fps fracionario nao passa', () => {
    expect(() => cadencia(29.97)).toThrow(/inteiro/);
  });
});
```

- [ ] **Step 3: rodar o teste e conferir que falha**

Run: `cd instagram/remotion && npx vitest run tests/cadencia.test.ts`
Expected: FALHA — `Failed to resolve import "../src/motor/cadencia"`.

- [ ] **Step 4: trocar `TEMPO` por segundos em `src/identidade/tokens.ts`**

Substituir o bloco das linhas 15–23 inteiro por:

```ts
// Tempos em SEGUNDOS. Medidos, nao escolhidos -- e a conversao para frame e
// `emFrames(s, fps)` de `motor/relogio.ts`, uma vez, em `motor/cadencia.ts`.
//
// POR QUE SEGUNDOS, DEPOIS DE TER SIDO FRAMES
//
// Ate 01/10/2026 estes numeros eram frames medidos a 30 fps, e nenhuma camada de
// texto chamava `useVideoConfig`. A 60 fps cada entrada, saida, hold e stagger
// duraria METADE do medido e a peca sairia inteira, com exit 0 e sem aviso.
//
// Os segundos abaixo foram obtidos dividindo os frames medidos por 30, e
// `tests/cadencia.test.ts` prova que `cadencia(30)` devolve exatamente os frames
// de antes: 12 / 3 / 12, com DURACAO_MINIMA 36. A migracao nao muda a peca a
// 30 fps -- so passa a estar certa nos outros.
export const TEMPO = {
  entradaS: 0.4,        // eram 12 frames; faixa util 8-18 frames a 30 fps
  saidaExpoente: 2.4,   // aceleracao de saida t^2.4 -- adimensional, nao escala
  overshoot: 0.03,      // 2-4% -- adimensional, nao escala
  staggerS: 0.1,        // eram 3 frames; faixa util 2-4 frames a 30 fps
  holdFinalS: 0.4,      // eram 12 frames; faixa 8-18
  pousoEasing: 'cubic-bezier(0.20,0.80,0.20,1.00)',
} as const;
```

E no bloco `LEGENDA` (linhas 37–44), trocar a linha do piso:

```ts
  // Piso de leitura de um bloco, em SEGUNDOS. Era `duracaoMinFrames: 10`, um
  // literal de 30 fps aplicado DENTRO de uma funcao que ja recebia fps
  // (`agrupar.ts:20`). 0,333 s = 10 frames a 30, 8 a 24, 20 a 60.
  duracaoMinSegundos: 0.333,
```

- [ ] **Step 5: criar `src/motor/cadencia.ts`**

```ts
// A CADENCIA: a tabela de tempos da marca, em FRAMES, para um fps.
//
// E o unico lugar do motor que converte os tokens de tempo. Quem precisa de
// tempo recebe uma `Cadencia` pronta e nunca chama `emFrames` por conta propria
// -- assim existe um ponto so para conferir, e `cadencia(30)` e um teste de
// nao-regressao do motor inteiro.
//
// O PARAMETRO E OBRIGATORIO, E ISSO E DE PROPOSITO.
//
// Poderia ter default `cadencia(30)`. Nao tem, porque um default aqui devolveria
// exatamente o bug que esta tarefa conserta: uma camada que esquecesse de passar
// a cadencia da composicao continuaria desenhando no tempo de 30 fps, com exit 0.
// Sendo obrigatorio, `npm run tsc` enumera todo ponto de chamada que ficou para
// tras. O compilador e o portao.

import {TEMPO} from '../identidade/tokens';
import {emFrames} from './relogio';

export type Cadencia = {
  /** o fps de que esta tabela saiu */
  fps: number;
  /** frames de entrada de um elemento */
  entrada: number;
  /** frames entre elementos irmaos */
  stagger: number;
  /** frames em que o elemento fica cheio depois de o ultimo irmao entrar */
  holdFinal: number;
  /** entrada + holdFinal + entrada. Abaixo disso as pontas comprimem. */
  duracaoMinima: number;
  /** adimensional: nao escala com fps */
  saidaExpoente: number;
  /** adimensional: nao escala com fps */
  overshoot: number;
};

/** Os tempos da marca em segundos, expostos para quem precisa da unidade crua. */
export const TEMPO_S = {
  entrada: TEMPO.entradaS,
  stagger: TEMPO.staggerS,
  holdFinal: TEMPO.holdFinalS,
} as const;

export function cadencia(fps: number): Cadencia {
  const entrada = emFrames(TEMPO.entradaS, fps);
  const stagger = emFrames(TEMPO.staggerS, fps);
  const holdFinal = emFrames(TEMPO.holdFinalS, fps);
  return {
    fps,
    entrada,
    stagger,
    holdFinal,
    duracaoMinima: entrada + holdFinal + entrada,
    saidaExpoente: TEMPO.saidaExpoente,
    overshoot: TEMPO.overshoot,
  };
}
```

- [ ] **Step 6: rodar o teste da cadência e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/cadencia.test.ts`
Expected: `Tests 6 passed (6)`.

- [ ] **Step 7: fazer `movimento.ts` receber a cadência**

Em `src/motor/movimento.ts`: trocar a linha 34 (`import {PUSH, TEMPO} from ...`) por

```ts
import {PUSH, TEMPO} from '../identidade/tokens';
import type {Cadencia} from './cadencia';
```

Apagar a linha `export const DURACAO_MINIMA = TEMPO.entrada + TEMPO.holdFinal + TEMPO.entrada;`
(era a linha 122) e o comentário dela, e pôr no lugar:

```ts
// `DURACAO_MINIMA` era uma constante de modulo derivada de frames a 30 fps.
// Agora ela e `c.duracaoMinima`, porque depende do fps da composicao -- ver
// `motor/cadencia.ts`. A soma continua sendo entrada + holdFinal + entrada.
```

E substituir as cinco funções que leem tempo, mantendo o corpo e só trocando a fonte dos
números:

```ts
export function fases(duracao: number, c: Cadencia): Fases {
  const d = Math.max(0, Math.floor(duracao));
  if (d === 0) return {entrada: 0, hold: 0, saida: 0};
  const ponta = Math.min(c.entrada, Math.floor(d / 3));
  return {entrada: ponta, hold: d - 2 * ponta, saida: ponta};
}

export function progresso(frame: number, janela: Janela, c: Cadencia): Estado {
  const {inicio, duracao} = janela;
  const t = frame - inicio;

  if (t < 0) return {fase: 'antes', presenca: 0, escala: 1 + c.overshoot};
  if (t >= duracao) return {fase: 'depois', presenca: 0, escala: 1 - c.overshoot};

  const f = fases(duracao, c);
  const inicioSaida = duracao - f.saida;

  const pEntrada = f.entrada === 0 ? 1 : Math.min(1, t / f.entrada);
  const entrada = POUSO(pEntrada);

  // O `+1` normaliza pelo ULTIMO FRAME DESENHADO (Tarefa 2 do plano de
  // qualidade). Nao mexa nele aqui.
  const pSaida =
    f.saida === 0 || t < inicioSaida
      ? 0
      : Math.min(1, (t - inicioSaida + 1) / f.saida);
  const queda = Math.pow(pSaida, c.saidaExpoente);

  const fase: Fase = t < f.entrada ? 'entrada' : t < inicioSaida ? 'hold' : 'saida';

  return {
    fase,
    presenca: Math.min(entrada, 1 - queda),
    escala: 1 + c.overshoot * (1 - entrada) - c.overshoot * queda,
  };
}

export function atrasoDoIrmao(indice: number, c: Cadencia): number {
  return Math.max(0, Math.floor(indice)) * c.stagger;
}

export function janelasDeIrmaos(
  quantidade: number,
  base: Janela,
  c: Cadencia,
): Janela[] {
  return Array.from({length: Math.max(0, Math.floor(quantidade))}, (_, i) => ({
    inicio: base.inicio + atrasoDoIrmao(i, c),
    duracao: base.duracao,
  }));
}

export function duracaoComIrmaos(
  quantidade: number,
  duracao: number,
  c: Cadencia,
): number {
  const n = Math.max(1, Math.floor(quantidade));
  return duracao + atrasoDoIrmao(n - 1, c);
}

export function duracaoDeIrmao(quantidade: number, c: Cadencia): number {
  const n = Math.max(1, Math.floor(quantidade));
  return c.duracaoMinima + atrasoDoIrmao(n - 1, c);
}
```

`bezierDeCss`, `POUSO` e `push` **não mudam** — nenhum dos três lê tempo em frames.

- [ ] **Step 8: fazer `texto-forma.ts` receber a cadência**

Em `src/motor/camadas/texto-forma.ts`, acrescentar ao import de `../movimento` o tipo:

```ts
import {atrasoDoIrmao, duracaoComIrmaos, duracaoDeIrmao} from '../movimento';
import type {Cadencia} from '../cadencia';
```

Substituir as três funções que leem tempo:

```ts
export function duracaoPorPalavra(texto: string, c: Cadencia): number {
  return duracaoDeIrmao(contarPalavras(texto), c);
}

export function duracaoDaFrase(
  texto: string,
  c: Cadencia,
  duracao: number = duracaoPorPalavra(texto, c),
): number {
  const n = contarPalavras(texto);
  if (n === 0) return 0;
  return duracaoComIrmaos(n, duracao, c);
}
```

E em `formaTextoTela`, acrescentar `cadencia` ao objeto de parâmetros — **campo nomeado
obrigatório**, para que `tsc` aponte os 21 pontos de chamada de teste um por um:

```ts
export function formaTextoTela({
  texto,
  modo,
  zonas,
  papel = 'manchete',
  palavraAcento,
  cadencia,
}: {
  texto: string;
  modo: Modo;
  zonas: Zonas;
  papel?: PapelTexto;
  /** indice da UNICA palavra que recebe `COR.acento`. Fora da faixa = nenhuma. */
  palavraAcento?: number;
  /** de `cadencia(useVideoConfig().fps)`. Obrigatorio: sem ele o stagger volta a
   *  ser 3 frames em qualquer fps. */
  cadencia: Cadencia;
}): Forma {
```

E na montagem das palavras, trocar `atrasoDoIrmao(irmao)` por `atrasoDoIrmao(irmao, cadencia)`.

- [ ] **Step 9: fazer `TextoTela.tsx` ler o fps da composição**

Em `src/motor/camadas/TextoTela.tsx`: trocar a linha 49 e acrescentar o import da cadência:

```tsx
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
```
```tsx
import {cadencia} from '../cadencia';
```

E dentro do componente, substituir das linhas 90 até 111 (de `const frame` até a linha do
`conjunto`) por:

```tsx
  const frame = useCurrentFrame();
  // A CADENCIA VEM DA COMPOSICAO, nao de uma constante. Este `useVideoConfig` e
  // a razao pela qual a peca passa a estar certa em qualquer fps: antes de
  // 01/10/2026 nenhuma camada de texto chamava esta funcao, e a 60 fps a
  // manchete inteira durava metade.
  const {fps} = useVideoConfig();
  const c = React.useMemo(() => cadencia(fps), [fps]);
  const t = frame - inicioFrame;

  const forma = React.useMemo(
    () => formaTextoTela({texto, modo, zonas, papel, palavraAcento, cadencia: c}),
    [texto, modo, zonas, papel, palavraAcento, c],
  );

  if (forma.palavras.length === 0) return null;

  const duracaoPalavra = duracaoFrames ?? duracaoDeIrmao(forma.palavras.length, c);
  const duracaoCena = duracaoComIrmaos(forma.palavras.length, duracaoPalavra, c);
  if (t < 0 || t >= duracaoCena) return null;

  const conjunto = progresso(t, {inicio: 0, duracao: duracaoCena}, c);
```

E na chamada de `progresso` de dentro do `.map` das palavras (era a linha 160), passar `c`:

```tsx
                const e = progresso(t, {
                  inicio: p.atrasoFrames,
                  duracao: duracaoPalavra,
                }, c);
```

- [ ] **Step 10: consertar `src/legenda/agrupar.ts`, que já recebia fps e ignorava**

Trocar as linhas 20–21 por:

```ts
    // O piso de leitura vem em SEGUNDOS e e convertido com o fps que esta
    // funcao JA recebia. Antes de 01/10/2026 comparava com
    // `LEGENDA.duracaoMinFrames`, um literal de 30 fps dentro de uma funcao
    // parametrizada por fps -- a incoerencia mais barata de achar do motor.
    const pisoFrames = emFrames(LEGENDA.duracaoMinSegundos, fps);
    if (b.fimFrame - b.inicioFrame < pisoFrames) {
      b.fimFrame = b.inicioFrame + pisoFrames;
    }
```

E acrescentar ao topo do arquivo, depois do import de `LEGENDA`:

```ts
import {emFrames} from '../motor/relogio';
```

- [ ] **Step 11: rodar o typecheck e deixar o compilador enumerar o que falta**

Run: `cd instagram/remotion && npm run tsc`
Expected: uma lista de erros `TS2554: Expected 2 arguments, but got 1` (e `Expected 3, but got
2`) em `tests/textotela.test.ts`, `tests/agrupar.test.ts` e nos `.tsx` que ainda chamam as
funções antigas — **isso é o portão funcionando**, não uma falha do plano. Anote quantos erros
são; o Step 13 tem que zerar a lista.

- [ ] **Step 12: varrer os testes com o casamento mecânico**

Acrescentar no topo de `tests/textotela.test.ts`, depois dos imports existentes:

```ts
import {cadencia} from '../src/motor/cadencia';

// A cadencia de 30 fps, que e o fps em que TODOS os numeros deste arquivo foram
// medidos. Passar `C` em vez de deixar um default e o que garante que o teste
// continua medindo o mesmo tempo depois de a cadencia virar parametro.
const C = cadencia(30);
```

Depois rodar a varredura mecânica — ela cobre os casos de um argumento, que são a maioria. **Só
`textotela.test.ts`**: medido, `agrupar.test.ts` não tem nenhuma ocorrência para varrer, e
`manchete-props.test.ts` tem as cinco chamadas com objeto ou expressão aninhada, que o regex não
casa — elas são resolvidas à mão no Step 13.

```bash
cd instagram/remotion
node -e "
const fs=require('node:fs');
for (const arq of ['tests/textotela.test.ts']) {
  let s=fs.readFileSync(arq,'utf8');
  s=s.replace(/\bDURACAO_MINIMA\b/g,'C.duracaoMinima');
  s=s.replace(/\batrasoDoIrmao\(([^()]*)\)/g,'atrasoDoIrmao(\$1, C)');
  s=s.replace(/\bduracaoDeIrmao\(([^()]*)\)/g,'duracaoDeIrmao(\$1, C)');
  s=s.replace(/\bduracaoPorPalavra\(([^()]*)\)/g,'duracaoPorPalavra(\$1, C)');
  s=s.replace(/\bfases\(([^()]*)\)/g,'fases(\$1, C)');
  fs.writeFileSync(arq,s);
  console.log('varrido', arq);
}
"
```

`progresso`, `duracaoComIrmaos`, `duracaoDaFrase` e `formaTextoTela` **não** entram na varredura
porque os argumentos deles contêm parênteses e chaves aninhados, e um regex que os tentasse
casar erraria silenciosamente. Eles são resolvidos à mão no passo seguinte, com o compilador
apontando cada um.

- [ ] **Step 13: fechar a lista do compilador à mão, um erro por vez**

Run: `cd instagram/remotion && npm run tsc`

**Cinco desses erros estão em `tests/manchete-props.test.ts`, e eles são medidos, não previstos:**
linhas **63** (`formaTextoTela({texto: vazio, modo, zonas: z})`), **65** (`duracaoDaFrase(vazio)`),
**176** (`duracaoDaFrase(m!.texto)`), **186** e **211** (`formaTextoTela({texto: m!.texto, modo:
m!.modo, zonas: z})`). Acrescente ao topo daquele arquivo o mesmo `const C = cadencia(30);` do Step
12 — os números dele também foram todos medidos a 30 fps.

Para cada erro restante, a correção é sempre uma das quatro, e nenhuma muda número:

| erro | correção |
|---|---|
| `progresso(f, j)` | `progresso(f, j, C)` |
| `duracaoComIrmaos(n, d)` | `duracaoComIrmaos(n, d, C)` |
| `duracaoDaFrase(t)` | `duracaoDaFrase(t, C)` |
| `duracaoDaFrase(t, d)` | `duracaoDaFrase(t, C, d)` — a cadência entra no **meio** |
| `formaTextoTela({...})` | acrescentar `cadencia: C` ao objeto |
| `TEMPO.entrada` / `TEMPO.stagger` / `TEMPO.holdFinal` num teste | `C.entrada` / `C.stagger` / `C.holdFinal` |
| `LEGENDA.duracaoMinFrames` num teste | `emFrames(LEGENDA.duracaoMinSegundos, 30)` |

Repetir `npm run tsc` até a saída ficar **vazia**. Nenhuma asserção numérica muda: a 30 fps
`C.entrada` é 12, `C.stagger` é 3, `C.holdFinal` é 12 e `C.duracaoMinima` é 36 — exatamente os
valores que os testes mediram.

- [ ] **Step 14: rodar a suíte inteira**

Run: `cd instagram/remotion && npx vitest run`
Expected: **BASE + 3 (do §0) + 12 (relógio e cadência)** testes passando, e **nenhum teste
antigo alterado no valor esperado**. Se algum teste antigo falhar, a migração mudou o tempo a
30 fps — pare e compare o valor com a tabela do Step 13 antes de "ajustar o teste".

- [ ] **Step 15: CONFERÊNCIA NO PIXEL — o sha256 tem que ser o mesmo**

Este é o passo que nenhum teste unitário faz, porque teste unitário não renderiza.

Run:
```
cd instagram/remotion
npx remotion still src/index.ts Reel out/depois-f300.png --frame=300 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
npx remotion still src/index.ts Reel out/depois-f120.png --frame=120 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
node -e "const c=require('node:crypto'),f=require('node:fs');const h=n=>c.createHash('sha256').update(f.readFileSync('out/'+n+'.png')).digest('hex');for(const n of ['f300','f120'])console.log(n, h('antes-'+n)===h('depois-'+n)?'IDENTICO':'MUDOU '+h('antes-'+n)+' -> '+h('depois-'+n))"
```
Expected: `f300 IDENTICO` e `f120 IDENTICO`.

Se `MUDOU`: **abra os dois PNG e olhe** antes de qualquer coisa. A migração para segundos não
tem direito de mover um pixel a 30 fps; se moveu, algum `Math.round` mudou de lado e o lugar de
descobrir isso é a tabela do Step 2 de `cadencia.test.ts`, não o still.

- [ ] **Step 16: commit**

```bash
git add instagram/remotion/src instagram/remotion/tests
git commit -m "$(cat <<'MSG'
Motor: cadencia derivada de fps, tokens de tempo em segundos

A 30 fps o still do frame 120 e do 300 tem o mesmo sha256 de antes.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 3: papel de evento e família de tipografia, e o `etiqueta` que explode

Medido nesta sessão: `formaTextoTela({texto: 'SERIE 10', papel: 'etiqueta', …})` lança
`TypeError: Cannot read properties of undefined (reading 'x')`, porque `PapelTexto` é
`'manchete' | 'dado'` (`texto-forma.ts:49`) e é indexado **direto** em `GLIFOS`, cujas chaves são
`manchete`, `corpo`, `dado`. O mapa papel→família é **obrigatório, não cosmético**.

Esta tarefa também é onde nascem as duas tabelas que a spec decidiu tirar do briefing (C4 e C2):
cadência derivada do papel e pista padrão por papel. Um botão que o briefing possa girar sem
saber avaliar produz inconsistência silenciosa entre peças da mesma série — é a lição 8 do
`CLAUDE.md` aplicada a tempo em vez de cenário.

**E é aqui que a cadência CHEGA AO RENDER.** A versão anterior deste plano criava
`CADENCIA_DO_PAPEL`, usava a tabela no compilador **só para contar frames**, e nenhum passo tocava o
escalonamento de `texto-forma.ts` — que continuava incrementando o índice de irmão por **palavra** em
todo papel. A divergência é medível: a etiqueta `MEDEIROS 1250 M` tem cadência `bloco`, logo 1 irmão,
logo `duracaoDeIrmao(1)` = **36** frames no plano; `TextoTela` recebia 36 e recalculava
`duracaoComIrmaos(3, 36, c)` = 36 + 2×3 = **42**, porque contava as 3 palavras. **Seis frames entre o
plano e o pixel** — e os portões `abaixo-do-piso` e `evento-estoura-cena` mediriam um número que a
tela não usa. Os Steps 5 e 6 fecham isso.

**Files:**
- Create: `instagram/remotion/src/motor/pista.ts` (os NOMES das pistas, os conflitos e o tipo `Encaixe`; a geometria é a Tarefa 4)
- Create: `instagram/remotion/src/motor/evento.ts`
- Create: `instagram/remotion/tests/evento.test.ts`
- Modify: `instagram/remotion/src/motor/camadas/texto-forma.ts` (tipo `PapelTexto`, `Forma`, indexação por família, **e o escalonamento por cadência**)
- Modify: `instagram/remotion/src/motor/camadas/TextoTela.tsx` (lê `forma.familia` e `forma.irmaos`)

**Por que `pista.ts` nasce AQUI, e não na Tarefa 4.** A versão anterior punha
`import type {Pista} from './layout';` dentro de `evento.ts`, nesta tarefa — e `Pista` só era criado
na Tarefa 4. O `npm run tsc` sem saída do Step final era **impossível de satisfazer**: a ordem estava
invertida. O conserto não é adiantar a Tarefa 4, é separar o que cada coisa precisa: o **nome** de uma
pista não depende de geometria nenhuma, então nasce num arquivo sem dependência alguma, aqui, e a
Tarefa 4 acrescenta a geometria ao mesmo arquivo.

- [ ] **Step 1: escrever o teste que falha**

Criar `instagram/remotion/tests/evento.test.ts`:

```ts
import {describe, expect, it} from 'vitest';
import {
  CADENCIA_DO_PAPEL,
  FAMILIA_DO_PAPEL,
  PAPEIS_DE_EVENTO,
  PISTA_PADRAO,
} from '../src/motor/evento';
import {CONFLITO_DE_PISTA, PISTAS} from '../src/motor/pista';
import {cadencia} from '../src/motor/cadencia';
import {formaTextoTela} from '../src/motor/camadas/texto-forma';
import {layout} from '../src/motor/layout';

const C = cadencia(30);

describe('papel de evento', () => {
  it('os tres papeis de evento tem familia, cadencia e pista padrao', () => {
    // Nenhuma tabela pode ter buraco: um papel sem familia e o TypeError medido
    // em 30/09/2026 (`Cannot read properties of undefined (reading 'x')`).
    // `ENCAIXE_PADRAO` NAO esta aqui porque encaixe deixou de ser escolha: ele e
    // derivado de (pista, formato) na Tarefa 4 -- spec §3.4.2.
    for (const papel of PAPEIS_DE_EVENTO) {
      expect(FAMILIA_DO_PAPEL[papel]).toBeDefined();
      expect(CADENCIA_DO_PAPEL[papel]).toBeDefined();
      expect(PISTAS).toContain(PISTA_PADRAO[papel]);
      expect(CONFLITO_DE_PISTA[PISTA_PADRAO[papel]]).toBeDefined();
    }
  });

  it('nenhum papel de evento tem `rodape` por padrao: o rodape e da legenda', () => {
    // A pista `rodape` e a caixa da camada `Legenda`. Um evento ali cairia sobre
    // a fala, que e a camada mais vista da peca.
    for (const papel of PAPEIS_DE_EVENTO) {
      expect(PISTA_PADRAO[papel]).not.toBe('rodape');
    }
  });

  it('etiqueta usa a familia do dado: mono resolve rotulo e carimbo', () => {
    expect(FAMILIA_DO_PAPEL.etiqueta).toBe('dado');
    expect(FAMILIA_DO_PAPEL.manchete).toBe('manchete');
    expect(FAMILIA_DO_PAPEL.dado).toBe('dado');
    // `legenda` esta na tabela porque nomeia a familia da CAMADA Legenda, e NAO
    // porque e papel de evento -- ver o teste seguinte.
    expect(FAMILIA_DO_PAPEL.legenda).toBe('corpo');
  });

  it('legenda NAO e papel de evento', () => {
    // A legenda e camada de PECA, fora da TransitionSeries: se ela fosse evento
    // de cena, na janela de crossfade duas legendas com textos diferentes
    // ficariam no ar ao mesmo tempo.
    expect(PAPEIS_DE_EVENTO).not.toContain('legenda');
  });

  it('a cadencia do dado e por LINHA, e isso vem de medicao', () => {
    // `duracaoDaFrase('R$ 39,90')` trata 'R$' e '39,90' como dois irmaos: um
    // cartao de preco que revela 'R$' e o numero 3 frames depois le como
    // defeito. Cada linha de um dado e um CAMPO.
    expect(CADENCIA_DO_PAPEL.dado).toBe('linha');
    expect(CADENCIA_DO_PAPEL.manchete).toBe('palavra');
    expect(CADENCIA_DO_PAPEL.etiqueta).toBe('bloco');
  });

  it('formaTextoTela com papel etiqueta NAO explode mais, e sai em mono', () => {
    // Este e o TypeError medido. Antes: Cannot read properties of undefined.
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 9 / 16});
    const f = formaTextoTela({
      texto: 'SERIE 10',
      modo: 'sobreImagem',
      zonas: z,
      papel: 'etiqueta',
      cadencia: C,
    });
    expect(f.familia).toBe('dado');
    expect(f.corpo).toBeGreaterThan(0);
    expect(f.palavras.length).toBe(2);
  });

  it('a Forma declara a FAMILIA, nao o papel, para o .tsx nao ter que mapear', () => {
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 9 / 16});
    const f = formaTextoTela({
      texto: 'CAFE',
      modo: 'cartela',
      zonas: z,
      papel: 'manchete',
      cadencia: C,
    });
    expect(f.papel).toBe('manchete');
    expect(f.familia).toBe('manchete');
  });

  it('A CADENCIA CHEGA AO ESCALONAMENTO: manchete por palavra, dado por linha, etiqueta em bloco', () => {
    // O FURO QUE ISTO FECHA: `CADENCIA_DO_PAPEL` era criada, usada pelo compilador
    // para contar frames, e NUNCA chegava ao render -- `atrasoDoIrmao(irmao)` de
    // `texto-forma.ts` incrementava `irmao` por PALAVRA em todo papel. A etiqueta
    // `MEDEIROS 1250 M` recebia 36 frames do plano e desenhava 42.
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 9 / 16});
    const comum = {modo: 'cartela' as const, zonas: z, cadencia: C};

    // manchete: um irmao por PALAVRA, atraso crescente
    const m = formaTextoTela({...comum, texto: 'UM DOIS TRES', papel: 'manchete'});
    expect(m.irmaos).toBe(3);
    expect(m.palavras.map((p) => p.atrasoFrames)).toEqual([0, C.stagger, 2 * C.stagger]);

    // etiqueta: UM irmao, todas as palavras entram JUNTAS. Um carimbo nao tem
    // ritmo interno: ou esta no quadro ou nao esta.
    const e = formaTextoTela({...comum, texto: 'MEDEIROS 1250 M', papel: 'etiqueta'});
    expect(e.irmaos).toBe(1);
    expect(new Set(e.palavras.map((p) => p.atrasoFrames))).toEqual(new Set([0]));

    // dado: um irmao por LINHA. Palavras da mesma linha compartilham o atraso.
    const d = formaTextoTela({...comum, texto: 'R$ 39,90', papel: 'dado'});
    expect(d.irmaos).toBe(d.linhas.length);
    for (const p of d.palavras) {
      expect(p.atrasoFrames).toBe(C.stagger * p.linha);
    }
  });

  it('a duracao do EVENTO sai de forma.irmaos, nao do numero de palavras', () => {
    // E o par do teste acima, do outro lado: se `TextoTela` continuar usando
    // `palavras.length`, o plano e a tela discordam em 6 frames na etiqueta.
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 9 / 16});
    const e = formaTextoTela({
      texto: 'MEDEIROS 1250 M',
      modo: 'cartela',
      zonas: z,
      papel: 'etiqueta',
      cadencia: C,
    });
    expect(e.palavras.length).toBe(3);
    expect(e.irmaos).toBe(1);
    expect(duracaoDeIrmao(e.irmaos, C)).toBe(36);
    expect(duracaoComIrmaos(e.irmaos, duracaoDeIrmao(e.irmaos, C), C)).toBe(36);
  });
});
```

E ao topo do arquivo de teste, junto dos outros imports:

```ts
import {duracaoComIrmaos, duracaoDeIrmao} from '../src/motor/movimento';
```

- [ ] **Step 2: rodar o teste e conferir que falha**

Run: `cd instagram/remotion && npx vitest run tests/evento.test.ts`
Expected: FALHA — `Failed to resolve import "../src/motor/evento"` (e `../src/motor/pista`).

- [ ] **Step 3: criar `src/motor/pista.ts` — só os nomes, nenhuma geometria**

```ts
// AS PISTAS: os nomes, os conflitos e o tipo do encaixe. SEM GEOMETRIA.
//
// A GEOMETRIA ENTRA NA TAREFA 4, NESTE MESMO ARQUIVO
//
// Este arquivo nasce sem UM import de proposito. `motor/evento.ts` precisa do tipo
// `Pista` para declarar `PISTA_PADRAO`, e se o tipo morasse em `layout.ts` a
// Tarefa 3 dependeria da Tarefa 4 -- que foi exatamente o erro de ordem da versao
// anterior deste plano (`npm run tsc` impossivel de passar). Nome nao depende de
// caixa; entao o nome vem primeiro, sozinho.
//
// O QUE E UMA PISTA
//
// Uma faixa horizontal EXCLUSIVA de uma coluna de texto. Duas camadas na mesma
// pista, no mesmo frame, sao recusa -- e a recusa e do portao de ritmo, nao do
// desenho, porque ela so e decidivel depois da conversao para frames.
//
// E POR QUE ISSO EXISTE: medido em 01/10/2026, nas caixas cruas que `layout()`
// devolve com fonte 9:16, a caixa da manchete e a da legenda se INTERSECTAM em
// 90,20 px no eixo x no 1:1, 102,35 px no 4:5 e 122,56 px no 16:9 -- 15,67%,
// 14,07% e 22,26% da area da caixa da legenda. No 9:16 a intersecao e ZERO. O
// defeito e dos formatos em que o video vira coluna, e a causa mecanica esta em
// `layout.ts:68-73` (ver Tarefa 4).

/** As quatro pistas horizontais em que uma camada de texto pode morar. */
export const PISTAS = ['topo', 'principal', 'rodape', 'tela'] as const;
export type Pista = (typeof PISTAS)[number];

/** As pistas que um EVENTO pode declarar. `rodape` e so da camada `Legenda`. */
export const PISTAS_DE_EVENTO = ['topo', 'principal', 'tela'] as const;
export type PistaDeEvento = (typeof PISTAS_DE_EVENTO)[number];

/**
 * A forma da caixa de um texto. DERIVADA de (pista, formato), nunca declarada --
 * ver `encaixe()` na Tarefa 4 e a spec §3.4.2.
 *
 * Eram tres valores no briefing, como lista de preferencia. Sairam de la porque
 * `faixa` x `coluna` nao e escolha, e consequencia do formato: no 9:16 a sobra ao
 * lado do video e 0,00 px (medido), logo `encaixe: ['coluna']` ali e
 * insatisfazivel -- um campo que o motor nao pode honrar e o HTTP 200 que ignora
 * o parametro, licao 3 do CLAUDE.md.
 */
export const ENCAIXES = ['faixa', 'coluna', 'cartela'] as const;
export type Encaixe = (typeof ENCAIXES)[number];

/**
 * Que pistas cada pista bloqueia.
 *
 * `tela` e a cartela: ela ocupa o quadro e portanto conflita com `topo` e
 * `principal`. NAO conflita com `rodape`, porque a legenda continua correndo por
 * cima do terra chapado da cartela -- a escolha que `PecaVideo.tsx:115-120` ja
 * defendeu por escrito: cartela por cima de tudo apagaria a legenda por dois
 * segundos e quebraria a continuidade de leitura.
 */
export const CONFLITO_DE_PISTA: Record<Pista, readonly Pista[]> = {
  topo: ['topo', 'tela'],
  principal: ['principal', 'tela'],
  rodape: ['rodape'],
  tela: ['tela', 'topo', 'principal'],
};
```

- [ ] **Step 4: criar `src/motor/evento.ts`**

```ts
// AS TABELAS DE PAPEL. Puras, sem React e sem remotion.
//
// Um evento de texto declara o PAPEL dele, e o papel decide tres coisas que o
// briefing NAO escolhe: a familia de tipografia, a cadencia de revelacao e a
// pista onde ele mora por padrao.
//
// POR QUE O BRIEFING NAO ESCOLHE
//
// Um botao que quem escreve o briefing pode girar sem saber avaliar produz
// inconsistencia silenciosa entre pecas da MESMA serie -- e a licao 8 do
// CLAUDE.md (coesao de serie) aplicada a tempo em vez de cenario. Tabela por
// papel da coesao de graca: toda manchete de toda peca revela por palavra.

import type {Papel} from '../identidade/tipografia';
// `Pista` vem de `./pista`, que nao importa NADA -- nem `layout`. Se viesse de
// `layout.ts`, este arquivo dependeria da geometria da Tarefa 4 e o `tsc` desta
// tarefa nao passaria. Os dois imports sao `import type`, que o transpilador
// apaga: nenhum efeito de modulo entra aqui, e e por isso que `esquema.ts` pode
// importar deste arquivo sem puxar `loadFont` para dentro do vitest.
import type {Pista} from './pista';

/** Os papeis que um EVENTO de cena pode ter. `legenda` nao esta aqui. */
export const PAPEIS_DE_EVENTO = ['manchete', 'dado', 'etiqueta'] as const;
export type PapelEvento = (typeof PAPEIS_DE_EVENTO)[number];

/**
 * Papel de evento (e a legenda) -> familia de tipografia.
 *
 * O MAPA E OBRIGATORIO, NAO COSMETICO. Medido em 30/09/2026:
 * `formaTextoTela({papel: 'etiqueta', ...})` lancava
 * `TypeError: Cannot read properties of undefined (reading 'x')`, porque o papel
 * era indexado DIRETO em `GLIFOS`, cujas chaves sao manchete/corpo/dado.
 *
 * `legenda` esta na tabela porque ela nomeia a familia que a CAMADA `Legenda`
 * usa -- e nao porque legenda seja papel de evento. Ver `PAPEIS_DE_EVENTO`.
 */
export const FAMILIA_DO_PAPEL: Record<PapelEvento | 'legenda', Papel> = {
  manchete: 'manchete', // Archivo Black, alturaLinha 1,088 (hhea)
  dado: 'dado', // IBM Plex Mono, avanco 0,6 em fixo, alturaLinha 1,3
  etiqueta: 'dado', // rotulo e carimbo: mono resolve
  legenda: 'corpo', // Inter Bold, alturaLinha 1,21
};

/** Como o texto de cada papel se revela. */
export type CadenciaTexto = 'palavra' | 'linha' | 'bloco';

/**
 * Papel -> cadencia de revelacao.
 *
 * A DO `dado` E FORCADA POR MEDICAO, NAO POR GOSTO. `duracaoDaFrase('R$ 39,90')`
 * trata `R$` e `39,90` como dois irmaos; um cartao de preco que revela `R$` e o
 * numero 3 frames depois le como defeito, nao como ritmo. Cada linha de um dado
 * e um CAMPO, e o stagger e por linha.
 *
 * `etiqueta` entra por bloco porque um carimbo nao tem ritmo interno: ou esta no
 * quadro ou nao esta.
 */
export const CADENCIA_DO_PAPEL: Record<PapelEvento, CadenciaTexto> = {
  manchete: 'palavra',
  dado: 'linha',
  etiqueta: 'bloco',
};

/**
 * Papel -> pista SUGERIDA.
 *
 * NAO E UM DEFAULT DO MOTOR. `pista` e obrigatorio no briefing (spec §2.3), e
 * nenhum passo do compilador le esta tabela para preencher um campo em branco --
 * default escondido e o que esta spec proibe em toda parte. Ela existe para a
 * skill `canastra-briefing` ESCREVER o campo no arquivo: assim a escolha fica
 * visivel no JSON, onde o Rafael a le e a muda, em vez de morar no motor.
 *
 * `manchete` -> `topo` porque e a faixa que `layout()` ja reservava para ela.
 * `dado` -> `principal` porque um cartao numerico e o elemento dominante da cena
 * dele, e `proibicoes.md:19` pede um dominante por cena.
 * `etiqueta` -> `topo` porque carimbo mora na borda. Manchete e etiqueta na mesma
 * pista ao mesmo tempo e ERRO DE BRIEFING, pego por `refinar.ts` -- e erro
 * explicito e melhor que sobreposicao silenciosa, que e o defeito medido de hoje:
 * a caixa da manchete e a da legenda se intersectam em 90,20 px no eixo x no 1:1
 * (medido em 01/10/2026; a versao anterior chamava esse numero de "invasao de
 * 353,20 px", que era `manchete.fim - legenda.y`, outra grandeza).
 *
 * `rodape` NAO aparece nesta tabela: ela e a caixa da camada `Legenda`.
 */
export const PISTA_PADRAO: Record<PapelEvento, Pista> = {
  manchete: 'topo',
  dado: 'principal',
  etiqueta: 'topo',
};
```

**`ENCAIXE_PADRAO` não existe.** A versão anterior declarava aqui uma tabela papel → lista de
preferência de encaixe. Ela saiu junto com o campo `encaixe` do briefing: encaixe é **derivado** de
`(pista, formato)` na Tarefa 4 (spec §3.4.2), e o caminho para pedir cartela é declarar
`pista: "tela"`. Uma lista de preferência sem regra para "nenhum item passou" era um silêncio no
meio do contrato.

- [ ] **Step 5: alargar `PapelTexto`, indexar por família e ESCALONAR POR CADÊNCIA em `texto-forma.ts`**

Em `src/motor/camadas/texto-forma.ts`:

1. Acrescentar aos imports:

```ts
import {CADENCIA_DO_PAPEL, FAMILIA_DO_PAPEL, type CadenciaTexto, type PapelEvento} from '../evento';
import type {Papel} from '../../identidade/tipografia';
```

2. Substituir a declaração de `PapelTexto` (linha 49) por:

```ts
/**
 * Papel de um texto de tela. Sao os papeis de EVENTO -- e o mapa para a familia
 * de tipografia e `FAMILIA_DO_PAPEL`, nunca indexacao direta: `GLIFOS` tem as
 * chaves manchete/corpo/dado, e `papel: 'etiqueta'` indexado direto lancava
 * `TypeError: Cannot read properties of undefined (reading 'x')` (medido).
 */
export type PapelTexto = PapelEvento;
```

3. Em `Forma`, acrescentar **dois** campos logo depois de `papel`:

```ts
  papel: PapelTexto;
  /** a familia de tipografia do papel. E ela que o `.tsx` usa, nao o papel. */
  familia: Papel;
  /** como este texto se revela: `CADENCIA_DO_PAPEL[papel]` */
  cadenciaTexto: CadenciaTexto;
  /**
   * Quantos elementos ESCALONADOS o texto tem, pela cadencia.
   *
   * `palavra` -> uma por palavra · `linha` -> uma por linha · `bloco` -> 1.
   *
   * ESTE CAMPO EXISTE PARA O PLANO E O PIXEL NAO DISCORDAREM. Quem dimensiona a
   * duracao (`duracaoDeIrmao`, `duracaoComIrmaos`) tem que contar a MESMA coisa
   * que o stagger escalona. Antes de 01/10/2026 o compilador contava por cadencia
   * e `TextoTela` contava `palavras.length`: a etiqueta `MEDEIROS 1250 M` recebia
   * 36 frames e desenhava 42.
   */
  irmaos: number;
```

4. Em `quebrar` e `medirBloco`, trocar a medição para passar pela família:

```ts
export function quebrar(
  texto: string,
  {papel, corpo, largura}: {papel: PapelTexto; corpo: number; largura: number},
): string[] {
  const familia = FAMILIA_DO_PAPEL[papel];
  const palavras = texto.split(/\s+/).filter((p) => p.length > 0);
  if (palavras.length === 0) return [];

  const linhas: string[] = [];
  let atual = palavras[0];
  for (let i = 1; i < palavras.length; i++) {
    const tentativa = `${atual} ${palavras[i]}`;
    if (larguraEm(tentativa, familia) * corpo <= largura + EPS) {
      atual = tentativa;
    } else {
      linhas.push(atual);
      atual = palavras[i];
    }
  }
  linhas.push(atual);
  return linhas;
}
```

```ts
function medirBloco(
  texto: string,
  papel: PapelTexto,
  corpo: number,
  entrelinha: number,
  caixa: Caixa,
) {
  const familia = FAMILIA_DO_PAPEL[papel];
  const linhas = quebrar(texto, {papel, corpo, largura: caixa.largura});
  const larguraBloco = linhas.reduce(
    (m, l) => Math.max(m, larguraEm(l, familia) * corpo),
    0,
  );
  const alturaBloco = linhas.length * corpo * entrelinha;
  return {linhas, larguraBloco, alturaBloco};
}
```

5. Dentro de `formaTextoTela`, trocar a linha da entrelinha por uma que passa pela família:

```ts
  const familia = FAMILIA_DO_PAPEL[papel];
  const entrelinha =
    modo === 'cartela' ? METRICAS[familia].alturaLinha : LEGENDA.entrelinha;
```

6. **O escalonamento pela cadência.** Substituir o bloco que monta `palavras` (o `linhas.forEach`
com `let irmao = 0`) por:

```ts
  // O INDICE DE IRMAO SAI DA CADENCIA DO PAPEL, nao do numero de palavras.
  //
  // Antes de 01/10/2026 este bloco incrementava `irmao` por PALAVRA em todo papel,
  // e `CADENCIA_DO_PAPEL` existia sem chegar aqui. As consequencias eram duas, e as
  // duas medidas: (a) `duracaoDaFrase('R$ 39,90')` tratava `R$` e `39,90` como dois
  // irmaos, e um cartao de preco que revela `R$` e o numero 3 frames depois le como
  // defeito -- e essa e a justificativa ESCRITA da cadencia do `dado`; (b) a
  // etiqueta `MEDEIROS 1250 M` recebia 36 frames do plano (1 irmao, cadencia
  // `bloco`) e desenhava 42 (3 palavras), porque o plano contava por cadencia e a
  // tela contava por palavra.
  //
  // `irmaoDaPalavra` e a UNICA regra, e ela vale para o atraso E para a contagem:
  //
  //   palavra .... o indice da palavra na FRASE (nao na linha): o stagger varre a
  //                manchete inteira e nao reinicia a cada quebra
  //   linha ...... o indice da LINHA. Cada linha de um dado e um campo, e as
  //                palavras de uma linha entram juntas
  //   bloco ...... sempre 0. Um carimbo nao tem ritmo interno: ou esta no quadro
  //                ou nao esta
  const cadenciaTexto = CADENCIA_DO_PAPEL[papel];
  const palavras: PalavraPosta[] = [];
  let indiceNaFrase = 0;
  linhas.forEach((linha, iLinha) => {
    for (const p of linha.split(' ')) {
      const irmao =
        cadenciaTexto === 'palavra' ? indiceNaFrase : cadenciaTexto === 'linha' ? iLinha : 0;
      palavras.push({
        texto: p,
        irmao,
        linha: iLinha,
        // UM acento por cena: uma palavra, nunca duas. O indice do acento continua
        // sendo o da PALAVRA na frase, e nao o de irmao -- senao numa etiqueta
        // (todos os irmaos 0) o acento pintaria o bloco inteiro.
        cor: indiceNaFrase === palavraAcento ? COR.acento : COR.creme,
        atrasoFrames: atrasoDoIrmao(irmao, cadencia),
      });
      indiceNaFrase++;
    }
  });

  const irmaos =
    cadenciaTexto === 'palavra'
      ? Math.max(1, palavras.length)
      : cadenciaTexto === 'linha'
        ? Math.max(1, linhas.length)
        : 1;
```

7. No `return`, depois de `papel,`:

```ts
    familia,
    cadenciaTexto,
    irmaos,
```

**`PalavraPosta.irmao` deixa de ser o índice na frase e passa a ser o índice de irmão.** É o que
`progresso(t, {inicio: p.atrasoFrames, ...})` já consome, então nenhuma camada muda por causa disso
— mas a `key` do `<span>` em `TextoTela.tsx` usa `${p.irmao}-${p.texto}`, e numa etiqueta os três
irmãos são 0. Trocar a `key` por `${indice}-${p.texto}` usando o índice do `.map`, no Step 6.

- [ ] **Step 6: fazer `TextoTela.tsx` usar `forma.familia` e `forma.irmaos`**

Em `src/motor/camadas/TextoTela.tsx`:

1. as três indexações por papel passam pela família:

```tsx
  const espaco = larguraEm(' ', forma.familia) * forma.corpo;
```

e no `<span>` de cada palavra:

```tsx
                      fontFamily: PILHA[forma.familia],
                      fontWeight: TIPO[forma.familia].peso,
```

2. **a duração passa a sair de `forma.irmaos`**, e é esta troca que faz plano e pixel medirem a mesma
coisa. Substituir as duas linhas que contam palavras:

```tsx
  // `forma.irmaos`, NAO `forma.palavras.length`: a cadencia do papel decide quantos
  // elementos escalonam (palavra / linha / bloco), e o compilador dimensionou a cena
  // com esse MESMO numero. Contar palavras aqui devolveria a divergencia de 6 frames
  // que a etiqueta de 3 palavras produzia.
  const duracaoPalavra = duracaoFrames ?? duracaoDeIrmao(forma.irmaos, c);
  const duracaoCena = duracaoComIrmaos(forma.irmaos, duracaoPalavra, c);
```

3. a `key` de cada palavra deixa de usar `p.irmao`, que agora repete dentro de uma etiqueta ou de
uma linha de dado:

```tsx
            {forma.palavras
              .filter((p) => p.linha === iLinha)
              .map((p, iPalavra) => {
```
```tsx
                  <span
                    key={`${iLinha}-${iPalavra}-${p.texto}`}
```

- [ ] **Step 7: rodar o teste e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/evento.test.ts`
Expected: `Tests 9 passed (9)`.

- [ ] **Step 8: rodar a suíte inteira e o typecheck**

Run: `cd instagram/remotion && npx vitest run && npm run tsc`
Expected: a suíte com **BASE + 3 + 12 + 9** testes, e `npm run tsc` sem saída. Nenhum teste
antigo muda **no valor esperado**: `'manchete'` e `'dado'` continuam sendo papéis válidos,
`FAMILIA_DO_PAPEL` mapeia os dois para si mesmos, e a cadência de `manchete` é `palavra` — que é
exatamente o que o escalonamento fazia para todos antes.

**Os dois testes que poderiam se importar foram conferidos no arquivo, não supostos.**
`grep -n "papel: 'dado'" tests/*.test.ts` acha **uma** ocorrência, `textotela.test.ts:536`, e ela
asserta só `f.papel` e `f.entrelinha > 0` — não toca stagger. E a única asserção sobre
`p.irmao` é `textotela.test.ts:528`, `[0, 1, 2, 3]`, num `formaTextoTela` **sem `papel`**, logo
`manchete`, logo cadência `palavra`, logo `[0, 1, 2, 3]` continua certo. Se algum outro teste
asseverar stagger por palavra num `dado`, o número novo é o certo e a justificativa está no
comentário do Step 5 item 6.

- [ ] **Step 9: CONFERÊNCIA NO PIXEL — o sha256 continua o mesmo**

Run:
```
cd instagram/remotion
npx remotion still src/index.ts Reel out/t3-f120.png --frame=120 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
node -e "const c=require('node:crypto'),f=require('node:fs');const h=n=>c.createHash('sha256').update(f.readFileSync('out/'+n+'.png')).digest('hex');console.log(h('antes-f120')===h('t3-f120')?'IDENTICO':'MUDOU')"
```
Expected: `IDENTICO`. Esta tarefa consertou um papel que **nunca foi desenhado**; se o pixel da
manchete mudou, a indexação por família está devolvendo outra métrica e o texto vai vazar da
caixa em algum formato. O escalonamento por cadência também não pode mover nada aqui: a manchete
do `props.json` é `papel: 'manchete'`, cadência `palavra`, que é o comportamento de antes.

- [ ] **Step 10: commit**

```bash
git add instagram/remotion/src instagram/remotion/tests
git commit -m "$(cat <<'MSG'
Motor: papel de evento mapeado para familia, e o papel etiqueta para de explodir

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 4: pistas, o formato `4:5`, o encaixe derivado e o piso de dominância em área

Quatro coisas, todas remedidas em 01/10/2026 com `layout()` **pós-§0** (margem em fração), e
nenhuma delas é a que a versão anterior deste plano escrevia:

**1. A sobreposição, com o eixo nomeado.** O número antigo — *"a manchete entra 353,20 px por
dentro da legenda no 1:1"* — era `manchete.fim − legenda.y`, que não é interseção e é **maior que a
caixa inteira da legenda** (172,80 px de altura), o que torna a frase impossível. A interseção real,
medida nos dois eixos:

| formato | interseção em x | interseção em y | `manchete.fim − legenda.y` (o número antigo) |
|---|---:|---:|---:|
| 1080×1920 | 760,00 | **0,00** | −867,20 |
| 1080×1080 | **90,20** | 172,80 | 353,20 |
| 1080×1350 | **102,35** | 216,00 | 364,00 |
| 1920×1080 | **122,56** | 172,80 | 594,31 |

**No 9:16 não há sobreposição nenhuma.** O defeito é dos formatos em que o vídeo vira coluna, e os
90,20 px que a auditoria relatou são a interseção **em x** no 1:1 — reproduzidos aqui.

**2. A causa mecânica, e ela é uma linha.** Não é "as zonas são mal escolhidas". `layout.ts:68-73`
calcula a **largura** da caixa de legenda supondo que o `x` seja `video.x + 16k` (é o que `−32k`
significa: 16 de respiro de cada lado do vídeo) e usa `seguro.x` no `x`. Com o vídeo em coluna,
`video.x = 0` e `seguro.x = 160`, então a caixa desliza 144,00 px para a direita levando a largura
inteira e **vaza a borda direita do vídeo** em 128,00 px no 1:1, 128,00 no 4:5 e 227,56 no 16:9
(medido). É nesse vazamento que a coluna da manchete mora, e 735,50 − 645,30 = **90,20 px**.

**3. O corpo.** Com o texto real do `props.json` (`'SUA PRÓPRIA MARCA DE CAFÉ'`) e fonte 9:16, a
manchete na coluna sai **48 px no 1:1** e **26 px no 4:5**, contra **78 px** de corpo de legenda. O
elemento que deveria dominar é o menor texto do quadro.

**4. O piso de dominância é de ÁREA, não de corpo.** `proibicoes.md:19` fala de *elemento
dominante*, e o que domina um quadro é a **mancha**, não o tamanho da letra. O piso é
`1,25 × dominancia(legenda no mesmo quadro)`, medido em fração da área do quadro.

**Files:**
- Modify: `instagram/remotion/src/motor/layout.ts` (enum de formato, `MARGEM` exportado, **o conserto da largura da legenda**)
- Modify: `instagram/remotion/src/motor/pista.ts` (a geometria: `colunaDeTexto()`, `pistas()`, `seguroDoVideo()`, `encaixe()`)
- Create: `instagram/remotion/src/motor/encaixe.ts` (a medição: corpo na caixa e dominância)
- Create: `instagram/remotion/tests/pistas.test.ts`
- Create: `instagram/remotion/tests/encaixe.test.ts`
- Modify: `instagram/remotion/tests/layout.test.ts` (o par que faltava: legenda × manchete, nos quatro formatos, nos dois eixos, com fonte retrato **e** paisagem)

- [ ] **Step 1: escrever o teste de pistas que falha**

Criar `instagram/remotion/tests/pistas.test.ts`:

```ts
import {describe, expect, it} from 'vitest';
import {layout, type Caixa} from '../src/motor/layout';
import {
  CONFLITO_DE_PISTA,
  LIMIAR_DE_COLUNA,
  colunaDeTexto,
  encaixe,
  pistas,
  seguroDoVideo,
} from '../src/motor/pista';

const QUADROS: Array<[number, number, string]> = [
  [1080, 1920, '9:16'],
  [1080, 1080, '1:1'],
  [1080, 1350, '4:5'],
  [1920, 1080, '16:9'],
];

/**
 * AS DUAS RAZOES DE FONTE QUE O ACERVO TEM, e a segunda e a que faltava.
 *
 * `0,5625` e o `pl.mp4` (retrato). `4/3` sao as 26 fotos da fazenda, 4032x3024 --
 * e e a fonte da PECA DE PROVA da Tarefa 13. A versao anterior destes testes usava
 * `razaoFonte: 9/16` nos seis casos, entao a fonte em PAISAGEM nunca aparecia em
 * verde nem em vermelho. Com ela, a geometria antiga produzia
 * `intersecao(pista topo, seguroDoVideo) = 760,00 x 0,00 px` -- caixa DEGENERADA --
 * no 9:16 e no 4:5, porque o video letterboxado comeca ABAIXO da faixa de topo do
 * quadro. Todo evento cairia em cartela e a peca de prova sairia com tres cartelas
 * de terra em vez dos tres registros que ela existe para exercitar.
 */
const RAZOES: Array<[number, string]> = [
  [0.5625, 'retrato (pl.mp4)'],
  [4 / 3, 'paisagem (foto 4032x3024)'],
];

function areaDaIntersecao(a: Caixa, b: Caixa): number {
  const x = Math.max(a.x, b.x);
  const y = Math.max(a.y, b.y);
  const direita = Math.min(a.x + a.largura, b.x + b.largura);
  const baixo = Math.min(a.y + a.altura, b.y + b.altura);
  return Math.max(0, direita - x) * Math.max(0, baixo - y);
}

describe('formato', () => {
  it('o 4:5 deixa de sair como "outro"', () => {
    // Medido em 30/09/2026: `layout({largura:1080, altura:1350})` devolvia
    // `formato: 'outro'`. A geometria JA estava certa (coluna de 759,4 x 1350 e
    // sobra de 320,63 px); so o rotulo faltava -- extensao de enum, nao
    // reescrita, como 05-formatos.md secao 6 previu.
    for (const [w, h, rotulo] of QUADROS) {
      expect(layout({largura: w, altura: h, razaoFonte: 9 / 16}).formato).toBe(rotulo);
    }
  });
});

describe('pistas', () => {
  it('nenhuma pista de EVENTO invade a pista da legenda, em nenhum formato e em nenhuma razao', () => {
    // O DEFEITO QUE ISTO TORNA IMPOSSIVEL, remedido em 01/10/2026 nos DOIS eixos:
    // a caixa de manchete e a de legenda se intersectam em 90,20 px em x no 1:1,
    // 102,35 no 4:5 e 122,56 no 16:9. No 9:16, zero.
    //
    // ESTE TESTE DEPENDE DO §0, e nao so por causa do `import` de `MARGEM`. Medido:
    // com o conserto da largura da legenda (Step 3, item 5) mas SEM a `MARGEM` em
    // fracao, a combinacao 1:1 x paisagem ainda da 22.429,50 px² de area -- a
    // sobreposicao ali e em Y (`principal` desce a 626,71 e a legenda comeca em
    // 597,20), e conserto de largura nao toca o eixo y. Se este `it` falhar SO nessa
    // combinacao, o §0 nao foi feito; nao mexa na geometria.
    for (const [rf] of RAZOES) {
      for (const [w, h] of QUADROS) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        const p = pistas(z);
        expect(areaDaIntersecao(p.topo, p.rodape), `${w}x${h} rf ${rf}`).toBeCloseTo(0, 6);
        expect(areaDaIntersecao(p.principal, p.rodape), `${w}x${h} rf ${rf}`).toBeCloseTo(0, 6);
      }
    }
  });

  it('topo e principal nao se sobrepoem, em nenhum formato e em nenhuma razao', () => {
    for (const [rf] of RAZOES) {
      for (const [w, h] of QUADROS) {
        const p = pistas(layout({largura: w, altura: h, razaoFonte: rf}));
        expect(areaDaIntersecao(p.topo, p.principal), `${w}x${h} rf ${rf}`).toBeCloseTo(0, 6);
      }
    }
  });

  it('toda pista tem altura positiva COM FONTE EM PAISAGEM -- era aqui que degenerava', () => {
    // Medido com a geometria antiga (faixa de topo do QUADRO, 0,18 da altura):
    // 9:16 com fonte 4:3 dava 760,00 x 0,00 e 4:5 idem. Com a coluna de texto
    // como base, a pista mais baixa mede 153,58 px de altura -- medido.
    for (const [rf] of RAZOES) {
      for (const [w, h] of QUADROS) {
        const p = pistas(layout({largura: w, altura: h, razaoFonte: rf}));
        for (const nome of ['topo', 'principal', 'rodape', 'tela'] as const) {
          expect(p[nome].altura, `${nome} ${w}x${h} rf ${rf}`).toBeGreaterThan(1);
          expect(p[nome].largura, `${nome} ${w}x${h} rf ${rf}`).toBeGreaterThan(1);
        }
      }
    }
  });

  it('a pista de evento esta SEMPRE dentro da coluna de texto', () => {
    // A propriedade que torna a sobreposicao decidivel so em y: as pistas de
    // evento partilham o intervalo em x da coluna.
    for (const [rf] of RAZOES) {
      for (const [w, h] of QUADROS) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        const c = colunaDeTexto(z);
        for (const nome of ['topo', 'principal'] as const) {
          const b = pistas(z)[nome];
          expect(b.x).toBeCloseTo(c.x, 6);
          expect(b.largura).toBeCloseTo(c.largura, 6);
          expect(b.y).toBeGreaterThanOrEqual(c.y - 1e-6);
          expect(b.y + b.altura).toBeLessThanOrEqual(c.y + c.altura + 1e-6);
        }
      }
    }
  });

  it('a coluna de texto e a SOBRA quando ela passa do limiar, e o seguro do video quando nao', () => {
    // Sobras medidas em 01/10/2026, com fonte retrato: 0,00 px no 9:16 (0,00%),
    // 472,50 no 1:1 (43,75%), 320,63 no 4:5 (29,69%) e 1312,50 no 16:9 (68,36%).
    // O limiar 0,22 fica no meio do vao: qualquer valor entre 0 e 29,69% separa os
    // MESMOS grupos.
    expect(LIMIAR_DE_COLUNA).toBe(0.22);
    const z916 = layout({largura: 1080, altura: 1920, razaoFonte: 0.5625});
    expect(colunaDeTexto(z916)).toEqual(seguroDoVideo(z916));
    const z11 = layout({largura: 1080, altura: 1080, razaoFonte: 0.5625});
    expect(colunaDeTexto(z11).x).toBeGreaterThan(z11.video.largura);
  });

  it('a pista tela conflita com topo e principal, e NAO com rodape', () => {
    // A cartela cobre o video mas nao cobre a legenda: a legenda continua
    // correndo por cima do terra chapado. E a escolha que PecaVideo.tsx:115-120
    // ja tomou e defendeu por escrito -- cartela por cima de tudo apagaria a
    // legenda por dois segundos e quebraria a continuidade de leitura.
    expect(CONFLITO_DE_PISTA.tela).toContain('topo');
    expect(CONFLITO_DE_PISTA.tela).toContain('principal');
    expect(CONFLITO_DE_PISTA.tela).not.toContain('rodape');
  });

  it('a pista rodape E a caixa de legenda, nao uma caixa parecida', () => {
    // Duas caixas "quase iguais" para a mesma coisa divergem no primeiro
    // conserto. A pista rodape e literalmente zonas.legenda.
    for (const [rf] of RAZOES) {
      for (const [w, h] of QUADROS) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        expect(pistas(z).rodape).toEqual(z.legenda);
      }
    }
  });
});

describe('encaixe derivado', () => {
  it('tela sempre da cartela, e ela e o UNICO caminho para a cartela', () => {
    for (const [rf] of RAZOES) {
      for (const [w, h] of QUADROS) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        expect(encaixe('tela', z)).toBe('cartela');
        expect(encaixe('topo', z)).not.toBe('cartela');
        expect(encaixe('principal', z)).not.toBe('cartela');
      }
    }
  });

  it('sobra abaixo do limiar da FAIXA; acima da COLUNA', () => {
    // No 9:16 a sobra e 0,00 px: `coluna` ali nao e uma escolha ruim, e uma
    // escolha impossivel -- e foi por isso que o campo `encaixe` saiu do briefing.
    const z916 = layout({largura: 1080, altura: 1920, razaoFonte: 0.5625});
    expect(encaixe('topo', z916)).toBe('faixa');
    const z11 = layout({largura: 1080, altura: 1080, razaoFonte: 0.5625});
    expect(encaixe('topo', z11)).toBe('coluna');
    // com fonte PAISAGEM o video preenche a largura tambem no 1:1 e no 4:5, e a
    // faixa volta a ser a resposta. Medido: sobra 0,00 px nos tres verticais.
    const z11p = layout({largura: 1080, altura: 1080, razaoFonte: 4 / 3});
    expect(encaixe('topo', z11p)).toBe('faixa');
  });
});

describe('seguroDoVideo', () => {
  it('fica dentro do video E dentro do seguro do quadro', () => {
    // Um evento em encaixe 'faixa' mora SOBRE o video, e o video nem sempre e o
    // quadro: no 1:1 com fonte retrato ele e uma coluna de 607,5 px de largura, e
    // com fonte paisagem ele e uma faixa de 810,0 px de altura no meio.
    for (const [rf] of RAZOES) {
      for (const [w, h] of QUADROS) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        const s = seguroDoVideo(z);
        expect(s.x).toBeGreaterThanOrEqual(z.video.x - 1e-6);
        expect(s.x + s.largura).toBeLessThanOrEqual(z.video.x + z.video.largura + 1e-6);
        expect(s.y).toBeGreaterThanOrEqual(z.video.y - 1e-6);
        expect(s.y + s.altura).toBeLessThanOrEqual(z.video.y + z.video.altura + 1e-6);
        expect(s.x).toBeGreaterThanOrEqual(z.seguro.x - 1e-6);
        expect(s.altura).toBeGreaterThan(1);
        expect(s.largura).toBeGreaterThan(1);
      }
    }
  });

  it('no 9:16 com fonte retrato o seguro do video E o seguro do quadro', () => {
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 9 / 16});
    const s = seguroDoVideo(z);
    expect(s.x).toBeCloseTo(z.seguro.x, 6);
    expect(s.largura).toBeCloseTo(z.seguro.largura, 6);
    expect(s.y).toBeCloseTo(z.seguro.y, 6);
  });
});
```

- [ ] **Step 2: rodar o teste e conferir que falha**

Run: `cd instagram/remotion && npx vitest run tests/pistas.test.ts`
Expected: FALHA na resolução dos nomes — `pistas`, `colunaDeTexto`, `seguroDoVideo`, `encaixe` e
`LIMIAR_DE_COLUNA` não existem em `pista.ts` (que a Tarefa 3 criou só com os nomes). O primeiro
`describe` falha com `expected 'outro' to be '4:5'`.

- [ ] **Step 3: estender `src/motor/layout.ts` — enum, `MARGEM` visível e o conserto de uma linha**

1. Trocar o tipo `Zonas` (o bloco das linhas 8–12) para incluir `4:5`:

```ts
export type Caixa = {x: number; y: number; largura: number; altura: number};

export type Zonas = {
  seguro: Caixa; video: Caixa; legenda: Caixa; manchete: Caixa;
  formato: '9:16' | '1:1' | '4:5' | '16:9' | 'outro';
};
```

(Os nomes `PISTAS`, `Pista`, `Encaixe` e `CONFLITO_DE_PISTA` **não** entram aqui: eles nasceram em
`src/motor/pista.ts` na Tarefa 3, e a geometria deles entra lá no Step 4 desta tarefa. `layout.ts`
não importa `pista.ts`, e `pista.ts` importa `layout.ts` — a seta aponta para um lado só.)

2. **Tornar `MARGEM` visível, EDITANDO a linha, não substituindo o bloco.**

A Tarefa 3 do plano de qualidade escreveu, acima dessa linha, um comentário de ~25 linhas com as
três medições que justificam as frações (**16,15% / 28,70% / 51,03%** de base efetiva nos três
formatos, e o registro de que os 160 px do lado **foram escolhidos no olho e nunca medidos**). Esse
comentário é a **única cópia daquela medição no repositório**.

Então: acrescente `export ` ao começo da linha existente. **Não apague o bloco de comentário acima
dela.** O resultado é:

```ts
export const MARGEM = {topo: 0.05, base: 0.16, lado: 160 / 1080};
```

Confira que o comentário sobreviveu:

```bash
cd instagram/remotion
grep -c "16,15%\|28,70%\|51,03%" src/motor/layout.ts
```
Expected: **3**. Se der 0, o bloco foi substituído em vez de editado e a medição se perdeu — desfaça
com `git checkout src/motor/layout.ts` e refaça o §0 antes de continuar.

**`FRACAO_TOPO` não existe.** A versão anterior criava uma constante de 0,18 da altura do QUADRO para
a pista de topo. Ela saiu porque produzia caixa degenerada com fonte em paisagem: medido, no 9:16 com
fonte 4:3 o vídeo é letterboxado em `y 555,00 .. 1365,00`, e a faixa de topo do quadro
(`y 96,00 .. 441,60`) **não intersecta o vídeo** — `intersecao(topo, seguroDoVideo) = 760,00 × 0,00`.
A altura de pista agora é fração da **coluna de texto**, que já é a caixa certa por construção.

3. Acrescentar `4:5` à detecção de formato (era a linha 30–33):

```ts
  const r = largura / altura;
  const formato: Zonas['formato'] =
    Math.abs(r - 9 / 16) < 0.01 ? '9:16' :
    Math.abs(r - 1) < 0.01 ? '1:1' :
    Math.abs(r - 4 / 5) < 0.01 ? '4:5' :
    Math.abs(r - 16 / 9) < 0.01 ? '16:9' : 'outro';
```

4. Trocar o `if (formato === '9:16')` por uma condição sobre a **geometria**, não sobre o rótulo
— senão o 4:5 entra no ramo errado só por ter ganhado nome:

```ts
  let video: Caixa, manchete: Caixa;

  // A pergunta certa nao e "qual e o rotulo", e "a fonte preenche a largura?".
  // Antes de 01/10/2026 o teste era `formato === '9:16'`, e com o 4:5 ganhando
  // rotulo isso viraria um ramo escolhido por nome em vez de por medida.
  const preencheALargura = Math.abs(altura * razaoFonte - largura) < 0.5;

  if (preencheALargura) {
```

(o corpo dos dois ramos não muda)

5. **O CONSERTO DE UMA LINHA: a largura da caixa de legenda.** Substituir o bloco das linhas 68–73
(pós-§0, com `kx`) por:

```ts
  // legenda sempre ancorada no rodape da area segura, sobre o video
  const alturaLegenda = altura * 0.16;
  // O `x` e o `min` da largura tem que falar do MESMO ponto de partida.
  //
  // Antes de 01/10/2026 a largura era `Math.min(seguro.largura, video.largura -
  // 32 * kx)`: ela supoe que `x` seja `video.x + 16*kx` (e o que o `-32` significa,
  // 16 de respiro de cada lado do video), e o `x` usava `seguro.x`. Com o video em
  // coluna, `video.x = 0` e `seguro.x = 160`: a caixa desliza 144,00 px para a
  // direita levando a largura inteira, e a borda direita dela VAZA o video em
  // 128,00 px no 1:1, 128,00 no 4:5 e 227,56 no 16:9 (medido em 01/10/2026). E
  // nesse vazamento que a coluna da manchete mora: 735,50 - 645,30 = 90,20 px,
  // que e a intersecao em x que a auditoria relatou.
  //
  // Agora a borda direita e o MENOR entre a borda do seguro e a borda do video
  // menos o respiro, e a largura e a distancia dela ao `x` que realmente foi usado.
  //
  // CUSTO HONESTO, medido com a correcao aplicada: a largura util da legenda cai de
  // 575,50 para 431,50 px no 1:1 (-25,0%), de 727,38 para 583,38 no 4:5 (-19,8%) e
  // de 550,61 para 294,61 no 16:9 (-46,5%). O 9:16 nao muda em nada (x 160,00,
  // largura 760,00). Isso empurra a busca binaria de corpo da legenda para baixo
  // nesses formatos e toca D6/V11 -- nao e conserto de graca.
  const xLegenda = Math.max(seguro.x, video.x + 16 * kx);
  const legenda: Caixa = {
    x: xLegenda,
    y: seguro.y + seguro.altura - alturaLegenda,
    largura:
      Math.min(seguro.x + seguro.largura, video.x + video.largura - 16 * kx) - xLegenda,
    altura: alturaLegenda,
  };
```

6. Acrescentar a `tests/layout.test.ts` o par que faltava — ele tem hoje **4** `it` (medido), e um
deles é *"as zonas de video e de manchete nao se sobrepoem no 1:1"*. Falta legenda × manchete:

```ts
  it('legenda e manchete NAO se intersectam, nos quatro formatos e nos dois eixos', () => {
    // O PAR QUE CONVERTE O PARAGRAFO EM INVARIANTE. Medido ANTES do conserto, a
    // intersecao em x era 90,20 px no 1:1, 102,35 no 4:5 e 122,56 no 16:9 (no 9:16,
    // zero). Depois do conserto, 0,00 nos quatro. Medir UM eixo da um numero
    // plausivel e errado -- foi o que produziu os "353,20 px" e a leitura de "100%
    // da caixa" que dois revisores diferentes escreveram.
    for (const rf of [0.5625, 4 / 3]) {
      for (const [w, h] of [[1080, 1920], [1080, 1080], [1080, 1350], [1920, 1080]]) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        const x = Math.max(z.legenda.x, z.manchete.x);
        const direita = Math.min(
          z.legenda.x + z.legenda.largura,
          z.manchete.x + z.manchete.largura,
        );
        const y = Math.max(z.legenda.y, z.manchete.y);
        const baixo = Math.min(
          z.legenda.y + z.legenda.altura,
          z.manchete.y + z.manchete.altura,
        );
        const area = Math.max(0, direita - x) * Math.max(0, baixo - y);
        expect(area, `${w}x${h} rf ${rf}`).toBeCloseTo(0, 6);
      }
    }
  });

  it('a caixa de legenda nao vaza a borda do video', () => {
    // Vazamento medido antes do conserto: +128,00 px no 1:1, +128,00 no 4:5,
    // +227,56 no 16:9. Depois: -16,00 / -16,00 / -28,44 -- a legenda fica DENTRO do
    // video, com o respiro pretendido.
    for (const rf of [0.5625, 4 / 3]) {
      for (const [w, h] of [[1080, 1920], [1080, 1080], [1080, 1350], [1920, 1080]]) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        expect(z.legenda.x + z.legenda.largura, `${w}x${h} rf ${rf}`).toBeLessThanOrEqual(
          z.video.x + z.video.largura + 1e-6,
        );
        expect(z.legenda.largura, `${w}x${h} rf ${rf}`).toBeGreaterThan(0);
      }
    }
  });
```

- [ ] **Step 4: acrescentar a GEOMETRIA a `src/motor/pista.ts`**

Acrescentar ao fim do arquivo que a Tarefa 3 criou (ele até agora não importava nada):

```ts
import {MARGEM, type Caixa, type Zonas} from './layout';

// ---------------------------------------------------------------------------
// A GEOMETRIA
//
// UMA PISTA E UMA FAIXA HORIZONTAL DE UMA COLUNA DE TEXTO, e as duas coisas sao
// DERIVADAS, nunca declaradas. A coluna primeiro, porque a pista depende dela.

/**
 * A partir de que sobra ao lado do video a coluna de texto vira a sobra.
 *
 * `[escolhido]`, e a razao e medida: as sobras sao 0,00 px no 9:16 (0,00% da
 * largura), 472,50 no 1:1 (43,75%), 320,63 no 4:5 (29,69%) e 1312,50 no 16:9
 * (68,36%), com fonte retrato [medido em 01/10/2026]. Qualquer limiar entre 0 e
 * 29,69% separa os MESMOS grupos; 0,22 fica no meio do vao e nao encosta em
 * nenhum lado.
 *
 * Com fonte em PAISAGEM (as 26 fotos da fazenda, 4032x3024) as sobras sao 0,00 nos
 * tres verticais e 480,00 px (25,00%) no 16:9 [medido] -- entao a coluna cai no
 * seguro do video nos formatos que a gente entrega, e e por isso que a faixa e o
 * encaixe da peca de foto parada.
 */
export const LIMIAR_DE_COLUNA = 0.22;

function intersecao(a: Caixa, b: Caixa): Caixa {
  const x = Math.max(a.x, b.x);
  const y = Math.max(a.y, b.y);
  const direita = Math.min(a.x + a.largura, b.x + b.largura);
  const baixo = Math.min(a.y + a.altura, b.y + b.altura);
  return {x, y, largura: Math.max(0, direita - x), altura: Math.max(0, baixo - y)};
}

/**
 * A area segura DO VIDEO, que nao e a do quadro.
 *
 * Um evento em encaixe `faixa` mora SOBRE o video, e o video nem sempre e o
 * quadro: no 1:1 com fonte retrato ele e uma coluna de 607,50 px de largura, e com
 * fonte paisagem ele e uma faixa de 810,00 px de altura no meio de 1080. Usar o
 * seguro do QUADRO poria a faixa metade sobre o video e metade sobre o terra
 * chapado -- e, com fonte paisagem, INTEIRAMENTE fora do video.
 *
 * As mesmas fracoes de `MARGEM`, aplicadas aos eixos do VIDEO, e depois recortadas
 * contra o seguro do quadro: a borda do Instagram nao perdoa nem o que esta sobre
 * video.
 */
export function seguroDoVideo(z: Zonas): Caixa {
  return intersecao(
    {
      x: z.video.x + MARGEM.lado * z.video.largura,
      y: z.video.y + MARGEM.topo * z.video.altura,
      largura: z.video.largura * (1 - 2 * MARGEM.lado),
      altura: z.video.altura * (1 - MARGEM.topo - MARGEM.base),
    },
    z.seguro,
  );
}

/**
 * A coluna em que o texto de evento mora.
 *
 * Duas respostas, e a escolha e do FORMATO, nao de quem escreve o briefing:
 *
 *   sobra >= LIMIAR_DE_COLUNA  ->  a caixa da sobra ao lado do video
 *   senao                      ->  o seguro DO VIDEO
 *
 * No segundo caso o texto fica SOBRE a imagem; no primeiro, AO LADO dela. Nenhum
 * dos dois e melhor: eles sao o que cabe.
 */
export function colunaDeTexto(z: Zonas): Caixa {
  const largura = z.seguro.largura + 2 * z.seguro.x; // a largura do quadro
  const sobra = largura - z.video.largura;
  return sobra >= LIMIAR_DE_COLUNA * largura
    ? intersecao(z.manchete, z.seguro)
    : seguroDoVideo(z);
}

/**
 * As fracoes de altura das pistas de EVENTO, sobre a coluna de texto.
 *
 * `[escolhido]`, e amarradas a dois numeros medidos: a caixa de legenda de hoje e
 * `altura * 0.16` do QUADRO (`layout.ts:67`) e, dentro do seguro do 9:16 -- que e
 * 1.516,80 px de 1.920,00 [medido] --, 307,20 / 1516,80 = **0,2025**; 0,24 da a
 * folga da segunda linha que a Tarefa 7 do plano de qualidade promove a invariante.
 * `topo` recebe a mesma altura que a folga de baixo porque uma faixa superior mais
 * baixa que a inferior le como desalinhamento, e o que sobra, 0,52, e `principal`.
 */
export const FRACAO_DE_PISTA = {topo: 0.24, principal: 0.52, folgaDeBaixo: 0.24} as const;

/**
 * As caixas das quatro pistas.
 *
 * `topo` e `principal` sao faixas da COLUNA DE TEXTO. `rodape` e literalmente
 * `z.legenda` -- a caixa da camada `Legenda`, nao uma caixa parecida com ela. E
 * `tela` e o seguro do quadro, onde a cartela desenha.
 *
 * POR QUE `rodape` NAO E A FAIXA DE BAIXO DA COLUNA.
 * Medido em 01/10/2026: com fonte em paisagem no 1:1, a faixa de baixo da coluna
 * fica em `y 661,82 .. 815,40` e `z.legenda` em `y 734,40 .. 907,20` -- as duas se
 * sobrepoem em 61.560 px². Se `rodape` fosse a faixa, existiriam DUAS caixas quase
 * iguais para a mesma coisa (a que a `Legenda` desenha e a que o portao confere), e
 * duas caixas quase iguais divergem no primeiro conserto. Entao a faixa de baixo da
 * coluna e apenas FOLGA: nenhum evento a declara, e e ela que garante que
 * `principal` nao encoste na legenda.
 *
 * (A spec §3.4.2 escrevia `rodape` como a faixa de baixo da coluna. Foi CORRIGIDA
 * em 01/10/2026 e agora escreve o mesmo que este arquivo: `rodape` e `z.legenda`,
 * `tela` e `z.seguro`, e so `topo` e `principal` sao fracoes da coluna.)
 *
 * A invariante que isso compra, medida nas 8 combinacoes (4 formatos x 2 razoes de
 * fonte): `intersecao(topo, rodape)` e `intersecao(principal, rodape)` tem area
 * ZERO em todas. ATENCAO AO QUE SUSTENTA ISSO -- sao TRES coisas, nao uma:
 * `MARGEM` em fracao (§0), o conserto da largura da legenda (Step 3, item 5) e
 * `rodape` ser a caixa real. As pistas de EVENTO partilham o intervalo em x da
 * coluna, logo a disjuncao ENTRE ELAS e decidida so em y; mas `rodape` NAO
 * partilha esse x (a legenda mora sobre o video, a coluna de evento mora na
 * sobra), entao a disjuncao com ela e MEDIDA, nao construida. Medido: com o
 * conserto da largura e SEM o §0, a combinacao 1:1 x paisagem ainda da
 * 22.429,50 px², porque ali a sobreposicao e em y (principal desce a 626,71 e a
 * legenda comeca em 597,20) e conserto de largura nao toca o eixo y.
 */
export function pistas(z: Zonas): Record<Pista, Caixa> {
  const c = colunaDeTexto(z);
  return {
    topo: {x: c.x, y: c.y, largura: c.largura, altura: c.altura * FRACAO_DE_PISTA.topo},
    principal: {
      x: c.x,
      y: c.y + c.altura * FRACAO_DE_PISTA.topo,
      largura: c.largura,
      altura: c.altura * FRACAO_DE_PISTA.principal,
    },
    rodape: z.legenda,
    tela: z.seguro,
  };
}

/**
 * `encaixe(pista, zonas)` -- DERIVADO, nunca declarado. Resolucao de C2.
 *
 *   pista === 'tela'            -> 'cartela'   -> Modo 'cartela'
 *   sobra < LIMIAR_DE_COLUNA    -> 'faixa'     -> Modo 'sobreImagem'
 *   senao                       -> 'coluna'    -> Modo 'sobreImagem'
 *
 * `coluna` e `faixa` caem no MESMO `Modo` porque a diferenca entre as duas nao e de
 * desenho de texto, e de CAIXA: as duas desenham creme sobre o que estiver atras, e
 * quem muda e a `Caixa` que chega. `texto-forma.ts:46` tem `Modo = 'sobreImagem' |
 * 'cartela'` [medido], dois valores, e o mapeamento 3 -> 2 fica explicito aqui em
 * vez de um terceiro modo nascer lá.
 */
export function encaixe(pista: Pista, z: Zonas): Encaixe {
  if (pista === 'tela') return 'cartela';
  const largura = z.seguro.largura + 2 * z.seguro.x;
  const sobra = largura - z.video.largura;
  return sobra >= LIMIAR_DE_COLUNA * largura ? 'coluna' : 'faixa';
}

/** O `Modo` de `texto-forma.ts` que cada encaixe usa. O mapeamento 3 -> 2. */
export function modoDoEncaixe(e: Encaixe): 'sobreImagem' | 'cartela' {
  return e === 'cartela' ? 'cartela' : 'sobreImagem';
}

/** A caixa em que o texto daquela pista e medido e desenhado. */
export function caixaDaPista(pista: Pista, z: Zonas): Caixa {
  return pistas(z)[pista];
}
```

- [ ] **Step 5: rodar os testes de pistas e de layout, e conferir que passam**

Run: `cd instagram/remotion && npx vitest run tests/pistas.test.ts tests/layout.test.ts`
Expected: `pistas.test.ts` com `Tests 12 passed (12)` e `layout.test.ts` com `Tests 6 passed (6)` — os
4 de antes mais os 2 do Step 3 item 6.

Se `legenda e manchete NAO se intersectam` falhar com uma área positiva, o conserto do Step 3 item 5
não foi aplicado, ou foi aplicado só no `x`. Imprima as duas caixas antes de mexer no teste: a
interseção tem que ser 0,00 nos **quatro** formatos e nas **duas** razões.

- [ ] **Step 6: escrever o teste de encaixe que falha**

Criar `instagram/remotion/tests/encaixe.test.ts`:

```ts
import {describe, expect, it} from 'vitest';
import {cadencia} from '../src/motor/cadencia';
import {
  FATOR_DE_DOMINANCIA,
  dominanciaDaLegenda,
  pisoDeDominancia,
  resolverEncaixe,
} from '../src/motor/encaixe';
import {layout} from '../src/motor/layout';
import {LEGENDA} from '../src/identidade/tokens';

const C = cadencia(30);
const TEXTO = 'SUA PRÓPRIA MARCA DE CAFÉ'; // o texto real de props.json
const RETRATO = 0.5625; // pl.mp4
const PAISAGEM = 4 / 3; // as 26 fotos da fazenda, 4032x3024

describe('o piso de dominancia', () => {
  it('e de AREA, e vale 1,25 x a dominancia da legenda no mesmo quadro', () => {
    // POR QUE AREA E NAO CORPO: `proibicoes.md:19` fala de "elemento dominante", e o
    // que domina um quadro e a MANCHA, nao o tamanho da letra. Uma manchete de corpo
    // grande em duas palavras pode ocupar menos area que uma legenda de duas linhas
    // cheias -- e nesse caso ela nao domina, mesmo com o corpo maior.
    expect(FATOR_DE_DOMINANCIA).toBe(1.25);
    for (const [w, h] of [[1080, 1920], [1080, 1080], [1080, 1350], [1920, 1080]]) {
      const z = layout({largura: w, altura: h, razaoFonte: RETRATO});
      expect(pisoDeDominancia(z)).toBeCloseTo(FATOR_DE_DOMINANCIA * dominanciaDaLegenda(z), 9);
    }
  });

  it('a referencia da legenda sao DUAS LINHAS CHEIAS, e isso vem de uma invariante existente', () => {
    // A caixa de legenda guarda duas linhas -- e a invariante que a Tarefa 7 do plano
    // de qualidade promove. Entao a mancha de referencia e
    // `largura da caixa x corpo x entrelinha x 2`, e nenhum numero novo entra: o
    // corpo e `LEGENDA.corpoEm1080` escalado, a entrelinha e `LEGENDA.entrelinha`.
    const z = layout({largura: 1080, altura: 1920, razaoFonte: RETRATO});
    const esperado =
      (z.legenda.largura * LEGENDA.corpoEm1080 * LEGENDA.entrelinha * 2) / (1080 * 1920);
    expect(dominanciaDaLegenda(z)).toBeCloseTo(esperado, 9);
    // Medido em 01/10/2026: 5,489% do quadro, e o piso 6,861%.
    expect(100 * dominanciaDaLegenda(z)).toBeCloseTo(5.489, 2);
    expect(100 * pisoDeDominancia(z)).toBeCloseTo(6.861, 2);
  });
});

describe('resolverEncaixe', () => {
  it('no 9:16 a coluna nao existe (sobra zero) e o encaixe derivado e a faixa', () => {
    // Medido: no 9:16 o video preenche a largura, sobra = 0,00 px. Uma coluna de
    // largura zero nao e uma escolha ruim, e uma escolha impossivel -- e foi por
    // isso que o campo `encaixe` saiu do briefing (spec §3.4.2).
    const z = layout({largura: 1080, altura: 1920, razaoFonte: RETRATO});
    const r = resolverEncaixe({texto: TEXTO, papel: 'manchete', pista: 'topo', zonas: z, cadencia: C});
    expect(r.encaixe).toBe('faixa');
    expect(r.modo).toBe('sobreImagem');
    // 99 px de corpo, 3 linhas, mancha de 10,435% do quadro contra um piso de
    // 6,861% -- medido em 01/10/2026.
    expect(r.corpo).toBe(99);
    expect(100 * r.dominancia).toBeCloseTo(10.435, 2);
    expect(r.domina).toBe(true);
  });

  it('no 1:1 com fonte retrato a coluna NAO domina, e isso e reprovacao, nao ajuste', () => {
    // O defeito medido: a coluna do 1:1 da 48 px de corpo e 3,793% de mancha, contra
    // um piso de 6,925%. `proibicoes.md:19` pede um elemento dominante por cena, e o
    // motor entregava o contrario -- a manchete era o MENOR texto do quadro.
    //
    // E aqui `resolverEncaixe` NAO tem plano B: o encaixe e derivado do formato, e a
    // saida e `domina: false`. Quem reprova e o portao de ritmo. Para pedir cartela,
    // o briefing declara `pista: "tela"` -- explicitamente, no arquivo.
    const z = layout({largura: 1080, altura: 1080, razaoFonte: RETRATO});
    const r = resolverEncaixe({texto: TEXTO, papel: 'manchete', pista: 'topo', zonas: z, cadencia: C});
    expect(r.encaixe).toBe('coluna');
    expect(r.corpo).toBe(48);
    expect(100 * r.dominancia).toBeCloseTo(3.793, 2);
    expect(r.domina).toBe(false);
    // e a mensagem tem que dizer os DOIS numeros, senao ela nao ensina nada
    expect(r.porque).toMatch(/3,79|3\.79/);
    expect(r.porque).toMatch(/6,92|6\.92/);
  });

  it('a cartela domina em todo formato, e e ela que a pista tela entrega', () => {
    // Medido: 152 px de corpo e 24,245% de mancha no 9:16, 43,102% no 1:1, 34,482%
    // no 4:5. E o caminho que o `01-private-label` usa.
    for (const [w, h, esperado] of [
      [1080, 1920, 24.245],
      [1080, 1080, 43.102],
      [1080, 1350, 34.482],
    ] as Array<[number, number, number]>) {
      const z = layout({largura: w, altura: h, razaoFonte: RETRATO});
      const r = resolverEncaixe({texto: TEXTO, papel: 'manchete', pista: 'tela', zonas: z, cadencia: C});
      expect(r.encaixe, `${w}x${h}`).toBe('cartela');
      expect(r.modo, `${w}x${h}`).toBe('cartela');
      expect(r.corpo, `${w}x${h}`).toBe(152);
      expect(100 * r.dominancia, `${w}x${h}`).toBeCloseTo(esperado, 2);
      expect(r.domina, `${w}x${h}`).toBe(true);
    }
  });

  it('COM FONTE EM PAISAGEM a pista principal domina os tres formatos de entrega', () => {
    // O caso da PECA DE PROVA (Tarefa 13): foto 4032x3024. Medido em 01/10/2026,
    // com `SUA PRÓPRIA MARCA DE CAFÉ` em `principal`, encaixe `faixa`:
    //   9:16  99 px  10,435%  piso  6,861%
    //   1:1   99 px  18,552%  piso 12,198%
    //   4:5   99 px  14,841%  piso  9,758%
    // E a mesma manchete em `topo` da 79 px e NAO domina em nenhum dos tres
    // (5,297% / 9,417% / 7,534%) -- e por isso que a peca de prova declara
    // `principal` e nao `topo`.
    for (const [w, h, dom] of [
      [1080, 1920, 10.435],
      [1080, 1080, 18.552],
      [1080, 1350, 14.841],
    ] as Array<[number, number, number]>) {
      const z = layout({largura: w, altura: h, razaoFonte: PAISAGEM});
      const p = resolverEncaixe({texto: TEXTO, papel: 'manchete', pista: 'principal', zonas: z, cadencia: C});
      expect(p.encaixe, `${w}x${h}`).toBe('faixa');
      expect(p.corpo, `${w}x${h}`).toBe(99);
      expect(100 * p.dominancia, `${w}x${h}`).toBeCloseTo(dom, 2);
      expect(p.domina, `${w}x${h}`).toBe(true);

      const t = resolverEncaixe({texto: TEXTO, papel: 'manchete', pista: 'topo', zonas: z, cadencia: C});
      expect(t.corpo, `${w}x${h} topo`).toBe(79);
      expect(t.domina, `${w}x${h} topo`).toBe(false);
    }
  });

  it('a ETIQUETA nao e candidata a dominar, e o resultado diz isso', () => {
    // `MEDEIROS 1250 M` em `dado` (a familia da etiqueta) sai com 84 px de corpo e
    // 2,940% de mancha no 9:16 -- abaixo do piso, e isso esta CERTO: um carimbo nao
    // e o elemento dominante da cena. Quem exige dominancia e o portao, e ele exige
    // de `manchete` e `dado`, nunca de `etiqueta` (ver Tarefa 10).
    const z = layout({largura: 1080, altura: 1920, razaoFonte: PAISAGEM});
    const r = resolverEncaixe({
      texto: 'MEDEIROS 1250 M',
      papel: 'etiqueta',
      pista: 'topo',
      zonas: z,
      cadencia: C,
    });
    expect(r.corpo).toBe(84);
    expect(100 * r.dominancia).toBeCloseTo(2.94, 2);
    expect(r.domina).toBe(false);
    expect(r.candidataADominar).toBe(false);
  });

  it('a caixa devolvida esta SEMPRE dentro da area segura do quadro', () => {
    for (const rf of [RETRATO, PAISAGEM]) {
      for (const [w, h] of [[1080, 1920], [1080, 1080], [1080, 1350], [1920, 1080]]) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        for (const pista of ['topo', 'principal', 'tela'] as const) {
          const r = resolverEncaixe({texto: TEXTO, papel: 'manchete', pista, zonas: z, cadencia: C});
          const rotulo = `${w}x${h} rf ${rf} ${pista}`;
          expect(r.caixa.x, rotulo).toBeGreaterThanOrEqual(z.seguro.x - 1e-6);
          expect(r.caixa.y, rotulo).toBeGreaterThanOrEqual(z.seguro.y - 1e-6);
          expect(r.caixa.x + r.caixa.largura, rotulo).toBeLessThanOrEqual(
            z.seguro.x + z.seguro.largura + 1e-6,
          );
          expect(r.caixa.y + r.caixa.altura, rotulo).toBeLessThanOrEqual(
            z.seguro.y + z.seguro.altura + 1e-6,
          );
          expect(r.corpo, rotulo).toBeGreaterThan(0);
        }
      }
    }
  });

  it('RECUSA caixa degenerada em vez de devolver corpo 1 -- e ela nao acontece mais', () => {
    // A rede. Com a geometria antiga (faixa de topo do QUADRO) e fonte em paisagem, a
    // intersecao dava 760,00 x 0,00 px: `formaTextoTela` devolveria corpo 1 e o texto
    // sairia ilegivel com exit 0. Nenhuma das 8 combinacoes produz isso agora -- a
    // menor altura de pista medida e 153,58 px -- e este teste existe para a rede nao
    // ser silenciosamente removida.
    const z = layout({largura: 1080, altura: 1920, razaoFonte: PAISAGEM});
    const degenerada = {...z, manchete: {x: z.seguro.x, y: z.seguro.y, largura: 760, altura: 0}};
    expect(() =>
      resolverEncaixe({texto: TEXTO, papel: 'manchete', pista: 'tela', zonas: {...degenerada, seguro: {...z.seguro, altura: 0}}, cadencia: C}),
    ).toThrow(/degenerada/);
  });
});
```

- [ ] **Step 6b: rodar e conferir que falha**

Run: `cd instagram/remotion && npx vitest run tests/encaixe.test.ts`
Expected: FALHA — `Failed to resolve import "../src/motor/encaixe"`.

- [ ] **Step 7: criar `src/motor/encaixe.ts`**

```ts
// A MEDIÇÃO DO TEXTO NA CAIXA DA PISTA, e o veredito de dominancia.
//
// A geometria mora em `motor/pista.ts`; aqui se MEDE. A divisao existe porque medir
// exige `formaTextoTela`, que importa `identidade/glifos` e `identidade/tokens` --
// e `pista.ts` precisa ficar livre dessa dependencia para `motor/evento.ts` poder
// importar o tipo `Pista` dele sem arrastar tipografia (ver Tarefa 3).
//
// O ENCAIXE NAO E ESCOLHIDO AQUI. Ele e derivado de (pista, formato) por
// `encaixe()` de `pista.ts`. Este modulo nao tem plano B, nao tem lista de
// preferencia e nao promove nada a cartela: se o texto nao domina, ele devolve
// `domina: false` com os dois numeros, e quem reprova e o portao de ritmo.
//
// A VERSAO ANTERIOR TINHA PLANO B, E ERA ERRADO. Ela recebia
// `preferencias: ['coluna','faixa','cartela']` e promovia a cartela quando a coluna
// nao alcancava o piso. Duas consequencias: (a) o briefing pedia uma coisa e a peca
// entregava outra, em silencio, que e a licao 3 do CLAUDE.md; (b) com fonte em
// PAISAGEM a promocao disparava em todo evento -- medido, a intersecao da faixa de
// topo do quadro com o video letterboxado era 760,00 x 0,00 px -- e a peca de foto
// parada sairia com terra chapado cobrindo as fotos.
//
// O PISO E DE AREA, E E RELATIVO A LEGENDA
//
// `proibicoes.md:19` pede "um elemento dominante por cena", e o que domina um quadro
// e a MANCHA, nao o tamanho da letra. Medido em 01/10/2026 com o texto real de
// `props.json` (`SUA PROPRIA MARCA DE CAFE`), mancha em % da area do quadro:
//
//   fonte retrato       coluna/faixa   cartela   piso (1,25x legenda)
//   1080x1920 9:16        10,435%      24,245%       6,861%
//   1080x1080 1:1          3,793%      43,102%       6,925%
//   1080x1350 4:5          0,890%      34,482%       7,490%
//
//   fonte paisagem      topo    principal   cartela   piso
//   1080x1920 9:16      5,297%   10,435%    24,245%   6,861%
//   1080x1080 1:1       9,417%   18,552%    43,102%  12,198%
//   1080x1350 4:5       7,534%   14,841%    34,482%   9,758%
//
// O piso e RELATIVO A LEGENDA de proposito: o defeito medido e que o elemento que
// deveria dominar e menor que a legenda, e um piso absoluto em % do quadro nao
// captura isso -- ele passaria numa peca sem legenda e reprovaria numa com legenda
// grande.

import {LEGENDA} from '../identidade/tokens';
import type {Cadencia} from './cadencia';
import {formaTextoTela, type Forma} from './camadas/texto-forma';
import type {PapelEvento} from './evento';
import {MARGEM, type Caixa, type Zonas} from './layout';
import {caixaDaPista, encaixe as encaixeDaPista, modoDoEncaixe, type Encaixe, type Pista} from './pista';

/**
 * Quantas vezes a mancha da legenda o texto tem que ter para "dominar".
 *
 * `[escolhido]`: 1,25 e o menor fator que garante que a diferenca seja visivel em
 * miniatura e nao um empate. Mexer no criterio e mexer AQUI, num lugar so -- nao num
 * `if` por formato.
 */
export const FATOR_DE_DOMINANCIA = 1.25;

/**
 * A mancha de referencia: a legenda com DUAS LINHAS CHEIAS naquele quadro.
 *
 * Duas linhas porque e a invariante da caixa de legenda (Tarefa 7 do plano de
 * qualidade). Nenhum numero novo entra: a largura vem da caixa que `layout()`
 * devolve, o corpo e `LEGENDA.corpoEm1080` escalado pela largura do quadro, a
 * entrelinha e `LEGENDA.entrelinha`.
 *
 * Medido em 01/10/2026: 5,489% do quadro no 9:16 com fonte retrato.
 */
export function dominanciaDaLegenda(z: Zonas): number {
  const largura = z.seguro.largura + 2 * z.seguro.x; // a largura do quadro
  const altura = z.seguro.altura / (1 - MARGEM.topo - MARGEM.base); // e a altura dele
  const corpo = LEGENDA.corpoEm1080 * (largura / 1080);
  return (z.legenda.largura * corpo * LEGENDA.entrelinha * 2) / (largura * altura);
}

/** O piso: `FATOR_DE_DOMINANCIA` vezes a mancha da legenda no mesmo quadro. */
export function pisoDeDominancia(z: Zonas): number {
  return FATOR_DE_DOMINANCIA * dominanciaDaLegenda(z);
}

/** Papeis de que se EXIGE dominancia. `etiqueta` nao esta aqui: carimbo nao domina. */
export const PAPEIS_QUE_DOMINAM: readonly PapelEvento[] = ['manchete', 'dado'];

export type EncaixeResolvido = {
  /** derivado de (pista, formato) por `pista.ts`, nunca escolhido aqui */
  encaixe: Encaixe;
  /** o modo que `formaTextoTela` entende: cartela cobre o video, sobreImagem nao */
  modo: 'sobreImagem' | 'cartela';
  /** a caixa já recortada contra a área segura do quadro */
  caixa: Caixa;
  corpo: number;
  /** area do bloco de texto ÷ area do quadro */
  dominancia: number;
  piso: number;
  /** `dominancia >= piso` */
  domina: boolean;
  /** `false` para `etiqueta`: de um carimbo nao se exige dominancia */
  candidataADominar: boolean;
  /** a frase com os DOIS numeros, para o diagnostico e para o portao */
  porque: string;
  forma: Forma;
};

export function resolverEncaixe({
  texto,
  papel,
  pista,
  zonas,
  cadencia,
  palavraAcento,
}: {
  texto: string;
  papel: PapelEvento;
  /** DECLARADA no briefing. O encaixe sai dela mais o formato. */
  pista: Pista;
  zonas: Zonas;
  cadencia: Cadencia;
  palavraAcento?: number;
}): EncaixeResolvido {
  const enc = encaixeDaPista(pista, zonas);
  const modo = modoDoEncaixe(enc);
  const caixa = caixaDaPista(pista, zonas);

  // A REDE. Caixa degenerada faria `formaTextoTela` devolver corpo 1 e o texto sairia
  // ilegivel com exit 0 -- a licao 3 do CLAUDE.md. Com a geometria de pista sobre a
  // coluna de texto isso nao acontece nas 8 combinacoes medidas (a menor altura de
  // pista e 153,58 px), e a rede fica para o caso que ninguem previu.
  if (caixa.largura <= 1 || caixa.altura <= 1) {
    throw new Error(
      `resolverEncaixe: a caixa da pista '${pista}' e degenerada: ` +
        `${caixa.largura.toFixed(2)} x ${caixa.altura.toFixed(2)} px. Isso e erro de ` +
        'geometria, nao de briefing: uma pista sem area nao pode receber texto, e ' +
        'desenhar corpo 1 sairia ilegivel com exit 0.',
    );
  }

  // `formaTextoTela` escolhe o corpo por busca binaria contra a caixa que as ZONAS
  // dizem. Para medir a caixa de uma pista, montamos zonas com a caixa da pista no
  // lugar de `manchete` -- e o `seguro` continua o do quadro, para o recorte final
  // permanecer o do Instagram. Na cartela as zonas vao inteiras: o modo `cartela` de
  // `formaTextoTela` usa `zonas.seguro` por conta propria.
  const zonasDoEncaixe: Zonas = modo === 'cartela' ? zonas : {...zonas, manchete: caixa};

  const forma = formaTextoTela({
    texto,
    modo,
    zonas: zonasDoEncaixe,
    papel,
    palavraAcento,
    cadencia,
  });

  const largura = zonas.seguro.largura + 2 * zonas.seguro.x;
  const altura = zonas.seguro.altura / (1 - MARGEM.topo - MARGEM.base);
  const dominancia = (forma.larguraBloco * forma.alturaBloco) / (largura * altura);
  const piso = pisoDeDominancia(zonas);
  const candidataADominar = PAPEIS_QUE_DOMINAM.includes(papel);
  const domina = dominancia >= piso;

  const pct = (x: number) => `${(100 * x).toFixed(3).replace('.', ',')}%`;
  const porque = candidataADominar
    ? `${enc} em '${pista}': corpo ${forma.corpo} px, ${forma.linhas.length} linha(s), ` +
      `mancha ${pct(dominancia)} do quadro contra o piso ${pct(piso)} ` +
      `(1,25x a legenda de duas linhas). ${domina ? 'DOMINA' : 'NAO DOMINA'}`
    : `${enc} em '${pista}': corpo ${forma.corpo} px, mancha ${pct(dominancia)}. ` +
      `Papel '${papel}' nao e candidato a dominar -- carimbo nao e o elemento ` +
      'dominante da cena.';

  return {
    encaixe: enc,
    modo,
    caixa: forma.caixa,
    corpo: forma.corpo,
    dominancia,
    piso,
    domina,
    candidataADominar,
    porque,
    forma,
  };
}
```

- [ ] **Step 8: rodar o teste de encaixe e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/encaixe.test.ts`
Expected: `Tests 9 passed (9)`.

Se um número de corpo ou de mancha divergir, **não ajuste o teste**: empacote o módulo e imprima o
resultado, que é como estes números foram obtidos.

```
cd instagram/remotion
node_modules/.bin/esbuild src/motor/encaixe.ts --bundle --format=esm --platform=node   --outfile=out/e.mjs --log-level=error
```

Os três lugares onde a divergência pode nascer, em ordem de probabilidade: (1) o §0 não foi feito e
`MARGEM` ainda está em pixel, e aí **todas** as caixas mudam; (2) o conserto da largura da legenda do
Step 3 item 5 não foi aplicado, e aí a mancha da legenda — logo o piso — sai maior no 1:1, no 4:5 e
no 16:9; (3) a fração de pista foi escrita sobre a altura do quadro em vez da altura da coluna.

- [ ] **Step 9: rodar a suíte inteira e o typecheck**

Run: `cd instagram/remotion && npx vitest run && npm run tsc`
Expected: suíte com **BASE + 3 + 12 + 9 + 12 + 2 + 9** testes; `npm run tsc` sem saída.

**Um teste antigo PODE mudar de valor nesta tarefa, e ele é conhecido:** o conserto da largura da
legenda encurta a caixa em 25,0% no 1:1, 19,8% no 4:5 e 46,5% no 16:9 (medido), e
`tests/layout.test.ts:19-28` asserta que *a legenda fica dentro do seguro nos 3 formatos* — que
continua verdadeiro, porque a caixa **encolheu**. Nenhuma asserção de `textotela.test.ts` lê
`zonas.legenda`: `grep -n "legenda" tests/textotela.test.ts` antes de concluir o contrário. O 9:16
não muda em nada (x 160,00, largura 760,00), e é dele que vem o still do Step 10.

- [ ] **Step 10: CONFERÊNCIA NO PIXEL — o Reel não muda, o 1:1 MUDA, e o 1:1 é o que se olha**

Esta tarefa ainda **não** liga `resolverEncaixe` na árvore (isso é a Tarefa 9), mas ela **muda uma
linha de `layout()`**: a largura da caixa de legenda. Então o pixel não é intocado, e o que muda é
previsto e medido.

**O 9:16 não muda: medido, `x = 160,00` e `largura = 760,00` antes e depois.**

Run:
```
cd instagram/remotion
npx remotion still src/index.ts Reel out/t4-f300.png --frame=300   --props=projetos/01-private-label/props.json   --public-dir=projetos/01-private-label/public
node -e "const c=require('node:crypto'),f=require('node:fs');const h=n=>c.createHash('sha256').update(f.readFileSync('out/'+n+'.png')).digest('hex');console.log(h('antes-f300')===h('t4-f300')?'IDENTICO':'MUDOU')"
```
Expected: `IDENTICO`. O frame 300 é o que tem legenda (o 120 tem manchete e legenda). Se der
`MUDOU`, o conserto pegou o 9:16 — e no 9:16 `video.x = 0`, `video.largura = 1080`, logo
`min(160+760, 1080−16) − 160 = min(920, 1064) − 160 = 760`, o mesmo número de antes. Um `MUDOU` aqui
é erro de sinal no `min`.

**O 1:1 e o 4:5 MUDAM, de propósito.** A legenda fica 25,0% e 19,8% mais estreita, e o corpo dela
cai junto (busca binária). Isso é **D6/V11**, e é a parte do conserto que não é de graça:

Run:
```
cd instagram/remotion
npx remotion still src/index.ts Feed out/t4-feed300.png --frame=300   --props=projetos/01-private-label/props.json   --public-dir=projetos/01-private-label/public
npx remotion still src/index.ts Feed out/t4-feed120.png --frame=120   --props=projetos/01-private-label/props.json   --public-dir=projetos/01-private-label/public
```

**Abra `out/t4-feed300.png` em recorte ampliado da faixa de legenda** (lição 13 — em miniatura isso
passa batido) e responda por escrito:

1. a legenda ainda **vaza** a borda direita do vídeo? Antes vazava 128,00 px (medido). Depois tem que
   estar 16,00 px **dentro** dele.
2. a legenda continua caber em **duas linhas**? É a invariante que a Tarefa 7 do plano de qualidade
   promove, e o `PISO_DE_DOMINANCIA` desta tarefa depende dela. Se passou de duas linhas, a Tarefa 7
   tem que rodar antes da Tarefa 9.
3. o corpo da legenda ficou legível a 360 px de largura? (`--portao=telefone` mede isso; aqui é para
   o olho.)

E o par que a D2 pede, para o Rafael olhar antes da Tarefa 9 mudar a manchete do 1:1:

Run:
```
cd instagram/remotion
npx remotion still src/index.ts Feed out/t4-feed-cartela.png --frame=120   --props=projetos/01-private-label/props.json   --public-dir=projetos/01-private-label/public
```
Expected: o Feed 1:1 com a manchete **em cartela** (o `props.json` de hoje já pede
`modo: 'cartela'`). Descreva por escrito: qual é o corpo aparente, e a manchete domina o quadro ou a
legenda domina. Guarde a resposta — é o antes da comparação da Tarefa 9, onde o briefing passa a
declarar `pista: "tela"` para pedir a mesma cartela.

- [ ] **Step 11: commit**

```bash
git add instagram/remotion/src instagram/remotion/tests
git commit -m "$(cat <<'MSG'
Layout: pistas sobre a coluna de texto, 4:5, encaixe derivado e dominancia em area

E o conserto de uma linha em layout.ts: a largura da caixa de legenda partia de
video.x+16k e o x usava seguro.x, o que a fazia vazar o video em 128,00 px no 1:1.
A intersecao manchete x legenda vai de 90,20 px a 0,00 nos quatro formatos.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 4A: `sondar()` passa a servir para FOTO — EXIF `Orientation`, e nada inventado

**Tarefa nova, entrou com a revisão da spec (§3.3.3), e é a correção mais grave dela.** A spec
anterior nomeava `sondar()` como o mecanismo que preenche `razaoExibicao` — *"quem preenche o campo é
`sondar()`, não o dedo"* — e `sondar()` **não serve para foto**. Reproduzido: empacotando
`src/motor/sondar.ts` com `esbuild` e rodando sobre
`base-curada/01-real-verificada/torrefacao-uberlandia-875m/packshot-classico/Classico (5).jpg`, ele
devolve

```json
{"largura":4096,"altura":2304,"rotacao":0,"razao":1.7777777777777777,
 "duracao":0.04,"fps":25,"fpsMedio":25,"codificada":{"largura":4096,"altura":2304}}
```

Três defeitos numa resposta: **razão 1,7778** quando a de exibição é **0,5625**; **`rotacao: 0`** num
arquivo cujo EXIF traz `Orientation = 6`; e **`fps: 25` e `duracao: 0.04` inventados** para uma foto
parada. A causa está em `sondar.ts:189-199`: ele honra só `side_data_list.rotation`, que é o
**displaymatrix**, metadado de contêiner de vídeo, e `grep -in "exif\|orientation" src/motor/sondar.ts`
= **0 linhas**.

**Este é o terceiro caso do mesmo padrão neste repositório, e o padrão é o achado:**

1. `pl.mp4` grava 1024×576 com `displaymatrix -90` e exibe 576×1024 — foi o que motivou `sondar()`.
2. Os três recortes em `projetos/01-private-label/public/assets/` são **4096×2304, deitados**, com o
   `Orientation 6` da origem nunca aplicado — e o laudo `instagram/assets/embalagem/suave-250g.json`
   grava `"dimensoes": [4096, 2304]`.
3. `sondar()` sobre foto.

> **Regra, não acidente:** em todo ponto onde este motor recebe um arquivo de imagem ou vídeo, a
> dimensão de exibição é **derivada de metadado de rotação**, e o metadado tem dois nomes por
> tecnologia: `side_data_list.rotation` (displaymatrix, contêiner de vídeo) e EXIF `Orientation`
> (JPEG/TIFF). Ler `width`/`height` sem os dois é o defeito padrão deste repositório, e ele já custou
> três rodadas.

**A decisão é estender, não criar outro mecanismo, e ela é sustentada por medição:** o **mesmo**
`ffprobe` que `sondar()` já resolve expõe o EXIF. Medido em 01/10/2026 com
`ffprobe -show_frames -read_intervals '%+#1' -show_format`:

| arquivo | `format_name` | `width`×`height` | `frames[0].tags.Orientation` | `side_data_list` |
|---|---|---|---|---|
| `IMG_1398.JPG` (a foto da peça de prova) | `image2` | 4032×3024 | `"    1"` | ausente |
| `Classico (5).jpg` (packshot) | `image2` | 4096×2304 | `"    6"` | ausente |
| `suave-250g.png` (recorte já publicado) | `image2` | 4096×2304 | **ausente** | ausente |
| `pl.mp4` | `mov,mp4,m4a,3gp,3g2,mj2` | 1024×576 | ausente | `rotation: -90` |

Três coisas que essa tabela decide, e nenhuma delas é suposição: o valor do `Orientation` **vem
preenchido de espaços** (`"    6"`), então comparação de string falha em silêncio e é obrigatório
`Number()`; `format_name === 'image2'` é o sinal de foto parada, e vale para JPEG **e** PNG; e o
recorte PNG **não tem** `Orientation`, o que confirma o caso (2) acima — a rotação foi perdida na
publicação, não está esperando no arquivo.

**Nenhuma dependência nova. Nenhum parser de EXIF escrito à mão.**

**Files:**
- Modify: `instagram/remotion/src/motor/sondar.ts` (o tipo `Sonda` e a chamada do ffprobe)
- Modify: `instagram/remotion/tests/sondar.test.ts` (**6 `it` hoje**, medido; dois deles mudam de forma)

- [ ] **Step 1: escrever os testes que falham**

Em `tests/sondar.test.ts`, **trocar** a asserção de rotação (era `expect(r.rotacao).toBe(-90)`) por:

```ts
    // `rotacao` deixou de ser um numero: um `0` que significa "nao achei metadado"
    // e um `0` que significa "medi e e zero" sao fatos DIFERENTES, e um deles e um
    // alarme. Agora ela diz de onde veio.
    expect(r.rotacao.graus).toBe(-90);
    expect(r.rotacao.fonte).toBe('displaymatrix');
```

E acrescentar ao fim do arquivo:

```ts
// ---------------------------------------------------------------------------
// FOTO. Tudo abaixo e o que `sondar()` errava em 01/10/2026: ele devolvia razao
// 1,7778 para um arquivo que exibe 0,5625, `rotacao: 0` num Orientation 6, e
// inventava `fps: 25` / `duracao: 0.04` para uma imagem parada.

// Os caminhos seguem a convencao que o arquivo JA usa (`PL`, linhas 8-10): resolvidos
// a partir do arquivo de teste com `fileURLToPath(new URL(...))`, para o teste passar
// rodando de qualquer diretorio. De `tests/` ate a raiz do repositorio sao TRES
// niveis: `tests/` -> `instagram/remotion/` -> `instagram/` -> raiz.
const cam = (rel: string) => fileURLToPath(new URL(rel, import.meta.url));
const PACKSHOT = cam(
  '../../../base-curada/01-real-verificada/torrefacao-uberlandia-875m/packshot-classico/Classico (5).jpg',
);
const FOTO_LAVOURA = cam(
  '../../../base-curada/01-real-verificada/fazenda-medeiros-1250m/cafezal/IMG_1398.JPG',
);
const RECORTE = cam('../projetos/01-private-label/public/assets/suave-250g.png');

describe('sondar sobre FOTO', () => {
  it('honra o EXIF Orientation 6: 4096x2304 gravado exibe 2304x4096', async () => {
    const r = await sondar(PACKSHOT);
    expect(r.codificada).toEqual({largura: 4096, altura: 2304});
    expect(r.largura).toBe(2304);
    expect(r.altura).toBe(4096);
    expect(r.razao).toBeCloseTo(0.5625, 6);
    expect(r.rotacao.fonte).toBe('exif');
    expect(r.rotacao.graus).toBe(90);
  });

  it('Orientation 1 nao troca nada, e diz que MEDIU o zero', async () => {
    // A diferenca que o campo `{fonte, graus}` existe para fazer: aqui o zero foi
    // medido; num arquivo sem metadado nenhum ele seria `fonte: 'nenhuma'`.
    const r = await sondar(FOTO_LAVOURA);
    expect(r.largura).toBe(4032);
    expect(r.altura).toBe(3024);
    expect(r.razao).toBeCloseTo(4 / 3, 6);
    expect(r.rotacao.fonte).toBe('exif');
    expect(r.rotacao.graus).toBe(0);
  });

  it('NAO inventa fps nem duracao para imagem parada', async () => {
    // O ffprobe devolve `r_frame_rate: 25/1` e `duration: 0.040000` para todo
    // `image2`, e os dois sao artefato do demuxer, nao medida do arquivo. Numero
    // inventado e pior que ausencia -- licao 3 do CLAUDE.md.
    const r = await sondar(FOTO_LAVOURA);
    expect(r.duracao).toBeNull();
    expect(r.fps).toBeNull();
    expect(r.fpsMedio).toBeNull();
    expect(r.imagemParada).toBe(true);
  });

  it('o recorte de embalagem publicado esta DEITADO e sem Orientation', async () => {
    // O caso (2) do padrao: os tres PNG de `public/assets/` sao 4096x2304 deitados e
    // o `Orientation 6` da origem NAO esta no arquivo -- ele foi perdido na
    // publicacao. Este teste e o que impede alguem de "consertar" isso supondo que o
    // metadado esteja la esperando.
    const r = await sondar(RECORTE);
    expect(r.codificada).toEqual({largura: 4096, altura: 2304});
    expect(r.largura).toBe(4096);
    expect(r.rotacao.fonte).toBe('nenhuma');
    expect(r.rotacao.graus).toBe(0);
    expect(r.imagemParada).toBe(true);
  });

  it('video continua com fps e duracao, e imagemParada e false', async () => {
    const r = await sondar(PL);
    expect(r.imagemParada).toBe(false);
    expect(r.duracao).not.toBeNull();
    expect(r.fps).not.toBeNull();
  });
});
```

`PL` é a constante que o arquivo já tem (linhas 8–10, medido) e ela já usa
`fileURLToPath(new URL(...))` — o `cam()` acima é a mesma receita, nomeada. `base-curada/` é
**gitignorado e pesado, e vive só no diretório principal**: os tres testes que leem `base-curada/` falham num worktree, e
isso está certo — a alternativa seria copiar 4 MB de foto para dentro de `tests/`. Se você estiver num
worktree, rode `npx vitest run tests/sondar.test.ts` a partir do diretório principal.

- [ ] **Step 2: rodar e conferir que falha**

Run: `cd instagram/remotion && npx vitest run tests/sondar.test.ts`
Expected: FALHA. As duas primeiras por tipo (`r.rotacao.graus` é `undefined` porque `rotacao` é
`number`), a terceira com `expected 0.04 to be null`, a quarta com `expected 4096 to be ...`.

- [ ] **Step 3: estender `src/motor/sondar.ts`**

1. Trocar os três campos do tipo `Sonda`:

```ts
export type Sonda = {
  /** largura de EXIBICAO, ja com a rotacao aplicada */
  largura: number;
  /** altura de EXIBICAO, ja com a rotacao aplicada */
  altura: number;
  /**
   * De onde a rotacao veio, e quantos graus.
   *
   * POR QUE NAO E SO UM NUMERO. Um `0` que significa "nao achei metadado" e um `0`
   * que significa "medi e e zero" sao fatos diferentes, e um deles e um alarme: se
   * a fonte e `nenhuma` num JPEG de camera, ou a foto foi reescrita por um editor
   * que apagou o EXIF, ou o `Orientation` esta la e nao foi lido. Devolver `0` nos
   * dois casos foi exatamente como o defeito de 01/10/2026 passou despercebido.
   */
  rotacao: {fonte: 'displaymatrix' | 'exif' | 'nenhuma'; graus: number};
  /** largura/altura de EXIBICAO */
  razao: number;
  /** `true` quando o fluxo tem um frame so (`format_name === 'image2'`) */
  imagemParada: boolean;
  /** segundos. `null` em imagem parada: o 0,04 do ffprobe e do demuxer, nao do arquivo */
  duracao: number | null;
  /** r_frame_rate. `null` em imagem parada: os 25 fps do ffprobe sao ficcao */
  fps: number | null;
  /** avg_frame_rate. `null` em imagem parada */
  fpsMedio: number | null;
  /** dimensao como esta gravada no container, antes da rotacao */
  codificada: {largura: number; altura: number};
  /** o binario que respondeu, para o relato de falha */
  ffprobe: string;
};
```

2. Acrescentar ao tipo `FluxoFfprobe` nada — o EXIF não vem no fluxo, vem no **frame**. Declarar os
dois tipos novos ao lado dele:

```ts
type FrameFfprobe = {tags?: Record<string, string>};
type FormatoFfprobe = {duration?: string; format_name?: string};
```

3. A tabela EXIF, acima de `sondar()`:

```ts
/**
 * EXIF `Orientation` -> graus de rotacao no sentido do displaymatrix.
 *
 * A tabela EXIF tem 8 valores; 2, 4, 5 e 7 incluem espelhamento, que este motor NAO
 * aplica -- ele so troca largura por altura quando preciso. Espelhar uma foto de
 * produto trocaria o lado do rotulo, e isso e alteracao de arte, nao de
 * enquadramento.
 *
 * 5, 6, 7 e 8 trocam os eixos. E so isso que a dimensao de exibicao precisa saber.
 */
const GRAUS_DO_ORIENTATION: Record<number, number> = {
  1: 0,
  2: 0,
  3: 180,
  4: 180,
  5: 90,
  6: 90,
  7: 270,
  8: 270,
};
```

4. Acrescentar `-show_frames -read_intervals '%+#1'` à chamada. **Um frame só**: o custo não é o do
arquivo inteiro.

```ts
    ({stdout} = await exec(
      ffprobe,
      [
        '-v',
        'error',
        '-print_format',
        'json',
        '-show_streams',
        '-show_format',
        // O EXIF vem nas TAGS DO FRAME, nao do fluxo. `%+#1` pede UM frame: medido,
        // e o mesmo binario que ja estava aqui, sem dependencia nova.
        '-show_frames',
        '-read_intervals',
        '%+#1',
        absoluto,
      ],
      {maxBuffer: 16 * 1024 * 1024},
    ));
```

5. Trocar a declaração do JSON e o bloco de rotação/duração pelo seguinte (substitui de
`let j: {streams?...}` até o `return`):

```ts
  let j: {streams?: FluxoFfprobe[]; frames?: FrameFfprobe[]; format?: FormatoFfprobe};
  try {
    j = JSON.parse(stdout);
  } catch {
    throw new Error(`ffprobe devolveu JSON invalido para ${absoluto}`);
  }

  const v = (j.streams ?? []).find((s) => s.codec_type === 'video');
  if (!v) throw new Error(`sem faixa de video em ${absoluto}`);
  if (!v.width || !v.height) {
    throw new Error(`ffprobe nao devolveu dimensao para ${absoluto}`);
  }

  // IMAGEM PARADA. Medido em 01/10/2026: `format_name` e `image2` para JPEG e para
  // PNG, e `mov,mp4,m4a,3gp,3g2,mj2` para o `pl.mp4`. Para todo `image2` o ffprobe
  // devolve `r_frame_rate: 25/1` e `duration: 0.040000` -- os dois sao artefato do
  // demuxer e nao medida do arquivo.
  const imagemParada = (j.format?.format_name ?? '') === 'image2';

  // ROTACAO, por DOIS metadados, nesta ordem de prioridade.
  //
  // O displaymatrix vence porque, quando os dois existem, ele e o que o contêiner de
  // video declara e e o que um player honra. Na pratica eles nao coexistem: medido,
  // `pl.mp4` tem displaymatrix e nenhum `Orientation`, e os JPEG tem `Orientation` e
  // nenhum side_data.
  const rotacao = (() => {
    const bruto = v.side_data_list?.find((s) => s.rotation !== undefined)?.rotation;
    if (bruto !== undefined && Number.isFinite(Number(bruto))) {
      return {fonte: 'displaymatrix' as const, graus: Number(bruto)};
    }
    // O ffprobe devolve o Orientation PREENCHIDO DE ESPACOS (`"    6"`, medido).
    // `Number()` sobre a string resolve; comparacao de string falharia em silencio,
    // e silencio aqui e a razao de o defeito ter durado tres rodadas.
    const cru = j.frames?.[0]?.tags?.Orientation;
    const n = cru === undefined ? NaN : Number(String(cru).trim());
    if (Number.isFinite(n) && n in GRAUS_DO_ORIENTATION) {
      return {fonte: 'exif' as const, graus: GRAUS_DO_ORIENTATION[n]};
    }
    return {fonte: 'nenhuma' as const, graus: 0};
  })();

  const normalizada = ((Math.round(rotacao.graus) % 360) + 360) % 360;
  const trocado = normalizada === 90 || normalizada === 270;

  const largura = trocado ? v.height : v.width;
  const altura = trocado ? v.width : v.height;

  const fps = imagemParada ? null : taxa(v.r_frame_rate);
  const fpsMedio = imagemParada ? null : taxa(v.avg_frame_rate) || fps;
  const duracao = imagemParada
    ? null
    : Number(v.duration ?? j.format?.duration ?? 0);

  return {
    largura,
    altura,
    rotacao,
    razao: largura / altura,
    imagemParada,
    duracao,
    fps,
    fpsMedio,
    codificada: {largura: v.width, altura: v.height},
    ffprobe,
  };
```

- [ ] **Step 4: rodar o teste e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/sondar.test.ts`
Expected: `Tests 11 passed (11)` — os 6 de antes (um deles com a asserção de forma trocada) mais os 5
de foto.

- [ ] **Step 5: fechar a lista do compilador — quem lia `rotacao`, `duracao` ou `fps`**

`rotacao` mudou de `number` para objeto, e `duracao`/`fps` passaram a admitir `null`. O compilador
enumera os pontos de chamada, e essa é a razão de a mudança ser de **tipo** e não de valor.

Run: `cd instagram/remotion && npm run tsc`

Os pontos conhecidos, medidos agora com
`grep -rn "sondar(" scripts/ src/ tests/`: `scripts/conferir.mjs:130` (imprime
`fonte.duracao.toFixed(2)` e `fonte.fps.toFixed(2)`) e `scripts/conferir.mjs` no portão 4, que passa
`duracaoS: fonte.duracao`. `.mjs` não é checado pelo `tsc`, então **estes dois não aparecem na lista e
quebram em tempo de execução** — conserte-os no mesmo passo:

```js
  // `sondar()` devolve `null` para imagem parada desde 01/10/2026. Aqui o alvo e
  // sempre um MP4 renderizado, mas imprimir `null.toFixed` seria um TypeError a
  // esperar o dia em que alguem aponte o portao para um still.
  if (fonte.duracao === null || fonte.fps === null) {
    throw new Error(
      `${video} nao e um video: sondar() diz imagem parada. Os portoes conferem a ` +
        'peca renderizada, nao um still.',
    );
  }
```

Run: `cd instagram/remotion && npm run tsc`
Expected: sem saída.

- [ ] **Step 6: medir a razão de exibição das fontes que os briefings vão declarar**

Este passo produz os números que as Tarefas 5 e 13 escrevem nos briefings. **Meça, não copie.**

Run:
```
cd instagram/remotion
node --experimental-strip-types -e "
const {sondar} = await import('./src/motor/sondar.ts');
for (const f of [
  'projetos/01-private-label/public/fonte/pl.mp4',
  '../../base-curada/01-real-verificada/fazenda-medeiros-1250m/cafezal/IMG_1398.JPG',
]) {
  const s = await sondar(f);
  console.log(f);
  console.log('  exibicao', s.largura + 'x' + s.altura, '| razao', s.razao.toFixed(6));
  console.log('  codificada', s.codificada.largura + 'x' + s.codificada.altura,
              '| rotacao', s.rotacao.fonte, s.rotacao.graus,
              '| imagemParada', s.imagemParada);
}"
```
Expected, e estes números são os que os briefings usam:

| arquivo | exibição | `razaoExibicao` | rotação |
|---|---|---|---|
| `pl.mp4` | 576×1024 | **0,562500** | `displaymatrix -90` |
| `IMG_1398.JPG` | 4032×3024 | **1,333333** | `exif 0` |

- [ ] **Step 7: o aviso que fecha a armadilha do dedo**

`razaoExibicao` no briefing é campo de número, então nada impede o dedo de escrever `1.3333`. **E o
dedo já escreveu:** o protótipo `out/_spec-briefing/b-jornada-foto.json` declara
`razaoExibicao: 1.3333` para `IMG_1421.JPG` e `IMG_1424.JPG`, e os dois são `Orientation 6`, ou seja
**0,75** — duas das três fotos daquele briefing estão erradas pela razão exata desta tarefa.

Por isso o portão de ritmo (Tarefa 10) **confere `razaoExibicao` declarada contra `sondar()` medida,
com tolerância 0,005**. O campo existe para ser conferido, não para ser acreditado. Nada a fazer neste
passo além de confirmar que a Tarefa 10 tem a checagem — marque quando tiver lido a lista de lá.

- [ ] **Step 8: commit**

```bash
git add instagram/remotion/src/motor/sondar.ts instagram/remotion/tests/sondar.test.ts \
  instagram/remotion/scripts/conferir.mjs
git commit -m "$(cat <<'MSG'
Sondar: EXIF Orientation, e nada inventado para imagem parada

O mesmo ffprobe expoe o EXIF; rotacao passa a dizer de onde veio; fps e duracao
viram null num fluxo de um frame.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 5: o briefing como esquema zod

O `briefing.json` é **a verdade humana**: editável à mão, com **um relógio só** (segundos
contados do início da cena). O esquema valida a **forma**; sentido é a Tarefa 6 e aritmética é a
Tarefa 7.

Duas regras de dependência, medidas:

1. **`zod` e `@remotion/zod-types` são dependências fantasma.** `node_modules/zod` é 4.5.4 e
   `node_modules/@remotion/zod-types` é 4.0.530, e **nenhum dos dois está no `package.json`**.
   `npm ci` numa máquina limpa derruba qualquer schema. Esta tarefa declara `zod`.
2. **`@remotion/zod-types` NÃO entra em `src/briefing/esquema.ts`.** O `package.json` dele
   declara `"dependencies": {"remotion": "4.0.530"}`, ou seja arrasta `remotion` para dentro de
   qualquer módulo que o vitest carregue — o modo de falha que `tipografia.ts` já pagou com
   `TypeError: Invalid URL`. `zColor()` e `zTextarea()`, se um dia entrarem, moram só em
   `esquema-studio.ts`, na fronteira do Studio.

**Files:**
- Modify: `instagram/remotion/package.json` (declarar `zod`)
- Create: `instagram/remotion/src/briefing/esquema.ts`
- Create: `instagram/remotion/tests/esquema.test.ts`
- Create: `instagram/remotion/projetos/01-private-label/briefing.json` (o exemplo comentado, que é o que o Rafael edita)

- [ ] **Step 1: declarar `zod` em `package.json`**

Em `instagram/remotion/package.json`, dentro de `"dependencies"`, acrescentar **sem caret** (a
versão que já está no `node_modules` e no lock), depois de `"remotion"`:

```json
    "remotion": "^4.0.530",
    "zod": "4.5.4"
```

Run: `cd instagram/remotion && npm ls zod`
Expected: `zod@4.5.4` listado como dependência direta, sem `invalid`.

- [ ] **Step 2: escrever o teste que falha**

Criar `instagram/remotion/tests/esquema.test.ts`:

```ts
import {describe, expect, it} from 'vitest';
import {
  FORMATOS,
  LICENCAS,
  SERIES,
  zBriefing,
  zCena,
  zEventoTexto,
  zFonte,
} from '../src/briefing/esquema';

/**
 * O briefing minimo que passa: uma cena, uma fonte de cor, nenhum evento.
 *
 * `audio` E OBRIGATORIO e esta aqui. Nao da para ter um "minimo" sem ele: peca de
 * foto parada sem faixa perde elegibilidade para nao-seguidor (`05-formatos.md` §3,
 * [oficial]), e a versao anterior deste esquema tinha `trilha?: Trilha` com o
 * comentario "obrigatoria se nao houver locucao" -- condicionando a obrigatoriedade
 * a um campo que NAO EXISTIA em parte nenhuma do esquema.
 */
const MINIMO = {
  _esquema: 'canastra-briefing/1',
  serie: 'avulsa',
  formatos: ['9:16'],
  duracao: {modo: 'somaCenas'},
  cenas: [
    {duracaoS: 3, fonte: {tipo: 'cor', cor: '#3B2A1F'}, eventos: []},
  ],
  transicoes: [],
  audio: {
    locucao: null,
    trilha: {
      arquivo: 'ambiente.wav',
      ganhoDb: -18,
      aparaAntesS: 0,
      loopar: true,
      fadeEntradaS: 0.5,
      fadeSaidaS: 0.8,
    },
  },
  gancho: 'o gancho desta peca de teste',
  cta: 'chama no direct',
};

describe('zBriefing', () => {
  it('aceita o briefing minimo e aplica os defaults declarados', () => {
    const b = zBriefing.parse(MINIMO);
    expect(b.fps).toBe(30);
    // As 12 licencas nascem TODAS desligadas. Nenhuma tecnica que colide com
    // proibicoes.md entra por omissao.
    for (const chave of LICENCAS) expect(b.licencas[chave]).toBe(false);
    expect(b.licencas.justificativa).toBe('');
  });

  it('recusa campo desconhecido em vez de ignorar em silencio', () => {
    // A licao 3 do CLAUDE.md: HTTP 200 ignorando o parametro. Um briefing com
    // `"duracao_alvo": 24` em vez de `duracao.alvoS` tem que FALHAR, nao render
    // 3 s e sair com exit 0.
    const r = zBriefing.safeParse({...MINIMO, duracao_alvo: 24});
    expect(r.success).toBe(false);
  });

  it('recusa fps fora de 1..120 e fps fracionario', () => {
    expect(zBriefing.safeParse({...MINIMO, fps: 0}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, fps: 121}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, fps: 29.97}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, fps: 60}).success).toBe(true);
  });

  it('duracao.modo NAO tem default: briefing sem ele falha', () => {
    // Sem default de proposito. Um default aqui seria escolha estetica
    // disfarcada de conveniencia: quem pedir 24 s receberia 22,4 s sem perceber
    // na primeira peca que usar crossfade.
    const {duracao, ...semModo} = MINIMO;
    void duracao;
    expect(zBriefing.safeParse(semModo).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, duracao: {}}).success).toBe(false);
  });

  it('exige pelo menos uma cena e pelo menos um formato', () => {
    expect(zBriefing.safeParse({...MINIMO, cenas: []}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, formatos: []}).success).toBe(false);
  });

  it('os 12 slugs de serie de 05-formatos.md, mais avulsa', () => {
    expect(SERIES.length).toBe(13);
    expect(SERIES).toContain('voce-sabia');
    expect(SERIES).toContain('objecao-preco');
    expect(SERIES).toContain('avulsa');
    expect(zBriefing.safeParse({...MINIMO, serie: 'inventada'}).success).toBe(false);
  });

  it('os quatro formatos, e 4:5 entre eles', () => {
    expect([...FORMATOS]).toEqual(['9:16', '1:1', '4:5', '16:9']);
  });

  it('`audio` e OBRIGATORIO: briefing sem ele falha', () => {
    // A ausencia A4. Medido em 30/09/2026: `grep -rn "Audio" src/` so achava
    // `motor/audio/normalizar.ts`, que e medicao POS-render. Nao havia `<Audio>` na
    // arvore e todo som era carona do `<Video>` -- logo TODA peca de foto parada
    // saia muda, e 5 das 12 series do catalogo partem de foto parada.
    const {audio, ...semAudio} = MINIMO;
    void audio;
    expect(zBriefing.safeParse(semAudio).success).toBe(false);
  });

  it('locucao e trilha podem ser null, mas NAO as duas', () => {
    // A regra escrita sobre campos que EXISTEM. O esquema aceita a forma; a recusa
    // dos dois nulos e do refinador (Tarefa 6), porque ela cita um criterio
    // [oficial] e a mensagem e o que ensina.
    expect(zBriefing.safeParse({...MINIMO, audio: {locucao: null, trilha: null}}).success).toBe(
      true,
    );
    // ausente nao e o mesmo que null: `null` e uma declaracao, ausencia e esquecimento
    expect(zBriefing.safeParse({...MINIMO, audio: {trilha: null}}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, audio: {locucao: null}}).success).toBe(false);
  });

  it('a trilha exige loopar, fadeEntradaS e fadeSaidaS -- SEM default', () => {
    // Uma trilha de 20 s numa peca de 40 s e ou loop ou silencio na metade, e isso
    // nao se decide por conveniencia.
    const t = {arquivo: 'ambiente.wav', ganhoDb: -18, aparaAntesS: 0};
    expect(zBriefing.safeParse({...MINIMO, audio: {locucao: null, trilha: t}}).success).toBe(
      false,
    );
    expect(
      zBriefing.safeParse({
        ...MINIMO,
        audio: {locucao: null, trilha: {...t, loopar: true, fadeEntradaS: 0, fadeSaidaS: 0}},
      }).success,
    ).toBe(true);
  });

  it('NAO existe campo de LUFS no briefing', () => {
    // `AUDIO = {lufs: -14, picoDbtp: -1}` e alvo de POS-render: quem o aplica e
    // `scripts/normalizar-audio.mjs:90`, sobre a MISTURA, com `-c:v copy`. Um alvo
    // por faixa aqui seria uma segunda verdade que o normalizador sobrescreve sem
    // avisar -- e o prototipo `out/_spec-briefing/a-private-label.json` trazia
    // `alvoLufs`, que por isso NAO entra.
    const t = {
      arquivo: 'ambiente.wav',
      ganhoDb: -18,
      aparaAntesS: 0,
      loopar: false,
      fadeEntradaS: 0,
      fadeSaidaS: 0,
      alvoLufs: -14,
    };
    expect(zBriefing.safeParse({...MINIMO, audio: {locucao: null, trilha: t}}).success).toBe(
      false,
    );
  });
});

describe('zLegenda', () => {
  const legenda = {arquivo: 'transcricao.json', relogio: 'fonte', ancora: {tipo: 'locucao'}};

  it('`relogio` e um enum de UM valor: declarar e o ponto, nao escolher', () => {
    expect(zBriefing.safeParse({...MINIMO, legenda}).success).toBe(true);
    expect(
      zBriefing.safeParse({...MINIMO, legenda: {...legenda, relogio: 'peca'}}).success,
    ).toBe(false);
  });

  it('a ancora tem TRES casos, e nenhum deles e implicito', () => {
    // Com N cenas ha N valores de `aparaAntesS` e UMA legenda: somar "o"
    // `aparaAntesS` deixa de ser definido. A resolucao e nomear o instante da
    // transcricao que cai no frame 0 da peca -- ver spec §2.2.1.
    for (const ancora of [
      {tipo: 'locucao'},
      {tipo: 'cena', indice: 0},
      {tipo: 'segundo', valorS: 1.14},
    ]) {
      expect(zBriefing.safeParse({...MINIMO, legenda: {...legenda, ancora}}).success, JSON.stringify(ancora)).toBe(true);
    }
    expect(
      zBriefing.safeParse({...MINIMO, legenda: {...legenda, ancora: {tipo: 'inventado'}}})
        .success,
    ).toBe(false);
    // `ancora` ausente NAO passa: sem ela o compilador teria que escolher a cena 0
    // por conveniencia, que e o default escondido que esta spec proibe.
    const {ancora, ...semAncora} = legenda;
    void ancora;
    expect(zBriefing.safeParse({...MINIMO, legenda: semAncora}).success).toBe(false);
  });

  it('NAO existe `aparaAntesS` na legenda: o nome dela e `ancora`', () => {
    expect(
      zBriefing.safeParse({...MINIMO, legenda: {...legenda, aparaAntesS: 1.14}}).success,
    ).toBe(false);
  });
});

describe('zAsset', () => {
  it('recorte de embalagem exige `laudoExigido: true` LITERAL', () => {
    const a = {arquivo: 'suave-250g.png', tipo: 'recorte-embalagem', laudoExigido: true};
    expect(zBriefing.safeParse({...MINIMO, assets: [a]}).success).toBe(true);
    expect(zBriefing.safeParse({...MINIMO, assets: [{...a, laudoExigido: false}]}).success).toBe(
      false,
    );
    // lista vazia e valido: a maioria das pecas nao tem recorte de embalagem
    expect(zBriefing.safeParse({...MINIMO, assets: []}).success).toBe(true);
  });

  it('o laudo NAO e copiado para dentro do briefing', () => {
    // Copiar `aprovado: true` para ca criaria a segunda fonte de verdade, e um humano
    // podendo digitar `aprovado: true` a mao transformaria o portao fail-closed de
    // `publicar.py:82` em decoracao. A prova e a PRESENCA do arquivo em
    // `public/assets/`, e quem a confere e o portao de ritmo.
    const a = {
      arquivo: 'suave-250g.png',
      tipo: 'recorte-embalagem',
      laudoExigido: true,
      aprovado: true,
    };
    expect(zBriefing.safeParse({...MINIMO, assets: [a]}).success).toBe(false);
  });
});

describe('zFonte', () => {
  it('video exige razaoExibicao MEDIDA e apara em segundos', () => {
    expect(
      zFonte.safeParse({
        tipo: 'video',
        arquivo: 'pl.mp4',
        razaoExibicao: 0.5625,
        aparaAntesS: 1.14,
        enquadramento: 'preencher',
        camera: 'parado',
      }).success,
    ).toBe(true);
    // Sem razaoExibicao nao passa: `pl.mp4` grava 1024x576 e exibe 576x1024
    // (displaymatrix -90). Quem preenche este campo e `sondar()`, nao o dedo.
    const r = zFonte.safeParse({
      tipo: 'video',
      arquivo: 'pl.mp4',
      aparaAntesS: 0,
      enquadramento: 'preencher',
      camera: 'parado',
    });
    expect(r.success).toBe(false);
  });

  it('foto exige `registro` SEM default -- e a regra da marca por construcao', () => {
    // proibicoes.md:24: "Foto real entra por um registro que declara a origem
    // (moldura, cartao, tela cheia), nunca como recorte flutuando." Sem default,
    // a regra e cumprida por construcao em vez de por lembranca.
    const base = {
      tipo: 'foto',
      arquivo: 'cafezal.jpg',
      razaoExibicao: 4032 / 3024,
      enquadramento: {tipo: 'faixa'},
      camera: 'pushLento',
    };
    expect(zFonte.safeParse(base).success).toBe(false);
    expect(zFonte.safeParse({...base, registro: 'telaCheia'}).success).toBe(true);
    expect(zFonte.safeParse({...base, registro: 'inventado'}).success).toBe(false);
  });

  it('recorte de foto e em FRACAO da fonte, nunca em pixel', () => {
    // Fracao para o mesmo briefing servir a foto de 4032x3024 e a regravacao
    // dela em outra resolucao sem reescrever numero.
    const base = {
      tipo: 'foto',
      arquivo: 'cafezal.jpg',
      razaoExibicao: 4032 / 3024,
      registro: 'telaCheia',
      camera: 'pushLento',
    };
    expect(
      zFonte.safeParse({
        ...base,
        enquadramento: {tipo: 'recorte', x: 0.2, y: 0, largura: 0.4218, altura: 1},
      }).success,
    ).toBe(true);
    expect(
      zFonte.safeParse({
        ...base,
        enquadramento: {tipo: 'recorte', x: 0.2, y: 0, largura: 1701, altura: 3024},
      }).success,
    ).toBe(false);
  });

  it('grade aceita 2 a 4 celulas de fonte SIMPLES, e nao grade dentro de grade', () => {
    const celula = {tipo: 'cor', cor: '#4A5D3A'};
    expect(
      zFonte.safeParse({
        tipo: 'grade',
        colunas: 2,
        linhas: 1,
        calha: 8,
        celulas: [celula, celula],
      }).success,
    ).toBe(true);
    expect(
      zFonte.safeParse({tipo: 'grade', colunas: 2, linhas: 1, calha: 8, celulas: [celula]})
        .success,
    ).toBe(false);
    // Recursao em zod obriga anotacao de tipo manual = segunda fonte de verdade.
    // Nenhuma das 12 series pede grade dentro de grade.
    expect(
      zFonte.safeParse({
        tipo: 'grade',
        colunas: 2,
        linhas: 1,
        calha: 8,
        celulas: [celula, {tipo: 'grade', colunas: 2, linhas: 1, calha: 8, celulas: [celula, celula]}],
      }).success,
    ).toBe(false);
  });
});

describe('zEventoTexto', () => {
  // `pista` e OBRIGATORIO: ele esta em todo objeto de evento daqui para baixo.
  const base = {texto: 'X', entradaS: 0, pista: 'topo'} as const;

  it('aceita os tres papeis de evento e RECUSA legenda', () => {
    for (const papel of ['manchete', 'dado', 'etiqueta']) {
      expect(zEventoTexto.safeParse({...base, papel}).success).toBe(true);
    }
    // A legenda e camada de PECA, fora da TransitionSeries. Se `legenda` fosse
    // papel de evento, na janela de crossfade duas legendas com textos
    // diferentes ficariam no ar ao mesmo tempo.
    expect(zEventoTexto.safeParse({...base, papel: 'legenda'}).success).toBe(false);
  });

  it('`pista` e OBRIGATORIO, sem default', () => {
    // A tabela `PISTA_PADRAO` existe em `motor/evento.ts`, mas ela NAO e default do
    // motor: e o que a skill `canastra-briefing` escreve no arquivo. Assim a escolha
    // fica visivel no JSON, onde o Rafael a le e a muda, em vez de morar no codigo.
    const {pista, ...semPista} = base;
    void pista;
    expect(zEventoTexto.safeParse({...semPista, papel: 'manchete'}).success).toBe(false);
  });

  it('`rodape` NAO e pista de evento: ela e da camada Legenda', () => {
    expect(zEventoTexto.safeParse({...base, papel: 'manchete', pista: 'rodape'}).success).toBe(
      false,
    );
    for (const p of ['topo', 'principal', 'tela']) {
      expect(zEventoTexto.safeParse({...base, papel: 'manchete', pista: p}).success).toBe(true);
    }
  });

  it('NAO existe campo `encaixe` no evento: ele e derivado de (pista, formato)', () => {
    // `faixa` x `coluna` nao e escolha, e consequencia do formato: no 9:16 a sobra ao
    // lado do video e 0,00 px (medido), logo `encaixe: ['coluna']` ali e
    // insatisfazivel -- um campo que o motor nao pode honrar e o HTTP 200 que ignora
    // o parametro, licao 3 do CLAUDE.md. Para pedir cartela, declare `pista: 'tela'`.
    expect(
      zEventoTexto.safeParse({...base, papel: 'manchete', encaixe: ['cartela']}).success,
    ).toBe(false);
  });

  it('entradaS e relativo a CENA, e negativo nao existe', () => {
    expect(zEventoTexto.safeParse({...base, papel: 'manchete', entradaS: -1}).success).toBe(
      false,
    );
  });

  it('texto vazio nao e evento', () => {
    expect(zEventoTexto.safeParse({...base, papel: 'manchete', texto: '   '}).success).toBe(
      false,
    );
  });

  it('nao existe campo de cadencia no evento: ela vem do papel', () => {
    expect(
      zEventoTexto.safeParse({...base, papel: 'manchete', cadencia: 'palavra'}).success,
    ).toBe(false);
  });
});

describe('zCena', () => {
  it('cena com duracao zero ou negativa nao existe', () => {
    const fonte = {tipo: 'cor', cor: '#3B2A1F'};
    expect(zCena.safeParse({duracaoS: 0, fonte, eventos: []}).success).toBe(false);
    expect(zCena.safeParse({duracaoS: -1, fonte, eventos: []}).success).toBe(false);
  });

  it('eventos LISTA VAZIA e cena completa, nao cena quebrada', () => {
    // A propriedade que a Tarefa 5 do plano de qualidade protege com "opcional
    // sem placeholder" sobrevive: lista vazia e peca completa sem evento, sem
    // erro e sem texto de exemplo.
    const fonte = {tipo: 'cor', cor: '#3B2A1F'};
    expect(zCena.safeParse({duracaoS: 2, fonte, eventos: []}).success).toBe(true);
  });
});
```

- [ ] **Step 3: rodar o teste e conferir que falha**

Run: `cd instagram/remotion && npx vitest run tests/esquema.test.ts`
Expected: FALHA — `Failed to resolve import "../src/briefing/esquema"`.

- [ ] **Step 4: criar `src/briefing/esquema.ts`**

```ts
// A FORMA do briefing, em zod. Sentido e `refinar.ts`; aritmetica e `compilar.ts`.
//
// ZOD PURO, SEM `@remotion/zod-types`
//
// `node_modules/@remotion/zod-types/package.json` declara
// `"dependencies": {"remotion": "4.0.530"}` (medido em 30/09/2026). Importar
// `remotion` num modulo que o vitest carrega e o modo de falha que
// `tipografia.ts` ja pagou: `loadFont` no topo do modulo derruba o vitest com
// `TypeError: Invalid URL`. `zColor()` e `zTextarea()`, quando entrarem, moram em
// `esquema-studio.ts` e so lá.
//
// UM RELOGIO SO: SEGUNDOS, CONTADOS DO INICIO DA CENA
//
// Nenhum campo deste arquivo esta em frames. A posicao de uma cena vem da ORDEM
// no array, nunca de um campo de tempo. A unica conversao do sistema e
// `emFrames(s, fps)` de `motor/relogio.ts`, chamada por `compilar.ts`.
//
// O tempo da FONTE (transcricao, palavra em milissegundo) sobrevive num lugar so:
// o arquivo de transcricao, que DECLARA o relogio dele em `legenda.relogio`.
//
// TODO OBJETO E `strictObject`
//
// Campo desconhecido FALHA em vez de ser ignorado. E a licao 3 do CLAUDE.md
// aplicada a JSON: um briefing com `duracao_alvo: 24` em vez de `duracao.alvoS`
// renderizaria 3 segundos e sairia com exit 0.

import {z} from 'zod';
// `PAPEIS_DE_EVENTO` vem de `motor/evento.ts` e `PISTAS_DE_EVENTO` de
// `motor/pista.ts`, para nao existirem DUAS listas de cada coisa. Os dois modulos sao
// puros, e os unicos imports deles para `identidade/*` sao `import type`, que o
// transpilador apaga -- entao `loadFont` nao e puxado para dentro do vitest por estas
// linhas. `pista.ts` importa `layout.ts` (geometria pura, sem React) e nada mais.
import {PAPEIS_DE_EVENTO} from '../motor/evento';
import {PISTAS_DE_EVENTO} from '../motor/pista';

/** Os 12 slugs de `instagram/estrategia/05-formatos.md` secao 4, mais `avulsa`. */
export const SERIES = [
  'voce-sabia',
  'infografico',
  'arraste',
  'jornada',
  'capsula-parceiro',
  'piada',
  'meme-pacote',
  'preparo-slow',
  'bastidor',
  'objecao-preco',
  'safra-limitada',
  'convidado',
  'avulsa',
] as const;

export const FORMATOS = ['9:16', '1:1', '4:5', '16:9'] as const;
export type Formato = (typeof FORMATOS)[number];

/**
 * Dimensao de cada formato, em pixel.
 *
 * `16:9` fica no enum porque `layout()` o rotula, mas a margem de base dele e
 * 51,03% da altura (medido): e formato LATENTE, nao entrega. Ver §5 da spec.
 */
export const DIMENSAO: Record<Formato, {largura: number; altura: number}> = {
  '9:16': {largura: 1080, altura: 1920},
  '1:1': {largura: 1080, altura: 1080},
  '4:5': {largura: 1080, altura: 1350},
  '16:9': {largura: 1920, altura: 1080},
};

/** As 12 licencas de tecnica. Cada uma nomeia a linha de `proibicoes.md`. */
export const LICENCAS = [
  'particulas', // 11-12: "explosao de particula"
  'orbesDeBrilho', // 11: "brilho"
  'varreduraDeLuz', // 11: "brilho"
  'shockwave', // 11-12: particula + brilho
  'molaComOvershoot', // 11: "easing elastico"
  'revelarCaractereACaractere', // 14: "Revelar texto caractere a caractere"
  'flashNoCorte', // 16: "Flash branco instantaneo"
  'irisWipe', // 16: por vizinhanca com "whip pan"
  'motionBlurBurst', // 7-8: nomeia <CameraMotionBlur>
  'swipeMarcaTexto', // 20: seria o 2o saturado ao lado de COR.acento
  'highlightPalavraAtiva', // nao e proibicao: e 1 acento, mas troca 2,45x/s
  'aceitaTempoMorto', // 11-12: "tempo morto"
] as const;
export type Licenca = (typeof LICENCAS)[number];

const zLicencas = z.strictObject({
  ...Object.fromEntries(LICENCAS.map((k) => [k, z.boolean().default(false)])),
  /**
   * Por que alguma esta ligada. `refinar.ts` reprova licenca ligada com
   * justificativa curta -- ligar uma tecnica que colide com a marca e decisao,
   * e decisao sem motivo escrito nao sobrevive a proxima sessao.
   */
  justificativa: z.string().default(''),
} as Record<Licenca | 'justificativa', z.ZodTypeAny>) as z.ZodType<
  Record<Licenca, boolean> & {justificativa: string}
>;

/**
 * Movimento de camera sobre a fonte.
 *
 * Os nomes sao os da spec §2.3 e os do prototipo
 * `out/_spec-briefing/b-jornada-foto.json`, que ja escrevia `"camera": "pushLento"`. O
 * `Lento` esta no NOME de proposito: `proibicoes.md:21` pede "push de camera lento,
 * nunca impacto", e um enum chamado so `push` convidaria a segunda velocidade.
 */
const zCamera = z.enum(['parado', 'pushLento']);

const zFonteVideo = z.strictObject({
  tipo: z.literal('video'),
  /** nome do arquivo dentro de `public/fonte/`, nunca um caminho */
  arquivo: z.string().min(1),
  /**
   * Razao de EXIBICAO, honrando a matriz de rotacao. MEDIDA por `sondar()`, nunca
   * lida do container: `pl.mp4` grava 1024x576 e exibe 576x1024
   * (`displaymatrix -90`), e os 12 packshots leem 4096x2304 e exibem 2304x4096
   * (`EXIF Orientation 6`). Armadilha ja paga duas vezes.
   */
  razaoExibicao: z.number().positive(),
  /** ar morto da cabeca, em segundos. 1,14 no pl.mp4 */
  aparaAntesS: z.number().min(0),
  aparaDepoisS: z.number().min(0).optional(),
  enquadramento: z.enum(['faixa', 'preencher']),
  camera: zCamera,
});

const zRecorte = z.strictObject({
  tipo: z.literal('recorte'),
  /** em FRACAO da fonte (0..1), nunca em pixel */
  x: z.number().min(0).max(1),
  y: z.number().min(0).max(1),
  largura: z.number().gt(0).max(1),
  altura: z.number().gt(0).max(1),
});

const zFonteFoto = z.strictObject({
  tipo: z.literal('foto'),
  arquivo: z.string().min(1),
  razaoExibicao: z.number().positive(),
  /**
   * OBRIGATORIO, SEM DEFAULT. `proibicoes.md:24`: "Foto real entra por um
   * registro que declara a origem (moldura, cartao, tela cheia), nunca como
   * recorte flutuando." Sem default, a regra da marca e cumprida por construcao.
   */
  registro: z.enum(['moldura', 'cartao', 'telaCheia']),
  /**
   * `faixa` (contain) ou `recorte`. Nenhum e obviamente melhor, e por isso e
   * campo: as 26 fotos da fazenda sao 4032x3024 (razao 1,3333), e num 9:16 de
   * 1080x1920 `faixa` deixa 42,2% da altura como foto (57,8% fundo chapado) e
   * `recorte` joga fora 57,8% da foto.
   */
  enquadramento: z.union([z.strictObject({tipo: z.literal('faixa')}), zRecorte]),
  camera: zCamera,
});

const zFonteCor = z.strictObject({
  tipo: z.literal('cor'),
  /** hex de 6 digitos. Branco puro e proibido (`proibicoes.md:13`) e o refinador o recusa. */
  cor: z.string().regex(/^#[0-9a-fA-F]{6}$/),
});

/** As fontes que podem ser CELULA de grade. Grade nao entra: recursao fora. */
const zFonteSimples = z.discriminatedUnion('tipo', [zFonteVideo, zFonteFoto, zFonteCor]);

const zFonteGrade = z.strictObject({
  tipo: z.literal('grade'),
  colunas: z.union([z.literal(1), z.literal(2)]),
  linhas: z.union([z.literal(1), z.literal(2)]),
  /** calha entre celulas, em px a 1080 de largura */
  calha: z.number().min(0),
  /**
   * 2 a 4 celulas de fonte SIMPLES. Grade dentro de grade e recursao que nenhuma
   * das 12 series pede, e recursao em zod obriga anotacao de tipo manual -- uma
   * segunda fonte de verdade para o mesmo tipo.
   */
  celulas: z.array(zFonteSimples).min(2).max(4),
});

export const zFonte = z.discriminatedUnion('tipo', [
  zFonteVideo,
  zFonteFoto,
  zFonteCor,
  zFonteGrade,
]);
export type Fonte = z.infer<typeof zFonte>;

export const zEventoTexto = z.strictObject({
  /**
   * `legenda` NAO esta aqui de proposito: a legenda e camada de PECA, fora da
   * `TransitionSeries`. Dentro de uma cena ela seria remontada por cena e, na
   * janela de crossfade, duas legendas com textos diferentes ficariam no ar ao
   * mesmo tempo -- bug garantido e invisivel em miniatura.
   */
  papel: z.enum(PAPEIS_DE_EVENTO),
  texto: z.string().trim().min(1),
  /** segundos, relativo ao inicio DA CENA a que o evento pertence */
  entradaS: z.number().min(0),
  /** ausente = `duracaoDaFrase(texto)`, que ja cresce com o stagger */
  duracaoS: z.number().gt(0).optional(),
  /**
   * OBRIGATORIO, sem default.
   *
   * `PISTAS_DE_EVENTO` de `motor/pista.ts`: `topo`, `principal`, `tela`. `rodape`
   * NAO esta na lista -- ela e a caixa da camada `Legenda`, e um evento ali cairia
   * sobre a fala.
   *
   * `PISTA_PADRAO[papel]` existe em `motor/evento.ts` e NAO e aplicado aqui: ele e o
   * que a skill `canastra-briefing` escreve no arquivo. Default no esquema poria a
   * escolha no codigo, onde ninguem a le.
   *
   * O ENCAIXE SAI DELA. `pista: 'tela'` -> cartela. `topo`/`principal` -> faixa ou
   * coluna, conforme a sobra ao lado do video naquele formato (`pista.ts`).
   */
  pista: z.enum(PISTAS_DE_EVENTO),
  /** indice da UNICA palavra que recebe `COR.acento`. `proibicoes.md:20`. */
  palavraAcento: z.number().int().min(0).optional(),
  // NAO existe campo `encaixe`: ele e DERIVADO de (pista, formato). Ver spec §3.4.2.
  // Um campo que o motor nao pode honrar -- `encaixe: ['coluna']` no 9:16, onde a
  // sobra e 0,00 px -- e o HTTP 200 que ignora o parametro.
});
export type EventoTexto = z.infer<typeof zEventoTexto>;

export const zCena = z.strictObject({
  duracaoS: z.number().gt(0),
  fonte: zFonte,
  /** lista VAZIA e cena completa sem evento -- sem erro e sem placeholder */
  eventos: z.array(zEventoTexto),
});
export type Cena = z.infer<typeof zCena>;

const zTransicao = z.discriminatedUnion('tipo', [
  /** 0 frames. E o default, e e o que faz `Sigma cenas` ser a duracao da peca. */
  z.strictObject({tipo: z.literal('corte')}),
  z.strictObject({tipo: z.literal('fade'), duracaoS: z.number().gt(0)}),
  z.strictObject({
    tipo: z.literal('wipe'),
    duracaoS: z.number().gt(0),
    direcao: z.enum(['from-left', 'from-right', 'from-top', 'from-bottom']),
  }),
]);
export type Transicao = z.infer<typeof zTransicao>;

const zLegenda = z.strictObject({
  /** nome do arquivo de transcricao, relativo a raiz do projeto */
  arquivo: z.string().min(1),
  /**
   * O relogio em que os tempos da transcricao estao. **Enum de UM valor**: declarar
   * e o ponto, nao escolher. `peca` saiu porque `relogio: 'peca'` mais
   * `aparaAntesS != 0` era uma contradicao que o esquema aceitava e o refinador
   * tinha que desfazer -- forma que se pode escrever errada e forma errada.
   */
  relogio: z.literal('fonte'),
  /**
   * QUE INSTANTE DA TRANSCRICAO CAI NO FRAME 0 DA PECA. Spec §2.2.1.
   *
   * O buraco que isto fecha: com N cenas ha N valores de `Cena.fonte.aparaAntesS` e
   * UMA legenda, entao somar "o" `aparaAntesS` deixa de ser definido. Hoje o motor
   * tem sorte -- `PecaVideo.tsx:134` passa um numero so porque ha uma cena so.
   *
   * A resolucao e NEGAR a pergunta: nenhum `aparaAntesS` de cena entra no rebase,
   * porque a legenda nao e imagem, e a FALA, e a fala tem uma fonte de audio so.
   *
   *   locucao ....... = `audio.locucao.aparaAntesS`. O caso normal
   *   cena+indice ... = `cenas[indice].fonte.aparaAntesS`. O UNICO jeito de um
   *                     aparaAntesS de cena tocar a legenda, e ele e NOMINAL: quem
   *                     escreve aponta a cena com o dedo
   *   segundo ....... um valor cru, para transcricao que nao veio de nenhum dos dois
   *
   * Sem locucao e sem ancora, o refinador RECUSA -- nao escolhe a cena 0 por
   * conveniencia.
   */
  ancora: z.discriminatedUnion('tipo', [
    z.strictObject({tipo: z.literal('locucao')}),
    z.strictObject({tipo: z.literal('cena'), indice: z.number().int().min(0)}),
    z.strictObject({tipo: z.literal('segundo'), valorS: z.number().min(0)}),
  ]),
  /** quando a pista de legenda entra na PECA. default 0 */
  entradaNaPecaS: z.number().min(0).default(0),
  /** default `LEGENDA.maxPalavras`, que e 2 */
  maxPalavrasPorBloco: z.number().int().min(1).max(6).optional(),
  // NAO existe `aparaAntesS` aqui: o nome dele e `ancora`, e a razao esta acima.
});

// ---- audio: fecha a ausencia A4 ------------------------------------------ §3.6
//
// A VERSAO ANTERIOR TINHA UM CAMPO SO, `trilha?: Trilha`, com o comentario
// "obrigatoria se nao houver locucao" -- e NAO EXISTIA campo de locucao em parte
// nenhuma do esquema. O comentario condicionava a obrigatoriedade a um campo
// inexistente, e sem locucao a peca de foto parada saia muda duas vezes: sem voz e
// sem faixa. O prototipo `out/_spec-briefing/a-private-label.json` ja tinha a forma
// certa (`audio.locucao {arquivo: "pl.wav", ganhoDb: 0, aparaAntesS: 1.14}`).

const zFaixa = z.strictObject({
  /** NOME dentro da subpasta, nunca um caminho */
  arquivo: z.string().min(1),
  /**
   * Ganho RELATIVO na mistura, em dB. **NAO e LUFS.**
   *
   * `scripts/normalizar-audio.mjs` roda DEPOIS do render, sobre o MP4 ja mixado, com
   * `-c:v copy`, e leva a MISTURA a `AUDIO = {lufs: -14, picoDbtp: -1}` dos tokens
   * (medido: `normalizar-audio.mjs:90` le os dois). Logo este campo decide quanto a
   * trilha fica ABAIXO da voz; o nivel final e do normalizador.
   *
   * Ponto de partida [escolhido], sem medicao nossa que o sustente:
   * `locucao.ganhoDb = 0` e `trilha.ganhoDb = -18`. A primeira peca com as duas
   * faixas tem de medir o resultado, e o numero volta para a spec.
   */
  ganhoDb: z.number().min(-60).max(12),
  /** apara (§2.2): de onde o arquivo comeca a tocar. 1,14 no `pl.wav` */
  aparaAntesS: z.number().min(0),
});

const zTrilha = zFaixa.extend({
  /** SEM default: 20 s de trilha numa peca de 40 s e ou loop ou silencio na metade */
  loopar: z.boolean(),
  fadeEntradaS: z.number().min(0),
  fadeSaidaS: z.number().min(0),
});

const zAudio = z.strictObject({
  /** `null` = peca sem voz. NUNCA ausente. */
  locucao: zFaixa.nullable(),
  /** `null` so e aceito COM locucao -- `refinar.ts` cobra, citando [oficial]. */
  trilha: zTrilha.nullable(),
});
// NAO existe campo de LUFS no briefing: o `alvoLufs`/`picoMaximoDbtp` que o
// prototipo trazia fica fora, porque seria uma segunda verdade que o normalizador
// sobrescreve sem avisar.

const zAsset = z.strictObject({
  /** nome dentro de `projetos/<p>/public/assets/` */
  arquivo: z.string().min(1),
  tipo: z.literal('recorte-embalagem'),
  /**
   * LITERAL `true`: recorte sem laudo nao entra.
   *
   * E O LAUDO NAO E COPIADO PARA CA. A prova de que o recorte foi aprovado e a
   * PRESENCA do arquivo em `public/assets/`, porque a unica porta de entrada daquela
   * pasta e `instagram/recorte/publicar.py:82`, que so copia o PNG cujo laudo irmao
   * traz `aprovado is True` -- fail-closed. E por isso que os tres PNG que estao la
   * nao tem `.json` ao lado (medido). Um humano podendo digitar `aprovado: true` aqui
   * transformaria aquele portao em decoracao.
   */
  laudoExigido: z.literal(true),
});

// O NOME E `zBriefingEstrito`, E NAO `zBriefing`, DE PROPOSITO.
//
// O Step 8 acrescenta um `z.preprocess` em volta dele para permitir chave de
// comentario (`_leia`), e `zBriefing` passa a ser esse embrulho. Escrevendo o nome
// certo aqui, o Step 8 fica ADITIVO -- ele nao precisa mandar redigitar um objeto de
// ~50 campos, que e onde um campo se perde.
const zBriefingEstrito = z.strictObject({
  _esquema: z.literal('canastra-briefing/1'),
  serie: z.enum(SERIES),
  /**
   * O fps da peca. CAMPO, nao constante: antes de 01/10/2026 era `FPS = 30` em
   * `Raiz.tsx:22` e nenhuma camada de texto lia `useVideoConfig`.
   */
  fps: z.number().int().min(1).max(120).default(30),
  formatos: z.array(z.enum(FORMATOS)).min(1),
  duracao: z.strictObject({
    /**
     * SEM DEFAULT, de proposito. `somaCenas`: as cenas mandam e `alvoS`, se
     * houver, e conferencia. `totalFixo`: `alvoS` manda e o compilador devolve os
     * frames das transicoes as cenas. Um default aqui seria escolha estetica
     * disfarcada de conveniencia -- quem pedisse 24 s receberia 22,4 s sem
     * perceber na primeira peca com crossfade.
     */
    modo: z.enum(['somaCenas', 'totalFixo']),
    alvoS: z.number().gt(0).optional(),
  }),
  cenas: z.array(zCena).min(1),
  /** exatamente `cenas.length - 1` entradas. `refinar.ts` cobra a contagem. */
  transicoes: z.array(zTransicao),
  legenda: zLegenda.optional(),
  /**
   * OBRIGATORIO. Peca de foto parada nao tem fonte com som, e Reel sem audio perde
   * elegibilidade para nao-seguidor (`05-formatos.md` §3, [oficial]). "Mudo" no
   * catalogo significa SEM LOCUCAO, nunca sem faixa -- e 5 das 12 series entregam
   * Reel a partir de foto parada (1, 2, 5, 10, 11), com a serie 4 sendo
   * explicitamente "sem voz, COM faixa".
   */
  audio: zAudio,
  licencas: zLicencas.default(
    Object.fromEntries([
      ...LICENCAS.map((k) => [k, false]),
      ['justificativa', ''],
    ]) as Record<Licenca, boolean> & {justificativa: string},
  ),
  /**
   * Os recortes de embalagem que a peca usa. `[]` e valido e e o caso comum.
   *
   * SUBSTITUI O `exigePreservacao: boolean` DA VERSAO ANTERIOR. Um booleano dizia
   * "exija preservacao" sem dizer DE QUE, e o portao ficava sem saber qual arquivo
   * conferir. A lista nomeia os arquivos, e o portao de ritmo checa que cada um
   * existe em `projetos/<p>/public/assets/` -- existir ali ja e o certificado, porque
   * a unica porta de entrada e `publicar.py`, que e fail-closed.
   *
   * `exigePreservacao` continua existindo no PLANO, derivado: `assets.length > 0`.
   */
  assets: z.array(zAsset).default([]),
  /** o que prende nos 2 primeiros segundos */
  gancho: z.string().trim().min(1),
  cta: z.string().trim().min(1),
});

/**
 * O briefing, com uma excecao a estrita: chave que comeca com `_` e COMENTARIO.
 *
 * Sem isto, documentar o briefing por dentro seria impossivel, e um briefing sem
 * comentario e um briefing que a proxima sessao le errado -- este repositorio ja
 * pagou isso quatro vezes (o `_LEIA` do `gerar-props.mjs`). Com o prefixo `_`, a
 * chave de comentario nao pode COLIDIR com campo real: nenhum campo do esquema
 * comeca com `_` a nao ser `_esquema`, que e literal.
 */
export const zBriefing = z.preprocess((cru) => {
  if (typeof cru !== 'object' || cru === null || Array.isArray(cru)) return cru;
  const limpo: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(cru as Record<string, unknown>)) {
    if (k.startsWith('_') && k !== '_esquema') continue;
    limpo[k] = v;
  }
  return limpo;
}, zBriefingEstrito) as unknown as typeof zBriefingEstrito;

export type Briefing = z.infer<typeof zBriefingEstrito>;
```

- [ ] **Step 5: rodar o teste e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/esquema.test.ts`
Expected: `Tests 29 passed (29)` — 10 em `zBriefing`, 3 em `zLegenda`, 2 em `zAsset`, 4 em `zFonte`,
8 em `zEventoTexto`, 2 em `zCena`. **Conte os `it(` do bloco que você colou antes de rodar**: se der
outro número, faltou um pedaço, e este `Expected` é o jeito de descobrir.

**`z.strictObject` existe: medido.** `node -e "console.log(require('zod/package.json').version)"` dá
`4.5.4` e `node -e "const {z}=require('zod');console.log(typeof z.strictObject)"` dá `function`. A
versão anterior deste plano gastava um parágrafo de plano B (`z.object().strict()`) para um risco que
custava um comando para medir e não foi medido — e o plano B saiu junto dos **Riscos assumidos**.

- [ ] **Step 6: escrever o `briefing.json` do projeto que já existe**

Criar `instagram/remotion/projetos/01-private-label/briefing.json`. Ele reproduz **a peça de
hoje** — uma cena, o vídeo inteiro, uma manchete — e é o exemplo que o Rafael edita:

```json
{
  "_esquema": "canastra-briefing/1",
  "_leia": "ESTE arquivo e a verdade humana e pode ser editado a mao. `plano.json`, que nasce dele, NAO pode: ele carrega o sha256 deste arquivo e o portao de ritmo reprova plano cujo hash nao bate. Todo tempo aqui esta em SEGUNDOS, contados do inicio DA CENA.",
  "serie": "avulsa",
  "fps": 30,
  "formatos": ["9:16", "1:1"],
  "duracao": {"modo": "somaCenas", "alvoS": 23.2},
  "cenas": [
    {
      "duracaoS": 23.2,
      "fonte": {
        "tipo": "video",
        "arquivo": "pl.mp4",
        "razaoExibicao": 0.5625,
        "aparaAntesS": 1.14,
        "enquadramento": "faixa",
        "camera": "parado"
      },
      "eventos": [
        {
          "papel": "manchete",
          "texto": "SUA PRÓPRIA MARCA DE CAFÉ",
          "entradaS": 2.333,
          "palavraAcento": 2,
          "pista": "tela"
        }
      ]
    }
  ],
  "transicoes": [],
  "legenda": {
    "arquivo": "transcricao.json",
    "relogio": "fonte",
    "ancora": {"tipo": "locucao"}
  },
  "audio": {
    "locucao": {"arquivo": "pl.wav", "ganhoDb": 0, "aparaAntesS": 1.14},
    "trilha": null
  },
  "assets": [],
  "gancho": "pergunta direta sobre lucro, na voz do dono, nos 2 primeiros segundos",
  "cta": "clique aqui embaixo e vem conosco"
}
```

Os números não são novos: `aparaAntesS: 1.14` é o ar morto medido em `02 PL.mp4` (34 frames a
30 fps, `Raiz.tsx:25`); `duracaoS: 23.2` é `24,33 − 1,14` (696 frames, `Raiz.tsx:28`);
`entradaS: 2.333` é o `inicioFrame: 104` do `props.json` menos os 34 frames do corte, dividido
por 30 — `(104 − 34) / 30 = 2,3333 s`; `razaoExibicao: 0.5625` é o `9/16` de exibição do
`pl.mp4`, medido por `sondar()` na Tarefa 4A Step 6, não o `16/9` do container.

**`"enquadramento": "faixa"`, e não `"preencher"` — corrigido em 01/10/2026.** A versão anterior
escrevia `preencher` espelhando o `objectFit: 'cover'` chumbado na `Fonte.tsx` antiga. Nesta peça as
duas palavras são **pixel-idênticas** — `zonas.video` já tem a razão da fonte nos dois formatos
(1080×1920 no Reel, 607,50×1080 no Feed, medido), e `cover` dentro de uma caixa da mesma razão é
`contain` —, mas **o significado deixou de ser cosmético**: desde o conserto de `razaoDaPeca()`,
`preencher` quer dizer *"esta cena corta para encher o quadro"*, logo ela **sai** da conta da razão.
Com `preencher` aqui, `razaoDaPeca` viraria `null`, `layout()` usaria a razão do quadro e o Feed 1:1
passaria a **recortar** o vídeo em vez de o deixar em coluna — o recorte que este motor existe para
não fazer, e a quebra do `IDENTICO` da Tarefa 8, Step 8. Com `faixa`, `razaoDaPeca` = **0,5625**, que
é o que o Step 6 imprime.

**Quatro campos mudaram de forma com a revisão da spec, e cada um por um motivo medido:**

- **`"pista": "tela"` no lugar de `"encaixe": ["cartela"]`.** O encaixe é derivado; `tela` é o único
  caminho para a cartela, e é o que a peça de hoje desenha (`props.json` pede `modo: 'cartela'`).
  Medido: em `tela` a manchete dá 152 px de corpo e **24,245%** de mancha no 9:16 e **43,102%** no
  1:1, contra pisos de 6,861% e 6,925% — domina nos dois. Em `topo`, o 1:1 daria 48 px e **3,793%**,
  e o portão de ritmo reprovaria. Esse é o defeito que a pista faz aparecer em número.
- **`legenda.arquivo` no lugar de `legenda.transcricao`**, e **`ancora` no lugar de `aparaAntesS`**.
  O `1.14` não desapareceu: ele agora mora em `audio.locucao.aparaAntesS`, e a âncora **aponta para
  lá** em vez de repetir o número. Dois campos com o mesmo valor divergem no primeiro conserto.
- **`audio` obrigatório, com a locução que já está no disco.** Medido:
  `projetos/01-private-label/public/fonte/` contém `pl.mp4` **e `pl.wav`** — o wav extraído, que é
  exatamente a locução desta peça. `trilha: null` é aceito porque há locução.
- **`assets: []` no lugar de `exigePreservacao: false`.** Esta peça não tem recorte de embalagem no
  quadro. Os três PNG em `public/assets/` existem para a composição `PonteAssets`, que é instrumento
  de conferência, não peça.

- [ ] **Step 7: provar que o briefing do projeto real passa no esquema**

Acrescentar ao fim de `tests/esquema.test.ts`:

```ts
describe('o briefing do 01-private-label', () => {
  it('passa no esquema, com os numeros medidos em 02 PL.mp4', () => {
    // O briefing e o arquivo que o Rafael edita: se ele nao passar no proprio
    // esquema, o esquema esta errado.
    const bruto = JSON.parse(
      readFileSync('projetos/01-private-label/briefing.json', 'utf8'),
    );
    const b = zBriefing.parse(bruto);
    expect(b.cenas.length).toBe(1);
    expect(b.transicoes.length).toBe(0);
    // 23,2 s = 696 frames a 30 fps, que e DURACAO_FRAMES de Raiz.tsx:28.
    expect(Math.round(b.cenas[0].duracaoS * b.fps)).toBe(696);
    // 1,14 s = 34 frames, que e CORTAR_ANTES_FRAMES de Raiz.tsx:25.
    const fonte = b.cenas[0].fonte;
    expect(fonte.tipo).toBe('video');
    if (fonte.tipo === 'video') expect(Math.round(fonte.aparaAntesS * b.fps)).toBe(34);
    // 2,3333 s = 70 frames = o inicioFrame 104 do props.json menos o corte de 34.
    expect(Math.round(b.cenas[0].eventos[0].entradaS * b.fps)).toBe(70);
    // A manchete pede a CARTELA pela pista, que e o unico caminho para ela.
    expect(b.cenas[0].eventos[0].pista).toBe('tela');
    // A locucao que ja esta no disco: `public/fonte/pl.wav` (medido). E o 1,14 mora
    // AQUI, nao na legenda -- a legenda aponta para ele por `ancora`.
    expect(b.audio.locucao?.arquivo).toBe('pl.wav');
    expect(Math.round((b.audio.locucao?.aparaAntesS ?? 0) * b.fps)).toBe(34);
    expect(b.audio.trilha).toBeNull();
    expect(b.legenda?.ancora).toEqual({tipo: 'locucao'});
    expect(b.assets).toEqual([]);
  });

  it('o campo `_leia` nao derruba o parse, porque comeca com _', () => {
    // Chave de comentario num arquivo estrito: sem esta regra, documentar o
    // briefing por dentro seria impossivel -- e um briefing sem comentario e um
    // briefing que a proxima sessao le errado.
    expect(zBriefing.safeParse({...MINIMO, _qualquer_nota: 'texto livre'}).success).toBe(true);
  });
});
```

E ao topo do arquivo de teste:

```ts
import {readFileSync} from 'node:fs';
```

- [ ] **Step 8: conferir que a exceção do `_` é EXCEÇÃO, e não um furo na estrita**

Nenhuma linha de código neste passo: o embrulho de `z.preprocess` já foi escrito no Step 4, junto do
objeto, exatamente para que nenhum passo mande redigitar um objeto de ~50 campos. (A versão anterior
mostrava `z.strictObject({ // ... o objeto inteiro escrito no Step 4 })` — a **única** elisão de código
do plano, e num objeto desse tamanho a redigitação é onde um campo se perde.)

O que este passo faz é provar que a exceção não abriu a porteira. Acrescentar a `tests/esquema.test.ts`:

```ts
  it('a excecao do `_` NAO deixa passar campo desconhecido sem underscore', () => {
    // O risco do preprocess: se ele removesse chave demais, ou se a estrita ficasse
    // frouxa, `duracao_alvo: 24` voltaria a ser ignorado em silencio.
    expect(zBriefing.safeParse({...MINIMO, duracao_alvo: 24}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, Audio: {}}).success).toBe(false);
  });

  it('a excecao do `_` nao vale para `_esquema`, que e campo de verdade', () => {
    const {_esquema, ...sem} = MINIMO;
    void _esquema;
    expect(zBriefing.safeParse(sem).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, _esquema: 'canastra-briefing/2'}).success).toBe(false);
  });
```

- [ ] **Step 9: rodar o teste inteiro e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/esquema.test.ts`
Expected: `Tests 33 passed (33)` — os 29 do Step 5, mais 2 do Step 7 (o briefing real e o `_leia`) e 2
do Step 8 (a exceção do `_` não é furo).

- [ ] **Step 10: rodar a suíte inteira e o typecheck**

Run: `cd instagram/remotion && npx vitest run && npm run tsc`
Expected: suíte com **BASE + 3 + 12 + 9 + 12 + 2 + 9 + 5 + 33** testes; `npm run tsc` sem saída. Nenhum
render mudou nesta tarefa — ela só acrescenta arquivos e uma dependência declarada, então **não
há conferência no pixel**: não existe pixel novo para conferir.

- [ ] **Step 11: commit**

```bash
git add instagram/remotion/package.json instagram/remotion/src/briefing \
  instagram/remotion/tests/esquema.test.ts \
  instagram/remotion/projetos/01-private-label/briefing.json
git commit -m "$(cat <<'MSG'
Briefing: esquema zod, zod declarado, e o briefing do 01-private-label

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 6: `refinar.ts` — as recusas de sentido que zod não expressa

zod valida forma. Ninguém valida sentido, e é no sentido que este repositório se machuca: lote
que não existe (`F:23.2025`), tempo morto, duas camadas no mesmo lugar, licença ligada sem
motivo. `refinar.ts` é puro, roda **antes do render** e devolve a lista inteira de recusas, não
a primeira — quem escreve briefing quer consertar tudo numa passada.

**Files:**
- Create: `instagram/remotion/src/briefing/refinar.ts`
- Create: `instagram/remotion/tests/refinar.test.ts`

- [ ] **Step 1: escrever o teste que falha**

Criar `instagram/remotion/tests/refinar.test.ts`:

```ts
import {describe, expect, it} from 'vitest';
import {zBriefing, type Briefing} from '../src/briefing/esquema';
import {exigirBriefingCoerente, refinar} from '../src/briefing/refinar';

/** A locucao que o 01-private-label tem no disco, para o audio nao ficar mudo. */
const LOCUCAO = {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 0};

function briefing(patch: Record<string, unknown> = {}): Briefing {
  return zBriefing.parse({
    _esquema: 'canastra-briefing/1',
    serie: 'avulsa',
    formatos: ['9:16'],
    duracao: {modo: 'somaCenas'},
    cenas: [
      {
        duracaoS: 4,
        fonte: {tipo: 'cor', cor: '#3B2A1F'},
        eventos: [
          // `pista` e OBRIGATORIA desde a revisao da spec (nao ha default no esquema),
          // e `topo` e a que `PISTA_PADRAO.manchete` sugere.
          {papel: 'manchete', texto: 'CAFE DA SERRA', entradaS: 0, pista: 'topo'},
        ],
      },
    ],
    transicoes: [],
    audio: {locucao: LOCUCAO, trilha: null},
    gancho: 'gancho de teste',
    cta: 'chama no direct',
    ...patch,
  });
}

const codigos = (b: Briefing) => refinar(b).map((r) => r.codigo);

describe('refinar', () => {
  it('o briefing minimo coerente nao tem recusa', () => {
    expect(refinar(briefing())).toEqual([]);
  });

  it('transicoes tem que ser exatamente cenas.length - 1', () => {
    // Uma transicao sobrando ou faltando sai como video torto com exit 0.
    expect(codigos(briefing({transicoes: [{tipo: 'corte'}]}))).toContain('transicoes-contagem');
  });

  it('cena sem evento E sem legenda e TEMPO MORTO, que proibicoes.md:11-12 proibe', () => {
    const b = briefing({
      cenas: [{duracaoS: 4, fonte: {tipo: 'cor', cor: '#3B2A1F'}, eventos: []}],
    });
    expect(codigos(b)).toContain('tempo-morto');
  });

  it('a licenca aceitaTempoMorto desliga essa recusa -- com justificativa', () => {
    const b = briefing({
      cenas: [{duracaoS: 4, fonte: {tipo: 'cor', cor: '#3B2A1F'}, eventos: []}],
      licencas: {aceitaTempoMorto: true, justificativa: 'respiro antes do CTA, decidido por serie'},
    });
    expect(codigos(b)).not.toContain('tempo-morto');
  });

  it('licenca ligada sem justificativa de 12 caracteres e recusada', () => {
    const b = briefing({licencas: {particulas: true, justificativa: 'porque'}});
    const r = refinar(b).find((x) => x.codigo === 'licenca-sem-justificativa');
    expect(r).toBeDefined();
    // A mensagem tem que NOMEAR a linha de proibicoes.md que a licenca derruba,
    // senao ligar uma virou clicar em "ok".
    expect(r!.mensagem).toMatch(/proibicoes\.md/);
    expect(r!.mensagem).toMatch(/particulas/);
  });

  it('dado com texto de lote, fabricacao ou validade e RECUSADO', () => {
    // Licao 22 do CLAUDE.md: saiu `F:23.2025`, um mes que nao existe, e no Canela
    // saiu `F:12.2025`, plausivel -- e por isso pior. Informacao regulatoria
    // falsa nao entra em peca de e-commerce.
    for (const texto of ['F:23.2025', 'VAL 03/2027', 'LOTE 4471', 'f.12.2025']) {
      const b = briefing({
        cenas: [
          {
            duracaoS: 4,
            fonte: {tipo: 'cor', cor: '#3B2A1F'},
            eventos: [{papel: 'dado', texto, entradaS: 0}],
          },
        ],
      });
      expect(codigos(b), texto).toContain('dado-regulatorio');
    }
  });

  it('dado que e PRECO passa: o filtro pega lote, nao numero', () => {
    const b = briefing({
      cenas: [
        {
          duracaoS: 4,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [{papel: 'dado', texto: 'R$ 39,90', entradaS: 0, pista: 'principal'}],
        },
      ],
    });
    expect(codigos(b)).not.toContain('dado-regulatorio');
  });

  it('dois eventos na mesma pista ao mesmo tempo e erro de briefing', () => {
    const b = briefing({
      cenas: [
        {
          duracaoS: 6,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [
            {papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'topo', duracaoS: 3},
            {papel: 'etiqueta', texto: 'DOIS', entradaS: 1, pista: 'topo', duracaoS: 3},
          ],
        },
      ],
    });
    expect(codigos(b)).toContain('pista-ocupada');
  });

  it('a cartela conflita com topo e principal, e NAO com a legenda', () => {
    const b = briefing({
      cenas: [
        {
          duracaoS: 6,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [
            {papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'tela', duracaoS: 3},
            {papel: 'dado', texto: 'R$ 39,90', entradaS: 1, pista: 'principal', duracaoS: 3},
          ],
        },
      ],
    });
    expect(codigos(b)).toContain('pista-ocupada');
  });

  it('evento que passa do fim da cena e recusado, com os dois numeros', () => {
    const b = briefing({
      cenas: [
        {
          duracaoS: 1.2,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [{papel: 'manchete', texto: 'UMA FRASE DE SEIS PALAVRAS AQUI', entradaS: 0.5, pista: 'topo'}],
        },
      ],
    });
    const r = refinar(b).find((x) => x.codigo === 'evento-estoura-cena');
    expect(r).toBeDefined();
    expect(r!.mensagem).toMatch(/frames/);
  });

  it('transicao maior ou igual a cena vizinha e recusada', () => {
    const b = briefing({
      cenas: [
        {
          duracaoS: 1.5,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [{papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'topo'}],
        },
        {
          duracaoS: 4,
          fonte: {tipo: 'cor', cor: '#4A5D3A'},
          eventos: [{papel: 'manchete', texto: 'DOIS', entradaS: 0, pista: 'topo'}],
        },
      ],
      transicoes: [{tipo: 'fade', duracaoS: 2}],
    });
    expect(codigos(b)).toContain('transicao-maior-que-cena');
  });

  it('branco puro como fonte de cor e recusado por proibicoes.md:13', () => {
    const b = briefing({
      cenas: [
        {
          duracaoS: 4,
          fonte: {tipo: 'cor', cor: '#FFFFFF'},
          eventos: [{papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'topo'}],
        },
      ],
    });
    expect(codigos(b)).toContain('branco-puro');
  });

  it('dois acentos na mesma cena e recusado: um acento por cena', () => {
    const b = briefing({
      cenas: [
        {
          duracaoS: 8,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [
            {papel: 'manchete', texto: 'UM DOIS', entradaS: 0, palavraAcento: 0, duracaoS: 2, pista: 'topo'},
            {papel: 'dado', texto: 'R$ 39,90', entradaS: 4, palavraAcento: 1, duracaoS: 2, pista: 'principal'},
          ],
        },
      ],
    });
    expect(codigos(b)).toContain('dois-acentos');
  });

  it('palavraAcento fora da faixa de palavras e recusado', () => {
    const b = briefing({
      cenas: [
        {
          duracaoS: 4,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [{papel: 'manchete', texto: 'UM DOIS', entradaS: 0, palavraAcento: 7, pista: 'topo'}],
        },
      ],
    });
    expect(codigos(b)).toContain('acento-fora-da-faixa');
  });

  it('arquivo com barra e recusado: o campo e NOME, nao caminho', () => {
    // O prefixo de pasta vive em `Fonte.tsx` por `SUB.fonte`, de proposito: o
    // briefing fala de MEDIDA, nao de arrumacao de pasta.
    const b = briefing({
      cenas: [
        {
          duracaoS: 4,
          fonte: {
            tipo: 'video',
            arquivo: 'fonte/pl.mp4',
            razaoExibicao: 0.5625,
            aparaAntesS: 0,
            enquadramento: 'preencher',
            camera: 'parado',
          },
          eventos: [{papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'topo'}],
        },
      ],
    });
    expect(codigos(b)).toContain('arquivo-com-caminho');
  });

  it('grade com colunas x linhas diferente do numero de celulas e recusada', () => {
    const celula = {tipo: 'cor', cor: '#4A5D3A'};
    const b = briefing({
      cenas: [
        {
          duracaoS: 4,
          fonte: {tipo: 'grade', colunas: 2, linhas: 2, calha: 8, celulas: [celula, celula]},
          eventos: [{papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'topo'}],
        },
      ],
    });
    expect(codigos(b)).toContain('grade-incompleta');
  });

  it('totalFixo sem alvoS e recusado', () => {
    expect(codigos(briefing({duracao: {modo: 'totalFixo'}}))).toContain('totalfixo-sem-alvo');
  });

  it('peca SEM locucao e SEM trilha e recusada, citando o criterio [oficial]', () => {
    // A ausencia A4, agora sobre campos que existem. `05-formatos.md` §3, [oficial]:
    // Reel sem audio perde elegibilidade para nao-seguidor. "Mudo" no catalogo
    // significa SEM LOCUCAO, nunca sem faixa.
    const b = briefing({audio: {locucao: null, trilha: null}});
    const r = refinar(b).find((x) => x.codigo === 'audio-mudo');
    expect(r).toBeDefined();
    expect(r!.mensagem).toMatch(/05-formatos/);
    expect(r!.mensagem).toMatch(/oficial/);
  });

  it('trilha null COM locucao passa, e locucao null COM trilha tambem', () => {
    expect(codigos(briefing())).not.toContain('audio-mudo');
    const t = {
      arquivo: 'ambiente.wav',
      ganhoDb: -18,
      aparaAntesS: 0,
      loopar: true,
      fadeEntradaS: 0.5,
      fadeSaidaS: 0.8,
    };
    expect(codigos(briefing({audio: {locucao: null, trilha: t}}))).not.toContain('audio-mudo');
  });

  it('legenda ancorada na LOCUCAO sem locucao no audio e recusada', () => {
    // A ancora `locucao` le `audio.locucao.aparaAntesS`. Sem locucao ela nao tem de
    // onde ler, e escolher a cena 0 "por conveniencia" seria o default escondido que a
    // spec proibe -- entao recusa, nomeando as duas saidas.
    const b = briefing({
      audio: {
        locucao: null,
        trilha: {
          arquivo: 'ambiente.wav',
          ganhoDb: -18,
          aparaAntesS: 0,
          loopar: true,
          fadeEntradaS: 0,
          fadeSaidaS: 0,
        },
      },
      legenda: {arquivo: 'transcricao.json', relogio: 'fonte', ancora: {tipo: 'locucao'}},
    });
    const r = refinar(b).find((x) => x.codigo === 'legenda-sem-ancora');
    expect(r).toBeDefined();
    expect(r!.mensagem).toMatch(/cena/);
    expect(r!.mensagem).toMatch(/segundo/);
  });

  it('legenda ancorada numa cena que nao existe, ou numa cena sem apara, e recusada', () => {
    const base = {arquivo: 'transcricao.json', relogio: 'fonte' as const};
    // indice fora da faixa
    expect(
      codigos(briefing({legenda: {...base, ancora: {tipo: 'cena', indice: 7}}})),
    ).toContain('legenda-sem-ancora');
    // a cena existe, mas a fonte dela e `cor`: nao ha `aparaAntesS` nenhum para ler
    expect(
      codigos(briefing({legenda: {...base, ancora: {tipo: 'cena', indice: 0}}})),
    ).toContain('legenda-sem-ancora');
  });

  it('registro telaCheia com enquadramento faixa e recusado', () => {
    // §3.3.2: `telaCheia` diz "a foto E o quadro", e `faixa` (contain) deixa fundo
    // chapado em 42,19% da altura numa foto paisagem. As duas coisas nao cabem.
    const b = briefing({
      cenas: [
        {
          duracaoS: 4,
          fonte: {
            tipo: 'foto',
            arquivo: 'cafezal.jpg',
            razaoExibicao: 4 / 3,
            registro: 'telaCheia',
            enquadramento: {tipo: 'faixa'},
            camera: 'pushLento',
          },
          eventos: [{papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'principal'}],
        },
      ],
    });
    expect(codigos(b)).toContain('telacheia-com-faixa');
  });

  it('exigirBriefingCoerente lanca com TODAS as recusas na mensagem, nao a primeira', () => {
    const b = briefing({
      transicoes: [{tipo: 'corte'}],
      cenas: [{duracaoS: 4, fonte: {tipo: 'cor', cor: '#FFFFFF'}, eventos: []}],
    });
    let erro: Error | null = null;
    try {
      exigirBriefingCoerente(b);
    } catch (e) {
      erro = e as Error;
    }
    expect(erro).not.toBeNull();
    expect(erro!.message).toMatch(/transicoes-contagem/);
    expect(erro!.message).toMatch(/branco-puro/);
    expect(erro!.message).toMatch(/tempo-morto/);
  });
});
```

- [ ] **Step 2: rodar o teste e conferir que falha**

Run: `cd instagram/remotion && npx vitest run tests/refinar.test.ts`
Expected: FALHA — `Failed to resolve import "../src/briefing/refinar"`.

- [ ] **Step 3: criar `src/briefing/refinar.ts`**

```ts
// AS RECUSAS DE SENTIDO. Puro: sem React, sem remotion, sem I/O.
//
// zod valida FORMA. Um briefing pode ter forma perfeita e nao fazer sentido: uma
// cena de 1,2 s com uma manchete de seis palavras, duas camadas na mesma pista no
// mesmo frame, um carimbo de lote inventado, uma licenca ligada sem motivo
// escrito. Sentido e aqui.
//
// DEVOLVE A LISTA INTEIRA, NAO A PRIMEIRA
//
// Quem escreve briefing quer consertar tudo numa passada. Recusar a primeira e
// obrigar uma rodada por erro -- e em briefing de 8 cenas isso sao 8 rodadas.
//
// RODA ANTES DO RENDER
//
// Cada recusa aqui e um render que nao acontece. Render de Reel de 23 s leva
// minutos; `refinar()` leva milissegundos. E a licao "erro e evidencia barata" do
// CLAUDE.md aplicada ao motor.

import {cadencia} from '../motor/cadencia';
import {layout} from '../motor/layout';
import {CONFLITO_DE_PISTA, type Pista} from '../motor/pista';
import {duracaoComIrmaos, duracaoDeIrmao} from '../motor/movimento';
import {emFrames} from '../motor/relogio';
import {resolverEncaixe} from '../motor/encaixe';
import {DIMENSAO, LICENCAS, type Briefing, type Cena, type EventoTexto} from './esquema';

export type Recusa = {
  /** slug estavel, para teste e para o portao de ritmo */
  codigo: string;
  /** caminho do campo no briefing, no formato que um humano acha no arquivo */
  campo: string;
  mensagem: string;
};

/**
 * Lote, fabricacao e validade. Licao 22 do CLAUDE.md: o modelo redesenha carimbo
 * variavel como qualquer outro texto, e saiu `F:23.2025` -- um mes que nao existe.
 * No Canela saiu `F:12.2025`, plausivel, e passaria despercebido. Plausivel e pior
 * que absurdo: o absurdo voce ve.
 */
const REGULATORIO = /^\s*F\s*[:.]|\bVAL\b|\bVALIDADE\b|\bLOTE\b|\bFAB\b/i;

/** A linha de `proibicoes.md` que cada licenca derruba, para a mensagem citar. */
const LINHA_DA_LICENCA: Record<string, string> = {
  particulas: 'proibicoes.md:11-12 ("explosao de particula")',
  orbesDeBrilho: 'proibicoes.md:11 ("brilho")',
  varreduraDeLuz: 'proibicoes.md:11 ("brilho")',
  shockwave: 'proibicoes.md:11-12 (particula + brilho)',
  molaComOvershoot: 'proibicoes.md:11 ("easing elastico")',
  revelarCaractereACaractere: 'proibicoes.md:14 ("Revelar texto caractere a caractere")',
  flashNoCorte: 'proibicoes.md:16 ("Flash branco instantaneo")',
  irisWipe: 'proibicoes.md:16 (vizinhanca de "whip pan")',
  motionBlurBurst: 'proibicoes.md:7-8 (nomeia <CameraMotionBlur>)',
  swipeMarcaTexto: 'proibicoes.md:20 (seria o 2o saturado ao lado de COR.acento)',
  highlightPalavraAtiva: 'nao e proibicao: e 1 acento, mas troca 2,45x/s',
  aceitaTempoMorto: 'proibicoes.md:11-12 ("tempo morto")',
};

/** Quantos frames o evento ocupa, no PIOR formato pedido (o mais apertado). */
export function duracaoDoEventoFrames(
  e: EventoTexto,
  b: Briefing,
): {frames: number; irmao: number} {
  const c = cadencia(b.fps);
  if (e.duracaoS !== undefined) {
    const frames = emFrames(e.duracaoS, b.fps);
    return {frames, irmao: frames};
  }

  // Sem `duracaoS` declarado, a duracao e a da FRASE -- e ela depende de quantos
  // irmaos o texto tem, que depende da quebra de linha, que depende do formato.
  // Pega-se o MAIOR entre os formatos pedidos, para o evento caber em todos.
  let maior = 0;
  let maiorIrmao = 0;
  for (const formato of b.formatos) {
    const {largura, altura} = DIMENSAO[formato];
    const z = layout({largura, altura, razaoFonte: razaoDaPeca(b) ?? largura / altura});
    const r = resolverEncaixe({
      texto: e.texto,
      papel: e.papel,
      pista: e.pista,
      zonas: z,
      cadencia: c,
      palavraAcento: e.palavraAcento,
    });
    // `forma.irmaos` E A UNICA CONTAGEM DO SISTEMA. Ela sai de `CADENCIA_DO_PAPEL`
    // dentro de `formaTextoTela` (Tarefa 3, Step 5), que e o MESMO lugar de onde sai
    // o `atrasoFrames` de cada palavra e o `duracaoCena` de `TextoTela`. Antes de
    // 01/10/2026 este arquivo tinha um `contarIrmaos()` proprio, lendo a mesma tabela
    // -- e duas implementacoes da mesma regra divergem no primeiro conserto. Esta e
    // literalmente a razao pela qual o plano contava 36 frames para a etiqueta e a
    // tela desenhava 42.
    const irmaos = r.forma.irmaos;
    const irmao = duracaoDeIrmao(irmaos, c);
    const total = duracaoComIrmaos(irmaos, irmao, c);
    if (total > maior) {
      maior = total;
      maiorIrmao = irmao;
    }
  }
  return {frames: maior, irmao: maiorIrmao};
}

/**
 * A razao de exibicao que a PECA usa em `layout()`.
 *
 * E a MENOR entre as cenas que entram por CONTAIN (`enquadramento` = `faixa`),
 * porque sao elas, e so elas, que obrigam o quadro a abrir uma faixa de terra ao
 * lado da imagem. A caixa de legenda e a coluna de texto sao dimensionadas por essa
 * razao: com a menor delas, a legenda cabe sobre o video de todas as cenas em
 * contain. `null` quando NENHUMA cena entra por contain -- e ai quem chama usa a
 * razao do proprio quadro, e a imagem ocupa o quadro inteiro.
 *
 * O ENQUADRAMENTO NAO PODE SER IGNORADO AQUI, e a versao anterior desta funcao o
 * ignorava: ela fazia `razoes.push(f.razaoExibicao)` para todo `video` e toda
 * `foto`. Consequencia medida: numa peca cuja unica cena e uma foto 4:3 com
 * `registro: "telaCheia"` + `enquadramento: {tipo:"recorte"}`, a funcao devolvia
 * 1,3333, `layout()` punha o video como faixa de 1080x810 no 9:16 e a cena
 * `telaCheia` preenchia 810 de 1920 px de altura -- 57,81% do quadro em terra
 * chapado, com o nome de "tela cheia". `recorte` (foto) e `preencher` (video) sao
 * exatamente a declaracao de que aquela cena CORTA para encher o quadro: a razao de
 * exibicao dela deixa de restringir o quadro, e quem manda e a razao do quadro.
 *
 * `cor` e `grade` continuam fora da conta pelo mesmo motivo: nao tem razao de
 * arquivo a honrar.
 */
export function razaoDaPeca(b: Briefing): number | null {
  const razoes: number[] = [];
  for (const cena of b.cenas) {
    const f = cena.fonte;
    // `faixa` e a UNICA palavra que significa contain nos dois tipos -- string no
    // video, objeto discriminado na foto (spec §2.3).
    if (f.tipo === 'video' && f.enquadramento === 'faixa') razoes.push(f.razaoExibicao);
    if (f.tipo === 'foto' && f.enquadramento.tipo === 'faixa') razoes.push(f.razaoExibicao);
  }
  return razoes.length === 0 ? null : Math.min(...razoes);
}

// `pistaDoEvento()` NAO EXISTE MAIS: `e.pista` e obrigatoria no esquema, e uma funcao
// que aplicasse `PISTA_PADRAO` aqui seria o default escondido de novo -- agora dentro
// do refinador, onde ninguem procuraria por ele.

export function refinar(b: Briefing): Recusa[] {
  const r: Recusa[] = [];

  if (b.transicoes.length !== b.cenas.length - 1) {
    r.push({
      codigo: 'transicoes-contagem',
      campo: 'transicoes',
      mensagem:
        `sao ${b.cenas.length} cenas, logo ${b.cenas.length - 1} transicoes, e o ` +
        `briefing tem ${b.transicoes.length}. Uma sobrando ou faltando sai como ` +
        'video torto com exit 0. Use {"tipo": "corte"} onde nao houver transicao: ' +
        'corte e 0 frames.',
    });
  }

  if (b.duracao.modo === 'totalFixo' && b.duracao.alvoS === undefined) {
    r.push({
      codigo: 'totalfixo-sem-alvo',
      campo: 'duracao.alvoS',
      mensagem:
        'duracao.modo e "totalFixo" e nao ha alvoS. Em totalFixo o alvo MANDA e as ' +
        'cenas sao ajustadas; sem alvo nao ha o que mandar.',
    });
  }

  // AUDIO. A regra escrita sobre campos que existem (§3.6).
  if (b.audio.locucao === null && b.audio.trilha === null) {
    r.push({
      codigo: 'audio-mudo',
      campo: 'audio',
      mensagem:
        'audio.locucao e audio.trilha sao os dois null: a peca sai MUDA. ' +
        '`05-formatos.md` §3, [oficial]: Reel sem audio perde elegibilidade para ' +
        'nao-seguidor. "Mudo" no catalogo significa SEM LOCUCAO, nunca sem faixa -- e ' +
        '5 das 12 series entregam Reel a partir de foto parada, que nao tem som ' +
        'nenhum. Declare uma trilha, ou uma locucao, ou as duas.',
    });
  }

  // A ANCORA DA LEGENDA TEM QUE SER RESOLVIVEL (§2.2.1).
  if (b.legenda) {
    const a = b.legenda.ancora;
    const saidas =
      'As tres saidas: ancore na locucao (e declare audio.locucao), aponte uma cena ' +
      'com {"tipo":"cena","indice":N} cuja fonte tenha aparaAntesS, ou declare o ' +
      'valor cru com {"tipo":"segundo","valorS":X}.';

    if (a.tipo === 'locucao' && b.audio.locucao === null) {
      r.push({
        codigo: 'legenda-sem-ancora',
        campo: 'legenda.ancora',
        mensagem:
          'a legenda esta ancorada na locucao e audio.locucao e null: nao ha de onde ' +
          `ler o instante que cai no frame 0 da peca. ${saidas} O compilador NAO ` +
          'escolhe a cena 0 por conveniencia -- default escondido e o que este ' +
          'desenho proibe em toda parte.',
      });
    }

    if (a.tipo === 'cena') {
      const cena = b.cenas[a.indice];
      if (!cena) {
        r.push({
          codigo: 'legenda-sem-ancora',
          campo: 'legenda.ancora.indice',
          mensagem:
            `a ancora aponta a cena ${a.indice} e o briefing tem ${b.cenas.length} ` +
            `cena(s), indices 0..${b.cenas.length - 1}. ${saidas}`,
        });
      } else if (cena.fonte.tipo !== 'video' && cena.fonte.tipo !== 'foto') {
        r.push({
          codigo: 'legenda-sem-ancora',
          campo: 'legenda.ancora.indice',
          mensagem:
            `a ancora aponta a cena ${a.indice}, cuja fonte e "${cena.fonte.tipo}" e ` +
            `nao tem aparaAntesS para ler. ${saidas}`,
        });
      } else if (cena.fonte.tipo === 'foto') {
        r.push({
          codigo: 'legenda-sem-ancora',
          campo: 'legenda.ancora.indice',
          mensagem:
            `a ancora aponta a cena ${a.indice}, que e FOTO: foto nao tem tempo, logo ` +
            `nao tem apara. ${saidas}`,
        });
      }
    }
  }

  for (const chave of LICENCAS) {
    if (!b.licencas[chave]) continue;
    if (b.licencas.justificativa.trim().length < 12) {
      r.push({
        codigo: 'licenca-sem-justificativa',
        campo: `licencas.${chave}`,
        mensagem:
          `a licenca "${chave}" esta ligada e derruba ${LINHA_DA_LICENCA[chave]}. ` +
          'Ligar uma exige justificativa de 12 caracteres ou mais em ' +
          'licencas.justificativa -- decisao sem motivo escrito nao sobrevive a ' +
          'proxima sessao. E nenhuma tecnica de licenca esta implementada nesta ' +
          'versao: o campo registra a decisao, o codigo vem depois dela.',
      });
    }
  }

  b.cenas.forEach((cena, i) => {
    refinarCena(cena, i, b, r);
  });

  b.transicoes.forEach((t, i) => {
    if (t.tipo === 'corte') return;
    const frames = emFrames(t.duracaoS, b.fps);
    const vizinhas = [
      emFrames(b.cenas[i]?.duracaoS ?? 0, b.fps),
      emFrames(b.cenas[i + 1]?.duracaoS ?? 0, b.fps),
    ];
    const menor = Math.min(...vizinhas);
    if (frames >= menor) {
      r.push({
        codigo: 'transicao-maior-que-cena',
        campo: `transicoes[${i}].duracaoS`,
        mensagem:
          `a transicao pede ${frames} frames e a cena vizinha mais curta tem ` +
          `${menor}. Durante a transicao as DUAS cenas sao renderizadas, entao uma ` +
          'transicao maior que a cena consome a cena inteira e a proxima comeca ' +
          'antes da anterior aparecer.',
      });
    }
  });

  return r;
}

function refinarCena(cena: Cena, i: number, b: Briefing, r: Recusa[]): void {
  const f = cena.fonte;

  if (f.tipo === 'cor' && f.cor.toUpperCase() === '#FFFFFF') {
    r.push({
      codigo: 'branco-puro',
      campo: `cenas[${i}].fonte.cor`,
      mensagem:
        'branco puro e o padrao do modelo generativo sem direcao, e ' +
        'proibicoes.md:13 o nomeia. O fundo da marca e COR.terra (#3B2A1F).',
    });
  }

  if ((f.tipo === 'video' || f.tipo === 'foto') && /[\\/]/.test(f.arquivo)) {
    r.push({
      codigo: 'arquivo-com-caminho',
      campo: `cenas[${i}].fonte.arquivo`,
      mensagem:
        `"${f.arquivo}" tem separador de pasta. Este campo e o NOME do arquivo ` +
        'dentro de public/fonte/; o prefixo vive em Fonte.tsx por SUB.fonte, para ' +
        'que mudar a convencao de pasta nao obrigue a reescrever cada briefing.',
    });
  }

  if (f.tipo === 'foto' && f.registro === 'telaCheia' && f.enquadramento.tipo === 'faixa') {
    r.push({
      codigo: 'telacheia-com-faixa',
      campo: `cenas[${i}].fonte.enquadramento`,
      mensagem:
        '`registro: "telaCheia"` diz que a foto E o quadro, e ' +
        '`enquadramento: {"tipo":"faixa"}` e `contain`: ele deixa fundo chapado em ' +
        '42,19% da altura numa foto paisagem num 9:16 (medido). As duas declaracoes ' +
        'nao cabem juntas. Ou declare `{"tipo":"recorte", ...}` em fracao da fonte, ou ' +
        'troque o registro para "moldura" ou "cartao", que existem justamente para a ' +
        'foto NAO preencher o quadro.',
    });
  }

  if (f.tipo === 'grade' && f.colunas * f.linhas !== f.celulas.length) {
    r.push({
      codigo: 'grade-incompleta',
      campo: `cenas[${i}].fonte.celulas`,
      mensagem:
        `grade de ${f.colunas}x${f.linhas} pede ${f.colunas * f.linhas} celulas e ` +
        `recebeu ${f.celulas.length}. Celula faltando deixa buraco de terra que ` +
        'parece bug de render.',
    });
  }

  if (cena.eventos.length === 0 && !b.legenda && !b.licencas.aceitaTempoMorto) {
    r.push({
      codigo: 'tempo-morto',
      campo: `cenas[${i}].eventos`,
      mensagem:
        'cena sem nenhum evento e sem legenda na peca: sao ' +
        `${emFrames(cena.duracaoS, b.fps)} frames sem camada alguma, que e o ` +
        '"tempo morto" de proibicoes.md:11-12. Ligue licencas.aceitaTempoMorto com ' +
        'justificativa se for de proposito.',
    });
  }

  const comAcento = cena.eventos.filter((e) => e.palavraAcento !== undefined);
  if (comAcento.length > 1) {
    r.push({
      codigo: 'dois-acentos',
      campo: `cenas[${i}].eventos`,
      mensagem:
        `${comAcento.length} eventos desta cena declaram palavraAcento. ` +
        'proibicoes.md:20 pede UM acento de cor por cena, com funcao.',
    });
  }

  const duracaoCenaFrames = emFrames(cena.duracaoS, b.fps);
  const ocupacao: Array<{pista: Pista; de: number; ate: number; texto: string}> = [];

  cena.eventos.forEach((e, j) => {
    const palavras = e.texto.split(/\s+/).filter((p) => p.length > 0);
    if (e.palavraAcento !== undefined && e.palavraAcento >= palavras.length) {
      r.push({
        codigo: 'acento-fora-da-faixa',
        campo: `cenas[${i}].eventos[${j}].palavraAcento`,
        mensagem:
          `palavraAcento ${e.palavraAcento} e o texto tem ${palavras.length} ` +
          'palavras. Indice fora da faixa nao acentua nada e passa sem erro, que e ' +
          'pior que falhar: a peca sai sem o acento que alguem pediu.',
      });
    }

    if (e.papel === 'dado' && REGULATORIO.test(e.texto)) {
      r.push({
        codigo: 'dado-regulatorio',
        campo: `cenas[${i}].eventos[${j}].texto`,
        mensagem:
          `"${e.texto}" parece lote, fabricacao ou validade. Licao 22 do ` +
          'CLAUDE.md: carimbo variavel e regenerado e nunca confiavel -- saiu ' +
          '`F:23.2025`, um mes que nao existe, e `F:12.2025`, plausivel e por isso ' +
          'pior. Em peca de e-commerce isso e informacao regulatoria falsa: ou sai ' +
          'do enquadramento, ou entra por composicao da foto real.',
      });
    }

    // `encaixe-repetido` NAO EXISTE MAIS: o campo `encaixe` saiu do briefing (spec
    // §3.4.2), e uma recusa sobre um campo inexistente e codigo morto com aparencia de
    // protecao.

    const {frames} = duracaoDoEventoFrames(e, b);
    const de = emFrames(e.entradaS, b.fps);
    const ate = de + frames;
    if (ate > duracaoCenaFrames) {
      r.push({
        codigo: 'evento-estoura-cena',
        campo: `cenas[${i}].eventos[${j}]`,
        mensagem:
          `o evento entra no frame ${de} da cena e ocupa ${frames} frames, ` +
          `terminando em ${ate}; a cena tem ${duracaoCenaFrames}. O stagger empurra ` +
          'o fim junto com o comeco (ver duracaoDeIrmao), entao a ultima palavra ' +
          'perderia a saida e sumiria por corte. Alongue a cena ou declare ' +
          'duracaoS no evento.',
      });
    }

    ocupacao.push({pista: e.pista, de, ate, texto: e.texto});
  });

  for (let a = 0; a < ocupacao.length; a++) {
    for (let bb = a + 1; bb < ocupacao.length; bb++) {
      const x = ocupacao[a];
      const y = ocupacao[bb];
      const seCruzam = x.de < y.ate && y.de < x.ate;
      const conflitam =
        CONFLITO_DE_PISTA[x.pista].includes(y.pista) ||
        CONFLITO_DE_PISTA[y.pista].includes(x.pista);
      if (seCruzam && conflitam) {
        r.push({
          codigo: 'pista-ocupada',
          campo: `cenas[${i}].eventos`,
          mensagem:
            `"${x.texto}" (pista ${x.pista}, frames ${x.de}..${x.ate}) e ` +
            `"${y.texto}" (pista ${y.pista}, frames ${y.de}..${y.ate}) ocupam ` +
            'pistas que conflitam ao mesmo tempo. Medido no motor antigo: a caixa ' +
            'da manchete se intersectava com a da legenda em 90,20 px no eixo x no 1:1 sem ' +
            'ninguem reclamar. A pista existe para isso ser erro, nao desenho.',
        });
      }
    }
  }
}

/** Lanca com TODAS as recusas, uma por linha. */
export function exigirBriefingCoerente(b: Briefing): void {
  const recusas = refinar(b);
  if (recusas.length === 0) return;
  throw new Error(
    `o briefing tem ${recusas.length} recusa(s) de sentido:\n` +
      recusas.map((x) => `  [${x.codigo}] ${x.campo}: ${x.mensagem}`).join('\n'),
  );
}
```

- [ ] **Step 4: rodar o teste e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/refinar.test.ts`
Expected: `Tests 23 passed (23)`.

Se `evento-estoura-cena` não disparar no teste da cena de 1,2 s, imprima o número:
`duracaoDoEventoFrames` sobre `'UMA FRASE DE SEIS PALAVRAS AQUI'` a 30 fps tem 6 palavras, então
`duracaoDeIrmao(6)` = 36 + 5×3 = 51 e o total é 51 + 15 = 66 frames, contra os 36 frames da cena
— **não ajuste o teste**, confira a conta.

- [ ] **Step 5: provar que o briefing real passa pelo refinador**

Acrescentar ao fim de `tests/refinar.test.ts`:

```ts
describe('o briefing do 01-private-label passa no refinador', () => {
  it('nenhuma recusa', () => {
    const bruto = JSON.parse(
      readFileSync('projetos/01-private-label/briefing.json', 'utf8'),
    );
    expect(refinar(zBriefing.parse(bruto))).toEqual([]);
  });
});
```

E ao topo: `import {readFileSync} from 'node:fs';`

Run: `cd instagram/remotion && npx vitest run tests/refinar.test.ts`
Expected: `Tests 24 passed (24)`. Se a recusa `evento-estoura-cena` aparecer para o briefing
real, leia os dois números da mensagem: a manchete tem 5 palavras, logo
`duracaoDeIrmao(5)` = 36 + 12 = 48 e o total é 48 + 12 = 60 frames; ela entra no frame 70 e a
cena tem 696 — cabe. Se não couber, a cadência não está vindo de `cadencia(30)`.

- [ ] **Step 6: rodar a suíte inteira e o typecheck**

Run: `cd instagram/remotion && npx vitest run && npm run tsc`
Expected: suíte com **BASE + 3 + 12 + 9 + 12 + 2 + 9 + 5 + 33 + 24** testes; `npm run tsc` sem saída.
Nenhum pixel mudou: `refinar.ts` não é importado por nenhum `.tsx` — **sem conferência no
pixel**, porque não há pixel novo.

- [ ] **Step 7: commit**

```bash
git add instagram/remotion/src/briefing/refinar.ts instagram/remotion/tests/refinar.test.ts
git commit -m "$(cat <<'MSG'
Briefing: refinador de sentido, com a lista inteira de recusas por rodada

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 7: `compilar.ts` — briefing → plano, e toda a aritmética de tempo num lugar

O compilador é **puro** e é onde os três relógios se encontram: segundos do briefing → frames da
peça, e os blocos de legenda saem do tempo da **fonte** para o tempo da **peça**.

A regra de C5, que a spec resolveu: `duracaoPecaFrames = Σ cenas − Σ transições`. Durante a
transição as duas cenas são renderizadas, então ela **não soma tempo: ela gasta**. Com a
transição default sendo `corte` de 0 frames, `Σ cenas` continua sendo a duração — e é por isso
que os dois desenhos paralelos estavam certos ao mesmo tempo.

**Files:**
- Create: `instagram/remotion/src/briefing/compilar.ts`
- Create: `instagram/remotion/src/briefing/impressao.ts` (o sha256 canonico e `selarPlano`)
- Create: `instagram/remotion/tests/compilar.test.ts`
- Create: `instagram/remotion/tests/impressao.test.ts`
- Create: `instagram/remotion/scripts/compilar.mjs`
- Modify: `instagram/remotion/src/legenda/agrupar.ts` (`maxPalavras` passa a ser parametro)

- [ ] **Step 1: escrever o teste que falha**

Criar `instagram/remotion/tests/compilar.test.ts`:

```ts
import {readFileSync} from 'node:fs';
import {describe, expect, it} from 'vitest';
import {compilar} from '../src/briefing/compilar';
import {selarPlano, sha256Do} from '../src/briefing/impressao';
import {zBriefing, type Briefing} from '../src/briefing/esquema';

function briefing(patch: Record<string, unknown> = {}): Briefing {
  return zBriefing.parse({
    _esquema: 'canastra-briefing/1',
    serie: 'avulsa',
    formatos: ['9:16'],
    duracao: {modo: 'somaCenas'},
    cenas: [
      {
        duracaoS: 4,
        fonte: {tipo: 'cor', cor: '#3B2A1F'},
        eventos: [{papel: 'manchete', texto: 'UM DOIS', entradaS: 0, pista: 'topo'}],
      },
      {
        duracaoS: 6,
        fonte: {tipo: 'cor', cor: '#4A5D3A'},
        eventos: [{papel: 'manchete', texto: 'TRES', entradaS: 0, pista: 'topo'}],
      },
    ],
    transicoes: [{tipo: 'corte'}],
    // `audio` e OBRIGATORIO. A locucao e a do 01-private-label, que existe no disco.
    audio: {locucao: {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 0}, trilha: null},
    gancho: 'g',
    cta: 'c',
    ...patch,
  });
}

describe('compilar', () => {
  it('com transicoes de corte, a duracao da peca e a SOMA das cenas', () => {
    // 4 s + 6 s = 10 s = 300 frames a 30 fps. Corte e 0 frames, entao nao
    // subtrai nada -- e por isso o exemplo de 600 frames do desenho de contrato e
    // a subtracao do desenho de cena estao os dois certos.
    const p = compilar(briefing());
    expect(p.duracaoFrames).toBe(300);
    expect(p.cenas.map((c) => c.duracaoFrames)).toEqual([120, 180]);
    expect(p.cenas.map((c) => c.inicioNaPecaFrames)).toEqual([0, 120]);
  });

  it('a transicao GASTA frames: 1 s de fade tira 30 frames da peca', () => {
    const p = compilar(briefing({transicoes: [{tipo: 'fade', duracaoS: 1}]}));
    expect(p.duracaoFrames).toBe(270);
    // A cena 2 comeca 30 frames antes, porque durante o fade as duas correm.
    expect(p.cenas[1].inicioNaPecaFrames).toBe(90);
    expect(p.transicoes[0]).toEqual({tipo: 'fade', duracaoFrames: 30});
  });

  it('somaCenas com alvoS divergente LANCA, com os dois numeros e a diferenca', () => {
    // Nao e console.warn: uma peca que sai mais curta que o briefing e o defeito
    // que o pedido do Rafael nomeia.
    let erro: Error | null = null;
    try {
      compilar(briefing({duracao: {modo: 'somaCenas', alvoS: 12}, transicoes: [{tipo: 'fade', duracaoS: 1}]}));
    } catch (e) {
      erro = e as Error;
    }
    expect(erro).not.toBeNull();
    expect(erro!.message).toMatch(/270/);
    expect(erro!.message).toMatch(/360/);
    expect(erro!.message).toMatch(/90 frames/);
  });

  it('somaCenas com alvoS que bate nao lanca', () => {
    expect(compilar(briefing({duracao: {modo: 'somaCenas', alvoS: 10}})).duracaoFrames).toBe(300);
  });

  it('totalFixo DEVOLVE os frames da transicao as cenas, proporcionalmente', () => {
    // 4 s e 6 s com 1 s de fade dariam 270 frames. Pedindo 300, faltam 30 frames:
    // distribuidos na proporcao 120:180, dao 12 e 18.
    const p = compilar(
      briefing({
        duracao: {modo: 'totalFixo', alvoS: 10},
        transicoes: [{tipo: 'fade', duracaoS: 1}],
      }),
    );
    expect(p.duracaoFrames).toBe(300);
    expect(p.cenas.map((c) => c.duracaoFrames)).toEqual([132, 198]);
  });

  it('totalFixo joga o resto inteiro na cena MAIS LONGA, deterministicamente', () => {
    // 1 s e 1 s com 1 s de fade dao 30 frames; pedindo 31 falta 1 frame, que nao
    // divide por dois. O resto vai para a cena mais longa; empate vai para a de
    // indice menor. Determinismo importa porque o portao 3 compara sha256 de
    // dois renders.
    const p = compilar(
      briefing({
        cenas: [
          {duracaoS: 1, fonte: {tipo: 'cor', cor: '#3B2A1F'}, eventos: []},
          {duracaoS: 2, fonte: {tipo: 'cor', cor: '#4A5D3A'}, eventos: []},
        ],
        transicoes: [{tipo: 'fade', duracaoS: 0.5}],
        duracao: {modo: 'totalFixo', alvoS: 3.1},
        licencas: {aceitaTempoMorto: true, justificativa: 'cena de cor pura para o teste de resto'},
      }),
    );
    expect(p.duracaoFrames).toBe(93);
    const soma = p.cenas.reduce((s, c) => s + c.duracaoFrames, 0);
    expect(soma - 15).toBe(93);
    // duas compilacoes do MESMO briefing dao o MESMO plano
    const q = compilar(
      briefing({
        cenas: [
          {duracaoS: 1, fonte: {tipo: 'cor', cor: '#3B2A1F'}, eventos: []},
          {duracaoS: 2, fonte: {tipo: 'cor', cor: '#4A5D3A'}, eventos: []},
        ],
        transicoes: [{tipo: 'fade', duracaoS: 0.5}],
        duracao: {modo: 'totalFixo', alvoS: 3.1},
        licencas: {aceitaTempoMorto: true, justificativa: 'cena de cor pura para o teste de resto'},
      }),
    );
    expect(q.cenas.map((c) => c.duracaoFrames)).toEqual(p.cenas.map((c) => c.duracaoFrames));
  });

  it('o evento sai com inicio relativo a CENA e duracao calculada', () => {
    const p = compilar(briefing());
    const e = p.cenas[0].eventos[0];
    expect(e.inicioFrames).toBe(0);
    // 'UM DOIS' tem 2 palavras: duracaoDeIrmao(2) = 36 + 3 = 39, e o total com
    // stagger e 39 + 3 = 42.
    expect(e.duracaoIrmaoFrames).toBe(39);
    expect(e.duracaoFrames).toBe(42);
    expect(e.familia).toBe('manchete');
    expect(e.pista).toBe('topo');
  });

  it('compilar NAO carrega hash: selar e passo separado, e compilar.ts e puro', () => {
    // `sha256Do` precisa de `node:crypto`, que e Node-only. Se ele morasse em
    // `compilar.ts`, o arquivo deixaria de ser puro e a PRIMEIRA importacao de VALOR
    // a partir de um `.tsx` derrubaria o render -- hoje `Raiz.tsx`, `Peca.tsx` e
    // `Cena.tsx` sobrevivem por acidente, porque importam so `import type`, que o
    // transpilador apaga. Entao o hash e de `briefing/impressao.ts` e entra por
    // `selarPlano`.
    const p = compilar(briefing());
    expect(p._sha256Briefing).toBe('');
    expect(p._gerado_por).toMatch(/compilar/);
  });
});

describe('sha256Do -- a serializacao canonica', () => {
  it('O HASH VE O QUE ESTA ANINHADO. Era aqui que a protecao era um no-op', () => {
    // O DEFEITO MEDIDO: `JSON.stringify(valor, Object.keys(valor).sort())` -- o
    // segundo argumento do JSON.stringify e uma ALLOWLIST APLICADA RECURSIVAMENTE a
    // todo objeto da estrutura. Passando so as chaves de topo, TUDO que esta aninhado
    // e descartado: o serializado saia
    //   {"_esquema":"x","cenas":[{}],"cta":"c","duracao":{},"fps":30,...}
    // e dois briefings com `cenas[0].duracaoS` 23,2 contra 99 e textos completamente
    // diferentes davam O MESMO HASH (3dc6692d6a05fb71 nos dois, medido).
    //
    // Como o `_sha256Briefing` e a UNICA protecao nomeada no Risco assumido nº 3, a
    // protecao central do desenho era um no-op -- e o teste que existia so variava
    // `cta`, chave de TOPO, entao passava e dava falsa confianca.
    const a = briefing();
    const b = briefing({
      cenas: [
        {
          duracaoS: 99,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [{papel: 'manchete', texto: 'TEXTO TOTALMENTE OUTRO', entradaS: 0, pista: 'topo'}],
        },
        {
          duracaoS: 6,
          fonte: {tipo: 'cor', cor: '#4A5D3A'},
          eventos: [{papel: 'manchete', texto: 'TRES', entradaS: 0, pista: 'topo'}],
        },
      ],
    });
    expect(sha256Do(a)).not.toBe(sha256Do(b));
  });

  it('e ESTAVEL: a ordem das chaves no objeto nao muda o hash', () => {
    // Determinismo importa porque o portao compara hashes entre execucoes, e a ordem
    // de insercao de `Object.keys` muda com a ordem de escrita do JSON.
    const um = {a: 1, b: {c: 2, d: [3, {e: 4}]}};
    const outro = {b: {d: [3, {e: 4}], c: 2}, a: 1};
    expect(sha256Do(um)).toBe(sha256Do(outro));
  });

  it('distingue o que JSON.stringify cru confundiria', () => {
    // Tres pares que um serializador descuidado achata:
    expect(sha256Do({a: undefined})).not.toBe(sha256Do({}));
    expect(sha256Do([1, 2])).not.toBe(sha256Do({0: 1, 1: 2}));
    expect(sha256Do({a: null})).not.toBe(sha256Do({a: 0}));
  });

  it('muda com QUALQUER campo, em QUALQUER profundidade', () => {
    const base = briefing();
    const iguais = sha256Do(briefing());
    expect(iguais).toBe(sha256Do(base)); // o mesmo briefing da o mesmo hash
    // topo
    expect(sha256Do(briefing({cta: 'outro cta'}))).not.toBe(iguais);
    // profundidade 3: cenas[0].eventos[0].texto
    const fundo = briefing();
    fundo.cenas[0].eventos[0].texto = 'OUTRO';
    expect(sha256Do(fundo)).not.toBe(iguais);
    // profundidade 3: audio.locucao.aparaAntesS
    const audio = briefing();
    audio.audio.locucao!.aparaAntesS = 1.14;
    expect(sha256Do(audio)).not.toBe(iguais);
  });
});

describe('selarPlano', () => {
  it('sela o plano com o hash do briefing que o gerou', () => {
    const b = briefing();
    const p = selarPlano(compilar(b), b);
    expect(p._sha256Briefing).toMatch(/^[0-9a-f]{64}$/);
    expect(p._sha256Briefing).toBe(sha256Do(b));
  });
});

describe('compilar, continuacao', () => {

  // O FIXTURE. Dois construtores de cena parametrizados pelo par
  // (tipo, enquadramento), porque e esse par -- e nao o tipo sozinho -- que
  // `razaoDaPeca()` tem de olhar.
  const cenaVideo = (enquadramento: 'faixa' | 'preencher', razao: number) => ({
    duracaoS: 4,
    fonte: {
      tipo: 'video' as const,
      arquivo: 'pl.mp4',
      razaoExibicao: razao,
      aparaAntesS: 0,
      enquadramento,
      camera: 'parado' as const,
    },
    eventos: [{papel: 'manchete' as const, texto: 'UM', entradaS: 0, pista: 'topo' as const}],
  });
  const cenaFoto = (
    registro: 'moldura' | 'cartao' | 'telaCheia',
    enquadramento: {tipo: 'faixa'} | {tipo: 'recorte'; x: number; y: number; largura: number; altura: number},
    razao: number,
  ) => ({
    duracaoS: 6,
    fonte: {
      tipo: 'foto' as const,
      arquivo: 'cafezal.jpg',
      razaoExibicao: razao,
      registro,
      enquadramento,
      camera: 'pushLento' as const,
    },
    eventos: [{papel: 'manchete' as const, texto: 'DOIS', entradaS: 0, pista: 'topo' as const}],
  });
  const RECORTE = {tipo: 'recorte' as const, x: 0.289, y: 0, largura: 0.422, altura: 1};

  it('a razao da peca e a MENOR das cenas que entram por CONTAIN (faixa)', () => {
    const p = compilar(
      briefing({
        cenas: [
          cenaVideo('faixa', 0.5625),
          cenaFoto('cartao', {tipo: 'faixa'}, 4032 / 3024),
        ],
      }),
    );
    // Com a MENOR razao, a caixa de legenda cabe sobre o video de todas as cenas em
    // contain.
    expect(p.razaoDaPeca).toBeCloseTo(0.5625, 9);
  });

  it('cena que PREENCHE o quadro nao entra na conta -- e era aqui que o teste antigo passava errado', () => {
    // O TESTE QUE DEVERIA TER PEGO O DEFEITO, E QUE EM VEZ DISSO O FIXAVA.
    //
    // A versao anterior deste arquivo tinha `cena 0 = video 'preencher' 0,5625` e
    // `cena 1 = foto telaCheia + faixa 1,3333`, e esperava **0,5625** -- que e o
    // valor da funcao ERRADA. Com o enquadramento olhado, a cena 0 sai da conta e o
    // resultado certo e 1,3333: o teste nao "passava por sorte", ele ASSERTAVA o
    // defeito. (E o fixture era invalido de outra forma: `telaCheia` + `faixa` e
    // recusado por `refinar()` com `telacheia-com-faixa`, logo `compilar` lancaria.)
    //
    // Aqui a cena que preenche tem a razao MENOR de proposito: se ela entrasse na
    // conta o resultado seria 0,5625 em vez de 1,3333. O teste so passa se o
    // enquadramento for olhado.
    const p = compilar(
      briefing({
        cenas: [
          cenaVideo('preencher', 0.5625),
          cenaFoto('cartao', {tipo: 'faixa'}, 4032 / 3024),
        ],
      }),
    );
    expect(p.razaoDaPeca).toBeCloseTo(4032 / 3024, 9);
  });

  it('peca inteira em telaCheia/recorte da razao NULA, e e isso que deixa a foto encher o quadro', () => {
    // `registro: "telaCheia"` + `recorte` diz "a foto E o quadro". Se a razao do
    // arquivo (1,3333) voltasse daqui, `layout()` poria o video como faixa de
    // 1080x810 no 9:16 e a "tela cheia" preencheria 810 de 1920 px -- 57,81% do
    // quadro em terra chapado. Com `null`, quem chama usa `width / height` e a
    // imagem ocupa o quadro inteiro.
    // `transicoes: []` porque e UMA cena: `exigirBriefingCoerente` lanca
    // `transicoes-contagem` com o default de uma transicao do helper.
    const p = compilar(
      briefing({cenas: [cenaFoto('telaCheia', RECORTE, 4032 / 3024)], transicoes: []}),
    );
    expect(p.razaoDaPeca).toBeNull();
  });

  it('a razao e null quando nenhuma cena tem arquivo: as duas do helper sao cor chapada', () => {
    const p = compilar(
      briefing({
        licencas: {aceitaTempoMorto: true, justificativa: 'cenas de cor pura no teste de razao'},
      }),
    );
    expect(p.razaoDaPeca).toBeNull();
  });

  it('a legenda e REBASEADA pela FORMULA da ancora, e nenhum bloco desaparece calado', () => {
    // A FORMULA (spec §2.2.1):
    //   desloc = emFrames(entradaNaPecaS ?? 0, fps) - emFrames(ancoraS, fps)
    // com `ancora: {tipo:'locucao'}` -> ancoraS = audio.locucao.aparaAntesS = 1,14 s
    // = 34 frames, e entradaNaPecaS = 0, logo desloc = -34.
    const PALAVRAS = [
      {texto: 'antes', inicioMs: 0, fimMs: 500},
      {texto: 'do', inicioMs: 500, fimMs: 900},
      {texto: 'corte', inicioMs: 1400, fimMs: 1800},
      {texto: 'depois', inicioMs: 1800, fimMs: 2400},
    ];
    const p = compilar(
      briefing({
        audio: {locucao: {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 1.14}, trilha: null},
        legenda: {arquivo: 'transcricao.json', relogio: 'fonte', ancora: {tipo: 'locucao'}},
      }),
      {palavras: PALAVRAS},
    );
    expect(p.legenda).not.toBeNull();
    expect(p.legenda!.deslocamentoFrames).toBe(-34);
    // nenhum bloco comeca antes do frame 0 da peca
    for (const x of p.legenda!.blocos) expect(x.inicioFrame).toBeGreaterThanOrEqual(0);

    // E O BLOCO QUE FOI GRUDADO EM 0 E CONTADO, com o maior recuo.
    //
    // O caso ja vivido: o Whisper pos a primeira palavra dentro do ar morto, e hoje o
    // `blocos.find()` de `Legenda.tsx:35` simplesmente NAO ACHA nada -- a palavra
    // desaparece em silencio. Grudar em 0 e o comportamento certo; nao contar e o
    // defeito.
    expect(p.legenda!.grudadosEmZero).toBeGreaterThan(0);
    expect(p.legenda!.maiorRecuoFrames).toBeGreaterThan(0);
  });

  it('a ancora `cena` le a apara DAQUELA cena, nomeada pelo indice', () => {
    const p = compilar(
      briefing({
        cenas: [
          {
            duracaoS: 4,
            fonte: {
              tipo: 'video',
              arquivo: 'pl.mp4',
              razaoExibicao: 0.5625,
              aparaAntesS: 2,
              enquadramento: 'preencher',
              camera: 'parado',
            },
            eventos: [{papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'topo'}],
          },
          {
            duracaoS: 6,
            fonte: {tipo: 'cor', cor: '#4A5D3A'},
            eventos: [{papel: 'manchete', texto: 'TRES', entradaS: 0, pista: 'topo'}],
          },
        ],
        legenda: {
          arquivo: 'transcricao.json',
          relogio: 'fonte',
          ancora: {tipo: 'cena', indice: 0},
        },
      }),
      {palavras: [{texto: 'um', inicioMs: 3000, fimMs: 3400}]},
    );
    // 2 s = 60 frames a 30 fps
    expect(p.legenda!.deslocamentoFrames).toBe(-60);
  });

  it('`entradaNaPecaS` ATRASA a pista de legenda, e entra na mesma formula', () => {
    const p = compilar(
      briefing({
        audio: {locucao: {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 1}, trilha: null},
        legenda: {
          arquivo: 'transcricao.json',
          relogio: 'fonte',
          ancora: {tipo: 'locucao'},
          entradaNaPecaS: 2,
        },
      }),
      {palavras: [{texto: 'um', inicioMs: 0, fimMs: 400}]},
    );
    // desloc = emFrames(2) - emFrames(1) = 60 - 30 = +30
    expect(p.legenda!.deslocamentoFrames).toBe(30);
    expect(p.legenda!.blocos[0].inicioFrame).toBe(30);
  });

  it('bloco DEPOIS do fim da peca e descartado, e contado', () => {
    // O numero no diagnostico e o que denuncia uma peca encurtada por `totalFixo` que
    // comeu a fala.
    const p = compilar(
      briefing({
        legenda: {arquivo: 'transcricao.json', relogio: 'fonte', ancora: {tipo: 'segundo', valorS: 0}},
      }),
      {
        palavras: [
          {texto: 'dentro', inicioMs: 0, fimMs: 400},
          // a peca tem 300 frames = 10 s; 20 s esta fora
          {texto: 'fora', inicioMs: 20000, fimMs: 20400},
        ],
      },
    );
    expect(p.legenda!.descartadosDepoisDoFim).toBe(1);
    expect(p.legenda!.blocos.every((x) => x.inicioFrame < p.duracaoFrames)).toBe(true);
  });

  it('sem legenda declarada, plano.legenda e null e nao um objeto vazio', () => {
    // Objeto vazio parece legenda configurada e sai peca muda sem ninguem
    // entender. `null` e visivelmente ausente.
    expect(compilar(briefing()).legenda).toBeNull();
  });

  it('compilar RECUSA briefing incoerente: refinar roda primeiro', () => {
    let erro: Error | null = null;
    try {
      compilar(briefing({transicoes: []}));
    } catch (e) {
      erro = e as Error;
    }
    expect(erro).not.toBeNull();
    expect(erro!.message).toMatch(/transicoes-contagem/);
  });

  it('o diagnostico diz qual encaixe foi DERIVADO, por formato, com a mancha', () => {
    const p = compilar(briefing({formatos: ['9:16', '1:1']}));
    const d = p.diagnostico.eventos[0];
    // No 9:16 a sobra e 0,00 px -> faixa. No 1:1 com fonte de COR a razao da peca e
    // null, entao `layout()` usa a razao do proprio quadro e o video preenche a
    // largura -> faixa tambem. A derivacao nao tem plano B: ela e o formato.
    expect(d.porFormato['9:16'].encaixe).toBe('faixa');
    expect(typeof d.porFormato['1:1'].corpo).toBe('number');
    expect(typeof d.porFormato['1:1'].dominancia).toBe('number');
    expect(typeof d.porFormato['1:1'].piso).toBe('number');
    expect(typeof d.porFormato['1:1'].domina).toBe('boolean');
    // e o `porque` carrega os DOIS numeros, para o portao nao ter que recalcular
    expect(d.porFormato['1:1'].porque).toMatch(/%/);
  });

  it('exigePreservacao e DERIVADO de assets, nao um booleano a parte', () => {
    expect(compilar(briefing()).exigePreservacao).toBe(false);
    const com = briefing({
      assets: [{arquivo: 'suave-250g.png', tipo: 'recorte-embalagem', laudoExigido: true}],
    });
    const p = compilar(com);
    expect(p.exigePreservacao).toBe(true);
    expect(p.assets.map((a) => a.arquivo)).toEqual(['suave-250g.png']);
  });

  it('o plano carrega `audio` inteiro, com os dois campos', () => {
    const p = compilar(briefing());
    expect(p.audio.locucao?.arquivo).toBe('pl.wav');
    expect(p.audio.trilha).toBeNull();
  });
});

describe('o briefing do 01-private-label compila para a peca de hoje', () => {
  it('696 frames, uma cena, manchete no frame 70', () => {
    const bruto = JSON.parse(
      readFileSync('projetos/01-private-label/briefing.json', 'utf8'),
    );
    // Medido nesta sessao: `transcricao.json` E um array de
    // {texto, inicioMs, fimMs} com 75 palavras -- exatamente o tipo `Palavra` que
    // `src/legenda/agrupar.ts:3` declara.
    const palavras = JSON.parse(
      readFileSync('projetos/01-private-label/transcricao.json', 'utf8'),
    );
    expect(Array.isArray(palavras)).toBe(true);
    expect(palavras.length).toBe(75);

    const p = compilar(zBriefing.parse(bruto), {palavras});
    // DURACAO_FRAMES de Raiz.tsx:28 era 696. O motor novo tem que dar o mesmo.
    expect(p.duracaoFrames).toBe(696);
    expect(p.cenas.length).toBe(1);
    expect(p.cenas[0].eventos[0].inicioFrames).toBe(70);

    // 75 palavras / 2 por bloco = 38 blocos no tempo da FONTE, que e o que o
    // props.json de hoje tem. O deslocamento e -34 (a ancora aponta para
    // `audio.locucao.aparaAntesS` = 1,14 s), e o PRIMEIRO bloco termina no frame 20 da
    // fonte -- logo em -14 na peca.
    expect(p.legenda!.deslocamentoFrames).toBe(-34);

    // AS DUAS REGRAS DE BORDA, e cada uma fecha um modo de falha (spec §2.2.1):
    //
    //   fim <= 0 ............ DESCARTADO e contado. "Você está" ia de 0 a 20 na fonte,
    //                         logo -34..-14 na peca: nenhum frame visivel. Grudar em 0
    //                         um bloco sem duracao nao e conservar nada.
    //   inicio < 0 < fim .... GRUDADO em 0 e contado, com o recuo. "procurando algo"
    //                         ia de 20 a 49, logo -14..15: ele APARECE. Hoje o
    //                         `blocos.find()` de `Legenda.tsx:35` nao acha nada e a
    //                         palavra desaparece EM SILENCIO -- e esse silencio e o
    //                         defeito, nao o recorte.
    expect(p.legenda!.blocos.length).toBe(37);
    expect(p.legenda!.descartadosAntesDoInicio).toBe(1);
    expect(p.legenda!.blocos[0].texto).toBe('procurando algo');
    expect(p.legenda!.blocos[0].inicioFrame).toBe(0);
    expect(p.legenda!.blocos[0].fimFrame).toBe(15);
    expect(p.legenda!.grudadosEmZero).toBe(1);
    expect(p.legenda!.maiorRecuoFrames).toBe(14);
    // o ultimo bloco termina em 684, 12 frames antes do fim da peca
    expect(p.legenda!.blocos.at(-1)!.fimFrame).toBe(684);
    expect(p.legenda!.descartadosDepoisDoFim).toBe(0);
  });
});
```

- [ ] **Step 2: rodar o teste e conferir que falha**

Run: `cd instagram/remotion && npx vitest run tests/compilar.test.ts`
Expected: FALHA — `Failed to resolve import "../src/briefing/compilar"`.

- [ ] **Step 2b: criar `src/briefing/impressao.ts` — a serialização canônica**

**Este arquivo existe por duas razões, e as duas são defeitos consertados.**

**A primeira: o hash era um no-op.** A versão anterior tinha, dentro de `compilar.ts`:

```ts
export function sha256Do(valor: unknown): string {
  return createHash('sha256')
    .update(JSON.stringify(valor, Object.keys(valor as object).sort()))
    .digest('hex');
}
```

O segundo argumento de `JSON.stringify` **não é uma ordem de chaves: é uma allowlist, aplicada
recursivamente a todo objeto da estrutura.** Passando só as chaves de topo, tudo que está aninhado é
descartado. O serializado sai assim:

```
{"_esquema":"x","cenas":[{}],"cta":"c","duracao":{},"fps":30,"gancho":"g","serie":"avulsa","transicoes":[]}
```

Dois briefings idênticos exceto `cenas[0].duracaoS` (23,2 contra 99) e `cenas[0].eventos[0].texto`
(`'UM'` contra `'TEXTO TOTALMENTE OUTRO'`) produzem **o mesmo hash** — `3dc6692d6a05fb71`, rodado. E o
`_sha256Briefing` é a **única proteção nomeada no Risco assumido nº 3**.

**A segunda: `compilar.ts` é declarado puro pela spec §2.4** e `import {createHash} from 'node:crypto'`
o torna Node-only. Hoje sobrevive por acidente: `Raiz.tsx`, `Peca.tsx` e `Cena.tsx` o importam apenas
com `import type`, que o transpilador apaga. **A primeira importação de VALOR a partir de um `.tsx`
derruba o render** — e nada no plano anterior dizia isso, nem no cabeçalho do arquivo nem nos riscos.

```ts
// A IMPRESSAO DIGITAL DO BRIEFING. Node-only: importa `node:crypto`.
//
// POR QUE ESTE ARQUIVO EXISTE E NAO E `compilar.ts`
//
// A spec §2.4 declara `compilar.ts` PURO, e `node:crypto` o tornaria Node-only. Hoje
// `Raiz.tsx`, `Peca.tsx` e `Cena.tsx` importam `compilar.ts` apenas com `import type`,
// que o transpilador apaga -- entao o bundle do Chrome nunca ve o `require`. A
// primeira importacao de VALOR a partir de um `.tsx` derrubaria o render, e ninguem
// lembraria por que. Separando, o compilador continua podendo entrar no bundle e este
// arquivo nunca entra: quem o importa e `scripts/compilar.mjs` e `verificacao/ritmo.ts`,
// os dois de Node.

import {createHash} from 'node:crypto';

/**
 * Serializacao CANONICA: mesma estrutura -> mesma string, em qualquer ordem de chave.
 *
 * POR QUE NAO `JSON.stringify(valor, Object.keys(valor).sort())`
 *
 * Porque o segundo argumento do `JSON.stringify` NAO e uma ordem de chaves: e uma
 * ALLOWLIST, e ela e aplicada RECURSIVAMENTE a todo objeto da estrutura. Com as chaves
 * de topo apenas, `cenas` sai como `[{}]` e `duracao` como `{}` -- o hash ignora cenas,
 * eventos, fontes, duracoes e transicoes. Medido: dois briefings com duracoes e textos
 * completamente diferentes davam o MESMO hash.
 *
 * O que esta funcao garante, e cada item fecha um jeito de dois valores diferentes
 * virarem a mesma string:
 *
 *   - chaves ordenadas em TODA profundidade, nao so no topo;
 *   - array e objeto tem delimitadores diferentes, entao `[1,2]` nao colide com
 *     `{0:1,1:2}`;
 *   - `undefined` e representado, em vez de a chave desaparecer;
 *   - `null` nao vira `0`;
 *   - numero passa por `Number.prototype.toString`, que e o mesmo do JSON.
 */
export function canonico(valor: unknown): string {
  if (valor === undefined) return 'u';
  if (valor === null) return 'z';
  if (typeof valor === 'number') {
    if (!Number.isFinite(valor)) {
      throw new Error(`canonico: numero nao finito (${valor}) nao tem forma estavel`);
    }
    return `n:${valor}`;
  }
  if (typeof valor === 'boolean') return valor ? 'b:1' : 'b:0';
  if (typeof valor === 'string') return `s:${valor.length}:${valor}`;
  if (Array.isArray(valor)) {
    return `a[${valor.map(canonico).join(',')}]`;
  }
  if (typeof valor === 'object') {
    const chaves = Object.keys(valor as object).sort();
    const partes = chaves.map(
      (k) => `${k.length}:${k}=${canonico((valor as Record<string, unknown>)[k])}`,
    );
    return `o{${partes.join(',')}}`;
  }
  throw new Error(
    `canonico: nao sei serializar ${typeof valor}. Briefing e plano sao JSON: se ` +
      'apareceu function, symbol ou bigint aqui, alguem passou um objeto vivo em vez ' +
      'de dado lido de arquivo.',
  );
}

/** O sha256 da forma canonica. Mesma estrutura -> mesmo hash, sempre. */
export function sha256Do(valor: unknown): string {
  return createHash('sha256').update(canonico(valor), 'utf8').digest('hex');
}

/**
 * Sela o plano com o hash do briefing que o gerou.
 *
 * SEPARADO DE `compilar()` de proposito: `compilar()` e puro e devolve
 * `_sha256Briefing: ''`. Quem sela e quem escreve o arquivo (`scripts/compilar.mjs`),
 * porque selar e um ato de ESCRITA -- e um plano em memoria, dentro de um teste, nao
 * precisa de selo.
 */
export function selarPlano<T extends {_sha256Briefing: string}>(plano: T, briefing: unknown): T {
  return {...plano, _sha256Briefing: sha256Do(briefing)};
}
```

E um teste próprio, `instagram/remotion/tests/impressao.test.ts`, com os quatro `it` do
`describe('sha256Do')` e o `describe('selarPlano')` que o Step 1 escreveu — mova-os para lá em vez de
deixá-los em `compilar.test.ts`: o arquivo de teste segue o módulo.

- [ ] **Step 2c: medir de onde a fala começa, antes de acreditar na transcrição**

O rebase da legenda depende da âncora, e a âncora do `01-private-label` é `{tipo: 'locucao'}` — ou
seja `audio.locucao.aparaAntesS` = 1,14 s = 34 frames. **A transcrição discorda dela**, e antes de
escolher um lado é preciso medir qual está errado.

Run:
```
cd instagram/remotion
node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -hide_banner \
  -i projetos/01-private-label/public/fonte/pl.wav \
  -af silencedetect=noise=-40dB:d=0.2 -f null - 2>&1 | grep -i "silence\|Duration" | head -4
```

Medido em 01/10/2026, e este número decide a questão:

```
Duration: 00:00:24.33
silence_start: 0
silence_end: 1.135 | silence_duration: 1.135
```

**A fala começa em 1,135 s.** A 30 fps isso é 34,05 frames, que confirma o `cortarAntesFrames: 34` de
`Raiz.tsx:25` — medido de forma independente, por um caminho diferente. Logo a âncora em 1,14 s está
**certa**, e a transcrição está **errada na cabeça**: o Whisper pôs o primeiro bloco em 0..667 ms e o
segundo em 667..1633 ms, os dois **dentro do silêncio medido**.

Consequências, e nenhuma delas é ajuste de número para o teste passar:

1. `descartadosAntesDoInicio: 1` e `grudadosEmZero: 1` com `maiorRecuoFrames: 14` são a leitura
   **correta** de uma transcrição com a cabeça errada.
2. **A palavra "Você está" nunca apareceu nesta peça, e ninguém sabia.** Com o motor antigo,
   `Legenda.tsx:34` somava 34 ao frame corrente e o `blocos.find()` do frame 0 caía no bloco
   `20..49` — o primeiro bloco era inalcançável. O motor novo **conta** isso em vez de engolir.
3. O portão de ritmo (Tarefa 10) reprova recuo acima de `LEGENDA.duracaoMinFrames` = **10 frames**, e
   aqui são 14. **Então o `01-private-label` reprova**, e a reprovação é verdadeira.

**Este plano NÃO conserta a transcrição, e a razão é de escopo, não de preguiça.** A resolução é de
**dado**: ou o Whisper roda outra vez sobre o `.wav` com o parâmetro que não ancora a primeira palavra
em 0, ou as duas primeiras palavras recebem à mão o início medido (1,135 s). Nenhuma das duas é código
deste plano, e as duas mexem num arquivo de origem que é **prova** — o mesmo `transcricao.json` que
`tests/manchete-props.test.ts` usa para provar que a manchete é citação literal da fala. Reescrever
prova no meio de uma migração de motor é como se perde a prova.

O que este plano faz é o que o Rafael precisa para decidir: **medir, contar e reprovar em voz alta.**

- a medição está acima, e é reprodutível num comando;
- os contadores `grudadosEmZero`, `maiorRecuoFrames`, `descartadosAntesDoInicio` e
  `descartadosDepoisDoFim` saem no diagnóstico do compilador (Step 3) e na saída do CLI (Step 6);
- o portão de ritmo reprova, e **é essa reprovação que a Tarefa 10 usa como prova de que o portão
  dispara** — em vez de um caso inventado.

E o que **não** serve, para não ser tentado depois: `entradaNaPecaS` e `ancora: {tipo:'segundo'}`
deslocariam a legenda **inteira**, e o resto dela está no lugar — a cabeça errada não se conserta
movendo o corpo.

- [ ] **Step 3: criar `src/briefing/compilar.ts`**

```ts
// BRIEFING -> PLANO. Puro: sem React, sem remotion, sem I/O.
//
// E aqui, e so aqui, que segundo vira frame. O briefing tem UM relogio (segundos
// do inicio da cena); o plano tem os TRES, e por isso ele e GERADO e carrega o
// sha256 do briefing que o produziu -- um plano editado a mao e detectavel.
//
// A CONTA DE C5: `duracaoPecaFrames = Sigma cenas - Sigma transicoes`
//
// Durante a transicao as DUAS cenas sao renderizadas, entao ela nao soma tempo:
// ela GASTA. Com a transicao default sendo `corte` de 0 frames, `Sigma cenas`
// continua sendo a duracao da peca.
//
// POR QUE ELE LANCA EM VEZ DE AVISAR
//
// Com `alvoS` divergente, uma peca que sai mais curta que o briefing e exatamente
// o defeito que o pedido nomeia. `console.warn` num pipeline de render e uma linha
// que ninguem le -- e a licao 3 do CLAUDE.md: exit 0 com o resultado errado.

// NAO HA `import {createHash} from 'node:crypto'` AQUI, e isso e o ponto.
//
// A spec §2.4 declara este arquivo PURO. O hash mora em `briefing/impressao.ts`, que e
// Node-only, e quem sela o plano e quem o escreve. Hoje `Raiz.tsx`, `Peca.tsx` e
// `Cena.tsx` importam este arquivo so com `import type`, que o transpilador apaga --
// mas a primeira importacao de VALOR a partir de um `.tsx` derrubaria o render se
// `node:crypto` estivesse aqui, e ninguem lembraria por que.
import {cadencia} from '../motor/cadencia';
import {agrupar, type Bloco, type Palavra} from '../legenda/agrupar';
import {CADENCIA_DO_PAPEL, FAMILIA_DO_PAPEL} from '../motor/evento';
import {resolverEncaixe} from '../motor/encaixe';
import {layout} from '../motor/layout';
import type {Encaixe, Pista} from '../motor/pista';
import {duracaoComIrmaos, duracaoDeIrmao} from '../motor/movimento';
import {emFrames, emSegundos} from '../motor/relogio';
import {LEGENDA} from '../identidade/tokens';
import type {Papel} from '../identidade/tipografia';
import {
  DIMENSAO,
  type Asset,
  type Audio,
  type Briefing,
  type Fonte,
  type Formato,
  type Licenca,
} from './esquema';
import {exigirBriefingCoerente, razaoDaPeca} from './refinar';

export type EventoCompilado = {
  papel: 'manchete' | 'dado' | 'etiqueta';
  texto: string;
  familia: Papel;
  cadenciaTexto: 'palavra' | 'linha' | 'bloco';
  pista: Pista;
  /**
   * Quantos elementos escalonam, pela cadencia do papel.
   *
   * E o MESMO numero que `formaTextoTela` devolve em `forma.irmaos`, e e ele que
   * dimensiona `duracaoIrmaoFrames` e `duracaoFrames`. Guardado aqui para o portao
   * poder conferir a conta sem remedir a tipografia.
   */
  irmaos: number;
  /** frames, relativo ao inicio DA CENA */
  inicioFrames: number;
  /** frames que CADA irmao fica presente */
  duracaoIrmaoFrames: number;
  /** frames que o evento inteiro ocupa, stagger incluido */
  duracaoFrames: number;
  palavraAcento?: number;
};

export type CenaCompilada = {
  duracaoFrames: number;
  /** frame da PECA em que esta cena comeca, com as transicoes ja descontadas */
  inicioNaPecaFrames: number;
  fonte: Fonte;
  /** frames de apara, ja convertidos (video) */
  aparaAntesFrames: number;
  eventos: EventoCompilado[];
};

export type TransicaoCompilada =
  | {tipo: 'corte'; duracaoFrames: 0}
  | {tipo: 'fade'; duracaoFrames: number}
  | {tipo: 'wipe'; duracaoFrames: number; direcao: string};

export type DiagnosticoEvento = {
  cena: number;
  indice: number;
  texto: string;
  porFormato: Record<
    string,
    {
      /** DERIVADO de (pista, formato). Nao ha escolha para relatar. */
      encaixe: Encaixe;
      corpo: number;
      /** area do bloco ÷ area do quadro */
      dominancia: number;
      piso: number;
      domina: boolean;
      /** `false` para `etiqueta` */
      candidataADominar: boolean;
      /** a frase com os dois numeros, pronta para o portao e para o CLI */
      porque: string;
    }
  >;
};

/** Os contadores do rebase da legenda. Nenhum bloco desaparece sem numero. */
export type DiagnosticoLegenda = {
  deslocamentoFrames: number;
  /** blocos que atravessavam o frame 0 e foram grudados nele */
  grudadosEmZero: number;
  /** o maior recuo, em frames. Acima de LEGENDA.duracaoMinFrames o portao reprova */
  maiorRecuoFrames: number;
  /** blocos inteiramente antes do frame 0: sem frame visivel */
  descartadosAntesDoInicio: number;
  /** blocos que comecavam depois do fim da peca */
  descartadosDepoisDoFim: number;
};

export type Plano = {
  _gerado_por: string;
  _sha256Briefing: string;
  serie: string;
  fps: number;
  formatos: Formato[];
  duracaoFrames: number;
  /** a menor razao de exibicao entre as cenas visuais, ou null */
  razaoDaPeca: number | null;
  cenas: CenaCompilada[];
  transicoes: TransicaoCompilada[];
  legenda: ({blocos: Bloco[]} & DiagnosticoLegenda) | null;
  /** as duas faixas, no relogio da PECA. `audio` e obrigatorio no briefing. */
  audio: Audio;
  assets: Asset[];
  licencas: Record<Licenca, boolean> & {justificativa: string};
  /** DERIVADO: `assets.length > 0`. Nao e campo de briefing. */
  exigePreservacao: boolean;
  gancho: string;
  cta: string;
  diagnostico: {eventos: DiagnosticoEvento[]; licencasLigadas: Licenca[]};
};

export function compilar(
  b: Briefing,
  fontes: {palavras?: Palavra[]} = {},
): Plano {
  // O refinador roda PRIMEIRO. Compilar um briefing incoerente produz um plano
  // coerente com um briefing errado, que e a pior das saidas: parece pronto.
  exigirBriefingCoerente(b);

  const fps = b.fps;
  const c = cadencia(fps);
  const razao = razaoDaPeca(b);

  const transicoes: TransicaoCompilada[] = b.transicoes.map((t) =>
    t.tipo === 'corte'
      ? {tipo: 'corte', duracaoFrames: 0}
      : t.tipo === 'fade'
        ? {tipo: 'fade', duracaoFrames: emFrames(t.duracaoS, fps)}
        : {tipo: 'wipe', duracaoFrames: emFrames(t.duracaoS, fps), direcao: t.direcao},
  );
  const gastoDeTransicao = transicoes.reduce((s, t) => s + t.duracaoFrames, 0);

  let cenasFrames = b.cenas.map((cena) => emFrames(cena.duracaoS, fps));
  let duracaoFrames = cenasFrames.reduce((s, x) => s + x, 0) - gastoDeTransicao;

  if (b.duracao.modo === 'totalFixo') {
    const alvo = emFrames(b.duracao.alvoS as number, fps);
    cenasFrames = devolverFramesAsCenas(cenasFrames, alvo - duracaoFrames);
    duracaoFrames = cenasFrames.reduce((s, x) => s + x, 0) - gastoDeTransicao;
  } else if (b.duracao.alvoS !== undefined) {
    const alvo = emFrames(b.duracao.alvoS, fps);
    if (duracaoFrames !== alvo) {
      const diff = alvo - duracaoFrames;
      throw new Error(
        `duracao.modo e "somaCenas" e o alvo nao bate: as cenas somam ` +
          `${cenasFrames.reduce((s, x) => s + x, 0)} frames, as transicoes gastam ` +
          `${gastoDeTransicao}, logo a peca tem ${duracaoFrames} frames ` +
          `(${emSegundos(duracaoFrames, fps).toFixed(3)} s), e alvoS pede ${alvo} ` +
          `frames (${b.duracao.alvoS} s). Diferenca de ${Math.abs(diff)} frames, ` +
          `${Math.abs(emSegundos(diff, fps)).toFixed(3)} s. Ajuste as cenas, ou use ` +
          'duracao.modo "totalFixo" para o alvo mandar.',
      );
    }
  }

  const diagnosticoEventos: DiagnosticoEvento[] = [];
  let acumulado = 0;
  const cenas: CenaCompilada[] = b.cenas.map((cena, i) => {
    const inicioNaPecaFrames = acumulado;
    acumulado += cenasFrames[i] - (transicoes[i]?.duracaoFrames ?? 0);

    const eventos: EventoCompilado[] = cena.eventos.map((e, j) => {
      const porFormato: DiagnosticoEvento['porFormato'] = {};
      let maiorTotal = 0;
      let irmaoDoMaior = 0;
      let irmaosDoMaior = 1;

      for (const formato of b.formatos) {
        const {largura, altura} = DIMENSAO[formato];
        const z = layout({largura, altura, razaoFonte: razao ?? largura / altura});
        // `pista` vem do briefing e o ENCAIXE e derivado dela mais o formato. Nao ha
        // lista de preferencia e nao ha promocao a cartela: `resolverEncaixe` mede e
        // relata, e quem reprova e o portao de ritmo.
        const r = resolverEncaixe({
          texto: e.texto,
          papel: e.papel,
          pista: e.pista,
          zonas: z,
          cadencia: c,
          palavraAcento: e.palavraAcento,
        });
        porFormato[formato] = {
          encaixe: r.encaixe,
          corpo: r.corpo,
          dominancia: r.dominancia,
          piso: r.piso,
          domina: r.domina,
          candidataADominar: r.candidataADominar,
          porque: r.porque,
        };

        // `r.forma.irmaos` E A UNICA CONTAGEM. Ela sai de `CADENCIA_DO_PAPEL` dentro de
        // `formaTextoTela`, que e o mesmo lugar de onde sai o `atrasoFrames` de cada
        // palavra e o `duracaoCena` de `TextoTela`. Antes de 01/10/2026 o compilador
        // contava por cadencia e a tela contava palavras: a etiqueta de 3 palavras
        // recebia 36 frames e desenhava 42.
        const irmaos = r.forma.irmaos;
        const irmao =
          e.duracaoS !== undefined ? emFrames(e.duracaoS, fps) : duracaoDeIrmao(irmaos, c);
        const total =
          e.duracaoS !== undefined ? irmao : duracaoComIrmaos(irmaos, irmao, c);
        if (total > maiorTotal) {
          maiorTotal = total;
          irmaoDoMaior = irmao;
          irmaosDoMaior = irmaos;
        }
      }

      diagnosticoEventos.push({cena: i, indice: j, texto: e.texto, porFormato});

      return {
        papel: e.papel,
        texto: e.texto,
        familia: FAMILIA_DO_PAPEL[e.papel],
        cadenciaTexto: CADENCIA_DO_PAPEL[e.papel],
        pista: e.pista,
        irmaos: irmaosDoMaior,
        inicioFrames: emFrames(e.entradaS, fps),
        duracaoIrmaoFrames: irmaoDoMaior,
        duracaoFrames: maiorTotal,
        ...(e.palavraAcento !== undefined ? {palavraAcento: e.palavraAcento} : {}),
      };
    });

    return {
      duracaoFrames: cenasFrames[i],
      inicioNaPecaFrames,
      fonte: cena.fonte,
      aparaAntesFrames:
        cena.fonte.tipo === 'video' ? emFrames(cena.fonte.aparaAntesS, fps) : 0,
      eventos,
    };
  });

  return {
    _gerado_por: 'src/briefing/compilar.ts',
    // VAZIO de proposito: quem sela e `selarPlano` de `briefing/impressao.ts`, chamado
    // por quem ESCREVE o arquivo. `compilar()` e puro e nao importa `node:crypto`.
    _sha256Briefing: '',
    serie: b.serie,
    fps,
    formatos: b.formatos,
    duracaoFrames,
    razaoDaPeca: razao,
    cenas,
    transicoes,
    legenda: compilarLegenda(b, fontes.palavras, duracaoFrames),
    audio: b.audio,
    assets: b.assets,
    licencas: b.licencas,
    // DERIVADO, nao declarado: um booleano a parte podia dizer `false` com tres
    // recortes na lista, e o portao nao teria como saber qual dos dois acreditar.
    exigePreservacao: b.assets.length > 0,
    gancho: b.gancho,
    cta: b.cta,
    diagnostico: {
      eventos: diagnosticoEventos,
      licencasLigadas: (Object.keys(b.licencas) as Array<keyof typeof b.licencas>).filter(
        (k) => k !== 'justificativa' && b.licencas[k] === true,
      ) as Licenca[],
    },
  };
}

/**
 * A legenda sai do tempo da FONTE para o tempo da PECA, uma vez, aqui.
 *
 * Antes de 01/10/2026 `Legenda.tsx` somava `deslocamentoFrames` ao frame corrente
 * e procurava o bloco -- o caminho oposto, que funcionava porque havia UMA cena.
 * Com N cenas a legenda fica FORA da `TransitionSeries`, no relogio da peca, e
 * entao o rebase tem que estar nos DADOS: e o compilador que o faz, e a fiacao passa
 * `deslocamentoFrames={0}` -- que `Legenda.tsx:14` ja preve por escrito.
 *
 * A FORMULA, e por que ela nao soma `aparaAntesS` de cena (spec §2.2.1)
 *
 * Com N cenas ha N valores de `Cena.fonte.aparaAntesS` e UMA legenda: somar "o"
 * aparaAntesS deixa de ser definido. A resolucao e NEGAR a pergunta -- a legenda nao e
 * imagem, e a FALA, e a fala tem uma fonte de audio so na peca. Entao:
 *
 *   ancoraS  = conforme `legenda.ancora`
 *   desloc   = emFrames(entradaNaPecaS ?? 0, fps) - emFrames(ancoraS, fps)
 *   bloco.inicioNaPeca = bloco.inicioFonteFrames + desloc
 *
 * `ancora: {tipo:'cena', indice}` e o UNICO jeito de um aparaAntesS de cena tocar a
 * legenda, e ele e NOMINAL: quem escreve aponta a cena com o dedo.
 */
function compilarLegenda(
  b: Briefing,
  palavras: Palavra[] | undefined,
  duracaoPecaFrames: number,
): ({blocos: Bloco[]} & DiagnosticoLegenda) | null {
  if (!b.legenda) return null;
  if (!palavras) {
    throw new Error(
      'o briefing declara legenda e nenhuma palavra foi passada para compilar(). ' +
        `Leia ${b.legenda.arquivo} e passe {palavras} -- o compilador e puro e ` +
        'nao le arquivo.',
    );
  }

  const ancoraS = (() => {
    const a = b.legenda.ancora;
    if (a.tipo === 'segundo') return a.valorS;
    if (a.tipo === 'locucao') {
      if (b.audio.locucao === null) {
        // `refinar()` ja recusou isto. Se chegou aqui, alguem chamou `compilar()` sem
        // refinar -- e um lanco e melhor que um 0 silencioso, que poria a legenda 34
        // frames fora de lugar sem ninguem perceber.
        throw new Error(
          'legenda ancorada na locucao e audio.locucao e null. `refinar()` recusa isto ' +
            'com o codigo legenda-sem-ancora: chame `exigirBriefingCoerente` antes.',
        );
      }
      return b.audio.locucao.aparaAntesS;
    }
    const cena = b.cenas[a.indice];
    if (!cena || cena.fonte.tipo !== 'video') {
      throw new Error(
        `legenda ancorada na cena ${a.indice}, que nao existe ou nao tem aparaAntesS. ` +
          '`refinar()` recusa isto com o codigo legenda-sem-ancora.',
      );
    }
    return cena.fonte.aparaAntesS;
  })();

  const deslocamentoFrames =
    emFrames(b.legenda.entradaNaPecaS ?? 0, b.fps) - emFrames(ancoraS, b.fps);

  // `agrupar()` tem hoje a assinatura `(palavras, {fps})` e le `LEGENDA.maxPalavras`
  // de dentro (medido: `agrupar.ts:6-8`). Para honrar `maxPalavrasPorBloco` ele precisa
  // do parametro, e a mudanca e uma linha -- feita no Step 3b, abaixo.
  const brutos = agrupar(palavras, {
    fps: b.fps,
    maxPalavras: b.legenda.maxPalavrasPorBloco ?? LEGENDA.maxPalavras,
  });

  const blocos: Bloco[] = [];
  let grudadosEmZero = 0;
  let maiorRecuoFrames = 0;
  let descartadosAntesDoInicio = 0;
  let descartadosDepoisDoFim = 0;

  for (const x of brutos) {
    const inicioFrame = x.inicioFrame + deslocamentoFrames;
    const fimFrame = x.fimFrame + deslocamentoFrames;

    // SEM NENHUM FRAME VISIVEL: descartado, e contado. Grudar em 0 um bloco cujo FIM
    // tambem e negativo nao conserva nada -- daria um bloco de duracao negativa.
    if (fimFrame <= 0) {
      descartadosAntesDoInicio++;
      continue;
    }

    // DEPOIS DO FIM DA PECA: descartado, e contado. O numero e o que denuncia uma peca
    // encurtada por `totalFixo` que comeu a fala.
    if (inicioFrame >= duracaoPecaFrames) {
      descartadosDepoisDoFim++;
      continue;
    }

    // ATRAVESSA O FRAME 0: GRUDADO em 0, nunca descartado, e contado com o recuo.
    //
    // E o caso ja vivido: o Whisper pos a primeira palavra dentro do ar morto, e hoje o
    // `blocos.find()` de `Legenda.tsx:35` simplesmente nao acha nada -- a palavra
    // DESAPARECE EM SILENCIO. O portao de ritmo reprova quando o maior recuo passa de
    // `LEGENDA.duracaoMinFrames` (10 frames, medido em `tokens.ts`): abaixo disso e
    // arredondamento de Whisper, acima e ancora errada.
    if (inicioFrame < 0) {
      grudadosEmZero++;
      maiorRecuoFrames = Math.max(maiorRecuoFrames, -inicioFrame);
    }

    blocos.push({texto: x.texto, inicioFrame: Math.max(0, inicioFrame), fimFrame});
  }

  return {
    blocos,
    deslocamentoFrames,
    grudadosEmZero,
    maiorRecuoFrames,
    descartadosAntesDoInicio,
    descartadosDepoisDoFim,
  };
}

/**
 * `totalFixo`: devolve `falta` frames as cenas, proporcionalmente a duracao de
 * cada uma, jogando o resto inteiro na cena MAIS LONGA.
 *
 * Deterministico de proposito: empate vai para o indice menor. O portao 3 compara
 * o sha256 de dois renders do mesmo plano, e um `Math.random` ou uma ordem de
 * `Object.keys` aqui quebraria o portao sem mudar nada visivel.
 */
export function devolverFramesAsCenas(cenas: number[], falta: number): number[] {
  if (falta === 0) return [...cenas];
  const total = cenas.reduce((s, x) => s + x, 0);
  if (total <= 0) {
    throw new Error('devolverFramesAsCenas: as cenas somam zero frames');
  }
  const bruto = cenas.map((x) => (x * falta) / total);
  const inteiro = bruto.map((x) => Math.trunc(x));
  let resto = falta - inteiro.reduce((s, x) => s + x, 0);

  const ordem = cenas
    .map((x, i) => ({x, i}))
    .sort((a, bb) => (bb.x - a.x !== 0 ? bb.x - a.x : a.i - bb.i));
  let k = 0;
  const passo = resto >= 0 ? 1 : -1;
  while (resto !== 0) {
    inteiro[ordem[k % ordem.length].i] += passo;
    resto -= passo;
    k++;
  }

  const saida = cenas.map((x, i) => x + inteiro[i]);
  for (const [i, x] of saida.entries()) {
    if (x <= 0) {
      throw new Error(
        `devolverFramesAsCenas: a cena ${i} ficaria com ${x} frames. O alvo de ` +
          'duracao.alvoS e curto demais para o numero de cenas pedido.',
      );
    }
  }
  return saida;
}
```

- [ ] **Step 3b: `agrupar()` passa a receber `maxPalavras`, uma linha**

Medido: `src/legenda/agrupar.ts:6` tem a assinatura `agrupar(palavras, {fps})` e lê
`LEGENDA.maxPalavras` de dentro, nas linhas 7–8. O campo `maxPalavrasPorBloco` do briefing não tem
como chegar lá sem o parâmetro.

Em `src/legenda/agrupar.ts`, trocar a assinatura:

```ts
export function agrupar(
  palavras: Palavra[],
  {fps, maxPalavras = LEGENDA.maxPalavras}: {fps: number; maxPalavras?: number},
): Bloco[] {
  const blocos: Bloco[] = [];
  for (let i = 0; i < palavras.length; i += maxPalavras) {
    const grupo = palavras.slice(i, i + maxPalavras);
```

**O default fica aqui, e ele NÃO é um default escondido:** `LEGENDA.maxPalavras` é o token medido em
referência real (2 palavras por bloco, 2,45 blocos/s), e o briefing pode sobrescrevê-lo nomeando o
campo. Default que aponta para um token medido é o token; default que escolhe um número no olho é o
que esta spec proíbe.

`tests/agrupar.test.ts` **não muda**: medido, os 5 `it` dele chamam `agrupar(palavras, {fps: 30})`, e o
parâmetro novo é opcional.

- [ ] **Step 4: rodar o teste e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/compilar.test.ts tests/impressao.test.ts`
Expected: `compilar.test.ts` com **22** e `impressao.test.ts` com **5** — os `describe('sha256Do')` e
`describe('selarPlano')` do Step 1 moram no segundo arquivo, porque o arquivo de teste segue o módulo.

O formato da transcrição foi **medido nesta sessão** e não é suposição:
`projetos/01-private-label/transcricao.json` é um **array** de `{texto, inicioMs, fimMs}` com
**75 palavras**, a primeira `{"texto":"Você","inicioMs":0,"fimMs":340}` — exatamente o tipo
`Palavra` de `src/legenda/agrupar.ts:3`. Se o teste do rebase falhar num número de bloco,
confira a conta antes de mexer: 75 palavras a 2 por bloco dão 38 blocos, o primeiro termina no
frame 20 da fonte, o corte é de 34, logo sobram 37.

- [ ] **Step 5: criar o CLI `scripts/compilar.mjs`**

```js
// briefing.json -> plano.json. O unico escritor de plano do sistema.
//
//   node scripts/compilar.mjs --projeto=projetos/01-private-label
//   node scripts/compilar.mjs --projeto=projetos/02-voce-sabia --seco
//
// POR QUE ELE SE RELANCA
//
// O compilador e TypeScript e o Node 22.16 so carrega `.ts` com
// `--experimental-strip-types`, que nao da para ligar de dentro do processo ja
// rodando. Mesma receita de `scripts/conferir.mjs`, com os imports DINAMICOS pelo
// mesmo motivo: import estatico e resolvido antes da primeira linha executar, e o
// processo pai morreria de ERR_UNKNOWN_FILE_EXTENSION antes do relancamento.
//
// E POR QUE ELE REGISTRA `_resolver-ts.mjs`
//
// Porque `--experimental-strip-types` NAO BASTA. Todo modulo de `src/` importa sem
// extensao (`import {LEGENDA} from '../identidade/tokens'`), que e a convencao
// `moduleResolution: "bundler"` do tsconfig, e o resolvedor ESM cru do Node exige o
// caminho exato. Medido em 01/10/2026:
//
//   node --experimental-strip-types -e "await import('./src/legenda/agrupar.ts')"
//   -> ERR_MODULE_NOT_FOUND: Cannot find module '<raiz>/src/identidade/tokens'
//
// `scripts/conferir.mjs` sobrevive sem o gancho por ACIDENTE: `sondar`, `folha`,
// `telefone` e `determinismo` importam apenas builtins de `node:` e `pngjs`. Este
// script importa `esquema.ts` e `compilar.ts`, que importam meio `src/`. O unico lugar
// do repositorio que registrava o gancho era `scripts/gerar-props.mjs:173` -- e a
// Tarefa 12 apaga aquele arquivo, levando o conhecimento com ele. E por isso que ele
// esta escrito aqui, com a medicao.
//
// ELE E O UNICO ESCRITOR. `scripts/gerar-props.mjs` foi retirado no commit em que
// este nasceu: dois escritores disputando um arquivo e pior que um.

import fs from 'node:fs';
import {register} from 'node:module';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const FLAG = '--experimental-strip-types';

if (!process.execArgv.includes(FLAG)) {
  const filho = spawn(
    process.execPath,
    [FLAG, '--no-warnings', fileURLToPath(import.meta.url), ...process.argv.slice(2)],
    {stdio: 'inherit'},
  );
  filho.on('close', (codigo) => process.exit(codigo ?? 1));
  filho.on('error', (e) => {
    console.error(`nao consegui me relancar com ${FLAG}: ${e.message}`);
    process.exit(1);
  });
} else {
  try {
    await principal();
  } catch (e) {
    console.error(`\nFALHA  ${e.message}`);
    if (process.env.CANASTRA_PILHA) console.error(e);
    process.exit(1);
  }
}

async function principal() {
  const a = {projeto: 'projetos/01-private-label', seco: false};
  for (const cru of process.argv.slice(2)) {
    if (cru === '--seco') {
      a.seco = true;
      continue;
    }
    const m = /^--([a-zA-Z]+)=(.*)$/.exec(cru);
    if (!m || !(m[1] in a)) {
      throw new Error(`argumento nao entendido: ${cru}. Use --projeto=DIR ou --seco.`);
    }
    a[m[1]] = m[2];
  }

  const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  process.chdir(raiz);

  // TEM QUE VIR ANTES DO PRIMEIRO IMPORT DINAMICO de `src/`. Ver o cabecalho: sem
  // isto, `ERR_MODULE_NOT_FOUND: Cannot find module '.../src/identidade/tokens'`.
  register('./_resolver-ts.mjs', import.meta.url);

  const {zBriefing} = await import('../src/briefing/esquema.ts');
  const {compilar} = await import('../src/briefing/compilar.ts');
  const {selarPlano} = await import('../src/briefing/impressao.ts');

  const caminhoBriefing = path.join(a.projeto, 'briefing.json');
  if (!fs.existsSync(caminhoBriefing)) {
    throw new Error(`nao achei ${caminhoBriefing}. O briefing e a entrada do motor.`);
  }

  const briefing = zBriefing.parse(JSON.parse(fs.readFileSync(caminhoBriefing, 'utf8')));

  let palavras;
  if (briefing.legenda) {
    const caminhoTranscricao = path.join(a.projeto, briefing.legenda.arquivo);
    if (!fs.existsSync(caminhoTranscricao)) {
      throw new Error(
        `o briefing declara legenda em ${briefing.legenda.arquivo} e o arquivo ` +
          'nao existe. Transcreva com src/legenda/transcrever.ts antes de compilar.',
      );
    }
    const cru = JSON.parse(fs.readFileSync(caminhoTranscricao, 'utf8'));
    palavras = Array.isArray(cru) ? cru : cru.palavras;
    if (!Array.isArray(palavras)) {
      throw new Error(
        `${caminhoTranscricao} nao tem uma lista de palavras. O compilador espera ` +
          '[{texto, inicioMs, fimMs}], que e o tipo Palavra de src/legenda/agrupar.ts.',
      );
    }
  }

  // `compilar()` e puro e devolve `_sha256Briefing: ''`. Selar e ato de ESCRITA, e e
  // aqui que a escrita acontece.
  const plano = selarPlano(compilar(briefing, {palavras}), briefing);

  console.log(`\n== plano ==`);
  console.log(`  serie ................ ${plano.serie}`);
  console.log(`  fps .................. ${plano.fps}`);
  console.log(`  formatos ............. ${plano.formatos.join(', ')}`);
  console.log(
    `  duracao .............. ${plano.duracaoFrames} frames ` +
      `(${(plano.duracaoFrames / plano.fps).toFixed(3)} s)`,
  );
  console.log(`  cenas ................ ${plano.cenas.length}`);
  console.log(
    `  legenda .............. ${plano.legenda ? `${plano.legenda.blocos.length} blocos` : 'nenhuma'}`,
  );
  if (plano.legenda) {
    // OS CONTADORES DO REBASE. Nenhum bloco desaparece sem numero: era exatamente
    // assim que a primeira palavra da fala do 01-private-label sumia sem ninguem saber.
    const l = plano.legenda;
    console.log(
      `    deslocamento ....... ${l.deslocamentoFrames} frames ` +
        `(ancora: ${briefing.legenda.ancora.tipo})`,
    );
    console.log(
      `    grudados em 0 ...... ${l.grudadosEmZero}, maior recuo ${l.maiorRecuoFrames} frames`,
    );
    console.log(
      `    descartados ........ ${l.descartadosAntesDoInicio} antes do inicio, ` +
        `${l.descartadosDepoisDoFim} depois do fim`,
    );
  }
  console.log(
    `  locucao .............. ${plano.audio.locucao ? plano.audio.locucao.arquivo : 'NENHUMA'}`,
  );
  console.log(
    `  trilha ............... ${plano.audio.trilha ? plano.audio.trilha.arquivo : 'NENHUMA'}`,
  );
  console.log(`  assets ............... ${plano.assets.length}`);
  console.log(`  razao da peca ........ ${plano.razaoDaPeca ?? 'a do quadro'}`);

  for (const d of plano.diagnostico.eventos) {
    console.log(`\n  evento cena ${d.cena} #${d.indice}: "${d.texto}"`);
    for (const [formato, r] of Object.entries(d.porFormato)) {
      console.log(`    ${formato.padEnd(5)} ${r.porque}`);
    }
  }

  if (plano.diagnostico.licencasLigadas.length > 0) {
    console.log(
      `\n  AVISO licencas ligadas: ${plano.diagnostico.licencasLigadas.join(', ')}. ` +
        'Nenhuma tecnica de licenca esta implementada nesta versao: o campo registra ' +
        'a decisao, o codigo vem depois dela.',
    );
  }

  if (a.seco) {
    console.log('\n--seco: nada foi escrito.');
    return;
  }

  const destino = path.join(a.projeto, 'plano.json');
  fs.writeFileSync(destino, `${JSON.stringify(plano, null, 2)}\n`, 'utf8');
  console.log(`\n  escrito ${destino}`);
  console.log(
    '  NAO EDITE plano.json a mao: ele carrega o sha256 do briefing, e o portao de ' +
      'ritmo reprova plano cujo hash nao bate.',
  );
}
```

- [ ] **Step 6: rodar o CLI a seco no projeto real**

Run: `cd instagram/remotion && node scripts/compilar.mjs --projeto=projetos/01-private-label --seco`

Expected, e cada linha é uma conta conferível:

```
== plano ==
  serie ................ avulsa
  fps .................. 30
  formatos ............. 9:16, 1:1
  duracao .............. 696 frames (23,200 s)
  cenas ................ 1
  legenda .............. 37 blocos
    deslocamento ....... -34 frames (ancora: locucao)
    grudados em 0 ...... 1, maior recuo 14 frames
    descartados ........ 1 antes do inicio, 0 depois do fim
  locucao .............. pl.wav
  trilha ............... NENHUMA
  assets ............... 0
  razao da peca ........ 0.5625

  evento cena 0 #0: "SUA PRÓPRIA MARCA DE CAFÉ"
    9:16  cartela em 'tela': corpo 152 px, 4 linha(s), mancha 24,245% do quadro contra o piso 6,861% (1,25x a legenda de duas linhas). DOMINA
    1:1   cartela em 'tela': corpo 152 px, 4 linha(s), mancha 43,102% do quadro contra o piso 6,925% (1,25x a legenda de duas linhas). DOMINA
```

Os números da manchete foram medidos em 01/10/2026 e **são a razão de o briefing declarar
`pista: "tela"`**: em `topo`, o 1:1 daria 48 px de corpo e 3,793% de mancha, abaixo do piso de 6,925%,
e o portão reprovaria. **Leia as duas linhas de formato** — é ali que a D2 aparece em número.

E leia as **três linhas do rebase**. Elas são novas e são o que este motor passou a contar em vez de
engolir: o bloco `"Você está"` (0..20 na fonte, −34..−14 na peça) é descartado por não ter nenhum
frame visível, e `"procurando algo"` (20..49 → −14..15) é **grudado em 0** com recuo de 14 frames. O
Step 2c mediu por que: a fala de `pl.wav` começa em **1,135 s** e o Whisper pôs os dois primeiros
blocos dentro do silêncio. **Com o motor antigo, `"Você está"` nunca apareceu nesta peça e ninguém
sabia.**

- [ ] **Step 7: escrever o plano de verdade**

Run: `cd instagram/remotion && node scripts/compilar.mjs --projeto=projetos/01-private-label`
Expected: `escrito projetos/01-private-label/plano.json`.

Run:
```
cd instagram/remotion
node -e "const p=require('./projetos/01-private-label/plano.json');console.log(p._gerado_por, p._sha256Briefing.slice(0,12), p.duracaoFrames, p.legenda.maiorRecuoFrames)"
```
Expected: `src/briefing/compilar.ts <12 hexa> 696 14`.

**E conferir que o selo é do briefing, não de uma versão dele:** mude uma letra no `cta` do
`briefing.json`, rode o CLI outra vez e compare os dois hashes. Eles **têm** que diferir — é a prova de
que a serialização canônica do Step 2b vê o que está no arquivo, e não só as chaves de topo. Desfaça a
letra depois.

- [ ] **Step 8: rodar a suíte inteira e o typecheck**

Run: `cd instagram/remotion && npx vitest run && npm run tsc`
Expected: suíte com **BASE + 3 + 12 + 9 + 12 + 2 + 9 + 5 + 33 + 24 + 22 + 5** testes; `npm run tsc` sem
saída.

Nenhum pixel mudou: nada em `src/motor/*.tsx` foi tocado — **sem conferência no pixel**.

- [ ] **Step 9: commit**

```bash
git add instagram/remotion/src/briefing instagram/remotion/src/legenda/agrupar.ts \
  instagram/remotion/tests/compilar.test.ts instagram/remotion/tests/impressao.test.ts \
  instagram/remotion/scripts/compilar.mjs \
  instagram/remotion/projetos/01-private-label/plano.json
git commit -m "$(cat <<'MSG'
Briefing: compilador puro, plano gerado com o sha256 do briefing

696 frames para o 01-private-label, o mesmo DURACAO_FRAMES de Raiz.tsx:28.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 8: a fonte deixa de ser só vídeo — foto, cor e grade

A ausência **A1**, e a mais caro-benefício do plano: o acervo tem **1 vídeo contra 38 fotos
verificadas** (26 de lavoura + 12 packshots, `05-formatos.md` §1), e **5 das 12 séries partem de
foto parada**. Medido: `grep -rn "<Img" src/` só acha `PonteAssets.tsx:85`, que é instrumento de
conferência.

`registro` (`moldura | cartao | telaCheia`) é a regra da marca escrita em `proibicoes.md:24`:
*"Foto real entra por um registro que declara a origem, nunca como recorte flutuando."* A
geometria dos três é **pura e testada**, porque o que precisa de prova não mora num `.tsx`.

**Files:**
- Create: `instagram/remotion/src/motor/registro.ts`
- Create: `instagram/remotion/tests/registro.test.ts`
- Modify: `instagram/remotion/src/motor/camadas/Fonte.tsx` (reescrito)
- Modify: `instagram/remotion/src/motor/PecaVideo.tsx` (passa a montar uma `Fonte` de tipo `video`)

- [ ] **Step 1: escrever o teste que falha**

Criar `instagram/remotion/tests/registro.test.ts`:

```ts
import {describe, expect, it} from 'vitest';
import {SOMBRA} from '../src/identidade/tokens';
import {caixaDoRegistro, SOMBRA_DO_REGISTRO, recorteEmPorcento} from '../src/motor/registro';

const CAIXA = {x: 0, y: 0, largura: 1080, altura: 1920};

describe('caixaDoRegistro', () => {
  it('telaCheia e a caixa inteira: a foto E o quadro', () => {
    expect(caixaDoRegistro('telaCheia', CAIXA)).toEqual(CAIXA);
  });

  it('moldura recua a margem de lado da marca nos dois eixos', () => {
    // 14,81% (160/1080) e a MARGEM.lado que o motor ja usa. Nenhum numero novo:
    // inventar uma "largura de moldura" seria escolher no olho um numero que
    // muda de significado a cada formato.
    const m = caixaDoRegistro('moldura', CAIXA);
    expect(m.x).toBeCloseTo(1080 * (160 / 1080), 6);
    expect(m.largura).toBeCloseTo(1080 * (1 - 2 * (160 / 1080)), 6);
    expect(m.y).toBeCloseTo(1920 * (160 / 1080), 6);
    // a moldura e simetrica: o mesmo recuo em cima e embaixo
    expect(m.y).toBeCloseTo(CAIXA.altura - (m.y + m.altura), 6);
  });

  it('cartao recua a margem de TOPO e ancora no alto', () => {
    const c = caixaDoRegistro('cartao', CAIXA);
    expect(c.y).toBeCloseTo(1920 * 0.05, 6);
    expect(c.x).toBeCloseTo(1080 * 0.05, 6);
    // ancorado no alto: sobra mais embaixo que em cima
    expect(CAIXA.altura - (c.y + c.altura)).toBeGreaterThan(c.y);
  });

  it('os tres registros sao geometricamente DISTINGUIVEIS', () => {
    // Se dois registros dessem a mesma caixa, declarar a origem seria decoracao.
    const t = caixaDoRegistro('telaCheia', CAIXA);
    const m = caixaDoRegistro('moldura', CAIXA);
    const c = caixaDoRegistro('cartao', CAIXA);
    expect(m).not.toEqual(t);
    expect(c).not.toEqual(t);
    expect(c).not.toEqual(m);
  });

  it('nenhum registro sai da caixa', () => {
    for (const r of ['telaCheia', 'moldura', 'cartao'] as const) {
      const b = caixaDoRegistro(r, CAIXA);
      expect(b.x).toBeGreaterThanOrEqual(0);
      expect(b.y).toBeGreaterThanOrEqual(0);
      expect(b.x + b.largura).toBeLessThanOrEqual(CAIXA.largura + 1e-6);
      expect(b.y + b.altura).toBeLessThanOrEqual(CAIXA.altura + 1e-6);
    }
  });

  it('cada registro usa um perfil de sombra DIFERENTE: nunca a mesma em duas camadas', () => {
    expect(SOMBRA_DO_REGISTRO.moldura).toEqual(SOMBRA.papel);
    expect(SOMBRA_DO_REGISTRO.cartao).toEqual(SOMBRA.cartao);
    // telaCheia nao tem sombra: nao ha borda para a sombra cair.
    expect(SOMBRA_DO_REGISTRO.telaCheia).toBeNull();
  });
});

describe('recorteEmPorcento', () => {
  it('recorte de fracao vira largura e deslocamento em porcento', () => {
    // A foto de 4032x3024 recortada para 9:16 aproveita 1701 px de largura =
    // 0,4218 da largura. A imagem tem que ficar 1/0,4218 = 237,05% da caixa, e
    // deslocada -x/largura.
    const r = recorteEmPorcento({tipo: 'recorte', x: 0.2, y: 0, largura: 0.4218, altura: 1});
    expect(r.larguraPorcento).toBeCloseTo(237.08, 1);
    expect(r.alturaPorcento).toBeCloseTo(100, 6);
    expect(r.esquerdaPorcento).toBeCloseTo(-47.415, 2);
    expect(r.topoPorcento).toBeCloseTo(0, 6);
  });

  it('faixa devolve 100% sem deslocamento', () => {
    const r = recorteEmPorcento({tipo: 'faixa'});
    expect(r.larguraPorcento).toBe(100);
    expect(r.alturaPorcento).toBe(100);
    expect(r.esquerdaPorcento).toBe(0);
    expect(r.topoPorcento).toBe(0);
  });
});
```

- [ ] **Step 2: rodar o teste e conferir que falha**

Run: `cd instagram/remotion && npx vitest run tests/registro.test.ts`
Expected: FALHA — `Failed to resolve import "../src/motor/registro"`.

- [ ] **Step 3: criar `src/motor/registro.ts`**

```ts
// O REGISTRO DA FOTO REAL. Puro.
//
// `proibicoes.md:24-25`, textualmente: "Foto real entra por um registro que
// declara a origem (moldura, cartao, tela cheia), nunca como recorte flutuando."
//
// A regra da marca cumprida por CONSTRUCAO: `registro` e obrigatorio no esquema,
// sem default, e a geometria dos tres esta aqui, com teste. Um `.tsx` decidindo
// isto no meio de um `style` seria a regra cumprida por lembranca.
//
// NENHUM NUMERO NOVO
//
// Os recuos saem de `MARGEM`, que o motor ja usa para area segura, e as sombras de
// `SOMBRA`, que ja tem um perfil por material. Inventar uma "largura de moldura"
// seria escolher no olho um numero que muda de significado a cada formato -- e
// este arquivo nao tem constante numerica propria. Confira: as unicas literais
// abaixo sao 0, 1 e 2.

import {SOMBRA} from '../identidade/tokens';
import {MARGEM, type Caixa} from './layout';

export type Registro = 'moldura' | 'cartao' | 'telaCheia';

/**
 * Perfil de sombra de cada registro. `proibicoes.md:28` (da tabela de tokens):
 * nunca a mesma sombra em duas camadas.
 *
 * `telaCheia` nao tem sombra porque nao tem borda: nao ha onde a sombra cair.
 */
export const SOMBRA_DO_REGISTRO: Record<
  Registro,
  {dy: number; blur: number; op: number} | null
> = {
  moldura: SOMBRA.papel,
  cartao: SOMBRA.cartao,
  telaCheia: null,
};

/**
 * Onde a foto mora dentro da caixa da cena, por registro.
 *
 * `telaCheia` ..... a foto e o quadro.
 * `moldura` ....... recua `MARGEM.lado` (14,81%) nos dois eixos, simetrico: o
 *                   terra em volta e o passe-partout, e a foto se declara como
 *                   foto emoldurada.
 * `cartao` ........ recua `MARGEM.topo` (5%) nos dois eixos e ANCORA NO ALTO,
 *                   deixando a sobra embaixo -- e a geometria de um cartao
 *                   apoiado, e e onde a legenda passa.
 */
export function caixaDoRegistro(registro: Registro, caixa: Caixa): Caixa {
  if (registro === 'telaCheia') return {...caixa};

  if (registro === 'moldura') {
    const dx = caixa.largura * MARGEM.lado;
    const dy = caixa.altura * MARGEM.lado;
    return {
      x: caixa.x + dx,
      y: caixa.y + dy,
      largura: caixa.largura - 2 * dx,
      altura: caixa.altura - 2 * dy,
    };
  }

  const dx = caixa.largura * MARGEM.topo;
  const dy = caixa.altura * MARGEM.topo;
  return {
    x: caixa.x + dx,
    y: caixa.y + dy,
    largura: caixa.largura - 2 * dx,
    // Ancorado no alto: a sobra fica embaixo, onde a legenda corre. A altura e a
    // largura vezes a razao da caixa menos o recuo de topo, o que deixa o cartao
    // mais raso que a caixa sem inventar uma fracao nova.
    altura: (caixa.altura - 2 * dy) * (1 - MARGEM.topo - MARGEM.base),
  };
}

export type Enquadramento = {tipo: 'faixa'} | {
  tipo: 'recorte';
  x: number;
  y: number;
  largura: number;
  altura: number;
};

/**
 * Recorte em FRACAO da fonte -> largura e deslocamento em porcento da caixa.
 *
 * A fracao existe para o mesmo briefing servir a foto de 4032x3024 e a regravacao
 * dela em outra resolucao sem reescrever numero. O CSS quer porcento, e a conversao
 * e uma divisao -- feita aqui, uma vez, com teste, em vez de dentro de um template
 * de `style`.
 */
export function recorteEmPorcento(e: Enquadramento): {
  larguraPorcento: number;
  alturaPorcento: number;
  esquerdaPorcento: number;
  topoPorcento: number;
} {
  if (e.tipo === 'faixa') {
    return {larguraPorcento: 100, alturaPorcento: 100, esquerdaPorcento: 0, topoPorcento: 0};
  }
  const larguraPorcento = 100 / e.largura;
  const alturaPorcento = 100 / e.altura;
  return {
    larguraPorcento,
    alturaPorcento,
    esquerdaPorcento: -(e.x / e.largura) * 100,
    topoPorcento: -(e.y / e.altura) * 100,
  };
}
```

- [ ] **Step 4: rodar o teste e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/registro.test.ts`
Expected: `Tests 8 passed (8)`.

- [ ] **Step 5: reescrever `src/motor/camadas/Fonte.tsx` inteiro**

```tsx
// Camada de FONTE. Quatro tipos: video, foto, cor e grade.
//
// POR QUE DEIXOU DE SER SO VIDEO
//
// Antes de 01/10/2026 este arquivo montava `<Video>` sem alternativa (linha 48), e
// o acervo tem 1 VIDEO contra 38 FOTOS verificadas -- 26 de lavoura mais 12
// packshots (`05-formatos.md` §1). Cinco das doze series do catalogo partem de
// FOTO PARADA. `grep -rn "<Img" src/` so achava `PonteAssets.tsx:85`, que e
// instrumento de conferencia, nao peca.
//
// TRES COISAS QUE ESTA CAMADA RESOLVE E QUE NINGUEM MAIS RESOLVE
//
// 1. O CORTE DO AR MORTO, por `aparaAntesFrames`, nunca chumbado aqui -- cada
//    projeto tem o seu. `02 PL.mp4` tem 1,14 s, que a 30 fps sao 34 frames.
//
// 2. O RECORTE E DECISAO DO LAYOUT, NAO DESTA CAMADA. A caixa vem pronta de
//    `layout()`; aqui so se obedece. `overflow: hidden` existe para que um erro de
//    meio pixel nao vaze da zona, nao para cortar de proposito.
//
// 3. A PRE-MONTAGEM. `premountFor={fps}` monta a midia um segundo antes de ela
//    entrar, para o decodificador estar pronto no primeiro frame desenhado. O
//    numero e `fps`, nao 30: e um SEGUNDO. Sem isso o primeiro frame de midia pode
//    ser desenhado antes do decodificador estar pronto, e o resultado e um frame
//    errado GRAVADO no arquivo, com exit 0.
//
// `arquivo` e o NOME do arquivo dentro da subpasta `fonte/` da pasta publica do
// projeto -- so `pl.mp4`, nunca um caminho. Quem sabe o prefixo e esta camada, por
// `SUB.fonte`. O prefixo entra aqui e nao no briefing de proposito: o briefing fala
// de MEDIDA (que arquivo, que razao, que corte), nao de arrumacao de pasta.
//
// O PUSH E DA CENA, NAO DA CAMADA
//
// `push(frame, duracaoCenaFrames)` e linear porque `proibicoes.md:21` pede "push de
// camera lento, nunca impacto", e qualquer easing concentra a velocidade em algum
// trecho -- que e justamente o impacto. A escala entra como `transform: scale()`;
// quando a Tarefa 4 do plano de qualidade entrar, esta linha passa a ser a
// propriedade `scale`, e e o UNICO lugar deste arquivo que muda.

import {Video} from '@remotion/media';
import {Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import React from 'react';
import type {Fonte as FonteDeclarada} from '../../briefing/esquema';
import {COR} from '../../identidade/tokens';
import type {Caixa} from '../layout';
import {push} from '../movimento';
import {SUB} from '../pasta-publica';
import {caixaDoRegistro, recorteEmPorcento, SOMBRA_DO_REGISTRO} from '../registro';

export type PropsFonte = {
  fonte: FonteDeclarada;
  caixa: Caixa;
  /** frames de ar morto da cabeca (so `video` usa) */
  aparaAntesFrames: number;
  /** duracao DA CENA em frames: e sobre ela que o push corre */
  duracaoCenaFrames: number;
  /** escala do quadro: `largura / 1080`. Sombra e calha acompanham. */
  escala: number;
};

export const Fonte: React.FC<PropsFonte> = ({
  fonte,
  caixa,
  aparaAntesFrames,
  duracaoCenaFrames,
  escala,
}) => (
  <div
    style={{
      position: 'absolute',
      left: caixa.x,
      top: caixa.y,
      width: caixa.largura,
      height: caixa.altura,
      overflow: 'hidden',
      // O fundo e terra e nao preto: no 1:1 a sobra ao lado da coluna de video
      // fica visivel, e branco com texto centrado e exatamente o padrao de modelo
      // generativo que `proibicoes.md:13` barra.
      backgroundColor: COR.terra,
    }}
  >
    <Conteudo
      fonte={fonte}
      caixa={{x: 0, y: 0, largura: caixa.largura, altura: caixa.altura}}
      aparaAntesFrames={aparaAntesFrames}
      duracaoCenaFrames={duracaoCenaFrames}
      escala={escala}
    />
  </div>
);

const Conteudo: React.FC<PropsFonte> = ({
  fonte,
  caixa,
  aparaAntesFrames,
  duracaoCenaFrames,
  escala,
}) => {
  const {fps} = useVideoConfig();
  const frame = useCurrentFrame();

  if (fonte.tipo === 'cor') {
    return (
      <div style={{width: '100%', height: '100%', backgroundColor: fonte.cor}} />
    );
  }

  if (fonte.tipo === 'grade') {
    const calha = fonte.calha * escala;
    const largura = (caixa.largura - calha * (fonte.colunas - 1)) / fonte.colunas;
    const altura = (caixa.altura - calha * (fonte.linhas - 1)) / fonte.linhas;
    return (
      <div
        style={{
          display: 'grid',
          width: '100%',
          height: '100%',
          gridTemplateColumns: `repeat(${fonte.colunas}, 1fr)`,
          gridTemplateRows: `repeat(${fonte.linhas}, 1fr)`,
          gap: calha,
        }}
      >
        {fonte.celulas.map((celula, i) => (
          <div key={i} style={{position: 'relative', overflow: 'hidden'}}>
            <Conteudo
              fonte={celula}
              caixa={{x: 0, y: 0, largura, altura}}
              aparaAntesFrames={celula.tipo === 'video' ? aparaAntesFrames : 0}
              duracaoCenaFrames={duracaoCenaFrames}
              escala={escala}
            />
          </div>
        ))}
      </div>
    );
  }

  const escalaPush = fonte.camera === 'pushLento' ? push(frame, duracaoCenaFrames) : 1;

  if (fonte.tipo === 'video') {
    return (
      <Video
        src={staticFile(`${SUB.fonte}/${fonte.arquivo}`)}
        trimBefore={aparaAntesFrames}
        objectFit={fonte.enquadramento === 'preencher' ? 'cover' : 'contain'}
        premountFor={fps}
        style={{
          width: '100%',
          height: '100%',
          transform: `scale(${escalaPush})`,
          transformOrigin: 'center center',
        }}
      />
    );
  }

  // foto
  const dentro = caixaDoRegistro(fonte.registro, caixa);
  const r = recorteEmPorcento(fonte.enquadramento);
  const sombra = SOMBRA_DO_REGISTRO[fonte.registro];

  return (
    <div
      style={{
        position: 'absolute',
        left: dentro.x,
        top: dentro.y,
        width: dentro.largura,
        height: dentro.altura,
        overflow: 'hidden',
        boxShadow: sombra
          ? `0 ${sombra.dy * escala}px ${sombra.blur * escala}px rgba(0,0,0,${sombra.op})`
          : undefined,
      }}
    >
      <Img
        src={staticFile(`${SUB.fonte}/${fonte.arquivo}`)}
        style={{
          position: 'absolute',
          width: `${r.larguraPorcento}%`,
          height: `${r.alturaPorcento}%`,
          left: `${r.esquerdaPorcento}%`,
          top: `${r.topoPorcento}%`,
          // `contain` na faixa e `cover` no recorte: no recorte a caixa JA esta na
          // razao pedida, entao cobrir nao corta nada que o briefing nao mandou.
          objectFit: fonte.enquadramento.tipo === 'faixa' ? 'contain' : 'cover',
          transform: `scale(${escalaPush})`,
          transformOrigin: 'center center',
        }}
      />
    </div>
  );
};
```

- [ ] **Step 6: fazer `PecaVideo.tsx` montar uma fonte de tipo `video`**

`PecaVideo.tsx` continua existindo até a Tarefa 9 e precisa compilar. Trocar o bloco `<Fonte …>`
(linhas 110–114) por:

```tsx
      <Fonte
        fonte={{
          tipo: 'video',
          arquivo: p.arquivo,
          razaoExibicao: p.razaoFonte,
          aparaAntesS: p.cortarAntesFrames / fps,
          // `cover` e o que esta camada fazia antes, chumbado em `objectFit`.
          enquadramento: 'preencher',
          // Sem push: o motor antigo nao tinha push na fonte, so no bloco de texto.
          camera: 'parado',
        }}
        caixa={z.video}
        aparaAntesFrames={p.cortarAntesFrames}
        duracaoCenaFrames={durationInFrames}
        escala={width / 1080}
      />
```

E trocar a linha 97 para ler também `fps` e `durationInFrames`:

```tsx
  const {width, height, fps, durationInFrames} = useVideoConfig();
```

- [ ] **Step 7: rodar a suíte e o typecheck**

Run: `cd instagram/remotion && npx vitest run && npm run tsc`
Expected: suíte com **BASE + 3 + 12 + 9 + 12 + 2 + 9 + 5 + 33 + 24 + 22 + 5 + 8** testes; `npm run tsc`
sem saída. Os 8 novos são `tests/registro.test.ts`.

- [ ] **Step 8: CONFERÊNCIA NO PIXEL — o vídeo não muda**

Run:
```
cd instagram/remotion
npx remotion still src/index.ts Reel out/t8-f300.png --frame=300 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
node -e "const c=require('node:crypto'),f=require('node:fs');const h=n=>c.createHash('sha256').update(f.readFileSync('out/'+n+'.png')).digest('hex');console.log(h('antes-f300')===h('t8-f300')?'IDENTICO':'MUDOU')"
```
Expected: `IDENTICO`. A camada foi reescrita e o vídeo é o mesmo `cover` com o mesmo
`trimBefore`, então o pixel não tem direito de mudar. Se `MUDOU`, o suspeito é o
`premountFor={fps}`, que **não deveria** mudar frame nenhum — se mudar, era um frame errado antes
e o certo é agora; abra os dois PNG e decida olhando, não pelo hash.

- [ ] **Step 9: medir a foto, e registrar por que a conferência no pixel NÃO cabe aqui**

Run:
```
cd instagram/remotion
mkdir -p projetos/02-foto-parada/public/fonte
cp "../../base-curada/01-real-verificada/fazenda-medeiros-1250m/cafezal/IMG_1398.JPG" \
  projetos/02-foto-parada/public/fonte/cafezal.jpg
node --experimental-strip-types -e "
const {sondar} = await import('./src/motor/sondar.ts');
const s = await sondar('projetos/02-foto-parada/public/fonte/cafezal.jpg');
console.log('exibicao', s.largura + 'x' + s.altura, '| razao', s.razao.toFixed(6));
console.log('rotacao', s.rotacao.fonte, s.rotacao.graus, '| imagemParada', s.imagemParada);
"
```
(No PowerShell: `New-Item -ItemType Directory -Force projetos/02-foto-parada/public/fonte` e
`Copy-Item "<raiz>/base-curada/.../IMG_1398.JPG" projetos/02-foto-parada/public/fonte/cafezal.jpg`.
O resto é igual.)

Expected, medido em 01/10/2026 e confirmado pela Tarefa 4A:

```
exibicao 4032x3024 | razao 1.333333
rotacao exif 0 | imagemParada true
```

**Anote `1.333333`** — é o `razaoExibicao` do briefing da Tarefa 13, e lê-lo do arquivo em vez de
medi-lo é a armadilha que este repositório já pagou três vezes. `rotacao exif 0` é a resposta útil:
o EXIF **foi lido** e vale 1, contra `nenhuma`, que significaria que ninguém achou metadado. E
`imagemParada: true` é o que impede o motor de acreditar nos `25 fps` que o ffprobe inventa.

**E a conferência no pixel dos três registros não cabe nesta tarefa. A razão é mecânica:** quem monta
uma `Fonte` a partir do plano é `Cena.tsx`, e `Cena.tsx` nasce na **Tarefa 9**. Nesta tarefa a única
composição que renderiza é a antiga, por `PecaVideo.tsx`, cujas props são `{arquivo, razaoFonte,
cortarAntesFrames, manchete, blocos}` — **não existe caminho para uma foto entrar no quadro**. Render
de `registro` aqui não é caro nem difícil: é impossível.

Então a conferência está na **Tarefa 13, Step 8**, com os frames derivados das janelas de **evento** (e
não das de cena, que foi o erro da versão anterior). O que este passo garante é que ela não se perca:

- [ ] a conferência no pixel dos três registros está feita na **Tarefa 13, Step 8** — volte e marque
  esta caixa **depois** de descrever por escrito os sete stills de lá

**Por que a caixa dupla, em vez de confiar na Tarefa 13.** `caixaDoRegistro` tem teste geométrico, e
neste repositório teste geométrico **já aprovou recorte visivelmente errado** (lição do `CLAUDE.md`).
Um `registro` que chega ao fim do plano sem nunca ter sido olhado é exatamente o tipo de coisa que a
próxima sessão descobre errada numa peça publicada.

- [ ] **Step 10: commit**

```bash
git add instagram/remotion/src instagram/remotion/tests/registro.test.ts
git commit -m "$(cat <<'MSG'
Fonte: video, foto, cor e grade, com o registro da marca por construcao

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 9: existe cena — `TransitionSeries`, `Cena.tsx` e `Peca.tsx`

A ausência **A3**. Medido: `grep -rn "TransitionSeries\|<Series\|Sequence" src/` dá **5
ocorrências, todas comentário**. As séries 3, 4, 10 e 11 do catálogo não existem sem isto.

Duas decisões desta tarefa, escritas para não serem redescobertas:

- **A legenda e a trilha ficam FORA da `TransitionSeries`.** A legenda é a fala, e a fala não
  reinicia porque a imagem trocou. Dentro, ela seria remontada por cena e **na janela de
  crossfade duas legendas com textos diferentes ficariam no ar ao mesmo tempo** — bug garantido e
  invisível em miniatura. Fora, ela é uma camada só, no relógio da peça, e fica **por cima** da
  transição, o que é o comportamento certo.
- **`TransitionSeries.Overlay` fica declarado e vazio, com o motivo escrito.** Ele renderiza
  sobre o corte sem mexer na duração, e o uso canônico dele é *light leak* e flash —
  `proibicoes.md:16` proíbe flash branco instantâneo. Registrar que existe e por que está vazio
  evita que a próxima sessão o descubra e o ache grátis.

**Files:**
- Modify: `instagram/remotion/package.json` (instalar `@remotion/transitions@4.0.530`)
- Create: `instagram/remotion/src/motor/tempo-de-cena.ts` (puro, e é dele que o teste importa)
- Create: `instagram/remotion/src/motor/Cena.tsx`
- Create: `instagram/remotion/src/motor/Peca.tsx`
- Create: `instagram/remotion/src/motor/camadas/Trilha.tsx`
- Modify: `instagram/remotion/src/motor/pasta-publica.ts` (a subpasta `audio`)
- Modify: `instagram/remotion/src/motor/Raiz.tsx` (reescrito)
- Modify: `instagram/remotion/scripts/conferir.mjs` (passa a usar `plano.json`)
- Delete: `instagram/remotion/src/motor/PecaVideo.tsx`
- Create: `instagram/remotion/tests/cena-tempo.test.ts`

- [ ] **Step 1: instalar `@remotion/transitions` na versão exata do lock**

Medido: o pacote **não está instalado** — ausente do `package.json`,
`grep -c "remotion/transitions" package-lock.json` = 0, e `ls node_modules/@remotion/` lista 25
pacotes sem ele. Todos os outros `@remotion/*` estão em `4.0.530`.

Run: `cd instagram/remotion && npm install @remotion/transitions@4.0.530 --save-exact`
Expected: `added 1 package`, e `package.json` com `"@remotion/transitions": "4.0.530"` em
`dependencies`.

Run: `cd instagram/remotion && node -e "console.log(require('@remotion/transitions/package.json').version)"`
Expected: `4.0.530`. Versão diferente da dos outros `@remotion/*` é o tipo de divergência que dá
erro de runtime obscuro no render e não no import.

Esta é a **D8** da spec, e a escolha é `TransitionSeries` em vez de `Series` + `offset` negativo.
O que ela compra é **falha alta** em cinco invariantes (transição ≤ duração das cenas adjacentes;
sem duas transições adjacentes; sem dois overlays adjacentes; transição e overlay não adjacentes;
ao menos uma cena de um dos lados) que, à mão, seriam vídeo torto com exit 0 — a lição 3 do
`CLAUDE.md` outra vez.

- [ ] **Step 2: escrever o teste de tempo de cena que falha**

Criar `instagram/remotion/tests/cena-tempo.test.ts`. Ele testa a **aritmética** que a árvore vai
obedecer, não a árvore: nenhum teste unitário renderiza.

```ts
import {describe, expect, it} from 'vitest';
import {compilar} from '../src/briefing/compilar';
import {zBriefing} from '../src/briefing/esquema';
// DE `tempo-de-cena.ts`, NAO DE `Peca.tsx`.
//
// `Peca.tsx` importa `camadas/Legenda.tsx` -> `identidade/tipografia.ts`, que faz
// `loadFont` e `delayRender` no TOPO DO MODULO. Nao existe `vitest.config*` neste
// projeto (medido: `ls vitest.config*` -> No such file), entao o ambiente e `node`: sem
// `document`, e o fetch de asset estoura com `TypeError: Invalid URL`. E o mesmo modo de
// falha que os cabecalhos de `movimento.ts:5-9`, `texto-forma.ts:4-6` e
// `TextoTela.tsx:8-12` registram, e e a razao declarada de aqueles dois modulos
// existirem.
//
// A linha de Architecture deste plano diz: "a fronteira e rigida: nada que precise de
// prova mora num .tsx". Entao as duas funcoes puras nascem num `.ts`, e `Peca.tsx`
// REEXPORTA de la -- em vez de uma nota condicional dizendo "se o vitest falhar, mova".
import {
  frameDaCenaNoFrameDaPeca,
  janelaDaCenaNaPeca,
} from '../src/motor/tempo-de-cena';

function tresCenas(transicoes: unknown[]) {
  return zBriefing.parse({
    _esquema: 'canastra-briefing/1',
    serie: 'avulsa',
    formatos: ['9:16'],
    duracao: {modo: 'somaCenas'},
    cenas: [
      {duracaoS: 2, fonte: {tipo: 'cor', cor: '#3B2A1F'}, eventos: [{papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'topo'}]},
      {duracaoS: 3, fonte: {tipo: 'cor', cor: '#4A5D3A'}, eventos: [{papel: 'manchete', texto: 'DOIS', entradaS: 0, pista: 'topo'}]},
      {duracaoS: 4, fonte: {tipo: 'cor', cor: '#C8661E'}, eventos: [{papel: 'manchete', texto: 'TRES', entradaS: 0, pista: 'topo'}]},
    ],
    transicoes,
    audio: {locucao: {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 0}, trilha: null},
    gancho: 'g',
    cta: 'c',
  });
}

describe('janela de cada cena no relogio da PECA', () => {
  it('com corte, as cenas se encostam sem sobrepor', () => {
    const p = compilar(tresCenas([{tipo: 'corte'}, {tipo: 'corte'}]));
    expect(janelaDaCenaNaPeca(p, 0)).toEqual({de: 0, ate: 60});
    expect(janelaDaCenaNaPeca(p, 1)).toEqual({de: 60, ate: 150});
    expect(janelaDaCenaNaPeca(p, 2)).toEqual({de: 150, ate: 270});
    expect(p.duracaoFrames).toBe(270);
  });

  it('com fade, as janelas SE SOBREPOEM exatamente pela duracao da transicao', () => {
    // Durante a transicao as duas cenas sao renderizadas. Se as janelas nao se
    // sobrepusessem, haveria um frame de terra chapado no meio do crossfade.
    const p = compilar(tresCenas([{tipo: 'fade', duracaoS: 0.5}, {tipo: 'corte'}]));
    const a = janelaDaCenaNaPeca(p, 0);
    const b = janelaDaCenaNaPeca(p, 1);
    expect(a.ate - b.de).toBe(15);
    expect(p.duracaoFrames).toBe(270 - 15);
  });

  it('o frame da CENA e o frame da peca menos o inicio da cena', () => {
    // E o terceiro relogio: dentro de `TransitionSeries.Sequence` o Remotion
    // rebaseia `useCurrentFrame()`, e esta funcao e a mesma conta feita a mao,
    // para o teste poder verificar sem renderizar.
    const p = compilar(tresCenas([{tipo: 'corte'}, {tipo: 'corte'}]));
    expect(frameDaCenaNoFrameDaPeca(p, 1, 60)).toBe(0);
    expect(frameDaCenaNoFrameDaPeca(p, 1, 75)).toBe(15);
    expect(frameDaCenaNoFrameDaPeca(p, 2, 150)).toBe(0);
  });

  it('a soma das janelas menos as sobreposicoes E a duracao da peca', () => {
    // Invariante que pega erro de sinal: se `inicioNaPecaFrames` somasse a
    // transicao em vez de subtrair, este teste falha e o video sairia mais longo
    // que o briefing sem ninguem perceber.
    for (const trans of [
      [{tipo: 'corte'}, {tipo: 'corte'}],
      [{tipo: 'fade', duracaoS: 0.5}, {tipo: 'corte'}],
      [{tipo: 'fade', duracaoS: 0.5}, {tipo: 'wipe', duracaoS: 0.25, direcao: 'from-left'}],
    ]) {
      const p = compilar(tresCenas(trans));
      const ultima = janelaDaCenaNaPeca(p, p.cenas.length - 1);
      expect(ultima.ate).toBe(p.duracaoFrames);
    }
  });
});
```

- [ ] **Step 3: rodar o teste e conferir que falha**

Run: `cd instagram/remotion && npx vitest run tests/cena-tempo.test.ts`
Expected: FALHA — `Failed to resolve import "../src/motor/tempo-de-cena"`.

- [ ] **Step 3b: criar `src/motor/tempo-de-cena.ts` — puro, sem React**

```ts
// O TERCEIRO RELOGIO, em duas funcoes puras.
//
// POR QUE NAO MORAM EM `Peca.tsx`
//
// Porque elas tem TESTE, e `Peca.tsx` importa `camadas/Legenda.tsx` ->
// `identidade/tipografia.ts`, que faz `loadFont` e `delayRender` no topo do modulo. Nao
// existe `vitest.config*` neste projeto, logo o ambiente e `node`: sem `document`, e o
// carregamento estoura com `TypeError: Invalid URL`. Medido em 30/09/2026 -- um teste
// que so importava `Legenda.tsx` passou a asercao e o vitest ainda saiu com codigo 1.
//
// E a mesma fronteira de `movimento.ts` e `texto-forma.ts`, e ela e a linha de
// Architecture deste plano: nada que precise de prova mora num `.tsx`. `Peca.tsx`
// reexporta as duas, para quem le a arvore nao ter que caçar.

import type {Plano} from '../briefing/compilar';

/** A janela de uma cena no relogio da PECA. */
export function janelaDaCenaNaPeca(p: Plano, i: number): {de: number; ate: number} {
  const c = p.cenas[i];
  if (!c) throw new Error(`janelaDaCenaNaPeca: nao existe cena ${i} em ${p.cenas.length}`);
  return {de: c.inicioNaPecaFrames, ate: c.inicioNaPecaFrames + c.duracaoFrames};
}

/**
 * O frame da CENA, dado um frame da PECA.
 *
 * Dentro de `TransitionSeries.Sequence` o Remotion rebaseia `useCurrentFrame()`, e esta
 * funcao e a MESMA conta feita a mao -- para o teste poder verificar sem renderizar.
 */
export function frameDaCenaNoFrameDaPeca(p: Plano, i: number, framePeca: number): number {
  return framePeca - janelaDaCenaNaPeca(p, i).de;
}

/** A janela de um EVENTO no relogio da PECA. E ela que decide em que frame olhar. */
export function janelaDoEventoNaPeca(
  p: Plano,
  cena: number,
  evento: number,
): {de: number; ate: number} {
  const c = p.cenas[cena];
  if (!c) throw new Error(`janelaDoEventoNaPeca: nao existe cena ${cena}`);
  const e = c.eventos[evento];
  if (!e) {
    throw new Error(
      `janelaDoEventoNaPeca: a cena ${cena} nao tem evento ${evento} (tem ${c.eventos.length})`,
    );
  }
  const de = c.inicioNaPecaFrames + e.inicioFrames;
  return {de, ate: de + e.duracaoFrames};
}
```

**`janelaDoEventoNaPeca` existe por um defeito medido.** A versão anterior deste plano derivou as
janelas das **cenas** corretamente (0..240, 225..465, 465..715) e nunca derivou as dos **eventos dentro
delas** — então dois dos sete stills de conferência da Tarefa 13 pediam frames em que o evento que eles
deveriam mostrar **já tinha terminado**. Com a função, o frame sai de uma conta em vez de um chute, e a
Tarefa 13 Step 8 a usa.

- [ ] **Step 4: criar `src/motor/Cena.tsx`**

```tsx
// UMA CENA: a fonte mais os eventos de texto dela.
//
// O RELOGIO AQUI E O DA CENA. Este componente mora dentro de
// `TransitionSeries.Sequence`, e o Remotion rebaseia `useCurrentFrame()`: o frame 0
// deste componente e o primeiro frame DESTA cena. Por isso `evento.inicioFrames` do
// plano e cena-relativo e entra direto, sem subtracao -- o contrario do que
// `PecaVideo.tsx` fazia com `manchete.inicioFrame - cortarAntesFrames`.
//
// ORDEM DE ARVORE E ORDEM DE CAMADA (`z-index` nao vale no Remotion): fonte
// primeiro, eventos depois, na ordem em que o plano os lista. A legenda e a trilha
// NAO estao aqui: elas sao camadas da PECA, ver `Peca.tsx`.
//
// NENHUM NUMERO NASCE AQUI. Tempo vem do plano, geometria de `resolverEncaixe`,
// cadencia de `cadencia(fps)`. Se voce precisar de um numero neste arquivo, ele
// esta no lugar errado.

import {AbsoluteFill, useVideoConfig} from 'remotion';
import React from 'react';
import type {CenaCompilada} from '../briefing/compilar';
import {cadencia} from './cadencia';
import {Fonte} from './camadas/Fonte';
import {TextoTela} from './camadas/TextoTela';
import {resolverEncaixe} from './encaixe';
import type {Zonas} from './layout';

export const Cena: React.FC<{cena: CenaCompilada; zonas: Zonas}> = ({cena, zonas}) => {
  // `height` entra junto por causa da caixa da fonte que preenche o quadro, abaixo.
  const {fps, width, height} = useVideoConfig();
  const c = React.useMemo(() => cadencia(fps), [fps]);
  const escala = width / 1080;

  // MEMOIZADO, E ISSO NAO E OTIMIZACAO PREMATURA.
  //
  // `resolverEncaixe` faz uma BUSCA BINARIA de `formaTextoTela` por evento, e o corpo
  // deste componente roda em TODO FRAME da cena. Numa peca de 715 frames com 3 eventos
  // seriam mais de duas mil buscas binarias redundantes por render -- e `TextoTela.tsx`
  // memoiza `formaTextoTela` (linhas 93-96) exatamente por esse motivo, que e o
  // precedente escrito do repositorio.
  //
  // As dependencias sao a cena, as zonas e a cadencia: nenhuma delas muda por frame.
  const postos = React.useMemo(
    () =>
      cena.eventos.map((e) => {
        const r = resolverEncaixe({
          texto: e.texto,
          papel: e.papel,
          pista: e.pista,
          zonas,
          cadencia: c,
          palavraAcento: e.palavraAcento,
        });
        // As MESMAS zonas que `resolverEncaixe` usou para medir. Passar outras daria um
        // corpo diferente do que o compilador relatou no diagnostico, e o portao de
        // ritmo estaria medindo uma peca que nao e a renderizada.
        const zonasDoEvento: Zonas =
          r.modo === 'cartela' ? zonas : {...zonas, manchete: r.caixa};
        return {e, r, zonasDoEvento};
      }),
    [cena.eventos, zonas, c],
  );

  // A CAIXA DA FONTE NAO E SEMPRE `zonas.video`, E ESSA E A OUTRA METADE DO
  // CONSERTO DE `razaoDaPeca()`.
  //
  // `zonas.video` e a caixa de CONTAIN: ela e letterboxada quando a razao da peca
  // nao e a do quadro. Uma cena que declara `enquadramento: 'preencher'` (video) ou
  // `{tipo: 'recorte'}` (foto) esta dizendo o contrario -- que ela CORTA para encher
  // o quadro --, e `registro: 'telaCheia'` exige `recorte` (o refinador recusa
  // `telaCheia` + `faixa`). Se essa cena recebesse `zonas.video`, "tela cheia"
  // encheria a FAIXA e nao o quadro: medido, numa peca de razao 1,3333 no 9:16 a
  // faixa e 1080x810 e sobrariam 57,81% de terra chapado em cima e embaixo.
  //
  // Entao: cena que preenche recebe o QUADRO; cena em contain recebe `zonas.video`.
  // Numa peca sem nenhuma cena em contain, `razaoDaPeca()` devolve `null`, a razao
  // vira a do quadro e os dois valores coincidem -- este ramo so se separa na peca
  // MISTA, que e exatamente o caso da peca de prova da Tarefa 13.
  //
  // O texto continua medido nas `zonas` da peca, que sao as mesmas que o compilador
  // relatou: deixar o evento seguir a caixa da cena faria o corpo da manchete mudar
  // de cena para cena, e o portao de ritmo estaria medindo outra peca.
  const preenche =
    (cena.fonte.tipo === 'video' && cena.fonte.enquadramento === 'preencher') ||
    (cena.fonte.tipo === 'foto' && cena.fonte.enquadramento.tipo === 'recorte');
  const caixaDaFonte = preenche
    ? {x: 0, y: 0, largura: width, altura: height}
    : zonas.video;

  return (
    <AbsoluteFill>
      <Fonte
        fonte={cena.fonte}
        caixa={caixaDaFonte}
        aparaAntesFrames={cena.aparaAntesFrames}
        duracaoCenaFrames={cena.duracaoFrames}
        escala={escala}
      />
      {postos.map(({e, r, zonasDoEvento}, i) => (
        <TextoTela
          key={`${i}-${e.texto}`}
          texto={e.texto}
          modo={r.modo}
          zonas={zonasDoEvento}
          inicioFrame={e.inicioFrames}
          duracaoFrames={e.duracaoIrmaoFrames}
          papel={e.papel}
          palavraAcento={e.palavraAcento}
        />
      ))}
    </AbsoluteFill>
  );
};
```

- [ ] **Step 5: criar `src/motor/Peca.tsx`**

```tsx
// A PECA. Uma composicao unica que serve todos os formatos: ela nao sabe se e Reel,
// Feed 1:1, 4:5 ou 16:9 -- pergunta a dimensao do quadro ao Remotion e deixa
// `layout()` decidir onde cada camada vive. E isso que faz o 1:1 ser
// REENQUADRAMENTO e nao recorte do 9:16, e nenhuma cena, nenhum 4:5 e nenhum
// briefing cria um `PecaFeed`.
//
// A ARVORE, e por que ela e esta:
//
//   AbsoluteFill(terra)
//     TransitionSeries          AS CENAS, e so elas
//       Sequence(premountFor)   -> Cena: fonte + eventos, no relogio DA CENA
//     Legenda                   FORA: relogio da PECA, continua
//     Trilha                    FORA: relogio da PECA
//
// POR QUE A LEGENDA FICA FORA
//
// A legenda e a fala, e a fala nao reinicia porque a imagem trocou. Dentro da
// `TransitionSeries` ela seria remontada por cena, `deslocamentoFrames` viraria um
// numero por cena, e na janela de crossfade DUAS legendas com textos diferentes
// ficariam no ar ao mesmo tempo -- bug garantido e invisivel em miniatura. Fora,
// ela e uma camada so e fica POR CIMA da transicao, que e o comportamento certo.
//
// `TransitionSeries.Overlay` EXISTE, NAO E USADO, E NAO E DECLARADO -- DE PROPOSITO
//
// Ele renderiza sobre o corte sem mexer na duracao, e o uso canonico dele e light leak e
// flash. `proibicoes.md:16` proibe "Flash branco instantaneo". Esta nota existe para a
// proxima sessao nao o descobrir e achar que e gratis.
//
// A spec §3.2.1 pede que ele fique "declarado e vazio, com o motivo escrito". Aqui ele
// fica so com o MOTIVO ESCRITO, sem a declaracao, e a divergencia esta registrada nos
// Riscos assumidos do plano: um `<TransitionSeries.Overlay />` vazio no JSX e codigo
// morto que o proximo leitor tenta preencher, e a `TransitionSeries` tem invariante sobre
// overlay adjacente -- um overlay vazio no lugar errado vira erro de runtime no render,
// nao aviso. Comentario explica sem criar o risco.
//
// POR QUE OS FILHOS SAO UM ARRAY E NAO FRAGMENTS
//
// `TransitionSeries` inspeciona os filhos diretos para saber o que e cena e o que e
// transicao. Embrulhar um par cena+transicao num `<React.Fragment>` esconde os dois
// dele. Um array plano com `key` em cada item e o que ele entende.

// Nao ha `Sequence` nem `Audio` neste import: quem sequencia e a
// `TransitionSeries`, e o `<Audio>` vive em `camadas/Trilha.tsx`.
import {AbsoluteFill, useVideoConfig} from 'remotion';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {wipe} from '@remotion/transitions/wipe';
import React from 'react';
import type {Plano} from '../briefing/compilar';
import {COR} from '../identidade/tokens';
import {Cena} from './Cena';
import {Legenda} from './camadas/Legenda';
import {Trilha} from './camadas/Trilha';
import {layout} from './layout';
import {pistas} from './pista';

// As tres funcoes de tempo sao REEXPORTADAS de `tempo-de-cena.ts`, onde elas tem teste.
// Elas nao podem morar aqui: este arquivo importa `camadas/Legenda`, que puxa
// `identidade/tipografia.ts`, que faz `loadFont` no topo do modulo e derruba o vitest em
// ambiente `node` com `TypeError: Invalid URL`. A reexportacao existe para quem le a
// arvore achar as tres no lugar onde espera.
export {
  frameDaCenaNoFrameDaPeca,
  janelaDaCenaNaPeca,
  janelaDoEventoNaPeca,
} from './tempo-de-cena';

export const Peca: React.FC<Plano> = (p) => {
  const {width, height, fps} = useVideoConfig();
  const zonas = layout({
    largura: width,
    altura: height,
    // `razaoDaPeca` e a MENOR razao entre as cenas que entram por CONTAIN
    // (`enquadramento: 'faixa'`): com ela, a caixa de legenda cabe sobre o video de
    // todas elas. `null` = nenhuma cena em contain, e ai a razao e a do quadro e a
    // imagem o ocupa inteiro. Cena que PREENCHE nao entra nessa conta e tambem nao
    // usa `zonas.video` -- ver a caixa da fonte em `Cena.tsx`.
    razaoFonte: p.razaoDaPeca ?? width / height,
  });

  const filhos: React.ReactNode[] = [];
  p.cenas.forEach((cena, i) => {
    filhos.push(
      <TransitionSeries.Sequence
        key={`cena-${i}`}
        durationInFrames={cena.duracaoFrames}
        // UM SEGUNDO de pre-montagem, derivado de fps. E onde a fonte da cena
        // SEGUINTE tem de estar bufferizada antes do crossfade comecar: sem isso o
        // primeiro frame da transicao pode ser desenhado antes do decodificador
        // estar pronto, e o frame errado vai GRAVADO no arquivo com exit 0.
        premountFor={fps}
      >
        <Cena cena={cena} zonas={zonas} />
      </TransitionSeries.Sequence>,
    );

    const t = p.transicoes[i];
    if (!t || t.duracaoFrames === 0) return;
    filhos.push(
      <TransitionSeries.Transition
        key={`transicao-${i}`}
        timing={linearTiming({durationInFrames: t.duracaoFrames})}
        // `presentation` NUNCA e omitido: o default do Remotion e `slide()`, que
        // ninguem do nosso lado escolheu e que encosta em whip pan
        // (`proibicoes.md:16`). `iris`, `clockWipe` e `flip` ficam fora pelo mesmo
        // motivo, e por isso o enum de transicao e fechado em corte/fade/wipe.
        presentation={
          t.tipo === 'wipe'
            ? wipe({direction: t.direcao as Parameters<typeof wipe>[0]['direction']})
            : fade()
        }
      />,
    );
  });

  return (
    // O fundo e terra, nao preto e nunca branco: no 1:1 a sobra ao lado da coluna
    // de video fica visivel, e branco com texto centrado e exatamente o padrao de
    // modelo generativo que `proibicoes.md:13` barra.
    <AbsoluteFill style={{backgroundColor: COR.terra}}>
      <TransitionSeries>{filhos}</TransitionSeries>

      {p.legenda ? (
        <Legenda
          blocos={p.legenda.blocos}
          caixa={pistas(zonas).rodape}
          escala={width / 1080}
          // ZERO: o compilador ja entregou os blocos no relogio da PECA. O
          // deslocamento existia porque `Legenda.tsx` convertia o relogio na hora;
          // com N cenas isso seria um numero por cena.
          deslocamentoFrames={0}
        />
      ) : null}

      {/* AS DUAS FAIXAS, no relogio da PECA, fora da TransitionSeries. A locucao mora em
          `public/fonte/` (material cru do projeto, e `pl.wav` ja esta la); a trilha mora
          em `public/audio/`, subpasta nova, porque musica licenciada tem procedencia e
          licenca que material gravado por nos nao tem. */}
      <Trilha audio={p.audio} duracaoPecaFrames={p.duracaoFrames} />
    </AbsoluteFill>
  );
};
```

- [ ] **Step 6: criar `src/motor/camadas/Trilha.tsx`** (a ausência A4)

**Duas coisas aqui foram medidas em `node_modules`, e uma delas contradiz o que o plano anterior
afirmava.**

1. **`loop` É prop declarada — mas do `Audio` de `@remotion/media`, não do de `remotion`.** Medido:
   `node_modules/remotion/dist/cjs/audio/props.d.ts` **não** tem `loop?: boolean` (só
   `loopVolumeCurveBehavior`), e o `Audio` de lá estende `React.AudioHTMLAttributes`, onde `loop` é
   atributo HTML nativo — ou seja compila e **pode ser ignorado no pipeline de render**, que é a lição
   3 do `CLAUDE.md`. Já `node_modules/@remotion/media/dist/audio/props.d.ts:26` declara
   **`loop?: boolean`** no próprio `AudioProps`, ao lado de `trimBefore`, `volume` e `premountFor`. O
   plano anterior importava de `remotion` e afirmava *"repete a faixa quando ela e mais curta que a
   peca"* sem medir. **Importe de `@remotion/media`**, que é de onde `Fonte.tsx` já importa o `Video`.
2. **`volume` aceita função de frame.** Medido: `node_modules/remotion/dist/cjs/volume-prop.d.ts:1` é
   `export type VolumeProp = number | ((frame: number) => number)`. É isso que torna
   `fadeEntradaS`/`fadeSaidaS` implementáveis sem filtro de ffmpeg.

```tsx
// CAMADA DE AUDIO: locucao e trilha. O `<Audio>` que nao existia.
//
// A AUSENCIA QUE ISTO FECHA
//
// Medido em 30/09/2026: `grep -rn "Audio" src/` so achava `motor/audio/normalizar.ts`
// (medicao POS-render) e um comentario prevendo um `<Audio>` futuro. Nao havia nenhum na
// arvore, e todo som era carona do `<Video>`. Consequencia: TODA peca de foto parada
// saia MUDA -- e 5 das 12 series do catalogo partem de foto parada.
//
// E isso nao e questao de gosto: `05-formatos.md` §3 registra, como [oficial], que Reel
// sem audio perde elegibilidade para nao-seguidor. "Mudo" no catalogo significa SEM
// LOCUCAO, nunca sem faixa. A serie 4 e explicitamente "sem voz, COM faixa".
//
// DE ONDE VEM O `Audio`, E POR QUE ISSO IMPORTA
//
// De `@remotion/media`, nao de `remotion`. Medido em `node_modules`:
//   - `remotion/dist/cjs/audio/props.d.ts` NAO declara `loop`; o `Audio` de la estende
//     `React.AudioHTMLAttributes`, onde `loop` e atributo HTML nativo -- compila e pode
//     ser ignorado no render. Seria a licao 3 do CLAUDE.md: parametro aceito e ignorado.
//   - `@remotion/media/dist/audio/props.d.ts:26` declara `loop?: boolean` no proprio
//     `AudioProps`, ao lado de `trimBefore`, `volume` e `premountFor`.
// `Fonte.tsx` ja importa o `Video` deste mesmo pacote.
//
// A NORMALIZACAO NAO E AQUI
//
// `AUDIO = {lufs: -14, picoDbtp: -1}` e alvo de POS-render: quem o aplica e
// `scripts/normalizar-audio.mjs`, com `-c:v copy`, idempotente, sobre a MISTURA.
// `ganhoDb` aqui e RELACAO ENTRE AS FAIXAS -- quanto a trilha fica abaixo da voz --, nao
// nivel absoluto. Mexer nele para "acertar o LUFS" e trabalho perdido, porque a
// normalizacao vem depois e por cima.
//
// FICA FORA DA `TransitionSeries`, no relogio da PECA, pelo mesmo motivo da legenda: a
// faixa nao reinicia porque a imagem trocou.

import {Audio} from '@remotion/media';
import {interpolate, staticFile, useVideoConfig} from 'remotion';
import React from 'react';
import type {Audio as AudioDeclarado, Faixa} from '../../briefing/esquema';
import {SUB} from '../pasta-publica';

/** dB relativo -> ganho linear. `-18 dB` = 0,126; `0 dB` = 1. */
function linear(db: number): number {
  return Math.pow(10, db / 20);
}

const UmaFaixa: React.FC<{
  faixa: Faixa;
  subpasta: string;
  loopar?: boolean;
  fadeEntradaS?: number;
  fadeSaidaS?: number;
  duracaoPecaFrames: number;
}> = ({faixa, subpasta, loopar, fadeEntradaS, fadeSaidaS, duracaoPecaFrames}) => {
  const {fps} = useVideoConfig();
  const ganho = linear(faixa.ganhoDb);
  const entrada = Math.max(0, Math.round((fadeEntradaS ?? 0) * fps));
  const saida = Math.max(0, Math.round((fadeSaidaS ?? 0) * fps));

  // `volume` COMO FUNCAO DE FRAME, que `VolumeProp` declara (medido em
  // `remotion/dist/cjs/volume-prop.d.ts:1`). Sem fade os dois sao 0 e a funcao devolve o
  // ganho constante -- nenhuma rampa por acidente.
  const volume = React.useCallback(
    (frame: number) => {
      const sobe =
        entrada === 0
          ? 1
          : interpolate(frame, [0, entrada], [0, 1], {extrapolateRight: 'clamp'});
      const desce =
        saida === 0
          ? 1
          : interpolate(frame, [duracaoPecaFrames - saida, duracaoPecaFrames], [1, 0], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
      return ganho * Math.min(sobe, desce);
    },
    [entrada, saida, ganho, duracaoPecaFrames],
  );

  return (
    <Audio
      src={staticFile(`${subpasta}/${faixa.arquivo}`)}
      // `aparaAntesS` e APARA (§2.2): de onde o arquivo comeca a tocar. Ela nunca
      // posiciona nada na peca.
      trimBefore={Math.round(faixa.aparaAntesS * fps)}
      volume={volume}
      {...(loopar !== undefined ? {loop: loopar} : {})}
      premountFor={fps}
    />
  );
};

export const Trilha: React.FC<{
  audio: AudioDeclarado;
  duracaoPecaFrames: number;
}> = ({audio, duracaoPecaFrames}) => (
  <>
    {audio.locucao ? (
      // LOCUCAO -> `SUB.fonte`. Ela e material cru do projeto e ja esta la: medido,
      // `projetos/01-private-label/public/fonte/` contem `pl.mp4` E `pl.wav`. Zero
      // mudanca de convencao. E ela NAO recebe `loop`: voz repetida nao e faixa, e erro.
      <UmaFaixa
        faixa={audio.locucao}
        subpasta={SUB.fonte}
        duracaoPecaFrames={duracaoPecaFrames}
      />
    ) : null}
    {audio.trilha ? (
      // TRILHA -> `SUB.audio`, subpasta NOVA. Separada de proposito: musica licenciada
      // tem procedencia e licenca que material gravado por nos nao tem, e guardar as duas
      // na mesma pasta perde essa distincao -- que e justamente o que a D9 precisa
      // decidir. Medido: `public/audio/` nao existe hoje.
      <UmaFaixa
        faixa={audio.trilha}
        subpasta={SUB.audio}
        loopar={audio.trilha.loopar}
        fadeEntradaS={audio.trilha.fadeEntradaS}
        fadeSaidaS={audio.trilha.fadeSaidaS}
        duracaoPecaFrames={duracaoPecaFrames}
      />
    ) : null}
  </>
);
```

E `SUB` ganha a terceira subpasta. Medido: `src/motor/pasta-publica.ts:33-38` declara hoje
`SUB = {fonte, assets}` e só isso.

```ts
export const SUB = {
  fonte: 'fonte',
  assets: 'assets',
  /**
   * Trilha de audio. SEPARADA de `fonte` de proposito: musica licenciada tem procedencia
   * e licenca que material gravado por nos nao tem, e guardar as duas na mesma pasta
   * perde a distincao. E a D9 da spec, e ela bloqueia 5 series por elegibilidade -- nao
   * por gosto.
   */
  audio: 'audio',
} as const;
```

- [ ] **Step 6b: PROVAR que o `loop` da trilha funciona, em vez de acreditar no `tsc`**

O `tsc` **não é portão aqui**, e essa é a lição 3 do `CLAUDE.md` outra vez: um parâmetro aceito pelo
tipo pode ser ignorado pelo pipeline. Então mede-se o efeito.

A prova é barata e usa o que já está no disco: `pl.wav` tem **24,33 s** (medido). Uma peça de **35 s**
cuja única faixa é essa trilha, com `loopar: true`, tem que ter energia depois de 24,33 s. Sem loop,
ali é silêncio digital.

Run:
```
cd instagram/remotion
node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -hide_banner \
  -i <a peca com trilha> -ss 25 -t 3 -af volumedetect -f null - 2>&1 | grep -i volume
```
Expected: `mean_volume` **acima de −60 dB**. Silêncio digital dá `-91.0 dB` ou `-inf`, e é isso que um
`loop` ignorado produz.

**Este passo depende de uma peça com trilha, e ela nasce na Tarefa 13.** A peça de prova de lá usa a
locução como trilha e tem 23,833 s — mais curta que a faixa, então ela **não** exercita o loop. Para
medir de verdade é preciso uma peça mais longa que a faixa, e o caminho mais barato é uma variante do
briefing da Tarefa 13 com `duracao: {"modo":"totalFixo","alvoS":35}` e `loopar: true`, renderizada uma
vez e descartada.

- [ ] o `loop` da trilha foi medido com `volumedetect` depois de 24,33 s

**Se o `loop` NÃO funcionar**, o campo vira mentira e a saída honesta é uma das duas: tirar `loopar` do
esquema e exigir faixa mais longa que a peça (o refinador passa a comparar as durações, e para isso
precisa de `sondar()` — que a Tarefa 4A já ensinou a medir áudio), ou repetir a faixa por composição no
ffmpeg, fora do Remotion. **Nenhuma das duas é adivinhação: escolha depois de ver o `mean_volume`.**

- [ ] **Step 7: rodar o teste de cena e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/cena-tempo.test.ts`
Expected: `Tests 4 passed (4)`.

**Não pode falhar com `TypeError: Invalid URL`**, porque o teste importa
`src/motor/tempo-de-cena.ts`, que não importa nenhum `.tsx`. A versão anterior deste plano importava de
`Peca.tsx` e punha o conserto numa **nota condicional** deste passo (*"se o vitest falhar, as duas
funções têm que sair para..."*) — contrariando a própria linha de Architecture do plano, e deixando o
executor descobrir na falha o que já estava medido: `Legenda.tsx` → `tipografia.ts` → `loadFont` no topo
do módulo, sem `vitest.config*` no projeto, logo ambiente `node`, logo sem `document`.

Se ainda assim falhar, o suspeito é **`src/briefing/compilar.ts`**: o teste o importa por valor
(`compilar()`), e se alguém puser `node:crypto` de volta lá o vitest carrega um módulo Node-only. O
hash mora em `briefing/impressao.ts` exatamente por isso (Tarefa 7, Step 2b).

- [ ] **Step 8: reescrever `src/motor/Raiz.tsx` inteiro**

```tsx
// Registro das composicoes.
//
// UMA COMPOSICAO POR FORMATO, UM COMPONENTE SO
//
// `Reel`, `Feed`, `Feed4x5` e `Larga` sao a MESMA peca (`Peca`) com dimensao
// diferente. Nao ha componente separado por formato de proposito: a diferenca
// inteira vive em `layout()`, que reenquadra em vez de recortar. Se um dia aparecer
// um "PecaFeed", o motor perdeu a propriedade que ele existe para ter.
//
// O FPS E A DURACAO VEM DO PLANO, NAO DE UMA CONSTANTE
//
// Antes de 01/10/2026 havia `FPS = 30` chumbado na linha 22 e
// `DURACAO_FRAMES = 696` derivado em tempo de modulo -- a peca do primeiro projeto
// estava escrita no registro das composicoes. Agora `calculateMetadata` le o
// `plano.json` passado por `--props` e devolve `fps` e `durationInFrames` dele.
// Isto e a **D7(a)** da spec, e a consequencia esta escrita nos Riscos assumidos do
// plano: `--props` deixa de ser opcional para um render de verdade.
//
// A DIMENSAO NAO VEM DO PLANO
//
// Ela vem de `DIMENSAO[formato]`, fixa por composicao. Deixar o plano escolher
// largura e altura permitiria um briefing pedir 1080x1081, e nenhum portao pegaria.
//
// O PLANO NAO E VALIDADO POR ZOD AQUI, E ISSO E UMA ESCOLHA
//
// `plano.json` e ARTEFATO GERADO: `compilar.ts` ja o produziu a partir de um
// briefing que passou por `zBriefing` e por `refinar()`. Um segundo esquema zod
// espelhando `Plano` seria uma segunda fonte de verdade para o mesmo tipo, e
// divergiria no primeiro campo novo. Quem protege contra plano editado a mao e o
// `_sha256Briefing` que ele carrega, conferido pelo portao de ritmo ANTES do render.
// Isto supera o objetivo "schema zod nas composicoes" da Tarefa 5 do plano de
// qualidade, pelo motivo acima.

import {Composition} from 'remotion';
import React from 'react';
import {DIMENSAO, type Formato} from '../briefing/esquema';
import type {Plano} from '../briefing/compilar';
import {Peca} from './Peca';
import {PonteAssets, PONTE_PADRAO} from './PonteAssets';
import {COR, TIPO} from '../identidade/tokens';
import {PILHA} from '../identidade/tipografia';

/**
 * O plano de reserva. UMA cena de terra de 1 segundo, sem evento e sem legenda.
 *
 * Um render sem `--props` sai visivelmente incompleto, que e melhor que sair com
 * conteudo de exemplo parecendo pronto: foi um placeholder que fez quatro MP4
 * sairem com legenda inventada queimada no quadro (ver o cabecalho de
 * `gerar-props.mjs`, retirado na Tarefa 12).
 */
const PLANO_VAZIO: Plano = {
  _gerado_por: 'src/motor/Raiz.tsx (plano de reserva, nao compilado)',
  _sha256Briefing: '',
  serie: 'avulsa',
  fps: 30,
  formatos: ['9:16'],
  duracaoFrames: 30,
  razaoDaPeca: null,
  cenas: [
    {
      duracaoFrames: 30,
      inicioNaPecaFrames: 0,
      fonte: {tipo: 'cor', cor: COR.terra},
      aparaAntesFrames: 0,
      eventos: [],
    },
  ],
  transicoes: [],
  legenda: null,
  // `audio` e obrigatorio no briefing, e aqui as duas faixas sao null de proposito: um
  // plano de RESERVA nao tem arquivo nenhum para tocar. `refinar()` recusaria este
  // objeto -- e isso esta certo, porque ele nunca passa por `refinar()`: ele existe
  // para um render sem `--props` sair visivelmente incompleto em vez de parecer pronto.
  audio: {locucao: null, trilha: null},
  assets: [],
  licencas: {
    particulas: false,
    orbesDeBrilho: false,
    varreduraDeLuz: false,
    shockwave: false,
    molaComOvershoot: false,
    revelarCaractereACaractere: false,
    flashNoCorte: false,
    irisWipe: false,
    motionBlurBurst: false,
    swipeMarcaTexto: false,
    highlightPalavraAtiva: false,
    aceitaTempoMorto: false,
    justificativa: '',
  },
  exigePreservacao: false,
  gancho: '',
  cta: '',
  diagnostico: {eventos: [], licencasLigadas: []},
};

/** `fps` e `durationInFrames` do plano; largura e altura do formato. */
const metadados = (formato: Formato) => ({props}: {props: Plano}) => ({
  durationInFrames: props.duracaoFrames,
  fps: props.fps,
  width: DIMENSAO[formato].largura,
  height: DIMENSAO[formato].altura,
});

// A composicao de teste tambem desenha texto, entao tambem usa a pilha da marca.
// Ela e a tela mais barata para conferir se a tipografia carregou:
// `remotion still src/index.ts Teste <arq>` sai em segundos e a palavra CANASTRA em
// Archivo Black nao se parece com nada que o Chrome traga de casa.
const Teste: React.FC = () => (
  <div style={{flex: 1, background: '#1a1410', color: COR.creme,
               display: 'flex', alignItems: 'center', justifyContent: 'center',
               fontFamily: PILHA.manchete, fontWeight: TIPO.manchete.peso,
               fontSize: 90}}>CANASTRA</div>
);

export const Raiz: React.FC = () => (
  <>
    <Composition
      id="Reel"
      component={Peca}
      defaultProps={PLANO_VAZIO}
      calculateMetadata={metadados('9:16')}
      durationInFrames={PLANO_VAZIO.duracaoFrames}
      fps={PLANO_VAZIO.fps}
      width={DIMENSAO['9:16'].largura}
      height={DIMENSAO['9:16'].altura}
    />
    <Composition
      id="Feed"
      component={Peca}
      defaultProps={PLANO_VAZIO}
      calculateMetadata={metadados('1:1')}
      durationInFrames={PLANO_VAZIO.duracaoFrames}
      fps={PLANO_VAZIO.fps}
      width={DIMENSAO['1:1'].largura}
      height={DIMENSAO['1:1'].altura}
    />
    <Composition
      id="Feed4x5"
      component={Peca}
      defaultProps={PLANO_VAZIO}
      calculateMetadata={metadados('4:5')}
      durationInFrames={PLANO_VAZIO.duracaoFrames}
      fps={PLANO_VAZIO.fps}
      width={DIMENSAO['4:5'].largura}
      height={DIMENSAO['4:5'].altura}
    />
    {/* 16:9 e formato LATENTE, nao entrega: a margem de base dele e 51,03% da
        altura (medido). Registrado porque `layout()` o rotula e porque a serie 12
        recebe corte de criador; nenhum briefing do catalogo o pede hoje. */}
    <Composition
      id="Larga"
      component={Peca}
      defaultProps={PLANO_VAZIO}
      calculateMetadata={metadados('16:9')}
      durationInFrames={PLANO_VAZIO.duracaoFrames}
      fps={PLANO_VAZIO.fps}
      width={DIMENSAO['16:9'].largura}
      height={DIMENSAO['16:9'].altura}
    />
    <Composition id="Teste" component={Teste}
      durationInFrames={60} fps={30} width={1080} height={1920} />

    {/* Instrumento de conferencia, nao peca: prova que `--public-dir` esta
        apontando para uma pasta que contem `assets/` e que os tres recortes
        carregam. 1 frame porque um still e tudo que ela precisa produzir.
        Formato deitado porque sao tres embalagens em pe lado a lado. */}
    <Composition id="PonteAssets" component={PonteAssets}
      durationInFrames={1} fps={30} width={1920} height={1080}
      defaultProps={PONTE_PADRAO} />
  </>
);
```

- [ ] **Step 9: apagar `PecaVideo.tsx` e apontar `conferir.mjs` para o plano**

Run: `cd instagram/remotion && rm src/motor/PecaVideo.tsx`

Em `scripts/conferir.mjs`, trocar a linha que monta o caminho das props (era
`const props = path.join(a.projeto, 'props.json');`) por:

```js
  // `plano.json`, nao `props.json`: o plano e o artefato que `compilar.ts` gera a
  // partir do briefing, e e o unico que a composicao entende desde 01/10/2026.
  const props = path.join(a.projeto, 'plano.json');
```

E na lista de arquivos exigidos, trocar o rótulo `'o props.json'` por `'o plano.json'` e a
mensagem de erro `'Rode a Tarefa 7 (render dos dois formatos) antes dos portoes.'` por:

```js
        `${rotulo} nao existe: ${p}. Rode ` +
          '`node scripts/compilar.mjs --projeto=<dir>` e depois o render, antes dos ' +
          'portoes.',
```

- [ ] **Step 10: rodar a suíte e o typecheck**

Run: `cd instagram/remotion && npx vitest run && npm run tsc`
Expected: `npm run tsc` sem saída. A suíte perde o que quebrar por causa de `PecaVideo.tsx`: se
`tests/manchete-props.test.ts` falhar no import, **não o apague** — ele é o portão que prova que
a manchete é citação literal da fala, e a Tarefa 12 o migra para o briefing. Até lá, ele só lê
`props.json` e `transcricao.json`, então não deveria importar `PecaVideo`. Confira com
`grep -n "PecaVideo" tests/*.ts`: se aparecer, troque o import pelo tipo do plano
(`import type {Plano} from '../src/briefing/compilar';`).

- [ ] **Step 11: render de verdade, e CONFERÊNCIA NO PIXEL do Reel**

Este é o primeiro render do motor novo, e **o que pode e o que não pode mudar está decidido de
antemão**, por medição:

| o que | muda? | por quê |
|---|---|---|
| manchete no **9:16** | **não** | o briefing declara `pista: "tela"` → `encaixe: cartela` → `modo: 'cartela'`, e `formaTextoTela` no modo cartela usa `zonas.seguro`, que o conserto da Tarefa 4 não tocou no 9:16. Medido: 152 px de corpo, 4 linhas — os mesmos de hoje |
| legenda no **9:16** | **não** | medido: `x 160,00`, `largura 760,00` antes e depois do conserto |
| vídeo no **9:16** | **não** | `cover` com o mesmo `trimBefore: 34`. O `premountFor={fps}` é novo e **não deveria** mover frame nenhum |
| legenda no **1:1** e **4:5** | **SIM** | a caixa encurta 25,0% e 19,8% (medido). É a parte paga do conserto |
| manchete no **1:1** | **não**, com `pista: "tela"` | 152 px de corpo nos dois. Em `pista: "topo"` daria 48 px e o portão reprovaria — e é isso que a D2 pergunta |

Run:
```
cd instagram/remotion
npx remotion render src/index.ts Reel out/t9-reel.mp4 \
  --props=projetos/01-private-label/plano.json \
  --public-dir=projetos/01-private-label/public
npx remotion still src/index.ts Reel out/t9-f120.png --frame=120 \
  --props=projetos/01-private-label/plano.json \
  --public-dir=projetos/01-private-label/public
npx remotion still src/index.ts Reel out/t9-f300.png --frame=300 \
  --props=projetos/01-private-label/plano.json \
  --public-dir=projetos/01-private-label/public
npx remotion still src/index.ts Feed out/t9-feed120.png --frame=120 \
  --props=projetos/01-private-label/plano.json \
  --public-dir=projetos/01-private-label/public
```

Primeiro a duração, medida e não suposta:

```
cd instagram/remotion
node --experimental-strip-types -e "
const {sondar} = await import('./src/motor/sondar.ts');
const s = await sondar('out/t9-reel.mp4');
console.log(s.largura + 'x' + s.altura, s.duracao, Math.round(s.duracao * 30), 'frames');
"
```
Expected: `1080x1920 23.2 696 frames`.

Depois o sha256 dos dois stills do 9:16 contra os de referência da Tarefa 2:

```
cd instagram/remotion
node -e "const c=require('node:crypto'),f=require('node:fs');const h=n=>c.createHash('sha256').update(f.readFileSync('out/'+n+'.png')).digest('hex');for(const n of ['f120','f300'])console.log(n, h('antes-'+n)===h('t9-'+n)?'IDENTICO':'MUDOU')"
```
Expected: **`f120 IDENTICO` e `f300 IDENTICO`.** A tabela acima diz por que: no 9:16, com
`pista: "tela"`, nada do que esta tarefa mudou alcança o pixel.

**Se der `MUDOU`, o suspeito tem ordem**, e ele é curto porque a tabela já eliminou o resto:

1. **`premountFor={fps}`** — é o único parâmetro novo no caminho da mídia. Se ele mudou o frame, era
   um frame **errado** antes (decodificador não pronto) e o certo é agora. **Abra os dois PNG e decida
   olhando**, não pelo hash.
2. **a `Fonte` polimórfica** — o `<div>` externo dela pinta `COR.terra` e tem `overflow: hidden`, que
   `PecaVideo.tsx` não tinha. No 9:16 o vídeo cobre o quadro inteiro, então não deveria aparecer; se
   aparecer uma borda de 1 px, é arredondamento de `caixa` e o lugar de olhar é `z.video`.
3. **a cadência** — se o `f120` mudou e o `f300` não, é a manchete, e a Tarefa 3 já provou que ela não
   se move. Volte ao Step 9 daquela tarefa.

**E o que tem de ser olhado com o olho**, em recorte ampliado e não na imagem inteira (lição 13):

1. no `t9-f120.png`, a cartela da manchete tem a mesma quebra de linha e o mesmo corpo de
   `antes-f120.png`?
2. no `t9-f300.png`, a legenda está no rodapé e **não** encosta na manchete? (No 9:16 a interseção
   sempre foi 0,00 — este é o controle.)
3. no `t9-feed120.png`, a manchete domina o quadro, ou a legenda continua sendo o maior texto? E a
   legenda **mais estreita** ficou legível, ou passou de duas linhas?

O item 3 é a **D2** e a **D6** virando imagem ao mesmo tempo. Guarde a resposta: é o que o Rafael
precisa ver para decidir.

- [ ] **Step 12: commit**

```bash
git add instagram/remotion/package.json instagram/remotion/package-lock.json \
  instagram/remotion/src instagram/remotion/tests instagram/remotion/scripts/conferir.mjs
git commit -m "$(cat <<'MSG'
Motor: existe cena -- TransitionSeries, Cena, Peca, e a trilha de audio

A legenda e a trilha ficam fora da TransitionSeries: a fala nao reinicia porque a
imagem trocou.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 10: o portão de ritmo, e o portão de preservação que estava órfão

Dois portões, um novo e um que **já existe e nunca foi ligado**. Medido:
`src/verificacao/preservacao.ts` tem 125 linhas, exporta `compararRegiao` e `Laudo`,
`tests/preservacao.test.ts` tem 9 `it` — e `scripts/conferir.mjs:77` lista os portões válidos como
`todos, folha, telefone, determinismo, loop`, **sem `preservacao`**. Peça com recorte de embalagem
sai hoje sem nenhuma prova de que o rótulo não foi alterado.

O portão de ritmo é **puro e roda antes do render**. Cada recusa dele é um render que não
acontece: render de Reel de 23 s leva minutos, o portão leva milissegundos.

**Três correções em relação à versão anterior desta tarefa, e todas vêm de defeito medido:**

1. **O hash do briefing não detecta plano editado à mão.** Ele detecta **briefing alterado depois de
   compilar** — coisa diferente. O portão passa a **recompilar** o briefing e comparar o plano inteiro,
   canonicamente. Isso subsume o hash e cumpre a promessa escrita.
2. **O portão lê disco, e continua puro**, porque o disco entra **injetado**. Sem isso, três recusas da
   spec §3.9.1 (`razaoExibicao` medida, arquivo declarado que não existe, asset sem laudo) não tinham
   como ser implementadas num módulo declarado puro.
3. **A dominância é RECUSA, não aviso** (spec §3.4.2), e `etiqueta` está fora da exigência.

**E duas checagens da spec §3.9.1 que o portão NÃO implementa, cada uma por um motivo:**

- **`laudo.aprovado !== true` em asset de recorte.** Ela não existe porque a spec a substituiu: a prova
  de laudo aprovado é a **presença** do arquivo em `public/assets/`, já que a única porta de entrada
  daquela pasta é `instagram/recorte/publicar.py:82`, que é fail-closed. Um portão que fosse reler o
  laudo seria o **terceiro leitor** do mesmo fato, e cada leitor novo é uma chance nova de divergir. O
  `Laudo` de `src/verificacao/preservacao.ts` **não tem** campo `aprovado` (medido: os campos são
  `pixelsDiferentes`, `maiorDelta`, `total`, `considerados`, `pixelsAlfaPerdido`) — o `aprovado` é do
  laudo Python, em `instagram/assets/embalagem/<slug>.json`.
- **`duracaoPecaFrames ≠ alvo`.** Ela **sai** da lista do portão, e a razão é mecânica: o compilador
  **lança** nesse caso (Tarefa 7), então `plano.json` não é escrito e o portão — que roda sobre o plano
  — nunca veria o caso. A checagem era **morta**. Fica com o compilador, que é o único lugar onde os
  dois números existem ao mesmo tempo, e é a única exceção à regra "o compilador não recusa". E por
  isso `Plano` **não** carrega `alvoS`: um campo que existisse só para uma checagem impossível.

**Files:**
- Create: `instagram/remotion/src/verificacao/ritmo.ts`
- Create: `instagram/remotion/tests/ritmo.test.ts`
- Modify: `instagram/remotion/scripts/conferir.mjs` (dois portões novos, **e a ordem do fluxo**)
- Create: `instagram/remotion/projetos/01-private-label/preservacao.json` (o descritor que o portão 5 exige, para ele ser **exercitado** e não só ligado)

- [ ] **Step 1: escrever o teste que falha**

Criar `instagram/remotion/tests/ritmo.test.ts`:

```ts
import {describe, expect, it} from 'vitest';
import {compilar} from '../src/briefing/compilar';
import {selarPlano} from '../src/briefing/impressao';
import {zBriefing} from '../src/briefing/esquema';
import {portaoDeRitmo} from '../src/verificacao/ritmo';

/**
 * O DISCO DE MENTIRA. O portao e puro: ele nao le arquivo, ele PERGUNTA.
 *
 * Sem isto, as tres recusas que dependem do disco (razaoExibicao medida, arquivo que
 * nao existe, asset sem laudo) nao teriam como ser testadas sem um projeto no disco --
 * e um portao que so da para testar com arquivo real e um portao que ninguem testa.
 */
const DISCO_OK = {
  existe: () => true,
  razaoMedida: () => 0.5625,
};

function plano(patch: Record<string, unknown> = {}) {
  const b = zBriefing.parse({
    _esquema: 'canastra-briefing/1',
    serie: 'avulsa',
    formatos: ['9:16'],
    duracao: {modo: 'somaCenas'},
    cenas: [
      {
        duracaoS: 4,
        fonte: {
          tipo: 'video',
          arquivo: 'pl.mp4',
          razaoExibicao: 0.5625,
          aparaAntesS: 0,
          enquadramento: 'preencher',
          camera: 'parado',
        },
        // `tela` -> cartela: medido, 24,245% de mancha contra um piso de 6,861% no 9:16.
        // Em `topo` a mancha do 1:1 e 3,793% e o portao reprova -- ver o teste da
        // dominancia, abaixo.
        eventos: [{papel: 'manchete', texto: 'CAFE DA SERRA', entradaS: 0, pista: 'tela'}],
      },
    ],
    transicoes: [],
    audio: {locucao: {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 0}, trilha: null},
    gancho: 'g',
    cta: 'c',
    ...patch,
  });
  return {briefing: b, plano: selarPlano(compilar(b), b)};
}

describe('portaoDeRitmo', () => {
  it('a peca coerente passa', () => {
    const {briefing, plano: p} = plano();
    const r = portaoDeRitmo({plano: p, briefing, disco: DISCO_OK});
    expect(r.aprovado).toBe(true);
    expect(r.falhas).toEqual([]);
  });

  it('REPROVA plano editado a mao -- e agora pelo motivo certo', () => {
    // O DEFEITO DO TESTE ANTERIOR: ele mutava o PLANO com spread
    // (`{...p, duracaoFrames: p.duracaoFrames + 30}`) e esperava `plano-incoerente`, que
    // compara `sha256Do(briefing)` com `plano._sha256Briefing`. O spread COPIA o hash
    // intacto, entao os dois continuavam iguais e a falha nao podia disparar pelo motivo
    // certo -- so a `duracao-nao-fecha` disparava.
    //
    // E o defeito CONCEITUAL por baixo: um hash DO BRIEFING nunca detecta edicao NO
    // PLANO. A promessa escrita ("um plano editado a mao seja detectavel") exige comparar
    // o plano com o que o briefing PRODUZ -- e o portao tem os dois em maos.
    const {briefing, plano: p} = plano();
    const editado = {...p, duracaoFrames: p.duracaoFrames + 30};
    const r = portaoDeRitmo({plano: editado, briefing, disco: DISCO_OK});
    expect(r.aprovado).toBe(false);
    const codigos = r.falhas.map((f) => f.codigo);
    expect(codigos).toContain('plano-nao-e-do-briefing');
    // e a mensagem tem que NOMEAR o campo que diverge, senao ela nao ensina nada
    expect(r.falhas.find((f) => f.codigo === 'plano-nao-e-do-briefing')!.mensagem).toMatch(
      /duracaoFrames/,
    );
  });

  it('REPROVA quando o briefing mudou depois de compilar -- o outro caso, e ele e diferente', () => {
    // Aqui o PLANO esta intacto e o BRIEFING mudou. E o caso que o `_sha256Briefing`
    // detecta, e ele continua existindo: `plano-incoerente`.
    const {plano: p} = plano();
    const {briefing: outro} = plano({cta: 'outro cta'});
    const r = portaoDeRitmo({plano: p, briefing: outro, disco: DISCO_OK});
    expect(r.falhas.map((f) => f.codigo)).toContain('plano-incoerente');
  });

  it('o plano selado com o briefing certo NAO dispara nenhum dos dois', () => {
    const {briefing, plano: p} = plano();
    const r = portaoDeRitmo({plano: p, briefing, disco: DISCO_OK});
    expect(r.falhas.map((f) => f.codigo)).not.toContain('plano-incoerente');
    expect(r.falhas.map((f) => f.codigo)).not.toContain('plano-nao-e-do-briefing');
  });

  it('reprova plano cuja duracao nao e a soma das cenas menos as transicoes', () => {
    const {briefing, plano: p} = plano();
    const adulterado = {...p, cenas: [{...p.cenas[0], duracaoFrames: 999}]};
    const r = portaoDeRitmo({plano: adulterado, briefing, disco: DISCO_OK});
    expect(r.falhas.map((f) => f.codigo)).toContain('duracao-nao-fecha');
  });

  it('reprova evento mais curto que DURACAO_MINIMA, que sao 36 frames a 30 fps', () => {
    // 12 + 12 + 12. A constante JA EXISTE exportada em `movimento.ts:122` com esta
    // formula, e `tests/textotela.test.ts:81` asserta a igualdade -- o portao IMPORTA a
    // cadencia, nao recalcula o numero.
    const {briefing, plano: p} = plano({
      cenas: [
        {
          duracaoS: 4,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [
            {papel: 'manchete', texto: 'CAFE', entradaS: 0, duracaoS: 0.5, pista: 'tela'},
          ],
        },
      ],
    });
    const r = portaoDeRitmo({plano: p, briefing, disco: DISCO_OK});
    expect(r.falhas.some((f) => f.codigo === 'abaixo-do-piso')).toBe(true);
    expect(r.falhas.find((f) => f.codigo === 'abaixo-do-piso')!.mensagem).toMatch(/36/);
  });

  it('reprova peca SEM locucao e SEM trilha: perde elegibilidade', () => {
    // 05-formatos.md §3, [oficial]: Reel sem audio perde entrega a nao-seguidor.
    // `refinar()` ja pega isso no briefing; o portao repete NO PLANO, que e o arquivo que
    // renderiza.
    const {briefing, plano: p} = plano({audio: {locucao: null, trilha: null}});
    const r = portaoDeRitmo({plano: p, briefing, disco: DISCO_OK});
    expect(r.falhas.some((f) => f.codigo === 'peca-muda')).toBe(true);
  });

  it('com trilha declarada, a peca de foto parada passa', () => {
    const {briefing, plano: p} = plano({
      cenas: [
        {
          duracaoS: 4,
          fonte: {
            tipo: 'foto',
            arquivo: 'cafezal.jpg',
            razaoExibicao: 4 / 3,
            registro: 'moldura',
            enquadramento: {tipo: 'recorte', x: 0.25, y: 0, largura: 0.5, altura: 1},
            camera: 'pushLento',
          },
          eventos: [
            {papel: 'manchete', texto: 'CAFE DA SERRA', entradaS: 0, pista: 'principal'},
          ],
        },
      ],
      audio: {
        locucao: null,
        trilha: {
          arquivo: 'ambiente.wav',
          ganhoDb: -18,
          aparaAntesS: 0,
          loopar: true,
          fadeEntradaS: 0.5,
          fadeSaidaS: 0.8,
        },
      },
    });
    const r = portaoDeRitmo({
      plano: p,
      briefing,
      disco: {existe: () => true, razaoMedida: () => 4 / 3},
    });
    expect(r.aprovado).toBe(true);
  });

  it('REPROVA dominancia abaixo do piso -- e isso e recusa, nao aviso', () => {
    // A versao anterior deste portao AVISAVA. A spec §3.4.2 poe a dominancia na lista de
    // RECUSAS, e `proibicoes.md:19` ("um elemento dominante por cena") fica sem quem a
    // cumpra se ela for aviso.
    //
    // Medido: com a manchete em `pista: 'topo'` e fonte retrato, o 1:1 da 48 px de corpo e
    // 3,793% de mancha contra um piso de 6,925%. Consequencia dita em voz alta: LIGADO
    // HOJE, o piso reprova o 01-private-label no 1:1 se ele declarar `topo` -- e e por
    // isso que o briefing dele declara `tela`.
    const {briefing, plano: p} = plano({
      formatos: ['9:16', '1:1'],
      cenas: [
        {
          duracaoS: 4,
          fonte: {
            tipo: 'video',
            arquivo: 'pl.mp4',
            razaoExibicao: 0.5625,
            aparaAntesS: 0,
            enquadramento: 'preencher',
            camera: 'parado',
          },
          eventos: [
            {papel: 'manchete', texto: 'SUA PRÓPRIA MARCA DE CAFÉ', entradaS: 0, pista: 'topo'},
          ],
        },
      ],
    });
    const r = portaoDeRitmo({plano: p, briefing, disco: DISCO_OK});
    const f = r.falhas.find((x) => x.codigo === 'sem-dominante');
    expect(f).toBeDefined();
    expect(f!.mensagem).toMatch(/1:1/);
    expect(f!.mensagem).toMatch(/%/);
  });

  it('cena com SO etiqueta nao precisa de dominante: carimbo nao domina', () => {
    // Medido: `MEDEIROS 1250 M` em `dado` da 84 px de corpo e 2,940% de mancha no 9:16,
    // abaixo do piso -- e isso esta CERTO. Exigir dominancia de um carimbo mataria a cena
    // 1 da peca de prova, que existe para exercitar exatamente esse caso.
    const {briefing, plano: p} = plano({
      cenas: [
        {
          duracaoS: 4,
          fonte: {
            tipo: 'video',
            arquivo: 'pl.mp4',
            razaoExibicao: 0.5625,
            aparaAntesS: 0,
            enquadramento: 'preencher',
            camera: 'parado',
          },
          eventos: [{papel: 'etiqueta', texto: 'MEDEIROS 1250 M', entradaS: 0, pista: 'topo'}],
        },
      ],
    });
    const r = portaoDeRitmo({plano: p, briefing, disco: DISCO_OK});
    expect(r.falhas.map((f) => f.codigo)).not.toContain('sem-dominante');
  });

  it('REPROVA razaoExibicao declarada que nao bate com a medida, tolerancia 0,005', () => {
    // O campo existe para ser CONFERIDO, nao para ser acreditado. E o dedo ja errou: o
    // prototipo `out/_spec-briefing/b-jornada-foto.json` declara `1.3333` para
    // `IMG_1421.JPG` e `IMG_1424.JPG`, e os dois sao `Orientation 6`, ou seja 0,75
    // (medido em 01/10/2026 com ffprobe nos dois arquivos).
    const {briefing, plano: p} = plano();
    const r = portaoDeRitmo({
      plano: p,
      briefing,
      disco: {existe: () => true, razaoMedida: () => 1.7778},
    });
    const f = r.falhas.find((x) => x.codigo === 'razao-nao-bate');
    expect(f).toBeDefined();
    expect(f!.mensagem).toMatch(/0,5625|0\.5625/);
    expect(f!.mensagem).toMatch(/1,7778|1\.7778/);
    // e dentro da tolerancia PASSA: 0,5625 contra 0,5640 sao 0,0015
    expect(
      portaoDeRitmo({plano: p, briefing, disco: {existe: () => true, razaoMedida: () => 0.564}})
        .falhas.map((x) => x.codigo),
    ).not.toContain('razao-nao-bate');
  });

  it('REPROVA arquivo declarado que nao existe em public/', () => {
    const {briefing, plano: p} = plano();
    const r = portaoDeRitmo({
      plano: p,
      briefing,
      disco: {existe: () => false, razaoMedida: () => 0.5625},
    });
    const f = r.falhas.find((x) => x.codigo === 'arquivo-ausente');
    expect(f).toBeDefined();
    expect(f!.mensagem).toMatch(/pl\.mp4/);
  });

  it('REPROVA asset de recorte que nao esta em public/assets/ -- a presenca E o laudo', () => {
    // A spec §3.9.1: existir em `public/assets/` ja e o certificado, porque a unica porta
    // de entrada daquela pasta e `instagram/recorte/publicar.py:82`, que so copia o PNG
    // cujo laudo irmao traz `aprovado is True` -- fail-closed. E por isso que os tres PNG
    // que estao la NAO tem `.json` ao lado (medido). Um portao que fosse reler o laudo
    // seria o terceiro leitor do mesmo fato.
    const {briefing, plano: p} = plano({
      assets: [{arquivo: 'suave-250g.png', tipo: 'recorte-embalagem', laudoExigido: true}],
    });
    const r = portaoDeRitmo({
      plano: p,
      briefing,
      disco: {
        existe: (rel: string) => !rel.includes('assets/'),
        razaoMedida: () => 0.5625,
      },
    });
    const f = r.falhas.find((x) => x.codigo === 'asset-sem-laudo');
    expect(f).toBeDefined();
    expect(f!.mensagem).toMatch(/publicar\.py/);
  });

  it('REPROVA bloco de legenda grudado em 0 por mais de 10 frames', () => {
    // `LEGENDA.duracaoMinFrames` = 10 (medido em `tokens.ts`): abaixo disso e
    // arredondamento de Whisper, acima e ancora errada. O caso real do
    // 01-private-label tem recuo de 14 -- ver a Tarefa 7, Step 2c.
    const {briefing, plano: p} = plano({
      legenda: {arquivo: 'transcricao.json', relogio: 'fonte', ancora: {tipo: 'segundo', valorS: 1}},
    });
    const comLegenda = {
      ...p,
      legenda: {
        blocos: [{texto: 'um', inicioFrame: 0, fimFrame: 20}],
        deslocamentoFrames: -30,
        grudadosEmZero: 1,
        maiorRecuoFrames: 14,
        descartadosAntesDoInicio: 1,
        descartadosDepoisDoFim: 0,
      },
    };
    const r = portaoDeRitmo({plano: comLegenda, briefing, disco: DISCO_OK});
    const f = r.falhas.find((x) => x.codigo === 'legenda-recuada');
    expect(f).toBeDefined();
    expect(f!.mensagem).toMatch(/14/);
    expect(f!.mensagem).toMatch(/10/);
  });

  it('AVISA sobre licenca ligada, sem reprovar', () => {
    // O campo registra a DECISAO. Reprovar mataria briefing legitimo; ficar calado
    // faria a decisao desaparecer. Entao avisa, nomeando a linha da proibicao.
    const {briefing, plano: p} = plano({
      licencas: {
        flashNoCorte: true,
        justificativa: 'teste explicito de licenca ligada neste portao',
      },
    });
    const r = portaoDeRitmo({plano: p, briefing, disco: DISCO_OK});
    expect(r.aprovado).toBe(true);
    expect(r.avisos.some((a) => a.includes('flashNoCorte'))).toBe(true);
    expect(r.avisos.some((a) => a.includes('nenhuma tecnica de licenca'))).toBe(true);
  });

  it('SEM disco, as tres checagens de arquivo saem como AVISO de nao-conferido', () => {
    // O portao continua rodavel sem disco -- num teste, num CI sem `public/`. O que ele
    // NAO faz e passar em silencio: "nao conferido" e um aviso nomeado, porque uma
    // checagem que desaparece sem ruido e pior que uma que falha.
    const {briefing, plano: p} = plano();
    const r = portaoDeRitmo({plano: p, briefing});
    expect(r.aprovado).toBe(true);
    expect(r.avisos.some((a) => a.includes('nao conferido'))).toBe(true);
  });

  it('reprova dado com carimbo regulatorio mesmo se alguem editou o plano', () => {
    // `refinar()` ja pega isso no briefing. O portao repete a checagem NO PLANO, que e o
    // arquivo que renderiza: e a unica leitura que corresponde ao pixel.
    const {briefing, plano: p} = plano();
    const adulterado = {
      ...p,
      cenas: [
        {
          ...p.cenas[0],
          eventos: [
            {...p.cenas[0].eventos[0], papel: 'dado' as const, texto: 'F:23.2025'},
          ],
        },
      ],
    };
    const r = portaoDeRitmo({plano: adulterado, briefing, disco: DISCO_OK});
    expect(r.falhas.some((f) => f.codigo === 'dado-regulatorio')).toBe(true);
  });

  it('reprova duas camadas na mesma pista ao mesmo tempo, no PLANO', () => {
    const {briefing, plano: p} = plano();
    const e = p.cenas[0].eventos[0];
    const adulterado = {
      ...p,
      cenas: [{...p.cenas[0], eventos: [e, {...e, texto: 'OUTRO'}]}],
    };
    const r = portaoDeRitmo({plano: adulterado, briefing, disco: DISCO_OK});
    expect(r.falhas.some((f) => f.codigo === 'pista-ocupada')).toBe(true);
  });
});
```

- [ ] **Step 2: rodar o teste e conferir que falha**

Run: `cd instagram/remotion && npx vitest run tests/ritmo.test.ts`
Expected: FALHA — `Failed to resolve import "../src/verificacao/ritmo"`.
- [ ] **Step 3: criar `src/verificacao/ritmo.ts`**

```ts
// O PORTAO DE RITMO. Puro, e roda ANTES do render.
//
// POR QUE ANTES
//
// Cada recusa aqui e um render que nao acontece. Render de Reel de 23 s leva minutos;
// este portao leva milissegundos. E a "erro e evidencia barata" do CLAUDE.md aplicada ao
// motor.
//
// POR QUE ELE REPETE CHECAGENS DE `refinar()`
//
// `refinar()` le o BRIEFING; este portao le o PLANO. O plano e o arquivo que renderiza, e
// a unica leitura que corresponde ao pixel.
//
// E COMO ELE DETECTA PLANO EDITADO A MAO -- o que o hash sozinho NAO fazia
//
// A versao anterior comparava `sha256Do(briefing)` com `plano._sha256Briefing`. Isso
// detecta BRIEFING ALTERADO DEPOIS DE COMPILAR, que e outra coisa: um plano editado a mao
// mantem o hash intacto e passa. A promessa escrita ("um plano editado a mao seja
// detectavel") exige comparar o plano com o que o briefing PRODUZ -- e o portao tem os
// dois em maos, entao ele RECOMPILA e compara canonicamente. Custa milissegundos e fecha
// o buraco inteiro, incluindo campos que ninguem pensou em checar.
//
// Os dois codigos continuam separados de proposito, porque as acoes sao diferentes:
//   plano-nao-e-do-briefing .. recompile (`node scripts/compilar.mjs`)
//   plano-incoerente ......... decida qual dos dois arquivos esta certo
//
// COMO ELE LE DISCO SEM DEIXAR DE SER PURO
//
// Ele NAO le: ele PERGUNTA. `disco` e injetado por quem tem I/O (`scripts/conferir.mjs`).
// Tres recusas da spec §3.9.1 dependem do disco -- razaoExibicao medida, arquivo que nao
// existe, asset sem laudo -- e sem injecao elas nao teriam como existir num modulo puro.
// Sem `disco`, as tres saem como AVISO de "nao conferido", nunca em silencio.
//
// AVISO NAO E FALHA, E A DIFERENCA E DELIBERADA
//
// FALHA: a peca esta errada de um jeito que nenhum olho conserta depois -- duracao que
// nao fecha, elemento abaixo do piso de leitura, peca muda, carimbo regulatorio
// inventado, duas camadas no mesmo lugar, nada dominando o quadro, razao declarada que
// nao bate com a medida, arquivo que nao existe.
// AVISO: a peca esta legitima e alguem precisa SABER -- licenca ligada, checagem de disco
// nao conferida, exigePreservacao pedindo o portao 5.

import {compilar, type Plano} from '../briefing/compilar';
import type {Palavra} from '../legenda/agrupar';
import {canonico, sha256Do} from '../briefing/impressao';
import type {Briefing, Licenca} from '../briefing/esquema';
import {LICENCAS} from '../briefing/esquema';
import {LEGENDA} from '../identidade/tokens';
import {cadencia} from '../motor/cadencia';
import {CONFLITO_DE_PISTA} from '../motor/pista';
import {SUB} from '../motor/pasta-publica';

export type FalhaDeRitmo = {codigo: string; onde: string; mensagem: string};
export type Veredito = {aprovado: boolean; falhas: FalhaDeRitmo[]; avisos: string[]};

/**
 * O disco, injetado. Quem tem I/O responde; o portao so pergunta.
 *
 * `existe(relativo)` recebe caminho relativo a `projetos/<p>/public/`, que e a raiz que
 * o Remotion serve -- a mesma convencao de `staticFile()`.
 * `razaoMedida(relativo)` devolve `sondar().razao`, ou `null` se nao der para medir.
 */
export type Disco = {
  existe: (relativoAPublic: string) => boolean;
  razaoMedida: (relativoAPublic: string) => number | null;
};

const REGULATORIO = /^\s*F\s*[:.]|\bVAL\b|\bVALIDADE\b|\bLOTE\b|\bFAB\b/i;

/** Tolerancia da conferencia de razao de exibicao. Spec §3.3.3. */
export const TOLERANCIA_DE_RAZAO = 0.005;

/** Papeis de que se EXIGE dominancia. `etiqueta` fora: carimbo nao domina. */
const PAPEIS_QUE_DOMINAM = new Set(['manchete', 'dado']);

export function portaoDeRitmo({
  plano,
  briefing,
  palavras,
  disco,
}: {
  plano: Plano;
  /** o briefing que deveria ter gerado este plano */
  briefing: Briefing;
  /**
   * A transcricao, para a RECOMPILACAO. Obrigatoria quando o plano tem legenda: sem ela,
   * recompilar compararia um plano sem legenda com um plano com legenda, e a divergencia
   * seria ficcao. Quem le o arquivo e `scripts/conferir.mjs`.
   */
  palavras?: Palavra[];
  /** ausente = as tres checagens de arquivo saem como aviso de nao-conferido */
  disco?: Disco;
}): Veredito {
  const falhas: FalhaDeRitmo[] = [];
  const avisos: string[] = [];
  const c = cadencia(plano.fps);

  // ---------------------------------------------------------------- procedencia
  const hash = sha256Do(briefing);
  if (plano._sha256Briefing !== hash) {
    falhas.push({
      codigo: 'plano-incoerente',
      onde: '_sha256Briefing',
      mensagem:
        `o plano diz ter saido de um briefing de hash ${plano._sha256Briefing.slice(0, 12) || '(vazio)'} ` +
        `e o briefing atual tem ${hash.slice(0, 12)}. O BRIEFING mudou depois de ` +
        'compilar, ou o plano veio de outro projeto. Decida qual dos dois arquivos esta ' +
        'certo e recompile: `node scripts/compilar.mjs --projeto=<dir>`.',
    });
  }

  // E A CHECAGEM QUE O HASH NAO FAZIA: o plano E o que este briefing produz?
  //
  // Recompilar custa milissegundos e pega TODA edicao manual do plano, incluindo campo
  // que ninguem pensou em checar. `compilar()` e deterministico (o teste de `totalFixo`
  // prova), entao duas compilacoes do mesmo briefing dao a mesma estrutura.
  if (plano.legenda && !palavras) {
    throw new Error(
      'portaoDeRitmo: a peca declara legenda e as palavras nao foram passadas. Chame com ' +
        '`{plano, briefing, palavras}` -- `scripts/conferir.mjs` le a transcricao e as ' +
        'injeta. Lancar aqui e melhor que comparar metade: uma divergencia calculada sem a ' +
        'legenda apontaria campos que estao certos.',
    );
  }
  const recompilado = compilar(briefing, palavras ? {palavras} : {});
  const camposDivergentes = divergencias(recompilado, plano);
  if (camposDivergentes.length > 0) {
    falhas.push({
      codigo: 'plano-nao-e-do-briefing',
      onde: camposDivergentes.slice(0, 5).join(', '),
      mensagem:
        `recompilando o briefing, ${camposDivergentes.length} campo(s) do plano.json nao ` +
        `batem: ${camposDivergentes.slice(0, 5).join(', ')}` +
        (camposDivergentes.length > 5 ? ` (e mais ${camposDivergentes.length - 5})` : '') +
        '. plano.json e ARTEFATO GERADO e nao se edita -- rode ' +
        '`node scripts/compilar.mjs --projeto=<dir>` outra vez. Se voce precisa que o ' +
        'numero mude, mude o BRIEFING: e ele que e a verdade humana.',
    });
  }

  // ---------------------------------------------------------------- aritmetica
  const somaCenas = plano.cenas.reduce((s, x) => s + x.duracaoFrames, 0);
  const gasto = plano.transicoes.reduce((s, x) => s + x.duracaoFrames, 0);
  if (somaCenas - gasto !== plano.duracaoFrames) {
    falhas.push({
      codigo: 'duracao-nao-fecha',
      onde: 'duracaoFrames',
      mensagem:
        `as cenas somam ${somaCenas} frames, as transicoes gastam ${gasto}, logo a ` +
        `peca teria ${somaCenas - gasto} frames -- e o plano declara ` +
        `${plano.duracaoFrames}. Durante a transicao as duas cenas sao ` +
        'renderizadas, entao ela GASTA tempo em vez de somar.',
    });
  }

  // ---------------------------------------------------------------- audio
  if (plano.audio.locucao === null && plano.audio.trilha === null) {
    falhas.push({
      codigo: 'peca-muda',
      onde: 'audio',
      mensagem:
        'audio.locucao e audio.trilha sao os dois null: a peca sai MUDA. ' +
        '05-formatos.md §3, [oficial]: Reel sem audio perde elegibilidade para ' +
        'nao-seguidor. "Mudo" no catalogo significa SEM LOCUCAO, nunca sem faixa.',
    });
  }

  // ---------------------------------------------------------------- legenda
  if (plano.legenda && plano.legenda.maiorRecuoFrames > LEGENDA.duracaoMinFrames) {
    falhas.push({
      codigo: 'legenda-recuada',
      onde: 'legenda.ancora',
      mensagem:
        `${plano.legenda.grudadosEmZero} bloco(s) de legenda foram grudados no frame 0, ` +
        `com recuo de ate ${plano.legenda.maiorRecuoFrames} frames -- o piso e ` +
        `${LEGENDA.duracaoMinFrames} (LEGENDA.duracaoMinFrames). Abaixo do piso e ` +
        'arredondamento de Whisper; acima, a ancora esta errada ou a transcricao nao ' +
        'corresponde ao audio desta peca. Meca de onde a fala comeca antes de mexer na ' +
        'ancora: `ffmpeg -i <wav> -af silencedetect=noise=-40dB:d=0.2 -f null -`.',
    });
  }
  if (plano.legenda && plano.legenda.descartadosDepoisDoFim > 0) {
    falhas.push({
      codigo: 'legenda-cortada',
      onde: 'legenda',
      mensagem:
        `${plano.legenda.descartadosDepoisDoFim} bloco(s) de legenda comecam DEPOIS do ` +
        `fim da peca (${plano.duracaoFrames} frames). A peca esta mais curta que a fala: ` +
        'ou `duracao.alvoS` em totalFixo comeu o fim, ou a transcricao e de outro audio.',
    });
  }

  // ---------------------------------------------------------------- disco
  if (!disco) {
    avisos.push(
      'as tres checagens de arquivo NAO FORAM CONFERIDAS nesta execucao (razaoExibicao ' +
        'medida, existencia dos arquivos e dos assets): `portaoDeRitmo` foi chamado sem ' +
        '`disco`. Rode pelo `scripts/conferir.mjs`, que injeta o disco.',
    );
  } else {
    for (const [i, cena] of plano.cenas.entries()) {
      for (const f of achatarFontes(cena.fonte)) {
        if (f.tipo !== 'video' && f.tipo !== 'foto') continue;
        const rel = `${SUB.fonte}/${f.arquivo}`;
        if (!disco.existe(rel)) {
          falhas.push({
            codigo: 'arquivo-ausente',
            onde: `cenas[${i}].fonte.arquivo`,
            mensagem:
              `"${f.arquivo}" nao existe em public/${SUB.fonte}/. O campo e o NOME do ` +
              'arquivo dentro daquela subpasta, sem caminho -- e o render falharia com ' +
              'um 404 de asset no meio de minutos de trabalho.',
          });
          continue;
        }
        const medida = disco.razaoMedida(rel);
        if (medida === null) {
          avisos.push(
            `a razao de "${f.arquivo}" nao foi conferida: sondar() nao conseguiu medir.`,
          );
          continue;
        }
        if (Math.abs(medida - f.razaoExibicao) > TOLERANCIA_DE_RAZAO) {
          falhas.push({
            codigo: 'razao-nao-bate',
            onde: `cenas[${i}].fonte.razaoExibicao`,
            mensagem:
              `o briefing declara razaoExibicao ${f.razaoExibicao} para "${f.arquivo}" e ` +
              `sondar() mede ${medida.toFixed(6)} (tolerancia ${TOLERANCIA_DE_RAZAO}). O ` +
              'campo existe para ser CONFERIDO, nao acreditado: o metadado de rotacao ' +
              'tem dois nomes (displaymatrix no video, EXIF Orientation no JPEG) e ler ' +
              'width/height sem os dois e o defeito padrao deste repositorio. Rode a ' +
              'medicao e copie o numero dela.',
          });
        }
      }
    }

    for (const [i, a] of plano.assets.entries()) {
      const rel = `${SUB.assets}/${a.arquivo}`;
      if (!disco.existe(rel)) {
        falhas.push({
          codigo: 'asset-sem-laudo',
          onde: `assets[${i}].arquivo`,
          mensagem:
            `"${a.arquivo}" nao esta em public/${SUB.assets}/. A PRESENCA do arquivo ali e ` +
            'o certificado de laudo aprovado, porque a unica porta de entrada daquela ' +
            'pasta e instagram/recorte/publicar.py:82, que so copia o PNG cujo laudo ' +
            'irmao traz `aprovado is True` -- fail-closed. O laudo NAO e copiado para ' +
            'dentro do briefing de proposito: um humano podendo digitar aprovado:true a ' +
            'mao transformaria aquele portao em decoracao.',
        });
      }
    }
  }

  // ---------------------------------------------------------------- por cena
  plano.cenas.forEach((cena, i) => {
    if (cena.eventos.length === 0 && plano.legenda === null && !plano.licencas.aceitaTempoMorto) {
      falhas.push({
        codigo: 'tempo-morto',
        onde: `cenas[${i}]`,
        mensagem:
          `${cena.duracaoFrames} frames sem nenhuma camada alem da fonte. ` +
          'proibicoes.md:11-12 proibe tempo morto.',
      });
    }

    cena.eventos.forEach((e, j) => {
      if (e.duracaoFrames < c.duracaoMinima) {
        falhas.push({
          codigo: 'abaixo-do-piso',
          onde: `cenas[${i}].eventos[${j}]`,
          mensagem:
            `"${e.texto}" dura ${e.duracaoFrames} frames e o piso e ` +
            `${c.duracaoMinima} (entrada ${c.entrada} + holdFinal ${c.holdFinal} + ` +
            `saida ${c.entrada}, a ${plano.fps} fps). Abaixo disso as pontas ` +
            'comprimem e o elemento aparece e sai no mesmo piscar.',
        });
      }

      if (e.inicioFrames + e.duracaoFrames > cena.duracaoFrames) {
        falhas.push({
          codigo: 'evento-estoura-cena',
          onde: `cenas[${i}].eventos[${j}]`,
          mensagem:
            `"${e.texto}" entra no frame ${e.inicioFrames} e ocupa ` +
            `${e.duracaoFrames}, terminando em ${e.inicioFrames + e.duracaoFrames}; ` +
            `a cena tem ${cena.duracaoFrames}. A ultima palavra perderia a saida.`,
        });
      }

      if (e.papel === 'dado' && REGULATORIO.test(e.texto)) {
        falhas.push({
          codigo: 'dado-regulatorio',
          onde: `cenas[${i}].eventos[${j}]`,
          mensagem:
            `"${e.texto}" parece lote, fabricacao ou validade (licao 22 do ` +
            'CLAUDE.md). Informacao regulatoria falsa nao entra em peca de ' +
            'e-commerce: ou sai do enquadramento, ou entra por composicao da foto ' +
            'real.',
        });
      }

      // `papel` do tipo nao aceita 'legenda', mas o plano chega como JSON: um
      // arquivo escrito a mao pode trazer qualquer string.
      if ((e.papel as string) === 'legenda') {
        falhas.push({
          codigo: 'legenda-como-evento',
          onde: `cenas[${i}].eventos[${j}]`,
          mensagem:
            'a legenda NAO e evento de cena: ela e camada da PECA, e vive no campo ' +
            '`legenda` do briefing. Dentro de uma cena, na janela de crossfade duas ' +
            'legendas com textos diferentes ficariam no ar ao mesmo tempo.',
        });
      }
    });

    // O PISO DE DOMINANCIA, e ele e RECUSA (spec §3.4.2).
    //
    // A regra e por CENA e por FORMATO: ao menos um evento candidato tem que dominar.
    // `etiqueta` nao e candidata -- carimbo nao e o elemento dominante --, entao cena
    // que so tem etiqueta nao entra na exigencia.
    const candidatos = cena.eventos
      .map((e, j) => ({e, j}))
      .filter(({e}) => PAPEIS_QUE_DOMINAM.has(e.papel));
    if (candidatos.length > 0) {
      for (const formato of plano.formatos) {
        const algumDomina = candidatos.some(({j}) => {
          const d = plano.diagnostico.eventos.find((x) => x.cena === i && x.indice === j);
          return d?.porFormato[formato]?.domina === true;
        });
        if (algumDomina) continue;
        const detalhe = candidatos
          .map(({j}) => {
            const d = plano.diagnostico.eventos.find((x) => x.cena === i && x.indice === j);
            return d ? `  ${d.texto}: ${d.porFormato[formato]?.porque ?? 'sem diagnostico'}` : '';
          })
          .filter((x) => x.length > 0)
          .join('\n');
        falhas.push({
          codigo: 'sem-dominante',
          onde: `cenas[${i}] em ${formato}`,
          mensagem:
            `nenhum evento desta cena domina o quadro em ${formato}. ` +
            'proibicoes.md:19 pede um elemento dominante por cena, e o defeito medido do ' +
            'motor antigo era o contrario: a manchete era o MENOR texto do quadro (48 px ' +
            `no 1:1 contra 78 px de legenda). As contas:\n${detalhe}\n` +
            'Saidas: declare `pista: "tela"` (cartela domina em todo formato), encurte o ' +
            'texto, ou tire este formato de `formatos`.',
        });
      }
    }

    for (let a = 0; a < cena.eventos.length; a++) {
      for (let b = a + 1; b < cena.eventos.length; b++) {
        const x = cena.eventos[a];
        const y = cena.eventos[b];
        const seCruzam =
          x.inicioFrames < y.inicioFrames + y.duracaoFrames &&
          y.inicioFrames < x.inicioFrames + x.duracaoFrames;
        const conflitam =
          CONFLITO_DE_PISTA[x.pista].includes(y.pista) ||
          CONFLITO_DE_PISTA[y.pista].includes(x.pista);
        if (seCruzam && conflitam) {
          falhas.push({
            codigo: 'pista-ocupada',
            onde: `cenas[${i}].eventos`,
            mensagem:
              `"${x.texto}" (pista ${x.pista}) e "${y.texto}" (pista ${y.pista}) ` +
              'ocupam pistas que conflitam ao mesmo tempo.',
          });
        }
      }
    }
  });

  // ---------------------------------------------------------------- licencas
  for (const chave of LICENCAS) {
    if (!plano.licencas[chave]) continue;
    if (plano.licencas.justificativa.trim().length < 12) {
      falhas.push({
        codigo: 'licenca-sem-justificativa',
        onde: `licencas.${chave}`,
        mensagem: `a licenca "${chave}" esta ligada sem justificativa de 12 caracteres.`,
      });
      continue;
    }
    avisos.push(
      `licenca "${chave}" LIGADA: "${plano.licencas.justificativa.trim()}". E ` +
        'nenhuma tecnica de licenca esta implementada nesta versao -- o campo ' +
        'registra a decisao, o codigo vem depois dela.',
    );
  }

  if (plano.exigePreservacao) {
    avisos.push(
      `a peca declara ${plano.assets.length} recorte(s) de embalagem: rode tambem ` +
        '`node scripts/conferir.mjs --portao=preservacao`, que compara pixel por pixel a ' +
        'regiao da embalagem entre o recorte de origem e o frame renderizado.',
    );
  }

  return {aprovado: falhas.length === 0, falhas, avisos};
}

/**
 * Os campos em que dois planos divergem, em notacao de caminho.
 *
 * Compara pela forma CANONICA (`briefing/impressao.ts`), entao ordem de chave nao conta.
 * `_sha256Briefing` fica fora: ele e selado depois de compilar, e a divergencia dele tem
 * codigo proprio.
 */
function divergencias(esperado: Plano, recebido: Plano): string[] {
  const fora = new Set(['_sha256Briefing']);
  const achados: string[] = [];
  const anda = (a: unknown, b: unknown, caminho: string) => {
    if (canonico(a) === canonico(b)) return;
    if (
      typeof a !== 'object' || a === null ||
      typeof b !== 'object' || b === null ||
      Array.isArray(a) !== Array.isArray(b)
    ) {
      achados.push(caminho || '(raiz)');
      return;
    }
    const chaves = new Set([...Object.keys(a), ...Object.keys(b)]);
    for (const k of chaves) {
      if (caminho === '' && fora.has(k)) continue;
      anda(
        (a as Record<string, unknown>)[k],
        (b as Record<string, unknown>)[k],
        caminho ? `${caminho}.${k}` : k,
      );
    }
  };
  anda(esperado, recebido, '');
  return achados;
}

/** Todas as fontes de uma cena, achatando a grade (que tem 2 a 4 celulas). */
function achatarFontes(f: Plano['cenas'][number]['fonte']): Plano['cenas'][number]['fonte'][] {
  return f.tipo === 'grade' ? f.celulas : [f];
}
```

**O teste da legenda do Step 1 passa `palavras` junto**, porque ele monta um plano com legenda à mão.
Sem isso, `portaoDeRitmo` lança — e lançar é o comportamento certo: comparar um plano com legenda contra
uma recompilação sem legenda apontaria como divergentes campos que estão corretos.

- [ ] **Step 4: rodar o teste e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/ritmo.test.ts`
Expected: `Tests 18 passed (18)`.
- [ ] **Step 5: ligar os dois portões em `scripts/conferir.mjs`, e CONSERTAR A ORDEM DO FLUXO**

**A ordem é o defeito, e ela é medida.** A versão anterior mandava inserir o portão de ritmo *"antes do
portão 1"*. Mas em `scripts/conferir.mjs`, **antes de qualquer portão**, rodam duas coisas:

- **linhas 114–125**: o laço `for (const [rotulo, p] of [['a peca renderizada', video], ['o props.json',
  props], ['a pasta publica', publicDir]]) if (!fs.existsSync(p)) throw` — ele **lança** se
  `saida/<composicao>.mp4` não existir;
- **linha 130**: `const fonte = await sondar(video)`, que lê o MP4.

Ou seja `--portao=ritmo` **não roda antes do render** — e isso destrói a premissa inteira do portão
(*"roda ANTES do render; cada recusa dele é um render que não acontece"*). No `01-private-label` funciona
por acidente, porque o MP4 antigo está lá. Num projeto novo, como o `02-foto-parada` da Tarefa 13, o
comando falha com `a peca renderizada nao existe`.

O conserto tem quatro partes.

**1. Registrar o resolvedor de `.ts`, antes do primeiro import dinâmico.**

No topo de `scripts/conferir.mjs`, junto dos imports:

```js
import {register} from 'node:module';
```

e, dentro de `conferir()`, **antes** do primeiro `await import('../src/...')`:

```js
  // OS MODULOS NOVOS IMPORTAM `src/` DE VERDADE, e o resolvedor cru do Node nao segue a
  // convencao `moduleResolution: "bundler"` do projeto (import sem extensao). Medido:
  //   node --experimental-strip-types -e "await import('./src/legenda/agrupar.ts')"
  //   -> ERR_MODULE_NOT_FOUND: Cannot find module '.../src/identidade/tokens'
  //
  // Este script sobrevivia sem o gancho por ACIDENTE: `sondar`, `folha`, `telefone` e
  // `determinismo` importam apenas builtins de `node:` e `pngjs`. `esquema.ts` e
  // `ritmo.ts` importam meio `src/`. O unico lugar que registrava o gancho era
  // `scripts/gerar-props.mjs:173`, e a Tarefa 12 apaga aquele arquivo.
  register('./_resolver-ts.mjs', import.meta.url);
```

**2. Mover a exigência de arquivo para DEPOIS do portão 0, e exigir só o que cada portão usa.**

Substituir o laço das linhas 114–125 por:

```js
  // O QUE CADA PORTAO EXIGE, e nada além disso.
  //
  // O portao 0 (ritmo) le `briefing.json` e `plano.json` e RODA ANTES DO RENDER -- e a
  // razao de ele existir. Exigir o MP4 antes dele, como este script fazia ate 01/10/2026,
  // tornava impossivel usa-lo num projeto novo: `--portao=ritmo` falhava com "a peca
  // renderizada nao existe", e a premissa inteira do portao morria.
  //
  // Os portoes 1 a 5 leem a PECA RENDERIZADA, e para eles a exigencia continua.
  const exigir = (rotulo, p) => {
    if (!fs.existsSync(p)) {
      throw new Error(
        `${rotulo} nao existe: ${p}. Rode ` +
          '`node scripts/compilar.mjs --projeto=<dir>` e depois o render, antes dos ' +
          'portoes de imagem.',
      );
    }
  };

  const soRitmo = a.portao === 'ritmo';
  exigir('o plano.json', props);
  exigir('a pasta publica', publicDir);
  if (!soRitmo) exigir('a peca renderizada', video);
```

E o `sondar(video)` da linha 130, com o bloco `== peca ==` que ele alimenta, passa a ser condicional:

```js
  const roda = (nome) => a.portao === 'todos' || a.portao === nome;
  const falhas = [];

  let fonte = null;
  if (!soRitmo) {
    fonte = await sondar(video);
    console.log(`\n== peca ==`);
    console.log(`  ${video}`);
    // `sondar()` devolve `null` em duracao/fps para imagem parada desde 01/10/2026
    // (Tarefa 4A). Aqui o alvo e sempre um MP4, mas `null.toFixed` seria um TypeError a
    // esperar o dia em que alguem aponte o portao para um still.
    if (fonte.duracao === null || fonte.fps === null) {
      throw new Error(
        `${video} nao e um video: sondar() diz imagem parada. Os portoes de imagem ` +
          'conferem a peca renderizada, nao um still.',
      );
    }
    console.log(
      `  ${fonte.largura}x${fonte.altura} · ${fonte.duracao.toFixed(2)}s · ` +
        `${fonte.fps.toFixed(2)} fps · ${mb(fs.statSync(video).size)}`,
    );
  }
```

(As três ocorrências de `fonte.duracao` nos portões 1 e 4 continuam válidas: eles só rodam quando
`soRitmo` é falso, e nesse caso `fonte` foi preenchido.)

**3. A lista de portões, e o argumento novo.**

Na lista de portões válidos (era a linha 77), trocar por:

```js
  const validos = [
    'todos',
    'ritmo',
    'folha',
    'telefone',
    'determinismo',
    'loop',
    'preservacao',
  ];
```

Acrescentar `preservacao: ''` ao objeto `a` de `argumentos()` (o caminho do descritor de
preservação; vazio = usa o do projeto), depois de `larguraTelefone: 360`:

```js
    preservacao: '',
```

**4. O portão 0, antes de todos, com o disco injetado.**

```js
  // ------------------------------------------------------------- portao 0
  // O UNICO que nao depende do arquivo renderizado: ele le o briefing e o plano. Cada
  // recusa dele e um render que nao precisava acontecer.
  if (roda('ritmo')) {
    console.log(`\n== portao 0: ritmo ==`);
    const {zBriefing} = await import('../src/briefing/esquema.ts');
    const {portaoDeRitmo} = await import('../src/verificacao/ritmo.ts');

    const caminhoBriefing = path.join(a.projeto, 'briefing.json');
    if (!fs.existsSync(caminhoBriefing)) {
      throw new Error(
        `nao achei ${caminhoBriefing}. O portao de ritmo compara o plano com o ` +
          'briefing que o gerou: sem o briefing nao ha com o que comparar.',
      );
    }
    const briefing = zBriefing.parse(JSON.parse(fs.readFileSync(caminhoBriefing, 'utf8')));
    const plano = JSON.parse(fs.readFileSync(props, 'utf8'));

    // A transcricao, para a RECOMPILACAO. O portao e puro e nao le arquivo.
    let palavras;
    if (briefing.legenda) {
      const t = path.join(a.projeto, briefing.legenda.arquivo);
      if (!fs.existsSync(t)) {
        throw new Error(
          `o briefing declara legenda em ${briefing.legenda.arquivo} e o arquivo nao ` +
            'existe. O portao recompila o briefing para conferir o plano, e sem a ' +
            'transcricao a comparacao seria entre um plano com legenda e um sem.',
        );
      }
      const cru = JSON.parse(fs.readFileSync(t, 'utf8'));
      palavras = Array.isArray(cru) ? cru : cru.palavras;
    }

    // O DISCO, INJETADO. O portao pergunta; quem tem I/O responde.
    const {sondar: sondarArquivo} = await import('../src/motor/sondar.ts');
    const medidas = new Map();
    const disco = {
      existe: (rel) => fs.existsSync(path.join(publicDir, rel)),
      razaoMedida: (rel) => (medidas.has(rel) ? medidas.get(rel) : null),
    };
    // `razaoMedida` e sincrono porque o portao e puro; entao as medidas sao colhidas
    // ANTES, aqui, onde `await` existe.
    for (const cena of plano.cenas) {
      for (const f of cena.fonte.tipo === 'grade' ? cena.fonte.celulas : [cena.fonte]) {
        if (f.tipo !== 'video' && f.tipo !== 'foto') continue;
        const rel = `fonte/${f.arquivo}`;
        if (medidas.has(rel)) continue;
        const abs = path.join(publicDir, rel);
        if (!fs.existsSync(abs)) continue;
        try {
          medidas.set(rel, (await sondarArquivo(abs)).razao);
        } catch (e) {
          console.log(`  AVISO  nao consegui medir ${rel}: ${e.message}`);
          medidas.set(rel, null);
        }
      }
    }

    const v = portaoDeRitmo({plano, briefing, palavras, disco});

    console.log(
      `  ${plano.cenas.length} cena(s) · ${plano.duracaoFrames} frames a ` +
        `${plano.fps} fps · legenda ${plano.legenda ? `${plano.legenda.blocos.length} blocos` : 'nenhuma'} · ` +
        `locucao ${plano.audio.locucao ? plano.audio.locucao.arquivo : 'NENHUMA'} · ` +
        `trilha ${plano.audio.trilha ? plano.audio.trilha.arquivo : 'NENHUMA'}`,
    );
    for (const av of v.avisos) console.log(`  AVISO  ${av}`);
    for (const f of v.falhas) falhas.push(`ritmo [${f.codigo}] ${f.onde}: ${f.mensagem}`);
    console.log(`  ${v.aprovado ? 'OK — ritmo aprovado' : 'REPROVADO'}`);
  }
```

**5. O portão 5, depois do portão 4.**

```js
  // ------------------------------------------------------------- portao 5
  // JA EXISTIA E NUNCA FOI CHAMADO. `src/verificacao/preservacao.ts` tem 125 linhas e 9
  // testes desde 30/09/2026, e a lista de portoes deste script nao o conhecia: peca com
  // recorte de embalagem saia sem nenhuma prova de que o rotulo nao foi alterado, que e
  // exatamente o que este repositorio existe para garantir.
  if (roda('preservacao')) {
    console.log(`\n== portao 5: preservacao do rotulo ==`);
    const descritor = a.preservacao || path.join(a.projeto, 'preservacao.json');
    const plano = JSON.parse(fs.readFileSync(props, 'utf8'));

    if (!fs.existsSync(descritor)) {
      if (plano.exigePreservacao) {
        falhas.push(
          `preservacao: o plano declara ${plano.assets.length} recorte(s) de embalagem e ` +
            `${descritor} nao existe. Ele diz QUAL regiao comparar: {origem, regiao:{x,y,` +
            'largura,altura}, tolerancia}. Sem ele o portao nao tem o que medir, e ' +
            'fail-closed aqui e o comportamento certo.',
        );
      } else {
        console.log(
          `  PULADO: ${descritor} nao existe e o plano nao declara nenhum asset de ` +
            'recorte. Peca sem embalagem no quadro nao tem rotulo para preservar.',
        );
      }
    } else {
      const {compararRegiao} = await import('../src/verificacao/preservacao.ts');
      const d = JSON.parse(fs.readFileSync(descritor, 'utf8'));
      const alvo = path.join(saida, `f${a.frame}a.png`);
      if (!fs.existsSync(alvo)) {
        throw new Error(
          `preservacao precisa do still ${alvo}, que o portao 3 produz. Rode ` +
            '`--portao=determinismo` antes, ou `--portao=todos`.',
        );
      }
      const laudo = await compararRegiao(d.origem, alvo, d.regiao, d.tolerancia ?? 0);
      console.log(
        `  regiao ${d.regiao.largura}x${d.regiao.altura} em (${d.regiao.x},${d.regiao.y}) · ` +
          `${laudo.considerados} pixels considerados · ${laudo.pixelsDiferentes} diferentes · ` +
          `maior delta ${laudo.maiorDelta} · alfa perdido ${laudo.pixelsAlfaPerdido}`,
      );
      if (laudo.pixelsDiferentes > 0) {
        falhas.push(
          `preservacao: ${laudo.pixelsDiferentes} de ${laudo.considerados} pixels da ` +
            `embalagem mudaram (maior delta ${laudo.maiorDelta}). proibicoes.md:7-8 ` +
            'proibe qualquer efeito que altere pixel dentro da embalagem, incluindo ' +
            'glow, gradiente por cima e correcao de cor local.',
        );
      } else {
        console.log('  OK — nenhum pixel da embalagem foi alterado');
      }
    }
  }
```

- [ ] **Step 6: provar que o portão de ritmo roda ANTES do render, e que ele reprova**

**A primeira prova é a que a versão anterior não podia fazer.** O portão tem de rodar num projeto que
ainda **não tem MP4** — é o caso de uso inteiro dele.

Run:
```
cd instagram/remotion
mv projetos/01-private-label/saida projetos/01-private-label/_saida-guardada
node scripts/compilar.mjs --projeto=projetos/01-private-label
node scripts/conferir.mjs --projeto=projetos/01-private-label --portao=ritmo
mv projetos/01-private-label/_saida-guardada projetos/01-private-label/saida
```
Expected: o bloco `== portao 0: ritmo ==` **sem** o bloco `== peca ==` acima dele, e **sem** o erro
`a peca renderizada nao existe`. Se aparecer aquele erro, a parte 2 do Step 5 não foi aplicada e o
portão continua dependendo do render — o defeito exato que esta tarefa conserta.

Depois, com a pasta de volta, o veredito:

Run: `cd instagram/remotion && node scripts/conferir.mjs --projeto=projetos/01-private-label --portao=ritmo`

Expected: `REPROVADO`, com **uma** falha:

```
FALHA ritmo [legenda-recuada] legenda.ancora: 1 bloco(s) de legenda foram grudados no
frame 0, com recuo de ate 14 frames -- o piso e 10 ...
```

**E essa reprovação é verdadeira, não um falso positivo.** A Tarefa 7, Step 2c mediu por que: a fala de
`pl.wav` começa em **1,135 s** e o Whisper pôs os dois primeiros blocos **dentro do silêncio**. Com o
motor antigo, a palavra `"Você está"` nunca apareceu nesta peça e ninguém sabia. O portão passou a
dizer isso em voz alta — e é ela que serve de prova de que o portão dispara, em vez de um caso
inventado.

**Não conserte o `briefing.json` para o portão passar.** A resolução é de dado (re-transcrever, ou
corrigir à mão as duas primeiras palavras com o início medido) e está registrada na Tarefa 7, Step 2c
como decisão do Rafael. Registre o veredito e siga.

E a terceira prova, a do plano editado à mão — a que o teste do Step 1 cobre e que agora falha pelo
motivo certo:

Run:
```
cd instagram/remotion
node -e "const f=require('node:fs');const p='projetos/01-private-label/plano.json';const j=JSON.parse(f.readFileSync(p));j.duracaoFrames=720;f.writeFileSync(p,JSON.stringify(j,null,2))"
node scripts/conferir.mjs --projeto=projetos/01-private-label --portao=ritmo
node scripts/compilar.mjs --projeto=projetos/01-private-label
```
Expected: **três** falhas, e as três por motivos diferentes — `[plano-nao-e-do-briefing]` nomeando
`duracaoFrames`, `[duracao-nao-fecha]` com os três números, e `[legenda-recuada]`. Saída **1**.

O que **não** pode aparecer é `[plano-incoerente]`: o hash do briefing continua correto, porque o
briefing não mudou. Se ele aparecer, a comparação está olhando o campo errado. Se `[plano-nao-e-do-
briefing]` **não** aparecer, a recompilação não está sendo feita — e aí a proteção contra plano editado
à mão continua sendo a que a versão anterior tinha: nenhuma.

- [ ] **Step 6b: provar que o portão 5 DISPARA — ligar não é exercitar**

O portão 5 estava órfão; ligá-lo e nunca vê-lo falhar o deixaria órfão com outra aparência. **"Depois de
escrever um portão, prove que ele dispara pelo comando"** é a lição que este próprio plano manda escrever
no `CLAUDE.md` na Tarefa 13.

A prova usa o que já está no disco: `projetos/01-private-label/public/assets/suave-250g.png`, um recorte
**4096×2304** com alfa (medido na Tarefa 4A).

Primeiro, o descritor. Criar `instagram/remotion/projetos/01-private-label/preservacao.json`:

```json
{
  "_leia": "Descritor do portao 5. `origem` e o recorte publicado (a fonte da verdade do rotulo); `regiao` e onde ele aparece no frame renderizado, em pixel do QUADRO; `tolerancia` e o delta por canal que ainda conta como igual. O portao compara pixel por pixel usando o alfa da origem como mascara.",
  "origem": "public/assets/suave-250g.png",
  "regiao": {"x": 0, "y": 0, "largura": 4096, "altura": 2304},
  "tolerancia": 0
}
```

Depois, a prova em duas metades — e ela **não precisa de render novo**, porque compara a origem consigo
mesma e com uma cópia alterada:

Run:
```
cd instagram/remotion
node --experimental-strip-types -e "
const {compararRegiao} = await import('./src/verificacao/preservacao.ts');
const d = JSON.parse(require('node:fs').readFileSync('projetos/01-private-label/preservacao.json','utf8'));
const o = 'projetos/01-private-label/' + d.origem;
const igual = await compararRegiao(o, o, d.regiao, 0);
console.log('IGUAL  ', igual.pixelsDiferentes, 'de', igual.considerados, 'maior delta', igual.maiorDelta);
"
```
Expected: `IGUAL 0 de <N> maior delta 0`, com `N` **maior que zero**. Um `considerados: 0` seria um portão
que compara nada e aprova tudo — e é exatamente o modo de falha silencioso que esta prova existe para
excluir.

Run:
```
cd instagram/remotion
node --experimental-strip-types -e "
const fs = require('node:fs');
const {PNG} = require('pngjs');
const d = JSON.parse(fs.readFileSync('projetos/01-private-label/preservacao.json','utf8'));
const o = 'projetos/01-private-label/' + d.origem;
const png = PNG.sync.read(fs.readFileSync(o));
// mexe em UM canal de UM pixel opaco, no meio da imagem
let i = 0;
for (let p = 0; p < png.width * png.height; p++) {
  if (png.data[p * 4 + 3] === 255) { i = p; break; }
}
png.data[i * 4] = png.data[i * 4] ^ 0xff;
fs.mkdirSync('out', {recursive: true});
fs.writeFileSync('out/suave-alterado.png', PNG.sync.write(png));
const {compararRegiao} = await import('./src/verificacao/preservacao.ts');
const r = await compararRegiao(o, 'out/suave-alterado.png', d.regiao, 0);
console.log('ALTERADO', r.pixelsDiferentes, 'diferentes, maior delta', r.maiorDelta);
"
```
Expected: `ALTERADO 1 diferentes, maior delta 255`. **Um pixel muda e o portão acusa.** Se der
`0 diferentes`, o portão não está comparando o que diz comparar, e ligá-lo no `conferir.mjs` seria
decoração.

E por fim o portão pelo **comando**, que é o que a lição pede:

Run:
```
cd instagram/remotion
node scripts/conferir.mjs --projeto=projetos/01-private-label --portao=determinismo --frame=300
node scripts/conferir.mjs --projeto=projetos/01-private-label --portao=preservacao --frame=300
```
Expected: o bloco `== portao 5: preservacao do rotulo ==` com a linha de região e contagem. **Aqui ele
vai REPROVAR**, e isso é esperado: o frame 300 do Reel não contém a embalagem naquela região — a peça
`01-private-label` não põe recorte no quadro. A reprovação prova que o portão **mede de verdade**; depois
dela, **apague o `preservacao.json`** deste projeto:

Run: `cd instagram/remotion && rm projetos/01-private-label/preservacao.json`
Expected: `--portao=preservacao` volta a dizer `PULADO: ... o plano nao declara nenhum asset de recorte`.

**Pular dizendo por quê é diferente de pular calado**, e a diferença é o que separa um portão de uma
linha de log.
- [ ] **Step 7: rodar a suíte e o typecheck**

Run: `cd instagram/remotion && npx vitest run && npm run tsc`
Expected: `npm run tsc` sem saída, e os **18** testes de `ritmo.test.ts` passando junto com os
anteriores. `tests/preservacao.test.ts` (9 `it`) continua passando sem nenhuma mudança — o portão só
passou a ser **chamado** e a ser **exercitado**, e o módulo não mudou.

- [ ] **Step 8: commit**

```bash
git add instagram/remotion/src/verificacao/ritmo.ts \
  instagram/remotion/tests/ritmo.test.ts instagram/remotion/scripts/conferir.mjs
git commit -m "$(cat <<'MSG'
Portoes: ritmo ANTES do render, e a preservacao orfa passa a ser chamada e exercitada

O portao de ritmo deixou de exigir o MP4 renderizado, que era o que o impedia de rodar
num projeto novo -- e ele passou a RECOMPILAR o briefing para comparar o plano, porque um
hash do briefing nunca detecta edicao no plano.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 11: a skill `canastra-briefing`, e a poda da `canastra-video`

Skill **nova**, irmã de `canastra-video`, e não uma extensão dela: dois donos de um fluxo é pior
que um, do mesmo jeito que dois planos. Medido: `.claude/skills/canastra-video/SKILL.md` tem 239
linhas e a seção `## Antes de escrever uma linha: o que coletar` está na linha 32 — ela **migra
inteira** e sai de lá, senão o texto existe em dois lugares e eles divergem.

**Files:**
- Create: `.claude/skills/canastra-briefing/SKILL.md`
- Modify: `.claude/skills/canastra-video/SKILL.md` (uma linha na tabela de roteamento; a seção de coleta sai)

- [ ] **Step 1: criar `.claude/skills/canastra-briefing/SKILL.md`**

```markdown
---
name: canastra-briefing
description: Use when starting any Café Canastra moving piece from information rather than from a file — the Rafael brings a series, a photo, a recording, numbers, a hook, or just an idea — or when a briefing.json must be written, validated, compiled into plano.json, or when a briefing was refused by the engine and needs to be understood. Also use when deciding which of the 12 catalogue series a piece belongs to.
---

# Briefing do motor de vídeo — Café Canastra

Esta skill é dona da **entrada**: coleta, esquema, compilação, recusas, portão de ritmo e
registro de lição. A `canastra-video` é dona da **saída**: render, portões de imagem, ffmpeg,
pasta pública, normalização de áudio.

O motor vive em `instagram/remotion/`. **Todo texto de tela é desenhado por código, nunca por
modelo generativo** — é a diferença entre este fluxo e a `canastra-conteudo`.

---

## Rotear primeiro

| A tarefa é… | Skill |
|---|---|
| jogar informação e virar peça; escrever ou consertar `briefing.json` | **canastra-briefing** (esta) |
| renderizar, passar portões de imagem, entregar arquivo | `canastra-video` |
| imagem estática gerada por modelo | `canastra-conteudo` |
| a embalagem aparece legível dentro da peça | esta **e** `canastra-embalagem` |

---

## O fluxo, em uma linha

```
informação → briefing.json → compilar.mjs → plano.json → render → portões
```

`briefing.json` é **a verdade humana**, editável à mão, com **um relógio só**: segundos contados
do início da cena. `plano.json` é **artefato gerado** e não se edita — ele carrega o `sha256` do
briefing, e o portão de ritmo reprova plano cujo hash não bate.

---

## Antes de escrever uma linha: o que coletar

Colete **na ordem em que as respostas travam**, e pare na primeira que faltar. Faltando qualquer
uma, **pergunte** — não escolha por ele.

1. **A série do catálogo.** São 12 slugs em `instagram/estrategia/05-formatos.md` §4, mais
   `avulsa`. **7 das 12 estão bloqueadas** por captura, negociação ou por um dado da operação:
   série bloqueada **para aqui**, e o que se faz é dizer qual bloco de captura falta. As três da
   fila são `voce-sabia`, `objecao-preco` e `piada` (§8).
2. **As fontes, com caminho real e camada.** Fotografia obedece às camadas de `base-curada/`:
   `03-mood-terceiros` e `04-quarentena` **nunca** viram pixel. Uma tem marca d'água, outra tem
   rosto de quem não autorizou.
3. **Tem locução?** Troca metade do pipeline: com locução, a legenda nasce de Whisper
   (`src/legenda/transcrever.ts`, modelo **multilíngue** — `medium.en` é só inglês); sem locução,
   não há legenda e a **trilha passa a ser obrigatória** (item 5).
4. **Duração alvo e superfície**, e o `fps` e a razão de exibição **medidos por `sondar()`**.
   Nunca leia `width`/`height` do container: `pl.mp4` grava 1024×576 e exibe 576×1024
   (`displaymatrix -90`); os packshots leem 4096×2304 e exibem 2304×4096 (`Orientation 6`).
   Armadilha já paga duas vezes.
5. **A faixa de áudio.** `audio` é **obrigatório**, e `locucao` e `trilha` não podem ser os dois
   `null`: `05-formatos.md` §3, **[oficial]**, Reel sem áudio perde elegibilidade para não-seguidor.
   "Mudo" no catálogo significa **sem locução**, nunca sem faixa. O portão de ritmo reprova peça muda.
   A locução mora em `public/fonte/` (material cru nosso); a trilha em `public/audio/`, separada porque
   música licenciada tem procedência que material gravado por nós não tem.
6. **Os formatos.** `9:16` sempre; `1:1` e `4:5` quando também vai para o feed. O 1:1 **não é
   recorte** do 9:16 — `layout()` reenquadra.
7. **O gancho e o CTA, nas palavras dele.** "Chama no direct" é CTA; "conheça a marca" não é.
8. **Licenças, se alguma.** Ver a seção abaixo. O padrão é nenhuma.

---

## Escrever o briefing

Comece do exemplo real: `instagram/remotion/projetos/01-private-label/briefing.json`. O esquema
está em `src/briefing/esquema.ts` e é a fonte da verdade; o resumo:

| campo | regra que morde |
|---|---|
| `fps` | inteiro 1..120, default 30. É dele que toda duração em frame sai |
| `formatos` | `9:16` · `1:1` · `4:5` · `16:9`. O 16:9 é latente: a margem de base dele é 51,03% da altura |
| `duracao.modo` | **sem default.** `somaCenas` (as cenas mandam) ou `totalFixo` (`alvoS` manda) |
| `cenas[].duracaoS` | segundos. A posição da cena vem da **ordem no array**, nunca de um campo de tempo |
| `transicoes` | **exatamente `cenas.length - 1`**. Use `{"tipo":"corte"}` onde não houver — corte é 0 frames |
| `fonte.tipo` | `video` · `foto` · `cor` · `grade`. Grade tem 2 a 4 células de fonte **simples** |
| `fonte.razaoExibicao` | **medido por `sondar()`**, nunca lido do container |
| `fonte.registro` (foto) | **obrigatório, sem default**: `moldura` · `cartao` · `telaCheia`. É `proibicoes.md:24` cumprido por construção |
| `eventos[].papel` | `manchete` · `dado` · `etiqueta`. **`legenda` não é papel de evento** |
| `eventos[].entradaS` | segundos, relativo ao início **da cena** |
| `eventos[].pista` | **obrigatório**: `topo` · `principal` · `tela`. `rodape` é da legenda. **Não existe campo `encaixe`**: ele é derivado da pista mais o formato, e `tela` é o único caminho para a cartela |
| `legenda.relogio` | `fonte`, e só. Enum de um valor: declarar é o ponto, não escolher |
| `legenda.ancora` | **obrigatório**, três casos: `{"tipo":"locucao"}` · `{"tipo":"cena","indice":N}` · `{"tipo":"segundo","valorS":X}`. É o instante da transcrição que cai no frame 0 da peça |
| `audio` | **obrigatório**. `locucao` e `trilha` podem ser `null`, **não os dois**. `ganhoDb` é relativo, nunca LUFS |
| `audio.trilha` | exige `loopar`, `fadeEntradaS` e `fadeSaidaS`, **sem default**: 20 s de trilha em 40 s de peça é loop ou silêncio na metade |
| `assets` | os recortes de embalagem, por nome. `[]` é o caso comum. O laudo **nunca** é copiado para cá: a presença do arquivo em `public/assets/` **é** o laudo |

Chave que começa com `_` é **comentário** e o esquema a ignora: use `_leia` para documentar o
briefing por dentro.

**O que o briefing NÃO escolhe**, e por quê: família de tipografia, cadência de revelação e pista
padrão vêm do **papel** (`src/motor/evento.ts`). Um botão que quem escreve o briefing pode girar
sem saber avaliar produz inconsistência silenciosa entre peças da mesma série.

---

## Compilar e conferir

```bash
cd instagram/remotion
node scripts/compilar.mjs --projeto=projetos/<p> --seco   # só imprime, não escreve
node scripts/compilar.mjs --projeto=projetos/<p>          # escreve plano.json
node scripts/conferir.mjs --projeto=projetos/<p> --portao=ritmo
```

O `--seco` imprime, **por formato**, qual encaixe o motor **derivou** da pista, com o corpo em px, a
mancha em % do quadro, o piso de dominância e se domina. **Leia essa tabela antes de renderizar**: é
onde se vê que a manchete saiu menor que a legenda, que foi o defeito medido do motor antigo (48 px de
corpo e 3,793% de mancha no 1:1, contra um piso de 6,925%).

E leia as **três linhas do rebase da legenda** — deslocamento, grudados em 0 com o maior recuo, e
descartados. Elas contam o que o motor antigo engolia: na peça `01-private-label`, a primeira palavra
da fala nunca apareceu e ninguém sabia.

Depois do render, a `canastra-video` assume os portões de imagem.

---

## Quando o motor recusa

As recusas têm **código estável** e vêm todas de uma vez, não uma por rodada. Não "ajuste o
briefing até passar" — leia o que a mensagem mediu.

| código | o que fazer |
|---|---|
| `transicoes-contagem` | pôr `{"tipo":"corte"}` onde não houver transição |
| `tempo-morto` | dar evento à cena, ou ligar `licencas.aceitaTempoMorto` com justificativa |
| `evento-estoura-cena` | alongar a cena ou declarar `duracaoS` no evento. O stagger empurra o fim junto com o começo |
| `abaixo-do-piso` | o piso é `entrada + holdFinal + entrada` = 36 frames a 30 fps. Derivado dos tokens, não escolhido |
| `peca-muda` | declarar `locucao` ou `trilha` no `audio`. É elegibilidade, não gosto |
| `dado-regulatorio` | lote, fabricação e validade **não** entram por texto de tela (lição 22) |
| `pista-ocupada` | duas camadas no mesmo lugar ao mesmo tempo. Mude a pista ou o tempo |
| `dois-acentos` | um acento de cor por cena (`proibicoes.md:20`) |
| `branco-puro` | o fundo da marca é `COR.terra` (#3B2A1F) |
| `arquivo-com-caminho` | o campo é o **nome** dentro de `public/fonte/`, sem pasta |
| `plano-nao-e-do-briefing` | alguém editou `plano.json`. Recompile — e se o número tem de mudar, mude o **briefing** |
| `plano-incoerente` | o **briefing** mudou depois de compilar. Decida qual dos dois está certo |
| `audio-mudo` | `locucao` e `trilha` os dois `null`. É elegibilidade, não gosto |
| `legenda-sem-ancora` | a âncora não tem de onde ler. Três saídas, e a mensagem nomeia as três |
| `legenda-recuada` | a transcrição começa antes da âncora em mais de 10 frames. **Meça de onde a fala começa** antes de mexer na âncora: `ffmpeg -i <wav> -af silencedetect=noise=-40dB:d=0.2 -f null -` |
| `sem-dominante` | nenhum evento da cena domina o quadro naquele formato. Declare `pista: "tela"`, encurte o texto, ou tire o formato |
| `razao-nao-bate` | `razaoExibicao` declarada ≠ medida. Rode `sondar()` e **copie** o número |
| `arquivo-ausente` / `asset-sem-laudo` | o arquivo não está em `public/fonte/` ou `public/assets/` |
| `licenca-sem-justificativa` | ≥ 12 caracteres dizendo por quê |

---

## As 12 licenças

São técnicas que **colidem com `src/identidade/proibicoes.md`**: partículas, orbes de brilho,
varredura de luz, shockwave, mola com overshoot, revelação caractere a caractere, flash no corte,
iris wipe, motion blur burst, swipe de marca-texto, highlight de palavra ativa, tempo morto.

Três regras:

1. **Todas nascem `false`.** Nada que colida com a marca entra por omissão.
2. **Ligar exige `licencas.justificativa` com ≥ 12 caracteres**, e o refinador reprova sem.
3. **Nenhuma está implementada.** O campo registra a decisão, versionada e auditável; o código
   vem depois dela. O portão de ritmo **avisa** a cada licença ligada.

**Decida por série, não por peça** — senão a coesão da série vira acidente. E a decisão é do
Rafael: não ligue nenhuma por conta própria.

O substituto legítimo para "um hit visual a cada 0,4–0,8 s" neste motor é **corte e tipo**:
palavra entrando, bloco de legenda virando, cartela cobrindo. É o que cena e manchete plural
passaram a permitir.

---

## O que nunca fazer

- Editar `plano.json` à mão. Ele é gerado e carrega o hash do briefing.
- Escrever `razaoExibicao` sem `sondar()`. O container mente **por dois nomes**: `displaymatrix` no
  vídeo e EXIF `Orientation` no JPEG. O portão de ritmo confere o campo contra a medida, tolerância
  0,005 — e o dedo já errou duas das três fotos de um briefing de protótipo por isso.
- Deixar a peça sair muda porque "é sem locução".
- Copiar `aprovado: true` do laudo de recorte para dentro do briefing: isso transforma um portão
  fail-closed em decoração.
- Ligar uma licença "só para testar".
- Declarar uma série bloqueada como se a matéria-prima existisse.

---

## Registro de lição

Quando algo falhar e custar uma rodada, a correção não é só consertar: é acrescentar a lição ao
**Registro de lições** no fim de `CLAUDE.md`, no formato **sintoma → causa raiz → regra**. Todo
erro que não virou regra escrita será repetido pela próxima sessão, que não tem a memória desta.
```

- [ ] **Step 2: podar a `canastra-video`**

Em `.claude/skills/canastra-video/SKILL.md`:

1. Na tabela `## Rotear primeiro`, acrescentar uma linha **no topo** do corpo da tabela:

```markdown
| a informação ainda não é um arquivo: série, briefing, planejamento | **canastra-briefing** |
```

2. **Apagar a seção inteira** `## Antes de escrever uma linha: o que coletar` (linha 32 até a
linha antes de `## Pipeline, em ordem`, na linha 52), e pôr no lugar:

```markdown
## Antes de escrever uma linha

A coleta virou skill: **`canastra-briefing`**. Ela é dona da entrada — série do catálogo, fontes
e camada, locução, duração, trilha obrigatória, formatos, gancho e CTA, licenças — e do
`briefing.json` que compila para `plano.json`.

Esta skill começa onde o `plano.json` existe. Se ele não existe, você está na skill errada:

```bash
cd instagram/remotion
node scripts/compilar.mjs --projeto=projetos/<p>
```

O texto de coleta **não** vive mais aqui de propósito: duas skills descrevendo a mesma coleta
divergem no primeiro conserto.
```

3. Trocar as **duas** menções a "quatro portões" — estão na **linha 13**
(`A peça só é entregue depois de passar pelos quatro portões`) e na **linha 146**
(`## Os quatro portões — regra dura, não sugestão`) — por "seis portões", e acrescentar duas
linhas à tabela de portões da linha 155, mantendo as quatro colunas dela: a de ritmo **antes** da
linha do portão 1, e a de preservação **depois** da linha do portão 4:

```markdown
| 0 | ritmo | comando | roda **antes** do render: plano que não corresponde ao briefing, evento abaixo do piso, peça muda, duas camadas na mesma pista |
| 5 | preservação | comando | pixel alterado dentro da embalagem. Fail-closed quando o briefing declara `exigePreservacao` |
```

E acrescentar, depois do parágrafo do **Portão 4**:

```markdown
**Portão 0 — ritmo.** O único que não depende do arquivo renderizado: ele lê `briefing.json` e
`plano.json` e reprova antes de gastar minutos de render. É também onde as licenças ligadas
aparecem como **aviso**, nomeando a linha de `proibicoes.md` que cada uma derruba.

**Portão 5 — preservação.** Compara a região da embalagem entre o recorte de origem e o frame
renderizado, pixel por pixel, com o alfa da origem como máscara. Ele **existia desde 30/09/2026 e
não era chamado por ninguém**: `conferir.mjs` não o listava. Precisa do still do portão 3, então
rode `--portao=todos` ou `--portao=determinismo` antes.
```

4. Trocar `props.json` por `plano.json` nas **quatro** menções medidas: linhas **70**
(`Escrever o props.json`, que passa a ser `Compilar o plano.json`, com o comando
`node scripts/compilar.mjs --projeto=projetos/<p>`), **77** e **79** (os dois `--props=`) e **115**
(`No props.json, arquivo é só o nome`). Run:
`grep -n "props.json" .claude/skills/canastra-video/SKILL.md` — **nenhuma linha deve sobrar**.

- [ ] **Step 3: conferir que as duas skills não se contradizem**

Run:
```
grep -c "o que coletar" .claude/skills/canastra-video/SKILL.md
grep -c "o que coletar" .claude/skills/canastra-briefing/SKILL.md
grep -rn "props.json" .claude/skills/
```
Expected: `0` na primeira, `1` na segunda, e **nada** na terceira. Se a primeira der 1, a seção
não saiu e o texto agora existe em dois lugares — que é exatamente o que a C8 da spec decidiu
evitar.

- [ ] **Step 4: commit**

```bash
git add .claude/skills/canastra-briefing .claude/skills/canastra-video
git commit -m "$(cat <<'MSG'
Skills: canastra-briefing e dona da entrada; canastra-video perde a coleta

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 12: um escritor só — `gerar-props.mjs` sai, e o portão da manchete migra

Resolução de **C9**: `scripts/gerar-props.mjs` (13.165 B) escreve `props.json`, e o compilador
escreve `plano.json`. Dois escritores disputando o mesmo papel divergem no primeiro conserto —
então o script sai **no mesmo commit** em que o compilador assume.

O que **não** pode sair junto é `tests/manchete-props.test.ts` (16 `it`): é o portão que prova que
a manchete é **citação literal da fala**, palavra por palavra, e sem ele "manchete" volta a ser
campo de texto livre no meio de um pipeline que existe para nunca queimar frase inventada no
quadro. Ele migra para o briefing.

**Files:**
- Modify: `instagram/remotion/projetos/01-private-label/briefing.json` (recebe o bloco `_manchete`)
- Modify: `instagram/remotion/tests/manchete-props.test.ts` (lê o briefing e o plano)
- Delete: `instagram/remotion/scripts/gerar-props.mjs`
- Delete: `instagram/remotion/projetos/01-private-label/props.json`

- [ ] **Step 1: mover a proveniência da manchete para o briefing**

O `props.json` de hoje tem um bloco `_manchete` com a proveniência estruturada. Copiá-lo para o
`briefing.json` é o que mantém o portão vivo: chave começando com `_` é **comentário** e o esquema
a ignora, então ela sobrevive no arquivo e o teste a lê do JSON cru.

Em `projetos/01-private-label/briefing.json`, acrescentar depois de `"_leia"`:

```json
  "_manchete": {
    "nota": "texto = CITACAO LITERAL de transcricao.json, palavras dePalavra..atePalavra (indices 0-based, contiguas), com a UNICA transformacao de caixa alta. inicioMs e o inicioMs da palavra dePalavra; entradaS do evento = (inicioMs/1000) - fonte.aparaAntesS, porque o relogio do evento e o da CENA. tests/manchete-props.test.ts prova tudo isso e reprova copy inventada.",
    "citacao": "sua própria marca de café",
    "dePalavra": 11,
    "atePalavra": 15,
    "inicioMs": 3460,
    "fimMs": 4530,
    "fps": 30,
    "palavraAcentoTexto": "MARCA"
  },
```

Nenhum número novo: os sete campos são os mesmos que estão no `props.json` hoje.

- [ ] **Step 2: fazer o teste ler o briefing, sem mexer nas 16 asserções**

Em `tests/manchete-props.test.ts`, substituir o bloco das linhas **40–42** (de
`const PROJETO` até a linha do `palavras`) por:

```ts
const PROJETO = '../projetos/01-private-label';
const briefing = ler(`${PROJETO}/briefing.json`);
const plano = ler(`${PROJETO}/plano.json`);
const palavras: Palavra[] = ler(`${PROJETO}/transcricao.json`);

// ADAPTADOR. As 16 asserçoes deste arquivo provam a mesma coisa que provavam antes -- que
// a manchete e citacao literal da fala -- e o que mudou foi so ONDE o dado mora:
// `props.json` virou `briefing.json` (verdade humana) mais `plano.json` (artefato
// gerado). Reconstruir a forma antiga aqui mantem a prova intacta em vez de reescrever 16
// testes que ja estavam certos.
//
// OS `blocos` VEM DE `agrupar()`, NAO DO PLANO -- e isso e um conserto, nao um atalho.
//
// A versao anterior deste adaptador somava `aparaFrames` de volta aos blocos do plano para
// "voltar ao relogio da fonte". Nao funciona, porque `compilarLegenda` e DESTRUTIVO: ele
// descarta bloco cujo fim cai antes do frame 0 e gruda em 0 o que atravessa o corte.
// Medido nos dados reais: `blocos[0]` = {'Você está', 0, 20} e `blocos[1]` =
// {'procurando algo', 20, 49} no tempo da fonte; depois do rebase de -34, o bloco 0 morre
// e o 1 vira {0, 15}. Reconstruindo com +34 sairia {34, 49} -- e o original era {20, 49}.
// O bloco 0 nao voltaria de jeito nenhum, e o `texto` era descartado junto.
//
// Passava por sorte: das 16 asserçoes so `Math.max(...fimFrame)` usa `blocos`, e o ultimo
// fimFrame sobrevive (684 + 34 = 718). Qualquer asserçao futura sobre INICIO de bloco
// mediria ficcao.
//
// `agrupar(palavras, {fps})` e exatamente o que produzia os `blocos` do `props.json`:
// mesma funcao, mesma entrada, relogio da FONTE. Ele nao reconstroi -- ele RECALCULA, e o
// resultado e o dado original, com `texto` e tudo.
const cenaZero = briefing.cenas[0];
const aparaFrames = Math.round((cenaZero.fonte.aparaAntesS ?? 0) * briefing.fps);
const eventoManchete = (cenaZero.eventos as Array<Record<string, unknown>>).find(
  (e) => e.papel === 'manchete',
);

const props = {
  razaoFonte: plano.razaoDaPeca,
  cortarAntesFrames: aparaFrames,
  // no relogio da FONTE, que e o relogio da proveniencia -- recalculado, nao reconstruido
  blocos: agrupar(palavras, {fps: briefing.fps}),
  manchete: eventoManchete
    ? {
        texto: eventoManchete.texto as string,
        // `pista: 'tela'` e o unico caminho para a cartela desde 01/10/2026: o encaixe e
        // derivado da pista mais o formato, e nao existe mais campo `encaixe` no briefing.
        modo: eventoManchete.pista === 'tela' ? ('cartela' as const) : ('sobreImagem' as const),
        inicioFrame: Math.round((eventoManchete.entradaS as number) * briefing.fps) + aparaFrames,
        palavraAcento: eventoManchete.palavraAcento as number | undefined,
      }
    : null,
  _manchete: briefing._manchete,
};
```

E ao topo do arquivo de teste, junto dos imports existentes:

```ts
import {agrupar} from '../src/legenda/agrupar';
```

**Uma asserção deste arquivo muda de valor, e ela é conhecida.** `formaTextoTela` e `duracaoDaFrase`
passaram a exigir `cadencia` na Tarefa 2 (linhas 63, 65, 176, 186 e 211 — medidas), então acrescente
`const C = cadencia(30);` ao topo e passe `C`. **Nenhum número muda com isso**: a 30 fps
`cadencia(30)` devolve exatamente os frames de antes.

E trocar a linha que lê a proveniência (era a linha 91, `const prov = props._manchete as …`) —
ela continua válida porque o adaptador acima já expõe `_manchete`. Só a mensagem de erro muda, na
linha 97:

```ts
    expect(prov, 'briefing.json tem manchete e nao tem "_manchete"').toBeTruthy();
```

E o comentário da linha 170, que citava `props.json`:

```ts
    // O limite vem da TRANSCRICAO, para nao repetir aqui a duracao da peca: o ultimo
    // bloco de legenda marca o fim da fala, e a peca vai no minimo ate esse ponto.
```

- [ ] **Step 3: rodar o teste e conferir que passa**

Run: `cd instagram/remotion && npx vitest run tests/manchete-props.test.ts`
Expected: `Tests 16 passed (16)`.

Se `inicioFrame` falhar, a conta é esta e ela está medida: a proveniência diz `inicioMs: 3460`,
que a 30 fps dá `Math.round(3.46 * 30)` = **104**; o briefing declara `entradaS: 2.333`, que dá
`Math.round(2.333 * 30)` = **70**; e `70 + 34` = **104**. Se der 103 ou 105, o `entradaS` do
briefing foi arredondado com menos casas — corrija o **briefing**, não o adaptador.

- [ ] **Step 4: apagar o script e o `props.json`**

Run:
```
cd instagram/remotion
rm scripts/gerar-props.mjs
rm projetos/01-private-label/props.json
grep -rn "gerar-props\|props\.json" src/ tests/ scripts/ .claude/ ../../.claude/ 2>/dev/null
```
Expected: **nenhuma linha**. Se alguma sobrar, ela aponta para um arquivo que não existe mais — e
é exatamente o tipo de referência morta que faz a próxima sessão recriar o script.

- [ ] **Step 5: rodar a suíte e o typecheck**

Run: `cd instagram/remotion && npx vitest run && npm run tsc`
Expected: `npm run tsc` sem saída, suíte inteira verde.

- [ ] **Step 6: commit**

```bash
git add -A instagram/remotion
git commit -m "$(cat <<'MSG'
Um escritor so: gerar-props.mjs sai e o portao da manchete passa a ler o briefing

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

### Tarefa 13: a prova — uma peça de FOTO PARADA, de briefing a portões

A tarefa que fecha o plano. Nada antes dela provou que o motor faz o que o pedido do Rafael
descreve, porque `01-private-label` é a peça antiga: um vídeo, uma cena. Esta peça é **três cenas
de foto parada, com trilha e transição** — o caminho que 5 das 12 séries precisam e que o motor
não tinha.

A matéria-prima é real e foi medida nesta sessão:

| arquivo | medida | como medi |
|---|---|---|
| `base-curada/01-real-verificada/fazenda-medeiros-1250m/cafezal/IMG_1398.JPG` | **4032×3024**, EXIF `Orientation = 1`, `format_name: image2` | `ffprobe -show_streams -show_frames -read_intervals '%+#1' -show_format` |
| razão de exibição da foto | **1,333333** (não há rotação para honrar) | 4032 / 3024, e `sondar()` da Tarefa 4A confirma com `rotacao: {fonte: 'exif', graus: 0}` |
| `projetos/01-private-label/public/fonte/pl.wav` | existe, 778.736 B, **24,33 s**, fala começa em **1,135 s** | `ls -la` e `ffmpeg -af silencedetect=noise=-40dB:d=0.2` |
| `projetos/01-private-label/transcricao.json` | array de 75 `{texto, inicioMs, fimMs}` | `node -e` sobre o arquivo |

**Files:**
- Create: `instagram/remotion/projetos/02-foto-parada/briefing.json`
- Create: `instagram/remotion/projetos/02-foto-parada/public/fonte/` (foto e wav copiados)
- Create: `instagram/remotion/projetos/02-foto-parada/public/audio/` (a trilha)
- Create: `instagram/remotion/projetos/02-foto-parada/transcricao.json` (copiado)

- [ ] **Step 1: montar a pasta pública do projeto novo**

`base-curada/` é gitignorado e pesado, e vive só no diretório principal — então o material é
**copiado** para a pasta pública do projeto, que também é gitignorada.

**No Git Bash** (o shell deste plano; ver a seção "Em que shell rodar os comandos deste plano"):

```
cd instagram/remotion
mkdir -p projetos/02-foto-parada/public/fonte projetos/02-foto-parada/public/audio
cp "../../base-curada/01-real-verificada/fazenda-medeiros-1250m/cafezal/IMG_1398.JPG" \
  projetos/02-foto-parada/public/fonte/cafezal.jpg
cp projetos/01-private-label/public/fonte/pl.wav projetos/02-foto-parada/public/fonte/locucao.wav
cp projetos/01-private-label/public/fonte/pl.wav projetos/02-foto-parada/public/audio/ambiente.wav
cp projetos/01-private-label/transcricao.json projetos/02-foto-parada/transcricao.json
ls -la projetos/02-foto-parada/public/fonte/ projetos/02-foto-parada/public/audio/
```

No PowerShell, as duas primeiras linhas viram:

```powershell
New-Item -ItemType Directory -Force projetos/02-foto-parada/public/fonte, projetos/02-foto-parada/public/audio
Copy-Item "../../base-curada/01-real-verificada/fazenda-medeiros-1250m/cafezal/IMG_1398.JPG" projetos/02-foto-parada/public/fonte/cafezal.jpg
```

Expected: `cafezal.jpg` e `locucao.wav` em `fonte/`, `ambiente.wav` em `audio/`.

**Sobre `ambiente.wav` ser uma cópia da locução: isso é honesto e é declarado.** A **D9** da spec
continua aberta — não existe música licenciada nem som ambiente no acervo, e a peça de prova não
resolve isso. Usar a mesma locução nas duas faixas exercita o **mecanismo** (duas `<Audio>` na árvore,
com ganhos diferentes, uma com `loopar`) sem fingir que a matéria-prima existe. O `_leia` do briefing
diz isso em voz alta.

O nome do arquivo de origem tem espaço e parêntese em vários irmãos dele (`IMG_1397 (2).JPG`);
`IMG_1398.JPG` foi escolhido por **não** ter, porque `staticFile()` com espaço no nome é uma
rodada perdida que não precisa acontecer.

- [ ] **Step 2: escrever `projetos/02-foto-parada/briefing.json`**

```json
{
  "_esquema": "canastra-briefing/1",
  "_leia": "PECA DE PROVA DO MOTOR, nao peca publicavel. Ela existe para exercitar em UM arquivo o que 5 das 12 series precisam: foto parada, tres cenas, tres registros, transicao, locucao, trilha e legenda. `serie` e 'avulsa' de proposito: a locucao e o pitch de private label, nao um roteiro de 'voce sabia', e declarar uma serie do catalogo aqui seria dizer que a materia-prima dela existe. E `audio.trilha` aponta para uma COPIA da locucao: a D9 (de onde vem a faixa) continua aberta, e isto exercita o mecanismo sem fingir acervo que nao temos.",
  "_manchete": {
    "nota": "as duas manchetes sao CITACAO LITERAL de transcricao.json, com a unica transformacao de caixa alta.",
    "cena0": "sua própria marca de café (palavras 11..15)",
    "cena2": "a gente tem plantio próprio (trecho contiguo)"
  },
  "serie": "avulsa",
  "fps": 30,
  "formatos": ["9:16", "1:1", "4:5"],
  "duracao": {"modo": "somaCenas"},
  "cenas": [
    {
      "duracaoS": 8,
      "fonte": {
        "tipo": "foto",
        "arquivo": "cafezal.jpg",
        "razaoExibicao": 1.333333,
        "registro": "telaCheia",
        "enquadramento": {"tipo": "recorte", "x": 0.289, "y": 0.0, "largura": 0.422, "altura": 1.0},
        "camera": "pushLento"
      },
      "eventos": [
        {
          "papel": "manchete",
          "texto": "SUA PRÓPRIA MARCA DE CAFÉ",
          "entradaS": 0.5,
          "palavraAcento": 2,
          "pista": "principal"
        }
      ]
    },
    {
      "duracaoS": 8,
      "fonte": {
        "tipo": "foto",
        "arquivo": "cafezal.jpg",
        "razaoExibicao": 1.333333,
        "registro": "moldura",
        "enquadramento": {"tipo": "recorte", "x": 0.25, "y": 0, "largura": 0.5, "altura": 1},
        "camera": "parado"
      },
      "eventos": [
        {
          "papel": "etiqueta",
          "texto": "MEDEIROS 1250 M",
          "entradaS": 0.5,
          "pista": "topo"
        }
      ]
    },
    {
      "duracaoS": 8.33,
      "fonte": {
        "tipo": "foto",
        "arquivo": "cafezal.jpg",
        "razaoExibicao": 1.333333,
        "registro": "cartao",
        "enquadramento": {"tipo": "faixa"},
        "camera": "pushLento"
      },
      "eventos": [
        {
          "papel": "manchete",
          "texto": "A GENTE TEM PLANTIO PRÓPRIO",
          "entradaS": 1.0,
          "pista": "principal"
        }
      ]
    }
  ],
  "transicoes": [
    {"tipo": "fade", "duracaoS": 0.5},
    {"tipo": "corte"}
  ],
  "legenda": {
    "arquivo": "transcricao.json",
    "relogio": "fonte",
    "ancora": {"tipo": "locucao"}
  },
  "audio": {
    "locucao": {"arquivo": "locucao.wav", "ganhoDb": 0, "aparaAntesS": 1.135},
    "trilha": {
      "arquivo": "ambiente.wav",
      "ganhoDb": -18,
      "aparaAntesS": 0,
      "loopar": true,
      "fadeEntradaS": 0.5,
      "fadeSaidaS": 0.8
    }
  },
  "assets": [],
  "gancho": "a pergunta sobre lucro nos dois primeiros segundos, sobre a lavoura real",
  "cta": "clique aqui embaixo e vem conosco"
}
```

**Cinco escolhas deste briefing saem de medição, e nenhuma é gosto:**

1. **`pista: "principal"` nas duas manchetes.** Medido com fonte 4:3 e o texto real: em `principal` a
   manchete dá **99 px** de corpo e mancha de **10,435% / 18,552% / 14,841%** nos três formatos, contra
   pisos de **6,861% / 12,198% / 9,758%** — domina nos três. Em `topo` daria 79 px e **5,297% / 9,417%
   / 7,534%**, abaixo do piso nos três, e o portão reprovaria com `sem-dominante`. **Esta é a D2
   virando decisão de briefing.**
2. **`pista: "topo"` na etiqueta.** Medido: `MEDEIROS 1250 M` dá 84 px de corpo e **2,940%** de mancha —
   abaixo do piso, e está **certo**: carimbo não é o elemento dominante da cena, e o portão não exige
   dominância de `etiqueta`. A cena 1 existe para exercitar exatamente esse caso.
3. **`registro: "telaCheia"` com `recorte`, não com `faixa`.** `refinar()` recusa
   `telaCheia` + `{"tipo":"faixa"}` com o código `telacheia-com-faixa`: `telaCheia` diz "a foto É o
   quadro" e `faixa` é `contain`, que deixaria 42,19% de fundo chapado numa foto paisagem num 9:16. O
   recorte `x: 0.289, largura: 0.422` é o mesmo do protótipo `out/_spec-briefing/b-jornada-foto.json`.

   **E esta é a peça MISTA que exercita o conserto de `razaoDaPeca()`.** A cena 2 é `cartao` +
   `{"tipo":"faixa"}`, logo entra na conta e `razaoDaPeca` = **1,333333**; as cenas 0 e 1 são
   `recorte` e **não** entram. Consequência, e ela é a razão de `Cena.tsx` escolher a caixa da
   fonte: `zonas.video` no 9:16 é uma faixa de **1080×810** no meio de 1920, então a cena 0
   receberia 810 px de altura e "tela cheia" deixaria 57,81% do quadro em terra chapado. Com a
   caixa do quadro para as cenas que preenchem, a cena 0 enche 1080×1920 e a cena 2 continua em
   contain — é isso que `f60.png` e `f480.png` conferem no pixel, e **se a foto da cena 0 sair com
   faixas de terra em cima e embaixo, o conserto não foi aplicado.**
4. **`aparaAntesS: 1.135` na locução.** É o início de fala **medido** em `pl.wav` (Tarefa 7, Step 2c),
   não o `1.14` arredondado. A âncora da legenda aponta para este número.
5. **`duracaoS: 8.33` na última cena.** `emFrames(8.33, 30)` = 250, e 240 + 240 + 250 − 15 = **715**.

- [ ] **Step 3: compilar a seco e ler as duas tabelas**

Run: `cd instagram/remotion && node scripts/compilar.mjs --projeto=projetos/02-foto-parada --seco`

Expected, e estas são contas que dá para conferir na mão:

- `duracao ....... 715 frames (23,833 s)` — `emFrames(8,30)=240`, `emFrames(8,30)=240`,
  `emFrames(8.33,30)=250`, soma **730**, menos o fade de `emFrames(0.5,30)=15` = **715**.
- `cenas ......... 3`
- `legenda ....... 37 blocos`, `deslocamento -34 frames (ancora: locucao)`,
  `grudados em 0 ... 1, maior recuo 14 frames`, `descartados ... 1 antes do inicio, 0 depois do fim`
  — os mesmos números do `01-private-label`, porque é a mesma transcrição e a mesma âncora.
  `emFrames(1.135, 30)` = 34.
- `locucao ....... locucao.wav` · `trilha ....... ambiente.wav` · `assets ....... 0`
- `razao da peca . 1.333333`
- **três blocos de evento, um por evento, cada um com três linhas de formato.**

**Leia as nove linhas de formato**, e confira contra a tabela do Step 2: as seis das manchetes têm de
dizer `faixa` e `DOMINA`; as três da etiqueta, `faixa` e `nao e candidato a dominar`.

`faixa` nos três formatos porque a fonte é **paisagem**: medido, a sobra ao lado do vídeo é **0,00 px**
no 9:16, no 1:1 e no 4:5 quando a foto é 4:3 — o vídeo preenche a largura e é letterboxado na altura. É
por isso que a geometria de pista **tem** de ser fração da coluna de texto e não da altura do quadro: com
a faixa de topo do quadro, a interseção com o vídeo letterboxado media **760,00 × 0,00 px** e todo evento
caía em cartela.

- [ ] **Step 4: compilar de verdade e passar o portão de ritmo**

Run:
```
cd instagram/remotion
node scripts/compilar.mjs --projeto=projetos/02-foto-parada
node scripts/conferir.mjs --projeto=projetos/02-foto-parada --portao=ritmo
```
Expected: `escrito projetos/02-foto-parada/plano.json`, e depois o bloco `== portao 0: ritmo ==`
**sem** o bloco `== peca ==` acima dele — porque **o MP4 ainda não existe**, e é exatamente isso que o
portão 0 existe para permitir. Se aparecer `a peca renderizada nao existe`, o Step 5 da Tarefa 10 não
foi aplicado.

O veredito esperado é **REPROVADO com uma falha**, `[legenda-recuada]` com recuo de 14 frames contra o
piso de 10 — a mesma da peça antiga, pela mesma causa medida (a transcrição começa antes da fala). Não
conserte o briefing para passar: registre, e veja a Tarefa 7, Step 2c.

Se aparecer `[peca-muda]`, o áudio não foi lido. Se aparecer `[sem-dominante]`, compare com a tabela do
Step 2 — e **não mude o teste nem o briefing antes de ler os dois números da mensagem.**

Se aparecer `[razao-nao-bate]`, o `razaoExibicao: 1.333333` do briefing não bate com o que `sondar()`
mede no `cafezal.jpg`. O número medido está no Step 9 da Tarefa 8; **copie o medido**, não o arredondado.

- [ ] **Step 5: render dos três formatos**

Run:
```
cd instagram/remotion
npx remotion render src/index.ts Reel projetos/02-foto-parada/saida/reel.mp4 \
  --props=projetos/02-foto-parada/plano.json \
  --public-dir=projetos/02-foto-parada/public
npx remotion render src/index.ts Feed projetos/02-foto-parada/saida/feed.mp4 \
  --props=projetos/02-foto-parada/plano.json \
  --public-dir=projetos/02-foto-parada/public
npx remotion render src/index.ts Feed4x5 projetos/02-foto-parada/saida/feed4x5.mp4 \
  --props=projetos/02-foto-parada/plano.json \
  --public-dir=projetos/02-foto-parada/public
```
Expected: três MP4. Conferir dimensão e duração medindo, não confiando:

Run:
```
cd instagram/remotion
node --experimental-strip-types -e "
const {sondar} = await import('./src/motor/sondar.ts');
for (const f of ['reel','feed','feed4x5']) {
  const s = await sondar('projetos/02-foto-parada/saida/'+f+'.mp4');
  console.log(f, s.largura+'x'+s.altura, s.duracao.toFixed(3)+'s', Math.round(s.duracao*30)+' frames');
}"
```
Expected: `reel 1080x1920 23.833s 715 frames`, `feed 1080x1080 23.833s 715 frames`,
`feed4x5 1080x1350 23.833s 715 frames`.

- [ ] **Step 6: normalizar o áudio e provar que a peça NÃO é muda**

**O `normalizar-audio.mjs` NÃO aceita caminho posicional.** Medido na função `argumentos()` dele: ela
casa `/^--([a-zA-Z]+)=(.*)$/` e, no `else`, lança
`argumento nao entendido: <cru>. Use --chave=valor ou --medir.` As chaves válidas são **`projeto`,
`arquivo` e `medir`**. A versão anterior deste plano passava
`node scripts/normalizar-audio.mjs projetos/02-foto-parada/saida/reel.mp4` — o script lançava antes de
fazer qualquer coisa.

Run:
```
cd instagram/remotion
node scripts/normalizar-audio.mjs --projeto=projetos/02-foto-parada --medir
node scripts/normalizar-audio.mjs --projeto=projetos/02-foto-parada
```
Expected: o relatório de LUFS, com o alvo `-14` de `AUDIO.lufs` (medido: `normalizar-audio.mjs:90` lê
`lufs` **e** `picoDbtp` dos tokens). O `--medir` primeiro, porque medir antes de escrever é mais barato
que descobrir depois que o arquivo já foi reescrito.

**E `feed4x5.mp4` NÃO é normalizado por esse comando.** Medido: sem `--arquivo`, o script monta a lista
como `['reel.mp4', 'feed.mp4'].map(...)` — o 4:5 é formato novo e não está lá. Rode o terceiro à mão:

```
cd instagram/remotion
node scripts/normalizar-audio.mjs --arquivo=projetos/02-foto-parada/saida/feed4x5.mp4
```

Acrescentar `'feed4x5.mp4'` àquela lista seria o conserto certo, e ele é de uma linha — mas mexe num
script que os quatro portões antigos usam, então **fica registrado aqui** em vez de entrar de carona
nesta tarefa. O comando acima resolve a peça de hoje.

**E antes disso, a prova de que existe faixa:**

Run:
```
cd instagram/remotion
node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe -v error \
  -select_streams a -show_entries stream=codec_name,duration -of default=nw=1 \
  projetos/02-foto-parada/saida/reel.mp4
```
Expected: um `codec_name` de áudio e uma `duration`. **Saída vazia significa peça muda** — e peça
muda perde elegibilidade para não-seguidor (`05-formatos.md` §3, **[oficial]**), que é a ausência
A4 que esta tarefa fecha.

- [ ] **Step 6b: as DUAS faixas estão na mistura, e o `loop` funciona**

Uma faixa de áudio no MP4 não prova que as **duas** entraram: elas são mixadas numa só. A prova de que
a trilha está lá é o **nível**, e ela é medível.

Run:
```
cd instagram/remotion
node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -hide_banner \
  -i projetos/02-foto-parada/saida/reel.mp4 -ss 1 -t 1 -af volumedetect -f null - 2>&1 | grep -i volume
```
Expected: `mean_volume` **acima de −60 dB** no primeiro segundo. Aquele segundo é silêncio na locução
(a fala começa em 1,135 s, e `aparaAntesS: 1.135` corta justamente isso) — então **o que se ouve ali é a
trilha**, a −18 dB com fade de entrada de 0,5 s. Silêncio digital (`-91.0 dB` ou `-inf`) significa que a
segunda `<Audio>` não entrou na árvore.

**E o `loop`, que o `tsc` não prova** (a Tarefa 9, Step 6b explica por quê: `loop` é prop declarada do
`Audio` de `@remotion/media`, medida em `node_modules`, mas um parâmetro aceito pode ser ignorado pelo
pipeline). Esta peça tem 23,833 s e a faixa 24,33 s — **ela não exercita o loop**. Para medir, uma
variante descartável:

Run:
```
cd instagram/remotion
node -e "const f=require('node:fs');const p='projetos/02-foto-parada/briefing.json';const j=JSON.parse(f.readFileSync(p,'utf8'));j.duracao={modo:'totalFixo',alvoS:35};f.writeFileSync('projetos/02-foto-parada/briefing-loop.json',JSON.stringify(j,null,2))"
node scripts/compilar.mjs --projeto=projetos/02-foto-parada --seco
```
e, com o briefing de 35 s compilado e renderizado num arquivo à parte, medir depois de 24,33 s:

```
node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -hide_banner \
  -i <o mp4 de 35 s> -ss 26 -t 3 -af volumedetect -f null - 2>&1 | grep -i volume
```
Expected: `mean_volume` acima de −60 dB. **Se der silêncio, o `loop` é aceito e ignorado** — e a saída
honesta está escrita na Tarefa 9, Step 6b: ou o campo sai do esquema com a recusa correspondente no
refinador, ou a repetição passa a ser feita no ffmpeg. **Decida depois de ver o número.**

- [ ] **Step 7: os seis portões, no comando**

Run: `cd instagram/remotion && node scripts/conferir.mjs --projeto=projetos/02-foto-parada --composicao=Reel --frame=300`
Expected: os seis blocos impressos. O portão 5 tem que dizer
`PULADO: ... o plano nao declara nenhum asset de recorte` — esta peça não tem recorte de embalagem, e
pular **dizendo por quê** é diferente de pular calado.

**O portão 0 vai REPROVAR com `[legenda-recuada]`**, então `checagens duras` não sai `OK` e a saída é
**1**. Isso é o portão funcionando: veja o Step 4. Para ver os outros cinco em verde, rode-os por nome
(`--portao=folha`, `--portao=telefone`, `--portao=determinismo`, `--portao=loop`,
`--portao=preservacao`).

- [ ] **Step 8: CONFERÊNCIA NO PIXEL — os três registros, a transição e o 4:5**

Nenhum teste renderiza. Este passo é a prova, e **é ele que fecha a caixa que a Tarefa 8, Step 9 deixou
em aberto.**

**Os frames saem da aritmética das janelas de EVENTO, não das de cena.** A versão anterior derivou as
janelas das cenas certo (0..240, **225**..465, 465..715 — o fade de 15 frames faz a cena 1 começar
antes) e **não** derivou as dos eventos dentro delas, então dois dos sete stills pediam frames em que o
evento já tinha terminado. A conta, agora:

| cena | janela na peça | evento | cadência | irmãos | duração | janela do EVENTO |
|---|---|---|---|---|---|---|
| 0 | 0..240 | manchete, `entradaS 0.5` → frame 15 | palavra | 5 | `duracaoDeIrmao(5)=48`, `duracaoComIrmaos(5,48)=60` | **15..75** |
| 1 | 225..465 | etiqueta, `entradaS 0.5` → frame 15 | **bloco** | **1** | `duracaoDeIrmao(1)=36`, `duracaoComIrmaos(1,36)=36` | **240..276** |
| 2 | 465..715 | manchete, `entradaS 1.0` → frame 30 | palavra | 5 | 60 | **495..555** |

Os dois erros que isso conserta: a etiqueta vive em **240..276** e o plano pedia **f300**; a segunda
manchete vive em **495..555**, e **555 é o primeiro frame FORA** — `TextoTela` devolve `null` em
`t >= duracaoCena`. O plano pedia f555 e dizia "no hold".

E é aqui que o **irmãos = 1** da etiqueta importa: sem o conserto da Tarefa 3 (a cadência chegando ao
render), o plano diria 36 e a tela desenharia 42 — a janela do still sairia certa e a do pixel, não.

**No Git Bash:**

```
cd instagram/remotion
for FR in 60 258 480 530 660 232; do
  npx remotion still src/index.ts Reel projetos/02-foto-parada/saida/f$FR.png --frame=$FR \
    --props=projetos/02-foto-parada/plano.json \
    --public-dir=projetos/02-foto-parada/public
done
npx remotion still src/index.ts Feed4x5 projetos/02-foto-parada/saida/f45-60.png --frame=60 \
  --props=projetos/02-foto-parada/plano.json \
  --public-dir=projetos/02-foto-parada/public
```

No PowerShell, o laço é `foreach ($FR in 60,258,480,530,660,232) { npx remotion still ... --frame=$FR }`
— ou abra o Git Bash, que é o que este plano assume.

| still | frame | o que tem que estar lá |
|---|---|---|
| `f60.png` | 60 | cena 0, `registro: telaCheia` — a foto ocupa o quadro **inteiro, 1080×1920**, sem borda, sem sombra e **sem faixa de terra em cima nem embaixo**. Terra ali significa que a cena recebeu `zonas.video` (1080×810) em vez da caixa do quadro — o conserto de `Cena.tsx` não foi aplicado. A manchete está no hold (janela 15..75) |
| `f258.png` | 258 | cena 1, `registro: moldura` — a foto **recuada** com terra em volta nos quatro lados, com sombra de papel. A etiqueta `MEDEIROS 1250 M` **visível** (janela 240..276), em **IBM Plex Mono**, não em Archivo Black |
| `f480.png` | 480 | cena 2, `registro: cartao` — a foto recuada 5% e **ancorada no alto**, com mais terra embaixo que em cima. **Sem texto**: a manchete só entra em 495 |
| `f530.png` | 530 | cena 2 com a segunda manchete no hold (janela 495..555; a última palavra entra em 507 e a entrada dela fecha em 519) |
| `f660.png` | 660 | cena 2 perto do fim: a manchete já saiu em 555 e **não** há resíduo de texto a ~19% de opacidade |
| `f232.png` | 232 | **o meio do fade** (225..240): as **duas** cenas misturadas — `telaCheia` por baixo e `moldura` por cima. Se aparecer terra chapada, as janelas das cenas não estão se sobrepondo e `tests/cena-tempo.test.ts` estava medindo outra coisa |
| `f45-60.png` | 60 (4:5) | o mesmo instante em 4:5 — e o encaixe que a tabela do Step 3 previu: `faixa`, corpo 99 px, mancha 14,841% |

**Descreva por escrito o que você viu em cada um dos sete stills**, em recorte ampliado e não na
imagem inteira (lição 13). Em miniatura, os três registros parecem a mesma foto.

E marque as duas caixas que ficaram em aberto lá atrás:

- [ ] a conferência no pixel dos três registros está feita (fecha a **Tarefa 8, Step 9**)
- [ ] o `loop` da trilha foi medido com `volumedetect` (fecha a **Tarefa 9, Step 6b**)
- [ ] **Step 9: registrar as lições no `CLAUDE.md`**

Acrescentar ao **Registro de lições**, no fim de
`C:/Users/rafae/OneDrive/Desktop/Canastra Inteligencia/Agentes AI/Canastra-Content-Creator/CLAUDE.md`,
continuando a numeração que estiver lá. São **sete**, e cada uma custou uma rodada:

```markdown
N. **O motor de vídeo tinha `FPS = 30` chumbado e nenhuma camada de texto chamava
   `useVideoConfig`** → `TEMPO` estava em frames medidos a 30 fps, então a 60 fps cada entrada,
   saída, hold e stagger duraria metade, com exit 0 e sem aviso. O conserto foi declarar os
   tempos em SEGUNDOS e derivar os frames de `cadencia(fps)`, com o parâmetro OBRIGATÓRIO → num
   refatoramento de unidade, faça o parâmetro obrigatório em vez de dar default: o compilador
   enumera os pontos de chamada que ficaram para trás, e um default esconde exatamente o bug que
   se está consertando. A prova de não-regressão foi o **sha256 do still** antes e depois — e ela
   só vale com o **controle** rodado antes (o portão de determinismo, dois renders do mesmo
   frame): sem o controle, um "MUDOU" é ambíguo entre regressão e não-determinismo.
N+1. **A manchete saía menor que a legenda no 1:1 e no 4:5** — 48 px e 26 px de corpo contra 78 px
   — e `proibicoes.md:19` pede um elemento dominante por cena → a causa não era a zona: era um
   `min` que esquecia de onde a caixa começava. `layout.ts:68-73` calculava a **largura** da caixa
   de legenda supondo `x = video.x + 16k` e usava `x = seguro.x`, então com vídeo em coluna a caixa
   deslizava 144,00 px e vazava o vídeo em 128,00 px — e era nesse vazamento que a coluna da
   manchete morava → **antes de redesenhar uma zona, confira se as duas contas dela falam do mesmo
   ponto de partida.** O conserto foi uma linha, e a interseção manchete × legenda foi de 90,20 px
   a 0,00 nos quatro formatos.
N+2. **"A manchete invade a legenda em 353,20 px"** era um rótulo errado em cima de um número
   certo: 353,20 é `manchete.fim − legenda.y`, não interseção — e é **maior que a caixa inteira da
   legenda** (172,80 px), o que torna a frase impossível. Um revisor mediu o mesmo defeito só no
   eixo y e escreveu "100% da caixa" → **interseção de caixas é grandeza de dois eixos, e medir um
   só dá um número plausível.** Plausível é pior que absurdo: o absurdo você vê. (Terceira aparição
   do mesmo erro no mesmo desenho.)
N+3. **`sha256Do` com `JSON.stringify(valor, Object.keys(valor).sort())` era um no-op** → o segundo
   argumento do `JSON.stringify` **não é uma ordem de chaves: é uma allowlist aplicada
   recursivamente a todo objeto da estrutura.** Com as chaves de topo apenas, `cenas` serializa como
   `[{}]` e dois briefings com durações e textos completamente diferentes dão o mesmo hash → para
   hashear estrutura, escreva a **serialização canônica** e teste que ela distingue o que
   `JSON.stringify` cru confundiria (`{a: undefined}` vs `{}`, `[1,2]` vs `{0:1,1:2}`).
N+4. **Um hash DO BRIEFING nunca detecta edição NO PLANO** → o teste mutava o plano com spread, o
   hash era copiado intacto, e a falha não podia disparar pelo motivo certo. A proteção nomeada do
   desenho protegia outra coisa (briefing alterado depois de compilar) → quando a promessa é "X
   editado à mão é detectável", a checagem tem de olhar **X**: o portão passou a **recompilar** o
   briefing e comparar o plano inteiro. E dois códigos distintos, porque as ações são diferentes:
   recompile, ou decida qual dos dois arquivos está certo.
N+5. **O portão que "roda antes do render" exigia o render** → `conferir.mjs` checava a existência do
   MP4 e chamava `sondar()` **antes de qualquer portão**, então `--portao=ritmo` falhava com "a peça
   renderizada não existe" num projeto novo. Funcionava no projeto antigo por acidente, porque o MP4
   velho estava lá → **a ordem do orquestrador é parte do contrato do portão.** Prove o portão no
   caso de uso dele: rode-o num projeto **sem** o artefato que ele promete dispensar.
N+6. **`sondar()` inventava `fps: 25` e `duracao: 0.04` para foto parada, e devolvia razão 1,7778
   onde a exibição é 0,5625** → ele honrava só `side_data_list.rotation` (displaymatrix, metadado de
   vídeo) e não o EXIF `Orientation`. Terceiro caso do mesmo padrão no repositório: `pl.mp4` com
   displaymatrix −90, os três recortes 4096×2304 deitados com o `Orientation 6` da origem perdido na
   publicação, e agora a foto → **em todo ponto onde o motor recebe imagem ou vídeo, a dimensão de
   exibição é derivada de metadado de rotação, e o metadado tem dois nomes: `side_data_list.rotation`
   e EXIF `Orientation`.** O mesmo `ffprobe` expõe os dois (`-show_frames -read_intervals '%+#1'`), e
   o valor do `Orientation` vem **preenchido de espaços** (`"    6"`), então comparação de string
   falha em silêncio. E: `duracao`/`fps` viraram `null` em `format_name: image2` — **número inventado
   é pior que ausência.**
N+7. **`src/verificacao/preservacao.ts` existia com 9 testes e ninguém o chamava** →
   `conferir.mjs` listava cinco portões e não o incluía, então peça com recorte de embalagem saía
   sem prova de que o rótulo não foi alterado → módulo de verificação que não está na lista do
   orquestrador é código morto com aparência de proteção. E **ligar não é exercitar**: depois de
   escrever um portão, prove que ele **dispara** pelo comando — alterando um pixel de propósito e
   vendo o portão acusar — e confira que `considerados > 0`, porque um portão que compara nada
   aprova tudo.
```

**E uma lição que só apareceu porque o motor passou a contar em vez de engolir**, que vale escrever
junto: a legenda do `01-private-label` descarta a primeira palavra da fala desde que a peça foi feita, e
ninguém sabia. `Legenda.tsx:34` somava o deslocamento ao frame corrente e o `blocos.find()` do frame 0
caía no segundo bloco; o primeiro era inalcançável. Medido agora: a fala de `pl.wav` começa em
**1,135 s** (`silencedetect`) e o Whisper pôs os dois primeiros blocos **dentro do silêncio** →
**bloco que sai do quadro tem de ser contado, não descartado em silêncio**, e o número no diagnóstico é
o que transforma "a legenda parece certa" em "a legenda perdeu 1 bloco com recuo de 14 frames".
- [ ] **Step 10: commit**

```bash
git add -A instagram/remotion CLAUDE.md
git commit -m "$(cat <<'MSG'
Prova: peca de tres cenas de foto parada, com trilha e transicao, dos portoes ao pixel

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
MSG
)"
```

---

## Verificação final

- [ ] **1: suíte e typecheck**

Run: `cd instagram/remotion && npx vitest run && npm run tsc`
Expected: `npm run tsc` sem saída nenhuma.

**Este plano não declara um total de testes, e isso é deliberado.** A versão anterior dizia
*"+110 testes novos"* e a lista ao lado somava **107** — e como todo `Expected` cumulativo se apoiava
nessa contagem, o executor não tinha como saber se o número final estava certo. Um número que ninguém
somou é pior que nenhum número.

O que se faz, em vez disso, é **contar os arquivos** e conferir o delta:

```
cd instagram/remotion
grep -c 'it(' tests/*.test.ts
```

Os arquivos **novos** deste plano, cada um com a contagem que o próprio passo declara:

| arquivo | `it(` | onde o número é declarado |
|---|---:|---|
| `tests/relogio.test.ts` | 6 | Tarefa 1, Step 4 |
| `tests/cadencia.test.ts` | 6 | Tarefa 2, Step 6 |
| `tests/evento.test.ts` | 9 | Tarefa 3, Step 7 |
| `tests/pistas.test.ts` | 12 | Tarefa 4, Step 5 |
| `tests/encaixe.test.ts` | 9 | Tarefa 4, Step 8 |
| `tests/esquema.test.ts` | 33 | Tarefa 5, Step 9 |
| `tests/refinar.test.ts` | 24 | Tarefa 6, Step 5 |
| `tests/compilar.test.ts` | 22 | Tarefa 7, Step 4 |
| `tests/impressao.test.ts` | 5 | Tarefa 7, Step 4 |
| `tests/registro.test.ts` | 8 | Tarefa 8, Step 4 |
| `tests/cena-tempo.test.ts` | 4 | Tarefa 9, Step 7 |
| `tests/ritmo.test.ts` | 18 | Tarefa 10, Step 7 |

Os arquivos **alterados**: `layout.test.ts` vai de 4 para **6** (Tarefa 4, Step 3 item 6),
`sondar.test.ts` de 6 para **11** (Tarefa 4A), `textotela.test.ts` e `manchete-props.test.ts` mantêm a
contagem (51 e 16 — só ganham o parâmetro `cadencia`), e `agrupar.test.ts` fica em 5, intocado.

A soma dos arquivos novos é **6 + 6 + 9 + 12 + 9 + 33 + 24 + 22 + 5 + 8 + 4 + 18 = 156**, e os
alterados somam **+2** (`layout.test.ts`) **+5** (`sondar.test.ts`) **+3** (do §0, as Tarefas 2 e 3 do
plano de qualidade). Com a BASE de 91 `it(` medida no §0, o total esperado é
**91 + 3 + 2 + 5 + 156 = 257**.

**Este número foi somado, não estimado — mas ele não foi RODADO.** A suíte não foi executada nesta
sessão, e o §0 registra que o plano de qualidade anotou `85 passed` contra as 91 chamadas `it(` que o
`grep` conta. **Use o que a sua execução imprimir**, e se divergir de 255, o arquivo que falta é o que a
soma acusa — não ajuste o número, ache o arquivo.

- [ ] **2: as quatro ausências estruturais, fechadas por `grep`**

Run:
```
cd instagram/remotion
echo "A1 foto:"; grep -c "<Img" src/motor/camadas/Fonte.tsx
echo "A2 eventos em lista:"; grep -c "cena.eventos.map" src/motor/Cena.tsx
echo "A3 cena:"; grep -c "TransitionSeries" src/motor/Peca.tsx
echo "A4 audio:"; grep -c "<Audio" src/motor/camadas/Trilha.tsx
echo "portoes:"; grep -c "'ritmo'" scripts/conferir.mjs
echo "fps derivado, arquivo por arquivo:"
grep -rl "useVideoConfig" src/ | sort
```
Expected: os quatro primeiros ≥ 1, `portoes` ≥ 1, e a **lista** do último com pelo menos
`src/motor/Cena.tsx`, `src/motor/Peca.tsx`, `src/motor/camadas/Fonte.tsx`,
`src/motor/camadas/TextoTela.tsx` e `src/motor/camadas/Trilha.tsx`.

**O comando antigo estava errado e passava por construção.** Ele era
`grep -rlc "useVideoConfig" src/motor/camadas/ src/motor/ | wc -l`: as duas raízes se sobrepõem —
`src/motor/` é recursivo e já contém `camadas/` —, então **todo arquivo de `camadas/` era contado duas
vezes** e o número saía inflado; e `-c` junto com `-l` é redundante, porque o `-l` vence. A verificação
*"maior que 1"* passava sem medir o que prometia. Agora a saída é a **lista de nomes**, que é o fato:
antes desta sessão `useVideoConfig` aparecia em **um** arquivo só (`PecaVideo.tsx`), e só lia
`width`/`height`.

- [ ] **3: os dois projetos passam os portões que podem passar**

Run:
```
cd instagram/remotion
node scripts/conferir.mjs --projeto=projetos/01-private-label --composicao=Reel --frame=300
node scripts/conferir.mjs --projeto=projetos/02-foto-parada --composicao=Reel --frame=300
```

Expected: **os dois reprovam no portão 0, com `[legenda-recuada]`, e saem com código 1.** Isso não é
falha do plano: é a reprovação verdadeira que a Tarefa 7, Step 2c mediu — a transcrição começa 14
frames antes da fala, e as duas peças usam a mesma transcrição. Os cinco portões de imagem passam nos
dois, e dá para vê-los por nome:

```
cd instagram/remotion
for P in folha telefone determinismo loop preservacao; do
  node scripts/conferir.mjs --projeto=projetos/02-foto-parada --composicao=Reel --frame=300 --portao=$P
done
```

O `01-private-label` prova que o motor novo **não perdeu** a peça antiga; o `02-foto-parada` prova que
ele ganhou o caminho novo — foto, três cenas, transição, locução e trilha.

- [ ] **4: o briefing é de fato a entrada**

Run:
```
cd instagram/remotion
node -e "
const fs=require('fs');
for (const p of ['projetos/01-private-label','projetos/02-foto-parada']) {
  console.log(p, fs.existsSync(p+'/briefing.json')?'briefing OK':'SEM BRIEFING',
              fs.existsSync(p+'/plano.json')?'plano OK':'SEM PLANO',
              fs.existsSync(p+'/props.json')?'AINDA TEM props.json':'props.json foi');
}"
grep -rn "gerar-props" src/ tests/ scripts/ .claude/ 2>/dev/null
```
Expected: `briefing OK plano OK props.json foi` nos dois, e **nenhuma linha** no `grep` — referência a
script apagado é o que faz a próxima sessão recriá-lo.

- [ ] **5: a conferência de olho, que nenhum comando substitui**

Abra, **em recorte ampliado** (lição 13):

1. os sete stills da Tarefa 13, Step 8 — três registros, o meio do fade, o 4:5 e o frame sem
   resíduo. Os frames saem das janelas de **evento**, e a tabela de lá mostra a conta;
2. `projetos/02-foto-parada/saida/contato.png` (folha de contato) célula por célula;
3. `projetos/02-foto-parada/saida/telefone.mp4` a 360 px — **se a legenda não se lê aí, ela não
   se lê no feed de ninguém**. E olhe a **largura** dela no 1:1 e no 4:5: o conserto da Tarefa 4
   encurtou a caixa em 25,0% e 19,8%, e é aqui que se vê se o preço foi alto;
4. `projetos/02-foto-parada/saida/loop.mp4`, a emenda.

E escreva as respostas das três decisões que este plano deixou medidas e abertas:

- **D2** — no 1:1 e no 4:5, a manchete em `principal` domina o quadro? (O portão diz que sim, por
  área. O olho concorda?)
- **D6/V11** — a legenda mais estreita continua legível e em duas linhas?
- **D9** — de onde vem a trilha de verdade, agora que o mecanismo existe e a peça de prova usa uma
  cópia da locução como placeholder declarado?
## Riscos assumidos

Decisões que a spec deixou abertas, ou em que uma medição deste plano contradisse a spec, e que o plano
**precisou** tomar para poder construir. Cada uma está marcada no código, e desfazer qualquer uma é
mexer num lugar só.

**1. D7(a): as composições passam a usar `calculateMetadata`, lendo `fps` e `durationInFrames` do
plano.** Consequência que muda o dia a dia: **`--props` deixa de ser opcional para um render de
verdade.** Sem ele, o Remotion usa `PLANO_VAZIO` e sai 1 segundo de terra — visivelmente
incompleto, que é melhor que sair com conteúdo de exemplo parecendo pronto, mas ainda é um
comportamento novo. Desfazer é trocar `metadados(formato)` por `durationInFrames` fixo em
`Raiz.tsx` e voltar a registrar uma composição por fps.

**2. D2 resolvida por DERIVAÇÃO e medição, não por escolha de briefing.** O encaixe sai de
`(pista, formato)`; a dominância é medida em **área** e comparada a `1,25 ×` a mancha da legenda; e
quando o texto não domina, `resolverEncaixe` **não tem plano B** — ele devolve `domina: false` e o
portão de ritmo **reprova**. Isso muda o pixel do 1:1 e do 4:5 em peça que declare `pista: "topo"`, e é
a opção (c) da spec com a diferença de que a reprovação é explícita em vez de uma promoção silenciosa a
cartela. Se o Rafael preferir a coluna mesmo pequena, o lugar de mexer é **`FATOR_DE_DOMINANCIA`** em
`src/motor/encaixe.ts`, num lugar só; se preferir cartela, o briefing declara `pista: "tela"`.

**3. O plano não é validado por zod na composição — e a proteção contra plano editado à mão passou a
ser outra.** A Tarefa 5 do plano de qualidade queria schema zod nas composições; aqui `plano.json` é
artefato gerado por um compilador que já validou o briefing, e um segundo esquema espelhando `Plano`
seria uma segunda fonte de verdade que divergiria no primeiro campo novo.

**O que mudou em relação à versão anterior deste risco:** ela dizia que a proteção era o
`_sha256Briefing`. **Não era.** Um hash do briefing detecta *briefing alterado depois de compilar*, e
não *plano editado*: o hash é copiado intacto junto com a edição. Medido no próprio teste que existia,
que mutava o plano com spread e nunca podia falhar pelo motivo certo. Agora o portão **recompila o
briefing e compara o plano inteiro**, canonicamente — e os dois códigos (`plano-nao-e-do-briefing` e
`plano-incoerente`) são separados porque as ações são diferentes. O risco residual é o mesmo de antes,
e continua sendo o único: **quem renderizar direto pelo `npx remotion render`, sem passar o portão, não
é protegido.** Mitigação escrita na skill; mitigação estrutural seria um wrapper de render, e isso não
está neste plano.

**4. `src/motor/pista.ts` e `src/motor/encaixe.ts` são dois arquivos, e a spec §2.4 nomeia um.** A
geometria fica em `pista.ts` e a medição em `encaixe.ts`, porque medir exige `formaTextoTela`, que
importa `identidade/glifos` e `identidade/tokens`. Mantendo `pista.ts` livre dessa dependência,
`motor/evento.ts` pode importar o tipo `Pista` dele sem arrastar tipografia — e foi exatamente essa
importação que tornava impossível o `npm run tsc` da Tarefa 3 na versão anterior. Desfazer é juntar os
dois e aceitar que `evento.ts` dependa de tipografia por caminho transitivo.

**5. A pista `rodape` É `zonas.legenda`, e não a faixa de baixo da coluna que a spec §3.4.2
descreve.** Medido: com fonte em paisagem no 1:1, a faixa de baixo da coluna fica em
`y 661,82 .. 815,40` e `zonas.legenda` em `y 734,40 .. 907,20` — as duas se sobrepõem em **61.560 px²**.
Se `rodape` fosse a faixa, existiriam **duas caixas quase iguais para a mesma coisa** (a que a `Legenda`
desenha e a que o portão confere), e duas caixas quase iguais divergem no primeiro conserto. A faixa de
baixo da coluna fica como **folga**: nenhum evento a declara, e é ela que garante, nas 8 combinações
medidas (4 formatos × 2 razões de fonte), que `principal` não encosta na legenda.

**6. `TransitionSeries.Overlay` fica com o motivo escrito e SEM a declaração.** A spec §3.2.1 pede
"declarado e vazio". Um `<TransitionSeries.Overlay />` vazio no JSX é código morto que o próximo leitor
tenta preencher, e a `TransitionSeries` tem invariante sobre overlay adjacente — um overlay vazio no
lugar errado vira **erro de runtime no render**, não aviso. O comentário no cabeçalho de `Peca.tsx`
explica o que ele é e por que está fora, sem criar o risco.

**7. `exigePreservacao` deixou de ser campo de briefing e passou a ser derivado de `assets`.** A spec
§2.3 tem `assets: Asset[]` e a versão anterior deste plano tinha um booleano. Os dois juntos seriam duas
verdades: o booleano podia dizer `false` com três recortes na lista, e o portão não teria como saber em
qual acreditar. `Plano.exigePreservacao` continua existindo, calculado como `assets.length > 0`.

**E cinco coisas que continuam abertas, sem decisão deste plano:**

- **D1 — as 12 licenças.** Todas `false`, nenhuma implementada. A decisão é por **série**, e é do
  Rafael.
- **D3 — `duracao.modo` sem default.** O plano implementa obrigatório. Se virar um default, o
  lugar é `zBriefingEstrito`, e a consequência é quem pedir 24 s receber 22,4 s sem perceber na
  primeira peça com crossfade.
- **D5 — enquadramento de foto, reformulada pela spec.** Não é "default por série": é *dado que `faixa`
  custa 42,19% de fundo chapado na foto paisagem e 25,00% na retrato, e que o packshot orientado custa
  zero, qual dos três grupos aceita `faixa` e qual exige `recorte`?* A pergunta antiga não era decidível
  porque a medição estava errada. O briefing declara caso a caso.
- **D6 e D11 — corpo de legenda que encolhe, e folga vertical no `sobreImagem`.** Herdadas do plano de
  qualidade, e agora com um custo **medido**: o conserto da largura da legenda (Tarefa 4) encurta a
  caixa em 25,0% no 1:1, 19,8% no 4:5 e 46,5% no 16:9. As Tarefas 1 e 7 daquele plano estão agendadas
  no §0.6.
- **D9 — de onde vem a faixa de áudio das peças sem locução.** A peça de prova usa uma **cópia da
  locução** como trilha, declarada como tal no `_leia` do briefing: isso fecha o motor e **não**
  responde a pergunta. Cinco séries continuam bloqueadas por ela — música licenciada (e qual licença,
  porque a peça é comercial), som ambiente gravado na fazenda (que não existe no acervo hoje), ou
  publicar sem faixa e perder elegibilidade **[oficial]**.

**Duas coisas da spec que este plano deliberadamente NÃO constrói:**

- **`springTiming` como timing de transição.** A spec §3.2.3 o permite exigindo
  `duracaoFramesDeclarada`, porque a duração de uma mola é emergente e o compilador puro não pode
  chamar `spring()` (vem de `remotion`). O plano implementa **só `linearTiming`**: nenhuma das 12
  séries pede mola na transição, e um campo que o compilador aceita e não resolve é a lição 3 do
  `CLAUDE.md`. Quando entrar, o lugar é o union de `zTransicao` mais um ramo em `Peca.tsx`, e o
  teste tem de rodar **no navegador** conferindo `timing.getDurationInFrames({fps})` contra o
  declarado.
- **`src/briefing/esquema-studio.ts` com `zColor()` e `zTextarea()`.** A spec o prevê como a
  fronteira do Studio. Ele não é criado porque o **Risco 3** tirou o `schema` das composições: sem
  schema, não há painel do Studio para tipar, e `@remotion/zod-types` — que arrasta `remotion`
  para dentro de qualquer módulo que o vitest carregue — fica fora do projeto. Se um dia o Studio
  precisar editar briefing na mão, o arquivo nasce ali e **só** ali.

**Dois riscos técnicos que a execução resolve, e um que foi medido e saiu da lista:**

- **O `loop` da trilha pode ser aceito e ignorado.** `@remotion/media/dist/audio/props.d.ts:26` declara
  `loop?: boolean` (medido), mas declaração de tipo não é comportamento de pipeline — é a lição 3 do
  `CLAUDE.md`. A Tarefa 9, Step 6b e a Tarefa 13, Step 6b medem o efeito com `volumedetect` depois de
  24,33 s, e as duas saídas honestas para o caso de falhar estão escritas lá.
- **A varredura de testes da Tarefa 2 é mecânica e pode deixar pontos para trás.** O compilador
  os enumera (`npm run tsc`), e a prova de que a varredura foi correta é que **nenhuma asserção
  numérica muda**: a 30 fps `cadencia(30)` devolve exatamente os frames de antes. Se algum teste
  antigo precisar de número novo, a migração está errada e não é o teste que se ajusta.
- ~~`z.strictObject` pode não existir nessa versão de zod.~~ **Medido, e o risco não existe:**
  `node -e "console.log(require('zod/package.json').version)"` dá **4.5.4** e
  `node -e "const {z}=require('zod');console.log(typeof z.strictObject)"` dá **function**. A versão
  anterior gastava um parágrafo de plano B para um risco que custava um comando para medir e não foi
  medido — que é a forma mais barata de escrever ficção num plano.
