"""Recortes de colagem da peça 06: folha gerada -> objetos com retícula e filete.

Entrada: as folhas do ChatGPT (objetos separados sobre branco liso) e fotos reais.
Saída, em `public/colagem/`, para cada peça três arquivos `<nome>-b0/b1/b2.png`:
o mesmo objeto com a borda de papel recortado em três variantes, para o "boil"
de stop-motion que o Remotion alterna a cada 3 quadros.

Por que recorte local e não remove.bg: as folhas nascem sobre branco liso de
propósito, o que torna a separação exata em resolução cheia; o remove.bg só
entrega prévia de baixa resolução no plano gratuito.

Tudo determinístico (semente por nome de peça).

    python -m uv run python scripts/colagem_assets.py
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps

BRUTOS = Path("saida-teste/motion-06/brutos")
FONTE = Path("instagram/remotion/projetos/06-voce-sabia-especial/public/fonte")
DEST = Path("instagram/remotion/projetos/06-voce-sabia-especial/public/colagem")
CREME = np.array([241, 236, 224], np.float32)
TINTA = np.array([20, 16, 13], np.float32)


def rng(nome: str) -> np.random.Generator:
    return np.random.default_rng(int(hashlib.sha256(nome.encode()).hexdigest()[:8], 16))


# ---------------------------------------------------------------- separação

def mascara_objetos(rgb: np.ndarray, limiar: int = 22) -> np.ndarray:
    """Objeto = tudo que se afasta do branco. Sombra suave clara fica de fora."""
    dist = 255 * 3 - rgb.astype(np.int32).sum(axis=2)
    m = (dist > limiar * 3).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    # fecha buracos internos (xícara branca dentro do pires branco)
    cont, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cheia = np.zeros_like(m)
    cv2.drawContours(cheia, cont, -1, 1, thickness=cv2.FILLED)
    return cheia


def convexo(alfa: np.ndarray) -> np.ndarray:
    """Preenche o contorno convexo: objeto branco sobre fundo branco (pires) perde
    metade da borda no limiar, e o pires é redondo -- o casco o devolve inteiro."""
    m = (alfa > 0.5).astype(np.uint8)
    pts = cv2.findNonZero(m)
    casco = np.zeros_like(m)
    cv2.fillConvexPoly(casco, cv2.convexHull(pts), 1)
    return cv2.GaussianBlur(casco.astype(np.float32), (3, 3), 0.8)


def separar(folha: Path, nomes: list[str], juntar_px: int = 18, area_min: int = 2500,
            limiar: int = 22) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    rgb = np.array(Image.open(folha).convert("RGB"))
    m = mascara_objetos(rgb, limiar)
    grosso = cv2.dilate(m, np.ones((juntar_px, juntar_px), np.uint8))
    n, rot, stats, cent = cv2.connectedComponentsWithStats(grosso)
    comps = [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] >= area_min]
    if len(comps) != len(nomes):
        raise SystemExit(f"{folha.name}: achei {len(comps)} objetos, esperava {len(nomes)} "
                         f"(areas {[int(stats[i, 4]) for i in comps]})")
    # ordem de leitura: linhas por centro y (tolerância de 1/2 altura média), depois x
    alt = np.median([stats[i, cv2.CC_STAT_HEIGHT] for i in comps])
    comps.sort(key=lambda i: (round(cent[i][1] / (alt * 0.9)), cent[i][0]))
    out = {}
    for nome, i in zip(nomes, comps):
        x, y, w, h = stats[i, :4]
        p = 8
        x0, y0, x1, y1 = max(x - p, 0), max(y - p, 0), min(x + w + p, rgb.shape[1]), min(y + h + p, rgb.shape[0])
        alfa = ((rot[y0:y1, x0:x1] == i) & (m[y0:y1, x0:x1] > 0)).astype(np.float32)
        alfa = cv2.GaussianBlur(alfa, (3, 3), 0.8)
        out[nome] = (rgb[y0:y1, x0:x1].copy(), alfa)
    return out


# ---------------------------------------------------------------- estética

def reticula(rgb: np.ndarray, celula: int = 7, satur: float = 0.8, forca: float = 0.55) -> np.ndarray:
    """Retícula de revista: pontos a 45° com raio pela escuridão, multiplicando a cor."""
    h, w = rgb.shape[:2]
    lum = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[..., 1] *= satur
    base = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB).astype(np.float32)
    base = base * 0.82 + CREME * 0.18  # papel por baixo da tinta
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u = (xx + yy) / np.sqrt(2) / celula
    v = (xx - yy) / np.sqrt(2) / celula
    du, dv = u - np.round(u), v - np.round(v)
    d = np.sqrt(du ** 2 + dv ** 2)  # 0 no centro da célula, ~0,7 no canto
    escuro = cv2.GaussianBlur(1 - lum, (0, 0), celula * 0.5)
    raio = np.sqrt(np.clip(escuro, 0, 1)) * 0.62
    ponto = np.clip((raio - d) * celula * 1.2 + 0.5, 0, 1)  # anti-aliased
    mult = 1 - forca * ponto[..., None]
    return np.clip(base * mult, 0, 255)


def ruido_suave(shape: tuple[int, int], escala: float, r: np.random.Generator) -> np.ndarray:
    h, w = shape
    pequeno = r.standard_normal((max(2, int(h / escala)), max(2, int(w / escala)))).astype(np.float32)
    grande = cv2.resize(pequeno, (w, h), interpolation=cv2.INTER_CUBIC)
    return grande / (np.abs(grande).max() + 1e-6)


def peca(rgb: np.ndarray, alfa: np.ndarray, nome: str, filete: int, com_reticula: bool = True) -> None:
    """Grava <nome>-b0..b2: objeto (retícula) + filete creme de borda irregular."""
    pad = filete * 2 + 6
    rgb = cv2.copyMakeBorder(rgb, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    alfa = cv2.copyMakeBorder(alfa, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    obj = reticula(rgb) if com_reticula else rgb.astype(np.float32)
    dentro = (alfa > 0.5).astype(np.uint8)
    dist_fora = cv2.distanceTransform(1 - dentro, cv2.DIST_L2, 5)
    for b in range(3):
        r = rng(f"{nome}#{b}")
        # borda de tesoura: raio do filete oscila em baixa frequência + picote fino
        raio = filete * (1 + 0.35 * ruido_suave(dentro.shape, 60, r) + 0.12 * ruido_suave(dentro.shape, 9, r))
        fil = np.clip(raio - dist_fora + 0.5, 0, 1)
        fil = np.maximum(fil, alfa)
        cor = CREME[None, None, :] * (1 - alfa[..., None]) + obj * alfa[..., None]
        rgba = np.dstack([np.clip(cor, 0, 255), fil * 255]).astype(np.uint8)
        ys, xs = np.where(fil > 0.02)
        rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        DEST.mkdir(parents=True, exist_ok=True)
        Image.fromarray(rgba, "RGBA").save(DEST / f"{nome}-b{b}.png", optimize=True)
    print(f"{nome:16s} {rgba.shape[1]}x{rgba.shape[0]}")


def foto_rasgada(arquivo: Path, nome: str, larg: int, recorte: tuple[float, float, float, float] | None = None,
                 margem: int = 18, com_reticula: bool = False) -> None:
    """Foto real como cópia impressa: retângulo com margem creme e borda rasgada."""
    im = ImageOps.exif_transpose(Image.open(arquivo)).convert("RGB")
    if recorte:
        W, H = im.size
        x0, y0, x1, y1 = recorte
        im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    im = im.resize((larg, int(im.height * larg / im.width)), Image.LANCZOS)
    rgb = np.array(im).astype(np.float32)
    if com_reticula:
        rgb = reticula(rgb.astype(np.uint8), celula=6, satur=0.85, forca=0.4)
    h, w = rgb.shape[:2]
    for b in range(3):
        r = rng(f"{nome}#{b}")
        H2, W2 = h + 2 * margem, w + 2 * margem
        tela = np.tile(CREME, (H2, W2, 1))
        tela[margem:margem + h, margem:margem + w] = rgb
        yy, xx = np.mgrid[0:H2, 0:W2]
        dist = np.minimum.reduce([xx, yy, W2 - 1 - xx, H2 - 1 - yy]).astype(np.float32)
        rasgo = 5 + 4 * ruido_suave((H2, W2), 40, r) + 2.5 * ruido_suave((H2, W2), 4, r)
        a = np.clip(dist - rasgo, 0, 1)
        rgba = np.dstack([tela, a * 255]).astype(np.uint8)
        DEST.mkdir(parents=True, exist_ok=True)
        Image.fromarray(rgba, "RGBA").save(DEST / f"{nome}-b{b}.png", optimize=True)
    print(f"{nome:16s} {w + 2 * margem}x{h + 2 * margem} (foto)")


def kraft(w: int = 1080, h: int = 1920) -> None:
    """Grão de papel para multiplicar sobre o campo de cor (cinza neutro ~128)."""
    r = rng("kraft")
    g = 0.5 * ruido_suave((h, w), 220, r) + 0.3 * ruido_suave((h, w), 30, r) + 0.2 * r.standard_normal((h, w)).astype(np.float32) * 0.6
    fibras = cv2.GaussianBlur(r.standard_normal((h, w)).astype(np.float32), (0, 0), sigmaX=6, sigmaY=0.6)
    v = 200 + 22 * g + 18 * fibras / (np.abs(fibras).max() + 1e-6)
    Image.fromarray(np.clip(v, 0, 255).astype(np.uint8), "L").save(DEST / "kraft.png", optimize=True)
    print("kraft.png")


def fitas() -> None:
    """Tiras de fita crepe: bege translúcido, pontas picotadas."""
    for b in range(3):
        r = rng(f"fita#{b}")
        w, h = 220, 58
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        ponta = 7 + 5 * ruido_suave((h, w), 6, r)
        a = np.clip(np.minimum(xx - ponta, (w - 1 - xx) - ponta) + 0.5, 0, 1)
        a *= np.clip(np.minimum(yy, h - 1 - yy) - 1, 0, 1)
        tex = 1 + 0.06 * ruido_suave((h, w), 3, r)
        cor = np.array([228, 214, 172], np.float32)[None, None] * tex[..., None]
        rgba = np.dstack([np.clip(cor, 0, 255), a * 0.82 * 255]).astype(np.uint8)
        Image.fromarray(rgba, "RGBA").save(DEST / f"fita-b{b}.png", optimize=True)
    print("fita-b0..b2.png")


if __name__ == "__main__":
    import sys

    so = set(sys.argv[1:])

    def quer(k: str) -> bool:
        return not so or k in so

    if quer("folha1"):
        for nome, (rgb, a) in separar(BRUTOS / "motion06-folha1-xicara.png", ["xicara", "colher"],
                                      juntar_px=40, limiar=8).items():
            peca(rgb, convexo(a) if nome == "xicara" else a, nome, filete=12)
    if quer("folha2"):
        nomes = [f"grao-{i:02d}" for i in range(1, 11)] + ["grao-defeito"]
        for nome, (rgb, a) in separar(BRUTOS / "motion06-folha2-graos.png", nomes, juntar_px=30).items():
            peca(rgb, a, nome, filete=9)
    if quer("folha3"):
        for nome, (rgb, a) in separar(BRUTOS / "motion06-folha3-balanca.png", ["prato"], juntar_px=40).items():
            peca(rgb, a, nome, filete=12)
    if quer("folha4"):
        f4 = BRUTOS / "motion06-folha4-cerejas.png"
        if f4.exists():
            # o cacho fica à direita da linha do meio, então cai depois das amarelas
            nomes = ["cereja-verde-1", "cereja-verde-2", "cereja-verde-3",
                     "cereja-amarela-1", "cereja-amarela-2", "cereja-amarela-3", "cachinho",
                     "cereja-vermelha-1", "cereja-vermelha-2", "cereja-vermelha-3"]
            for nome, (rgb, a) in separar(f4, nomes, juntar_px=24, limiar=55).items():
                peca(rgb, a, nome, filete=9)
    if quer("folha5"):
        for nome, (rgb, a) in separar(BRUTOS / "motion06-folha5-peneira.png", ["peneira", "torrado"], juntar_px=40).items():
            peca(rgb, a, nome, filete=12)
    if quer("fotos"):
        foto_rasgada(FONTE / "lavoura-rua.jpg", "foto-lavoura-rua", 1080)
        foto_rasgada(FONTE / "lavoura-ceu.jpg", "foto-lavoura-ceu", 1100)
        foto_rasgada(FONTE / "cafeeiro.jpg", "foto-cafeeiro", 560, recorte=(0.0, 0.0, 1.0, 1.0))
        foto_rasgada(FONTE / "cereja-verde.jpg", "foto-cereja-verde", 620, recorte=(0.05, 0.1, 0.95, 0.75))
    if quer("textura"):
        DEST.mkdir(parents=True, exist_ok=True)
        kraft()
        fitas()
