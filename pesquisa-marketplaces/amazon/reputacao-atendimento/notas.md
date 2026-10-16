# Reputação, atendimento e pós-venda: Amazon Brasil

Frente: reputacao-atendimento · Plataforma: Amazon (amazon.com.br; Amazon global quando a mecânica é a mesma) · Data da nota: 2026-10-15 · Analista: frente reputacao-atendimento

**Como ler esta nota**
- **Tipos:**
  - [OFICIAL]: página ou canal da plataforma.
  - [OFICIAL via terceiro]: regra oficial descrita por blog, ferramenta ou praticante.
  - [PRÁTICA]: tática de praticante.
  - [CASE]: número com período e base.
  - [DADO]: estudo ou ferramenta.
  - [OBS]: observação direta.
- **Confiança:** A, B ou C, conforme o protocolo. Na tabela da seção 8, A equivale a alta, B a média e C a baixa.
- **Canal oficial em vídeo:** os webinars do canal "Venda com a Amazon Brasil" (Seller University, apresentados por funcionários da Amazon) contam como N1, com o id do vídeo e a data de publicação.
- **Páginas sem data:**
  - As páginas de ajuda ao cliente da amazon.com.br (`/gp/help/customer/display.html?nodeId=...`) e as páginas de venda.amazon.com.br não mostram data de atualização. Foram lidas em 15/10/2026.
  - Uma regra sem data confirmada por uma fonte de 2026 é tratada como vigente. Sem essa confirmação, leva "(pode estar superada)".
- **Limite importante desta rodada:**
  - A Central de Ajuda do Seller Central (sellercentral.amazon.com.br/help/...) só carrega com login. Ela devolveu uma página de cadastro, e não houve login, conforme a regra.
  - Por isso, as metas de saúde da conta vêm de três camadas: (a) páginas públicas de venda.amazon.com.br, (b) webinars oficiais, (c) documentação pública da Selling Partner API (developer-docs.amazon), que descreve os campos do painel de saúde da conta.
  - O limite de buscas na web do turno acabou no início desta frente. As fontes foram lidas por acesso direto a URLs conhecidas (WebFetch e curl), sem novas buscas.
- **Fontes lidas:**
  - 9 transcrições da frente, na íntegra.
  - Trechos de 14 transcrições de apoio: 9 webinars oficiais e 5 de praticantes.
  - 26 páginas oficiais:
    - 16 de ajuda ao cliente da amazon.com.br;
    - 7 de venda.amazon.com.br e sell.amazon.com;
    - 3 documentos e modelos da SP-API.
  - 8 páginas de 3 fontes de dados ou ferramentas: Jungle Scout (3 páginas), Helium 10 (4 páginas) e SellerApp (1).
  - Observação de líderes (observacao/lideres.tsv, 14/10/2026) e notas de redes (social/notas.md).
- **Separação:** [REVENDA] = revenda, importação e genérico. [MARCA] = indústria e marca própria. Quando não há marcação, vale para ambos.

---

## 1. Resumo executivo

1. **Metas de envio próprio e DBA no Brasil:** envio tardio (LSR) < 4% e cancelamento antes do envio < 2,5%; acima disso, as ofertas podem ser desativadas. [OFICIAL] venda.amazon.com.br/cresca/dba (lida em 15/10/2026); PeBETM-rBxk (21/08/2026). A.
2. **ODR < 1% em 60 dias** é a meta global; não há documento N1 brasileiro com o número nesta rodada. O campo `orderDefectRate` (FBA e envio próprio separados) existe no relatório de saúde da conta. [OFICIAL] developer-docs.amazon, Performance Reports (06/10/2026); [OFICIAL via terceiro] SellerApp (28/09/2026). B.
3. **O painel "Estado da conta"** reúne nota de saúde (AHR: status e pontuação), ODR, envio tardio, cancelamento, rastreamento válido, entrega no prazo e violações de política, inclusive da política de avaliações. [OFICIAL] developer-docs.amazon (06/10/2026); PeBETM-rBxk. A.
4. **Reputação → Buy Box → Ads:** a oferta em destaque pesa preço, prazo e custo de entrega e métricas da conta; métricas ruins tiram a Buy Box até de vendedor único; sem Buy Box, o anúncio patrocinado fica "congelado". [OFICIAL] nDtHI8fUEAA (20/08/2026), 06XpeVMN7ek (17/08/2026), q0-Y5gG6Q2w (15/09/2026). A.
5. **Exclusões e contestação:** atraso da transportadora DBA tem as métricas isentadas em até 72 h; problema no ponto de coleta e pedido não reconhecido são contestados por chamado. [OFICIAL] venda.amazon.com.br/cresca/dba; lBnzH7KSh4E (20/08/2026); PeBETM-rBxk. A.
6. **Garantia de A a Z:** o cliente abre até 90 dias após a última data prevista de entrega; quase todos os gatilhos são o vendedor não responder ou resolver em 48 h, inclusive pedido de nota fiscal. [OFICIAL] amazon.com.br nodeId=GQ37ZCNECJKTFYQV (sem data; lida em 15/10/2026). A.
7. **SLA de atendimento:** o vendedor responde mensagens e instruções de devolução em até 2 dias úteis; depois disso, a A a Z cobre entrega, condição e devolução. [OFICIAL] GLC8ZMBWMBTR6QZZ, GKM69DUUYKQWKWX7, GKQNFKFK5CF3C54B. A.
8. **Devolução:** 30 dias na maioria; 7 dias para comestíveis, ração e bebidas alcoólicas; 90 dias para durável com defeito. O vendedor paga o frete de volta em arrependimento (até 7 dias) e em defeito. [OFICIAL] GKM69DUUYKQWKWX7, GFLBEJCLHMVFEPA8. A.
9. **SAFE-T (DBA e FBA Onsite):** só depois do reembolso ao cliente; DBA 45 dias, FBA Onsite 52, item devolvido com problema 7, apelação 7; perda ou dano no DBA tem reembolso automático em 3 dias; embalagem inadequada tira a elegibilidade; reembolsa só o preço do item. [OFICIAL] cya4LLoRX7A (28/07/2026). A.
10. **Avaliações de produto:** só avalia quem gastou R$ 50 em 12 meses; a nota sai de modelos de IA (recência, compra verificada), não de média simples; avaliação não verificada só conta com texto, imagem ou vídeo. [OFICIAL] G8UYX7LALQC8V9KA; GLHXEX85MENUE4XF. A.
11. **Gerar avaliações dentro das regras:** uma solicitação por pedido (botão ou API); proibido pedir só a quem gostou, pedir alteração ou dar recompensa (dinheiro, vale, desconto, produto, reembolso); punição até suspensão e retenção de pagamentos. [OFICIAL] SP-API Solicitations (09/09/2026); GLHXEX85MENUE4XF. A.
12. **Vine Brasil:** Brand Registry, oferta FBA e menos de 30 avaliações; R$ 0 (até 2 unidades), R$ 200 (3 a 10) ou R$ 500 (11 a 30) por produto pai, cobrado só após a 1ª avaliação. [OFICIAL] venda.amazon.com.br/vine (lida em 15/10/2026). A.
13. **Embalagem, avaria, prazo e vendedor não cabem na avaliação do produto:** vão para o feedback do vendedor (1 a 5 estrelas, até 90 dias do pedido); avaliação de produto sobre isso viola as diretrizes e pode ser denunciada. [OFICIAL] GLHXEX85MENUE4XF, G5T39MTBJSEVYQWW. A.
14. **Motivos de devolução do POE não existem para o Brasil:** a Customer Feedback API, que reproduz o POE, cobre só EUA, Reino Unido, França, Itália, Alemanha, Espanha e Japão. O diagnóstico brasileiro usa `return_reason_code` do relatório de devoluções e o relatório de devoluções FBA. [OFICIAL] developer-docs.amazon (09/09 e 06/10/2026). A (tela do POE no Brasil: B, inferência).
15. **FBA transfere atendimento, devolução e parte do risco de métrica:** dano no CD ou na transportadora é reembolsado automaticamente; item inapto é descartado após 30 dias sem reembolso; no Vem de Amazon, o DBA para em 4 estrelas (5 exige FBA ou FBA Onsite). [OFICIAL] venda.amazon.com.br/cresca/fba; /programas/vem-de-amazon. A.

---

## 2. Como funciona (mecânica e regras oficiais)

### 2.1 Saúde da conta (Estado da conta)

**Onde fica.** Menu > Estado da conta > Gerenciar estado da conta > desempenho no envio. [OFICIAL] PeBETM-rBxk (21/08/2026).

**Componentes** [OFICIAL] developer-docs.amazon/sp-api/docs/report-type-values-performance (atualizada em 06/10/2026)
- O relatório `GET_V2_SELLER_PERFORMANCE_REPORT` reproduz "as métricas do painel Account Health" do Seller Central:
  - `accountHealthRating` (`ahrStatus`, `ahrScore`);
  - `orderDefectRate` (separado em `afn` = FBA e `mfn` = envio pelo vendedor);
  - `lateShipmentRate`;
  - `preFulfillmentCancellationRate`;
  - `validTrackingRate`;
  - `onTimeDeliveryRate` e `unitOnTimeDeliveryRate`.
- Violações de política: anúncios, produtos restritos, `customerProductReviewsPolicyViolations` e outras.
- Cada métrica traz `targetValue`, `targetCondition` e período de apuração. Os valores não aparecem na documentação pública.

**Metas confirmadas para o Brasil (envio próprio e DBA)**

| Métrica | Meta | Consequência | Fonte |
|---|---|---|---|
| Envio tardio (LSR) | < 4% | Desativação de ofertas | [OFICIAL] venda.amazon.com.br/cresca/dba (lida em 15/10/2026); PeBETM-rBxk (21/08/2026); lBnzH7KSh4E (20/08/2026) |
| Cancelamento antes do envio | < 2,5% | "Pode impactar negativamente a sua loja" | [OFICIAL] PeBETM-rBxk |
| Agendamento tardio (DBA coleta) | Sem número publicado | Afeta as métricas de desempenho | [OFICIAL] lBnzH7KSh4E |
| Envio tardio e cancelamento como critério de entrada no Amazon Flash (entrega no mesmo dia) | Sem número publicado | Elegibilidade | [OFICIAL] gZ4fDdLtwBo (07/10/2026) |

**Metas globais ainda sem confirmação N1 brasileira** [OFICIAL via terceiro] SellerApp (28/09/2026; o artigo tem cabeçalho "Seller Updates 2023"); sinais fracos 6 e 7 → confiança C para janelas e B para o ODR.
- ODR < 1%, em 60 dias.
- Cancelamento < 2,5%, em 7 dias.
- Envio tardio < 4%, em 10 e 30 dias.
- Entrega no prazo > 97%, "sem penalidade atual".
- Insatisfação com devolução < 10%.
- Rastreamento válido apurado em 30 dias.
- Escala numérica da AHR (0 a 1.000 nos EUA, com faixas Saudável, Em risco e Crítico): **sem evidência** para o Brasil nesta rodada. O SellerApp só cita os status "Good", "At Risk" e "Critical".

**Isenções e contestação** [OFICIAL]
- **Atraso da transportadora DBA:** as métricas são isentadas em até 72 h (venda.amazon.com.br/cresca/dba).
- **Problema no ponto de coleta:** abrir chamado no Seller Central e avisar o gerente de operação, se houver. A equipe "vai em até 72 horas isentar as métricas" (lBnzH7KSh4E, 20/08/2026).
- **Pedido que o vendedor não reconhece como tardio ou cancelado:** Obter ajuda > "meu problema não está listado" > contestação (PeBETM-rBxk).
- **Integração:** envio sem rastreio via Amazon Track App ou transportadora integrada "vai começar a aparecer como atrasado" (gZ4fDdLtwBo).
- **Capacidade diária:** configurar a capacidade diária e os feriados protege o LSR em pico (lBnzH7KSh4E).

### 2.2 Oferta em destaque (Buy Box) e acesso a Ads

- **Requisito:** plano Profissional. A elegibilidade à oferta em destaque é "de acordo com a performance". [OFICIAL] venda.amazon.com.br/precos.
- **Critérios citados pela Amazon:**
  - preço, inclusive comparado a outros marketplaces;
  - tempo e valor de entrega;
  - métricas de saúde da conta;
  - FBA "ajuda muito";
  - a Buy Box pode variar por região (frete melhor de um concorrente na Bahia, por exemplo).
  - Fonte: [OFICIAL] nDtHI8fUEAA (20/08/2026). O algoritmo não é público.
- **Ads dependem da Buy Box:**
  - sem a oferta em destaque, a campanha de Produtos Patrocinados não entrega;
  - o anúncio fica "congelado" e não consome orçamento.
  - Fonte: [OFICIAL] 06XpeVMN7ek (17/08/2026); q0-Y5gG6Q2w (15/09/2026); thiokBBRZhA (21/08/2026).
- **Amazon Mais Vantagens (desconto Pix de 5% pago pela Amazon):**
  - dá "melhor qualificação" à oferta em destaque, que considera o preço com desconto;
  - tarifa de 2,5% a partir de 31/10/2026 (1,5% no período promocional);
  - o plano Amazon Vantagens fica em 1,5%.
  - Fonte: [OFICIAL] H0ab_x1YIBY (14/10/2026).
- **Programa Vem de Amazon (São Paulo, CNPJ):**
  - nota de 0 a 100 a cada 90 dias;
  - Logística vale até 40 pontos: cancelamento e envio tardio no DBA; ruptura e visualizações Prime no FBA e FBA Onsite;
  - Catálogo, Publicidade e Promoções valem 20 pontos cada;
  - requisitos mínimos: 5 produtos ativos e 30 pedidos;
  - o DBA chega no máximo a 4 estrelas;
  - 5 estrelas (91 a 100 pontos) dão gerente de contas por 3 meses e isenção de comissão no trimestre (até R$ 60 mil);
  - ciclos de 01/07 a 30/09/2026 e de 01/10 a 31/12/2026.
  - Fonte: [OFICIAL] venda.amazon.com.br/programas/vem-de-amazon.

### 2.3 Garantia de A a Z (lado do cliente; o vendedor arca com o custo)

Fonte: [OFICIAL] amazon.com.br nodeId=GQ37ZCNECJKTFYQV, G9VEMT3X4FQET5DH, GSZAYH7K2C2NVNC9 (sem data; lidas em 15/10/2026).

- **Cobertura:** produto vendido e enviado por vendedor parceiro com atendimento próprio. Cobre entrega no prazo e condição do produto.
- **Prazo:** menos de 90 dias desde a última data possível de entrega.
- **Gatilhos:**
  1. Não recebeu o pacote: 3 dias após a última data estimada, ou rastreio mostra entrega, e o vendedor não respondeu nem resolveu em 48 h.
  2. Pediu nota fiscal e o vendedor não enviou em 48 h.
  3. Produto danificado, com defeito ou diferente do anúncio, e o vendedor não autorizou a devolução em 48 h.
  4. O vendedor não ofereceu endereço de devolução no Brasil, etiqueta pré-paga ou reembolso sem devolução.
  5. O vendedor encerrou ou negou a devolução, ou deu etiqueta com rastreio inválido.
  6. Devolução entregue ao vendedor há 7 dias sem reembolso, ou extraviada com a etiqueta do vendedor.
  7. Cobrança extra (alfândega) não coberta.
- **Valores:** defeito ou produto diferente reembolsa produto, frete original e frete de volta. Outros motivos reembolsam produto e frete original, sem frete de volta, com possível taxa de reabastecimento.
- **Exclusões:** quem contestou no cartão (chargeback) perde a A a Z; bens digitais não são cobertos.
- **Análise:** a Amazon leva até 1 semana. O cliente pode recorrer em até 30 dias.
- **Lado do vendedor:** venda.amazon.com.br/ajuda diz que, se o vendedor não resolver, a Amazon pode reembolsar o cliente com débito na conta do vendedor [OFICIAL]. A regra de que A a Z e chargeback entram no ODR é global e vem via terceiro (SellerApp). Confiança B.

### 2.4 Devolução e reembolso

Fonte: [OFICIAL] GKM69DUUYKQWKWX7, GFLBEJCLHMVFEPA8, GKQNFKFK5CF3C54B (lidas em 15/10/2026).

**Prazos de devolução**

| Produto | Janela |
|---|---|
| Maioria dos físicos | 30 dias após a entrega |
| Comestíveis, alimentos para animais, bebidas alcoólicas | 7 dias após a entrega |
| Duráveis com defeito (eletrônicos) | 90 dias |
| Inflamáveis, colecionáveis, códigos digitais | Não retornável |

**Regras de devolução**
- O produto deve voltar "em condições novas", com embalagem e selo.
- Vendedor parceiro: responde com instruções em até 2 dias úteis. A devolução usa serviço rastreado (PAC). Itens de R$ 300 ou mais exigem seguro e assinatura.
- O vendedor paga o frete de volta quando:
  - a devolução ocorre até 7 dias após a entrega (arrependimento do CDC);
  - o defeito em bem não durável é apontado em até 30 dias;
  - o defeito em bem durável é apontado em até 90 dias.
- Fora desses casos, o vendedor pode descontar o frete de volta do reembolso.

**Por modalidade logística**
- **DBA:**
  - a Amazon emite a etiqueta pré-paga e autoriza automaticamente as devoluções elegíveis, sem tarifa de devolução ao vendedor [OFICIAL] venda.amazon.com.br/cresca/dba;
  - o cliente é reembolsado depois que o vendedor recebe e avalia o pacote;
  - passados 30 dias, o reembolso ao cliente é automático [OFICIAL] PeBETM-rBxk.
- **FBA:** o cliente devolve ao CD. Item revendável volta ao estoque. O inapto pode ser removido ou reembolsado, conforme o caso. [OFICIAL] venda.amazon.com.br/cresca/fba.
- **FBA Onsite:** o vendedor processa a devolução no sistema da Amazon, que decide o reembolso. A página é contraditória sobre quem medeia. [OFICIAL] venda.amazon.com.br/cresca/fba-onsite.

**Tarifa administrativa de reembolso:** 20% da comissão, limitada a R$ 10 (vale o menor valor), conforme a tabela mostrada em tela. A página /precos lida não exibiu essa linha. [OFICIAL via terceiro] l9MMfiAAWqo (08/10/2026; vídeo gravado em julho de 2026). Confiança B.

### 2.5 SAFE-T: reembolso ao vendedor (DBA e FBA Onsite)

Fonte: [OFICIAL] cya4LLoRX7A, webinar de Seller Coaching (28/07/2026). O FBA clássico e o envio próprio não foram cobertos.

| Cenário | DBA | FBA Onsite |
|---|---|---|
| Cliente reembolsado (não recebeu) | Abrir em até 45 dias do reembolso | Até 52 dias |
| Item devolvido com dano ou trocado ("pedra no lugar do livro") | 7 dias corridos da data da devolução | 7 dias corridos |
| Status "perdido/danificado" no retorno | Reembolso proativo em até 3 dias | Abrir em até 14 dias do status |
| Retorno não chega em 60 dias | Reembolso automático | Até 52 dias do reembolso ao cliente |
| Apelação de negativa | 7 dias corridos | 7 dias corridos |

- **Pré-condição:** sem reembolso ao cliente, não há SAFE-T.
- **Inelegível:**
  - vendedor recusou o pacote;
  - vendedor ausente em 3 ou mais tentativas;
  - endereço desatualizado;
  - embalagem inadequada (exemplo citado: vidro sem plástico-bolha).
- **Valor:** o preço de venda do item. Comissão, tarifa logística e impostos não voltam.
- **Caminho:** Pedidos > Gerenciar reivindicações SAFE-T > Registrar > Verificar elegibilidade. A conferência fica em Pagamentos > Visualizar transações (marcado "SAFE-T claim ID").

### 2.6 Avaliações de produto e feedback do vendedor

**Quem avalia e como a nota é calculada** [OFICIAL] G8UYX7LALQC8V9KA, G75XTB7MBMBTXP6W, GLHXEX85MENUE4XF
- Só avalia quem gastou R$ 50 na amazon.com.br nos últimos 12 meses com cartão. Descontos promocionais não contam.
- O selo "Compra verificada" exige que o avaliador tenha comprado na Amazon e pago o preço disponível à maioria dos clientes. Logo, unidade muito descontada pode perder o selo.
- A nota geral por estrelas usa modelos de IA com recência e compra verificada, não média simples.
- Avaliação sem compra verificada fica fora da nota até ganhar texto, imagem ou vídeo.
- Avaliações em idioma diferente do português são proibidas na amazon.com.br.

**O que não pode estar na avaliação de produto** [OFICIAL] GLHXEX85MENUE4XF
- vendedor e atendimento;
- problemas com pedido ou devolução;
- embalagem de envio;
- condição e dano do produto;
- custo e velocidade do frete.
- Esses temas vão para o feedback do vendedor.

**Proibições**
- conteúdo do próprio vendedor ou de parentes, funcionários, sócios e concorrentes;
- avaliação negativa de vendedor sobre produto concorrente;
- avaliações criadas, editadas ou removidas em troca de recompensa: dinheiro, vale-presente, desconto, produto grátis ou reembolso;
- exemplos vedados citados pela Amazon: vale no pacote condicionado a avaliação positiva; reembolso oferecido para mudar avaliação negativa.

**Consequências:** remoção do conteúdo, remoção de produtos relacionados, suspensão ou encerramento da conta e retenção de pagamentos. [OFICIAL] GLHXEX85MENUE4XF; G5T39MTBJSEVYQWW.

**Feedback do vendedor** [OFICIAL] G5346HRPNJFYRA49, G5T39MTBJSEVYQWW, GL8DXVU3MMGKKXT7
- de 1 a 5 estrelas, com a média exibida ao lado do nome do vendedor;
- o cliente tem até 90 dias da data do pedido;
- o botão aparece até 3 dias após a conclusão;
- o cliente pode remover, mas não editar;
- a Amazon remove comentário sobre preço, conteúdo promocional e avaliação de produto colocada no lugar errado.

**Solicitação de avaliação** [OFICIAL] SP-API, modelo `solicitations.json` e guia "Solicit feedback for an order" (09/09/2026)
- Uma única solicitação por pedido, por API ou pelo botão "Solicitar avaliação".
- Uma segunda tentativa retorna erro 403. O botão do Seller Central acusa que o pedido já foi solicitado.
- O pedido único combina avaliação do produto e feedback do vendedor.
- Proibido:
  - pedir seletivamente a quem teve boa experiência;
  - pedir alteração de avaliação existente;
  - oferecer recompensa.
- Resolvido o problema, o vendedor pode pedir uma vez a remoção de feedback negativo (`createNegativeFeedbackRemoval`).
- A API lista as regiões NA, EU e FE. O Brasil opera na região NA da SP-API (inferência; a lista de marketplaces não foi lida).
- **Janela:** a documentação oficial diz só "dentro do prazo permitido". Terceiros divergem: 4 a 30 dias da compra (Jungle Scout, 05/03/2024) ou 5 a 30 dias após a entrega (Helium 10, 2021). Fica como faixa, confiança C. O SellerBoard mostra 10 dias após a entrega como configuração de praticante (AuWtJJ_708Q).

**Vine** [OFICIAL] venda.amazon.com.br/vine (lida em 15/10/2026); sell.amazon.com/programs/vine (EUA)
- **Requisitos:**
  - plano Profissional;
  - representante da marca ou revendedor autorizado no Brand Registry;
  - oferta FBA "Novo" com estoque;
  - menos de 30 avaliações.
  - Ficam fora: adultos, digitais, pacotes e volumosos.
- **Custo por produto pai no Brasil:**
  - até 2 unidades: R$ 0;
  - 3 a 10: R$ 200;
  - 11 a 30: R$ 500;
  - mais comissão e custos FBA das unidades reivindicadas.
  - Nos EUA: US$ 0, US$ 75 e US$ 200.
- **Cobrança:** só após a 1ª avaliação. Sem avaliação em 90 dias, nada é cobrado.
- **Cancelamento:** depois que uma unidade é reivindicada, não dá mais para cancelar nem reinscrever.
- **Avaliadores:** os Vine Voices são convidados pela qualidade das avaliações anteriores. A página não exige nota positiva.
- **Promessa:** "até 30%" de vendas, com asterisco sem explicação.
- **Prazo:** a avaliação chega de 4 a 8 semanas após o envio (Jungle Scout, 09/10/2023, EUA; confiança C).

**Ferramentas que não estão confirmadas no Brasil**
- **Customer Reviews (contatar avaliador crítico, abaixo de 3 estrelas, com oferta de reembolso):** confirmado só nos EUA (sell.amazon.com/tools/customer-reviews). Brasil sem evidência.
- **Customer Service by Amazon (CSBA, atendimento terceirizado do envio próprio):** só EUA, Alemanha e Japão (sell.amazon.com/programs/customer-service-by-amazon).

### 2.7 Atendimento: canais e SLA

- **Antes da compra:** o cliente pergunta pelo "Fazer uma pergunta" na página do vendedor. **Depois da compra:** usa Seus pedidos > Problema com o pedido. Em ambos os casos, a resposta do vendedor deve sair em até 2 dias úteis. [OFICIAL] GLC8ZMBWMBTR6QZZ.
- **Mensagens:** o canal comprador-vendedor aceita anexos (PDF, JPG, PNG, XML, até 10 MB). A Amazon remove e-mails e links "não fidedignos". O cliente pode bloquear mensagens não solicitadas. [OFICIAL] G3JQ9V9LQ8FFMR7W.
- **FBA e DBA:** a Amazon cuida dos contatos pós-venda, 24/7 no FBA. [OFICIAL] venda.amazon.com.br/cresca/fba; /cresca/dba; gVHIZsn3dbA (17/08/2026).
  - No DBA, o reembolso ao cliente segue com o vendedor; o canal de reivindicação é o SAFE-T.
- **Nota fiscal:** pedido de NF sem resposta em 48 h abre A a Z. Pedido de comprovante de autenticidade exige NF anterior ao cadastro, segundo praticante (d4EH8e36Z7g).

### 2.8 Suspensão, bloqueio e propriedade intelectual

- **Causas citadas:**
  - produto proibido;
  - preço baixo demais;
  - reclamações de consumidores;
  - falsificação;
  - denúncia de fabricante. A mais comum seria venda sem autorização da marca.
  - Fonte: [PRÁTICA] jOLN_O6O3aw (advogado, 03/09/2026; sinais fracos 1, 3 e 5 → N7).
- **Saldo:** retenção de saldo por mais de 90 dias seria contestável na Justiça, segundo o advogado. Nos EUA, os fundos ficam retidos 90 dias antes do desembolso final (Helium 10, 2023, confiança C).
- **Plano de ação (EUA):** reconhecer o problema, causa raiz, correção e prevenção, em 1 a 2 páginas, com exemplos por ASIN. Fonte: [DADO/PRÁTICA] Helium 10 (08/09/2023; pode estar superada).
- **Marca:** quem tem o registro no INPI pode notificar via Brand Protection. Reiteração "pode ensejar inclusive no bloqueio da sua conta". Fonte: [PRÁTICA] T3J04yzlV28 (advogada em podcast, 15/06/2026). [MARCA] e [REVENDA].

---

## 3. O que os melhores fazem

### 3.1 Práticas com consenso (duas ou mais fontes independentes)

- **Tratar a saúde da conta como pré-requisito de evento (Black Friday, Prime):**
  - responder todas as perguntas e devoluções;
  - medir diariamente a conversão de Buy Box;
  - investigar por que perde a Buy Box (preço, avaliação da loja ou entrega).
  - "Regra de ouro: saúde da conta... e estoque".
  - Fontes: [PRÁTICA] VH7Q5FddoRY (Smollan, agência, 19/08/2026); [OFICIAL] nDtHI8fUEAA; q0-Y5gG6Q2w.
- **Usar FBA para tirar o atendimento e a devolução da operação no pico:**
  - FBA na curva A;
  - Prime visível;
  - menos risco de envio tardio.
  - Fontes: [PRÁTICA] VH7Q5FddoRY; [OFICIAL] venda.amazon.com.br/cresca/fba; gZ4fDdLtwBo. Na Amazon, o FBA dá selo Prime e, segundo o webinar, "melhores avaliações" (gZ4fDdLtwBo).
- **Configurar capacidade diária, feriados e horário de corte no Seller Central** para não estourar o LSR em pico. Fontes: [OFICIAL] lBnzH7KSh4E; [PRÁTICA] PeBETM-rBxk (perguntas de vendedores sobre galpão terceirizado sem acesso ao painel).
- **Pedir avaliação de forma sistemática e uniforme:**
  - botão ou API em todo pedido entregue;
  - ferramentas de automação (SellerBoard, Helium 10, Jungle Scout) apertam o botão por API.
  - Fontes: [PRÁTICA] AuWtJJ_708Q (24/06/2026); Helium 10 (2021); Jungle Scout (2024); [OFICIAL] SP-API.
- **Vine no lançamento de produto de marca,** antes de escalar Ads. Fontes: [PRÁTICA] VK7jalYzwxc (03/08/2026: Vine e depois Ads, 15 vendas em 15 dias); [OFICIAL] venda.amazon.com.br/vine. [MARCA]
- **Responder avaliações e perguntas como parte do atendimento,** não só o WhatsApp. Fontes: [PRÁTICA] pSoQ2xvfF5s (Jess, mentora, 01/09/2026); VH7Q5FddoRY ("avaliações em dia respondidas, pergunta ativa").
- **Medir devolução em duas camadas:**
  - "sistêmica": o que o painel mostra;
  - "operacional": o que de fato chega, inclusive caixa vazia ou produto trocado;
  - cortar SKU "curva A" com devolução alta.
  - Fontes: [PRÁTICA] SqoNj2DDRSU (consultora financeira, 02/06/2026; multicanal). Amarra com a janela de 7 dias do SAFE-T para item trocado (cya4LLoRX7A).
- **Organizar documentação fiscal por CNPJ e por conta:**
  - a reclamação de autenticidade exige nota fiscal;
  - sem NF coerente com a conta, o estoque fica preso.
  - Fontes: [PRÁTICA] d4EH8e36Z7g (Ariadne, mentora, 22/04/2026: cerca de R$ 35 mil de estoque perdido, produto de 300 a 400 unidades/mês, por volta de 2023; relato sem base comparativa, portanto PRÁTICA e não CASE); jOLN_O6O3aw. [REVENDA] principalmente.
- **Embalar para o pior trajeto,** porque embalagem inadequada tira o SAFE-T. Fontes: [OFICIAL] cya4LLoRX7A; [PRÁTICA] pSoQ2xvfF5s (embalagem como custo de preço).

### 3.2 Divergências entre fontes

- **Janela do pedido de avaliação:** 4 a 30 dias da compra (Jungle Scout, 2024) contra 5 a 30 dias após a entrega (Helium 10, 2021). A Amazon só diz "prazo permitido". → faixa de 4 a 30 dias, com confiança C.
- **Taxa de avaliação por venda:**
  - 1 avaliação a cada 100 vendas, ou seja, cerca de 1% (AuWtJJ_708Q, 2026, Brasil, sem base);
  - "cerca de 1 a 3%" antes do botão de 2020 (Helium 10, EUA);
  - 4% a 20% de avaliações e notas por unidade com o botão ou e-mail (Helium 10, EUA, 2020, produtos próprios).
  - Fica como faixa de 1% a 20%, dependente de categoria e país. O dado brasileiro não tem metodologia publicada.
- **Ganho de vendas do FBA:**
  - "4x" (venda.amazon.com.br/cresca/fba, "dados internos Amazon 2025");
  - "20 a 25% mais" (webinar gVHIZsn3dbA, 17/08/2026).
  - Ambas são da Amazon e sem metodologia. Fica a faixa, nunca a média.
- **Excluir quem deu feedback negativo da solicitação automática:** a praticante recomenda (AuWtJJ_708Q). A documentação oficial proíbe pedir seletivamente a quem teve boa experiência (SP-API, 09/09/2026). → **risco de violação**: a fonte forte desmente a fraca (ver seção 6).
- **Mensagem personalizada no pedido de avaliação:** a praticante mostra texto livre via SellerBoard (AuWtJJ_708Q). Helium 10 (2020) diz que alterar os modelos da Amazon pode violar as diretrizes de comunicação. O caminho oficial é o modelo fixo da Solicitations API. → divergência, com confiança C para o lado da praticante.
- **FBA Onsite, quem medeia a devolução:** a página oficial se contradiz (venda.amazon.com.br/cresca/fba-onsite).

### 3.3 Margem de segurança interna (métricas usadas abaixo do limite)

- **Sem evidência N1 a N6 brasileira** de que operações publiquem metas internas, como "LSR interno de 2%".
- O que existe:
  - praticantes recomendam monitoramento diário (SqoNj2DDRSU; VH7Q5FddoRY);
  - a Amazon recomenda manter o LSR "o mais baixo possível" (lBnzH7KSh4E).
- **Método derivado (princípio, não regra; confiança C):**
  - a meta dá a margem em pedidos: com 400 pedidos de envio próprio no período, 4% são 16 envios tardios, e 2,5% de cancelamento são 10 pedidos;
  - em conta pequena, um único pedido pesa muito;
  - por isso o FBA reduz o denominador exposto, já que as métricas de envio só se aplicam ao envio pelo vendedor (SellerApp; `orderDefectRate` separado em afn e mfn).
- **Programa Vem de Amazon como termômetro trimestral:** pontuação de Logística com cancelamento e atraso (DBA) ou ruptura (FBA). [OFICIAL]

---

## 4. Números de referência

| Item | Valor | Tipo | Fonte | Data | Confiança |
|---|---|---|---|---|---|
| Envio tardio (LSR), meta Brasil | < 4% | OFICIAL | venda.amazon.com.br/cresca/dba; PeBETM-rBxk | 15/10/2026; 21/08/2026 | A |
| Cancelamento antes do envio, meta Brasil | < 2,5% | OFICIAL | PeBETM-rBxk | 21/08/2026 | B (fonte única N1) |
| ODR | < 1%, 60 dias | OFICIAL via terceiro (global) | SellerApp | 28/09/2026 | B |
| Janelas: cancelamento 7 d; LSR 10 e 30 d; VTR 30 d | — | OFICIAL via terceiro (global) | SellerApp | 28/09/2026 | C |
| Entrega no prazo (OTDR) | > 97%, sem penalidade | OFICIAL via terceiro (global) | SellerApp | 28/09/2026 | C |
| Insatisfação com devolução | < 10% | OFICIAL via terceiro (global) | SellerApp | 28/09/2026 | C |
| Isenção por atraso da transportadora DBA | até 72 h | OFICIAL | /cresca/dba; lBnzH7KSh4E | 2026 | A |
| A a Z: prazo do cliente | < 90 dias da última data de entrega | OFICIAL | GQ37ZCNECJKTFYQV | lida em 15/10/2026 | A |
| A a Z: gatilho de inação do vendedor | 48 h | OFICIAL | GQ37ZCNECJKTFYQV | lida em 15/10/2026 | A |
| A a Z: recurso do cliente / análise | 30 dias / até 1 semana | OFICIAL | G9VEMT3X4FQET5DH; GSZAYH7K2C2NVNC9 | lida em 15/10/2026 | A |
| Resposta do vendedor a mensagem e devolução | até 2 dias úteis | OFICIAL | GLC8ZMBWMBTR6QZZ; GKM69DUUYKQWKWX7 | lida em 15/10/2026 | A |
| Devolução: geral / comestíveis / durável com defeito | 30 / 7 / 90 dias | OFICIAL | GKM69DUUYKQWKWX7 | lida em 15/10/2026 | A |
| Frete de volta pago pelo vendedor | arrependimento ≤ 7 d; defeito não durável ≤ 30 d; durável ≤ 90 d | OFICIAL | GFLBEJCLHMVFEPA8 | lida em 15/10/2026 | A |
| Devolução de R$ 300+ | seguro e assinatura | OFICIAL | GKM69DUUYKQWKWX7 | lida em 15/10/2026 | A |
| DBA: reembolso automático ao cliente | 30 dias sem avaliação do vendedor | OFICIAL | PeBETM-rBxk | 21/08/2026 | B |
| Tarifa administrativa de reembolso | 20% da comissão, máx. R$ 10 | OFICIAL via terceiro | l9MMfiAAWqo | 08/10/2026 | B |
| SAFE-T DBA / FBA Onsite (cliente reembolsado) | 45 / 52 dias | OFICIAL | cya4LLoRX7A | 28/07/2026 | B |
| SAFE-T item devolvido com problema; apelação | 7 dias; 7 dias | OFICIAL | cya4LLoRX7A | 28/07/2026 | B |
| SAFE-T perda/dano: DBA / FBA Onsite | automático em 3 d / abrir em 14 d | OFICIAL | cya4LLoRX7A | 28/07/2026 | B |
| Prazo padrão de retorno da devolução | 60 dias | OFICIAL | cya4LLoRX7A | 28/07/2026 | B |
| FBA: item "não apto" armazenado | até 30 dias, depois descarte sem reembolso | OFICIAL | /cresca/fba | lida em 15/10/2026 | A |
| Gasto mínimo para avaliar | R$ 50 em 12 meses | OFICIAL | G8UYX7LALQC8V9KA; GLHXEX85MENUE4XF | lida em 15/10/2026 | A |
| Feedback do vendedor: prazo do cliente | 90 dias do pedido | OFICIAL | G5T39MTBJSEVYQWW | lida em 15/10/2026 | A |
| Solicitação de avaliação | 1 por pedido | OFICIAL | SP-API | 09/09/2026 | A |
| Janela da solicitação | 4–30 d (compra) a 5–30 d (entrega) | DADO (faixa) | Jungle Scout; Helium 10 | 2024; 2021 | C |
| Vine Brasil: custo por produto pai | R$ 0 (≤2 un) / R$ 200 (3–10) / R$ 500 (11–30) | OFICIAL | venda.amazon.com.br/vine | lida em 15/10/2026 | A |
| Vine: limite de avaliações para entrar | < 30 | OFICIAL | venda.amazon.com.br/vine; sell.amazon.com/programs/vine | 2026 | A |
| Vine: tempo até a avaliação | 4–8 semanas | DADO | Jungle Scout (EUA) | 09/10/2023 | C |
| Taxa de avaliação por unidade | ~1% (Brasil, sem base) a 4–20% (EUA, 2020) | DADO/PRÁTICA (faixa) | AuWtJJ_708Q; Helium 10 | 2026; 2021 | C |
| Vem de Amazon: Logística | até 40 de 100 pontos; DBA máx. 4 estrelas | OFICIAL | /programas/vem-de-amazon | lida em 15/10/2026 | A |
| Amazon Mais Vantagens | 2,5% a partir de 31/10/2026 | OFICIAL | H0ab_x1YIBY | 14/10/2026 | B |
| CSBA (EUA): melhora de ODR | 38% (jan.–mar. 2022, dado da própria Amazon) | DADO (Amazon, sem metodologia) | sell.amazon.com/programs/customer-service-by-amazon | 2022 (pode estar superada) | C |
| Líderes de café: avaliações | Orfeu 16.737 (4,7); Baggio 10.981 (4,8); Coffee Mais 2.254 (4,7); Italle 1.647 (4,5) | OBS | observacao/lideres.tsv | 14/10/2026 | A (observação direta) |

---

## 5. Alimentos, perecíveis e marca própria/indústria

- **Janela curta de devolução:** comestíveis, ração e bebidas alcoólicas têm 7 dias após a entrega, contra 30 dias da maioria. [OFICIAL] GKM69DUUYKQWKWX7.
  - Na prática, essa janela coincide com o arrependimento do CDC, em que o vendedor paga o frete de volta (GFLBEJCLHMVFEPA8).
  - A exigência de "condições novas" com selo do fabricante limita a revenda do item devolvido.
- **FBA com alimento devolvido:**
  - o item inapto fica no máximo 30 dias e é descartado sem reembolso se não houver pedido de remoção [OFICIAL] /cresca/fba;
  - para alimento aberto ou violado, o padrão esperado é descarte; a regra específica para comestíveis devolvidos não foi lida (lacuna).
- **Embalagem é variável de reputação e de dinheiro:**
  - embalagem inadequada derruba o SAFE-T [OFICIAL] cya4LLoRX7A;
  - reclamação de avaria ou embalagem não deve ficar na avaliação do produto, que pode ser denunciada; ela vai para o feedback do vendedor [OFICIAL] GLHXEX85MENUE4XF;
  - para alimento (vidro, pó, grão), o risco de avaria pesa nas duas frentes.
- **Prova social dos líderes da categoria:**
  - [OBS] lideres.tsv (14/10/2026): Café Orfeu Grãos 1 kg, vendido e enviado pela Amazon (1P), tem 16.737 avaliações e nota 4,7. Baggio tem 10.981 (4,8). Coffee Mais tem 2.254 (4,7), com selo "Escolha da Amazon". A Italle, 3P marca com FBA, tem 1.647 (4,5).
  - Os patrocinados na busca "café em grãos" são de marcas com menos avaliações.
  - Leitura: os líderes de alimentos são majoritariamente 1P, e o atendimento e a devolução são da Amazon.
  - [MARCA] 3P em alimentos concorre com isso usando FBA (Prime, atendimento Amazon) e Ads.
- **Vine para marca de alimentos:**
  - exige Brand Registry, FBA e menos de 30 avaliações; ficam fora apenas adultos, digitais, pacotes e volumosos;
  - alimento não aparece como excluído [OFICIAL] venda.amazon.com.br/vine;
  - "pacotes" (bundles) não são elegíveis, o que atinge kits.
  - [MARCA]
- **Recorrência (Programe e Poupe):** aparece nos líderes de consumo recorrente (Italle, Lysoform) [OBS]. Em produto de recompra, a praticante segmenta a solicitação de avaliação para clientes novos (AuWtJJ_708Q) [PRÁTICA]. Não foi lida regra oficial sobre o efeito disso.
- **Nota fiscal e rastreabilidade:** a reclamação de autenticidade pede NF. Para marca própria, o registro no INPI e o Brand Registry protegem contra notificações de terceiros (T3J04yzlV28; venda.amazon.com.br/brand-registry). [MARCA]
- **Sem evidência nesta rodada:**
  - regras de validade mínima para alimentos no FBA Brasil;
  - categoria Alimentos e Bebidas exigir aprovação;
  - exigências da Anvisa no anúncio.
  - Ficam para a frente alimentos-marca-propria.

---

## 6. Erros comuns e mitos

1. **"Pode excluir da solicitação quem deu feedback negativo ou neutro"** (AuWtJJ_708Q, 24/06/2026).
   - A Amazon proíbe pedir seletivamente avaliações positivas (SP-API, 09/09/2026).
   - Excluir clientes insatisfeitos é a forma típica de seleção.
   - Fonte forte desmente fonte fraca. O vídeo tem 4 sinais fracos: CTA dominante (link de afiliado "dois meses grátis" e WhatsApp comercial), conflito de interesse (afiliado), promessa ("hack que ninguém passa") e número sem base ("1 a cada 100 vendas").
2. **"Avaliação ruim por causa de embalagem ou atraso fica para sempre"**: falso. Essas reclamações violam as diretrizes da avaliação de produto e podem ser denunciadas; o lugar delas é o feedback do vendedor. [OFICIAL] GLHXEX85MENUE4XF. A remoção não é garantida: depende da análise da Amazon.
3. **"Oferecer reembolso ou brinde em troca de avaliação é aceitável se a avaliação for honesta"**: falso. Qualquer recompensa, inclusive desconto ou reembolso, é proibida. A punição vai até a suspensão e a retenção de pagamentos. [OFICIAL] GLHXEX85MENUE4XF.
4. **"Ads compensam reputação ruim"**: sem a oferta em destaque, os Produtos Patrocinados não entregam, e a oferta em destaque considera as métricas da conta. [OFICIAL] 06XpeVMN7ek, nDtHI8fUEAA.
5. **"No DBA o vendedor não tem nada a ver com devolução"**: parcial.
   - A Amazon emite a etiqueta e não cobra tarifa de devolução.
   - O reembolso ao cliente continua com o vendedor, e o prejuízo depende de abrir o SAFE-T no prazo (7, 45 dias...).
   - [OFICIAL] /cresca/dba; cya4LLoRX7A.
6. **"SAFE-T devolve tudo"**: devolve o preço do item. Comissão, tarifa logística e impostos não voltam. [OFICIAL] cya4LLoRX7A.
7. **"Recusar a devolução protege a margem"**: recusar o pacote, estar ausente 3 vezes ou ter endereço desatualizado anula o SAFE-T. [OFICIAL] cya4LLoRX7A.
8. **Limites de AHR (0 a 1.000, 200 e 100) vendidos como brasileiros:** são números da Amazon EUA (sinal fraco 7). Nesta rodada não houve confirmação de que a escala é idêntica no Brasil. O campo `ahrScore` existe na API global.
9. **"Saldo retido é ilegal após 90 dias e se resolve em 1 a 2 semanas"** (jOLN_O6O3aw): afirmação de advogado com CTA de serviço, sem caso, período ou base. Sinais fracos 1, 3 e 5 → N7, hipótese.
10. **Estatísticas de blog sem fonte:**
    - "Com 5 avaliações, conversão cerca de 270% maior" (sell.amazon.com/blog, 18/08/2026, texto feito com IA e sem fonte);
    - "84% confiam em avaliações como em amigos" (G2, via Helium 10 2020, sem amostra).
    - Sinal fraco 2. Não usar como benchmark.
11. **Confundir avaliação do produto com feedback do vendedor:** são sistemas distintos, com regras e prazos próprios (90 dias para o feedback). O feedback do vendedor pesa na Buy Box segundo praticantes (social/notas.md: "abaixo de 85%" de feedback positivo, teoria de 14/08/2024, pode estar superada).

---

## 7. Revenda/importação x indústria/marca própria

**[REVENDA] revenda, importação e genérico**
- **Buy Box compartilhada:**
  - a disputa é por preço, entrega e métricas da conta [OFICIAL] nDtHI8fUEAA;
  - a reputação define quem leva a venda no mesmo ASIN, como nos 53 vendedores do suporte de notebook em lideres.tsv [OBS];
  - Ads só rodam com a Buy Box.
- **Risco de conta maior:**
  - denúncia de marca e reclamação de autenticidade exigem NF anterior e coerente com o CNPJ da conta (d4EH8e36Z7g; jOLN_O6O3aw);
  - "venda sem autorização da marca" é a causa de bloqueio mais citada pelo advogado (N7).
- **Ferramentas de avaliação:**
  - o Vine e as respostas a avaliações exigem papel de representante da marca ou revendedor autorizado no Brand Registry, o que limita o revendedor comum [OFICIAL] /vine;
  - a solicitação de avaliação (1 por pedido) vale para todos.
- **Atendimento:** com envio próprio ou DBA, o SLA de 2 dias úteis e os gatilhos de 48 h da A a Z recaem sobre o vendedor.

**[MARCA] indústria e marca própria**
- **Prova social construída do zero:**
  - Vine (até 30 unidades, menos de 30 avaliações, FBA);
  - solicitação uniforme em todo pedido;
  - a nota é calculada por modelo com peso de recência, então uma sequência ruim recente pesa mais [OFICIAL] G8UYX7LALQC8V9KA.
- **Proteção:** Brand Registry com marca registrada ou pedido no órgão nacional; denúncia de violação; Projeto Zero. [OFICIAL] venda.amazon.com.br/brand-registry. A marca registrada é a defesa contra notificação de terceiros (T3J04yzlV28).
- **Diagnóstico de produto:**
  - Brand Analytics existe no Brasil [OFICIAL] /brand-registry;
  - os tópicos de avaliação e devolução do POE (Customer Feedback API) não estão disponíveis para o Brasil [OFICIAL] developer-docs;
  - a marca brasileira faz a leitura manual das avaliações e dos códigos de motivo dos relatórios de devolução.
- **Ferramentas EUA ainda não confirmadas no Brasil:** Customer Reviews (contatar avaliador crítico) e CSBA.

---

## 8. Tabela de afirmações

| id | Afirmação | Tipo | Fonte | Data | Confiança |
|---|---|---|---|---|---|
| A1 | No DBA, o vendedor deve manter envio tardio abaixo de 4% para evitar desativação de ofertas. | OFICIAL | venda.amazon.com.br/cresca/dba; PeBETM-rBxk; lBnzH7KSh4E | lida em 15/10/2026; 21/08/2026 | alta |
| A2 | Meta de cancelamento antes do envio no DBA: 2,5%. | OFICIAL | PeBETM-rBxk | 21/08/2026 | média |
| A3 | ODR global < 1% em 60 dias; o painel separa ODR de FBA e de envio próprio. | OFICIAL via terceiro + OFICIAL (campo) | SellerApp; developer-docs Performance Reports | 28/09/2026; 06/10/2026 | média |
| A4 | O painel de saúde da conta inclui AHR (status e pontuação), ODR, LSR, cancelamento, VTR, OTDR e violações de política, inclusive de avaliações. | OFICIAL | developer-docs.amazon/sp-api/docs/report-type-values-performance | 06/10/2026 | alta |
| A5 | Atraso da transportadora DBA tem as métricas isentadas em até 72 h; problema no ponto de coleta exige chamado. | OFICIAL | /cresca/dba; lBnzH7KSh4E | 20/08/2026 | alta |
| A6 | Envio tardio ou cancelamento não reconhecido é contestado por chamado (Obter ajuda > meu problema não está listado). | OFICIAL | PeBETM-rBxk | 21/08/2026 | média |
| A7 | A oferta em destaque considera preço, prazo e custo de entrega e métricas da conta; métricas ruins tiram a Buy Box até de vendedor único. | OFICIAL | nDtHI8fUEAA | 20/08/2026 | média |
| A8 | Produtos Patrocinados só entregam com a oferta em destaque; sem ela, o anúncio congela e não gasta. | OFICIAL | 06XpeVMN7ek; q0-Y5gG6Q2w; thiokBBRZhA | 17/08 a 15/09/2026 | alta |
| A9 | Envio tardio e cancelamento são critério de elegibilidade ao Amazon Flash (entrega no mesmo dia). | OFICIAL | gZ4fDdLtwBo | 07/10/2026 | média |
| A10 | Garantia de A a Z: até 90 dias da última data de entrega; gatilhos de 48 h sem resposta ou solução do vendedor. | OFICIAL | amazon.com.br GQ37ZCNECJKTFYQV | lida em 15/10/2026 | alta |
| A11 | Pedido de nota fiscal sem resposta em 48 h permite A a Z. | OFICIAL | GQ37ZCNECJKTFYQV | lida em 15/10/2026 | alta |
| A12 | Chargeback no cartão torna o cliente inelegível à A a Z; recurso do cliente em 30 dias. | OFICIAL | GQ37ZCNECJKTFYQV; G9VEMT3X4FQET5DH | lida em 15/10/2026 | alta |
| A13 | O vendedor deve responder mensagens e instruções de devolução em até 2 dias úteis. | OFICIAL | GLC8ZMBWMBTR6QZZ; GKM69DUUYKQWKWX7; GKQNFKFK5CF3C54B | lida em 15/10/2026 | alta |
| A14 | Devolução: 30 dias na maioria; 7 dias para comestíveis, ração e bebidas alcoólicas; 90 dias para durável com defeito. | OFICIAL | GKM69DUUYKQWKWX7 | lida em 15/10/2026 | alta |
| A15 | O vendedor paga o frete de volta em arrependimento até 7 dias e em defeito (30 dias não durável, 90 dias durável). | OFICIAL | GFLBEJCLHMVFEPA8 | lida em 15/10/2026 | alta |
| A16 | No DBA, a Amazon emite a etiqueta e autoriza a devolução sem tarifa de devolução ao vendedor. | OFICIAL | /cresca/dba | lida em 15/10/2026 | alta |
| A17 | No DBA, o reembolso ao cliente é automático 30 dias após a devolução sem avaliação do vendedor. | OFICIAL | PeBETM-rBxk | 21/08/2026 | média |
| A18 | Tarifa administrativa de reembolso: 20% da comissão, limitada a R$ 10. | OFICIAL via terceiro | l9MMfiAAWqo | 08/10/2026 | média |
| A19 | SAFE-T só após reembolso ao cliente: DBA 45 dias, FBA Onsite 52 dias; item devolvido com problema, 7 dias; apelação, 7 dias. | OFICIAL | cya4LLoRX7A | 28/07/2026 | média |
| A20 | No DBA, perda ou dano no retorno tem reembolso proativo em até 3 dias; no FBA Onsite, abrir em até 14 dias. | OFICIAL | cya4LLoRX7A | 28/07/2026 | média |
| A21 | SAFE-T é negado por embalagem inadequada, recusa do pacote, 3 ausências ou endereço errado; reembolsa só o preço do item. | OFICIAL | cya4LLoRX7A | 28/07/2026 | média |
| A22 | FBA: dano no CD ou pela transportadora é reembolsado automaticamente; item inapto é descartado após 30 dias sem reembolso. | OFICIAL | /cresca/fba | lida em 15/10/2026 | alta |
| A23 | Só avalia quem gastou R$ 50 em 12 meses; a nota por estrelas usa IA (recência, compra verificada), não média simples. | OFICIAL | G8UYX7LALQC8V9KA; GLHXEX85MENUE4XF | lida em 15/10/2026 | alta |
| A24 | Avaliação de produto não pode tratar de vendedor, embalagem, dano, frete ou prazo; esses temas vão ao feedback do vendedor. | OFICIAL | GLHXEX85MENUE4XF | lida em 15/10/2026 | alta |
| A25 | Avaliação em troca de dinheiro, vale, desconto, produto grátis ou reembolso é proibida; punição vai até suspensão e retenção de pagamento. | OFICIAL | GLHXEX85MENUE4XF; G5T39MTBJSEVYQWW | lida em 15/10/2026 | alta |
| A26 | Feedback do vendedor: 1 a 5 estrelas, até 90 dias do pedido; o cliente remove, mas não edita. | OFICIAL | G5T39MTBJSEVYQWW; GL8DXVU3MMGKKXT7 | lida em 15/10/2026 | alta |
| A27 | Uma solicitação de avaliação por pedido; proibido pedir seletivamente, pedir alteração ou incentivar. | OFICIAL | SP-API Solicitations (modelo e guia) | 09/09/2026 | alta |
| A28 | A janela da solicitação vai de 4–30 dias da compra a 5–30 dias após a entrega, conforme a fonte. | DADO (faixa) | Jungle Scout; Helium 10 | 05/03/2024; 2021 | baixa |
| A29 | Vine Brasil: Brand Registry, FBA, < 30 avaliações; R$ 0 / R$ 200 / R$ 500 por produto pai; cobra após a 1ª avaliação. | OFICIAL | venda.amazon.com.br/vine | lida em 15/10/2026 | alta |
| A30 | A avaliação do Vine leva 4 a 8 semanas para chegar (EUA). | DADO | Jungle Scout | 09/10/2023 | baixa |
| A31 | Os tópicos de avaliação e devolução do POE (Customer Feedback API) não estão disponíveis no Brasil. | OFICIAL | developer-docs Customer Feedback API | 09/09/2026 | alta |
| A32 | O relatório de devoluções do envio próprio traz `return_reason_code` e `a_to_z_claim`; a devolução FBA usa relatório próprio. | OFICIAL | developer-docs Returns Reports | 06/10/2026 | alta |
| A33 | Vem de Amazon: Logística vale até 40 de 100 pontos; DBA máx. 4 estrelas; 5 estrelas exige FBA ou FBA Onsite. | OFICIAL | /programas/vem-de-amazon | lida em 15/10/2026 | alta |
| A34 | Customer Reviews (contatar avaliador crítico) e CSBA só estão confirmados nos EUA (CSBA: EUA, Alemanha e Japão). | OFICIAL | sell.amazon.com/tools/customer-reviews; /programs/customer-service-by-amazon | 2026 | média |
| A35 | Saúde da conta é "número um" para evento; o maior erro na Black Friday anterior foi ruptura de estoque. | PRÁTICA | VH7Q5FddoRY (agência Smollan) | 19/08/2026 | baixa |
| A36 | Praticante configura a solicitação automática 10 dias após a entrega e exclui pedidos com feedback negativo (este último conflita com A27). | PRÁTICA | AuWtJJ_708Q | 24/06/2026 | baixa |
| A37 | Uma avaliação a cada 100 vendas é a referência citada por praticante brasileira. | PRÁTICA (número sem base) | AuWtJJ_708Q | 24/06/2026 | baixa |
| A38 | Taxa de avaliações e notas por unidade de 4% a 20% em produtos próprios nos EUA (2020); cerca de 1 a 3% antes do botão. | DADO | Helium 10 | 11/03/2021 | baixa |
| A39 | Estoque de cerca de R$ 35 mil ficou preso por falta de NF coerente com o CNPJ da conta após reclamação de autenticidade. | PRÁTICA | d4EH8e36Z7g | 22/04/2026 (fato de ~2023) | baixa |
| A40 | Denúncia de marca via Brand Protection pode levar a bloqueio de conta se reiterada. | PRÁTICA | T3J04yzlV28 | 15/06/2026 | baixa |
| A41 | Devolução deve ser medida em duas camadas, a do painel e a operacional (o que chega de fato). | PRÁTICA | SqoNj2DDRSU | 02/06/2026 | baixa |
| A42 | Ganho de vendas com FBA: "4x" (página) a "20–25%" (webinar), ambos dados internos sem metodologia. | DADO (faixa) | /cresca/fba; gVHIZsn3dbA | 2025; 17/08/2026 | baixa |
| A43 | Líderes de café na Amazon são majoritariamente 1P, com 2.254 a 16.737 avaliações e notas de 4,5 a 4,8. | OBS | observacao/lideres.tsv | 14/10/2026 | alta |
| A44 | Amazon Mais Vantagens melhora a qualificação para a oferta em destaque; tarifa de 2,5% a partir de 31/10/2026. | OFICIAL | H0ab_x1YIBY | 14/10/2026 | média |

---

## 9. Lacunas

1. **Central de Ajuda do Seller Central Brasil (login obrigatório):** não foram lidos o texto oficial brasileiro das metas de desempenho do cliente (ODR, janelas), a política de atendimento, a escala da AHR no Brasil, a política de comunicação comprador-vendedor e a página "Solicitar uma avaliação". Os limites globais vieram via terceiro (SellerApp), com confiança B ou C.
2. **Escala numérica da AHR no Brasil (0 a 1.000?) e se o programa de Account Health Rating está ativo no Brasil:** sem evidência. Só existe o campo na API global.
3. **Janela oficial do botão "Solicitar avaliação":** a documentação diz apenas "prazo permitido"; os terceiros divergem (4 ou 5 a 30 dias).
4. **Metas internas com margem de segurança:** nenhuma operação brasileira publica números internos (por exemplo, LSR interno ou ODR interno). Sem evidência.
5. **Benchmarks brasileiros de taxa de avaliação por venda, taxa de devolução por categoria e ODR médio:** não há estudo público com metodologia. As ferramentas consultadas (Jungle Scout, Helium 10) trazem dados dos EUA de 2020 a 2024; o relatório Jungle Scout 2025 (cerca de 1.500 vendedores, jan. 2025) não traz achados sobre reputação.
6. **Product Opportunity Explorer no Seller Central Brasil:** a ausência da Customer Feedback API para o Brasil sugere que os tópicos de avaliação e devolução do POE não existem aqui, mas a tela não foi vista (exige login).
7. **Customer Reviews (contato com avaliador crítico), resposta pública a avaliações e CSBA no Brasil:** sem evidência.
8. **Regras de alimentos no FBA Brasil** (validade mínima no recebimento, descarte de devolvidos comestíveis, aprovação de categoria): não lidas.
9. **SAFE-T no envio próprio e no FBA clássico, e reembolso FBA por estoque perdido:** o webinar cobriu só DBA e FBA Onsite, e a página do FBA não menciona estoque perdido.
10. **Tarifa administrativa de reembolso:** só vista em tela de praticante; a página /precos lida não a exibiu.
11. **Pesquisas web:** o limite de buscas do turno acabou antes desta frente. As fontes foram lidas por URL direta. Uma nova rodada de busca pode trazer o fórum do Seller Central Brasil, a Nubimetrics para Amazon e a Marketplace Pulse.

## 10. Verificação (2026-10-14)

Método: leitura direta de páginas oficiais (venda.amazon.com.br, developer-docs.amazon). As páginas de ajuda do comprador em amazon.com.br (nodeId GQ37ZCNECJKTFYQV, GKM69DUUYKQWKWX7, GFLBEJCLHMVFEPA8, GLC8ZMBWMBTR6QZZ) retornaram HTTP 503 e o limite de buscas do turno acabou; o Seller Central exige login. Sem leitura oficial, o veredito é SEM FONTE OFICIAL (não significa que o dado esteja errado). Regras de plataforma com mais de 6 meses "podem estar superadas". Tipo de todas as fontes abaixo: [OFICIAL].

| id | veredito | fonte oficial (URL) | observação |
|---|---|---|---|
| A1 | CONFIRMADA | https://venda.amazon.com.br/cresca/dba (lida 14/10/2026) | A página exige índice de envios tardios abaixo de 4% e cita desativação de ofertas. Só conta atraso causado pelo vendedor; prazo de preparo padrão no DBA é 0 dia, ajustável por SKU. |
| A2 | SEM FONTE OFICIAL | https://venda.amazon.com.br/cresca/dba (não cita a métrica) | A página DBA não menciona meta de cancelamento antes do envio. O webinar PeBETM-rBxk não foi reverificado. Não confirmar o 2,5%. |
| A3 | SEM FONTE OFICIAL | https://developer-docs.amazon/sp-api/docs/report-type-values-performance | Confirma só que o relatório separa ODR em afn (Amazon) e mfn (envio próprio). Os campos targetValue/targetCondition vêm sem valor e sem duração; 1% e 60 dias não aparecem. |
| A5 | CONFIRMADA | https://venda.amazon.com.br/cresca/dba (lida 14/10/2026) | A página diz que atraso causado pela transportadora parceira do DBA é isento "em até 72h". A condição "com chamado aberto" e o ponto de coleta não foram verificados. |
| A8 | SEM FONTE OFICIAL | não localizada (a FAQ de Amazon Ads em pt-br retornou 404) | Só webinars de praticantes. Não confirmar. |
| A10 | SEM FONTE OFICIAL | https://www.amazon.com.br/gp/help/customer/display.html?nodeId=GQ37ZCNECJKTFYQV (HTTP 503) | 90 dias e gatilho de 48 h não verificados nesta rodada. |
| A13 | SEM FONTE OFICIAL | https://www.amazon.com.br/gp/help/customer/display.html?nodeId=GLC8ZMBWMBTR6QZZ (HTTP 503) | Prazo de 2 dias úteis não verificado. |
| A14 | SEM FONTE OFICIAL | https://www.amazon.com.br/gp/help/customer/display.html?nodeId=GKM69DUUYKQWKWX7 e nodeId=GFLBEJCLHMVFEPA8 (HTTP 503) | Janelas de 30/7/90 dias e frete de devolução não verificados. |
| A18 | SEM FONTE OFICIAL | https://venda.amazon.com.br/precos (lida 14/10/2026) | A página mostra comissão de 10% a 15% e mínimo de R$ 1,00, mas não cita tarifa administrativa de reembolso (20%, teto R$ 10). A ausência não refuta; segue só em tela de praticante. |
| A19 | SEM FONTE OFICIAL | https://venda.amazon.com.br/cresca/fba (não cita SAFE-T) | Prazos de 45, 52, 7 e 3 dias só vieram de webinar, não reverificado. A página FBA diz apenas que itens danificados são reembolsados automaticamente. |
| A27 | CONFIRMADA | https://developer-docs.amazon/sp-api/docs/solicit-feedback-for-an-order (lida 14/10/2026) | Uma solicitação por pedido (a segunda dá 403). Proibido pedir só a quem avaliou bem, pedir alteração de avaliação ou oferecer recompensa. A lista exata de incentivos (vale, desconto, etc.) e a página brasileira GLHXEX85MENUE4XF não foram lidas. |
| A29 | CONFIRMADA | https://venda.amazon.com.br/vine (lida 14/10/2026) | Valores batem (R$ 0 até 2 un., R$ 200 de 3 a 10, R$ 500 de 11 a 30, por produto pai; filhos sem custo). Cobra só após a 1ª avaliação publicada; sem avaliação em 90 dias, sem cobrança. Detalhes: conta Profissional, oferta FBA em condição Novo, ser dono da marca ou revendedor autorizado no Brand Registry, menos de 30 avaliações. Tarifas e FBA das unidades enviadas continuam valendo. |

Resumo: 4 confirmadas, 0 contestadas, 8 sem fonte oficial lida. Uma nova rodada com as páginas de ajuda do comprador (se saírem do 503) e o Seller Central fecharia A10, A13, A14 e A19.

## 11. Verificação pelo navegador (2026-10-15)

Método: Chrome renderizando JavaScript; leitura das páginas públicas de ajuda (amazon.com.br/gp/help e ajuda do Seller Central, só leitura), advertising.amazon.com/pt-br e venda.amazon.com.br. Sem captcha. Páginas sem data visível (s/d).

| id | veredito | fonte oficial | observação |
|---|---|---|---|
| A2 | SEM FONTE OFICIAL | https://sellercentral.amazon.com.br/help/hub/reference/G200285210 ; https://sellercentral.amazon.com.br/help/hub/reference/G201379690 | A página do Índice de cancelamento (CR) define a métrica (pedidos com envio pelo vendedor), mas não dá meta em %. A página do Delivery by Amazon não traz meta de cancelamento. Também procurei na busca da ajuda do Seller Central. Os 2,5% seguem só no webinar. |
| A3 | CONFIRMADA | https://sellercentral.amazon.com.br/help/hub/reference/G200285170 | ODR menor que 1% calculado sobre 60 dias, formado por avaliação negativa, A a Z e estorno. Acima de 1% pode suspender as ofertas com envio pelo vendedor. A separação FBA/envio próprio vem do developer-docs (rodada anterior). |
| A8 | PARCIAL | https://advertising.amazon.com/pt-br/solutions/products/sponsored-products | A fonte oficial exige que o produto seja elegível à oferta em destaque, não que já a tenha. "Congela e não gasta" sem a oferta em destaque não aparece. Atenção: a ajuda do Seller Central diz que a partir de set/2026 deixa de haver requisitos de qualificação para a oferta em destaque. |
| A10 | CONFIRMADA | https://www.amazon.com.br/gp/help/customer/display.html?nodeId=GQ37ZCNECJKTFYQV | Os gatilhos de 48 h estão confirmados: vendedor sem resposta ou solução, nota fiscal não enviada e devolução não autorizada. Também há gatilhos de 3 dias após a última data estimada de entrega e de 7 dias após a devolução ser entregue sem reembolso. |
| A13 | CONFIRMADA | https://www.amazon.com.br/gp/help/customer/display.html?nodeId=GKM69DUUYKQWKWX7 ; https://www.amazon.com.br/gp/help/customer/display.html?nodeId=GLC8ZMBWMBTR6QZZ | A página de contato com o vendedor diz que ele responde por e-mail em até dois dias úteis. Se não responder, o cliente pode acionar a Garantia de A a Z. |
| A14 | CONFIRMADA | https://www.amazon.com.br/gp/help/customer/display.html?nodeId=GKM69DUUYKQWKWX7 ; https://www.amazon.com.br/gp/help/customer/display.html?nodeId=GQ37ZCNECJKTFYQV | 30 dias para a maioria, 7 dias para comestíveis, ração e bebidas alcoólicas, e 90 dias para bens duráveis com defeito. Frete de devolução (tabela da A a Z): reembolsado só para produto danificado, com defeito ou diferente. |
| A18 | CONFIRMADA | https://sellercentral.amazon.com.br/help/hub/reference/G200387220 | A fórmula oficial é 20% x (comissão x valor reembolsado), com teto de R$ 10,00 por item. |
| A19 | PARCIAL | https://sellercentral.amazon.com.br/help/hub/reference/GNGYMYPKATHYPHJN ; https://sellercentral.amazon.com.br/help/hub/reference/G201988660 | Confirmado: o prazo de 7 dias corridos conta a partir de "devolvido/entregue ao vendedor" ou da notificação de reembolso, o que vier depois. Contestado: o recurso tem prazo de 5 dias úteis, não 7. Os prazos de 45 e 52 dias não aparecem. No DBA com devolução por envio próprio, o pedido vai de 30 a 60 dias. A política de reembolso do DBA dá 60 dias após o último evento da transportadora. |
