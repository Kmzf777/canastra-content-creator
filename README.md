# Canastra Image Engine (CIE)

Sistema local de geracao de imagem assistida por IA para o **Cafe Canastra**, ancorado
na base de fotos reais da operacao (fazenda em Medeiros/MG e microtorrefacao em
Uberlandia/MG).

> **Principio inegociavel:** a IA edita e estende o real; a IA nao inventa o real.
>
> Isso nao e slogan de README: e validacao executavel em `cie/guardrails.py`, chamada
> antes de qualquer requisicao a API e coberta por testes.

## Estado atual

| Fase | Escopo | Situacao |
|---|---|---|
| 1 | Esqueleto, modelos, SQLite + migracoes, ingestao, CLI basica, testes | **em andamento** |
| 2 | Guardrails, templates YAML, `PromptComposer`, `--dry-run` ponta a ponta | pendente |
| 3 | Sondagem da API xAI, cliente, `ReferenceStrategy`, fila com orcamento, Style DNA | pendente |
| 4 | UI de curadoria e revisao, compositor de produto, exportacao | pendente |
| 5 | Relatorios de custo, guia de operacao, politica de uso de IA | pendente |

## Instalacao

```bash
uv venv --python 3.11
uv sync --group dev
cp .env.example .env   # preencha XAI_API_KEY quando chegar a fase 3
```

HEIC (fotos de celular) exige o extra opcional:

```bash
uv sync --group dev --extra heic
```

## Uso (fase 1)

```bash
uv run cie ingest ./assets/originals --verbose
uv run cie assets list --pillar 3
uv run cie assets show 12
uv run cie assets curate 12 --no-person --reference --done
uv run cie db status
```

### Convencao de nomes da base

```
CANASTRA_[PILAR]_[LOCAL]_[ASSUNTO]_[NNN].ext
CANASTRA_3_TORREFACAO_TAMBOR_007.jpg
```

`PILAR` aceita `1..4`, `product` ou `people`; `LOCAL` aceita `FAZENDA`/`MEDEIROS`,
`TORREFACAO`/`UBERLANDIA`, `ESTUDIO`, `OUTRO`. Quando a inferencia nao fecha, o asset
entra como `needs_review` — o sistema nunca chuta.

### Campos que a maquina nunca preenche

`has_identifiable_person` e `consent_on_file` entram sempre no default mais restritivo
(pessoa presumida presente, consentimento ausente) e so mudam por acao humana, via
`cie assets curate` ou pela UI de curadoria.

## Testes

```bash
uv run pytest
```

Nenhum teste toca a API real.
