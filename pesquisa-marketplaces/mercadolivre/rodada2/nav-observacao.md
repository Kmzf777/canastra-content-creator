# Rodada 2 · nav-observacao: orgânico x patrocinado na busca do Mercado Livre

Frente: observação direta com protocolo (LACUNAS §4 item 30; §0.4). Data de acesso: 2026-10-15, entre 13:47 e 13:57 (horário de Brasília). Ferramenta: Claude in Chrome, numa aba própria, fechada no fim. Sessão de comprador já aberta e logada; nenhum login novo. Nenhum captcha apareceu.

Dados brutos: `mercadolivre/rodada2/nav-observacao.tsv`, com 168 linhas: 6 termos × 24 posições, mais uma 2ª passada de "café em grãos 1kg".
Prints: pasta `mercadolivre/rodada2/nav-observacao-prints/`.

## Resumo

- **Como identificar o patrocinado pelo DOM.** O rótulo visível no card é **"Ad"**, não "Patrocinado". Três sinais coincidem em 100% dos casos (45 de 45 cards patrocinados nas passadas com as três checagens):
  1. elemento `a.poly-component__ads-promotions`, com texto "Ad", dentro de `.poly-card__footer`;
  2. atributo `aria-label="Patrocinado"` no card;
  3. link do card apontando para `click1.mercadolivre.com.br/mclics/...`, o rastreador de clique de anúncio.

  O banner de marca (Brand Ads) usa outro seletor, `.bads-brand-wrapper .bads-top-search-no-image__promoted-text`, também com o texto "Ad".
- **Onde caem os patrocinados.** O padrão foi fixo nos 6 termos: posições **1–4 e 13–16** da grade. Na página inteira, os blocos seguem a cada 12 posições: 1–4, 13–16, 25–28, 37–40, 49–52. Isso dá 8 de 24 (33%) nas 24 primeiras posições. A exceção foi "ração gato 10kg": a posição 15 veio orgânica, então foram 7 de 24.
- **Banner de marca.** Cada página teve 1 banner de marca acima da grade (Brand Ads, com "Ir para a loja"), fora da contagem das 24 posições.
- **O mesmo anúncio aparece duas vezes.** Em café e em ração, o mesmo produto aparece pago e também orgânico nas 24 primeiras posições:
  - café em grãos: 4 casos;
  - cápsulas: 3 casos;
  - café moído: 1 caso;
  - ração: 3 casos.

  Em fone e garrafa não houve nenhum caso.
- **Café é diferente das outras categorias.**
  - Nas buscas de café, 83% a 92% dos 24 primeiros resultados são cards de **"Full Super"**, no formato `poly-card--CPG` (supermercado). Esses cards não mostram nota, vendidos, vendedor nem "frete grátis"; mostram só "Chegará sábado".
  - Ainda em café, há um carrossel "Adicione mais de FULL SUPER" logo abaixo do banner.
  - Nas outras categorias aparece o FULL comum ("Enviado pelo FULL"), o frete grátis chega a 92–100% e a loja oficial a 29–67%.

## Achados por item

### Contexto de cada página (vale para os 6 termos)

| Campo | Valor |
|---|---|
| Data | 2026-10-15 |
| Logado | sim (conta já aberta no Chrome) |
| CEP no topo | **não exibido**: o topo mostra "Enviar para …" com o endereço salvo da conta, sem CEP. Rua e nome foram omitidos por privacidade |
| Ordenação | "Mais relevantes" (padrão) |
| Itens na grade | 64 (cafés), 68 (cápsulas, fone, garrafa), 47 (ração) |
| Captcha | não |

| # | Termo | Hora | URL | Total exibido | Print |
|---|---|---|---|---|---|
| 1 | café em grãos 1kg | 13:47 (2ª passada 13:57) | https://lista.mercadolivre.com.br/cafe-em-graos-1kg | 1.569 (2ª: 1.566) resultados | `nav-observacao-prints/01-cafe-em-graos-1kg.jpg` |
| 2 | café moído | 13:50 | https://lista.mercadolivre.com.br/cafe-moido | +9.999 | `02-cafe-moido.jpg` |
| 3 | cápsulas nespresso compatível | 13:50 | https://lista.mercadolivre.com.br/capsulas-nespresso-compativel | 1.714 | `03-capsulas-nespresso-compativel.jpg` |
| 4 | fone bluetooth | 13:52 | https://lista.mercadolivre.com.br/fone-bluetooth | +9.999 | `04-fone-bluetooth-carregando.jpg` (só cabeçalho e spinner; ver Aberto) |
| 5 | garrafa térmica | 13:54 | https://lista.mercadolivre.com.br/garrafa-termica | +9.999 | `05-garrafa-termica.jpg` |
| 6 | ração gato 10kg | 13:55 | https://lista.mercadolivre.com.br/racao-gato-10kg | 1.433 | `06-racao-gato-10kg-carregando.jpg` (só cabeçalho) |

Os prints com conteúdo mostram a parte de cima da página: banner de marca com "Ad", filtros e o carrossel Full Super nos cafés. A grade foi lida pelo DOM. Os caminhos dos prints são relativos a `pesquisa-marketplaces/mercadolivre/rodada2/`.

### Contagem por termo (posições 1–24)

| Termo | Patrocinados (posições) | % FULL (tipo) | % frete grátis | % loja oficial | Patrocinado repetido como orgânico (pago → orgânico) |
|---|---|---|---|---|---|
| café em grãos 1kg | 8: 1,2,3,4,13,14,15,16 | 83% (20, todos Full Super) | 17% (4, todos patrocinados) | 4% (1) | 1→5, 2→7, 4→6, 15→9 |
| café moído | 8: 1–4, 13–16 | 83% (20, Full Super) | 17% (4) | 0% | 2→5 |
| cápsulas nespresso compatível | 8: 1–4, 13–16 | 92% (22, Full Super) | 8% (2) | 8% (2) | 3→11, 4→5, 14→12 |
| fone bluetooth | 8: 1–4, 13–16 | 88% (21, "Enviado pelo FULL") | 92% (22) | 67% (16) | nenhum |
| garrafa térmica | 8: 1–4, 13–16 | 42% (10, FULL) | 100% | 29% (7) | nenhum |
| ração gato 10kg | 7: 1,2,3,4,13,14,16 | 38% (9, FULL) | 100% | 33% (8) | 1→24, 2→8, 4→5 |
| café em grãos 1kg, 2ª passada (10 min depois) | 8: 1–4, 13–16 | 83% (Full Super) | 17% | 4% | os ocupantes das posições 13 e 16 mudaram |

FULL entre patrocinados e orgânicos:

| Termo | Patrocinados com FULL | Orgânicos com FULL |
|---|---|---|
| café em grãos | 4 de 8 | 16 de 16 |
| café moído | 4 de 8 | 16 de 16 |
| cápsulas | 7 de 8 | 15 de 16 |
| fone | 7 de 8 | 14 de 16 |
| garrafa | 2 de 8 | 8 de 16 |
| ração | 3 de 7 | 6 de 17 |

Nos cafés, os patrocinados sem Full Super são os únicos cards com nota, vendidos e "Frete grátis". Exemplos: posições 3, 13, 14 e 16 de café em grãos.

### O que muda entre café e as outras categorias

1. **Formato do card.** Café aparece dentro da vitrine de Supermercado:
   - card `poly-card--CPG` com o selo "Full Super";
   - prazo "Chegará sábado", sem "grátis";
   - sem nota, vendidos e vendedor no card.

   Nas outras três categorias, o card padrão mostra nota, vendidos, vendedor ou marca e frete.
   Consequência para a pesquisa: em café, o orgânico do topo é quase todo Full Super. O frete grátis medido no card é baixo (8–17%) porque o card de Full Super não exibe frete. Esse número não quer dizer que o frete seja pago.
2. **Loja oficial** é rara no topo de café (0–8%) e comum em fone (67%).
3. **Sinal social no card.** Em café, só 2 a 4 dos 24 cards mostram nota. Nas outras categorias, 21 a 23.
4. **Patrocínio.** Não muda entre categorias: os mesmos slots (1–4, 13–16) e a mesma proporção (33%). A diferença é quem ocupa o slot. Em café, metade ou mais dos patrocinados também são Full Super, e vários se repetem logo abaixo como orgânicos.
5. **Frete grátis em itens baratos (fora de café).** Itens de R$19,40 (fone) e R$23,99 (garrafa) mostram "Frete grátis ou rápido", abaixo da faixa de R$79. Não foi apurado se isso vem da conta, de campanha ou de regra nova; ver Aberto.

### Seletores que funcionaram (para repetir a observação, item 33)

- Grade: `li.ui-search-layout__item`.
- Título: `.poly-component__title`.
- Preço atual: `.poly-price__current .andes-money-amount__fraction` e `__cents`.
- Patrocinado: `a.poly-component__ads-promotions` (texto "Ad"), ou `[aria-label="Patrocinado"]`, ou link com `mclics`.
- FULL: `[aria-label]` com "Full Super" ou "Enviado pelo FULL".
- Frete: `.poly-component__shipping-v2`, com texto "Frete grátis", "Chegará grátis …" ou "Frete grátis ou rápido".
- Loja oficial: `.poly-component__seller svg[aria-label="Loja oficial"]`.
- Nota e vendidos: `.poly-component__review-compacted`.
- Selo: "MAIS VENDIDO", "OFERTA DO DIA", "OFERTA IMPERDÍVEL".
- Banner de marca: `.bads-brand-wrapper`.

Limitações dos seletores:
- Na 1ª passada dos três cafés, o sinal `aria-label="Patrocinado"` não foi testado. A 2ª passada de café em grãos confirmou os três sinais juntos.
- O frete dos cafés na 1ª passada foi lido no texto do card inteiro.
- A medalha MercadoLíder não aparece nos cards da busca; ficou n/d.

## Tabela de afirmações novas

| id | afirmação | tipo | fonte | data | confiança | fecha |
|---|---|---|---|---|---|---|
| R2-OBS-1 | Na busca do ML, o card patrocinado leva o rótulo visível "Ad" (`a.poly-component__ads-promotions`), mais `aria-label="Patrocinado"` e link `click1.mercadolivre.com.br/mclics`. Os três sinais coincidiram em 45 de 45 cards | [OBS] | URLs dos 6 termos (tabela acima) | sem data; acesso 2026-10-15 | alta | §4 item 30; LACUNAS §0.4 / §1.0 (ads "sem Patrocinado"); consolidado §7 item 11 ("não capturou o rótulo") |
| R2-OBS-2 | Os patrocinados ocupam as posições 1–4 e 13–16 da grade, em blocos de 4 a cada 12 posições (25–28, 37–40, 49–52), igual em 6 de 6 termos: 8 de 24 (33%) no topo. Exceção: ração, posição 15 orgânica | [OBS] | idem | acesso 2026-10-15, 13:47–13:57 | alta para esta sessão, logada e de um único horário | §4 item 30; ADS Q9 (parte "quanto se usa Ads" no topo da busca); divergência 13 |
| R2-OBS-3 | Há 1 banner de Brand Ads ("Ad", "Ir para a loja") acima da grade em todas as 6 buscas | [OBS] | idem; prints 01, 02, 03, 05 | acesso 2026-10-15 | alta | ADS Q1/Q2 (formato Brand Ads visível ao comprador) |
| R2-OBS-4 | O mesmo produto aparece patrocinado e orgânico nas 24 primeiras posições: café em grãos 4×, cápsulas 3×, ração 3×, café moído 1×; fone e garrafa 0× | [OBS] | nav-observacao.tsv | acesso 2026-10-15 | média: identidade por título e preço, sem ID do item | §4 item 30; ADS Q5 (indício de canibalização, sem medir incrementalidade) |
| R2-OBS-5 | Em buscas de café, 83–92% dos 24 primeiros resultados são cards "Full Super" (formato supermercado), sem nota, vendidos, vendedor nem frete grátis exibidos, com um carrossel "Adicione mais de FULL SUPER" | [OBS] | URLs 1–3; prints 01–03 | acesso 2026-10-15 | alta | §1.3 Q3 (efeito do Full na exposição, observado e não causal); §1.7 / §1.9 (Full Super e Supermercado) |
| R2-OBS-6 | Fora de café, o FULL comum ("Enviado pelo FULL") vai de 38% a 88% do topo, o frete grátis de 92% a 100% e a loja oficial de 29% a 67%. Em café, a loja oficial fica em 0–8% | [OBS] | URLs 4–6 | acesso 2026-10-15 | alta para esta amostra | §1.3 (FULL só nos cards); §1.5 produto-mix |
| R2-OBS-7 | O topo da busca não exibe CEP para o comprador logado; mostra só "Enviar para" com o endereço salvo | [OBS] | todas as URLs | acesso 2026-10-15 | alta | protocolo de observação (§0.4: "CEP registrado") |
| R2-OBS-8 | Itens de R$19,40 e R$23,99 exibiram "Frete grátis ou rápido" no card | [OBS] | fone (posição 20), garrafa (posição 17) | acesso 2026-10-15 | média: pode depender da conta | levanta pergunta para preco-promocao R2/R3 (frete por faixa) |

## Aberto

- **2º horário.** A 2ª passada (café em grãos, 13:57) veio só 10 minutos depois. Não vale como segundo horário do protocolo. Falta repetir os 6 termos em outro turno (noite) e, se possível, deslogado e com CEP explícito.
- **Prints com a grade.** Com a janela oculta, o screenshot dava timeout depois da renderização. Os prints de fone e ração mostram só o cabeçalho. Os de café e garrafa mostram banner e filtros, não os 24 cards; os dados da grade vieram do DOM.
- **Medalha MercadoLíder.** Não aparece no card da busca. Exige abrir o anúncio ou a página do vendedor; não foi feito.
- **Identidade dos itens.** Os itens repetidos foram casados por título e preço. O ID MLB do anúncio patrocinado fica escondido atrás do link `mclics`.
- **"Frete grátis ou rápido" abaixo de R$79.** Não foi apurado se é benefício da conta, campanha ou regra nova.
- **Personalização.** A sessão é de uma conta logada. Não se sabe quanto do ranking orgânico e da escolha dos anúncios é personalizado; falta comparar com uma sessão deslogada.
- **Série temporal (item 33).** Não iniciada.
