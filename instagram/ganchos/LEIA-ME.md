# Máquina de ganchos: dados

Os dados da skill [`canastra-ganchos`](../../.claude/skills/canastra-ganchos/SKILL.md). A
rubrica e o léxico de vícios ficam na skill; aqui ficam o corpus, os padrões e o registro.

| Arquivo | O que é | Quem escreve |
|---|---|---|
| `corpus.jsonl` | 128 ganchos de Reel viral (vê / escrito / dito + views, curtidas, idioma, etiqueta, link) | `python scripts/ganchos.py extrair` |
| `padroes-mapa.json` | cada gancho do corpus → um dos 9 padrões, e as fórmulas de lacuna de cada padrão (julgamento) | à mão |
| `padroes.md` | padrões com n, mediana de views e exemplos; medidas do corpus; vícios | `python scripts/ganchos.py padroes` |
| `avaliacoes.jsonl` | todo gancho gerado ou avaliado, com nota por regra; `escolhido: true` = o publicado | `checar --registrar` |
| `recalibracao-AAAA-MM-DD.md` | proposta de pesos a partir do resultado real | `python scripts/ganchos.py recalibrar` |
| `contraste-AAAA-MM-DD.md` | vencedores × perdedores por perfil (corte na mediana do perfil), a partir de `instagram/metricas/concorrentes/` e `proprios.jsonl` | `python scripts/ganchos.py contrastar` |
| `ciclo1-capas-20a30-10.md` | primeira rodada da máquina: capas para os carrosséis de 20/10 a 30/10 | sessão de 15/10/2026 |

## Ficha nova em `instagram/referencias-virais/`?

```bash
python scripts/ganchos.py extrair
python scripts/ganchos.py padroes     # recusa se o mapa não cobrir algum id novo
```

Acrescente o id novo em `padroes-mapa.json` e rode `padroes` de novo.

## Post publicado?

Registre o gancho **com o texto exato da capa** e `--escolhido --post <shortcode>`. É assim que
o resultado do fluxo 1 (`instagram/metricas/proprios.jsonl`, campo `gancho`) encontra a
avaliação na hora de recalibrar.

## Comparar o gancho do Rafael com os gerados

```bash
python scripts/ganchos.py ranking --tema "<tema>"
```
