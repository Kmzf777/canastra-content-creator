# Shopee Brasil: logística, frete e estoque

Frente: logistica-estoque · Plataforma: Shopee (Brasil) · Data da nota: 2026-10-14/15 · Analista da frente

**Como ler esta nota**

- **Tipos:** [OFICIAL], [OFICIAL via terceiro], [PRÁTICA], [CASE], [DADO], [OBS].
- **Confiança:** A (alta), B (média), C (baixa).
- **Escopo:** [REVENDA] = revenda, dropshipping e importação. [MARCA] = indústria e marca própria. [AMBOS] = vale para os dois.
- **Data:** toda regra de plataforma anterior a 2026-04-14, ou sem data publicada, leva "(pode estar superada)".
- **Artigos da central de ajuda** (help.shopee.com.br): não mostram data de publicação. Foram lidos em 2026-10-15 pela API pública da própria central e são citados pelo id do artigo. Por isso todos levam "(pode estar superada)". Valem como regra vigente na data de acesso, mas sem data de origem.
- **Limitações de método:**
  - O orçamento de WebSearch da rodada estava esgotado.
  - O Centro de Educação do Vendedor (seller.shopee.com.br/edu) é uma SPA e a API dele recusou a leitura. As tabelas oficiais do Full (taxas, dimensões, termos) **não foram lidas direto na fonte**. Elas aparecem aqui como [OFICIAL via vídeo oficial] ou [OFICIAL via terceiro] com tela.
- **ML e Amazon:** esta nota é da Shopee. Mercado Livre (Full, Flex, coleta) e Amazon (FBA, DBA, FBM) aparecem só quando uma fonte da Shopee faz a comparação. As regras deles estão nas notas das pastas `mercadolivre/` e `amazon/`.

---

## 1. Resumo executivo

1. **Full Shopee é o fulfillment da plataforma.** A Shopee armazena, embala, emite a nota e despacha. O primeiro CD fica na Grande São Paulo e foi inaugurado em setembro de 2024. [OFICIAL] vídeo institucional republicado em HfqVbVgdNtg (2026-05-25) e TUs6QYGqGrw (2026-08-04). Confiança A.
2. **Entrada no Full em 2026:**
   - CNPJ, no Simples Nacional ou no regime normal;
   - nota da loja acima de 4,5;
   - pelo menos 5 pedidos por dia;
   - requisitos por item: mínimo de vendas, dimensões, peso e preço.
   
   [OFICIAL] TUs6QYGqGrw (canal Shopee Brasil, 2026-08-04). Confirmado por OUC2vulFv8E (2026-04-27). Confiança A.
3. **Adesão:** cadastro fiscal completo (série de NF exclusiva para a Shopee, certificado digital, regra fiscal por produto com CFOP, CST e ICMS por UF) e "nomeação" de cada produto, que a Shopee aprova ou recusa. [OFICIAL] CDXeiFn8Ykw (2026-09-17). [PRÁTICA com tela] ty0iwe3dV1I (2026-07-20). Confiança A.
4. **Envio ao CD:**
   - **Itens a partir de R$20:** o envio ao CD é gratuito.
   - **Itens abaixo de R$20:** desde 1/7/2026 pagam "envio excepcional" por unidade: R$1 (P), R$2,50 (M), R$6 (G) e R$12,50 (XG).
   - A tela mostrou mínimo de 15 unidades por SKU e teto de 1.000 unidades por solicitação.
   
   [PRÁTICA com tela] ty0iwe3dV1I (2026-07-20). Confiança C, fonte única.
5. **Multas do Full (abril de 2026):**
   - R$5 por unidade agendada e não enviada;
   - R$3 por unidade divergente, a mais ou a menos;
   - o cancelamento sem multa vai até 2 dias antes do agendamento.
   
   Na época, armazenagem e envio eram gratuitos. [PRÁTICA, sem tela] OUC2vulFv8E (2026-04-27). Confiança C. Não houve leitura oficial de tabela de armazenagem nem de estoque antigo. Ver a Lacuna 1.
6. **Programa Full+ (lançado em junho de 2026):** reduz a comissão de itens Full a partir de R$50 conforme a participação de pedidos Full no mês.
   - **Com 40% a 70% de pedidos Full:** 0,5 p.p. (itens de R$50 a R$79,99) ou 1 p.p. (a partir de R$80).
   - **Com 70% ou mais:** 1 p.p. (itens de R$50 a R$79,99) ou 2 p.p. (a partir de R$80).
   - O desconto é creditado na carteira na 1ª semana do mês seguinte.
   
   [OFICIAL] 0oRYednAlHY (2026-08-04). Confiança B.
7. **Benefícios oficiais do Full:** envio todos os dias, cupons e descontos exclusivos e acesso a campanhas especiais. Não há número publicado de ganho de exposição. [OFICIAL] oUbb0vhDqNs (2026-08-04). Tela do painel em Vfbc25kqgYs (2026-05-05). Confiança A para a existência dos benefícios; sem evidência para o tamanho do efeito.
8. **Prazo de despacho (DTS) no envio próprio:**
   - até 2 dias úteis após o pagamento;
   - de 7 a 30 dias corridos para personalizados e pré-encomenda;
   - cancelamento automático se o vendedor não postar no prazo ou ficar inativo por mais de 7 dias.
   
   [OFICIAL] help 76324 (sem data, pode estar superada). Confiança B.
9. **Atraso e não envio geram pontos de penalidade com corte semanal:**
   - **1 ponto:** taxa de não envio de 8% ou mais com pelo menos 2 pedidos, ou atraso de 5% ou mais com pelo menos 2 pedidos.
   - **2 pontos:** a mesma taxa com 90 pedidos ou mais.
   - **Faixas:**
     - de 3 a 5 pontos: 14 dias sem Vendedor Indicado e sem campanhas, −5% de visibilidade e R$100;
     - de 6 a 8 pontos: também perde o frete grátis, −10% e R$250;
     - de 9 a 11 pontos: 21 dias, −20% e R$500;
     - de 12 a 14 pontos: 28 dias, −30% e R$1.000;
     - 15 pontos ou mais: conta congelada por 28 dias e R$1.500.
   - Os pontos zeram a cada trimestre.
   
   [OFICIAL via terceiro com tela] LLDUrAuF3qQ (2026-05-14) e ThPsYQpMxJE (2026-08-05), concordantes. Confiança B.
10. **Frete grátis obrigatório para todos desde março de 2026.** O subsídio da Shopee ao frete é de até R$20 (itens até R$79,99), R$30 (de R$80 a R$199,99) e R$40 (a partir de R$200). A partir de 1/10/2026, a taxa fixa da faixa até R$79,99 sobe de R$4 para R$4,50. [OFICIAL via terceiro] j_2kh6auKiw (2026-06-04), 9VOoazXt_aE (2026-09-25) e hEkVpRw_vNg (2026-10-13). Confiança B. Diverge da central do comprador, que fala em teto de R$20 no cupom. Ver a seção 6.
11. **Modalidades além do Full:**
    - Shopee Xpress (SPX), com coleta no endereço para vendedores selecionados;
    - Agência Shopee (drop-off);
    - Correios;
    - Logística do Vendedor (volumosos);
    - Entrega Rápida (mesmo dia ou dia seguinte, só na Grande SP, frete fixo de R$8);
    - Entrega Turbo (até 4 h, raio de 10 km, com Uber, desde 13/5/2026).
    
    [OFICIAL] help 76163, 164639/198296, 132039, 150530/151051 e 223979. Turbo via sqRN4l8OQ-w com tela. Confiança A.
12. **Perecíveis no fulfillment:** o vendedor responde pela validade. A Shopee pode descartar na hora produto vencido ou contaminado, e item bloqueado parado por mais de 7 dias passa a ser dela. [OFICIAL] help 124091, Termos do Programa de Logística, atualizado em 16/02/2023 (pode estar superada). Confiança B.
13. **Anvisa:** desde 21/09/2026, o atributo Anvisa é obrigatório para **novos** anúncios em 169 categorias listadas. [OFICIAL via terceiro] RvJiFGQiK3c (integrador com API, 2026-09-14). Confiança C.
14. **Embalagem inadequada e recorrente** pode reduzir a visibilidade, remover produtos, gerar códigos de violação e penalidades. A Shopee recomenda filmar ou fotografar a embalagem. [OFICIAL] 9CxujZDsRCw (2026-10-01). Confiança B.
15. **Não há fonte pública, oficial ou de dados, que meça:**
    - quanto o selo Full, o frete grátis ou o prazo aumentam a conversão na Shopee;
    - quanto tempo um anúncio leva para recuperar a posição depois de uma ruptura.
    
    Ver a seção 9.

---

## 2. Como funciona (mecânica e regras oficiais, com data)

### 2.1 Mapa das modalidades (Shopee Brasil, out/2026)

| Modalidade | Quem opera | Regra principal | Fonte · data · tipo |
|---|---|---|---|
| **Full Shopee** | A Shopee armazena, embala, emite NF e despacha | Exige convite ou habilitação e requisitos de loja e de item. O CD fica na Grande SP. | TUs6QYGqGrw 2026-08-04 [OFICIAL]; HfqVbVgdNtg 2026-05-25 [OFICIAL republicado] |
| **Shopee Xpress (SPX)** | Coleta no endereço do vendedor pelo parceiro Shopee | "Para vendedores selecionados". Há horário de corte. Embalagem fora do padrão é recusada. A taxa depende de peso e dimensões. | help 76163, sem data (pode estar superada) [OFICIAL] |
| **Agência Shopee** (drop-off) | O vendedor posta num ponto parceiro | Até 120 cm num lado, até 200 cm na soma dos lados e até 30 kg. O pacote fica no máximo 3 dias na agência. | help 198296 e 198750, sem data [OFICIAL] |
| **Correios / entrega padrão** | Parceiro logístico | Prazo local de 1 a 25 dias úteis a partir da coleta | help 76335 e 76349, sem data [OFICIAL] |
| **Logística do Vendedor** | O vendedor entrega (transportadora própria) | Para itens grandes, como móveis e geladeiras. O vendedor atualiza o status e informa o rastreio. | help 132039, sem data [OFICIAL] |
| **Entrega Rápida** | O vendedor entrega | Mesmo dia ou dia seguinte, com faixas "Chega Hoje" e "Chega Amanhã". Só na Grande SP. Frete fixo de R$8. O vendedor define horário de corte, área e capacidade diária. Segunda a sexta. | help 150530, 151051 e 151052, sem data [OFICIAL] |
| **Entrega Turbo** | Uber Direct coleta e entrega | Até 4 h, raio de 10 km, em teste desde 13/05/2026 | sqRN4l8OQ-w 2026-05-19 [OFICIAL via terceiro, com tela]; contrato "Uber Direct" listado em help 77326 [OFICIAL] |

**Obrigação de uso.** Pelos Termos do Programa de Logística, quando uma solução logística está disponível na conta, o vendedor deve "utilizar necessariamente" esse serviço. A Shopee pode trocar a forma de envio da conta ou do produto. [OFICIAL] help 124091 (16/02/2023, pode estar superada).

**Escada logística vista por praticante.** Correios → Shopee Express → entrega no mesmo dia → Full. Segundo ele, o topo da busca quase não tem anúncio postado pelos Correios. [PRÁTICA, com tela de busca e sem medição] PeQPVfCjZp8 (2026-07-02). Confiança C.

### 2.2 Full Shopee: regras de entrada e operação

- **Requisitos da loja:**
  - CNPJ, no Simples Nacional ou no regime normal;
  - avaliação da loja acima de 4,5;
  - pelo menos 5 pedidos por dia.
  
  Os requisitos por item são mínimo de vendas, dimensões, peso e preço. Os valores exatos ficam "no centro de educação do vendedor" e não foram lidos. [OFICIAL] TUs6QYGqGrw (2026-08-04).
- **Versão anterior (pode estar superada):** o Full era só por convite, para lojas da região de SP e categorias como eletrônicos e casa. [DADO/blog] Bling, 2025-11-15, https://blog.bling.com.br/full-shopee/. Em 2026 a liberação passou a ser "em lotes", e "a grande maioria" dos grupos de vendedores já estaria habilitada. [PRÁTICA] ty0iwe3dV1I (2026-07-20).
- **Cadastro fiscal** (passo a passo oficial):
  1. CNPJ no perfil da loja.
  2. Série de NF exclusiva para a Shopee e certificado digital.
  3. Escolher se o frete entra na NF.
  4. Prazo de cancelamento da NF de 24 h.
  5. Regra fiscal:
     - **Simples Nacional:** tabela na própria plataforma.
     - **Regime normal:** planilha com CFOP para dentro e fora do estado, CST e alíquota de IPI, PIS/Cofins e ICMS por UF, para quatro tipos de NF: venda, remessa, retorno ao vendedor e retorno ao Full.
  6. Aceitar os termos do Full.
  
  [OFICIAL] CDXeiFn8Ykw (2026-09-17).
- **Nomeação do produto** (etapa que, segundo o praticante, não existe no ML nem na Amazon). Em "indicar produtos ao Full", o vendedor informa:
  1. **Preço de custo:** é a base do reembolso em caso de extravio.
  2. **Dados fiscais e medidas reais:** a Shopee mede de novo no recebimento. A multa por discrepância não estava publicada em julho.
  3. **Ciclo de vida:** quanto tempo se espera que o produto fique no CD.
  4. **Quantidade mínima em estoque:** dispara o alerta de reposição.
  5. **Dias mínimos de cobertura:** a recomendação da tela era 0.
  
  A Shopee aprova ou recusa. [PRÁTICA com tela] ty0iwe3dV1I (2026-07-20).
- **Solicitação de envio:**
  1. Escolher o CD (havia só um para aquele vendedor).
  2. Escolher o método (coleta ou entrega própria; a coleta não aparecia para todos).
  3. Escolher variações e quantidade. Para um SKU abaixo de R$20, a tela mostrou mínimo de 15 unidades. O teto é de 1.000 unidades.
  4. Informar o número de caixas e a data (a mais próxima era a segunda-feira seguinte).
  
  [PRÁTICA com tela] ty0iwe3dV1I.
- **Custos de entrada ao CD (a partir de 01/07/2026):**
  - itens a partir de R$20 não pagam envio;
  - itens abaixo de R$20 pagam R$1 (P), R$2,50 (M), R$6 (G) ou R$12,50 (XG) por unidade.
  
  [PRÁTICA com tela da documentação] ty0iwe3dV1I. Antes disso (abril), "não paga nada" para enviar nem para armazenar. [PRÁTICA] OUC2vulFv8E (2026-04-27).
- **Inconformidades:**
  - **Reserva não cumprida:** R$5 por unidade agendada e não enviada, com cancelamento sem multa até 2 dias antes.
  - **Quantidade divergente:** R$3 por unidade a mais ou a menos.
  
  [PRÁTICA, sem tela] OUC2vulFv8E (2026-04-27).
- **Responsabilidade por extravio:** se um produto "sumiu desde que deu entrada", o vendedor não responde. [PRÁTICA] Vfbc25kqgYs (2026-05-05). Fonte oficial do reembolso: não lida. O valor de custo informado na nomeação é a referência. [PRÁTICA] ty0iwe3dV1I.
- **Cancelamento do comprador:** pedidos de Entrega Expressa (Full, Rápida ou Turbo) entram na separação "minutos após" o pagamento e não podem ser interrompidos. O comprador precisa recusar na entrega. [OFICIAL] help 223979 (sem data, pode estar superada).

### 2.3 Programa Full+

- Lançado em junho de 2026 e sem inscrição: toda loja no Full já é elegível.
- **Participação** = pedidos via Full ÷ pedidos totais da loja no mês calendário fechado. Itens abaixo de R$50 contam para a participação, mas não geram desconto.
- **Faixas:**
  - menos de 40%: nada;
  - de 40% a 70%: 0,5 p.p. (de R$50 a R$79,99) ou 1 p.p. (a partir de R$80);
  - 70% ou mais: 1 p.p. (de R$50 a R$79,99) ou 2 p.p. (a partir de R$80).
- O crédito cai na carteira na 1ª semana do mês seguinte. A contagem recomeça do zero todo mês.
- A peça fala em "até 14% de desconto sobre a sua comissão", ou seja, 2 p.p. sobre uma comissão de 14%.

[OFICIAL] 0oRYednAlHY (2026-08-04).

### 2.4 Prazo de despacho, cancelamento e penalidades (envio próprio)

- **DTS:** até 2 dias úteis após a confirmação do pagamento. Para produtos personalizados ou pré-encomenda, de 7 a 30 dias corridos. Cancelamento automático se o vendedor não cumprir o prazo ou ficar inativo por mais de 7 dias. [OFICIAL] help 76324 (sem data, pode estar superada).
- **Métricas semanais do painel "Desempenho da conta"** (tela de conta de aluno):

| Métrica | Limite | O que afeta |
|---|---|---|
| Taxa de não cumprimento (cancelamento pelo vendedor + falta de envio + devolução por erro do vendedor) | menos de 8% | Vendedor Indicado e pontos |
| Envio atrasado | menos de 5% | Pontos |
| Tempo de preparação | menos de 1 dia | Vendedor Indicado |
| Envios aos sábados | mais de 20% | Vendedor Indicado |
| Produtos de pré-encomenda | menos de 20% | Vendedor Indicado e limite de anúncios |

  [OFICIAL via terceiro com tela] LLDUrAuF3qQ (2026-05-14). Confiança C nos limites do Vendedor Indicado (fonte única) e B nos limites de pontos (concordam com ThPsYQpMxJE).
- **Pontos e faixas:** ver o Resumo, item 9. Os pontos acumulam no trimestre (jan–mar, abr–jun, jul–set, out–dez) e zeram na virada. Pedir ao comprador que cancele por falta de estoque dá 2 pontos direto. [OFICIAL via terceiro, tutorial lido em tela] ThPsYQpMxJE (2026-08-05).
- **Entrega Turbo:**
  - o vendedor define dias, horário e limite de pedidos por hora;
  - coletas de hora em hora, a 1ª 3 h após a abertura e a última 3 h após o fechamento;
  - 1 h para imprimir a etiqueta, senão o pedido é cancelado e conta como não cumprimento;
  - o motorista é atribuído cerca de 15 min antes;
  - a loja deve ficar aberta 30 min a mais para receber devoluções.
  
  [OFICIAL via terceiro com tela do artigo de 13/05/2026] sqRN4l8OQ-w.

### 2.5 Frete grátis e custo do frete

- **Lado vendedor:**
  - Desde março de 2026, todas as lojas entram automaticamente no programa de frete grátis, que antes era opcional e pago à parte. [OFICIAL via terceiro com tela] j_2kh6auKiw (2026-06-04). Confirmado em Zx8826q-qLk (2026-05-22).
  - **Subsídio máximo:** R$20 (até R$79,99), R$30 (de R$80 a R$199,99) e R$40 (a partir de R$200). O programa "frete grátis extra" seguia sem mudança em 25/09/2026. [OFICIAL via terceiro] 9VOoazXt_aE.
  - **Coparticipação com logística ou transportadora própria** (exemplo da documentação): frete cotado de R$100, cupom de R$40, comprador paga R$60. Do cupom, o vendedor banca 25% (R$10) e a Shopee 75% (R$30). [OFICIAL via terceiro com tela] j_2kh6auKiw.
- **Lado comprador:**
  - Cupom de frete grátis só no app, acima de um valor mínimo por vendedor.
  - Não cobre frete acima de R$20: desconta até R$20 e o comprador paga a diferença.
  - Até 10 cupons por semana; um cupom vale para até 3 pacotes; pode não estar disponível para todos os vendedores.
  
  [OFICIAL] help 76220 e 76265 (sem data, pode estar superada).
- **ShopeeVIP** (assinatura do comprador, R$9,90 por mês): cupons de frete grátis ilimitados em compras acima de R$10, para fretes até R$20. [OFICIAL] help 223874 (sem data). [PRÁTICA] Kasbq8gziOg (2026-05-21).
- **Cálculo do frete:** usa as dimensões cadastradas pelo vendedor, a origem e o destino. Informação errada gera "cobrança divergente" repassada ao vendedor. O endereço de coleta tem de ser o físico (sem caixa postal ou endereço de terceiro). [OFICIAL] help 124091 (16/02/2023, pode estar superada); help 76332 (sem data).
- **Comissão que convive com o frete** (detalhes na frente preco-promocao):
  - até R$79,99: 20% + R$4, que passa a R$4,50 em 01/10/2026;
  - de R$80 a R$99,99: 14% + R$16;
  - de R$100 a R$199,99: 14% + R$20;
  - subsídio Pix de 5% a partir de R$80, chegando a 8% acima de R$500;
  - adicional de R$3 por item para vendedor CPF acima de um volume em 90 dias.
  
  [OFICIAL via terceiro] 9VOoazXt_aE (2026-09-25) e hEkVpRw_vNg (2026-10-13). Confiança B.

### 2.6 Picos (campanhas)

- **Prazos em campanha:** em grandes eventos, o tempo de preparação do vendedor e do CD e o tempo de coleta aumentam. A data prometida já embute essa variação por "inteligência preditiva". [OFICIAL] help 223979 (sem data).
- **Checklist oficial para o 10.10:**
  1. Conferir se o estoque registrado bate com o físico.
  2. Validar a integradora e usar a atualização em massa.
  3. Pré-embalar os mais vendidos.
  4. Aplicar FIFO e deixar os mais vendidos perto do empacotamento.
  
  Nas campanhas de produto, a nomeação **só é aprovada com estoque disponível**. Na campanha de cupom, a quantidade não pode ser editada depois de nomeada. [OFICIAL] urA_Dc9FBvU (2026-09-24).

---

## 3. O que os melhores fazem

### 3.1 Práticas com algum consenso

- **P1. Mandar para o Full só o que gira.** Isso reduz o capital parado e prepara para cobranças futuras de armazenagem. [PRÁTICA] Vfbc25kqgYs (vendedor desde 2016, multicanal, operação própria em SP, 2026-05-05). Na nomeação, o praticante usa ciclo de vida de 1 dia para item de venda diária. [PRÁTICA com tela] ty0iwe3dV1I. Confiança C, fontes N6 e N7 concordantes no princípio.
- **P2. Evitar o Full para item abaixo de R$20 e volumoso.** A taxa de envio por unidade (até R$12,50 no XG) inviabiliza a margem. A saída é subir o preço acima de R$20 ou montar kit. [PRÁTICA com tela] ty0iwe3dV1I. Coerente com o desenho do Full+, que só dá desconto de R$50 para cima. [OFICIAL] 0oRYednAlHY. Confiança B no incentivo e C na tática.
- **P3. Usar o Full como capacidade extra quando falta espaço ou mão de obra.**
  - **Caso:** loja de fraldas com 90–95% das vendas na Shopee e cerca de 600 pedidos por dia com 3 pessoas.
  - **Motivo da entrada:** "eu precisava de espaço dentro do barracão".
  - **Resultado:** a loja que já tracionava chegou a 40–50% dos pedidos via Full pouco tempo depois.
  
  [PRÁTICA, sem base de comparação; rebaixado de CASE] 8N5ktlBoTJ8 (2026-09-09). Confiança C.
- **P4. Não vender acima da capacidade de expedição.** Se só se consegue expedir 50–80 peças por dia, não se pode vender 100: o atraso vira ponto e a bola de neve leva ao congelamento. [PRÁTICA com tela] LLDUrAuF3qQ (2026-05-14). Mecanismos oficiais que limitam a demanda: capacidade diária na Entrega Rápida e pedidos por hora na Turbo. [OFICIAL] help 151052; sqRN4l8OQ-w. Confiança B.
- **P5. Operação própria organizada para o envio próprio.**
  - ERP com produtos identificados, estoque mapeado e separação em onda.
  - Pré-embalar campeões em pico; FIFO.
  
  [PRÁTICA] Vfbc25kqgYs; lUHmbbFLF7M (ML, separação em onda); [OFICIAL] urA_Dc9FBvU. Confiança B.
- **P6. Registrar a embalagem em foto ou vídeo** para contestar avaria. Para itens de alto valor, não expor a marca por fora e usar lacre. [OFICIAL] 9CxujZDsRCw (2026-10-01).
- **P7. Precificar com o frete dentro do custo.**
  - A coparticipação de frete entra no custo antes do markup.
  - A fórmula divide os valores nominais por (1 − comissão − imposto − margem).
  - Refazer a conta a cada mudança de frete.
  
  [PRÁTICA com tela] j_2kh6auKiw (2026-06-04, ferramenta de precificação, com CTA). [DADO/blog] Avantpro, https://avantpro.com.br/como-vender-mais-shopee/ (aprox. 2026-05). Confiança B no método.
- **P8. Ativar a Entrega Turbo só com densidade e equipe.** Faz sentido em capitais e grandes centros. Exige estar com o pacote pronto a cada coleta horária. [PRÁTICA] sqRN4l8OQ-w. Confiança C.

### 3.2 Divergências entre fontes

- **D1. Entrar ou não no Full.**
  - **Contra (por ora):** Vitor Miranda (Vfbc25kqgYs, 2026-05-05). Motivos:
    - estoque fica exclusivo de um canal, o que pesa para quem é multicanal;
    - a "cultura de giro" corrói a margem;
    - relatos de atraso de até 5 dias no Full, sumiço de peças e cancelamentos afetando a conta em maio de 2026.
  - **A favor:** a Shopee (todos os vídeos oficiais); Universidade Ecommerce (OUC2vulFv8E); a loja de fraldas (8N5ktlBoTJ8, "tá surpreendendo").
  - Nenhum dos lados mostra número de conversão antes e depois.
- **D2. Custo de envio e armazenagem.**
  - "Não paga nada para enviar nem armazenar" (OUC2vulFv8E, abril).
  - Taxa por unidade para itens abaixo de R$20 desde julho (ty0iwe3dV1I).
  - Ninguém mostrou tabela de armazenagem nem de estoque antigo.
  - **Faixa:** de R$0 a R$12,50 por unidade no envio; armazenagem "sem evidência".
- **D3. Teto do frete grátis.**
  - A central do comprador diz teto de R$20 no cupom (help 76220, sem data).
  - Fontes do lado vendedor dizem subsídio de R$20, R$30 ou R$40 conforme a faixa de preço (j_2kh6auKiw, 9VOoazXt_aE).
  - Hipótese: o artigo do comprador descreve o cupom-base, ou está desatualizado. Não deu para checar no Seller Centre.
- **D4. Vantagem do Full no algoritmo.** "O algoritmo tende a dar mais relevância" (OUC2vulFv8E) e "mais destaque na plataforma" (texto do painel em Vfbc25kqgYs). Não há medição. Fica como hipótese.

---

## 4. Números de referência

| Item | Valor / faixa | Fonte | Data | Tipo | Conf. |
|---|---|---|---|---|---|
| Requisitos de loja no Full | CNPJ; nota acima de 4,5; pelo menos 5 pedidos/dia | TUs6QYGqGrw; OUC2vulFv8E | 2026-08-04; 2026-04-27 | OFICIAL | A |
| Envio ao CD, item a partir de R$20 | R$0 | ty0iwe3dV1I | 2026-07-20 | PRÁTICA (tela) | C |
| Envio ao CD, item abaixo de R$20 (por unidade) | P R$1 · M R$2,50 · G R$6 · XG R$12,50 | ty0iwe3dV1I | vigente desde 2026-07-01 | PRÁTICA (tela) | C |
| Lote por solicitação ao Full | mín. 15 un. (SKU observado) · máx. 1.000 un. | ty0iwe3dV1I | 2026-07-20 | PRÁTICA (tela) | C |
| Multa por reserva não enviada | R$5 por unidade | OUC2vulFv8E | 2026-04-27 | PRÁTICA | C |
| Multa por quantidade divergente | R$3 por unidade | OUC2vulFv8E | 2026-04-27 | PRÁTICA | C |
| Cancelar agendamento sem multa | até 2 dias antes | OUC2vulFv8E | 2026-04-27 | PRÁTICA | C |
| Armazenagem e estoque antigo no Full | sem evidência (em abril era "grátis") | OUC2vulFv8E | 2026-04-27 | PRÁTICA | C |
| Full+, participação mínima | 40% dos pedidos do mês | 0oRYednAlHY | 2026-08-04 | OFICIAL | B |
| Full+, desconto de comissão | 0,5 a 2 p.p. (itens a partir de R$50) | 0oRYednAlHY | 2026-08-04 | OFICIAL | B |
| DTS padrão | 2 dias úteis | help 76324 | sem data (pode estar superada) | OFICIAL | B |
| DTS personalizado ou pré-venda | de 7 a 30 dias corridos | help 76324 | sem data | OFICIAL | B |
| Cancelamento automático por inatividade | mais de 7 dias | help 76324 | sem data | OFICIAL | B |
| Não cumprimento, ponto | 8% ou mais e pelo menos 2 pedidos (1 pt); pelo menos 90 pedidos (2 pt) | ThPsYQpMxJE; LLDUrAuF3qQ | 2026-08-05; 2026-05-14 | OFICIAL via terceiro | B |
| Atraso, ponto | 5% ou mais e pelo menos 2 pedidos (1 pt); pelo menos 90 pedidos (2 pt) | ThPsYQpMxJE | 2026-08-05 | OFICIAL via terceiro | B |
| Faixas de penalidade | de 3 a 15 pontos ou mais: −5% a −30% de visibilidade; multa de R$100 a R$1.500; perde frete grátis a partir de 6 pontos | ThPsYQpMxJE; LLDUrAuF3qQ | 2026 | OFICIAL via terceiro | B |
| Vendedor Indicado, logística | preparo em menos de 1 dia; mais de 20% de envios aos sábados | LLDUrAuF3qQ | 2026-05-14 | OFICIAL via terceiro | C |
| Subsídio de frete grátis (vendedor) | R$20 / R$30 / R$40 por faixa de preço | j_2kh6auKiw; 9VOoazXt_aE | 2026-06-04; 2026-09-25 | OFICIAL via terceiro | B |
| Cupom de frete grátis (comprador) | até R$20; 10 por semana; 3 pacotes por cupom | help 76220 | sem data | OFICIAL | B |
| Coparticipação no frete (exemplo oficial) | vendedor 25% e Shopee 75% do cupom | j_2kh6auKiw | 2026-06-04 | OFICIAL via terceiro | C |
| Entrega Rápida | frete fixo de R$8; mesmo dia ou D+1; Grande SP | help 151051, 150530 | sem data | OFICIAL | B |
| Entrega Turbo | até 4 h; raio de 10 km; 1 h para a etiqueta; coletas a cada hora | sqRN4l8OQ-w (artigo de 13/05/2026) | 2026-05-19 | OFICIAL via terceiro | B |
| Agência Shopee | 1 lado até 120 cm; soma até 200 cm; até 30 kg; até 3 dias na agência | help 198296, 198750 | sem data | OFICIAL | B |
| Prazo de entrega local | de 1 a 25 dias úteis após a coleta | help 76349 | sem data | OFICIAL | B |
| Produto bloqueado nos "Pontos" | após 7 dias corridos, a propriedade passa à Shopee | help 124091 | 2023-02-16 (pode estar superada) | OFICIAL | B |
| ShopeeVIP | R$9,90/mês; frete grátis em compras acima de R$10 com frete até R$20 | help 223874 | sem data | OFICIAL | B |
| Receita de logística da Shopee (global) | −9,0% a/a no 2T26 (US$676,4 mi) por maior abatimento de subsídios de frete | Sea 6-K, ex. 99.1 | 2026-08-11 | DADO (N2) | B |
| Pedidos/dia de uma loja grande, Full | cerca de 600/dia, 40–50% via Full | 8N5ktlBoTJ8 | 2026-09-09 | PRÁTICA | C |

O 6-K da Sea está em https://www.sec.gov/Archives/edgar/data/1703399/000119312526344596/d120948dex991.htm. É dado global da Shopee: não isola o Brasil e serve só como sinal de que o subsídio de frete está crescendo.

---

## 5. Alimentos, perecíveis e marca própria/indústria

- **Validade é do vendedor.**
  - Nos "Pontos" logísticos, o vendedor responde pela validade e pelas condições dos produtos.
  - A Shopee pode bloquear a venda ou pedir a retirada se faltar NF, se houver avaria ou se o produto for diferente do anunciado.
  - Perecível vencido ou contaminado ("pragas, traças e fungos") pode ser destruído na hora, sem indenização.
  
  [OFICIAL] help 124091 (16/02/2023, pode estar superada) [MARCA e REVENDA].
- **Prazo de 7 dias.** Produto bloqueado que fica mais de 7 dias corridos passa a ser da Shopee, que pode descartar, doar, vender ou destruir à custa do vendedor. Para alimentos, isso transforma bloqueio por validade em perda total se não houver retirada rápida. [OFICIAL] help 124091.
- **Lote, validade mínima na entrada, FEFO e temperatura no Full:** **sem evidência**. Nenhuma fonte pública lida traz regra de validade mínima no recebimento, controle por lote ou cadeia fria. A única menção oficial a vencimento é o FIFO, recomendado às Agências e aos vendedores para "evitar perdas por vencimento". [OFICIAL] help 176312 (sem data); urA_Dc9FBvU (2026-09-24).
- **Café no Full existe.** Na busca "café em grãos" ordenada por vendas, a marca Baggio aparece com selos "Full" e "Oficial". A maioria dos líderes é marca própria ou torrefação. [OBS] observacao/lideres.md (2026-10-14, sem login, uma página de busca). Confiança C. Mostra que alimento não perecível de prateleira entra no Full em ao menos um caso. Não mostra quais regras se aplicaram.
- **Anvisa no cadastro.** Desde 21/09/2026, o atributo Anvisa (protocolo ou código) é obrigatório para novos anúncios em 169 categorias listadas numa planilha. Os anúncios antigos ficam como estão "por enquanto". [OFICIAL via terceiro] RvJiFGQiK3c (integrador Vendedor 360, que diz receber os comunicados pela API, 2026-09-14). Confiança C. A planilha não foi conferida para alimentos ou café.
- **Medicamentos e suplementos.** Comprar medicamento ou suplemento de saúde não é possível na Shopee. Suplementos alimentares só por "vendedores selecionados". [OFICIAL] help 76328 (sem data).
- **Embalagem de produto sensível.**
  - Pedido misto segue a diretriz do item mais sensível. Separar os itens por dentro evita vazamento e atrito.
  - Marcação feita à mão pode não ser aceita quando o manuseio exige identificação clara.
  - Produto perigoso ou restrito tem regras próprias de classificação e documentação.
  
  [OFICIAL] 9CxujZDsRCw (2026-10-01).
- **Indústria no Full: o peso fiscal.** O cadastro exige regra fiscal por produto e quatro tipos de NF (venda, remessa, retorno ao vendedor e retorno ao Full), com CST e alíquota de ICMS por UF no regime normal. O praticante que se declarou "fabricante do produto" preencheu orientado pela contabilidade. [OFICIAL] CDXeiFn8Ykw; [PRÁTICA] ty0iwe3dV1I. A Shopee pode recolher ou repassar tributos cobrados durante o transporte, por exemplo o DIFAL de ICMS. [OFICIAL] help 124091.
- **Inmetro:** sem evidência para Shopee neste tema.

---

## 6. Erros comuns e mitos

| O que se diz | O que as fontes fortes mostram | Fontes |
|---|---|---|
| "O Full da Shopee é grátis" | Em julho de 2026, itens abaixo de R$20 passaram a pagar envio por unidade (até R$12,50). Há multas de R$5 e R$3 por unidade em no-show e divergência. A armazenagem não tem tabela pública lida. | ty0iwe3dV1I; OUC2vulFv8E |
| "Frete grátis é totalmente grátis" | O cupom cobre até R$20 no lado do comprador. O comprador paga a diferença. | help 76220 [OFICIAL]; Kasbq8gziOg |
| "O subsídio de frete sai do bolso do vendedor" | Pela documentação mostrada, o subsídio padrão é da Shopee. Só há coparticipação de 25% no cenário de logística ou transportadora própria. | j_2kh6auKiw; hEkVpRw_vNg |
| "Se eu atrasar mas enviar, não conta" | Conta. O envio atrasado gera ponto a partir de 5% com pelo menos 2 pedidos, mesmo sem entrar na taxa de não cumprimento. | ThPsYQpMxJE; LLDUrAuF3qQ |
| "Peço ao cliente para cancelar e fico limpo" | Orientar o comprador a cancelar dá 2 pontos direto, mais do que o próprio não envio. | ThPsYQpMxJE |
| "Os pontos somem depois de cumprir a suspensão" | Não: acumulam no trimestre. Uma nova infração na mesma janela leva à faixa seguinte. | LLDUrAuF3qQ |
| "Na Entrega Turbo, se o Uber atrasar a culpa é minha" | Segundo o artigo, o atraso do entregador não pesa para o vendedor. Pesa não imprimir a etiqueta em 1 h, o que cancela o pedido e conta como não cumprimento. | sqRN4l8OQ-w |
| Medida "ajustada" no cadastro para cair em faixa menor | A Shopee mede de novo no recebimento do Full. Dimensão errada gera cobrança divergente de frete repassada ao vendedor. | ty0iwe3dV1I; help 124091 |
| "No ML, mais de 90% da 1ª página é Full" (dito num vídeo sobre Shopee) | Número sem base nem método (sinal fraco 2). Não usar como benchmark. | Vfbc25kqgYs |
| "Full = mais relevância no algoritmo" | Nenhuma fonte mede o efeito. A Shopee fala em "mais oportunidades" e campanhas, sem número. É hipótese. | OUC2vulFv8E; oUbb0vhDqNs |

**Sinais de conteúdo fraco.**

- **CTA de curso ou ferramenta no meio do conteúdo:** Vfbc25kqgYs (treinamento), sqRN4l8OQ-w e LLDUrAuF3qQ (portal de aulas), j_2kh6auKiw (planilha e consultoria, QR code). Mesmo assim, as telas mostradas em LLDUrAuF3qQ, j_2kh6auKiw e sqRN4l8OQ-w sustentam as regras. Ficam como N6 para a regra e N7 para a opinião.
- **Pedidos embutidos tratados como sinal fraco e ignorados:** "deixa nos comentários" para pressionar a Shopee (ty0iwe3dV1I); "comenta penalidade" para receber o link (ThPsYQpMxJE).

---

## 7. Revenda/importação x indústria/marca própria

**[REVENDA] revenda, dropshipping e importação**

- **Dropshipping puro** não tem como usar o Full: o Full pressupõe estoque próprio enviado ao CD. A restrição do DTS (2 dias úteis) e a meta de pré-encomenda abaixo de 20% (Vendedor Indicado) também penalizam quem depende do prazo do fornecedor. Fontes: help 76324; LLDUrAuF3qQ.
- **Ticket baixo:** o revendedor de item barato abaixo de R$20 é quem mais sente a taxa de envio por unidade ao CD e o fim do frete grátis opcional. O desenho do Full+ (desconto de R$50 para cima) empurra para kit ou ticket maior. Fontes: ty0iwe3dV1I; 0oRYednAlHY.
- **Fornecedor atrasado:** se o fornecedor atrasa, o agendamento ao Full precisa ser cancelado até 2 dias antes para não pagar R$5 por unidade. Fonte: OUC2vulFv8E.
- **Importação:** o prazo internacional ao comprador é de 30 a 50 dias corridos. O cupom de frete grátis não cobre custos logísticos internacionais embutidos no preço. Fontes: help 76349 e 76265.

**[MARCA] indústria e marca própria**

- **Cadastro fiscal:** a carga é maior (regra fiscal por produto, ICMS por UF, quatro tipos de NF). Uma vez feita, a Shopee emite as NFs de venda a partir do CD. Fonte: CDXeiFn8Ykw.
- **Responsabilidades e riscos:**
  - responder pela validade e condição do lote;
  - risco de descarte de perecível;
  - risco de perda após 7 dias de bloqueio.
  
  Fonte: help 124091 (pode estar superada).
- **Escala:** os relatos de grandes vendedores de fábrica própria (6.000 pedidos/dia em QoF266Zzi20; itens hospitalares em tSy5Vjapgyg) não detalham a logística da Shopee. Sem evidência para práticas de Full específicas de indústria.
- **Anvisa:** o atributo obrigatório em novos anúncios (desde 21/09/2026) recai sobre quem é fabricante ou detentor do registro. Fonte: RvJiFGQiK3c.

**[AMBOS]**

- DTS, pontos e faixas;
- frete grátis obrigatório e faixas de subsídio;
- regras da Agência, do SPX e da Turbo;
- embalagem e registro em vídeo;
- conferência de estoque antes de campanhas.

---

## 8. Tabela de afirmações

| id | afirmação | tipo | fonte | data | confiança | revenda/marca | superada? |
|---|---|---|---|---|---|---|---|
| A1 | Full: a Shopee armazena, embala e envia; o 1º CD fica na Grande SP desde set/2024 | OFICIAL | TUs6QYGqGrw; HfqVbVgdNtg | 2026-08-04; 2026-05-25 | alta | ambos | não |
| A2 | Requisitos do Full: CNPJ (Simples ou normal), nota acima de 4,5, pelo menos 5 pedidos/dia, mínimos por item | OFICIAL | TUs6QYGqGrw; OUC2vulFv8E | 2026-08-04 | alta | ambos | não |
| A3 | Adesão exige série de NF exclusiva, certificado digital, regra fiscal e quatro tipos de NF | OFICIAL | CDXeiFn8Ykw | 2026-09-17 | média | ambos (pesa mais para MARCA) | não |
| A4 | Produto precisa ser "nomeado" e aprovado; informa custo, ciclo de vida, estoque mínimo e cobertura | PRÁTICA (tela) | ty0iwe3dV1I | 2026-07-20 | baixa | ambos | não |
| A5 | Desde 01/07/2026, item abaixo de R$20 paga R$1/R$2,50/R$6/R$12,50 por unidade para entrar no Full; a partir de R$20 é grátis | PRÁTICA (tela) | ty0iwe3dV1I | 2026-07-20 | baixa | revenda | não |
| A6 | Solicitação ao Full: mín. de 15 un. (SKU observado) e máx. de 1.000 un. | PRÁTICA (tela) | ty0iwe3dV1I | 2026-07-20 | baixa | ambos | não |
| A7 | Multas: R$5/un. por reserva não enviada; R$3/un. por divergência; cancelar até 2 dias antes | PRÁTICA | OUC2vulFv8E | 2026-04-27 | baixa | ambos | não (limiar) |
| A8 | Armazenagem do Full era gratuita em abr/2026; tabela de estoque antigo não encontrada | PRÁTICA | OUC2vulFv8E | 2026-04-27 | baixa | ambos | não |
| A9 | Full+: desconto de 0,5 a 2 p.p. na comissão para itens a partir de R$50, com 40% ou mais de pedidos Full no mês | OFICIAL | 0oRYednAlHY | 2026-08-04 | média | ambos | não |
| A10 | Itens Full têm cupons exclusivos, campanhas especiais e envio todos os dias | OFICIAL | oUbb0vhDqNs; Vfbc25kqgYs (tela) | 2026-08-04 | alta | ambos | não |
| A11 | DTS de 2 dias úteis (7 a 30 corridos para pré-venda); cancela automaticamente se não postar ou após mais de 7 dias de inatividade | OFICIAL | help 76324 | sem data | média | ambos | sim (sem data) |
| A12 | Ponto por não envio (8% ou mais) ou atraso (5% ou mais) com pelo menos 2 pedidos; 2 pontos com pelo menos 90 | OFICIAL via terceiro | ThPsYQpMxJE; LLDUrAuF3qQ | 2026-08-05 | média | ambos | não |
| A13 | Faixas: de 3 a 15 pontos ou mais = −5% a −30% de visibilidade, multa de R$100 a R$1.500, perde frete grátis a partir de 6, congela a partir de 15; zera por trimestre | OFICIAL via terceiro | ThPsYQpMxJE; LLDUrAuF3qQ | 2026 | média | ambos | não |
| A14 | Vendedor Indicado: preparo em menos de 1 dia e mais de 20% de envios aos sábados | OFICIAL via terceiro | LLDUrAuF3qQ | 2026-05-14 | baixa | ambos | não |
| A15 | Pedir ao comprador para cancelar = 2 pontos | OFICIAL via terceiro | ThPsYQpMxJE | 2026-08-05 | baixa | ambos | não |
| A16 | Frete grátis obrigatório para todos desde mar/2026 | OFICIAL via terceiro | j_2kh6auKiw; Zx8826q-qLk | 2026-06-04 | média | ambos | não |
| A17 | Subsídio de frete: R$20 (até R$79,99), R$30 (de R$80 a R$199,99), R$40 (a partir de R$200) | OFICIAL via terceiro | j_2kh6auKiw; 9VOoazXt_aE | 2026-09-25 | média | ambos | não |
| A18 | Com logística própria, o vendedor coparticipa com 25% do cupom de frete (exemplo oficial) | OFICIAL via terceiro | j_2kh6auKiw | 2026-06-04 | baixa | ambos | não |
| A19 | Cupom do comprador: até R$20 de frete, 10/semana, 3 pacotes/cupom, valor mínimo por vendedor | OFICIAL | help 76220 | sem data | média | ambos | sim |
| A20 | Taxa fixa até R$79,99 sobe de R$4 para R$4,50 em 01/10/2026 | OFICIAL via terceiro | 9VOoazXt_aE; hEkVpRw_vNg | 2026-09-25 | média | revenda (ticket baixo) | não |
| A21 | Entrega Rápida: mesmo dia ou D+1, Grande SP, frete fixo de R$8, o vendedor entrega e define corte e capacidade | OFICIAL | help 150530, 151051, 151052 | sem data | média | ambos | sim |
| A22 | Entrega Turbo: até 4 h, raio de 10 km, Uber, 1 h para a etiqueta, coleta a cada hora, limite por hora definido pelo vendedor | OFICIAL via terceiro + OFICIAL | sqRN4l8OQ-w; help 77326; help 223979 | 2026-05-13 | alta | ambos | não |
| A23 | SPX: coleta no endereço para vendedores selecionados; taxa por peso e dimensão; embalagem ruim recusada | OFICIAL | help 76163 | sem data | média | ambos | sim |
| A24 | Agência: 120 cm / 200 cm / 30 kg; até 3 dias na agência | OFICIAL | help 198296, 198750 | sem data | média | ambos | sim |
| A25 | Se uma logística está disponível, o uso é obrigatório; a Shopee pode trocar o modo de envio | OFICIAL | help 124091 | 2023-02-16 | média | ambos | sim |
| A26 | Dimensão cadastrada errada gera cobrança divergente repassada; endereço de coleta deve ser físico | OFICIAL | help 124091 | 2023-02-16 | média | ambos | sim |
| A27 | Perecível vencido ou contaminado pode ser destruído na hora; bloqueado por mais de 7 dias passa à Shopee | OFICIAL | help 124091 | 2023-02-16 | média | marca (alimentos) | sim |
| A28 | Pedido Full/Rápida/Turbo não pode ser cancelado após a separação; o comprador recusa na entrega | OFICIAL | help 223979 | sem data | média | ambos | sim |
| A29 | Em campanhas, a nomeação de produto só é aprovada com estoque disponível | OFICIAL | urA_Dc9FBvU | 2026-09-24 | média | ambos | não |
| A30 | Embalagem inadequada e recorrente pode reduzir visibilidade, remover anúncio e gerar penalidade | OFICIAL | 9CxujZDsRCw | 2026-10-01 | média | ambos | não |
| A31 | Atributo Anvisa obrigatório para novos anúncios em 169 categorias desde 21/09/2026 | OFICIAL via terceiro | RvJiFGQiK3c | 2026-09-14 | baixa | marca | não |
| A32 | Período sem estoque reduz o sinal usado no ranqueamento | DADO (blog de ferramenta, sem método) | avantpro.com.br/como-vender-mais-shopee | aprox. 2026-05 | baixa | ambos | — |
| A33 | Receita de logística da Shopee caiu 9% a/a no 2T26 por mais subsídio de frete (global) | DADO (N2) | Sea 6-K ex. 99.1 | 2026-08-11 | média | ambos | — |
| A34 | Loja de fraldas foi ao Full por falta de espaço; 40–50% dos pedidos via Full; cerca de 600 pedidos/dia | PRÁTICA | 8N5ktlBoTJ8 | 2026-09-09 | baixa | revenda | — |
| A35 | Relatos de atraso de até 5 dias e perda de peças no Full (mai/2026) | PRÁTICA (N7) | Vfbc25kqgYs | 2026-05-05 | baixa | ambos | — |
| A36 | Topo da busca quase sem anúncios postados pelos Correios (escada Correios → SPX → mesmo dia → Full) | PRÁTICA | PeQPVfCjZp8 | 2026-07-02 | baixa | ambos | — |
| A37 | Café em grãos: marca com selo Full entre os líderes da busca | OBS | observacao/lideres.md | 2026-10-14 | baixa | marca | — |
| A38 | Full antes de 2026: só por convite, região SP, categorias limitadas | DADO (blog) | blog.bling.com.br/full-shopee | 2025-11-15 | baixa | ambos | sim |

---

## 9. Lacunas

1. **Tabela oficial de armazenagem, permanência prolongada e estoque antigo do Full.** Não encontrada nem lida. A última fonte (abril de 2026) dizia "grátis". O Seller Centre e o Centro de Educação não foram acessíveis sem login ou JS. **Pergunta aberta:** existe cobrança por idade de estoque em out/2026?
2. **Multa por discrepância de medidas no recebimento do Full:** "a gente ainda não sabe" (ty0iwe3dV1I, julho de 2026). Sem fonte.
3. **Faixas P/M/G/XG do Full** (limites em cm e kg) e **limites de preço, peso e dimensão por item:** citados, mas sem números.
4. **Efeito da modalidade na exposição e na conversão:** nenhuma fonte mede o ganho do selo Full, da Entrega Rápida ou da Turbo, nem do frete grátis na Shopee Brasil. Só há afirmações qualitativas oficiais e opiniões de praticantes.
5. **Ruptura:** não há fonte sobre quanto cai a posição ou a entrega de Ads ao zerar estoque, nem quanto tempo leva para recuperar. Só a hipótese do blog Avantpro (sem método) e a regra oficial de que campanha exige estoque.
6. **Métricas de saúde de estoque à la IPI da Amazon:** não foi achado índice equivalente público na Shopee. Os campos vistos no painel do Full são: estoque mínimo (alerta), dias mínimos de cobertura, ciclo de vida. Sell-through e idade de estoque não aparecem em fonte pública.
7. **Multi-CD:** a única fonte de tela (jul/2026) mostra um só CD disponível. O anúncio de Recife (mai/2025) vem de blog e não foi confirmado. Não há regra de distribuição entre CDs.
8. **Limites de envio ao CD em picos** (cotas de recebimento, janela de corte para Black Friday ou 11.11): sem evidência.
9. **Regras de alimentos no Full:** validade mínima no recebimento, lote, FEFO, temperatura e categorias aceitas. Sem evidência. Inmetro também sem evidência.
10. **Termos do Programa de Frete Grátis Extra** (help 137281) e **Contrato Uber Direct** (help 196450): os links aparecem na página oficial de políticas, mas o artigo retornou "não existe" sem login.
11. **Camada de dados fraca neste tema.**
    - Lidos: Bling (2025), Avantpro (2026) e Sea 6-K/20-F (global).
    - Não acessados: Nubimetrics, UpSeller, Olist e Neotrust/Conversion, por falta de busca e de páginas estáticas.
    - Não há estudo com metodologia sobre logística da Shopee Brasil.
12. **Comparação com ML Full/Flex e Amazon FBA/DBA/FBM:** fora desta nota. Ver as notas das plataformas. A única afirmação comparativa encontrada aqui ("mais de 90% Full na 1ª página do ML") é número sem base.

---

## 10. Verificação (2026-10-14)

Método: leitura direta de artigos da central de ajuda (help.shopee.com.br) em 2026-10-15. O orçamento de WebSearch estava esgotado, então não houve busca nova. As páginas de seller.shopee.com.br/edu e a busca da central devolveram só títulos, sem conteúdo (SPA). Na dúvida, não confirmado. Os artigos da central não têm data de publicação: tudo o que vem deles fica "pode estar superado".

| id | veredito | fonte oficial (URL) | observação |
|---|---|---|---|
| A2 | SEM FONTE OFICIAL | https://seller.shopee.com.br/edu/article/full (só lista os tópicos: requisitos, taxas ao CD, multas) | Não foi possível ler os requisitos do Full na fonte oficial. Só o vídeo e praticantes sustentam os números. |
| A5 | SEM FONTE OFICIAL | mesma página do Centro de Educação (só título "taxas de envio ao CD") | Taxas por tamanho abaixo de R$20 não lidas em fonte oficial. Segue dependendo de um vídeo de praticante. |
| A7 | SEM FONTE OFICIAL | mesma página do Centro de Educação (só título "multas") | Multas de R$5 e R$3 não lidas em fonte oficial. Fonte do analista é de abril/2026, sem tela: pode estar superada. |
| A9 | SEM FONTE OFICIAL | nenhuma página oficial de texto localizada | Full+ só aparece em vídeo. Faixas e percentuais não conferidos em texto oficial. |
| A11 | CONFIRMADA (parcial) | https://help.shopee.com.br/portal/4/article/76324 | Confere: 2 dias úteis após o pagamento, 7 a 30 dias corridos para pré-encomenda/personalizado, cancelamento automático após mais de 7 dias de inatividade. Artigo sem data (pode estar superado). O artigo traz também a ressalva "O DTS não é válido apenas para dias úteis", que a nota não registra. A parte "cancelamento se não postar no prazo" não foi vista no trecho lido. |
| A12 | SEM FONTE OFICIAL | https://seller.shopee.com.br/edu/home (só lista "pontos de penalidade") | Limiares de 8%, 5%, 2 e 90 pedidos não lidos em texto oficial. O artigo 76267 testado era de outro assunto. |
| A13 | SEM FONTE OFICIAL | mesma página; nenhuma tabela oficial lida | Faixas de pontos, visibilidade, prazos e multas não conferidos. Como o valor financeiro é alto, tratar como não verificado. |
| A16-A17 | SEM FONTE OFICIAL (com divergência) | https://help.shopee.com.br/portal/4/article/76220 | O artigo é do lado do comprador: "O frete grátis não será aplicado em fretes acima de R$20", cupom de até R$20, 10 cupons por semana, até 3 pacotes por cupom, "pode não estar disponível para todos os vendedores". Não fala de subsídio por faixa (R$20/R$30/R$40), nem de obrigatoriedade para o vendedor, nem de quem paga. Não contesta a regra do lado do vendedor, mas também não a confirma. Ver D3. |
| A18 | SEM FONTE OFICIAL | nenhuma página oficial de texto localizada | Coparticipação de 25% / 75% só em vídeo. O artigo 76220 não detalha a divisão de custo. |
| A22 | SEM FONTE OFICIAL | https://help.shopee.com.br/portal/4/article/223979 e https://help.shopee.com.br/portal/4/article/77326 | O 223979 só diz que a Entrega Expressa (Full, Rápida, Turbo) entra na separação minutos após o pagamento e não pode ser interrompida. Não traz 4 h, 10 km, Uber, 1 h para etiqueta, coleta por hora nem limite por hora. O 77326 só lista o "Contrato de Parceria para Uso do Uber Direct" (sem o texto). A data de 13/05/2026 não foi conferida. |
| A27 | CONFIRMADA | https://help.shopee.com.br/portal/4/article/124091 | Itens 3.1 e 3.2: o vendedor controla a validade; perecível inadequado ("vencido ou contaminado com pragas, traças e fungos") pode ser descartado na hora, sem indenização; produto com mais de 7 dias corridos nos Pontos passa à Shopee. Atualizado em 16/02/2023: pode estar superada. É o termo do "Programa de Logística" dos Pontos, e não se confirmou que vale ao Full atual. |
| A31 | SEM FONTE OFICIAL | https://seller.shopee.com.br/edu/home (só lista "atributo Anvisa") | A existência do tema é confirmada só pelo título. Data de 21/09/2026, 169 categorias e restrição a anúncios novos não conferidos. |

Resumo: 2 confirmadas (A11 parcial, A27 desatualizável), 0 contestadas, 10 sem fonte oficial lida. Pendente para nova rodada com busca: Centro de Educação do Vendedor (Full, penalidades, Anvisa) e a página de políticas de frete grátis do vendedor.
