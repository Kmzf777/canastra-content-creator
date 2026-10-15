# Shopee Brasil: mapa de conhecimento consolidado

Data da consolidação: 2026-10-14. Plataforma: Shopee (Brasil). Pesquisa neutra sobre como os melhores operam a plataforma. Este mapa não parte da situação de nenhuma empresa e não traz recomendação para nenhuma empresa específica.

## Como ler

**Siglas dos arquivos-fonte** (todos dentro de `pesquisa-marketplaces/shopee/`):

| Sigla | Arquivo |
|---|---|
| ADS | `ads/notas.md` |
| PRE | `preco-promocao/notas.md` |
| LOG | `logistica-estoque/notas.md` |
| RAN | `ranqueamento-anuncio/notas.md` |
| MIX | `produto-mix/notas.md` |
| REP | `reputacao-atendimento/notas.md` |
| ALI | `alimentos-marca-propria/notas.md` |
| CAS | `cases-grandes/notas.md` |
| SOC | `social/notas.md` |
| OBS-L | `observacao/lideres.md` |

A citação "(PRE §2.1)" remete à seção da nota. Ids de vídeo do YouTube aparecem como estão nas notas (ex.: `0oRYednAlHY` = youtube.com/watch?v=0oRYednAlHY). "help 76225" = help.shopee.com.br/portal/4/article/76225.

**Tipos:** [OFICIAL] regra dita pela plataforma · [OFICIAL via terceiro] tela ou artigo oficial mostrado por praticante, sem leitura direta · [PRÁTICA] tática de praticante · [CASE] números de operação (quase todos rebaixados a PRÁTICA por falta de período e base) · [DADO] estudo, relatório ou ferramenta · [OBS] observação direta.

**Escopo:** [REVENDA] revenda, dropshipping, importação · [MARCA] indústria, marca própria · [AMBOS].

**Regra de data:** regra de plataforma anterior a 2026-04-14, ou sem data, leva "(pode estar superada)". Os artigos da Central de Ajuda não mostram data, por isso tudo que vem deles leva essa marca.

**Limite que vale para o mapa inteiro.** Em todas as frentes, a cota de busca na web se esgotou no início, e o Centro de Educação do Vendedor (seller.shopee.com.br/edu) e boa parte da Central de Ajuda não renderizaram sem JavaScript. Por isso a tabela de comissão, a tabela de pontos de penalidade, os critérios do Vendedor Indicado e as taxas do Full **não foram lidos na fonte oficial**. Eles vêm de praticantes que mostraram a tela ([OFICIAL via terceiro]). Na verificação cruzada das notas, só 10 afirmações foram confirmadas contra texto oficial lido e 1 foi contestada em parte; o restante ficou "sem fonte oficial lida", o que não significa que esteja errado. A observação direta (OBS-L) cobriu uma única página de busca ("café em grãos"), interrompida por exigência de login.

---

## 0. A plataforma em uma página

**Modelo.** A Shopee Brasil é um marketplace 3P. Cada vendedor tem anúncio próprio e não há catálogo compartilhado nem buy box documentado: a disputa é anúncio contra anúncio (RAN §2.6; PRE §2.5). A plataforma declara mais de 3 milhões de vendedores brasileiros e 95% das vendas feitas por eles [OFICIAL] `yxG_g8vHZIc`, 2026-08-25 (MIX §1; CAS A20).

**Para onde vai o dinheiro.** No 2T26, a receita core de marketplace da Shopee (comissões e anúncios) cresceu 65,6% a/a, contra 28,4% do GMV, e a receita de logística caiu 9% por mais subsídio de frete [DADO N2] Sea 6-K, 2026-08-11 (CAS §1 item 5; LOG §4). Os números são globais, sem recorte do Brasil. A leitura das notas é convergente: a plataforma subsidia frete e cobra mais por transação e por Ads.

**Como o vendedor paga.** Comissão percentual mais taxa fixa **por item**, em faixas de preço. Desde 2026-10-01, item até R$79,99 paga 20% + R$4,50 e item de R$80 paga 14% + R$16, o que cria um degrau forte em R$79,99/R$80 [OFICIAL via terceiro] (PRE §2.1; MIX §2.3). O frete grátis passou a valer para todos em 2026, com subsídio da Shopee limitado por faixa (PRE §2.2; LOG §2.5). Ads é pré-pago e, em 2026, é configurado por meta de ROAS (GMV Max), não por lance por palavra-chave (ADS §2.2). Campanhas oficiais cobram taxa extra de 2% a 3% sobre todas as vendas da loja no período, segundo praticante com tela (PRE §1 item 8).

**Superfícies de exposição.** Busca com quatro ordenações (Relevância, Mais recente, Vendas Principais e Preço) e filtro só de Vendedores Indicados [OFICIAL] help 76162 e 76198, sem data (RAN §2.1); descoberta ("Você também pode gostar", "Descobertas do Dia"); banners e campanhas do calendário de datas duplas, uma por mês; Shopee Video e Live; afiliados; e Google Ads via Shopee (ADS §2.1, §2.4, §2.5; PRE §1 item 15).

**Portões que decidem quem é visto** (síntese das notas, não regra declarada pela Shopee):

1. **Vendedor Indicado.** Selo e filtro de busca. Perdê-lo tira a loja das campanhas e, segundo praticantes, derruba vendas e Ads (REP §2.4; ADS A24; RAN §3.1 item 6).
2. **Pontos de penalidade.** São contados por trimestre e punem a partir de 3 pontos, com −5% a −30% de visibilidade, perda do Indicado, das campanhas e do frete grátis, e taxa de R$100 a R$1.500 [OFICIAL via terceiro] (REP §2.2).
3. **Conversão do anúncio.** Capa, título, preço dentro da faixa do mercado, selos e avaliações formam o funil impressão → clique → venda, que os praticantes usam para diagnóstico (RAN §3.1).
4. **Economia unitária sob a tarifa.** Ticket, kit e faixa de preço definem se sobra margem para Ads (MIX §2.3; PRE §3.1).
5. **Ads com ROAS-alvo compatível com a margem.** Com alvo acima do que o leilão comporta, a plataforma simplesmente não gasta (ADS §2.3; SOC §1).
6. **Capacidade de expedição e acesso à logística da plataforma.** O Full exige nota da loja >4,5 e ao menos 5 pedidos por dia [OFICIAL] `TUs6QYGqGrw` (LOG §2.2).
7. **Status negociado.** Loja Oficial (por convite) libera Display e outros formatos. O gerente de contas aparece como alavanca, sem critério público (ADS §2.1; CAS §3.2 item 6; ALI §2.3).

**O que a Shopee não publica:** fórmula de ranqueamento, pesos de sinais, benchmark por categoria, share de categoria e efeito medido do Full ou do frete grátis na conversão (RAN §9; LOG §9; MIX §9).

---

## 1. Regras e números que importam

A coluna "Status" diz o grau de verificação: **N1 lida** (confirmada contra página oficial na verificação) · **vídeo oficial** (canal Shopee Brasil, não relido na verificação) · **via terceiro** (tela oficial mostrada por praticante, sem N1 lido) · **N2** (relatório regulatório ou de investidor).

### 1.1 Tarifas e preço

| Regra / número | Valor | Fonte e data | Status | Nota |
|---|---|---|---|---|
| Comissão até R$79,99 | 20% + R$4,50 por item (era R$4 até 2026-09-30) | `hEkVpRw_vNg` 2026-10-13; `9VOoazXt_aE` 2026-09-25; `H_QVxVF7FHs` 2026-09-23 | via terceiro (4 canais concordam) | PRE §2.1; MIX §2.3; CAS §2.1 |
| Comissão a partir de R$80 | R$80–99,99: 14% + R$16; R$100–199,99: 14% + R$20; R$200 ou mais: 14% + R$26 | idem; `Zx8826q-qLk` 2026-05-22 | via terceiro | Faixas desde 2026-03-01 (PRE §2.1) |
| Taxa fixa por item, não por pedido | 3 unidades avulsas pagam 3 taxas | `IYi2eifHqSY`; `hEkVpRw_vNg` | via terceiro | Kit contar como 1 item **não confirmado** (MIX §9 item 2) |
| Taxa efetiva no degrau | 25,6% em R$79,99 e 34,0% em R$80; 42,6% em R$19,90 | cálculo sobre a tabela | depende da linha acima | MIX §2.3; CAS §2.1 |
| Vendedor CPF | +R$3 por item depois de 450 pedidos em 90 dias | `9VOoazXt_aE`; `5j2y3UumtnI` | via terceiro | PRE §2.1 |
| Subsídio Pix (pago pela Shopee) | 5% de R$80 a R$499,99; até 8% a partir de R$500; repasse igual ao vendedor | `hEkVpRw_vNg`; UpSeller-619 2026-02-25 | via terceiro; lado comprador em help 197770 (N1 lida, sem %) | PRE §1 item 6, §10 R6 |
| Spam de preço entre variações | diferença >4x "pode ser" spam; armadilha do acessório | `MfH07p4ZtT4` 2026-08-27 | vídeo oficial | PRE §2.5; RAN §2.3 |
| Desconto enganoso | subir o preço regular e logo descontar é infração | `fqDYuDPJsEg` 2026-09-03 | vídeo oficial | PRE §2.5 |
| Empilhamento de cupons | 1 cupom do vendedor + 1 da Shopee; loja e produto não se combinam | help 76177 (sem data, pode estar superada) | **N1 lida** (parcial) | PRE §10 R10 |
| Taxa de campanha oficial | +2% a 3% sobre todas as vendas da loja; inscrição renova sozinha | `4oQLk8XXYP4` 2026-09-01 | prática com tela, fonte única | PRE §2.4; SOC §2 |
| Full+ | −0,5 a −2 p.p. de comissão em itens ≥R$50 via Full, com ≥40% dos pedidos no Full | `0oRYednAlHY` 2026-08-04 | vídeo oficial | LOG §2.3 |
| Calendário | uma data dupla por mês; 10.10 de 2026 com R$18 milhões em cupons | blog Shopee "datas-duplas" 2026-09-30 | oficial (blog) | PRE §1 item 15 |

### 1.2 Frete e logística

| Regra / número | Valor | Fonte e data | Status | Nota |
|---|---|---|---|---|
| Frete grátis obrigatório | todas as lojas desde 2026 (março ou maio, diverge); extinto o adicional de 6% | `j_2kh6auKiw` 2026-06-04; UpSeller-619 | via terceiro | PRE §2.2; LOG §2.5 |
| Teto do subsídio de frete | R$20 / R$30 / R$40 por faixa de preço | `j_2kh6auKiw`; `9VOoazXt_aE` | via terceiro | Diverge do cupom do comprador (§4) |
| Cupom de frete do comprador | até R$20; 10 por semana; até 3 pacotes por cupom | help 76220 (sem data, pode estar superada) | N1 lida | LOG §10 |
| Requisitos do Full | CNPJ; nota da loja >4,5; ≥5 pedidos/dia; mínimos por item | `TUs6QYGqGrw` 2026-08-04 | vídeo oficial | LOG §2.2 |
| Envio ao CD, item <R$20 | R$1 / R$2,50 / R$6 / R$12,50 por unidade (P/M/G/XG) desde 2026-07-01 | `ty0iwe3dV1I` 2026-07-20 | prática com tela, fonte única | LOG §2.2 |
| DTS (envio próprio) | 2 dias úteis; 7 a 30 dias corridos para pré-encomenda; cancelamento após >7 dias de inatividade | help 76324 (sem data, pode estar superada) | **N1 lida** (parcial) | LOG §10 A11 |
| Perecível nos Pontos logísticos | vencido ou contaminado pode ser descartado na hora; bloqueado >7 dias passa à Shopee | help 124091, 2023-02-16 (pode estar superada) | **N1 lida** | Não se confirmou que vale para o Full atual (LOG §10 A27) |
| Embalagem inadequada recorrente | pode reduzir visibilidade, remover anúncio e gerar penalidade | `9CxujZDsRCw` 2026-10-01 | vídeo oficial | LOG §1 item 14; REP §2.6 |

### 1.3 Reputação e integridade

| Regra / número | Valor | Fonte e data | Status | Nota |
|---|---|---|---|---|
| Pontos de penalidade | trimestre civil; 1–2 pts = aviso; punição a partir de 3 | `ThPsYQpMxJE` 2026-08-05; `LLDUrAuF3qQ` 2026-05-14; UpSeller 946 | via terceiro | REP §2.2 |
| Faixas | 3–5: 14 d, −5%, R$100 · 6–8: 14 d, −10%, sem frete grátis, R$250 · 9–11: 21 d, −20%, R$500 · 12–14: 28 d, −30%, R$1.000 · ≥15: conta congelada 28 d, R$1.500 | idem | via terceiro; R$300/R$600 na UpSeller | REP §2.2 |
| Gatilhos de envio | não envio ≥8% e ≥2 pedidos = 1 pt (≥90 = 2); atraso ≥5% e ≥2 pedidos = 1 pt (≥90 = 2) | `ThPsYQpMxJE` | via terceiro | REP §2.3 |
| Condutas que dão 2 pontos | chat abusivo; levar comprador para fora; pedir que cancele; resposta abusiva a avaliação | `ThPsYQpMxJE` | via terceiro | REP §2.3 |
| Spam de anúncio | termos irrelevantes ou excessivos, preço inexato, duplicados (devem virar variação) | help 76225 (sem data, pode estar superada) | **N1 lida** | RAN §10 A3 |
| Cota de anúncios | muitos pontos por violação de anúncio limitam a cota por 28 dias | help 76225 | **N1 lida**; "reenvio gera pontos extras" foi **contestado** em parte | RAN §10 A4 |
| Avaliações | até 10 moedas por avaliação com imagem e vídeo; inflar a nota de forma não natural é fraude | help 76444, 88798 (sem data) | **N1 lida** | RAN §10 A15 |
| Taxa de resposta do chat | 12 h; últimos 30 dias; fins de semana e feriados contam | `Arwxa4I9DgE` 2026-06-05 | via terceiro | REP §2.5 |
| Vendedor Indicado | entrar: nota >4,5, chat ≥60%, TNC <2%, ≤1 pt, preparo ≤1 dia útil, sábado ≥20%, CNPJ, loja >90 dias; sair: nota <4,2, chat <50%, TNC >3%, ≥3 pts | `8cRhids_rNs` 2026-03-18 | via terceiro (**pode estar superada**) | REP §2.4 |

### 1.4 Ads e anúncio

| Regra / número | Valor | Fonte e data | Status | Nota |
|---|---|---|---|---|
| Formatos | Busca de Produtos, Busca da Loja, Descoberta, Combinados, Display | ads.shopee.com.br (sem data, pode estar superada) | oficial (portal) | ADS §2.1 |
| Cobrança | busca e descoberta por clique; Display por CPM, com reserva de datas | /ad-types/419 e /1414 | **N1 lida** | Diverge de relato de cobrança por impressão (§4) |
| Busca da Loja | automática para vendedores selecionados com bom histórico | /ad-types/421 | **N1 lida** | ADS §10 A4 |
| Display só para Lojas Oficiais | lista de elegíveis | /ad-types/1414 | portal; exclusividade não reapareceu na releitura | ADS §10 A3 |
| Google Ads via Shopee | ≥30 dias ativo; orçamento ±20%; pausa reinicia aprendizado; ≥5 produtos na seleção manual | `BZbrt87EAzs`, `M9Plk5F5144` 2026-07-06 | vídeo oficial, confirmado pelo verificador | ADS §2.4 |
| GMV Max com meta de ROAS; orçamento mínimo R$10/dia; atribuição 7 d clique + 1 d visualização | — | praticantes com tela, 2026-05 a 09 | **sem N1** | ADS §2.2 |
| Título | produto + marca + especificação; 36 primeiros caracteres decisivos no celular | `zSfe4Z0Ukbc` 2026-06-25 | vídeo oficial | RAN §2.3 |
| Capa e vídeo | produto em ~70% da capa, ≥1.000 px; vídeo MP4 de 10 a 60 s, ≤30 MB | `fmcvIUvhE3Q`; `BjlJ3AnBHRM` | vídeo oficial | RAN §2.3 |
| Atributos | EAN/GTIN e registros reais; dado inconsistente leva a remoção permanente | `S03qUnOmvek` 2026-07-23 | vídeo oficial | RAN §2.3 |
| Variação x anúncio novo | cor, tamanho, voltagem e sabor no mesmo anúncio; muda função, proposta ou categoria → anúncio novo | `rcGxXjm76xE` 2026-07-30 | vídeo oficial | MIX §2.2 |

### 1.5 Regulatório, alimentos e mercado

| Regra / número | Valor | Fonte e data | Status | Nota |
|---|---|---|---|---|
| Atributo Anvisa | obrigatório em anúncios novos de 169 categorias desde 2026-09-21; legados "por enquanto" mantidos | `RvJiFGQiK3c` 2026-09-14 (integrador) | via terceiro, **sem N1** | ALI §2.1 |
| Retiradas da Anvisa | alegação de saúde não aprovada em anúncio online é o motivo mais frequente | atos Anvisa 2026-02-06, 03-19, 08-07 | **N2** | ALI §5.2 |
| Fiscalização em CD | Anvisa fiscalizou o estoque Full do ML em Cajamar | Anvisa 2026-03-18 | **N2** (precedente, não Shopee) | ALI §1 item 3 |
| Café torrado | Portaria SDA 570/2022 em vigor desde 2023-01-01; RDC 716/2022, 727/2022, 843/2024 | ABIC (2025) | oficial via ABIC | ALI §2.2 |
| Lojas Oficiais | original com NF; dúvida de autenticidade → reembolso integral em cupom; devolução em 30 dias | blog Shopee "lojas-oficiais" 2026-06-02 | **N1 lida** | ALI §10 R7 |
| Mercado Shopee | foco em não perecíveis; dias temáticos | blog Shopee 2026-06-02 | N1 lida (metade) | ALI §10 R12 |
| Monetização global | GMV 2T26 US$38,3 bi (+28,4%); receita core US$4,3 bi (+65,6%) | Sea 6-K 2026-08-11 | **N2** | CAS §4 |

---

## 2. Por frente: o que os melhores fazem

### 2.1 Ads

**Consenso (três ou mais fontes):**
- **Ads amplifica, não conserta.** O anúncio precisa estar completo (fotos, vídeo, título, ficha), com estoque, e a loja precisa ter o Indicado antes de investir (ADS §3.1 itens 1 e 11; SOC §1; RAN §6).
- **Começar pelos SKUs que já vendem**, ordenados por vendas de 30 dias (ADS §3.1 item 2).
- **Anúncio individual por SKU** para ler o resultado produto a produto. O GMV Max da loja fica para teste ou para a cauda do catálogo (ADS §3.1 item 3; SOC §1, sistema de 3 grupos).
- **Orçamento limitado no início** (R$10 a R$20 por produto), sem recarga automática, e 7 dias sem mexer antes de julgar (ADS §3.1 itens 4 e 5; SOC S06).
- **Ciclo de otimização:** julgar por ACOS/ROAS, diagnosticar CTR (capa, preço, título) e conversão (fotos, vídeo, avaliação), cortar ACOS alto e subir orçamento em passos de 20% a 30% quando o dia é consumido (ADS §3.1 item 6; SOC S07, S10).
- **TACOS-teto embutido no preço.** O valor citado é cerca de 5% (= ROAS 20), e a conta de equilíbrio é ROAS = 1 ÷ margem antes de Ads (ADS §3.4; PRE §3.1; SOC S03).
- **Juntar Ads às ferramentas da central de marketing** (campanhas, cerca de 5% de desconto no catálogo) (ADS §3.1 item 8).

**Combinações vistas nos maiores:** curva C e lançamento com ROAS-alvo baixo, curva A com ROAS alto (MIX §3.5; CAS A25). Na revenda de commodity, quase nenhum Ads em produto de terceiro e verba só na marca própria (ADS §7; CAS A21). Teste em grupo com ROAS 30 e cerca de R$50/dia; o vencedor vai para uma campanha própria (SOC S09).

**Faixa de resultados mostrados:** ROAS semanal de 9 a 19 em contas com tela, TACOS de loja de 3,77% numa conta de R$127 mil/mês. São contas únicas, sem nicho nem base (ADS §4).

### 2.2 Preço e promoção

- **Precificar pela margem de contribuição, item a item.** O preço vem do mercado; o custo só diz se dá para entrar. Custo fixo fica fora do preço unitário (PRE §3.1, consenso de 5 ou mais fontes).
- **Kit e "leve mais por menos" diluem a taxa fixa.** A margem percentual cai um pouco e a margem em reais sobe. O kit é calibrado logo abaixo dos degraus de R$79,99, R$99,99 e R$199,99 (PRE §3.1; MIX §2.3, §3.4).
- **Cupom com cesta mínima** de cerca de 2x o ticket. O cupom de seguidor (2% basta) é tratado como obrigatório (PRE §3.1).
- **Preço cheio calculado, com "gordura" para campanha.** É orientação oficial e também prática (PRE §1 item 12, §3.2).
- **Conciliação do repasse venda a venda via ERP ou API.** Nos grandes, um analista concilia a cada 30 minutos (PRE §3.1; CAS A18).
- **Antes de aderir, calcular a taxa extra de campanha sobre a loja inteira.** O desconto da campanha substitui o do anúncio, não soma (PRE §3.4; SOC S22).
- **Hipóteses de fonte única:** reajustar em lotes de 5 a 7 anúncios a cada 3 ou 4 dias; escada de preço junto com o ROAS a cada patamar de cerca de 15 e 30 vendas (PRE §3.2; SOC S05).

### 2.3 Logística e estoque

- **Full para o que gira.** Item abaixo de R$20 e volumoso fica fora, por causa da taxa de envio por unidade. O desenho do Full+ (desconto só de R$50 para cima) empurra para kit e ticket maior (LOG §3.1 P1, P2).
- **Full como capacidade extra.** Os grandes enviam de 40% a 77% dos pedidos pelo Full (CAS A7; LOG P3).
- **Não vender acima da capacidade de expedição.** O atraso vira ponto, e uma semana ruim basta para chegar a 3 pontos (LOG P4; REP §3.1).
- **Operação de pico pelo checklist oficial:** conferir o estoque físico contra o sistema, pré-embalar os campeões, aplicar FIFO e só nomear em campanha o que tem estoque (LOG §2.6, P5).
- **Filmar ou fotografar a embalagem** para contestar. Isso é recomendação oficial desde 2026-10 e prática antiga dos grandes (LOG P6; REP §3.1).
- **Medida real no cadastro.** A Shopee mede de novo no Full, e dimensão errada gera cobrança divergente (LOG §6).
- **Frete dentro do custo, refeito a cada mudança de regra** (LOG P7).
- **Erros documentados:** fornecedor único; crescer mais rápido que a expedição; promoção mal parametrizada no ERP, que gerou cerca de R$150 mil de ICMS a mais (CAS §6).

### 2.4 Ranqueamento e anúncio

- **Seguir a trilha oficial de 2026:** título com produto + marca + especificação nos 36 primeiros caracteres; capa com ~70% de produto; galeria em sequência (visão geral → detalhe → variações → uso); vídeo de 10 a 60 s; categoria mais específica; atributos opcionais preenchidos com códigos reais (RAN §2.3).
- **Funil como ferramenta de diagnóstico:** exposição → CTR → conversão. A capa ganha a atenção; título, preço dentro da faixa, selos e frete ganham o clique (RAN §3.1).
- **Coerência capa ↔ produto.** Capa enganosa gera devolução e penalidade (RAN §3.1 item 3).
- **Avaliações como bola de neve, dentro da regra:** lembrete oficial "Lembrar compradores de avaliar" com moedas. A taxa observada foi de 55% a 72% das vendas em dois anúncios grandes (RAN A24, A25).
- **Cauda longa no título.** Praticantes dizem que a cauda curta está tomada por Ads (RAN §1 item 13; ADS A23).
- **Escada de tamanhos em anúncios separados** quando o preço passaria de 4x entre variações (RAN §5 item 3; MIX §2.2).
- **Riscos tratados como violação, não como tática:** anúncio duplicado, anúncio "fake" para liberar dados de categoria, EAN inventado, avaliação combinada (RAN §6).

### 2.5 Produto e mix

- **Demanda dentro da Central:** Assistente de vendas (mais vendidos, em alta, similares, palavras-chave), lido toda semana no mesmo dia, de baixo para cima, para pegar o "pré-pico" (MIX §2.1, §3.7).
- **"Vendidos" é acumulado.** É preciso dividir pela idade do anúncio (MIX §1 item 3).
- **Teste de entrada na 1ª página (60 anúncios):** demanda de 30 dias, perfil dos concorrentes (oficiais, indicados, internacionais, com vídeo) e margem ao empatar com o preço de referência (MIX §3.2).
- **Corte de SKU pela margem depois do Ads.** As saídas são absorver, reajustar, virar kit ou sair do portfólio (MIX §3.5).
- **Catálogo curto com volume alto é possível:** cerca de 30 SKUs numa fábrica de 6 mil pedidos/dia. A faixa observada vai de 30 a 330 SKUs ativos (MIX §3.8).
- **Reposição** pela venda de 30 dias com projeção de 30, 60 e 90 dias (MIX §3.5).
- **Risco de concentração:** 90% a 95% do volume em uma marca de terceiro levou a migração forçada (MIX §3.8; CAS §6).

### 2.6 Reputação e atendimento

- **Tratar a régua do Indicado como meta operacional,** porque é mais apertada que a de pontos: TNC <2–3% contra 8%, preparo ≤1 dia, chat ≥60% (REP §4).
- **Unidade de controle semanal.** A punição chega na semana seguinte (REP §2.1).
- **Nunca pedir ao comprador que cancele:** dá 2 pontos, mais que o próprio não envio (REP §3.1).
- **Chat configurado antes do volume** (saudação, atalhos, perguntas frequentes), com grupos por pré-venda, pós-venda e devolução, e a descrição reescrita a partir das perguntas (REP §3.1).
- **Devolução lida por anúncio** em Diagnóstico do produto > Alta taxa de devolução, com correção da causa: conferência, produto ou expectativa (REP §3.1).
- **Responder todas as avaliações** com modelos por estrela; resolver atraso com explicação, sem condicionar benefício à avaliação (REP §3.2).

### 2.7 Alimentos e marca própria

- **Regularizar antes de anunciar e nunca prometer saúde** no título, na descrição, no vídeo ou na live (ALI §3.1 item 1).
- **Escada de tamanhos e kits** (250g a 3kg; degustação 5x50g; kit de origens) (ALI §3.1 item 2; OBS-L).
- **Título que vende atributo:** espécie, torra, notas, pontuação SCA, variedade, "moído no dia do envio" (ALI §3.1 item 3; OBS-L).
- **Marca e EAN próprios** como barreira; denúncia ativa de falsificação (ALI §3.1 item 4; RAN §7).
- **Qualidade de expedição antes de escalar** (ALI §3.1).

### 2.8 Cases grandes

As oito operações descritas (Inova, Dourá, TNT, Na Web, Hugo, Vital, Vizzela, Jonas) têm números autodeclarados, rebaixados a [PRÁTICA] C (CAS §3.1). Padrões:
- a Shopee pesa como canal principal em alguns casos (80% a 95%) e empata ou perde para o ML em outros;
- equipes enxutas, com R$200 a 290 mil por pessoa por mês;
- Full alto;
- live rara, mas forte quando há apresentador;
- gerente de contas sem critério conhecido;
- preço igual entre canais por pressão do ML;
- linha ou marca exclusiva por canal;
- o dono olha caixa e conciliação antes de vendas (CAS §3.2 a §3.4).

As quebras documentadas vêm de expedição, fornecedor único e configuração fiscal, não de demanda (CAS §6).

---

## 3. Benchmarks de referência

**Não há benchmark público por categoria na Shopee Brasil** de CPC, CTR, CVR, ACOS, TACOS, devolução ou tempo de resposta (ADS §9; RAN §9; REP §9). Todos os números abaixo vêm de contas únicas ou de regras descritas por terceiros. Usar como faixa de ordem de grandeza, nunca como média.

| Métrica | Faixa | Base / contexto | Fonte (nota) | Tipo, confiança |
|---|---|---|---|---|
| ROAS de equilíbrio | 1 ÷ margem antes de Ads (margem 15% → ROAS 6,7) | método | ADS §3.4 | método, B |
| ROAS entregue (contas com tela) | 9 a 19; ~10 em 3 meses | contas únicas, sem nicho; parte com conflito de interesse | ADS §4 | PRÁTICA, C |
| ROAS do GMV Max automático | 3,9 a 8 | estimativas de painel e relatos | ADS §3.2; RAN §4 | PRÁTICA, C |
| ROAS em produto saturado | ~6, mesmo pedindo 10 a 20 | relato sem tela | RAN A34 | PRÁTICA, C |
| ROAS-alvo por fase | <5 (novo) a ~10 (já vende); entrada em 30 e descida | divergente | ADS §3.2 | PRÁTICA, C |
| TACOS de loja | 3,77% real; meta <4% | uma conta, R$127 mil/mês | ADS A18 | PRÁTICA, C |
| TACOS embutido no preço | ~5% (= ROAS 20) | método de praticantes | PRE A34 | PRÁTICA, B |
| Custo real de Ads com ROAS sugerido | 17% a 25,6% da receita atribuída | conta sobre ROAS 3,9 a 5,9 | SOC S03 | método, B |
| ACOS de produto | alvo de ~4–5%; alerta acima de 6–8% | uma conta | ADS §4 | PRÁTICA, C |
| CTR | 2% a 5% "muito bom"; alunos de 1,5–2% para 5–8% | sem base | RAN §4 | PRÁTICA, C (não usar como meta) |
| Conversão | 4% a 6% "muito bom" | sem base | RAN §4 | PRÁTICA, C |
| "Produto bom" para Ads (oficial) | ROAS >7–10, >10 vendas, >100 visualizações; "bom ROAS" >2 | portal Ads, sem data (pode estar superada) | MIX §2.4 | OFICIAL, B |
| Taxa efetiva de tarifa | 19,2% (R$499,99) a 42,6% (R$19,90); 34% em R$80 | cálculo | MIX §2.3 | cálculo |
| Margem mínima citada | bruta ≥25–30% / MC ≥20% / MC pós-Ads 12–15% | bases diferentes | PRE §3.3; MIX §3.2 | PRÁTICA, C |
| Margem pós-Ads (exemplo) | ~9%, contra 23% antes de Ads | um painel | PRE §3.1; MIX §3.5 | PRÁTICA, C |
| Margem líquida da revenda de commodity | 5–6% (meses fracos) a 12–14% (com rebate) | um case | CAS A16 | PRÁTICA, C |
| Markup da revenda nacional | 1,9x a 2,1x o custo | contexto ML | PRE §4; CAS §4 | PRÁTICA, C |
| Capital de giro | ~R$0,5 mi por R$1 mi vendido | um case | CAS §4 | PRÁTICA, C |
| Pedidos via Full nos grandes | 40% a 77% | três cases | CAS A7 | PRÁTICA, C |
| Cobertura de estoque-alvo | 60 dias, em vez de 90 (curva A) | um case de fábrica | MIX §3.5 | PRÁTICA, C |
| Reposição | só escalar se a reposição diária superar a venda diária | regra de mentor | CAS §6 | PRÁTICA, C |
| Devolução | 0,7% a 1% das vendas (ferramentas, multicanal); "15–20%" em moda sem base | cases | REP N26; MIX §4 | PRÁTICA, C |
| Taxa de avaliação | 55% a 72% das vendas | dois anúncios grandes | RAN A25 | OBS de praticante, C |
| Recompra | 3% (moda, loja própria); pet "extremamente grande" | uma conta | MIX §3.6 | PRÁTICA, C |
| Faturamento por pessoa | R$200 a 290 mil/mês | revenda e importação | CAS A15 | PRÁTICA, C |
| SKUs ativos | 30 a 330 em operações de milhões/mês | heterogêneo | MIX §3.8 | PRÁTICA, C |
| Gasto de Ads na precificação | 5% fixo (Mamba) | um praticante | ADS §4 | PRÁTICA, C |
| Café em grãos, preço por kg | ~R$67 a R$114/kg; degustação R$311/kg | uma página de busca | OBS-L | OBS, C |

Benchmarks de EUA e Amazon (Pacvue, Jungle Scout) não foram coletados e ficam fora deste mapa (ADS §4).

---

## 4. Divergências entre fontes e como resolver na prática

| # | Tema | Posição A | Posição B | O que medir para resolver |
|---|---|---|---|---|
| D1 | Cobrança do Shopee Ads | Por clique em busca e descoberta; CPM só no Display (portal oficial, N1 lida; ADS §2.1, §6) | Por impressão desde 2026-05-07 (dois praticantes; RAN A18) | Ler no extrato e no relatório de cada campanha se o custo acompanha impressões ou cliques; achar a página oficial de faturamento |
| D2 | ROAS-alvo inicial | Começar alto (30) e descer a cada 2–3 dias (ADS §3.2) | Começar baixo (<5 ou "baixinho") e subir com as vendas (ADS §3.2; SOC S04) | Teste pareado em SKUs comparáveis, com a mesma janela de 7 dias, medindo margem pós-Ads e vendas totais do SKU, não só ROAS direto |
| D3 | Ads antes ou depois do orgânico | Sem Ads não sai a 1ª venda (SOC S15) | Ads só após 4–5 dias de venda orgânica (RAN §3.3) | Holdout: lançar lotes de SKUs com e sem Ads e comparar tempo até N avaliações e posição |
| D4 | Lance manual por palavra-chave em 2026 | O portal oficial ainda o descreve (/ad-types/419) | Os painéis de 2026 mostram só GMV Max (ADS §9 item 5) | Conferir no painel da própria conta quais métodos aparecem |
| D5 | Incrementalidade do Ads | "Orgânico melhora com Ads" (ADS §6) | Ninguém mostrou teste de pausa; o ROAS "não direto" mistura vendas orgânicas (ADS §1 item 13) | Pausa controlada por SKU ou por semana; comparar ROAS direto com venda total do SKU |
| D6 | Taxas das faixas 2 e 3 de penalidade | R$250 / R$500 (duas telas; REP §2.2) | R$300 / R$600 (UpSeller) | Ler a política oficial no Centro de Educação com navegador |
| D7 | Gatilho de atraso | <5% (tela) | "8%" na fala do mesmo autor (REP §3.3) | Tratar 5% como teto operacional até a leitura do N1 |
| D8 | TNC do Indicado | <2% para entrar e <3% para manter (card de mar/2026) | Só "<8%" (tela de mai/2026) | Provavelmente são réguas diferentes; monitorar as duas toda semana |
| D9 | Teto do frete grátis | R$20/30/40 por faixa (lado vendedor; LOG D3) | Teto de R$20 no cupom (help 76220, lado comprador) | Comparar, no extrato de pedidos por faixa, quanto a Shopee cobriu |
| D10 | Data do frete grátis obrigatório | Março de 2026 (`j_2kh6auKiw`) | Maio de 2026 (UpSeller-619) | Irrelevante para a operação atual; registrar a data oficial |
| D11 | Custo do Full | Envio e armazenagem grátis (abr/2026) | Taxa por unidade abaixo de R$20 (jul/2026); armazenagem sem tabela (LOG D2) | Ler a tabela atual; acompanhar se aparece cobrança por idade de estoque |
| D12 | Rede de CDs do Full | Uma tela mostrou um só CD disponível (LOG §9 item 7) | Blog oficial: 5 CDs de fulfillment (SP, PE, GO, RS, MG) em 2026-05 (ALI §2.5) | Ver no fluxo de envio quais CDs a conta pode escolher |
| D13 | Full melhora ranking ou reputação | "Mais relevância" (praticantes, texto do painel) | Sem medição; relatos de atraso e perda no CD de SP (LOG D1, D4) | Comparar conversão e posição do mesmo SKU antes e depois do Full, com controle de preço |
| D14 | Loja Oficial | Por convite; "não vejo vantagem" (2022) | Por proposta ao gerente; "+30% num dia" (2026) (ALI §3.2; CAS §2.7) | Sem página de critérios; o efeito precisa de antes e depois com base |
| D15 | Garantia da Loja Oficial | "2x o dinheiro de volta" (2024) | Reembolso integral em cupom (blog oficial 2026, N1 lida) | Prevalece o oficial de 2026 |
| D16 | Repassar ou absorver a taxa | Repassar ao preço (PRE §3.3) | Decidir item a item porque "quem dá preço é o mercado" | Elasticidade por SKU: vendas antes e depois do reajuste, com Ads constante |
| D17 | Experiência de compra conta arrependimento | Praticante diz que conta tudo (REP §3.3) | Sem N1 sobre exclusões | Cruzar o motivo das devoluções com a métrica do painel |
| D18 | Kit paga uma taxa fixa só | Praticantes assumem que sim (MIX §9) | Sem confirmação oficial | Conferir no extrato de um pedido de kit |
| D19 | Punição por reclamação | "Zera a exposição por 21 dias" (fabricante) | Tabela: −20% e 21 dias na faixa 9–11 (ALI §3.2) | Prevalece a tabela; registrar se houver régua separada de experiência de compra |
| D20 | GMV da Shopee no Brasil em 2024 | ~R$30 bi (Statista via Bling) | ~R$60 bi (Exame via Bling) (MIX §4) | Usar faixa; a Sea não abre o número do Brasil |
| D21 | Margem mínima | Bruta ≥25–30% | MC pós-Ads 12–15% (PRE §3.3) | Padronizar a escada CM1 → CM2 (pós-Ads) → CM3 antes de comparar |
| D22 | Impulsão rápida | Desligar (maioria; ADS §3.2) | Ligar nos 3 primeiros dias (SOC §1) | Teste A/B por SKU; medir custo por pedido nos 7 dias |

**Princípio que atravessa as divergências:** quase nenhuma fonte de praticante mostra período, base e nicho ao mesmo tempo, e nenhuma usa grupo de controle (ADS §6; RAN §3.3). A resolução prática, para quem desenhar agentes, é sempre a mesma: registrar uma linha de base, mudar uma variável por vez e medir margem e vendas totais do SKU, não só a métrica de atribuição do painel.

---

## 5. Indústria/marca própria x revenda: onde a plataforma favorece cada um

### 5.1 O que favorece indústria e marca própria [MARCA]

- **Formatos e vitrines reservados.** Display e "Expandir Branding" são para Lojas Oficiais. Busca da Loja é para vendedores selecionados com histórico. A vitrine e o filtro de Lojas Oficiais, os cupons exclusivos, o Festival Lojas Oficiais no 10.10 e a devolução estendida também (ADS §7; PRE §7; ALI §2.3).
- **Convite de Loja Oficial** hoje prioriza "marcas e fabricantes", segundo praticantes (ALI §2.3).
- **Margem de fábrica comporta o ROAS-alvo baixo do GMV Max.** Praticantes dizem que, com margem de revenda, os ROAS sugeridos dão prejuízo (SOC S30; ADS §7).
- **Controle de atributos e registros:** marca, EAN próprio, Anvisa e Inmetro reais. A Shopee pune código inventado (RAN §7).
- **Kits e tamanhos exclusivos por canal** diluem a taxa fixa sem guerra de preço par a par (PRE §7; MIX §3.4).
- **Ads concentrado na própria marca:** o anúncio da marca acumula avaliações no mesmo lugar (CAS §7; ALI §7).

**Custos específicos da marca:**
- carga fiscal maior no Full (regra fiscal por produto, ICMS por UF, quatro tipos de NF);
- responsabilidade por validade e alegação no rótulo e no anúncio;
- falsificação: 604 anúncios em duas semanas num case;
- derrubada de anúncio fora da política comercial leva cerca de 20 dias na Shopee, contra cerca de 3 no ML;
- conflito com distribuidores e varejo físico, que leva marcas a evitar desconto profundo.

Fontes: LOG §5, §7; CAS A17; PRE §3.2.

### 5.2 O que favorece revenda e importação [REVENDA]

- **Ferramentas nativas de promoção sem Ads** ("leve mais por menos", cupom, preço de/por) sustentam operações grandes de revenda (CAS A21).
- **Rebates e verbas** de fabricante e de marketplace: "varejo ganha na compra" (CAS §7).
- **Velocidade de sortimento:** hype, feiras e importação com estoque curto (MIX §7).

**Riscos e custos específicos da revenda:**
- concorrência no mesmo produto, decidida por capa, preço dentro da faixa, frete, selo e avaliações;
- margem de 5% a 14%;
- fornecedor único que corta o abastecimento quando a revenda cresce;
- dropshipping sem acesso ao Full;
- teto de 20% de pré-encomenda;
- DTS de 2 dias úteis;
- item barato abaixo de R$20, que sofre com a taxa fixa e com o envio por unidade ao CD;
- importação informal, que gerou multas e bloqueios.

Fontes: RAN §7; CAS §6, §7; LOG §7; REP §7.

### 5.3 O que vale para os dois [AMBOS]

Tabela de tarifas e degraus; frete grátis obrigatório; pontos e Indicado; regras de título, capa, variação e spam de preço; ROAS de equilíbrio e TACOS-teto; conciliação venda a venda; capacidade de expedição como teto de escala (todas as notas, seções 7).

---

## 6. Alimentos e café: regras e oportunidades específicas

### 6.1 Regras

1. **Atributo Anvisa** obrigatório em anúncios novos de 169 categorias desde 2026-09-21. **Não se sabe se café, chá, cápsula e suplemento estão na lista** [OFICIAL via terceiro, C] (ALI §2.1; RAN §5).
2. **Alegação de saúde é o principal gatilho de retirada.** A Anvisa age sobre o anúncio online onde quer que esteja, e em 2026 abriu revisão das normas de propaganda de alimentos citando marketplaces e influenciadores [N2, A] (ALI §5.2).
3. **Café torrado:** Portaria SDA 570/2022 (classificação e rotulagem, com declaração de arábica ou canéfora), RDC 716/2022 e RDC 727/2022; tabela nutricional não obrigatória para café [oficial via ABIC] (ALI §2.2).
4. **Elegibilidade:** alimento precisa ser embalado ou selado; frescos, caseiros e laticínios não pasteurizados são proibidos na política da Shopee Video [OFICIAL] help 188364, sem data (RAN §5). Medicamento é proibido, inclusive "natural"; suplemento é para vendedores selecionados (LOG §5; ALI §2.1).
5. **Perecível na logística:** o vendedor responde pela validade. Item vencido ou contaminado pode ser descartado sem indenização e item bloqueado por mais de 7 dias passa à Shopee [OFICIAL, N1 lida, termos de 2023, pode estar superada] (LOG §5). **Validade mínima no recebimento do Full, lote, FEFO e temperatura: sem evidência** (LOG §9; ALI §9).
6. **Promoção bloqueada** só para leite em pó e comida de bebê; não há restrição equivalente achada para café ou alimentos em geral (PRE §2.4). Em Ads, fórmulas infantis, mamadeiras e suplementos aparecem como proibidos [via terceiro, 2025, pode estar superada] (ADS §2.6).
7. **Vídeo:** sabor diferente entre o vídeo e o link é "irrelevante" e gera penalidade. Promessa de cura ou resultado gera alerta (RAN §5 itens 4 e 5).
8. **Spam de preço x escada de peso:** variações 250g → 3kg com preço proporcional passam de 4x. Por isso os líderes separam tamanhos em anúncios próprios. Isso é inferência, não regra declarada para alimentos (RAN §5 item 3; MIX §5).

### 6.2 Economia unitária no ticket baixo

- **Pacote de 250g a 500g na faixa de R$20 a R$40** paga de 31% a 43% de comissão mais taxa fixa, antes de frete, imposto e Ads [cálculo] (CAS §5; PRE §5).
- **Pacote de 1kg logo abaixo de R$80** fica na faixa de 20% + R$4,50, sem subsídio Pix. Acima de R$80, a taxa fixa sobe para R$16 e o Pix passa a ser subsidiado (PRE §5).
- **Item abaixo de R$20 no Full** paga envio por unidade, com mínimo de 15 unidades na tela observada (ALI §1 item 12).
- **Recompra:** não há assinatura oficial nem compra programada para o comprador. As ferramentas de recompra são cupons (de seguidor, para compradores específicos, de live) e moedas. O ShopeeVIP (R$9,90/mês) é um clube de cupons do comprador (ALI §5.6).

### 6.3 O que a prateleira de café mostra [OBS, uma página, 2026-10-14]

- Lojas Oficiais de marca no topo (Italle 1ª, também líder no ML; Baggio com Full e Oficial).
- Torrefadores pequenos de MG e SP no top 40, com UF no card e especiais de 84 pontos acima de R$100/kg no top 20.
- Escada de tamanhos de 250g a 3kg; kit degustação 5x50g e kit de origens.
- Títulos com atributos separados por barras; preço riscado (−5% a −56%) e "no Pix" em quase todos; selo Indicado em muitos vendedores menores; vídeo na maioria dos cards.
- A amostra sugere prateleira menos concentrada que a do ML, mas sem dados de vendidos.

Fontes: OBS-L; SOC "Observação dos líderes"; MIX §5.

### 6.4 Contexto de demanda [DADO]

- Marketplace como principal local de compra de café passou de 0,8% (2023) para 3,5% (2025). Supermercado tem 63,1%, site do fabricante 1,1% e clube de café 0,6% [ABIC 2025, n = 4.032] (ALI §1 item 6).
- 48% dos consumidores não sabem a diferença entre estilos de café; especial é 11% das compras declaradas (ALI §5.3).
- O Mercado Shopee declara foco em não perecíveis, com dia de mercearia às quartas (ALI §2.4).

### 6.5 Oportunidades estruturais que as fontes apontam (sem recomendação)

- Canal pequeno e em crescimento rápido para café.
- Prateleira com espaço para torrefações pequenas ao lado de marcas oficiais.
- Formato de kit e escada de tamanhos que dilui a taxa fixa.
- Atributo e conteúdo como diferenciação num público que não lê estilo.
- Formatos de marca (Loja Oficial, Display) inacessíveis à revenda comum.

Fontes: ALI §3.1, §5.3; OBS-L; ADS §5.

---

## 7. Perguntas abertas para a fase de estratégia

**Regra oficial a confirmar no N1, com navegador e sem login de terceiros:**

1. A tabela de comissão de 2026-10-01 está como os praticantes mostram? O kit paga uma taxa fixa só? A regra de item abaixo de R$8 existe? (PRE §9; MIX §9)
2. Qual é a política oficial de pontos? Quais são as taxas das faixas 2 e 3, qual é o gatilho de atraso e existe isenção abaixo de R$2.500 de GMV? (REP §9)
3. Quais são os critérios atuais do Vendedor Indicado, que só aparecem num card de mar/2026? (REP §9)
4. O Ads cobra por clique ou por impressão em 2026? Ainda existe lance por palavra-chave? Qual é a atribuição oficial? (ADS §9; RAN §9)
5. Existe cobrança de armazenagem ou de estoque antigo no Full? Quais são as faixas P/M/G/XG, a multa por medida errada e os CDs disponíveis por região? (LOG §9)
6. A planilha das 169 categorias com atributo Anvisa inclui café, chá, cápsula e suplemento? Que número a Shopee aceita para café dispensado de registro? (ALI §9)
7. Há regras de alimento no Full: validade mínima no recebimento, lote, FEFO, descarte, categorias aceitas? (LOG §9; ALI §9)
8. Quais são os critérios e benefícios mensuráveis da Loja Oficial, e existe programa de associação de marca (help 182821) equivalente a Brand Registry? (ALI §9; RAN §5)

**Efeitos que ninguém mediu:**

9. Quanto o selo Full, o frete grátis, o Indicado e a Loja Oficial mudam a conversão e a posição de um mesmo SKU? (LOG §9; RAN §9)
10. Qual é a incrementalidade real do Ads na Shopee, quanto do ROAS "não direto" é orgânico e como fica o orgânico depois de uma pausa? (ADS §9)
11. Quanto tempo um anúncio novo leva para ganhar posição, e quanto tempo leva para recuperar depois de uma ruptura? (RAN §3.4; LOG §9)
12. Qual é o efeito de promoção e de data dupla, separando o subsídio da plataforma do desconto do vendedor? (PRE §9)
13. Qual é a recompra de alimentos e café na Shopee e que formato (unidade, kit, tamanho) recompra mais? (ALI §9; MIX §9)

**Estrutura de mercado sem dado público:**

14. Qual é a concentração por categoria (top 3 a 5) e quem lidera café, com vendidos e evolução em 12 meses? (MIX §3.3; CAS §9)
15. Quais são os benchmarks por categoria de CTR, CVR, ACOS, devolução e tempo de resposta na Shopee Brasil? Nubimetrics, Avantpro, Neotrust e NIQ Ebit não foram acessados. (ADS §9; REP §9)
16. Qual é o peso do Brasil na Shopee (GMV, Ads, VIP)? Os relatórios da Sea não abrem o país. (CAS §9)

**Desenho operacional:**

17. Que régua interna usar como meta: a do Indicado ou a de pontos? E com que folga semanal? (REP §4)
18. Como conciliar o preço igual entre canais (pressão do ML) com kits e tamanhos exclusivos por canal? (CAS A27, A28)
19. Que métrica de margem os agentes devem otimizar, dado que as fontes misturam margem bruta, MC e MC pós-Ads? (PRE §3.3)
20. Como a taxa de campanha (2–3% sobre a loja inteira) e a renovação automática entram na decisão de aderir a cada data dupla? (PRE §1 item 8)
