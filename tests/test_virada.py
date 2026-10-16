"""Detector de virada (fluxo 4): degrau sustentado, queda de patamar e pico isolado.

Spec em docs/superpowers/specs/2026-10-15-detector-virada-design.md. As séries são geradas
aqui, no formato do contrato do fluxo 1 (instagram/metricas/), para que cada caso se leia no
próprio teste. Nenhum teste toca rede.

`scripts/` nao e pacote importavel, entao o modulo e carregado pelo caminho.
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_MODULO = RAIZ / "scripts" / "virada.py"


def _carrega_modulo():
    spec = importlib.util.spec_from_file_location("virada", CAMINHO_MODULO)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["virada"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


v = _carrega_modulo()

INICIO = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
HOJE = date(2026, 12, 31)


def _linhas(valores, passo=3, tipo="REEL", legendas=None, inicio=INICIO, views=None, prefixo="p"):
    linhas = []
    for n, valor in enumerate(valores):
        data = inicio + timedelta(days=passo * n)
        linhas.append({
            "id": f"{prefixo}{n:03d}",
            "url": f"https://www.instagram.com/p/{prefixo.upper()}{n:03d}/",
            "data_publicacao": data.strftime("%Y-%m-%dT%H:%M:%S+0000"),
            "tipo": tipo,
            "legenda": legendas[n] if legendas else f"post {n}",
            "curtidas": valor - valor // 10,
            "comentarios": valor // 10,
            "views": views[n] if views else None,
            "seguidores": 10_000,
            "coletado_em": "2026-10-15T10:00:00Z",
        })
    return linhas


def _grava(caminho: Path, linhas) -> Path:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("\n".join(l if isinstance(l, str) else json.dumps(l, ensure_ascii=False)
                                 for l in linhas) + "\n", encoding="utf-8")
    return caminho


def _eventos(det):
    return [(e["tipo"], e["i"]) for e in det["eventos"]]


def _analisa(tmp_path, linhas, dias=0, maturidade=3, hoje=HOJE):
    arq = _grava(tmp_path / "serie.jsonl", linhas)
    posts, contagem = v.ler_jsonl(arq)
    return v.analisar("teste", arq, posts, contagem, dict(v.PADROES), hoje, dias, maturidade)


# --- leitura do contrato -------------------------------------------------------------------

def test_dedup_fica_coleta_mais_recente(tmp_path):
    velho = _linhas([10])[0] | {"coletado_em": "2026-10-01T10:00:00Z"}
    novo = _linhas([99])[0] | {"coletado_em": "2026-10-15T10:00:00Z"}
    for ordem in ([velho, novo], [novo, velho]):
        posts, contagem = v.ler_jsonl(_grava(tmp_path / "s.jsonl", ordem))
        assert len(posts) == 1
        assert posts[0].engajamento == 99
        assert contagem["duplicados"] == 1


def test_linha_invalida_contada(tmp_path):
    bons = _linhas([10, 20])
    sem_id = {k: x for k, x in _linhas([30])[0].items() if k != "id"}
    data_ruim = _linhas([40], prefixo="q")[0] | {"data_publicacao": "ontem"}
    posts, contagem = v.ler_jsonl(_grava(tmp_path / "s.jsonl", [*bons, "não é json", sem_id, data_ruim]))
    assert [p.engajamento for p in posts] == [10, 20]
    assert contagem["invalidas"] == 3
    assert contagem["linhas"] == 5


def test_datas_iso_variantes():
    esperado = datetime(2026, 9, 25, 14, 3, tzinfo=timezone.utc)
    for texto in ("2026-09-25T14:03:00Z", "2026-09-25T14:03:00+0000", "2026-09-25T14:03:00+00:00"):
        assert v.parse_data(texto) == esperado
    assert v.parse_data("ontem") is None
    assert v.parse_data(None) is None


def test_localizar_proprio_e_concorrente(tmp_path):
    proprio = _grava(tmp_path / "proprios.jsonl", _linhas([1]))
    concorrente = _grava(tmp_path / "concorrentes" / "orfeucafes.jsonl", _linhas([1]))
    assert v.localizar("@CafeCanastra", tmp_path) == proprio
    assert v.localizar("orfeucafes", tmp_path) == concorrente


def test_proprios_e_arroba_no_nome(tmp_path):
    # proprios.jsonl grava `seguidores_conta`; o fluxo 3 também aceita `@<handle>.jsonl`
    linha = {k: x for k, x in _linhas([10])[0].items() if k != "seguidores"} | {"seguidores_conta": 10_300}
    posts, _ = v.ler_jsonl(_grava(tmp_path / "proprios.jsonl", [linha]))
    assert posts[0].seguidores == 10_300
    arroba = _grava(tmp_path / "concorrentes" / "@zanellicoffee.jsonl", _linhas([1]))
    assert v.localizar("zanellicoffee", tmp_path) == arroba


def test_perfil_ausente_mensagens(tmp_path):
    def motivo(raiz, handle):
        try:
            v.localizar(handle, raiz)
        except v.PerfilAusente as erro:
            return str(erro)
        raise AssertionError("devia faltar")

    assert "fluxo 1" in motivo(tmp_path / "nao-existe", "fulano")
    (tmp_path / "watchlist.json").write_text(json.dumps({"perfis": [{"handle": "@fulano"}]}), encoding="utf-8")
    assert "está na watchlist" in motivo(tmp_path, "fulano")
    assert "não está na watchlist" in motivo(tmp_path, "ciclano")


# --- detecção ------------------------------------------------------------------------------

def test_degrau_limpo():
    det = v.detectar([50] * 20 + [200] * 20, **v.PADROES)
    assert _eventos(det) == [("degrau", 20)]
    assert det["estados"][21:28] == ["puxador"] * 7


def test_queda():
    det = v.detectar([200] * 20 + [50] * 20, **v.PADROES)
    assert _eventos(det) == [("queda", 20)]


def test_escada_da_dois_degraus():
    det = v.detectar([50] * 20 + [200] * 20 + [800] * 20, **v.PADROES)
    assert _eventos(det) == [("degrau", 20), ("degrau", 40)]


def test_pico_isolado():
    det = v.detectar([50] * 15 + [400] + [50] * 15, **v.PADROES)
    assert _eventos(det) == [("pico", 15)]
    assert det["eventos"][0]["confirmado"] is True
    assert det["eventos"][0]["razao"] == 8.0


def test_pico_recente_nao_confirmado():
    det = v.detectar([50] * 15 + [400], **v.PADROES)
    assert _eventos(det) == [("pico", 15)]
    assert det["eventos"][0]["confirmado"] is False


def test_salto_que_nao_volta_nem_sustenta_nao_e_pico():
    # 8× e depois um patamar 1,6×: o perfil não voltou (não é pico isolado) e não subiu o
    # bastante para degrau (1,6 < 1,8). Fica fora da lista de eventos, de propósito: o post
    # aparece no gráfico com a razão, e baixar --degrau é a forma de olhar para ele.
    det = v.detectar([50] * 15 + [400] + [80] * 15, **v.PADROES)
    assert det["eventos"] == []
    assert det["estados"][15] == "normal"
    assert det["razao"][15] == 8.0


def test_ruido_sem_evento():
    rng = random.Random(7)
    det = v.detectar([round(50 * rng.uniform(0.7, 1.3)) for _ in range(60)], **v.PADROES)
    assert det["eventos"] == []


def test_sem_base_nos_primeiros():
    det = v.detectar([50] * 20, **v.PADROES)
    assert det["estados"][:6] == ["sem_base"] * 6
    assert det["estados"][6] == "normal"


# --- o que mudou ao redor ------------------------------------------------------------------

def test_antes_depois(tmp_path):
    antes = _linhas([50] * 20, passo=7, tipo="IMAGE", legendas=["foto do dia no sítio"] * 20)
    inicio_depois = INICIO + timedelta(days=7 * 20)
    gancho = "Você sabia? torra clara de verdade #torraclara"
    depois = _linhas([200] * 20, passo=2, tipo="REEL", legendas=[gancho] * 20, inicio=inicio_depois, prefixo="r")
    posts, _ = v.ler_jsonl(_grava(tmp_path / "s.jsonl", antes + depois))
    valores = [p.engajamento for p in posts]
    ad = v.antes_depois(posts, valores, 20, k=12, m=8)
    assert ad["antes"]["formatos"] == {"IMAGE": 12}
    assert ad["depois"]["formatos"] == {"REEL": 8}
    assert ad["antes"]["cadencia_semana"] == 1.0
    assert ad["depois"]["cadencia_semana"] == 3.5
    novas = [x["termo"] for x in ad["palavras_novas"]]
    assert {"torra", "clara", "sabia"} <= set(novas)
    assert "você" not in novas  # stopword
    assert [x["termo"] for x in ad["hashtags_novas"]] == ["torraclara"]
    assert len(ad["puxaram"]) == 8
    assert ad["puxaram"][0]["primeira_linha"] == gancho


# --- relatório -----------------------------------------------------------------------------

def test_imaturos_fora_da_deteccao(tmp_path):
    linhas = _linhas([50] * 15 + [400])
    hoje = v.parse_data(linhas[-1]["data_publicacao"]).date() + timedelta(days=1)
    rel = _analisa(tmp_path, linhas, hoje=hoje)
    serie = rel["series"]["engajamento"]
    assert serie["posts"][-1]["estado"] == "imaturo"
    assert rel["contagens"]["imaturos"] == 1
    assert serie["eventos"] == []


def test_janela_dias(tmp_path):
    linhas = _linhas([50] * 40)  # um a cada 3 dias, de 01/01 a 28/04
    hoje = date(2026, 5, 1)
    rel = _analisa(tmp_path, linhas, dias=30, hoje=hoje)
    datas = [p["data"][:10] for p in rel["series"]["engajamento"]["posts"]]
    assert min(datas) >= "2026-04-01"
    assert rel["contagens"]["fora_da_janela"] == 40 - len(datas)


def test_serie_curta_avisa(tmp_path):
    rel = _analisa(tmp_path, _linhas([50] * 8))
    assert any("série curta" in a for a in rel["avisos"])
    assert rel["series"]["engajamento"]["eventos"] == []


def test_views_so_com_maioria(tmp_path):
    metade = [1000 if n % 2 else None for n in range(30)]
    rel = _analisa(tmp_path, _linhas([50] * 30, views=metade))
    assert set(rel["series"]) == {"engajamento"}
    assert any("views" in a for a in rel["avisos"])
    rel = _analisa(tmp_path, _linhas([50] * 30, views=[1000] * 30))
    assert set(rel["series"]) == {"engajamento", "views"}


def test_main_grava_json_e_html(tmp_path, capsys):
    metricas = tmp_path / "metricas"
    _grava(metricas / "concorrentes" / "orfeucafes.jsonl", _linhas([50] * 20 + [200] * 20))
    saida = tmp_path / "out"
    codigo = v.main(["@orfeucafes", "--metricas", str(metricas), "--saida", str(saida),
                     "--hoje", "2026-06-01", "--dias", "0"])
    assert codigo == 0
    rel = json.loads((saida / "2026-06-01.json").read_text(encoding="utf-8"))
    evento = rel["series"]["engajamento"]["eventos"][0]
    assert evento["tipo"] == "degrau"
    assert evento["post"]["url"] == "https://www.instagram.com/p/P020/"
    pagina = (saida / "2026-06-01.html").read_text(encoding="utf-8")
    assert "<svg" in pagina
    assert "https://www.instagram.com/p/P020/" in pagina
    assert "Degrau sustentado" in pagina
    assert "degrau" in capsys.readouterr().out


def test_main_perfil_ausente_sai_2(tmp_path, capsys):
    codigo = v.main(["fulano", "--metricas", str(tmp_path / "nada")])
    assert codigo == 2
    assert "fluxo 1" in capsys.readouterr().err


# --- HTML ----------------------------------------------------------------------------------

def test_html_autocontido(tmp_path):
    valores = [50] * 15 + [400] + [50] * 14 + [200] * 20
    legendas = ["<b>negrito</b> & cia"] * len(valores)
    rel = _analisa(tmp_path, _linhas(valores, legendas=legendas))
    eventos = rel["series"]["engajamento"]["eventos"]
    assert [e["tipo"] for e in eventos] == ["pico", "degrau"]
    pagina = v.render_html(rel)
    assert "<script src" not in pagina and "<link" not in pagina
    assert "prefers-color-scheme" in pagina
    assert pagina.count('class="ponto"') == len(valores)
    assert pagina.count('class="faixa degrau"') == 1
    assert pagina.count('class="anel"') == 1
    assert "<b>negrito</b>" not in pagina
    assert "&lt;b&gt;negrito&lt;/b&gt; &amp; cia" in pagina
