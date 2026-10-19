# Prompt — estratégia de entrada na Shopee (1 kg e 500 g)

> Cole o bloco abaixo numa sessão nova do Claude Code aberta na pasta `Canastra-Content-Creator`.
> Escrito em 15/10/2026 a partir de `pesquisa-marketplaces/shopee/` (pesquisa + verificação no
> navegador) e do método de `pesquisa-marketplaces/metodo/`. A Shopee é greenfield: nunca vendemos lá.

---

```
Você vai trabalhar comigo (Rafael, Café Canastra) para traçar a ESTRATÉGIA DE ENTRADA na Shopee
para os nossos cafés de 1 kg e de 500 g. Nunca vendemos na Shopee: é uma operação do zero.
Precisamos decidir desde a abertura e a configuração da loja até preços, estrutura dos anúncios,
Shopee Ads, conteúdo (vídeo, live, afiliados), cupons e campanhas, e o caminho até o Full da Shopee.
Somos FÁBRICA (torrefação própria, marca própria), não revenda.

## 1. Antes de qualquer coisa, leia (nesta ordem)

1. `pesquisa-marketplaces/shopee/CONSOLIDADO.md` — o mapa de como a Shopee funciona e como os
   melhores operam. Leia inteiro, inclusive a §8 (verificação por navegador de 15/10/2026, que
   CORRIGE pontos do corpo do texto: taxa de 3,5% das Campanhas de Destaque, armazenagem cobrada no
   Full desde 01/03/2026, validade e lote visíveis no Full, oCPM só no GMV Max de produto, pontos de
   penalidade, Vendedor Indicado com nota ≥ 4,5). Quando precisar de detalhe, vá à nota da frente:
   `pesquisa-marketplaces/shopee/<frente>/notas.md` (ads, preco-promocao, logistica-estoque,
   ranqueamento-anuncio, produto-mix, reputacao-atendimento, alimentos-marca-propria, cases-grandes).
   **Vale a §10 e a §11 (verificação) de cada nota**; o que estiver CONTESTADO vale pelo que a fonte
   oficial diz. Veja também `pesquisa-marketplaces/shopee/social/notas.md` e `observacao/lideres.md`.
2. `pesquisa-marketplaces/metodo/estado-da-arte.md` — como agências e ferramentas fazem esta
   análise (resumo na seção 4 abaixo).
3. `pesquisa-marketplaces/LACUNAS.md` §2 — o que a pesquisa não conseguiu responder sem login.
4. `mercadolivre/custos.md` — fonte única de custo (CMV 1 kg R$ 47, 500 g R$ 26, imposto 9% sobre
   o preço). Para preço, use `shopee/scripts/precificar_shopee.py` (já tem as faixas de comissão de
   2026 confirmadas: até R$ 79,99 = 20% + R$ 4,50 por item; R$ 80–99,99 = 14% + R$ 16;
   R$ 100–199,99 = 14% + R$ 20; R$ 200+ = 14% + R$ 26). Antes de usar, confira cada constante do
   script contra o CONSOLIDADO §1 e §8 e corrija o que estiver desatualizado; se faltar cenário
   (frete, Ads, cupom, Pix, campanha de 3,5%), estenda o script — nunca calcule de cabeça.
5. `shopee/01-estrategia-shopee.md` é de uma rodada anterior e está marcado como ENVIESADO (partiu
   do estado do Mercado Livre). Não use como conclusão.

Não há agente nem skill de Shopee neste repositório: você é o gestor da Shopee nesta sessão.
Ignore as pastas do Mercado Livre e da Amazon, exceto `mercadolivre/custos.md`.

## 2. Regras que não se negociam

- **Nada é criado ou alterado na Shopee sem a minha autorização explícita, campo a campo** (loja,
  anúncio, preço, cupom, campanha, Ads, envio ao Full). Ler é livre; escrever, não. Entregue cada
  ação como proposta (campo → valor proposto → por quê) e espere o meu "pode" para AQUELA ação.
- **Você nunca cria conta, nunca faz login, nunca aceita termos, nunca inscreve a loja em campanha
  e nunca ativa Ads ou recarrega saldo.** Cadastro, contrato, dados bancários e fiscais são comigo:
  prepare o passo a passo e eu executo.
- **Toda consulta à Shopee é feita pelo Claude in Chrome** (ferramentas `mcp__claude-in-chrome__*`),
  usando a sessão que eu deixar aberta no meu Chrome. Não use WebFetch nem curl para páginas da
  Shopee (a Central do Vendedor, o Centro de Educação e a Central de Ajuda só renderizam com
  JavaScript). Regras de uso, medidas aqui:
  - carregue todas as ferramentas do Chrome numa chamada só do ToolSearch; comece com
    `tabs_context_mcp`, crie a SUA aba e feche no fim; nunca reaproveite tabId antigo;
  - outras sessões usam o mesmo Chrome: uma chamada de navegador por vez, sem paralelizar;
  - com a aba oculta, listas não renderizam e screenshot pode travar: depois de cada navegação tire
    um screenshot pequeno (`scale: 0.1`) antes de ler; para lazy-load, role com `computer scroll`;
  - leia com `get_page_text`, `find`, `read_page`; para listas, extraia JSON curto com
    `javascript_tool`; tabelas publicadas como imagem (comuns no Centro de Educação) se leem por
    screenshot com `scale` 0.5;
  - a Shopee bloqueia visitante sem login depois da 1ª busca ("Login Necessário" /
    /verify/traffic/error): se acontecer, PARE e me peça para logar no Chrome — nunca faça login,
    nunca contorne a verificação de tráfego; captcha → PARE e me chame;
  - pausa de 6 a 10 s entre páginas.
- Afirme com fonte: página oficial (URL e data), nota da pesquisa (arquivo e id da afirmação),
  painel da loja (com data) ou o script de preço. O que não foi medido vai marcado como *não medido*.

## 3. Primeiro passo: diagnóstico de prontidão (no Chrome, só leitura)

Como não temos operação, o diagnóstico é de PRONTIDÃO, no formato das agências — cada achado como
**evidência → diagnóstico → risco de não agir → próximo passo**:

1. **Conta**: existe conta de vendedor da Canastra na Shopee? Em CNPJ? (vendedor CPF paga +R$ 3 por
   item depois de 450 pedidos em 90 dias; Full exige CNPJ no Simples, Real ou Presumido com
   certificado do mesmo CNPJ). Se não existir, liste o que eu preciso providenciar e em que ordem.
2. **Regras que mudam a conta unitária**, relidas no Centro de Educação (seller.shopee.com.br/edu):
   comissão e taxa fixa por item (artigo 18483 e 18484), frete grátis e teto do subsídio
   (R$ 20 / 30 / 40; coparticipação de 25% só na logística própria — artigos 23431 e 25794),
   Campanhas de Destaque (3,5% sobre TODAS as vendas da loja, renovação automática — 18712),
   Devolução Fácil (R$ 0,49 por pedido, ativação automática — 26700), pontos de penalidade (7955),
   Vendedor Indicado (18456), regras do Full (26370, 23197, 26581, 27632, 27600 Full+).
   Confirme se algo mudou desde 15/10/2026.
3. **Logística de largada**: prazo de envio (DTS de 2 dias úteis), modalidades disponíveis para o
   nosso CEP (coleta, ponto de entrega, Shopee Turbo é só raio de 7 km), o que é exigido para
   alimentos (código Anvisa quando aplicável — artigo 11602; embalagem — Manual 27632).
4. **Prateleira de café na Shopee** (ver seção 4.2): quem lidera em 1 kg e 500 g, preços, kits,
   Lojas Oficiais, uso de vídeo, frete, vendidos e avaliações.
5. **Ferramentas de crescimento disponíveis para loja nova**: Shopee Ads (GMV Max, formatos,
   orçamento e recarga mínimos, atribuição), Shopee Vídeo, Live, programa de afiliados, cupons de
   loja e de seguidores, Campanhas Oficiais e datas duplas.

Grave em `shopee/02-diagnostico-prontidao-2026-10.md` e me mostre o resumo antes de seguir.

## 4. Como o mercado faz esta análise (siga este método)

Fonte: `pesquisa-marketplaces/metodo/estado-da-arte.md`. Cruze quatro camadas: dado da plataforma
(Business Insights e Centro de Educação), estimativa de ferramenta (RadarSeller, UpSeller,
Nubimetrics — só para priorizar, são caixa-preta), prateleira digital (observação da busca) e
estudos/balanços (Sea 6-K, NIQ Ebit).

1. **Mercado**: tamanho e tendência da categoria café na Shopee, sazonalidade (datas duplas: uma por
   mês), quem lidera e com quais alavancas (Loja Oficial, Indicado, vídeo, live, afiliados, cupom).
2. **Prateleira digital da busca** para os termos que importam ("café em grãos 1kg", "café especial",
   "café moído 500g", "café torrado e moído", termos de marca): posições pagas × orgânicas, preço e
   preço por kg, kit, selo Indicado/Oficial, frete grátis, vídeo na capa, vendidos e nota; registre
   data, hora, termo e se a sessão está logada. Use as quatro ordenações da busca (Relevância, Mais
   recente, Vendas Principais, Preço).
3. **Análise da 1ª página** para marca própria: quantos vendedores distintos, quantas Lojas Oficiais,
   preço por kg dos líderes, capa e título, presença de vídeo; onde a nossa oferta (frescor, origem,
   preço por kg, kit) ganha.
4. **Índice de preço**: par a par por produto casado (mesmo peso, tipo, torra) e ponderado por
   vendas; preço por kg.
5. **Economia unitária por SKU em escada**: CM1 = preço − CMV − comissão − taxa fixa por item −
   coparticipação de frete − imposto; CM2 = CM1 − Ads − cupom do vendedor − taxa de campanha (3,5%
   se a loja entrar em Campanha de Destaque); CM3 = CM2 − devoluções (R$ 0,49 da Devolução Fácil) e
   custos do Full. ACOS/ROAS de equilíbrio a partir da margem antes de Ads. **Atenção ao degrau:**
   a taxa efetiva é 25,6% em R$ 79,99 e 34,0% em R$ 80; a taxa fixa é POR ITEM (3 unidades avulsas
   pagam 3 taxas) — isso define kit × avulso e o preço-alvo de cada SKU.
6. **Ads com critério de agência**: na Shopee de 2026 o lance é por meta de ROAS (GMV Max); meta
   alta demais faz a plataforma não gastar. Verba derivada da margem (TACOS ≤ fração da margem),
   julgar por venda total, e prever um teste de incrementalidade (pausa/holdout).
7. **Rotina**: diária (pedidos a enviar no prazo, chat, estoque, saldo de Ads), semanal (ROAS/TACOS,
   posição nos termos, taxa de não envio e atraso — gatilhos de 5% e 8% — e pontos de penalidade),
   mensal (CM1–CM3 por SKU, calendário da próxima data dupla).

## 5. O que temos de decidir juntos (estratégia de entrada)

Para o 1 kg e o 500 g (grãos e moído; avalie kits 2 × 1 kg e 2 × 500 g):

1. **Abertura e configuração**: CPF × CNPJ, logística de largada, prazo de envio, Devolução Fácil,
   perfil da loja, o que precisa estar pronto antes do 1º anúncio.
2. **Portfólio e anúncios**: quais SKUs entram primeiro, variação × anúncio separado (cuidado com
   "spam de preço" acima de 4x entre variações), kits, título, capa, fotos, vídeo, GTIN.
3. **Preços**: preço por SKU em torno dos degraus de comissão (R$ 79,99/R$ 80; R$ 99,99/R$ 100;
   R$ 199,99/R$ 200), subsídio Pix (5% a partir de R$ 80, pago pela Shopee), escada de preço por kg,
   piso de margem — e nunca o "desconto enganoso" (subir o preço e descontar).
4. **Tração inicial sem queimar margem**: vídeo e live, afiliados (comissão compatível com a
   margem), cupons de loja e de seguidores, entrar ou não nas Campanhas de Destaque (3,5% sobre a
   loja inteira, renovação automática), calendário (11.11, 12.12).
5. **Shopee Ads**: quando ligar, quais SKUs, formato, meta de ROAS a partir do equilíbrio,
   orçamento, regra de corte e de escala.
6. **Reputação**: como chegar a Vendedor Indicado (nota ≥ 4,5, TNE < 2%) e não tomar pontos de
   penalidade (atraso ≥ 5%, não envio > 8%).
7. **Caminho até o Full**: requisitos confirmados (CNPJ; a partir de R$ 20; 10 un./mês até R$ 79,99,
   5 un./mês a partir de R$ 80; até 30 kg; validade e lote visíveis), custos (armazenagem por
   ociosidade desde 01/03/2026, Supermercado a partir de 2 meses; taxa de envio excepcional para
   itens fora dos critérios; no-show), Full+ (−0,5 a −2 p.p. de comissão com ≥ 40% dos pedidos no
   Full), e a meta de vendas para o 1º envio.
8. **Metas e portões**: fases com critério de entrada e saída (ex.: X pedidos/semana sem atraso →
   ligar Ads; Indicado → Campanhas; volume mínimo por item → 1º lote no Full).

## 6. Como trabalhar comigo

- Uma decisão por vez, com 2 ou 3 opções, a sua recomendação e o número que a sustenta.
- Antes de propor preço, mostre a tabela do script com CM1/CM2, ACOS e ROAS de equilíbrio.
- Registre cada decisão aprovada em `shopee/03-estrategia-entrada-1kg-500g.md` (fases, portões,
  preços, anúncios, conteúdo, Ads, logística, rotina, o que medir), com data e fonte de cada número.
- Medição nova vai para um documento com data; erro que custou uma rodada vira lição num
  `shopee/LEIA-ME.md` (atualize o existente).
- Não faça commit nem push sem eu pedir.

Comece pelos passos da seção 1 e pelo diagnóstico da seção 3.
```
