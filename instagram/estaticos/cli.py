"""Linha de comando do motor de estaticos.

    python -m instagram.estaticos conferir
    python -m instagram.estaticos listar
    python -m instagram.estaticos prompt <slug> [--correcao soletrar ...]

`conferir` devolve 1 quando a declaracao tem problema -- de proposito, para
quebrar qualquer script que ignore o relatorio e siga gerando.
"""

from __future__ import annotations

import argparse
import sys

from .catalogo import PECAS, validar
from .prompt import CORRECOES, montar


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m instagram.estaticos")
    sub = p.add_subparsers(dest="comando", required=True)

    sub.add_parser("conferir", help="valida a declaracao sem gerar nada")
    sub.add_parser("listar", help="lista os slugs declarados")

    pr = sub.add_parser("prompt", help="imprime o prompt de uma peca")
    pr.add_argument("slug")
    pr.add_argument(
        "--correcao", action="append", default=[], choices=list(CORRECOES),
        help="degrau de correcao a aplicar; pode repetir",
    )

    a = p.parse_args(argv)

    if a.comando == "conferir":
        problemas = validar(PECAS)
        if problemas:
            for x in problemas:
                print(x, file=sys.stderr)
            return 1
        print(f"ok: {len(PECAS)} peca(s) declarada(s), nenhum problema")
        return 0

    if a.comando == "listar":
        for peca in PECAS:
            print(f"{peca.slug}\t{peca.molde}")
        return 0

    por_slug = {peca.slug: peca for peca in PECAS}
    peca = por_slug.get(a.slug)
    if peca is None:
        print(
            f"slug '{a.slug}' nao existe. Validos: {', '.join(sorted(por_slug))}",
            file=sys.stderr,
        )
        return 2
    try:
        print(montar(peca, tuple(a.correcao)))
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    return 0
