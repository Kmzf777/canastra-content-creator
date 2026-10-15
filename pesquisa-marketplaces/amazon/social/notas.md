# Amazon: o que os criadores de Instagram/TikTok ensinam (notas do analista social)

Data da análise: 2026-10-14. Escopo: Amazon Brasil, com referências da Amazon global quando a mecânica é a mesma.
Pesquisa neutra: descreve como os melhores operam a plataforma. Não traz recomendação para nenhuma empresa.

## Base usada e limites

- **Transcrições (21 vídeos)** em `social/transcricoes/`: 13 reels do Instagram (código curto, ex. `DVujNjkjDWQ`) e 8 TikToks (id numérico). A transcrição é automática (whisperx small): nomes e números podem ter erro de áudio. Onde o número importa, isso está sinalizado.
- **Metadados:** `posts.tsv` (38 reels com legenda e data) e `tiktok.txt` (20 TikToks com tema). Posts sem transcrição entram só pela legenda, marcados "(só legenda)".
- **Falha de download:** `DcZWVc8K-6F` (FBA x DBA, Anderson Muquem) não foi transcrito; vale só a legenda.
- **Observação dos líderes:** o arquivo `observacao/lideres.md` **não existe** na pasta; usei apenas `observacao/lideres.tsv` (11 linhas, coletadas em 2026-10-14).
- **Datas dos TikToks:** tiradas do próprio id do vídeo (os primeiros 32 bits são o horário de publicação). Datas do Instagram vêm do `posts.tsv`.
- **Corte de 6 meses:** regra de plataforma anterior a **2026-04-14** recebe a marca "pode estar superada".
- **Muitos posts não servem:** cerca de metade dos 38 reels é chamada de curso/mentoria ("comenta AMAZON"), conteúdo motivacional ou algo fora do tema (entregador nos EUA, extensão de cupom, venda no agro). Estes vão para a seção de venda de curso e para a lista de descartes.

## Panorama em 5 linhas

1. O tema que mais aparece é **logística (FBA x DBA)**, puxado pelo próprio canal da Amazon (@vendacomamazon) e por "embaixadores/mentores oficiais".
2. O conteúdo de **Ads** com mais método é curto e operacional: diagnóstico na ordem orçamento, termos de busca e desempenho, com uma mudança por vez (`7678395422586539282`).
3. **Buy Box** é o centro da revenda de produto de marca alheia. Marca própria e genérico são citados como "fuga" da disputa (`7403049875136417030`).
4. Em **ranqueamento**, o método mais repetido para entrar é preço abaixo do líder e Ads no mínimo, subindo o preço conforme a posição sobe (`DVujNjkjDWQ`, `Da0yCpDBUO3`). É tática de revenda/genérico e vem de vendedores de mentoria.
5. Quase nada fala de **alimentos**. A única fonte direta é a observação das páginas (lideres.tsv): no topo de café estão marcas 1P (a Amazon compra e revende) com milhares de avaliações.

---

## 1. Ads (Amazon Ads)

**O que ensinam**

- **Diagnóstico de Sponsored Products em 3 etapas, nesta ordem** (`7678395422586539282`, @ariadne.sou, 2026-08-26) [PRÁTICA]:
  1. **Orçamento.** Se o orçamento acaba no meio do dia e a campanha vende, aumente. Se acaba sem converter, aumentar não resolve.
  2. **Termos de busca.** Um termo que vende de forma consistente pode ganhar campanha manual própria. Um termo que acumula clique e gasto sem conversão deve ser revisto ou negativado.
  3. **Desempenho.** Compare CPC, taxa de conversão e ACoS. O objetivo não é o ACoS mínimo: na fase de posicionar o produto, um gasto maior é aceito se converter. Correspondência ampla ("vaga") e complementos tendem a inflar o gasto.
  - Regra de ouro dela: **uma mudança por vez**, para saber o que causou o efeito.
- **Lance inicial no mínimo, não no sugerido**, subindo aos poucos até entender o CPC do produto (`Da0yCpDBUO3`, Picchi, 2026-07-15) [PRÁTICA]. Promessa associada, sem prova: "em uma semana" na primeira página.
- **Sponsored Brands para quem tem marca registrada**, ligado à Brand Store. Segundo o criador, é o formato que "leva lá pra cima" e sobe o ticket (`DXSHDl4Dv5Q`, Tomé Marcos, 2026-04-18) [PRÁTICA, opinião]. O post tem a tag #Ad e o criador vende assessoria de Ads.
- **Ads mais ferramentas promocionais** (cupom, quadro de promoções) como um conjunto, com Ads apresentado como "fundamental para escalar" (`7668382328430939409`, @vendacomamazon, 2026-07-30) [OFICIAL, depoimento de vendedor no canal da Amazon; sem número].
- **Ads atrelado ao custo de FBA** (`7663218104134126849`, @vendacomamazon, 2026-07-16) [OFICIAL]:
  - Conta FBA ativada a partir de 01/04/2026: investir no mínimo **3,5% em Amazon Ads** mantém os benefícios logísticos.
  - Conta FBA anterior: atingir 3,5% em até 30 dias corridos, ou aumentar em 1 ponto o que já investia em abril de 2026.
  - Benefício citado: frete fixo de cerca de R$ 6 com meta batida, mais coleta e armazenagem gratuitas. O valor saiu da transcrição automática e precisa ser conferido na página oficial.
  - Leitura: a Amazon Brasil usa o subsídio logístico para empurrar gasto em Ads. Isso muda a conta de margem de quem não anuncia.
- **Ferramenta de terceiros** mostra a origem da venda por produto, orgânica ou Ads (`DeNhhwruKWg`, SellerMind, 2026-10-07) [PRÁTICA, peça de venda de software].

**Revenda x marca própria:** o método de diagnóstico e a regra de uma mudança por vez valem para os dois. Sponsored Brands e Brand Store exigem marca registrada (Brand Registry), então são exclusivos de marca própria ou indústria.

## 2. Preço e promoção

- **Preço de entrada abaixo do líder** quando você não tem avaliações nem histórico. Depois, subir o preço devagar conforme a posição melhora, até o ponto com margem (`DVujNjkjDWQ`, Picchi, 2026-03-11; `Da0yCpDBUO3`, 2026-07-15) [PRÁTICA]. A justificativa do criador é que, sem avaliação, o preço é o único atrativo.
- **Na Buy Box, preço é o fator nº 1**, seguido de logística (FBA) e avaliação do vendedor. Com os três empatados, a Buy Box pode ser alternada entre vendedores, inclusive por geolocalização (`7403049875136417030`, Capellete, 2024-08-14) [PRÁTICA; mecânica da plataforma, pode estar superada]. O algoritmo não é público: é leitura de praticante.
- **Repricer automático de Buy Box** oferecido por software (`DeNhhwruKWg`, 2026-10-07) [PRÁTICA, peça de venda]. Específico de revenda.
- **Ferramentas promocionais nativas citadas:** cupom e quadro de promoções (`7668382328430939409`, 2026-07-30) [OFICIAL, menção].
- **Fornecedor com tabela mais cara para e-commerce do que para loja física**: alegação de consultor tributário, sem dado de apoio (`DaDtQRcBBrK`, 2026-06-26) [PRÁTICA, opinião].

**Revenda x marca própria:** a briga de preço por Buy Box é de revenda de marca alheia. O preço de entrada abaixo do líder, com subida gradual, aparece para genérico e marca nova; numa marca com política de preço, pode conflitar com o canal.

## 3. Logística e estoque

**Conteúdo oficial (@vendacomamazon)**
- **DBA (Delivery by Amazon)** é a porta de entrada: todo vendedor novo começa nele. O vendedor prepara o pedido; a Amazon coleta e entrega, com rastreio de 100% dos pedidos e suporte pós-venda ligado à coleta (`7651729932934024464`, 2026-06-15) [OFICIAL].
- **FBA para MEI** foi anunciado como novidade em fev/2026 (`DUTynYdErA8`, só legenda, 2026-02-03) [OFICIAL, pode estar superada].
- **FBA mais Ads (regra dos 3,5%)**: ver a frente de Ads (`7663218104134126849`, 2026-07-16) [OFICIAL].

**Prática**
- **Prioridade é FBA.** O DBA fica para quem está em estado sem FBA, tem produto caro demais para deixar em estoque da Amazon ou personalizado, ou como segunda oferta além da FBA (`7664720778054602005`, Capellete, 2026-07-20) [PRÁTICA].
- **DBA tem tarifa de venda diferente da FBA** (`DayaotctkVR`, Capellete, 2026-07-14) [PRÁTICA; valores não informados].
- **Contraponto:** "DBA vende" (`7604881679047544071`, @oliveiraecom, 2026-02-09) [OBS do criador: vídeo de expedição cheia em DBA; sem números].
- **FBA liberado desde o 1º dia para conta PJ, inclusive MEI**, sem exigência de histórico de vendas. Conta aberta em CPF não migra para CNPJ (`DVujNjkjDWQ`, Picchi, 2026-03-11) [PRÁTICA sobre regra; pode estar superada]. O criador também cita isenção do serviço no 1º mês e coleta em boa parte de SP; não confirmado.
- **Passo a passo do envio ao FBA:** etiqueta da Amazon sobre o código de barras, caixa fechada com etiqueta master, entrega no centro de distribuição ou coleta. Devolução apta volta ao estoque; a inapta fica separada até um pedido de remoção (`DVujNjkjDWQ`) [PRÁTICA].
- **Única preparação é a etiqueta de identificação**, sem embalar pedido a pedido (`Ddo6NZMhFuZ`, Leonardo Marques, 2026-09-23) [PRÁTICA].
- **Prep center terceirizado:** o fornecedor entrega no prep center, que etiqueta e envia à Amazon. O dono opera de outra cidade e diz ter feito "mais de 10 mil vendas" no mês (`Dd7FuKeyPcv`, Gustavo Forza, 2026-09-30) [CASE autodeclarado, sem verificação]. A legenda oferece indicação de prep center por DM.
- **Marca própria de cosmético (Baddha)**: produtos com validade e código de barras, embalados em plástico, com fita sobre códigos que não podem aparecer (`7351820036966944006`, 2024-03-29) [PRÁTICA de marca própria; regra de preparação pode estar superada; transcrição ruim].
- **Teste de estoque com 3 unidades:** enviar vários produtos com 3 unidades cada, dobrar o estoque dos que giram e repetir 3 nos lentos (`DeQMMCSsL03`, Hilton Modesto, Amazon Europa, 2026-10-09) [PRÁTICA de revenda/arbitragem; mecânica FBA igual].
- **Capital:** comprar só cerca de 25% do caixa em produto e guardar o resto para recompra e capital de giro (exemplo: R$ 500 de R$ 2.000) (`DVujNjkjDWQ`) [PRÁTICA].
- **Previsão de estoque e ruptura** como função de ferramenta (`DeNhhwruKWg`) [PRÁTICA, peça de venda].

**Revenda x marca própria:** o fluxo FBA (etiqueta, envio, remoção) vale para os dois. O lote de 3 unidades e o "compro em São Paulo e mando" são de revenda. Validade e lote, que aparecem no caso de cosmético, são o ponto que mais se aproxima de produto perecível.

## 4. Ranqueamento e anúncio (listing)

- **O que dá credibilidade para ranquear é recorrência de vendas e avaliação boa**, não só um anúncio bonito (`DVujNjkjDWQ`, 2026-03-11) [PRÁTICA].
- **Nota mínima de 4,1.** Abaixo de 4 "dá problema", e uma primeira avaliação ruim mata o anúncio (`Da0yCpDBUO3`, 2026-07-15) [PRÁTICA, opinião sem dado].
- **Estrutura do anúncio:** conteúdo A+, bullet points (com emoji, na versão do criador), fotos de 1000x1000 bem enquadradas e preço (`Da0yCpDBUO3`) [PRÁTICA]. Bom anúncio é pré-requisito: "anúncio ruim não vende" (`DVujNjkjDWQ`).
- **10 ajustes de Brand Store e listing** (`DXSHDl4Dv5Q`, Tomé Marcos, 2026-04-18) [PRÁTICA]:
  1. Banner principal com benefício, não com a marca.
  2. Loja organizada por categoria.
  3. Foto 1 com fundo branco; foto 2 com o produto em uso.
  4. Vídeo assim que possível.
  5. Escolher a subcategoria mais específica (menos concorrência).
  6. Atualizar a listagem pelo menos 1 vez por mês.
  7. Sequência de imagens como pitch de venda, sem repetir informação; se for kit, mostrar o kit.
  8. Teste A/B de título e descrição.
  9. Sponsored Brands.
  10. Ler os insights da loja.
- **Buy Box e catálogo:** produto de marca com EAN não pode ser recadastrado; é preciso entrar no anúncio existente e disputar. Fugas citadas: kits, combos, marca própria e genérico. O criador cita uma regra de out/2023 que reduziria a disputa em genérico (`7403049875136417030`, 2024-08-14) [PRÁTICA sobre regra; pode estar superada].
- **Acompanhar a Buy Box:** no Seller Central, ver o % de ofertas com Buy Box e, em Relatório Comercial, o % de destaque na Buy Box no período. Abaixo de 85% de feedback positivo, o vendedor "começaria a perder" a Buy Box (teoria, não regra) (`7403049875136417030`) [PRÁTICA].
- **Solicitação automática de avaliação** via ferramenta (`DeNhhwruKWg`) [PRÁTICA, peça de venda].
- **Personalização de anúncios** (`7673183184204336402`, @leonardolulio, 2026, só tema; não transcrito).

**Revenda x marca própria:** Brand Store, A+ e Sponsored Brands pedem marca registrada. Buy Box e catálogo compartilhado são o problema central da revenda.

## 5. Produto e mix

- **Pesquisa de mercado antes de comprar:** comparar custo do fornecedor com o preço praticado na Amazon e escolher produtos com recorrência e boas avaliações. O criador diz que o comprador da Amazon é "mais rígido" com qualidade (`DVujNjkjDWQ`, 2026-03-11) [PRÁTICA].
- **Validar 1 produto, escalar e só então ir para o próximo** (`DVujNjkjDWQ`) [PRÁTICA].
- **Vários SKUs de giro em vez de uma aposta grande.** No exemplo dele: 25% de margem, R$ 15 de lucro unitário e 100 unidades/mês dão R$ 1.500 por SKU; com 5 SKUs, cerca de R$ 7.500/mês (`DdbwS4DO_MI`, Gabriel Lima, 2026-09-18) [PRÁTICA; exemplo hipotético, não case].
- **Variedade aumenta a chance de vender a toda hora; produto parado é dinheiro parado** (`DeQMMCSsL03`, 2026-10-09) [PRÁTICA].
- **"Na Amazon vende de tudo":** uma luminária de vaso sanitário de R$ 145 teria 5.980 avaliações; não verificado (`DX-a0v2pWvN`, Nathalia Galeazzi, 2026-05-05) [PRÁTICA/entretenimento; isca para curso]. A legenda afirma que o tráfego orgânico da Amazon "disparou" em 2025-26, sem fonte.
- **Patentes expiradas do USPTO como fonte de produto** (`DZAd7mgjCy6`, só legenda, 2026-05-31) [PRÁTICA de criador; promessa de R$ 2 mil/mês; fora do Brasil].
- **Marca própria de 1P da Amazon** e Amazon/ML comprando direto da indústria: citados como ameaça ao e-commerce nativo (`DaDtQRcBBrK`, 2026-06-26) [PRÁTICA, opinião sem dado].

**Revenda x marca própria:** quase todo o conteúdo de mix é de revenda (comprar de fornecedor em SP e revender). O princípio que vale para indústria é o portfólio de vários SKUs de giro, com reposição guiada pela velocidade de venda.

## 6. Reputação e atendimento

- **Avaliação do vendedor é o 3º pilar da Buy Box.** Feedback abaixo de 85% é a zona de risco segundo o praticante (`7403049875136417030`, 2024-08-14) [PRÁTICA; pode estar superada].
- **Avaliação do produto mínima de 4,1** (`Da0yCpDBUO3`) [PRÁTICA].
- **No FBA, a Amazon assume o atendimento ao cliente** (`DdrlIE6T25E`, Arthur Mundim, 2026-09-24; legenda de `DcZWVc8K-6F`, 2026-08-23) [PRÁTICA]. No **DBA**, o suporte oficial cobre o pós-venda ligado à coleta e entrega (`7651729932934024464`) [OFICIAL].
- **Devoluções no FBA** são recolhidas pela Amazon (`DVujNjkjDWQ`) [PRÁTICA].
- **Pedido automático de avaliação** como alavanca de vendas (`DeNhhwruKWg`) [PRÁTICA, peça de venda].
- **IA com aprovação humana:** a Amazon (EUA) teria integrado o Claude ao Seller Central para reposição e preço, em beta, com nada executado sem o "sim" do vendedor (`Dd9H1A5Re90`, só legenda, 2026-10-01) [PRÁTICA/notícia de criador; não confirmado; EUA].

## 7. Alimentos e marca própria

- **Nenhum criador do conjunto fala de alimentos.** O único vídeo de marca própria com envio FBA é de cosmético (`7351820036966944006`), e trata de validade e código de barras visíveis.
- **Marca própria nos criadores** aparece como forma de fugir da Buy Box e de ter acesso a Brand Store, A+ e Sponsored Brands (`7403049875136417030`; `DXSHDl4Dv5Q`).
- Os padrões de alimentos vêm da **observação direta** (seção "Observação dos líderes").

## 8. Cases grandes

- **Franboots crescendo com a Amazon** (`7678052821186514197`, @vendacomamazon, 2026-08-25): listado no `tiktok.txt`, **sem transcrição**; números não disponíveis [CASE oficial, não lido].
- **"Mais de R$ 100 milhões faturados" por alunos** e prêmio de "Melhor Mentoria da Amazon Brasil" (`DV9g9K-DkXw`, Tomé Marcos, só legenda, 2026-03-16) [CASE autodeclarado; peça de venda de mentoria; sem verificação].
- **"Mais de 10 mil vendas no mês sem ver o produto"**, usando FBA e prep center (`Dd7FuKeyPcv`, 2026-09-30) [CASE autodeclarado].
- **Do quartinho ao galpão:** operação começou em casa e foi para o 1º galpão em cerca de 1 ano e meio (`DVujNjkjDWQ`) [CASE autodeclarado, sem faturamento].
- **"55 mil vendedores independentes passaram de US$ 1 milhão"**: legenda em espanhol, Amazon global, sem fonte (`DVwoDlCEckx`, 2026-03-11) [DADO citado por criador, não verificado; isca de curso].
- Os cases do conjunto são todos autodeclarados por quem vende curso, mentoria ou software. Nenhum traz número auditável.

---

## Conteúdo x venda de curso

| Código | Criador | Vende o quê | Conteúdo útil? | Promessa (separada do conteúdo) |
|---|---|---|---|---|
| `DVujNjkjDWQ` | Matheus Picchi | comunidade e mentoria (formulário) | Sim: passo a passo de FBA, capital de giro, preço de entrada | "Bagagem" para começar; ressalva honesta de que não é dinheiro rápido |
| `Da0yCpDBUO3` | Matheus Picchi | mentoria (#mentoriaamazon) | Parcial: lance mínimo, nota 4,1, estrutura do anúncio | "Em uma semana" na 1ª página (sem prova) |
| `Dbq2m47MWc-`, `DZ5GEb-tEW0` | Matheus Picchi | aulão e mentoria | Não transcritos | "Vender em menos de 5 minutos" |
| `DXSHDl4Dv5Q` | Tomé Marcos | assessoria de Ads (#Ad) | Sim: 10 ajustes de Brand Store | — |
| `DV9g9K-DkXw` | Tomé Marcos | mentoria ROI | Não | R$ 100 mi de alunos, prêmio de mentoria |
| `DX-a0v2pWvN`, `DXt01TQDnwX` | Nathalia Galeazzi | material/método ("comenta 3", "FAST") | Mínimo: entretenimento e frase motivacional | Tráfego orgânico "disparou" |
| `DeQMMCSsL03` | Hilton Modesto | metodologia ("comente eu quero") | Sim: teste com 3 unidades | — |
| `DdbwS4DO_MI` | Gabriel Lima | embaixador/mentoria | Sim: conta de vários SKUs | — |
| `Ddo6NZMhFuZ` | Leonardo Marques | mentor oficial | Parcial: o que é FBA | Viver 100% do marketplace |
| `DdrlIE6T25E` | Arthur Mundim | captação ("comenta FBA") | Didático básico sobre FBA | — |
| `DbJgCjLq6BZ`, `DbwUNZ5zDn0`, `DVwoDlCEckx`, `DVhZFmFjgrx` | vários | captação pura ("comenta AMAZON/FBA/começar") | Não (só legenda) | Faturar alto / importação segura |
| `DeNhhwruKWg` | SellerMind | software (20 dias grátis, indicação paga) | Lista útil de funções que um gestor de conta acompanha | "Única ferramenta" |
| `Dd7FuKeyPcv` | Gustavo Forza | indicação de prep center por DM | Sim: modelo com prep center | 10 mil vendas/mês |
| `DaDtQRcBBrK` | Ricardo Campos | consultoria tributária | Opinião de mercado | Tom alarmista ("bomba") |
| `7678395422586539282` | @ariadne.sou | (não explícito) | **Sim, o melhor método de Ads do conjunto** | — |
| `7403049875136417030`, `7664720778054602005`, `DayaotctkVR` | Bruno Capellete | menciona treinamento | Sim: Buy Box, FBA x DBA | Dicas extras "dentro do treinamento" |
| `76517…`, `76632…`, `76683…`, `DUTynYdErA8` | @vendacomamazon | canal oficial (promove programas) | Sim: regras de DBA, FBA e Ads | Peça institucional |

**Descartados por estarem fora do tema ou sem conteúdo:** `Db0f_bGxHGM` e `DcyHwHeRR0o` (entregador nos EUA), `Da7vX6tuXIE` (extensão de cupom), `DYnXFBfhP2k` (vendas no agro), `DbCGWHBBK2x`, `Dd97tGNMdfP`, `Dd6GvHHvXCo`/`DeVIM_-Bnsx` (motivacional), `DU5SbrbjiBT`/`DYe2sUQRY2K` (afiliado), `DdrOsv2K1M-` (ChatGPT, só legenda), `Dbs8I22y8Os`, `Dc4RhDYBSi0` (Mercado Livre), `DZdGbHvtxYA` (sem legenda).

---

## Observação dos líderes (lideres.tsv, coletado em 2026-10-14) [OBS]

Fonte: `observacao/lideres.tsv` (11 páginas: mais vendidos, busca e páginas de produto). O `lideres.md` não existe.

1. **Os líderes de alimentos e café são 1P.** Orfeu, Coffee Mais, Baggio e Lysoform aparecem "vendido e enviado por Amazon.com.br", com loja da marca. O mais vendido de café não é 3P com FBA: é a marca vendendo para a Amazon.
2. **Escala de prova social no topo.** Orfeu Grãos 1kg (B07HDSL78H) é o #1 de Café e o 6º de toda a categoria Alimentos e Bebidas: 16.737 avaliações, nota 4,7, "mais de 10 mil compras no mês passado". Baggio: 10.981 avaliações. Coffee Mais: 2.254. Fora do café, Lysoform tem 26.687. No top 10 de Alimentos e Bebidas, os itens têm de 1.784 a 26.189 avaliações.
3. **Formatos que dominam.** Café em grãos/moído em **1kg e 250g**. Cápsulas (Nescafé/Dolce Gusto e 3 Corações TRES) ocupam cerca de 12 das 30 posições do top de Café, Chá e Bebidas, a R$ 1,55-1,79 por cápsula. Packs de 2, 4 ou 12 unidades aparecem no top de Alimentos.
4. **Patrocinado ocupa o topo da busca.** Na busca "café em grãos", 8 dos 30 resultados são patrocinados (posições 1-4 e 21-24), além de um banner de marca no topo (Giói). Os patrocinados são de marcas com **menos avaliações** (Italle, Tale, Giói, Dupan, Bem Te Vi, Govone, Odebrecht). Os orgânicos do topo são os líderes de avaliação (Orfeu com selo "Mais vendido", Coffee Mais com "Escolha da Amazon").
5. **Conquista de espaço na página do concorrente.** Banners patrocinados de marcas rivais aparecem dentro da página dos líderes: Italle na Orfeu, Orfeu na Coffee Mais. A Italle (3P marca + FBA, 1.647 avaliações, cerca de 900 compras/mês) compra a 1ª posição patrocinada e banners nos concorrentes.
6. **Conteúdo do anúncio dos líderes.** 4 a 6 fotos; vídeo em 3 dos 5 produtos observados com campo de vídeo; A+ em Orfeu, Baggio, Italle e Lysoform; 5 a 7 bullets. A Coffee Mais é exceção, no top 20 **sem A+**, com título cheio de atributos separados por "│" (100% Arábica, Torra Média, 250g).
7. **Variações num só anúncio.** A Orfeu junta sabor (Clássico, Intenso, Orgânico) e tamanho no mesmo ASIN; Coffee Mais faz o mesmo com grão/moído.
8. **Recompra por assinatura.** "Programe e Poupe" disponível em Italle e Lysoform, produtos de consumo recorrente.
9. **Preço e desconto visível.** Coffee Mais a R$ 28,43 "de R$ 54,90" (43% OFF); Orfeu com cupom de app de R$ 20 exibido; entrega grátis "amanhã" em todos os líderes observados.
10. **Faixa de preço por kg.** Café em grãos na busca vai de cerca de R$ 66 a R$ 150/kg. Orfeu fica em R$ 122-136/kg, Baggio em R$ 135,60/kg, Coffee Mais em R$ 113,72/kg e Italle em R$ 69,78/kg.
11. **Contraste com genérico importado.** Suporte de notebook WR (B086CB6BXW) tem **53 ofertas no mesmo ASIN**: a disputa de Buy Box típica de revenda que os criadores descrevem. Tem 3 bullets e não tem A+. Os líderes de alimentos de marca não mostram essa disputa (Orfeu tem 5 outras ofertas, Baggio 5).

**Cruzamento criadores x páginas**
- Os criadores falam quase só de 3P/FBA e revenda; nos alimentos, o topo é 1P. Nenhum vídeo do conjunto explica como uma marca vira fornecedora 1P (Vendor).
- "Entrar com preço abaixo e Ads no mínimo" (Picchi) aparece nas páginas na forma de marcas menores comprando o topo patrocinado e banners nos concorrentes (Italle), não necessariamente com preço baixo.
- A+, vídeo e foto de uso (Tomé Marcos) aparecem na maioria dos líderes, mas a Coffee Mais mostra que dá para chegar ao top 20 sem A+.

---

## Tabela de afirmações

| id | afirmação | tipo | fonte | data |
|---|---|---|---|---|
| A01 | Otimização de Sponsored Products segue a ordem orçamento, termos de busca e desempenho. | PRÁTICA | tiktok 7678395422586539282 | 2026-08-26 |
| A02 | Aumentar o orçamento só faz sentido se a campanha vende e o orçamento acaba no meio do dia. | PRÁTICA | tiktok 7678395422586539282 | 2026-08-26 |
| A03 | Termo que converte de forma consistente merece campanha manual; termo que só gasta deve ser revisto. | PRÁTICA | tiktok 7678395422586539282 | 2026-08-26 |
| A04 | O objetivo não é o ACoS mínimo; na fase de posicionamento aceita-se gasto maior se converter. | PRÁTICA | tiktok 7678395422586539282 | 2026-08-26 |
| A05 | Faça uma mudança por vez na campanha para isolar o efeito. | PRÁTICA | tiktok 7678395422586539282 | 2026-08-26 |
| A06 | Correspondência ampla e complementos tendem a inflar o gasto sem resultado. | PRÁTICA | tiktok 7678395422586539282 | 2026-08-26 |
| A07 | Comece o lance de Ads no mínimo e suba aos poucos até entender o CPC. | PRÁTICA | IG Da0yCpDBUO3 | 2026-07-15 |
| A08 | Conta FBA ativada a partir de 01/04/2026 mantém os benefícios logísticos investindo 3,5% em Ads. | OFICIAL | tiktok 7663218104134126849 | 2026-07-16 |
| A09 | Conta FBA anterior a abril/2026 deve chegar a 3,5% em 30 dias ou subir 1 ponto sobre o investimento de abril. | OFICIAL | tiktok 7663218104134126849 | 2026-07-16 |
| A10 | Meta de Ads batida dá frete fixo (cerca de R$ 6, valor de transcrição) e coleta e armazenagem gratuitas. | OFICIAL | tiktok 7663218104134126849 | 2026-07-16 |
| A11 | Ads, cupons e quadro de promoções funcionam em conjunto; Ads é apresentado como fundamental para escalar. | OFICIAL | tiktok 7668382328430939409 | 2026-07-30 |
| A12 | Sponsored Brands, para quem tem marca, é o formato que mais leva para cima e sobe o ticket (opinião). | PRÁTICA | IG DXSHDl4Dv5Q | 2026-04-18 |
| A13 | Na Buy Box pesam preço (1º), logística FBA (2º) e avaliação do vendedor (3º). | PRÁTICA | tiktok 7403049875136417030 (pode estar superada) | 2024-08-14 |
| A14 | Com preço, logística e avaliação empatados, a Buy Box pode ser alternada, inclusive por geolocalização. | PRÁTICA | tiktok 7403049875136417030 (pode estar superada) | 2024-08-14 |
| A15 | Abaixo de 85% de feedback positivo, o vendedor tenderia a perder a Buy Box (teoria). | PRÁTICA | tiktok 7403049875136417030 | 2024-08-14 |
| A16 | Produto de marca com EAN não pode ser recadastrado; o vendedor entra no anúncio existente e disputa a Buy Box. | PRÁTICA | tiktok 7403049875136417030 (pode estar superada) | 2024-08-14 |
| A17 | Marca própria, genérico, kits e combos são as formas citadas de fugir da Buy Box. | PRÁTICA | tiktok 7403049875136417030 | 2024-08-14 |
| A18 | Quando vende o mesmo ASIN com preço menor, a Amazon (1P) leva a Buy Box; terceiros ganham quando falta estoque à Amazon. | PRÁTICA | tiktok 7403049875136417030 | 2024-08-14 |
| A19 | Sem avaliações, o preço abaixo do líder é o atrativo de entrada; depois o preço sobe conforme a posição. | PRÁTICA | IG DVujNjkjDWQ; IG Da0yCpDBUO3 | 2026-03-11 / 2026-07-15 |
| A20 | Todo vendedor novo começa no DBA: ele prepara o pedido; a Amazon coleta, entrega e rastreia 100%. | OFICIAL | tiktok 7651729932934024464 | 2026-06-15 |
| A21 | O FBA passou a atender vendedor MEI. | OFICIAL | IG DUTynYdErA8 (legenda; pode estar superada) | 2026-02-03 |
| A22 | O FBA é liberado desde o 1º dia para conta PJ; conta aberta em CPF não migra para CNPJ. | PRÁTICA | IG DVujNjkjDWQ (pode estar superada) | 2026-03-11 |
| A23 | A prioridade é FBA; DBA só sem FBA no estado, com produto caro ou personalizado, ou como 2ª oferta. | PRÁTICA | tiktok 7664720778054602005 | 2026-07-20 |
| A24 | DBA e FBA têm tarifas de venda diferentes. | PRÁTICA | IG DayaotctkVR | 2026-07-14 |
| A25 | No FBA, a preparação é colar a etiqueta da Amazon sobre o código de barras e mandar a caixa com etiqueta master. | PRÁTICA | IG DVujNjkjDWQ; IG Ddo6NZMhFuZ | 2026-03-11 / 2026-09-23 |
| A26 | Devolução apta no FBA volta ao estoque; a inapta fica separada até um pedido de remoção. | PRÁTICA | IG DVujNjkjDWQ | 2026-03-11 |
| A27 | No FBA, a Amazon assume o atendimento ao cliente. | PRÁTICA | IG DdrlIE6T25E; IG DcZWVc8K-6F (legenda) | 2026-09-24 / 2026-08-23 |
| A28 | Prep center terceirizado recebe do fornecedor, etiqueta e envia ao FBA; criador declara 10 mil vendas/mês. | CASE | IG Dd7FuKeyPcv | 2026-09-30 |
| A29 | Marca própria de cosmético exige validade e código de barras visíveis e embalagem plástica no envio ao FBA. | PRÁTICA | tiktok 7351820036966944006 (pode estar superada) | 2024-03-29 |
| A30 | Testar produtos com 3 unidades cada no FBA, dobrar os que giram e repetir 3 nos lentos. | PRÁTICA | IG DeQMMCSsL03 | 2026-10-09 |
| A31 | Comprar só cerca de 25% do caixa em produto e reservar o resto para recompra e capital de giro. | PRÁTICA | IG DVujNjkjDWQ | 2026-03-11 |
| A32 | Vários SKUs de giro superam uma aposta única (exemplo: 5 SKUs de R$ 1.500 de lucro = R$ 7.500/mês). | PRÁTICA | IG DdbwS4DO_MI | 2026-09-18 |
| A33 | Credibilidade para ranquear vem de recorrência de vendas e avaliações, não só de anúncio bonito. | PRÁTICA | IG DVujNjkjDWQ | 2026-03-11 |
| A34 | Produto precisa de nota mínima de 4,1; primeira avaliação ruim compromete o anúncio. | PRÁTICA | IG Da0yCpDBUO3 | 2026-07-15 |
| A35 | Anúncio: A+, bullets, fotos 1000x1000 e preço competitivo. | PRÁTICA | IG Da0yCpDBUO3 | 2026-07-15 |
| A36 | Brand Store: banner de benefício, categorias, foto 2 de uso, vídeo, subcategoria específica, atualização mensal, teste A/B. | PRÁTICA | IG DXSHDl4Dv5Q | 2026-04-18 |
| A37 | O % de destaque na Buy Box é acompanhado no Relatório Comercial do Seller Central. | PRÁTICA | tiktok 7403049875136417030 | 2024-08-14 |
| A38 | Fornecedores teriam tabela mais cara para e-commerce do que para loja física (opinião sem dado). | PRÁTICA | IG DaDtQRcBBrK | 2026-06-26 |
| A39 | Alunos de uma mentoria teriam faturado mais de R$ 100 milhões (autodeclarado, peça de venda). | CASE | IG DV9g9K-DkXw (legenda) | 2026-03-16 |
| A40 | Amazon EUA integrou o Claude ao Seller Central para reposição e preço, com aprovação do vendedor (beta; não confirmado). | PRÁTICA | IG Dd9H1A5Re90 (legenda) | 2026-10-01 |
| A41 | Café Orfeu Grãos 1kg é o #1 de Café e o 6º de Alimentos e Bebidas, com 16.737 avaliações e nota 4,7. | OBS | amazon.com.br/dp/B07HDSL78H; bestsellers/grocery | 2026-10-14 |
| A42 | Os líderes de café (Orfeu, Coffee Mais, Baggio) são vendidos e enviados por Amazon.com.br (1P). | OBS | lideres.tsv (B07HDSL78H, B09MWN12GJ, B08VKMBSNT) | 2026-10-14 |
| A43 | Cápsulas ocupam cerca de 12 das 30 posições do top de Café, Chá e Bebidas. | OBS | amazon.com.br/gp/bestsellers/grocery/19778001011 | 2026-10-14 |
| A44 | Na busca "café em grãos", 8 de 30 resultados são patrocinados (posições 1-4 e 21-24), mais um banner de marca. | OBS | amazon.com.br/s?k=café+em+grãos | 2026-10-14 |
| A45 | Os patrocinados da busca de café são de marcas com menos avaliações que os líderes orgânicos. | OBS | amazon.com.br/s?k=café+em+grãos | 2026-10-14 |
| A46 | Marcas rivais compram banner patrocinado dentro da página do produto líder (Italle na Orfeu; Orfeu na Coffee Mais). | OBS | B07HDSL78H; B09MWN12GJ | 2026-10-14 |
| A47 | Coffee Mais está no top 20 de Café sem A+, com título de atributos separados por "│". | OBS | amazon.com.br/dp/B09MWN12GJ | 2026-10-14 |
| A48 | A Orfeu reúne variações de sabor e tamanho no mesmo anúncio. | OBS | amazon.com.br/dp/B07HDSL78H | 2026-10-14 |
| A49 | "Programe e Poupe" (assinatura) aparece em produtos de recompra (Italle, Lysoform). | OBS | B08TM18LQB; B07N4FX3TC | 2026-10-14 |
| A50 | Café em grãos na busca vai de cerca de R$ 66 a R$ 150/kg; a Orfeu fica em R$ 122-136/kg. | OBS | busca café em grãos; B07HDSL78H | 2026-10-14 |
| A51 | Genérico importado (suporte de notebook) tem 53 ofertas no mesmo ASIN; líderes de café de marca têm cerca de 5. | OBS | B086CB6BXW; B07HDSL78H; B08VKMBSNT | 2026-10-14 |
| A52 | Italle (3P + FBA) tem cerca de 900 compras/mês e 1.647 avaliações, bem abaixo dos líderes 1P. | OBS | amazon.com.br/dp/B08TM18LQB | 2026-10-14 |
