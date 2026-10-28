"""Voz e palavras de um corte seco no relógio da IMAGEM (reel falado, peça 10 em diante).

    python -I scripts/sincronizar_voz_corte.py <projeto> <fim_s> [--bruto public/fonte/IMG_1128.MP4]
        [--corte saida/corte-seco-v2.mp4] [--trechos saida/corte-seco-v2.json]
        [--palavras palavras-v2.json] [--palavras-bruto palavras-IMG_1128.json]

POR QUE EXISTE (lição 77): na peça 10 havia três relógios. A imagem do corte seco; a `voz.wav`, que
ia atrasando até 0,47 s no fim (esticada 0,76%), e cortava a última palavra; e o `palavras-v2.json`,
que ia adiantando até 0,23 s. Legenda, texto e som liam as palavras, então tudo saía fora da boca.

O que faz, trecho a trecho do corte (`trechos` = o json do corte seco: saida_ini, i, dur):
  1. mede o deslocamento bruto−saída pela IMAGEM (3 quadros do corte contra o bruto, ±0,5 s);
  2. refina pelo áudio do próprio corte (que está colado na imagem), ±60 ms, se a correlação passar
     de 0,6; o menor dos dois deixa a voz no máximo 1 quadro ATRASADA, nunca adiantada;
  3. monta `public/fonte/voz-sync.wav` cortando o BRUTO nesses pontos (48 kHz, rampa de 4 ms nas
     emendas). O último trecho vai até `fim_s`: estenda além do corte para a última palavra respirar;
  4. relê cada palavra no whisper do bruto e grava `palavras-v3.json` no mesmo relógio;
  5. grava `saida/sync-v3.json` (deslocamento por trecho) para estender quadros do fim, se preciso.

Confira depois no MP4 FINAL (lição 72): correlação da voz do reel contra o áudio do corte.
Rode com o Python do venv `~/.cache/rbg` (numpy).
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import subprocess
import unicodedata
import wave

import numpy as np

SR = 48000


def aud(src: str, ss: float, t: float, sr: int = 8000, ch: int = 1) -> np.ndarray:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{ss:.4f}', '-t', f'{t:.4f}', '-i', src, '-map', '0:a:0',
                          '-ac', str(ch), '-ar', str(sr), '-f', 's16le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32)
    return a.reshape(-1, ch) if ch > 1 else a


def vid(src: str, ss: float, t: float) -> np.ndarray:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{ss:.4f}', '-t', f'{t:.4f}', '-i', src,
                          '-vf', 'scale=72:128,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 128, 72).astype(np.float32)


def deslocamentos(bruto: str, corte: str, segs: list[dict], ini: list[float], fim_corte: float) -> list[float]:
    out = []
    for k, s in enumerate(segs):
        a, b = ini[k], min(ini[k + 1], fim_corte)
        t = a + 0.05
        L = max(0.2, b - a - 0.1)
        g = s['i'] - s['saida_ini']
        BV = vid(bruto, t + g - 0.5, L + 1.0)
        cand = []
        for f in np.linspace(0, L - 0.05, 3):
            v = vid(corte, t + f, 0.04)[0]
            cand.append(t + g - 0.5 + int(np.argmin([np.abs(v - x).mean() for x in BV])) / 30 - (t + f))
        sv = float(np.median(cand))
        c = aud(corte, t, L)
        BA = aud(bruto, t + sv - 0.06, L + 0.12)
        sc = [np.dot(c, BA[d:d + len(c)]) / (np.linalg.norm(BA[d:d + len(c)]) * np.linalg.norm(c) + 1) for d in range(0, len(BA) - len(c), 2)]
        kk = int(np.argmax(sc))
        sa = sv - 0.06 + kk * 2 / 8000
        sh = min(sa, sv) if sc[kk] > 0.6 else sv
        out.append(sh)
        print(f'{a:6.2f}  json {g:.3f}  imagem {sv:.3f}  audio {sa:.3f} (r {sc[kk]:.2f})  usa {sh:.3f}')
    return out


def montar_voz(bruto: str, ini: list[float], desl: list[float], dest: str) -> None:
    partes = []
    for k in range(len(desl)):
        n = int(round(ini[k + 1] * SR)) - int(round(ini[k] * SR))
        x = aud(bruto, ini[k] + desl[k], n / SR + 0.05, SR, 2)[:n]
        if len(x) < n:
            x = np.vstack([x, np.zeros((n - len(x), 2), np.float32)])
        r = int(0.004 * SR)
        env = np.ones(n)
        env[:r] = np.linspace(0, 1, r)
        env[-r:] = np.linspace(1, 0, r)
        partes.append(x * env[:, None])
    y = np.clip(np.vstack(partes), -32768, 32767).astype(np.int16)
    with wave.open(dest, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(y.tobytes())
    print(dest, len(y) / SR, 's')


def norm(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD', s.lower()) if c.isalnum())


def remapear_palavras(v2: list[dict], bruto: list[dict], ini: list[float], desl: list[float]) -> list[dict]:
    cand = []
    for k, d in enumerate(desl):
        a, z = ini[k] + d, ini[k + 1] + d
        for w in bruto:
            if a - 0.05 <= w['i'] < z - 0.02:
                cand.append({'t': norm(w['p']), 'i': w['i'] - d, 'f': min(w['f'] - d, ini[k + 1])})
    sm = difflib.SequenceMatcher(None, [norm(w['texto']) for w in v2], [c['t'] for c in cand], autojunk=False)
    par = {bl.a + j: cand[bl.b + j] for bl in sm.get_matching_blocks() for j in range(bl.size)}
    out = [{**w, 'inicio': round(par[n]['i'], 3), 'fim': round(par[n]['f'], 3)} if n in par else dict(w) for n, w in enumerate(v2)]
    faltou = [n for n in range(len(v2)) if n not in par]
    for n in faltou:  # herda o deslocamento da vizinha casada mais próxima
        viz = min(par, key=lambda m: abs(m - n))
        d = par[viz]['i'] - v2[viz]['inicio']
        out[n]['inicio'] = round(v2[n]['inicio'] + d, 3)
        out[n]['fim'] = round(v2[n]['fim'] + d, 3)
    for n in range(1, len(out)):
        out[n]['inicio'] = max(out[n]['inicio'], out[n - 1]['inicio'])
    print('palavras casadas', len(par), 'de', len(v2), '| sem par:', [v2[n]['texto'] for n in faltou])
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('projeto')
    ap.add_argument('fim', type=float)
    ap.add_argument('--bruto', default='public/fonte/IMG_1128.MP4')
    ap.add_argument('--corte', default='saida/corte-seco-v2.mp4')
    ap.add_argument('--trechos', default='saida/corte-seco-v2.json')
    ap.add_argument('--palavras', default='palavras-v2.json')
    ap.add_argument('--palavras-bruto', default='palavras-IMG_1128.json')
    a = ap.parse_args()
    os.chdir(a.projeto)
    segs = json.load(open(a.trechos, encoding='utf-8'))
    ini = [s['saida_ini'] for s in segs] + [a.fim]
    fim_corte = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.corte],
                                     capture_output=True, text=True).stdout)
    desl = deslocamentos(a.bruto, a.corte, segs, ini, fim_corte)
    montar_voz(a.bruto, ini, desl, 'public/fonte/voz-sync.wav')
    json.dump([{'saida_ini': ini[k], 'desloc': desl[k]} for k in range(len(segs))], open('saida/sync-v3.json', 'w'), indent=1)
    v3 = remapear_palavras(json.load(open(a.palavras, encoding='utf-8')), json.load(open(a.palavras_bruto, encoding='utf-8')), ini, desl)
    json.dump(v3, open('palavras-v3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
