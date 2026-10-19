# Diagnóstico da conta — 1 kg e 500 g (15/10/2026)

> Lido no painel da conta `CAFECANASTRA` pelo Claude in Chrome em **15/10/2026, entre 14h50 e 15h40**,
> com a janela do Chrome oculta (`visibilityState = hidden`). **Nada foi alterado na conta.**
> Formato de agência: **evidência → diagnóstico → risco de não agir → próximo passo**, em ordem de
> impacto em dinheiro. Cálculos de margem: `mercadolivre/scripts/precificar.py` (`--conferir` OK
> nos 3 anúncios medidos, 15/10). Pesquisa: `pesquisa-marketplaces/mercadolivre/CONSOLIDADO.md`.

---

## 0. Resumo em oito linhas

1. **Reputação vermelha na janela de 365 dias:** envios incorretos **36,61% (26 de 71)**, limite 13%;
   canceladas **2,66% (2 de 75)**, limite 2,5%; reclamações **0%**. O produto agrada, mas o despacho falha.
2. **Os 26 envios incorretos:** 20 são de drip coffee (fev–abr/2026) e 6 do Suave 1 kg (jan, abr,
   mai, jul ×2, 01/09). Eles só saem da janela de 365 dias entre jan e set/2027.
3. **O caminho até o verde que o painel mostra:** "130 envios corretos" e "6 vendas sem cancelar". No
   ritmo atual (2 vendas em 30 dias) isso leva anos. **Amarelo** pede ~40 envios corretos seguidos
   (cálculo na §1).
4. **O único 1 kg ativo é o Suave a R$ 109,90**, que deixa **R$ 3,32 de lucro por venda (3,0%)**. ROAS de
   equilíbrio: **33×**. Não há nenhum anúncio de 500 g.
5. **O gargalo de venda é tráfego:** **30 visitas em 30 dias**, 2 vendas (conversão de 6,7%).
6. **Ads, promoções, cupons e Full Super estão trancados pela cor.** Existe uma campanha criada
   (R$ 25/dia, **ROAS objetivo 4×**, sem nenhum anúncio) que daria prejuízo se fosse ligada.
7. **Full fora desta análise** (decisão do Rafael, 15/10): 1 kg e 500 g ainda não têm Full; o despacho
   segue próprio, e a reputação depende dele.
8. **Pendência cadastral:** "complete os dados da sociedade — exigência do Banco Central" aparece em
   várias telas, com o aviso "para continuar usando a conta como de costume".

---

## 1. Reputação e saúde

**Evidência** (Reputação, 15/10; `/reputacao` e o card do Resumo)

| Métrica (365 d, de 15/10/2025 a hoje) | Conta | Limite verde | Situação |
|---|---:|---:|---|
| Vendas · com envio | 75 · 71 | — | janela de 365 d (60 d exige 101 vendas; há **5** em 60 d) |
| Reclamações | **0%** (0) | 2% | ok |
| Canceladas por você | **2,66%** (2) | 2,5% | afeta a cor |
| Envios incorretos | **36,61%** (26) | 13% | afeta a cor |
| Requisitos 2/4 | "**6** que você não cancelar · **130** envios corretos" | | texto do painel |

Nos últimos 60 dias (Métricas › Atendimento): **5 vendas, 0 problemas**, 0% de canceladas.

**Os 26 envios incorretos por mês e produto** (Detalhe dos envios incorretos, 15/10)

| Mês | 1 kg Suave | Drip | Saem da janela em |
|---|---:|---:|---|
| jan/2026 | 1 | — | jan/2027 |
| fev/2026 | — | 5 | fev/2027 |
| mar/2026 | — | 14 | mar/2027 |
| abr/2026 | 1 | 1 | abr/2027 |
| mai/2026 | 1 | — | mai/2027 |
| jul/2026 | 2 | — | jul/2027 |
| set/2026 | 1 | — | set/2027 |

O de 01/09 tinha despacho previsto para 02/09 às 14:00 e foi postado às 15:22: **1 h 22 min de atraso**.
Todos foram pela **Agência Mercado Livre**.

**Quanto falta por cor** (limites de 365 d, [rep A4]; cálculo meu, só com envios novos corretos):

| Cor | Limite de envios incorretos | Envios corretos a mais |
|---|---:|---:|
| Laranja | 28,5% | 21 |
| Amarelo | 23,5% | 40 |
| Verde | 13% | 130 (bate com o painel) |

**Reputação Protegida (oferta ativa, lida em `/reputacao/beneficio_reputacao`):** garantia de **R$ 250**
(era R$ 75 em 30/09 e R$ 125 em 08/10). Por **60 dias** a conta aparece verde e a Experiência de Compra
fica em 100. A proteção cai com **5 vendas afetadas**, e a devolução da garantia vai de 100% (0 afetadas)
a 80/60/40/20/0%. *Não medido:* se a cor "protegida" libera Ads, promoções, cupom e o desconto de frete
de 50%. A pesquisa diz que os programas "mascaram a cor sem mudá-la" [rep A21, A22], e a
equivalência Benefício × Protegida segue ABERTA [rep §12.1].

**Experiência de compra** do Suave: **65 ("com problemas")**. Qualidade: **86**, com "2 objetivos".

**Diagnóstico.** A cor vermelha vem do despacho pela agência, e nenhum preço, anúncio ou Ads resolve
isso. Com 2 vendas/mês, a diluição natural não chega ao amarelo em prazo útil. O verde por mérito
próprio só viria em 2027, quando os 20 incorretos do drip saírem da janela.

**Risco de não agir.** Cada atraso novo fica 365 dias na conta. Enquanto a cor for vermelha: frete sem
desconto (R$ 34,30 no 1 kg [custos.md]; o verde teria até 50% [rep A15]), Ads impedido, promoções
trancadas e catálogo inacessível.

**Próximo passo.** (a) Prazo de disponibilidade real em todo anúncio, mais um horário de corte interno
para postar antes das 14h. (b) Decidir a Protegida como ponte de 60 dias, sabendo que 5 vendas
afetadas a derrubam. (c) Rotas de despacho que não dependem da agência: coleta (o Full está fora desta análise, §4).

**Hoje, 15/10:** a venda `#2000018985951484` (Suave, de 14/10 às 21:22) tinha prazo na agência às 16:00
e às 15:19 estava "pronta para emitir NF-e". O Rafael foi despachar.

---

## 2. Anúncios de 1 kg e 500 g

**Evidência** (lista de anúncios, 15/10; colunas "A pagar" e "Você recebe")

| ID | Produto | Status | Preço | Tipo | Tarifa | Frete grátis | Recebe | Estoque |
|---|---|---|---:|---|---:|---:|---:|---:|
| `5903454718` | Suave 1 kg grãos | **Ativo** | 109,90 | Clássico | 15,39 | 34,30 | 60,21 | 33 |
| `7791049478` | Clássico 1 kg grãos | Pausado | 109,90 | Clássico | 15,39 | 34,30 | 60,21 | 10 |
| `7791161926` | Néctar Gourmet 1 kg grãos | Pausado | 99,90 | Clássico | 13,99 | **29,50** | 56,41 | 10 |
| `7791312402` | Kit 2 × 1 kg Clássico | Pausado | 219,80 | Clássico | 30,77 | 54,10 | 134,93 | 5 |
| — | **500 g (qualquer)** | **não existe** | | | | | | |

O frete do Néctar mudou de **R$ 28,90 (11/10) para R$ 29,50 (15/10)**: ou a tabela de envio mudou, ou
o valor mudou por outro motivo. Não confirmei a causa. Ele fica abaixo dos R$ 34,30 do Suave porque o
preço R$ 99,90 está numa faixa mais barata da tabela por preço [pre A2].

**Economia unitária** (`precificar.py`, CMV R$ 47 e imposto de 9%, 15/10)

| Anúncio | Preço | Lucro | Margem = ACOS de equilíbrio | ROAS de equilíbrio |
|---|---:|---:|---:|---:|
| Suave/Clássico 1 kg | 109,90 | **3,32** | 3,0% | **33×** |
| Kit 2 × 1 kg | 219,80 | 21,15 | 9,6% | 10,4× |
| (referência) 1 kg a 129,90 | 129,90 | 18,72 | 14,4% | 6,9× |

O Néctar não entra na conta porque o CMV dele **não foi informado** [custos.md].

**Desempenho** (Métricas › Negócio, conta inteira, onde só o Suave está ativo)

| Janela | Visitas | Vendas | Conversão | Vendas brutas |
|---|---:|---:|---:|---:|
| 7 d | 16 | 2 | 12,5% | R$ 220 |
| 30 d | **30** | 2 | **6,7%** | R$ 220 |
| 30 d anteriores | 17 | 3 | 17,7% | R$ 330 |

As recomendações do próprio ML no Resumo são: "crie um vídeo", "mude para Premium" e "adicione mais
preços de atacado" (no Suave).

**Diagnóstico.** A conversão é boa para a faixa de preço (prática de 1,5–5% entre R$ 79 e 250 [rank A39]),
mas a amostra é pequena. O problema é **exposição**: 1 visita por dia. A margem de 3% não paga nenhum
canal de tráfego. A linha de 500 g não existe no ML.

**Risco de não agir.** Vender a R$ 3,32 por venda é trabalhar de graça, e cada despacho ainda arrisca a
reputação.

**Próximo passo.** Decidir preço e portfólio (o 500 g entra?) com a tabela do `precificar.py`, que é a
1ª decisão da estratégia (`18-…`).

---

## 3. Mercado Ads

**Evidência** (Publicidade › Product Ads, 15/10)

- Faixa vermelha: **"Seus anúncios patrocinados não estão sendo exibidos… Sua reputação deve ser de cor
  amarela ou superior."** Isso confirma no painel o requisito escrito [ads A6] para esta conta.
- Existe a **"Campanha 2801"**: orçamento **R$ 25/dia**, **ROAS objetivo 4×**, **0 anúncios patrocinados**,
  diagnóstico "Excelente". Métricas de 30 dias: zero.
- Bônus disponível: R$ 0. Orçamento não compartilhado (exige 2 campanhas ativas).
- Definição de venda atribuída no painel: direta (clicou e comprou o produto) e indireta (clicou e comprou
  outro produto seu).

*Não medido:* janela de atribuição (o painel não mostra), ROAS recomendado e CPC de café (aparecem só
ao montar uma campanha, e não montei).

**Diagnóstico.** Ads está impedido até a cor amarela. A campanha que já existe, com ROAS 4×, gastaria
cerca de R$ 27 por venda a R$ 109,90 (ACOS de 25%) contra R$ 3,32 de margem.

**Risco de não agir.** Se a cor subir e alguém puser o Suave nessa campanha, cada venda atribuída dá
prejuízo de cerca de R$ 24.

**Próximo passo.** Antes de qualquer reputação amarela, reconfigurar ou pausar a 2801 (ação do Rafael).
O ROAS objetivo sai do equilíbrio da tabela da §2.

---

## 4. Full — fora desta análise

**Decisão do Rafael, 15/10/2026:** os produtos de 1 kg e 500 g **ainda não têm Full**, e o Full sai
desta análise. Registro só o que foi lido, para uma rodada futura:

- A conta tem 13 anúncios de cápsula e drip ligados ao Full, todos sem estoque (Gestão de estoque Full).
- `/shipping/inbounds` e Planejamento de envios deram erro em todas as tentativas de 15/10, inclusive
  com a janela visível e depois de o Rafael completar os dados da sociedade. O aviso do Banco Central
  ainda aparecia minutos depois, talvez por atraso de propagação.
- O formulário do Suave não oferece Full em Forma de entrega; a entrada é pelo fluxo de envio.

**Releitura do formulário do Suave em 15/10, ~15h50 (janela visível):** **Prazo de disponibilidade vazio**;
**135 visitas e 18 un vendidas** na vida do anúncio; "Preço para ganhar" e "Ajuste automático de preços"
aparecem **"sem referência"**; atacado com 2 de 5 faixas; **sem vídeo**; 6 fotos; EAN `7892262780034`;
embalagem calculada pelo ML em 29 × 27 × 11 cm e 1,128 kg ("confirme as medidas").

## 5. Análise de mercado (Métricas › Análise da concorrência)

| Aba | O que mostrou (15/10) |
|---|---|
| Ranking | "**0 categorias** · Você não tem vendas nesse período", em out e em set/2026 |
| Tendências | "Ainda não conseguimos mostrar informações das suas categorias porque você **não tem vendas suficientes**". Em outras categorias, Alimentos e Bebidas aparece com **3%** de variação (o texto não traz o sinal) |
| Oportunidades | "Economize **30% na tarifa** ao anunciar produtos da lista". Em Alimentos e Bebidas são **36 produtos**; o único café é **"1 Kg Café 100% Arábica em Grãos Bonuto Torra Média", R$ 80**, de outra marca |

**Requisito exato para liberar o detalhe:** o painel não diz um número; diz só "vendas suficientes". O
R$ 300 × R$ 1.500–2.000 da LACUNAS §1 continua sem confirmação.

**Próximo passo.** A análise de mercado vai vir da prateleira digital (busca observada com protocolo,
método da `estado-da-arte.md` §5) e de tendencias.mercadolivre.com.br, até o painel liberar.

---

## 6. Promoções e cupons

Central de promoções: "**No momento, não é possível oferecer promoções.** Recupere sua reputação verde
ou amarela", com **0 anúncios**. O Resumo marca a **Competitividade de preços como "Boa"**: "tarifa de
venda reduzida em categorias selecionadas" e "acesso a campanhas com investimento do ML". Esses
benefícios são citados mas não podem ser usados com a cor atual. Cupom exige verde [pre A17].

Sem promoção, sobram como alavancas de preço o **preço do anúncio**, o **atacado** (só CNPJ vê, com teto
de repasse de frete) e o preço Pix que a vitrine já mostra (−9% no Suave, 08/10). *Não medido:* quem
banca o Pix.

---

## 7. Preço nos outros canais

| Produto | Loja própria (`loja.cafecanastra.com`, 15/10) | ML |
|---|---:|---:|
| Suave 1 kg grãos | **R$ 109,90** (12x com juros) | R$ 109,90 (vitrine Pix ~R$ 99,90) |
| Clássico 1 kg grãos | **R$ 109,90** | R$ 109,90 (pausado) |
| Suave 500 g moído | **R$ 65,70** | não anunciado |
| Clássico 500 g moído | **R$ 65,70** | não anunciado |
| Néctar de Minas 1 kg | não está na loja | R$ 99,90 (pausado) |

Nenhum preço Pix ou promocional aparece na loja; o frete grátis da loja não foi lido. A Loja Integrada
nova não foi consultada. **Leitura:** hoje o ML **não** é mais caro que a loja própria; no Pix é mais
barato. Qualquer alta de preço no ML (ex.: R$ 129,90) deixa o ML acima da loja, e o risco descrito em
[cases A3; pre A23] é o inverso. *Não medido:* se o ML compara com a loja própria.

---

## 8. Outros achados

- **Pendência no Banco Central:** "Para continuar usando a conta como de costume, complete os dados da
  sociedade." *Não medido:* o que bloqueia e quando. **Alta prioridade, ação do Rafael.**
- Conta: 41 anúncios, 11 "ativos" pelo contador (a lista filtrada mostra só o Suave ativo entre os de
  café; contador de carrossel não é medição, ver lição 14 do `LEIA-ME`), 9 sem dados fiscais e
  1 inativo por descumprir políticas.
- Saldo no Mercado Pago: R$ 0 disponível, R$ 120 a liberar.

---

## 9. Medido × não medido

| Medido em 15/10 | Não medido (como resolver) |
|---|---|
| Cor, 3 métricas e 26 envios incorretos com data | Se a Protegida libera Ads, promoções e o desconto de frete (perguntar ao suporte ou observar depois de ativar) |
| Preço, frete, tarifa e "recebe" dos 4 anúncios de 1 kg | Frete do 500 g (formulário ao criar) |
| Visitas e conversão de 7 e 30 d | Visitas por anúncio (aba Anúncios das métricas; o clique não pegou com a janela oculta) |
| Campanha 2801 e o bloqueio de Ads | ROAS recomendado, CPC e janela de atribuição |
| Full: fora desta análise (§4) | — |
| Promoções trancadas | Calendário da Black Friday na Central |
| Preços da loja própria | Loja Integrada; se o ML compara com ela |
| Painel de mercado bloqueado por vendas | Volume mínimo que libera |
