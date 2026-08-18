# Fluxo de geração de imagem — Café Canastra

Documento de arquitetura. Substitui a premissa de `docs/dna-embalagens.md`.

## A regra que organiza tudo

> **A embalagem entra como pixel, nunca como texto.**
>
> Descrever o logotipo no prompt e pedir para o modelo desenhar produz um sósia da
> marca. Pode ficar bonito, pode ficar convincente, e vai estar errado — porque o
> modelo está inventando a identidade, não reproduzindo.

O caminho é **image guidance**: a foto real do pacote é a entrada, e o prompt só
descreve o que muda em volta.

---

## Os três fluxos possíveis, e quando usar cada um

### 1 · `/images/edits` com a foto real — **padrão**

A imagem-fonte é o packshot. O prompt manda preservar o pacote e descreve o novo
ambiente. A arte da embalagem vem dos pixels reais.

**Schema — este é o ponto onde é fácil errar:**

```json
{
  "model": "grok-imagine-image-2.0",
  "prompt": "<preservação + ambiente + foco + estética>",
  "image": { "url": "data:image/jpeg;base64,...", "type": "image_url" },
  "n": 3,
  "quality": "medium",
  "resolution": "2k"
}
```

`image` é **objeto** com `url` e `type: "image_url"`. Não é string, não é
`image_url` em lista. Passar `image_url` devolve **HTTP 200 e ignora a imagem** —
o endpoint gera do texto e você não percebe que o guidance nunca foi aplicado.
Foi exatamente esse falso positivo que atrasou o projeto.

Até 3 imagens-fonte por requisição, para combinar sujeitos ou compor cena.
Não existe parâmetro de `strength`, `fidelity` ou máscara — `seed` e `strength`
passam validação mas não estão documentados e provavelmente são ignorados.

**Resultado medido:** crista da serra com o perfil real, passando atrás de "Café";
swash como borrão à esquerda com rastro de pincel seco; letras de CANASTRA com a
irregularidade do original; topo prensado sem zíper; sanfona lateral. Nenhuma dessas
coisas foi acertada por descrição em prompt.

**Limite honesto:** é uma re-renderização muito próxima, **não idêntica ao pixel**.
Desvios típicos: ombro esquerdo da crista um pouco mais compacto, menos falha de
tinta no rastro do swash, ® às vezes quase invisível.

### 2 · Composição local do recorte — quando tem que ser exato

Para anúncio pago, e-commerce, rótulo ou qualquer peça onde o logotipo precisa ser
exato ao pixel: gerar a cena **sem** o pacote e compor o recorte real por cima.

Etapas que a experiência mostrou serem obrigatórias:

1. Recorte por croma (limiar medido, não adivinhado — no Suave `S≥75 e V≥120`), com
   **preenchimento de furos** para recuperar a tipografia preta, que cai fora do
   limiar por ser escura.
2. **Medir a direção da luz na cena gerada.** Não se dita luz no prompt — o modelo
   ignora. O especular de um objeto cilíndrico e a direção das sombras dão o azimute.
3. Reiluminar o recorte com gradiente lateral no sentido medido.
4. Sombra projetada no sentido correto **mais** oclusão de contato na base. Sem a
   segunda, o pacote parece colado por cima da foto.
5. **Um passe de câmera sobre a imagem inteira** — ruído, halo de nitidez, JPEG. É
   isso que costura recorte e cena.

Recorte pronto do Suave frontal: `saida-teste/recorte-suave-frontal.png`.

### 3 · Geração pura por texto — só para cena sem produto

Fundo, paisagem, mesa, ambiente. No instante em que a embalagem entra no quadro,
volte para o fluxo 1 ou 2.

---

## O bloco de preservação — verificado

Note o que ele **não** faz: não descreve serra, script, pincel, "Desde 1985" nem
"250g". De propósito.

```text
Keep the coffee package in this image EXACTLY as it is. Same paper, same colour, same
printed artwork, every letter and every line identical, same proportions, same creases
and folds, same crimped top, same vent. Do not redraw it, do not restyle it, do not
relabel it, do not reinterpret or improve the design, do not change a single character
of the lettering. The package must survive this edit pixel-faithful. It is a real
product and its label is legally exact.

Change ONLY what is around it.
```

Negativo que acompanha:

```text
redrawn label, altered logo, changed lettering, restyled packaging, new brand name,
warped text, gibberish text, different typeface, cleaned up design
```

## Coerência de luz — a etapa que quase todo mundo esquece

A foto-fonte tem uma direção de luz própria. No `Suave (5).jpg` a luz vem da
**esquerda** (a sombra cai à direita do saco, na parede).

**O ambiente pedido tem que herdar essa direção.** Se o prompt pedir luz da direita
e o pacote vier iluminado da esquerda, a imagem denuncia mesmo com o logotipo
perfeito. No prompt final: *"The light on the package already comes from the LEFT —
keep it that way, and let the whole scene be lit from the LEFT."*

Escolher a imagem-fonte é, portanto, também escolher a luz da cena.

## Bloco anti-bokeh — obrigatório

Sem ele o modelo entrega anúncio com fundo desfocado. E **desfoque não se desfaz em
pós** — testado: tone mapping, ruído, halo e artefato de JPEG se adicionam depois;
profundidade de campo rasa não se remove. Morre na geração ou não morre.

```text
EVERYTHING IN THE FRAME IS SHARP. This is a phone with a tiny 1/1.7 inch sensor at
f/1.8, which gives an enormous depth of field. The near table edge, the package, the
mug and the coffee bushes twenty metres behind are ALL equally crisp. You can count
the leaves on the distant bushes. There is NO focus falloff, NO background blur, NO
subject separation anywhere. The far hills are hazy from atmosphere only, never from
defocus.
```

Negativo: `blurred background, defocused background, out of focus leaves, bokeh,
bokeh balls, depth of field falloff, subject separation, shallow focus, portrait
mode, lens blur, rim light, golden hour rim lighting, studio lighting, softbox,
product photography, catalogue photography, advertisement, commercial hero shot,
styled set, food styling, glossy perfection, centred symmetrical composition`.

## Formato 4:5

`4:5` **não existe** na API. Proporções aceitas: `1:1`, `3:4`, `4:3`, `9:16`,
`16:9`, `2:3`, `3:2`, `9:19.5`, `19.5:9`, `9:20`, `20:9`, `1:2`, `2:1`, `auto`.

Gerar em `3:4` (0,750), recortar a altura até 4:5 (0,800) tirando ~62% da sobra do
topo, e reduzir para **1080×1350**. Perda de ~6% da altura.

## Modelo

`grok-imagine-image-2.0` com `quality: "medium"` e `resolution: "2k"`. US$ 0,08 por
imagem. É o único que a documentação associa a `/images/edits`, e o único cuja
resolução nativa (1584×1980 após recorte) desce para 1080×1350 sem ampliar.

Correção de uma recomendação anterior: eu havia indicado o `-2.0` por causa da
tipografia. Esse argumento **caiu** — com image guidance a tipografia vem da foto,
não do modelo. O que sustenta a escolha agora é só a resolução e o suporte a edits.

`grok-imagine-image` (US$ 0,02) segue descartado.

---

## Onde o resultado ainda não está perfeito

1. Composição tende ao centro e ao arrumado. Um instantâneo real é mais desleixado.
2. Comida gerada sai lustrosa demais — pão de queijo com brilho de vitrine.
3. A base do pacote não afunda na textura do tecido; falta oclusão de contato, que o
   fluxo 2 resolve e o fluxo 1 não.
4. Kraft sai mais quente/laranja que o real, que é um marrom mais acinzentado. Em
   parte é a luz quente da cena, em parte é deriva.

## O que a base de fotos ainda precisa

Nada disto substitui foto real. `docs/briefing-captura.md` segue valendo: o Bloco A
(produto na mesa mineira, ~55 fotos) e o Bloco B (grão torrado, ~25) continuam sendo
o que desbloqueia o motor de verdade. Image guidance funciona porque existe um
packshot real por trás — e hoje existem apenas 4 ângulos do Suave, 4 do Clássico e
4 do Canela, todos contra parede lisa.
