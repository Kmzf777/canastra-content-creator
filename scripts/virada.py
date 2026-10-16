"""Detector de virada: em que post o desempenho de um perfil do Instagram mudou de patamar.

Lê a série gravada pelo coletor do fluxo 1 (instagram/metricas/), calcula a linha de base
móvel (mediana dos k posts anteriores) e marca três coisas que NÃO são a mesma:

- degrau sustentado: o patamar subiu e ficou;
- queda de patamar: o patamar desceu e ficou;
- pico isolado: um post estourou e o perfil voltou ao patamar.

Para cada degrau e queda, compara a janela antes com a janela depois: formato, cadência,
legenda, palavras e hashtags novas. Calcula e não interpreta; a leitura é da skill
canastra-virada. Grava instagram/viradas/<handle>/<AAAA-MM-DD>.json e .html.

    python scripts/virada.py orfeucafes
    python scripts/virada.py orfeucafes --dias 90          # rodada rápida
    python scripts/virada.py cafecanastra --dias 0         # histórico inteiro
    python scripts/virada.py fulano --arquivo instagram/viradas/fulano/_coleta-manual.jsonl

Spec: docs/superpowers/specs/2026-10-15-detector-virada-design.md. Só stdlib.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from statistics import median, pstdev

RAIZ_METRICAS = Path("instagram/metricas")
RAIZ_SAIDA = Path("instagram/viradas")
PROPRIO = "cafecanastra"

PADROES = {"k": 12, "m": 8, "pico": 3.0, "degrau": 1.8, "queda": 0.55, "sustentacao": 0.6}
MIN_BASE = 6            # menos que isso de posts anteriores e a mediana não é linha de base
MIN_DEPOIS = 5          # menos que isso adiante e não dá para dizer se o patamar ficou
MIN_CONFIRMA_PICO = 3   # pico com menos seguintes ainda pode ser o começo de um degrau
VOLTA_AO_PATAMAR = 1.5  # seguintes abaixo disso × base = o perfil voltou depois do pico
FRACAO_VIEWS = 0.6      # views só vira série quando a maioria dos posts traz o número
AUSENTE, PRESENTE = 0.15, 0.40  # assinatura: surgiu = ≤ 15% dos posts antes e ≥ 40% depois
T_FORTE, T_MODERADA = 4.0, 2.5  # confiança do degrau pelo t de Welch sobre log1p
CV_ESTAVEL, MAX_ESTAVEL = 1.2, 6.0  # perfil "estável": CV < 1,2 e máximo < 6× a mediana

# Heurísticas de legenda em pt-BR. São regex, não leitura: confira as legendas na dúvida.
CTA_RE = re.compile(
    r"\bcoment(a|e|em|ar)\b|\blink na bio\b|\b(chama|manda|mande)\b[^.!?\n]{0,15}"
    r"\b(dm|direct|inbox|whats(app)?|mensagem)\b|\bcupo(m|ns)\b|\bfrete\b|\bcompr(e|ar)\b"
    r"|\bgaranta\b|\bpeça (já|o seu|a sua)\b|\bc[oó]digo\b",
    re.I)
PRODUTO_RE = re.compile(
    r"\bpacotes?\b|\bc[aá]psulas?\b|\bem gr[aã]os?\b|\bmo[ií]do\b|\b\d+\s?(g|kg)\b|\bkits?\b|r\$"
    r"|\bpre[cç]o\b|\bpromo|\bloja\b|\bnosso caf[eé]\b",
    re.I)
MENCAO_RE = re.compile(r"(?<![\w.])@[\w.]{2,}")  # @perfil; e-mail (a@b.com) não conta

ESTADOS = ("sem_base", "normal", "degrau", "queda", "pico", "puxador", "imaturo")

STOPWORDS = set("""
    para pelo pela pelos pelas com sem sobre entre ate até desde como mais menos muito muita
    muitos muitas pouco você voce vocês voces nosso nossa nossos nossas seu sua seus suas
    esse essa esses essas este esta estes estas isso isto aquele aquela aqui ali onde quando
    quem qual quais porque porquê então entao também tambem ainda agora sempre nunca cada
    todo toda todos todas outro outra outros outras mesmo mesma depois antes tudo nada algo
    alguém alguem fazer feito faz foram eram está estão estao estava ser sido sendo será
    sera têm tem ter tinha temos vamos vai vão vou pode podem deve aqui lhe dele dela deles
    delas numa num umas uns pra pro pros pras that this with from your have
""".split())

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
_MINIMO = datetime.min.replace(tzinfo=timezone.utc)


class PerfilAusente(Exception):
    """O perfil não tem série gravada pelo fluxo 1."""


@dataclass
class Post:
    id: str
    url: str
    data: datetime
    tipo: str
    legenda: str
    curtidas: int | None
    comentarios: int | None
    views: int | None
    seguidores: int | None
    coletado_em: datetime | None

    @property
    def engajamento(self) -> int | None:
        if self.curtidas is None or self.comentarios is None:
            return None
        return self.curtidas + self.comentarios


# --- leitura do contrato do fluxo 1 --------------------------------------------------------

def normalizar_handle(handle: str) -> str:
    return handle.strip().lstrip("@").lower()


def parse_data(valor) -> datetime | None:
    """ISO 8601 com `Z`, `+0000` ou `+00:00`. Sem fuso = UTC. Qualquer outra coisa = None."""
    if not isinstance(valor, str) or not valor.strip():
        return None
    texto = valor.strip().replace("Z", "+00:00")
    texto = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", texto)
    try:
        dt = datetime.fromisoformat(texto)
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _inteiro(valor) -> int | None:
    if valor is None or isinstance(valor, bool):
        return None
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def _carimbo(post: Post) -> datetime:
    return post.coletado_em or _MINIMO


def ler_jsonl(caminho: Path) -> tuple[list[Post], dict]:
    """Lê o .jsonl do fluxo 1, em ordem de publicação.

    O mesmo `id` em coletas diferentes é a mesma postagem: fica o `coletado_em` mais recente.
    Linha ruim é contada e reportada, nunca derruba a leitura.
    """
    contagem = {"linhas": 0, "invalidas": 0, "duplicados": 0}
    por_id: dict[str, Post] = {}
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        contagem["linhas"] += 1
        try:
            bruto = json.loads(linha)
            post = Post(
                id=str(bruto["id"]),
                url=str(bruto.get("url") or ""),
                data=parse_data(bruto.get("data_publicacao")),
                tipo=str(bruto.get("tipo") or "?").upper(),
                legenda=str(bruto.get("legenda") or ""),
                curtidas=_inteiro(bruto.get("curtidas")),
                comentarios=_inteiro(bruto.get("comentarios")),
                views=_inteiro(bruto.get("views")),
                # proprios.jsonl grava `seguidores_conta`; concorrentes, `seguidores`
                seguidores=_inteiro(bruto.get("seguidores", bruto.get("seguidores_conta"))),
                coletado_em=parse_data(bruto.get("coletado_em")),
            )
        except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
            contagem["invalidas"] += 1
            continue
        if post.data is None:
            contagem["invalidas"] += 1
            continue
        anterior = por_id.get(post.id)
        if anterior is not None:
            contagem["duplicados"] += 1
            if _carimbo(post) < _carimbo(anterior):
                continue
        por_id[post.id] = post
    return sorted(por_id.values(), key=lambda p: p.data), contagem


def na_watchlist(handle: str, raiz: Path) -> bool:
    """O formato da watchlist ainda não foi publicado: procura o handle em qualquer string."""
    arq = raiz / "watchlist.json"
    if not arq.exists():
        return False
    try:
        pilha = [json.loads(arq.read_text(encoding="utf-8"))]
    except json.JSONDecodeError:
        return False
    while pilha:
        item = pilha.pop()
        if isinstance(item, dict):
            pilha.extend(item.values())
        elif isinstance(item, list):
            pilha.extend(item)
        elif isinstance(item, str) and normalizar_handle(item) == handle:
            return True
    return False


def localizar(handle: str, raiz: Path = RAIZ_METRICAS) -> Path:
    h = normalizar_handle(handle)
    candidatos = ([raiz / "proprios.jsonl"] if h == PROPRIO else
                  [raiz / "concorrentes" / f"{h}.jsonl", raiz / "concorrentes" / f"@{h}.jsonl"])
    for caminho in candidatos:
        if caminho.exists():
            return caminho
    caminho = candidatos[0]
    if not raiz.exists():
        motivo = f"{raiz}/ não existe: a coleta do fluxo 1 ainda não rodou nesta cópia do repositório."
    elif na_watchlist(h, raiz):
        motivo = f"@{h} está na watchlist, mas {caminho} ainda não foi gravado: rode a coleta do fluxo 1."
    else:
        motivo = (f"@{h} não está na watchlist do fluxo 1 ({raiz / 'watchlist.json'}): "
                  "peça a inclusão e rode a coleta.")
    raise PerfilAusente(motivo + " Fallback explícito: ler o perfil pelo Claude in Chrome e passar "
                                 "--arquivo (ver .claude/skills/canastra-virada/SKILL.md).")


# --- detecção ------------------------------------------------------------------------------

def _log_media(valores) -> float:
    return sum(math.log1p(x) for x in valores) / len(valores)


def _welch(antes: list[float], depois: list[float]) -> float | None:
    """t de Welch de (depois − antes) sobre log1p. None quando os dois lados não variam."""
    la, lb = [math.log1p(x) for x in antes], [math.log1p(x) for x in depois]
    if len(la) < 2 or len(lb) < 2:
        return None
    ma, mb = sum(la) / len(la), sum(lb) / len(lb)
    va = sum((x - ma) ** 2 for x in la) / (len(la) - 1)
    vb = sum((x - mb) ** 2 for x in lb) / (len(lb) - 1)
    erro = math.sqrt(va / len(la) + vb / len(lb))
    return None if erro == 0 else (mb - ma) / erro


def _confianca(t: float | None) -> str:
    if t is None:
        return "sem variância"
    return "forte" if abs(t) >= T_FORTE else "moderada" if abs(t) >= T_MODERADA else "fraca"


def _selecao_gulosa(candidatos: list[int], contraste: list, m: int, maior: bool) -> list[int]:
    """Candidatos vizinhos são o mesmo degrau visto de vários índices: fica o de contraste
    mais extremo, saem os que estão a menos de m posts dele, e repete."""
    restantes = sorted(candidatos, key=lambda i: contraste[i], reverse=maior)
    escolhidos: list[int] = []
    for i in restantes:
        if all(abs(i - j) >= m for j in escolhidos):
            escolhidos.append(i)
    return sorted(escolhidos)


def detectar(valores: list[float], k: int = 12, m: int = 8, pico: float = 3.0, degrau: float = 1.8,
             queda: float = 0.55, sustentacao: float = 0.6) -> dict:
    """Detecção sobre uma lista de números já em ordem cronológica.

    Devolve, por índice, base, razão do post, razão de nível e estado, e a lista de eventos.
    """
    n = len(valores)
    base: list[float | None] = [None] * n
    razao: list[float | None] = [None] * n
    nivel: list[float | None] = [None] * n
    contraste: list[float | None] = [None] * n
    sobe, desce = [], []

    for i in range(n):
        anteriores = valores[max(0, i - k):i]
        if len(anteriores) < MIN_BASE:
            continue
        base[i] = median(anteriores)
        b = max(base[i], 1)
        razao[i] = valores[i] / b
        depois = valores[i:i + m]
        if len(depois) < MIN_DEPOIS:
            continue
        nivel[i] = median(depois) / b
        contraste[i] = _log_media(depois) - _log_media(anteriores)
        acima = sum(x > base[i] for x in depois) / len(depois)
        abaixo = sum(x < base[i] for x in depois) / len(depois)
        if nivel[i] >= degrau and acima >= sustentacao:
            sobe.append(i)
        if nivel[i] <= queda and abaixo >= sustentacao:
            desce.append(i)

    degraus = _selecao_gulosa(sobe, contraste, m, maior=True)
    quedas = _selecao_gulosa(desce, contraste, m, maior=False)

    estados = ["sem_base" if base[i] is None else "normal" for i in range(n)]
    eventos = []
    for tipo, pontos in (("degrau", degraus), ("queda", quedas)):
        for i in pontos:
            estados[i] = tipo
            anteriores, depois = valores[max(0, i - k):i], valores[i:i + m]
            t = _welch(anteriores, depois)
            eventos.append({
                "tipo": tipo, "i": i, "nivel": round(nivel[i], 2), "contraste": round(contraste[i], 3),
                "base_antes": base[i], "mediana_depois": median(depois),
                "n_antes": len(anteriores), "n_depois": len(depois),
                "t_welch": None if t is None else round(t, 2), "confianca": _confianca(t),
            })
    for i in degraus:
        for j in range(i + 1, min(n, i + m)):
            if valores[j] >= pico * max(base[i], 1) and estados[j] == "normal":
                estados[j] = "puxador"

    for i in range(n):
        if razao[i] is None or razao[i] < pico or estados[i] != "normal":
            continue
        seguintes = valores[i + 1:i + 1 + m]
        if seguintes and median(seguintes) >= VOLTA_AO_PATAMAR * max(base[i], 1):
            continue  # o perfil não voltou ao patamar; não é pico isolado
        estados[i] = "pico"
        eventos.append({
            "tipo": "pico", "i": i, "razao": round(razao[i], 2), "base_antes": base[i],
            "seguintes": len(seguintes), "confirmado": len(seguintes) >= MIN_CONFIRMA_PICO,
        })

    eventos.sort(key=lambda e: e["i"])
    return {"base": base, "razao": razao, "nivel": nivel, "estados": estados, "eventos": eventos}


# --- o que mudou ao redor ------------------------------------------------------------------

def primeira_linha(legenda: str, limite: int = 140) -> str:
    for linha in legenda.splitlines():
        if linha.strip():
            linha = linha.strip()
            return linha if len(linha) <= limite else linha[:limite - 1] + "…"
    return ""


def _hashtags(texto: str) -> list[str]:
    return [h.lower() for h in re.findall(r"#(\w+)", texto)]


def _palavras(texto: str) -> list[str]:
    limpo = re.sub(r"https?://\S+|[#@]\w+", " ", texto.lower())
    return [p for p in re.findall(r"[^\W\d_]{4,}", limpo) if p not in STOPWORDS]


def _fatias(extrair, posts: list[Post], de) -> dict[str, float]:
    """Fração dos posts em que cada termo aparece (conta post, não ocorrência)."""
    contagem = Counter(t for p in posts for t in set(extrair(de(p))))
    return {t: c / len(posts) for t, c in contagem.items()} if posts else {}


def _assinatura(extrair, antes: list[Post], depois: list[Post], de=lambda p: p.legenda,
                limite: int = 15) -> dict:
    """O que surgiu (≤ 15% → ≥ 40% dos posts), sumiu (o espelho) e se manteve (≥ 40% nos dois).

    O que se manteve é tão informativo quanto o que surgiu: o que o perfil NÃO mudou na
    virada fica fora da explicação."""
    fa, fd = _fatias(extrair, antes, de), _fatias(extrair, depois, de)
    grupos = {"surgiram": [], "sumiram": [], "mantidos": []}
    for termo in sorted(set(fa) | set(fd)):
        a, d = fa.get(termo, 0.0), fd.get(termo, 0.0)
        item = {"termo": termo, "antes": round(a, 2), "depois": round(d, 2)}
        if a <= AUSENTE and d >= PRESENTE:
            grupos["surgiram"].append(item)
        elif a >= PRESENTE and d <= AUSENTE:
            grupos["sumiram"].append(item)
        elif a >= PRESENTE and d >= PRESENTE:
            grupos["mantidos"].append(item)
    for nome, chave in (("surgiram", "depois"), ("sumiram", "antes"), ("mantidos", "depois")):
        grupos[nome] = sorted(grupos[nome], key=lambda x: -x[chave])[:limite]
    return grupos


def _comentarios_por_curtida(posts: list[Post]) -> float | None:
    """Sinal de funil: legenda que pede comentário (comentário → DM) puxa a razão para cima."""
    pares = [(p.curtidas, p.comentarios) for p in posts if p.curtidas is not None and p.comentarios is not None]
    curtidas = sum(c for c, _ in pares)
    return round(sum(x for _, x in pares) / curtidas, 3) if curtidas else None


def _fatia(regex: re.Pattern, posts: list[Post]) -> float:
    return round(sum(bool(regex.search(p.legenda)) for p in posts) / len(posts), 2)


def _consistencia(valores: list[float]) -> dict | None:
    """Perfil estável (faixa apertada em torno da mediana) × dependente de pico (vive de estouros)."""
    if len(valores) < MIN_BASE:
        return None
    med, media = median(valores), sum(valores) / len(valores)
    cv = pstdev(valores) / media if media else None
    max_med = max(valores) / med if med else None
    central = sum(0.5 * med <= x <= 2 * med for x in valores) / len(valores)
    estavel = cv is not None and max_med is not None and cv < CV_ESTAVEL and max_med < MAX_ESTAVEL
    return {
        "n": len(valores), "mediana": med,
        "cv": None if cv is None else round(cv, 2),
        "max_sobre_mediana": None if max_med is None else round(max_med, 1),
        "faixa_central": round(central, 2),
        "leitura": "estável" if estavel else "dependente de pico",
    }


def _janela(posts: list[Post]) -> dict:
    datas = [p.data for p in posts]
    span = (datas[-1] - datas[0]).total_seconds() / 86400 if len(datas) >= 2 else 0
    intervalos = [(b - a).total_seconds() / 86400 for a, b in zip(datas, datas[1:])]
    return {
        "posts": len(posts),
        "de": datas[0].date().isoformat(),
        "ate": datas[-1].date().isoformat(),
        "formatos": dict(Counter(p.tipo for p in posts)),
        "cadencia_semana": round((len(posts) - 1) / span * 7, 2) if span > 0 else None,
        "intervalo_mediano_dias": round(median(intervalos), 1) if intervalos else None,
        "legenda_mediana_chars": median(len(p.legenda) for p in posts),
        "hashtags_mediana": median(len(_hashtags(p.legenda)) for p in posts),
        "comentarios_por_curtida": _comentarios_por_curtida(posts),
        "cta_fatia": _fatia(CTA_RE, posts),
        "produto_fatia": _fatia(PRODUTO_RE, posts),
        "colab_fatia": _fatia(MENCAO_RE, posts),
    }


def antes_depois(posts: list[Post], valores: list[float], i: int, k: int, m: int) -> dict:
    antes, depois = posts[max(0, i - k):i], posts[i:i + m]
    base = median(valores[max(0, i - k):i])
    return {
        "antes": _janela(antes),
        "depois": _janela(depois),
        "puxaram": [
            {"id": p.id, "url": p.url, "data": p.data.date().isoformat(), "tipo": p.tipo, "valor": x,
             "razao": round(x / max(base, 1), 2), "comentarios_por_curtida": _comentarios_por_curtida([p]),
             "primeira_linha": primeira_linha(p.legenda)}
            for p, x in zip(depois, valores[i:i + m]) if x > base
        ],
        "palavras": _assinatura(_palavras, antes, depois),
        "hashtags": _assinatura(_hashtags, antes, depois),
        "tipos": _assinatura(lambda tipo: [tipo], antes, depois, de=lambda p: p.tipo),
    }


# --- relatório -----------------------------------------------------------------------------

def _post_json(p: Post, valor, base=None, razao=None, estado="normal") -> dict:
    return {
        "id": p.id, "url": p.url, "data": p.data.isoformat(), "tipo": p.tipo, "valor": valor,
        "base": base, "razao": None if razao is None else round(razao, 2), "estado": estado,
        "primeira_linha": primeira_linha(p.legenda),
    }


def _serie(maduros: list[Post], imaturos: list[Post], extrair, params: dict) -> dict:
    validos = [p for p in maduros if extrair(p) is not None]
    valores = [extrair(p) for p in validos]
    det = detectar(valores, **params)
    posts = [_post_json(p, x, det["base"][i], det["razao"][i], det["estados"][i])
             for i, (p, x) in enumerate(zip(validos, valores))]
    posts += [_post_json(p, extrair(p), estado="imaturo") for p in imaturos]
    eventos = []
    for ev in det["eventos"]:
        p = validos[ev["i"]]
        evento = {**ev, "post": _post_json(p, valores[ev["i"]], estado=ev["tipo"])}
        if ev["tipo"] in ("degrau", "queda"):
            evento["antes_depois"] = antes_depois(validos, valores, ev["i"], params["k"], params["m"])
        eventos.append(evento)
    return {"posts": posts, "eventos": eventos, "sem_valor": len(maduros) - len(validos),
            "avaliados": len(valores)}


def analisar(perfil: str, fonte: Path, posts: list[Post], contagem: dict, params: dict, hoje: date,
             dias: int, maturidade: int) -> dict:
    agora = datetime(hoje.year, hoje.month, hoje.day, 23, 59, 59, tzinfo=timezone.utc)
    janela = [p for p in posts if dias <= 0 or p.data >= agora - timedelta(days=dias)]
    limite = agora - timedelta(days=maturidade)
    maduros = [p for p in janela if p.data <= limite]
    imaturos = [p for p in janela if p.data > limite]
    avisos = []
    consistencia = _consistencia([p.engajamento for p in maduros if p.engajamento is not None])

    if contagem.get("invalidas"):
        avisos.append(f"{contagem['invalidas']} linha(s) inválida(s) no arquivo foram ignoradas.")
    series = {"engajamento": _serie(maduros, imaturos, lambda p: p.engajamento, params)}
    minimo = MIN_BASE + MIN_DEPOIS
    if series["engajamento"]["avaliados"] < minimo:
        avisos.append(f"série curta: {series['engajamento']['avaliados']} posts maduros na janela; "
                      f"são precisos ao menos {minimo} para avaliar um degrau.")
    com_views = sum(p.views is not None for p in maduros)
    if maduros and com_views / len(maduros) >= FRACAO_VIEWS:
        series["views"] = _serie(maduros, imaturos, lambda p: p.views, params)
    elif com_views:
        avisos.append(f"views em só {com_views} de {len(maduros)} posts maduros: abaixo de "
                      f"{FRACAO_VIEWS:.0%}, a série de views não foi analisada.")

    ultimo = max((p for p in posts if p.seguidores is not None), key=_carimbo, default=None)
    return {
        "perfil": f"@{normalizar_handle(perfil)}",
        "fonte": str(fonte),
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "hoje": hoje.isoformat(),
        "janela_dias": dias,
        "maturidade_dias": maturidade,
        "parametros": params,
        "contagens": {
            **contagem,
            "posts_unicos": len(posts),
            "fora_da_janela": len(posts) - len(janela),
            "imaturos": len(imaturos),
            "maduros": len(maduros),
        },
        "consistencia": consistencia,
        "seguidores_coleta": None if ultimo is None else {
            "valor": ultimo.seguidores,
            "coletado_em": ultimo.coletado_em.isoformat() if ultimo.coletado_em else None,
            "aviso": "número do dia da coleta, não o da data de cada post; por isso nada é normalizado por seguidor.",
        },
        "series": series,
        "avisos": avisos,
    }


def gravar(rel: dict, pasta: Path) -> tuple[Path, Path]:
    pasta.mkdir(parents=True, exist_ok=True)
    caminho_json = pasta / f"{rel['hoje']}.json"
    caminho_html = pasta / f"{rel['hoje']}.html"
    caminho_json.write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")
    caminho_html.write_text(render_html(rel), encoding="utf-8")
    return caminho_json, caminho_html


def resumo(rel: dict) -> str:
    linhas = [f"{rel['perfil']}: {rel['contagens']['maduros']} posts maduros "
              f"({rel['contagens']['imaturos']} imaturos) em "
              f"{'todo o histórico' if rel['janela_dias'] <= 0 else str(rel['janela_dias']) + ' dias'}"]
    c = rel["consistencia"]
    if c:
        linhas.append(f"  consistência: {c['leitura']} (CV {_num(c['cv'])}, máximo {_num(c['max_sobre_mediana'])}× "
                      f"a mediana, {c['faixa_central']:.0%} dos posts entre 0,5× e 2×)")
    for nome, serie in rel["series"].items():
        tipos = Counter(e["tipo"] for e in serie["eventos"])
        linhas.append(f"  {nome}: {tipos['degrau']} degrau(s), {tipos['queda']} queda(s), {tipos['pico']} pico(s)")
        for e in serie["eventos"]:
            fator = e["nivel"] if "nivel" in e else e["razao"]
            confianca = f"  confiança {e['confianca']}" if "confianca" in e else ""
            linhas.append(f"    {e['tipo']:<6} {e['post']['data'][:10]}  {_num(fator)}×  "
                          f"{e['post']['tipo']:<14} {e['post']['url']}{confianca}")
    linhas += [f"  aviso: {a}" for a in rel["avisos"]]
    return "\n".join(linhas)


# --- HTML ----------------------------------------------------------------------------------

NOMES_TIPO = {"REEL": "Reel", "VIDEO": "Vídeo", "CAROUSEL_ALBUM": "Carrossel", "IMAGE": "Foto"}
CLASSE_TIPO = {"REEL": "reel", "VIDEO": "reel", "CAROUSEL_ALBUM": "carrossel", "IMAGE": "foto"}
TITULO_EVENTO = {"degrau": "Degrau sustentado", "queda": "Queda de patamar", "pico": "Pico isolado"}


def _num(x) -> str:
    """Número em pt-BR: 12.345 e 3,8."""
    if x is None:
        return "—"
    if isinstance(x, float) and not x.is_integer():
        casas = 2 if abs(x) < 1 else 1
        texto = f"{x:,.{casas}f}".rstrip("0").rstrip(".")
        return texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{int(x):,}".replace(",", ".")


def _e(texto) -> str:
    return html.escape(str(texto), quote=True)


def _pct(x) -> str:
    return "—" if x is None else f"{x:.0%}"


def _data_br(iso: str) -> str:
    return f"{iso[8:10]}/{iso[5:7]}/{iso[:4]}"


def _marcas_y(vmin: float, vmax: float) -> list[int]:
    """Marcas 1-2-5 de vmin a vmax (escala log)."""
    marcas, e = [], 0
    while True:
        for f in (1, 2, 5):
            x = f * 10 ** e
            if x > vmax * 1.05:
                return marcas or [1]
            if x >= vmin:
                marcas.append(x)
        e += 1


def _piso_y(vmin: float) -> float:
    """Maior marca 1-2-5 abaixo do menor valor: o eixo não começa em 1 à toa."""
    piso = 0.0
    for e in range(0, 9):
        for f in (1, 2, 5):
            if f * 10 ** e <= vmin * 0.9:
                piso = f * 10 ** e
    return piso


def _marcas_x(t0: datetime, t1: datetime) -> list[datetime]:
    meses = (t1.year - t0.year) * 12 + t1.month - t0.month + 1
    passo = max(1, math.ceil(meses / 12))
    marcas, ano, mes = [], t0.year, t0.month
    while (ano, mes) <= (t1.year, t1.month):
        d = datetime(ano, mes, 1, tzinfo=timezone.utc)
        if t0 <= d <= t1:
            marcas.append(d)
        mes += passo
        while mes > 12:
            mes, ano = mes - 12, ano + 1
    return marcas


def _svg(serie: dict) -> str:
    pts = [p for p in serie["posts"] if p["valor"] is not None]
    if not pts:
        return '<p class="vazio">Sem posts com valor nesta série.</p>'
    W, H, L, R, T, B = 1000, 360, 58, 18, 14, 34
    datas = [datetime.fromisoformat(p["data"]) for p in pts]
    t0, t1 = min(datas), max(datas)
    span = (t1 - t0).total_seconds() or 1
    vmax = max([p["valor"] for p in pts] + [p["base"] or 0 for p in pts] + [1])
    piso = _piso_y(min([p["valor"] for p in pts] + [p["base"] for p in pts if p["base"] is not None]))
    topo, chao = math.log10(vmax * 1.05 + 1), math.log10(piso + 1)

    def x(d: datetime) -> float:
        return L + (d - t0).total_seconds() / span * (W - L - R)

    def y(valor: float) -> float:
        return T + (topo - math.log10(valor + 1)) / (topo - chao) * (H - T - B)

    partes = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Engajamento por post ao longo do tempo">']
    for ev in serie["eventos"]:
        if ev["tipo"] not in ("degrau", "queda"):
            continue
        dep = ev["antes_depois"]["depois"]
        x0 = x(datetime.fromisoformat(ev["post"]["data"]))
        x1 = max(x(datetime.fromisoformat(dep["ate"] + "T23:59:59+00:00")), x0 + 4)
        partes.append(f'<rect class="faixa {ev["tipo"]}" x="{x0:.1f}" y="{T}" width="{min(x1, W - R) - x0:.1f}" '
                      f'height="{H - T - B}"><title>{_e(TITULO_EVENTO[ev["tipo"]])}</title></rect>')
    for v in _marcas_y(piso, vmax):
        partes.append(f'<line class="grade" x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>'
                      f'<text class="eixo" x="{L - 8}" y="{y(v) + 4:.1f}" text-anchor="end">{_num(v)}</text>')
    for d in _marcas_x(t0, t1):
        partes.append(f'<line class="grade" x1="{x(d):.1f}" x2="{x(d):.1f}" y1="{T}" y2="{H - B}"/>'
                      f'<text class="eixo" x="{x(d):.1f}" y="{H - B + 18}" text-anchor="middle">'
                      f'{MESES[d.month - 1]}{"" if d.month != 1 else " " + str(d.year)[2:]}</text>')
    linha_base = " ".join(f"{x(datetime.fromisoformat(p['data'])):.1f},{y(p['base']):.1f}"
                          for p in pts if p["base"] is not None)
    if linha_base:
        partes.append(f'<polyline class="base" points="{linha_base}"/>')
    for p in pts:
        cx, cy = x(datetime.fromisoformat(p["data"])), y(p["valor"])
        estado, classe_tipo = p["estado"], CLASSE_TIPO.get(p["tipo"], "outro")
        razao = f" · {_num(p['razao'])}× a base" if p["razao"] is not None else ""
        dica = (f"{_data_br(p['data'])} · {NOMES_TIPO.get(p['tipo'], p['tipo'])} · {_num(p['valor'])}{razao}"
                f" · {estado}" + (f"\n{p['primeira_linha']}" if p["primeira_linha"] else ""))
        anel = f'<circle class="anel" cx="{cx:.1f}" cy="{cy:.1f}" r="10"/>' if estado == "pico" else ""
        raio = 6.5 if estado in ("degrau", "queda") else 4.5
        partes.append(f'<a href="{_e(p["url"])}" target="_blank" rel="noopener">{anel}'
                      f'<circle class="ponto" data-c="{classe_tipo} e-{estado}" cx="{cx:.1f}" cy="{cy:.1f}" r="{raio}">'
                      f'<title>{_e(dica)}</title></circle></a>')
    partes.append("</svg>")
    return "".join(partes)


def _tabela_antes_depois(ad: dict) -> str:
    a, d = ad["antes"], ad["depois"]

    def formatos(f: dict) -> str:
        return ", ".join(f"{NOMES_TIPO.get(t, t)} {n}" for t, n in sorted(f.items(), key=lambda x: -x[1]))

    linhas = [
        ("Posts", a["posts"], d["posts"]),
        ("Período", f"{_data_br(a['de'])} – {_data_br(a['ate'])}", f"{_data_br(d['de'])} – {_data_br(d['ate'])}"),
        ("Formatos", formatos(a["formatos"]), formatos(d["formatos"])),
        ("Cadência (posts/semana)", _num(a["cadencia_semana"]), _num(d["cadencia_semana"])),
        ("Intervalo mediano (dias)", _num(a["intervalo_mediano_dias"]), _num(d["intervalo_mediano_dias"])),
        ("Legenda mediana (caracteres)", _num(a["legenda_mediana_chars"]), _num(d["legenda_mediana_chars"])),
        ("Hashtags por post (mediana)", _num(a["hashtags_mediana"]), _num(d["hashtags_mediana"])),
        ("Comentários por curtida", _num(a["comentarios_por_curtida"]), _num(d["comentarios_por_curtida"])),
        ("Com chamada para ação (CTA)", _pct(a["cta_fatia"]), _pct(d["cta_fatia"])),
        ("Sobre o produto", _pct(a["produto_fatia"]), _pct(d["produto_fatia"])),
        ("Com colaboração (@menção)", _pct(a["colab_fatia"]), _pct(d["colab_fatia"])),
    ]
    corpo = "".join(f"<tr><th>{_e(r)}</th><td>{_e(x)}</td><td>{_e(y)}</td></tr>" for r, x, y in linhas)
    return f'<table><thead><tr><th></th><th>Antes</th><th>Depois</th></tr></thead><tbody>{corpo}</tbody></table>'


def _assinatura_html(titulo: str, grupos: dict, rotulo=lambda termo: termo) -> str:
    """Surgiram / sumiram / mantidos, cada termo com a fração de posts antes → depois."""
    blocos = []
    for nome, classe in (("surgiram", "surgiu"), ("sumiram", "sumiu"), ("mantidos", "manteve")):
        if grupos[nome]:
            itens = "".join(f'<li class="{classe}">{_e(rotulo(t["termo"]))} '
                            f'<span class="n">{_pct(t["antes"])} → {_pct(t["depois"])}</span></li>'
                            for t in grupos[nome])
            blocos.append(f'<p class="grupo">{nome.capitalize()}</p><ul class="termos">{itens}</ul>')
    return f"<h4>{_e(titulo)}</h4>" + "".join(blocos) if blocos else ""


def _cartao(ev: dict, serie_nome: str) -> str:
    p = ev["post"]
    tipo = ev["tipo"]
    if tipo == "pico":
        fator = f"{_num(ev['razao'])}× a base"
        sub = f"{_num(p['valor'])} contra linha de base {_num(ev['base_antes'])}"
        if not ev["confirmado"]:
            sub += " · ainda não confirmado: poucos posts depois, pode ser o começo de um degrau"
    else:
        fator = f"{_num(ev['nivel'])}×"
        t = "" if ev["t_welch"] is None else f"t = {_num(ev['t_welch'])}; "
        sub = (f"mediana antes {_num(ev['base_antes'])} → depois {_num(ev['mediana_depois'])} · "
               f"confiança {ev['confianca']} ({t}{ev['n_antes']} posts antes × {ev['n_depois']} depois)")
    corpo = [f'<p class="sub">{_e(sub)}</p>',
             f'<p class="post"><a href="{_e(p["url"])}" target="_blank" rel="noopener">'
             f'{_e(NOMES_TIPO.get(p["tipo"], p["tipo"]))} de {_data_br(p["data"])}</a>'
             f'{" — " + _e(p["primeira_linha"]) if p["primeira_linha"] else ""}</p>']
    if tipo != "pico":
        ad = ev["antes_depois"]
        corpo.append(_tabela_antes_depois(ad))
        if ad["puxaram"]:
            itens = "".join(
                f'<li><a href="{_e(x["url"])}" target="_blank" rel="noopener">{_data_br(x["data"])}</a> '
                f'<span class="n">{_e(NOMES_TIPO.get(x["tipo"], x["tipo"]))} · {_num(x["valor"])} · '
                f'{_num(x["razao"])}× · {_num(x["comentarios_por_curtida"])} coment./curtida</span> '
                f'{_e(x["primeira_linha"])}</li>' for x in ad["puxaram"])
            titulo = "Posts acima da base antiga" if tipo == "degrau" else "Posts que ainda ficaram acima da base"
            corpo.append(f"<h4>{titulo}</h4><ul class='puxaram'>{itens}</ul>")
        corpo.append(_assinatura_html("Formatos", ad["tipos"], lambda t: NOMES_TIPO.get(t, t)))
        corpo.append(_assinatura_html("Palavras da legenda", ad["palavras"]))
        corpo.append(_assinatura_html("Hashtags", ad["hashtags"], lambda t: "#" + t))
    return (f'<article class="cartao {tipo}"><header><span class="selo">{_e(TITULO_EVENTO[tipo])}</span>'
            f'<h3>{_data_br(p["data"])} · {_e(fator)}</h3><span class="serie">{_e(serie_nome)}</span></header>'
            + "".join(corpo) + "</article>")


CSS = """
:root{--fundo:#f6f3ee;--papel:#fffdf9;--tinta:#1f1b16;--suave:#6b6259;--linha:#e2dbd1;
--reel:#b4532a;--carrossel:#2f6f8f;--foto:#7a8c3a;--outro:#8a7f74;--degrau:#2e8b57;--queda:#c0392b;
--pico:#d4a017;--base:#1f1b16;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--fundo:#16130f;--papel:#201c17;
--tinta:#f1ebe2;--suave:#a89d90;--linha:#3a332b;--reel:#e07a4f;--carrossel:#5fa8cc;--foto:#a9bd5c;
--outro:#a89d90;--degrau:#4cc28a;--queda:#ef6b5c;--pico:#f0c24b;--base:#f1ebe2;color-scheme:dark}}
:root[data-theme="dark"]{--fundo:#16130f;--papel:#201c17;--tinta:#f1ebe2;--suave:#a89d90;--linha:#3a332b;
--reel:#e07a4f;--carrossel:#5fa8cc;--foto:#a9bd5c;--outro:#a89d90;--degrau:#4cc28a;--queda:#ef6b5c;
--pico:#f0c24b;--base:#f1ebe2;color-scheme:dark}
*{box-sizing:border-box}
body{overflow-wrap:anywhere;margin:0;background:var(--fundo);color:var(--tinta);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1080px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:19px;margin:32px 0 8px}h3{font-size:17px;margin:2px 0}
h4{font-size:13px;text-transform:uppercase;letter-spacing:.04em;color:var(--suave);margin:16px 0 6px}
.meta{color:var(--suave);margin:0}.avisos{background:var(--papel);border-left:3px solid var(--pico);padding:8px 12px;margin:16px 0}
.avisos p{margin:4px 0}
.grafico{background:var(--papel);border:1px solid var(--linha);border-radius:10px;padding:8px}
svg{width:100%;height:auto;display:block}
.grade{stroke:var(--linha);stroke-width:1}.eixo{fill:var(--suave);font-size:12px}
.base{fill:none;stroke:var(--base);stroke-width:1.5;stroke-dasharray:5 4;opacity:.55}
.faixa.degrau{fill:var(--degrau);opacity:.14}.faixa.queda{fill:var(--queda);opacity:.14}
circle[data-c~="reel"]{fill:var(--reel)}circle[data-c~="carrossel"]{fill:var(--carrossel)}
circle[data-c~="foto"]{fill:var(--foto)}circle[data-c~="outro"]{fill:var(--outro)}
circle[data-c~="e-imaturo"]{fill:none;stroke:var(--suave);stroke-width:1.5}
circle[data-c~="e-degrau"]{stroke:var(--degrau);stroke-width:3}circle[data-c~="e-queda"]{stroke:var(--queda);stroke-width:3}
.anel{fill:none;stroke:var(--pico);stroke-width:2.5}
a:hover circle.ponto{stroke:var(--tinta);stroke-width:2}
.legenda{display:flex;flex-wrap:wrap;gap:6px 16px;color:var(--suave);font-size:13px;margin:8px 4px 0}
.legenda i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:5px;vertical-align:-1px}
.legenda .q{border-radius:2px}
.cartoes{display:grid;gap:14px}
.cartao{background:var(--papel);border:1px solid var(--linha);border-left:4px solid var(--suave);border-radius:10px;padding:14px 16px}
.cartao.degrau{border-left-color:var(--degrau)}.cartao.queda{border-left-color:var(--queda)}.cartao.pico{border-left-color:var(--pico)}
.cartao header{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px}
.selo{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:var(--suave)}
.serie{margin-left:auto;font-size:12px;color:var(--suave)}
.sub{color:var(--suave);margin:4px 0}.post{margin:6px 0}
a{color:inherit;text-decoration-color:var(--suave)}
table{border-collapse:collapse;width:100%;margin-top:10px;font-size:14px}
th,td{text-align:left;padding:5px 8px;border-bottom:1px solid var(--linha);vertical-align:top}
thead th{color:var(--suave);font-weight:600;font-size:12px;text-transform:uppercase}
tbody th{font-weight:500;color:var(--suave);width:38%}
ul{margin:0;padding-left:18px}.puxaram li{margin:3px 0}.n{color:var(--suave);font-size:13px}
.termos{display:flex;flex-wrap:wrap;gap:6px;padding:0;list-style:none}
.termos li{background:var(--fundo);border:1px solid var(--linha);border-radius:99px;padding:1px 10px;font-size:13px}
.termos li.surgiu{border-color:var(--degrau)}.termos li.sumiu{border-color:var(--queda);opacity:.8}
.grupo{font-size:12px;color:var(--suave);margin:8px 0 4px}
.consistencia{background:var(--papel);border:1px solid var(--linha);border-radius:10px;padding:10px 14px;margin:16px 0}
.consistencia strong{font-size:16px}
.vazio{color:var(--suave)}
@media (max-width:560px){h1{font-size:21px}tbody th{width:auto}.serie{margin-left:0}
.rolagem{overflow-x:auto}.rolagem svg{min-width:680px}}
"""


def render_html(rel: dict) -> str:
    c = rel["contagens"]
    janela = "todo o histórico" if rel["janela_dias"] <= 0 else f"últimos {rel['janela_dias']} dias"
    seg = rel["seguidores_coleta"]
    meta = (f"{janela} até {_data_br(rel['hoje'])} · {c['maduros']} posts avaliados · {c['imaturos']} imaturos "
            f"(menos de {rel['maturidade_dias']} dias) · {c['duplicados']} registros repetidos descartados")
    if seg:
        meta += f" · {_num(seg['valor'])} seguidores no dia da coleta"
    p = rel["parametros"]
    regra = (f"Linha de base = mediana dos {p['k']} posts anteriores. Degrau = mediana dos {p['m']} posts seguintes "
             f"≥ {_num(p['degrau'])}× a base, com {p['sustentacao']:.0%} deles acima. Queda = ≤ {_num(p['queda'])}×. "
             f"Pico isolado = post ≥ {_num(p['pico'])}× a base, com o perfil voltando ao patamar depois.")
    avisos = "".join(f"<p>{_e(a)}</p>" for a in rel["avisos"])
    cons = rel["consistencia"]
    consistencia = "" if not cons else (
        f"<div class='consistencia'><h4 style='margin-top:0'>Consistência do perfil</h4>"
        f"<strong>{_e(cons['leitura'].capitalize())}</strong> "
        f"<span class='meta'>· mediana {_num(cons['mediana'])} · CV {_num(cons['cv'])} · máximo "
        f"{_num(cons['max_sobre_mediana'])}× a mediana · {_pct(cons['faixa_central'])} dos posts entre 0,5× e "
        f"2× a mediana</span><p class='meta'>Estável = CV abaixo de {_num(CV_ESTAVEL)} e máximo abaixo de "
        f"{_num(MAX_ESTAVEL)}× a mediana: o perfil cresce por constância, não por estouro.</p></div>")
    secoes = []
    for nome, serie in rel["series"].items():
        rotulo = "Engajamento (curtidas + comentários)" if nome == "engajamento" else "Views"
        cartoes = "".join(_cartao(ev, rotulo) for ev in serie["eventos"]) or \
            '<p class="vazio">Nenhuma virada nesta série com os limiares atuais.</p>'
        secoes.append(
            f"<section><h2>{_e(rotulo)}</h2><div class='grafico'><div class='rolagem'>{_svg(serie)}</div>"
            "<div class='legenda'><span><i style='background:var(--reel)'></i>Reel</span>"
            "<span><i style='background:var(--carrossel)'></i>Carrossel</span>"
            "<span><i style='background:var(--foto)'></i>Foto</span>"
            "<span><i style='border:1.5px solid var(--suave)'></i>Imaturo</span>"
            "<span><i style='border:2.5px solid var(--pico)'></i>Pico isolado</span>"
            "<span><i class='q' style='background:var(--degrau);opacity:.35'></i>Degrau</span>"
            "<span><i class='q' style='background:var(--queda);opacity:.35'></i>Queda</span>"
            "<span>– – linha de base</span></div></div>"
            f"<h2>Viradas, em ordem cronológica</h2><div class='cartoes'>{cartoes}</div></section>")
    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>Virada {_e(rel['perfil'])}</title><style>{CSS}</style></head><body><main>"
        f"<h1>Detector de virada · {_e(rel['perfil'])}</h1><p class='meta'>{_e(meta)}</p>"
        f"<p class='meta'>{_e(regra)} Clique num ponto para abrir o post.</p>"
        + (f"<div class='avisos'>{avisos}</div>" if avisos else "")
        + consistencia
        + "".join(secoes)
        + f"<p class='meta' style='margin-top:32px'>Fonte: {_e(rel['fonte'])} · gerado em {_e(rel['gerado_em'])}</p>"
        "</main></body></html>"
    )


# --- CLI -----------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Detector de virada: degrau, queda e pico na série de um perfil.")
    ap.add_argument("perfil", help="handle, com ou sem @ (cafecanastra lê proprios.jsonl)")
    ap.add_argument("--dias", type=int, default=365, help="janela em dias até --hoje; 0 = histórico inteiro")
    ap.add_argument("--maturidade", type=int, default=3, help="posts mais novos que isso ficam fora da detecção")
    for nome, padrao in PADROES.items():
        ap.add_argument(f"--{nome}", type=type(padrao), default=padrao)
    ap.add_argument("--arquivo", type=Path, help="lê este .jsonl em vez do do fluxo 1 (fallback manual)")
    ap.add_argument("--metricas", type=Path, default=RAIZ_METRICAS, help="raiz da coleta do fluxo 1")
    ap.add_argument("--saida", type=Path, help="pasta de saída (padrão instagram/viradas/<handle>/)")
    ap.add_argument("--hoje", type=date.fromisoformat, default=date.today(), help="AAAA-MM-DD")
    a = ap.parse_args(argv)

    handle = normalizar_handle(a.perfil)
    if a.arquivo is not None:
        if not a.arquivo.exists():
            print(f"ERRO: {a.arquivo} não existe.", file=sys.stderr)
            return 2
        fonte = a.arquivo
    else:
        try:
            fonte = localizar(handle, a.metricas)
        except PerfilAusente as erro:
            print(f"ERRO: {erro}", file=sys.stderr)
            return 2

    posts, contagem = ler_jsonl(fonte)
    params = {nome: getattr(a, nome) for nome in PADROES}
    rel = analisar(handle, fonte, posts, contagem, params, a.hoje, a.dias, a.maturidade)
    caminho_json, caminho_html = gravar(rel, a.saida or RAIZ_SAIDA / handle)
    print(resumo(rel))
    print(f"JSON: {caminho_json}\nHTML: {caminho_html}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
