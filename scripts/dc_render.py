"""Artboard do Claude Design (.dc.html) -> PNG 1080x1350 + os portoes do carrossel.

Uso:
    python -m uv run python scripts/dc_render.py <pasta-do-canvas> <blobs.json> <destino>

`<pasta-do-canvas>` e a pasta que contem `project/` (canvas.json + *.dc.html).
`<blobs.json>` mapeia a URL `/_blob/<id>` que o artboard usa para o arquivo local
que foi enviado ao canvas -- o render local precisa do mesmo pixel que o canvas mostra.

POR QUE EXISTE. O Claude Design mostra o deck, mas o motor de carrossel exige tres
portoes medidos e o olho no `_feed` antes de publicar (skill canastra-carrossel). Este
script nao reimplementa nada: tira o miolo do `<x-dc>`, monta um HTML comum e chama
`instagram.carrossel.render` (render, medir, miniaturas) e `portoes` (transbordo,
legibilidade). Os campos medidos sao os elementos com `data-campo`, igual ao motor.

LIMITE CONHECIDO: o artboard nao pode depender de `{{buracos}}` do runtime -- o texto
tem que estar literal no markup (o que o proprio formato recomenda para copy).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from instagram.carrossel import portoes  # noqa: E402
from instagram.carrossel.molde import ALTURA, LARGURA, SEGURO_BASE, SEGURO_TOPO  # noqa: E402
from instagram.carrossel.render import _MEDICAO_JS, medir, miniaturas, render  # noqa: E402


def html_local(dc: str, blobs: dict[str, Path]) -> str:
    """Miolo do <x-dc> num documento comum, com os blobs trocados por file://."""
    m = re.search(r"<x-dc>(.*)</x-dc>", dc, re.S)
    if not m:
        raise ValueError("artboard sem <x-dc>")
    miolo = m.group(1)
    h = re.search(r"<helmet>(.*?)</helmet>", miolo, re.S)
    cabeca = h.group(1) if h else ""
    corpo = miolo.replace(h.group(0), "") if h else miolo
    if "{{" in corpo:
        raise ValueError("artboard usa {{buraco}} -- o render local nao resolve o runtime")
    for url, arq in blobs.items():
        cabeca = cabeca.replace(url, arq.resolve().as_uri())
        corpo = corpo.replace(url, arq.resolve().as_uri())
    faltando = re.findall(r"/_blob/[A-Za-z0-9_-]+", cabeca + corpo)
    if faltando:
        raise ValueError(f"blob sem arquivo local no mapa: {sorted(set(faltando))}")
    js = _MEDICAO_JS % (SEGURO_TOPO, SEGURO_BASE, ALTURA, LARGURA)
    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        f"<title>sem medicao</title>{cabeca}"
        f"<style>html,body{{margin:0;width:{LARGURA}px;height:{ALTURA}px;overflow:hidden}}</style>"
        f"</head><body>{corpo}<script>{js}</script></body></html>"
    )


def main(argv: list[str]) -> int:
    pasta, mapa, destino = Path(argv[0]), Path(argv[1]), Path(argv[2])
    canvas = json.loads((pasta / "project" / "canvas.json").read_text(encoding="utf-8"))
    blobs = {k: (RAIZ / v) for k, v in json.loads(mapa.read_text(encoding="utf-8")).items()}
    html_dir = destino / "_html"
    html_dir.mkdir(parents=True, exist_ok=True)

    htmls: list[Path] = []
    for i, nome in enumerate(canvas["order"], 1):
        dc = (pasta / "project" / nome).read_text(encoding="utf-8")
        p = html_dir / f"slide-{i}.html"
        p.write_text(html_local(dc, blobs), encoding="utf-8")
        htmls.append(p)

    pngs = render(htmls, destino)
    medicoes = [medir(h) for h in htmls]
    for png in pngs:
        miniaturas(png, destino / "_feed")

    trans = portoes.transbordo(medicoes)
    leg = portoes.legibilidade(medicoes)
    for m in medicoes:
        print(f"slide {m['slide']}: campos {[t['campo'] for t in m['textos']]} "
              f"| px min {min((t['px'] for t in m['textos']), default=0):.0f} "
              f"| fonte {m.get('fonte_pintada', '?')[:40]}")
    for x in trans + leg:
        print("PORTAO:", x)
    print("ok" if not (trans or leg) else "REPROVADO",
          f"- {len(pngs)} PNG em {destino}; olhe o _feed antes de publicar")
    return 0 if not (trans or leg) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
