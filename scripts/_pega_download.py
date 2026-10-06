"""Pega o PNG mais recente baixado do ChatGPT em Downloads e copia pro destino.

Uso: python scripts/_pega_download.py <destino relativo a partir da raiz do repo>
"""
import glob
import json
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


# `exigir_recente` sozinho nao basta quando se baixa varias imagens em sequencia:
# se o clique em Baixar nao disparar, o download ANTERIOR ainda esta dentro da
# janela de 180 s e passa como se fosse o desta rodada. Medido em 04/10/2026 - a
# 17.7 foi gravada com a imagem da 21.6, mesmo carimbo de hora, sem um erro. Por
# isso cada arquivo de origem so pode ser consumido UMA vez.
CONSUMIDOS = RAIZ / ".cie" / "downloads-consumidos.json"


def ja_consumido(caminho: str) -> bool:
    chave = f"{os.path.abspath(caminho)}|{os.path.getmtime(caminho):.0f}"
    vistos = json.loads(CONSUMIDOS.read_text()) if CONSUMIDOS.exists() else []
    if chave in vistos:
        return True
    CONSUMIDOS.parent.mkdir(parents=True, exist_ok=True)
    CONSUMIDOS.write_text(json.dumps(vistos[-200:] + [chave]))
    return False


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
    # NAO filtre por nome. Ja vimos tres padroes: "ChatGPT Image ....png" (conta
    # em ingles), "Imagem do ChatGPT ....png" (conta em portugues) e, desde
    # 04/10/2026, o TITULO DO CHAT ("Capsulas Cafe Canastra em Estudio.png") -
    # ou seja, uma string arbitraria que o proprio modelo escolheu. Nome de
    # arquivo e um seletor que o fornecedor pode trocar a qualquer momento; o
    # que de fato separa o download desta rodada dos outros e o CARIMBO DE HORA.
    # Entao: qualquer .png, o mais recente, e `exigir_recente` como unica trava.
    DOWNLOADS = Path(r"C:\Users\rafae\Downloads")
    files = glob.glob(str(DOWNLOADS / "*.png"))
    if not files:
        print("NENHUM ARQUIVO ENCONTRADO EM DOWNLOADS", file=sys.stderr)
        return 1
    latest = max(files, key=os.path.getmtime)
    exigir_recente(latest)
    if ja_consumido(latest):
        raise SystemExit(
            f"ABORTADO: {latest} ja foi gravado numa rodada anterior. "
            "O clique em Baixar nao disparou e o glob devolveu o download "
            "passado. Clique em Baixar de novo e repita."
        )
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
