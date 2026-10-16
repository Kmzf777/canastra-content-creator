# Detector de virada — plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `scripts/virada.py` + skill `canastra-virada`, que acham em que post um perfil do
Instagram mudou de patamar (degrau, queda) ou só estourou (pico) e geram JSON + HTML
cronológico.

**Architecture:** script único, só stdlib (roda com `python` puro, sem o venv do `cie`),
em camadas puras e testáveis: leitura do `.jsonl` do fluxo 1 → `detectar()` sobre uma lista
de números → `antes_depois()` sobre os posts → `analisar()` monta o relatório →
`render_html()` → `main()`. Spec: `docs/superpowers/specs/2026-10-15-detector-virada-design.md`.

**Tech Stack:** Python 3.11 stdlib (`statistics.median`, `math.log1p`, `argparse`), pytest.
O módulo é carregado nos testes por `importlib`, como em `tests/test_pega_download.py`,
porque `scripts/` não é pacote.

**Restrições da sessão:** só se tocam `scripts/virada.py`, `tests/test_virada.py`,
`.claude/skills/canastra-virada/`, `instagram/viradas/` e estes dois documentos.
**Sem commit** até o Rafael pedir: os passos de commit do modelo ficam de fora.

---

## Mapa de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `scripts/virada.py` | leitura, detecção, antes×depois, relatório, HTML, CLI |
| `tests/test_virada.py` | uma função por caso da spec, com as séries geradas no teste |
| `.claude/skills/canastra-virada/SKILL.md` | roteamento, pré-condição, rodar, ler, passo qualitativo, limites |
| `instagram/viradas/<handle>/<data>.{json,html}` | saída (gerada, não escrita à mão) |

Interfaces públicas do módulo, nomes fixos para todas as tarefas:

```python
PADROES = {"k": 12, "m": 8, "pico": 3.0, "degrau": 1.8, "queda": 0.55, "sustentacao": 0.6}
class PerfilAusente(Exception): ...
@dataclass class Post: id, url, data, tipo, legenda, curtidas, comentarios, views, seguidores, coletado_em
                       # propriedade .engajamento -> int | None
def normalizar_handle(handle: str) -> str
def parse_data(valor) -> datetime | None
def ler_jsonl(caminho: Path) -> tuple[list[Post], dict]          # contagem: linhas, invalidas, duplicados
def localizar(handle: str, raiz: Path) -> Path                    # levanta PerfilAusente
def detectar(valores, k, m, pico, degrau, queda, sustentacao) -> dict
    # {"base": [...], "razao": [...], "nivel": [...], "estados": [...], "eventos": [{"tipo", "i", ...}]}
def antes_depois(posts, valores, i, k, m) -> dict                 # {"antes", "depois", "puxaram", "palavras_novas", "hashtags_novas"}
def analisar(perfil, fonte, posts, contagem, params, hoje, dias, maturidade) -> dict
def render_html(rel: dict) -> str
def gravar(rel: dict, pasta: Path) -> tuple[Path, Path]
def main(argv: list[str] | None = None) -> int                   # 0 ok, 2 perfil ausente
```

---

### Task 1: leitura do contrato do fluxo 1

**Files:** Create `scripts/virada.py`, `tests/test_virada.py`

- [ ] **Step 1: testes que falham.** `_linhas(valores, passo=3, tipo="REEL", legendas=None)`
  gera dicionários no formato do contrato, a partir de 01/01/2026 12:00 UTC. `_grava(tmp, nome, linhas)`
  escreve o `.jsonl`. Casos:
  - `test_dedup_fica_coleta_mais_recente`: dois registros do mesmo `id`, o mais novo com
    `curtidas=99`, nas duas ordens de linha → 1 post com 99, `duplicados == 1`;
  - `test_linha_invalida_contada`: `"não é json"`, linha sem `id` e linha com
    `data_publicacao: "ontem"` → `invalidas == 3` e os válidos lidos;
  - `test_datas_iso_variantes`: `Z`, `+0000` e `+00:00` dão o mesmo instante;
  - `test_localizar_proprio_e_concorrente`: `@CafeCanastra` → `proprios.jsonl`, `orfeucafes`
    → `concorrentes/orfeucafes.jsonl`;
  - `test_perfil_ausente_mensagens`: sem pasta → menção a "fluxo 1"; com `watchlist.json`
    contendo `["@fulano"]` → "está na watchlist"; fora dela → "não está na watchlist".
- [ ] **Step 2:** `python -m pytest tests/test_virada.py -q --noconftest` → falha por módulo ausente.
- [ ] **Step 3:** implementar `Post`, `normalizar_handle`, `parse_data` (troca `Z` e
  `±HHMM` para `±HH:MM`; sem fuso = UTC), `ler_jsonl` (dedup por `id`, fica o maior
  `coletado_em`; em caso de empate, a linha posterior), `localizar`, `na_watchlist` (anda pelo
  JSON inteiro coletando strings, porque o formato da watchlist ainda não foi publicado).
- [ ] **Step 4:** rodar → passa.

### Task 2: detecção (degrau, queda, pico)

**Files:** Modify `scripts/virada.py`, `tests/test_virada.py`

- [ ] **Step 1: testes que falham**, chamando `detectar(valores, **PADROES)`:
  - `test_degrau_limpo`: `[50]*20 + [200]*20` → eventos `[("degrau", 20)]`; posts 21–27 com
    estado `puxador`; nenhum pico;
  - `test_queda`: `[200]*20 + [50]*20` → `[("queda", 20)]`;
  - `test_escada_da_dois_degraus`: `[50]*20 + [200]*20 + [800]*20` → degraus em 20 e 40;
  - `test_pico_isolado`: `[50]*15 + [400] + [50]*15` → `[("pico", 15)]`, `confirmado` True;
  - `test_pico_recente_nao_confirmado`: `[50]*15 + [400]` → pico, `confirmado` False;
  - `test_ruido_sem_evento`: 60 valores `50 × U(0,7; 1,3)` com `random.Random(7)` → nenhum evento;
  - `test_sem_base_nos_primeiros`: estados 0–5 = `sem_base`.
- [ ] **Step 2:** rodar → falha.
- [ ] **Step 3:** implementar segundo a spec: base = mediana dos `k` anteriores (≥ 6);
  nível = mediana(i..i+m−1)/base (≥ 5 adiante); candidato de degrau com nível ≥ `degrau` e
  fração acima ≥ `sustentacao`, de queda com o espelho; seleção gulosa por contraste de
  `média(log1p)` com raio de exclusão `m`; puxador = post da janela de um degrau com
  `v ≥ pico × base`; pico = razão ≥ `pico`, não ponto nem puxador, mediana dos seguintes
  < 1,5 × base; `confirmado` se há ≥ 3 seguintes. Divisor `max(base, 1)` para perfil com 0.
- [ ] **Step 4:** rodar → passa.

### Task 3: o que mudou ao redor

**Files:** Modify `scripts/virada.py`, `tests/test_virada.py`

- [ ] **Step 1: teste que falha** `test_antes_depois`: 20 posts `IMAGE` a cada 7 dias, valor
  50, legenda `"foto do dia no sítio"`; depois 20 `REEL` a cada 2 dias, valor 200, legenda
  `"Você sabia? torra clara de verdade #torraclara"`. Em `i = 20`: formatos antes
  `{"IMAGE": 12}`, depois `{"REEL": 8}`; cadência antes 1,0 e depois 3,5 posts/semana;
  `"torra"`, `"clara"` e `"sabia"` em `palavras_novas`; `"torraclara"` em `hashtags_novas`;
  `puxaram` com 8 itens e `primeira_linha` igual à legenda.
- [ ] **Step 2:** rodar → falha.
- [ ] **Step 3:** implementar `_janela` (posts, de/até, formatos, cadência = (n−1)/span×7,
  intervalo mediano, legenda mediana, hashtags medianas), `primeira_linha` (1ª linha não
  vazia, até 140 caracteres), `_palavras` (sem `#…`, `@…` e links; `[^\W\d_]{4,}`; sem
  stopwords), `_hashtags`, `_novas` (por presença em post: ≥ 2 depois, 0 antes, top 15).
- [ ] **Step 4:** rodar → passa.

### Task 4: relatório e CLI

**Files:** Modify `scripts/virada.py`, `tests/test_virada.py`

- [ ] **Step 1: testes que falham:**
  - `test_imaturos_fora_da_deteccao`: `[50]*15 + [400]`, o 400 um dia antes de `hoje` →
    estado `imaturo`, `contagens.imaturos == 1`, sem pico;
  - `test_janela_dias`: 40 posts, `dias=30` → só os dos últimos 30 dias,
    `fora_da_janela` contado;
  - `test_serie_curta_avisa`: 8 posts → aviso com "série curta", sem eventos;
  - `test_views_so_com_maioria`: metade com views → só `engajamento` + aviso; todos → `views`;
  - `test_main_grava_json_e_html`: `main([... "--metricas", tmp, "--saida", tmp/"out", "--hoje", "2026-06-01", "--dias", "0"])`
    → 0; JSON com o degrau; HTML com `<svg`, a URL do post do degrau e "Degrau sustentado";
  - `test_main_perfil_ausente_sai_2`: código 2 e "fluxo 1" no stderr.
- [ ] **Step 2:** rodar → falha.
- [ ] **Step 3:** implementar `analisar` (janela, maturidade, série de engajamento, série de
  views se ≥ 60%, eventos com o post e `antes_depois`, `seguidores_coleta` com aviso),
  `gravar`, `resumo`, `main` (`--dias --maturidade --k --m --pico --degrau --queda
  --sustentacao --arquivo --metricas --saida --hoje`; `sys.stdout.reconfigure("utf-8")` só
  no `__main__`).
- [ ] **Step 4:** rodar → passa.

### Task 5: HTML

**Files:** Modify `scripts/virada.py`, `tests/test_virada.py`

- [ ] **Step 1: teste que falha** `test_html_autocontido`: sem `http` fora dos links de post
  (nenhum `<script src`, nenhum `<link`), `prefers-color-scheme`, um `<a href>` por post com
  valor, uma faixa por degrau, um anel por pico, e o texto escapado (legenda com `<b>` não
  vira tag).
- [ ] **Step 2:** rodar → falha.
- [ ] **Step 3:** implementar `render_html`: SVG 1000×360 em `viewBox`, x linear no tempo,
  y em log10(1+v) com marcas 1-2-5, meses no eixo x (passo que deixa ≤ 12 marcas), base em
  tracejado, faixas de degrau/queda pelas datas de `antes_depois.depois`, anéis nos picos,
  imaturos vazados; a legenda das cores; um cartão por evento; números em pt-BR.
- [ ] **Step 4:** rodar a suíte do arquivo → passa.

### Task 6: skill `canastra-virada`

**Files:** Create `.claude/skills/canastra-virada/SKILL.md`

- [ ] Frontmatter `name`/`description` ("Use when…"), tabela "Rotear primeiro", pré-condição
  da coleta e fallback pelo Chrome, comandos, como ler (degrau × pico × queda ×
  imaturo × não avaliável), passo qualitativo com `indice_referencias.py buscar` e o critério
  para fichar, publicação do HTML como Artifact, limites de leitura.

### Task 7: rodada de ponta a ponta

- [ ] Gerar uma série realista (fixture de demonstração em scratchpad: ruído, um pico, um
  degrau com mudança de formato e cadência), rodar o CLI com `--arquivo`, abrir o HTML no
  navegador embutido, conferir no pixel (pontos, faixas, cartões, celular e modo escuro).
- [ ] Rodar o detector numa série real se o fluxo 1 já tiver gravado `instagram/metricas/`.
- [ ] Publicar o HTML de demonstração como Artifact.
