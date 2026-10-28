"""Reel 10 (linguagem "sala de prova"): imagens do ChatGPT → recortes LIMPOS, sem filete de papel.

Diferente da colagem das peças 07–09 (filete creme + 3 bordas de boil), aqui o objeto entra como
foto recortada, com borda suave de 1,5 px, e a sombra é desenhada no motor. Vidro (lupa, jarra,
xícara) fica translúcido: o miolo claro vira transparência parcial.

    python -m uv run python scripts/recorte_limpo_10.py
"""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image

BR = Path("saida-teste/reel10-geradas")
DEST = Path("instagram/remotion/projetos/10-isso-e-chafe/public/colagem")


def mascara(rgb: np.ndarray, limiar: int = 18) -> np.ndarray:
    """Distância ao branco > limiar = objeto (0/1)."""
    d = 255 - rgb.astype(np.int16).min(axis=2)
    return (d > limiar).astype(np.uint8)


def limpar(m: np.ndarray, area_min: int = 1500, preencher: bool = True) -> np.ndarray:
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, rot, st, _ = cv2.connectedComponentsWithStats(m)
    out = np.zeros_like(m)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= area_min:
            out[rot == i] = 1
    if preencher:
        cont, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(out, cont, -1, 1, thickness=cv2.FILLED)
    return out


def convexo(m: np.ndarray) -> np.ndarray:
    out = np.zeros_like(m)
    cont, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cont:
        cv2.fillConvexPoly(out, cv2.convexHull(c), 1)
    return out


def salvar(rgb: np.ndarray, alfa: np.ndarray, nome: str, pad: int = 8) -> None:
    a = cv2.GaussianBlur(alfa.astype(np.float32), (0, 0), 1.2)
    ys, xs = np.where(a > 0.02)
    y0, y1 = max(0, ys.min() - pad), min(a.shape[0], ys.max() + pad)
    x0, x1 = max(0, xs.min() - pad), min(a.shape[1], xs.max() + pad)
    rgba = np.dstack([rgb[y0:y1, x0:x1], (np.clip(a[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8)])
    DEST.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(DEST / f"r10-{nome}.png", optimize=True)
    print(f"r10-{nome:14s} {x1 - x0}x{y1 - y0}")


def vidro(rgb: np.ndarray, casca: np.ndarray, minimo: float = 0.28) -> np.ndarray:
    """Dentro do contorno, o quanto o pixel se afasta do branco vira opacidade (vidro translúcido)."""
    d = (255 - rgb.astype(np.float32).min(axis=2)) / 255
    return casca * np.clip(minimo + d * 2.4, minimo, 1)


def isnet(nome: str) -> np.ndarray:
    """Máscara do modelo isnet-general-use (rembg), que separa o objeto da sombra no branco."""
    return (np.asarray(Image.open(BR / "mascaras" / f"mask-{nome}.png").convert("L")).astype(np.float32) / 255 > 0.5).astype(np.uint8)


def abrir(arq: str) -> np.ndarray:
    return np.asarray(Image.open(BR / arq).convert("RGB"))


def componentes(m: np.ndarray, area_min: int) -> list[np.ndarray]:
    n, rot, st, _ = cv2.connectedComponentsWithStats(m)
    comps = [(st[i, cv2.CC_STAT_LEFT], (rot == i).astype(np.uint8)) for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= area_min]
    return [c for _, c in sorted(comps, key=lambda t: t[0])]


def main() -> None:
    # objetos opacos
    for nome in ["pacote", "bandeja", "cereja", "balanca", "filtro", "dosador", "carimbo", "caneca"]:
        rgb = abrir(f"r10-{nome}.png")
        salvar(rgb, limpar(isnet(nome)), nome)
    # objetos brancos sobre branco: contorno convexo
    for nome in ["manometro", "prancheta"]:
        rgb = abrir(f"r10-{nome}.png")
        salvar(rgb, convexo(limpar(mascara(rgb, 12))), nome)
    # lupa: aro e cabo opacos, lente vazia (não preenche o furo)
    rgb = abrir("r10-lupa.png")
    salvar(rgb, limpar(mascara(rgb, 24), preencher=False), "lupa")
    # vidro translúcido
    rgb = abrir("r10-jarra.png")
    salvar(rgb, vidro(rgb, convexo(limpar(mascara(rgb, 10)))), "jarra")
    rgb = abrir("g1-xicara-clarinha.png")
    salvar(rgb, vidro(rgb, convexo(limpar(mascara(rgb, 10))), 0.35), "xicara")
    # várias peças numa folha
    rgb = abrir("r10-defeitos.png")
    for nome, c in zip(["def-preto", "def-ardido", "def-broca", "def-quebrado"], componentes(limpar(isnet("defeitos")), 4000)):
        salvar(rgb, c, nome)
    rgb = abrir("r10-acucar.png")
    for k, c in enumerate(componentes(limpar(isnet("acucar")), 3000)):
        salvar(rgb, c, f"acucar-{k + 1}")
    # texturas de fundo: inteiras
    for nome in ["juta", "aco"]:
        Image.open(BR / f"r10-{nome}.png").convert("RGB").save(DEST / f"r10-{nome}.jpg", quality=92)
        print(f"r10-{nome}.jpg (textura)")


if __name__ == "__main__":
    main()
