# Rodada 2 (navegador): tarifas, promoções, reputação e experiência de compra

Frente: nav-preco-reputacao. Ferramenta: Claude in Chrome, numa aba própria, aberta e fechada nesta sessão. Acesso em 2026-10-15. Pausa de 6 a 10 s entre páginas do mercadolivre.com.br. Não apareceu captcha. Não houve login, aceite de termos nem clique em ação. Lacunas atacadas: LACUNAS §4 itens 11, 14, 16 e 18; §1.2; §1.6.

## Resumo

- **Tarifa do café fechada (§4 item 11).** O buscador de categoria da landing oficial de custos dá, para Alimentos e Bebidas > Mercearia > Infusões > Café > Café Moído e em Grão, **Clássico 14% e Premium 19%**. É o teto das faixas 10–14% e 15–19%. A API `listing_prices` deixou de ser pública: devolve 403 sem token.
- **Corte da janela de reputação resolvido (§1.6, §4 item 16).** Uma nota oficial anuncia que, **a partir de 10 de setembro**, o corte para medir pelos últimos 60 dias passou de **60 para 101 vendas**. A ajuda/866 já mostra 101. A doc developers (11/08/2025) ainda mostra 60, porque é anterior à mudança. Nenhuma fonte oficial cita "68": o número do vídeo fica sem respaldo.
- **Faixas de 365 dias publicadas em fonte oficial.** A mesma nota traz as faixas de cada cor para medição em 365 dias, por variável. Isso fecha "só via Terazi".
- **Benefício de Reputação contra Reputação Protegida (§4 item 18).** A doc developers define o Benefício (RECOVERY_GRNTEE) para reputação vermelha, laranja ou amarela, com valor em garantia e nível congelado em verde. O link "Termos e Condições: Brasil (MLB)" dessa doc leva à **ajuda/29528**, cujo título é "Termos e condições da **Reputação Protegida**". A ligação oficial sugere que, no Brasil, os dois nomes apontam para o mesmo regulamento, mas isso não é dito com todas as letras. Os valores de R$75 a R$250 mil e o prazo de 120 dias **não aparecem** em nenhuma página oficial lida. A Protegida vale 60 dias corridos, com garantia de 1% a 3% do faturamento de 60 dias.
- **Experiência de compra.** A nota oficial confirma a janela 60/365: 100 vendas do anúncio em 60 dias, ou 200 vendas na categoria. Os "180 dias" da doc developers (03/02/2026) são a janela das **vendas com problema exibidas** na API e nas telas. Esse número não aparece como período de cálculo da nota. A divergência fica parcialmente explicada.
- **Promoções e automação reconferidas (§4 item 14).** São 12 tipos de promoção, com a tabela de quem define o preço, quem tem bonificação do ML, prazo e aprovação. Há campos `meli_percentage` e `seller_percentage`, que separam o aporte de cada lado (toca §1.2 Q6). Há um "boost" automático do ML, compensado em redução de custos por venda. PRICE_MATCHING é cofinanciado e PRICE_MATCHING_MELI_ALL é 100% ML; o prazo máximo é de 10 dias (SMART: 30). A automação INT/INT_EXT tem piso obrigatório, validação contra 60 dias, bloqueio por API desde 18/03/2026 e pausa ao entrar em promoção.
- **Envio abaixo de R$79.** A tabela completa da ajuda/40538 foi relida: degraus de R$0–18,99, R$19–48,99 e R$49–78,99 por peso, com teto de metade do preço abaixo de R$19. O "custo fixo" de R$12,50 só aparece na nota educativa, que não dá os valores das três faixas intermediárias. A ajuda/870 não fala mais em custo fixo.

## Achados por item

### Item 11: tarifa por categoria (café) e 51251
- A landing `vendedores.mercadolivre.com.br/landing/custos-de-venda` tem um buscador. Consultei "café moído", que retornou a categoria "Café Moído e em Grão": Clássico **14%**, Premium **19%**. Nota da página: o Premium é "composto pela tarifa ... mais a taxa por oferecer parcelamento sem juros". Página sem data. [OFICIAL], confiança alta.
- O id da categoria vem da API pública `domain_discovery`: `MLB247538`, domínio `MLB-GROUND_AND_WHOLE_BEANS_COFFEE`. [OFICIAL], alta.
- `api.mercadolibre.com/sites/MLB/listing_prices?price=..&category_id=MLB247538` devolveu **403 PA_UNAUTHORIZED_RESULT_FROM_POLICIES** em todos os preços testados (R$10 a R$200). A rota exige autenticação. [OBS], alta.
- A tabela 51251 (Café: −5 p.p. no Premium e −3 p.p. no Clássico entre R$150 e R$700) já estava CONFIRMADA na verificação [pre R6]. Não foi reaberta. A ajuda/870 repete a regra e acrescenta: "Os produtos da seção Supermercado pagam outras tarifas", com link para a ajuda/16449.
- Combinando as duas fontes: café em grão ou moído entre R$150 e R$700 pagaria 11% no Clássico e 14% no Premium. Isso é inferência aritmética, sem página que mostre o valor final.
- Não consegui consultar a categoria de cápsulas: o buscador não retornou sugestão.

### Item 14: promoções, price matching, cupons, automação
- **gerenciar-ofertas** (developers, 09/06/2026):
  - Lista 12 tipos: DEAL, MARKETPLACE_CAMPAIGN, PRICE_DISCOUNT, LIGHTNING, DOD, VOLUME, PRE_NEGOTIATED, SELLER_CAMPAIGN, SMART, PRICE_MATCHING, UNHEALTHY_STOCK, SELLER_COUPON_CAMPAIGN.
  - Tabela "Características": têm bonificação do ML MARKETPLACE_CAMPAIGN, VOLUME, PRE_NEGOTIATED, SMART, PRICE_MATCHING e UNHEALTHY_STOCK. Não têm DEAL, DOD, LIGHTNING e SELLER_CAMPAIGN. LIGHTNING exige estoque.
  - Campos `meli_percentage` ("aportada pelo Mercado Livre") e `seller_percentage`.
  - Aviso novo: o ML "pode aplicar um desconto automático sobre a oferta base". O valor é compensado como redução nos custos por venda, pelos campos `boosted_offer` e `discount_meli_boost_amount`.
  - [OFICIAL], alta. Fecha [pre A14–A16, R10] e responde em parte à §1.2 Q6: no nível do item a API separa subsídio do ML e desconto do vendedor. Não há agregado público.
- **campanhas-smart-price-matching** (09/06/2026):
  - SMART e PRICE_MATCHING: o ML "assume uma porcentagem do desconto". Os candidatos mudam diariamente.
  - PRICE_MATCHING é cofinanciado; PRICE_MATCHING_MELI_ALL é "100% financiado pelo Mercado Livre".
  - Duração máxima de 30 dias (SMART) e 10 dias (preço competitivo).
  - Confirma o veredito CONTESTADA de [pre R11] ("sempre cofinanciado" é falso). [OFICIAL], alta.
- **cupons-do-vendedor**: já CONFIRMADA [pre R12] (28/08/2025). Não foi reaberta.
- **automatizacoes-de-precos** (developers, 01/10/2026):
  - Regras INT_EXT ("dentro e fora do Mercado Livre") e INT. `min_price` obrigatório.
  - Erro "unusual value" quando o piso ou o teto fica anômalo diante de vendas e preços "dos últimos 60 dias".
  - Desde 18/03/2026, PUT de preço em item automatizado é rejeitado (400) ou ignorado.
  - A automação pode render a etiqueta "Recomendado" e a distinção VIP.
  - "Quando um item ... entra em uma promoção, a automatização é pausada" (causas COMPETITORS, PROMO, ITEM_NO_ACTIVE).
  - No catálogo, a automação exige reputação amarela, verde-clara ou verde, item novo e produto com "oportunidades".
  - Tag `dynamic_standard_price`.
  - [OFICIAL], alta. Fecha [pre A23] e o item "não reconferida" de §1.2.

### Item 16 e §1.6: janela da experiência de compra e corte de reputação
- **Nota "vamos-mudar-a-forma-como-calculamos-sua-reputacao"** (Central de vendedores, sem ano visível; o texto diz "a partir de 10 de setembro"):
  - "Hoje ... você precisa ter 60 vendas ou mais nesse período. Com a mudança, esse número sobe para 101 vendas."
  - Com menos de 101 vendas nos últimos 60 dias, a medição é pelos últimos 365 dias.
  - Os limites de 60 dias não mudam. A tabela nova de 365 dias, por variável, vem a seguir:

| Variável | Verde | Amarelo | Laranja | Vermelho |
|---|---|---|---|---|
| Canceladas por você (60 d) | até 1,5% | 1,5–3,5% | 3,5–4% | >4% |
| Canceladas por você (365 d) | até 2,5% | 2,5–5,5% | 5,5–6,5% | >6,5% |
| Envios incorretos (60 d) | até 10% | 10–18% | 18–22% | >22% |
| Envios incorretos (365 d) | até 13% | 13–23,5% | 23,5–28,5% | >28,5% |
| Reclamações (qualquer janela) | até 2% | 2–4,5% | 4,5–8% | >8% |

  - "Para a variável de reclamações, o percentual não muda."
  - [OFICIAL], alta. O ano 2026 é inferido do contexto (vídeo "desde 10/09/2026" e nota viva). Confiança média-alta para o ano.
- **ajuda/866** (sem data): "Se você atingir ou superar 101 vendas concluídas ... últimos 60 dias"; abaixo disso, 365 dias. A reputação só começa após 10 vendas em 365 dias. [OFICIAL], alta.
- **developers reputacao-de-vendedores** ("Última atualização em 11/08/2025"): "Para MLB > ou = a 60 vendas", últimos 60 dias. Está **desatualizada** em relação à nota e à 866. [OFICIAL], alta para o texto e baixa como regra vigente.
- **"68 vendas"**: não aparece em nenhuma das três fontes oficiais. É provável erro do vídeo [rep A2; cases A26]. [OBS] por ausência, confiança média.
- **ajuda/864** (MercadoLíder, sem data): mede os "3 meses mais os dias do mês vigente":
  - 230, 575 ou 1.725 vendas e R$37.000, R$118.400 ou R$296.000 de faturamento (Líder, Gold, Platinum).
  - Reclamações abaixo de 1%, mediadas abaixo de 0,5%, canceladas abaixo de 0,5%, envios incorretos abaixo de 6%.
  - Mais de 4 meses de cadastro.
  - [OFICIAL], alta. Reconfere [cases A25].
- **Nota "como-proporcionar-a-melhor-experiencia-de-compra"** (sem data):
  - "Se o seu anúncio atingir 100 vendas totais em um período de 60 dias", usa essas operações; senão, usa "o último ano".
  - Com menos de 100 vendas, complementa com os outros anúncios da categoria, desde que somem 200 vendas. Sem isso, o anúncio fica sem Experiência.
  - O infográfico mostra 100 Boa, 65 Média e 30 Ruim. O texto dá Boa 75–100, Mediana 50–74 e Ruim 30 ou menos.
  - [OFICIAL], alta.
- **developers experiencia-de-compra** ("Última atualização em 03/02/2026"):
  - Os "180 dias" aparecem como contagem das "vendas com problemas nos últimos 180 dias" exibidas no front (`central_tag`, `empty_state_title`).
  - Score −1 = item sem vendas.
  - Tipos de congelamento ("freeze") incluem um de "Beneficio de reputación" (`Internal_newbie_grntee`) e "Beneficio Verde claro". Com eles a publicação "não perderá exposição, nem será pausada" por experiência ruim ou média.
  - Leitura: o período de cálculo é 60/365 (nota); 180 dias é a janela de exibição de problemas na API. A divergência [rank A9] fica rebaixada para "janelas com funções diferentes", sem frase oficial que diga isso. [OFICIAL], média.

### Item 18: Benefício de Reputação contra Reputação Protegida
- **developers recuperacao-de-reputacao** ("Programa Decola e Benefício de Reputação", 04/02/2025):
  - Decola (NEWBIE_GRNTEE) é para quem não tem reputação.
  - Benefício de Reputação (RECOVERY_GRNTEE) é para 1_red, 2_orange ou 3_yellow.
  - O nível fica "congelado em verde" por um período. O vendedor deixa "uma quantia de dinheiro como garantia" e recebe de volta parte ou tudo conforme reclamações, cancelamentos e atrasos.
  - Termos do Brasil: Decola → ajuda/33285; Benefício → **ajuda/29528** (slug `termos-e-condicoes-reputacao-vantagens`).
  - [OFICIAL], alta.
- **ajuda/29528** (título "Termos e condições da Reputação Protegida", sem data):
  - Exige reputação amarela, laranja ou vermelha, ou verde ou Líder com anúncios em amarelo ou vermelho.
  - Valor de 3% do faturamento de 60 dias (vermelho ou laranja), 2% (amarelo) ou 1% (verde).
  - Prazo de **60 dias corridos**, ou até cancelar ou atingir o limite de vendas afetadas.
  - Reativação só após 6 meses quando encerrada por limite.
  - Aparece "verde claro". Saldo liberado 10 dias corridos após o fim.
  - "O Mercado Livre pode disponibilizar ... apenas para Vendedores específicos".
  - [OFICIAL], alta. Reconfere [rep A22] e fecha "A Protegida só pode ser reativada 6 meses depois", que antes vinha [OFICIAL via terceiro].
- **ajuda/866**: "Caso queira conquistar ou proteger a cor verde ..., você pode ativar Reputação Protegida". Não cita "Benefício de Reputação".
- **Conclusão:** a documentação oficial liga o Benefício de Reputação aos termos da Reputação Protegida. Não achei página oficial com R$75 a R$250.000 nem com 120 dias. A coexistência como dois produtos distintos **não tem suporte oficial**, e a hipótese de que são o mesmo programa no Brasil tem suporte indireto (o link). A página `/reputacao/beneficio_reputacao` segue exigindo login.
- A busca na Central (`vendedores.mercadolivre.com.br/busca?q=...`) redirecionou para o painel logado ("Resumo"). Não li nada dele e saí na hora. Registro: exige login.

### §1.2: envio abaixo de R$79 e desconto por reputação
- **ajuda/40538** (sem data), relida por completo:
  - "Até 50% de desconto nos seus custos por ter reputação verde". A tabela já inclui o desconto.
  - Frete grátis padrão de R$19 a R$78,99, pago pelo ML. Frete grátis rápido a partir de R$79, pago pelo vendedor. Abaixo de R$79 é opcional.
  - Exemplo de degraus para café de 0,5–1 kg: **R$6,05** (R$0–18,99), **R$7,15** (R$19–48,99), **R$8,45** (R$49–78,99), **R$14,45** (R$79–99,99).
  - Para 1–1,5 kg: R$6,15, R$7,35, R$8,65 e R$14,75.
  - "*Os produtos de menos de R$ 19 pagam no máximo metade do preço"; kit paga um único custo.
  - Exceções com tabela própria: Full Super, Livros, categorias especiais, alimento de animais e usados.
  - [OFICIAL], alta. Os 70% do vídeo de maio não têm respaldo na página atual.
- **Custo fixo**: a nota "como-funcionam-as-taxas-do-mercado-livre" (texto recolhido) mantém "menor que R$ 12,50, o custo fixo será de 50%" e "três faixas" entre R$12,50 e R$79, sem os valores. A ajuda/870 e a landing de custos **não citam** custo fixo; mostram só tarifa percentual e custo de envio. Leitura: o custo fixo da nota pode estar superado pela tabela de envio (a coluna R$0–18,99 tem teto de 50% do preço). [OFICIAL] para o texto, confiança média para a vigência.
- **ajuda/44007**: o valor estimado por venda não inclui publicidade, custos do Full nem a tarifa de "Minha página". O ML não retém impostos. [OFICIAL], alta.

## Tabela de afirmações novas

| id | afirmação | tipo | fonte | data | confiança | fecha |
|---|---|---|---|---|---|---|
| R2-PR-1 | Café Moído e em Grão (MLB247538): Clássico 14%, Premium 19% | OFICIAL | vendedores.mercadolivre.com.br/landing/custos-de-venda (buscador de categoria) | sem data; acesso 2026-10-15 | alta | §1.2 Q1; §4 item 11; pre §9.1, A8 |
| R2-PR-2 | `listing_prices` exige autenticação (403 PolicyAgent); `domain_discovery` segue pública | OBS | api.mercadolibre.com/sites/MLB/listing_prices; /domain_discovery/search | acesso 2026-10-15 | alta | §4 item 11 (rota alternativa) |
| R2-PR-3 | Café entre R$150 e R$700 ficaria em cerca de 11% (Clássico) e 14% (Premium), combinando R2-PR-1 com 51251 | OBS (inferência) | landing custos + ajuda/51251 [pre R6] | acesso 2026-10-15 | média | §1.2 Q1 |
| R2-PR-4 | Corte da janela de reputação: 60 → 101 vendas "a partir de 10 de setembro"; abaixo disso, 365 dias | OFICIAL | vendedores.mercadolivre.com.br/aprender/nota/vamos-mudar-a-forma-como-calculamos-sua-reputacao | 10/09 (ano inferido 2026); acesso 2026-10-15 | alta | §1.6 "101 x 68 x 60"; rep A2; cases A26; §4 item 16 |
| R2-PR-5 | Developers ainda mostra 60 vendas para MLB (11/08/2025): desatualizada | OFICIAL | developers.mercadolivre.com.br/pt_br/reputacao-de-vendedores | 11/08/2025 | alta | idem R2-PR-4 |
| R2-PR-6 | "68 vendas" não aparece em fonte oficial | OBS (ausência) | 866, nota de mudança, developers | acesso 2026-10-15 | média | rep A2 |
| R2-PR-7 | Faixas por cor em 365 dias: canceladas 2,5/5,5/6,5%; envios incorretos 13/23,5/28,5%; reclamações 2/4,5/8% em qualquer janela | OFICIAL | nota "vamos-mudar..." | idem | alta | §1.6 "faixas de 365 dias só via Terazi" |
| R2-PR-8 | Experiência de compra: 100 vendas do anúncio em 60 dias, senão o último ano; abaixo de 100, complementa com a categoria (mínimo de 200) | OFICIAL | vendedores.mercadolivre.com.br/nota/como-proporcionar-a-melhor-experiencia-de-compra | sem data | alta | rank A9; §4 item 16 |
| R2-PR-9 | Os "180 dias" da developers são a janela das vendas com problema exibidas; score −1 = sem vendas | OFICIAL | developers.mercadolivre.com.br/pt_br/experiencia-de-compra | 03/02/2026 | média | rank A9 (rebaixa a divergência) |
| R2-PR-10 | Congelamentos ("Benefício de reputação", "Verde claro") impedem perda de exposição e pausa por experiência ruim ou média | OFICIAL | developers experiencia-de-compra | 03/02/2026 | alta | rep §2.4 (freeze) |
| R2-PR-11 | Benefício de Reputação (RECOVERY_GRNTEE) é para vermelho, laranja ou amarelo, com garantia em dinheiro e nível congelado em verde; os termos do Brasil apontam para a ajuda/29528 | OFICIAL | developers.mercadolivre.com.br/pt_br/recuperacao-de-reputacao | 04/02/2025 | alta | §1.6 Benefício; §4 item 18 |
| R2-PR-12 | A ajuda/29528 se chama "Reputação Protegida": 1–3% do faturamento de 60 dias, 60 dias corridos, reativação após 6 meses se encerrada por limite, saldo após 10 dias | OFICIAL | mercadolivre.com.br/ajuda/29528 | sem data | alta | rep A22; rep §2.5 (reativação, antes via terceiro) |
| R2-PR-13 | R$75–250 mil e 120 dias do Benefício: sem fonte oficial; coexistência com a Protegida sem suporte, com indício de que são o mesmo regulamento | OBS | R2-PR-11 + R2-PR-12 | acesso 2026-10-15 | média | §1.6; §4 item 18 (parcial) |
| R2-PR-14 | Reputação só a partir de 10 vendas em 365 dias; MercadoLíder: 230/575/1.725 vendas e R$37 mil/118,4 mil/296 mil em 3 meses mais o mês vigente | OFICIAL | ajuda/866; ajuda/864 | sem data | alta | reconciliação §1.9 (cases A25–A26) |
| R2-PR-15 | 12 tipos de promoção; bonificação do ML em MARKETPLACE_CAMPAIGN, VOLUME, PRE_NEGOTIATED, SMART, PRICE_MATCHING e UNHEALTHY_STOCK | OFICIAL | developers.mercadolivre.com.br/pt_br/gerenciar-ofertas | 09/06/2026 | alta | pre A14–A16, R10; §1.2 Q5 |
| R2-PR-16 | API separa `meli_percentage` e `seller_percentage` por item; "boost" automático do ML compensado como redução de custos por venda | OFICIAL | gerenciar-ofertas; campanhas-smart-price-matching | 09/06/2026 | alta | §1.2 Q6 (parcial) |
| R2-PR-17 | PRICE_MATCHING é cofinanciado, PRICE_MATCHING_MELI_ALL é 100% ML; prazo de 10 dias (preço competitivo) e 30 dias (SMART); candidatos mudam diariamente | OFICIAL | campanhas-smart-price-matching | 09/06/2026 | alta | pre R11 (mantém CONTESTADA) |
| R2-PR-18 | Automação INT/INT_EXT: piso obrigatório, validação contra 60 dias, bloqueio de preço por API desde 18/03/2026, pausa ao entrar em promoção, etiqueta "Recomendado"; no catálogo exige reputação amarela ou melhor | OFICIAL | developers.mercadolivre.com.br/pt_br/automatizacoes-de-precos | 01/10/2026 | alta | pre A23; §1.2 "automação não reconferida" |
| R2-PR-19 | Tabela de envio com degraus abaixo de R$79 (R$0–18,99, R$19–48,99, R$49–78,99) e "até 50%" por reputação verde; abaixo de R$19, teto de metade do preço | OFICIAL | mercadolivre.com.br/ajuda/40538 | sem data | alta | §1.2 "50% x 70%"; "custo fixo abaixo de R$79" |
| R2-PR-20 | "Custo fixo" (abaixo de R$12,50 = 50%, três faixas até R$79) só na nota educativa, sem valores; ajuda/870 e landing não o citam | OFICIAL | nota como-funcionam-as-taxas; ajuda/870; landing | sem data | média | mix R12 (segue PARCIAL) |
| R2-PR-21 | O valor recebido por venda exclui publicidade, custos do Full e "Minha página"; o ML não retém impostos | OFICIAL | mercadolivre.com.br/ajuda/44007 | sem data | alta | §1.2 (conta unitária) |

## Aberto

- **Benefício de Reputação:** valores (R$75 a R$250 mil) e 120 dias sem fonte oficial. A página `/reputacao/beneficio_reputacao` e a busca da Central exigem login. Falta uma frase oficial que diga se Benefício e Protegida são o mesmo programa.
- **Ano da mudança de 10 de setembro:** a nota não mostra o ano. Inferido 2026.
- **Custo fixo de R$12,50 a R$79:** os valores das três faixas não estão em página escrita, e a vigência diante da tabela de envio não está confirmada.
- **Tarifa de cápsulas e de outras subcategorias de alimentos:** o buscador não retornou cápsulas. A tarifa da seção Supermercado (ajuda/16449) não foi reaberta nesta frente.
- **`listing_prices`:** só com token. A tarifa por faixa de preço e por tipo de anúncio fica dependente do buscador da landing.
- **Separação do subsídio (§1.2 Q6):** existe por item na API (exige login do vendedor). Não há agregado público.
- **Calendário de campanhas de 2026 e duração mínima de relâmpago e oferta do dia:** não foram procurados nesta frente.
- **Página 51251 e cupons:** já confirmadas na verificação; não foram reabertas.
