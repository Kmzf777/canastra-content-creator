# TikTok Shop: lacunas da rodada 1 e plano da próxima rodada

Versão de 2026-10-16. Crítica de completude feita sobre `protocolo.md`, `CONSOLIDADO.md`, as 16 notas de frente (seções 9, 10 e 11 de cada uma), `verificacao/resultado.tsv`, `social/notas.md`, `observacao/vitrine.md`, `metodo.md` §10 e o corpus de vídeos (`videos.tsv`, `selecionados.tsv`, `transcricoes/`).

A pesquisa é neutra. Este arquivo lista o que falta saber sobre como os melhores operam o TikTok Shop. Não traz recomendação para empresa alguma.

---

## 0. Como ler

**Estado de cada pergunta do protocolo (§7)**
- **R** = respondida com fonte no padrão do protocolo. Pode ter ressalva de data.
- **P** = parcial. Parte tem fonte; parte é prática sem painel, dado de outro país, divergência não resolvida ou regra antiga.
- **S** = sem resposta. Não há evidência que passe no protocolo.

**O que cada lacuna exige**
- **WEB:** WebFetch em URL conhecida.
- **NAV:** agente de navegador, sem login. Para página que só renderiza com JavaScript, captcha ou índice da Academy BR.
- **LOGIN:** só se resolve dentro do Seller Center, da Central de Afiliados ou do Ads Manager de uma loja real. Fica fora do alcance de qualquer agente desta pesquisa.
- **MED:** só se resolve com medição própria (teste, extrato, série de observação).
- **PAGO:** relatório ou ferramenta paga.

**Prioridade da próxima rodada:** P1 (muda leitura de custo, regra ou acesso), P2 (muda tática), P3 (completa o mapa).

**Códigos de citação:** os mesmos do `CONSOLIDADO.md`. "[ads §9.3]" é o item 3 da seção 9 da nota de ads; "[ads R11]" é a linha R11 da verificação; "kid=" é o `knowledge_id` da Academy BR.

---

## 1. Diagnóstico geral

### 1.1 Placar das perguntas do protocolo

| Frente | Perguntas | R | P | S |
|---|---|---|---|---|
| ads | 9 | 1 | 6 | 2 |
| preco-promocao | 8 | 1 | 5 | 2 |
| logistica-estoque | 8 | 2 | 6 | 0 |
| ranqueamento-vitrine | 8 | 1 | 4 | 3 |
| produto-mix | 7 | 0 | 6 | 1 |
| reputacao-atendimento | 8 | 1 | 7 | 0 |
| alimentos-marca-propria | 8 | 0 | 7 | 1 |
| cases-grandes | 8 | 1 | 5 | 2 |
| conteudo-video | 8 | 0 | 6 | 2 |
| live-commerce | 8 | 0 | 4 | 4 |
| afiliados-criadores | 9 | 3 | 5 | 1 |
| conta-onboarding | 8 | 2 | 6 | 0 |
| conta-de-marca-conteudo | 8 | 1 | 4 | 3 |
| dados-mercado-br | 7 | 2 | 5 | 0 |
| ferramentas-analise | 8 | 2 | 4 | 2 |
| regulatorio-fiscal | 8 | 1 | 7 | 0 |
| **Total** | **128** | **18** | **87** | **23** |

Leitura: a rodada 1 cobriu quase todas as perguntas, mas só 14% (18 de 128) fecham no padrão do protocolo. O "P" dominante tem quatro causas que se repetem:
1. a regra é global ou dos EUA, e falta a página BR;
2. a prática vem de um praticante, sem painel e quase sempre dos EUA;
3. duas páginas oficiais BR se contradizem;
4. a página BR é anterior a 2026-04-15.

**Frentes mais fracas:** live-commerce (4 S), ranqueamento-vitrine e conta-de-marca-conteudo (3 S cada).

### 1.2 Lacunas estruturais (valem para todas as frentes)

1. **Nenhum benchmark BR com amostra.** Faltam CPM, CTR, CTOR, GPM, conversão de LIVE, ROI de GMV Max, taxa de devolução, distribuição de SPS e taxa de amostra que vira post [CONSOLIDADO §3; met §10.4].
2. **Nenhum teste de incrementalidade publicado no BR.** Vale para GMV Max, afiliado, LIVE, conta própria e halo para outros canais. No mundo, há só um estudo da plataforma no Reino Unido (n = 11) e números internos [ads §9.7; met §10.5].
3. **A camada N5 (ferramentas) quase não entrou.** Kalodata devolveu 403. Nenhuma faixa de GMV por categoria, loja ou produto foi tirada de Kalodata, FastMoss, EchoTik ou Tabcut com filtro Brasil. Nenhuma ferramenta confirma em página oficial que cobre o BR, nem desde quando [ferr §9.1; dados §9.3; cases §9.1].
4. **A camada N4 (estudo com método) é fina.** A única fonte de escala do BR com método é o relatório pago da Momentum Works (US$ 52,95), que não foi lido [dados §9.2]. Literatura acadêmica sobre live commerce e social commerce não foi consultada em nenhuma frente.
5. **A observação direta (N3) é mínima.** Foram uma passada e um horário, só na categoria Café: 50 cards e 3 páginas de produto, em **sessão logada** [obs §Observação direta]. Ficaram de fora:
   - outras categorias;
   - série temporal;
   - LIVE observada;
   - posição na busca do app;
   - contagem de criadores por produto.
6. **Índice da Academy BR exige JavaScript.** Por isso, páginas que provavelmente existem não foram achadas:
   - GMV Max BR;
   - definições do painel de LIVE;
   - oferta relâmpago e cupom do vendedor;
   - Super Brand Day;
   - FAQ de impostos do criador;
   - guia de envio pelo vendedor;
   - qualidade de anúncio BR [ads §9.2; live §9.2; pre §9.5; marca §9.2; reg §9.1; log §9.1; rank §9.2].
7. **A camada internacional ficou rasa.** De 239 vídeos selecionados, só 4 citam Sudeste Asiático ou Reino Unido. Os dois vídeos de case de SEA e UK (MtJQmOYKIxQ, Cz8mV3p7dk0) ficaram sem transcrição. China (Douyin) não aparece [cases §9.8; alim §9.10]. Cerca de 97 dos 239 selecionados têm título em português; o resto é quase todo dos EUA.
8. **Alimentos têm pouca evidência por dentro da operação.**
   - Só 15 dos 239 vídeos selecionados tratam de alimento ou bebida, e quase todos são dos EUA.
   - Nenhuma fonte social trata de alimento por dentro da operação [soc §7].
   - Nenhum operador de alimento BR mostrou painel.
9. **N2 lido de segunda mão.** CDC, Decreto 7.962/2013, Guia CONAR 2026, LC 214/2025, RDC 429/2020 e Portaria SDA 570/2022 vieram de imprensa, de escritório ou da pesquisa do ML. Nenhuma fiscalização dirigida ao TikTok Shop BR foi achada [reg §9].
10. **Conflito de interesse concentrado.** Vieram de quem vende curso, mentoria, agência ou ferramenta:
    - 13 de 15 vídeos-base em mix;
    - 17 de 21 em cases;
    - 19 de 22 em conta de marca [CONSOLIDADO, Como ler].
11. **Desvio de protocolo a registrar.** A observação direta de 2026-10-16 foi feita com sessão logada, depois de um captcha resolvido pelo usuário [obs]. O protocolo §1.2 pede sem login. O dado vale como [OBS] com possível personalização e precisa ser repetido sem login.

### 1.3 Problemas de consistência achados no CONSOLIDADO

| Ponto | O que o CONSOLIDADO diz | O que as notas sustentam | Ação |
|---|---|---|---|
| Super Brand Day "por convite" | [OFICIAL] em §2.8, §2.13 e §5 | A Newsroom (2026-06-04) cita só a Riachuelo e não diz "por convite", nem cita a Granado [marca R5] | Rebaixar para [PRÁTICA/imprensa] até achar página BR |
| "AHR" como nome dos pontos do vendedor BR | Usa AHR como sinônimo da escala de 0 a 1.000 | A equivalência é [OBS, a confirmar] [onb §9.6]. "AHR" é o nome dos EUA, que substituiu os Violation Points em 2026-07 (ppc.land, EUA) | Confirmar o nome usado na página BR kid=1444948508641040 e na kid=7734094290093831 |
| GMV Max como "único formato desde julho de 2025" | [OFICIAL, global] em §0 | A página de migração é global e não lista países. A página BR mais próxima (kid=3355910447433489) trata de campanha, não de descontinuação | Achar página BR de GMV Max (NAV) |
| Always Fit | Usada como case-âncora em logística, afiliados, mix e cases | Só fala dos sócios, com divergências internas: "60% de afiliados" contra "menos da metade"; "R$ 1 mi/dia" contra "900 e poucos mil" [cases §9.2] | Manter [CASE, fala] e buscar confirmação independente |
| Meta de chat | 70% em 24 h (kid=2583022047233809) | A página é de 2025-09-30. Terceiros citam 85% a 90% e mudança para 12 h em 2025-08 [cases R9] | Reverificar (pode estar superada) |
| Taxa de comissão de Shop Ads | CONFIRMADA no BR | A página BR (kid=5955311610251025, 2026-04-22) confirma. A página global diz "só convidados" [afil A13] | Confirmar no painel se o recurso aparece para toda loja BR (LOGIN) |

---

## 2. Por frente

Em cada frente: estado das perguntas, afirmações sem fonte oficial ou contestadas, camadas que faltaram e o que só se resolve com login ou medição.

### 2.1 ads

| # | Estado | O que falta |
|---|---|---|
| 1 Formatos e descontinuação | P | Página BR de GMV Max; vigência BR de Spark Ads de afiliado e de LIVE GMV Max; data de corte no BR [ads §9.2] |
| 2 Meta e atribuição; modo Pro | P | Janela de atribuição completa (clique, view, 24 h) [ads R2]; o "Pro" está "em teste" no blog pt-BR (2026-05-13), e o PDF que lista o Brasil não diz qual recurso vale onde |
| 3 ROI de equilíbrio por fase | P | Só praticante dos EUA (p7BZwvm2Y_c) e conta [OBS]. Nenhum praticante BR com painel separa lançamento, escala e defesa |
| 4 Produtos e criativos; cadência | P | Divergência entre "poucos produtos" e "todos" [ads R10]. Cadência de troca de criativo sem número |
| 5 Incrementalidade | S | Nenhum teste BR. Relatório de transbordamento sem método. Fospha deu 404 [ads §9.7] |
| 6 Proteção de ROI | P | Existe no BR (kid=3334685477029649); limiares de 90% e 20 pedidos/dia só na página global [ads R3] |
| 7 Benchmarks | S | Nenhum CPM, CTR, CVR, ROI ou custo por pedido BR com amostra; nos EUA, só blogs sem método |
| 8 Pré-requisitos para escalar | P | Prática dos EUA; números divergentes (25 vídeos por semana até 50 por produto) |
| 9 Ads × afiliados | R | Páginas globais (2026-03 e 2026-09) e comissão de Shop Ads BR (kid=5955311610251025) |

**Sem fonte oficial ou contestadas:**
- "50 a 70 vídeos, 5 a 10 por dia", "50 conversões em 7 dias" e "reavaliação a cada 15 minutos" estão CONTESTADOS [ads R11; CRuJUkehO8o].
- Um produto só em uma campanha: SEM FONTE [ads R10].
- Proteção de ROI que depende da meta sugerida: não confirmada [ads §9.8].
- Valor em BRL do creative boost: SEM FONTE [ads R12].
- A regra própria do SFP e do "tráfego gratuito de anúncios" dentro do GMV Max: não lida [ads §9.12].

**Camadas que faltaram:** N1 BR de Ads; N6 BR com painel do GMV Max (só dois casos de ROI de cerca de 15, ambos no pico); N4 de incrementalidade; N5 com selo "AD" por marca de alimento.

**Transcrições que faltam (12):** ciyEKKJPT8c, VqaNndB_vfE, 3XOMFCGbKmE, RVIp1lY0CJY, S4xOd0GwOb4, BimhUTun6vQ, QniRGmboan0, emyPP8gn6pQ, EQJ3UpzBWAw, muQ0ALeY0Mo, VGNbKxg9VxY, DLWchGwGIZU.

**Só com LOGIN ou MED:**
- painel de Anúncios da loja BR: proteção de ROI, Pro, mínimo de boost em BRL e definição na lupa do ROI;
- separação de orgânico nos seis cortes do Data Compass;
- testes de holdout, pausa e comissão de anúncio [CONSOLIDADO §4].

### 2.2 preco-promocao

| # | Estado | O que falta |
|---|---|---|
| 1 Estrutura de custo e take rate | P | "Por item" (unidade, SKU ou kit) [pre A25]; se o 0% da loja nova cobre a taxa fixa e o SFP [pre A4]; se cupom da loja e a parte do vendedor no cupom cofinanciado entram como "desconto do vendedor" na base [pre §9.2] |
| 2 Faixa de R$ 50 e reação de julho | P | A conta está feita [OBS]. A reação dos grandes (preço médio, comissão média, mix de kits antes e depois) não tem dado [pre §9.9] |
| 3 Ferramentas promocionais e quem paga | P | Páginas BR de oferta relâmpago do vendedor, cupom da loja, desconto de produto e "Guia de empilhamento de preços" não achadas. Limites vêm da UpSeller [pre §9.5] |
| 4 Preço de referência | R | 14 dias (kid=5696139560355601, 2026-07-18). Preço-limite de campanha de 2026-02-11 (pode estar superada) |
| 5 Calendário e preparo | P | Black Friday 2026 só na imprensa [pre A19]; regulamento no Seller Center; Super Brand Day e "Brand Crazy Deals" sem página BR |
| 6 Subsídio na base | P | A base do afiliado e a da tarifa estão lidas. A divisão dos R$ 100 mi da Black Friday 2026 está em aberto |
| 7 Efeito da promoção | S | Nenhum estudo separa desconto do vendedor e subsídio da plataforma. +129% é contra o 10/10 [pre §9.8] |
| 8 Conflito com outros canais e entre revendedores | S | Nenhum case BR de paridade de preço. O preço-limite pode ler outras plataformas, mas o método não está descrito |

**Sem fonte oficial ou contestadas:**
- "Taxa de campanha" ou Smart Promotion no BR: SEM FONTE. O que existe é o GMV Max obrigatório em campanha [pre A35; kid=3355910447433489].
- "Todo cupom do vendedor fica fora do histórico": CONTESTADO em parte [pre A13].
- Cupom "100% bancado pela plataforma": não achado [mix A22].
- "Fase intensa a partir de 19/11": fonte única [pre A19].
- Desconto médio e % do GMV em campanha no BR: nenhuma fonte [pre §9.11].

**Camadas que faltaram:** N1 BR das ferramentas promocionais; N5 de preço médio por categoria; N3 de preço riscado fora de café; N6 BR com extrato de Finanças.

**Só com LOGIN ou MED:**
- extrato de um pedido com 2 unidades do mesmo SKU e de um kit;
- extrato dos primeiros 60 dias de loja nova;
- regulamento da Black Friday 2026 no Seller Center;
- painel de missões;
- teste de cupom em metade da base.

### 2.3 logistica-estoque

| # | Estado | O que falta |
|---|---|---|
| 1 Modelos, transportadoras e prazos | P | Guia BR de envio pelo vendedor (LSPs compatíveis, aprovação); lista oficial de transportadoras e regiões, hoje só na imprensa [log §9.1, §9.2] |
| 2 Métricas logísticas | P | Metas lidas. Faltam a janela do LDR ("período aplicável") e as janelas de FDR e VTR [log §9.4] |
| 3 Logística no SPS, campanha e frete grátis | P | O critério de "má experiência" que tira o produto do frete grátis não está definido [log §9.6] |
| 4 Estoque para pico | P | Só um case (Always Fit); sem dado agregado de ruptura [log §9.11] |
| 5 Amostras na logística | P | Prazo de envio da amostra e consequência do não envio [log §9.7] |
| 6 Limites de loja nova | R | kid=1444948507379472 (2026-04-02), tabela lida no navegador |
| 7 Devolução e frete de volta | R | kid=894339073115921 (2026-09-24), com a divergência de alimento (ver §2.7) |
| 8 Embalagem, validade, temperatura | P | Não há validade mínima numérica no BR; os 90 a 270 dias são dos EUA [log §9.10] |

**Sem fonte oficial ou contestadas:**
- O que é "significativamente acima de 4%" para o OVL, e como o OVL é calculado (só referência da Malásia) [log §9.3].
- O corte de "4 horas" do ponto de postagem (KMZ8gimnMhc) [log §9.12].
- Cancelamento em "três dias" (Always Fit) contra 6 dias úteis na política.
- TikTok Logistics Brazil (capital de R$ 111 mi): sem data de operação nem escopo; não reverificada [log A25; dados A19].
- "Cinco transportadoras homologadas": só Meio & Mensagem, sem porta-voz [dados A19].

**Páginas não lidas:** kid=2583991870097169 (cancelamento), kid=6843306600302353 (item faltando ou errado).

**Camadas que faltaram:** N1 do guia de envio; N5 ou N4 de LDR e prazo médio (não existem); N6 BR mostrando painel de saúde logística.

**Só com LOGIN ou MED:** painel de logística e OVL de uma loja; status de pedido atrasado (6 dias úteis × 3 dias); capacidade de expedição num pico de 10× [CONSOLIDADO §8.25].

### 2.4 ranqueamento-vitrine

| # | Estado | O que falta |
|---|---|---|
| 1 O que o TikTok declara sobre recomendação de compra | S | Não há parâmetro oficial da aba Loja nem da busca. O "Para Você" é de 2020, global [rank §9.1] |
| 2 Vitrine do criador, da loja e da marca | P | Vitrine do criador é de 2025-04-14 (pode estar superada). Vitrine da marca e ordenação da loja oficial: sem documento [rank §9.6] |
| 3 Efeito de SPS, selos e avaliações | S | Nenhum número oficial; só o vínculo do selo do SFP com o tráfego [rank §9.3] |
| 4 SEO de produto | P | Consenso de praticantes dos EUA, sem teste; nada BR com painel. Campo de palavras-chave e áudio do vídeo na busca: sem fonte [rank §9.9] |
| 5 Diagnóstico pelo funil | P | Prática sem painel BR |
| 6 Práticas punidas | R | Política de Conteúdo BR (kid=1413208980588305, 2026-07-01) |
| 7 Tempo até tração | P | Prazos com rastro são dos EUA; BR só com relato [rank §9.10] |
| 8 Busca como canal de demanda no BR | S | Sem volume público. Creative Center com filtro BR não confirmado. Os 57% e 23% não têm país [rank §9.5] |

**Sem fonte oficial ou contestadas:**
- "+10% de visibilidade a 2,5", "Poor/Fair suprimidos" e "48% a 65% das vendas vêm da busca" foram derrubados [rank §6].
- Régua de qualidade de anúncio BR: a kid=481891871868714 BR dá 404. Título de até 300 caracteres e até 9 imagens só na UpSeller [rank R10].
- Cupom em troca de avaliação: não há regra BR específica, só a §3.11 [rank R5].
- Divisão entre busca digitada e navegação na aba Loja: nenhuma fonte.

**Camadas que faltaram:**
- N1 legal da UE: os termos do Shop na UE devem listar os principais parâmetros de ranqueamento, mas a leitura parou num captcha [rank §9.1];
- N3 de posição na busca do app;
- N5 de mix por superfície em 2026 (só no relatório pago da Momentum).

**Só com LOGIN ou MED:**
- aba "Melhorar qualidade do anúncio" no Seller Center BR;
- análise de aba Loja e busca (existência no BR não confirmada);
- impressões antes e depois de uma medida de marco, com controle;
- teste de título com e sem palavra-chave.

### 2.5 produto-mix

| # | Estado | O que falta |
|---|---|---|
| 1 Pesquisa de produto nas ferramentas | P | Fluxo descrito por praticante. Nenhuma fonte reporta incerteza como faixa |
| 2 Critérios de entrada | P | Prática; a comissão aceitável diverge (8% a 10% BR contra 15% a 20% EUA) |
| 3 Pico × demanda sustentada; capacidade de repetição | P | Critérios dos EUA. Nenhuma métrica publicada de vídeos ou ângulos por produto antes de saturar [mix §9.10] |
| 4 Categorias líderes e restritas | P | Restritas lidas (2026-04-30). Composição de 2026 por categoria só no relatório pago; Newsroom só qualitativa |
| 5 Sortimento dos grandes | P | Cases dos EUA e fala da Always Fit |
| 6 Racionalização de SKU | S | Nenhum case BR com critério numérico [mix §9.9] |
| 7 Critérios de revenda × marca | P | Síntese sem dado BR |

**Sem fonte oficial ou contestadas:**
- Suplemento em geral "só por convite": DIVERGENTE entre kid=6907568440706832 (2025-12-03) e kid=6504327061473040 (2026-04-30) [mix A4; reg A22].
- "Beleza por convite": CONTESTADO, porque a seção só pede Anvisa [mix A2].
- "10,5% automático": CONTESTADO [mix A19; afil A17].
- Bundle ou pacote no Seller Center BR: sem página (só EUA e Malásia, via terceiro) [mix §9.6].
- "81% dos itens abaixo de US$ 30": sem fonte [mix A36].

**Camadas que faltaram:** N5 com filtro Brasil (nenhuma faixa coletada); N3 de produtos líderes fora de café; curva pós-pico BR.

**Transcrição que falta:** Q2m0gPCQxAg (Kalodata, pt).

**Só com LOGIN ou PAGO:** Kalodata, FastMoss e EchoTik pagos com filtro BR; relatório Momentum BR H1 2026.

### 2.6 reputacao-atendimento

| # | Estado | O que falta |
|---|---|---|
| 1 Cálculo do SPS no BR | P | Janelas e métricas lidas (kid=7517966208927489). Os pesos aparecem só no painel ("--%" na página) [rep §9.1] |
| 2 Consequências por faixa | P | Sem número para CRM, cupons, LIVE Flash Sale e desqualificação de afiliados ("abaixo do padrão") [rep §9.3] |
| 3 Pontos de violação | P | Dedução por tipo não publicada [rep §9.4]. Recuperação ambígua: "+1" ou "até 200 a cada 300 pedidos" [reg §9.9] |
| 4 Operação de atendimento | P | Página de chat de 2025-09-30. Meta dos EUA de 98% não verificada [cases R9] |
| 5 Avaliação negativa e causas | P | Sem limiar BR. Kid=8270844531967761 veio vazia [rep §9.5] |
| 6 Conteúdo do criador e reputação da loja | P | Placar de criador ligado às avaliações dos produtos: noticiado nos EUA, não confirmado no BR [rep §9.12] |
| 7 Métricas internas com margem | P | Prática dos EUA (s2xtJVLtHHg) |
| 8 Recurso de penalidade | R | kid=1444948508641040 (2026-10-14) |

**Sem fonte oficial ou contestadas:**
- Violação reduz alcance: os relatos se contradizem; a página diz que medidas "podem reduzir o tráfego".
- Benchmarks de 1 e 4 pontos por categoria: só o exemplo de LDR de 3% e 8%, de categoria não identificada [rep §9.2].
- LDR do FBT ou do envio pela plataforma fora da conta no BR: não se sabe [rep §9.6].

**Páginas vazias ou não lidas:**
- kid=3989684486358785 (desempenho do criador);
- kid=7204971943560976 (políticas em destaque);
- kid=8994711168665361 (pedidos fraudulentos);
- kid=2324329879832321 (conteúdo gerado por IA);
- kid=3039191651075856 (negociação de contas LATAM) [rep §9.11].

**Camadas que faltaram:** N4 de devolução, avaliação e reclamação (Reclame Aqui deu 403; consumidor.gov.br sem perfil) [rep §9.8]; N6 BR mostrando o painel de saúde; operador de alimento.

**Só com LOGIN ou MED:** pesos do SPS e benchmarks da categoria; dedução de pontos por violação; efeito de medida sobre impressões.

### 2.7 alimentos-marca-propria

| # | Estado | O que falta |
|---|---|---|
| 1 Regras e convite | P | O processo de 6 etapas está lido (kid=6911810440005392). Faltam critérios, documentos por subcategoria e prazo. A lógica "SPS > 4" para loja sem SPS está sem solução [alim §9.1; onb §9.5] |
| 2 Regras de conteúdo × Anvisa e CONAR | P | §4.2 lida. "Superalimento" na lista e HFSS "declarado ao TikTok Shop" não confirmados [vid A7]. Guia CONAR 2026 e Anexo H não lidos |
| 3 Marcas e números no BR | P | Nomes (BIS, SEDE, Desinchá, Guday, Power Focus) sem nenhum número [alim §9.5] |
| 4 Ticket baixo e tarifa fixa | P | Conta [OBS] feita; "por item" aberto; nenhum case BR |
| 5 Marca × revendedores | P | Síntese; sem case de alimento |
| 6 Recompra e assinatura | S | Nenhuma taxa de recompra dentro do Shop (BR ou fora). Assinatura só nos EUA [alim §9.7] |
| 7 Escada de margem | P | Hipotética [OBS]; sem custo real de amostra de alimento |
| 8 Cases fora do BR | P | EUA e Irlanda. SEA só com ranking de rastreador sem método (FindNiche) [alim §9.10] |

**Sem fonte oficial ou contestadas:**
- Devolução de alimento: "não retornável" (kid=2578485181925121, 2026-04-14) contra "volta lacrado" (kid=894339073115921, 2026-09-24) [rep R12].
- "Formulário de 4 etapas" com análise de cadastro: não aparece [alim A7].
- Plano de expansão da categoria no 2º ano: CONTESTADO [alim A14].
- Alimentos e Bebidas "entre as principais categorias": a Newsroom não diz [dados A20].
- Validade mínima no BR: não existe número oficial.

**Camadas que faltaram:**
- N2 completo: RDC 429/2020, IN 75/2020, Portaria SDA 570/2022 lida só pela pesquisa do ML, Anexo H do CBAP;
- N5 da categoria no BR;
- N6 de operador de alimento BR;
- N3 de LIVE de alimento;
- Momentum Works sobre alimentos no SEA.

**Só com LOGIN ou MED:**
- documentos e prazo no Centro de qualificação para cada subcategoria;
- fluxo de devolução da categoria no Seller Center;
- custo por amostra que virou conteúdo e GMV por amostra num ciclo de 4 a 8 semanas [CONSOLIDADO §8.22].

### 2.8 cases-grandes

| # | Estado | O que falta |
|---|---|---|
| 1 Maiores lojas por categoria; mudança desde 2025-05 | S | Nenhum ranking verificável; Kalodata deu 403 [cases §9.1] |
| 2 Alavancas dos líderes | P | Padrões repetidos, mas de fontes com conflito |
| 3 Cases com número verificável | P | Moderna (60%), BigHome (5×, R$ 17 mi) e Natura (+228%) são release sem base nem período [cases §9.3]. Granado: 18 mil produtos contra 18 milhões de impressões [cases R11] |
| 4 Equipe e processo | P | Poucos dados; só Natura e Always Fit |
| 5 Multicanal sem conflito; transbordamento | S | Nenhum case BR de paridade de preço ou com medição controlada [cases §9.6] |
| 6 Quedas e erros | P | Um caso (Always Fit); nenhuma suspensão de grande vendedor na imprensa [cases §9.7] |
| 7 EUA, UK e SEA × BR | P | Nenhum case de SEA ou UK lido; MtJQmOYKIxQ e Cz8mV3p7dk0 sem transcrição |
| 8 O que o TikTok incentiva | R | Newsroom 2026-06-04 e páginas de campanha |

**Sem fonte oficial ou contestadas:**
- Subsídio de LIVE de 20% a 30% (2025-11): SEM FONTE [cases R2].
- Menor preço de 30 dias e desconto máximo de 30% em campanha: SEM FONTE [cases R6].
- Separação de orgânico no ROI do painel: SEM FONTE [cases R8].
- Afiliados ativos "56×": CONTESTADO, porque a Newsroom diz 46× [cases R12].
- Always Fit sem confirmação independente (Exame, Valor e E-commerce Brasil não acharam nada) [cases §9.2].

**Camadas que faltaram:**
- N4 de cases;
- N5 de ranking BR;
- documentos de empresas abertas que mencionem o TikTok Shop (resultados trimestrais de Natura &Co, Mercado Livre, Sea);
- vagas e perfis de equipe como sinal de estrutura (não buscado).

**Só com PAGO:** Momentum "TikTok Shop in the U.S. & Brazil H1 2026"; Kalodata e FastMoss pagos.

### 2.9 conteudo-video

| # | Estado | O que falta |
|---|---|---|
| 1 Formatos que vendem por categoria | P | Estrutura dominante em 8 de 15 transcrições, sem evidência por categoria no BR |
| 2 Medição de desempenho | P | Definições do painel BR (GMV direto × indireto, abas próprio × afiliado) só em páginas dos EUA [vid §9.6]. Denominador do GPM sem fonte [ferr §9.5] |
| 3 Estrutura e regra × tática | P | Regra lida; tática de praticante |
| 4 Taxa de acerto | S | 90/10 e 5% são de agência dos EUA, sem método |
| 5 Reaproveitamento | P | Prática; "mídia importada" oficial |
| 6 Regras de conteúdo | P | Política BR lida. Faltam pré-verificação de vídeo no BR e música protegida × link [vid A20] |
| 7 Ferramentas para analisar criativo | P | Creative Center e Symphony não documentados (JavaScript) [vid §9.9] |
| 8 Fadiga | S | Sem métrica oficial nem curva [vid §9.7] |

**Sem fonte oficial ou contestadas:**
- Aplicação real da §3.13.1: vídeos sem fala aparecem entre os mais vendidos [vid §9.1]. É o ponto mais alto da frente.
- "Tamanho e formato" como critério de exibição do produto: CONTESTADO [vid A6].
- Duração ideal: nenhum número oficial.
- Lista de proibidos do conteúdo de marca e vitaminas para afiliado do Shop BR: a confirmar [vid §9.4].

**Camadas que faltaram:**
- N4 só de anúncio global (VidMob, System1), nada de Shop;
- N6 BR com painel de vídeo;
- N3 de vídeos de alimento (só legendas de 9 vídeos de café).

**Leitura incompleta:** zZxJbxCDj0Y (93 min, só trechos).

**Só com LOGIN ou MED:**
- "Análise de vídeo" e "Video Diagnosis" no Seller Center;
- distribuição de gasto e receita por criativo na Central de Criativos;
- teste de gancho com corpo igual.

### 2.10 live-commerce

| # | Estado | O que falta |
|---|---|---|
| 1 Métricas do painel e definições | S | Nenhum artigo BR sobre LIVE Analytics ou LIVE Manager (enter room rate, tap-through, GPM de LIVE) [live §9.2] |
| 2 Benchmarks BR | S | Só casos de uma LIVE (AJOAtisYWtM, fel1dZ8-zz0) e faixa de agência (1GDosmkdolA) [live §9.1] |
| 3 Estrutura da LIVE | P | Prática |
| 4 LIVE Flash Sale e LIVE GMV Max | P | Flash Sale lida (2026-07-18). LIVE GMV Max só na página global. Contagem de 5 min CONTESTADA [live R3] |
| 5 LIVE de marca × de afiliado | P | Cases de release e falas |
| 6 Estrutura física e custos | S | Nenhum custo por hora ou por LIVE; os R$ 10 mil são hipótese de agência [live §9.10] |
| 7 Categorias que performam | P | Newsroom qualitativa (cosméticos, cozinha) |
| 8 Práticas da China e do SEA | S | Momentum "Live Commerce in SEA" e Douyin não lidos |

**Sem fonte oficial ou contestadas:**
- Requisito do criador para vender em LIVE no BR: SEM FONTE [live R9].
- "Produto fixado na câmera": SEM FONTE [live R7].
- Subsídio de LIVE em 2026 [live R12].
- Flash de 15% ou de 15 minutos na Black Friday 2026: divergência de imprensa.
- Conversão de 7,8%, 22 min médios, "40% ou 60% do GMV vem de LIVE", GPM ideal de US$ 50 a 150: circulam sem fonte [CONSOLIDADO §3.4].

**Páginas e políticas não lidas:** Política de Jogos de Azar; sorteio do console no BR; leilão no BR; avatar de IA em LIVE [live §9.5 a §9.7].

**Transcrições que faltam (8):** 3rEXumkmN30, UYU_2r4jxps, T-Aj2PFqylc, NjuETySCtoE, 60J9lpXDUwI, eGrRstH4DNs, EcKLRskrTkw, 7QDrA2SJC-8.

**Camadas que faltaram:**
- N3: nenhuma LIVE observada, de qualquer categoria;
- N4 acadêmica de live commerce (literatura chinesa com método);
- N5 de dados de LIVE com filtro BR [live §9.13].

**Só com LOGIN ou MED:** painel de LIVE; GMV por hora contra custo por hora; GMV de afiliados nas semanas com e sem LIVE da marca.

### 2.11 afiliados-criadores

| # | Estado | O que falta |
|---|---|---|
| 1 Colaborações aberta e direcionada | R | kid=6580476438529809 (2025-04-14, pode estar superada). Conflito "30 dias" × "dia seguinte" sem página que resolva [afil §9.2] |
| 2 Base e taxas padrão | R | kid=1517752301717265; kid=3355295847515925 (2026-09-21) |
| 3 Seleção de criadores | P | Prática dos EUA (AD32WdQGXRY) |
| 4 Amostras | P | Regras lidas (2026-02-05, pode estar superada). Custo de amostra que vira conteúdo: nenhum dado BR |
| 5 Métricas de programa | P | 50% a 60% postam uma vez (ferramenta dos EUA, com conflito); 35% a 40% não viram vídeo (agência BR) |
| 6 Requisitos do criador | R | kid=1396756526679824 e kid=924877269190418 (2026-07). A requisição de cadastro está só em imagem (kid=6807244117362448) |
| 7 Parceiros oficiais | P | Guias CAP e TAP de 2025-04. Remuneração e lista de agências BR sem leitura (portal partners/br em JavaScript) [afil §9.5] |
| 8 Incrementalidade | S | Nenhum holdout, cupom por criador ou geo-teste [afil §9.9] |
| 9 Tributação da comissão | P | FAQ de impostos do criador vista só em print (zdNnfmmjNyc); para quem emitir a nota segue em conflito [afil A23] |

**Sem fonte oficial ou contestadas:**
- Teto de outreach por faixa de GMV e "200 novos criadores por dia": SEM FONTE [ferr A16, A17]. A única cota BR é a da CAP (100 por dia).
- Amostra grátis dependente do nível 1 a 10: não aparece [mix A20].
- Exigência de vídeo nos últimos 180 dias: superada pela página de 2026-07 [afil A15/A16].
- Retenção de IR na fonte: "se aplicável", sem regra [reg §9.6].

**Camadas que faltaram:** N6 BR de agência ou MCN com painel da Central de Afiliados; N4 de programa de afiliados; N1 da Central do Criador BR. Creator Marketplace e TikTok One: sem evidência no Shop [afil §9.12].

**Só com LOGIN ou MED:**
- Afiliados > Colaboração direcionada > Ver regras (teto de convites);
- data efetiva de uma redução de taxa no extrato;
- coorte de amostras (custo e GMV por amostra);
- taxa de aceite por faixa de comissão.

### 2.12 conta-onboarding

| # | Estado | O que falta |
|---|---|---|
| 1 Requisitos de cadastro | P | kid=1721569656112912 (2025-12-18). FAQ de 2024-12 tem fluxo com CPF. Nenhuma página de 2026 [onb R9] |
| 2 Período de experiência | R | kid=1444948507379472 (2026-04-02), tabela lida no navegador |
| 3 Incentivos de loja nova | P | Cobertura da taxa fixa sob o 0%; frete grátis de loja nova sem página [onb §9.3, §9.4] |
| 4 Contas oficial e de marketing | R | Página global e BR (2026-04-02). Comissão para a conta de marketing: sem resposta [marca §9.3] |
| 5 ERPs e integrações | P | Sem lista oficial (Service Market BR); escopo de Magis5 e Ideris não detalhado [onb §9.9] |
| 6 Categorias com aprovação | P | Processo lido; prazos só em relatos divergentes [onb §9.13] |
| 7 Erros de lançamento | P | Oficial e prática, sem frequência |
| 8 Primeiros 90 dias | P | Consenso de ordem; números divergentes |

**Sem fonte oficial ou contestadas:**
- Emissor nativo de NF-e (regimes aceitos, XML): SEM FONTE [onb R10].
- "Vendedor individual" num país que exige CNPJ: MEI ou EI? [onb §9.2].
- Selo de loja oficial ou verificado no BR: só EUA (2026-01-22) [onb §9.10].
- Página oficial de vínculo da conta oficial: não lida [onb §9.8].

**Camadas que faltaram:** N1 de cadastro em 2026 (home em JavaScript); N4 de sobrevivência de loja nova, tempo até a 1ª venda e taxa de aprovação (inexistente) [onb §9.12].

**Só com LOGIN ou MED:** fluxo de cadastro real; tempo de aprovação; dias até sair do período de experiência.

### 2.13 conta-de-marca-conteudo

| # | Estado | O que falta |
|---|---|---|
| 1 Uso da conta e divisão de GMV | P | Divisão BR inexistente; EUA (alimentos, 17,6%) e Europa (7,3% a 34,3%) via Kalodata [marca §9.1] |
| 2 Cadência e equipe | P | Só Natura tem número [marca §9.8] |
| 3 Funcionários e consultoras como criadores | R | Cases (Natura, Granado, MAC, Maxfen) |
| 4 Super Brand Day | S | Elegibilidade, custo, cofinanciamento e duração sem página [marca §9.2] |
| 5 Proteção de preço e PI | P | IP Protection Centre não confirmado no BR [marca §9.6] |
| 6 Efeito fora do TikTok | S | Relatório de transbordamento e Off-site Performance Analysis sem disponibilidade BR nem método [marca §9.7] |
| 7 Branding × conversão | P | Prática |
| 8 Rótulo de conteúdo próprio impulsionado | S | Nem a política de conteúdo de marca nem a do Shop trata disso [marca §9.4] |

**Sem fonte oficial ou contestadas:**
- Super Brand Day "por convite" (ver §1.3) [marca R5].
- Guia CONAR 2026: só resumos, que divergem na vigência (13/5 ou 1/6) [marca R12].
- "+228%" e "3×" da Natura sem base [marca §9.9].

**Camadas que faltaram:**
- N1 de PI e de "Práticas recomendadas para conteúdo promocional";
- N2 do PDF do CONAR;
- N5 de mix de GMV BR;
- N3 das contas das marcas líderes BR (vídeos por semana, horas de LIVE), possível em perfil público.

**Só com LOGIN ou MED:** seis cortes do Data Compass; teste de pausa da conta própria; geo-teste de halo.

### 2.14 dados-mercado-br

| # | Estado | O que falta |
|---|---|---|
| 1 Tamanho | P | Faixa Momentum/Tabcut × EchoTik (2× de diferença), sem método publicado [dados §9.3] |
| 2 Comparação com ML, Shopee e Amazon | P | GMV absoluto de ML e Shopee no BR não aberto; Amazon, Magalu e Shein sem número [dados §9.4] |
| 3 Composição por categoria e canal | P | Agosto de 2025 (Tabcut); 2026 só no relatório pago [dados §9.5] |
| 4 Perfil do comprador | P | Opinion Box (n = 1.066) lido via blog; sem recortes demográficos [dados §9.7] |
| 5 Marcos | R | Newsroom 2025-05-08, 2025-11-06, 2025-12-02, 2026-06-04; tarifa 2026-06-12 |
| 6 BR × EUA e SEA | P | EUA via Momentum; SEA pouco |
| 7 Divergências | R | Registradas e reportadas como faixa |

**Sem fonte oficial:**
- 134 milhões de usuários [dados A4];
- "15 milhões de sellers" [dados A22];
- 12º ou 14º país;
- ticket médio de R$ 47;
- "3º maior marketplace";
- histórico de R$ 2 por item abaixo de R$ 79 [dados A16].

Pesquisa Optimiza sem amostra [dados §9.8]. Relatório LCA (PDF de mais de 10 MB) não aberto [dados §9.13].

**Camadas que faltaram:**
- N4: Momentum pago, NIQ Ebit Webshoppers, ABComm;
- N2 e N4 de concorrentes: 10-Q do Mercado Livre e deck da Sea;
- Opinion Box original.

**Só com PAGO:** Momentum BR H1 2026; eMarketer (403).

### 2.15 ferramentas-analise

| # | Estado | O que falta |
|---|---|---|
| 1 Cobertura do BR e desde quando | S | Nenhuma página oficial de ferramenta lista o Brasil; inferência por telas de tutorial (2025-11 em diante) [ferr §9.1] |
| 2 Método e erro | S | Só a Cruva declara erro (±30%). Nenhum teste independente de estimativa × Seller Center [ferr §9.2] |
| 3 Fluxo das agências | R | Prática consistente entre fontes |
| 4 Definições de métrica | P | Denominador do GPM no Seller Center BR sem fonte [ferr §9.5] |
| 5 Dados nativos | P | Data Compass completo em pt-BR não lido (página de 2025-02, global); novos × recorrentes por criador [ferr §9.3] |
| 6 Gestão de afiliados e teto | P | Teto BR sem fonte [ferr A16, A17] |
| 7 Conflitos de interesse | R | Registrados |
| 8 Preço e histórico | P | Preços vêm de concorrente (Hubfluence); histórico da FastMoss diverge (90 a 1.500 dias) [ferr §9.7] |

**Sem fonte oficial ou contestadas:**
- "Número de destaque do painel a preço de tabela": CONTESTADO [ferr A33].
- Tockfy, Viral e outras ferramentas BR: não abertas; legitimidade da revenda de acesso não verificada [ferr §9.8].
- Cobertura de alimento (categoria só para convidados) nas ferramentas [ferr §9.10].

**Transcrições que faltam:** Q2m0gPCQxAg, U3-7SyOleMM.

**Só com LOGIN, MED ou PAGO:** comparação de estimativa contra Seller Center de lojas que aceitem abrir o painel (N3/N6); lupa do painel BR.

### 2.16 regulatorio-fiscal

| # | Estado | O que falta |
|---|---|---|
| 1 CDC e decreto de e-commerce | P | Textos do planalto falharam duas vezes; sem decisão de Procon ou tribunal sobre LIVE [reg §9.3] |
| 2 Publicidade de criador | P | Rótulo do TikTok lido; Guia CONAR 2026 só via imprensa [reg §9.2] |
| 3 Sanitário | P | IN 281/2024 lida no DOU. Faltam RDC 429/2020 e notificação × registro de cosmético [reg §9.8]. Nenhuma fiscalização dirigida ao TikTok Shop [reg §9.11] |
| 4 Tributação | P | DIFAL e ICMS interestadual sem fonte [reg §9.5]; retenção de IR [reg §9.6]; afiliado MEI (CNAE 7490-1/04) sem fonte primária [reg §9.7] |
| 5 Importação e cross-border | R | Não há vendedor cross-border; pagamentos domésticos |
| 6 PI e falsificação | P | Retenções lidas; canal de PI BR não confirmado |
| 7 Sorteio em LIVE | P | Política proíbe jogos de azar; norma vigente da SPA/MF e status da Portaria 422/2013 a confirmar [reg §9.12] |
| 8 Mudanças em discussão | P | LC 214/2025 e LC 227/2026 lidas via terceiro; substituição tributária voluntária e split payment no Simples [reg §9.13] |

**Sem fonte oficial ou contestadas:**
- Repasse de 7/3/31 dias × 35 a 40 dias: os Termos (kid=3268441302615809, 155 mil caracteres) só foram lidos em parte [reg A10/A11].
- Reembolso sem devolução até R$ 25 "automático": CONTESTADO; vale "pode ser ativado" [reg A14/A15].
- "Chance de ganhar prêmio" como proibição própria: CONTESTADO [reg A18/A19].
- Afiliado PJ emite nota para cada vendedor: SEM FONTE [reg A8].

**Camadas que faltaram:** N2 primário (planalto, Receita/CGSN, CONAR, Anvisa, SPA/MF, DOU); N6 de contadores com data e caso.

**Só com MED:** pedido com cupom da plataforma e conferência da comissão no demonstrativo; caminho da nota de amostra (CFOP 5911/6911) num caso real.

---

## 3. Itens transversais

### 3.1 Regras BR anteriores a 2026-04-15 que precisam de releitura

Todas estão no CONSOLIDADO como vigentes, mas com data antiga. Reler a versão atual de cada uma (WEB; NAV se vier vazia).

| kid | Tema | Data da página |
|---|---|---|
| 6580476438529809 | Colaborações (limites de convite; edição "no dia seguinte") | 2025-04-14 |
| 6810747971798800; 6817362679023376 | CAP/MCN; convites de colaboração | 2025-04 |
| 6825383530710785 | Vitrine do criador (2.000 produtos, selos) | 2025-04-14 |
| 6880013740476161 | GMV × Liquidação | 2025-04-16 |
| 3951967941150480 | Amostra reembolsável | 2025-07-22 |
| 2583022047233809 | Metas de chat | 2025-09-30 |
| 3309653722089232 | OVL | 2025-10-27 |
| 1487157475673872; 4896169624913680 | NF-e, amostra, emissor | 2025-05; 2025-09 |
| 1721569656112912 | Cadastro (só CNPJ, MEI aceito) | 2025-12-18 |
| 6907568440706832 | Suplemento por convite | 2025-12-03 |
| 6821109446018832 | Criadores confiáveis | 2025-12-30 |
| 974093010454289 | CHR do criador | 2026-01-23 |
| 6589441682917136 | Amostra grátis | 2026-02-05 |
| 2850789359355649 | Regras de comissão (redução em 30 dias) | 2026-02-10 |
| 2569565069149953 | Cupom cofinanciado | 2026-02-10 |
| 3027449152374544 | Benefícios de campanha (SPS 3,5) | 2026-02-10 |
| 24428156389121 | Fatura fiscal | 2026-02-10 |
| 3351782382814993 | Preço-limite de campanha | 2026-02-11 |
| 3039191651075856; 1984591137818385 | Contas (proibido transferir; reverificação) | 2026-02/03 |
| 1442971111884545 | Modelos de envio | 2026-03-06 |
| 3026645972993808 | Recurso logístico | 2026-03-06 |
| 3321767214286609 | LDR | 2026-03 |
| 1074592103220993 | Webinar LATAM do SPS | 2026-03-26 |

### 3.2 Divergências entre páginas oficiais BR (não resolvidas)

1. Devolução de alimento: kid=2578485181925121 (2026-04-14) × kid=894339073115921 (2026-09-24).
2. Suplemento por convite: kid=6907568440706832 (2025-12-03) × kid=6504327061473040 (2026-04-30).
3. Redução de comissão: kid=2850789359355649 e kid=5955311610251025 (30 dias) × kid=6580476438529809 (dia seguinte).
4. Repasse: kid=1442971112769281 (7/3/31 dias) × Termos kid=3268441302615809 (35 a 40 dias).
5. Base da comissão: kid=1517752301717265 × kid=2850789359355649 (redação diferente).
6. Rótulo de campanha: SPS 3,0 (kid=2996214162966289) × 3,5 (kid=3027449152374544). Podem medir coisas diferentes (elegibilidade × rótulo).
7. LIVE Flash Sale: a mesma página alterna "≤" e "<" no preço de 14 dias (kid=5696139560355601).
8. Cadastro com CPF: FAQ de 2024-12 (kid=3636433944823553) × página de 2025-12 (kid=1721569656112912).

### 3.3 Vídeos citados e não transcritos (24)

- **ads (12):** ciyEKKJPT8c, VqaNndB_vfE, 3XOMFCGbKmE, RVIp1lY0CJY, S4xOd0GwOb4, BimhUTun6vQ, QniRGmboan0, emyPP8gn6pQ, EQJ3UpzBWAw, muQ0ALeY0Mo, VGNbKxg9VxY, DLWchGwGIZU.
- **live (8):** 3rEXumkmN30, UYU_2r4jxps, T-Aj2PFqylc, NjuETySCtoE, 60J9lpXDUwI, eGrRstH4DNs, EcKLRskrTkw, 7QDrA2SJC-8.
- **cases (2):** MtJQmOYKIxQ (Malásia), Cz8mV3p7dk0 (Reino Unido).
- **ferramentas (2):** Q2m0gPCQxAg, U3-7SyOleMM.

Conferido em `transcricoes/` em 2026-10-16: nenhum dos 24 tem arquivo. Os afiliados listados como "não lidos" em [afil §9.11] (8WJV5i3K8U0, OPdBYdwYEso, JDRXXF3wHm8, 3yYNNuHhdrs, ZOOZitZ1Duw, 1GDosmkdolA) já estão transcritos e só precisam de leitura.

---

## 4. O que só se resolve com acesso logado ou medição própria

Nenhum agente desta pesquisa entra no Seller Center. Os itens abaixo ficam registrados como **fora de alcance** e não devem ser "fechados" com prática de terceiro.

### 4.1 Seller Center, Central de Afiliados ou Ads Manager (LOGIN)

1. Tarifa "por item": unidade, SKU ou kit (extrato de Finanças) [pre A25].
2. Isenção de 0% da loja nova: cobre a taxa fixa e o SFP? [pre A4].
3. Documentos e prazos do Centro de qualificação por subcategoria de alimento; como uma loja sem SPS cumpre "SPS > 4" [onb §9.5].
4. Pesos do SPS e benchmarks de 1 e 4 pontos da categoria [rep §9.1, §9.2].
5. Dedução de pontos por tipo de violação; recuperação por 300 pedidos [rep §9.4; reg §9.9].
6. Proteção de ROI (limiares), GMV Max Pro, mínimo de boost em BRL, definição do ROI na lupa [ads §9.1].
7. ROI que a plataforma usa ao criar anúncio por CPV, campanha a campanha [pre A35].
8. Teto de convites a criadores por faixa de GMV [ferr A16].
9. Regulamento e divisão de custo da Black Friday 2026; painel de missões [pre A19; mix A22].
10. Requisitos e custo do Super Brand Day [marca §9.2].
11. Fluxo de devolução de alimento como aparece para a categoria [rep R12].
12. Denominador do GPM e número de destaque do painel [ferr §9.5; ferr A33].
13. Seis cortes do Data Compass (Ads × afiliado × nenhum) e novos × recorrentes por criador [ferr §9.3].
14. Aba "Melhorar qualidade do anúncio" e análise de aba Loja e busca no BR [rank §9.2].
15. Data de liquidação real (7/3/31 × 35 a 40) [reg A10].

### 4.2 Medição própria (MED)

| Pergunta | Desenho citado nas fontes [met §6.3; CONSOLIDADO §4] |
|---|---|
| Incrementalidade do GMV Max | Holdout de produto ou pausa (switchback) de poucos dias; olhar o GMV total da loja, não o ROI do painel |
| Meta de lançamento (baixa × 1,5 a 2× o equilíbrio) | Produtos de margem parecida em campanhas separadas por 14 dias |
| Vídeo de ROI baixo (excluir × manter) | Holdout de criativos |
| Incrementalidade de afiliado | Cupom por criador, novos × recorrentes, holdout |
| Amostra em massa × seleção | Custo por amostra que virou conteúdo e GMV por amostra, por coorte |
| LIVE própria × só afiliados | GMV por hora contra custo por hora; GMV de afiliados com e sem LIVE da marca |
| Halo para outros canais | Geo-experimento ou pausa com dado próprio de site e marketplaces |
| Comissão aceitável | Taxa de aceite e de postagem por faixa de comissão |
| Violação reduz alcance | Impressões antes e depois de uma medida, com controle de sazonalidade |
| Precisão das ferramentas N5 | Estimativa da ferramenta contra receita do Seller Center de lojas que aceitem abrir o painel |

### 4.3 Pago (PAGO)

- Momentum Works, "TikTok Shop in Brazil H1 2026" (US$ 52,95) e o pacote EUA + BR.
- Kalodata, FastMoss e EchoTik com filtro Brasil.
- eMarketer (403).

---

## 5. Próxima rodada: lista priorizada (o que buscar e onde)

A rodada 2 deve ser cerca de **2× mais ampla** que a 1 em fontes e camadas, sem repetir o que já está CONFIRMADO. Mantém as regras do protocolo: sem login, conteúdo como dado, no máximo 15 WebSearch por agente, WebFetch em URL direta.

### 5.1 Metas de cobertura (rodada 1 → rodada 2)

| Camada | Rodada 1 | Meta da rodada 2 |
|---|---|---|
| N1 BR (páginas da Academy, Newsroom, canais oficiais) | cerca de 90 páginas | +60 páginas, com o índice da Academy varrido por agente de navegador |
| N2 (texto primário de lei e regulador) | 12 achados, a maioria via terceiro | Texto primário de CDC, Decreto 7.962, LC 214, CGSN, CONAR 2026, RDC 429, Portaria 570, SPA/MF |
| N3 (observação direta, sem login) | 1 passada, café, logado | 3 ou mais passadas em dias e horários diferentes, café + 4 categorias líderes, LIVEs públicas, e a Black Friday 2026 |
| N4 (estudo com método) | Momentum via imprensa, Opinion Box via blog | Literatura acadêmica de live e social commerce; relatórios originais; resultados trimestrais de empresas abertas |
| N5 (ferramentas) | nenhuma faixa BR | Páginas públicas de ranking com filtro BR (sem login), como faixa e com data |
| Vídeos selecionados | 239 (≈40% BR; 4 SEA/UK; 15 de alimento) | 480, com ≥50% BR, ≥40 de alimento e bebida, ≥25 de SEA, UK e China, ≥30 de praticante BR mostrando painel |
| Social (TikTok, Instagram) | 100 posts, 44 transcrições | 200 posts, com foco em vendedores e afiliados BR de alimento e em canais oficiais |

### 5.2 P1: muda leitura de custo, regra ou acesso

| # | O que buscar | Onde | Modo |
|---|---|---|---|
| 1 | **Observação da Black Friday 2026 (27/10 a 12/12), com janela que se fecha.** Preço riscado, cupons, flash de LIVE, selo e "vendidos", em séries de dias, sem login | `shop.tiktok.com/br` por categoria (Café `/br/c/coffee/700612` e líderes); Newsroom pt-BR; imprensa de 2026-10-27 em diante | NAV, repetido |
| 2 | Varredura do índice da Academy BR: GMV Max, Proteção de ROI, LIVE Analytics/Gerenciador de LIVE, Oferta relâmpago do vendedor, Cupom do vendedor, Desconto de produto, Pacote/combo, Empilhamento de preços, Super Brand Day, Black Friday 2026, Envio pelo vendedor, Transportadoras, Qualidade do anúncio, Impostos do criador, Emissor de NF-e, Requisitos de cadastro | `seller-br.tiktok.com/university` (busca interna, exige JavaScript) | NAV |
| 3 | Páginas que vieram vazias ou não foram lidas | kid=8270844531967761, 3989684486358785, 7204971943560976, 8994711168665361, 2324329879832321, 2583991870097169, 6843306600302353, 6160913167009537, 6807244117362448 (imagem) | NAV |
| 4 | Termos de Serviço do Vendedor BR na íntegra: repasse de 35 a 40 dias × 7/3/31, publicidade, responsabilidade | kid=3268441302615809 (155 mil caracteres; ler em blocos) | WEB/NAV |
| 5 | Releitura das 23 regras anteriores a 2026-04-15 (§3.1) | Academy BR, pelos kids listados | WEB |
| 6 | Divergências entre páginas oficiais (§3.2): achar versão mais nova ou página que arbitre | Academy BR; Central de Ajuda do Vendedor | WEB/NAV |
| 7 | Parâmetros oficiais de ranqueamento | `tiktok.com/legal/page/eea/tiktok-shop-terms-of-service/en` (exigência legal da UE; marcar "UE"); `tiktok.com/transparency/pt-br/recommendation-system`; `tiktok.com/support/faq_detail?id=7655285288050104852` | NAV |
| 8 | Página BR de GMV Max ou descontinuação de Shop Ads no BR; vigência BR de LIVE GMV Max | Academy BR; blog `ads.tiktok.com/business/pt-BR/blog`; vídeos @sellwithtiktokshop_br | NAV/WEB |
| 9 | Nome e regra dos pontos do vendedor BR ("AHR" ou outro) | kid=1444948508641040; kid=7734094290093831 | WEB |
| 10 | Super Brand Day no BR: existe página? "Por convite" tem fonte? | Academy BR; Newsroom pt-BR; releases de Riachuelo e Granado | NAV/WEB |

### 5.3 P2: muda tática ou a leitura de prática

| # | O que buscar | Onde | Modo |
|---|---|---|---|
| 11 | Faixas N5 com filtro Brasil: top lojas por categoria, GMV de 30 dias de alimentos e café, nº de criadores por produto, preço médio. Registrar como faixa, com data e ferramenta, nunca somar | Páginas públicas de ranking de FastMoss, Kalodata, EchoTik, Tabcut e Shoplus abertas sem login (Kalodata dá 403 no WebFetch: tentar por navegador) | NAV |
| 12 | Transcrever os 24 vídeos de §3.3, a começar por LIVE (8) e ads BR (VqaNndB_vfE, 3XOMFCGbKmE, RVIp1lY0CJY) | YouTube, pelas ferramentas de `ferramentas/` (pausa de 6 s; erro 429 = repetir mais tarde) | WEB |
| 13 | Praticantes BR mostrando painel (N6): Seller Center, Data Compass, painel GMV Max, Central de Afiliados, painel de LIVE, saúde da conta | YouTube em pt-BR com consultas como "Bússola de Dados", "painel GMV Max", "análise de LIVE TikTok Shop", "saúde da conta TikTok Shop"; webinars LATAM na Academy (modelo: kid=1074592103220993) | WEB |
| 14 | Alimentos e bebidas no BR: vendedores e afiliados de café, snacks e bebidas em vídeo, LIVE e post; marcas convidadas (BIS, SEDE, Desinchá, Guday, Power Focus) | TikTok e Instagram públicos; YouTube pt-BR; imprensa (Meio & Mensagem, Mercado & Consumo, Consumidor Moderno) | WEB/NAV |
| 15 | LIVEs públicas observadas (N3): duração, nº de produtos, ciclo de oferta, uso de Flash Sale, presença de operador. Se o web exigir login, registrar e seguir | `tiktok.com/@<loja>/live` de lojas BR de beleza, cozinha e alimento | NAV |
| 16 | Momentum Works e Tabcut, posts gratuitos sobre o BR em 2026 (mix de canal, categorias, preço médio) | `thelowdown.momentum.asia`; `momentum.asia/insights`; imprensa que cita o relatório H1 2026 | WEB |
| 17 | Cases fora do BR: SEA (Malásia, Indonésia, Tailândia), UK e China (Douyin), com país marcado e método | MtJQmOYKIxQ, Cz8mV3p7dk0; Momentum "Live Commerce in Southeast Asia 2026"; blog TikTok for Business UK (en-GB); literatura sobre Douyin | WEB |
| 18 | N4 acadêmico: conversão em live commerce, efeito do apresentador, incrementalidade de social commerce | Google Scholar, SSRN, periódicos de marketing (ler resumo e método; registrar amostra e país) | WEB |
| 19 | Reclamação e pós-venda: perfil do TikTok Shop no Reclame Aqui e no consumidor.gov.br (índices, motivos) | reclameaqui.com.br (403 no WebFetch; tentar por navegador); consumidor.gov.br | NAV |
| 20 | Placar de criador ligado às avaliações (EUA) e equivalente BR | ecomcrew (EUA); Academy BR (Classificação de integridade do criador) | WEB |

### 5.4 P3: completa o mapa

| # | O que buscar | Onde | Modo |
|---|---|---|---|
| 21 | N2 primário: CDC art. 49 e Decreto 7.962/2013; LC 214/2025 (responsabilidade de plataforma); Resolução CGSN 140, Anexo XI (ocupações do MEI); Guia CONAR 2026 (PDF); RDC 429/2020 e IN 75/2020; Portaria SDA 570/2022; norma vigente de sorteio da SPA/MF | planalto.gov.br; in.gov.br; gov.br/receitafederal; conar.org.br; gov.br/anvisa; gov.br/agricultura; gov.br/fazenda | WEB |
| 22 | Fiscalização e decisões que citam TikTok Shop | Busca no DOU; portal da Anvisa; decisões do CONAR; Procons estaduais; Senacon | WEB |
| 23 | Empresas abertas que citam TikTok Shop em resultado ou teleconferência (Natura &Co, Mercado Livre, Sea, Magalu) | Sites de RI, releases do 3º tri de 2026 (fim de outubro e novembro) | WEB |
| 24 | ERPs e integradores BR: lista oficial do Service Market e escopo de Bling, Tiny/Olist, UpSeller, Magis5, Anymarket, Ideris | Página de parceiros `seller-br.tiktok.com/partners/br` (NAV); centrais de ajuda dos ERPs | NAV/WEB |
| 25 | Estrutura de equipe dos líderes: vagas de "TikTok Shop", "live commerce" e "afiliados" em marcas BR, como sinal [OBS] | LinkedIn Vagas e Gupy públicos, sem login (se exigir, registrar) | NAV |
| 26 | Cadência das contas oficiais das marcas líderes BR: vídeos por semana e LIVEs, contados no perfil público | Perfis públicos (Natura, Boticário, Granado, Riachuelo, Moderna, BigHome) | NAV |
| 27 | Opinion Box original (recortes de idade, renda e região) e NIQ Ebit Webshoppers | Sites dos institutos | WEB |
| 28 | Creative Center com filtro BR (hashtags, palavras, Top Ads de Shop) | `ads.tiktok.com/business/creativecenter` | NAV |

### 5.5 Como dividir a rodada 2

- **Agentes web** (WebFetch primeiro, WebSearch só para achar URL): P1 itens 4, 5, 6 e 9; P2 itens 12, 13, 16, 17, 18 e 20; P3 itens 21 a 23 e 27.
- **Agente de navegador (sem login):** P1 itens 1, 2, 3, 7, 8 e 10; P2 itens 11, 15 e 19; P3 itens 24 a 26 e 28.
- **Verificação:** cada afirmação nova de regra BR passa pela mesma tabela de status (CONFIRMADA, PARCIAL, CONTESTADA, SEM FONTE OFICIAL) e entra em `verificacao/resultado.tsv` com trecho literal de até 15 palavras.
- **Critério de pronto da rodada 2:** cada pergunta do protocolo sobe de S para P, ou de P para R, ou ganha a marca "só com LOGIN/MED/PAGO", com o motivo escrito.
