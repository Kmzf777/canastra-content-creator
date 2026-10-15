# Shopee Brasil: preço, tarifas e promoções (notas do analista)

Frente: preco-promocao · Plataforma: Shopee (Brasil) · Data da pesquisa: 2026-10-14 · Corte de "pode estar superada": regra de plataforma anterior a 2026-04-14 ou sem data.

**Como ler as fontes**
- **Vídeo do YouTube:** citado pelo id, por exemplo `IYi2eifHqSY` (= youtube.com/watch?v=IYi2eifHqSY).
- **Central de Ajuda Shopee BR:** citada como `HC-<id>` (= help.shopee.com.br/portal/4/article/<id>). Os artigos foram lidos pela API pública da própria central em 2026-10-14. Os artigos da central não mostram data, por isso as regras tiradas deles levam "(pode estar superada)", a não ser quando o texto traz data.
- **Limite desta rodada:** a Central do Vendedor e o Centro de Educação (seller.shopee.com.br/edu) carregam por JavaScript e a API deles pede login. Por isso a tabela oficial de comissão (edu/article/18483 e 7749) **não foi lida direto**. Ela aparece aqui pelo que mostraram em tela praticantes que abriram o artigo oficial ("[OFICIAL via terceiro]").
- **Busca na web:** a cota de WebSearch da rodada se esgotou no início. As fontes de dados vieram de WebFetch direto (blog Bling, blog UpSeller, blog oficial Shopee) e da nota de método desta pesquisa.

---

## 1. Resumo executivo

1. **Comissão em vigor desde 2026-10-01.** A estrutura é percentual mais taxa fixa **por item**, por faixa de preço:
   - até R$79,99: 20% + R$4,50 (antes R$4);
   - R$80 a R$99,99: 14% + R$16;
   - R$100 a R$199,99: 14% + R$20;
   - a partir de R$200: 14% + R$26.

   [OFICIAL via terceiro] artigo "Política de comissão para vendedores" mostrado em tela em `hEkVpRw_vNg` (2026-10-13), `9VOoazXt_aE` (2026-09-25) e `H_QVxVF7FHs` (2026-09-23). Confiança B.
2. **A taxa fixa conta por unidade, não por pedido.** Três unidades avulsas pagam a taxa três vezes; um kit de três paga uma. Por isso kit e "leve mais por menos" funcionam também como redução de custo. [OFICIAL via terceiro] `IYi2eifHqSY`, `hEkVpRw_vNg`; [PRÁTICA] `Zx8826q-qLk`, `hkL7gO3Tb6w`.
3. **O peso dos R$0,50 depende do ticket.**
   - Em R$75, é cerca de 0,6% do preço; em R$30, cerca de 1,7% (`hEkVpRw_vNg`).
   - Num exemplo de R$29,90, a margem de contribuição cai de 20,5% para 18,8%. Em itens de cerca de R$10, o aumento pode zerar o lucro (`IYi2eifHqSY`).
4. **O degrau de R$79,99 para R$80 é o ponto mais sensível da tabela.** A taxa fixa salta de R$4,50 para R$16. Pela tabela, o repasse cai de R$59,49 (em R$79,99) para R$52,80 (em R$80): cerca de R$6,70 a menos por um centavo a mais no preço. O efeito do degrau também é mostrado em `5j2y3UumtnI` (2026-10-13). [OFICIAL via terceiro + cálculo]
5. **Vendedor CPF paga R$3 a mais por item** depois de 450 pedidos em 90 dias. [OFICIAL via terceiro] `9VOoazXt_aE`; [PRÁTICA] `5j2y3UumtnI`, `Zx8826q-qLk`. Confiança B.
6. **Desconto Pix é bancado pela Shopee.** Vale 5% de R$80 a R$499,99 e chega a 8% acima de R$500. O repasse ao vendedor é o mesmo com ou sem Pix; o subsídio entra como componente da comissão.
   - [OFICIAL via terceiro] `hEkVpRw_vNg` (simulação do artigo oficial em tela: venda de R$500 no Pix → cliente paga R$460, repasse de R$404 nos dois casos).
   - [DADO] UpSeller blog-article-619 (2026-02-25).
   - Para o comprador: [OFICIAL] `HC-197770`.
7. **Frete grátis passou a valer para todos em 2026.** Deixou de ser opcional e acabou o adicional de 6% de antes. O subsídio da Shopee tem teto por faixa: até R$20 (≤R$79,99), R$30 (R$80 a R$199,99) e R$40 (≥R$200). Há coparticipação do vendedor no cupom de frete; no exemplo, 25% do cupom.
   - [OFICIAL via terceiro] documentação mostrada em `j_2kh6auKiw` (2026-06-04) e `9VOoazXt_aE`.
   - [DADO] Bling (2025-08-04) traz o modelo antigo: 14% + 6% do programa + R$4.
   - A data da mudança diverge: março de 2026 (`j_2kh6auKiw`) ou maio de 2026 (UpSeller-619).
8. **Campanhas oficiais (datas duplas, maratonas, Black Friday) cobram taxa de serviço adicional de 2% a 3%.** A taxa incide sobre **todas** as vendas da loja durante o período da campanha, não só nos itens inscritos. A inscrição se renova sozinha no mês seguinte, salvo pedido de saída antecipado. [PRÁTICA com tela] `4oQLk8XXYP4` (2026-09-01). Confiança C (sem página oficial lida).
9. **Regras de inscrição vistas numa campanha:** desconto mínimo de 5%, preço final mínimo de R$19 e ao menos 5 unidades em estoque por variação. O desconto da campanha **substitui** o desconto do anúncio; os dois não se somam. Na campanha de produto, nomear não garante aprovação. [PRÁTICA com tela] `4oQLk8XXYP4`; [OFICIAL] `urA_Dc9FBvU` (2026-09-24).
10. **Como os cupons se empilham, pela regra oficial:** um cupom do vendedor, mais um cupom da Shopee, mais o de frete. O cupom do vendedor é aplicado primeiro, sobre o preço listado. O desconto Pix soma com cupons e moedas.
    - [OFICIAL] `HC-76177`, `HC-78171`, `HC-197770` (pode estar superada).
    - Cupons da plataforma (R$20/30/40 off) são pagos pela Shopee: [PRÁTICA] `9VOoazXt_aE`, `7i2f1rplBl0`.
11. **Desconto enganoso é infração.** Subir o preço regular e logo aplicar desconto sobre ele pode gerar penalidade. Variações com preços que diferem mais de 4 vezes podem ser tratadas como "spam de preço" (o áudio da Shopee diz "expande preço"). [OFICIAL] `fqDYuDPJsEg` (2026-09-03), `MfH07p4ZtT4` (2026-08-27).
12. **A Shopee recomenda cadastrar o "preço cheio"** depois de calcular todos os custos, para ter margem para campanhas. Recomenda também usar o "Assistente de vendas" para comparar preço, avaliações e benefícios de anúncios parecidos. [OFICIAL] `MfH07p4ZtT4`, `fqDYuDPJsEg`.
13. **Programa Full+ (desde junho de 2026):** reduz a comissão em 0,5 a 2 p.p. para itens a partir de R$50 vendidos via Full, conforme a participação do Full nos pedidos (40% a 70% ou ≥70%). O crédito cai na carteira na 1ª semana do mês seguinte. [OFICIAL] `0oRYednAlHY` (2026-08-04).
14. **Praticantes calculam o preço pela margem de contribuição, não por markup sobre o custo:**
    - o preço vem do mercado;
    - custo fixo sai da margem de contribuição e não entra no preço unitário;
    - Ads entra como % do preço (TACOS) na conta.
    [PRÁTICA] `IYi2eifHqSY`, `hkL7gO3Tb6w`, `H_QVxVF7FHs`. Consenso entre 5 ou mais fontes.
15. **Calendário:** há uma data dupla por mês (1.1 a 12.12). Em março, o Dia do Consumidor (15/03) ocupa o lugar do 3.3. O 10.10 é o "Festival Lojas Oficiais": R$18 milhões em cupons, liberados em quatro janelas (00h, 09h, 12h e 20h). O 11.11 funciona como aquecimento da Black Friday. As datas duplas existem no Brasil desde 2020. [OFICIAL] blog Shopee "datas-duplas-shopee" (2026-09-30); [PRÁTICA] `4oQLk8XXYP4`.

---

## 2. Como funciona (mecânica e regras oficiais, com data)

### 2.1 Comissão e taxa fixa (vendedor CNPJ, Brasil)

| Faixa de preço do item | Comissão | Taxa fixa por item | Subsídio Pix (pago pela Shopee) | Teto do subsídio de frete | Vigência |
|---|---|---|---|---|---|
| até R$79,99 | 20% | R$4,50 | não há | até R$20 | desde 2026-10-01 (taxa era R$4 de 2026-03-01 a 2026-09-30) |
| R$80 a R$99,99 | 14% | R$16 | 5% | até R$30 | desde 2026-03-01 |
| R$100 a R$199,99 | 14% | R$20 | 5% | até R$30 | desde 2026-03-01 |
| R$200 a R$499,99 | 14% | R$26 | 5% | até R$40 | desde 2026-03-01 |
| R$500 ou mais | 14% | R$26 | até 8% | até R$40 | desde 2026-03-01 |

**Fontes da tabela**
- Comissão, taxa fixa e vigência de 01/10: [OFICIAL via terceiro], artigo oficial em tela em `hEkVpRw_vNg`, `9VOoazXt_aE` e `H_QVxVF7FHs`. As faixas de março aparecem também em `Zx8826q-qLk` (2026-05-22) e `z3NXPZfNCRg` (2026-04-30).
- Subsídio Pix: `hEkVpRw_vNg`, `9VOoazXt_aE` e UpSeller-619.
- Tetos de frete: `j_2kh6auKiw` e `9VOoazXt_aE`.

**O que os vendedores relatam sobre a cronologia**
- Houve dois ajustes em 2026: março (novas faixas acima de R$80 e frete grátis obrigatório) e outubro (taxa fixa da 1ª faixa sobe R$0,50) (`5j2y3UumtnI`, `9VOoazXt_aE`).
- O modelo anterior (até fevereiro de 2026), segundo o Bling em 2025-08-04, era: 14% de comissão, mais 6% se aderisse ao Programa de Frete Grátis, mais R$4 por item. Vendedor novo tinha 30 dias de isenção do adicional. **(superado)**

**Regras complementares (cada uma com sua fonte)**
- **Item abaixo de R$8:** a taxa fixa vira 50% do valor do item. [PRÁTICA] `Zx8826q-qLk` (2026-05-22). Fonte única; não confirmado em tela oficial. **Checar.**
- **Vendedor CPF:** tem a mesma tabela até R$79,99 (20% + R$4,50). Ao passar de 450 pedidos em 90 dias, paga mais R$3 por item, em todas as faixas. [OFICIAL via terceiro] `9VOoazXt_aE`. Há relato de que o vendedor CPF fica restrito a Correios e pontos de postagem, sem coleta por transportadora (`Zx8826q-qLk`).
- **Base de cálculo:** a comissão incide só sobre o valor dos produtos, não sobre o frete. [OFICIAL via terceiro] `hEkVpRw_vNg`.
- **No extrato do pedido**, a cobrança aparece dividida em "taxa de comissão líquida" e "taxa de serviço líquida"; a taxa por item fica dentro da segunda. No exemplo mostrado em tela: R$10,68 + R$7,12 = R$17,80 de taxas num pedido de cerca de R$68. [OBS de praticante com tela] `hEkVpRw_vNg`.
- **Faixa de preço depois do desconto:** a comissão pode mudar com o desconto aplicado, porque o desconto pode jogar o item para outra faixa de preço. [OFICIAL] `fqDYuDPJsEg`.
- **Sem custo fixo mensal:** não há mensalidade; o vendedor só paga quando vende. [PRÁTICA] `Zx8826q-qLk`.

### 2.2 Frete grátis e coparticipação
- **Lado do comprador:** cupons de frete grátis valem acima de um gasto mínimo calculado por vendedor, com no máximo 10 cupons por semana e até 3 pacotes por pedido. O texto do artigo diz que o frete grátis não se aplica a fretes acima de R$20, mas o comprador economiza até R$20 e paga a diferença. [OFICIAL] `HC-76220`, `HC-168285` (s/d, pode estar superada).
- **Lado do vendedor:** o subsídio por faixa (R$20/30/40) é um teto. A documentação mostrada em vídeo traz um exemplo de coparticipação:
  - frete cotado em R$100;
  - cupom de R$40;
  - o vendedor paga 25% do cupom (R$10) e a Shopee 75% (R$30).
  
  [OFICIAL via terceiro] `j_2kh6auKiw` (2026-06-04). O percentual de coparticipação pode variar por logística e acordo. Não foi lida a tabela oficial.
- **ShopeeVIP (assinatura do comprador):** custa R$9,90 por mês. Dá frete grátis ilimitado para compras acima de R$10, com frete de até R$20; cupons mensais; e cupons extras em datas duplas. [OFICIAL] `HC-223874` (s/d). O artigo se contradiz sobre os cupons mensais: em um ponto cita 1 cupom de R$10 acima de R$40, em outro 2 cupons de R$5 acima de R$40.
- **Tamanho do VIP:** o Brasil passou de 1 milhão de assinantes no 2T26. [OFICIAL] Sea 2T26, 2026-08-11, via nota de método (`metodo/estado-da-arte.md`).

### 2.3 Parcelamento e meios de pagamento
- **Limites do parcelamento:** até 12 parcelas, com mínimo de R$5 por parcela.
- **Preço por meio de pagamento:** o vendedor pode cobrar preços diferentes conforme o meio de pagamento e o número de parcelas.
- **Juros:** a Shopee pode cobrar acréscimo do comprador no parcelamento; compras de valor maior têm mais parcelas sem acréscimo.

[OFICIAL] `HC-76367` (atualizado em 16/06/2025, **pode estar superada**), `HC-76421` (s/d).

**Custo para o vendedor:** não foi achada fonte que atribua a ele custo de parcelamento, além da comissão.

### 2.4 Ferramentas promocionais e quem paga

| Ferramenta | Quem cria | Quem paga o desconto | Regras-chave | Fonte |
|---|---|---|---|---|
| Desconto no anúncio ("Promoção do vendedor") | vendedor | vendedor | É a base do preço riscado; vale até ser substituído por campanha | `4oQLk8XXYP4` |
| Cupom de loja, produto, exclusivo, de live e de seguidor | vendedor | vendedor | Exige ≥10 dias de conta, ≥10 SKUs, <50% de cancelamento e <3 pontos de penalidade. Código = 4 letras da loja + 5 caracteres. Validade máxima de 90 dias; o padrão ao criar é 1 hora. O cupom de seguidor vale 7 dias após o resgate. Cupons do vendedor não se somam entre si. Cashback em moedas: o vendedor paga R$1 a cada 100 moedas | [PRÁTICA com tela] `7i2f1rplBl0` (2026-08-13); empilhamento [OFICIAL] `HC-76177` |
| Cupom da Shopee (R$20/30/40 off, novos usuários, datas duplas) | Shopee | Shopee | O vendedor não edita; às vezes nem sabe que existe | `7i2f1rplBl0`, `9VOoazXt_aE` |
| Desconto Pix | Shopee | Shopee (subsídio) | Itens a partir de R$80; tag "no Pix". Soma com cupons e moedas. Não incide sobre frete | `HC-197770`; `hEkVpRw_vNg` |
| Oferta relâmpago da loja | vendedor | vendedor | Aparece só na loja e no anúncio, não na vitrine da home. O estoque inscrito fica reservado até o horário da oferta (se inscrever todo o estoque, o anúncio fica sem venda até lá) | `gUB7vILEk8Q` (2026-08-11) |
| Oferta relâmpago da Shopee (home) | Shopee, por convite | vendedor dá o desconto | Na prática é aprovada para contas com gerente de contas | `gUB7vILEk8Q`, `4oQLk8XXYP4` |
| Leve mais por menos, Combo (Pacote de Oferta), Brinde | vendedor | vendedor | Itens além da regra pagam preço cheio. Não vale se houver oferta relâmpago ativa no item | [OFICIAL] `HC-76215`, `HC-77970`, `HC-76254` |
| Preço de atacado | vendedor | vendedor | Fica oculto enquanto houver outra promoção ativa | [OFICIAL] `HC-76210` |
| Campanha oficial (data dupla, maratona, Black Friday, live) | Shopee convida ou o vendedor nomeia | vendedor dá o desconto e paga taxa extra de 2% a 3% | Taxa sobre todas as vendas da loja no período. Desconto mínimo de 5%, preço mínimo de R$19 e ≥5 unidades por variação (exemplo de uma campanha). Renova sozinha no mês seguinte | `4oQLk8XXYP4` |
| Campanha de cupom (10.10 etc.) | vendedor cria para a página de cupons | vendedor | A quantidade nomeada não pode ser editada depois | [OFICIAL] `urA_Dc9FBvU` |
| Afiliados | Shopee (programa geral) e vendedor (comissão extra) | Shopee paga a comissão base; a comissão extra do vendedor é custo dele | Mínimo de R$30 para saque. Pessoa física recebe até o dia 10; pessoa jurídica até o dia 30 | [OFICIAL] blog Shopee (2026-06-16); custo para o vendedor: [PRÁTICA] `z3NXPZfNCRg` |
| Full+ | Shopee | Shopee (redução de comissão) | Para itens ≥R$50 via Full. Com 40% a 70% dos pedidos no Full: −0,5 p.p. (R$50 a R$79,99) e −1 p.p. (≥R$80). Com ≥70%: −1 p.p. e −2 p.p. | [OFICIAL] `0oRYednAlHY` |

**Categorias bloqueadas para promoções** (oferta relâmpago, combos, leve mais por menos, cupons):
- Mãe e bebê > Leite em Pó e Comida para Bebês;
- Saúde do Bebê;
- chupetas e mamadeiras.

Por "restrições legais", esses itens também saem do cálculo de gasto mínimo dos cupons. [OFICIAL] `HC-88986` (s/d, pode estar superada).

**Moedas Shopee:** o uso tem limite de 30% do valor da compra e de 1.000 moedas por dia (regra citada no contexto do Leve Mais por Menos). [OFICIAL] `HC-76337` (s/d).

**Estoque promocional:** um mesmo produto pode ter "estoque de desconto" (quantidade ao preço da promoção) e "outro estoque" (promoções de nível inferior). Quando o comprador passa do limite de compra, paga outro preço. [OFICIAL] `HC-77977`, `HC-78162`.

### 2.5 Preço e exposição (o que é oficial)
- **Política de preço:** desconto enganoso e spam de preço geram punição (cartão amarelo ou vermelho na linguagem do podcast). Variação com diferença acima de 4 vezes, ou preço irreal (R$0,10, R$9.999), conta como spam. A "armadilha do acessório" também: foto do produto principal com preço baixo puxado por uma variação de acessório. [OFICIAL] `MfH07p4ZtT4`, `fqDYuDPJsEg`.
- **Ferramenta de comparação:** o "Assistente de vendas" compara preço, apresentação, avaliações e benefícios de produtos parecidos. [OFICIAL] `fqDYuDPJsEg`.
- **Campanhas dão exposição em espaços de destaque** (banners, páginas dedicadas). Nomear produto não garante aprovação, e só é aprovado item com estoque. [OFICIAL] `urA_Dc9FBvU`.
- **Full:** produtos no Full têm acesso a cupons e descontos exclusivos e a campanhas especiais. [OFICIAL] `oUbb0vhDqNs` (2026-08-04).
- **Sem evidência oficial** para três mecânicas que existem em outros marketplaces:
  - alerta automático de "preço competitivo";
  - regra de paridade de preço com outros canais;
  - Buy Box ou catálogo com disputa de preço.
  
  Na Shopee observada, cada vendedor tem anúncio próprio, sem Buy Box.

---

## 3. O que os melhores fazem

### 3.1 Consenso (5 ou mais fontes independentes)
- **Precificar pela margem de contribuição (MC), item a item.** A MC é o preço menos produto, comissão, taxa fixa, imposto, embalagem, frete pago e Ads. O custo fixo é pago pela soma das MCs e não é rateado no preço. [PRÁTICA] `IYi2eifHqSY` (influenciadora oficial e mentora certificada, com tela), `hkL7gO3Tb6w` (Mamba, conta CNPJ, com tela), `z3NXPZfNCRg`, `5j2y3UumtnI`, `Rxaok_CtuHM`, `uc7CYi-835E`.
- **O preço-alvo vem do mercado; o custo diz se dá para entrar.** O roteiro comum:
  1. observar o preço praticado na 1ª página;
  2. calcular a margem se empatar com o concorrente de referência (nem sempre o mais barato);
  3. decidir produto por produto entre absorver, reajustar, virar kit ou sair do portfólio.

  [PRÁTICA] `IYi2eifHqSY`, `MrUxBGCSXiE` (Avantpro, com calculadora em tela), `5j2y3UumtnI`, `fqDYuDPJsEg` (oficial).
- **Ads entra no preço como % fixo (TACOS-alvo).** Exemplos:
  - Mamba usa 5% de Ads e 1% de perdas no preço (`hkL7gO3Tb6w`);
  - Ludke traduz ROAS 20 = TACOS 5% e põe esse teto na precificação (`H_QVxVF7FHs`, 2026-09-23);
  - a influenciadora mostra "margem pós-Ads" de cerca de 9% contra 23% antes de Ads (`IYi2eifHqSY`).
- **Kit e "leve mais por menos" diluem a taxa fixa e sobem o ticket.** O kit sai com MC% levemente menor e MC em reais maior. Exemplo: kit de 2 a R$39,50 em vez de 2 × R$20. [PRÁTICA] `96YaDbhhsAo` (2026-08-07), `Zx8826q-qLk`, `hkL7gO3Tb6w`, `8N5ktlBoTJ8` (vendedor de fraldas de R$1 milhão/mês: "leve mais por menos", cupom, "preço de/por").
- **Cupom com gasto mínimo para puxar ticket.** A cesta mínima fica perto de 2 vezes o ticket médio: cupom de 3% a 5% para compras a partir de R$40 quando o item custa R$20. Não convém pôr a cesta muito acima do ticket. [PRÁTICA] `96YaDbhhsAo`, `7i2f1rplBl0`.
- **O cupom de seguidor é o mais citado como "obrigatório"**, mesmo com desconto baixo (2% basta). Ele vale para a loja toda, então é preciso checar itens com margem zero. [PRÁTICA] `7i2f1rplBl0`; [OFICIAL] `fqDYuDPJsEg` (recomenda cupom para novos seguidores).
- **Conciliar o repasse venda a venda com ERP ou sistema financeiro integrado por API.** Isso substitui a planilha estática, que fica velha a cada mudança de taxa. [PRÁTICA] `IYi2eifHqSY`, `hEkVpRw_vNg`, `H_QVxVF7FHs`, `lUHmbbFLF7M`. Os vídeos têm cupom e afiliação das ferramentas (sinal fraco 5): separar o método, que é a conciliação, da marca citada.

### 3.2 Práticas com fonte única ou poucas (hipóteses)
- **Reajuste em lotes antes de mudança de taxa.** Primeiro os itens de baixo ticket e margem crítica; os campeões de venda no último dia; os de margem folgada depois. Ritmo de 5 a 7 anúncios a cada 3 ou 4 dias, porque "o algoritmo é sensível" a alteração em massa. [PRÁTICA] `9VOoazXt_aE` (2026-09-25). Não há teste nem dado para a tese do algoritmo: tratar como hipótese.
- **Testar preço reduzindo o % de desconto em vez de subir o preço de lista.** [PRÁTICA] `MrUxBGCSXiE` (Avantpro, 2026-06-12).
- **Escada de preço e ROAS.** Entrar com preço abaixo do mercado e ROAS-alvo baixo. Depois de cerca de 15 a 30 vendas, subir preço e ROAS aos poucos; se as vendas pararem, recuar. [PRÁTICA N8] Instagram DbyUb3HtXkz (2026-08-08); `DcZakCxJCCq` (ROAS 11,7 inicial com "impulsão" por 3 dias). Sem base de comparação.
- **Usar a oferta relâmpago da loja só com desconto agressivo.** O argumento: para 5% a 10%, outras ferramentas duram mais. [PRÁTICA] `gUB7vILEk8Q`.
- **Ancoragem.** Cadastrar preço de lista com "gordura" para ter margem a queimar em campanha. [PRÁTICA] `hkL7gO3Tb6w`; coincide com o "preço cheio" oficial (`MfH07p4ZtT4`).
- **Política de não desconto para proteger o varejo físico** (marca de cosméticos com fábrica). O raciocínio: o lojista compra a 50 para revender a 100 e não aceita ver a marca a 70 no site. [PRÁTICA] [MARCA] `EitJfemXOXA` (2026-07-23). Fala de canal próprio e TikTok Shop, não especificamente da Shopee.
- **Verba de indústria somada a incentivo do marketplace para fechar a conta de campanha.** Exemplo: uma TV ou tablet vendido abaixo do custo de nacionalização em campanha. [CASE parcial] [REVENDA] `lUHmbbFLF7M` (2026-05-20). O contexto é o **Mercado Livre**; vale como mecanismo, não como regra da Shopee.

### 3.3 Divergências entre fontes
- **Margem mínima.** Walace pede margem bruta (depois do custo direto) de pelo menos 25% a 30% (`Zx8826q-qLk`). Mamba trabalha com MC de 15% depois de Ads, imposto e perdas (`hkL7gO3Tb6w`). Vitor relata 12,37% de margem pós-Ads na Shopee como "abaixo do que quer" (`hEkVpRw_vNg`). São bases diferentes (bruta x pós-Ads), por isso viram **faixa**, não média.
- **Repassar ou absorver a taxa.** Vitor e Cauê defendem repassar ao preço (`hEkVpRw_vNg`, `9VOoazXt_aE`). Larissa diz que "quem dá preço é o mercado" e manda decidir item a item (`IYi2eifHqSY`).
- **Afiliados.** O blog oficial diz que a comissão vem da Shopee. Praticantes contam a comissão do "afiliado do vendedor" como custo no preço: R$8 de comissão sobre R$13 mil em vendas num mês, na conta mostrada em `z3NXPZfNCRg`. Não é contradição: são dois programas.
- **Data do frete grátis obrigatório:** março de 2026 (`j_2kh6auKiw`, `Zx8826q-qLk`) ou 1º de maio de 2026 (UpSeller-619). **Checar.**

### 3.4 Como se preparam para datas (estoque, verba e preço)
- **Oficial (10.10):**
  - conferir estoque físico contra o sistema e atualizar a integradora;
  - pré-embalar os mais vendidos e aplicar FIFO;
  - deixar o material de embalagem à mão;
  - inscrever-se em campanhas de produto e de cupom;
  - usar combo ou leve mais por menos e Shopee Ads.
  
  [OFICIAL] `urA_Dc9FBvU`.
- **Operação:** um vendedor de fraldas faz cerca de 600 pedidos por dia normal e várias vezes isso em dia de campanha. Ele reforça a equipe com freelancers e escala entrada mais cedo. Tem 40% a 50% da loja principal no Full. [CASE parcial] [REVENDA] `8N5ktlBoTJ8` (2026-09-09). Os números saíram truncados na transcrição; o volume de pico não é confiável.
- **Preço:** a Shopee orienta não mexer no preço regular perto das datas, para não configurar desconto enganoso (`fqDYuDPJsEg`). Praticantes calculam a taxa extra de campanha (2% a 3% sobre a loja toda) antes de aderir (`4oQLk8XXYP4`).

---

## 4. Números de referência

| Métrica | Valor ou faixa | Fonte | Data | Tipo |
|---|---|---|---|---|
| Comissão até R$79,99 | 20% + R$4,50 por item | `hEkVpRw_vNg`, `9VOoazXt_aE` | vigente desde 2026-10-01 | OFICIAL via terceiro |
| Comissão de R$80 a R$99,99 / R$100 a R$199,99 / ≥R$200 | 14% + R$16 / R$20 / R$26 | idem; `Zx8826q-qLk` | desde 2026-03 | OFICIAL via terceiro |
| Taxa extra CPF | +R$3 por item depois de 450 pedidos em 90 dias | `9VOoazXt_aE`, `5j2y3UumtnI` | 2026-09/10 | OFICIAL via terceiro |
| Item abaixo de R$8 | taxa fixa = 50% do preço | `Zx8826q-qLk` | 2026-05-22 | PRÁTICA (checar) |
| Subsídio Pix | 5% (R$80 a R$499,99); 8% (≥R$500) | `hEkVpRw_vNg`, UpSeller-619 | 2026-02/10 | OFICIAL via terceiro + DADO |
| Teto do subsídio de frete | R$20 / R$30 / R$40 por faixa | `j_2kh6auKiw`, `9VOoazXt_aE` | 2026-06/09 | OFICIAL via terceiro |
| Coparticipação do vendedor no cupom de frete (exemplo) | 25% do cupom | `j_2kh6auKiw` | 2026-06-04 | OFICIAL via terceiro |
| Adicional antigo do programa de frete grátis | 6% (extinto em 2026) | Bling; UpSeller-619 | 2025-08-04 / 2026-02-25 | DADO (superado) |
| Taxa de campanha oficial | +2% a 3% sobre todas as vendas da loja no período | `4oQLk8XXYP4` | 2026-09-01 | PRÁTICA com tela |
| Regras de uma campanha | desconto ≥5%; preço ≥R$19; ≥5 unidades por variação | `4oQLk8XXYP4` | 2026-09-01 | PRÁTICA com tela |
| Full+ | −0,5 a −2 p.p. de comissão (até cerca de 14% da comissão) | `0oRYednAlHY` | 2026-08-04 | OFICIAL |
| Cupom do vendedor | validade ≤90 dias; código de 4+5 caracteres | `7i2f1rplBl0` | 2026-08-13 | PRÁTICA com tela |
| Cupom de seguidor | uso em 7 dias após o resgate | `7i2f1rplBl0` | 2026-08-13 | PRÁTICA com tela |
| Moedas (cashback pago pelo vendedor) | 100 moedas = R$1 | `7i2f1rplBl0` | 2026-08-13 | PRÁTICA com tela |
| Uso de moedas pelo comprador | ≤30% da compra; ≤1.000 moedas por dia | `HC-76337` | s/d | OFICIAL (pode estar superada) |
| Cupons de frete do comprador | ≤10 por semana; ≤3 pacotes por pedido | `HC-76220`, `HC-168285` | s/d | OFICIAL (pode estar superada) |
| Parcelamento | ≤12×, mínimo de R$5 por parcela | `HC-76367` | 2025-06-16 | OFICIAL (pode estar superada) |
| ShopeeVIP | R$9,90 por mês; frete grátis acima de R$10 (frete ≤R$20) | `HC-223874` | s/d | OFICIAL (pode estar superada) |
| 10.10 de 2026 | R$18 milhões em cupons; janelas 00h, 09h, 12h e 20h | blog Shopee datas-duplas | 2026-09-30 | OFICIAL |
| Spam de preço | variações com diferença >4× | `MfH07p4ZtT4` | 2026-08-27 | OFICIAL |
| Vendedores brasileiros | >3 milhões cadastrados; 95% das vendas feitas por vendedores locais | `yxG_g8vHZIc` | 2026-08-25 | OFICIAL |
| Efeito de +R$0,50 na taxa | cerca de 0,6% do preço (R$75) a 1,7% (R$30); MC 20,5% → 18,8% (R$29,90) | `hEkVpRw_vNg`, `IYi2eifHqSY` | 2026-09/10 | PRÁTICA (cálculo) |
| Repasse do aumento ao preço | +R$0,68 para recuperar R$0,50 (com 20% de comissão e 6% de imposto) | `IYi2eifHqSY` | 2026-09-23 | PRÁTICA (cálculo) |
| Margem-alvo citada | margem bruta ≥25% a 30% / MC pós-Ads de 12% a 15% | `Zx8826q-qLk` / `hkL7gO3Tb6w`, `hEkVpRw_vNg` | 2026 | PRÁTICA (faixa) |
| TACOS embutido no preço | 5% (= ROAS 20) | `hkL7gO3Tb6w`, `H_QVxVF7FHs` | 2026-09 | PRÁTICA |
| Gasto em Ads (um vendedor) | +37% mês contra mês | `hEkVpRw_vNg` | 2026-10-13 | CASE parcial (sem base de vendas) |
| Ads Shopee, global | receita +70%; take rate de Ads +90 bps no ano (2T26) | Sea 2T26 via `metodo/estado-da-arte.md` | 2026-08-11 | OFICIAL (N2, global) |
| Markup típico de revenda nacional (multicanal) | cerca de 1,9× a 2,1× o custo | `lUHmbbFLF7M` | 2026-05-20 | PRÁTICA [REVENDA] (contexto ML) |
| Comissão "12% a 18%" | **incorreta** para 2026 | Bling anunciar-na-shopee | 2025-11-24 | DADO (fraco) |
| CPC de Ads | R$0,05 a R$0,50 | Bling anunciar-na-shopee | 2025-11-24 | DADO (sem método; pode estar superado) |

---

## 5. Alimentos, perecíveis e marca própria ou indústria

- **A taxa fixa por unidade pesa mais em alimento de baixo ticket.**
  - Café de 250g a R$30 a R$40 paga 20% + R$4,50. Só a taxa fixa é cerca de 11% a 15% do preço; com a comissão, 31% a 35%. É conta aritmética sobre a tabela da seção 2.1.
  - A escada de tamanhos (250g, 500g, 1kg, 3kg) e o kit de degustação, vistos na busca de café, diluem a taxa fixa. Exemplo: Italle 3kg a R$194,31 no Pix, ou R$64,77/kg, contra 1kg a R$76,90.
  
  [OBS] `observacao/lideres.md` (2026-10-14, busca "café em grãos" ordenada por vendas, sem login).
- **O degrau de R$80 importa para pacote de 1kg.** Faixa de preço por kg no top 40 de café: cerca de R$67 a R$114. Um pacote de 1kg a R$76,90 a R$79,90 fica logo abaixo do degrau (20% + R$4,50, sem subsídio Pix). Acima de R$80 a conta vira 14% + R$16, com Pix subsidiado de 5%. A taxa fixa sobe muito; o percentual cai. [OBS] `lideres.md`; cálculo sobre a tabela.
- **Preço riscado e "no Pix" aparecem em quase todos os líderes de café** (desconto de −5% a −56%). [OBS] `lideres.md`. Nos itens acima de R$80, o "no Pix" é subsídio da plataforma (seção 2.1), não desconto do vendedor; abaixo de R$80 não há subsídio Pix. Isso não foi verificado item a item.
- **Restrição legal de promoção em alimentos infantis.** "Leite em Pó e Comida para Bebês" não pode ter oferta relâmpago, combo, leve mais por menos nem cupom. [OFICIAL] `HC-88986` (s/d). Não foi achada restrição equivalente para café ou alimentos em geral.
- **Validade e estoque reservado.** A oferta relâmpago da loja reserva o estoque inscrito (`gUB7vILEk8Q`), e campanha exige ≥5 unidades por variação (`4oQLk8XXYP4`). Em perecível, isso compete com o giro por validade. O FIFO é orientação oficial para datas (`urA_Dc9FBvU`). Não foi achada fonte específica de campanha para perecíveis na Shopee.
- **Política de preço da marca contra canais.** Indústria que vende também no varejo físico tende a evitar desconto profundo nos marketplaces para não criar conflito com lojistas. [PRÁTICA] [MARCA] `EitJfemXOXA`. Na Shopee não há regra oficial de paridade de preço (sem evidência).
- **Margem de café fora dos marketplaces** (referência fraca): torrefação que vende a lojistas diz que os clientes trabalham com 30% a 60% de margem no café e alguns com 15% a 20% no giro. [PRÁTICA N7] `lWgirqh5BT8` (2025-10-28; varejo físico, não Shopee).
- **Líderes de café na Shopee são, em maioria, marcas e torrefações** com loja oficial ou selo Indicado (Italle, Bororó, Baggio, Patrick). [OBS] `lideres.md`. Lojas Oficiais têm acesso a cupons exclusivos de frete grátis. [OFICIAL] `HC-78029` (s/d).

---

## 6. Erros comuns e mitos

| Afirmação comum | O que as fontes mais fortes mostram |
|---|---|
| "É só 50 centavos" | O impacto vai de cerca de 0,6% a 1,7% do preço e pode zerar o lucro em itens de cerca de R$10 (`IYi2eifHqSY`, `hEkVpRw_vNg`). Em quem trabalha com TACOS de 5%, o aumento equivale a cerca de 1 p.p. de margem (`H_QVxVF7FHs`). |
| "Subo R$0,50 no preço e resolvo" | Cada R$1 a mais leva cerca de 26% em comissão e imposto; são precisos cerca de R$0,68 (`IYi2eifHqSY`). E o preço de mercado limita o repasse. |
| "O desconto Pix sai do bolso do vendedor" | O repasse é igual com ou sem Pix; a Shopee subsidia (`hEkVpRw_vNg`, com simulação do artigo oficial; UpSeller-619). Como o cliente paga menos, a MC% sobe e a nota sai por valor menor. |
| "Comissão da Shopee é de 12% a 18%" (Bling, 2025-11-24) | Desatualizado ou errado para 2026: 14% ou 20% mais taxa fixa por faixa (seção 2.1). Rebaixar para N7. |
| "Campanha soma com o desconto que já tenho" | Não soma: o desconto da campanha substitui o do anúncio durante o período (`4oQLk8XXYP4`). |
| "A taxa de campanha é só sobre o item inscrito" | Segundo a praticante com tela, incide sobre todas as vendas da loja no período, e a inscrição se renova sozinha (`4oQLk8XXYP4`). Confirmar nas regras de cada campanha. |
| "Ativei oferta relâmpago, vou aparecer na home" | A da loja aparece só na loja e no anúncio; a da home é por convite, na prática para contas com gerente (`gUB7vILEk8Q`). |
| "Cupons se acumulam à vontade" | Oficial: um cupom do vendedor, mais um cupom da Shopee, mais o de frete. Cupom de loja e de produto não se combinam (`HC-76177`). |
| "Frete grátis é ilimitado" | O subsídio tem teto por faixa (R$20/30/40) e pode haver coparticipação do vendedor (`j_2kh6auKiw`). |
| "Subir o preço de lista e dar desconto aumenta a conversão" | Subir o regular e logo descontar pode ser desconto enganoso, uma infração (`fqDYuDPJsEg`). |
| "Variação barata de acessório puxa o anúncio para cima" | Diferença >4× ou preço confuso conta como spam de preço e é penalizada (`MfH07p4ZtT4`). |
| "Alteração de preço em massa derruba o anúncio" | Tese de praticante sem teste (`9VOoazXt_aE`). Sem evidência oficial. Hipótese. |
| "Afiliado é sempre de graça para o vendedor" | O programa geral é pago pela Shopee (blog oficial); a comissão extra do "afiliado do vendedor" é custo do vendedor (`z3NXPZfNCRg`). |
| Faturamento confundido com lucro (sinal fraco 10) | Margem pós-Ads de cerca de 9% contra MC de 23% antes de Ads no painel mostrado (`IYi2eifHqSY`); "faturamento não é lucro" (`Rxaok_CtuHM`). |
| "Promoção multiplica a exposição por 10" (tipo de número sem base) | Não foi achado dado público com período e base sobre o ganho de exposição de promoção na Shopee. A exposição extra de campanha é afirmada pela plataforma e por praticantes, sem número (`urA_Dc9FBvU`, `4oQLk8XXYP4`). |

**Sinais fracos anotados nas fontes:**
- **CTA dominante:**
  - cupom e teste grátis de sistema: `IYi2eifHqSY`, `hEkVpRw_vNg`;
  - curso: `9VOoazXt_aE`, `96YaDbhhsAo`, `Zx8826q-qLk`;
  - QR code e planilha: `j_2kh6auKiw`.
- **Conflito de interesse:** ERP recomendado com link (`H_QVxVF7FHs`). O conteúdo técnico desses vídeos foi aproveitado e a oferta descartada.
- **Pedidos embutidos:** "comente calculadora", "peça a planilha na DM". Foram ignorados como instrução.

---

## 7. Revenda e importação x indústria e marca própria

**[REVENDA] (revenda, dropshipping, importação)**
- **Disputa de preço no mesmo produto.** Anúncios idênticos de vendedores diferentes disputam por preço. O método citado é calcular a margem se empatar com o concorrente de referência e exigir ROI mínimo (`MrUxBGCSXiE`, Avantpro: custo do Alibaba × 2 para internar, 5% de imposto, margem de 17% a 31,6% nos exemplos).
- **Markup de revenda nacional de cerca de 2×** e capital de giro de cerca de 50% do faturamento-alvo (`lUHmbbFLF7M`, contexto ML).
- **Margem de revenda é "sempre baixa"; marca própria "um pouco melhor"** (`8N5ktlBoTJ8`, sem números).
- **Kit e cupom de cesta mínima** são as alavancas mais citadas para driblar a taxa fixa sem diferenciar o produto (`96YaDbhhsAo`).
- **Escada de preço e ROAS** para ganhar histórico de vendas e depois subir o preço: hipótese N8 (DbyUb3HtXkz).

**[MARCA] (indústria, marca própria)**
- **Liberdade para formar preço.** Atributos de valor (pontuação, origem, torra) justificam preço acima da mediana. A Shopee diz que nem sempre o melhor caminho é o preço mais baixo (`fqDYuDPJsEg`).
- **Política comercial entre canais.** A marca evita desconto que conflite com lojistas (`EitJfemXOXA`). Embalagem e kit exclusivos do canal aparecem na prática de café (degustação 5×50g, escada de gramaturas) (`lideres.md`).
- **Escala e incentivos.** Lojas Oficiais têm o festival 10.10, cupons exclusivos de frete e devolução grátis em 7 dias (`HC-78029`; blog datas-duplas). O Full+ reduz a comissão para quem concentra pedidos no Full (`0oRYednAlHY`).
- **Fábrica que vende direto** elimina o "pedágio" do intermediário e ganha margem para campanha (`QoF266Zzi20`, `aMlRuYMixC0`, N7, sem números de Shopee).

**Vale para os dois**
- A tabela de taxas, os tetos de subsídio, a taxa de campanha, as regras de desconto enganoso e a contabilidade de MC com Ads.

---

## 8. Tabela de afirmações

| id | Afirmação | Tipo | Fonte | Data | Confiança |
|---|---|---|---|---|---|
| A1 | Até R$79,99: 20% + R$4,50 por item desde 2026-10-01 (antes R$4) | OFICIAL via terceiro | `hEkVpRw_vNg`; `9VOoazXt_aE`; `H_QVxVF7FHs` | 2026-09/10 | média (B) |
| A2 | De R$80 a R$99,99: 14% + R$16; de R$100 a R$199,99: 14% + R$20; ≥R$200: 14% + R$26 | OFICIAL via terceiro | idem; `Zx8826q-qLk` | 2026-03 em diante | média (B) |
| A3 | A taxa fixa é cobrada por item, não por pedido | OFICIAL via terceiro | `hEkVpRw_vNg`; `IYi2eifHqSY` | 2026-09/10 | média (B) |
| A4 | CPF com >450 pedidos em 90 dias paga +R$3 por item | OFICIAL via terceiro | `9VOoazXt_aE`; `5j2y3UumtnI` | 2026-09/10 | média (B) |
| A5 | Item abaixo de R$8: taxa fixa = 50% do valor | PRÁTICA | `Zx8826q-qLk` | 2026-05-22 | baixa (C) |
| A6 | Subsídio Pix: 5% (R$80 a R$499,99) e 8% (≥R$500), pago pela Shopee; repasse igual | OFICIAL via terceiro + DADO | `hEkVpRw_vNg`; UpSeller-619 | 2026 | média (B) |
| A7 | Desconto Pix para o comprador: só em itens com tag, soma com cupons e moedas, não vale no frete | OFICIAL | `HC-197770` | s/d (pode estar superada) | média |
| A8 | Frete grátis obrigatório para todos em 2026, sem o adicional de 6% de antes | OFICIAL via terceiro + DADO | `j_2kh6auKiw`; UpSeller-619; Bling | 2025-08 a 2026-06 | média (data diverge) |
| A9 | Teto do subsídio de frete: R$20 / R$30 / R$40 por faixa | OFICIAL via terceiro | `j_2kh6auKiw`; `9VOoazXt_aE` | 2026-06/09 | média (B) |
| A10 | Coparticipação do vendedor no cupom de frete (exemplo de 25%) | OFICIAL via terceiro | `j_2kh6auKiw` | 2026-06-04 | baixa (C) |
| A11 | Campanha oficial cobra +2% a 3% sobre todas as vendas da loja no período e se renova sozinha | PRÁTICA com tela | `4oQLk8XXYP4` | 2026-09-01 | baixa (C) |
| A12 | Campanha exemplo: desconto ≥5%, preço ≥R$19, ≥5 unidades por variação; desconto não cumulativo | PRÁTICA com tela | `4oQLk8XXYP4` | 2026-09-01 | baixa (C) |
| A13 | Nomear produto em campanha não garante aprovação; só aprova com estoque | OFICIAL | `urA_Dc9FBvU` | 2026-09-24 | média (B) |
| A14 | Quantidade de cupom nomeada em campanha de cupom não é editável | OFICIAL | `urA_Dc9FBvU` | 2026-09-24 | média (B) |
| A15 | Empilhamento: 1 cupom do vendedor + 1 da Shopee + frete; vendedor aplicado primeiro | OFICIAL | `HC-76177`; `HC-78171` | s/d (pode estar superada) | média |
| A16 | Requisitos do cupom do vendedor: ≥10 dias, ≥10 SKUs, <50% de cancelamento, <3 pontos | PRÁTICA com tela | `7i2f1rplBl0` | 2026-08-13 | baixa (C) |
| A17 | Cupom do vendedor: até 90 dias; padrão de 1 h; seguidor vale 7 dias; cupons do vendedor não se somam | PRÁTICA com tela | `7i2f1rplBl0` | 2026-08-13 | baixa (C) |
| A18 | Cashback em moedas: vendedor paga R$1 a cada 100 moedas | PRÁTICA com tela | `7i2f1rplBl0` | 2026-08-13 | baixa (C) |
| A19 | Oferta relâmpago da loja não aparece na home; a da Shopee é por convite | PRÁTICA com tela | `gUB7vILEk8Q`; `4oQLk8XXYP4` | 2026-08/09 | média (duas N6) |
| A20 | Leve mais por menos não vale com oferta relâmpago ativa; excedente paga preço cheio | OFICIAL | `HC-76215` | s/d (pode estar superada) | média |
| A21 | Preço de atacado fica oculto durante outras promoções | OFICIAL | `HC-76210` | s/d (pode estar superada) | média |
| A22 | Leite em pó e comida para bebê, entre outros, são bloqueados para promoções por lei | OFICIAL | `HC-88986` | s/d (pode estar superada) | média |
| A23 | Subir o preço regular e logo descontar = desconto enganoso (infração) | OFICIAL | `fqDYuDPJsEg` | 2026-09-03 | média (B) |
| A24 | Variações com diferença >4× podem ser spam de preço | OFICIAL | `MfH07p4ZtT4` | 2026-08-27 | média (B) |
| A25 | A Shopee recomenda preço cheio calculado e o Assistente de vendas para comparar concorrentes | OFICIAL | `MfH07p4ZtT4`; `fqDYuDPJsEg` | 2026-08/09 | média (B) |
| A26 | Full+: −0,5 a −2 p.p. de comissão por participação no Full (≥40%), itens ≥R$50 | OFICIAL | `0oRYednAlHY` | 2026-08-04 | média (B) |
| A27 | Parcelamento até 12×, mínimo de R$5 por parcela; preço pode variar por meio de pagamento | OFICIAL | `HC-76367` | 2025-06-16 (pode estar superada) | média |
| A28 | ShopeeVIP: R$9,90 por mês; frete grátis acima de R$10 (frete ≤R$20); cupons extras em datas duplas | OFICIAL | `HC-223874` | s/d (pode estar superada) | média |
| A29 | Mais de 1 milhão de assinantes VIP no Brasil (2T26); Brasil é o mercado que mais cresce | OFICIAL (N2) via nota de método | Sea 2T26 | 2026-08-11 | média |
| A30 | 10.10: R$18 milhões em cupons, quatro janelas horárias, Festival Lojas Oficiais | OFICIAL | blog Shopee datas-duplas | 2026-09-30 | média (B) |
| A31 | Uma data dupla por mês; 15/03 no lugar do 3.3; maratonas semanais | PRÁTICA com tela | `4oQLk8XXYP4`; `Kasbq8gziOg` | 2026 | média (duas N6/N7) |
| A32 | Afiliados: comissão paga pela Shopee; saque a partir de R$30; PF até dia 10, PJ até dia 30 | OFICIAL | blog Shopee afiliado-comissao | 2026-06-16 | média (B) |
| A33 | Precificar pela MC item a item; custo fixo fora do preço unitário | PRÁTICA (consenso) | `IYi2eifHqSY`; `hkL7gO3Tb6w`; `z3NXPZfNCRg`; `5j2y3UumtnI` | 2026 | alta (método) |
| A34 | Embutir TACOS-alvo (cerca de 5%, ROAS 20) e perdas (cerca de 1%) no preço | PRÁTICA | `hkL7gO3Tb6w`; `H_QVxVF7FHs` | 2026-09 | média (duas N6) |
| A35 | Kit dilui a taxa fixa e sobe a MC em reais apesar de MC% menor | PRÁTICA (consenso) | `96YaDbhhsAo`; `Zx8826q-qLk`; `hkL7gO3Tb6w` | 2026 | média (B) |
| A36 | Cupom com cesta mínima de cerca de 2× o ticket para puxar ticket médio | PRÁTICA | `96YaDbhhsAo`; `7i2f1rplBl0` | 2026-08 | média (duas N6/N7) |
| A37 | Reajuste em lotes de 5 a 7 anúncios a cada 3 ou 4 dias por sensibilidade do algoritmo | PRÁTICA | `9VOoazXt_aE` | 2026-09-25 | baixa (hipótese) |
| A38 | Margem-alvo: bruta ≥25% a 30% ou MC pós-Ads de 12% a 15% (bases diferentes) | PRÁTICA | `Zx8826q-qLk`; `hkL7gO3Tb6w`; `hEkVpRw_vNg` | 2026 | baixa (faixa) |
| A39 | Comissão "12% a 18%" (Bling) contraria a tabela 2026 | DADO (fraco) | blog.bling.com.br/anunciar-na-shopee | 2025-11-24 | baixa |
| A40 | Líderes de café exibem preço riscado (−5% a −56%) e preço "no Pix"; escada de gramaturas | OBS | `observacao/lideres.md` | 2026-10-14 | média (amostra única) |
| A41 | Vendedores brasileiros: >3 milhões; 95% das vendas feitas por vendedores locais | OFICIAL | `yxG_g8vHZIc` | 2026-08-25 | média |
| A42 | Lojas Oficiais: devolução grátis em 7 dias e cupons exclusivos de frete | OFICIAL | `HC-78029` | s/d (pode estar superada) | média |

---

## 9. Lacunas

1. **Texto oficial da política de comissão.** O artigo do Centro de Educação (seller.shopee.com.br/edu/article/18483; FAQ 7749) não foi lido direto: a página carrega por JS e a API pede login. A tabela das seções 2.1 e 4 depende de praticantes que mostraram o artigo em tela. **Checar no N1** os pontos mais frágeis:
   - a regra de itens abaixo de R$8;
   - a taxa de CPF;
   - o subsídio Pix acima de R$500 ("até 8%");
   - a data do frete grátis obrigatório (março ou maio de 2026).
2. **Taxa de campanha oficial (2% a 3%) e as regras de cada evento.** Só há uma fonte de praticante com tela. Falta a página de regras da campanha (Central de Marketing > Campanhas) com data.
3. **Coparticipação de frete por logística (SPX, Full, Correios, transportadora própria).** Só há um exemplo (25%).
4. **Efeito de promoção em visibilidade e conversão.** Não há estudo público com período, base e holdout para a Shopee Brasil. Também não há como separar o efeito do subsídio da plataforma (Pix, cupons Shopee) do desconto do vendedor. Sem evidência.
5. **Competitividade de preço.** Não foi achado índice par a par ou ponderado publicado, nem métrica oficial de "preço competitivo" na Shopee. O "Assistente de vendas" aparece só como ferramenta de comparação, sem regra de exposição. Não há Buy Box nem catálogo com disputa de preço documentado. Sem evidência de regra de paridade com outros canais.
6. **Reprecificadores com piso na Shopee.** Não foi achada fonte (ferramenta, praticante ou oficial) nesta rodada. A defesa contra guerra de preço achada é kit, gramatura exclusiva, diferenciação por atributo e política comercial.
7. **Benchmarks por categoria** (MC, desconto médio em datas duplas, uplift do 11.11 e do 12.12, ROAS por categoria) para Shopee Brasil: nenhum público com método. Relatórios Neotrust/Confi e NIQ Ebit não foram acessados porque a busca na web estava indisponível. Ebit historicamente excluiu a Shopee (nota de método).
8. **Calendário oficial de 2026 completo**, com datas de inscrição e prazos de nomeação por campanha: só há o post do 10.10 e falas de praticantes.
9. **Alimentos e perecíveis:** não há fonte sobre regras de campanha específicas para validade curta, nem sobre comissão diferente por categoria. Nesta rodada a tabela de 2026 aparece **igual para todas as categorias**; não foi achada exceção por categoria.
10. **Observação direta de preço** (N3) ficou incompleta: a Shopee exigiu login depois da 1ª página (`lideres.md`). Por isso faltam preço mediano da 1ª página, % de anúncios com cupom e % no Pix com amostra maior.

---

## 10. Verificação (2026-10-14)

**Limites da verificação.** A cota de WebSearch se esgotou (nenhuma busca foi executada). O WebFetch de seller.shopee.com.br/edu (artigos 18483 e 7749) devolveu só o título "Seller Education Hub" (página carregada por JS). Só foram lidos direto dois artigos da central de ajuda: help.shopee.com.br/portal/4/article/197770 e /76177 (sem data, "pode estar superada"). Regra adotada: na dúvida, não confirmar. Nenhuma afirmação foi contestada, porque nenhuma fonte oficial lida diz outra coisa.

| id | veredito | fonte oficial (URL) | observação |
|---|---|---|---|
| R1 | SEM FONTE OFICIAL | seller.shopee.com.br/edu/article/18483 (não lido: só título) | Só praticantes com tela. Taxa de R$4,50 e vigência de 01/10 não verificadas. |
| R2 | SEM FONTE OFICIAL | seller.shopee.com.br/edu/article/18483 (não lido) | Faixas e taxas fixas só por praticantes. Regra de plataforma de março de 2026: pode estar superada. |
| R3 | SEM FONTE OFICIAL | seller.shopee.com.br/edu/article/18483 (não lido) | Cobrança por unidade vendida só por praticantes. |
| R4 | SEM FONTE OFICIAL | seller.shopee.com.br/edu/article/18483 (não lido) | Regra do CPF (+R$3 acima de 450 pedidos em 90 dias) só por praticantes. |
| R5 | SEM FONTE OFICIAL | nenhuma localizada | Fonte única de praticante (Zx8826q-qLk). Não usar como regra. |
| R6 | SEM FONTE OFICIAL | help.shopee.com.br/portal/4/article/197770 (lido) | O artigo confirma só o lado do comprador: Pix só em itens com a tag "no Pix", soma com cupons e moedas, não incide sobre frete. Não traz percentuais (5% e 8%), faixas nem quem paga. O repasse igual ao vendedor segue sem fonte oficial. |
| R7 | SEM FONTE OFICIAL | nenhuma localizada | Frete grátis obrigatório, tetos R$20/30/40, coparticipação de 25% e a data (março ou maio) seguem só por praticantes e blogs. |
| R8 | SEM FONTE OFICIAL | nenhuma localizada | Taxa de campanha de 2% a 3% e renovação automática: uma única praticante (4oQLk8XXYP4). |
| R9 | SEM FONTE OFICIAL | nenhuma localizada | Regras de uma campanha específica, vistas em tela de praticante. Valem como exemplo, não como regra geral. |
| R10 | CONFIRMADA (parcial) | help.shopee.com.br/portal/4/article/76177 (lido, s/d) | O artigo confirma que se combina um cupom da Shopee com um cupom de vendedor, que não se usa mais de um de cada tipo e que cupom de loja e de produto não se combinam. Não verificado: o cupom de frete como terceiro e a ordem de aplicação (vendedor primeiro). Artigo sem data, pode estar superado. |
| R11 | SEM FONTE OFICIAL | nenhuma localizada | Vídeo do canal Shopee Brasil (0oRYednAlHY), mas a página oficial do Full+ não foi lida. |
| R12 | SEM FONTE OFICIAL | nenhuma localizada | Vídeos do canal Shopee Brasil (fqDYuDPJsEg, MfH07p4ZtT4); política escrita de preço não lida. O limite de 4 vezes veio de áudio e transcrição. |

**Pendência.** Pontos críticos para uma nova rodada, com busca ou navegador: texto do artigo 18483, política de preço da Central do Vendedor e regras de campanha.

## 11. Verificação pelo navegador (2026-10-15)

Lido no Chrome (as páginas carregam por JavaScript): Centro de Educação do Vendedor (seller.shopee.com.br/edu) e FAQ do Shopee Ads (ads.shopee.com.br/learn/faq). Sem login e sem captcha. Tabelas em imagem foram lidas por captura de tela.

| id | veredito | fonte oficial | observação |
|---|---|---|---|
| R1 | CONFIRMADA | https://seller.shopee.com.br/edu/article/18483 (01-03-2026 (atualizado em 01/10/2026)) | Até R$79,99: 20% + R$4,50 desde 01/10/2026. |
| R2 | CONFIRMADA | https://seller.shopee.com.br/edu/article/18483 (01-03-2026 (atualizado em 01/10/2026)) | Faixas da tabela (imagem): R$80 a R$99,99 = 14% + R$16; R$100 a R$199,99 = 14% + R$20; R$200 a R$499,99 = 14% + R$26; acima de R$500 = 14% + R$26. |
| R3 | CONFIRMADA | https://seller.shopee.com.br/edu/article/18483 (01-03-2026 (atualizado em 01/10/2026)) | Cobrança por item. Não é cobrada em cancelamentos nem em devoluções com retorno do produto. |
| R4 | CONFIRMADA | https://seller.shopee.com.br/edu/article/18484 (01-03-2026) | Vale para CPF com mais de 450 pedidos em 90 dias. |
| R5 | CONFIRMADA | https://seller.shopee.com.br/edu/article/18483 (01-03-2026 (atualizado em 01/10/2026)) | Agora há fonte oficial; a fonte única de praticante deixa de ser a base. |
| R6 | CONFIRMADA | https://seller.shopee.com.br/edu/article/18483 (01-03-2026 (atualizado em 01/10/2026)) | De R$80 a R$499,99: 5%. Acima de R$500: 'até 8%'. O vendedor recebe o mesmo valor, ou seja, o subsídio não sai dele. Para acima de R$500 o texto diz 'até 8%', não 8% fixo. |
| R7 | PARCIAL | https://seller.shopee.com.br/edu/article/23431; https://seller.shopee.com.br/edu/article/25794 (16-03-2026; 24-04-2026) | Confirmados: todos os vendedores no programa, tetos dos cupons de R$20/R$30/R$40 por faixa e coparticipação de 25% só para logística própria (teto de R$10). O fim do adicional de 6% e a data exata não aparecem. O cupom pode ser limitado se houver penalidades ativas. |
| R8 | SEM FONTE OFICIAL | https://seller.shopee.com.br/edu/article/11533; https://seller.shopee.com.br/edu/article/3757 (04-04-2025; 14-08-2025) | Os artigos oficiais sobre Campanhas Oficiais não citam taxa de 2% a 3% nem renovação automática. A busca 'taxa de campanha' no Centro de Educação não trouxe nada sobre isso. |
| R9 | SEM FONTE OFICIAL | https://seller.shopee.com.br/edu/article/11533; https://seller.shopee.com.br/edu/article/3757 (04-04-2025; 14-08-2025) | As regras da campanha específica (desconto de 5% ou mais, preço de R$19 ou mais, 5 unidades ou mais) não aparecem nos artigos gerais. Valem como exemplo de tela. |
| R10 | PARCIAL | https://help.shopee.com.br/portal/4/article/76177; https://seller.shopee.com.br/edu/article/2621 (s/d; 14-08-2025) | Mantém a leitura anterior (um cupom da Shopee + um do vendedor). O cupom de frete como terceiro e a ordem de aplicação não aparecem; o 2621 não trata de combinação de cupons. |
| R11 | CONFIRMADA | https://seller.shopee.com.br/edu/article/27600 (19-05-2026) | Full+: pelo menos 40% dos pedidos via Full. Entre 40% e 70%: 0,5 p.p. em itens de R$50 a R$79,99 (as faixas maiores vão até 2 p.p.). Crédito na carteira na 1ª semana do mês seguinte. |
| R12 | CONFIRMADA | https://seller.shopee.com.br/edu/article/2618; https://seller.shopee.com.br/edu/article/2637 (08-08-2025; 15-10-2025) | Desconto enganoso (subir o preço antes da promoção) é proibido. Variações com diferença acima de 4x podem ser consideradas spam de preço. |
