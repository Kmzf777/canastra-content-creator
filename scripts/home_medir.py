"""Mede as variantes contra o perfil de camera do projeto e contra o contraste.

POR QUE MEDIR E NAO OLHAR. O alvo nao e gosto: e a assinatura do dispositivo que
a base real do projeto tem. Ponto preto levantado, saturacao lavada, altas
puxando azul, cantos moles. Uma imagem bonita fora do alvo denuncia geracao;
uma imagem dentro do alvo passa por foto.

ALVOS, medidos nas fotos proprias (iPhone 7 na fazenda, Motorola nos packshots):

    p1 (ponto preto)         14      HDR de celular nao desce mais que isso
    preto%                   0,007   celular quase nunca chega a preto puro
    estourado%               0,015   celular estoura area pequena sem pedir licenca
    saturacao                70      a base e LAVADA, nao vibrante
    cast altas R/B           0,969   puxa AZUL; dourado quente e assinatura de IA
    nitidez centro/borda     1,57    lente barata desaba nos cantos

CONTRASTE DA ZONA DE TEXTO. A Nike nao tem um unico scrim: a sombra sob o texto
esta DENTRO da foto, e a zona e mais escura que o resto do quadro em 12 de 12
casos. Aqui a zona medida e o quarto inferior esquerdo, contra `cal` #F1F0EA, e
o que se mede e o PERCENTIL 95 da luminancia — nao a media. E o pixel claro que
quebra a legibilidade, nao o tipico.

    python -m uv run python scripts/home_medir.py saida-teste/home-cenas
    python -m uv run python scripts/home_medir.py entrega-site --texto
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ALVO = {
    "p1": 14.0,
    "preto%": 0.007,
    "estourado%": 0.015,
    "satur": 70.0,
    "R/B": 0.969,
    "nitidez": 1.57,
}

#: Luminancia relativa WCAG do `cal` #F1F0EA, a cor do texto sobre o heroi.
L_CAL = 0.8690


def _lin(c: np.ndarray) -> np.ndarray:
    """sRGB -> linear, para luminancia relativa WCAG."""
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def luminancia_relativa(rgb: np.ndarray) -> np.ndarray:
    r, g, b = (_lin(rgb[..., i] / 255.0) for i in range(3))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def perfil(caminho: Path) -> dict[str, float]:
    im = Image.open(caminho).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    cinza = a.mean(axis=2)

    p1 = float(np.percentile(cinza, 1))
    preto = float((cinza <= 2).mean() * 100)
    estourado = float((cinza >= 253).mean() * 100)

    mx, mn = a.max(axis=2), a.min(axis=2)
    satur = float(np.where(mx > 0, (mx - mn) / np.maximum(mx, 1) * 255, 0).mean())

    # Cast nas ALTAS: so o quarto mais claro do quadro. E la que o dourado de IA
    # aparece — na sombra ele se esconde.
    lim = np.percentile(cinza, 75)
    altas = cinza >= lim
    rb = float(a[..., 0][altas].mean() / max(a[..., 2][altas].mean(), 1e-6))

    # Nitidez centro vs borda: variancia do laplaciano aproximada por gradiente.
    h, w = cinza.shape
    def nit(bloco: np.ndarray) -> float:
        gy, gx = np.gradient(bloco)
        return float((gx**2 + gy**2).mean())

    centro = cinza[h // 3 : 2 * h // 3, w // 3 : 2 * w // 3]
    cantos = np.concatenate(
        [
            cinza[: h // 6, : w // 6].ravel(),
            cinza[: h // 6, -w // 6 :].ravel(),
            cinza[-h // 6 :, : w // 6].ravel(),
            cinza[-h // 6 :, -w // 6 :].ravel(),
        ]
    ).reshape(-1, 1)
    borda = nit(cantos.reshape(2, -1))
    razao = nit(centro) / max(borda, 1e-6)

    return {
        "p1": p1,
        "preto%": preto,
        "estourado%": estourado,
        "satur": satur,
        "R/B": rb,
        "nitidez": razao,
    }


def contraste_zona_texto(caminho: Path) -> tuple[float, float]:
    """Contraste na zona de texto do heroi: quarto inferior esquerdo.

    Devolve (contraste no percentil 95, contraste na mediana). O que decide e o
    p95: e o pixel claro que quebra a legibilidade.
    """
    im = Image.open(caminho).convert("RGB")
    a = np.asarray(im)
    h, w = a.shape[:2]
    zona = a[int(h * 0.62) : int(h * 0.97), int(w * 0.04) : int(w * 0.46)]
    L = luminancia_relativa(zona.astype(np.float32))
    p95 = float(np.percentile(L, 95))
    med = float(np.median(L))
    razao = lambda l: (L_CAL + 0.05) / (l + 0.05)  # noqa: E731
    return razao(p95), razao(med)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dir")
    ap.add_argument("--texto", action="store_true", help="mede a zona de texto")
    ap.add_argument("--glob", default="*.jpg")
    a = ap.parse_args()

    arquivos = sorted(Path(a.dir).glob(a.glob))
    if not arquivos:
        print("nada encontrado", file=sys.stderr)
        return 2

    cab = f"{'arquivo':34s} {'p1':>6s} {'preto%':>7s} {'estou%':>7s} {'satur':>6s} {'R/B':>6s} {'nitid':>6s}"
    if a.texto:
        cab += f" {'txt p95':>8s} {'txt med':>8s}"
    print(cab)
    print("-" * len(cab))
    print(
        f"{'>>> ALVO':34s} {ALVO['p1']:6.1f} {ALVO['preto%']:7.3f} "
        f"{ALVO['estourado%']:7.3f} {ALVO['satur']:6.1f} {ALVO['R/B']:6.3f} "
        f"{ALVO['nitidez']:6.2f}"
    )
    print("-" * len(cab))

    for f in arquivos:
        p = perfil(f)
        linha = (
            f"{f.name[:34]:34s} {p['p1']:6.1f} {p['preto%']:7.3f} "
            f"{p['estourado%']:7.3f} {p['satur']:6.1f} {p['R/B']:6.3f} "
            f"{p['nitidez']:6.2f}"
        )
        if a.texto:
            c95, cmed = contraste_zona_texto(f)
            linha += f" {c95:7.1f}: {cmed:7.1f}:"
        print(linha)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
