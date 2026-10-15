# Amazon Brasil: mapa de conhecimento da plataforma (CONSOLIDADO)

- **Data:** 2026-10-14. As notas das frentes são de 14 e 15/10/2026.
- **Escopo:** Amazon Brasil, com referências da Amazon global ou dos EUA quando a mecânica é a mesma (sempre marcadas).
- **Uso:** base para quem vai desenhar estratégia e agentes. A pesquisa é neutra: descreve como os melhores operam e não recomenda nada a nenhuma empresa.

**Como ler**
- **Tipos:**
  - [OFICIAL]: página da plataforma.
  - [OFICIAL via webinar]: regra falada por funcionário no canal "Venda com a Amazon Brasil", sem página escrita conferida.
  - [OFICIAL via terceiro]: regra oficial relatada por praticante ou blog.
  - [PRÁTICA]: tática de praticante.
  - [CASE]: números de uma operação.
  - [DADO]: estudo, relatório ou ferramenta.
  - [OBS]: observação direta.
- **Corte de 6 meses:** regra de plataforma anterior a 2026-04-14, ou sem data, leva "(pode estar superada)". Princípio e método valem sem corte.
- **Modelos:** [REVENDA] = revenda de marca alheia, genérico, importação. [MARCA] = indústria ou marca própria.
- **Vídeos:** `youtube.com/watch?v=<id>`. Os ids numéricos e os códigos do Instagram estão em `social/`.
- **Notas citadas** (pasta `pesquisa-marketplaces/amazon/`):
  - [ads] `ads/notas.md`
  - [preco] `preco-promocao/notas.md`
  - [log] `logistica-estoque/notas.md`
  - [rank] `ranqueamento-anuncio/notas.md`
  - [mix] `produto-mix/notas.md`
  - [rep] `reputacao-atendimento/notas.md`
  - [alim] `alimentos-marca-propria/notas.md`
  - [cases] `cases-grandes/notas.md`
  - [social] `social/notas.md`
  - [obs] `observacao/lideres.tsv`, coletado em 2026-10-14, sem CEP e sem hora. O `lideres.md` não existe.
- **Limites comuns a todas as frentes:**
  - A ajuda do Seller Central Brasil exige login e não foi lida.
  - A cota de busca na web acabou cedo; as páginas foram abertas por URL direta.
  - Pacvue, Perpetua, SmartScout e Nubimetrics ficaram de fora.
  - Muitas regras brasileiras só existem em webinar.

---

## 0. A plataforma em uma página

**Catálogo único.** Cada produto tem um ASIN, e vários vendedores ofertam no mesmo ASIN.
- Produto de marca com EAN entra no anúncio existente e disputa a oferta em destaque (Buy Box); não se cria anúncio novo ([OFICIAL via webinar] yutQ_7zR4Eo, 2026-10-02; nDtHI8fUEAA, 2026-08-20; [rank] §2.1).
- O conteúdo da página segue esta precedência: dono da marca registrada, depois o sistema, depois a maioria dos vendedores (nDtHI8fUEAA; 7ILvtU6GcPo, 2026-09-11; [rank] §2.2).
- A Amazon também é varejista (1P): compra da indústria e revende. Em café, os líderes observados são 1P ([OBS]; [cases] §1).

**O que decide quem vende: seis engrenagens**

1. **Buy Box.**
   - Fatores citados, sem pesos: preço (inclusive frente a outros marketplaces), prazo e custo de entrega, métricas da conta, região e logística da Amazon ([OFICIAL via webinar] nDtHI8fUEAA; [rank] §2.3; [rep] §2.2).
   - Desde 30/09/2026, no plano Mais Vantagens, conta o preço com Pix (H0ab_x1YIBY, 2026-10-14; [preco] §2.2).
   - O menor preço não vence sozinho: oferta 10% a 20% mais barata já ficou sem Buy Box ([PRÁTICA] GBnC2vqmRQo, 2026-08-27).
2. **Ads dependem da Buy Box e do estoque.**
   - Produtos Patrocinados exigem item qualificado para a oferta em destaque e com estoque ([OFICIAL] advertising.amazon.com/pt-br/solutions/products/sponsored-products, sem data, pode estar superada; [ads] R3; [rank] R2).
   - Sem Buy Box, o anúncio fica parado e não gasta.
   - Ads não fazem ganhar a Buy Box (q0-Y5gG6Q2w, 2026-09-15; [preco] §6).
3. **Logística subsidiada e amarrada a Ads.** No "Experimente FBA 3.0", a conta existente paga R$ 6 por unidade para produto a partir de R$ 79, com coleta e armazenagem zeradas, se gastar ao menos 3,5% da receita em anúncios ([OFICIAL] venda.amazon.com.br/termos/experimente-fba, de 01/07/2026 a 31/01/2027; [ads] §2.6; [log] §2.3).
4. **Ranqueamento sem fórmula pública.**
   - A Amazon cita relevância, preço, qualidade do anúncio, saúde da conta, Ads e vendas ([OFICIAL] sell.amazon.com/blog/amazon-seo, EUA, 2025-09-03, pode estar superada).
   - Praticantes convergem em que quem converte mais em menos tempo sobe ([PRÁTICA] 9Hlvkfh1Eow, VK7jalYzwxc, 78sSkRh2crI; [rank] A24). Nenhuma fonte tem teste causal.
5. **Prova social.**
   - A nota por estrelas sai de modelo de IA com peso de recência e de compra verificada.
   - Só avalia quem gastou R$ 50 em 12 meses ([OFICIAL] ajuda G8UYX7LALQC8V9KA, lida em 15/10/2026; [rep] §2.6).
   - Os líderes de café têm de 1,6 mil a 16,7 mil avaliações ([OBS]).
6. **Marca registrada abre ferramentas exclusivas:** Sponsored Brands (mínimo de 3 produtos), Display, Store, A+, Brand Analytics, Vine, kits virtuais e Programe e Poupe ([OFICIAL] venda.amazon.com.br/brand-registry e /publicidade, sem data, pode estar superada; [alim] §2.4).

**Para onde a plataforma empurra.**
- No 2º tri de 2026, a receita de Ads da Amazon cresceu 26% (US$ 19,8 bi), contra 16% dos serviços a vendedores 3P ([OFICIAL N2] release de 30/07/2026; [cases] §1).
- No Brasil, os incentivos de 2026 favorecem FBA e marca ([OFICIAL] /cresca/programa-de-recompensas-do-vendedor, sem data, pode estar superada; [cases] §2.2):
  - FBA a R$ 6;
  - comissão de 5% nas primeiras 100 unidades de item Prime novo;
  - crédito de até R$ 300 mil em comissão para dono de marca;
  - até R$ 5.300 em crédito de Ads.

**Prateleira de alimentos.** Em "café em grãos", 8 de 30 resultados eram patrocinados (posições 1 a 4 e 21 a 24), mais um banner ([OBS]; [ads] §5).
- Os patrocinados eram desafiantes com menos avaliações.
- Os líderes orgânicos eram 1P, com "Mais vendido" ou "Escolha da Amazon".

---

## 1. Regras e números que importam

Só entram itens confirmados em página oficial ou marcados como tal. O status segue as verificações (§10) das notas:
- **Confirmada:** lida em página escrita.
- **Webinar:** só falada.
- **Contestada:** página oficial diz outra coisa.

| Regra | Valor | Fonte e data | Status | Nota |
|---|---|---|---|---|
| Comissão "Comidas e bebidas" | 10%, mínimo R$ 1; faixa geral de 10% a 15%; bebida alcoólica 11%; saúde e suplementos 12% | venda.amazon.com.br/precos, de 20/01/2025 (pode estar superada) | Confirmada | [preco] A1; [alim] R1 |
| Comissão mínima | Texto diz R$ 1; tabela traz R$ 2 em parte das categorias | idem | Divergência interna | [cases] R3 |
| Plano Profissional | R$ 19/mês, grátis no 1º ano; página cita R$ 2 por item sem deixar claro se vale para ele | idem | Confirmada com ressalva | [mix] R2 |
| FBA, tabela padrão | Por peso e faixa de preço: de R$ 10,05 (0 a 100 g, abaixo de R$ 30) a R$ 51,35 (9 a 10 kg). Peso = maior entre real e cúbico (C×L×A÷6000) + 20 g | /precos; /cresca/fba, de 01/08/2025 (pode estar superada) | Confirmada | [log] §2.2 |
| FBA abaixo de R$ 30 (200 g a 1 kg) | R$ 10,95 a R$ 12,45 | /precos (pode estar superada) | Confirmada | [alim] R2 |
| FBA "fixa" abaixo de R$ 79 | R$ 5,65 / 5,85 / 6,50 no webinar; nos termos, só na linha de 1 a 1,5 kg | q0-Y5gG6Q2w, 2026-09-15 x termos | **Contestada** | [preco] A2; [log] A6 |
| Experimente FBA 3.0, conta existente | R$ 6/un. a partir de R$ 79; coleta e armazenagem R$ 0 em qualquer preço | /termos/experimente-fba, de 01/07/2026 a 31/01/2027 | Confirmada | [ads] R1; [log] A4 |
| Condição do R$ 6 | 3,5% da receita dos 30 dias anteriores em gasto efetivo de Ads. Contas de antes de 01/04/2026: ou +1 p.p. sobre abril/2026. Validação no dia 20 (última em 20/12/2026) | idem | Confirmada; base "elegível" x "total" ambígua | [ads] R1-R2; [log] A5 |
| Experimente FBA, conta nova | 30 dias sem logística, coleta e armazenagem | idem | Confirmada | [log] A4 |
| Comissão de lançamento Prime | 5% nas primeiras 100 un. (50 extragrandes), até 120 dias | /cresca/fba (sem data, pode estar superada) | Confirmada | [mix] R4 |
| Crédito de marca | Até R$ 300 mil, sobre comissão de 5% até R$ 6 mi em vendas | Recompensas (rodapé 2024; pode estar superada) | Confirmada | [cases] R8 |
| Crédito de Ads | Até R$ 5.300, ligado a gasto em Produtos Patrocinados | Recompensas (sem data) | Confirmada | [ads] R10 |
| Armazenagem FBA | R$ 75/m³/mês (até 10.000 cm³); R$ 37,50 (maiores); +R$ 525/m³ acima de 365 dias | /precos (pode estar superada) | Confirmada | [log] A1-A2 |
| Não apto e remoção | Remover em 30 dias ou descarte sem reembolso; remoção de R$ 0,99 a R$ 3,60/un. | /cresca/fba; /precos (sem data) | Confirmada | [log] A3 |
| Limites FBA | Produto: 22 kg, lado até 100 cm, soma até 200 cm. Caixa master: até 30 kg e 105×105×72 cm | /cresca/fba; /central-de-treinamento-fba (sem data) | Confirmada (contesta o "22 kg por caixa" dos webinars) | [log] A9; [mix] R6 |
| Entrada no FBA | CNPJ com NF-e, Simples ou Regime Normal (MEI aceito), IE em 12 UFs (SP, MG, PR, RJ, SC, RS, CE, DF, PE, BA, GO, ES) ou Programa de Filiais | /cresca/fba (sem data) | Confirmada | [log] A7 |
| DBA abaixo de R$ 79 | R$ 4,50 (abaixo de R$ 30), R$ 6,50 (R$ 30 a 49,99), R$ 6,75 (R$ 50 a 78,99) | /precos | Confirmada | [preco] A5 |
| DBA, metas | Envio tardio abaixo de 4% (risco de desativar ofertas); preparo padrão de 0 dia; isenção de até 72 h por atraso da transportadora | venda.amazon.com.br/cresca/dba, lida em 14-15/10/2026 | Confirmada | [rep] A1, A5; [log] A10 |
| Cancelamento antes do envio | Abaixo de 2,5% | PeBETM-rBxk, 2026-08-21 | Webinar | [rep] A2 |
| ODR | Abaixo de 1% em 60 dias (global); painel separa FBA (afn) e envio próprio (mfn) | SellerApp, 2026-09-28; SP-API, 2026-10-06 | Valor sem fonte oficial; campo confirmado | [rep] A3 |
| Garantia de A a Z | Até 90 dias após a última data de entrega; gatilhos de 48 h sem resposta, inclusive pedido de NF | ajuda GQ37ZCNECJKTFYQV (sem data) | Lida em 15/10; verificação deu 503 | [rep] A10 |
| Devolução | 30 dias na maioria; **7 dias para comestíveis**; 90 dias para durável com defeito | ajuda GKM69DUUYKQWKWX7 (sem data) | Lida em 15/10; verificação deu 503 | [rep] A14 |
| SLA de atendimento | Até 2 dias úteis | ajuda GLC8ZMBWMBTR6QZZ (sem data) | Lida em 15/10; verificação deu 503 | [rep] A13 |
| Solicitação de avaliação | Uma por pedido; proibido pedir seletivamente, pedir alteração ou dar recompensa | SP-API "solicit feedback", 2026-09-09 | Confirmada | [rep] A27 |
| Vine Brasil | Brand Registry, FBA, menos de 30 avaliações; R$ 0 (até 2 un.) / R$ 200 (3 a 10) / R$ 500 (11 a 30) por produto pai; só cobra após a 1ª avaliação; exclui pacotes | venda.amazon.com.br/vine, lida em 14-15/10/2026 | Confirmada | [rep] A29 |
| Brand Registry | Marca fixada no produto; registrada ou "em processo"; pedido pendente "em alguns casos" | /brand-registry (sem data) | Confirmada; "protocolo basta" é webinar | [alim] R6 |
| Sponsored Brands e Store | Exigem Brand Registry; SB pede 3 ou mais produtos; CPC ou vCPM | /publicidade; advertising pt-br (sem data) | Confirmada | [alim] R7 |
| Brand Analytics no BR | SQP, Search Catalog Performance, Market Basket e Repeat Purchase em 18 lojas, inclusive BR | developer-docs SP-API, 2026-10-06 | Confirmada | [mix] R8 |
| Temas de avaliação e devolução do Explorador (Customer Feedback API) | Não cobrem o Brasil | developer-docs, 2026-09-09 | Confirmada | [rep] A31 |
| Orçamento de Produtos Patrocinados | Diário; pode acabar em minutos; teto do mês = diário × dias do mês | advertising pt-br SP (sem data) | Confirmada (contesta o "× 30" do webinar) | [ads] R7 |
| Parcelamento sem juros | 1,5% a partir de R$ 40 | /precos | Confirmada | [rank] R3 |
| Mais Vantagens | 12x + Pix de 5% pago pela Amazon; taxa de 1,5% até 30/10 e 2,5% a partir de 31/10/2026; itens de R$ 40 a R$ 10 mil; Buy Box usa o preço com Pix | H0ab_x1YIBY, 2026-10-14 | Webinar | [preco] A6-A7 |
| Preço riscado | Mediana de 90 dias, sem vendas promocionais | K7a4jlTP9ME; q0-Y5gG6Q2w, set/2026 | Webinar | [preco] A8 |
| Promoções | Relâmpago de 4 a 12 h; Oferta da Semana de 7 dias; cupom de 5% a 80%, até 90 dias; quarentena de 14 dias | /promocoes (sem data; pode estar superada) | Página confirmada; webinars de 2026 divergem | [preco] A11-A12 |
| Frete grátis (FBA) | Abaixo de R$ 19, só Prime; de R$ 19 a 79, grátis em 3 dias ou mais; acima de R$ 79, em até 1 dia. /cresca/fba: não Prime a partir de R$ 129 | /termos/frete19 (15/08/2025; pode estar superada); /cresca/fba | **Contestada** entre páginas | [log] A12 |
| Project Zero BR | Entrada com 90% de denúncias aceitas em 6 meses; manutenção com 99% de precisão | /brand-registry/project-zero (sem data) | Confirmada | [alim] R11 |

**Só em webinar, mas tratados como certos pelos praticantes:**
- Aprendizado de Ads: 7 dias sem mexer, otimizar após 14, escalar após 30 ([ads] R8).
- Leilão de segundo preço + R$ 0,01 ([ads] R5).
- Estoque: cobertura de 5 semanas, IDI de 700 ou mais, promover aos 60 a 90 dias e remover acima de 90 ([log] A7-A8).
- SAFE-T: 45, 52 e 7 dias ([rep] A19).
- Validade visível e sem reembolso do vencido ([alim] R4).
- Título de 75 caracteres no BR ([rank] R1, via praticante).

---

## 2. Por frente: o que os melhores fazem

### 2.1 Ads ([ads])
- **Preparar a listagem antes de anunciar (consenso):** Buy Box, estoque, fotos, título, bullets, A+, preço na média e avaliações ([OFICIAL via webinar] QIF69cN-mrc, 2026-09-14; thiokBBRZhA, 2026-08-21; [PRÁTICA] VK7jalYzwxc, VH7Q5FddoRY; [ads] C1). Há quem use o Vine antes de escalar.
- **Automática para minerar, manual para controlar:**
  - os termos que convertem migram para exata ou frase, e a automática segue ativa (QIF69cN-mrc; nHdlguzjAik; 9Hlvkfh1Eow; [ads] C2);
  - a automática tem quatro grupos com lance próprio: aproximada, vaga, substitutos e complementos.
- **Negativação periódica** por exportação de termos, preferindo negativa exata ou de ASIN, após cerca de 14 dias ([ads] C3).
- **Ajustar o grupo ou o posicionamento que performa,** não a campanha inteira (thiokBBRZhA; [ads] C4).
- **Diagnóstico pelo funil, uma mudança por vez** ([PRÁTICA] 5WvOddb-A2k, 2026-07-28; TikTok 7678395422586539282, 2026-08-26; [ads] C5; [social] §1):
  - impressão sem clique: imagem, título, preço;
  - clique sem pedido: página, avaliações, preço;
  - orçamento que acaba cedo só aumenta se a campanha vende.
- **TACOS e margem pós-Ads como métrica de decisão** (9Hlvkfh1Eow; VK7jalYzwxc; 5WvOddb-A2k; [ads] C6). A Amazon confirma só que o ACOS deve ficar abaixo da margem e que não há ACOS "bom" universal ([OFICIAL] guia de ACOS pt-br, sem data).
- **Meta por fase** ([PRÁTICA] 9Hlvkfh1Eow; [ads] §3.2; confiança C):
  - lançamento aceita ACOS até o equilíbrio ou acima;
  - genérico vai até a margem de contribuição;
  - revenda com Buy Box compartilhada mantém o gasto baixo, porque o anúncio favorece todos os vendedores do ASIN;
  - manutenção fica bem abaixo da margem.
- **Eventos:** aquecer antes e reservar verba para o pico (VH7Q5FddoRY; q0-Y5gG6Q2w; [ads] C7). Nos EUA, 83% do gasto da janela do Prime Big Deal Days saiu antes do evento ([DADO] Skai, 2026-10-13).
- **Defesa de marca quase universal:** 96% das marcas compram SP no próprio nome; nos genéricos da categoria, a presença é de 36% ([DADO] Jungle Scout/PODEAN, 3.500 marcas, 6 países com o BR, 2026-10-12; [ads] A18).
- **O desafiante compra o topo e a página do rival:** em café, marcas com menos avaliações ocupam os patrocinados e compram banner na página dos líderes ([OBS]; [ads] A20-A21).
- **Incrementalidade:**
  - nenhum teste de pausa ou holdout no Brasil; o substituto usado é a tendência do TACOS, que é atribuição e não causalidade ([ads] §3.5);
  - a Amazon sugere comparar, no painel da Store, a venda vinda de Sponsored Brands com a orgânica (7ILvtU6GcPo; [alim] §3).

### 2.2 Preço e promoção ([preco])
- **Promover pelas ferramentas, não pelo inventário** (três falas da Amazon: K7a4jlTP9ME, 2026-09-04; q0-Y5gG6Q2w; VH7Q5FddoRY; [preco] §3.3). Baixar o preço "na mão" não gera selo e rebaixa a referência de 90 dias.
- **Calibrar produto novo:** desconto no preço mais Ads. Em 1 a 2 meses, o ASIN recebe sugestão de oferta especial; a Amazon sugere começar em julho para o pico de out-dez (K7a4jlTP9ME; [preco] §3.4).
- **Ofertas especiais são por convite.** No cofinanciamento, a Amazon sugere o preço e reduz a comissão (ex.: de 12% para 10%) (q0-Y5gG6Q2w; [preco] A13, só webinar).
- **Cupom não muda o preço da vitrine nem pesa na Buy Box** ([OFICIAL via webinar] u34wosZEh1g, 2026-10-14; [preco] A12).
- **Oferta + Ads + FBA como roda:** o Ads no produto em oferta também conta para os 3,5% (K7a4jlTP9ME; [preco] §3.4).
- **Preço por canal** sai da margem de contribuição de cada canal: preço = custo ÷ (1 − taxas% − margem%) ([PRÁTICA, método] cZysnqICrkY, 2026-05-14; [preco] §3.1).
- **Escada de margem:** Ads em cerca de 10% da receita (5% a 6% estável, 12% a 13% em tração); piso de margem de contribuição de 10% na revenda e 15% no importador ([PRÁTICA] kML9xEpimsw, 2026-09-23).
- **[REVENDA] contra guerra de preço:** reprecificador com piso e teto (a Amazon tem um gratuito, blog oficial, 16/09/2026), oferta FBA e DBA no mesmo ASIN, kits e Buy Box medida todo dia (GBnC2vqmRQo, com conflito de interesse; 02Bn3HyAYqk; [preco] §3.3).
- **Calendário 2026** ([OFICIAL] aboutamazon.com.br, 02/10/2026; blog, 16/09/2026; [preco] A16-A17):
  - datas duplas mensais;
  - Mega Oferta Prime de 5 a 11/10, com cafés em "Mercado" com até 50%;
  - Semana do bem-estar a partir de 19/10;
  - Black Friday de 3/11 a 30/11.
- **Pico** ([OFICIAL] blog sazonal; q0-Y5gG6Q2w; VH7Q5FddoRY):
  - estoque no FBA 2 semanas antes ou mais;
  - Ads cerca de 14 dias antes;
  - volume de 3 a 10 vezes o normal, com 15% a 20% de segurança;
  - voltar ao preço cheio antes de zerar o estoque.

### 2.3 Logística e estoque ([log])
- **FBA para a curva A; DBA ou envio próprio para a cauda** (crnP1JO2B1o, 2026-09-04; VH7Q5FddoRY; TikTok 7664720778054602005; [log] P1).
- **Oferta dupla no mesmo ASIN** (SKU FBA + SKU DBA): quando o FBA zera, a outra assume ([PRÁTICA] 02Bn3HyAYqk; [log] P2). A Amazon recomenda duplicar a oferta, não converter (zdDPzE7jftg, 2026-08-20).
- **Reposição por cobertura** ([log] P3; [cases] §4):
  - Amazon: 5 semanas (k0v5Yw5h5NQ, 2026-09-11);
  - revenda BR: 30 a 45 dias (78sSkRh2crI);
  - marca importada nos EUA: 90 a 120 dias (nLM_JFURSTI).
- **Higiene mensal:** zerar "sem oferta ativa", remover o não apto antes de 30 dias, liquidar aos 60 a 90 dias e remover acima de 90. Tudo isso pesa no IDI, que define a capacidade em m³ (k0v5Yw5h5NQ; [log] P6).
- **Pico:** enviar de 15 a 30 dias antes. O recebimento leva de 3 a 7 dias, ou de 2 a 3 semanas na sazonalidade (zdDPzE7jftg; [log] P4).
- **Não zerar no pós-pico:** a ruptura desperdiça o ranqueamento conquistado (VvcswcsjuUw, 2026-09-24, opinião; [log] P5).
- **Profundidade conta:** lote raso não é redistribuído entre CDs. A entrega em horas (SP e RJ) exige cerca de 4 semanas de cobertura e Buy Box (gZ4fDdLtwBo, 2026-10-07; [log] A14, A20).
- **Excesso de estoque é o erro que mais mata operação grande** ([PRÁTICA] nLM_JFURSTI, EUA; [cases] §6):
  - giro de 4 a 6 vezes por ano;
  - teto de 12 meses;
  - corte do SKU que não vende o lote em 12 meses.

### 2.4 Ranqueamento e anúncio ([rank])
- **A primeira foto e o título decidem o clique; página, preço e avaliações decidem a conversão** (ekW57cfZ8dc; VK7jalYzwxc; 06XpeVMN7ek; [rank] §3.1).
- **Título com marca, atributo e uso,** sem sensacionalismo (yutQ_7zR4Eo; VH7Q5FddoRY). Um líder do top 20 de café usa atributos separados por "│" e não tem A+ ([OBS]; [social]).
- **Imagens:** até 9, principal com fundo branco; selo promocional na foto pode suprimir o item ([OFICIAL via webinar] O_kXw3vvD8s, 2026-10-13). A página dos EUA só recomenda fundo simples ([rank] R9).
- **Variações agrupadas** (sabor, tamanho, quantidade): o SKU pai não tem estoque e não há limite de variações (O_kXw3vvD8s; [mix] §2.2). O líder de café agrupa sabor e tamanho ([OBS]).
- **Palavra-chave:** com marca, Brand Analytics/SQP (volume, impressão, clique, carrinho e compra por termo) ([OFICIAL] developer-docs; [mix] §2.1). Sem marca, o relatório de termos da campanha automática ([rank] §3.2).
- **Avaliações dentro da regra:** Vine, solicitação uniforme e picos de venda, limitando a quantidade por cliente em desconto agressivo (K7a4jlTP9ME; VH7Q5FddoRY; [rank] §3.3).
- **Teste A/B oficial** com Brand Registry, 8 a 10 semanas recomendadas ([OFICIAL] sell.amazon.com/tools/manage-your-experiments, EUA, sem data; [rank] R12). Não está confirmado no BR, e ninguém no BR o cita.
- **IA de compras como prateleira nova:** nos EUA, 63,9% das recomendações ficaram fora do top 10 orgânico ([DADO] Marketplace Pulse, 2026-07-16, uma conta; confiança C).

### 2.5 Produto e mix ([mix])
- **Teto da categoria em três camadas que não se somam:** dado da Amazon (Explorador, Brand Analytics), estimativa de ferramenta e conta de prateleira ([mix] §3.1).
  - O selo "mais de X compras" é piso em degraus: preço × selo dá limite inferior ([mix] A21).
  - As ferramentas admitem erro acima de 20% por marca ([DADO] SmartScout, s/d).
- **Critérios de entrada** ([PRÁTICA] 1fXOj1mcRuU, dJLRqoodacM, TkQHhJ8DyRc, vZjq7xV4DB0, vários N7; [mix] §3.2):
  - demanda provada e margem conferida na calculadora;
  - maturidade dos líderes;
  - fuga da Buy Box com a Amazon 1P;
  - preço acima de R$ 50 a 80 e caber no FBA;
  - tendência de busca e devolução do nicho.
- **A tarifa cria faixas de preço:** degraus do DBA em R$ 30, R$ 50 e R$ 79 e régua de R$ 79 do FBA ([OFICIAL] /precos; termos; [mix] §3.4).
- **Catálogo inteiro primeiro, corte depois:** a curva A de outro canal nem sempre se repete (VH7Q5FddoRY; [mix] A18). A recomendação de reposição só aparece após cerca de 3 meses (VvcswcsjuUw; [mix] A17).
- **Variação de tamanho e pack como motor:** uma fita virou cerca de 500 SKUs ([PRÁTICA] tpS__DSMMqo, EUA, autodeclarado). Bundling de item procurado com item lento sobe o ticket ([OFICIAL] blog, 2026-09-16).
- **Racionalizar pelo financeiro:** margem por SKU, giro, dependência, devolução e preço de recompra (SqoNj2DDRSU; 4Vvrft5eTDo; [mix] A31).
- **Expandir com Market Basket e Repeat Purchase** (oficiais no BR para marca; [mix] A1-A3). Nenhum praticante brasileiro mostrou esses relatórios.
- **Lançar vários produtos:** "lance quatro" (tpS__DSMMqo); acerto perto de 60% com pedidos iniciais pequenos (nLM_JFURSTI; [cases] §3.2).

### 2.6 Reputação e atendimento ([rep])
- **Saúde da conta como pré-requisito de evento:** responder perguntas e devoluções, medir a Buy Box todo dia e investigar perdas (VH7Q5FddoRY; nDtHI8fUEAA; [rep] §3.1).
- **FBA tira atendimento, devolução e envio tardio da operação.** As métricas de envio só valem para o envio próprio, e o ODR é separado (developer-docs; [rep] §3.3).
- **Configurar capacidade diária, feriados e horário de corte** para proteger o envio tardio (lBnzH7KSh4E, 2026-08-20).
- **Pedir avaliação de forma uniforme** (botão ou API). Excluir quem deu feedback negativo, como uma praticante faz, conflita com a proibição de pedir seletivamente (SP-API x [PRÁTICA] AuWtJJ_708Q; [rep] §6).
- **Avaliação de produto não é feedback do vendedor:** embalagem, avaria e prazo não cabem na avaliação do produto e podem ser denunciados ([OFICIAL] ajuda GLHXEX85MENUE4XF; [rep] §2.6).
- **Embalar para o pior trajeto:** embalagem inadequada anula o SAFE-T, que só reembolsa o preço do item (cya4LLoRX7A, 2026-07-28; [rep] A21).
- **Devolução em duas camadas** (painel e o que chega de fato) (SqoNj2DDRSU). No BR, o diagnóstico usa `return_reason_code`, porque os temas do Explorador não existem aqui ([rep] A31-A32).
- **NF coerente com o CNPJ:** reclamação de autenticidade exige nota (d4EH8e36Z7g; [rep] §3.1). Pesa mais em [REVENDA].
- **"Vem de Amazon" (SP) como termômetro trimestral:** Logística vale até 40 de 100 pontos; o DBA chega no máximo a 4 estrelas ([OFICIAL] /programas/vem-de-amazon; [rep] A33).

### 2.7 Alimentos e marca própria ([alim])
- **Registrar a marca cedo** e usar o pedido pendente para destravar ferramentas (7ILvtU6GcPo; p3_Iq6ETtdk, 2026-08-30; [alim] §3). A página só aceita o pedido pendente "em alguns casos".
- **Brand Store em abas por linha de produto,** com Sponsored Brands levando à aba certa. O exemplo oficial é de café: cápsula, máquina e kits (7ILvtU6GcPo).
- **Assinatura como ativo:**
  - testar o desconto e medir por coorte; a Amazon EUA sugere 5% e depois 10% ([OFICIAL EUA] blog S&S, 25/08/2025, pode estar superada);
  - não empilhar oferta, assinatura e cupom: um item de US$ 18 caiu para cerca de US$ 9 (UJDdmCK8zMY; [alim] §3).
- **Etiqueta fora da validade e controle da idade do estoque,** porque o vencido não é reembolsado (zdDPzE7jftg; k0v5Yw5h5NQ).
- **Kits exclusivos:** kit virtual, ou kit físico com isenção de GTIN pedida grátis pelo Listing Hub, gera ASIN que o revendedor do avulso não disputa (nDtHI8fUEAA; [alim] §5.6).

### 2.8 Cases ([cases]; [social] §8)
- **Nenhum case brasileiro tem número auditável.** Os de mentoria são peças de venda. As 21 histórias oficiais não trazem métricas ([OFICIAL] venda.amazon.com.br/historias).
- **EUA, autodeclarados (C):**
  - Ângelo Mário: mais de US$ 1 mi/mês, cerca de 500 SKUs, 15 funcionários remotos e rotina fixa por dia da semana (tpS__DSMMqo, 2026-07-23).
  - Josh Hadley: mais de US$ 20 mi/ano, com planejamento de compra como função-chave (nLM_JFURSTI, 2026-07-29).
- **Padrões dos grandes:** time enxuto, ferramenta própria, marca própria como destino, Ads como acelerador e FBA como padrão ([cases] §3.2). Há viés de sobrevivente.
- **Erros documentados** ([cases] §6):
  - defeito de lote que derrubou a nota de 4,8 para 4,2;
  - antidumping com US$ 50 mil presos;
  - contestações em 5% a 10% das vendas DBA, que levaram um vendedor a sair (L380mHir7aA, 2026-09-04).
- **Topo estável nos EUA:** 68,6% dos top 10 mil já estavam lá 12 meses antes ([DADO] Marketplace Pulse, 2026-07-09).

---

## 3. Benchmarks de referência

Não há benchmark público com método por categoria para a Amazon Brasil. Número dos EUA vale só como ordem de grandeza.

| Métrica | Faixa | Fonte e tipo | Nota |
|---|---|---|---|
| ACOS / ROAS de equilíbrio | ACOS = margem de contribuição antes de Ads; ROAS = 1 ÷ essa margem | Método; princípio [OFICIAL] guia de ACOS | [ads] §3.2 |
| ROAS "bom" (BR) | 5 a 6 ou mais com margem de 30%; tela madura: ACOS 12%, ROAS 8,31, TACOS 8% | [PRÁTICA] 5WvOddb-A2k, 2026-07-28 (embaixadora com contrato com a Amazon) | [ads] A25 |
| ROAS médio (EUA) | 2:1; marcas miram 3 a 4 | [OFICIAL global] guia de ROAS (sem data) | [ads] §4 |
| Ads como % da receita | Piso de 3,5% para o FBA a R$ 6; praticante usa cerca de 10% (5% a 13%) | Termos; [PRÁTICA] kML9xEpimsw | [preco] A24 |
| Gasto de lançamento [MARCA] | 2x a 3x o lucro unitário; R$ 10 mil a 15 mil até o lucro no 3º ou 4º mês | [PRÁTICA] 9Hlvkfh1Eow (sem base) | [ads] §3.2 |
| CTR "saudável" (BR) | 0,20% a mais de 1% | Dois webinars oficiais divergentes; VK7jalYzwxc | [ads] §3.3 |
| CTR e CPC (EUA) | CTR em evento de 0,41%; CPC de cerca de US$ 1,00 (US$ 1,46 no Prime Big Deal Days) | [DADO] Skai, 2026 | [ads] §4 |
| Lance (BR) | Partida de R$ 0,40 a 1,20; madura, R$ 0,35 | [PRÁTICA] nHdlguzjAik (N7); 5WvOddb-A2k | [ads] §4 |
| Conversão de Ads | 10% a 20% (teto prático de 25%) | [PRÁTICA] VK7jalYzwxc (N7) | [ads] §4 |
| Conversão da página | 4% a 5% | [PRÁTICA] 9Hlvkfh1Eow (N7, sem base) | Só hipótese |
| Avaliações por venda | Cerca de 1% (BR, sem base) a 4% a 20% (EUA, 2020) | [PRÁTICA] AuWtJJ_708Q; [DADO] Helium 10, 2021 | [rep] §3.2 |
| Avaliações dos líderes de café | 1.647 a 16.737; nota de 4,5 a 4,8 | [OBS] | [rep] §4 |
| Margem | Bruta: private label 40% a 60%, atacado 20% a 40% (estimativa Amazon EUA). Revenda BR: cerca de 8% líquida (N7). Importação: margem de contribuição acima de 25% (N7) | [DADO] sell.amazon.com/blog, 2026-07-27; CpeAKSyctRg; rN4j4kZvkDg | [alim] §4; [mix] §4 |
| Piso de margem de contribuição | 10% revenda; 15% importador | [PRÁTICA] kML9xEpimsw | [preco] A24 |
| Tarifas no ticket baixo | Item de R$ 28 e 270 g: comissão + FBA = 49% do preço pela tabela por peso; 26% no DBA. Com a tarifa fixa do webinar, o FBA dá de 17% a 20% | Cálculo sobre /precos (pode estar superada) | [alim] §5.7; [preco] §5 |
| Cobertura de estoque | 5 semanas (Amazon); 30 a 60 dias (consenso); 90 a 120 dias (marca importada EUA) | k0v5Yw5h5NQ; 78sSkRh2crI; nLM_JFURSTI | [log] P3 |
| Idade do estoque | Promover aos 60 a 90 dias; remover acima de 90; longo prazo cobrado acima de 365 | Webinar; /precos | [log] §4 |
| IDI | 700 ou mais (BR, webinar); IPI nos EUA de 0 a 1.000 com limite de 400 | k0v5Yw5h5NQ; Jungle Scout, 2023 | [log] A10 |
| Giro e teto | Giro de 4 a 6/ano (exterior) ou 10 a 20 (local); teto de 12 meses | [PRÁTICA] nLM_JFURSTI | [cases] §4 |
| Pico | 3 a 10 vezes a venda diária; segurança de 15% a 20%; envio de 2 a 4 semanas antes | [OFICIAL] blog; q0-Y5gG6Q2w | [preco] §4 |
| Saúde da conta | Envio tardio abaixo de 4% (BR); cancelamento abaixo de 2,5% (webinar); ODR abaixo de 1% (global); entrega no prazo acima de 97% (global, C) | /cresca/dba; PeBETM-rBxk; SellerApp | [rep] §4 |
| Patrocinados e defesa de marca | 8 de 30 em "café em grãos"; 96% das marcas no próprio nome | [OBS]; [DADO] Jungle Scout | [ads] A18, A20 |
| Assinatura | S&S acima de 20% da receita em marcas dos EUA (depoimentos); assinante com 2 a 3 vezes mais compras (sem método) | sell.amazon.com S&S; UJDdmCK8zMY | [alim] §4 |
| Efeito do FBA | "4x" (página) a "20% a 25%" (webinar), sem método | /cresca/fba; gVHIZsn3dbA | [rep] §3.2 |

---

## 4. Divergências entre fontes e como resolver na prática

| Tema | Versão A | Versão B | Como resolver (o que medir) |
|---|---|---|---|
| FBA abaixo de R$ 79 | Fixa sem peso, R$ 5,65 / 5,85 / 6,50 (webinar, 15/09/2026) | Tabela por peso desde R$ 10,05 (/precos); termos com o fixo só em 1 a 1,5 kg | Simular o ASIN na Calculadora de Receitas e conferir o débito no extrato do 1º envio. É a divergência que mais muda a conta do ticket baixo ([preco] A2; [log] A6) |
| Alternativa e base do 3,5% | +1 p.p. sobre abril (termos); receita "elegível" | "Maio" (VvcswcsjuUw); "+1% de crescimento"; receita "total" | Prevalece o termo escrito. Calcular gasto efetivo ÷ receita pelas duas bases nos 30 dias que fecham no dia 20 e usar a mais exigente ([ads] R2; [log] A5) |
| Frete grátis ao não Prime | R$ 19 a 79 com 3 dias ou mais (/termos/frete19) | R$ 129 (/cresca/fba); R$ 149 (fba-onsite); R$ 79 (praticante) | Ver a página deslogado ou com conta não Prime, em vários CEPs ([log] A12) |
| Caixa master | 22 kg e 100 cm (webinars) | 30 kg e 105×105×72 cm (página) | 22 kg e 100 cm valem para o produto; conferir no fluxo de envio ([log] A9) |
| Regras de promoção | Relâmpago de cerca de 24 h; cupom de 5% a 50% por 30 dias (webinars 2026) | 4 a 12 h; 5% a 80% por 90 dias (/promocoes, sem data) | Vale o que o Seller Central mostra ao criar a promoção; registrar a tela ([preco] A11-A12) |
| Preço riscado | Mediana de 90 dias (duas sessões oficiais) | Média de 6 meses (gerente em evento) | Comparar o preço "De" exibido com o histórico próprio ([preco] §3.5) |
| Título no BR | 75 caracteres desde 27/07/2026 (via praticante) | 200, com recomendação de até 60 (EUA, 2025) | Testar a publicação acima de 75. Até lá, faixa de 60 a 75 ([rank] §3.5) |
| Teto do orçamento | Diário × 30 (webinar) | Diário × dias do mês (página) | Prevalece a página; conferir na fatura ([ads] R7) |
| Quando otimizar Ads | 14 dias, "inegociável" (oficial) | 3 dias (nHdlguzjAik); 10 dias (ekW57cfZ8dc) | Comparar o CPA da semana 1 com o das semanas 3 e 4 sem mudanças |
| Lance inicial | Sugerido (webinar) | Mínimo e subir (praticantes) | Campanhas gêmeas por 14 dias |
| CTR saudável | 0,20% | Mais de 1% | Medir por posicionamento antes de comparar |
| +270% de conversão com 5 avaliações | OFICIAL dos EUA ([rank] A28) | Blog sem fonte, texto feito com IA ([rep] §6) | Não usar; medir a conversão própria por marco de avaliações |
| Vine e Brand Analytics no BR | "Não confirmados" ([rank]; [alim]) | Confirmados em /vine e na SP-API ([rep] A29; [mix] R8) | Resolvido: existem no BR |
| Brand Registry com protocolo | Basta; só não denuncia (webinar) | "Em alguns casos"; a página não restringe a denúncia | Ver no cadastro o que o sistema aceita ([alim] R6) |
| Efeito do FBA; fatia Prime | "4x"; mais de 80% | "20% a 25%"; "mais de 50%" | Números da Amazon sem método. Medir a conversão antes e depois do FBA com o mesmo preço |
| Paridade de preço entre canais | Manter preço parecido (gerente de contas) | Preço por margem de cada canal (praticantes) | Não há regra oficial lida. Acompanhar perda de Buy Box quando o preço externo cai ([preco] §9) |
| Genérico e Buy Box | "Não disputa" (praticante) | 53 ofertas num ASIN genérico ([OBS]) | Contar as ofertas antes de assumir exclusividade ([mix] §3.2) |
| Solicitação seletiva de avaliação | Excluir quem deu feedback negativo (praticante) | Proibido pedir seletivamente (SP-API) | A fonte forte vale ([rep] §3.2) |
| Mais estoque melhora o ranking | Praticantes ([cases] §6) | Sem teste; longo prazo a R$ 525/m³ | Medir a posição por termo com cobertura alta e baixa |

**Medir de forma contínua, porque nenhuma fonte responde:**
- incrementalidade de Ads (pausa ou holdout por ASIN ou região);
- tempo de recuperação da posição após ruptura;
- taxa de avaliação por venda;
- percentual de Buy Box diário (Relatório Comercial; [social] A37);
- preço contra a mediana da 1ª página por termo.

---

## 5. Indústria/marca própria x revenda: onde a plataforma favorece cada um

**Favorece [MARCA]**
- **Controle do conteúdo:** só o dono edita o ASIN; o revendedor que grafou errado a marca pode ser denunciado (nDtHI8fUEAA; 7ILvtU6GcPo; [rank] §2.2).
- **Ferramentas exclusivas** ([OFICIAL] /brand-registry; /publicidade; developer-docs; [ads] §7; [alim] §5.5):
  - Sponsored Brands (também por vCPM, com meta de parcela no topo) e Display com remarketing;
  - Store gratuita, com tráfego orgânico contra pago, e A+;
  - Brand Analytics, Vine, kits virtuais, Programe e Poupe e Project Zero.
- **Dinheiro dirigido:** crédito de até R$ 300 mil em comissão ([cases] R8, pode estar superada).
- **Números da Amazon (direção, sem método nem holdout):** SB com 79% de vendas a clientes novos; A+ com até 8% ou 20%; Store com 53,9% mais frequência; S&S com até 1,8x de conversão ([OFICIAL] /brand-registry; 7ILvtU6GcPo; [alim] §1).
- **Lógica de gasto:** o investimento de lançamento pode passar da margem, com retorno esperado no orgânico e na recompra ([PRÁTICA] 9Hlvkfh1Eow, C).
- **Custos:**
  - ASIN novo sem histórico não recebe oferta sugerida nem mostra preço riscado (K7a4jlTP9ME; [rank] §7);
  - aporte citado de R$ 10 mil a 15 mil por SKU nacional e R$ 50 mil ou mais por importado ([PRÁTICA N7] CpeAKSyctRg).
- **Equity:** a conta se vende a 3 a 4 vezes o lucro anual nos EUA, com o estoque pago à parte (tpS__DSMMqo; Vl6KK7-lEz0; [cases] §7).
- **Risco 1P:** a Amazon pode ser cliente (Vendor) e concorrente no mesmo ASIN. Em café, é o modelo dominante ([OBS]). Não há fonte sobre os termos do 1P no Brasil.

**Favorece [REVENDA]**
- **ASIN existente herda o histórico:** vende no 1º dia e recebe oferta sugerida mais cedo (K7a4jlTP9ME; [preco] §7).
- **O jogo é a Buy Box:** preço (inclusive Pix), FBA, métricas e região; reprecificador, oferta dupla e monitoramento diário ([preco] §3.3; [rank] §7).
- **Ser o primeiro FBA do ASIN** dá selo Prime e vantagem de entrega (VvcswcsjuUw; [log] §3.2).
- **Limites:**
  - Ads em Buy Box compartilhada beneficiam todos os vendedores do ASIN;
  - margem de cerca de 8% (N7);
  - autorização de marca temporária, com NF;
  - mais risco de bloqueio por autenticidade;
  - sem Sponsored Brands, Store, A+, Vine ou S&S ([rep] §7; [alim] §7).
- **Genérico importado:** ASIN próprio, mas sem ferramentas de marca e sem garantia de exclusividade ([mix] §3.2).
- **Tributário:** a reforma de 2027 a 2032 tende a fechar a vantagem de quem compra com nota parcial ([PRÁTICA] 6jtpl-y_iZw, 2026-08-12; [preco] §7).

**Vale para os dois:** tarifas, FBA a R$ 6 com 3,5% de Ads, saúde da conta, A a Z, SAFE-T, calendário, envio antecipado e promoção pelas ferramentas ([preco] §7; [log] §7; [rep] §7).

---

## 6. Alimentos e café: regras e oportunidades específicas

**Regras**
- **Comissão:** 10% em "Comidas e bebidas", sem degrau por preço; é a menor da tabela (nos EUA, 8% ou 15%) ([OFICIAL] /precos, 20/01/2025, pode estar superada; [preco] §5).
- **Ticket baixo é dominado pela logística:**
  - pela tabela escrita, 250 g a 1 kg abaixo de R$ 30 pagam de R$ 10,95 a R$ 12,45 de FBA, contra R$ 4,50 no DBA ([alim] §5.7);
  - parcelamento e planos Vantagens só a partir de R$ 40;
  - a partir de R$ 79, o FBA a R$ 6 com Ads favorece 1 kg, kits e packs (leitura de regra; [preco] §5; [cases] §5).
- **Validade** ([OFICIAL via webinar] zdDPzE7jftg; VvcswcsjuUw; -7TGtIYZX0U; k0v5Yw5h5NQ; [alim] §2.2; [log] §5):
  - a etiqueta não pode cobrir a data, e já houve lote removido por isso;
  - o recebimento confere a validade;
  - vencido não é reembolsado;
  - não apto é descartado em 30 dias ([OFICIAL] /cresca/fba).
- **Armazenagem sanitária:** no GRU9, as ruas seguem a classificação da vigilância sanitária (-7TGtIYZX0U).
- **Preparação:** categoria "alimento" no envio; fita em tampa de rosca; kit montado em saco, com uma etiqueta e o NCM do item de maior valor (crnP1JO2B1o; VvcswcsjuUw).
- **Devolução de comestíveis em 7 dias,** coincidindo com o arrependimento do CDC, em que o vendedor paga o frete de volta ([OFICIAL] ajudas GKM69DUUYKQWKWX7 e GFLBEJCLHMVFEPA8; [rep] §5).
- **Entrega no mesmo dia:** mercearia só tem frete grátis a partir de R$ 79, contra R$ 19 nas demais (gZ4fDdLtwBo).
- **Categoria regulada:** suplemento pede Anvisa, tabela nutricional e NF no cadastro (nDtHI8fUEAA). Não se sabe se "Comidas e bebidas" inteira exige aprovação. Categoria fechada fica fora de Ads e de promoções ([OFICIAL] /publicidade; /promocoes, sem data).
- **Vine** aceita alimento, mas exclui pacotes, o que atinge kits ([OFICIAL] /vine).
- **Programe e Poupe:** no BR, é benefício de marca (10% a 15%). A mecânica só foi lida nos EUA: vendedor banca 0/5/10%, Amazon soma 5% a partir de 5 itens, exige estoque disponível acima de 90% ([alim] §2.6).
- **Regras sanitárias externas** (via nota do ML, não relidas aqui; [alim] §2.3):
  - RDC 843/2024 e IN 281/2024, com transição até 01/09/2026;
  - rotulagem do café pela Portaria SDA/MAPA 570/2022 (grupo, espécie, torra);
  - fiscalização da Anvisa no Full do ML em 18/03/2026; não há registro equivalente na Amazon.

**Prateleira de café** ([OBS]; [alim] §5; [social] Observação; [cases] §5)
- **Líderes 1P:** Orfeu Grãos 1 kg é o 1º em Café e o 6º em Alimentos e Bebidas, com 16.737 avaliações, nota 4,7, mais de 10 mil compras no mês, vídeo e A+. Coffee Mais e Baggio também são 1P. Cada um tem cerca de 5 outras ofertas no ASIN.
- **Formatos:** 1 kg e 250 g; cápsulas em caixa de 10 ocupam cerca de 12 das 30 posições do top; packs de 2, 4 e 12 no top de Alimentos.
- **Preço por kg:** de R$ 66 a 150 na busca; líderes 1P entre R$ 113 e R$ 136; o desafiante 3P em cerca de R$ 70.
- **Alavancas:**
  - Líderes: variações num ASIN, A+, selos, cupom de app e desconto visível. Um item chega ao top 20 sem A+.
  - Desafiante 3P com FBA: topo patrocinado, banner na página do líder, Programe e Poupe e entrega "amanhã".
- **Evento:** cafés com até 50% na Mega Oferta Prime 2026 ([OFICIAL] aboutamazon.com.br, 02/10/2026).

**Oportunidades criadas pela mecânica (leitura de regra, não recomendação)**
- **Kits e packs acima de R$ 79:** FBA a R$ 6, frete de mercearia e o 5% extra do S&S (EUA). Limite: exclusão de pacotes no Vine.
- **Assinatura em consumível:** exige estoque contínuo, por isso casa com FBA.
- **Barreira sanitária:** filtra revendedores; praticantes evitam alimentos por isso ([PRÁTICA N7] vZjq7xV4DB0; [mix] §5).
- **Topo pago:** a busca de café já é disputada em mídia, e o orgânico do topo é de quem tem milhares de avaliações.

**Lacunas** ([log] §9; [alim] §9): vida útil mínima no recebimento, retirada antes do vencimento, temperatura, lista de proibidos, aprovação de categoria, recompra no BR, ACOS de alimentos e termos do 1P.

---

## 7. Perguntas abertas para a fase de estratégia

1. Qual é a tarifa FBA real abaixo de R$ 79 por peso de embalagem: a tabela por peso ou o fixo da campanha? Sem isso, a conta do ticket baixo fica aberta.
2. O 3,5% conta sobre receita elegível ou total? O que vale depois de 31/01/2027?
3. "Comidas e bebidas" exige aprovação no BR? Quais são a vida útil mínima no recebimento, a retirada antes do vencimento e a regra de calor? (Exige ajuda logada.)
4. Quais são os termos do 1P (Vendor) para a indústria no Brasil? Como o 3P de marca convive com o 1P no mesmo ASIN?
5. Que desenho de teste (pausa por ASIN, região ou período) mede a incrementalidade de Ads em alimentos?
6. Entre os desafiantes de café, quanto do gasto vai para a própria marca, para genéricos e para a página do concorrente?
7. Quais são o ACOS, o CTR e a conversão normais em café na Amazon BR? Só medição própria responde.
8. Programe e Poupe no BR: níveis, quem banca, elegibilidade, painel e retenção típica em café?
9. O título está limitado a 75 caracteres no BR? Qual é o limite do campo de palavras de backend?
10. Experimentos A/B e o Explorador completo estão ativos no Brasil?
11. Quanto tempo a posição leva para voltar após ruptura? Qual cobertura protege a posição sem estourar a validade?
12. Há cobrança de paridade de preço com outros canais?
13. Que formato vence na prateleira (1 kg, 250 g, cápsula, kit, assinatura) e com que peso de avaliações, selo, A+ e preço por kg?
14. Como o preço Pix do Mais Vantagens (2,5% a partir de 31/10/2026) muda a Buy Box entre R$ 40 e R$ 80?
15. A Portaria INPI 66/2026 está vigente? Qual é a classe NCL do café? Quando o pedido pendente basta para o Brand Registry?
16. Qual é a taxa de avaliação por venda em alimento de marca com solicitação uniforme, e em quanto tempo se chega às faixas dos líderes?
17. Que métricas da conta um agente pode monitorar via SP-API, dado que `targetValue` vem sem valor na documentação pública ([rep] §2.1)?
