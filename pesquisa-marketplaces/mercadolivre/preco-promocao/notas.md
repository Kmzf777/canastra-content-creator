# Preço, tarifas e promoções no Mercado Livre (Brasil): nota do analista

Frente: preco-promocao. Data da nota: 2026-10-14. Plataforma central: Mercado Livre Brasil (MLB). Shopee e Amazon aparecem só como comparação.

**Como ler esta nota**
- Os tipos seguem o protocolo: [OFICIAL], [OFICIAL via terceiro], [PRÁTICA], [CASE], [DADO] e [OBS].
- As páginas da Central de Ajuda do ML **não exibem data**. Foram lidas ao vivo em 14/10/2026, com o HTML público baixado sem login. Pelo protocolo, regra sem data leva "(pode estar superada)", e essa marca vale para todas elas. Os valores lidos batem com vídeos de agosto e setembro de 2026, o que indica que estão vigentes.
- As páginas de developers.mercadolivre.com.br trazem a data de "Última atualização", e ela vai indicada em cada citação.
- **Lida com sucesso:** 13 páginas oficiais N1, 2 cartas a acionistas N2 (SEC 8-K), 15 transcrições e 1 arquivo de observação.
- **Não lidas:** a landing de custos e a tabela de tarifas por categoria pedem login, e por isso não foram abertas.
- **Limite de busca:** a cota de buscas na web acabou no fim da coleta. Por isso a camada de dados ficou mais curta do que o planejado (ver seção 9).

---

## 1. Resumo executivo

1. **A tarifa tem dois componentes por venda.**
   - **Tarifa de venda percentual:** Clássico de 10% a 14%, sem parcelamento; Premium de 15% a 19%, com até 12x sem juros.
   - **Custo de envio:** tabela por peso × faixa de preço, cobrado em **toda** venda, "mesmo que o comprador pague pelo envio".
   - Fontes: [OFICIAL] mercadolivre.com.br/ajuda/870 e /ajuda/40538, lidas em 14/10/2026 (pode estar superada).
2. **O antigo "custo fixo por unidade" abaixo de R$ 79 não aparece mais na página oficial.** Abaixo de R$ 79, o que existe hoje são faixas de custo de envio (R$ 0–18,99; 19–48,99; 49–78,99).
   - Exemplos até 0,3 kg: R$ 5,65, R$ 6,85 e R$ 8,15.
   - Abaixo de R$ 19, o custo é de "no máximo metade do preço do produto".
   - Fontes: [OFICIAL] /ajuda/40538. Os blogs ainda divergem (ver seção 6).
3. **A tabela de envio foi reajustada em 24/08/2026.** O aumento médio foi de cerca de 1,6% (≈ R$ 0,46), com algumas faixas em queda.
   - No Full Super, os "produtos selecionados" ficaram até ~20% mais baratos até 5 kg. Os demais subiram de 20% a 40%.
   - Fonte: [OFICIAL via terceiro] Bruno Gontijo, KvVyJlYt6w0, 12/08/2026. Os valores novos batem com /ajuda/40538 (ex.: R$ 6,85 até 0,3 kg na faixa de R$ 19–48,99).
4. **Desconto por reputação: a página oficial diz "até 50%"** para verde/MercadoLíder, já embutido na tabela. Um vídeo de maio/2026 citava "até 70%".
   - Fontes: [OFICIAL] /ajuda/40538; [PRÁTICA] 8dZiKLuJWXg, 28/05/2026.
5. **Frete grátis tem três faixas.** De R$ 19 a R$ 78,99, o ML oferece frete grátis padrão (lento). A partir de R$ 79, o vendedor oferece frete grátis rápido. Abaixo de R$ 79, o frete rápido é opcional e custa a partir de R$ 12,95. [OFICIAL] /ajuda/40538.
6. **Tarifa menor existe para quem é competitivo.**
   - Categorias selecionadas entre R$ 150 e R$ 700 têm redução em pontos percentuais. Em Alimentos e Bebidas (incluindo "Café Moído e em Grão"), a redução é de **5 pp no Premium e 3 pp no Clássico**. Fonte: [OFICIAL] /ajuda/51251.
   - Em abril/2026 o ML criou descontos de take rate para vendedores e desconto no PIX para compradores, **"condicionados a anúncios com preço competitivo"**. Fonte: [OFICIAL] carta Q2'26, SEC 8-K, 05/08/2026.
7. **A Central de Promoções reúne 12 tipos de promoção.** Para cada tipo, a documentação diz quem define o preço e se há "bonificação MELI".
   - Cofinanciadas: MARKETPLACE_CAMPAIGN, SMART e PRICE_MATCHING. Uma variante é 100% ML: PRICE_MATCHING_MELI_ALL.
   - Pagas só pelo vendedor: DEAL, PRICE_DISCOUNT, SELLER_CAMPAIGN, VOLUME do vendedor e cupons.
   - Fonte: [OFICIAL] developers "Gerenciar promoções", atualizado em 09/06/2026.
8. **O ML pode "turbinar" o desconto por conta própria** (boosted offer) em DEAL, PRICE_DISCOUNT, PRE_NEGOTIATED, SMART, PRICE_MATCHING e LIGHTNING. A compensação vem como redução equivalente nos custos por venda. Isso explica os prints de praticantes com "tarifa zerada" em oferta relâmpago. [OFICIAL] developers, 09/06/2026; [PRÁTICA] iAM5PWaVV08, 13/08/2026.
9. **A campanha "Saia na frente da concorrência" (price matching) usa preço de concorrentes externos.**
   - Os candidatos são recalculados todo dia. O opt-in dura 7 dias.
   - Se a diferença de preço diminui, o aporte cai sozinho. Se aumenta, a campanha cai e pede novo opt-in.
   - É sempre cofinanciada.
   - Fontes: [OFICIAL] webinar do time de pricing, W1hgC6snin4, 03/06/2026; developers, 09/06/2026.
10. **Segundo o time de pricing do ML, o desconto que mais converte é o que leva o preço de "mais caro" para "igual ou mais barato" que a referência do comprador** (o "efeito qualitativo"), e não o percentual em si. Dado interno, sem números publicados. [OFICIAL] W1hgC6snin4.
11. **Na buy box de catálogo, o algoritmo pondera** preço, parcelamento sem juros, Full, frete grátis e envio no mesmo dia, além de reputação e modo de envio. Quem perde tem só "minimum" de visitas. [OFICIAL] developers "Competição", 21/07/2026. [PRÁTICA] Alex Moro (WF333Qri_i8, 24/06/2026) mostra um anúncio a R$ 141 no Full ganhando de outro a R$ 139.
12. **Praticantes fortes deixam "espaço promocional" no preço de lista.** O preço real de venda é o preço com promoção. Bruno Gontijo mostra 2.204 de 2.715 anúncios (81%) em campanhas cofinanciadas. O ML também pede "margem para trabalhar com descontos". [PRÁTICA com tela] ilZ92K2U_2k, 09/06/2026; ezMdUgD-Vl8, 09/06/2026; [OFICIAL] W1hgC6snin4.
13. **Na sazonalidade, o ML recomenda adiantar tudo.**
   - Natal: sortimento ativo em setembro, relevância em outubro, **pico em novembro**, queda em dezembro.
   - Calendário de importados: pedido em junho, cadastro em agosto, Full em setembro.
   - Fonte: [OFICIAL] executivo de categoria do ML, -NK3VLYm0q0, 01/06/2026.
14. **O 11.11 de 2025 foi o maior dia de vendas da história do ML**, com tráfego 56% maior e R$ 100 mi em cupons na Black Friday (+150%). Na Black Friday de 2025, o e-commerce brasileiro somou R$ 4,76 bi (+11,2%), com ticket médio de R$ 553,6 (−12,8%). [OFICIAL via terceiro] Mundo do Marketing, 14/11/2025; [DADO] Confi Neotrust via Exame, 30/11/2025.
15. **Nenhuma fonte publica teste de holdout que separe o efeito do subsídio do ML do efeito do desconto do vendedor.** A API expõe `meli_percentage` e `seller_percentage` por oferta, então a separação é mensurável na 1ª parte, mas não há estudo público. Ver seção 9.

---

## 2. Como funciona (mecânica e regras oficiais)

### 2.1 Estrutura de custo por venda (ML)

**Tarifa de venda** ([OFICIAL] /ajuda/870, s/d, lida em 14/10/2026, pode estar superada)
- **Clássico:** de 10% a 14% conforme a categoria, "Sem parcelamento" sem juros.
- **Premium:** de 15% a 19%, até 12x sem juros.
- A tarifa reflete intermediação, processamento do pagamento e, quando houver, taxa de antecipação.
- **Kits** pagam a tarifa de cada produto. O custo de envio é **um por kit** (/ajuda/42129 e /ajuda/40538).
- **Anúncio grátis** dura 60 dias e tem baixa exposição, sem parcelamento. O limite é de 5 vendas por ano para produto novo, com até 10 anúncios de 1 unidade.
- **O ML não retém impostos.** O valor de "quanto você recebe" **não inclui** Ads, custos de Full nem a mensalidade da Minha Página (/ajuda/44007). Esses custos precisam entrar na margem à parte.

**Parcelas no Premium** ([OFICIAL] /ajuda/22737)

| Preço da venda | Parcelas sem juros (Cartão Mercado Pago) | Parcelas sem juros (outros meios) |
|---|---|---|
| até R$ 29,99 | 1 | 1 |
| R$ 30 a 59,99 | 4 | 2 |
| R$ 100 a 149,99 | 6 | 4 |
| mais de R$ 500 | 12 | 10 |

- Assinantes Meli+ ganham até 3 parcelas extras em produtos abaixo de R$ 900.

**Custo de envio** ([OFICIAL] /ajuda/40538, reputação verde, MercadoLíder ou sem reputação; Full, Coleta e Agências)
- Calculado por peso e medidas da embalagem final e pelo preço.
- Cobrado em todas as vendas, mesmo quando o comprador paga o frete.
- Faixas de preço: 0–18,99; 19–48,99; 49–78,99; 79–99,99; 100–119,99; 120–149,99; 150–199,99; 200+.
- Valores de amostra até 0,3 kg: R$ 5,65 / 6,85 / 8,15 / 12,95 / 14,95 / 16,95 / 19,05 / 21,65.
- Valores de amostra de 1 a 1,5 kg: R$ 6,15 / 7,35 / 8,65 / 14,75 / 17,15 / 19,45 / 21,75 / 25,45.
- **Frete rápido opcional abaixo de R$ 79:** de R$ 12,95 (até 0,3 kg) a R$ 19,75 (4–5 kg).

**Inconsistência entre páginas oficiais:** a página de frete no atacado (/ajuda/56258) ainda mostra a tabela **anterior** (ex.: R$ 6,55 e R$ 12,35 até 0,3 kg), que é a mesma citada em vídeos de maio/2026 (8dZiKLuJWXg). Vale a página principal, /ajuda/40538, que bate com vídeos de setembro/2026 (R4CkSr5c6Jw).

**Mudanças de 24/08/2026** ([OFICIAL via terceiro] KvVyJlYt6w0, que mostra o link oficial em tela)
- Tabela geral: +1,6% em média; maior aumento de R$ 1,70 (4–5 kg, a partir de R$ 200).
- Full Super: divisão entre "produtos selecionados" (lista por EAN) e "demais".
- Flex: o repasse passa a variar por peso. Até 500 g em área próxima, cai de R$ 8,90 para R$ 7,99, segundo resposta do assistente do ML em tela.

### 2.2 Como o ML usa preço na exposição

**Catálogo / buy box** ([OFICIAL] developers "Competição", 21/07/2026)
- Um algoritmo escolhe o vencedor da página de produto com base em preço, parcelamento sem juros, Envio Full, frete grátis ou no mesmo dia.
- Status possíveis:
  - `winning`: visit_share "maximum";
  - `sharing_first_place`: "medium";
  - `competing`: "minimum";
  - `listed`: não compete.
- Motivos de exclusão: `reputation_below_threshold`, `winner_has_better_reputation`, `shipping_mode` (ME2 > ME1 > personalizado), `manufacturing_time`, `non_trusted_seller` e `newbie_program_seller` (limite de vendas do programa Decola).
- O endpoint `price_to_win` devolve o preço necessário para ganhar.

**Referências de preço** ([OFICIAL] developers, 17/12/2025, pode estar superada)
- Baseadas em preços de similares dentro e fora do ML, histórico de vendas e demanda.
- Segundo o ML, "melhora o posicionamento nos resultados de busca".
- Status: `with_benchmark_highest`, `with_benchmark_high`, `no_benchmark_ok`, `no_benchmark_lowest`.

**Automação de preços** ([OFICIAL] developers, 01/10/2026)
- **Regras disponíveis:**
  - INT_EXT: o menor preço entre similares dentro e fora do ML;
  - INT: só dentro do ML.
- **Preço mínimo obrigatório** (piso) e preço máximo.
- **Validação anti-anomalia:** compara os preços informados com o histórico de 60 dias.
- **Benefício declarado:** etiqueta "Recomendado" e distinção VIP. A queda automática aparece ao comprador como desconto.
- **Desde 18/03/2026,** itens automatizados não aceitam edição de preço via API.

**Tarifa condicionada a preço competitivo**
- Redução em pp para R$ 150–700 em categorias selecionadas (/ajuda/51251).
- Descontos de take rate desde abril/2026, condicionados a preço competitivo (carta Q2'26).
- A carta diz que o "índice de competitividade de preço" do ML melhorou, mas **não publica a fórmula**.

**Paridade com outros canais**
- **Não há regra oficial de paridade (MFN)** encontrada.
- Na prática, PRICE_MATCHING e a regra INT_EXT **leem preços externos** e geram oferta quando o item está mais caro fora do ML (W1hgC6snin4).

**Etiquetas e filtros de evento**
- Participar de eventos comerciais dá etiqueta visual e entrada nos filtros de oferta ([OFICIAL] sJsohjswUzs, 12/06/2026).
- Campanhas sazonais com banner trazem mais visitas que campanhas próprias (W1hgC6snin4).

### 2.3 Ferramentas promocionais e quem paga

Fonte: [OFICIAL] developers "Gerenciar promoções", 09/06/2026, e páginas de cada tipo.

| Tipo (API) | Quem define o preço | Bonificação ML | Regras-chave |
|---|---|---|---|
| Tradicional (DEAL), ex.: Dia dos Pais, 8.8 | vendedor, dentro de máximo e mínimo | não (pode haver boost) | preço sugerido e "top_deal_price" |
| Cofinanciada (MARKETPLACE_CAMPAIGN), "menos tarifa" | vendedor aceita | sim (`meli_percent` + `seller_percent`; exemplo da doc: 5 + 25) | só participa ou não |
| SMART (cofinanciada automatizada) | aceita | sim | itens escolhidos por algoritmo |
| PRICE_MATCHING / PRICE_MATCHING_MELI_ALL | aceita / automático | sim / 100% ML | candidatos diários, referência externa |
| Oferta do dia (DOD) | vendedor define | não | estoque mínimo informativo |
| Oferta relâmpago (LIGHTNING) | vendedor define, entre mín. e máx. | não (pode haver boost) | estoque reservado obrigatório; encerra ao esgotar; **não pode ser removida depois de ativa** (só pausar o item) |
| PRE_NEGOTIATED / UNHEALTHY_STOCK (liquidação Full) | acordado | sim, com aprovação | |
| Desconto individual / campanha do vendedor (PRICE_DISCOUNT, SELLER_CAMPAIGN) | vendedor | não | até 31 dias (praticante, G0lNX-1_754) |
| Desconto por quantidade do vendedor (VOLUME: BNGM, BNSP, SPONTH) | vendedor | **não** ("o ML não entra com coparticipação") | doc de 23/01/2025, pode estar superada; a tabela geral marca bonificação "sim" para VOLUME, provavelmente as campanhas antigas criadas pelo ML |
| Cupom do vendedor (SELLER_COUPON_CAMPAIGN, só MLB) | vendedor | não | reputação verde, item novo, máx. 31 dias, **acumula com a promoção ativa**, 1 cupom por venda, com ou sem código, orçamento (doc de 28/08/2025, pode estar superada) |
| PIX cofinanciado (BANK/COFINANCED, só MLB) | aceita | sim (exemplo: meli 8 + seller 11) | doc de 29/04/2025, pode estar superada |

**Outras condições e quem paga**
- **Preço de atacado:** visível só para compradores com CNPJ validado. O envio é calculado sobre o pedido inteiro, e acima de R$ 79 o frete é grátis. Segundo o ML, a economia chega a 80% (/ajuda/36440).
- **Parcelamento sem juros:** pago pelo vendedor via tarifa Premium.
- **Frete grátis de R$ 19 a 78,99:** é o ML que "oferece", mas o vendedor paga o custo de envio da tabela.
- **Afiliados:** comissão definida pelo vendedor, de até 12%, com janela de 24 h ([OFICIAL] -NK3VLYm0q0).
- **Cupons da plataforma em datas:** pagos pelo ML (R$ 100 mi na Black Friday de 2025).

**Nova Central de Promoções** ([OFICIAL] CZtSrI1qeoo, 20/08/2026; 2Wa4bV8vBcU, 25/08/2026)
- Métricas de 30 dias: visitas, vendas, conversão e faturamento bruto.
- "Tarefas e recomendações", que inclui problemas de competitividade.
- Calendário de eventos (relâmpago, Black Friday, Natal).
- Vista de promoções por tipo e editor em massa.

---

## 3. O que os melhores fazem

### 3.1 Práticas com consenso (≥ 2 fontes)

**P1. Preço de lista com espaço promocional**
- Os praticantes definem o preço-alvo **com** promoção e publicam a lista acima dele, para caber em campanhas sem destruir margem. Fontes: [PRÁTICA] ezMdUgD-Vl8 (Magiic), ilZ92K2U_2k (Gontijo), iAM5PWaVV08 (Ritter); [OFICIAL] W1hgC6snin4 e -NK3VLYm0q0.
- O time de pricing do ML impõe um limite a isso: lista inflada com desconto de 40% a 50% e preço final acima do concorrente não converte.
- Ritter ainda afirma que o ML "percebe" lista inflada depois de publicada e exige preço mais baixo (afirmação sem base). Ver A21 e A22.

**P2. Estar sempre em alguma promoção, com cobertura escalonada**
- Os praticantes participam de várias campanhas ao mesmo tempo para não ficar "sem promoção" quando uma acaba. Só a de maior desconto fica ativa; as outras ficam programadas, mas o anúncio aparece nas páginas de todas.
- Fontes: [PRÁTICA com tela] G0lNX-1_754 (GeMarket, 22/07/2026); ezMdUgD-Vl8.
- **Frequência de revisão:** pelo menos 1 vez por semana (GeMarket). Para price matching, o ML recomenda olhar diariamente (W1hgC6snin4).

**P3. Priorizar campanhas cofinanciadas e "menos tarifa"**
- Gontijo entra nas cofinanciadas mesmo com margem um pouco menor, porque o preço cai mais do que a margem. Ele evita campanhas não cofinanciadas que forçam o preço para baixo.
- Ritter mostra rebate de R$ 52 num produto de cerca de R$ 1.000, com margem de 20% para 25%.
- Fontes: [PRÁTICA com tela] ilZ92K2U_2k; iAM5PWaVV08; [OFICIAL] W1hgC6snin4 ("aporte ML bem positivo" no price matching).

**P4. Margem-alvo por segmento e piso explícito**
- Gontijo configura margem-alvo de 20% (aceita 15%) numa conta nova e exige mais de 30% para importados. A ferramenta de terceiros entra em massa só onde a margem promocional fica acima do piso.
- O ML exige `min_price` em toda automação.
- Fontes: [PRÁTICA] ilZ92K2U_2k; [OFICIAL] developers, automação, 01/10/2026.

**P5. Promoção ligada ao estoque**
- Antes de ativar uma promoção, os praticantes perguntam "o estoque aguenta se der certo?". Comparam o potencial de venda do estoque (estoque × preço) com a venda atual. Estoque alto e giro travado pedem promoção agressiva; estoque baixo pede promoção leve ou nenhuma.
- Fontes: [PRÁTICA] ezMdUgD-Vl8; [OFICIAL] -NK3VLYm0q0 (alerta de reposição quando restam ~30%); sJsohjswUzs.

**P6. Kits e quantidade como alavanca de preço sem guerra**
- O kit paga um único custo de envio (oficial).
- Gontijo vendeu 16 kits de 3 unidades contra 3 vendas avulsas do mesmo item.
- Líderes de café usam desconto por quantidade (5 e 10 un) e kits como anúncios separados.
- Fontes: [OFICIAL] /ajuda/40538, /ajuda/45023; [PRÁTICA] F_3Wy-Xsvx8; [OBS] lideres.md.

**P7. Cupom como empurrão final, não como preço-base**
- Variações usadas: cupom semanal (urgência), valor mínimo acima do ticket médio e cupom de carrinho abandonado via Minha Página e canal de transmissão.
- Fontes: [PRÁTICA] G0lNX-1_754; iAM5PWaVV08. Regras na doc oficial de cupons.

### 3.2 Divergências entre fontes

**D1. Começar com preço baixo ou alto?**
- Gontijo (F_3Wy-Xsvx8, 11/10/2026) começa alto e desce se precisar. Mostra 4 importados com margem pós-Ads de 34,9% a 40,8% e TACOS de 0,06% a 1%, sem "vender no prejuízo".
- O conteúdo de mentoria que ele critica defende preço agressivo inicial.
- O próprio Natan Aquino diz que o iniciante nos Correios precisa ser "mais agressivo no preço" (8dZiKLuJWXg).
- Não há teste controlado. O caso de Gontijo escolhe 4 produtos, um deles fraco, o que é risco de viés de sobrevivente.

**D2. Premium vale a pena?**
- Natan: "só acima de R$ 500" (opinião).
- Universidade Ecommerce: depende do hábito do público.
- O documento oficial de catálogo lista "parcelamento sem juros" como fator da buy box. Em catálogo, portanto, o Premium tem efeito de exposição. Fora do catálogo, não há evidência pública.

**D3. Promoção própria ou da plataforma?**
- O ML confirma que as campanhas de data com banner trazem mais visitas.
- GeMarket diz que a promoção própria "não tem incentivo da plataforma", mas conta para a qualidade do anúncio. Isso não foi confirmado em fonte oficial.

**D4. Ads ou promoção quando a margem é curta?** O ML não hierarquiza ("objetivos diferentes"). Gontijo opina que a central "às vezes dá mais resultado do que Ads" (opinião, N7).

### 3.3 Como medem competitividade de preço

**Ferramentas oficiais**
- "Gestão de preços": mostra concorrentes internos e externos e faz ajuste automático (W1hgC6snin4).
- Status de referência de preço (developers).
- `price_to_win` no catálogo.
- No painel "Métricas > Análise de mercado", os % de uso de cupons e Premium por concorrente (protocolo; não verificado nesta frente).

**Praticantes**
- Monitoram o catálogo hora a hora com ferramenta de terceiros: quem saiu, quem ficou sem estoque e quando o concorrente repõe. Usam essas brechas para **subir** preço quando o concorrente rompe ([PRÁTICA] Alex Moro, WF333Qri_i8; CTA de ferramenta, conflito de interesse).
- Comparam "preço total" (preço + frete) com os primeiros colocados.

**Sem evidência no ML Brasil:** índice ponderado de Lowe, % de buy box por portfólio e preço contra a mediana da 1ª página como rotina documentada. O próprio ML usa um "índice de competitividade" interno sem fórmula pública.

### 3.4 Como calculam preço mínimo e preço-alvo

**Método** ([PRÁTICA] R4CkSr5c6Jw, 29/09/2026, planilha em tela; POjujir152o, 25/09/2026; G0lNX-1_754)

**Fórmula do preço-alvo (markup divisor)**

  P = (custo do produto + embalagem + custo de envio em R$) ÷ (1 − comissão% − imposto% − TACOS-alvo% − devoluções% − margem-alvo%)

- O custo de envio depende da faixa de preço. Por isso o cálculo é **iterativo** e precisa checar os degraus de R$ 19, 49, 79, 100, 120, 150 e 200.
- A comissão incide sobre o **preço promocional** final (G0lNX-1_754; consistente com a doc de cofinanciadas).

**Escada de margem e limites de Ads**
- **CM1** = preço − custo − imposto − comissão − envio − embalagem.
- **ACOS máximo** = CM1% e **ROAS mínimo** = 1/CM1% (Milewa: CM1 de 26,35% leva a ROAS mínimo de 3,80).
- **CM2** = CM1 − Ads (via TACOS).
- **CM3** = CM2 − armazenagem e estoque antigo do Full, inconformidades, devoluções com culpa do vendedor, afiliados e cupons ([PRÁTICA] XETb71Rn4dM, 24/07/2026; /ajuda/21793).

**Exemplo ilustrativo** (cálculo desta nota, com custos oficiais e premissas hipotéticas; não é dado de empresa)
- Premissas: produto de 1–1,5 kg, reputação verde, Clássico a 12%, imposto de 6%, custo de R$ 30, embalagem de R$ 1,50.
- **A R$ 69,90:** envio de R$ 8,65; CM1 = R$ 17,17 (24,6%), o que dá ROAS mínimo de ≈ 4,1. Com TACOS de 5%, a CM2 fica em 19,6%. Com 2% de devoluções, a CM3 fica em 17,6%.
- **A R$ 79,90:** o envio sobe para R$ 14,75 e a CM1 fica em R$ 19,27 (24,1%). Subir R$ 10 no preço rende só +R$ 2,10 de CM1.
- O **degrau de R$ 79** é onde os praticantes mais erram (ver seção 6).

### 3.5 Como evitam guerra de preço

**Mecanismos oficiais**
- Piso obrigatório na automação (INT/INT_EXT).
- Possibilidade de **não** acompanhar a oferta de price matching quando o concorrente está numa "super promoção pontual". O próprio ML diz que vale avaliar se faz sentido seguir (W1hgC6snin4).

**Mecanismos de praticantes e observação**
- Kits e combinações, desconto por quantidade e atacado para CNPJ.
- Linha completa de formatos e tamanhos, que gera embalagens próprias e menos comparação direta ([OBS] lideres: Orfeu e Italle cobrem grão, moído, cápsula e drip em 250 g, 500 g e 1 kg).
- Vencer o catálogo por logística e reputação em vez de preço (R$ 141 no Full ganhando de R$ 139).
- Muitos SKUs de cauda longa em vez de poucos SKUs disputados ([PRÁTICA] F_3Wy-Xsvx8).

**Preço por canal:** não há regra oficial que proíba, mas o ML monitora preços externos e gera ofertas de equiparação quando o item está mais caro fora.

### 3.6 Calendário e preparação

**Calendário de eventos observado no ML Brasil em 2026** ([OFICIAL] W1hgC6snin4, -NK3VLYm0q0, G0lNX-1_754)
- Dia dos Namorados (12/06) e Copa do Mundo (junho).
- Datas duplas mensais, entre elas 6.6, 7.7 "Descontaço" e 8.8 (vigente de 20/07 a 10/08 segundo GeMarket).
- Dia dos Pais, 9.9, 10.10 e 11.11.
- Black Friday: sexta-feira, 27/11/2026 (cálculo de calendário, não confirmação do ML).
- Natal.
- A carta Q2'26 cita "Hot Sale" e "Cyber Day", mas esses são eventos de outros países (México, Argentina e Chile).

**Preparação**
- **Estoque:** curva A e envio antecipado ao Full, com agenda marcada cedo. Escolher de 10 a 20 produtos foco. Projetar volume pelo histórico (se cresceu 30% na última BF, enviar 30% a mais). Fonte: [OFICIAL] EnviosCast hvXa7Pr0mp4, 29/09/2026, com embaixador do ML: "1º de novembro já é atrasado".
- **Preço:** ativar campanhas do calendário pela central e manter margem para promoção (sJsohjswUzs).
- **Verba:** começar Ads **antes** do pico para ganhar relevância orgânica e não pagar o leilão mais caro ([OFICIAL] -NK3VLYm0q0). ROAS mais alto para a curva A e mais baixo para lançamentos (sJsohjswUzs).
- Quem se sai bem no fim do ano colhe em janeiro e março pelo ganho de ranqueamento (hvXa7Pr0mp4, opinião de participante).

---

## 4. Números de referência

| # | Número | Fonte | Data | Tipo |
|---|---|---|---|---|
| N1 | Clássico 10–14%; Premium 15–19% | /ajuda/870 | s/d, lido 14/10/2026 (pode estar superada) | OFICIAL |
| N2 | Envio até 0,3 kg: R$ 5,65 (0–18,99), 6,85 (19–48,99), 8,15 (49–78,99), 12,95 (79–99,99), 21,65 (200+) | /ajuda/40538 | idem | OFICIAL |
| N3 | Abaixo de R$ 19: custo de envio máximo de 50% do preço | /ajuda/40538 | idem | OFICIAL |
| N4 | Desconto por reputação verde: até 50% (já embutido) | /ajuda/40538 | idem | OFICIAL |
| N5 | Frete rápido opcional abaixo de R$ 79: R$ 12,95 a 19,75 (até 5 kg) | /ajuda/40538 | idem | OFICIAL |
| N6 | R$ 150–700, Alimentos e Bebidas: −5 pp Premium / −3 pp Clássico | /ajuda/51251 | idem | OFICIAL |
| N7 | Full Super: preço > R$ 8; reputação verde; frete grátis na loja a partir de R$ 199 | /ajuda/16449 | idem | OFICIAL |
| N8 | Full Super, abaixo de R$ 29: envio máximo de 25% do preço; "selecionados" até 0,3 kg de R$ 1,00 a R$ 4,80 abaixo de R$ 199 | /ajuda/49972 | idem | OFICIAL |
| N9 | Armazenagem Full por dia: P R$ 0,007; M 0,015; G 0,050; GG 0,107; Supermercado P/M grátis; estoque antigo acima de 2 meses gera custo | /ajuda/21793 | idem | OFICIAL |
| N10 | Reajuste de envio em 24/08/2026: +1,6% em média; Full Super "demais" +20–40% | KvVyJlYt6w0 | 12/08/2026 | OFICIAL via terceiro |
| N11 | Cupom do vendedor: máx. 31 dias; reputação verde | developers, cupons | 28/08/2025 (pode estar superada) | OFICIAL |
| N12 | Price matching: opt-in dura 7 dias; candidatos diários | W1hgC6snin4; developers | 03/06/2026; 09/06/2026 | OFICIAL |
| N13 | Validação de piso da automação: histórico de 60 dias | developers, automação | 01/10/2026 | OFICIAL |
| N14 | Relâmpago: desconto mínimo exigido de 31% no caso mostrado; desconto na 2ª unidade ≥ 30%; Meli+ ≥ 5 pp acima | G0lNX-1_754 | 22/07/2026 | PRÁTICA (tela) |
| N15 | Duração de relâmpago de ~12 h, segundo Ritter | iAM5PWaVV08 | 13/08/2026 | PRÁTICA (sem doc oficial de duração) |
| N16 | Faixa de margem: iniciante revendedor 10–20%; fabricante ou importador direto 25–35%+ | R4CkSr5c6Jw | 29/09/2026 | PRÁTICA (N7, sem base) |
| N17 | ACOS máximo = CM1% (ex.: 26,35% → ROAS 3,80) | POjujir152o | 25/09/2026 | PRÁTICA (método) |
| N18 | Clips: 5x visitas, 2x vendas, +143% vendas (30 dias antes e depois), +11% conversão | -NK3VLYm0q0 | 01/06/2026 | DADO interno ML, sem metodologia nem controle |
| N19 | Preço é decisivo para "60% dos consumidores"; diferença de 5–10% muda o canal | W1hgC6snin4 | 03/06/2026 | OFICIAL, sem base publicada |
| N20 | Black Friday 2025, e-commerce BR: R$ 4,76 bi (+11,2%); 8,69 mi pedidos (+28%); ticket R$ 553,6 (−12,8%) | Confi Neotrust via Exame | 30/11/2025 | DADO (amostra não divulgada) |
| N21 | ML 11.11 2025: tráfego +56%; R$ 100 mi em cupons na BF (+150%) | Mundo do Marketing (exec. ML) | 14/11/2025 | OFICIAL via terceiro |
| N22 | ML Brasil Q2'26: GMV +39% FX-neutral; itens +56%; conversão +1,1 pp; vendedores ativos +29% | Carta Q2'26 (8-K) | 05/08/2026 | OFICIAL N2 |
| N23 | Frete grátis lento é contribuição-positivo em metade das faixas de preço médio entre R$ 19 e 79 | Carta Q2'26 | 05/08/2026 | OFICIAL N2 |
| N24 | Shopee (CNPJ, desde 01/03/2026): até R$ 79,99 → 20% + R$ 4; 80–99,99 → 14% + R$ 16; 100–199,99 → 14% + 20; 200+ → 14% + 26; subsídio PIX de 5% (8% acima de R$ 500); CPF com mais de 450 pedidos em 90 dias paga +R$ 3 | R4CkSr5c6Jw; Anymarket | 29/09/2026; 2026 | OFICIAL via terceiro (divergência sobre teto de R$ 100) |
| N25 | Amazon BR: Alimentos e Bebidas 10%; plano profissional R$ 19/mês | R4CkSr5c6Jw (tabela em tela) | 29/09/2026 | OFICIAL via terceiro |
| N26 | Cofinanciadas em 81% dos anúncios de uma operação grande (2.204/2.715) | ilZ92K2U_2k | 09/06/2026 | PRÁTICA (tela) |

---

## 5. Alimentos, perecíveis e marca própria/indústria

**O que muda no custo**
- **Full Super** (/ajuda/16449 e /ajuda/49972) tem custo de envio próprio, com faixas que vão até "a partir de R$ 199" em vez de R$ 79. Exige preço acima de R$ 8, reputação verde e estoque no Full.
- A lista de **"Produtos selecionados"** (por EAN, vinculada a catálogo) paga bem menos. Até 0,3 kg, R$ 2,40 na faixa de R$ 49–78,99, contra R$ 3,60 dos demais.
- Abaixo de R$ 29, o envio fica limitado a 25% do preço. O frete grátis na loja Full Super começa em R$ 199. Isso favorece cestas de várias unidades, e não o item avulso.
- **Alerta:** a economia de envio por quantidade ou kit **não se aplica à seção Supermercado** (/ajuda/45023). A lógica de "kit barateia o frete" vale para alimentos fora do Supermercado, não dentro dele.
- **Armazenagem:** Supermercado não paga diária em P/M, mas o estoque antigo começa a ser cobrado **depois de 2 meses**, contra 4 meses em categorias gerais (/ajuda/21793; [PRÁTICA] XETb71Rn4dM).
- Para perecíveis e itens de validade curta, isso torna a previsão de demanda e a liquidação (campanha UNHEALTHY_STOCK, com bonificação ML) parte do preço.

**Tarifa**
- Alimentos e Bebidas, incluindo Café Moído e em Grão, Café Solúvel, Chá e Infusões, tem **−5 pp no Premium e −3 pp no Clássico** entre R$ 150 e R$ 700 (/ajuda/51251).
- Isso desloca o incentivo para **kits e packs nessa faixa**. Para indústria e marca própria com linha completa, é uma alavanca de tarifa sem desconto ao consumidor.
- A porcentagem-base da categoria não foi verificada em fonte oficial (pede login). Um blog cita 11–13% no Premium (Jaguarsheet, 19/05/2026, N5), o que é **incompatível** com o piso oficial de 15% do Premium. Ver seção 6.

**Como o preço aparece em alimentos** ([OBS] lideres.md, 14/10/2026, CEP em MG)
- Todos os líderes de café mostram preço riscado, preço no PIX (8% a 53% OFF) e preço por kg.
- Faixas por kg: supermercado R$ 32–84; especial de marca R$ 90–160; microlotes acima de R$ 200.
- Também aparecem desconto por quantidade (Appassionato 5 un a R$ 92/un; Pilão 5 un a R$ 66,39/un) e relâmpago com contador.
- O desconto no PIX é, pelo menos em parte, **financiado pelo ML** desde abril/2026 (carta Q2'26). Isso explica descontos no PIX maiores que a margem plausível do vendedor. Separar o que é subsídio do que é desconto do vendedor exige olhar a oferta na Central ou na API (`meli_percentage`).

**Marca e indústria em catálogo**
- O catálogo é disputado por revendedores. No Pilão 1 kg havia 72 vendedores, e quem ganhava era um supermercado revendedor. A loja oficial Italle aparecia mais cara que outra loja no próprio produto ([OBS] lideres.md).
- O ML **não oferece política de preço mínimo anunciado (MAP)** para a marca, pelo que se encontrou. O Brand Protection Program trata de propriedade intelectual, não de preço.
- O 1P do próprio ML também disputa preço em categorias (carta Q1'26, 07/05/2026).

---

## 6. Erros comuns e mitos

**1. "Existe custo fixo de R$ 6,25 a 6,75 (ou de R$ 5,50 a 10,00) por unidade abaixo de R$ 79 / R$ 199."**
- O que dizem as fontes fracas: blogs de 2026 divergem entre si. A Jaguarsheet chega a citar faixas de custo fixo até R$ 199.
- O que diz a fonte forte: a página oficial hoje mostra só tarifa % + custo de envio por peso × faixa. Abaixo de R$ 19, o máximo é metade do preço.
- **Status:** superado. Blogs divergentes viram faixa, nunca média.

**2. "Produto abaixo de R$ 12,50 paga 50% de custo fixo."** (8dZiKLuJWXg, 28/05/2026)
- A regra oficial atual usa **R$ 19** como corte, com custo de envio de no máximo 50% do preço.

**3. "Reputação verde dá 70% de desconto no frete."**
- A página oficial atual diz **até 50%**. Os 70% eram citados em maio/2026.

**4. "Subir o preço de lista e dar 40–50% de desconto resolve."**
- O time de pricing do ML diz que o comprador compara com a referência de mercado. Desconto grande com preço final acima do concorrente não converte.
- Além disso, a automação valida preços contra o histórico de 60 dias.
- A legalidade de "de/por" fictício (CDC/Procon) não foi verificada aqui (lacuna).

**5. "Promoções se somam."**
- Não se somam: só a de maior desconto fica ativa.
- O que soma é **promoção + cupom** (doc de cupons: acumulativo com a promoção ativa, um cupom por venda).

**6. "Oferta relâmpago zera a tarifa."**
- Acontece em casos específicos (prints de Ritter) e corresponde ao "boosted offer" documentado. **Não é regra**: a relâmpago não tem bonificação padrão, e o vendedor define o preço dentro dos limites.

**7. "Clássico permite parcelar em 6x com juros"** (blogs) **vs. "Sem parcelamento"** (/ajuda/870).
- A página de parcelas indica que o ML pode oferecer até 12x **com acréscimo** ao comprador quando o anúncio tem menos de 12x sem juros. A divergência é de definição: o Clássico não oferece parcelas sem juros.

**8. "Não pode mudar preço nos 60 dias antes da Black Friday (CDC)."** (participante do EnviosCast hvXa7Pr0mp4)
- Nenhuma base legal foi encontrada nesta pesquisa. Fica como afirmação sem fonte. Não confundir com a regra europeia de 30 dias.

**9. "Ganhar o catálogo é ser o mais barato."**
- A doc oficial pondera Full, parcelamento, frete grátis, reputação e modo de envio. O caso dos R$ 141 contra R$ 139 ilustra (PRÁTICA, N6).

**10. Números sem base**
- "90% das vendas estão na 1ª página" e "promoção mostra para 100 em vez de 10" (Avantpro, citados no protocolo).
- "Mais de 90% das compras são de clientes novos" (G0lNX-1_754, sem base).
- "Assinante Meli+ compra 78% a mais", citado como aumento de vendas. É confusão de métricas, e o próprio GeMarket corrige.

**11. Atribuição tratada como causalidade**
- "Clips aumentam vendas em 143%" vem de comparação 30 dias antes e depois, sem controle.
- "A promoção saiu e a conversão despencou" (Magiic) é uma correlação.

**12. "Ativar a 'consultoria Platinum' por link libera mais campanhas cofinanciadas."** (Gontijo)
- Não existe página oficial do programa no Brasil (lacuna conhecida). É sinal fraco e não deve ser tratado como regra.

**Sinais de conteúdo fraco por fonte**
- **iAM5PWaVV08:** QR code e grupo de WhatsApp (CTA), promessa ("não tem erro"), mentoria.
- **ilZ92K2U_2k, F_3Wy-Xsvx8:** cupom da ferramenta (conflito de interesse), mas com demonstração em tela.
- **ezMdUgD-Vl8, WF333Qri_i8:** a ferramenta vende o próprio painel.
- **R4CkSr5c6Jw:** "comente PLANILHA" (CTA) e faixa de margem sem base.

---

## 7. Revenda/importação x indústria/marca própria

**[REVENDA] revenda, dropshipping e importação**
- **Disputa de catálogo** de marcas de terceiros (Pilão, Mondial): o revendedor não controla título, fotos nem avaliações. A alavanca é preço total + Full + reputação + reação rápida a ruptura de concorrente (WF333Qri_i8; lideres.md).
- **Margens-piso altas** para importados (mais de 30% em Gontijo), por causa do risco cambial e do prazo de reposição. **Calendário de importação:** pedido em junho para o Natal (-NK3VLYm0q0).
- **Price matching e automação INT** pressionam mais quem vende produto idêntico comparável. Para produto genérico, o piso (`min_price`) é a defesa principal.
- **Os casos mostrados são quase todos de importadores:** Ritter (ticket de ~R$ 1.000, produto achado via ferramenta de pesquisa de importação) e Gontijo (importação, 4 SKUs). Generalizar para marca é arriscado.

**[MARCA] indústria e marca própria**
- **Linha de formatos e tamanhos** reduz a comparação direta e cria kits na faixa de R$ 150–700, com tarifa −3 a −5 pp em Alimentos ([OBS] Orfeu e Italle; /ajuda/51251).
- **Risco específico:** perder a buy box do próprio produto para revendedores (Italle, Pilão). Não há MAP oficial, então o controle depende de distribuição e canal, fora do ML.
- **Lista de "produtos selecionados" do Full Super** por EAN: indústria com EAN próprio e catálogo pode ter custo de envio menor. A seleção é feita pelo ML, e o critério não é publicado.
- **Paridade de canal:** se o preço no site próprio ou em outros marketplaces for menor, o ML gera ofertas de equiparação cofinanciadas (INT_EXT/PRICE_MATCHING). Marcas multicanal precisam considerar que o ML lê preços externos.

**Vale para ambos**
- Escada CM1 → CM3, comissão sobre o preço promocional, degraus de faixa de envio, ACOS máximo = CM1% e prioridade a campanhas cofinanciadas.
- Revisão semanal da central e diária no price matching. Antecipação de estoque e Ads para a sazonalidade.

---

## 8. Tabela de afirmações

| id | afirmação | tipo | fonte | data | confiança |
|---|---|---|---|---|---|
| A1 | Clássico 10–14% sem parcelamento; Premium 15–19% com até 12x sem juros | OFICIAL | mercadolivre.com.br/ajuda/870 | s/d, lido 14/10/2026 (pode estar superada) | alta (A: + R4CkSr5c6Jw) |
| A2 | Custo de envio cobrado em toda venda, por peso, medidas e preço, mesmo que o comprador pague o frete | OFICIAL | /ajuda/40538 | idem | alta |
| A3 | Faixas de envio até 0,3 kg: 5,65 / 6,85 / 8,15 / 12,95 / 14,95 / 16,95 / 19,05 / 21,65 | OFICIAL | /ajuda/40538 | idem | alta (bate com R4CkSr5c6Jw) |
| A4 | Abaixo de R$ 19, o envio custa no máximo metade do preço | OFICIAL | /ajuda/40538 | idem | alta |
| A5 | Desconto por reputação verde de até 50%, embutido na tabela | OFICIAL | /ajuda/40538 | idem | média (diverge de 8dZiKLuJWXg: 70%) |
| A6 | R$ 19–78,99: ML oferece frete grátis padrão; a partir de R$ 79, vendedor oferece frete grátis rápido; rápido abaixo de R$ 79 é opcional, a partir de R$ 12,95 | OFICIAL | /ajuda/40538 | idem | alta |
| A7 | Reajuste de envio em 24/08/2026: +1,6% médio; Full Super "demais" +20–40% | OFICIAL via terceiro | KvVyJlYt6w0 | 12/08/2026 | média |
| A8 | Alimentos e Bebidas R$ 150–700: −5 pp Premium, −3 pp Clássico | OFICIAL | /ajuda/51251 | s/d (pode estar superada) | média (fonte única N1) |
| A9 | Desde abril/2026: desconto de take rate a vendedores e PIX a compradores, condicionados a preço competitivo | OFICIAL N2 | SEC 8-K, carta Q2'26 | 05/08/2026 | alta |
| A10 | Full Super: preço > R$ 8, reputação verde, CD Full; frete grátis na loja a partir de R$ 199 | OFICIAL | /ajuda/16449 | s/d (pode estar superada) | média |
| A11 | Full Super abaixo de R$ 29: envio máximo de 25% do preço; "selecionados" com custo menor | OFICIAL | /ajuda/49972 | s/d (pode estar superada) | média |
| A12 | Economia de envio por quantidade ou kit não vale na seção Supermercado | OFICIAL | /ajuda/45023 | s/d (pode estar superada) | média |
| A13 | Supermercado: sem diária P/M; estoque antigo acima de 2 meses gera custo | OFICIAL | /ajuda/21793 | s/d (pode estar superada) | alta (+ XETb71Rn4dM) |
| A14 | 12 tipos de promoção na API; cofinanciadas: MARKETPLACE_CAMPAIGN, SMART, PRICE_MATCHING; MELI_ALL 100% ML | OFICIAL | developers, Gerenciar promoções; Smart/PM | 09/06/2026 | alta |
| A15 | ML pode aplicar desconto automático (boost), compensado como redução nos custos por venda (DEAL, PRICE_DISCOUNT, PRE_NEGOTIATED, SMART, PRICE_MATCHING, LIGHTNING) | OFICIAL | developers | 09/06/2026 | alta (+ prints iAM5PWaVV08) |
| A16 | Relâmpago: estoque reservado, encerra ao esgotar; não pode ser removida depois de ativa | OFICIAL | developers, Ofertas relâmpago | 09/06/2026 | alta |
| A17 | Cupom do vendedor: só MLB, reputação verde, máx. 31 dias, acumula com promoção, 1 por venda | OFICIAL | developers, Cupons | 28/08/2025 (pode estar superada) | média |
| A18 | Desconto por quantidade criado pelo vendedor não tem coparticipação ML | OFICIAL | developers, Volume | 23/01/2025 (pode estar superada) | baixa (contradiz a tabela geral) |
| A19 | Price matching: referência externa, algoritmo diário, 7 dias, aporte cai sozinho e aumento pede novo opt-in; sempre cofinanciado | OFICIAL | W1hgC6snin4; developers | 03/06/2026; 09/06/2026 | alta |
| A20 | Buy box: preço, parcelamento sem juros, Full, frete grátis, mesmo dia; visit_share max/medium/min; motivos de exclusão | OFICIAL | developers, Competição | 21/07/2026 | alta |
| A21 | Desconto que leva de "mais caro" para "igual ou mais barato" que a referência é o que mais converte | OFICIAL (dado interno sem número) | W1hgC6snin4 | 03/06/2026 | média |
| A22 | ML detecta lista inflada depois de publicada e exige preço menor | PRÁTICA | iAM5PWaVV08 | 13/08/2026 | baixa (N7) |
| A23 | Automação: regras INT/INT_EXT, piso obrigatório, validação de 60 dias, etiqueta "Recomendado"; API bloqueada desde 18/03/2026 | OFICIAL | developers, Automatizações | 01/10/2026 | alta |
| A24 | Referência de preço melhora o posicionamento na busca (afirmação do ML) | OFICIAL | developers, Referências | 17/12/2025 (pode estar superada) | média |
| A25 | Operação grande com 81% dos anúncios em cofinanciadas; margem-alvo 20% (aceita 15%); importados acima de 30% | PRÁTICA (tela) | ilZ92K2U_2k | 09/06/2026 | média |
| A26 | 4 importados com margem pós-Ads de 34,9–40,8% e TACOS 0,06–1%, sem preço de prejuízo (jun–out/2026) | CASE (viés de seleção) | F_3Wy-Xsvx8 | 11/10/2026 | baixa |
| A27 | Rebate eleva margem de 20% para 25% em produto de ~R$ 1.000; relâmpago com tarifa de R$ 0,01 em casos mostrados | PRÁTICA (tela, sinais fracos) | iAM5PWaVV08 | 13/08/2026 | baixa |
| A28 | Só a promoção de maior desconto fica ativa; promoção + cupom somam | PRÁTICA + OFICIAL | G0lNX-1_754; developers, Cupons | 22/07/2026; 28/08/2025 | alta |
| A29 | Comissão incide sobre o preço promocional final | PRÁTICA (tela) | G0lNX-1_754 | 22/07/2026 | média |
| A30 | ACOS máximo = CM1%; ROAS mínimo = 1/CM1 | PRÁTICA (método) | POjujir152o | 25/09/2026 | alta (princípio) |
| A31 | Natal: ativar em setembro, relevância em outubro, pico em novembro; importados com pedido em junho | OFICIAL | -NK3VLYm0q0 | 01/06/2026 | média |
| A32 | BF: "1º de novembro já é atrasado"; foco em 10–20 SKUs curva A; projetar pelo crescimento histórico | OFICIAL (podcast ML com convidados) | hvXa7Pr0mp4 | 29/09/2026 | média |
| A33 | Afiliados: comissão de até 12% definida pelo vendedor, janela de 24 h | OFICIAL | -NK3VLYm0q0 | 01/06/2026 | média |
| A34 | Black Friday 2025 BR: R$ 4,76 bi (+11,2%), ticket R$ 553,6 (−12,8%) | DADO | Confi Neotrust via Exame | 30/11/2025 | média |
| A35 | 11.11 2025 foi o maior dia de vendas do ML; R$ 100 mi em cupons na BF | OFICIAL via terceiro | Mundo do Marketing | 14/11/2025 | média |
| A36 | Líderes de café exibem PIX 8–53% OFF, preço/kg e desconto por quantidade | OBS | observacao/lideres.md | 14/10/2026 | média (fonte única N3) |
| A37 | Catálogo de marca ganho por revendedor (Pilão: 72 vendedores) | OBS | lideres.md (MLB35944622) | 14/10/2026 | média |
| A38 | Shopee CNPJ: 20% + R$ 4 até R$ 79,99; 14% + R$ 16/20/26 acima; PIX 5%/8% | OFICIAL via terceiro | R4CkSr5c6Jw; Anymarket | 2026 | média |
| A39 | Amazon BR Alimentos 10%; plano profissional R$ 19/mês | OFICIAL via terceiro | R4CkSr5c6Jw | 29/09/2026 | média |
| A40 | Página de atacado (/ajuda/56258) ainda mostra a tabela antiga | OBS (leitura de N1) | /ajuda/56258 vs /ajuda/40538 | 14/10/2026 | alta |
| A41 | Ferramentas de estimativa admitem que os dados são "estimados", não precisos | DADO | Termos Nubimetrics (nubimetrics.com/pdf/terminos_pt.pdf) | s/d | média |

---

## 9. Lacunas

1. **Tarifa % exata por categoria** (ex.: Alimentos, Café) **e landing de custos:** pedem login e não foram abertas. A única fonte de terceiros encontrada (11–13% no Premium) conflita com o piso oficial de 15%.
2. **Separação subsídio × desconto do vendedor no efeito de promoção:** nenhum estudo público, holdout ou teste de pausa. Há só afirmações qualitativas do ML (W1hgC6snin4) e da carta Q2'26 (índice de competitividade sem fórmula).
3. **Índice de competitividade de preço do ML:** citado na carta, sem fórmula. Também não há prática documentada no Brasil de índice ponderado (Lowe), % de buy box de portfólio ou preço contra a mediana da 1ª página.
4. **Duração e desconto mínimo oficiais de oferta relâmpago e oferta do dia:** só há relatos de praticantes (12 h; 31%). A doc da API não fixa esses números.
5. **Regra de paridade e MAP:** nenhuma política oficial de paridade de preço com outros canais nem de preço mínimo para marcas.
6. **Calendário oficial de campanhas de 2026 com prazos de adesão:** não foi encontrado em página pública. Datas montadas a partir de webinars e praticantes. A data da Black Friday de 2026 é cálculo.
7. **Legalidade de "preço de/por" e a suposta regra de 60 dias antes da Black Friday:** não verificadas (CDC/Procon/Senacon).
8. **Critério da lista de "produtos selecionados" do Full Super:** não publicado.
9. **Campanha "consultoria Platinum" e programas de assessoria pagos:** sem página oficial no Brasil.
10. **Camada de dados curta:** a cota de buscas na web acabou durante a coleta. NIQ Ebit 2025, Real Trends, Hunter HUB, Olist e Bling ficaram sem fonte com método. Neotrust aparece via imprensa, sem amostra divulgada.
11. **Shopee e Amazon:** as páginas oficiais da Shopee são renderizadas por JavaScript e não puderam ser lidas. Os números vêm de terceiros e de tela de vídeo, com divergência sobre o teto de R$ 100 da comissão.
12. **Benchmarks públicos de Ads e promoção por categoria no ML Brasil:** não existem (lacuna conhecida, confirmada).


## 10. Verificação (2026-10-14)

Limite da verificação: as páginas oficiais do ML (mercadolivre.com.br/ajuda/*, developers.mercadolivre.com.br/*) responderam HTTP 403 ao leitor automático, e a cota de buscas na web da execução estava esgotada. Sem leitura direta da fonte oficial, nada foi marcado CONFIRMADA, por regra ("na dúvida, não confirme"). Exceção: R7, lida no documento da SEC.

| id | veredito | fonte oficial (URL) | observação |
|----|----------|---------------------|------------|
| R1 | SEM FONTE OFICIAL (não reverificada) | https://www.mercadolivre.com.br/ajuda/870 (403) | Página bloqueada ao leitor; percentuais não reconferidos. Pode estar superada. |
| R2 | SEM FONTE OFICIAL (não reverificada) | https://www.mercadolivre.com.br/ajuda/40538 (403) | Valores da tabela de envio não reconferidos; vale a nota A40 (/ajuda/56258 mostra tabela antiga). |
| R3 | SEM FONTE OFICIAL (não reverificada) | https://www.mercadolivre.com.br/ajuda/40538 (403) | Não reconferida. |
| R4 | SEM FONTE OFICIAL (não reverificada) | https://www.mercadolivre.com.br/ajuda/40538 (403) | Conflito 50% x 70% segue em aberto; tratar o número como incerto. |
| R5 | SEM FONTE OFICIAL (não reverificada) | YouTube KvVyJlYt6w0 (2026-08-12), via terceiro | Sem acesso a comunicado oficial do ML; "Full Super" segmentado não reconferido. |
| R6 | SEM FONTE OFICIAL (não reverificada) | https://www.mercadolivre.com.br/ajuda/51251 (403) | Página bloqueada; pontos percentuais por categoria não reconferidos. |
| R7 | CONFIRMADA (parcial) | https://www.sec.gov/Archives/edgar/data/1099590/000109959026000021/meli-20260805xex991.htm (2026-08-05) | Carta Q2'26 cita descontos PIX a compradores e desconto de take rate a vendedores desde abril, em certas categorias e faixas de preço, condicionados a preço competitivo. Sem fórmula nem lista de categorias. |
| R8 | SEM FONTE OFICIAL (não reverificada) | /ajuda/16449, /49972, /45023 | Não acessadas nesta passada. |
| R9 | SEM FONTE OFICIAL (não reverificada) | /ajuda/21793 | Não acessada; prazos de estoque antigo não reconferidos. |
| R10 | SEM FONTE OFICIAL (não reverificada) | https://developers.mercadolivre.com.br/pt_br/gerenciar-ofertas (403) | Lista de tipos e quem paga não reconferida. |
| R11 | SEM FONTE OFICIAL (não reverificada) | https://developers.mercadolivre.com.br/pt_br/campanhas-smart-price-matching (403) | Não reconferida; vídeo oficial W1hgC6snin4 não reassistido. |
| R12 | SEM FONTE OFICIAL (não reverificada) | https://developers.mercadolivre.com.br/pt_br/cupons-do-vendedor (403) | Doc de 2025-08-28, pode estar superada; não reconferida. |

Nenhuma afirmação foi CONTESTADA, mas só porque nenhuma fonte contrária foi lida. Refazer R1-R6 e R8-R12 com leitura autenticada ou pelo agente de navegador.
