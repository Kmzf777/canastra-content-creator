# Shopee — Café Canastra

> **Leia antes de qualquer coisa nesta pasta.** Operação do zero: em 15/10/2026 ainda não se
> sabe se a loja existe (a Central não foi aberta logada). Custo do produto (CMV, imposto) é o
> mesmo do ML: [`../mercadolivre/custos.md`](../mercadolivre/custos.md), fonte única. Mapa de
> regras da plataforma: [`../pesquisa-marketplaces/shopee/CONSOLIDADO.md`](../pesquisa-marketplaces/shopee/CONSOLIDADO.md)
> (vale a §8, verificação de 15/10/2026).

| Arquivo | Conteúdo |
|---|---|
| [`02-diagnostico-prontidao-2026-10.md`](02-diagnostico-prontidao-2026-10.md) | **COMECE AQUI.** Prontidão em 15/10/2026: conta, regras relidas, logística, prateleira de café (2 buscas, 80 cards), economia unitária, ferramentas e o que falta |
| `03-estrategia-entrada-1kg-500g.md` | (a criar) decisões aprovadas pelo Rafael, uma a uma, com data e fonte |
| [`scripts/precificar_shopee.py`](scripts/precificar_shopee.py) | Escada CM1 → CM2 → CM3 com comissão de 01/10/2026, CPF, coparticipação de frete, Ads, cupom, campanha 3,5%, afiliado, Devolução Fácil, Full+; pisos, zonas mortas, kit × avulso |
| [`01-estrategia-shopee.md`](01-estrategia-shopee.md) | **ENVIESADO** — rodada de 14/10 que partiu do estado do ML. Não usar como conclusão |
| [`pesquisa/2026-10-estrategia/`](pesquisa/2026-10-estrategia/) | Transcrições e notas da rodada de 14/10 |

## A regra que não se negocia

Nada é criado ou alterado na Shopee sem autorização explícita do Rafael, campo a campo. Ler é
livre. Conta, login, termos, campanha, Ads e recarga são sempre com ele.

## O que destrava esta pasta

1. Saber se a conta existe e em que documento (CNPJ é o caminho: Full, Indicado e sem +R$ 3/item).
2. Login de comprador no Chrome para ler "vendidos" e anúncios líderes.
3. Código Anvisa do café torrado confirmado pelo contador/RT ("00" se dispensado).
4. Extrato do 1º pedido avulso e do 1º kit (taxa fixa do kit, D18 do CONSOLIDADO).

## Lições (sintoma → causa → regra)

1. **`javascript_tool` devolveu `[BLOCKED: Cookie/query string data]`** ao retornar o texto de um
   artigo do Centro de Educação → o filtro da extensão bloqueia saída que contenha URL com query ou
   algo parecido com cookie → para ler artigo, use `get_page_text`; no JS, devolva só campos
   curtos e sem URL.
2. **A saída do `javascript_tool` corta em ~1.000 caracteres (`[TRUNCATED]`)** → guarde o
   resultado em `window.__x` e leia em fatias de 8 a 10 linhas curtas.
3. **Selos dos cards de busca (Indicado, Oficial, Full) não estão no `innerText`** — são
   `img[alt=flag-label]`. Em 15/10/2026, a largura identifica: 48 px = Indicado, 37 px = Oficial,
   23 px = Full (conferido por zoom). Sem login, o card **não mostra "vendidos"**.
4. **A conexão com o Chrome caiu no meio de um `browser_batch`** e o grupo de abas sumiu; o
   `tabs_context_mcp` passou a responder "sem grupo" → recrie com `createIfEmpty: true`; as abas
   antigas ficam órfãs na janela do usuário — avise para ele fechar.
