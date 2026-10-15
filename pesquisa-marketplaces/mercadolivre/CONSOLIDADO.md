# Mercado Livre Brasil: mapa consolidado de conhecimento

Consolidação de 2026-10-14. É uma pesquisa neutra sobre como os melhores operam a plataforma. Não parte da situação de nenhuma empresa e não traz recomendação para nenhuma.

**Para que serve.** Este é o ponto de partida de quem vai desenhar estratégia e agentes. Cada ponto aponta para a nota de origem, onde estão a URL, o id do vídeo e o raciocínio completo.

**Notas de origem**

Todas as notas ficam em `pesquisa-marketplaces/mercadolivre/`.

| Código | Arquivo |
|---|---|
| [ads] | `ads/notas.md` |
| [pre] | `preco-promocao/notas.md` |
| [log] | `logistica-estoque/notas.md` |
| [rank] | `ranqueamento-anuncio/notas.md` |
| [mix] | `produto-mix/notas.md` |
| [rep] | `reputacao-atendimento/notas.md` |
| [alim] | `alimentos-marca-propria/notas.md` |
| [cases] | `cases-grandes/notas.md` |
| [soc] | `social/notas.md` |
| [obs] | `observacao/lideres.md` |

**Como ler as citações.** "[rep A3]" quer dizer a afirmação A3 da tabela da nota de reputação. "[log §2.3]" quer dizer a seção 2.3 da nota de logística.

**Tipos de afirmação**

| Tipo | O que é |
|---|---|
| [OFICIAL] | Regra, tarifa ou política dita pela plataforma |
| [PRÁTICA] | Tática de praticante |
| [CASE] | Número de uma operação |
| [DADO] | Estudo, relatório ou ferramenta |
| [OBS] | Observação direta |
| N2 | Balanço da MELI na SEC (8-K) |

**Status de verificação.** Cada frente releu as páginas oficiais em 14/10/2026.
- "conf." quer dizer que a afirmação foi confirmada por leitura direta da página oficial.
- "não reconf." quer dizer que a página bloqueou o leitor (HTTP 403, conteúdo carregado por JavaScript ou exigência de login), ou que a afirmação depende só de vídeo.

**"Pode estar superada".** A Central de Ajuda e a Central de Vendedores do ML não mostram data. Por regra, toda tarifa ou política lida nelas leva "(pode estar superada)", mesmo quando está vigente na leitura de 14/10/2026.

---

## 0. A plataforma em uma página

### Como o dinheiro circula

**O que o vendedor paga em cada venda**
- Uma tarifa percentual: Clássico de 10% a 14%; Premium de 15% a 19%, com até 12x sem juros.
- Um custo de envio, calculado por peso e faixa de preço. É cobrado em toda venda, mesmo quando o comprador paga o frete [pre A1–A3; alim A8].
- O antigo "custo fixo por unidade abaixo de R$79" não aparece mais na página oficial. Hoje o que existe são degraus de envio em R$19, 49, 79, 100, 120, 150 e 200 [pre §2.1, §6].
- Nos degraus o vendedor pode perder margem ao subir o preço. Exemplo: passar de R$69,90 para R$79,90 rende só +R$2,10 de margem de contribuição [pre §3.4].

**Frete grátis**
- Entre R$19 e R$78,99, o ML oferece frete grátis padrão (lento), mas o custo de envio continua sendo cobrado do vendedor.
- A partir de R$79, o vendedor oferece frete grátis rápido [pre A6; log A10].
- O limite caiu de R$79 para R$19 em junho de 2025. Segundo o balanço, isso é o motor do crescimento no Brasil: no 2T26, GMV +39% em moeda constante, itens vendidos +56% e conversão +1,1 p.p. [cases A5; pre N22; N2].

**A plataforma paga para ter preço competitivo**
- Desde abril de 2026, o ML dá desconto de tarifa ao vendedor e desconto no Pix ao comprador, só em anúncios com preço competitivo [pre A9; cases A1; N2, conf.].
- A automação de preços e o *price matching* leem os preços de fora do ML [pre §2.2].
- A imprensa relata que, desde outubro de 2025, há punição para quem fica mais caro no ML do que em outros canais [cases A3, não reconf.].

### O que decide quem vende

Os fatores estão em ordem de força da evidência.

1. **Reputação da conta.** É uma porta de acesso, não um ajuste fino. A cor libera ou bloqueia Ads, catálogo, Central de Promoções, Flex, desconto de frete e exposição na busca [rep §2.2; ads A6]. Para ser verde, os limites são: reclamações até 2%, cancelamentos até 1,5% ou 2,5% e envios incorretos até 10% ou 13% [rep A3, conf.].
2. **Experiência de compra por anúncio.** É uma nota de 0 a 100 que tira exposição, pausa ou cancela o anúncio. Entram nela reclamações, atrasos, perguntas, mensagens e título ou descrição inconsistentes [rank A8, A10; rep A18, conf.]. O jeito como o anúncio é construído afeta o ranqueamento também pelo pós-venda.
3. **Logística.** O Full é um *boost* oficial no catálogo, entra no Ad Score dos Ads e aparece como selo e filtro [rank A4; ads A5]. Nas buscas de café observadas, 26 de 40, 21 de 30 e 22 de 25 dos primeiros resultados tinham FULL [obs 1]. Os grandes declaram mandar de 95% a 97% das vendas pelo Full [cases A7].
4. **Preço total e condições.** O vencedor do catálogo é escolhido por algoritmo: preço, parcelas sem juros, Full, frete grátis, envio no mesmo dia e reputação. Quem ganha leva visibilidade máxima e quem perde fica com o mínimo [rank A4–A6, conf.]. Ter o menor preço não basta: um anúncio a R$141 no Full ganhava de outro a R$139 [rank A40].
5. **Qualidade do anúncio.** É uma nota de 0 a 100 que mistura conteúdo (GTIN, ficha técnica, pelo menos 3 fotos, título) e oferta (frete grátis, parcelas, estoque, Mercado Envios) [rank A13, conf.].
6. **Ads.** Vence o leilão quem tem o maior Ad Score × CPC máximo, com o CPC máximo derivado do ROAS objetivo [ads A4]. Ads amplifica um anúncio que já converte e não conserta um anúncio fraco: há consenso de fontes oficiais e de praticantes [ads §6].
7. **Pesos.** O ML não publica a fórmula do ranqueamento. Não há teste A/B nem *holdout* público para nenhum desses fatores [rank §9].

### Para onde a plataforma vai (N2)
- A receita de Ads cresceu +62% a/a e o 1P cresceu +69% a/a, acima do GMV [ads A34; cases A22].
- O ML lançou a marca própria "Basics" [alim A28].
- O MELI+ dá frete rápido abaixo de R$79 a assinantes [cases A31].
- A rede de *fulfillment* faz 55% dos envios regionais [log A18].

**Leitura.** A plataforma premia quem tem o menor preço total, entrega rápido (Full) e mantém poucos problemas por anúncio. Ela também compete diretamente com marcas em 1P.

---

## 1. Regras e números que importam

Só entram aqui regras oficiais, com o status de verificação de cada uma. As páginas sem data levam "(pode estar superada)".

| Tema | Regra / número | Fonte oficial | Data | Status | Nota |
|---|---|---|---|---|---|
| Tarifa | Clássico 10–14% (sem parcelas sem juros); Premium 15–19% (até 12x) | ajuda/870 | s/d (pode estar superada) | conf. | [pre A1; mix §10 R12] |
| Envio | Por peso × faixa de preço, em toda venda. 0,3–0,5 kg a R$19–48,99: R$6,95. Abaixo de R$19: no máximo 50% do preço. Tabela já inclui até 50% de desconto pela reputação verde | ajuda/40538 | s/d | conf. | [alim A8; pre A2–A5] |
| Envio | Faixas: 0–18,99 / 19–48,99 / 49–78,99 / 79–99,99 / 100–119,99 / 120–149,99 / 150–199,99 / 200+. Até 0,3 kg: R$5,65 a R$21,65 | ajuda/40538 | s/d | parcial | [pre A3] |
| Envio | Reajuste em 24/08/2026: +1,6% em média | via terceiro (KvVyJlYt6w0) | 12/08/2026 | não reconf. | [pre A7] |
| Frete grátis | R$19–78,99: padrão, oferecido pelo ML. A partir de R$79: rápido, oferecido pelo vendedor | ajuda/40538; 8-K | s/d; 05/08/2026 | parcial | [log R7; cases A30] |
| Kit | Paga a tarifa de cada produto e um único custo de envio | ajuda/40538 | s/d | conf. | [alim A9] |
| Supermercado | Economia de envio por quantidade não se aplica | ajuda/45023 | s/d | conf. | [alim A9] |
| Tarifa competitiva | Alimentos e Bebidas, R$150–700: −5 p.p. no Premium e −3 p.p. no Clássico | ajuda/51251 | s/d | não reconf. | [pre A8] |
| Tarifa competitiva | Desconto de tarifa e Pix condicionados a preço competitivo, desde abril de 2026 | 8-K 2T26 | 05/08/2026 | conf. (N2) | [pre A9; cases A1] |
| Full | Armazenagem diária por unidade: P R$0,007; M R$0,015; G R$0,050; XG R$0,107 | envios.mercadolivre.com.br/mercado-envios-full | s/d | conf. | [log R1] |
| Full | Estoque antigo cobrado a partir de 4 meses (geral) e 2 meses (Supermercado). Supermercado, item P: R$2,00 a R$14,20 por mês | ajuda/15373 | s/d | conf. | [alim A4; log A3] |
| Full | Índice de desempenho 40/30/20/10. Nota do dia 15 define o espaço; 70 ou mais pode dar espaço estendido. Estrelas ficam fora de 3 métricas | nota Central de Vendedores | s/d | conf. | [log R3] |
| Full | Inconformidade: R$5, R$3 ou R$9 por unidade; tolerância de 5%; 1 abono por trimestre | nota Central de Vendedores | s/d | conf. | [log R4] |
| Full | Produto novo e industrializado, até 25 kg, validade acima de 90 dias | página Full; ajuda/15737 | s/d | conf. | [log R5; alim A1] |
| Full | Proíbe refrigerados ou com controle de temperatura ou umidade, e kits ou packs de supermercado sem EAN | ajuda/5200 | s/d | conf. | [alim A2] |
| Full | Sem estoque no CD, o anúncio é pausado, mesmo com Flex | nota Flex+Full | s/d | conf. | [log R10] |
| Full / Supermercado | Não inclui mais novos vendedores autorizados de Supermercado | ajuda/23329 | s/d | conf. | [alim A3] |
| Full Super | Preço acima de R$8, reputação verde, itens P/M sem armazenagem diária, frete grátis na loja a partir de R$199 (padrão; varia por rota) | ajuda/16449 | s/d | conf. com ressalva | [alim A5–A6] |
| Full Super | Envio até 1 kg a R$29–48,99: "selecionados" R$1,60, demais R$2,40. Abaixo de R$29: no máximo 25% do preço | ajuda/49972 | s/d | conf. (data de 24/08 não conf.) | [alim A7] |
| Despacho | Atrasos até 10% (60 dias) ou 13% (365 dias). Selo "Chegará amanhã" exige 97% no prazo. Bônus Flex de 10% a partir de R$79, só no verde | notas Central de Vendedores | s/d | conf. | [log R12] |
| Reputação | Cinza até 10 vendas em 365 dias. Janela de 60 dias com 101 ou mais vendas em 60 dias; senão, 365 dias | ajuda/866 | s/d (vigência citada: 10/09/2026) | conf. (data não conf.) | [rep A2] |
| Reputação | Verde: reclamações até 2%; cancelamentos até 1,5% (60 dias) ou 2,5% (365 dias); envios incorretos até 10% ou 13% | nota de reputação | s/d | conf. | [rep A3] |
| Reputação | Escala de 60 dias (Líder / verde / amarelo / laranja): reclamações 1/2/4,5/8%; cancelamentos 0,5/1,5/3,5/4%; atraso 6/10/18/22% | developers | 11/08/2025 (pode estar superada) | conf. | [rep A4] |
| Reputação | MercadoLíder / Gold / Platinum: 230 / 575 / 1.725 vendas e R$37 mil / 118,4 mil / 296 mil. Limites: reclamações abaixo de 1%, mediações e cancelamentos abaixo de 0,5%, envios abaixo de 6% | ajuda/864 | s/d | conf. | [rep A5–A6] |
| Reputação | Só afetam reclamações de produto incompleto ou com defeito; pacote avariado não afeta. Cancelamentos acima de 2,5% podem levar à suspensão | ajuda/30193; 5205 | s/d | conf. | [rep A8, A10] |
| Reputação | Reclamação com `has_incentive` respondida bem em 48 h não afeta | developers | 2026 | conf. | [rep A11] |
| Programas | Decola: R$250, até 365 dias, até 5 vendas afetadas. Reputação Protegida: 1% a 3% do faturamento de 60 dias | ajuda/33314; 29276 | s/d | conf. | [rep A21–A22] |
| Devolução | 30 dias (novo) ou 5 (usado). Arrependimento é grátis para o vendedor e não afeta a reputação; defeito ou produto diferente custa e afeta | ajuda/3285; 28088; 32761 | s/d | conf. | [rep A24–A25] |
| Exp. de compra | Boa 75–100, Mediana 50–74, Ruim ≤30. Mediana perde exposição; Ruim pode ser cancelado. Kit herda a pior nota | nota de vendedores; ajuda/39234 | s/d | conf. | [rank A8; rep A18] |
| Catálogo | Algoritmo pesa preço, parcelas sem juros, Full, frete grátis e envio no mesmo dia. `visit_share`: max, medium ou min. Lista motivos de exclusão. Endpoint `price_to_win` | developers | 21/07/2026 | conf. | [rank A4–A6] |
| Qualidade | Nota 0–100 (Básica, Satisfatória, Profissional): GTIN, ficha, pelo menos 3 fotos, título com pelo menos 3 palavras, frete grátis, parcelas, 2 ou mais unidades, Mercado Envios | developers | 31/01/2025 (pode estar superada) | conf. | [rank A13] |
| Anúncio | Título até 60 caracteres; 12 fotos (10 por variação); descrição até 50.000 caracteres. Verificar por categoria | API /categories | 14/10/2026 | conf. | [rank A14] |
| Anúncio | Foto recomendada 1200×1200; mínimo 500; máximo 1920; até 10 MB | developers | 24/03/2026 | conf. | [rank A16] |
| Anúncio | Duplicados proibidos: são cancelados ou ocultados. Usar variações | nota de duplicados | s/d | conf. | [rank A21; mix R5] |
| Mix | Kit virtual: 2 a 6 produtos, até 10 unidades de cada, composição imutável, só item novo, só marketplace | developers | 17/09/2026 | conf. | [mix R1] |
| Mix | User Products: preço e condições por variação, até 30 por produto | developers | 17/09/2026 | conf. | [mix R3] |
| Mix | Desconto por quantidade: reputação verde ou amarela, experiência 50 ou mais, até 1 mês; não vale para itens por kg nem kits | nota; developers | 23/01/2025 (pode estar superada) | conf. | [mix R10] |
| Mix | Preço de atacado só para CNPJ; frete até 80% menor, exceto volumosos e Supermercado | nota | s/d | conf. | [mix R11] |
| Painéis | Concorrência: até 50 anúncios com números aproximados. Tendências por categoria: vendas brutas, unidades e competitividade | notas | s/d | conf. | [mix R6–R7] |
| Ads | Product Ads por ROAS objetivo; `acos_target` visível até 30/03/2026; ACOS = 1/ROAS | developers | 06/07/2026 | conf. (faixa de 1x a 35x não conf.) | [ads A2–A3] |
| Ads | Requisitos: reputação amarela (calculada a partir de 10 vendas), sem dívidas, sem restrição por falsificação, pelo menos 1 anúncio ativo. Decola dispensa reputação | nota de requisitos | s/d | conf. | [ads A6–A7; rep A16] |
| Ads | Brand Ads: Loja Oficial ou Minha Página, reputação verde, 3 ou mais publicações, palavra-chave *phrase*. Migração para Product Ads desde 17/06/2026 | developers | 09/06/2026 | conf. | [ads A8–A9] |
| Ads | Atribuição de 14 dias na API (o webinar diz 15). `sov` = % das vendas vindas de Ads | developers | 06/07/2026 | conf. (14 dias) | [ads A10–A11] |
| Ads | Ad Rank = Ad Score × CPC máximo | developers Brand Ads; webinar | 09/06/2026 | parcial (para Product Ads, só webinar) | [ads A4] |
| Promoções | 12 tipos; cofinanciadas (MARKETPLACE_CAMPAIGN, SMART, PRICE_MATCHING); *boost* do ML; relâmpago não pode ser removida depois de ativa | developers | 09/06/2026 | não reconf. | [pre A14–A16] |
| Preço | Automação: regras INT ou INT_EXT, piso obrigatório, validação contra 60 dias de histórico | developers | 01/10/2026 | não reconf. | [pre A23] |
| Alimentos | Proibido: alimento sem inscrição sanitária, aberto ou fracionado, perto do vencimento, e "Artesanal" em destilados | ajuda/Alimentos_2274 | s/d | conf. | [alim A10] |
| Alimentos | Entrada no Full: rótulo em português, registro Anvisa ou MAPA, lote, validade acima de 90 dias | ajuda/15737 | s/d | conf. | [alim A1] |
| Marca | Loja oficial: documentação de registro de marca e Minha Página; não dá exclusividade | ajuda/1087 | s/d | conf. parcial ("protocolo não serve" não lido literalmente) | [alim A11] |

---

## 2. Por frente: o que os melhores fazem

### 2.1 Ads

**Meta a partir da margem.** Essa conta é consenso.
- ACOS máximo = margem antes de Ads (CM1%).
- ROAS mínimo = 1 ÷ CM1. Exemplo: CM1 de 26,35% dá ROAS mínimo de 3,80 [ads A22; pre A30].
- A meta prática fica abaixo do equilíbrio.

**ROAS por fase do produto** [ads A23; ads §3.1]
- Lançamento: ROAS de 2 a 5.
- Escala: 5 a 10.
- Rentabilidade: 10 a 25.
- O vídeo oficial dá a mesma direção sem números: ROAS mais alto para a curva A [mix A15].
- Divergência: há quem comece em 8–15 e recuse ROAS de 3–4 "para ranquear" [ads A24]. O representante do ML sugere começar perto de 10.

**Estrutura de campanhas**
- Segmentar por margem, faixa de ticket, curva ABC e estratégia. O ML recomenda de 15 a 30 produtos homogêneos por campanha [ads §3.2, A18].
- Produto que destoa vai para uma campanha isolada.
- Produto novo vai para uma campanha nova por 20 a 30 dias [ads A19].

**Peneira** [ads A26]
- Colocar de 10 a 20 anúncios numa campanha de teste.
- Em cerca de uma semana, 3 ou 4 levam quase todos os cliques e vão para a campanha principal.
- O resto vai para uma nova base de teste ou é corrigido.

**Diagnóstico antes de mexer** [ads §3.3]
- Muita impressão e pouco clique: olhar capa e preço.
- Muito clique e pouca venda: olhar o anúncio.
- ROAS caindo: olhar ruptura, preço do concorrente e promoção.
- O representante do ML desaconselha baixar o orçamento quando o ACOS sobe.

**Ritmo de ajuste**
- Não mexer por 7 dias; primeiro ajuste em 15 a 20 dias; subir o ROAS de 2 em 2 [ads A25].
- O gasto é pós-pago na fatura, por isso o acompanhamento é diário [ads A17].

**Pacing pelo estoque** [ads A30, A32; log A29]
- Com cobertura abaixo de 5 dias, reduzir.
- Com estoque acima de 90 dias e ROAS de 30 a 60, trocar rentabilidade por giro.

**TACOS como régua da conta** [ads A28; soc S06]
- Faixas declaradas de 1,5% a 6%.
- Não há teste de incrementalidade. O TACOS é atribuição tratada como causa.

**Contraponto** [soc S07]
- Há operação que declara cerca de R$1,5 milhão por mês sem Ads.
- O ponto comum com os demais: Ads só amplifica o que já converte.

### 2.2 Preço e promoção

**Preço-alvo calculado de trás para frente** [pre §3.4; soc S09]
- Fórmula: P = (custo + embalagem + envio) ÷ (1 − comissão − imposto − TACOS − devoluções − margem).
- O cálculo é iterativo, porque o envio depende da faixa de preço.
- Escada de margem:
  - CM1: antes de Ads;
  - CM2: depois de Ads;
  - CM3: depois de armazenagem, estoque antigo, devolução, afiliados e cupom.

**Degraus de envio.** Baixar de R$50,49 para R$48,99 muda a faixa e pode aumentar a margem [soc S12; pre §3.4].

**Espaço promocional no preço de lista** [pre P1, A25]
- Os praticantes publicam o preço de lista acima do preço-alvo para caber em campanhas.
- Numa operação grande, 81% dos anúncios estavam em campanhas cofinanciadas.
- Limite dado pelo time de pricing do ML: desconto grande com preço final acima do concorrente não converte [pre A21].

**Cobertura contínua de promoções** [pre P2; pre A28]
- Várias campanhas programadas ao mesmo tempo; só a de maior desconto fica ativa.
- Promoção e cupom se somam.
- Revisão semanal; *price matching* revisto todo dia.

**Prioridade às cofinanciadas** ("menos tarifa", SMART, *price matching*). Nelas o preço cai mais do que a margem [pre P3].

**Piso explícito** [pre P4]
- Margem-alvo de cerca de 20% (aceita 15%); importados acima de 30%.
- O ML exige `min_price` em toda automação.

**Promoção ligada ao estoque** [pre P5]
- Antes de ativar, a pergunta é se o estoque aguenta caso a promoção funcione.

**Evitar guerra de preço** [pre §3.5]
- Kits e desconto por quantidade.
- Linha de formatos e tamanhos.
- Ganhar o catálogo por logística e reputação, não por preço.

### 2.3 Logística e estoque

**O que vai para o Full** [log §3.1]
- Curva A e Produtos Estrela.
- Testes e baixo giro ficam em Flex ou Coleta.
- O critério financeiro é fluxo de caixa positivo.

**Antes de levar ao Full**
- Esperar demanda estável: cerca de 2 meses de curva A.
- Ordenar a curva ABC por unidades, não por faturamento [log A28].
- Produto novo vai em lote pequeno [log §3.1].

**Cobertura**
- O ML dá de 4 semanas (piso dos Estrelas) a 8 semanas (teto) [log §3.4].
- Os praticantes enviam para 15 a 30 dias e revisam a cada 15 [log A30].
- Mandar um pouco acima do mínimo sugerido libera a distribuição entre CDs [log A14].

**Lead time completo** [log A16]
- Pedido + preparação + agendamento + trânsito + entrada no CD.
- Pode chegar a 2 semanas.
- O estoque de segurança fica no depósito próprio, proporcional à confiabilidade do fornecedor.

**Índice do Full acompanhado todo dia**, porque duas das métricas são diárias. Nota baixa faz o ML reduzir o espaço do vendedor [log §2.3].

**Ruptura**
- O anúncio pausa e a recomendação de reposição cai, porque passa a ler um histórico com vendas zeradas.
- Ninguém mede o tempo para recuperar a posição [log A12–A13, §9].

**Black Friday** [log A31–A32]
- Planejar desde meados de setembro.
- Fechar os envios até 20–25 de outubro.
- Escolher de 10 a 20 SKUs e dimensionar pelo crescimento histórico.

**Estoque parado**
- O descarte é mais barato do que a retirada [log A26].
- No Supermercado, o estoque antigo começa aos 2 meses [log §5].

### 2.4 Ranqueamento e anúncio

**Cadastro completo antes de tráfego** [rank §3.1]
- Ficha técnica 100% preenchida.
- De 5 a 8 fotos com função definida: capa limpa, benefícios, objeções tiradas das perguntas do líder, itens inclusos, foto ambientada.
- Clipe e descrição.

**Palavra-chave tirada do próprio ML** [rank §3.1; soc S20, S25]
- Fontes: autocomplete, "palavras mais buscadas", tendencias.mercadolivre e "Tendências por categoria".
- Título com até 60 caracteres e o produto nas primeiras palavras [rank A19].
- O líder em café em grão usa título genérico rico em palavra-chave, sem a marca no início [obs 8].

**Engenharia reversa** dos 3 a 5 líderes: extrair perguntas, reclamações e objeções [rank §3.1].

**Clipes** [rank A23–A28]
- Vertical, de 10 a 60 segundos, gravado com o produto em mãos.
- Mais clipes por produto dão mais alcance, porque cada usuário vê um clipe uma única vez.
- No catálogo, o clipe da marca é priorizado.
- Teste do ML: clipe na 1ª posição da galeria deu +10 a 15% de conversão. É o único número com desenho experimental declarado.

**Não mexer no anúncio vencedor.** O ML diz que trocar título ou fotos faz o algoritmo ler o anúncio como novo. Isso vem de webinar, sem página escrita [rank A20].

**Funil** [rank A38; soc S22]
- Impressão baixa: relevância e palavra-chave.
- Clique baixo: capa, preço e título.
- Visita sem venda: descrição, preço total e confiança.
- Um praticante usa cortes de intenção abaixo de 10% das visitas e venda abaixo de 25% da intenção.

**Catálogo** [rank A31, A40]
- Monitorar `price_to_win` e a concorrência todo dia.
- Reagir com logística, parcelas e preço.

### 2.5 Produto e mix

**Painéis oficiais primeiro** [mix §3.1]
- Tendências por categoria e Concorrência.
- As ferramentas externas são aproximações sem margem de erro publicada.

**Triangular a demanda** [mix §3.1]
- Visitas em 30 dias, avaliações novas, idade do anúncio e gráfico de visitas.
- Não somar ferramentas.

**Critérios de entrada com consenso** [mix §3.2]
- Visitas.
- Margem depois de todas as tarifas.
- Quem domina o catálogo, e se o preço do vencedor cobre o *break-even*.

**Ciladas citadas**
- Tarifa + frete acima de 30% do preço.
- Vencedor do catálogo abaixo do seu *break-even*.
- Demanda nas mãos de 1 ou 2 gigantes ou do próprio ML [mix A21].

**Mais buscado não é mais vendido.** O mix precisa cobrir os dois [mix A14].

**Escada de kits** [mix §3.4, A26]
- 1, 2, 3, 5, 10 e 20 unidades.
- Kits de unidades iguais não podem ser kit virtual.

**Racionalizar o portfólio** [mix §3.5]
- ABC por lucro.
- Compra de 90 dias = venda de 30 dias × 3, ajustada pelo giro.
- Margem abaixo de 10% trava a compra.
- Variação curva A sem estoque derruba a conversão.

**Papéis no portfólio** [mix §7]
- Estrela: Full e ROAS alto.
- Novos: ROAS baixo e fora do Full.
- Kits: misturam baixa e alta rotação.

**Divergência sem resolução** [mix §3.5]
- Cauda longa no ML, para diluir o risco de concentração.
- Contra poucos SKUs profundos, argumento vindo de loja própria.

### 2.6 Reputação e atendimento

**Rotina de reputação** [rep P1–P2]
- Página de reputação todos os dias, olhando a tendência e as vendas antigas que saem da janela.
- Alerta interno a 50% do limite.

**Atrasar em vez de cancelar** [rep P3–P4]
- O limite de atraso é de 4 a 12 vezes o de cancelamento.
- Antes de cancelar, oferecer uma variação pela mensagem ativa (350 caracteres).

**Resolver em 24 a 48 h, antes da mediação, assumindo o erro** [rep P5; rep A11].

**Corrigir a causa no anúncio** [rep P6, P11]
- Foto fiel, medidas e quebra de objeção.
- Ler os motivos de devolução por anúncio.

**Qualidade do lote** [rep P7]
- Testar o lote e trocá-lo com o fornecedor. É o que mais aparece em revenda e importação.

**Operação sem falha** [rep P8–P10]
- Estoque sincronizado e Modo férias.
- Despacho no mesmo dia.
- Perguntas respondidas em até cerca de 12 h, com assistente e relatório de perguntas frequentes alimentando o cadastro.

**Programas como colchão em conta nova ou em recuperação.** Decola e Protegida mascaram a cor, mas não a mudam [rep §2.5, §6].

**Limite de mensagens** [rep A29]
- Não há ferramenta oficial para pedir avaliação.
- O campo livre de mensagem some depois da entrega.

### 2.7 Alimentos e marca própria

**Linha completa** [alim P1; obs 3]
- Formatos: grão, moído, cápsula e drip.
- Tamanhos: 250 g, 500 g e 1 kg.
- Isso gera várias posições na busca.

**Full como padrão** [alim P2]
- Ressalva: a habilitação de Supermercado no Full está fechada a novos autorizados.

**Preço em camadas** [alim P3; obs 4–5]
- Preço riscado, Pix (8% a 53% OFF) e preço por kg.
- Desconto por quantidade de 5, 10 ou 100 unidades.

**Informação de uso para reduzir reclamação** [alim P4]
- Escala de intensidade na cápsula; explicação da válvula da embalagem.

**Rentabilidade por pedido e por canal** [alim P5; cases §3.2.4]
- DRE por pedido e analista de conciliação.

**Registro de marca e Brand Protection Program** [alim P6]
- Registrar marca, fotos e desenho.

**Equipe por canal × categoria** [alim P7].

### 2.8 Cases grandes

Todos os números são autodeclarados e foram rebaixados a [PRÁTICA] C [cases A9].

**Pontos em comum**
- 95% a 97% das vendas do ML pelo Full [cases A7].
- Operação perto dos CDs de SP [cases §3.2].
- Cadastro disparado pela nota de entrada, com meta de 10 dias até o produto estar em todos os canais [cases A42].
- Margem conciliada por pedido [cases A44].
- Organização matricial canal × categoria, com mídia à parte [cases A45].
- Times enxutos: 8 pessoas para mais de R$3 milhões por mês; 52 pessoas para cerca de R$6 milhões [cases A10–A11].
- Lucro Real como marco de escala [cases §3.2.7].

**Erros documentados**
- Concentração em um item: 80% do faturamento [cases A14].
- Sair do nicho [cases A15].
- 7.000 SKUs [cases A16].
- Fornecedor que não acompanha quando o anúncio ranqueia [cases A17].

**Reação à regra de preço**
- Preço único entre canais.
- Linhas exclusivas por canal [cases A4].

**Revenda que vira marca.** Três de onze cases migraram de revenda para marca própria por guerra de preço no catálogo [cases A18].

---

## 3. Benchmarks de referência

São faixas, não médias. Ninguém publica benchmark por categoria com método para o ML Brasil [ads §9; rank §9; rep §4].

| Indicador | Faixa | Tipo / confiança | Fonte |
|---|---|---|---|
| ACOS máximo | CM1% (método, não número) | [PRÁTICA] método, B | [ads A22; pre A30] |
| ROAS objetivo permitido | 1x–35x | [OFICIAL] não reconf. | [ads A2] |
| ROAS inicial praticado | 8–15 (2–5 em lançamento agressivo) | [PRÁTICA] C | [ads A24; soc S03–S04] |
| ROAS visto pelo representante do ML | 3–40 | [OFICIAL via representante] | [ads §4] |
| TACOS-alvo declarado | 1,5–6% | [PRÁTICA] C | [ads A28; soc S06] |
| TACOS mostrado em tela | 0,6–5,8% (30 dias); 0,06–1% (importados, poucos SKUs) | [CASE] C | [ads §4; pre A26] |
| Vendas vindas de Ads | 27–81% por conta; cerca de 50% "média" | [PRÁTICA] C | [ads A29] |
| ACOS por categoria no BR | 5–25% (método não publicado) | [DADO] C | [ads A37] |
| Amazon EUA, Food & Grocery | ACOS 21% (35% em contas grandes); só ordem de grandeza | [DADO] C | [ads A38] |
| Conversão "boa" | R$19–79: 3–6%; R$79–250: 1,5–5%; acima de R$250: frequentemente abaixo de 1% | [PRÁTICA] C | [rank A39] |
| Conversão média de conta | cerca de 6%; abaixo de 2% é ruim | [PRÁTICA] C | [ads §4] |
| Margem-alvo | 15–20% (revenda); acima de 30% (importados); 25–35% (fabricante) | [PRÁTICA] C | [pre A25, N16; soc S10] |
| Margem de grandes | margem de contribuição cerca de 28% e lucro líquido cerca de 10% (moda com fábrica); 20–60% por nicho (hospitalar) | [PRÁTICA] C | [cases A12, §4] |
| Peso da plataforma em café (fora do Super) | 250 g a R$35: envio cerca de 20% e tarifa + envio cerca de 30–34%. 1 kg a R$85: cerca de 27–31% | cálculo com tabela oficial | [alim §5.7] |
| Cobertura de estoque no Full | 4–8 semanas (ML); envios de 15–30 dias (praticantes); vermelho abaixo de 5 dias; alto acima de 90 | [OFICIAL] + [PRÁTICA] | [log §3.2, §3.4] |
| Giro para ir ao Full | cerca de 3 unidades/dia ou cerca de 2 meses de curva A | [PRÁTICA] C | [soc S14; log A28] |
| Lote de teste no Full | 20–30 unidades | [PRÁTICA] C | [mix §4] |
| Margem de segurança da reputação | alerta a 50% do limite | [PRÁTICA] C | [rep A34] |
| Folga real no limiar de 101 vendas | 2 reclamações mantêm o verde; a 3ª leva ao amarelo | cálculo com limite oficial | [rep §4] |
| Devolução "saudável" | cerca de 2% em eletrônicos, ou o histórico do próprio produto; o ML não publica número | [PRÁTICA] C | [rep A37] |
| Fotos | 6–9 nos líderes de café; "média de 8" no top 100 de algumas categorias | [OBS]; [PRÁTICA] | [obs 9; rank §4] |
| Selo FULL no topo de café | 26/40 grãos; 21/30 moído; 22/25 cápsulas | [OBS] | [obs 1] |
| Preço por kg de café | supermercado R$32–84; especial de marca R$90–160; microlote acima de R$200 | [OBS] | [obs 4] |
| Faturamento por pessoa | revenda enxuta R$300–375 mil por mês; marca com produção R$100–160 mil | [PRÁTICA] C (bases diferentes) | [cases §3.1] |
| Cofinanciadas na operação | 81% dos anúncios | [PRÁTICA] tela | [pre A25] |

---

## 4. Divergências entre fontes e como resolver na prática

| # | Divergência | Lados | Leitura provisória | O que medir ou checar |
|---|---|---|---|---|
| 1 | Janela de atribuição de Ads | API 14 dias × webinar 15 dias [ads A10] | Usar 14 dias, que é a regra escrita | Conferir no painel; comparar vendas atribuídas no dia 15 |
| 2 | Requisitos de Product Ads | Nota oficial (amarelo, 10 vendas) × webinar (+15 dias de conta, sem fatura vencida) [ads §2.2; rep A16] | Vale a nota de requisitos | Testar a elegibilidade numa conta nova |
| 3 | Ads eleva o orgânico? | Praticantes dizem que sim, e alguns falam em "score de TACOS" × nenhuma fonte oficial [ads A33; rank §3.2] | Hipótese | Teste de pausa ou *holdout* por SKU, ou geo-teste, lendo vendas sem publicidade |
| 4 | Gasto de Ads em termos da própria marca | Product Ads não expõe termo de busca [ads §3.4] | Não mensurável hoje | Comparar com o Brand Ads (que tem palavra-chave) ou com períodos de pausa |
| 5 | Desconto de envio por reputação | até 50% (página atual) × 70% (vídeo de maio) [pre A5; rep A15] | 50% | Conferir na tabela logada de custos |
| 6 | Custo fixo abaixo de R$79 | Página atual: só degraus de envio × blogs e vídeo de maio: custo fixo, corte em R$12,50 [pre §6; mix A37] | Vale a página atual (40538) | Simulador logado; conferir faturas reais por faixa |
| 7 | Janela da experiência de compra | 60/365 dias (nota da Central) × 180 dias (developers e ajuda/39234) [rank §2.3, A9; rep A18] | Sem conciliação oficial; talvez uma seja janela de exibição | Comparar o texto do painel com as vendas da janela |
| 8 | Corte da janela de reputação | 101 (oficial) × 68 (vídeo) × 60 (developers 2025) [rep A2; cases A26] | 101 | Conferir no painel da conta |
| 9 | Decola | 90 dias (webinar de maio) × 365 dias (página atual) [rep §2.5] | 365 | — |
| 10 | Cobertura máxima no Full | 30–45 dias × "até 2 meses" [log A15] | Faixa de 4 a 8 semanas | Índice do Full e custo de estoque antigo por SKU |
| 11 | Ganho de vendas com Full | "até 2x", "70% dos anúncios +150%" (ML) × "até 5x" (praticante) [log A17] | Alegação sem método | Antes e depois com controle (SKUs pareados fora do Full) |
| 12 | Desconto de frete no Full | "50% a partir de R$79" (nota antiga) × tabela única para todas as modalidades [log §3.4; rep A27] | Vale a tabela única | — |
| 13 | Catálogo "sempre primeiro" × mecânica da buy box | Frase da nota de dicas × `visit_share` minimum para quem perde [rank A2] | Não tratar como regra mecânica | Posição observada com e sem buy box |
| 14 | Preço por variação | "Variação sem aumento de preço" (nota antiga) × User Products com preço por variação [mix R3, R5] | A regra depende do modelo da conta | Verificar se a conta já migrou para User Products |
| 15 | Paridade de preço com outros canais | Sem regra oficial de paridade [pre §2.2] × punição desde out/2025 relatada pela imprensa [cases A3] | O ML lê preços externos, comprovadamente via INT_EXT e *price matching* | Avisos na Central; elegibilidade a cofinanciadas com preço externo menor |
| 16 | Supermercado no Full | Ajuda 23329 (sem novos autorizados) × praticante ("faz muito sentido") × nota que coloca em Supermercado, automaticamente, quem tem estoque no Full [alim A3, §2.4] | Ponto mais crítico a checar | Abrir pedido de habilitação; ler a nota logada |
| 17 | Estoque antigo em alimentos | 2 meses (ajuda 15373) × 4 meses (vídeo) [alim §3.2] | 2 meses para Supermercado | — |
| 18 | Estoque compartilhado | Exclui Alimentos e Bebidas e itens com validade (oficial) × lista de praticante [log §3.4] | Vale a oficial; não reconferida [log R9] | — |
| 19 | A descrição indexa na busca? | "Não indexa" × "cole palavras-chave no fim" [soc S20–S21] | Sem fonte oficial; o ML só diz que a palavra-chave deve estar no título [rank A19] | Busca por termo presente só na descrição |
| 20 | Começar com preço baixo ou alto | Preço de entrada baixo × começar caro e descer [rank §3.2; pre D1; mix §3.2] | Sem teste | Teste por SKU pareado; o catálogo pesa logística |
| 21 | Efeito da medalha | Oficial: mais exposição × praticante: nenhum efeito visto [rep D2] | Hipótese | Impressões antes e depois da troca de medalha |
| 22 | Classe do INPI para loja oficial | Classe 35 × classe do produto × página que não cita classe [alim §3.2] | Sem regra oficial | Consulta ao ML na solicitação |

---

## 5. Indústria e marca própria × revenda: onde a plataforma favorece cada um

| Alavanca | Favorece | Por quê | Fonte |
|---|---|---|---|
| Catálogo e buy box | Revenda eficiente | O algoritmo escolhe por preço total, Full, parcelas e reputação, não por quem é o dono da marca. No Pilão 1 kg havia 72 ofertas e ganhava um supermercado; no Italle, outra loja oficial vencia a própria marca | [rank A4; obs 2] |
| Avaliações e "vendidos" | Marca | Pertencem ao produto de catálogo, então a marca acumula prova social que a revenda usa mas não controla | [rep A40; obs 2] |
| Clipe no catálogo | Marca | O clipe da marca é priorizado sobre o do ganhador | [rank A28] |
| Loja oficial, Brand Ads, Minha Página | Marca | Exigem registro de marca; o Brand Ads é o único formato com palavra-chave | [alim A11; ads A8] |
| Brand Protection Program | Marca | É gratuito e cobre marca, desenho e direito autoral | [alim A12] |
| GTIN, ficha e Full Super "selecionados" | Marca com EAN | O GTIN pontua na qualidade; os selecionados por EAN pagam envio menor (critério não publicado) | [rank A13; pre §7] |
| Desenho do produto para o Full | Marca | Só quem fabrica pode adaptar tamanho e peso à classe mais barata | [log §7] |
| Margem para ROAS de lançamento | Marca | Margem bruta maior permite ROAS 5 e ainda reter cerca de 20% | [ads §3.1] |
| Preço de lista e *price matching* | Contra a marca multicanal | O ML lê preços externos e gera ofertas de equiparação; não há política de preço mínimo anunciado (MAP) para a marca | [pre §5, §7] |
| 1P e marca Basics | Contra as duas, mais contra marca de produto fácil de copiar | A plataforma compete diretamente | [alim A28; cases A22] |
| Escala de compra, exclusividade e subsídio do fornecedor | Revenda | Compra com prazo, liquidação paga pelo fornecedor e curva Z | [cases §7] |
| Peneira e cauda longa | Revenda e importação | Muitos SKUs, concentração nos vencedores, giro | [ads §7; mix §3.5] |
| Estoque compartilhado | Revenda do mesmo EAN | Unidades idênticas geridas juntas (alimentos excluídos) | [log §7] |

**Específico de revenda, dropshipping e importação**
- Disputa de buy box em catálogo alheio [pre §7].
- Margem-piso alta e calendário de importação: pedido em junho, Full em setembro [mix §7].
- Teste de lote e risco de fornecedor [rep P7; cases A17].
- Dropshipping é incompatível com o Full e piora o tempo de disponibilidade [rank §7; log §7].
- Título longo e "de/por" agressivo do importado com marca própria [obs, outras categorias].

**Específico de indústria e marca própria**
- Defender o próprio catálogo competindo nas mesmas variáveis da buy box [rank §5].
- Conflito com a tabela do canal físico [cases §5].
- Linhas ou colaborações exclusivas por canal [cases §7].
- Regularização sanitária e rótulo próprios [alim §7].

---

## 6. Alimentos e café: regras e oportunidades específicas

### Regras
- **Logística decide a viabilidade** [alim A1–A3; log §5]:
  - o Full exige validade acima de 90 dias, rótulo em português e registro Anvisa ou MAPA;
  - não aceita refrigerados;
  - não aceita kit ou pack de supermercado sem EAN de fábrica;
  - fora do Full não há validade mínima, desde que a legislação seja cumprida.
- **Supermercado no Full fechado a novos autorizados** (ajuda 23329, conf.). Tem impacto direto em quem ainda não está habilitado [alim A3].
- **Full Super** [alim A5–A7, conf.]:
  - preço acima de R$8, reputação verde;
  - itens P e M sem armazenagem diária;
  - frete grátis na loja a partir de R$199;
  - envio dos "selecionados" muito mais barato: R$1,60 contra R$6,95 do envio comum na faixa de R$19–48,99.
- **Estoque antigo a partir de 2 meses** em Supermercado. Com validade, isso transforma previsão e liquidação em parte do preço [alim A4; pre §5].
- **Sem economia por volume em Supermercado.** A redução de envio por quantidade não vale; o kit paga um único envio [alim A9].
- **Desconto por quantidade não vale para itens vendidos por kg** [mix A8].
- **Tarifa menor na faixa de R$150 a R$700.** Alimentos e Bebidas (incluindo café em grão, moído e solúvel) têm −3 a −5 p.p. Isso incentiva kits e packs nessa faixa (não reconf.) [pre A8].
- **Política de alimentos** [alim A10]: proíbe produto sem inscrição sanitária, fracionado ou perto do vencimento. A API de reclamações tem o grupo `expiring_food` [rep A33].
- **Rótulo de café (Portaria SDA 570/2022)**: grupo, espécie, ponto de torra, lote e CNPJ. "Gourmet" e "Superior" são categorias privadas [alim A14].
- **Fiscalização no CD.** A Anvisa inspecionou o CD de Cajamar em 18/03/2026; os retidos foram 0,34% dos itens regulados [alim A13].
- **Estoque compartilhado** exclui alimentos e itens com validade [log A22].

### Oportunidades estruturais observadas (neutras, sem recomendação)
- **Catálogo de marca grande vira arena de revenda** [obs 2; alim A23]. Quem combina Full, reputação Platinum e preço total competitivo pode ganhar a buy box de marcas consolidadas. A marca dona do produto pode perdê-la.
- **Linha completa ocupa várias posições na busca** [obs 3]. Os líderes de marca usam 4 formatos × 3 tamanhos e loja oficial com seguidores (+35,3 mil e +11,7 mil).
- **Preço por kg na página** [obs 4]. Ele torna o kg a unidade de comparação entre embalagens. As faixas observadas separam bem o supermercado do especial e do microlote.
- **Desconto por quantidade, kits e multipacks** são padrão dos líderes [obs 5]. Na faixa de R$150–700 eles também capturam a redução de tarifa [pre §5].
- **Topo da busca pouco disputado no especial.** Os cafés especiais sem Full aparecem no topo com poucas vendas. As exceções com volume (Appassionato, Serra do Encontro) mostram espaço para operação especial com escala [obs 1].
- **Recompra** [alim §5.4]:
  - o ML só tem botão de recompra, sem assinatura;
  - a Amazon tem Programe e Poupe;
  - os seguidores de Minha Página "compram 60% mais", segundo o ML, sem base publicada [ads §2.5].
- **Embalagem e informação reduzem reclamação** [alim A31; rep §5]. Produto que chega aberto ou danificado pesa na experiência de compra. Escala de intensidade e explicação da válvula reduzem queixas de expectativa.
- **Ticket baixo** [alim §5.7; pre §3.4]. Abaixo de R$49 o envio domina, chegando a cerca de 20% do preço. Embalagem maior, kit e o Full Super mudam a conta.

---

## 7. Perguntas abertas para a fase de estratégia

1. **Habilitação de Supermercado.** Qual a via real hoje para um vendedor de alimentos sem autorização prévia: Full comum, Full Super, Flex ou Coleta? Como a regra da ajuda 23329 convive com a entrada automática em Supermercado? [alim A3, §2.4]
2. **Tarifa exata.** Qual o percentual da categoria café e Alimentos no Clássico e no Premium (simulador logado)? A redução de −3/−5 p.p. entre R$150 e R$700 está vigente? [pre §9.1]
3. **Lista de "produtos selecionados".** Quais critérios valem no Full Super e como um EAN entra nela? [pre §9.8; alim §9]
4. **Ads × orgânico.** Existe efeito incremental do Product Ads sobre as vendas orgânicas? Que desenho de teste de pausa ou *holdout* cabe na operação? [ads §9]
5. **Clique pago e buy box.** Quem recebe a venda quando o clique pago leva a um catálogo ganho por outro vendedor? [ads §9]
6. **Recuperação após ruptura.** Quanto tempo leva para recuperar a posição, e qual o custo em vendas? [log §9.1]
7. **Peso do Full no ranking.** Quanto o Full pesa contra o preço, isolado de outros fatores? [log §9.2; rank §9]
8. **Experiência de compra.** Qual janela vale de fato, 60/365 ou 180 dias? Qual o efeito da nota calculada "por categoria" em anúncios novos? [rank A9]
9. **Preço multicanal.** Qual a regra formal de paridade, que lista de canais externos o ML monitora e qual o efeito na elegibilidade a cofinanciadas e no desconto de tarifa? [cases §9.5; pre §9.5]
10. **Benchmarks de alimentos.** Quais são, para alimentos no ML, as faixas de conversão, ACOS e TACOS, devolução e recompra? Hoje há só faixas genéricas de praticantes [alim §9; ads §9].
11. **Painel Concorrência aplicado a café.** Qual o share por vendedor, que alavancas os líderes usam e quanto usam de Ads? A observação não capturou o rótulo "Patrocinado" [obs, limitações].
12. **Devolução de alimentos.** Qual o prazo específico, o destino da unidade aberta na triagem do Full e o custo real do arrependimento em perecível? [rep §5, §9.6]
13. **Assinatura e recorrência.** Existe ou está previsto um programa de assinatura no ML? Qual o lado vendedor do Programe e Poupe da Amazon no Brasil? [alim §9]
14. **Shopee e Amazon.** As regras de alimentos, *fulfillment* e Ads ficaram quase sem fonte oficial brasileira e precisam de rodada própria [log §9.9; alim §9; ads §9].
15. **Reverificação.** É preciso reler por navegador logado as regras marcadas "não reconf.": promoções, automação de preço, tabela 51251 e faixas de envio completas [pre §10; cases §10].
16. **Sortimento.** Para cada papel no portfólio (estrela, aposta, kit), qual o número mínimo de SKUs e formatos para ocupar mais de uma posição sem diluir o giro no Full e no índice de desempenho? [mix §9; log §2.3]
