# Máquina de ganchos: plano de implementação

> **Para agentes:** sub-skill obrigatória: superpowers:executing-plans (inline, nesta sessão).
> As etapas usam checkbox (`- [ ]`). **Não commitar**: o Rafael pediu que nada vá para o git
> sem pedido dele. Onde o método manda commitar, esta versão diz "sem commit".

**Objetivo:** a skill `canastra-ganchos` gera e avalia ganchos de capa de carrossel e de
Reel com uma rubrica de 18 regras tirada de dados reais. A recalibração pelos nossos
resultados já fica desenhada.

**Arquitetura:** `scripts/ganchos.py` cuida do que é reproduzível:

- extrai os 130 ganchos das fichas de virais
- mede os padrões
- aplica as regras mecânicas da rubrica
- calcula a nota a partir dos julgamentos que recebe
- recalibra pelo `proprios.jsonl`

A rubrica (`rubrica.md`) e o léxico de vícios de IA (`vicios-ia.md`) são a **fonte
única**: o script lê as tabelas desses arquivos. O julgamento (lacuna, promessa, contraste)
fica com o Claude, e a skill diz como fazer.

**Stack:** Python 3.11, só biblioteca padrão. pytest (`python -m uv run pytest`).

Spec: `docs/superpowers/specs/2026-10-15-maquina-ganchos-design.md`.

**Ajuste em relação à spec:** os nossos carrosséis entram como **avaliações** em
`avaliacoes.jsonl`, e não no corpus. O sidecar não guarda o texto da capa, e é a avaliação
que se cruza com a métrica. O corpus fica só com os virais.

---

## Mapa de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `scripts/ganchos.py` | criar: parser de camadas, `extrair`, `medir`, `padroes`, rubrica, regras mecânicas, `avaliar`, `recalibrar`, CLI |
| `tests/test_ganchos.py` | criar |
| `.claude/skills/canastra-ganchos/vicios-ia.md` | criar: tabela com `regex` e `proibe` |
| `.claude/skills/canastra-ganchos/rubrica.md` | criar: tabela de 18 regras |
| `.claude/skills/canastra-ganchos/SKILL.md` | criar |
| `instagram/ganchos/corpus.jsonl` | gerado |
| `instagram/ganchos/padroes-mapa.json` | à mão |
| `instagram/ganchos/padroes.md` | gerado |
| `instagram/ganchos/avaliacoes.jsonl` | gerado (sementes: os 2 carrosséis já feitos) |
| `instagram/ganchos/LEIA-ME.md` | criar: o que é cada arquivo, o que é gerado e o que é à mão |

---

### Tarefa 1: parser de camadas e `extrair`

**Arquivos:** criar `scripts/ganchos.py` e `tests/test_ganchos.py`.

- [ ] **1.1 Teste que falha.** `tests/test_ganchos.py`:

```python
"""Máquina de ganchos (scripts/ganchos.py). `scripts/` não é pacote: carrega pelo caminho."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent


def _carrega():
    spec = importlib.util.spec_from_file_location("ganchos", RAIZ / "scripts" / "ganchos.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


g = _carrega()

# As 8 variantes de rótulo existem nas fichas (inventário de 15/10/2026).
SECAO_BRASIL = """- **Vê-se:** Ele no corredor de café segurando dois pacotes.
- **Escrito na tela:** "🔴 Não compre café ruim pra sua casa nunca mais" (caixa branca, serifa).
- **Dito:** "Não compre café ruim para sua casa, nunca mais. Tá vendo esse café aqui?"
"""
SECAO_PROCESSO = """- **Vê:** close de cima, mão despejando **grão verde** no funil.
- **Escrito:** nada. **Dito:** nada.
- Gancho = **antes e depois em 2 s**.
"""
SECAO_TABELA = """| Camada | Conteúdo |
|---|---|
| O que se VÊ | Lance atrás da bancada, gesticulando. |
| O que está ESCRITO | Legenda amarela: "COFFEE RECIPES ARE / TOO COMPLICATED" |
| O que é DITO | "Coffee recipes are too complicated, so let's make it a lot easier." |
"""
SECAO_MOTION = """- **VÊ:** tela dividida em três.
- **ESCRITO:** "FINAL RENDER", "VIEWPORT".
- **DITO-OUVIDO:** sem fala; trilha.
"""
SECAO_DITO_TEMPO = """- **Vê:** terreiro ao sol.
- **Escrito:** "Café na peneira"
- **Dito (0,0–2,7 s):** "Isso aqui é o que separa o café bom."
"""


def test_camadas_bullet_brasil():
    c = g.ler_camadas(SECAO_BRASIL)
    assert c["ve"].startswith("Ele no corredor")
    assert g.texto_citado(c["escrito"]) == "🔴 Não compre café ruim pra sua casa nunca mais"
    assert g.texto_citado(c["dito"]).startswith("Não compre café ruim")


def test_camadas_dois_rotulos_na_mesma_linha_e_negrito_que_nao_e_rotulo():
    c = g.ler_camadas(SECAO_PROCESSO)
    assert "grão verde" in c["ve"]
    assert g.texto_citado(c["escrito"]) == ""
    assert g.texto_citado(c["dito"]) == ""


def test_camadas_tabela():
    c = g.ler_camadas(SECAO_TABELA)
    assert c["ve"].startswith("Lance")
    assert g.texto_citado(c["escrito"]) == "COFFEE RECIPES ARE / TOO COMPLICATED"
    assert g.texto_citado(c["dito"]).startswith("Coffee recipes")


def test_camadas_motion_e_dito_com_tempo():
    c = g.ler_camadas(SECAO_MOTION)
    assert g.texto_citado(c["escrito"]) == "FINAL RENDER / VIEWPORT"
    assert g.texto_citado(c["dito"]) == ""
    c2 = g.ler_camadas(SECAO_DITO_TEMPO)
    assert g.texto_citado(c2["dito"]) == "Isso aqui é o que separa o café bom."


def test_texto_citado_aspas_simples_e_texto_sem_aspas():
    assert g.texto_citado("Legenda: 'Oh, Pumpkin Spice Latte?' / 'The drink'") == "Oh, Pumpkin Spice Latte? / The drink"
    assert g.texto_citado("Nada; música.") == ""
    assert g.texto_citado("Escolhendo café (amarelo)") == "Escolhendo café"


def test_extrair_corpus_real():
    corpus = g.extrair()
    assert len(corpus) >= 120                      # 130 fichas, 1 vídeo em duas frentes
    assert len({x["id"] for x in corpus}) == len(corpus)
    com_ve = sum(1 for x in corpus if x["ve"])
    assert com_ve / len(corpus) >= 0.95
    x = next(x for x in corpus if x["id"] == "DVMF38UgD0M")
    assert x["escrito"].startswith("🔴 Não compre")
    assert x["views"] and x["idioma"] == "pt"
```

- [ ] **1.2 Rodar e confirmar a falha:** `python -m uv run pytest tests/test_ganchos.py -q`.
  Esperado: erro de arquivo ausente.

- [ ] **1.3 Implementação mínima** em `scripts/ganchos.py`:

```python
"""Máquina de ganchos: corpus, padrões, checagem pela rubrica e recalibração.

    python scripts/ganchos.py extrair
    python scripts/ganchos.py padroes
    python scripts/ganchos.py checar --formato capa --manchete "..." [--apoio "..."]
           [--fonte "..."] [--julgamento J1=1,J2=0] [--json] [--registrar --tema T]
    python scripts/ganchos.py recalibrar [--proprios CAMINHO]

A rubrica e o léxico de vícios são fonte única: este script lê as tabelas de
.claude/skills/canastra-ganchos/{rubrica,vicios-ia}.md, nunca guarda cópia de peso.

Skill: .claude/skills/canastra-ganchos/ · Spec: docs/superpowers/specs/2026-10-15-maquina-ganchos-design.md
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FICHAS = RAIZ / "instagram" / "referencias-virais" / "videos"
INDICE = RAIZ / "instagram" / "referencias-virais" / "indice.json"
SAIDA = RAIZ / "instagram" / "ganchos"
SKILL = RAIZ / ".claude" / "skills" / "canastra-ganchos"
RUBRICA = SKILL / "rubrica.md"
VICIOS = SKILL / "vicios-ia.md"
PROPRIOS = RAIZ / "instagram" / "metricas" / "proprios.jsonl"


def sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


# --- parser das 8 variantes de rótulo ---------------------------------------

_ROTULO = re.compile(r"\*\*([^*\n]{1,40}?)\s*:\s*\*\*|\*\*([^*\n]{1,40}?)\*\*\s*:")
_LINHA_TABELA = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$")


def _classifica(rotulo: str) -> str | None:
    r = sem_acento(rotulo).lower()
    if "escrit" in r:
        return "escrito"
    if "dito" in r or "ouv" in r:
        return "dito"
    if re.search(r"\bve\b|\bve-se\b", r):
        return "ve"
    return None


def ler_camadas(secao: str) -> dict[str, str]:
    """Seção `## 2. Gancho` -> {ve, escrito, dito} com o conteúdo cru de cada rótulo."""
    linhas = []
    for linha in secao.splitlines():
        m = _LINHA_TABELA.match(linha.strip())
        if m and _classifica(m.group(1)):
            linhas.append(f"**{m.group(1)}:** {m.group(2)}")
        else:
            linhas.append(linha)
    texto = "\n".join(linhas)
    marcas = []
    for m in _ROTULO.finditer(texto):
        tipo = _classifica(m.group(1) or m.group(2))
        if tipo:
            marcas.append((m.start(), m.end(), tipo))
    camadas = {"ve": "", "escrito": "", "dito": ""}
    for i, (_, fim, tipo) in enumerate(marcas):
        prox = marcas[i + 1][0] if i + 1 < len(marcas) else len(texto)
        trecho = re.split(r"\n\s*-\s|\n\s*\n", texto[fim:prox])[0]
        if not camadas[tipo]:
            camadas[tipo] = trecho.strip().strip("-").strip()
    return camadas


_NADA = re.compile(r"^(nada|sem fala|nenhum|—|-)", re.I)


def texto_citado(conteudo: str) -> str:
    """O texto literal de uma camada: o que está entre aspas, ou o conteúdo sem descrição."""
    s = conteudo.strip()
    if not s or _NADA.match(s):
        return ""
    trechos = [a or b for a, b in re.findall(r'"([^"]+)"|“([^”]+)”', s)]
    if not trechos:
        trechos = re.findall(r"(?<!\w)'([^']+)'(?!\w)", s)
    if trechos:
        return " / ".join(t.strip() for t in trechos)
    s = re.sub(r"\([^)]*\)", "", s)
    return re.sub(r"\s+", " ", s).strip(" .;")


# --- corpus -----------------------------------------------------------------

def extrair(fichas: Path = FICHAS, indice: Path = INDICE) -> list[dict]:
    """Um registro por vídeo (deduplicado por id), com as 3 camadas e o resultado."""
    meta = {Path(x["arquivo"]).stem: x for x in json.loads(indice.read_text(encoding="utf-8"))}
    corpus, vistos = [], set()
    for arq in sorted(fichas.glob("*/*.md")):
        m = re.search(r"## 2\. Gancho[^\n]*\n(.*?)\n## 3", arq.read_text(encoding="utf-8"), re.S)
        x = meta.get(arq.stem)
        if not m or not x or x["id"] in vistos:
            continue
        vistos.add(x["id"])
        c = ler_camadas(m.group(1))
        corpus.append({
            "id": x["id"], "chave": arq.stem, "frente": x["frente"], "perfil": x["perfil"],
            "idioma": x["idioma"], "views": x.get("views"), "curtidas": x.get("curtidas"),
            "organico": x.get("organico"), "etiqueta": x["gancho"], "formato_video": x["formato"],
            "ve": c["ve"], "escrito": texto_citado(c["escrito"]), "dito": texto_citado(c["dito"]),
            "link": x.get("link"), "ficha": f"instagram/referencias-virais/{x['arquivo']}",
        })
    return corpus
```

- [ ] **1.4 Rodar:** `python -m uv run pytest tests/test_ganchos.py -q`. Esperado: PASS. Se
  `test_extrair_corpus_real` falhar porque `ve` está vazio em mais de 5%, liste as fichas
  sem `ve` e acrescente a variante de rótulo que faltou em `_classifica`. Não afrouxe o
  limite.
- [ ] **1.5 Sem commit.**

### Tarefa 2: léxico de vícios de IA, `medir` e `padroes`

**Arquivos:** criar `.claude/skills/canastra-ganchos/vicios-ia.md` e completar o script e
os testes.

- [ ] **2.1 Criar `vicios-ia.md`.** A tabela tem as colunas
  `| id | vício | regex | proibe | incidência no corpus | fonte |`. As linhas iniciais (a
  incidência é preenchida na 2.6):

| id | vício | regex | proibe |
|---|---|---|---|
| V1 | "não é só X, é Y" | `\bn[ãa]o [ée] (s[óo]|apenas)\b|\bnot just\b` | sim |
| V2 | "mais do que um…" | `\bmais (do )?que (um|uma|s[óo]|apenas)\b|\bmore than (just )?a\b` | sim |
| V3 | travessão de redação | `—` | sim |
| V4 | léxico de folheto | `\b(descubra|desvende|mergulhe|embarque|jornada|experi[êe]ncia [úu]nica|transforme|eleve|desperte|ess[êe]ncia|universo d[eo]|feito com amor|momento especial|apaixonad[oa]s? por)\b` | sim |
| V5 | adjetivo de vitrine | `\b(incr[íi]vel|surpreendente|fascinante|impressionante|sensacional|perfeit[oa])\b` | sim |
| V6 | abertura "Imagine" / "Prepare-se" | `^(imagine|prepare-se)\b|voc[êe] precisa (conhecer|provar)` | sim |
| V7 | "Você sabia que" | `\bvoc[êe] sabia\b|\bdid you know\b` | medir |
| V8 | "segredo / ninguém te conta" | `segredo|ningu[ée]m (te )?(conta|fala)|secret` | medir |
| V9 | emoji de brilho | `[✨🚀💫🌟]` | medir |

`proibe = sim` vira falha em M3. `medir` só entra na contagem do corpus: se os virais usam
a construção, ela não é vício, é padrão. A decisão de cada linha `medir` sai na 2.6, com o
número na mão.

- [ ] **2.2 Testes que falham**, acrescentados a `tests/test_ganchos.py`:

```python
def test_ler_vicios_real():
    v = g.ler_vicios()
    ids = {x["id"] for x in v}
    assert {"V1", "V3", "V4"} <= ids
    assert all(x["proibe"] in ("sim", "medir") for x in v)
    assert all(x["regex"].search("") is None or True for x in v)  # compila


def test_palavras_e_primeira_frase():
    assert g.palavras("Não compre café ruim pra sua casa") == ["Não", "compre", "café", "ruim", "pra", "sua", "casa"]
    assert g.primeira_frase("Coffee is 98.5% water. And that matters.") == "Coffee is 98.5% water."


def test_medir_corpus_sintetico():
    corpus = [
        {"id": "a", "idioma": "pt", "views": 100, "escrito": "Você sabia disso?", "dito": "", "etiqueta": []},
        {"id": "b", "idioma": "pt", "views": 10, "escrito": "3 cafés", "dito": "Olha isso. Depois", "etiqueta": []},
        {"id": "c", "idioma": "en", "views": 50, "escrito": "", "dito": "Coffee is 98.5% water.", "etiqueta": []},
        {"id": "d", "idioma": "pt", "views": 5, "escrito": "", "dito": "", "etiqueta": []},
    ]
    m = g.medir(corpus, g.ler_vicios())
    pt = m["pt"]
    assert pt["n"] == 3
    assert pt["pct_pergunta"] == pytest.approx(100 / 3, abs=0.1)
    assert pt["pct_numero"] == pytest.approx(100 / 3, abs=0.1)
    assert pt["vicios"]["V7"] == 1
    assert m["todos"]["n"] == 4
```

- [ ] **2.3 Rodar e confirmar a falha.**
- [ ] **2.4 Implementar** (acrescentar a `scripts/ganchos.py`):

```python
import statistics

# --- tabelas markdown (fonte única) -----------------------------------------

def _linhas_tabela(caminho: Path, prefixo: str) -> list[list[str]]:
    """Linhas de tabela cuja 1ª célula casa `prefixo` (regex); células sem a crase externa."""
    out = []
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if not linha.startswith("|"):
            continue
        celulas = [c.strip() for c in re.split(r"(?<!\\)\|", linha.strip())[1:-1]]
        if celulas and re.fullmatch(prefixo, celulas[0]):
            out.append([c.replace("\\|", "|") for c in celulas])
    return out


def _sem_crase(s: str) -> str:
    return s[1:-1] if len(s) >= 2 and s[0] == s[-1] == "`" else s


def ler_vicios(caminho: Path = VICIOS) -> list[dict]:
    out = []
    for c in _linhas_tabela(caminho, r"V\d+"):
        out.append({"id": c[0], "nome": c[1], "regex": re.compile(_sem_crase(c[2]), re.I),
                    "proibe": c[3].lower()})
    return out


# --- medidas do corpus ------------------------------------------------------

_PALAVRA = re.compile(r"[0-9A-Za-zÀ-ÿ]+(?:[-'’.,][0-9A-Za-zÀ-ÿ]+)*")


def palavras(s: str) -> list[str]:
    return _PALAVRA.findall(s)


def primeira_frase(s: str) -> str:
    m = re.match(r"(.+?[.?!…])(\s|$)", s.strip())
    return m.group(1) if m else s.strip()


def _abertura(x: dict) -> str:
    """O texto do gancho que se lê/ouve primeiro: 1ª tela citada + 1ª frase dita."""
    tela = x["escrito"].split(" / ")[0] if x["escrito"] else ""
    return f"{tela} {primeira_frase(x['dito']) if x['dito'] else ''}".strip()


_VOCE = re.compile(r"\b(voc[êe]|vc|seu|sua|teu|tua|you|your)\b", re.I)
_NEG = re.compile(r"^\W*(n[ãa]o|nunca|pare|no|never|don'?t|stop)\b", re.I)


def _pct(n: int, total: int) -> float:
    return round(100 * n / total, 1) if total else 0.0


def _quartis(vals: list[int]) -> dict:
    if not vals:
        return {"mediana": None, "p25": None, "p75": None}
    q = statistics.quantiles(vals, n=4) if len(vals) > 1 else [vals[0]] * 3
    return {"mediana": statistics.median(vals), "p25": q[0], "p75": q[2]}


def _bloco(itens: list[dict], vicios: list[dict]) -> dict:
    ab = [_abertura(x) for x in itens]
    telas = [len(palavras(x["escrito"].split(" / ")[0])) for x in itens if x["escrito"]]
    falas = [len(palavras(primeira_frase(x["dito"]))) for x in itens if x["dito"]]
    n = len(itens)
    return {
        "n": n,
        "com_tela": len(telas), "com_fala": len(falas),
        "palavras_tela": _quartis(telas), "palavras_fala_1a_frase": _quartis(falas),
        "pct_pergunta": _pct(sum("?" in a for a in ab), n),
        "pct_numero": _pct(sum(bool(re.search(r"\d", a)) for a in ab), n),
        "pct_voce": _pct(sum(bool(_VOCE.search(a)) for a in ab), n),
        "pct_negacao_inicial": _pct(sum(bool(_NEG.search(a)) for a in ab), n),
        "pct_sem_texto": _pct(sum(not a for a in ab), n),
        "vicios": {v["id"]: sum(bool(v["regex"].search(a)) for a in ab) for v in vicios},
    }


def medir(corpus: list[dict], vicios: list[dict]) -> dict:
    """Medidas por idioma e top 25% de views contra o resto (dentro dos virais)."""
    out = {"todos": _bloco(corpus, vicios)}
    for idi in ("pt", "en"):
        out[idi] = _bloco([x for x in corpus if x["idioma"] == idi], vicios)
    com_views = sorted((x for x in corpus if x.get("views")), key=lambda x: -x["views"])
    corte = len(com_views) // 4
    out["top25"] = _bloco(com_views[:corte], vicios)
    out["resto75"] = _bloco(com_views[corte:], vicios)
    return out
```

- [ ] **2.5 Rodar os testes.** Esperado: PASS.
- [ ] **2.6 Medir de verdade.** Gravar o corpus, imprimir as medidas e preencher a coluna
  `incidência no corpus` de `vicios-ia.md`, com contagem pt / en / total. Decisão por
  linha `medir`:
  - incidência em pt ≥ 3 ganchos: continua `medir` e vira **padrão**, não vício
  - incidência 0: vira `sim` só se houver outra fonte além do meu gosto; caso contrário
    fica `medir` com a nota "[leitura minha], sem lastro no corpus"

```bash
python -m uv run python scripts/ganchos.py extrair
python -m uv run python scripts/ganchos.py medir
```

  (`extrair` e `medir` entram no CLI da Tarefa 5; até lá, rode
  `python -c "import importlib.util,..."`, ou adiante o `main` com esses dois
  subcomandos.)

### Tarefa 3: padrões (julgamento, não medida)

**Arquivos:** criar `instagram/ganchos/padroes-mapa.json` e completar o script.

- [ ] **3.1 Ler os 129 ganchos** do `corpus.jsonl` (abertura + `ve` + views) e escrever
  `padroes-mapa.json`:

```json
{
  "padroes": {
    "<slug>": {"nome": "...", "forma": "molde em uma linha", "descricao": "o que faz o gancho funcionar"}
  },
  "mapa": {"<id do corpus>": "<slug>"}
}
```

  Regras:
  - cada gancho recebe **um** padrão, o dominante
  - de 6 a 10 padrões
  - padrão com n < 5 entra num padrão vizinho ou em `outro`
  - o padrão descreve a **mecânica** (contraste de dois objetos, imperativo negativo,
    pergunta de diagnóstico, número que contradiz, resultado antes do processo, ação já no
    meio, situação reconhecível, autoridade de quem faz), não o assunto
  - os 58 de motion entram, mas o relatório mostra pt-café à parte, porque o motion vende
    outra categoria

- [ ] **3.2 Teste que falha:**

```python
def test_padroes_agrupa_e_ordena():
    corpus = [
        {"id": "a", "idioma": "pt", "views": 100, "escrito": "A", "dito": "", "perfil": "@x", "frente": "brasil"},
        {"id": "b", "idioma": "pt", "views": 300, "escrito": "B", "dito": "", "perfil": "@y", "frente": "brasil"},
        {"id": "c", "idioma": "en", "views": 50, "escrito": "C", "dito": "", "perfil": "@z", "frente": "marcas"},
    ]
    mapa = {"padroes": {"p1": {"nome": "Um", "forma": "f", "descricao": "d"},
                        "p2": {"nome": "Dois", "forma": "f", "descricao": "d"}},
            "mapa": {"a": "p1", "b": "p1", "c": "p2"}}
    t = g.tabela_padroes(corpus, mapa)
    assert [p["slug"] for p in t] == ["p1", "p2"]           # ordena por n
    assert t[0]["n"] == 2 and t[0]["mediana_views"] == 200
    assert t[0]["exemplos"][0]["id"] == "b"                 # exemplo de maior view primeiro


def test_padroes_mapa_cobre_o_corpus_real():
    corpus = [json.loads(l) for l in (RAIZ / "instagram/ganchos/corpus.jsonl").read_text(encoding="utf-8").splitlines()]
    mapa = json.loads((RAIZ / "instagram/ganchos/padroes-mapa.json").read_text(encoding="utf-8"))
    faltam = [x["id"] for x in corpus if x["id"] not in mapa["mapa"]]
    assert not faltam
    assert set(mapa["mapa"].values()) <= set(mapa["padroes"])
    assert 6 <= len(mapa["padroes"]) <= 10
```

- [ ] **3.3 Implementar `tabela_padroes` e `escrever_padroes_md`:**

```python
def tabela_padroes(corpus: list[dict], mapa: dict) -> list[dict]:
    grupos: dict[str, list[dict]] = {}
    for x in corpus:
        slug = mapa["mapa"].get(x["id"])
        if slug:
            grupos.setdefault(slug, []).append(x)
    out = []
    for slug, itens in grupos.items():
        views = [x["views"] for x in itens if x.get("views")]
        out.append({
            "slug": slug, **mapa["padroes"][slug], "n": len(itens),
            "n_pt": sum(x["idioma"] == "pt" for x in itens),
            "mediana_views": statistics.median(views) if views else None,
            "exemplos": sorted(itens, key=lambda x: -(x.get("views") or 0))[:3],
        })
    return sorted(out, key=lambda p: (-p["n"], p["slug"]))


def _fmt_views(v) -> str:
    if not v:
        return "?"
    return f"{v / 1e6:.1f} mi".replace(".", ",") if v >= 1e6 else f"{v / 1e3:.0f} mil"


def escrever_padroes_md(corpus: list[dict], mapa: dict, medidas: dict, destino: Path) -> None:
    linhas = [
        "# Padrões de gancho — gerado por `scripts/ganchos.py padroes`; não edite à mão",
        "",
        "Corpus: as fichas de `instagram/referencias-virais/` (só Reel, **só vencedores**). "
        "Os números dizem o que os virais têm em comum, não o que separa viral de fracasso. "
        "O agrupamento (`padroes-mapa.json`) é julgamento **[leitura minha]**; as contagens "
        "sobre ele são **[medido]**.",
        "",
        "## Padrões",
        "",
        "| Padrão | Forma | n | n pt | Mediana de views | Exemplos (maior view primeiro) |",
        "|---|---|---:|---:|---:|---|",
    ]
    for p in tabela_padroes(corpus, mapa):
        ex = "<br>".join(f"{x['perfil']} {_fmt_views(x.get('views'))}: “{_abertura(x) or x['ve'][:80]}”"
                         for x in p["exemplos"])
        linhas.append(f"| **{p['nome']}** (`{p['slug']}`) | {p['forma']} | {p['n']} | {p['n_pt']} | "
                      f"{_fmt_views(p['mediana_views'])} | {ex} |")
    linhas += ["", "## Medidas do corpus **[medido]**", "",
               "| Recorte | n | tela (pal., mediana · p25–p75) | fala 1ª frase (idem) | pergunta | número | você | negação no início | sem texto |",
               "|---|---:|---|---|---:|---:|---:|---:|---:|"]
    for nome, b in medidas.items():
        t, f = b["palavras_tela"], b["palavras_fala_1a_frase"]
        linhas.append(f"| {nome} | {b['n']} | {t['mediana']} · {t['p25']}–{t['p75']} | "
                      f"{f['mediana']} · {f['p25']}–{f['p75']} | {b['pct_pergunta']}% | {b['pct_numero']}% | "
                      f"{b['pct_voce']}% | {b['pct_negacao_inicial']}% | {b['pct_sem_texto']}% |")
    linhas += ["", "## Vícios de IA no corpus (contagem de ganchos)", "",
               "| id | " + " | ".join(medidas) + " |", "|---|" + "---:|" * len(medidas)]
    for vid in medidas["todos"]["vicios"]:
        linhas.append(f"| {vid} | " + " | ".join(str(b["vicios"][vid]) for b in medidas.values()) + " |")
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")
```

- [ ] **3.4 Rodar os testes. Gerar `padroes.md` e lê-lo.** Se algum padrão tiver mediana
  de views muito acima dos outros, anotar como candidato a peso em J6, mas com a ressalva:
  amostra só de vencedores.

### Tarefa 4: rubrica

**Arquivos:** criar `.claude/skills/canastra-ganchos/rubrica.md` e completar o script.

- [ ] **4.1 Escrever `rubrica.md`.** A tabela tem as colunas
  `| id | regra | tipo | quem | formato | peso | como verificar | fonte |`, com:
  - `tipo` ∈ `portao`, `pontuada`
  - `quem` ∈ `script`, `claude`
  - `formato` ∈ `todos`, `capa`, `reel`
  - `peso` `0` nos portões

  As 18 regras com os pesos iniciais (os números de fonte saem do `padroes.md`):

| id | regra | tipo | quem | formato | peso |
|---|---|---|---|---|---:|
| P1 | número ou alegação tem fonte (`--fonte`) | portao | script | todos | 0 |
| P2 | sem pseudociência (dopamina, cérebro, "60 mil vezes") | portao | script | todos | 0 |
| P3 | sem escassez ou superlativo sem prova | portao | script | todos | 0 |
| P4 | a promessa é paga num slide/segundo apontável | portao | claude | todos | 0 |
| M1 | tamanho na faixa do formato | pontuada | script | todos | 8 |
| M2 | a 2ª camada não repete a 1ª | pontuada | script | todos | 6 |
| M3 | sem vício de IA (`vicios-ia.md`, `proibe = sim`) | pontuada | script | todos | 12 |
| M4 | sem abertura proibida (saudação, "fica até o final", "você não vai acreditar") | pontuada | script | todos | 4 |
| M5 | fala com a pessoa (você/seu/sua) | pontuada | script | todos | 6 |
| J1 | lacuna específica: dá para escrever a pergunta | pontuada | claude | todos | 14 |
| J2 | promessa, não assunto | pontuada | claude | todos | 10 |
| J3 | tem contraste | pontuada | claude | todos | 9 |
| J4 | coisa real e concreta (objeto, lugar, número, gesto), não abstração | pontuada | claude | todos | 10 |
| J5 | tom de procedência: risco real, sem drama fabricado nem humor de fora | pontuada | claude | todos | 5 |
| J6 | usa padrão do corpus com n ≥ 5 | pontuada | claude | todos | 6 |
| C1 | foto e manchete se completam; a foto sozinha diz do que se trata | pontuada | claude | capa | 6 |
| C2 | a capa pede o arraste (pergunta ou afirmação cuja prova está nos slides) | pontuada | claude | capa | 4 |
| R1 | frame a 0,5 s faz sentido sozinho | pontuada | claude | reel | 10 |

  Soma: capa = 90 + 10 = 100, reel = 90 + 10 = 100. Cada linha tem `como verificar` (o
  teste em uma frase) e `fonte` com marca, por exemplo `02-ganchos.md` Teste 2
  **[criador]**; `padroes.md`: 0 de 51 ganchos pt usam V1 **[medido]**; ou diretriz do
  cliente de 07/10/2026 em `canastra-carrossel` **[medido]**. Abaixo da tabela, uma seção
  por regra com 1 exemplo que passa e 1 que falha, tirados do corpus ou do banco G1–G15.

- [ ] **4.2 Testes que falham:**

```python
def test_rubrica_real_valida():
    regras = g.ler_rubrica()
    assert 15 <= len(regras) <= 20
    assert g.validar_rubrica(regras) == []


def test_validar_rubrica_pega_soma_errada_e_mecanica_sem_funcao():
    R = g.Regra
    regras = [R("M1", "x", "pontuada", "script", "todos", 60, "", ""),
              R("Z9", "y", "pontuada", "script", "capa", 30, "", "")]
    erros = g.validar_rubrica(regras)
    assert any("soma" in e and "capa" in e for e in erros)
    assert any("Z9" in e for e in erros)
```

- [ ] **4.3 Implementar:**

```python
from dataclasses import dataclass

TIPOS = ("portao", "pontuada")
QUEM = ("script", "claude")
FORMATOS = ("capa", "reel")


@dataclass(frozen=True)
class Regra:
    id: str
    nome: str
    tipo: str
    quem: str
    formato: str
    peso: int
    verificacao: str
    fonte: str


def ler_rubrica(caminho: Path = RUBRICA) -> list[Regra]:
    out = []
    for c in _linhas_tabela(caminho, r"[PMJCR]\d+"):
        out.append(Regra(c[0], c[1], c[2], c[3], c[4], int(c[5] or 0), c[6], c[7]))
    return out


def regras_do_formato(regras: list[Regra], formato: str) -> list[Regra]:
    return [r for r in regras if r.formato in ("todos", formato)]


def validar_rubrica(regras: list[Regra]) -> list[str]:
    erros = []
    ids = [r.id for r in regras]
    if len(ids) != len(set(ids)):
        erros.append("id repetido na rubrica")
    for r in regras:
        if r.tipo not in TIPOS or r.quem not in QUEM or r.formato not in ("todos", *FORMATOS):
            erros.append(f"{r.id}: tipo/quem/formato fora do vocabulário")
        if r.tipo == "portao" and r.peso:
            erros.append(f"{r.id}: portão não tem peso")
        if r.quem == "script" and r.id not in MECANICAS:
            erros.append(f"{r.id}: quem=script mas não há função em MECANICAS")
    for f in FORMATOS:
        soma = sum(r.peso for r in regras_do_formato(regras, f) if r.tipo == "pontuada")
        if soma != 100:
            erros.append(f"soma dos pesos de {f} = {soma}, devia ser 100")
    return erros
```

  (`MECANICAS` é definido na Tarefa 5; para os testes da 4.2 passarem antes dela, defina
  já `MECANICAS: dict = {}` e preencha depois.)

### Tarefa 5: regras mecânicas, `avaliar`, CLI e registro

- [ ] **5.1 Testes que falham:**

```python
G = g.Gancho


def test_p1_numero_sem_fonte():
    ok, _ = g.MECANICAS["P1"](G("capa", manchete="O microlote custa 4 reais a mais"))
    assert not ok
    ok, _ = g.MECANICAS["P1"](G("capa", manchete="O microlote custa quatro reais a mais"))
    assert not ok                                   # número por extenso também
    ok, _ = g.MECANICAS["P1"](G("capa", manchete="O microlote custa 4 reais a mais",
                                fonte="tabela de 11/09/2026"))
    assert ok


def test_p2_e_p3():
    assert not g.MECANICAS["P2"](G("reel", fala="O cheiro da torra age no seu cérebro"))[0]
    assert not g.MECANICAS["P3"](G("capa", manchete="O café mais premiado de Minas"))[0]
    assert g.MECANICAS["P3"](G("capa", manchete="Tem casca no seu café?"))[0]


def test_m1_faixa():
    a, b = g.FAIXAS["capa"]
    assert g.MECANICAS["M1"](G("capa", manchete=" ".join(["pal"] * a)))[0]
    assert not g.MECANICAS["M1"](G("capa", manchete=" ".join(["pal"] * (b + 3))))[0]


def test_m2_repeticao():
    assert not g.MECANICAS["M2"](G("reel", fala="Café na geladeira não conserva.",
                                   tela="Café na geladeira não conserva"))[0]
    assert g.MECANICAS["M2"](G("reel", fala="Café na geladeira não conserva.",
                               tela="Onde guardar o pacote aberto"))[0]
    assert g.MECANICAS["M2"](G("capa", manchete="Tem casca no seu café?"))[0]   # sem 2ª camada


def test_m3_m4_m5():
    assert not g.MECANICAS["M3"](G("capa", manchete="Não é só café, é uma experiência"))[0]
    assert not g.MECANICAS["M3"](G("capa", manchete="Descubra a jornada do grão"))[0]
    assert g.MECANICAS["M3"](G("capa", manchete="Tem casca no seu café?"))[0]
    assert not g.MECANICAS["M4"](G("reel", fala="Bom dia! Hoje eu vou falar da colheita"))[0]
    assert g.MECANICAS["M5"](G("capa", manchete="Tem casca no seu café?"))[0]
    assert not g.MECANICAS["M5"](G("capa", manchete="A colheita de 2026"))[0]


def test_avaliar_portao_pendente_e_completo():
    regras = g.ler_rubrica()
    r = g.avaliar(G("capa", manchete="O café mais premiado de Minas"), regras, {})
    assert r["nota"] == 0 and "P3" in r["portoes_falhos"]
    r = g.avaliar(G("capa", manchete="Tem casca no seu café?"), regras, {})
    assert r["nota"] is None and "J1" in r["pendentes"]
    todos = {x.id: True for x in g.regras_do_formato(regras, "capa") if x.quem == "claude"}
    r = g.avaliar(G("capa", manchete="Tem casca no seu café?", apoio="A gente explica o que é"), regras, todos)
    assert r["nota"] == r["subtotal"] and 0 < r["nota"] <= 100


def test_registrar_anexa(tmp_path):
    destino = tmp_path / "avaliacoes.jsonl"
    r = g.avaliar(G("capa", manchete="Tem casca no seu café?"), g.ler_rubrica(), {})
    g.registrar(r, tema="casca", destino=destino, escolhido=True, post="DefH_1ClN30")
    g.registrar(r, tema="casca", destino=destino)
    linhas = [json.loads(l) for l in destino.read_text(encoding="utf-8").splitlines()]
    assert len(linhas) == 2 and linhas[0]["escolhido"] is True and linhas[0]["post"] == "DefH_1ClN30"
    assert linhas[0]["gancho"]["manchete"] == "Tem casca no seu café?"
```

- [ ] **5.2 Rodar e confirmar a falha.**
- [ ] **5.3 Implementar.** Os limites de `FAIXAS` saem das medidas da 2.6:
  - capa = faixa p25–p75 de palavras da tela no corpus pt, arredondada
  - reel = 5–8 na 1ª frase falada [criador], com a tela em 4–7 [medido banco]

  Registre os números escolhidos no comentário.

```python
from dataclasses import asdict, field
from datetime import date

#: Faixa de palavras da camada principal (manchete da capa / 1ª frase da fala do Reel).
#: capa: p25–p75 da 1ª tela no corpus pt (padroes.md) · reel: 5–8, 02-ganchos.md [criador]
FAIXAS = {"capa": (4, 10), "reel": (5, 8)}
#: 2ª camada: tela do Reel 4–7 (02-ganchos.md, contado nos 17 do banco); apoio da capa até 14.
FAIXAS_2 = {"capa": (0, 14), "reel": (4, 7)}

NUMERO_EXTENSO = re.compile(r"\b(dois|duas|tr[êe]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|"
                            r"vinte|trinta|quarenta|cinquenta|cem|cento|mil|milh[ãa]o|metade|dobro|triplo)\b", re.I)
FOLCLORE = re.compile(r"dopamina|c[ée]rebro|neuro|cortisol|serotonina|60[ .]?000|60 mil vezes", re.I)
ESCASSEZ = re.compile(r"[úu]ltimas unidades|s[óo] hoje|imperd[íi]vel|corre que|mais premiad|"
                      r"o melhor (caf[ée] )?d[oa] (brasil|mundo|minas)|[úu]nic[oa] no mundo|nunca vist", re.I)
ABERTURA = re.compile(r"^\W*(bom dia|boa tarde|boa noite|oi\b|ol[áa]|hoje (eu )?vou|neste (post|v[íi]deo)|"
                      r"nesse (post|v[íi]deo)|fica at[ée] o final|voc[êe] n[ãa]o vai acreditar)", re.I)


@dataclass
class Gancho:
    formato: str              # capa | reel
    manchete: str = ""
    apoio: str = ""
    fala: str = ""
    tela: str = ""
    fonte: str = ""

    @property
    def principal(self) -> str:
        return self.manchete if self.formato == "capa" else self.fala

    @property
    def secundario(self) -> str:
        return self.apoio if self.formato == "capa" else self.tela

    def textos(self) -> str:
        return " ".join(t for t in (self.manchete, self.apoio, self.fala, self.tela) if t)


def _p1(gc: Gancho):
    t = gc.textos()
    achou = re.findall(r"\d[\d.,]*", t) + NUMERO_EXTENSO.findall(t)
    if achou and not gc.fonte.strip():
        return False, f"número sem --fonte: {', '.join(map(str, achou))}"
    return True, f"fonte: {gc.fonte}" if achou else "sem número"


def _p2(gc: Gancho):
    m = FOLCLORE.search(gc.textos())
    return (False, f"pseudociência: “{m.group(0)}” (07-nao-fazer §1)") if m else (True, "")


def _p3(gc: Gancho):
    m = ESCASSEZ.search(gc.textos())
    if m and not gc.fonte.strip():
        return False, f"escassez/superlativo sem prova: “{m.group(0)}”"
    return True, ""


def _m1(gc: Gancho):
    a, b = FAIXAS[gc.formato]
    alvo = gc.principal if gc.formato == "capa" else primeira_frase(gc.principal)
    n = len(palavras(alvo))
    det = f"{n} palavras (faixa {a}–{b})"
    if gc.secundario:
        a2, b2 = FAIXAS_2[gc.formato]
        n2 = len(palavras(gc.secundario))
        det += f"; 2ª camada {n2} (faixa {a2}–{b2})"
        return a <= n <= b and a2 <= n2 <= b2, det
    return a <= n <= b, det


def _conteudo(s: str) -> set[str]:
    return {sem_acento(p).lower() for p in palavras(s) if len(p) > 3}


def _m2(gc: Gancho):
    if not gc.secundario:
        return True, "sem 2ª camada"
    a, b = _conteudo(gc.principal), _conteudo(gc.secundario)
    jac = len(a & b) / len(a | b) if a | b else 0
    return jac <= 0.5, f"sobreposição {jac:.0%}"


def _m3(gc: Gancho):
    achados = [v["id"] for v in ler_vicios() if v["proibe"] == "sim" and v["regex"].search(gc.textos())]
    return (False, "vício de IA: " + ", ".join(achados)) if achados else (True, "")


def _m4(gc: Gancho):
    m = ABERTURA.search(gc.principal)
    return (False, f"abertura proibida: “{m.group(0).strip()}”") if m else (True, "")


def _m5(gc: Gancho):
    return (True, "") if _VOCE.search(gc.textos()) else (False, "não fala com a pessoa")


MECANICAS = {"P1": _p1, "P2": _p2, "P3": _p3, "M1": _m1, "M2": _m2, "M3": _m3, "M4": _m4, "M5": _m5}


def avaliar(gc: Gancho, regras: list[Regra], julgamento: dict[str, bool]) -> dict:
    res = {}
    for r in regras_do_formato(regras, gc.formato):
        if r.quem == "script":
            ok, det = MECANICAS[r.id](gc)
        else:
            ok, det = julgamento.get(r.id), ""
        res[r.id] = {"ok": ok, "detalhe": det, "peso": r.peso, "tipo": r.tipo, "quem": r.quem, "nome": r.nome}
    falhos = [i for i, v in res.items() if v["tipo"] == "portao" and v["ok"] is False]
    pendentes = [i for i, v in res.items() if v["ok"] is None]
    subtotal = sum(v["peso"] for v in res.values() if v["tipo"] == "pontuada" and v["ok"])
    nota = 0 if falhos else (subtotal if not pendentes else None)
    return {"gancho": asdict(gc), "resultados": res, "portoes_falhos": falhos,
            "pendentes": pendentes, "subtotal": subtotal, "nota": nota}


def registrar(r: dict, tema: str, destino: Path = SAIDA / "avaliacoes.jsonl",
              escolhido: bool = False, post: str | None = None) -> None:
    linha = {"data": date.today().isoformat(), "tema": tema, "gancho": r["gancho"], "nota": r["nota"],
             "subtotal": r["subtotal"], "resultados": {i: v["ok"] for i, v in r["resultados"].items()},
             "portoes_falhos": r["portoes_falhos"], "pendentes": r["pendentes"],
             "escolhido": escolhido, "post": post}
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("a", encoding="utf-8") as f:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")
```

  E o CLI, no fim do arquivo:

```python
import argparse
import io
import sys


def _imprime(r: dict) -> None:
    for i, v in r["resultados"].items():
        marca = {True: "ok ", False: "XX ", None: "?? "}[v["ok"]]
        peso = "portão" if v["tipo"] == "portao" else f"{v['peso']:>2}"
        print(f"{marca}{i:<3} [{peso}] {v['nome']}" + (f" — {v['detalhe']}" if v["detalhe"] else ""))
    if r["portoes_falhos"]:
        print(f"\nREPROVADO nos portões {', '.join(r['portoes_falhos'])}: nota 0")
    elif r["pendentes"]:
        print(f"\nsubtotal {r['subtotal']} · faltam julgar: {', '.join(r['pendentes'])} "
              f"(--julgamento {','.join(p + '=1' for p in r['pendentes'])})")
    else:
        print(f"\nNOTA {r['nota']}/100")


def _julgamento(s: str) -> dict[str, bool]:
    out = {}
    for par in filter(None, (s or "").split(",")):
        k, v = par.split("=")
        out[k.strip().upper()] = v.strip() in ("1", "s", "sim", "true")
    return out


def main(argv: list[str] | None = None) -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(prog="ganchos")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("extrair")
    sub.add_parser("medir")
    sub.add_parser("padroes")
    c = sub.add_parser("checar")
    c.add_argument("--formato", choices=FORMATOS, required=True)
    for campo in ("manchete", "apoio", "fala", "tela", "fonte", "julgamento", "tema", "post"):
        c.add_argument(f"--{campo}", default="")
    c.add_argument("--json", action="store_true")
    c.add_argument("--registrar", action="store_true")
    c.add_argument("--escolhido", action="store_true")
    rc = sub.add_parser("recalibrar")
    rc.add_argument("--proprios", default=str(PROPRIOS))
    a = ap.parse_args(argv)

    if a.cmd == "extrair":
        corpus = extrair()
        SAIDA.mkdir(parents=True, exist_ok=True)
        (SAIDA / "corpus.jsonl").write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in corpus), encoding="utf-8")
        print(f"{len(corpus)} ganchos -> {SAIDA / 'corpus.jsonl'}")
        return 0
    corpus_arq = SAIDA / "corpus.jsonl"
    if a.cmd in ("medir", "padroes"):
        corpus = [json.loads(l) for l in corpus_arq.read_text(encoding="utf-8").splitlines()]
        med = medir(corpus, ler_vicios())
        if a.cmd == "medir":
            print(json.dumps(med, ensure_ascii=False, indent=1))
            return 0
        mapa = json.loads((SAIDA / "padroes-mapa.json").read_text(encoding="utf-8"))
        escrever_padroes_md(corpus, mapa, med, SAIDA / "padroes.md")
        print(f"-> {SAIDA / 'padroes.md'}")
        return 0
    if a.cmd == "checar":
        regras = ler_rubrica()
        erros = validar_rubrica(regras)
        if erros:
            print("rubrica inválida:\n" + "\n".join(erros))
            return 2
        gc = Gancho(a.formato, a.manchete, a.apoio, a.fala, a.tela, a.fonte)
        if not gc.principal:
            print("falta --manchete (capa) ou --fala (reel)")
            return 2
        r = avaliar(gc, regras, _julgamento(a.julgamento))
        print(json.dumps(r, ensure_ascii=False, indent=1)) if a.json else _imprime(r)
        if a.registrar:
            registrar(r, tema=a.tema, escolhido=a.escolhido, post=a.post or None)
        return 0
    if a.cmd == "recalibrar":
        return recalibrar_cli(Path(a.proprios))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **5.4 Rodar todos os testes de `tests/test_ganchos.py`.** Esperado: PASS. Depois,
  conferir à mão os casos-limite:

```bash
python -m uv run python scripts/ganchos.py checar --formato capa --manchete "Tem casca no seu café?"
python -m uv run python scripts/ganchos.py checar --formato reel --fala "O microlote custa quatro reais a mais." --tela "Quatro reais de diferença" --fonte "tabela 11/09/2026"
```

### Tarefa 6: recalibração

- [ ] **6.1 Testes que falham:**

```python
def _post(i, gancho, alcance, saves, shares, coletado="2026-11-01T10:00:00"):
    return {"id": f"p{i}", "gancho": gancho, "alcance": alcance, "saves": saves, "shares": shares,
            "curtidas": 10, "coletado_em": coletado, "tipo": "carrossel"}


def _aval(manchete, j3):
    return {"gancho": {"formato": "capa", "manchete": manchete, "apoio": "", "fala": "", "tela": "", "fonte": ""},
            "resultados": {"J3": j3, "M1": True}, "escolhido": True}


def test_ultima_linha_por_id():
    linhas = [_post(1, "A", 100, 1, 1, "2026-11-01T10:00:00"), _post(1, "A", 200, 5, 5, "2026-11-03T10:00:00")]
    assert g.ultimas_por_id(linhas)[0]["alcance"] == 200


def test_metrica_prefere_envios_e_salvos():
    assert g.metrica(_post(1, "A", 200, 6, 4), "capa") == pytest.approx(0.05)
    assert g.metrica({"alcance": 100, "curtidas": 7}, "capa") == pytest.approx(0.07)
    assert g.metrica({"alcance": None, "curtidas": 7}, "capa") is None


def test_recalibrar_amostra_insuficiente_e_proposta():
    regras = [g.Regra("J3", "contraste", "pontuada", "claude", "todos", 10, "", ""),
              g.Regra("M1", "tamanho", "pontuada", "script", "todos", 8, "", "")]
    posts = [_post(i, f"Gancho {i}", 100, 1, 1) for i in range(5)]
    avals = [_aval(f"Gancho {i}", True) for i in range(5)]
    assert g.propor(regras, g.cruzar(posts, avals), "capa")["status"] == "amostra-insuficiente"
    # 8 posts: os 4 com contraste rendem o dobro
    posts = [_post(i, f"Gancho {i}", 100, 4 if i < 4 else 2, 0) for i in range(8)]
    avals = [_aval(f"gancho {i}!", i < 4) for i in range(8)]     # casa por texto normalizado
    p = g.propor(regras, g.cruzar(posts, avals), "capa")
    assert p["status"] == "ok" and p["n"] == 8
    j3 = next(x for x in p["regras"] if x["id"] == "J3")
    assert j3["fator"] == 1.5 and j3["peso_proposto"] == 15        # razão 2.0 limitada a 1.5
    m1 = next(x for x in p["regras"] if x["id"] == "M1")
    assert m1["peso_proposto"] == 8 and m1["nota"] == "sem contraste (todos passaram)"
```

- [ ] **6.2 Rodar e confirmar a falha.**
- [ ] **6.3 Implementar:**

```python
N_MIN = 8
LIMITE = (0.5, 1.5)


def normalizar(s: str) -> str:
    s = re.sub(r"[^a-z0-9 ]", " ", sem_acento(s or "").lower())
    return re.sub(r"\s+", " ", s).strip()


def carregar_jsonl(caminho: Path) -> list[dict]:
    if not caminho.exists():
        return []
    return [json.loads(l) for l in caminho.read_text(encoding="utf-8").splitlines() if l.strip()]


def ultimas_por_id(linhas: list[dict]) -> list[dict]:
    ult: dict[str, dict] = {}
    for x in linhas:
        if x.get("id") and (x["id"] not in ult or (x.get("coletado_em") or "") >= (ult[x["id"]].get("coletado_em") or "")):
            ult[x["id"]] = x
    return list(ult.values())


def metrica(post: dict, formato: str) -> float | None:
    """(saves+shares)/alcance [oficial: envios é sinal principal]; senão curtidas/alcance;
    Reel com tempo médio assistido usa ele."""
    if formato == "reel" and post.get("tempo_medio_assistido_s") is not None:
        return float(post["tempo_medio_assistido_s"])
    alc = post.get("alcance")
    if not alc:
        return None
    if post.get("saves") is not None and post.get("shares") is not None:
        return (post["saves"] + post["shares"]) / alc
    if post.get("curtidas") is not None:
        return post["curtidas"] / alc
    return None


def cruzar(posts: list[dict], avaliacoes: list[dict]) -> list[dict]:
    """Casa `gancho` do post com a avaliação de mesmo texto principal (a última, preferindo escolhida)."""
    idx: dict[str, dict] = {}
    for a in avaliacoes:
        gc = a["gancho"]
        chave = normalizar(gc.get("manchete") or gc.get("fala"))
        if chave and (chave not in idx or a.get("escolhido") or not idx[chave].get("escolhido")):
            idx[chave] = a
    out = []
    for p in ultimas_por_id(posts):
        a = idx.get(normalizar(p.get("gancho") or ""))
        if a:
            out.append({"post": p, "avaliacao": a, "formato": a["gancho"]["formato"]})
    return out


def propor(regras: list[Regra], cruzados: list[dict], formato: str, n_min: int = N_MIN) -> dict:
    itens = [(c, metrica(c["post"], formato)) for c in cruzados if c["formato"] == formato]
    itens = [(c, v) for c, v in itens if v is not None]
    if len(itens) < n_min:
        return {"status": "amostra-insuficiente", "n": len(itens), "n_min": n_min, "formato": formato}
    out = []
    for r in regras_do_formato(regras, formato):
        if r.tipo != "pontuada":
            continue
        passou = [v for c, v in itens if c["avaliacao"]["resultados"].get(r.id) is True]
        falhou = [v for c, v in itens if c["avaliacao"]["resultados"].get(r.id) is False]
        linha = {"id": r.id, "nome": r.nome, "peso": r.peso, "n_passou": len(passou), "n_falhou": len(falhou),
                 "mediana_passou": statistics.median(passou) if passou else None,
                 "mediana_falhou": statistics.median(falhou) if falhou else None,
                 "fator": 1.0, "peso_proposto": r.peso, "nota": ""}
        if not passou or not falhou:
            linha["nota"] = "sem contraste (todos passaram)" if passou else "sem contraste (todos falharam)" if falhou else "sem dado"
        else:
            mp, mf = linha["mediana_passou"], linha["mediana_falhou"]
            razao = mp / mf if mf > 0 else (LIMITE[1] if mp > 0 else 1.0)
            linha["fator"] = round(min(max(razao, LIMITE[0]), LIMITE[1]), 2)
            linha["peso_proposto"] = round(r.peso * linha["fator"])
        out.append(linha)
    return {"status": "ok", "n": len(itens), "formato": formato, "regras": out,
            "soma_proposta": sum(x["peso_proposto"] for x in out)}


def escrever_recalibracao(props: list[dict], destino: Path) -> None:
    linhas = [f"# Recalibração da rubrica — {date.today().isoformat()}", "",
              "Gerado por `scripts/ganchos.py recalibrar`. **Proposta**: a rubrica só muda com aprovação do "
              "Rafael. Pesos limitados a ±50%; a soma precisa ser renormalizada a 100 ao aplicar.", ""]
    for p in props:
        linhas.append(f"## {p['formato']} — n = {p['n']}")
        if p["status"] != "ok":
            linhas += ["", f"Amostra insuficiente ({p['n']} de {p['n_min']}). Nada proposto.", ""]
            continue
        linhas += ["", "| regra | peso | proposto | fator | passou (n · mediana) | falhou (n · mediana) | nota |",
                   "|---|---:|---:|---:|---|---|---|"]
        for x in p["regras"]:
            linhas.append(f"| {x['id']} {x['nome']} | {x['peso']} | {x['peso_proposto']} | {x['fator']} | "
                          f"{x['n_passou']} · {x['mediana_passou']} | {x['n_falhou']} · {x['mediana_falhou']} | {x['nota']} |")
        linhas += ["", f"Soma proposta: {p['soma_proposta']} (renormalizar a 100).", ""]
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def recalibrar_cli(proprios: Path) -> int:
    posts = carregar_jsonl(proprios)
    if not posts:
        print(f"aviso: {proprios} não existe ou está vazio; nada a recalibrar (o fluxo 1 ainda não gravou métricas)")
        return 0
    cruzados = cruzar(posts, carregar_jsonl(SAIDA / "avaliacoes.jsonl"))
    regras = ler_rubrica()
    props = [propor(regras, cruzados, f) for f in FORMATOS]
    destino = SAIDA / f"recalibracao-{date.today().isoformat()}.md"
    escrever_recalibracao(props, destino)
    for p in props:
        print(f"{p['formato']}: {p['status']} (n = {p['n']})")
    print(f"-> {destino}")
    return 0
```

- [ ] **6.4 Rodar todos os testes.** `recalibrar` sem arquivo imprime o aviso e sai com 0.

### Tarefa 7: SKILL.md, LEIA-ME e sementes

- [ ] **7.1 `SKILL.md`**, com frontmatter `name: canastra-ganchos` e uma `description`
  que dispara em "gancho", "capa de carrossel", "primeira frase do Reel", "dar nota",
  "título do post" e "aprovar pauta". Seções:
  - rotear (o que fica com `canastra-carrossel`/`canastra-video`)
  - os dois modos, com os passos e o comando `checar`
  - formato da resposta (tabela regra a regra + a pergunta que o gancho abre + matéria-prima
    existe/falta)
  - "não soar como IA" (aponta para `vicios-ia.md` + 3 instruções de escrita tiradas das
    medidas)
  - recalibração
  - limites
- [ ] **7.2 `instagram/ganchos/LEIA-ME.md`:** tabela de arquivos (gerado / à mão) e os
  comandos.
- [ ] **7.3 Sementes de avaliação:** registrar os dois carrosséis já feitos com
  `--escolhido`. `casca-no-cafe` leva `--post DefH_1ClN30`. Os julgamentos ficam
  explícitos na linha de comando.

### Tarefa 8: uso imediato e entrega

- [ ] **8.1** Rodar o modo **gerar** para as 4 pautas da fila de `instagram/agenda.md`
  (preço contra café de mercado, SCA 80+, cereja verde, e a quarta escolhida pela
  matéria-prima existente; altitude está bloqueada e "moído ou grãos" não tem fonte). Para
  cada uma: cerca de 10 candidatos, `checar` em todos, julgamento, 3 finalistas com nota.
  Registrar com `--registrar --tema`.
- [ ] **8.2** Escrever `instagram/ganchos/ciclo1-capas-20a30-10.md` com o resultado para o
  Rafael.
- [ ] **8.3** Avaliar 1 gancho do próprio Rafael (o "Tem casca no seu café?" já publicado)
  como demonstração do modo **avaliar**.
- [ ] **8.4** Nota em `side-session-notes/…/fluxo5-ganchos.md`:
  - mudança proposta para o `promptPauta` (texto pronto para colar)
  - propostas para `instagram/estrategia/02-ganchos.md`
  - o que a recalibração espera do `proprios.jsonl`
- [ ] **8.5** Verificação final: `python -m uv run pytest -q` (suíte inteira) e `git status`
  para conferir que nada fora do escopo foi tocado.
