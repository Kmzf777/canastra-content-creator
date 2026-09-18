# Fotos de produto — organização por SKU

131 fotos do shoot de **11/09/2026** (15:51–16:41, Motorola), separadas por
**produto → gramatura → moagem**. Referência de catálogo: `tabela.cafecanastra.com`.

- `_MANIFESTO.tsv` — de/para completo (nome original → pasta → nome novo → face).
- `_reverter.sh` — desfaz tudo, devolvendo os nomes originais à raiz.

## O que foi fotografado

| Pasta | Fotos | Consta na tabela? |
|---|---:|---|
| `Canastra-Classico-250g-Moido` | 6 | sim — R$ 28,70 |
| `Canastra-Classico-250g-Graos` | 7 | sim — R$ 31,70 |
| `Canastra-Classico-500g-Moido` | 4 | sim — R$ 52,70 |
| `Canastra-Classico-500g-Graos` | 6 | sim — R$ 54,70 |
| `Canastra-Classico-1kg-Graos` | 4 | sim — R$ 97,70 |
| `Canastra-Suave-250g-Moido` | 7 | sim — R$ 28,70 |
| `Canastra-Suave-250g-Graos` | 5 | sim — R$ 31,70 |
| `Canastra-Suave-500g-Moido` | 5 | sim — R$ 52,70 |
| `Canastra-Suave-500g-Graos` | 5 | sim — R$ 54,70 |
| `Canastra-Suave-1kg-Graos` | 6 | sim — R$ 97,70 |
| `Canastra-Canela-250g-Moido` | 4 | sim — R$ 28,70 |
| `Microlote-250g-Moido` | 4 | sim — R$ 32,70 |
| `Microlote-250g-Graos` | 6 | sim — R$ 32,70 |
| `Nectar-de-Minas-Gourmet-500g-Moido` | 9 | sim — R$ 39,70 |
| `Nectar-de-Minas-Gourmet-1kg-Graos` | 5 | sim — R$ 88,70 |
| `Capsulas-Classico-10un-5g` | 11 | **não** |
| `Capsulas-Canela-10un-5g` | 12 | **não** |
| `Drip-Coffee-Classico-100g` | 9 | **não** |
| `Drip-Coffee-Suave-100g` | 8 | **não** |
| `Drip-Coffee-Canela-100g` | 8 | **não** |

## Buracos de cobertura

Produtos da tabela **sem nenhuma foto** neste shoot:

- Néctar de Minas Blend Arábica com Robusta — 1kg em grãos
- Granel Canastra Suave — 2kg em grãos
- Granel Canastra Clássico — 2kg em grãos
- Granel Néctar de Minas Espresso — 2kg em grãos
- Granel Néctar de Minas Intenso — 2kg em grãos
- Moedor Café Canastra

Produtos fotografados **ausentes da tabela de preços**: cápsulas (Clássico e
Canela) e drip coffee (Clássico, Suave e Canela).

## Como a moagem foi determinada

Cada linha marca moído/grãos de um jeito diferente na frente do pacote:

| Linha | Em grãos | Moído |
|---|---|---|
| Clássico 250g/500g | selo circular `CLÁSSICO EM GRÃOS · TORRA EXCLUSIVA` | sem selo; texto `CLÁSSICO / TORRADO E MOÍDO` |
| Clássico 1kg | texto `CLÁSSICO / TORRADO EM GRÃOS` | — (não existe) |
| Suave | texto `SUAVE / TORRADO EM GRÃOS`, tinta bordô | texto `SUAVE / TORRADO E MOÍDO`, tinta preta |
| Microlote | selo `CAFÉ TORRADO EM GRÃOS` | selo `CAFÉ MOÍDO PARA COADOR` |
| Néctar de Minas | `TORRADO EM GRÃOS` | `TORRADO E MOÍDO` |

**Cuidado com o verso.** O código de barras e o texto `ING.: CAFÉ TORRADO E
MOÍDO` do verso são os mesmos para moído e grãos do mesmo peso — conferido no
Microlote 250g (`7892262780140` nos dois) e no Clássico 500g
(`7892262780089` nos dois). O verso **não** distingue moagem; só a frente.

## Códigos de barras lidos

| Produto | EAN |
|---|---|
| Clássico 500g (moído e grãos) | 7892262780089 |
| Clássico 1kg grãos | 7892262780225 |
| Suave 500g grãos | 7892262780065 |
| Suave 500g moído | 7892262780027 |
| Suave 1kg grãos | 7892262780034 |
| Microlote 250g (moído e grãos) | 7892262780140 |
| Néctar Gourmet 500g moído | 7892262780164 |
| Néctar Gourmet 1kg grãos | 7892262780157 |
| Cápsulas Clássico | 7892262780096 |
| Cápsulas Canela | 7892262780102 |
| Drip Clássico | 7892262780188 |
| Drip Suave | 7892262780195 |
| Drip Canela | 7892262781239 |

## Nomenclatura dos arquivos

`<produto>-<gramatura>-<moagem>-<face>-NN.jpg`

`face` é `frente` (packshot frontal ou 3/4), `verso`, `lateral` ou `detalhe`
(macro). A numeração `NN` segue a ordem cronológica original do shoot.
