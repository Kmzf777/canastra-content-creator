---
name: canastra-embalagem
description: Use when a Café Canastra package is legible in the frame — packshot de catálogo, troca de fundo, lateral, verso, ou o pacote aparecendo numa composição ou UGC — and the printed label must survive the generation letter for letter.
---

# Embalagem — fidelidade de rótulo

**Regra zero: a embalagem entra como pixel, nunca como texto solto.** Fidelidade
escala com o tamanho no quadro: abaixo de ~30% da altura, conte com erro de letra;
abaixo de ~2%, a tipografia não sobrevive de jeito nenhum.

Use junto com **canastra-conteudo**, que manda no fluxo e na conferência.

## Fontes da verdade

| Preciso de… | Vem de |
|---|---|
| a arte real do SKU | `fotos produtos cru/<Pasta-Do-SKU>/` (137 fotos, 24 pastas) |
| âncora de estúdio já aprovada | `saida-teste/catalogo-estudio/<N>-<slug>/<N>.1-frente-branco.png` |
| o prompt pronto daquela imagem | `docs/PROMPTS-ESTUDIO-CATALOGO.md`, seção do produto |
| mudar qualquer convenção de prompt | `scripts/prompts_catalogo.py` — **nunca o .md** |

Cada pasta de `fotos produtos cru/` nomeia as faces: `-frente-`, `-verso-`,
`-lateral-`. Confirme qual face é qual **olhando**, não pelo número: no set de
cápsulas o `verso` é a face de contato e código de barras, não a do selo 1985.

## A ordem importa e economiza refação

1. **Frente fundo branco** — confira o texto aqui. Só siga quando estiver certo.
2. **Frente fundo cor** — anexe **só a aprovada do passo 1**. É troca de fundo, então
   posição e rótulo vêm de graça.
3. **Laterais**, cada uma com sua foto.
4. **Verso** — o ponto fraco. CNPJ, endereço, lote, QR e código de barras em corpo
   minúsculo. O modelo redesenha em vez de copiar. Rota confiável é composição da
   foto real; se gerar mesmo assim, trate como rascunho.

## A âncora de outro SKU da mesma família

Quando a foto crua do SKU novo é ruim — as cápsulas Suave chegaram por WhatsApp em
591×1280, um oitavo da área das outras — anexe **duas** imagens e separe os papéis
no prompt, em parágrafo próprio:

- **Imagem 1**: a foto do SKU novo. Fonte da **arte**: cor da faixa, nome da
  variante, ilustração, cada linha impressa.
- **Imagem 2**: a `<N>.1-frente-branco.png` já aprovada de um SKU irmão. Fonte só de
  **forma, geometria, traço do logo, luz, fundo e enquadramento**.

Sem esse parágrafo o modelo copia o que não devia. Diga explicitamente o que **não**
trazer da imagem 2 — a faixa preta do Clássico, o badge `CLÁSSICO`, os grãos e as
folhas ao lado das cápsulas. Funcionou de primeira nas cápsulas Suave.

## Quando a referência não deixa ler

`"copie da foto"` só é instrução se a foto permitir ler. Quando não permite, é
convite ao chute — o modelo inventou `70 / 80 / 80 / 40` para notas que eram
`7,0 / 10 / 10 / 6,0`.

1. Amplie e tente de verdade (PIL, 5–7×, `ImageOps.autocontrast`).
2. Não conseguiu? **Pergunte ao Arthur.** Não derive de barra, não infira do SKU irmão.
3. Com o valor na mão, **soletre no prompt** — e grave no campo `lateral_extra` do
   produto em `scripts/prompts_catalogo.py`, para a próxima sessão não repetir.

## Corrupções recorrentes — confira estas por nome

| Sai | Certo | Onde |
|---|---|---|
| `EXPRESSO` | `ESPRESSO` | sugestão de preparo |
| `CATUAI` | `CATUAÍ` | parágrafo de descrição |
| `70` `80` `40` | `7,0` `10` `6,0` | notas sensoriais |
| `TORRA MÉDIA ESCURA` | `TORRA MÉDIA` (Suave é uma linha só) | intensidade |
| `SCA 80+` | `SCAA 80+` (dois A) | só na cápsula |
| `Doodo 1985` | `Desde 1985` | assinatura do logo |
| `TRODULB E HÚMO` | `TORRADO E MOÍDO` | frente dos sacos |
| `MICROIRREGIÃO` | `MICRORREGIÃO` | lateral |
| `1kg` | `1Kg` (K maiúsculo só no quilo) | peso |

Acentos que somem com frequência: `CAFÉ`, `GRÃOS`, `ARÁBICA`, `Ã` de `MICRORREGIÃO`,
`À`, `CONTEÚDO`, `INDÚSTRIA`, `SEM GLÚTEN`, `DOÇURA`.

## Diferenças entre famílias

Cada família tem corpo e ocupação próprios, já escritos no script. O que muda mais:

- **Sacos** (`saco`/`doypack`): a lateral é rascunho conhecido — o modelo insiste
  num perfil pontudo em vez da sanfona reta. Decisão do Arthur: aceitar como rascunho.
- **Caixas** (cápsula, drip): 5 imagens em vez de 4 — duas laterais. A faixa do topo
  identifica a variante: Clássico preta, Canela vinho, Suave marrom-chocolate.

## Erros que já custaram rodada

- Conferir pela imagem inteira em vez do recorte ampliado.
- Aprovar campo que a referência não permite ler (ver `canastra-conteudo`, fase 4).
- Inserir prompt longo com `computer.type` — o `\n` envia truncado.
- Assumir que o download é o certo porque a dimensão bate.
- Inserir produto novo no meio da lista do script: renumera as pastas já geradas em
  disco. Produto novo entra **no fim**.
