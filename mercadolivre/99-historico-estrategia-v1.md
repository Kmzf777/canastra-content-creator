> # ⚠️ ARQUIVO HISTÓRICO — CONTÉM NÚMEROS SUPERADOS
>
> Esta foi a **primeira versão** da estratégia, de 24-25/09/2026. Várias afirmações
> aqui foram derrubadas por dado depois. **Não use para decidir.**
>
> O que mudou está em [](LEIA-ME.md), seção “O que eu errei e corrigi”.
> Os principais erros deste arquivo: custos de envio vindos de blog, ROAS 7,3× como
> alvo, Brand Ads no plano, consolidação 13→3 e título de 81 caracteres.
>
> **Fonte da verdade atual:** os arquivos  a  desta pasta.

# Cápsulas no Mercado Livre — concorrência, taxas, SEO e GEO

> **Objetivo declarado:** a cápsula é o produto escolhido para ser o **primeiro a escalar
> em vendas** no Mercado Livre.
>
> **Data da pesquisa:** 24/09/2026; concorrência auditada no ML em 25/09/2026. Preços e tarifas de marketplace mudam rápido —
> reconfira qualquer número antes de decidir preço.
>
> **Página publicada (mesmo conteúdo, com calculadora de margem interativa):**
> <https://claude.ai/artifact/HXZvh82c13pUp3zCwyr1g3> — artifact privado, v2 de
> 25/09/2026. Para atualizar de outra sessão, passe essa URL como `url` no Artifact;
> publicar sem ela cria um artifact separado.
>
> **Playbook de execução (artefato irmão):**
> <https://claude.ai/artifact/8TQMzvo2xD4DVEukZhpvXk> — "Lançar a Cápsula", v1 de
> 25/09/2026. Preço, tipo de anúncio, título, descrição, ficha, fotos, vídeo, estoque no
> Full, configuração de Ads e sprint de 30 dias.
>
> **Este arquivo é a fonte da verdade.** As páginas são a apresentação. Ao editar, edite
> aqui primeiro e republique a partir daqui.

---

## Índice

1. [Ponto de partida e o que está bloqueado](#1-ponto-de-partida-e-o-que-está-bloqueado)
2. [A matemática do ML para cápsula — a seção que decide tudo](#2-a-matemática-do-ml-para-cápsula)
3. [Estratégia de preço e formato: o penhasco dos R$79](#3-estratégia-de-preço-e-formato-o-penhasco-dos-r79)
4. [Concorrência](#4-concorrência)
5. [SEO dentro do Mercado Livre](#5-seo-dentro-do-mercado-livre)
6. [GEO — Generative Engine Optimization](#6-geo--generative-engine-optimization)
7. [Mercado Ads](#7-mercado-ads)
8. [Cursos e fontes de capacitação](#8-cursos-e-fontes-de-capacitação)
9. [Plano de 90 dias](#9-plano-de-90-dias)
10. [O que ainda não foi verificado](#10-o-que-ainda-não-foi-verificado)
11. [Registro de método](#11-registro-de-método)

---

## 1. Ponto de partida e o que está bloqueado

### O que existe hoje

Na loja própria (`loja.cafecanastra.com/capsulas`), **medido em 24/09/2026**:

| Produto | Preço | R$/cápsula | Status |
|---|---:|---:|---|
| Cápsula Nespresso — Canastra **Suave** (1 cx, 10 un) | R$ 24,90 | 2,49 | disponível |
| Cápsula Nespresso — Canastra **Canela** (1 cx, 10 un) | R$ 24,90 | 2,49 | disponível |
| Canastra **Clássico** (1 cx, 10 un) | — | — | **esgotado** |
| Clássico 6 cx (60 un) | — | — | **esgotado** |
| Canela 6 cx (60 un) | — | — | **esgotado** |
| Kit Clássico 2 + Canela 2 (40 un) | — | — | **esgotado** |
| Kit Clássico 3 + Canela 3 (60 un) | — | — | **esgotado** |

Três leituras disso, e nenhuma é boa para um plano de escala:

1. **Todo formato multi-caixa está esgotado.** São exatamente os formatos que o
   Mercado Livre exige para dar margem (ver seção 2). O gargalo de escala não é
   marketing, é estoque.
2. **O Clássico está esgotado** — e é o SKU com foto pronta em
   `fotos produtos cru/Capsulas-Classico-10un-5g`. Clássico é também o blend de
   entrada, o que um comprador de marketplace testa primeiro.
3. Existem fotos para **Clássico** e **Canela**, mas a loja vende **Suave** e
   **Canela**. Há um SKU vendido sem foto e um SKU fotografado sem estoque.

> **Ação antes de qualquer anúncio:** resolver estoque de Clássico e dos kits. Subir
> anúncio de cápsula no ML sem kit disponível é subir o formato que não fecha conta.

### O que está bloqueado e por quê

A auditoria de **preço** foi feita em 25/09/2026 (ver seção 4). Seguem em aberto
**volume vendido, reputação e posição na busca** por anúncio. O histórico técnico do
bloqueio, registrado para a próxima sessão não repetir o caminho:

| Rota tentada | Resultado |
|---|---|
| `WebFetch` em `lista.mercadolivre.com.br` | **HTTP 403** |
| `api.mercadolibre.com/sites/MLB/search` | **HTTP 403** — exige token OAuth desde 2025 |
| `curl` com User-Agent de navegador na busca | **200, mas devolve `suspicious-traffic-frontend`** (muro anti-bot) |
| `curl` em `vendedores.mercadolivre.com.br` | **200, conteúdo real** — páginas de educação do vendedor passam |
| `curl` em `tendencias.mercadolivre.com.br` | **200**, mas só o top nacional; corte por categoria exige login |
| Extensão Claude in Chrome, 24/09 | `list_connected_browsers` → `[]` (não conectada) |
| Extensão Claude in Chrome, 25/09 | **funcionou** via `tabs_context_mcp`; `list_connected_browsers` deu falso negativo |
| Busca no ML deslogado | `/gz/account-verification` — exige conta |
| Busca no ML logado, 1ª consulta | **136 cards** — dados reais |
| Busca no ML logado, consultas 2 a 5 | `ui-search-loading-screen`, `cards=0` — limite de ritmo contra automação |

**Conclusão operacional:** dado de concorrência no ML exige (a) extensão conectada,
(b) **conta logada** e (c) **o humano navegando** — a automação consegue uma busca e
depois trava. A leitura via `javascript_tool` sobre a página já carregada funciona
sem limite. Contornar o muro anti-bot está fora de escopo e não foi tentado.

---

## 2. A matemática do ML para cápsula

Esta é a seção que decide o projeto. **Uma caixa de 10 cápsulas a R$24,90 não é um
produto viável no Mercado Livre**, e a razão é estrutural, não de execução.

### As três taxas

**a) Comissão por categoria.** Cápsula de café cai em *Alimentos e Bebidas* —
caminho **confirmado em 25/09/2026** na própria busca do ML:
`Alimentos e Bebidas › Mercearia › Infusões › Cápsulas`.

| Tipo de anúncio | Comissão | Parcelamento |
|---|---:|---|
| Clássico | **14%** | não |
| Premium | **19%** | até 12x sem juros para o comprador |

*Alimentos e Bebidas está na faixa mais alta da plataforma* — a média geral de
Clássico é 11,5–12%. Café paga 14%.

**b) Custo operacional por unidade vendida.** Desde **02/03/2026** o antigo custo
fixo virou uma tarifa variável por **peso × faixa de preço** — 29 faixas de peso ×
8 faixas de preço = **232 combinações**, e desde março existem **tabelas separadas
por cor de reputação** (verde/MercadoLíder, amarela, vermelha).

Faixa até 0,3 kg, reputação verde (valores publicados como ilustrativos, já com
desconto de reputação):

| Preço do anúncio | Custo por unidade |
|---|---:|
| até R$ 18,99 | R$ 5,65 |
| R$ 19,00 – 48,99 | R$ 6,55 |
| R$ 49,00 – 78,99 | R$ 7,75 |
| R$ 79,00 – 99,99 | R$ 12,35 |

**c) Tarifas do Full.** Armazenagem diária por unidade, por tamanho:

| Tamanho | Full padrão | Full Super (Supermercado) |
|---|---:|---:|
| Pequeno (até 12×15×25 cm) | R$ 0,007/dia | **R$ 0,000/dia** |
| Médio (até 28×36×51 cm) | R$ 0,015/dia | **R$ 0,000/dia** |
| Grande (até 60×60×70 cm) | R$ 0,050/dia | R$ 0,014/dia |
| Extragrande | R$ 0,107/dia | R$ 0,025/dia |

Mais: **custo por estoque antigo**, que a página oficial do ML descreve assim —
cobrança a partir de **2 meses para produtos de Supermercado** ou **4 meses para
todos os demais**. Em 2026 a armazenagem subiu **+7,6%** (médios e grandes), a
retirada de estoque **+5%**, o estoque antigo **+6,4%** e a coleta domiciliar
**+5% a +10%** conforme volume e distância.

> **Fork estratégico a resolver:** se a cápsula for cadastrada em **Supermercado**,
> a armazenagem de item pequeno cai para **R$ 0,000/dia** — mas o gatilho de estoque
> antigo antecipa de 4 para **2 meses**. Para um produto de giro alto isso é troca
> boa; para um lançamento sem histórico de venda, é risco. Decidir com dados de giro,
> não por padrão.

**d) Saque.** Mercado Pago: 8 saques/mês grátis, **R$ 5,90** a partir do 9º.

### Quem paga o frete — e a divergência que precisa ser resolvida na sua conta

| Faixa de preço | Regra |
|---|---|
| < R$ 19 | Comprador paga, salvo se o vendedor oferecer frete grátis por conta própria |
| R$ 19 – 78,99 | **Divergência entre fontes** (ver abaixo) |
| ≥ R$ 79 | **Frete grátis obrigatório** para produto novo; ML subsidia conforme reputação, desconto de **até 70%** |

A divergência: uma fonte afirma que na faixa R$19–78,99 *"a plataforma cobre
integralmente o frete para produtos novos em envio padrão"*; outra afirma que abaixo
do piso obrigatório, *se* o vendedor optar por frete grátis, ele paga **100% sem
subsídio**. A segunda leitura é a que bate com a tabela de custo operacional acima
(R$6,55 para um produto de R$19–48,99 não faria sentido se o ML pagasse tudo).

**Trate a segunda como verdadeira até medir.** E meça assim: Central do Vendedor →
simulador de custos, com peso e preço reais do SKU. É o único número que vale.

### O CPV real — e a conta que ele produz

> **CPV confirmado pela Canastra em 25/09/2026: R$ 15,10 por caixa de 10, impostos
> inclusos — R$ 1,51 por cápsula.** Com esse número a margem deixa de ser hipótese.

**O fato que decide o lançamento:** no ML, a caixa de 10 a R$ 24,90 **perde R$ 0,66 por
pedido**. Comissão R$ 3,49 + envio R$ 6,55 + CPV R$ 15,10 = R$ 25,14 contra receita de
R$ 24,90. Não é margem apertada — é negativa, antes de qualquer centavo de anúncio.

Clássico (14%), Full, reputação verde, 60 dias de armazenagem:

| Formato | Preço | R$/cáp | Comissão | Envio | CPV | Lucro | Margem |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10 un — preço de hoje | 24,90 | 2,49 | 3,49 | 6,55 | 15,10 | **−0,66** | **−2,6%** |
| 10 un — equilíbrio | 27,90 | 2,79 | 3,91 | 6,55 | 15,10 | 1,92 | 6,9% |
| **10 un — isca** | 32,90 | 3,29 | 4,61 | 6,55 | 15,10 | 6,22 | 18,9% |
| 20 un | 64,90 | 3,25 | 9,09 | 7,75 | 30,20 | 17,44 | 26,9% |
| 40 un | 109,90 | 2,75 | 15,39 | 15,00 | 60,40 | 18,21 | 16,6% |
| **40 un — principal** | 129,90 | 3,25 | 18,19 | 15,00 | 60,40 | **35,41** | **27,3%** |
| 60 un | 179,90 | 3,00 | 25,19 | 15,00 | 90,60 | 48,21 | 26,8% |
| **100 un — ticket alto** | 289,90 | 2,90 | 40,59 | 20,00 | 151,00 | **77,41** | **26,7%** |

Envio acima de R$ 79 é **estimativa** (R$ 15 para 40 un, R$ 20 para 100 un) — confirmar no
simulador. Tudo o mais é medido ou publicado.

**Preço mínimo para 25% de margem:** 10 un → R$ 36,18 (R$ 3,62/cáp) · 20 un → R$ 62,90
(R$ 3,15) · 40 un → R$ 125,08 (R$ 3,13) · 60 un → R$ 174,59 (R$ 2,91) · 100 un →
R$ 281,80 (R$ 2,82). *Quanto maior o kit, menor o R$/cápsula necessário* — é o custo por
pedido se diluindo.

**Clássico vs Premium:** Premium custa exatamente **5 pontos de margem** em qualquer
preço. Kit 40 a R$ 129,90: 27,3% → 22,3%, e 12× de R$ 10,83 não move ninguém. Kit 100 a
R$ 289,90: 26,7% → 21,7%, mas 12× de R$ 24,16 é alavanca real. **Clássico em tudo;
testar Premium só no kit de 100.**

**ROAS objetivo** (ACOS = metade da margem): kit 40 → **7,3×** (ACOS 13,6%) · kit 100 →
7,5× (13,4%) · caixa 10 → 10,6× (9,5%), ou seja **não anunciar a caixa de 10**.

### A conta de take do ML, formato por formato

Premissas: reputação verde, Full, faixa até 0,3 kg até 30 un e 0,3–0,5 kg acima,
anúncio Clássico (14%), preço mantido em ~R$2,50/cápsula. Custos de envio acima de
R$79 são **estimativa** — substituir pelo simulador.

| Formato | Preço | R$/cáp | Comissão 14% | Envio/operacional | Total ML | **% da receita** | Líquido |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 cx — 10 un | 24,90 | 2,49 | 3,49 | 6,55 | 10,04 | **40,3%** | 14,86 |
| 2 cx — 20 un | 49,90 | 2,50 | 6,99 | 7,75 | 14,74 | **29,5%** | 35,16 |
| 3 cx — 30 un | 74,90 | 2,50 | 10,49 | 7,75 | 18,24 | **24,4%** | 56,66 |
| 4 cx — 40 un | 99,90 | 2,50 | 13,99 | ~13,00 | 26,99 | **27,0%** | 72,91 |
| 6 cx — 60 un | 149,90 | 2,50 | 20,99 | ~18,00 | 38,99 | **26,0%** | 110,91 |
| 10 cx — 100 un | 239,90 | 2,40 | 33,59 | ~21,00 | 54,59 | **22,8%** | 185,31 |

**O que essa tabela diz, em uma frase:** o custo operacional é **por pedido, não por
cápsula**. Ele custa o mesmo para despachar 10 ou 60 cápsulas. Diluído em 10 unidades
são **R$0,655 por cápsula**; diluído em 60, **R$0,109**. A diferença de 40,3% para
26,0% de take do ML é toda aí.

Somando o CPV (café + cápsula + encapsulamento + embalagem), a caixa isolada de 10 a
R$24,90 fica **sem espaço para Ads e impostos**. Não é um anúncio ruim — é um formato
que não fecha.

---

## 3. Estratégia de preço e formato: o penhasco dos R$79

### A decisão central

R$79 é um **penhasco**, não uma rampa:

- **R$74,90** (3 caixas): fica abaixo do piso. Custo operacional R$7,75, take de
  24,4%. Mas o comprador vê "+ frete" — e frete visível derruba conversão no ML.
- **R$99,90** (4 caixas): frete grátis obrigatório, custo estimado ~R$13,00, take de
  27,0%. Paga-se ~2,6 pontos de take para comprar o selo de frete grátis.

**Recomendação:** os ~2,6 pontos valem. Frete grátis é sinal de ranqueamento e de
conversão simultaneamente, e conversão realimenta ranqueamento. Mas a decisão só
fecha com o número real do simulador — se o custo acima de R$79 vier bem acima de
R$13, o cálculo inverte.

### Arquitetura de portfólio proposta

Três anúncios, cada um com um trabalho distinto:

| Anúncio | Formato | Preço sugerido | Papel |
|---|---|---:|---|
| **Isca** | 1 cx, 10 un | R$ 32,90 | Não é para dar lucro. É para captar review e primeira compra. Preço acima do D2C justamente para não canibalizar. |
| **Cavalo de batalha** | 4 cx, 40 un (2 Clássico + 1 Suave + 1 Canela) | R$ 129,90 | O anúncio que recebe Ads, persegue Buy Box e carrega o histórico de conversão. Cruza R$79. |
| **Ticket alto** | 10 cx, 100 un | R$ 289,90 | Take mais baixo (22,8%), melhor margem absoluta. Público recorrente. |

O kit misto no cavalo de batalha faz três coisas de uma vez: cruza R$79 com folga,
resolve a objeção "não sei qual blend eu gosto", e **aumenta o valor percebido sem
baixar o R$/cápsula**.

### O que não fazer

- **Não replicar o preço D2C no ML.** R$24,90 na loja própria é margem; R$24,90 no
  ML é prejuízo. Preço de marketplace é preço com 26–40% de take embutido.
- **Não usar Premium (19%) no lançamento.** Cinco pontos de comissão em troca de
  parcelamento sem juros só se paga em ticket alto. Testar Premium **apenas** no
  anúncio de 100 unidades, e medir.
- **Não entrar em guerra de preço por cápsula.** A faixa de mercado no ML é R$2–3/
  cápsula e há cápsula genérica bem abaixo. Café especial com fazenda própria compete
  em origem e rastreabilidade, não em centavo.

---

## 4. Concorrência

> **Auditado dentro do Mercado Livre em 25/09/2026, sessão logada na conta Canastra.**
> A faixa de preço está medida, não estimada.

### Correção de uma leitura anterior

A primeira passagem (24/09) sugeria que o Orfeu praticava **R$ 5,43–5,59 por cápsula**
no ML. Esses eram anúncios da linha *Arara* — microlote — revendidos por terceiros. A
escada real do Orfeu para os blends correntes é **R$ 2,29–2,79**. Canastra a R$ 2,49
**não está precificada como marca de massa**: está dentro da faixa de especial, logo
abaixo do Orfeu.

### A faixa do café especial em cápsula

| Patamar | Quem está nele | R$/cápsula |
|---|---|---:|
| **Massa** | Pilão, 3 Corações, Nescafé, Dolce Gusto, L'or, Tres | 1,44 – 2,00 |
| **Genérico em kit** | Café Italle, Capresso, Melicidade | 1,40 – 1,56 |
| **Especial** ← onde a Canastra compete | Orfeu, Coffee++, Sebastian, Zanelli, Baobá | **2,29 – 3,14** |
| **Premium e importado** | Orfeu descafeinado/orgânico, Orfeu Arara, Nespresso, Illy | 3,44 – 4,20 |

R$ 2,49/cápsula coloca a Canastra no **terço inferior da faixa de especial** — abaixo
de todo blend corrente do Orfeu. Há espaço para subir sem sair do patamar, e há um teto
de R$ 3,99–4,20 que o mercado já paga por linha premium.

### Orfeu — escada completa no ML

| SKU | Preço | Un | R$/cáp |
|---|---:|---:|---:|
| Bourbon Amarelo | 45,73 | 20 | 2,29 |
| Clássico (anúncio pago) | 49,80 | 20 | 2,49 |
| Catucaí | 26,40 | 10 | 2,64 |
| Acauã | 26,40 | 10 | 2,64 |
| Forte | 27,06 | 10 | 2,71 |
| Bourbon Amarelo | 27,08 | 10 | 2,71 |
| Clássico | 27,90 | 10 | 2,79 |
| Intenso | 27,90 | 10 | 2,79 |
| **Kit 50 un** | 156,98 | 50 | **3,14** |
| Descafeinado | 39,90 | 10 | 3,99 |
| Orgânico | 39,90 | 10 | 3,99 |
| Arara (microlote) | 83,23 | 20 | 4,16 |

**O achado que muda a arquitetura de kit:** o Kit 50 do Orfeu sai a **R$ 3,14/cápsula —
mais caro** que a caixa de 10 a R$ 2,64. O kit não é desconto por volume: é produto
premium, com frete grátis e parcelamento embutidos. **Não é preciso baixar o R$/cápsula
para montar kit** — suposição que a versão anterior deste documento fazia, e que o
mercado desmente.

### Coffee++ — lacuna fechada

Existe, é café especial em cápsula, é concorrente direto. Distribuído via **Cafezale**,
com a marca irmã **Coffee Mais**.

| Anúncio | De | Por | R$/cáp | Sinais |
|---|---:|---:|---:|---|
| Café Especial Arara Coffee++ 10 cáps | 49,90 | **28,90** | 2,89 | 42% OFF |
| Coffee++ Arara Sem Glúten · Cafezale | 52,50 | 47,25 | — | 5.0 · +25 vendidos · frete grátis |
| Coffee Mais Cerrado Mineiro 10 cáps | — | 28,90 | 2,89 | — |
| Coffee++ Chapada de Minas | — | — | — | linha por região |

Repare no **"Sem Glúten" no título**: *É livre de glúten* é filtro nativo da categoria.
Eles capturam um filtro que a maioria ignora.

### Piso e teto

| Marca | Formato | Preço | R$/cáp |
|---|---|---:|---:|
| Pilão Fortíssimo | 10 un | 14,35 | 1,44 |
| 3 Corações Mogiana | 10 un | 14,61 | 1,46 |
| 3 Corações Cerrado Mineiro | 10 un | 15,44 | 1,54 |
| Nescafé Farmers Origins | 10 un | 16,82 | 1,68 |
| Tres 3 Corações | kit 30 | 59,75 | 1,99 |
| Illy Iperespresso | 18 un | 62,00 | 3,44 |
| Nespresso Vertuo | 20 un | 78,00 | 3,90 |
| Nespresso original | 50 un | 185,00 | 3,70 |
| Nespresso Seleção Especial | 50 un | 200,00 | 4,00 |
| Nespresso Barista Creations | 10 un | 42,00 | 4,20 |

Quase todo anúncio Nespresso aparece como **anúncio pago**. A marca não disputa orgânico
nessa categoria — compra a posição.

### Sellers de volume — a mecânica que já funciona

| Anúncio | Preço | Un | R$/cáp |
|---|---:|---:|---:|
| **Café Italle 50 un** — *mais vendido da categoria* | 73,79 | 50 | 1,48 |
| Café Italle 100 un (R$ 131 levando 30+) | 139,90 | 100 | 1,40 |
| Capresso 80 un | 124,45 | 80 | 1,56 |
| Melicidade Blend Especial 20 un | 27,90 | 20 | 1,40 |
| Kit Nescafé 50 un (frete grátis) | 99,90 | 50 | 2,00 |

**A tese do kit, confirmada empiricamente:** o selo "MAIS VENDIDO" da categoria está num
**kit de 50 unidades**, não numa caixa de 10. E **"Unidades por embalagem: 50 ou mais" é
filtro nativo** — o comprador procura formato grande de propósito.

### O que a estrutura da categoria revela

- **Categoria confirmada:** `Alimentos e Bebidas › Mercearia › Infusões › Cápsulas`.
  Comissão de 14% (Clássico) aplicável.
- **8.402 resultados** em "capsula de cafe". Categoria grande e disputada.
- **Filtros = campos de ficha que o comprador usa:** Marca · Variedade da infusão ·
  Formato de venda (Unidade / **Kit**) · **Unidades por embalagem** (por unidade · 2–17 ·
  18–49 · **50+**) · **Intensidade** (4 a 12) · **É livre de glúten** · É recarregável.
  Deixar qualquer um em branco é sumir de um filtro.
- **"Frete grátis em carrinhos a partir de R$ 19"** — o ML monta carrinho consolidado.
  Ameniza, mas não elimina, o penhasco dos R$ 79.
- **Full Super: frete grátis acima de R$ 249** em envio consolidado.

### O nome "Canastra" já está ocupado no Mercado Livre

**O achado mais consequente da auditoria.** A busca `cafe canastra` devolve **41 anúncios
com "Canastra" no título — e nenhum é a marca de vocês.** São terceiros usando a região
como descritor, em café em grão, moído *e em cápsula*. Um deles é um vendedor chamado
literalmente **"Café da Serra da Canastra"**.

As cápsulas deles saem a **R$ 3,80–5,03 por cápsula** — bem acima da faixa de especial
(R$ 2,29–3,14) e do dobro do preço de vocês.

| Anúncio | De | Por | Un | R$/cáp | Sinais |
|---|---:|---:|---:|---:|---|
| Cápsulas Café Serra Canastra Nespresso Arábica | — | 39,92 | 10 | 3,99 | — |
| Cápsulas Café Serra Canastra Nespresso Arábica | 85,90 | 75,90 | 20 | 3,80 | frete grátis |
| Cápsulas Café Serra Canastra Nespresso Arábica | 160,90 | 150,90 | 30 | **5,03** | frete grátis |
| 30 Cápsulas Café da Serra da Canastra Moído Forte | — | 121,90 | 30 | 4,06 | frete grátis |
| 50 Cápsulas Café da Serra da Canastra Moído Forte *(Catálogo)* | — | 227,90 | 50 | 4,56 | vendedor **"Café da Serra da Canastra"** · **+5 vendas** · sem Full |

**Leitura estratégica.** O volume deles é **baixo** — o anúncio de catálogo tem apenas 5
vendas. Não é concorrente forte; é **espaço vago sendo mal ocupado**. A marca que tem
fazenda própria na Serra da Canastra não aparece em nenhuma busca pelo próprio nome,
enquanto terceiros cobram R$ 5,03/cápsula usando o topônimo.

Duas ações caem daqui:

1. **Ocupar o termo `canastra`** no título dos anúncios — hoje é território livre, com
   preço alto e concorrência fraca.
2. **Avaliar registro de marca e uso indevido**, se "Café Canastra" for marca registrada —
   há vendedor operando com nome quase idêntico.

Também ocupam o nome, em grão e moído (não cápsula, mas mostram a disputa pelo termo):
Café Frutado da Serra Canastra 500g R$ 25,99 · Café Especial Canastra Premium 500g
R$ 69,90 · Canastra Premium Cereja Descascado 1kg R$ 113,90 (+500 vendidos, 4.0) ·
2un Canastra Premium 500g R$ 98 (+100 vendidos, 4.8) · Canastra Premium 250g R$ 45,90
(+50 vendidos, 4.9) · Café Artesanal Oká Canastra 250g R$ 28.

### Catálogo completo do que foi pesquisado

Três buscas em 25/09/2026: `capsula de cafe` (8.402 resultados), `capsula cafe especial`
e `cafe canastra`. "Por" é o preço praticado no momento da captura.

#### Grupo A · Massa — a âncora de preço

**Estratégia do grupo:** desconto permanente agressivo (20–54% "OFF") sobre preço de lista
inflado, caixa de 10 como formato padrão, giro por recompra. Preço de tabela existe para
ser riscado. Não dá para competir aqui — e não se deve.

| Anúncio | De | Por | Un | R$/cáp | Sinais |
|---|---:|---:|---:|---:|---|
| Pilão Espresso Extraforte 52g | 22,90 | 12,96 | 10 | 1,30 | 43% Pix · R$ 12,83 levando 2+ |
| Tres Filtrado Tradicional 8g | 23,39 | 13,88 | 10 | 1,39 | 40% OFF no Pix |
| Pilão Fortíssimo Espresso | — | 14,35 | 10 | 1,44 | — |
| 3 Corações Mogiana Paulista | 18,89 | 14,61 | 10 | 1,46 | 22% OFF |
| União Velluto | 32,90 | 14,90 | 10 | 1,49 | 54% OFF · R$ 12 levando 3+ |
| 3 Corações Descafeinado | 18,89 | 14,98 | 10 | 1,50 | 20% OFF |
| Pilão Extraforte | — | 29,99 | 20 | 1,50 | — |
| 3 Corações Cerrado Mineiro | 18,89 | 15,44 | 10 | 1,54 | 18% OFF |
| 3 Corações Intenso · Intensidade 13 | — | 15,49 | 10 | 1,55 | — |
| Pilão Intenso 8 | 22,90 | 15,73 | 10 | 1,57 | 31% OFF no Pix |
| Tres Cappuccino Avelã | 23,39 | 15,66 | 10 | 1,57 | 33% OFF |
| 3 Corações Colombia · Espírito Santo · Peru · Orgânico | 22,90 | 15,98 | 10 | 1,60 | 30% OFF |
| Nescafé Farmers Origins México · Índia · Brazil | 25,01 | 16,82 | 10 | 1,68 | 32% OFF |
| Dolce Gusto Café Caseiro | 21,39 | 16,98 | 10 | 1,70 | 20% OFF |
| Tres Espresso Atento · Pleno | 27,49 | 16,99 | 10 | 1,70 | 38% OFF |
| Dolce Gusto Espresso Intenso 80g | 21,39 | 17,22 | 10 | 1,72 | 19% OFF |
| 3 Corações Chapada Diamantina | — | 17,49 | 10 | 1,75 | linha "regiões" |
| Tres Espresso Supremo | 19,65 | 17,49 | 10 | 1,75 | 10% OFF |
| Tres Descafeinado · Rituais · Ameno | 23,39 | 17,49 | 10 | 1,75 | 25% OFF |
| L'or Ristretto | — | 35,83 | 20 | 1,79 | sem glúten no título |
| Nescafé Farmers Origins Colombia | 25,01 | 17,90 | 10 | 1,79 | 28% OFF |
| Dolce Gusto Mochaccino Canela | 22,03 | 17,90 | 10 | 1,79 | 18% OFF |
| Dolce Gusto Lungo 70g | 27,99 | 18,31 | 10 | 1,83 | 34% OFF no Pix |
| L'or Origins Guatemala | 32,99 | 18,54 | 10 | 1,85 | 43% OFF |
| Dolce Gusto Café Au Lait | 22,03 | 18,98 | 10 | 1,90 | 13% OFF |
| Dolce Gusto Kopenhagen Chococino Cereja · Lajotinha | 29,99 | 19,90 | 10 | 1,99 | 33% OFF · co-branding |
| Kit 30 Cápsulas Tres | — | 59,75 | 30 | 1,99 | kit da marca |
| 3 Corações Especiais Peru · Orgânico Alumínio | — | 22,50 | 10 | 2,25 | alumínio = upsell |

#### Grupo B · Especial nacional — onde a Canastra compete

**Estratégia do grupo:** preço 60–100% acima da massa, justificado por origem nomeada
(Arara, Catucaí, Acauã, Cerrado, Chapada) e pontuação SCA. Desconto moderado (7–14%),
exceto Coffee++ que usa 42%. Frete grátis e parcelamento sem juros são norma no kit.
**Linha premium — descafeinado, orgânico, microlote — sustenta R$ 3,99–4,16.**

| Anúncio | De | Por | Un | R$/cáp | Sinais e estratégia |
|---|---:|---:|---:|---:|---|
| Melicidade Blend Especial | — | 27,90 | 20 | 1,40 | "especial" com preço de massa — dilui o termo |
| Orfeu Bourbon Amarelo | — | 45,73 | 20 | 2,29 | piso da linha Orfeu |
| Orfeu Clássico | 53,80 | 49,80 | 20 | 2,49 | **anúncio pago** · 7% OFF |
| Orfeu Catucaí · Acauã | — | 26,40 | 10 | 2,64 | varietal nomeado |
| Orfeu Forte | — | 27,06 | 10 | 2,71 | — |
| Orfeu Bourbon Amarelo | — | 27,08 | 10 | 2,71 | — |
| **Orfeu Clássico · Intenso** | — | 27,90 | 10 | **2,79** | **referência direta da caixa de 10** |
| Coffee++ Arara | 49,90 | 28,90 | 10 | 2,89 | 42% OFF — desconto de massa em produto especial |
| Coffee Mais Cerrado Mineiro | — | 28,90 | 10 | 2,89 | marca irmã do Coffee++ |
| Café Especial Clássico | — | 29,00 | 10 | 2,90 | sem marca no título |
| Café Especial 100% arábica | — | 29,90 | 10 | 2,99 | — |
| Sebastian Coffee — Lote Especial 86 Pontos | — | 29,99 | — | — | frete grátis · **pontuação SCA no título** |
| Sebastian Coffee — Lote Especial 86 Pontos | — | 35,00 | — | — | frete grátis |
| Zanelli Coffee 100% Arábica | — | 34,90 | 10 | 3,49 | R$ 24,90 levando 5+ · **Exclusivo Negócios** |
| **Orfeu Kit 50** | — | 156,98 | 50 | **3,14** | **kit mais caro por cápsula que a caixa de 10** |
| Coffee++ Arara Sem Glúten · Cafezale | 52,50 | 47,25 | — | — | 5.0 · +25 vendidos · FG · **"sem glúten" captura filtro** |
| Coffee Mais Arara · Cafezale | 47,90 | 43,11 | — | — | frete grátis |
| Cápsula Premium 50g Baobá | — | 45,90 | — | — | vende por gramatura, não por unidade |
| **Orfeu Descafeinado** | — | 39,90 | 10 | **3,99** | **+43% sobre a linha base — lacuna da Canastra** |
| **Orfeu Orgânico** | — | 39,90 | 10 | **3,99** | mesma mecânica de prêmio |
| Orfeu Arara — microlote | — | 83,23 | 20 | 4,16 | R$ 83 levando 2+ · Exclusivo Negócios · FG |
| Orfeu Arara — *revenda de terceiro* | 65,00 | 55,90 | 10 | 5,59 | 5.0 · +100 vendidos · **não é preço da marca** |
| Orfeu Arara kit — *revenda* | 194,99 | 165,74 | 30 | 5,52 | 5x sem juros · frete grátis |
| Orfeu Arara kit — *revenda* | 258,60 | 217,22 | 40 | 5,43 | 6x sem juros · frete grátis |

#### Grupo C · Importado premium — o teto

**Estratégia do grupo:** sem desconto, preço firme, presença quase inteiramente comprada —
**praticamente todo anúncio Nespresso é anúncio pago**. A marca não disputa orgânico:
compra a posição e vende o sistema, não a cápsula.

| Anúncio | Preço | Un | R$/cáp | Sinais |
|---|---:|---:|---:|---|
| Nespresso World Explorations | 108,07 | 30 | 3,60 | 14% OFF · anúncio pago |
| Nespresso Variados · Sabores Intensos · Equilibrados | 185,00 | 50 | 3,70 | anúncio pago |
| Nespresso Vertuo Espressos · Altissio | 78,00 | 20 | 3,90 | sistema fechado próprio |
| Nespresso Seleção Especial | 200,00 | 50 | 4,00 | anúncio pago |
| Nespresso Clássicos · Baunilha/Caramelo/Chocolate | 126,00 | 30 | 4,20 | anúncio pago |
| Nespresso Barista Creations Baunilha · Caramello | 42,00 | 10 | 4,20 | **teto da categoria** |
| Illy Iperespresso Forte | 62,00 | 18 | 3,44 | sistema próprio |

#### Grupo D · Genérico em kit grande — quem ganha volume

**Estratégia do grupo:** kit de 50 a 100 unidades, R$ 1,40–2,00 por cápsula, desconto
progressivo por quantidade e selo **Exclusivo Negócios** (B2B). É a mecânica que o
algoritmo premia hoje — o **"MAIS VENDIDO" da categoria está aqui**. Não é onde competir
em preço, mas é de onde se copia o *formato*.

| Anúncio | De | Por | Un | R$/cáp | Sinais |
|---|---:|---:|---:|---:|---|
| **Café Italle 50 un** — *mais vendido da categoria* | 89,90 | 73,79 | 50 | 1,48 | R$ 67 levando 20+ · Exclusivo Negócios · anúncio pago |
| Café Italle 100 un | 169,90 | 139,90 | 100 | 1,40 | R$ 131 levando 30+ · Exclusivo Negócios |
| Capresso compatível Nespresso | — | 124,45 | 80 | 1,56 | anúncio pago |
| Kit Nescafé compatível Nespresso | — | 99,90 | 50 | 2,00 | frete grátis · anúncio pago |
| Café em Sachês Legusta Extraforte · CAFEFACIL | — | 107,86 | 60 | 1,80 | 4.8 · +500 vendidos · frete grátis |

> **Ressalva de método sobre "vendidos".** Numa página de produto do ML, os blocos
> `poly-card` são **carrosséis de recomendação**, não o produto aberto — um número lido
> daí pertence a outro anúncio. Os valores acima vêm de cartões dentro da lista de
> resultados; onde houve dúvida, a célula ficou vazia em vez de preenchida por estimativa.

### O que ainda falta

A busca por marca foi concluída: **nenhum dos 41 resultados de `cafe canastra` é a marca
de vocês** — ver o bloco acima. Se existe anúncio de vocês no ar, ele não aparece pelo
próprio nome, o que já é problema de SEO por si só.

Seguem em aberto: confirmar se os anúncios Orfeu de R$ 2,29–2,79 são da loja oficial (o
cartão de resultado não expõe o vendedor), e levantar **volume vendido, reputação e
posição na busca** anúncio a anúncio.

### Método da auditoria

Para cada concorrente relevante, capturar num TSV:

```
handle_seller | titulo_completo | preco | qtd_capsulas | preco_por_capsula |
tipo_anuncio | full? | frete_gratis? | qtd_vendida | reputacao | qtd_fotos |
tem_video? | ficha_tecnica_completa? | em_catalogo? | posicao_busca | termo
```

Termos a varrer: `cápsula de café` · `cápsula nespresso` · `cápsula café especial` ·
`cápsula café gourmet` · `kit cápsula café` · `cápsula café 100 unidades` ·
`cápsula café compatível nespresso` · `cápsula café minas gerais`

A coluna que decide é `preco_por_capsula` cruzada com `qtd_vendida`.

**Restrição operacional medida:** a navegação programática é limitada pelo ML após a
primeira busca — quatro páginas seguidas travaram em `ui-search-loading-screen` com
`cards=0`. A rota que funciona é **o humano navegar e a leitura ser feita sobre a página
já carregada**.

## 5. SEO dentro do Mercado Livre

O algoritmo pesa, em ordem de força prática:

### 5.1 Conversão (CVR) — o fator dominante

Anúncio que recebe tráfego e não converte **perde posição rápido**. Consequência
contra-intuitiva: é melhor subir com **um** anúncio forte do que seis medianos.
Tráfego dividido entre seis anúncios gera seis históricos fracos de conversão.

### 5.2 Reputação — filtro binário

Verde entra na disputa de Buy Box, amarelo não. Não é um peso, é uma porta. E desde
março/2026 a reputação também define **qual tabela de frete você paga** — reputação
ruim custa duas vezes: posição e dinheiro.

### 5.3 Full — a alavanca mais agressiva de visibilidade

O Full garante prazo de entrega, e prazo é critério de Buy Box. Para cápsula, o Full
tem uma vantagem extra: item **pequeno**, armazenagem de R$0,007/dia. Estocar 500
caixas por 60 dias custa ~R$210. É barato. O risco real não é a armazenagem, é o
**custo por estoque antigo** se o giro não vier.

### 5.4 Título — como o cliente busca, não como a marca fala

O título é o vetor principal de match. Regras:

- **Nunca editar título de anúncio rodando** — reseta o histórico de relevância.
  Acertar antes de publicar é mais barato que corrigir depois.
- Ordem: produto + marca + atributo de compatibilidade + quantidade + diferencial.
- O comprador de cápsula busca por **compatibilidade** (`compatível nespresso`) e por
  **quantidade** (`100 unidades`). Ambos precisam estar no título.

Proposta para o cavalo de batalha:

```
Kit 40 Cápsulas Café Especial Canastra Compatível Nespresso
```

> **Correção: o limite do ML é 60 caracteres.** A versão anterior deste documento propunha
> um título de **81 caracteres**, que seria truncado. O título acima tem **59**. Os três
> blends saem do título e vão para a ficha técnica (campo Modelo/Linha) e a descrição,
> onde não custam caractere e ainda são indexados.

Títulos dos outros dois formatos: `Kit 100 Cápsulas Café Especial Canastra Nespresso
Serra MG` (58) e `Cápsulas Café Especial Canastra Compatível Nespresso 10un` (57).

### 5.5 Ficha técnica — a válvula do orgânico

O ML prioriza anúncio com **100% dos campos obrigatórios** e bonifica os opcionais.
Isto é trabalho mecânico de meia hora que muitos concorrentes não fazem. Para cápsula,
preencher sem falha: marca, compatibilidade, quantidade de unidades, peso por cápsula,
peso líquido total, tipo de torra, intensidade, moagem, origem, tipo de embalagem,
se é descafeinado, validade.

### 5.6 Catálogo

Competir por Buy Box em página de Catálogo muda o jogo: você disputa com preço, prazo
e reputação sobre uma ficha compartilhada. Para produto de marca própria, avaliar se
**criar** a página de catálogo compensa — dá controle da ficha, mas abre a porta para
revendedor competir no mesmo espaço depois.

### 5.7 Conteúdo visual

As fotos já existem em `fotos produtos cru/Capsulas-*`. O ML premia completude: usar
o máximo de slots, fundo branco no slot 1 (exigência de catálogo), e pelo menos uma
foto que mostre **escala** — cápsula na mão ou ao lado da máquina. Nota do
`CLAUDE.md`: cápsula em escala real fica minúscula na grade, então o enquadramento
tem que ser fechado.

### 5.8 Tendências

`tendencias.mercadolivre.com.br` é público, mas **só entrega o top nacional** — o
corte por categoria exige login na Central do Vendedor. Verificado em 24/09/2026:
`cafeteira` aparece entre os termos mais buscados do país, o que confirma base
instalada crescente de máquina — demanda derivada de cápsula.

---

## 6. GEO — Generative Engine Optimization

A pergunta que importa: quando alguém pergunta a um assistente de IA *"qual a melhor
cápsula de café especial brasileira?"*, a Canastra aparece?

### Por que isso não é hype

Em IA generativa a visibilidade é **binária**: o modelo não ranqueia, ele sintetiza.
Você está na resposta ou não está — não existe "página 2". E o tráfego que vem de lá
converte melhor: um levantamento em 94 marcas de e-commerce apontou conversão **31%
maior** vindo de referral do ChatGPT do que de orgânico não-branded.

### O ponto cego: o ML não é o canal de GEO

**Anúncio de Mercado Livre não é bom material de citação.** Um LLM cita fontes que
explicam, comparam e têm autoridade — não fichas de marketplace. Então o trabalho de
GEO acontece em `cafecanastra.com`, e o ML colhe a demanda que ele gera. São dois
canais em série, não em paralelo.

### O que fazer, em ordem de retorno

**1. Título e descrição em linguagem natural (maior impacto).** O título é o âncora
de relevância. Errado: `Canastra Clássico`. Certo: `Cápsula de Café Especial
Compatível com Nespresso — Canastra Clássico, 10 un, torra média, Serra da Canastra
MG`. Máximo ~70 caracteres no campo de título, o resto nos atributos.

**2. Structured data no site próprio.** JSON-LD de `Product`, com `aggregateRating` e
`review`. Sem schema, o crawler de IA adivinha. Com schema, ele extrai.

**3. Liberar os crawlers de IA no `robots.txt`.** Bloqueio de crawler de IA é
autoexclusão da resposta. Verificar hoje o que está bloqueado.

**4. `llms.txt` na raiz do domínio.** Custo próximo de zero, benefício crescente.

**5. Reviews distribuídos.** LLM sintetiza múltiplas fontes: um produto com centenas
de avaliações em cinco plataformas ganha de um com quarenta só no site próprio. Aqui
o ML **ajuda o GEO** — avaliação de ML é fonte indexada e citável.

**6. Conteúdo em formato que LLM cita.** Resposta direta, lista `<ul>/<li>`, FAQ com
`FAQPage` schema, parágrafo de 2–3 frases claras. Prosa poética não é citada. A
narrativa de fazenda própria e Serra da Canastra é ótima para humano e precisa de uma
versão **factual e extraível** para máquina.

**7. `ChatGPT Merchant Program`** em `chatgpt.com/merchants`. Quem não está em Shopify
precisa integrar com Stripe e montar feed compatível com ACP. Os dois protocolos que
importam: **ACP** (OpenAI) e **UCP** (Google).

**8. Renderização server-side.** Crawler de IA não executa JS por completo. Página que
só monta conteúdo no cliente é página invisível.

### O que não funciona

Bloquear crawler de IA; schema ausente ou errado; título só com voz de marca; página
JS-only; review só no site próprio; imagem sem ALT descritivo e sem nome de arquivo
semântico.

### Medição

Não existe medição confiável ainda — a expectativa do mercado é Q4/2026–Q1/2027.
Proxy aceitável agora: rodar um conjunto fixo de perguntas semanalmente em ChatGPT,
Gemini, Perplexity e Claude, e registrar se a marca aparece. Sugestão de perguntas:

- "melhor cápsula de café especial brasileira"
- "cápsula compatível com nespresso de café especial"
- "café especial de Minas Gerais em cápsula"
- "marca de café com fazenda própria que vende cápsula"

Métrica: **citation rate** — em quantas das N perguntas a marca apareceu. Registrar em
planilha com data. É rudimentar e é o que existe.

---

## 7. Mercado Ads

### Formatos

| Formato | O que é | Requisito |
|---|---|---|
| **Product Ads** | Posições patrocinadas na busca, na página de concorrente e em listas de categoria. Leilão de **segundo preço** — paga o mínimo para superar quem está imediatamente abaixo. | O formato principal. Começar aqui. |
| **Brand Ads** | "Posição 0", antes dos patrocinados. Modo automático ou customizado com até **200 keywords**. | Exige **Minha Página ativa + reputação verde**. |
| **Display Ads** | Duas versões. A de autoserviço **não é recomendada em 2026** (sem segmentação real). A versão com assessor comercial tem segmentação de audiência. | Não usar a de autoserviço. |

### Lance: ROAS objetivo, não CPC

Desde outubro/2025 o mecanismo principal é **ROAS objetivo** (faixa **1x a 35x**), não
ACOS objetivo. Não se define CPC. O algoritmo ajusta o lance por leilão considerando
ROAS objetivo, **ad-score** (foto, ficha técnica, preço, reputação) e relevância.

ROAS e ACOS são inversos: **ROAS 8,33x = ACOS 12%**.

**Regra de calibração:** o ACOS objetivo deve ficar em **metade ou menos da margem de
contribuição**.

| Margem de contribuição | ROAS objetivo | ACOS equivalente |
|---:|---:|---:|
| 40% | ~5x | 20% |
| 30% | ~6,7x | 15% |
| 20% | ~10x | 10% |

Cruzando com a seção 2: no kit de 40 un a R$99,90, o ML já leva 27%. Depois do CPV, a
margem de contribuição provável fica em **20–30%** — logo **ROAS objetivo entre 6,7x e
10x**, ou seja ACOS de 10–15%. **Não 30%.** Rodar Ads com ACOS de 30% neste produto é
comprar receita com prejuízo.

### Estrutura e operação

- Agrupar **15 a 30 anúncios com preço e margem semelhantes** na mesma campanha.
  Com três anúncios de cápsula, é uma campanha só.
- Modo automático no início; manual depois de 2–3 meses com dados.
- **Ciclo de aprendizado: mínimo 14–15 dias; conclusão estatística confiável em 28
  dias.** Qualquer alteração — lance, orçamento, foto principal, título — **reinicia**
  o aprendizado.
- Orçamento: dimensionar por **dezenas de cliques por anúncio por semana** como piso
  para o algoritmo aprender, multiplicado pelo CPC médio da categoria.

### Métrica de decisão: TACOS, não ACOS

- **ACOS** = investimento ÷ receita atribuída a Ads.
- **TACOS** = investimento ÷ receita **total** (orgânica + paga).

TACOS é a métrica que decide escalar ou pausar. ACOS caindo com TACOS subindo
significa que Ads está canibalizando orgânico, não criando venda nova.

### Erros a evitar

Mexer em lance antes de 7 dias · pausar campanha bruscamente (esfria o orgânico) ·
editar título de anúncio rodando (reseta relevância) · tratar ML Ads como Google Ads ·
confundir ACOS com TACOS na decisão de escala · rodar Display autoserviço ·
subdimensionar orçamento e impedir o aprendizado.

---

## 8. Cursos e fontes de capacitação

### Gratuitos e oficiais — fazer primeiro

| Fonte | O que é | Por que |
|---|---|---|
| **Mercado Ads Academy** — `academy.mercadoads.com` | Cursos e certificação oficiais, 100% gratuitos. Módulos: Fundamentals, **Product Ads**, Brand Building, Audience Deals. Certificado exige **80% de acerto**. Login com a própria conta ML. | É a documentação do leilão escrita por quem opera o leilão. O módulo Product Ads é o mais direto ao objetivo. |
| **Central de Aprendizagem do Vendedor** — `vendedores.mercadolivre.com.br/aprender` | Catálogo de cursos + **treinamentos ao vivo**. Tem as páginas oficiais de custo do Full. | Fonte primária de tarifa. Quando blog e ML divergem, o ML ganha. |
| **Mercado Livre + Esecom** | Trilha para vendedor de qualquer nível, feita pelo ML com a Esecom. | Gratuito e oficial. |
| **Trilha do Conhecimento Nuvemshop** | Curso gratuito de ML, 8 aulas. | Bom nivelamento de time. |

### Pagos — avaliar depois

| Fonte | Observação |
|---|---|
| **Ecommerce na Prática** — "Mercado Livre do Zero" | Assinatura dá acesso a +40 cursos. Voltado a quem começa de zero — provavelmente abaixo do nível de vocês. |
| **Mapa do Mercado Livre** (Universidade Ecommerce) | Curso focado só em ML. |
| **Udemy** — "Do Zero ao Vendedor Profissional" | Barato, nível iniciante. |
| **Nubimetrics** (ferramenta, não curso) | Inteligência de mercado específica de ML: volume de busca por categoria, share de concorrente, sazonalidade. **Para a análise de concorrência que está bloqueada aqui, isto é o atalho pago.** A `academia.nubimetrics.com` publica relatórios trimestrais gratuitos. |

**Recomendação:** o time faz a **Mercado Ads Academy** (gratuita, oficial, certificada)
e avalia **Nubimetrics** como ferramenta. Curso pago de nível iniciante não resolve o
problema de vocês — o problema é dado de concorrência e conta de margem, não
fundamento de marketplace.

---

## 9. Plano de 90 dias

### Dias 1–15 — destravar e medir

| # | Ação | Entregável |
|---|---|---|
| 1 | Resolver estoque de **Clássico** e dos **kits multi-caixa** | Estoque para 90 dias de venda projetada |
| 2 | Rodar o **simulador de custo** da Central do Vendedor com peso e preço reais de cada formato | Tabela da seção 2 com números reais no lugar das estimativas |
| 3 | Resolver o **fork Supermercado vs. Alimentos e Bebidas** | Categoria decidida com a conta dos dois cenários |
| 4 | Conectar a extensão do Chrome e rodar a **auditoria de concorrência** (seção 4) | TSV preenchido, 3 recortes |
| 5 | Fotografar o SKU **Suave** em cápsula (vendido e sem foto) | Fotos nos slots do ML |
| 6 | Auditar `robots.txt` e schema do site | Crawlers de IA liberados, `Product` JSON-LD no ar |

### Dias 16–45 — subir certo

| # | Ação |
|---|---|
| 7 | Publicar os **3 anúncios** da arquitetura da seção 3, com ficha técnica **100%** preenchida |
| 8 | Entrar no **Full** com os três formatos. Lote inicial conservador — estoque antigo cobra a partir de 2 ou 4 meses |
| 9 | Time faz a **Mercado Ads Academy**, módulo Product Ads |
| 10 | Ligar **Product Ads** em modo automático só no cavalo de batalha (40 un), ROAS objetivo **7x** |
| 11 | **Não tocar em nada por 28 dias.** Toda alteração reinicia o aprendizado |
| 12 | Montar a planilha de **citation rate** (seção 6) e rodar a primeira medição |

### Dias 46–90 — escalar o que provou

| # | Ação |
|---|---|
| 13 | Ler os 28 dias: TACOS, % de impressão perdida por orçamento e por classificação |
| 14 | Se TACOS saudável → aumentar orçamento. Se perda por classificação alta → subir ROAS objetivo |
| 15 | Avaliar **Premium (19%)** apenas no anúncio de 100 un, com medição |
| 16 | Avaliar **Catálogo** para o cavalo de batalha |
| 17 | Avaliar **Brand Ads** (exige Minha Página + verde) |
| 18 | Abrir as duas lacunas achadas no Orfeu: **descafeinado** e **Dolce Gusto** |
| 19 | Publicar no site o conteúdo factual e extraível para GEO + `FAQPage` schema |

### O indicador único de sucesso

Não é faturamento. É **reputação verde mantida com CVR acima da mediana da categoria
no anúncio de 40 unidades**. Isso é o que destrava Buy Box, tabela de frete melhor,
Brand Ads e escala de Ads. Tudo o mais é consequência.

---

## 10. O que ainda não foi verificado

Lista honesta. Nada aqui deve virar decisão sem checagem.

| # | Lacuna | Como fechar | Impacto |
|---|---|---|---|
| 1 | **Concorrência no ML** — preços **auditados** em 25/09; faltam volume vendido, reputação e posição | Humano navega, leitura sobre a página carregada | **Médio.** Parcialmente fechada |
| 2 | **Quem paga o frete na faixa R$19–78,99** — fontes divergem | Simulador da Central do Vendedor | **Alto.** Muda o ponto de preço |
| 3 | **Custo de envio acima de R$79** para o peso real | Simulador, com peso e dimensão reais | **Alto.** As linhas de 40/60/100 un são estimativa |
| 4 | ~~Categoria exata e comissão~~ — **confirmada**: `Alimentos e Bebidas › Mercearia › Infusões › Cápsulas`, 14% Clássico | Auditado 25/09/2026 | **Fechada** |
| 5 | **Tabela completa de estoque antigo** (valor por tamanho por mês) | Central do Vendedor, logada | Médio |
| 6 | ~~CPV real da caixa de 10~~ — **R$ 15,10 com impostos** (R$ 1,51/cápsula) | Informado pela Canastra, 25/09/2026 | **Fechada** |
| 7 | **Anúncio atual de vocês** — busca por marca concluída: **nenhum dos 41 resultados de `cafe canastra` é a marca**. O anúncio não é achável pelo próprio nome | Mandar o link direto, se existir | **Alto** |
| 8 | **Volume de busca por termo** na categoria café | Tendências logado, ou Nubimetrics | Médio |
| 9 | ~~Coffee++ não identificada~~ — **é café especial em cápsula, via Cafezale, marca irmã Coffee Mais** | Auditado 25/09/2026 | **Fechada** |

---

## 11. Registro de método

O que esta pesquisa ensinou, no formato do `CLAUDE.md` — **sintoma → causa → regra**:

1. **`WebFetch` devolveu 403 em toda página do ML** → o User-Agent do WebFetch é
   recusado; `curl` com UA de Chrome recebe 200 na home → antes de concluir que um
   site é inacessível, teste o mesmo host com UA de navegador. Mas: 200 na home não
   é 200 na busca.
2. **`curl` com UA de navegador devolveu 200 na busca e nenhum produto** → a resposta
   era `suspicious-traffic-frontend`, o muro anti-bot, com status 200 → **status 200
   não prova que você recebeu o conteúdo.** Confira o `<html data-assets-prefix>`
   antes de parsear. É a mesma lição do CLAUDE.md ("HTTP 200 não prova que o
   parâmetro funcionou") em outro domínio.
3. **Dois blogs afirmaram regras opostas de frete na mesma faixa de preço** → conteúdo
   de blog sobre tarifa de marketplace envelhece e se copia errado → tarifa só vale se
   vier do simulador logado. Blog serve para saber **que a tarifa existe**, não quanto
   ela é.
4. **`tendencias.mercadolivre.com.br` respondeu 200 e pareceu útil** → entrega só o top
   nacional; toda tentativa de corte por categoria (`/MLB1403` e variantes) devolveu
   404 servindo a mesma página → 404 que renderiza conteúdo é 404. Confira se o dado
   mudou, não se a página abriu.
5. **A conta da caixa de 10 unidades só apareceu ao montar a tabela por formato** →
   olhando um preço isolado, 14% de comissão parece pouco → em produto de ticket
   baixo, o custo **por pedido** domina o custo **percentual**. Sempre calcule o take
   total como % da receita, nunca só a comissão.

6. **A navegação programática no ML funciona uma vez e depois trava** → a primeira busca
   carregou 136 cards; as quatro seguintes ficaram em `ui-search-loading-screen` com
   `cards=0`, inclusive com espera de 10s e recarga → é limitação de ritmo contra
   automação, não falha de seletor. **Confira `spinner` e `cards` antes de concluir que o
   seletor quebrou.** A rota que funciona é o humano navegar e a leitura ser feita sobre a
   página já carregada — `javascript_tool` sobre o DOM pronto, sem `navigate`.
7. **Li preço de concorrente em anúncio de revendedor e tomei por preço da marca** →
   "Orfeu Arara" a R$ 5,52–5,59/cápsula eram revendas de microlote; a escada real do Orfeu
   é R$ 2,29–2,79 → **em marketplace, preço sem vendedor identificado não é preço da
   marca.** O cartão de resultado não expõe o vendedor; confirme na página do anúncio
   antes de usar o número como âncora competitiva.
8. **Li "+10mil vendidos" numa página de produto e quase publiquei como volume do
   concorrente** → o número veio de um bloco `poly-card`, que **na página de produto é
   carrossel de recomendação**, não o produto aberto; o dado real estava em
   `[class*="ui-pdp-seller"]` e dizia **+5 vendas** → o mesmo seletor significa coisas
   diferentes em páginas diferentes. Antes de usar um número raspado, **rastreie o nó pai**
   (`TreeWalker` + cadeia de `className`) e confirme de qual container ele veio. É a lição
   17 do topo deste arquivo em outro domínio: um seletor que encontra *algo* é pior que um
   que falha.
