"""Revisão quadro a quadro de um motion narrado: cada célula da folha leva o tempo e a
palavra que a VOZ está dizendo naquele quadro (de palavras.json), para conferir texto ×
fala e corte × fala com o olho, e não pelo código.

    python scripts/revisar_sincronia.py <reel.mp4> <palavras.json> <saida_dir> [--qps 6] [--deslocamento 3.0]
        [--de 0] [--ate 999] [--por-folha 48]

`--deslocamento` é o segundo da peça em que a narração começa (a abertura sem voz).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mp4")
    ap.add_argument("palavras")
    ap.add_argument("saida")
    ap.add_argument("--qps", type=float, default=6)
    ap.add_argument("--deslocamento", type=float, default=0.0)
    ap.add_argument("--de", type=float, default=0.0)
    ap.add_argument("--ate", type=float, default=999.0)
    ap.add_argument("--por-folha", type=int, default=48)
    a = ap.parse_args()
    pal = json.loads(Path(a.palavras).read_text(encoding="utf-8"))
    for p in pal:
        p["inicio"] += a.deslocamento
        p["fim"] += a.deslocamento
    out = Path(a.saida)
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a.de), "-to", str(a.ate), "-i", a.mp4,
                        "-vf", f"fps={a.qps},scale=216:-2", f"{tmp}/q_%05d.png"], check=True)
        quadros = sorted(Path(tmp).glob("q_*.png"))
        fonte = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 17)
        cols = 8
        for f0 in range(0, len(quadros), a.por_folha):
            lote = quadros[f0:f0 + a.por_folha]
            w, h = Image.open(lote[0]).size
            rows = (len(lote) + cols - 1) // cols
            folha = Image.new("RGB", (cols * w, rows * (h + 24)), "black")
            d = ImageDraw.Draw(folha)
            for k, q in enumerate(lote):
                t = a.de + (f0 + k) / a.qps
                fala = next((p["texto"] for p in pal if p["inicio"] <= t < p["fim"]), "·")
                x, y = (k % cols) * w, (k // cols) * (h + 24)
                folha.paste(Image.open(q), (x, y + 24))
                d.text((x + 3, y + 3), f"{t:05.2f} {fala}", fill="yellow", font=fonte)
            nome = out / f"sinc_{a.de + f0 / a.qps:05.1f}.png"
            folha.save(nome)
            print(nome)


if __name__ == "__main__":
    main()
