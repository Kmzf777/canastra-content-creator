# Qualidade do motor de vídeo — plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** fechar as violações mecânicas do motor de vídeo — as que uma fonte
independente chama de bug, não de gosto — sem importar nada do que
`src/identidade/proibicoes.md` proíbe.

**Architecture:** o motor já separa o que é provável em Node (`movimento.ts`,
`texto-forma.ts`, `layout.ts`, `agrupar.ts`) do que é só fiação (`.tsx`). Todo
conserto aqui entra pelo lado puro, com teste em `vitest`, e o `.tsx` só passa a
ler o campo novo. Nenhuma tarefa introduz dependência nova além de declarar o
`zod` que já está no `node_modules`.

**Tech Stack:** Remotion 4.0.530, React 19.3, TypeScript 7.0.2, vitest 5.0.2,
zod 4.5.4, `@remotion/media` 4.0.530, `@remotion/fonts`, `@remotion/captions`.

**Diretório de trabalho de todo comando deste plano:**
`C:/Users/rafae/OneDrive/Desktop/Canastra Inteligencia/Agentes AI/Canastra-Content-Creator/instagram/remotion`

**Base medida antes de começar** (`npx vitest run`, 30/09/2026):

```
 Test Files  6 passed (6)
      Tests  85 passed (85)
```

---

## 1. As regras mecânicas, consolidadas

Quatro fontes, todas lidas no arquivo e não de memória:

| sigla | fonte | onde |
|---|---|---|
| **A** | `digbenjamins/remotion-animation` → `CLAUDE.md`, 15.471 B, 360 linhas | `scratchpad/remotion-rules/digbenjamins-CLAUDE.md` |
| **B** | gist de `ThariqS` (o vídeo de 123.422 views) = **cópia da system prompt oficial** `remotion.dev/docs/ai/system-prompt`, verificada string por string | `scratchpad/remotion-rules/thariqs-Remotion-CLAUDE.md` |
| **C** | skills oficiais `remotion-dev/skills`, versão `4.0.531`, sobretudo `remotion-markup/SKILL.md` | `scratchpad/remotion/skills/skills-main/skills/` |
| **D** | elemento oficial **Popping Word Captions** (@JonnyBurger) | `remotion.dev/elements/captions/popping-word-captions` |

### 1.1 O que as fontes prescrevem, com número

| # | regra | número | fonte |
|---|---|---|---|
| 1 | Nunca `linear`. Entrada por `spring()`, o resto por `interpolate()` com easing | mola de entrada `{damping: 200, stiffness: 100, mass: 0.5}`; easing default `Easing.out(Easing.cubic)`; ênfase `Easing.out(Easing.back(1.5))` | A (regra 1 + defaults); B dá só `spring({fps, frame, config:{damping:200}})` |
| 2 | Animar **só** `transform` e `opacity`. Nunca `width`, `height`, `top`, `left`, `margin` | — | A (regra 2) |
| 2b | Usar as propriedades CSS individuais `scale` / `translate` / `rotate`, não a string `transform`; manter a chamada `interpolate()` **inline** no `style`; `output: 'perceptual-scale'` em escala | — | **C só** |
| 3 | Tudo derivado de `fps` por `useVideoConfig()`. Nunca `30` chumbado. Duração em segundos × fps | `0.5 * fps` | A (regra 3); B silencioso (só "default frame rate 30") |
| 4 | `clamp` nos dois lados de todo `interpolate` | — | A (regra 4) e B concordam |
| 5 | Um movimento herói por cena | — | A (regra 5) |
| 6 | Enter, settle, exit. Nada entra nem sai seco | entrada **0,5 s** (15 f a 30 fps), saída **0,4 s** (12 f) | A (regra 6 + defaults) |
| 7 | Stagger de grupo | `índice * 0.06 * fps` = **1,8 f** a 30 fps (e `step = 0.06` é o default de `Stagger.tsx`) | A (regra 7) |
| 8 | Margem title-safe | **5 a 8%** das bordas | A (regra 8) |
| 9 | Determinismo: `Math.random()` proibido, usar `random('seed')`; evitar `useEffect`; nenhum event handler; render puro | — | B |
| 10 | `premountFor={fps}` em **todo** item temporizado que aceita (mídia, `Sequence`, `Series.Sequence`, `TransitionSeries.Sequence`, `TransitionSeries.Overlay`) — um segundo de pré-montagem | `premountFor={fps}` | **C só** |
| 11 | Legenda: página por tempo, pop da palavra ativa, contorno | `combineTokensWithinMilliseconds: 800`; corpo desejado **80 px**; ponta de pop `min(4, duração/2)` frames com `spring({config:{damping:200}})` e saída por `interpolate` 1→0 na mesma janela; escala ativa **1,03** com `transformOrigin: 'center bottom'`; **`WebkitTextStroke: corpo/7`** com `paintOrder: 'stroke fill'`; entrelinha **1,5** | **D** |
| 12 | Defaults de composição | fps **30**; 1920×1080, ou 1080×1920 quando o pedido é vertical; deslocamento de entrada ≤ **40 px** para texto, ≤ **80 px** para bloco grande | A; B (fps 30, 1920×1080) |
| 13 | Props tipadas e validadas por `zod`, `zColor()` para cor, zod **pinado na versão exata** que o Remotion pede (`npx remotion add zod`) | — | A + C |
| 14 | Escala tipográfica | hero 96 / title 64 / body 36 / caption 24 px; espaçamento múltiplo de **8**; uma cor de fundo, uma de frente, **um** acento saturado | A |

### 1.2 Onde as fontes divergem — e não se resolve por média

**D1 — duração de entrada.** A manda **0,5 s** (15 f). D, que é o elemento
oficial de legenda do próprio Remotion, usa **no máximo 4 f = 0,133 s**. São
objetos diferentes (elemento de cena × palavra de legenda), mas a diferença é de
3,75×, e o nosso motor hoje usa 12 f = 0,4 s para manchete e **0 f** para
legenda. Não existe um número único: a decisão tem que ser por camada. Este
plano resolve assim, e diz de onde vem cada metade: entrada de legenda pela
nossa medição (93% da massa no primeiro frame → 2 f), saída de legenda pelo
número de D (4 f).

**D2 — stagger.** A: `0.06 s` = 1,8 f a 30 fps. B: silencioso. Nosso:
`TEMPO.stagger = 3` f = 0,1 s, **1,67×** o de A. O nosso foi medido em
referência; o de A é o default de uma biblioteca. Divergência legítima: fica o
nosso, e fica escrito que é o nosso.

**D3 — mola × bezier.** A e B mandam `spring()` nas entradas. O nosso motor usa
`cubic-bezier(0.20,0.80,0.20,1.00)` para tudo e nunca chama `spring()`
(`movimento.ts:116`). Na prática uma bezier sem overshoot e um `damping: 200`
descrevem o mesmo comportamento — mas só a nossa é mensurável em Node sem
importar `remotion`, e é isso que mantém `tests/textotela.test.ts` rodando fora
do navegador. Divergência de implementação, não de resultado.

**D4 — linear.** A, regra 1: *"Never `linear`. Ever. A linear tween is the
number one tell of amateur motion."* O nosso `push()` é linear **de propósito**
(`movimento.ts:233-239`), porque `proibicoes.md:21` pede "push de câmera lento,
nunca impacto" e qualquer easing concentra a velocidade em algum trecho. A
própria A, na seção de hook, descreve o push do `Background` como *"parallax
`scale` 1.05 → 1.15 over the scene"* **sem dizer easing**. Divergência real, não
resolvida por medida. Fica linear, com esta linha escrita.

**D5 — modo hook.** A tem um "retention override" que **sobrepõe a regra 5** e
prescreve ~30 partículas subindo, 2–3 orbes de brilho em caminho senoidal, um
*light sweep* periódico, `Shockwave` em palavra de impacto, molas com overshoot
`{damping: 11, stiffness: 130, mass: 0.7}` e *"um hit visual a cada 0,4 a 0,8 s"*.
B, C e D não têm nada disso. É o único lugar onde uma das fontes prescreve
exatamente o que `proibicoes.md` proíbe — ver §3.2.

**D6 — margem lateral.** A: 5 a 8%. Nossa: **14,81%** (160 px em 1080), e o
comentário de `layout.ts:14` diz "medidas em referência de Reels" sem registrar
nenhuma medida. Pela lição 10 do CLAUDE.md, isso não é medida, é escolha. Este
plano **mantém os 14,81%** e corrige o comentário, porque mudar a largura da
manchete é decisão estética do Rafael, não bug.

---

## 2. O que o nosso motor viola hoje

Ordenado por impacto sobre a qualidade percebida **nos formatos que de fato
saem** (`Reel` 1080×1920 e `Feed` 1080×1080, `Raiz.tsx:58-75`). Todo número
abaixo foi medido rodando o próprio módulo, não lido de comentário.

### V1 — A legenda é a camada mais vista e a única sem movimento nenhum · regra 6, fonte D
`src/motor/camadas/Legenda.tsx:28-65`, especialmente `:36` e o `<span>` de `:51-63`.

`const b = blocos.find(...)`; `if (!b) return null;` — e nenhuma propriedade do
`<span>` depende do frame: sem `opacity`, sem `scale`, sem `frame` na conta. A
legenda entra por corte e sai por corte, e quando há silêncio entre blocos ela
apaga num frame sobre vídeo em movimento. O cabeçalho do arquivo defende isso
com uma medida real ("93% da massa de movimento já no primeiro frame"), mas 93%
no primeiro frame descreve um pop de 1–2 frames com 7% de assentamento — não
descreve zero. E a medida cobre a **entrada**; a saída não é mencionada em
lugar nenhum do arquivo. Agravante: o token que documenta a decisão,
`LEGENDA.corte: 'seco'` (`tokens.ts:40`), não é lido por ninguém — `grep -rn
"LEGENDA.corte" src/` devolve **0**. É documentação vestida de código.

Segundo defeito na mesma camada: não há contorno. Só `textShadow`
(`Legenda.tsx:59`). Creme sobre imagem em movimento sem contorno é exatamente o
problema que o elemento oficial (D) resolve com `WebkitTextStroke = corpo/7` e
`paintOrder: 'stroke fill'` — **11,14 px** no nosso corpo de 78 px.

### V2 — Tudo desaparece a 18,85% de opacidade, num frame · regra 6
`src/motor/movimento.ts:160-162`, consumido por `TextoTela.tsx:108` e `:125`.

`pSaida = Math.min(1, (t - inicioSaida) / f.saida)` normaliza pelo primeiro
frame **não desenhado**. Medido numa janela de 36 f (fases 12/12/12), presença
nos seis últimos frames desenhados:

```
t=30..35: 0.8105  0.7257  0.6221  0.4986  0.3544  0.1885
t=36    : não é desenhado (TextoTela.tsx:108 devolve null em t >= duracaoCena)
```

O expoente 2,4 **amplifica** o erro: com saída linear o resíduo seria 8,33%; com
`t^2.4` é 18,85%. Vale para cada palavra da manchete **e** para o fundo da
cartela (`TextoTela.tsx:125` liga a `opacity` do fundo em `conjunto.presenca`) —
ali é uma tela cheia de terra sumindo de 18,85% para zero em um frame. Numa cena
real de 6 palavras (66 f) o conjunto no último frame desenhado mede **0,1885**.

`tests/textotela.test.ts:151-159` passa hoje porque mede `progresso(duracao)`,
que é o ramo `'depois'` — nunca o último frame renderizado.

### V3 — 28,70% da altura do Feed 1:1 é margem de baixo · regra 8
`src/motor/layout.ts:15` e `:21`.

Um `k` só, derivado da **largura**, escala também as margens verticais.
Medido rodando `layout()` com `razaoFonte 9/16`:

| formato | topo | base | lado | área segura |
|---|---|---|---|---|
| 1080×1920 | 90,0 px = **4,69%** | 310,0 px = **16,15%** | 160,0 px = 14,81% | 760,0 × 1520,0 |
| 1080×1080 | 90,0 px = **8,33%** | 310,0 px = **28,70%** | 160,0 px = 14,81% | 760,0 × 680,0 |
| 1920×1080 | 160,0 px = **14,81%** | 551,1 px = **51,03%** | 284,4 px = 14,81% | 1351,1 × **368,9** |

No 16:9 metade do quadro é margem, e a área segura fica com 368,9 px de altura —
é exatamente o 368,9 que `texto-forma.ts:205-206` registra como "texto de borda a
borda, o oposto de respiro maior". O sintoma que `linhasDeFolga` tenta consertar
é consequência desta linha.

### V4 — A margem de topo fica em 4,33%, abaixo do piso de 5% · regra 8
`src/motor/layout.ts:15` (`topo: 90`) e `TextoTela.tsx:139-142`.

90,0 px em 1920 = **4,69%**, já abaixo do piso. Pior: em `sobreImagem` o bloco
ancora em `flex-start` e o push escala a caixa por **1,0394** em torno do
centro, então o topo desce para **83,2 px = 4,33%**. Nenhum teste cobre isso —
`tests/textotela.test.ts:376-388` prova que a caixa fica dentro de
`zonas.seguro`, nunca que `zonas.seguro` respeita a borda.

### V5 — A manchete do Feed 1:1 sai em 44 px, menor que a legenda · regra 5 invertida
`src/motor/camadas/texto-forma.ts:193` sobre `layout.ts:58-63`.

Medido com o texto `CAFE ESPECIAL DA SERRA DA CANASTRA`:

| formato | modo | corpo | % da altura |
|---|---|---:|---:|
| 1080×1920 | sobreImagem | 90 px | 4,69% |
| 1080×1920 | cartela | 123 px | 6,41% |
| **1080×1080** | **sobreImagem** | **44 px** | **4,07%** |
| 1080×1080 | cartela | 104 px | 9,63% |

A caixa do `sobreImagem` no 1:1 é a interseção de `zonas.manchete` com
`zonas.seguro` e mede **274,7 × 640,4** — uma coluna estreita ao lado da coluna
de vídeo. A legenda no mesmo quadro tem **78 px**. O elemento que deveria
dominar a cena é o menor texto do quadro.

### V6 — O push é chamado de câmera e move uma camada só · regra 5
`TextoTela.tsx:139-141` escala o `div` do texto; a camada `Fonte`
(`PecaVideo.tsx:110-114`) não escala. Um bloco de texto crescendo 4% sobre um
vídeo parado em escala lê como elemento de interface, não como câmera.
**Isto é divergência, não bug** — ver §3.2, porque aplicar o push à peça inteira
recortaria o vídeo, e isso colide com a regra do próprio `layout.ts:5-6`.

### V7 — Nada é derivado de fps · regra 3
`tokens.ts:15-23` e `:39`; `movimento.ts:34`; `Legenda.tsx`, `Fonte.tsx`,
`TextoTela.tsx` sem `useVideoConfig`.

`grep -rn "useVideoConfig" src/` devolve **uma** ocorrência: `PecaVideo.tsx:97`,
`const {width, height} = useVideoConfig();` — o `fps` está na mão e é
descartado. Medido rodando os tokens:

| token | 24 fps | 30 fps | 60 fps |
|---|---:|---:|---:|
| `entrada: 12` | 0,500 s | 0,400 s | 0,200 s |
| `stagger: 3` | 0,125 s | 0,100 s | 0,050 s |
| `holdFinal: 12` | 0,500 s | 0,400 s | 0,200 s |
| `duracaoMinFrames: 10` | 0,417 s | 0,333 s | 0,167 s |

Registrar uma composição a 60 fps corta pela metade a duração de toda entrada,
saída, hold e stagger **sem erro, sem aviso e com exit 0**.

Instância mais barata do mesmo defeito: `src/legenda/agrupar.ts:20-21` já tem
`fps` no escopo (`:6`), converte ms→frames corretamente em `:12-13`, e duas
linhas abaixo aplica o literal de 30 fps `LEGENDA.duracaoMinFrames`.

### V8 — Nenhum `premountFor` · regra 10
`src/motor/camadas/Fonte.tsx:48-53`. `grep -rn "premountFor" src/` → nada. As
typings instaladas aceitam: `node_modules/@remotion/media/dist/video/props.d.ts:78`
declara `VideoProps ... & InteractivePremountProps`, e
`node_modules/remotion/dist/cjs/Interactive.d.ts:12` mostra que isso é
`'premountFor' | 'postmountFor' | 'styleWhilePremounted' | 'styleWhilePostmounted'`.

### V9 — Nenhum schema zod · regra 13
`src/motor/Raiz.tsx:58-85`. `grep -rn "zod\|schema" src/` → nada. `zod@4.5.4` e
`@remotion/zod-types@4.0.530` **já estão** em `node_modules` (transitivos do
`@remotion/cli`), e `package-lock.json` pina `"zod": "4.5.4"` — mas nenhum dos
dois está declarado em `package.json`. Sem schema, as composições não são
editáveis no Studio e um `props.json` com `"modo": "aleatorio"` só falha na
renderização. (Lição 11 do CLAUDE.md, traduzida para npm: dependência
transitiva não é dependência declarada.)

### V10 — `transform: scale()` em string · regra 2b
`TextoTela.tsx:140` e `:180`. C manda a propriedade individual `scale`, com o
`interpolate` inline, senão o Studio não consegue editar o valor.

### V11 — A legenda estoura a altura da caixa no 16:9 · latente, e o teste finge cobrir
`Legenda.tsx:51-63` não ajusta corpo nenhum: `fontSize = LEGENDA.corpoEm1080 *
escala`, com `escala = width / 1080` (`PecaVideo.tsx:133`). Medido sobre os **38
blocos reais** de `projetos/01-private-label/props.json`, com as larguras de
avanço de `glifos.ts`:

| formato | corpo | caixa | máx. linhas | 2 linhas medem | cabe na altura? |
|---|---:|---:|---:|---:|---|
| 1080×1920 | 78,0 px | 760,0 × 307,2 | 2 (`"melhores profissionais"`, 871,5 px) | 149,8 px | sim |
| 1080×1080 | 78,0 px | 575,5 × 172,8 | 2 (6 de 38 blocos) | 149,8 px | sim |
| 1920×1080 | **138,7 px** | 550,6 × 172,8 | 2 | **266,2 px** | **não** |

**Correção de uma conclusão apressada:** o `<span>` não vaza para fora da caixa,
ele **quebra em duas linhas**, e como a caixa ancora em `flex-end` a última linha
fica sempre na mesma linha de base — a segunda linha aparece **acima**. Ou seja,
1 de 38 blocos no Reel e 6 de 38 no Feed saem em duas linhas e isso **lê como
legenda de duas linhas normal, não como defeito**. Não há defeito visível nos
formatos que saem hoje.

O que existe é risco medido, em dois pontos: (a) no 16:9 duas linhas medem 266,2
px numa caixa de 172,8 e transbordam para cima; (b) nada no motor garante o
limite de duas linhas — um bloco de 3 palavras longas passaria de 224,6 px e
estouraria a caixa do Feed. E `tests/textotela.test.ts:32-36` e
`tests/layout.test.ts:20` varrem 1920×1080 e passam, dando cobertura que não
existe — a lição 10 outra vez. Tarefa 7 fecha o invariante; o 16:9 fica fora
(§3.1).

### V12 — Seis tokens declarados e nunca lidos
`grep -rn` em `src/`: `SOMBRA.papel` 0, `SOMBRA.cartao` 0, `SOMBRA.objetoAlto`
0, `COR.verde` 0, `COR.preto` 0, `LEGENDA.corte` 0. Um token que ninguém lê é
uma decisão que ninguém aplica.

### V13 — A manchete sobre vídeo tem folga vertical zero
`texto-forma.ts:214` dá `linhasDeFolga = 0` ao `sobreImagem`. Medido no 9:16:
corpo 90, entrelinha 0,96, 4 linhas = **345,6 px** numa caixa de **345,6 px** —
sobra relativa **0,000**, contra **0,559** da cartela. É o mesmo defeito de
borda a borda que a cartela já corrigiu, ainda presente no modo que aparece
sobre o vídeo.

---

## 3. O que falta

### 3.1 Cabe na marca

**Agendado neste plano** (tarefas 1 a 7):

| falta | fonte | tarefa |
|---|---|---|
| Ponta de entrada e de saída na legenda | A regra 6 + D | 1 |
| Contorno de legenda `corpo/7` com `paintOrder: 'stroke fill'` | D | 1 |
| Saída que chega a zero no último frame desenhado | A regra 6 | 2 |
| Margem em fração do eixo próprio, topo em 5% | A regra 8 | 3 |
| Push que não come a margem de topo | A regra 8 | 4 |
| Propriedade CSS individual `scale` em vez de string `transform` | C | 4 |
| `premountFor={fps}` no vídeo | C | 5 |
| Schema `zod` das composições, com `z.looseObject` | A + C regra 13 | 5 |
| Portão de fps: 30 é medido, não suposto, e o piso da legenda em segundos | A regra 3 | 6 |
| Invariante de duas linhas na legenda | A regra 8 | 7 |

**Cabe na marca e NÃO está agendado** — cada um com o motivo de ficar fora:

- **Piso de corpo da manchete no Feed 1:1 (V5).** O conserto não é um número: a
  coluna de 274,7 px nasce de `layout.ts:58-63` dar à manchete `sobra * 0.84` do
  espaço ao lado do vídeo. Corrigir é decidir se, no 1:1, a manchete deixa de
  ser coluna e passa a ser faixa sobre o vídeo — mudança de composição, não de
  constante. **Decisão do Rafael**, com um still lado a lado antes.
- **Corpo de legenda que encolhe para caber (V11), como o elemento oficial faz
  com `Math.min(desiredFontSize, fitText(...).fontSize)`.** Medido: encolher por
  bloco resolveria os estouros (0 de 38 nos dois formatos), mas o corpo passaria
  a variar de 78,0 a 68,0 px no Reel e de 78,0 a 51,5 px no Feed — o tamanho da
  legenda mudando de bloco em bloco lê como acidente de render, e é o oposto da
  coesão que a lição 8 do CLAUDE.md pede. Encolher a peça inteira pelo pior
  bloco custaria 78 → 51,5 px em 32 blocos por causa de 6. Nenhuma das duas é
  obviamente melhor que as duas linhas que saem hoje: **decisão do Rafael**, com
  still. A tarefa 7 fecha o invariante de altura no meio-tempo. (E não usar
  `fitText` de `@remotion/layout-utils`: pacote ausente e mede no DOM — ver §5.)
- **Folga vertical no `sobreImagem` (V13).** `linhasDeFolga = 1` no
  `sobreImagem` derrubaria o corpo de 90 para algo menor no 9:16, e o corpo da
  manchete já está em 4,69% da altura. Trocar respiro por tamanho quando o
  tamanho já é o problema é piorar. Volta depois da decisão de V5.
- **Transições de cena por `@remotion/transitions`** (`linearTiming` /
  `springTiming`, `fade()`, `wipe()`). Pacote ausente. Cabe na marca **desde que
  a apresentação seja `fade` ou `wipe`** — `iris`, `clockWipe` e `flip` não
  (§3.2). Não há hoje mais de uma cena por peça, então é YAGNI.
- **`createTikTokStyleCaptions` de `@remotion/captions`** (já instalado,
  4.0.530, **zero usos** em `src/`). Ele pagina por `combineTokensWithinMilli
  seconds: 800`, ou seja pela **pausa da fala**; o nosso `agrupar()` corta em 2
  palavras fixas (`tokens.ts:38`), o que ignora a pausa. Trocar é refazer a
  medição de 2,45 blocos/s e 1,7 palavras/bloco que gerou o token. Fica fora até
  haver uma medição nova.
- **`ensureMaxCharactersPerLine` de `@remotion/captions`** — mesma razão.
- **`random('seed')` em vez de `Math.random()`** (regra 9 de B). `grep -rn
  "Math.random" src/` devolve **0** hoje: não há o que consertar. A regra tem
  que estar escrita antes do primeiro grão, partícula ou jitter, não depois.

### 3.2 Colide com proibições — fica de fora, com a linha da proibição

Tudo abaixo aparece em A, em `fx.tsx` de A ou nos prompts lidos na tela, e é
exatamente o que `src/identidade/proibicoes.md` barra. É aqui que está a energia
dos reels virais daqueles vídeos, e é aqui que a marca escolhe não ir:

| o que a fonte pede | onde | proibição |
|---|---|---|
| ~30 partículas subindo no fundo do hook | A, modo hook + `Background.tsx` | `proibicoes.md:11` "explosão de partícula" |
| 2–3 orbes de brilho em caminho senoidal, *light sweep* periódico | A, modo hook | `:11` "brilho" |
| grid em gradiente à deriva | A, modo hook | `:11` "gradiente em elemento de interface" |
| molas com overshoot `{damping: 11, stiffness: 130, mass: 0.7}`, "punch, don't glide" | A, modo hook | `:11` "easing elástico" |
| `Shockwave` (anel de impacto que expande) | A, `src/scenes/fx.tsx` | `:11` partícula + brilho |
| `TypeText` (revelação caractere a caractere com cursor) | A, `src/scenes/fx.tsx` | `:14` "Revelar texto caractere a caractere" |
| *flash cut* entre cenas; "Blue Iris Wipes and Ring Tunnels" | A `Opener.tsx`; prompt `the-kinetic-marketing` | `:16` "Flash branco instantâneo e whip pan" |
| "motion blur burst 0 → 9 px" de quadro cheio | prompt do MoSidd, cena 1 do Netflix | `:7-8` nomeia `<CameraMotionBlur>` |
| *marker-yellow swipe* sobre o título | prompts do MoSidd (Vox / Macintosh) | `:19` "Um acento de cor por cena" — o amarelo seria o segundo saturado ao lado de `COR.acento` |
| "word that shatter-kicks off screen" | A, modo hook | `:11` partícula |

**Dois casos que não são proibição, são decisão do Rafael:**

1. **Highlight rolante da palavra ativa na legenda** (`highlightColor` de D).
   Tecnicamente é **um** acento com função, o que `proibicoes.md:19` permite —
   mas ele troca de palavra 2,45 vezes por segundo, que é um acento por palavra
   e não por cena. Não entra neste plano.
2. **"Never let a frame be static"** (A, modo hook). Na direção, A e
   `proibicoes.md:11` concordam: "tempo morto" já é proibido aqui. O que colide
   é o **meio** que A prescreve (partícula + brilho). O substituto legítimo para
   um hit visual a cada 0,4–0,8 s neste motor é **corte e tipo** — palavra
   entrando, bloco de legenda virando, cartela cobrindo — nunca efeito.

---

## 4. Tarefas

Todo comando roda em
`C:/Users/rafae/OneDrive/Desktop/Canastra Inteligencia/Agentes AI/Canastra-Content-Creator/instagram/remotion`.

Ordem = impacto sobre a qualidade percebida, não facilidade. A tarefa 1 é a mais
trabalhosa e a mais visível; a 7 é a mais barata e a menos visível.

As contagens de teste dos `Expected` são **aritmética** a partir da base de 85, não
medição: cada tarefa soma os `it` que ela acrescenta. Se o número real divergir,
conte os `it` antes de concluir que algo quebrou.

---

### Tarefa 1: a legenda ganha ponta de entrada e de saída, e contorno

**Files:**
- Modify: `src/identidade/tokens.ts:36-44` (o bloco `LEGENDA`)
- Modify: `src/motor/movimento.ts:34` (import) e fim do arquivo (funções novas)
- Modify: `src/motor/camadas/Legenda.tsx` (arquivo inteiro)
- Test: `tests/legenda.test.ts` (criar)

- [ ] **Step 1: escrever o teste que falha** — criar `tests/legenda.test.ts`

```ts
// Portao da camada de legenda: a gramatica de tempo dela e o contorno.
//
// Nao renderiza, pela mesma razao de `tests/textotela.test.ts`: `Legenda.tsx`
// importa `tipografia.ts`, que faz `loadFont` no topo do modulo e derruba o
// vitest em Node com `TypeError: Invalid URL`. Logo o que precisa de prova mora
// em `src/motor/movimento.ts`, que e puro.

import {describe, it, expect} from 'vitest';
import {estadoDeLegenda, pontasDeLegenda} from '../src/motor/movimento';
import {COR, LEGENDA, TEMPO} from '../src/identidade/tokens';

// Duracao mediana dos 38 blocos reais de projetos/01-private-label/props.json:
// min 10, mediana 19, max 38 frames.
const D = 19;

describe('pontasDeLegenda', () => {
  it('as pontas vem de tokens em SEGUNDOS, entao duram o mesmo em qualquer fps', () => {
    // A regra 3 das fontes: duracao se declara em segundos e se converte por
    // fps. Um bloco de 0,633 s tem 19 frames a 30 fps e 38 a 60 fps, e a ponta
    // tem que durar os mesmos milissegundos nos dois.
    for (const fps of [30, 60]) {
      const p = pontasDeLegenda(Math.round(0.633 * fps), fps);
      expect(p.entrada / fps).toBeCloseTo(LEGENDA.pontaEntradaSegundos, 2);
      expect(p.saida / fps).toBeCloseTo(LEGENDA.pontaSaidaSegundos, 2);
    }
  });

  it('a 30 fps a entrada e 2 frames e a saida 4', () => {
    expect(pontasDeLegenda(D, 30)).toEqual({entrada: 2, saida: 4});
  });

  it('num bloco curto as pontas cedem e nunca somam mais que a duracao', () => {
    // A alternativa -- deixar entrada e saida se sobreporem -- daria presenca
    // subindo e descendo no mesmo frame.
    for (const d of [1, 2, 3, 5, 10]) {
      const p = pontasDeLegenda(d, 30);
      expect(p.entrada).toBeGreaterThanOrEqual(1);
      expect(p.entrada + p.saida).toBeLessThanOrEqual(d);
    }
  });
});

describe('estadoDeLegenda', () => {
  it('o primeiro frame desenhado ja sai com 94,6% da presenca', () => {
    // A referencia medida tem 93% da massa de movimento no PRIMEIRO frame. Com
    // 2 frames de ponta e a curva de pouso, o primeiro frame desenhado da
    // 0,946079 -- o mais perto do medido sem cair em corte seco.
    expect(estadoDeLegenda(0, D, 30).presenca).toBeCloseTo(0.946079, 6);
    expect(estadoDeLegenda(0, D, 30).presenca).toBeGreaterThan(0.9);
  });

  it('o ULTIMO frame desenhado fecha em zero: a legenda nao sai por corte', () => {
    expect(estadoDeLegenda(D - 1, D, 30).presenca).toBeCloseTo(0, 9);
  });

  it('a saida cai por t^saidaExpoente ao longo dos 4 frames de ponta', () => {
    expect(estadoDeLegenda(15, D, 30).presenca).toBeCloseTo(
      1 - Math.pow(1 / 4, TEMPO.saidaExpoente),
      6,
    );
    expect(estadoDeLegenda(16, D, 30).presenca).toBeCloseTo(
      1 - Math.pow(2 / 4, TEMPO.saidaExpoente),
      6,
    );
    expect(estadoDeLegenda(17, D, 30).presenca).toBeCloseTo(
      1 - Math.pow(3 / 4, TEMPO.saidaExpoente),
      6,
    );
  });

  it('o hold fica cheio e parado', () => {
    for (let f = 1; f <= 14; f++) {
      expect(estadoDeLegenda(f, D, 30).presenca).toBeCloseTo(1, 9);
      expect(estadoDeLegenda(f, D, 30).escala).toBeCloseTo(1, 9);
    }
  });

  it('a escala e uma direcao so: de 1+overshoot a 1-overshoot, sem repique', () => {
    // Repique -- passar do alvo e voltar -- e easing elastico, e
    // `proibicoes.md` proibe. O elemento oficial de legenda do Remotion faz
    // 1 -> 1,03 -> 1, que sao duas direcoes; aqui nao.
    let anterior = Infinity;
    for (let f = 0; f < D; f++) {
      const s = estadoDeLegenda(f, D, 30).escala;
      expect(s).toBeLessThanOrEqual(anterior + 1e-9);
      expect(s).toBeLessThanOrEqual(1 + TEMPO.overshoot + 1e-9);
      expect(s).toBeGreaterThanOrEqual(1 - TEMPO.overshoot - 1e-9);
      anterior = s;
    }
  });

  it('fora do bloco o elemento nao existe', () => {
    expect(estadoDeLegenda(-1, D, 30).presenca).toBe(0);
    expect(estadoDeLegenda(D, D, 30).presenca).toBe(0);
    expect(estadoDeLegenda(D + 40, D, 30).presenca).toBe(0);
  });

  it('as tres fases aparecem na ordem, sem buraco', () => {
    const vistas: string[] = [];
    for (let f = 0; f < D; f++) {
      const fase = estadoDeLegenda(f, D, 30).fase;
      expect(fase).not.toBe('antes');
      expect(fase).not.toBe('depois');
      if (vistas[vistas.length - 1] !== fase) vistas.push(fase);
    }
    expect(vistas).toEqual(['entrada', 'hold', 'saida']);
  });
});

describe('contorno da legenda', () => {
  it('o divisor de contorno e 7, o numero do elemento oficial do Remotion', () => {
    expect(LEGENDA.contornoDivisor).toBe(7);
    expect(LEGENDA.corpoEm1080 / LEGENDA.contornoDivisor).toBeCloseTo(11.142857, 6);
  });

  it('a cor do contorno e o preto da paleta, nao #000000', () => {
    expect(LEGENDA.corContorno).toBe(COR.preto);
    expect(LEGENDA.corContorno).not.toBe('#000000');
  });
});

describe('o token que ninguem lia', () => {
  it('LEGENDA.corte nao existe mais: a decisao que ele documentava foi revertida', () => {
    // `corte: 'seco'` ficou 1 rodada no arquivo sem nenhum leitor (`grep -rn
    // "LEGENDA.corte" src/` = 0). Token que ninguem le e decisao que ninguem
    // aplica.
    expect('corte' in LEGENDA).toBe(false);
  });
});
```

- [ ] **Step 2: rodar o teste e conferir que falha**

Run: `npx vitest run tests/legenda.test.ts`
Expected: FALHA. `TypeError: estadoDeLegenda is not a function` e
`pontasDeLegenda is not a function`; as asserções de `LEGENDA.pontaEntradaSegundos`,
`contornoDivisor` e `corContorno` recebem `undefined`; a de `'corte' in LEGENDA`
recebe `true`.

- [ ] **Step 3: trocar o bloco `LEGENDA` em `src/identidade/tokens.ts`**

Substituir as linhas 36-44 por:

```ts
// Legenda, medida em referencia real: 2,45 blocos/s, 1,7 palavras/bloco.
export const LEGENDA = {
  maxPalavras: 2,
  duracaoMinFrames: 10,        // 0,33s a 30fps
  // PONTAS EM SEGUNDOS, e ASSIMETRICAS de proposito. Cada metade tem fonte:
  //
  //   entrada 0,067 s = 2 frames a 30 fps. A referencia medida tem 93% da massa
  //   de movimento no PRIMEIRO frame; com a curva de pouso e 2 frames de ponta
  //   o primeiro frame desenhado sai com 94,6% -- o mais perto que se chega do
  //   medido sem voltar a ser corte seco.
  //
  //   saida 0,133 s = 4 frames a 30 fps. Este numero NAO e nosso: e o do
  //   elemento oficial de legenda do Remotion (`Popping Word Captions`,
  //   @JonnyBurger), que usa `min(4, duracao/2)` frames de ponta. A medicao dos
  //   93% cobria a ENTRADA; para a saida nao havia medida nenhuma neste
  //   projeto, e vale o numero do fornecedor em vez de um escolhido no olho.
  //
  // Por que nao usar a mesma ponta nas duas: com 2 frames de saida, a queda por
  // t^2,4 pula de 0,8105 para 0 em UM frame -- continuaria sendo corte. Medido.
  pontaEntradaSegundos: 0.067,
  pontaSaidaSegundos: 0.133,
  entrelinha: 0.96,
  corpoEm1080: 78,
  cor: COR.creme,
  // CONTORNO, nao brilho. `WebkitTextStroke` com `paintOrder: 'stroke fill'`
  // desenha o traco ATRAS do preenchimento, entao o desenho da letra nao muda:
  // ela so engrossa para fora. O divisor 7 e o do elemento oficial de legenda
  // do Remotion (corpo 80 -> 11,4 px); no nosso corpo de 78 da 11,14 px.
  //
  // A sombra continua: ela separa a legenda do fundo, o contorno define a
  // letra. Sao dois trabalhos diferentes sobre video em movimento.
  contornoDivisor: 7,
  corContorno: COR.preto,
} as const;
```

(`corte: 'seco'` sai. `grep -rn "LEGENDA.corte" src/` devolvia 0 leitores.)

- [ ] **Step 4: acrescentar a gramática de legenda em `src/motor/movimento.ts`**

Trocar a linha 34:

```ts
import {LEGENDA, PUSH, TEMPO} from '../identidade/tokens';
```

E acrescentar no FIM do arquivo, depois de `push()`:

```ts
// ---------------------------------------------------------------------------
// legenda
//
// A legenda NAO usa `fases()`. Ali a ponta e `TEMPO.entrada` (12 frames, 0,4 s a
// 30 fps) ou um terco da janela -- e o bloco de legenda mediano dura 19 frames,
// entao a entrada comeria 6 frames, 0,2 s, para uma palavra que fica menos de
// 0,7 s na tela. A referencia medida tem 93% da massa de movimento no PRIMEIRO
// frame.
//
// Por isso a legenda tem pontas proprias, e elas sao assimetricas: entrada de
// `LEGENDA.pontaEntradaSegundos` (nossa medida) e saida de
// `LEGENDA.pontaSaidaSegundos` (numero do elemento oficial do Remotion). Ver o
// comentario daqueles tokens.

export type PontasLegenda = {entrada: number; saida: number};

/**
 * Quantos frames de entrada e de saida um bloco de `duracaoBloco` frames recebe.
 *
 * Nenhuma ponta passa da metade do bloco, e as duas juntas nunca passam do
 * bloco: um bloco de 2 frames aparece num e sai no outro, em vez de ter entrada
 * e saida se sobrepondo no mesmo frame.
 */
export function pontasDeLegenda(duracaoBloco: number, fps: number): PontasLegenda {
  const d = Math.max(0, Math.floor(duracaoBloco));
  const folga = Math.max(1, Math.floor(d / 2));
  const entrada = Math.min(
    Math.max(1, Math.round(LEGENDA.pontaEntradaSegundos * fps)),
    folga,
  );
  const saida = Math.min(
    Math.max(1, Math.round(LEGENDA.pontaSaidaSegundos * fps)),
    d - entrada,
  );
  return {entrada, saida};
}

/**
 * Estado de UM bloco de legenda, no tempo local do bloco.
 *
 * Mesma forma de `Estado` que `progresso`, e a mesma curva de pouso e o mesmo
 * expoente de saida -- o motor tem UMA gramatica de movimento, com duracoes
 * diferentes por camada, nao duas gramaticas.
 */
export function estadoDeLegenda(
  frameLocal: number,
  duracaoBloco: number,
  fps: number,
): Estado {
  const d = Math.max(0, Math.floor(duracaoBloco));
  if (frameLocal < 0) return {fase: 'antes', presenca: 0, escala: 1 + TEMPO.overshoot};
  if (frameLocal >= d) return {fase: 'depois', presenca: 0, escala: 1 - TEMPO.overshoot};

  const p = pontasDeLegenda(d, fps);
  // O `+1` nas duas pontas normaliza pelo ULTIMO FRAME DESENHADO, nao pelo
  // primeiro que nao e desenhado. Sem ele o primeiro frame sairia com presenca
  // 0 (um frame invisivel gasto) e o ultimo com presenca sobrando (um pop de
  // saida) -- o mesmo defeito que a tarefa 2 conserta em `progresso`.
  const entrada = POUSO(Math.min(1, (frameLocal + 1) / p.entrada));
  const inicioSaida = d - p.saida;
  const pSaida =
    p.saida === 0 || frameLocal < inicioSaida
      ? 0
      : Math.min(1, (frameLocal - inicioSaida + 1) / p.saida);
  const queda = Math.pow(pSaida, TEMPO.saidaExpoente);

  const fase: Fase =
    frameLocal < p.entrada ? 'entrada' : frameLocal < inicioSaida ? 'hold' : 'saida';

  return {
    fase,
    presenca: Math.min(entrada, 1 - queda),
    escala: 1 + TEMPO.overshoot * (1 - entrada) - TEMPO.overshoot * queda,
  };
}
```

- [ ] **Step 5: rodar o teste e conferir que passa**

Run: `npx vitest run tests/legenda.test.ts`
Expected: PASS, 13 testes.

- [ ] **Step 6: fazer a camada ler a gramática** — reescrever `src/motor/camadas/Legenda.tsx` inteiro

```tsx
// Camada de legenda.
//
// ---------------------------------------------------------------------------
// PONTA CURTA, NAO CORTE SECO (mudou em 30/09/2026)
//
// Ate esta data esta camada nao animava NADA: `blocos.find(...)`, e um `<span>`
// cujo estilo nao dependia do frame. Entrava por corte e saia por corte, e no
// silencio entre blocos apagava num frame sobre video em movimento.
//
// A defesa escrita era uma medida real -- a referencia tem 93% da massa de
// movimento no primeiro frame. Mas 93% no primeiro frame descreve um pop de 1-2
// frames com 7% de assentamento; nao descreve zero. E a medida cobria a
// ENTRADA: para a saida nao havia medida nenhuma.
//
// Agora a entrada tem 2 frames (94,6% de presenca ja no primeiro frame
// desenhado, contra os 93% medidos) e a saida tem 4, que e o numero do elemento
// oficial de legenda do Remotion. Tudo em `movimento.ts` / `estadoDeLegenda`,
// porque o que precisa de prova nao pode morar num `.tsx`.
//
// ---------------------------------------------------------------------------
// CONTORNO E SOMBRA FAZEM TRABALHOS DIFERENTES
//
// A sombra (`SOMBRA.sobreVideo`: dy 14, blur 26, op 0,42) separa a legenda do
// fundo. O contorno (`corpo/7` = 11,14 px a 78 px) define a letra. Sobre imagem
// em movimento os dois sao necessarios, e `paintOrder: 'stroke fill'` garante
// que o traco fica ATRAS do preenchimento -- a forma da letra nao muda.
//
// CONFERENCIA OBRIGATORIA: contorno grosso em corpo pequeno fecha contra-forma
// de `a`, `e` e `o`. Depois de mexer no `contornoDivisor`, confira num RECORTE
// AMPLIADO da faixa de legenda, nao na imagem inteira -- e a licao 13 do
// CLAUDE.md.
//
// ---------------------------------------------------------------------------
// DESLOCAMENTO -- o detalhe que erra a legenda inteira por 1,14 s:
// os blocos vem da transcricao da FONTE, entao os frames deles estao no tempo
// do arquivo original. A composicao, porem, comeca depois do corte do ar morto:
// o frame 0 da peca e o frame `cortarAntesFrames` da fonte. Por isso o frame
// corrente e convertido para tempo-da-fonte antes de procurar o bloco. Quem
// passar blocos ja realinhados usa `deslocamentoFrames={0}`.

import {useCurrentFrame, useVideoConfig} from 'remotion';
import React from 'react';
import {LEGENDA, TIPO} from '../../identidade/tokens';
// `PILHA.corpo` no lugar de `TIPO.corpo.familia` cru: importar daqui tambem
// PUXA o carregamento das tres familias (o modulo tem efeito colateral), entao
// esta camada nao depende de alguem ter lembrado de importar a tipografia la em
// cima. Antes de 30/09/2026 nao havia carregamento nenhum e esta legenda saia
// em Times New Roman sem avisar.
import {PILHA} from '../../identidade/tipografia';
import {estadoDeLegenda} from '../movimento';
import type {Bloco} from '../../legenda/agrupar';
import type {Caixa} from '../layout';

export const Legenda: React.FC<{
  blocos: Bloco[];
  caixa: Caixa;
  escala: number;
  deslocamentoFrames?: number;
}> = ({blocos, caixa, escala, deslocamentoFrames = 0}) => {
  const {fps} = useVideoConfig();
  const f = useCurrentFrame() + deslocamentoFrames;
  const b = blocos.find((x) => f >= x.inicioFrame && f < x.fimFrame);
  if (!b) return null;

  const e = estadoDeLegenda(f - b.inicioFrame, b.fimFrame - b.inicioFrame, fps);
  const corpo = LEGENDA.corpoEm1080 * escala;

  return (
    <div
      style={{
        position: 'absolute',
        left: caixa.x,
        top: caixa.y,
        width: caixa.largura,
        height: caixa.altura,
        display: 'flex',
        alignItems: 'flex-end',
        justifyContent: 'center',
      }}
    >
      <span
        style={{
          fontFamily: PILHA.corpo,
          fontWeight: TIPO.corpo.peso,
          fontSize: corpo,
          lineHeight: LEGENDA.entrelinha,
          color: LEGENDA.cor,
          textAlign: 'center',
          // `scale` como propriedade individual, nao string `transform`: e o que
          // a skill oficial `remotion-markup` pede, para o valor continuar
          // editavel no Studio.
          //
          // `display: inline-block` porque `scale` nao vale em caixa inline.
          // Origem no rodape: a ultima linha fica na mesma linha de base em
          // qualquer escala, entao a legenda nao "pula" ao entrar.
          display: 'inline-block',
          opacity: e.presenca,
          scale: e.escala,
          transformOrigin: 'center bottom',
          WebkitTextStroke: `${corpo / LEGENDA.contornoDivisor}px ${LEGENDA.corContorno}`,
          paintOrder: 'stroke fill',
          textShadow: `0 ${14 * escala}px ${26 * escala}px rgba(0,0,0,.42)`,
        }}
      >
        {b.texto}
      </span>
    </div>
  );
};
```

- [ ] **Step 7: rodar a suíte inteira e o typecheck**

Run: `npx vitest run`
Expected: `Test Files 7 passed (7)` · `Tests 98 passed (98)` (85 de antes + 13 novos)

Run: `npm run tsc`
Expected: nenhuma saída (exit 0).

- [ ] **Step 8: conferir no pixel, porque nenhum teste renderiza**

Run:
```
npx remotion render src/index.ts Reel out/t1-legenda.mp4 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public \
  --frames=300-330
```
Expected: MP4 de 31 frames. Depois, um still do primeiro frame de um bloco e um
do último:
```
npx remotion still src/index.ts Reel out/t1-f300.png --frame=300 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
```
Confira **num recorte ampliado da faixa de legenda**: contorno presente,
contra-forma de `a`/`e`/`o` aberta, e o rodapé do texto na mesma altura nos dois
stills.

- [ ] **Step 9: commit**

```bash
git add src/identidade/tokens.ts src/motor/movimento.ts src/motor/camadas/Legenda.tsx tests/legenda.test.ts
git commit -m "Legenda: ponta de 2/4 frames e contorno, em vez de corte seco"
```

---

### Tarefa 2: a saída chega a zero no último frame desenhado

**Files:**
- Modify: `src/motor/movimento.ts:159-162`
- Test: `tests/textotela.test.ts:142-149` (ajustar) e um `it` novo depois de `:159`

- [ ] **Step 1: escrever o teste que falha** — acrescentar em
`tests/textotela.test.ts`, dentro do `describe('progresso')`, logo depois do
teste `'a saida cai monotonicamente ate 0'` (linha 159):

```ts
  it('o ULTIMO frame DESENHADO fecha em zero, e nao a 18,85%', () => {
    // O DEFEITO QUE ESTE TESTE PEGA, e que os outros deixaram passar:
    //
    // a saida era normalizada pelo primeiro frame NAO desenhado. Medido numa
    // janela de 36 frames, presenca nos seis ultimos frames desenhados:
    //   0.8105  0.7257  0.6221  0.4986  0.3544  0.1885
    // e o frame seguinte nunca e desenhado (`TextoTela.tsx` devolve null em
    // `t >= duracaoCena`). Ou seja o elemento desaparecia de 18,85% de
    // opacidade para zero num frame -- o "sai seco" que a regra 6 proibe. Na
    // cartela isso e uma tela cheia de terra sumindo a 19%.
    //
    // O teste vizinho passava porque media `progresso(duracao)`, que e o ramo
    // 'depois' -- nunca o ultimo frame renderizado.
    for (const duracao of [36, 51, 66, 90]) {
      const janela = {inicio: 0, duracao};
      expect(progresso(duracao - 1, janela).presenca).toBeCloseTo(0, 9);
      expect(progresso(duracao - 1, janela).escala).toBeCloseTo(
        1 - TEMPO.overshoot,
        9,
      );
    }
  });
```

- [ ] **Step 2: rodar o teste e conferir que falha**

Run: `npx vitest run tests/textotela.test.ts -t "ULTIMO frame DESENHADO"`
Expected: FALHA. `expected 0.18849... to be close to 0`.

- [ ] **Step 3: consertar `src/motor/movimento.ts`**

Substituir as linhas 159-162:

```ts
  // Saida: 1 -> 0 acelerando por t^saidaExpoente.
  //
  // O `+1` normaliza pelo ULTIMO FRAME DESENHADO, nao pelo primeiro que nao e
  // desenhado. Sem ele, medido numa janela de 36 frames: t=35 saia com presenca
  // 0,1885 e t=36 nunca e desenhado (`TextoTela.tsx` devolve null em
  // `t >= duracaoCena`) -- o elemento desaparecia de 18,85% de opacidade para
  // zero num frame. O expoente 2,4 AMPLIFICA o erro: com saida linear o residuo
  // seria 8,33%.
  const pSaida =
    f.saida === 0 || t < inicioSaida
      ? 0
      : Math.min(1, (t - inicioSaida + 1) / f.saida);
  const queda = Math.pow(pSaida, TEMPO.saidaExpoente);
```

- [ ] **Step 4: ajustar o teste vizinho, que media a metade pelo relógio antigo**

Em `tests/textotela.test.ts`, no teste `'a saida e ACELERADA: na metade ainda
esta quase cheia'` (linhas 142-149), substituir o corpo por:

```ts
  it('a saida e ACELERADA: na metade ainda esta quase cheia', () => {
    const inicioSaida = 10 + 60 - TEMPO.entrada;
    // `pSaida` = 0,5 cai no frame (inicioSaida + entrada/2 - 1), porque a saida
    // e normalizada pelo ULTIMO frame desenhado -- ver o comentario em
    // `movimento.ts`. Sem o `-1` isto mede 7/12 e nao 6/12.
    const meio = inicioSaida + TEMPO.entrada / 2 - 1;
    const esperado = 1 - Math.pow(0.5, TEMPO.saidaExpoente);
    expect(progresso(meio, j).presenca).toBeCloseTo(esperado, 6);
    // e isso e bem mais lento que linear no comeco
    expect(progresso(meio, j).presenca).toBeGreaterThan(0.75);
  });
```

Valores medidos: `esperado` = 0,810535 e `progresso(63, j).presenca` = 0,810535.

- [ ] **Step 5: rodar a suíte inteira**

Run: `npx vitest run`
Expected: `Test Files 7 passed (7)` · `Tests 99 passed (99)`

Nenhum outro teste muda: a entrada não foi tocada (`progresso(10, j).presenca` =
0, `escala` = 1,03), o hold segue cheio de t=12 a t=47, e
`progresso(10 + 60, j).presenca` segue 0 pelo ramo `'depois'`.

- [ ] **Step 6: conferir no pixel** — o defeito era de UM frame, então o still
tem que ser exatamente o último frame da cena da manchete. Com
`manchete.inicioFrame = 104` e `cortarAntesFrames = 34`, a cena começa no frame
70 da peça; `duracaoDaFrase('SUA PRÓPRIA MARCA DE CAFÉ')` dá a duração.

Run:
```
npx remotion render src/index.ts Reel out/t2-saida.mp4 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public \
  --frames=120-145
```
Expected: os últimos frames da cartela terminam em terra transparente, sem um
frame de terra a ~19% de opacidade antes do corte.

- [ ] **Step 7: commit**

```bash
git add src/motor/movimento.ts tests/textotela.test.ts
git commit -m "Movimento: a saida fecha em zero no ultimo frame desenhado"
```

---

### Tarefa 3: margens em fração do eixo próprio, topo em 5%

**Files:**
- Modify: `src/motor/layout.ts:14-27`
- Test: `tests/layout.test.ts` (dois `it` novos)

- [ ] **Step 1: escrever os testes que falham** — acrescentar em
`tests/layout.test.ts`, dentro do `describe('layout')`:

```ts
  it('as margens sao a MESMA porcentagem do eixo proprio em todo formato', () => {
    // O DEFEITO: um `k` unico derivado da LARGURA escalava tambem as margens
    // verticais. Medido antes do conserto, base efetiva como % da ALTURA:
    //   1080x1920 -> 16,15%   1080x1080 -> 28,70%   1920x1080 -> 51,03%
    // No 16:9 metade do quadro era margem e a area segura ficava com 368,9 px
    // de altura -- exatamente o numero que `texto-forma.ts` registra como
    // "texto de borda a borda".
    for (const [w, h] of [[1080, 1920], [1080, 1080], [1920, 1080]]) {
      const z = layout({largura: w, altura: h, razaoFonte: 9 / 16});
      const base = h - (z.seguro.y + z.seguro.altura);
      expect(z.seguro.y / h).toBeCloseTo(0.05, 6);
      expect(base / h).toBeCloseTo(0.16, 6);
      expect(z.seguro.x / w).toBeCloseTo(160 / 1080, 6);
    }
  });

  it('a margem de topo respeita o piso de 5% da convencao title-safe', () => {
    // Eram 90 px em 1920 = 4,69%, abaixo do piso da faixa 5-8%.
    for (const [w, h] of [[1080, 1920], [1080, 1080], [1920, 1080]]) {
      const z = layout({largura: w, altura: h, razaoFonte: 9 / 16});
      expect(z.seguro.y / h).toBeGreaterThanOrEqual(0.05 - 1e-9);
    }
  });
```

- [ ] **Step 2: rodar os testes e conferir que falham**

Run: `npx vitest run tests/layout.test.ts`
Expected: FALHA nos dois. No primeiro, `expected 0.046875 to be close to 0.05`;
no segundo, `expected 0.046875 to be greater than or equal to 0.05`.

- [ ] **Step 3: consertar `src/motor/layout.ts`**

Substituir as linhas 14-27 por:

```ts
// MARGENS DE AREA SEGURA, EM FRACAO DO EIXO QUE CADA UMA CORTA.
//
// Antes de 30/09/2026 eram pixeis a 1080x1920 escalados por um `k` unico
// derivado da LARGURA. Medido rodando `layout()` com razaoFonte 9/16, a base
// efetiva como porcentagem da ALTURA:
//
//   1080x1920 ... 310,0 px = 16,15%
//   1080x1080 ... 310,0 px = 28,70%
//   1920x1080 ... 551,1 px = 51,03%   (area segura de 1351,1 x 368,9)
//
// No 1:1 quase um terco do quadro era margem de baixo; no 16:9 metade. E os 368,9
// px de altura do 16:9 sao exatamente o numero que `texto-forma.ts:205-206`
// registra como "texto de borda a borda, o oposto de respiro maior" -- o sintoma
// que `linhasDeFolga` tenta consertar nasce desta linha, nao da cartela.
//
// Agora cada margem e fracao do eixo que ela corta, entao a porcentagem e a
// MESMA nos tres formatos:
//
//   topo   5,00%  piso da faixa title-safe 5-8%. Eram 90 px = 4,69% a 1920 de
//                 altura, abaixo do piso; em 1920 de altura da 96,0 px.
//   base  16,00%  eram 310 px = 16,15% a 1920 de altura. Mesma faixa, agora
//                 constante.
//   lado  14,81%  160 px a 1080 de largura. ESTE NUMERO FOI ESCOLHIDO NO OLHO e
//                 nunca medido: esta fora da faixa 5-8% da convencao e fica
//                 porque e o que as pecas aprovadas usaram. Mudar a largura da
//                 manchete e decisao estetica, nao conserto -- entao fica, mas
//                 sem se chamar "medida".
const MARGEM = {topo: 0.05, base: 0.16, lado: 160 / 1080};

export function layout(
  {largura, altura, razaoFonte}:
  {largura: number; altura: number; razaoFonte: number}
): Zonas {
  // `kx` NAO escala margem nenhuma. Ele sobra para as folgas em pixel da caixa
  // de legenda (16 e 32 px a 1080 de largura), que sao respiro contra a borda do
  // VIDEO e por isso acompanham a largura.
  const kx = largura / 1080;
  const seguro: Caixa = {
    x: MARGEM.lado * largura,
    y: MARGEM.topo * altura,
    largura: largura * (1 - 2 * MARGEM.lado),
    altura: altura * (1 - MARGEM.topo - MARGEM.base),
  };
```

E nas linhas da caixa de legenda (antes 68-73), trocar `k` por `kx`:

```ts
  const legenda: Caixa = {
    x: Math.max(seguro.x, video.x + 16 * kx),
    y: seguro.y + seguro.altura - alturaLegenda,
    largura: Math.min(seguro.largura, video.largura - 32 * kx),
    altura: alturaLegenda,
  };
```

- [ ] **Step 4: rodar a suíte inteira**

Run: `npx vitest run`
Expected: `Test Files 7 passed (7)` · `Tests 101 passed (101)`

Todas as asserções existentes continuam válidas — conferido rodando o layout
patchado contra cada uma:

| asserção existente | sob o patch |
|---|---|
| `layout.test.ts:5-9` vídeo ocupa 1080 no 9:16 | `video.largura` = 1080 |
| `layout.test.ts:19-28` legenda dentro do seguro nos 3 formatos | verdadeiro nos 3 |
| `layout.test.ts:30-35` manchete não cruza o vídeo no 1:1 | `false` |
| `textotela.test.ts:376-388` caixa dentro do seguro | verdadeiro nos 3 × 2 modos |
| `textotela.test.ts:390-407` bloco cabe na caixa | verdadeiro nos 3 × 2 modos × 3 textos |
| `textotela.test.ts:437-439` cartela mais alta que sobre | `true` |
| `textotela.test.ts:458-469` cartela guarda 1 linha de folga | `true` nos 3 |
| `textotela.test.ts:471-475` cartela respira mais | `0,559 > 0,000` |
| `textotela.test.ts:409-418` texto longo recebe corpo menor | `114 < 258` |
| `textotela.test.ts:482-487` quebram diferente ou corpo diferente | `true` |

Efeito colateral medido e desejado: o corpo da cartela sobe de 104 para **123 px**
no Feed 1:1 e de 111 para **156 px** no 16:9, porque a área segura deixou de ser
comida pela margem.

- [ ] **Step 5: conferir no pixel os dois formatos**

Run:
```
npx remotion still src/index.ts Reel out/t3-reel.png --frame=120 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
npx remotion still src/index.ts Feed out/t3-feed.png --frame=120 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
```
Expected: no Feed a cartela vem visivelmente maior (corpo 104 → 123 px) e a
legenda **desce** 137,2 px — de `y = 597,2` para `y = 734,4`, ficando a 172,8 px
da borda de baixo em vez de 310,0. No Reel a legenda desce 2,8 px (1302,8 →
1305,6) e a margem de topo sobe de 90,0 para 96,0 px.

- [ ] **Step 6: commit**

```bash
git add src/motor/layout.ts tests/layout.test.ts
git commit -m "Layout: margem em fracao do eixo proprio, topo no piso de 5%"
```

---

### Tarefa 4: o push não move mais o canto do bloco, e vira propriedade `scale`

**Files:**
- Modify: `src/motor/camadas/texto-forma.ts` (tipo `Forma`, retorno de `formaTextoTela`, duas funções novas)
- Modify: `src/motor/camadas/TextoTela.tsx:139-142` e `:180`
- Test: `tests/textotela.test.ts` (um `describe` novo no fim)

**O que esta tarefa NÃO faz, e por quê.** O bloco de texto é ajustado para
**preencher** a caixa (`texto-forma.ts:216-241` maximiza o corpo), então qualquer
push > 1 leva o bloco 4% além da caixa. Tentei reservar o push na busca de corpo
(`m.larguraBloco * PUSH.para <= caixa.largura`) e medi o resultado: no 9:16 o
corpo do `sobreImagem` **não muda** (90), a cartela cai de 123 para 118 — mas no
Feed 1:1 o `sobreImagem` **desaba de 44 para 15 px**, porque a coluna de 274,7 px
faz a quebra gulosa oscilar e a rede `while (corpo > 1 && !cabe(corpo)) corpo--`
desce até achar um corpo em que cabe. Reserva de push na busca de corpo é
**rejeitada por medição**, e o vazamento de 4% à direita e embaixo fica para
depois da decisão de V5 (§3.1). Esta tarefa fecha só o que o `transformOrigin`
resolve sozinho, que é exatamente o defeito V4: o topo do bloco.

- [ ] **Step 1: escrever o teste que falha** — acrescentar no fim de
`tests/textotela.test.ts`:

```ts
// ---------------------------------------------------------------------------
describe('o push nao move o canto de ancoragem do bloco', () => {
  const texto = 'CAFE ESPECIAL DA SERRA DA CANASTRA';

  it('a origem do push e o canto superior esquerdo da caixa, nos dois modos', () => {
    const z = zonasDe(1080, 1920);
    for (const modo of ['sobreImagem', 'cartela'] as const) {
      expect(formaTextoTela({texto, modo, zonas: z}).origemPush).toBe('left top');
    }
  });

  it('o topo e a esquerda do bloco nao se movem com o push', () => {
    // O DEFEITO: `TextoTela.tsx` escalava o bloco por PUSH.para em torno do
    // CENTRO da caixa. Como o texto e alinhado a esquerda, escalar do centro
    // arrasta a borda esquerda para FORA: medido no 9:16, x ia de 160,0 para
    // 144,8 e o topo de 96,0 para 89,1 px = 4,64% da altura -- abaixo do piso de
    // 5% que `layout()` acabou de garantir. O push comia a margem.
    for (const [w, h] of FORMATOS) {
      const z = zonasDe(w, h);
      for (const modo of ['sobreImagem', 'cartela'] as const) {
        const f = formaTextoTela({texto, modo, zonas: z});
        const antes = caixaDoBloco(f);
        const depois = blocoComPush(f, PUSH.para);
        // esquerda e ponto fixo
        expect(depois.x).toBeCloseTo(antes.x, 6);
        // topo nunca SOBE: ancorado no topo fica parado, centrado desce
        expect(depois.y).toBeGreaterThanOrEqual(antes.y - 1e-9);
        // e em nenhum caso invade a margem de 5%
        expect(depois.y / h).toBeGreaterThanOrEqual(0.05 - 1e-9);
      }
    }
  });

  it('o bloco cresce, nao anda: a escala multiplica as duas dimensoes', () => {
    const z = zonasDe(1080, 1920);
    const f = formaTextoTela({texto, modo: 'sobreImagem', zonas: z});
    const antes = caixaDoBloco(f);
    const depois = blocoComPush(f, PUSH.para);
    expect(depois.largura).toBeCloseTo(antes.largura * PUSH.para, 6);
    expect(depois.altura).toBeCloseTo(antes.altura * PUSH.para, 6);
  });

  it('push de 1 nao move nada', () => {
    const z = zonasDe(1080, 1080);
    for (const modo of ['sobreImagem', 'cartela'] as const) {
      const f = formaTextoTela({texto, modo, zonas: z});
      const antes = caixaDoBloco(f);
      const depois = blocoComPush(f, 1);
      expect(depois).toEqual(antes);
    }
  });
});
```

E acrescentar `caixaDoBloco` e `blocoComPush` ao import da linha 27:

```ts
import {
  blocoComPush,
  caixaDoBloco,
  duracaoDaFrase,
  duracaoPorPalavra,
  formaTextoTela,
  quebrar,
} from '../src/motor/camadas/texto-forma';
```

- [ ] **Step 2: rodar o teste e conferir que falha**

Run: `npx vitest run tests/textotela.test.ts -t "push nao move"`
Expected: FALHA. `caixaDoBloco is not a function` e `blocoComPush is not a
function`; a asserção de `origemPush` recebe `undefined`.

- [ ] **Step 3: acrescentar a geometria em `src/motor/camadas/texto-forma.ts`**

No tipo `Forma` (linhas 69-88), acrescentar antes de `alinhaHorizontal`:

```ts
  /**
   * `transform-origin` do push de camera.
   *
   * `left top` nos dois modos, e isso e carregando: o texto e alinhado a
   * ESQUERDA (`alinhaHorizontal`), entao escalar em torno do CENTRO da caixa
   * arrasta a borda esquerda para fora dela. Medido no 9:16: com origem no
   * centro, o x do bloco ia de 160,0 para 144,8 px e o topo de 96,0 para 89,1
   * -- 4,64% da altura, abaixo do piso title-safe de 5%. Com origem no canto, o
   * canto e ponto fixo e o bloco so CRESCE.
   */
  origemPush: OrigemPush;
```

Acrescentar o tipo, perto de `SombraPosta` (antes de `Forma`):

```ts
export type OrigemPush = 'left top' | 'center center';
```

No `return` de `formaTextoTela` (linhas 270-307), acrescentar antes de
`alinhaHorizontal: 'flex-start',`:

```ts
    origemPush: 'left top',
```

E acrescentar no FIM do arquivo:

```ts
// ---------------------------------------------------------------------------
// onde o bloco de texto fica, antes e depois do push
//
// Estas duas funcoes existem para que o efeito do push seja PROVAVEL em Node.
// Antes delas o push era uma string de CSS dentro do `.tsx` e ninguem media o
// que ele fazia com a margem -- foi assim que o topo do bloco passou a viver em
// 4,33% da altura com o teste verde.

/** A caixa do BLOCO DE TEXTO dentro de `forma.caixa`, antes do push. */
export function caixaDoBloco(forma: Forma): Caixa {
  const y =
    forma.alinhaVertical === 'center'
      ? forma.caixa.y + (forma.caixa.altura - forma.alturaBloco) / 2
      : forma.caixa.y;
  return {
    x: forma.caixa.x,
    y,
    largura: forma.larguraBloco,
    altura: forma.alturaBloco,
  };
}

/**
 * Onde o bloco de texto fica depois de um push de `escala`.
 *
 * O push escala o CONTAINER (`forma.caixa`) em torno de `forma.origemPush`, e o
 * bloco anda junto. Com `left top` o canto superior esquerdo da caixa e ponto
 * fixo: um bloco ancorado ali nao se move, e um bloco centrado verticalmente
 * desce -- nunca sobe para dentro da margem de topo.
 */
export function blocoComPush(forma: Forma, escala: number): Caixa {
  const b = caixaDoBloco(forma);
  const fx =
    forma.origemPush === 'left top'
      ? forma.caixa.x
      : forma.caixa.x + forma.caixa.largura / 2;
  const fy =
    forma.origemPush === 'left top'
      ? forma.caixa.y
      : forma.caixa.y + forma.caixa.altura / 2;
  return {
    x: fx + (b.x - fx) * escala,
    y: fy + (b.y - fy) * escala,
    largura: b.largura * escala,
    altura: b.altura * escala,
  };
}
```

- [ ] **Step 4: rodar o teste e conferir que passa**

Run: `npx vitest run tests/textotela.test.ts -t "push nao move"`
Expected: PASS, 4 testes.

- [ ] **Step 5: fazer o `.tsx` ler `origemPush` e usar a propriedade `scale`**

Em `src/motor/camadas/TextoTela.tsx`, trocar as linhas 139-142 por:

```ts
          // Push de camera lento sobre o bloco inteiro, nunca impacto.
          //
          // `scale` como propriedade individual, nao string `transform`: e o que
          // a skill oficial `remotion-markup` pede, para o valor continuar
          // editavel no Studio.
          //
          // A origem vem de `texto-forma.ts` e nao esta aqui de proposito: ela e
          // decisao de GEOMETRIA e tem teste. Ver `blocoComPush`.
          scale: push(t, duracaoCena),
          transformOrigin: forma.origemPush,
```

E a linha 180, no `<span>` de cada palavra, por:

```ts
                      // Pouso: entra 3% grande, assenta em 100%, sai em 97%.
                      // Uma direcao so, do primeiro ao ultimo frame -- repique
                      // seria easing elastico, e isso e proibido.
                      //
                      // Propriedade `scale`, nao string `transform`: mesma razao
                      // do push acima. Funciona sem `display: inline-block`
                      // porque cada palavra e filha de um container `flex`, e
                      // filho de flex e blockificado.
                      scale: e.escala,
```

- [ ] **Step 6: rodar a suíte inteira e o typecheck**

Run: `npx vitest run`
Expected: `Test Files 7 passed (7)` · `Tests 105 passed (105)`

Run: `npm run tsc`
Expected: nenhuma saída (exit 0).

- [ ] **Step 7: conferir no pixel que a escala não morreu**

A troca de `transform: scale()` por `scale:` é o tipo de mudança que o teste não
vê: se o React não passasse a propriedade, o pouso e o push simplesmente
deixariam de existir e o vitest continuaria verde. Então compare dois stills do
MESMO frame, antes e depois:

```
npx remotion still src/index.ts Reel out/t4-f072.png --frame=72 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
npx remotion still src/index.ts Reel out/t4-f130.png --frame=130 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
```
Expected: no frame 72 (2 frames depois do início da cena) as primeiras palavras
ainda estão visivelmente maiores que no frame 130. Se os dois stills tiverem o
texto do mesmo tamanho, a propriedade `scale` não está sendo aplicada — volte
para a string `transform` e registre a lição.

- [ ] **Step 8: commit**

```bash
git add src/motor/camadas/texto-forma.ts src/motor/camadas/TextoTela.tsx tests/textotela.test.ts
git commit -m "Push com origem no canto: para de comer a margem de topo"
```

---

### Tarefa 5: `premountFor={fps}` no vídeo e schema zod nas composições

**Files:**
- Create: `src/motor/esquema.ts`
- Create: `tests/esquema.test.ts`
- Modify: `src/motor/camadas/Fonte.tsx`
- Modify: `src/motor/PecaVideo.tsx:58-59` e `:68-94` (tipos) e `:96-98`
- Modify: `src/motor/Raiz.tsx`
- Modify: `package.json` (declarar `zod`)

- [ ] **Step 1: escrever o teste que falha** — criar `tests/esquema.test.ts`

```ts
// Portao do contrato de props.
//
// O props.json e o unico arquivo do pipeline que um humano edita a mao e que vai
// direto para o quadro. Sem schema, `"modo": "aleatorio"` so falha na
// renderizacao, e um campo digitado errado nao falha nunca -- sai peca sem
// manchete e ninguem sabe por que.
//
// Nao importa `PecaVideo.tsx`: aquele arquivo importa `tipografia.ts`, que faz
// `loadFont` no topo do modulo e derruba o vitest em Node. O schema mora num
// modulo proprio justamente por isso.

import {describe, it, expect} from 'vitest';
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {esquemaPeca} from '../src/motor/esquema';

const ler = (rel: string) =>
  JSON.parse(fs.readFileSync(fileURLToPath(new URL(rel, import.meta.url)), 'utf8'));

const props = ler('../projetos/01-private-label/props.json');

const PADRAO = {
  arquivo: 'pl.mp4',
  razaoFonte: 9 / 16,
  cortarAntesFrames: 34,
  blocos: [],
  manchete: null,
};

describe('esquemaPeca', () => {
  it('aceita o props.json real do projeto 01-private-label', () => {
    const r = esquemaPeca.safeParse(props);
    expect(r.success).toBe(true);
  });

  it('PRESERVA as chaves de documentacao que comecam com _', () => {
    // MEDIDO: props.json tem `_frames`, `_origem` e `_manchete`, e `z.object`
    // DESCARTA chave desconhecida em silencio -- os comentarios que explicam a
    // convencao de tempo do arquivo desapareceriam do objeto validado. Por isso
    // `z.looseObject`, e nao `z.object`.
    const r = esquemaPeca.parse(props);
    expect(Object.keys(r)).toContain('_frames');
    expect(Object.keys(r)).toContain('_origem');
    expect(Object.keys(r)).toContain('_manchete');
  });

  it('aceita os defaultProps de Raiz.tsx, manchete null incluida', () => {
    expect(esquemaPeca.safeParse(PADRAO).success).toBe(true);
  });

  it('reprova modo de manchete que nao existe', () => {
    const r = esquemaPeca.safeParse({
      ...PADRAO,
      manchete: {texto: 'CAFE', modo: 'aleatorio', inicioFrame: 1},
    });
    expect(r.success).toBe(false);
  });

  it('reprova corte de ar morto negativo', () => {
    expect(esquemaPeca.safeParse({...PADRAO, cortarAntesFrames: -1}).success).toBe(false);
  });

  it('reprova razao de fonte zero ou negativa', () => {
    expect(esquemaPeca.safeParse({...PADRAO, razaoFonte: 0}).success).toBe(false);
  });

  it('reprova arquivo vazio', () => {
    expect(esquemaPeca.safeParse({...PADRAO, arquivo: ''}).success).toBe(false);
  });

  it('reprova bloco de legenda sem frame', () => {
    const r = esquemaPeca.safeParse({
      ...PADRAO,
      blocos: [{texto: 'oi', inicioFrame: 0}],
    });
    expect(r.success).toBe(false);
  });
});
```

- [ ] **Step 2: rodar o teste e conferir que falha**

Run: `npx vitest run tests/esquema.test.ts`
Expected: FALHA no carregamento: `Failed to load url ../src/motor/esquema`.

- [ ] **Step 3: declarar o `zod` em `package.json`**

`zod@4.5.4` e `@remotion/zod-types@4.0.530` já estão no `node_modules` como
dependências transitivas do `@remotion/cli`, e `package-lock.json` já pina
`"zod": "4.5.4"` — mas dependência transitiva não é dependência declarada (é a
lição 11 do CLAUDE.md traduzida para npm: um `npm ci` depois de uma poda do
`@remotion/cli` derruba o import). Em `package.json`, dentro de
`"dependencies"`, acrescentar **sem caret**, na ordem alfabética:

```json
    "remotion": "^4.0.530",
    "zod": "4.5.4"
```

Run: `npm ls zod`
Expected: `zod@4.5.4` listado como dependência direta, sem `invalid` nem
`deduped` conflitante.

- [ ] **Step 4: criar `src/motor/esquema.ts`**

```ts
// O CONTRATO DE PROPS DA PECA, em zod.
//
// POR QUE EXISTE
//
// `props.json` e o unico arquivo do pipeline que um humano edita a mao e que vai
// QUEIMADO no quadro. Antes deste arquivo, `"modo": "aleatorio"` so falhava na
// renderizacao e um campo com o nome errado nao falhava nunca -- saia peca sem
// manchete, com exit 0, e ninguem sabia por que. O schema tambem e o que faz as
// composicoes serem editaveis no painel direito do Studio.
//
// ---------------------------------------------------------------------------
// `z.looseObject`, NAO `z.object`
//
// MEDIDO em 30/09/2026: `projetos/01-private-label/props.json` tem oito chaves
// de topo, e tres comecam com `_` -- `_frames`, `_origem`, `_manchete`. Elas
// documentam a convencao de tempo do arquivo (que os frames estao no tempo da
// FONTE) e a procedencia da manchete. `z.object` DESCARTA chave desconhecida em
// silencio, entao essas tres desapareceriam do objeto validado sem nenhum aviso.
// `z.looseObject` preserva. Confirmado rodando as duas contra o arquivo real.
//
// ---------------------------------------------------------------------------
// ESTE ARQUIVO E A FONTE DO TIPO, NAO UMA COPIA DELE
//
// `PecaVideo.tsx` deriva `Props` daqui por `z.infer`. Um tipo escrito a mao ao
// lado de um schema e duas fontes de verdade que vao divergir -- e a divergencia
// nao daria erro de compilacao, porque os dois sao validos separadamente.

import {z} from 'zod';

/** Um bloco de legenda, no tempo da FONTE. Ver `Legenda.tsx`. */
export const esquemaBloco = z.object({
  texto: z.string(),
  inicioFrame: z.number().int(),
  fimFrame: z.number().int(),
});

/**
 * A manchete. O texto e CITACAO LITERAL da fala, e quem prova isso e
 * `tests/manchete-props.test.ts` -- zod nao tem como saber o que foi falado.
 */
export const esquemaManchete = z.object({
  texto: z.string().min(1),
  modo: z.enum(['sobreImagem', 'cartela']),
  /** frame no tempo da FONTE. `PecaVideo` subtrai `cortarAntesFrames`. */
  inicioFrame: z.number().int(),
  /** indice da UNICA palavra que recebe `COR.acento`. */
  palavraAcento: z.number().int().min(0).optional(),
});

export const esquemaPeca = z.looseObject({
  arquivo: z.string().min(1),
  razaoFonte: z.number().positive(),
  cortarAntesFrames: z.number().int().min(0),
  blocos: z.array(esquemaBloco),
  // Ausente, `null` ou texto em branco = peca sem manchete, sem erro. Ver o
  // cabecalho de `PecaVideo.tsx`: nao existe texto de reserva, de proposito.
  manchete: esquemaManchete.nullable().optional(),
});
```

- [ ] **Step 5: rodar o teste e conferir que passa**

Run: `npx vitest run tests/esquema.test.ts`
Expected: PASS, 8 testes.

- [ ] **Step 6: fazer `PecaVideo.tsx` derivar os tipos do schema**

Trocar as linhas 58-66 (imports) por:

```tsx
import {AbsoluteFill, useVideoConfig} from 'remotion';
import React from 'react';
import type {z} from 'zod';
import {layout} from './layout';
import {Fonte} from './camadas/Fonte';
import {Legenda} from './camadas/Legenda';
import {TextoTela} from './camadas/TextoTela';
import {COR} from '../identidade/tokens';
import {esquemaManchete, esquemaPeca} from './esquema';
```

(`import type {Modo}` e `import type {Bloco}` saem: os dois passam a vir do
schema. `Modo` continua exportado por `texto-forma.ts` para quem precisa dele.)

Trocar as linhas 68-94 (os dois `type`) por:

```tsx
// Os tipos vem do schema, nao de uma copia escrita a mao ao lado dele -- ver o
// cabecalho de `esquema.ts`. A documentacao de cada campo vive la.
export type Manchete = z.infer<typeof esquemaManchete>;
export type Props = z.infer<typeof esquemaPeca>;
```

- [ ] **Step 7: pré-montar o vídeo em `src/motor/camadas/Fonte.tsx`**

Trocar as linhas 27-55 por:

```tsx
import {Video} from '@remotion/media';
import {staticFile, useVideoConfig} from 'remotion';
import React from 'react';
import type {Caixa} from '../layout';
import {SUB} from '../pasta-publica';

export const Fonte: React.FC<{
  arquivo: string;
  caixa: Caixa;
  cortarAntesFrames: number;
}> = ({arquivo, caixa, cortarAntesFrames}) => {
  const {fps} = useVideoConfig();
  return (
    <div
      style={{
        position: 'absolute',
        left: caixa.x,
        top: caixa.y,
        width: caixa.largura,
        height: caixa.altura,
        overflow: 'hidden',
      }}
    >
      <Video
        src={staticFile(`${SUB.fonte}/${arquivo}`)}
        trimBefore={cortarAntesFrames}
        objectFit="cover"
        style={{width: '100%', height: '100%'}}
        // UM SEGUNDO de pre-montagem, derivado de fps. E o que a skill oficial
        // `remotion-markup` manda pôr em todo item temporizado que aceita:
        // `premountFor={fps}`. Sem isso o primeiro frame de midia pode ser
        // desenhado antes do decodificador estar pronto -- e o resultado disso
        // e um frame errado GRAVADO no arquivo, com exit 0.
        //
        // As typings instaladas aceitam: `@remotion/media/dist/video/props.d.ts`
        // declara `VideoProps ... & InteractivePremountProps`.
        premountFor={fps}
      />
    </div>
  );
};
```

E acrescentar ao cabeçalho do arquivo, depois do item 2:

```
// 3. A PRE-MONTAGEM. `premountFor={fps}` monta a camada um segundo antes de ela
//    entrar, para o decodificador estar pronto no primeiro frame desenhado. O
//    numero e `fps`, nao 30: e um SEGUNDO, e a duracao em segundos e o que a
//    regra 3 das fontes pede.
```

- [ ] **Step 8: registrar o schema em `src/motor/Raiz.tsx`**

Acrescentar ao import de `PecaVideo` (linhas 16-17):

```tsx
import {PecaVideo} from './PecaVideo';
import type {Props} from './PecaVideo';
import {esquemaPeca} from './esquema';
```

E acrescentar `schema={esquemaPeca}` nas duas composições de peça:

```tsx
    <Composition
      id="Reel"
      component={PecaVideo}
      schema={esquemaPeca}
      durationInFrames={DURACAO_FRAMES}
      fps={FPS}
      width={1080}
      height={1920}
      defaultProps={PADRAO}
    />
    <Composition
      id="Feed"
      component={PecaVideo}
      schema={esquemaPeca}
      durationInFrames={DURACAO_FRAMES}
      fps={FPS}
      width={1080}
      height={1080}
      defaultProps={PADRAO}
    />
```

(`Teste` e `PonteAssets` ficam sem schema: `Teste` não tem props e `PonteAssets`
é instrumento de conferência, não peça.)

- [ ] **Step 9: rodar a suíte, o typecheck e um render de verdade**

Run: `npx vitest run`
Expected: `Test Files 8 passed (8)` · `Tests 113 passed (113)`

Run: `npm run tsc`
Expected: nenhuma saída (exit 0). Se `defaultProps` reclamar do tipo, é sinal de
que `Props` não está saindo do schema — volte ao Step 6.

Run:
```
npx remotion render src/index.ts Reel out/t5-reel.mp4 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public \
  --frames=0-60
```
Expected: renderiza sem erro de validação de props. Exit 0 **não prova** que o
schema está ativo — para provar, quebre o props de propósito uma vez:

```
node -e "const fs=require('fs');const p=JSON.parse(fs.readFileSync('projetos/01-private-label/props.json','utf8'));p.manchete.modo='aleatorio';fs.writeFileSync('out/props-ruim.json',JSON.stringify(p))"
npx remotion render src/index.ts Reel out/t5-ruim.mp4 \
  --props=out/props-ruim.json \
  --public-dir=projetos/01-private-label/public --frames=0-1
```
Expected: **FALHA** de validação citando `modo`. Se renderizar, o schema não está
ligado.

- [ ] **Step 10: commit**

```bash
git add package.json src/motor/esquema.ts src/motor/PecaVideo.tsx src/motor/Raiz.tsx src/motor/camadas/Fonte.tsx tests/esquema.test.ts
git commit -m "Schema zod das pecas e premountFor no video"
```

---

### Tarefa 6: portão de fps, e o piso da legenda em segundos

**Files:**
- Modify: `src/identidade/tokens.ts` (`TEMPO` e `LEGENDA`)
- Modify: `src/motor/movimento.ts` (uma função nova)
- Modify: `src/legenda/agrupar.ts:20-21`
- Modify: `src/motor/PecaVideo.tsx:97`
- Test: `tests/movimento-fps.test.ts` (criar), `tests/agrupar.test.ts` (um `it` novo)

**Escopo honesto.** O conserto completo da regra 3 é declarar `TEMPO` em segundos
e passar `fps` por `progresso`, `fases`, `atrasoDoIrmao`, `duracaoDeIrmao`,
`duracaoComIrmaos`, `janelasDeIrmaos`, `duracaoPorPalavra`, `duracaoDaFrase` e
`formaTextoTela` — são ~50 pontos de chamada entre `src/` e três arquivos de
teste, e nada no projeto pede outro fps hoje. Esta tarefa faz as duas coisas que
valem sozinhas: **(a)** um portão que mata o render em vez de entregar tempo
errado com exit 0, e **(b)** o único lugar onde `fps` já está no escopo e é
ignorado. O resto fica em §3.1 com este parágrafo como razão.

- [ ] **Step 1: escrever o teste que falha** — criar `tests/movimento-fps.test.ts`

```ts
// Portao de fps.
//
// `TEMPO` e `LEGENDA` estao em FRAMES medidos a 30 fps. Medido rodando os
// tokens, a entrada de 12 frames dura:
//   24 fps -> 0,500 s    30 fps -> 0,400 s    60 fps -> 0,200 s
// e o stagger de 3 frames dura 0,125 / 0,100 / 0,050 s.
//
// Registrar uma composicao a 60 fps, ou entregar Shorts a 60, cortaria pela
// metade a duracao de TODA entrada, saida, hold e stagger -- sem erro, sem aviso
// e com exit 0. E o modo de falha que `tipografia.ts` descreve pela fonte e que
// a licao 3 do CLAUDE.md nomeia: exit 0 nao prova nada.
//
// Enquanto a gramatica nao for declarada em segundos (ver §3.1 do plano), este
// portao transforma o erro silencioso em erro alto.

import {describe, it, expect} from 'vitest';
import {exigirFpsDeReferencia} from '../src/motor/movimento';
import {TEMPO} from '../src/identidade/tokens';

describe('exigirFpsDeReferencia', () => {
  it('o fps de referencia e 30, e e o mesmo que Raiz.tsx registra', () => {
    expect(TEMPO.fpsDeReferencia).toBe(30);
  });

  it('aceita o fps de referencia', () => {
    expect(() => exigirFpsDeReferencia(TEMPO.fpsDeReferencia)).not.toThrow();
  });

  it('recusa qualquer outro fps em vez de encurtar tudo em silencio', () => {
    for (const fps of [24, 25, 50, 60]) {
      expect(() => exigirFpsDeReferencia(fps)).toThrow(/30/);
    }
  });

  it('a mensagem diz o que aconteceria, com numero', () => {
    // A 60 fps a entrada de 12 frames duraria 0,200 s em vez de 0,400 s.
    expect(() => exigirFpsDeReferencia(60)).toThrow(/0,200/);
    expect(() => exigirFpsDeReferencia(60)).toThrow(/0,400/);
  });
});
```

E acrescentar em `tests/agrupar.test.ts`, dentro do `describe('agrupar')`:

```ts
  it('o piso de duracao e o MESMO em segundos em qualquer fps', () => {
    // O DEFEITO: `agrupar` recebe `fps`, converte ms->frames certo, e duas
    // linhas depois aplica `LEGENDA.duracaoMinFrames`, que e um literal de 30
    // fps. A 60 fps o piso de leitura da legenda caia de 0,333 s para 0,167 s --
    // abaixo do tempo de ler duas palavras.
    for (const fps of [24, 30, 60]) {
      const bs = agrupar(palavras, {fps});
      for (const b of bs) {
        expect((b.fimFrame - b.inicioFrame) / fps).toBeGreaterThanOrEqual(
          0.333 - 1e-9,
        );
      }
    }
  });
```

- [ ] **Step 2: rodar os testes e conferir que falham**

Run: `npx vitest run tests/movimento-fps.test.ts tests/agrupar.test.ts`
Expected: FALHA. Em `movimento-fps`: `exigirFpsDeReferencia is not a function` e
`TEMPO.fpsDeReferencia` é `undefined`. Em `agrupar`: a 60 fps o bloco mais curto
dá `0.16666...`, e `expected 0.16666 to be greater than or equal to 0.333`.

- [ ] **Step 3: acrescentar os tokens em `src/identidade/tokens.ts`**

No bloco `TEMPO` (linhas 15-23), trocar o comentário e acrescentar o campo:

```ts
// Tempos em FRAMES a `fpsDeReferencia`. Medidos, não escolhidos.
//
// Estarem em frames é uma DÍVIDA conhecida, não um descuido: a regra 3 das
// fontes de referência pede duração em segundos convertida por
// `useVideoConfig().fps`. Enquanto a dívida existir, `exigirFpsDeReferencia()`
// em `movimento.ts` mata o render de qualquer composição com outro fps, em vez
// de entregar a peça inteira com o tempo errado e exit 0.
export const TEMPO = {
  fpsDeReferencia: 30,  // o fps em que TODO numero abaixo foi medido
  entrada: 12,          // faixa util 8-18
  saidaExpoente: 2.4,   // aceleracao de saida t^2.4
  overshoot: 0.03,      // 2-4%
  stagger: 3,           // 2-4 frames entre elementos irmaos
  holdFinal: 12,        // 8-18
  pousoEasing: 'cubic-bezier(0.20,0.80,0.20,1.00)',
} as const;
```

E no bloco `LEGENDA`, trocar a linha do piso:

```ts
  // Piso de leitura de um bloco, em SEGUNDOS. Era `duracaoMinFrames: 10`, um
  // literal de 30 fps aplicado dentro de uma funcao que JA recebia fps.
  // 0,333 s = 10 frames a 30 fps, 8 a 24, 20 a 60.
  duracaoMinSegundos: 0.333,
```

- [ ] **Step 4: acrescentar o portão em `src/motor/movimento.ts`**

Acrescentar no FIM do arquivo:

```ts
// ---------------------------------------------------------------------------
// o portao de fps

/**
 * Mata o render se a composicao nao estiver no fps em que os tokens foram
 * medidos.
 *
 * Nao e uma limitacao do motor, e a recusa de um modo de falha silencioso:
 * `TEMPO` esta em FRAMES, entao a 60 fps cada entrada, saida, hold e stagger
 * duraria metade do medido -- e o render sairia inteiro, com exit 0. E a licao 3
 * do CLAUDE.md aplicada ao tempo, do mesmo jeito que `tipografia.ts` a aplica a
 * fonte.
 *
 * Para servir outro fps de verdade, `TEMPO` tem que ser declarado em SEGUNDOS e
 * os frames derivados de `useVideoConfig().fps` -- ver a secao 3.1 de
 * `docs/superpowers/plans/2026-09-30-motor-video-qualidade.md`.
 */
export function exigirFpsDeReferencia(fps: number): void {
  if (fps === TEMPO.fpsDeReferencia) return;
  const seg = (frames: number, f: number) =>
    (frames / f).toFixed(3).replace('.', ',');
  throw new Error(
    `este motor foi calibrado a ${TEMPO.fpsDeReferencia} fps e a composicao ` +
      `pediu ${fps}. TEMPO e LEGENDA estao em FRAMES medidos a ` +
      `${TEMPO.fpsDeReferencia}: a ${fps} fps a entrada de ${TEMPO.entrada} ` +
      `frames duraria ${seg(TEMPO.entrada, fps)} s em vez de ` +
      `${seg(TEMPO.entrada, TEMPO.fpsDeReferencia)} s, e o stagger de ` +
      `${TEMPO.stagger} frames viraria ${seg(TEMPO.stagger, fps)} s em vez de ` +
      `${seg(TEMPO.stagger, TEMPO.fpsDeReferencia)} s. A peca sairia inteira, ` +
      `com o tempo todo errado e exit 0 -- entao este portao para antes. Para ` +
      `servir outro fps, declare TEMPO em SEGUNDOS e derive os frames de ` +
      `useVideoConfig().fps.`,
  );
}
```

- [ ] **Step 5: consertar `src/legenda/agrupar.ts`**

Trocar as linhas 16-25 por:

```ts
  // garante duracao minima empurrando o fim, e resolve a sobreposicao que
  // isso cria empurrando o inicio do proximo.
  //
  // O piso vem de `LEGENDA.duracaoMinSegundos` convertido pelo `fps` que esta
  // funcao JA recebe. Antes de 30/09/2026 era o literal `duracaoMinFrames: 10`,
  // medido a 30 fps: a 60 fps o piso de leitura caia para 0,167 s.
  const pisoFrames = Math.round(LEGENDA.duracaoMinSegundos * fps);
  for (let i = 0; i < blocos.length; i++) {
    const b = blocos[i];
    if (b.fimFrame - b.inicioFrame < pisoFrames) {
      b.fimFrame = b.inicioFrame + pisoFrames;
    }
    const prox = blocos[i + 1];
    if (prox && prox.inicioFrame < b.fimFrame) prox.inicioFrame = b.fimFrame;
  }
  return blocos;
}
```

- [ ] **Step 6: chamar o portão em `src/motor/PecaVideo.tsx`**

Trocar a linha 97 por:

```tsx
  const {width, height, fps} = useVideoConfig();
  // Antes de qualquer conta de tempo: ver `exigirFpsDeReferencia`.
  exigirFpsDeReferencia(fps);
```

E acrescentar ao import (depois de `import {layout} from './layout';`):

```tsx
import {exigirFpsDeReferencia} from './movimento';
```

- [ ] **Step 7: rodar a suíte inteira e o typecheck**

Run: `npx vitest run`
Expected: `Test Files 9 passed (9)` · `Tests 118 passed (118)`

O teste existente `tests/agrupar.test.ts:19-23` continua verde: a 30 fps
`Math.round(0.333 * 30)` = 10, o mesmo piso de antes.

Run: `npm run tsc`
Expected: nenhuma saída (exit 0).

- [ ] **Step 8: provar que o portão dispara**

Um portão que nunca disparou não é portão. Acrescente em `src/motor/Raiz.tsx`,
**temporariamente**, uma composição a 60 fps:

```tsx
    <Composition id="ReelSessenta" component={PecaVideo} schema={esquemaPeca}
      durationInFrames={60} fps={60} width={1080} height={1920}
      defaultProps={PADRAO} />
```

Run:
```
npx remotion render src/index.ts ReelSessenta out/t6-60.mp4 \
  --public-dir=projetos/01-private-label/public --frames=0-1
```
Expected: **FALHA**, com a mensagem `este motor foi calibrado a 30 fps e a
composicao pediu 60` e os números `0,200` e `0,400`.

Depois **remova** a composição `ReelSessenta` de `Raiz.tsx` e rode
`npx vitest run` de novo, esperando os mesmos 118 testes verdes.

- [ ] **Step 9: commit**

```bash
git add src/identidade/tokens.ts src/motor/movimento.ts src/legenda/agrupar.ts src/motor/PecaVideo.tsx tests/movimento-fps.test.ts tests/agrupar.test.ts
git commit -m "Portao de fps e piso de legenda em segundos"
```

---

### Tarefa 7: invariante de duas linhas na legenda

**Files:**
- Create: `src/legenda/linhas.ts`
- Create: `tests/legenda-linhas.test.ts`
- Modify: `src/motor/camadas/texto-forma.ts:111-114` (alargar o `papel` de `quebrar`)

- [ ] **Step 1: escrever o teste que falha** — criar `tests/legenda-linhas.test.ts`

```ts
// Portao de altura da legenda.
//
// MEDIDO em 30/09/2026 sobre os 38 blocos reais de
// projetos/01-private-label/props.json, com as larguras de avanco de glifos.ts:
//
//   Reel 1080x1920, caixa 760,0 x 307,2 px, corpo 78 .... max 2 linhas
//     (1 de 38: "melhores profissionais", 871,5 px)
//   Feed 1080x1080, caixa 575,5 x 172,8 px, corpo 78 .... max 2 linhas (6 de 38)
//   duas linhas medem 149,8 px e cabem nos dois
//   TRES linhas mediriam 224,6 px e NAO cabem na caixa do Feed
//
// `Legenda.tsx` desenha um `<span>` sem limite de linha e sem ajuste de corpo:
// quem quebra e o Chrome, na largura da caixa. Duas linhas nao sao defeito -- a
// caixa ancora em `flex-end`, entao a ultima linha fica sempre na mesma linha de
// base e a segunda aparece acima, que e como legenda de duas linhas se parece.
// Tres seriam: transbordariam a caixa do Feed para cima.
//
// Nada no motor garantia esse limite. Este portao garante, e reprova a
// transcricao que o rompe ANTES do render.
//
// O 16:9 NAO entra na varredura: `Raiz.tsx` nao o registra, e ali o motor
// sabidamente estoura (2 linhas = 266,2 px numa caixa de 172,8). Fingir
// cobertura que nao existe e a licao 10 do CLAUDE.md.

import {describe, it, expect} from 'vitest';
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {medirBlocosDeLegenda} from '../src/legenda/linhas';
import {layout} from '../src/motor/layout';
import {LEGENDA} from '../src/identidade/tokens';
import type {Bloco} from '../src/legenda/agrupar';

const ler = (rel: string) =>
  JSON.parse(fs.readFileSync(fileURLToPath(new URL(rel, import.meta.url)), 'utf8'));

const props = ler('../projetos/01-private-label/props.json') as {blocos: Bloco[]};

/** Os dois formatos de peca REGISTRADOS em `Raiz.tsx`. */
const REGISTRADOS: Array<[number, number]> = [
  [1080, 1920],
  [1080, 1080],
];

const medidas = (largura: number, altura: number) => {
  const z = layout({largura, altura, razaoFonte: 9 / 16});
  return medirBlocosDeLegenda(props.blocos, {
    corpo: LEGENDA.corpoEm1080 * (largura / 1080),
    largura: z.legenda.largura,
    altura: z.legenda.altura,
  });
};

describe('medirBlocosDeLegenda', () => {
  it('mede todos os 38 blocos do projeto, sem perder nenhum', () => {
    for (const [w, h] of REGISTRADOS) {
      expect(medidas(w, h).length).toBe(props.blocos.length);
    }
  });

  it('nenhum bloco passa de DUAS linhas nos formatos registrados', () => {
    for (const [w, h] of REGISTRADOS) {
      for (const m of medidas(w, h)) {
        expect(m.linhas.length).toBeLessThanOrEqual(2);
      }
    }
  });

  it('todo bloco cabe na ALTURA da caixa de legenda', () => {
    for (const [w, h] of REGISTRADOS) {
      for (const m of medidas(w, h)) {
        expect(m.cabe).toBe(true);
      }
    }
  });

  it('o Feed tem mais bloco de duas linhas que o Reel, porque a caixa e menor', () => {
    // Medido: 1 de 38 no Reel (caixa 760,0), 6 de 38 no Feed (caixa 575,5).
    const duas = (w: number, h: number) =>
      medidas(w, h).filter((m) => m.linhas.length === 2).length;
    expect(duas(1080, 1920)).toBe(1);
    expect(duas(1080, 1080)).toBe(6);
  });

  it('nao perde nem reordena palavra do bloco', () => {
    for (const [w, h] of REGISTRADOS) {
      const ms = medidas(w, h);
      for (let i = 0; i < ms.length; i++) {
        expect(ms[i].linhas.join(' ')).toBe(props.blocos[i].texto);
      }
    }
  });

  it('reprova um bloco inventado que ocuparia tres linhas no Feed', () => {
    // A prova de que o portao morde: nao basta passar nos blocos que existem.
    const z = layout({largura: 1080, altura: 1080, razaoFonte: 9 / 16});
    const [m] = medirBlocosDeLegenda(
      [{texto: 'profissionais profissionais profissionais', inicioFrame: 0, fimFrame: 30}],
      {corpo: LEGENDA.corpoEm1080, largura: z.legenda.largura, altura: z.legenda.altura},
    );
    expect(m.linhas.length).toBeGreaterThanOrEqual(3);
    expect(m.cabe).toBe(false);
  });
});
```

- [ ] **Step 2: rodar o teste e conferir que falha**

Run: `npx vitest run tests/legenda-linhas.test.ts`
Expected: FALHA no carregamento: `Failed to load url ../src/legenda/linhas`.

- [ ] **Step 3: alargar o `papel` de `quebrar` em `src/motor/camadas/texto-forma.ts`**

A quebra de linha é a mesma para as três famílias; só `formaTextoTela` é que é
restrita a `manchete` e `dado`. Trocar a assinatura (linhas 111-114) por:

```ts
export function quebrar(
  texto: string,
  {papel, corpo, largura}: {papel: Papel; corpo: number; largura: number},
): string[] {
```

E acrescentar ao topo dos imports (linha 37 e seguintes):

```ts
import type {Papel} from '../../identidade/tipografia';
```

`import type` é apagado na compilação, então isto **não** puxa o efeito colateral
de `loadFont` para dentro do módulo puro — é a mesma razão pela qual
`glifos.ts:15` já importa `Papel` daquele arquivo.

- [ ] **Step 4: criar `src/legenda/linhas.ts`**

```ts
// QUANTAS LINHAS UM BLOCO DE LEGENDA OCUPA. Puro: sem React, sem remotion, sem
// DOM.
//
// POR QUE ESTE MODULO EXISTE
//
// `Legenda.tsx` desenha um `<span>` sem limite de linha e sem ajuste de corpo:
// quem quebra a linha e o Chrome, na largura da caixa que `layout()` deu. Medido
// sobre os 38 blocos reais de `projetos/01-private-label/props.json`:
//
//   Reel 1080x1920, caixa 760,0 x 307,2, corpo 78 ... max 2 linhas (1 de 38)
//   Feed 1080x1080, caixa 575,5 x 172,8, corpo 78 ... max 2 linhas (6 de 38)
//   duas linhas medem 149,8 px e cabem nos dois
//   tres linhas mediriam 224,6 px e NAO caberiam na caixa do Feed
//
// Duas linhas NAO sao defeito: a caixa ancora em `flex-end`, entao a ultima
// linha fica sempre na mesma linha de base e a segunda aparece acima -- e como
// legenda de duas linhas se parece. Tres transbordariam a caixa do Feed para
// cima, por cima do video, e a transcricao que produzisse isso passaria pelo
// motor sem nenhum aviso.
//
// A largura vem da MESMA fonte que a da manchete: as larguras de avanco lidas do
// `hmtx` dos .ttf (`identidade/glifos.ts`), somadas pela mesma quebra gulosa de
// `texto-forma.ts`. Se os dois divergissem, o portao mediria uma quebra que a
// tela nao faz.

import {LEGENDA} from '../identidade/tokens';
import {quebrar} from '../motor/camadas/texto-forma';
import type {Bloco} from './agrupar';

/** Tolerancia de ponto flutuante, a mesma de `texto-forma.ts`. */
const EPS = 1e-6;

export type MedidaDeBloco = {
  texto: string;
  linhas: string[];
  /** altura do bloco em px: `linhas * corpo * LEGENDA.entrelinha` */
  altura: number;
  /** o bloco cabe na altura da caixa de legenda? */
  cabe: boolean;
};

export function medirBlocosDeLegenda(
  blocos: Bloco[],
  {corpo, largura, altura}: {corpo: number; largura: number; altura: number},
): MedidaDeBloco[] {
  return blocos.map((b) => {
    const linhas = quebrar(b.texto, {papel: 'corpo', corpo, largura});
    const alturaBloco = linhas.length * corpo * LEGENDA.entrelinha;
    return {
      texto: b.texto,
      linhas,
      altura: alturaBloco,
      cabe: alturaBloco <= altura + EPS,
    };
  });
}
```

- [ ] **Step 5: rodar o teste e conferir que passa**

Run: `npx vitest run tests/legenda-linhas.test.ts`
Expected: PASS, 6 testes.

- [ ] **Step 6: rodar a suíte inteira e o typecheck**

Run: `npx vitest run`
Expected: `Test Files 10 passed (10)` · `Tests 124 passed (124)`

Run: `npm run tsc`
Expected: nenhuma saída (exit 0).

- [ ] **Step 7: commit**

```bash
git add src/legenda/linhas.ts src/motor/camadas/texto-forma.ts tests/legenda-linhas.test.ts
git commit -m "Portao: nenhum bloco de legenda passa de duas linhas"
```

---

### Fechamento das sete tarefas

- [ ] **Passo final 1: suíte e typecheck**

Run: `npx vitest run`
Expected: `Test Files 10 passed (10)` · `Tests 124 passed (124)`

Run: `npm run tsc`
Expected: nenhuma saída.

- [ ] **Passo final 2: render completo dos dois formatos, e conferência ampliada**

```
npx remotion render src/index.ts Reel out/final-reel.mp4 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
npx remotion render src/index.ts Feed out/final-feed.mp4 \
  --props=projetos/01-private-label/props.json \
  --public-dir=projetos/01-private-label/public
```

Confira, **em recorte ampliado** e não na imagem inteira (lição 13):
1. contra-forma de `a`, `e`, `o` na legenda, com o contorno de 11,14 px;
2. o último frame de cada cena de manchete, que não pode ter resíduo de terra;
3. a margem de topo da manchete no Reel, que tem que dar 96 px;
4. os blocos de duas linhas (1 no Reel, 6 no Feed) com a última linha na mesma
   altura dos blocos de uma linha.

- [ ] **Passo final 3: registrar as lições no CLAUDE.md**

Acrescentar ao **Registro de lições**, no fim do arquivo
`C:/Users/rafae/OneDrive/Desktop/Canastra Inteligencia/Agentes AI/Canastra-Content-Creator/CLAUDE.md`,
as três que este plano mediu e que nenhuma sessão futura vai redescobrir de graça:

```markdown
25. **Todo elemento do motor de vídeo desaparecia a 18,85% de opacidade** → a
    saída era normalizada pelo primeiro frame NÃO desenhado (`(t - inicioSaida) /
    saida`), e o expoente 2,4 amplificava o resíduo: com saída linear seriam
    8,33%. O teste passava porque media `progresso(duracao)`, que é o ramo
    "depois" → **normalize janela de animação pelo ÚLTIMO frame desenhado**, e
    teste `duracao - 1`, nunca `duracao`.
26. **Um `k` só derivado da largura escalava as margens verticais** → a margem de
    base saía 16,15% da altura no 9:16, 28,70% no 1:1 e 51,03% no 16:9, e a área
    segura do 16:9 ficava com 368,9 px — o mesmo 368,9 que outro comentário do
    motor registrava como "texto de borda a borda" sem ligar as duas coisas →
    **margem é fração do eixo que ela corta**; um fator por eixo, e teste a
    porcentagem, não o pixel.
27. **Quis reservar o push de 4% na busca de corpo e o corpo desabou de 44 para
    15 px** no Feed 1:1 → a quebra gulosa faz `cabe()` não ser monotônico no
    corpo, e a rede `while (corpo > 1 && !cabe(corpo)) corpo--` desce até achar um
    valor que cabe, que pode estar muito abaixo → **antes de apertar uma restrição
    de layout, meça o corpo resultante em todos os formatos**; numa busca com rede
    de segurança, uma restrição 4% mais dura não custa 4%.
```

- [ ] **Passo final 4: commit**

```bash
git add CLAUDE.md
git commit -m "Licoes 25 a 27: saida off-by-one, margem por eixo, busca de corpo"
```

---

## 5. O que NÃO mudar

A auditoria achou isto conforme, e cada item tem uma razão medida por trás. Não
são preferências: mexer neles desfaz um bug já pago.

**A gramática de tempo**

- `bezierDeCss()` + `POUSO` (`movimento.ts:57-116`). A curva que o teste mede e a
  curva que o Chrome desenha saem dos **mesmos quatro números** de
  `TEMPO.pousoEasing`. Se o easing fosse reescrito à mão em JS, alguém editaria o
  token e o movimento continuaria o antigo sem ninguém perceber. **Não trocar por
  `spring()`** (que é o que A e B pedem — divergência D3): `spring` vem de
  `remotion`, e importar `remotion` no módulo puro acabaria com os 85 testes em
  Node.
- `fases()` comprimindo as **pontas** em vez de estourar o hold
  (`movimento.ts:135-140`). Um elemento de 3 frames ainda tem uma fase de cada, e
  o hold nunca fica negativo. A alternativa — entrada e saída se sobrepondo —
  daria presença subindo e descendo no mesmo frame.
- `duracaoDeIrmao()` (`movimento.ts:225-228`) e o teste que o prova
  (`textotela.test.ts:333-360`). Foi ele que resolveu o defeito visto num still e
  não num teste: com `DURACAO_MINIMA` para todas as palavras, 'CAFE' já estava em
  0,81 de presença, saindo, enquanto 'CANASTRA' ainda entrava — não existia **um**
  frame com a manchete legível inteira.
- `TEMPO.overshoot` lido como **pouso de uma direção só**, nunca repique
  (`movimento.ts:26-32` e `:172`). Repique é easing elástico, e
  `proibicoes.md:11` proíbe. O elemento oficial de legenda do Remotion faz
  1 → 1,03 → 1, que são duas direções; nós não.
- `push()` **linear** (`movimento.ts:233-244`). Divergência D4, consciente.

**A medição de tipografia**

- As larguras de avanço lidas do `hmtx` dos próprios `.ttf`
  (`identidade/glifos.ts`, `larguraEm`) e a busca binária de corpo
  (`texto-forma.ts:216-241`), **incluindo a rede**
  `while (corpo > 1 && !cabe(corpo)) corpo--`. **Não trocar por `fitText` de
  `@remotion/layout-utils`**: `fitText` mede no DOM, e é exatamente por ser puro
  que o corpo é provável em Node. O pacote, além disso, não está instalado.
- A guarda de `identidade/tipografia.ts:128-200`: mede a largura de uma amostra
  sob a família alvo contra a mesma amostra sob uma família inexistente, e
  `cancelRender` se derem igual. Já pegou um bug real — quatro MP4 entregues em
  Times New Roman com exit 0. É a lição 3 aplicada à fonte.
- Os `.ttf` locais em vez de `@remotion/google-fonts`: o portão de determinismo
  (`verificacao/determinismo.ts`) nomeia "fonte carregada por rede" como causa de
  render não determinístico, e uma máquina offline volta ao fallback em silêncio.
- A amostra `'Canastra private label 250g CAO acucar 12,5'`
  (`tipografia.ts:103`), com acento de pt-BR de propósito: um `.ttf` recortado
  sem `latin-ext` denunciaria pela largura.
- `letterSpacing: 0` explícito (`TextoTela.tsx:173`). A conta de largura só vale
  se o CSS não mexer no tracking; kerning fica ligado porque nestas grotescas os
  pares com kern **apertam**, então o texto real sai igual ou mais estreito que o
  medido — o lado seguro.

**A geometria**

- `intersecao(zonas.manchete, zonas.seguro)` (`texto-forma.ts:95-101` e `:193`).
  `zonas.manchete` vaza 122 px pela direita e 180 px por baixo no 1:1. O recorte
  é carregando, não cosmético.
- `linhasDeFolga = 1` na cartela (`texto-forma.ts:214`), e "uma linha" sendo a
  unidade que a própria fonte define (`corpo * alturaLinha` lido de `hhea`), não
  um percentual escolhido no olho.
- `alinhaHorizontal: 'flex-start'` nos **dois** modos (`texto-forma.ts:302`).
  Centrar texto é o reflexo do modelo generativo sem direção, e
  `proibicoes.md:13` chama isso pelo nome.
- `fundo: COR.terra` na cartela, nunca branco (`texto-forma.ts:283`), e o fundo
  da peça em terra e não preto (`PecaVideo.tsx:106-109`), porque no 1:1 a sobra
  ao lado da coluna de vídeo fica visível.
- O encaixe `contain` nos dois eixos, nunca `cover` (`layout.ts:41-55`): o vídeo
  nunca é cortado na largura para caber num quadro mais largo, ele vira coluna.
  É a propriedade que faz o 1:1 ser **reenquadramento** e não recorte.
- A sombra da manchete escalada pelo corpo contra o corpo da legenda
  (`texto-forma.ts:291-299`): uma manchete de 123 px com a sombra de um texto de
  78 px pareceria sem sombra.

**A arquitetura**

- Uma composição só (`PecaVideo`) servindo os dois formatos, com a diferença
  inteira dentro de `layout()` (`Raiz.tsx:1-12`). Se aparecer um componente
  "PecaFeed", o motor perdeu a propriedade que ele existe para ter.
- A separação puro / fiação: o que precisa de prova vive em `movimento.ts`,
  `texto-forma.ts`, `layout.ts`, `agrupar.ts` e `linhas.ts`; o `.tsx` só liga
  fios. A razão é mecânica e está medida: `tipografia.ts` faz `loadFont` no topo
  do módulo e derruba o vitest em Node com `TypeError: Invalid URL` — um teste que
  só importava `Legenda.tsx` passava a asserção e o vitest saía com código 1.
- A ordem de árvore `Fonte` → `TextoTela` → `Legenda` (`PecaVideo.tsx:110-135`) e
  o comentário que explica a escolha: a cartela cobre o vídeo mas **não** cobre a
  legenda, porque apagar a legenda por dois segundos quebraria a continuidade de
  leitura.
- A manchete **opcional sem placeholder** (`PecaVideo.tsx:100-103`,
  `Raiz.tsx:38-42`) e `blocos: []` por padrão. Um texto de exemplo aqui seria a
  mesma armadilha do `_LEIA` que fez quatro MP4 saírem com legenda inventada
  queimada no quadro.
- `tests/manchete-props.test.ts` inteiro. É o portão que prova que
  `manchete.texto` é trecho **contíguo** de `transcricao.json`, com caixa alta
  como única transformação. Sem ele, "manchete" é campo de texto livre no meio de
  um pipeline que existe para nunca queimar frase inventada.
- O `props.json` guardando **um relógio só** (tempo da FONTE), com a conversão
  acontecendo uma vez em `PecaVideo.tsx:126` e uma vez em
  `Legenda.tsx` pelo `deslocamentoFrames`. Um props com dois relógios é um props
  que alguém vai ler errado.
- `SUB.fonte` morando na camada `Fonte` e não no `props.json`
  (`Fonte.tsx:13-25`): o props fala de MEDIDA, não de arrumação de pasta.

**A base**

- Os 85 testes que já passam, e que **nenhuma** das sete tarefas remove. Duas
  asserções são ajustadas, com o número novo medido e escrito: a do meio da saída
  (tarefa 2) e nada mais. `npx vitest run` na base:
  `Test Files 6 passed (6)` · `Tests 85 passed (85)`.
