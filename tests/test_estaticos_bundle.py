import json

import pytest
from PIL import Image

from instagram.estaticos.bundle import BundleBloqueado, escrever
from instagram.estaticos.catalogo import PECAS


def _peca_png(tmp_path, tamanho=(1080, 1350)):
    p = tmp_path / "peca.png"
    Image.new("RGB", tamanho, (20, 20, 20)).save(p)
    return p


def _todos_ok():
    return {s: "ok" for s in PECAS[0].strings_impressas}


def test_escreve_as_tres_coisas(tmp_path):
    destino = escrever(
        peca=PECAS[0], png=_peca_png(tmp_path), legenda="rascunho de legenda",
        vereditos=_todos_ok(), degraus=("soletrar",), tentativas=2,
        laudo={"pixels_alterados": 0, "aprovado": True},
        raiz=tmp_path / "saida", data="2026-10-02",
    )
    assert (destino / "peca.png").exists()
    assert (destino / "legenda.txt").read_text(encoding="utf-8") == "rascunho de legenda"
    assert (destino / "sidecar.json").exists()


def test_a_pasta_carrega_data_e_slug(tmp_path):
    destino = escrever(
        peca=PECAS[0], png=_peca_png(tmp_path), legenda="x", vereditos=_todos_ok(),
        degraus=(), tentativas=1, laudo={"aprovado": True},
        raiz=tmp_path / "saida", data="2026-10-02",
    )
    assert destino.name == "2026-10-02-cartao-classico-250g-graos"


def test_sidecar_registra_proveniencia_e_a_origem_de_cada_dado(tmp_path):
    destino = escrever(
        peca=PECAS[0], png=_peca_png(tmp_path), legenda="x", vereditos=_todos_ok(),
        degraus=("soletrar", "compor"), tentativas=3,
        laudo={"pixels_alterados": 0, "aprovado": True},
        raiz=tmp_path / "saida", data="2026-10-02",
    )
    s = json.loads((destino / "sidecar.json").read_text(encoding="utf-8"))

    assert s["slug"] == "cartao-classico-250g-graos"
    assert s["molde"] == "cartao-produto"
    assert len(s["fonte_sha256"]) == 64
    assert s["strings_esperadas"] == list(PECAS[0].strings_impressas)
    assert s["degraus"] == ["soletrar", "compor"]
    assert s["tentativas"] == 3
    assert s["laudo"]["aprovado"] is True
    assert s["dados"]["preco"]["valor"] == "R$ 31,70"
    assert "11/09/2026" in s["dados"]["preco"]["origem"]


def test_campo_nao_verificavel_bloqueia_o_bundle(tmp_path):
    v = _todos_ok()
    v["SCA 80+"] = "nao-verificavel"
    with pytest.raises(BundleBloqueado, match="SCA 80"):
        escrever(
            peca=PECAS[0], png=_peca_png(tmp_path), legenda="x", vereditos=v,
            degraus=(), tentativas=1, laudo={"aprovado": True},
            raiz=tmp_path / "saida", data="2026-10-02",
        )


def test_veredito_faltando_para_string_declarada_bloqueia(tmp_path):
    parcial = {s: "ok" for s in PECAS[0].strings_impressas[:-1]}
    with pytest.raises(BundleBloqueado, match="sem veredito"):
        escrever(
            peca=PECAS[0], png=_peca_png(tmp_path), legenda="x", vereditos=parcial,
            degraus=(), tentativas=1, laudo={"aprovado": True},
            raiz=tmp_path / "saida", data="2026-10-02",
        )


def test_laudo_reprovado_bloqueia(tmp_path):
    with pytest.raises(BundleBloqueado, match="laudo"):
        escrever(
            peca=PECAS[0], png=_peca_png(tmp_path), legenda="x", vereditos=_todos_ok(),
            degraus=("compor",), tentativas=3,
            laudo={"pixels_alterados": 12, "aprovado": False},
            raiz=tmp_path / "saida", data="2026-10-02",
        )


def test_dimensao_errada_bloqueia(tmp_path):
    ruim = _peca_png(tmp_path, tamanho=(1080, 1349))
    with pytest.raises(BundleBloqueado, match="1080x1350"):
        escrever(
            peca=PECAS[0], png=ruim, legenda="x", vereditos=_todos_ok(),
            degraus=(), tentativas=1, laudo={"aprovado": True},
            raiz=tmp_path / "saida", data="2026-10-02",
        )
