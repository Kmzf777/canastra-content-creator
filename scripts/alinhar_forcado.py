"""Alinhamento FORÇADO da narração: tempo de cada palavra pelo áudio, não pelo whisper.

Por que existe: o `alinhar_narracao.py` casa o texto do roteiro com os tempos do
whisper e só corrige o início de uma palavra quando ele cai DENTRO de um silêncio.
Medido na peça 07 (07/10/2026): o whisper atrasa o início de frase em 0,1 a 0,4 s
sem cair em silêncio nenhum — "A primeira é no grão cru" começa em 14,38 s e o
whisper marcou 14,80 s; "Agora vem a xícara" começa em 32,95 s e ele marcou 33,36 s.
Legenda de corte seco e colagem que bate na palavra denunciam esse atraso.

Aqui o texto já é conhecido (o roteiro), então não há o que transcrever: o modelo
MMS_FA (wav2vec2 multilíngue treinado para alinhamento, torchaudio) dá a
probabilidade de cada letra em cada quadro de 20 ms, e o `forced_align` acha o
caminho CTC que lê o roteiro inteiro, letra por letra, sobre o áudio.

    python scripts/alinhar_forcado.py <palavras.json> <audio> [saida.json]

Lê a lista de palavras (texto e índice) de `palavras.json` e grava os tempos novos
no mesmo formato. Sem `saida`, só imprime a comparação com os tempos atuais.
Requer `torchaudio` com a versão do `torch` instalado; o modelo (~1,2 GB) baixa na
primeira execução para o cache do torch.
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
import torch
import torchaudio.functional as F
from torchaudio.pipelines import MMS_FA

SR = 16000
JANELA = 24.0  # s por passada do modelo (atenção é quadrática no tempo)
SOBRA = 3.0  # s de contexto de cada lado, descartados na costura


def ffmpeg() -> str:
    raiz = os.path.join(os.path.dirname(__file__), "..", "instagram", "remotion", "node_modules", "@remotion")
    for d in os.listdir(raiz) if os.path.isdir(raiz) else []:
        c = os.path.join(raiz, d, "ffmpeg.exe")
        if d.startswith("compositor") and os.path.exists(c):
            return os.path.abspath(c)
    return "ffmpeg"


def carregar(audio: str) -> np.ndarray:
    """Áudio em 16 kHz mono. A build de ffmpeg do Remotion não tem saída s16le em pipe,
    então passa por um WAV temporário."""
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "a.wav")
        subprocess.run([ffmpeg(), "-v", "error", "-y", "-i", audio, "-ac", "1", "-ar", str(SR), wav], check=True)
        w = wave.open(wav)
        x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768
        w.close()
    return x


def normalizar(p: str) -> str:
    s = unicodedata.normalize("NFKD", p.lower())
    return "".join(c for c in s if c in "abcdefghijklmnopqrstuvwxyz'")


def emissao(modelo: torch.nn.Module, x: np.ndarray) -> tuple[torch.Tensor, float]:
    """Log-probabilidades [T, C] da faixa inteira, costurando janelas com sobra de contexto."""
    partes: list[torch.Tensor] = []
    passo_s = None
    ini = 0.0
    dur = len(x) / SR
    while ini < dur:
        a = max(0.0, ini - SOBRA)
        b = min(dur, ini + JANELA + SOBRA)
        seg = torch.from_numpy(x[int(a * SR):int(b * SR)].copy()).unsqueeze(0)
        with torch.inference_mode():
            em, _ = modelo(seg)
        em = torch.log_softmax(em[0], dim=-1)
        passo_s = (b - a) / em.shape[0]
        q0 = int(round((ini - a) / passo_s))
        q1 = int(round((min(dur, ini + JANELA) - a) / passo_s))
        partes.append(em[q0:q1])
        print(f"  janela {ini:5.1f}-{min(dur, ini + JANELA):5.1f} s: {q1 - q0} quadros", file=sys.stderr)
        ini += JANELA
    return torch.cat(partes), float(passo_s)


def alinhar(palavras: list[dict], x: np.ndarray) -> list[dict]:
    modelo = MMS_FA.get_model(with_star=False)
    modelo.eval()
    dicionario = MMS_FA.get_dict(star=None)
    em, passo = emissao(modelo, x)
    textos = [normalizar(p["texto"]) for p in palavras]
    vazias = [p["texto"] for p, t in zip(palavras, textos) if not t]
    if vazias:
        raise SystemExit(f"palavras sem letra alinhável: {vazias}")
    alvo = [dicionario[c] for t in textos for c in t]
    caminho, pontos = F.forced_align(em.unsqueeze(0), torch.tensor([alvo], dtype=torch.int32), blank=0)
    trechos = F.merge_tokens(caminho[0], pontos[0].exp())
    assert len(trechos) == len(alvo), (len(trechos), len(alvo))
    out, k = [], 0
    for p, t in zip(palavras, textos):
        letras = trechos[k:k + len(t)]
        k += len(t)
        out.append({
            "i": p["i"], "texto": p["texto"],
            "inicio": round(letras[0].start * passo, 3), "fim": round(letras[-1].end * passo, 3),
            "confianca": round(float(np.mean([s.score for s in letras])), 3),
        })
    return out


def silencios(x: np.ndarray, limiar_db: float = -45, minimo: float = 0.04) -> list[tuple[float, float]]:
    jan = int(SR * 0.01)
    n = len(x) // jan
    db = 20 * np.log10(np.sqrt((x[: n * jan].reshape(n, jan) ** 2).mean(axis=1)) + 1e-9)
    runs, st = [], None
    for i, v in enumerate(np.append(db < limiar_db, False)):
        if v and st is None:
            st = i
        if not v and st is not None:
            if (i - st) * 0.01 >= minimo:
                runs.append((st * 0.01, i * 0.01))
            st = None
    return runs


def fundir(whisper: list[dict], ctc: list[dict], x: np.ndarray, limiar_curto: float = -45) -> list[dict]:
    """Funde o CTC com o whisper. Medido na peça 07 contra ~110 inícios lidos à mão no
    envelope do áudio (07/10/2026):

    - o whisper acerta o ataque de palavra quando acerta a região, mas DESLIZA: de
      23,8 s a 28,6 s ficou 0,5 a 0,7 s atrasado, sem cair em silêncio nenhum;
    - o CTC nunca perde a região (lê o roteiro inteiro sobre o áudio), mas tem viés de
      ~0,1 s TARDE dentro da frase e, em frase que começa depois de pausa, às vezes
      atrasa a frase inteira 0,2 a 0,4 s ("Zero defeito grave", "Se não tem nota").

    Regras, nesta ordem:
      1. primeira palavra depois de pausa (≥ 100 ms) → início = fim da pausa (o ataque;
         numa oclusiva, a explosão). Se isso puxou o CTC mais de 0,15 s para trás, a
         frase inteira do CTC está atrasada: as palavras seguintes, até a próxima
         pausa, ficam com o tempo do whisper;
      2. senão, whisper e CTC a até 0,25 s um do outro → média dos dois;
      3. senão → CTC (o whisper deslizou);
      4. um silêncio curto (≥ 40 ms: oclusão, respiro) termina até 0,2 s antes da
         estimativa e começa bem depois do início da palavra anterior → início = fim
         dele ("defeitos | nasce": estimativa 52,46 s, ataque 52,27 s). Sem silêncio
         assim, a estimativa recua 0,04 s: as duas fontes atrasam em média;
      5. início dentro de silêncio → fim do silêncio, sem passar do fim da palavra.
    A pausa da regra 1 é procurada até o tempo do CTC, nunca do whisper: com o whisper
    0,7 s atrasado, ela achava a pausa SEGUINTE e jogava a palavra para depois dela.
    """
    sil = silencios(x)
    pausas = silencios(x, -48, 0.10)
    curtos = silencios(x, limiar_curto, 0.04)
    out: list[dict] = []
    frase_whisper = False
    for k, (w, c) in enumerate(zip(whisper, ctc)):
        ant = out[k - 1]["inicio"] if k else -1.0
        # pausa que começa depois do início da palavra anterior e termina antes desta
        pausa = None
        for a, b in pausas:
            if a > ant + 0.03 and b <= c["inicio"] + 0.03:
                pausa = (a, b)
        if pausa is not None:
            ini = pausa[1]
            frase_whisper = c["inicio"] - ini > 0.15
            regra = "pausa" + (" (frase do CTC atrasada)" if frase_whisper else "")
        else:
            if frase_whisper and w["inicio"] > ant:
                est, regra = w["inicio"], "whisper"
            elif abs(w["inicio"] - c["inicio"]) <= 0.25:
                est, regra = (w["inicio"] + c["inicio"]) / 2, "média"
            else:
                est, regra = c["inicio"], "ctc"
            curto = [b for a, b in curtos if est - 0.2 <= b < est + 0.04 and a > ant + 0.15]
            if curto:
                ini, regra = curto[-1], regra + " + ataque após silêncio curto"
            else:
                ini = est - 0.04
        for a, b in sil:
            if a <= ini < b:
                ini = min(b, max(c["fim"], ini + 0.02) - 0.02)
                regra += " + saiu do silêncio"
                break
        ini = max(ini, ant + 0.03)
        out.append({"i": c["i"], "texto": c["texto"], "inicio": round(ini, 3),
                    "fim": round(max(c["fim"], ini + 0.05), 3), "confianca": c["confianca"], "regra": regra})
    return out


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    palavras = json.load(open(sys.argv[1], encoding="utf-8"))
    x = carregar(sys.argv[2])
    novas = fundir(palavras, alinhar(palavras, x), x)
    for a, n in zip(palavras, novas):
        d = n["inicio"] - a["inicio"]
        marca = "  <<<" if abs(d) >= 0.08 else ""
        print(f"{n['i']:3d} {n['texto']:<16s} {a['inicio']:6.2f} -> {n['inicio']:6.2f} ({d:+.2f})"
              f"  fim {n['fim']:6.2f}  conf {n['confianca']:.2f}  [{n['regra']}]{marca}")
    if len(sys.argv) > 3:
        with open(sys.argv[3], "w", encoding="utf-8") as f:
            json.dump([{k: n[k] for k in ("i", "texto", "inicio", "fim")} for n in novas], f, ensure_ascii=False, indent=1)
        print(f"gravado: {sys.argv[3]}", file=sys.stderr)


if __name__ == "__main__":
    main()
