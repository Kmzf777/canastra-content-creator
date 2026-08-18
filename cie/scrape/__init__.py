"""Raspagem de imagem do Instagram para dentro de `raspagem/`.

O pacote e dividido em uma parte pura e uma parte suja:

  * `targets` e `parser` nao tocam rede e nao sabem que Playwright existe;
  * `browser` e a unica fronteira com o mundo, e e fina de proposito.

Nada aqui escreve no banco do CIE. `cie scrape` para em `raspagem/`; mover para
`base-curada/` continua sendo decisao humana registrada.
"""

from __future__ import annotations
