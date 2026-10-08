"""Varre um MP4 renderizado procurando salto de movimento que ninguém pediu.

    python scripts/varrer_movimento.py <video.mp4> [quadros,conhecidos,...]

Extrai os quadros em baixa resolução (cinza 135x240) e mede, quadro a quadro:
  - MAD: diferença média absoluta para o quadro anterior (conteúdo que muda de uma vez);
  - deslocamento global por correlação de fase (a câmera que pula).
Lista o que acontece LONGE (> 7 quadros) das trocas conhecidas — chicotes, coberturas,
batidas com tremor — que se passam como segundo argumento.

Como ler: movimento rápido intencional (foco num defeito, panorâmica do mural, mergulho
no selo) aparece como sequência de picos de MAD; isso é esperado. O que importa é a
segunda lista, "saltos isolados": a câmera andou muito num quadro e os vizinhos ficaram
parados. Na peça 07 ela saiu vazia — é o resultado que se quer.

Usa o ffmpeg do Remotion (`instagram/remotion/node_modules/@remotion/compositor-*`).
"""

from __future__ import annotations

import glob
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image


def ffmpeg() -> str:
    raiz = os.path.join(os.path.dirname(__file__), "..", "instagram", "remotion", "node_modules", "@remotion")
    for d in os.listdir(raiz) if os.path.isdir(raiz) else []:
        c = os.path.join(raiz, d, "ffmpeg.exe")
        if d.startswith("compositor") and os.path.exists(c):
            return os.path.abspath(c)
    return "ffmpeg"


def desloc(a: np.ndarray, b: np.ndarray) -> tuple[int, int]:
    A = np.fft.fft2(a - a.mean())
    B = np.fft.fft2(b - b.mean())
    R = A * np.conj(B)
    R /= np.abs(R) + 1e-9
    r = np.fft.ifft2(R).real
    y, x = np.unravel_index(np.argmax(r), r.shape)
    if y > a.shape[0] // 2:
        y -= a.shape[0]
    if x > a.shape[1] // 2:
        x -= a.shape[1]
    return x * 8, y * 8  # em pixel do quadro 1080x1920


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    video = sys.argv[1]
    conhecidos = [int(q) for q in sys.argv[2].split(",")] if len(sys.argv) > 2 else []
    with tempfile.TemporaryDirectory() as d:
        subprocess.run([ffmpeg(), "-v", "error", "-i", video, "-vf", "scale=135:240", os.path.join(d, "q%05d.png")], check=True)
        Q = [np.asarray(Image.open(a).convert("L"), dtype=np.float32) for a in sorted(glob.glob(os.path.join(d, "*.png")))]
    print(f"{len(Q)} quadros")
    mad = np.array([np.abs(Q[k] - Q[k - 1]).mean() for k in range(1, len(Q))])
    dv = np.array([desloc(Q[k], Q[k - 1]) for k in range(1, len(Q))], dtype=float)

    def perto(q: int) -> bool:
        return any(abs(q - c) <= 7 for c in conhecidos)

    med = float(np.median(mad))
    print(f"MAD mediana {med:.2f} · p95 {np.percentile(mad, 95):.2f} · máx {mad.max():.2f}")
    print("picos de MAD longe das trocas conhecidas (quadro, s, MAD) — movimento rápido intencional também cai aqui:")
    for k in range(len(mad)):
        if mad[k] > max(6 * med, 4.0) and not perto(k + 1):
            print(f"  q{k + 1:5d}  {(k + 1) / 30:6.2f}s  {mad[k]:6.2f}")
    print("saltos de câmera isolados (quadro, s, dx, dy) — aqui tem que sair vazio:")
    n = 0
    for k in range(1, len(dv) - 1):
        m = np.hypot(*dv[k])
        viz = max(np.hypot(*dv[k - 1]), np.hypot(*dv[k + 1]))
        if m >= 40 and m > 3 * (viz + 8) and not perto(k + 1):
            n += 1
            print(f"  q{k + 1:5d}  {(k + 1) / 30:6.2f}s  dx {dv[k][0]:+.0f} dy {dv[k][1]:+.0f}  (vizinhos {viz:.0f})")
    print(f"  {n} salto(s)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
