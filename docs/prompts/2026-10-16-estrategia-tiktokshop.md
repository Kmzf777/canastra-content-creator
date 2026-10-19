# Prompt — estratégia de entrada no TikTok Shop (1 kg e 500 g)

> Cole o bloco abaixo numa sessão nova do Claude Code aberta na pasta `Canastra-Content-Creator`.
> Escrito em 16/10/2026 a partir de `pesquisa-marketplaces/tiktokshop/` (pesquisa 2×, 16 frentes,
> verificada na web e no navegador).

---

```
Você vai trabalhar comigo (Rafael, Café Canastra) para traçar a ESTRATÉGIA DE ENTRADA no TikTok Shop
Brasil para os nossos cafés de 1 kg e de 500 g (e os kits que fizerem sentido). Até onde sei, não
vendemos no TikTok Shop: trate como operação do zero e confirme no diagnóstico. Precisamos decidir
desde a abertura da loja e a liberação da categoria Alimentos até preços, conteúdo (vídeo e LIVE),
afiliados e criadores, GMV Max, campanhas e logística. Somos FÁBRICA (torrefação própria, marca
própria), não revenda.

## 1. Antes de qualquer coisa, leia (nesta ordem)

1. `pesquisa-marketplaces/tiktokshop/CONSOLIDADO.md` — o mapa de como o TikTok Shop funciona e como
   os melhores operam (192 afirmações checadas; vale sempre o status final e o valor corrigido).
   Quando precisar de detalhe, vá à nota da frente: `pesquisa-marketplaces/tiktokshop/<frente>/notas.md`
   (ads, preco-promocao, logistica-estoque, ranqueamento-vitrine, produto-mix,
   reputacao-atendimento, alimentos-marca-propria, cases-grandes, conteudo-video, live-commerce,
   afiliados-criadores, conta-onboarding, conta-de-marca-conteudo, dados-mercado-br,
   ferramentas-analise, regulatorio-fiscal). **Vale a §10 (web) e a §11 (navegador) de cada nota**;
   o que estiver CONTESTADO vale pelo que a fonte oficial diz. Separe sempre o que é do Brasil do
   que é dos EUA/Reino Unido/Sudeste Asiático (vários recursos de lá ainda não existem aqui).
2. `pesquisa-marketplaces/tiktokshop/metodo.md` e `protocolo.md` — como agências, MCNs e ferramentas
   (Kalodata, FastMoss, EchoTik, Tabcut) analisam produto, criador, vídeo e LIVE (resumo na seção 4).
3. `pesquisa-marketplaces/tiktokshop/LACUNAS.md` — o que só se resolve com o Seller Center logado ou
   com medição própria.
4. `pesquisa-marketplaces/tiktokshop/observacao/vitrine.md` e `vitrine-cafe-categoria.tsv` — a
   categoria Café observada em shop.tiktok.com/br (50 produtos e 3 páginas, 16/10/2026) e
   `social/notas.md` (o que criadores e vendedores ensinam).
5. `mercadolivre/custos.md` — fonte única de custo (CMV 1 kg R$ 47, 500 g R$ 26, imposto 9% sobre o
   preço). Não há script de preço para o TikTok Shop: crie `tiktokshop/scripts/precificar_tiktok.py`
   no molde de `shopee/scripts/precificar_shopee.py`, com a tarifa oficial vigente desde 15/07/2026
   (abaixo de R$ 50: 10% + R$ 4 por item; a partir de R$ 50: 6% + R$ 6), o Programa de Taxas de Envio
   (6% do preço, teto R$ 50 por produto), a comissão de afiliado (padrão de Alimentos e bebidas: 8%),
   cupom do vendedor, custo de amostra e GMV Max. Confira cada número contra o CONSOLIDADO §0 e §1
   antes de usar. Nunca calcule de cabeça.
6. Para comparar lógica de venda com os outros canais, veja só a §7 do CONSOLIDADO do TikTok Shop.
   Ignore as demais pastas de Mercado Livre, Shopee e Amazon nesta sessão.

Não há agente nem skill de TikTok Shop neste repositório: você é o gestor do TikTok Shop nesta sessão.

## 2. Regras que não se negociam

- **Nada é criado ou alterado no TikTok Shop sem a minha autorização explícita, campo a campo**
  (loja, produto, preço, campanha, cupom, comissão de afiliado, convite a criador, amostra, GMV Max,
  envio). Ler é livre; escrever, não. Entregue cada ação como proposta (campo → valor proposto → por
  quê) e espere o meu "pode" para AQUELA ação.
- **Você nunca cria conta, nunca faz login, nunca aceita termos, nunca inscreve a loja em campanha,
  nunca envia convite ou mensagem a criador, nunca aprova amostra e nunca ativa GMV Max ou adiciona
  forma de pagamento.** Cadastro, documentos, qualificação de categoria e contratos são comigo:
  prepare o passo a passo e eu executo.
- **Toda consulta ao TikTok e ao TikTok Shop é feita pelo Claude in Chrome** (ferramentas
  `mcp__claude-in-chrome__*`), na sessão que eu deixar aberta no meu Chrome. Não use WebFetch nem curl
  para a Academy/Seller Center (só renderizam com JavaScript). Regras de uso, medidas aqui:
  - existem dois Chrome conectados ao Claude in Chrome neste PC: use o meu ("navegador rafael"). No
    começo, rode `list_connected_browsers`; se houver dúvida, use `switch_browser` e eu clico em
    Connect no navegador certo;
  - carregue todas as ferramentas do Chrome numa chamada só do ToolSearch; comece com
    `tabs_context_mcp`, crie a SUA aba e feche no fim; nunca reaproveite tabId antigo;
  - outras sessões usam o mesmo Chrome: uma chamada de navegador por vez, sem paralelizar;
  - depois de cada navegação tire um screenshot pequeno (`scale: 0.1`) antes de ler; para lazy-load,
    role com `computer scroll`; leia com `get_page_text`, `find`, `read_page`; para listas, extraia JSON
    curto com `javascript_tool` (a saída trunca perto de 1.500 caracteres: leia em partes);
  - a vitrine pública fica em shop.tiktok.com/br e não tem busca de produto: navegue por categoria
    (Alimentos e bebidas `/br/c/food-beverages/700437` → Bebidas `/br/c/drinks/914824` → Café
    `/br/c/coffee/700612`, botão "Ver mais"); o número de vendidos do card da categoria é recente, o
    da página do produto é o acumulado;
  - `tiktok.com/shop` costuma abrir "Security Check" (captcha de quebra-cabeça): PARE e me peça para
    resolver — nunca resolva captcha, nunca faça login; pausa de 6 a 10 s entre páginas.
- Afirme com fonte: página oficial (kid da Academy BR, URL e data), nota da pesquisa (arquivo e id da
  afirmação), painel do Seller Center (com data) ou o script de preço. O que não foi medido vai marcado
  como *não medido*.

## 3. Primeiro passo: diagnóstico de prontidão (no Chrome, só leitura)

No formato das agências — cada achado como **evidência → diagnóstico → risco de não agir → próximo
passo**:

1. **Conta e loja**: temos conta de vendedor (CNPJ; MEI aceito; até 5 lojas por CNPJ)? Conta oficial e
   contas de marketing vinculadas? Em que nível de loja estaríamos (Iniciante 50 pedidos/dia →
   Padrão 100 → Premium 200 → Profissional ilimitado) e o que cada nível exige.
2. **A porta da categoria Alimentos** (o ponto mais crítico): Alimentos é categoria por convite e de
   alto risco — exige qualificação com AHR > 150 e SPS > 4, no Centro de qualificação (6 etapas, só
   desktop). Leia na Academy BR o fluxo atual, os documentos pedidos (Anvisa/MAPA, rotulagem) e se
   café torrado em grãos/moído está entre os permitidos; confirme na lista de proibidos que não
   caímos em nenhuma restrição. Liste exatamente o que eu preciso providenciar e em que ordem.
3. **Regras que mudam a conta unitária**, relidas na Academy BR: tarifa (kid=24428156307201), se a
   tarifa fixa conta por unidade, SKU ou kit (está ABERTO na pesquisa — tente resolver), loja nova com
   0% de comissão por 60 dias (teto R$ 17 mil), Programa de Taxas de Envio, comissão padrão de
   afiliado da categoria, regras de campanha (SPS ≥ 3,0 e AHR > 150; campanha exige GMV Max),
   LIVE Flash Sale e preço-limite de campanha.
4. **Logística de largada**: Envio pelo TikTok (padrão) × envio pelo vendedor, SLA (RTS em 1 dia útil,
   TTS em 2), metas (LDR ≤ 4%, SFCR ≤ 2,5%), penalidades, coleta no nosso CEP, devolução de
   alimento (só lacrado; verifique a regra mais recente).
5. **Prateleira de café** (seção 4.2): quem vende café em grãos e moído de 1 kg e 500 g, preço e
   preço por kg, kits, frete, vendidos, avaliações, uso de vídeo, LIVE e afiliados.
6. **Ferramentas de crescimento disponíveis para loja nova**: programa de afiliados (aberto,
   direcionado, Shop Ads), amostras (grátis e reembolsável), GMV Max, LIVE, campanhas do calendário.

Grave em `tiktokshop/01-diagnostico-prontidao-2026-10.md` e me mostre o resumo antes de seguir.

## 4. Como o mercado faz esta análise (siga este método)

Fonte: `pesquisa-marketplaces/tiktokshop/metodo.md`. No TikTok Shop a unidade de análise não é só o
produto: é **produto × conteúdo × criador × LIVE**.

1. **Mercado e categoria**: tamanho e tendência (Momentum Works/Tabcut, Newsroom BR), peso das
   superfícies de fechamento (no BR ~50% do GMV fecha na aba Loja, ~26% em vídeo, ~23% em LIVE —
   ago/2025), sazonalidade e calendário de campanhas.
2. **Prateleira e concorrência**: os produtos de café que vendem, com preço, kit, frete, vendidos e
   avaliações; as lojas de torrefação (Coffee Mais, Minas Estate e outras) e como usam kits, LIVE e
   afiliados.
3. **Criadores e conteúdo** (como as ferramentas fazem): quais criadores vendem café/alimentos, GMV por
   criador, formatos de vídeo e ganchos que convertem, GPM e CTR do vídeo, conversão e GMV/hora de
   LIVE. Use ferramenta de terceiros (Kalodata, FastMoss, EchoTik) só para priorizar; trate os números
   como estimativa.
4. **Economia unitária por SKU em escada**: CM1 = preço − CMV − tarifa − Programa de Taxas de Envio −
   imposto; CM2 = CM1 − comissão de afiliado − cupom − GMV Max; CM3 = CM2 − amostras e frete de amostra
   − devoluções/reembolso sem devolução. **Atenção:** o peso está na parte fixa da tarifa no ticket
   baixo (R$ 4 ou R$ 6 por item) e a conta é contínua em R$ 50 (não há degrau em R$ 49,90); um kit só
   reduz tarifa se contar como 1 item.
5. **Ads com critério de agência**: GMV Max é o formato para vender no Shop e atribui a si pedidos
   orgânicos e de afiliado — julgue por venda total e margem, não pelo ROI que ele mostra; preveja
   teste de incrementalidade (pausa/holdout).
6. **Rotina**: diária (pedidos no prazo, chat em 24 h, estoque para o pico, LIVE), semanal (SPS e AHR,
   afiliados ativos, amostras → conteúdo, GMV Max), mensal (CM1–CM3 por SKU, criadores que trazem
   venda, calendário de campanhas).

## 5. O que temos de decidir juntos (estratégia de entrada)

1. **Abertura e liberação de Alimentos**: passo a passo até a loja poder vender café (documentos,
   qualificação, metas de SPS/AHR) e o que fazer enquanto a categoria não libera.
2. **Portfólio**: quais SKUs entram primeiro (1 kg, 500 g, kits, kit degustação), preço por SKU e por
   kg, com a tarifa fixa por item no centro da conta, e o piso de margem.
3. **Conteúdo próprio**: linha editorial da conta da marca (vídeo e LIVE), frequência, roteiro,
   quem apresenta, o que mostrar do café (torra, origem, preparo), e o que a Política de Conteúdo
   proíbe (LIVE estática, conteúdo não original, alegação de saúde, "menor preço" sem prova).
4. **Afiliados e criadores**: comissão por SKU (padrão 8% em Alimentos), colaboração aberta ×
   direcionada × Shop Ads, política de amostras (grátis × reembolsável), perfil de criador para café,
   meta de criadores ativos, e o teto de pedidos da loja nova (um criador grande pode estourar o limite
   e deixar o produto "esgotado").
5. **LIVE commerce**: se, quando e como fazer LIVE da marca; LIVE Flash Sale (só a conta oficial cria;
   preço ≤ menor de 14 dias).
6. **GMV Max e campanhas**: quando ligar, ROI-alvo a partir do equilíbrio, entrar ou não nas campanhas
   (exigem GMV Max ativo), calendário (11.11, Black Friday, 12.12).
7. **Logística e reputação**: SLA de despacho, metas de LDR/SFCR, estoque para pico viral, devolução e
   reembolso de alimento, caminho de SPS para liquidação Expressa (> 3,5) e selo (> 4,5).
8. **Metas e portões**: fases com critério de entrada e saída (ex.: categoria liberada → primeiras
   amostras; N vídeos de afiliados com venda → GMV Max; SPS ≥ 3,0 → campanhas; nível Padrão → escala).

## 6. Como trabalhar comigo

- Uma decisão por vez, com 2 ou 3 opções, a sua recomendação e o número que a sustenta.
- Antes de propor preço, mostre a tabela do script com CM1/CM2/CM3 por SKU e o ROI de equilíbrio.
- Registre cada decisão aprovada em `tiktokshop/02-estrategia-entrada-1kg-500g.md` (fases, portões,
  preços, conteúdo, afiliados, LIVE, GMV Max, logística, rotina, o que medir), com data e fonte de
  cada número.
- Medição nova vai para um documento com data; erro que custou uma rodada vira lição num
  `tiktokshop/LEIA-ME.md` (crie se não existir).
- Não faça commit nem push sem eu pedir.

Comece pelos passos da seção 1 e pelo diagnóstico da seção 3.
```
