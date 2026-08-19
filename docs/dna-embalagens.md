# DNA das embalagens Café Canastra

> ## ⚠️ A premissa central deste documento está SUPERADA
>
> Este arquivo foi escrito na tese de que "a fidelidade da embalagem vem da descrição
> escrita". Isso produz um **sósia** da marca — plausível, nunca correto. O teste
> seguinte derrubou a tese: com **image guidance** via `/images/edits`, e o prompt
> **sem uma palavra** sobre a arte do pacote, o logotipo sai muito mais próximo do
> real — inclusive na crista da serra, que passa atrás de "Café", detalhe que
> nenhuma versão descrita em prompt acertou.
>
> **Leia `docs/flow-geracao.md` primeiro.** Ele define o fluxo correto.
>
> O que continua válido aqui: a **descrição física de cada SKU** (material, cor da
> tinta, blocos de texto, diferenças entre Suave, Clássico e Canela), útil como
> referência humana e para escolher a imagem-fonte certa. O que **não** deve ser
> usado: os blocos de prompt que descrevem a arte, e a recomendação de modelo.

Especificação verificada contra os packshots reais em
`base-curada/01-real-verificada/torrefacao-uberlandia-875m/`.

---

## Estrutura comum aos 3 SKUs

Saco de papel/filme de **fundo chato** (block bottom), 250 g, com **sanfona lateral**
que dobra para dentro. **Nitidamente mais alto que largo**, cerca de 3 de altura por
2 de largura.

O topo é uma **dobra prensada reta** — sem zíper, sem trilho plástico, sem cursor.
Isto precisa ser dito e negado explicitamente: o modelo tende a produzir doypack com
zip-lock, que é a embalagem errada.

Na frente, acima da arte, um **respiro redondo em relevo** com um único ponto escuro
no centro.

Arte da frente, de cima para baixo, idêntica em layout nos três:

1. **Serra**, em traço fino e solto. **Crista baixa, larga, de topo quase plano** —
   uma chapada, escarpa de planalto, com a borda superior quase horizontal, entalhes
   rasos e irregulares, e um ponto alto arredondado. Estrias verticais na face.
   **Não é montanha alpina, não são picos triangulares.** Três marquinhas em V de
   aves voando no alto à esquerda.
2. **"Café"** pequeno, em script manuscrito inclinado, sobreposto à serra, um pouco à
   direita do centro. **Com acento agudo no "e".**
3. **"CANASTRA"** muito grande, em **script de pincel seco**, traços irregulares e
   parcialmente falhados, com a fibra do papel aparecendo através da tinta. Não é
   fonte vetorial limpa.
4. **Swash** de pincel pesado por baixo de CANASTRA, grosso à esquerda começando como
   um borrão e afinando até ponta à direita.
5. **®** minúsculo no alto à direita do A final.
6. **"Desde 1985"** pequeno e manuscrito, abaixo à direita, acima da ponta fina do swash.
7. Bloco de identificação do SKU (varia — ver abaixo).
8. Canto inferior direito: retângulo de cantos arredondados com **"250g"**.

## O que muda em cada SKU

| | **Suave** | **Clássico** | **Canela** |
|---|---|---|---|
| Material | papel **kraft** natural, fibroso, mate | filme **preto mate** | filme **vermelho metalizado brilhante** |
| Cor da tinta | **preta** | **branca** | **branca** |
| Bloco do SKU | caixa de linha fina: `SPECIALTY` / `ESPECIAL` / `SCA 80+` | idem, em branco | **não tem caixa** |
| Texto inferior esq. | `SUAVE` / `TORRADO E MOÍDO` | `CLÁSSICO` | `CAFÉ TORRADO E` / `MOÍDO COM CANELA` |
| Elemento extra | — | — | desenho de **canela em rama** amarrada, no canto inferior direito acima do 250g |
| Superfície | mate, sem reflexo | mate, reflexo difuso amplo | **especular forte**, faixas de brilho, banding de cor |
| ISO real do packshot | 105–124 | 365–698 | 950–1018 |

O `MOÍDO` leva **acento agudo no I**. O modelo erra isso com frequência e escreve
`MOIDO` — vale repetir a palavra acentuada no prompt.

O verso dos três traz QR de rastreabilidade, `SEM GLÚTEN`, medidores de `TORRA` e
`INTENSIDADE`, ícone de montanha com `ALTITUDE 1.250 METROS`, `SUGESTÃO DE PREPARO`
em bullets, selo circular `PLANTIO PRÓPRIO DIRETO DO PRODUTOR — 1985`, código de
barras e `www.cafecanastra.com`. O verso quase nunca é o que a foto quer mostrar;
está aqui para não ser usado como referência por engano.

---

## Bloco de prompt verificado — Suave

Testado em 5 gerações, todas com o logotipo correto e legível.

```text
The coffee package is a 250g flat-bottom kraft paper pouch, natural unbleached brown
paper, visibly fibrous, with soft vertical creases and inward side gussets. It is
noticeably TALLER THAN WIDE, roughly 3 units tall to 2 wide. The top is a straight
crimped fold, not a zip lock, not a plastic slider. A small round embossed degassing
vent with one dark centre dot sits on the front panel above the artwork.

All artwork is a single flat matte BLACK ink printed straight onto the bare kraft. No
white label, no sticker, no second colour, no gloss, no foil.

The artwork, top to bottom:
  - A mountain range drawn in thin sketchy open line. CRITICAL: this range is a LOW,
    WIDE, FLAT-TOPPED TABLELAND - a plateau escarpment whose upper edge runs almost
    HORIZONTAL with only small shallow irregular notches and one gentle rounded high
    point, with fine vertical striations down its face. It is emphatically NOT an
    alpine mountain, NOT sharp triangular peaks, NOT tall pointed summits. It is a
    long flat mesa ridge, wider than it is tall, sitting low behind the lettering.
    Three tiny V-shaped bird marks fly at its far upper left.
  - Overlapping and in front of that ridge, slightly right of centre: the word "Cafe"
    written small in a slanted handwritten script - and it MUST carry an ACUTE ACCENT
    over the final e, reading "Cafe" with the accent mark, never a bare e.
  - Directly below, very large: "CANASTRA" in a thick DRY BRUSH script. The strokes
    are uneven and partly broken, with the paper fibre showing through the ink in
    places, the way a loaded brush skips on rough stock. Not a clean vector font.
  - A single heavy tapering brush swash sweeps underneath "CANASTRA", thick at its
    left end where it starts as a blob and thinning to a point at the right.
  - A very small (R) registered trademark symbol at the upper right of the final A.
  - "Desde 1985" small and handwritten, to the lower RIGHT, just above the swash tip.
  - Below, centred: a thin single-line rectangle outline containing three stacked
    lines - "SPECIALTY" small and letterspaced, "ESPECIAL" large and bold, "SCA 80+"
    small.
  - Bottom left, small sans-serif caps, two lines: "SUAVE" over "TORRADO E MOIDO",
    where MOIDO carries an acute accent on the I.
  - Bottom right: a small rounded rectangle outline containing "250g".

The package is the subject of the photograph. Every one of those words must be
legible and spelled exactly as written.
```

Para **Clássico**, troque o parágrafo do material e da tinta por: filme preto mate,
tinta **branca**, e o texto inferior esquerdo por `CLASSICO`. Para **Canela**: filme
vermelho metalizado com reflexo especular em faixas, tinta **branca**, **remova** a
caixa `SPECIALTY / ESPECIAL / SCA 80+`, acrescente um desenho de canela em rama
amarrada no canto inferior direito, e o texto inferior esquerdo em duas linhas,
`CAFE TORRADO E` / `MOIDO COM CANELA`.

## Bloco anti-bokeh — obrigatório

Sem isto o modelo entrega anúncio de produto com fundo desfocado. E **desfoque não
se desfaz em pós-processamento** — testado: tone mapping, ruído, halo e artefato de
JPEG se adicionam depois, profundidade de campo rasa não se remove. Tem que morrer
na geração.

```text
CRITICAL - EVERYTHING IN THIS FRAME IS SHARP. This was taken on a phone with a tiny
1/1.7 inch sensor, which at f/1.8 gives an enormous, almost infinite depth of field.
The near edge of the table, the package, AND the coffee bushes twenty metres up the
hillside behind are ALL equally crisp and fully resolved. You can count the
individual leaves on the distant bushes. The background is exactly as sharp as the
foreground - NO focus falloff anywhere, NO blur, NO softness, NO separation between
subject and background. The far hills are hazy from atmosphere only, never from
defocus.
```

Negativo que acompanha:

```text
blurred background, defocused background, out of focus foliage, blurry leaves, bokeh,
bokeh balls, depth of field falloff, subject separation, soft backdrop, shallow focus,
selective focus, portrait mode, lens blur, rim light, golden hour rim lighting, studio
lighting, softbox, product photography, catalogue photography, advertisement,
commercial product shot, hero shot, styled set, food styling, sharp triangular
mountain peaks, alpine summits, white rectangular label, sticker, glossy foil, zip
lock top, plastic slider, warped text, distorted logo, gibberish lettering, missing
accent, watermark, 3d render, CGI, illustration
```

---

## Modelo recomendado

**`grok-imagine-image-2.0` com `quality: "medium"` e `resolution: "2k"`.** US$ 0,08
por imagem, saída nativa 1776×2368.

Evidência da comparação, mesma cena e mesmas referências:

| Modelo | Preço | Saída | Fidelidade da embalagem |
|---|---:|---|---|
| `grok-imagine-image` | $0,02 | 864×1152 | pior — serra mais errada, layout deslocado |
| `grok-imagine-image-quality` | $0,05 | 864×1152 | boa; pincel mais próximo do real |
| `grok-imagine-image-2.0` med/2k | $0,08 | **1776×2368** | **melhor** — tipografia mais nítida, aceitou todas as correções |

Dois motivos decidem, e os dois são irrecuperáveis em pós:

1. **Resolução.** O feed 4:5 do Instagram quer 1080×1350. Os outros dois modelos
   entregam 864×1080 depois do recorte — **abaixo da especificação**, exigindo
   ampliação. O `-2.0` em 2k entrega 1776×2220 e desce para 1080×1350 com folga.
2. **Tipografia.** Detalhe de letra não se adiciona depois. O `-2.0` é o único que
   resolve `SCA 80+`, `Desde 1985` e o `®` de forma consistentemente limpa.

O contra do `-2.0` é o viés forte para fotografia comercial polida — e é por isso
que o bloco anti-bokeh acima não é opcional. Com ele, o `-2.0` produz cena de
celular. Sem ele, produz anúncio.

`grok-imagine-image` a US$ 0,02 está descartado: economiza 6 centavos e erra mais a
marca, que é o ativo que o projeto existe para proteger.

## Parâmetros da API confirmados

- Proporções aceitas: `1:1`, `3:4`, `4:3`, `9:16`, `16:9`, `2:3`, `3:2`, `9:19.5`,
  `19.5:9`, `9:20`, `20:9`, `1:2`, `2:1`, `auto`.
- **`4:5` não existe.** Gerar em `3:4` (0,750) e recortar a altura até 4:5 (0,800),
  tirando ~62% da sobra do topo. Perda de ~6% da altura.
- Referência nativa: campo `image_url`, **lista de data URIs**. Até 4 aceitas.
  Referência de 2048 px no lado maior é aceita.
- `-2.0` aceita `quality` apenas em `low` e `medium` (`high` devolve 400), e
  `resolution` em `1k` e `2k`.
- `/images/edits` existe e aceita `image_url` como lista. `/images/variations` não
  existe (404).
- `seed` e `strength` passam a validação.

---

## Erros residuais conhecidos

Ainda presentes na melhor configuração, em ordem de importância:

1. **A serra fica acima e separada do texto.** No pacote real ela envolve e passa
   **atrás** de "Café". Nas gerações ela flutua acima do conjunto.
2. **`MOÍDO` sai sem acento** em boa parte das gerações.
3. **Posição do ®** oscila — às vezes sobre o A final em vez de à direita dele.
4. **Letras de CANASTRA mais regulares** que o original, que tem linha de base
   irregular e mais falha de tinta.
5. Composição ainda tende ao centro e ao "herói de produto", mesmo com o negativo.

Nenhum deles é bloqueante para publicação, mas 1 e 2 são os que um cliente atento
percebe. Onde o logotipo precisar ser exato ao pixel — anúncio pago, e-commerce,
rótulo —, use **composição do recorte real** em vez de geração. O recorte limpo do
Suave frontal está em `saida-teste/recorte-suave-frontal.png`.

## Histórico de correção

A **v1** deste documento descrevia a serra como `jagged peaks`. Os três modelos
desenharam, fielmente, picos alpinos pontudos — errados. O erro não era do modelo:
era da especificação. A **v2** corrigiu quatro pontos e todos passaram a sair certos:
topo plano de chapada, acento em `Café`, símbolo `®`, e pincel seco com falha de
tinta em vez de vetor limpo.

Isto é o que torna este arquivo o ativo crítico: **o modelo é obediente. Ele erra
exatamente onde a descrição erra.**
