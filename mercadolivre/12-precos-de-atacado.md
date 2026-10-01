# Preços de atacado — vale a pena?

> Script: [`scripts/atacado.py`](scripts/atacado.py).
> **Resposta curta: sim nos 4 kits, não nas 3 caixas — e só depois da reputação verde.**

---

## O que é, medido

No formulário o bloco se chama **"Preços de atacado · EXCLUSIVO NEGÓCIOS"**.

> *"Isso aqui **só serve para empresas**. Só conta **CNPJ** tem disponível a opção de preços
> por atacado. **CPFs vão entrar no anúncio mas não vai ter essa opção** disponível lá
> dentro. Pode adicionar até **cinco opções**."*
> — `BSNDMsezcbc`, criação de anúncio passo a passo

> *"Não vou colocar preço atacado, mas **recomendo que você utilize**. (…) Ah, não vai
> deixar porque **eu não tenho estoque suficiente**. (…) Ele só avisou."*
> — Fabio Ludke, 10/08/2026, `-javeW5ePCg`

Três consequências:

1. **Não canibaliza o varejo.** Quem paga com CPF nem enxerga a faixa. O risco de derrubar o ticket do varejo é **zero**.
2. **Até 5 faixas** por anúncio.
3. **A faixa precisa caber no estoque.** O ML avisa quando não cabe — faixa de 10 com 5 no Full é decoração.

### Precedente na própria conta
O café em grãos `MLB5903454718` (R$ 109,90) **já usa duas faixas**: `5+ → R$ 99,99` (−9,0%)
e `10+ → R$ 94,99` (−13,6%). Ou seja, a mecânica já roda aqui.

---

## A conta que separa kit de caixa

Tudo depende de **como o frete se comporta num pedido de N unidades**.

| | Caixa de 10 | Kit de 40 |
|---|---|---|
| Quem paga o frete | **comprador** | **vendedor** (frete grátis) |
| O que o vendedor paga | custo operacional, **~6% do pedido** | **R$ 14,45 por ENVIO** |
| O que acontece no lote | sobe proporcional ao valor — **não dilui nada** | fica quase o mesmo — **dilui** |

É essa diferença que decide.

### Kit de 40 — a margem se sustenta

| Qtd | Preço/un | Desconto | Lucro/un | Margem | R$/cápsula |
|---:|---:|---:|---:|---:|---:|
| 1 | 139,90 | — | 45,46 | 32,5% | 3,50 |
| **2+** | **132,90** | 5,0% | **43,68** | **32,9%** | 3,32 |
| **3+** | **129,90** | 7,1% | **42,97** | **33,1%** | 3,25 |
| **5+** | **124,90** | 10,7% | **40,55** | **32,5%** | 3,12 |
| 10+ | 119,90 | 14,3% | 38,14 | 31,8% | 3,00 |

**A margem não cai** — em 2 e 3 unidades ela até sobe, porque os R$ 14,45 de frete grátis
se dividem por mais kits.

### Caixa de 10 — a margem cai direto

| Qtd | Preço/un | Desconto | Lucro/un | Margem |
|---:|---:|---:|---:|---:|
| 1 | 34,90 | — | 12,82 | 36,7% |
| 3+ | 32,90 | 5,7% | 11,22 | 34,1% |
| 5+ | 31,90 | 8,6% | 10,42 | 32,7% |
| 10+ | 29,90 | 14,3% | 8,82 | 29,5% |
| 20+ | 28,90 | 17,2% | 8,02 | 27,8% |

O desconto sai **inteiro da margem**, porque não há frete de vendedor para diluir.

---

## O problema que o atacado hoje resolve, e que não é o atacado

| Produto | R$/cápsula |
|---|---:|
| Caixa de 10 avulsa | **3,49** |
| Kit de 40 avulso | **3,50** |

**O kit de 40 não tem desconto por volume nenhum.** Está um centavo *mais caro* por cápsula
que a caixa avulsa. Não existe motivo para o comprador subir de ticket.

As faixas de atacado corrigem isso **para CNPJ**. Mas o problema de fundo é do **varejo**, e
esse nenhuma faixa de atacado resolve — para o CPF a escada continua plana.

**Vale decidir à parte:** ou o kit de 40 desce (R$ 129,90 = R$ 3,25/cáp), ou a caixa de 10
sobe. Hoje as duas pontas se anulam. *(não está no escopo das edições aprovadas)*

---

## O contra-argumento que quase passou batido

A métrica de reputação conta **envios**, não unidades. Faltam **131 envios limpos** para o
verde (`26 ÷ (69+V) ≤ 0,13`).

| Unidades vendidas | Envios se avulso | Envios em lotes de 5 | Diferença |
|---:|---:|---:|---:|
| 100 | 100 | 20 | **−80** |
| 200 | 200 | 40 | **−160** |
| 300 | 300 | 60 | **−240** |

**Atacado vende mais unidades com menos envios.** Enquanto a conta estiver vermelha, isso
**atrasa a chegada ao verde** — que é o objetivo número um dos próximos 60 dias.

É o mesmo raciocínio de [`09-remessa-e-estrategia-de-preco.md`](09-remessa-e-estrategia-de-preco.md):
o gargalo não é faturamento, é quantidade de envios limpos.

---

## Recomendação

### Agora, enquanto a conta está vermelha
**Não configurar.** Não porque faça mal, mas porque compete com a prioridade: cada pedido
grande é um envio limpo a menos na conta que precisa de 131 deles.

### Depois do verde — nos 4 kits, três faixas

| ID | Anúncio | 2+ | 3+ | 5+ |
|---|---|---:|---:|---:|
| `2691993380` | Kit 40 Clássico | 132,90 | 129,90 | 124,90 |
| `2691960931` | Kit 40 Suave | 132,90 | 129,90 | 124,90 |
| `2691974195` | Kit 40 Canela | 132,90 | 129,90 | 124,90 |
| `2691974682` | Kit 40 · 3 Sabores | 132,90 | 129,90 | 124,90 |

Três faixas das cinco disponíveis. **Não use a faixa de 10+** sem ter 10 kits daquele
anúncio no Full — na postura conservadora (5 de cada) ela nunca dispara.

**Por que essas faixas:** a de 5+ leva a R$ 3,12/cápsula, que **empata com o Orfeu**
(R$ 3,14/cáp no kit de 50) — o patamar certo para ganhar um comprador CNPJ sem entregar
margem. E todas as três mantêm a margem em ~33%.

### Nas 3 caixas de 10 — não

`2692127545` · `2692082114` · `2692076338`: **deixar sem faixa.**

A caixa de 10 é item de entrada e de teste. Empresa que quer volume compra o kit — é para lá
que a escada deve empurrar. Colocar atacado na caixa faz o oposto: dá desconto de volume no
produto errado e ainda come a margem, que é onde a caixa não tem folga.

### Quando revisar
Depois de 30 dias com as faixas no ar, olhe **quantos pedidos vieram por faixa**. Se a de
5+ nunca disparar, ela não custa nada — mas a de 2+ deveria disparar. Se nem ela disparar,
o comprador CNPJ não está chegando, e o problema é de tráfego, não de preço.

---

## O que não foi medido

| Item | Situação |
|---|---|
| **Como o frete grátis escala com o peso do pedido** | Usei `14,45 × √n`. Medi só o valor de 1 unidade. **No pior caso** (14,45 por unidade), a margem do 5+ cai de 32,5% para 26,1% — ainda saudável, então a recomendação não muda |
| Custo operacional exato da caixa a R$ 34,90 | Estimado em 6%. Medidos: 1,40@18,70 · 2,40@40 · 4,80@83,10 · 7,20@139,90 |
| Se há tarifa mínima por pedido no ML Negócios | Não encontrado em nenhuma fonte |
| Volume real de compradores CNPJ em cápsula | Nunca medido. É o que os 30 dias de teste respondem |
