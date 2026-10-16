"""Efeitos sonoros e cama musical da peça 06 (motion "Você sabia" em colagem).

Tudo sintetizado aqui, com semente fixa: rodar duas vezes dá os mesmos bytes.
Não há trilha licenciada no repositório (skill canastra-video §1), e efeito de
papel/carimbo é exatamente o tipo de som que síntese simples resolve bem.

Filtros por máscara de FFT (sem scipy, que está quebrado neste venv).

    python -m uv run python scripts/colagem_sfx.py
"""

from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

SR = 44100
RNG = np.random.default_rng(20261007)
DEST = Path("instagram/remotion/projetos/06-voce-sabia-especial/public/sfx")


def t(dur: float) -> np.ndarray:
    return np.arange(int(dur * SR)) / SR


def ruido(dur: float) -> np.ndarray:
    return RNG.standard_normal(int(dur * SR))


def banda(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    """Passa-banda por máscara suave na FFT."""
    X = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    m = 1 / (1 + (lo / np.maximum(fr, 1)) ** 4) * 1 / (1 + (fr / hi) ** 4)
    return np.fft.irfft(X * m, len(x))


def env(dur: float, ataque: float, decai: float) -> np.ndarray:
    tt = t(dur)
    a = np.clip(tt / max(ataque, 1e-4), 0, 1)
    return a * np.exp(-np.maximum(tt - ataque, 0) / decai)


def norm(x: np.ndarray, pico: float = 0.8) -> np.ndarray:
    return x / (np.max(np.abs(x)) + 1e-9) * pico


def thump() -> np.ndarray:
    tt = t(0.45)
    f = 70 * np.exp(-tt * 6) + 38
    corpo = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(0.45, 0.003, 0.12)
    clique = banda(ruido(0.45), 800, 4000) * env(0.45, 0.001, 0.008) * 0.3
    return norm(corpo + clique, 0.9)


def tick() -> np.ndarray:
    return norm(banda(ruido(0.05), 1800, 6000) * env(0.05, 0.0005, 0.006), 0.5)


def tink() -> np.ndarray:
    tt = t(1.4)
    parc = [(2210, 1.0, 0.45), (3470, 0.5, 0.3), (5130, 0.3, 0.18), (7020, 0.15, 0.1)]
    s = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt / d) for f, a, d in parc)
    return norm(s * np.clip(tt / 0.002, 0, 1), 0.55)


def rasgo() -> np.ndarray:
    dur = 0.55
    n = ruido(dur)
    estalos = (RNG.random(len(n)) < 0.012).astype(float) * RNG.standard_normal(len(n)) * 6
    s = banda(n + estalos, 1200, 9000)
    e = np.interp(t(dur), [0, 0.04, 0.4, dur], [0, 1, 0.7, 0])
    return norm(s * e, 0.6)


def slide() -> np.ndarray:
    dur = 0.32
    e = np.interp(t(dur), [0, 0.12, dur], [0, 1, 0])
    return norm(banda(ruido(dur), 900, 5000) * e, 0.35)


def pop() -> np.ndarray:
    tt = t(0.09)
    f = 520 * np.exp(-tt * 30) + 180
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(0.09, 0.001, 0.025), 0.5)


def carimbo() -> np.ndarray:
    tt = t(0.3)
    corpo = np.sin(2 * np.pi * 95 * tt) * env(0.3, 0.001, 0.05)
    madeira = banda(ruido(0.3), 300, 2500) * env(0.3, 0.0005, 0.02)
    return norm(corpo * 0.8 + madeira, 0.95)


def ding() -> np.ndarray:
    tt = t(1.8)
    s = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt / d)
            for f, a, d in [(1318.5, 1, 0.9), (2637, 0.35, 0.5), (3955, 0.15, 0.3)])
    return norm(s * np.clip(tt / 0.003, 0, 1), 0.5)


def whoosh() -> np.ndarray:
    dur = 0.7
    n = ruido(dur)
    out = np.zeros_like(n)
    blocos = 14
    tam = len(n) // blocos
    for i in range(blocos):
        c = 3000 * (1 - i / blocos) + 400
        out[i * tam:(i + 1) * tam] = banda(n, c * 0.5, c * 1.5)[i * tam:(i + 1) * tam]
    e = np.interp(t(dur), [0, 0.3, dur], [0, 1, 0])
    return norm(out * e, 0.45)


def vento() -> np.ndarray:
    dur = 7.2
    s = banda(ruido(dur), 150, 900)
    mod = 0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * t(dur))
    e = np.interp(t(dur), [0, 1.2, dur - 1.5, dur], [0, 1, 1, 0])
    return norm(s * mod * e, 0.25)


def nota(freq: float) -> np.ndarray:
    tt = t(0.7)
    s = np.sin(2 * np.pi * freq * tt) + 0.25 * np.sin(2 * np.pi * freq * 4 * tt) * np.exp(-tt / 0.05)
    return norm(s * env(0.7, 0.002, 0.22), 0.45)


def cama(dur: float = 51.0) -> np.ndarray:
    """Pad quente em Ré maior, 96 BPM; acordes de 2 compassos (5 s)."""
    tt = t(dur)
    acordes = [[146.83, 220.0, 293.66, 369.99],  # D
               [123.47, 246.94, 293.66, 369.99],  # Bm
               [98.0, 196.0, 293.66, 392.0],      # G
               [110.0, 220.0, 277.18, 329.63]]    # A
    out = np.zeros_like(tt)
    seg = 5.0
    for k in range(int(np.ceil(dur / seg))):
        a0 = k * seg
        fatia = (tt >= a0 - 0.6) & (tt < a0 + seg + 0.6)
        lt = tt[fatia] - a0
        e = np.clip((lt + 0.6) / 1.2, 0, 1) * np.clip((seg + 0.6 - lt) / 1.2, 0, 1)
        for f in acordes[k % 4]:
            for det in (-0.6, 0.6):
                out[fatia] += np.sin(2 * np.pi * (f + det) * tt[fatia]) * e * 0.12
    out = banda(out, 60, 1800)
    # pulso suave de bumbo a cada batida (0,625 s), bem baixo
    batida = 60 / 96
    k = thump()[: int(0.3 * SR)] * 0.18
    for b in np.arange(0, dur - 0.3, batida):
        i = int(b * SR)
        out[i:i + len(k)] += k
    e = np.interp(tt, [0, 2.0, dur - 3.0, dur], [0, 1, 1, 0])
    return norm(out * e, 0.6)


def salvar(nome: str, x: np.ndarray) -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(DEST / f"{nome}.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"{nome}.wav  {len(x) / SR:5.2f} s")


if __name__ == "__main__":
    for nome, fn in [("thump", thump), ("tick", tick), ("tink", tink), ("rasgo", rasgo),
                     ("slide", slide), ("pop", pop), ("carimbo", carimbo), ("ding", ding),
                     ("whoosh", whoosh), ("vento", vento)]:
        salvar(nome, fn())
    for i, f in enumerate([587.33, 739.99, 880.0, 1174.66], 1):
        salvar(f"nota{i}", nota(f))
    salvar("cama", cama())
