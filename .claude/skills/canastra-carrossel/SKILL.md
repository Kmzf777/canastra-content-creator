---
name: canastra-carrossel
description: Use when producing a Café Canastra carousel — múltiplos slides 4:5 para o feed, deck de produto, "arraste para entender", carrossel educativo, de história ou de autosseleção — or when a deck came out looking generic and needs slide variety, when building slides in Claude Design, when a new deck must follow the approved "Céu a pino" style, or when running the three gates in instagram/carrossel.
---

# Carrossel — o deck e seus portões

Esta skill manda em **composição de slide e montagem do deck**. O motor é
`instagram/carrossel/`, e a spec é
`docs/superpowers/specs/2026-10-05-carrossel-motor-design.md`.

## Rotear primeiro

| Assunto | Dono |
|---|---|
| fluxo de 5 fases, mecânica do ChatGPT, conferência ampliada | **canastra-conteudo** |
| fidelidade de rótulo e a escada de correção | **canastra-embalagem**, **canastra-estatico** |
| realismo de foto, perfil de câmera, procedência | **canastra-cena** |
| que chão, que empilhamento, que paleta na foto | **canastra-direcao** |
| **quantos slides, de que tipo, com que ritmo, e os três portões** | **esta skill** |

**Onde a composição colidir com a óptica, a óptica ganha.** Se o layout pedir
desfoque para ficar bonito, `canastra-cena` vence.

---

## A causa do "genérico", nomeada

Em 05/10/2026 publiquei um carrossel de cinco slides com **um tipo só repetido**:
foto em cima, faixa terra embaixo, manchete, subtítulo. O cliente chamou de
genérico e estava certo. **O defeito não era a paleta — era a falta de taxonomia.**

Dez tipos existem para que isso não se repita:

| Tipo | Para quê |
|---|---|
| `capa` | a pergunta ou a afirmação que faz arrastar |
| `conceito` | um título e um parágrafo |
| `lista` | 2 a 6 itens |
| `passo` | 2 a 5 passos numerados |
| `comparacao` | dois lados rotulados |
| `numero` | um número gigante e o que ele é |
| `citacao` | frase com autor |
| `produto` | um SKU, nome e descritor |
| **`prova`** | **afirmação + evidência + `fonte` obrigatória** |
| `fecho` | a chamada e o destino |

**`prova` é nosso, não veio de repo nenhum.** O posicionamento da marca é "a gente
consegue provar" — GPS no EXIF, 41 anúncios medidos, 1.250 m gravados no arquivo.
Declaração sem `fonte` **não passa** em `tipos.validar`. É a mesma ideia do
`Dado.origem` do motor de estáticos: a regra vira estrutura, não boa intenção.

---

## O que é constante e o que varia

Superfície e acento são **travados** nos tokens da marca — terra, creme, verde,
acento, e Archivo Black / Inter / IBM Plex Mono. Quatro estilos diferentes é erro
para **uma** marca: o feed vira colcha de retalhos.

O que varia é **tipo de slide** e **fundo** (`foto` · `terra` · `creme`), e o ritmo
tem regra verificada: capa sempre `foto`, fecho sempre `terra`, e **nunca três
slides seguidos com o mesmo fundo**.

---

## Diretriz do cliente, 07/10/2026: todo slide tem imagem planejada

Pedido explícito do cliente, depois de ver os slides 1 e 2:

- **Todo slide tem imagem**, e ela é **planejada antes de gerar**. A lista de fotos
  (slide → imagem → real ou gerada → referências) vai para aprovação **junto com a
  copy**. Slide só tipográfico (fundo `creme` ou `terra` liso) não entra mais. A regra
  de ritmo de fundo cede a esta.
- **Copy de rede social, não editorial.** Frase curta, "você" e "a gente", uma ideia por
  slide, e chamada de engajamento no fim. Nada de "capítulo", página, linha do tempo ou
  parágrafo de enciclopédia.
- **Reforçar marca e altitude**: a logo de `marca/logo/` pequena no topo de todo slide,
  e a logo grande assinando o fecho. A altitude entra pela copy; o selo `▲ 1.250 m` foi
  testado e o cliente o tirou.

A camada gráfica abaixo (kicker de capítulo, número gigante, pílula) foi a v1 e ficou
**editorial demais**. A **v2 social** (10 slides no canvas, `V2-01…V2-10`, aguardando
aprovação final) segue estas escolhas do cliente:

- **Logo no topo, centralizada, pequena e translúcida:** `left: 50%; top: 64px;
  height: 84px; transform: translateX(-50%); opacity: 0.7`. É preta sobre céu e branca
  quando o topo da foto é escuro; confira no render, porque a logo some sobre fundo do
  mesmo tom.
- **Sem selo de altitude.** O cliente tirou o `▲ 1.250 m` do topo. A altitude entra
  pela copy (capa, slide da altitude, slide do GPS).
- **Manchete curta** (Archivo Black 72 a 84px), com a palavra-chave em marca-texto
  preto (`background: #14100D; color: #F1ECE0`), e uma linha de apoio (Inter 600, 36 a
  38px).
- **Texto direto no céu** quando ele é largo. Sobre fundo cheio (folhagem, vale escuro),
  use **blocos de marca-texto por linha** (`box-decoration-break: clone`).
- **Fecho** com a logo grande e dois selos: `Segue @cafecanastra` e `cafecanastra.com`.

A **foto** do Céu a pino continua valendo.

## O estilo aprovado: Céu a pino

**Aprovado pelo cliente em 07/10/2026**, nos slides 1 e 2 do carrossel de história.
É o padrão dos próximos decks até o cliente pedir outro. O molde completo está em
`ceu-a-pino.md`, nesta pasta: prompts, artboards, como escolher o recorte e
contraste medido.

**A ideia: o céu de meio-dia é a página.** A foto é composta para deixar a metade de
cima livre, e o texto vai em preto direto sobre o azul, sem faixa, sem caixa e sem
degradê. **A faixa terra do `render.py` é o molde antigo**, o que o cliente chamou de
genérico em 05/10. Não a use em deck novo.

| Elemento | Regra |
|---|---|
| foto | celular no chão, horizonte baixo, assunto à direita, metade de cima só céu. É o look **Céu a pino** em `canastra-direcao` |
| linha de topo (y = 206) | kicker em Plex Mono 34px à esquerda; à direita, `ARRASTE →` na capa e `02/10` no miolo |
| manchete da capa | Archivo Black 92px, quebra de linha à mão, termina **acima** do topo do produto |
| número gigante | Archivo Black 270px: o ano, a altitude, o dado do slide |
| corpo | Inter 500 de 34 a 38px, coluna de 410 a 450px ao lado do assunto, termina acima do horizonte |
| pílula de navegação | escura, em y = 1136, com todos os marcos (anos ou etapas); o atual em `#E07A2E` com ponto |
| cor do texto | preto `#14100D` sobre o céu; o laranja **só** sobre fundo escuro, porque sobre o azul dá 1,5:1 |
| fecho | assina com a logo de `marca/logo/`, a branca sobre o terra |

**É o tratamento dos slides de fundo `foto`.** A regra de ritmo continua: entre fotos
entram slides `creme` e `terra` com a mesma grade (ver `ceu-a-pino.md` §3). **E só
serve para assunto ao ar livre, na fazenda.** Torra, moagem e xícara vão em slide
tipográfico ou noutro look.

**O design se monta no Claude Design (tipo Design)**, com um artboard 1080×1350 por
slide e o texto literal com `data-campo`. **A conferência é o `scripts/dc_render.py`**:
ele renderiza o mesmo HTML e roda `transbordo`, `legibilidade` e `_feed` do motor. Os
portões desta skill valem fora do motor também. O `orcamento` não roda lá: passe a
copy por `tipos.validar` antes de gerar.

**Texto só onde o céu foi medido.** O portão de legibilidade mede tamanho, não fundo.
Texto preto sobre copa de árvore passa no portão e some no feed. A receita de medição
está em `ceu-a-pino.md` §2.

---

## A ordem de trabalho, e ela não é negociável

```
declarar o deck -> portão orcamento -> APROVAR A COPY
   -> gerar e APROVAR A CAPA -> gerar o resto com theme-lock
   -> render -> portões transbordo e legibilidade -> olhar o _feed
```

Em 05/10 eu fiz ao contrário: gerei quatro imagens e escrevi o texto depois. Copy
aprovada primeiro é mais barato — texto se reescreve de graça, geração não.

### Theme-lock

A capa aprovada vira **âncora**. Toda imagem seguinte do deck anexa **a capa** como
referência adicional, e o prompt termina com:

> *Match the colour palette, lighting, art style, texture and mood of the provided
> reference photograph exactly. Change only the subject described above.*

Resolve a lição 8 por construção, em vez de repetir a descrição da cena em texto.
`python -m instagram.carrossel prompt <slug>` imprime os blocos na ordem certa.

**Quando a capa tem o produto, a âncora vai sem ele.** Anexe uma faixa da capa só
com céu, terra e fileiras, e diga *"of the FIRST photograph"* na frase final. Com o
pacote dentro da âncora, o modelo tem motivo para repetir o produto num slide que
não é sobre ele.

---

## Os três portões

```bash
python -m uv run python -m instagram.carrossel conferir          # devolve 1 se a declaracao falha
python -m uv run python -m instagram.carrossel listar
python -m uv run python -m instagram.carrossel prompt <slug>
python -m uv run python -m instagram.carrossel render <slug> --destino DIR
```

| Portão | Natureza | O que pega |
|---|---|---|
| `orcamento` | **declarado** | teto de caracteres por campo; recusa antes de gastar render |
| `transbordo` | **medido** | texto cortado, fora do quadro, ou invadindo a área segura da UI |
| `legibilidade` | medido contra piso declarado | texto abaixo de 33px no quadro = 11px no feed |

### Portão é necessário, não suficiente

Os três passaram no deck de teste e **o olho ainda pegou dois defeitos** que nenhum
deles vê: a faixa cobrindo a base da embalagem, e o `1.250 m` quebrando em duas
linhas. Por isso o render emite `_feed/360.png` e `_feed/320.png`, e por isso a
mensagem de sucesso termina em *"olhe o `_feed` antes de publicar"*.

**Abra as miniaturas. Número não substitui olhar.**

### E não confie num alarme que acende em tudo

A primeira rodada reprovou os sete slides por transbordo — em **todo** título.
Imprimindo o número cru em vez do booleano: `h1` de 92px com `line-height 1.03` dá
`sh=198 ch=190 delta=8` com `overflow: visible`, e nada é cortado. Lição 47.

---

## Bandeiras vermelhas — pare

- O deck tem **um tipo de slide só**. É o defeito que este motor existe para impedir.
- Um slide **não tem imagem**, ou a imagem dele não estava na lista aprovada com a copy.
- Você vai gerar imagem **antes** de a copy estar aprovada.
- Você vai gerar o slide 3 **sem anexar a capa aprovada**.
- Você declarou um `prova` e deixou `fonte` vazia, ou pôs ali "conhecimento geral".
- Os três portões passaram e você **não abriu o `_feed`**.
- Você está prestes a mudar um teto de `molde.ORCAMENTO` porque o texto não coube —
  **encurte o texto ou troque o tipo de slide**; o teto existe para isso.
- Você vai montar um slide de foto com **faixa terra embaixo**. É o molde antigo; o
  aprovado é o Céu a pino.
- Você posicionou texto **sem medir onde o céu termina**.
- O prompt pede câmera alta **e** o produto passando do horizonte (lição 48).
- A âncora de theme-lock **tem o pacote dentro**.
- Você vai descrever a logo num prompt em vez de usar o arquivo de `marca/logo/`.
