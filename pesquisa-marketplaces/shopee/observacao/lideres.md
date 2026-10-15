# Shopee: padrões dos líderes (observação direta, parcial)

Data da observação: 2026-10-14. Não houve login. A observação foi interrompida porque a Shopee passou a exigir login.

## O que aconteceu

- **Página 1:** a busca "café em grãos" (ordenada por vendas) abriu. Foi preciso escolher o idioma Português (BR). O banner de cookies **não** foi aceito.
- **Página 2:** o produto Café Italle 1kg abriu por um instante na vitrine "Lojas Oficiais" e logo redirecionou para `/verify/traffic/error` com a mensagem "Login Necessário".
- **Página 3:** depois de 10 s, a busca "café moído" também caiu na mesma tela de login.
- Não apareceu captcha, mas era um bloqueio de verificação de tráfego/login. Pela regra de não fazer login, parei a Shopee aqui. **Não foi possível medir:** vendidos, número de fotos, vídeo, nº de avaliações, frete, loja dos itens e as listas de mais vendidos de outras categorias.
- Os dados estão em `lideres.tsv` (1 linha de resumo da busca e 9 líderes de café). Todas as afirmações abaixo são **[OBS]** feitas a partir da página 1, fonte `https://shopee.com.br/search?keyword=café em grãos&sortBy=sales`.

## Padrões vistos na busca de café em grãos

1. **Lojas oficiais de marca no topo.** Café Italle é o 1º com selo "Oficial" e também tem 1kg torra escura e 3kg. Baggio aparece com selos "Full" e "Oficial". A marca líder é a mesma do Mercado Livre (Italle).
2. **Escada de tamanhos da mesma loja.**
   - Italle: 1kg a R$76,90 e 3kg a R$194,31 no Pix, que dá R$64,77/kg.
   - Bororó: 1kg a R$79,90 e 2kg a R$151,91.
   - Patrick Coffees: 500g e 1kg.
   - Goiabeiras: 500g e 1kg.
   
   Também é comum ter variação 250g/500g/1kg dentro do mesmo anúncio.
3. **Muitos torrefadores e produtores pequenos de MG e SP entre os 40 primeiros.** O card mostra a UF de origem, e Minas Gerais predomina. Há especiais de 84 pontos acima de R$100/kg no top 20 (Patrick Coffees R$114/kg), além de microlote e kit degustação 5x50g. Isso difere do Mercado Livre, onde o topo é dominado por FULL e marcas grandes.
4. **O título vende atributos.** Usa barras verticais e lista de atributos, por exemplo:
   - "100% Arábica | Torra Média | Notas de Chocolate e Caramelo | Moído Dia do Envio";
   - pontuação SCA ("84pts");
   - variedade (Arara, Catuaí, Mundo Novo);
   - escassez ("ÚLTIMO LOTE SAFRA 2025");
   - emoji 🔥.
5. **Preço de referência riscado e desconto** em quase todos os itens (de -5% a -56%). Vários mostram o preço "no Pix".
6. **Selos visíveis:** "Indicado" (aparece em muitos cards de vendedores menores), "Full" e "Oficial". A maioria dos cards tem ícone de vídeo, ou seja, vídeo na galeria/capa.
7. **Faixa de preço por kg no top 40:** de cerca de R$67/kg (Italle, Profeta, Origem) a R$114/kg (especiais). Microformatos chegam a R$311/kg (degustação).

## Específico de revenda vs. marca própria

- Quase todos os líderes observados são **marca própria/torrefação** vendendo direto (Italle, Bororó, Baggio, Patrick, Coffee Mais, Goiabeiras, LOFFE).
- Não deu para identificar revendedores sem abrir as páginas de produto.

## Limitações

Amostra de uma única página de busca, sem login e sem dados de vendidos. Use como indício, não como ranking.
