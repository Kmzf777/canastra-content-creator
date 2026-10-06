---
name: canastra-carrossel
description: Use when producing a Café Canastra carousel — múltiplos slides 4:5 para o feed, deck de produto, "arraste para entender", carrossel educativo ou de autosseleção — or when a deck came out looking generic and needs slide variety, or when running the three gates in instagram/carrossel.
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
- Você vai gerar imagem **antes** de a copy estar aprovada.
- Você vai gerar o slide 3 **sem anexar a capa aprovada**.
- Você declarou um `prova` e deixou `fonte` vazia, ou pôs ali "conhecimento geral".
- Os três portões passaram e você **não abriu o `_feed`**.
- Você está prestes a mudar um teto de `molde.ORCAMENTO` porque o texto não coube —
  **encurte o texto ou troque o tipo de slide**; o teto existe para isso.
