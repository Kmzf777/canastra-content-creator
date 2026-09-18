# Café Canastra — plano do site e prompt de execução

> Escrito em 25/08/2026. Auditado no ar, medido no arquivo e no HTML servido.
> Documentos irmãos: `docs/PROMPT-HOME-NIKE.md` (a gramática, em detalhe),
> `docs/BRIEFING-IMAGENS-HOME.md` (a direção de imagem), `entrega-site/` (as
> imagens prontas).

---

## 0. Antes de qualquer pixel: **a loja não vende hoje**

Isto não é opinião de design. É medição, e reordena o resto do documento.

```
GET https://loja.canastrainteligencia.com/api/health     → 404  text/html
GET https://loja.canastrainteligencia.com/api/config     → 404  text/html
GET https://loja.canastrainteligencia.com/api/dashboard  → 404  text/html

grep -o "produtoId" no HTML da home  →  0 ocorrências
grep -o "skuLoja"   no HTML da home  →  37 ocorrências
```

Os 404 vêm com `content-type: text/html` e `<title>Café Canastra</title>` — ou
seja, **é o próprio Next respondendo**. O nginx não faz proxy de `/api`, então a
API Express nunca é alcançada.

**A consequência é total.** `produtoId` só nasce do casamento por SKU com o banco
(`repositorio.ts` → `buscarDadosAoVivo()` → `fetch(API_BASE + "/dashboard")`).
Sem ele, `usar-adicionar.ts` devolve a ação `"sem-loja"` e **todo** clique em
"Adicionar à sacola" — home, PLP e PDP — responde:

> *"Não conseguimos falar com a loja agora. Tente de novo em instantes."*

Agravante estrutural: `API_BASE` está compilado no bundle como a **string
relativa `"/api"`**, e `fetch` relativo não resolve no Node do servidor. **Mesmo
que o Express suba, essa leitura continua falhando** até virar URL absoluta ou
até o Next ganhar uma rota interna.

E há um segundo efeito silencioso: como `buscarDadosAoVivo()` devolve mapa vazio,
**a vitrine anuncia preço e estoque do JSON versionado**, não do banco. Os
valores de estoque no HTML são literalmente 20, 10, 12, 8, 6 e 0 — os mesmos de
`data/catalogo-canastra.json`. Mudar preço no painel não chega à loja.

> **Nenhuma home nova conserta isso.** Uma vitrine com estética de marca grande
> em cima de uma loja que não põe no carrinho é decoração. Esta é a tarefa P0, e
> ela vem antes de qualquer coisa neste documento.

### O banco também está atrasado

O Supabase responde `PGRST205` para `avaliacoes`, `cupons`, `newsletter` e
`assinaturas`: **as migrações 0009 a 0016 não foram aplicadas.** E a linha
pública de `config_loja` não tem a coluna `frete_gratis_minimo_centavos`.

Daí saem três coisas visíveis: o "Frete grátis acima de R$ 149" no topo de toda
página é **fallback chumbado no código**, o bloco de avaliações da PDP existe mas
nunca renderiza, e o formulário de newsletter do rodapé **posta numa rota 404**.

---

## 1. O que mais está quebrado, com a URL

Encontrado na auditoria e conferido no HTML servido.

| # | Defeito | Onde |
|---|---|---|
| 1 | **`R$ 0,00` exibido duas vezes** e a PDP perde o JSON-LD de `Product` inteiro | `/cafes/canela` |
| 2 | **Card de caixa mostra o peso de UM pacote com o preço da CAIXA**: "Em grãos · 500 g / R$ 236,70" para uma caixa de 4×500 g — na mesma página em que o pacote de 500 g avulso custa R$ 65,70 | home, seção "Nossos kits" |
| 3 | **Néctar de Minas usa a foto do Clássico**, inclusive no `image` do JSON-LD | `/cafes/nectar-de-minas` |
| 4 | O bloco "Kits e caixas" da PLP **ignora todo filtro** e devolve sempre os mesmos 3 kits, 2 esgotados — e não bate com a seção "Nossos kits" da home, para onde o "Ver mais" aponta | `/cafes` |
| 5 | **Cápsulas e Drip Coffee estão 100% esgotados** — e são as duas primeiras categorias da trilha | home |
| 6 | Newsletter posta em rota 404 | rodapé, todas as páginas |
| 7 | **O domínio de teste está totalmente indexável**, com sitemap de 42 URLs e canonicals próprios — conteúdo duplicado esperando os domínios definitivos | site inteiro |

O defeito 2 é o mais caro dos sete. Não é um bug de layout: é a página dizendo
ao cliente que 500 g custam R$ 236,70 logo abaixo de 500 g por R$ 65,70. Quem lê
não conclui "há um erro"; conclui "essa loja é cara".

**Números reais do catálogo:** 29 SKUs cadastrados, **16 vendem**, faixa de
R$ 39,70 a R$ 236,70.

### O que já está bom e não se toca

i18n completa em pt/en/es com `hreflang` e canonical corretos, e um aviso honesto
de que o checkout só existe em português · 37 links internos testados, nenhum
morto · busca funcionando · conteúdo editorial de `/historia` e `/a-serra` pronto
nos três idiomas · PDP densa, com receita de preparo parametrizada · CSP
restritiva, HSTS preload · HTML pré-renderizado de 20 KB.

Isso é uma base boa. O problema não é o site — é que **ele está desligado da
loja**.

---

## 2. A decisão: estética de marca grande, loja de verdade

A versão anterior deste plano era **Nike pura** — zero preço na home, zero botão
de sacola. Você mudou isso, e a mudança está certa: a Nike compra o direito de
não mostrar preço com bilhões em tráfego de marca. Uma torrefação familiar paga
o preço e não recebe a contrapartida.

**O que se importa da Nike, e é medido no HTML servido deles:**

| | Medido |
|---|---|
| Um verbo de CTA | `Shop` 7×. Não existe `Explore`, `Buy`, `Discover` |
| Uma escala tipográfica | H1 do herói e **todo** H2 no mesmo token: 40px mobile / 76px desktop |
| Densidade de CTA | 8 botões formais em 23 posições |
| O tercet | faixa de marca sem CTA → campanha full-bleed com **1** CTA → linha de roteamento |
| Sem gradiente | **zero scrims** no CSS. A sombra sob o texto está **dentro da foto**, mais escura em 12 de 12 casos, 12:1 a 15,8:1 |
| Cor por função | produto quente e saturado (S 179–206); **gente e lugar lavados e frios** (S 40–75, R/B 0,967) |
| Movimento | zero. A home inteira é estática |

**O que NÃO se importa, e a razão de cada um:**

- **Zero preço na home.** Aqui o preço fica. É consumível de recompra.
- **Caixa alta em 96px.** A Redaction 35 tem degradação de impressão simulada;
  em caixa alta a 96px a degradação vira sujeira. Teto em 4,5rem, caixa mista.
- **Barra promocional desligada.** No Brasil, esconder frete e prazo custa venda.
- **Membership escondido no chrome.** O Clube é receita recorrente. Ganha banda.

### A regra que resolve a tensão

**A gramática da Nike não é "não vender" — é *uma superfície, um trabalho*.**

A Nike tira preço da home porque ninguém precisa de âncora de preço para tênis, e
porque a grade um clique abaixo já tem 194 preços. Café é outro produto: é
consumo recorrente, a decisão de **formato** vem antes da decisão de café, e
frete é a objeção nº 1.

Então importamos a **forma** inteira — uma escala tipográfica só, um verbo
dominante, campanha full-bleed, alternância de superfície, movimento zero, cor
por função — e trocamos **só a regra de preço**.

**O mecanismo é tipográfico, não de layout.** Todo preço é **Martian Mono**, a
fonte de número do sistema, exibido no mesmo registro que SCA, gramatura,
altitude e estoque. `R$ 39,70` tem exatamente o mesmo peso visual que `SCA 86` e
que `1.250 M`.

> **Preço lido como ficha técnica é o lado "etiqueta" dos 80% de rigor do
> `estetica.md §3`. Ele não briga com a estética — ele *é* a estética.**

Consequências duras, e nenhuma é negociável:

- **Vermelho `#C4231E` nunca marca preço.** O vermelho é acento de marca, não de
  oferta.
- Não existe preço riscado, "de/por", selo de `% OFF`, badge de promoção nem
  contador regressivo.
- Desconto aparece **só** como o segundo preço da assinatura, também em Martian
  Mono.

### Duas superfícies de venda, declaradas

A venda mora em **dois blocos**: a **Prateleira** e o **Clube**. São os únicos
com preço de produto e ação de compra. Todo o resto roteia.

| | superfícies com comércio |
|---|---|
| Coffee Mais | **11 de 15** — e paga o preço: `system-ui` em heading, banner de encarte, zero fotografia editorial. Marca nenhuma. |
| Nike | **0** |
| **Canastra** | **2** — o mínimo que uma loja de café precisa e o máximo que a forma aguenta |

---

## 3. A home nova, bloco a bloco

Alternância de superfície do `estetica.md §7.1`: **nunca duas escuras seguidas**.
A sequência abaixo confere.

| # | Bloco | Superfície | Roteia | Vende | Preço | Imagem |
|---|---|---|:---:|:---:|:---:|---|
| 0 | Barra de condição + cabeçalho | fuligem | — | — | frete | — |
| 1 | **Herói** 100vh | fuligem | sim | não | não | `cafe-especial-serra-da-canastra-heroi.jpg` |
| 2 | **Compre por formato** — 5 ladrilhos | cal | sim | não | não | `comprar-*.jpg` (4 de 5) |
| 3 | **A prateleira** — trilho de SKU | juta-claro | — | **SIM** | **SIM** | packshots |
| 4 | **Faixa de condições** | cal | — | não | frete, parcelas | — |
| 5 | **Clube da Canastra** | mata | — | **SIM** | **SIM** | `clube-assinatura-de-cafe-especial.jpg` |
| 6 | **As linhas** — 3 ladrilhos | cal | sim | não | não | `pacote-*.jpg` |
| 7 | **A serra** — banda de campanha | fuligem | sim | não | não | `serra-da-canastra-chapadao-21x9.jpg` ✅ **foto real** |
| 8 | **Do pé à xícara** | cal | — | não | não | `cafezal-serra-da-canastra-21x9.jpg` ✅ **foto real** |
| 9 | **Explore** — links densos | juta-claro | sim | não | não | — |
| 10 | Rodapé | fuligem | — | — | — | — |

Alternância:
`fuligem → cal → kraft → cal → mata → cal → fuligem → cal → kraft → fuligem`.
Nenhuma escura encosta noutra. Confira antes de mexer na ordem.

**O caminho até a compra, contado em telas de mobile:**

| | onde |
|---|---|
| Ícone de sacola e busca | **tela 0** — no cabeçalho |
| CTA do herói `Comprar todos os cafés` → `/cafes` | **tela 0** |
| Trilha de formato | **~0,9 tela** |
| **Primeiro preço** (a Prateleira) | **~1,6 tela** |

O herói é 100vh de propósito, e o preço vem logo depois. Se na implementação
passar de 2 telas até o primeiro preço, **encurte o herói para 85vh** antes de
mexer em qualquer outra coisa.

### 3.1 Herói — bloco 1

Full-bleed, `min-h-screen`. Foto sangra até as quatro bordas.

- **O gradiente `fuligem` FICA, e isto é uma divergência deliberada da Nike.**

  A Nike não tem um único scrim: a sombra sob o texto está dentro da foto, e a
  zona de texto é mais escura que o resto do quadro em 12 de 12 casos, com 12:1
  a 15,8:1. Eu tentei importar essa regra e **medi que ela não se aplica aqui**.

  Medição do quarto inferior esquerdo contra `cal` #F1F0EA, percentil 95 da
  luminância — é o pixel claro que quebra a legibilidade, não o típico:

  | | contraste p95 |
  |---|---:|
  | as 6 variantes do herói | **1,7:1 a 2,4:1** |
  | a foto real do cafezal | 2,1:1 |
  | a foto real do chapadão | 2,3:1 |

  **Ao meio-dia, num cafezal aberto, não existe um quarto escuro.** A regra da
  Nike funciona porque as fotos deles são urbanas e low-key — vestiário, canyon
  de rua, interior. A luz da Canastra é sol a pino em campo aberto, e é ela que
  o perfil de câmera do projeto foi calibrado para reproduzir.

  Então o gradiente é a fonte do contraste, não a rede de segurança. Mantenha o
  que já existe (`fuligem` 0 → 60%, de baixo para cima) e **meça**: o texto em
  `cal` precisa de ≥ 4,5:1 sobre a composição final. Anote o número medido em
  comentário no código.
- `<Serra>` no rodapé do quadro — **mantenha**. É a "mão" do `estetica.md §3`
  aparecendo uma vez, e é o equivalente da faixa de marca da Nike.
- Empilhamento, alinhado ao canto inferior esquerdo:
  1. kicker — Archivo Cond 600, 12px, caixa alta, `tracking .18em`, cor `juta`
  2. `<h1>` — `--t-capitulo`, cor `cal`, máximo 2 linhas
  3. uma linha de corpo — 18px, `max-w-[52ch]`, `cal/80`
  4. **uma** tarja de dado em Martian Mono 12px
  5. **um** `<BotaoLink>`

**Texto:**

```
kicker  CAFÉ QUE VEM DE CIMA · SERRA DA CANASTRA
h1      Café especial da Serra da Canastra.
corpo   Torrado sob demanda, em lotes pequenos. Café da família desde 1985.
tarja   SCA 75–86 · 1.250 M · MEDEIROS, MINAS GERAIS
cta     Comprar os cafés  →  /cafes
```

> **O H1 mudou de propósito.** `Café que vem de cima` é bonito e tem **demanda
> zero** de busca — o autocomplete do Google BR devolve uma única sugestão para
> "café de origem única", e é ela mesma. A frase da marca vira o kicker; o `<h1>`
> carrega o termo. Nada é escondido: o que o buscador lê é o que a pessoa vê.

**O segundo botão sai.** Hoje há `Ver os cafés` + `Conhecer a serra`. Um CTA por
seção. `/a-serra` continua no menu e no rodapé.

### 3.2 Compre por formato — bloco 2

Cinco ladrilhos, grade `2 col mobile / 5 col desktop`. Foto 4:5 + título que **é**
o link. Sem preço, sem descrição, sem botão.

**Ordem canônica, e ela não muda em lugar nenhum** — nem no `ItemList.position`,
nem no bloco Explore:

| Ladrilho | Texto (é o rótulo **e** a âncora **e** o breadcrumb) | Destino | Imagem |
|---|---|---|---|
| 1 | `Café em grãos` | `/cafes?formato=graos` | `comprar-cafe-em-graos.jpg` |
| 2 | `Café moído` | `/cafes?formato=moido` | `comprar-cafe-moido.jpg` |
| 3 | `Cápsulas de café` | `/cafes?formato=capsula` | `comprar-capsulas-de-cafe.jpg` |
| 4 | `Drip coffee` | `/cafes?formato=drip` | `comprar-drip-coffee.jpg` |
| 5 | `Kits e caixas` | `/cafes?tipo=kit` | ⚠️ `/pacote-classico.jpg` — ver abaixo |

A caixa alta vem por `text-transform: uppercase` no CSS — **nunca** maiúscula
digitada, que leitor de tela soletra.

> **Cápsulas e Drip estão 100% esgotados hoje.** Ladrilho que leva a lista vazia
> é pior que ladrilho que não existe. Ou o estoque volta antes do lançamento, ou
> esses dois ganham selo `Em breve` e não são clicáveis. Decida — não deixe como
> está.

> **O ladrilho 5 é o único sem imagem gerada, e a razão está medida.** A cena de
> kits ficou ótima — praça de bairro, banco de concreto, sombra dura de meio-dia,
> fiação com bobina — mas **três embalagens legíveis num quadro é o pior caso de
> fidelidade de rótulo**, e as seis variantes confirmaram: `SCA 80+` saiu
> `GLA GB)` e o peso `250g` virou **`200g`**, que é erro factual sobre o produto.
>
> A placa está em `entrega-site/_conferir/`. **A rota de conserto é composição
> local** — gerar a cena sem os pacotes e colar os três recortes reais por cima,
> que é a única com tipografia garantida. Até lá o ladrilho usa
> `/pacote-classico.jpg`, que já existe e é foto real.

Isto **substitui** o `<TrilhaDeCategorias>` na home. O componente continua no
repositório; a home deixa de chamá-lo.

### 3.3 A prateleira — bloco 3 · **primeira superfície de venda**

Trilho horizontal, `<Carrossel>` que já existe. `<CardProduto>` como está hoje:
foto, linha, formato, gramatura, **preço exato** e **botão de sacola**.

**Três correções obrigatórias antes de publicar:**

1. **O subtítulo do card precisa dizer `pacotes`.** Hoje `CardProduto.tsx` monta
   linha + formato + `gramas` e nunca `pacotes`. É o defeito 2 da §1. Uma caixa
   de 4×500 g tem de ler `Caixa com 4 pacotes de 500 g`, não `500 g`.
2. **Nunca renderizar `R$ 0,00`.** Preço ausente vira estado `Esgotado` com
   captura de e-mail "avise-me quando chegar".
3. **Parcelamento e Pix no card ou logo abaixo do trilho.** No Brasil o
   parcelamento é a âncora, não o preço cheio. `12x de R$ X` em Martian Mono.

#### Kits e caixas, dentro da prateleira

Trilho com preço e sacola, igual ao bloco 3. Presente se decide por orçamento,
então preço aqui é obrigatório.

**Depende do conserto 1 da §3.3** — sem o `pacotes` no subtítulo, este bloco é o
que mais mente.

### 3.4 Faixa de condições — bloco 4

Faixa fina, superfície `cal`, filete acima e abaixo. **Sem imagem, sem CTA.**
Três células em Martian Mono 12px, caixa alta:

```
FRETE GRÁTIS ACIMA DE R$ 149  ·  ATÉ 12X SEM JUROS  ·  PIX COM DESCONTO
```

É aqui que o mercado brasileiro entra sem quebrar a forma: as três objeções que
mais travam compra, no registro de **dado**, logo depois do primeiro preço — e
não como banner piscando no topo.

> **Cada célula precisa ser verdade antes de subir.** O "R$ 149" de hoje é
> fallback chumbado no código porque a coluna `frete_gratis_minimo_centavos` não
> existe no banco (§0). Se o Pix não tem desconto, **a terceira célula sai** — não
> se inventa condição comercial.

### 3.5 As linhas — bloco 6 · capítulo + grade

Cartão de **texto puro**. Sem imagem, sem CTA — é o `containerType='text'` da
Nike, que separa capítulos e dá ao olho onde descansar.

```
h2     As linhas do Canastra
corpo  Três torras, uma origem. Clássico escuro, Suave médio, Canela para quem
       gosta de doce.
```

Respiro vertical generoso (`py-20 md:py-28`).

#### A grade, logo abaixo do capítulo

Três ladrilhos: Clássico, Suave, Canela. Foto 4:5 + kicker com as notas + título
que é o link. **Sem preço** — quem já sabe a linha vai para a listagem dela.

| Linha | Kicker | Texto/âncora | Destino | Imagem |
|---|---|---|---|---|
| Clássico | `CARAMELO · CHOCOLATE` | `Café Clássico` | `/cafes?linha=classico` | `/pacote-classico.jpg` ✅ |
| Suave | `CHOCOLATE · CÍTRICO` | `Café Suave` | `/cafes?linha=suave` | `/pacote-suave.jpg` ✅ |
| Canela | `CARAMELO · CANELA` | `Café Canela` | `/cafes?linha=canela` | `/pacote-canela.jpg` ✅ |

As notas saem de `data/catalogo-canastra.json → linhas[].notas`. Não escreva à mão.

### 3.6 A serra — bloco 7 · banda de campanha · superfície `fuligem`

Banda full-bleed, foto sangra na largura toda, altura `~55vh`, texto **abaixo**
da foto, centrado. kicker + `<h2>` + uma linha + **um** `<BotaoLink>`.

**A foto é real** — não gerada. `serra-da-canastra-chapadao-21x9.jpg`, do acervo
próprio, 3840×1646. É a única imagem do site que não precisa de nenhuma ressalva,
e é a mais bonita que a marca tem.

```
kicker  MEDEIROS · MINAS GERAIS · 1.250 M
h2      O chapadão.
corpo   O grão amadurece devagar onde a noite é fria. É isso que dá doçura.
cta     Conhecer a serra  →  /a-serra
```

> Este é o único CTA da home que não começa com "Comprar". A exceção é
> deliberada e é uma só: o destino é institucional, e chamá-lo de "Comprar"
> seria mentira. **Não abra uma segunda exceção.**

### 3.7 Clube da Canastra — bloco 5 · **segunda superfície de venda**

Superfície `mata`, a única escura do miolo. Foto à esquerda, texto à direita
(no mobile, foto em cima).

```
kicker  ASSINATURA
h2      Clube da Canastra
corpo   Café novo em casa a cada 15, 30 ou 45 dias, moído do jeito que você
        prepara. Cancele quando quiser, sem multa.
tarja   A PARTIR DE R$ XX,XX / MÊS
cta     Assinar o Clube  →  /clube
```

> **Contraste:** `estetica.md §4.1` — vermelho sobre mata é 2,0:1, **proibido**.
> CTA em `variante="primarioEscuro"`, cor `cal`. Não troque.

A tarja de preço é o que faz esta banda vender em vez de só apresentar. Puxe o
valor real do plano mais barato; se ainda não existir, **a banda sai** até
existir — banda de assinatura sem preço é folheto.

### 3.8 Do pé à xícara — bloco 8

Banda de foto full-bleed no topo (~40vh) e as cinco etapas em `<ol>` abaixo.
Mantenha a numeração calculada que já existe (`numeroDaEtapa`) — é sequência real
e irreversível, não enfeite.

Imagem: `cafezal-serra-da-canastra-21x9.jpg`, **foto real** do acervo (iPhone 7,
EXIF + GPS, altitude gravada 1.235–1.272 m — o arquivo prova sozinho os "1.250
metros" que a marca alega).

### 3.9 Explore — bloco 9

Grade densa de links de texto, sem foto, antes do rodapé. Archivo Cond 600, caixa
alta, 13px. Quatro colunas no desktop, duas no mobile.

É o bloco que devolve à home a autoridade que ela distribui para as folhas.
Colunas: **Por formato** · **Por linha** · **A Canastra** · **Ajuda**.

### 3.10 O que sai da home

| Sai | Motivo |
|---|---|
| `<SecaoDoBlog>` | Hoje é casca: `"O caderno ainda está em branco."` A Nike não publica seção vazia. Volta quando houver post. |
| A faixa de prova de 4 colunas | Reabsorvida como tarja de dado dentro do herói. |
| O segundo botão do herói | Um CTA por seção. |
| `<TrilhaDeCategorias>` na home | Substituída pelos ladrilhos com foto. |

**Não remova** `<BarraFreteGratis>` nem `<BotaoWhatsApp>`. A Nike não os tem; o
mercado brasileiro cobra a ausência. Registre em comentário no código que é
divergência deliberada, para a próxima sessão não "corrigir".

---

## 4. Regras de escrita

### Um verbo

`Comprar` em tudo que leva a superfície de compra. `Assinar o Clube` para o
clube. `Conhecer a serra` é a **única** exceção institucional.

### Vocabulário proibido

Nenhuma variação de posicionamento de massa: **popular, acessível, barato,
econômico, para todos, democrático, custo-benefício, preço justo**. O site fala
como café especial; a amplitude aparece na variedade de formato e no elenco das
fotos — nunca no texto.

Também proibido pelo `estetica.md §11`: caricatura mineira (*uai*, *trem bão*,
*sô*), exclamação em CTA, emoji em estado vazio, frase acima de 20 palavras.

### Os fatos que a home pode afirmar

| Fato | Fonte |
|---|---|
| Família planta café **desde 1985** | `a-serra/conteudo.ts` |
| Na **Serra da Canastra desde 2008** | idem |
| Torrefação própria **desde 2016** — *não* desde 1985 | idem |
| Medeiros/MG, **1.250 m** | EXIF das fotos: altitude 1.235–1.272 m |
| Microtorrefação em **Uberlândia** | `catalogo-canastra.json` |
| Variedades **Arara, Caturra 2SL, Paraíso** | `marca.variedades` |
| **Torra sob demanda**, em lotes pequenos | atributo declarado |
| Microlote **SCA 86**; Néctar de Minas **SCA 75** | `linhas[].scaExata: true` |

**Não afirme:** "lote rastreado" (a `/rastreabilidade` diz que não há código por
embalagem), **"SCA 80+" sobre a coleção** (falso para o Néctar, que tem 75), nem
"torrado desde 1985". "Carbono zero" e "100% fotovoltaica" só entram como display
se houver página de prova; sem certificado de terceiro, ficam na ficha técnica.

---

## 5. SEO

Termos levantados no autocomplete do Google BR (`suggestqueries.google.com`,
`hl=pt-BR&gl=br`) em 25/08/2026. Dez sugestões = demanda alta; uma a três =
residual. É proxy verificável, não volume absoluto.

### O achado que muda o título

O `<title>` de hoje é `Café Canastra — Café de origem única da Serra da
Canastra`. O seed `cafe de origem unica` devolve **uma** sugestão: ela mesma.

**Em português, "origem única" é vocabulário de marca, não de busca.** O mesmo
erro está no `/es`. Só o `/en` acerta — `single origin coffee` tem autocomplete
cheio.

| Locale | `<title>` | car. |
|---|---|---:|
| `pt` | `Café Canastra \| Café Especial da Serra da Canastra` | 49 |
| `en` | `Café Canastra \| Brazilian Specialty Coffee, Single Origin` | 57 |
| `es` | `Café Canastra \| Café de Especialidad Brasileño` | 46 |

| Locale | `<meta description>` |
|---|---|
| `pt` | `Da Serra da Canastra para a sua xícara: café especial 100% arábica, torrado sob demanda em lotes pequenos. Grãos, moído, drip coffee, cápsulas e kits.` |
| `en` | `Single origin specialty coffee from the Serra da Canastra, Minas Gerais, at 1,250 m. Whole bean, ground, drip bags and capsules, roasted to order.` |
| `es` | `Café de especialidad brasileño de la Serra da Canastra, a 1.250 m. En grano, molido, drip coffee y cápsulas, tostado bajo pedido en lotes pequeños.` |

A description em `pt` enumera os quatro formatos de propósito: **é assim que o
posicionamento expressa amplitude sem usar nenhuma palavra proibida.**

> **Não escreva "SCA 80+" em nenhuma das três.** `cafe sca 80` devolve uma
> sugestão — não é vocabulário de busca do consumidor brasileiro. E 80+ é o piso
> da coleção, **falso para o Néctar de Minas**. Afirmação de coleção na meta
> description é afirmação sobre tudo.
>
> Conte os caracteres antes de commitar.

### Os termos que valem, por página

| Página | Mira |
|---|---|
| `/` | marca (`café canastra`, `café canastra é bom`) + `café especial da Serra da Canastra` |
| `/cafes` | `café especial em grãos`, `café especial 250g`, `comprar café especial online` |
| PDP | linha + formato + **perfil de torra** (`café especial torra escura`) |
| `/clube` | `assinatura de café especial mensal`, `clube de cafés especiais` |
| `/a-serra` | **terroir**: `café cerrado mineiro`, altitude, variedades |

**Canibalização a evitar:** `/a-serra` e a home usam hoje a mesma frase no title.
A home vence sempre. Dê à `/a-serra` o ângulo de terroir e deixe o termo
comercial puro na home.

### O cluster geográfico — e por que ele casa com as fotos

O seed `onde comprar café especial` devolve **dez sugestões, e todas as dez são
cidades**: BH e São Paulo à frente. É o cluster transacional mais denso da
pesquisa inteira.

**As fotos urbanas que este plano entrega são exatamente o ativo que páginas
"café especial em São Paulo" e "café especial em BH" vão precisar.** São o
primeiro conteúdo editorial a produzir depois do lançamento.

### Três problemas que esta tarefa não resolve

1. **Título duplicado**: `/cafes`, `/historia` e as PDPs saem como
   `Cafés — Café Canastra — Café Canastra`. A página passa um título que já
   inclui o sufixo e o `title.template` do layout aplica de novo. Em `/cafes`
   sobram 22 caracteres úteis. **A home escapa porque usa `title: { absolute }`;
   mantenha isso.**
2. **Nenhuma URL filtrada está no sitemap.** O `app/sitemap.ts` emite `/cafes` e
   `/cafes/[slug]`, nada mais. Os cinco ladrilhos de formato apontam para *query
   params*, que roteiam o usuário mas **não são alvos indexáveis**. Saída: rotas
   reais (`/cafes/em-graos`) ou, mais barato, acrescentar as URLs filtradas ao
   sitemap com canonical próprio.
3. **O domínio de teste está indexável.** `loja.canastrainteligencia.com` serve
   42 URLs com canonicals próprios. Como `cafecanastra.com` e
   `loja.cafecanastra.com` serão os definitivos, **o de teste precisa de
   `noindex` agora** e de 301 no corte — senão os dois competem.

---

## 6. As imagens

Entregues em `entrega-site/`. Copie para `frontend/public/`.

**Como foram feitas.** Cada pessoa é ficcional e existe primeiro como um avatar
gerado do zero — instantâneo de celular contra parede lisa, com pedido explícito
de pele com poro, oleosidade, assimetria, mancha e acne. Nenhum rosto parte de
foto de pessoa real. O avatar entra como referência na geração da cena, que é o
único jeito de o mesmo rosto sobreviver entre duas imagens.

**Onde a embalagem aparece, ela é pixel de foto real.** O packshot entra junto no
campo de fontes e o prompt nunca descreve o rótulo — descrever faz o modelo
redesenhar, e o que sai é um sósia da marca.

**Quatro descobertas da execução, registradas porque custaram tempo:**

1. **Os packshots estão rotacionados no arquivo.** Abertos como estão, o pacote
   parece deitado e o modelo o reproduz **de cabeça para baixo** — foi o que a
   primeira sonda devolveu, com o rótulo espelhado. Girados −90°, são o que
   sempre foram: o pacote em pé contra a parede, arte inteira legível. Isso
   corrigiu de uma vez a fidelidade do rótulo. Ver `saida-teste/packshot-em-pe/`.
2. **A ordem das fontes decide o rosto.** Com o packshot na frente, o rosto
   derivou do avatar e saiu outra pessoa. Com o avatar na frente, ele segura.
3. **`Desde 1985` não sobrevive em nenhuma variante.** Conferido com recorte
   ampliado nas seis do ladrilho de moído: `Café CANASTRA`, a serra,
   `SPECIALTY / ESPECIAL / SCA 80+` e `250g` saem certos; o manuscrito pequeno
   sai como rabisco. É a lição 13, e é previsível — abaixo de ~2% da altura do
   quadro a tipografia é reescrita. **No ladrilho renderizado a ~400px isso são
   três pixels e ninguém lê.** Mas não use nenhuma dessas imagens ampliada, e
   não as use na PDP.
4. **Eu inventei um objeto e a pesquisa me pegou.** Escrevi que o copo americano
   tem "facetas verticais rasas". Ele não tem: é um **tronco de cone liso**, base
   estreita, boca larga — e é justamente essa conicidade que o faz empilhar.
   190 ml, 9,3 cm, 105 g. O descritor foi corrigido contra a ficha do fabricante.
   **Objeto descrito de memória sai genérico; genérico é o que denuncia.**

**Perfil de câmera, medido nas variantes e calibrado contra as fotos reais do
próprio acervo** (que dão p1 6–29, saturação 76–91, R/B 0,84–1,12):

| | p1 | preto% | satur | R/B |
|---|---:|---:|---:|---:|
| alvo do projeto | 14,0 | 0,007 | 70,0 | 0,969 |
| foto real do cafezal | 6,3 | 0,211 | 91,1 | 0,839 |
| **herói escolhido** | 3,0 | 0,352 | 93,9 | 0,822 |

O herói está na mesma faixa da foto real tirada no mesmo lugar. É esse o
benchmark que importa — não o alvo abstrato, que foi medido num conjunto misto.

Foco profundo sem exceção em todas: desfoque não se desfaz em pós, morre na
geração ou não morre.

> **Rotulagem.** `docs/POLITICA-IA.md §5` diz que não existe imagem de IA da casa
> que dispense o aviso. As imagens geradas deste lote precisam de metadado de
> origem e de decisão sua sobre onde o aviso aparece no site. As duas fotos reais
> (`serra-...` e `cafezal-...`) não precisam de nada.

---

## 7. Ordem de execução

Não é a ordem que dá vontade. É a ordem que faz o site funcionar.

**P0 — a loja precisa vender.** Publicar a API Express atrás do nginx; trocar
`API_BASE` de `/api` relativo para URL absoluta no servidor; aplicar as migrações
0009–0016; conferir que `produtoId` aparece no HTML. **Critério: um item entra na
sacola.** Sem isso, nada abaixo importa.

**P1 — os sete defeitos da §1.** `R$ 0,00`, o card de caixa que mente no peso, a
foto do Néctar, o bloco de kits da PLP, os esgotados na trilha, a newsletter 404,
o `noindex` no domínio de teste.

**P2 — a home nova.** Os 11 blocos da §3, com as imagens de `entrega-site/`.

**P3 — SEO.** Títulos e descriptions da §5, sitemap com as URLs filtradas, o
título duplicado.

**P4 — medir.** Instrumentar antes e depois. Sem baseline ninguém vai saber se a
home nova ajudou ou atrapalhou — e essa é a única pergunta que importa.

---

## 8. Critérios de aceite

```bash
cd frontend
npm run lint && npx tsc --noEmit && npm test && npm run build
```

- [ ] **Um produto entra na sacola** no ambiente publicado
- [ ] `grep -c produtoId` no HTML da home é **maior que zero**
- [ ] Nenhuma página renderiza `R$ 0,00`
- [ ] Todo card de caixa diz quantos pacotes tem
- [ ] Todo CTA visível começa com `Comprar`, ou é `Assinar o Clube`, ou é a
      exceção única `Conhecer a serra`
- [ ] `<h1>` e todos os `<h2>` usam o mesmo token de tamanho
- [ ] Nenhuma superfície escura encosta noutra escura
- [ ] Cada `?formato=` e `?linha=` foi aberto e devolve resultado — liste quais
- [ ] As três home saem do build como HTML estático
- [ ] Nenhuma palavra da lista proibida aparece no arquivo
- [ ] LCP, INP e CLS medidos em mobile, antes e depois
- [ ] Contraste medido na zona de texto do herói, ≥ 7:1 para `cal`

**Se um item falhar, diga qual e por quê. Não ajuste o critério para ele passar.**
