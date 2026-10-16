# Lacunas da pesquisa: Mercado Livre, Shopee e Amazon (Brasil)

Crítico de completude · 2026-10-14 · Base lida: `metodo/protocolo.md`, os três `CONSOLIDADO.md`, as seções 9 (Lacunas) e 10 (Verificação) das 24 notas de frente, as notas `social/` e os arquivos de `observacao/`.

**Para que serve.** Lista o que falta para a pesquisa cumprir o checklist do protocolo (§8). Para cada plataforma e frente, mostra:
- as perguntas do protocolo (§7) sem resposta ou com resposta parcial;
- as afirmações importantes sem fonte oficial lida, ou contestadas;
- as camadas de fonte que faltaram.

No fim vem a lista priorizada da próxima rodada. A pesquisa segue neutra: aqui não há recomendação a nenhuma empresa.

**Legenda.**
- Pergunta: **R** = respondida com fonte · **P** = parcial (falta N1, falta número ou só há praticante) · **S** = sem evidência.
- Camadas:
  - **Oficial:** N1 lido em texto, ou N2.
  - **Dados:** N4 e N5.
  - **Obs.:** N3, observação direta com protocolo.
  - **Social:** N6 a N8, criadores e comentários.
- Estado de cada camada: OK · fraca · ausente.
- Os códigos entre colchetes remetem às notas. Exemplo: [rep A16] = afirmação A16 da nota `reputacao-atendimento`.

---

## 0. Diagnóstico transversal (vale para as três plataformas)

1. **A causa principal das lacunas é de acesso, não de inexistência.** A cota de busca na web acabou no início da coleta, em todas as frentes. Além disso:
   - o Centro de Educação da Shopee e a Central de Ajuda (help.shopee.com.br) carregam por JavaScript;
   - a Central de Ajuda do ML respondeu 403 ou veio vazia para parte das frentes;
   - o Seller Central da Amazon exige login, e as ajudas de comprador da Amazon deram HTTP 503.

   Boa parte do que está "sem fonte oficial" pode ser fechada só com um leitor que renderize JavaScript, sem login.
2. **Inconsistência entre frentes da mesma plataforma.** A mesma página foi lida por uma frente e dada como ilegível por outra. Isso deixou afirmações "não reconf." que já estão confirmadas em outra nota. Ver a lista em §1.9, §3.9 e §2.9. A correção não custa coleta nova: basta reconciliar.
3. **A camada Dados (N4/N5) está quase vazia nas três plataformas.** Não foram acessados:
   - estudos: NIQ Ebit Webshoppers, Neotrust/Confi, Conversion, ABComm;
   - ferramentas brasileiras: Nubimetrics (relatórios recentes), Real Trends, Avantpro, UpSeller, JoomPulse;
   - benchmarks: Pacvue (403), Perpetua (404), Jungle Scout Benchmark 2026 (atrás de formulário), SmartScout e Helium 10 para o BR.

   O que há de dado é blog de ERP (Bling, Magis5, UpSeller) sem metodologia. A exceção é a Amazon, com Jungle Scout/PODEAN (3.500 marcas), Skai e Marketplace Pulse, todos com recorte global ou dos EUA.
4. **A observação direta (N3) não seguiu o protocolo de §3**, que pede data, hora, URL, termo, CEP, logado ou não e print.
   - **ML:** 13 páginas, CEP de MG, sem hora e sem print; o rótulo "Patrocinado" não foi capturado.
   - **Shopee:** 1 página de busca; parou na exigência de login.
   - **Amazon:** 11 linhas, sem CEP, sem hora e sem print.
   - Nas três: nenhuma repetição em outro horário ou dia, e quase tudo concentrado em "café". Fora de alimentos, só o ML tem 3 categorias.
5. **Causalidade zero.** Em nenhuma das 24 frentes há teste de pausa, *holdout* ou geo-teste público, seja sobre Ads × orgânico, efeito do fulfillment, efeito da promoção, recuperação após ruptura ou tempo para ranquear. Hoje essas perguntas são respondidas só com atribuição e opinião. O protocolo pede que se registre "sem evidência suficiente" com motivo, e isso foi feito; mas ninguém procurou literatura acadêmica ou experimentos publicados pelas próprias plataformas (Amazon Science, papers sobre ranqueamento de marketplace).
6. **Nenhum benchmark por categoria com método** no Brasil, em nenhuma das três plataformas: CPC, CTR, CVR, ACOS, TACOS, devolução, tempo de resposta, recompra.
7. **Nenhum case auditável.** Todos os cases das três plataformas são autodeclarados e foram rebaixados a [PRÁTICA] C, o que está correto. Faltou procurar cases com período e base em fontes de indústria: prateleira digital (Lett/Neogrid, Profitero), releases com auditoria e entrevistas em veículos de negócios.
8. **Regras com data anterior a 2026-04-14 (ou sem data) que sustentam números centrais.** São as primeiras a reverificar:
   - **ML:**
     - qualidade das publicações: 31/01/2025;
     - tabela de reputação em developers: 11/08/2025, desatualizada no corte de vendas;
     - desconto por quantidade: 23/01/2025;
     - variações: 29/12/2025;
     - `/trends`: 27/05/2025;
     - toda a Central de Ajuda, que não tem data.
   - **Amazon:**
     - comissões: 20/01/2025;
     - tabela FBA: 01/08/2025;
     - `/termos/frete19`: 15/08/2025;
     - Programe e Poupe (EUA): 25/08/2025;
     - blog de SEO (EUA): 03/09/2025.
   - **Shopee:**
     - critérios do Vendedor Indicado: card de 18/03/2026;
     - termos de logística dos Pontos (help 124091): 16/02/2023;
     - portal de Ads sem data.
9. **País trocado (sinal fraco 7 do protocolo), mais comum na Amazon.** Várias regras [OFICIAL] da Amazon vêm de sell.amazon.com (EUA): SEO, Gerenciar experimentos, Programe e Poupe, taxas do Vine em US$, IPI. Estão marcadas como EUA nas notas, mas o consolidado usa algumas como mecânica válida para o BR sem N1 brasileiro.
10. **Viés da camada social.** As três notas `social/` só usam Instagram e TikTok, com transcrição automática (whisper small) e erros de reconhecimento declarados. Cerca de metade dos posts da Amazon é captação de curso. A camada N8 (fóruns, comentários, Reclame Aqui) foi usada só uma vez, no ML, para detectar mudança de regra, que é o uso que o protocolo prevê.

---

## 1. Mercado Livre

**Atualização de 2026-10-15.** Esta seção foi revista depois da rodada 2. Base: a §12 (estado final) das oito notas de frente em `mercadolivre/<frente>/notas.md` e o `mercadolivre/CONSOLIDADO.md` (versão final de 15/10). Não houve coleta nova nesta revisão: só leitura de arquivos. O texto original de 14/10 foi mantido em cada item. A marca de estado vem antes dele, e a fonte ou o motivo vem depois de "→".

**Legenda do estado (só nesta seção).**
- **FECHADO:** respondido com fonte, que vai citada. Inclui a resposta negativa documentada, quando uma fonte oficial confirma que o dado não é divulgado ou que a regra não existe.
- **PARCIAL:** parte respondida e parte pendente; o resíduo é indicado.
- **ABERTO:** sem resposta. O motivo é um destes: exige login de vendedor; sem fonte pública; precisa de medição própria ou série temporal; não foi relido.

Todas as páginas da Central de Ajuda e da Central de Vendedores seguem sem data. Toda regra dada como FECHADA vale como "vigente na leitura de 14 e 15/10/2026".

### Quadro-resumo da §1 (estado em 15/10/2026)

| Bloco | Itens | FECHADO | PARCIAL | ABERTO |
|---|---|---|---|---|
| 1.1 ads | 13 | 2 | 8 | 3 |
| 1.2 preco-promocao | 11 | 5 | 4 | 2 |
| 1.3 logistica-estoque | 8 | 3 | 3 | 2 |
| 1.4 ranqueamento-anuncio | 10 | 4 | 3 | 3 |
| 1.5 produto-mix | 8 | 1 | 0 | 7 |
| 1.6 reputacao-atendimento | 7 | 2 | 1 | 4 |
| 1.7 alimentos-marca-propria | 10 | 5 | 3 | 2 |
| 1.8 cases-grandes | 8 | 2 | 3 | 3 |
| **Subtotal das lacunas (1.1 a 1.8)** | **75** | **24** | **25** | **26** |
| 1.9 reconciliações internas | 8 | 8 | 0 | 0 |
| **Total da §1** | **83** | **32** | **25** | **26** |

**Leitura.** Fecharam sobretudo as regras escritas da plataforma: tarifas, envio, custo fixo, Full, reputação, experiência de compra e regulatório do café. O que segue aberto tem três causas. A primeira é a medição de efeito: Ads, Full, medalha, edição de anúncio e ruptura. A segunda são os painéis logados. A terceira são números que a plataforma não publica. Nenhum item aberto se resolve com mais leitura de página pública.

**Só se resolve com acesso logado de vendedor**
1. Janela de atribuição do Product Ads, 14 × 15 dias (painel do Ads) [ads A10].
2. Requisitos do Product Ads, texto × fala, testados na elegibilidade de uma conta nova [ads A6; rep A16].
3. Benchmarks de Ads por categoria no Brasil (Ads Center e portal do Mercado Ads) [ads Q7].
4. Painel Concorrência aplicado a café: share por vendedor e uso de Ads, Full e promoções pelos líderes [cases Q1, Q2].
5. Aba "Oportunidades" e requisito de acesso ao detalhe do painel de mercado (R$300 × R$1.500 a R$2.000) [mix §9].
6. Tendências, mais vendidos e visitas: a API exige token e a permissão "Métricas do negócio" [mix A10; rank A34].
7. Tarifa da seção Supermercado e percentual-base de Cápsulas: o simulador e o `listing_prices` exigem login ou token [cases A29; R2-PR-2].
8. Valor do TH do custo fixo (faturas por faixa) e frete grátis fora da loja Full Super, R$19 × R$79 (simulador) [mix A37; R2-BA-29].
9. Separação de subsídio do ML e desconto do vendedor por item (`meli_percentage` e `seller_percentage` com token) [pre Q6]. O efeito da promoção também exige medição própria.
10. Lista de produtos de Supermercado restritos a autorizados (fluxo de envio ao Full) [alim A3].
11. Benefício de Reputação × Reputação Protegida (`/reputacao/beneficio_reputacao`) [rep A23].
12. Quem opera cada conta de grupo multimarca e se o ML vende essas marcas em 1P ("Vendido por" bloqueado) [alim Q9].
13. Calendário promocional de 2026 com prazos de adesão (Central de Promoções), que não tem página pública [pre Q8].
14. Datas sem fonte: ano de 10/09 e data de 20/05 dos extragrandes (Novidades da Central) [rep A2; log A9].

**Só se resolve com medição própria ao longo do tempo**
1. Incrementalidade de Ads, inclusive em termos da própria marca, e efeito de Ads sobre o orgânico (holdout ou pausa por SKU pareado) [ads Q5, Q6; rank A42].
2. Efeito do Full na exposição e na conversão (antes e depois com SKUs pareados) [log Q3, A17].
3. Tempo para recuperar a posição depois de uma ruptura (série de posição) [log Q7].
4. Tempo para um anúncio novo ganhar posição orgânica [rank Q8].
5. Efeito de editar título ou fotos de um anúncio que vende ("lido como novo") [rank A20].
6. Magnitude do efeito do clipe na conversão [rank A25, A26].
7. Se a descrição indexa na busca (busca por termo presente só na descrição) [soc S20–S21].
8. Efeito da medalha MercadoLíder na exposição (impressões antes e depois da troca) [rep A38].
9. Concentração por categoria (CR3, CR5, HHI) e ranking de vendedores com mudança em 12 meses (observação com protocolo, em série) [mix Q3; cases Q1].
10. Índice de preço par a par e % de buy box de portfólio [pre Q4].
11. Share contra a categoria [cases Q7].
12. Canibalização entre kit e avulso [mix §9].
13. Teste de formato: multipack × unitário [alim Q8].
14. Observação de busca com segundo horário, sessão deslogada e CEP explícito [R2-OBS].

### 1.0 Camadas por frente

A coluna "Rodada 2" resume o que mudou em 15/10, segundo a §12 de cada nota.

| Frente | Oficial | Dados | Obs. | Social | Rodada 2 (15/10) |
|---|---|---|---|---|---|
| ads | OK (developers; 8 de 12 conf.) | ausente (ACOS 5–25% sem método) | fraca (sem "Patrocinado") | OK | Oficial reforçada: 21 das 42 afirmações confirmadas, 8 delas só em fala de webinar reassistido com minuto; N2 (cartas e 10-Q) relido. Obs.: o patrocinado foi medido com rótulo e slots fixos (R2-OBS-1 a 3). Dados segue ausente |
| preco-promocao | fraca na verificação (403; 1 de 12 conf.), mas páginas lidas por outras frentes; N2 OK | ausente | parcial (preço em camadas, só café) | OK | Oficial passa a OK: tarifa do café, 51251, 40538, gerenciar-ofertas, price matching e automação lidos. Regulatório do "de/por" lido na fonte. Dados segue ausente |
| logistica-estoque | parcial (Ajuda por JS; 5 de 12 conf.) | ausente | parcial (FULL só nos cards) | OK | Oficial passa a OK: 24253, 16645, 15373, 44922, 42158 e 42159 lidas. Dados: só Lett, sem recorte de marketplace (N4 C). Obs.: Full Super no topo de café |
| ranqueamento-anuncio | OK (9 de 12 conf.) | ausente | parcial | OK | Oficial reforçada (clips, experiência de compra, API). Obs.: busca com protocolo em 6 termos. Dados segue ausente |
| produto-mix | OK (10 de 12 conf.) | fraca (Nubimetrics sem método nem data) | parcial | OK | Oficial OK. Dados ficou mais fraca: a API pública de busca, tendências e mais vendidos fechou (token) |
| reputacao-atendimento | OK (10 de 12 conf.) | ausente | parcial (só a medalha dos líderes) | parcial | Oficial completa: tabela por cor em 60 e 365 dias, corte de 101 vendas, Decola e Protegida. Dados: só Reclame Aqui (N8, amostra pequena) |
| alimentos-marca-propria | OK (11 de 12 conf.); N2 Anvisa só via imprensa | ausente | OK em café | parcial | N2 lido na fonte: Anvisa, IN 281, RDC 843, Portaria 570, INPI. Dados: NIQ e Worldpanel (N4 B) |
| cases-grandes | fraca (403; só o 8-K relido) | fraca (XP, Santander e Avenue via imprensa) | parcial | OK | N2 relido: 4 cartas, 4 calls e o 10-Q 2T26. Busca dirigida não achou case de vendedor com medição de terceiro |

### 1.1 ads
**Perguntas do protocolo**
- **PARCIAL.** Q1 **P**: os requisitos de Display self-service e do canal Top Brands não são públicos [ads §9]. → Os formatos e a cobrança por formato estão documentados (10-Q 2T26), e há teste grátis de 10 dias [ads §12.4 Q1]. Os requisitos de Display e Top Brands seguem não públicos (sem fonte pública), e o desempate dos requisitos do Product Ads exige login (ver abaixo).
- **PARCIAL.** Q2 **P**: Ad Rank = Ad Score × CPC está escrito só para Brand Ads. Para Product Ads, a fórmula, o "segundo preço" e o CPC derivado do ROAS vêm só do webinar JzejZyVeauE, não reassistido [ads A4, rank A30]. → O webinar foi reassistido com minuto (JzejZyVeauE 30:46–31:54, 57:16, 58:53), e a fala de 30/09/2026 descreve três variáveis (LOZL-QmsGL4 16:28). Em texto, o Product Ads segue só com "ROAS objetivo + relevância", e o "segundo preço" tem uma única fonte oral [ads A4, R2-WEB-1 a 4]. Resíduo: página escrita.
- **ABERTO.** Q5 **S**: não há incrementalidade. O Product Ads não expõe termo de busca, então a fatia do gasto em termos da própria marca não é mensurável [ads §9]. → Motivo: precisa de medição própria (holdout ou pausa por SKU pareado). O ML não publicou experimento (R2-EVC-16). A literatura externa indica que a atribuição superestima (R2-EVC-1 a 3), e a duplicação pago + orgânico (R2-OBS-4) é só indício.
- **ABERTO.** Q6 **S** em fonte oficial: só praticantes e um suposto "score de TACOS" [ads A33]. → Motivo: sem fonte oficial e precisa de medição própria. A fala do ML ("+21% de cliques e +39% de vendas") é atribuição, sem holdout [rank A42]. O "score de TACOS" segue sem fonte.
- **ABERTO.** Q7 **S** para o BR: só ACOS de 5% a 25% sem método [ads A37] e Amazon EUA [ads A38]. → Motivo: exige login (portal do Mercado Ads com 403; Ads Center logado) e não há estudo de agência BR com amostra. A rodada 2 achou só heurística de blog (R2-DAD-28).
- **PARCIAL.** Q9 **S**: não há integração confirmada de Pacvue, Flywheel, Perpetua ou Skai com o Mercado Ads. A participação de Ads por concorrente no painel Concorrência não foi verificada. → O painel Concorrência mostra o % de vendas com publicidade por concorrente (nota oficial, [ads §12.2]). Há método público de medição do patrocinado: rótulo, slots 1–4 e 13–16, 33% do top 24 (R2-OBS-1 a 3). Resíduo: integração das ferramentas citadas (sem fonte pública) e série temporal.

**Sem fonte oficial ou contestado**
- **FECHADO.** Faixa de ROAS objetivo de 1x a 35x [ads A2]: o consolidado a usa como benchmark [OFICIAL], mas não foi reconferida. → developers `product-ads-para-catalogo-e-user-products-leitura` (06/07/2026), trecho literal na seção 11 [ads A2]. Ressalva: o desempate por WebFetch deu 403.
- **PARCIAL.** Orçamento compartilhado e cobrança pós-paga [ads A15]. → O orçamento compartilhado está confirmado em texto (nota de redistribuição automática; exclui campanhas com menos de 7 dias) [ads A15]. A cobrança só por clique, na fatura do Mercado Pago, está em fala oficial e no 10-Q 2T26 [ads A17]. Resíduo: o texto N1 do "pós-pago" não foi lido.
- **PARCIAL.** Janela de atribuição: 14 dias na API contra 15 no webinar [ads A10]. → O texto técnico de 06/07/2026 (14 dias) pesa mais que a fala de maio (15 dias); nenhum webinar de setembro cita prazo. Motivo do resíduo: o desempate final exige o painel, com login.
- **PARCIAL.** Requisitos do Product Ads: a nota oficial contesta o webinar (15 dias de conta, fatura vencida) [rep A16, CONTESTADA]. → As frentes uniformizaram o estado: o texto da Central fica CONFIRMADO como leitura, e a divergência com três falas de 2026 fica aberta [ads A6, §12.2-2; rep A16 PARCIAL]. Motivo do resíduo: nenhuma fonte tem data que desempate. Exige teste numa conta nova (login).
- **FECHADO.** Ads/GMV do MELI em cerca de 2,6%: só fonte secundária. → Resposta negativa documentada: o MELI não divulga Ads/GMV, e a call do 4T25 diz só "still small compared to its potential" (R2-BA-15) [ads §12.1]. Os 2,6% não devem ser usados.
- **PARCIAL.** Fase de aprendizado oficial: não documentada. → Não há página que defina a fase. Os 7 dias sem mexer são "regra de ouro" em duas falas de set/2026 (5UhmqSFuX7U; LOZL-QmsGL4), coerentes com a exclusão de campanhas com menos de 7 dias da redistribuição [ads §9 → §12.1].
- **PARCIAL.** Quem recebe a venda quando o clique pago cai num catálogo ganho por outro vendedor: não documentado. → Fala de nov/2025: Product Ads de catálogo só imprime para quem vence o catálogo (b-ZNQktRHjc 41:54) [ads §12.1; R2-WEB-18]. Resíduo: falta texto escrito, reconfirmação em 2026 e regra para venda indireta.

### 1.2 preco-promocao
**Perguntas**
- **PARCIAL.** Q1 **P**: a tarifa percentual exata por categoria (Alimentos, café) não foi lida. A tabela de tarifa competitiva (ajuda/51251: −3 a −5 p.p. entre R$150 e R$700) e o reajuste de envio de +1,6% em 24/08/2026 não foram reconferidos [pre A7, A8]. → Fechados: tarifa do café (Clássico 14%, Premium 19%; landing custos-de-venda, R2-PR-1) [pre A1]; a 51251, ampliada a Cápsulas, Solúvel, Infusões e Cremes [pre A8; R2-BA-4]; a data de 24 de agosto (ajuda/48578) [pre A7]. Resíduos: o "+1,6%" segue sem fonte oficial. A tarifa da seção Supermercado e o valor do TH exigem login.
- **PARCIAL.** Q2 **P**: não há regra oficial de paridade. A punição por preço externo desde out/2025 vem só de imprensa [cases A3]. O índice de competitividade citado na carta 2T26 não tem fórmula. → A comparação com preço externo é oficial: developers `referencias-de-precos` (17/12/2025) e automação INT_EXT, que inclui o Google (01/10/2026) [pre A23, A24; cases A3]. Resíduo: aviso, prazo de 3 dias e perda de visibilidade seguem só na imprensa (R2-SIN-18). A fórmula do índice não é publicada (sem fonte pública).
- **ABERTO.** Q4 **S**: não há índice par a par ou ponderado, % de buy box de portfólio nem preço contra a mediana da 1ª página praticados no BR. → Motivo: sem prática documentada e precisa de medição própria em série. O painel Concorrência mostra o uso de alavancas, não preço relativo [pre §12.4 Q4].
- **FECHADO.** Q5 **P**: os 12 tipos de promoção, as cofinanciadas e quem paga cada parte vêm de developers não reconferido [pre A14–A16, R10–R12]. → developers `gerenciar-ofertas` (09/06/2026): 12 tipos; com bonificação MARKETPLACE_CAMPAIGN, VOLUME, PRE_NEGOTIATED, SMART, PRICE_MATCHING e UNHEALTHY_STOCK; aporte separado por `meli_percentage` e `seller_percentage` [pre A14, A15; R2-PR-15, 16]. Resíduo menor: VOLUME tem contradição interna entre a tabela de 2026 e a doc de 2025 [pre A18].
- **ABERTO.** Q6 **S**: nada separa o subsídio do ML do desconto do vendedor. → Motivo: exige login e medição própria. A API separa os aportes por item (R2-PR-16), mas só com token do vendedor, e não há estudo nem holdout público de efeito [pre §12.4 Q6].
- **PARCIAL.** Q8 **P**: não há calendário oficial de 2026 com prazos de adesão. A data da Black Friday é cálculo [pre §9.6]. → Acréscimos: moldura legal do "de/por" (R2-REG-25 a 29) e peso de Alimentos e Bebidas na Black Friday de 2024 (R2-DAD-04). Resíduo: calendário e prazos de adesão sem página pública (provável só na Central logada).

**Sem fonte oficial ou contestado**
- **FECHADO.** Desconto de frete por reputação: 50% (página atual) contra 70% (vídeo de maio) [pre A5; rep A15]. → Verde até 50%, já embutido; amarela até 40%; laranja e vermelha 0%. Fonte: ajudas 40538, 40545 e 40547. Os 70% estão superados [pre A5; rep A15; R2-SIN-9, 10].
- **FECHADO.** Custo fixo abaixo de R$79: a página atual mostra só degraus de envio; blogs e um vídeo de maio falam em corte de R$12,50 [mix R12, SEM FONTE]. → developers "Custos por vender" (03/09/2026): desde 02/03/2026, abaixo do TH, só Flex, ME1 e envio personalizado cobram custo fixo; Full, Coleta, Places, Drop off e Turbo não cobram. Os R$12,50 são a regra anterior [mix A37; R2-BA-5]. Ressalvas: leitor único (WebFetch de desempate com 403) e valor do TH não publicado.
- **FECHADO.** Automação de preços (INT/INT_EXT, piso, 60 dias) [pre A23]: não reconferida. → developers `automatizacoes-de-precos` (01/10/2026). Acréscimos: pausa quando o item entra em promoção; no catálogo, reputação amarela ou melhor [pre A23; R2-PR-18].
- **PARCIAL.** Duração e desconto mínimo de relâmpago e oferta do dia: só praticantes. → Oficial: a LIGHTNING exige estoque, não tem bonificação padrão, e o vendedor define o preço entre um mínimo e um máximo (gerenciar-ofertas) [pre A16]. Resíduo: a duração (cerca de 12 h) segue só em praticante [pre N15], e o mínimo numérico não está em página lida.
- **FECHADO.** Legalidade de "de/por" e a suposta regra de 60 dias antes da Black Friday (CDC, Senacon): não verificadas. → Lidos na fonte: CDC, arts. 37 e 38; Decreto 5.903/2006. Os "60 dias" são recomendação do Procon-SP (desconto sobre o menor preço de 60 dias), não lei. O PL 5925/2025 não é lei [R2-REG-25 a 29; pre §12.1].

### 1.3 logistica-estoque
**Perguntas**
- **PARCIAL.** Q2 **P**: custos oficiais de retirada e descarte por m³ (ajuda/16645), coleta ao Full e armazenagem diária (ajuda/24253, que redirecionou) não foram lidos. → Lidas: ajuda/16645 (retirada a partir de R$98; descarte de R$1 a R$18 por m³) [log A26] e ajuda/24253 (armazenagem geral e do Supermercado) [log A1]. Resíduo: a coleta ao Full (por m³ e distância) segue sem tabela pública. A 16645 tem duas incoerências internas e leitor único.
- **ABERTO.** Q3 **S** quantitativo: o efeito do Full ou do frete na exposição tem só "2x", "+150%" e "5x", sem método [log A17]. → Motivo: precisa de medição própria (antes e depois com SKUs pareados). O ML não publica experimento sobre o Full (R2-EVC-16). Há só a ordem de grandeza externa de cerca de +1,45% por dia útil a menos de prazo (R2-EVC-10) e a observação do Full Super no topo de café (R2-OBS-5).
- **ABERTO.** Q7 **P**: o anúncio pausa sem estoque (conf.), mas o tempo para recuperar a posição não foi medido. → Motivo: precisa de série temporal própria. O único número (37,9% voltam no 1º dia, 59% no 2º) é da Lett, sem nome de marketplace nem amostra (R2-DAD-17). A queda da recomendação de reposição está só em vídeo oficial [log A13].
- **PARCIAL.** Q8 **P**: procedimento de validade dentro do Full (alerta, descarte, FEFO) não documentado; páginas do Inmetro e do MAPA por categoria não lidas. → Confirmados em N1: validade acima de 90 dias (15737), validade legível e não manuscrita, recusa de validade próxima (5200), código universal em kits de supermercado. A inspeção da Anvisa no CD do Full é N2 (R2-REG-1). Resíduo: alerta de vencimento, descarte por validade e FEFO seguem sem página (sem fonte pública). As páginas do Inmetro e do MAPA por categoria não foram lidas, e as operações do MAPA exigem login.

**Sem fonte oficial ou contestado**
- **PARCIAL.** Restrição de extragrandes de 20/05/2026 (20 kg, 80 cm, 125 L, preço mínimo) [log R6]: a página oficial ainda fala em mais de 18 kg e até 25 kg. → O conflito está resolvido: 25 kg é o limite de entrada (15573), 18 kg é o tamanho XG de armazenagem (24253) e 20 kg / 80 cm / 125 L é a lista de extragrandes (44922). Nenhuma subcategoria de alimentos está na lista [log A9, §12.2]. Resíduo: a data de 20/05 segue sem fonte oficial, e o metadado "a partir de 15 de outubro" da 44922 não foi confirmado.
- **FECHADO.** Estoque compartilhado: reputação verde, experiência 75, exclusão de alimentos e de itens com validade [log R9; ajuda 42158/42159 não carregaram]. → ajudas 42158 e 42159 lidas na rodada 2 [log A22; alim A32; R2-FS-15, 16].
- **FECHADO.** Lado de até 120 cm, soma de até 260 cm e proibição de itens com controle de temperatura [log R5]. A frente de alimentos confirmou a proibição na ajuda/5200 [alim A2]: ver reconciliação. → ajuda/15573 (menos de 25 kg, um lado até 120 cm, soma até 260 cm) e ajuda/5200 (proibição de itens com controle de temperatura ou umidade) [log A7, A8].
- **FECHADO.** Penetração do Full só no Brasil: o 8-K dá 55% regional. → Resposta negativa documentada: o número do Brasil não é divulgado. O regional é de 55% (1T26) e "mais da metade" no 10-Q 2T26 [log A18; R2-BA-17].

### 1.4 ranqueamento-anuncio
**Perguntas**
- **FECHADO.** Q1 **P**: não há fórmula nem pesos. → Resposta verificada por ausência: o ML não publica fórmula nem pesos. As declarações oficiais de ordenação foram lidas em texto: nota de posicionamento, experiência de compra, qualidade, ajuda/864 ("mais visibilidade" para MercadoLíder) e ajuda/16449 ("destaque nas buscas" para Full Super) [rank §12.4 Q1].
- **PARCIAL.** Q7 **P**: não há página oficial sobre incentivo a avaliações (cartão na embalagem, brinde) [rank §9]. → Em N1, perguntas, respostas e opiniões entram na experiência de compra. Em fala, a avaliação entra no Ad Score e na qualidade do Ad Rank [rank §12.4 Q7]. Resíduo: a página sobre incentivo a avaliações não foi encontrada (sem fonte pública), e o efeito da avaliação no orgânico não tem peso nem teste.
- **ABERTO.** Q8 **S**: o próprio ML "não informa prazo" para um anúncio ganhar posição. → Motivo: precisa de série temporal própria. As referências que existem são de campanhas de Ads: 7 dias sem mexer (R2-WEB-10) e 20 a 30 dias para produto novo (R2-WEB-11) [rank §12.4 Q8].

**Sem fonte oficial ou contestado**
- **PARCIAL.** "Trocar título ou fotos faz o anúncio ser lido como novo" [rank A20]: só webinar MFYKfOYs0iE. O consolidado trata como prática dos melhores. → Confirmado literalmente como fala oficial (MFYKfOYs0iE 60:26–62:03). Conflito: a developers diz que, pela API, o título não é editável com vendas, e a fala diz que é possível (65:18) [rank A20]. Resíduo: não há página nem dado; precisa de medição própria (série de posição antes e depois de uma edição controlada).
- **FECHADO.** Especificações de Clips (duração, moderação em 48 h, logo) [rank A23]: sem página escrita. → Texto da Central: 9:16, de 10 s a 1 min. Vídeo oficial: aprovação em até 48 h, até 280 MB, logo abaixo de 10% e lista de proibidos (tJLgMpKRe8s; QuOP9KeKnk8) [rank A23, A27, A29]. Ressalva: logo "e" × "ou" entre falas; na dúvida, cumprir as duas condições.
- **PARCIAL.** Teste de +10% a 15% de conversão com clipe na 1ª posição: único número com desenho experimental declarado, mas só falado em webinar, sem amostra nem período. → A fala foi reconferida com minuto (QuOP9KeKnk8 35:03–35:37). Continuam sem amostra, período, categoria e controle [rank A26]. A magnitude só se resolve com medição própria.
- **FECHADO.** Janela da experiência de compra: 60/365 dias contra 180 dias, divergência oficial interna [rank A9]. → 60 dias com 100 vendas, senão o último ano. Os 180 dias são a janela de exibição das vendas com problema. Fontes: nota "como proporcionar a melhor experiência de compra" e developers `experiencia-de-compra` (03/02/2026) [rank A9; rep A18]. Ressalva: a função dos 180 dias vem de leitura cruzada, sem frase oficial explícita.
- **FECHADO.** Frase "catálogo sempre primeiro" contra `visit_share` mínimo para quem perde a buy box [rank A2]. → Conciliada: a frase é dica sem critério técnico. Outra nota oficial diz "sempre nos primeiros resultados", e o vencedor depende de localização e parâmetros. Só o vencedor tem `visit_share` maximum (developers `concorrencia-em-catalogo`, 21/07/2026) [rank A2, A4, A5]. Não é regra mecânica.
- **ABERTO.** Lista de categorias que exigem fundo branco: não publicada. → Motivo: sem fonte pública. A developers `diagnostico-de-imagens` (14/07/2025) não publica a lista [rank A17].
- **ABERTO.** A descrição indexa na busca? [soc S20–S21]: sem fonte. → Motivo: sem fonte oficial; resolve-se com teste próprio (buscar um termo presente só na descrição) [CONSOLIDADO §4.1 #21].

### 1.5 produto-mix
**Perguntas**
- **ABERTO.** Q3 **P**: não há CR3, CR5 nem HHI para nenhuma categoria do ML-BR. → Motivo: sem fonte pública e precisa de medição própria em série. A API pública de busca e de mais vendidos fechou (token), e a Nubimetrics só dá a faixa de cerca de 63–74% de Platinum, sem método [mix A24; §12.4 Q3]. Só observação com protocolo daria uma estimativa.
- **ABERTO.** Q4 **P**: não há dado de sortimento ML × Shopee dos mesmos vendedores. → Motivo: sem fonte pública. A rodada 2 só acrescentou o lado do ML: anúncio separado por envio e várias lojas oficiais por conta (R2-MIX-9, 10) [mix §12.4 Q4].
- **ABERTO.** Q6 **S**: não há equivalente público a Market Basket ou Traffic Graph. → Motivo: sem fonte pública. Há só proxies agregados de recompra no N2 (itens por comprador +19%; +10 p.p. de usuários em 3 ou mais categorias), sem taxa por categoria [mix A17; §12.4 Q6].
- **ABERTO.** Q7 **P**: share of search no Google sem evidência. → Motivo: sem fonte lida; precisa de medição própria. A API de tendências do ML agora exige token e permissão [mix A10; R2-MIX-1].

**Sem fonte oficial ou contestado**
- **FECHADO.** "Sem entrega diferente por variante" no modelo User Products [mix R3, CONTESTADA em parte]. → CONTESTADA → corrigida: o UP permite preço e condições por variação (até 30). A limitação de entrega é do modelo antigo, e a alternativa escrita é o anúncio separado por forma de envio (developers `preco-variacao`, 17/09/2026; `user-products`, 17/06/2026; ajuda/2517) [mix A5, A3].
- **ABERTO.** Conteúdo atual da aba "Oportunidades" (medalhas, sazonalidade, top 100): precisa de checagem logada, que fica fora do escopo sem login. → Motivo: exige login de vendedor [mix §9].
- **ABERTO.** Requisito de acesso ao detalhe do painel: R$300 contra R$1.500 a R$2.000 em 60 dias (estado-da-arte §2.1, pode estar superada). → Motivo: exige login; não foi relido na rodada 2 [mix §12].
- **ABERTO.** Canibalização entre kit e avulso: nenhuma medição. → Motivo: precisa de medição própria. R2-OBS-4 mostra pago e orgânico do mesmo produto lado a lado, o que é indício e não medida [mix §12.4 Q5].

### 1.6 reputacao-atendimento
**Perguntas**
- **ABERTO.** Q2 **P**: o efeito da medalha na exposição tem a afirmação oficial contra um praticante que não viu efeito [rep D2]. → Motivo: precisa de medição própria (impressões antes e depois da troca de medalha) [rep A38]. As outras consequências de cada cor ficaram oficiais: frete 50/40/0%, Ads a partir de amarela, catálogo sem vitória para laranja e vermelha, cupons, Full Super e estoque compartilhado só no verde [rep §12.4 Q2].
- **ABERTO.** Q3 **P**: o número de recursos na contestação vem de N7. → Motivo: sem fonte pública. Não há página oficial com o fluxo nem o número de recursos, e a rodada 2 não trouxe fonte nova [rep §12.4 Q3]. As exclusões estão em N1.
- **ABERTO.** Q8 **P**: há divergências internas da Ajuda sobre o Full (retirada de não aptos em 20 ou 30 dias; contestação em 60 dias corridos ou úteis). → Motivo: as páginas não foram relidas na rodada 2, e não há dado que compare reclamações entre Full e envio próprio. Novo em N1: o vendedor não responde por produto de outro no estoque compartilhado (ajuda/42158) [rep §12.4 Q8].

**Sem fonte oficial ou contestado**
- **FECHADO.** Faixas de 365 dias para amarelo, laranja e vermelho: só via Terazi. → Nota oficial "vamos mudar a forma como calculamos sua reputação". Canceladas: verde até 2,5%, amarelo até 5,5%, laranja até 6,5%. Envios incorretos: 13 / 23,5 / 28,5%. Reclamações: iguais às de 60 dias [rep §12.1 "§4 Faixas de 365 dias"; R2-PR-7].
- **PARCIAL.** Benefício de Reputação (R$75 a R$250 mil, 120 dias): só terceiros. Não se sabe se coexiste com a Reputação Protegida. → Os valores de R$75 a R$250 mil e os 120 dias não estão em página oficial: não usar [rep A23]. No Brasil, os termos do Benefício (`RECOVERY_GRNTEE`) apontam para a ajuda/29528, "Reputação Protegida", o que é indício forte de que são o mesmo programa (R2-PR-11). Motivo do resíduo: a página `/reputacao/beneficio_reputacao` exige login.
- **FECHADO.** Corte da janela de reputação: 101 (oficial, sem data) contra 68 (vídeo, "desde 10/09/2026") contra 60 (developers 2025) [rep A2; cases A26]. → Desde 10 de setembro, 101 vendas em 60 dias; o corte anterior era 60, e o "68" é erro do vídeo. Fontes: nota "vamos mudar…" e ajuda/866 [rep A2; cases A26]. Ressalva: o ano de 2026 vem de tela de vídeo (6QFwvsIPSkQ).
- **ABERTO.** Benchmark de reclamação, devolução e tempo de resposta por categoria: ausente. → Motivo: sem fonte pública; o ML não publica. Há só o Reclame Aqui (N8, amostra pequena e sem taxa por pedido) [rep A37; R2-SIN-19 a 23].

### 1.7 alimentos-marca-propria
**Perguntas**
- **FECHADO.** Q2 **P**: o comunicado oficial gov.br da inspeção da Anvisa em Cajamar (18/03/2026) não foi lido; o dado vem de imprensa. Não se procuraram inspeções do MAPA em CDs. → Nota da Anvisa lida (gov.br/anvisa, 18/03/2026). O 0,34% é declaração do ML à imprensa e não está na nota [alim A13; R2-REG-1 a 4]. Busca do MAPA: nenhuma inspeção em CD de marketplace encontrada; 1 lote de café em alerta em 2026, sem marketplace [alim §12.4 Q2]. Resíduo menor: as REs não foram lidas no DOU.
- **PARCIAL.** Q3 **S**: o case 3 Corações/Lett (2025) que o protocolo cita não foi encontrado nem buscado. Não há share of search, content score ou ruptura com case brasileiro. → O case 3 Corações/Lett foi achado, mas não é do ML nem auditável. Há o case Ypê/Lett no ML (1 SKU, sem controle, R2-DAD-20) e dado de ruptura da Lett (R2-DAD-17) [alim §12.4 Q3]. Resíduo: share of search e content score de alimentos no ML (sem fonte pública).
- **ABERTO.** Q4 **P**: não há assinatura no ML (confirmado por ausência). Não há dado público do botão de recompra. → Motivo: sem fonte pública. A ausência de assinatura se mantém, e o MELI+ exclui Supermercado (ajuda/30487) [cases A31]. Não há taxa de recompra por categoria nem dado de uso do botão [alim §12.4 Q4].
- **ABERTO.** Q8 **P**: não há teste de formato (multipack contra unitário). → Motivo: precisa de teste próprio. A regra está confirmada (kit e pack no Full com código universal; sem economia por kit no Supermercado), mas nenhuma fonte tem número por formato [alim §12.4 Q8].
- **PARCIAL.** Q9 **S**: a organização 1P/3P de Nestlé, Ambev, Unilever e 3 Corações em 2026 tem só o caso Nestlé/Brasil CT, de 2019. → Estrutura observada: uma conta por grupo com várias lojas oficiais (R2-EVC-23 a 25); 1P abaixo de 10% do GMV (10-Q 2T26) [alim §12.4 Q9]. Motivo do resíduo: quem opera cada conta e o "Vendido por" exigem login.

**Sem fonte oficial ou contestado**
- **FECHADO.** Convivência da ajuda/23329 (Full fechado a novos autorizados de Supermercado) com a nota que coloca automaticamente em Supermercado quem tem estoque no Full [alim §2.4]. O consolidado a chama de ponto mais crítico; não há leitura que concilie. → Conciliada no texto: a 23329 restringe "alguns produtos", não a categoria. A 5200 põe esses produtos entre os proibidos no Full para quem não é autorizado, e os demais entram automaticamente (inferência média) [alim A3; log §12.2; R2-FS-1 a 4]. Resíduo: a lista de produtos restritos não é pública e só se vê no fluxo de envio, com login.
- **PARCIAL.** Lista e critério dos "produtos selecionados" do Full Super (envio de R$1,60 contra R$2,40) e a data de 24/08/2026: não lidos. → Valores confirmados na ajuda/49972; a diferença existe só até 8 kg; vale automaticamente para anúncio de catálogo [alim A7; log A25]. Resíduos: a lista é um PDF no CDN do ML, não aberto; o critério não é publicado; a data de 24/08 só está confirmada para a tabela geral (ajuda/48578); o rótulo de peso diverge entre notas ("até 1 kg" × "até 0,3 kg").
- **FECHADO.** Classe do INPI exigida para loja oficial (35 ou classe do produto): sem regra. → O ML não exige classe (Lojas Oficiais e BPP não citam). Pela NCL 13-2026, o café é classe 30, e na classe 35 a venda de produtos não é serviço [alim A27; R2-REG-33, 34]. Resíduo menor: o que o painel "Minhas Marcas" aceita na prática exige login.
- **FECHADO.** Enquadramento do café na IN 281/2024: não confirmado no DOU. → Anexo III, item 5, da IN 281/2024 (Anvisa Legis): comunicação de início de fabricação ou importação, não registro nem notificação. O prazo de 01/09/2026 não é do café [alim A15, A16; R2-REG-11, 12, 14].
- **FECHADO.** Norma de exibição do rótulo no anúncio online: não encontrada. → Resposta negativa documentada: não há norma sanitária específica para o anúncio online (RDC 727/2022 define rotulagem como a embalagem). O dever vem do CDC, art. 31; do Decreto 7.962/2013, art. 2º; da Lei 10.962/2004, art. 2º, III; e do Decreto-Lei 986/1969, art. 23 [R2-REG-19 a 24; CONSOLIDADO §6.2].

### 1.8 cases-grandes
**Perguntas**
- **ABERTO.** Q1 **S**: não há ranking público. O painel Concorrência exige login, e as ferramentas N5 não tiveram relatório de 2026 encontrado. → Motivo: exige login e série temporal própria. A API pública fechou busca, mais vendidos e tendências (R2-BA-26) e mostra o estoque em faixas (R2-BA-24) [cases §12.4 Q1].
- **PARCIAL.** Q2 **P**: o painel Concorrência aplicado a café (share por vendedor, % de Ads) não foi visto. → Observação com protocolo em 6 termos: Ads em 33% do topo, Brand Ads em toda busca e Full Super dominante em café (R2-OBS-2 a 6) [cases §12.4 Q2]. Motivo do resíduo: o painel aplicado a café exige login. Faltam ainda um segundo horário, uma sessão deslogada e o CEP exibido.
- **ABERTO.** Q5 **P**: Shopee e Amazon só aparecem pelos cases. → Motivo: sem fonte pública além de praticantes. O lado oficial do ML se limita à comparação com preço externo [cases A3, §12.4 Q5]. Shopee e Amazon ficam com as frentes próprias.
- **ABERTO.** Q7 **S**: nenhum case mede share contra a categoria. → Motivo: sem fonte pública e precisa de medição própria. Os dados de tendência exigem login ou token (R2-BA-20) [cases §12.4 Q7].

**Sem fonte oficial ou contestado**
- **PARCIAL.** Pacote de preço competitivo de abril de 2026 no nível de detalhe (−1 p.p., armazenagem grátis no Full, campanhas bancadas pelo ML) [cases A2]: só InfoMoney. → N2 confirma a parte geral: desconto no Pix, desconto de take rate por categoria e faixa de preço e corte da tarifa de envio no fim do 1T26 (carta 2T26; call 1T26) [cases A1, A2; R2-BA-12 a 14]. Resíduo: nenhum N2 cita "−1 p.p.", armazenagem grátis no Full nem campanhas bancadas.
- **FECHADO.** MELI+ com frete rápido abaixo de R$79 a R$9,90 [cases A31]: o 8-K 2T26 não cita; os 8-K de 1T26 e 4T25 não foram relidos. → Carta 3T25 (entrega rápida a partir de R$19 desde out/2025); carta 4T25 e página de planos (Essencial a R$9,90). Os termos (ajuda/30487) excluem Supermercado e limitam o subsídio a R$20 [cases A31; R2-BA-8 a 10].
- **PARCIAL.** Critérios de Polos, Meli Pro, gerente de conta e contêiner direto no Full: só relatos. → A existência do Meli Pro está em fala oficial: teste grátis de Product Ads de 20 dias no Meli Pro, contra 10 para os demais (5UhmqSFuX7U 26:26) [cases A20]. Resíduo: critérios de acesso, Polos e contêiner direto da China sem fonte oficial [cases A21].
- **FECHADO.** Restrição da API para ferramentas externas: só relato de usuário. → developers `permissoes-funcionais` (21/11/2025), `bloqueio-de-aplicacoes` (15/04/2026) e `itens-e-buscas` (31/08/2026), mais teste curl de 15/10/2026: busca, tendências, mais vendidos, visitas e `listing_prices` exigem token e permissão; um app só de leitura pode ser bloqueado [rank A34; mix A18; R2-BA-20 a 26].

### 1.9 Reconciliações internas pendentes (sem coleta nova)

Todas foram aplicadas nas §12.2 das notas em 15/10. A coluna "Estado" registra o resultado.

| Afirmação dada como "não reconf." | Onde já está confirmada | Ação | Estado (15/10) |
|---|---|---|---|
| Tabela de envio, R$6,95 e desconto de até 50% [pre R1–R4] | [alim A8] leu a ajuda/40538 | Atualizar [pre] e o consolidado §1 | **FECHADO**: aplicada e superada por leitura direta (ajudas 40538, 40545, 40547) [pre A2–A5, §12.2] |
| Tarifa Clássico e Premium [pre R1; cases A29] | [mix R2] leu a ajuda/870 | Atualizar | **FECHADO**: ajuda/870 relida; café 14% e 19% [pre A1; cases A29] |
| MercadoLíder e reputação [cases A25–A26] | [rep A2–A6] leu as ajudas 864 e 866 | Atualizar | **FECHADO**: corte de 101 vendas; "68" contestado [cases A25, A26; rep §12.2] |
| Estoque antigo de Supermercado e valores [log R2] | [alim A4] leu a ajuda/15373 | Atualizar a tabela de [log] | **FECHADO**: 2 meses no Supermercado, 4 nos demais; 15373 e 15731 com a mesma tabela [log A2, A3] |
| Full Super: R$8, sem armazenagem P/M, R$199 [log R8] | [alim A5–A7] leu as ajudas 16449 e 49972 | Atualizar | **FECHADO**: aplicada [log A21, A25]. Divergência nova registrada: "R$79 fora da loja" (16449) × R$19 (40538) |
| Proibição de refrigerados no Full [log R5] | [alim A2] leu a ajuda/5200 | Atualizar | **FECHADO** [log A8] |
| Isenção de 180 dias para SKUs Estrela [log R11] | [mix R9] confirmou por vídeo oficial | Uniformizar o veredito: é vídeo oficial, sem página escrita | **FECHADO** (uniformizada): fala oficial tGWTaeqbsmU, sem página escrita; a afirmação segue PARCIAL [log A5; mix A12] |
| Painel Concorrência [cases A8] | [mix R6] leu a nota oficial | Atualizar | **FECHADO**: nota "análise de concorrência" [cases A8; ads §12.2] |

---

## 2. Shopee

### 2.0 Camadas por frente

O retrato geral: a camada Oficial em texto ficou quase vazia. Nas 8 frentes houve 10 confirmações e 1 contestação parcial. O conteúdo "oficial" vem de vídeos do canal Shopee Brasil, não reassistidos na verificação, e de telas mostradas por praticantes [OFICIAL via terceiro].

| Frente | Oficial (conf./total) | Dados | Obs. | Social |
|---|---|---|---|---|
| ads | fraca (3/12; portal sem data) | ausente (blogs de ERP) | ausente (sem patrocinados observados) | OK |
| preco-promocao | fraca (1 parcial de 12) | ausente | fraca (1 página) | OK |
| logistica-estoque | fraca (2/12; um termo de 2023) | ausente | ausente | OK |
| ranqueamento-anuncio | fraca (2/12; 1 contestada) | ausente | fraca | OK |
| produto-mix | ausente (0/12) | ausente (extensões sem fórmula) | fraca | OK |
| reputacao-atendimento | ausente (0/12) | ausente | ausente | OK |
| alimentos-marca-propria | fraca (1/12, blog); N2 Anvisa OK | ausente | fraca | parcial |
| cases-grandes | ausente (0/12); N2 Sea global | ausente | fraca | OK |

### 2.1 ads
**Perguntas**
- Q1 **P**: GMV Max, afiliados do vendedor (comissão, atribuição, tributação) e "Restrições do Shopee Ads" sem N1. A exclusividade do Display para Lojas Oficiais não reapareceu na releitura [ads A3].
- Q2 **S** em N1: há conflito sobre cobrança por clique (portal /ad-types/419) ou por impressão desde 2026-05-07 (dois praticantes) [D1]. Continua aberto se ainda existe lance por palavra-chave [D4].
- Q5, Q6, Q7, Q9 **S**.
- Afirmação solta de que mídia atribuída aumenta a comissão (hEkVpRw_vNg): sem regra localizada.

**Sem fonte oficial**
- Orçamento mínimo de R$10/dia [A7].
- Pré-pago e recarga mínima de R$50 [A8].
- Atribuição de 7 dias por clique e 1 por visualização [A11].
- Definição de ROAS e ACOS "diretos" [A12].
- Teto de ROAS 30 [A13].
- Posições dos anúncios na busca [A22]: só blog Magis5.

### 2.2 preco-promocao
**Perguntas**
- Q1 **P**: tabela de 2026-10-01 só via terceiro (4 canais concordam, confiança B). Continuam abertos:
  - regra de itens abaixo de R$8;
  - taxa de CPF;
  - subsídio Pix de "até 8%" acima de R$500;
  - data do frete grátis obrigatório (março ou maio);
  - coparticipação de frete por modalidade (um único exemplo de 25%).
- Q4 **S**.
- Q6 **S**.
- Q7 **P**: não se achou reprecificador com piso na Shopee.
- Q8 **P**: calendário só com o post do 10.10; faltam prazos de inscrição e nomeação.

**Sem fonte oficial**
- Taxa de campanha oficial de 2% a 3% sobre todas as vendas da loja, com renovação automática [PRE R8]: fonte única. Muda a conta de toda data dupla.
- Repasse do subsídio Pix ao vendedor [R6]: o lado do comprador está confirmado na help 197770, sem percentuais.
- Comissão sem exceção por categoria: afirmação negativa, não verificada.

### 2.3 logistica-estoque
**Perguntas**
- Q1 **P**: requisitos do Full (nota acima de 4,5, 5 pedidos por dia) só em vídeo oficial não reassistido. Faixas P/M/G/XG sem números.
- Q2 **S**: não se sabe se existe armazenagem ou cobrança por idade de estoque em out/2026 [D11]. A multa por medida errada no recebimento é desconhecida até para o praticante.
- Q3 **S**.
- Q5 **P**: não há índice tipo IPI.
- Q6 **P**: não há cotas de recebimento em pico.
- Q7 **S**.
- Q8 **S** para alimentos no Full.

**Sem fonte oficial ou contestado**
- Taxa de envio ao CD para item abaixo de R$20 (R$1 a R$12,50 por unidade desde 2026-07-01) [A5]: fonte única.
- Full+ (−0,5 a −2 p.p.) [A9]: só vídeo.
- Rede de CDs: uma tela com um único CD contra o blog oficial que cita 5 CDs [D12].
- Termos do Programa de Frete Grátis Extra (help 137281) e do Uber Direct (help 196450): links existem, mas o conteúdo não abriu.
- Tetos de subsídio de frete de R$20/30/40 (lado vendedor) contra o cupom de R$20 do comprador (help 76220) [D9].

### 2.4 ranqueamento-anuncio
**Perguntas**
- Q1 **P**: só as quatro ordenações e o filtro de Indicados.
- Q2 **P**: a classificação "a melhorar / qualificado / excelente" não tem critérios, nem se sabe se afeta a busca.
- Q5: não se aplica, mas falta confirmar se o EAN agrupa anúncios em "encontrar similares".
- Q6 **P**: não há relatório de share por etapa do funil.
- Q8 **S**.

**Sem fonte oficial ou contestado**
- Trilha oficial de anúncio em vídeo, não reassistida [A6, A9, A11, A12, A14]:
  - 36 primeiros caracteres do título;
  - produto em 70% da capa e imagem de pelo menos 1.000 px;
  - vídeo de 10 a 60 s e até 30 MB;
  - remoção permanente por EAN inventado;
  - spam de preço acima de 4x entre variações.
- Limites de caracteres do título e da descrição e número máximo de fotos: sem N1.
- Reenvio de anúncio excluído gerar pontos extras [A4, CONTESTADA em parte pela help 76225].
- Atributo Anvisa obrigatório em 169 categorias [A30]: só via integrador.

### 2.5 produto-mix
**Perguntas**
- Q1 **S**: a Shopee não mostra vendas brutas da categoria. As extensões (Avantpro, RadarSeller, SellerBP) não têm fórmula.
- Q3 **S**.
- Q4 **P**.
- Q6 **S**.
- Canibalização: **S**.

**Sem fonte oficial**
- Kit pagar uma única taxa fixa [D18]: central para a tese de que o kit dilui a taxa por item, que aparece em §2.2 e §6.2 do consolidado.
- Assistente de vendas: só praticante.
- Limite de variações em 2 níveis e GTIN [A6].
- Número institucional de 3 milhões de vendedores e 95% das vendas [A17]: vídeo de marketing.
- GMV da Shopee no Brasil em 2024: R$30 bi contra R$60 bi [D20].

### 2.6 reputacao-atendimento
**Perguntas**
- Q1 **P**: fórmula da nota da loja (média simples? janela?) desconhecida.
- Q2 **P**: tudo via terceiro.
- Q3 **S**: não há documento sobre o que sai do cálculo (arrependimento, atraso da transportadora ou do Full, caso fortuito).
- Q5 **P**: não se sabe qual régua usar internamente, a do Indicado ou a de pontos.
- Q8 **S**.

**Sem fonte oficial ou contestado**
- Tabela de pontos: trimestre, faixas e multas de R$250/500 contra R$300/600 [D6].
- Gatilho de atraso de 5% contra 8% [D7].
- TNC do Indicado: abaixo de 2–3% contra abaixo de 8% [D8].
- Isenção abaixo de R$2.500 de GMV, 14 dias para contestar e 7 de reenvio [A15–A16]: só blog UpSeller. É a prioridade máxima segundo a própria nota.
- Taxa de R$0,49 do Devolução Fácil [A26].
- Critérios do Indicado (card de 2026-03, pode estar superado).

### 2.7 alimentos-marca-propria
**Perguntas**
- Q1 **S** em N1:
  - a política de proibidos e restritos não foi lida;
  - a planilha das 169 categorias com atributo Anvisa não foi lida (não se sabe se inclui café, chá, cápsula e suplemento);
  - não se sabe que número aceitar para café dispensado de registro.
- Q2 **P**: as retiradas da Anvisa (N2) estão documentadas, mas a ação contra a Shopee que gerou a RE revogada não foi achada.
- Q3 **S**.
- Q5 **P**: a Loja Oficial não tem página de critérios. A existência de Brand Ads ou de algo equivalente ao Brand Registry na Shopee (help 182821) não foi verificada.
- Q9 **S**.

**Sem fonte oficial**
- Validade mínima no recebimento do Full, FEFO e categorias aceitas: os CDs se declaram "moda, beleza, tecnologia".
- Mercado Shopee "foco em não perecíveis": só metade confirmada.

### 2.8 cases-grandes
**Perguntas**
- Q1 **S**.
- Q4 **P**: rotina semanal e mensal e comparação entre agência e time interno não descritas.
- Q7 **S**.
- Q8 **P**: os 6-K da Sea não abrem números do Brasil.

**Sem fonte oficial**
- Preço do ShopeeVIP e efeito no vendedor.
- Título "R$50 milhões/mês" da MadeiraMadeira (QwL3e7QUnx4): não confirmado no vídeo.
- Critérios do gerente de contas.

### 2.9 Pontos da Shopee que dependem de um único leitor com JavaScript
Quase todas as pendências acima apontam para as mesmas URLs:
- `seller.shopee.com.br/edu/article/18483` e `/18439` (comissão e taxa fixa) e FAQ 7749;
- `seller.shopee.com.br/edu/article/23724` (DTS);
- `seller.shopee.com.br/edu/article/full` (requisitos, taxas ao CD, multas);
- `help.shopee.com.br/portal/4/article/76428` (normas de desempenho e pontos);
- `ads.shopee.com.br/learn/faq` (artigos de GMV Max, cobrança, recarga, atribuição, restrições; /learn/faq/115/438 deu erro 500);
- `help.shopee.com.br/portal/4/article/137281`, `/196450` e `/182821`;
- tema "atributo Anvisa" no Centro de Educação.

Ler essas páginas fecha cerca de 40 afirmações.

---

## 3. Amazon

### 3.0 Camadas por frente

| Frente | Oficial | Dados | Obs. | Social |
|---|---|---|---|---|
| ads | parcial (páginas públicas; 5 conf., 1 contestada; muito webinar) | parcial (Jungle Scout/PODEAN com BR; Skai EUA) | fraca (8 de 30 patrocinados, sem CEP e sem hora) | OK |
| preco-promocao | parcial (2 conf., 3 contestadas, 7 sem fonte) | ausente (Jungle Scout e Numerator atrás de formulário) | fraca | OK |
| logistica-estoque | parcial (6 conf., 2 contestadas) | fraca (IPI EUA de 2023) | ausente | OK |
| ranqueamento-anuncio | fraca no BR (3 conf.; base em sell.amazon.com EUA) | parcial (Marketplace Pulse EUA) | fraca | OK |
| produto-mix | parcial (SP-API confirma Brand Analytics no BR) | fraca (SmartScout s/d) | fraca | OK |
| reputacao-atendimento | parcial (ajudas de comprador com 503) | fraca (EUA, 2020–2024) | ausente | parcial |
| alimentos-marca-propria | fraca (regra de alimentos no FBA só em webinar) | ausente | fraca (só café) | ausente (quase nada sobre alimentos) |
| cases-grandes | parcial (venda.amazon.com.br; release N2 global) | fraca (Marketplace Pulse EUA) | fraca | parcial (cases dos EUA) |

### 3.1 ads
**Perguntas**
- Q1 **P**: disponibilidade no BR de DSP, Prime Video ads, Sponsored TV e share of voice reservado de SB não verificada. Requisito do Sponsored Display sem fonte [ads R4].
- Q2 **P**: o "segundo preço + R$0,01" só aparece em webinar [R5]. Não se sabe se a métrica-alvo no BR é ACOS ou ROAS [ads §9.3; R9].
- Q5 **P**: só a defesa de marca global de 96% (sem recorte do BR); não há incrementalidade.
- Q6 **S** oficial.
- Q7 **S** para o BR.
- Q9 **S**.

**Sem fonte oficial ou contestado**
- Lance dinâmico (+100% ou +50%) e teto de 900% por posicionamento [R6].
- Janelas de aprendizado de 7, 14 e 30 dias [R8]: o consolidado as trata como "certas pelos praticantes".
- Orçamento mensal = diário × 30 [R7, CONTESTADA: a página diz diário × dias do mês].
- Base do 3,5% do Experimente FBA: receita elegível [ads R1] contra receita total [log A5], leitura divergente da mesma página de termos.
- Limiar numérico de quando não anunciar: inexistente.

### 3.2 preco-promocao
**Perguntas**
- Q1 **P**: tarifa FBA abaixo de R$79 [D1, CONTESTADA]. Comissão mínima de R$1 ou R$2 (divergência interna da /precos). R$2 por item no plano Profissional ambíguo. Tarifa administrativa de reembolso só em tela de praticante.
- Q2 **P**: não há N1 sobre preço justo, paridade ou alerta de preço competitivo.
- Q4 **S**.
- Q6 **S**.
- Q8 **P**: data e resultados do Prime Day 2026 no BR não divulgados.

**Sem fonte oficial ou contestado**
- **Amazon Mais Vantagens** [A6–A7]: Pix de 5% pago pela Amazon, taxa de 1,5% passando a 2,5% em 31/10/2026, itens de R$40 a R$10 mil e Buy Box calculada com o preço Pix. Só webinar de 14/10/2026. É regra recente com efeito direto na Buy Box e não tem texto.
- Preço riscado: mediana de 90 dias contra média de 6 meses [A8].
- Regras de promoção: webinar de 2026 contra página sem data. Relâmpago de 4 a 12 h ou cerca de 24 h; cupom de 5% a 80% por 90 dias ou 5% a 50% por 30 dias [A11, A12, CONTESTADAS].
- Cofinanciamento com comissão reduzida de 12% para 10% [A13].
- "Ads não fazem ganhar a Buy Box" e anúncio congelado [A15]: só webinar.
- Desconto mínimo de 5% ou R$50 a R$100 [A10].

### 3.3 logistica-estoque
**Perguntas**
- Q2 **P**: multa por divergência no recebimento não encontrada. IDI de "700 ou mais" só em webinar, e a escala do BR é desconhecida.
- Q3 **S** causal: "4x" (página) e "20% a 25%" (webinar), sem método.
- Q6 **P**: não há fórmula pública de ponto de pedido.
- Q7 **S**.
- Q8 **S** no BR: validade mínima no recebimento, retirada antes do vencimento, formato da data, calor, Anvisa e Inmetro.

**Sem fonte oficial ou contestado**
- Anexo 2 dos termos do Experimente FBA veio incompleto. R$5,65/5,85/6,05 aparecem só na linha de 1 a 1,5 kg; o R$6,50 não aparece [A6].
- Frete grátis ao não Prime: R$19–79 com 3 dias ou mais (/termos/frete19) contra R$129 (/cresca/fba) contra R$149 (/cresca/fba-onsite) [A12, CONTESTADA].
- Caixa master de 22 kg contra 30 kg [A9, CONTESTADA]. Contradição interna: lado de 100 cm contra pacote de 105×105×105 [mix R6].
- Cobertura de 5 semanas e limiares de 60/90 dias [A7]: só webinar.
- Cancelamento antes do envio abaixo de 2,5% [A11]: só webinar.

### 3.4 ranqueamento-anuncio
**Perguntas**
- Q1 **P**: a única página é do blog de SEO dos EUA (2025-09-03).
- Q2 **S** no BR: painel de qualidade e supressão não lido.
- Q5 **P**: os fatores da Buy Box só aparecem em webinar [R4]; a página dos EUA deu 404.
- Q8 **S**: só um relato de lucro no 3º ou 4º mês.
- Q9 **P**: regra brasileira sobre palavra-chave de marca alheia (Ads e backend) não encontrada.

**Sem fonte oficial ou contestado**
- Título de 75 caracteres no BR desde 27/07/2026 [R1]: só o vídeo cNn3iConWSw, de praticante.
- Limite de 250 bytes do campo de backend.
- Janela do botão "Solicitar avaliação": 4 ou 5 a 30 dias.
- Precedência do conteúdo (dono da marca, depois sistema, depois maioria) [R5].
- Fundo branco e selo promocional que suprime o item [R9]: só webinar; a página dos EUA só recomenda fundo simples.
- Gerenciar experimentos no BR [R12]: a página não lista marketplaces, e "4 semanas" foi contestado.
- Fatia de vendas pela Buy Box acima de 80%: blog sem fonte.
- "+270% de conversão com 5 avaliações": não usar (texto feito com IA, sem fonte).

### 3.5 produto-mix
**Perguntas**
- Q3 **P**: não há cálculo de concentração no BR. O recorte possível (click share e conversion share dos 3 primeiros ASINs no Search Terms) não foi demonstrado.
- Q5 **P**: não há caso brasileiro de CM2 negativa ou canibalização.
- Q6 **P**: Market Basket e Repeat Purchase existem no BR (SP-API), mas ninguém os mostrou em uso.
- Q7 **S** para share of search no Google. A defasagem EUA → BR é hipótese.

**Sem fonte oficial ou contestado**
- Regras de kit físico, kit virtual e isenção de GTIN [R10] e de variações (pai sem estoque, tarifa por variação de quantidade) [R11]: só webinar; o Listing Hub deu 404.
- "17 meses de histórico" do Brand Analytics [R8, CONTESTADA: é o máximo por requisição].
- Portaria INPI 66/2026 (exame prioritário para marketplace): vista só via advogada com oferta comercial.

### 3.6 reputacao-atendimento
**Perguntas**
- Q1 **P**: escala da AHR no BR e se o programa está ativo, desconhecidos. O ODR abaixo de 1% vem só da SellerApp. `targetValue` vem vazio na SP-API.
- Q3 **P**: SAFE-T só para DBA e FBA Onsite; reembolso de estoque perdido no FBA clássico não coberto.
- Q5 **S**.
- Q8 **P**.

**Sem fonte oficial (ajudas com 503)**
- Garantia de A a Z: 90 dias e gatilho de 48 h [A10].
- Devolução: 30, 7 (comestíveis) e 90 dias [A14].
- SLA de 2 dias úteis [A13].
- Prazos do SAFE-T: 45, 52 e 7 dias [A19].
- Tarifa de reembolso de 20%, com teto de R$10 [A18].
- Customer Reviews, resposta pública a avaliações e CSBA no BR: sem evidência.
- Conflito de prática: excluir quem deu feedback negativo da solicitação de avaliação contra a proibição de pedir seletivamente (SP-API). Está registrado; vale a fonte oficial.

### 3.7 alimentos-marca-propria
**Perguntas**
- Q1 **S** em texto: não se sabe se "Comidas e bebidas" exige aprovação no 3P, nem a vida útil mínima no FBA. "Etiqueta não cobre a validade" e "vencido sem reembolso" estão só em webinar [R4–R5].
- Q2 **S**: não há fiscalização sanitária registrada em CD da Amazon.
- Q3 **S**.
- Q4 **P**: a mecânica do Programe e Poupe no BR (níveis, quem banca, elegibilidade) é desconhecida; só há os EUA, de 2025.
- Q9 **S**: termos do 1P (Vendor) para a indústria no BR desconhecidos, embora o 1P domine o topo de café.

**Sem fonte oficial ou contestado**
- "Protocolo basta" para o Brand Registry e "não denuncia com protocolo" [R6, CONTESTADA: a página aceita pedido pendente "em alguns casos"].
- Isenção de GTIN para kits em cerca de 10 dias úteis e prazo da autorização de marca [R12].
- Frete de mercearia no mesmo dia (R$79 contra R$19; R$8,90 e R$10,90): nenhuma página.
- Regras sanitárias externas (RDC 843/2024, IN 281/2024, Portaria SDA 570/2022): vieram da nota do ML e não foram relidas na fonte.

### 3.8 cases-grandes
**Perguntas**
- Q1 **S**: só a foto de 2026-10-14, sem série.
- Q3 **R** por negativa: nenhum case brasileiro tem número; as 21 histórias oficiais não têm métricas.
- Q4 **P**: só cases dos EUA.
- Q5 **P**: multicanal da Amazon só anunciado nos EUA.
- Q7 **S**.

**Sem fonte oficial**
- Regra de transição do 3,5% [cases R2]: está nos termos lidos por [log A5] e [ads R2]; ver reconciliação.
- Mais Vantagens [cases R9].
- Faturamento da Amazon Brasil e share por categoria: o balanço não separa o BR.

### 3.9 Reconciliações internas pendentes
| Divergência entre notas | Ação |
|---|---|
| [cases R2] "sem fonte" para a transição do 3,5%, contra [log A5] e [ads R2] confirmados em `/termos/experimente-fba` | Uniformizar. A frente cases leu só /cresca/fba |
| Base do 3,5%: "receita elegível" [ads R1; mix R3] contra "receita total dos 30 dias" [log A5] | Reler a seção 3.1 dos termos e registrar o trecho literal (até 15 palavras) |
| [cases R1] "página não informa início nem fim" contra [log A4] (01/07/2026 a 31/01/2027 nos termos) | Citar os termos como fonte da vigência |
| Vine e Brand Analytics "não confirmados no BR" em [rank §9] e [alim §9], contra a confirmação em [rep A29] e [mix R8] | Corrigir as notas [rank] e [alim]. O consolidado já resolveu |

---

## 4. Lista priorizada da próxima rodada

Restrições que valem em todos os itens: sem login, sem aceitar termos ou cookies não essenciais, sem preencher formulário com dado pessoal sem autorização do usuário, e sem contornar bloqueio de tráfego. Quando uma página exigir login, registrar "exige login" e seguir para a alternativa. Toda leitura nova entra na ficha com URL, data da fonte, data de acesso e tipo.

### P0: regras que mudam a conta unitária e estão sem N1 ou contestadas

| # | O que buscar | Onde | Fecha |
|---|---|---|---|
| 1 | Tabela de comissão e taxa fixa de 2026-10-01: R$4,50; faixas de R$80 a R$200 ou mais; regra abaixo de R$8; taxa de CPF; se o kit conta como 1 item | `seller.shopee.com.br/edu/article/18483` e `/18439`, FAQ 7749, com leitor que renderize JS (agente de navegador, sem login) | Shopee PRE R1–R5; MIX A8–A10, A30, D18; CAS A5, A5b, A31 |
| 2 | Política de pontos de penalidade: trimestre, faixas, multas (R$250/500 ou R$300/600), gatilhos de 5% ou 8%, isenção abaixo de R$2.500; e critérios atuais do Vendedor Indicado | `help.shopee.com.br/portal/4/article/76428`; `seller.shopee.com.br/edu/article/23724`; tema "pontos de penalidade" no Centro de Educação | Shopee REP A3–A17, A15–A16, D6–D8; RAN A21, A26 |
| 3 | Shopee Ads: cobrança (CPC ou CPM), existência de lance por palavra-chave, GMV Max, orçamento e recarga mínimos, atribuição, teto de ROAS, elegibilidade do Display | artigos de `ads.shopee.com.br/learn/faq` e `/news`, renderizados; notícia "Atualizamos as métricas ROI e CIR" | Shopee ADS A3, A6–A8, A11–A13; D1, D4 |
| 4 | Full Shopee: requisitos, faixas P/M/G/XG, taxa ao CD abaixo de R$20, armazenagem ou estoque antigo, multa por medida, CDs disponíveis, regras de alimento; Full+ | `seller.shopee.com.br/edu/article/full`; reassistir os vídeos oficiais TUs6QYGqGrw e 0oRYednAlHY com transcrição salva | Shopee LOG A2, A5, A7, A9; D11, D12 |
| 5 | Taxa de campanha de 2% a 3% e renovação automática; regras do 11.11 e do 12.12 de 2026 | Central de Marketing > Campanhas (páginas públicas do Centro de Educação); blog oficial shopee.com.br/blog | Shopee PRE R8–R9 |
| 6 | Amazon Mais Vantagens: Pix de 5%, taxa de 1,5% para 2,5% em 31/10/2026, Buy Box com preço Pix | comunicado escrito em venda.amazon.com.br (as URLs /cresca/amazon-mais-vantagens deram 404: procurar pelo menu), aboutamazon.com.br, páginas públicas de Seller News; reler H0ab_x1YIBY com transcrição | Amazon PRECO A6–A7; RANK R3; CASES R9 |
| 7 | Tarifa FBA abaixo de R$79: tabela por peso contra fixa; Anexo 2 completo dos termos | leitura visual (print) de `venda.amazon.com.br/termos/experimente-fba` e `/precos`; arquivo de tarifas DBA acima de R$79 (download só com autorização, informando nome, origem e tamanho) | Amazon PRECO A2; LOG A6; D1 |
| 8 | Frete grátis ao não Prime (R$19, R$79, R$129 ou R$149) | `/termos/frete19`, `/cresca/fba`, `/cresca/fba-onsite`, mais observação deslogada em página de produto com 2 CEPs | Amazon LOG A12; ALIM R10 |
| 9 | Ajuda do Seller Central BR em formato externo (validade no FBA, aprovação de categoria de alimentos, Buy Box, preço de referência, título, variações e kits) | tentar `sellercentral.amazon.com.br/help/hub/reference/external/<código>` (G201030350, G201003420 e os demais citados). Se pedir login, parar e registrar | Amazon ALIM R4–R5; LOG §9.1; RANK R1, R4–R8; MIX R10–R11 |
| 10 | Ajudas de comprador da Amazon que deram 503 (A a Z, devolução de 7 dias para comestíveis, SLA) | `amazon.com.br/gp/help/customer/display.html?nodeId=GQ37ZCNECJKTFYQV`, `GKM69DUUYKQWKWX7`, `GFLBEJCLHMVFEPA8`, `GLC8ZMBWMBTR6QZZ`, em outro dia e horário | Amazon REP A10, A13, A14 |
| 11 | Tarifa percentual por categoria no ML (Alimentos e Bebidas, café) e tabela 51251 | API pública `api.mercadolibre.com/sites/MLB/listing_prices?price=<p>&category_id=<id>` (testar se segue pública, como `/categories` seguiu em [rank A14]); `mercadolivre.com.br/ajuda/51251` pelo navegador integrado | ML PRE §9.1, A8; consolidado §7 item 2 |
| 12 | Habilitação de Supermercado no Full: ajuda/23329 contra a entrada automática; lista e critério dos "produtos selecionados" do Full Super; data de 24/08/2026 | ajudas 23329, 16449, 49972 e a nota de Supermercado, pelo navegador integrado; página da lista de selecionados a partir da 49972 | ML ALIM A3, A7; consolidado §7 itens 1 e 3 |

### P1: reverificação no ML e reconciliação (baixo custo)

| # | O que fazer | Onde | Fecha |
|---|---|---|---|
| 13 | Aplicar as reconciliações de §1.9 e §3.9 nas notas e nos consolidados | notas já existentes | cerca de 15 afirmações "não reconf." |
| 14 | Promoções, *price matching*, cupons e automação de preços | `developers.mercadolivre.com.br/pt_br/gerenciar-ofertas`, `/campanhas-smart-price-matching`, `/cupons-do-vendedor`, página de automação de preços (01/10/2026), pelo navegador integrado | ML PRE A14–A16, A23, R10–R12 |
| 15 | Custos do Full não lidos: armazenagem diária (24253), retirada e descarte (16645), estoque compartilhado (42158, 42159), anúncio a mais por mudança de envio (2518), restrição de extragrandes | `mercadolivre.com.br/ajuda/<id>`, pelo navegador integrado | ML LOG R5, R6, R9; RANK A21 |
| 16 | Janela da experiência de compra (60/365 ou 180 dias) e corte de reputação (101, 68 ou 60) | nota "como-proporcionar-a-melhor-experiencia-de-compra"; developers `experiencia-de-compra` e `reputacao-de-vendedores`; ajuda/866; buscar comunicado de 10/09/2026 | ML RANK A9; REP A2, A4; divergências 7 e 8 |
| 17 | Webinars oficiais não reassistidos (Ad Rank do Product Ads, 15 a 30 produtos por campanha, clips, "não mexer no anúncio vencedor", orçamento pós-pago) | YouTube JzejZyVeauE, QuOP9KeKnk8, MFYKfOYs0iE: baixar legenda com `ferramentas/baixar_legendas.py` e citar o minuto | ML ADS A4, A15; RANK A20, A23, A30 |
| 18 | Benefício de Reputação contra Reputação Protegida; faixas de 365 dias | página pública da Central sobre o Benefício (a de `/reputacao/beneficio_reputacao` exige login); busca de comunicado | ML REP §9.2–9.3 |

### P1: documentos regulatórios e balanços (N2)

| # | O que buscar | Onde | Fecha |
|---|---|---|---|
| 19 | MELI+ e frete abaixo de R$79; pacote de preço competitivo; restrições de API | 8-K Ex-99.1 de 1T26 (07/05/2026) e 4T25 (24/02/2026) na SEC, além dos *earnings calls* | ML CASES A2, A31 |
| 20 | Comissão "híbrida" de março de 2026, que o protocolo cita como fonte-alvo e nenhuma nota leu; Brasil na Sea | 6-K e *earnings call* da Sea do 1T26 e 2T26 (sea.com/investor) | Shopee PRE §2.1 (faixas desde 2026-03-01); CAS §9.10 |
| 21 | Inspeção da Anvisa em Cajamar e retiradas por alegação em marketplace | gov.br/anvisa (notícias de 18/03/2026); DOU (resoluções RE de 2026); revisão das normas de propaganda de alimentos | ML ALIM §9; Shopee ALI §9.11 |
| 22 | Café na IN 281/2024 e RDC 843/2024 (transição até 01/09/2026); Portaria SDA/MAPA 570/2022 lida na fonte, não via ABIC | DOU e in.gov.br; gov.br/agricultura | as três notas de alimentos |
| 23 | Portaria INPI 66/2026 e classe NCL de café para loja oficial e Brand Registry | gov.br/inpi | ML ALIM §3.2; Amazon MIX §9.11 |
| 24 | Legalidade de "de/por", referência de preço e Black Friday | Senacon, Procon-SP, CDC art. 37 e decretos de oferta | ML PRE §9.7 |

### P1: camada de dados (N4/N5)

| # | O que buscar | Onde | Fecha |
|---|---|---|---|
| 25 | Estudo com amostra declarada sobre marketplace no BR (GMV por plataforma, conversão, categorias) | NIQ Ebit Webshoppers 2026 (resumo público); Neotrust/Confi; Conversion; ABComm | GMV Shopee BR [D20]; peso das plataformas |
| 26 | Benchmarks de Ads com amostra (CPC, CTR, CVR, ACOS por categoria), com recorte BR se houver | partes públicas de Pacvue, Skai, Perpetua e Jungle Scout Benchmark (formulário só com autorização); Mercado Ads Insights; relatórios de agências BR | ADS Q7 nas três plataformas |
| 27 | Prateleira digital de alimentos com case: o case 3 Corações/Lett (2025) do protocolo; share of search, ruptura, content score | blog e cases da Lett (Neogrid), Profitero, Nielsen; imprensa de trade (Mercado & Consumo, SuperHiper) | ALIM Q3 nas três plataformas |
| 28 | Estimativas N5 de concentração e liderança por categoria, sempre como faixa | academia.nubimetrics.com, blog da Real Trends, blog da Avantpro (posts de 2026 por categoria); SmartScout e Jungle Scout para o BR | MIX Q1 e Q3; CASES Q1 e Q7 |
| 29 | Recompra de consumíveis no BR | ABIC (pesquisa de consumo), Kantar Worldpanel, relatórios de clubes de assinatura | ALIM Q4 |

### P1: observação direta com protocolo completo

| # | O que observar | Como | Fecha |
|---|---|---|---|
| 30 | ML: separar orgânico e patrocinado | 3 termos de café e 3 de outras categorias; capturar o rótulo "Patrocinado" pelo DOM (atributo ou texto do card); 2 horários; CEP registrado; print salvo; sessão de comprador sem novo login | ADS Q9; divergência 13; consolidado §7 item 11 |
| 31 | Amazon: repetir `lideres.tsv` com protocolo | registrar hora, CEP exibido e print; posições patrocinadas (1–4, 21–24) em 2 horários e 2 dias; número de ofertas por ASIN e quem tem a Buy Box | ADS A20; CASES Q1 |
| 32 | Shopee: ampliar a amostra sem login | testar outros pontos de entrada públicos (página da categoria, vitrine de Lojas Oficiais, mall) em outro dia. Se a verificação de tráfego voltar, parar e registrar; não contornar | MIX Q1/Q3; REP; PRE Q4 |
| 33 | Série temporal mínima | repetir as observações 30 a 32 uma vez por semana durante 4 semanas | CASES Q1 ("mudança de liderança") |

### P2: causalidade, cases e camada social

| # | O que buscar | Onde | Fecha |
|---|---|---|---|
| 34 | Experimentos publicados sobre ranqueamento, Ads × orgânico e efeito de fulfillment | Amazon Science, Google Scholar ("sponsored products incrementality", "marketplace search ranking fulfillment"), MELI Tech Blog (Medium) | Q5/Q6 de ads; Q3 de logística; Q8 de ranqueamento |
| 35 | Cases com período e base | entrevistas de executivos (E-commerce Brasil, Valor, Exame, Mercado & Consumo); releases com auditoria; prêmios com métrica (Effie) | CASES Q3 nas três plataformas |
| 36 | Organização 1P/3P e agências *full commerce* das indústrias de alimentos | releases e LinkedIn de Nestlé, 3 Corações, Melitta, Orfeu e Italle; termos públicos do Amazon Vendor no BR | ALIM Q9; Amazon §7 item 4 |
| 37 | Mudanças recentes de regra (N8, só para levantar pergunta): cobrança CPM na Shopee, título de 75 caracteres na Amazon, punição por preço externo no ML, janela de 68 vendas | YouTube e TikTok dos últimos 30 dias com tela de comunicado; fóruns públicos de vendedores; depois confirmar em N1 | D1 Shopee; RANK R1 Amazon; ML CASES A3 e REP A2 |
| 38 | Padrão de reclamação de alimentos por plataforma (validade curta, avaria) | Reclame Aqui, páginas públicas de ML, Shopee e Amazon, filtrando por alimentos (N8) | REP Q6 e ALIM Q2 |
| 39 | Afiliados e vídeo (Shopee Video e Live, afiliados do vendedor, clips do ML) com regras e comissão | help e Centro de Educação da Shopee; developers do ML; vídeos oficiais | Shopee ADS §9.8; ML ADS Q1 |

### Critério de pronto da próxima rodada
- Shopee com pelo menos 30 afirmações de regra confirmadas em texto N1, contra 10 hoje.
- Amazon com Mais Vantagens, FBA abaixo de R$79, frete ao não Prime e validade no FBA resolvidos, ou marcados "exige login" com a alternativa tentada.
- ML com as reconciliações aplicadas e a tarifa por categoria lida.
- Ao menos um estudo N4 com amostra declarada por plataforma.
- Observação refeita com CEP, hora e print, e com orgânico separado do patrocinado.
- Todas as perguntas Q1 a Q9 de cada frente com R, P ou S explícito, com motivo, nas notas, como pede o checklist do protocolo (§8).
