"""Peça 08 ("esse café já foi uma fruta"): a folha do ChatGPT → biblioteca → projeto.

Frango de padaria no espeto, refratômetro de Brix, chama e carrinho de supermercado,
gerados juntos sobre branco liso (08/10/2026) e recortados aqui, com filete de papel e
3 bordas pela união dos bboxes (lição 60). SEM retícula: ficam fotográficos como as
peças da 07.

    python -m uv run python scripts/colagem_assets_08.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import biblioteca_colagem as B  # noqa: E402
from colagem_assets import peca, separar  # noqa: E402

BR = Path("saida-teste/motion-08/brutos")
TMP = Path("saida-teste/motion-08/pecas")
DIA = "2026-10-08"
PROJ = "08-cafe-ja-foi-fruta"
FOLHA = "peca08-folha-frango-refratometro.png"
PROMPT = (BR / "prompt-folha-08.txt")

ITENS = [  # nome, categoria, tags
    ("frango-padaria", "objeto", ["frango", "padaria", "espeto", "assado", "girando"]),
    ("refratometro", "xicara-utensilio", ["refratometro", "brix", "acucar", "medir", "maturacao"]),
    ("chama", "objeto", ["fogo", "chama", "torra", "calor"]),
    ("carrinho-mercado", "objeto", ["supermercado", "carrinho", "compra", "mercado"]),
]

if __name__ == "__main__":
    pecas = separar(BR / FOLHA, [n for n, _, _ in ITENS], juntar_px=24, limiar=22)
    bruto = B.RAIZ / "brutos" / f"{DIA}_folha-08.png"
    bruto.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BR / FOLHA, bruto)
    prompt = PROMPT.read_text(encoding="utf-8") if PROMPT.exists() else None
    ids = []
    for nome, cat, tags in ITENS:
        rgb, a = pecas[nome]
        peca(rgb, a, nome, filete=10, com_reticula=False, destino=TMP)
        var = [TMP / f"{nome}-b{b}.png" for b in range(3)]
        e = B.registrar(nome, cat, var, tags, "gerado-chatgpt", bruto=bruto.as_posix(), prompt=prompt, dia=DIA,
                        substituir=True)
        ids.append(e["id"])
    B.publicar(PROJ, ids)
