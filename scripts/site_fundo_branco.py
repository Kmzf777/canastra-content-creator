"""Packshots dos 3 SKUs em fundo branco, para o site.

Nao e geracao de cena: e **edicao de fundo**. A foto-fonte manda no
enquadramento, na pose e no rotulo; o prompt so troca o cenario por um ciclorama
branco e reaterra a sombra de contato.

Por que Gemini e nao xAI: as tres fontes sao 4:5 (0,806) e `4:5` e nativo aqui —
sai 1856x2304 sem recorte. Ver `cie/providers/gemini.py`.

Risco conhecido (CLAUDE.md): o Gemini trata referencia como inspiracao e
**redesenha** o rotulo. Duas defesas neste script:
  1. o prompt pede identidade pixel a pixel do pacote, e nomeia o que nao pode mudar;
  2. o bloco por SKU soletra cada string impressa — se ele redesenhar, redesenha certo.
Mesmo assim erra ~1 em 3: gere `--n` variantes e escolha olhando.

    python -m uv run python scripts/site_fundo_branco.py --n 1          # sonda
    python -m uv run python scripts/site_fundo_branco.py --n 3          # rodada cheia
    python -m uv run python scripts/site_fundo_branco.py --sku canela --n 2
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from cie.providers.gemini import ErroGemini, ProvedorGemini  # noqa: E402

SAIDA = RAIZ / "saida-teste" / "site-fundo-branco"
ASPECTO = "4:5"
TAMANHO = "2K"
MODELO = "gemini-3-pro-image"


# --------------------------------------------------------------------------- #
# prompt
# --------------------------------------------------------------------------- #

#: O que vale para os tres. Escrito como ordem de EDICAO, nao de geracao — a
#: primeira frase e o que segura o modelo dentro da foto que recebeu.
BASE = """\
EDIT THE PROVIDED PHOTOGRAPH. This is a background replacement, not a new photo. \
Do not re-stage it, do not re-shoot it, do not re-draw it, do not re-frame it.

KEEP THE PACKAGE PIXEL-FOR-PIXEL IDENTICAL to the source image: the same bag, at \
the exact same position in the frame, the exact same scale, the exact same \
rotation and camera perspective, the exact same crop and framing. The same \
creases, folds, wrinkles and dents in the material. The same crimped top fold. \
The same round embossed degassing vent with its single dark centre dot. The same \
printed artwork and the same typography, letter for letter. The package must \
occupy exactly the same pixels of the frame as it does in the source.

CHANGE ONLY THE BACKGROUND. Replace the backdrop and the floor with a clean, \
seamless PURE WHITE studio cove — white sweep paper curving from wall to floor \
with no visible horizon line, no seam, no corner, no edge, no table, no surface \
texture, no props, no gradient banding. The white is even and bright across the \
whole frame, with at most a very faint neutral falloff near the outer corners.

Relight the package for that white cove only as far as physics demands: keep the \
same key light direction and the same specular highlight pattern that already \
exists on the bag, and remove the coloured light that used to spill onto it from \
the old backdrop. The bag keeps its own material and its own colour.

Directly beneath the base of the package, a soft short CONTACT SHADOW grounding \
it on the white floor — diffuse, neutral grey, no hard edge, no long cast shadow, \
no mirror reflection of the bag.

{sku}

EVERYTHING IN THE FRAME IS SHARP. No background blur, no bokeh, no \
depth-of-field falloff, no vignette, no glow, no lens flare. No added text, no \
watermark, no logo overlay, no reflection of the package on the floor.

Output the same vertical 4:5 framing as the source image.\
"""

#: Layout comum da frente. Vale para os tres; o que muda entra por `{variacao}`.
ARTE = """\
The printed front artwork, which must survive unchanged: a mountain ridge drawn \
in thin sketchy open line — a LOW, WIDE, FLAT-TOPPED tableland, an almost \
horizontal plateau escarpment with shallow irregular notches and one gently \
rounded high point, never sharp alpine peaks — with three tiny V-shaped bird \
marks at its far upper left. Overlapping and in front of that ridge, slightly \
right of centre, the word "Cafe" written small in slanted handwriting AND \
CARRYING AN ACUTE ACCENT over the final e. Directly below, very large, \
"CANASTRA" spelled C-A-N-A-S-T-R-A in a thick dry-brush script with uneven, \
partly broken strokes. A single heavy tapering brush swash sweeps underneath it, \
thick at the left and thinning to a point at the right. A very small registered \
trademark mark at the upper right of the final A. "Desde 1985" small and \
handwritten at the lower right, just above the tip of the swash. {variacao} \
Bottom right, a small rounded rectangle containing "250g", spelled two-five-zero-g.\
"""

CAIXA_ESPECIAL = (
    'Below the swash, centred, a thin single-line rectangle outline containing '
    'three stacked lines: "SPECIALTY" small and letterspaced, spelled '
    'S-P-E-C-I-A-L-T-Y, then "ESPECIAL" large and bold, then "SCA 80+".'
)


@dataclass(frozen=True)
class Sku:
    slug: str
    fonte: Path
    bloco: str

    def prompt(self) -> str:
        return BASE.format(sku=self.bloco)


def _arte(variacao: str) -> str:
    return ARTE.format(variacao=variacao)


SKUS: tuple[Sku, ...] = (
    Sku(
        slug="suave",
        fonte=RAIZ / "imagens" / "Produto Suave 250" / "Suave-kraft.jpg",
        bloco=(
            "The package is a 250g flat-bottom KRAFT PAPER pouch: natural unbleached "
            "brown paper, matte, visibly fibrous, with inward side gussets. All "
            "printing is flat matte BLACK ink laid directly on the bare kraft — no "
            "white label, no sticker, no gloss, no foil. "
            + _arte(
                CAIXA_ESPECIAL
                + ' Bottom left, small sans-serif caps on two lines: "SUAVE" over '
                '"TORRADO E MOIDO", where MOIDO carries an acute accent on the I.'
            )
        ),
    ),
    Sku(
        slug="classico",
        fonte=RAIZ
        / "imagens"
        / "Produto Classico 250"
        / "Gemini_Generated_Image_rw2resrw2resrw2r.jpg",
        bloco=(
            "The package is a 250g flat-bottom pouch in MATTE BLACK film, with a wide "
            "soft diffuse sheen and inward side gussets. All printing is flat WHITE "
            "ink on the black film. "
            + _arte(
                CAIXA_ESPECIAL
                + ' Bottom left, small sans-serif caps on two lines: "CLASSICO" — '
                "with an acute accent on the first A, reading CLÁSSICO — over "
                '"TORRADO E MOIDO", where MOIDO carries an acute accent on the I.'
            )
        ),
    ),
    Sku(
        slug="canela",
        fonte=RAIZ
        / "imagens"
        / "Produto Canela 250"
        / "Gemini_Generated_Image_hhlj5jhhlj5jhhlj.jpg",
        bloco=(
            "The package is a 250g flat-bottom pouch in GLOSSY RED METALLIC film, "
            "with strong specular highlights running in broad bands across the "
            "surface, and inward side gussets. All printing is flat WHITE ink on the "
            "red foil. This SKU has NO rectangular SPECIALTY / ESPECIAL / SCA 80+ box "
            "— do not add one. "
            + _arte(
                "In the lower right, above the weight badge, a white line drawing of "
                "two tied cinnamon quills. Bottom left, small sans-serif caps on two "
                'lines: "CAFE TORRADO E" — with an acute accent on the final e of '
                'CAFÉ — over "MOIDO COM CANELA", where MOIDO carries an acute accent '
                "on the I."
            )
        ),
    ),
)


# --------------------------------------------------------------------------- #
# execucao
# --------------------------------------------------------------------------- #


def gerar(skus: tuple[Sku, ...], n: int, seco: bool, tag: str = "") -> int:
    faltando = [s.slug for s in skus if not s.fonte.exists()]
    if faltando:
        print(f"fonte ausente para: {', '.join(faltando)}", file=sys.stderr)
        return 2

    if seco:
        for sku in skus:
            print(f"\n{'=' * 70}\n{sku.slug.upper()}  <- {sku.fonte.name}\n{'=' * 70}")
            print(sku.prompt())
        print(f"\n[seco] {len(skus) * n} imagem(ns) NAO geradas.")
        return 0

    load_dotenv(override=False)
    SAIDA.mkdir(parents=True, exist_ok=True)
    provedor = ProvedorGemini(modelo=MODELO, tamanho=TAMANHO)

    erros = 0
    for sku in skus:
        print(f"[{sku.slug}] {n}x {MODELO} {ASPECTO} {TAMANHO} <- {sku.fonte.name}")
        try:
            imagens = provedor.gerar(
                sku.prompt(), fontes=[sku.fonte], aspecto=ASPECTO, n=n
            )
        except ErroGemini as exc:
            print(f"[{sku.slug}] FALHOU: {exc}", file=sys.stderr)
            erros += 1
            continue
        for i, bruto in enumerate(imagens, start=1):
            destino = SAIDA / f"{sku.slug}-branco{tag}-v{i}.jpg"
            destino.write_bytes(bruto)
            print(f"[{sku.slug}]   {destino.relative_to(RAIZ)}  {len(bruto) // 1024} KB")
    return 1 if erros else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--n", type=int, default=1, help="variantes por SKU (padrao 1)")
    p.add_argument(
        "--sku",
        action="append",
        choices=[s.slug for s in SKUS],
        help="limita a um SKU; repetivel",
    )
    p.add_argument("--dry-run", action="store_true", help="imprime o prompt, nao gasta")
    p.add_argument(
        "--tag",
        default="",
        help="sufixo no nome do arquivo, para nao sobrescrever a rodada anterior",
    )
    args = p.parse_args()

    escolhidos = (
        SKUS if not args.sku else tuple(s for s in SKUS if s.slug in set(args.sku))
    )
    return gerar(escolhidos, max(1, args.n), args.dry_run, args.tag)


if __name__ == "__main__":
    raise SystemExit(main())
