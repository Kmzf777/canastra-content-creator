# Custos — fonte da verdade para preço no Mercado Livre

> **Informado pelo Rafael em 14/10/2026.** Substitui a pergunta "qual o CPV do 1 kg?",
> que bloqueava o `14-estrategia-1kg.md` §4. Se um número daqui mudar, mude **aqui** e
> rode `python mercadolivre/scripts/precificar.py` de novo — nenhum outro arquivo guarda CMV.

## CMV por embalagem (café torrado, linha Canastra)

| Embalagem | CMV (R$) | Imposto |
|---|---:|---|
| **1 kg** | **47,00** | **9% do preço de venda** |
| **500 g** | **26,00** | 9% do preço de venda |
| **250 g** | **14,00** | 9% do preço de venda |

- O imposto é **sobre o preço de venda** (não sobre o líquido do ML), então cresce com o preço.
- CMV de cápsula: R$ 15,10 por caixa de 10 (`LEIA-ME.md`, informado em 30/09).
- **Não informado:** se o CMV do Néctar de Minas é o mesmo da linha Canastra. Não assuma — pergunte.

## Custos do Mercado Livre medidos na conta

| Item | Valor | Origem |
|---|---:|---|
| Tarifa Clássico | 14% | painel de custos do formulário |
| Tarifa Premium | 19% | idem |
| Frete grátis obrigatório | a partir de R$ 79 | idem |
| Frete grátis 1 kg (reputação vermelha) | **R$ 34,30** | Suave `MLB5903454718`, formulário e venda real |
| Frete grátis kit 2 × 1 kg (vermelha) | **R$ 54,10** | Kit Clássico `7791312402`, formulário 11/10 |
| Frete grátis 1 kg a R$ 99,90 (vermelha) | **R$ 29,50** (era R$ 28,90 em 11/10) | Néctar `7791161926`, lista de anúncios 15/10 |
| Frete em reputação verde/amarela | **não medido** | o ML dá desconto; meça antes de usar |

## A fórmula

```
lucro = preço × (1 − tarifa − 9%) − frete − CMV
preço para margem m = (CMV + frete) / (1 − tarifa − 9% − m)
```

1 kg no Clássico, frete R$ 34,30: **empata em R$ 105,58**. Abaixo disso cada venda perde dinheiro.
