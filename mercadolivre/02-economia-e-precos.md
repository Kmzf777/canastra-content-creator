# Economia e preços

> Base de todo cálculo do projeto. Script: [`../scripts/econ2.py`](scripts/econ2.py) e
> [`../scripts/promo2.py`](scripts/promo2.py).

---

## Constantes

| Item | Valor | Origem |
|---|---|---|
| **CPV** | **R$ 15,10 por caixa de 10** = R$ 1,51/cápsula, impostos inclusos | Rafael |
| Comissão Clássico | **14%** sobre o preço efetivo | conta (R$ 4,05 em R$ 28,90) |
| Comissão Premium | **19%** — exatos 5 pontos a mais, em qualquer preço | conta |
| Categoria | Alimentos e Bebidas › Mercearia › Infusões › Cápsulas | busca do ML |

**A comissão é igual em Supermercado e em Alimentos e Bebidas.** Confirmado pelos
números da conta. A diferença entre as duas é só armazenagem e prazo de estoque antigo.

---

## Custo de envio — medido na conta, não em blog

Esta é a correção mais importante do projeto. Os valores de blog que eu usava estavam
errados nos dois sentidos.

| Situação | Custo real | Onde foi medido |
|---|---:|---|
| Caixa 10 · comprador paga | **R$ 1,40** | anúncio a R$ 18,70 |
| Kit 40 · comprador paga | **R$ 2,40** | anúncio a R$ 40 |
| Kit 40 · comprador paga | **R$ 4,80** | anúncio a R$ 83,10 |
| **Caixa 10 · frete grátis** | **R$ 14,45** | anúncio a R$ 28,90 |
| **Kit 60 · frete grátis** | **R$ 29,90 a 34,30** | anúncios a R$ 109,99 |

**Padrão:** com o comprador pagando, o custo fica em ~6% do preço. Com frete grátis,
dispara.

**Único número ainda estimado:** o frete grátis do **kit de 40**, interpolado em
**R$ 20,00** entre os R$ 14,45 da caixa e os R$ 29,90 do kit de 60. Confirmar no
simulador da Central antes de fixar preço.

### Regra de faixa

| Faixa | Quem paga |
|---|---|
| < R$ 19 | Comprador, salvo se o vendedor oferecer grátis |
| R$ 19 – 78,99 | Se o vendedor oferecer grátis, **ele paga** (R$ 6,95 a 8,25) |
| ≥ R$ 79 | **Frete grátis obrigatório**; custo a partir de R$ 13,85, com desconto por reputação |

---

## Armazenagem no Full e estoque antigo

| Tamanho | Supermercado | Alimentos e Bebidas |
|---|---:|---:|
| Pequeno (caixa de 10) | **R$ 0,000/dia** | R$ 0,007/dia |
| Médio (kit de 40) | **R$ 0,000/dia** | R$ 0,015/dia |

**Estoque antigo começa a cobrar aos 2 meses em Supermercado** e aos 4 nos demais.

### A escalada do estoque parado

| Unidades paradas | Mês 1 | Mês 5 | Mês 7 |
|---:|---:|---:|---:|
| 100 | R$ 21 | R$ 121 | **R$ 1.221** |
| 300 | R$ 63 | R$ 363 | **R$ 3.663** |
| 600 | R$ 126 | R$ 726 | **R$ 7.326** |

*(Milewa, 25/09/2026, `7h4R4KPK9bw`)*

**Regra que sai disso:** mande ao Full só o que gira antes do prazo, medido pelas vendas
dos últimos 30 dias — não pelo que você tem em casa.

### Trocar de categoria: quanto custa

Para 90 caixas + 80 kits em 3 meses:

| | Supermercado | Alimentos e Bebidas |
|---|---:|---:|
| Armazenagem | **R$ 0,00** | R$ 164,70 |
| Estoque antigo começa | **2 meses** | **4 meses** |

Trocar custa **R$ 164,70 em 3 meses** e compra o dobro de prazo. **Decisão do Rafael:
manter Supermercado** — o que só é seguro se o giro vier.

**O status Produto Estrela desliga essa multa.** Ver
[`06-plano-de-escala.md`](06-plano-de-escala.md).

---

## Preços decididos

| Produto | Preço | R$/cáp | Comissão | Envio | Lucro | Margem |
|---|---:|---:|---:|---:|---:|---:|
| Caixa 10 un | **34,90** | 3,49 | 4,89 | 2,09 | **12,82** | **36,7%** |
| Kit 40 un | **139,90** | 3,50 | 19,59 | **14,45** | **45,46** | **32,5%** |

*(Clássico 14%, Supermercado com armazenagem zero, comprador paga o frete na caixa)*

### Por que o kit não pode ficar abaixo de R$ 79
A R$ 78,90 com o comprador pagando, sobra **R$ 1,82** — o CPV do kit já é R$ 60,40.
Cruzar os R$ 79 e assumir o frete grátis é a única faixa que fecha.

### O preço de hoje dá prejuízo
A caixa de 10 a R$ 24,90 (preço da loja própria) **perde R$ 0,66 por pedido** no ML:
comissão R$ 3,49 + envio R$ 6,55 + CPV R$ 15,10 = R$ 25,14 contra R$ 24,90 de receita.
**Preço de marketplace é preço com 26–40% de take embutido.**

---

## Promoção — a escada do preço riscado

A comissão incide sobre o **preço efetivo**, então o desconto não é cobrado em cima do
cheio.

### Caixa de 10, de R$ 34,90

| Por | Desconto | Lucro | Margem | Posição |
|---:|---:|---:|---:|---|
| 34,90 | — | 12,82 | 36,7% | acima de todo especial corrente |
| 31,90 | 8,6% | 10,42 | 32,7% | — |
| 29,90 | 14,3% | 8,82 | 29,5% | R$ 1 acima do Coffee++ |
| **28,90** | **17,2%** | **8,02** | **27,8%** | **empata com o Coffee++** |
| 27,90 | 20,1% | 7,22 | 25,9% | empata com o Orfeu |
| 26,90 | 22,9% | 6,42 | 23,9% | abaixo do Orfeu — piso |

### Kit de 40, de R$ 139,90

| Por | Desconto | Lucro | Margem | R$/cáp |
|---:|---:|---:|---:|---:|
| 139,90 | — | 45,46 | 32,5% | 3,50 |
| 129,90 | 7,1% | 31,31 | 24,1% | 3,25 |
| **124,90** | **10,7%** | **27,01** | **21,6%** | **3,12** — passa por baixo do kit 50 do Orfeu (3,14) |
| 119,90 | 14,3% | 22,71 | 18,9% | 3,00 |
| 114,90 | 17,9% | 18,41 | 16,0% | 2,87 — margem apertada para Ads |

### Por que o preço cheio precisa de folga

> *"Se você coloca exatamente 10% de margem e entra numa promoção, sua margem pode ir a
> zero — aí você não vai participar de promoção nenhuma e sua venda vai ficar
> extremamente prejudicada."*
> — Milton P Rabello, 27/08/2026, `swCx36qRg0w`

Com 36,7% no cheio, dá para descontar 17% e ainda sobrar 27,8%. É isso que permite entrar
nas campanhas da Central de Promoções — que, segundo a mesma fonte, viram **anúncio pago
do ML no Instagram, Facebook e TikTok**.

---

## Clássico ou Premium

Premium custa **exatos 5 pontos de margem** em qualquer preço.

> **Tarifas conferidas no formulário em 30/09:** caixa a R$ 18,70 paga R$ 2,62 (Clássico)
> contra R$ 3,55 (Premium); kit a R$ 139,90 paga R$ 19,59 contra R$ 26,58. Bate com 14% e 19%.

| Produto | Clássico | Premium | Custo | 12× de |
|---|---:|---:|---:|---:|
| Caixa 10 · R$ 34,90 | 36,7% | 30,5% | R$ 1,75 | R$ 2,91 |
| Kit 40 · R$ 139,90 | **32,5%** | **27,5%** | R$ 6,99 | R$ 11,66 |
| Kit 60 · R$ 199,90 | 24,2% | 19,2% | R$ 10,00 | R$ 16,66 |

### A regra das fontes

| Situação | Escolha | Fonte |
|---|---|---|
| Produto **abaixo de R$ 150** | Clássico | Milton P Rabello, 27/08 |
| Produto **acima de R$ 150** | **Premium** — "o consumidor vai querer dividir; você perde para quem está parcelando, mesmo se o produto dele for mais caro" | idem |
| Abaixo de R$ 400, ticket baixo | Clássico | Ivan Saldanha, 25/08 |
| **Anúncio de catálogo** | **Sempre Clássico** — catálogo é disputa de preço | Milton, 27/08 |
| **Conta nova** | Premium acelera mais no começo | Milton, 27/08 |

### O que eu não tinha considerado
- Premium tem **disponibilidade total das campanhas** da Central de Promoções; Clássico
  pode ter campanhas restringidas
- **O cashback da campanha pode pagar exatamente a diferença de tarifa** — exemplo dele:
  produto de R$ 100, Clássico 11% = R$ 11, Premium 16% = R$ 16, cashback R$ 5
- Dá para ter **os dois no mesmo anúncio**, criando uma variação Premium do Clássico

**Decisão atual:** Clássico nos 7 (todos abaixo de R$ 150). Avaliar a variação Premium
para elegibilidade a promoção.
