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

## 11. Verificação pelo navegador (2026-10-15)

Método: leitura das páginas oficiais no Chrome (renderiza JavaScript), sem login, captcha ou aceite de termos. Datas: "sem data" quando a página não traz data de atualização.

| id | veredito | fonte oficial | observação |
|---|---|---|---|
| R1 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/870 (sem data (lida 15/10/2026)) | Clássico sem parcelamento; Premium até 12x sem juros (depende do valor e do meio de pagamento). |
| R2 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/custos-envio-reputacao-verde-mercado-lider_40538 (sem data (lida 15/10/2026)) | As 8 faixas até 0,3 kg batem exatamente (5,65/6,85/8,15/12,95/14,95/16,95/19,05/21,65). |
| R3 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/custos-envio-reputacao-verde-mercado-lider_40538 (sem data (lida 15/10/2026)) | Também confirmados: abaixo de R$ 19 paga no máximo metade do preço; R$ 19–78,99 frete grátis padrão pelo ML; a partir de R$ 79 o vendedor oferece frete grátis rápido; rápido abaixo de R$ 79 é opcional (a partir de R$ 12,95). |
| R4 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/custos-envio-reputacao-verde-mercado-lider_40538 (sem data (lida 15/10/2026)) | A página oficial diz até 50% e que a tabela já inclui o desconto. Os 70% do vídeo 8dZiKLuJWXg não aparecem em fonte oficial. |
| R5 | PARCIAL | https://www.mercadolivre.com.br/ajuda/49972 (sem data (lida 15/10/2026)) | Confirmada a separação no Full Super entre "produtos selecionados" e "demais" (demais custam de ~9% a 50% mais, conforme a faixa). Não aparecem: a data 24/08/2026, o reajuste médio de +1,6% nem "+20–40%". |
| R6 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/51251 (sem data (lida 15/10/2026)) | Alimentos e Bebidas com preço entre R$ 150 e R$ 700: -5 pp no Premium e -3 pp no Clássico em todas as subcategorias listadas. |
| R7 | PARCIAL | https://www.sec.gov/Archives/edgar/data/1099590/000109959026000021/meli-20260805xex991.htm (05/08/2026) | Mantido o veredito da rodada de 14/10 (carta Q2'26). Sem fórmula nem lista de categorias em fonte oficial. |
| R8 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/16449 ; https://www.mercadolivre.com.br/ajuda/49972 ; https://www.mercadolivre.com.br/ajuda/45023 (sem data (lidas 15/10/2026)) | Full Super: preço acima de R$ 8, reputação verde, CD Full, frete grátis a partir de R$ 199; selecionados com custo menor; economia por quantidade ou kit não vale para Supermercado. |
| R9 | CONFIRMADA | https://www.mercadolivre.com.br/ajuda/21793 ; https://www.mercadolivre.com.br/ajuda/quais-custos-estoque-antigo_15731 (sem data (lidas 15/10/2026)) | Supermercado sem diária P/M (G R$ 0,014; XG R$ 0,025) e estoque antigo a partir de 2 meses. Ressalva: /21793 diz de forma genérica que estoque com mais de 2 meses gera custo; /15731 diz 4 meses para os demais produtos. |
| R10 | PARCIAL | https://developers.mercadolivre.com.br/pt_br/gerenciar-ofertas ; https://developers.mercadolivre.com.br/pt_br/campanhas-smart-price-matching (09/06/2026) | 12 tipos e boost (DEAL, PRICE_DISCOUNT, PRE_NEGOTIATED, SMART, PRICE_MATCHING, LIGHTNING) confirmados. A tabela oficial marca bonificação MELI também em VOLUME, PRE_NEGOTIATED e UNHEALTHY_STOCK: a lista de cofinanciadas da nota está incompleta. |
| R11 | CONTESTADA | https://developers.mercadolivre.com.br/pt_br/campanhas-smart-price-matching (09/06/2026) | Há PRICE_MATCHING (cofinanciado) e PRICE_MATCHING_MELI_ALL (100% ML): "sempre cofinanciado" é falso. Duração máxima de 10 dias, não 7. Confirmados: comparação com outros sites e marketplaces e candidatos atualizados diariamente. Aporte que cai sozinho e novo opt-in não aparecem. |
| R12 | CONFIRMADA | https://developers.mercadolivre.com.br/pt_br/cupons-do-vendedor (28/08/2025) | Só MLB, reputação verde, prazo máximo de 31 dias. A doc segue com data de 28/08/2025. |

## 12. Rodada 2 e estado final (2026-10-15)

Base desta seção: seções 10 e 11 desta nota; `verificacao/resultado-mercadolivre.tsv` (linhas preco-promocao R1–R12 e cases-grandes A3/A29); `LACUNAS.md` §1.2, §1.9 e §4; e os arquivos `mercadolivre/rodada2/` (nav-preco-reputacao, balancos-api, sinais-recentes, regulatorio, nav-full-supermercado, nav-observacao, webinars, dados-mercado, evidencias-cases). Nenhuma coleta nova foi feita para esta seção: é só consolidação de leituras já registradas. As páginas da Central de Ajuda seguem sem data e mantêm a marca "(pode estar superada)".

### 12.1 Estado final das afirmações

| id | status final | valor correto | fonte | de onde veio |
|---|---|---|---|---|
| A1 | CONFIRMADA | Clássico 10–14% sem parcelamento; Premium 15–19% com até 12x sem juros. Para Café Moído e em Grão (MLB247538): Clássico 14% e Premium 19% (teto das faixas). O `percentage_fee` pode variar por "outros parâmetros objetivos" e no tempo | https://www.mercadolivre.com.br/ajuda/870 (s/d, lida 15/10/2026); vendedores.mercadolivre.com.br/landing/custos-de-venda (buscador, s/d); developers.mercadolivre.com.br/pt_br/comissao-por-vender (03/09/2026) | seção 11 (R1); rodada2/nav-preco-reputacao (R2-PR-1); rodada2/balancos-api (R2-BA-6); reconciliação §1.9 ([mix R2], [cases A29]) |
| A2 | CONFIRMADA | Custo de envio em toda venda, "mesmo que o comprador pague pelo envio" | https://www.mercadolivre.com.br/ajuda/custos-envio-reputacao-verde-mercado-lider_40538 (s/d, lida 15/10/2026) | seção 11 (R3); rodada2/nav-preco-reputacao (R2-PR-19) |
| A3 | CONFIRMADA | 5,65 / 6,85 / 8,15 / 12,95 / 14,95 / 16,95 / 19,05 / 21,65 até 0,3 kg; 0,5–1 kg: 6,05 / 7,15 / 8,45 / 14,45 nas quatro primeiras faixas; 1–1,5 kg: 6,15 / 7,35 / 8,65 / 14,75 | ajuda/40538 (s/d, lida 15/10/2026) | seção 11 (R2); rodada2/nav-preco-reputacao (R2-PR-19); reconciliação §1.9 ([alim A8]: R$ 6,95 em 0,3–0,5 kg, coerente com a escada) |
| A4 | CONFIRMADA | Abaixo de R$ 19, no máximo metade do preço | ajuda/40538 | seção 11 (R3); rodada2/sinais-recentes (R2-SIN-12) |
| A5 | CONFIRMADA (divergência 50% × 70% resolvida a favor de 50%) | Verde ou MercadoLíder: até 50%, já embutido na tabela; amarela: até 40%; laranja e vermelha: sem desconto. O "até 70%" (vídeo de 28/05/2026, tabela logada) não aparece em nenhuma página pública atual e fica como superado | ajuda/40538; ajuda/40545; ajuda/40547 (s/d, lidas 15/10/2026); 8dZiKLuJWXg ~2:00 | seção 11 (R4); rodada2/sinais-recentes (R2-SIN-9, R2-SIN-10); rodada2/nav-preco-reputacao (R2-PR-19) |
| A6 | CONFIRMADA | R$ 19–78,99: frete grátis padrão oferecido pelo ML; a partir de R$ 79: frete grátis rápido pago pelo vendedor; rápido abaixo de R$ 79 é opcional, a partir de R$ 12,95. Para assinantes MELI+, entrega rápida a partir de R$ 19 desde out/2025 | ajuda/40538; Carta 3T25 (SEC 8-K Ex-99.1, 29/10/2025) | seção 11 (R3); rodada2/balancos-api (R2-BA-8) |
| A7 | PARCIAL | A data de **24 de agosto** para a nova tabela geral de envio tem página oficial (ajuda/48578, ano não escrito; 2026 por contexto). O "+1,6% em média" e o "+20–40%" do Full Super "demais" seguem sem fonte oficial. Praticante com e-mail na tela fala em "cerca de R$ 0,90" por envio, o que diverge do ≈ R$ 0,46 de KvVyJlYt6w0 | https://www.mercadolivre.com.br/ajuda/48578 (s/d, lida 15/10/2026); KvVyJlYt6w0 (12/08/2026); Mj-oOzE0ZuE ~0:30 (02/09/2026) | seção 11 (R5); rodada2/nav-full-supermercado (R2-FS-10); rodada2/sinais-recentes (R2-SIN-29) |
| A8 | CONFIRMADA (ampliada) | −5 pp no Premium e −3 pp no Clássico entre R$ 150 e R$ 700 em Café Moído e em Grão e também em Cápsulas, Café Solúvel, Infusões e Cremes para Café. Combinado com A1, café em grão ou moído nessa faixa ficaria em cerca de 11% (Clássico) e 14% (Premium): inferência aritmética, sem página que mostre o valor final | https://www.mercadolivre.com.br/ajuda/51251 (s/d, lida 15/10/2026) | seção 11 (R6); rodada2/balancos-api (R2-BA-4); rodada2/nav-preco-reputacao (R2-PR-3) |
| A9 | PARCIAL | Enunciado confirmado em N2: desde abril/2026, desconto no PIX ao comprador e desconto de take rate ao vendedor "in certain categories and ASP ranges", condicionados a preço competitivo. Acréscimos: não é corte da plataforma toda; houve redução da tarifa de envio ao vendedor no fim do 1T26 (call, transcrição de terceiro). Seguem sem fonte: fórmula do índice, lista de categorias, % do PIX, "−1 p.p." e "armazenagem grátis no Full" | https://www.sec.gov/Archives/edgar/data/1099590/000109959026000021/meli-20260805xex991.htm (05/08/2026); call 1T26 (07/05/2026, roic.ai) | seção 11 (R7); rodada2/balancos-api (R2-BA-12, R2-BA-13, R2-BA-14) |
| A10 | CONFIRMADA (com divergência oficial interna) | Preço acima de R$ 8 (com exceções comerciais), reputação verde, categoria de supermercado, estoque no Full; frete grátis na loja Full Super a partir de R$ 199; o ML pode abrir exceções por marca. A mesma página diz "Fora da loja, o frete é grátis a partir de R$ 79", o que não bate com o R$ 19 da ajuda/40538 | https://www.mercadolivre.com.br/ajuda/16449 (s/d, lida 15/10/2026) | seção 11 (R8); rodada2/nav-full-supermercado (R2-FS-7); rodada2/balancos-api (R2-BA-29); reconciliação §1.9 ([log R8], [alim A5–A7]) |
| A11 | CONFIRMADA | Abaixo de R$ 29, no máximo 25% do preço; "selecionados" mais baratos que "demais" até 8 kg (ex.: R$ 29–48,99: R$ 1,60 × R$ 2,40; R$ 49–78,99: R$ 2,40 × R$ 3,60); a partir de R$ 199 as duas tabelas são iguais. Ressalva aberta: a rodada 2 rotula essa linha de valores como "até 1 kg", e esta nota (seção 4, N8; seção 5) como "até 0,3 kg"; os valores coincidem, o rótulo de peso precisa de releitura | https://www.mercadolivre.com.br/ajuda/49972 (s/d, lida 15/10/2026) | seção 11 (R8); rodada2/nav-full-supermercado (R2-FS-8) |
| A12 | CONFIRMADA | Economia de envio por quantidade ou kit não vale na seção Supermercado | https://www.mercadolivre.com.br/ajuda/45023 (s/d, lida 15/10/2026) | seção 11 (R8) |
| A13 | CONFIRMADA | Supermercado: armazenagem diária P e M grátis (G R$ 0,014; XG R$ 0,025); estoque antigo a partir de 2 meses no Supermercado e de 4 meses nos demais produtos (resolve a ressalva da seção 11 sobre "2 meses genérico") | https://www.mercadolivre.com.br/ajuda/24253; https://www.mercadolivre.com.br/ajuda/15373; ajuda/21793 (s/d, lidas 15/10/2026) | seção 11 (R9); rodada2/nav-full-supermercado (R2-FS-11, R2-FS-14); reconciliação §1.9 ([log R2], [alim A4]) |
| A14 | PARCIAL (lista corrigida) | 12 tipos confirmados (DEAL, MARKETPLACE_CAMPAIGN, PRICE_DISCOUNT, LIGHTNING, DOD, VOLUME, PRE_NEGOTIATED, SELLER_CAMPAIGN, SMART, PRICE_MATCHING, UNHEALTHY_STOCK, SELLER_COUPON_CAMPAIGN). Com bonificação do ML: MARKETPLACE_CAMPAIGN, VOLUME, PRE_NEGOTIATED, SMART, PRICE_MATCHING e UNHEALTHY_STOCK; sem bonificação: DEAL, DOD, LIGHTNING e SELLER_CAMPAIGN. PRICE_MATCHING_MELI_ALL é 100% ML. A lista de cofinanciadas da tabela 8 (só três tipos) estava incompleta | https://developers.mercadolivre.com.br/pt_br/gerenciar-ofertas (09/06/2026) | seção 11 (R10); rodada2/nav-preco-reputacao (R2-PR-15) |
| A15 | CONFIRMADA | O ML "pode aplicar um desconto automático sobre a oferta base", compensado como redução nos custos por venda (`boosted_offer`, `discount_meli_boost_amount`); campos `meli_percentage` e `seller_percentage` por oferta | gerenciar-ofertas (09/06/2026) | seção 11 (R10); rodada2/nav-preco-reputacao (R2-PR-16) |
| A16 | PARCIAL | Confirmado: LIGHTNING exige estoque e não tem bonificação padrão do ML. Não reconferidos na rodada 2: "encerra ao esgotar" e "não pode ser removida depois de ativa" | gerenciar-ofertas (09/06/2026) | rodada2/nav-preco-reputacao (R2-PR-15) |
| A17 | CONFIRMADA | Só MLB, reputação verde, prazo máximo de 31 dias, acumulativo com a promoção ativa, um cupom por venda (doc de 28/08/2025, pode estar superada) | https://developers.mercadolivre.com.br/pt_br/cupons-do-vendedor (28/08/2025) | seção 11 (R12) |
| A18 | ABERTA | Contradição oficial interna persiste: a tabela geral (09/06/2026) marca VOLUME com bonificação do ML; a doc específica de VOLUME do vendedor (23/01/2025) diz que o ML não entra com coparticipação. A doc de 2025 não foi relida | gerenciar-ofertas (09/06/2026); developers, Volume (23/01/2025) | rodada2/nav-preco-reputacao (R2-PR-15) |
| A19 | CONTESTADA → valor correto | PRICE_MATCHING é cofinanciado e PRICE_MATCHING_MELI_ALL é 100% financiado pelo ML ("sempre cofinanciado" é falso); duração máxima de **10 dias** no preço competitivo (SMART: 30), não 7; candidatos atualizados diariamente; referência inclui outros sites e marketplaces. "Aporte cai sozinho" e "aumento pede novo opt-in" só têm a fala do webinar (W1hgC6snin4), sem texto escrito | https://developers.mercadolivre.com.br/pt_br/campanhas-smart-price-matching (09/06/2026); W1hgC6snin4 (03/06/2026) | seção 11 (R11); rodada2/nav-preco-reputacao (R2-PR-17) |
| A20 | CONFIRMADA (com acréscimos) | Fatores: preço, parcelamento sem juros, Full, frete grátis e envio no mesmo dia; `winning` = maximum, `sharing_first_place` = medium, `competing` = minimum. Motivos de exclusão incluem também `non_trusted_seller`, `item_not_opted_in`, `item_paused` e estados temporários | https://developers.mercadolivre.com.br/pt_br/concorrencia-em-catalogo (21/07/2026) | reconciliação com a verificação de [rank A4–A6] (frente ranqueamento-anuncio) |
| A21 | ABERTA | Fala oficial em webinar, sem número publicado; o webinar não foi reassistido na rodada 2 | W1hgC6snin4 (03/06/2026) | sem mudança |
| A22 | SEM FONTE OFICIAL | Nenhuma página diz que o ML "detecta lista inflada depois de publicada". O que existe em fonte oficial é correlato: `max_discounted_price` limita o preço promocional para "descontos críveis" e `suggested_discounted_price` usa o histórico do item (critério não publicado); a automação valida piso e teto contra 60 dias | gerenciar-ofertas (09/06/2026); automatizacoes-de-precos (01/10/2026) | rodada2/regulatorio (R2-REG-35); rodada2/nav-preco-reputacao (R2-PR-18) |
| A23 | CONFIRMADA (com acréscimos) | INT_EXT ("dentro e fora do Mercado Livre", inclui outros sites e buscadores como o Google) e INT; `min_price` obrigatório; erro "unusual value" contra os últimos 60 dias; PUT de preço rejeitado ou ignorado desde 18/03/2026; etiqueta "Recomendado" e distinção VIP. Novo: a automação **é pausada quando o item entra em promoção**; no catálogo exige reputação amarela, verde-clara ou verde | https://developers.mercadolivre.com.br/pt_br/automatizacoes-de-precos (01/10/2026); nota "venda-mais-com-ajustes-automaticos-de-preco" (s/d) | rodada2/nav-preco-reputacao (R2-PR-18); rodada2/sinais-recentes (R2-SIN-17) |
| A24 | PARCIAL | Confirmado: a referência usa produtos semelhantes "tanto na plataforma Mercado Livre quanto em outras" e os status de benchmark. A frase "melhora o posicionamento nos resultados de busca" não foi reconferida na rodada 2 | https://developers.mercadolivre.com.br/pt_br/referencias-de-precos (17/12/2025) | reconciliação com [cases A3] (TSV, PARCIAL); rodada2/sinais-recentes (R2-SIN-17) |
| A25, A26, A27, A30 | SEM FONTE OFICIAL (prática ou case, não verificável em N1) | Sem mudança. A30 é princípio de cálculo, não regra da plataforma | ilZ92K2U_2k; F_3Wy-Xsvx8; iAM5PWaVV08; POjujir152o | sem mudança |
| A28 | PARCIAL | A parte "promoção + cupom somam" está confirmada (doc de cupons). "Só a de maior desconto fica ativa" segue só em praticante | cupons-do-vendedor (28/08/2025); G0lNX-1_754 | seção 11 (R12) |
| A29 | SEM FONTE OFICIAL | A comissão sobre o preço promocional final segue só em tela de praticante; a doc "Custos por vender" não diz isso com essas palavras | G0lNX-1_754 | sem mudança |
| A31, A32, A33 | ABERTA | Falas oficiais em vídeo (webinar e podcast), não reassistidas na rodada 2 | -NK3VLYm0q0; hvXa7Pr0mp4 | sem mudança |
| A34 | SEM FONTE OFICIAL (N4 via imprensa) | Sem mudança. Contexto novo: 1º semestre de 2026 com R$ 208,4 bi (+16,9%) e tíquete de R$ 275,50 (−13,3%), também sem método publicado | Confi Neotrust via Exame; Confi/E-commerce Brasil via GiroNews (28–29/07/2026) | rodada2/dados-mercado (R2-DAD-05) |
| A35 | SEM FONTE OFICIAL N1/N2 (OFICIAL via terceiro) | Sem mudança | Mundo do Marketing (14/11/2025) | sem mudança |
| A38, A39 | SEM FONTE OFICIAL (fora do escopo desta frente) | Valores de Shopee e Amazon seguem via terceiro; tratados nas frentes dessas plataformas (LACUNAS §4 P0) | R4CkSr5c6Jw; Anymarket | sem mudança |
| A40 | ABERTA | A ajuda/56258 (atacado) não foi relida em 15/10/2026; não se sabe se ainda mostra a tabela anterior | /ajuda/56258 | sem mudança |

Afirmações fora da tabela 8 que mudaram de estado:
- **Seção 6, mitos 1 e 2 (custo fixo abaixo de R$ 79 / R$ 12,50):** resolvidos por fonte oficial datada. Desde **02/03/2026** no Brasil, abaixo do limite de frete grátis obrigatório (TH), só o Flex cobra custo fixo entre os modos ME2; Coleta, Places, Drop off, Turbo e Full não cobram; ME1 e envio personalizado cobram; acima do TH não há custo fixo (developers "Custos por vender", 03/09/2026). A nota da Central com "50% abaixo de R$ 12,50" e "três faixas até R$ 79" segue no ar, sem data, e descreve a regra anterior. Fonte: rodada2/balancos-api (R2-BA-5); rodada2/sinais-recentes (R2-SIN-11, R2-SIN-12); rodada2/nav-preco-reputacao (R2-PR-20).
- **Seção 6, mito 8 ("60 dias antes da Black Friday"):** CONTESTADA. Nenhuma lei ou decreto federal proíbe mudar o preço antes de uma data nem fixa janela de preço de referência. A origem provável é a recomendação do Procon-SP (2019, repetida em 2025) de "aplicar desconto sobre o menor preço dos últimos 60 dias", que é base de cálculo do desconto, não proibição. Fonte: rodada2/regulatorio (R2-REG-25, R2-REG-26).
- **Seção 2.1, parcelas do Premium:** completadas. R$ 30–59,99: 2x (4x no Cartão MP); R$ 60–99,99: 3x (5x); R$ 100–149,99: 4x (6x); R$ 180–299,99: 6x (8x); MELI+ com até 3 parcelas extras abaixo de R$ 900 (ajuda/22737). Fonte: rodada2/balancos-api (R2-BA-7).

### 12.2 Reconciliações aplicadas (LACUNAS §1.9)

| Reconciliação | Como fica nesta frente |
|---|---|
| Tabela de envio, R$ 6,95 e desconto de até 50% [pre R1–R4] ← [alim A8] (ajuda/40538) | Aplicada e superada pela leitura direta da seção 11 (R2, R3 e R4 CONFIRMADAS) e da rodada 2 (R2-PR-19). O R$ 6,95 de [alim A8] é a faixa 0,3–0,5 kg em R$ 19–48,99, coerente com os R$ 6,85 até 0,3 kg desta nota. |
| Tarifa Clássico e Premium [pre R1; cases A29] ← [mix R2] (ajuda/870) | Aplicada. R1 CONFIRMADA na seção 11 e [cases A29] CONFIRMADA no TSV. Acréscimo: percentual do café (14% / 19%) pelo buscador da landing (R2-PR-1). |
| Estoque antigo de Supermercado [log R2] ← [alim A4] (ajuda/15373) | Aplicada a A13: 2 meses no Supermercado e 4 meses nos demais, com valores (R2-FS-14). Ressalva de citação: a seção 11 cita "quais-custos-estoque-antigo_15731", e LACUNAS e a rodada 2 citam ajuda/15373; o conteúdo é o mesmo, o id precisa de conferência. |
| Full Super: R$ 8, sem armazenagem P/M, R$ 199 [log R8] ← [alim A5–A7] (ajudas 16449 e 49972) | Aplicada a A10, A11, N7 e N8 (seção 11, R8; R2-FS-7, R2-FS-8). Fica registrada a divergência oficial interna "R$ 79 fora da loja" (16449) × "R$ 19" (40538). |
| Painel Concorrência [cases A8] ← [mix R6] | Aplicada à seção 3.3. O painel oficial existe e mostra, por concorrente (com apelido e números aproximados), o % de vendas com frete grátis, parcelamento, Full, Flex, **promoções, cupons**, publicidade, clips e catálogo, além de até 50 anúncios com vendas e conversão aproximadas. É ferramenta de leitura de concorrência, não um índice de preço; não muda Q4. |

As demais linhas de §1.9 (MercadoLíder, refrigerados no Full, isenção de 180 dias) não tocam esta frente.

Reconciliações adicionais entre arquivos da rodada 2:
- **Custo fixo:** sinais-recentes trata o tema como "duas páginas oficiais que não batem"; balancos-api traz a página developers datada (03/09/2026) com a vigência de 02/03/2026. A leitura conciliada é que a nota da Central está desatualizada. Fica aberto só o valor numérico do TH, que a página não informa.
- **Data de 24/08:** a ajuda/48578 confirma a data da tabela geral (R2-FS-10); a divisão "selecionados/demais" do Full Super não tem data oficial.

### 12.3 Achados novos da rodada 2 desta frente

| id | achado | fonte | confiança |
|---|---|---|---|
| R2-PR-1 | Café Moído e em Grão: Clássico 14%, Premium 19%; o Premium inclui a taxa por oferecer parcelamento sem juros | landing custos-de-venda (buscador) | média-alta (leitura única; ver 12.5 sobre a sessão) |
| R2-PR-2 / R2-BA-1 / R2-BA-2 | `listing_prices` deixou de ser pública (403 PolicyAgent); simulador e landing de tarifas por categoria redirecionam para login. A tarifa por faixa de preço e tipo de anúncio depende de token ou sessão | api.mercadolibre.com; mercadolivre.com.br/simulador-de-custos | alta |
| R2-BA-3 | IDs: Café Moído e em Grão MLB247538; Cápsulas MLB247540 (fora do nó Café); Café Solúvel MLB247537; preço mínimo de R$ 8 nas três folhas | api.mercadolibre.com/categories | alta |
| R2-BA-4 | A redução da 51251 vale também para Cápsulas, Café Solúvel, Infusões e Cremes para Café | ajuda/51251 | alta |
| R2-PR-3 | Café entre R$ 150 e R$ 700: cerca de 11% (Clássico) e 14% (Premium), por inferência | landing + 51251 | média |
| R2-BA-5 | Nova lógica de custo fixo desde 02/03/2026 (só Flex, ME1 e personalizado abaixo do TH) | developers comissao-por-vender (03/09/2026) | alta |
| R2-BA-6 | O `percentage_fee` pode variar por parâmetros além de categoria e tipo, e no tempo, na faixa com redução | idem | alta |
| R2-BA-7 | Escada completa de parcelas sem juros do Premium (ver 12.1) | ajuda/22737 | alta |
| R2-BA-8 a R2-BA-11 | MELI+: entrega rápida a partir de R$ 19 desde out/2025; Essencial a R$ 9,90 por mês; assinantes +72% a/a no 2T26; frete grátis lento com contribuição positiva em metade das faixas de R$ 19–79 | Cartas 3T25, 4T25, 1T26 e 2T26 (SEC) | alta |
| R2-BA-12 a R2-BA-14 | O pacote de abril/2026 é por categoria e faixa de preço; inclui corte de tarifa de envio ao vendedor no fim do 1T26; nenhum N2 cita "−1 p.p." ou armazenagem grátis | Carta 2T26; calls 1T26 e 2T26 | média-alta (calls por transcrição de terceiro) |
| R2-PR-15 a R2-PR-17 | Tabela oficial de bonificação por tipo de promoção; separação `meli_percentage`/`seller_percentage`; boost; price matching de 10 dias e SMART de 30 | gerenciar-ofertas; campanhas-smart-price-matching | alta |
| R2-PR-18 | A automação pausa ao entrar em promoção; exigência de reputação no catálogo | automatizacoes-de-precos (01/10/2026) | alta |
| R2-PR-21 | O valor recebido exclui publicidade, custos do Full e "Minha página"; o ML não retém impostos (reconfirma a seção 2.1) | ajuda/44007 | alta |
| R2-SIN-9 | Desconto de envio por reputação: amarela até 40%; laranja e vermelha sem desconto | ajudas 40545 e 40547 | alta |
| R2-SIN-17 / R2-SIN-18 | A comparação com preço externo é oficial (referências, automação com Google); aviso, 3 dias e perda de visibilidade por preço externo seguem só na imprensa (24/10/2025), sem comunicado novo nos últimos 60 dias | developers referencias-de-precos; Mercado&Consumo | alta / média |
| R2-FS-8 / R2-FS-9 | Full Super: diferença selecionados × demais só até 8 kg; a lista de selecionados é um PDF no CDN do ML, não aberto; vale automaticamente para publicações ligadas ao catálogo; critério não publicado | ajuda/49972 | alta (PDF não lido) |
| R2-FS-10 | Página oficial "Custos do Envios ... a partir de 24 de agosto" | ajuda/48578 | média (ano inferido) |
| R2-REG-23 | No comércio eletrônico, o preço à vista deve vir junto à imagem, em fonte de no mínimo 12 | Lei 10.962/2004, art. 2º, III | alta |
| R2-REG-25 a R2-REG-29 | "De/por": publicidade enganosa inclui preço (CDC, art. 37), ônus da prova do anunciante (art. 38), crime (arts. 66 e 67); atribuir preços distintos ao mesmo item é infração no comércio eletrônico (Decreto 5.903/2006); recomendação do Procon-SP de desconto sobre o menor preço de 60 dias; o PL 5925/2025 (inflar preço para simular desconto) não é lei | Planalto; procon.sp.gov.br; camara.leg.br | alta |
| R2-REG-30 | A Portaria Senacon 61/2026 vale para transporte e entrega, não para marketplace de bens | Nota Técnica 3/2026/DPDC | alta |
| R2-REG-35 | `max_discounted_price` limita o preço promocional para "descontos críveis"; `suggested_discounted_price` vem do histórico; critério numérico não publicado | gerenciar-ofertas (09/06/2026) | média |
| R2-OBS-8 | Itens de R$ 19,40 e R$ 23,99 exibiram "Frete grátis ou rápido" no card, em sessão logada. Coerente com o frete grátis padrão de R$ 19–78,99 e com a entrega rápida do MELI+ a partir de R$ 19; não se apurou se depende da conta | nav-observacao (15/10/2026) | média |
| R2-DAD-04 | Black Friday 2024: Alimentos e Bebidas foi a 8ª categoria em intenção (9,8%) e a 4ª em compra realizada (14,1%) | Webshoppers 51 (NIQ Ebit) | média |
| webinar (sem id) | Cupom de carrinho abandonado recupera "pelo menos 7%" das vendas perdidas: dado do ML, sem método | nJlDztc3WGk 47:30 (10/03/2026) | baixa como número |

Não pertencem a esta frente e não foram usados aqui: a bonificação de campanha relâmpago do Mercado Ads (R2-WEB-24, que é orçamento de Ads), os achados de reputação (R2-PR-4 a R2-PR-14), Full e logística (R2-FS-1 a 7 e 11 a 21, salvo onde citados em 12.1), o regulatório de alimentos (R2-REG-1 a 22 e 31 a 34) e os experimentos de ranqueamento e logística (evidencias-cases).

### 12.4 Perguntas do protocolo (§7.2)

| Q | estado | motivo |
|---|---|---|
| Q1 Estrutura de custo com vigência | **R** | Tarifa por tipo (A1) e por categoria para café (R2-PR-1), redução 51251 ampliada (R2-BA-4), custo fixo com vigência de 02/03/2026 (R2-BA-5), tabela de envio com data de 24/08 (A2–A6, R2-FS-10), parcelas (R2-BA-7) e Full Super (A10–A13). Resíduos: valor numérico do TH; tarifa da seção Supermercado ("pagam outras tarifas", sem percentual público); percentual-base de Cápsulas; "+1,6%" sem fonte oficial. |
| Q2 Preço na exposição | **P** | Oficial: fatores do catálogo e `price_to_win` (A20), referência de preço com concorrentes internos e externos (A24), automação INT_EXT (A23), descontos condicionados a preço competitivo (A9). Falta: comunicado oficial de alerta ou punição por preço externo (só imprensa, R2-SIN-18), fórmula do índice de competitividade e regra de paridade (não existe em fonte lida). |
| Q3 Preço mínimo e preço-alvo | **R** | Método de praticantes com planilha em tela (seção 3.4), piso obrigatório na automação (A23) e custos que entram na conta confirmados (A2–A4, R2-PR-21, R2-BA-5). |
| Q4 Medição de competitividade | **S** | Não há prática documentada no BR de índice par a par ou ponderado, % de buy box de portfólio ou preço contra a mediana da 1ª página. O painel Concorrência (12.2) mostra o uso de alavancas por concorrente, não um índice de preço. |
| Q5 Ferramentas promocionais e quem paga | **R** | 12 tipos e bonificação por tipo reconferidos (A14, R2-PR-15), separação `meli_percentage`/`seller_percentage` e boost (A15), cupons (A17), price matching corrigido (A19), frete grátis por faixa (A6). Resíduos: VOLUME com contradição interna (A18); PIX cofinanciado com doc de 29/04/2025 não relida. |
| Q6 Efeito da promoção separando subsídio e desconto | **S** | A API separa os aportes por item (R2-PR-16), então a medição é possível na primeira parte, mas não há estudo, holdout nem dado público de efeito. A rodada 2 de evidências não achou experimento publicado sobre promoção. |
| Q7 Como evitam guerra de preço | **R** | Piso obrigatório e pausa da automação em promoção (A23), opção de não acompanhar o price matching (seção 3.5), kits e linha de formatos (seção 3.5), redução 51251 na faixa de R$ 150–700 (A8). |
| Q8 Calendário e preparação | **P** | Não há calendário oficial de 2026 com prazos de adesão em página pública; a Black Friday de 27/11/2026 é cálculo; a preparação vem de falas oficiais em vídeo (A31, A32). Acréscimos: quadro legal de "de/por" para a Black Friday (R2-REG-25 a 29) e peso de Alimentos e Bebidas na Black Friday de 2024 (R2-DAD-04). |

### 12.5 Contaminação verificada

**Nenhuma contaminação encontrada.** Conferi as afirmações da seção 11 e as da rodada 2 usadas acima. Todas citam URLs do Mercado Livre (mercadolivre.com.br, vendedores.mercadolivre.com.br, developers.mercadolivre.com.br, api.mercadolibre.com), da SEC ou de órgãos públicos brasileiros. Nenhuma cita URL da Shopee ou da Amazon, e os trechos citados batem com a URL de cada uma. As menções a Shopee e Amazon nos arquivos da rodada 2 (regulatorio R2-REG-7 e R2-REG-9; dados-mercado; evidencias-cases) são comparações explícitas ou notícias que envolvem várias plataformas, e não foram usadas aqui.

Pontos que não são contaminação, mas pedem cuidado:
1. **R2-PR-1 (café 14% / 19%):** veio do buscador da landing `/landing/custos-de-venda`, no Chrome. Outras duas sessões registram que `/landing/custos-de-venda` (sinais-recentes) e `/landing/custos-de-venda/tarifas-de-venda` (balancos-api) exigem login. O mesmo Chrome tinha uma sessão de conta já aberta (nav-observacao: sessão de comprador "já aberta e logada"; nav-preco-reputacao: a busca da Central caiu no painel logado). O valor é coerente com as faixas oficiais (teto de 10–14% e 15–19%) e por isso foi mantido, mas com confiança média-alta e a ressalva de que pode ter sido servido a uma sessão autenticada.
2. **Id da página de estoque antigo:** a seção 11 cita `quais-custos-estoque-antigo_15731`; LACUNAS §1.9 e nav-full-supermercado citam ajuda/15373. O conteúdo descrito é o mesmo; tratei como divergência de citação.
3. **Valores de armazenagem do Supermercado (G R$ 0,014; XG R$ 0,025):** a seção 11 os atribui à ajuda/21793; a rodada 2 os leu na ajuda/24253. O conteúdo bate; a página de origem precisa ser conferida.
4. **Rótulo de peso da tabela do Full Super:** "até 1 kg" (rodada 2) × "até 0,3 kg" (seções 4 e 5 desta nota), com os mesmos valores. Fica para releitura.
5. **R2-OBS-8:** observado em sessão logada; o selo "Frete grátis ou rápido" pode depender de a conta ser assinante MELI+.
