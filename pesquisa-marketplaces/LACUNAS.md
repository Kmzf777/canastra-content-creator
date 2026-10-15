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

### 1.0 Camadas por frente

| Frente | Oficial | Dados | Obs. | Social |
|---|---|---|---|---|
| ads | OK (developers; 8 de 12 conf.) | ausente (ACOS 5–25% sem método) | fraca (sem "Patrocinado") | OK |
| preco-promocao | fraca na verificação (403; 1 de 12 conf.), mas páginas lidas por outras frentes; N2 OK | ausente | parcial (preço em camadas, só café) | OK |
| logistica-estoque | parcial (Ajuda por JS; 5 de 12 conf.) | ausente | parcial (FULL só nos cards) | OK |
| ranqueamento-anuncio | OK (9 de 12 conf.) | ausente | parcial | OK |
| produto-mix | OK (10 de 12 conf.) | fraca (Nubimetrics sem método nem data) | parcial | OK |
| reputacao-atendimento | OK (10 de 12 conf.) | ausente | parcial (só a medalha dos líderes) | parcial |
| alimentos-marca-propria | OK (11 de 12 conf.); N2 Anvisa só via imprensa | ausente | OK em café | parcial |
| cases-grandes | fraca (403; só o 8-K relido) | fraca (XP, Santander e Avenue via imprensa) | parcial | OK |

### 1.1 ads
**Perguntas do protocolo**
- Q1 **P**: os requisitos de Display self-service e do canal Top Brands não são públicos [ads §9].
- Q2 **P**: Ad Rank = Ad Score × CPC está escrito só para Brand Ads. Para Product Ads, a fórmula, o "segundo preço" e o CPC derivado do ROAS vêm só do webinar JzejZyVeauE, não reassistido [ads A4, rank A30].
- Q5 **S**: não há incrementalidade. O Product Ads não expõe termo de busca, então a fatia do gasto em termos da própria marca não é mensurável [ads §9].
- Q6 **S** em fonte oficial: só praticantes e um suposto "score de TACOS" [ads A33].
- Q7 **S** para o BR: só ACOS de 5% a 25% sem método [ads A37] e Amazon EUA [ads A38].
- Q9 **S**: não há integração confirmada de Pacvue, Flywheel, Perpetua ou Skai com o Mercado Ads. A participação de Ads por concorrente no painel Concorrência não foi verificada.

**Sem fonte oficial ou contestado**
- Faixa de ROAS objetivo de 1x a 35x [ads A2]: o consolidado a usa como benchmark [OFICIAL], mas não foi reconferida.
- Orçamento compartilhado e cobrança pós-paga [ads A15].
- Janela de atribuição: 14 dias na API contra 15 no webinar [ads A10].
- Requisitos do Product Ads: a nota oficial contesta o webinar (15 dias de conta, fatura vencida) [rep A16, CONTESTADA].
- Ads/GMV do MELI em cerca de 2,6%: só fonte secundária.
- Fase de aprendizado oficial: não documentada.
- Quem recebe a venda quando o clique pago cai num catálogo ganho por outro vendedor: não documentado.

### 1.2 preco-promocao
**Perguntas**
- Q1 **P**: a tarifa percentual exata por categoria (Alimentos, café) não foi lida. A tabela de tarifa competitiva (ajuda/51251: −3 a −5 p.p. entre R$150 e R$700) e o reajuste de envio de +1,6% em 24/08/2026 não foram reconferidos [pre A7, A8].
- Q2 **P**: não há regra oficial de paridade. A punição por preço externo desde out/2025 vem só de imprensa [cases A3]. O índice de competitividade citado na carta 2T26 não tem fórmula.
- Q4 **S**: não há índice par a par ou ponderado, % de buy box de portfólio nem preço contra a mediana da 1ª página praticados no BR.
- Q5 **P**: os 12 tipos de promoção, as cofinanciadas e quem paga cada parte vêm de developers não reconferido [pre A14–A16, R10–R12].
- Q6 **S**: nada separa o subsídio do ML do desconto do vendedor.
- Q8 **P**: não há calendário oficial de 2026 com prazos de adesão. A data da Black Friday é cálculo [pre §9.6].

**Sem fonte oficial ou contestado**
- Desconto de frete por reputação: 50% (página atual) contra 70% (vídeo de maio) [pre A5; rep A15].
- Custo fixo abaixo de R$79: a página atual mostra só degraus de envio; blogs e um vídeo de maio falam em corte de R$12,50 [mix R12, SEM FONTE].
- Automação de preços (INT/INT_EXT, piso, 60 dias) [pre A23]: não reconferida.
- Duração e desconto mínimo de relâmpago e oferta do dia: só praticantes.
- Legalidade de "de/por" e a suposta regra de 60 dias antes da Black Friday (CDC, Senacon): não verificadas.

### 1.3 logistica-estoque
**Perguntas**
- Q2 **P**: custos oficiais de retirada e descarte por m³ (ajuda/16645), coleta ao Full e armazenagem diária (ajuda/24253, que redirecionou) não foram lidos.
- Q3 **S** quantitativo: o efeito do Full ou do frete na exposição tem só "2x", "+150%" e "5x", sem método [log A17].
- Q7 **P**: o anúncio pausa sem estoque (conf.), mas o tempo para recuperar a posição não foi medido.
- Q8 **P**: procedimento de validade dentro do Full (alerta, descarte, FEFO) não documentado; páginas do Inmetro e do MAPA por categoria não lidas.

**Sem fonte oficial ou contestado**
- Restrição de extragrandes de 20/05/2026 (20 kg, 80 cm, 125 L, preço mínimo) [log R6]: a página oficial ainda fala em mais de 18 kg e até 25 kg.
- Estoque compartilhado: reputação verde, experiência 75, exclusão de alimentos e de itens com validade [log R9; ajuda 42158/42159 não carregaram].
- Lado de até 120 cm, soma de até 260 cm e proibição de itens com controle de temperatura [log R5]. A frente de alimentos confirmou a proibição na ajuda/5200 [alim A2]: ver reconciliação.
- Penetração do Full só no Brasil: o 8-K dá 55% regional.

### 1.4 ranqueamento-anuncio
**Perguntas**
- Q1 **P**: não há fórmula nem pesos.
- Q7 **P**: não há página oficial sobre incentivo a avaliações (cartão na embalagem, brinde) [rank §9].
- Q8 **S**: o próprio ML "não informa prazo" para um anúncio ganhar posição.

**Sem fonte oficial ou contestado**
- "Trocar título ou fotos faz o anúncio ser lido como novo" [rank A20]: só webinar MFYKfOYs0iE. O consolidado trata como prática dos melhores.
- Especificações de Clips (duração, moderação em 48 h, logo) [rank A23]: sem página escrita.
- Teste de +10% a 15% de conversão com clipe na 1ª posição: único número com desenho experimental declarado, mas só falado em webinar, sem amostra nem período.
- Janela da experiência de compra: 60/365 dias contra 180 dias, divergência oficial interna [rank A9].
- Frase "catálogo sempre primeiro" contra `visit_share` mínimo para quem perde a buy box [rank A2].
- Lista de categorias que exigem fundo branco: não publicada.
- A descrição indexa na busca? [soc S20–S21]: sem fonte.

### 1.5 produto-mix
**Perguntas**
- Q3 **P**: não há CR3, CR5 nem HHI para nenhuma categoria do ML-BR.
- Q4 **P**: não há dado de sortimento ML × Shopee dos mesmos vendedores.
- Q6 **S**: não há equivalente público a Market Basket ou Traffic Graph.
- Q7 **P**: share of search no Google sem evidência.

**Sem fonte oficial ou contestado**
- "Sem entrega diferente por variante" no modelo User Products [mix R3, CONTESTADA em parte].
- Conteúdo atual da aba "Oportunidades" (medalhas, sazonalidade, top 100): precisa de checagem logada, que fica fora do escopo sem login.
- Requisito de acesso ao detalhe do painel: R$300 contra R$1.500 a R$2.000 em 60 dias (estado-da-arte §2.1, pode estar superada).
- Canibalização entre kit e avulso: nenhuma medição.

### 1.6 reputacao-atendimento
**Perguntas**
- Q2 **P**: o efeito da medalha na exposição tem a afirmação oficial contra um praticante que não viu efeito [rep D2].
- Q3 **P**: o número de recursos na contestação vem de N7.
- Q8 **P**: há divergências internas da Ajuda sobre o Full (retirada de não aptos em 20 ou 30 dias; contestação em 60 dias corridos ou úteis).

**Sem fonte oficial ou contestado**
- Faixas de 365 dias para amarelo, laranja e vermelho: só via Terazi.
- Benefício de Reputação (R$75 a R$250 mil, 120 dias): só terceiros. Não se sabe se coexiste com a Reputação Protegida.
- Corte da janela de reputação: 101 (oficial, sem data) contra 68 (vídeo, "desde 10/09/2026") contra 60 (developers 2025) [rep A2; cases A26].
- Benchmark de reclamação, devolução e tempo de resposta por categoria: ausente.

### 1.7 alimentos-marca-propria
**Perguntas**
- Q2 **P**: o comunicado oficial gov.br da inspeção da Anvisa em Cajamar (18/03/2026) não foi lido; o dado vem de imprensa. Não se procuraram inspeções do MAPA em CDs.
- Q3 **S**: o case 3 Corações/Lett (2025) que o protocolo cita não foi encontrado nem buscado. Não há share of search, content score ou ruptura com case brasileiro.
- Q4 **P**: não há assinatura no ML (confirmado por ausência). Não há dado público do botão de recompra.
- Q8 **P**: não há teste de formato (multipack contra unitário).
- Q9 **S**: a organização 1P/3P de Nestlé, Ambev, Unilever e 3 Corações em 2026 tem só o caso Nestlé/Brasil CT, de 2019.

**Sem fonte oficial ou contestado**
- Convivência da ajuda/23329 (Full fechado a novos autorizados de Supermercado) com a nota que coloca automaticamente em Supermercado quem tem estoque no Full [alim §2.4]. O consolidado a chama de ponto mais crítico; não há leitura que concilie.
- Lista e critério dos "produtos selecionados" do Full Super (envio de R$1,60 contra R$2,40) e a data de 24/08/2026: não lidos.
- Classe do INPI exigida para loja oficial (35 ou classe do produto): sem regra.
- Enquadramento do café na IN 281/2024: não confirmado no DOU.
- Norma de exibição do rótulo no anúncio online: não encontrada.

### 1.8 cases-grandes
**Perguntas**
- Q1 **S**: não há ranking público. O painel Concorrência exige login, e as ferramentas N5 não tiveram relatório de 2026 encontrado.
- Q2 **P**: o painel Concorrência aplicado a café (share por vendedor, % de Ads) não foi visto.
- Q5 **P**: Shopee e Amazon só aparecem pelos cases.
- Q7 **S**: nenhum case mede share contra a categoria.

**Sem fonte oficial ou contestado**
- Pacote de preço competitivo de abril de 2026 no nível de detalhe (−1 p.p., armazenagem grátis no Full, campanhas bancadas pelo ML) [cases A2]: só InfoMoney.
- MELI+ com frete rápido abaixo de R$79 a R$9,90 [cases A31]: o 8-K 2T26 não cita; os 8-K de 1T26 e 4T25 não foram relidos.
- Critérios de Polos, Meli Pro, gerente de conta e contêiner direto no Full: só relatos.
- Restrição da API para ferramentas externas: só relato de usuário.

### 1.9 Reconciliações internas pendentes (sem coleta nova)
| Afirmação dada como "não reconf." | Onde já está confirmada | Ação |
|---|---|---|
| Tabela de envio, R$6,95 e desconto de até 50% [pre R1–R4] | [alim A8] leu a ajuda/40538 | Atualizar [pre] e o consolidado §1 |
| Tarifa Clássico e Premium [pre R1; cases A29] | [mix R2] leu a ajuda/870 | Atualizar |
| MercadoLíder e reputação [cases A25–A26] | [rep A2–A6] leu as ajudas 864 e 866 | Atualizar |
| Estoque antigo de Supermercado e valores [log R2] | [alim A4] leu a ajuda/15373 | Atualizar a tabela de [log] |
| Full Super: R$8, sem armazenagem P/M, R$199 [log R8] | [alim A5–A7] leu as ajudas 16449 e 49972 | Atualizar |
| Proibição de refrigerados no Full [log R5] | [alim A2] leu a ajuda/5200 | Atualizar |
| Isenção de 180 dias para SKUs Estrela [log R11] | [mix R9] confirmou por vídeo oficial | Uniformizar o veredito: é vídeo oficial, sem página escrita |
| Painel Concorrência [cases A8] | [mix R6] leu a nota oficial | Atualizar |

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
