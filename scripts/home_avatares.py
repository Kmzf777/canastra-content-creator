"""Avatares do elenco da home — a referencia de identidade de cada personagem.

POR QUE ESTE PASSO EXISTE. O motor nao tem identity-lock e seed nao serve para
isso. A unica coisa que funciona hoje e mandar uma FOTO da pessoa junto com o
prompt da cena. Como nao vamos usar o rosto de ninguem real, a foto tem de ser
gerada antes: e o que este script faz.

O que ele produz nao e retrato de campanha. E o pior tipo de foto possivel de
proposito — instantaneo de celular contra parede lisa, luz chata de janela,
quadro torto. Foto de documento mal tirada. Isso e o que faz o rosto sobreviver
como referencia sem impor uma estetica a cena seguinte.

A DISCIPLINA ANTI-BELEZA vem do teste com rosto real em `saida-teste/arthur/`,
que provou duas coisas: (1) pedir "nao embeleze, nao suavize, nao rejuvenesca"
funciona; (2) o modelo inventa joia sozinho, e por isso a proibicao de corrente,
anel e brinco esta escrita em todos.

    python -m uv run python scripts/home_avatares.py --dry-run
    python -m uv run python scripts/home_avatares.py --n 2
    python -m uv run python scripts/home_avatares.py --quem wesley --n 4
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

SAIDA = RAIZ / "saida-teste" / "home-elenco"
ASPECTO = "1:1"
TAMANHO = "2K"
MODELO = "gemini-3-pro-image"


# --------------------------------------------------------------------------- #
# blocos comuns
# --------------------------------------------------------------------------- #

#: O ATO FOTOGRAFICO, nao a pessoa. O achado mais alinhado ao alvo medido do
#: projeto (p1=14, saturacao 70, cantos moles) nao e descrever o rosto — e
#: descrever a foto como amadora. Ver `saida-teste/arthur/`.
ATO = """\
This is a badly taken phone snapshot, not a portrait session. Head and shoulders, \
shot straight on from about arm's length with the front camera of an ordinary \
phone. The frame is tilted two or three degrees, the head is slightly off centre, \
there is too much empty wall above the head. Plain painted interior wall behind, \
scuffed, no decoration. Flat indirect daylight from a window off to one side, no \
lamp, no fill, no reflector. Nobody arranged anything."""

#: As sete frases que atacam, uma a uma, a assinatura de "rosto de IA": pele sem
#: poro, simetria alta demais, luz de beleza, dente uniforme, catchlight
#: incoerente, mandibula generica de dataset, olhar vazio.
REAL = """\
Real unretouched skin with visible pores, slight oiliness on the forehead and the \
bridge of the nose, and uneven tone. Faint blemishes and a small mole or two. The \
two halves of the face are clearly NOT symmetrical - one eyebrow sits higher, one \
eye is slightly smaller, the mouth is not level. Lips closed, no smile, no visible \
teeth. Looking straight at the lens with an ordinary neutral expression, neither \
friendly nor stern. A single small hard specular highlight in each eye, both from \
the same direction. NO beauty retouching, NO skin smoothing, NO makeup look, NO \
studio lighting, NO rim light."""

#: O modelo inventa joia sozinho. Provado no segundo teste de `arthur/`, onde
#: apareceu uma corrente que nao era dele.
SEM_JOIA = """\
NO jewellery at all: no chain, no necklace, no pendant, no earrings, no bracelet, \
no ring, no watch, no sunglasses, no hat, no cap. The neck and collar are bare."""

#: Foco profundo. O bloco mais importante do conjunto — desfoque nao se desfaz em
#: pos. Aqui em versao de interior, sem a clausula de lavoura do bloco original.
FOCO = """\
EVERYTHING IN THE FRAME IS SHARP. Tiny 1/1.7 inch phone sensor at f/1.8, enormous \
depth of field. The face and the wall behind are equally crisp. NO focus falloff, \
NO background blur, NO bokeh, NO subject separation, NO portrait mode. The four \
CORNERS are visibly softer the way a cheap wide phone lens falls apart away from \
centre. Fine luminance noise in the shadows."""

#: Ponto preto levantado, saturacao baixa, altas puxando azul — o perfil de camera
#: medido do projeto (p1 14, saturacao 70, cast R/B 0,969).
PERFIL = """\
Phone HDR: shadows LIFTED and open and slightly grey rather than black, the \
brightest patch of wall BLOWN OUT to featureless white, midtones flat and \
processed. Slightly cool, washed white balance, muted low saturation - NOT warm, \
NOT orange, NOT amber, NOT rich."""

NEG = (
    "beauty retouching, skin smoothing, airbrushed skin, poreless skin, "
    "symmetrical face, open mouth smile, perfect teeth, model, fashion model, "
    "stock photo person, headshot, professional portrait, studio lighting, "
    "softbox, reflector, rim light, bokeh, background blur, shallow focus, "
    "portrait mode, golden hour, warm glow, amber light, teal and orange, "
    "jewellery, necklace, chain, earrings, glasses unless stated, hat, cap, "
    "makeup, lipstick unless stated, 3d render, CGI, illustration, watermark, "
    "text overlay, celebrity, famous person, recognisable public figure"
)


@dataclass(frozen=True)
class Pessoa:
    slug: str
    #: Descricao fisica. Fenotipo, idade e corpo SAO obrigatorios: o default do
    #: modelo e pele clara, e sem isso o elenco inteiro sai igual.
    corpo: str

    def prompt(self) -> str:
        return (
            f"{ATO}\n\n{self.corpo}\n\n{REAL}\n\n{SEM_JOIA}\n\n"
            f"{PERFIL}\n\n{FOCO}\n\nAvoid: {NEG}"
        )


# --------------------------------------------------------------------------- #
# o elenco
# --------------------------------------------------------------------------- #
#
# Sete pessoas ficcionais. Cinco de sete sao pardas ou pretas, o que e fidelidade
# ao pais (Censo 2022: 45,3% pardos) e nao cota — e e a unica forma de o site
# dizer "alcance amplo", ja que o copy esta proibido de dizer.
#
# NINGUEM AQUI E COPIA DE PESSOA REAL. Se alguma variante sair parecida com
# alguem identificavel, ela e descartada, nao ajustada.

ELENCO: tuple[Pessoa, ...] = (
    Pessoa(
        "wesley",
        "A 31-year-old Black Brazilian man, medium-dark skin, round face, full "
        "eyebrows, uneven short stubble along the jaw, a small scar through one "
        "eyebrow. Hair cut low with a barbershop fade and a sharp lined edge. "
        "Slightly heavy build. He wears a faded forest-green cotton t-shirt cut "
        "slightly large, worn out at the neck.",
    ),
    Pessoa(
        "yuri",
        "A 29-year-old Brazilian man of Japanese descent, pale skin with a yellow "
        "undertone, epicanthic fold, angular face, narrow jaw, no facial hair, "
        "tall and thin. Thick straight black hair in a messy medium cut, the "
        "fringe falling into one eyebrow, slightly greasy at the root. He wears "
        "thin round wire-frame prescription glasses - these he keeps - over a "
        "small-checked short-sleeve shirt in dark green and off-white.",
    ),
    Pessoa(
        "thaina",
        "A 26-year-old Brazilian woman with light golden-brown skin, faint "
        "freckles across the cheekbones, a straight nose with a rounded tip, a "
        "small acne scar on the chin and one active spot on the jaw. Voluminous "
        "3C curls to the shoulder, defined with cheap gel, with real frizz "
        "standing up at the crown and along the hairline - no straightening, no "
        "glossy shampoo-commercial curl. She wears a grimy off-white ribbed vest "
        "with wide straps.",
    ),
    Pessoa(
        "barbara",
        "A 37-year-old white Brazilian woman with very pale skin, dense freckles "
        "across the nose and cheeks, mild rosacea flushing on both cheeks, light "
        "brown eyes, pale patchy eyebrows, faint lines at the eyes. Long auburn "
        "wavy hair clipped up with a plastic claw clip, loose strands escaping "
        "at the temples. She wears a fine off-white knit top, pilled with wear.",
    ),
    Pessoa(
        "rosangela",
        "A 44-year-old Brazilian woman with light brown skin, a full face, a soft "
        "double chin, natural dark circles under the eyes, eyebrows drawn in with "
        "pencil, old lipstick almost entirely worn off leaving only a stain. "
        "Dyed chestnut hair pulled back into a ponytail with THREE CENTIMETRES OF "
        "DARK ROOT SHOWING and a side fringe falling across her face. She wears a "
        "yellowed off-white uniform polo shirt with the collar open.",
    ),
    Pessoa(
        "diego",
        "A 19-year-old Brazilian man with deep brown skin, very black hair and "
        "eyebrows, a thin unformed moustache, ACTIVE ACNE on the forehead and "
        "along the jaw with a few healing marks, a full lower lip, a face that "
        "has not finished growing. Hair cut short with a shaved part on one side "
        "and more length on top. Thin neck. He wears a faded plain red "
        "amateur-football shirt with NO text, number, crest or badge on it.",
    ),
    Pessoa(
        "dulce",
        "A 52-year-old Black Brazilian woman, dark even skin tone, long face with "
        "a strong jaw, full lips, small deep-set eyes, deep lines at the mouth and "
        "across the forehead, permanent sun damage on the cheekbones. Natural 4C "
        "hair cut VERY SHORT, about two centimetres, no straightening, no "
        "headwrap, NO GLOSS AT ALL - the hairline is uneven and the scalp shows "
        "through at the temples. Cheap acetate prescription glasses with one arm "
        "mended with tape - these she keeps. She wears a thin dark forest-green "
        "cotton t-shirt worn out at the neck.",
    ),
    Pessoa(
        "igor",
        "A 23-year-old Brazilian man with medium brown skin, a thin face, a "
        "narrow nose, patchy island-like stubble along the jaw, a small closed-up "
        "stretched hole in one earlobe. Slim, narrow shoulders. Brown 3B curly "
        "hair with volume on top and shorter sides, slightly oily at the root. "
        "He wears an oversized grimy off-white t-shirt with a small unreadable "
        "print.",
    ),
)


# --------------------------------------------------------------------------- #
# execucao
# --------------------------------------------------------------------------- #


def gerar(pessoas: tuple[Pessoa, ...], n: int, seco: bool, tag: str) -> int:
    if seco:
        for p in pessoas:
            print(f"\n{'=' * 70}\n{p.slug.upper()}\n{'=' * 70}")
            print(p.prompt())
        print(f"\n[seco] {len(pessoas) * n} imagem(ns) NAO geradas.")
        return 0

    load_dotenv(override=False)
    SAIDA.mkdir(parents=True, exist_ok=True)
    provedor = ProvedorGemini(modelo=MODELO, tamanho=TAMANHO)

    erros = 0
    for p in pessoas:
        print(f"[{p.slug}] {n}x {MODELO} {ASPECTO} {TAMANHO}", flush=True)
        try:
            imagens = provedor.gerar(p.prompt(), fontes=[], aspecto=ASPECTO, n=n)
        except ErroGemini as exc:
            print(f"[{p.slug}] FALHOU: {exc}", file=sys.stderr, flush=True)
            erros += 1
            continue
        for i, bruto in enumerate(imagens, start=1):
            destino = SAIDA / f"{p.slug}{tag}-v{i}.jpg"
            destino.write_bytes(bruto)
            print(f"[{p.slug}]   {destino.name}  {len(bruto) // 1024} KB", flush=True)
    return 1 if erros else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--quem", action="append", choices=[p.slug for p in ELENCO])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    escolhidos = (
        ELENCO if not a.quem else tuple(p for p in ELENCO if p.slug in set(a.quem))
    )
    return gerar(escolhidos, max(1, a.n), a.dry_run, a.tag)


if __name__ == "__main__":
    raise SystemExit(main())
