# Prompt — reformular a home com a gramática da nike.com

> **Como usar:** abra um Claude Code na raiz do repositório
> `Kmzf777/loja-cafecanastra` e cole este arquivo inteiro como primeira mensagem.
> Ele é autossuficiente: não depende de nada desta conversa.
>
> As imagens que ele referencia estão especificadas em
> `BRIEFING-IMAGENS-HOME.md`, que é o documento irmão deste.

---

## 0. A tarefa

Reescrever a homepage de `loja.canastrainteligencia.com` para que ela tenha a
**semântica de navegação e merchandising da homepage da nike.com**, vestida com
a estética que o `estetica.md` deste repositório já define.

Não é copiar o visual da Nike. Preto, swoosh e Futura ficam de fora. O que se
importa é a **gramática**: a sequência de blocos, o trabalho que cada bloco faz,
a hierarquia tipográfica, o vocabulário de CTA e a regra de para onde os links
apontam.

O arquivo a reescrever é **`frontend/app/[locale]/(vitrine)/page.tsx`**.

---

## 1. A gramática da Nike, medida no HTML servido

Isto não é inferência de design. Foi capturado do HTML renderizado de
`nike.com` e do payload `__NEXT_DATA__` embutido (45 cartões, 200 `layoutItems`,
23 posições no desktop). Cada regra abaixo tem contagem por trás.

**R1 — Zero preço na home.** Busca por `currentPrice`, `initialPrice`,
`fullPrice`, `salePrice`, `msrp` no HTML da home: **0 ocorrências**. Busca pelo
caractere `$` no texto visível: **0**. Na grade de destino (`/w/mens-shoes`), no
mesmo dia e mesma sessão: **194 ocorrências de `currentPrice`**, com valores
reais. A supressão não é limitação de CMS — é decisão de camada. A home carrega
desejo; a grade carrega transação.

**R2 — A home nunca linka para uma PDP.** `destinationType` agregado nos 45
cartões: **39 `gridwall`, 6 `page`, 0 `pdp`**. Contando `urlIngredients`: 124
`GRIDWALL`, 7 `PAGE`, 4 `URL`. A home escolhe o **conjunto**; o usuário escolhe
o **item**.

**R3 — Um verbo só.** Inventário completo de `actionButtons[].actionText` nos 45
cartões: **7× `Shop` + 1× `Shop NikeSKIMS`**. Não existe `Explore`, `Buy`,
`Discover` ou `Learn More`. Os títulos de ladrilho começam pelo mesmo verbo:
`Shop Men's`, `Shop Footwear`, `Shop All`.

**R4 — Densidade baixa de CTA.** Em 23 posições no desktop há **8 botões
formais**. No máximo 1 por seção de campanha. Faixas de marca, cartões de texto
e espaçadores têm zero.

**R5 — Uma escala tipográfica só.** O H1 do herói e **todos** os H2 de seção
usam o mesmo token `display2`: 40px até 959px, 76px de 960 a 1919px, 96px acima
de 1920px. Sempre `line-height: 0.9`, `font-weight: 500` (medium, **não** bold),
caixa alta. A hierarquia **não** vem do tamanho da fonte — vem da escala da
imagem e da posição no scroll.

**R6 — O tercet, repetido.** O padrão que governa a página é
`faixa de marca sem CTA → cartão de campanha full-bleed com exatamente 1 CTA →
linha de roteamento (2-up, 3-up ou filmstrip de 3)`. Cartões de **texto puro**
(`containerType='text'`: "Back in Session", "Top of the Class", "TRENDING")
funcionam como cabeçalho de capítulo — sem imagem, sem CTA — e separam os blocos
narrativos.

**R7 — A página fecha com atalhos, não com produtos.** Os últimos blocos são uma
grade de 16 ícones de franquia em PNG recortado com fundo transparente. Sem nome
de SKU, sem preço, sem botão de sacola. Todos apontam para grade filtrada.

**R8 — O que ela recusa.** Sem barra promocional (a flag `showBanner` existe e
está desligada), sem newsletter no corpo, sem selo de frete, sem avaliações, sem
contador de urgência, sem parcelamento. Membership vive só no chrome do header,
em 12px — o menor token do sistema.

**R9 — Não existe gradiente. A sombra está dentro da foto.** Grep nos dois
stylesheets da Nike (bundle de 70 KB + `ncss.en-us.min.css` de 145 KB) e no HTML
inline: **zero scrims**. Nenhuma regra `rgba(0,0,0)` sobre imagem. O único
`linear-gradient` do site inteiro é um hover arco-íris de botão. A zona onde o
texto pousa (40% × 33% inferior-esquerda nos heróis) foi medida em luminância
relativa WCAG e é mais escura que o resto do quadro em **12 de 12 casos**, com
contraste de 12,08:1 a 15,84:1 para texto branco. O perfil linha a linha
confirma a origem: em "Shop Cleats" a luminância cai de 127 no topo para 27 na
base. **O fotógrafo entrega a sombra; o CSS não salva ninguém.**

**R10 — A cor inverte o esperado, e há uma regra de função.** Saturação média
medida (canal S de HSV, 0–255) em 16 imagens: ladrilhos de **produto** 179 e 206;
fotos de **gente e lugar** 40, 42, 75. Cast quente (razão R/B nas altas): 3,04 no
herói de campanha do Acuña, 2,02 e 1,63 nos ladrilhos de produto, contra
1,04–1,10 nas fotos de pessoa e **0,967** — puxando azul — em "Rep Your School".
Não existe um "look Nike" de saturação única: existe **uma cor dominante por
campanha** e uma regra de função — **produto quente e saturado; lugar e gente
lavados e frios.** O fundo nunca é a paleta da marca: é o material real do lugar
(tijolo, azulejo, concreto, madeira).

> Isto converge com o perfil de câmera já medido neste projeto: saturação alvo
> **70** (base lavada) e cast das altas **R/B 0,969** (puxando azul). O registro
> "lugar e gente" da Nike **é** o perfil que a base do Canastra já tem. Não há
> conflito a resolver — há uma coincidência a explorar.

**R11 — Movimento zero.** A home inteira é estática. Nenhum desfoque de
movimento, nenhuma ação congelada. No herói principal a atleta está **sentada**
num banco de vestiário. Não peça movimento nas imagens.

---

## 2. O que NÃO importar

Quatro decisões da Nike que **não** vêm junto, e a razão de cada uma:

| Da Nike | Por que fica de fora |
|---|---|
| Caixa alta em 96px | A Redaction 35 tem degradação de impressão simulada. Em caixa alta a 96px a degradação vira sujeira. Ver §3 abaixo para o que entra no lugar. |
| Barra promocional desligada | O e-commerce brasileiro não perdoa esconder frete e prazo. A `<BarraFreteGratis>` **fica**, reescrita como informação de decisão e não como promoção. |
| Imperativo ("JUST DO IT") | O `estetica.md §11` proíbe. A marca afirma fato, não ordena. |
| Membership escondido no chrome | O Clube é receita recorrente de um consumível. Ele ganha uma banda inteira. |

---

## 3. Tipografia: uma escala só, adaptada

Importe a regra da R5 — **um token para o H1 e para todos os H2** — mas não o
corpo dela.

```css
--t-capitulo: clamp(2.5rem, 5.2vw, 4.5rem);
/* Redaction 35 · line-height 0.95 · tracking -0.02em · peso normal · CAIXA MISTA */
```

Três diferenças deliberadas em relação à Nike, e cada uma tem motivo:

1. **Teto em 4.5rem (72px), não 96px.** Acima disso a degradação da Redaction
   deixa de ser textura e vira ruído.
2. **Caixa mista, não caixa alta.** A caixa alta fica reservada aos *kickers*
   (Archivo Condensed 600, 12px, `tracking 0.18em`) e às tarjas de dado (Martian
   Mono). É a divisão "a mão e a etiqueta" do `estetica.md §3`: o título é mão,
   o kicker é etiqueta.
3. **Peso normal.** A Redaction 35 não tem bold útil; forçar peso quebra a
   degradação.

O que **não** muda da Nike: **o H1 e todos os H2 têm exatamente o mesmo
tamanho.** A hierarquia é carregada pela escala da imagem e pela posição no
scroll. Não crie um `--t-h2` menor.

Corpo continua Archivo 400. Números, preços, altitude, SCA e datas continuam
Martian Mono — regra do `estetica.md §11`, sem exceção.

---

## 4. CTA: um verbo só, e ele é `Comprar`

A R3 diz "um verbo". Em pt-BR esse verbo é **`Comprar`**, não `Ver` e não
`Explorar`. A pobreza de vocabulário só funciona se a palavra escolhida for a
transacional — e há um segundo ganho: o texto-âncora vira palavra-chave.

**Inventário fechado de CTA da home.** Nada fora desta lista:

| Texto | Destino |
|---|---|
| `Comprar café em grãos` | `/cafes?formato=graos` |
| `Comprar café moído` | `/cafes?formato=moido` |
| `Comprar cápsulas de café` | `/cafes?formato=capsula` |
| `Comprar drip coffee` | `/cafes?formato=drip` |
| `Comprar kits de café` | `/cafes?tipo=kit` |
| `Comprar o Clássico` | `/cafes?linha=classico` |
| `Comprar o Suave` | `/cafes?linha=suave` |
| `Comprar o Canela` | `/cafes?linha=canela` |
| `Comprar o microlote` | `/cafes?linha=microlote` |
| `Comprar todos os cafés` | `/cafes` |
| `Assinar o Clube` | `/clube` |

**Antes de escrever qualquer um desses links, valide que a PLP aceita o
parâmetro.** Leia `app/[locale]/(vitrine)/cafes/page.tsx` e
`cafes/conteudo.ts`. Se `?linha=` não existir, ou você o implementa na PLP, ou
troca o destino — **não** escreva um CTA que cai em lista vazia. Registre no
final o que você verificou.

**Uma string por link, em três lugares.** O texto-âncora, o rótulo visível do
ladrilho e o `name` do `BreadcrumbList`/`ItemList` têm de ser **a mesma
palavra**. É onde este tipo de documento costuma se contradizer: a âncora diz
"Comprar cápsulas de café", o ladrilho mostra `CÁPSULAS` e o breadcrumb diz
"Cápsulas" — três strings para o mesmo destino, e o sinal se dilui em três.

A regra: **o rótulo visível é a âncora.** O ladrilho escreve `Cápsulas de café`
no HTML e a caixa alta vem por `text-transform: uppercase` no CSS — nunca
maiúscula digitada, que leitor de tela soletra. O breadcrumb repete a mesma
string.

**Ordem canônica dos cinco ladrilhos, e ela não muda em lugar nenhum:**
`em grãos · moído · cápsulas · drip coffee · kits`. Essa ordem vale para o
layout, para o `ItemList.position` e para o bloco Explore.

**Forma visual do CTA.** A Nike usa botão preenchido no herói e título-que-é-link
nos ladrilhos. Aqui:

- **Herói:** um `<BotaoLink variante="primario">` só. Um. Hoje há dois
  (`Ver os cafés` + `Conhecer a serra`) — o segundo sai.
- **Ladrilho de roteamento:** o título do ladrilho **é** o link. Archivo
  Condensed 600, caixa alta, com sublinhado de 1px que engrossa no hover. Sem
  caixa de botão.
- **Banda de campanha:** um `<BotaoLink>`.
- **Cabeçalho de capítulo:** zero CTA.

---

## 5. A pilha — 10 blocos

Alternância de superfície conforme `estetica.md §7.1`: **nunca duas escuras
seguidas**. A sequência abaixo satisfaz isso —
`fuligem → cal → kraft → kraft → cal → mata → cal → cal → kraft → fuligem`.

### 1. HERÓI — campanha — superfície `fuligem`

Full-bleed, `min-h-screen` (100vh, não os 88vh de hoje). Foto sangra até as
quatro bordas, `object-cover`.

- **A sombra vem da foto, não do CSS** (R9). A foto de herói é brifada para
  entregar a zona inferior-esquerda já escura. O gradiente `fuligem` que existe
  hoje **fica, mas encolhe**: passa a ser rede de segurança, não a fonte do
  contraste.

  **Como verificar:** meça a luminância relativa WCAG na zona onde o texto pousa
  (40% × 33% inferior-esquerda). Se a foto sozinha entregar ≥ 7:1 para texto em
  `cal`, reduza o gradiente ao mínimo que ainda cobre o pior caso de recorte
  responsivo. Se ela entregar menos que isso, **a foto está errada** — peça
  outra em vez de compensar com CSS mais escuro. Anote o número medido em
  comentário no código.

- `<Serra>` no rodapé do quadro, como já existe hoje. **Mantenha.** É a "mão"
  do `estetica.md §3` aparecendo uma vez na página, e é o equivalente estrutural
  da faixa de marca da R6.
- Empilhamento, nesta ordem, alinhado ao canto **inferior esquerdo**:
  1. kicker — Archivo Condensed 600, 12px, caixa alta, `tracking 0.18em`, cor `juta`
  2. `<h1>` — `--t-capitulo`, cor `cal`, máximo 2 linhas
  3. uma linha de corpo — 18px, `max-w-[52ch]`, `cal/80`
  4. **uma** tarja de dado em Martian Mono 12px — é aqui que a antiga faixa de
     prova é reabsorvida (ver §7 abaixo)
  5. **um** `<BotaoLink>`

Imagem: `HERO-01` do briefing. **Esta é a LCP da página** — ver §9.

### 2. COMPRE POR FORMATO — roteamento — superfície `cal`

Cinco ladrilhos, grade `2 col mobile / 5 col desktop`. É o equivalente do
filmstrip de roteamento que a Nike põe imediatamente abaixo do herói (R6), e
está aqui em cima de propósito: **o primeiro caminho até uma superfície de
compra precisa estar visível em no máximo 1,5 tela de scroll no mobile.**

Cada ladrilho: foto 4:5 + título-que-é-link. Sem preço, sem descrição, sem botão.

| Ladrilho | Título/CTA | Destino | Imagem |
|---|---|---|---|
| Cápsulas | `Comprar cápsulas de café` | `/cafes?formato=capsula` | `FMT-01` |
| Drip Coffee | `Comprar drip coffee` | `/cafes?formato=drip` | `FMT-02` |
| Em grãos | `Comprar café em grãos` | `/cafes?formato=graos` | `FMT-03` |
| Moído | `Comprar café moído` | `/cafes?formato=moido` | `FMT-04` |
| Kits | `Comprar kits de café` | `/cafes?tipo=kit` | `FMT-05` |

Isto **substitui** o `<TrilhaDeCategorias>` atual, que é uma fila de palavras.
Mantenha o componente no repositório — ele é usado noutras rotas —, mas a home
deixa de o chamar.

### 3. AS LINHAS — cabeçalho de capítulo — superfície `juta-claro`

Cartão de **texto puro**. Sem imagem, sem CTA. É o `containerType='text'` da R6.

Só um `<h2>` em `--t-capitulo` e, abaixo, uma linha de corpo de no máximo 20
palavras. Respiro vertical generoso (`py-20 md:py-28`). O trabalho dele é
separar capítulos e dar ao olho um lugar para descansar entre duas superfícies
de imagem.

### 4. GRADE DAS LINHAS — roteamento — superfície `juta-claro`

Três ladrilhos: Clássico, Suave, Canela. Grade `1 col mobile / 3 col desktop`.

Cada um: foto 4:5 + kicker com as notas + título-que-é-link. **Sem preço.**

| Linha | Kicker | Título/CTA | Destino | Imagem |
|---|---|---|---|---|
| Clássico | `CARAMELO · CHOCOLATE` | `Comprar o Clássico` | `/cafes?linha=classico` | `/pacote-classico.jpg` ✅ existe |
| Suave | `CHOCOLATE · CÍTRICO` | `Comprar o Suave` | `/cafes?linha=suave` | `/pacote-suave.jpg` ✅ existe |
| Canela | `CARAMELO · CANELA` | `Comprar o Canela` | `/cafes?linha=canela` | `/pacote-canela.jpg` ✅ existe |

As notas saem de `data/catalogo-canastra.json → linhas[].notas`. Não escreva à
mão.

### 5. MICROLOTE — campanha — superfície `cal`

Banda full-bleed. Foto sangra na largura toda, altura `~60vh`; texto **abaixo**
da foto, centrado. É a forma de cartão de campanha da R6.

kicker + `<h2>` em `--t-capitulo` + uma linha + **um** `<BotaoLink>`
(`Comprar o microlote` → `/cafes?linha=microlote`).

O Microlote é o único SKU com nota SCA publicada acima do piso (**86**,
`scaExata: true`). Esse número é a única coisa que a marca pode afirmar sem
ressalva, e ele vai na tarja de dado desta seção, em Martian Mono.

> **Atenção factual:** `SCA 80+` é o **piso da coleção**, não a nota de nenhum
> café, e é **falso para o Néctar de Minas**, que tem 75 e não é café especial.
> Ver `catalogo-canastra.json → marca.sca_observacao`. Nenhum texto desta home
> pode afirmar SCA 80+ sobre a coleção inteira.

Imagem: `CAMP-01`.

### 6. CLUBE DA CANASTRA — banda de membro — superfície `mata`

O equivalente do bloco de membership. Foto à esquerda (ou fundo, no mobile),
texto à direita.

kicker `ASSINATURA` + `<h2>` + a linha que já existe hoje + **um** botão
`Assinar o Clube` → `/clube`.

> **Contraste:** `estetica.md §4.1` — vermelho sobre mata é 2,0:1, **proibido**.
> O CTA aqui é `variante="primarioEscuro"`, em `cal`. Não troque.

Imagem: `CLUBE-01`.

### 7. DO PÉ À XÍCARA — capítulo + sequência — superfície `cal`

Mantenha as cinco etapas e a numeração calculada que já existem hoje
(`numeroDaEtapa`). O que muda é a forma: banda de foto full-bleed no topo
(altura `~40vh`), e as cinco etapas em `<ol>` abaixo dela.

A numeração é justificada porque é sequência real e irreversível
(`estetica.md §7.1`). Não é enfeite.

Imagem: `SEQ-01`.

### 8. EM ALTA — atalhos — superfície `cal`

O equivalente exato da grade de 16 ícones de franquia da R7: recortes com fundo
liso, sem nome de SKU, sem preço, sem botão de sacola, todos apontando para
grade filtrada.

Grade de `3 col mobile / 6 col desktop`. Cada célula: recorte + uma palavra.

Use os recortes que já existem em `saida-teste/site-fundo-branco/`:
`FINAL-classico-250g-branco.jpg` e `FINAL-suave-250g-branco.jpg` estão
**limpos** e podem ir direto. `FINAL-canela-250g-branco.jpg` tem um bloco de
micro-texto corrompido no canto superior direito (saiu `AD BNPELEARI`) — **corte
os 12% do topo antes de usar**, ou peça a regeração. Detalhe em
`BRIEFING-IMAGENS-HOME.md`.

### 9. EXPLORE — links densos — superfície `juta-claro`

Grade densa de links de texto, sem foto, antes do rodapé. Archivo Condensed 600,
caixa alta, 13px.

É o bloco que devolve à home a autoridade de SEO que ela perde ao tirar os
produtos: são links internos com texto-âncora rico apontando para as folhas que
precisam ranquear. Quatro colunas no desktop, duas no mobile.

Colunas: **Por formato** · **Por linha** · **A Canastra** · **Ajuda**. Os
destinos saem da tabela de CTA da §4 mais as rotas institucionais que já
existem (`/a-serra`, `/historia`, `/rastreabilidade`, `/clube`, `/bio`).

### 10. RODAPÉ

Já existe (`<Rodape>`). Não toque.

---

## 6. O que sai da home, e por quê

| Sai | Motivo |
|---|---|
| Os três `<SecaoDeProdutos>` com preço e botão de sacola | R1. É o núcleo da mudança. |
| A chamada a `produtosDaHome()` | Sem preço e sem `produtoId`, a leitura ao vivo não serve para nada. **Consequência boa: a home deixa de fazer `fetch` e vira 100% estática.** |
| `<TrilhaDeCategorias>` na home | Substituída pelos ladrilhos com foto do bloco 2. O componente continua no repositório. |
| A faixa de prova como faixa de 4 colunas | R8. Reabsorvida como tarja de dado dentro do herói. |
| `<SecaoDoBlog>` | Hoje é casca marcada "Em breve". A Nike não publica seção vazia. Volta quando houver post. |
| O segundo botão do herói (`Conhecer a serra`) | R4. Um CTA por seção. O destino continua no menu e no rodapé. |

**Não remova** `<BarraFreteGratis>` nem `<BotaoWhatsApp>`. A R8 diz que a Nike
não os tem; o mercado brasileiro diz que a ausência custa venda. Esta é uma
divergência deliberada da gramática — registre-a em comentário no código para
que a próxima sessão não a "corrija".

---

## 7. Os fatos que a home pode afirmar

Nenhum texto novo pode inventar. Estes são os fatos verificáveis, com a fonte:

| Fato | Fonte |
|---|---|
| Família planta café **desde 1985** | `a-serra/conteudo.ts` |
| Na **Serra da Canastra desde 2008** | idem |
| Torrefação própria **desde 2016** — *não* desde 1985 | idem |
| Fazenda Divinéia, Medeiros/MG, **1.250 m** | EXIF das fotos base: altitude gravada 1.235–1.272 m |
| Microtorrefação em **Uberlândia** | `catalogo-canastra.json` |
| Variedades **Arara, Caturra 2SL, Paraíso** | `marca.variedades` — confirmadas pela marca |
| **Origem única** da Serra da Canastra | `marca.atributos` |
| **Torra sob demanda**, em lotes pequenos | atributo declarado |
| Microlote **SCA 86**; Néctar de Minas **SCA 75** | `linhas[].scaExata: true` |

**Não afirme:** "lote rastreado" (a `/rastreabilidade` diz na cara que não há
código por embalagem), "SCA 80+" sobre a coleção inteira (falso para o Néctar),
nem "torrado desde 1985".

**Carbono zero** e **100% fotovoltaica** existem em `marca.atributos`, mas só
entram como tarja de display se houver página de prova. Sem certificado de
terceiro, ficam na ficha técnica da PDP, não no display da home.

### Vocabulário proibido no copy

Nenhuma variação de posicionamento de massa: **popular, acessível, barato,
econômico, para todos, democrático, custo-benefício, preço justo**. O site fala
como café especial. A amplitude aparece na variedade de formato e no elenco das
fotos — nunca no texto.

Também proibido pelo `estetica.md §11`: caricatura mineira (*uai*, *trem bão*,
*sô*), exclamação em CTA, emoji em estado vazio, e frase acima de 20 palavras.

---

## 8. SEO

Os termos abaixo foram levantados no autocomplete do Google BR
(`suggestqueries.google.com`, `hl=pt-BR&gl=br`), coletado em 25/08/2026. O
autocomplete é ordenado por popularidade real: **10 sugestões = demanda alta;
1–3 = demanda residual.** É proxy, não volume absoluto — mas é verificável, e
qualquer um pode repetir a coleta.

### O achado que muda tudo: o título de hoje mira um termo sem demanda

O `<title>` atual é `Café Canastra — Café de origem única da Serra da Canastra`.
O seed `cafe de origem unica` devolve **uma** sugestão no autocomplete BR: ele
mesmo.

**Em português, "origem única" é vocabulário de marca, não de busca.** O mesmo
erro está no `/es` (`origen único`; o termo real é `café de especialidad`). Só o
`/en` acerta — `single origin coffee` tem autocomplete cheio.

A expressão continua verdadeira e continua valendo como *posicionamento*. Ela só
não pode ser o que carrega o título.

### Title e description — escreva exatamente isto

| Locale | `<title>` | car. |
|---|---|---:|
| `pt` | `Café Canastra \| Café Especial da Serra da Canastra` | 49 |
| `en` | `Café Canastra \| Brazilian Specialty Coffee, Single Origin` | 57 |
| `es` | `Café Canastra \| Café de Especialidad Brasileño` | 46 |

> **Por que o título em `pt` não leva "em Grãos".** Porque a home venceria a
> `/cafes` no duelo interno pela mesma consulta, e a home **sempre** vence — ela
> tem mais autoridade. O modificador transacional pertence ao title da listagem,
> não ao da porta de entrada. A description já enumera os formatos, que é onde
> eles trabalham sem canibalizar. Mesma razão para tirar "en Grano" do `es`.

| Locale | `<meta description>` | car. |
|---|---|---:|
| `pt` | `Da Serra da Canastra para a sua xícara: café especial 100% arábica, torrado sob demanda em lotes pequenos. Grãos, moído, drip coffee, cápsulas e kits.` | 150 |
| `en` | `Single origin specialty coffee from the Serra da Canastra, Minas Gerais, at 1,250 m. Whole bean, ground, drip bags and capsules, roasted to order.` | ~147 |
| `es` | `Café de especialidad brasileño de la Serra da Canastra, a 1.250 m. En grano, molido, drip coffee y cápsulas, tostado bajo pedido en lotes pequeños.` | ~148 |

A description em `pt` enumera os quatro formatos de propósito: **é assim que o
posicionamento expressa amplitude sem usar nenhuma palavra da lista proibida da
§7.**

> **Não escreva "SCA 80+" em nenhuma das três descrições.** A pesquisa mostra
> que `cafe sca 80` devolve 1 sugestão — não é vocabulário de busca do
> consumidor brasileiro. E, mais importante, 80+ é o **piso da coleção** e é
> **falso para o Néctar de Minas** (75). Afirmação de coleção na meta description
> é afirmação sobre tudo. SCA é prova dentro da página, nunca alvo de
> ranqueamento.
>
> Conte os caracteres você mesmo antes de commitar. As contagens de `en` e `es`
> estão marcadas com `~` porque foram estimadas, não medidas.

### H1

O `<h1>` é um só, está no herói, e precisa carregar a palavra-chave. A tensão é
real: `Café que vem de cima` tem zero termo de busca.

**Resolução — inverta os dois slots:**

```
kicker  →  CAFÉ QUE VEM DE CIMA · SERRA DA CANASTRA     (Archivo Cond 600, caps)
  h1    →  Café especial da Serra da Canastra.           (Redaction, --t-capitulo)
```

A frase da marca vira o rótulo em caixa alta — que é exatamente o registro
"etiqueta" do `estetica.md §3` — e o `<h1>` carrega o termo. Nada é escondido:
o que o buscador lê é o que a pessoa vê, no tamanho em que vê.

### Os H2, com termo e sem empilhamento

| Bloco | `<h2>` |
|---|---|
| 2 · formato | `Como você prepara` |
| 3 · capítulo | `As linhas do Canastra` |
| 5 · microlote | `Microlote: 86 pontos` |
| 6 · clube | `Clube da Canastra: assinatura de café especial` |
| 7 · sequência | `Do pé à xícara` |
| 8 · em alta | `Em alta` |
| 9 · explore | `Explore` |

O termo de busca vive no texto-âncora dos 11 CTAs (§4), que é onde ele trabalha
melhor. Não force keyword em todo H2 — dois ou três bastam, e a página lê como
página em vez de ler como planilha.

### Três problemas que esta tarefa NÃO resolve, e que precisam de decisão

Encontrados na pesquisa. Registre-os no relatório final e siga; nenhum deles
bloqueia a home.

1. **Três domínios disputando "café canastra".** `cafecanastra.com` (o mais bem
   otimizado, com blog e canonical próprio), `loja.cafecanastra.com` (loja Tray
   — **sem nenhuma tag `<title>` na home**, `description` e `keywords` são
   literalmente `-`) e `loja.canastrainteligencia.com` (este). Nenhum aponta
   canonical ou 301 para outro. `café canastra` tem 10 sugestões de autocomplete
   — há demanda de marca real sendo dividida em três. **Eleger um domínio
   canônico é decisão do dono, e vale mais que qualquer coisa neste documento.**

2. **Título duplicado em três rotas.** `/cafes`, `/historia` e as PDPs saem como
   `Cafés — Café Canastra — Café Canastra`. Causa provável: a página passa um
   título que já inclui o sufixo e o `title.template` do `app/layout.tsx` aplica
   `%s — Café Canastra` por cima. Em `/cafes` sobram 22 caracteres úteis. **A
   home já usa `title: { absolute }` e por isso escapa** — mas confira que a sua
   reescrita mantém o `absolute`.

3. **Nenhuma URL filtrada está no sitemap.** O `app/sitemap.ts` emite `/cafes` e
   `/cafes/[slug]`, nada mais. Os 11 CTAs da §4 apontam para *query params*
   (`?formato=graos`), que roteiam o usuário perfeitamente mas **não são alvos
   indexáveis**. O ganho de SEO que a §5.9 promete só se realiza se essas
   páginas puderem ranquear. Duas saídas, em ordem de preferência: rotas reais
   (`/cafes/em-graos`) com canonical próprio, ou — mais barato — acrescentar as
   URLs filtradas ao `sitemap.ts` com canonical para si mesmas. **Isto é tarefa
   à parte. Não a faça agora; registre-a.**

### Regras invioláveis

- `<title>` ≤ 60 caracteres; `<meta description>` entre 150 e 158. Nos três
  idiomas, com termo próprio de cada mercado — não traduza a keyword
  literalmente.
- Um `<h1>` por página. Todo `<h2>` de seção carrega termo, sem empilhar
  keyword.
- `alt` descreve a foto com honestidade. Um `alt` que promete o que a imagem não
  mostra é pior que um `alt` genérico.
- Nome de arquivo de imagem em kebab-case com termo:
  `cafe-especial-serra-da-canastra-heroi.jpg`, não `hero-01.jpg`.
- `alternates` / `hreflang` já funcionam via `alternativasDeIdioma()`. **Não
  reescreva.** Confirme que `x-default` está presente.
- JSON-LD: `Organization` e `WebSite` na home; `BreadcrumbList` e `ItemList`
  para os ladrilhos de roteamento. **Não** emita `Product`/`Offer` na home — não
  há mais produto nela, e schema que descreve o que a página não mostra é
  penalizável.

### O que se perde, e a compensação

Tirar produto e preço da home remove os termos de SKU do texto e o schema de
`Product`. A compensação é o bloco **EXPLORE** (§5.9) e o texto-âncora rico da
tabela de CTA (§4): 11 links internos com termo de busca, todos apontando para
folhas que precisam ranquear. É mais link equity concentrado, não menos — só
distribuído para a PLP em vez de ficar preso na home.

**Consequência a aceitar:** a `/cafes` passa a ser a superfície transacional do
site. Se ela estiver fraca, a home nova piora o resultado. Verifique a PLP antes
de dar isto por pronto.

---

## 9. Performance

O herói é o LCP e é uma foto full-bleed de 100vh. É o maior risco técnico desta
mudança.

- `next/image` com `fill`, `priority`, `fetchPriority="high"`, `sizes="100vw"`.
- AVIF com fallback WebP. `srcset` em 640 / 1080 / 1600 / 2048 / 2560.
- **Teto de peso do herói servido: 250 KB no breakpoint de desktop.** Se a foto
  não couber, corte resolução antes de cortar qualidade.
- Nenhuma outra imagem da página leva `priority`. Todas com `loading="lazy"`.
- Reserve proporção em toda imagem (`aspect-ratio` ou `width`/`height`) para
  CLS não subir.
- A home volta a ser **estática**: mantenha `generateStaticParams()` e
  `revalidate`. Sem a chamada a `produtosDaHome()`, não há mais `fetch` de
  servidor por visita.

Meça antes e depois. Anote LCP, INP e CLS em mobile no relatório final.

---

## 10. i18n

A home serve `pt`, `en` e `es`, e a tabela de textos vive **dentro** do
`page.tsx` (`const pt`, `const en: TextosDaHome`, `const es: TextosDaHome`).

- `pt` é a fonte do tipo. `en` e `es` são **declarados** como `TextosDaHome`, e
  chave faltante quebra o build. Preserve esse mecanismo.
- Rótulo reutilizado (botão, contagem) continua vindo de `lib/i18n/dicionario.ts`.
  Texto corrido de página mora com a página.
- **Os CTAs da §4 precisam de tradução própria por mercado.** `Comprar café em
  grãos` → `Shop whole bean coffee` → `Comprar café en grano`. Traduza a
  intenção de busca, não a string.
- `META` (title/description) já existe por locale. Reescreva os seis valores.

---

## 11. Acessibilidade

- Todo ladrilho de roteamento é **um** link, não uma div clicável com um link
  dentro. Alvo de toque mínimo 44×44.
- Sequência de heading sem buraco: um `<h1>`, depois `<h2>` por seção.
- Contraste: as duas proibições de `estetica.md §4.1` já estão codificadas em
  `lib/cor.test.ts`. Se você escrever uma combinação nova à mão, o teste **não**
  a pega — confira você.
- `prefers-reduced-motion`: o `estetica.md §12` registra que **nada no código
  consulta essa media query hoje**. Se você adicionar qualquer animação de
  entrada, adicione o bloco junto.
- Kicker em caixa alta com `tracking` largo: use `letter-spacing` no CSS, não
  texto escrito em maiúsculas no conteúdo — leitor de tela soletra.

---

## 12. Critérios de aceite

Rode e cole a saída. Não declare pronto sem isto.

```bash
cd frontend
npm run lint
npx tsc --noEmit
npm test
npm run build
```

Depois confirme, item por item:

- [ ] `grep -riE 'R\$|precoCentavos|preco' app/\[locale\]/\(vitrine\)/page.tsx`
      não retorna nada
- [ ] Nenhum link da home aponta para `/cafes/[slug]` (regra R2)
- [ ] Todo CTA visível começa com `Comprar` ou é `Assinar o Clube` (regra R3)
- [ ] Contagem de botões formais no corpo da home ≤ 8 (regra R4)
- [ ] `<h1>` e todos os `<h2>` usam o mesmo token de tamanho (regra R5)
- [ ] Nenhuma superfície escura encosta noutra escura
- [ ] Cada `?formato=` e `?linha=` da §4 foi aberto no navegador e devolve
      resultado — liste o que você testou
- [ ] As três home (`/`, `/en`, `/es`) saem do build como HTML estático —
      confira `.next/prerender-manifest.json`
- [ ] Nenhuma palavra da lista proibida da §7 aparece no arquivo
- [ ] LCP, INP e CLS medidos em mobile, antes e depois

**Se algum item falhar, diga qual e por quê. Não ajuste o critério para ele
passar.**

---

## 13. Uma nota sobre risco

Esta mudança tira o preço e o botão de sacola da porta de entrada de uma loja de
consumível de recompra. A Nike compra esse direito com tráfego de marca que uma
torrefação familiar não tem.

A decisão foi tomada com o trade-off explícito na mesa. As mitigações que não
custam nada da escolha estão embutidas: a sacola continua no header, o
roteamento por formato está no bloco 2 (não no fim da página), a barra de frete
fica, e todos os 11 CTAs vão para superfície de compra e não para página
institucional sem saída.

**O que fica por fazer, e é do dono do projeto, não desta tarefa:** instrumentar
a home antes e depois para saber o efeito. Sem baseline, ninguém vai conseguir
dizer se funcionou.
