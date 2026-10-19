# Auditoria da conta Amazon — Café Canastra (15/10/2026)

> Lido no Seller Central e na amazon.com.br pelo Claude in Chrome, **só leitura**, sessão do Rafael,
> 15/10/2026 entre ~16h e ~17h BRT. Nada foi alterado, aceito, inscrito ou baixado.
> Formato de agência: **evidência → diagnóstico → risco de não agir → próximo passo**, por impacto em
> dinheiro. O que não foi lido está marcado *não medido*.

## Resumo em 6 linhas

1. **Não há 1 kg nem 500 g na conta.** As 6 ofertas são de drip coffee, todas inativas, estoque 0. A
   estratégia de 1 kg/500 g é um **lançamento de ASIN novo**.
2. **A única operação (1 envio, 50 un. de drip) vendeu 33 e perdeu 17 por VALIDADE.** Em junho/2026 a
   Amazon passou as 17 restantes para "EXPIRED"; 15 voltaram ao vendedor em julho, 1 foi descartada e
   1 perdida em agosto. **É a lição nº 1 para o 1 kg.**
3. **Os campeões esgotaram em 3 semanas e não foram repostos.** Drip Suave 10 un. e Canela 10 un.
   venderam as 10 unidades de cada em abril (conversão de 34% e 20%) e ficaram sem estoque.
4. **Nunca houve Ads** (o console abre na tela de cadastro) e **não há Brand Registry** (o site de
   cadastro de marcas abre nas boas-vindas). Sem Brand Registry não há Vine, A+, Store nem Brand Analytics.
5. **A própria Amazon (1P) vende um produto nosso**: "Café Néctar de Minas Café Canastra Moído 500 g"
   (B08LXZ7C41), marca "Café Canastra", a **R$ 137,00**, sob encomenda, 1 avaliação.
6. **Conta saudável**: AHR 200 (Ideal), 0 violações, nota de vendedor 5,0.

---

## 1. Histórico: o que fizemos e o que aconteceu (impacto: alto)

### 1.1 O envio

| Remessa | Criada | Em trânsito | Entregue | Recebimento encerrado | Destino | Unidades |
|---|---|---|---|---|---|---:|
| FBA199CQZ0L1 (ref. 4U3IYOIN) | 23/03/2026 | 31/03 | 01/04/2026 | 13/04/2026 | CNF5 | 50/50, sem divergência, todas Prime |

Fonte: Gerenciar envios (`/manage/shipments`), 15/10/2026. É o **único** envio listado; envios
cancelados ou rascunhos fora do filtro padrão: *não verificado*. Prazo real entre entrega e fim do
recebimento: **12 dias**, fora de pico.

### 1.2 Para onde foram as 50 unidades

Fonte: Registro de inventário (`/reportcentral/LEDGER_REPORT/0`), visão resumida, por país, mensal,
03/2026 a 09/2026, lido em tela (sem download).

| ASIN | Produto | Recebido (abr) | Vendido abr | Vendido mai | Virou EXPIRED (jun) | Devolvido ao vendedor (jul) | Perdido / descartado (ago) |
|---|---|---:|---:|---:|---:|---:|---|
| B0GSX3PTZ7 | Drip Suave 10 un. | 10 | **10** | — | 0 | 0 | — |
| B0GSXB9KC6 | Drip Canela 10 un. | 10 | **10** | — | 0 | 0 | — |
| B0GSH9NBM9 | Drip Clássico 10 un. | 10 | 0 | 9 | 1 | 1 | — |
| B0GSHN4S14 | Kit 30 Clássico | 10 | 0 | 0 | **10** | 8 | 1 perdida · 1 descartada |
| B0GSXD75GS | Kit 30 Suave | 5 | 0 | 2 | 3 | 3 | — |
| B0GSX6N68W | Kit 30 Canela | 5 | 1 | 1 | 3 | 3 | — |
| **Total** | | **50** | **21** | **12** | **17** | **15** | **2** |

### 1.3 Vendas e tráfego

Fonte: Relatórios de negócios › Vendas e tráfego por item filho, períodos 01–30/04/2026, 01–31/05/2026
e 15/10/2025–15/10/2026.

| Período | Sessões | Unidades | Vendas | Observação |
|---|---:|---:|---:|---|
| abril/2026 | 123 | 21 | R$ 727,90 | Suave e Canela 10 un. esgotam |
| maio/2026 | 82 | 12 | R$ 556,80 | Clássico 10 un. vende 9 |
| junho a outubro/2026 | 1 | 0 | R$ 0,00 | estoque vencido / zerado |
| **12 meses** | **206** | **33** | **R$ 1.284,70** | |

Por ASIN, 12 meses: conversão (unidade/sessão) de **34,5%** no Suave 10 un., **20,4%** no Canela 10 un.,
21,4% no Clássico 10 un., 10% no kit 30 Suave, 3,9% no kit 30 Canela e **0%** no kit 30 Clássico
(14 sessões, nenhuma venda). Oferta em destaque de 96,9% a 100% em todos (único vendedor).
Preço implícito: R$ 31,90 o 10 un. e R$ 89,90 o kit 30.

**Diagnóstico**
- O produto **converte** quando tem estoque: 20–34% de unidade por sessão no 10 un. é alto (praticante
  cita 4–5% como conversão de página típica, CONSOLIDADO §3, sem base). O tráfego é que era mínimo
  (206 sessões em um ano, sem Ads).
- A perda não foi por falta de demanda e sim por **lote mal dimensionado e validade curta**: mandou-se
  o mesmo volume para os SKUs que venderam (10 un.) e para os que não venderam (kit 30), não se repôs
  os que esgotaram, e o que sobrou venceu em ~2 meses de prateleira.
- **O kit 30 Clássico** não vendeu nenhuma unidade e respondeu por 10 das 17 perdas.

**Risco de não agir:** repetir o erro no 1 kg, que tem CMV de R$ 47 por unidade: 17 un. de 1 kg
vencidas seriam ~R$ 800 de CMV perdido, mais remoção.

**Próximo passo:** saber a validade impressa no drip e no 1 kg/500 g (pergunta ao Rafael) e dimensionar
o 1º envio de 1 kg por **cobertura curta** (ver §4).

## 2. Saúde da conta (impacto: baixo — está boa)

Fonte: Estado da conta (`/performance/dashboard`), 15/10/2026.

| Métrica | FBA | Envio próprio | Meta |
|---|---|---|---|
| ODR (negativa, A a Z, estorno) | N/A | N/A | < 1% |
| Envio tardio / cancelamento / rastreio válido | — | N/A | < 4% / < 2,5% / > 95% |
| Account Health Rating | **200 — Ideal** | | |
| Violações (PI, autenticidade, condição, segurança de alimento, produto restrito, avaliações, regulatória) | **0** | | |
| Nota de vendedor (home) | 5,0/5 | | |

"N/A" no ODR = nenhum pedido nos últimos 60 dias. Nada a fazer.

## 3. Estoque FBA e validade (impacto: alto, preventivo)

- Hoje: **0 unidade** em todos os estados. Nada envelhecendo, nada a remover.
- Capacidade: 1º recebimento em 01/04/2026 → ~28 semanas de FBA → **sem limite de capacidade** (contas
  com menos de 39 semanas; ajuda G202174810). IPI: *não medido*.
- **Validade é o risco nº 1 desta conta.** O drip foi marcado EXPIRED em junho, ~2 meses depois de
  disponível. A regra: café precisa chegar com **mais de 150 dias** de validade e, a 50 dias do
  vencimento, a unidade sai de venda e não volta (ajuda G201003420). Logo, **a janela útil de venda de
  um lote é (validade na chegada − 50 dias)**. Com 150 dias na chegada, sobram ~100 dias de venda.
- *Não medido:* a validade do drip na chegada (o lote foi aceito, então tinha mais que o mínimo).

## 4. Catálogo dos 1 kg e 500 g (impacto: alto)

- **Na conta: nenhum.** Busca "café canastra" e "café canastra 1kg" na amazon.com.br (15/10/2026,
  ~17h, sessão logada, CEP do comprador não lido): nenhum 1 kg Canastra no catálogo.
- **No catálogo, fora da conta:** **B08LXZ7C41 — "Café Néctar de Minas Café Canastra Moído 500 g"**,
  marca "Café Canastra", **vendido e enviado pela Amazon.com.br (1P)**, R$ 137,00, "sob encomenda",
  nota 5,0 com 1 avaliação.
  - **Diagnóstico:** a Amazon cadastrou (ou alguém cadastrou e a Amazon assumiu) um ASIN com a nossa
    marca. Sem Brand Registry, não controlamos título, imagem nem conteúdo dele, e o preço de R$ 274/kg
    não vende. Se o EAN do 500 g Néctar for o desse ASIN, a nossa oferta tem de entrar **nele**, não num
    ASIN novo (CONSOLIDADO §0).
  - **Próximo passo:** o Rafael confirma se vendeu para a Amazon (Vendor) alguma vez e qual é o EAN do
    Néctar 500 g; eu comparo com o EAN do ASIN (exige abrir a página de detalhes do produto no Seller
    Central, só leitura).
- **Homônimos, não são nossos:** "Café Gourmet Canastra Premium" (B0GDRRKQ7Y, marca ATACARNE, vendido
  por CANASTRA PREMIUM FOODS, R$ 59,90 o 500 g); REI DO CAFÉ e Santa Clara usam "Serra da Canastra" no
  título. Isso dilui a busca por "canastra" — vale para o título e para Ads de marca.

## 5. Brand Registry e marca (impacto: alto)

- **Confirmado: não há conta no Brand Registry.** `brandregistry.amazon.com.br` abre em "Bem-vindo ao
  Cadastro de Marcas da Amazon" com o botão "Revisar os termos e continuar" (não clicado). A home do
  Seller Central recomenda "Cadastre sua marca na Amazon".
- **O que se perde sem ele:** Vine (avaliações para ASIN novo), A+, Store, Sponsored Brands, Brand
  Analytics/SQP, kit virtual, Programe e Poupe, e o controle do ASIN B08LXZ7C41.
- **Requisito:** marca registrada ou com pedido pendente no INPI, aplicada de forma permanente na
  embalagem (ajudas G202130410 e GQCYJTBSFZK8HGN6).
- **Pergunta ao Rafael:** há registro ou protocolo no INPI de "Café Canastra"? De quem é a titularidade?

## 6. Programas e condições (impacto: médio)

| Programa | Estado | Fonte |
|---|---|---|
| Sponsored Products | **nunca ativado**: `/cm` redireciona para o cadastro | Console de anúncios, 15/10/2026 |
| Crédito de Ads para novo vendedor | a página oferece "até US$ 1.000 em créditos … por até 90 dias após listar um produto"; termos em advertising.amazon.com/pt-br/legal/terms-conditions/new-seller-sponsored-products-promotion-2024 (**não lidos**; se a contagem é por produto novo, o 1º 1 kg pode habilitar) | idem |
| Vine | **não inscrito** (página de boas-vindas); exige Brand Registry | `/vine`, 15/10/2026 |
| Experimente FBA 3.0 | conta **não é "nova"** (teve envio FBA em 2026, antes de 31/07); é conta **ativada no FBA antes de 01/04/2026** (envio criado em 23/03). Logo vale a alternativa "+1 p.p. sobre abril/2026" — e o gasto de Ads de abril foi **zero** (nunca houve Ads). **Leitura literal: a meta seria 1% da receita, não 3,5%.** Confirmar o texto dos termos antes de usar | termos, CONSOLIDADO §1 |
| Mais Vantagens / Vantagens | inscrição *não medida* (a página de programas não mostra status) | `/recommended-programs` |
| Comissão de lançamento Prime (5% nas primeiras 100 un.) | *não medido*; um ASIN de 1 kg novo pode se qualificar | /cresca/fba |

## 7. Ads (impacto: médio)

Nunca houve campanha: gasto, ACOS, TACOS e termos = **inexistentes**. Todo o tráfego de 2026 (206
sessões) foi orgânico. Não há base de termos de busca da nossa marca — o 1º mês de Sponsored Products
automática é a forma de criá-la (CONSOLIDADO §2.1).

## 8. Dados de 1ª parte (impacto: médio)

- Business Reports: lidos (§1.3).
- Brand Analytics (SQP, Top Search Terms, Repeat Purchase): **indisponível** sem Brand Registry.
- Product Opportunity Explorer: *não lido* nesta rodada.

## 9. Lucratividade e tarifas (impacto: médio)

- **Tarifa FBA real, conferida na conta:** R$ 5,85 no drip 10 un. (~R$ 31,90) e R$ 12,05 no kit 30
  (~R$ 89,90). Bate com a tabela de `venda.amazon.com.br/precos` ("atualizadas em 01/08/2025"), lida
  célula a célula: **abaixo de R$ 79 a tarifa é fixa por preço, qualquer peso** (R$ 5,65 / 5,85 / 6,05);
  a partir de R$ 79 é por peso (1–1,5 kg: R$ 12,95 / 14,95 / 16,95 / 19,45 / 20,35 nas faixas
  R$ 79–99,99 / 100–119,99 / 120–149,99 / 150–199,99 / 200+). Resolve a pergunta aberta nº 1 do
  CONSOLIDADO §7. Gravado em `amazon/scripts/precificar_amazon.py`.
- Repasses recentes (Painel de pagamentos): R$ 30,31 (28/04), R$ 30,31 (12/05), R$ 48,92 (23/06),
  R$ 7,59 (04/08); saldo −R$ 0,17. Os repasses são separados por bandeira de cartão, por isso a soma
  não fecha com os R$ 1.284,70 vendidos. **Tarifas efetivamente debitadas (comissão, FBA, remoção,
  descarte) e eventual reembolso da unidade perdida: *não medido*** — exige o extrato por grupo de
  pagamento ou o download do relatório de transações (autorização necessária).

## 10. Prateleira de busca (amostra para a estratégia)

15/10/2026 ~17h, sessão logada, CEP do comprador não lido. P = patrocinado, O = orgânico.

**"café em grãos 1kg"** — 26 primeiros: patrocinados nas posições 1–4 e 21–24 (mesmo padrão de 14/10).
Preços de R$ 66 a R$ 129. Exemplos: Hunters 1 kg R$ 94,05 (P, 4,4, 136 aval., +700/mês); Café Italle
1 kg R$ 66,29 (P e O, Escolha da Amazon, +900/mês); Orfeu Clássico 1 kg R$ 129,21 (O, Mais vendido,
4,7); Bororó R$ 74,95 (O, 597 aval., +500/mês); Coffee Mais Super R$ 107,90 (O, 301 aval., +500/mês);
Campos Altos Especial R$ 125,68 (O, +700/mês); Ankara Especial R$ 123,45 (P, 20 aval., +300/mês).
Mediana visual dos especiais/gourmet: **R$ 85–125/kg**.

**"café moído 500g"** — dominado por 3 Corações, Melitta e Pilão a R$ 24–29 (R$ 48–58/kg), nota 4,7–4,8.
Especiais aparecem só no patrocinado (Irmãs Pereira R$ 81,40; um 100% arábica a R$ 42,65 com 117 aval.).
**Diagnóstico:** no 500 g moído, a prateleira orgânica é de café commodity a 1/3 do nosso preço por kg;
o 500 g especial só aparece pago.

---

## Achados priorizados por impacto em dinheiro

| # | Achado | Risco de não agir | Próximo passo |
|---|---|---|---|
| 1 | Validade venceu 34% do único lote (17 de 50) | Repetir no 1 kg (CMV R$ 47/un.) | Validade do 1 kg/500 g; 1º envio por cobertura curta |
| 2 | Sem Brand Registry | Sem Vine, A+, SQP; sem controle do ASIN 1P com a nossa marca | Status no INPI → decidir pedido |
| 3 | Campeões esgotaram em abril e não foram repostos | Perder ranqueamento e a janela de lançamento | Reposição por cobertura com gatilho |
| 4 | ASIN 1P "Café Canastra" a R$ 137 | Concorre com a nossa marca a um preço que queima a percepção | Confirmar EAN e histórico Vendor |
| 5 | Nunca houve Ads | Lançar 1 kg sem tráfego (206 sessões/ano orgânicas) | Desenhar SP automática + Experimente FBA |
| 6 | Experimente FBA: meta pode ser 1%, não 3,5% | Pagar Ads além do necessário ou perder o R$ 6 | Ler os termos e confirmar |

## Perguntas ao Rafael

1. Validade (em dias) impressa no drip, no 1 kg e no 500 g, a partir da torra.
2. A marca "Café Canastra" tem registro ou protocolo no INPI? Em nome de quem?
3. A Canastra já vendeu para a Amazon como fornecedor (Vendor/1P)? O EAN do Néctar de Minas 500 g moído
   é o mesmo do ASIN B08LXZ7C41?
4. "Enviamos estoque ao FBA algumas vezes": a tela mostra 1 envio. Houve outro (cancelado, ou por outra
   conta)?
5. O que foi feito com as 15 unidades devolvidas em julho?
