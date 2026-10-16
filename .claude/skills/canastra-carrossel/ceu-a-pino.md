# Céu a pino — molde de referência

Aprovado pelo cliente em 07/10/2026, nos slides 1 e 2 do carrossel "História do Café
Canastra". O canvas aprovado está em https://claude.ai/artifact/9wwERfFSapxxPuWLP8dt7d.
O exemplo vivo fica em `saida-teste/carrossel-historia/`, mas aquela pasta é
**gitignored** e não viaja com o repositório. **Este arquivo é a fonte.**

**Quando o look não se aplica.** Céu a pino exige um assunto **ao ar livre, na
fazenda**: pacote, muda, cereja no pé, lavoura. Torra, moagem e xícara são assuntos
de interior. Eles vão em slide tipográfico (`creme` ou `terra`) ou noutro look, como a
Bancada. Não force um céu onde a cena não tem céu. E o `POLITICA-IA` §2 continua
valendo: cena que afirma fato da operação (terreiro, torrador) não se gera.

---

## 1. A foto: três blocos que o prompt não pode perder

O resto do prompt segue `canastra-cena`: anti-bokeh, celular 2017, sol a pino e
negação escrita por cena. Estes três blocos são o que faz o look:

```text
TRUE SCALE - this matters most: the package is a small 250 g bag, about 23 cm tall
and 12 cm wide. A fallen dry coffee leaf, about 12 cm long, lies on the earth right
next to it and is half the height of the package. The coffee trees are 2 metres tall
and stand 20 to 30 metres behind the package. The package must read as a small bag
on the ground, never as a large object in the field.

CAMERA POSITION: the phone lies almost flat on the earth, the lens about 8 cm above
the ground, about 70 cm in front of the subject, tilted slightly upward. Because the
camera is that low, the horizon sits low in the frame, at about 65% of the frame
height, and the ground is a narrow, strongly foreshortened strip of red earth.

FRAMING: vertical. The package stands right of centre, front facing the camera
squarely so the whole label is readable. Its base sits at about 76% of the frame
height and its top at about 44%. The distant coffee rows look low and small: their
tops reach only about 57% of the frame height, well below the top of the package.
Everything above that - the upper half of the frame, across the full width - is open
blue sky with a few white cumulus clouds. Keep the upper-left two thirds of the sky
completely free of trees, poles, wires and birds.
```

**O que a capa aprovada anexou, nesta ordem:**

- **FIRST**, o produto: a âncora de estúdio aprovada do SKU,
  `saida-teste/catalogo-estudio/<N>-<slug>/<N>.1-frente-branco.png`. Na capa foi a
  `6.1`, Clássico 250g moído. Se ela não existir nesta máquina, gere-a antes pelo
  fluxo da `canastra-embalagem` (frente em fundo branco), em vez de anexar a foto crua.
  O `compor_rotulo.py` também precisa dela, porque mascara o fundo branco de estúdio.
- **SECOND**, o lugar: `base-curada/01-real-verificada/fazenda-medeiros-1250m/cafezal/IMG_1400.JPG`,
  aberta com `exif_transpose` e reduzida a 1600 px. É a clareira de terra vermelha com
  fileiras ao fundo e céu largo. A IMG_1405 (corredor entre fileiras) deu um céu em V
  estreito, onde a manchete não coube.

O prompt abre com *"EDIT THE FIRST PROVIDED PHOTOGRAPH: take the coffee package out of
the white studio and stand it in the coffee farm shown in the SECOND photograph. Keep
the package pixel-for-pixel identical"*: é a operação nomeada (lição 12).

O `<N>` de cada SKU é a pasta de `saida-teste/catalogo-estudio/` (ex.: `1-suave-250g-moido`,
`11-canela-250g-moido`), na ordem de `scripts/prompts_catalogo.py`.

**Âncora entre decks:** `ancora-ceu-a-pino.jpg`, nesta pasta, é a faixa sem pacote da
capa aprovada. Na capa de um deck novo, anexe-a como **THIRD**, depois do produto e do
lugar, com a linha *"THIRD - style reference only: match its palette and light; do not
copy anything from it"*. *(Ainda não testada entre decks.)*

- **Faça a conta antes de enviar: o horizonte fica na altura da câmera.** Um
  assunto que passa do horizonte exige a lente no chão. Com a câmera "na altura do
  joelho" e o pacote acima das fileiras, o modelo devolve um pacote de 1 m. Foi
  reprovado pelo cliente (lição 48).
- **O assunto fica à direita e o céu livre à esquerda.** O texto mora no canto
  superior esquerdo. Peça isso no prompt; não conte com o recorte.
- **A âncora de theme-lock vai sem o produto.** Para as imagens seguintes, anexe uma
  **faixa da capa sem o pacote** (na capa de 1024×1536: `crop((0, 0, 440, 1536))`)
  como FIRST, e no fim do prompt troque "the provided reference photograph" por
  "the FIRST photograph". Com o pacote dentro da âncora, o modelo tem motivo para
  repetir o produto num slide que não é sobre ele. A faixa leva o que interessa:
  céu, terra, luz e fileiras.
- **Rótulo.** Nas rodadas da capa, o texto pequeno quebrou toda vez (`Desde 1985`,
  `TORRADO E MOÍDO`) e o grande nunca quebrou (logo, selo, `250g`). Confira cada
  campo ampliado contra a referência e cole o texto real:

  ```bash
  python -m uv run python scripts/compor_rotulo.py <gerada.png> <referencia.png> <saida.png> --preset classico-moido
  ```

  O script alinha pelo próprio rótulo com SIFT e transformação afim. Ele recusa quando
  há menos de 40 pontos ou erro acima de 1,5 px: nesse caso o pacote gerado não é cópia
  em escala da referência. Também garante 0 pixels alterados fora das caixas. O preset
  só vale para `6.1-frente-branco.png`. Para outro SKU, meça as caixas no pixel da
  referência e passe `--caixa nome=x0,y0,x1,y1`. **Texto em arco (o selo do `em grãos`)
  vai direto para cá:** soletrar não converge (lição 46).

## 2. Onde o texto pode morar: meça o céu

Antes de posicionar, meça linha a linha onde há céu. Texto preto sobre a copa de uma
árvore some, e o portão de legibilidade não vê isso, porque ele mede tamanho, não
fundo.

```python
a = np.asarray(Image.open(foto).convert("RGB")).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
lum = 0.2126 * R + 0.7152 * G + 0.0722 * B
ceu = ((B > R + 15) & (B > 120)) | ((lum > 200) & (abs(R - B) < 40))
# para cada y: o maior trecho contínuo de `ceu` é a largura útil daquela linha
```

**Como escolher o `top` da foto.** A foto entra inteira, com 1080×1620, e só o `top`
negativo decide o recorte. Escolha o valor que cumpre ao mesmo tempo:

- a última linha de texto termina **acima** do topo do assunto e **acima** do horizonte;
- a base do assunto fica **acima** de y = 1136 (onde começa a pílula, nos capítulos) ou
  de y = 1216 (borda da área segura, na capa).

Nos slides aprovados, isso deu `top: -68px` na capa e `top: -180px` no capítulo.

**Contraste medido nos slides aprovados**, no pior pixel (p1) sob cada texto:

| Combinação | Contraste |
|---|---|
| preto `#14100D` sobre o céu | de 6,0:1 a 8,6:1 |
| laranja `#E07A2E` na pílula escura | 4,3:1 (mediana 5,6:1) |
| acento oficial `#C8661E` na mesma pílula | 3,3:1, **reprova** |
| creme a 55% na pílula | 4,5:1 |

**O piso é 4,5:1.** Pelo WCAG, 34 px no quadro conta como "texto grande", com piso de
3:1. Mas no feed de 360 px esses 34 px viram 11 px, que é tamanho de texto normal, e
é no feed que se lê. Por isso a linha do tempo usa `#E07A2E`, o acento clareado
(4,3:1 no pior pixel, 5,6:1 na mediana), e não o `#C8661E`, que mal passaria no 3:1.
Laranja sobre o azul do céu dá 1,5:1 e nunca entra lá.

## 3. Os moldes de artboard (Claude Design, 1080×1350)

Fontes no `<helmet>`, numa linha do Google Fonts: `Archivo+Black`,
`Inter:wght@400;500;600` e `IBM+Plex+Mono:wght@500`. O artboard carrega o próprio
Inter 500; não dependa de `molde.FONTES_GOOGLE`, que é do render do motor e só traz
400 e 600. Todo texto sobre o céu é preto `#14100D`.

**Tetos do molde**, medidos no Chrome com as fontes carregadas em 07/10/2026:

| Campo | Medida | Teto |
|---|---|---|
| kicker (Plex 34, tracking .12em) | 24 px por caractere; `02/10` ocupa 122 px | **32** caracteres no miolo, **26** na capa (o `ARRASTE →` ocupa ~280 px) |
| número gigante (Archivo Black 270) | `1985` 672 px · `1.250` 750 px · `HOJE` 776 px · `41` 336 px | **5** caracteres. O topo do assunto tem de ficar abaixo do número onde os dois se cruzam |
| manchete da capa (Archivo Black 92) | `não é enfeite` 628 px | **14** caracteres por linha, 3 linhas |
| título do capítulo (Archivo Black 54) | `Um sonho e um` 446 px | **16** caracteres por linha, 2 linhas: **32** sem o ano. O teto 42 do campo `titulo` inclui o `AAAA · ` |
| marcos da pílula (Plex 34, tracking .06em) | 22 px por caractere; 884 px úteis | soma de **30** caracteres em 5 marcos (ex.: `CEREJA SECAGEM TORRA MOAGEM XÍCARA` cabe com 49 px entre eles) |

**Para o portão `orcamento`**, o capítulo é o tipo `conceito`: o `titulo` leva o ano
(`1985 · Um sonho e um pedaço de terra`, teto 42) e o `corpo`, o parágrafo (teto 220).
O número gigante, o kicker, a página e a pílula derivam da declaração. Os tetos deles
são os da tabela acima.

**Capa**

```html
<img src="/_blob/<ID>" alt="..." style="position: absolute; left: 0; top: -68px; width: 1080px; height: 1620px">
<div style="position: absolute; left: 64px; right: 64px; top: 206px; display: flex; justify-content: space-between; align-items: center">
<p data-campo="kicker" style="margin: 0; font-family: 'IBM Plex Mono', monospace; font-weight: 500; font-size: 34px; letter-spacing: 0.12em; color: #14100D">A HISTÓRIA DA FAMÍLIA</p>
<p data-campo="badge" style="margin: 0; font-family: 'IBM Plex Mono', monospace; font-weight: 500; font-size: 34px; letter-spacing: 0.12em; color: #F1ECE0; background: #14100D; padding: 10px 20px; border-radius: 6px">ARRASTE →</p>
</div>
<h1 data-campo="manchete" style="position: absolute; left: 60px; top: 262px; margin: 0; font-family: 'Archivo Black', Impact, sans-serif; font-weight: 400; font-size: 92px; line-height: 0.98; letter-spacing: -0.025em; color: #14100D">Linha um<br>linha dois<br>linha três.</h1>
<p data-campo="sub" style="position: absolute; left: 64px; top: 566px; width: 410px; margin: 0; font-size: 38px; line-height: 1.28; font-weight: 500; color: #14100D">Sub em coluna estreita, ao lado do produto.</p>
```

**Capítulo**: kicker e página, número gigante, título, corpo e pílula.

```html
<div style="position: absolute; left: 64px; right: 64px; top: 206px; display: flex; justify-content: space-between; align-items: center; font-family: 'IBM Plex Mono', monospace; font-weight: 500; font-size: 34px; letter-spacing: 0.12em; color: #14100D">
<p data-campo="kicker" style="margin: 0">CAPÍTULO 1 · PATROCÍNIO, MG</p>
<p data-campo="pagina" style="margin: 0">02/10</p>
</div>
<p data-campo="ano" style="position: absolute; left: 54px; top: 240px; margin: 0; font-family: 'Archivo Black', Impact, sans-serif; font-size: 270px; line-height: 0.86; letter-spacing: -0.045em; color: #14100D">1985</p>
<h2 data-campo="titulo" style="position: absolute; left: 64px; top: 478px; width: 560px; margin: 0; font-family: 'Archivo Black', Impact, sans-serif; font-weight: 400; font-size: 54px; line-height: 1.04; letter-spacing: -0.015em; color: #14100D">Título em duas linhas</h2>
<p data-campo="corpo" style="position: absolute; left: 64px; top: 606px; width: 450px; margin: 0; font-size: 34px; line-height: 1.28; font-weight: 500; color: #14100D">Corpo em coluna de 450px; termina acima do horizonte.</p>
<div style="position: absolute; left: 64px; right: 64px; top: 1136px; height: 72px; border-radius: 36px; background: rgba(20, 16, 13, 0.84); padding: 0 34px; display: flex; justify-content: space-between; align-items: center; font-family: 'IBM Plex Mono', monospace; font-weight: 500; font-size: 34px; letter-spacing: 0.06em; color: rgba(241, 236, 224, 0.55)">
<span data-campo="marco-1" style="color: #E07A2E; display: flex; align-items: center; gap: 12px"><span style="width: 14px; height: 14px; border-radius: 7px; background: #E07A2E"></span>1985</span>
<span data-campo="marco-2">1996</span>
<!-- um span por marco; só o ativo leva a cor e o ponto -->
</div>
```

- **A pílula aparece em todo slide de miolo** e marca onde o leitor está. Num deck
  cronológico, os marcos são anos. Num deck de processo ("da cereja à xícara"), são as
  etapas, com até 7 letras cada para caber nos 952px.
- **Slide `creme` ou `terra`** (tipográfico, sem foto) usa a mesma grade: linha de topo
  em y = 206, número gigante, título e corpo. Sobre terra, o texto vira creme. *(Ainda
  não validado pelo cliente: os dois slides aprovados são de foto. Mostre o primeiro
  tipográfico antes de replicar.)*
- **Fecho** assina com a logo de `marca/logo/`: a branca sobre o terra. A logo entra
  como pixel, nunca redesenhada.
- Cada artboard é um `.dc.html` completo: cabeçalho com `./support.js`, `<x-dc>`,
  `<helmet>` e o bloco `<script type="text/x-dc" data-dc-script>` com
  `renderVals() { return {}; }`. **O texto vai literal no markup, nunca em
  `{{buraco}}`**: o render local não resolve o runtime.

## 4. Montar e conferir

1. Rode `Artifact quickstart intent=design` e crie o canvas a partir do tipo Design,
   com `title` e `auto_open: after_first_write`.
2. Exporte cada foto inteira em 1080×1620 JPEG e suba como asset
   (`publish asset:true url=<canvas>`). Use o `/_blob/<id>` que voltar.
3. Publique `project/canvas.json` primeiro, com todos os artboards listados, junto com
   `Main.dc.html`. Depois publique um `.dc.html` por chamada.
4. Mapeie cada `/_blob/<id>` para o arquivo local num `blobs.json` e rode:

```bash
python -m uv run python scripts/dc_render.py <pasta-com-project> <blobs.json> <destino>
```

Ele renderiza o mesmo HTML no Chrome, roda `transbordo` e `legibilidade` do motor e
grava `<destino>/_feed/*-360.png`. **Ele não roda o `orcamento`**: declare a copy como
`Deck` e passe por `tipos.validar` antes de gerar. Para slides `foto` ainda sem imagem,
qualquer foto existente serve de provisória para o validador.

**Abra o PNG e o `_feed`.** Nos dois slides aprovados, o olho pegou três defeitos que
passaram nos portões:

- o ponto final da manchete encostava no pacote;
- a última linha do corpo caía sobre a copa escura;
- a pílula cobria a base da muda.

Os três se resolveram mexendo no `top` e no tamanho do tipo, sem gerar de novo.
