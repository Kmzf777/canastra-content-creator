# Reputação, atendimento e pós-venda: Mercado Livre Brasil

Frente: reputacao-atendimento · Plataforma: Mercado Livre (MLB) · Data da nota: 2026-10-14 · Analista: frente reputacao-atendimento

**Como ler esta nota**
- **Tipos:** [OFICIAL] página da plataforma; [OFICIAL via terceiro] regra oficial descrita por blog ou ferramenta; [PRÁTICA] tática de praticante; [CASE] número com período e base; [DADO] estudo ou ferramenta; [OBS] observação direta.
- **Confiança:** A, B ou C, conforme o protocolo.
- **Datas das páginas de ajuda:** as páginas da Central de Ajuda (mercadolivre.com.br/ajuda/<id>) não mostram data. Todas foram lidas em 2026-10-14. Quando uma regra sem data é confirmada por uma fonte de 2026, ela é tratada como vigente. Quando não há essa confirmação, leva "(pode estar superada)".
- **Escopo:** a nota cobre o Mercado Livre. Para Shopee e Amazon não foi coletada evidência oficial nesta rodada, porque as páginas exigem login ou não renderizaram (ver seção 9).
- **Fontes lidas:** 11 transcrições da frente na íntegra, mais trechos de 33 transcrições de apoio (11 citadas); 37 páginas oficiais (31 da Central de Ajuda e da Central de Vendedores, 6 documentos para developers, lidas em 14/10/2026); 4 fontes de dados ou ferramentas (Hunter HUB, Terazi, Bling, UpSeller), mais resumos da Nubimetrics vistos em busca; observação de líderes (observacao/lideres.md).

---

## 1. Resumo executivo

1. **Janela de medição (desde 10/09/2026):** com 101+ vendas concluídas em 60 dias, mede 60 dias; abaixo disso, 365 dias. Sem reputação (cinza) até 10 vendas em 365 dias. O corte antigo era 60. [OFICIAL] ajuda/866 e nota oficial de reputação; 6QFwvsIPSkQ (02/09/2026). A.
2. **Variáveis:** reclamações, canceladas por você e envios incorretos; mediação só para MercadoLíder; vale a pior variável. [OFICIAL] ajuda/30193, ajuda/20245. A.
3. **Verde:** reclamações ≤ 2%; cancelamentos ≤ 1,5% (60d) ou 2,5% (365d); envios ≤ 10% (60d) ou 13% (365d). MercadoLíder: < 1%, < 0,5%, < 6% e mediações < 0,5%. [OFICIAL] nota oficial; ajuda/864. A.
4. **Escala de 60 dias (Líder/verde/amarelo/laranja; acima, vermelho):** reclamações 1/2/4,5/8%; cancelamentos 0,5/1,5/3,5/4%; atraso 6/10/18/22%. [OFICIAL] developers/reputacao-de-vendedores (11/08/2025, pode estar superada), confirmada por Hunter HUB e Terazi. A.
5. **Exclusões:** arrependimento, cancelamento pelo comprador, problema da transportadora alheio ao vendedor, devolução "não serve"; só reclamações de produto incompleto, faltante ou com defeito de qualidade afetam (pacote avariado não). [OFICIAL] ajuda/30193, 5205, 3285. A (pacote avariado: B).
6. **48 h:** reclamação com `has_incentive` respondida bem em 48 h não afeta; o canal oficial orienta resolver em até 24 h para evitar mediação. [OFICIAL] developers/gerenciar-reclamacoes (20/08/2026); Ag1UXXB1fec. A.
7. **Cancelamento é a variável mais apertada:** acima de 2,5% a conta pode ser suspensa; praticantes preferem atrasar a cancelar. [OFICIAL] ajuda/5205; [PRÁTICA] HRmtJMCZdZw. A.
8. **Cor muda custo e acesso:** verde tem melhor busca, catálogo, Publicidade, desconto de frete e dinheiro mais cedo (ajuda/21065); frete até 50% de desconto no verde, 40% no amarelo, 0% em laranja e vermelho (Hunter, Terazi); Ads exige amarelo ou melhor (JzejZyVeauE). A.
9. **MercadoLíder:** 230/575/1.725 vendas e R$ 37 mil/118,4 mil/296 mil em 3 meses mais o mês corrente, com 4+ meses de conta e verde escuro. [OFICIAL] ajuda/864. A.
10. **Experiência de compra por anúncio:** nota 0–100 (boa 100–75, média 74–50, ruim ≤ 30), janela de 180 dias; média perde exposição e pode ser pausada, ruim pode ser cancelada; kit herda o pior produto. [OFICIAL] ajuda/39234, developers (03/02/2026). A.
11. **Proteções pagas:** Decola (R$ 250, até 365 dias, 5 vendas afetadas) [OFICIAL] ajuda/33314; Reputação Protegida (1% a 3% do faturamento de 60 dias, até 60 dias) [OFICIAL] ajuda/29276; Benefício de Reputação (R$ 75 a R$ 250 mil, 120 dias) [OFICIAL via terceiro]. A/A/B.
12. **Devolução:** 30 dias (novo) ou 5 (usado); o motivo define custo e impacto: arrependimento é grátis para o vendedor e não afeta; defeito ou diferente custa e afeta. [OFICIAL] ajuda/3285, 28088, 32761. A.
13. **Full:** o Mercado Livre despacha, responde reclamações de entrega e faz triagem das devoluções em 3 dias úteis; a qualidade do produto segue com o vendedor. [OFICIAL] ajuda/5171, 19200. A.
14. **Opiniões não afetam a cor** (ajuda/15040, 851). Não há ferramenta oficial para o vendedor pedir avaliação; o campo livre de mensagem some após a entrega (developers, 28/09/2026). A.
15. **Blogs ainda circulam limites antigos** (3%, 15%, "60 vendas"), herdados da página superada ajuda/4421 e da doc de 2025 (Bling 30/09/2025; Nubimetrics). A.

---

## 2. Como funciona (mecânica e regras oficiais)

### 2.1 Reputação da conta (termômetro)

**Ativação e janela** [OFICIAL] ajuda/866, nota "por que a reputação é importante", ajuda/30193 (lidas em 14/10/2026)
- O vendedor fica cinza até concluir 10 vendas nos últimos 365 dias.
- Com 101 vendas concluídas ou mais nos últimos 60 dias, é medido por 60 dias; com menos, por 365 dias.
- A janela é recalculada todo dia, contada a partir da data atual.
- O corte de 101 entrou em vigor em 10/09/2026 (6QFwvsIPSkQ, 02/09/2026; Terazi, 16/09/2026).
- A documentação de developers (11/08/2025) ainda mostra 60 vendas para o MLB e está desatualizada nesse ponto.
- O vídeo i9MQ51OkODg (21/08/2026) fala em "68 vendas", número que nenhuma outra fonte confirma.

**Fórmulas** [OFICIAL] ajuda/20243, ajuda/20245, developers/reputacao-de-vendedores
- Reclamações = vendas com reclamação ÷ total de vendas. No carrinho, cada produto diferente conta como uma venda.
- Mediações = vendas com reclamação em mediação ÷ total de vendas. Só conta para MercadoLíder.
- Cancelamentos = vendas canceladas pelo vendedor sem reclamação ÷ total de vendas.
- Envio com atraso (*handling time*) = vendas despachadas com atraso ÷ vendas enviadas pelo Mercado Envios 2.
  - A métrica só se aplica a quem tem 10 ou mais vendas enviadas.
  - Num carrinho com vários pedidos no mesmo pacote, o atraso conta uma vez por pedido.

**O que é "envio incorreto"** [OFICIAL] ajuda/30193, ajuda/57334
- despacho com atraso;
- envio a partir do depósito errado;
- no Flex: entrega não feita até as 21 h e reagendada, tentativa com comprador ausente depois das 21 h, ou envio atrasado que o comprador cancela;
- um envio cancelado depois de atrasar também afeta.

**O que é "cancelamento"** [OFICIAL] ajuda/5205
- É qualquer devolução do dinheiro antes da entrega, pedida por qualquer das partes.
- Conta contra o vendedor quando ele clica em "Cancelar venda" ou devolve o dinheiro numa reclamação.
- Devolução de produto não é cancelamento.
- Acima de 2,5% de vendas canceladas, a conta pode ser suspensa para vendas.

**Regras de contagem** [OFICIAL] nota oficial, ajuda/15027, ajuda/30193
- Uma venda com reclamação e depois cancelada conta só como reclamação.
- Uma venda cancelada pelo comprador nunca conta.
- Quando o comprador se arrepende, é ele quem deve pedir o cancelamento.
- A mediação conta tanto se o vendedor a abriu quanto se foi o comprador, e a reclamação que a originou conta também em "Reclamações".

**Exceções gerais** [OFICIAL] nota oficial e ajuda/866
- Envios incorretos não contam nas categorias de arte e artesanato, alianças e kits de brinquedos personalizados.
- Vendas de Imóveis não afetam a reputação.
- Em autopeças, contam as reclamações por compatibilidade informada errada.
- Com "Disponibilidade de estoque" marcada, o prazo de envio conta a partir da data que o vendedor indicou.

**Exclusão automática e contestação**
- Na API, reclamações com a tag `avoid_reputation` não contam. Para vendedor protegido, o campo `excluded` mostra os números reais [OFICIAL] developers/reputacao-de-vendedores.
- A página de reputação permite pedir revisão de reclamação, cancelamento ou atraso que o vendedor não reconhece [OFICIAL via canal] Ag1UXXB1fec.
- Terazi (set/2026) lista dez casos de exclusão analisados, entre eles reclamação aberta por engano, compra não reconhecida, arrependimento com produto perfeito, atraso dos Correios com postagem no prazo e resposta dentro de 24 h úteis. [OFICIAL via terceiro], B.
- Problema da logística do Mercado Livre (coleta ou agência) não gera penalidade, e se gerar o vendedor deve abrir chamado [OFICIAL via canal] Ag1UXXB1fec.

**Janela de 365 dias:** só o verde é oficial direto (2% / 2,5% / 13%). As faixas das outras cores vêm do Terazi (seção 4).

### 2.2 Consequências de cada nível

| Nível | Consequência | Fonte e tipo |
|---|---|---|
| Cinza (menos de 10 vendas) | Sem cor. O Decola dá verde-claro, R$ 250 em Publicidade, catálogo, Clips, Central de Promoções e Flex. | [OFICIAL] ajuda/33314 |
| Verde | Melhor posição na busca, mais chance no catálogo, ofertas exclusivas, Mercado Crédito, desconto no envio, Publicidade, dinheiro liberado antes | [OFICIAL] ajuda/21065 |
| Verde | Liberação do dinheiro em 8 dias com reputação e 12 dias sem | [OFICIAL via terceiro] Terazi, B |
| Amarelo | Perde exposição. Frete com até 40% de desconto. Ads ainda liberado (exige amarelo ou melhor, 10 vendas, 15 dias de conta e nenhuma fatura vencida). | [OFICIAL via canal] Ag1UXXB1fec; JzejZyVeauE; Hunter HUB |
| Laranja | Perde Central de Promoções, catálogo, Minha Página e Ads. Frete sem desconto. | [OFICIAL via canal, fala de consultoria parceira] Ag1UXXB1fec, B |
| Vermelho | Tudo o que o laranja perde. O canal oficial relata contas que "nunca mais" venderam. | Ag1UXXB1fec (parceira), C |
| Vermelho | Item ou vendedor vermelho fica fora da campanha de *price matching* | [OFICIAL via canal] W1hgC6snin4 (03/06/2026) |
| MercadoLíder / Gold / Platinum | Prioridade e mais visibilidade na busca (maior quanto mais alta a medalha), frete grátis com desconto, atendimento personalizado por chat, capacitações | [OFICIAL] ajuda/864, nota "como ser um MercadoLíder" |

**Divergências registradas:**
- O Terazi diz que Flex exige amarelo ou verde e que campanhas de desconto do vendedor exigem verde ([OFICIAL via terceiro], B).
- O vídeo 8dZiKLuJWXg (28/05/2026) leu na tabela oficial "desconto de até 70% por reputação". As fontes de set/out 2026 falam em até 50%. É uma faixa entre fontes, e a mais nova é a de 50%.
- "Vendedor Indicado" e Featured Offer são conceitos da Amazon e não têm equivalente oficial no ML com esse nome. No ML, o paralelo é ganhar o catálogo, que considera reputação, preço total, logística e estoque ([OFICIAL via canal] Ag1UXXB1fec; [PRÁTICA] WF333Qri_i8).

### 2.3 Reclamações, mediação e devolução

**Etapas** [OFICIAL] developers/gerenciar-reclamacoes, 20/08/2026
- `claim`: só comprador e vendedor;
- `dispute`: mediação com representante do Mercado Livre;
- `recontact`: contato depois do fechamento.

**Motivos e tipos** [OFICIAL] developers/gerenciar-reclamacoes
- PNR: produto não recebido.
- PDD: produto diferente ou defeituoso.
- CS: compra cancelada.
- Há grupos de motivos por vertical, entre eles `expiring_food` e `expiring_health`.
- A triagem por regras classifica em *repentant*, *defective*, *incomplete*, *different* e *not_working*.

**Afeta ou não a reputação** [OFICIAL] developers/gerenciar-reclamacoes
- O recurso `/affects-reputation` responde `affected`, `not_affected` ou `not_applies`, e informa `has_incentive` e `due_date`.
- No painel do vendedor existe o filtro "Isso afetará sua reputação" ([DADO] UpSeller, doc de 10/07/2024).

**Devoluções** [OFICIAL] ajuda/3285
- Prazo do comprador: 30 dias para produto novo, 5 dias para usado ou recondicionado.
- Custam ao vendedor e podem afetar a reputação: produto diferente do anunciado (modelo, cor, tamanho), com problema, incompleto ou com defeito.
- São grátis para o vendedor e não afetam: arrependimento, ou "é o que pedi, mas não serve".
- Devolução que vai para o endereço do vendedor: ele tem 3 dias úteis após receber para reportar problema, com fotos ou vídeo.

**Quando a devolução é cobrada** [OFICIAL] ajuda/32761, ajuda/28088
- É cobrada quando o motivo é responsabilidade do vendedor.
- Não é cobrada quando o dano ou a perda ocorreu no trajeto sob responsabilidade do Mercado Envios.
- No arrependimento, o frete de volta é do Mercado Livre.

**Trocas e itens faltantes**
- Há troca em moda e envio de itens faltantes ([OFICIAL via canal] EnviosCast 0yjqItQOMyI, 06/10/2026).
- No Full, a troca é feita no ponto de retirada com revisão em 3 dias úteis ([OFICIAL] ajuda/33189).

### 2.4 Experiência de compra (reputação por anúncio)

[OFICIAL] developers/experiencia-de-compra (03/02/2026), ajuda/39234, ajuda/26919

- **Pontuação e consequências:**
  - boa, de 100 a 75; abaixo de 100 com problemas já há aviso de risco de exposição;
  - média, de 74 a 50: perde exposição e pode ser pausado;
  - ruim, de 30 ou menos: pode ser cancelado ou pausado pela reputação.
- **Janela:** 180 dias. A interface mostra o texto "Em 180 dias você fez X vendas e teve Y problemas".
- **Taxonomia de causas em três níveis.** Exemplos do próprio documento:
  - PRODUCT, POOR_CONDITION, BROKEN_PRODUCT (chegou aberto ou danificado);
  - OPERATION, PACK_OFF, com quatro causas: produto não preparado, etiqueta mal impressa, sem estoque, vendedor inativo (STOP_DUE_HOLIDAY).
  - Cada causa traz um *remedy* (ação sugerida).
- **Congelamentos (*freeze*):** acordo comercial, Benefício de Reputação, verde-claro e outros. Enquanto vigoram, o item não perde exposição.
- **Catálogo:** a experiência ruim prejudica a competição no catálogo.
- **Kit:** a nota é a do produto com pior desempenho.
- **Sem histórico suficiente:** a nota é calculada pelas vendas do vendedor na mesma categoria. O texto aparece na tela em 9GJUi32R5sc ([PRÁTICA], 10/09/2026, mostra tela). Esse vendedor tinha 51 anúncios marcados, a maioria por experiência "de categoria".
- **Reputação Protegida** coloca todos os anúncios com 100 enquanto vigorar ([OFICIAL] ajuda/29276).

### 2.5 Programas de proteção

| Programa | Quem pode | Garantia | Duração | Limite | Devolução da garantia | Fonte |
|---|---|---|---|---|---|---|
| Decola | Sem cor de reputação, sem restrições | R$ 250 no Mercado Pago (conversível em R$ 250 de Publicidade) | Até 365 dias | 5 vendas afetadas | 0 afetadas: R$ 250; 1: R$ 200; 2: R$ 150; 3: R$ 100; 4: R$ 50; 5: R$ 0. Análise em 10 dias corridos. | [OFICIAL] ajuda/33314 |
| Reputação Protegida | Qualquer cor | 3% do faturamento de 60 dias (vermelho ou laranja), 2% (amarelo), 1% (verde) | Até 60 dias | Definido por conta | Proporcional. Ex.: limite 5 e 3 problemas = 60% cobrado. Análise em até 10 dias. | [OFICIAL] ajuda/29276 |
| Benefício de Reputação | Amarelo, laranja ou vermelho, mediante oferta | R$ 75 a R$ 250.000 | Até 120 dias (verde-claro mascarado) | Definido por conta (ex.: 5) | 100%, parcial ou zero | [OFICIAL via terceiro] Terazi (set/2026); [PRÁTICA] WC7JMKOXbAE (10/08/2026), B |

**Observações sobre os programas:**
- O Decola pode suspender Publicidade e Concorrência por até 5 dias após as primeiras vendas, para avaliar o desempenho ([OFICIAL] ajuda/33314). A página afirma aumento de vendas "em até 20 vezes", número sem base publicada.
- O webinar oficial de 25/05/2026 falava em Decola de 90 dias. A página atual diz 365 dias, e o Hunter (out/2026) confirma. Tratar 90 dias como superado.
- A Protegida só pode ser reativada 6 meses depois de encerrada por limite estourado ([OFICIAL via terceiro] Hunter HUB, B).

### 2.6 Atendimento e mensagens

- **Tempo de resposta às perguntas:** é uma métrica oficial (média de tempo para responder) [OFICIAL] ajuda/38071.
- **Mensagens pós-venda iniciadas pelo vendedor** [OFICIAL] developers/motivos-para-se-comunicar (28/09/2026):
  - exigem um motivo e têm cota (`cap_available`); com cota zero não dá para enviar;
  - motivos: confirmar variante, dados de faturamento, link de nota fiscal, campo livre (OTHER) e promessa de entrega (só Flex);
  - o campo livre não fica disponível depois que o status é "Entregue";
  - o comprador pode escrever a qualquer momento.
- **Limite de 350 caracteres** na primeira mensagem ativa, a ser usada para trocar variação sem estoque e evitar cancelamento [OFICIAL via canal] Ag1UXXB1fec.
- **Modo férias:** pausa todos os anúncios, exceto os com estoque no Full. Mudar o estoque pode reativar anúncios [OFICIAL] ajuda/32434.
- **Opiniões:** a opinião sobre o vendedor é opcional, aparece no perfil e não afeta a reputação [OFICIAL] ajuda/15040 e ajuda/851.
- **Opiniões de produto (API):** a API de reviews traz os campos `coupon_redeemed`, `earned_rewards` e `has_pdd` [OFICIAL] developers/opinioes-sobre-um-produto (18/08/2026). Isso indica que a própria plataforma registra incentivos dados por ela e se houve reclamação PDD.

---

## 3. O que os melhores fazem

### Práticas com consenso (duas fontes ou mais)

- **P1. Página de reputação todo dia, olhando a tendência e a saída de vendas antigas da janela.** [PRÁTICA] Ag1UXXB1fec (agência parceira Digital Growth, 25/05/2026); HRmtJMCZdZw (Graboski, 23/06/2026, tela, R$ 536 mil em 60 dias, revenda). B.
- **P2. Margem de segurança de ~50% do limite:** alerta com reclamações em 0,5% (limite Líder 1%); com cancelamentos em 0,25% (limite 0,5%) para de cancelar até a janela andar 10 a 15 dias. [PRÁTICA] HRmtJMCZdZw. C.
- **P3. Atrasar em vez de cancelar**, pois o limite de atraso (6% a 13%) é 4 a 12 vezes o de cancelamento. [PRÁTICA] HRmtJMCZdZw; [OFICIAL via canal] Ag1UXXB1fec. A.
- **P4. Oferecer variação ou alternativa pela mensagem ativa antes de cancelar.** Ag1UXXB1fec; nota oficial de reputação. A.
- **P5. Resolver em menos de 24 a 48 h, antes da mediação, assumindo o erro** (reembolso, devolução ou reenvio, sem culpar o transporte). has_incentive; Ag1UXXB1fec; 0yjqItQOMyI. A.
- **P6. Corrigir a causa no anúncio:** ficha técnica completa, fotos fiéis (cuidado com foto de IA "ideal"), imagens de quebra de objeção nas posições 2 e 3, clips, medidas e voltagem. A maior parte das reclamações vem de produto diferente, quebrado ou faltando. [OFICIAL via canal] 0yjqItQOMyI (06/10/2026); Ag1UXXB1fec; [PRÁTICA] QANPOYRNZsI (07/08/2026). A.
- **P7. Controle de qualidade do lote:** Gabriel (Crowley, 95% eletrônicos) testa 100% dos itens e mantém 2 pessoas de pós-venda inclusive nos fins de semana; Diego Rosa cita um vendedor de smartwatch que testava cada unidade e trocava lotes ruins. Causa mais comum de excesso de devolução: lote ruim comprado por 5% a 10% de desconto. [PRÁTICA] 0yjqItQOMyI, SFvw5IWL4_Y, sem números auditados. B. Típico de [REVENDA/IMPORTAÇÃO].
- **P8. Estoque sincronizado, pausa do que acabou, Modo férias e Disponibilidade de estoque.** ajuda/5205, 32434; Ag1UXXB1fec. A.
- **P9. Despacho no mesmo dia e checagem diária do horário de corte** (muda com a rota). Ag1UXXB1fec; ajuda/21114. A.
- **P10. Perguntas respondidas rápido (canal oficial cita até 12 h), da mais antiga para a mais nova, com assistente ou integrador.** Líderes usam Gobots também para relatórios de perguntas e reclamações frequentes que alimentam o cadastro: fábrica de colchões (JRx32XZkgQA, 08/10/2026, [MARCA]) e QtE-2WsUOt8. B.
- **P11. Devolução como dado:** ler motivos por anúncio e reescrever a descrição. 0yjqItQOMyI; QANPOYRNZsI (sem antes e depois). B.

### Divergências entre fontes

**D1. Taxa de devolução "saudável".**
- Diego Rosa: cerca de 2% no máximo, para eletrônicos, a partir da margem líquida.
- No mesmo episódio ele diz que não existe padrão e que o *benchmark* deve ser o histórico do próprio produto.
- O Mercado Livre diz que a taxa saudável é "a menor possível" e não publica *benchmark* (0yjqItQOMyI).
- Resultado: sem número oficial; registrar como faixa "não publicada".

**D2. Efeito da medalha.**
- Oficial: mais exposição.
- O Écomm Vitor ([PRÁTICA] 6hPsDJ-D7oM, 01/07/2026, R$ 40 mil por mês) diz não ter visto diferença em vendas, cliques ou impressões.
- Nenhum dos lados apresenta holdout. Fica como hipótese aberta.

**D3. Mediação e IA.**
- O Graboski diz que quase não há mediação porque a IA resolve antes.
- O Bruno Gontijo diz que a IA decide a favor do comprador e que só há "duas chances" (pedido e uma recorrência) para reverter. Ele atribui a informação a outra criadora (N7).
- A própria plataforma admite que a IA de pós-venda está "em melhoria" e orienta abrir chamado pedindo revisão (Ag1UXXB1fec).

**D4. Estoque compartilhado no Full.**
- O Mercado Livre diz que problema de produto de outro vendedor não afeta o vendedor ([OFICIAL via praticante, tela] SFvw5IWL4_Y).
- Diego Rosa aponta custo indireto: devoluções que não ocorreriam.

**D5. Uso de IA para contestar.** O Bruno Gontijo distribui um GPT para montar defesas (9GJUi32R5sc). É uma tática de praticante sem taxa de sucesso medida. Sinais fracos: CTA, promessa implícita, links de afiliado. Rebaixada para C.

---

## 4. Números de referência

**Limites e regras da plataforma**

| Métrica | Valor | Fonte | Data | Tipo |
|---|---|---|---|---|
| Vendas para ter reputação | 10 concluídas em 365 dias | ajuda/866 | lida em 14/10/2026 | OFICIAL |
| Corte de janela 60 ou 365 dias | 101 vendas concluídas em 60 dias | ajuda/866; nota oficial | vigente desde 10/09/2026 | OFICIAL |
| Reclamações, verde | ≤ 2% (60 e 365 dias) | nota oficial | lida em 14/10/2026 | OFICIAL |
| Reclamações, amarelo / laranja / vermelho (60 dias) | ≤ 4,5% / ≤ 8% / > 8% | developers/reputacao | 11/08/2025 (pode estar superada) | OFICIAL; confirmado por Hunter (out/2026) |
| Canceladas por você, verde | ≤ 1,5% (60 dias); ≤ 2,5% (365 dias) | nota oficial | lida em 14/10/2026 | OFICIAL |
| Cancelamentos, amarelo / laranja / vermelho (60 dias) | ≤ 3,5% / ≤ 4% / > 4% | developers/reputacao | 11/08/2025 | OFICIAL |
| Envios incorretos, verde | ≤ 10% (60 dias); ≤ 13% (365 dias) | nota oficial | lida em 14/10/2026 | OFICIAL |
| Envios, amarelo / laranja / vermelho (60 dias) | ≤ 18% / ≤ 22% / > 22% | developers/reputacao | 11/08/2025 | OFICIAL |
| Faixas de 365 dias (amarelo, laranja, vermelho) | cancelamentos 5,5 / 6,5 / > 6,5%; envios 23,5 / 28,5 / > 28,5% | Terazi | 16 a 20/09/2026 | OFICIAL via terceiro (B) |
| MercadoLíder: reclamações / mediações / cancelamentos / envios | < 1% / < 0,5% / < 0,5% / < 6% | ajuda/864 | lida em 14/10/2026 | OFICIAL |
| MercadoLíder (vendas; faturamento) | 230 e R$ 37 mil; Gold 575 e R$ 118,4 mil; Platinum 1.725 e R$ 296 mil (3 meses mais o mês corrente) | ajuda/864 | lida em 14/10/2026 | OFICIAL |
| Suspensão por cancelamento | > 2,5% das vendas | ajuda/5205 | s/d (pode estar superada) | OFICIAL |
| Janela de resposta com incentivo | 48 h | developers/gerenciar-reclamacoes | 20/08/2026 | OFICIAL |
| Prazo de devolução do comprador | 30 dias (novo); 5 dias (usado ou recondicionado); vendedor reporta problema em 3 dias úteis | ajuda/3285 | lida em 14/10/2026 | OFICIAL |
| Triagem de devolução no Full | 3 dias úteis; retirada de não aptos em 20 dias corridos (ajuda/19200), descarte com custo após 30 dias (ajuda/3285); contestação em 60 dias corridos (19200) ou 60 dias úteis (3285) | ajuda/19200, ajuda/3285 | lida em 14/10/2026 | OFICIAL, com divergência interna |
| Desconto de frete por cor | verde até 50%; amarelo até 40%; laranja e vermelho 0% | Hunter HUB; Terazi | out/2026; set/2026 | OFICIAL via terceiro (A: duas fontes) |
| Desconto de frete por cor (leitura anterior) | "até 70% por reputação" | 8dZiKLuJWXg | 28/05/2026 | OFICIAL via praticante (C; pode estar superada) |
| Full: desconto no frete grátis | 50% a partir de R$ 79 | ajuda/5171 | s/d (pode estar superada) | OFICIAL |
| Product Ads: requisitos | amarelo ou melhor, ≥ 10 vendas, ≥ 15 dias de conta, sem fatura vencida | JzejZyVeauE (webinar oficial) | 21/05/2026 | OFICIAL via canal |

Experiência de compra, Decola, Reputação Protegida e Benefício de Reputação: números nas seções 2.4 e 2.5.

**Contas de margem de segurança (derivadas dos limites oficiais)**
- No limiar de 101 vendas em 60 dias: 2 reclamações mantêm o verde (1,98%) e a 3ª leva ao amarelo (2,97%). Com cancelamentos, 1 venda = 0,99%; a 2ª = 1,98% (amarelo).
- No Platinum mínimo (1.725 vendas): cabem 17 reclamações, 8 mediações, 8 cancelamentos e 103 atrasos.
- Na janela de 365 dias com 300 vendas: cabem 6 reclamações, 7 cancelamentos e 39 envios incorretos.
- Com 10 vendas, um único problema vale 10%, o que explica o "colchão" dos programas Decola e Protegida (HRmtJMCZdZw; Hunter HUB).

**Benchmarks de praticantes e dados (não oficiais)**

| Métrica | Valor | Fonte | Data | Tipo e confiança |
|---|---|---|---|---|
| Alerta interno de reclamações | 50% do limite (0,5% contra 1%) | HRmtJMCZdZw | 23/06/2026 | PRÁTICA, C |
| Devolução "saudável" em eletrônicos | ~2% máx., ou o histórico do próprio produto | 0yjqItQOMyI (Diego Rosa) | 06/10/2026 | PRÁTICA, C |
| Arrependimento como parte das devoluções | "1 a 2%" das reclamações e devoluções (fala do Mercado Livre, sem base) | 0yjqItQOMyI | 06/10/2026 | OFICIAL via canal, sem método, C |
| Anúncios com experiência média ou ruim | de ~200 para 51 anúncios em poucos dias, numa conta | 9GJUi32R5sc | 10/09/2026 | PRÁTICA com tela, C |
| Enquete sobre problema de experiência de compra | "meio a meio" (enquete informal) contra 15 em 1.000 mentorados (1,5%) | 9GJUi32R5sc | 10/09/2026 | N8, só levanta pergunta |
| Base declarada pela ferramenta | 13 mil sellers e R$ 7 bi analisados (autorreportado) | Hunter HUB | 14/10/2026 | DADO, método não publicado |

Não há *benchmark* público de taxa de reclamação, devolução ou tempo de resposta por categoria no ML Brasil.

---

## 5. Alimentos, perecíveis e marca própria ou indústria

- **Motivos de reclamação próprios.** A API tem os grupos `expiring_food` e `expiring_health` [OFICIAL] developers/gerenciar-reclamacoes (20/08/2026). Isso indica um fluxo específico para validade, mas a página de ajuda com prazos de devolução de alimentos não foi encontrada.
  - A regra geral (30 dias para produto novo) é a única oficial lida.
  - O prazo de "12 dias para alimentos" citado em blog não foi confirmado e é tratado como mito até prova.
- **Embalagem é o vetor de reclamação mais controlável.**
  - "Chegou aberto ou danificado" (BROKEN_PRODUCT) é causa de experiência de compra média.
  - O Mercado Livre lembra que no Full o despacho é dele, mas o cuidado com o produto é do vendedor ([OFICIAL via canal] 0yjqItQOMyI).
  - Para vidro e frágeis, a orientação é plástico-bolha e caixa (Ag1UXXB1fec).
  - Pela regra oficial, pacote avariado não afeta a reputação, mas produto com problema de qualidade afeta (ajuda/30193).
- **Triagem do Full e alimento aberto.** Na triagem, caixa original aberta leva o produto a "disponível para retirada", com descarte cobrado após 30 dias (ajuda/3285). Em alimento, devolução por arrependimento tende a virar perda física, mesmo sem afetar a reputação. É uma inferência a partir da regra; não há dado.
- **Validade e lote.** A causa mais comum de excesso de devolução apontada pela consultoria é o lote (0yjqItQOMyI). Na indústria, isso se traduz em rastrear lote e validade e conferir a validade mínima antes de enviar ao Full. É uma inferência de método e não há fonte específica de alimentos.
- **Marca própria ou indústria e catálogo.** Na observação de 14/10/2026 ([OBS] lideres.md):
  - nota, avaliações e "vendidos" pertencem ao produto de catálogo, não ao vendedor;
  - os líderes de café (Italle, Orfeu, Healthy Coffee) são MercadoLíder Platinum e Appassionato é Gold;
  - as notas vão de 4,7 a 4,9 com milhares de opiniões (Italle, 6.703).
  - Por isso a dona da marca colhe as avaliações acumuladas do produto, enquanto o revendedor depende da reputação da conta para ganhar o catálogo.
- **Kits.** Kits (café com moedor, multipacks) herdam a pior experiência entre os produtos (ajuda/39234). Um item problemático contamina o kit.
- **Supermercado.** Nas lojas de supermercado, o frete grátis depende de um carrinho mínimo variável ([OFICIAL] ajuda/15948). As regras de reputação são as mesmas; não foi achada exceção para alimentos.
- **Prazo de produção.** Produto com prazo de fabricação (35 dias, no exemplo do webinar) tem travas, como Ads. A "Disponibilidade de estoque" desloca a contagem de atraso (Ag1UXXB1fec; ajuda/866). Pode valer para torra sob demanda; não há fonte específica de café.

---

## 6. Erros comuns e mitos

| Mito ou afirmação fraca | O que dizem as fontes fortes | Fontes |
|---|---|---|
| "Corte de 60 vendas para a janela de 60 dias" | Desde 10/09/2026 o corte é 101; o 60 é da documentação de 2025 | ajuda/866 contra developers (2025), Nubimetrics |
| "Agora o mínimo é 68 vendas" | Nenhuma fonte oficial confirma; o oficial diz 101 | i9MQ51OkODg (canal de 1 min, sem tela) |
| "Verde = reclamações < 3% e atrasos < 15%" | São números da página antiga "Mudanças na reputação" (ajuda/4421, superada); hoje são 2% e 10% ou 13% | Bling (30/09/2025); Nubimetrics |
| "Janela de 3 meses ou 60 vendas, o que vier primeiro" e "atraso só conta acima de 3%" | Sem amparo oficial | Bling |
| "MercadoLíder com 60/150/450 vendas e R$ 36,5k/125k/320k" | O oficial é 230/575/1.725 e R$ 37k/118,4k/296k | ui2Gh2u_xDI (24/09/2026, aula com CTA) contra ajuda/864 |
| "Peça avaliação oferecendo cupom ou desconto" | Não foi achado texto oficial que permita. A API marca cupom e recompensa nas reviews, e o campo livre some depois da entrega. O webinar oficial veta "brinde" como isca no anúncio. Prática de risco, sem base | Bling contra developers e Ag1UXXB1fec |
| Copiar depoimentos de outra plataforma para as imagens | Chamado de "fake" no próprio vídeo; não é avaliação do ML | tNqmJiXsjDA |
| "Bateu 30% você não vende mais nada" | Confusão de métrica: 30 é a nota da experiência de compra ruim (≤ 30 em 100), não um percentual de reclamações | SFvw5IWL4_Y contra ajuda/39234 |
| "Mediação conta para todos" | Só conta para MercadoLíder; a reclamação de origem conta para todos | HRmtJMCZdZw contra ajuda/30193 e ajuda/20245 |
| "Opinião negativa derruba a reputação" | Opiniões não afetam a reputação (podem afetar conversão e catálogo) | ajuda/15040, ajuda/851 |
| "Do vermelho ao verde em 1 dia" | É o verde-claro mascarado de um programa pago; a cor real continua sendo calculada | WC7JMKOXbAE (título com promessa) contra ajuda/29276 |
| "Decola dura 90 dias" | A página atual diz até 365 dias | Ag1UXXB1fec (mai/2026) contra ajuda/33314 e Hunter (out/2026) |
| "Toda devolução derruba a reputação" | Arrependimento e "não serve" não afetam nem custam frete ao vendedor | ajuda/3285, ajuda/28088 |
| "Algoritmo ama avaliações recentes" (com peso) | Afirmação sem base nem teste. O ML não publica o peso da reputação ou das avaliações no ranking | D21_ErqP09E (N7) contra Hunter HUB ("não publica o peso") |
| "Com o Decola, os vendedores aumentam as vendas em até 20x" | Número oficial sem base nem período. Sinal fraco 2 | ajuda/33314 |

---

## 7. Revenda e importação x indústria e marca própria

| Tema | [REVENDA] revenda, dropshipping, importação | [MARCA] indústria, marca própria | Ambos |
|---|---|---|---|
| Fonte principal de reclamação | Lote e fornecedor variável; produto "esteticamente igual" de qualidade inferior (0yjqItQOMyI) | Descrição, embalagem e consistência de lote de produção | Produto diferente do anunciado, quebrado ou faltando |
| Controle de qualidade | Teste de 100% e troca de lote com o fornecedor (Gabriel, Diego Rosa) | Controle na origem; rastreio de lote | Checagem dupla antes do despacho (Ag1UXXB1fec) |
| Avaliações | Em catálogo de marca alheia, o revendedor não controla título, fotos nem avaliações; disputa o catálogo por preço total, reputação e logística (lideres.md; WF333Qri_i8) | A marca acumula as avaliações do produto de catálogo e a experiência de compra dos próprios anúncios | Opiniões sobre o vendedor não afetam a reputação |
| Dropshipping ou sem estoque | Risco maior de cancelamento (limite verde 1,5%) e atraso. Praticante sem estoque usa a margem de cancelamento ao limite (HRmtJMCZdZw) | Não se aplica | Atrasar é menos custoso que cancelar |
| Full e estoque compartilhado | Exige verde; problema de produto de outro vendedor não afeta, mas pode gerar devolução (SFvw5IWL4_Y) | Full reduz o envio incorreto; triagem de 3 dias úteis | Qualidade do produto continua sendo do vendedor |
| Uso dos programas | Decola e Protegida como "colchão" em contas novas ou em recuperação | Contas novas de marca também começam cinza, sem exceção por CNPJ (ui2Gh2u_xDI, N7) | — |
| Prazo de produção | — | Produto sob encomenda tem travas (Ads); usar Disponibilidade de estoque | — |

---

## 8. Tabela de afirmações

| id | afirmação | tipo | fonte | data | confiança | rev/marca | pode estar superada? |
|---|---|---|---|---|---|---|---|
| A1 | Reputação só começa com 10 vendas concluídas em 365 dias | OFICIAL | ajuda/866; nota oficial | lida em 14/10/2026 | alta | ambos | não |
| A2 | Corte de 101 vendas em 60 dias define a janela de 60 ou 365 dias | OFICIAL | ajuda/866; 6QFwvsIPSkQ; Terazi | 10/09/2026 | alta | ambos | não |
| A3 | Verde: reclamações ≤ 2%, cancelamentos ≤ 1,5% (60d) ou 2,5% (365d), envios ≤ 10% (60d) ou 13% (365d) | OFICIAL | nota oficial "por que a reputação é importante" | lida em 14/10/2026 | alta | ambos | não |
| A4 | Escala de 60 dias: reclamações 4,5 / 8%, cancelamentos 3,5 / 4%, atraso 18 / 22% (amarelo / laranja) | OFICIAL | developers/reputacao | 11/08/2025 | alta (confirmada por Hunter e Terazi) | ambos | sim (data) |
| A5 | MercadoLíder: < 1% reclamações, < 0,5% mediações, < 0,5% cancelamentos, < 6% envios | OFICIAL | ajuda/864 | lida em 14/10/2026 | alta | ambos | não |
| A6 | Medalhas: 230 / 575 / 1.725 vendas e R$ 37k / 118,4k / 296k em 3 meses mais o mês corrente | OFICIAL | ajuda/864; nota MercadoLíder | lida em 14/10/2026 | alta | ambos | não |
| A7 | Mediação só entra no cálculo de MercadoLíder | OFICIAL | ajuda/30193; ajuda/20245 | lida em 14/10/2026 | alta | ambos | não |
| A8 | Só reclamações de produto incompleto, faltante ou com problema de qualidade afetam; pacote aberto ou avariado não | OFICIAL | ajuda/30193 | lida em 14/10/2026 | média (fonte única) | ambos | s/d |
| A9 | Reclamação por arrependimento e venda cancelada pelo comprador não contam | OFICIAL | nota oficial; ajuda/15027 | lida em 14/10/2026 | alta | ambos | não |
| A10 | Mais de 2,5% de vendas canceladas pode suspender a conta | OFICIAL | ajuda/5205 | s/d | média | ambos | sim (sem data) |
| A11 | Resposta satisfatória em 48 h com `has_incentive` não afeta a reputação | OFICIAL | developers/gerenciar-reclamacoes | 20/08/2026 | alta | ambos | não |
| A12 | Envio incorreto inclui atraso, depósito errado e falhas do Flex depois das 21 h | OFICIAL | ajuda/30193; nota oficial | lida em 14/10/2026 | alta | ambos | não |
| A14 | Verde dá melhor busca, catálogo, ofertas exclusivas, Publicidade, desconto de envio e dinheiro mais rápido | OFICIAL | ajuda/21065 | lida em 14/10/2026 | alta | ambos | não |
| A15 | Desconto de frete: verde até 50%, amarelo até 40%, laranja e vermelho 0% | OFICIAL via terceiro | Hunter HUB; Terazi | out/2026; set/2026 | alta | ambos | não |
| A16 | Product Ads exige amarelo ou melhor, 10 vendas, 15 dias de conta e nenhuma fatura vencida | OFICIAL via canal | JzejZyVeauE | 21/05/2026 | média | ambos | não |
| A17 | Laranja perde Central de Promoções, catálogo, Minha Página e Ads | OFICIAL via canal (parceira) | Ag1UXXB1fec | 25/05/2026 | média | ambos | não |
| A18 | Experiência de compra: boa 100–75, média 74–50, ruim ≤ 30; 180 dias; pausa ou cancelamento | OFICIAL | ajuda/39234; developers | 03/02/2026 | alta | ambos | não |
| A19 | Kit herda a pior experiência de compra entre seus produtos | OFICIAL | ajuda/39234 | lida em 14/10/2026 | alta | marca | não |
| A20 | Sem dados suficientes, a experiência do item é calculada pela categoria | PRÁTICA (tela) | 9GJUi32R5sc | 10/09/2026 | média | ambos | não |
| A21 | Decola: R$ 250, até 365 dias, 5 vendas afetadas, R$ 50 devolvidos a menos por afetada | OFICIAL | ajuda/33314 | lida em 14/10/2026 | alta | ambos | não |
| A22 | Reputação Protegida: 1% a 3% do faturamento de 60 dias, até 60 dias, devolução proporcional | OFICIAL | ajuda/29276 | lida em 14/10/2026 | alta | ambos | não |
| A23 | Benefício de Reputação: R$ 75 a R$ 250 mil, até 120 dias | OFICIAL via terceiro | Terazi; WC7JMKOXbAE | set/2026; ago/2026 | média | ambos | não |
| A24 | Devolução: 30 dias (novo) e 5 dias (usado); o motivo define custo e impacto | OFICIAL | ajuda/3285 | lida em 14/10/2026 | alta | ambos | não |
| A25 | Arrependimento: frete de devolução pago pelo Mercado Livre; defeito: pelo vendedor | OFICIAL | ajuda/28088; ajuda/32761 | lida em 14/10/2026 | alta | ambos | não |
| A26 | Triagem de devoluções no Full em 3 dias úteis, com 4 destinos possíveis | OFICIAL | ajuda/19200; ajuda/3285 | lida em 14/10/2026 | alta | ambos | não |
| A27 | Full: o Mercado Livre responde reclamações de entrega e produto entregue; 50% de desconto no frete grátis ≥ R$ 79 | OFICIAL | ajuda/5171 | s/d | média | ambos | sim (sem data) |
| A28 | Opiniões não afetam a reputação | OFICIAL | ajuda/15040; ajuda/851 | lida em 14/10/2026 | alta | ambos | não |
| A29 | O campo livre de mensagem ao comprador fica indisponível depois da entrega; mensagens exigem motivo e cota | OFICIAL | developers/motivos-para-se-comunicar | 28/09/2026 | alta | ambos | não |
| A32 | Atraso da logística do Mercado Livre (coleta, agência, Flex comum) não penaliza; Flex Turbo é responsabilidade do vendedor | OFICIAL via canal | Ag1UXXB1fec | 25/05/2026 | média | ambos | não |
| A33 | Grupos de motivo `expiring_food` e `expiring_health` existem na API de reclamações | OFICIAL | developers/gerenciar-reclamacoes | 20/08/2026 | alta | marca | não |
| A34 | Alerta interno a 50% do limite de reclamação; parar de cancelar a 50% do limite | PRÁTICA (tela) | HRmtJMCZdZw | 23/06/2026 | baixa | revenda | não |
| A35 | Preferir atrasar a cancelar | PRÁTICA + OFICIAL via canal | HRmtJMCZdZw; Ag1UXXB1fec | jun–mai/2026 | alta | ambos | não |
| A36 | Testar 100% dos produtos e manter pós-venda 7 dias por semana reduz devoluções | PRÁTICA | 0yjqItQOMyI (Crowley) | 06/10/2026 | baixa | revenda | não |
| A37 | Devolução saudável ~2% em eletrônicos (ou histórico próprio) | PRÁTICA | 0yjqItQOMyI (Diego Rosa) | 06/10/2026 | baixa | revenda | não |
| A38 | Medalha não mudou vendas, cliques nem impressões | PRÁTICA (relato) | 6hPsDJ-D7oM | 01/07/2026 | baixa | revenda | não |
| A39 | Líderes de café são MercadoLíder Platinum ou Gold, com nota de 4,7 a 4,9 | OBS | observacao/lideres.md | 14/10/2026 | média | marca | não |
| A40 | Avaliações de catálogo pertencem ao produto, não ao vendedor | OBS | observacao/lideres.md | 14/10/2026 | média | ambos | não |
| A41 | Página antiga de limites (3% / 7% / 12% de reclamações; 15% / 20% de atraso) foi superada | OFICIAL (histórico) | ajuda/4421 | s/d | alta | ambos | sim |

---

## 9. Lacunas

1. **Shopee e Amazon:** sem evidência oficial nesta nota (Seller Central BR e Shopee Seller Education Hub não renderizaram sem login; orçamento de busca esgotado). Ficam em aberto: Account Health Rating e ODR, Featured Offer e efeito do FBA, pontos de penalidade e selos da Shopee, motivos de devolução no POE. O paralelo do POE no ML é a taxonomia de três níveis da Experiência de compra e o grupo "arrependimento" das métricas (ajuda/20241).
2. **Faixas de 365 dias** para amarelo, laranja e vermelho: só via Terazi. Não foi achada página oficial com essa tabela.
3. **Benefício de Reputação:** a página oficial (mercadolivre.com.br/reputacao/beneficio_reputacao) exige login. Os valores (R$ 75 a R$ 250 mil, 120 dias) vêm de terceiros. Também não ficou claro se o Benefício e a Reputação Protegida coexistem ou se um substituiu o outro.
4. **Peso da reputação e das opiniões no ranqueamento:** não é publicado. Não há teste de pausa ou holdout público sobre o efeito da medalha.
5. **Taxa de reclamação, devolução e tempo de resposta por categoria:** não há *benchmark* público no ML Brasil, nem estudo com metodologia (NIQ Ebit, Neotrust) lido nesta rodada.
6. **Alimentos:** não foi achada página oficial com prazo de devolução específico de alimentos ou perecíveis. Também não há regra pública sobre validade mínima na entrada do Full nesta frente.
7. **Contestação:** não há página oficial com o número de recursos permitidos. As "duas chances" vêm de N7.
8. **Avaliações incentivadas:** não foi achado texto oficial explícito sobre incentivo dado pelo vendedor em troca de avaliação. Só há evidência indireta (campos da API, regra de mensagens, veto a "brinde" como isca).
9. **Desconto de frete por cor:** 50% (set/out 2026) contra 70% (mai/2026). Não foi possível ler a tabela oficial de custos nesta frente.
10. **Divergências internas da Central de Ajuda sobre o Full:**
    - retirada de devoluções não aptas em 20 ou 30 dias;
    - contestação em 60 dias corridos ou úteis.
11. **Data das páginas de ajuda:** não há data publicada. Cada regra deve ser revalidada na conta antes de virar número de planejamento.


## 10. Verificação (2026-10-14)

Método: leitura direta (HTTP) das páginas oficiais em 14/10/2026. As páginas da Central de ajuda e da Central de aprendizagem não trazem data publicada; todas as regras abaixo valem "como lidas em 14/10/2026" e devem ser revalidadas na conta. A busca web estava sem orçamento, então não foi possível procurar a camada de YouTube oficial, releases e cartas a investidores. O que não veio de página oficial lida fica como SEM FONTE OFICIAL. Tipo de todas as fontes abaixo: [OFICIAL].

| id | veredito | fonte oficial (URL) | observação |
|---|---|---|---|
| A2 | CONFIRMADA (regra); SEM FONTE OFICIAL (data e corte anterior) | https://www.mercadolivre.com.br/ajuda/866 ; https://vendedores.mercadolivre.com.br/nota/por-que-a-reputacao-do-vendedor-e-importante | As duas páginas dizem: 101 ou mais vendas concluídas nos últimos 60 dias, janela de 60 dias; menos de 101, janela de 365 dias. Nenhuma traz a data de vigência (10/09/2026) nem cita o corte anterior. O corte de 60 vendas aparece na página de desenvolvedores (ver A4), o que é coerente com a mudança, mas não a data. Reputação só começa após 10 vendas concluídas (ajuda/866). |
| A3 | CONFIRMADA | https://vendedores.mercadolivre.com.br/nota/por-que-a-reputacao-do-vendedor-e-importante | Para ser verde: reclamações até 2% (MercadoLíder até 1%); canceladas por você até 1,5% (60 dias) e 2,5% (365 dias), MercadoLíder até 0,5%; envios incorretos até 10% (60 dias) e 13% (365 dias), MercadoLíder até 6%. Reclamação de arrependimento não conta. Venda com reclamação e cancelamento depois conta só como reclamação. |
| A4 | CONFIRMADA (números); vigência incerta, pode estar superada | https://developers.mercadolivre.com.br/pt_br/reputacao-de-vendedores | A tabela MLB (Líder / verde / amarelo / laranja / vermelho acima) bate: reclamações 1 / 2 / 4,5 / 8% (> 8%); cancelamentos 0,5 / 1,5 / 3,5 / 4% (> 4%); atraso (delayed handling time) 6 / 10 / 18 / 22% (> 22%). A página não tem data e ainda traz o corte antigo de 60 vendas para o MLB (hoje 101 na ajuda/866), então não está totalmente atualizada. Os valores de verde e Líder coincidem com a ajuda/866 e a ajuda/864. A tabela da API também trata o atraso só para quem usa Mercado Envios com 10 ou mais envios. |
| A5-A6 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/864 | Janela: 3 meses mais os dias do mês vigente. Vendas concretizadas: 230+, 575+, 1.725+. Faturamento: R$ 37.000+, R$ 118.400+, R$ 296.000+ (Líder, Gold, Platinum). Reclamações < 1%, mediadas < 0,5%, canceladas < 0,5%, envios incorretos < 6%. Exige ainda cadastro de mais de 4 meses, documentação, comprovação fiscal e termômetro verde escuro. Faturamento não considera anúncios Grátis. |
| A8 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/30193 | Só afetam reclamações de produto incompleto ou com itens em falta e as de qualidade (defeito, fabricação, não funciona). Pacote aberto ou avariado não impacta. A página também lista Mediações (só para MercadoLíder) e define envio incorreto (despacho atrasado, depósito errado, regras do Flex após 21 h). |
| A10 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/5205 | Texto: se mais de 2,5% das vendas forem canceladas, a conta "poderá ser suspensa para vendas". É possibilidade, não automatismo. Devolução de produto não conta como venda cancelada. Cancelamento por problema dos Correios ou da transportadora não prejudica. |
| A11 | CONFIRMADA | https://developers.mercadolivre.com.br/pt_br/gerenciar-reclamacoes | Campo has_incentive: com true, se o vendedor responder satisfatoriamente nas primeiras 48 h, não afeta a reputação. Com false, o vendedor tem as mesmas 48 h, mas o efeito na reputação não é garantido. A página não mostra data legível; a data 20/08/2026 não foi checada. |
| A15 | SEM FONTE OFICIAL | (nenhuma lida) https://www.mercadolivre.com.br/landing/custos-de-venda pede login | A página de custos exigiu login e não foi achada página pública da Central de ajuda com a tabela de desconto de frete por cor. Os valores (50% verde, 40% amarelo, 0% laranja e vermelho; 70% em maio/2026) seguem só de praticantes. Não use como número de planejamento. |
| A16 | CONTESTADA (parcial) | Central de aprendizagem do Mercado Livre, URL exata não registrada (artigo "Quais requisitos preciso cumprir para criar campanhas de Aumentar Vendas com Product Ads?"; lido em 14/10/2026, sem data) | O artigo oficial exige: conta ativa, reputação mínima amarela, sem verificação de pagamento pendente, sem dívidas, sem restrição por falsificação, pelo menos um anúncio ativo no catálogo e país com Publicidade. Não cita "15 dias de conta" nem "10 vendas" como requisito próprio (só diz que a reputação é calculada a partir de 10 vendas, então sem 10 vendas não há cor). Acrescenta o requisito de anúncio ativo no catálogo. Quem está no Programa Decola ativo fica dispensado do requisito de reputação e vendas. Localizar o artigo pelo título para citar a URL. |
| A18 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/39234 ; https://developers.mercadolivre.com.br/pt_br/experiencia-de-compra | Faixas: boa 100-75, média 74-50, ruim 30 ou menos. A faixa de 31 a 49 não é descrita na página. Média: perde exposição e pode ser pausado; ruim: pode ser cancelado. Em kit vale o produto de pior desempenho. A documentação de desenvolvedores cita janela de 180 dias para o cálculo e a contagem de vendas do anúncio. Reputação Protegida e Benefício de Reputação levam a experiência a 100 durante a proteção. |
| A21-A22 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/33314 ; https://www.mercadolivre.com.br/ajuda/29276 | Decola: R$ 250 em garantia, até 365 dias, máximo de 5 vendas afetadas (reclamação, cancelamento por você, envio incorreto); devolução de R$ 250 / 200 / 150 / 100 / 50 / 0 para 0 a 5 afetadas, após revisão de 10 dias corridos. Exige não ter cor de reputação. Reputação Protegida: garantia de 3% (vermelho ou laranja), 2% (amarelo) ou 1% (verde) do faturamento dos últimos 60 dias, ativa por no máximo 60 dias, com limite de vendas com problema; excedido o limite perde-se 100% da garantia. |
| A24-A25 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/3285 ; https://www.mercadolivre.com.br/ajuda/28088 ; https://www.mercadolivre.com.br/ajuda/32761 | Prazo para devolver: produto novo até 30 dias após o recebimento; usado ou recondicionado até 5 dias. Arrependimento ou "não serve": grátis para o vendedor e sem impacto na reputação. Produto diferente do anunciado, com problema, incompleto ou com defeito: tem custo para o vendedor e pode afetar a reputação. A ajuda/28088 confirma o frete de volta por conta do Mercado Livre no arrependimento. A ajuda/32761 diz que o valor do produto é cobrado do vendedor quando o motivo foi de responsabilidade dele (exceto dano ou perda no trajeto sob responsabilidade do Mercado Livre). |

Resumo: 10 confirmadas (A2 com ressalva de data), 1 contestada (A16), 1 sem fonte oficial (A15). Ressalvas gerais: (a) a página de desenvolvedores de reputação (A4) está desatualizada no corte de vendas; use a ajuda/866 como regra e a tabela de cores só como referência; (b) nenhuma página lida traz data, então a marca "pode estar superada" vale para tudo que for tarifa, frete e Ads.

## 11. Verificação pelo navegador (2026-10-15)

| id | veredito | fonte oficial | observação |
|---|---|---|---|
| A15 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/custos-envio-reputacao-verde-mercado-lider_40538 ; https://www.mercadolivre.com.br/ajuda/40545 ; https://www.mercadolivre.com.br/ajuda/40547 | Índice /ajuda/40525 traz três tabelas: verde/MercadoLíder/sem reputação (até 50%), amarela (até 40%) e laranja ou vermelha (sem seção de desconto; até 0,3 kg a partir de R$79 = R$25,90, o dobro dos R$12,95 do verde). Os 70% citados por praticantes não aparecem. |

## 12. Rodada 2 e estado final (2026-10-15)

Método: só leitura dos arquivos da verificação (seções 10 e 11, `verificacao/resultado-mercadolivre.tsv`), de LACUNAS §1.6, §1.9 e §4 e dos arquivos de `mercadolivre/rodada2/`. Não houve navegador, coleta nova nem WebFetch: nenhum ponto exigiu desempate externo. As páginas oficiais citadas continuam sem data publicada. Os valores valem "como lidos em 14 e 15/10/2026" e devem ser revalidados na conta antes de virar número de planejamento.

### 12.1 Estado final das afirmações

Inclui as afirmações da tabela 8 cujo status mudou, as que foram reconfirmadas na verificação, as que seguem sem fonte oficial e quatro pontos fora da tabela 8 (marcados com §) que mudaram de status.

| id | status final | valor correto | fonte | de onde veio |
|---|---|---|---|---|
| A1 | CONFIRMADA | Reputação só a partir de 10 vendas concluídas em 365 dias | https://www.mercadolivre.com.br/ajuda/866 | seção 10 (obs. de A2); rodada2/nav-preco-reputacao (R2-PR-14) |
| A2 | CONFIRMADA (regra, data e corte anterior) | Desde 10 de setembro, 101 ou mais vendas concluídas em 60 dias → janela de 60 dias; menos de 101 → 365 dias. O corte anterior era 60. O ano 2026 não está escrito na nota: vem da tela de 6QFwvsIPSkQ (~0:30, 02/09/2026), que lê "a partir do dia 10 de setembro de 2026" no site. "68 vendas" não aparece em fonte oficial (erro do vídeo i9MQ51OkODg). | https://vendedores.mercadolivre.com.br/aprender/nota/vamos-mudar-a-forma-como-calculamos-sua-reputacao ; ajuda/866 | rodada2/nav-preco-reputacao (R2-PR-4 a 6); rodada2/sinais-recentes (R2-SIN-1, R2-SIN-4); TSV cases A26; reconciliação §1.9 |
| A3 | CONFIRMADA | Verde: reclamações ≤ 2%; canceladas ≤ 1,5% (60 d) e ≤ 2,5% (365 d); envios incorretos ≤ 10% (60 d) e ≤ 13% (365 d) | nota "por que a reputação é importante"; nota "vamos mudar..." | seção 10; rodada2/sinais-recentes (R2-SIN-2) |
| A4 | CONFIRMADA (vigente) | Escala de 60 dias (verde / amarelo / laranja; vermelho acima): reclamações 2 / 4,5 / 8%; canceladas 1,5 / 3,5 / 4%; envios incorretos 10 / 18 / 22%. A nota oficial de 2026 diz que os limites de 60 dias não mudaram, então a tabela da developers vale para as cores, embora esteja desatualizada no corte (60 em vez de 101). | nota "vamos mudar..."; https://developers.mercadolivre.com.br/pt_br/reputacao-de-vendedores | seção 10; rodada2/nav-preco-reputacao (R2-PR-5, R2-PR-7); rodada2/sinais-recentes (R2-SIN-2, R2-SIN-3) |
| §4 Faixas de 365 dias | CONFIRMADA (antes só via Terazi) | Canceladas: verde ≤ 2,5%, amarelo 2,5–5,5%, laranja 5,5–6,5%, vermelho > 6,5%. Envios incorretos: 13% / 13–23,5% / 23,5–28,5% / > 28,5%. Reclamações: 2% / 2–4,5% / 4,5–8% / > 8%, iguais nas duas janelas. Fecha a lacuna 9.2. | nota "vamos mudar..." | rodada2/nav-preco-reputacao (R2-PR-7); rodada2/sinais-recentes (R2-SIN-2, R2-SIN-3) |
| A5-A6 | CONFIRMADA | MercadoLíder: < 1% reclamações, < 0,5% mediações, < 0,5% canceladas, < 6% envios incorretos; 230 / 575 / 1.725 vendas e R$ 37.000 / 118.400 / 296.000 em 3 meses mais o mês vigente; mais de 4 meses de cadastro | https://www.mercadolivre.com.br/ajuda/864 | seção 10; rodada2/nav-preco-reputacao (R2-PR-14); reconciliação §1.9 |
| A7 | CONFIRMADA | Mediação só conta para MercadoLíder | ajuda/30193 | seção 10 (obs. de A8) |
| A8 | CONFIRMADA (antes "média, fonte única") | Só afetam reclamações de produto incompleto, faltante ou com problema de qualidade; pacote aberto ou avariado não | ajuda/30193 | seção 10 |
| A9 | CONFIRMADA (parte do arrependimento) | Reclamação de arrependimento não conta; venda com reclamação e depois cancelada conta só como reclamação. "Cancelada pelo comprador não conta" (ajuda/15027) não foi relida. | nota "por que a reputação é importante" | seção 10 (obs. de A3) |
| A10 | CONFIRMADA | Acima de 2,5% de canceladas a conta "poderá ser suspensa" (possibilidade, não automatismo) | ajuda/5205 | seção 10 |
| A11 | CONFIRMADA | Com `has_incentive` = true, resposta satisfatória em 48 h não afeta; com false, mesmas 48 h sem garantia. A data 20/08/2026 da página não foi checada. | developers/gerenciar-reclamacoes | seção 10 |
| A12 | CONFIRMADA | Envio incorreto inclui despacho atrasado, depósito errado e regras do Flex após 21 h | ajuda/30193 | seção 10 (obs. de A8); sinal coerente em w2izIQTFXi0 (01/10/2026: reagendamento do Flex afeta a reputação), rodada2/sinais-recentes §3 |
| A15 | CONFIRMADA (era SEM FONTE OFICIAL na seção 10) | Verde, MercadoLíder ou sem reputação: até 50% de desconto, já embutido na tabela; amarela: até 40%; laranja ou vermelha: sem desconto (até 0,3 kg a partir de R$ 79: R$ 25,90 contra R$ 12,95 no verde). Os 70% de 8dZiKLuJWXg (28/05/2026) não aparecem em nenhuma página pública atual: tratar como superado. | https://www.mercadolivre.com.br/ajuda/custos-envio-reputacao-verde-mercado-lider_40538 ; ajuda/40545 ; ajuda/40547 (índice ajuda/40525) | seção 11; TSV reputacao A15 e preco-promocao R4; rodada2/sinais-recentes (R2-SIN-9, R2-SIN-10); rodada2/nav-preco-reputacao (R2-PR-19); reconciliação §1.9 (pre R1–R4) |
| A16 | PARCIAL (era CONTESTADA parcial) | Consenso entre texto e fala: reputação amarela ou melhor e nenhuma dívida ou fatura vencida. Divergem: "15 dias de conta" e "10 vendas" só na fala oficial (três webinars de 2026); "anúncio ativo no catálogo" e a dispensa para quem está no Decola só no artigo escrito, que não tem data nem URL registrada. Não há fonte datada que desempate. | artigo da Central de aprendizagem "Quais requisitos preciso cumprir para criar campanhas de Aumentar Vendas com Product Ads?" (URL não registrada); JzejZyVeauE 10:05; 5UhmqSFuX7U 23:09; LOZL-QmsGL4 10:54 | seção 10; rodada2/webinars (R2-WEB-12) |
| A17 | PARCIAL | Abaixo de amarelo perde Ads (requisito oficial de A16). No catálogo, laranja ou vermelha "podem participar ... mas não ganhar" (participar não é o mesmo que perder o acesso). A automação de preços no catálogo exige amarela, verde-clara ou verde. A perda de Central de Promoções e de Minha Página segue só na fala da consultoria parceira (Ag1UXXB1fec). | https://vendedores.mercadolivre.com.br/nota/como-a-concorrencia-funciona-no-catalogo ; developers/automatizacoes-de-precos (01/10/2026) | TSV cases A27 (reconciliação cruzada); rodada2/nav-preco-reputacao (R2-PR-18) |
| A18 | CONTESTADA (parcial) → janela de cálculo de 60 dias ou do último ano | Faixas confirmadas (boa 75–100, média 50–74, ruim ≤ 30; a faixa de 31 a 49 não é descrita). Janela: com 100 vendas do anúncio em 60 dias, usa esse período; abaixo disso, o último ano. Os "180 dias" da developers são a janela das vendas com problema exibidas na API e nas telas, não o período de cálculo. Não há frase oficial que diga isso com todas as letras. | https://vendedores.mercadolivre.com.br/nota/como-proporcionar-a-melhor-experiencia-de-compra ; https://developers.mercadolivre.com.br/pt_br/experiencia-de-compra (03/02/2026) | seção 10; rodada2/nav-preco-reputacao (R2-PR-8, R2-PR-9) |
| A19 | CONFIRMADA | Em kit vale o produto de pior desempenho | ajuda/39234 | seção 10 (obs. de A18) |
| A20 | CONFIRMADA (era PRÁTICA com tela) | Com menos de 100 vendas, a nota do anúncio é complementada com os outros anúncios da categoria, desde que somem 200 vendas; sem isso, o anúncio fica sem experiência. O vídeo ZYce3H1naP4 fala em "200 vendas em 60 dias"; a nota oficial não fixa a janela desse complemento. | nota "como proporcionar a melhor experiência de compra" | rodada2/nav-preco-reputacao (R2-PR-8); rodada2/sinais-recentes (R2-SIN-25) |
| A21 | CONFIRMADA | Decola: R$ 250, até 365 dias, 5 vendas afetadas, devolução de R$ 250 a R$ 0; os "90 dias" do webinar de maio estão superados | ajuda/33314 | seção 10 |
| A22 | CONFIRMADA (ampliada) | Reputação Protegida: 3% (vermelho ou laranja), 2% (amarelo) ou 1% (verde) do faturamento de 60 dias; até 60 dias corridos ou até o limite de vendas afetadas; saldo liberado 10 dias corridos após o fim; reativação só 6 meses depois se encerrada pelo limite (antes via terceiro, agora oficial); aceita verde ou MercadoLíder com anúncios em amarelo ou vermelho; o ML pode oferecer só a vendedores específicos | ajuda/29276 ; ajuda/29528 | seção 10; rodada2/nav-preco-reputacao (R2-PR-12); rodada2/sinais-recentes (R2-SIN-6) |
| A23 | SEM FONTE OFICIAL (valores) | Os R$ 75 a R$ 250 mil e os 120 dias não aparecem em nenhuma página oficial: não usar. No Brasil, os termos oficiais do Benefício de Reputação (`RECOVERY_GRNTEE`) apontam para a ajuda/29528, intitulada "Reputação Protegida" (mesmo id que leva a "beneficio de reputación" nos outros países). Indício forte de que são o mesmo programa, sem frase oficial que o diga. Para valores, usar os de A22. | https://developers.mercadolivre.com.br/pt_br/recuperacao-de-reputacao (04/02/2025); ajuda/29528 | rodada2/nav-preco-reputacao (R2-PR-11, R2-PR-13); rodada2/sinais-recentes (R2-SIN-5, R2-SIN-7) |
| §2.5 Benefício × Protegida | ABERTA (inferência média-alta) | Provável mesmo regulamento no Brasil (ver A23). A página `/reputacao/beneficio_reputacao` segue exigindo login. A developers ainda exclui o verde; a ajuda/29528 já aceita verde com anúncios amarelos ou vermelhos. | idem A23 | rodada2/nav-preco-reputacao; rodada2/sinais-recentes |
| A24-A25 | CONFIRMADA | Devolução: 30 dias (novo), 5 dias (usado); arrependimento e "não serve" grátis para o vendedor e sem impacto; defeito, diferente ou incompleto custa e pode afetar; frete do arrependimento pago pelo ML | ajuda/3285 ; ajuda/28088 ; ajuda/32761 | seção 10 |
| A27 | PARCIAL | A tabela de custos de envio da ajuda/40538 vale para Full, Coleta e Agência, com o desconto por reputação (até 50% no verde) já embutido. Os "50% no Full a partir de R$ 79" da ajuda/5171 coincidem com o desconto por reputação, e não aparecem como benefício próprio do Full na tabela atual (leitura cruzada, não frase oficial). "O ML responde reclamações de entrega no Full" não foi relido. | ajuda/40538 | TSV logistica-estoque R7 (reconciliação cruzada) |
| A32 | PARCIAL | Escrito: cancelamento por problema dos Correios ou da transportadora não prejudica (ajuda/5205). Que atraso de coleta ou agência não penaliza e que o Flex Turbo é responsabilidade do vendedor segue só via canal (Ag1UXXB1fec). | ajuda/5205 | seção 10 (obs. de A10) |
| A34 | SEM FONTE OFICIAL (prática) | Alerta a 50% do limite: um praticante, com tela | HRmtJMCZdZw | sem mudança |
| A35 | SEM FONTE OFICIAL (prática + canal) | Atrasar em vez de cancelar: lógica coerente com os limites oficiais (canceladas 1,5% ou 2,5% contra envios incorretos 10% ou 13%), sem texto oficial que recomende | HRmtJMCZdZw; Ag1UXXB1fec | sem mudança; limites de 365 dias agora oficiais |
| A36 | SEM FONTE OFICIAL (prática) | Teste de 100% e pós-venda 7 dias por semana, sem números auditados | 0yjqItQOMyI | sem mudança |
| A37 | SEM FONTE OFICIAL | O ML não publica taxa de devolução saudável; o ~2% é de consultoria | 0yjqItQOMyI | sem mudança |
| A38 | ABERTA | Efeito da medalha nas vendas: oficial diz "mais exposição", praticante não viu efeito, ninguém tem holdout | ajuda/864; 6hPsDJ-D7oM | sem mudança |
| A39 | PARCIAL | OBS de 14/10 não repetida com protocolo; a medalha não aparece no card da busca e exige abrir o anúncio | observacao/lideres.md | rodada2/nav-observacao |
| §2.2 Terazi (dinheiro em 8 dias, Flex exige amarelo ou verde) | SEM FONTE OFICIAL | Sem página oficial lida | Terazi | sem mudança |
| §2.2 Terazi (campanhas de desconto exigem verde) | PARCIAL | Cupons do vendedor: só MLB e só reputação verde (developers, 28/08/2025). Não há regra lida para as demais campanhas do vendedor. | https://developers.mercadolivre.com.br/pt_br/cupons-do-vendedor | TSV preco-promocao R12 (reconciliação cruzada) |

Sem mudança de status e sem reverificação nesta rodada (seguem como lidas na rodada 1, em 14/10/2026): A14 (ajuda/21065), A26 (triagem do Full), A28 (opiniões não afetam), A29 (mensagens com motivo e cota), A33 (`expiring_food` e `expiring_health`), A40 (avaliação de catálogo é do produto) e A41 (página antiga superada, agora reforçada pela nota de 2026).

### 12.2 Reconciliações aplicadas (LACUNAS §1.9 e cruzadas)

**De §1.9 que tocam esta frente**
1. **MercadoLíder e reputação [cases A25–A26] ← [rep A2–A6].** Aplicada nos dois sentidos. As ajudas 864 e 866 foram relidas (R2-PR-14), e a verificação de cases A26 trouxe a nota oficial "vamos mudar..." com o corte de 60 para 101 a partir de 10/09. Resultado: A2 passa a CONFIRMADA também na data e no corte anterior. O "68" é erro de fonte em [rep A2] e em [cases A26].
2. **Tabela de envio e desconto de até 50% [pre R1–R4] ← [alim A8] (ajuda/40538).** Aplicada a [rep A15]: o desconto por reputação está confirmado em três ajudas (40538, 40545, 40547), lidas por navegador (seção 11) e também por leitura direta sem navegador (rodada2/sinais-recentes).
3. **Full Super: R$ 8, sem armazenagem P/M, R$ 199 [log R8] ← [alim A5–A7].** Só toca esta frente pela exigência de reputação verde (ajuda/16449). Entra como consequência do verde em 12.3.

**Cruzadas (outras frentes, sem coleta nova)**
- [cases A27] → [rep A17]: laranja e vermelha participam do catálogo, mas não ganham.
- [pre R12] → divergência Terazi da §2.2: cupons do vendedor exigem verde.
- [log R7] → [rep A27]: a tabela de envio é a mesma para Full, Coleta e Agência.
- [log R9] e R2-FS-16 → consequência do verde: o estoque compartilhado do Full exige reputação verde e experiência de compra de 75 ou mais.
- [rank A9] → [rep A18]: a divergência da janela (60/365 contra 180 dias) fica rebaixada para "janelas com funções diferentes".

### 12.3 Achados novos da rodada 2 desta frente

| id | achado | tipo | fonte | confiança |
|---|---|---|---|---|
| R2-PR-4 / R2-SIN-1 | Corte da janela de 60 para 101 vendas "a partir de 10 de setembro"; a mudança é automática | OFICIAL | nota "vamos mudar..."; ajuda/866 | alta (ano: média-alta) |
| R2-PR-7 / R2-SIN-2 / R2-SIN-3 | Tabela oficial completa por cor nas janelas de 60 e 365 dias; reclamações iguais nas duas | OFICIAL | nota "vamos mudar..." | alta |
| R2-PR-5 / R2-SIN-4 | A developers de reputação (11/08/2025) segue com 60 vendas para MLB; "68" não existe em fonte oficial | OFICIAL + OBS por ausência | developers/reputacao-de-vendedores; i9MQ51OkODg | alta |
| R2-PR-8 | Experiência de compra: 100 vendas do anúncio em 60 dias, senão o último ano; abaixo de 100, complemento pela categoria com mínimo de 200 vendas; sem isso, sem experiência | OFICIAL | nota "como proporcionar a melhor experiência de compra" | alta |
| R2-PR-9 | Os "180 dias" são a janela de exibição das vendas com problema; score −1 = item sem vendas | OFICIAL | developers/experiencia-de-compra (03/02/2026) | média |
| R2-PR-10 | Congelamentos "Benefício de reputação" e "Verde claro" impedem perda de exposição e pausa por experiência média ou ruim | OFICIAL | developers/experiencia-de-compra | alta |
| R2-PR-11 / R2-SIN-5 | Benefício de Reputação (`RECOVERY_GRNTEE`, para amarelo, laranja ou vermelho, só por convite) tem como termos no Brasil a ajuda/29528, "Reputação Protegida" | OFICIAL (inferência por link e id) | developers/recuperacao-de-reputacao; ajuda/29528 | média-alta |
| R2-PR-12 / R2-SIN-6 | Protegida: 1–3% do faturamento de 60 dias, 60 dias corridos, reativação após 6 meses se encerrada pelo limite, liberação em 10 dias, elegibilidade ampliada a verde ou Líder com anúncios amarelos ou vermelhos | OFICIAL | ajudas 29528 e 29276 | alta |
| R2-PR-13 / R2-SIN-7 | R$ 75–250 mil e 120 dias sem fonte oficial: não usar | OBS por ausência | ajudas 29528 e 29276; developers | média |
| R2-SIN-8 | Em set–out/2026 a Protegida aparece oferecida a contas verdes; exemplo em tela: garantia de R$ 21.250 por 60 dias (cerca de 1% do faturamento de 60 dias, coerente com a regra), perde a proteção com 855 vendas afetadas, devolve 100% com 0–170 afetadas e 80% com 171–341 | PRÁTICA (tela) | PbU19wAcBlw ~0:30–6:00; w2izIQTFXi0 ~1:00 | média |
| R2-SIN-9 / R2-SIN-10 | Desconto de envio por cor: 50% / 40% / 0%; o "até 70%" está superado | OFICIAL | ajudas 40538, 40545, 40547 | alta |
| R2-PR-18 | A automação de preços no catálogo exige reputação amarela, verde-clara ou verde | OFICIAL | developers/automatizacoes-de-precos (01/10/2026) | alta |
| R2-WEB-3 | O Ad Rank do Product Ads considera a "qualidade", que inclui reputação do vendedor, pós-venda e avaliações, além de relevância e ROAS objetivo. Primeiro vínculo oficial, ainda que oral, entre reputação e leilão de Ads. | OFICIAL via canal | LOZL-QmsGL4 16:28–17:32 (30/09/2026) | média |
| R2-WEB-12 | Requisitos de Product Ads repetidos em três webinars de 2026 (amarela ou melhor, 10 vendas, 15 dias, sem fatura vencida), em conflito com o artigo escrito | OFICIAL via canal | JzejZyVeauE 10:05; 5UhmqSFuX7U 23:09; LOZL-QmsGL4 10:54 | média |
| (webinars §, sem id) | A campanha "Aumentar Seguidores" exige Minha Página ativa e reputação amarela ou melhor | OFICIAL via canal | LOZL-QmsGL4 52:21 | média |
| R2-FS-15 | Estoque compartilhado no Full: o vendedor não sofre impacto por problema de produto de outro vendedor, e quem fica fora do padrão de qualidade é retirado. Passa a parte oficial da D4 de "via praticante, tela" para texto N1. | OFICIAL | https://www.mercadolivre.com.br/ajuda/42158 | alta |
| R2-FS-16 | Estoque compartilhado exige vendedor verde e produto sem reclamações, com experiência de 75 ou mais, no catálogo e sem validade; exclui Alimentos e Bebidas | OFICIAL | ajuda/42159 | alta |
| R2-FS-7 (consequência do verde) | Full Super exige reputação verde e preço acima de R$ 8 | OFICIAL | ajuda/16449 | alta |
| R2-SIN-19 a R2-SIN-21 | Reclame Aqui (N8, amostra pequena por bloqueio 403): em 27/09–15/10/2026, 6 reclamações de alimento ou suplemento em 63 registros; padrão dominante de validade curta ou vencida, mais avaria, data adulterada e embalagem inadequada; recorre a exigência de devolução física do alimento vencido para o estorno. Sem taxa por pedido. | DADO (N8) | busca pública do Reclame Aqui | média |
| R2-SIN-22 / R2-SIN-23 | Contexto de volume (todas as categorias): "Atraso na entrega" 138.697, "Produto errado" 23.650, "Encomendas danificadas" 5.349 no histórico; 199.069 reclamações de abr a set/2026, 77,1% resolvidas | DADO (N8) | Reclame Aqui | média (não é taxa por pedido) |
| R2-EVC-9 | Experimento no eBay: ranking que promove vendedores de maior qualidade não observável elevou em 0,3 p.p. a volta do comprador; a nota positiva média de 99,3% discrimina pouco. Explica por que a plataforma pesa experiência além das opiniões, sem medir o peso no ML. | DADO (acadêmico) | nber.org/papers/w20830 | alta (no contexto do eBay) |

### 12.4 Perguntas do protocolo (§7.6)

| Q | status | motivo |
|---|---|---|
| Q1. Cálculo da reputação (componentes, janelas, níveis, limites) | **R** (ML) | Componentes, fórmulas, corte de 101 vendas com data e tabela completa por cor nas janelas de 60 e 365 dias estão em N1 (nota de 2026, ajudas 866, 864, 30193). Resta só o ano escrito da vigência, que vem de tela de vídeo. Shopee e Amazon estão fora do escopo desta nota (ver seção 9). |
| Q2. Consequências de cada nível | **P** | Agora oficiais: frete por cor (50/40/0%), Ads só a partir de amarelo, catálogo sem vitória para laranja e vermelho, cupons, Full Super e estoque compartilhado só no verde, automação de catálogo a partir de amarelo, reputação no Ad Rank (fala). Seguem sem N1: perda de Central de Promoções e Minha Página no laranja, dinheiro em 8 dias, Flex por cor e o tamanho do efeito da medalha na exposição (D2, sem holdout). |
| Q3. Exclusões e contestação | **P** | As exclusões estão em N1 (arrependimento, cancelamento pelo comprador, transportadora, pacote avariado, `avoid_reputation`). A contestação não tem página oficial com fluxo nem número de recursos: as "duas chances" seguem em N7, e a rodada 2 não trouxe fonte nova. |
| Q4. Como os melhores operam o atendimento | **P** | Práticas convergentes (P1 a P11) vêm de praticantes e do canal oficial, sem *benchmark* público de tempo de resposta, mediação ou devolução por categoria. A rodada 2 só acrescenta que o pós-venda entra na "qualidade" do Ad Rank (R2-WEB-3, fala). |
| Q5. Métricas internas com margem de segurança | **P** | Uma única fonte de praticante com tela (HRmtJMCZdZw, alerta a 50% do limite). As contas de margem podem agora ser derivadas de limites oficiais completos (inclusive 365 dias), mas não há segunda fonte de prática nem dado de resultado. |
| Q6. Avaliação negativa e suas causas | **P** | Em N1: opiniões não afetam a cor; taxonomia de causas da experiência de compra, com *remedy*. A rodada 2 traz só sinal N8 (Reclame Aqui, amostra pequena) sobre alimentos: validade, avaria e embalagem dominam, e o atraso não aparece ligado a alimento. Não há taxa por pedido nem leitura das opiniões de produto do ML. |
| Q7. Experiência de compra no diagnóstico de produto | **R** (ML) | Faixas, janela de cálculo (60 dias ou último ano), complemento pela categoria, janela de 180 dias de exibição, taxonomia com *remedy*, congelamentos e regra do kit, tudo em N1. Ressalva: a função dos "180 dias" é leitura cruzada, sem frase oficial. O POE da Amazon fica fora desta nota. |
| Q8. Fulfillment contra envio próprio na reputação | **P** | Em N1: triagem de 3 dias úteis, mesma tabela de frete para Full, Coleta e Agência e nenhum impacto por produto de outro vendedor no estoque compartilhado (ajuda/42158). Seguem abertas as divergências internas da Ajuda (retirada de não aptos em 20 ou 30 dias; contestação em 60 dias corridos ou úteis), a frase "o ML responde reclamações de entrega no Full", que não foi relida, e qualquer dado comparando taxas de reclamação entre Full e envio próprio. |

### 12.5 Contaminação verificada

**Resultado: nenhuma contaminação encontrada. Nada foi descartado por esse motivo.**

O que foi checado:
- **URLs da seção 11 e da linha da frente no TSV:** todas são do domínio mercadolivre.com.br (ajudas 40538, 40545, 40547 e o índice 40525). O conteúdo bate com cada URL: verde até 50%, amarela até 40%, laranja ou vermelha sem desconto. A mesma leitura foi feita de forma independente, sem navegador, por `curl` em rodada2/sinais-recentes, e também pelas frentes preco-promocao (R4) e logistica-estoque (R7) no TSV.
- **Nota "vamos mudar..." e ajuda/29528:** foram lidas por duas sessões diferentes (nav-preco-reputacao, pelo Chrome; sinais-recentes, por `curl`), com a mesma tabela e os mesmos termos. Isso afasta resposta trocada entre abas.
- **URLs de outras plataformas na rodada 2:** só aparecem em `dados-mercado.md` (advertising.amazon.com, benchmarks do Amazon Ads) e em `evidencias-cases.md` (estudos da Amazon). Estão rotuladas como Amazon nos próprios arquivos e não foram usadas aqui. Nenhuma afirmação da rodada 2 ou da seção 11 usada nesta seção cita shopee ou amazon como fonte de regra do ML.
- **R2-EVC-9:** a URL do NBER (w20830) corresponde ao estudo de Nosko e Tadelis sobre o eBay descrito no arquivo.

Diferenças que não são contaminação, registradas para não confundir:
- O complemento da experiência pela categoria tem "200 vendas" na nota oficial, sem janela, e "200 vendas em 60 dias" no vídeo ZYce3H1naP4. Vale a versão oficial.
- Os termos do Decola aparecem como ajuda/33285 na developers, e a página de ajuda do programa é a 33314. São páginas diferentes, não conflito.
- R2-FS-21 alerta que a trilha de links no topo da Central de Ajuda reflete o histórico da sessão. Nenhuma conclusão desta seção depende dessa trilha.
- O Reclame Aqui traz nomes de marcas e lojas nos endereços das reclamações. Eles não foram reproduzidos aqui, pela regra de neutralidade.
