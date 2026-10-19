"""Peça 09: takes dos três criadores, recortados e prontos para o Remotion.

Cada take sai do reel original (raspagem/_jeitinho-cafe, gitignored) com o recorte que tira
a legenda queimada e o pacote da Veroo (medidos em raspagem/_jeitinho-cafe/medir/grade.jpg;
tempos em projetos/09-jeitinho-cafe/decupagem.md). Destino: public/fonte/clipes (gitignored),
30 fps, sem áudio. As durações medidas vão para clipes.json, que a peça lê.

    python -m uv run python scripts/jeitinho_clipes.py
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

SRC = Path("raspagem/_jeitinho-cafe")
DEST = Path("instagram/remotion/projetos/09-jeitinho-cafe/public/fonte/clipes")
JSON = Path("instagram/remotion/projetos/09-jeitinho-cafe/clipes.json")

# recortes em fração do quadro (x0, y0, x1, y1)
# Fábio: legenda a ~0,76 da altura; a Veroo fica à direita (de ~0,72 a ~0,86 conforme o take).
# Cada take tem o recorte CENTRADO NA AÇÃO (coador, tangerina, copo), medido no quadro com grade
# (raspagem/_jeitinho-cafe/tmpf/origs.png): o recorte único x 0–0,70 cortava o copo do f4 na borda.
FABIO = (0.0, 0.06, 0.70, 0.70)
PAULO = (0.08, 0.08, 0.92, 0.84)       # limpo; mesma proporção de cartão do Fábio
PAULO_ROSTO = (0.0, 0.12, 1.0, 0.60)   # etiqueta de perfil do IG a ~0,63
GABRIEL = (0.04, 0.05, 0.96, 0.585)    # legenda a ~0,61–0,64, na altura das mãos
# o "aperta" precisa mostrar o aparelho: recorte alto, e a legenda dele (a ~0,76 deste
# recorte) fica embaixo da etiqueta APERTA desenhada na cena
GABRIEL_ALTO = (0.04, 0.05, 0.96, 0.80)

# Giuseppe: a legenda queimada dele fica a ~0,78–0,88 da altura em todos os takes (medido em
# raspagem/_jeitinho-cafe/tmpf/gq.png); o recorte para em 0,74.
GIUSEPPE = (0.0, 0.04, 1.0, 0.74)

# nome → (arquivo, início, fim, recorte)
TAKES = {
    "f0": ("fabio_DdOzPnzuRz4", 0.0, 2.0, (0.06, 0.255, 0.74, 0.74)),  # rala (abertura dele): corte abaixo do título "CAFÉ CÍTRICO"
    "f1": ("fabio_DdOzPnzuRz4", 7.5, 10.6, (0.20, 0.28, 0.70, 0.74)),    # tangerina sobre o pó e na mão ("congelada")
    "f2": ("fabio_DdOzPnzuRz4", 11.0, 13.4, (0.10, 0.06, 0.80, 0.70)),   # rala sobre o pó
    "f3": ("fabio_DdOzPnzuRz4", 16.3, 21.2, (0.03, 0.06, 0.73, 0.70)),   # água sobre a tangerina
    "f4": ("fabio_DdOzPnzuRz4", 24.4, 27.0, (0.12, 0.06, 0.82, 0.72)),   # serve no copo, a cor
    "p1": ("paulo_DaS9xiXuVZ6", 6.6, 8.6, PAULO),     # paçoquitas na tigela
    "p2": ("paulo_DaS9xiXuVZ6", 9.0, 9.95, PAULO),    # esfarelada
    "p3": ("paulo_DaS9xiXuVZ6", 12.4, 13.25, PAULO),  # leite em pó
    "p3b": ("paulo_DaS9xiXuVZ6", 13.95, 14.9, PAULO), # creme de leite (depois que o rótulo "Creme de leite" sai)
    "p4": ("paulo_DaS9xiXuVZ6", 15.6, 18.0, PAULO),   # vira pasta
    "p5": ("paulo_DaS9xiXuVZ6", 21.8, 24.0, PAULO),   # café despejado sobre a pasta
    "p6": ("paulo_DaS9xiXuVZ6", 24.0, 26.3, PAULO),   # copo pronto
    "p7": ("paulo_DaS9xiXuVZ6", 28.0, 29.9, PAULO_ROSTO),  # Paulo prova
    # o terceiro criador agora é o Giuseppe (o Gabriel usava prensa, não "na mão" — erro de leitura
    # apontado pelo cliente em 15/10/2026); os takes g* ficam só no histórico
    "gi0": ("giuseppe_DYUvyf1MRcV", 12.0, 13.9, GIUSEPPE),  # ele falando ("sou italiano")
    "gi1": ("giuseppe_DYUvyf1MRcV", 3.0, 4.8, GIUSEPPE),    # o creme pronto, colher puxando
    "gi2": ("giuseppe_DYUvyf1MRcV", 28.0, 29.2, GIUSEPPE),  # bate o mel
    "gi3": ("giuseppe_DYUvyf1MRcV", 33.9, 35.4, GIUSEPPE),  # joga o café solúvel
    "gi4": ("giuseppe_DYUvyf1MRcV", 36.6, 38.2, GIUSEPPE),  # água quente
    "gi5": ("giuseppe_DYUvyf1MRcV", 39.0, 40.4, GIUSEPPE),  # liga a batedeira
    "gi6": ("giuseppe_DYUvyf1MRcV", 47.6, 49.0, GIUSEPPE),  # vira creme
    "gi7": ("giuseppe_DYUvyf1MRcV", 65.6, 68.4, GIUSEPPE),  # come de colher
    "g0": ("pirados_DeKAxH5gwKH", 8.8, 10.8, GABRIEL),  # mostra o aparelho na mão
    "g1": ("pirados_DeKAxH5gwKH", 21.9, 23.6, GABRIEL),  # pó
    "g2": ("pirados_DeKAxH5gwKH", 24.0, 24.9, GABRIEL),  # água quente
    "g3": ("pirados_DeKAxH5gwKH", 25.9, 26.9, GABRIEL),  # mexe
    "g4": ("pirados_DeKAxH5gwKH", 27.0, 28.4, GABRIEL),  # tampa
    "g5": ("pirados_DeKAxH5gwKH", 0.4, 2.4, GABRIEL_ALTO),  # aperta: legenda tapada pela etiqueta na cena
}


def sonda(p: Path) -> tuple[int, int]:
    s = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True, check=True).stdout.strip()
    w, h = s.split(",")
    return int(w), int(h)


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    medidas = {}
    for nome, (arq, a, b, (x0, y0, x1, y1)) in TAKES.items():
        src = SRC / f"{arq}.mp4"
        w, h = sonda(src)
        cw, ch = int((x1 - x0) * w) // 2 * 2, int((y1 - y0) * h) // 2 * 2
        cx, cy = int(x0 * w), int(y0 * h)
        out = DEST / f"{nome}.mp4"
        larg = min(1080, cw) // 2 * 2
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", f"{b - a:.3f}", "-i", str(src), "-an",
                        "-vf", f"crop={cw}:{ch}:{cx}:{cy},scale={larg}:-2,fps=30",
                        "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", str(out)], check=True)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                                   capture_output=True, text=True, check=True).stdout)
        ow, oh = sonda(out)
        medidas[nome] = {"duracao": round(dur, 3), "largura": ow, "altura": oh, "razao": round(ow / oh, 4)}
        print(f"{nome}: {ow}x{oh} {dur:.2f}s")
    # abertura: o vídeo cru do Rafael, inteiro, e o áudio ambiente dele à parte
    ab = SRC / "gancho_rafael.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ab), "-an", "-vf", "scale=1080:1920,fps=30", "-c:v", "libx264",
                    "-crf", "17", "-pix_fmt", "yuv420p", str(DEST / "abertura.mp4")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ab), "-vn", "-ac", "2", "-ar", "48000",
                    str(DEST.parent / "abertura-ambiente.wav")], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(DEST / "abertura.mp4")], capture_output=True, text=True, check=True).stdout)
    medidas["abertura"] = {"duracao": round(dur, 3), "largura": 1080, "altura": 1920, "razao": 0.5625}
    JSON.write_text(json.dumps(medidas, indent=2), encoding="utf-8")
    print("abertura:", dur)


if __name__ == "__main__":
    main()
