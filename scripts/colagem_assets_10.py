"""Reel 10 ("chafé: dois erros"): imagens geradas no ChatGPT → peças de colagem → biblioteca → projeto.

Cada imagem sai sobre branco liso (#FFFFFF), uma por conversa nova (canastra-conteudo, fase 3),
e vira peça com filete de papel e 3 bordas (boil), como na peça 07.

    python -m uv run python scripts/colagem_assets_10.py g1
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import biblioteca_colagem as B  # noqa: E402
from colagem_assets import convexo, peca, separar  # noqa: E402

BR = Path("saida-teste/reel10-geradas")
TMP = BR / "pecas"
DIA = "2026-10-28"
PROJ = "10-isso-e-chafe"

PROMPTS = {
    "g1": ("xicara-vidro-clarinha", "g1-xicara-clarinha.png", ["xícara", "vidro", "café", "torra média", "clarinho", "translúcido"],
           "Create an image. Photo of a single clear glass cup (straight-sided borosilicate tumbler, no handle) filled to 80% "
           "with freshly brewed filter coffee, medium roast: the liquid is translucent amber-brown — light passes through it, "
           "the edges glow lighter and you can faintly see through the coffee. Side view at eye level, cup centred with a "
           "generous empty margin, on a seamless pure white background (#FFFFFF). Plain even daylight from the front, "
           "neutral-to-cool white balance. Deep depth of field, everything equally sharp. Realistic smartphone photo of a real "
           "object, not a 3D render, not an illustration. Vertical 2:3 format. DO NOT INCLUDE: saucer, spoon, steam, foam, crema, "
           "latte art, milk, coffee beans, cookies, napkin, table surface, plant shadows, window reflections, text, logos, labels, "
           "hands, golden or warm light, dark opaque coffee, vignette, colour grading, bokeh."),
}


def main(chave: str) -> None:
    nome, arq, tags, prompt = PROMPTS[chave]
    pecas = separar(BR / arq, [nome], juntar_px=24, limiar=22)
    rgb, a = pecas[nome]
    peca(rgb, convexo(a), nome, filete=14, com_reticula=False, destino=TMP)
    bruto = B.RAIZ / "brutos" / f"{DIA}_{nome}.png"
    bruto.parent.mkdir(parents=True, exist_ok=True)
    bruto.write_bytes((BR / arq).read_bytes())
    B.registrar(nome, "objeto", [TMP / f"{nome}-b{i}.png" for i in range(3)], tags, "gerado-chatgpt",
                bruto=bruto.as_posix(), prompt=prompt, dia=DIA, nota="Reel 10: o café clarinho que chamam de chafé")
    B.publicar(PROJ, [f"{DIA}_{nome}"])


if __name__ == "__main__":
    main(sys.argv[1])
