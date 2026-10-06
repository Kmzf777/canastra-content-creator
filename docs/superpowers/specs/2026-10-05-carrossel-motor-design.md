# Motor de carrossel — spec

Data: 05/10/2026. Implementa `instagram/carrossel/`.

## O problema, em uma frase

O carrossel de cápsulas publicado em 05/10 tem **um tipo de slide repetido cinco
vezes** — foto em cima, faixa terra embaixo, manchete e subtítulo. O cliente chamou
de genérico, e está certo: o defeito não é a paleta, é a **falta de taxonomia**.

## O que foi lido antes de decidir

Quatro skills públicas, baixadas e lidas em 05/10/2026:

| Repo | ★ | O que entrega de fato |
|---|---:|---|
| `itchernetski/threads-carousel-claude-skill` | 107 | 12 tipos de slide, 8 fundos, 6 formatos, 3 eixos de estilo compostos em runtime |
| `jeevanbavandla/instagram-carousel-skill` | 8 | 4 estilos com CSS, **área segura da UI do Instagram**, ritmo de fundo, design fixo 420×525 |
| `charlie947/social-media-skills` | 3.790 | toolkit de 17 skills; a de design escolhe entre HTML/CSS e prompt de imagem |
| `charlesdove977/carousel-builder` | 44 | orquestração Higgsfield→Canva; o valor são **theme-lock** e **orçamento de caracteres** |

Decisão tomada com o Rafael: **portar a taxonomia do `itchernetski`, redesenhar o CSS.**
Ficam os nomes e a estrutura de dados; nenhum pixel deles entra.

## O que esta spec NÃO governa

- realismo de foto e perfil de câmera → `canastra-cena`
- fidelidade de rótulo e a escada de correção → `canastra-embalagem`, `canastra-estatico`
- fluxo do ChatGPT e conferência ampliada → `canastra-conteudo`

Este motor manda em **composição de slide e montagem do deck**. Onde a direção de arte
colidir com a óptica, a óptica ganha.

---

## 1. Taxonomia de slides

Dez tipos. Nove portados do `itchernetski` (podando `emoji`, `checklist` e fundindo
`hook`/`body`); um — `prova` — é nosso e não existe lá.

| Tipo | Campos obrigatórios | Campos opcionais |
|---|---|---|
| `capa` | `manchete` | `sub`, `badge` |
| `conceito` | `titulo`, `corpo` | — |
| `lista` | `titulo`, `itens` (2–6) | — |
| `passo` | `titulo`, `passos` (2–5, cada um `titulo` + `texto?`) | — |
| `comparacao` | `rotulo_esq`, `itens_esq`, `rotulo_dir`, `itens_dir` | `titulo` |
| `numero` | `numero`, `rotulo` | `sub` |
| `citacao` | `frase` | `autor`, `papel` |
| `produto` | `nome`, `descritor` | `sub` |
| `prova` | `afirmacao`, `evidencia`, `fonte` | — |
| `fecho` | `manchete` | `sub`, `destino` |

**Por que `prova` existe.** O posicionamento da marca é "a gente consegue provar": GPS
no EXIF, 41 anúncios medidos, 1.250 m no arquivo. Um tipo de slide que **exige** o
campo `fonte` transforma isso em estrutura em vez de boa intenção. `fonte` vazia
reprova a declaração, como `Dado.origem` já faz em `instagram/estaticos/catalogo.py`.

## 2. Eixos travados

O `itchernetski` compõe fonte × superfície × acento em 440 combinações. Para **uma**
marca isso é defeito. Aqui superfície e acento são constantes dos tokens de
`instagram/remotion/src/identidade/tokens.ts`:

```
terra  #3B2A1F   creme #F1ECE0   verde #4A5D3A   acento #C8661E   preto #14100D
Archivo Black (manchete) · Inter (corpo) · IBM Plex Mono (dado/rodapé)
```

O que varia é **tipo de slide** e **fundo**. Nada mais.

## 3. Fundo e ritmo

`fundo` ∈ `foto` | `terra` | `creme`.

Regras, verificadas por portão:

- `capa` é sempre `foto`;
- `fecho` é sempre `terra` — é a constante que fecha todo deck;
- **nunca três slides seguidos com o mesmo fundo**;
- slide `fundo="foto"` exige o campo `foto`; `terra` e `creme` o proíbem.

## 4. Área segura

Portado de `jeevanbavandla`: 80px de topo e 52px de base num design de 525px de
altura, para limpar o cabeçalho do perfil e a barra de progresso do Instagram.

Convertido ao nosso 1080×1350: **topo 206px, base 134px** (15,24% e 9,90%).

> **[a conferir]** Esses números são do repo deles, não medidos por nós numa captura
> real do app. Até alguém medir, valem como margem conservadora — e a consequência de
> estarem errados é texto atrás da UI, não peça quebrada.

## 5. Os três portões

Nenhum dos quatro repos tem os três juntos. É aqui que o motor ganha deles.

### 5.1 `orcamento` — declarado

Teto de caracteres por campo. Estourou, **recusa antes de renderizar**. Vem do
`charlesdove977`, onde texto fora do orçamento reflui a caixa e quebra a unidade.

Tetos iniciais (decisão nossa, não medição):

| Campo | Teto |
|---|---:|
| `manchete` | 60 |
| `titulo` | 42 |
| `corpo` | 220 |
| `sub` | 120 |
| item de `lista` | 60 |
| `passos[].titulo` | 34 |
| `passos[].texto` | 90 |
| `frase` | 160 |
| `numero` | 8 |
| `afirmacao` | 90 |
| `evidencia` | 120 |
| `fonte` | 90 |

### 5.2 `transbordo` — medido

Depois de renderizar, o Chrome headless mede `scrollHeight > clientHeight` em cada
caixa de texto e devolve a lista de quem transbordou. **É medição, não declaração** —
o orçamento de caracteres é heurística; isto é o fato.

### 5.3 `legibilidade` — medido e inspecionado

Do `charlie947`: inspecionar no tamanho do feed, ~360px de largura, 320px na
miniatura — não só em tamanho cheio.

- **Piso declarado:** nenhum texto abaixo de **11px no feed de 360px**, ou seja
  **33px no quadro de 1080**. O portão lê os tamanhos computados e reprova abaixo disso.
- **Além do número:** o render emite `_feed/360.png` e `_feed/320.png` de cada slide,
  para inspeção humana. Número não substitui olhar.

> O piso de 11px é **decisão**, não medição. Está aqui para ser contestado com um teste
> de leitura, não para ser citado como fato.

## 6. Theme-lock na geração

Do `charlesdove977`, adaptado à nossa pilha (`claude-in-chrome + ChatGPT`, nunca
Higgsfield):

1. gera e **aprova a capa** primeiro — ela é a âncora;
2. toda imagem seguinte do deck anexa **a capa aprovada** como referência adicional;
3. o prompt termina com: *"Match the colour palette, lighting, art style, texture and
   mood of the provided reference photograph exactly. Change only the subject
   described above."*

Resolve a lição 8 por construção, em vez de repetir a descrição da cena em texto.

## 7. Ordem de trabalho

Do `charlesdove977`: **copy aprovada antes de qualquer geração.** Em 05/10 fizemos ao
contrário — geramos quatro imagens e escrevemos o texto depois.

```
declarar o deck -> portão orcamento -> aprovar copy
   -> gerar e aprovar a CAPA -> gerar o resto com theme-lock
   -> render -> portões transbordo e legibilidade -> bundle
```

## 8. Arquivos

```
instagram/carrossel/
  tipos.py      taxonomia, dataclasses, validação de campos
  molde.py      tokens, área segura, ritmo de fundo, orçamentos
  portoes.py    os três portões
  render.py     HTML/CSS por tipo + Chrome headless + medições
  catalogo.py   decks declarados
  cli.py        conferir | listar | render | portoes
```

CLI espelha `instagram/estaticos`: `conferir` devolve **1** quando a declaração tem
problema, de propósito, para quebrar script que ignore o relatório.

## 9. Como se prova que funciona

- `pytest` verde nos quatro módulos;
- um deck real declarado e renderizado em 1080×1350 exatos;
- os três portões rodados com saída registrada;
- `_feed/360.png` gerado e **olhado**.
