# Vitrine do TikTok Shop BR: observação (2026-10-15)

## O que deu para observar
- **Vitrine direta: bloqueada.** `https://www.tiktok.com/shop` abriu um "Security Check" com captcha de quebra-cabeça na primeira carga. A observação parou ali, como manda a regra (não resolver captcha). Páginas de produto e shop.tiktok.com não foram abertas. Por isso, **preço, preço/kg, frete, vendidos, nota e avaliações não foram coletados nesta rodada.** [OBS]
- O que está em `vitrine.tsv` é **observação indireta**: vídeos de afiliados que apareceram na busca "café tiktok shop" (cards de busca e legendas, 2026). Serve para ver *quem* vende café e *como*, mas não para ver números da página de produto. [OBS]

## Padrões (indiretos, só café; nada de outras categorias foi visto em página de produto)
1. **No café, a venda passa pelo afiliado, não pela loja.** A mesma marca aparece em vários perfis de afiliados diferentes: Café Italle em 6 ou mais (ex.: @dicasdorogerinho 7681062374006131986, @giessencial 7678723520154684693) e Café Varanda de Vó em pelo menos 2 (@robsonelana.shop 7634174999506488597, @diegodicas 7630250530144652551). [OBS]
2. **O formato de pacote mais citado é 1 kg ou kit** (1 kg em grãos ou moído, 2 x 500 g, kit com 6 cafés especiais, kit degustação). O 250 g aparece pouco (@progressoshop 7632094027600383253). [OBS]
3. **As legendas falam de preço e de selo, quase nunca de origem.** Os apelos mais comuns são "preço de café comum", promoção e "oferta do dia". Os atributos citados são 100% arábica, gourmet e selo ABIC. Origem só aparece de passagem ("Sul de Minas", "uma região diferente"). [OBS]
4. **Café especial com conta própria e pouca distribuição de afiliados tem engajamento baixo** (@lojadocafe 7665709548539235605, 5 curtidas no card), enquanto as marcas espalhadas entre afiliados somam milhares de curtidas. É uma amostra pequena e não prova causa. [OBS]
5. **Acessórios de café (moedor, filtro, xícara, cafeteira) aparecem mais na busca do que o próprio café.** O vídeo de filtro de pano reutilizável @juliana.vivencia 7683563490686061845 tem 11,1 mil curtidas. [OBS]

## Lacunas para a próxima sessão
- Abrir páginas de produto (PDP) de café e de 3 a 5 líderes de outras categorias **só se** a vitrine abrir sem captcha (outro horário ou outro dispositivo, sempre sem login), ou pegar esses dados por fontes de terceiros (Kalodata, FastMoss, Shoplus), marcando-os como [DADO] de terceiro.
- Confirmar preço e preço/kg de Italle, Varanda de Vó, Coffee Mais e SUPERCAFÉ direto na página.

## Observação direta da vitrine (2026-10-16, ~01:20–01:35, Claude in Chrome, sessão logada)

Depois que o Rafael resolveu o captcha em `tiktok.com/shop`, a vitrine pública abriu em
`shop.tiktok.com/br` (Bytedance Brasil Tecnologia LTDA no rodapé). A versão web não tem caixa de
busca de produto; a navegação é por categoria: **Alimentos e bebidas** (`/br/c/food-beverages/700437`)
→ **Bebidas** (`/br/c/drinks/914824`) → **Café** (`/br/c/coffee/700612`). Amostra: 50 cards da categoria
Café (`vitrine-cafe-categoria.tsv`) e 3 páginas de produto (linhas novas em `vitrine.tsv`).

**Padrões medidos [OBS]:**
1. **Preço riscado é a regra:** quase todos os cards mostram preço riscado, com descontos de 15% a 76%
   (vários perto de −40% a −50%). Flash sale com contador regressivo aparece em 9 de 50 cards.
2. **Mix da categoria Café:** cápsulas (Dolce Gusto, Delta Q, compatíveis Nespresso, Orfeu, Giói),
   solúvel e "café funcional" (SuperCoffee/Caffeine Army, Brainstorm) dividem a vitrine com grãos e
   moído. Torrefações pequenas de café especial aparecem (Coffee Mais, Minas Estate, América Oro,
   Fazenda Santa Alcina, Mezzanotte, Grassy Caffè, Bry Coffee, Tiger/Unique).
3. **Preço do café em grãos 1 kg:** R$ 45,99 (Bry, com −67%), R$ 79,00 (Minas Estate, 85 pts),
   R$ 99,90 (Grassy), R$ 110,00 (Tiger/Unique). 250 g de especial a R$ 16,45–24,10 (R$ 66–96/kg) e
   500 g a R$ 31,99–46,90.
4. **Vendidos no card × na página:** o card da categoria mostrou "61 vendidos" e a página do mesmo
   produto (Coffee Mais 250 g) "5,1 mil vendidos". O card parece mostrar vendas recentes e a página o
   acumulado: não use o número do card como volume total.
5. **Poucas avaliações para o volume:** 5,1 mil vendidos com 9 avaliações (Coffee Mais); 52 vendidos
   com 8 (Minas Estate); 114 com 9 (SuperCoffee). As notas ficam entre 4,8 e 5,0.
6. **Frete:** convivem "Frete grátis" e frete pago pelo comprador (Minas Estate 1 kg: "a partir de
   R$ 7,31 neste pedido"). Vários cards mostram só "Free shipping" no lugar do título.
7. **Live como canal de café:** uma avaliação do Coffee Mais cita "comprado em live" (kit de 6). As lojas
   de torrefação oferecem kits (3 e 6 pacotes de variedades) e kit degustação em drip.
8. **Ruído na categoria:** itens que não são café (semente de pastagem, um livro) aparecem na categoria:
   a categorização é do vendedor e não é limpa.

**Limites:** uma passada, um horário, sessão logada (pode haver personalização); sem busca por termo
(a web não tem busca pública de produto); vídeos e afiliados vinculados não foram contados por página;
só 3 páginas de produto; nenhuma categoria fora de alimentos nesta passada.
