# Preço e configuração — Suave e Clássico 1 kg em grãos

> **14/10/2026.** Primeira análise com o **CMV real** (`custos.md`: R$ 47 + 9% de imposto).
> Concorrência: pesquisa de **08/10/2026** (588 anúncios, recorte por torra com
> `scripts/analise_1kg_torra.py`). A atualização de hoje pela busca **não rodou**: a janela do
> Chrome estava oculta e a lista não renderiza. Custos do Suave **remedidos hoje** no formulário.
>
> **Nada aqui foi aplicado.** Cada campo precisa da autorização do Rafael.

---

## 1. O diagnóstico: o preço atual não paga a operação

| | Suave `MLB5903454718` (ativo) | Clássico `7791049478` (pausado) |
|---|---|---|
| Preço · tipo · frete | R$ 109,90 · Clássico · grátis | idem |
| Tarifa · frete (medido 14/10) | R$ 15,39 · R$ 34,30 | idem (11/10) |
| Recebe do ML | R$ 60,21 | R$ 60,21 |
| − imposto 9% · − CMV | R$ 9,89 · R$ 47,00 | idem |
| **Lucro por venda** | **R$ 3,32 (3,0%)** | **R$ 3,32** |
| Ponto de equilíbrio | **R$ 105,58** | idem |

O Suave está **R$ 4,32 acima do prejuízo**. Qualquer custo não previsto (devolução, frete de
reenvio, um centavo de Ads) põe a venda no vermelho. **Ads é inviável a esse preço**: o ROAS
de equilíbrio é **33×**.

Estado medido hoje: estoque 34 (era 35 em 08/10 → 1 venda), 126 visitas e 17 unidades no
total, **reputação vermelha** (74 vendas em 365 dias). A garantia da Reputação protegida
subiu para **R$ 250** (R$ 75 em 30/09, R$ 125 em 08/10).

## 2. Onde está o mercado (especial 1 kg em grãos, sem blend)

| Recorte | n | Pix p25 · **mediana** · p75 | Cheio p25 · **mediana** · p75 |
|---|---:|---|---|
| Todos | 48 | 99,90 · **112,50** · 127,56 | 109,90 · **125,01** · 148,90 |
| Torra **média** (vizinho do Suave) | 9 | 101,75 · **113,00** · 119,90 | 117,90 · **129,90** · 137,75 |
| Torra **escura** (vizinho do Clássico) | 9 | 102,90 · **123,99** · 139,90 | 112,90 · **133,99** · 149,90 |

- **Nós estamos no percentil 25:** o Suave é o mais barato da torra média depois do Venturim.
- **Quem vende volume não é o mais barato:** Tamanduá Bandeira R$ 128 cheio (+1.000, com a data
  da torra no título), Tiger R$ 140 (+1.000), Cafeeiro Alto Serra R$ 137,56 (+500), Arrudas
  R$ 115 (+500). A exceção é o Patrick a R$ 103 com 84 pts no título.
- O desconto Pix da vitrine é ~R$ 10 em praticamente todos. Na venda real do Suave o "recebe"
  bateu com o preço cheio (R$ 60,21), então **o desconto Pix não saiu do nosso líquido** nesse
  caso — confirmar numa venda paga por Pix antes de dar como regra.

## 3. A estratégia recomendada

### Preço: R$ 129,90 nos dois, tipo Clássico

| Preço cheio | Vitrine Pix ≈ | Lucro | Margem | Percentil (cheio) | Piso ROAS |
|---:|---:|---:|---:|---:|---:|
| 109,90 (hoje) | 99,90 | 3,32 | 3,0% | 25% | 33× |
| 124,90 | 114,90 | 14,87 | 11,9% | 50% | 8,4× |
| **129,90** | **119,90** | **18,72** | **14,4%** | **54%** | **6,9×** |
| 134,90 | 124,90 | 22,57 | 16,7% | 65% | 6,0× |

**Por que 129,90:** é a mediana exata da torra média (preço cheio) e fica abaixo da mediana da
escura. Cada venda passa a deixar **5,6× mais** que hoje — o volume do Suave pode cair à metade
e o lucro ainda triplica. O Suave vende ~1,2/mês; o risco de perder venda é pequeno perto do
ganho, e a recompra (1 cliente comprou 4 vezes) é de quem já confia no produto.

**Mesmo preço nos dois:** mesma tabela de atacado, mesma família, e o comprador compara torra,
não preço. O Clássico teria espaço para R$ 134,90 (vizinhança escura mais cara), mas nasce sem
venda nem avaliação — não é hora de ser o mais caro da família.

**Alternativa conservadora:** Suave a **R$ 124,90** por 30 dias, medir, e depois 129,90. Só
vale se você quiser proteger o histórico de venda do Suave a qualquer custo.

**Clássico, não Premium:** abaixo de R$ 150, o Premium custaria 5 pontos (lucro R$ 12,23 a
129,90) para oferecer parcelamento que metade dos líderes nesta faixa nem oferece.

### Atacado (só CNPJ vê)

O ML impõe **teto = preço − economia de frete por unidade**. Em 109,90 a economia medida foi
R$ 14,56 (5 un) e R$ 19,17 (10 un). Se ela se mantiver a 129,90:

| Faixa | Teto | Lucro/un | Margem |
|---|---:|---:|---:|
| 5 un | **R$ 115,34** | 22,07 | 19,1% |
| 10 un | **R$ 110,73** | 23,13 | 20,9% |

Proposta: **usar o teto** (link *Aplicar* do balão vermelho). O frete mais baixo faz o atacado
dar **mais** lucro por unidade que o avulso. ⚠ A economia de frete precisa ser **relida no
formulário** depois de trocar o preço.

### Mercado Ads: não agora

A R$ 129,90 o piso é ROAS 6,9× e o alvo 10–12× deixa ~R$ 7,89 por venda — dá para começar,
mas as pré-condições da skill `canastra-ml-ads` falham: **reputação vermelha** e **43% de
envio atrasado** no Suave. Ads em cima disso compra clique caro para uma conta que converte mal.
**Ordem:** preço novo → 30 dias sem "Você atrasou o envio" → Ads de descoberta a R$ 10/dia,
só no Suave (o que tem avaliação).

## 4. Configuração campo a campo

### Suave `MLB5903454718`

| Campo | Hoje | Proposta |
|---|---|---|
| **Preço** | R$ 109,90 | **R$ 129,90** |
| Tipo | Clássico | manter |
| **Atacado 5 un / 10 un** | 99,99 / 94,99 | **teto lido no formulário** (~115,34 / ~110,73) |
| **Prazo de disponibilidade** | vazio | os dias reais de torra + embalagem (você decide o número) — é o remédio para os atrasos |
| **Embalagem de envio** | 29 × 27 × 11 cm, 1,128 kg calculado | medir o pacote real; pode baixar o frete de todos |
| Vídeo | nenhum | vertical ≤ 1 min (objetivo pendente no ML) |
| Título, fotos, ficha | — | manter |

### Clássico `7791049478` (pausado)

| Campo | Hoje | Proposta |
|---|---|---|
| **Preço** | R$ 109,90 | **R$ 129,90** |
| **Atacado** | nenhum | 5 un e 10 un no teto |
| Prazo de disponibilidade | — | o mesmo do Suave |
| Fotos | 3 | completar com os packshots conferidos (`canastra-embalagem`) |
| Status | pausado | **você ativa** quando o despacho estiver resolvido |

### Consequência no Kit 2 kg Clássico `7791312402` (pausado)

A R$ 219,80 ele ficaria **R$ 20 mais barato por quilo** que o avulso novo — ao contrário dos
líderes, que não dão desconto no kit. Opções: R$ 249,90 Premium (lucro 31,83 · 12,7%) ou
R$ 259,80 Premium (38,96 · 15,0%). Fora do escopo desta tarefa; decidir junto com o 1 kg.

## 5. Não verificado

| Item | Como resolver |
|---|---|
| Concorrência de hoje | deixar a janela do Chrome visível e rodar as buscas de novo |
| Economia de frete do atacado a 129,90 | ler no balão do formulário |
| Quem banca o desconto Pix | abrir uma venda paga por Pix e conferir o "recebe" |
| Frete em reputação verde | medir quando mudar de cor |
| Elasticidade: quanto o volume cai a 129,90 | medir 30 dias depois da troca |
