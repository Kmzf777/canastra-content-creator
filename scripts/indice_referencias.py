"""Biblioteca de referências virais: lê o bloco "## 0. Etiquetas" de cada ficha em
instagram/referencias-virais/videos/<frente>/*.md e gera INDICE.md + indice.json.

Vídeo novo entra assim: crie a ficha no mesmo modelo (seções 0 a 7, ver LEIA-ME.md)
e rode de novo. Campo fora do vocabulário é recusado, para o índice não virar sopa.

    python scripts/indice_referencias.py
    python scripts/indice_referencias.py buscar torra selecao      # filtra por termo
"""

from __future__ import annotations

import io

import json
import re
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path("instagram/referencias-virais")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
CAMPOS = ["frente", "perfil", "id", "views", "curtidas", "duracao_s", "data", "cortes_por_10s", "idioma", "pais",
          "quem_aparece", "formato", "gancho", "fala", "humor", "etapas", "torra_mostrada", "organico", "licao"]
VOCAB = {
    "frente": {"processo", "brasil", "influenciadores", "marcas",
               "motion-criadores", "motion-marcas", "motion-3d-fooh", "motion-brasil"},
    "quem_aparece": {"produtor-familia", "trabalhador", "criador-especialista", "equipe-marca", "convidado",
                     "maos-apenas", "ninguem"},
    "formato": {"asmr-processo", "tarefa-continua", "produtor-fala", "esquete-humor", "experimento",
                "tutorial-preparo", "comparacao", "mito-verdade", "minidoc-pessoa", "evento-comunidade", "collab",
                "produto-estudio", "vida-real", "outro",
                # motion (coleta de 12/10/2026)
                "motion-colagem", "kinetic-type", "animacao-2d", "cgi-3d", "fooh", "stop-motion", "live-mais-motion",
                "ui-produto", "mascote-personagem", "breakdown-making-of"},
    "gancho": {"imagem-estranha", "resultado-primeiro", "pergunta", "numero-contraintuitivo", "segredo",
               "conflito-vilao", "acao-no-meio", "pessoa-falando", "humor-situacao"},
    "fala": {"criador-na-camera", "off-da-pessoa", "sem-fala", "so-texto"},
    "humor": {"nenhum", "do-cafe", "da-vida-real", "fora-do-cafe", "do-produto", "fora-do-produto"},
    "etapas": {"colheita", "boia-lavagem", "terreiro-secagem", "beneficiamento", "selecao", "torra",
               "prova-cupping", "preparo", "consumo", "preco", "supermercado", "fazenda-paisagem", "nenhuma"},
    "torra_mostrada": {"nao-aparece", "cor-do-grao", "fogo-chama", "so-texto"},
    "organico": {"sim", "provavel-pago", "collab", "incerto"},
}
# Campos opcionais (fichas de motion): tecnica é lista de vocabulário; os outros, texto livre.
OPCIONAIS = ["tecnica", "ferramentas", "categoria_marca", "metodo"]
VOCAB_TECNICA = {"colagem-recorte", "kinetic-type", "parallax-2-5d", "camera-virtual", "match-cut", "morph-transicao",
                 "chicote-whip", "mascara-revelacao", "rotoscopia", "tracking-3d", "cgi-fotoreal", "personagem-2d",
                 "stop-motion-real", "loop-perfeito", "sound-design-sincronizado", "legenda-animada", "ui-animada",
                 "grafismo-dados", "textura-papel-grao", "ia-gerativa", "outro"}
LISTAS = {"gancho", "etapas", "tecnica"}


def ler(arq: Path) -> dict:
    texto = arq.read_text(encoding="utf-8")
    m = re.search(r"^## 0\. Etiquetas\s*\n(.*?)(?=^## )", texto, flags=re.S | re.M)
    if not m:
        raise SystemExit(f"{arq}: sem bloco '## 0. Etiquetas'")
    d: dict = {}
    for linha in m.group(1).splitlines():
        lm = re.match(r"^- (\w+):\s*(.*)$", linha.strip())
        if lm:
            d[lm.group(1)] = lm.group(2).strip()
    faltam = [c for c in CAMPOS if c not in d]
    if faltam:
        raise SystemExit(f"{arq}: faltam campos {faltam}")
    for c in OPCIONAIS:
        d.setdefault(c, "")
    for c in LISTAS:
        d[c] = [v.strip() for v in d[c].split(",") if v.strip()]
    ruins = [v for v in d["tecnica"] if v not in VOCAB_TECNICA]
    if ruins:
        raise SystemExit(f"{arq}: 'tecnica' fora do vocabulário: {ruins}")
    for c, ok in VOCAB.items():
        vals = d[c] if c in LISTAS else [d[c]] if d[c] else []
        ruins = [v for v in vals if v not in ok]
        if ruins:
            raise SystemExit(f"{arq}: '{c}' fora do vocabulário: {ruins}")
    for c in ("views", "curtidas"):
        d[c] = int(d[c]) if d[c] else None
    for c in ("duracao_s", "cortes_por_10s"):
        d[c] = float(d[c].replace(",", ".")) if d[c] else None
    titulo = texto.splitlines()[0].lstrip("# ").strip()
    d["titulo"] = titulo
    d["arquivo"] = arq.relative_to(RAIZ).as_posix()
    d["link"] = f"https://www.instagram.com/reel/{d['id']}/"
    return d


def carregar() -> list[dict]:
    itens = [ler(a) for a in sorted((RAIZ / "videos").glob("*/*.md"))]
    return sorted(itens, key=lambda d: -(d["views"] or 0))


def fmt_views(v: int | None) -> str:
    if v is None:
        return "?"
    return f"{v / 1e6:.1f} mi".replace(".", ",") if v >= 1e6 else f"{v / 1e3:.0f} mil"


def linha(d: dict) -> str:
    return (f"| [{d['perfil']} · {d['id']}]({d['arquivo']}) | {fmt_views(d['views'])} | {d['frente']} | {d['formato']} | "
            f"{', '.join(d['gancho'])} | {d['fala']} | {', '.join(d['etapas'])} | {d['torra_mostrada']} | "
            f"{d['duracao_s'] or '?'} s | {d['licao']} |")


CAB = ("| Vídeo | Views | Frente | Formato | Gancho | Fala | Etapas | Torra | Duração | Lição |\n"
       "|---|---|---|---|---|---|---|---|---|---|")


def gerar() -> None:
    itens = carregar()
    (RAIZ / "indice.json").write_text(json.dumps(itens, ensure_ascii=False, indent=1), encoding="utf-8")
    md = [
        "# Índice da biblioteca de referências virais",
        "",
        f"Gerado por `scripts/indice_referencias.py` a partir de {len(itens)} fichas. **Não edite à mão**: "
        "edite a ficha e rode o script. Como usar e regras: [LEIA-ME.md](LEIA-ME.md). "
        "Relatório com as conclusões: [relatorio.md](relatorio.md).",
        "",
        "## Panorama",
        "",
    ]
    for campo in ("frente", "formato", "fala", "humor", "torra_mostrada", "quem_aparece", "organico"):
        c = Counter(d[campo] for d in itens)
        md.append(f"- **{campo}:** " + " · ".join(f"{k} {v}" for k, v in c.most_common()))
    for campo in ("gancho", "etapas", "tecnica"):
        c = Counter(v for d in itens for v in d[campo])
        md.append(f"- **{campo}:** " + " · ".join(f"{k} {v}" for k, v in c.most_common()))
    md += ["", "## Todos, por views", "", CAB] + [linha(d) for d in itens]
    for campo, titulo in (("etapas", "Por etapa do processo"), ("formato", "Por formato"), ("gancho", "Por tipo de gancho"),
                         ("tecnica", "Por técnica de motion")):
        md += ["", f"## {titulo}"]
        valores = sorted({v for d in itens for v in (d[campo] if campo in LISTAS else [d[campo]])})
        for v in valores:
            sel = [d for d in itens if v in (d[campo] if campo in LISTAS else [d[campo]])]
            md += ["", f"### {v} ({len(sel)})", "", CAB] + [linha(d) for d in sel]
    (RAIZ / "INDICE.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{len(itens)} fichas → {RAIZ}/INDICE.md e indice.json")


def buscar(termos: list[str]) -> None:
    termos = [t.lower() for t in termos]
    for d in carregar():
        alvo = json.dumps(d, ensure_ascii=False).lower()
        if all(t in alvo for t in termos):
            print(f"{fmt_views(d['views']):>9}  {d['perfil']:28s} {d['formato']:18s} {RAIZ / d['arquivo']}\n"
                  f"           {d['licao']}")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "buscar":
        buscar(sys.argv[2:])
    else:
        gerar()
