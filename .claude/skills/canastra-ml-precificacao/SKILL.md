---
name: canastra-ml-precificacao
description: Use when pricing a Café Canastra listing on Mercado Livre — computing profit, margin, break-even, target price, wholesale (atacado) tiers, kit price, Clássico vs Premium, or the effect of a promotion or Pix discount. Uses the real CMV from mercadolivre/custos.md and the scripts/precificar.py calculator.
---

# Precificar no Mercado Livre

**Fonte de custo única:** [`mercadolivre/custos.md`](../../../mercadolivre/custos.md).
**Calculadora:** `python mercadolivre/scripts/precificar.py` (rode com `PYTHONIOENCODING=utf-8`
no Windows).

## Começo de toda sessão

```bash
python mercadolivre/scripts/precificar.py --conferir
```

Ela bate a fórmula com o "Você recebe" lido no formulário de 3 anúncios. **Se divergir, um
custo do ML mudou** — abra o formulário, leia tarifa e frete e atualize `custos.md` e as
constantes do script antes de recomendar qualquer preço.

## A fórmula

```
lucro = preço × (1 − tarifa − 9% imposto) − frete − CMV
preço para margem m = (CMV + frete) / (1 − tarifa − 9% − m)
```

| Uso | Comando |
|---|---|
| Tabela padrão 1 kg e kit 2 kg | `precificar.py` |
| Um preço | `precificar.py --preco 119.90 --cmv 47 --frete 34.30 --tipo classico` |
| Preço para uma margem | `precificar.py --margem 15 --cmv 47 --frete 34.30` |
| Desconto bancado pelo vendedor | `--desconto 10` |

## Regras que já custaram caro

1. **Frete sai do formulário, nunca de blog.** Ele depende do peso, da embalagem cadastrada e
   da **cor da reputação**. Os R$ 34,30 do 1 kg são de reputação **vermelha**.
2. **Frete grátis é obrigatório a partir de R$ 79** — todo café de 1 kg paga frete.
3. **Abaixo de R$ 150 → Clássico; acima → Premium** (parcelamento). Premium custa 5 pontos de
   margem; só compensa se a campanha ou o parcelamento trouxer conversão que pague isso.
4. **Atacado tem teto:** o ML obriga a repassar a economia de frete
   (`teto = preço − economia de frete por unidade`, lido no balão do ícone vermelho). Calcule o
   lucro **no teto**, não no preço que você queria.
5. **Promoção (preço riscado, campanhas, cashback) exige reputação verde ou amarela.** Confira
   na Central de promoções antes de modelar um cenário que dependa dela.
6. **A vitrine não é o preço configurado.** "X% OFF no Pix" aparece por cima; leia o preço no
   formulário. Quem banca o desconto do Pix **não está medido** — não assuma que é o ML.
7. **Escada de preço tem que descer por unidade base** (por kg, por cápsula). Mas os líderes
   de 1 kg **não dão desconto no kit** — o kit vende conveniência e frete diluído.
8. Imposto é **9% do preço de venda**, não do líquido.

## Como entregar

Tabela com preço, tipo, "recebe do ML", lucro em R$ e margem %, o ponto de equilíbrio, e a
recomendação com o porquê. Diga sempre quais números são medidos e quais são estimados.
