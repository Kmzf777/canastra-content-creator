# O catálogo de formatos

Este é o documento que o motor de vídeo (`instagram/remotion/`) consome como **briefing**.
Ele não discute se a Canastra deve postar mais — isso já está decidido por medição em
[`01-concorrencia.md`](../01-concorrencia.md). Ele responde à pergunta seguinte: **qual
peça exatamente, feita com qual arquivo que já existe no disco, e o que o motor tem que
executar para entregá-la.**

A convenção de marcação é a de [`LEIA-ME.md`](LEIA-ME.md): **[oficial]** · **[medido]** ·
**[criador]** · **[terciário]** · **[folclore]**. Afirmação sem marca aqui é erro de
redação.

Regra que organiza o arquivo inteiro: **nenhuma linha da tabela mestra entra sem
matéria-prima nomeada.** Onde a matéria-prima não existe, a linha diz qual bloco do
[`docs/briefing-captura.md`](../../docs/briefing-captura.md) a desbloqueia e quanto custa —
não é aspiração escondida em coluna vazia.

---

## 1. O estado da matéria-prima, medido hoje

Contado em **30/09/2026** percorrendo as pastas com `find` e lendo a dimensão de cada
arquivo com PIL **[medido]**. É o inventário contra o qual toda linha da tabela é conferida.

| Acervo | O que tem | Dimensão | Pode virar pixel? |
|---|---|---|---|
| `base-curada/01-real-verificada/fazenda-medeiros-1250m/` | **26** fotos — 20 de cafezal, 3 de cereja **verde**, 2 de mão no pé, 1 de folha | 4032×3024 nos 26 | **sim** |
| `base-curada/01-real-verificada/torrefacao-uberlandia-875m/` | **12** packshots dos 3 SKUs contra parede lisa | arquivo lê 4096×2304; `Orientation = 6` nos 3 conferidos → **2304×4096 na tela** | **sim** |
| `fotos produtos cru/` | **134** arquivos, 21 pastas por SKU/gramatura/moagem, faces `frente`/`verso`/`lateral` | 124 a 3072×4096 · 6 a 4096×3072 · 4 a 591×1280 | sim, é foto própria |
| `imagens/Arthur Rosto/` | **13** retratos | **960×1280 nas 13** — abaixo de 1080 de largura | sim, mas **não enche quadro de Reel sem ampliar** |
| `base-curada/02-real-nao-verificada/` | 6 paisagens da Serra, sem EXIF e sem GPS | 12 MP | **não**, até alguém confirmar a origem |
| `base-curada/03-mood-terceiros/` | 16 scrapes de Pinterest — é a estética-alvo e nada é nosso | 736 px de largura | **nunca** |
| `base-curada/04-quarentena/` | 6 — 2 sintéticas do Gemini, 4 arruinadas por WhatsApp | ≤1024 | **nunca** |
| `instagram/remotion/projetos/01-private-label/fonte/pl.mp4` | **1 vídeo** — selfie caminhando pelo galpão, pitch de private label | 576×1024, 24,33 s, 29,96 fps | sim, é o único vídeo do acervo |

**As três ausências que definem o catálogo**, levantadas em `docs/briefing-captura.md` sobre
os 66 arquivos de `/imagens` e reconferidas agora **[medido]**:

1. **Zero foto de grão torrado.** É o produto que a marca vende.
2. **Zero foto de café pronto** — xícara, coador, bule, mesa posta com o produto.
3. **Zero foto de torrefação em operação, de terreiro, de colheita com cereja madura e de
   painel solar.** Três dos quatro pilares da `Direcao-Criativa.md` não têm uma foto própria
   **[medido]**.

E duas armadilhas de acervo que já custaram trabalho neste repositório:

- **20 fotos de cafezal são do mesmo dia, na mesma luz de meio-dia — a diversidade real é de
  ~4 cenas [medido].** Quem contar 20 acha que tem um mês de conteúdo e tem uma tarde.
- **Discrepância no acervo de produto, registrada e não resolvida [medido]:** a pasta tem 134
  arquivos de imagem; `fotos produtos cru/_LEIA-ME.md` declara **131** e sua tabela não lista
  `Capsulas-Suave-10un-5g` (4 arquivos, **591×1280**, vindos de WhatsApp — os mesmos da lição
  18 do `CLAUDE.md`); e `Canastra-Classico-250g-Graos` tem **6** arquivos onde o LEIA-ME
  declara 7. Quem for usar a pasta confere a pasta, não a tabela.

### Preço de tabela, para os formatos que citam número

Lidos em `fotos produtos cru/_LEIA-ME.md`, que os copiou de `tabela.cafecanastra.com` em
**11/09/2026** **[medido]** — e podem ter mudado desde então, o que precisa ser confirmado
antes de qualquer peça que mostre preço:

250 g moído **R$ 28,70** · 250 g grãos **R$ 31,70** · 500 g moído **R$ 52,70** ·
500 g grãos **R$ 54,70** · 1 kg grãos **R$ 97,70** · Microlote 250 g **R$ 32,70** ·
Néctar de Minas 500 g moído **R$ 39,70** · Néctar 1 kg grãos **R$ 88,70** — os oito
lidos no arquivo, não de memória **[medido]**.

---

## 2. O que o motor consome deste catálogo

**Não confie nesta seção para saber o que o motor faz — liste a pasta.** O que está escrito
aqui é um *retrato*, e a regra que governa isso está em `LEIA-ME.md`, seção *Estado do
repositório não é [medido]*.

*Retrato de 30/09/2026, lido em `instagram/remotion/`:* o motor **existe e renderiza**.
`src/motor/Raiz.tsx` registra **três composições** — `Reel` (1080×1920), `Feed` (1080×1080) e
`Teste` (60 frames, placeholder). `Reel` e `Feed` são a **mesma peça** (`PecaVideo`) com
dimensão diferente: a diferença inteira vive em `src/motor/layout.ts`, que **reenquadra em vez
de recortar**. Existem também `src/motor/camadas/Legenda.tsx`, `src/motor/sondar.ts`,
`src/legenda/transcrever.ts` e `src/legenda/agrupar.ts`, quatro módulos em `src/verificacao/`,
e `npm test` passava **23 testes em 4 arquivos** nessa data. `AUDIO = {lufs: -14, picoDbtp: -1}`
está em `src/identidade/tokens.ts`. Há transcrição do `pl.mp4` em
`projetos/01-private-label/transcricao.json` e MP4 renderizados em `projetos/01-private-label/saida/`.

> **A versão anterior desta seção dizia, marcada [medido], que existia "uma composição
> chamada `Teste`" e que "zero formatos são renderizáveis".** Era falsa no mesmo dia. É o caso
> que deu origem à regra do `LEIA-ME.md`: estado de repositório envelhece, e [medido] promete
> uma estabilidade que caminho de arquivo não tem.

O que continua valendo, porque é sobre **especificação e não sobre estado**: a fonte do que o
motor deve fazer é `docs/superpowers/plans/2026-09-30-motor-video-remotion.md` — função de
zonas que reenquadra o mesmo timeline em 9:16 e 1:1, legenda karaokê de no máximo 2 palavras
por bloco, transcrição Whisper em pt-BR, normalização a −14 LUFS com teto de −1 dBTP, push de
câmera de 1,00 a 1,04, e portões de verificação de preservação de pixel e legibilidade.

**A coluna "o que o motor precisa fazer" da tabela mestra é um pedido de implementação por
formato** — e §6 lista as capacidades que este catálogo exige e o plano não cobre. Essas
lacunas são de **especificação**, então não envelhecem do mesmo jeito; mesmo assim, confira
antes de dizer a um cliente que algo não dá.

Três proibições do motor que decidem o desenho de vários formatos daqui, transcritas de
`proibicoes.md` no plano e das lições já pagas do `CLAUDE.md`:

- **Letra é sempre código.** Nenhum texto de tela sai de modelo generativo — é a resposta
  estrutural ao `Doodo 1985` (lição 13 do `CLAUDE.md`) e ao `SOSCIALTY` da seção *Regra zero*,
  nas palavras do próprio `instagram/LEIA-ME.md` **[medido]**.
- **Nada altera pixel dentro da embalagem** — nem `<CameraMotionBlur>`, nem glow, nem
  correção de cor local.
- **Lote, fabricação e validade nunca são redesenhados** (lição 22: saiu `F:23.2025`, mês que
  não existe, e no Canela saiu `F:12.2025`, plausível — que é pior). Ou sai do enquadramento,
  ou entra por composição da foto real.

---

## 3. Portão de elegibilidade — vale para toda linha em Reel

Critérios do próprio Instagram para um Reel ser entregue a **não-seguidores** **[oficial]**:
sem marca d'água · **com áudio** · ≤3 minutos · substancialmente original · conta em bom
status. E os três sinais de ranking mais importantes, nesta ordem de peso **[oficial]**:
**tempo médio assistido** (o principal tanto em seguidor quanto em recomendação), **curtidas
por alcance** (pesa mais no conectado), **envios por alcance** (pesa mais no
não-conectado) — Mosseri, textualmente: *"sends são uma parte enorme do sucesso dos Reels"*
**[oficial]**.

Duas consequências diretas para este catálogo, e elas cortam formatos:

1. **"Mudo" aqui significa "sem locução", nunca "sem faixa de áudio".** Reel sem áudio perde
   a elegibilidade para não-seguidores **[oficial]**. O formato de tela dividida do Orfeu é
   sem voz, não sem som.
2. **Repostar print de piada de terceiro colide com dois critérios de uma vez** — carrega
   marca d'água alheia e não é substancialmente original **[oficial]** — e ainda colide com a
   regra de camada deste repositório, que proíbe pixel de terceiro na saída. A versão
   transferível do formato @omsom é **piada própria desenhada em código**, não repost. Ver
   série 6.

E o motivo pelo qual cadência é o assunto de fundo: **conteúdo novo recebe ~100 impressões e,
performando acima do esperado, gradua para 1.000 e depois 10.000 [oficial]**. Cada peça é um
bilhete nessa loteria, e a **1 post a cada 42 dias [medido]** a marca compra pouquíssimos.

---

## 4. Tabela mestra

Nesta tabela: **duração alvo** vem do relógio comportamental do harness `corte-viral`
**[criador]** — resposta rápida 15–45 s, contradição 20–60 s, história 35–90 s; **esforço** é
leitura nossa do trabalho humano exigido *depois* que a matéria-prima existe; **matéria-prima**
é caminho de arquivo real ou o bloco de captura que falta **[medido]**. A origem de cada série
e sua marca estão na seção §5.

| Série | Estrutura em 1 linha | Formato | Duração alvo | Matéria-prima | Esforço | O que o motor precisa fazer |
|---|---|---|---|---|---|---|
| **1. Você sabia que** `voce-sabia` | Pergunta na capa → resposta em uma frase → a prova aparece na imagem → o que isso muda na xícara | reel | 15–30 s | 1 foto de `01-real-verificada` + locução de ~20 s no celular. **Pronta** | baixo | capa com texto em código; push 1,00→1,04 sobre a foto parada; legenda karaokê ≤2 palavras; corte do ar morto; áudio a −14 LUFS |
| **2. Infográfico sobre foto real** `infografico` | A foto real recebe setas e rótulos que nomeiam o que se vê nela | estático 1:1 + reel de 8 s | 1 imagem, ou 8 s com entrada em stagger | foto da camada 01 + 3 a 5 rótulos escritos. **Parcial:** cereja **madura** e bóia na água não existem — Blocos D e E | médio | camada de seta e rótulo em código, ancorada em coordenada da imagem; nunca escrever rótulo por modelo; entrada com stagger de 3 frames |
| **3. Arraste para entender** `arraste` | Carrossel de 5–7 slides, um conceito por slide, cenário compartilhado declarado, último slide é a pergunta | carrossel | 5–7 slides | 1 foto da camada 01 por slide + texto. **Pronta** (limite: ~4 cenas reais de cafezal) | médio | **zona 4:5 que o plano do motor não tem**; série coesa com fundo declarado e variação negada (lição 8); numeração de slide em código |
| **4. Jornada do grão** `jornada` | O mesmo grão em 5 estágios, em tela dividida, vídeo real sem locução | reel sem voz, **com** faixa de áudio | 20–40 s | 5 clipes curtos: galho, terreiro, sacaria, tambor, xícara. **Bloqueada** — existem 0 dos 5; Blocos C, D e E | alto | grade de 2 ou 4 células com trim independente por célula; rótulo por célula; faixa de áudio obrigatória (§3) |
| **5. Cápsula com parceiro local** `capsula-parceiro` | Edição limitada feita com uma casa da região, com data de encerramento, publicada como coautoria nos dois perfis | reel ou carrossel | 15–30 s | o parceiro + 1 foto do encontro dos dois produtos. **Bloqueada por negociação**, não por captura | médio | cartão com nome do parceiro e data-limite em código; nada de contador de escassez sem número real |
| **6. Piada relatable sem produto** `piada` | Uma frase que só quem toma café entende, composta em tipografia sobre a paleta da marca | estático | 1 imagem | **nenhuma foto — é o ponto.** Só texto escrito. **Pronta** | baixo | composição só-tipografia em 1:1 e 9:16; nunca repost de print de terceiro (§3) |
| **7. Meme de legenda com o pacote no cotidiano** `meme-pacote` | Foto de celular do pacote onde ele não deveria estar, legenda curta carregando a piada | estático | 1 imagem | 1 foto nova de celular por post — as 134 de `fotos produtos cru/` são `frente`/`verso`/`lateral` de catálogo, não cotidiano **[medido]**. **Custo: 5 minutos, sem viagem** | baixo | nada, é publicação direta; se o pacote entrar em cena montada, recorte de foto real + sombra de contato, jamais rótulo redesenhado |
| **8. Preparo em câmera lenta** `preparo-slow` | Um gesto único em câmera lenta, uma legenda emocional de ≤8 palavras | reel | 10–20 s | 1 clipe do preparo em slow. **Bloqueada** — Bloco A2, a mais barata de desbloquear | baixo depois da captura | retime; um texto único com hold de 12 frames; normalização de áudio; nenhuma transição além de corte |
| **9. Bastidor-comemoração da família** `bastidor` | Celular na mão registrando algo que aconteceu de verdade, sem roteiro | reel | 15–45 s | gravação do dia + **autorização de imagem assinada**. As 13 fotos de `imagens/Arthur Rosto/` são 960×1280 **[medido]** → não servem de quadro cheio | baixo | corte de ar morto; transcrição pt-BR com modelo **multilíngue** (`medium.en` é só inglês); **rosto real nunca sintetizado** |
| **10. Objeção: por que custa mais** `objecao-preco` | A conta aberta: o preço do outro, o nosso, e para onde vai a diferença | reel ou carrossel | 30–60 s | preços de tabela de 11/09/2026 (§1) + preço do concorrente **fotografado na gôndola no dia** + 1 foto da camada 01. **Pronta com substituição** | médio | cartões numéricos em mono (IBM Plex Mono), um por beat, com stagger; nenhum número desenhado por modelo |
| **11. Edição limitada real da safra** `safra-limitada` | Número real de sacas, data real de encerramento, e o que acontece quando acabar: acaba | reel + estático | 15–30 s | o número de sacas, dado pela operação + 1 foto do lote. **Bloqueada por um dado**, não por captura | baixo | contador em código a partir do número informado; **proibido gerar carimbo de lote ou validade** (lição 22) |
| **12. Convidado na mesa (coautoria)** `convidado` | Um criador da região prepara o nosso café na casa dele; o post nasce nos dois feeds | reel | 20–45 s | 1 criador + 1 pacote enviado. **Bloqueada pela agenda de terceiro** | médio | recebe o corte do criador e só legenda e normaliza; não reenquadra, não recolore, não redesenha |

**Balanço da tabela, conferido linha por linha [medido]:** 12 séries, e as quatro pilhas
somam 12.

- **Prontas hoje, com arquivo que está no disco (3):** 1, 3, 6.
- **Prontas com um gesto de minutos (2):** 7 pede **uma** foto de celular do pacote no
  cotidiano; 10 pede **uma** foto de gôndola com data visível.
- **Bloqueadas por captura (3):** 2 na versão canônica — cereja madura e bóia, Blocos D e E
  (a variante que rotula cafezal ou packshot roda hoje); 4, Blocos C, D e E; 8, Bloco A2.
- **Bloqueadas por terceiro, por um acontecimento ou por um dado que só a operação tem (4):**
  5 negociação com o parceiro; 9 o acontecimento real **mais autorização de imagem assinada**;
  11 o número de sacas do lote; 12 a agenda do criador.

---

## 5. Origem de cada série, e o que cada uma exige de verdade

### 1. Você sabia que — origem @sebastianspecialtycoffee

**Origem:** o perfil mais parecido com a Canastra da amostra — **6.276 seguidores**, um terço
da Canastra, e mediana de **~73 curtidas em reel contra ~14 em estático, 5,2× [medido]**. Não
é questão de tamanho de audiência.

O que a série exige que já existe: uma foto da camada 01 e vinte segundos de voz gravada no
celular. O que ela não exige: cenário, equipe, luz. **É o formato de menor distância entre
intenção e publicação no acervo atual.**

Assunto de cada peça vem do que a fazenda tem por direito e está escrito em EXIF: **altitude
1235–1272 m gravada no arquivo das fotos de março/2017 [medido]** — rastreabilidade que se
verifica sozinha, não alegação de marketing.

Risco: a foto é parada. O tempo médio assistido é o sinal principal **[oficial]**, e uma foto
parada com push de 4% não segura 30 s sozinha — segura a voz. Se a locução for fraca, a peça
é fraca, e o motor não conserta isso.

### 2. Infográfico sobre foto real — origem @sebastianspecialtycoffee

**Origem:** o mesmo perfil, com setas e rótulos apontando cereja contra bóia **[criador]** —
leitura nossa de uma amostra de 12 posts, não declaração da conta.

**A parte honesta:** o exemplo canônico do formato — cereja madura ao lado de bóia flutuando
na água — **não é executável hoje**. As 3 fotos de cereja da base são de fruto **verde
[medido]**, e não existe uma única foto de grão. O que *é* executável agora com a camada 01:
rotular uma foto de cafezal (fileira, espaçamento, sombra de meio-dia, a chapada ao fundo) ou
um packshot (onde está a informação de torra, de intensidade, o selo de 1985).

O que desbloqueia a versão canônica: Bloco E (cereja madura, 8 fotos) e Bloco B (grão, 25
fotos). Uma tarde, sem viagem. As quantidades são as **pedidas** no `briefing-captura.md`
**[medido]** — pedido de captura, não contagem de acervo.

### 3. Arraste para entender — origem @cafezale.com.br

**Origem:** carrossel educativo do Cafezale **[criador]** — e é honesto dizer que o Cafezale
tem **0,08% de taxa medida**, não é o perfil de melhor desempenho da amostra **[medido]**. O
formato entra porque é o de **maior vazão com o acervo parado**, não porque o vizinho vai bem
com ele.

A favor, com marca: envios por alcance é sinal declarado e pesa mais no alcance
não-conectado **[oficial]**, e conteúdo em carrossel didático é o que naturalmente se envia.
Contra: os números de engajamento por formato que circulam — **carrossel 6,9% · foto única
4,4% · reels 3,3%** — são **[criador]** de uma fonte que não sabemos qual é, amostra de uma
conta só, e não devem virar meta.

Exigência técnica que o plano do motor não cobre: o `CLAUDE.md` registra **4:5 como o alvo de
feed** e o plano do motor prevê **9:16 e 1:1** — os dois lidos nos arquivos **[medido]**. Ressalva
honesta: **a pesquisa desta base não cobriu proporção de feed**, então 4:5 aqui é convenção
interna do repositório, não número da plataforma. Ver §6.

### 4. Jornada do grão — origem @orfeucafes

**Origem:** 5 slides em tela dividida com vídeo real sem locução **[criador]**, lido no perfil
que tem **1.125 curtidas medianas com 153 mil seguidores — 0,74%, dezoito vezes o Coffee++
[medido]**.

**Bloqueada, e vale dizer o tamanho do bloqueio:** os cinco estágios pedem terreiro, sacaria,
tambor e xícara, e a base tem **zero** de cada um **[medido]**. É Bloco C (~40 fotos, uma
manhã em Uberlândia) mais Bloco D (~30, depende de safra) mais Bloco A3.

Não substitua por imagem gerada. O `briefing-captura.md` é explícito sobre colheita e
terreiro: *se não for a estação, agende*.

### 5. Cápsula com parceiro local — origem @flybyjing

**Origem:** 143 mil seguidores **[medido]**; o mecanismo — cápsulas com parceiro local por
tempo limitado, anunciadas nos dois perfis — é **[criador]**, leitura nossa.

É **a resposta mais direta ao problema "como ter frequência sem virar institucional"**: o
conteúdo novo não sai do nosso acervo, sai do encontro. Padaria, queijaria e cafeteria de
Minas são o equivalente disponível, e queijo canastra ao lado do café é a colaboração óbvia
que a região oferece de graça.

O que não fazer: escassez inventada. Se o número de unidades não é real, a peça não usa
número. É a mesma regra da série 11.

### 6. Piada relatable sem produto — origem @omsom

**Origem:** 74,9 mil seguidores **[medido]**; o mecanismo — repostar piada relatable sem o
produto aparecer, a custo de produção zero — é **[criador]**.

**Aqui o formato precisa ser adaptado, não copiado**, e o motivo é oficial: repost de print de
terceiro carrega marca d'água alheia e não é substancialmente original, os dois critérios de
elegibilidade **[oficial]**. Versão transferível: **a frase é nossa e o motor a desenha em
código** sobre a paleta da marca. Custo de produção continua zero e a peça continua elegível.

Guarda-corpo de tom: a Canastra é marca de fazenda de família, tom sério de procedência. A
piada aqui é de **reconhecimento** — *"café que esfriou não se esquenta, se aceita"* — não de
deboche. Humor escrachado **não transfere** (§7).

Guarda-corpo de mix: este é o formato mais barato do catálogo e por isso o mais fácil de
abusar. A conta já é **69% estática [medido]** e reel bate estático em **todo** perfil da
amostra. Sugestão a testar, marcada como hipótese **[criador]**: no máximo 1 peça deste
formato a cada 4 publicadas.

### 7. Meme de legenda com o pacote no cotidiano — origem @getgraza

**Origem:** 222 mil seguidores **[medido]**; o mecanismo — legenda-meme sobre foto simples do
produto no cotidiano, produto sempre herói, estética de celular, tom irônico — é **[criador]**.

E o achado contraintuitivo que o `04-arquetipos.md` desenvolve: **a origem agrícola quase não
aparece no perfil da Graza** — a prova de autenticidade vem do bastidor da empresa, não da
oliveira **[criador]**. Isso contraria o instinto de "mostrar a fazenda" e é **achado para
testar, não regra para adotar**: é marca de Nova York, tom irônico, público urbano.

Matéria-prima, com precisão: as 134 fotos de `fotos produtos cru/` **não servem** — o
`_MANIFESTO.tsv` classifica cada arquivo como `frente`, `verso` ou `lateral`, e são packshots
de catálogo **[medido]**. Cotidiano é o pacote na porta do carro, ao lado da chave, no balcão
com a louça suja. Uma foto de celular por post, cinco minutos.

### 8. Preparo em câmera lenta — origem @chamberlaincoffee

**Origem:** 541 mil seguidores **[medido]**; mecanismo — preparo em câmera lenta com legenda
emocional curta — **[criador]**.

**Bloqueada, e é a mais barata de desbloquear do catálogo inteiro:** o Bloco A2 pede **12
fotos** de coador de pano em ação — água caindo, vapor, pó molhado no filtro, mão na chaleira
**[medido]**; o clipe em câmera lenta é extensão nossa do mesmo set-up, não está no briefing.
Casa de alguém da equipe, uma tarde, celular na mão.

Restrições de captura que valem mais que a peça: **sem Modo Retrato** — o bokeh computacional
tem borda de recorte e o motor aprende o artefato; **sem flash**, **sem filtro**, **sem
tripé**. Luz de janela, sombra dura bem-vinda.

### 9. Bastidor-comemoração da família — origem @getgraza

**Origem:** o formato bastidor-comemoração da equipe, lido no perfil da Graza **[criador]**.
É prova de real sem roteiro, e no caso da Canastra é o pilar que a marca tem por direito e
está sendo tomado: **@cafedaserradacanastra publica a cada 3,9 dias construindo narrativa de
origem — "Da raiz à xícara", "Tudo começa na origem" — com 3.903 seguidores [medido]**.

Duas exigências que não são negociáveis: **autorização de uso de imagem assinada antes da
gravação**, para cada pessoa identificável; e **rosto de pessoa real nunca é sintetizado** —
foto de pessoa é foto.

Limite medido do acervo: as 13 fotos de `imagens/Arthur Rosto/` estão todas em **960×1280
[medido]**, abaixo de 1080 de largura. Servem como cartão dentro de um quadro, nunca como
fundo de tela cheia em 1080×1920 — ampliar 1,13× em rosto entrega exatamente o macio que a
peça existe para negar. Mesma aritmética do `pl.mp4`: 576 px de largura pede 1,88× para
chegar a 1080 **[medido]**, e regravar em 1080×1920 resolve sem tocar no motor.

### 10. Objeção: por que custa mais — arquétipo de objeção derrubada

**Origem:** arquétipo de conteúdo de marca de produto, levantado na pesquisa **[criador]**.
Não veio de um perfil específico da amostra.

Por que ele importa aqui e não em qualquer marca: a Canastra compete na faixa especial e três
contas ocupam o nome *Serra da Canastra* sem ser a marca **[medido]** — uma delas com 14,4 mil
seguidores e **0,05% de engajamento [medido]**, território ocupado por uma placa. Quem explica
o preço melhor ocupa o termo.

**Regra de método, e ela é dura:** o preço do outro entra na peça **fotografado na gôndola no
dia**, com a data visível, ou não entra. Número de concorrente citado de memória é afirmação
sem fonte, e esta base não tem espaço para isso. O que já está medido e pode ser usado: nossos
preços de tabela de 11/09/2026 (§1) e o **anúncio de Catálogo do Mercado Livre do
@cafedaserradacanastra — 50 cápsulas a R$ 227,90, R$ 4,56 por cápsula [medido]**.

Substituição declarada, porque a foto de colheita seletiva não existe: o beat que pediria *mão
na cereja* vira **cartão numérico** até o Bloco D acontecer.

### 11. Edição limitada real da safra — drop com número real

**Origem:** arquétipo, com a restrição escrita no próprio plano: **número real de sacas, nunca
escassez falsa** **[criador]**.

Bloqueada por **um dado**, não por captura: quantas sacas tem o lote. É uma pergunta à
operação, não uma produção.

E a lição que decide o enquadramento: **carimbo de lote, fabricação e validade são regenerados
e nunca confiáveis** (lição 22 — saiu `F:23.2025`, mês que não existe, e `F:12.2025`,
plausível, que passaria batido). Em peça que fala de safra, ou o carimbo sai do quadro, ou
entra por composição da foto real. **Plausível é pior que absurdo: o absurdo você vê.**

### 12. Convidado na mesa (coautoria) — não estava na lista, e é o mais bem medido

**Origem:** não veio das marcas fora do café; veio da medição da própria conta e da
concorrência direta **[medido]**, e por isso entra na tabela:

- Orfeu: **51 de 120 posts (42,5%) são coautoria com criador**; nos últimos 12, **7 de 12**. O
  post com @priscila_ilogti fez **8.332 curtidas**; o melhor post próprio do Orfeu na janela
  fez 4.684 **[medido]**.
- Canastra: post próprio tem mediana de **52** curtidas; **post em coautoria, 83**; e o melhor
  post da amostra é o reel do @thiago.laulima com **412 — 8× a mediana própria** **[medido]**.

**A colaboração com criador já é o conteúdo de melhor desempenho da conta, e é o que menos se
faz [medido].** Coautoria, não repost: o post nasce nos dois feeds.

O que **não** entra por aqui: envio pago a criador de um milhão de seguidores. Não transfere
(§7) — e não é do que se trata. Os números acima são de criadores de nicho.

---

## 6. O que este catálogo exige e o plano do motor ainda não cobre

Briefing, no sentido literal. Cada item é pedido de implementação, com a série que o pede:

| Capacidade | Quem pede | Estado no plano do motor |
|---|---|---|
| **Zona 4:5** para feed e carrossel | séries 3, 10 | o plano prevê **9:16 e 1:1** apenas. A função de zonas recebe `{largura, altura}`, então é extensão e não reescrita |
| **Grade de tela dividida** (2 ou 4 células, trim independente por célula) | série 4 | não previsto |
| **Camada de seta e rótulo ancorada em coordenada da imagem** | série 2 | não previsto |
| **Cartão numérico em mono, com stagger** | séries 10, 11 | `TIPO.dado` (IBM Plex Mono) existe nos tokens; o componente, não |
| **Retime / câmera lenta** | série 8 | não previsto |
| **Contador a partir de número informado** | série 11 | não previsto |
| **Composição de recorte com sombra de contato** (pacote em cena montada) | série 7, variante | é `cie/compositor.py`, que hoje **não faz recorte, reiluminação nem sombra de contato** — ver `CLAUDE.md` |

E uma armadilha de sondagem que atravessa metade da tabela, já paga duas vezes neste
repositório **[medido]**: **dimensão declarada mente**. O `pl.mp4` declara 1024×576 e é
576×1024 na tela (`displaymatrix: rotation of -90°`); os 12 packshots leem 4096×2304 e são
2304×4096 na tela (`Orientation = 6`). Quem ler `width`/`height` sem honrar a rotação
renderiza tudo deitado, em vídeo **e** em foto.

---

## 7. Mais tarde, ou nunca

Formatos que apareceram na pesquisa e **não entram na tabela mestra**, cada um com o motivo.

| Formato | Origem | Por que fica fora |
|---|---|---|
| **Comédia roteirizada com ator** | @liquiddeath, 7,2 mi **[medido]** | **Não transfere.** Fracassou no Reino Unido porque humor não atravessa fronteira, e a operação é bancada por captação de **US$ 195 milhões [terciário]** — números citados na pesquisa sem fonte registrada. A Canastra é marca de fazenda de família; o tom é procedência, não piada |
| **Flat-lay de lista relatable com objetos de estilo de vida** | @drinkpoppi, 706 mil **[medido]**; mecanismo **[criador]** | exige direção de objeto e props que não existem no acervo — e o repositório já catalogou o erro de pôr na cena objeto que não existe naquele lugar (balança de cozinha, colher de cupping e bule de ágata na lavoura são invenção). Pode voltar depois do Bloco A, com objeto que é de lá |
| **Packshot de estúdio com luz controlada** | prática de catálogo | o alvo estético é **foto de celular**: sensor pequeno, foco profundo, cantos moles, saturação lavada. Estúdio é o oposto do perfil medido do acervo |
| **Qualquer peça com rosto sintetizado** | — | proibido sem exceção. Foto de pessoa é foto |
| **Time-lapse de painel solar para o pilar de sustentabilidade** | `Direcao-Criativa.md` pede explicitamente | **zero foto de painel solar na base [medido]**. Volta quando o Bloco D acontecer — e "Carbono Zero" e "100% fotovoltaica" são os diferenciais mais fortes da marca sem uma única foto própria |
| **Sorteio para crescer seguidor** | @coffeemais, o único post fora da curva: 1.545 curtidas e **4.151 comentários [medido]** | a conta tem **269 mil seguidores e 0,04% [medido]**, contra 0,50% da Canastra. *(Leitura minha, não medição: base construída por sorteio explicaria os dois números ao mesmo tempo. Não dá para provar de fora.)* É a métrica errada para copiar |
| **Envio pago a criador de um milhão de seguidores** | prática de mercado | não transfere: depende de verba que não existe. A coautoria de nicho da série 12 é o que está medido funcionando **[medido]** |

---

## 8. Os três primeiros

Critério, na ordem em que foi aplicado: **(a)** matéria-prima no disco hoje, **(b)** menor
dependência do motor que ainda não existe, **(c)** ataque direto ao gargalo medido — 1 post a
cada 42 dias e 69% do feed estático **[medido]**.

### Primeiro: série 1, **Você sabia que** — reel

Único formato do catálogo em que **tudo** já está no disco: foto da camada 01 mais vinte
segundos de voz no celular. Ataca as duas medições ao mesmo tempo — é reel (contra os 69%
estáticos) e é barato o suficiente para repetir duas vezes por semana. É também o formato do
perfil mais parecido da amostra, que tira 5,2× mais curtida em reel que em estático com um
terço da audiência da Canastra **[medido]**.

Do motor exige o mínimo caminho do plano: foto parada com push, texto em código, legenda
karaokê, áudio normalizado. Nenhuma capacidade nova.

### Segundo: série 10, **Objeção: por que custa mais** — reel

Entra por um motivo que nenhum dos outros tem: **é o único formato da tabela que trabalha a
posição de preço**, que é a objeção real de um café especial de fazenda. A matéria-prima é
número escrito, não imagem: os preços de tabela de 11/09/2026 e o anúncio do concorrente
homônimo no Mercado Livre estão medidos (§1 e §5) — falta uma foto de gôndola com data, que é
ida ao mercado, não produção.

Do motor exige o cartão numérico em mono, que é componente novo mas pequeno, e reaproveita
tudo o mais da série 1.

### Terceiro: série 6, **Piada relatable sem produto** — estático

Entra como o formato que **fecha a semana quando a captura não aconteceu**: zero matéria-prima,
zero captura, zero geração, zero dependência de terceiro. É o único do catálogo que não
depende de ninguém além de quem escreve a frase.

Com duas cordas amarradas, porque o barato é o que se abusa: é **estático**, e a conta já está
69% estática **[medido]**; e o tom é reconhecimento, não deboche. Teto sugerido como hipótese
**[criador]**, a rever depois dos 30 dias: **no máximo 1 a cada 4 peças**.

### O que ficou de fora dos três, e por quê

- **Série 3, Arraste para entender** — matéria-prima pronta, mas depende da **zona 4:5 que o
  motor não tem** (§6). Entra assim que a zona existir; é a quarta da fila.
- **Série 12, Convidado na mesa** — é a de **melhor desempenho medido** da própria conta
  (83 contra 52, e 412 no melhor post **[medido]**), e fica fora dos três só porque depende da
  agenda de outra pessoa. **Não espere por ela: a negociação começa em paralelo à semana 1**,
  como trilha, não como render.
- **Série 8, Preparo em câmera lenta** — a mais barata de desbloquear do catálogo (Bloco A2,
  uma tarde). Deveria ser o primeiro item da lista de captura.
- **Séries 4, 5, 11** — bloqueadas por captura de safra, por negociação e por um dado da
  operação. Nenhuma das três se resolve escrevendo.

**Avaliação só depois de 30 dias**, e do conjunto, não da peça: medir no dia seguinte mede o
ranking por exploração **[oficial]**, não o formato.

**Quantas dessas três entram já, e a que ritmo, não se decide aqui.** `06-cadencia.md` §3 é a
**fonte de verdade para cadência**, e o que ele especifica é uma **rampa**, não três séries de
saída: **fase 1 (dias 1–30) roda uma única combinação, 2 posts por semana**; a segunda entra na
fase 2 (dias 31–90, 4/semana) e a terceira na fase 3 (dia 91+, 6/semana). O motivo de a fase 1
ter só uma combinação é aritmético — é a única forma de acumular 8–9 observações **do mesmo
formato** em 30 dias sem publicar 6 vezes por semana no primeiro mês.

Então a lista acima é **ordem de entrada**, não lote inicial: a série 1 abre a fase 1; as séries
10 e 6 ficam engatilhadas com estoque pronto, e entram quando a rampa as chamar.

> **Correção registrada:** esta seção afirmava que *"três séries × 2 por semana durante 30 dias
> é a receita testada"*. Duas coisas erradas numa frase. A aritmética contradizia a rampa de
> `06-cadencia.md` — 3 × 2 dá 6 posts/semana no primeiro mês, não 2. E **"testada" não se
> sustenta**: `06-cadencia.md` §3 registra que o plano chama a receita de testada mas **não
> nomeia quem testou**, e a rebaixou a **[criador]** sem autor identificável. Pela regra de
> `08-fontes.md`, isso sustenta *hipótese de teste*, não meta. A meta de **2 posts/semana** é
> que é **[medido]** — vem do piso da categoria (1,8–2,3/semana).

---

## 9. Conferência desta tabela

Executada agora, contra o passo de verificação da Tarefa 6 do plano:

- **Toda linha tem matéria-prima declarada?** Sim, 12 de 12 — cada uma com caminho de arquivo
  real ou com o bloco de `briefing-captura.md` que a desbloqueia. Nenhuma célula diz "fotos da
  fazenda" sem dizer quais.
- **Alguma linha exige coisa que a marca não tem?** Nenhuma exige **estúdio, ator, celebridade
  ou verba** — esses quatro estão em §7. **Nove das doze** exigem algo que ainda não está no
  disco, e cada uma nomeia o quê e o custo — uma foto de cinco minutos, um bloco do
  `briefing-captura.md`, uma conversa ou um número — em vez de esconder a lacuna na coluna.
  O balanço das quatro pilhas está no fim da §4 e soma 12.
- **Nenhum número sem marca?** Varrido à mão. Preços, contagens de arquivo, dimensões e
  cadências são **[medido]**; seguidores dos perfis fora do café são **[medido]** com data de
  leitura não registrada (§ `08-fontes.md`); os mecanismos lidos nesses perfis são
  **[criador]**; US$ 195 mi da Liquid Death é **[terciário]**; os segundos de duração são
  **[criador]** do harness `corte-viral`.
- **Nenhuma inferência de criador redigida como oficial?** Os percentuais de engajamento por
  formato (carrossel 6,9% · foto 4,4% · reels 3,3%) aparecem uma vez, na série 3, marcados
  **[criador]** e com a ressalva de que a fonte é desconhecida. Elegibilidade, três sinais e
  ranking por exploração aparecem como **[oficial]** e em nenhum lugar como número a bater.
- **Pseudociência?** Nenhum mecanismo causal de retenção é invocado neste arquivo. O
  vocabulário **[folclore]** da amostra — inclusive o termo neuroquímico que aparece em fonte
  após fonte sem um estudo citado — vive só em `07-nao-fazer.md`, e de propósito: a verificação
  final do plano procura esse termo fora da seção de pseudociência, e não deve encontrá-lo aqui.

Uma pendência de manutenção, não de conteúdo: a linha de `05-formatos.md` na tabela *Estado*
do `LEIA-ME.md` continua marcada como *a escrever*. Este agente não escreve em arquivo de
outro agente enquanto a sessão paralela está aberta — quem consolidar troca para *escrito*.
