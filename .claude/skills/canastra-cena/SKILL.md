---
name: canastra-cena
description: Use when a Café Canastra image has a scene rather than a plain packshot — lavoura, terreiro, mesa, torrefação, UGC, lifestyle, post de rede social — or when a generated image looks like stock/IA and needs to read as a real phone photo.
---

# Cena — realismo e procedência

O alvo estético **não é gosto pessoal**: é o perfil medido das nossas próprias fotos
de celular. Uma cena bonita que não bate com esse perfil denuncia IA mesmo com o
rótulo perfeito.

Use junto com **canastra-conteudo**. Se a embalagem aparece legível, **canastra-embalagem**
manda no rótulo.

## Curadoria em uma linha

Só `base-curada/01-real-verificada/` (38 arquivos) vira pixel. As camadas `02`, `03`
e `04` têm uso definido em `base-curada/LEIA-ME.md` — leia antes de anexar qualquer
coisa. `03-mood-terceiros` é a estética-alvo **e** é de terceiros: serve para extrair
descritor textual, nunca para entrar num request.

## O buraco que muda o plano

`docs/briefing-captura.md` registra o que **não existe** na base própria:

| Assunto | Cobertura |
|---|---|
| Grão torrado | zero |
| Café pronto, xícara, coador | zero |
| Torrefação, tambor, cupping | zero |
| Painel solar, colheita, terreiro | zero |
| Pessoas | zero (2 fotos de mão, sem rosto) |

**Se a cena pedida cai num desses, não existe referência real para anexar.** Não
force um substituto de outra camada. Descreva a cena em texto no prompt e diga ao
Arthur que aquele assunto é buraco de captura. O que existe de sobra: lavoura ao
meio-dia (a diversidade real é ~4 cenas, não 20), e packshot sobre bancada clara.

## Perfil de câmera medido — o alvo

| Métrica | Alvo | Por quê |
|---|---:|---|
| ponto preto (`p1`) | 14 | HDR de celular não desce mais |
| preto % | 0,007 | celular quase nunca chega a preto puro |
| cast altas R/B | 0,969 | puxa **azul**; dourado quente é assinatura de IA |
| ruído | 0,42 | leve |

**Duas métricas do alvo antigo eram média de populações diferentes e não descreviam
nenhuma delas.** Compare cena com cena, packshot com packshot:

| Métrica | Lavoura ao meio-dia | Packshot de bancada |
|---|---:|---:|
| saturação | ~86 | ~59 |
| estourado % | 0,26 (até 3,5 com céu aberto) | 0,001 |

`nitidez centro/borda 1,57` está suspeito: o cálculo em `scripts/home_medir.py:perfil`
empilha os quatro cantos num vetor e mede gradiente nele, o que não é vizinhança
espacial. Não decida nada por esse número até o cálculo ser corrigido.

**Em imagem gerada, o passe de pós deve ser mínimo — só saturação, e contra o grupo
certo.** Duas tentativas de calibração completa saíram net-negativas: corrigiam uma
métrica e estragavam três. (Em **foto real** não se aplica passe nenhum.) E as
métricas medem assinatura de dispositivo, não plausibilidade: uma imagem calibrada
com pão de queijo em formato errado é pior que uma com duas métricas fora.

## Quando a saída é a foto real, não uma geração

O caminho mais curto para "imagem real" costuma ser **cortar**, não gerar. Duas
armadilhas que não dão erro, só entregam errado:

- **Orientação EXIF.** Os 38 arquivos de `01-real-verificada` têm `orientation = 6`:
  estão girados no disco. `Image.open(f).crop(...)` devolve a foto **deitada**, sem
  reclamar. Abra sempre com `ImageOps.exif_transpose(Image.open(f))` e confira o lado
  maior antes de cortar.
- **Formato de feed.** Post de feed é **4:5** (1080×1350, razão exata 0,8000). Corte a
  partir do retrato nativo e escolha de que lado tirar a sobra olhando o assunto —
  cortar por cima decapita um pé de café. Só reduza depois, em LANCZOS. Precedente:
  `FINAL-suave-1080x1350-feed.jpg`. (O 3:4 é formato de **geração**; 4:5 nativo não
  existe na xAI, ver `CLAUDE.md`.)

Uma foto real é a **fonte** da medida de calibração, não candidata a ser corrigida
por ela. Não aplique passe de saturação numa foto da base.

## Blocos obrigatórios do prompt

**Anti-bokeh** — desfoque não se desfaz em pós; morre na geração ou não morre.
Descreva a física: sensor 1/1.7" a f/1.8, profundidade de campo enorme, tudo
igualmente nítido, distância suaviza por névoa e nunca por desfoco, cantos moles
por lente larga barata.

**Luz** — `Direcao-Criativa.md` pede golden hour na fazenda. **O acervo não tem isso:**
as 26 fotos de Medeiros foram capturadas entre 10h e 11h (EXIF). O documento de marca
prescreve uma aspiração; quem manda no que existe é o arquivo. A luz real da fazenda é
**sol a pino**: céu azul com cumulus, sombra dura,
iPhone 7, ISO 20, março, meio-dia. Não invente dia nublado. E **direção de luz não
se dita no prompt** — o modelo ignora. Gere, **meça** a direção na imagem (especular
de objeto cilíndrico, sentido das sombras) e reilumine a composição a partir do medido.

**Espontaneidade** — nada de derramado arrumado, objeto atravessado por cima, mesa
posta. Comida é **meio comida**: mordida, farelo, dourado desigual, crosta mate.
Pedir comida bonita devolve render de comida.

**Props que existem naquele lugar** — a base real mostra pé de café, terra vermelha,
mangueira de irrigação, poste de madeira, arame, cadeira de plástico, galpão de
zinco. Balança de cozinha, colher de cupping, bule de ágata e pano de crochê na
lavoura são invenção.

## Vieses do modelo que você vai enfrentar

- Deixa o produto **em pé**; "deitado no chão" costuma ser ignorado.
- Puxa **dourado quente**; nosso alvo puxa azul.
- Em série, inventa variação de cenário — descreva o cenário compartilhado
  explicitamente e **negue** as variações (já saiu madeira azul num carrossel).

## Conferência de cena

A fase 4 de `canastra-conteudo` vale igual, com dois acréscimos:

- **Valide a região que você mediu.** Já se mediu "ruído" numa textura de madeira e
  "sombra do caneco" em cima do próprio caneco.
- **Plausibilidade antes de métrica.** Objeto que não existe naquele lugar, comida
  com formato errado ou pessoa com anatomia estranha reprovam a imagem mesmo com
  todas as métricas dentro do alvo.
