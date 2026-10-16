# Ferramentas e método de análise no TikTok Shop: notas da frente (2026-10-15)

Frente: ferramentas-analise. Pesquisa neutra sobre como os melhores operadores usam ferramentas de terceiros (Kalodata, FastMoss, EchoTik, Shoplus, Tabcut, Cruva, Hubfluence e outras) e os dados de 1ª parte do Seller Center para escolher produto, criador, vídeo e LIVE.

Convenções:
- Tipos: [OFICIAL] regra, política ou definição publicada pelo TikTok · [PRÁTICA] tática de praticante · [CASE] números de uma operação · [DADO] ferramenta, estudo ou relatório · [OBS] observação ou cálculo desta frente.
- Marcas: [REVENDA] para afiliado, dropshipping ou importação; [MARCA] para indústria ou marca própria.
- País entre parênteses quando não é o Brasil. Regra anterior a 2026-04-15 leva **(pode estar superada)**.
- Ids de 11 caracteres são vídeos do YouTube (transcrições em `tiktokshop/transcricoes/<id>.txt`).
- Estimativa de ferramenta sempre com faixa, ferramenta, país e data. Ferramentas nunca são somadas entre si.

Fontes desta rodada: 13 transcrições indicadas e mais 14 da pasta com tema de ferramenta (27 lidas no total); 9 WebSearch; 27 WebFetch. Kalodata.com, G2 e o blog da AfterShip devolveram 403. O índice da Academy BR exige JavaScript, por isso só foram lidas páginas com `knowledge_id` conhecido.

---

## 1. Resumo executivo

1. **Nenhuma ferramenta de terceiros publica sua fórmula de estimativa.** Só a Cruva declara erro: cerca de ±30%, que varia com a estratégia de afiliados da marca. [DADO] cruva.com/help-center/social-intelligence/social-intelligence-data, s/d. A Kalodata diz coletar "canais públicos" e refinar com IA, e admite divergência em valor de transação e gasto em Ads (G2, via resumo de busca, s/d). A Tabcut alega espelhar "mais de 90%" dos dados, sem método. [DADO] tabcut.com, 2026-10-15.
2. **O método mais citado é a diferença diária de estoque ou de contador "vendidos" multiplicada pelo preço.** Quem descreve é um vendedor de API, e não há confirmação de que Kalodata ou FastMoss façam exatamente isso. [DADO] scrapecreators.com, 2025-08-06 (EUA, conflito de interesse). Consequência de método: reposição, devolução e mudança de preço distorcem a estimativa [OBS].
3. **A cobertura do Brasil existe, mas só aparece em tela e em guia de terceiro, não em página oficial das ferramentas.** FastMoss e Kalodata mostram o filtro "Brasil" em tutoriais de 2025-11 a 2026-02 (9vNHkmjzPZQ; YZ8FGCmIPTc; MFNkRTC-tzo). A Kalodata tem interface em pt-BR [DADO] viniensina.com.br, 2026-07-16. A Tabcut cobre o BR de forma indireta: o relatório da Momentum Works sobre o BR no 1º semestre de 2026 usa dados dela.
4. **O dado de mercado com método mais sólido para o BR é o relatório Momentum Works + Tabcut.** GMV de R$ 5,3 bilhões no 1º semestre de 2026, de R$ 5 milhões no mês de lançamento a R$ 1,58 bilhão em junho de 2026, 110,2 mil lojas e 2,3 milhões de influenciadores ativos. [DADO] momentum.asia, 2026-08 (relatório pago, US$ 52,95). É estimativa de ferramenta, não balanço.
5. **O dado nativo do Seller Center separa o que nenhuma ferramenta separa.** O relatório Visão geral do Data Compass divide a receita bruta em seis cortes: com Ads, sem Ads, Ads sem afiliado, Ads e afiliado ao mesmo tempo, afiliado sem Ads e nenhum dos dois. A atribuição padrão é de 7 dias após o clique ou 1 dia após a visualização. [OFICIAL] ads.tiktok.com/help/article/about-ads-metrics-in-seller-center, atualizado em 2025-02 **(pode estar superada; global, não específico do BR)**.
6. **A receita e o ROI do GMV Max incluem pedidos orgânicos.** Segundo o TikTok, a receita bruta soma pedidos pagos e orgânicos atribuídos à campanha, e o ROI e o custo por pedido também misturam os dois. [OFICIAL] ads.tiktok.com/help/article/how-to-see-reporting-for-your-product-gmv-max-campaign, 2026-06. O ROI "Pro", que desconta afiliado, cupom e tarifa, ainda está "em teste". [OFICIAL] blog pt-BR, 2026-05-13.
7. **O GMV muda de definição conforme a fonte.** Para o TikTok, "receita bruta" é o que o comprador paga, menos imposto, mais o desconto da plataforma (ads help, 2025-02). Para a EchoTik, GMV é "antes de devolução" (2026-04-28). Dois praticantes dos EUA dizem que o número de destaque do painel está a preço de tabela, inflado em relação ao GMV depois do desconto (ARKJE_iDEbI, 2026-07-25; 1ngx3DmdwlQ, 2026-02-20). Esse ponto não foi conferido em N1.
8. **GPM tem pelo menos três denominadores em circulação**: mil impressões (EchoTik, 2026-04-28), mil views de vídeo (praticante BR, 1GDosmkdolA) e mil espectadores de LIVE (metodo.md §4.1). A página oficial de métricas do Data Compass não define GPM.
9. **O fluxo das agências se repete**: produto → criadores que vendem o produto → vídeos (com selo de anúncio) → LIVE → loja concorrente → "análise de afiliados" da loja concorrente para convidar os mesmos criadores. [PRÁTICA] AD32WdQGXRY (EUA); pOAL8R1dWK0 (EUA); MFNkRTC-tzo; YZ8FGCmIPTc.
10. **Os cortes usados para achar produto "alcançável" são parecidos entre fontes.** Faturamento de 30 dias entre US$ 30 mil e 200 mil, crescimento de 20% a 100%, de 2 a 100 criadores e concentração nos três maiores criadores (rA2nsDx7-Jg, EUA). Outra versão: pelo menos US$ 10 mil em 7 dias, crescimento semanal de 15% ou mais, menos de 600 criadores e comissão de 10% ou mais (h7-OxsXH8AI, EUA). No BR, um instrutor pede pelo menos R$ 200 mil de GMV em 30 dias (metodo.md §3.2). [PRÁTICA]
11. **O limite de convites da plataforma vale para todo software de outreach.** O teto semanal de primeiro contato escala com o GMV de afiliados dos últimos 30 dias. Tabela de um fornecedor (EUA): pacote inicial de 1.000; zero com GMV zero; 2.000 por semana até US$ 2 mil; 7.000 de US$ 2 mil a 50 mil; ilimitado acima de US$ 50 mil; renova no domingo. [PRÁTICA/DADO] hubfluence.io, 2026-06-10 (EUA, conflito de interesse). A página BR lida só mostra 50 criadores e 100 produtos por convite e 1.000 colaborações em 24 h. [OFICIAL] Academy BR kid=6580476438529809, 2025-04-14 **(pode estar superada)**.
12. **Preço e histórico variam muito, e os números circulam com conflito de interesse.**
    - EchoTik: US$ 9,90, 19,10 e 29,10 por usuário/mês no plano anual, com 30 dias, 90 dias e histórico ilimitado [DADO] echotik.live/pricing, 2026-10-15.
    - Shoplus: US$ 39, 49 e 79 por mês [DADO] shoplus.net, 2026-10-15.
    - Kalodata: cerca de US$ 49,99 (90 dias) e 109,99 (180 dias) por mês; FastMoss: US$ 558, 854 e 1.084 por ano (90, 180 e 1.200 dias). Ambos segundo um concorrente [DADO] hubfluence.io, 2026-10-08.
13. **Os tutoriais em vídeo são quase todos comerciais.** Há link de afiliado da ferramenta: a FastMoss paga de 15% a 30% recorrentes a quem indica (UaZEv-sWUak). Há vídeos patrocinados (ShopShark, XiK_nMFz3Us) e vídeos do fundador da ferramenta (SmartScout, 5Bw9zTCbvHg; HiveHQ, 1ngx3DmdwlQ). No BR, um revendedor de "Kalodata ilimitado" dentro de um pacote de IA aparece em quatro vídeos do mesmo canal (Tockfy: 25vuaes4kjc, FsXd0__CbtM, 4LnQ0HB6A_Q, xvxpbLEcJhY).
14. **Ensinar a burlar o limite gratuito é sinal de fonte fraca.** Um tutorial BR ensina a recriar conta da Kalodata com e-mail temporário a cada 10 pesquisas (MFNkRTC-tzo, 2025-11-16). A afirmação "dados que nem o dono do TikTok tem" (9vNHkmjzPZQ) é falsa por construção, porque a ferramenta estima a partir de sinais públicos.

---

## 2. Como funciona (mecânica e regras oficiais)

### 2.1 Duas camadas de dado que não se misturam
| Camada | O que é | Quem vê | Confiabilidade |
|---|---|---|---|
| 1ª parte (Seller Center, Central de Afiliados, painel GMV Max, Ads Manager) | Pedidos, GMV, tráfego, atribuição por canal da **própria** loja | Só o dono da loja (e parceiros autorizados) | Alta para a própria conta; a atribuição se sobrepõe entre canais |
| 3ª parte (Kalodata, FastMoss etc.) | Estimativa a partir de sinais públicos (produto, vitrine, vídeo comprável, LIVE) | Qualquer assinante, sobre qualquer loja | Direcional; erro não publicado (exceto ±30% da Cruva) |

A EchoTik resume o limite da camada 3: a ferramenta "normalmente não vê" pedidos privados, reembolsos, tarifas e repasses do concorrente. [DADO] echotik.live/blog/how-accurate-is-tiktok-shop-data, 2026-08-07. O mesmo texto admite que algumas ferramentas misturam dado de conta conectada (confirmado) com estimativa de mercado, e recomenda conferir o carimbo de horário da coleta antes de comparar.

### 2.2 Data Compass: relatórios e definições oficiais
Segundo o TikTok, o Data Compass fica no menu superior do Seller Center. [OFICIAL] ads.tiktok.com/help/article/about-ads-metrics-in-seller-center, atualizado em 2025-02 **(pode estar superada; texto global, sem menção ao BR)**.

- **Janela de atribuição padrão:** 7 dias após o clique ou 1 dia após a visualização, salvo personalização. O Seller Center conta vendas do mesmo dia; o Ads Manager usa a janela de 7 dias. Por isso os dois painéis não batem por definição.
- **Receita bruta:** o que o comprador paga, menos impostos, mais os descontos de produto pagos pela plataforma. Pedido é contado por SKU, e uma compra pode gerar vários pedidos.
- **Relatório Vídeo** (Shop Ads com vídeos das contas oficial e de marketing):
  - views sem replays;
  - taxa de exibição do produto = visitas à página do produto ÷ views;
  - CTR = visitas à página do produto ÷ impressões de anúncio;
  - CTOR = pedidos ÷ visitas à página do produto.
- **Relatório LIVE:**
  - PV de LIVE = entradas na sala (quem só vê pelo feed não conta);
  - taxa de entrada = PV ÷ impressões;
  - taxa de exibição do produto = cliques em produto ÷ PV;
  - CTR = cliques ÷ impressões do cartão dentro da sala;
  - CTOR = pedidos ÷ cliques em anúncio de produto da LIVE.
- **Relatório Cartão de produto:** só Product Shopping Ads.
- **Relatório Visão geral:** receita bruta total da loja e mais seis cortes:
  - com Ads;
  - sem Ads;
  - Ads sem afiliado;
  - Ads e afiliado ao mesmo tempo (comprador interagiu com anúncio que usava vídeo de afiliado);
  - afiliado sem Ads;
  - nem Ads nem afiliado.
  É o único lugar, entre as fontes lidas, que mostra oficialmente a sobreposição entre afiliado e Ads.

Leitura de método [OBS]: a página define métricas de **anúncio**. O Data Compass completo (produto, criador, clientes) aparece em tutoriais, mas suas definições não foram lidas em página oficial nesta rodada. O nome da seção em pt-BR também não foi confirmado.

- **Criativos do GMV Max no Data Compass:** caminho Data Compass > LIVE e vídeo > Vídeo > Detalhes do vídeo. Mostra receita e pedidos de cada criativo da campanha de produto, com exportação e filtro por produto. [OFICIAL] ads.tiktok.com/help/article/how-to-see-metrics-for-your-creative-assets-in-seller-center, 2025-08 **(pode estar superada)**.

### 2.3 Painel do GMV Max: o que o número inclui
- **Receita bruta** = pedidos do TikTok Shop "pagos e orgânicos" atribuídos à campanha.
- **ROI** = retorno de todos os pedidos atribuídos.
- **Custo por pedido** inclui pedidos orgânicos e pagos. O próprio TikTok recomenda usar a receita bruta, não o custo por pedido, para julgar produto ou vídeo.
- Pedido é contado por SKU. "Ver criativos" abre o desempenho por vídeo ou imagem.
[OFICIAL] ads.tiktok.com/help/article/how-to-see-reporting-for-your-product-gmv-max-campaign, 2026-06.

No Brasil, o blog oficial pt-BR (2026-05-13) apresenta:
- a Central de Criativos do GMV Max (criativos e criadores que mais geram GMV);
- relatórios de transbordamento ("spillover");
- o ROI "Pro" **em teste**, que considera fluxos de tráfego, custo de afiliado, cupons e tarifas.
[OFICIAL] ads.tiktok.com/business/pt-BR/blog/gmv-max-automate-shop-roi, 2026-05-13.

Consequência: o ROI padrão não é ROAS incremental e, até prova em contrário, não desconta afiliado nem tarifa. A divergência com o praticante BR que diz o contrário fica registrada em metodo.md §4.3.

Terceiros confirmam a mesma leitura:
- O Daasity diz que o GMV Max atribui a si os pedidos orgânicos e de afiliado.
- A Fospha conta 1 pedido = 1 pedido (não por SKU) e usa receita líquida, por isso nunca bate com o TikTok.
[DADO] help.daasity.com; help-center.fospha.com (via resumo de busca, s/d).

### 2.4 Central de Afiliados: o que filtra e o que limita (BR)
- **Filtros de criador para amostra** [OFICIAL] Academy BR kid=6589441682917136, 2026-02-05 **(pode estar superada)**:
  - categoria (receita ou promoção na categoria em 30 dias, ou produto adicionado à vitrine em 90 dias);
  - seguidores;
  - tipo de conteúdo (vídeo, LIVE ou ambos em 30 dias);
  - agência ou independente;
  - colaborações anteriores;
  - idade e gênero do seguidor;
  - GMV de 30 dias;
  - views médias por vídeo (opção de contar só os vídeos de afiliado);
  - espectadores médios por LIVE;
  - "Criadores confiáveis" = os 20% melhores em proporção de amostras recebidas que viraram conteúdo publicado.
- **Prazos:**
  - o criador tem 14 dias para publicar com a amostra;
  - o vídeo fica público por pelo menos 3 dias, ou a LIVE dura pelo menos 10 minutos;
  - o vendedor tem 7 dias para analisar o pedido de amostra, mas a mesma página cita rejeição automática em 30 dias. Contradição interna, a conferir.
- **Convites direcionados:** até 50 criadores e 100 produtos por convite, e até 1.000 colaborações em 24 h. Se o produto está na colaboração aberta e na direcionada, vale a comissão da direcionada. Mudança no convite vale no dia seguinte. A página não fala em teto semanal. [OFICIAL] Academy BR kid=6580476438529809, 2025-04-14 **(pode estar superada)**.
- **Teto semanal de primeiro contato** (via fornecedores, não lido em N1):
  - escala com o GMV **de afiliados** de 30 dias; venda orgânica não conta;
  - com GMV zero, o outreach fica bloqueado;
  - convite e DM ao mesmo criador na mesma semana gastam uma vaga só;
  - criador que já respondeu não conta;
  - renova no domingo.
  [DADO] cruva.com/help-center/having-an-issue/outreach-caps-and-limits, s/d; hubfluence.io, 2026-06-10 (EUA).
  - Faixas da Hubfluence: 1.000 (pacote inicial), 2.000, 7.000 e ilimitado.
  - Uma agência dos EUA cita o 3º nível com ≈ 7 mil criadores por semana (AD32WdQGXRY, 2026-08-20). Outra cita "ilimitado" ≈ 10 mil por semana (metodo.md §3.4).
  - O caminho no painel seria Afiliados > Colaboração direcionada > Ver regras (resumo de busca sobre aftership.com e joinbrands, 2026-10).
- **Possível novo teto diário:** a AfterShip afirma que, a partir de 9 de outubro (de 2026), o TikTok Shop limita novos convites a 200 criadores por dia. [DADO via resumo de busca] aftership.com, 2026-10-07. A página devolveu 403 e o país não foi confirmado. Tratar como não confirmado.

### 2.5 Como as ferramentas de terceiros estimam (o que se sabe)
| Ferramenta | Base declarada | Atualização | Erro | Atribuição a vídeo e LIVE |
|---|---|---|---|---|
| Kalodata | "Canais públicos" + modelos de IA retreinados diariamente (G2, via busca, s/d) | Não publicada | "Pequenas variações" em transação e Ads | Mostra receita por criador, vídeo e LIVE e selo "AD" no vídeo (MFNkRTC-tzo). Num vídeo BR, mostra a fatia da receita do vídeo vinda de anúncio (91% no exemplo de 25vuaes4kjc, 2026-10-07) |
| FastMoss | Não publica método; "dados de vendas precisos" (fastmoss.com, 2026-10-15) | "Atualizações rápidas", acompanhamento diário | Não publica | LIVE em tempo real (vendas, visitas, pico de espectadores) e vídeo com vendas e receita (YZ8FGCmIPTc; 9vNHkmjzPZQ) |
| EchoTik | Sinais de mercado + dado de conta autorizada | **Sem intervalo fixo**: vídeo "geralmente mais rápido"; LIVE revisada depois do fim da sessão; atribuição a criador atrasa | Não publica | Idem, com aviso de revisão |
| Tabcut | Não publica; "espelha mais de 90%" | A cada 24 h | Não publica | Listas de 1, 3 e 7 dias; monitoramento de influenciador com dado ≈ 1 h depois de adicionado |
| Shoplus | Não publica | Não informada na página de preços (metodo.md: "de hora em hora") | Não publica | Produto, criador, vídeo, loja |
| Cruva | Observação diária de milhões de links públicos + modelos | Diária | **≈ ±30%**, varia com a estratégia de afiliados | Prioriza criadores de maior desempenho com vídeo comprável, por isso subconta vídeos e GMV |

Pontos de método [OBS]:
- **A atribuição de GMV por vídeo e LIVE é a parte mais frágil.** A ferramenta só vê o que tem link público. LIVE é revista depois (EchoTik), e criador pequeno é subamostrado (Cruva).
- **A separação orgânico × anúncio por vídeo** que a Kalodata exibe não tem método publicado. O próprio TikTok só faz essa separação para a loja dona, no Data Compass.
- **Ferramentas discordam entre si.** "São ferramentas de estimativa, têm estimativas diferentes" diz o fundador da SmartScout (5Bw9zTCbvHg, 2026-08-11, EUA). Num tutorial, Kalodata e FastMoss mostraram rankings de top produtos diferentes para o mesmo país e dia (hPruXGL9xos, 2026-03-03, EUA). Em aula BR, dois alunos viram "1 milhão" e "3,7 milhões" no mesmo produto (metodo.md §3.3).

---

## 3. O que os melhores fazem

### 3.1 Fluxo de pesquisa (consenso)
1. **Produto.** Ranking por GMV ou unidades em 7, 28 ou 30 dias, com filtro de país e categoria. Depois, a curva diária. [PRÁTICA] MFNkRTC-tzo; 9vNHkmjzPZQ; rA2nsDx7-Jg (EUA); PfPTgT_KJf0 (EUA).
2. **Criadores do produto.** Quem mais vende aquele item na janela escolhida (Kalodata: 7 ou 30 dias no gratuito). [PRÁTICA] MFNkRTC-tzo.
3. **Vídeos.** Ordenados por venda; o selo "AD" indica que a loja impulsiona. Lido como "validado", mas também como sinal de que o alcance foi comprado (h7-OxsXH8AI, EUA; 25vuaes4kjc). [PRÁTICA]
4. **LIVE.** Duas ferramentas com papéis diferentes, segundo uma praticante BR:
   - FastMoss para acompanhar em tempo real quem está vendendo agora (útil para pegar "oferta relâmpago");
   - Kalodata para o histórico e as gravações.
   [PRÁTICA] [REVENDA] YZ8FGCmIPTc, 2026-02-09 (vende curso).
5. **Loja concorrente.** Top produtos, preços, criadores e curva da loja. Para afiliado, "não é uma opção muito usada" (MFNkRTC-tzo). Para marca, é o ponto de partida (AD32WdQGXRY, EUA; dW7lF22BlKU, EUA).
6. **Criadores do concorrente** ("affiliate sniping"). Na loja concorrente, abrir a análise de afiliados (7, 28 ou 90 dias, ordenada por GMV ou unidades), exportar e convidar em lote com aprovação manual de amostra. [PRÁTICA] [MARCA] AD32WdQGXRY (EUA). Um vendedor dos EUA atribui "grande parte" do seu resultado a esse método na Kalodata (pOAL8R1dWK0, 2026-10-10, EUA). Outro usa a FastMoss para o mesmo fim (mSI-O3m1_ho, 2026-01-01, EUA).
7. **Validação manual no app.** Conta nova, busca por palavra-chave do produto, conferir se vários criadores aparecem e se há comentários reais. [PRÁTICA] PfPTgT_KJf0 (EUA, vende mentoria).

### 3.2 Filtros e cortes que aparecem
| Fonte | Objetivo | Cortes |
|---|---|---|
| rA2nsDx7-Jg (CreatorBrian, 2026-02-01, EUA) [REVENDA] afiliado de vídeo | Produto de baixa concorrência | Fonte de receita = vídeo; receita de 30 dias de US$ 30 mil a 200 mil; crescimento de 20% a 100% (rejeita 999%, lido como Ads ou viral único); de 2 a 100 criadores; olhar concentração |
| h7-OxsXH8AI (Derek Kumo, 2026-09-05, EUA) | Demanda alta, competição baixa, via FastMoss MCP + IA | GMV ≥ US$ 10 mil em 7 dias; crescimento semanal ≥ 15%; < 600 criadores; comissão ≥ 10%; ranking por receita por criador |
| PfPTgT_KJf0 (Jon Reiter, 2026-05-09, EUA) [MARCA/importação] | Produto para vendedor | Canais da Kalodata "novos produtos", "alto potencial para afiliado" e "vendas crescendo rápido"; depois, custo na Alibaba e calculadora de margem (tarifa de 6% a 8%, afiliado de 15%, margem bruta de 39% no exemplo) |
| XiK_nMFz3Us (ShopShark, 2026-07-22, EUA, patrocinado) | Tendência | Crescimento **e** volume; crescimento percentual sobre base pequena engana |
| DolDBnRQVM4 (Natan Sousa, 2026-09-23, BR) [REVENDA] | Tendência | Comparar curva de 30 dias com a de 7 dias: alta em 30 e queda em 7 = esfriando |
| sejE9lVCO1M (via metodo.md, 2026-06-26, BR) [REVENDA] | Volume | GMV ≥ R$ 200 mil em 30 dias; janela de 7 dias |
| YZ8FGCmIPTc (Lais Fernanda, 2026-02-09, BR) [REVENDA] | LIVE | Ordenar por GMV, não por visitas; preferir criadores afiliados a lojas, porque loja vende mais por ficar mais horas no ar; "lives com poucos seguidores e alta receita" |
| 9vNHkmjzPZQ (Caio Dlugosz, 2025-11-13, BR) [REVENDA] | Produto viral | Índice de popularidade de 0 a 100 da FastMoss; nº de vídeos (≈ 1 mil) contra vendas; proporção por canal (86% via influenciador); vídeos novos por semana como sinal de entrada cedo |

**Concentração** (Kalodata, segundo rA2nsDx7-Jg): receita dos 3 maiores criadores ÷ receita total do produto. Com 70% a 75%, o produto depende de poucos criadores. A fonte não descarta o produto por isso quando há poucos criadores no total.

### 3.3 Escolha de criador: ferramenta × Central de Afiliados
- **Na Central (1ª parte):**
  - categoria;
  - GMV de 30 dias (ex.: ≥ US$ 1 mil a 5 mil no início);
  - views médias (≥ 5 mil);
  - taxa estimada de postagem (70% a 80% ou mais, com exceção para criador de GMV muito alto);
  - nota de amostra (no exemplo, 92% das amostras viram post);
  - divisão de GMV por categoria e por formato (vídeo, LIVE, cartão).
  [PRÁTICA] AD32WdQGXRY (EUA).
- **Checagem manual de 30 segundos:**
  - sinais verdes: vídeo comprável nas últimas 2 semanas, demonstração real, já vendeu na categoria;
  - sinais vermelhos: último post há mais de 1 mês, views sem engajamento, "colecionador de amostras" que repete o mesmo formato para 10 marcas.
  [PRÁTICA] AD32WdQGXRY (EUA).
- **Seguidor não é critério.** "Os seguidores não compram, o público compra" (paráfrase de AD32WdQGXRY). O mesmo aparece em htmvtQC9XJU (EUA, link de afiliado) e YZ8FGCmIPTc.
- **Gestão da base depois do convite (1ª parte + ferramenta de lucro):**
  - criadores "dormentes": venderam e pararam de postar, em geral porque acabou o produto; reenviar amostra trouxe +US$ 18 mil de GMV em um mês;
  - criadores que crescem mais rápido;
  - "primeiro vídeo forte".
  [CASE] [MARCA] HiveHQ, 1ngx3DmdwlQ, 2026-02-20 (EUA, CEO da ferramenta: conflito de interesse).

### 3.4 Análise de vídeo concorrente
- Baixar ou transcrever o vídeo top e decompor em gancho, problema, solução, prova de preço e CTA. Isso é feito com IA (Viral, ferramenta BR: W85iYXiFFIU, 2026-01-08) ou com o módulo de roteiro da FastMoss e da EchoTik (UaZEv-sWUak; echotik.live/pricing). [PRÁTICA] [REVENDA]
- Com o MCP da FastMoss ligado a um assistente de IA: top 3 vídeos de um produto em 90 dias, roteiro e padrão comum. No exemplo, os três eram impulsionados por Ads, sinal de que o alcance não era orgânico. [PRÁTICA] h7-OxsXH8AI, 2026-09-05 (EUA, link de afiliado).
- Marca grande de suplemento (EUA): a ferramenta serve sobretudo para estudar vídeos, sabendo que muito vídeo de marca é impulsionado. [PRÁTICA] [MARCA] dW7lF22BlKU, Hayden Bowles, 2026-05-11 (EUA). A mesma fonte diz que afiliados também assinam essas ferramentas para entrar cedo em produto que está subindo.

### 3.5 Análise de listagem concorrente (marca)
Listar de 5 a 10 anúncios líderes da categoria e anotar:
- preço, variações e kits;
- título e palavras-chave;
- ordem das imagens e vídeos principais;
- avaliações dos dois lados (o que encantou e o que decepcionou).
[PRÁTICA] [MARCA] PkW3bkdFbCM (caso medicube, 2026-10-02, EUA; legenda traduzida).

### 3.6 Painel de 1ª parte que as marcas montam
- Escada de receita: vendas a preço de tabela → GMV depois do desconto → GMV líquido de cancelamento e reembolso. No exemplo: US$ 1 milhão "a preço inflado", US$ 541 mil e US$ 515 mil.
- Depois, deduções:
  - tarifa de 6% (EUA);
  - frete do FBT;
  - CPV;
  - **custo de amostras**;
  - Ads e créditos de GMV Max;
  - comissões, folha e retainers.
- Resultado: marketing em 40% do GMV líquido no exemplo, margem de contribuição e lucro por SKU.
- "Painel do CEO": pedidos, AOV, amostras enviadas, GMV de afiliado, GMV de LIVE, GMV de vídeo comprável, impressões, Ads e TACoS. Clientes novos × recorrentes e % com 1, 2 ou 3 pedidos.
[CASE] [MARCA] 1ngx3DmdwlQ, 2026-02-20 (EUA, ferramenta própria).

Leitura de método [OBS]: é a mesma escada CM1 a CM3 do estado-da-arte, com duas linhas próprias do social commerce, **amostra** e **comissão de afiliado**.

### 3.7 Divergências
- **"AD" = validado** (MFNkRTC-tzo) **× "AD" = alcance comprado, não replicável no orgânico** (h7-OxsXH8AI; 25vuaes4kjc; atARj0cZmv8). As duas leituras são compatíveis: o vídeo convenceu a loja a pagar, mas o número de views não serve de meta orgânica.
- **Janela de 7 dias** (afiliado, timing) **× 90 dias** (marca, evergreen). [PRÁTICA] MFNkRTC-tzo × PfPTgT_KJf0.
- **Seguir a loja ou o criador?** Para LIVE, uma praticante BR manda seguir criadores e ofertas, não lojas (YZ8FGCmIPTc). Agências de marca começam pela loja concorrente (AD32WdQGXRY).
- **Ferramenta é indispensável?** "Você não precisa investir nessas ferramentas no início" (paráfrase de W85iYXiFFIU, que mesmo assim vende cupom). As alternativas gratuitas citadas são a aba Loja, a busca do TikTok, o Creative Center, a Biblioteca de Anúncios da Meta e o próprio Seller Center (FsXd0__CbtM; viniensina.com.br, 2026-07-16).
- **Live dá mais dinheiro que vídeo?** Um praticante BR mede por GMV por hora de LIVE e acha a LIVE "matematicamente mais precisa" (1GDosmkdolA). Ele vende comunidade de agência.

---

## 4. Números de referência

| Número | Fonte | Data | País | Tipo | Leitura |
|---|---|---|---|---|---|
| GMV do TikTok Shop BR no 1º semestre de 2026 ≈ R$ 5,3 bi (US$ 1,0 bi); R$ 1,58 bi em junho de 2026; 110,2 mil lojas e 2,3 mi influenciadores ativos; ≈ 3.500 lojas e ≈ 200 influenciadores acima de US$ 1 mi | momentum.asia (dados Tabcut) | 2026-08 | BR | [DADO] | Estimativa de ferramenta com método só descrito em linhas gerais; faixa, não exato |
| Agosto de 2025: GMV BR US$ 46,1 mi; aba Loja ≈ 50%, vídeo curto 25,70%, LIVE 23,43%; beleza 21,26% | thelowdown.momentum.asia | 2025-09-08 | BR | [DADO] | Um mês só; origem Tabcut provável, não explícita |
| GMV médio diário de maio de 2026 = 102× o de maio de 2025; LIVEs diárias 20×; GMV de LIVE 161× | TikTok Shop via equalocean.com | 2026-08-03 | BR | [OFICIAL via imprensa] | Multiplicador sem valor absoluto |
| Erro de estimativa ≈ ±30% | Cruva | s/d | não informado | [DADO] | Única declaração de erro entre as ferramentas |
| "Mais de 90%" dos dados espelhados | Tabcut | 2026-10-15 | não informado | [DADO] | Alegação sem método |
| GPM de LIVE "ideal" US$ 50 a 150 | EchoTik | 2026-04-28 | não informado | [DADO] | Sem amostra; não usar |
| Teto semanal de outreach: 1.000 / 0 / 2.000 / 7.000 / ilimitado conforme GMV de afiliados de 30 dias | hubfluence.io | 2026-06-10 | EUA | [DADO] | Fornecedor; não confirmado em N1 nem para o BR |
| 200 novos criadores por dia a partir de 9 de outubro | aftership.com (resumo de busca) | 2026-10-07 | provável EUA | [DADO] | Não confirmado |
| Preços EchoTik (anual, por usuário/mês): gratuito, US$ 9,90, 19,10 e 29,10; histórico de 30 dias, 90 dias e ilimitado; monitor de LIVE 5, 50 e 300 por mês | echotik.live/pricing | 2026-10-15 | — | [DADO] | Página oficial |
| Preços Shoplus: US$ 39, 49 e 79 por mês (top 100, 300 e ilimitado) | shoplus.net/pricing | 2026-10-15 | — | [DADO] | Página oficial |
| FastMoss: planos Basic, Pro, Team e Enterprise; cartões com 90 dias de histórico; detalhe de 28, 90 e até 180 dias; contatos de criador 5 a 300 por dia; exportação 2 por dia × 3.000 registros; monitor de vídeo e LIVE 10, 200 e 600 por mês; teste de 7 dias | fastmoss.com/pricing | 2026-10-15 | — | [DADO] | Preço não renderizou |
| FastMoss US$ 558, 854 e 1.084 por ano (90, 180 e 1.200 dias); Kalodata ≈ US$ 49,99 e 109,99 por mês (90 e 180 dias), Enterprise sob consulta (1.000 dias) | hubfluence.io | 2026-10-08 | — | [DADO] | Concorrente; o metodo.md registrou "1.500 dias" na home da FastMoss: divergência |
| Kalodata "≈ US$ 80/mês" | dW7lF22BlKU | 2026-05-11 | EUA | [PRÁTICA] | Link de desconto |
| Kalodata "R$ 2.200/mês" | FsXd0__CbtM | 2026-07-29 | BR | [PRÁTICA] | Dito por quem revende acesso "ilimitado"; incoerente com as outras fontes; não usar |
| Kalodata gratuita: 10 pesquisas; filtros de 7 e 30 dias | MFNkRTC-tzo | 2025-11-16 | BR | [PRÁTICA] | Pode ter mudado |
| Exemplo BR na FastMoss: produto com ≈ 71 mil unidades e ≈ R$ 820 mil em 28 dias; criadora com 20 mil seguidores e ≈ R$ 130 mil de GMV "ontem" | 9vNHkmjzPZQ | 2025-11-13 | BR | [DADO] na tela | Ilustração de escala, não benchmark; época de Natal |
| Exemplo BR na Kalodata: LIVE de 3 h com ≈ R$ 93 mil de GMV só com foto do produto; LIVE de 10 h com ≈ R$ 224 mil | YZ8FGCmIPTc | 2026-02-09 | BR | [DADO] na tela | Ilustração; quem mostra vende curso |
| Vídeo com 91% da receita vinda de anúncio | 25vuaes4kjc (Kalodata via Tockfy) | 2026-10-07 | BR | [DADO] na tela | Método da separação não publicado |
| GMV por hora de LIVE: mínimo de R$ 300; nível 3 de R$ 1.000 a 1.500 | 1GDosmkdolA | 2026-08-11 | BR | [PRÁTICA] | Regra de bolso; quem diz vende comunidade |
| Escada de GMV de uma marca: US$ 1 mi a preço de tabela → US$ 541 mil depois do desconto → US$ 515 mil líquido; marketing ≈ 40% | 1ngx3DmdwlQ | 2026-02-20 | EUA | [CASE] | Uma conta; ferramenta do próprio autor |
| Divisão por canal de um cliente: LIVE 92,24%, vídeo 3,7%, cartão ≈ 4% | ARKJE_iDEbI | 2026-07-25 | EUA | [CASE] | Uma conta |
| "Mais de 60% das vendas do TikTok vêm de LIVE" | ARKJE_iDEbI | 2026-07-25 | EUA | [PRÁTICA] | Sem fonte; no BR, agosto de 2025, a LIVE era 23% (Momentum) |

Nenhum benchmark de conversão, CTR, CTOR ou GPM com fonte para o Brasil foi encontrado.

---

## 5. Alimentos, café e marca própria ou indústria

1. **A categoria é só para convidados no BR** (alimentos e bebidas, página de 2026-04-30; metodo.md §2.6). Consequência de método [OBS]: rankings de ferramenta no BR têm pouca amostra de alimento, e o que aparece tende a ser marca convidada ou produto mal classificado. Antes de concluir "a categoria não vende", conferir quantos produtos de alimento a ferramenta enxerga no BR.
2. **A venda de café observada no BR passa por afiliados.** A mesma marca aparece em seis ou mais perfis de afiliado. [OBS] observacao/vitrine.md, 2026-10-15. O recorte útil é **loja → análise de afiliados** (quantos criadores vendem a marca, concentração nos três maiores) e não só o ranking de produto, porque o GMV de uma marca se espalha em vários vídeos pequenos.
3. **A subamostragem de criador pequeno (Cruva) pesa mais em categoria de cauda longa.** Uma marca de café com muitos afiliados pequenos tende a ter vídeos e GMV subcontados pela ferramenta [OBS a partir de cruva.com].
4. **Recompra é o diferencial de consumível, e a ferramenta não mede recompra.** Só a 1ª parte mostra clientes novos × recorrentes e % com 1, 2 ou 3 pedidos (painel de HiveHQ sobre dados do Seller Center, 1ngx3DmdwlQ, EUA). Que o Seller Center BR mostre novos × recorrentes por loja e **não** por criador está no protocolo, mas não foi confirmado em página oficial nesta rodada.
5. **Exemplos de alimento ou consumível achados com ferramenta (todos EUA):**
   - kit de 8 molhos de pimenta pego cedo por um afiliado, com ≈ US$ 80 mil de um vídeo (rA2nsDx7-Jg);
   - kit de fermentação natural com US$ 81 mil em 30 dias, 77 criadores, comissão de 14% e concentração alta;
   - marca de suplemento com US$ 2,4 a 2,8 mi em 30 dias e US$ 7 mi em 90 dias (dW7lF22BlKU, Kalodata).
   Servem de ilustração do método, não de expectativa para o BR.
6. **Sazonalidade e timing.** Kalodata e FastMoss mostram curva diária e vídeos novos por semana. Para consumível evergreen, a fonte de marca prefere 90 dias e produto "evergreen e presenteável" (PfPTgT_KJf0, EUA). Isso conversa com café em kit e presente. Leitura desta frente, não recomendação.
7. **Alegação de produto.** A política BR restringe alegação medicinal e "detox" ou "superalimento" sem comprovação (metodo.md §2.6, via resumo). As ferramentas de roteiro por IA reproduzem o gancho do vídeo concorrente sem filtrar alegação. É um risco de método ao modelar vídeo de alimento ou suplemento [OBS].

---

## 6. Erros comuns e mitos

1. **"A ferramenta mostra o faturamento real."** Falso. É estimativa sem erro publicado (exceto ±30% da Cruva). "Dados que nem o dono do TikTok tem" (9vNHkmjzPZQ) inverte a realidade.
2. **Tratar GMV como faturamento ou lucro.**
   - GMV é bruto, antes de devolução (EchoTik).
   - O destaque do painel pode estar a preço de tabela (ARKJE_iDEbI, 1ngx3DmdwlQ, EUA).
   - "Base de 10% de comissão" para afiliado (YZ8FGCmIPTc) não é regra: a comissão é definida pelo vendedor por produto (metodo.md §2.1).
3. **Somar ou comparar ferramentas diferentes.** Cada uma tem cobertura, fuso, moeda e tratamento de devolução próprios (EchoTik, 2026-08-07). Nunca somar; comparar só dentro da mesma ferramenta e data.
4. **Ler crescimento percentual sem volume** (999%, ou de 1 para 1.000 unidades). [PRÁTICA] rA2nsDx7-Jg; XiK_nMFz3Us.
5. **Usar views de vídeo impulsionado como meta orgânica.** O selo "AD" e a fatia de receita de anúncio mostram que o alcance foi comprado (25vuaes4kjc; h7-OxsXH8AI).
6. **Tomar o ROI do GMV Max como ROAS incremental.** Ele inclui pedidos orgânicos e, por enquanto, não desconta afiliado nem tarifa [OFICIAL].
7. **Escolher criador por seguidores.** Contradiz todas as fontes de agência lidas.
8. **Achar que o software de outreach multiplica convites.** O teto é da plataforma e depende do GMV de afiliados (Cruva; Hubfluence). Um fornecedor sugere inflar o GMV com compras pelo próprio vídeo de afiliado (joinbrands, via resumo de busca). Isso arrisca a conta.
9. **Raspar dados ou burlar o limite gratuito** (e-mail temporário, inspetor do navegador; MFNkRTC-tzo; sejE9lVCO1M). A própria agência dos EUA diz que raspar a Central viola política (AD32WdQGXRY).
10. **Comprar acesso "ilimitado" revendido.** Tockfy aparece em quatro vídeos de um canal BR prometendo "Kalodata ilimitado". A legitimidade do acesso não foi verificada, e o canal ganha com a venda.
11. **Copiar o número de uma peça como regra** ($90K de um vídeo, R$ 93 mil em 3 h de LIVE). É sobrevivência, não média.
12. **Confundir métricas:**
    - GPM por impressão, por view ou por espectador;
    - CTR de anúncio (visitas à página do produto ÷ impressões) com CTR de vídeo orgânico;
    - CTOR com conversão de visita.
13. **Regra de outro país como brasileira:** tarifa de 6% a 8% dos EUA, teto de outreach em dólar, reset às 12 h GMT-7.

---

## 7. Revenda ou importação × indústria ou marca própria

| Dimensão | [REVENDA] afiliado, dropshipping, importação | [MARCA] indústria e marca própria |
|---|---|---|
| Pergunta principal | O que está subindo agora e onde entro antes da saturação? | Quem vende minha categoria, com que criadores e criativos, e quanto sobra depois de comissão, amostra e Ads? |
| Ferramenta típica | Kalodata, FastMoss, Viral (BR) e EchoTik em modo ranking; FastMoss ao vivo para LIVE | Mesmo conjunto para concorrência e criadores, mais Seller Center (Data Compass, Central de Afiliados, GMV Max), ferramenta de lucro (HiveHQ e similares), CRM de afiliados (Hubfluence, Cruva, Euka, Reacher) e SmartScout para participação por categoria e cruzamento com a Amazon |
| Janela | 7 dias (timing) | 28 a 90 dias, mais curva de 6 meses para sazonalidade |
| Cortes | GMV mínimo, crescimento, nº de criadores, comissão, concentração | Comissão paga pelos concorrentes (para calibrar a própria), taxa de postagem e nota de amostra do criador, custo por amostra que virou post, receita por SKU |
| Uso do vídeo concorrente | Modelar roteiro, muitas vezes com IA e sem rosto | Entender padrões (gancho, objeção, demonstração) para briefing de criadores; separar vídeo orgânico de impulsionado |
| Risco de método | Copiar o pico de quem já saiu; produto de baixa qualidade derruba a conta do afiliado junto (1GDosmkdolA) | Confundir ROI atribuído com incremental; subcontagem de afiliados pequenos; histórico curto no plano básico (90 dias) para analisar sazonalidade |
| Conflito de interesse mais comum | Cupom de ferramenta + curso ou mentoria (9vNHkmjzPZQ, W85iYXiFFIU, YZ8FGCmIPTc) | Fundador da ferramenta apresentando "o painel que as marcas usam" (1ngx3DmdwlQ, 5Bw9zTCbvHg); agência que vende serviço (AD32WdQGXRY) |

---

## 8. Tabela de afirmações

| id | Afirmação | Tipo | Fonte | Data | País | Confiança |
|---|---|---|---|---|---|---|
| A1 | Cruva declara erro de ≈ ±30%, que varia com a estratégia de afiliados, e prioriza criadores de maior desempenho com vídeo comprável | [DADO] | cruva.com/help-center/social-intelligence/social-intelligence-data | s/d | não informado | A (para o que a Cruva declara) |
| A2 | Kalodata coleta de "canais públicos" e refina com IA retreinada diariamente; admite variação em transação e Ads | [DADO] | g2.com/sellers/kalodata (via resumo de busca; página 403) | s/d | — | B |
| A3 | Tabcut atualiza a cada 24 h e alega espelhar "mais de 90%" dos dados, sem método | [DADO] | tabcut.com | 2026-10-15 | — | B |
| A4 | EchoTik não promete intervalo fixo de atualização; LIVE é revista depois do fim; atribuição a criador atrasa | [DADO] | echotik.live/blog/how-accurate-is-tiktok-shop-data | 2026-08-07 | — | B |
| A5 | Método genérico de estimativa: diferença diária de estoque × preço; não confirmado para Kalodata ou FastMoss | [DADO] | scrapecreators.com | 2025-08-06 | EUA | C |
| A6 | Data Compass: atribuição padrão de 7 dias após clique ou 1 dia após visualização; Seller Center conta vendas do mesmo dia, Ads Manager usa 7 dias | [OFICIAL] | ads.tiktok.com/help/article/about-ads-metrics-in-seller-center | 2025-02 | global | B (pode estar superada) |
| A7 | Receita bruta = valor pago pelo comprador − impostos + descontos da plataforma; pedido contado por SKU | [OFICIAL] | idem | 2025-02 | global | B |
| A8 | Visão geral do Data Compass separa receita em Ads, não Ads, Ads sem afiliado, Ads e afiliado, afiliado sem Ads e nenhum | [OFICIAL] | idem | 2025-02 | global | B |
| A9 | Definições: CTR = visitas à página do produto ÷ impressões; CTOR = pedidos ÷ visitas à página do produto; taxa de entrada na LIVE = PV ÷ impressões | [OFICIAL] | idem | 2025-02 | global | B |
| A10 | Receita bruta, ROI e custo por pedido do GMV Max incluem pedidos orgânicos e pagos | [OFICIAL] | ads.tiktok.com/help/article/how-to-see-reporting-for-your-product-gmv-max-campaign | 2026-06 | global | A |
| A11 | ROI "Pro" (afiliado, cupom, tarifa) está em teste | [OFICIAL] | ads.tiktok.com/business/pt-BR/blog/gmv-max-automate-shop-roi | 2026-05-13 | BR (página pt-BR) | A |
| A12 | Criativos do GMV Max: Data Compass > LIVE e vídeo > Detalhes do vídeo, com receita e pedidos por criativo | [OFICIAL] | ads.tiktok.com/help/article/how-to-see-metrics-for-your-creative-assets-in-seller-center | 2025-08 | global | B (pode estar superada) |
| A13 | Filtros de amostra no BR incluem GMV de 30 dias, views médias, espectadores de LIVE, agência e "Criadores confiáveis" (top 20%) | [OFICIAL] | Academy BR kid=6589441682917136 | 2026-02-05 | BR | B (pode estar superada) |
| A14 | Amostra: 14 dias para postar; vídeo público por 3 dias ou LIVE de 10 min; 7 dias para o vendedor analisar (a página também cita 30) | [OFICIAL] | idem | 2026-02-05 | BR | B |
| A15 | Convite direcionado: até 50 criadores e 100 produtos; até 1.000 colaborações em 24 h; vale a comissão da direcionada | [OFICIAL] | Academy BR kid=6580476438529809 | 2025-04-14 | BR | B (pode estar superada) |
| A16 | Teto semanal de primeiro contato escala com o GMV de afiliados de 30 dias (1.000 / 0 / 2.000 / 7.000 / ilimitado), renova no domingo e não conta venda orgânica | [DADO] | hubfluence.io/blog/tiktok-shop-outreach-message-limits; cruva.com outreach caps | 2026-06-10 / s/d | EUA | C para o BR |
| A17 | Novo limite de 200 novos criadores por dia desde 9 de outubro | [DADO] | aftership.com (resumo de busca; página 403) | 2026-10-07 | provável EUA | C |
| A18 | GMV do TikTok Shop BR no 1º semestre de 2026 ≈ R$ 5,3 bi; R$ 1,58 bi em junho; 110,2 mil lojas e 2,3 mi influenciadores | [DADO] | momentum.asia (Tabcut) | 2026-08 | BR | B |
| A19 | Agosto de 2025: aba Loja ≈ 50%, vídeo 25,70%, LIVE 23,43% do GMV BR | [DADO] | thelowdown.momentum.asia | 2025-09-08 | BR | B (um mês; fonte do dado não explícita) |
| A20 | GMV médio diário BR em maio de 2026 = 102× o de maio de 2025; GMV de LIVE 161× | [OFICIAL via imprensa] | equalocean.com | 2026-08-03 | BR | B |
| A21 | Preços EchoTik: US$ 9,90 / 19,10 / 29,10 por usuário/mês (anual); histórico de 30 dias / 90 dias / ilimitado | [DADO] | echotik.live/pricing | 2026-10-15 | — | A |
| A22 | Preços Shoplus: US$ 39 / 49 / 79 por mês | [DADO] | shoplus.net/pricing | 2026-10-15 | — | A |
| A23 | FastMoss: US$ 558 / 854 / 1.084 por ano (90 / 180 / 1.200 dias); Kalodata ≈ US$ 49,99 / 109,99 por mês (90 / 180 dias) | [DADO] | hubfluence.io/blog/kalodata-vs-fastmoss | 2026-10-08 | — | C (concorrente) |
| A24 | FastMoss limita contatos de criador a 5–300 por dia e exportação a 2 por dia × 3.000 registros; teste de 7 dias | [DADO] | fastmoss.com/pricing | 2026-10-15 | — | B |
| A25 | Kalodata tem interface em pt-BR; FastMoss, EchoTik e Shoplus em inglês | [DADO] | viniensina.com.br/melhores-ferramentas-tiktok-shop | 2026-07-16 | BR | B |
| A26 | FastMoss e Kalodata têm filtro Brasil com LIVE em tempo real (FastMoss) e gravações (Kalodata) | [PRÁTICA] | 9vNHkmjzPZQ; YZ8FGCmIPTc | 2025-11-13; 2026-02-09 | BR | B |
| A27 | Concentração = receita dos 3 maiores criadores ÷ receita do produto (Kalodata) | [PRÁTICA] | rA2nsDx7-Jg | 2026-02-01 | EUA | B |
| A28 | Cortes para produto alcançável: US$ 30 mil a 200 mil em 30 dias, crescimento de 20% a 100%, de 2 a 100 criadores | [PRÁTICA] [REVENDA] | rA2nsDx7-Jg | 2026-02-01 | EUA | B |
| A29 | Cortes via FastMoss MCP: ≥ US$ 10 mil em 7 dias, ≥ 15% de crescimento semanal, < 600 criadores, comissão ≥ 10% | [PRÁTICA] | h7-OxsXH8AI | 2026-09-05 | EUA | B |
| A30 | Agências colhem criadores na "análise de afiliados" da loja concorrente (7, 28 ou 90 dias, por GMV) e convidam com aprovação manual de amostra | [PRÁTICA] [MARCA] | AD32WdQGXRY; pOAL8R1dWK0 | 2026-08-20; 2026-10-10 | EUA | B |
| A31 | Filtro de criador: taxa estimada de postagem ≥ 70% a 80%, views médias ≥ 5 mil, GMV de 30 dias ≥ US$ 1 mil a 5 mil | [PRÁTICA] | AD32WdQGXRY | 2026-08-20 | EUA | B |
| A32 | Criadores dormentes reativados com nova amostra trouxeram +US$ 18 mil de GMV em um mês | [CASE] [MARCA] | 1ngx3DmdwlQ | 2026-02-20 | EUA | C (ferramenta do autor) |
| A33 | Número de destaque do painel está a preço de tabela; o valor real fica em Finanças | [PRÁTICA] | ARKJE_iDEbI; 1ngx3DmdwlQ | 2026-07-25; 2026-02-20 | EUA | C (contradiz a definição oficial de receita bruta; conferir) |
| A34 | Na LIVE, seguir criadores afiliados e não lojas, porque loja vende por ficar mais horas no ar | [PRÁTICA] [REVENDA] | YZ8FGCmIPTc | 2026-02-09 | BR | C (vende curso) |
| A35 | Ferramenta BR (Viral) exclui produtos do próprio dono para evitar manipulação; janelas de 7, 28 e 90 dias; transcrição e "insight viral" | [PRÁTICA] | W85iYXiFFIU | 2026-01-08 | BR | C (cupom + curso) |
| A36 | Kalodata exibe a fatia da receita de um vídeo vinda de anúncio (91% no exemplo) | [DADO] na tela | 25vuaes4kjc | 2026-10-07 | BR | C |
| A37 | Kalodata gratuita: 10 pesquisas e filtros de 7 e 30 dias | [PRÁTICA] | MFNkRTC-tzo | 2025-11-16 | BR | C (pode ter mudado) |
| A38 | FastMoss paga de 15% a 30% de comissão recorrente a afiliados que indicam assinaturas | [PRÁTICA] | UaZEv-sWUak | 2025-12-11 | EUA | B |
| A39 | GPM = receita por mil impressões; VSR = vendas por mil views (EchoTik) | [DADO] | echotik.live/blog/tiktok-gmv-tracking | 2026-04-28 | — | B (definição de uma ferramenta) |
| A40 | GMV por hora de LIVE ≥ R$ 300 como piso; nível 3 com R$ 1.000 a 1.500 por hora | [PRÁTICA] | 1GDosmkdolA | 2026-08-11 | BR | C |
| A41 | "Mais de 60% das vendas do TikTok vêm de LIVE" | [PRÁTICA] | ARKJE_iDEbI | 2026-07-25 | EUA | C (sem fonte; contradiz A19 para o BR) |

---

## 9. Lacunas

1. **Data de início da cobertura do BR** em cada ferramenta: nenhuma página oficial de Kalodata, FastMoss, EchoTik, Shoplus, Tabcut ou Cruva lista o Brasil nem a data de entrada. A cobertura é inferida de telas de tutorial (2025-11 em diante) e do relatório Momentum + Tabcut.
2. **Método de estimativa:** nenhuma ferramenta publica. Falta um teste independente que compare estimativa de ferramenta com Seller Center de lojas reais no BR. Seria possível com lojas que topem abrir o painel (N3/N6).
3. **Data Compass completo em pt-BR:** nome das seções, definições de produto, criador e clientes novos × recorrentes, retenção do histórico, e se existe corte de novos × recorrentes por criador. A página oficial lida só cobre métricas de anúncio e é de 2025-02.
4. **Teto de outreach no BR:** faixas, moeda, dia e hora de reset, e o suposto limite de 200 novos criadores por dia (AfterShip, 2026-10-07). Conferir em Afiliados > Colaboração direcionada > Ver regras (exige login) ou em página da Academy BR.
5. **GPM no Seller Center BR:** qual denominador o painel usa (view, impressão ou espectador). Não aparece nas páginas oficiais lidas.
6. **Número de destaque do painel a preço de tabela** (A33): conferir na lupa do painel BR, porque contradiz a definição oficial de receita bruta.
7. **Preços oficiais de Kalodata e FastMoss:** Kalodata.com e G2 bloqueiam (403), e a página da FastMoss não renderiza o preço. Os valores vêm de concorrente (Hubfluence). Histórico divergente na FastMoss: 90, 180, 1.200 ou 1.500 dias, conforme a fonte.
8. **Viral, Tockfy e outras ferramentas BR** (Cruva BR? Hubfluence BR?): não foram abertas. Tockfy revende acesso a Kalodata, e a legitimidade não foi verificada.
9. **Benchmarks BR com fonte** (CTR, CTOR, GPM, conversão de LIVE, taxa de postagem): nenhum encontrado.
10. **Alimentos:** quantos produtos de alimento e bebida as ferramentas enxergam no BR e se a categoria só para convidados aparece separada.
11. **Transcrições fora desta rodada:** Q2m0gPCQxAg (Kalodata) e U3-7SyOleMM (agência) seguem sem legenda em pt (limite 429, ver metodo.md §10).
12. **Fontes com método ou amostra:** a meta de 3 foi atingida só de forma parcial:
    - Momentum Works + Tabcut (dados de plataforma em grande escala);
    - Cruva (erro declarado);
    - EchoTik (método qualitativo).
    O levantamento Opinion Box (n = 1.066 usuários, janeiro) apareceu só em resumo de busca e não foi aberto.

---

## 10. Verificação web (2026-10-15)

Método: WebFetch nas URLs oficiais e 4 WebSearch. Nenhuma página do Seller Center logado foi aberta. Páginas de ads.tiktok.com não declaram país; tratar como global.

| id | veredito | fonte oficial | observação |
|---|---|---|---|
| A6 | CONFIRMADA (global; BR não confirmado) | ads.tiktok.com/help/article/about-ads-metrics-in-seller-center (atualizada 2025-02; pode estar superada) [OFICIAL] | A página diz janela padrão de 7 dias após clique ou 1 dia após visualização; Seller Center conta vendas do dia; Ads Manager conta a janela de 7 dias. Também diz que o painel de Ads credita a venda ao dia do clique. Não há página BR; vale para o Brasil só por inferência. |
| A7 | CONFIRMADA | mesma página (2025-02); definição repetida em ads.tiktok.com/help/article/about-gross-revenue-for-tiktok-shop-ads (2025-08) [OFICIAL] | Receita bruta = pago pelo comprador − impostos sobre vendas + descontos de produto da plataforma. Pedidos contados por SKU; uma compra pode gerar vários pedidos. País não declarado. |
| A8 | CONFIRMADA | mesma página (2025-02) [OFICIAL] | Seis cortes: com Ads, sem Ads, Ads sem afiliado, Ads e afiliado, afiliado sem Ads, nenhum dos dois. Nomes em inglês; o nome em pt-BR do Data Compass não foi verificado. |
| A10 | CONFIRMADA | ads.tiktok.com/help/article/how-to-see-reporting-for-your-product-gmv-max-campaign (2026-06) [OFICIAL] | Receita bruta, ROI e custo por pedido incluem pedidos orgânicos e pagos atribuídos à campanha. A página avisa que o gasto alto pode distorcer ROI e custo por pedido. Global. |
| A11 | CONFIRMADA em parte | ads.tiktok.com/business/pt-BR/blog/gmv-max-automate-shop-roi (2026-05-13) [OFICIAL] | Confirmado: ROI "Pro" (afiliado, cupons, tarifas) "atualmente em teste". NÃO confirmado de forma explícita: que o ROI padrão não desconta esses custos; a página só sugere isso. Tratar a segunda frase como inferência. |
| A13 | CONFIRMADA | Academy BR kid=6589441682917136 (2026-02-05; pode estar superada) [OFICIAL] | "Criadores confiáveis" = os 20% melhores pela proporção de amostras recebidas que viraram conteúdo publicado. Brasil. |
| A14 | CONFIRMADA (contradição interna mantida) | idem (2026-02-05) [OFICIAL] | 14 dias para publicar; vídeo público por 3 dias ou LIVE de 10 min; vendedor tem 7 dias para analisar; a página também cita filtro de rejeição automática em 30 dias, sem reconciliar. Brasil. |
| A15 | CONFIRMADA | Academy BR kid=6580476438529809 (2025-04-14; pode estar superada, mais de 6 meses) [OFICIAL] | Até 50 criadores e 100 produtos por convite; até 1.000 colaborações em 24 h; produto em colaboração aberta e direcionada paga a comissão da direcionada. Brasil. Limites podem ter mudado (ver A16 e A17). |
| A16 | SEM FONTE OFICIAL | nenhuma encontrada (WebSearch em seller-br e Academy não trouxe página) | Não existe página oficial lida com faixas semanais, reset no domingo ou regra de GMV de 30 dias. Fontes de terceiros citam reset semanal no domingo (Hamstergarage) e a regra de GMV de afiliados zero sem contato (Euka, 2026-04), mas são EUA e privadas de método. Seguir como [DADO] C para o BR. Conferir em Afiliados > Colaboração direcionada > Ver regras (exige login). |
| A17 | SEM FONTE OFICIAL | nenhuma encontrada | Só o blog da AfterShip (2026-10-07, vendor concorrente) cita 200 novos convites por dia desde 9/10 e cota compartilhada com ferramentas de terceiros. Fontes mais antigas citam 1.000 em 24 h e 400 por dia (Superfiliate, 2024-12). Conflito não resolvido; país não confirmado. Não usar como regra. |
| A20 | CONFIRMADA (com ressalva de base) | newsroom.tiktok.com/tiktok-shop-cresce-102-vezes-em-seu-primeiro-ano-no-brasil (2026-06-04) [OFICIAL] | Newsroom BR: GMV médio diário por mês 102× desde o lançamento no Brasil (meses de comparação não citados); LIVEs diárias 20× e GMV de LIVE 161×, maio de 2025 contra maio de 2026. EqualOcean (2026-08-03) repete atribuindo ao TikTok Shop. Dado informado pela própria plataforma, sem auditoria. |
| A33 | CONTESTADA | ads.tiktok.com/help/article/about-gross-revenue-for-tiktok-shop-ads (2025-08) [OFICIAL] | A fonte oficial diz: no Seller Center, GMV = pagamento do cliente (já com descontos), e receita bruta = GMV − impostos + descontos da plataforma. Não fala em preço de tabela. Há só uma ressalva: os painéis do Seller Center podem excluir alguns descontos da plataforma do GMV, o que explica diferença com a receita bruta de Ads. A tela do painel BR não foi vista (exige login); os vídeos são EUA e prática de terceiros. |

Pendentes de navegador (exigem login ou tela renderizada): A16 e A17 (Afiliados > Colaboração direcionada > Ver regras no Seller Center BR) e A33 (lupa do número de destaque no painel BR).

## 11. Verificação pelo navegador (2026-10-15)

Método: Claude in Chrome, páginas oficiais renderizadas lidas por JavaScript (Academy BR e Newsroom BR), sem login próprio, sem captcha. Tudo Brasil, salvo indicação. Data entre parênteses é a da página.

| id | veredito | fonte | observação |
|---|---|---|---|
| A16 | SEM FONTE OFICIAL | seller-br.tiktok.com/university/search?keyword=limite%20convite%20criadores%20por%20dia | Academy BR: 'Encontrar criadores para afiliados' (kid=6576089779898113, 2026-02-25) não traz faixas semanais, reset no domingo nem regra de GMV de 30 dias. Academy US redireciona para BR na sessão. Regra fica no Seller Center logado. |
| A17 | SEM FONTE OFICIAL | seller-br.tiktok.com/university/search?keyword=limite%20convite%20criadores%20por%20dia | Única cota oficial achada é de CAP (agência parceira de criadores), não do vendedor. 'Convite de Colaboração' (kid=6817362679023376, 2025-04-14) diz que não há limite de convites que o criador recebe. Os 200/dia seguem só AfterShip. Trecho: "CAPs podem enviar até 100 convites por dia para criadores". |
| A33 | CONTESTADA | seller-br.tiktok.com/university/essay?knowledge_id=6880013740476161 (2025-04-16) | Academy BR 'GMV vs Liquidação': GMV da Bússola de Dados é igual ao total pago pelo cliente, não preço de tabela. Certo só em parte: o valor recebido (Liquidação) fica em Finanças, após taxas e ajustes. Página com mais de 6 meses: pode estar superada. [OFICIAL] BR Trecho: "GMV = preço original do produto - todos os descontos + taxas pagas pelo cliente". |
