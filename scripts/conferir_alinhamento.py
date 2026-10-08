"""Confere o tempo das palavras contra o ÁUDIO, não contra outro alinhador.

Dois modos:

    python scripts/conferir_alinhamento.py pausas <palavras.json> <narracao>
        Lista cada ataque de voz depois de uma pausa funda e a palavra do JSON mais
        perto dele. Delta acima de ±0,06 s é suspeito: é a primeira conferência,
        a que pega o alinhador deslizando (peça 07: o whisper chegou a 0,7 s).

    python scripts/conferir_alinhamento.py faixa <palavras.json> <narracao> 23.1-25.3 [...] [--com outro.json]
        Desenha o envelope do áudio em caracteres de 20 ms e marca embaixo o início de
        cada palavra (^texto). Com `--com`, uma segunda linha de marcas para comparar
        (ex.: palavras-whisper.json). É assim que se lê o ataque real à mão:
            ' ' < -50 dB (silêncio)  '.' -50..-40  ':' -40..-30  '|' -30..-22  '#' > -22
        Oclusiva (p, t, k) começa por um silêncio curto; fricativa (s, f, x) é '.' ou ':'
        antes da vogal; vogal tônica é '#'. Respiro antes da frase também é '.'/':' —
        não confunda com a palavra.

Por que existe: na peça 07 a fusão whisper + CTC (`alinhar_forcado.py`) foi validada
contra 109 ataques lidos assim (mediana 0,02 s, máximo 0,15 s). Os limiares da fusão
foram calibrados NESSA voz; voz nova, ou a mesma em outra velocidade, pede nova leitura
de pelo menos um ataque por frase antes de confiar.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unicodedata
import wave

import numpy as np

SR = 16000


def ffmpeg() -> str:
    raiz = os.path.join(os.path.dirname(__file__), "..", "instagram", "remotion", "node_modules", "@remotion")
    for d in os.listdir(raiz) if os.path.isdir(raiz) else []:
        c = os.path.join(raiz, d, "ffmpeg.exe")
        if d.startswith("compositor") and os.path.exists(c):
            return os.path.abspath(c)
    return "ffmpeg"


def carregar(audio: str) -> np.ndarray:
    # a build do Remotion não tem saída s16le em pipe: passa por WAV temporário
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "a.wav")
        subprocess.run([ffmpeg(), "-v", "error", "-y", "-i", audio, "-ac", "1", "-ar", str(SR), wav], check=True)
        w = wave.open(wav)
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768
        w.close()
    return x


def db(x: np.ndarray, hop: float) -> np.ndarray:
    jan = int(SR * hop)
    n = len(x) // jan
    return 20 * np.log10(np.sqrt((x[: n * jan].reshape(n, jan) ** 2).mean(axis=1)) + 1e-9)


def ascii_(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def pausas(P: list[dict], x: np.ndarray) -> None:
    e = db(x, 0.01)
    ev, i = [], 0
    while i < len(e):
        if e[i] < -52:
            j = i
            while j < len(e) and e[j] < -45:
                j += 1
            if j - i >= 6 and j < len(e):
                ev.append((i * 0.01, j * 0.01))
            i = j + 1
        else:
            i += 1
    suspeitos = 0
    for a, o in ev:
        k = min(range(len(P)), key=lambda k: abs(P[k]["inicio"] - o))
        d = o - P[k]["inicio"]
        marca = "  <<<" if abs(d) >= 0.06 else ""
        suspeitos += bool(marca)
        print(f"pausa {a:6.2f}-{o:6.2f}  ataque {o:6.2f}  -> {k:3d} {ascii_(P[k]['texto']):14s} "
              f"inicio {P[k]['inicio']:6.2f}  delta {d:+.2f}{marca}")
    print(f"\n{len(ev)} ataques depois de pausa; {suspeitos} com |delta| >= 0,06 s (leia esses com `faixa`)")


def faixa(P: list[dict], x: np.ndarray, faixas: list[str], outro: list[dict] | None) -> None:
    hop = 0.02
    e = db(x, hop)

    def marcas(L: list[dict], t0: float, n: int, rotulo: str) -> str:
        lab = [" "] * n
        for p in L:
            k = int(round((p["inicio"] - t0) / hop))
            if 0 <= k < n:
                for j, c in enumerate("^" + ascii_(p["texto"])):
                    if k + j < n and lab[k + j] == " ":
                        lab[k + j] = c
        return rotulo + " " + "".join(lab)

    for f in faixas:
        t0, t1 = map(float, f.split("-"))
        a, b = int(t0 / hop), int(t1 / hop)
        linha = "".join(" " if v < -50 else "." if v < -40 else ":" if v < -30 else "|" if v < -22 else "#" for v in e[a:b])
        regua = "".join(str(int(round((t0 + i * hop) * 10)) % 10) if i % 5 == 0 else "-" for i in range(b - a))
        print(f"{t0:.2f}..{t1:.2f}  (1 caractere = 20 ms; dígito = décimo de segundo)")
        print("  " + regua)
        print("  " + linha)
        print(marcas(P, t0, b - a, "A"))
        if outro:
            print(marcas(outro, t0, b - a, "B"))
        print()


def main() -> None:
    if len(sys.argv) < 4 or sys.argv[1] not in ("pausas", "faixa"):
        raise SystemExit(__doc__)
    modo, arq, audio, *resto = sys.argv[1:]
    P = json.load(open(arq, encoding="utf-8"))
    outro = None
    if "--com" in resto:
        i = resto.index("--com")
        outro = json.load(open(resto[i + 1], encoding="utf-8"))
        resto = resto[:i] + resto[i + 2:]
    x = carregar(audio)
    if modo == "pausas":
        pausas(P, x)
    else:
        faixa(P, x, resto, outro)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
