# Shopee — estratégia para o Café Canastra (pesquisa de outubro/2026)

> **14/10/2026.** Pesquisa feita com o mesmo método da do Mercado Livre: 58 vídeos do YouTube
> dos últimos 90 dias (21 deles do canal **oficial Shopee Brasil**), reels do Instagram e busca
> no TikTok, destilados em 5 notas por tema e cruzados com o **CMV real** da Canastra
> (`mercadolivre/custos.md`). Fontes e método: [`pesquisa/2026-10-estrategia/`](pesquisa/2026-10-estrategia/).
>
> **Nada aqui foi medido numa conta da Shopee.** Não há loja logada no Chrome e a busca pública
> da Shopee exige login. Toda taxa é **afirmada em vídeo**; o que muda a decisão está em
> §8 "O que medir primeiro". Calculadora: `python shopee/scripts/precificar_shopee.py`.

---

## 0. Resumo em oito linhas

1. **Na tabela de comissão afirmada, a Shopee deixa muito mais que o ML no 1 kg e no kit**, porque
   o vendedor não paga o frete grátis (só o ML cobra R$ 34,30 da conta vermelha). 1 kg a
   R$ 109,90: **R$ 17,62 (16%) na Shopee contra R$ 3,32 (3%) no ML.**
2. **Essa vantagem inteira depende de uma premissa não medida:** quem paga o frete e o
   "programa de frete grátis extra". Se o vendedor pagar R$ 20 por pedido, o 1 kg a R$ 109,90
   vira prejuízo. **É a primeira coisa a medir num pedido real.**
3. **Itens baratos são piores na Shopee:** abaixo de R$ 80 a comissão é 20% + R$ 4,50. A caixa
   de 10 cápsulas a R$ 34,90 deixa R$ 5,18; o 250 g, R$ 6,28. Na Shopee, cápsula é **kit de 40**.
4. **Preço tem degraus:** entre R$ 100,00 e R$ 105,19 o 1 kg rende **menos** que a R$ 99,99; o
   mesmo entre R$ 80 e 88,69 e entre R$ 200 e 207,78. Preço-tampa: R$ 99,90 / R$ 109,90+.
5. **O kit 2 × 1 kg é o produto da Shopee:** R$ 219,80 deixa R$ 49,25 (22%) — se a taxa fixa for
   cobrada uma vez por kit (medir).
6. **Full: não agora.** Exige 5 pedidos/dia, 4,5★, NF de remessa/retorno; o Full+ devolve só
   1–2 p.p. de comissão; café perecível não é tratado em nenhum vídeo.
7. **A Shopee é plataforma de conteúdo e cupom:** live semanal, Shopee Vídeo, cupom de seguidor
   e afiliados. É onde uma torrefação tem vantagem natural (aroma, moagem, preparo).
8. **Ads só depois de vender no orgânico** e com a margem medida; ROAS de equilíbrio do 1 kg a
   R$ 109,90 é **6,2×** sem frete do vendedor, e meta inicial de ROAS 8–10.

---

## 1. A conta — o que cada venda deixa

**Comissão a partir de 01/10/2026** (afirmada em 6 vídeos: `hEkVpRw_vNg`, `9VOoazXt_aE`,
`IYi2eifHqSY`, `M37L89O1dng`, `jZeOeA6yA20`, `7Q1J56HVVbw`; a única mudança de outubro foi a
taxa fixa da faixa mais barata, de R$ 4,00 para R$ 4,50):

| Preço do item | Comissão | Taxa fixa por item |
|---|---:|---:|
| até R$ 79,99 | 20% | R$ 4,50 |
| R$ 80 a 99,99 | 14% | R$ 16 |
| R$ 100 a 199,99 | 14% | R$ 20 |
| R$ 200 ou mais | 14% | R$ 26 |

- **Pix:** o comprador paga 5% menos a partir de R$ 80 (até 8% acima de R$ 500); **a Shopee
  absorve**, o repasse não muda (`hEkVpRw_vNg`).
- **Frete:** os vídeos dizem que o frete grátis com cupom é pago pela Shopee (`9GlE-nTGOXo`);
  nenhum afirma cobrança ao vendedor, e nenhum a exclui. Há um "programa de frete grátis extra"
  com valores R$ 20/30/40 sem explicação de quem paga (`9VOoazXt_aE`).
- Nenhum vídeo cita **teto** de comissão.

Fórmula: `lucro = preço − comissão − taxa fixa − frete do vendedor − 9% × preço − CMV`.

| SKU | Preço | **Lucro Shopee** | Margem | Lucro no ML (frete medido) |
|---|---:|---:|---:|---:|
| 1 kg | 99,90 | **13,92** | 13,9% | −4,38 |
| 1 kg | 109,90 | **17,62** | 16,0% | 3,32 |
| 1 kg | 119,90 | **25,32** | 21,1% | 11,02 |
| 1 kg | 129,90 | **33,02** | 25,4% | 18,72 |
| Kit 2 × 1 kg | 199,90 | 39,92 | 20,0% | 5,82 |
| Kit 2 × 1 kg | 219,80 | **49,25** | 22,4% | 21,15 |
| Kit 2 × 1 kg | 239,80 | 64,65 | 27,0% | 36,55 |
| Moído 500 g | 54,90 | 8,48 | 15,4% | — |
| Moído 250 g | 34,90 | 6,28 | 18,0% | — |
| Cápsulas, caixa de 10 | 34,90 | 5,18 | 14,8% | — |
| Cápsulas, kit de 40 | 139,90 | **27,32** | 19,5% | — |

**Pisos** (frete do vendedor zero): 1 kg — zero R$ 72,54 · 15% R$ 108,06 · 20% R$ 117,54 ·
kit 2 kg — 15% R$ 183,87 · cápsula 10 — 15% R$ 35,00 · kit 40 cápsulas — 15% R$ 129,68.

**Estresse do frete** (1 kg a R$ 109,90, hipótese de frete pago pelo vendedor):

| Frete do vendedor | Lucro | ROAS de equilíbrio |
|---:|---:|---:|
| R$ 0 | 17,62 (16,0%) | 6,2 |
| R$ 10 | 7,62 (6,9%) | 14,4 |
| R$ 15 | 2,62 (2,4%) | 41,9 |
| R$ 20 | −2,38 | — |

**Leitura.** A Shopee vence o ML no 1 kg enquanto o frete que sobra para o vendedor for menor
que **R$ 14,30** por pedido. Abaixo de R$ 80 ela é mais cara que o ML (20% contra 14%), então
ali só vende kit.

### Os degraus de preço (zonas mortas)

A taxa fixa sobe em degraus; logo acima de cada um, cobrar mais deixa menos:

| Faixa | Rende menos que | Regra prática |
|---|---|---|
| R$ 80,00 a 88,69 | R$ 79,99 | item barato: R$ 79,90 ou ≥ R$ 89,90 |
| **R$ 100,00 a 105,19** | R$ 99,99 | 1 kg: **R$ 99,90** ou **≥ R$ 109,90**; nunca R$ 100–105 |
| R$ 200,00 a 207,78 | R$ 199,99 | kit: R$ 199,90 ou **≥ R$ 209,90** |

---

## 2. Qual o papel da Shopee para a Canastra

| | Mercado Livre | Shopee |
|---|---|---|
| Custo do 1 kg a R$ 109,90 | R$ 3,32 de lucro (frete R$ 34,30 da conta vermelha) | R$ 17,62 (se o frete não for do vendedor) |
| Itens < R$ 80 | 14% (+ custos de envio próprios) | 20% + R$ 4,50 — caro |
| Motor de tráfego | busca, catálogo, Ads | busca + **conteúdo** (live, vídeo, afiliados) + cupom |
| O que exige | reputação, Full, frete | despacho no prazo (inclusive sábado), conteúdo frequente |
| Comprador | busca por especificação | sensível a preço, cupom e frete grátis (`2SbqWeP3ex8`, `RT2GgkCEOYc`) |

**A tese "na Shopee só fabricante lucra"** (`2SbqWeP3ex8`, `jZeOeA6yA20`) vale **pelo custo**,
não pelo preço: quem fabrica aguenta o desconto que o revendedor não aguenta. A prova mais forte
dos vídeos é a fábrica de private label com **5–6 mil pedidos/dia** (`QoF266Zzi20`): poucos SKUs
de reposição, frete grátis como gatilho, ticket de ~R$ 28, e um gargalo de capacidade de
produção. A Canastra tem duas das três condições (produto de reposição, poucos SKUs); a terceira
(teto de torra e expedição em pico) precisa ser perguntada à produção.

**Nenhum vídeo mostra café ou alimento na Shopee.** O ticket típico dos cases é de R$ 28 a R$ 50.
Logo, o papel da Shopee é uma **hipótese a testar**: canal de **kit e recompra**, onde a margem
por pedido é melhor que no ML, com conteúdo próprio para compensar o ticket acima da média.

---

## 3. Organização dos anúncios

Na Shopee, **variação é forte**: cada combinação tem preço, estoque, SKU, EAN e foto próprios, e
as vendas se somam num anúncio só (`rcGxXjm76xE`, `1Sbvlp1lYD8`, oficiais). Anúncio novo só quando
muda função, proposta ou categoria. Limite oficial: a variação mais cara até **4×** a mais barata
(`MfH07p4ZtT4`), acima disso o anúncio arrisca ser tratado como spam.

| Anúncio | Variações | Por quê |
|---|---|---|
| **A — Café em Grãos Canastra 1 kg** | Suave · Clássico | ticket ≥ R$ 109,90; histórico somado |
| **B — Kit 2 × 1 kg** | Suave+Suave · Clássico+Clássico · Suave+Clássico | kit é anúncio próprio; maior lucro por pedido |
| **C — Café Moído** | torra × 500 g / 250 g, ou kit 2 × 500 g | separado do grão: outra busca (moedor × coador) |
| **D — Cápsulas compatíveis Nespresso** | **kit de 40** (caixa de 10 só como entrada, se couber nos 4×) | caixa avulsa deixa R$ 5 |

Grão de 1 kg e moído de 250 g **no mesmo anúncio** quebrariam a regra dos 4× e fariam a vitrine
mostrar "a partir de R$ 34" para quem busca 1 kg.

**O anúncio** (série oficial "Ajuda Aí Shopee"):
- **Título:** produto, marca, especificação, com o essencial nos **primeiros 36 caracteres**
  (`zSfe4Z0Ukbc`). Ex.: `Café em Grãos Canastra 1kg Suave Torrefação Própria`.
- **Capa:** 1:1, ≥ 1.000 px, pacote ocupando ~70%, fundo neutro (`fmcvIUvhE3Q`).
- **Galeria:** pacote → variações lado a lado → grão de perto → xícara pronta → perfil sensorial
  → etiqueta de torra/validade → "Desde 1985" e a torrefação (`sASFbQPoByM`).
- **Vídeo no anúncio:** MP4, 10–60 s, até 30 MB (`BjlJ3AnBHRM`): torra, moagem, xícara.
- **Atributos completos e EAN real** (`S03qUnOmvek`); categoria mais específica (`BuWT9gBqjtU`).
- **Anvisa:** desde 21/09/2026 cadastros novos em 169 categorias exigem o campo Anvisa
  (`RvJiFGQiK3c`). Confirmar se café está na lista e qual documento a fábrica tem.

---

## 4. Frete grátis

Na Shopee o frete grátis é **benefício da plataforma** ligado a cupom e à saúde da loja: com 6
pontos de penalidade a loja **perde o frete grátis** (`ThPsYQpMxJE`). Não é escolha do vendedor
como no ML. O que está na mão da Canastra:
- **Não perder o benefício:** despachar no prazo. 8% de não envio ou 5% de atraso geram ponto;
  3 pontos tiram selo e campanhas (`ThPsYQpMxJE`).
- **Entender o "frete grátis extra"** antes de aderir (§8): se for custo do vendedor, entra no
  numerador e pode zerar a vantagem sobre o ML.

---

## 5. Full × envio próprio

**Envio próprio agora; Full depois, e só para o SKU de maior giro.**

| Critério | Full Shopee (oficiais `TUs6QYGqGrw`, `CDXeiFn8Ykw`, `0oRYednAlHY`) | Canastra hoje |
|---|---|---|
| Elegibilidade | CNPJ, loja ≥ 4,5★, **≥ 5 pedidos/dia** | loja não medida |
| Fiscal | certificado digital, série de NF exclusiva, NF de remessa e retorno | passar ao contador |
| Ganho | Full+: 40–70% dos pedidos no Full = −1 p.p. de comissão (R$ 1,10 no 1 kg); ≥ 70% = −2 p.p. | pequeno |
| Envio ao galpão | itens ≥ R$ 20 sem taxa de envio (`ty0iwe3dV1I`) | café passa |
| Perecível | **nenhum vídeo trata** | torra fresca é o argumento de venda |

A conta do Full+: −2 p.p. no 1 kg são R$ 2,20; **uma perda (validade, devolução) a cada ~21
unidades apaga o ganho.** Não enviar estoque antes de ter histórico de algumas semanas
(`3dFbYxsShkA`).

**Despacho próprio:** prazo de postagem compatível com o ciclo de torra, **nunca vender estoque
que não existe** (cancelamento por falta de estoque é penalidade grave, `MpCWZv2RyjA`), e
**envio no sábado** em ≥ 20% dos pedidos para buscar o selo de **vendedor indicado**
(`h5-bSl5jCOM`; `DIDtaQXMCXU` lembra que o selo é consequência, não meta).

---

## 6. Conteúdo, cupom e afiliados — o motor da Shopee

**Live** (oficiais `jHqyToCEwyA`, `yoj_8MgXWjI`, `4TxYhqtpvjw`):
- 1 por semana, 1 h a 1 h 30, 10–15 produtos; lembrete 7 dias antes nas campanhas.
- Preço de live tem de ser **o menor dos últimos 30 dias**, promoção verdadeira.
- Moedas: 100 moedas = R$ 1 (`7i2f1rplBl0`); 20 mil moedas/h (~700 espectadores) = R$ 200/h,
  ou ~4 pedidos de 1 kg por hora só para pagar a moeda. **Começar sem moeda ou com pouca.**
- Formato da Canastra: "mesa de preparo" — moer, coar, prensa, cápsula ao vivo, tema por semana
  ("café da semana", "presente de Natal", "grão × cápsula"). Sem QR code, sem link externo,
  sem citar outros canais (`aUqdtKFx5gM`).

**Shopee Vídeo:** clipes curtos reaproveitando a live (moagem, crema, aroma). Vídeo e afiliado
demoram a dar exposição (`JnuEW1aKquk`): começar já para colher no fim do ano.

**Cupons:**
- Cupom de **seguidor de 2%** já basta para estimular o seguir (`7i2f1rplBl0`); vale para a loja
  inteira, então precisa caber no SKU de menor margem (cápsula).
- **Recompra:** cupom exclusivo por chat por volta do 21º–25º dia após a compra do 1 kg
  (hipótese a testar).
- **Cupom com mínimo** perto do kit (3% acima de R$ 190) puxa quem compraria 1 kg para o kit.

**Afiliados do vendedor:** o afiliado escolhe por preço × comissão (`A2_b1aHi8xk`); faixa
comum de 4% a 12% (`0yVxN6kutVg`, não verificada). Com a margem da §1: **8% no 1 kg** (R$ 8,79)
e **12% no kit** (R$ 26,38) deixam o kit mais atraente ao afiliado e ainda com lucro. A
ferramenta não existe para loja com menos de 90 dias (`RT2GgkCEOYc`).

---

## 7. Shopee Ads

- **Antes de anunciar:** conversão de 30 dias ≥ 1,5% (`bq2NKPmkty8`), estoque ≥ 10, loja
  decorada (logo, banner, categorias), algumas vendas orgânicas (`gR0M6J11gJs`).
- **Desligar** "Ads Fácil 2.0 / GMV +10%" e a recarga automática: ele separa 10% de cada venda
  como crédito de Ads, o canal `t8PUjZr8joA` teve prejuízo por mais de um mês com isso. Recarga
  manual, de valor pequeno.
- **Equilíbrio:** ROAS = preço ÷ lucro antes de Ads. 1 kg a R$ 109,90: **6,2×**; a R$ 129,90:
  **3,9×**; kit a R$ 219,80: **4,5×** (sem frete do vendedor). ROAS alto não é lucro
  (`wcZmjCYnHIo`): a régua é o lucro depois de Ads.
- **Primeira campanha:** anúncio individual do 1 kg, R$ 10–20/dia, 7 dias sem mexer, meta de
  ROAS **8–10** (piso 7). GMV Max de loja só com 3+ SKUs com histórico (`WjE-oGa1iUM`).
- **Depois, três grupos** (reel `DeUhkVpxhoE`): produto novo com lance automático e orçamento
  baixo por 3–7 dias, depois meta = o ROAS que bateu; campeões com meta média e +20% de
  orçamento por semana enquanto bate a meta; reservas em GMV Max de loja com meta alta.
- **Orgânico primeiro** (reel `DcelP7tP_DV`): Shopee Vídeo com link do produto e capa que se
  destaca; Ads só depois de 4–5 dias seguidos vendendo.
- Os ROAS de 15–60 dos vídeos são de revenda com margem de 10–15%; **não copiar a meta,
  copiar o método.**
- **Google Ads dentro da Shopee** (oficial `hNfKhZpquFs`): leva o catálogo ao Google; só depois
  de o Shop Ads provar lucro.

---

## 8. O que medir primeiro (antes de qualquer decisão)

Em ordem; as três primeiras decidem se a Shopee vale mais que o ML:

1. **Extrato de um pedido real de 1 kg e de um kit:** comissão, taxa fixa e qualquer linha de
   **frete ao vendedor**. Se o frete do vendedor passar de **R$ 14,30**, a Shopee perde do ML no 1 kg.
2. **"Programa de frete grátis extra":** adesão, custo, se R$ 20/30/40 é cobrança ou subsídio.
3. **Kit conta como 1 item ou como N unidades na taxa fixa.** Se for N, o kit a R$ 219,80 cai de
   R$ 49,25 para R$ 23,25.
4. Se a **loja existe**, é CNPJ, nota e pedidos/dia; se o café exige **Anvisa** no cadastro.
5. **Preço dos concorrentes de café na Shopee** (precisa de login no Chrome com uma conta de
   comprador; a busca pública é bloqueada).
6. Se a **comissão é sobre o preço de lista ou o pago** (com cupom do vendedor) e se o desconto
   muda a faixa.
7. Coleta no CEP da fábrica, prazo de postagem e se o Full aceita café.
8. Capacidade de torra e expedição em pico (11.11, Natal).

---

## 9. Plano

| Fase | Quando | O quê | Portão para a próxima |
|---|---|---|---|
| **0 — medir** | outubro | itens 1–5 da §8; abrir/ajustar a loja; cadastrar A, B e D com o padrão da §3 | frete do vendedor < R$ 14,30 e kit = 1 item |
| **1 — orgânico e conteúdo** | 20/10 a 11/11 | 1 live por semana (terças: 20/10, 27/10, 03/11) como ensaio; clipes no Shopee Vídeo; cupom de seguidor 2%; despacho no prazo e sábado | 10+ vendas, conversão ≥ 1,5%, zero ponto |
| **2 — primeira data e Ads** | 11.11 (quarta) | lembrete até 04/11; kit e 1 kg na campanha se a conta fechar; primeira campanha de Ads do 1 kg (meta 8–10) | lucro depois de Ads positivo em 7 dias |
| **3 — fim de ano** | 27/11 a 24/12 | Black Friday; 12.12 (sábado) como live de presente; recompra por chat; afiliados no kit (loja ≥ 90 dias) | — |
| **4 — escala** | 2027 | Full para o SKU de maior giro (se aceitar perecível), GMV Max, Google Ads | — |

**Preços de partida propostos** (decisão do Rafael; nada aplicado):
1 kg **R$ 109,90** (Pix ≈ R$ 104,41, sem custo para a loja); kit 2 × 1 kg **R$ 219,80**; kit de 40
cápsulas **R$ 139,90**. Evitar R$ 100–105, R$ 80–88 e R$ 200–207.

---

## 10. O que aprender com revenda, dropshipping e afiliado

| Eles fazem | Por quê | Para a fábrica |
|---|---|---|
| Garimpar produto "explodindo" e trocar de mix | não controlam produto | não se aplica; o mix é a linha da torrefação |
| Preço mínimo para ranquear, depois subir 1–5% a cada 3–5 dias (`MpCWZv2RyjA`) | margem de compra | começar perto da mediana, nunca abaixo do piso de 15% |
| Kit para subir ticket e diluir taxa fixa (`2SbqWeP3ex8`) | taxa por item | **sim**: kit 2 × 1 kg e kit de 40 cápsulas |
| Impulsionar grátis a cada 4 h (`MpCWZv2RyjA`) | custo zero | sim, nos 5 anúncios principais |
| Vídeo de IA sem aparecer | escala barata | a Canastra tem a coisa real: torra, moagem e preparo |
| ROAS 28 com ticket de R$ 50 (`hNxA9Ujto7c`) | anúncio já ranqueado | meta de longo prazo; no início, 8–10 |

O que o fabricante tem e o revendedor não: **custo** (CMV de R$ 47 contra atacado), **frescor**
(data de torra), **conteúdo de origem** e **capacidade de fazer kit e lote exclusivo**. Na
Shopee isso vira live, vídeo, kit e cupom de recompra, não preço baixo.

---

## Fontes

- Notas por tema: [`pesquisa/2026-10-estrategia/notas/`](pesquisa/2026-10-estrategia/notas/) —
  `taxas-regras-preco.md`, `ads.md`, `full-anuncio.md`, `cases-fabrica.md`, `live-video-cupons.md`.
- Transcrições: `pesquisa/2026-10-estrategia/transcricoes/<id>.txt` (link do vídeo no cabeçalho).
- Lista e consultas: `videos-1.tsv`, `videos-2.tsv`, `selecionados.txt`.
- Instagram: `pesquisa/2026-10-estrategia/instagram/`.
