# Remessa ao Full × estratégia de preço no Ads

> Script: [`scripts/envio.py`](scripts/envio.py) — gera todos os números deste arquivo.
> Artefato: [Remessa, Verba e Verde](https://claude.ai/artifact/DVnV5QhiRsh1GLeD2iyEBD).
> Leituras da conta: **30/09/2026**, extensão do Chrome na sessão logada.
>
> **Revisado em 30/09 com os custos reais lidos dentro do formulário de edição.**
> Ver [Custos corrigidos](#custos-corrigidos-lidos-no-formulário) — duas premissas caíram e
> a recomendação mudou.

---

## Os dois bloqueadores medidos na conta hoje

### 1. O certificado digital vence hoje
Painel de anúncios, textual: *"Seus anúncios Full serão pausados amanhã. Seu certificado
digital vence amanhã, em 30/09/2026. Sem ele, você não consegue emitir NF-e."*

**Nada deste plano roda com anúncio Full pausado.** É a primeira ação, antes do resto.

### 2. A Central de promoções está bloqueada
`Anúncios → Central de promoções` (URL real: `vendedores.mercadolivre.com.br/anuncios/lista/promos`),
textual:

> *"No momento, não é possível oferecer promoções. Recupere sua reputação verde ou amarela
> para oferecê-las novamente."*

**0 anúncios** elegíveis. A página tem os filtros `Com redução de tarifas` e
`Meus melhores anúncios`, e um calendário de campanhas — o mecanismo existe nesta conta,
só está trancado pela cor.

**Consequência direta:** das três estratégias de preço abaixo, **só a primeira está
disponível hoje.**


---

## Custos corrigidos, lidos no formulário

Abrir o formulário de edição em 30/09 deu os custos exatos e **derrubou duas premissas**.

### Medido, Clássico, no Full

| | Caixa 10 @ R$ 18,70 | Kit 40 @ R$ 139,90 |
|---|---:|---:|
| Comissão Clássico (14%) | R$ 2,62 | R$ 19,59 |
| Comissão Premium (19%) | R$ 3,55 | R$ 26,58 |
| **Frete grátis** | **R$ 14,45** | **R$ 14,45** |
| Comprador paga | R$ 1,40 | R$ 7,20 |

**O frete grátis é R$ 14,45 nos dois** — valor único, que não muda com o preço nem com o
peso. Era o único número que a documentação marcava como mole (R$ 20,00 interpolado).

### O que mudou

| | Antes | Agora |
|---|---:|---:|
| Frete grátis do kit | R$ 20,00 *(interpolado)* | **R$ 14,45** *(medido)* |
| Lucro do kit a R$ 139,90 | R$ 39,91 | **R$ 45,46** |
| Lucro médio, estratégia 3 | R$ 22,37 | **R$ 24,87** |
| ROAS de equilíbrio, estratégia 3 | 3,52× | **3,17×** |
| Agressiva + misto em 3 meses | −R$ 29 | **+R$ 753** |

### A categoria não é Supermercado

O formulário mostra **Alimentos e Bebidas > Mercearia > Infusões > Cápsulas**. O rótulo
`SUPERMERCADO` que aparece na lista de anúncios é outra coisa — canal, não categoria.

Consequência: **o estoque antigo dispara aos 4 meses, não aos 2**, então não incide em
nenhum mês desta projeção. No lugar entra a armazenagem diária de A&B
(R$ 0,007/dia caixa · R$ 0,015/dia kit), que é pequena. O teto de "2 meses de cobertura"
da postura ideal era conservador demais — mas eu o mantive, porque folga de estoque
também protege contra ruptura.

### Frete grátis não é obrigatório acima de R$ 79

O kit a R$ 139,90 aceita comprador-paga, que custa **R$ 7,20** contra R$ 14,45 do grátis —
**mais R$ 7,25 por kit**. Em troca, o anúncio sai do filtro "Frete grátis", que é um dos
mais usados na busca.

**Não apliquei.** É mudança de estratégia, não de execução — decisão do Rafael. Um campo.

---

## As três estratégias de preço no Ads

A pergunta era se a estratégia 3 (Ads misto, com e sem verdinho) existe. **Existe, de dois
jeitos.**

### Jeito simples — a promoção é por anúncio, não por campanha
O verdinho é configurado anúncio por anúncio na Central de promoções. O Product Ads anuncia
o anúncio e mostra o preço que ele tiver. Logo **uma mesma campanha pode conter anúncio com
verdinho e anúncio sem** — nada no Ads acopla os dois. Não exige truque nenhum.

### Jeito avançado — o mesmo produto nos dois estados ao mesmo tempo

> *"Os anúncios premium têm uma disponibilidade total dessas campanhas… Se for um anúncio
> clássico, [não]. (…) Você vai entrar num anúncio seu que tá lá no clássico, você vai criar
> uma variação daquele anúncio, inclui uma variação, escolhe o premium, todo o restante é
> igual. Fazendo essa diferenciação de preço, você vai tá coberto dos dois lados."*
>
> *"Tem várias campanhas lá da Central de Promoções que têm pagamentos de cashback. Então
> você reduz o seu preço em, sei lá, R$ 20, só que R$ 5 disso o Mercado Livre devolve para
> você em redução de tarifa."* — e ele mede um caso em que **o cashback cobriu exatamente a
> diferença de tarifa Clássico→Premium**.
>
> — Milton P Rabello, 27/08/2026, `swCx36qRg0w`

Como Premium acessa campanhas que Clássico não acessa, o par **Clássico + variação Premium**
deixa o *mesmo* produto anunciado com e sem verdinho simultaneamente.

Ele acrescenta duas regras operacionais:

- **Precifique 30% acima do preço final objetivo.** Sem essa gordura você não entra em
  promoção sem zerar a margem, nem paga afiliado (*"quase nenhum afiliado se interessa por
  produto que paga menos de 7, 8% de comissão"*).
- **Varra a Central 1× por semana** cruzando com o gerenciador. Campanha com cashback
  aparece e sai; se o concorrente pega e você não, a venda para.

### A distinção que decide a ação de hoje

**Baixar o preço ≠ verdinho.** Editar preço é campo do anúncio e está liberado (a Gestão de
preços abre; a conta marca "competitividade de preços boa"). O que a reputação vermelha
tranca é a **promoção**: o riscado, a entrada nas campanhas do ML e o cashback.

Vender a R$ 28,90 você pode hoje. Vender **R$ 28,90 riscado de R$ 34,90**, não — e é o
riscado que converte.

---

## A conta que escolhe entre as três

O verdinho custa margem e compra conversão. A pergunta útil não é "qual converte mais", é
**quanto mais precisa converter para pagar o desconto**. Isso é derivável do custo real.

| Estratégia | Caixa 10 | Kit 40 | Lucro médio | ROAS de equilíbrio | Lift necessário |
|---|---:|---:|---:|---:|---:|
| **1** Preço cheio nos dois | 34,90 | 139,90 | **27,51** | 2,99× | — |
| **2** Verdinho nos dois | 28,90 | 124,90 | **19,07** | 3,78× | **+44,3%** |
| **3** Verdinho só na caixa | 28,90 | 139,90 | **24,87** | 3,17× | **+10,6%** |

Mix de 55% caixa / 45% kit. Lift necessário = razão entre os lucros médios.

**O desconto no kit é o que não se paga.** A caixa de 10 é o item que o comprador compara
com o Coffee++ a R$ 28,90 — o riscado trabalha ali, e pede só +11,8%. No kit se comparam
R$/cápsula, não preço absoluto: o riscado convence muito menos do que custa, e a exigência
salta para +51%.

**A estratégia 3 domina a 2 por construção, não por gosto.**

---

## As três posturas

Cada postura escolhe **duas** coisas. Todo o resto decorre.

| Postura | Ads/dia (mês 1→3) | Folga de estoque sobre a demanda |
|---|---|---|
| Conservadora | 10 → 10 → 15 | 1,3× |
| **Ideal** | **20 → 30 → 40** | **2,0× — o teto do Supermercado** |
| Agressiva | 60 → 80 → 80 | 1,8× (esgotar destrói o ativo) |

A folga da ideal é 2 meses de cobertura porque **em Supermercado o custo de estoque antigo
dispara aos 2 meses**, não aos 4.

---

## Resultado em 3 meses, por estratégia × postura

| Postura | Estratégia 1 | Estratégia 2 | Estratégia 3 |
|---|---:|---:|---:|
| Conservadora | +615 | +718 | **+820** |
| Ideal | +652 | +841 | **+1.059** |
| Agressiva | −40 | +338 | **+753** |

A estratégia 3 ganha nas três posturas.

### Plano de remessa da estratégia 3

| Postura | Mês 1 | Em 3 meses | Capital mês 1 | Capital 3 meses | Vendas 3 m |
|---|---|---|---:|---:|---:|
| Conservadora | 5 de cada · 15 cx + 20 kits | 99 un | 1.435 | 3.817 | 76 |
| Ideal | 13 de cada · 39 cx + 52 kits | 268 un | 3.730 | 10.494 | 155 |
| **Agressiva** | **26 de cada · 78 cx + 104 kits** | **458 un** | **7.459** | **17.757** | **302** |

"De cada" = unidades por anúncio, já respeitando o anúncio mais exigente (3 de caixa,
4 de kit). Do mês 2 em diante a remessa é só **reposição do que vendeu**.

**Capital:** só o do mês 1 sai do bolso. Do mês 2 em diante a receita repõe — com uma
exceção medida: na postura **ideal** o faturamento do mês 1 fica R$ 232 abaixo da reposição
do mês 2. Conservadora e agressiva se autofinanciam.

---

## O que a agressividade compra: o verde

A reputação é média móvel de **365 dias**. Hoje: **26 envios incorretos em 69 envios =
37,68%**, contra teto de 13%.

> **131 vendas limpas levam a conta ao verde.**
> `26 ÷ (69 + V) ≤ 0,13 → V ≥ 131`

| Postura (estratégia 3) | Vendas em 3 meses | Envios incorretos no mês 3 | Verde? |
|---|---:|---:|---|
| Conservadora | 76 | 17,9% | **não** — faltam 55 vendas |
| Ideal | 155 | 11,6% | **sim, no mês 3** |
| Agressiva | 302 | 7,0% | **sim, no mês 2** |

**A conservadora não cura a reputação em nenhuma das três estratégias** (61 / 94 / 76
vendas). Ela dá o melhor resultado por real investido e deixa a conta vermelha — Ads caro,
sem Buy Box, sem catálogo, sem promoção. É lucro pequeno num beco.

Na estratégia 1, a **ideal também não chega** — 125 vendas, faltando 6. Outro motivo para
não ficar no preço cheio.

---

## O nó, e os R$ 75 que o desatam

A estratégia 3 é a melhor. Mas o verdinho exige verde; o verde exige 131 vendas; e fazer
131 vendas no preço cheio é justamente a estratégia 1, a pior das três.

A saída está escrita na própria página de reputação do ML:

> *"Recupere a cor verde-claro da sua reputação deixando **R$ 75 como garantia**. Com esse
> benefício, mais compradores encontrarão seus anúncios."*

Os R$ 75 **pulam as 131 vendas** e destravam a Central de promoções de imediato.

| Postura | Estratégia 1 (hoje) | Estratégia 3 (com o verde) | Diferença em 3 meses |
|---|---:|---:|---:|
| Conservadora | +615 | +820 | **+205** |
| Ideal | +652 | +1.059 | **+407** |
| Agressiva | −40 | +753 | **+793** |

---

## Recomendação

**Renovar o certificado hoje → depositar os R$ 75 → estratégia 3 → postura ideal.**

Melhor resultado de 3 meses (**+R$ 647**) e **verde no mês 3** com 155 vendas.

A agressiva chega ao verde um mês antes, mas custa **R$ 7.459 de capital no mês 1** e fecha
no zero a zero (−R$ 29). Vale se a pressa pelo verde e pelo Produto Estrela valer mais que o
lucro do trimestre — e nela o prejuízo é quase nulo justamente porque a estratégia 3 tem
ROAS de equilíbrio baixo.

---

## Premissas — medido × suposto

### Medido
CPV R$ 15,10/caixa e R$ 60,40/kit · comissão 14% sobre o preço efetivo · envio pago pelo
comprador ~6% do preço · categoria Alimentos e Bebidas (armazenagem R$ 0,007/dia caixa · R$ 0,015/dia kit) ·
reputação 26/69 com janela de 365 dias · Central de promoções bloqueada (30/09/2026) ·
tráfego orgânico de 12 visitas/dia num anúncio, no vermelho e sem Ads.

### Interpolado ou suposto — não afirmar como fato
| Item | Valor | Situação |
|---|---|---|
| ~~Frete grátis do kit~~ | **R$ 14,45** | **medido no formulário 30/09** |
| ~~Estoque antigo nos meses 2 e 3~~ | **não incide** | categoria A&B dispara aos 4 meses |
| Mix de vendas | 55% caixa / 45% kit | premissa |
| Curva de ROAS | 4,50× a R$ 10/dia, expoente 0,25 | premissa, ancorada em "ROAS 3 a 5 nas primeiras semanas" |
| **Lift do verdinho** | **+35% na caixa, 0% no kit** | **premissa, nunca medida** |
| CPC e conversão da categoria | — | nunca medidos. É o que a Fase 1 existe para resolver |

**Onde o modelo é mais frágil:** no lift do verdinho. Ele decide a corrida entre as
estratégias e é palpite informado. Mas a conclusão não depende do valor exato — o que vale
é o **limiar**: a caixa precisa de +11,8% e o kit de +51%. Esses dois são derivados do custo
real e valem qualquer que seja o lift verdadeiro.

Segunda fragilidade: a **elasticidade do ROAS com a verba**. Se o leilão desta categoria for
raso, a agressiva entrega menos do que a tabela mostra.

---

## Achado a conferir

O contador do painel me deu **14** numa leitura e **1** em outra, no mesmo lugar.
[`01-situacao-da-conta.md`](01-situacao-da-conta.md) registra **1**. **Ler o mesmo contador
duas vezes e obter números diferentes significa que eu não sei ler esse contador** — ele
fica num carrossel de cards e o número que eu capturo pode ser o do card vizinho.

**O que está medido de verdade:** os **7 anúncios em escopo** foram lidos um a um e todos
estão inativos por **falta de estoque** (*"Não há mais unidades à venda"*), nenhum por
política. Isso vale.

**Para saber quantos são de fato:** filtre a lista por "Inativos por descumprir políticas"
e conte as linhas. Não use o contador do card.
