# Sondagem da API da xAI

## Por que este documento existe

O ambiente onde o CIE foi construido **nao tem egress para `api.x.ai` nem para
`docs.x.ai`** — o proxy responde 403. Nenhuma requisicao real foi feita, nenhuma pagina
de documentacao foi lida.

A consequencia foi tratada como decisao de arquitetura, e nao como limitacao a contornar:
**nenhum parametro de API foi assumido.** Tudo que depende de saber como a API se
comporta esta atras de `cie/capabilities.py`, cujo default e "nao suportado" para
absolutamente tudo. `scripts/probe_api.py` existe para substituir suposicao por
evidencia, uma pergunta de cada vez, contra a API de verdade.

Chutar sai caro de duas formas. A barata: a API responde 400 e voce perde tempo. A cara:
a API responde **200**, ignora silenciosamente o campo desconhecido, cobra a imagem e
devolve algo que nao seguiu referencia nenhuma — e voce so descobre semanas depois,
olhando um lote inteiro fora do estilo.

---

## Em que modo o sistema esta agora

```bash
uv run cie probe      # o que a sondagem descobriu, ou que ela nunca rodou
uv run cie models     # catalogo de modelos, precos e se sao verificados
```

Enquanto `.cie/capabilities.json` nao existir, valem estes defaults:

| Capacidade | Default | Efeito |
|---|---|---|
| `native_reference_supported` | `false` | referencia visual so por texto (`DescriptorReferenceStrategy`) |
| `reference_field` / `reference_endpoint` | `None` | nenhum campo de imagem vai no corpo do request |
| `max_reference_images` | `0` | — |
| `supports_seed` | `false` | `seed` nao e enviado; geracoes nao sao reproduziveis |
| `supports_aspect_ratio` | `false` | proporcao pedida pode ser ignorada pela API |
| `supports_size` / `supports_quality` | `false` | nao enviados |
| `max_n` | `1` | ver a nota sobre `n`, mais abaixo |
| `response_formats` | `["b64_json"]` | o CIE grava bytes, nunca URL |
| `vision_model` | `None` | `cie dna build --execute` falha pedindo `CIE_VISION_MODEL` |

Todos os modelos do catalogo de precos nascem com `verified=false`, e cada job em modo
seco carrega o aviso `model_not_verified`. Isso e proposital: um numero errado no
relatorio de custo e pior do que um numero marcado como incerto.

---

## As perguntas em aberto

### 1. Quais modelos de imagem existem hoje, e quanto custam?

O catalogo semente (`cie/pricing.py`) traz `grok-imagine-image` (US$ 0,02),
`grok-imagine-image-quality` (US$ 0,05 a 0,07) e `grok-imagine-image-2.0` (US$ 0,04 a
0,08). Esses numeros vieram da especificacao do projeto e **nao** foram conferidos.

A sondagem faz `GET /models` (e testa dois endpoints de catalogo hipoteticos,
`/image-generation-models` e `/language-models`, que podem simplesmente nao existir) e
grava os nomes vistos.

**O que muda:** `.cie/models.yaml` passa a listar os modelos que existem de fato, e
`cie models` os mostra. **Preco continua nao verificado** — a API nao expoe tabela de
precos, e inventar um numero ali seria pior do que nao ter. Confira os precos na fatura
ou na pagina de precos da xAI e edite `.cie/models.yaml` a mao; e para isso que o
arquivo existe.

### 2. `/images/generations` aceita imagem de referencia? Em qual campo?

**A pergunta mais importante da lista.** A sondagem testa cinco campos candidatos
(`image`, `images`, `reference_images`, `input_image`, `image_url`) em duas codificacoes
(base64 puro e data URI), um pedido isolado por combinacao — dez tentativas. Se algum
retornar 200 e o campo for de lista, ela ainda testa duas referencias no mesmo pedido.

**O que muda:** com um campo confirmado, `native_reference_supported` vira `true` e
`cie.reference.choose_strategy` passa a usar a `NativeReferenceStrategy`: a foto real
viaja no corpo do request, redimensionada para 1536 px e em JPEG 90, ate o limite de 3
referencias (politica da casa) ou o que a API aceitou, o que for menor. As referencias
sao escolhidas por `quality_score` decrescente, entre os assets que passam no teste de
consentimento. Sem confirmacao, a `DescriptorReferenceStrategy` continua sendo a unica
via — e o aviso `native_reference_capability` aparece em todo job com referencia.

### 3. Existe `/images/edits`?

A sondagem tenta o endpoint em JSON e em `multipart/form-data`.

**O que muda:** se existir, e a porta para edicao real de imagem — extensao de cena,
outpainting, variacao a partir de uma foto nossa — que e o caso de uso mais alinhado ao
principio da casa ("a IA edita e estende o real"). Hoje o resultado so e registrado em
`capabilities.reference_endpoint`; usar de fato o endpoint de edicao e trabalho novo,
que so faz sentido depois da prova de que ele existe.

### 4. `aspect_ratio` ou `size`?

A sondagem envia `aspect_ratio: "1:1"` e `size: "1024x1024"` em pedidos separados.

**O que muda:** `supports_aspect_ratio` e `supports_size` sao gravados. Atencao ao que a
sondagem **nao** responde: ela prova que o *parametro* e aceito, nao *quais valores* ele
aceita — testar todas as proporcoes custaria uma imagem cada. Por isso
`.cie/models.yaml` mantem a lista de proporcoes do catalogo semente. Se um `9:16` voltar
400 na producao, corrija a lista `aspect_ratios` do modelo nesse arquivo.

Independente da resposta, `4:5` (feed vertical do Instagram) continua saindo do recorte
local na exportacao: nenhuma API de imagem que conhecemos gera nessa proporcao.

### 5. `seed` e aceito?

**O que muda:** com `supports_seed=true`, da para repetir uma geracao que deu certo e
variar so um parametro — o que reduz retrabalho e, portanto, custo por imagem aprovada.
Sem isso, cada geracao e um evento unico e o campo `generations.seed` fica vazio.

### 6. `quality` e aceito?

Relevante so para `grok-imagine-image-2.0`, cuja faixa de preco (0,04 a 0,08) depende de
`low`/`medium`. **O que muda:** com `supports_quality=true`, a estimativa de custo passa
a poder usar a chave `1k:low` / `2k:medium` do catalogo em vez do preco cheio.

### 7. Qual o `n` maximo por request?

A sondagem envia `n: 2`. **O que muda, e este e o efeito colateral mais importante de
toda a sondagem:** `capabilities.max_n` vira `2` (se aceitou) ou `1` (se recusou), e esse
valor e escrito como `max_n` de cada modelo em `.cie/models.yaml`. O guardrail
`n_within_limits` usa `min(10, modelo.max_n)` — ou seja, **depois de sondar, um job com
`n: 4` passa a ser bloqueado**, mesmo que a API aceite dez.

Isso e conservadorismo deliberado, nao bug: o sistema so afirma o que provou. Quando
souber o teto real (pela documentacao ou testando `n` maior a mao), edite `max_n` em
`.cie/models.yaml`. O teto duro de 10 imagens por job continua valendo de qualquer jeito.

### 8. Quais os limites de rate?

**A sondagem nao responde isso hoje**, e e importante dizer com todas as letras. Ela nao
mede taxa, nao dispara rajada e nao guarda cabecalhos de resposta — `.cie/probe/attempts.json`
tem endpoint, campo, status, latencia e corpo de erro, mais nada.

O que existe hoje e a defesa do cliente (`cie/xai.py`): 429 e 5xx sao retentados com
backoff exponencial (base 1s, fator 2, teto 30s) e jitter, honrando `Retry-After`
numerico, ate 5 retentativas. Na pratica, a fila do CIE e sequencial e pequena (dezenas
de imagens por semana), entao o rate limit tende a nao ser o gargalo. Se aparecerem 429
em serie, o caminho e ler os cabecalhos `x-ratelimit-*` de uma resposta real e ajustar o
tamanho do lote — nao aumentar a retentativa.

### 9. Qual o modelo com visao para o Style DNA?

A sondagem filtra a lista de `/models` por tokens (`vision`, `grok-4`, `grok-3`,
`grok-2v`), descarta os que parecem de imagem, pega ate 3 candidatos e manda para cada um
um `/chat/completions` com uma imagem em data URI e o pedido de descrever em uma frase.
O primeiro que responder 200 vira `capabilities.vision_model`.

**O que muda:** `cie dna build --execute` passa a funcionar sem configuracao. Enquanto
nao rodar, o comando falha explicando as duas saidas: rodar a sondagem, ou definir
`CIE_VISION_MODEL=<nome>` no `.env`. Nao existe fallback com nome chutado — um chute
custa uma chamada com 12 imagens anexadas para receber 404.

---

## Como rodar

Numa maquina com rede e com `XAI_API_KEY` no ambiente ou no `.env`:

```bash
python scripts/probe_api.py --dry-run     # imprime o plano e o teto de custo, nao chama nada
python scripts/probe_api.py               # roda, pedindo confirmacao interativa
python scripts/probe_api.py --yes         # roda sem perguntar
```

Opcoes uteis:

| Flag | Para que serve |
|---|---|
| `--skip-edits` | pula as duas tentativas em `/images/edits` |
| `--model <nome>` | testa outro modelo de imagem (padrao: `grok-imagine-image`) |
| `--out <dir>` | onde gravar o resultado (padrao: `.cie`) |
| `--base-url <url>` | aponta para outra base da API |
| `--timeout <seg>` | timeout por pedido (padrao: 120s) |

O script vive **fora** da suite de testes de proposito: ele e a unica parte do
repositorio que toca a rede, e nenhum teste automatizado pode depender disso.

---

## Quanto custa

Cada geracao de imagem bem-sucedida custa entre US$ 0,02 e US$ 0,08. O plano completo
dispara ate cerca de 19 pedidos de imagem, mas a maioria das tentativas de campo de
referencia deve falhar com 4xx — e tentativa recusada normalmente nao e cobrada. **Na
pratica, o gasto fica entre US$ 0,05 e US$ 0,40.**

O teto pessimista (tudo cobrado, na resolucao mais cara) e calculado e impresso antes de
comecar, e o script exige confirmacao interativa a menos que venha `--yes`. Comece sempre
por `--dry-run`.

---

## O que sai da sondagem

| Arquivo | Conteudo | Quem le |
|---|---|---|
| `.cie/capabilities.json` | todas as capacidades confirmadas, mais o log de tentativas | `cie/capabilities.py`, guardrails, escolha de estrategia, `cie probe` |
| `.cie/models.yaml` | modelos vistos, com `max_n` sondado e os precos **nao** verificados | `cie/pricing.py` via `load_overrides`, `cie models` |
| `.cie/probe/attempts.json` | log cru: endpoint, campo, status, latencia, corpo de erro | auditoria humana |

**A chave nunca aparece em nenhum deles.** Todo corpo de erro passa por
`cie.config.redact` antes de virar relatorio, e a chave nao e impressa nem no cabecalho
do plano (o script so informa se ela esta presente ou ausente).

---

## Resumo: nativa contra descritiva

|  | `DescriptorReferenceStrategy` (hoje) | `NativeReferenceStrategy` (depois da prova) |
|---|---|---|
| Como a foto real entra | como **texto**: o Style DNA extraido dela vira frase no prompt | como **pixel**: base64 no corpo do request |
| Precisa da sondagem | nao | sim — campo, endpoint e codificacao confirmados |
| Fidelidade ao acervo | media: paleta, luz, lente e materiais | alta: enquadramento e textura da propria foto |
| Custo | uma chamada de visao por perfil de estilo | zero extra por job (payload maior) |
| Rastreabilidade | `style_dna_id` no job, mais `reference_asset_ids` como referencia conceitual | `reference_asset_ids` no job, agora com os pixels que foram enviados |
| Limite | 8 a 15 fotos por perfil | ate 3 referencias por job |

A troca e automatica: `cie.reference.choose_strategy` olha as capacidades e decide. Nada
no plano semanal, nos templates ou nos comandos muda quando a sondagem confirmar o
suporte — a mesma fila passa a mandar as fotos junto.

**O que nao muda nunca, com sondagem ou sem ela:** rosto de pessoa real nao e
sintetizado, embalagem com texto legivel nao nasce do zero, toda saida carrega
proveniencia e exige rotulagem de IA. As capacidades da API mudam o *como*; a
[politica](POLITICA-IA.md) manda no *o que*.

---

## Quando rodar de novo

- antes do primeiro `--execute` em qualquer maquina nova;
- quando a xAI anunciar modelo novo, ou quando `cie models` nao listar o modelo que voce
  quer usar;
- quando comecarem a aparecer 4xx com mensagem de parametro desconhecido em jobs que
  antes funcionavam;
- a cada poucos meses, como higiene: custa centavos e evita descobrir a mudanca por meio
  de um lote inteiro perdido.
