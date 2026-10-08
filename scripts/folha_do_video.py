"""Folha de contato tirada do MP4 FINAL, por número de quadro.

    python scripts/folha_do_video.py <video.mp4> <saida.png> <q1,q2,...> [colunas]

O `contato.mjs` renderiza stills pelo Remotion — serve antes do render. Esta folha lê o
arquivo que vai ao ar, depois do encode: é a que prova o chicote (pegue dois quadros
DENTRO de cada janela, q-2 e q+1 da troca) e o que a normalização não mexeu no vídeo.
Cada célula leva o quadro e o segundo escritos em cima.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

W, H = 216, 384


def ffmpeg() -> str:
    raiz = os.path.join(os.path.dirname(__file__), "..", "instagram", "remotion", "node_modules", "@remotion")
    for d in os.listdir(raiz) if os.path.isdir(raiz) else []:
        c = os.path.join(raiz, d, "ffmpeg.exe")
        if d.startswith("compositor") and os.path.exists(c):
            return os.path.abspath(c)
    return "ffmpeg"


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    video, saida = sys.argv[1], sys.argv[2]
    quadros = [int(q) for q in sys.argv[3].split(",")]
    cols = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    imgs = []
    with tempfile.TemporaryDirectory() as d:
        for q in quadros:
            out = os.path.join(d, f"{q}.png")
            # meio do quadro, para o seek não cair no vizinho
            subprocess.run([ffmpeg(), "-v", "error", "-y", "-ss", f"{(q + 0.5) / 30:.4f}", "-i", video,
                            "-frames:v", "1", "-vf", f"scale={W}:{H}", out], check=True)
            imgs.append((q, Image.open(out).convert("RGB")))
    linhas = (len(imgs) + cols - 1) // cols
    folha = Image.new("RGB", (cols * (W + 4), linhas * (H + 22)), (30, 30, 30))
    d = ImageDraw.Draw(folha)
    for k, (q, im) in enumerate(imgs):
        x, y = (k % cols) * (W + 4), (k // cols) * (H + 22)
        folha.paste(im, (x, y + 20))
        d.text((x + 4, y + 4), f"q{q}  {q / 30:.2f}s", fill=(255, 255, 255))
    folha.save(saida)
    print(saida)


if __name__ == "__main__":
    main()
