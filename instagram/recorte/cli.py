"""Linha de comando do recorte: foto real -> PNG RGBA + laudo em JSON.

Uso:
    python -m instagram.recorte <entrada.jpg> <saida.png> [--banda 6]
    python -m instagram.recorte <entrada.jpg> <saida.png> \
        --retangulo-rotulo x0 y0 x1 y1

O codigo de saida e 1 quando o laudo reprova. Isso e proposital: quebra
qualquer script que ignore o laudo e siga publicando um recorte que mexeu no
pixel do rotulo. Ver `verificar.laudo_preservacao` e o plano em
docs/superpowers/plans/2026-09-30-assets-recorte-e-geracao.md.

`--retangulo-rotulo` e opcional porque o retangulo so se conhece DEPOIS de
abrir o PNG e medir onde a tipografia comeca e termina (licao 14 do CLAUDE.md:
limite de arte se mede no proprio pixel, nao se chuta). O fluxo e: recortar
uma vez sem retangulo, medir, rodar de novo com o retangulo medido -- ai o
laudo passa a exigir alfa 255 letra por letra.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image

from .matte import recortar_detalhado
from .trimap import MODOS, PremissaDeRecorteViolada
from .verificar import laudo_preservacao


def _sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="python -m instagram.recorte",
        description="Recorta packshot em fundo neutro preservando o pixel.",
    )
    p.add_argument("entrada")
    p.add_argument("saida")
    p.add_argument("--banda", type=int, default=6,
                   help="largura em px da faixa de incerteza do trimap")
    p.add_argument("--retangulo-rotulo", type=int, nargs=4,
                   metavar=("X0", "Y0", "X1", "Y1"), default=None,
                   help="retangulo medido da tipografia; dentro dele qualquer "
                        "alfa abaixo de 255 reprova")
    p.add_argument("--modo", choices=MODOS, default="auto",
                   help="metodo de trimap; 'auto' mede e escolhe, e registra "
                        "no JSON qual rodou")
    a = p.parse_args(argv)

    entrada = Path(a.entrada)
    saida = Path(a.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)

    img = np.array(Image.open(entrada).convert("RGB"))
    try:
        rgba, diagnostico = recortar_detalhado(img, banda=a.banda,
                                               modo=a.modo)
    except PremissaDeRecorteViolada as erro:
        # Nao grava nada: PNG com parede junto e pior que PNG ausente, porque
        # o ausente alguem percebe.
        print(f"RECUSADO {a.entrada}\n  {erro}", file=sys.stderr)
        return 2

    retangulo = tuple(a.retangulo_rotulo) if a.retangulo_rotulo else None
    laudo = laudo_preservacao(img, rgba[:, :, :3], rgba[:, :, 3],
                              retangulo_rotulo=retangulo)

    Image.fromarray(rgba).save(saida)
    saida.with_suffix(".json").write_text(
        json.dumps(
            {
                "origem": a.entrada,
                "origem_sha256": _sha256(entrada),
                "dimensoes": [int(img.shape[1]), int(img.shape[0])],
                "banda": a.banda,
                "retangulo_rotulo": list(retangulo) if retangulo else None,
                "gerado_em": datetime.now(timezone.utc).isoformat(
                    timespec="seconds"),
                "recorte": diagnostico,
                "laudo": laudo,
            },
            ensure_ascii=False, indent=1),
        encoding="utf-8")

    print(f"{saida}  modo={diagnostico['modo']} "
          f"cobertura={100 * diagnostico['fracao_coberta']:.1f}% "
          f"toca_borda={diagnostico['toca_borda']} "
          f"alterados={laudo['pixels_alterados']} "
          f"maior_delta={laudo['maior_delta']} "
          f"alfa_min_rotulo={laudo['alfa_minimo_no_rotulo']} "
          f"aprovado={laudo['aprovado']}")
    return 0 if laudo["aprovado"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
