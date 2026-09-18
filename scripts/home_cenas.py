"""As cenas da home — geradas com o avatar do personagem como referencia.

COMO FUNCIONA. Cada cena manda para o Gemini o prompt da cena MAIS a foto do
avatar gerado em `scripts/home_avatares.py`. O avatar e o unico jeito de o mesmo
rosto sobreviver entre duas imagens: o motor nao tem identity-lock e seed nao
resolve isso.

Onde a EMBALAGEM aparece legivel, a foto real do pacote entra junto, no mesmo
campo de fontes. Nunca se descreve o rotulo em texto — descrever faz o modelo
redesenhar, e o que sai e um sosia da marca (licao 1 do CLAUDE.md).

ORDEM DAS FONTES IMPORTA. A saida herda a proporcao da primeira fonte, entao o
avatar (1:1) vai por ultimo quando ha packshot 4:5 na lista.

    python -m uv run python scripts/home_cenas.py --dry-run
    python -m uv run python scripts/home_cenas.py --cena heroi --n 4
    python -m uv run python scripts/home_cenas.py --n 3
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from cie.providers.gemini import ErroGemini, ProvedorGemini  # noqa: E402

ELENCO = RAIZ / "saida-teste" / "home-elenco"
SAIDA = RAIZ / "saida-teste" / "home-cenas"
PACK = RAIZ / "base-curada" / "01-real-verificada" / "torrefacao-uberlandia-875m"
TAMANHO = "2K"
MODELO = "gemini-3-pro-image"


# --------------------------------------------------------------------------- #
# blocos
# --------------------------------------------------------------------------- #

#: Identidade. O avatar manda no rosto; o prompt so proibe que ele seja
#: "melhorado". Sem esta clausula o modelo embeleza e a pessoa vira outra.
IDENTIDADE = """\
The reference portrait is the person who must appear in this photograph. Reproduce \
THAT face: the same proportions, the same skin, the same hair, the same marks. Do \
NOT beautify, slim, smooth, de-age or clean up the skin. Keep the pores, the \
blemishes, the asymmetry. He or she must look exactly as ordinary as in the \
reference. Lips closed, no visible teeth."""

#: O modelo inventa joia sozinho. Provado no teste de `saida-teste/arthur/`.
SEM_JOIA = """\
NO jewellery that is not described: no chain, no necklace, no pendant, no \
earrings, no bracelet, no watch, no sunglasses, no cap."""

#: Sol a pino de Medeiros. Verbatim de templates/blocos/luz-sol-pino.yaml.
LUZ_FAZENDA = """\
THE LIGHT IS HARSH OVERHEAD MIDDAY SUN. A bright blue sky with hard-edged white \
cumulus. The sun is almost straight up, so shadows are SHORT, SMALL and fall \
almost directly beneath things, and their edges are HARD and sharply defined, not \
soft. Strong contrast between the lit red earth and the dark interior of the \
coffee bushes. The lit ground is bright and slightly bleached out. This is the \
middle of a dry-season day, not a soft morning, not overcast, not golden hour."""

#: Sao Paulo e majoritariamente encoberta: 5 a 6 horas de sol por dia o ano
#: inteiro. O ceu branco entrega o alvo do projeto sem esforco de calibracao.
LUZ_SP = """\
OVERCAST WHITE SKY, the default weather of Sao Paulo. The light source is the \
entire hemisphere: there are NO cast shadows anywhere, only tight contact shadows \
directly under objects where they touch a surface. Contrast is very low, the black \
point sits naturally lifted, around 6800K with a blue-grey cast across the whole \
frame. This is a grey working weekday, not a bright day."""

#: BH e planalto a 852 m com estacao seca de junho a agosto. Sombra de borda dura
#: e sombra aberta muito azul — que E o cast R/B 0,969 ja medido no projeto.
LUZ_BH = """\
DRY-SEASON HIGHLAND SUN at midday, the light of Belo Horizonte between May and \
August. Direct sun around 5600K, shadows SHORT and HARD-EDGED, falling almost \
straight down. The open shade is filled only by the sky, so it goes strongly BLUE, \
around 9000K. Fine dry dust in suspension lifts the black point."""

#: Interior de comercio brasileiro: duas temperaturas no mesmo quadro. E a luz
#: real de padaria e boteco e deve ser descrita como tal, nao corrigida.
LUZ_COMERCIO = """\
Mixed indoor light, exactly as it really is in this kind of place: cool white \
fluorescent tubes overhead throwing a faint GREEN into the shadows, and one hard \
rectangle of daylight coming in through the open door. Two colour temperatures in \
the same frame. Do not correct them to a single source."""

HDR = """\
PHONE HDR at work: the shadows are LIFTED and open and slightly grey rather than \
black, nothing is a solid black mass. At the same time the brightest patches are \
BLOWN OUT to featureless white. The midtones look a bit flat and processed. \
Slightly cool, washed white balance, muted low saturation - NOT warm, NOT orange, \
NOT amber, NOT rich or vivid."""

FOCO = """\
EVERYTHING IN THE FRAME IS SHARP. Tiny 1/1.7 inch phone sensor at f/1.8, enormous \
depth of field. The nearest surface and the far end of the scene are ALL equally \
crisp and detailed. NO focus falloff, NO background blur, NO bokeh, NO subject \
separation, NO portrait mode. Distance reads faint from atmospheric haze only, \
never from defocus. The four CORNERS are visibly SOFTER and slightly smeared the \
way a cheap wide phone lens falls apart away from centre. Fine luminance noise in \
the shadows, faint JPEG blocking in flat areas."""

#: Substitui o bloco `espontaneidade`, que afirma "NO PEOPLE VISIBLE" e por isso
#: nao pode entrar em cena com gente. Preserva a funcao anti-anuncio dele.
AMADORA = """\
Phone photo, taken in about two seconds with one hand. Nobody composed it, nobody \
arranged anything, nobody moved anything into place for the photograph. The frame \
is tilted a couple of degrees, the horizon is not level, the subject sits off to \
one side, and the edges cut through things arbitrarily. The place is cluttered \
with the ordinary mess of somewhere in use. NOT a product photograph, NOT an \
advertisement, NOT a styled set."""

#: Cena urbana brasileira e feita das superficies que mais carregam marca. O
#: modelo preenche cada uma com um logotipo plausivel, e logotipo plausivel de
#: terceiro e marca de terceiro.
SEM_MARCA = """\
No third-party brand, logo, wordmark, emblem, badge, team crest or legible \
commercial name anywhere in the frame - not on bottles, crates, chairs, machines, \
appliances, tape, boxes, signs, vehicles, awnings, cups, flasks, trainers or \
clothing. Every bottle, crate, chair and appliance is plain and unbranded."""

#: Preservacao de embalagem. Verbatim de templates/blocos/preservar-embalagem.yaml.
#: Repare no que ele NAO faz: nao descreve a arte. Descrever faz redesenhar.
PRESERVAR = """\
One of the source images is a coffee package. Keep that package EXACTLY as it is: \
same paper, same colour, same printed artwork, every letter and every line \
identical, same proportions, same creases, same crimped top, same vent. Do not \
redraw, restyle, relabel or reinterpret it. Its label is legally exact. Only its \
LIGHTING should change, to match the light of the scene."""

NEG_BASE = (
    "beauty retouching, skin smoothing, airbrushed skin, poreless skin, "
    "symmetrical face, open mouth smile, perfect teeth, model, fashion model, "
    "stock photo look, uncanny face, extra fingers, malformed hand, "
    "glossy salon hair, floating hair, motion blur, "
    "blurred background, defocused background, background blur, bokeh, "
    "shallow focus, portrait mode, lens blur, "
    "studio lighting, softbox, reflector, rim light, "
    "product photography, catalogue photography, advertisement, "
    "commercial hero shot, symmetrical centred composition, tidy, "
    "golden hour, warm glow, amber light, orange grading, teal and orange, "
    "crushed blacks, deep black shadows, vibrant saturated colours, "
    "billboard, LED panel, large signage, graffiti mural, "
    "watermark, text overlay, 3d render, CGI, illustration"
)

NEG_ROTULO = "redrawn label, altered logo, changed lettering, restyled packaging, warped text, gibberish text"


@dataclass(frozen=True)
class Cena:
    slug: str
    aspecto: str
    avatar: str | None
    corpo: str
    luz: str
    packshots: tuple[Path, ...] = ()
    extra_neg: str = ""
    n_sugerido: int = 3

    def fontes(self) -> list[Path]:
        # AVATAR PRIMEIRO. No Gemini a proporcao vem explicita em
        # `imageConfig.aspectRatio`, entao a ordem nao decide enquadramento — mas
        # decide peso: na sonda com o packshot na frente o rosto derivou do
        # avatar. Com o rosto na frente ele segura.
        out: list[Path] = []
        if self.avatar:
            escolhido = sorted(ELENCO.glob(f"{self.avatar}-v*.jpg"))
            if not escolhido:
                raise SystemExit(
                    f"[{self.slug}] avatar ausente: rode scripts/home_avatares.py "
                    f"--quem {self.avatar}"
                )
            out.append(escolhido[0])
        out.extend(self.packshots)
        return out

    def prompt(self) -> str:
        partes = []
        if self.packshots:
            partes.append(PRESERVAR)
        if self.avatar:
            partes.append(IDENTIDADE)
        partes += [self.corpo, SEM_JOIA, SEM_MARCA, self.luz, HDR, FOCO, AMADORA]
        neg = NEG_BASE
        if self.packshots:
            neg += ", " + NEG_ROTULO
        if self.extra_neg:
            neg += ", " + self.extra_neg
        return "\n\n".join(partes) + f"\n\nAvoid: {neg}"


CENAS: tuple[Cena, ...] = ()  # preenchido em home_cenas_lista.py


def gerar(cenas: tuple[Cena, ...], n: int, seco: bool, tag: str) -> int:
    if seco:
        for c in cenas:
            print(f"\n{'=' * 70}\n{c.slug.upper()}  [{c.aspecto}]  fontes: "
                  f"{[f.name for f in c.fontes()]}\n{'=' * 70}")
            print(c.prompt())
        print(f"\n[seco] {sum(1 for _ in cenas) * n} imagem(ns) NAO geradas.")
        return 0

    load_dotenv(override=False)
    SAIDA.mkdir(parents=True, exist_ok=True)
    erros = 0
    for c in cenas:
        prov = ProvedorGemini(modelo=MODELO, tamanho=TAMANHO)
        fontes = c.fontes()
        print(f"[{c.slug}] {n}x {c.aspecto} <- {[f.name for f in fontes]}", flush=True)
        try:
            imgs = prov.gerar(c.prompt(), fontes=fontes, aspecto=c.aspecto, n=n)
        except ErroGemini as exc:
            print(f"[{c.slug}] FALHOU: {exc}", file=sys.stderr, flush=True)
            erros += 1
            continue
        for i, bruto in enumerate(imgs, start=1):
            d = SAIDA / f"{c.slug}{tag}-v{i}.jpg"
            d.write_bytes(bruto)
            print(f"[{c.slug}]   {d.name}  {len(bruto) // 1024} KB", flush=True)
    return 1 if erros else 0


def main() -> int:
    from home_cenas_lista import CENAS as LISTA  # noqa: PLC0415

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=0, help="0 = usa o n sugerido de cada cena")
    ap.add_argument("--cena", action="append")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    sel = LISTA if not a.cena else tuple(c for c in LISTA if c.slug in set(a.cena))
    if not sel:
        print("nenhuma cena casou", file=sys.stderr)
        return 2
    if a.n:
        return gerar(sel, a.n, a.dry_run, a.tag)
    # n por cena
    erros = 0
    for c in sel:
        erros |= gerar((c,), c.n_sugerido, a.dry_run, a.tag)
    return erros


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
