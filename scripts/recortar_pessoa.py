"""Recorta a pessoa de um vídeo quadro a quadro (PNG com alfa), para a câmera 3D do reel falado.

    python -I scripts/recortar_pessoa.py <video.mp4> <pasta_saida> <q0> <q1> [--grade "<filtro ffmpeg>"]
        [--ss <segundo do 1º quadro no vídeo>]

Grava `<pasta_saida>/<qqqqq>.png` de q0 a q1 (numeração do quadro da PEÇA). Por padrão o quadro q sai
do segundo q/30 do vídeo; para estender o fim de uma peça com quadros do BRUTO, passe `--ss` (o segundo
do bruto que corresponde a q0, de `saida/sync-v3.json`) e o mesmo `--grade` da peça (`cor-grade.txt`).
Confira a emenda: o quadro novo contra o último antigo deve dar erro médio de ~2/255.

Máscara `u2net_human_seg` (rembg; lição 71: isnet e birefnet perderam), média ponderada com os
vizinhos (0,25/0,5/0,25) para a borda não tremer, e desfoque de 1,2 px. Nunca grava por cima de
um quadro que já existe (a pasta `public/` é intocável: só se acrescenta).
Venv `~/.cache/rbg`.
"""
from __future__ import annotations

import argparse
import glob
import os
import subprocess
import tempfile

import numpy as np
from PIL import Image, ImageFilter
from rembg import new_session, remove


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('video')
    ap.add_argument('saida')
    ap.add_argument('q0', type=int)
    ap.add_argument('q1', type=int)
    ap.add_argument('--grade', default='')
    ap.add_argument('--ss', type=float, default=None)
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    tmp = tempfile.mkdtemp()
    # um quadro de folga de cada lado, para a média temporal das bordas
    q0 = max(0, a.q0 - 1)
    ss = (a.ss - (a.q0 - q0) / 30) if a.ss is not None else q0 / 30
    vf = ['-vf', a.grade] if a.grade else []
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{ss:.4f}', '-i', a.video, '-frames:v', str(a.q1 - q0 + 2), *vf,
                    '-start_number', str(q0), os.path.join(tmp, '%05d.png')], check=True)
    s = new_session('u2net_human_seg')
    masks = {}
    for f in sorted(glob.glob(os.path.join(tmp, '*.png'))):
        q = int(os.path.basename(f)[:5])
        masks[q] = np.asarray(remove(Image.open(f), session=s, only_mask=True, post_process_mask=True)).astype(np.float32)
        if q % 25 == 0:
            print('quadro', q, flush=True)
    qs = sorted(masks)
    n = 0
    for i, q in enumerate(qs):
        if q < a.q0 or q > a.q1:
            continue
        viz = [masks[qs[j]] for j in range(max(0, i - 1), min(len(qs), i + 2))]
        w = [0.25, 0.5, 0.25] if len(viz) == 3 else [0.5, 0.5]
        m = Image.fromarray(np.clip(sum(x * y for x, y in zip(viz, w)), 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
        rgb = Image.open(os.path.join(tmp, f'{q:05d}.png')).convert('RGB')
        rgb.putalpha(m)
        dest = os.path.join(a.saida, f'{q:05d}.png')
        if os.path.exists(dest):
            raise SystemExit(f'já existe, não sobrescrevo: {dest}')
        rgb.save(dest)
        n += 1
    print('FIM', n)


if __name__ == '__main__':
    main()
