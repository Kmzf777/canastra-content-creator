# Prompt — estratégia final do Mercado Livre (1 kg e 500 g)

> Cole o bloco abaixo numa sessão nova do Claude Code aberta na pasta
> `Canastra-Content-Creator`. Escrito em 15/10/2026, a partir da pesquisa
> `pesquisa-marketplaces/mercadolivre/` (versão final) e do método de `pesquisa-marketplaces/metodo/`.

---

```
Você vai trabalhar comigo (Rafael, Café Canastra) para traçar a ESTRATÉGIA FINAL do Mercado Livre
para os nossos cafés de 1 kg e de 500 g: como organizar preços, como montar e estruturar os
anúncios, como usar o Mercado Ads e qual o caminho até vendermos o suficiente para liberar o Full.
Somos FÁBRICA (torrefação própria, marca própria), não revenda.

## 1. Antes de qualquer coisa, leia (nesta ordem)

1. `.claude/agents/mercadolivre.md` — o seu papel de gestor do ML. Siga-o como instrução própria
   nesta sessão (não o dispare como subagente). Carregue as skills que ele indica por tarefa:
   `canastra-mercadolivre` (operar o painel), `canastra-ml-precificacao`, `canastra-ml-concorrencia`,
   `canastra-ml-anuncio`, `canastra-ml-ads`.
2. `pesquisa-marketplaces/mercadolivre/CONSOLIDADO.md` — o mapa final de como o ML funciona e como
   os melhores operam (versão final de 15/10/2026). É a base de conhecimento desta estratégia.
   Quando precisar de detalhe, vá à nota da frente: `pesquisa-marketplaces/mercadolivre/<frente>/notas.md`
   (frentes: ads, preco-promocao, logistica-estoque, ranqueamento-anuncio, produto-mix,
   reputacao-atendimento, alimentos-marca-propria, cases-grandes). **Vale sempre o estado final da
   §12 de cada nota**; o que estiver CONTESTADO vale pelo que a fonte oficial diz.
3. `pesquisa-marketplaces/metodo/estado-da-arte.md` — como agências, consultorias e ferramentas
   fazem esse tipo de análise (é o método que você vai seguir; resumo na seção 4 abaixo).
4. `pesquisa-marketplaces/LACUNAS.md` §1 — o que a pesquisa não conseguiu responder sem acesso
   logado de vendedor. Várias dessas respostas você vai buscar no painel (seção 3).
5. `mercadolivre/custos.md` — fonte única de custo (CMV 1 kg R$ 47, 500 g R$ 26, imposto 9% sobre
   o preço) e `mercadolivre/scripts/precificar.py` (rode `--conferir` no início; todo cálculo de
   preço sai dele, nunca de conta de cabeça).
6. `mercadolivre/LEIA-ME.md` (estado da conta, erros já corrigidos). Os documentos
   `mercadolivre/14-estrategia-1kg.md`, `15-preco-1kg-suave-classico.md` e `16-estrategia-competir.md`
   são de uma rodada anterior: use como MEDIÇÕES históricas da nossa conta (preços, fretes,
   concorrência de 08/10), não como conclusão — o 16 está marcado como enviesado.

Ignore `shopee/`, `amazon/` e `pesquisa-marketplaces/shopee|amazon` nesta sessão.

## 2. Regras que não se negociam

- **Nada muda na conta do ML sem a minha autorização explícita, campo a campo.** Autorizar preço
  não autoriza título. Ler é livre; escrever, não. Entregue cada mudança como proposta
  (campo → valor atual → valor proposto → por quê) e espere o meu "pode" para AQUELE campo.
- Nunca, nem com autorização genérica: reativar ou excluir anúncio, ativar campanha ou mudar verba
  de Ads, depositar garantia, enviar estoque ao Full, aceitar termos. Prepare e me entregue o passo a passo.
- **Toda consulta ao Mercado Livre é feita pelo Claude in Chrome** (ferramentas
  `mcp__claude-in-chrome__*`), na sessão que já está logada no meu Chrome. Não use WebFetch, curl
  nem a API pública para o ML (dão 403 ou dado incompleto). Regras de uso, medidas aqui:
  - carregue todas as ferramentas do Chrome numa chamada só do ToolSearch; comece com
    `tabs_context_mcp`, crie a SUA aba e feche no fim; nunca reaproveite tabId antigo;
  - outras sessões usam o mesmo Chrome: uma chamada de navegador por vez, sem paralelizar;
  - com a aba oculta, listas não renderizam e screenshot pode travar: depois de cada navegação tire
    um screenshot pequeno (`scale: 0.1`) antes de ler; para lazy-load, role com `computer scroll`
    (não `scrollTo` via JS);
  - leia com `get_page_text`, `find` e `read_page` (com `filter`/`depth`); para listas, extraia JSON
    curto com `javascript_tool` e acumule em `localStorage` quando forem muitas páginas;
    screenshot só quando o layout importar, com `scale` 0.3–0.5;
  - pausa de 6 a 10 s entre páginas do ML; se aparecer captcha ("Segurança — Mercado Livre"),
    PARE e me chame — nunca resolva captcha, nunca faça login;
  - para EDITAR um anúncio (só depois do meu "pode"), siga a receita da skill
    `canastra-mercadolivre` (clique triplo, nunca Ctrl+A; confira na lista de anúncios, não no toast).
- Afirme com fonte: número medido no painel (com data), na pesquisa (arquivo e id da afirmação)
  ou no `precificar.py`. O que não foi medido vai marcado como *não medido*.

## 3. Primeiro passo: diagnóstico da conta (no Chrome, só leitura)

Faça uma auditoria no formato que as agências usam — cada achado como
**evidência → diagnóstico → risco de não agir → próximo passo**, priorizado por impacto em dinheiro:

1. **Reputação e saúde**: cor, as três métricas (reclamações, cancelamentos, envios incorretos) com
   a janela atual (101 vendas em 60 dias desde 10/09, senão 365 dias), pedidos afetados e a causa de
   cada um, experiência de compra por anúncio, Reputação Protegida/benefício disponível.
2. **Anúncios de 1 kg e 500 g** que existem hoje (ativos e pausados): preço, tipo (Clássico/Premium),
   forma de envio, frete que pagamos no formulário (o formulário mostra o custo exato ao trocar o
   preço), estoque, prazo de disponibilidade, qualidade da publicação, visitas, conversão e vendas.
3. **Ads**: a conta consegue criar Product Ads hoje? (requisitos: reputação amarela ou melhor, sem
   dívida, anúncio ativo; há divergência entre texto e webinar — veja `ads/notas.md` §12). Qual o
   ROAS recomendado e o CPC de café? Qual a janela de atribuição que o painel mostra?
4. **Full**: a conta pode enviar ao Full hoje? O que o painel pede para habilitar (reputação, volume,
   convite, categoria)? O café entra em Supermercado/Full Super? Algum item nosso está na lista
   restrita a autorizados? (a pesquisa não achou critério público de liberação do Full — descubra no
   painel e registre exatamente o que ele exige).
5. **Painel "Métricas > Análise de mercado"** (Concorrência e Oportunidades) para as categorias de
   café em grãos e moído: ranking de vendedores, % de uso de Full, Ads, frete grátis, cupom,
   Premium, catálogo; tendência e sazonalidade; top 100 anúncios. Se o detalhe estiver bloqueado
   por falta de vendas na categoria, registre o requisito que o painel mostra.
6. **Central de Promoções e cupons**: o que está disponível para a nossa cor de reputação.
7. Preço dos mesmos produtos nos nossos outros canais (o ML não pode ser o mais caro: há relato de
   punição e as cofinanciadas comparam preço externo).

Grave o diagnóstico em `mercadolivre/17-diagnostico-2026-10.md` e me mostre o resumo antes de seguir.

## 4. Como o mercado faz esta análise (siga este método)

Fonte: `pesquisa-marketplaces/metodo/estado-da-arte.md`. Cruze sempre quatro camadas: dado do
painel do ML (mais confiável para a nossa conta), estimativa de ferramenta (só para priorizar,
erro de 10–40%), prateleira digital (observação da busca) e estudos/balanços.

1. **Análise de mercado** (como as consultorias leem o painel oficial e a Nubimetrics): teto da
   categoria e tendência, crescimento × saturação (nº de vendedores e de MercadoLíderes Gold/Platinum),
   sazonalidade, quem lidera e com quais alavancas. Fonte gratuita complementar:
   tendencias.mercadolivre.com.br.
2. **Prateleira digital da busca** (método da indústria, Profitero/Lett) para os termos que
   importam (ex.: "café em grãos 1kg", "café especial 1kg", "café moído 500g", "café torrado e moído",
   e os termos da nossa marca): **share of search orgânico × patrocinado** (no ML o patrocinado tem o
   rótulo "Ad" e cai nas posições 1–4 e 13–16; seletor `a.poly-component__ads-promotions` /
   `aria-label="Patrocinado"`), % Full/Full Super, frete grátis, loja oficial, nota e vendidos,
   **content score** dos líderes (fotos, vídeo/clips, ficha técnica, título), e **disponibilidade**.
   Registre data, hora, termo e se a sessão está logada.
3. **Análise da 1ª página** (adaptada do método Avantpro para marca própria): para cada termo,
   quantos resultados, quantos vendedores distintos, quantos no Full, em promoção, patrocinados,
   catálogo; idade do anúncio × vendas acumuladas dos líderes. Para fábrica, o que importa não é
   achar "quem não tem Full", é onde a nossa oferta (frescor, origem, preço por kg, kit) ganha.
4. **Índice de preço**: par a par (nosso preço ÷ preço do concorrente × 100) por produto casado
   (mesmo peso, tipo, torra), e o índice da categoria ponderado por vendas/visitas — não use média
   simples. Compare preço por kg.
5. **Economia unitária por SKU em escada** (como as agências fazem): CM1 = preço − CMV − tarifa −
   frete/fulfillment − imposto; CM2 = CM1 − Ads; CM3 = CM2 − devoluções e armazenagem.
   **ACOS de equilíbrio = margem antes de Ads ÷ preço; ROAS de equilíbrio = 1 ÷ ACOS.** Tudo pelo
   `precificar.py` (se faltar um cenário, estenda o script em vez de calcular à mão).
6. **Ads com critério de agência**: verba derivada da margem (TACOS ≤ uma fração da margem), julgar
   por TACOS e venda total, não só ROAS; separar termo de marca de termo genérico; "retail
   readiness" antes de investir (anúncio completo, estoque, reputação); e prever um **teste de
   incrementalidade** (pausa ou holdout medindo a venda total) — a literatura mostra que a
   atribuição superestima o Ads (`CONSOLIDADO.md` §7).
7. **Rotina** (cadência que os profissionais usam, `estado-da-arte.md` §6.3): diária (ruptura,
   preço do concorrente direto, orçamento de Ads, pedidos atrasados), semanal (ACOS/ROAS/TACOS por
   SKU, posição e share nos termos, reputação), mensal (share × crescimento da categoria, CM1–CM3 por
   SKU, sazonalidade do próximo trimestre).

## 5. O que temos de decidir juntos (a estratégia final)

Para o 1 kg e o 500 g (grãos e moído; avalie também kit 2 × 1 kg e kit 2 × 500 g "1 kg"):

1. **Portfólio e anúncios**: quais SKUs entram, quantos anúncios, anúncio separado × variação,
   kit como anúncio próprio, Clássico × Premium por faixa de preço, catálogo e loja oficial (marca
   registrada INPI classe 30), título/ficha/fotos/clips com o padrão dos líderes.
2. **Preços**: preço de lista e preço de campanha por SKU, escada de preço por kg (avulso → kit),
   degraus de envio (R$ 19/49/79/100/120/150/200) que mudam a margem, desconto Pix/atacado,
   posição no índice de preço contra os concorrentes casados, piso de margem por SKU.
3. **Mercado Ads**: quando ligar (pré-requisitos), quais SKUs, estrutura de campanha (o ML recomenda
   15 a 30 produtos por campanha; com poucos SKUs, decida), ROAS objetivo a partir do equilíbrio,
   orçamento diário, regra de corte e de escala, teste de incrementalidade.
4. **Promoções e cupons**: o que usar enquanto a reputação não libera a Central, e depois;
   calendário (Black Friday 27/11; Natal).
5. **Logística até o Full**: como despachar sem atraso agora (prazo de disponibilidade real,
   horário de corte, coleta/agência/Flex), **qual meta de vendas e de reputação precisamos atingir
   para liberar o Full** (com o critério que você levantou no painel), e o plano do primeiro envio
   (SKUs, tamanho do lote pela validade do café e pela cobertura de 15–30 dias, Full × Full Super,
   custos lidos: armazenagem, estoque antigo em 2 meses no Supermercado, retirada × descarte).
6. **Metas e portões**: fases com critério de entrada e saída (ex.: reputação amarela → ligar Ads;
   N vendas/semana com envio limpo → primeiro lote no Full), e os indicadores da rotina.

## 6. Como trabalhar comigo

- Uma decisão por vez, com 2 ou 3 opções, a sua recomendação e o número que a sustenta.
- Antes de propor preço, mostre a tabela do `precificar.py` com CM1/CM2, ACOS e ROAS de equilíbrio.
- Registre cada decisão aprovada em `mercadolivre/18-estrategia-final-1kg-500g.md` (fases, portões,
  preços, anúncios, Ads, logística, rotina, o que medir), com data e com a fonte de cada número.
- Medição nova vai para o documento do tema com data; erro que custou uma rodada vira lição no
  `mercadolivre/LEIA-ME.md`.
- Não faça commit nem push sem eu pedir.

Comece pelos passos da seção 1 e pelo diagnóstico da seção 3.
```
