# Canastra Image Engine (CIE)

Sistema local de geracao de imagem assistida por IA para o **Cafe Canastra**, ancorado
na base de fotos reais da operacao — fazenda em Medeiros/MG (~1.250 m, familia Boaventura
desde 1985) e microtorrefacao em Uberlandia/MG.

> ### A IA edita e estende o real; a IA nao inventa o real.
>
> Isso nao e slogan de README. E validacao executavel em [`cie/guardrails.py`](cie/guardrails.py),
> chamada antes de qualquer requisicao a API — bloqueando **antes de gastar credito** — e coberta
> por testes unitarios regra a regra.

A marca vende autenticidade e rastreabilidade farm-to-cup. Uma estetica sintetica generica
contradiz a promessa comercial do produto. Por isso o sistema inteiro e desenhado para usar a
base de fotos reais como materia-prima, nao para substitui-la.

---

## O que o sistema garante, no codigo

| Garantia | Onde vive |
|---|---|
| Rosto de pessoa real identificavel nunca e sintetizado | `guardrails.no_synthetic_identifiable_faces` + `face_regeneration_forbidden` |
| Embalagem com logotipo/texto legivel nunca nasce do zero | `guardrails.packaging_requires_reference` + trilha do `cie/compositor.py` |
| Toda imagem carrega proveniencia (modelo, prompt, referencias, data, custo) | tabela `generations` + XMP/EXIF da exportacao |
| Toda imagem sabe se precisa de rotulagem de IA | `generations.disclosure_required` + `manifest.json` do lote |
| Nada gasta credito por acidente | `--dry-run` e o padrao de `generate` e `queue run`; `--execute` exige `--budget-usd` |
| Nenhum parametro de API foi inventado | tudo atras de `cie/capabilities.py`, preenchido por `scripts/probe_api.py` |

Os campos `has_identifiable_person` e `consent_on_file` **nunca** sao preenchidos pela maquina.
Entram no default mais restritivo (pessoa presumida presente, consentimento ausente) e so mudam
por acao humana explicita, na UI de curadoria ou via `cie assets curate`.

---

## Instalacao

```bash
uv venv --python 3.11
uv sync --group dev
cp .env.example .env        # preencha XAI_API_KEY
```

Fotos de celular em HEIC exigem o extra opcional:

```bash
uv sync --group dev --extra heic
```

`XAI_API_KEY` vem exclusivamente do ambiente (lida de `.env` via python-dotenv). `.env` esta no
`.gitignore` e a chave nunca e impressa — nem em mensagem de erro: todo texto de erro da API passa
por `config.redact()` antes de ser guardado ou exibido.

---

## Antes de tudo: rode a sondagem

O ambiente onde este sistema foi construido **nao tinha acesso de rede a `api.x.ai` nem a
`docs.x.ai`**. Nenhum parametro de API foi assumido. `scripts/probe_api.py` responde
empiricamente as perguntas que a arquitetura depende:

```bash
python scripts/probe_api.py --dry-run     # mostra o plano, nao gasta nada
python scripts/probe_api.py --yes         # roda de verdade (custa alguns centavos)
```

Ele grava `.cie/capabilities.json` e `.cie/models.yaml`. Consulte o resultado com:

```bash
uv run cie probe
uv run cie models
```

**O que muda com a resposta:** se a API aceitar imagem de referencia, o sistema passa a usar a
`NativeReferenceStrategy` (ate 3 referencias por request, ordenadas por `quality_score`). Enquanto
nao houver prova, ele usa a `DescriptorReferenceStrategy` — consistencia vem do Style DNA textual
extraido das suas proprias fotos. Detalhes em [docs/SONDAGEM-API.md](docs/SONDAGEM-API.md).

---

## Fluxo de trabalho

```bash
# 1. popular o catalogo a partir da base de fotos reais
uv run cie ingest ./assets/originals --verbose

# 2. curadoria humana (campos de politica, qualidade de referencia)
uv run cie assets review               # abre a UI em http://127.0.0.1:8765/assets
uv run cie assets list --needs-review

# 3. destilar o estilo real da operacao em texto reutilizavel
uv run cie dna build --pillar 3 --name "laboratorio-uberlandia"   # modo seco
uv run cie dna build --pillar 3 --name "laboratorio-uberlandia" --execute
uv run cie dna list

# 4. carregar as cenas
uv run cie templates sync
uv run cie templates list

# 5. trabalhar em modo seco - o padrao mental do sistema
uv run cie generate --template macro_grao_torrado --dna laboratorio-uberlandia --n 4

# 6. planejar a semana e rodar com teto rigido de orcamento
uv run cie queue add --from-plan plans/semana-01.yaml
uv run cie queue run --limit 20 --budget-usd 5.00 --execute

# 7. aprovar/rejeitar
uv run cie review                      # http://127.0.0.1:8765/review

# 8. exportar para publicacao
uv run cie export --approved --formats 9:16,4:5,1:1 --out ./export

# 9. acompanhar custo
uv run cie report costs --since 2026-08-01 --monthly-budget 50
```

`--dry-run` imprime o prompt final resolvido, o custo estimado e o veredito de cada guardrail,
**sem chamar a API**. E o default de `generate` e de `queue run`.

---

## Como a base de fotos vira consistencia

Duas estrategias atras da mesma interface (`cie/reference/base.py`):

**`DescriptorReferenceStrategy`** (padrao). Em duas etapas:

1. **Extracao de Style DNA**, offline, uma vez por conjunto: 8 a 15 fotos reais aprovadas vao para
   o endpoint de chat com visao, que devolve JSON estrito com paleta, qualidade de luz, lente,
   textura, enquadramento, materiais recorrentes, mood e lista de coisas a evitar.
2. **Composicao do prompt** (`cie/prompt.py`), sempre nesta ordem: corpo do template com variaveis
   resolvidas → `prompt_fragment` do Style DNA → ancoras tecnicas fotograficas → negative prompt.
   O resultado e persistido em `jobs.resolved_prompt` para auditoria.

**`NativeReferenceStrategy`**. Envia as imagens direto no request — **somente** se a sondagem
confirmar suporte. Maximo de 3 referencias, ordenadas por `quality_score`.

**Modo hibrido para produto.** Quando o template e `product_shot` e existe foto real do SKU, o
sistema prefere composicao local (`cie/compositor.py`): recorte do produto real sobre fundo gerado.
Assim o rotulo permanece real e legivel, em vez de deixar a difusao inventar tipografia. Coloque
PNGs ja recortados (com alfa) em `assets/cutouts/`.

---

## Convencao de nomes da base

```
CANASTRA_[PILAR]_[LOCAL]_[ASSUNTO]_[NNN].ext
CANASTRA_3_TORREFACAO_TAMBOR_007.jpg
```

`PILAR` aceita `1..4`, `product` ou `people`. `LOCAL` aceita `FAZENDA`/`MEDEIROS`,
`TORREFACAO`/`UBERLANDIA`, `ESTUDIO`, `OUTRO`. Quando o nome nao segue a convencao, a ingestao
tenta tokens do caminho e o GPS do EXIF; se ainda assim nao fechar, o asset entra como
`needs_review`. **O sistema nunca chuta.**

Se o nome do arquivo e o GPS discordarem, o nome vence (e curadoria humana explicita) e o conflito
fica registrado em `notes`, com o asset marcado para revisao.

---

## Os quatro pilares de conteudo

1. **Terroir e Tradicao** — fazenda, altitude, colheita seletiva, familia, terreiro de secagem.
2. **Sustentabilidade e Engenharia Agricola** — painel solar, carbono zero, Arara e Catuai 2SL.
3. **Laboratorio de Torrefacao e Sensorialidade** — tambor, first crack, cupping, macro de grao.
4. **Educacao e Cultura Brewing** — V60, coador, drip, capsula, harmonizacao com queijo da Canastra.

12 cenas prontas em [`templates/`](templates), cobrindo os quatro pilares. Corpo dos prompts em
ingles (os modelos respondem melhor), comentarios em portugues.

---

## Arquitetura

```
cie/
  guardrails.py     as regras inegociaveis, chamadas antes de qualquer chamada a API
  capabilities.py   o que a API aceita de verdade (preenchido pela sondagem)
  pricing.py        catalogo de modelos e estimativa de custo
  prompt.py         PromptComposer
  reference/        NativeReferenceStrategy | DescriptorReferenceStrategy
  dna.py            extracao de Style DNA via modelo com visao
  queue.py          fila com teto rigido de orcamento
  xai.py            cliente httpx async com retry, backoff, jitter e 429
  compositor.py     composicao local produto real sobre fundo gerado
  export.py         recorte inteligente, XMP/EXIF, manifesto
  reports.py        custo por modelo, template, pilar e dia
  web/              UI de curadoria e de revisao (FastAPI + HTMX + Tailwind CDN)
  ingest.py         varredura, dedupe, EXIF, thumbnails, quality_score local
scripts/probe_api.py   sondagem empirica da API (fora da suite de testes)
```

Sem torch, sem modelo local, sem build step de front-end, sem dependencia de nuvem alem da API da
xAI. O `quality_score` e heuristica classica local: variancia do Laplaciano para nitidez,
histograma para exposicao, e resolucao minima.

---

## Testes

```bash
uv run pytest
uv run pytest --cov=cie --cov-report=term-missing
```

Nenhum teste toca a API real — o cliente e exercitado com `httpx.MockTransport` (sucesso, 429, 5xx,
payload malformado) e a sondagem e um script separado, fora da suite.

---

## Documentacao

- [docs/OPERACAO.md](docs/OPERACAO.md) — guia do dia a dia, do arquivo bruto ao post publicado.
- [docs/POLITICA-IA.md](docs/POLITICA-IA.md) — politica de uso de IA da marca, pronta para publicar.
- [docs/SONDAGEM-API.md](docs/SONDAGEM-API.md) — perguntas em aberto sobre a API e como responde-las.

---

## Restricoes de projeto

A base de fotos reais nunca sai do diretorio do projeto: so derivados trafegam (thumbnails locais e,
no momento do request, bytes em base64 de referencias redimensionadas). Nenhuma chamada de rede
acontece fora de `api.x.ai`.
