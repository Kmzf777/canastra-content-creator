# Mercado Livre: o que os líderes têm em comum (observação direta)

Data da observação: 2026-10-14. Navegador com sessão de comprador já aberta (endereço de entrega em MG), sem login novo. Foram 13 páginas, com pausa de 8 a 15 s entre elas e **nenhum captcha**. Os dados linha a linha estão em `lideres.tsv`. Todas as afirmações abaixo são **[OBS]**, salvo quando outro tipo estiver indicado.

## Alimentos e bebidas / café

1. **O FULL é praticamente obrigatório na primeira página.** Na busca "cafe em graos", 26 dos 40 primeiros resultados têm selo FULL; em "cafe moido", 21 de 30; em "cafe capsulas", 22 de 25. Os anúncios sem FULL que aparecem no topo mostram "Frete grátis" e quase sempre são de lojas pequenas de café especial com poucas vendas (+25 a +500). As exceções com volume são Appassionato e Serra do Encontro, que têm +1000 a +10mil vendidos. Fontes: lista.mercadolivre.com.br/cafe-em-graos, /cafe-moido e /cafe-capsulas.
2. **O catálogo (página /p/) concentra a disputa, e a buy box não é necessariamente da marca.**
   - Pilão 1kg: 72 vendedores no mesmo produto, e quem ganhava era um supermercado revendedor (MLB35944622).
   - Café Italle 1kg: ganhava a loja oficial de outra empresa (Healthy Coffee), com a própria loja oficial Italle mais cara na lista de "outras opções" (MLB26184226).
   - Ventilador Mondial: ganhava um vendedor com +50 vendas e "Atendimento ruim" (MLB18932156).
   - Nota, avaliações e "vendidos" pertencem ao produto de catálogo, e não a quem vende.
3. **Lojas oficiais de marca com sortimento amplo ocupam várias posições.**
   - Orfeu aparece 5 vezes nos 40 primeiros resultados de grãos (1kg, 250g, Bourbon Amarelo, Intenso) e ainda com drip e cápsulas.
   - Café Italle aparece em grãos (1º), moído (1º) e cápsulas (50 e 100 un).
   - Santa Monica, Baggio, Melitta e 3 Corações também aparecem com várias embalagens.
   - O padrão é cobrir formatos (grão, moído, cápsula, drip) e tamanhos (250g, 500g, 1kg) com uma linha inteira.
4. **O preço é exibido em camadas: "de" riscado, preço no Pix e preço em outros meios.** Todos os líderes de alimentos mostram desconto no Pix, entre 8% e 53% OFF. A página de produto mostra "Preço por quilo" (Italle R$67/kg; Pilão R$83,89/kg). Faixas de preço por kg observadas: café de supermercado entre R$32 e R$84/kg, gourmet ou especial de marca entre R$90 e R$160/kg, e microlotes acima de R$200/kg.
5. **Os líderes usam desconto por quantidade dentro do anúncio:**
   - Appassionato: 5 un a R$92/un, 10 un a R$89,90/un;
   - Pilão: 5 un a R$66,39/un;
   - Italle: "levando 100 ou mais" a R$48,80/un.
   
   Kits também aparecem como anúncios separados (2un, 4x250g, café + moedor).
6. **Selos e prova social no topo da página:**
   - "MAIS VENDIDO" com posição no ranking da categoria (ex.: "3º em Café Moído e em Grão", "20º em Cápsulas");
   - contagem de vendidos ("+100 mil");
   - nota de 4.7 a 4.9 com milhares de opiniões (Italle 6.703; Orfeu 3.410; Italle cápsulas 5.348);
   - oferta relâmpago com contador regressivo (Italle).
7. **Os vendedores líderes têm reputação no topo da escala.** Italle, Orfeu e Healthy Coffee são MercadoLíder Platinum; Appassionato é Gold. As lojas oficiais exibem seguidores (Italle +35,3 mil; Orfeu +11,7 mil) e "+100 Produtos".
8. **O título é escrito para a busca, não para a marca.** O líder em grãos usa um título genérico ("Cafe Graos Torrado Torra Media Arábica Em Grãos 1kg Gourmet"), sem a marca na frente. O de cápsulas repete "cápsula" 4 vezes. Marcas tradicionais (Orfeu, Pilão, Melitta) usam um título curto com marca + formato + peso + torra.
9. **Galeria:** os produtos de café abertos têm de 6 a 9 miniaturas. Houve miniatura de vídeo confirmada no líder Italle; nos demais, a detecção automática de vídeo não foi confiável (marcado como "?" no TSV).
10. **No top 20 de Alimentos e Bebidas só há marcas nacionais muito conhecidas.** Café aparece com União 500g (6º, +500mil vendidos) e Melitta 500g (12º). Nesse topo o preço é de supermercado (R$16 a R$22 por 500g) e as entregas são do FULL/Supermercado.

## Outras categorias (líderes gerais)

- **Marca própria de importado com título longo e preço "de/por" agressivo.**
  - Redfin (controle): 1º em Gamepads, título de cerca de 200 caracteres empilhando compatibilidades, 43 mil opiniões, preço de R$114,90 por R$41,32, vendedor com +1 M vendas (MLB39960346).
  - Woosh (mixer): 1º em Mixers, 80% OFF, loja oficial com +500 mil vendas (MLB20306137).
  - Esse padrão é **específico de importação/marca própria de importado**.
- **Marca nacional estabelecida:** Mondial é 1º em Ventiladores com cerca de 200 mil opiniões e variações de cor e voltagem no mesmo catálogo (MLB18932156).
- O padrão se repete fora de alimentos: selo "MAIS VENDIDO + Nº na categoria", preço no Pix, desconto por quantidade (20 un, 2 un) e variações agrupadas.

## O que vale para indústria/marca própria e o que é de revenda

- **Indústria/marca:** loja oficial, linha completa de formatos, FULL, preço por kg competitivo dentro da faixa do segmento, desconto progressivo e reputação Platinum (Orfeu, Italle, Appassionato, Santa Monica).
- **Revenda:** disputar a buy box de catálogos de marcas grandes por preço (Pilão com 72 ofertas, Melitta via Emporio Villamarin, Mondial via BAMBROZIO). Quem revende não controla título, fotos nem avaliações, porque são do catálogo.

## Limitações

- O rótulo "Patrocinado" não foi capturado nos cards. Por isso não foi possível separar o resultado orgânico do Product Ads.
- O selo FULL só foi medido nos cards da busca; na página de produto a detecção falhou.
- "Vendidos" aparecem em faixas ("+10mil"), não em números exatos.
- Os resultados de busca refletem um comprador com CEP em MG; o prazo de entrega e o FULL Super podem variar por região.
