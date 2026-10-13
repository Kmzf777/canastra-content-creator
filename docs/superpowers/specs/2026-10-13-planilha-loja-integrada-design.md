# Planilha de produtos da Loja Integrada — design

**Data:** 13/10/2026 · **Branch:** `planilha-loja-integrada`

## O pedido

A Loja Integrada, pela parceria com a Intergalática, monta a loja em até 5 dias
úteis depois de receber os materiais, e o benefício tem validade de 30 dias
correndo. Pediram: logotipo em boa resolução, fotos mais a planilha de produtos
preenchida com **até 20 produtos**, domínio próprio, meios de pagamento e frete,
e referência para o banner.

**Escopo decidido pelo cliente em 13/10/2026:** só planilha, fotos e logo.
Domínio, pagamento, frete e banner ele trata direto com eles.

## As fontes

| Fonte | O que dá |
|---|---|
| `loja.cafecanastra.com` (Tray) | 42 produtos com nome, SKU, preço cheio, disponibilidade e descrição completa. Raspados via `sitemap_1.xml` + `curl` com UA de Chrome |
| `saida-teste/catalogo-estudio/` | 25 SKUs fotografados, cada um com frente em fundo branco e frente em fundo colorido, 1086×1448 PNG |
| `marca/logo/` | logo oficial preta e branca, com e sem recorte, fundo transparente |
| `mercadolivre/14-estrategia-1kg.md` | os EANs já lidos no verso das embalagens |
| planilha modelo da Loja Integrada | 49 colunas; `imagem-1..5` esperam URL |

## Os 20 produtos

As 20 unidades avulsas da Tray, sem kit e sem caneca:

Clássico e Suave em 250 g / 500 g / 1 kg, em grãos e moído (10) · Canela moído
250 g · Microlote grãos e moído 250 g · Néctar de Minas 1 kg grãos e 500 g moído
· Cápsulas Clássico, Suave e Canela 10 un · Drip Coffee Clássico e Suave 10 un.

Fica fora o **Drip Coffee Canela**, para fechar em 20. A Tray tem o **Suave em
Grãos 250 g duplicado** (SKU 49 e 63, mesmo nome e mesmo preço); entra uma linha
só — e isso é um defeito a corrigir na Tray.

## As fotos

Por produto: `N.1-frente-branco` e `N.2-frente-cor`. As três cápsulas levam mais
três cada — embalagem com a cápsula, cápsula isolada, três cápsulas. Total **49
arquivos**, convertidos de PNG para JPG abaixo de 1 MB, sem redimensionar
(lição 39: receita de vitrine não é portátil entre plataformas; o original 3:4 é
o que sobe).

**Não entram laterais nem versos.** São rascunhos e as lições 22 e 44 registram
que o carimbo de lote sai regenerado neles — `F: 23.2025`, um mês que não existe.
Informação regulatória falsa não vai para loja pública.

`imagem-1..5` ficam **vazias** por decisão do cliente: a entrega é de arquivos, e
a equipe da Loja Integrada sobe. A ponte produto → arquivo é o nome do arquivo e
a tabela do `LEIA-ME`.

## As colunas

| Coluna | De onde vem |
|---|---|
| `tipo` | `sem-variacao` nas 20 linhas |
| `sku` | código legível criado aqui (`CAN-CLA-GR-250`), com o SKU numérico da Tray registrado no `LEIA-ME` |
| `ativo` / `usado` / `destaque` | `S` / `N` / `N` |
| `nome` | o nome da Tray, sem o sufixo `- Café Canastra` que o `og:title` acrescenta |
| `descricao-completa` | a descrição da Tray, entidades HTML resolvidas e o rodapé de "Formas de Pagamento" cortado |
| `preco-cheio` | o preço cheio da Tray, medido em 13/10/2026 |
| `preco-promocional` | vazio |
| `marca` | `Café Canastra` |
| `categoria-nome-nivel-1/2` | espelha a árvore da Tray: Cafés Especiais → Em Grãos / Moídos para Coador / Cápsulas / Drip Coffee |
| `estoque-gerenciado` | `N`, com disponibilidade imediata — não temos número de estoque confiável e inventar quantidade é pior que não gerenciar |
| `gtin` | o EAN documentado onde existe; **vazio** onde o código nunca foi lido no verso |
| `ncm` | `09012100` (café torrado, não descafeinado), marcado para a contabilidade confirmar |
| `peso-em-kg`, dimensões | **estimados** a partir do peso líquido mais embalagem, e marcados como estimativa no `LEIA-ME` — afetam cálculo de frete |
| `seo-tag-title` / `seo-tag-description` | escritos aqui a partir do nome e das notas |

Não existe peso nem dimensão de postagem em lugar nenhum do projeto, nem na
página da Tray (medido: nenhum campo `weight`/`height` no HTML). Estimativa
declarada é melhor que número com cara de medido — lição 28, corolário da ausência.

## Os portões

1. **Rótulo, letra por letra.** Recorte ampliado da faixa de texto nas 20 frentes.
   As imagens são geradas; a lição 21 mostra que o acento cai antes do dígito, e a
   30 e a 38 mostram que o gabarito também erra. Qualquer peça com texto quebrado
   ou dado regulatório inventado não vai.
2. **Dado contra a fonte.** Nome e preço das 20 linhas conferidos um a um contra a
   página da Tray.
3. **Arquivo.** Cada JPG: 1086×1448, abaixo de 1 MB, e contagem de pixel não-branco
   na moldura do fundo para provar que o fundo é limpo.

Portão é necessário, não suficiente (lição 47): depois dos três, olhar a folha de
contato antes de enviar.

## A entrega

```
loja-integrada/
  planilha-produtos-cafe-canastra.xlsx    20 linhas no modelo oficial
  LEIA-ME.md                              produto → arquivos, SKU da Tray, o que é estimativa
  fotos/                                  49 JPGs nomeados por produto
  logo/                                   as 4 PNGs oficiais
```

Entregue ao cliente pelo Discord como arquivos.
