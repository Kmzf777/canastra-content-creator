"""Som da peça 08 (cópia do script da 07; seções: início → "Fruta, semente" groove · respiro abafado até "Esse aqui nasceu" · groove · fecho em "E amanhã")

Som da peça 07: efeitos de colagem e uma trilha em seções cravadas na narração.

As referências do @_victorzk põem um som em CADA entrada (papel, carimbo, caneta,
pop) e trocam o clima da trilha na virada. Aqui tudo é sintetizado com semente fixa
(rodar duas vezes dá os mesmos bytes). As seções da trilha começam em FRASES da
narração, lidas de `<PROJ>/palavras.json` — nenhum segundo digitado (lição 56):

    início → "Calma"              tensão: zumbido grave + batimento   ("Até um por cento…")
    "Calma" → "E aqui vem"        groove lo-fi 88 BPM
    "E aqui vem" → "Por isso"     respiro: sem bateria, abafado       ("o que quase ninguém conta")
    "Por isso" → "Salva esse"     groove de volta                     (a fazenda)
    "Salva esse" → FIM            fecho; FIM = última palavra + 0,5 s, a mesma regra do roteiro.ts

Peça nova: copie, troque `PROJ` e as frases em `trilha()`.

    python -m uv run python scripts/colagem_sfx_v2.py
"""

from __future__ import annotations

import json
import math
import re
import sys
import unicodedata
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from colagem_sfx import SR, banda, ding, env, norm, pop, rasgo, slide, t, thump, tick, tink, whoosh  # noqa: E402
from colagem_sfx import carimbo as carimbo_v1  # noqa: E402

RNG = np.random.default_rng(20261007 + 7)
PROJ = Path("instagram/remotion/projetos/08b-onze-etapas")
DEST = PROJ / "public" / "sfx"
PALAVRAS = json.loads((PROJ / "palavras.json").read_text(encoding="utf-8"))
DUR = math.ceil((PALAVRAS[-1]["fim"] + 0.5) * 10) / 10


def _chave(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())


def inicio_de(trecho: str) -> float:
    """Início (s) da primeira ocorrência da frase na narração. Lança se não achar."""
    alvo = [_chave(w) for w in trecho.split()]
    chaves = [_chave(p["texto"]) for p in PALAVRAS]
    for i in range(len(chaves) - len(alvo) + 1):
        if chaves[i:i + len(alvo)] == alvo:
            return PALAVRAS[i]["inicio"]
    raise SystemExit(f'frase "{trecho}" não está em {PROJ}/palavras.json')
BPM = 88
BATIDA = 60 / BPM


def ruido(d: float) -> np.ndarray:
    return RNG.standard_normal(int(d * SR))


def salvar(nome: str, x: np.ndarray, estereo: bool = False) -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(DEST / f"{nome}.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"{nome}.wav  {len(x) / SR:5.2f} s")


# ------------------------------------------------------------------ efeitos novos

def batimento() -> np.ndarray:
    a = thump()[: int(0.32 * SR)] * 0.9
    b = thump()[: int(0.32 * SR)] * 0.6
    out = np.zeros(int(0.75 * SR))
    out[: len(a)] += a
    k = int(0.22 * SR)
    out[k: k + len(b)] += b
    return norm(banda(out, 25, 400), 0.85)


def rabisco() -> np.ndarray:
    d = 0.38
    n = banda(ruido(d), 1500, 7000)
    zig = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 11 * t(d)))
    return norm(n * zig * env(d, 0.01, 0.2), 0.35)


def fita() -> np.ndarray:
    d = 0.32
    n = ruido(d)
    estalos = (RNG.random(len(n)) < 0.02) * RNG.standard_normal(len(n)) * 5
    e = np.interp(t(d), [0, 0.02, 0.25, d], [0, 1, 0.6, 0])
    return norm(banda(n + estalos, 2000, 11000) * e, 0.45)


def digitacao(n: int = 9, intervalo: float = 1 / 30) -> np.ndarray:
    out = np.zeros(int((n * intervalo + 0.2) * SR))
    for k in range(n):
        c = banda(ruido(0.03), 1800, 8000) * env(0.03, 0.0005, 0.006)
        corpo = np.sin(2 * np.pi * (180 + RNG.random() * 60) * t(0.03)) * env(0.03, 0.0005, 0.01) * 0.5
        i = int(k * intervalo * SR * (1 + (RNG.random() - 0.5) * 0.2))
        out[i: i + len(c)] += c + corpo
    return norm(out, 0.4)


def golinho() -> np.ndarray:
    d = 0.6
    n = ruido(d)
    out = np.zeros_like(n)
    blocos = 12
    tam = len(n) // blocos
    for i in range(blocos):
        c = 600 + 2200 * (i / blocos)
        out[i * tam:(i + 1) * tam] = banda(n, c * 0.6, c * 1.4)[i * tam:(i + 1) * tam]
    turb = 0.6 + 0.4 * np.sin(2 * np.pi * 23 * t(d)) ** 2
    e = np.interp(t(d), [0, 0.05, 0.45, d], [0, 1, 0.8, 0])
    return norm(out * turb * e, 0.4)


def graos(n: int = 26, dur: float = 0.7) -> np.ndarray:
    out = np.zeros(int((dur + 0.1) * SR))
    for _ in range(n):
        i = int(RNG.random() ** 1.6 * dur * SR)
        f = 1800 + RNG.random() * 3500
        c = np.sin(2 * np.pi * f * t(0.02)) * env(0.02, 0.0003, 0.004) * (0.3 + RNG.random() * 0.7)
        out[i: i + len(c)] += c
    return norm(out, 0.5)


def brilho() -> np.ndarray:
    d = 0.7
    tt = t(d)
    s = np.zeros_like(tt)
    for k, f in enumerate([2349, 2793, 3136, 3729, 4699]):
        a0 = k * 0.05
        e = np.clip((tt - a0) / 0.005, 0, 1) * np.exp(-np.maximum(tt - a0, 0) / 0.18)
        s += np.sin(2 * np.pi * f * tt) * e * 0.4
    return norm(s + banda(ruido(d), 6000, 14000) * env(d, 0.01, 0.15) * 0.15, 0.32)


def chicote() -> np.ndarray:
    w = whoosh()
    k = int(0.36 * SR)
    return norm(w[len(w) // 2 - k // 2: len(w) // 2 + k // 2] * np.hanning(k), 0.6)


def drone(d: float = 6.3) -> np.ndarray:
    tt = t(d)
    s = sum(np.sin(2 * np.pi * f * tt + RNG.random() * 6) * a for f, a in [(41.2, 1), (55, 0.6), (61.7, 0.35), (82.4, 0.25)])
    ronco = banda(ruido(d), 30, 220) * 0.5
    trem = 0.75 + 0.25 * np.sin(2 * np.pi * 0.35 * tt)
    e = np.interp(tt, [0, 0.8, d - 0.6, d], [0.35, 1, 1, 0])
    return norm((s + ronco) * trem * e, 0.75)


# ------------------------------------------------------------------ trilha

NOTAS = {"D3": 146.83, "F#3": 185.0, "A3": 220.0, "C#4": 277.18, "B2": 123.47, "D4": 293.66, "F#4": 369.99,
         "G2": 98.0, "B3": 246.94, "A2": 110.0, "E3": 164.81, "G3": 196.0, "C#3": 138.59, "E4": 329.63}
ACORDES = [  # Dmaj7 · Bm7 · Gmaj7 · A7 — um compasso cada
    ("D2", ["D3", "F#3", "A3", "C#4"]), ("B1", ["B2", "D3", "F#3", "A3"]),
    ("G1", ["G2", "B2", "D3", "F#3"]), ("A1", ["A2", "C#3", "E3", "G3"]),
]
BAIXO = {"D2": 73.42, "B1": 61.74, "G1": 49.0, "A1": 55.0}


def rhodes(f: float, d: float) -> np.ndarray:
    tt = t(d)
    s = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt / 0.4) + 0.12 * np.sin(2 * np.pi * 3 * f * tt) * np.exp(-tt / 0.2)
    trem = 1 - 0.18 * (0.5 + 0.5 * np.sin(2 * np.pi * 4.2 * tt))
    return s * trem * np.exp(-tt / 2.2) * np.clip(tt / 0.006, 0, 1)


def trilha() -> np.ndarray:
    n = int(DUR * SR)
    mus = np.zeros(n)
    bat = np.zeros(n)
    ini, resp, volta, fim = (inicio_de("Esse punhado aqui"), inicio_de("E aqui vem o que"), inicio_de("Por isso, aqui"),
                             inicio_de("Manda esse vídeo"))
    compasso = 4 * BATIDA
    k = 0
    tc = ini
    while tc < fim + compasso:
        raiz, notas = ACORDES[k % 4]
        dur = compasso + 0.4
        i = int(tc * SR)
        bloco = sum(rhodes(NOTAS[x], dur) for x in notas) * 0.16
        bx = np.sin(2 * np.pi * BAIXO[raiz] * t(dur)) * np.exp(-t(dur) / 1.6) * 0.5
        seg = (bloco + bx)[: max(0, n - i)]
        abafa = resp <= tc < volta
        if abafa:
            seg = banda(seg, 40, 700) * 0.8
        mus[i: i + len(seg)] += seg
        if not abafa and tc < fim:
            for b in range(4):
                tb = tc + b * BATIDA
                ib = int(tb * SR)
                if b in (0, 2):
                    kk = thump()[: int(0.25 * SR)] * 0.55
                    bat[ib: ib + len(kk)] += kk[: max(0, n - ib)]
                if b in (1, 3):
                    sn = banda(ruido(0.18), 900, 6000) * env(0.18, 0.001, 0.05) * 0.35
                    bat[ib: ib + len(sn)] += sn[: max(0, n - ib)]
                for h in range(2):
                    ih = int((tb + h * BATIDA / 2 + (0.03 if h else 0)) * SR)  # swing leve
                    hh = banda(ruido(0.04), 7000, 14000) * env(0.04, 0.0005, 0.01) * 0.12
                    bat[ih: ih + len(hh)] += hh[: max(0, n - ih)]
        tc += compasso
        k += 1
    vinil = banda(ruido(DUR), 1000, 6000) * 0.012 + (RNG.random(n) < 0.0004) * RNG.standard_normal(n) * 0.15
    out = mus + bat + vinil
    tt = np.arange(n) / SR
    out *= np.interp(tt, [0, ini - 0.02, ini, fim, DUR], [0, 0, 1, 1, 0.0])
    return norm(out, 0.7)


if __name__ == "__main__":
    salvar("trilha", trilha())
