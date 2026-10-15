# Shopee Brasil: alimentos, perecíveis, café e marca própria/indústria (notas do analista)

- **Frente:** alimentos-marca-propria · **Plataforma:** Shopee (Brasil) · **Data de corte:** 2026-10-14
- **Regra de data:** toda regra de plataforma anterior a 2026-04-14, ou sem data, vem marcada "(pode estar superada)".
- **Marcadores:** [REVENDA] = revenda, dropshipping e importação. [MARCA] = indústria e marca própria. [AMBOS] = vale para os dois.
- **Confiança:**
  - A: duas fontes independentes, uma delas N1 a N3.
  - B: uma fonte N1 a N4, ou duas fontes N5/N6 que concordam.
  - C: fonte única N5 a N8.

## Limitações de coleta

- **Busca na web:** o limite de buscas do turno estava esgotado. Por isso não usei o buscador e li só páginas de URL conhecido ou achadas em sitemap e em API pública de conteúdo.
- **Central de Ajuda e Seller Education:** os sites help.shopee.com.br e seller.shopee.com.br/edu são aplicações JavaScript. A API recusou o pedido ("not allowed language") e nenhum artigo pôde ser lido.
- **O que serviu como camada oficial:** o blog e a sala de imprensa da Shopee (shopee.com.br/blog), os vídeos do canal oficial Shopee Brasil e as notícias da Anvisa, lidas pela API Plone do gov.br.
- **Observação direta:** veio de `observacao/lideres.md` (2026-10-14). A coleta parou na tela de login.

---

## 1. Resumo executivo

1. **Atributo Anvisa obrigatório.** Desde 21/09/2026 a Shopee exige o campo Anvisa (protocolo ou código) nos anúncios novos de uma lista de 169 categorias. Os anúncios antigos ("legados") ficaram como estavam "por enquanto". [OFICIAL via terceiro], confiança C. Fonte: RvJiFGQiK3c e c7WmiWzZu4E (Vendedor 360, que recebe os comunicados por ser integrador de API), 14 e 15/09/2026, e o post vendedor360.com.br/guia-completo-regras-da-anvisa-para-vender-produtos-na-shopee/ (14/09/2026).
2. **Medida da Anvisa sobre a Shopee.** A Anvisa revogou em 06/08/2026 uma medida preventiva contra a Shopee (RE 3.056/2026), ligada à venda e à propaganda de medicamentos. A agência avisou que a revogação "não isenta" a plataforma de cumprir a regulação sanitária. [OFICIAL] N2, 10/08/2026: gov.br/anvisa/.../sobre-revogacoes-de-resolucoes-e-medidas-preventivas-para-plataformas-digitais.
3. **Fiscalização chega ao estoque.** Em 18/03/2026 a Anvisa fiscalizou o estoque Full do Mercado Livre em Cajamar (SP) e apreendeu, entre outros, 19 suplementos e 270 probióticos/enzimas, por falta de registro, rótulo estrangeiro, alegação de saúde não aprovada e marca com sugestão terapêutica. Chamou marketplaces de "novo campo de atuação". [OFICIAL] N2, 18/03/2026. Para a Shopee é precedente, não fato da plataforma.
4. **O padrão das retiradas em alimentos** é a alegação de saúde no anúncio, somada a origem desconhecida ou falta de regularização: sal "para atletas" (RE 3.052/2026, 07/08), "café de açaí" contra diabetes (06/02), suplementos (RE 1.045/2026, 19/03). [OFICIAL] N2, Anvisa, confiança A.
5. **Café torrado tem norma do MAPA:** Portaria SDA 570/2022, em vigor desde 01/01/2023 (classificação obrigatória e rotulagem; Procon e MP podem agir), mais RDC 716/2022, RDC 727/2022 e RDC 843/2024 com IN 281/2024. Tabela nutricional não obrigatória para café. [OFICIAL] via ABIC (legislação, 10/12/2025; portaria570, 20/05/2025).
6. **Marketplace como canal de café ainda é pequeno, mas cresce rápido.** Na pergunta sobre o principal local de compra de café, marketplace passou de 0,8% (2023) para 3,5% (2025). Supermercado tem 63,1% e atacarejo 28,2%. Site do fabricante ficou em 1,1% e clube de café em 0,6%. [DADO] N4: ABIC, Hábitos e Preferências 2025 (n = 4.032, confiança declarada de 99%), set/2025.
7. **Mercado Shopee.** A seção de mercado foca em itens de supermercado **não perecíveis**: alimentos e bebidas, casa, higiene e pets. Há três dias de ofertas por semana: segunda, lavanderia; quarta, mercearia; sexta, happy hour. [OFICIAL] blog Shopee, atualizado em 02/06/2026.
8. **Lojas Oficiais.** O selo vermelho "Oficial" garante produto original com nota fiscal. Se houver dúvida de autenticidade, o comprador recebe o valor integral em cupom. A devolução tem prazo estendido de 30 dias. Marcas de alimentos listadas: Café Pilão, Mundo Danone, Bauducco, Fini, Heinz e Carrefour. [OFICIAL] blog Shopee "lojas-oficiais", 02/06/2026.
9. **Entrada como Loja Oficial.** A entrada é por convite ou negociação com o gerente de contas, e não há formulário público. [PRÁTICA] OjxNoZ4Sums (2022), r5oEfzPV324 (2024) e _p1IBEyvCwo (2026), confiança B (pode estar superada no detalhe). No caso de 2026, a loja apresentou uma proposta ao gerente e virou oficial. O vendedor relatou alta de 30% num dia comum, número sem base declarada.
10. **Comissão desde 01/10/2026.** Itens de até R$79,99 pagam 20% mais R$4,50 **por item** (antes R$4). Isso pesa mais em alimento de ticket baixo. As demais faixas pagam 14% mais uma taxa fixa de R$16, R$20 ou R$26. [OFICIAL via terceiro] IYi2eifHqSY, 9VOoazXt_aE e hEkVpRw_vNg (23/09 a 13/10/2026), confiança B.
11. **Full Shopee.**
    - Pré-requisitos: CNPJ, Simples ou regime normal, nota da loja acima de 4,5 e no mínimo 5 pedidos por dia. [OFICIAL] TUs6QYGqGrw, 04/08/2026.
    - Full Mais (lançado em jun/2026): redução de 0,5 a 2 pontos percentuais (p.p.) na comissão de itens a partir de R$50, se pelo menos 40% dos pedidos saírem pelo Full. [OFICIAL] 0oRYednAlHY, 04/08/2026.
    - Rede: 5 CDs de fulfillment (SP, PE, GO, RS, MG). [OFICIAL] blog, 07/05/2026.
    - Não achei regra oficial de validade mínima ou temperatura para alimentos no Full Shopee. Ver lacunas.
12. **Itens abaixo de R$20 no Full** pagam "envio excepcional" por unidade: R$1 (P), R$2,50 (M), R$6 (G) e R$12,50 (GG), com mínimo de 15 unidades. Para alimento barato, isso tende a inviabilizar unidade avulsa. [PRÁTICA] com tela, ty0iwe3dV1I, 20/07/2026, confiança C.
13. **Busca "café em grãos" (14/10/2026):** Lojas Oficiais de marca no topo (Italle, Baggio), escada de tamanhos de 250g a 3kg, cerca de R$67 a R$114/kg, kit degustação 5x50g a R$311/kg, títulos com atributos (espécie, torra, notas, SCA) e líderes quase todos marca própria ou torrefação. [OBS] lideres.md, C.
14. **Recorrência.** Não achei produto oficial de assinatura ou compra programada para o comprador, equivalente ao Programe e Poupe. As ferramentas de recompra são de cupom: seguidor (vale 7 dias após o resgate), cupom para "compradores específicos" e cupom de live. [PRÁTICA] 7i2f1rplBl0, 13/08/2026. O ShopeeVIP (R$9,90/mês) é um clube de cupons do comprador, não assinatura de produto. [PRÁTICA] Kasbq8gziOg, 21/05/2026.
15. **Conflito indústria x distribuidor:** marcas evitam o marketplace por causa do distribuidor (EitJfemXOXA, 23/07/2026); indústria corta o revendedor que cresce (8N5ktlBoTJ8, 09/09/2026); seller põe Ads só na marca própria (8N5ktlBoTJ8). [PRÁTICA] C.

---

## 2. Como funciona (mecânica e regras oficiais, com data)

### 2.1 Regularização sanitária e atributo Anvisa na Shopee

**Atributo Anvisa** ([OFICIAL via terceiro], C, 14/09/2026, fontes RvJiFGQiK3c e c7WmiWzZu4E)

- **Vigência e alcance:** desde 21/09/2026 o atributo Anvisa passou a ser "mandatório" só em anúncios novos. Os legados permanecem "por enquanto".
- **O que aceita:** protocolo ou código. Sem o dado, o anúncio novo não sobe.
- **Escopo:** uma planilha de 169 categorias diz, para cada uma, se o campo é obrigatório. Exemplos citados: protetor solar sim, navalha e lâmina não, e até "casa e decoração" aparece.
- **Lacuna:** a planilha não foi vista aqui. Ficou sem confirmação quais categorias de alimentos entram, em particular café, chá e suplemento.

**Post do Vendedor 360** (14/09/2026): a plataforma "pode proibir itens mesmo que sejam legalizados no país"; suplementos são "altamente visados"; medicamento é proibido, inclusive "natural"; punição vai de suspensão do anúncio a banimento. Não trata de validade nem rotulagem.

**Penalidade por anúncio** ([OFICIAL], série Ajuda AÍ, LPKmJotE9Vc, 17/09/2026): episódio sobre Anvisa, Anatel e Inmetro; distingue anúncio "banido" de "removido", com níveis de severidade. Praticante que mostra o tutorial: conteúdo proibido por lei é nível extremo (ThPsYQpMxJE, 05/08/2026).

**Base regulatória para alimentos** (N2, via ABIC, B)

- RDC 843/2024 e IN 281/2024 definem a forma de regularização por categoria de alimento.
- RDC 727/2022: rotulagem geral e alergênicos.
- RDC 716/2022: requisitos sanitários de café, cevada, chás, erva-mate, especiarias e molhos.
- RDC 655/2022: recolhimento de alimentos.
- Portaria Inmetro 93/2022: pré-medidos (conteúdo nominal).
- Lacuna: não li a IN 281/2024 e não confirmei a categoria do café nem se ele é dispensado de registro.

### 2.2 Café: o que muda por norma

**Portaria SDA/MAPA nº 570** (publicada em 11/05/2022, em vigor desde 01/01/2023)

- Cria o padrão oficial de classificação do café torrado: identidade e qualidade, amostragem e rotulagem.
- A classificação é obrigatória para todas as torrefações, "das nano às grandes". Pode ser feita por classificador próprio, com manual de boas práticas, ou terceirizada.
- Procon e MP podem agir contra fraude.
- Fonte: [OFICIAL] N2 via ABIC (/certificacoes/portaria570, atualizada em 20/05/2025).

**Relato de fábrica** ([PRÁTICA], kqerLjGQAgY, 05/07/2026)

- Torrefador de Poços de Caldas, na série da agência Mamba.
- Segundo ele, a norma obriga a declarar no rótulo se o café é arábica ou canéfora (robusta/conilon). Também é possível declarar "100%" ou "predominantemente".
- No rótulo dele aparecem ainda o processo (natural, cereja descascado, fermentado) e o tipo de torra.
- No vídeo a norma aparece como "SD 70". Pela descrição, é muito provavelmente a SDA 570 (inferência).
- Nota de torra Agtron: cerca de 60 para cápsula, 75 para coado e 45 a 50 no café "de supermercado". [PRÁTICA] do mesmo vídeo, número de fabricante, sem medição independente, C.

### 2.3 Lojas Oficiais

Fonte: [OFICIAL] blog Shopee, publicado em 28/08/2025 e atualizado em 02/06/2026.

- Cada marca tem página com categorias, selo vermelho "Oficial" e garantia de produto original com nota fiscal.
- Em caso de dúvida de autenticidade, o comprador recebe reembolso integral **em cupom**.
- Devolução estendida para 30 dias.
- Há acesso a cupons de frete grátis e filtro "Lojas Oficiais" na busca.
- O total citado varia entre posts: "mais de 2 milhões de produtos" no post de Lojas Oficiais e "mais de 70 mil" no post do Mercado Shopee. São atualizações de épocas diferentes.

**Divergência:** Jackie Santos (r5oEfzPV324, 2024) falava em "duas vezes o dinheiro de volta". A página oficial de 2026 fala em reembolso integral em cupom. Prevalece a fonte oficial e atual.

**Lives:** grandes marcas da seção podem "adquirir pacotes" para aparecer nas lives oficiais ([OFICIAL], blog de 2023, atualizado em 02/06/2026, pode estar superada).

**Serviço exclusivo:** a MadeiraMadeira oferece montagem contratada no checkout da própria Loja Oficial ([OFICIAL], 13/07/2026).

**Como entrar** (não há página oficial de critérios) — [PRÁTICA], B, pode estar superada:

- É por convite. O foco mudou com o tempo: primeiro o maior volume, depois quem era oficial em outros marketplaces, e hoje "marcas e fabricantes" (OjxNoZ4Sums, 15/05/2022; r5oEfzPV324, 21/08/2024).
- Em 2021 a Shopee pediu exclusividade de canal a um vendedor de moda, que recusou (OjxNoZ4Sums). Não há confirmação recente.
- Caso de 2026: proposta apresentada ao gerente de contas e ao diretor da categoria. O vendedor diz que o gerente atende 290 lojas (_p1IBEyvCwo, 02/06/2026).

### 2.4 Mercado Shopee (supermercado)

Fonte: [OFICIAL] blog, criado em 31/12/2022 e atualizado em 02/06/2026. Além do foco em não perecíveis e do calendário (resumo, item 7), o objetivo declarado é fortalecer supermercados oficiais e grandes marcas de alimentos, limpeza e higiene, com cupons exclusivos. 100 Moedas Shopee valem R$1.

### 2.5 Full Shopee e o que se sabe para alimento

**Pré-requisitos da loja** ([OFICIAL], TUs6QYGqGrw, 04/08/2026)

- CNPJ, Simples Nacional ou regime normal.
- Avaliação acima de 4,5 estrelas.
- No mínimo 5 pedidos por dia.
- Mínimos de venda, dimensão, peso e preço por item, com detalhes no Centro de Educação (não lido).

**Adesão** ([OFICIAL], CDXeiFn8Ykw, 17/09/2026): configuração fiscal com série de nota exclusiva para a Shopee, certificado digital e regra fiscal por produto.

**Full Mais** ([OFICIAL], 0oRYednAlHY, 04/08/2026)

- Lançado em junho de 2026.
- Base: participação mensal de pedidos via Full.
  - Abaixo de 40%: nada.
  - De 40% a 70%: 0,5 p.p. em itens de R$50 a R$79,99 e 1 p.p. em itens a partir de R$80.
  - 70% ou mais: 1 p.p. e 2 p.p., respectivamente.
- Teto de "até 14%" sobre a comissão.
- O crédito cai na carteira na 1ª semana do mês seguinte.
- Itens abaixo de R$50 contam na participação, mas não geram desconto.

**Custos** ([PRÁTICA])

- Envio e armazenagem sem custo. Só se paga por inconformidade (Universidade Ecommerce, OUC2vulFv8E, 27/04/2026, C).
- Itens abaixo de R$20 pagam "envio excepcional" de R$1 a R$12,50 por unidade, com mínimo de 15 unidades (ty0iwe3dV1I, 20/07/2026, tela, C).
- Multa de R$3 por erro de conferência na entrada. Um fabricante de moda relata multas somadas de "9.000" e passou a bipar 100% da remessa (RwYs9zPynLw, 01/09/2026, C).

**Rede logística** ([OFICIAL], 23/02 e 07/05/2026)

- 19 CDs (14 de cross-docking e 5 de fulfillment), mais de 200 hubs, mais de 3 mil Agências Shopee e entrega no dia seguinte em mais de 75 cidades.
- Os CDs de Goiânia e de BH declaram operação "multicategoria (moda, beleza, tecnologia)". Não citam alimentos.

**Validade, lote e temperatura no Full Shopee:** sem evidência oficial. Só há referência indireta de que produtos "restritos ou com condições específicas" têm regras adicionais de embalagem e documentação (vídeo oficial de embalagem, 9CxujZDsRCw, 01/10/2026).

**Comparação com o ML** ([OFICIAL via terceiro], xWw-95fez58, 01/09/2026, tabela de ago/2026, C; o vídeo tem 3+ sinais fracos):

- A linha de supermercado tem armazenagem grátis para itens pequenos e médios.
- Acima de 4 meses se paga armazenagem extra: R$1 por unidade por mês entre 4 e 6 meses, R$12 entre 6 e 12 e R$28 acima de 12.
- A retirada de estoque custa cerca de R$98 a R$120.
- O ML "descarta analisando data de validade".

### 2.6 Tarifas que pesam no alimento de ticket baixo

Fonte: [OFICIAL via terceiro], três canais independentes que concordam, B, set a out/2026.

| Faixa de preço do item | Comissão (desde 01/10/2026) | Subsídio Pix (pago pela Shopee) |
|---|---|---|
| até R$79,99 | 20% + R$4,50 por item (antes R$4) | não |
| R$80 a R$99,99 | 14% + R$16 | 5% |
| R$100 a R$199,99 | 14% + R$20 | 5% |
| R$200 a R$499,99 | 14% + R$26 | 5% |
| a partir de R$500 | 14% + R$26 | até 8% |

- A taxa fixa é **por item, não por pedido**. Três unidades avulsas pagam a taxa três vezes (IYi2eifHqSY).
- Vendedor CPF paga 20% + R$4,50 na primeira faixa. Há regra adicional para CPF acima de 450 pedidos em 90 dias (9VOoazXt_aE). Não detalhada aqui.
- Taxa "Devolução Fácil": R$0,49 por venda, ligada automaticamente desde maio/2026. [PRÁTICA] yAmvIlW11GY, 09/05/2026, C.
- Adicional de 2% a 3% para entrar em eventos oficiais, que varia por evento. [PRÁTICA] 4oQLk8XXYP4, 01/09/2026, C.

### 2.7 Conteúdo, Vídeo e Live

[OFICIAL], aUqdtKFx5gM, 20/08/2026: promoção tem de ser "100% verdadeira", réplicas e imagem de terceiros são proibidas, o produto mostrado tem de ser o anunciado e a jornada fica dentro da Shopee. No alimento isso soma com a regra sanitária: alegação de saúde dita em vídeo ou live é propaganda (ver 5.2).

---

## 3. O que os melhores fazem (consenso, divergências, ids)

### 3.1 Consenso

**1. Regularizar antes de anunciar e nunca prometer saúde. [MARCA] e [REVENDA]**

As retiradas da Anvisa em 2026 se repetem pelo mesmo motivo: "alegações terapêuticas, funcionais ou de saúde não aprovadas" em anúncio online. Exemplos: sal "evita câimbra", "café de açaí" contra diabetes, suplemento "100 dores".

- Fontes: Anvisa, 06/02, 19/03 e 07/08/2026.
- Confiança A: padrão em vários atos.
- Em 05/08/2026 a Anvisa abriu processo para rever as normas de propaganda de alimentos. Citou marketplaces e "marketing de influenciadores" (N2).

**2. Escada de tamanhos e kits na mesma loja. [MARCA]**

- Os líderes de café oferecem 250g, 500g, 1kg, 2kg e 3kg, com preço por kg menor no tamanho maior. Exemplo: Italle de 3kg a R$64,77/kg contra R$76,90 no 1kg. [OBS] lideres.md.
- Kit de origens (4x250g) e kit degustação (5x50g) aparecem no top 40.
- Método do kit (Cauê Oliveira, 96YaDbhhsAo, 07/08/2026, [PRÁTICA] C):
  - kits de 2, 4, 6, 8 e 10 unidades, com margem % um pouco menor a cada degrau e mais margem em R$;
  - a "ferramenta combo" junta produtos que se completam.

**3. Título que vende atributo, e não só marca. [AMBOS]**

O padrão no topo de "café em grãos" usa barras verticais e lista de atributos: espécie, torra, notas, pontos SCA, variedade, "moído no dia do envio" e escassez de safra. [OBS], C. Casa com a Portaria 570, que obriga declarar espécie e classificação, e com o hábito do consumidor: 48% não sabem a diferença entre estilos de café (ABIC 2025).

**4. Marca registrada mais embalagem própria como barreira. [MARCA]**

Fábricas e sellers que crescem registram marca e EAN e fazem embalagem própria para "não cair no catálogo" do concorrente. [PRÁTICA] 9UVMD3UIQSQ, 02/09/2026 (vendedor de pet com tela), C. A frase "se cair no meu catálogo posso processar" é do contexto ML e não se aplica igual à Shopee.

**5. Ads concentrado na marca própria. [MARCA]**

O seller de fraldas (R$1 milhão por mês na Shopee, segundo o canal) diz que quase não gasta Ads em itens de terceiros e põe a verba "apenas na minha marca própria". [PRÁTICA] 8N5ktlBoTJ8, 09/09/2026, C.

**6. Logística perto do CD de fulfillment. [AMBOS]** Um fabricante de Goiânia acha o Full Shopee local melhor que o de SP (RwYs9zPynLw, 01/09/2026, C). A Shopee abriu Full em GO e MG em 2026 e promete cerca de 50% menos prazo nessas regiões ([OFICIAL]).
 Qualidade e expedição antes de escalar. [MARCA]**

- Marca de cosméticos: o faturamento "lateralizou" porque a expedição ruim derrubou a recompra (EitJfemXOXA, 23/07/2026).
- Fabricante de moda: "ou você tem um produto bom ou sai do mercado", por causa das regras de experiência de compra (RwYs9zPynLw).
- [PRÁTICA], C.

### 3.2 Divergências entre fontes

| Tema | Fonte A | Fonte B | Leitura |
|---|---|---|---|
| Vale a pena ser Loja Oficial? | "Não vejo vantagem", só selo e página; exigiam exclusividade (OjxNoZ4Sums, 2022) | "Exposição infinitamente maior", banners e cupons só para oficiais (r5oEfzPV324, 2024); +30% de vendas num dia (_p1IBEyvCwo, 2026) | Faixa, não média. A fonte oficial confirma página, selo, cupons e garantia, sem dado de visibilidade. A de 2022 pode estar superada. |
| Garantia ao comprador | "2x o dinheiro de volta" (r5oEfzPV324, 2024) | Reembolso integral em cupom (blog oficial, 2026) | Prevalece o oficial de 2026. |
| Punição por reclamação | Shopee "zera sua exposição durante 21 dias" (RwYs9zPynLw, 2026) | Tabela oficial de pontos: 21 dias de suspensão de benefícios e −20% de visibilidade na faixa de 9 a 11 pontos (ThPsYQpMxJE e LLDUrAuF3qQ, 2026) | "Zerar" não aparece na tabela mostrada. Pode existir outra régua de experiência de compra; sem documento oficial lido. |
| Rendimento da saca torrada | 60 kg crus → 50 kg torrados (fábrica, kqerLjGQAgY) | 42 a 43 kg, ou 48 kg num café muito bom (lWgirqh5BT8) | Faixa de 42 a 50 kg, conforme umidade, defeito e torra. |
| Full x expedição própria | Full é o modelo preferido do fabricante (RwYs9zPynLw) | Queixas de demora no Full SP (Vfbc25kqgYs, 05/05/2026) | Depende do CD e da época. |

---

## 4. Números de referência

| # | Número | Fonte | Data | Tipo | Confiança |
|---|---|---|---|---|---|
| N1 | Comissão até R$79,99: 20% + R$4,50 por item | IYi2eifHqSY, 9VOoazXt_aE, hEkVpRw_vNg | set a out/2026 | OFICIAL via terceiro | B |
| N2 | Faixas a partir de R$80: 14% + R$16 / R$20 / R$26; Pix 5% a até 8% | idem | out/2026 | OFICIAL via terceiro | B |
| N3 | Full Mais: participação ≥40% e redução de 0,5 a 2 p.p. em itens ≥R$50 | 0oRYednAlHY | 04/08/2026 | OFICIAL | B |
| N4 | Full: nota >4,5, ≥5 pedidos/dia, CNPJ | TUs6QYGqGrw | 04/08/2026 | OFICIAL | B |
| N5 | Envio excepcional de itens <R$20: R$1 / R$2,50 / R$6 / R$12,50 por unidade; mínimo de 15 unidades | ty0iwe3dV1I | 20/07/2026 | PRÁTICA (tela) | C |
| N6 | Multa de R$3 por erro de conferência no Full | RwYs9zPynLw | 01/09/2026 | PRÁTICA | C |
| N7 | Devolução Fácil: R$0,49 por venda | yAmvIlW11GY | 09/05/2026 | PRÁTICA | C |
| N8 | Adicional de eventos oficiais: 2% a 3% | 4oQLk8XXYP4 | 01/09/2026 | PRÁTICA | C |
| N9 | Penalidade por pontos no trimestre: 3 a 5 pts = −5% de visibilidade e R$100; 6 a 8 = −10%, perde frete grátis e R$250; 9 a 11 = 21 dias, −20% e R$500; 12 a 14 = 28 dias, −30% e R$1.000; ≥15 = conta congelada 28 dias e R$1.500 | ThPsYQpMxJE, LLDUrAuF3qQ | mai a ago/2026 | OFICIAL via terceiro | B |
| N10 | Atributo Anvisa: 169 categorias; obrigatório em anúncios novos desde 21/09/2026 | RvJiFGQiK3c | 14/09/2026 | OFICIAL via terceiro | C |
| N11 | Marketplace como principal local de compra de café: 0,8% (2023) → 3,5% (2025) | ABIC, pesquisa 2025 | set/2025 | DADO (n=4.032) | B |
| N12 | Supermercado 63,1%, atacarejo 28,2%, site do fabricante 1,1%, clube de café 0,6% | ABIC 2025 | set/2025 | DADO | B |
| N13 | Estilo comprado: tradicional 32%, extraforte 23%, gourmet 14%, superior 13%, especial 11% | ABIC 2025 | set/2025 | DADO | B |
| N14 | Consumo interno de 21,4 milhões de sacas em 2025 (−2,31%); faturamento da indústria R$46,24 bi (+25,6%); 4,82 kg/hab de torrado | ABIC indicadores | atualizado jan/2026 | DADO | B |
| N16 | Café em grãos na Shopee: cerca de R$67 a R$114/kg no top 40; degustação até R$311/kg; descontos riscados de −5% a −56% | lideres.md | 14/10/2026 | OBS | C |
| N18 | Margem de café moído na hora no varejo físico: 30% a 60% "em média"; 15% a 20% em quem ganha no giro | lWgirqh5BT8 | 28/10/2025 | PRÁTICA (fora do marketplace) | C |
| N19 | Produto de R$29,90 com custo de R$12 e 6% de imposto: margem de contribuição de 20,5% → 18,8% após R$4,50 | IYi2eifHqSY | 23/09/2026 | PRÁTICA (cálculo) | B (aritmética conferível) |
| N22 | Anvisa no CD do ML: 19 suplementos e 270 probióticos/enzimas apreendidos, entre 2.517 itens | Anvisa | 18/03/2026 | OFICIAL N2 | A |

**Benchmarks pedidos sem número público para Shopee Brasil:** recompra de consumíveis, ruptura, content score, share of search e ROAS por categoria de alimentos. Ver a seção 9.

---

## 5. Alimentos, perecíveis e marca própria/indústria (centro da nota)

### 5.1 Regras de categoria (Shopee, com comparação mínima)

**Shopee**

- **Atributo Anvisa** obrigatório nos anúncios novos das categorias listadas desde 21/09/2026 (C). Para o café, não confirmei se o campo é obrigatório.
- **Medicamento** proibido, inclusive "natural".
- **Suplemento** sob vigilância maior.
- **Perecível:** o Mercado Shopee declara foco em não perecíveis. Não achei regra oficial de cadeia fria nem de validade mínima no Full. Na prática o modelo favorece seco e de longa vida: café, chá, grãos, snacks e bebidas não refrigeradas. Isso é inferência a partir do foco declarado e da falta de oferta refrigerada.
- **Embalagem:** produto "restrito ou com condições específicas de transporte" tem regras adicionais ([OFICIAL], 9CxujZDsRCw, 01/10/2026). O vídeo não traz a lista.

**Mercado Livre** (só para comparação; a frente ML cobre)

- A Anvisa já fiscalizou o estoque Full (mar/2026).
- O ML descarta por validade e tem incentivo de armazenagem na linha de supermercado (xWw-95fez58, C).

**Amazon:** sem evidência coletada nesta frente.

### 5.2 Fiscalização: o que gera retirada

Padrão dos atos da Anvisa em 2026, todos N2:

1. **Alegação de saúde ou terapêutica no anúncio ou no rótulo.** É o motivo mais frequente. Exemplos: "evita câimbra", "recuperação mais rápida", tratamento de diabetes, "100 dores".
2. **Origem desconhecida e falta de regularização.** Exemplos: azeite Campo Ourique, "café de açaí" e sais.
3. **Ingrediente não autorizado** para a categoria, como constituinte não permitido em suplemento.
4. **Falta de estudo de estabilidade** que sustente o prazo de validade do rótulo. Um suplemento declarava 24 meses sem estudo, segundo a RE 1.045/2026.
5. **Rótulo em idioma estrangeiro e marca que sugere terapia.** Ambos aparecem na inspeção do CD do ML.

**Ponto de método:** o alvo da Anvisa é o produto anunciado, onde quer que esteja. Na ação de Cajamar, os fiscais também mandaram tirar a divulgação do site. Para quem vende alimento funcional, o risco está no texto do título, na descrição, no vídeo e na live, e não só no rótulo.

### 5.3 Café em particular

**Formato e preço por kg** ([OBS])

- O grão domina o topo da busca.
- O moído aparece como variação ou com a promessa "moído no dia do envio".
- A cápsula é linha à parte. Há ao menos três padrões de máquina, Nespresso, Dolce Gusto e Três Corações, e cada um exige linha de envase própria, segundo a fábrica em kqerLjGQAgY.

**Cápsula** ([PRÁTICA], C)

- O fabricante diz que uma saca torrada vira 10 mil cápsulas.
- Diz também que, vendendo a R$1 a cápsula, faz cerca de R$10 mil por saca, contra cerca de R$2 mil exportando o grão.
- É número de receita bruta sem custo, sem canal e sem período: número sem base. Serve como hipótese de agregação de valor, não como margem.

**Industrialização para terceiros (private label)** ([PRÁTICA], C)

- A mesma fábrica faz chá em cápsula para outra marca: custo de cerca de R$0,60, vendido a cerca de R$3,50 por unidade.
- O que a fábrica relata é a terceirização, a marca contratante não foi verificada.

**O que o consumidor compra** ([DADO], ABIC 2025, B)

- 55% compram extraforte ou tradicional.
- Especial é 11% das compras declaradas.
- "Foco no melhor preço" predomina como critério.
- 87% acham o produto com selo ABIC melhor.

**Por que isso importa no marketplace**

O consumidor médio não lê estilo: 48% não sabem a diferença entre estilos de café. Então título, foto e atributo carregam a explicação, e um selo de terceiro conta como credibilidade. Isso é inferência ligada ao [OBS] dos títulos.

### 5.4 Escada de margem em alimento (CM1 → CM2 → CM3)

O método vale sem corte de data. Os números são ilustrativos e saem das fontes citadas.

**Componentes que mudam no alimento:** taxa fixa por item (R$0,50 a mais = cerca de 0,6% num item de R$75 e quase 2% num de R$30; hEkVpRw_vNg), peso e cubagem (café e bebida são densos), envio excepcional do Full abaixo de R$20, baixa de estoque vencido, Devolução Fácil (R$0,49) e adicional de campanha (2% a 3%). Sem regra oficial Shopee de validade.
 (IYi2eifHqSY)

| Item | Valor |
|---|---|
| Preço | R$29,90 |
| Custo | R$12,00 |
| Imposto (6%) | R$1,79 |
| Comissão (20%) | R$5,98 |
| Taxa fixa | R$4,50 |
| **CM1** | **R$5,63 (18,8%)** |

A mesma fonte mostra que um item de R$19,90 com custo de R$6 caiu de R$1,77 para R$1,27 de margem. Um item mais barato, com custo de R$3, passou a dar prejuízo.

**CM2 (depois do Ads)**

O mesmo canal mostra loja com margem real de 9% depois de publicidade, num caso de marca de cosméticos. Fonte: [CASE] fraco, sem período nem base. Rebaixado para [PRÁTICA].

**Saídas usadas pelos praticantes**

- **Kit ou multipack como um único item**, para pagar uma taxa fixa só e subir o ticket. Cauê põe isso no "médio prazo" (96YaDbhhsAo).
- **Pedido mínimo por cupom** de valor mínimo, no curto prazo.
- **Passar de R$50 ou R$80** para entrar no Full Mais (≥R$50) e no subsídio Pix (≥R$80). Isso é inferência a partir das faixas oficiais e de praticantes.

A leitura de que o kit paga uma taxa fixa só é inferência: a fonte diz que a taxa é "por item vendido", e o kit é um item no anúncio.

### 5.5 Embalagem e kits que funcionam (evidência)

| Formato | O que se vê | Evidência |
|---|---|---|
| 250g, 500g, 1kg e 2/3kg na mesma loja ou anúncio | Preço por kg cai no tamanho maior | [OBS] C |
| Kit de origens (4x250g) | Produto próprio de marca de especial; também no ML | [OBS] C |
| Kit degustação (5x50g) | Ticket parecido com o de 1kg e preço por kg muito alto (R$311/kg) | [OBS] C |
| Kit de 2 a 10 unidades | Margem % menor por degrau, mais R$ | [PRÁTICA] 96YaDbhhsAo C |
| Combo de complementares | Ferramenta combo da Shopee | [PRÁTICA] 96YaDbhhsAo C |

**Sem evidência** de taxa de conversão ou de recompra por formato na Shopee Brasil.

### 5.6 Recorrência e assinatura

- **Shopee:** sem programa oficial de compra recorrente ou assinatura de produto para o comprador (sem evidência de que exista).
  - A recompra depende de cupom de seguidor (vale do resgate até 7 dias depois), cupom para compradores específicos e cupom de live (7i2f1rplBl0, 13/08/2026).
  - Também depende de Moedas Shopee, que saem de compras em indicados ou oficiais ([OFICIAL]).
- **ShopeeVIP:** R$9,90 por mês, para o comprador. Dá cupons de frete grátis acima de R$10 e cupons de R$5 acima de R$40. Segundo o praticante, o "frete grátis" cobre até R$20 (Kasbq8gziOg, 21/05/2026, C).
- **Fora do marketplace:**
  - assinatura própria de café é modelo citado por curso (iejwhe1DzM8, 10/03/2026). Promessas como "R$15.000 garantidos" com 100 assinantes são número sem base e vêm com CTA dominante: rebaixado para N7;
  - o canal "clube de café" é 0,6% do principal local de compra (ABIC 2025).
- **Benchmark de recompra de consumível na Shopee:** sem evidência. O único sinal é o caso de cosméticos, que usa CRM e mensagem de recompra a 60 dias, mas no site próprio (EitJfemXOXA).

### 5.7 Como a indústria organiza a operação

**Modelos observados**

1. **Indústria com Loja Oficial e gerente de contas** (3P com status): Danone, Pilão, Heineken e Unilever, segundo o blog oficial.
2. **Indústria que contrata agência ou operação terceirizada.** Exemplos:
   - Café Caldense com a Mamba no ML: mais de R$100 mil somados em menos de um ano, em [CASE] fraco, medido pela agência, com conflito de interesse;
   - MRT Marketplace, que se apresenta como "operação, não consultoria" para indústrias (xWw-95fez58).
3. **Distribuidor ou revendedor que cria marca própria** para escapar da margem apertada: fraldas, com terceirização da marca (8N5ktlBoTJ8); sugestão da MRT.
4. **Fábrica B2B que produz com a marca do seller** (white label): pet em Cafelândia, onde 90% dos clientes são e-commerce (9UVMD3UIQSQ); torrefação que envasa chá para outra marca (kqerLjGQAgY).

**Atritos de canal** ([PRÁTICA], C)

- A indústria corta o revendedor que cresce no marketplace (8N5ktlBoTJ8).
- A marca teme o distribuidor (EitJfemXOXA).
- O influenciador "oficial" da Shopee defende vender direto para "parar de depender de distribuidores" (aMlRuYMixC0, 13/07/2026, N7 por CTA e promessa).

**1P x 3P:** a Shopee opera como marketplace 3P. Sem evidência de compra 1P de alimentos pela Shopee Brasil. A MadeiraMadeira diz rodar 1P via dropshipping, mas no ML (QwL3e7QUnx4).

---

## 6. Erros comuns e mitos

1. **"Produto legalizado no Brasil pode ser vendido na Shopee."** Errado: a plataforma tem regras próprias e pode proibir item regular (post do Vendedor 360, 14/09/2026). Além disso, desde 21/09/2026 o anúncio novo sem atributo Anvisa nem sobe nas categorias listadas.
2. **"Se o rótulo está certo, o anúncio pode dizer o que quiser."** Errado: a Anvisa age sobre anúncios em plataformas por alegação não aprovada. Casos de 2026: sal, café de açaí e suplementos.
3. **"Loja Oficial dá 2x o dinheiro de volta."** Superado. O oficial de 2026 diz reembolso integral em cupom.
4. **"Basta pedir para virar Loja Oficial."** Sem formulário público. É por convite ou negociação com o gerente (B).
5. **"A Shopee zera a exposição por 21 dias se houver reclamação."** A tabela oficial mostrada por praticantes traz 21 dias de suspensão de benefícios com −20% de visibilidade na faixa de 9 a 11 pontos. "Zerar" não aparece. Ver a seção 3.2.
6. **"Ser Loja Oficial dá comissão menor."** Não é regra geral. Praticantes dizem que só grandes marcas negociam (r5oEfzPV324, OjxNoZ4Sums, C). O desconto de comissão documentado é o do Full Mais, aberto a qualquer vendedor elegível.
7. **"Mandar tudo para o Full é sempre melhor."**
   - Itens abaixo de R$20 pagam envio excepcional.
   - Erro de conferência dá multa.
   - Não há regra pública de validade para alimento.
   - No ML, estoque parado e retirada custam caro.
8. **Números sem base em conteúdo fraco** (sinais 1, 2 e 3):
   - "68% querem receber em 24h", atribuído à Capgemini sem ano nem amostra (MIRTO, xWw-95fez58);
   - "90% dos lojistas erram o básico" (iejwhe1DzM8);
   - "100 assinantes = R$15.000 garantidos" (iejwhe1DzM8);
   - "R$50.000 numa saca em cápsula" (kqerLjGQAgY).
   Tratar como hipótese N7.
9. **"Café de supermercado é carvão" e "café brasileiro é fraude"** (título de kqerLjGQAgY). É posicionamento de fabricante, sem medição independente. Não serve como dado de qualidade.
10. **Confundir faturamento com lucro em cases.** "Mais de R$100k em menos de um ano" (Café Caldense) e "R$1 milhão/mês" (fraldas) são faturamento bruto, sem margem nem base de comparação. Ficam rebaixados para [PRÁTICA].

---

## 7. Revenda/importação x indústria/marca própria

| Tema | [REVENDA] | [MARCA] |
|---|---|---|
| Atributo Anvisa | Depende do fornecedor ter registro ou notificação: "conversa com o fornecedor" (RvJiFGQiK3c). Sem o dado, não anuncia item novo | A indústria detém o número e controla a conformidade e o rótulo |
| Risco sanitário | Origem desconhecida ou importado sem regularização é o 1º alvo da Anvisa (azeite, sais, suplementos) | Responde pela alegação no rótulo e no anúncio e pelo estudo de estabilidade (validade) |
| Loja Oficial | Só ocorre por exceção | Caminho natural: o convite hoje prioriza "marcas e fabricantes" |
| Abastecimento | Pode ser cortado pela indústria quando cresce (8N5ktlBoTJ8) | Controla capacidade, mas imobiliza capital (RwYs9zPynLw) |
| Ads | Uso menor ou nulo em produto de terceiros (8N5ktlBoTJ8) | Verba concentrada na marca, que "precisa estar sendo mostrada" |
| Diferenciação | Preço, frete e kits próprios montados com itens de terceiros | Kits exclusivos, tamanhos por canal, atributos de origem, selos e conteúdo |
| Café | Revender marca de gôndola briga com a Loja Oficial da própria marca no topo ([OBS] Italle e Baggio) | Torrefação ou produtor pequeno aparece no top 40 com especial e microlote ([OBS]) |
| Margem | "Revenda sempre a margem vai ser baixa" (8N5ktlBoTJ8) | "Marca própria sempre vai ter uma margem um pouco melhor" (idem). Sem número |

---

## 8. Tabela de afirmações

| id | Afirmação | Tipo | Fonte | Data | Confiança |
|---|---|---|---|---|---|
| A1 | Atributo Anvisa obrigatório para anúncios novos desde 21/09/2026; legados mantidos "por enquanto" | OFICIAL via terceiro | RvJiFGQiK3c; c7WmiWzZu4E | 14 e 15/09/2026 | baixa |
| A2 | A planilha da Shopee lista 169 categorias, com indicação de obrigatoriedade | OFICIAL via terceiro | RvJiFGQiK3c | 14/09/2026 | baixa |
| A3 | Shopee proíbe medicamentos, inclusive "remédios naturais" | OFICIAL via terceiro | vendedor360.com.br/guia-completo-regras-da-anvisa... | 14/09/2026 | média |
| A4 | Anvisa revogou medida preventiva sobre a Shopee (RE 3.056/2026) sem isentar a regulação sanitária | OFICIAL N2 | gov.br/anvisa/.../sobre-revogacoes-de-resolucoes-e-medidas-preventivas-para-plataformas-digitais | 10/08/2026 | alta |
| A5 | Anvisa fiscalizou o estoque Full do ML em Cajamar e apreendeu suplementos e probióticos por registro, rótulo e alegações | OFICIAL N2 | gov.br/anvisa/.../anvisa-apreende-produtos-irregulares-em-deposito-do-mercado-livre | 18/03/2026 | alta |
| A6 | Alegação de saúde em anúncio online leva a proibição de alimentos e suplementos (sal, café de açaí, suplementos) | OFICIAL N2 | Anvisa: anvisa-proibe-sal-sem-registro-vendido-na-internet; po-para-decoracao...; anvisa-proibe-suplementos-alimentares-por-propaganda-irregular | 06/02, 19/03 e 07/08/2026 | alta |
| A7 | Anvisa abriu processo para rever normas de propaganda de alimentos, citando marketplaces e influenciadores | OFICIAL N2 | gov.br/anvisa/.../anvisa-aprova-abertura-de-processo-para-revisar-normas-da-propaganda... | 05/08/2026 | alta |
| A8 | Portaria SDA 570/2022 (classificação e rotulagem do café torrado) em vigor desde 01/01/2023 | OFICIAL via ABIC | abic.com.br/certificacoes/portaria570 | 20/05/2025 | alta |
| A9 | Tabela nutricional não é obrigatória para café | OFICIAL via ABIC | abic.com.br/institucional/legislacao | 10/12/2025 | média |
| A10 | Marketplace como principal local de compra de café: 0,8% → 3,5% (2023 a 2025) | DADO | ABIC, pesquisa 2025 (PDF) | set/2025 | média |
| A11 | Mercado Shopee foca em itens não perecíveis, com dias temáticos seg/qua/sex | OFICIAL | shopee.com.br/blog/mercado-shopee-como-fazer-suas-compras/ | 02/06/2026 | média |
| A12 | Lojas Oficiais: original com NF, reembolso integral em cupom, devolução em 30 dias, selo vermelho | OFICIAL | shopee.com.br/blog/lojas-oficiais/ | 02/06/2026 | média |
| A13 | Marcas de alimentos (Pilão, Danone, Bauducco, Fini, Heinz, Carrefour) são Lojas Oficiais | OFICIAL | idem | 02/06/2026 | média |
| A14 | Loja Oficial é por convite ou negociação, sem formulário público | PRÁTICA | OjxNoZ4Sums; r5oEfzPV324; _p1IBEyvCwo | 2022, 2024 e 2026 | média (pode estar superada) |
| A15 | Virar Loja Oficial deu +30% de vendas num dia comum | PRÁTICA (CASE rebaixado) | _p1IBEyvCwo | 02/06/2026 | baixa |
| A17 | Comissão até R$79,99: 20% + R$4,50 por item desde 01/10/2026 | OFICIAL via terceiro | IYi2eifHqSY; 9VOoazXt_aE; hEkVpRw_vNg | set a out/2026 | média |
| A18 | Faixas ≥R$80: 14% + R$16/20/26; subsídio Pix de 5% a até 8% | OFICIAL via terceiro | 9VOoazXt_aE; hEkVpRw_vNg | set a out/2026 | média |
| A19 | Full: CNPJ, Simples ou normal, nota >4,5, ≥5 pedidos/dia | OFICIAL | TUs6QYGqGrw | 04/08/2026 | média |
| A20 | Full Mais: ≥40% via Full; 0,5 a 2 p.p. em itens ≥R$50; crédito na 1ª semana | OFICIAL | 0oRYednAlHY | 04/08/2026 | média |
| A21 | Full: envio e armazenagem sem custo, só inconformidade é cobrada | PRÁTICA | OUC2vulFv8E | 27/04/2026 | baixa |
| A22 | Itens <R$20 no Full: R$1 a R$12,50 por unidade, mínimo de 15 unidades | PRÁTICA (tela) | ty0iwe3dV1I | 20/07/2026 | baixa |
| A23 | Multa de R$3 por erro de conferência no Full | PRÁTICA | RwYs9zPynLw | 01/09/2026 | baixa |
| A24 | 5 CDs de fulfillment (SP, PE, GO, RS, MG), 19 CDs no total | OFICIAL | blog CD MG | 07/05/2026 | média |
| A25 | Nenhuma regra oficial de validade ou temperatura para alimento no Full Shopee foi encontrada | lacuna | — | 14/10/2026 | — |
| A26 | Taxa Devolução Fácil de R$0,49 por venda desde maio/2026 | PRÁTICA | yAmvIlW11GY | 09/05/2026 | baixa |
| A27 | Adicional de 2% a 3% para eventos oficiais | PRÁTICA | 4oQLk8XXYP4 | 01/09/2026 | baixa |
| A28 | Penalidade em pontos trimestrais, multas de R$100 a R$1.500 e −5% a −30% de visibilidade | OFICIAL via terceiro | ThPsYQpMxJE; LLDUrAuF3qQ | mai e ago/2026 | média |
| A29 | Vídeo e Live: promoção verdadeira, proibidas réplicas, jornada dentro da Shopee | OFICIAL | aUqdtKFx5gM | 20/08/2026 | média |
| A30 | Busca "café em grãos": oficiais no topo, escada de tamanhos, R$67 a R$114/kg | OBS | observacao/lideres.md | 14/10/2026 | baixa |
| A31 | Títulos de café no topo listam atributos (espécie, torra, notas, SCA) | OBS | idem | 14/10/2026 | baixa |
| A32 | Kits de 2 a 10 unidades reduzem a margem % e aumentam a margem em R$ | PRÁTICA | 96YaDbhhsAo | 07/08/2026 | baixa |
| A33 | Taxa fixa por item pesa cerca de 2% em ticket de R$30 e cerca de 0,6% em R$75 | PRÁTICA (cálculo) | hEkVpRw_vNg | 13/10/2026 | média |
| A34 | Não há assinatura ou compra programada oficial para o comprador na Shopee | lacuna | 7i2f1rplBl0; Kasbq8gziOg | 2026 | baixa |
| A36 | Seller de fraldas concentra Ads na marca própria | PRÁTICA | 8N5ktlBoTJ8 | 09/09/2026 | baixa |
| A37 | Indústria cortou o abastecimento de revendedor que crescia no marketplace | PRÁTICA | 8N5ktlBoTJ8 | 09/09/2026 | baixa |
| A39 | Saca de 60 kg crua rende 42 a 50 kg torrados | PRÁTICA (faixa de 2 fontes) | kqerLjGQAgY; lWgirqh5BT8 | 2025 e 2026 | média |

---

## 9. Lacunas

1. **Documento oficial do atributo Anvisa.** Faltam a planilha das 169 categorias e o comunicado da Shopee. Não confirmei se café torrado, chá, cápsula e suplemento estão como "sim". Também não sei que número aceitar para café que, conforme a IN 281/2024, pode ter outra forma de regularização. Não li a IN.
2. **Política de produtos proibidos e restritos da Shopee Brasil (Central de Ajuda).** Não foi lida, porque o site é aplicação JS e a API recusou. Sem regra oficial de validade mínima, lote, temperatura ou bebida alcoólica.
3. **Regras de alimento no Full Shopee.** Faltam validade mínima no recebimento, descarte, FEFO e categorias aceitas. Os CDs se declaram multicategoria "moda, beleza, tecnologia", sem menção a alimento.
4. **Benchmarks de recompra de consumíveis, ruptura, content score e share of search na Shopee Brasil.** Sem fonte pública. As ferramentas (Nubimetrics, Avantpro, UpSeller) não publicaram nada sobre alimentos e café em páginas acessíveis. O sitemap do blog da Avantpro não tem posts de alimentos.
5. **Critérios e benefícios mensuráveis de Loja Oficial.** Não há página oficial de critérios de entrada. O efeito em visibilidade só tem relato (+30%, sem base). A existência de "Brand Ads" ou de dados exclusivos para marca na Shopee Brasil está sem evidência.
6. **Equivalente a Brand Registry na Shopee:** proteção de marca contra revendedor não autorizado e denúncia de PI. Não lido; sem evidência.
7. **Assinatura e recorrência.** Não há programa oficial. Benchmarks de "subscribe & save" ficam para a frente Amazon. Sem número para a Shopee.
8. **Cases de marcas de alimentos na Shopee com número, período e base.** Nenhum achado. Os cases de indústria com números são de moda, pet, ferramentas, fraldas e cosméticos, e o de café é do ML (Café Caldense, agência).
9. **Organização 1P/3P e agências full commerce dos grandes de alimentos na Shopee.** Sem fonte direta. Só a lista de Lojas Oficiais.
10. **Observação direta incompleta.** Faltaram vendidos, avaliações, fotos, frete e o tipo de loja dos itens, por bloqueio de login em 14/10/2026.
11. **Ação da Anvisa contra a Shopee que gerou a RE revogada.** A notícia de origem e a data da medida não foram achadas no índice de notícias de 2025 e 2026. Só a revogação ficou documentada.

## 10. Verificação (2026-10-14)

Método: tentativa de refutar cada afirmação na camada oficial. WebSearch indisponível (limite de buscas da sessão esgotado). WebFetch lê só as páginas estáticas do blog oficial (shopee.com.br/blog); Central do Vendedor, Shopee Uni e help.shopee.com.br são aplicações JS e retornaram só o título ("Seller Education Hub", "Help Center"). Nenhuma afirmação foi contestada; as não confirmadas ficam "sem fonte oficial" por falta de acesso, não por refutação. Tipo de todas as fontes oficiais citadas: [OFICIAL].

| id | veredito | fonte oficial (URL) | observação |
|---|---|---|---|
| R1 | SEM FONTE OFICIAL | não acessada (seller.shopee.com.br e help.shopee.com.br só em JS) | Só Vendedor 360 (praticante) afirma. Falta comunicado e lista das 169 categorias. Regra de 09/2026, dentro de 6 meses. |
| R2 | SEM FONTE OFICIAL | não acessada; blog oficial de taxas sem valores | Valores 20% + R$4,50 só em vídeos de praticantes. Blog oficial (shopee.com.br/blog) não traz comissão. Não confirmar o R$4,50 sem ver a política de taxas. |
| R3 | SEM FONTE OFICIAL | não acessada | Faixas 14%+R$16/R$20/R$26 e subsídio Pix 5% a 8% sem página oficial lida. |
| R4 | SEM FONTE OFICIAL | não acessada (vídeo oficial TUs6QYGqGrw não reverificado) | Fonte original é vídeo oficial de 04/08/2026, mas não revisto aqui; blog oficial de Full não traz os requisitos. Pode estar superada só após 02/2027. |
| R5 | SEM FONTE OFICIAL | não acessada (vídeo oficial 0oRYednAlHY não reverificado) | Mesmo caso de R4. Percentuais do Full Mais não vistos em texto oficial. |
| R6 | SEM FONTE OFICIAL | não acessada | Tarifas de envio excepcional e mínimo de 15 unidades só em vídeo de praticante. Regra de 07/2026 e 04/2026: a de 04/2026 passa de 6 meses, pode estar superada. |
| R7 | CONFIRMADA | https://shopee.com.br/blog/lojas-oficiais/ | Página (data exibida 02/06/2026) diz: produtos originais com nota fiscal, dúvida de autenticidade com reembolso integral em cupom para uso na plataforma, devolução de 30 dias, selo vermelho "Oficial". Política de consumidor com mais de 4 meses. |
| R8 | SEM FONTE OFICIAL | https://shopee.com.br/blog/lojas-oficiais/ (omissa) | A página oficial não descreve como virar Loja Oficial; só diz que marcas parceiras têm espaço próprio. A parte "convite/negociação, sem formulário" não tem confirmação oficial, e a ausência na página não prova que não exista formulário. |
| R9 | SEM FONTE OFICIAL | não acessada (política de pontos em help.shopee.com.br, JS) | Tabela de pontos e multas só por vídeo. Valores de multa e % de visibilidade não verificados; tratar com cautela. |
| R10 | SEM FONTE OFICIAL | não acessada | Taxa de R$0,49 do Devolução Fácil só por vídeo de 05/2026. Regra de mais de 5 meses, quase no corte de 6 meses. |
| R11 | SEM FONTE OFICIAL | não acessada | Adicional de 2% a 3% em campanhas só por vídeo de 09/2026. Sem página oficial lida. |
| R12 | SEM FONTE OFICIAL | https://shopee.com.br/blog/mercado-shopee-como-fazer-suas-compras/ | Metade confirmada: o blog oficial (data exibida 02/06/2026) diz foco em supermercado não perecível (alimentos e bebidas, cuidados com a casa, higiene, pets) e ofertas na segunda (lavanderia e limpeza), quarta (mercearia) e sexta (happy hour, bebidas e snacks). A metade "não há regra oficial de validade ou temperatura no Full" é afirmação negativa que não consegui verificar; mantém-se como lacuna. |

Resumo: 1 confirmada (R7), 0 contestadas, 11 sem fonte oficial (R1 a R6, R8 a R12). Para fechar R1 a R6, R9 a R11 é preciso abrir seller.shopee.com.br/edu e help.shopee.com.br com navegador (renderização JS) ou revisar os vídeos oficiais de 04/08/2026.
