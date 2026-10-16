# Amazon Brasil: logística, frete e estoque (notas do analista)

Frente: logistica-estoque. Plataforma: Amazon Brasil, com referência à Amazon EUA quando a mecânica é a mesma.
Data da análise: 2026-10-14. Pesquisa neutra: descreve como os melhores operam. Não traz recomendação para nenhuma empresa.

**Base usada**
- 12 transcrições da frente e 8 transcrições correlatas da pasta (ids abaixo). Das 20, 11 são webinars do canal oficial "Venda com a Amazon Brasil", gravados entre jul e out/2026. Quando um funcionário da Amazon afirma uma regra em webinar oficial, a nota marca [OFICIAL via webinar].
- 10 páginas oficiais lidas em 2026-10-14: venda.amazon.com.br/precos, /cresca/fba, /cresca/dba, /cresca/fba-onsite, /termos/experimente-fba, /termos/frete19, /central-de-treinamento-fba (índice, "gerenciamento-de-inventario", "criacao-de-um-envio") e sell.amazon.com/fulfillment-by-amazon (EUA). As páginas de ajuda do Seller Central (ex. G201030350, requisitos do FBA) exigem login e não abriram. Ficaram de fora.
- 5 fontes de dados: Jungle Scout (relatório State of the Amazon Seller 2025, artigos sobre IPI, tarifas FBA e gestão de estoque) e Helium 10 (gestão de estoque). Todas tratam da Amazon EUA.
- Observação de líderes: `observacao/lideres.tsv` (2026-10-14).
- Limite: a cota de busca na web da sessão acabou antes desta frente. Por isso as fontes de dados foram abertas por URL direta, e a camada de dados ficou mais fina que o ideal.

Convenções. Tipos: [OFICIAL], [OFICIAL via webinar], [PRÁTICA], [CASE], [DADO] e [OBS]. Confiança A, B ou C, conforme o protocolo. Toda regra de plataforma anterior a 2026-04-14, ou sem data, leva "(pode estar superada)". [REVENDA] e [MARCA] separam o que é específico de cada modelo.

---

## 1. Resumo executivo

1. **Há quatro modalidades.** No **FBA** a Amazon armazena, embala, entrega e atende; a oferta ganha selo Prime. No **FBA Onsite** o estoque fica no armazém do vendedor, opera no sistema da Amazon e tem selo Prime; é restrito a parceiros convidados. No **DBA** o vendedor embala e a Amazon coleta ou recebe no ponto de postagem. Na **logística própria (MFN/FBM)** o vendedor entrega e define o frete. Fontes: venda.amazon.com.br/precos e /cresca/fba-onsite (lidas em 2026-10-14) [OFICIAL] e `0rnXQha3Eew` [PRÁTICA]. Confiança A.
2. **Entrada no FBA:** CNPJ ativo na Sefaz e emitindo NF-e, Simples Nacional ou Regime Normal (MEI aceito), certificado A1 e uso do Faturador da Amazon. A inscrição estadual precisa estar em SP, MG, PR, RJ, SC, RS, CE, DF, PE, BA, GO ou ES. Para outros estados existe o Programa de Filiais. Não há mínimo de vendas nem de unidades. Fontes: /cresca/fba [OFICIAL] e `crnP1JO2B1o` (2026-09-04) [OFICIAL via webinar]. Confiança A.
3. **Tabela padrão do FBA:** armazenagem de **R$ 75/m³/mês** para itens abaixo de 10.000 cm³ e de **R$ 37,50/m³/mês** para os maiores. A **armazenagem de longo prazo** custa **R$ 525/m³**, soma-se à mensal e incide sobre estoque com mais de 365 dias. A tarifa logística vai de R$ 10,05 (0 a 100 g, preço abaixo de R$ 30) a dezenas de reais nos itens pesados. A remoção custa de R$ 0,99 a R$ 3,60 por unidade. Fontes: /precos e /cresca/fba [OFICIAL], tarifas de 01/08/2025 (pode estar superada; vigentes na página em 14/10/2026). Confiança A.
4. **Campanha "Experimente FBA 3.0" (01/07/2026 a 31/01/2027).** Conta nova tem 30 dias com logística, coleta e armazenagem isentas. Conta existente paga **R$ 6,00 fixos** por unidade de produto com preço a partir de R$ 79 e não paga coleta nem armazenagem. A condição é investir **3,5% da receita em Amazon Ads**, ou, para contas anteriores a 01/04/2026, 1 ponto percentual acima do que investiam em abril de 2026. A validação é no dia 20 de cada mês e o efeito vale no mês seguinte. Fonte: venda.amazon.com.br/termos/experimente-fba [OFICIAL]. Confiança A.
5. **Inventário "não apto para venda"** (danificado, vencido ou com defeito) precisa de pedido de remoção em até **30 dias**; depois disso é descartado sem reembolso. Fontes: /cresca/fba e /central-de-treinamento-fba/gerenciamento-de-inventario [OFICIAL], `k0v5Yw5h5NQ` [OFICIAL via webinar]. Confiança A.
6. **Cobertura recomendada pela Amazon: 5 semanas.** Estoque de 60 a 90 dias deve ir para promoção e o acima de 90 dias, para remoção. A entrega em horas exige cerca de 4 semanas de cobertura. Fontes: `k0v5Yw5h5NQ` (2026-09-11) e `gZ4fDdLtwBo` (2026-10-07) [OFICIAL via webinar]. Confiança B.
7. **A capacidade de envio ao CD é medida em m³ e separada por tipo** (tamanho padrão, extragrande e perigosos). Ela depende do Índice de Desempenho de Inventário (IDI), que a Amazon considera saudável a partir de 700, e pode ser revista sob pedido. Um produto em excesso, por exemplo com 10 semanas de cobertura contra as 5 recomendadas, pode ter limite próprio. Fontes: `k0v5Yw5h5NQ` [OFICIAL via webinar] e /gerenciamento-de-inventario [OFICIAL]. Confiança B.
8. **Picos:** a Amazon e as agências recomendam enviar de 2 a 4 semanas antes do evento. Fora de pico, o recebimento leva de 3 a 7 dias; perto de sazonalidade, 2 a 3 semanas. A coleta pode ficar para 2 semanas depois. Fontes: `zdDPzE7jftg`, `q0-Y5gG6Q2w` e `VvcswcsjuUw` [OFICIAL via webinar], `VH7Q5FddoRY` [PRÁTICA, agência Smollan]. Confiança A.
9. **O efeito da logística na conversão** só tem fonte da própria Amazon, sem método publicado: "vendas crescem 4x em média" (dado interno de 2025), "80% dos clientes são Prime" e "membros Prime gastam 2,5x". Fontes: /cresca/fba e `zdDPzE7jftg` [OFICIAL, sem método]. Não há estudo independente. Confiança B para "existe efeito positivo"; o tamanho do efeito fica sem evidência.
10. **Promessa de entrega = tempo de preparo + trânsito + feriados.** Desde 2026, o tempo de preparo padrão da conta no DBA e na logística própria é fixo em **0 dia**. Prazo maior só por produto (ASIN), de 1 a 30 dias. Promessa mais curta ganha visibilidade e conversão (afirmação qualitativa da Amazon). Fontes: `lBnzH7KSh4E` (2026-08-20) [OFICIAL via webinar] e /cresca/dba [OFICIAL]. Confiança A.
11. **DBA:** a modalidade Postagem atende quem tem média de até 9 pacotes por dia e a Coleta, quem tem 10 ou mais. O limite é de 30 kg por pacote. As metas são envio tardio abaixo de 4% e cancelamento antes do envio abaixo de 2,5%. A regra geral é: pedido até 11h, agendamento até 11h30 e entrega no ponto até 14h, com variação por região. Fontes: /cresca/dba [OFICIAL] e `PeBETM-rBxk` (2026-08-21) [OFICIAL via webinar]. Confiança A.
12. **Ruptura:** sem estoque, ou sem a Buy Box, o anúncio patrocinado é suspenso ("congelado") e não gasta orçamento. Fonte: `q0-Y5gG6Q2w` [OFICIAL via webinar], confiança B. A Amazon também diz que faltar estoque logo após o pico desperdiça o ranqueamento conquistado (`VvcswcsjuUw`, Head de FBA, confiança B). Nenhuma fonte mede quanto tempo a posição leva para voltar (sem evidência).
13. **A Amazon redistribui o estoque FBA entre CDs** por conta própria e sem custo; o vendedor não escolhe o CD. A redistribuição só acontece com estoque suficiente ("cinco unidades não espalham"). Fontes: `VvcswcsjuUw` e `k0v5Yw5h5NQ` [OFICIAL via webinar]. Confiança B.
14. **Alimentos:** as regras públicas e abertas da Amazon Brasil não detalham prazo mínimo de validade, lote nem temperatura no FBA. Elas estão na ajuda do Seller Central, que exige login. O que se sabe por webinar: a etiqueta não pode cobrir a validade, o recebimento confere a validade, item vencido não é reembolsado e a armazenagem segue a classificação da vigilância sanitária. Fontes: `zdDPzE7jftg`, `k0v5Yw5h5NQ` e `-7TGtIYZX0U` [OFICIAL via webinar]. Confiança B.
15. **Entre os líderes de café na Amazon Brasil**, os anúncios observados mostram "Entrega GRÁTIS amanhã". Em 4 de 5 casos a venda é 1P (Amazon compra da marca e revende); a Italle vende como 3P com FBA. Fonte: `observacao/lideres.tsv` (2026-10-14) [OBS]. Confiança B.

---

## 2. Como funciona (mecânica e regras oficiais)

### 2.1 Modalidades e regras de entrada

| Modalidade | Quem armazena e embala | Quem entrega | Selo Prime | Entrada | Fonte |
|---|---|---|---|---|---|
| FBA | Amazon (CD) | Amazon | Sim | CNPJ na Sefaz, Faturador, A1, IE em um dos 12 estados (ou filial); NCM e origem na oferta | /cresca/fba; `crnP1JO2B1o` |
| FBA Onsite | Vendedor, no sistema da Amazon | Amazon coleta no armazém do vendedor | Sim | Restrito e limitado a alguns parceiros, mediante avaliação | /cresca/fba-onsite |
| DBA | Vendedor | Amazon (AMZL, Total Express, Correios) | Não | CPF, MEI ou CNPJ; padrão para novos vendedores desde 05/08/2024 | /cresca/dba |
| Logística própria (MFN) | Vendedor | Transportadora escolhida pelo vendedor | Não | Qualquer conta; produto perigoso ou fora dos limites do DBA cai aqui | /precos; `lBnzH7KSh4E` |
| Amazon Flash (DBA ou MFN) | Vendedor | Transportadora homologada ou frota própria, no mesmo dia | Não | São Paulo capital, CEPs configuráveis; formulário de interesse | `gZ4fDdLtwBo` |

- **Lista de estados com FBA.** A página oficial (2026-10-14) traz 12 unidades: SP, MG, PR, RJ, SC, RS, CE, DF, PE, BA, GO e ES. O webinar de 04/09/2026 fala em "10 estados mais o DF". A Head de FBA anunciou CDs na Bahia e no Espírito Santo e outro no Paraná para meados de outubro de 2026 (`VvcswcsjuUw`). Prevalece a página oficial. [OFICIAL]
- **Programa de Filiais:** permite abrir filial em um estado com CD, no endereço do CD ou no próprio. A Amazon subsidia a abertura e cobra os custos de quem sair. Fonte: /cresca/fba [OFICIAL].
- **Passo a passo do FBA** (`crnP1JO2B1o`, `zdDPzE7jftg`, `VvcswcsjuUw`) [OFICIAL via webinar]: configurar o Faturador (Regime Normal também sobe planilhas fiscais; há conversor da planilha "full" do Mercado Livre ou da Shopee), com série de NF exclusiva para a Amazon; duplicar a oferta (SKU "_FBA") em vez de converter; criar o envio, etiquetar e agendar a coleta. Certificado A1 vencido bloqueia as ofertas; a orientação é renovar com um mês de antecedência.

### 2.2 Tarifas do FBA (tabela padrão, sem campanha)

| Item | Valor | Fonte e data |
|---|---|---|
| Tarifa logística | Por unidade, conforme faixa de preço (abaixo de R$ 30, R$ 30 a 49,99, R$ 50 a 78,99, R$ 79 a 99,99, R$ 100 a 119,99, R$ 120 a 149,99, R$ 150 a 199,99, acima de R$ 200) e peso. Vai de R$ 10,05 (0 a 100 g, abaixo de R$ 30) a R$ 51,35 (9 a 10 kg). Kg adicional: R$ 3,05 a R$ 3,50 | /precos, /cresca/fba; atualização de 01/08/2025 (pode estar superada) |
| Peso cobrado | O maior entre o peso real e o dimensional (C×L×A ÷ 6000), mais 20 g de embalagem; tabela até 22 kg | idem |
| Armazenagem mensal | R$ 75,00/m³ (abaixo de 10.000 cm³); R$ 37,50/m³ (a partir de 10.000 cm³); cobrada no mês seguinte pela média diária de volume | idem; no webinar: "R$ 2,50/m³/dia" e "R$ 1,25 com 50% de desconto" para itens grandes (`crnP1JO2B1o`) |
| Armazenagem de longo prazo | R$ 525,00/m³ para inventário com mais de 365 dias, somada à mensal | idem; no webinar: "R$ 17,50/m³/dia" (`crnP1JO2B1o`) |
| Remoção | R$ 0,99 (0 a 250 g) a R$ 3,60 (9 a 10 kg), mais R$ 0,17 por kg adicional | /precos |
| Coleta | Por caixa, por estado de origem e peso; SP: R$ 0,93 a R$ 2,92 até 3 kg | /precos |
| Comissão | 10% a 15% por categoria; mínimo de R$ 1,00 (em algumas categorias, R$ 2,00); atualização de 20/01/2025 (pode estar superada) | /precos |
| Comissão promocional | 5% para produtos novos elegíveis ao Prime, nas primeiras 100 unidades (50 se extragrande), por até 120 dias | /cresca/fba |

Observações:
- Na extração automática, a tabela da tarifa logística ficou com colunas desalinhadas nas faixas acima de R$ 79. Os valores por célula precisam de conferência visual em /precos.
- Os webinars oficiais citam R$ 5,65, R$ 5,85 e R$ 6,05 (ou 6,50, conforme a fala) como tarifa fixa para itens abaixo de R$ 79 na campanha. Os termos da campanha não confirmam esses valores, porque o Anexo 2 abriu incompleto. Conflito em aberto (ver Lacunas).

### 2.3 Campanha "Experimente FBA 3.0" (termos lidos em 2026-10-14)

- **Vigência:** de 01/07/2026 a 31/01/2027. Última validação mensal em 20/12/2026.
- **Status da conta:** é "conta existente" quem teve inventário ativo ou envio aceito entre 01/01/2025 e 31/07/2026.
- **Conta nova:** 100% de isenção em logística, coleta e armazenagem por 30 dias, contados da primeira oferta ativa no FBA.
- **Conta existente:** R$ 6,00 por unidade de produto com preço a partir de R$ 79; coleta e armazenagem zeradas em qualquer faixa de preço.
- **Condição:** investimento efetivamente gasto (não o orçamento alocado) de 3,5% da receita total dos 30 dias anteriores. Contas ativadas antes de 01/04/2026 também podem cumprir com 1 ponto percentual acima do percentual de abril/2026.
  - Divergência: a Head de FBA disse "em relação a maio" (`VvcswcsjuUw`). Os termos dizem abril. Prevalecem os termos.
- **Efeito:** quem bate a meta no mês tem o benefício no mês seguinte, a partir do dia 1º. Quem não bate volta à tabela padrão e pode recuperar o benefício depois.
- **Limites:** a Amazon pode limitar o número de ASINs elegíveis e mudar os critérios com 15 dias de aviso.

### 2.4 Envio ao CD (inbound)

Regras citadas nos webinars de ago/set/2026 (`crnP1JO2B1o`, `k0v5Yw5h5NQ`, `VvcswcsjuUw`) [OFICIAL via webinar]:
- Até 200 caixas por envio com coleta Amazon. Cada caixa tem no máximo 22 kg e lado maior de até 100 cm (o sistema bloqueia acima disso).
- Cada unidade leva a etiqueta FNSKU ("X00..."), colada sobre o código de barras original. A exceção são celulares. Não se colam duas etiquetas X00 sobrepostas.
- Cada caixa leva 2 etiquetas, e a NF de remessa vai em uma delas.
- Caixa de papelão obrigatória. Ração é o único item aceito sem caixa master. Saco de lixo é recusado.

Pela página /cresca/fba [OFICIAL]:
- Tamanho padrão vai até 45×35×20 cm ou 9 kg; acima disso, o item é extragrande.
- Pacote do produto: lado de até 100 cm, soma de até 200 cm, girth de até 295 cm e peso de até 22 kg.

Divergência com página antiga sem data, /criacao-de-um-envio (pode estar superada):
- Caixa master de até 105×105×72 cm e 30 kg.
- Armazenagem inicial de 625 unidades (pequenos), 300 (grandes) e 200 (perigosos).
- Penalidade por "no-show" na coleta nas últimas 4 semanas: 3 a 4 ocorrências cortam 20% da capacidade; 5 ou mais, 40%.

Outras regras de inbound: coleta cancelável em até 24h; liberação de CEP para coleta em 15 a 21 dias, sem garantia; o envio pode ser dividido entre CDs de pequenos e grandes (GRU8 e XCV9 em SP) (`k0v5Yw5h5NQ`). A Amazon não prepara nem monta kits: o kit chega pronto, em saco, com uma etiqueta (`zdDPzE7jftg`, `VvcswcsjuUw`).

### 2.5 Gestão de inventário dentro do FBA

- **Ferramentas citadas nos webinars:** coluna "semanas de cobertura" (atualização D-1), página "Envie mais para o FBA / Produtos recomendados" e "Relatório de inventário". Esse relatório traz excedente, unidades a enviar para evitar ruptura e data-limite de envio. Também existem as abas "Sem oferta ativa" e "Não apto para venda" e o painel "Desempenho de inventário". Fontes: `zdDPzE7jftg`, `k0v5Yw5h5NQ`, `VvcswcsjuUw` [OFICIAL via webinar].
- **Quando aparecem as recomendações:** a recomendação de reposição usa o histórico. Em conta nova, ela leva "cerca de 3 meses" para aparecer (`VvcswcsjuUw`). O IDI também só fica disponível após 3 meses (/gerenciamento-de-inventario) [OFICIAL].
- **Remoção:** prazo normal de 14 dias úteis; 30 dias úteis ou mais em pico. Existe remoção automática do inventário não apto, que pode rodar 1 ou 2 vezes por mês. Fontes: /gerenciamento-de-inventario [OFICIAL, sem data, pode estar superada] e `k0v5Yw5h5NQ`.
- **Reembolso** (`k0v5Yw5h5NQ`) [OFICIAL via webinar]: automático para perda ou dano no CD ou na transportadora da Amazon e fraude de cliente; nenhum para defeito de origem, devolução por defeito e item vencido; sob investigação para perda no inbound e dano na remoção.
- **Divergência de contagem no recebimento:** contesta-se com a NF de remessa (`VvcswcsjuUw`).
- **Entrega em horas (FBA):**
  - Amazon leva estoque de alta demanda a CDs dedicados em SP e RJ, sem custo ao vendedor e sem adesão.
  - Requisitos: cerca de 4 semanas de cobertura, oferta vencedora (Buy Box) e demanda regional.
  - Ficam fora os itens extragrandes, de alto valor e perigosos.
  - Fonte: `gZ4fDdLtwBo` (2026-10-07) [OFICIAL via webinar].

### 2.6 DBA, logística própria e promessa de entrega

- **Tempo de preparo:** o padrão da conta é 0 dia e não pode ser alterado. Por ASIN, vai de 1 a 30 dias, e a orientação é ser fiel ao prazo real (`lBnzH7KSh4E`).
- **Horário de corte:** no DBA é definido pela Amazon, sempre em "meia hora" (9h30, 10h30, 11h30). Na logística própria, o mínimo é 11h.
- **Capacidade de pedidos (OHC):** pedidos acima da capacidade diária informada recebem promessa de um dia a mais.
- **DBA, limites:** postagem até 9 pacotes por dia e coleta a partir de 10 (/cresca/dba). No webinar, o limite de pacote é soma de até 200 cm, até 30 kg e lado de até 100 cm. Produto acima disso ou perigoso cai para envio próprio (`PeBETM-rBxk`).
- **DBA, tarifas por unidade:** R$ 4,50 (abaixo de R$ 30), R$ 6,50 (R$ 30 a 49,99) e R$ 6,75 (R$ 50 a 78,99). Acima de R$ 79, a tabela varia por peso e região (/precos). Uma mentora citou desconto de 50% em SP acima de R$ 79 (`l9MMfiAAWqo`, [PRÁTICA], não confirmado na página).
- **DC-e:** vendedores CPF no DBA têm a Declaração de Conteúdo eletrônica emitida pela Amazon a partir de 15/09/2026, com implantação gradual. No envio próprio, o vendedor emite a DC-e por conta própria (`OBY9LjwvhnA`) [OFICIAL via webinar].
- **SAFE-T** (`cya4LLoRX7A`, 2026-07-28) [OFICIAL via webinar]: reclamação em até 45 dias do reembolso ao cliente no DBA e 52 no FBA Onsite; item devolvido com problema e apelo, 7 dias cada; retorno da devolução em até 60 dias; reembolso proativo do DBA em até 3 dias após "perdido/danificado"; cobre só o preço do item, não as tarifas.

### 2.7 Frete grátis ao cliente

| Faixa do pedido | FBA / FBA Onsite | DBA | Fonte |
|---|---|---|---|
| Abaixo de R$ 19 | Só cliente Prime | Frete pago | /termos/frete19 (início em 15/08/2025, pode estar superada) |
| R$ 19 a R$ 79 | Grátis, entrega em 3 dias ou mais | Grátis se origem e destino estão na mesma região | idem |
| Acima de R$ 79 | Grátis, com entrega nacional em até 1 dia onde houver | Grátis entre regiões | idem |

- **Conflito sobre o não-Prime.** /cresca/fba diz que o cliente não-Prime tem frete grátis no FBA a partir de R$ 129. /cresca/fba-onsite fala em R$ 99 para livros e R$ 149 para os demais. Os três números não batem com /termos/frete19 (ver Lacunas).
- **Entrega em horas:** grátis a partir de R$ 19, exceto mercearia e livros, que exigem a partir de R$ 79. Abaixo disso, o frete é R$ 8,90 para Prime e R$ 10,90 para não-Prime (`gZ4fDdLtwBo`) [OFICIAL via webinar].

---

## 3. O que os melhores fazem

### 3.1 Consenso (fontes independentes concordam)

- **P1. FBA para a curva A; DBA ou MFN para a cauda.**
  - A Amazon recomenda enviar "curva A ou B" (`crnP1JO2B1o`).
  - A agência Smollan diz que "pelo menos uma parte" das ofertas da curva A deve estar em FBA (`VH7Q5FddoRY`).
  - Capellete coloca o DBA para produto caro, personalizado ou de estado sem FBA (social `7664720778054602005`).
  - Confiança A.
- **P2. Oferta dupla no mesmo ASIN.**
  - Um SKU FBA e um SKU DBA/MFN: quando o FBA zera, a oferta própria assume a Buy Box. Fontes: `02Bn3HyAYqk` (Capellete, 2026-07-30, com tela) [PRÁTICA] e `VH7Q5FddoRY` ("ofertas híbridas, plano B") [PRÁTICA].
  - A Amazon recomenda duplicar em vez de converter, porque o integrador reverte oferta híbrida (`zdDPzE7jftg`).
  - Ponto de atenção: com uma oferta única, quando o FBA acaba a venda passa automaticamente ao DBA (`k0v5Yw5h5NQ`).
  - Confiança A.
- **P3. Reposição proativa por cobertura, não por ruptura.**
  - A Amazon fala em 5 semanas (`k0v5Yw5h5NQ`); um praticante, em 30 a 45 dias de demanda (`78sSkRh2crI`); a Jungle Scout, em cerca de 60 dias, tratando como excesso o que passa de 90 dias (EUA, 2023, pode estar superada).
  - Faixa de consenso: **30 a 60 dias de cobertura**.
  - Confiança B.
- **P4. Envio antecipado para picos.**
  - A Amazon fala em pelo menos 2 semanas (`q0-Y5gG6Q2w`) e em "o quanto antes", com agendas que ficam restritas perto da Black Friday (`VvcswcsjuUw`).
  - A Smollan fala no ideal de 1 mês antes, mínimo de 15 a 20 dias (`VH7Q5FddoRY`).
  - Faixa: **15 a 30 dias antes do evento**. Confiança A.
- **P5. Não deixar a oferta de pico zerar.**
  - Limitar a quantidade da oferta relâmpago ou do cupom e voltar ao preço normal antes de acabar. Exemplo citado: com 1.000 unidades, encerrar a oferta quando restam 100.
  - O motivo dado é que "ranquear de novo é um pouco mais complexo" (`VH7Q5FddoRY`).
  - A Head de FBA dá a mesma leitura do outro lado: ruptura depois do pico desperdiça o efeito halo (`VvcswcsjuUw`).
  - Confiança B.
- **P6. Higiene de inventário mensal.**
  - Zerar "sem oferta ativa", remover o não apto antes de 30 dias (ou ligar a remoção automática), liquidar com promoção aos 60 a 90 dias e remover acima de 90.
  - Esses itens também pesam no IDI e, portanto, na capacidade.
  - Fontes: `k0v5Yw5h5NQ` e `q0-Y5gG6Q2w` [OFICIAL via webinar]; Jungle Scout (IPI EUA, 2023).
  - Confiança A.
- **P7. Preparação para reduzir divergência:** um SKU por caixa com "CASE" escrito, variantes em caixas separadas, fita em tampa de rosca, foto da caixa e NF de remessa guardada (`k0v5Yw5h5NQ`, `VvcswcsjuUw`). Confiança B.
- **P8. Teste com poucas unidades e escala pelo giro:** mandar pouco da curva A na isenção de 30 dias e repor o que gira (`VvcswcsjuUw`). Na revenda, 3 unidades por SKU, dobrando as que giram (social `DeQMMCSsL03`, Europa) [PRÁTICA, REVENDA]. Limite: lote raso não entra na redistribuição entre CDs nem na entrega em horas. Confiança B.

### 3.2 Como decidem o que vai para o fulfillment

Procedimento que aparece nas fontes, em ordem:
1. **Giro e curva ABC.** Começar pelo relatório "Vendas e tráfego por ASIN" e pela página de produtos recomendados (`zdDPzE7jftg`, `VvcswcsjuUw`).
2. **Ser o primeiro FBA do ASIN.** Se ninguém vende o ASIN em FBA, vale testar mesmo fora da curva A (`VvcswcsjuUw`, gerente de contas Amazon) [OFICIAL via webinar, opinião].
3. **Faixa de preço contra tarifa.** Acima de R$ 79, a tarifa fixa de R$ 6 da campanha torna o FBA mais barato que o DBA, que pela tabela fica acima de R$ 6,75. Abaixo de R$ 79, as diferenças são pequenas (`l9MMfiAAWqo` [PRÁTICA], /precos [OFICIAL]). Praticantes testam preços como R$ 78,90 e R$ 90 para mudar de faixa (`Bmg4iBZvbhs`) [PRÁTICA].
4. **Cubagem.** A armazenagem é cobrada por m³, e o padrão (até 45×35×20 cm ou 9 kg) tem limite de capacidade diferente do extragrande.
5. **Restrições.** Perigosos (hazmat), extragrandes e itens de alto valor têm limite menor e ficam fora da entrega em horas. Para inflamáveis, a Amazon pede documentação (`zdDPzE7jftg`, `gZ4fDdLtwBo`).
6. **Sazonalidade.** Picos de 2026: Mega Ofertas Prime de 05 a 11/10; Black Friday de 03/11 até a Cyber Monday (`VvcswcsjuUw`). O estoque do evento vai antes, e o resto se cobre com DBA.

### 3.3 Divergências entre fontes

| Tema | Fonte A | Fonte B | Leitura |
|---|---|---|---|
| Cobertura ideal | Amazon: 5 semanas | Jungle Scout: 60 dias (EUA) | Faixa de 35 a 60 dias |
| Antecedência para picos | Amazon: 2 semanas ou mais | Smollan: ideal 30 dias | Faixa de 15 a 30 dias |
| Limite físico da caixa | Webinars de 2026: 22 kg e 100 cm | Página de treinamento sem data: 30 kg e 105×105×72 cm | Prevalece o webinar de 2026, porque a página parece anterior (cita só Cajamar e GRU8) |

---

## 4. Números de referência

| Métrica ou limite | Valor | Tipo | Fonte | Data | Pode estar superada? |
|---|---|---|---|---|---|
| Armazenagem mensal FBA (até 10.000 cm³) | R$ 75,00/m³/mês (≈ R$ 2,50/m³/dia) | OFICIAL | /precos; `crnP1JO2B1o` | 01/08/2025; webinar 04/09/2026 | Página sim (2025); confirmada por webinar de 2026 |
| Armazenagem mensal FBA (10.000 cm³ ou mais) | R$ 37,50/m³/mês | OFICIAL | /precos | 01/08/2025 | Sim |
| Armazenagem de longo prazo | R$ 525/m³ (acima de 365 dias, somada à mensal) | OFICIAL | /precos; `crnP1JO2B1o` | 2025 e 2026 | Confirmada em 2026 |
| Prazo de remoção | 14 dias úteis; 30 ou mais em pico | OFICIAL | /gerenciamento-de-inventario | sem data | Sim |
| Cobertura recomendada | 5 semanas | OFICIAL via webinar | `k0v5Yw5h5NQ` | 2026-09-11 | Não |
| Cobertura para entrega em horas | cerca de 4 semanas | OFICIAL via webinar | `gZ4fDdLtwBo` | 2026-10-07 | Não |
| Idade do estoque: promover | 60 a 90 dias | OFICIAL via webinar | `k0v5Yw5h5NQ` | 2026 | Não |
| Idade do estoque: remover | acima de 90 dias | OFICIAL via webinar | `k0v5Yw5h5NQ` | 2026 | Não |
| IDI saudável | 700 ou mais | OFICIAL via webinar | `k0v5Yw5h5NQ` | 2026 | Não. Nos EUA, o IPI vai de 0 a 1.000 com limite de 400 (Jungle Scout, 2023) |
| IDI: quando passa a existir | após 3 meses no FBA | OFICIAL | /gerenciamento-de-inventario | sem data | Sim |
| Recebimento no CD | 3 a 7 dias; 2 a 3 semanas em sazonalidade | OFICIAL via webinar | `zdDPzE7jftg` | 2026-08-20 | Não |
| Antecedência para pico | 2 semanas ou mais (Amazon); 15 a 30 dias (agência) | OFICIAL via webinar / PRÁTICA | `q0-Y5gG6Q2w`; `VH7Q5FddoRY` | 2026 | Não |
| Cobertura (praticante) | 30 a 45 dias de demanda | PRÁTICA | `78sSkRh2crI` | 2026-08-18 | — |
| Prazo de entrega FBA | 1 dia útil em mais de 200 cidades; 2 dias úteis em mais de 1.300 | OFICIAL via webinar | `zdDPzE7jftg`, `VvcswcsjuUw` | 2026 | Não |
| Entrega em horas | até 4h30, SP e RJ | OFICIAL via webinar | `gZ4fDdLtwBo` | 2026-10-07 | Não |
| DBA: tarifa até R$ 78,99 | R$ 4,50 / R$ 6,50 / R$ 6,75 | OFICIAL | /precos, /cresca/dba | 2026 | Não |
| Clientes Prime | "80% dos clientes" | OFICIAL, sem método | `zdDPzE7jftg`, `q0-Y5gG6Q2w` | 2026 | — |
| Efeito do FBA nas vendas | "4x em média" (dado interno de 2025) | OFICIAL, sem método | /cresca/fba | 2025 | — |
| EUA: taxa de estoque baixo | cobrada quando a cobertura histórica fica abaixo de 28 dias nas janelas de 30 e 90 dias | DADO (citando a Amazon) | Jungle Scout, artigo de tarifas FBA | 2024-09-30 | Sim |
| EUA: sobretaxa de estoque envelhecido | a partir de 181 dias | OFICIAL (EUA) | sell.amazon.com/fulfillment-by-amazon | 2026 | Não |
| EUA: amostra do State of the Amazon Seller | cerca de 1.500 vendedores, 10 a 27/01/2025, mais de 20 países; 38% citam custo de frete como desafio | DADO | junglescout.com, relatório 2025 | 2025 | Sim |

---

## 5. Alimentos, perecíveis e marca própria/indústria

**O que está documentado (Amazon Brasil):**
- **Validade visível.** A etiqueta FNSKU não pode cobrir a data de validade. Já houve envio inteiro com a validade coberta que precisou de remoção (`zdDPzE7jftg`, `VvcswcsjuUw`) [OFICIAL via webinar]. Confiança B.
- **Conferência no recebimento.** O recebimento abre a caixa master e confere integridade, embalagem e validade. No GRU9, as ruas são separadas por categoria segundo critério da vigilância sanitária, e os produtos de categorias diferentes não se misturam (`-7TGtIYZX0U`) [OFICIAL via webinar]. Confiança B.
- **Vencido é perda.** Item que vence no CD é não apto e não reembolsável. Precisa ser removido em 30 dias ou é descartado (`k0v5Yw5h5NQ`; /cresca/fba). Confiança A.
- **Preparo de embalagem.** A criação do envio pede a categoria de preparação ("alimento", "líquido", "frágil" etc.). Pote com tampa de rosca sem lacre leva fita. Líquidos vão em saco plástico no CD (`crnP1JO2B1o`, `k0v5Yw5h5NQ`, `0rnXQha3Eew` com trecho do vídeo do Iberê) [OFICIAL via webinar / PRÁTICA]. Confiança B.
- **Kits.** Caixas de café com sabores variados, por exemplo, precisam chegar montadas em saco, com uma etiqueta só e um NCM. A orientação é usar o NCM do item de maior valor e confirmar com a contabilidade (`VvcswcsjuUw`). Confiança B.
- **Frete de mercearia na entrega em horas.** Frete grátis só a partir de R$ 79, contra R$ 19 nas demais categorias (`gZ4fDdLtwBo`). Confiança B.
- **Recorrência.** "Programe e Poupe" (assinatura) aparece em café FBA (Italle) e em limpeza 1P (Lysoform). Para recompra, a assinatura combina com FBA porque exige estoque contínuo ([OBS] `lideres.tsv`, 2026-10-14). A ligação entre Programe e Poupe e FBA não foi conferida em página oficial brasileira. Confiança C.

**O que não está documentado em fonte aberta (ver Lacunas):**
- Prazo mínimo de validade no recebimento e regra de descarte antes do vencimento no FBA Brasil.
- Exigência de lote.
- Produto sensível a calor.
- Exigências da Anvisa e do Inmetro para venda e armazenagem em marketplace.
- Aprovação de categoria para Alimentos e Bebidas.

As regras da Amazon EUA para validade existem na ajuda do Seller Central, mas a página não abriu sem login. Por isso a nota não as reproduz.

**Leitura para indústria e marca própria [MARCA]:**
- **Estoque parado custa duas vezes.** Para quem tem validade, a curva de idade (60 a 90 dias: promover; acima de 90: remover) encontra a data de vencimento. O estoque parado pesa no IDI e corre risco de virar não apto sem reembolso. A cobertura de 5 semanas recomendada pela Amazon é compatível com giro de alimento seco. O teto de 60 dias da Jungle Scout é mais arriscado para itens de validade curta. É uma inferência do analista, sem fonte direta.
- **1P x 3P nos líderes de café.** Os líderes observados vendem 1P: a Amazon compra da marca e entrega no dia seguinte. A promessa de entrega dessas marcas não depende do FBA do 3P. A Italle chega à mesma promessa ("amanhã") como 3P com FBA ([OBS] 2026-10-14).

---

## 6. Erros comuns e mitos

| Afirmação (fonte fraca) | O que a fonte forte diz | Fontes |
|---|---|---|
| "FBA grátis para itens a partir de R$ 100" (mentor, jun/2026) | A campanha vigente é de R$ 6 por unidade acima de R$ 79, só para conta existente que cumpre 3,5% de Ads; zero só nos 30 dias de conta nova | `n-YyqeRmWds` x /termos/experimente-fba |
| "Promoção vai até janeiro de 2026" (mentora) | Os termos dizem 31/01/2027 | `l9MMfiAAWqo` x termos |
| "FBA vende 8x; reabastecendo, 16x" | Número sem base, em conteúdo que vende consultoria (sinais 1, 2 e 5: rebaixado a N7). A própria Amazon diz 4x, com dado interno | `78sSkRh2crI` x /cresca/fba |
| "Armazenagem não entra no preço porque não é para acontecer" | Armazenagem mensal e de longo prazo existem; a isenção depende da meta de Ads e termina em 31/01/2027 | `Bmg4iBZvbhs` x /precos e termos |
| "Posso escolher em que CD fica meu estoque" | A distribuição é interna e não controlável. Praticante diz que dá para "pedir à Amazon dividir para a filial do Nordeste"; não confirmado | `k0v5Yw5h5NQ` x `78sSkRh2crI` |
| "Colocar o produto em Ads ajuda a recuperar a Buy Box ou a vender sem estoque" | Sem Buy Box ou sem estoque, o anúncio fica congelado e não gasta | `q0-Y5gG6Q2w` |
| "Converter a oferta para FBA é mais simples" | Converter tira a oferta de venda até o estoque chegar ao CD, e o integrador pode reverter oferta híbrida; a Amazon recomenda duplicar | `crnP1JO2B1o`, `zdDPzE7jftg` |
| "Ponto de coleta: horário das 13h às 18h que aparece no Seller Central" | Na modalidade postagem, o limite real é 14h (ou o horário regional); o sistema ainda exibe o horário antigo | `PeBETM-rBxk` |
| "Dropshipping funciona na Amazon" | O mentor diz que "não presta" (opinião). O tempo de preparo fixo em 0 dia e a meta de envio tardio abaixo de 4% tornam a operação sem estoque difícil (inferência) | `0rnXQha3Eew`; `lBnzH7KSh4E` |
| "Mandar 5 unidades já garante entrega rápida no Brasil todo" | Lote raso não é redistribuído entre CDs | `VvcswcsjuUw` |

Também não está documentado o mito "a ruptura derruba o ranking por X dias". Nenhuma fonte, oficial ou de ferramenta, mede o tempo de recuperação; a Jungle Scout trata o tema só como opinião de especialista.

---

## 7. Revenda/importação x indústria/marca própria

| Tema | [REVENDA] (revenda, importação, genérico) | [MARCA] (indústria, marca própria) |
|---|---|---|
| Disputa no ASIN | Vários vendedores no mesmo ASIN (53 ofertas num genérico observado). O FBA pesa na Buy Box junto com preço e reputação | ASIN próprio, em geral sem disputa. O FBA pesa na promessa, no selo Prime e na elegibilidade a eventos |
| Oferta dupla FBA + DBA | Usada para não perder a Buy Box em ruptura (`02Bn3HyAYqk`) | Usada como plano B de pico (`VH7Q5FddoRY`) |
| Teste de envio | 3 unidades por SKU e escala do que gira (social, Europa); "ser o primeiro FBA do ASIN" | Envio de curva A com profundidade, para entrar na redistribuição e na entrega em horas |
| Origem e fiscal | Importado: origem da mercadoria diferente de 0 na oferta. A emissão de NF pelo Faturador vale para os dois. Prep center para quem está fora dos estados com CD (`n-YyqeRmWds`) | Fabricante declara a atividade "fabricante" no Faturador. O Programa de Filiais atende indústria fora dos estados com CD |
| Validade e lote | Menos frequente | Central em alimentos, cosméticos e suplementos: validade visível, risco de não apto e de descarte |
| Recorrência | Baixa | Programe e Poupe e estoque contínuo ([OBS]) |
| Vendedor CPF | Pode usar DBA (com DC-e emitida pela Amazon desde 15/09/2026); não entra no FBA | Indústria sempre tem CNPJ |

As regras de tarifa, capacidade, IDI e inbound valem igualmente para os dois.

---

## 8. Tabela de afirmações

Confiança: alta (A), média (B) e baixa (C).

| id | Afirmação | Tipo | Fonte | Data | Confiança |
|---|---|---|---|---|---|
| A1 | Armazenagem FBA: R$ 75/m³/mês até 10.000 cm³; R$ 37,50/m³ acima | OFICIAL | venda.amazon.com.br/precos; /cresca/fba | 01/08/2025 (pode estar superada; vigente na página em 14/10/2026) | alta |
| A2 | Armazenagem de longo prazo: R$ 525/m³ acima de 365 dias, somada à mensal | OFICIAL | /precos; `crnP1JO2B1o` | 2025 e 2026 | alta |
| A3 | Inventário não apto deve ser removido em 30 dias, ou é descartado sem reembolso | OFICIAL | /cresca/fba; `k0v5Yw5h5NQ` | 2026 | alta |
| A4 | Campanha Experimente FBA 3.0: R$ 6 por unidade a partir de R$ 79, coleta e armazenagem zero para conta existente; vigência de 01/07/2026 a 31/01/2027 | OFICIAL | /termos/experimente-fba | 2026 | alta |
| A5 | Condição: 3,5% da receita em Ads, ou +1 p.p. sobre abril/2026 para contas anteriores a 01/04/2026; validação no dia 20 | OFICIAL | /termos/experimente-fba | 2026 | alta |
| A6 | Conta nova: 30 dias de isenção total, contados da primeira oferta FBA ativa | OFICIAL | termos; `crnP1JO2B1o` | 2026 | alta |
| A7 | Entrada no FBA: CNPJ na Sefaz, Simples ou Regime Normal (MEI aceito), A1, Faturador, IE em 12 estados ou filial; sem mínimo | OFICIAL | /cresca/fba; `crnP1JO2B1o` | 2026 | alta |
| A8 | Cobertura recomendada pela Amazon: 5 semanas | OFICIAL via webinar | `k0v5Yw5h5NQ` | 2026-09-11 | média |
| A9 | Idade do estoque: promover entre 60 e 90 dias; remover acima de 90 | OFICIAL via webinar | `k0v5Yw5h5NQ` | 2026-09-11 | média |
| A10 | O limite de capacidade (m³, por tipo) depende do IDI; saudável a partir de 700; pode haver limite por produto em excesso | OFICIAL via webinar | `k0v5Yw5h5NQ` | 2026-09-11 | média |
| A11 | Até 200 caixas por envio; caixa de até 22 kg e lado de até 100 cm | OFICIAL via webinar | `k0v5Yw5h5NQ`, `VvcswcsjuUw` | 2026 | média (página antiga diz 30 kg) |
| A12 | Recebimento no CD: 3 a 7 dias; 2 a 3 semanas em sazonalidade | OFICIAL via webinar | `zdDPzE7jftg` | 2026-08-20 | média |
| A13 | Enviar para picos com 2 semanas ou mais (Amazon) ou 15 a 30 dias (agência) de antecedência | OFICIAL via webinar + PRÁTICA | `q0-Y5gG6Q2w`; `VH7Q5FddoRY` | 2026 | alta |
| A14 | Entrega em horas (SP e RJ) é automática, exige cerca de 4 semanas de cobertura e Buy Box, sem custo de transferência | OFICIAL via webinar | `gZ4fDdLtwBo` | 2026-10-07 | média |
| A15 | Tempo de preparo padrão da conta (DBA/MFN) = 0 dia, fixo; por ASIN, de 1 a 30 dias | OFICIAL via webinar + OFICIAL | `lBnzH7KSh4E`; /cresca/dba | 2026 | alta |
| A16 | DBA: envio tardio abaixo de 4%; cancelamento abaixo de 2,5% | OFICIAL | /cresca/dba; `PeBETM-rBxk` | 2026 | alta |
| A17 | DBA Postagem com até 9 pacotes/dia; Coleta com 10 ou mais; 30 kg | OFICIAL | /cresca/dba; `PeBETM-rBxk` | 2026 | alta |
| A18 | Frete grátis: FBA a partir de R$ 19 (abaixo disso, só Prime); DBA a partir de R$ 19 na mesma região e de R$ 79 entre regiões | OFICIAL | /termos/frete19 | 15/08/2025 (pode estar superada) | média (há conflito com a regra do não-Prime em /cresca/fba) |
| A19 | Sem estoque ou sem Buy Box, o anúncio patrocinado não é veiculado e não gasta | OFICIAL via webinar | `q0-Y5gG6Q2w` | 2026-09-15 | média |
| A20 | A Amazon redistribui o estoque FBA entre CDs sem custo; exige profundidade de estoque | OFICIAL via webinar | `VvcswcsjuUw`; `k0v5Yw5h5NQ` | 2026 | média |
| A21 | O FBA aumenta as vendas "4x em média" | OFICIAL, sem método | /cresca/fba; `crnP1JO2B1o` | dado de 2025 | baixa (tamanho do efeito) |
| A22 | 80% dos clientes são Prime; membros Prime gastam 2,5x mais | OFICIAL, sem método | `zdDPzE7jftg` | 2026-08-20 | baixa |
| A23 | Oferta dupla FBA + DBA no mesmo ASIN segura a venda quando o FBA zera | PRÁTICA (com tela) | `02Bn3HyAYqk`; `VH7Q5FddoRY` | 2026 | média |
| A24 | Faixa de cobertura dos praticantes: 30 a 60 dias | PRÁTICA + DADO | `78sSkRh2crI`; Jungle Scout (2023) | 2023 a 2026 | média |
| A25 | Ruptura logo após o pico desperdiça o ranqueamento conquistado | OFICIAL via webinar (opinião) | `VvcswcsjuUw` | 2026-09-24 | baixa |
| A26 | A etiqueta FNSKU não pode cobrir a validade; o recebimento confere a validade | OFICIAL via webinar | `zdDPzE7jftg`; `-7TGtIYZX0U` | 2026 | média |
| A27 | Item vencido no CD não é reembolsável | OFICIAL via webinar | `k0v5Yw5h5NQ` | 2026-09-11 | média |
| A28 | Reembolso automático por perda ou dano no CD ou na transportadora da Amazon; perda no inbound só mediante investigação | OFICIAL via webinar + OFICIAL | `k0v5Yw5h5NQ`; /cresca/fba | 2026 | alta |
| A29 | SAFE-T: DBA em 45 dias, FBA Onsite em 52 dias, item devolvido em 7 dias; reembolsa só o preço do item | OFICIAL via webinar | `cya4LLoRX7A` | 2026-07-28 | média |
| A30 | DC-e de vendedor CPF no DBA passou a ser emitida pela Amazon a partir de 15/09/2026 | OFICIAL via webinar | `OBY9LjwvhnA` | 2026-09-11 | média |
| A31 | No-show de coleta reduz a capacidade em 20% (3 a 4 ocorrências) ou 40% (5 ou mais) | OFICIAL | /central-de-treinamento-fba/criacao-de-um-envio | sem data (pode estar superada) | baixa |
| A32 | EUA: taxa de estoque baixo quando a cobertura histórica fica abaixo de 28 dias (janelas de 30 e 90 dias); sobretaxa de envelhecido a partir de 181 dias | DADO / OFICIAL (EUA) | Jungle Scout (2024-09-30); sell.amazon.com | 2024 a 2026 | média (EUA; não vale para o Brasil sem confirmação) |
| A33 | Os líderes de café observados entregam "amanhã", majoritariamente em 1P; a Italle em 3P com FBA | OBS | `lideres.tsv` | 2026-10-14 | média |

---

## 9. Lacunas

1. **Regras de validade, lote e temperatura no FBA Brasil.** A ajuda do Seller Central (G201030350, G201003420) exige login. Faltam o prazo mínimo de validade no recebimento, o descarte antes do vencimento, o formato da data e a política para itens sensíveis a calor. Também não se confirmou se a Amazon Brasil exige aprovação de categoria para Alimentos e Bebidas no 3P. Sem evidência.
2. **Anvisa e Inmetro no fulfillment.** Nenhuma fonte lida trata de exigência regulatória específica para alimentos em CD de marketplace, como dispensa de registro, rotulagem ou responsabilidade do armazenador. Sem evidência.
3. **Tempo de recuperação do ranking após ruptura.** Nenhuma fonte mede isso. A Jungle Scout traz só opinião, e as fontes oficiais falam qualitativamente. Sem evidência.
4. **Efeito causal do FBA e do prazo sobre conversão e exposição.** Existe apenas o "4x" interno da Amazon, sem método, sem grupo de controle e sujeito a viés de sobrevivente (quem entra no FBA já vende melhor). Não há estudo independente para o Brasil.
5. **Fórmula e faixas do IDI no Brasil.** O "700 ou mais" vem só do webinar. Nos EUA, o IPI tem limite de 400 numa escala de 0 a 1.000 (Jungle Scout, 2023). Não se sabe se a escala brasileira é a mesma.
6. **Tarifa logística abaixo de R$ 79 dentro da campanha.** Os webinars dizem R$ 5,65, R$ 5,85 e R$ 6,05 (ou 6,50). A página de termos abriu com o Anexo 2 incompleto. Precisa de conferência visual em /termos/experimente-fba e /precos.
7. **Frete grátis para não-Prime no FBA.** Três números se contradizem: R$ 19 a R$ 79 com entrega em 3 dias ou mais (/termos/frete19), R$ 129 (/cresca/fba) e R$ 149 (/cresca/fba-onsite).
8. **Limites físicos da caixa master.** Os webinars de 2026 dizem 22 kg e lado de 100 cm. A página de treinamento, sem data, diz 30 kg e 105×105×72 cm.
9. **Benchmarks brasileiros de saúde de estoque.** Não foram encontrados dados sobre ruptura média dos top SKUs, sell-through por categoria ou idade média do estoque no Brasil. Nenhuma ferramenta, nem Nubimetrics para Amazon BR, foi aberta. A cota de busca acabou.
10. **Multa por divergência no recebimento.** Nenhuma fonte cita multa monetária. Há métrica de erros de envio (peso, dimensão, etiqueta), que gera aviso e pode limitar a capacidade (`VvcswcsjuUw`, `k0v5Yw5h5NQ`), mas os limites não são públicos.
11. **Previsão de demanda e estoque de segurança.** Nenhuma fonte publica fórmula de ponto de pedido para Amazon Brasil. As ferramentas (Jungle Scout Inventory Manager) não divulgam o método.

---

## 10. Verificação (2026-10-14)

Fontes oficiais lidas em 2026-10-14 (páginas sem data de publicação; todas tipo [OFICIAL]). Seller Central exige login e não foi aberto.

| id | veredito | fonte oficial (URL) | observação |
|---|---|---|---|
| A1 | CONFIRMADA | https://venda.amazon.com.br/precos | R$ 75/m³ abaixo de 10.000 cm³ e R$ 37,50/m³ a partir disso, sobre o volume médio diário, cobrado no mês seguinte. A página só data "01/08/2025" para a tarifa de logística, e a de armazenagem não tem data: pode estar superada. |
| A2 | CONFIRMADA | https://venda.amazon.com.br/precos | R$ 525/m³ para inventário com mais de 365 dias, adicional à mensal. Sem data na página. |
| A3 | CONFIRMADA | https://venda.amazon.com.br/cresca/fba | Não apto pode ficar até 30 dias após a classificação; sem pedido de remoção é descartado sem reembolso. Há aviso semanal e remoção a qualquer momento, com envio ao endereço do CNPJ. A remoção é cobrada por unidade (R$ 0,99 a R$ 3,60 por faixa de peso, em /precos). |
| A4 | CONFIRMADA | https://venda.amazon.com.br/termos/experimente-fba | Campanha 3.0 de 01/07/2026 a 31/01/2027. Conta existente: tarifa única R$ 6 em preço de venda a partir de R$ 79, com coleta e armazenagem zeradas em todas as faixas de preço. Conta nova: isenção de 100% de logística, coleta e armazenagem por 30 dias a partir da primeira oferta ativa (aplicável até 10 dias após a chegada do 1º envio). |
| A5 | CONFIRMADA | https://venda.amazon.com.br/termos/experimente-fba | 3,5% da receita total dos 30 dias anteriores (não só FBA), em valor consumido. Contas anteriores a 01/04/2026: 3,5% ou 1 p.p. acima do percentual de 01 a 30/04/2026. Validação todo dia 20 (primeira 20/07/2026, última 20/12/2026). "Efeito no mês seguinte" não foi lido literalmente nesta página. |
| A6 | CONFIRMADA (parcial) | https://venda.amazon.com.br/termos/experimente-fba | Anexos 1 e 2 trazem R$ 5,65 (abaixo de R$ 30), R$ 5,85 (R$ 30 a 49,99) e R$ 6,05 (R$ 50 a 78,99), só para a faixa de peso 1 a 1,5 kg. O R$ 6,50 não aparece. As demais faixas de peso vieram incompletas. Não dá para tratar como tarifa geral. |
| A7 | SEM FONTE OFICIAL | https://venda.amazon.com.br/cresca/fba (não cita) | Cobertura de 5 semanas, limiares de 60/90 dias e 4 semanas para entrega em horas não constam nas páginas públicas lidas. Só webinars. |
| A8 | SEM FONTE OFICIAL | https://venda.amazon.com.br/cresca/fba (não cita) | IDI, 700 e capacidade em m³ por tipo não constam. A página diz apenas que a capacidade inicial é ilimitada para envio e armazenagem. Seguem como informação de webinar. |
| A9 | CONTESTADA | https://venda.amazon.com.br/central-de-treinamento-fba/criacao-de-um-envio ; https://venda.amazon.com.br/cresca/fba | O 22 kg e o lado de 100 cm valem para o produto/embalagem (soma das dimensões até 200 cm). A caixa master tem até 30 kg e 105×105×72 cm. Assim, 22 kg e 100 cm não são o limite da caixa. O limite de 200 caixas não foi encontrado (a página diz só que a coleta é cobrada por caixa). Páginas sem data. |
| A10 | SEM FONTE OFICIAL (parcial) | https://venda.amazon.com.br/cresca/dba | Confirmado: tempo de preparo padrão de 0 dia (preparo no mesmo dia útil antes do corte) e prazo maior configurável por SKU. A faixa de 1 a 30 dias não consta. Logística própria (não DBA) não foi coberta. |
| A11 | SEM FONTE OFICIAL (parcial) | https://venda.amazon.com.br/cresca/dba | Confirmados: envio tardio abaixo de 4%, postagem até 9 pacotes/dia e coleta a partir de 10, produto abaixo de 30 kg. O cancelamento antes do envio abaixo de 2,5% não consta nesta página. |
| A12 | CONTESTADA | https://venda.amazon.com.br/termos/frete19 ; https://venda.amazon.com.br/cresca/fba | Os termos (início 15/08/2025, sem fim; pode estar superada): FBA/FBA Onsite abaixo de R$ 19 só Prime; de R$ 19 a R$ 79 frete grátis com entrega de 3 dias ou mais; acima de R$ 79 com entrega em até 1 dia. DBA: abaixo de R$ 19 frete pago; R$ 19 a R$ 79 só na mesma região; acima de R$ 79 só entre regiões diferentes. Já /cresca/fba diz R$ 129 para não-Prime e não cita R$ 149. A página de DBA confirma R$ 19 mas trata R$ 79 como faixa de tarifa, não como limite de frete. A contradição segue sem resolução. |


## 11. Verificação pelo navegador (2026-10-15)

Método: Chrome do usuário, lendo advertising.amazon.com/pt-br, venda.amazon.com.br, amazon.com.br/gp/help e a Central de Ajuda do Seller Central (sessão já aberta, só leitura). Sem captcha. Ids como em pendentes-amazon.tsv.

| id | veredito | fonte oficial | observação |
|---|---|---|---|
| A6 | CONFIRMADA | https://venda.amazon.com.br/termos/experimente-fba | Isenção de logística, coleta e armazenagem. Conta nova = sem inventário ou envio FBA entre 01/01/2025 e 31/07/2026. A isenção pode ser aplicada em até 10 dias após a chegada do 1º envio. |
| A7 | PARCIAL | https://venda.amazon.com.br/cresca/fba | Confirmados: CNPJ ativo na Sefaz, Simples ou Regime Normal, IE em 12 estados (SP, MG, PR, RJ, SC, RS, CE, DF, PE, BA, GO, ES) ou Programa de Filiais, Faturador como passo 1. MEI aceito, certificado A1 e 'sem mínimo' não aparecem. |
| A8 | CONTESTADA | https://sellercentral.amazon.com.br/help/hub/reference/G201104750 | A ajuda oficial recomenda de 2 semanas (ou o prazo de reposição) a 13 semanas, não 5. As 5 semanas aparecem só no webinar. Lido na Central de Ajuda do Seller Central com a sessão já aberta, só leitura. |
| A10 | PARCIAL | https://sellercentral.amazon.com.br/help/hub/reference/GAFNWEYTJUV2GBFC ; https://sellercentral.amazon.com.br/help/hub/reference/G202174810 | Confirmado: limite mensal por tipo de armazenagem, em m³, pelo IPI e pelas vendas; contas com menos de 39 semanas no FBA não têm limite. Pontuação 700 e limite por produto em excesso não aparecem. Lido na Central de Ajuda do Seller Central com a sessão já aberta, só leitura. |
| A11 | SEM FONTE OFICIAL | https://sellercentral.amazon.com.br/help/hub/reference/GX4YXVJBW4C3MHU7 ; https://sellercentral.amazon.com.br/help/hub/reference/G200178470 | 200 caixas por envio, 22 kg e 100 cm não encontrados. Indício de divergência: a tabela de tarifas de coleta tem faixas por caixa até 30 kg. |
