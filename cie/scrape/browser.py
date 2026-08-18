"""Fronteira com o mundo: Playwright sobre um perfil de Chrome persistente.

Fino de proposito. Abre o perfil, executa um snippet, devolve o JSON cru. Nada
aqui interpreta resposta do Instagram - isso e trabalho do `parser`, que e puro
e testavel. Este modulo nao tem teste automatizado justamente por ser a fronteira;
a verificacao dele e manual, via `cie scrape status`.
"""

from __future__ import annotations

from pathlib import Path

from ..errors import ScrapeError

JS_DIR = Path(__file__).parent / "js"

#: Snippets que precisam existir em disco para a raspagem funcionar.
#: Tambem serve de allowlist: `nome` nunca vira caminho de arquivo sem passar
#: por aqui, entao um `nome` hostil (ex: "../parser") nunca chega ao disco.
SNIPPETS = ("appid", "profile", "post", "hashtag")


def load_snippet(nome: str) -> str:
    """Le um snippet de `js/`. Snippet ausente e erro de instalacao, nao de rede."""
    if nome not in SNIPPETS:
        raise ScrapeError(
            f"snippet {nome!r} nao encontrado em {JS_DIR}; instalacao incompleta"
        )
    caminho = JS_DIR / f"{nome}.js"
    if not caminho.is_file():
        raise ScrapeError(
            f"snippet {nome!r} nao encontrado em {JS_DIR}; instalacao incompleta"
        )
    return caminho.read_text(encoding="utf-8")
