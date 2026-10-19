# TikTok Shop: Café Canastra

> **Leia antes de qualquer coisa nesta pasta.** A loja existe (Cafe Canastra, BRLCXJL2E9) e a
> qualificação de Alimentos e bebidas está aprovada desde 15/10/2026. Em 16/10/2026 ainda não há
> produto cadastrado. O custo do produto (CMV e imposto) é o mesmo do ML:
> [`../mercadolivre/custos.md`](../mercadolivre/custos.md), fonte única. Regras da plataforma:
> [`../pesquisa-marketplaces/tiktokshop/CONSOLIDADO.md`](../pesquisa-marketplaces/tiktokshop/CONSOLIDADO.md).

| Arquivo | Conteúdo |
|---|---|
| [`01-diagnostico-prontidao-2026-10.md`](01-diagnostico-prontidao-2026-10.md) | **COMECE AQUI.** Prontidão em 16/10/2026: conta, porta de Alimentos, regras relidas, logística, prateleira de café, ferramentas e o que falta |
| `02-estrategia-entrada-1kg-500g.md` | (a criar) decisões aprovadas pelo Rafael, uma a uma, com data e fonte |
| [`scripts/precificar_tiktok.py`](scripts/precificar_tiktok.py) | Escada CM1 → CM2 → CM3 com tarifa de 15/07/2026, SFP, afiliado, cupom, GMV Max, isenção de loja nova, amostra e perdas; pisos; kit × avulso |
| [`medicoes/`](medicoes/) | Medições com data (prateleira de café de 16/10/2026) |

## A regra que não se negocia

Nada é criado ou alterado no TikTok Shop sem autorização explícita do Rafael, campo a campo. Ler é
livre. Conta, login, termos, campanha, afiliados, amostra, GMV Max e forma de pagamento são sempre
com ele.

## Lições (sintoma → causa → regra)

1. **Escrevi 4 valores de "CM3 só conta própria" de cabeça no diagnóstico e errei os 4** (ex.: 17,63
   em vez de 18,23) → copiei o padrão de outra coluna em vez de rodar o caso → todo número de margem
   sai do script (`--preco ... --cmv ...` ou `resultado()`), inclusive os que parecem óbvios.
2. **O Seller Center injeta centenas de "maxline" no `innerText`** de algumas páginas (Logística,
   Contas vinculadas) → use `innerText.replace(/maxline\s*/g,'')` no `javascript_tool`, ou
   `get_page_text`.
3. **Screenshot dá timeout ("renderer frozen") na aba do MCP** em páginas pesadas, mas
   `get_page_text` e `javascript_tool` respondem → não insista no screenshot; leia texto.
4. **O clique em "Inscreva-se agora" (campanha) foi bloqueado pelo controle de permissões** → botão
   que abre fluxo de inscrição conta como escrita, mesmo sem enviar; os requisitos da campanha ficam
   para quando o Rafael abrir o fluxo.
5. **A Central de Afiliados abre com um modal "Ativar amostras grátis"** para todos os produtos da
   colaboração aberta → feche pelo X; nunca clique em "Ativar".
6. **Na vitrine web, o "Ver mais" da categoria Café acaba em 100 cards** (5 cliques) → para mais
   amostra, use outra subcategoria ou outra hora; o "vendidos" do card é recente e o da página é o
   acumulado.
