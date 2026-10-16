"""Máquina de ganchos (scripts/ganchos.py). `scripts/` não é pacote: carrega pelo caminho."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent


def _carrega():
    spec = importlib.util.spec_from_file_location("ganchos", RAIZ / "scripts" / "ganchos.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod          # dataclass com `from __future__ import annotations` exige
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
    assert g.texto_citado("**nada**. O arquivo tem áudio mudo.") == ""
    assert g.texto_citado("só o rótulo da garrafa.") == ""          # descrição, não texto
    assert g.texto_citado("Voz em off: 'Arthur, please don't do that. You know why.'") == \
        "Arthur, please don't do that. You know why."


def test_extrair_corpus_real():
    corpus = g.extrair()
    assert len(corpus) >= 120                      # 130 fichas, 1 vídeo em duas frentes
    assert len({x["id"] for x in corpus}) == len(corpus)
    com_ve = sum(1 for x in corpus if x["ve"])
    assert com_ve / len(corpus) >= 0.95
    x = next(x for x in corpus if x["id"] == "DVMF38UgD0M")
    assert x["escrito"].startswith("🔴 Não compre")
    assert x["views"] is None and x["curtidas"] and x["idioma"] == "pt"   # 8 fichas sem views lidas
    y = next(x for x in corpus if x["id"] == "DZOC2OdJSgo")
    assert y["views"] == 21_120_000 and "café" in y["escrito"].lower()


def test_ler_vicios_real():
    v = g.ler_vicios()
    ids = {x["id"] for x in v}
    assert {"V1", "V3", "V4"} <= ids
    assert all(x["proibe"] in ("sim", "medir") for x in v)
    assert next(x for x in v if x["id"] == "V1")["regex"].search("Não é só café, é ritual")


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


def test_padroes_agrupa_e_ordena():
    corpus = [
        {"id": "a", "idioma": "pt", "views": 100, "escrito": "A", "dito": "", "perfil": "@x", "frente": "brasil", "ve": ""},
        {"id": "b", "idioma": "pt", "views": 300, "escrito": "B", "dito": "", "perfil": "@y", "frente": "brasil", "ve": ""},
        {"id": "c", "idioma": "en", "views": 50, "escrito": "C", "dito": "", "perfil": "@z", "frente": "motion-marcas", "ve": ""},
    ]
    mapa = {"padroes": {"p1": {"nome": "Um", "forma": "f", "descricao": "d"},
                        "p2": {"nome": "Dois", "forma": "f", "descricao": "d"}},
            "mapa": {"a": "p1", "b": "p1", "c": "p2"}}
    t = g.tabela_padroes(corpus, mapa)
    assert [p["slug"] for p in t] == ["p1", "p2"]           # ordena por n
    assert t[0]["n"] == 2 and t[0]["mediana_views"] == 200
    assert t[0]["n_cafe"] == 2 and t[1]["n_cafe"] == 0      # motion não é café
    assert t[0]["exemplos"][0]["id"] == "b"                 # exemplo de maior view primeiro


def test_padroes_mapa_cobre_o_corpus_real():
    corpus = [json.loads(l) for l in (RAIZ / "instagram/ganchos/corpus.jsonl").read_text(encoding="utf-8").splitlines()]
    mapa = json.loads((RAIZ / "instagram/ganchos/padroes-mapa.json").read_text(encoding="utf-8"))
    faltam = [x["id"] for x in corpus if x["id"] not in mapa["mapa"]]
    assert not faltam
    assert set(mapa["mapa"].values()) <= set(mapa["padroes"])
    assert 6 <= len(mapa["padroes"]) <= 10
    assert all(n >= 5 for n in __import__("collections").Counter(mapa["mapa"].values()).values())


# --- rubrica e regras mecânicas ---------------------------------------------

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


def test_caracteres_da_capa_batem_com_o_motor_de_carrossel():
    from instagram.carrossel.molde import ORCAMENTO
    assert g.CARACTERES["capa"] == (ORCAMENTO["manchete"], ORCAMENTO["sub"])


G = g.Gancho


def test_p1_numero_sem_fonte():
    assert not g.MECANICAS["P1"](G("capa", manchete="O microlote custa 4 reais a mais"))[0]
    assert not g.MECANICAS["P1"](G("capa", manchete="O microlote custa quatro reais a mais"))[0]
    assert g.MECANICAS["P1"](G("capa", manchete="O microlote custa 4 reais a mais",
                               fonte="tabela de 11/09/2026"))[0]
    assert g.MECANICAS["P1"](G("capa", manchete="Tem casca no seu café?"))[0]


def test_p2_e_p3():
    assert not g.MECANICAS["P2"](G("reel", fala="O cheiro da torra age no seu cérebro"))[0]
    assert not g.MECANICAS["P3"](G("capa", manchete="O café mais premiado de Minas"))[0]
    assert g.MECANICAS["P3"](G("capa", manchete="Tem casca no seu café?"))[0]


def test_m1_faixa_e_caracteres():
    a, b = g.FAIXAS["capa"]
    assert g.MECANICAS["M1"](G("capa", manchete=" ".join(["pal"] * a)))[0]
    assert not g.MECANICAS["M1"](G("capa", manchete=" ".join(["pal"] * (b + 1))))[0]
    assert not g.MECANICAS["M1"](G("capa", manchete="Paralelepípedos descomunais inexplicavelmente desalinhados ontem"))[0]  # > 60 car.
    assert not g.MECANICAS["M1"](G("capa", manchete="Tem casca no seu café?", apoio="x" * 121))[0]
    a, b = g.FAIXAS["reel"]
    assert g.MECANICAS["M1"](G("reel", fala="Café na geladeira não conserva. Ele absorve o cheiro."))[0]


def test_m2_repeticao():
    assert not g.MECANICAS["M2"](G("reel", fala="Café na geladeira não conserva.",
                                   tela="Café na geladeira não conserva"))[0]
    assert g.MECANICAS["M2"](G("reel", fala="Café na geladeira não conserva.",
                               tela="Onde guardar o pacote aberto"))[0]
    assert g.MECANICAS["M2"](G("capa", manchete="Tem casca no seu café?"))[0]   # sem 2ª camada


def test_m3_m4():
    assert not g.MECANICAS["M3"](G("capa", manchete="Não é só café, é uma experiência"))[0]
    assert not g.MECANICAS["M3"](G("capa", manchete="Descubra a jornada do grão"))[0]
    assert g.MECANICAS["M3"](G("reel", fala="Não é CHAFÉ!"))[0]          # negação não é V1; fala aceita "!"
    assert not g.MECANICAS["M3"](G("capa", manchete="Não é CHAFÉ!"))[0]  # na tela não (10-voz §7)


def test_m3_voz_da_marca():
    assert not g.MECANICAS["M3"](G("capa", manchete="Um café gourmet de verdade"))[0]          # V10
    assert not g.MECANICAS["M3"](G("reel", fala="O segredo do nosso café"))[0]                 # V8
    assert not g.MECANICAS["M3"](G("reel", fala="O que a gente viu na lavoura", tela="A lavoura ☕"))[0]  # V14 na tela
    assert g.MECANICAS["M3"](G("capa", manchete="Um café perfeito para a manhã"))[0]         # mantida pelo cliente
    assert not g.MECANICAS["M3"](G("capa", manchete="Olha o que aconteceu…"))[0]               # V15
    assert g.MECANICAS["M3"](G("capa", manchete="Tem casca no seu café?"))[0]
    assert not g.MECANICAS["M4"](G("reel", fala="Bom dia! Hoje eu vou falar da colheita"))[0]
    assert g.MECANICAS["M4"](G("reel", fala="Hoje eu vou tirar o boia desse café, galera."))[0]


def test_avaliar_portao_pendente_e_completo():
    regras = g.ler_rubrica()
    r = g.avaliar(G("capa", manchete="O café mais premiado de Minas"), regras, {})
    assert r["nota"] == 0 and "P3" in r["portoes_falhos"]
    r = g.avaliar(G("capa", manchete="Tem casca no seu café?"), regras, {})
    assert r["nota"] is None and "J1" in r["pendentes"] and "R1" not in r["resultados"]
    todos = {x.id: True for x in g.regras_do_formato(regras, "capa") if x.quem == "claude"}
    r = g.avaliar(G("capa", manchete="Tem casca no seu café?", apoio="A gente explica o que é"), regras, todos)
    assert r["nota"] == r["subtotal"] == 100
    todos["P4"] = False
    assert g.avaliar(G("capa", manchete="Tem casca no seu café?"), regras, todos)["nota"] == 0


def test_registrar_anexa(tmp_path):
    destino = tmp_path / "avaliacoes.jsonl"
    r = g.avaliar(G("capa", manchete="Tem casca no seu café?"), g.ler_rubrica(), {})
    g.registrar(r, tema="casca", destino=destino, escolhido=True, post="DefH_1ClN30")
    g.registrar(r, tema="casca", destino=destino)
    linhas = [json.loads(l) for l in destino.read_text(encoding="utf-8").splitlines()]
    assert len(linhas) == 2 and linhas[0]["escolhido"] is True and linhas[0]["post"] == "DefH_1ClN30"
    assert linhas[0]["gancho"]["manchete"] == "Tem casca no seu café?"


def test_cli_checar(capsys):
    assert g.main(["checar", "--formato", "capa", "--manchete", "Tem casca no seu café?"]) == 0
    saida = capsys.readouterr().out
    assert "faltam julgar" in saida and "M3" in saida


# --- recalibração -------------------------------------------------------------

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
    assert g.metrica({"alcance": 100, "tempo_medio_assistido_s": 4.2}, "reel") == pytest.approx(4.2)


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


def test_recalibrar_sem_arquivo_avisa_e_nao_falha(tmp_path, capsys):
    assert g.main(["recalibrar", "--proprios", str(tmp_path / "nao-existe.jsonl")]) == 0
    assert "aviso" in capsys.readouterr().out


def test_cruzar_pelo_shortcode_mesmo_sem_gancho_no_post():
    aval = {"gancho": {"formato": "capa", "manchete": "Tem casca no seu café?"}, "resultados": {},
            "escolhido": True, "post": "DefH_1ClN30"}
    post = {"id": "1789", "url": "https://www.instagram.com/p/DefH_1ClN30/", "gancho": None,
            "coletado_em": "2026-10-16T05:00:00Z"}
    assert g.cruzar([post], [aval])[0]["avaliacao"] is aval
    post2 = {"id": "1790", "url": "https://www.instagram.com/p/OUTRO/", "gancho": "tem casca no seu cafe",
             "coletado_em": "2026-10-16T05:00:00Z"}
    assert g.cruzar([post2], [aval])[0]["avaliacao"] is aval     # e pelo texto normalizado


# --- v2: melhorias tiradas do "Hook Machine" (Kallaway), aprovadas em 15/10/2026 ---------

def _julg_capa(**muda):
    regras = g.ler_rubrica()
    d = {x.id: True for x in g.regras_do_formato(regras, "capa") if x.quem == "claude" and x.tipo != "bonus"}
    d.update(muda)
    return regras, d


def test_j7_existe_e_bonus_fica_fora_da_soma():
    regras = g.ler_rubrica()
    ids = {r.id: r for r in regras}
    assert ids["J7"].tipo == "pontuada" and ids["J7"].quem == "claude"
    assert ids["B1"].tipo == "bonus" and ids["B1"].peso > 0
    assert g.validar_rubrica(regras) == []


def test_bonus_premia_sem_penalizar_e_nao_passa_de_100():
    regras, j = _julg_capa(J3=False)
    gc = G("capa", manchete="Tem casca no seu café?", apoio="A gente explica o que é")
    sem = g.avaliar(gc, regras, j)
    assert sem["nota"] == 90 and "B1" not in sem["pendentes"]          # ausência do bônus não pende
    com = g.avaliar(gc, regras, {**j, "B1": True})
    assert com["nota"] == 90 + ids_peso(regras, "B1")
    tudo = g.avaliar(gc, regras, {**j, "J3": True, "B1": True})
    assert tudo["nota"] == 100


def ids_peso(regras, rid):
    return next(r.peso for r in regras if r.id == rid)


def test_nota_minima_avisa_no_checar(capsys):
    assert g.main(["checar", "--formato", "capa", "--manchete", "O café da tarde é bom.",
                   "--julgamento", "P4=1,J1=0,J2=0,J3=0,J4=0,J5=1,J6=0,J7=1,C1=0,C2=0"]) == 0
    assert f"abaixo da nota mínima ({g.NOTA_MINIMA})" in capsys.readouterr().out


def test_m3_jargao_a_frio_e_sinal_amarelo_nao_falha():
    ok, det = g.MECANICAS["M3"](G("capa", manchete="Café de via úmida tem outro gosto?"))
    assert ok and "V16" in det and "J7" in det


def test_suspeitos_de_impulsionamento():
    corpus = [{"id": str(i), "views": 1000, "curtidas": 40, "organico": "sim"} for i in range(9)]
    corpus.append({"id": "baixo", "views": 1000, "curtidas": 5, "organico": "sim"})       # 0,5% contra mediana 4%
    corpus.append({"id": "pago", "views": 1000, "curtidas": 40, "organico": "provavel-pago"})
    corpus.append({"id": "sem-views", "views": None, "curtidas": 40, "organico": "sim"})
    assert g.suspeitos(corpus) == {"baixo", "pago"}


def test_padroes_contam_perfis_e_sinalizam_suspeitos():
    base = {"idioma": "pt", "escrito": "x", "dito": "", "frente": "brasil", "ve": "", "organico": "sim"}
    corpus = [{**base, "id": "a", "perfil": "@x", "views": 100, "curtidas": 4},
              {**base, "id": "b", "perfil": "@x", "views": 300, "curtidas": 12},
              {**base, "id": "c", "perfil": "@y", "views": 900, "curtidas": 1}]          # suspeito
    mapa = {"padroes": {"p1": {"nome": "Um", "forma": "f", "descricao": "d"}}, "mapa": {"a": "p1", "b": "p1", "c": "p1"}}
    p = g.tabela_padroes(corpus, mapa, suspeitos={"c"})[0]
    assert p["n_perfis"] == 2 and p["perfil_dominante"] == "@x" and p["fatia_dominante"] == pytest.approx(2 / 3)
    assert p["n_suspeitos"] == 1
    assert p["mediana_views"] == 300 and p["mediana_views_sem_suspeitos"] == 200


def test_formulas_do_mapa_real_vem_de_vencedores_do_proprio_padrao():
    corpus = {x["id"] for x in (json.loads(l) for l in (RAIZ / "instagram/ganchos/corpus.jsonl").read_text(encoding="utf-8").splitlines())}
    mapa = json.loads((RAIZ / "instagram/ganchos/padroes-mapa.json").read_text(encoding="utf-8"))
    for slug, p in mapa["padroes"].items():
        for f in p.get("formulas", []):
            assert f["id"] in corpus, f
            assert mapa["mapa"][f["id"]] == slug, f
            assert "[" in f["formula"], f                            # mad-lib tem lacuna
    transferem = [s for s in mapa["padroes"] if s not in ("marca-clima", "objeto-impossivel")]
    assert all(mapa["padroes"][s].get("formulas") for s in transferem)


def _linha_conc(handle, i, curtidas, legenda, views=None, coletado="2026-10-16T05:00:00Z"):
    return {"id": f"{handle}-{i}", "url": f"https://www.instagram.com/p/{handle}{i}/", "tipo": "carrossel",
            "legenda": legenda, "curtidas": curtidas, "comentarios": 1, "views": views,
            "seguidores": 1000, "coletado_em": coletado}


def test_contrastar_corta_pela_mediana_de_cada_perfil(tmp_path):
    pasta = tmp_path / "concorrentes"
    pasta.mkdir()
    linhas = [_linha_conc("aaa", i, 100 + i, f"Por que o café {i} amarga?\nresto da legenda") for i in range(4)]
    linhas += [_linha_conc("aaa", i, 10 + i, f"Novidade da semana {i}") for i in range(4, 8)]
    linhas.append(_linha_conc("aaa", 0, 999, "Por que o café 0 amarga?", coletado="2026-10-17T05:00:00Z"))  # última vale
    (pasta / "aaa.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in linhas), encoding="utf-8")
    poucos = [_linha_conc("bbb", i, 50, "oi") for i in range(3)]
    (pasta / "bbb.jsonl").write_text("".join(json.dumps(x) + "\n" for x in poucos), encoding="utf-8")
    r = g.contrastar(pasta)
    a = r["perfis"]["aaa"]
    assert a["n"] == 8 and a["metrica"] == "curtidas"
    assert a["corte"] == pytest.approx(59)                            # mediana de 14..17 e 101..103 + 999 (a última linha do id 0 vale)
    assert a["vencedores"]["n"] == 4 and a["vencedores"]["pct_pergunta"] == 100.0
    assert a["perdedores"]["pct_pergunta"] == 0.0
    assert r["perfis"]["bbb"]["status"] == "poucos posts"
    assert r["gancho_de"]["aaa"] == "1ª linha da legenda"


def test_contrastar_prefere_o_gancho_de_tela_dos_proprios(tmp_path):
    pasta = tmp_path / "concorrentes"
    pasta.mkdir()
    proprios = tmp_path / "proprios.jsonl"
    linhas = [{"id": str(i), "url": f"https://www.instagram.com/p/X{i}/", "legenda": "legenda longa",
               "gancho": f"Tem casca {i}?", "curtidas": i, "alcance": 100, "views": 100 + i,
               "coletado_em": "2026-10-16T05:00:00Z"} for i in range(8)]
    proprios.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in linhas), encoding="utf-8")
    r = g.contrastar(pasta, proprios=proprios)
    assert r["gancho_de"]["cafecanastra"] == "gancho de tela (ganchos.json)"
    assert r["perfis"]["cafecanastra"]["metrica"] == "views"


def test_ranking_por_tema(tmp_path, capsys):
    destino = tmp_path / "avaliacoes.jsonl"
    regras = g.ler_rubrica()
    for m, j3 in (("Tem casca no seu café?", False), ("Parece casca no seu café. Não é.", True)):
        r = g.avaliar(G("capa", manchete=m), regras, _julg_capa(J3=j3)[1])
        g.registrar(r, tema="casca", destino=destino)
    linhas = g.ranking("casca", destino)
    assert [x["gancho"]["manchete"] for x in linhas][0] == "Parece casca no seu café. Não é."


def test_escolher_marca_a_avaliacao_registrada_e_cruza_pelo_shortcode(tmp_path):
    destino = tmp_path / "avaliacoes.jsonl"
    regras = g.ler_rubrica()
    r = g.avaliar(G("capa", manchete="Parece casca no seu café. Não é."), regras, _julg_capa()[1])
    g.registrar(r, tema="casca", destino=destino)
    linha = g.escolher("parece casca no seu cafe nao e", post="DefH_1ClN30", destino=destino)
    assert linha["escolhido"] is True and linha["post"] == "DefH_1ClN30" and linha["nota"] == 100
    todas = g.carregar_jsonl(destino)
    assert len(todas) == 2 and todas[-1]["resultados"] == todas[0]["resultados"]
    post = {"id": "1", "url": "https://www.instagram.com/p/DefH_1ClN30/", "gancho": None, "coletado_em": "x"}
    assert g.cruzar([post], todas)[0]["avaliacao"]["post"] == "DefH_1ClN30"


def test_escolher_sem_avaliacao_registra_o_que_o_script_sabe(tmp_path):
    destino = tmp_path / "avaliacoes.jsonl"
    linha = g.escolher("Tem casca no seu café?", post="X1", destino=destino, formato="capa")
    assert linha["escolhido"] is True and linha["nota"] is None and "J1" in linha["pendentes"]
    assert linha["tema"] == "(publicado sem avaliação prévia)"
