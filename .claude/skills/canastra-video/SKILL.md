---
name: canastra-video
description: Use when producing or auditing any Café Canastra moving piece — reel, vídeo de Instagram, Shorts, TikTok, motion, criativo animado, legenda queimada, kinetic type, versão 1:1 ou 4:5 de um vertical — or when writing/compiling a briefing.json for the video engine in instagram/remotion, rendering a peça, running the conferir.mjs portões, normalizing audio, or debugging why a render came out torto, mudo or with the wrong duração.
---

# Motor de vídeo — Café Canastra

O motor vive em `instagram/remotion/` e é **dirigido por briefing**:

```
briefing.json  (humano, editável)  →  compilar.mjs  →  plano.json  (gerado, selado)  →  render
```

`plano.json` é o único `--props` que as composições entendem. **Todo texto de tela é
desenhado por código, nunca por modelo generativo** — é a diferença entre esta skill e a
`canastra-conteudo`.

Quatro composições de entrega, todas o **mesmo** componente `Peca` com dimensão diferente
(`src/motor/Raiz.tsx`): `Reel` 9:16 1080×1920 · `Feed` 1:1 1080×1080 (**reenquadramento**,
não recorte) · `Feed4x5` 4:5 1080×1350 · `Larga` 16:9 **latente, não entrega** (margem de
base 51,03% da altura). `Teste` e `PonteAssets` são instrumento, não peça.

**`PecaVideo.tsx` foi apagado.** `props.json` e `scripts/gerar-props.mjs` são do motor
antigo (`cortarAntesFrames`, `manchete`, `razaoFonte`) e **nenhuma composição os lê**. Se
você se vir escrevendo `props.json`, parou no modelo errado.

| A peça é… | Skill |
|---|---|
| vídeo, reel, motion, legenda, kinetic type | **esta** |
| imagem estática gerada por modelo | `canastra-conteudo` · `canastra-estatico` |
| embalagem legível **dentro** do vídeo | esta **e** `canastra-embalagem` |
| lavoura/torrefação num frame gerado | esta **e** `canastra-cena` |

---

## 1. O que coletar antes de escrever uma linha

Todo objeto do esquema é `strictObject`: chave desconhecida **falha**. Medido —
`duracao_alvo: 24` em vez de `duracao.alvoS` devolve
`ZodError: Unrecognized key: "duracao_alvo"`, não um render de 3 s com exit 0.

| Preciso saber | Campo | Se faltar |
|---|---|---|
| que série é | `serie` | zod: um dos 13 slugs, `avulsa` inclusive |
| quantos fps | `fps` | default 30. É **campo**, não constante |
| para que superfícies | `formatos` | zod, mín. 1. Decide em quantos quadros o texto tem de caber |
| **quem manda na duração** | `duracao.modo` | **zod, sem default** |
| tempo de cada cena | `cenas[].duracaoS` | zod, `> 0` |
| **quanto tempo cada texto fica** | `cenas[].eventos[].duracaoS` | opcional e **traiçoeiro**: sem ele o evento dura **36 frames** e some, com exit 0 (§2) |
| a fonte de cada cena | `cenas[].fonte` | zod. `video` \| `foto` \| `cor` \| `grade` |
| **a razão de exibição da fonte** | `fonte.razaoExibicao` | zod. Chutada, a peça sai torta **com exit 0** |
| se a foto preenche ou não | `enquadramento` + `registro` | zod, sem default nos dois |
| o que há entre as cenas | `transicoes` | `refinar`: exatamente `cenas − 1` |
| **que som a peça tem** | `audio.locucao` / `audio.trilha` | zod exige as duas chaves; `null` é **declaração**, ausência é esquecimento. Os dois `null` → recusa `audio-mudo` |
| o gancho dos 2 primeiros segundos | `gancho` | zod, não vazio |
| o que a pessoa faz depois | `cta` | zod, não vazio. "Chama no direct" é CTA; "conheça a marca" não |
| se há fala legendada | `legenda` | opcional; exige `transcricao.json` e âncora resolvível |
| se há recorte de embalagem | `assets` | default `[]` |

**Não existe peça muda, nem com licença.** Medido em 01/10/2026: os dois `null` param o
compile com `[audio-mudo]`, e **nenhuma das 12 licenças destrava isso** — a recusa manda
"declare uma trilha, ou uma locução, ou as duas". E o repositório inteiro tem **um** arquivo
de áudio, `01-private-label/public/fonte/pl.wav`: nenhuma trilha sem voz foi gravada ou
licenciada até hoje. Então uma peça nova ou empresta aquela locução — como `03-prova-cena`
faz, e o empréstimo tem de estar **escrito** no briefing, porque a fala é sobre private
label — ou espera o áudio existir. **Não invente o arquivo**: nome declarado sem arquivo no
disco mata o render (§6).

**Os enums, medidos por erro** em 01/10/2026 (zod enumera os válidos na mensagem — sonde
antes de chutar):

| campo | valores |
|---|---|
| `serie` | `voce-sabia` `infografico` `arraste` `jornada` `capsula-parceiro` `piada` `meme-pacote` `preparo-slow` `bastidor` `objecao-preco` `safra-limitada` `convidado` `avulsa` |
| `formatos[]` | `9:16` `1:1` `4:5` `16:9` |
| `fonte.camera` | `parado` `pushLento` — só dois |
| `fonte.registro` (foto) | `moldura` `cartao` `telaCheia` |
| `enquadramento.tipo` (foto) | `faixa` `recorte` |
| `eventos[].papel` | `manchete` `dado` `etiqueta` |
| `eventos[].pista` | `topo` `principal` `tela` |
| `transicoes[].tipo` | `corte` `fade` `wipe` — `corte` dispensa `duracaoS`; `fade` pede `duracaoS`; `wipe` pede `duracaoS` **e** `direcao` (`from-left` `from-right` `from-top` `from-bottom`) |

E duas perguntas técnicas que economizam a rodada: **a fonte foi gravada deitada?** (§2) e
**o arquivo de áudio existe em `public/`?** — nenhum portão confere, e o render morre no
meio (§6).

---

## 2. Como se escreve um briefing

### Tempo em SEGUNDOS, nunca em frames

Nenhum campo está em frames; a posição de uma cena vem da **ordem no array**. A única
conversão do sistema é `emFrames(s, fps)`, chamada uma vez, em `compilar.ts`.

**Por quê:** até 01/10/2026 os tempos eram frames medidos a 30 fps e nenhuma camada de
texto lia `useVideoConfig` — a 60 fps cada entrada, saída, hold e stagger duraria metade e
a peça saía inteira, com exit 0. Agora `fps` é campo, então um número em frames
significaria coisas diferentes em peças diferentes.

Única exceção: **apara**, um deslocamento que diz de onde o arquivo começa a ser usado e
nunca posiciona nada na peça. Três nomes têm a licença e os três a carregam no nome —
`fonte.aparaAntesS`, `fonte.aparaDepoisS`, `audio.*.aparaAntesS`.

### A forma

O **menor briefing completo** que o motor aceita está em
`projetos/04-exemplo-duas-fotos/briefing.json`: duas fotos paradas, uma etiqueta em cada,
uma transição, e cada escolha justificada numa chave `_` ao lado dela. Para uma peça nova,
copiar aquele e trocar as fotos e os textos é um caminho mais curto que partir do recorte
abaixo.

Recortado de `projetos/03-prova-cena/briefing.json`, **com `duracaoS` acrescentado nos dois
eventos** — o arquivo real não o tem, e por isso os textos dele vivem 36 frames (leia o
bloco de `duracaoS` logo abaixo antes de copiar este molde). Chave que começa com `_` é
**comentário**: o `preprocess` as remove em qualquer profundidade, por isso a procedência
de uma citação pode morar ao lado dela.

```jsonc
{
  "_esquema": "canastra-briefing/1",
  "serie": "jornada", "fps": 30, "formatos": ["9:16"],
  "duracao": {"modo": "somaCenas"},
  "cenas": [
    {
      "_cena": "razaoExibicao 0,5625 MEDIDA por sondar: o container mente 1024x576.",
      "duracaoS": 4,
      "fonte": {"tipo": "video", "arquivo": "pl.mp4", "razaoExibicao": 0.5625,
                "aparaAntesS": 1.14, "enquadramento": "preencher", "camera": "parado"},
      "eventos": [{"papel": "manchete", "texto": "SUA PRÓPRIA MARCA",
                   "entradaS": 0.2, "duracaoS": 3.4, "pista": "tela", "palavraAcento": 2}]
    },
    {
      "duracaoS": 4,
      "fonte": {"tipo": "foto", "arquivo": "cafezal.jpg", "razaoExibicao": 1.333333,
                "registro": "cartao", "enquadramento": {"tipo": "faixa"},
                "camera": "pushLento"},
      "eventos": [{"papel": "etiqueta", "texto": "MEDEIROS 1250 M",
                   "entradaS": 0.5, "duracaoS": 3.0, "pista": "topo"}]
    }
  ],
  "transicoes": [{"tipo": "fade", "duracaoS": 0.5}],
  "audio": {"locucao": {"arquivo": "pl.wav", "ganhoDb": 0, "aparaAntesS": 1.14},
            "trilha": null},
  "assets": [],
  "gancho": "o pacote com a sua marca, feito na Canastra",
  "cta": "chama no direct"
}
```

`arquivo` é **só o nome** dentro de `public/fonte/`; quem concatena o prefixo é
`Fonte.tsx`, por `SUB.fonte`. Barra no campo → recusa `arquivo-com-caminho`. O briefing
fala de **medida**, não de arrumação de pasta.

### Os campos que mais confundem

**`eventos[].duracaoS` — o campo cuja ausência não dá erro nenhum.** É opcional no zod, e
sem ele o compilador escreve `duracaoFrames: 36` no evento: **1,2 s a 30 fps**. A etiqueta
entra, fica um piscar e some, e o resto da cena corre sem texto. Nada reprova: o compile
imprime o encaixe normalmente, o selo passa, o render sai exit 0.

Medido em 01/10/2026 escrevendo `04-exemplo-duas-fotos` do zero, seguindo o molde acima: as
duas cenas tinham 4 s e um evento cada, `entradaS: 0.4` e nenhum `duracaoS`. O plano saiu
com `inicioFrames: 12, duracaoFrames: 36` nos dois, e os stills dos frames 60 e 170
**saíram sem texto nenhum** — foto limpa, exit 0, nenhum aviso. Com `duracaoS: 3.4` os
mesmos dois frames trazem a etiqueta.

Regra prática: escreva `entradaS + duracaoS` um pouco **menor** que a `duracaoS` da cena
(0,4 + 3,4 = 3,8 numa cena de 4,0), para o texto sair antes do corte. E **confira num
frame do meio da cena**, nunca só no começo: no frame 20 a etiqueta de 36 frames ainda
está lá e o defeito não aparece.

**`duracao.modo`.** `somaCenas`: as cenas mandam e `alvoS`, se houver, é **conferência** —
divergir lança com os dois números. `totalFixo`: `alvoS` manda e o compilador devolve
frames às cenas, proporcionalmente, com o resto na cena mais longa. A transição **gasta**
frames, não soma: `duracaoPeca = Σ cenas − Σ transições`. Em `03-prova-cena` as cenas
somam 360 e a peça tem 345, porque o `fade` de 15 frames sobrepõe (medido).

**`razaoExibicao` é MEDIDA, não chutada** — honra a matriz de rotação:

```bash
cd instagram/remotion
node --experimental-strip-types --import ./scripts/_registrar-ts.mjs --input-type=module \
  -e "const {sondar}=await import('./src/motor/sondar.ts');for(const a of process.argv.slice(1)){const s=await sondar(a);console.log(a,'| exibe',s.largura+'x'+s.altura,'| razao',s.razao.toFixed(6),'| rotacao',s.rotacao.fonte,s.rotacao.graus,'| parada',s.imagemParada);}" \
  -- <arquivo> [<arquivo>...]
```

`<arquivo>` é **caminho no disco a partir de `instagram/remotion/`**, não o nome que vai
no briefing: `projetos/<p>/public/fonte/IMG_1398.JPG`. Rode-o **depois** de pôr os arquivos
na pasta pública do projeto, para medir o arquivo que o render vai abrir.

Os três modos de a dimensão mentir, medidos em 01/10/2026:

| arquivo | codificado | **exibe** | razão | rotação |
|---|---|---|---|---|
| `pl.mp4` | 1024×576 | **576×1024** | 0,562500 | `displaymatrix` −90 |
| `IMG_1421.JPG` | 4032×3024 | **3024×4032** | 0,750000 | `exif` 90 |
| `classico-250g.png` | 4096×2304 | 4096×2304 | 1,777778 | **`nenhuma` 0** |

O terceiro é o pior: o recorte de embalagem **perdeu** o EXIF no caminho, então `sondar()`
não tem o que descobrir e o pacote sai **deitado** com exit 0. Só nesse caso declare
`rotacaoGraus` (0/90/180/270), e ponha em `razaoExibicao` a razão **depois** do giro.
`rotacao: 'nenhuma'` num JPEG de câmera é alarme, não zero.

**`registro`** (só foto, obrigatório, sem default) — `proibicoes.md`: "foto real entra por
um registro que declara a origem, nunca como recorte flutuando".

| valor | geometria (`motor/registro.ts`) | sombra |
|---|---|---|
| `moldura` | recua 14,81% nos dois eixos, simétrico (passe-partout de terra) | `SOMBRA.papel` |
| `cartao` | recua 5% e **ancora no alto**; a sobra fica embaixo, onde a legenda corre | `SOMBRA.cartao` |
| `telaCheia` | a foto **é** o quadro | nenhuma |

**O que `cartao` de fato desenha, medido no pixel** (`04-exemplo-duas-fotos`, foto 4:3 com
`faixa` num `Reel` 9:16, still do frame 0, escala de câmera 1,00): a caixa do cartão sai em
`x 48..1031`, ou seja **4,44% de recuo lateral** — o 5% da tabela confere. Mas na vertical
ela sai em `y 591..1187`: **30,8% do quadro vazio acima** e 37,7% abaixo. A foto **não
encosta no alto**; "ancora no alto" descreve a intenção, não o que sai num 9:16. Conte com
o cartão no terço do meio e escolha o enquadramento sabendo disso.

**`enquadramento`** — `faixa` é `contain`; o outro **corta para encher**. Vídeo: string
`"faixa"`/`"preencher"`. Foto: `{"tipo":"faixa"}` ou
`{"tipo":"recorte","x","y","largura","altura"}` em **fração do arquivo já orientado**
(0..1), nunca em pixel. `telaCheia` + `faixa` é recusado: numa foto paisagem num 9:16 a
faixa deixa 57,81% de terra chapado com nome de "tela cheia". Nenhum dos dois é melhor —
medido nas 26 fotos da fazenda, 18 são `Orientation 1` (faixa = 42,19% da altura) e 8 são
`Orientation 6` (faixa = 75,00%). **Não é a mesma decisão nos dois grupos.**

**`pista`** (obrigatória em todo evento) — `topo`, `principal`, `tela`. `rodape` **não**
está na lista: é a caixa da camada `Legenda`, e um evento ali cairia sobre a fala.
`PISTA_PADRAO` em `motor/evento.ts` **não** é aplicado pelo motor — é o que esta skill
escreve no arquivo, para a escolha ficar visível no JSON.

O **encaixe é DERIVADO** de (pista, formato), nunca declarado: `tela` → cartela; sobra ao
lado do vídeo < 22% da largura → faixa sobre a imagem; senão → coluna ao lado. Não existe
campo `encaixe` de propósito — no 9:16 a sobra é 0,00 px, logo pedir coluna ali seria o
HTTP 200 que ignora o parâmetro.

**`papel`** decide três coisas que o briefing não escolhe. É assim que a coesão de série
sai de graça.

| papel | família | cadência | pista sugerida |
|---|---|---|---|
| `manchete` | Archivo Black | por **palavra** | `topo` |
| `dado` | IBM Plex Mono | por **linha** (cada linha é um campo) | `principal` |
| `etiqueta` | IBM Plex Mono | **bloco** (carimbo não tem ritmo interno) | `topo` |

`legenda` **não** é papel de evento: é camada da peça, fora da `TransitionSeries`.

**`legenda.ancora`** responde *que instante da transcrição cai no frame 0 da peça*. Com N
cenas há N `aparaAntesS` e **uma** legenda, então somar "o" apara deixa de ser definido —
a resolução é negar a pergunta: a legenda é a **fala**, e a fala tem uma fonte de áudio só.

- `{"tipo":"locucao"}` — o caso normal; lê `audio.locucao.aparaAntesS`.
- `{"tipo":"cena","indice":N}` — o **único** jeito de uma apara de cena tocar a legenda, e
  é nominal. A cena tem de ser `video`.
- `{"tipo":"segundo","valorS":X}` — valor cru.

Sem locução e sem âncora o refinador **recusa**: ele não escolhe a cena 0 por conveniência.

**As 12 licenças de técnica proibida.** Nascem desligadas; ligar uma exige `justificativa`
de 12+ caracteres, e a recusa cita a linha de `proibicoes.md` que aquela técnica derruba.
**Nenhuma das 12 está implementada** — o campo registra a decisão, o código vem depois. A
única com efeito prático é `aceitaTempoMorto`, que destrava cena sem evento e sem legenda.

---

## 3. O fluxo, com os comandos que foram rodados

### As duas partes obrigatórias da linha de comando

`scripts/compilar.mjs` importa `.ts` de `src/`. Precisa das **duas**, e cada uma que falta
dá um erro diferente — medido em 01/10/2026:

| linha | erro |
|---|---|
| `node scripts/compilar.mjs …` | `ERR_UNKNOWN_FILE_EXTENSION: Unknown file extension ".ts"` |
| `node --import ./scripts/_registrar-ts.mjs …` | **a mesma** `ERR_UNKNOWN_FILE_EXTENSION` |
| `node --experimental-strip-types …` | `ERR_MODULE_NOT_FOUND: Cannot find module '…/motor/cadencia'` |

A flag liga o type stripping; o `--import` liga o gancho que adivinha a extensão
(`moduleResolution: bundler` deixa `src/` importar sem ela, e o resolvedor ESM cru do Node
não). Sem as duas você não chega nem à validação.

**`conferir.mjs` e `normalizar-audio.mjs` se relançam sozinhos** — rode-os pelados.

```bash
cd instagram/remotion

# 0a. criar o projeto. Um projeto É uma pasta em projetos/ com briefing.json; o resto nasce
#     do fluxo (plano.json pelo compile, saida/ pelo render). Copie as fontes para dentro:
#     o briefing só nomeia arquivos que vivem na pasta pública DESTE projeto.
mkdir -p projetos/<p>/public/fonte projetos/<p>/saida
cp <as fotos, o video, o wav> projetos/<p>/public/fonte/

# 0b. o recorte de embalagem, se houver. Fail-closed: só o PNG com laudo aprovado viaja.
python -m uv run python -m instagram.recorte.publicar --projeto=01-private-label

# 1. medir a razão de exibição de cada fonte  (o one-liner de §2)
# 2. escrever projetos/<p>/briefing.json

# 3. compilar: briefing -> plano, selado duas vezes
node --experimental-strip-types --import ./scripts/_registrar-ts.mjs \
  scripts/compilar.mjs --projeto=projetos/<p>

# 4. portão 0 ANTES do render: não precisa da peça, e um plano fora de sincronia
#    invalida todos os outros portões
node scripts/conferir.mjs --portao=selo --projeto=projetos/<p>

# 5. render. --props é o plano.json; --public-dir é a pasta public/ DO PROJETO
npx remotion render src/index.ts Reel projetos/<p>/saida/reel.mp4 \
  --props=projetos/<p>/plano.json --public-dir=projetos/<p>/public
npx remotion render src/index.ts Feed projetos/<p>/saida/feed.mp4 \
  --props=projetos/<p>/plano.json --public-dir=projetos/<p>/public

# 5b. ANTES do render inteiro: um still por cena, num frame do MEIO dela. Mesmo comando,
#     trocando `render` por `still` e acrescentando --frame. É a conferência mais barata
#     que existe e é a que pega texto que entrou e já saiu (§2, duracaoS de evento).
npx remotion still src/index.ts Reel projetos/<p>/saida/still-cena1.png \
  --props=projetos/<p>/plano.json --public-dir=projetos/<p>/public --frame=60

# 6. normalizar o áudio. OBRIGATÓRIO depois de TODO render.
node scripts/normalizar-audio.mjs --projeto=projetos/<p>
node scripts/normalizar-audio.mjs --projeto=projetos/<p> --medir   # só mede

# 7. portões
node scripts/conferir.mjs --projeto=projetos/<p> --composicao=Reel
```

O compile imprime o diagnóstico de encaixe **por evento e por formato** — leia. Saída real
do passo 3 em `03-prova-cena`:

```
  duracao .............. 345 frames (11.500 s)
    cena 2 ev 0 [9:16] faixa em 'principal': corpo 310 px, 2 linha(s), mancha 16,017%
      do quadro contra o piso 6,861% (1,25x a legenda de duas linhas). DOMINA. Corpo
      SEGURADO PELO TETO de 15,500% da altura do quadro …
```

Se há legenda, o passo 2 é a transcrição: `whisper.cpp` local, modelo **multilíngue**
(`.en` é só inglês e não serve para pt-BR), instalado por `scripts/preparar-whisper.mjs`
com `WHISPER_MODELO` no ambiente — este projeto usa `small`. `transcricao.json` é um array
de `{texto, inicioMs, fimMs}` **no tempo da fonte, cru**: o rebase para o relógio da peça é
do compilador, uma vez. Leia a transcrição com os olhos antes de seguir.

### A pasta pública: uma por projeto, com subpastas

O Remotion aceita **uma** por render. Os nomes vivem em `src/motor/pasta-publica.ts`
(`SUB`) — nunca escreva `'assets/'` à mão num `staticFile`.

```
projetos/<p>/public/fonte/    pl.mp4, pl.wav, as fotos   ← SUB.fonte
projetos/<p>/public/assets/   <sku>-250g.png             ← SUB.assets (só com laudo)
projetos/<p>/public/audio/    a trilha licenciada        ← SUB.audio
projetos/<p>/saida/           reel.mp4, contato.png, …
```

Depois de publicar um recorte, **prove que o motor o enxerga**:

```bash
npx remotion still src/index.ts PonteAssets projetos/<p>/saida/ponte-assets.png \
  --public-dir=projetos/<p>/public
```

Fundo **magenta**: cor ausente dos três SKUs, então furo de alfa ou halo de recorte viram
franja rosa. `<Img>` abre `delayRender` e **mata** o render quando a imagem não carrega —
um still que sai é um still que provou a pasta pública.

---

## 4. O que esta skill recusa

Nenhum item abaixo tem portão automático. A recusa é sua.

- **Asset sem laudo.** A prova de que um recorte foi aprovado é a **presença** do arquivo
  em `public/assets/`, cuja única porta é `instagram/recorte/publicar.py`: ele só copia o
  PNG cujo `.json` irmão traz `laudo.aprovado == true`, e cada recusa sai nomeada no
  stderr. `laudoExigido` é `z.literal(true)` justamente para ninguém digitar a aprovação
  ali. **Nunca copie um PNG para `assets/` à mão** — isso transforma o portão em decoração.
- **Arquivo de `base-curada/03-mood-terceiros` ou `04-quarentena` como pixel.** Uma tem
  marca d'água, outra tem rosto identificável de quem não autorizou, as de quarentena são
  sintéticas. Servem para descrever estética em texto. **Nenhum código do motor conhece
  camada**: a regra vive aqui.
- **Texto de tela gerado por modelo.** Letra é sempre código. Tipografia desenhada por
  difusão é um sósia da marca, como o rótulo redesenhado.
- **Rosto de pessoa real sintetizado.** Foto de pessoa é foto.
- **Briefing que pede técnica proibida.** A lista é `src/identidade/proibicoes.md` e ela
  manda nesta skill. Não ligue uma licença só para "deixar registrado que queria": ligada
  e sem código, ela mente para o próximo leitor.
- **Legenda que o motor não conseguiu alinhar.** O compile imprime
  `grudados em zero ... N (maior recuo M)`. Acima de arredondamento de Whisper isso é
  âncora errada, e **ninguém reprova por você** (§6). `descartadosDepoisDoFim` é fala
  cortada por um `totalFixo` curto demais.
- **Carimbo de lote, fabricação ou validade como texto de tela.** `refinar` recusa
  `papel: "dado"` que casa `F:`/`VAL`/`LOTE`/`FAB` — lição 22 do `CLAUDE.md`: saiu
  `F:23.2025`, um mês que não existe, e `F:12.2025`, plausível e por isso pior.
- **Efeito que altera pixel dentro da embalagem** — inclusive `<CameraMotionBlur>`, cuja
  própria documentação avisa que o layered blending pode mudar cor e opacidade. E o portão
  que provaria que não alterou **não está ligado** (§6).

Os números de movimento (entrada 0,4 s, saída t^2,4, overshoot 3%, stagger 0,1 s, push
1,00→1,04) estão em `src/identidade/tokens.ts`. São **medidos**: não os ajuste no olho.

---

## 5. Os portões que existem de verdade

```bash
node scripts/conferir.mjs --portao=<nome> --projeto=projetos/<p> --composicao=Reel
```

`--portao=` aceita exatamente **seis** valores. Medido: qualquer outro devolve
`FALHA  --portao=X nao existe. Validos: todos, selo, folha, telefone, determinismo, loop.`

| # | portão | veredito | o que ele pega |
|---|---|---|---|
| 0 | `selo` | **comando** | plano fora de sincronia com o briefing, ou editado à mão |
| 1 | `folha` | olho | frame quebrado, legenda fora da área segura, corte errado |
| 2 | `telefone` | **comando** (só dimensão) + olho | legenda que só se lê no monitor |
| 3 | `determinismo` | **comando** | relógio, aleatoriedade sem semente, fonte por rede |
| 4 | `loop` | olho | o pulo na volta que faz perder a reexibição |

Outros argumentos: `--frame=` (300), `--larguraTelefone=` (360), `--entrada=`
(`src/index.ts`). Default de `--projeto` é `projetos/01-private-label` e de `--composicao`
é `Reel` — **passe os dois**, ou você confere a peça do vizinho.

**O default `--frame=300` derruba toda peça com menos de 10 s a 30 fps.** Medido em
01/10/2026 numa peça de 225 frames: o portão 3 morre com
`RangeError: Cannot use frame 300: Duration of composition is 225`, e `conferir.mjs` sai 1
**depois** de já ter escrito a folha de contato e o teste de telefone — parece que a peça
reprovou, e é só o argumento. Passe `--frame=` dentro da peça, num quadro com texto na tela
e movimento em curso:

```bash
node scripts/conferir.mjs --projeto=projetos/<p> --composicao=Reel --frame=60
```

- **Portão 0.** O único que não precisa da peça renderizada. São **dois** hashes:
  `_sha256Briefing` (de onde o plano veio) e `_sha256Plano` (ele ainda é o que saiu de lá).
  Plano sem selo **reprova por ausência**.
- **Portão 1.** O filme inteiro a 2 quadros/s num mosaico. Abra e passe o olho célula por
  célula.
- **Portão 2.** Renderiza a 360 px de largura, o tamanho em que a peça é vista de verdade:
  fonte de 78 px sobre 1080 vira 26 px aqui. **Se a legenda não se lê a 360 px, ela não se
  lê no feed de ninguém** — e a correção é corpo ou ancoragem, nunca "dá para entender".
  O veredito automático é só de dimensão.
- **Portão 3.** O mesmo frame renderizado duas vezes tem que dar o mesmo md5. Escolha um
  frame **com texto na tela e movimento em curso**: um frame preto passa em qualquer motor,
  inclusive num quebrado.
- **Portão 4.** Remux do vídeo com ele mesmo, `-c copy`, para assistir à emenda como o
  Instagram a exibe.

Exit 0 significa **"os arquivos de conferência estão prontos e as checagens duras
passaram"**, nunca "pode publicar". O script é honesto sobre isso:
`checagens duras: OK. As conferencias de olho continuam por fazer.`

---

## 6. Dívida honesta — o que o motor promete e não cumpre

Tudo medido, e a maior parte está escrita no próprio código como se funcionasse.

**`src/verificacao/ritmo.ts` NÃO EXISTE.** `ls src/verificacao/` devolve cinco arquivos:
`determinismo`, `folha`, `preservacao`, `selo`, `telefone`. E **7 comentários em 5 arquivos
de `src/`** invocam o portão de ritmo; **4 afirmam que ele reprova algo**
(`compilar.ts:210`, `compilar.ts:403`, `esquema.ts:436`, `encaixe.ts:11`). Não reprova. O
que é calculado, gravado no plano e **apenas impresso**:

| campo | quem reprova |
|---|---|
| `legenda.maiorRecuoFrames`, `grudadosEmZero`, `descartadosAntesDoInicio/DepoisDoFim` | **ninguém** — só `compilar.mjs` imprime |
| `diagnostico.eventos[].domina` | **ninguém** |
| existência de `assets[].arquivo` em `public/assets/` | **ninguém** |

A exceção real: **`semCorpoValido` reprova** no compile, código `sem-corpo-valido`,
nominalmente por formato.

E isto não é hipotético. O plano do `01-private-label`, a peça que foi **entregue**, traz
hoje em disco `grudadosEmZero: 1 · maiorRecuoFrames: 14 · descartadosAntesDoInicio: 1`: um
bloco de fala descartado por cair inteiro antes do frame 0, e outro grudado em 0 com 14
frames de recuo — acima do piso de leitura de um bloco, que é 10 frames a 30 fps
(`LEGENDA.duracaoMinSegundos = 0,333`). É exatamente a condição que `compilar.ts:403`
afirma que o portão de ritmo reprova. Ninguém reprovou, e a peça saiu.

**`src/verificacao/preservacao.ts` não está ligado a nada.** `compararRegiao` tem 9 testes
e **zero chamadores** no runtime; `exigePreservacao`, derivado de `assets.length > 0`, é
escrito no plano e lido por ninguém. O próprio arquivo avisa, em caixa alta, na primeira
linha do docstring. Motivo: para comparar uma região é preciso saber **onde** a embalagem
está no quadro, e `assets` vive no nível do briefing sem nomear cena nem retângulo. **Quem
lê aquele arquivo e conclui que o rótulo está protegido no pipeline está errado.**

**`02-jornada-do-grao` não renderiza.** Declara
`audio.trilha.arquivo = "trilha-sem-voz.wav"` e o arquivo não existe — nem a pasta
`public/audio/`. Medido em 01/10/2026, e **a nota antiga do próprio briefing está
superada**: ele não sai mudo com exit 0, ele **morre**.

```
Rendered 0/600
 http://localhost:3001/public/audio/trilha-sem-voz.wav  404 (Not Found)
An error occurred: CancelledError — Error fetching …: 404 Not Found
RENDER exit=1       ← nenhum arquivo escrito
```

`<Audio>` de `@remotion/media` chama `cancelRender`. O defeito que **sobrou** é o que custa
a rodada: **nenhum portão confere isso antes**, nem o selo — você paga o bundle inteiro
para descobrir um arquivo que faltava. Confira `public/` à mão antes de renderizar. O mesmo
briefing declara `assets: [suave-250g.png]` e a pasta `assets/` não existe: isso **não**
derruba o render (nenhuma cena usa o recorte) e **ninguém confere**.

**`03-prova-cena` não tem pasta `public/` nenhuma.** Compila e renderiza apontando para a
do vizinho, onde os quatro arquivos dele vivem — medido, exit 0, 13,3 MB:

```bash
npx remotion render src/index.ts Reel <saida>.mp4 \
  --props=projetos/03-prova-cena/plano.json --public-dir=projetos/01-private-label/public
```

**`loopar` da trilha é promessa de tipo, não garantia medida.** `@remotion/media` declara
`loop?: boolean` nas props (o `Audio` de `remotion` não declara, e lá seria atributo HTML
aceito e ignorado — razão de a camada importar do pacote certo). Mas **o efeito nunca foi
medido**: ninguém renderizou peça mais longa que a faixa e conferiu o silêncio depois do
fim. E a medição barata que o código propõe não roda aqui, porque `volumedetect` não existe
neste ffmpeg (§7).

**O selo detecta DERIVA, não falsificação.** Hash não é assinatura: quem edita
`duracaoFrames` **e** recalcula `_sha256Plano` passa pelo portão — medido. Não há segredo
no repositório, então não pode haver. Para o modo de falha real (alguém mexe num número
para testar e esquece de desfazer) deriva é o que importa. **Não escreva em lugar nenhum
que o plano está "protegido contra alteração".**

**Nenhuma das 12 licenças de técnica está implementada.** O campo registra a decisão.

---

## 7. Armadilhas de plataforma, todas pagas nesta máquina

Medidas em 01/10/2026, Node v22.16.0, Windows.

**`--props` com JSON inline não funciona no shell do Windows** — as aspas somem antes de
chegar ao Remotion. Passando `--props='{"duracaoFrames":90,"fps":30}'`:

```
You passed --props but it was neither valid JSON nor a file path to a valid JSON file.
Provided value: {duracaoFrames:90,fps:30}
```

Sempre arquivo. E o arquivo é `plano.json`, não `props.json`.

**O ffmpeg do Remotion é build reduzida.**
`node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe` publica **42 filtros**
(`-filters`, contado hoje). Não tem `fps`, `tile`, `ebur128`, `volumedetect` nem `select`.
Tem `loudnorm` — por isso a medição de loudness é feita por ele em modo de análise. A
mensagem para `fps=2` é enganosa (`No option name near '2'`, que parece erro de sintaxe);
só `fps=fps=2` revela `No such filter: 'fps'`. Amostragem se faz com `-r`, que é opção de
saída, e mosaico se monta em Node com `pngjs`. `ffprobe`/`ffmpeg` **não estão no PATH**, e
`execFile('npx', …)` devolve ENOENT no Windows: chame o binário por caminho absoluto, sem
shell.

**No PowerShell, `"$par[0]"` interpola errado:**

```powershell
$par = @('alfa','beta')
"errado: $par[0]"      # -> errado: alfa beta[0]
"certo: $($par[0])"    # -> certo: alfa
```

**Camada `.tsx` que importa `identidade/tipografia.ts` derruba o vitest.** `loadFont` roda
no **topo do módulo** e o ambiente de teste é `node`, sem `document`. O modo de falha é
traiçoeiro — um teste que só importa `Legenda.tsx` **passa a asserção** e o vitest ainda
sai 1:

```
 Test Files  1 passed (1)        Tests  1 passed (1)        Errors  1 error
Caused by: TypeError: Invalid URL
  input: '/src/identidade/fontes/ArchivoBlack-Regular.ttf'
exit=1
```

É por isso que nada que precise de prova mora num `.tsx` (`tempo-de-cena.ts`,
`movimento.ts`, `texto-forma.ts`, `pista.ts` existem como arquivos separados por essa razão
mecânica) e por isso que `esquema.ts` usa **zod puro**, sem `@remotion/zod-types`.

**Depois de qualquer re-render o áudio volta ao nível cru.** O Instagram entrega a −14
LUFS; o MP4 sai longe disso. Medido num render novo de `03-prova-cena` feito hoje:
**−18,19 LUFS integrado, pico real +0,22 dBTP** (o `reel.mp4` de `01-private-label` deu
−23,02 em 30/09 — o número varia com a mistura; nunca é −14). Rode `normalizar-audio.mjs`
**outra vez**. Ele copia com `-c:v copy`, então nenhum pixel muda e nenhum portão é
invalidado, e é idempotente. Quando o ganho não cabe sob o teto de pico ele cai para o modo
dinâmico e **avisa** — leia o aviso e ouça a peça.

**Menores:** `trimAfter` foi descontinuado em favor de `durationInFrames`; `z-index` não
existe no Remotion (ordem de camada é ordem da árvore); `--scale` aceita número que quebra
a proporção em silêncio (`0.333` sobre 1080×1920 dá still 360×639 e render 360×638, porque
o h264 exige lado par) — nunca digite a escala, derive de `escalaParaLargura()` em
`verificacao/telefone.ts`, que recusa lado ímpar.

---

## Licença e registro

Remotion é gratuito para uso comercial até **3 pessoas** (`remotion.pro/license`). Se a
Canastra passar disso, é preciso comprar licença antes de usar em produção. Confirme com o
usuário, não presuma.

Erro que custou uma rodada vira lição no `Registro de lições` do `CLAUDE.md`, no formato
**sintoma → causa raiz → regra**. Erro não registrado se repete na próxima sessão, que não
tem a memória desta.
