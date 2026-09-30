---
name: canastra-video
description: Use when producing or auditing any Café Canastra moving piece — reel, vídeo de Instagram, Shorts, TikTok, motion, criativo animado, legenda queimada, kinetic type, corte de pitch, versão 1:1 de um vertical — or when a rendered video needs to pass the verification gates before delivery.
---

# Motor de vídeo — Café Canastra

Reel 9:16 e post de feed 1:1, legendados, com o motion escrito em código. O motor
vive em `instagram/remotion/`. **Todo texto de tela é desenhado por código, nunca
por modelo generativo** — é a diferença entre esta skill e a `canastra-conteudo`,
que trata de imagem gerada.

A peça só é entregue depois de passar pelos quatro portões. Eles não são
opinião; três são comando e um é olho obrigatório.

---

## Rotear primeiro

| A peça é… | Skill |
|---|---|
| vídeo, reel, motion, legenda, kinetic type | **canastra-video** (esta) |
| imagem estática gerada por modelo | `canastra-conteudo` |
| a embalagem aparece legível **dentro do vídeo** | esta **e** `canastra-embalagem` |
| cenário de lavoura/torrefação num frame gerado | esta **e** `canastra-cena` |

Se a embalagem entra no quadro do vídeo, o rótulo obedece à `canastra-embalagem`
do mesmo jeito que numa foto: letra por letra, conferido ampliado.

---

## Antes de escrever uma linha: o que coletar

Não comece sem estas cinco respostas. Faltando qualquer uma, **pergunte**.

1. **A fonte** — arquivo de vídeo ou fotografia, e de onde veio. Se for fotografia,
   ela obedece às camadas de `base-curada/` (`03-mood-terceiros` e `04-quarentena`
   **nunca** viram pixel).
2. **Duração alvo** — e para qual superfície (Reel, Shorts, feed).
3. **O gancho** — o que prende nos primeiros 2 segundos. Sem gancho declarado, a
   peça é um vídeo sem motivo.
4. **O CTA** — o que a pessoa faz depois. "Chama no direct" é CTA; "conheça a
   marca" não é.
5. **Os formatos** — 9:16 sempre; 1:1 quando também vai para o feed. O 1:1 **não é
   recorte** do 9:16 (ver `layout()`).

E uma sexta, técnica, que economiza a rodada inteira: **a fonte foi gravada
deitada?** Ver `sondar()` logo abaixo.

---

## Pipeline, em ordem

```bash
cd instagram/remotion
```

1. **Sondar a fonte** — `src/motor/sondar.ts`. Devolve a dimensão de
   **exibição**, com a matriz de rotação já aplicada. Nunca leia `width`/`height`
   do container: `02 PL.mp4` está gravado 1024×576 com `rotation -90` e exibe
   576×1024. Ler o container e renderizar por ele deita a peça inteira.
2. **Medir o ar morto e os silêncios** — o começo mudo se corta por
   `cortarAntesFrames`, nunca na edição manual. No `02 PL.mp4` são 1,14 s = 34
   frames a 30 fps.
3. **Transcrever** — `src/legenda/transcrever.ts`, whisper.cpp local, modelo
   **multilíngue** (`.en` é só inglês e não serve para pt-BR). Leia a transcrição
   com os olhos antes de seguir.
4. **Agrupar** — `src/legenda/agrupar.ts`. Teto de **2 palavras por bloco**,
   mínimo de 10 frames por bloco, corte seco sem easing.
5. **Escrever o `props.json`** — `--props` com JSON inline **não funciona no
   shell do Windows** (as aspas somem). Sempre arquivo.
6. **Renderizar os dois formatos** — `--public-dir` é a pasta `public/` do
   projeto, **não** a `fonte/`:

```bash
npx remotion render src/index.ts Reel projetos/<p>/saida/reel.mp4 \
  --props=projetos/<p>/props.json --public-dir=projetos/<p>/public
npx remotion render src/index.ts Feed projetos/<p>/saida/feed.mp4 \
  --props=projetos/<p>/props.json --public-dir=projetos/<p>/public
```

7. **Normalizar o áudio** — **obrigatório depois de todo render.** O MP4 sai do
   Remotion a −23 LUFS e o Instagram entrega a −14; sem este passo a peça toca
   baixa no feed.

```bash
node scripts/normalizar-audio.mjs --projeto=projetos/<p>
node scripts/normalizar-audio.mjs --projeto=projetos/<p> --medir   # só mede
```

   Ele copia com `-c:v copy`, então **nenhum pixel muda e nenhum portão é
   invalidado**. É idempotente. Se você re-renderizar, rode de novo — medido em
   30/09/2026: render → −23,02 LUFS; normalização → −14,28 LUFS / −0,92 dBTP.

8. **Passar os portões** — `node scripts/conferir.mjs` (abaixo).

---

## A pasta pública: uma por projeto, com subpastas

O Remotion aceita **uma** pasta pública por render. Duas coisas disputavam esse
argumento — o vídeo cru do projeto e os recortes de embalagem — e a convenção que
resolveu é uma pasta pública por **projeto**, com subpastas nomeadas:

```
projetos/<p>/public/fonte/    pl.mp4, pl.wav       ← Fonte.tsx, staticFile('fonte/…')
projetos/<p>/public/assets/   <sku>-250g.png       ← staticFile('assets/…')
projetos/<p>/saida/           reel.mp4, feed.mp4, contato.png, …
```

Tudo sob `public/` e `saida/` é gitignored. Os nomes de subpasta vivem em
`src/motor/pasta-publica.ts` (`PASTA_PUBLICA`, `SUB`) — **nunca escreva
`'assets/'` à mão num `staticFile`**, use `SUB`.

No `props.json`, `arquivo` é só o nome (`pl.mp4`), sem prefixo: quem concatena
`fonte/` é a camada `Fonte.tsx`. O props fala de medida, não de arrumação de pasta.

### Levar um recorte de embalagem para dentro do vídeo

O recorte aprovado entra pelo portão de publicação, nunca copiado à mão:

```bash
python -m instagram.recorte.publicar                     # projeto padrão
python -m instagram.recorte.publicar --projeto=02-outro
```

Ele copia de `instagram/assets/embalagem/` só o PNG cujo `.json` irmão traz
`laudo.aprovado == true`. É **fail-closed**: PNG sem laudo, laudo truncado ou
`laudo: null` não viajam, e cada recusa sai nomeada no stderr.

**Depois de publicar, prove que o motor enxerga** — a etapa que separa a ponte
escrita da ponte funcionando:

```bash
npx remotion still src/index.ts PonteAssets projetos/<p>/saida/ponte-assets.png \
  --public-dir=projetos/<p>/public
```

Abra o PNG. As embalagens aparecem sobre **magenta**, cor que não existe em
nenhum dos três SKUs, então furo de alfa ou halo de recorte viram franja rosa.
O still é portão de verdade: com a pasta pública errada o `<Img>` dá 404 e o
render **morre sem escrever arquivo** (conferido em 30/09/2026 — exit 1).

---

## Os quatro portões — regra dura, não sugestão

```bash
node scripts/conferir.mjs
node scripts/conferir.mjs --portao=determinismo --frame=300
```

O script sai com código 0 quando as **duas checagens duras** passam. Isso não é
aprovação: os portões 1 e 4 produzem material para o olho, e o olho é obrigatório.

| # | Portão | Veredito | O que ele pega |
|---|---|---|---|
| 1 | folha de contato | olho | frame quebrado, legenda fora da área segura, corte errado |
| 2 | telefone (360 px) | comando + olho | legenda que só se lê no monitor |
| 3 | determinismo | comando | relógio, aleatoriedade sem semente, fonte por rede |
| 4 | emenda de loop | olho | o pulo na volta que faz perder a reexibição |

**Portão 1 — folha de contato.** O filme inteiro amostrado a 2 quadros por
segundo, num mosaico. Abra o PNG e passe o olho célula por célula.

**Portão 2 — telefone.** Renderiza a 360 px de largura, que é o tamanho em que a
peça é vista de verdade. Fonte de 78 px sobre 1080 vira 26 px aqui. **Se a
legenda não se lê a 360 px, ela não se lê no feed de ninguém** — e a correção é
aumentar o corpo ou mudar a ancoragem, nunca "dá para entender".

**Portão 3 — determinismo.** O mesmo frame renderizado duas vezes tem que dar o
mesmo md5. Sem isso não existe versão aprovada, só o arquivo que alguém baixou.
Escolha um frame **com legenda na tela e movimento em curso**: um frame preto
passa em qualquer motor, inclusive num quebrado.

**Portão 4 — loop.** Remux do vídeo com ele mesmo, `-c copy`, para assistir à
emenda como o Instagram a exibe.

---

## Armadilhas medidas nesta máquina

Todas custaram uma rodada. Nenhuma é inferida.

- **A dimensão codificada mente.** `displaymatrix: rotation of -90°`. Ver a lição
  25 do `CLAUDE.md`.
- **A mesma mentira existe na foto parada, por `EXIF Orientation`.** Medido em
  30/09/2026: os três recortes de embalagem são PNG 4096×2304 (deitado) porque os
  três JPEG de origem trazem `Orientation=6` (girar 90°) e o pipeline de recorte
  leu o buffer cru sem aplicar. Em pé seriam 2304×4096. **Não corrija girando na
  composição** — isso deixa o still bonito e o asset continua deitado em toda peça
  futura. A correção é no recorte. Antes de usar qualquer PNG de
  `instagram/assets/embalagem/`, confira `Image.open(f).getexif().get(274)` na
  foto de origem.
- **O ffmpeg do Remotion é build mínima.** `node_modules/@remotion/compositor-*/ffmpeg.exe`
  publica ~50 filtros e **não tem `fps` nem `tile`**. A mensagem para `fps=2` é
  enganosa (`No option name near '2'`, que parece erro de sintaxe); só
  `fps=fps=2` revela `No such filter: 'fps'`. Amostragem se faz com `-r`, que é
  opção de saída, e mosaico se monta em Node.
- **`--scale` aceita número que quebra a proporção, em silêncio.** `--scale=0.333`
  sobre 1080×1920 dá still 360×639 e **render 360×638** — o h264 exige lado par e
  o Remotion desce 639 para 638 sem avisar. 360/638 não é 9:16. Nunca digite a
  escala: derive de `escalaParaLargura()`, que recusa lado ímpar.
- **`ffprobe` e `ffmpeg` não estão no PATH** e `execFile('npx', …)` devolve ENOENT
  no Windows (o `npx` é um `.cmd`). Chame o binário do Remotion por caminho
  absoluto, sem shell.
- **`trimAfter` foi descontinuado** em favor de `durationInFrames`.
- **`z-index` não existe** no Remotion; ordem de camada é a ordem da árvore.

---

## O que nunca fazer

A lista completa é `instagram/remotion/src/identidade/proibicoes.md`, e ela manda
nesta skill. Leia antes de desenhar movimento. As quatro que mais aparecem:

- **Nenhum efeito altera pixel dentro da embalagem** — nem `<CameraMotionBlur>`,
  que a própria documentação avisa que "layered blending pode mudar cor e
  opacidade". O portão de preservação (`src/verificacao/preservacao.ts`) existe
  para provar que não alterou.
- **Letra é sempre código.** Texto de tela desenhado por modelo generativo é um
  sósia da tipografia da marca, do mesmo jeito que o rótulo redesenhado é um
  sósia do rótulo.
- **Push de câmera lento, nunca impacto.** 100% → 103–106% ao longo da cena.
- **Um elemento dominante e um acento de cor por cena.** Fundo branco puro com
  texto centrado é o que o modelo entrega quando não há direção — é sintoma, não
  estilo.

Os números de movimento (entrada de 12 frames, saída em t^2.4, overshoot de 3%,
stagger de 3 frames) estão em `src/identidade/tokens.ts`. São **medidos**, não
escolhidos: não os ajuste no olho.

---

## Licença

Remotion é gratuito para uso comercial até **3 pessoas** (`remotion.pro/license`).
Se a Canastra passar disso, é preciso comprar licença antes de usar em produção.
Confirme com o usuário, não presuma.
