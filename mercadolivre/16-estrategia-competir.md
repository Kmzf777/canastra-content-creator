# Estratégia para competir no Mercado Livre como fábrica

> **14/10/2026.** Pesquisa de 63 vídeos do YouTube (últimos 90 dias, mais o canal do Hugo
> Vasconcelos sem corte de data), reels e TikToks do @hugovasc_ e da busca do Instagram, as
> lives oficiais do canal "Vendedores Mercado Livre", a busca de café de 08/10/2026 (588
> anúncios) e as contas com o CMV real (`custos.md`, `scripts/cenarios_estrategia.py`).
> Material bruto e notas por tema: [`pesquisa/2026-10-estrategia/`](pesquisa/2026-10-estrategia/LEIA-ME.md).
>
> **Nada aqui foi aplicado na conta.** Cada campo precisa da autorização do Rafael.
> Número de vídeo é *afirmado pelo criador* até ser medido na conta; o id do vídeo vai junto.

---

## 0. As decisões em uma página

1. **O gargalo não é anúncio nem Ads: é o frete da reputação vermelha.** O frete grátis do
   1 kg (R$ 34,30) é **31% do preço** de R$ 109,90; o CMV é 43% e tarifa + imposto 23%.
   Sobram **R$ 3,32 (3%)**. Nenhuma tática dos vídeos (Ads, promoção, afiliado, cupom) cabe
   em 3%. **Sair do vermelho vem antes de tudo.**
2. **Preço do 1 kg avulso em R$ 129,90** (já proposto no `15-preco`): margem de
   contribuição (MC) de R$ 18,72 (14,4%), mediana do mercado especial.
3. **Competir no preço por kg pelo kit, não pelo avulso.** Kit 2 × 1 kg a **R$ 239,80 =
   R$ 119,90/kg com MC de 15,2%**, porque o frete do kit (R$ 54,10) é menor que dois fretes
   de 1 kg (R$ 68,60). É a escada que os líderes não oferecem (o kit deles não dá desconto
   por kg).
4. **Clássico abaixo de R$ 150, um anúncio por SKU, kit como anúncio próprio** (não
   variação). Cerca de 11 anúncios no total.
5. **Sem Full por enquanto; testar Full Super depois do amarelo.** O Full não muda frete nem
   tarifa; o custo de entrada por unidade come a margem com lote pequeno. Mas **um terço dos
   anúncios de café 1 kg da busca tem selo Full Super**, que tem outra tabela de frete: é a
   hipótese mais valiosa para medir.
6. **Ads só com MC ≥ 15% e reputação amarela** (a live oficial diz que o Mercado Ads exige
   amarela ou melhor). Verba = metade da MC; uma campanha, 1 kg e kit, 7 dias sem mexer.
7. **A vantagem de fábrica é real e grande:** um revendedor que compre café equivalente a
   R$ 60/kg perde R$ 9,68 por venda a R$ 109,90. A fábrica pode ficar abaixo de qualquer
   revendedor — o que falta é sair do frete vermelho para essa vantagem virar margem.

---

## 1. Diagnóstico: por que hoje não dá para competir

| 1 kg Clássico, frete grátis vermelho | R$ | % do preço |
|---|---:|---:|
| Preço | 109,90 | 100% |
| CMV | 47,00 | 43% |
| Frete grátis (medido, vermelha) | 34,30 | 31% |
| Tarifa 14% + imposto 9% | 25,28 | 23% |
| **Margem de contribuição** | **3,32** | **3%** |

Consequências (cenários do `scripts/cenarios_estrategia.py`, seção 1):

| Preço | MC | MC % | ROAS de equilíbrio |
|---:|---:|---:|---:|
| 109,90 | 3,32 | 3,0% | 33 |
| 119,90 | 11,02 | 9,2% | 10,9 |
| **129,90** | **18,72** | **14,4%** | **6,9** |
| 139,90 | 26,42 | 18,9% | 5,3 |

- **ROAS de 33** está fora de qualquer faixa praticada nos vídeos (15–20 é o "padrão" de
  Hunter, Natan e Sidinei; Bruno Maciel só passa de 30 em campanha madura).
- **O frete vale mais que qualquer desconto de tarifa.** Cada R$ 1 de frete economizado é
  R$ 1 de MC; cada R$ 1 de desconto no preço custa só R$ 0,77 (tarifa e imposto caem junto).
  Com a reputação verde o ML dá desconto de frete (*"até 70% em itens até R$ 79"*, Marcela
  Nanni `4t5uJ0V9u9c`; valor para 1 kg **não medido**). Se o frete cair 30%, o equilíbrio
  do 1 kg desce de R$ 105,58 para R$ 92,22; se cair 50%, para R$ 83,31.
- **A reputação também tranca a vitrine.** A Central de Promoções mostrou *"não é possível
  oferecer promoções. Recupere sua reputação verde ou amarela"* (lição 12 do `LEIA-ME.md`,
  lido na conta). A live oficial de Ads (`LOZL-QmsGL4`, 30/09) afirma amarela ou melhor,
  10 vendas e nenhum débito para anunciar.

---

## 2. Como o mercado faz

### 2.1 Os líderes de café 1 kg (busca de 08/10/2026, `14-estrategia-1kg.md` §3)

| Padrão | Quem | O que serve para nós |
|---|---|---|
| Preço de quem vende volume não é o mais baixo | Orfeu R$ 174,90 (+50 mil), Prima Qualità R$ 129 (+5 mil), Tamanduá R$ 118 (+1 mil) | Marca e torra vendem acima da mediana |
| Kit é anúncio próprio, sem desconto por kg | Appassionato 1 kg R$ 120 → kit 2 R$ 116,61/kg; Patrick R$ 103 → R$ 110/kg | **Brecha:** um kit que desce de verdade por kg se destaca |
| Catálogo (`/p/`) para a marca | Orfeu, Prima Qualità, Giói, Unique em página de catálogo | Catálogo próprio exige marca registrada (§3.4) |
| Data da torra / "Torra fresca" no título | Moquinha 5,0★, Tiger | Diferencial de quem torra sob demanda |
| Prazo de disponibilidade declarado | Patrick: *"inclui os 2 dias para deixar o produto pronto"* | **Remédio para o atraso de despacho** |
| 2 × 500 g moído vendido como "1 kg" | Zaro, Morena (+1.000) | Moído entra acima de R$ 79 sem perder a busca de "1 kg" |
| Vídeo no anúncio | 8 de 20 líderes | O nosso Suave não tem; o ML marca como objetivo pendente |
| Full Super | ~1/3 dos anúncios de café 1 kg da busca têm o selo | Café 1 kg **entra** no Full do Supermercado (§5) |

Quem vende muito é **MercadoLíder ou Loja oficial**, com NF-e verificada e nota ≥ 4,8.

### 2.2 O case mais próximo: Café Fazenda Floresta (`kn-LMGBkg98`, Mamba Digital, 12/10/2026)

Torrefação dentro da fazenda (São Sebastião da Grama), 1 kg, moído, drip, cápsulas e kit
degustação. Diagnóstico de uma agência:

- **Conversão de 3,8 a 4%** no café especial; caiu 1,2 ponto em setembro quando a
  presença em promoções caiu 47% — perderam ~R$ 20 mil no mês.
- **Piso de margem de 20%**; promoção de **4 a 7%** por produto (não igual para todos) +
  **cupom de 5%** para recompra e novos seguidores; meta de ~8 mil seguidores da Minha
  Página a ~R$ 2 por seguidor.
- **O 1 kg com promoção é o que mais vende.** O kit degustação "ninguém busca": é vitrine,
  não alvo de Ads. Ads foi redirecionado para 1 kg, 500 g e 250 g.
- **Full com freio de frescor:** usam 20 a 25% da capacidade, planejam 2 meses de estoque
  repondo a cada 15 dias, mas a produtora quer a torra do próprio mês.
- Catálogo aprovado com facilidade por ter marca registrada.
- Observação do apresentador: café especial é **sensível a preço** — qualquer promoção
  multiplica o volume — e o ML **não tem assinatura**; a recorrência vem de cupom de
  seguidor.

### 2.3 Fábrica que vende direto e os grandes

| Case | O que fazem | Vale para nós? |
|---|---|---|
| C4 Embalagens, fábrica, R$ 600–700 mil/mês (`VWTxfbKDEqg`) | B2B é o principal e o ML é canal; foto/câmera na expedição contra erro de envio; título longo no catálogo | **Sim**: controle de expedição é a nossa prioridade |
| Revenda multinicho R$ 2–2,5 mi/mês (`NzBzZjbbjmw`) | 90% no Full, 10 pessoas na expedição, preço revisto 2× ao dia, atacado para PJ | Atacado PJ sim; o resto depende de escala |
| Rical, mangueiras (`oMiqvbbt724`) | Catálogo próprio ancorado em demanda medida; concorrentes entravam no catálogo e derrubavam margem; kit montado contra devolução | Catálogo **só** com marca registrada |
| Mentorados do Hugo, R$ 0,8–2,5 mi/mês (`7siNQV8hDSM`, `C_kNWk-H_i0`) | Full com 90–120 dias de estoque, marca própria, 12–14% líquido, 25% de contribuição em item barato; "8% não fecha a conta" | A régua de margem vale; o estoque fundo não (café perece) |
| Conta nova, R$ 70 mil/mês (`VYicFEhUIdQ`) | Sem Full: Flex + agência + Central de Promoções; piso de 15% depois de imposto e Ads | Prova que dá sem Full — **com conta verde** |

**Hugo Vasconcelos (Pronix).** O "método DVP" é *demanda, viabilidade, posicionamento*; as
etapas são conteúdo pago. As "5 chaves" públicas: mix em camadas, estoque fundo no Full,
Ads com gestão diária, marca própria e **3 números diários — receita aprovada, margem de
contribuição e TACOS** (`ZlApNvma05o`). Quase todo vídeo termina com "diagnóstico gratuito"
e o ecossistema dele é de revenda e importação (distribuidora e prep center próprios para
mentorados). O que fica para a fábrica: a disciplina dos 3 números, marca/catálogo
próprio, clipes múltiplos por anúncio e procurar **subcategoria menos concorrida** em vez
do produto campeão (reel `Ddwkru1DzcG`). Notas: `pesquisa/2026-10-estrategia/notas/hugo-youtube.md`
e `notas/instagram.md`.

---

## 3. Como organizar os anúncios

### 3.1 O portfólio (~11 anúncios)

| Anúncio | Tipo | Preço-alvo | MC | Papel |
|---|---|---:|---:|---|
| Grãos 1 kg **Suave** (`MLB5903454718`) | Clássico | 129,90 | 18,72 (14,4%) | âncora de busca |
| Grãos 1 kg **Clássico** (`7791049478`, pausado) | Clássico | 129,90 | 18,72 (14,4%) | âncora de busca |
| **Kit 2 × 1 kg** Suave · Clássico · misto | Clássico | 239,80 | 36,55 (15,2%) | **arma de preço por kg** |
| Moído 2 × 500 g "1 kg" (Para Coador) | Clássico | medir | — | moído acima de R$ 79 |
| Néctar de Minas 1 kg | Clássico | medir CMV | — | marca secundária (CMV não informado) |
| Cápsulas caixa de 10 / kit de 40 | Clássico | ver `13-o-que-falta.md` | — | linha própria |

Escada por kg com margem parecida: **1 kg a R$ 129,90 → kit 2 kg a R$ 119,90/kg**. Mais
fundo: kit a R$ 219,80 (R$ 109,90/kg) ainda deixa MC de R$ 21,15 (9,6%), seis vezes a do
avulso de hoje — é o preço de batalha se um concorrente forçar.

### 3.2 Clássico ou Premium

- **Clássico abaixo de R$ 150** (`swCx36qRg0w` e `14-estrategia` §3b: parcelamento não é o
  que separa quem vende café). No 1 kg o Premium (19%) a R$ 109,90 dá **prejuízo de R$ 2,17**.
- No kit 2 × 1 kg (acima de R$ 150) o Premium cobra 5 pontos: a R$ 239,80 a MC cai de 15,2%
  para 10,2%. **Kit no Clássico primeiro**; espelho Premium só quando a margem permitir
  (para repassar o mesmo valor, o Premium precisa de preço 6,9% maior).

### 3.3 Variação ou anúncio separado

**Anúncio separado por torra e por peso; kit como anúncio próprio.** Ruptura de uma
variação derruba a conversão do anúncio inteiro (`3ejzmNU8OYw`, `gLd1Amczyt8`), e as palavras
e opiniões diferem por torra. O contra é dividir avaliações numa conta de ~74 vendas/ano —
por isso não abrir anúncio além da tabela acima.

Atenção (`gLd1Amczyt8`, não verificado): com menos de 100 vendas na categoria, a nota de
experiência de compra **contamina todos os anúncios** e um anúncio novo nasce com ela.
Se valer, multiplicar anúncios antes de corrigir a expedição não adianta.

### 3.4 Catálogo, marca e loja oficial

- Catálogo próprio, Loja Oficial e Minha Página dependem de **marca registrada**
  (`DZk1gpllL2c`, `K1B3VPcliYY`, `M4_Dntq6u_g`). Sem marca, revendedor entra no nosso
  catálogo e derruba o preço (Rical, `oMiqvbbt724`).
- **Medir:** status da marca "Café Canastra" no INPI (classe de café) e o EAN/GS1. Prazo
  afirmado de 1,5 a 2 anos para deferimento (fev/2026) — se não houver pedido, protocolar já.
- **Cuidado de nome:** existe o vendedor `CAFECANASTRAPREMIUMM` (+1.000 vendas) — para o
  comprador são dois "Café Canastra" (`14-estrategia` §3b).

### 3.5 O anúncio em si

- Título: "Torra fresca" ou a data da torra; "Para Coador" no moído; pontuação só se o lote
  confirmar (a descrição do Suave diz 83).
- **Prazo de disponibilidade** com os dias reais de torra + embalagem (Patrick).
- **Tempo de preparação e capacidade de envios** (Configurações → Preferências de venda):
  três criadores do Instagram afirmam que a capacidade padrão é baixa e limita o alcance da
  conta (`DcUHUKoBLoF`, `Dcbkdl6hyNh`, `DcW7lXEyO1T`). Na mesma tela fica o tempo de
  preparação, que precisa refletir a torra real. Medir os dois antes de mexer; subir a
  capacidade sem a expedição acompanhar piora a reputação.
- Ficha limpa (marca com acento, "Torrado", nível de torra no valor do filtro, validade).
- **Clipes: três por anúncio** (atração, conversão, prova). O de conversão responde às
  **10 principais objeções** tiradas das perguntas e opiniões dos concorrentes (reel
  `Ddo1XssCdpe`): moagem, torra, validade, grão × moído, como preparar.
- Descrição abrindo com dados de origem e a escala Doçura/Acidez/Corpo/Amargor em números.

---

## 4. Frete grátis: oferecer ou não

| Faixa | Regra | Decisão |
|---|---|---|
| **A partir de R$ 79** | Frete grátis obrigatório, pago pelo vendedor pela tabela da cor da reputação (`custos.md`) | Não há escolha: baixar o frete = sair do vermelho, e diluir com kit |
| **Abaixo de R$ 79** | Afirmado: custo fixo por unidade (~R$ 6,25–7,75, `LC2tq9H_Z60`, `iq-3WlsM9N8`; há vídeo dizendo que saiu da regra geral). Comprador paga o frete | 250 g, 500 g e caixa de 10 cápsulas **avulsos não são o jogo**; vender como kit que cruza R$ 79 |

- O kit dilui o frete porque a tabela cresce menos que o peso: **kit 2 kg R$ 54,10 contra
  2 × R$ 34,30** (medido). Risco: o kit acima de R$ 200 cai na faixa de preço mais cara
  (`jZpSJpyQbUg`, `KvVyJlYt6w0`) — conferir no formulário o frete a R$ 239,80.
- Antes de publicar qualquer kit novo, **ler o frete no formulário** (o formulário mostra o
  custo exato ao trocar o preço — lição 13 do `LEIA-ME`).

---

## 5. Full, sem Full, Flex e Full Super

| Modalidade | O que muda | Para a Canastra hoje |
|---|---|---|
| **Envio próprio / coleta / agência** | Frete da tabela; o prazo de despacho é nosso | **Ficar aqui** e corrigir o despacho |
| **Full** | Mesmo frete e mesma tarifa (`XETb71Rn4dM`); custo de entrada, armazenagem, estoque antigo (carência de **2 meses** em comida), inconformidade, retirada cara | Não agora: com lote de 30 un a entrada custa ~R$ 8/un, mais que a MC de R$ 3,32 |
| **Flex** | Entrega no mesmo dia por conta própria; repasse por peso; a partir de R$ 79 "bônus de 10% se verde" (ambíguo) | Só em região metropolitana coberta; no interior "quase não tem demanda" (`LC2tq9H_Z60`) |
| **Full Super** (Supermercado) | Tabela de frete própria, armazenagem afirmada grátis em 08/2026; frete grátis ao comprador a partir de R$ 199 (afirmado, `iq-3WlsM9N8`); setor exclusivo exige Full (`lbsEvYspYTA`) | **Hipótese nº 1 para medir**: um terço dos anúncios de café 1 kg da busca de 08/10 tem o selo |

Custo extra do Full por unidade (`cenarios_estrategia.py` §4, entrada SUPOSTA de R$ 250 por lote):

| Lote | Cobertura | Custo extra/un |
|---:|---:|---:|
| 10 | 60 dias | R$ 25–27 |
| 30 | 30 dias | R$ 8–9 |
| 60 | 30 dias | R$ 4–5 |
| 120 | 30 dias | R$ 2–3 |

**Quando entrar no Full:** reputação ≥ amarela, MC ≥ 10% no SKU e giro de ~30+ vendas/mês
do SKU, lote de **3–4 semanas** com torra programada para a janela de envio (café perece;
Floresta usa só 20–25% do Full por isso). Conferir antes o requisito fiscal (endereço do ML
= endereço fiscal e faturador, `xWw-95fez58`) e em que CD o Full cai (Hugo: interior de MG
manda para SP; prep center é solução de revendedor, `Dd94VA9J8gs`).

A favor do Full, quando der: o despacho sai das nossas mãos — que é exatamente o que está
derrubando a reputação — e criadores afirmam 3–5× exposição (não medido).

---

## 6. Mercado Ads

**Pré-requisitos:** reputação amarela ou melhor (oficial, `LOZL-QmsGL4`) **e** MC ≥ 15%
no SKU. Hoje nenhum dos dois.

**Regra de verba (fábrica, Bruno Maciel `72nX2ogs8xE`):** teto = fração da margem; ele
usou 5–6% do faturamento com 18% de margem e praticou 2,8%. Aqui: **TACOS ≤ metade da MC**.

| Preço do 1 kg | MC antes de Ads | TACOS teto | ROAS objetivo mínimo |
|---:|---:|---:|---:|
| 129,90 | 14,4% | 7,2% | ≥ 10 (equilíbrio 6,9) |
| 139,90 | 18,9% | 9,4% | ≥ 8 (equilíbrio 5,3) |

**Como começar** (consenso dos vídeos, oficial incluído):
1. Uma campanha só: 1 kg e kit 2 × 1 kg (os de maior margem e conversão). Fora: 500 g,
   250 g, cápsula avulsa, kit degustação (Floresta).
2. R$ 15–20/dia; **7 dias sem mexer**; ROAS objetivo acima do equilíbrio.
3. Julgar por **TACOS e MC**, não só ROAS (`llfy7gzSOk4`, `YqRFtFqqgvQ`); tirar o que não
   retorna, reforçar o que tem TACOS baixo.
4. Corrigir o anúncio antes de pagar clique (funil impressão → clique → venda).
5. Com ~74 vendas/ano, decidir por cliques e janelas de 30 dias, não por 7 dias.
6. Se a conta for elegível ao teste grátis do ML (10–20 dias, oficial), usar no 1 kg.

Afiliados (4–12% de comissão) ficam para depois: hoje a comissão é maior que a MC.

---

## 7. Promoções, sazonalidade e recompra

- **Sem rebate do ML, toda promoção a R$ 109,90 dá prejuízo:** o desconto máximo é R$ 4,31.
- A **R$ 129,90**, uma promoção de 5% ainda deixa MC de R$ 13,72; 7% (o teto da Floresta)
  deixa R$ 11,73; com R$ 5 de rebate do ML, 5% de desconto empata com o preço cheio
  (`cenarios_estrategia.py` §6).
- **O preço no ML não pode ser maior que em outro canal** — o ML compara e pode bloquear
  promoções (`Jg4gVFGfvfw`, não verificado). Conferir site próprio e Shopee.
- **Mexer no preço para ganhar promoção piora as ofertas** (oficial, `OeOifhxKJJc`: o
  algoritmo considera o preço histórico). Subir para R$ 129,90 deve vir **antes** e ficar.
- **Black Friday 27/11 e Cyber Monday 30/11** (11/11 como teste; 12/12; Natal). Com a conta
  vermelha a Central fica trancada; o realista é posicionar o **kit 2 × 1 kg e o kit de 40
  cápsulas como presente**, com estoque de torra planejado, sem desconto que não feche.
- **Recompra:** café é o caso clássico de recorrência (`M4_Dntq6u_g`, Floresta). Minha
  Página + cupom de seguidor de 5% quando a MC permitir (a R$ 129,90 com 5% sobra R$ 13,72, ~11%).

---

## 8. O que aprender com quem revende e faz dropshipping

| Eles fazem | Por quê | Tradução para fábrica |
|---|---|---|
| Escolhem produto por demanda medida e concorrência baixa | Não controlam o produto | Escolher **subcategoria e formato** (kit, moído "para coador", torra) onde a 1ª página é fraca |
| "Raio X" das 10 objeções nos concorrentes | Converter sem marca | Vídeo e descrição respondendo às objeções de café |
| Margem de contribuição diária, TACOS | Margem fina, sem gordura | Os mesmos 3 números (Hugo) por SKU |
| Ranquear no prejuízo, depois subir preço | Recuperam na escala | **Não**: o oficial diz que mexer no preço piora as ofertas; e o CMV é fixo |
| Estoque fundo no Full (90–120 dias) | Giro de importado | **Não**: café perece; lote de 3–4 semanas |
| Curva ABC e "papéis" por SKU | Capital limitado | Curva por **margem**, não por faturamento |

**A conta que mostra a vantagem da fábrica** (`cenarios_estrategia.py` §7, mesmo café,
mesmo frete):

| Custo do produto | Quem | MC a R$ 109,90 | Preço para 15% |
|---:|---|---:|---:|
| 47,00 | Canastra (CMV) | +3,32 | 131,13 |
| 60,00 | revendedor, atacado R$ 60 | −9,68 | 152,10 |
| 70,00 | revendedor, atacado R$ 70 | −19,68 | 168,23 |

Revendedor de café especial não acompanha o nosso preço. Os que vendem barato no ML
(Vending R$ 74, Dimoá R$ 55) são café comum, outra categoria de comprador.

**Princípios de administração aplicados** (todos no script):
- **Margem de contribuição** = preço − custos variáveis (tarifa, imposto, frete, CMV, Ads).
- **Markup divisor:** preço = (CMV + frete) ÷ (1 − tarifa − imposto − margem alvo).
  Markup "30% sobre o custo" dá exatamente o equilíbrio — margem se mede sobre o preço.
- **ACOS máximo = MC ÷ preço; ROAS de equilíbrio = 1 ÷ ACOS máximo.**
- **Ponto de equilíbrio do canal** = custo fixo mensal ÷ MC unitária. Com um fixo suposto de
  R$ 3.000/mês, o canal precisa de 1.807 vendas/mês a R$ 109,90 e 321 a R$ 129,90 (com
  metade da MC em Ads). O fixo real da operação de ML não foi informado.

---

## 9. Sequência com portões

| Fase | Entra quando | O que fazer | Sai quando |
|---|---|---|---|
| **0 — Despacho e preço** (agora) | — | Diagnosticar os pedidos "afetados" (37,68%); prazo de disponibilidade real; foto/vídeo da separação; contestar o indevido com prova; 1 kg a R$ 129,90 e kit 2 × 1 kg a R$ 239,80 (autorização campo a campo); vídeo no Suave; checar INPI; **sem Ads, sem promoção, sem Full** | Reputação amarela |
| **1 — Vitrine** | Amarela | Remedir o frete do 1 kg e do kit (quanto caiu); abrir a Central (11/11 como teste); primeira campanha de Ads se MC ≥ 15%; Minha Página | Verde e ~30 vendas/mês num SKU |
| **2 — Logística** | Verde | Testar Full Super (ou Full) com lote de 3–4 semanas no SKU de giro; espelho Premium do kit; clipes completos; catálogo se a marca estiver registrada | MC ≥ 15% com Ads rodando e TACOS estável |
| **3 — Escala** | — | Mais kits (3 × 1 kg), atacado para PJ, afiliados, resposta ao convite de fornecedor 1P se vier (`HDlyoNjF3hI`, `9TAbpvDnL84`) | — |

Benefício de reputação (garantia que mascara a cor por 120 dias, `WC7JMKOXbAE`; subiu
para R$ 250 na conta): **só depois de o despacho estar corrigido**, senão perde-se a
garantia e a cor volta.

---

## 10. O que medir na conta (o agente do #mercadolivre lê sem alterar)

1. Os pedidos "afetados" da reputação e a causa de cada um; a janela de cálculo.
2. Se a conta pode criar Product Ads hoje (reputação, débitos).
3. Frete no formulário: 1 kg a R$ 129,90; kit 2 × 1 kg a R$ 239,80 (a faixa acima de R$ 200);
   2 × 500 g; kit de 40 cápsulas.
4. Categoria do café (Supermercado ou Alimentos e Bebidas) e se aparece a opção Full Super.
5. Elegibilidade e custo do Full / Full Super para café (armazenagem, carência, CD de destino).
6. Se Flex existe para o endereço da fábrica.
7. Por que a Central não mostra sugestões (cor, preço em outro canal ou falta de sugestão).
8. Minha Página, cupom de seguidor e Loja Oficial: disponíveis com a cor atual?
9. Status da marca no INPI e EAN/GS1.
10. Conversão e visitas do Suave (referência de café especial: 3,8–4%; Hugo: 50–70 visitas
    por venda no começo) no funil Métricas → Negócio → Anúncios → Detalhe.
11. Preço dos mesmos produtos no site próprio e na Shopee.
12. Alíquota efetiva do imposto (9% é o informado; Simples sobe por faixa).
13. Tempo de preparação e capacidade de envios atuais (Preferências de venda).
14. Custo de embalagem e devolução por pedido (um criador reserva 2% do preço; hoje fora
    do `precificar.py`).

---

## 11. Fontes

- Notas por tema (com cada vídeo resumido): `pesquisa/2026-10-estrategia/notas/` —
  `ads.md`, `promocoes-sazonalidade.md`, `custos-frete-full.md`, `precificacao-portfolio.md`,
  `cases-grandes.md`, `hugo-youtube.md`, `mudancas-2026.md`, `instagram.md`.
- Transcrições: `pesquisa/2026-10-estrategia/transcricoes/<id>.txt` (link no cabeçalho de
  cada uma); lista em `selecionados.txt`; busca em `videos.tsv`.
- Oficiais (canal "Vendedores Mercado Livre"): `LOZL-QmsGL4` (Ads, 30/09),
  `ms_SiNzZKkA` e `OeOifhxKJJc` (Central de Promoções, 03/09 e 29/09).
- Café: `kn-LMGBkg98` (Café Fazenda Floresta). Fábrica: `VWTxfbKDEqg`, `72nX2ogs8xE`,
  `mFZikHzI_HU`.
- Contas: `scripts/cenarios_estrategia.py` (usa `precificar.py`, conferido com o "Você
  recebe" de 3 anúncios em 14/10).
- Mercado de café: `pesquisa/concorrencia-1kg-2026-10-08.tsv` e `14-estrategia-1kg.md`.

### Limites desta pesquisa

- O ML abriu **captcha** ("Segurança — Mercado Livre") nas páginas de produto no Chrome em
  14/10; a leitura dos líderes não foi refeita (vale a de 08/10). O Rafael precisa resolver
  o captcha na mão — isso também afeta o agente do #mercadolivre.
- Busca do Instagram sem login não mostra views; a seleção foi por tema. TikTok rendeu pouco
  (perfis com alcance baixo e limite de acesso).
- Nenhum vídeo dá o frete do 1 kg nas tabelas amarela e verde, nem trata de café no Full.
