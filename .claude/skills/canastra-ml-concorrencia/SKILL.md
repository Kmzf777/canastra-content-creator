---
name: canastra-ml-concorrencia
description: Use when researching competitors on Mercado Livre for Café Canastra — running searches, scraping result cards, opening leading listings, computing price medians, or refreshing an existing competitor survey. Covers the Claude in Chrome recipe that works and the traps that corrupt the data.
---

# Concorrência no Mercado Livre

Pesquisas anteriores (comece por elas, não do zero):

| Tema | Documento | Dados crus |
|---|---|---|
| Cápsulas | `mercadolivre/04-concorrencia.md` | — |
| 1 kg grãos e moído | `mercadolivre/14-estrategia-1kg.md` §3 e §3b | `pesquisa/concorrencia-1kg-*.tsv` / `.json` |

## Receita de busca (medida em 08/10/2026)

| Passo | Como |
|---|---|
| 1 | `navigate` para `https://lista.mercadolivre.com.br/<termo-com-hifens>` |
| 2 | `wait` 3 s → `screenshot` (escala 0,15 basta; força o render) → `wait` 3 s |
| 3 | colar e rodar o conteúdo de `mercadolivre/scripts/extrator_busca.js` no `javascript_tool` |
| 4 | a saída do `javascript_tool` **trunca em ~1.000 caracteres**: acumule e resuma no próprio JS (contagem, mediana, top 10) em vez de devolver a tabela |

- **Busca não trava**; o que parece trava é a **janela oculta** (lista no spinner, DOM sem
  `poly-card`). Screenshot destrava.
- **Um download automático por aba**; o segundo some sem erro. `localStorage` é por origem.
- O preço grande do card é o **preço Pix**; o cheio é ~R$ 10 acima.
- **Selos de vendidos são faixas acumuladas** (+500, +1.000), não vendas do mês.

## Abrir o anúncio líder

Card não basta: título, ficha, fotos, vídeo, descrição, atacado e opiniões estão dentro.
Use `mercadolivre/scripts/extrator_anuncio.js`. **Rastreie o nó pai antes de usar número
raspado**: blocos `poly-card` numa página de produto são carrossel de recomendação, não o
produto aberto (o "+10 mil vendidos" já foi lido do carrossel por engano).

## O que comparar, sempre no mesmo recorte

Compare **iguais com iguais**: especial 80+ em grãos com especial em grãos; gourmet com
gourmet; unitário com unitário; kit por **preço por kg**. Reporte n, p25, mediana, p75 e
quem vende volume (selo, nota, preço), e onde o nosso anúncio cai nessa distribuição.

## Registrar

Grave o recorte com data em `mercadolivre/pesquisa/` (`<tema>-AAAA-MM-DD.tsv`) e a leitura no
documento do tema, com a data. Pesquisa sem data vira número velho tratado como novo.
