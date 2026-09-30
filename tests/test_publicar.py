"""Portao de publicacao: so recorte aprovado chega ao motor de video.

Vive em arquivo proprio (e nao em tests/test_recorte.py, como o plano escreveu)
porque as outras tarefas do mesmo plano escrevem nesse arquivo em paralelo.
Plano: docs/superpowers/plans/2026-09-30-assets-recorte-e-geracao.md, Tarefa 6.
"""

import json
from pathlib import Path

from PIL import Image

from instagram.recorte.publicar import publicar


def _par(pasta: Path, nome: str, aprovado: bool) -> None:
    """Cria um png e o .json irmao com o laudo pedido."""
    Image.new("RGBA", (8, 8), (10, 20, 30, 255)).save(pasta / f"{nome}.png")
    (pasta / f"{nome}.json").write_text(
        json.dumps({"laudo": {"aprovado": aprovado}}), encoding="utf-8")


def test_publicar_copia_o_aprovado(tmp_path):
    origem, destino = tmp_path / "a", tmp_path / "b"
    origem.mkdir()
    destino.mkdir()
    _par(origem, "classico-250g", True)

    copiados = publicar(origem, destino)

    assert copiados == ["classico-250g.png"]
    assert (destino / "classico-250g.png").exists()


def test_publicar_ignora_o_reprovado(tmp_path):
    origem, destino = tmp_path / "a", tmp_path / "b"
    origem.mkdir()
    destino.mkdir()
    _par(origem, "suave-250g", False)

    copiados = publicar(origem, destino)

    assert copiados == []
    assert not (destino / "suave-250g.png").exists()


def test_publicar_ignora_png_sem_laudo(tmp_path):
    origem, destino = tmp_path / "a", tmp_path / "b"
    origem.mkdir()
    destino.mkdir()
    Image.new("RGBA", (8, 8)).save(origem / "orfao.png")

    copiados = publicar(origem, destino)

    assert copiados == []


# --- portao fecha tambem quando o laudo existe mas nao afirma nada ---------
# Sao os casos em que `.get("laudo", {}).get("aprovado")` estouraria ou
# mentiria. Fail-closed: laudo que nao se le nao e laudo aprovado.


def test_publicar_ignora_json_corrompido(tmp_path):
    origem, destino = tmp_path / "a", tmp_path / "b"
    origem.mkdir()
    destino.mkdir()
    Image.new("RGBA", (8, 8)).save(origem / "truncado.png")
    (origem / "truncado.json").write_text('{"laudo": {"aprov', encoding="utf-8")

    copiados = publicar(origem, destino)

    assert copiados == []
    assert not (destino / "truncado.png").exists()


def test_publicar_ignora_laudo_nulo(tmp_path):
    origem, destino = tmp_path / "a", tmp_path / "b"
    origem.mkdir()
    destino.mkdir()
    Image.new("RGBA", (8, 8)).save(origem / "sem-campo.png")
    (origem / "sem-campo.json").write_text(
        json.dumps({"origem": "x.jpg", "laudo": None}), encoding="utf-8")

    copiados = publicar(origem, destino)

    assert copiados == []


# --- a ponte com o motor de video ------------------------------------------
# A convencao da pasta publica esta escrita em DOIS lugares: aqui, em
# `destino_do_projeto()`, e no TypeScript, em `src/motor/pasta-publica.ts`. Nada
# no compilador liga os dois -- mudar so um lado deixa publicar.py escrevendo
# numa pasta que `staticFile()` nao le, e o sintoma e um `<Img>` 404 no meio de
# um render de 700 frames. Estes testes existem para que a divergencia apareca
# em 1 segundo de pytest, e nao no render.


def test_destino_fica_na_pasta_publica_do_projeto():
    from instagram.recorte.publicar import destino_do_projeto

    d = destino_do_projeto("01-private-label")

    # a ordem importa: `public` tem que ser ANCESTRAL de `assets`, porque e
    # `public` que vai em --public-dir e `assets/` que vai em staticFile()
    assert d.parts[-3:] == ("01-private-label", "public", "assets")


def test_destino_muda_com_o_projeto():
    """Chumbar o projeto faria o segundo projeto publicar em cima do primeiro."""
    from instagram.recorte.publicar import destino_do_projeto

    assert destino_do_projeto("01-private-label") != destino_do_projeto("02-outro")


def test_subpastas_batem_com_as_do_typescript():
    """Os nomes de subpasta do lado Python e do lado TS tem que ser os mesmos.

    Le o .ts como texto de proposito: importar TypeScript do pytest exigiria
    um runtime Node e o que se quer provar aqui e so a igualdade de duas
    strings. Se `pasta-publica.ts` for renomeado ou reescrito, este teste
    quebra -- que e exatamente o aviso desejado.
    """
    from instagram.recorte.publicar import destino_do_projeto

    ts = (Path(__file__).resolve().parents[1] / "instagram" / "remotion" /
          "src" / "motor" / "pasta-publica.ts")
    assert ts.exists(), f"o lado TS da convencao sumiu: {ts}"
    texto = ts.read_text(encoding="utf-8")

    destino = destino_do_projeto("01-private-label")
    pasta_publica, assets = destino.parts[-2], destino.parts[-1]

    assert f"PASTA_PUBLICA = '{pasta_publica}'" in texto, (
        f"o Python publica sob '{pasta_publica}/' e pasta-publica.ts discorda")
    assert f"assets: '{assets}'" in texto, (
        f"o Python publica em '{assets}/' e SUB.assets do TS discorda")
