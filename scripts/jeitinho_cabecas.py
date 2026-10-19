"""Peça 09: cabeças recortadas dos três criadores para a colagem.

Fonte: quadros dos reels deles (raspagem/_jeitinho-cafe, gitignored) e a máscara de
pessoa do rembg `u2net_human_seg` (rodada num venv isolado em ~/.cache/rbg). O rosto é de
terceiro: as cabeças vão só para `projetos/09-jeitinho-cafe/public/` (gitignored) e NÃO
entram na biblioteca de colagem. Publicar depende da autorização por escrito de cada um.

A máscara de pessoa traz o corpo, a escada atrás do Fábio, a cafeteira e a legenda queimada
do Gabriel; a cabeça é a maior região dentro de uma elipse em volta do rosto (caixa medida
na folha de máscaras sobre magenta).

    python -m uv run python scripts/jeitinho_cabecas.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from colagem_assets import peca  # noqa: E402

FONTE = Path("raspagem/_jeitinho-cafe/cabecas")
DEST = Path("instagram/remotion/projetos/09-jeitinho-cafe/public/colagem")

# nome de saída → (quadro, caixa da elipse em fração: x0, y0, x1, y1)
CABECAS = {
    "cab-fabio": ("fabio-sabor", (0.25, 0.372, 0.75, 0.745)),  # 30,7 s, o mais nítido; topo baixo tira a escada
    "cab-paulo": ("paulo", (0.16, 0.302, 0.548, 0.52)),
    "cab-gabriel": ("gabriel-close", (0.32, 0.13, 0.74, 0.50)),
    "cab-gabriel-sorriso": ("gabriel-frente", (0.33, 0.235, 0.66, 0.47)),
    "cab-giuseppe": ("giuseppe", (0.325, 0.172, 0.625, 0.462)),  # 25,5 s, o mais nítido; elipse deixa o polegar de fora
}


def cabeca(quadro: str, caixa: tuple[float, float, float, float]) -> tuple[np.ndarray, np.ndarray]:
    rgba = np.array(Image.open(FONTE / f"{quadro}-alfa.png").convert("RGBA"))
    h, w = rgba.shape[:2]
    x0, y0, x1, y1 = caixa
    elipse = np.zeros((h, w), np.uint8)
    cv2.ellipse(elipse, (int((x0 + x1) / 2 * w), int((y0 + y1) / 2 * h)),
                (int((x1 - x0) / 2 * w), int((y1 - y0) / 2 * h)), 0, 0, 360, 1, -1)
    a = (rgba[..., 3] > 127).astype(np.uint8) & elipse
    n, rot, st, _ = cv2.connectedComponentsWithStats(a)
    if n < 2:
        raise SystemExit(f"{quadro}: nada dentro da elipse")
    maior = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    a = (rot == maior).astype(np.float32)
    # o alfa do rembg é suave no cabelo: usa o valor dele dentro da região escolhida
    a = a * (rgba[..., 3].astype(np.float32) / 255)
    ys, xs = np.where(a > 0.02)
    p = 6
    y0p, y1p, x0p, x1p = max(ys.min() - p, 0), min(ys.max() + p, h), max(xs.min() - p, 0), min(xs.max() + p, w)
    return rgba[y0p:y1p, x0p:x1p, :3].copy(), a[y0p:y1p, x0p:x1p]


def main() -> None:
    for nome, (quadro, caixa) in CABECAS.items():
        rgb, a = cabeca(quadro, caixa)
        peca(rgb, a, nome, filete=10, com_reticula=False, destino=DEST)


if __name__ == "__main__":
    main()
