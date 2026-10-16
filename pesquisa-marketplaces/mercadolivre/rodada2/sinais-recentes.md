# Sinais recentes: Mercado Livre (rodada 2)

Frente "sinais-recentes" · acesso em 2026-10-15 · fecha LACUNAS §4 itens 37 e 38 (recorte ML) e toca nos itens 15, 16 e 18.
Pesquisa neutra: descreve regras da plataforma e o padrão público de reclamações. Não trata de nenhuma empresa específica.

**Método.**
- Páginas oficiais lidas por `curl` sem login: ajudas 866, 5200, 29276, 29528, 40538, 40545, 40547, 44922 e 870; notas da Central de vendedores; páginas de developers.
- YouTube: `buscar_youtube.py --dias 60` com 10 consultas. Legendas de 7 vídeos baixadas com `baixar_legendas.py --pausa 6`; outras 3 já estavam em `mercadolivre/transcricoes`.
- WebSearch: 6 buscas.
- Reclame Aqui: endpoint público de busca, sem login. A busca respondeu 403 depois de cerca de 7 consultas, nas duas tentativas. Não insistimos: a amostra ficou pequena (ver §2).
- Tipos de fonte: [OFICIAL] N1; [PRÁTICA] criador ou praticante; [DADO] contagem pública (Reclame Aqui, N8). As datas sem fonte própria são de acesso (2026-10-15).

---

## Resumo

1. **Corte da janela de reputação: fechado em N1, com data.** A nota oficial "Vamos mudar a forma como calculamos sua reputação" diz:
   - a regra vale "a partir de 10 de setembro" (a nota não traz o ano; o contexto e os vídeos de 02/09/2026 dão 2026);
   - o corte sobe de 60 para **101 vendas em 60 dias**;
   - a medição em 365 dias ganha limites próprios e mais folgados: canceladas, verde até 2,5% (era 1,5%); envios incorretos, verde até 13% (era 10%); reclamações sem mudança.

   O "68" não aparece em nenhuma página oficial. É erro de um canal de 1 minuto sem tela. O developers ainda mostra 60 (página de 11/08/2025, desatualizada).
   Fecha: REP A2 e a divergência 101/68/60 (§1.6); LACUNAS §4 #16 (parte da reputação) e #37 (janela de 68). → R2-SIN-1 a R2-SIN-4.
2. **Benefício de Reputação e Reputação Protegida são, no Brasil, o mesmo programa.**
   - A página oficial de developers "Programa Decola e Benefício de Reputação" (atualizada em 04/02/2025) liga os termos do Benefício no Brasil à ajuda/29528.
   - A ajuda/29528 se chama "Termos e condições da Reputação Protegida".
   - Nos outros países, o mesmo link leva a "beneficio de reputación".
   - Os valores de terceiros (R$75 a R$250 mil, 120 dias) não aparecem em nenhuma página oficial. O texto oficial atual dá garantia de 1% a 3% do faturamento de 60 dias e prazo de 60 dias.
   - A elegibilidade se ampliou: a ajuda/29528 aceita verde ou MercadoLíder "com algumas publicações em amarelo ou vermelho". O developers ainda exclui o verde.
   - Em set–out/2026, vários vendedores mostram na tela a oferta em contas verdes, com garantias de R$1 mil a R$25 mil.

   Fecha (com inferência): REP A23 e §9.3; LACUNAS §4 #18. → R2-SIN-5 a R2-SIN-8.
3. **Desconto de frete por reputação: vale 50% (verde) e 40% (amarelo); 70% está superado.** As ajudas 40538, 40545 e 40547 (lidas hoje) dizem:
   - verde: até 50%, "já incluem essa isenção" na tabela;
   - amarelo: até 40%;
   - laranja e vermelho: sem seção de desconto.

   Os 70% vieram da tabela de custos logada lida em vídeo de 28/05/2026. Hoje não há 70% em nenhuma página pública.
   Fecha: REP A15 e PRE A5 em favor de 50/40. → R2-SIN-9, R2-SIN-10.
4. **Custo abaixo de R$79: duas páginas oficiais em vigor que não batem.**
   - A nota "Como funcionam as taxas do Mercado Livre?" segue no ar, sem data. Ela traz o custo fixo de 50% abaixo de R$12,50 e três faixas entre R$12,50 e R$79.
   - A ajuda/870 ("Quanto custa vender") não fala em custo fixo.
   - A ajuda/40538 fala só em faixas de custo de envio, com teto de metade do preço abaixo de R$19.
   - O vídeo de maio leu exatamente a nota antiga (mesmo exemplo de R$8 → R$4).

   Não fecha: a hipótese mais provável é que a nota esteja desatualizada, mas não há comunicado de troca. → R2-SIN-11, R2-SIN-12.
5. **Full: extragrandes confirmados em N1 e uma nova lista sem condição de tamanho.**
   - A ajuda/44922 confirma os limites: igual ou maior que 20 kg, lado igual ou maior que 80 cm, volume igual ou maior que 125 L. Há exceção por preço mínimo de R$100 ou R$200 conforme a subcategoria.
   - A data de 20/05/2026 só aparece em terceiros (UpSeller, 26/05/2026; leitura de e-mail em 23/04/2026).
   - O resumo da página (metadado SEO) diz "Produtos restritos ao Full a partir de 15 de outubro", o que sugere uma nova onda.
   - A ajuda/5200 já traz a lista proibida sem condição de tamanho: assadeiras, cabides, copos e taças, mops etc. Um vídeo de 04/09/2026 diz que essa lista foi anunciada em 03/09, com vigência em 16/09.
   - Nenhum item de Alimentos e Bebidas está na lista de extragrandes; Ração para cães e gatos está.

   Fecha: LOG R6 e A9 (limites e preços mínimos). Data em aberto. → R2-SIN-13 a R2-SIN-16.
6. **Punição por preço externo: segue sem página oficial.**
   - O que é oficial: o ML compara preço com concorrentes "internos ou externos" (developers, referências de preço, 17/12/2025). A automação tem a estratégia "melhor preço dentro e fora do Mercado Livre", que considera outros sites e o Google.
   - O aviso, o prazo de 3 dias e a perda de visibilidade, campanhas e Ads vêm só da imprensa (23–24/10/2025).
   - Nenhum vídeo dos últimos 60 dias traz tela de comunicado novo.

   Fecha em parte: CASES A3 continua [OFICIAL via terceiro]. → R2-SIN-17, R2-SIN-18.
7. **Reclamações de alimentos no ML (Reclame Aqui, amostra de 27/09 a 15/10/2026):**
   - Entre as 60 reclamações mais recentes com "vencido" ou "validade", 6 são de alimento ou suplemento, cerca de 2 por semana nessas buscas. Padrões:
     - validade curta ou vencido;
     - avaria (leite amassado);
     - data adulterada;
     - embalagem inadequada;
     - exigência de devolver o alimento vencido para receber o reembolso.
   - Cosméticos e medicamentos veterinários dominam o tema "vencido".
   - A busca por termo não mostrou "atraso" ligado a alimento; o atraso aparece só no total geral.

   Fecha em parte: LACUNAS §4 #38 e REP Q6/ALIM Q2 (sinal N8, sem taxa por pedido). → R2-SIN-19 a R2-SIN-24.
8. **Outros sinais dos últimos 60 dias** (N8, só levantam pergunta):
   - experiência de compra herdada da categoria;
   - multiestoque com falha de disponibilidade;
   - indisponibilidade de compras no RS em setembro;
   - limite automático de capacidade de envio;
   - nova restrição de bebidas alcoólicas no Full;
   - "produtos selecionados" de Supermercado com tarifa menor;
   - aumento de frete em 24/08.

   → R2-SIN-25 a R2-SIN-29.

---

## Achados

### 1. Mudanças de regra dos últimos 60 dias (item 37)

#### 1.1 Janela de reputação (101, 68 ou 60)
- **Comunicado oficial: existe.** `https://vendedores.mercadolivre.com.br/aprender/nota/vamos-mudar-a-forma-como-calculamos-sua-reputacao` (sem data na página; vigência "a partir de 10 de setembro"; lida em 2026-10-15).
  - Dois critérios mudam: o volume de vendas que define o período e o limite de vendas afetadas na medição de 365 dias.
  - Exemplo da própria nota: com 100 vendas em 60 dias, a medição passa a ser de 365 dias.
  - Tabela oficial:

| Variável | Cor | Últimos 60 dias | Últimos 365 dias |
|---|---|---|---|
| Canceladas por você | Verde | até 1,5% | até 2,5% |
| | Amarelo | 1,5–3,5% | 2,5–5,5% |
| | Laranja | 3,5–4% | 5,5–6,5% |
| | Vermelho | > 4% | > 6,5% |
| Envios incorretos | Verde | até 10% | até 13% |
| | Amarelo | 10–18% | 13–23,5% |
| | Laranja | 18–22% | 23,5–28,5% |
| | Vermelho | > 22% | > 28,5% |
| Reclamações (igual nos dois períodos) | Verde até 2%; amarelo 2–4,5%; laranja 4,5–8%; vermelho > 8% | | |

  - A nota diz que a mudança é automática ("Não, a mudança será aplicada automaticamente em 10 de setembro").
- **Confirmação atual:** a ajuda/866, lida hoje, mantém 101 (igual ou mais de 101 vendas → 60 dias; menos → 365 dias). A página não tem data.
- **Tela de comunicado em vídeo:** 6QFwvsIPSkQ (Natan Aquino, 02/09/2026, aos ~0:30). O criador lê o site oficial, com a frase "a partir do dia 10 de setembro de 2026", e mostra os mesmos 2,5% e 13%. Também 2REuci4X_8g (03/09/2026).
- **O "68":** i9MQ51OkODg (Giro do E-commerce, 21/08/2026, vídeo de 1 min, sem tela) diz "o mínimo sobe para 68 vendas". Nenhuma página oficial (nota, ajuda/866, developers) traz 68. Veredito: erro do canal.
- **Developers desatualizado:** `developers.mercadolivre.com.br/pt_br/reputacao-de-vendedores` ("Última atualização em 11/08/2025") ainda diz MLB maior ou igual a 60 vendas.
- **Onde fica a N1:** a nota acima (Central de aprendizagem) e a ajuda/866.

#### 1.2 Benefício de Reputação contra Reputação Protegida
- `https://developers.mercadolivre.com.br/pt_br/recuperacao-de-reputacao` ("Última atualização em 04/02/2025"):
  - dois tipos de programa: Decola (`NEWBIE_GRNTEE`, para quem não tem reputação) e Benefício de Reputação (`RECOVERY_GRNTEE`, para amarelo, laranja ou vermelho);
  - verde "excluído de participar";
  - acesso só por convite.
- O link "Termos e Condições Brasil (MLB)" do Benefício aponta para `mercadolivre.com.br/ajuda/termos-e-condicoes-reputacao-vantagens_29528`. Essa ajuda se chama **"Termos e condições da Reputação Protegida"**. Em MLA, MLM, MLC e MCO, o mesmo item leva a "terminos-y-condiciones-beneficio-de-reputacion_29528" (mesmo id).
  - Inferência: no Brasil, o Benefício de Reputação é comercializado como Reputação Protegida. Confiança média-alta: mesmo id e mesmo tipo na API; falta uma frase oficial que diga isso.
- **Termos atuais (ajuda/29528, sem data):**
  - Quem pode: amarelo, laranja ou vermelho, ou verde/MercadoLíder com algumas publicações em amarelo ou vermelho.
  - Garantia: 3% (vermelho ou laranja), 2% (amarelo) ou 1% (verde) do faturamento de 60 dias.
  - Prazo: 60 dias corridos ou até atingir o limite de vendas afetadas.
  - Reativação: uma vez a cada 6 meses se a proteção terminar pelo limite.
  - O depósito de pessoa física rende.
  - Liberação 10 dias corridos depois do fim.
  - A ajuda/29276 (lida hoje) repete os 1–3% e os 60 dias, e põe a experiência de compra dos anúncios em 100.
- **R$75 a R$250 mil e 120 dias:** sem nenhuma página oficial. Pode ser regra antiga do Benefício ou de outro país. Recomenda-se não usar.
- **Tela em vídeo (set–out/2026):**
  - PbU19wAcBlw (Empresa em Ação, 05/10/2026, de ~0:30 a ~6:00) mostra a oferta numa conta verde de cerca de R$1 milhão por mês. Garantia de R$21.250 por 60 dias; perde a proteção com 855 vendas afetadas; devolve 100% com 0–170 afetadas e 80% com 171–341. A garantia equivale a 1% de cerca de R$2,1 milhões em 60 dias, coerente com a regra oficial.
  - w2izIQTFXi0 (Bruno Gontijo, 01/10/2026, ~1:00) relata a oferta "em todas as contas", com valores de R$1 mil a R$25 mil, como resposta à experiência de compra por categoria.
- **Onde fica a N1:** ajudas 29528 e 29276. Para saber se o "Benefício" com outro valor ainda existe, só com painel logado (`/reputacao/beneficio_reputacao` exige login).

#### 1.3 Desconto de frete por reputação (50% contra 70%)
- **Oficial atual (sem data, lido hoje):**
  - ajuda/40538: "Até 50% de desconto nos seus custos por ter reputação verde", valores já na tabela;
  - ajuda/40545: amarela, até 40%;
  - ajuda/40547: laranja ou vermelha, sem desconto.
- **70%:** 8dZiKLuJWXg (Natan Aquino, 28/05/2026, ~2:00) lê "desconto de até 70% por reputação" na tabela de custos logada (`/landing/custos-de-venda`, que exige login). Nenhuma página pública traz 70% hoje.
- Veredito: o 70% está superado ou era outra base de cálculo. Não há comunicado de troca localizado. Um vídeo de 02/09/2026 (Mj-oOzE0ZuE, ~0:30) cita aumento de frete desde 24/08/2026, "mais ou menos 90 centavos", com e-mail oficial na tela. Isso coincide com o reajuste de envio de 24/08/2026 já citado em PRE A7.
- **Onde fica a N1:** ajudas 40525, 40538, 40545 e 40547. O comunicado de 24/08/2026 só foi por e-mail ao vendedor.

#### 1.4 Custo abaixo de R$79 (degraus contra o corte de R$12,50)
- **A nota antiga segue no ar:** `vendedores.mercadolivre.com.br/nota/como-funcionam-as-taxas-do-mercado-livre` (sem data, lida hoje).
  - Abaixo de R$12,50, o custo fixo é 50% da unidade (exemplo de R$8 → R$4).
  - Entre R$12,50 e R$79, "o custo fixo varia em três faixas de preço".
  - Acima de R$79, não há custo fixo.
- **Páginas de ajuda atuais:**
  - ajuda/870 (tarifa Clássico 10–14%, Premium 15–19%): não fala em custo fixo.
  - ajuda/40538: faixas de custo de envio para todas as vendas; abaixo de R$19, no máximo metade do preço; de R$19 a R$78,99, frete grátis padrão; rápido abaixo de R$79 opcional, a partir de R$12,95.
- O vídeo 8dZiKLuJWXg (28/05/2026) lê exatamente a nota antiga, com o mesmo exemplo. Ou seja, o "corte de R$12,50" é a mesma fonte, não uma confirmação independente.
- Nenhum vídeo dos últimos 60 dias trouxe comunicado sobre custo fixo.
- **Onde fica a N1:** a simulação logada (`/landing/custos-de-venda`, exige login) ou a API `listing_prices` (LACUNAS #11). Sem um dos dois, a conta abaixo de R$79 fica em faixa.

#### 1.5 Extragrandes no Full (20/05/2026) e a nova lista
- **ajuda/44922**, "Produtos extragrandes restritos para envio ao Full" (sem data no corpo; lida hoje):
  - limites: peso igual ou maior que 20 kg, lado igual ou maior que 80 cm, volume igual ou maior que 125 L;
  - "Exceção por preço mínimo": se o preço de venda for igual ou maior que o mínimo da lista, o item pode seguir no Full;
  - mínimos: R$100 ou R$200 por subcategoria, ou "Sem exceção";
  - fecho literal: "você poderá continuar vendendo esses produtos por meio de outras logísticas".
  - Exemplos de mínimo: Recipientes para alimentos R$100; Carrinhos de compras R$200; Andadores médicos R$200; Ração para cães e gatos "Sem exceção".
  - Não há Alimentos e Bebidas nem Supermercado na lista.
- **Data:** o corpo não traz data. O metadado de descrição da página diz "Produtos restritos ao Full a partir de 15 de outubro". A data de 20/05/2026 vem de hz-H-lBm390 (23/04/2026, leitura de e-mail) e do blog UpSeller (26/05/2026).
- **Lista sem condição de tamanho:** a ajuda/5200, "Quais produtos são proibidos de enviar ao Full?" (sem data), lista assadeiras e formas, assento sanitário, cabides, colchões, copos e taças, escrivaninhas, lixeiras, mops/rodos/esfregões, pisos vinílicos, varais e varões.
  - ZYce3H1naP4 (Bruno Gontijo, 04/09/2026, ~0:40) diz que a lista foi "anunciada ontem", com vigência a partir de 16 de setembro, um "prazo de somente 13 dias".
  - w2izIQTFXi0 (01/10/2026) relata também espaço reduzido no Full e falta de coleta.
- A mesma ajuda/5200 traz regras ligadas a alimentos:
  - recusa de "consumo recorrente" com validade próxima;
  - data de validade legível, no idioma do país e não escrita à mão;
  - Supermercado "habilitados para vendedores autorizados";
  - kits de supermercado sem código universal recusados;
  - proibição de itens com controle de temperatura.
- **Onde fica a N1:** ajudas 44922 e 5200 (confirmadas). A data de cada onda está só no e-mail ou em Novidades da Central (exige login).

#### 1.6 Punição por preço externo
- **Oficial:**
  - developers "Gerenciar referências de preços" (17/12/2025): referência "com base em concorrentes internos ou externos"; status `with_benchmark_highest` e `with_benchmark_high`.
  - nota "Vença a concorrência automatizando seus preços": estratégia 2 considera "outros sites e ferramentas de busca (como Google)".
  - Nenhuma página fala em aviso, prazo de 3 dias ou perda de exposição.
- **Imprensa:**
  - Mercado&Consumo, 24/10/2025: monitoramento desde 23/10/2025; aviso; 3 dias para alinhar; menos visibilidade, campanhas e Ads.
  - Gironews e Seu Crédito Digital repetem.
  - Um diretor do ML diz que não há exclusividade.
- **Últimos 60 dias:** nenhum vídeo nem fórum com tela de comunicado novo sobre o tema (buscas de YouTube sem resultado relevante).
- **Onde fica a N1:** o comunicado de out/2025 deve estar em Novidades da Central do vendedor (exige login). A etiqueta "Preço alto" aparece na tela de automação.

### 2. Padrão de reclamações de alimentos no ML (item 38)

**Fonte e limite.** Reclame Aqui, empresa "Mercado Livre" (id 928), busca pública por termo, ordenada da mais recente para a mais antiga. Lemos o título e o início do relato; não registramos nomes nem dados pessoais. Houve bloqueio 403 depois de ~7 consultas, em duas tentativas, e paramos.

| Busca | Total histórico de resultados | Janela das 30 mais recentes |
|---|---|---|
| "validade" | 4.480 | 10/10 a 15/10/2026 (~5 por dia; inclui "validade" de cupom, cosmético etc.) |
| "vencido" | 2.457 | 27/09 a 15/10/2026 (~1,6 por dia; inclui código de postagem vencido etc.) |
| "alimento vencido" | 9 | 2017 a 20/08/2026 |

**Reclamações de alimento ou suplemento na janela de 27/09 a 15/10/2026** (6 em 63 registros únicos):

| Data | Produto | Padrão |
|---|---|---|
| 15/10/2026 | barrinhas de proteína | embalagem inadequada (caixa reaproveitada) e validade não identificada |
| 15/10/2026 | colágeno | vencido (compra de 10/08) |
| 14/10/2026 | creatina | validade curta (vence em 12/12); vendedor havia respondido sobre a validade no anúncio; reembolso negado |
| 14/10/2026 | tomate pelado em lata | data de validade com sinais de adulteração (lote de 2023); reembolso imediato |
| 13/10/2026 | leite UHT (6 caixas) | avaria (amassadas) e validade abaixo de 30 dias; devolução recusada |
| 06/10/2026 | whey 900 g | validade de "alguns dias"; só ofereceram devolução |

Endereços (prefixo `https://www.reclameaqui.com.br/mercado-livre/`):
- `produto-alimenticio-sem-identificacao-de-validade-e-atendimento-inadequado-ao-consumidor_wplEXqFUy1fRZGNV`
- `recebi-colageno-vencido-e-quero-meu-dinheiro-de-volta_M9vKOVidZUCoC78a`
- `recebi-creatina-perto-do-vencimento-e-o-mercado-livre-negou-meu-reembolso_5RQxBUYglVIiCV5w`
- `comprei-tomates-pelados-cirio-com-validade-adulterada_cbuiJmT8RtrWzBns`
- `comprei-leite-amassado-e-com-validade-curta-e-nao-aceitam-devolucao_esf7XGd4CVHPYb0A`
- `whey-enviado-com-validade-extremamente-proxima-ao-vencimento_HmOjGPltw7AJ6JI6`

**Casos mais antigos achados nas mesmas buscas:**
- 20/08/2026: whey com sabor alterado.
- 11/05/2026: balde de chocolate de loja oficial, vencido havia cerca de 9 meses.
- 17/03/2026: pasta de castanha vencida, com devolução exigida.
- 07/02/2026: farinha de outra marca, a 11 dias do vencimento. Produto diferente e validade curta.
- Também: 15/04/2025 (salgadinho vencido), 16/11/2024 (biscoito com data adulterada), 23/07/2024 (papinha vencida).

**Padrões (por frequência na amostra):**
1. **Validade curta ou vencido:** 5 dos 6 recentes e quase todos os antigos.
2. **Exigência de devolução física para reembolso de alimento vencido:** recorrente (farinha, pasta de castanha, whey, leite). Aparece também nos medicamentos veterinários.
3. **Data adulterada ou etiqueta sobreposta:** tomate (2026), biscoito (2024). Fora de alimentos: cosmético com duas validades.
4. **Avaria:** leite amassado.
5. **Produto diferente:** farinha de outra marca.
6. **Atraso:** a busca por termo não trouxe atraso ligado a alimento. No total do ML (todas as categorias e todo o histórico), "Atraso na entrega" tem 138.697 reclamações, "Produto errado" 23.650, "Encomendas danificadas" 5.349 e "Produtos divergentes" 363.

**Contexto de volume** (índice do próprio Reclame Aqui, lido em 2026-10-15): 199.069 reclamações de abr a set/2026; 37.866 nos últimos 30 dias; 77,1% resolvidas; nota 7,7. Não há categoria "Alimentos" entre as categorias do Reclame Aqui para o ML. Por isso, a contagem por alimento só sai por termo e é aproximada.

**Leitura.**
- A taxa de alimentos é baixa em relação ao total (cerca de 2 por semana nas buscas "vencido" e "validade", contra cerca de 8.800 reclamações por semana no total).
- O padrão dominante é qualitativo: validade, e não atraso.
- Isso conversa com duas regras oficiais: a recusa no Full de itens de consumo recorrente com validade próxima (ajuda/5200) e a necessidade de devolução física para estorno.
- Não há página pública do ML com taxa de reclamação por categoria.

### 3. Outros sinais de regra dos últimos 60 dias (N8; só levantam pergunta)
- **Experiência de compra herdada da categoria:**
  - fluxo citado como oficial em ZYce3H1naP4 (04/09/2026, de ~9:00 a ~11:00): com mais de 100 vendas em 60 dias, vale a experiência do item; se não, vale a da categoria, se ela tiver mais de 200 vendas em 60 dias; senão, fica "sem experiência".
  - coerente com 9GJUi32R5sc (10/09/2026, tela) e com REP A20.
- **Indisponibilidade regional e multiestoque:**
  - JziHF-pCCtU (23/09/2026): anúncios "não é possível enviar para a localização", concentrados no RS e em SC; o suporte reconheceu o problema.
  - w2izIQTFXi0 (01/10/2026): cerca de duas semanas sem vendas para o RS, sem aviso; falha no multiestoque (Full, Flex e agência no mesmo anúncio).
- **Capacidade de envio configurada automaticamente; reagendamento do Flex afeta a reputação; coleta exigida no sábado:** w2izIQTFXi0 (01/10/2026).
- **Bebidas alcoólicas:**
  - w2izIQTFXi0 (01/10/2026, ~10:30): só vendedor autorizado; estoque no Full com poucos dias para retirada.
  - A ajuda/5200 confirma só que bebidas "que não cumprem os regulamentos" são proibidas no Full.
  - Precedente de imprensa: suspensão de destilados em 07/10/2025 (Times Brasil, Mercado&Consumo).
- **Supermercado "produtos selecionados" com tarifa menor; Full mais caro para quem não gira; Flex com pagamento variável por tamanho e peso; envio de faltantes; promoções em formato de hub:** Mj-oOzE0ZuE (02/09/2026, e-mails oficiais na tela). O primeiro item conversa com ALIM A7 e com a lista de selecionados ainda não lida.

---

## Tabela de afirmações novas

| id | Afirmação | Tipo | Fonte | Data da fonte | Confiança | Fecha |
|---|---|---|---|---|---|---|
| R2-SIN-1 | Desde 10/09 (2026), quem tem 101 ou mais vendas concluídas em 60 dias é medido em 60 dias; com menos, em 365 dias; antes o corte era 60 | OFICIAL | vendedores.mercadolivre.com.br/aprender/nota/vamos-mudar-a-forma-como-calculamos-sua-reputacao; ajuda/866 | nota s/d (vigência 10/09); ajuda s/d; acesso 2026-10-15 | alta | REP A2; LACUNAS #16, #37 |
| R2-SIN-2 | Na medição de 365 dias: canceladas verde até 2,5% (60 dias: 1,5%); envios incorretos verde até 13% (60 dias: 10%); faixas completas na tabela §1.1 | OFICIAL | mesma nota | s/d (vigência 10/09/2026) | alta | REP A4 (tabela de 365 dias) |
| R2-SIN-3 | Reclamações: verde até 2%, amarelo 2–4,5%, laranja 4,5–8%, vermelho > 8%, iguais nos dois períodos | OFICIAL | mesma nota | s/d | alta | REP A4 |
| R2-SIN-4 | "68 vendas" é erro de fonte; nenhuma página oficial traz 68. Developers ainda mostra 60 (página de 11/08/2025) | OFICIAL (ausência) + PRÁTICA | i9MQ51OkODg (21/08/2026); developers/reputacao-de-vendedores | 21/08/2026; 11/08/2025 | alta | divergência 101/68/60 |
| R2-SIN-5 | No Brasil, o "Benefício de Reputação" (`RECOVERY_GRNTEE`) tem como termos a ajuda/29528, intitulada "Termos e condições da Reputação Protegida": é o mesmo programa | OFICIAL (inferência por link e id) | developers.mercadolivre.com.br/pt_br/recuperacao-de-reputacao; ajuda/29528 | 04/02/2025; s/d | média-alta | REP §9.3; LACUNAS #18 |
| R2-SIN-6 | Reputação Protegida: garantia de 1–3% do faturamento de 60 dias, até 60 dias, reativação a cada 6 meses se acabar pelo limite, liberação em 10 dias; aceita verde ou Líder com publicações em amarelo ou vermelho | OFICIAL | ajudas 29528 e 29276 | s/d | alta | REP A22, A23 |
| R2-SIN-7 | Os valores R$75 a R$250 mil e 120 dias não aparecem em nenhuma página oficial atual; não usar | OFICIAL (ausência) | ajudas 29528 e 29276; developers | — | média | REP A23 (rebaixa) |
| R2-SIN-8 | Em set–out/2026 o ML oferece a Reputação Protegida a contas verdes (ex.: R$21.250 por 60 dias, limite de 855 vendas afetadas, 100% devolvido com 0–170 afetadas e 80% com 171–341) | PRÁTICA (tela) | PbU19wAcBlw ~0:30–6:00; w2izIQTFXi0 ~1:00 | 05/10/2026; 01/10/2026 | média | REP §9.3 |
| R2-SIN-9 | Desconto de envio por reputação: verde até 50%, amarela até 40%, laranja ou vermelha sem desconto, já embutido na tabela | OFICIAL | ajudas 40538, 40545, 40547 | s/d (acesso 2026-10-15) | alta | REP A15; PRE A5 |
| R2-SIN-10 | O "até 70%" (tabela logada, mai/2026) não aparece em nenhuma página pública atual; considerar superado | PRÁTICA + OFICIAL (ausência) | 8dZiKLuJWXg ~2:00 | 28/05/2026 | média | PRE A5 |
| R2-SIN-11 | A nota "Como funcionam as taxas" segue publicada com custo fixo de 50% abaixo de R$12,50 e 3 faixas até R$79; o vídeo de maio é leitura dessa mesma nota | OFICIAL (sem data, possível desatualização) | vendedores.mercadolivre.com.br/nota/como-funcionam-as-taxas-do-mercado-livre | s/d | média | MIX R12, A37 (fonte única, não dupla) |
| R2-SIN-12 | As ajudas 870 e 40538 (atuais) não falam em custo fixo; abaixo de R$79 só há faixas de envio (abaixo de R$19, no máximo metade do preço) | OFICIAL | ajuda/870; ajuda/40538 | s/d | alta | PRE §2; MIX R12 (contradição oficial interna) |
| R2-SIN-13 | Extragrandes restritos ao Full: igual ou maior que 20 kg, lado igual ou maior que 80 cm ou volume igual ou maior que 125 L; exceção se o preço for igual ou maior que o mínimo da subcategoria (R$100 ou R$200, ou "Sem exceção") | OFICIAL | ajuda/44922 | s/d | alta | LOG R6, A9 |
| R2-SIN-14 | Nenhuma subcategoria de Alimentos, Bebidas ou Supermercado está na lista de extragrandes; Ração para cães e gatos está, "Sem exceção" | OFICIAL | ajuda/44922 | s/d | alta | LOG R6 (impacto por categoria) |
| R2-SIN-15 | O metadado da ajuda/44922 diz "Produtos restritos ao Full a partir de 15 de outubro", o que sugere uma onda nova; 20/05/2026 só em terceiros | OFICIAL (metadado) + PRÁTICA | ajuda/44922 (HTML); hz-H-lBm390; upseller.com/pt/blog-article-838 | s/d; 23/04/2026; 26/05/2026 | baixa (data) | LOG R6 (data) |
| R2-SIN-16 | A ajuda/5200 proíbe no Full, sem condição de tamanho, assadeiras, cabides, copos e taças, mops etc.; lista anunciada em 03/09 com vigência em 16/09/2026 (vídeo) | OFICIAL (lista) + PRÁTICA (data) | ajuda/5200; ZYce3H1naP4 ~0:40 | s/d; 04/09/2026 | alta (lista), média (data) | LOG §9.4 |
| R2-SIN-17 | Comparação com preços externos é oficial: referências de preço com base em concorrentes "internos ou externos" e automação "dentro e fora" com Google | OFICIAL | developers/referencias-de-precos; nota venda-mais-com-ajustes-automaticos-de-preco | 17/12/2025; s/d | alta | CASES A3 (parte) |
| R2-SIN-18 | Aviso, prazo de 3 dias e perda de visibilidade, campanhas e Ads por preço externo seguem só na imprensa (desde 23/10/2025); nenhum comunicado novo nos últimos 60 dias | OFICIAL via terceiro | mercadoeconsumo.com.br 24/10/2025; gironews | 24/10/2025 | média | CASES A3 (sem mudança) |
| R2-SIN-19 | Reclame Aqui, ML: "validade" tem 4.480 resultados; "vencido" 2.457; as 30 mais recentes de "vencido" cobrem 27/09–15/10/2026 | DADO (N8) | iosearch.reclameaqui.com.br (busca pública, empresa 928) | acesso 2026-10-15 | média | LACUNAS #38 |
| R2-SIN-20 | Na janela de 27/09–15/10/2026, 6 reclamações de alimento ou suplemento: validade curta (3), vencido (1), data adulterada (1), avaria e validade curta (1), embalagem inadequada (1, sobreposta) | DADO (N8) | Reclame Aqui, endereços na §2 | 06–15/10/2026 | média (amostra pequena) | REP Q6; ALIM Q2 |
| R2-SIN-21 | Padrão recorrente: o comprador de alimento vencido precisa devolver o produto para receber o estorno (farinha 02/2026, pasta de castanha 03/2026, whey 10/2026, leite 10/2026) | DADO (N8) | Reclame Aqui | 2026 | média | REP Q6 |
| R2-SIN-22 | "Atraso" não aparece ligado a alimento nas buscas por termo; no total do ML, "Atraso na entrega" = 138.697, "Produto errado" = 23.650, "Encomendas danificadas" = 5.349 (todas as categorias) | DADO (N8) | Reclame Aqui (facetas) | acesso 2026-10-15 | média | LACUNAS #38 |
| R2-SIN-23 | Volume do ML no Reclame Aqui: 199.069 reclamações de abr a set/2026; 37.866 em 30 dias; 77,1% resolvidas; nota 7,7 | DADO | Reclame Aqui (índice SIX_MONTHS) | período 01/04–30/09/2026 | alta | contexto §2 |
| R2-SIN-24 | Ajuda/5200: o Full recusa consumo recorrente com validade próxima e exige validade legível, no idioma do país e não manuscrita; Supermercado só para vendedores autorizados | OFICIAL | ajuda/5200 | s/d | alta | ALIM §2.4; LOG Q8 (parte) |
| R2-SIN-25 | Experiência de compra: item com mais de 100 vendas em 60 dias usa a própria; senão herda a da categoria, se ela tiver mais de 200 vendas em 60 dias; senão fica "sem experiência" | PRÁTICA (fluxograma descrito como oficial) | ZYce3H1naP4 ~9:00–11:00 | 04/09/2026 | média-baixa | RANK A9; REP A20 |
| R2-SIN-26 | Set/2026: anúncios indisponíveis para RS e SC (cerca de 2 semanas, sem aviso) e falha no multiestoque | PRÁTICA (N8) | JziHF-pCCtU; w2izIQTFXi0 | 23/09/2026; 01/10/2026 | baixa | sinal (sem lacuna) |
| R2-SIN-27 | Restrição nova de bebidas alcoólicas (só autorizados; estoque no Full a retirar em poucos dias) | PRÁTICA (N8) | w2izIQTFXi0 ~10:30; precedente de 07/10/2025 (timesbrasil.com.br) | 01/10/2026 | baixa | ALIM (novo) |
| R2-SIN-28 | Supermercado ganhou "produtos selecionados" com tarifa menor; Full mais caro para baixo giro; Flex com pagamento variável por tamanho e peso (e-mails na tela) | PRÁTICA (tela) | Mj-oOzE0ZuE ~1:00–3:00 | 02/09/2026 | média-baixa | ALIM A7 (parte) |
| R2-SIN-29 | Aumento do custo de envio desde 24/08/2026, cerca de R$0,90 por envio, com e-mail oficial na tela | PRÁTICA (tela) | Mj-oOzE0ZuE ~0:30 | 02/09/2026 | média | PRE A7 |

---

## O que segue aberto e por quê

1. **Ano da vigência de 10/09 na nota de reputação.** A nota oficial não traz o ano. 2026 vem dos vídeos que leem o site em 02/09/2026 e da cronologia, mas não do texto oficial.
2. **Benefício = Protegida:** a equivalência é inferida pelo id 29528 e pelo tipo `RECOVERY_GRNTEE`. Falta uma frase oficial. O valor de R$75 a R$250 mil e os 120 dias só podem ser checados no painel logado (`/reputacao/beneficio_reputacao`, exige login).
3. **Custo fixo abaixo de R$79:** há duas páginas oficiais em vigor que se contradizem (nota com custo fixo contra ajudas 870 e 40538 sem custo fixo). Fechar exige a simulação logada ou a API `listing_prices` (LACUNAS #11).
4. **Datas das ondas do Full:** 20/05/2026 (extragrandes), 16/09/2026 (lista sem condição de tamanho) e o "15 de outubro" do metadado. As datas só estão em e-mail ou em Novidades da Central (exige login). As ajudas 44922 e 5200 não têm data no corpo.
5. **Preço externo:** não achamos o comunicado de out/2025 em nenhuma página pública. Também não há sinal de mudança nos últimos 60 dias. Fica [OFICIAL via terceiro].
6. **Desconto de 70%:** não sabemos se foi um erro da tabela logada ou uma regra trocada sem comunicado público.
7. **Reclamações de alimentos:**
   - amostra pequena (63 registros únicos), porque o Reclame Aqui bloqueou a busca (403) depois de ~7 consultas e não insistimos;
   - não há categoria "Alimentos" no Reclame Aqui para o ML, então a contagem por alimento é por termo e aproximada;
   - não há taxa por pedido;
   - não foram lidas as opiniões de produto do ML (exigem página por anúncio) nem o consumidor.gov.br;
   - próximo passo: repetir as buscas "café", "chocolate", "leite", "alimento", "amassada" e "violada" em outro dia, com pausa longa entre consultas.
8. **Sinais N8 da §3** (bebidas alcoólicas, capacidade automática, experiência por categoria, "produtos selecionados" de Supermercado): falta N1 escrito. Procurar em Novidades da Central (exige login) e nas ajudas de Supermercado (23329, 49972).
9. **Camada social além do YouTube:** TikTok e fóruns públicos de vendedores não foram varridos nesta frente. As buscas no YouTube trouxeram pouca coisa sobre preço externo, extragrandes e custo abaixo de R$79 nos últimos 60 dias.
