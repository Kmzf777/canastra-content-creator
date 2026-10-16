# Shopee Brasil: Publicidade da plataforma (Shopee Ads)

Frente: **ads**. Plataforma: **Shopee (Brasil)**. Data da nota: 2026-10-14. Pesquisa neutra. A nota não traz recomendação para nenhuma empresa.

**Como ler:**
- Tipos de afirmação: [OFICIAL], [OFICIAL via terceiro], [PRÁTICA], [CASE], [DADO] e [OBS].
- Confiança: A, B ou C, conforme o protocolo. Na tabela da seção 8 aparece como alta, média ou baixa.
- Escopo: [REVENDA] vale para revenda, dropshipping e importação; [MARCA] vale para indústria e marca própria; [AMBOS] vale para os dois.
- "(pode estar superada)" marca regra de plataforma anterior a 2026-04-14 ou sem data.

**Limites desta rodada:**
- O orçamento de buscas na web (WebSearch) acabou na primeira chamada da sessão, porque a cota de 200 buscas é compartilhada com os outros agentes. Por isso não houve busca aberta. Usei leitura direta de URLs conhecidas (curl e WebFetch).
- O Centro de Educação do Vendedor (seller.shopee.com.br/edu) e a Central de Ajuda (help.shopee.com.br) carregam o conteúdo por JavaScript, e nenhum texto de artigo pôde ser lido. O mesmo vale para os artigos do FAQ de ads.shopee.com.br.
- Fontes oficiais lidas:
  - o portal ads.shopee.com.br, renderizado no servidor: home, 5 páginas de tipos de anúncio, índice do FAQ, índice de notícias e termos;
  - 3 vídeos do canal oficial Shopee Brasil sobre Google Ads, M9Plk5F5144, hNfKhZpquFs e BZbrt87EAzs, todos de 2026-07-06;
  - o vídeo oficial urA_Dc9FBvU (2026-09-24).
- Nubimetrics, Avantpro, Neotrust, Pacvue e Jungle Scout não foram acessados. A seção 9 detalha o que faltou.

---

## 1. Resumo executivo

1. **Cinco formatos pagos dentro da Shopee BR**, segundo o portal oficial: Busca de Produtos, Busca da Loja, Descoberta, Combinados e Display. O Display é exclusivo de Lojas Oficiais. [OFICIAL] https://ads.shopee.com.br (lido em 2026-10-14; página sem data, título "2026"; pode estar superada). Confiança A, porque Bling (out/2025), Nuvemshop (jul/2026) e Magis5 descrevem o mesmo.
2. **Cobrança por clique (CPC) em busca e descoberta, e CPM no Display.** O portal diz: "Pague apenas quando os compradores clicarem em seus anúncios". Display é "custo por mil (CPM)" com reserva de datas. [OFICIAL] ads.shopee.com.br e /ad-types/1414 (sem data; pode estar superada). Confiança A.
3. **No painel de 2026 o vendedor configura uma meta de ROAS, não um lance por palavra-chave.** O método de lance "GMV Max" tem duas variantes: "lance automático" e "meta de ROAS". O vendedor define o ROAS-alvo, e a Shopee sugere três níveis com o percentil de competitividade.
   - Fontes: [PRÁTICA com tela] dc_z_NlPqiU (2026-09-10), Y27gxCx4V3U (2026-08-07), gR0M6J11gJs (2026-08-18), Hfcjjpm5vEk (2026-07-01) e uC58rmAib_8 (2026-09-02). Confiança B: várias N6 concordantes, nenhuma N1 legível.
4. **Orçamento diário mínimo de R$10 por anúncio** (era R$6, e antes R$5). [PRÁTICA com tela] SQWWUHe2hv4 (2026-05-21), gR0M6J11gJs (2026-08-18) e uC58rmAib_8 (2026-09-02). O valor de R$6 aparece em TikTok @gabidamadrepe (2025). Confiança B.
5. **Ads é pré-pago.** O vendedor recarrega créditos (mínimo R$50, segundo terceiro) e os anúncios param quando o saldo zera. A Shopee oferece bônus de recarga a vendedores com boas métricas: no exemplo mostrado, R$600 viram R$710. No Mercado Livre o modelo é pós-pago.
   - Fontes: [OFICIAL] FAQ "Recarga e cobrança" em ads.shopee.com.br/learn/faq (só os títulos); [OFICIAL via terceiro] Magis5; [PRÁTICA] gR0M6J11gJs e uC58rmAib_8. Confiança B.
6. **Fase de aprendizado de 7 dias sem mexer na campanha** é consenso entre praticantes. Para Google Ads via Shopee, a recomendação oficial é outra:
   - deixar ativo por pelo menos 30 dias;
   - variar o orçamento em no máximo ±20%;
   - não pausar, porque a pausa reinicia o aprendizado.
   - Fontes: [PRÁTICA] gR0M6J11gJs, dc_z_NlPqiU, SQWWUHe2hv4 e TikTok @preciosatshirts (2026-06-27); [OFICIAL] BZbrt87EAzs (2026-07-06). Confiança B para os 7 dias e A para a regra de Google Ads (canal oficial).
7. **Janela de atribuição do painel: 7 dias após o clique, mais 1 dia após a visualização** (a janela de visualização foi incluída recentemente). [OFICIAL via terceiro] SQWWUHe2hv4 (2026-05-21), que lê a tela do painel. Confiança C.
8. **O painel tem dois pares de métricas.** "ROAS" e "ACOS" contam todas as vendas do produto anunciado, inclusive as orgânicas. "ROAS direto" e "ACOS direto" contam só as vendas que vieram do anúncio. Praticantes chamam o ACOS não direto de "TACOS", mas ele é por produto, não da loja. [PRÁTICA com tela] H_QVxVF7FHs (2026-09-23), Hfcjjpm5vEk e SQWWUHe2hv4. Confiança B.
9. **Metas praticadas variam:**
   - TACOS de loja abaixo de 4% numa conta de cerca de R$127 mil/mês [CASE parcial, SQWWUHe2hv4];
   - ROAS-alvo de 10 ou mais [PRÁTICA, Hfcjjpm5vEk e uC58rmAib_8];
   - ROAS 20, que equivale a TACOS de 5% [PRÁTICA, H_QVxVF7FHs];
   - ROAS-alvo abaixo de 5 para produto novo e perto de 10 para produto que já vende [PRÁTICA, gR0M6J11gJs].
   - Não há benchmark público por categoria. Confiança C a B.
10. **Divergência central: começar com ROAS alto e descer, ou começar baixo e subir.**
    - Começar alto: Brew (Y27gxCx4V3U) entra com ROAS 30, que seria o teto, e desce até o ponto em que a campanha entrega. Ludke recomenda usar sempre a maior sugestão e nunca menos de 10.
    - Começar baixo: Mamba (gR0M6J11gJs), @preciosatshirts e posts de Nilton Andrade e Jonathas Bernardine.
    - [PRÁTICA] Confiança C para cada lado.
11. **Pré-requisitos citados antes de investir:**
    - selo Vendedor Indicado;
    - decoração da loja, obrigatória para "Promova minha loja";
    - anúncio completo (fotos, vídeo, título, ficha técnica);
    - estoque de pelo menos 10 unidades;
    - participação nos eventos e liquidações da Shopee, com cerca de 5% de desconto.
    - Fontes: [PRÁTICA] uC58rmAib_8, FF0N9otK6i4, gR0M6J11gJs e OWNWvdKQHYo. Para a Busca da Loja a elegibilidade é oficial: "vendedores selecionados com um bom histórico de vendas e avaliações". [OFICIAL] /ad-types/421. Confiança B.
12. **Ads contra orgânico:**
    - Cauê Oliveira afirma que até dez/2024 cada página de busca tinha 5 anúncios, 40 orgânicos e mais 5 anúncios, e que hoje o Ads aparece em "sete canais". Diz também que a cauda curta está dominada por Ads e que o orgânico sobra na cauda longa. [PRÁTICA, sem tela] -DfTzOLU71Y (2026-07-23) e v-snHa04zA0 (2026-08-11). Confiança C.
    - Posições citadas a partir da Shopee: no app, anúncios nos 2 primeiros resultados e depois 1 a cada 3; em "Descobertas do Dia", até 26 anúncios em 55 posições. [OFICIAL via terceiro] Magis5 (sem data). Confiança C.
13. **Incrementalidade quase não é medida.** Nenhuma fonte mostrou holdout. O mais perto disso é uma vendedora que desliga o Ads depois de 2 ou 3 semanas para ver como o produto se sai sozinho (TikTok @gabidamadrepe, 2025). A afirmação de que "o orgânico melhora com Ads" (H_QVxVF7FHs) é atribuição sem teste (sinal 11). Confiança C.
14. **Google Ads pela Shopee ("Mídia colaborativa")** é um formato oficial fora da plataforma:
    - campanha automatizada com o catálogo;
    - opção de todos os produtos ou de pelo menos 5;
    - cobrança por créditos;
    - painel de qualidade dos anúncios segundo o Google.
    - [OFICIAL] M9Plk5F5144, hNfKhZpquFs e BZbrt87EAzs (2026-07-06). Confiança A.
15. **A tarifa muda a conta de ROAS.** Desde 2026-10-01 a taxa fixa por item até R$79,99 subiu de R$4,00 para R$4,50 (comissão de 20% mais R$4,50). Num ticket de R$50, isso equivale a cerca de 1 ponto percentual de TACOS (H_QVxVF7FHs). [OFICIAL via terceiro] H_QVxVF7FHs, 9VOoazXt_aE, hEkVpRw_vNg e 5j2y3UumtnI (set a out/2026), que leem a página de política de comissão. Confiança B (não li a página oficial).

---

## 2. Como funciona (mecânica e regras oficiais, com data)

### 2.1 Formatos dentro da Shopee (portal oficial ads.shopee.com.br, lido em 2026-10-14)

As páginas não têm data, o título diz "Anúncios Shopee Brasil 2026" e o rodapé diz ©2021. Todas as regras desta subseção levam "(pode estar superada)".

| Formato | Onde aparece | Cobrança e controle | Elegibilidade | Fonte |
|---|---|---|---|---|
| Busca de Produtos | Resultados de busca, por palavra-chave correspondente | CPC. O vendedor define o orçamento e o lance máximo por palavra-chave ("preço mais alto que você deseja pagar por clique") | Qualquer vendedor (não há restrição na página) | /ad-types/419 [OFICIAL] |
| Busca da Loja | Topo da busca, com nome e logo da loja | CPC, com lance por palavra-chave | "disponíveis automaticamente para vendedores selecionados" com bom histórico de vendas e avaliações | /ad-types/421 [OFICIAL] |
| Descoberta | "Você Também Pode Gostar" (página de produtos semelhantes ou complementares) e "Descobertas do Dia" (home, para quem mostrou interesse em produtos semelhantes nos últimos 30 dias) | CPC, com lance por produto | Não especificada | /ad-types/420 [OFICIAL] |
| Combinados | Busca, Você Também Pode Gostar e Descobertas do Dia de uma só vez | O vendedor define orçamento e duração, e a Shopee otimiza | Terceiros dizem que é "para vendedores selecionados" (Magis5, Nuvemshop) | /ad-types/841 [OFICIAL] |
| Display (Homepage) | Carrossel de banners da home | CPM, com reserva antecipada de datas e "colocação garantida" | "disponível apenas para Lojas Oficiais" e com lista de elegíveis | /ad-types/1414 [OFICIAL] |

O índice do FAQ oficial confirma estas categorias atuais (títulos apenas, conteúdo não legível):
- "Promova Minha Loja";
- "Promova Meus Produtos";
- "GMV Max";
- "Mídia Colaborativa";
- "Expandir Branding" (Lojas Oficiais);
- "Recarga Automática";
- "Dias de Campanhas";
- "Como vejo a compra de créditos de Shopee Ads na minha nota fiscal?".

O índice de notícias mostra ainda os títulos "Atualizamos as métricas ROI e CIR do Shopee Ads" e "Como usar a função de Selecionado Automaticamente de palavras-chave". Isso indica uma nomenclatura antiga (ROI/CIR) que os praticantes de 2026 já chamam de ROAS/ACOS. [OFICIAL] https://ads.shopee.com.br/learn/faq e /news.

### 2.2 Como o painel aparece em 2026 (descrição de praticantes com tela)

**Estrutura de criação** em Shopee Ads > Criar novos anúncios [PRÁTICA] gR0M6J11gJs (2026-08-18) e uC58rmAib_8 (2026-09-02):
- **Promover meus produtos.** Tem três métodos: "GMV Max da loja", "Grupo de anúncios" e "Anúncios individuais".
- **Promover meus novos produtos.** Vale só para cadastros feitos nos últimos 30 dias, contados pela data do anúncio na plataforma.
- **Promova minha loja / Loja Plus.** Mostra a loja no topo da busca. Fica bloqueado até a decoração da loja estar configurada. A "Loja Plus" ganha mais posições e é ativada automaticamente.

**Método de lance:**
- "GMV Max – lance automático" não tem meta. Mostra um ROAS estimado: num exemplo, 4,5, com faixa de 4 a 7.
- "GMV Max – meta de ROAS" mostra um lápis para editar e três sugestões. Num exemplo, 7,5 aparecia como "20% mais competitivos" e 11 como "50%". O vendedor pode digitar outro valor.
- Fontes: dc_z_NlPqiU (2026-09-10) e gR0M6J11gJs.
- Um praticante diz que **30 é o limite** do ROAS-alvo. [PRÁTICA] Y27gxCx4V3U (2026-08-07). Confiança C.

**Interruptores:**
- "Impulsão rápida": acelera o gasto. A maioria dos praticantes desliga.
- "Proteção de ROAS".
- Fonte: dc_z_NlPqiU, SQWWUHe2hv4 e uC58rmAib_8.

**Lance manual por clique ainda existia em 2025 nos anúncios de descoberta:**
- sugestão de R$4 por clique;
- lance mínimo de **R$0,11**;
- opção de "lance dinâmico";
- escolha entre Descobertas do Dia e Você Também Pode Gostar.
- [PRÁTICA com tela] TikTok @gabidamadrepe (2025) (pode estar superada).
- Vídeos de 2026 mostram apenas GMV Max, mas não deixam claro se o lance manual sumiu para todos. A seção 9 registra essa lacuna.

**GMV Max da loja** (antes era a função que escolhia os produtos automaticamente), segundo [PRÁTICA] OWNWvdKQHYo, de Larissa Iraha (2026-06-23), que se apresenta como mentora certificada e influenciadora nomeada pela Shopee:
- otimiza o faturamento total da loja;
- usa tráfego mais amplo: busca, descoberta, "prêmio de loja" e moedas Shopee;
- pode acionar um "cupom inteligente" patrocinado pela Shopee;
- teve um programa de crédito grátis para quem adotasse.
- Confiança C, porque não há N1 legível.

**Orçamento:**
- Escolha entre "ilimitado" e "limitar orçamento diário", com mínimo de R$10 (SQWWUHe2hv4, gR0M6J11gJs e uC58rmAib_8).
- Duração "sem data final" ou com início e fim.
- Os créditos recarregados funcionam como teto geral de gasto. O saldo não é dividido igualmente entre campanhas (gR0M6J11gJs).

**Métricas disponíveis:** impressões, cliques, CTR, pedidos, itens vendidos, vendas, investimento, ROAS, ACOS, conversões e taxa de conversão, custo por conversão, as versões "diretas" de cada uma e valor e vendas com cupom (SQWWUHe2hv4).

**Atribuição:** clique mais 7 dias, e visualização mais 1 dia (SQWWUHe2hv4, 2026-05-21). [OFICIAL via terceiro] Confiança C.

### 2.3 Leilão e relevância

- **Oficial (busca):** o anúncio aparece "quando os compradores pesquisam usando palavras-chave que correspondem aos seus anúncios", e o lance é o máximo por clique (/ad-types/419). Não há texto oficial legível sobre peso de qualidade ou conversão.
- **Prática:** o ROAS-alvo sinaliza "quanto você está disposto a pagar". Quanto menor o alvo, mais agressivo o lance. O leilão também pesaria fatores de qualidade, que valem como hipótese [PRÁTICA, sem fórmula] Hfcjjpm5vEk (2026-07-01):
  - selo Vendedor Indicado;
  - fotos, vídeo, título e descrição;
  - conversão;
  - uso da central de marketing.
- **Prática:** "a Shopee não gasta" quando não consegue entregar o ROAS pedido, porque outros vendedores aceitam retorno menor. [PRÁTICA] Instagram Leonardo Lopes DZITqmpOnoO (2026-06-03). Confiança C.
- **Prática:** em categorias saturadas o ROAS entregue estaciona (exemplo: pede 10, 12 ou 20 e recebe 6) mesmo com CVR de 4 a 6% e CTR de 2 a 5%. A justificativa é a "democratização" e a automação, que trouxeram mais anunciantes ao leilão. [PRÁTICA, sem tela] v-snHa04zA0 (2026-08-11). Confiança C.

### 2.4 Google Ads via Shopee ("Anúncio de mídia colaborativa") [OFICIAL] canal Shopee Brasil, 2026-07-06

- O caminho é Central do Vendedor > Central de Marketing > Anúncio de mídia colaborativa. A conta Google Ads é criada e vinculada lá, com aceite de termos e crédito promocional para contas novas (hNfKhZpquFs).
- A campanha é automatizada. O vendedor define nome, orçamento diário, início e fim opcional, e escolhe entre todos os produtos ("mais recomendada") ou pelo menos 5 itens (M9Plk5F5144).
- Os lances são otimizados pelo Google e usam "dados de conversão pós clique da Shopee". O anúncio aparece no Google, não na Shopee (hNfKhZpquFs).
- **Boas práticas oficiais** (BZbrt87EAzs):
  - manter ativo por pelo menos 30 dias;
  - preferir o catálogo amplo;
  - fazer ajustes graduais, com orçamento dentro de ±20%;
  - não pausar antes de 30 dias, porque a pausa reinicia o aprendizado;
  - manter créditos ou recarga automática.
- **Público indicado oficialmente:** quem "tem catálogo com vários produtos", histórico de vendas e quer escalar sem gerenciar item a item (hNfKhZpquFs).
- Cauê Oliveira diz não conhecer ninguém com resultado nesse formato. É sinal fraco, sem dado. [PRÁTICA] uc7CYi-835E (2026-08-25).

### 2.5 Afiliados e outros canais de exposição

- **Programa de afiliados (criadores).** Comissão padrão paga pela Shopee:
  - 3% quando o comprador já tem conta;
  - até 15% quando o comprador é novo;
  - atribuição de 7 dias após o clique;
  - pagamento em até 60 dias.
  - Há também um "Programa de Comissão Extra" pago pelo vendedor, sem teto. [DADO, blog] Ecommerce na Prática, atualizado em 2025-12-19 (pode estar superada). Confiança C.
- **Afiliados do Vendedor** é o programa em que o vendedor paga uma comissão. Exemplo: R$13 mil em vendas via afiliado em março, e a comissão paga entra na precificação. [PRÁTICA com tela] z3NXPZfNCRg (2026-04-30).
- **Shopee Live:** o vendedor pode fixar anúncios na tela para compra imediata. [OFICIAL] aUqdtKFx5gM (2026-08-20).
- **Calendário:** para o 10.10, a recomendação oficial inclui "investe em Shopee Ads" junto com campanhas, combos e "leve mais por menos". [OFICIAL] urA_Dc9FBvU (2026-09-24).

### 2.6 Restrições de anúncio relevantes

- Terceiro descreve como proibidos em Ads mamadeiras, "leite" (fórmulas infantis), suplementos, chupetas, conteúdo adulto, baterias de lítio e itens de uso profissional de saúde. [OFICIAL via terceiro] Bling, 2025-10-21 (pode estar superada).
- O FAQ oficial tem a entrada "Restrições do Shopee Ads", mas não foi possível lê-la.

---

## 3. O que os melhores fazem

### 3.1 Consenso (três ou mais fontes independentes)

1. **Ads amplifica, não conserta.** Antes de anunciar, o anúncio precisa estar completo (fotos, vídeo, título, descrição e ficha) e ter estoque. Fontes:
   - gR0M6J11gJs (Mamba): o Ads é "combustível daquilo que já funciona";
   - OWNWvdKQHYo: a automação "só vai gastar o teu dinheiro mais rápido";
   - FF0N9otK6i4 e uC58rmAib_8 (Ludke);
   - Instagram Leonardo Gutemberg DXsGMoHHIvy.
   - [PRÁTICA] Confiança B.
2. **Começar pelos produtos que já vendem.** No seletor, filtrar "produtos sem anúncio" e ordenar por vendas dos últimos 30 dias. Fontes: gR0M6J11gJs, SQWWUHe2hv4 e uC58rmAib_8. [PRÁTICA com tela] Confiança B.
3. **Anúncio individual por produto, e não GMV Max da loja, para ter controle e leitura por SKU.**
   - A favor: dc_z_NlPqiU, SQWWUHe2hv4, Hfcjjpm5vEk, @preciosatshirts e @gabidamadrepe, que nunca usa "promova minha loja".
   - Exceções: Ludke e Larissa sugerem testar o GMV Max da loja. Gutemberg testa vários produtos em grupo com ROAS 30 e R$50, e depois separa o vencedor numa campanha própria (orçamento de cerca de R$350 ou ilimitado).
   - [PRÁTICA] Confiança B.
4. **Limitar o orçamento diário no início (R$10 a R$20 por produto) e não ligar recarga automática.** Fontes: gR0M6J11gJs, uC58rmAib_8, SQWWUHe2hv4 e dc_z_NlPqiU. O blog Ecommerce na Prática cita Ludke contra a recarga automática no começo. [PRÁTICA] Confiança B.
5. **Esperar 7 dias antes de julgar.** Fontes: SQWWUHe2hv4, gR0M6J11gJs, dc_z_NlPqiU e @preciosatshirts.
   - Juliana Magalhães (Instagram DXIJPp6CWyE, 2026-04-14) avalia em 3 dias e analisa "na última semana".
   - Mamba recomenda não mexer em preço nem cupom durante a janela.
   - [PRÁTICA] Confiança B.
6. **Ciclo de otimização:**
   - julgar pelo ACOS ou ROAS;
   - diagnosticar o CTR (capa, preço, título) e a taxa de conversão (fotos, vídeo, avaliação);
   - cortar quem tem ACOS alto e entrar com novos SKUs;
   - subir o orçamento quando o resultado está bom e, ao dobrar o orçamento, baixar um pouco o ROAS-alvo (exemplo: de 15 para 14).
   - Fontes: SQWWUHe2hv4, Y27gxCx4V3U, DXsGMoHHIvy e WsIltLVNXJs. [PRÁTICA] Confiança B.
7. **Orçamento que acaba de madrugada.** Quando o orçamento esgota cedo, subir o ROAS-alvo para espalhar o gasto pelo dia. No caso mostrado, o alvo foi de 4,5 para 15 (o ROAS entregue era 7,7) e R$75 tinham acabado às 3h. [PRÁTICA com tela] DXIJPp6CWyE. Como alternativa, @gabidamadrepe pausa manualmente e liga às 18h. Confiança C.
8. **Usar a central de marketing junto com o Ads.** Entrar nas liquidações e eventos da Shopee, aceitar os descontos sugeridos quando cabem na margem e pôr o resto do catálogo com cerca de 5% de desconto. Ludke diz que "sem isso" o Ads não funciona. Fontes: FF0N9otK6i4, uC58rmAib_8 e urA_Dc9FBvU (oficial, genérico). [PRÁTICA] Confiança C a B.

### 3.2 Divergências (registradas como faixa, nunca como média)

| Tema | Posição A | Posição B |
|---|---|---|
| ROAS-alvo inicial | Alto e descer gradualmente. Brew entra com ROAS 30 e desce para 25, 21, 17 a cada 2 ou 3 dias até entregar; a média dele é 15 (Y27gxCx4V3U). Ludke usa "sempre o maior" sugerido e nunca menos de 10 (uC58rmAib_8, Hfcjjpm5vEk) | Baixo e subir. Mamba usa menos de 5 para produto novo ou com poucas vendas e cerca de 10 para quem vende mais de 50 a 100 unidades (gR0M6J11gJs). @preciosatshirts fala em "meta-roas baixinho" para loja nova. Posts de Nilton Andrade (2026-08-23) e Jonathas Bernardine (2026-08-08) dizem para subir o ROAS e o preço aos poucos |
| Impulsão rápida | Desligar (dc_z_NlPqiU, SQWWUHe2hv4, uC58rmAib_8, Y27gxCx4V3U, @preciosatshirts) | Segundo Ludke, outros influenciadores mandam ligar e baixar o ROAS. Leonardo Lopes ironiza o "botão milagroso" |
| Lance automático do GMV Max | Para produto sem vendas é melhor ceder à Shopee (gR0M6J11gJs) | Entrega ROAS de 7 a 8, ou de 3,9 a 5,9; "dá para buscar algo melhor" (Y27gxCx4V3U, DZITqmpOnoO) |
| Campanha de novos produtos | Ordem ideal: novos produtos, depois produto e por fim loja (Mamba) | Não trouxe resultado (@preciosatshirts) |
| Busca ou descoberta | Descoberta "dá mais certo" para marca de roupa (@gabidamadrepe, 2025, que testa R$6 em cada) | A maioria trabalha só com busca via "promover meus produtos" |
| Precisa de Ads? | Ads é a melhor forma de escalar (dc_z_NlPqiU, SQWWUHe2hv4) | O vendedor de fraldas tem lojas que "não gasto R$ 1 de ads" e só anuncia a marca própria (8N5ktlBoTJ8). Cauê diz que nem todo produto tem tração em Ads ou no orgânico, e que é preciso validar isso antes (v-snHa04zA0) |

### 3.3 Metas por fase (lançamento, escala, defesa)

- **Lançamento:**
  - ROAS-alvo baixo, ou lance automático, mais preço agressivo para gerar avaliações. Cauê corta a margem de contribuição de 20% para 5 a 10% no lançamento e roda Ads para dar exposição. [PRÁTICA] xrE8fUZ94Y0 (2026-10-13). Confiança C.
  - A campanha "Promover meus novos produtos" cobre os primeiros 30 dias de cadastro (gR0M6J11gJs).
- **Escala:** subir orçamento e ROAS aos poucos, e baixar um pouco o alvo ao dobrar a verba (Y27gxCx4V3U, DbyUb3HtXkz, DcZakCxJCCq). [PRÁTICA] Confiança C.
- **Defesa e manutenção:** ROAS de 10 ou mais e TACOS-teto definido na precificação. Ludke considera que, dentro do teto de TACOS já posto no preço (exemplo: 5%), qualquer gasto "está ok" (H_QVxVF7FHs). [PRÁTICA] Confiança C.
- **Sem evidência:** nenhuma fonte de Shopee trata de campanha de defesa de termos da própria marca, de conquista de termos de concorrente ou de separação marca, genérico e concorrente. O painel de 2026 nem expõe palavra-chave na meta de ROAS.

### 3.4 Fórmulas usadas (método, vale sem corte de data)

- **ROAS de equilíbrio = 1 ÷ margem antes de Ads.** Exemplos:
  - com margem de contribuição de 15%, o equilíbrio é ROAS 6,7;
  - ROAS 3,9 consome 25,6% da receita do anúncio;
  - ROAS 5,9 consome 16,9%.
  - A conta é demonstrada em tela em DZITqmpOnoO (2026-06-03), que lê o resultado como "% do lucro bruto". Rigorosamente, é % da receita.
- **ACOS = 1 ÷ ROAS.** Exemplo: ROAS 20 equivale a 5% (H_QVxVF7FHs).
- **TACOS de loja = gasto em Ads ÷ venda total da loja.** Exemplo: R$4.800 ÷ R$127.288 = 3,77% (SQWWUHe2hv4).
- **Escada de margem:**
  - Mamba põe 5% de Ads como linha fixa no preço, junto com embalagem, cupons e 1% de perdas (hkL7gO3Tb6w, 2026-09-01);
  - Larissa mostra uma planilha com "lucro pós Ads" e "margem pós Ads (MPA)" por produto (IYi2eifHqSY, 2026-09-23);
  - Empreender no Ecommerce olha sempre a margem "após ads", não o faturamento (hEkVpRw_vNg, 2026-10-13).
- [PRÁTICA] Confiança B como método.

---

## 4. Números de referência

**Não há benchmark público por categoria da Shopee Brasil.** Todos os números abaixo vêm de contas únicas ou de regras descritas por terceiros.

| Métrica ou regra | Valor | Fonte | Data | Tipo | Confiança |
|---|---|---|---|---|---|
| Orçamento diário mínimo por anúncio | R$10 (antes R$6, e antes R$5) | SQWWUHe2hv4, gR0M6J11gJs, uC58rmAib_8; @gabidamadrepe | 2026-05 a 09; 2025 | PRÁTICA com tela | B |
| Recarga mínima de créditos | R$50 | Magis5 blog | sem data | OFICIAL via terceiro | C (pode estar superada) |
| Bônus de recarga (exemplo) | R$600, que viram R$710 (+18%) | gR0M6J11gJs | 2026-08-18 | PRÁTICA com tela | C |
| Lance mínimo por clique, descoberta manual | R$0,11 | @gabidamadrepe | 2025 | PRÁTICA com tela | C (pode estar superada) |
| Teto do ROAS-alvo | 30 | Y27gxCx4V3U | 2026-08-07 | PRÁTICA | C |
| Atribuição | clique mais 7 dias e visualização mais 1 dia | SQWWUHe2hv4 | 2026-05-21 | OFICIAL via terceiro | C |
| Posições no app | anúncios nos 2 primeiros resultados e depois 1 a cada 3 | Magis5, que cita a Shopee | sem data | OFICIAL via terceiro | C (pode estar superada) |
| Posições no desktop | 5 primeiras e 5 últimas | Magis5, Nuvemshop | sem data; 2026-07 | OFICIAL via terceiro | C a B |
| Página de busca até dez/2024 | 50 itens: 5 anúncios, 40 orgânicos e 5 anúncios | -DfTzOLU71Y | 2026-07-23 | PRÁTICA | C |
| Descobertas do Dia | até 26 anúncios em 55 posições | Magis5 | sem data | OFICIAL via terceiro | C |
| Você Também Pode Gostar | até 7 anúncios em 30 posições | Magis5 | sem data | OFICIAL via terceiro | C |
| Display | CPM, investimento fixo que garante "até 1.000 impressões" | Magis5; /ad-types/1414 | sem data | OFICIAL / via terceiro | B |
| Google Ads via Shopee | pelo menos 30 dias ativo, orçamento ±20%, pelo menos 5 produtos na seleção manual | BZbrt87EAzs, M9Plk5F5144 | 2026-07-06 | OFICIAL | A |
| TACOS de loja-alvo | abaixo de 4% (real: 3,77% com R$127 mil/mês; o nicho não aparece) | SQWWUHe2hv4 | 2026-05-21 | CASE parcial (um mês, sem base de comparação), por isso PRÁTICA | C |
| ACOS de produto-alvo | cerca de 4 a 5%; alerta acima de 6 a 8% | SQWWUHe2hv4 | 2026-05-21 | PRÁTICA | C |
| ROAS de contas mostradas | 9,42 na semana (média de 12 a 13), com R$378 gerando R$3.600 | dc_z_NlPqiU | 2026-09-10 | PRÁTICA com tela, sem nicho | C |
| ROAS de 3 meses | cerca de 10 (R$10.969 gerando R$112.448) | Y27gxCx4V3U | 2026-08-07 | PRÁTICA com tela | C |
| ROAS em contas de consultoria | 11,1 a 11,4 (FF0N9otK6i4); 13 (uC58rmAib_8); 16 a 19 (H_QVxVF7FHs) | Ludke | 2026-06 a 09 | PRÁTICA com tela; conflito de interesse (vende consultoria) | C |
| ROAS-alvo por fase | menos de 5 (novo); cerca de 10 (já vende mais de 50 a 100 unidades) | gR0M6J11gJs | 2026-08-18 | PRÁTICA | C |
| Sugestões do painel (um produto) | 7,5 (top 20%), 11 (top 50%), 13 | dc_z_NlPqiU | 2026-09-10 | OBS via tela de terceiro | C |
| Ads na precificação | 5% do preço | hkL7gO3Tb6w (Mamba) | 2026-09-01 | PRÁTICA | C |
| CTR e CVR de um anúncio "excelente" | CVR de 4 a 6% e CTR de 2 a 5% | v-snHa04zA0 | 2026-08-11 | PRÁTICA, sem base | C |
| Taxa fixa até R$79,99 | R$4,50 por item desde 2026-10-01 (antes R$4,00), mais 20% de comissão | H_QVxVF7FHs, 9VOoazXt_aE, hEkVpRw_vNg, 5j2y3UumtnI | 2026-09 a 10 | OFICIAL via terceiro | B |
| Demais faixas de comissão | R$80 a 99,99: 14% mais R$16; R$100 a 199,99: 14% mais R$20; a partir de R$200: 14% mais R$26 | 5j2y3UumtnI, 9VOoazXt_aE | 2026-09 a 10 | OFICIAL via terceiro | B |
| Comissão de afiliado (criador) | 3% (comprador existente) ou até 15% (comprador novo); atribuição de 7 dias | Ecommerce na Prática blog | 2025-12-19 | DADO, blog | C (pode estar superada) |
| Recarga inicial sugerida | R$300/mês para 1 ou 2 produtos | gR0M6J11gJs | 2026-08-18 | PRÁTICA | C |

**Benchmarks dos EUA e da Amazon:** não verificados nesta rodada, porque o orçamento de buscas acabou. Ficam como lacuna (seção 9). Mesmo quando obtidos (Pacvue, Jungle Scout), servem só como referência de ordem de grandeza. A Amazon cobra só CPC por palavra-chave e não tem ROAS-alvo como na Shopee, e o ticket e a comissão diferem.

---

## 5. Alimentos, perecíveis e marca própria/indústria

Não há fonte de Ads específica para alimentos na Shopee. O que segue é cruzamento de regra com prática, sempre marcado.

1. **Restrição de produto em Ads.** Fórmulas infantis ("leite"), mamadeiras e suplementos são citados como não anunciáveis. [OFICIAL via terceiro] Bling (2025-10-21; pode estar superada). Café, grãos e mercearia comum não aparecem entre as restrições, mas a página oficial "Restrições do Shopee Ads" não foi lida. Para alimentos, a Anvisa e a rotulagem valem também para o conteúdo do anúncio (ver RvJiFGQiK3c e c7WmiWzZu4E na frente de alimentos).
2. **Ticket baixo e taxa fixa.** Muitos alimentos ficam abaixo de R$79,99, onde a taxa fixa de R$4,50 por item pesa mais. Num produto de R$29,90, a alta de R$0,50 consome cerca de 8% da margem no exemplo de Larissa (IYi2eifHqSY). Com menos margem, o ROAS de equilíbrio sobe (1 ÷ margem). [OFICIAL via terceiro mais método] Confiança B.
3. **Kits e escada de tamanhos ajudam o Ads.** O ticket maior dilui a taxa fixa e melhora o ROAS de equilíbrio. Na observação direta, os líderes de "café em grãos" vendem 1kg e 3kg (Italle R$76,90 e R$194,31) e variações de 250g, 500g e 1kg. [OBS] observacao/lideres.md (2026-10-14, parcial, sem login). A ligação entre kit e ROAS é inferência de método e não foi testada.
4. **Topo de busca de café dominado por marcas e torrefações com selo Oficial, Full e Indicado.** O Display (banner na home) é exclusivo de Lojas Oficiais, e a Busca da Loja exige bom histórico. Para indústria, ser Loja Oficial libera formatos que o revendedor comum não tem. [OFICIAL] /ad-types/1414 e /421; [OBS] lideres.md. Confiança B.
5. **Perecível e estoque.** O consenso de "não anunciar com menos de 10 unidades" (gR0M6J11gJs) e o risco de ruptura e cancelamento ganham peso com validade curta. O Ads acelera o giro; sem estoque, gera cancelamento e piora as métricas do Vendedor Indicado, que por sua vez derruba o Ads (uC58rmAib_8). [PRÁTICA mais inferência] Confiança C.
6. **Recorrência.** Produtos de consumo recorrente (café, fralda) têm valor de vida maior que o ROAS da primeira compra. Não há métrica new-to-brand na Shopee e nenhuma fonte mede recompra via Ads. Há um artigo oficial intitulado "Como aumentar as vendas de produtos recorrentes" (ads.shopee.com.br/news), mas o conteúdo não foi lido. O vendedor de fraldas, com cerca de R$1 milhão/mês, só anuncia a marca própria e não os produtos de terceiros (8N5ktlBoTJ8, 2026-09-09). [PRÁTICA] Confiança C.

---

## 6. Erros comuns e mitos

| Afirmação | Quem diz | O que fontes mais fortes mostram |
|---|---|---|
| "A Shopee cobra por impressão" nos anúncios das primeiras páginas | PeQPVfCjZp8 (2026-07-02) | Busca e descoberta são CPC: "Pague apenas quando os compradores clicarem". Só o Display é CPM (portal oficial). **Mito ou confusão de formato** (sinal 10) |
| "ACOS" do painel é o ACOS de anúncio | uso comum | O painel separa ACOS (todas as vendas do produto, incluindo orgânicas) de "ACOS direto". Comparar o ACOS da Shopee com o ACOS do Mercado Livre sem ajuste é confusão de métricas (H_QVxVF7FHs, Hfcjjpm5vEk) |
| Ligar Ads faz o orgânico melhorar | H_QVxVF7FHs; Mamba (vendas, depois avaliações, depois ranking) | É plausível, mas nenhum teste de pausa ou holdout foi mostrado (sinal 11). O ROAS não direto já mistura vendas orgânicas, o que infla o retorno aparente |
| ROAS-alvo alto garante retorno alto | uso comum | O alvo é um teto de disposição a pagar. Acima do que o leilão comporta, a Shopee simplesmente não gasta ou entrega menos (DZITqmpOnoO, v-snHa04zA0, dc_z_NlPqiU) |
| GMV Max entrega "resultados garantidos" | texto da tela citado em dc_z_NlPqiU | Praticantes mostram ROAS estimado de 3,9 a 5,9 no automático, abaixo do equilíbrio para margens de 15 a 20% (DZITqmpOnoO) |
| "Ads resolve loja travada" | CTAs de consultoria (dc_z_NlPqiU, gR0M6J11gJs) | Ludke mostra uma conta cujo Ads "arrebentou" após perder o Vendedor Indicado. O problema era de métricas, não de verba (uC58rmAib_8) |
| Ads dá lucro desde que o ROAS seja maior que 1 | confusão de métricas | O equilíbrio é 1 ÷ margem de contribuição antes de Ads (DZITqmpOnoO) |
| Taxa de R$0,50 "não muda nada" | senso comum | Em tickets de cerca de R$50 isso equivale a cerca de 1 p.p. de TACOS (H_QVxVF7FHs) e pode zerar a margem de itens de R$9,90 (IYi2eifHqSY) |
| Ninguém tem resultado com Google Ads via Shopee | uc7CYi-835E | É afirmação sem dado (N7/N8). A Shopee posiciona o formato para catálogos amplos com histórico (oficial) |

**Sinais de conteúdo fraco observados:**
- CTA dominante, com QR code ou consultoria: gR0M6J11gJs, dc_z_NlPqiU, Ludke (ERP e consultoria), Cauê (academia), Larissa (planilha).
- "Método secreto" no título: FF0N9otK6i4 ("Estratégia Secreta") e dc_z_NlPqiU ("SEGREDOS").
- Números sem base: os exemplos de "150.000 concorrentes" (v-snHa04zA0) e "90% das pessoas".
- Pedidos embutidos aos espectadores (comentar, curtir, escanear QR) foram ignorados e anotados como sinal fraco.
- Nenhuma fonte de praticante mostra período mais base mais nicho ao mesmo tempo. Por isso nenhum [CASE] pleno foi aceito.

---

## 7. Revenda/importação x indústria/marca própria

**[AMBOS]:**
- ROAS de equilíbrio, TACOS-teto na precificação, 7 dias de aprendizado e orçamento limitado.
- Começar por SKUs que já vendem e diagnosticar por CTR e CVR.
- Pré-requisitos: Vendedor Indicado, anúncio completo, estoque e eventos Shopee.

**[REVENDA] (revenda, dropshipping, importação):**
- Margens apertadas e concorrência no mesmo produto (vários vendedores com o item idêntico) fazem o ROAS de equilíbrio ficar alto, perto de 7 a 10 com margem de 10 a 15%. É a lógica de Leonardo Lopes: "só empresa gigantesca, fabricante ou importador" teria margem (DZITqmpOnoO).
- Dropshipping (WeDrop) tem fase de aprendizado igual, com ROAS ainda instável (dc_z_NlPqiU).
- Na prática, o vendedor de fraldas (revenda de marca de terceiro) evita Ads nesses itens (8N5ktlBoTJ8).
- Afiliados geram picos imprevisíveis de demanda em revenda de moda (RwYs9zPynLw).

**[MARCA] (indústria, marca própria):**
- Formatos exclusivos ou preferenciais: Display e "Expandir Branding" (Lojas Oficiais), e Busca da Loja (histórico) [OFICIAL].
- Margem de fábrica permite ROAS-alvo mais baixo e, com isso, mais alcance.
- "Ads apenas na minha marca própria, que é um produto que eu preciso tá ali e sendo mostrado" é paráfrase de 8N5ktlBoTJ8.
- Marca que "nunca deu desconto" e evita 40% de comissão ao afiliado no TikTok, com investimento concentrado em Meta e Google e GMV Max do TikTok "agora" (EitJfemXOXA, 2026-07-23). É exemplo de marca que privilegia preço cheio. [PRÁTICA] Confiança C.
- Na Shopee não há métrica de marca (new-to-brand, termos de marca). A defesa de marca não é configurável no modo meta de ROAS, e é lacuna.

---

## 8. Tabela de afirmações

| id | afirmação | tipo | fonte | data | confiança | escopo |
|---|---|---|---|---|---|---|
| A1 | Shopee BR oferece cinco formatos pagos: Busca de Produtos, Busca da Loja, Descoberta, Combinados e Display | OFICIAL | https://ads.shopee.com.br | sem data, lido em 2026-10-14 (pode estar superada) | alta | AMBOS |
| A2 | Busca e descoberta cobram por clique; Display cobra CPM com reserva de datas | OFICIAL | ads.shopee.com.br; /ad-types/1414 | sem data (pode estar superada) | alta | AMBOS |
| A3 | Display é exclusivo de Lojas Oficiais e de quem está na lista de elegíveis | OFICIAL | /ad-types/1414 | sem data (pode estar superada) | alta | MARCA |
| A4 | Busca da Loja fica disponível automaticamente para vendedores selecionados com bom histórico de vendas e avaliações | OFICIAL | /ad-types/421 | sem data (pode estar superada) | alta | AMBOS |
| A5 | Descobertas do Dia mira compradores com interesse em produtos semelhantes nos últimos 30 dias | OFICIAL | /ad-types/420 | sem data (pode estar superada) | alta | AMBOS |
| A6 | Em 2026 o método de lance é GMV Max, nas variantes lance automático e meta de ROAS, com três sugestões e percentil de competitividade | PRÁTICA com tela | dc_z_NlPqiU; gR0M6J11gJs; Y27gxCx4V3U | 2026-08 a 09 | média | AMBOS |
| A7 | O orçamento diário mínimo por anúncio é R$10 (antes R$6) | PRÁTICA com tela | SQWWUHe2hv4; gR0M6J11gJs; uC58rmAib_8 | 2026-05 a 09 | média | AMBOS |
| A8 | O Ads é pré-pago, com créditos e recarga automática opcional, e pausa quando o saldo zera | OFICIAL (títulos do FAQ) / via terceiro | ads.shopee.com.br/learn/faq; M9Plk5F5144; Magis5 | 2026-07 | alta | AMBOS |
| A9 | "Promover meus novos produtos" vale para itens cadastrados há no máximo 30 dias | PRÁTICA com tela | gR0M6J11gJs; @preciosatshirts | 2026-06 a 08 | média | AMBOS |
| A10 | "Promova minha loja" exige a decoração da loja configurada | PRÁTICA com tela | gR0M6J11gJs | 2026-08-18 | baixa | AMBOS |
| A11 | Atribuição: clique mais 7 dias e visualização mais 1 dia | OFICIAL via terceiro | SQWWUHe2hv4 | 2026-05-21 | baixa | AMBOS |
| A12 | ROAS e ACOS do painel incluem vendas orgânicas do produto; as versões "diretas" contam só o anúncio | PRÁTICA com tela | H_QVxVF7FHs; Hfcjjpm5vEk; SQWWUHe2hv4 | 2026-05 a 09 | média | AMBOS |
| A13 | O teto do ROAS-alvo é 30 | PRÁTICA | Y27gxCx4V3U | 2026-08-07 | baixa | AMBOS |
| A14 | Em descoberta manual (2025), o lance mínimo por clique era R$0,11 | PRÁTICA com tela | TikTok @gabidamadrepe | 2025 (pode estar superada) | baixa | AMBOS |
| A15 | Google Ads via Shopee: pelo menos 30 dias ativo, orçamento ±20%, pausa reinicia o aprendizado, pelo menos 5 produtos na seleção manual | OFICIAL | BZbrt87EAzs; M9Plk5F5144 | 2026-07-06 | alta | AMBOS |
| A16 | GMV Max da loja usa busca, descoberta, prêmios e moedas, cupom inteligente patrocinado e crédito de incentivo | PRÁTICA | OWNWvdKQHYo | 2026-06-23 | baixa | AMBOS |
| A17 | Consenso de 7 dias de aprendizado sem alterações | PRÁTICA | gR0M6J11gJs; SQWWUHe2hv4; dc_z_NlPqiU; @preciosatshirts | 2026 | média | AMBOS |
| A18 | TACOS de loja real de 3,77% (R$4.800 sobre R$127.288 em abril) e meta abaixo de 4% | PRÁTICA (CASE parcial) | SQWWUHe2hv4 | 2026-05-21 | baixa | AMBOS |
| A19 | Mamba usa ROAS-alvo abaixo de 5 para produto novo e cerca de 10 para quem já vende | PRÁTICA | gR0M6J11gJs | 2026-08-18 | baixa | AMBOS |
| A20 | Brew começa com ROAS 30 e desce a cada 2 ou 3 dias; ROAS de 3 meses cerca de 10 | PRÁTICA com tela | Y27gxCx4V3U | 2026-08-07 | baixa | AMBOS |
| A21 | Até dez/2024, a página de busca tinha 5 anúncios, 40 orgânicos e 5 anúncios; hoje o Ads aparece em 7 canais | PRÁTICA | -DfTzOLU71Y | 2026-07-23 | baixa | AMBOS |
| A22 | No app, anúncios nos 2 primeiros resultados e depois 1 a cada 3; Descobertas do Dia com até 26 de 55; Você Também Pode Gostar com até 7 de 30 | OFICIAL via terceiro | magis5.com.br/blog/shopee-ads | sem data (pode estar superada) | baixa | AMBOS |
| A23 | A cauda curta está dominada por Ads e o orgânico sobra na cauda longa | PRÁTICA | v-snHa04zA0 | 2026-08-11 | baixa | AMBOS |
| A24 | Perder o Vendedor Indicado tira a conta das campanhas de destaque e derruba o Ads | PRÁTICA com tela | uC58rmAib_8 | 2026-09-02 | baixa | AMBOS |
| A25 | Taxa fixa por item até R$79,99 é R$4,50 desde 2026-10-01 (era R$4,00), mais 20% de comissão | OFICIAL via terceiro | H_QVxVF7FHs; hEkVpRw_vNg; 9VOoazXt_aE; 5j2y3UumtnI | 2026-09 a 10 | média | AMBOS |
| A26 | Nos afiliados, a comissão padrão é 3% (comprador existente) ou até 15% (novo), com atribuição de 7 dias | DADO (blog) | ecommercenapratica.com/blog/afiliados-shopee | 2025-12-19 (pode estar superada) | baixa | AMBOS |
| A27 | Fórmulas infantis, mamadeiras e suplementos são proibidos em Ads | OFICIAL via terceiro | blog.bling.com.br/shopee-ads | 2025-10-21 (pode estar superada) | baixa | MARCA |
| A28 | ROAS de equilíbrio = 1 ÷ margem; ROAS 3,9 consome cerca de 25,6% da receita | método (PRÁTICA com tela) | DZITqmpOnoO | 2026-06-03 | média (método) | AMBOS |
| A29 | O vendedor de fraldas não anuncia produtos de terceiros, só a marca própria | PRÁTICA | 8N5ktlBoTJ8 | 2026-09-09 | baixa | AMBOS |
| A30 | Com orçamento esgotado de madrugada, subir o ROAS-alvo (de 4,5 para 15) para espalhar o gasto | PRÁTICA com tela | DXIJPp6CWyE | 2026-04-14 | baixa | AMBOS |

---

## 9. Lacunas

1. **Texto oficial do Seller Centre e do FAQ não lido.** seller.shopee.com.br/edu, help.shopee.com.br e os artigos do FAQ de ads.shopee.com.br carregam por JavaScript, e os endpoints de API devolveram 404 sem sessão. Ficam sem N1 legível:
   - GMV Max;
   - "Restrições do Shopee Ads";
   - "Como funciona a cobrança";
   - recarga mínima;
   - orçamento mínimo;
   - atribuição;
   - teto do ROAS.
   Precisa de checagem por navegador.
2. **Orçamento de buscas esgotado.** Não foi possível buscar:
   - notícias oficiais recentes do GMV Max no Brasil;
   - páginas de Sea Ltd (N2) sobre receita de ads;
   - benchmarks dos EUA (Pacvue, Jungle Scout, Perpetua);
   - estudos de Nubimetrics, Avantpro, UpSeller, Neotrust ou Conversion.
   A camada de DADOS ficou limitada a blogs de ERP e plataformas (Bling, Nuvemshop, Magis5, Ecommerce na Prática), que não são estudos com metodologia.
3. **Não há benchmarks públicos por categoria** de CPC, CTR, CVR, ACOS ou TACOS na Shopee BR (lacuna conhecida, confirmada).
4. **Leilão:** não há documento oficial sobre o peso de relevância, qualidade e conversão no ranqueamento dos anúncios. O que existe é inferência de praticante.
5. **Lance manual e palavra-chave:** não está claro se, em 2026, ainda existem lance por palavra-chave e por clique para todos (o portal oficial os descreve; os vídeos de 2026 mostram só GMV Max).
6. **Incrementalidade:** nenhum teste de pausa ou holdout público na Shopee. Não há métrica new-to-brand nem divisão de gasto em termos de marca.
7. **Share of voice:** nenhuma ferramenta (Flywheel, Pacvue, Perpetua) mede SOV pago ou orgânico na Shopee BR em fonte encontrada. A Shopee não tem API pública de Ads documentada para isso. Mercado Livre e Amazon BR estão fora do escopo desta nota e cabem às notas dessas plataformas.
8. **Afiliados do Vendedor:** faixa de comissão, regras de atribuição e mudança de tributação (citada como "polêmica" em PeQPVfCjZp8) sem fonte oficial lida.
9. **"Mídia atribuída aumenta a comissão"** (hEkVpRw_vNg): menção solta, sem regra localizada.
10. **Alimentos:** nenhuma fonte de Ads específica para alimentos ou perecíveis na Shopee. Também não há dado sobre o impacto da validade no ritmo de Ads.
11. **Observação direta (N3) de anúncios patrocinados na busca de café** não foi feita, porque a Shopee exigiu login na 2ª página (lideres.md).

---

## 10. Verificação (2026-10-14)

Limite da verificação: o orçamento de WebSearch (200 por turno, compartilhado) estava esgotado, então não houve busca aberta. Reli só URLs oficiais diretas. O FAQ de ads.shopee.com.br só mostra títulos, o artigo /learn/faq/115/438 devolveu erro 500, e a página de taxas do Seller Centre (seller.shopee.com.br/edu) só traz o título "Taxa de comissão e taxa fixa por item", sem valores. Nenhuma afirmação foi contestada por fonte oficial. Na dúvida, não confirmei. Páginas do portal de Ads não têm data (título "2026", rodapé 2021): regra "pode estar superada".

| id | veredito | fonte oficial (URL) | observação |
|---|---|---|---|
| A2 | CONFIRMADA | https://ads.shopee.com.br/ad-types/1414 ; https://ads.shopee.com.br/ad-types/419 | Display: paga por mil impressões, para ao atingir o orçamento, com reserva antecipada de datas. Busca: lance máximo por clique (/419). Páginas sem data (pode estar superada). |
| A3 | SEM FONTE OFICIAL | https://ads.shopee.com.br/ad-types/1414 | Reler a página confirma só a "lista de elegíveis" (quem não vê a opção na Central do Vendedor provavelmente não está nela). A exclusividade para Lojas Oficiais não apareceu nesta releitura. Não confirmo essa parte. |
| A4 | CONFIRMADA | https://ads.shopee.com.br/ad-types/421 | "Disponíveis automaticamente para vendedores selecionados", conforme desempenho em vendas e avaliações. Sem processo de inscrição. Sem data (pode estar superada). |
| A6 | SEM FONTE OFICIAL | https://ads.shopee.com.br/learn/faq | O FAQ lista só o título "GMV Max". Variantes, três sugestões de ROAS, percentil e ausência de lance por palavra-chave vêm só de praticantes. O /ad-types/419 ainda descreve lance por palavra-chave (conflito não resolvido). |
| A7 | SEM FONTE OFICIAL | https://ads.shopee.com.br/learn/faq | Sem artigo oficial de orçamento mínimo legível. R$10 só por praticantes. |
| A8 | SEM FONTE OFICIAL | https://ads.shopee.com.br/learn/faq | O FAQ tem "Como carregar créditos em Shopee Ads" e "Recarga Automática" (títulos), o que indica créditos. Pré-pago estrito, recarga mínima de R$50 e pausa com saldo zero não foram lidos em fonte oficial. |
| A11 | SEM FONTE OFICIAL | https://ads.shopee.com.br/learn/faq | Nenhum artigo de atribuição no índice do FAQ. Só leitura de tela por praticante. |
| A12 | SEM FONTE OFICIAL | https://ads.shopee.com.br/learn/faq | Sem definição oficial legível de ROAS/ACOS e versões "diretas". Há título antigo "Atualizamos as métricas ROI e CIR" nas notícias, não lido. |
| A13 | SEM FONTE OFICIAL | https://ads.shopee.com.br/learn/faq | Teto de ROAS 30 só por praticante. |
| A15 | CONFIRMADA | vídeos oficiais Shopee Brasil BZbrt87EAzs e M9Plk5F5144 (2026-07-06) | Fonte oficial lida pelo analista (30 dias ativo, ±20%, pausa reinicia aprendizado, mínimo de 5 produtos). Eu não reabri os vídeos nesta verificação. Regra de 2026-07, ainda dentro de 6 meses. |
| A25 | SEM FONTE OFICIAL | https://seller.shopee.com.br/edu/article/18439 | A página oficial lida só traz o título "Taxa de comissão e taxa fixa por item", sem valores. R$4,50 desde 2026-10-01 e as demais faixas vêm só de vídeos de praticantes. |
| A22 | SEM FONTE OFICIAL | https://ads.shopee.com.br/ad-types/420 | Nenhuma página oficial lida traz as posições (2 primeiros, 1 a cada 3, 26 em 55, 7 em 30). Só o blog Magis5, sem data. |

## 11. Verificação pelo navegador (2026-10-15)

Lido no Chrome (as páginas carregam por JavaScript): Centro de Educação do Vendedor (seller.shopee.com.br/edu) e FAQ do Shopee Ads (ads.shopee.com.br/learn/faq). Sem login e sem captcha. Tabelas em imagem foram lidas por captura de tela.

| id | veredito | fonte oficial | observação |
|---|---|---|---|
| A3 | PARCIAL | https://ads.shopee.com.br/ad-types/1414 (s/d) | Confirma só a lista de elegíveis. A exclusividade para Lojas Oficiais não aparece na página. |
| A6 | PARCIAL | https://ads.shopee.com.br/learn/faq/473/1527; https://ads.shopee.com.br/learn/faq/473/2205 (s/d (migração em 07/05/2026)) | Confirmados: GMV Max com Lance Automático e Meta de ROAS, e as 3 sugestões de ROAS. O percentil de competitividade não aparece. O 1527 ainda fala em seleção automática de palavras-chave; o lance manual por palavra-chave não é tratado. |
| A7 | SEM FONTE OFICIAL | https://ads.shopee.com.br/learn/faq/323/1469 (s/d) | O artigo oficial Orçamento usa R$10 só como exemplo e não fala em mínimo. O mínimo de R$10 (antes R$6) segue só por praticantes. |
| A8 | CONFIRMADA | https://ads.shopee.com.br/learn/faq/339/1496; https://ads.shopee.com.br/learn/faq/340/1498 (s/d) | Créditos comprados antes, não reembolsáveis; valores sem desconto expiram em 6 meses. A Recarga Automática existe (artigo próprio, só o título foi lido). A recarga mínima de R$50 não foi verificada. |
| A11 | CONFIRMADA | https://ads.shopee.com.br/learn/faq/473/2205 (migração em 07/05/2026) | A atribuição por impressão (1 dia) vale só para GMV Max Anúncios de Produto, que passaram a cobrar por impressão (oCPM) em 07/05/2026. A de clique (7 dias) vale para todos. |
| A12 | SEM FONTE OFICIAL | https://ads.shopee.com.br/learn/faq/473/2205; https://ads.shopee.com.br/learn/faq/473/2198; https://ads.shopee.com.br/learn/faq/354/1509 (s/d) | O oficial diz que, na atribuição por clique, entram vendas de outros produtos da mesma loja em até 7 dias; não fala em vendas orgânicas. 'Vendas' (antigo GMV) exclui descontos desde jan/2026. Não há definição oficial de métricas 'diretas'. |
| A13 | SEM FONTE OFICIAL | https://ads.shopee.com.br/learn/faq/473/1527; https://ads.shopee.com.br/learn/faq/473/1951 (s/d) | Os dois artigos oficiais sobre Meta de ROAS não citam teto. O ROAS 30 segue só por praticante. |
| A25 | CONFIRMADA | https://seller.shopee.com.br/edu/article/18483 (01-03-2026 (atualizado em 01/10/2026)) | Tabela CNPJ: até R$79,99 = 20% + R$4,50. A comissão já inclui a taxa de transação. |
| A22 | PARCIAL | https://ads.shopee.com.br/ad-types/420 (s/d) | Confirma só que existem as vitrines Descobertas do Dia e Você Também Pode Gostar. As contagens (2 primeiros, 1 a cada 3, 26 de 55, 7 de 30) não aparecem em página oficial. |
