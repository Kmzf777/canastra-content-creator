# Amazon Brasil — estratégia para o Café Canastra (FBA e venda "normal")

> **Rodada v1, enviesada (15/10/2026):** partiu do estado da conta da Canastra (reputação vermelha, frete de R$ 34,30). A pesquisa neutra que a substitui está em [`pesquisa-marketplaces/`](../pesquisa-marketplaces/LEIA-ME.md).

> **14/10/2026.** Pesquisa no mesmo molde da de Mercado Livre: 56 vídeos do YouTube
> transcritos (16 do canal **oficial** "Venda com a Amazon Brasil", o resto de praticantes
> brasileiros, maioria de jul–out/2026), busca de café na própria Amazon (528 resultados em 8
> buscas + 10 páginas de líderes abertas), Instagram e TikTok. Notas por tema e método em
> [`pesquisa/2026-10-estrategia/`](pesquisa/2026-10-estrategia/LEIA-ME.md). Contas em
> [`scripts/precificar_amazon.py`](scripts/precificar_amazon.py).
>
> **Nada foi medido no Seller Central** — a Canastra ainda não vende na Amazon. Toda tarifa
> abaixo é *afirmada em vídeo*, com a fonte. A comissão do café é o maior número em aberto
> (afirmado 10% para Alimentos e Bebidas; uso 10% e 15% nos cenários).

---

## 0. Em seis linhas

1. **A Amazon resolve o problema que trava o Mercado Livre: o frete.** No ML o 1 kg a R$ 109,90
   paga R$ 34,30 de frete e deixa **R$ 3,32**. No FBA, com a campanha vigente, a logística acima
   de R$ 79,90 é **R$ 6 fixos** e o mesmo 1 kg deixa **R$ 25 a 31** — mesmo com 15% de comissão e
   3,5% de Ads.
2. **O mercado de café na Amazon é FBA ou 1P.** Todos os líderes abertos são vendidos pela própria
   Amazon (Campos Altos, Coffee Mais, Orfeu 250 g, Latitude 13) ou pelo dono da marca com
   entrega pela Amazon (Hunters, Giói, Italle, kits Coffee Mais). Nenhum é envio próprio.
3. **Todos têm Programe e Poupe, Loja da Marca e quase todos A+.** Café é recompra; a assinatura é
   o motor que o ML não tem.
4. **O 250 g é produto de verdade na Amazon** (Orfeu 250 g 800+/mês, Latitude 13 900+/mês): abaixo
   de R$ 79,90 a tarifa FBA é fixa (~R$ 5,85) e o 250 g a R$ 44,90 deixa ~R$ 14–16 (30–35%).
5. **Ninguém ocupa "Café Canastra"**; terceiros usam "Serra da Canastra" no título. Registrar a
   marca (protocolo do INPI basta para o Registro de Marcas da Amazon) é o primeiro passo.
6. **Ordem:** conta CNPJ + marca → 3 SKUs piloto no FBA aproveitando os 30 dias grátis → avaliações
   (Vine) → Ads automático → Programe e Poupe → kits. Black Friday (27/11) só se o primeiro envio
   sair até ~27/10; senão, Natal.

---

## 1. Como o mercado faz (Amazon, 14/10/2026)

Busca `café em grãos 1kg`, `café especial em grãos`, `café especial moído`, `cápsulas compatível
nespresso`, `café gourmet grãos kit`, `café serra da canastra`, `café moído 500g`. "Compras" é o
selo "Mais de N compras no mês passado" da própria Amazon.

| Produto | Preço | Compras/mês | Quem vende · quem entrega | PP | Loja | A+ |
|---|---:|---:|---|:-:|:-:|:-:|
| Campos Altos Especial 1 kg grãos 84+ | 125,68 | 700+ | **Amazon · Amazon (1P)** | ✓ | ✓ | ✓ |
| Hunters Clássico 1 kg grãos | 94,05 | 700+ | marca · **FBA** | ✓ | ✓ | — |
| Coffee Mais Super Crema 1 kg | 107,90 | 500+ | **Amazon (1P)** | ✓ | ✓ | ✓ |
| Kit 4 pacotes Coffee Mais variados | 170,90 | 600+ | marca · **FBA** | ✓ | ✓ | — |
| Kit 6 pacotes Coffee Mais | 246,90 | 500+ | — | | | |
| Giói Especial 1 kg (10 variações) | 123,36 | 300+ | marca · **FBA** | ✓ | ✓ | ✓ |
| Italle Gourmet 1 kg | 66,29 | 900+ | marca · **FBA** (Escolha da Amazon) | ✓ | ✓ | ✓ |
| Orfeu Catucaí 250 g grãos | 48,70 | 800+ | **Amazon (1P)** | ✓ | ✓ | — |
| Latitude 13 Clássico 250 g moído | 25,90 | 900+ | **Amazon (1P)** | ✓ | ✓ | ✓ |

Leituras:
- **Preço por kg do especial pequeno é o dobro do 1 kg**: Orfeu 250 g = R$ 195/kg. O 1 kg especial
  fica em R$ 94–126.
- **Kits variados vendem** (Coffee Mais 4 e 6 pacotes) — o equivalente ao kit Suave + Clássico.
- **1P é o caminho dos grandes**: a marca vende para a Amazon (Vendor) e a Amazon revende. É uma
  porta para depois, não para a entrada (exige convite/negociação; nenhum vídeo detalha).
- **Busca "café serra da canastra"**: Rei do Café, Santa Clara, Dupan, Giói — nenhum Café Canastra.
- Patrocinados: ~20% dos resultados de cada busca.

Dados brutos: ficaram no navegador (o download do TSV não foi feito); extrator reaproveitável em
[`scripts/extrator_busca_amazon.js`](scripts/extrator_busca_amazon.js).

---

## 2. Quanto sobra — Amazon × Mercado Livre

`python amazon/scripts/precificar_amazon.py`. Comissão 10% (afirmada para Alimentos e Bebidas,
0KERUmnBrf4), Amazon Vantagens 1,5% em itens ≥ R$ 40 (oficial, H0ab_x1YIBY), imposto 9%, CMV de
`mercadolivre/custos.md`. `fba` = campanha Experimente FBA (R$ 6 ≥ R$ 79,90 com 3,5% de Ads);
`fba_pos` = cenário de estresse depois de 31/01/2027 (R$ 15, suposto); `dba` = R$ 17,45 (único valor
legível, de 2–3 kg; pessimista para 1 kg).

| SKU · preço | FBA | FBA pós-campanha | DBA | ML hoje |
|---|---:|---:|---:|---:|
| 1 kg · 109,90 | **30,52 (27,8%)** | 25,37 | 22,92 | 3,32 (3,0%) |
| 1 kg · 119,90 | **38,12 (31,8%)** | 33,32 | 30,87 | 11,02 |
| 1 kg · 129,90 | **45,72 (35,2%)** | 41,27 | 38,82 | 18,72 |
| 250 g · 44,90 | **15,85 (35,3%)** | 15,85 | 15,20 | — |
| 500 g · 69,90 | **23,72 (33,9%)** | 23,72 | 23,07 | — |
| Kit 2 × 1 kg · 219,80 | **67,05 (30,5%)** | 65,74 | 63,29 | 21,15 |
| Kit 4 × 250 g · 159,90 | **59,52 (37,2%)** | 56,12 | 53,67 | — |

Com **comissão de 15%** (pior caso): 1 kg a R$ 119,90 = R$ 32,13 (26,8%) no FBA e R$ 27,33 no
pós-campanha; 250 g a R$ 44,90 = R$ 13,60; kit 4 × 250 g = R$ 51,53.

**A conclusão não depende das taxas em aberto**: em qualquer cenário a Amazon deixa 5 a 10 vezes o
ML por 1 kg, porque o frete do ML com reputação vermelha (R$ 34,30) não existe aqui.

Armadilha do 250 g: a R$ 39,90 ele escapa da taxa de 1,5% do Vantagens, mas deixa R$ 3,38 a menos
que a R$ 44,90. Fique em R$ 44,90–49,90 (o Orfeu está em R$ 48,70).

---

## 3. FBA × venda "normal" (DBA / envio próprio)

| | **FBA** | **DBA** (Amazon coleta/ponto de coleta) | **Envio próprio (MFN)** |
|---|---|---|---|
| Quem guarda e despacha | Amazon, do CD (MG tem FBA; CD de Betim) | Você embala; Amazon transporta | Você, com transportadora própria |
| Selo Prime | sim | não | não |
| Tarifa (afirmada) | **R$ 6** ≥ R$ 79,90 na campanha; R$ 5,65–6,50 entre R$ 30 e 79 | R$ 6,50 < R$ 79; acima, por peso (sem valor de 1 kg) | você paga o frete |
| Prazo | não é seu problema | corte 11:30, entrega ao ponto até 14:00; preparo padrão **0 dia** | corte definido por você (mín. 11 h) |
| Métrica que pune | estoque/validade | **envio tardio < 4%, cancelamento < 2,5%** (oficial) — passar disso afeta a conta e pode desativar | idem |
| Proteção | reembolso FBA | perda/dano reembolsado em 3 dias (Safe-T) | — |

**A torra sob demanda é o que deixou o ML vermelho.** No DBA/MFN o mesmo atraso vira "envio tardio"
e põe a conta nova em risco logo no começo. **No FBA o problema some** — vira planejamento de lote.

Decisão:
- **FBA para tudo que vende** (1 kg, 250 g, 500 g, kits). Lote para **3–5 semanas** de venda (a
  Amazon recomenda ~5 semanas de cobertura; café torrado não aguenta os 2–3 meses que praticantes
  pregam). Torra programada para a janela de coleta.
- **DBA só como reserva no mesmo ASIN** (FBA e DBA podem coexistir, 02Bn3HyAYqk), com **prazo de
  preparo de 1–2 dias declarado por ASIN** e capacidade diária baixa (20–30 pedidos). Nunca
  declarar "0 dia" no que não se cumpre.
- **Kit chega montado** ao CD (o CD não monta kit), com uma etiqueta FNSKU externa; caixa master
  até 22 kg e 100 cm. Etiqueta **não cobre a validade**; vencido no CD não é reembolsado e é
  descartado em 30 dias.

---

## 4. Organização dos anúncios (catálogo)

Proposta (detalhe em `notas/marca-listagem-promocoes.md`):

| Pai (ASIN pai) | Filhos (variação) | Por quê |
|---|---|---|
| Café Canastra **Clássico** | grãos 1 kg · moído 500 g · moído 250 g · (kit 2 × 1 kg) | avaliações compartilhadas entre formatos |
| Café Canastra **Suave** | idem | idem |
| **Kit degustação** Café Canastra | 2 (Suave + Clássico 1 kg) · 4 × 250 g variados | o mercado compra kit variado |
| **Cápsulas** Café Canastra | caixa 10 · kit 40 | outro comprador e outra concorrência — depois |

- **Começar com 3–4 filhos** (1 kg Clássico, 1 kg Suave, 250 g moído, kit 4 × 250 g) para não
  diluir as primeiras avaliações. A confirmar: se a categoria aceita os temas "tipo/moagem" e
  "peso" juntos; se não, um pai por formato.
- **Título até 75 caracteres** (regra de 27/07/2026, cNn3iConWSw), marca primeiro:
  *"Café Canastra Clássico Torrado em Grãos 1 kg - Sabor Intenso"* (60) ·
  *"Café Canastra Suave Torrado e Moído, 250 g"* (42).
- **EAN/GS1 por formato** (sem EAN a oferta de marca não nasce). Peso e medidas reais por filho.
- **A+ e vídeo** com origem, torra e preparo — 8 de 10 líderes têm A+.
- **"Serra da Canastra" no título**: só depois de conferir com o jurídico (indicação geográfica).

---

## 5. Marca, avaliações e recompra

1. **Registro de Marcas da Amazon com o protocolo do INPI** (não precisa da marca concedida;
   oficial, 7ILvtU6GcPo). Libera Loja da Marca (grátis), A+, Sponsored Brands/Display, Vine,
   kits virtuais e a denúncia de quem usar a marca. Sem protocolo: depositar já (INPI 1,5–2 anos).
2. **Avaliações** — produto sem avaliação não converte. **Vine** (exige marca registrada + FBA +
   < 30 avaliações): R$ 0 até 2 unidades, R$ 200 de 3 a 10, R$ 500 de 11 a 30 (afirmado por
   agência). 10 unidades de 1 kg ≈ R$ 670 com o CMV. Só com lote fresco: Vine de café velho afunda
   o anúncio.
3. **Programe e Poupe** (assinatura): todos os líderes oferecem. Os vídeos só mostram o lado do
   comprador (~15% de desconto, cartão, cancelável); regras do vendedor (quem banca, desconto
   mínimo, elegibilidade de alimento) **precisam ser lidas no Seller Central**. Conta: 1 kg a
   R$ 119,90 com 10% de desconto (R$ 107,91) ainda deixa ~R$ 23,60 no FBA com 15% de comissão.
4. **Preço de referência limpo desde o dia 1**: a Amazon usa o histórico de preço como base de
   promoção. Publicar já no preço-alvo e dar desconto só por cupom/oferta; nunca baixar o preço
   do inventário à mão (oficial K7a4jlTP9ME; Smollan VH7Q5FddoRY).

---

## 6. Amazon Ads

Regras dos vídeos oficiais (QIF69cN-mrc, thiokBBRZhA) e de praticantes:
- **Começar por Sponsored Products automática**, lance sugerido, **R$ 40/dia por campanha**,
  **14 dias sem mexer**; depois negativar (exata negativa) e levar os termos que venderam para uma
  manual. Crédito de **R$ 530** na primeira campanha (Summit, PbfiOlFMXqc). Brands e Display só
  com marca registrada.
- **Os 3,5% de Ads são condição da tarifa FBA de R$ 6** — tratar como custo do produto (já está na
  tabela da seção 2).
- **ACOS de equilíbrio** = margem antes de Ads ÷ preço: 1 kg a R$ 119,90 ≈ **35%** (comissão 10%) /
  ~30% (15%). Folga real para ranquear — no ML era 3%.
- Estrutura: C1 automática 1 kg · C2 automática 250 g/500 g · C3 manual (dia 14+) com "café em grãos
  1kg", "café especial em grãos", "café especial", "café gourmet em grãos" · C4 concorrentes
  (Orfeu, Campos Altos, Hunters) só se o ACOS ficar abaixo do equilíbrio.
- **Pré-condição**: estoque no FBA e 5 avaliações ≥ 4,4 antes de abrir a verba (GdiQixclG1k).

---

## 7. Calendário (hoje 14/10; Black Friday 27/11, Cyber Monday 30/11)

| Quando | O quê |
|---|---|
| 14–20/10 | Conta de vendedor **CNPJ** (CPF não migra; FBA exige CNPJ), plano profissional, certificado A1 e Faturador ("fabricante"), EAN dos SKUs, protocolo INPI → Registro de Marcas. Perguntar ao suporte: café exige aprovação de categoria? Validade mínima no FBA? |
| até ~27/10 | **Primeiro envio FBA** (inicia os 30 dias sem coleta, armazenagem e tarifa do Experimente FBA, válido até 31/01/2027) |
| 30/10–13/11 | Ads automáticos pequenos; Vine nos 2 pais de 1 kg |
| 20–26/11 | Ads +50–100%; cupom e oferta no kit; revisar todo dia |
| 27–30/11 | Black Friday / Cyber Monday |
| dezembro | 2º envio (kits presente); Natal como janela de avaliações |

**Plano B**: se o primeiro envio não sair até ~12/11 (limite de 15–20 dias, afirmado), pular a
Black Friday e mirar o Natal. Conta nova sem avaliação não ganha a Black de qualquer jeito.

---

## 8. O que aprender com revenda e dropshipping (e o que não)

| Eles fazem | Vale para a fábrica? |
|---|---|
| Achar produto com demanda e margem antes de comprar | **Não precisa** — o produto é seu; use os mesmos sinais (compras/mês, preço/kg) para escolher **formato e preço**, não produto |
| Disputar Buy Box em ASIN alheio, precificação automática | **Não** — marca própria tem ASIN próprio; não há Buy Box a disputar se só você vende |
| FBA com 2–3 meses de estoque | **Adaptar**: 3–5 semanas, pelo frescor |
| Margem média de revenda ~8% (CpeAKSyctRg); 26% em operação boa | Fábrica com CMV de R$ 47 no 1 kg tem **27–35%**: a vantagem estrutural é o CMV |
| Kits para subir ticket e diluir tarifa | **Sim** — kit 4 × 250 g e 2 × 1 kg são os melhores itens da tabela |
| Keepa para histórico de preço dos líderes | **Sim** — ver quando a Amazon 1P (Orfeu, Campos Altos) fica sem estoque e concentrar Ads nessas janelas |

---

## 9. O que medir no Seller Central antes de decidir

1. A conta existe? CPF ou CNPJ? (precisa ser CNPJ)
2. **Comissão de café** (grãos, moído, cápsula) — o número que mais falta.
3. Tarifa FBA real de 250 g, 500 g, 1 kg e kit 2 kg (calculadora de receita) e se o R$ 6 vale para
   eles; se o 3,5% de Ads é sobre a conta toda.
4. Café exige aprovação de categoria? Validade mínima na entrada do FBA? Rótulo?
5. Regras de Programe e Poupe para o vendedor.
6. Elegibilidade Vine, Registro de Marcas e Loja.
7. Coleta do FBA no CEP da torrefação (TEX pode levar 15–21 dias para liberar; senão, levar o
   estoque por conta própria).
8. Mensalidade do plano profissional (citado R$ 19, com isenção promocional a confirmar).

---

## 10. Fontes e limites

- Notas por tema: `pesquisa/2026-10-estrategia/notas/` — `fba.md`, `dba-envio-proprio.md`,
  `custos-precificacao.md`, `ads.md`, `marca-listagem-promocoes.md`, `estrategia-cases.md`,
  `comecar-escalar-alimentos.md`. Cada número tem o id do vídeo.
- **Fontes fracas**: Instagram e TikTok de Amazon Brasil são rasos (pitch de mentoria); o TikTok
  bloqueou a listagem de perfis. Os 2 cases de alimentos (Empire Flippers, EUA) não falam de
  recompra nem validade.
- Nenhum vídeo dá a comissão do café, a tabela FBA por peso sem campanha, nem as regras de
  Programe e Poupe para o vendedor — todos listados na seção 9.
