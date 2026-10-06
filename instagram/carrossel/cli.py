"""Linha de comando do motor de carrossel.

    python -m instagram.carrossel conferir
    python -m instagram.carrossel listar
    python -m instagram.carrossel prompt <slug>
    python -m instagram.carrossel render <slug> --destino DIR

`conferir` devolve 1 quando a declaracao tem problema -- de proposito, para quebrar
script que ignore o relatorio. Mesma escolha de `instagram/estaticos/cli.py`.

`render` e `portoes` entram por IMPORT TARDIO: `conferir` e `listar` tem que
funcionar mesmo sem Chrome e sem PIL.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

from .catalogo import DECKS, por_slug
from .tipos import validar

#: Frase de theme-lock, portada de charlesdove977/carousel-builder e adaptada a
#: nossa pilha (claude-in-chrome + ChatGPT, nunca Higgsfield). A capa aprovada
#: vira ancora e viaja anexada em toda geracao seguinte -- e a licao 8 resolvida
#: por construcao, em vez de repetir a descricao da cena em texto.
THEME_LOCK = (
    "Match the colour palette, lighting, art style, texture and mood of the "
    "provided reference photograph exactly. Change only the subject described above."
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m instagram.carrossel")
    sub = p.add_subparsers(dest="comando", required=True)
    sub.add_parser("conferir", help="valida os decks declarados sem renderizar")
    sub.add_parser("listar", help="lista os decks e os tipos de slide usados")
    pr = sub.add_parser("prompt", help="imprime o bloco de theme-lock de cada slide com foto")
    pr.add_argument("slug")
    rd = sub.add_parser("render", help="renderiza e roda os tres portoes")
    rd.add_argument("slug")
    rd.add_argument("--destino", required=True)

    a = p.parse_args(argv)

    if a.comando == "conferir":
        problemas = [f"{d.slug}: {x}" for d in DECKS for x in validar(d)]
        if problemas:
            for x in problemas:
                print(x, file=sys.stderr)
            return 1
        print(f"ok: {len(DECKS)} deck(s), nenhum problema")
        return 0

    if a.comando == "listar":
        for d in DECKS:
            c = Counter(s.tipo for s in d.slides)
            f = Counter(s.fundo for s in d.slides)
            print(f"{d.slug}\t{len(d.slides)} slides")
            print(f"  tipos:  {', '.join(f'{k}x{v}' for k, v in c.items())}")
            print(f"  fundos: {', '.join(f'{k}x{v}' for k, v in f.items())}")
        return 0

    d = por_slug(a.slug)
    if d is None:
        print(f"slug '{a.slug}' nao existe. Validos: "
              f"{', '.join(x.slug for x in DECKS)}", file=sys.stderr)
        return 2

    if a.comando == "prompt":
        print(f"# {d.slug} -- blocos de geracao\n")
        print("ORDEM: gere e APROVE a capa primeiro. Ela vira a ancora; toda imagem")
        print("seguinte anexa a capa aprovada mais a frase de theme-lock abaixo.\n")
        for i, s in enumerate(d.slides, 1):
            if s.fundo != "foto":
                continue
            papel = "ANCORA (gere e aprove primeiro)" if i == 1 else "anexe a capa aprovada"
            print(f"## slide {i} -- {s.tipo} -- {papel}")
            print(f"foto declarada: {s.foto}")
            if i > 1:
                print(f"\n{THEME_LOCK}")
            print()
        return 0

    # render: import tardio
    try:
        from . import portoes, render
    except ImportError as e:
        print(f"render/portoes indisponivel: {e}", file=sys.stderr)
        return 2

    problemas = validar(d)
    if problemas:
        for x in problemas:
            print(x, file=sys.stderr)
        return 1

    destino = Path(a.destino)
    htmls = render.escrever_html(d, destino / "html")
    pngs = render.render(htmls, destino / "png")
    medicoes = [render.medir(h) for h in htmls]
    for png in pngs:
        render.miniaturas(png, destino / "_feed")

    r = portoes.todos(d, medicoes)
    for nome in ("orcamento", "transbordo", "legibilidade"):
        if r[nome]:
            print(f"-- portao {nome}", file=sys.stderr)
            for x in r[nome]:
                print(f"   {x}", file=sys.stderr)
    if not r["ok"]:
        return 1
    print(f"ok: {len(pngs)} slides, tres portoes passaram")
    print(f"   olhe {destino / '_feed'} antes de publicar -- numero nao substitui olhar")
    return 0
