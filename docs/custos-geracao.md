# Custos de geração de imagem — xAI vs Gemini

Levantado em 17/08/2026. Preços da xAI vêm do próprio endpoint `/models` da API
(campo `image_price`, unidade 1e-10 USD). Preços do Gemini vêm da página oficial
de preços da API.

## Tabela unitária

| Modelo | Resolução nativa | Por imagem |
|---|---|---:|
| **xAI** `grok-imagine-image` | 864×1152 | **US$ 0,020** |
| **xAI** `grok-imagine-image-quality` | 864×1152 | **US$ 0,050** |
| **xAI** `grok-imagine-image-2.0` low/1k | 1k | US$ 0,040 |
| **xAI** `grok-imagine-image-2.0` low/2k | 2k | US$ 0,060 |
| **xAI** `grok-imagine-image-2.0` medium/1k | 1k | US$ 0,060 |
| **xAI** `grok-imagine-image-2.0` medium/2k | 1776×2368 | **US$ 0,080** |
| **Gemini** `gemini-2.5-flash-image` (Nano Banana) | 1k | **US$ 0,039** |
| **Gemini** `gemini-3.1-flash-image` 1K | 1024 | US$ 0,067 |
| **Gemini** `gemini-3.1-flash-image` 2K | 2048 | US$ 0,101 |
| **Gemini** `gemini-3-pro-image` (Nano Banana Pro) 1K/2K | 928×1152 | **US$ 0,134** |
| **Gemini** `gemini-3-pro-image` 4K | 4k | US$ 0,240 |

Entrada no Gemini: US$ 2,00 por milhão de tokens, e cada imagem de referência
custa 560 tokens. Um prompt nosso com duas referências dá ~2.000 tokens de
entrada, ou **US$ 0,004** — arredondamento, não custo.

**Batch API do Gemini corta 50%** na saída: `gemini-3-pro-image` cai para
**US$ 0,067** por imagem em 1K/2K. Isso inverte o ranking — ver o final.

## O que o projeto de fato gastou

### xAI — 67 imagens, US$ 4,49

| Rodada | Imgs | Modelo | US$ |
|---|---:|---|---:|
| 1º teste (texto + referência) | 3 | quality | 0,15 |
| cena sem pacote | 4 | quality | 0,20 |
| sondagem v1 (com meu bug do `4:5`) | 4 | quality | 0,20 |
| sondagem v2 (capacidades) | 9 | quality | 0,45 |
| sondagem v2 (parâmetros do 2.0) | 3 | 2.0 misto | 0,18 |
| experimento H1–H4 | 7 | quality | 0,35 |
| experimento H4 | 1 | 2.0 med/2k | 0,08 |
| DNA v2 corrigido | 3 | 2.0 med/2k | 0,24 |
| anti-bokeh | 2 | 2.0 med/2k | 0,16 |
| teste final de guidance | 3 | 2.0 med/2k | 0,24 |
| humanização | 3 | 2.0 med/2k | 0,24 |
| carrossel de 4 slides | 8 | 2.0 med/2k | 0,64 |
| regeração do slide 3 | 2 | 2.0 med/2k | 0,16 |
| espontâneo, 1ª tentativa | 6 | 2.0 med/2k | 0,48 |
| sondagem de multi-fonte | 5 | 2.0 med/2k | 0,40 |
| espontâneo, refeito | 4 | 2.0 med/2k | 0,32 |
| **total** | **67** | | **4,49** |

Média US$ 0,067 por imagem gerada.

### Gemini — 4 imagens, US$ 0,55

4 × `gemini-3-pro-image` em 928×1152 (faixa 1K) = US$ 0,536, mais ~US$ 0,014 de
entrada. Média **US$ 0,137** por imagem.

## Custo por imagem aproveitada — e por que o número engana

| | geradas | aproveitadas | US$/aproveitada |
|---|---:|---:|---:|
| xAI | 67 | 10 | **0,45** |
| Gemini | 4 | 3 | **0,18** |

Parece que o Gemini foi 2,5× mais barato na prática. **Não foi, e essa
comparação é injusta.**

Das 67 imagens da xAI, cerca de **28 foram sondagem e correção de erro** — a
descoberta das capacidades da API, o meu bug do `4:5` que envenenou uma rodada
inteira, a referência errada (verso do pacote), a correção do DNA da serra, a
descoberta do formato de multi-fonte. Esse trabalho foi feito **uma vez** e o
Gemini herdou tudo pronto: quando rodei as 4 do Gemini, os blocos de
humanização, anti-bokeh e espontaneidade já estavam prontos e verificados.

Comparando só produção final contra produção final, a taxa de acerto é parecida.
A diferença real está na tabela unitária: **o Gemini Pro custa 1,7× o xAI 2.0
med/2k** (0,134 contra 0,080).

## Projeção para operação real

12 posts por mês, a maioria carrossel de 4 slides, com 2 variantes por slide
para escolha = **96 gerações/mês**:

| Configuração | Mensal | Anual |
|---|---:|---:|
| Gemini 2.5 Flash Image | US$ 3,74 | US$ 45 |
| xAI `-quality` | US$ 4,80 | US$ 58 |
| **Gemini 3 Pro em Batch** | **US$ 6,43** | **US$ 77** |
| **xAI `-2.0` medium/2k** | **US$ 7,68** | **US$ 92** |
| Gemini 3.1 Flash 2K | US$ 9,70 | US$ 116 |
| Gemini 3 Pro, padrão | US$ 12,86 | US$ 154 |

Mesmo dobrando o volume e ficando no modelo mais caro, o teto anual é ~US$ 300.

## A conclusão

**Custo não decide nada aqui.** A diferença entre a opção mais barata e a mais
cara da tabela é de US$ 110 por ano — menos que uma diária de fotógrafo. Escolher
o modelo por preço seria otimizar o item irrelevante da conta.

O que decide é o que já está medido:

- **Gemini `gemini-3-pro-image`** entrega cena muito mais natural. A foto da
  cadeira de plástico entrou com 1 métrica fora de 6 **antes de qualquer
  pós-processamento** — o melhor casamento com a assinatura do nosso celular real
  em todo o projeto.
- **xAI `/images/edits`** preserva o rótulo, porque é edição sobre a imagem-fonte.
  O Gemini trata a referência como inspiração e **redesenha** o rótulo: saiu
  `SOSCIALTY` e `288g` no Suave.
- O Gemini aceita **`4:5` nativo**; a xAI não tem 4:5 e obriga a gerar em 3:4 e
  recortar, perdendo ~6% da altura.
- A xAI em 2k entrega 1776×2368, acima da especificação de feed. O Gemini Pro
  entrega 928×1152, **abaixo** de 1080×1350, exigindo 1,16× de ampliação — a menos
  que se pague a faixa 4K (US$ 0,24).

**Regra de roteamento, por quanto o produto pesa no quadro:**

| Situação | Modelo | US$ |
|---|---|---:|
| Ambiente é o assunto, produto pequeno ou ausente | Gemini 3 Pro | 0,134 |
| Produto grande, rótulo precisa ser legível | xAI `/images/edits` 2.0 med/2k | 0,080 |
| Rótulo exato ao pixel | composição do recorte real | 0 |

E se a geração deixar de ser interativa — uma fila noturna que roda o lote do mês
—, o **Batch do Gemini a US$ 0,067** fica mais barato que o xAI 2.0 med/2k e
mantém a qualidade de cena. É a única mudança de preço que muda uma decisão.

---

Fontes de preço: [xAI `/models`](https://api.x.ai/v1/models) (consultado
diretamente) e [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing).
