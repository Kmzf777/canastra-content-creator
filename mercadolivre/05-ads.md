# Mercado Ads

> Scripts: [`scripts/ads.py`](scripts/ads.py) · [`scripts/matriz.py`](scripts/matriz.py) (teto de estoque) · [`scripts/teto.py`](scripts/teto.py) (teto de rentabilidade).
> Fontes com canal, data e ID em [`pesquisa/ACHADOS.md`](pesquisa/ACHADOS.md).

---

## Regra central: o orçamento é derivado, nunca escolhido

**Ads = 50% do lucro bruto do volume medido no mês anterior.** Recalcula todo mês.
Sobe sozinho quando a venda sobe.

Foi assim que dois erros meus foram corrigidos: eu dava número fixo (R$ 20/dia) e alvo
fixo (ROAS 7,3×), ambos descolados do volume real.

---

## Os três números de cada anúncio

| Anúncio | Lucro/pedido | Piso — nunca abaixo | Alvo inicial | Sobra no alvo |
|---|---:|---:|---:|---:|
| Caixa 10 · R$ 34,90 | 12,82 | **ROAS 2,8×** | 10–12× | R$ 8,91 a 9,49 |
| **Kit 40 · R$ 139,90** | **45,46** | **ROAS 3,1×** | **10–12×** | **R$ 26,79 a 28,80** |
| Kit 60 · R$ 199,90 | 48,41 | **ROAS 4,1×** | 10–12× | R$ 28,42 a 31,75 |

**Piso** = onde o gasto de Ads consome o lucro inteiro daquela venda.

O Kit 60 a ROAS 4 já sobra **−R$ 1,57** — é o mais sensível, e por isso o último a
receber verba.

### O erro que isso corrige
Eu recomendava **ROAS 7,3×**, derivado de "ACOS = metade da margem". Isso é o **máximo
tolerável**, não o alvo.

> *"Inicialmente eu gosto de colocar 10 para cima. Vou colocar 12 nesse caso."*
> — Fabio Ludke, 10/08/2026, `-javeW5ePCg`

> Contas de cliente rodando **ROAS 15, 19, 20, 25, 26**.
> — Bruno Maciel, 31/08/2026, `72nX2ogs8xE`

---

## Quanto investir

**R$ 10/dia na Fase 1. Não os R$ 60 que o ML sugere por padrão.**

R$ 10/dia é o valor em que **o ponto de equilíbrio coincide com ROAS 4** — os dois caem
em ~15 vendas, o que transforma a decisão numa pergunta só. Ver
[`06-plano-de-escala.md`](06-plano-de-escala.md).

Anúncio novo, sem avaliação e sem selo de vendas, converte mal: é realista esperar
**ROAS 3 a 5 nas primeiras semanas**, não 12.

### Teto por volume — a tabela que corrige a rampa antiga

| Vendas/mês | Lucro bruto | Ads a 50% | Por dia |
|---:|---:|---:|---:|
| 20 | 399 | 199 | **R$ 6,65** |
| 35 | 698 | 349 | **R$ 11,63** |
| 60 | 1.197 | 598 | **R$ 19,94** |
| 100 | 1.994 | 997 | R$ 33,24 |
| 150 | 2.992 | 1.496 | R$ 49,86 |

**R$ 20/dia só se sustenta a partir de ~60 vendas/mês.**

### Por que a rampa antiga não fecha
Eu propunha subir até R$ 150/dia com portões de ROAS ≥ 7. Mas **ROAS 7 a R$ 40/dia
exigiria R$ 8.400 de receita por mês** — acima de todos os cenários realistas deste nicho.
Os portões nunca abririam. A rampa fica em R$ 10–20/dia e o que varia é **por quanto tempo
roda**.

---

## Furar o teto de Ads — os dois tetos

Pergunta do Rafael: *"e se eu quiser passar o teto de ads?"*. A resposta exige separar
**dois tetos diferentes, de naturezas opostas** — eu tratava os dois como um só.

| Teto | O que é | Furar significa | Dá para furar? |
|---|---|---|---|
| **De estoque** (R$ 33/dia com 5 de cada) | Lucro máximo que o lote enviado comporta | Esgotar o anúncio no meio do mês | **Não.** Não se fura — se *levanta*, enviando mais estoque |
| **De rentabilidade** (ROAS 3,28×) | Ponto em que o Ads come o lucro inteiro da venda | Perder dinheiro por venda, de propósito | **Sim** — e às vezes é a decisão certa |

Gastar R$ 80/dia com 5 de cada não é agressividade: é **comprar tráfego para prateleira
vazia**. O estoque acaba no dia 7 e os outros 23 dias compram clique para anúncio que não
pode vender — e, pela regra do Milton P Rabello (27/08, `swCx36qRg0w`), **1 dia pausado =
2 dias de ranqueamento perdidos**. Para subir a verba, sobe o estoque junto.

### O critério para furar o teto de rentabilidade

> **Só se você estiver comprando um ativo, não uma venda.**

Perder R$ 5 numa venda para ganhar R$ 5 de faturamento é queimar dinheiro. Perder R$ 5
para ganhar **avaliação, histórico de ranqueamento ou o status Estrela** é comprar algo
que continua rendendo depois que a campanha parar.

| Ativo | Por que não se compra de outro jeito | Quanto dura |
|---|---|---|
| **Produto Estrela** | Exige ser dos mais vendidos da categoria no Full em 60 dias. Não há atalho | Enquanto mantiver o volume. **Desliga o teto de estoque** |
| **Avaliações** | Só vêm de venda. Anúncio sem avaliação converte abaixo do que vai converter | Permanente |
| **Histórico de ranqueamento** | O algoritmo lê venda acumulada | Acumula e decai devagar |

### Quanto custa comprar o Estrela

Alvo: **60 vendas em 60 dias**. Faturamento R$ 4.929, lucro bruto R$ 1.501, estoque
necessário **11 de cada** (77 unidades, R$ 3.156 de CPV).

| ROAS real | Ads total | Ads/dia | Resultado em 60 dias | Leitura |
|---:|---:|---:|---:|---|
| 5,0× | 986 | 16 | **+515** | o Estrela sai de graça e ainda dá lucro |
| 4,0× | 1.232 | 21 | **+268** | idem |
| 3,28× | 1.503 | 25 | 0 | o ponto de virada |
| **3,0×** | 1.643 | 27 | **−142** | custo irrisório pelo que destrava |
| 2,5× | 1.972 | 33 | −471 | ainda barato |
| **2,0×** | 2.464 | 41 | **−964** | **o limite recomendado** |
| 1,5× | 3.286 | 55 | −1.785 | caro demais — o problema é o anúncio, não a verba |

**Comparação que fecha a conta:** sem Estrela, 300 unidades paradas no Full custam
**R$ 3.663 no mês 7**; com Estrela, **R$ 0** (produto mais vendido não entra na métrica de
estoque antigo — ver [`06-plano-de-escala.md`](06-plano-de-escala.md)). Gastar até
~R$ 1.000 para destravar custo recorrente de milhares é conta que fecha.

### As três condições, antes de começar

| # | Condição | Se não for verdade |
|---:|---|---|
| 1 | **Estoque cobre o volume** que a verba vai gerar | Você esgota e **destrói o ativo que estava comprando**. Pior resultado possível |
| 2 | **Reputação verde** | Clique caro para anúncio que converte mal. O ROAS vem baixo por motivo que verba não conserta |
| 3 | **Stop-loss em reais E em dias** | Sem data de parada, "investimento de entrada" vira sangria permanente |

| Verba reservada | A R$ 40/dia | A R$ 80/dia |
|---:|---:|---:|
| R$ 1.000 | 25 dias | 12 dias |
| **R$ 2.000** | **50 dias** | **25 dias** |
| R$ 3.000 | 75 dias | 38 dias |
| R$ 5.000 | 125 dias | 62 dias |

### Quanto custa perder de propósito

| ROAS | Perde por venda | Em 30 vendas | Em 60 | Em 120 |
|---:|---:|---:|---:|---:|
| 3,00× | R$ 2,37 | 71 | 142 | 285 |
| 2,50× | R$ 7,85 | 235 | 471 | 942 |
| **2,00×** | **R$ 16,07** | 482 | 964 | 1.928 |
| 1,50× | R$ 29,76 | 893 | 1.785 | 3.571 |

**ROAS 2,0× é o piso.** Abaixo disso a perda por venda passa de R$ 16 e o problema deixa
de ser de verba: é o anúncio que não converte. Mais dinheiro num anúncio ruim só descobre
mais rápido, e mais caro, que ele é ruim.

### O limite que nenhuma verba atravessa

**O tamanho do nicho.** Os selos acumulados dos concorrentes de cápsula especial são
+25, +100 e +5. Se a demanda é de dezenas por mês, **nenhum orçamento cria centenas**.
A verba acelera a captura da demanda que existe; não inventa demanda nova.
**Sinal de que bateu nesse teto:** impressões param de crescer mesmo aumentando a verba.

---

## TACOS é a métrica de decisão

- **ACOS** = investimento ÷ receita **atribuída a Ads**
- **TACOS** = investimento ÷ receita **total** (orgânica + paga)

> *"Até 5 a 6% de investimento em publicidade, se for proporcional ao faturamento, tá
> lindo."*
> — Bruno Maciel, 31/08/2026, `72nX2ogs8xE`

| Faturamento total/mês | Ads a 5% | a 6% | Por dia |
|---:|---:|---:|---:|
| R$ 5.000 | 250 | 300 | R$ 8 a 10 |
| R$ 10.000 | 500 | 600 | R$ 16 a 20 |
| R$ 20.000 | 1.000 | 1.200 | R$ 33 a 40 |
| R$ 40.000 | 2.000 | 2.400 | R$ 66 a 80 |

**No lançamento o TACOS vai furar esse teto — e tudo bem.** Ads em lançamento é
**investimento de entrada**: compra review e histórico que não se compram de outro jeito.
Mas precisa de **teto de tempo**, não de infinito. A régua de 5–6% vale depois, quando o
orgânico existir.

**Sinal de alerta:** ACOS caindo com TACOS subindo = o Ads está canibalizando o orgânico,
não criando venda nova. Não escale.

---

## Configuração

| Item | Como deixar | Por quê |
|---|---|---|
| Formato | **Product Ads**, modo automático | Único formato viável hoje |
| **Brand Ads** | **não existe** | Foi extinto, ao menos temporariamente *(Seus Produtos Na Internet, 25/09)* |
| Display autoserviço | não usar | Sem segmentação real em 2026 |
| **Ajuste automático de orçamento** | **desligar** | Evita o ML subir o gasto antes de você ler o resultado *(Fabio Ludke, 10/08)* |
| **Orçamento compartilhado** | **não ativar** | *"A campanha que gasta muito e não dá retorno leva o excedente"* *(Marketfacil, 22/09)* |
| ROAS | **Dinâmico em banda**, se liberado | ROAS fixo perde leilão quando o concorrente fica agressivo |
| Anúncios na campanha | Só o **Kit 40 · 3 Sabores** no início | Concentra histórico de conversão |
| Alterações | **nenhuma por 28 dias** | Qualquer mudança reinicia o aprendizado |

### ROAS dinâmico — função nova
> *"Além do ROAS fixo, ele agora tá colocando o ROAS dinâmico. Ele coloca uma banda — por
> exemplo, foi de 4,8 a 7,2. Se você coloca um ROAS fixo, quando a sua concorrência
> estiver num momento de agressividade, você vai perder mais leilões."*
> — Seus Produtos Na Internet, 25/09/2026, `ZCSkvBUUddI`

Recentíssima; pode não estar liberada em toda conta. Conferir no gerenciador.

Existe também **"ROAS vendas Max"** — prioriza volume sobre retorno. **Não usar agora**:
serve para impulsionar lançamento com margem folgada, que não é o caso.

---

## O que mudou na plataforma e afeta a leitura

Segundo a Marketfacil (22/09, `upVnEGAYiXc`), o Ads mudou de novo:

- Segmentação: de **palavra-chave manual** para **intenção com IA**
- Cobrança: de **CPC** para **CPM**
- Atribuição: era só por clique, **agora conta também visualização**

**Consequência prática: o ROAS relatado vai parecer melhor** que na régua antiga, porque
passa a creditar venda de quem só viu o anúncio. Comparar períodos com cautela — e usar
**TACOS**, que não depende de atribuição, para decidir escala.

---

## Termos a monitorar no relatório de busca

No automático não se escolhe keyword, mas dá para ler o relatório.

| Termo | Expectativa |
|---|---|
| `cafe canastra` · `capsula canastra` | **CPC baixo, conversão alta.** Território livre: terceiros cobram R$ 3,99–5,03/cáp com 5 vendas. Se o CPC vier barato, é a melhor compra do leilão |
| `capsula cafe especial` | Público qualificado, concorrência com Orfeu e Coffee++ |
| `kit capsula cafe` · `capsula 100 unidades` | Intenção de volume |
| `capsula de cafe` | Genérico, 8.402 resultados, dominado por 3 Corações e Nespresso pago. **CPC caro, conversão baixa** — primeiro a cortar ao migrar para manual |
| `capsula compativel nespresso` | Alta intenção, muito disputado por genérico de R$ 1,40/cáp |

---

## Erros a evitar

Mexer em lance antes de 7 dias · pausar campanha bruscamente (esfria o orgânico) ·
editar título de anúncio rodando · tratar ML Ads como Google Ads · confundir ACOS com
TACOS na decisão de escala · subdimensionar orçamento e impedir o aprendizado.

---

## Pré-requisito que atravessa tudo

**Ads só depois do verde.** A conta está com reputação vermelha (37,68% de envios
incorretos). Verba em conta vermelha compra clique caro para um anúncio que converte
mal — e você conclui erroneamente que a demanda não existe.

Ver [`01-situacao-da-conta.md`](01-situacao-da-conta.md).
