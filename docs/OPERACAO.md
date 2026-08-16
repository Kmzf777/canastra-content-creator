# Operacao do dia a dia

Guia pratico do Canastra Image Engine (CIE), do arquivo bruto que saiu do cartao da
camera ate o post publicado e rotulado. Se voce so vai fazer uma coisa hoje, faca em
modo seco primeiro.

> **O padrao mental do sistema e `--dry-run`.**
> `cie generate` e `cie queue run` nascem em modo seco: eles resolvem o prompt, estimam
> o custo e mostram o veredito de cada guardrail **sem chamar a API e sem gravar nada**.
> Para gastar credito e preciso pedir `--execute` de proposito. Em `cie queue run`,
> `--execute` ainda exige `--budget-usd`: nada roda sem teto.

Todos os comandos abaixo rodam a partir da raiz do projeto, com `uv run` na frente
(`uv run cie ingest ...`). O texto omite o `uv run` para caber na linha.

---

## Mapa do fluxo

```
   base de fotos reais
        |
   1. cie ingest ............ catalogo (dedupe por sha256, EXIF, quality_score, thumb)
        |
   2. cie assets review ..... curadoria humana: pilar, local, SKU, pessoa, consentimento
        |
   3. cie dna build ......... Style DNA: 8 a 15 fotos viram assinatura visual em texto
        |
   4. cie templates sync .... 12 cenas YAML entram no banco
        |
   5. plano da semana ....... plans/semana-NN.yaml
        |
   6. cie generate .......... modo seco: prompt final + custo + guardrails
        |
   7. cie queue run ......... execucao com teto rigido de orcamento
        |
   8. cie review ............ aprovar / rejeitar / marcar ponto focal
        |
   9. cie export ............ 9:16, 4:5, 1:1 + XMP/EXIF + manifest.json
        |
  10. publicar ............... com rotulagem de IA, conforme o manifesto
```

---

## 0. Antes de comecar

```bash
uv venv --python 3.11
uv sync --group dev
cp .env.example .env          # preencha XAI_API_KEY
uv run cie version            # mostra CIE_HOME e o caminho do banco
uv run cie db migrate         # cria/atualiza o banco
uv run cie db status          # migracoes aplicadas e pendentes
```

Fotos de celular em HEIC precisam do extra opcional: `uv sync --group dev --extra heic`.
Sem ele, arquivos `.heic` entram no catalogo marcados para revisao, sem dimensoes e sem
`quality_score` — o arquivo nao e perdido, so nao e medido.

Estado local (banco, thumbs, geracoes, resultado da sondagem) vive em `CIE_HOME`, que
por padrao e `.cie/` na raiz do projeto. A base de fotos originais **nunca** e copiada
para la: o catalogo guarda o caminho, e so derivados (thumbnails) saem do lugar.

Antes do primeiro `--execute`, leia [SONDAGEM-API.md](SONDAGEM-API.md) e rode
`cie probe` para saber em que modo o sistema esta operando.

---

## 1. Preparar a base

Duas pastas importam:

| Pasta | O que vai la |
|---|---|
| a pasta que voce passa para `cie ingest` | fotos reais da operacao, em qualquer arvore de subpastas |
| `assets/cutouts/` | recortes PNG/WebP **com canal alfa** dos pacotes reais, um por SKU |

### Convencao de nomes da entrada

```
CANASTRA_[PILAR]_[LOCAL]_[ASSUNTO]_[NNN].ext
CANASTRA_3_TORREFACAO_TAMBOR_007.jpg
CANASTRA_1_MEDEIROS_TERREIRO_SECAGEM_012.jpg
CANASTRA_PRODUCT_ESTUDIO_PACOTE_MICROLOTE_003.jpg
```

- `PILAR`: `1`, `2`, `3`, `4`, `product` ou `people` (aceita tambem `TERROIR`, `SOLAR`,
  `LABORATORIO`, `BREWING`, `PACKSHOT`, `EQUIPE` e outros sinonimos).
- `LOCAL`: `FAZENDA` ou `MEDEIROS`; `TORREFACAO`, `UBERLANDIA` ou `UDI`; `ESTUDIO`;
  `OUTRO`.
- `ASSUNTO`: palavras livres separadas por `_`; termos conhecidos (`GRAO`, `TERREIRO`,
  `COLHEITA`, `TAMBOR`, `CUPPING`, `V60`, `JUTA`, `PAINEL`, `MAOS`, `ROTULO`, ...) viram
  tags pesquisaveis.
- `NNN`: sequencia numerica.

Quando o nome nao segue a convencao, a ingestao tenta tokens do caminho (nome das
pastas) e o GPS do EXIF. Se ainda assim faltar pilar ou local, o asset entra como
`needs_review`. **O sistema nunca chuta.** Se o nome e o GPS discordarem, o nome vence —
ele e curadoria humana explicita — e o conflito fica registrado em `notes`, com o asset
marcado para revisao.

### Recortes de produto

Coloque em `assets/cutouts/` um PNG por SKU, ja recortado, com fundo transparente, com o
nome do SKU no arquivo (`microlote.png`, `capsula_drip.png`). E dai que sai o rotulo
real nas composicoes de produto — o caminho preferido para qualquer `product_shot`.

---

## 2. Ingerir

```bash
cie ingest ./assets/originals --dry-run --verbose   # olha antes
cie ingest ./assets/originals --verbose             # grava
cie ingest ./assets/originals --no-thumbs           # sem miniaturas
```

O que acontece por arquivo:

- **dedupe por sha256** — o mesmo arquivo nunca entra duas vezes, mesmo com outro nome;
- **EXIF** — data de captura, camera, lente, GPS;
- **`quality_score`** — heuristica local (ver seccao 10), sem rede e sem modelo;
- **thumbnail** de 640 px em `CIE_HOME/thumbs/`;
- **inferencia** de pilar, local, SKU e tags, com o motivo de cada deducao gravado em
  `notes`.

O resumo final conta varridos, ingeridos, duplicados, ignorados, erros e quantos
precisam de revisao. Extensoes suportadas: JPEG, PNG, TIFF, WebP, HEIC/HEIF e os RAW
mais comuns. Arquivo sem decoder disponivel entra no catalogo mesmo assim, marcado para
revisao: perder o rastro de um arquivo da base e pior do que te-lo incompleto.

**Dois campos que a ingestao nunca preenche de verdade:** `has_identifiable_person`
entra como `1` e `consent_on_file` entra como `0`, sempre, para qualquer foto. Nenhuma
maquina mexe nesses dois. Quem mexe e voce, na curadoria.

---

## 3. Curar

```bash
cie assets review                       # UI em http://127.0.0.1:8765/assets
cie assets list --needs-review
cie assets list --pillar 3 --reference
cie assets show 42
cie assets curate 42 --pillar 3 --location TORREFACAO_UBERLANDIA --no-person --done
cie assets curate 51 --consent --packaging --reference
```

Na UI, atalhos de teclado: setas navegam, `p` alterna pessoa identificavel, `c` alterna
consentimento, `r` alterna qualidade de referencia, `espaco` seleciona, `s` aplica a
selecao em lote, `enter` salva o card. Cada toque de `p`, `c` ou `r` ja grava.

### O que cada campo de politica significa

| Campo | Pergunta que ele responde | Quem preenche | Efeito pratico |
|---|---|---|---|
| `has_identifiable_person` | da para reconhecer alguem nesta foto? | humano | com `1` e sem consentimento, a foto nao serve de referencia |
| `consent_on_file` | existe termo de imagem assinado e arquivado? | humano | libera a foto como referencia; **nao** libera regenerar rosto |
| `has_readable_packaging` | aparece rotulo/logotipo legivel? | inferido, humano confirma | templates que mexem em embalagem exigem pelo menos uma referencia assim |
| `is_reference_grade` | a foto tem nitidez e resolucao para guiar a geracao? | calculado, humano ajusta | referencia fraca bloqueia o job |
| `needs_review` | falta curadoria humana nesta linha? | inferido, humano encerra com `--done` | filtro de trabalho pendente |
| `pillar` / `location` / `sku` | de que eixo, lugar e produto e esta foto? | inferido, humano corrige | selecao de assets, Style DNA e nome de arquivo na exportacao |

Regra que vale a pena decorar: **consentimento autoriza usar a foto, nunca recriar a
pessoa.** Nenhum template com regeneracao de rosto roda com foto de pessoa
identificavel, com termo assinado ou sem.

---

## 4. Extrair o Style DNA

O Style DNA e a ponte entre as fotos reais e o prompt: um modelo com visao olha de 8 a
15 fotos **suas**, ja aprovadas, e devolve paleta, qualidade de luz, lente, textura,
enquadramento, materiais recorrentes, clima e o que evitar. Esse descritor vira uma
frase que entra em todo prompt daquele eixo.

```bash
cie dna build --pillar 3 --name "laboratorio-uberlandia"             # modo seco
cie dna build --pillar 3 --name "laboratorio-uberlandia" --execute   # chama a API
cie dna build --name "packshots" --assets 12,15,19,23,27,31,44,52 --execute
cie dna list
cie dna show laboratorio-uberlandia
```

Sem `--execute` o comando so lista quais fotos seriam enviadas — util para conferir a
selecao antes de pagar por ela. So entram assets `is_reference_grade` que passam no
teste de consentimento; menos de 8 fotos descreve uma foto e nao um estilo, mais de 15
dilui a assinatura e encarece a chamada sem ganho.

**Este comando precisa do nome do modelo com visao**, que o CIE nunca chuta. Ele vem de
`CIE_VISION_MODEL` no `.env`/ambiente, ou do resultado da sondagem
(`.cie/capabilities.json`). Sem um dos dois, o comando falha explicando como resolver.
Um Style DNA por eixo de conteudo costuma bastar; refaca quando a base mudar de cara
(nova camera, nova iluminacao de estudio, nova safra).

---

## 5. Carregar as cenas

```bash
cie templates sync            # le templates/*.yaml e grava no banco
cie templates list
cie templates list --pillar 4 --kind macro
```

O YAML e a fonte da verdade; a tabela do banco e so um espelho, sincronizado por `name`.
Renomear o campo `name` cria um template novo em vez de atualizar o antigo. Todo
`negative_prompt` precisa carregar os oito termos obrigatorios (`warped text`,
`distorted logo`, `extra fingers`, `plastic skin`, `oversaturated HDR`, `watermark`,
`stock photo look`, `uncanny faces`) e um template com `packaging_text` so passa na
validacao com `requires_reference: true`.

As 12 cenas que vem prontas:

| Template | Pilar | Tipo | AR | Exige ref. | Riscos |
|---|---|---|---|---|---|
| `cafezal_encosta` | 1 | scene | 3:2 | - | - |
| `terreiro_secagem` | 1 | scene | 3:2 | - | - |
| `maos_colheita_seletiva` | 1 | scene | 4:3 | sim | hands, human_face |
| `paineis_solares_amanhecer` | 2 | scene | 16:9 | - | - |
| `tambor_torra` | 3 | scene | 4:3 | - | - |
| `macro_grao_torrado` | 3 | macro | 1:1 | - | - |
| `bloom_v60` | 4 | macro | 3:4 | - | - |
| `vapor_xicara` | 4 | macro | 9:16 | - | - |
| `harmonizacao_queijo_canastra` | 4 | lifestyle | 3:2 | - | - |
| `drip_coffee_escritorio` | 4 | lifestyle | 4:3 | sim | packaging_text |
| `pacote_madeira_rustica` | product | product_shot | 3:4 | sim | packaging_text |
| `textura_juta_saco` | - | texture | 1:1 | - | - |

Cada template tem variaveis com valor padrao (`roast_level`, `time_of_day`,
`wood_surface`, ...). Sobrescreva na hora da geracao com `--var chave=valor`, repetivel.

---

## 6. Planejar a semana

Um plano e um YAML com uma lista `jobs`. Guarde em `plans/semana-NN.yaml` para ter
historico do que foi produzido em cada semana.

```yaml
# plans/semana-01.yaml
jobs:
  - template: macro_grao_torrado
    dna: laboratorio-uberlandia
    n: 4
    variables:
      roast_level: "medium, first crack just finished"

  - template: terreiro_secagem
    dna: terroir-medeiros
    n: 2
    aspect_ratio: "9:16"

  - template: pacote_madeira_rustica
    n: 2
    reference_assets: [51]
    use_compositor: true
```

As chaves de cada job sao os campos de `PlanEntry` (`cie/queue.py`): `template`, `dna`,
`n`, `aspect_ratio`, `model`, `variables`, `reference_assets`, `use_compositor`. Sem
`aspect_ratio` vale o padrao do template; sem `model` vale o modelo padrao do catalogo.

```bash
cie queue add --from-plan plans/semana-01.yaml --dry-run   # o que entraria
cie queue add --from-plan plans/semana-01.yaml             # enfileira
cie queue list
cie queue list --status blocked
```

Job que ja nasce bloqueado pelos guardrails entra na fila com status `blocked` e o motivo
escrito — ele nunca chega na API. Conserte a causa (referencia, consentimento,
`--use-compositor`) e enfileire de novo.

---

## 7. Modo seco: a etapa mais barata do processo

```bash
cie generate --template macro_grao_torrado --dna laboratorio-uberlandia --n 4
cie generate --template pacote_madeira_rustica --reference 51 --use-compositor --n 2
cie generate --template vapor_xicara --var steam_density="thin, slow" --aspect-ratio 9:16
```

O que aparece na tela, sem nenhuma chamada de rede:

1. template, Style DNA e **estrategia de referencia** em uso (`descriptor` ou `native`);
2. modelo, proporcao e `n`;
3. o **prompt final resolvido**, exatamente como iria para a API — corpo do template com
   as variaveis substituidas, depois o fragmento do Style DNA, depois as ancoras
   tecnicas de camera, depois o negative;
4. o **custo estimado** em dolares;
5. o **veredito de cada guardrail**, e, para cada regra que bloqueia, a linha
   "como resolver".

Leia o prompt em voz alta uma vez. Erro de variavel, cena impossivel e contradicao de
luz aparecem nessa leitura e custam zero.

Severidades: `BLOCK` impede a geracao; `WARN` nao impede nada, mas e um recado para a
revisao humana (tipografia de rotulo, maos, rosto de raspao, preco nao verificado,
ausencia de sondagem); `INFO` e rastro, como o lembrete de rotulagem obrigatoria.

Quando estiver satisfeito, `--execute` enfileira e roda aquele job na hora:

```bash
cie generate --template macro_grao_torrado --dna laboratorio-uberlandia --n 4 \
  --execute --budget-usd 0.50
```

---

## 8. Rodar a fila com orcamento

```bash
cie queue run --limit 20 --budget-usd 5.00              # ainda e modo seco
cie queue run --limit 20 --budget-usd 5.00 --execute    # gasta credito de verdade
```

`--execute` sem `--budget-usd` e recusado de proposito. O teto e rigido: a fila para
**antes** de estourar e diz quantos jobs continuam pendentes. Rodar de novo com um teto
maior retoma de onde parou.

Cada imagem produzida e gravada em `CIE_HOME/generations/` com sha256, prompt, modelo,
custo e `disclosure_required=1`. Falha de API marca o job como `failed` com o corpo do
erro preservado (sem a chave, que nunca e impressa). O cliente ja trata 429 e 5xx com
retentativa, backoff exponencial e jitter; erro 4xx que nao seja 429 falha na hora,
porque pedido errado nao melhora com insistencia.

---

## 9. Revisar

```bash
cie review        # UI em http://127.0.0.1:8765/review
```

Atalhos: setas navegam, `a` aprova, `r` rejeita. Rejeicao **exige motivo** — e esse
motivo que alimenta o relatorio de desperdicio depois. Clicar na imagem marca o **ponto
focal**: e ele que manda no recorte de todas as variantes da exportacao. Sem clique, o
sistema detecta sozinho a regiao com mais detalhe.

O que olhar, na ordem:

1. **tipografia e logotipo**, letra a letra, sempre que houver embalagem em quadro. Um
   glifo estranho ja e rejeicao;
2. **maos** — dedos, juntas, unhas;
3. **rosto**, inclusive parcial, refletido ou desfocado ao fundo;
4. **veracidade da cena** — ela afirma algo sobre a operacao que nao e verdade?
5. **coerencia com o acervo** — parece a nossa fazenda ou parece banco de imagens?

---

## 10. Exportar

```bash
cie export --approved --formats 9:16,4:5,1:1 --out ./export
```

So exporta o que foi aprovado (`--all` e recusado de proposito). Para cada aprovada, o
recorte e feito na proporcao pedida **sem distorcer**, centrado no ponto focal, e o
arquivo sai assim:

```
CANASTRA_[PILAR]_[TEMPLATE]_[NNN]_[AR].jpg
CANASTRA_3_MACRO_GRAO_TORRADO_001_9-16.jpg
```

`NNN` e o id da geracao, entao o nome e estavel entre lotes; o `:` da proporcao vira `-`
porque dois-pontos quebra nome de arquivo no Windows e em URL. Sai tambem:

- **XMP + EXIF embutidos** com modelo, data, template, assets de referencia e o
  principio da casa;
- **`<arquivo>.jpg.xmp`** ao lado, porque plataforma de rede social apaga metadados no
  upload;
- **`manifest.json`** do lote, com uma entrada por imagem: `generation_id`, `job_id`,
  template, pilar, prompt, modelo, seed, `reference_asset_ids`, sha256,
  `disclosure_required`, a frase de proveniencia e a instrucao de rotulagem.

---

## 11. Publicar

Abra o `manifest.json` do lote. Para cada imagem com `disclosure_required: true` — que
na pratica sao todas — ative a marcacao de conteudo de IA da plataforma: no
Instagram/Meta, em "Configuracoes avancadas" do post, e a mesma marcacao para Reels e
Stories. Os metadados do arquivo nao substituem isso: o upload costuma descarta-los.

O manifesto e o registro de proveniencia do lote. Guarde-o junto com as imagens; e ele
que responde, meses depois, "de onde veio essa foto".

---

## 12. Custo

```bash
cie models                                        # catalogo e precos conhecidos
cie report costs --since 2026-08-01
cie report costs --since 2026-08-01 --monthly-budget 50
```

Precos do catalogo semente (**nao confirmados** contra a documentacao da xAI enquanto a
sondagem nao rodar — ver [SONDAGEM-API.md](SONDAGEM-API.md)):

| Modelo | 1K | 2K |
|---|---|---|
| `grok-imagine-image` (padrao) | US$ 0,02 | US$ 0,02 |
| `grok-imagine-image-quality` | US$ 0,05 | US$ 0,07 |
| `grok-imagine-image-2.0` | US$ 0,04 a 0,06 | US$ 0,06 a 0,08 |

Quanto custa cada tipo de lote, com o modelo padrao a US$ 0,02 por imagem:

| Lote | Imagens | Estimativa |
|---|---|---|
| um teste de template | 1 | US$ 0,02 |
| um lote normal de cena | 4 | US$ 0,08 |
| um plano semanal tipico | 20 | US$ 0,40 |
| um mes de producao continua | ~80 | US$ 1,60 |
| a sondagem da API, uma vez | ate ~19 pedidos | US$ 0,05 a 0,40 |

Some o retrabalho: com metade das imagens rejeitadas na revisao, o custo por imagem
publicavel dobra. E exatamente isso que `cie report costs` mostra — ele divide o custo
**total** do periodo pelo numero de aprovadas, porque uma imagem que so ficou boa na
quinta tentativa custou as cinco. O relatorio quebra o gasto por modelo, template, pilar
e dia, e a projecao mensal (`--monthly-budget`) parte da media diaria observada.

`cie dna build --execute` usa o endpoint de chat com visao, com ate 15 imagens anexadas.
Esse custo nao esta no catalogo de imagem e nao entra na estimativa — e uma chamada por
perfil, nao por post.

---

## 13. Como ler o `quality_score`

Numero de 0 a 100, calculado localmente, sem rede e sem modelo:

```
score = 0,50 x nitidez + 0,25 x exposicao + 0,25 x resolucao
```

- **nitidez** — variancia do Laplaciano, em escala logaritmica, medida sempre a 1024 px
  para nao premiar arquivo grande;
- **exposicao** — contraste do histograma, com penalidade para preto e branco estourados;
- **resolucao** — 0 abaixo de 600 px de lado menor, 100 a partir de 2000 px.

| Faixa | Leitura | O que fazer |
|---|---|---|
| 85+ | excelente | candidata natural a Style DNA e a referencia |
| 70 a 84 | boa | serve de referencia se tiver 1200 px de lado menor |
| 50 a 69 | media | serve de documentacao interna, nao de referencia |
| abaixo de 50 | fraca | fora do trabalho de geracao |

**`is_reference_grade` exige as duas coisas: score >= 70 e lado menor >= 1200 px.** O
score e heuristica, nao juri: uma macro deliberadamente desfocada pode pontuar baixo e
ainda assim ser a melhor referencia de clima que voce tem — nesse caso, promova a mao
com `cie assets curate <id> --reference`.

---

## 14. Problemas comuns

| Sintoma | Causa provavel | Solucao |
|---|---|---|
| `bloqueado por no_synthetic_identifiable_faces` | referencia com pessoa e sem termo | `cie assets curate <id> --consent` (com termo arquivado) ou `--no-person` se nao ha rosto; ou troque a referencia |
| `bloqueado por packaging_requires_reference` | template de embalagem sem packshot real | passe `--reference <ids>` com uma foto marcada `--packaging`, ou rode com `--use-compositor` |
| `bloqueado por reference_quality` | asset nao e `is_reference_grade` | escolha outro em `cie assets list --reference`, ou promova com `cie assets curate <id> --reference` |
| `bloqueado por n_within_limits` com `n` pequeno | depois da sondagem, `.cie/models.yaml` limitou `max_n` a 1 ou 2 | quebre a tiragem em varios jobs, ou ajuste `max_n` no `.cie/models.yaml` com base no que a API aceitar |
| `bloqueado por aspect_ratio_supported` | proporcao fora da lista do modelo (ex.: `4:5`) | gere numa proporcao suportada; `4:5` sai do recorte local na exportacao |
| aviso `native_reference_capability` em todo job | a sondagem nunca rodou | normal: o sistema esta em modo descritivo. Rode `scripts/probe_api.py` numa maquina com rede |
| `nenhum modelo com visao configurado` | `cie dna build --execute` sem `CIE_VISION_MODEL` nem sondagem | defina `CIE_VISION_MODEL` no `.env` ou rode a sondagem |
| `XAI_API_KEY ausente` | `.env` nao preenchido | copie `.env.example` para `.env` e preencha; a chave nunca e impressa pelo CIE |
| ingestao marcou tudo como `needs_review` | nomes fora da convencao | renomeie seguindo `CANASTRA_[PILAR]_[LOCAL]_[ASSUNTO]_[NNN]`, ou cure na UI |
| arquivo entrou sem dimensoes e sem score | RAW/HEIC sem decoder | `uv sync --group dev --extra heic`, ou exporte JPEG do RAW |
| foto nao entrou e apareceu como duplicada | mesmo sha256 ja no catalogo | e o dedupe funcionando; confira com `cie assets list` |
| a fila parou no meio | teto de orcamento atingido | `cie queue run` de novo com `--budget-usd` maior; os pendentes continuam la |
| job `failed` com corpo de erro da API | 4xx/5xx da xAI | leia o `motivo` em `cie queue list --status failed`; 4xx costuma ser parametro nao suportado |
| exportacao reclamou que a imagem e pequena demais | recorte pedido nao cabe na geracao | gere numa proporcao mais proxima da final, ou tire esse formato do `--formats` |
| rotulo saiu com letra estranha | difusao deformando tipografia | rejeite, e refaca com `--use-compositor` a partir do recorte real em `assets/cutouts/` |

---

## Referencias

- [POLITICA-IA.md](POLITICA-IA.md) — o que pode e o que nao pode ser gerado, e por que.
- [SONDAGEM-API.md](SONDAGEM-API.md) — o que ainda nao sabemos sobre a API e como
  descobrir.
