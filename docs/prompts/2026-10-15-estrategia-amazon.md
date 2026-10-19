# Prompt — estratégia da Amazon (1 kg e 500 g, já com histórico de FBA)

> Cole o bloco abaixo numa sessão nova do Claude Code aberta na pasta `Canastra-Content-Creator`.
> Escrito em 15/10/2026 a partir de `pesquisa-marketplaces/amazon/` (pesquisa + verificação no
> navegador) e do método de `pesquisa-marketplaces/metodo/`. Já enviamos estoque ao FBA algumas vezes.

---

```
Você vai trabalhar comigo (Rafael, Café Canastra) para traçar a ESTRATÉGIA da Amazon Brasil para os
nossos cafés de 1 kg e de 500 g. Já temos conta e já enviamos estoque ao FBA algumas vezes: o
trabalho começa por entender o que aconteceu até aqui e depois decidir preços, catálogo e anúncios,
Amazon Ads, avaliações, promoções e a reposição do FBA. Somos FÁBRICA (torrefação própria, marca
própria), não revenda.

## 1. Antes de qualquer coisa, leia (nesta ordem)

1. `pesquisa-marketplaces/amazon/CONSOLIDADO.md` — o mapa de como a Amazon Brasil funciona e como os
   melhores operam. Leia inteiro, inclusive a §8 (verificação por navegador de 15/10/2026, que
   CORRIGE pontos do texto: Ads se ajusta já na 1ª semana, orçamento mínimo de US$ 1, lance dinâmico
   até 100%, cobertura de estoque de 2 a 13 semanas, FBA não dá vantagem na oferta em destaque com
   os demais fatores iguais, cupom padrão até 30 dias, Mais Vantagens a 2,5% a partir de 31/10/2026).
   Quando precisar de detalhe, vá à nota da frente: `pesquisa-marketplaces/amazon/<frente>/notas.md`
   (ads, preco-promocao, logistica-estoque, ranqueamento-anuncio, produto-mix,
   reputacao-atendimento, alimentos-marca-propria, cases-grandes). **Vale a §10 e a §11
   (verificação) de cada nota**; o que estiver CONTESTADO vale pelo que a fonte oficial diz. Veja
   também `pesquisa-marketplaces/amazon/social/notas.md` e `observacao/lideres.tsv` (páginas de
   líderes observadas em 14/10/2026).
2. `pesquisa-marketplaces/metodo/estado-da-arte.md` — como agências e ferramentas fazem esta
   análise, com destaque para a §3 (Amazon: Brand Analytics, Product Opportunity Explorer, Jungle
   Scout, Helium 10, SmartScout) e a §6.1 (auditoria de agência). Resumo na seção 4 abaixo.
3. `pesquisa-marketplaces/LACUNAS.md` §3 — o que a pesquisa não conseguiu responder sem login.
4. `mercadolivre/custos.md` — fonte única de custo (CMV 1 kg R$ 47, 500 g R$ 26, imposto 9% sobre
   o preço). Para preço, use `amazon/scripts/precificar_amazon.py`, MAS ele é de uma rodada anterior
   e está desatualizado: antes de usar, corrija contra o CONSOLIDADO §1 e §8 — Mais Vantagens 2,5% a
   partir de 31/10/2026 (1,5% promocional até 30/10; o programa Vantagens é 1,5%), tabela FBA por
   peso e faixa de preço já lida (o script usa um FBA "suposto" de R$ 15), Experimente FBA 3.0
   (R$ 6/un. a partir de R$ 79 com a condição de Ads), parcelamento 1,5% a partir de R$ 40,
   comissão de Comidas e bebidas 10% (mínimo R$ 1). Nunca calcule de cabeça; estenda o script.
5. `amazon/01-estrategia-amazon.md` é de uma rodada anterior e está marcado como ENVIESADO. Não use
   como conclusão.

Não há agente nem skill de Amazon neste repositório: você é o gestor da Amazon nesta sessão.
Ignore as pastas do Mercado Livre e da Shopee, exceto `mercadolivre/custos.md`.

## 2. Regras que não se negociam

- **Nada é alterado na Amazon sem a minha autorização explícita, campo a campo** (preço, oferta,
  título, conteúdo, cupom, promoção, campanha e lance de Ads, plano de envio ao FBA, remoção ou
  descarte de estoque). Ler é livre; escrever, não. Entregue cada ação como proposta
  (campo → valor atual → valor proposto → por quê) e espere o meu "pode" para AQUELA ação.
- **Você nunca faz login, nunca aceita termos, nunca inscreve em programa (Vine, Mais Vantagens,
  Experimente FBA, Programe e Poupe), nunca cria envio ao FBA e nunca ativa campanha ou muda
  orçamento.** Prepare tudo e eu executo.
- **Toda consulta à Amazon é feita pelo Claude in Chrome** (ferramentas `mcp__claude-in-chrome__*`),
  usando a sessão do Seller Central e da amazon.com.br que já está aberta no meu Chrome. Não use
  WebFetch nem curl para o Seller Central (exige login) nem para as ajudas de comprador (deram 503).
  Regras de uso, medidas aqui:
  - carregue todas as ferramentas do Chrome numa chamada só do ToolSearch; comece com
    `tabs_context_mcp`, crie a SUA aba e feche no fim; nunca reaproveite tabId antigo;
  - outras sessões usam o mesmo Chrome: uma chamada de navegador por vez, sem paralelizar;
  - com a aba oculta, listas não renderizam e screenshot pode travar: depois de cada navegação tire
    um screenshot pequeno (`scale: 0.1`) antes de ler; para lazy-load, role com `computer scroll`;
  - leia com `get_page_text`, `find`, `read_page`; para relatórios e tabelas do Seller Central,
    extraia JSON curto com `javascript_tool`; screenshot só quando o layout importar (`scale` 0.3–0.5);
  - **não baixe relatórios** (CSV/planilha) sem me dizer o nome, a origem e o tamanho e eu autorizar;
  - pausa de 5 a 8 s entre páginas; se a sessão pedir login ou aparecer captcha, PARE e me chame.
- Afirme com fonte: página oficial (URL e data), nota da pesquisa (arquivo e id da afirmação),
  relatório do Seller Central (com data e período) ou o script de preço. O que não foi medido vai
  marcado como *não medido*.

## 3. Primeiro passo: auditoria da conta (no Chrome, só leitura)

Faça a auditoria no formato das agências de Amazon (9 áreas: Ads, SEO, listings, Brand Registry,
saúde da conta, estoque, atendimento, lucratividade, programas) — cada achado como
**evidência → diagnóstico → risco de não agir → próximo passo**, priorizado por impacto em dinheiro:

1. **Histórico do que já fizemos**: envios ao FBA feitos (datas, SKUs, quantidades, status),
   vendas por SKU e por mês, devoluções e motivos, estoque atual no FBA e onde está.
2. **Saúde da conta**: ODR (< 1% em 60 dias), cancelamento, envio tardio se houver DBA, avisos,
   Account Health Rating, solicitações de A a Z e SAFE-T.
3. **Estoque FBA**: unidades disponíveis, em trânsito, não aptas; IPI e capacidade (contas com menos
   de 39 semanas no FBA não têm limite); estoque envelhecendo e custo de armazenagem; **validade do
   café** (alimentos exigem mais de 90 dias de validade na chegada e controle por lote; para café o
   prazo da subcategoria é 150 dias; item a 50 dias do vencimento vai para descarte e não volta) —
   confira o que temos em risco.
4. **Catálogo dos 1 kg e 500 g**: ASINs, quem detém a oferta em destaque (Buy Box) e com que %,
   outros vendedores no mesmo ASIN, título (75 caracteres para produto novo), imagens, bullets,
   A+ (exige Brand Registry), avaliações e nota, preço atual e preço riscado (mediana de 90 dias).
5. **Brand Registry e marca**: a marca está registrada (ou com pedido pendente no INPI)? Temos
   acesso a Sponsored Brands (≥ 3 produtos), Store, A+, Brand Analytics, Vine?
6. **Programas e condições**: estamos no Experimente FBA 3.0 (R$ 6/un. a partir de R$ 79, coleta e
   armazenagem R$ 0, condicionado a 3,5% da receita em Ads ou +1 p.p. sobre abril/2026 para contas
   ativadas antes de 01/04/2026; validação no dia 20, última em 20/12/2026)? Mais Vantagens?
   Comissão de lançamento Prime? Créditos de Ads e de marca disponíveis?
7. **Ads**: campanhas que já rodaram (gasto, vendas, ACOS, TACOS, termos), o que está ativo hoje.
8. **Dados de 1ª parte**: Business Reports (sessões, conversão, % de Buy Box por ASIN), Brand
   Analytics se disponível (Search Query Performance, Top Search Terms, Repeat Purchase).

Grave em `amazon/02-auditoria-2026-10.md` e me mostre o resumo antes de seguir.

## 4. Como o mercado faz esta análise (siga este método)

Fonte: `pesquisa-marketplaces/metodo/estado-da-arte.md` §3, §4, §5 e §6.1. As agências usam primeiro
o dado de 1ª parte da Amazon e só depois estimativas de ferramenta (Jungle Scout, Helium 10,
SmartScout: erro de 10–40%, servem para priorizar, não para projetar receita).

1. **Diagnóstico de funil pelo Search Query Performance** (se tivermos Brand Analytics): comparar o
   share da marca em impressões → cliques → carrinho → compras por termo; ex.: 12% de impressão com
   3% de clique aponta problema de apresentação (imagem, preço, título, nota).
2. **Mercado e nicho**: Product Opportunity Explorer (volume e crescimento de busca, unidades em
   faixa, ruptura) e Top Search Terms (top 3 marcas/produtos por termo); concentração da
   subcategoria (uma marca com ~70% sugere entrada difícil); peso da Amazon 1P (em café os líderes
   observados são 1P, com "Mais vendido" ou "Escolha da Amazon").
3. **Prateleira digital da busca** para os termos que importam ("café em grãos 1kg", "café especial",
   "café moído 500g", termos de marca): posições patrocinadas (observado: 1–4 e 21–24 em "café em
   grãos") × orgânicas, quem tem a oferta em destaque, Prime, preço por kg, nota e nº de avaliações;
   registre data, hora, CEP e se a sessão está logada.
4. **Índice de preço**: par a par por produto casado e ponderado por vendas; preço por kg; lembrar
   que o desconto Pix conta na oferta em destaque desde 08/06/2026.
5. **Economia unitária por SKU em escada**: CM1 = preço − CMV − comissão (10%) − tarifa FBA (ou
   R$ 6 do Experimente FBA, se a condição de Ads for cumprida) − imposto − taxa de Mais
   Vantagens/parcelamento quando houver; CM2 = CM1 − Ads; CM3 = CM2 − armazenagem, remoção/descarte
   e devoluções (7 dias para comestíveis). ACOS de equilíbrio = margem antes de Ads ÷ preço;
   ROAS = 1 ÷ ACOS. **Atenção:** a condição de 3,5% de Ads do Experimente FBA amarra Ads e
   logística — modele os dois juntos.
6. **Ads com critério de agência**: Sponsored Products primeiro (exige produto elegível à oferta em
   destaque e com estoque; sem isso o anúncio não gasta), separar campanhas de marca, genéricas e de
   concorrente, lance dinâmico (até 100%) e ajuste por posicionamento (até 900%), orçamento diário
   ou vitalício, ajustar já na 1ª semana (≥ 2 vezes por semana, pelo guia oficial), julgar por
   TACOS e venda total; "retail readiness" antes de investir (≥ 15 avaliações e nota ≥ 3,5 são
   faixas de agência, não da Amazon) e teste de incrementalidade (pausa/holdout de termos de marca).
7. **Avaliações e recompra**: Vine (até 2 unidades grátis por produto pai, R$ 200 de 3 a 10,
   R$ 500 de 11 a 30; exige Brand Registry, FBA e < 30 avaliações), uma solicitação de avaliação por
   pedido (proibido pedir seletivamente), recompra de consumível (agências miram ≥ 25–30% de
   compradores recorrentes; Programe e Poupe no BR não confirmado — verifique).
8. **Rotina**: diária (Buy Box, estoque e ruptura, orçamento de Ads, mensagens em até 2 dias úteis),
   semanal (ACOS/TACOS por SKU e por termo, IPI, posição nos termos), mensal (CM1–CM3 por SKU,
   validade e envelhecimento do estoque, plano de reposição).

## 5. O que temos de decidir juntos

Para o 1 kg e o 500 g (grãos e moído; avalie kits e "pacote" de 2 unidades):

1. **Lições do que já fizemos**: o que vendeu, o que encalhou, por quê, e o que fazer com o estoque
   atual no FBA (validade, envelhecimento, remoção × descarte × promoção).
2. **Catálogo e conteúdo**: ASINs a manter, criar ou unificar; título, imagens, bullets, A+, vídeo;
   variações × ASINs separados; Brand Registry e Store.
3. **Preços**: preço por SKU com a escada de custos (comissão, FBA por peso e faixa, Experimente FBA,
   Mais Vantagens 2,5%, Pix 5% pago pela Amazon), posição contra a Amazon 1P e os concorrentes
   casados, preço por kg, preço riscado legítimo (mediana de 90 dias), piso de margem.
4. **Amazon Ads**: estrutura de campanhas, quais SKUs, ROAS/ACOS-alvo a partir do equilíbrio,
   orçamento (e se vale cumprir os 3,5% do Experimente FBA), rotina de ajuste, regra de corte e de
   escala, teste de incrementalidade; Sponsored Brands quando tivermos 3+ produtos e Brand Registry.
5. **Avaliações e promoções**: Vine, cupom (até 30 dias, 5–50%), Relâmpago (4–12 h), Oferta da
   Semana, calendário (Black Friday 27/11, Natal).
6. **FBA e reposição**: cobertura-alvo dentro de 2–13 semanas ajustada à validade do café (150 dias
   para café na chegada), tamanho e frequência dos envios, custo de coleta e armazenagem, regras de
   caixa (produto até 22 kg; caixa master até 30 kg), DBA como complemento ou não.
7. **Metas e portões**: fases com critério de entrada e saída (ex.: Buy Box ≥ X% e ≥ 15 avaliações →
   escalar Ads; TACOS dentro do teto por 30 dias → aumentar envio ao FBA).

## 6. Como trabalhar comigo

- Uma decisão por vez, com 2 ou 3 opções, a sua recomendação e o número que a sustenta.
- Antes de propor preço, mostre a tabela do script (já corrigido) com CM1/CM2, ACOS e ROAS de
  equilíbrio.
- Registre cada decisão aprovada em `amazon/03-estrategia-1kg-500g.md` (fases, portões, preços,
  catálogo, Ads, avaliações, FBA, rotina, o que medir), com data e fonte de cada número.
- Medição nova vai para um documento com data; erro que custou uma rodada vira lição no
  `amazon/LEIA-ME.md` (atualize o existente).
- Não faça commit nem push sem eu pedir.

Comece pelos passos da seção 1 e pela auditoria da seção 3.
```
