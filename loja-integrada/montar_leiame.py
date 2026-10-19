# -*- coding: utf-8 -*-
"""Escreve o LEIA-ME da entrega a partir dos mesmos dados da planilha."""
import os, sys, json
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from catalogo import PRODUTOS, FORMATO

tray = {p["sku"]: p for p in json.load(open(os.path.join(AQUI, "tray-produtos.json"), encoding="utf-8"))}
fotos = json.load(open(os.path.join(AQUI, "mapa-fotos.json"), encoding="utf-8"))

ORIGEM_FOTO = {
    "CAN-CLA-GR-1000": "foto real do pacote, recortada — o packshot de estúdio foi reprovado",
    "CAN-SUA-GR-1000": "foto real do pacote, recortada — o packshot de estúdio foi reprovado",
    "CAN-MIC-MO-250": "packshot com o selo trocado pelo pixel da foto real",
}

SEM_GTIN = sum(1 for p in PRODUTOS if not p[6])
linhas = []
for i, (sku, tsku, _pg, _pr, cat, fmt, ean) in enumerate(PRODUTOS, 1):
    p = tray[tsku]
    peso = FORMATO[fmt][0]
    linhas.append((i, sku, tsku, p["nome"].replace(" - Café Canastra", ""), p["preco"], peso,
                   ean or "—", fotos[sku], ORIGEM_FOTO.get(sku, "packshot de estúdio")))

with open(os.path.join(AQUI, "entrega", "LEIA-ME.md"), "w", encoding="utf-8") as f:
    w = f.write
    w("""# Café Canastra — materiais para a Loja Integrada

Entrega de **13/10/2026**: logotipo, 20 produtos e as fotos de cada um.

## O que tem aqui

| Pasta / arquivo | O que é |
|---|---|
| `planilha-produtos-cafe-canastra.xlsx` | o modelo oficial de importação, 20 linhas preenchidas |
| `fotos/` | 27 JPGs, nomeados `NN-produto-N.jpg`, onde `NN` é a ordem da planilha |
| `logo/` | logotipo oficial, fundo transparente, 3508×2481 |

As colunas `imagem-1` a `imagem-5` da planilha estão **vazias de propósito**: as
fotos vão como arquivo, não como URL. A tabela abaixo liga cada produto aos seus
arquivos pelo número da linha.

## Logotipo

Quatro arquivos, todos PNG com fundo transparente em 3508×2481:

- `logo-cafe-canastra-preta.png` — para fundo claro
- `logo-cafe-canastra-branca.png` — para fundo escuro
- as versões `-recortada` são as mesmas sem a margem em volta

## Os 20 produtos

| # | SKU | Produto | Preço | Peso | GTIN | Fotos |
|---:|---|---|---:|---:|---|---|
""")
    for i, sku, tsku, nome, preco, peso, ean, arqs, _o in linhas:
        reais = f"{float(preco):.2f}".replace(".", ",")
        quilos = f"{peso:.3f}".replace(".", ",").rstrip("0").rstrip(",")
        arquivos = ", ".join("`" + a + "`" for a in arqs)
        w(f"| {i} | `{sku}` | {nome} | R$ {reais} | {quilos} kg | {ean} | {arquivos} |" + chr(10))

    w("""
## O que confirmar antes de publicar

Três campos saíram daqui **sem medição**, e estão marcados para o Rafael conferir:

- **`peso-em-kg` e as dimensões.** Não existe pesagem de postagem registrada em
  nenhum lugar do projeto, nem na página da loja atual. O único número medido é o
  do pacote de 1 kg — **1,128 kg em caixa de 27×29×11 cm**, pesado para o Mercado
  Livre. Os demais são estimativa de peso líquido mais embalagem. Isso entra no
  cálculo de frete, então vale a pena pesar um de cada formato.
- **`ncm`.** Preenchido `09012100` (café torrado, não descafeinado) nas 20 linhas.
  Confirmar com a contabilidade, principalmente para cápsula e drip coffee.
- **`gtin`.** Só está preenchido onde o código de barras foi lido no verso do
  pacote de verdade. """ + f"{SEM_GTIN} produtos ficaram" + """ em branco porque o código
  nunca foi lido. E atenção: **`7892262780089` é o mesmo código no Clássico 500 g moído e no
  500 g em grãos** — está assim na embalagem impressa, não é erro de digitação.

## De onde vieram os dados

Nome, preço e descrição são os da loja atual (`loja.cafecanastra.com`), lidos em
13/10/2026. Preço cheio, sem promocional.

Dois apontamentos sobre a loja atual, que valem a correção lá também:

- **"Suave em Grãos 250 g" está cadastrado duas vezes** (SKUs 49 e 63), com o
  mesmo nome e o mesmo preço. Aqui entrou uma linha só.
- A foto do Clássico 250 g na loja mostra a embalagem **antiga**, com o selo
  `GOURMET / SCAA 80+`. A embalagem atual traz `SPECIALTY / SCA 80+`. As fotos
  desta entrega são da embalagem atual.

## Sobre as fotos

Cada frente foi conferida **letra por letra contra a foto do pacote real** antes
de entrar. Três não passaram e foram substituídas:

""")
    for i, sku, _t, nome, _p, _pe, _e, _a, origem in linhas:
        if sku in ORIGEM_FOTO:
            w(f"- **{nome}** — {origem}.\n")
    w("""
Nos dois pacotes de 1 kg o packshot de estúdio tinha desenhado pássaros que não
existem na embalagem e escrito `Clássico` e `Suave` em caixa mista, onde o pacote
real traz tudo em maiúsculas. No Microlote moído, o selo redondo saiu dizendo só
`PARA COADOR`; o selo impresso diz `CAFÉ MOÍDO PARA COADOR`, em roxo, e foi
recolocado a partir da foto do pacote.

**Não entram** fotos de lateral nem de verso: nelas o carimbo de lote e as datas
de fabricação saem regenerados — já saiu `F: 23.2025`, um mês que não existe.
Data impossível em loja aberta ao público é informação regulatória falsa.
""")
print("LEIA-ME escrito")
