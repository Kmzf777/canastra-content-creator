"""Máquina de ganchos: corpus, padrões, checagem pela rubrica e recalibração.

    python scripts/ganchos.py extrair
    python scripts/ganchos.py medir
    python scripts/ganchos.py padroes
    python scripts/ganchos.py checar --formato capa --manchete "..." [--apoio "..."]
           [--fonte "..."] [--julgamento J1=1,J2=0] [--json] [--registrar --tema T]
    python scripts/ganchos.py recalibrar [--proprios CAMINHO]

A rubrica e o léxico de vícios são fonte única: este script lê as tabelas de
.claude/skills/canastra-ganchos/{rubrica,vicios-ia}.md, nunca guarda cópia de peso.

Skill: .claude/skills/canastra-ganchos/ · Spec: docs/superpowers/specs/2026-10-15-maquina-ganchos-design.md
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date
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
    """O texto literal de uma camada: só o que está entre aspas.

    Conteúdo sem aspas nas fichas é DESCRIÇÃO ("só o rótulo da garrafa", "trilha
    orquestral, sem voz"), não texto lido ou ouvido. Contá-lo como gancho inflava a
    contagem de palavras, então ele vira vazio. Conferido nas 26 ocorrências em 15/10/2026.
    """
    s = conteudo.replace("**", "").strip()
    if not s or _NADA.match(s):
        return ""
    trechos = [a or b for a, b in re.findall(r'"([^"]+)"|“([^”]+)”', s)]
    if not trechos:
        trechos = re.findall(r"(?<!\w)'(.+?)'(?!\w)", s)   # aceita apóstrofo dentro: didn't
    return " / ".join(t.strip() for t in trechos)


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


# --- tabelas markdown (fonte única) -----------------------------------------

def _linhas_tabela(caminho: Path, prefixo: str) -> list[list[str]]:
    """Linhas de tabela cuja 1ª célula casa `prefixo`; `|` dentro de crase não divide célula."""
    out = []
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if not linha.startswith("|"):
            continue
        celulas, atual, em_crase = [], "", False
        for ch in linha.strip()[1:]:
            if ch == "`":
                em_crase = not em_crase
            if ch == "|" and not em_crase:
                celulas.append(atual.strip())
                atual = ""
            else:
                atual += ch
        if celulas and re.fullmatch(prefixo, celulas[0]):
            out.append(celulas)
    return out


def _sem_crase(s: str) -> str:
    return s[1:-1] if len(s) >= 2 and s[0] == s[-1] == "`" else s


def ler_vicios(caminho: Path = VICIOS) -> list[dict]:
    out = []
    for c in _linhas_tabela(caminho, r"V\d+"):
        out.append({"id": c[0], "nome": c[1], "regex": re.compile(_sem_crase(c[2]), re.I),
                    "proibe": c[3].lower(), "onde": c[4].lower()})
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


_VOCE = re.compile(r"\b(voc[êe]|vc|seu|sua|seus|suas|teu|tua|you|your)\b", re.I)
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
    telas_txt = [x["escrito"].split(" / ")[0] for x in itens]
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
        "vicios": {v["id"]: sum(bool(v["regex"].search(t)) for t in (telas_txt if v.get("onde") == "tela" else ab))
                   for v in vicios},
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


# --- padrões (o mapa é julgamento; as contagens sobre ele são medida) --------

#: Frentes de café; as de motion vendem outras categorias e entram só no total.
FRENTES_CAFE = {"processo", "brasil", "marcas", "influenciadores"}


def tabela_padroes(corpus: list[dict], mapa: dict) -> list[dict]:
    grupos: dict[str, list[dict]] = {}
    for x in corpus:
        slug = mapa["mapa"].get(x["id"])
        if slug:
            grupos.setdefault(slug, []).append(x)
    out = []
    for slug, itens in grupos.items():
        views = [x["views"] for x in itens if x.get("views")]
        cafe = [x for x in itens if x["frente"] in FRENTES_CAFE]
        views_cafe = [x["views"] for x in cafe if x.get("views")]
        out.append({
            "slug": slug, **mapa["padroes"][slug], "n": len(itens),
            "n_pt": sum(x["idioma"] == "pt" for x in itens),
            "n_cafe": len(cafe),
            "mediana_views": statistics.median(views) if views else None,
            "mediana_views_cafe": statistics.median(views_cafe) if views_cafe else None,
            "exemplos": sorted(itens, key=lambda x: -(x.get("views") or 0))[:3],
        })
    return sorted(out, key=lambda p: (-p["n"], p["slug"]))


def _fmt_views(v) -> str:
    if not v:
        return "—"
    return f"{v / 1e6:.1f} mi".replace(".", ",") if v >= 1e6 else f"{v / 1e3:.0f} mil"


def escrever_padroes_md(corpus: list[dict], mapa: dict, medidas: dict, destino: Path) -> None:
    linhas = [
        "# Padrões de gancho",
        "",
        "> Gerado por `python scripts/ganchos.py padroes`. **Não edite à mão**: mude "
        "`padroes-mapa.json` ou as fichas e rode de novo.",
        "",
        f"Corpus: {len(corpus)} ganchos das fichas de `instagram/referencias-virais/` — **só Reel e só "
        "vencedores**. Os números dizem o que os virais têm em comum, não o que separa viral de "
        "fracasso. Views lidas da grade podem incluir mídia paga (campo `organico` da ficha). O "
        "agrupamento é julgamento **[leitura minha]**; as contagens sobre ele são **[medido]**.",
        "",
        "## Padrões",
        "",
        "| Padrão | Forma | n | n café | n pt | Mediana de views (todos · café) | Exemplos, maior view primeiro |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for p in tabela_padroes(corpus, mapa):
        ex = "<br>".join(
            f"{x['perfil']} {_fmt_views(x.get('views'))}: “{(_abertura(x) or '(sem texto) ' + x['ve'])[:90]}”"
            for x in p["exemplos"])
        linhas.append(f"| **{p['nome']}** (`{p['slug']}`) | {p['forma']} | {p['n']} | {p['n_cafe']} | {p['n_pt']} | "
                      f"{_fmt_views(p['mediana_views'])} · {_fmt_views(p['mediana_views_cafe'])} | {ex} |")
    linhas += ["", "## Medidas do corpus **[medido]**", "",
               "Abertura = 1ª tela citada entre aspas + 1ª frase falada. Texto sem aspas na ficha é "
               "descrição e não conta.", "",
               "| Recorte | n | palavras na tela (mediana · p25–p75) | palavras na 1ª frase falada (idem) | pergunta | número | você | negação no início | sem texto |",
               "|---|---:|---|---|---:|---:|---:|---:|---:|"]
    for nome, b in medidas.items():
        t, f = b["palavras_tela"], b["palavras_fala_1a_frase"]
        linhas.append(f"| {nome} | {b['n']} | {t['mediana']} · {t['p25']}–{t['p75']} | "
                      f"{f['mediana']} · {f['p25']}–{f['p75']} | {b['pct_pergunta']}% | {b['pct_numero']}% | "
                      f"{b['pct_voce']}% | {b['pct_negacao_inicial']}% | {b['pct_sem_texto']}% |")
    linhas += ["", "## Vícios de IA no corpus (ganchos em que aparecem)", "",
               "Definições em `.claude/skills/canastra-ganchos/vicios-ia.md`.", "",
               "| id | " + " | ".join(medidas) + " |", "|---|" + "---:|" * len(medidas)]
    for vid in medidas["todos"]["vicios"]:
        linhas.append(f"| {vid} | " + " | ".join(str(b["vicios"][vid]) for b in medidas.values()) + " |")
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")


# --- rubrica ----------------------------------------------------------------

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
    # len >= 8 separa a tabela de regras da tabela de exemplos (3 colunas, mesmos ids)
    return [Regra(c[0], c[1], c[2], c[3], c[4], int(c[5] or 0), c[6], c[7])
            for c in _linhas_tabela(caminho, r"[PMJCR]\d+") if len(c) >= 8]


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


# --- regras mecânicas -------------------------------------------------------

#: Palavras da camada principal (manchete da capa / 1ª frase falada do Reel).
#: p25–p75 do corpus (padroes.md, 15/10/2026): tela pt 2–9; fala 1ª frase 5–13.
FAIXAS = {"capa": (2, 9), "reel": (5, 13)}
#: 2ª camada: tela do Reel 2–7 (p25–p75 do corpus); apoio da capa só tem teto de caracteres.
FAIXAS_2 = {"capa": (0, 99), "reel": (2, 7)}
#: Caracteres (manchete, apoio) = ORCAMENTO de instagram/carrossel/molde.py; um teste confere.
CARACTERES = {"capa": (60, 120)}

NUMERO_EXTENSO = re.compile(r"\b(dois|duas|tr[êe]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|"
                            r"vinte|trinta|quarenta|cinquenta|cem|cento|mil|milh[ãa]o|metade|dobro|triplo)\b", re.I)
FOLCLORE = re.compile(r"dopamina|c[ée]rebro|neuro|cortisol|serotonina|60[ .]?000|60 mil vezes", re.I)
ESCASSEZ = re.compile(r"[úu]ltimas unidades|s[óo] hoje|imperd[íi]vel|corre que|mais premiad|"
                      r"o melhor (caf[ée] )?d[oa] (brasil|mundo|minas)|[úu]nic[oa] no mundo|nunca vist", re.I)
ABERTURA = re.compile(r"^\W*(bom dia|boa tarde|boa noite|oi\b|ol[áa]\b|"
                      r"hoje (eu )?vou (falar|mostrar|contar|explicar)|hoje (a gente )?vai falar|"
                      r"neste (post|v[íi]deo)|nesse (post|v[íi]deo)|fica at[ée] o final|"
                      r"voc[êe] n[ãa]o vai acreditar)", re.I)


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
    return True, (f"fonte: {gc.fonte}" if achou else "sem número")


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
    ok = a <= n <= b
    det = [f"{n} palavras (faixa {a}–{b})"]
    if gc.formato == "capa":
        c1, c2 = CARACTERES["capa"]
        ok = ok and len(gc.manchete) <= c1 and len(gc.apoio) <= c2
        det.append(f"{len(gc.manchete)}/{c1} caracteres" + (f", apoio {len(gc.apoio)}/{c2}" if gc.apoio else ""))
    elif gc.secundario:
        a2, b2 = FAIXAS_2["reel"]
        n2 = len(palavras(gc.secundario))
        ok = ok and a2 <= n2 <= b2
        det.append(f"tela {n2} (faixa {a2}–{b2})")
    return ok, "; ".join(det)


def _conteudo(s: str) -> set[str]:
    return {sem_acento(p).lower() for p in palavras(s) if len(p) > 3}


def _m2(gc: Gancho):
    if not gc.secundario:
        return True, "sem 2ª camada"
    a, b = _conteudo(gc.principal), _conteudo(gc.secundario)
    jac = len(a & b) / len(a | b) if a | b else 0
    return jac <= 0.5, f"sobreposição {jac:.0%}"


def _m3(gc: Gancho):
    """Vícios de IA e palavras recusadas pela voz (vicios-ia.md). `onde = tela` vale só para o
    que se lê: manchete e apoio da capa, tela do Reel (10-voz.md §7)."""
    tela = gc.textos() if gc.formato == "capa" else gc.tela
    achados = [v["id"] for v in ler_vicios() if v["proibe"] == "sim"
               and v["regex"].search(tela if v["onde"] == "tela" else gc.textos())]
    return (False, "vício: " + ", ".join(achados)) if achados else (True, "")


def _m4(gc: Gancho):
    m = ABERTURA.search(gc.principal)
    return (False, f"abertura proibida: “{m.group(0).strip()}”") if m else (True, "")


MECANICAS = {"P1": _p1, "P2": _p2, "P3": _p3, "M1": _m1, "M2": _m2, "M3": _m3, "M4": _m4}


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


# --- recalibração pelo resultado real (instagram/metricas/proprios.jsonl, fluxo 1) ---

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
    """O contrato do fluxo 1 grava 1 linha por post por coleta: vale a de maior `coletado_em`."""
    ult: dict[str, dict] = {}
    for x in linhas:
        i = x.get("id")
        if i and (i not in ult or (x.get("coletado_em") or "") >= (ult[i].get("coletado_em") or "")):
            ult[i] = x
    return list(ult.values())


def metrica(post: dict, formato: str) -> float | None:
    """(saves + shares) / alcance — envios é sinal principal [oficial]; senão curtidas / alcance.
    Reel com tempo médio assistido usa ele (sinal principal [oficial]). Campo ausente = None."""
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


def shortcode(url: str | None) -> str | None:
    m = re.search(r"/(?:p|reel)/([^/?#]+)", url or "")
    return m.group(1) if m else None


def cruzar(posts: list[dict], avaliacoes: list[dict]) -> list[dict]:
    """Casa cada post com a avaliação do gancho publicado.

    1º pelo shortcode (`url` do post × `post` da avaliação escolhida); senão pelo texto: o
    `gancho` do post (que o fluxo 1 copia de instagram/metricas/ganchos.json) contra a
    manchete/fala da avaliação, normalizados. Entre avaliações de mesmo texto vale a escolhida.
    """
    por_texto: dict[str, dict] = {}
    por_post: dict[str, dict] = {}
    for a in avaliacoes:
        gc = a["gancho"]
        if a.get("escolhido") and a.get("post"):
            por_post[a["post"]] = a
        chave = normalizar(gc.get("manchete") or gc.get("fala"))
        if chave and (chave not in por_texto or a.get("escolhido") or not por_texto[chave].get("escolhido")):
            por_texto[chave] = a
    out = []
    for p in ultimas_por_id(posts):
        a = por_post.get(shortcode(p.get("url")) or "") or por_texto.get(normalizar(p.get("gancho") or ""))
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
            linha["nota"] = ("sem contraste (todos passaram)" if passou else
                             "sem contraste (todos falharam)" if falhou else "sem dado")
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
              "Gerado por `scripts/ganchos.py recalibrar`. É **proposta**: a rubrica só muda com a "
              "aprovação do Rafael. Os pesos ficam limitados a ±50% e a soma precisa ser renormalizada "
              "a 100 ao aplicar. Regra cuja mediana de quem passou supera a de quem falhou, com n "
              "razoável dos dois lados, é candidata a trocar a marca **[criador]** por **[medido]**.", ""]
    for p in props:
        linhas.append(f"## {p['formato']} — n = {p['n']}")
        if p["status"] != "ok":
            linhas += ["", f"Amostra insuficiente ({p['n']} de {p['n_min']}). Nada proposto.", ""]
            continue
        linhas += ["", "| regra | peso | proposto | fator | passou (n · mediana) | falhou (n · mediana) | nota |",
                   "|---|---:|---:|---:|---|---|---|"]
        for x in p["regras"]:
            linhas.append(f"| {x['id']} {x['nome']} | {x['peso']} | {x['peso_proposto']} | {x['fator']} | "
                          f"{x['n_passou']} · {x['mediana_passou']} | {x['n_falhou']} · {x['mediana_falhou']} | "
                          f"{x['nota']} |")
        linhas += ["", f"Soma proposta: {p['soma_proposta']} (renormalizar a 100).", ""]
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def recalibrar_cli(proprios: Path) -> int:
    posts = carregar_jsonl(proprios)
    if not posts:
        print(f"aviso: {proprios} não existe ou está vazio; nada a recalibrar "
              "(o fluxo 1 ainda não gravou métricas). A rubrica segue com os pesos atuais.")
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


# --- CLI ----------------------------------------------------------------------

def _imprime(r: dict) -> None:
    for i, v in r["resultados"].items():
        marca = {True: "ok ", False: "XX ", None: "?? "}[v["ok"]]
        peso = "portão" if v["tipo"] == "portao" else f"{v['peso']:>2}"
        print(f"{marca}{i:<3} [{peso}] {v['nome']}" + (f" — {v['detalhe']}" if v["detalhe"] else ""))
    if r["portoes_falhos"]:
        print(f"\nREPROVADO nos portões {', '.join(r['portoes_falhos'])}: nota 0")
    elif r["pendentes"]:
        dica = ",".join(p + "=1" for p in r["pendentes"])
        print(f"\nsubtotal {r['subtotal']} · faltam julgar: {', '.join(r['pendentes'])} (--julgamento {dica})")
    else:
        print(f"\nNOTA {r['nota']}/100")


def _julgamento(s: str) -> dict[str, bool]:
    out = {}
    for par in filter(None, (s or "").split(",")):
        k, v = par.split("=")
        out[k.strip().upper()] = v.strip().lower() in ("1", "s", "sim", "true")
    return out


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(prog="ganchos")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("extrair", help="fichas de virais -> instagram/ganchos/corpus.jsonl")
    sub.add_parser("medir", help="imprime as medidas do corpus (JSON)")
    sub.add_parser("padroes", help="corpus + padroes-mapa.json -> padroes.md")
    c = sub.add_parser("checar", help="aplica a rubrica a um gancho")
    c.add_argument("--formato", choices=FORMATOS, required=True)
    for campo in ("manchete", "apoio", "fala", "tela", "fonte", "julgamento", "tema", "post"):
        c.add_argument(f"--{campo}", default="")
    c.add_argument("--json", action="store_true")
    c.add_argument("--registrar", action="store_true", help="anexa a avaliacoes.jsonl")
    c.add_argument("--escolhido", action="store_true", help="marca como o gancho escolhido/publicado")
    rc = sub.add_parser("recalibrar", help="propõe pesos a partir de proprios.jsonl")
    rc.add_argument("--proprios", default=str(PROPRIOS))
    a = ap.parse_args(argv)

    if a.cmd == "extrair":
        corpus = extrair()
        SAIDA.mkdir(parents=True, exist_ok=True)
        (SAIDA / "corpus.jsonl").write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in corpus), encoding="utf-8")
        print(f"{len(corpus)} ganchos -> {SAIDA / 'corpus.jsonl'}")
        return 0
    if a.cmd in ("medir", "padroes"):
        corpus = carregar_jsonl(SAIDA / "corpus.jsonl")
        if not corpus:
            print("corpus vazio: rode `extrair` antes")
            return 2
        med = medir(corpus, ler_vicios())
        if a.cmd == "medir":
            print(json.dumps(med, ensure_ascii=False, indent=1))
            return 0
        mapa = json.loads((SAIDA / "padroes-mapa.json").read_text(encoding="utf-8"))
        sem = [x["id"] for x in corpus if x["id"] not in mapa["mapa"]]
        if sem:
            print(f"padroes-mapa.json não cobre {len(sem)} ganchos: {', '.join(sem)}")
            return 2
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
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=1))
        else:
            _imprime(r)
        if a.registrar:
            registrar(r, tema=a.tema, escolhido=a.escolhido, post=a.post or None)
        return 0
    if a.cmd == "recalibrar":
        return recalibrar_cli(Path(a.proprios))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
