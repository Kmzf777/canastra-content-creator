# Shopee: o que os criadores de Instagram/TikTok ensinam (notas do analista social)

Data da análise: 2026-10-14. Pesquisa neutra sobre como os melhores operam a Shopee Brasil. Este documento não traz recomendação para nenhuma empresa.

## Base e método

- **Instagram:** 36 Reels listados em `posts.tsv` (abr a out/2026). Há transcrição de 15 deles, e 2 não têm fala (DX2gvF9Mb1w, DYYN1CbpdlC). Dos outros 21, só a legenda foi usada.
- **TikTok:** 20 vídeos listados em `tiktok.txt`. Há transcrição de 8, e 2 deles sem fala (7400447061402963206, 7587199517229927700).
- **Datas dos TikToks:** foram derivadas do ID do vídeo (o timestamp fica nos bits altos).
- **Código de citação:** o post do Instagram aparece como `IG:código`, que equivale a https://www.instagram.com/reel/código/. O TikTok aparece como `TT:@perfil/ID`.
- **Qualidade das transcrições:** foram feitas com whisperx small. Nomes e números podem ter erro, por exemplo "Chopin"/"Shoppettes" = Shopee/Shopee Ads e "rouas" = ROAS. Números de tarifa ditos em vídeo foram conferidos entre fontes sempre que possível.
- **Quanto vale cada coisa:** o conteúdo social é [PRÁTICA] de praticante, não regra oficial. Quando um criador cita tarifa ou política, a afirmação aparece como "[OFICIAL] segundo o criador" e precisa ser confirmada na Central do Vendedor.
- **Corte de 6 meses:** regra de plataforma com data anterior a 2026-04-14 recebe a marca **(pode estar superada)**.

---

## 1. Ads (Shopee Ads)

Esta é a frente com mais conteúdo, com cerca de 40% dos posts. Há consenso em alguns pontos e divergência em outros.

### Como a ferramenta está hoje, segundo os criadores

- **Opções ao criar campanha:** "Promover meus produtos", "Promover produtos novos" (listados há menos de 30 dias) e "Promover minha loja" (busca). Fonte: IG:DZITqmpOnoO (Leonardo Lopes, 2026-06-03) e TT:@preciosatshirts/7656131679282564373 (2026-06-27). [PRÁTICA]
- **Tipos de lance:** existe o lance automático "Meta de ROAS" (ROAS alvo), existe o "GMV Max" (loja ou produto, com ROAS sugerido pela Shopee) e existe o lance manual por clique, com descoberta e busca separadas, lance dinâmico e colocações "Descoberta do Dia" e "Você também pode gostar". Fontes: IG:DZITqmpOnoO; IG:DXsGMoHHIvy (Leonardo Gutemberg, 2026-04-28); TT:@gabidamadrepe/7489198895331904773 (2025-04-03, **pode estar superada**). [PRÁTICA]
- **Controles na campanha automática:** depois de criada, só dá para mexer em orçamento diário, ROAS alvo e "Impulsão rápida". Leonardo Lopes resume a campanha automática como engessada (IG:DZITqmpOnoO, 2026-06-03). [PRÁTICA]
- **O ROAS alvo não é garantido.** Com alvo alto, a Shopee pode simplesmente não gastar. A campanha entrega abaixo do alvo, ou só dá impressão sem gasto, porque "tem outros vendedores dispostos a receber menos" (IG:DZITqmpOnoO). Gutemberg mostra o mesmo: com alvo 25 a campanha entregou 16, e com alvo 20 entregou 18 (IG:Dbv4M7fOLoJ, 2026-08-07). [PRÁTICA]
- **Orçamento mínimo:** a gravação de 2025 diz que o mínimo diário passou de R$5 para R$6 (TT:@gabidamadrepe/7489198895331904773, 2025-04-03). [OFICIAL segundo o criador] **pode estar superada.**
- **Recarga:** a Shopee Ads funciona com saldo pré-pago. Alessandra (Rica Exclusive) recarrega dia sim, dia não em loja nova e todo dia em loja madura (TT:@preciosatshirts/7656131679282564373). Ela também evita recarregar no fim do mês, quando a Shopee não está dando cupom. [PRÁTICA]

### Método mais repetido: entrar com ROAS baixo e subir aos poucos

Este é o consenso entre cinco criadores.

- **Produto novo começa com ROAS alvo baixo** para ganhar alcance, gerar as primeiras vendas e criar histórico. Conforme vende, sobem o ROAS e o orçamento.
  - IG:DcZakCxJCCq (Nilton Andrade, 2026-08-23): ROAS 11,7, impulsão ativa por cerca de 3 dias, orçamento de pelo menos R$15/dia e nunca ilimitado. Depois de 3 a 4 dias, desliga a impulsão e sobe o ROAS.
  - IG:DbyUb3HtXkz (Jonathas Bernardine, 2026-08-08): ROAS baixo **com preço abaixo do mercado**. Com cerca de 15 vendas, sobe ROAS e preço. Se parar de vender, volta. Com 30 vendas, sobe de novo.
  - TT:@preciosatshirts/7656131679282564373 (2026-06-27): "Meta ROAS baixinho", impulsão desativada, R$20/dia em vez dos R$69 sugeridos, sem mexer por 7 dias, que ela trata como o tempo de leitura do algoritmo. Ela diz que ROAS alto "era para antes da atualização nova".
  - IG:DeWp45oN9LS (Alex Augusto, 2026-10-11): começa com R$10 e ROAS 20. Só sobe o orçamento, de 20% a 30%, quando o orçamento do dia é consumido. Se não entrega, baixa o ROAS para 16, 14 e até 10.
  - IG:DeUhkVpxhoE (Luan Alves, 2026-10-10): sistema de 3 grupos, descrito abaixo.
- **Lógica explicada:** ROAS alto mostra para menos pessoas, mais qualificadas. ROAS baixo libera a Shopee para mostrar para muita gente (IG:DeWp45oN9LS). [PRÁTICA]
- **Divergência sobre a impulsão rápida:** Nilton liga nos primeiros 3 dias. Alessandra desliga porque "gasta rápido demais" quando o ROAS já está baixo. Leonardo Lopes considera a impulsão inútil.

### Sistema de portfólio em 3 grupos (Luan Alves, IG:DeUhkVpxhoE, 2026-10-10) [PRÁTICA]

1. **Produto novo:** lance automático e orçamento baixo. Espera 3 dias. Se vendeu, mantém até 7 dias e depois passa para Meta de ROAS com o ROAS que a campanha bateu.
2. **Produtos campeões:** meta de ROAS média e orçamento médio. Se consumiu e bateu a meta, aumenta o orçamento em 20% por semana.
3. **Produtos reserva (cauda do catálogo):** GMV Max da loja com meta alta e orçamento ilimitado. A ideia é gastar pouco e girar o catálogo inteiro.

### Escala do vencedor (Leonardo Gutemberg, "Fabricação no Marketplace") [PRÁTICA]

- **Teste:** GMV Max em grupo com os produtos a testar, ROAS alvo 30 e cerca de R$50/dia.
- **Escala:** o produto que performa vai para uma campanha só dele, com ROAS 30 e orçamento alto (cerca de R$350) ou ilimitado. Fonte: IG:DXsGMoHHIvy (2026-04-28).
- **Ajuste fino:** se a campanha entrega perto do alvo, ele sobe o ROAS para forçar margem. Se parar de gastar, desce devagar, para 22 ou 23. Para desovar estoque, baixa o ROAS e aceita margem menor. Fonte: IG:Dbv4M7fOLoJ (2026-08-07).
- **Diagnóstico quando o Ads não vende:** CTR baixo indica que a capa não chama atenção. Conversão baixa pede melhores fotos e vídeo, além de revisar avaliações. Às vezes o problema "não pode ser só o Ads" (IG:DXsGMoHHIvy).

### Orçamento estourando cedo (Juliana Magalhães, IG:DXIJPp6CWyE, 2026-04-14) [PRÁTICA]

- **Situação:** orçamento de R$75 consumido entre meia-noite e 3h, com ROAS entregue de 7 contra meta de 4,5.
- **Correção:** ela sobe a meta para 15 e também o orçamento. Avalia em 3 dias e analisa sempre os últimos 7 dias.
- **Variante para orçamento mínimo:** Gabi (2025) pausa a campanha à meia-noite e só despausa às 18h para pegar o pico de celular (TT:@gabidamadrepe/7489198895331904773). **A tática é anterior à mudança de lances e pode estar superada.**

### Visões contrárias e alertas sobre Ads

- **A conta do ROAS na margem:** custo de Ads sobre a receita = 1/ROAS. ROAS 3,9 consome cerca de 25,6% da receita e ROAS 5,9 consome cerca de 17%. Com margem de contribuição de 15%, os ROAS sugeridos pelo GMV Max dão prejuízo. Segundo Leonardo Lopes, só fabricante ou importador grande aguenta (IG:DZITqmpOnoO). [PRÁTICA]
  - Observação do analista: o criador fala "% do lucro bruto", mas a conta é sobre a receita do pedido atribuído.
- **Ads não salva anúncio fraco.** ROAS alto depende da qualidade do anúncio e do preço, não só de orçamento (IG:DZITqmpOnoO). [PRÁTICA]
- **Anúncio individual em vez de GMV Max da loja ou campanha com todos os produtos:** Alessandra recomenda um produto por campanha (TT:@preciosatshirts/7656131679282564373). Gabi nunca promove a loja, porque "geralmente dá errado" (TT:@gabidamadrepe/7489198895331904773). Já Luan usa justamente o GMV Max da loja para a cauda do catálogo. Há divergência. [PRÁTICA]
- **Desconsiderar os avisos de "ruim" do painel,** que empurram para mais orçamento (TT:@preciosatshirts). [PRÁTICA]
- **Orgânico antes, Ads depois:** Eduardo Cipolli só paga Ads depois de 4 a 5 dias seguidos de venda orgânica. Para ele, Ads antes disso queima dinheiro e o produto "encalha" quando o pago é desligado (IG:DcelP7tP_DV, 2026-08-25). Alex Augusto diz o contrário: sem Ads não sai a primeira venda (IG:DeWp45oN9LS). **Há divergência direta.** [PRÁTICA]
- **Ads como teste barato de anúncio:** com cerca de R$6/dia, se o orçamento é consumido rápido, a capa, o preço e a descrição estão bons. Se não, troca foto, preço, título ou busca avaliações (TT:@gabidamadrepe, 2025). [PRÁTICA]

---

## 2. Preço e promoção

### Tarifas citadas pelos criadores (todas com status [OFICIAL segundo o criador]; confirmar na Central)

- **Até R$79,99:** comissão de 20% mais R$4 por item. De R$80 a R$99,99, a comissão cai para 14%, com taxa fixa maior. A transcrição diz "R$16"; o valor é incerto e a taxa fixa sobe por faixa de preço. Fonte: IG:DZT46Fut8o9 (Juliana Magalhães, 2026-06-08).
- **Novas faixas desde 1º de março de 2026:** para itens acima de R$80, sem mudança até R$80. Fonte: TT:@venderonline.ai/7603174331677543701 (2026-02-05). **pode estar superada**.
- **Vendedor CPF com menos de 450 vendas em 90 dias** tem tabela própria, e há desconto ou subsídio na tarifa quando o pagamento é por Pix. Fonte: TT:@mcarvalhodanni/7611979833073011989 (2026-02-28). **pode estar superada**.
- **Taxa fixa de R$4 para R$4,50** por item abaixo de R$79,99, a partir de 2026-10-01. Fontes: IG:Ddb8HcrxW5S (Leonardo Lopes, 2026-09-18), TT:@mathias.ecomm/7686930653031763220 (2026-09-18) e, pelo título, TT:@estefania_alencar/7687372620047617288. Segundo Lopes, o resto (subsídio Pix, programa de frete grátis) não muda. Três fontes convergem.
- **"Devolução fácil":** custaria cerca de R$0,49 por pedido concluído e teria vindo ativado por padrão em muitas contas. Lopes **especula** que essa seria a motivação do aumento (IG:Ddb8HcrxW5S). Isso é opinião, não fato.
- **Leitura do extrato:** os 20% aparecem divididos em "taxa de comissão líquida" e "taxa de transação". Exemplo de Juliana: R$14,09 + R$1,57 = R$15,66. Qualquer cobrança além de comissão e taxa fixa vem de campanha da Shopee com inscrição renovada todo mês, ou de ferramenta como "Shopee Ads Fácil". Nesse caso, ela recomenda abrir chamado e pedir restituição (IG:DZT46Fut8o9, 2026-06-08). [PRÁTICA + OFICIAL segundo o criador]

### Método de precificação

- **Fórmula de markup sobre o preço de venda** (Edson Saldanha, IG:DalGPIZxqHS, 2026-07-09):
  - custo de R$30;
  - comissão de 20% mais R$4;
  - imposto de 5%;
  - embalagem de R$1;
  - publicidade de 5%;
  - margem desejada de 20%.
  
  O resultado é cerca de R$69 de preço. [PRÁTICA]
- **Embutir a verba de Ads no preço como % fixo,** em torno de 5% (IG:DalGPIZxqHS). Leonardo Lopes mostra que na prática o Ads costuma consumir bem mais, de 17% a 25% com os ROAS sugeridos (IG:DZITqmpOnoO). [PRÁTICA]
- **Preço de teste:** entrar abaixo do mercado e subir conforme junta vendas (IG:DbyUb3HtXkz). [PRÁTICA]
- **Perda de matéria-prima no custo:** exemplo de 1kg que rende 800g, ou seja, 20% de perda (IG:Dcy-WrMO8MH, Minhas Finanças Organizadas, 2026-09-02). É conteúdo de alimentos em geral, não específico da Shopee. [PRÁTICA]
- **Muitos posts de precificação são isca de planilha ou calculadora** e trazem pouco conteúdo no vídeo: IG:DeO41vORshD, IG:DalGPIZxqHS, IG:Db6W_r3pPVc, IG:DeHq7yNRgAf (R$44,90/mês), IG:DbbhY8Zo70u, IG:DZvK_m3yP9D (ChatGPT) e TT:@venderonline.ai. Veja a seção "Conteúdo x venda".

### Promoção

- Cupom de loja aparece no extrato como desconto do vendedor; no exemplo, foram R$1,60 (IG:DZT46Fut8o9). [PRÁTICA]
- As campanhas da Shopee renovam automaticamente todo mês; para sair, é preciso preencher um formulário (IG:DZT46Fut8o9). [OFICIAL segundo o criador]
- Alessandra evita investir quando "a Shopee não está dando cupom", no fim do mês (TT:@preciosatshirts). [PRÁTICA]

---

## 3. Logística e estoque

**Esta frente quase não apareceu no conteúdo coletado.** É uma lacuna da amostra.

- **Selo "Full" (fulfillment Shopee):** visto em líderes de café (Baggio), mas nenhum criador explica o programa (lideres.tsv). [OBS]
- **"Programa de frete grátis" e subsídio Pix:** Lopes cita como componentes de tarifa que não mudaram em out/2026 (IG:Ddb8HcrxW5S). [OFICIAL segundo o criador]
- **Estoque parado como risco** de começar só no orgânico (IG:DeWp45oN9LS). Baixar o ROAS como tática para "limpar estoque" (IG:Dbv4M7fOLoJ). [PRÁTICA]
- **Operação:** IG:DakptRrxzf0 (Cristian Luque) brinca com a fase em que o capricho na embalagem dá lugar ao caos da operação. Só há a legenda. [PRÁTICA, fraco]
- **"Moído no dia do envio":** o atributo aparece em títulos de café como promessa logística e de frescor (lideres.md). [OBS]

---

## 4. Ranqueamento e anúncio (orgânico, algoritmo, conteúdo do anúncio)

- **A conversão manda mais que o clique.** O algoritmo funciona "como gerente de vendas" que precisa bater meta. Anúncio com muita visita e pouca venda perde exposição. Fonte: TT:@leticiasampaio.shopee/7650330048733383957 (2026-06-12). [PRÁTICA]
- **Não compartilhar o link da loja em grupos de amigos.** Isso gera visitas sem compra, derruba a taxa de conversão e o anúncio perde exposição (mesma fonte). [PRÁTICA, hipótese não verificada]
- **Passo a passo orgânico de Eduardo Cipolli** (IG:DcelP7tP_DV, 2026-08-25) [PRÁTICA]:
  1. A foto de capa deve se destacar das concorrentes. Se todos usam fundo branco, ele usa creme, bege ou cinza-claro.
  2. O título leva a busca exata do cliente, e a descrição deve ser clara a ponto de não deixar dúvida, o que pesa mais em ticket alto.
  3. Usar o **Shopee Vídeo** com link do produto: curtidas e visualizações dão relevância de graça e ensinam à plataforma para quem entregar.
  4. Só depois de 4 a 5 dias seguidos de venda é que ele entra com Ads.
- **Shopee Vídeo como canal:** é um tema forte entre afiliados (IG:DdKATUGsoNq, IG:DdB1l0WMzzc, IG:DZQwPl6zz7I, IG:Db4LMuiKtrd com vídeos de IA). Também aparece pelo título em TT:@jestruzik/7630721658260606226. **É, em grande parte, conteúdo de afiliado, não de vendedor.** [PRÁTICA]
- **Avaliações como motor de ranking:** a primeira venda serve para ganhar avaliação e subir para a primeira página (IG:DeWp45oN9LS). [PRÁTICA]
- **CTR para a capa, conversão para fotos, vídeo e avaliação:** é o diagnóstico de Gutemberg (IG:DXsGMoHHIvy). [PRÁTICA]
- **Algoritmo de 2026:** os títulos indicam atualização (TT:@samuel.importador/7618599158752070932, voltado a importação, e TT:@faturaplay_/7602267451388136724). Não há transcrição. [PRÁTICA, sem conteúdo verificado]

---

## 5. Produto e mix

- **Começar por produto com demanda já existente** na plataforma: algo que você fabrica, conhece quem fabrica ou consegue comprar. A ideia é testar produto, oferta, imagem e preço em vez de buscar a loja perfeita (IG:DX2gvF9Mb1w, legenda, Leonardo Gutemberg, 2026-05-02). [PRÁTICA]
- **"Vende muito, mas com lucro tão baixo que não compensa":** é o alerta de Edson Saldanha sobre parte dos produtos fáceis (IG:DagI7rqJAat, legenda, 2026-07-07). [PRÁTICA]
- **Portfólio novo / campeão / reserva**, com tratamento diferente em cada grupo (IG:DeUhkVpxhoE). [PRÁTICA]
- **Kits:** o exemplo de Alessandra é um kit Tramontina (TT:@preciosatshirts). Entre os líderes de café aparecem kit de 4 origens e kit degustação 5x50g (lideres.tsv). [PRÁTICA/OBS]
- **Fabricação própria em vez de revenda,** pela margem: é o posicionamento de "Fabricação no Marketplace" (Gutemberg e Cristian Luque, IG:DakptRrxzf0) e o motivo dado por Lopes para dizer que só fabricante ou importador aguenta os ROAS do GMV Max (IG:DZITqmpOnoO). [PRÁTICA]
- **Posts de "nichos ou produtos que vendem muito"** (IG:DXaYq-cjH3P, IG:DXDFdUYgNtK com venda de lista de fornecedores, IG:DZdpftSRCB4) não têm transcrição e são, em sua maioria, voltados a revenda.

---

## 6. Reputação e atendimento

- **Selo "Vendedor Indicado":** um dos critérios é ter 90 dias de loja ativa, segundo Alessandra. A loja dela tinha 54 dias e já cumpria os demais critérios. Ela diz que o selo "ajuda demais" a vender (TT:@preciosatshirts/7656131679282564373, 2026-06-27). [OFICIAL segundo o criador / PRÁTICA]
  - Entre os líderes de café, o selo "Indicado" aparece em muitos cards de vendedores menores (lideres.md). [OBS]
- **A primeira venda serve para ganhar avaliação,** que leva à exposição (IG:DeWp45oN9LS). Avaliação ruim aparece como causa de baixa conversão (IG:DXsGMoHHIvy). [PRÁTICA]
- **Avaliações da concorrência como fonte de melhoria:** análise de avaliações com IA, junto com análise de Ads, precificação, funil e curva ABC (IG:DZnxy_6Bm7p, legenda, Larissa Iraha, 2026-06-15). [PRÁTICA]
- **Descrição clara para evitar dúvida e desistência** (IG:DcelP7tP_DV). [PRÁTICA]
- **"Devolução fácil" tem custo por pedido** (IG:Ddb8HcrxW5S). [OFICIAL segundo o criador]
- **Atendimento por chat:** nenhum post da amostra trata disso.

---

## 7. Alimentos e marca própria

- **Pouco conteúdo específico** de alimentos no social. O vídeo do produtor de café (TT:@caiohenriquecafe/7587199517229927700, 2025-12-23) não tem fala; só o título indica que ele vende café direto com link no perfil. [OBS, fraco]
- **Perda de ingredientes no custo,** de 20% no exemplo (IG:Dcy-WrMO8MH). Vale para alimento processado. [PRÁTICA]
- **Diferença entre perfis:**
  - Vale para **indústria/marca própria**: escala com ROAS 30 (Gutemberg) e ROAS alto como alavanca de margem. A conta de Lopes indica que o modelo só fecha com margem de fabricante.
  - É específico de **revenda/afiliado**: "sem estoque, sem loja" (IG:DZQwPl6zz7I), vídeos de IA (IG:Db4LMuiKtrd), lista de fornecedores (IG:DXDFdUYgNtK) e importação (TT:@samuel.importador).
- **Na busca de café,** as marcas próprias e torrefações dominam o topo. Veja "Observação dos líderes". [OBS]

---

## 8. Cases grandes

**Não há case com números auditáveis.** Os números ditos pelos criadores são autodeclarados.

- **Alessandra (Rica Exclusive):** diz ter lojas "vendendo milhões", com mais de 4 anos, em que o Ads "não tem o que mexer" (TT:@preciosatshirts, 2026-06-27). [CASE autodeclarado, sem número]
- **Gabi (Madre P):** quatro anos na Shopee e um produto (um cropped) que "estourou" com no máximo R$5/dia de Ads, em conjunto com outras táticas (TT:@gabidamadrepe, 2025-04-03). [CASE autodeclarado]
- **Juliana Magalhães:** anúncio com 11 vendas e R$580 em 3 horas com R$75 de Ads, ROAS de cerca de 7,7 (IG:DXIJPp6CWyE, 2026-04-14). [CASE]
- **Isa Mariano:** mais de R$700 em um dia no 9/9 como afiliada do Shopee Vídeo (IG:DdKATUGsoNq, legenda). [CASE autodeclarado; afiliado; associado a desafio pago]
- **Leonardo Lopes:** cita mais de 36 bilhões de pedidos por semestre na plataforma. O número é duvidoso e não tem fonte (IG:Ddb8HcrxW5S). [DADO não verificado]
- **Sinal de mercado:** Mathias percebe vendedores migrando para o TikTok Shop por causa das taxas (TT:@mathias.ecomm/7686930653031763220). Prisciane Pereira observa convergência das plataformas (IG:DeMfiTtuMxb, só legenda). [PRÁTICA/opinião]

---

## Conteúdo x venda de curso

| Criador | Posts | O que vende | Conteúdo útil no vídeo? |
|---|---|---|---|
| Leonardo Gutemberg (Fabricação no Marketplace) | DX2gvF9Mb1w, DXsGMoHHIvy, Dbv4M7fOLoJ, DeO41vORshD | treinamento (link da bio); planilha como isca ("KIT") | **Sim**: método de Ads concreto (ROAS 30, separar vencedor, CTR/conversão) |
| Leonardo Lopes (leonardo.ecomm) | DZITqmpOnoO, Ddb8HcrxW5S, DZ6EifWuGCj, DaD4lKaRcfM | aulas/consultoria de Ads | **Sim**: conta ROAS x margem; notícia da taxa. "Antes que corrijam o bug" (DaD4lKaRcfM) é isca |
| Nilton Andrade | DcZakCxJCCq | programa "Scala 30" | Parcial: setup básico, o avançado fica atrás do curso |
| Jonathas Bernardine | DbyUb3HtXkz | não fica claro | Sim, curto |
| Luan Alves | DeUhkVpxhoE | não fica claro (pede "segue") | Sim, sistema de 3 grupos |
| Alex Augusto | DeWp45oN9LS | "manual" via comentário | Sim, regras básicas |
| Juliana Magalhães (mentora) | DXIJPp6CWyE, DZT46Fut8o9 | mentoria; aula grátis às quintas | **Sim**: leitura do extrato, orçamento estourando |
| Alessandra / Rica Exclusive | TT 7656131679282564373 | não vende curso no vídeo | Sim, setup de loja nova |
| Gabi (Madre P) | TT 7489198895331904773 | nada (diz ensinar de graça) | Sim, mas é de 2025 |
| Letícia Sampaio | TT 7650330048733383957 | gestão de lojas para terceiros | Sim, princípio da conversão |
| Eduardo Cipolli | DcelP7tP_DV | não fica claro | Sim, passo a passo orgânico |
| Edson Saldanha (Mestre Shopee) | DagI7rqJAat, DalGPIZxqHS | calculadora como isca | Fórmula simples |
| Larissa Iraha (Mentora "Certificada Shopee") | DZnxy_6Bm7p | mentoria/IA | Lista de tarefas, sem método |
| Isa Mariano, Carolina Xavier, Izabela Alves | DdKATUGsoNq, DdB1l0WMzzc, DZQwPl6zz7I, Db4LMuiKtrd | desafio e aula fechada de **afiliado** ("sem estoque, sem loja") | Pouco; é promessa de renda extra |
| Calculadoras/planilhas | DeHq7yNRgAf (R$44,90/mês), DbbhY8Zo70u (cupom), DZvK_m3yP9D, Db6W_r3pPVc, TT venderonline.ai, TT mcarvalhodanni | ferramenta paga ou isca de lead | Útil só para confirmar a estrutura de tarifa |
| Léo dos Santos | DXDFdUYgNtK | lista de fornecedores | Não, é revenda |

**Padrões de promessa a descontar:**

- "sem gastar R$0,01" (Cipolli);
- "antes que a Shopee corrija esse bug" (DaD4lKaRcfM);
- "vender sem aparecer e sem falar com ninguém" (afiliados com IA);
- R$700 em um dia (afiliado).

O conteúdo técnico mais consistente vem de quem mostra a própria tela de Ads (Gutemberg, Juliana, Alessandra, Lopes).

---

## Observação dos líderes (busca "café em grãos", 2026-10-14)

A fonte de tudo nesta seção é `observacao/lideres.md` e `lideres.tsv`, com URL `https://shopee.com.br/search?keyword=café em grãos&sortBy=sales`. A observação é parcial: a Shopee exigiu login depois da 1ª página. Por isso faltam vendidos, número de fotos, avaliações e frete.

1. **Lojas oficiais de marca no topo.** Café Italle é o 1º, com selo "Oficial". Baggio tem selos "Full" e "Oficial". [OBS]
2. **Escada de tamanhos na mesma loja:**
   - Italle: 1kg a R$76,90 e 3kg a R$194,31 no Pix, o que dá R$64,77/kg;
   - Bororó: 1kg a R$79,90 e 2kg a R$151,91;
   - Patrick e Goiabeiras: 500g e 1kg;
   - também há variação 250g/500g/1kg dentro do mesmo anúncio. [OBS]
3. **Torrefadores e produtores pequenos de MG e SP** aparecem com frequência no top 40, e a UF aparece no card. Há especiais de 84 pontos acima de R$100/kg no top 20. Isso difere do topo do Mercado Livre, mais concentrado em FULL e marcas grandes. [OBS]
4. **Título com atributos separados por "|":** espécie (100% Arábica), torra, notas sensoriais, pontuação SCA, variedade, "moído no dia do envio", escassez ("último lote safra 2025") e emoji. Isso é coerente com a dica de pôr no título a busca exata do cliente (IG:DcelP7tP_DV). [OBS]
5. **Preço riscado com desconto** de -5% a -56% em quase todos os itens, e vários mostram o "preço no Pix". Isso conversa com o subsídio Pix citado nas tarifas. [OBS]
6. **Selos "Indicado", "Full" e "Oficial"** à vista, e ícone de vídeo na maioria dos cards. Isso é coerente com a ênfase dos criadores em vídeo e no selo Indicado. [OBS]
7. **Faixa de preço por kg:** de cerca de R$67/kg (Italle, Profeta) a R$114/kg (especiais). Kit degustação chega a R$311/kg. [OBS]
8. **Marca própria x revenda:** quase todos os líderes observados são marca própria ou torrefação vendendo direto. Não foi possível identificar revenda sem abrir as páginas. [OBS]

---

## Tabela de afirmações

| id | afirmação | tipo | fonte | data |
|---|---|---|---|---|
| S01 | Campanha automática de Ads só permite ajustar orçamento diário, ROAS alvo e impulsão rápida | PRÁTICA | IG:DZITqmpOnoO | 2026-06-03 |
| S02 | Com ROAS alvo alto a Shopee pode não gastar ou entregar abaixo do alvo | PRÁTICA | IG:DZITqmpOnoO; IG:Dbv4M7fOLoJ | 2026-06-03; 2026-08-07 |
| S03 | Custo de Ads sobre a receita = 1/ROAS (ROAS 3,9 ≈ 25,6%; 5,9 ≈ 17%) | PRÁTICA | IG:DZITqmpOnoO | 2026-06-03 |
| S04 | Produto novo: começar com ROAS baixo e subir ROAS e orçamento conforme vende | PRÁTICA | IG:DcZakCxJCCq; IG:DbyUb3HtXkz; TT:@preciosatshirts/7656131679282564373; IG:DeWp45oN9LS | 2026-06 a 2026-10 |
| S05 | Subir preço junto com o ROAS a cada patamar de vendas (~15, ~30) | PRÁTICA | IG:DbyUb3HtXkz | 2026-08-08 |
| S06 | Deixar a campanha 7 dias sem mexer, tempo de leitura do algoritmo | PRÁTICA | TT:@preciosatshirts/7656131679282564373 | 2026-06-27 |
| S07 | Aumentar o orçamento em 20 a 30% só quando o orçamento diário é consumido | PRÁTICA | IG:DeWp45oN9LS | 2026-10-11 |
| S08 | Portfólio: novos (automático), campeões (meta média, +20%/semana), reserva (GMV Max loja, meta alta, ilimitado) | PRÁTICA | IG:DeUhkVpxhoE | 2026-10-10 |
| S09 | Testar em GMV Max com ROAS 30 e ~R$50/dia; vencedor vai para campanha própria com orçamento alto | PRÁTICA | IG:DXsGMoHHIvy | 2026-04-28 |
| S10 | CTR baixo indica capa; conversão baixa indica fotos, vídeo e avaliações | PRÁTICA | IG:DXsGMoHHIvy | 2026-04-28 |
| S11 | Orçamento consumido de madrugada: subir a meta de ROAS (4,5 para 15) e avaliar em 3 dias | PRÁTICA | IG:DXIJPp6CWyE | 2026-04-14 |
| S12 | Um produto por campanha; evitar campanha de todos os produtos / promover loja | PRÁTICA | TT:@preciosatshirts/7656131679282564373; TT:@gabidamadrepe/7489198895331904773 | 2026-06-27; 2025-04-03 |
| S13 | Orçamento mínimo diário de Ads subiu de R$5 para R$6 (pode estar superada) | OFICIAL (segundo criador) | TT:@gabidamadrepe/7489198895331904773 | 2025-04-03 |
| S14 | Pausar Ads de 0h a 18h para concentrar orçamento no pico noturno (pode estar superada) | PRÁTICA | TT:@gabidamadrepe/7489198895331904773 | 2025-04-03 |
| S15 | Divergência: orgânico primeiro e Ads após 4-5 dias de venda vs. sem Ads não sai a 1ª venda | PRÁTICA | IG:DcelP7tP_DV vs IG:DeWp45oN9LS | 2026-08-25; 2026-10-11 |
| S16 | Comissão até R$79,99: 20% + R$4/item; faixa R$80-99,99 com 14% e taxa fixa maior | OFICIAL (segundo criador) | IG:DZT46Fut8o9 | 2026-06-08 |
| S17 | Novas faixas de comissão acima de R$80 desde 01/03/2026 (pode estar superada) | OFICIAL (segundo criador) | TT:@venderonline.ai/7603174331677543701 | 2026-02-05 |
| S18 | CPF com menos de 450 vendas em 90 dias tem tabela própria; tarifa diferente no Pix (pode estar superada) | OFICIAL (segundo criador) | TT:@mcarvalhodanni/7611979833073011989 | 2026-02-28 |
| S19 | Taxa fixa por item abaixo de R$79,99 passa de R$4 para R$4,50 a partir de 01/10/2026 | OFICIAL (segundo criador) | IG:Ddb8HcrxW5S; TT:@mathias.ecomm/7686930653031763220 | 2026-09-18 |
| S20 | "Devolução fácil" custa ~R$0,49 por pedido e veio ativada em muitas contas | OFICIAL (segundo criador), não verificado | IG:Ddb8HcrxW5S | 2026-09-18 |
| S21 | Os 20% aparecem no extrato divididos em comissão líquida e taxa de transação | PRÁTICA | IG:DZT46Fut8o9 | 2026-06-08 |
| S22 | Inscrição em campanhas Shopee renova todo mês e gera cobrança; saída por formulário | OFICIAL (segundo criador) | IG:DZT46Fut8o9 | 2026-06-08 |
| S23 | Fórmula de preço com comissão, taxa fixa, imposto, embalagem, Ads 5% e margem-alvo | PRÁTICA | IG:DalGPIZxqHS | 2026-07-09 |
| S24 | Incluir % de perda de ingrediente no custo do alimento | PRÁTICA | IG:Dcy-WrMO8MH | 2026-09-02 |
| S25 | Algoritmo prioriza conversão sobre visitas; tráfego sem compra derruba o anúncio | PRÁTICA | TT:@leticiasampaio.shopee/7650330048733383957 | 2026-06-12 |
| S26 | Capa com fundo diferente do padrão da busca; título com a busca exata do cliente | PRÁTICA | IG:DcelP7tP_DV | 2026-08-25 |
| S27 | Shopee Vídeo com link do produto gera relevância e vendas sem Ads | PRÁTICA | IG:DcelP7tP_DV | 2026-08-25 |
| S28 | Selo Vendedor Indicado exige, entre outros, 90 dias de loja ativa e ajuda a vender | OFICIAL (segundo criador) | TT:@preciosatshirts/7656131679282564373 | 2026-06-27 |
| S29 | Começar com produto que já tem demanda e testar oferta, imagem e preço | PRÁTICA | IG:DX2gvF9Mb1w (legenda) | 2026-05-02 |
| S30 | ROAS sugeridos pelo GMV Max só fecham para fabricante/importador com margem alta | PRÁTICA | IG:DZITqmpOnoO | 2026-06-03 |
| S31 | Lojas com 4+ anos "vendendo milhões" (autodeclarado, sem número) | CASE | TT:@preciosatshirts/7656131679282564373 | 2026-06-27 |
| S32 | 11 vendas e R$580 com R$75 de Ads em ~3h (ROAS ~7,7) | CASE | IG:DXIJPp6CWyE | 2026-04-14 |
| S33 | Produto que "estourou" com no máximo R$5/dia de Ads (autodeclarado) | CASE | TT:@gabidamadrepe/7489198895331904773 | 2025-04-03 |
| S34 | Vendedores migrando da Shopee para o TikTok por causa das taxas (percepção) | PRÁTICA | TT:@mathias.ecomm/7686930653031763220 | 2026-09-18 |
| S35 | Busca "café em grãos": lojas oficiais de marca (Italle, Baggio) no topo | OBS | shopee.com.br/search?keyword=café em grãos&sortBy=sales | 2026-10-14 |
| S36 | Mesmas lojas oferecem escada 500g/1kg/2kg/3kg; 3kg Italle a R$64,77/kg no Pix | OBS | idem | 2026-10-14 |
| S37 | Torrefadores pequenos de MG/SP e especiais 84 pts acima de R$100/kg no top 20 | OBS | idem | 2026-10-14 |
| S38 | Títulos com "\|" e atributos (torra, notas, SCA, moído no envio, escassez) | OBS | idem | 2026-10-14 |
| S39 | Preço riscado (-5% a -56%) e "preço no Pix" na maioria dos cards | OBS | idem | 2026-10-14 |
| S40 | Selos Indicado, Full e Oficial visíveis; ícone de vídeo na maioria dos cards | OBS | idem | 2026-10-14 |
| S41 | Faixa de ~R$67/kg a R$114/kg no top 40; degustação 5x50g a R$311/kg | OBS | idem | 2026-10-14 |
| S42 | Sem login, a Shopee bloqueia página de produto e 2ª busca (/verify/traffic/error) | OBS | observacao/lideres.md | 2026-10-14 |
