# Rodada 2 · Camada de dados (N4/N5): Mercado Livre

Frente "dados-mercado" · coleta em 2026-10-15 · fecha LACUNAS §0.3, §0.6, §0.7 e §4 itens 25 a 29.

**Método.** Foram feitas 20 buscas na web (o teto da cota). O resto saiu de leitura direta por WebFetch e curl: dois PDFs da NIQ Ebit, a carta 8-K 2T26 da MELI, o blog e os cases da Lett, o PDF do Brand Footprint 2026, o RSS e posts da Nubimetrics e a API pública `/categories` do ML.

Não houve login, formulário nem aceite de termos. Páginas com 403 ou formulário foram registradas como tal e deixadas de lado. Todas as datas de acesso são 2026-10-15.

**Pesquisa neutra.** Este arquivo descreve o mercado e a plataforma, não uma empresa específica.

**Siglas de tipo:**
- [OFICIAL]: dado da própria plataforma (página, API ou declaração).
- [N2]: balanço ou documento regulatório.
- [DADO]: estudo ou painel de terceiro.
- [CASE]: case de fornecedor ou marca.
- [PRÁTICA]: regra prática de praticante.

**Confiança:**
- A: fonte primária com método.
- B: amostra declarada, mas lida via resumo ou com cobertura incompleta.
- C: sem método ou autodeclarado.

---

## Resumo

1. **A camada Dados deixa de estar vazia (§0.3).** Há agora quatro estudos N4 com amostra ou método declarado sobre o e-commerce brasileiro:
   - NIQ Ebit Webshoppers 51: dados transacionais de lojas conveniadas mais pesquisa no checkout.
   - Worldpanel by Numerator, Consumer Insights 2026: mais de 10 mil lares.
   - Worldpanel, Brand Footprint 2026: mais de 11.300 lares e mais de 400 marcas.
   - Lett, E-commerce Quality Index 2024: cerca de 700 a 750 mil páginas ou ofertas.

   Nenhum deles abre GMV por plataforma. A participação do ML só existe como estimativa de banco ou consultoria, sem método publicado. Ver R2-DAD-01 a 09 e 12 a 13. Isso atende ao critério "ao menos um estudo N4 com amostra declarada" no nível do mercado, não no nível do ML.

2. **Peso das plataformas: agora há uma faixa, ainda sem método (item 25; Shopee D20).**

   | Fonte | Ano | ML | Shopee | Amazon |
   |---|---|---|---|---|
   | UBS BB | 2025 | 42% (cerca de R$185 bi) | 19% (cerca de R$86 bi) | cerca de 11% |
   | IRTT | 2024 | R$138,9 bi | R$40 bi | R$39 bi |

   A liderança do ML é o único ponto de consenso. O tamanho do mercado varia de R$235,5 bi (ABComm, 2025) a R$450 bi (UBS, 2025), conforme o método. Ver R2-DAD-06, 07 e 09.

3. **Alimentos é a categoria menos digitalizada do FMCG (item 25; ALIM Q3).**
   - **Fatia online:** 1,4% do valor de Alimentos é vendido online, contra 8,3% em H&B (NIQ, 2024).
   - **Ocasiões e penetração:** o online responde por só 2% das ocasiões de compra de FMCG, mas já chega a 45,4% dos lares.
   - **Lacuna de frequência:** o desafio declarado é transformar experimentação em recorrência.
   - **Crescimento recente:** a compra de abastecimento online cresceu 94%.

   Ver R2-DAD-02, 03, 12 e 13.

4. **Recompra e frequência: proxies novos, sem taxa de recompra pública (item 29; ALIM Q4).**
   - **8-K 2T26:**
     - itens por comprador no Brasil +19% a/a;
     - DAU cresce mais rápido que MAU todo trimestre desde a mudança de frete;
     - +10 p.p. de usuários comprando em 3 ou mais categorias;
     - coortes novas com retenção maior.
   - **Executiva do ML:** supermercado com 1 em cada 4 compradores novo na categoria e botão de recompra.
   - **ABIC e Kantar:** não publicam recompra por canal.

   Ver R2-DAD-11, 15 e 14.

5. **Prateleira digital: o case 3 Corações/Lett foi encontrado e não serve como case auditável do ML (item 27; ALIM Q3; §0.7).**
   - **Página da própria Lett:** +56% de sell-out em cafeteiras e cápsulas, em Carrefour e GPA, sem período nem base.
   - **Imprensa:** outra versão, de 5 meses, com cápsulas +11% e uma cafeteira +81%.
   - **Relação com o ML:** o ML não aparece no case.

   O único case de prateleira digital no ML com número é o da Ypê/Lett (conversão de 15% para 43% em um SKU, em 6 meses). Ele também é autodeclarado e sem grupo de controle. Ver R2-DAD-19 e 20.

6. **Ruptura com número e tempo de recuperação: primeiro dado com desenho de painel (LOG Q7; ALIM Q3; consolidado §7 item 10).** Segundo a Lett, um dia de ruptura derruba do top 30:
   - 46% dos itens que estavam no top 5;
   - mais de 64% em café, limpeza, snacks e bebidas;
   - 39% em marketplaces e pure players.

   Na volta do estoque, 37,9% retornam ao top 5 no 1º dia e 59% no 2º. Em cerca de 7% dos dias havia anúncio pago de produto indisponível. A amostra não está declarada no resumo público. Ver R2-DAD-17.

7. **Ads: segue sem benchmark público com amostra para o ML-BR (item 26; ADS Q7; §0.6).**
   - **Ads/GMV:** a carta 2T26 confirma que a MELI não divulga essa razão. Ela informa que o Mercado Ads passou de 10% do mercado de publicidade digital da América Latina. Isso mantém aberta a afirmação de cerca de 2,6% (só fonte secundária). Ver R2-DAD-10.
   - **Amazon Ads:** liberou benchmarks por categoria no Brasil em 18/05/2026, mas só dentro do console, que exige login. Ver R2-DAD-23.
   - **Portais bloqueados:** o portal público do Mercado Ads e o Pacvue Q1 2026 deram 403.

8. **Concentração por categoria: não mensurável sem login (item 28; MIX Q3; CASES Q1 e Q7).**
   - **API pública:** `/sites/MLB/search` responde 403, `/highlights` 401 e `/trends` 403. Só `/categories` segue pública: café tem cerca de 39 a 40 mil anúncios e cápsulas cerca de 16 a 17 mil. Ver R2-DAD-25.
   - **Nubimetrics:** dá apenas a fatia de vendedores Platinum em categorias "saturadas", de 63% a 72%, sem dado de café. Ver R2-DAD-24.

---

## Achados

### (a) Estudos de mercado: GMV, participação, conversão e alimentos (item 25)

**NIQ Ebit Webshoppers 51, versão Free** (PDF publicado em abr/2025, dados de 2024). Fonte: `https://develop.nielseniq.com/wp-content/uploads/sites/4/2025/04/NIQ-E-commerce-Webshoppers_Free_-Ed.51.pdf`.

- **Método:**
  - dados transacionais de lojas conveniadas NIQ Ebit, captados automaticamente no pedido;
  - pesquisa no checkout e pesquisa de entrega por e-mail;
  - 12 categorias, com café listado como subcategoria de Alimentos e Bebidas.
- **Ressalva de cobertura:** uma nota de rodapé diz que um gráfico não considera vendas de Meli para categorias não FMCG, nem a operação 3P da Amazon. Logo, a cobertura dos marketplaces é parcial.
- **Mercado total:** GMV de R$351,4 bi em 2024, +19,1% sobre os R$295,1 bi de 2023. Shoppers ativos passaram de 108,4 mi para 125,6 mi.
- **Participação do online no FMCG (cerca de 80 categorias omnichannel), 2023 → 2024:**

  | Cesta | 2023 | 2024 |
  |---|---|---|
  | Total FMCG | 4,1% | 4,3% |
  | H&B | 7,2% | 8,3% |
  | Bebidas | 2,5% | 2,4% |
  | Alimentos | 1,2% | 1,4% |
  | Limpeza | 1,2% | 1,6% |

- **Missão de compra:** "Abastecimento & Reposição" é a missão principal, com cerca de 37% a 44% das intenções por trimestre. Alimentos e Bebidas, Saúde e Perfumaria são as categorias mais importantes para essa missão.
- **Alimentos e Bebidas por tipo de operação, 2024:** +41,9% de GMV nos pure players contra −11,3% nos brick & click.
- **Black Friday 2024:** Alimentos e Bebidas foi a 8ª categoria em intenção (9,8%) e a 4ª em compra realizada (14,1%). Fonte: pesquisa ad hoc de dez/2024.

**Confi/Neotrust com E-commerce Brasil, relatório "Da Compra à Confiança"** (GiroNews de 29/07/2026 e Portal IN de 28/07/2026).
- **1º semestre de 2026:**
  - faturamento de R$208,4 bi (+16,9%);
  - 756,7 mi de pedidos (+34,8%);
  - tíquete de R$275,50 (−13,3%);
  - itens por pedido de 2,25 para 1,97.
- **Projeção para 2026:** R$462,5 bi.
- **Lacunas:** a imprensa não publica a metodologia nem a abertura por marketplace ou por alimentos.

**UBS BB** (Money Times, 19/03/2026, `https://www.moneytimes.com.br/r-450-bilhoes-em-jogo-o-que-esperar-do-e-commerce-brasileiro-em-2026-segundo-o-ubs-bb-lmrs/`).
- **2025:** GMV de cerca de R$450 bi (+23%).
- **Participações:** ML 42% (cerca de R$185 bi), Shopee 19% (cerca de R$86 bi, +45%), Amazon cerca de 11%.
- **2026:** TikTok Shop com cerca de 1,6% estimado.
- **Método:** o texto não informa premissas ("estimamos").

**IRTT, continuidade dos estudos da SBVC** (via YAV, 20/05/2026, `https://yav.com.br/blog/maiores-empresas-ecommerce-brasil/`).

| Empresa | GMV 2024 estimado |
|---|---|
| ML | R$138,9 bi |
| Magalu | R$46,1 bi |
| Shopee | R$40 bi |
| Amazon | R$39 bi |
| Casas Bahia | R$16,6 bi |
| Shein | R$15 bi |

A própria fonte diz que os valores "oscilam entre relatórios". O post também cita a ABComm: R$235,5 bi em 2025. O post é de uma consultoria com serviço relacionado, e o PDF do IRTT não foi lido.

**Histórico, só para ordem de grandeza.** SBVC, 9ª edição, com dados NIQ de 2022 (Central do Varejo): os 5 maiores marketplaces somavam cerca de 78% do faturamento online, e o ML R$80,5 bi.

**Conversion, Relatório Setores do E-commerce.**
- **Fim da série:** a série acabou na edição de janeiro de 2026 (post de 28/01/2026, `https://www.conversion.com.br/blog/fim-do-relatorio-setores-ecommerce`).
- **Método:** Similarweb, mais de 2.000 sites, 18 categorias.
- **Acesso:** o PDF exige formulário, que não foi preenchido.
- **Dado público de dez/2025:** 33,6 bi de acessos em 12 meses, −5,3% no mês.

**Conversão.** Nenhum estudo público traz a taxa de conversão do ML. A única informação é a variação de +1,1 p.p. a/a no 2T26 (8-K, já em [cases A5]).

**Share of mind (peso das plataformas, sinal fraco).** NIQ Ebit, junho de 2026, 1.550 consumidores, via Economic News Brasil de 08/10/2026. Lembrança de loja para brinquedos: Amazon 27,6%, ML 22,6% e Shopee 15,7%.

### (b) Benchmarks de Ads (item 26)

- **MELI 8-K 2T26** (05/08/2026, Ex-99.1, sec.gov …000109959026000021), [N2]:
  - receita de Ads +62% a/a, sem efeito de câmbio;
  - "surpassed 10% share of the digital advertising market in Latin America";
  - Ads/GMV, *ad penetration* e valor absoluto não são divulgados;
  - a carta liga o aumento de itens do dia a dia, de preço baixo, à demanda por produtos de anúncio.
- **Benchmarks públicos com amostra para Mercado Ads:** nenhum encontrado.
  - O portal `publicidade.mercadolivre.com.br` deu 403.
  - `ads.mercadolivre.com.br` redireciona para verificação de conta, o que significa que exige login.
- **Mercado Ads, conteúdo de marca no Meio & Mensagem** (sem data visível; cita dados de 2021). Os números são autodeclarados:
  - cerca de 100 mil anunciantes;
  - mais de 135 mi de usuários únicos por mês na América Latina;
  - meta-análise da Kantar com mais de 200 campanhas no ML: +52% de awareness e cerca de 40% a mais de intenção de compra que a média de outras mídias.

  A meta-análise não informa período nem contratante. Os números são de topo de funil, sem CPC, CTR nem ACOS.
- **Amazon Ads** (18/05/2026, `https://advertising.amazon.com/pt-br/resources/whats-new/benchmarks-reporting-now-generally-available-worldwide`):
  - relatórios de benchmark por categoria, comparando com marcas semelhantes, com o Brasil incluído;
  - métricas: CTR, CPC, CPM, compras de clientes novos para a marca e métricas de vídeo;
  - acesso só pelo console ou pela API, o que exige login;
  - ROAS e CVR não estão na lista.
- **Pacvue, 2026 Q1 Retail Media Benchmark:** 403 na leitura direta. O resumo de busca indica cobertura só dos EUA (Amazon, Walmart, Instacart, Target). Não serve para o BR.
- **Regras práticas de blog** (Jaguarsheet, sem amostra), [PRÁTICA] C:
  - ACOS de 5% é "excelente", 15% é "bom" na maioria das categorias e 50% é "preocupante";
  - o ACOS de anúncios da mesma campanha varia de cerca de 3% a 40%.

  Não substituem benchmark.
- **Ligação com ruptura (Lett, 2025):** em cerca de 7% dos dias, ou cerca de 26 dias por ano, havia anúncios pagos de produtos indisponíveis. É um sinal de desperdício de mídia ligado à ruptura. Ver (c).

### (c) Prateleira digital de alimentos e cases (item 27)

**Lett, E-commerce Quality Index 2024.**
- **Fontes:** Mercado & Consumo de 13/11/2024 e blog da Lett de 03/12/2024 (`https://dcx.lett.digital/eqi-2024/`).
- **Ruptura:** 30,5% em jan–set/2024, +3,8 p.p. a/a.
  - Alimentos e Bebidas teve a maior alta: +3,9 p.p.
  - Marketplaces e pure players: −1,6 p.p.
  - Brick & click: +4 p.p.
- **Vendedores 3P:** 41% das ofertas não estariam disponíveis sem os vendedores 3P.
- **Amostra divergente:**
  - Mercado & Consumo: "748 mil páginas" em 16 e-commerces;
  - Lett: "700 mil ofertas em 3.900 lojas".
- **Acesso:** o estudo completo exige formulário.

**Lett, ruptura e visibilidade** (Mercado & Consumo, 13/05/2025).
- **Queda após 1 dia de ruptura:** 46% dos itens do top 5 saem do top 30.
- **Por categoria:**
  - café, limpeza, snacks e bebidas: mais de 64%;
  - leite e nutrição infantil, chocolates, molhos e suplementos: 38%.
- **Por canal:** brick & click de alimentos 46%; marketplaces e pure players 39%.
- **Recuperação:** 37,9% voltam ao top 5 no 1º dia e 59% no 2º.
- **Ressalvas:** a amostra e o método de medir a posição não estão no texto. O ML não é citado pelo nome.

**Lett, sazonalidade** (GiroNews, 24/11/2025; dados diários de out/2024 a set/2025).
- **Ruptura média:** Black Friday 30%; Carnaval e Páscoa até 50%.
- **Duração média do estoque:** Bebidas 6,68 dias; Alimentos 5,85 dias.
- **Ressalva:** a amostra não foi informada.

**Case 3 Corações/Lett** (o case citado pelo protocolo).
- **Página da Lett** (22/04/2025, `https://dcx.lett.digital/case-3coracoes-cafeteiras/`):
  - +56% de sell-out em cafeteiras e cápsulas;
  - varejistas: Carrefour e GPA;
  - pilares: conteúdo, disponibilidade e sortimento;
  - sem período, sem base e sem KPIs com valor.
- **Baguete** (16/06/2025):
  - em 5 meses: cápsulas +11%, um modelo de cafeteira +81%, imagens secundárias +27% e cafeteiras no Carrefour +56%;
  - não há base de comparação.
- **Conclusão:** as duas versões não batem entre si. O ML não aparece. Não há share of search, ruptura nem content score com valor.

**Case Ypê/Lett no ML** (GiroNews, 16/01/2026, `https://gironews.com/informacoes-de-fornecedores/apos-projeto-de-otimizacao-ype-registra-alta-de-28-na-taxa-de-conversao-de-seus-anuncios-no-mercado-livre/`).
- **Resultado:** a conversão do SKU Tixan Ypê XMax, na loja oficial, passou de 15% para 43% em seis meses (+28 p.p.).
- **O que mudou:**
  - título com palavras-chave;
  - descrição de até 251 palavras;
  - *hero image* e imagens secundárias;
  - vídeos.
- **Outras métricas:** qualidade de conteúdo +8%; share of search "ampliado", sem número.
- **Ressalvas:** é um único SKU, sem controle nem sazonalidade isolada.

**Case JDE/Lett, café e chá** (GiroNews, 01/07/2025).
- **Vendas:** e-commerce +45% em 2024 contra 2023.
- **Execução:** "Loja Perfeita" de 45% para 67% entre julho e setembro; share of voice +26%.
- **Ressalva:** o texto não cita varejista.

**Case Nestlé Cafés/Lett na Amazon** (08/04/2025, `https://dcx.lett.digital/case-nestle-cafes/`). Sell-out +80% em 3 meses. Mais de 30 itens passaram a ter destaque na busca "Café". Não há base.

**Supermercado no ML**, segundo uma executiva do ML na imprensa (Meio & Mensagem e Mercado & Consumo, 25/02/2025):
- vendas da categoria +77% em 2024 contra 2023;
- 18 mi de buscas por mês;
- 1 em cada 4 compradores novo na categoria;
- sortimento +74% em 6 meses;
- 80% dos recorrentes entregues em até 48 h;
- BBB 25: GMV +82% no dia de estreia contra o mesmo dia do ano anterior, com café torrado entre os 3 itens mais vendidos.

O título da matéria diz 84%, e o corpo, 82%.

**Profitero e Nielsen Digital Shelf com recorte BR:** nada público encontrado no tempo e na cota disponíveis. Ver "O que segue aberto".

### (d) Concentração e liderança por categoria (item 28)

**API pública do ML** (acesso em 15/10/2026, sem token).
- **`/categories/{id}`:** segue pública e traz `total_items_in_this_category`.

  | Categoria | Anúncios |
  |---|---|
  | Alimentos e Bebidas (MLB1403) | 1.503.578 |
  | Mercearia (MLB1423) | 811.128 |
  | Bebidas | 428.099 |
  | Infusões (MLB194831) | 118.424 |
  | Café (MLB247520) | 38.856 a 39.782 |
  | Café Moído e em Grão | 27.806 |
  | Café Solúvel | 8.074 |
  | Cápsulas (MLB247540) | 16.270 a 17.231 |

  O valor varia entre as leituras da categoria-mãe e da própria categoria, provavelmente por cache.
- **Endpoints fechados:**
  - `/sites/MLB/search`: 403 forbidden;
  - `/highlights/MLB/category/...`: 401, pede token;
  - `/trends/MLB`: 403 PolicyAgent.

  Sem login, não dá para medir CR3, CR5, HHI nem os mais vendidos pela API.

**Nubimetrics** (academia.nubimetrics.com):
- chocolate no ML: "mais 72% de vendedores platinum" (post de 29/01/2024);
- moda íntima: "mais de 63%" Platinum (post de 10/08/2026);
- agasalhos: concorrência "dominada" por Platinum (02/06/2026);
- café: só citado como sazonal, sem dado.

A Nubimetrics não publica a definição nem a base. Usar só como faixa de 63% a 72% em categorias que ela chama de saturadas.

**Real Trends e Avantpro.** O blog da Real Trends está em espanhol, e a URL `/br/blog` dá 404. O blog da Avantpro não tem posts de 2026 por categoria. Nada aproveitável.

### (e) Recompra de consumíveis e café (item 29)

**Worldpanel by Numerator, Consumer Insights 2026** (Mercado & Consumo, 25/09/2026). Mais de 10 mil lares; 12 meses até jun/2026.
- e-commerce de FMCG +58%;
- 2% das ocasiões de compra;
- abastecimento online +94%, com +5 p.p. de fatia em unidades;
- fatia do abastecimento por período do mês: 45,2% entre os dias 11 e 20, contra 21,9% nos dias 1 a 10 e 21,6% depois do dia 21;
- nos pure players, H&B é a cesta mais comprada.

Frase do diretor: "o próximo desafio é transformar experimentação em recorrência".

**Worldpanel, Brand Footprint Brasil 2026** (PDF de 03/08/2026, `https://static.poder360.com.br/uploads/2026/08/Relatorio-sobre-o-Brand-Footprint-Brasil-2026-3ago2026.pdf`; Mercado & Consumo de 19/08/2026). Mais de 400 marcas; métrica CRP, que combina penetração e frequência; mais de 11.300 lares.
- **Penetração do online em FMCG:**

  | Ano | Lares |
  |---|---|
  | 2023 | 23,8% |
  | 2024 | 31,1% |
  | 2025 | 45,4% (27,8 mi de lares, mais de 60% novos) |

- **Peso das cestas:** H&B é cerca de metade do faturamento online de FMCG.
- **Top 5 de marcas online:** Natura, Coca-Cola, Ypê, Colgate e Italac. Nenhuma marca de café.
- **Como as marcas cresceram:** das 238 que cresceram em CRP, 71% cresceram por penetração e 28% por penetração com frequência.
- **Repertório:** o shopper passou de 112 para 120 marcas.

**ABIC** (divulgado em 29/01/2026; Estadão via CompreRural).
- **Consumo** (nov/2024 a out/2025): 21,409 mi de sacas (−2,31%); per capita de 4,82 kg (−3,88%).
- **Faturamento da indústria em 2025:** R$46,24 bi (+25,6%), atribuído ao preço.
- **Preços, jan → dez/2025:**

  | Tipo | Variação |
  |---|---|
  | Cápsula | −16,8% |
  | Gourmet | +20,1% |
  | Tradicional e extraforte | +5,8% |
  | Superior | −3,5% |
  | Especial | +4,3% |

- **Lacunas:** não há abertura por canal online nem dado de recompra. A metodologia não está detalhada no texto.

**Lado do ML** (8-K 2T26, [N2]):
- itens por comprador +19% a/a no Brasil;
- DAU cresce mais rápido que MAU todo trimestre desde a mudança de frete;
- fatia de usuários com compra em 3 ou mais categorias +10 p.p. no Brasil;
- coortes novas com "higher retention" que as anteriores.

Não há taxa de recompra por categoria. O botão de recompra existe, segundo a executiva em fev/2025, mas não há dado de uso.

---

## Tabela de afirmações novas

| id | Afirmação | Tipo | Fonte | Data da fonte | Confiança | Fecha qual lacuna |
|---|---|---|---|---|---|---|
| R2-DAD-01 | E-commerce BR com GMV de R$351,4 bi em 2024 (+19,1%) e 125,6 mi de shoppers ativos; método por dados transacionais de lojas conveniadas mais pesquisa | [DADO] N4 | NIQ Ebit Webshoppers 51 Free (PDF develop.nielseniq.com …Ed.51.pdf) | abr/2025 (dados 2024) | B (cobertura parcial de marketplaces) | §0.3; item 25 |
| R2-DAD-02 | Fatia online do valor de FMCG: 4,3% no total; Alimentos 1,4%, Bebidas 2,4%, H&B 8,3%, Limpeza 1,6% (2024) | [DADO] N4 | Webshoppers 51 | abr/2025 | B | item 25; ALIM Q3 (contexto) |
| R2-DAD-03 | Abastecimento e Reposição é a missão nº 1 (cerca de 37% a 44%); Alimentos e Bebidas +41,9% nos pure players contra −11,3% nos brick & click (2024) | [DADO] N4 | Webshoppers 51 | abr/2025 | B | item 25 |
| R2-DAD-04 | Black Friday 2024: Alimentos e Bebidas foi a 8ª categoria em intenção (9,8%) e a 4ª em compra realizada (14,1%) | [DADO] N4 | Webshoppers 51 (pesquisa ad hoc, dez/2024) | abr/2025 | B | PRE Q8 (contexto) |
| R2-DAD-05 | 1º sem. 2026: R$208,4 bi (+16,9%), 756,7 mi de pedidos (+34,8%), tíquete de R$275,50 (−13,3%), itens por pedido de 2,25 para 1,97; projeção de R$462,5 bi em 2026 | [DADO] N4 | Confi/E-commerce Brasil via GiroNews e Portal IN | 28–29/07/2026 | C (método não publicado) | item 25 |
| R2-DAD-06 | GMV de 2025 de cerca de R$450 bi; ML 42% (cerca de R$185 bi), Shopee 19% (cerca de R$86 bi), Amazon cerca de 11% | [DADO] estimativa de banco | UBS BB via Money Times | 19/03/2026 | C | item 25; Shopee D20 (faixa) |
| R2-DAD-07 | GMV de 2024: ML R$138,9 bi, Magalu R$46,1 bi, Shopee R$40 bi, Amazon R$39 bi | [DADO] N5 | IRTT via YAV | 20/05/2026 | C | item 25; Shopee D20 (faixa) |
| R2-DAD-08 | Ranking Conversion (Similarweb, mais de 2.000 sites) encerrado em jan/2026; PDF por formulário | [DADO] | conversion.com.br/blog/fim-do-relatorio-setores-ecommerce | 28/01/2026 | B | item 25 (fonte esgotada) |
| R2-DAD-09 | O tamanho do e-commerce BR varia de R$235,5 bi (ABComm, 2025) a R$450 bi (UBS, 2025), conforme o método; só a liderança do ML é consenso | [DADO] síntese | R2-DAD-01, 05, 06 e 07 | 2025–2026 | B | item 25 |
| R2-DAD-10 | Mercado Ads passou de 10% do mercado de publicidade digital da América Latina no 2T26; Ads +62% a/a; Ads/GMV não divulgado | [N2] | MELI 8-K Ex-99.1 2T26 (sec.gov …000109959026000021) | 05/08/2026 | A | ADS (Ads/GMV de cerca de 2,6% segue sem N2); item 26 |
| R2-DAD-11 | Brasil: itens por comprador +19% a/a; DAU cresce mais que MAU desde a mudança de frete; +10 p.p. de usuários em 3 ou mais categorias; coortes novas com retenção maior | [N2] | MELI 8-K 2T26 | 05/08/2026 | A | item 29; ALIM Q4 (proxy) |
| R2-DAD-12 | E-commerce de FMCG +58% em 12 meses até jun/2026, mas só 2% das ocasiões; abastecimento online +94% e +5 p.p. em unidades; pico entre os dias 11 e 20 (45,2%) | [DADO] N4 painel (mais de 10 mil lares) | Worldpanel Consumer Insights 2026 via Mercado & Consumo | 25/09/2026 | B | item 29; ALIM Q4 |
| R2-DAD-13 | Online alcançou 45,4% dos lares em FMCG em 2025 (31,1% em 2024), 27,8 mi de lares, mais de 60% novos; H&B cerca de metade do faturamento; 71% das marcas cresceram por penetração | [DADO] N4 painel (mais de 11.300 lares) | Brand Footprint Brasil 2026 (PDF poder360) | 03/08/2026 | B | item 29; ALIM Q4 |
| R2-DAD-14 | Café: consumo de 21,409 mi de sacas (−2,31%), per capita de 4,82 kg; faturamento da indústria R$46,24 bi (+25,6%); cápsula −16,8% e gourmet +20,1% no preço em 2025 | [DADO] N4 setorial | ABIC via Estadão/CompreRural | 29–30/01/2026 | B | item 29 (sem canal nem recompra) |
| R2-DAD-15 | Supermercado no ML: vendas +77% em 2024; 18 mi de buscas por mês; 1 em cada 4 compradores novo; sortimento +74% em 6 meses; botão de recompra; café entre os 3 itens mais vendidos na estreia do BBB 25 | [OFICIAL] declaração de executiva via imprensa | Meio & Mensagem; Mercado & Consumo | 25/02/2025 | C | ALIM Q4; item 25 |
| R2-DAD-16 | Ruptura no e-commerce de 30,5% (jan–set/2024, +3,8 p.p.); Alimentos e Bebidas com a maior alta (+3,9 p.p.); marketplaces −1,6 p.p.; 41% das ofertas dependem de 3P | [DADO] N4 (cerca de 700 a 750 mil páginas) | Lett EQI 2024 via Mercado & Consumo; dcx.lett.digital/eqi-2024 | 13/11/2024; 03/12/2024 | B (amostra descrita de forma divergente) | item 27; ALIM Q3 |
| R2-DAD-17 | Um dia de ruptura tira do top 30 46% dos itens do top 5 (mais de 64% em café, limpeza, snacks e bebidas; 39% em marketplaces); 37,9% voltam no dia 1 e 59% no dia 2; cerca de 7% dos dias com anúncio de item indisponível | [DADO] N4 | Lett via Mercado & Consumo | 13/05/2025 | C (amostra não declarada) | LOG Q7; ALIM Q3; consolidado §7 item 10 |
| R2-DAD-18 | Ruptura média de 30% na Black Friday e até 50% no Carnaval e na Páscoa; duração do estoque de 5,85 dias em Alimentos e 6,68 em Bebidas | [DADO] N4 | Lett via GiroNews | 24/11/2025 | C | item 27 |
| R2-DAD-19 | Case 3 Corações/Lett: +56% de sell-out em cafeteiras e cápsulas (Carrefour e GPA), sem período nem base; outra versão em 5 meses (cápsulas +11%, cafeteira +81%); ML ausente | [CASE] | dcx.lett.digital/case-3coracoes-cafeteiras; Baguete | 22/04/2025; 16/06/2025 | C | ALIM Q3 ("case não buscado" fechado: encontrado, não auditável, não é ML); §0.7 |
| R2-DAD-20 | Case Ypê/Lett no ML: conversão de 1 SKU de 15% para 43% em 6 meses após título, descrição, imagens e vídeo; qualidade de conteúdo +8% | [CASE] | GiroNews | 16/01/2026 | C | ALIM Q3; RANK (conteúdo e conversão); §0.7 |
| R2-DAD-21 | Case JDE/Lett: e-commerce +45% em 2024; Loja Perfeita de 45% para 67%; share of voice +26% | [CASE] | GiroNews | 01/07/2025 | C | item 27 |
| R2-DAD-22 | Case Nestlé Cafés/Lett na Amazon: +80% de sell-out em 3 meses; mais de 30 itens com destaque na busca "Café" | [CASE] | dcx.lett.digital/case-nestle-cafes | 08/04/2025 | C | item 27 (Amazon) |
| R2-DAD-23 | Amazon Ads oferece benchmarks por categoria no Brasil (CTR, CPC, CPM, clientes novos para a marca), só no console ou na API | [OFICIAL] Amazon | advertising.amazon.com/pt-br/…/benchmarks-reporting-now-generally-available-worldwide | 18/05/2026 | A (existência); dado exige login | item 26 (Amazon ADS Q7: caminho, não número) |
| R2-DAD-24 | Nubimetrics: mais de 72% de vendedores Platinum em chocolate (2024) e mais de 63% em moda íntima (2026); sem dado de café; definição não publicada | [DADO] N5 | academia.nubimetrics.com (pt/supermercado-mercado-livre; pt/produtos-ticket-baixo-vender) | 29/01/2024; 10/08/2026 | C | MIX Q3 (faixa proxy, não CR) |
| R2-DAD-25 | API pública: Alimentos e Bebidas 1,50 mi de anúncios; café cerca de 39 a 40 mil; cápsulas cerca de 16 a 17 mil; `/search` 403, `/highlights` 401, `/trends` 403 sem token | [OFICIAL] API | api.mercadolibre.com/categories/MLB1403, MLB247520, MLB247540 | lido em 15/10/2026 | A (contagem) | MIX Q3; CASES Q1 (concentração inviável sem login) |
| R2-DAD-26 | Mercado Ads (autodeclarado): cerca de 100 mil anunciantes; mais de 135 mi de usuários únicos por mês; meta-análise da Kantar (mais de 200 campanhas) com +52% de awareness | [OFICIAL] conteúdo pago | Meio & Mensagem, patrocinado | sem data (cita 2021) | C | item 26 (topo de funil, sem CPC nem ACOS) |
| R2-DAD-27 | Lembrança de loja para brinquedos: Amazon 27,6%, ML 22,6%, Shopee 15,7% (1.550 consumidores) | [DADO] N4 | NIQ Ebit via Economic News Brasil | jun/2026 (publ. 08/10/2026) | B | item 25 (sinal fraco) |
| R2-DAD-28 | Regras práticas de ACOS no ML: 5% "excelente", 15% "bom", 50% "preocupante"; dispersão de cerca de 3% a 40% dentro da campanha | [PRÁTICA] | jaguarsheet.com/pt/blog | 2026 (sem data exata) | C | ADS Q7 (não fecha; só heurística) |

---

## O que segue aberto e por quê

1. **GMV e participação do ML por fonte com método (item 25).**
   - **NIQ Webshoppers 2026:** as edições 53 e 54 não foram achadas em versão Free. A edição 51 exclui Meli não FMCG e a Amazon 3P em parte das análises.
   - **Confi e IRTT:** a metodologia não é pública na imprensa, e o PDF do IRTT não foi lido.
   - **UBS:** estimativa sem premissas.
   - **Conversion:** a série acabou, e o PDF exige formulário.
   - **Situação:** a participação do ML segue como faixa (cerca de 40% a 42% do GMV), confiança C.
   - **Próximo passo:** ler o relatório "Da Compra à Confiança" no site da Confi, se houver versão sem formulário, e o PDF do IRTT.
2. **Benchmarks de Ads com amostra para o ML-BR (item 26; ADS Q7).** Continua S, pelos motivos abaixo.
   - O portal do Mercado Ads deu 403, e o Ads Center exige login.
   - Pacvue e eMarketer deram 403, e o Pacvue cobre só os EUA.
   - Não há agência BR com amostra publicada.
   - Ads/GMV oficial: a carta 2T26 confirma que não é divulgado.
   - **Próximo passo:** relatório anual 10-K de 2025 (segmento de Ads), *earnings calls* e cases do Mercado Ads em premiações com métrica (Effie).
3. **Share of search, content score e ruptura no ML com número (item 27).**
   - **Lett:** traz ruptura e recuperação por formato de canal, sem nome de marketplace. O EQI completo exige formulário.
   - **Cases:** o único case no ML (Ypê) é de 1 SKU, sem controle. Nenhum case mede share of search com valor.
   - **Profitero, Nielsen Digital Shelf e SuperHiper:** sem material público com recorte BR na cota disponível.
   - **Situação:** ALIM Q3 passa de S para P.
4. **Concentração por categoria (item 28; MIX Q3; CASES Q1 e Q7).**
   - A API pública fechou busca, *highlights* e tendências. A Nubimetrics dá só a fatia de vendedores Platinum. A Real Trends e a Avantpro não têm posts por categoria.
   - **Situação:** CR3, CR5 e HHI de café seguem S.
   - **Alternativa sem login:** a observação direta da 1ª página com protocolo (item 30), contando vendedores e lojas oficiais por termo. É estimativa N3, não N5.
5. **Taxa de recompra de consumíveis e café por canal (item 29; ALIM Q4).**
   - **Worldpanel:** dá penetração, ocasiões e crescimento, mas não recompra online por categoria. O relatório completo é pago.
   - **ABIC:** não abre canal.
   - **ML:** dá só proxies (itens por comprador, retenção de coortes, multicategoria). O uso do botão de recompra não é público.
   - **Situação:** ALIM Q4 passa de S para P, com proxies.
6. **Conversão absoluta do ML e por categoria.** Não é pública; só a variação de +1,1 p.p. (8-K). Sem fonte N4 que a meça.
7. **Divergências registradas, sem resolução:**
   - amostra do EQI 2024: 748 mil páginas em 16 e-commerces contra 700 mil ofertas em 3.900 lojas;
   - case 3 Corações: +56% total contra +11% e +81% por item;
   - BBB 25: GMV +82% contra +84%;
   - contagem de anúncios de café pela API: 38.856 contra 39.782, entre leituras.

**Fontes não acessadas:**

| Fonte | Situação |
|---|---|
| publicidade.mercadolivre.com.br | 403 |
| ads.mercadolivre.com.br | exige login |
| pacvue.com (relatório Q1 2026) | 403 |
| emarketer.com | 403 |
| PDF da Conversion | formulário |
| content.lett.digital (EQI completo) | formulário |
| api.mercadolibre.com `/search`, `/trends`, `/highlights` | 403, 403 e 401 |
| sec.gov via curl | bloqueado; lido por WebFetch |
