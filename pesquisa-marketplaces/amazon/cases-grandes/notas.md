# Amazon: como operam os maiores vendedores (frente cases-grandes)

Data da análise: 2026-10-14. Escopo: Amazon Brasil, com referências da Amazon dos EUA quando a mecânica é a mesma.
Pesquisa neutra: descreve como os melhores operam. Não traz recomendação para nenhuma empresa.

**Base usada**
- **Transcrições lidas (12 da frente):** tpS__DSMMqo, 78sSkRh2crI, gzPKGT7uRRI, kDF4gtMCAdo, 4Vvrft5eTDo, L380mHir7aA, 1fXOj1mcRuU, rN4j4kZvkDg, Vl6KK7-lEz0, SqoNj2DDRSU, 6jtpl-y_iZw, nLM_JFURSTI.
  - Os podcasts longos (gzPK, kDF4, rN4j, SqoN, 6jtp e a segunda metade de 78sS) foram lidos por extração de trechos com número, regra ou termo de operação.
  - Os outros foram lidos inteiros.
- **Transcrições extras consultadas pelo tema:** l9MMfiAAWqo (tarifas 2026), H0ab_x1YIBY (webinar oficial Amazon Vantagens), VvcswcsjuUw (masterclass oficial de FBA), CpeAKSyctRg (genérico, revenda e marca), nHdlguzjAik (PPC), cZysnqICrkY (preço por canal).
- **Camada oficial (13 páginas lidas em 2026-10-14):**
  - venda.amazon.com.br: /precos, home, /cresca/fba, /brand-registry, /historias, /cresca/programa-de-recompensas-do-vendedor, /publicidade, /promocoes, /acelere-seu-negocio.
  - sell.amazon.com/tools/amazon-brand-analytics (EUA).
  - Release do 2º tri de 2026 da Amazon (ir.aboutamazon.com).
  - aboutamazon.com.br: notícia "R$ 55 bilhões" e notícia da Mega Oferta Prime.
  - As páginas de ajuda do Seller Central (validade no FBA e alimentos) exigem login e não foram lidas.
- **Camada de dados (5 fontes):**
  - Marketplace Pulse: 3 artigos de jul a set de 2026.
  - Jungle Scout: páginas do State of the Amazon Seller 2025 e do relatório "3P seller disruption"; os números completos ficam atrás de formulário.
  - Benchmark 2026 da Jungle Scout: só resumo qualitativo.
- **Observação direta:** `observacao/lideres.tsv` (10 linhas coletadas em 2026-10-14). O arquivo `lideres.md` não existe.
- **Limite:** a cota de buscas na web desta rodada acabou cedo. As páginas oficiais foram abertas por URL direta. Pacvue, Perpetua, SmartScout, Helium 10 e Nubimetrics (Amazon BR) não foram lidos e aparecem na seção 9.
- **Corte de 6 meses:** regra de plataforma com data anterior a 2026-04-14, ou sem data, leva "(pode estar superada)".

---

## 1. Resumo executivo

1. **No topo de café, o líder é 1P (a Amazon compra e revende).**
   - Fonte: observação de 2026-10-14 em `lideres.tsv` [OBS].
   - O #1 de Café (Orfeu grãos 1 kg) é "vendido e enviado por Amazon.com.br", tem 16.737 avaliações e "mais de 10 mil compras no mês passado".
   - Coffee Mais e Baggio também são 1P.
   - A única marca 3P observada com FBA (Italle) compra a 1ª posição patrocinada e banners em páginas de concorrentes.
2. **Os cases de maior porte com número são dos EUA e todos autodeclarados.**
   - Ângelo Mário: mais de US$ 1 milhão/mês, cerca de 500 SKUs (cerca de 100 produtos-mãe), 70 mil unidades/mês, 15 funcionários remotos nas Filipinas e zero nos EUA (tpS__DSMMqo, 2026-07-23) [PRÁTICA, confiança C].
   - Josh Hadley: mais de US$ 20 milhões/ano (nLM_JFURSTI, 2026-07-29) [PRÁTICA, C].
3. **Nenhum case brasileiro de Amazon tem número auditável.**
   - Os números vêm de mentorias que vendem o próprio serviço (78sSkRh2crI, 4Vvrft5eTDo, 1fXOj1mcRuU).
   - As 21 histórias oficiais da Amazon também não trazem faturamento, período nem base de comparação (venda.amazon.com.br/historias, acesso 2026-10-14) [OFICIAL].
4. **A Amazon Brasil liga o subsídio logístico ao gasto em Ads.**
   - A tarifa única de R$ 6 por unidade no FBA vale para produtos a partir de R$ 79, com coleta e armazenagem isentas.
   - Para manter o benefício, o vendedor precisa investir pelo menos 3,5% da receita dos produtos elegíveis em anúncios patrocinados.
   - Fonte: venda.amazon.com.br/cresca/fba, acesso 2026-10-14 [OFICIAL; página sem data de início ou fim].
5. **Os incentivos de 2026 favorecem marca e FBA.**
   - Dono de marca: crédito de até R$ 300 mil, aplicado como desconto sobre a comissão de 5% nas primeiras vendas de marca, até R$ 6 milhões.
   - Item novo elegível ao Prime: comissão de 5% nas primeiras 100 unidades, por até 120 dias.
   - FBA grátis por 30 dias, com extensão possível até 31/01/2027.
   - Fonte: página de Recompensas do Vendedor, acesso 2026-10-14 [OFICIAL].
6. **A tabela de comissão define o piso da conta de margem.**
   - Alimentos ("Comidas e bebidas"): 10%. A maioria das categorias fica entre 12% e 15%.
   - Plano Profissional: R$ 2 por item vendido; mensalidade de R$ 19 a partir do 13º mês.
   - Fonte: venda.amazon.com.br/precos, "atualizadas em 20/01/2025" [OFICIAL, pode estar superada].
7. **A estrutura dos grandes é time enxuto, rotina fixa e ferramenta própria.**
   - Ângelo: reunião de board às segundas; produto às terças; criativos às quartas; vendas por produto conferidas "quase toda hora"; ferramenta própria mais uma de terceiros (tpS__DSMMqo) [PRÁTICA, C].
8. **Estoque é a principal causa de morte de marca, segundo o operador de 8 dígitos.**
   - Meta de 90 a 120 dias de cobertura, giro de 4 a 6 por ano e nunca mais de 12 meses de estoque.
   - O SKU é cortado se não vender o lote em 12 meses.
   - Exemplo citado: a Thrasio quebrou com 5 a 10 anos de estoque em SKUs específicos.
   - Fonte: nLM_JFURSTI, 2026-07-29 [PRÁTICA, C; EUA].
9. **Os erros documentados com consequência seguem o mesmo padrão.**
   - Queda de nota por defeito de lote: de 4,8 para 4,2, com estoque encalhado.
   - Antidumping: multa e carta de crédito de US$ 50 mil presa por 5 anos.
   - Fonte: tpS__DSMMqo [PRÁTICA, C].
   - Contestações de entrega em 5% a 10% das vendas DBA levaram um vendedor brasileiro a sair da Amazon (L380mHir7aA, 2026-09-04) [PRÁTICA, C].
10. **Ter vários canais não tira a concentração na Amazon.**
    - 71% dos vendedores com a Amazon como canal principal ainda tiram pelo menos 75% da receita de marketplace dela.
    - A Amazon diz que mais de 95% dos vendedores são multicanal.
    - Fonte: Marketplace Pulse, 24/09/2026 [DADO, EUA, método não detalhado].
11. **No ranking dos EUA, a rotatividade dos top sellers é alta.**
    - 68,6% dos top 10 mil estavam lá 12 meses antes; 49,6%, três anos antes.
    - A China tem 55,9% dos top 10 mil (42,5% em 2020). Os EUA têm 81,4% do top 100.
    - Fonte: Marketplace Pulse, 09/07/2026 [DADO, B].
12. **A receita da Amazon mostra para onde a plataforma empurra os vendedores.**
    - No 2º tri de 2026, Ads cresceu 26% ao ano (US$ 19,8 bi), acima dos serviços a vendedores 3P (+16%) e das assinaturas (+12%).
    - Fonte: release de 30/07/2026 [OFICIAL N2, global].
13. **Revenda de marca alheia tem margem estreita.**
    - Na revenda com disputa de Buy Box, a margem média dos grandes vendedores que um mentor atende é de 8% (CpeAKSyctRg, 2026-10-02) [PRÁTICA, C].
    - Marcas em declínio enfrentam 3 a 5 vezes mais revendedores que as líderes (Jungle Scout, 3p-seller-disruption, 2025) [DADO, método não publicado].
14. **Brand Registry pode começar antes da concessão do INPI.**
    - A Amazon aceita marca "em processo de registro ou com pedido pendente" em alguns casos (venda.amazon.com.br/brand-registry, acesso 2026-10-14) [OFICIAL].
    - O INPI teria criado exame prioritário para vendedor de marketplace (Portaria 66/2026), com prazo de 90 a 180 dias contra cerca de 24 meses no rito comum (kDF4gtMCAdo, advogada, 2026-06-09) [PRÁTICA, C; conferir no INPI].

---

## 2. Como funciona (mecânica e regras oficiais, com data)

### 2.1 Tarifas que moldam a operação (venda.amazon.com.br/precos, acesso 2026-10-14)
- **Comissão sobre o preço final** (página "atualizada em 20/01/2025", pode estar superada):

  | Comissão | Categorias |
  |---|---|
  | 10% | Comidas e bebidas; pneus; TV e áudio |
  | 11% | Bebidas alcoólicas; linha branca; celulares |
  | 12% | Casa, Cozinha, Pet, Bebês, Saúde e cuidados pessoais etc. |
  | 13% | Beleza; Papelaria |
  | 14% | Moda |
  | 15% | Demais categorias |
  | Faixas | Acessórios: 15% até R$ 100 e 10% no excedente. Móveis: 15% até R$ 200 e 10% no excedente |

- **Comissão mínima:** o texto diz R$ 1; a tabela mostra R$ 2 em parte das categorias. É uma divergência dentro da própria página.
- **Planos:**
  - Profissional: R$ 2 por item, mais comissão; mensalidade grátis no 1º ano e R$ 19/mês a partir do 13º mês.
  - Individual: R$ 2 por item.
- **FBA** (tarifas "atualizadas em 01/08/2025", pode estar superada):
  - Logística por peso, preço e dimensão. Exemplo: até 100 g e preço abaixo de R$ 30, R$ 10,05.
  - Armazenagem: R$ 75/m³ para itens abaixo de 10 mil cm³; R$ 37,50/m³ acima.
  - Longo prazo (mais de 365 dias): R$ 525/m³, somado à armazenagem.
  - Remoção: de R$ 0,99 a R$ 3,60.
  - Coleta por caixa e estado. Em SP, até 3 kg: R$ 0,93 a R$ 2,92.
- **DBA (Delivery by Amazon):**

  | Preço do produto | Tarifa por unidade |
  |---|---|
  | Abaixo de R$ 30 | R$ 4,50 |
  | R$ 30 a R$ 49,99 | R$ 6,50 |
  | R$ 50 a R$ 78,99 | R$ 6,75 |
  | A partir de R$ 79 | Tabela por estado e peso |

  - Uma praticante cita desconto de 50% no DBA para SP acima de R$ 79 (l9MMfiAAWqo, 2026-10-08) [PRÁTICA, não confirmado na página].
- **Parcelamento sem juros:** 1,5% sobre as vendas dos ASINs participantes, para produtos a partir de R$ 40.
- **Pagamento:** quinzenal (home de venda.amazon.com.br).
  - Um praticante dos EUA relata 14 dias mais 7 dias de retenção após a entrega (tpS__DSMMqo) [PRÁTICA; EUA].
  - Um vendedor brasileiro de DBA relata de 30 a 45 dias entre envio e dinheiro na conta (L380mHir7aA) [PRÁTICA].

### 2.2 Incentivos de 2026 (página de Recompensas do Vendedor e /cresca/fba, acesso 2026-10-14; sem data de início)
- **FBA grátis por 30 dias** (logística, coleta e armazenagem) para conta nova ou para quem entra no FBA pela primeira vez.
  - Depois disso: tarifa única de R$ 6 por unidade para preço a partir de R$ 79, com coleta e armazenagem zeradas.
  - Condição: investir pelo menos 3,5% em anúncios patrocinados.
  - Extensão possível até 31/01/2027 [OFICIAL].
- **A regra de transição dos 3,5% está detalhada no canal oficial (TikTok @vendacomamazon, 2026-07-16):**
  - Contas FBA ativadas a partir de 01/04/2026 investem 3,5%.
  - Contas anteriores atingem 3,5% em 30 dias ou somam 1 ponto ao que investiam em abril.
  - Fonte: `social/notas.md` [OFICIAL via terceiro; o valor saiu de transcrição automática].
- **Comissão de 5%** para itens novos elegíveis ao Prime: primeiras 100 unidades padrão ou 50 extragrandes, por até 120 dias.
- **Crédito para marcas** de até R$ 300 mil, como desconto sobre a comissão de 5% nas primeiras vendas de marca, até R$ 6 milhões.
- **Crédito de Ads** de até R$ 5.300, proporcional ao gasto em Sponsored Products.
- **Indicação:** R$ 1.000 por vendedor indicado (R$ 1.200 em SP).
- **Requisitos do FBA:**
  - CNPJ com NF-e, no Simples Nacional ou no Regime Normal.
  - Inscrição Estadual em SP, MG, PR, RJ, SC, RS, CE, DF, PE, BA, GO ou ES.
  - Fora desses estados, a operação passa pelo Programa de Filiais.
  - Tamanho padrão: até 45x35x20 cm e 9 kg.

### 2.3 Amazon Vantagens (webinar oficial H0ab_x1YIBY, 2026-10-14) [OFICIAL]
- **Amazon Vantagens:** 12x sem juros, taxa de 1,5%.
- **Amazon Mais Vantagens:** 12x sem juros mais 5% de desconto no Pix pago pela Amazon.
  - Taxa de 1,5% até 30/10/2026; 2,5% a partir de 31/10/2026.
  - Vale para produtos de R$ 40 a R$ 10 mil.
- **Efeito na Buy Box:** o preço com Pix (por exemplo R$ 95 num item de R$ 100) é o considerado na "oferta em destaque". O repasse ao vendedor é calculado sobre os R$ 100.
- Aumento de taxa é comunicado com pelo menos 30 dias de antecedência.

### 2.4 Catálogo, marca e leitura de mercado
- **Catálogo único:**
  - Produto de marca existente precisa entrar no anúncio que já existe e disputar a Buy Box.
  - Genérico sem marca cria anúncio do zero.
  - Fonte: CpeAKSyctRg, 2026-10-02 [PRÁTICA sobre regra; conferir no Seller Central].
- **Brand Registry** (venda.amazon.com.br/brand-registry) [OFICIAL]:
  - Exige marca fixada no produto ou na embalagem e marca registrada, em processo ou com pedido pendente "em alguns casos".
  - Dá acesso a A+, Brand Analytics, Sponsored Brands (mínimo de 3 produtos), Brand Store, Project Zero, Sponsored Display e Programe & Poupe.
- **Brand Analytics** (sell.amazon.com, EUA; mesma ferramenta no Seller Central BR via Brand Registry) [OFICIAL]. Relatórios:
  - Search Query Performance: impressões, cliques, carrinho e compra por termo.
  - Search Catalog Performance.
  - Top Search Terms: as três marcas e produtos de topo por termo.
  - Market Basket.
  - Repeat Purchase.
  - Demographics.
  - Customer Loyalty Analytics.
  - É o equivalente amazônico do painel de concorrência do ML. A diferença é que o share é por termo e por etapa do funil, não um ranking por apelido.
- **Promoções** (venda.amazon.com.br/promocoes) [OFICIAL]:
  - Oferta Relâmpago: 4 a 12 horas.
  - Oferta da Semana: 7 dias.
  - Cupom: até 90 dias, com desconto de 5% a 80% sobre o menor preço dos últimos 30 dias.
  - Nota mínima de 3 estrelas; a FAQ diz 3,5, o que é uma divergência interna.
  - Quarentena de 14 dias sem promoção. Programação com 1 semana de antecedência.
- **Calendário:** a Mega Oferta Amazon Prime teve a 4ª edição de 5 a 11/10/2026, só para membros Prime (Prime a R$ 19,90/mês ou R$ 166,80/ano). A Amazon cita mais de 300 centros logísticos nas 27 UFs (aboutamazon.com.br, 02/10/2026) [OFICIAL].

---

## 3. O que os melhores fazem (consenso, divergências, ids)

### 3.1 Perfil dos cases (todos autodeclarados)

| id | Operação | País | Tipo | Números declarados | Mostra tela? | Confiança |
|---|---|---|---|---|---|---|
| tpS__DSMMqo | Ângelo Mário (marca de fitas, mais uma de limpeza) | EUA (+ entrada no BR com air fryer) | [MARCA] importador | >US$ 1 mi/mês; ~500 SKUs; ~100 produtos; ~20 produtos = núcleo; 70 mil un./mês; 15 funcionários (Filipinas); US$ 100 mil/mês em ~1 ano | Não | C |
| nLM_JFURSTI | Josh Hadley | EUA | [MARCA] | >US$ 20 mi/ano; Amazon, Shopify e TikTok | Slides, sem dados da conta | C |
| Vl6KK7-lEz0 | Jamal Muse (3 exits) e corretor Guillaume Babin (Echelon, ex-SellerX) | EUA/Europa | [MARCA] | 1º exit em 2019, "sete dígitos"; estoque de "seis dígitos médios" no último | Não | C |
| 78sSkRh2crI | Grupo ROI (mentoria, prep center, contabilidade, agência) | BR | Majoritariamente [REVENDA], com marca própria em curso | 3 mil lojas de alunos; filtro de 20% de margem; buy box com 22% de margem; 70% em listagem própria | Não | C (N7: CTA e conflito de interesse) |
| 4Vvrft5eTDo | Mentorado de assessoria (Arthur Mundim) | BR | [REVENDA] genérico + "ampla concorrência" | R$ 15 mil em <30 dias; R$ 28 mil em estoque; margem de 22% a 27% | Não | C (N7) |
| 1fXOj1mcRuU | Ariadne Sousa | BR | [REVENDA]/importador | R$ 5 mi com um produto em 2023, margem de 25%, **no Mercado Livre** | Não | C (N7) |
| L380mHir7aA | Ajudo a Vender | BR | [REVENDA] de catálogo de fornecedor, DBA | Contestações em 5% a 10% das vendas | Não | C |
| CpeAKSyctRg | Bruno Capellete (mentor) | BR | ambos | Margem média de 8% na revenda dos grandes que mentora | Tela da busca | C |

### 3.2 Práticas com consenso (três ou mais fontes, ou case mais OBS)
- **Marca própria como destino final da operação.** Três fontes repetem a sequência "varejo → distribuidor → importador → fábrica ou marca":
  - tpS__DSMMqo: "marca própria é essencial".
  - kDF4gtMCAdo e 78sSkRh2crI: a mesma sequência, contada pelo apresentador.
  - CpeAKSyctRg: revenda de marca alheia com cerca de 8% de margem.
  - Os sinais oficiais apontam no mesmo sentido: crédito de R$ 300 mil para marcas e Sponsored Brands e Brand Analytics restritos a Brand Registry.
  - Ressalva: a tese vem de quem sobreviveu (viés de sobrevivente) e de vendedores de mentoria [PRÁTICA].
- **Lançar vários produtos, não apostar em um só.**
  - "Lance quatro", citando o dono da Zulay (tpS__DSMMqo).
  - Taxa de acerto de lançamentos perto de 60% como métrica, com pedidos iniciais pequenos (nLM_JFURSTI).
  - Vários SKUs de giro (`social/notas.md`, DdbwS4DO_MI).
- **Marketing de anúncio é a diferença entre os grandes.**
  - A ordem das imagens segue a dúvida do cliente; o time de criativos é fixo (tpS__DSMMqo).
  - Ângelo diz que grandes brasileiros têm boa operação e fraco marketing (opinião).
  - Os 10 ajustes de Brand Store (`social/notas.md`, DXSHDl4Dv5Q).
- **Ads como acelerador em fase de crescimento.**
  - Ângelo foi de 100 mil para 300 mil por mês ao dobrar o Ads, "no começo do PPC" (tpS__DSMMqo, sobre os EUA por volta de 2015).
  - Hoje a Amazon BR exige 3,5% de Ads para o subsídio FBA [OFICIAL].
  - Grupo ROI: Ads "indispensável" em listagem própria e dispensável em produto de catálogo com Buy Box (78sSkRh2crI).
- **FBA como padrão.**
  - A Amazon empurra o FBA com tarifa, Prime e comissão de 5% [OFICIAL].
  - Ângelo opera sem galpão nos EUA (tpS__DSMMqo).
  - Grupo ROI: cobertura de 30 a 45 dias de demanda no FBA (78sSkRh2crI).
  - Ângelo diz que, nos EUA, o estoque disponível influencia o ranking por localidade (opinião, sem teste).

### 3.3 Equipe, rotina e ferramentas
- **Ângelo, mais de US$ 1 mi/mês (tpS__DSMMqo):**
  - Board de líderes de área às segundas: gerente geral, logística, criativos (Brasil e Filipinas) e atendimento.
  - Pesquisa de produto com o sócio às terças; criativos às quartas.
  - O dono trabalha cerca de 3 horas por dia, de manhã.
  - Compradora/negociadora própria na China, mais um pequeno depósito consolidador pago por mês.
  - Ferramenta própria de vendas mais uma de terceiros, conferida várias vezes ao dia.
  - Decisão de lançamento: busca mensal do termo, conversão, número de concorrentes, viabilidade.
- **Josh Hadley (nLM_JFURSTI):**
  - Planejamento de compra é a função de "um dos melhores membros do time".
  - Manual de reposição revisto todo ano.
  - IA só com "controles e equilíbrios".
- **Corretor de M&A (Vl6KK7-lEz0):**
  - Comprador desconta dependência do fundador.
  - Recomenda cortar ferramentas duplicadas (três de reembolso FBA, duas de PPC com IA mais agência).
  - Preferência por freelancer qualificado e repassável.
  - Transição contratual típica: 20 horas no 1º mês e depois cerca de 10 horas por semana. No case, bastaram 30 minutos a cada 2 semanas.
- **Agência ou time interno:** o Grupo ROI lançou uma agência de Ads e SEO terceirizada (78sSkRh2crI). Os cases dos EUA preferem time próprio remoto. Não há dado comparativo [PRÁTICA].
- **Financeiro (SqoNj2DDRSU, consultora, 2026-06-02):**
  - Indicadores na ordem caixa → margem de contribuição diária → estoque.
  - Margem de contribuição bruta menos custos ocultos: devolução, Full, coleta e juros de antecipação.
  - Ler TACOS e não só ACOS.
  - Tirar a antecipação leva de 3 a 4 meses para o caixa normalizar [PRÁTICA, multicanal].

### 3.4 Multicanal
- **Preço por canal:** a margem de contribuição muda com a comissão de cada canal.
  - Fórmula: preço = custo ÷ (1 − comissão − imposto − margem-alvo).
  - Exemplo: R$ 50 de custo, 16% de comissão, 4% de imposto e 30% de margem dão R$ 100 (cZysnqICrkY) [PRÁTICA, método].
- **Divergência sobre preço alinhado:** o importador do case do ML perde competitividade na Amazon porque mantém o preço alinhado ao ML (iMR4J6w9woA, frente ML).
- **Divergência sobre ticket:** três fontes afirmam que o preço praticado na Amazon é mais alto pela menor concorrência. Exemplo: cabideiro a R$ 25 na Amazon e R$ 15 na Shopee (4Vvrft5eTDo; 78sSkRh2crI; rN4j4kZvkDg).
  - Em contraponto, a Amazon reduziu tarifas para baixar o ticket médio, segundo o mesmo praticante (4Vvrft5eTDo).
  - Não há dado de preço ponderado [PRÁTICA].
- **Conflito com 1P:** um fabricante saiu da Amazon quando ela passou a competir como 1P (0zdA5y8Y8B4, frente ML) [PRÁTICA].
  - Na OBS de café, os líderes são 1P [OBS].
- **Efeito TikTok → Amazon:**
  - Ângelo relata que, num produto lançado no TikTok Shop, cada 50 vendas no TikTok vinham com 50 na Amazon, porque a entrega é em 1 ou 2 dias (tpS__DSMMqo) [PRÁTICA, EUA].
  - A Marketplace Pulse mostra que 20% dos top 100 do TikTok Shop (EUA) estão no top 10 mil da Amazon, contra 4% no sentido inverso (10/09/2026) [DADO].
- **Ferramenta:** a Amazon anunciou em 24/09/2026 a gestão de eBay, Walmart, Shopify e TikTok Shop dentro do Seller Central, só nos EUA [DADO via Marketplace Pulse; não lançado no BR].

### 3.5 Divergências entre fontes
- **Tarifa "de quase 50% a 60%" da receita** (tpS__DSMMqo, EUA) contra comissão de 10% a 15% mais logística no BR [OFICIAL]. As bases são diferentes (EUA com FBA, Ads e armazenagem). Vira faixa, não média.
- **Investimento da Amazon no Brasil:**
  - "Plano de US$ 18 bilhões em 5 anos", ouvido "da diretoria" (78sSkRh2crI) [PRÁTICA, N8].
  - Contra "R$ 55 bilhões investidos" em 10 anos, publicado em 31/07/2025 (aboutamazon.com.br) [OFICIAL].
  - O valor futuro não aparece na página oficial.
- **Facilidade de ranquear só com SEO no BR** (78sSkRh2crI) contra a OBS de 8 dos 30 resultados de "café em grãos" serem patrocinados [OBS]. A busca em alimentos já é paga no topo.

---

## 4. Números de referência

| Métrica | Valor ou faixa | Fonte | Data | Tipo | Revenda/marca |
|---|---|---|---|---|---|
| Comissão Alimentos | 10% | venda.amazon.com.br/precos | atualiz. 20/01/2025 (pode estar superada) | OFICIAL | ambos |
| Comissão geral | 10% a 15% | idem | idem | OFICIAL | ambos |
| Tarifa por item (plano) | R$ 2 | idem | idem | OFICIAL | ambos |
| FBA, tarifa única | R$ 6/un. para preço ≥ R$ 79, com ≥ 3,5% em Ads | /cresca/fba | acesso 2026-10-14, sem data | OFICIAL | ambos |
| FBA, longo prazo | R$ 525/m³ após 365 dias | /precos | atualiz. 01/08/2025 (pode estar superada) | OFICIAL | ambos |
| DBA | R$ 4,50 / 6,50 / 6,75 por faixa de preço até R$ 78,99 | /precos | idem | OFICIAL | ambos |
| Comissão de lançamento Prime | 5% nas 100 primeiras un., até 120 dias | Recompensas | acesso 2026-10-14 | OFICIAL | ambos |
| Crédito de marca | até R$ 300 mil (5% sobre até R$ 6 mi) | Recompensas | idem | OFICIAL | [MARCA] |
| Mais Vantagens | 2,5% a partir de 31/10/2026 (1,5% antes); Pix 5% pago pela Amazon | H0ab_x1YIBY | 2026-10-14 | OFICIAL | ambos |
| Vendedores no BR | >100 mil parceiros | aboutamazon.com.br | 31/07/2025 | OFICIAL | — |
| Ads, crescimento global | +26% a/a; US$ 19,8 bi no tri | Release do 2T26 | 30/07/2026 | OFICIAL N2 | — |
| 3P seller services | +16% a/a; US$ 46,8 bi | idem | idem | OFICIAL N2 | — |
| Retenção de top sellers (EUA) | 68,6% em 12 meses; 49,6% em 3 anos | Marketplace Pulse | 09/07/2026 | DADO | — |
| China no top 10 mil (EUA) | 55,9% dos sellers; 28,6% do GMV | idem | idem | DADO | — |
| Concentração multicanal | 71% tiram ≥ 75% da receita na Amazon | Marketplace Pulse | 24/09/2026 | DADO | — |
| Revendedores em marca em declínio | 3 a 5 vezes mais que em marca líder | Jungle Scout | 2025 | DADO (método não publicado) | [MARCA] |
| Margem de revenda (Buy Box) | ~8% média; 20% a 22% "poucos e temporários" | CpeAKSyctRg | 2026-10-02 | PRÁTICA | [REVENDA] |
| Filtro de margem de mentoria | ≥ 20% | 78sSkRh2crI | 2026-08-18 | PRÁTICA (N7) | [REVENDA] |
| Cobertura de estoque | 30 a 45 dias (BR, revenda); 90 a 120 dias (EUA, marca importada) | 78sSkRh2crI; nLM_JFURSTI | 2026 | PRÁTICA | ambos |
| Giro de estoque | 4 a 6 por ano (fornecedor no exterior); 10 a 20 (fornecedor local) | nLM_JFURSTI | 2026-07-29 | PRÁTICA | [MARCA] |
| Teto de estoque | 12 meses; corta SKU que não vende o lote em 12 meses | nLM_JFURSTI | idem | PRÁTICA | ambos |
| Taxa de acerto de lançamento | ~60% | nLM_JFURSTI | idem | PRÁTICA | [MARCA] |
| Liquidação | 10 a 20 centavos por dólar investido; programa da Amazon a ~10% do valor | nLM_JFURSTI; tpS__DSMMqo | 2026 | PRÁTICA | ambos |
| Múltiplo de venda de conta (EUA) | 3 a 4 vezes o lucro anual (2 a 2,5 no início do mercado) | tpS__DSMMqo | 2026-07-23 | PRÁTICA | [MARCA] |
| Investimento por SKU de marca | R$ 10 mil a R$ 15 mil (suplemento nacional); ≥ R$ 50 mil (importado da China) | CpeAKSyctRg | 2026-10-02 | PRÁTICA | [MARCA] |
| Ganho de margem ao importar | +10 a 15 pontos de margem de contribuição (de 12-15% para ~30%) | rN4j4kZvkDg (trading que vende o serviço) | 2026-10-06 | PRÁTICA (conflito de interesse) | [REVENDA]/importador |
| Ciclo de importação | ~3 meses até chegar; ~5 meses de retorno do caixa | rN4j4kZvkDg | idem | PRÁTICA | importador |
| Taxa de devolução | 7% em eletrônico (EUA, 2014-15); ~1% nos alunos (BR) | tpS__DSMMqo; 78sSkRh2crI | 2026 | PRÁTICA | ambos |
| Contestações no DBA | 5% a 10% das vendas | L380mHir7aA | 2026-09-04 | PRÁTICA | [REVENDA] |

---

## 5. Alimentos, perecíveis e marca própria/indústria

- **Quem lidera café na Amazon BR** (OBS, 2026-10-14, `lideres.tsv`):
  - Orfeu grãos 1 kg: #1 em Café e 6º de toda Alimentos e Bebidas; 1P; 16.737 avaliações; R$ 129,21; variações de sabor e tamanho no mesmo anúncio; A+; cupom de app de R$ 20.
  - Coffee Mais Arara 250 g: 1P; 43% de desconto; selo "Escolha da Amazon"; mais de 4 mil compras no mês.
  - Baggio aromatizado 250 g: 1P; 10.981 avaliações; mais de 6 mil compras no mês.
  - Cápsulas (Nescafé, 3 Corações) ocupam cerca de 12 das 30 posições do top de Café.
- **Mix de alavancas dos líderes de café (OBS):**
  - Liderança vem com 1P, A+, variações num só ASIN, selo "Escolha da Amazon" ou "Mais vendido" e cupom.
  - A marca 3P em crescimento (Italle, FBA, 1.647 avaliações) usa Sponsored Products no topo, banner em página de concorrente e Programe e Poupe.
  - Na busca "café em grãos", 8 dos 30 resultados são patrocinados (posições 1 a 4 e 21 a 24), todos de marcas com menos avaliações que os orgânicos.
- **Ligação com caso oficial:** a marca Coffee++ (loja da Coffee Mais) aparece nas histórias oficiais da Amazon vendendo com fulfillment nos EUA (venda.amazon.com.br/historias). É o único case de café com selo oficial, mas sem números [OFICIAL].
- **Recompra:** Programe e Poupe está nos Lysoform e Italle observados [OBS] e é benefício do Brand Registry [OFICIAL]. O Brand Analytics tem relatório de Repeat Purchase.
  - Nenhuma fonte lida traz taxa de recompra de café na Amazon BR.
- **Comissão de Alimentos (10%)** é a menor da tabela. Com o FBA a R$ 6 para itens a partir de R$ 79, kit e pacote de 1 kg ou mais tendem a cair na faixa subsidiada; pacote de 250 g entra na tarifa por faixa (leitura da regra, não recomendação).
- **Validade e FBA:** as regras de vida útil mínima no recebimento e de remoção antes da validade estão em páginas do Seller Central que exigem login. Não foram lidas (sem evidência).
  - O único relato de preparação de item com validade é de cosmético de marca própria (`social/notas.md`, 7351820036966944006, 2024) [PRÁTICA, pode estar superada].
- **Indústria contra 1P:** em café, a indústria grande vende para a Amazon (1P) e não opera como 3P. O case do ML registra fabricante que saiu da Amazon por conflito com 1P (0zdA5y8Y8B4) [PRÁTICA].
- **Estoque de perecível:** a regra de "planejar ruptura no pico sazonal e subir preço quando o estoque acaba" (nLM_JFURSTI) vem de produto não perecível. Para alimento, o teto de cobertura é o prazo de validade menos a margem exigida pela Amazon (não verificada).

---

## 6. Erros comuns e mitos

**Erros documentados (o que aconteceu e o que veio depois)**

| Erro | O que veio depois | Fonte | Confiança |
|---|---|---|---|
| Defeito de lote (cabo detectado como não original) derrubou a nota de 4,8 para 4,2 | Estoque encalhado e descartado. Hoje a Amazon cobra descarte e oferece liquidação a ~10% do valor | tpS__DSMMqo [PRÁTICA, EUA] | C |
| Importação com antidumping (fita magnética dos EUA) | Multa e carta de crédito de US$ 50 mil presa por 5 anos. Mudança de fornecedor para o Vietnã, com vendas menores | tpS__DSMMqo | C |
| Compra de marca com conversão baixa (2019) | Ads caro sem retorno; o projeto não fechou | tpS__DSMMqo | C |
| Reposição baseada em 30 dias de pico da COVID e previsão no nível do produto-mãe (Thrasio) | 5 a 10 anos de estoque em SKUs; falência | nLM_JFURSTI [PRÁTICA, relato de terceiros] | C |
| Contestações de entrega e chargeback em 5% a 10% das vendas DBA, com o vendedor tendo de provar a entrega | Vendedor saiu da Amazon, que era seu canal de melhor margem | L380mHir7aA | C |
| Revenda com margem de contribuição de 15% e antecipação | Dívida de R$ 500 mil com faturamento de R$ 3 mi/mês; 8 meses de ajuste | SqoNj2DDRSU [multicanal] | C |
| Remessa grande ao Full no fim do mês em regime normal | ICMS destacado na remessa pesa no caixa | 6jtpl-y_iZw [PRÁTICA tributária] | C |
| Marca não registrada | Concorrente registra e derruba o anúncio pelo programa de proteção; pode bloquear a conta | kDF4gtMCAdo | C |

**Mitos e o que as fontes fortes mostram**
- **"Faturei 5 milhões com um produto na Amazon"** (título de 1fXOj1mcRuU): no próprio vídeo, o produto foi validado e vendido no Mercado Livre, com filtro Full, em 2023. É título enganoso, sinal fraco nº 7 (canal trocado).
- **"80% das compras vêm da busca e das duas primeiras fileiras"** e **"só de enviar pro FBA vendo 8 vezes mais"** (78sSkRh2crI): números sem base, num vídeo de captação de mentoria (sinais 1, 2 e 5).
- **"A Amazon zerou 100% das taxas"** (78sSkRh2crI): a página oficial mostra 30 dias de FBA grátis e tarifa de R$ 6 condicionada a 3,5% de Ads. A comissão continua [OFICIAL].
- **"Na Amazon dá para ranquear só com SEO, sem Ads"** (78sSkRh2crI): em café, metade do topo visível é patrocinada [OBS]. A própria Amazon condiciona o subsídio ao Ads [OFICIAL].
- **"Mais estoque no FBA melhora o ranking"** (tpS__DSMMqo, 78sSkRh2crI): afirmação de praticante, sem teste.
  - Em contraponto, há o custo de R$ 525/m³ após 365 dias [OFICIAL].
  - O operador de 8 dígitos trata excesso de estoque como risco existencial (nLM_JFURSTI).
- **"Mais de 50% dos vendedores da Amazon são chineses"** (tpS__DSMMqo): a Marketplace Pulse mede 55,9% no top 10 mil dos EUA, mas só 28,6% do GMV desse grupo. O número de sellers não equivale a share de vendas (sinal 10).
- **Cases de alunos (R$ 100 mi, 3 mil lojas, R$ 15 mil em 30 dias):** sem período, base nem medição independente. São release de marketing.

---

## 7. Revenda/importação x indústria/marca própria

**[REVENDA] (revenda de marca alheia, genérico, importação)**
- Produto de marca entra no catálogo existente: vende desde o 1º dia se tiver preço, mas vira leilão de Buy Box. Exemplo citado: 35 vendedores num kit de teclado (CpeAKSyctRg).
  - Margem de cerca de 8%.
  - Disputa com 1P e com a própria marca.
- Genérico exige criar o anúncio do zero e depende de Ads e SEO para aparecer (CpeAKSyctRg; 78sSkRh2crI).
- O Grupo ROI chama Buy Box de jogo "de relacionamento" (com fornecedor) e listagem própria de jogo "de ranqueamento"; diz operar 70% em listagem própria (78sSkRh2crI).
- O importador ganha margem de contribuição, segundo uma trading, mas imobiliza caixa por cerca de 5 meses (rN4j4kZvkDg).
  - Prática citada: validar no mercado nacional primeiro, com no máximo 10% do capital no produto-chave.
- O risco operacional mais citado no DBA é a contestação de entrega (L380mHir7aA).

**[MARCA] (indústria, marca própria)**
- Acesso exclusivo a Brand Registry, A+, Brand Store, Sponsored Brands, Brand Analytics (SQP, Market Basket, Repeat Purchase), Project Zero e Programe & Poupe [OFICIAL].
  - Crédito de até R$ 300 mil em comissão [OFICIAL].
- Equity e saída: a conta e a marca se vendem a cerca de 3 a 4 vezes o lucro anual nos EUA (tpS__DSMMqo).
  - O estoque é pago à parte do ágio (Vl6KK7-lEz0).
  - A dependência do fundador derruba o valuation.
- Variações (tamanho, pack, cor) ampliam o catálogo sobre o mesmo ativo: Ângelo foi de uma fita para cerca de 500 SKUs (tpS__DSMMqo). O líder de café também concentra sabores e tamanhos num ASIN [OBS].
- O risco específico é o 1P: a Amazon compra da indústria e revende. Em café, é o modelo dominante [OBS].
  - Para a indústria, a escolha entre 1P e 3P define quem controla o preço (sem dado oficial lido sobre os termos do 1P no Brasil).

**Vale para os dois**
- Estoque no nível do SKU, teto de 12 meses e plano de liquidação antes de precisar (nLM_JFURSTI).
- Margem de contribuição por canal e TACOS no lugar de ACOS isolado (SqoNj2DDRSU; cZysnqICrkY).
- O subsídio FBA a R$ 6 e a exigência de 3,5% de Ads mudam a conta de quem não anuncia [OFICIAL].

---

## 8. Tabela de afirmações

| id | Afirmação | Tipo | Fonte | Data | Confiança |
|---|---|---|---|---|---|
| A1 | Comissão de "Comidas e bebidas" na Amazon BR é 10% | OFICIAL | venda.amazon.com.br/precos | atualiz. 20/01/2025 (pode estar superada) | média |
| A2 | Plano Profissional: R$ 2 por item; mensalidade de R$ 19 a partir do 13º mês | OFICIAL | idem | idem | média |
| A3 | FBA: tarifa única de R$ 6 para preço ≥ R$ 79, coleta e armazenagem isentas, se investir ≥ 3,5% em Ads | OFICIAL | /cresca/fba; @vendacomamazon 2026-07-16 | 2026 | alta |
| A4 | FBA grátis por 30 dias para entrantes; extensão possível até 31/01/2027 | OFICIAL | Recompensas do Vendedor | acesso 2026-10-14 | média |
| A5 | Comissão de 5% nas 100 primeiras unidades de item novo elegível ao Prime, até 120 dias | OFICIAL | /cresca/fba; Recompensas | idem | média |
| A6 | Crédito de até R$ 300 mil para donos de marca, sobre comissão de 5% até R$ 6 mi em vendas | OFICIAL | Recompensas | idem | média |
| A7 | Armazenagem FBA de longo prazo: R$ 525/m³ após 365 dias | OFICIAL | /precos | atualiz. 01/08/2025 (pode estar superada) | média |
| A8 | DBA: R$ 4,50 (<R$ 30), R$ 6,50 (R$ 30-49,99), R$ 6,75 (R$ 50-78,99) | OFICIAL | /precos | idem | média |
| A9 | Amazon Mais Vantagens passa de 1,5% para 2,5% em 31/10/2026; Pix de 5% pago pela Amazon conta para a oferta em destaque | OFICIAL | H0ab_x1YIBY | 2026-10-14 | média |
| A10 | Brand Registry aceita marca com pedido pendente "em alguns casos" | OFICIAL | /brand-registry | acesso 2026-10-14 | média |
| A11 | Sponsored Brands e Stores exigem Brand Registry; Sponsored Brands exige ≥ 3 produtos | OFICIAL | /publicidade | idem | média |
| A12 | Cupom: desconto de 5% a 80% sobre o menor preço de 30 dias; 14 dias sem promoção antes | OFICIAL | /promocoes | idem | média |
| A13 | Ads cresceu 26% a/a no 2T26 (US$ 19,8 bi); 3P seller services, 16% | OFICIAL (N2) | Release Amazon | 30/07/2026 | alta |
| A14 | Mais de 100 mil vendedores parceiros no BR; R$ 55 bi investidos em 10 anos | OFICIAL | aboutamazon.com.br | 31/07/2025 | média |
| A15 | O #1 de Café é Orfeu 1 kg, 1P, com 16.737 avaliações e >10 mil compras no mês | OBS | lideres.tsv | 2026-10-14 | média |
| A16 | 8 dos 30 resultados de "café em grãos" são patrocinados | OBS | lideres.tsv | 2026-10-14 | média |
| A17 | 68,6% dos top 10 mil da Amazon.com estavam no ranking 12 meses antes | DADO | Marketplace Pulse | 09/07/2026 | média |
| A18 | 71% dos vendedores Amazon-first tiram ≥ 75% da receita de marketplace na Amazon | DADO | Marketplace Pulse | 24/09/2026 | baixa |
| A19 | Marcas em declínio têm 3 a 5 vezes mais revendedores | DADO | Jungle Scout | 2025 | baixa |
| A20 | Operação de >US$ 1 mi/mês com ~500 SKUs, 70 mil un./mês e 15 funcionários remotos | PRÁTICA | tpS__DSMMqo | 2026-07-23 | baixa |
| A21 | Regras de estoque: 90-120 dias de cobertura, giro de 4-6, teto de 12 meses, corte em 12 meses | PRÁTICA | nLM_JFURSTI | 2026-07-29 | baixa |
| A22 | Thrasio quebrou com 5 a 10 anos de estoque por reposição baseada em 30 dias | PRÁTICA | nLM_JFURSTI | 2026-07-29 | baixa |
| A23 | Margem média de revenda com Buy Box de ~8% | PRÁTICA | CpeAKSyctRg | 2026-10-02 | baixa |
| A24 | Contestações em 5% a 10% das vendas DBA levaram vendedor a sair | PRÁTICA | L380mHir7aA | 2026-09-04 | baixa |
| A25 | "R$ 5 mi com um produto" do título é um case do Mercado Livre | PRÁTICA (mito) | 1fXOj1mcRuU | 2026-08-20 | média |
| A26 | Múltiplo de venda de conta Amazon de 3 a 4 vezes o lucro anual | PRÁTICA | tpS__DSMMqo | 2026-07-23 | baixa |
| A27 | Na venda da empresa, o estoque é pago à parte do ágio | PRÁTICA | Vl6KK7-lEz0 | 2026-09-08 | baixa |
| A28 | INPI: exame prioritário para vendedor de marketplace em 90-180 dias (Portaria 66/2026) | PRÁTICA (regra de terceiro) | kDF4gtMCAdo | 2026-06-09 | baixa |
| A29 | Importar eleva a margem de contribuição em 10 a 15 pontos | PRÁTICA (conflito) | rN4j4kZvkDg | 2026-10-06 | baixa |
| A30 | Reforma tributária: CBS plena em 2027; ICMS cai 10% ao ano até 2032; split payment | PRÁTICA (regra de terceiro) | 6jtpl-y_iZw | 2026-08-12 | baixa |
| A31 | Prime custa R$ 19,90/mês; Mega Oferta Prime de 5 a 11/10/2026 | OFICIAL | aboutamazon.com.br | 02/10/2026 | alta |

---

## 9. Lacunas

- **Ranking de vendedores por categoria na Amazon BR e mudança em 12 meses:** não há painel público equivalente ao "Análise de mercado" do ML.
  - O Brand Analytics é restrito ao dono da marca.
  - Só existe a foto de 2026-10-14 (`lideres.tsv`). Sem série histórica, a mudança de liderança fica "sem evidência".
- **Case brasileiro de Amazon com número verificável:** nenhum. Os cases oficiais não têm métricas. Os de mentoria não têm período nem base.
- **Benchmarks de Ads por categoria no BR** (ACOS, TACOS, CPC, conversão de alimentos): não lidos.
  - Jungle Scout 2026 e Pacvue ficam atrás de formulário.
  - Perpetua, SmartScout, Helium 10 e Nubimetrics Amazon BR não foram consultados (cota de busca esgotada).
- **Regras de validade no FBA e de alimentos** (vida útil mínima, lote, Anvisa): páginas do Seller Central com login. Sem evidência.
- **Termos do 1P para a indústria no Brasil** (margem cobrada pela Amazon, fundos de marketing): sem fonte.
- **Datas de início e fim do incentivo dos 3,5%** e a consequência de não atingir a meta: a página oficial não traz. Os detalhes vêm de transcrição automática do canal oficial.
- **Faturamento da Amazon Brasil e share por categoria:** o balanço da Amazon não separa o Brasil. Não há NIQ Ebit lido.
- **Divergências internas da página de preços:** comissão mínima (R$ 1 ou R$ 2) e o limiar de frete grátis (a extração mostrou "acima de R$ 19" em um trecho, contra R$ 79 no resto).
- **Efeito causal do estoque no ranking e do Ads no orgânico:** nenhuma fonte com teste de pausa ou holdout.
- **Gestão multicanal da Amazon (Seller Central para outros marketplaces):** só anunciada para os EUA.

---

## 10. Verificação (2026-10-14)

Método: releitura das páginas oficiais de venda.amazon.com.br em 2026-10-14. A cota de buscas na web acabou, então não houve busca por fonte mais recente nem acesso ao Seller Central (exige login). R2 e R9 ficam sem fonte oficial escrita por isso. Todas as regras abaixo são [OFICIAL]. As páginas de tarifa têm data própria (comissões 20/01/2025, FBA 01/08/2025), mais de 6 meses: "pode estar superada".

| id | veredito | fonte oficial (URL) | observação |
|---|---|---|---|
| R1 | CONFIRMADA | https://venda.amazon.com.br/cresca/fba | A página traz tarifa única de R$ 6 para preço igual ou superior a R$ 79, com isenção de coleta e armazenagem, e exige no mínimo 3,5% da receita dos produtos elegíveis em anúncios patrocinados. A tarifa é descrita para contas existentes; conta nova tem 30 dias de FBA grátis. A página não informa início nem fim da oferta. |
| R2 | SEM FONTE OFICIAL | https://venda.amazon.com.br/cresca/fba (não detalha) | A página oficial não traz regra de transição, nem corte em 01/04/2026, nem prazo de 30 dias, nem "mais 1 ponto". Só há o TikTok @vendacomamazon por transcrição automática. Não confirmar o número; a regra detalhada fica no Seller Central (não lido). |
| R3 | CONFIRMADA (pode estar superada) | https://venda.amazon.com.br/precos | Comidas e bebidas 10% e categoria padrão 15%, com "comissões atualizadas em 20/01/2025". Mínimo: texto diz R$ 1,00 e a tabela traz R$ 2,00, sem limite claro entre os grupos (divergência real). A faixa intermediária de 12% a 14% não foi re-extraída nesta verificação. |
| R4 | CONFIRMADA | https://venda.amazon.com.br/precos | Profissional: R$ 2,00 por item mais comissão, 1º ano grátis e R$ 19,00/mês a partir do 13º mês. Individual: sem mensalidade, R$ 2,00 por item. Página de 20/01/2025: pode estar superada. |
| R5 | CONFIRMADA (pode estar superada) | https://venda.amazon.com.br/precos | R$ 75,00/m³ abaixo de 10 mil cm³; R$ 37,50/m³ com 10 mil cm³ ou mais; longo prazo (mais de 365 dias) R$ 525,00/m³ em adição à mensal. Tarifas "atualizadas em 01/08/2025". |
| R6 | CONFIRMADA (pode estar superada) | https://venda.amazon.com.br/precos | Faixas R$ 4,50 (abaixo de R$ 30), R$ 6,50 (R$ 30 a 49,99) e R$ 6,75 (R$ 50 a 78,99) conferem. A tabela acima de R$ 79 por estado e peso está em arquivo para download, não lido. A extração mostrou um trecho "Acima de R$ 19, com frete grátis", divergência a conferir. |
| R7 | CONFIRMADA | https://venda.amazon.com.br/cresca/programa-de-recompensas-do-vendedor | 5% nas primeiras 100 unidades de tamanho padrão ou 50 extragrandes, até 120 dias, para itens FBA e FBA Onsite. FBA grátis por 30 dias para quem entra, com extensão possível até 31/01/2027. A isenção de 30 dias para entrantes vale para preço de R$ 79 ou mais; quem já usa FBA tem coleta e armazenagem zeradas em qualquer preço. Termos completos no Seller Central. |
| R8 | CONFIRMADA | https://venda.amazon.com.br/cresca/programa-de-recompensas-do-vendedor | Crédito antecipado de R$ 300.000 como benefício de dono de marca, funcionando como desconto na comissão de 5% sobre as primeiras R$ 6 milhões em vendas elegíveis (FBA ou ofertas enviadas pelo vendedor). Sem data de início/fim. |
| R9 | SEM FONTE OFICIAL | nenhuma página escrita lida; só o webinar H0ab_x1YIBY | Nenhuma página oficial lida nesta verificação traz 1,5% para 2,5% em 31/10/2026, Pix de 5% pago pela Amazon ou o efeito na Buy Box. Não foi possível buscar o comunicado escrito (cota de busca esgotada). Não confirmar até achar comunicado ou Seller Central. |
| R10 | CONFIRMADA (com ressalva) | https://venda.amazon.com.br/brand-registry e https://venda.amazon.com.br/publicidade | Brand Registry: marca "registrada (ou em processo de registro)"; a FAQ restringe o pedido pendente a "alguns casos", sem dizer quais. Sponsored Brands: exige Brand Registry e pelo menos três produtos; a FAQ pede marca registrada ativa. Stores também exigem Brand Registry. |
| R11 | CONFIRMADA (com ressalva) | https://venda.amazon.com.br/promocoes | Cupom até 90 dias e produto sem oferta nos últimos 14 dias conferem. A base do desconto é inconsistente na própria página: "valor original" em uma passagem e menor preço dos 30 dias na tabela. Nota: 3 estrelas na lista de critérios; 3,5 na FAQ (nota do vendedor, com ao menos 5 avaliações). |
| R12 | CONFIRMADA | https://venda.amazon.com.br/cresca/fba | CNPJ ativo na Sefaz para NF-e; Simples Nacional ou Regime Normal; endereço e IE em SP, MG, PR, RJ, SC, RS, CE, DF, PE, BA, GO ou ES; Programa de Filiais para os demais. Há condições especiais para ES e SC, não descritas, e endereço de CD oferecido para filial em MG e RJ. |

Resumo: 10 confirmadas, 0 contestadas, 2 sem fonte oficial (R2, R9). Nenhuma foi contestada por fonte oficial, mas R2 e R9 não devem ser citadas como regra até haver comunicado escrito.

## 11. Verificação pelo navegador (2026-10-15)

Método: Chrome renderizando JavaScript; leitura das páginas públicas de ajuda (amazon.com.br/gp/help e ajuda do Seller Central, só leitura), advertising.amazon.com/pt-br e venda.amazon.com.br. Sem captcha. Páginas sem data visível (s/d).

| id | veredito | fonte oficial | observação |
|---|---|---|---|
| R2 | PARCIAL | https://sellercentral.amazon.com.br/help/hub/reference/G201112670 | Confirmado: o corte é para contas que usavam FBA antes de 1º/04/2026. A meta é 3,5% da receita em Ads ou +1 ponto sobre abril de 2026, com renovação mensal até 31/01/2027 e 1ª avaliação de 1 a 19/07. "Atingir 3,5% em 30 dias" não aparece: os 30 dias são a isenção total para novos vendedores do FBA. |
| R9 | PARCIAL | https://sellercentral.amazon.com.br/help/hub/reference/GR467L2LLXHTQMYP | Confirmado: Mais Vantagens custa 2,5%, com tarifa promocional de 1,5% de 30/09 a 30/10/2026. O desconto de 5% no Pix é financiado pela Amazon e o vendedor recebe o preço cheio. O Amazon Vantagens custa 1,5%. Os termos não falam de efeito na oferta em destaque. |
| R10 | CONFIRMADA | https://sellercentral.amazon.com.br/help/hub/reference/G202130410 ; https://venda.amazon.com.br/publicidade | Ressalva resolvida: a ajuda do Seller Central aceita pedido pendente como regra geral, sem o "em alguns casos" da página comercial. Sponsored Brands exige Brand Registry e 3 produtos (rodada anterior, /publicidade). |
| R11 | CONTESTADA | https://sellercentral.amazon.com.br/help/hub/reference/GJHCPEFJ5JJQD52D ; https://sellercentral.amazon.com.br/help/hub/reference/G363YLQW4NB5L38V | Seller Central: o cupom padrão termina em até 30 dias (a página comercial diz 90) e o desconto na planilha vai de 5% a 50%. A base é o "preço anterior ou preço sugerido". Nota: vendedor com pelo menos 3,5 e produto com 5 ou mais avaliações com pelo menos 3 estrelas, então os dois números valem em níveis diferentes. Não reconfirmei a regra de 14 dias. |
