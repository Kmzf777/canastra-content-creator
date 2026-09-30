"""Pega o PNG mais recente baixado do ChatGPT em Downloads e copia pro destino.

Uso: python scripts/_pega_download.py <destino relativo a partir da raiz do repo>
"""
import glob
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent

# Um seletor que nao acha o alvo mas acha ALGO e pior que um que falha: o glob
# pega o download de ontem e o script nao reclama (licao 17 do CLAUDE.md).
# Dimensao igual nao prova que e a imagem certa; carimbo de hora prova.
IDADE_MAXIMA_S = 180


def exigir_recente(caminho: str) -> None:
    """Aborta se o arquivo for velho demais para ser o download desta rodada."""
    idade = time.time() - os.path.getmtime(caminho)
    if idade > IDADE_MAXIMA_S:
        raise SystemExit(
            f"ABORTADO: {caminho} tem {idade/60:.1f} min de idade. "
            "O download provavelmente falhou e o glob pegou um arquivo antigo."
        )


def main():
    destino = sys.argv[1]
    # O ChatGPT nomeia o arquivo no idioma da conta: "ChatGPT Image ....png" em
    # ingles, "Imagem do ChatGPT ....png" em portugues. Procurar so um dos dois
    # nao da erro: pega silenciosamente um download antigo do outro padrao.
    DOWNLOADS = Path(r"C:\Users\rafae\Downloads")
    padroes = ("ChatGPT Image*.png", "Imagem do ChatGPT*.png")
    files = [f for pad in padroes for f in glob.glob(str(DOWNLOADS / pad))]
    if not files:
        print("NENHUM ARQUIVO ENCONTRADO EM DOWNLOADS", file=sys.stderr)
        return 1
    latest = max(files, key=os.path.getmtime)
    exigir_recente(latest)
    im = Image.open(latest)
    w, h = im.size
    dest_path = RAIZ / destino
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(latest, dest_path)
    carimbo = datetime.fromtimestamp(os.path.getmtime(latest)).strftime("%H:%M:%S")
    print(
        f"{latest} -> {dest_path.relative_to(RAIZ)} | {w}x{h} "
        f"ratio={w/h:.3f} baixado={carimbo}"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
