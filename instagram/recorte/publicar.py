"""Copia para o motor de video APENAS o recorte que passou no laudo.

PNG sem .json irmao e PNG reprovado nao viajam. O portao e aqui porque e o
ultimo ponto antes de o pixel virar video publicado.

O portao e fail-closed: qualquer duvida sobre o laudo (arquivo ausente, JSON
truncado, campo `laudo` vazio) conta como reprovado. Um seletor que nao acha o
laudo mas deixa passar o pixel e pior que um que recusa -- e a licao 17 do
CLAUDE.md aplicada ao lado da saida.

PARA ONDE ELE COPIA, e por que nao e `remotion/public/`: o Remotion aceita UMA
pasta publica por render (`--public-dir`), e o motor de video ja usava esse
mecanismo para servir o video cru do projeto. Uma pasta publica na raiz do motor
e uma pasta publica por projeto sao usos incompativeis do mesmo argumento.

A convencao que resolveu isso e UMA pasta publica por PROJETO, com subpastas:

    instagram/remotion/projetos/<projeto>/public/fonte/    video cru
    instagram/remotion/projetos/<projeto>/public/assets/   <- aqui

e o render passa `--public-dir=projetos/<projeto>/public`. O lado TypeScript
dessa convencao esta em `instagram/remotion/src/motor/pasta-publica.ts`; se um
dos dois lados mudar, o outro tem que mudar junto.

Uso:
    python -m instagram.recorte.publicar                      # projeto padrao
    python -m instagram.recorte.publicar --projeto=02-outro
    python -m instagram.recorte.publicar [origem] [destino]   # caminhos crus

Plano: docs/superpowers/plans/2026-09-30-assets-recorte-e-geracao.md, Tarefa 6.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

# Raiz do repositorio: .../instagram/recorte/publicar.py -> parents[2]
_RAIZ = Path(__file__).resolve().parents[2]
_PROJETOS = _RAIZ / "instagram" / "remotion" / "projetos"
PROJETO_PADRAO = "01-private-label"
ORIGEM_PADRAO = _RAIZ / "instagram" / "assets" / "embalagem"


def destino_do_projeto(projeto: str = PROJETO_PADRAO) -> Path:
    """`projetos/<projeto>/public/assets`, a subpasta que `staticFile` le.

    Existe como funcao, e nao como constante, porque o nome do projeto e um
    argumento: chumbar `01-private-label` numa constante faria o segundo projeto
    publicar em cima do primeiro sem reclamar.
    """
    return _PROJETOS / projeto / "public" / "assets"


DESTINO_PADRAO = destino_do_projeto()


def publicar(origem: Path, destino: Path) -> list[str]:
    """Copia de `origem` para `destino` so os PNG com laudo aprovado.

    Devolve a lista dos nomes copiados, em ordem. Cada recusa sai no stderr
    dizendo o motivo -- silencio aqui seria um asset faltando no video sem
    ninguem saber por que.
    """
    origem, destino = Path(origem), Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    copiados: list[str] = []
    for png in sorted(origem.glob("*.png")):
        laudo_path = png.with_suffix(".json")
        if not laudo_path.exists():
            print(f"  ignorado (sem laudo): {png.name}", file=sys.stderr)
            continue
        try:
            dados = json.loads(laudo_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as erro:
            print(f"  ignorado (laudo ilegivel: {erro}): {png.name}",
                  file=sys.stderr)
            continue
        laudo = dados.get("laudo") if isinstance(dados, dict) else None
        if not isinstance(laudo, dict) or laudo.get("aprovado") is not True:
            print(f"  ignorado (reprovado): {png.name}", file=sys.stderr)
            continue
        shutil.copy2(png, destino / png.name)
        copiados.append(png.name)
    return copiados


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("origem", nargs="?", default=str(ORIGEM_PADRAO))
    p.add_argument("destino", nargs="?", default=None)
    p.add_argument("--projeto", default=PROJETO_PADRAO,
                   help="projeto do motor de video; decide o destino se ele nao "
                        "for dado explicitamente")
    a = p.parse_args(argv)

    # `destino` explicito ganha de `--projeto`: quem digitou um caminho quer
    # aquele caminho. Sem ele, o destino sai do projeto.
    destino = Path(a.destino) if a.destino else destino_do_projeto(a.projeto)

    copiados = publicar(Path(a.origem), destino)
    print(f"{len(copiados)} publicado(s) em {destino}")
    for nome in copiados:
        print(f"  {nome}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
