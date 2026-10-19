# Amazon — Café Canastra

> Leia antes de qualquer trabalho de Amazon. **A conta de vendedor existe** ("Cafe Canastra", Seller
> Central BR). Em 15/10/2026 tinha só 6 ofertas de drip coffee, todas inativas e com estoque 0, e um
> único envio ao FBA (50 un., março/2026: 33 vendidas, 17 vencidas). **Não há 1 kg nem 500 g
> cadastrados, nem Brand Registry, nem Ads.** Ver
> [`02-auditoria-2026-10.md`](02-auditoria-2026-10.md). Custos de produto: fonte única em
> [`../mercadolivre/custos.md`](../mercadolivre/custos.md).

## Regra que vale aqui também

Nada é criado ou alterado no Seller Central sem autorização do Rafael, campo a campo — a mesma
regra do Mercado Livre.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| [`02-auditoria-2026-10.md`](02-auditoria-2026-10.md) | **Comece aqui.** Auditoria da conta em 15/10/2026 (completa) |
| [`01-estrategia-amazon.md`](01-estrategia-amazon.md) | Rodada anterior, **ENVIESADA**: não use como conclusão |
| [`scripts/precificar_amazon.py`](scripts/precificar_amazon.py) | Escada CM1/CM2, ACOS e ROAS de equilíbrio. Tabela FBA de /precos conferida contra a conta em 15/10/2026; Mais Vantagens 2,5%; Experimente FBA. **Peso do pacote não medido** |
| [`scripts/extrator_busca_amazon.js`](scripts/extrator_busca_amazon.js) | Extrator da busca da Amazon pelo Claude in Chrome (renderiza com a janela oculta) |
| [`pesquisa/2026-10-estrategia/`](pesquisa/2026-10-estrategia/LEIA-ME.md) | Transcrições, notas por tema e como reproduzir |

## Lições

1. **A tabela FBA de /precos "desalinhada" era célula mesclada** → no DOM os valores abaixo de R$ 79
   (5,65 / 5,85 / 6,05) aparecem só na linha 1–1,5 kg, e a pesquisa concluiu que eram tarifa daquele
   peso. A conta mostra R$ 5,85 para um drip leve de ~R$ 31,90: é tarifa fixa por preço, para qualquer
   peso → **antes de interpretar uma tabela extraída do DOM, confira uma célula contra um valor
   que a conta cobra de verdade.**
2. **Relatórios de negócios pedem login de novo** (`max_auth_age=300`) mesmo com a sessão aberta:
   as páginas comuns abrem, e essa redireciona para `/ap/signin`. Deixe-a para quando o Rafael
   puder logar na hora.
3. **O lote de drip venceu na prateleira do FBA** → em 04/2026 chegaram 50 un. em 6 SKUs, 10 de cada
   formato sem olhar a demanda; os dois que venderam esgotaram em abril e não foram repostos, e os 17
   que sobraram viraram EXPIRED em junho (a Amazon tira de venda a 50 dias do vencimento) → **o envio
   ao FBA de alimento se dimensiona pela janela útil = validade na chegada − 50 dias**, não por
   "mandar um lote"; e SKU sem venda em 30 dias não recebe o mesmo volume do campeão.
4. **Nos Relatórios de negócios, trocar a data pela URL não recarrega** → o hash muda e a tabela segue
   no período anterior, sem erro. Force a recarga com um parâmetro antes do `#`
   (`/business-reports?r=N#/report?...&fromDate=...`) e **confira as datas exibidas** antes de ler. E a
   tabela só renderiza as colunas visíveis: role o contêiner na horizontal (`scrollLeft = scrollWidth`
   em cada elemento com overflow, inclusive dentro de shadow DOM) antes de extrair unidades e vendas.
