# Shopee Brasil: reputação, atendimento e pós-venda (notas do analista)

Frente: reputacao-atendimento · Plataforma: Shopee (Brasil) · Data da nota: 2026-10-14

Antes de ler, saiba como esta nota foi feita:

- **Escopo.** A nota cobre só a Shopee. As perguntas sobre ML (Experiência de compra por anúncio, MercadoLíder) e Amazon (Featured Offer, motivos de devolução no POE) aparecem apenas para mostrar o equivalente na Shopee ou para registrar que não há evidência. Elas ficam para as notas dessas plataformas.
- **Limite da camada oficial.** As páginas `seller.shopee.com.br/edu/...` e `help.shopee.com.br/portal/...` só carregam com JavaScript. WebFetch e curl recebem apenas o título ("Seller Education Hub" / "Help Center"). Além disso, o orçamento de WebSearch da rodada já tinha acabado quando esta frente começou. Por isso a camada oficial veio de três lugares:
  - (a) vídeos do **canal oficial Shopee Brasil** no YouTube ([OFICIAL], N1);
  - (b) telas da Central do Vendedor e leituras de artigos oficiais feitas por praticantes ([OFICIAL via terceiro]);
  - (c) links oficiais citados por blogs, que não abriram. Veja a seção 9.
- **Fontes lidas.** 12 transcrições obrigatórias e mais 14 da pasta (5 delas do canal oficial). Do blog UpSeller saíram 5 artigos (3 usados) e do blog Bling, 2. Também entrou a observação de líderes (`observacao/lideres.md`).
- **Convenções.**
  - [REVENDA] = revenda, dropshipping, importação. [MARCA] = indústria, marca própria. [AMBOS] = vale para os dois.
  - Regra de plataforma anterior a 2026-04-14, ou sem data, leva **(pode estar superada)**.
  - Confiança: A/alta = duas fontes independentes, uma N1–N3. B/média = uma N1–N4, ou duas N5–N6 concordantes. C/baixa = fonte única N5–N8.

---

## 1. Resumo executivo

1. **Saúde da conta.** A Shopee mede a saúde da conta em três pilares, cada um com métricas próprias, todos calculados **semanalmente**: (1) pedidos concluídos (não cumprimento, envio atrasado, tempo de preparação, envios aos sábados), (2) produto/anúncios (violações, pré-venda) e (3) atendimento. A tela "Desempenho da conta" diz, para cada métrica, se ela afeta pontos de penalidade, Vendedor Indicado ou limite de anúncios. [OFICIAL via terceiro, tela] LLDUrAuF3qQ (2026-05-14) · B
2. **Pontos.** A penalidade funciona por **pontos que se acumulam no trimestre civil** (jan–mar, abr–jun, jul–set, out–dez) e zeram na virada. Com 1 ou 2 pontos há só aviso. A punição começa em **3 pontos**. Pagar a punição não apaga os pontos. [OFICIAL via terceiro] ThPsYQpMxJE (2026-08-05), LLDUrAuF3qQ (2026-05-14), UpSeller blog-article-946 (2026-07-07) · A
3. **Faixas (tela oficial).** 3–5 pts: 14 dias, −5% de visibilidade, R$100, mantém frete grátis. 6–8: 14 dias, −10%, sem frete grátis, R$250. 9–11: 21 dias, −20%, R$500. 12–14: 28 dias, −30%, R$1.000. 15+: **conta congelada 28 dias**, R$1.500. Todas suspendem Indicado e campanhas. [OFICIAL via terceiro] ThPsYQpMxJE, LLDUrAuF3qQ · B. A UpSeller diverge nas faixas 2 e 3 (R$300/R$600).
4. **Gatilhos de envio.** Não envio ≥8% **e** ≥2 pedidos = 1 ponto (≥90 pedidos = 2 pontos). Envio atrasado ≥5% **e** ≥2 pedidos = 1 ponto (≥90 = 2). O critério é combinado justamente para não punir loja pequena por um único pedido. [OFICIAL via terceiro] ThPsYQpMxJE · B
5. **Atendimento.** Cada uma destas condutas dá **2 pontos de uma vez**: resposta abusiva no chat, levar o comprador para fora da plataforma, pedir ao comprador que cancele o pedido e responder de forma abusiva a uma avaliação. [OFICIAL via terceiro] ThPsYQpMxJE · B
6. **Cancelamento.** Para a Taxa de Não Cumprimento (TNC), conta o cancelamento feito pelo vendedor e o cancelamento automático por falta de envio. **O cancelamento pedido pelo comprador não conta.** Devolução ou reembolso por erro do vendedor (variação ou quantidade errada) também entra na TNC. [OFICIAL via terceiro, tela] LLDUrAuF3qQ · C/B
7. **Vendedor Indicado.** Revisto toda semana, com limite de entrada e de permanência: nota >4,5 / >4,2; chat ≥60% / >50%; TNC <2% / <3%; pontos ≤1 / <3; preparo ≤1 / <1,3 dia útil; sábados ≥20%; CNPJ; loja >90 dias. [OFICIAL via terceiro, card] 8cRhids_rNs (2026-03-18) · C **(pode estar superada)**
8. **Taxa de resposta do chat.** Cobre os chats que exigem resposta nos **últimos 30 dias**. A mensagem precisa ser respondida em até **12 h**, e **fins de semana e feriados contam**. [OFICIAL via terceiro, leitura do artigo] Arwxa4I9DgE (2026-06-05) · B
9. **Gestão de chat.** Com subcontas, a ferramenta oficial monta grupos (pré-venda, pós-venda, devolução) e encaminha pelo **ponto de clique**, não pelo assunto. Quem volta em até 12 h cai no mesmo atendente. [OFICIAL] tMFZK5GEMlo (2026-08-18) · B
10. **Experiência de compra.** Anúncio com muitas reclamações ou devoluções perde visibilidade. O caminho de diagnóstico mostrado é: Informações gerenciais > Produto > Diagnóstico do produto > "Alta taxa de devolução". Segundo o praticante, a métrica conta todo tipo de reclamação, inclusive arrependimento. [PRÁTICA, tela parcial] p8OZWm62pQw (2026-09-11) · C
11. **Embalagem.** O guia oficial de embalagem (out/2026) recomenda **fotografar ou filmar a embalagem** para usar em contestação. Também avisa que embalagem inadequada recorrente pode levar a menos visibilidade, remoção de produtos, códigos de violação e penalidade na conta. [OFICIAL] 9CxujZDsRCw (2026-10-01) · B
12. **Devolução Fácil.** É uma tarifa de **R$0,49 por pedido**, ativada automaticamente em maio/2026. O vendedor pode sair em Pedidos > Configurações de envio. [PRÁTICA, tela] yAmvIlW11GY (2026-05-09) · C. Precisa de confirmação oficial.
13. **Avaliações dentro da regra.** O recurso oficial é Transmissão por chat > Atualizações proativas > "Lembrar compradores de avaliar", com benefício em moedas. Na prática, o primeiro volume de avaliações vem de preço agressivo (margem de 20% reduzida para 5–10%) somado a Ads ou vídeo. [PRÁTICA, tela] xrE8fUZ94Y0 (2026-10-13) · C
14. **Full Shopee.** Para entrar é preciso CNPJ, **nota da loja >4,5** e **no mínimo 5 pedidos/dia**. Ou seja, a reputação é condição de acesso à logística da plataforma. [OFICIAL] TUs6QYGqGrw (2026-08-04) · B
15. **Contestação.** Até 14 dias após a notificação; "reenvio obrigatório" em 7 dias; pontos lançados às segundas; isenção da taxa para GMV <R$2.500 no mês anterior. [DADO/blog de ferramenta, sem link oficial] UpSeller blog-article-946 (2026-07-07) · C

---

## 2. Como funciona (mecânica e regras oficiais, com data)

### 2.1 Onde fica e como é calculado

- **Caminho na Central do Vendedor.** Home > "Desempenho da loja" (status excelente/bom/ruim) > "Desempenho da conta". [OFICIAL via terceiro, tela] LLDUrAuF3qQ (2026-05-14)
- **Três pilares** e, para cada métrica, o que ela afeta, conforme aparece na tela:

| Pilar | Métrica | Meta mostrada na tela | O que afeta |
|---|---|---|---|
| Pedidos concluídos | Taxa de Não Cumprimento (cancelamento pelo vendedor ou automático + devolução/reembolso por erro do vendedor) | <8% | Vendedor Indicado + pontos |
| Pedidos concluídos | Taxa de envio atrasado | <5% (o apresentador cita 8% e 5% em momentos diferentes, e na tela do aluno a meta é <5%) | Pontos |
| Pedidos concluídos | Tempo de preparação | <1 dia | Vendedor Indicado |
| Pedidos concluídos | Envios aos sábados | >20% | Vendedor Indicado |
| Produto | Violações graves de anúncio | — | Pontos |
| Produto | Produtos de pré-venda (encomenda) | <20% | Limite de anúncios |
| Atendimento | Chat, avaliações, condutas | ver 2.3 | Pontos / Indicado |

Fonte: LLDUrAuF3qQ (2026-05-14), tela da conta de um aluno · [OFICIAL via terceiro] · confiança B.

- **Cálculo semanal.** Se a loja não cumpre a métrica numa semana, os pontos, a perda do Indicado ou a limitação de anúncios chegam na semana seguinte. Exemplo mostrado: 21% de envios atrasados numa semana, contra meta <5%, geraram pontos e deixaram a loja com 3 pontos. [OFICIAL via terceiro] LLDUrAuF3qQ
- **Calendário dos pontos.** São atribuídos às segundas-feiras, e a punição entra na segunda seguinte, o que dá cerca de uma semana para contestar. A taxa é descontada do saldo da carteira duas semanas depois do início da punição. Pedidos de sexta e do fim de semana precisam ser postados até terça. [DADO/blog] UpSeller 946 (2026-07-07) · C

### 2.2 Pontos de penalidade: faixas e consequências

| Faixa | Pontos acumulados no trimestre | Duração | Vendedor Indicado | Campanhas da Central de Marketing | Visibilidade | Frete grátis | Taxa |
|---|---|---|---|---|---|---|---|
| — | 0–2 | — | mantém | mantém | — | mantém | — (só aviso) |
| 1 | 3–5 | 14 dias | suspenso | suspensas | −5% | **mantém** | R$100 |
| 2 | 6–8 | 14 dias | suspenso | suspensas | −10% | perde | R$250 (UpSeller: R$300) |
| 3 | 9–11 | 21 dias | suspenso | suspensas | −20% | perde | R$500 (UpSeller: R$600) |
| 4 | 12–14 | 28 dias | suspenso | suspensas | −30% | perde | R$1.000 |
| 5 | ≥15 | 28 dias | — | — | **conta congelada** | — | R$1.500 |

Fontes:

- ThPsYQpMxJE (2026-08-05): leitura de "tutorial oficial da Shopee" em tela. [OFICIAL via terceiro]
- LLDUrAuF3qQ (2026-05-14): aba "Educação" da Central do Vendedor, faixas 1–3 lidas na tela. [OFICIAL via terceiro]
- UpSeller 946 (2026-07-07): diverge nas faixas 2 e 3 e não traz percentuais de visibilidade. [DADO]

Confiança B para a tabela. Nas taxas das faixas 2 e 3 há divergência: duas leituras de tela contra um blog de ferramenta. Vence a tela, mas a regra precisa ser checada.

Regras de duração, do LLDUrAuF3qQ e do ThPsYQpMxJE:

- Os pontos ficam no histórico durante o trimestre e zeram na virada (exemplo dado: zeram em 29/06/2026).
- Cumprir os 14 dias **não apaga os pontos**. Se a loja tem 3 pontos, cumpre a punição e um mês depois recebe mais 1, fica com 4 e cumpre de novo a punição da faixa 1.
- Pela UpSeller, zerar os pontos no trimestre não cancela uma punição em andamento.
- A UpSeller também diz que a "redução de visibilidade" é calculada sobre os últimos 30 dias. Não há outra fonte para isso. · C

### 2.3 Critérios que geram pontos (ThPsYQpMxJE, 2026-08-05, leitura do tutorial oficial)

**Envio**

| Condição | Pontos |
|---|---|
| Não envio ≥8% e ≥2 pedidos não enviados | 1 |
| Não envio ≥8% e ≥90 pedidos não enviados | 2 |
| Envio atrasado ≥5% e ≥2 pedidos atrasados | 1 |
| Envio atrasado ≥5% e ≥90 pedidos atrasados | 2 |
| (UpSeller) Não envio semanal acima de 40% | +1 automático |

**Anúncios**, por nível de severidade:

| Severidade | 2–9 violações | ≥10 violações |
|---|---|---|
| Baixa | 0 | 0 |
| Média | 1 | 2 |
| Alta | 2 | 3 |
| Extrema (produto ou conteúdo proibido por lei ou pela política) | 3 | (não lido) |

- A UpSeller acrescenta "nome de loja inadequado: até 2 pontos".
- O canal oficial confirma que existem níveis de severidade e que anúncio "banido" é diferente de anúncio "removido". [OFICIAL] LPKmJotE9Vc (2026-09-17), sem os números.

**Atendimento ao cliente** (2 pontos por uma ou mais ocorrências):

- resposta desrespeitosa, abusiva ou assédio **no chat**;
- resposta que **direciona para fora da plataforma**;
- **pedir ao comprador que cancele** (o objetivo dessa prática é fugir da TNC);
- resposta abusiva a uma **avaliação** do comprador.

A UpSeller acrescenta "alto índice de avaliações negativas" (sem limite publicado) e fraude (pacote vazio, endereço de devolução incorreto). · C

### 2.4 Vendedor Indicado (selo "Indicado")

Card de critérios mostrado em tela: 8cRhids_rNs (2026-03-18) · [OFICIAL via terceiro] · C · **(pode estar superada)**

| Critério | Para entrar | Para continuar (sai se...) |
|---|---|---|
| CNPJ | obrigatório | — |
| Envios aos sábados | ≥20% | <20% |
| Itens falsificados | 0 | qualquer um |
| Tempo de preparação | ≤1 dia útil | >1,3 |
| Loja ativa | >90 dias | — |
| Pedidos nos últimos 30 dias | >30 | <15 |
| Nota da loja | >4,5 | <4,2 |
| Taxa de resposta do chat | ≥60% | <50% |
| Compradores únicos em 30 dias | >10 | <5 |
| Pontos de penalidade | ≤1 | ≥3 |
| Taxa de não cumprimento | <2% | >3% |

- **Ciclo.** A Shopee revê aos domingos e atualiza na terça. Quem sai precisa cumprir de novo os critérios de entrada, não os de continuidade. [PRÁTICA] 8cRhids_rNs · C
- **Conflito interno a resolver.** O card de março/2026 põe a TNC do Indicado em <2–3%. A tela de maio/2026 (LLDUrAuF3qQ) mostra só "<8%" como meta de TNC ligada ao Indicado e aos pontos. A explicação mais provável é que 8% seja o gatilho de pontos e 2–3% o limite do Indicado, mas não há fonte oficial direta que confirme.
- **Consequência prática** (fala do praticante, sem dados): "de julho de 2025 para cá" quem perdeu o Indicado teve queda acentuada de vendas, que voltaram quando o selo voltou. [PRÁTICA, sem número] 8cRhids_rNs · C
- **O que se vê na busca pública:** o selo "Indicado" aparece em muitos cards de vendedores menores na busca "café em grãos". [OBS] observacao/lideres.md (2026-10-14, sem login, uma página)

### 2.5 Chat e atendimento: regras e ferramentas oficiais

**Taxa de resposta do chat.** O artigo oficial foi lido em tela por um praticante. [OFICIAL via terceiro] Arwxa4I9DgE (2026-06-05) · B

- Conta "chats que exigem resposta" nos últimos 30 dias.
- A resposta tem de sair em até 12 h depois do recebimento.
- Fins de semana e feriados entram no cálculo.
- A taxa cai a cada mensagem que passa de 12 h sem resposta.
- Pelo mesmo artigo, responder no chat ajuda a converter, a fidelizar e a **reduzir devoluções e reembolsos**, porque o comprador fica com expectativas mais precisas.

**Ferramentas da Central do Vendedor** (Atendimento ao cliente > Gerenciamento de bate-papo), mostradas em tela por Arwxa4I9DgE · [OFICIAL via terceiro] · B:

- saudação automática, disparada 1 vez a cada 24 h por comprador;
- atalhos;
- perguntas frequentes (até 5 por categoria; origem geral, produto ou pedido);
- assistente de IA, em 24 h ou horário personalizado, com painel de perguntas respondidas e nota do comprador.

Segundo a praticante, a resposta da IA **não conta** para a taxa de resposta. [PRÁTICA] · C, precisa de checagem.

**Gestão de chat com subcontas.** [OFICIAL] tMFZK5GEMlo (2026-08-18), w_kl2uNobuI (2026-07-21) · B

- Cada membro tem subconta com funções padrão ou personalizadas. A conta principal opera em modo "serviço" ou "monitorar".
- A distribuição é aleatória ou por grupo conforme a **origem do clique**: quem clicou em "reembolso" cai no grupo de reembolso.
- Comprador que volta em até 12 h cai no mesmo agente. Há encaminhamento entre agentes e regra de "longa espera".
- A aba de performance mostra visitantes, tempo médio de resposta e funil.

**Shopee Vídeo e Live.** Promoção deve ser verdadeira. Réplica, QR code, link externo e marca d'água de outro app são proibidos, sob pena de penalidade. [OFICIAL] aUqdtKFx5gM (2026-08-20) · B

### 2.6 Devolução, reembolso e contestação

- **Custo.** Quando o comprador abre a reclamação num motivo atribuído ao vendedor (por exemplo, "recebi o tamanho errado" em vez de "não serviu"), o vendedor pode pagar a devolução, hoje "R$15". [PRÁTICA] LUan-VFNxrY (2026-07-16) · C
- **Prazos.** Fonte: UpSeller 246 (2025-09-19) · [DADO/blog] · C · **(pode estar superada)**
  - Arrependimento: 7 dias após o recebimento (CDC). Garantia legal: 30 dias para não duráveis e 90 para duráveis.
  - Aprovada a solicitação, o comprador tem 7 dias para enviar de volta.
  - Depois de receber o item, o vendedor tem **3 dias** para confirmar o estado. Se não responder, o reembolso é concluído automaticamente.
  - Se recusar, abre-se uma disputa com evidências.
  - Existe reembolso sem devolução para item muito danificado ou de baixo valor.
  - Pacote parado nos Correios precisa ser retirado em 7 dias.
- **Evidência.** A Shopee recomenda registrar o produto antes de embalar, os materiais usados, o produto já protegido e a caixa fechada com a etiqueta visível. As imagens devem ser nítidas. [OFICIAL] 9CxujZDsRCw (2026-10-01) · B
- **Recurso.** Até 14 dias após a notificação; "reenvio obrigatório" em 7 dias, ou o recurso é rejeitado; recursos inválidos repetidos podem custar o acesso à ferramenta. UpSeller 946 · C
- **Como a disputa costuma terminar** (relato de praticante, sem dados). Com vídeo e prints, a Shopee costuma pagar o vendedor e reembolsar o comprador, que fica marcado; se ele repetir, pode perder o reembolso e ter o CPF bloqueado. Se a disputa for negada sem análise, o vendedor abre um ticket pedindo segunda análise, e o crédito costuma aparecer em "ajustes" na carteira. [PRÁTICA] LUan-VFNxrY · C
- **Devolução Fácil.** Tarifa de R$0,49 por pedido, ligada automaticamente em maio/2026. A saída fica em Pedidos > Configurações de envio > "Devolução Fácil Shopee", com opção de voltar depois. [PRÁTICA, tela] yAmvIlW11GY (2026-05-09) · C. O que o comprador ganha com o programa não foi descrito pela fonte.
- **Loja Oficial.** Oferece 30 dias para devolução ao comprador. [PRÁTICA] r5oEfzPV324 (2024-08-21) · C · **(pode estar superada)**

### 2.7 Logística e reputação

- **Full.** Exige CNPJ, nota da loja >4,5 e ≥5 pedidos/dia, além de requisitos por item. [OFICIAL] TUs6QYGqGrw (2026-08-04) · B
  - Produtos no Full têm acesso a cupons exclusivos e campanhas especiais, e o envio sai todos os dias. [OFICIAL] oUbb0vhDqNs (2026-08-04)
  - O programa Full+ dá redução de comissão de 0,5 a 2 p.p. quando ≥40% dos pedidos saem pelo Full. [OFICIAL] 0oRYednAlHY (2026-08-04)
- **Entrega Turbo.** 1 h para imprimir a etiqueta, senão cancelamento automático; atraso do motorista parceiro não conta contra o vendedor; não postar em 4 h gera atraso e pontos. sqRN4l8OQ-w (2026-05-19) · [OFICIAL via terceiro] · C

---

## 3. O que os melhores fazem

### 3.1 Práticas com consenso (duas ou mais fontes)

- **Vender só o que dá para postar.** Os pontos nascem de atraso ou não envio quando a venda passa a capacidade de separação ou de reposição (quem separa 50–80 peças/dia não vende 100/dia).
  - Fontes: LLDUrAuF3qQ, Rxaok_CtuHM (2026-09-17), sqRN4l8OQ-w. A versão oficial do mesmo princípio: FIFO, pré-embalar os mais vendidos e conferir o estoque da integradora antes de datas de pico. [OFICIAL] urA_Dc9FBvU (2026-09-24). · [PRÁTICA + OFICIAL] · A
- **Nunca pedir ao comprador que cancele.** Dá 2 pontos, mais que o próprio não envio.
  - Fonte: ThPsYQpMxJE. A UpSeller descreve o mesmo critério de atendimento de forma genérica. · B
- **Filmar a bancada de embalagem.** Fonte: LUan-VFNxrY (praticante desde 2014). · [PRÁTICA + OFICIAL] · A
  - Evolução relatada: celular e tripé com 30–60 pedidos/dia; câmera dedicada com cerca de 200/dia; hoje um servidor que grava na nuvem e apaga após 30 dias.
  - Em reclamação suspeita: localizar o pedido pela data de postagem, recortar o trecho, mandar 3 prints e o vídeo.
  - A Shopee passou a recomendar oficialmente o registro em foto ou vídeo. [OFICIAL] 9CxujZDsRCw
- **Configurar o chat antes do volume** (saudação, atalhos, perguntas frequentes) e reescrever a descrição do anúncio com base nas perguntas que chegam.
  - Fontes: Arwxa4I9DgE; LQSOVB8C_G0, canal oficial (2026-07-16), que manda "ajustar o texto com base nas perguntas" do chat. · [PRÁTICA + OFICIAL] · A
- **Separar grupos de atendimento** por pré-venda, pós-venda e devolução quando há equipe.
  - Fontes: tMFZK5GEMlo [OFICIAL]. Na prática, uma operação de R$3,1 milhões/mês tinha 12 pessoas, com 1 no chat e 1 dedicada só a devoluções (multicanal). [PRÁTICA] _p1IBEyvCwo (2026-06-02). · B
- **Olhar a devolução por anúncio, não só por loja.** O caminho é o painel "Diagnóstico do produto > Alta taxa de devolução" e, em seguida, a correção da causa:
  - variação errada → conferência;
  - qualidade → produto;
  - expectativa → foto, descrição e tabela de medidas.
  - Fontes: p8OZWm62pQw; 1Sbvlp1lYD8, oficial (2026-08-06): "tabela de medidas... ajuda demais a evitar devolução"; PeQPVfCjZp8 (2026-07-02): capa enganosa gera devolução e quebra a conversão. · [PRÁTICA + OFICIAL] · A
- **Acompanhar o Indicado toda semana**, com folga em tempo de preparo e TNC.
  - Fontes: 8cRhids_rNs, LLDUrAuF3qQ. · B (as duas são do mesmo autor, então a independência é baixa)

### 3.2 Avaliações: como geram e como respondem

- **Gerar as primeiras avaliações** ("bola de neve" venda → avaliação → venda). Fonte: xrE8fUZ94Y0 (2026-10-13) · [PRÁTICA] · C
  - Preço agressivo no lançamento (MC de 20% reduzida para 5–10%) com Shopee Ads ou, sem verba, Vídeo e "impulsionar". O preço sobe conforme as avaliações chegam.
- **Aumentar a taxa de avaliação** com Transmissão por chat > Atualizações proativas > "Lembrar compradores de avaliar" (pedido concluído com avaliação pendente, benefício em moedas). Fonte: xrE8fUZ94Y0, tela · C
  - O mesmo praticante **não** ativa o aviso de "pedido atrasado", para não chamar atenção a um atraso que o comprador nem notou.
- **Responder avaliações em escala.** Pelo ERP UpSeller, cria-se um modelo com até 10 respostas por nível de estrela e se desliga "só responder avaliações com conteúdo", para responder todas. Fonte: 8X7ZeFArJdQ (2026-07-30) · [PRÁTICA, tela, N6] · C
  - Cuidado do próprio autor: as respostas devem ser genéricas o bastante para não destoar do texto do comprador.
- **Desarmar a avaliação negativa antes que ela aconteça.** Diante de um comprador irritado com atraso causado por feriado e Correios, a vendedora explicou o motivo e ofereceu um cupom para a próxima compra. O comprador avaliou com 5 estrelas e elogiou o atendimento. Fonte: Arwxa4I9DgE · [PRÁTICA, relato de 1 caso] · C
  - A oferta não estava condicionada à avaliação. Condicionar seria arriscado (veja a seção 6).

### 3.3 Divergências entre fontes

| Tema | Fonte A | Fonte B | Leitura |
|---|---|---|---|
| Taxas das faixas 2 e 3 | R$250 / R$500 (ThPsYQpMxJE; LLDUrAuF3qQ para a faixa 3) | R$300 / R$600 (UpSeller 946) | Vence a leitura de tela. Checar no N1. |
| Gatilho de TNC para pontos | ≥8% e ≥2 pedidos (ThPsYQpMxJE); <8% (LLDUrAuF3qQ) | ">10% de TNC" (Bling, 2025-11-28) | Bling (pode estar superada) e sem fonte. Vale 8%. |
| Meta de envio atrasado | <5% (tela do aluno; ThPsYQpMxJE) | o apresentador também diz "<8%" (LLDUrAuF3qQ) | Erro de fala. Vale 5%. |
| TNC do Indicado | <2% para entrar e <3% para continuar (card de mar/2026) | só "<8%" na tela de mai/2026 | Provavelmente são métricas diferentes. Sem N1 direto. |
| Experiência de compra conta arrependimento? | Praticante diz que conta tudo e defende uma calibragem (p8OZWm62pQw) | Sem fonte oficial | Sem evidência N1 sobre exclusões. |
| Full melhora ou piora a reputação? | Oficial: entrega mais rápida e padronizada (TUs6QYGqGrw) | Praticante relata que, na fase de lotação do CD, a Shopee "afetando a conta" com atrasos e cancelamentos; ficou 20 dias sem coleta no início (Vfbc25kqgYs, 2026-05-05) | Sem regra oficial sobre de quem é o atraso do Full. |

---

## 4. Números de referência

| # | Número / limite | Valor | Fonte | Data | Tipo | Confiança |
|---|---|---|---|---|---|---|
| N1 | Início da punição | 3 pontos (1–2 = só aviso) | ThPsYQpMxJE; LLDUrAuF3qQ; UpSeller 946 | 2026-05 a 08 | OFICIAL via terceiro + DADO | A |
| N2 | Janela dos pontos | trimestre civil, zera na virada | idem | 2026 | OFICIAL via terceiro | A |
| N3 | Visibilidade por faixa | −5% / −10% / −20% / −30% / conta congelada | ThPsYQpMxJE; LLDUrAuF3qQ | 2026-05/08 | OFICIAL via terceiro | B |
| N4 | Taxa por faixa | R$100 / 250 / 500 / 1.000 / 1.500 | ThPsYQpMxJE (UpSeller: 100/300/600/1.000/1.500) | 2026-08 | OFICIAL via terceiro | B (divergência) |
| N5 | Duração da punição | 14 / 14 / 21 / 28 / 28 dias | ThPsYQpMxJE; LLDUrAuF3qQ | 2026 | OFICIAL via terceiro | B |
| N6 | Frete grátis | mantém na faixa 1 e perde a partir da faixa 2 | ThPsYQpMxJE; LLDUrAuF3qQ | 2026 | OFICIAL via terceiro | B |
| N7 | Ponto por não envio | ≥8% e ≥2 pedidos = 1 pt; ≥90 = 2 pts | ThPsYQpMxJE | 2026-08-05 | OFICIAL via terceiro | B |
| N8 | Ponto por atraso | ≥5% e ≥2 pedidos = 1 pt; ≥90 = 2 pts | ThPsYQpMxJE; LLDUrAuF3qQ (meta <5%) | 2026 | OFICIAL via terceiro | B |
| N9 | Condutas no atendimento | 2 pts cada (chat abusivo, levar para fora, pedir cancelamento, resposta abusiva a avaliação) | ThPsYQpMxJE | 2026-08-05 | OFICIAL via terceiro | B |
| N11 | Isenção da taxa | GMV <R$2.500 no mês anterior | UpSeller 946 | 2026-07-07 | DADO (sem link N1) | C |
| N13 | Taxa de resposta do chat | 12 h, últimos 30 dias, inclui fins de semana e feriados | Arwxa4I9DgE (lendo o artigo oficial) | 2026-06-05 | OFICIAL via terceiro | B |
| N14 | Chat no Indicado | ≥60% para entrar, <50% tira | 8cRhids_rNs; Arwxa4I9DgE ("acima de 60%") | 2026-03/06 | OFICIAL via terceiro | B (pode estar superada) |
| N15 | Nota da loja no Indicado | >4,5 para entrar, <4,2 tira | 8cRhids_rNs | 2026-03-18 | OFICIAL via terceiro | C (pode estar superada) |
| N16 | Nota da loja no Full | >4,5 + ≥5 pedidos/dia + CNPJ | TUs6QYGqGrw | 2026-08-04 | OFICIAL | B |
| N17 | Preparo no Indicado | ≤1 dia útil para entrar, >1,3 tira | 8cRhids_rNs; LLDUrAuF3qQ (<1 dia) | 2026-03/05 | OFICIAL via terceiro | B |
| N18 | Envios aos sábados | ≥20% | 8cRhids_rNs; LLDUrAuF3qQ | 2026-03/05 | OFICIAL via terceiro | B |
| N22 | Devolução Fácil | R$0,49 por pedido, automática desde mai/2026 | yAmvIlW11GY | 2026-05-09 | PRÁTICA | C |
| N25 | Taxa de avaliação observada | ~56% (11,2 mil/20 mil) contra ~72% (14,4 mil/20 mil) em dois anúncios | xrE8fUZ94Y0 (tela, sem data da coleta) | 2026-10-13 | OBS via praticante | C |
| N26 | Devolução numa operação grande | 0,7% a 1% das vendas/mês (multicanal, R$3,1 mi/mês) | _p1IBEyvCwo | 2026-06-02 | PRÁTICA (rebaixado de CASE: sem período nem base) | C |

Sobre o N25: dizer que a diferença vem do lembrete de avaliação é hipótese do praticante, não causalidade (sinal fraco 11).

**Margem de segurança usada pelos operadores.** Nenhuma fonte publica um alvo interno numérico. O que se pode reconstruir é isto:

- A régua mais apertada que existe é a do Indicado (TNC <2–3%, preparo ≤1 dia, chat ≥60%), e os praticantes tratam essa régua como meta operacional. A régua de pontos (8% e 5%) fica bem mais folgada.
- Na métrica de atraso, a semana é a unidade de controle, porque a punição chega na semana seguinte.
- O critério de "≥2 pedidos" protege a loja pequena, mas uma loja grande alcança "≥90 pedidos" numa única semana ruim. Uma semana com 21% de atraso bastou para levar uma loja a 3 pontos (LLDUrAuF3qQ).
- Não há benchmark de tempo de primeira resposta na Shopee. A UpSeller cita "15% de chance de fechamento perdida por hora" e "68% decidem pela velocidade", mas os números são do Mercado Livre ou genéricos, sem base publicada (sinal fraco 2). Não usar.

---

## 5. Alimentos, perecíveis e marca própria/indústria

- **Embalagem e itens com condição especial.** O guia oficial diz que produtos com condições específicas de transporte podem ter regras adicionais de embalagem, identificação e documentação. Também manda aplicar a diretriz mais segura quando o pedido mistura itens. [OFICIAL] 9CxujZDsRCw (2026-10-01) · B
  - Para alimentos (vazamento, odor, frágil) valem três pontos: separar os itens dentro da caixa, usar sinalização impressa (marcação à mão pode ser recusada) e usar lacre de violação em item de valor.
- **Reclamações típicas de alimentos.** Item avariado ou vazado e "não recebi conforme" entram em "devolução/reembolso por erro do vendedor", que soma na TNC (LLDUrAuF3qQ). A evidência de embalagem, em foto ou vídeo, é o que sustenta a contestação (9CxujZDsRCw, LUan-VFNxrY).
  - Arrependimento em alimentos: não houve fonte específica da Shopee sobre devolução de alimento aberto ou perecível. **Sem evidência.**
- **Tempo de preparação e "moído no dia".** Na busca "café em grãos", líderes usam o título "Moído Dia do Envio". [OBS] lideres.md (2026-10-14)
  - Quem promete moer ou torrar sob demanda precisa caber em preparo ≤1 dia útil (Indicado) e na régua de envio atrasado <5% (pontos). Torra ou moagem sob encomenda empurra para "pré-venda", que tem teto de 20% dos produtos (LLDUrAuF3qQ). · inferência a partir de [OFICIAL via terceiro] · C
- **Atributo Anvisa.** A Shopee passou a exigir o atributo Anvisa em novos anúncios de algumas categorias, enquanto os antigos ficam como estão "por enquanto". [OFICIAL via terceiro] RvJiFGQiK3c (2026-09-14) · C. Anúncio irregular é violação de anúncio, e violação gera pontos (2.3).
- **Marca própria e reputação da loja.**
  - Na busca observada, lojas de marca/torrefação com selo Oficial ou Full lideram, e vendedores menores aparecem com selo Indicado. [OBS] lideres.md · C
  - O Full exige nota da loja >4,5 (TUs6QYGqGrw). Para a indústria que quer o Full, a nota da loja é porta de entrada, não apenas resultado.
- **Avaliação com foto em alimentos.** O argumento de que a avaliação com foto ou vídeo é a prova social que o carrossel não dá (xrE8fUZ94Y0) pesa mais em produto sensorial. Não houve dado específico da categoria. **Sem evidência quantitativa.**

---

## 6. Erros comuns e mitos

| Mito ou erro | O que as fontes fortes dizem |
|---|---|
| "Pagou a punição, os pontos somem." | Não somem. Os pontos continuam até o fim do trimestre e se acumulam (LLDUrAuF3qQ; UpSeller 946). |
| "Peço para o cliente cancelar e fujo da TNC." | Dá 2 pontos de uma vez, mais que o próprio não envio (ThPsYQpMxJE). |
| "Atrasei mas enviei, então não conta." | Conta na taxa de atraso (≥5% gera ponto). Só não entra na TNC (LLDUrAuF3qQ). |
| "A IA do chat cuida da minha taxa de resposta." | Segundo a praticante, a resposta da IA não conta (Arwxa4I9DgE, C). A regra oficial das 12 h vale todos os dias, inclusive fins de semana. |
| "TNC acima de 10% gera pontos." (Bling, 2025-11-28) | O gatilho lido em 2026 é 8% com ≥2 pedidos (ThPsYQpMxJE). A fonte da Bling não tem link e é antiga. |
| "Avaliação comprada ou trocada por brinde é atalho." | O canal oficial pede promoções verdadeiras e proíbe prática enganosa (aUqdtKFx5gM). O benefício por avaliar que existe na plataforma é o próprio lembrete com moedas da Shopee. Não se achou regra textual sobre avaliação incentivada pelo vendedor (lacuna). |
| "Experiência de compra só pune erro do vendedor." | Segundo um praticante, conta todo tipo de reclamação, inclusive arrependimento (p8OZWm62pQw, C). Sem N1 sobre exclusões. |
| "Vendedor Indicado não muda nada." | Um praticante relata queda forte de vendas desde jul/2025 para quem perdeu o selo (8cRhids_rNs). O selo também some por 14–28 dias em qualquer faixa de pontos (ThPsYQpMxJE). Não há medição pública. |
| "A Shopee já está multando em R$1.500" (título alarmista) | O valor existe, mas só na faixa 5 (≥15 pontos), junto com o congelamento da conta (ThPsYQpMxJE). |

Sinais fracos encontrados:

- Canal Caue Oliveira: CTA de curso e afirmações sem número. As telas foram usadas como OFICIAL via terceiro; as opiniões, rebaixadas a C.
- Pedidos embutidos, ignorados: "comente penalidade" (ThPsYQpMxJE) e "dossiê para a Shopee" (p8OZWm62pQw).
- UpSeller: conflito de interesse e nenhum link oficial.
- Podcasts oficiais: "feitos com inteligência artificial", genéricos e com poucos números.

---

## 7. Revenda/importação x indústria/marca própria

| Tema | [REVENDA] revenda, drop, importação | [MARCA] indústria, marca própria | [AMBOS] |
|---|---|---|---|
| Origem dos pontos | Ruptura do fornecedor e prazo do dropshipper geram não envio e atraso. É a causa mais citada (LLDUrAuF3qQ, "às vezes é o seu fornecedor") | Capacidade de produção ou torra, e lote, limitam o ritmo de venda (LLDUrAuF3qQ, "sua fábrica") | A regra de 8%/5% vale igual para todos |
| Pré-venda | Drop com prazo longo cai em "encomenda" (teto de 20%) | Produção sob demanda também cai | — |
| Devolução e golpe | Item de terceiro: mais risco de "produto diferente". Exige conferência e vídeo (LUan-VFNxrY) | A marca controla a especificação. A devolução vira dado de produto (gramatura, qualidade; p8OZWm62pQw) | Filmar a embalagem (oficial) |
| Chat | Dúvidas repetitivas sobre cor, estampa e prazo resolvidas com atalhos e perguntas frequentes (Arwxa4I9DgE, drop de 3-6-9 Shops) | Dúvidas técnicas do produto. A descrição deve ser reescrita a partir do chat (LQSOVB8C_G0) | 12 h, 30 dias, fins de semana contam |
| Avaliações | Concorre no mesmo produto com quem já tem milhares de avaliações. Por isso usa preço agressivo e Ads no lançamento (xrE8fUZ94Y0) | As avaliações se acumulam no anúncio da própria marca, e a Loja Oficial dá mais prazo de devolução ao comprador (r5oEfzPV324, pode estar superada) | Lembrete de avaliação com moedas |
| Selo | O Indicado exige CNPJ, então CPF fica fora (8cRhids_rNs) | Selo Oficial e Full em destaque na busca (lideres.md) | O Full exige nota >4,5 |
| Falsificação | Itens falsificados tiram do Indicado. Réplica é proibida em Vídeo e Live (8cRhids_rNs; aUqdtKFx5gM) | A marca sofre falsificação de terceiros: uma indústria de cosméticos mapeou 604 falsificações em duas semanas (EitJfemXOXA, 2026-07-23, multicanal) | — |

---

## 8. Tabela de afirmações

| id | Afirmação | Tipo | Fonte | Data | Confiança | Rev/Marca | Pode estar superada? |
|---|---|---|---|---|---|---|---|
| A1 | A saúde da conta tem três pilares (pedidos, produto, atendimento), com cálculo semanal | OFICIAL via terceiro | LLDUrAuF3qQ | 2026-05-14 | média | ambos | não |
| A2 | Os pontos se acumulam no trimestre civil e zeram na virada | OFICIAL via terceiro | ThPsYQpMxJE; LLDUrAuF3qQ; UpSeller 946 | 2026-05/08 | alta | ambos | não |
| A3 | Com 1–2 pontos há só aviso; a punição começa em 3 | OFICIAL via terceiro | ThPsYQpMxJE; LLDUrAuF3qQ; UpSeller 946 | 2026 | alta | ambos | não |
| A4 | Faixa 1 (3–5 pts): 14 dias sem Indicado e campanhas, −5% de visibilidade, mantém frete grátis, R$100 | OFICIAL via terceiro | ThPsYQpMxJE; LLDUrAuF3qQ | 2026 | média | ambos | não |
| A5 | Faixa 2 (6–8 pts): 14 dias, −10%, perde frete grátis, R$250 (UpSeller: R$300) | OFICIAL via terceiro | ThPsYQpMxJE | 2026-08-05 | média | ambos | não |
| A6 | Faixa 3 (9–11): 21 dias, −20%, R$500; faixa 4 (12–14): 28 dias, −30%, R$1.000 | OFICIAL via terceiro | ThPsYQpMxJE; LLDUrAuF3qQ | 2026 | média | ambos | não |
| A7 | Faixa 5 (≥15 pts): conta congelada por 28 dias e taxa de R$1.500 | OFICIAL via terceiro | ThPsYQpMxJE; UpSeller 946 | 2026 | média | ambos | não |
| A8 | Pagar ou cumprir a punição não zera os pontos | OFICIAL via terceiro + DADO | LLDUrAuF3qQ; UpSeller 946 | 2026 | média | ambos | não |
| A9 | Não envio ≥8% com ≥2 pedidos = 1 pt; com ≥90 pedidos = 2 pts | OFICIAL via terceiro | ThPsYQpMxJE | 2026-08-05 | média | ambos | não |
| A10 | Envio atrasado ≥5% com ≥2 pedidos = 1 pt; com ≥90 = 2 pts | OFICIAL via terceiro | ThPsYQpMxJE; LLDUrAuF3qQ | 2026 | média | ambos | não |
| A11 | Cancelamento a pedido do comprador não entra na TNC; o do vendedor e o automático entram | OFICIAL via terceiro | LLDUrAuF3qQ | 2026-05-14 | baixa | ambos | não |
| A12 | Devolução ou reembolso por erro do vendedor entra na TNC | OFICIAL via terceiro | LLDUrAuF3qQ | 2026-05-14 | baixa | ambos | não |
| A13 | Chat abusivo, levar o comprador para fora, pedir cancelamento e resposta abusiva a avaliação dão 2 pts cada | OFICIAL via terceiro | ThPsYQpMxJE | 2026-08-05 | média | ambos | não |
| A14 | Violações de anúncio: média 2–9 = 1 pt, ≥10 = 2; alta 2–9 = 2, ≥10 = 3; extrema 2–9 = 3 | OFICIAL via terceiro | ThPsYQpMxJE | 2026-08-05 | média | ambos | não |
| A15 | Isenção da taxa para GMV <R$2.500 no mês anterior | DADO | UpSeller 946 | 2026-07-07 | baixa | ambos | não |
| A16 | Contestação em até 14 dias; reenvio obrigatório em 7 dias | DADO | UpSeller 946 | 2026-07-07 | baixa | ambos | não |
| A17 | Indicado: nota >4,5 para entrar e <4,2 tira; chat ≥60% e <50% tira; TNC <2% e >3% tira; pontos ≤1 e ≥3 tira | OFICIAL via terceiro | 8cRhids_rNs | 2026-03-18 | baixa | ambos | **sim** |
| A18 | Indicado exige CNPJ, loja com >90 dias, >30 pedidos e >10 compradores únicos em 30 dias, ≥20% dos envios aos sábados e preparo ≤1 dia útil | OFICIAL via terceiro | 8cRhids_rNs; LLDUrAuF3qQ | 2026-03/05 | média | ambos | parcial (março) |
| A19 | Indicado revisto toda semana (revisão no domingo, atualização na terça) | PRÁTICA | 8cRhids_rNs | 2026-03-18 | baixa | ambos | sim |
| A20 | Taxa de resposta: chats que exigem resposta, 30 dias, 12 h, fins de semana e feriados contam | OFICIAL via terceiro | Arwxa4I9DgE | 2026-06-05 | média | ambos | não |
| A22 | Gestão de chat roteia pela origem do clique, devolve ao mesmo agente em 12 h e tem regra de longa espera | OFICIAL | tMFZK5GEMlo | 2026-08-18 | média | ambos | não |
| A23 | Shopee recomenda registrar a embalagem em foto ou vídeo para contestação | OFICIAL | 9CxujZDsRCw | 2026-10-01 | média | ambos | não |
| A24 | Embalagem inadequada recorrente pode reduzir visibilidade, remover produtos e gerar violação e penalidade | OFICIAL | 9CxujZDsRCw | 2026-10-01 | média | ambos | não |
| A25 | Full exige CNPJ, nota da loja >4,5 e ≥5 pedidos/dia | OFICIAL | TUs6QYGqGrw | 2026-08-04 | média | ambos | não |
| A26 | Devolução Fácil cobra R$0,49 por pedido, automática desde mai/2026, com opção de sair | PRÁTICA | yAmvIlW11GY | 2026-05-09 | baixa | ambos | não |
| A27 | Devolução por motivo atribuído ao vendedor custa cerca de R$15 | PRÁTICA | LUan-VFNxrY | 2026-07-16 | baixa | ambos | não |
| A29 | Anúncio com alta taxa de devolução perde visibilidade (Experiência de compra); diagnóstico em Diagnóstico do produto | PRÁTICA | p8OZWm62pQw | 2026-09-11 | baixa | ambos | não |
| A30 | Lembrete de avaliação com moedas em Transmissão por chat > Atualizações proativas | PRÁTICA (tela) | xrE8fUZ94Y0 | 2026-10-13 | baixa | ambos | não |
| A31 | Lançamento com margem de 20% reduzida para 5–10% mais Ads para gerar as primeiras avaliações | PRÁTICA | xrE8fUZ94Y0 | 2026-10-13 | baixa | revenda | não |
| A33 | Pré-venda acima de 20% dos produtos afeta o limite de anúncios | OFICIAL via terceiro | LLDUrAuF3qQ | 2026-05-14 | baixa | ambos | não |
| A36 | Arrependimento em 7 dias; vendedor tem 3 dias para avaliar o item devolvido, senão reembolso automático | DADO | UpSeller 246 | 2025-09-19 | baixa | ambos | **sim** |
| A37 | Uma operação de R$3,1 mi/mês tem 0,7–1% de devolução e uma pessoa dedicada a devoluções | PRÁTICA | _p1IBEyvCwo | 2026-06-02 | baixa | marca (multicanal) | não |
| A38 | "TNC acima de 10% gera pontos" | DADO (blog, sem fonte) | blog.bling.com.br/cancelar-venda-na-shopee | 2025-11-28 | baixa (contrariada) | ambos | **sim** |

---

## 9. Lacunas

1. **Páginas N1 não lidas diretamente.** O help center e o Centro de Educação só carregam com JavaScript, e o WebSearch da rodada estava esgotado. Ficaram sem abrir `help.shopee.com.br/portal/4/article/76428-Normas-Políticas-de-Desempenho-do-Vendedor` e `seller.shopee.com.br/edu/article/23724/mudanca-no-prazo-de-envio-de-pedidos-DTS0`, ambos citados pela Bling. A meta de 6 fontes oficiais foi cumprida só com 11 vídeos do canal oficial e telas mostradas por terceiros. **Faixas, taxas e o card do Indicado devem ser conferidos pelo agente de navegador.**
2. **Taxas das faixas 2 e 3** (R$250/500 contra R$300/600) e a **isenção abaixo de R$2.500 de GMV**: sem N1 lido.
3. **Experiência de compra na Shopee.** Não se achou documento oficial com fórmula, janela, limiar ou lista de motivos excluídos (arrependimento, "não serviu", atraso da transportadora). Só há opinião de praticante.
4. **O que fica fora do cálculo.** Não há regra oficial lida sobre atraso causado pelo Full ou pela transportadora da Shopee, nem sobre greve ou caso fortuito. A única exceção documentada é o atraso do motorista na Entrega Turbo (via terceiro).
5. **Fórmula da nota da loja.** Não se sabe se é média simples, qual a janela, nem se há peso para avaliações recentes. Também não se achou regra textual sobre **avaliação incentivada pelo vendedor** (brinde por 5 estrelas) nem sobre remoção ou contestação de avaliação.
6. **Benchmarks.** Não há dado público de tempo de primeira resposta, taxa média de avaliação, taxa de devolução por categoria ou TNC média na Shopee Brasil. Os números do blog UpSeller são de ML ou genéricos, sem base publicada.
7. **Indicado atualizado.** O card é de mar/2026 (pode estar superado). Falta confirmar se os limites mudaram depois de 2026-04-14 e como fica a divergência de TNC (2–3% contra 8%).
8. **Alimentos e perecíveis.** Não se achou política Shopee específica sobre devolução de alimento, validade mínima na entrega ou embalagem de perecíveis.
9. **ML e Amazon** (Experiência de compra por anúncio, MercadoLíder, Featured Offer, motivos de devolução no POE): fora desta nota. Na Shopee, o equivalente mais próximo é "Diagnóstico do produto > Alta taxa de devolução" (p8OZWm62pQw).
10. **Cases com número, período e base** sobre reputação na Shopee: nenhum. O único número operacional (0,7–1% de devolução) não tem período, base nem separação por canal.

---

## 10. Verificação (2026-10-14)

**Limite da verificação.** O orçamento de WebSearch da rodada estava esgotado (todas as buscas foram recusadas). As páginas oficiais tentadas por WebFetch (`help.shopee.com.br/portal/4/article/76428` e `seller.shopee.com.br/edu/article/23724`) devolveram só o título ("Help Center" / "Seller Education Hub"), pois exigem JavaScript. Nenhuma afirmação pôde ser refutada nem confirmada contra texto oficial atual. Pela regra "na dúvida, não confirme", nenhuma recebe CONFIRMADA. O veredito abaixo diz "sem fonte oficial lida", o que não significa que a regra esteja errada. Todas as regras de plataforma têm mais de 6 meses de dúvida ou dependem de fonte de terceiro: tratar como "pode estar superada" até conferência pelo agente de navegador.

| id | veredito | fonte oficial (URL) | observação |
|---|---|---|---|
| A3 | SEM FONTE OFICIAL | tentada: help.shopee.com.br/portal/4/article/76428 (não renderizou) | Só vídeos e blog afirmam. Conferir se o acúmulo é trimestral e se a punição começa em 3 pontos. |
| A4 | SEM FONTE OFICIAL | tentada: help.shopee.com.br/portal/4/article/76428 (não renderizou) | Faixa 1 (R$100, -5%, 14 dias) vem de tela mostrada em vídeo [PRÁTICA]. Sem texto oficial lido. |
| A5 | SEM FONTE OFICIAL | tentada: help.shopee.com.br/portal/4/article/76428 (não renderizou) | Divergência R$250/500 (vídeo) contra R$300/600 (UpSeller) segue em aberto. Não resolvida. |
| A7 | SEM FONTE OFICIAL | tentada: help.shopee.com.br/portal/4/article/76428 (não renderizou) | Faixas 4 e 5 (R$1.000 / R$1.500, congelamento de 28 dias) só por vídeo e blog. |
| A9-A10 | SEM FONTE OFICIAL | tentada: seller.shopee.com.br/edu/article/23724 (não renderizou) | Limiares de 8% (não envio) e 5% (atraso) e a regra de 2 pontos com 90 pedidos não verificados em texto oficial. |
| A13 | SEM FONTE OFICIAL | tentada: help.shopee.com.br/portal/4/article/76428 (não renderizou) | Lista de condutas com 2 pontos só em vídeo. |
| A11-A12 | SEM FONTE OFICIAL | tentada: help.shopee.com.br (não renderizou) | Composição da TNC vista em tela de vídeo. A contradição com a nota de blog "TNC acima de 10%" (A38) continua sem solução. |
| A17 | SEM FONTE OFICIAL | tentada: seller.shopee.com.br/edu (não renderizou) | Card de mar/2026: pode estar superado. Não se confirmou se os limites mudaram depois. |
| A20 | SEM FONTE OFICIAL | tentada: help.shopee.com.br (não renderizou) | Janela de 30 dias e prazo de 12 h só via leitura de terceiro. |
| A25 | SEM FONTE OFICIAL | tentada: seller.shopee.com.br/edu (não renderizou) | O vídeo é do canal oficial, mas não foi reconferido contra página escrita. Não confirmar sem texto atual. |
| A26 | SEM FONTE OFICIAL | tentada: help.shopee.com.br (não renderizou) | Tarifa de R$0,49 e ativação automática só por vídeo de praticante. Tarifa: pode estar superada. |
| A15-A16 | SEM FONTE OFICIAL | nenhuma (só UpSeller, sem link oficial) | Isenção abaixo de R$2.500 de GMV, 14 dias de contestação, 7 dias de reenvio e lançamento às segundas: apenas blog. Prioridade máxima para conferência. |

**Pendência para o agente de navegador:** abrir as duas páginas oficiais acima com JavaScript e conferir, na ordem, A15-A16, A5, A17, A4/A7, A9-A10, A26.

## 11. Verificação pelo navegador (2026-10-15)

Chrome com JavaScript, só leitura, sem login. Fontes: Centro de Educação do Vendedor, Central de Ajuda, ads.shopee.com.br e blog oficial.

| id | veredito | fonte oficial | observação |
|---|---|---|---|
| A3 | CONFIRMADA | https://seller.shopee.com.br/edu/article/7955 (20-02-2026 (atualizado em 09/09/2026)) | 3 pontos ou mais restringem vantagens. A contagem é trimestral e os pontos zeram no fim do trimestre. |
| A4 | CONFIRMADA | https://seller.shopee.com.br/edu/article/7955 (20-02-2026 (atualizado em 09/09/2026)) | Quadro (imagem), faixa 3-5: 14 dias sem Indicado e campanhas, -5% de visibilidade, mantém frete grátis. |
| A5 | CONFIRMADA | https://seller.shopee.com.br/edu/article/7955 (20-02-2026 (atualizado em 09/09/2026)) | Faixa 6-8: 14 dias, -10%, perde frete grátis, R$250. O valor de R$300 do UpSeller está errado; R$500 é a faixa 9-11. |
| A7 | CONFIRMADA | https://seller.shopee.com.br/edu/article/7955 (20-02-2026 (atualizado em 09/09/2026)) | 15+ pontos = 28 dias de conta congelada e R$1.500. Faixa 4 (12-14) = 28 dias, -30%, R$1.000. Na faixa 5, a cada 3 pontos a mais o congelamento recomeça. |
| A9-A10 | CONFIRMADA | https://seller.shopee.com.br/edu/article/7955; https://seller.shopee.com.br/edu/article/3280 (20-02-2026; 06-05-2026) | Quadro: não envio de 8% ou mais = 1 pt; com 90 ou mais = 2 pts. Atraso de 5% ou mais, com as mesmas contagens. TNE acima de 40% na semana = +1 ponto. |
| A13 | CONFIRMADA | https://seller.shopee.com.br/edu/article/7955 (20-02-2026 (atualizado em 09/09/2026)) | Quadro de chat, 2 pontos: resposta abusiva ou que leva para fora da plataforma, pedir que o comprador cancele, resposta abusiva a avaliação. Se persistir, +4 pontos. |
| A11-A12 | CONFIRMADA | https://seller.shopee.com.br/edu/article/3280 (06-05-2026) | Só conta o que for responsabilidade do vendedor; 'aparece na Central do Vendedor como Taxa de Não Cumprimento'. Resolve A38: o ponto vem com TNE acima de 8%, não 10% (os 10% do 7955 são só exemplo de recálculo em apelação). |
| A17 | CONFIRMADA | https://seller.shopee.com.br/edu/article/18456 (04-02-2026 (atualizado em 29/06/2026)) | Tabela (imagem): chat 60% ou mais (sai abaixo de 50%); TNE até 2% (sai acima de 3%); até 1 ponto (sai com 3 ou mais). Ressalvas: a nota de entrada é 4,5 ou mais, não acima de 4,5; a métrica é TNE, que a Central chama de TNC. |
| A20 | CONFIRMADA | https://seller.shopee.com.br/edu/article/2713 (31-07-2025) | Janela de 30 dias; fins de semana e feriados contam. Peso maior para os 25% de chats mais recentes; precisa de no mínimo 2 chats. |
| A25 | PARCIAL | https://seller.shopee.com.br/edu/article/23197; https://seller.shopee.com.br/edu/article/26370 (26-01-2026; 29-10-2025) | CNPJ confirmado (26370, rodada anterior). Nota acima de 4,5 e 5 pedidos/dia não aparecem; o 23197 lista requisitos por item (R$20, 10 ou 5 un./mês, 30 kg, dimensões). |
| A26 | PARCIAL | https://seller.shopee.com.br/edu/article/26700 (22-04-2026 (atualizado em 17/08/2026)) | Confirmados R$0,49 por pedido, ativação automática e saída a qualquer momento. Divergência: ativação automática 'desde abril de 2026', com 30 dias grátis, não maio. Só para lojas elegíveis por métricas. |
| A15-A16 | CONFIRMADA | https://seller.shopee.com.br/edu/article/7955 (20-02-2026 (atualizado em 09/09/2026)) | Isenção com VBM abaixo de R$2.500 no mês anterior; recurso em até 14 dias; 7 dias para reenvio; pontos atribuídos às segundas e penalização na segunda seguinte. |
