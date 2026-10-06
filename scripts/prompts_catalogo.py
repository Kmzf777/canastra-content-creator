"""Gera `docs/PROMPTS-ESTUDIO-CATALOGO.md` - os prompts do catalogo de estudio.

Por que um script e nao um arquivo escrito a mao: sao 85 prompts, e o que decide
se cada um funciona sao as strings impressas na embalagem. `SCA 80+` no saco e
`SCAA 80+` na capsula. `1Kg` com K maiusculo so no quilo. Selo circular no
Classico em graos e bloco de texto no Suave em graos, no mesmo peso. Escrito a
mao, uma dessas diferencas se perde numa copia-e-cola e o modelo imprime o erro
com toda a confianca do mundo.

Tudo aqui foi lido das fotos em `fotos produtos cru/` em zoom, nao inferido de um
SKU para outro. Onde a leitura nao deu certeza - as letras miudas do verso - o
prompt manda copiar da foto em vez de soletrar, porque uma transcricao minha
errada e pior que nenhuma.

    python scripts/prompts_catalogo.py            # escreve o .md
    python scripts/prompts_catalogo.py --conferir # so valida as fontes citadas
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CRU = RAIZ / "fotos produtos cru"
DESTINO = RAIZ / "docs" / "PROMPTS-ESTUDIO-CATALOGO.md"
ANCORA = "saida-teste/site-fundo-branco/FINAL-suave-250g-branco.jpg"


# --------------------------------------------------------------------------- #
# blocos reaproveitados
# --------------------------------------------------------------------------- #

#: O tratamento de estudio. Identico em todas as imagens do catalogo - e o que faz o
#: catalogo parecer uma sessao so, e nao 85 fotos avulsas.
ESTUDIO = """\
STUDIO TREATMENT — identical across the whole catalogue. A clean commercial \
packshot on a seamless white cove: white sweep curving from wall to floor with no \
visible horizon line, no seam, no corner, no table, no surface texture, no props. \
One large softbox as key light from the upper left, a white bounce card on the \
right lifting the shadow side, and a narrow top kicker separating the top edge of \
the pack from the background. The white is bright and even, with at most a very \
faint neutral falloff near the outer corners. Directly beneath the base, a soft \
short CONTACT SHADOW — diffuse, neutral grey, no hard edge, no long cast shadow, \
no mirror reflection. Neutral daylight white balance: the warm tungsten cast of \
the reference photograph must be gone, the whites must read white.

EVERYTHING IN FRAME IS SHARP — deep depth of field, the whole package equally \
crisp from the nearest fold to the far edge. No background blur, no bokeh, no \
vignette, no glow, no lens flare, no added props, no added text, no watermark, no \
reflection of the package on the floor."""

#: O que impede o "heroi de produto" com camera no chao e o pacote tombando.
def enquadramento(ocupacao: int, orientacao: str = "straight on, front face square to the camera") -> str:
    return (
        f"FRAMING — vertical portrait, 3:4 aspect ratio (width:height = 3:4). The "
        f"package stands upright and centred, seen {orientacao}, at eye level with the "
        f"camera at the package's mid-height so the vertical edges stay parallel. No "
        f"low hero angle, no tilt, no wide-angle perspective distortion, no leaning. "
        f"The package occupies about {ocupacao}% of the frame height, with even "
        f"margins left and right and the base sitting a little below centre."
    )


#: Erro caro o suficiente para virar paragrafo proprio: o modelo redesenha a
#: tipografia mesmo quando o pedido e so de luz e fundo.
FIDELIDADE = """\
LABEL FIDELITY — this is the part that fails. Reproduce the printed artwork \
exactly as specified below: same layout, same proportions, same wording, same \
accents, letter for letter. Do not re-typeset it, do not translate it, do not \
paraphrase it, do not tidy it up, do not invent extra lines, do not add a barcode \
or a QR code that is not described. Every character listed must be legible and \
spelled exactly as written."""

LOGO = (
    'the Café Canastra logo lockup — a mountain ridge drawn in thin sketchy open '
    'line, a LOW, WIDE, FLAT-TOPPED tableland: an almost horizontal plateau '
    'escarpment with shallow irregular notches and one gently rounded high point, '
    'never sharp alpine peaks, with three tiny V-shaped bird marks at its far upper '
    'left; overlapping and in front of that ridge, slightly right of centre, the '
    'word "Café" written small in slanted handwriting AND CARRYING AN ACUTE ACCENT '
    'over the e; directly below, very large, "CANASTRA" spelled C-A-N-A-S-T-R-A in a '
    'thick dry-brush script with uneven, partly broken strokes; a single heavy '
    'tapering brush swash sweeping underneath it, thick at the left and thinning to '
    'a point at the right; a very small ® at the upper right of the final A; and '
    '"Desde 1985" small and handwritten at the lower right, just above the tip of '
    'the swash'
)

#: O bloco GOURMET/ESPECIAL/SCAA 80+ das tres caixas de capsula. Medido em
#: 04/10/2026: nos TRES SKUs ele e desenhado com quatro cantos, nao com
#: retangulo continuo. O script descrevia 'thin rectangle outline' no Classico
#: e no Canela - erro meu, lido por analogia e nao no pixel.
CANTOS = (
    'a rectangle outline drawn as FOUR CORNER BRACKETS rather than a continuous '
    'line — each corner is an L of rule and the middle of every side is open — '
    'containing '
)

CAIXA_SCA = (
    'a thin single-line rectangle outline containing three stacked lines: '
    '"SPECIALTY" small and letterspaced, spelled S-P-E-C-I-A-L-T-Y, then "ESPECIAL" '
    'large and bold, then "SCA 80+"'
)

SELO_GRAOS = (
    'a round seal outline reading "CLÁSSICO EM GRÃOS" along its upper arc and '
    '"TORRA EXCLUSIVA" along its lower arc, with a single coffee-bean icon in the '
    'centre'
)


def peso(valor: str) -> str:
    return f'a small rounded rectangle outline containing "{valor}"'


def linha_dupla(a: str, b: str) -> str:
    return (
        f'small sans-serif caps on two lines, "{a}" over "{b}"'
    )


# --------------------------------------------------------------------------- #
# catalogo
# --------------------------------------------------------------------------- #


@dataclass
class Produto:
    slug: str
    nome: str
    pasta: str
    familia: str          # saco | doypack | caixa
    corpo: str            # material e cor, como o modelo precisa ouvir
    fundo: str            # de onde sai a cor do fundo colorido
    ocupacao: int         # % da altura do quadro
    frente: str
    verso: str
    arte: str
    lateral_ref: str = ""  # foto crua em angulo, mostra a sanfona real (familia saco/doypack)
    laterais: list[tuple[str, str]] = field(default_factory=list)  # (rotulo, fonte|'')
    # rotulo -> texto extra anexado ao prompt daquela lateral. Existe para o caso
    # em que a foto crua nao da para ler: melhor soletrar um valor conferido com o
    # cliente do que mandar o modelo "copiar" algo ilegivel e aceitar o que vier.
    lateral_extra: dict[str, str] = field(default_factory=dict)
    # Familia capsula: a capsula de plastico de verdade, fotografada solta.
    # So preenchido onde ela existe - e so onde a cor foi LIDA numa foto da
    # capsula real, nunca copiada da ilustracao impressa na caixa. A caixa do
    # Canela desenha uma capsula VINHO e a capsula de verdade e COBRE: arte
    # impressa nao e fonte de cor de capsula.
    capsula_corpo: str = ""   # descricao fisica, lida no pixel da foto crua
    capsula_fonte: str = ""   # caminho, a partir de RAIZ, da foto da capsula real
    capsula_nota: str = ""    # ressalva de procedencia, impressa no .md

    @property
    def dir(self) -> Path:
        return CRU / self.pasta


#: A geometria da capsula, igual nos tres SKUs. Lida nas fotos cruas
#: `capsulas-classico-detalhe-06/07.jpg` e `capsulas-canela-detalhe-07/08.jpg`,
#: ampliadas 3x: a tampa de aluminio e LISA, sem impressao nenhuma - nao ha logo,
#: letra nem codigo nela. Se a geracao imprimir qualquer coisa na tampa, errou.
CAPSULA_FORMA = (
    "a Nespresso-compatible espresso capsule: a small truncated cone, WIDE at the "
    "open end where a crimped rim flange runs all the way round, tapering upward to "
    "a narrow rounded dome at the closed end, with a shallow concentric step moulded "
    "into the dome and a tiny centre pip. The flange is sealed with a smooth SILVER "
    "aluminium foil lid that is completely BLANK — no logo, no lettering, no number, "
    "no code, no printing of any kind on the foil. The crimped edge of the flange "
    "shows fine regular radial knurling and reads as bare bright metal"
)

#: O corpo, por SKU. Preto do Classico e do Suave conferido com o Arthur em
#: 04/10/2026: a capsula Suave e preta, identica a do Classico - so a caixa muda.
CAPSULA_PRETA = (
    "The body is opaque GLOSSY BLACK plastic, deep neutral black with no brown and "
    "no blue in it, carrying one soft vertical specular highlight down the lit side "
    "and a long dark reflection on the shadow side"
)
CAPSULA_COBRE = (
    "The body is COPPER metallic — a warm polished orange-brown metal finish with a "
    "bright specular band running round the taper. It is NOT wine red, NOT maroon "
    "and NOT the colour of the band on the carton: the capsule printed in the "
    "carton's own artwork is drawn wine red, and the real capsule is copper. The "
    "upper face of the flange carries the same copper colour; the outer crimped edge "
    "and the foil lid underneath it are silver"
)


def capsula_enq(altura: int, arranjo: str) -> str:
    """Enquadramento para as tomadas em que a capsula e o assunto.

    A capsula tem 37 mm; a caixa de 10 unidades mede por volta de 115 mm de
    altura (largura ~76 mm, exigida pelos 37 mm de diametro da capsula na
    profundidade que a propria descricao do corpo declara, "half as deep as it is
    wide"). Dai o um terco do bloco de conjunto - derivado, nao chutado.
    """
    return (
        f"FRAMING — vertical portrait, 3:4 aspect ratio (width:height = 3:4). "
        f"{arranjo} The camera is at eye level with the subject, only very slightly "
        f"above it — just enough that the top dome reads as a dome — square to the "
        f"group, no low hero angle, no top-down view, no wide-angle distortion. A "
        f"standing capsule occupies about {altura}% of the frame height, the group "
        f"centred with even margins left and right and resting a little below centre."
    )


SACO_SUAVE = (
    "a 250g-style flat-bottom KRAFT PAPER pouch: natural unbleached brown paper, "
    "matte, visibly fibrous, with inward side gussets and a straight crimped top "
    "fold — not a zip lock, not a plastic slider. A small round embossed degassing "
    "vent with one dark centre dot sits on the front panel above the artwork. All "
    "printing is flat matte BLACK ink laid directly on the bare kraft: no white "
    "label, no sticker, no gloss, no foil"
)
SACO_CLASSICO = (
    "a flat-bottom pouch in MATTE BLACK film with a wide soft diffuse sheen, inward "
    "side gussets and a straight crimped top fold — not a zip lock, not a plastic "
    "slider. A round embossed degassing vent with one dark centre dot sits on the "
    "front panel above the artwork. All printing is flat WHITE ink on the black film"
)
SACO_CANELA = (
    "a flat-bottom pouch in GLOSSY RED METALLIC film with strong specular highlights "
    "running in broad bands across the surface, inward side gussets and a straight "
    "crimped top fold. A round embossed degassing vent with one dark centre dot sits "
    "on the front panel above the artwork. All printing is flat WHITE ink on the red foil"
)


def arte_saco(bloco_inferior: str, peso_txt: str, com_caixa: bool = True) -> str:
    partes = [f"On the front panel, top to bottom: {LOGO}."]
    if com_caixa:
        partes.append(f"Below the swash, centred, {CAIXA_SCA}.")
    partes.append(f"Bottom left, {bloco_inferior}.")
    partes.append(f"Bottom right, {peso(peso_txt)}.")
    return " ".join(partes)


PRODUTOS: list[Produto] = [
    # ---------------- Suave ----------------
    Produto(
        "suave-250g-moido", "Canastra Suave 250g — Torrado e Moído",
        "Canastra-Suave-250g-Moido", "saco", SACO_SUAVE,
        "the kraft paper of the pouch itself — a warm natural tan", 56,
        "suave-250g-moido-frente-01.jpg", "suave-250g-moido-verso-06.jpg",
        arte_saco(linha_dupla("SUAVE", "TORRADO E MOÍDO"), "250g"),
        lateral_ref="suave-250g-moido-frente-05.jpg",
    ),
    Produto(
        "suave-250g-graos", "Canastra Suave 250g — Torrado em Grãos",
        "Canastra-Suave-250g-Graos", "saco", SACO_SUAVE,
        "the kraft paper of the pouch itself — a warm natural tan", 56,
        "suave-250g-graos-frente-01.jpg", "suave-250g-graos-verso-04.jpg",
        arte_saco(linha_dupla("SUAVE", "TORRADO EM GRÃOS"), "250g"),
        lateral_ref="suave-250g-graos-frente-03.jpg",
    ),
    Produto(
        "suave-500g-moido", "Canastra Suave 500g — Torrado e Moído",
        "Canastra-Suave-500g-Moido", "saco", SACO_SUAVE,
        "the kraft paper of the pouch itself — a warm natural tan", 70,
        "suave-500g-moido-frente-01.jpg", "suave-500g-moido-verso-05.jpg",
        arte_saco(linha_dupla("SUAVE", "TORRADO E MOÍDO"), "500g"),
        lateral_ref="suave-500g-moido-frente-04.jpg",
    ),
    Produto(
        "suave-500g-graos", "Canastra Suave 500g — Torrado em Grãos",
        "Canastra-Suave-500g-Graos", "saco", SACO_SUAVE,
        "the kraft paper of the pouch itself — a warm natural tan", 70,
        "suave-500g-graos-frente-01.jpg", "suave-500g-graos-verso-05.jpg",
        arte_saco(linha_dupla("SUAVE", "TORRADO EM GRÃOS"), "500g"),
        lateral_ref="suave-500g-graos-frente-04.jpg",
    ),
    Produto(
        "suave-1kg-graos", "Canastra Suave 1kg — Torrado em Grãos",
        "Canastra-Suave-1kg-Graos", "saco", SACO_SUAVE,
        "the kraft paper of the pouch itself — a warm natural tan", 88,
        "suave-1kg-graos-frente-01.jpg", "suave-1kg-graos-verso-05.jpg",
        arte_saco(
            'two lines in title case, not full caps: "Suave" over "Torrado em grãos"',
            "1Kg",
        ),
        lateral_ref="suave-1kg-graos-frente-04.jpg",
    ),
    # ---------------- Clássico ----------------
    Produto(
        "classico-250g-moido", "Canastra Clássico 250g — Torrado e Moído",
        "Canastra-Classico-250g-Moido", "saco", SACO_CLASSICO,
        "the matte black film of the pouch itself", 56,
        "classico-250g-moido-frente-01.jpg", "classico-250g-moido-verso-06.jpg",
        arte_saco(linha_dupla("CLÁSSICO", "TORRADO E MOÍDO"), "250g"),
        lateral_ref="classico-250g-moido-frente-05.jpg",
    ),
    Produto(
        "classico-250g-graos", "Canastra Clássico 250g — Torrado em Grãos",
        "Canastra-Classico-250g-Graos", "saco", SACO_CLASSICO,
        "the matte black film of the pouch itself", 56,
        "classico-250g-graos-frente-02.jpg", "classico-250g-graos-verso-07.jpg",
        arte_saco(SELO_GRAOS, "250g"),
        lateral_ref="classico-250g-graos-frente-06.jpg",
    ),
    Produto(
        "classico-500g-moido", "Canastra Clássico 500g — Torrado e Moído",
        "Canastra-Classico-500g-Moido", "saco", SACO_CLASSICO,
        "the matte black film of the pouch itself", 70,
        "classico-500g-moido-frente-01.jpg", "classico-500g-moido-verso-04.jpg",
        arte_saco(linha_dupla("CLÁSSICO", "TORRADO E MOÍDO"), "500g"),
        lateral_ref="classico-500g-moido-frente-03.jpg",
    ),
    Produto(
        "classico-500g-graos", "Canastra Clássico 500g — Torrado em Grãos",
        "Canastra-Classico-500g-Graos", "saco", SACO_CLASSICO,
        "the matte black film of the pouch itself", 70,
        "classico-500g-graos-frente-01.jpg", "classico-500g-graos-verso-06.jpg",
        arte_saco(SELO_GRAOS, "500g"),
        lateral_ref="classico-500g-graos-frente-05.jpg",
    ),
    Produto(
        "classico-1kg-graos", "Canastra Clássico 1kg — Torrado em Grãos",
        "Canastra-Classico-1kg-Graos", "saco", SACO_CLASSICO,
        "the matte black film of the pouch itself", 88,
        "classico-1kg-graos-frente-01.jpg", "classico-1kg-graos-verso-04.jpg",
        arte_saco(
            'two lines in title case, not full caps: "Clássico" over "Torrado em grãos"',
            "1Kg",
        ),
        lateral_ref="classico-1kg-graos-frente-03.jpg",
    ),
    # ---------------- Canela ----------------
    Produto(
        "canela-250g-moido", "Canastra Canela 250g — Torrado e Moído com Canela",
        "Canastra-Canela-250g-Moido", "saco", SACO_CANELA,
        "the glossy red metallic film of the pouch itself", 56,
        "canela-250g-moido-frente-01.jpg", "canela-250g-moido-verso-04.jpg",
        (
            f"On the front panel, top to bottom: {LOGO}. This SKU has NO rectangular "
            "SPECIALTY / ESPECIAL / SCA 80+ box — do not add one. In the lower right, "
            "above the weight badge, a white line drawing of two tied cinnamon quills. "
            'Bottom left, small sans-serif caps on two lines, "CAFÉ TORRADO E" over '
            '"MOÍDO COM CANELA", with the acute accent on the final E of CAFÉ and on '
            f"the I of MOÍDO. Bottom right, {peso('250g')}."
        ),
        lateral_ref="canela-250g-moido-frente-03.jpg",
    ),
    # ---------------- Microlote ----------------
    Produto(
        "microlote-250g-graos", "Microlote 250g — Torrado em Grãos",
        "Microlote-250g-Graos", "doypack",
        (
            "a 250g stand-up KRAFT PAPER doypack: natural unbleached brown paper, "
            "matte and fibrous, with a rounded top, a pressed seal across the top edge "
            "and inward side gussets, wider and shorter than a block-bottom bag. A "
            "round embossed degassing vent with one dark centre dot sits high on the "
            "front panel. All printing is BLACK ink on the bare kraft, except one red "
            "stamp"
        ),
        "the kraft paper of the pouch itself — a warm natural tan", 52,
        "microlote-250g-graos-frente-01.jpg", "microlote-250g-graos-verso-05.jpg",
        (
            f"On the front panel: at the top, {LOGO}, drawn smaller than on the "
            "standard bags. To its right, a round WHITE seal with black type reading "
            '"CAFÉ TORRADO" along the upper arc and "EM GRÃOS" along the lower arc, '
            "around a single coffee-bean icon. Filling the middle and lower panel, a "
            "large black halftone illustration of a tall waterfall falling into a "
            "valley, with flying birds and, at the lower left, a maned wolf standing "
            "in profile on a rocky outcrop with low scrub. Over the illustration at "
            'the right, a RED circular rubber stamp reading "MICROLOTE LIMITADO" '
            'around "86 PONTOS SCAA" with three small stars below. Running vertically '
            'up the left edge of the panel, small type: "Cachoeira Casca d\'Anta   MG   '
            'Brasil". At the bottom, in brush script, "Café Especial", and under it in '
            'small letterspaced caps "MICRORREGIÃO SERRA DA CANASTRA". Bottom right, '
            'small "PESO LÍQ." above a larger "250g"'
        ),
        lateral_ref="microlote-250g-graos-frente-04.jpg",
    ),
    Produto(
        "microlote-250g-moido", "Microlote 250g — Torrado e Moído",
        "Microlote-250g-Moido", "doypack",
        (
            "a 250g stand-up KRAFT PAPER doypack: natural unbleached brown paper, "
            "matte and fibrous, with a rounded top, a pressed seal across the top edge "
            "and inward side gussets, wider and shorter than a block-bottom bag. A "
            "round embossed degassing vent with one dark centre dot sits high on the "
            "front panel. All printing is BLACK ink on the bare kraft, except one red "
            "stamp"
        ),
        "the kraft paper of the pouch itself — a warm natural tan", 52,
        "microlote-250g-moido-frente-01.jpg", "microlote-250g-moido-verso-04.jpg",
        (
            f"On the front panel: at the top, {LOGO}, drawn smaller than on the "
            "standard bags. To its right, a round WHITE seal with black type reading "
            '"PARA COADOR" around a filter icon. Filling the middle and lower panel, a '
            "large black halftone illustration of a tall waterfall falling into a "
            "valley, with flying birds and, at the lower left, a maned wolf standing "
            "in profile on a rocky outcrop with low scrub. Over the illustration at "
            'the right, a RED circular rubber stamp reading "MICROLOTE LIMITADO" '
            'around "86 PONTOS SCAA" with three small stars below. Running vertically '
            'up the left edge of the panel, small type: "Cachoeira Casca d\'Anta   MG   '
            'Brasil". At the bottom, in brush script, "Café Especial", and under it in '
            'small letterspaced caps "MICRORREGIÃO SERRA DA CANASTRA". Bottom right, '
            'small "PESO LÍQ." above a larger "250g"'
        ),
        lateral_ref="microlote-250g-moido-frente-03.jpg",
    ),
    # ---------------- Néctar de Minas ----------------
    Produto(
        "nectar-1kg-graos", "Néctar de Minas Gourmet 1kg — Torrado em Grãos",
        "Nectar-de-Minas-Gourmet-1kg-Graos", "saco",
        (
            "a flat-bottom pouch in BLACK film with a soft satin sheen, inward side "
            "gussets whose folded edges catch the light as two lighter vertical "
            "bands, and a straight crimped top fold. A round embossed degassing vent "
            "with one dark centre dot sits high on the front panel. All printing is "
            "flat WHITE ink on the black film. This is the Néctar de Minas line — it "
            "does NOT carry the Café Canastra mountain logo"
        ),
        "the black film of the pouch itself", 88,
        "nectar-gourmet-1kg-graos-frente-01.jpg", "nectar-gourmet-1kg-graos-verso-04.jpg",
        (
            "On the front panel, centred and stacked: a solid white water-drop icon; "
            'below it, large hand-drawn chunky display lettering reading "NÉCTAR" on '
            'the first line — with an acute accent on the E — then "de MINAS" on the '
            "second, the words nested and slightly overlapping, with rough irregular "
            'letterforms; below that, in a relaxed script, "Café Gourmet" with an '
            "acute accent on the e; and below that a two-row box drawn in thin white "
            'rule: the upper row reads "1kg", then a short run of slashes, then "100% '
            'ARÁBICA"; the lower row reads "TORRADO EM GRÃOS"'
        ),
        lateral_ref="nectar-gourmet-1kg-graos-frente-03.jpg",
    ),
    Produto(
        "nectar-500g-moido", "Néctar de Minas Gourmet 500g — Torrado e Moído",
        "Nectar-de-Minas-Gourmet-500g-Moido", "saco",
        (
            "a flat-bottom pouch in BLACK film with a soft satin sheen, inward side "
            "gussets whose folded edges catch the light as two lighter vertical "
            "bands, and a straight crimped top fold. A round embossed degassing vent "
            "with one dark centre dot sits high on the front panel. All printing is "
            "flat WHITE ink on the black film. This is the Néctar de Minas line — it "
            "does NOT carry the Café Canastra mountain logo"
        ),
        "the black film of the pouch itself", 70,
        "nectar-gourmet-500g-moido-frente-01.jpg", "nectar-gourmet-500g-moido-verso-04.jpg",
        (
            "On the front panel, centred and stacked: a solid white water-drop icon; "
            'below it, large hand-drawn chunky display lettering reading "NÉCTAR" on '
            'the first line — with an acute accent on the E — then "de MINAS" on the '
            "second, the words nested and slightly overlapping, with rough irregular "
            'letterforms; below that, in a relaxed script, "Café Gourmet" with an '
            "acute accent on the e; and below that a two-row box drawn in thin white "
            'rule: the upper row reads "500g", then a short run of slashes, then "100% '
            'ARÁBICA"; the lower row reads "TORRADO & MOÍDO", with the acute accent on '
            "the I of MOÍDO"
        ),
        lateral_ref="nectar-gourmet-500g-moido-frente-08.jpg",
    ),
    # ---------------- Cápsulas ----------------
    Produto(
        "capsulas-classico", "Cápsulas Clássico — 10 un. de 5g",
        "Capsulas-Classico-10un-5g", "caixa",
        (
            "a small upright KRAFT CARDBOARD carton, matte uncoated board with visible "
            "fibre, noticeably taller than wide and about half as deep as it is wide, "
            "with crisp square corners and a solid BLACK printed band wrapping the top "
            "of the box including the top face. All other printing is BLACK ink on the "
            "bare kraft"
        ),
        "the black band at the top of the carton", 56,
        "capsulas-classico-frente-01.jpg", "capsulas-classico-verso-04.jpg",
        (
            'On the front face, top to bottom: across the black top band, in white '
            'letterspaced caps, "COMPATÍVEIS COM SISTEMA NESPRESSO". Below the band, '
            'small widely letterspaced caps, "C Á P S U L A S". Then ' + LOGO + ". "
            "Below the logo, a colour product photograph of one espresso capsule "
            "standing upright — black body, silver foil lid — with two more capsules "
            "lying behind it, a few roasted coffee beans and two small green coffee "
            "leaves at its left. To the right of that photograph, a rounded rectangle "
            'outline containing "CLÁSSICO", and under it two small lines, "CONTEÚDO" '
            'over "10un. DE 5g.". Lower centre, ' + CANTOS + 'three stacked lines, "GOURMET" small, "ESPECIAL" large, and "SCAA 80+" — '
            "note SCAA with two A, not SCA. At the very bottom, centred in small caps, "
            '"INDÚSTRIA BRASILEIRA"'
        ),
        laterais=[
            ("lateral esquerda", "capsulas-classico-lateral-02.jpg"),
            ("lateral direita", "capsulas-classico-lateral-03.jpg"),
        ],
        capsula_corpo=CAPSULA_PRETA,
        capsula_fonte="saida-teste/catalogo-estudio/_capsulas-recorte/capsula-classico-ref.jpg",
    ),
    Produto(
        "capsulas-canela", "Cápsulas Canela — 10 un. de 5g",
        "Capsulas-Canela-10un-5g", "caixa",
        (
            "a small upright KRAFT CARDBOARD carton, matte uncoated board with visible "
            "fibre, noticeably taller than wide and about half as deep as it is wide, "
            "with crisp square corners and a solid DEEP WINE RED printed band wrapping "
            "the top of the box including the top face. All other printing is BLACK "
            "ink on the bare kraft"
        ),
        "the deep wine red band at the top of the carton", 56,
        "capsulas-canela-frente-01.jpg", "capsulas-canela-verso-03.jpg",
        (
            'On the front face, top to bottom: across the wine red top band, in white '
            'letterspaced caps, "COMPATÍVEIS COM SISTEMA NESPRESSO". Below the band, '
            'small widely letterspaced caps, "C Á P S U L A S". Then ' + LOGO + ". "
            "Below the logo, a colour product photograph of one espresso capsule "
            "standing upright — wine red body, silver foil lid — with two more "
            "capsules lying behind it and a small bundle of cinnamon quills at its "
            "right. To the right of that photograph, a rounded rectangle outline "
            'containing "CANELA", and under it two small lines, "CONTEÚDO" over '
            '"10un. DE 5g.". Lower centre, ' + CANTOS + 'three stacked lines, "GOURMET" small, "ESPECIAL" large, and "SCAA 80+" — note '
            "SCAA with two A, not SCA. At the very bottom, centred in small caps, "
            '"INDÚSTRIA BRASILEIRA"'
        ),
        laterais=[
            ("lateral esquerda", "capsulas-canela-lateral-04.jpg"),
            ("lateral direita", "capsulas-canela-lateral-05.jpg"),
        ],
        capsula_corpo=CAPSULA_COBRE,
        capsula_fonte="saida-teste/catalogo-estudio/_capsulas-recorte/capsula-canela-ref.jpg",
    ),
    # ---------------- Drip ----------------
    Produto(
        "drip-classico", "Drip Coffee Clássico 100g — 10 sachês",
        "Drip-Coffee-Classico-100g", "caixa",
        (
            "a small upright KRAFT CARDBOARD carton, matte uncoated board with visible "
            "fibre, roughly as wide as it is tall and about two thirds as deep, with "
            "crisp square corners and a solid BLACK printed band wrapping the top of "
            "the box including the top face. All other printing is BLACK ink on the "
            "bare kraft"
        ),
        "the black band at the top of the carton", 62,
        "drip-classico-100g-frente-01.jpg", "drip-classico-100g-verso-03.jpg",
        (
            "On the front face, top to bottom: across the black top band, in white "
            'widely letterspaced caps, "D R I P   C O F F E E". Below the band, ' + LOGO
            + f". Below the logo, centred, {CAIXA_SCA}. Filling the lower left, a black "
            "line drawing of a single-serve drip bag with its two paper arms hooked "
            "over the rim of a wide mug. To the right of that drawing, a rounded "
            'rectangle outline containing "CLÁSSICO" in letterspaced caps, and '
            'immediately under it, smaller, "DARK ROAST". Below that, a rounded '
            'rectangle outline containing two lines, "CAFÉ FILTRADO" over "INDIVIDUAL". '
            'Bottom right, a large "100g", and beside it in three tiny lines "Peso Neto '
            '100g e", "Net Wt. 3.52oz"; to their right, set off by a thin vertical '
            'rule, three more tiny lines, "Contém 10 sachês", "Contiene 10 bolsitas", '
            '"10 servings"'
        ),
        laterais=[
            ("lateral esquerda", "drip-classico-100g-lateral-04.jpg"),
            ("lateral direita", "drip-classico-100g-lateral-05.jpg"),
        ],
    ),
    Produto(
        "drip-suave", "Drip Coffee Suave 100g — 10 sachês",
        "Drip-Coffee-Suave-100g", "caixa",
        (
            "a small upright KRAFT CARDBOARD carton, matte uncoated board with visible "
            "fibre, roughly as wide as it is tall and about two thirds as deep, with "
            "crisp square corners and a solid MUTED BRICK RED printed band wrapping "
            "the top of the box including the top face. All other printing is BLACK "
            "ink on the bare kraft"
        ),
        "the muted brick red band at the top of the carton", 62,
        "drip-suave-100g-frente-01.jpg", "drip-suave-100g-verso-04.jpg",
        (
            "On the front face, top to bottom: across the brick red top band, in white "
            'widely letterspaced caps, "D R I P   C O F F E E". Below the band, ' + LOGO
            + f". Below the logo, centred, {CAIXA_SCA}. Filling the lower left, a black "
            "line drawing of a single-serve drip bag with its two paper arms hooked "
            "over the rim of a wide mug. To the right of that drawing, a rounded "
            'rectangle outline containing "SUAVE" in letterspaced caps, and immediately '
            'under it, smaller, "MEDIUM ROAST". Below that, a rounded rectangle outline '
            'containing two lines, "CAFÉ FILTRADO" over "INDIVIDUAL". Bottom right, a '
            'large "100g", and beside it in three tiny lines "Peso Neto 100g e", "Net '
            'Wt. 3.52oz"; to their right, set off by a thin vertical rule, three more '
            'tiny lines, "Contém 10 sachês", "Contiene 10 bolsitas", "10 servings"'
        ),
        laterais=[
            ("lateral esquerda", "drip-suave-100g-lateral-02.jpg"),
            ("lateral direita", "drip-suave-100g-lateral-03.jpg"),
        ],
    ),
    Produto(
        "drip-canela", "Drip Coffee Canela 100g — 10 sachês",
        "Drip-Coffee-Canela-100g", "caixa",
        (
            "a small upright KRAFT CARDBOARD carton, matte uncoated board with visible "
            "fibre, roughly as wide as it is tall and about two thirds as deep, with "
            "crisp square corners and a solid DEEP WINE RED printed band wrapping the "
            "top of the box including the top face. All other printing is BLACK ink on "
            "the bare kraft"
        ),
        "the deep wine red band at the top of the carton", 62,
        "drip-canela-100g-frente-01.jpg", "drip-canela-100g-verso-04.jpg",
        (
            "On the front face, top to bottom: across the wine red top band, in white "
            'widely letterspaced caps, "D R I P   C O F F E E". Below the band, ' + LOGO
            + f". Below the logo, centred, {CAIXA_SCA}. Filling the lower left, a black "
            "line drawing of a single-serve drip bag with its two paper arms hooked "
            "over the rim of a wide mug, with two cinnamon quills lying against the "
            "foot of the mug. To the right of that drawing, a rounded rectangle outline "
            'containing "CANELA" in letterspaced caps, and immediately under it, '
            'smaller, "WITH CINNAMON". Below that, a rounded rectangle outline '
            'containing two lines, "CAFÉ FILTRADO" over "INDIVIDUAL". Bottom right, a '
            'large "100g", and beside it in three tiny lines "Peso Neto 100g e", "Net '
            'Wt. 3.52oz"; to their right, set off by a thin vertical rule, three more '
            'tiny lines, "Contém 10 sachês", "Contiene 10 bolsitas", "10 servings"'
        ),
        laterais=[
            ("lateral esquerda", "drip-canela-100g-lateral-02.jpg"),
            ("lateral direita", "drip-canela-100g-lateral-03.jpg"),
        ],
    ),
    # ---------------- Cápsulas Suave ----------------
    # Entrou depois dos 20 primeiros, por isso vem no fim e não junto das outras
    # cápsulas: inserir no meio renumeraria 18-20, que já estão gerados em disco.
    # As fotos cruas vieram por WhatsApp em 591x1280 — um oitavo da área das
    # outras cápsulas. O que não deu para ler em zoom (AROMA e DOÇURA nas barras
    # da lateral esquerda) não está soletrado aqui de propósito: o prompt de
    # lateral já manda copiar da foto, e chute meu vira erro impresso.
    Produto(
        "capsulas-suave", "Cápsulas Suave — 10 un. de 5g",
        "Capsulas-Suave-10un-5g", "caixa",
        (
            "a small upright KRAFT CARDBOARD carton, matte uncoated board with visible "
            "fibre, noticeably taller than wide and about half as deep as it is wide, "
            "with crisp square corners and a solid DARK CHOCOLATE BROWN printed band "
            "wrapping the top of the box including the top face — a warm deep brown, "
            "clearly brown rather than black and darker than the kraft. All other "
            "printing is BLACK ink on the bare kraft"
        ),
        "the dark chocolate brown band at the top of the carton", 56,
        "capsulas-suave-frente-01.jpg", "capsulas-suave-verso-02.jpg",
        (
            'On the front face, top to bottom: across the dark brown top band, in white '
            'letterspaced caps, "COMPATÍVEIS COM SISTEMA NESPRESSO". Below the band, '
            'small widely letterspaced caps, "C Á P S U L A S". Then ' + LOGO + ". "
            "Below the logo, a colour product photograph of espresso capsules: one "
            "capsule in the foreground seen from a raised angle, its body a warm "
            "reddish BROWN and its CREAM-WHITE foil lid peeled back and curling up and "
            "over the open cup, and a second capsule behind it to the right showing "
            "its cream-white foil lid face on, with a third brown capsule body just "
            "visible behind that. No coffee beans, no leaves, no cinnamon. To the "
            "right of that photograph, a short curved leader line pointing to a "
            'rounded rectangle outline containing "SUAVE" in letterspaced caps, and '
            'under it two small lines, "CONTEÚDO" over "10un. DE 5g.". Lower centre, a '
            "rectangle outline drawn as four corner brackets rather than a continuous "
            'line, containing three stacked lines, "GOURMET" small, "ESPECIAL" large, '
            'and "SCAA 80+" — note SCAA with two A, not SCA. At the very bottom, '
            'centred in small caps, "INDÚSTRIA BRASILEIRA"'
        ),
        laterais=[
            ("lateral esquerda", "capsulas-suave-lateral-03.jpg"),
            ("lateral direita", "capsulas-suave-lateral-04.jpg"),
        ],
        lateral_extra={
            # As notas nao dao para ler na foto do WhatsApp: as barras de AROMA e
            # DOCURA estao 100% cheias e o numero fica preto sobre preto. Sem isso
            # soletrado, o modelo inventa - a primeira geracao saiu "70 / 80 / 80 /
            # 40". Valores confirmados com o Arthur em 25/09/2026.
            "lateral esquerda": (
                "The reference photo is low resolution. The roast label is "
                '"TORRA MÉDIA" on ONE line — it is NOT "TORRA MÉDIA ESCURA". The '
                "four rating rows must carry exactly these values, with a comma as "
                'the decimal mark: CORPO "7,0" with the track about 70% filled; '
                'AROMA "10" with the track completely full end to end, the number '
                'reading over the black fill; DOÇURA "10", also completely full; '
                'CITRICIDADE "6,0" with the track about 60% filled. Do not write '
                "these as 70, 80 or 40 — CORPO is seven comma zero and CITRICIDADE "
                "is six comma zero."
            ),
        },
        # Nao existe foto da capsula Suave de fato: a pasta so tem 4 fotos da
        # CAIXA, vindas por WhatsApp. A ilustracao impressa desenha uma capsula
        # marrom, e arte impressa nao serve de fonte - no Canela ela desenha
        # vinho onde a capsula real e cobre. Cor confirmada com o Arthur em
        # 04/10/2026: a capsula Suave e PRETA, a mesma do Classico. Por isso a
        # fonte de pixel aqui e a foto do Classico, com o papel declarado no
        # proprio prompt.
        capsula_corpo=CAPSULA_PRETA,
        capsula_fonte="saida-teste/catalogo-estudio/_capsulas-recorte/capsula-classico-ref.jpg",
        capsula_nota=(
            "A foto da cápsula é a do **Clássico**: a cápsula Suave é idêntica — preta, "
            "tampa prata — confirmado com o Arthur em 04/10/2026, porque não existe foto "
            "da cápsula Suave de fato. Ela entra só como fonte de **forma, cor e luz da "
            "cápsula**; a caixa vem inteira da imagem 1."
        ),
    ),
]


# --------------------------------------------------------------------------- #
# montagem dos 4 tipos de tomada
# --------------------------------------------------------------------------- #


def p_frente_branco(p: Produto) -> str:
    return "\n\n".join([
        "Create a studio product photograph of the coffee package shown in the "
        "attached reference photo. The second attached image is the STYLE ANCHOR: "
        "match its lighting, its white background, its neutral colour and its overall "
        "treatment. The product itself comes from the first image.",
        f"THE PACKAGE — {p.corpo}.",
        ESTUDIO,
        enquadramento(p.ocupacao),
        FIDELIDADE,
        p.arte.rstrip(".") + ".",
    ])


def p_frente_cor(p: Produto) -> str:
    return "\n\n".join([
        "EDIT THE ATTACHED PHOTOGRAPH. This is a background replacement and nothing "
        "else. Do not re-stage it, do not re-shoot it, do not re-draw it, do not "
        "re-frame it.",
        "KEEP THE PACKAGE PIXEL-FOR-PIXEL IDENTICAL: the same package, at the exact "
        "same position in the frame, the exact same scale, the exact same rotation and "
        "camera perspective, the exact same crop. The same creases and folds. The same "
        "printed artwork and the same typography, letter for letter. The package must "
        "occupy exactly the same pixels of the frame as it does in the source.",
        "CHANGE ONLY THE BACKGROUND. Replace the white cove with a seamless sweep in "
        f"exactly the same colour as {p.fundo} — sample that colour from the package "
        "itself. Wall and floor are the same colour and continuous, with no visible "
        "horizon line, no seam, no edge and no props. Keep the same key light "
        "direction and the same highlight pattern on the package, and let the new "
        "backdrop bounce a little of its own colour back onto the package, the way a "
        "coloured cove really would.",
        "Keep the soft contact shadow under the base, now reading as a slightly deeper "
        "tone of the backdrop colour rather than grey. No mirror reflection. Everything "
        "stays sharp. No added text, no watermark.",
    ])


def p_lateral_saco(p: Produto) -> str:
    return "\n\n".join([
        "STRICT ROTATION TASK. Do not reproduce either attached image's viewpoint. The "
        "output must show a DIFFERENT camera angle than both attachments: a full "
        "90-degree side profile, described below.",
        f"THE PACKAGE — {p.corpo}.",
        "First attached image: the studio front view — copy its lighting, white cove "
        "background, and colour treatment only. Second attached image: a raw photo at "
        "a slight angle — look at it ONLY to measure the true depth and fold geometry "
        "of the side gusset (how far it recesses, the crease pattern, the taper). Its "
        "viewpoint, its printed logo, its background and its lighting must NOT appear "
        "in your output.",
        "THE OUTPUT VIEWPOINT: rotate the package a full 90 degrees past what is shown "
        "in either image, so the camera looks squarely at the narrow SIDE face of the "
        "pouch — the inward-folded gusset filling almost the entire frame width, "
        "running as a vertical crease down the middle, completely UNPRINTED. No logo, "
        "no lettering, no artwork, no front panel visible at all except a razor-thin "
        "sliver at the very left edge. If any part of \"CANASTRA\" or the mountain logo "
        "is legible in your output, the rotation failed — redo it further. The camera "
        "stays level at the package's mid-height, square to the subject, same distance "
        "as the front shot.",
        ESTUDIO,
        enquadramento(p.ocupacao, "in strict side profile"),
        "Do not invent any printed text on the side panel — it is blank.",
    ])


def p_lateral_caixa(p: Produto, rotulo: str) -> str:
    return "\n\n".join([
        f"Create a studio photograph of the {rotulo.upper()} of the carton shown in the "
        "attached reference photo. The second attached image is the STYLE ANCHOR for "
        "lighting and background; the first image is the panel to reproduce.",
        f"THE PACKAGE — {p.corpo}.",
        "Turn the carton so that this side panel faces the camera square on, at eye "
        "level, vertical edges parallel. Show only a very thin sliver of the front "
        "face at one edge so the box still reads as a solid object.",
        ESTUDIO,
        enquadramento(p.ocupacao, "with the side panel square to the camera"),
        "CRITICAL — THIS PANEL IS ALL TEXT. Reproduce every printed character exactly "
        "as it appears in the attached photograph: same wording, same line breaks, same "
        "order, same accents, same numbers. Do not re-typeset it, do not translate it, "
        "do not paraphrase it, do not summarise it, do not invent a single word. If a "
        "line is hard to read in the reference, reproduce it as it is rather than "
        "guessing at a replacement. Do not generate a QR code or a barcode that is not "
        "in the reference, and do not redraw the ones that are — copy them.",
    ] + ([p.lateral_extra[rotulo]] if rotulo in p.lateral_extra else []))


# --------------------------------------------------------------------------- #
# familia capsula: as 3 tomadas da capsula de plastico de verdade
# --------------------------------------------------------------------------- #

#: Repetido nas tres: a tampa e lisa. O modelo adora carimbar um logo nela.
CAPSULA_NEGATIVOS = (
    "DO NOT print anything on the foil lid — no logo, no mountain, no \"CANASTRA\", "
    "no variant name, no numbers, no barcode, no embossing. The lid is blank silver "
    "foil. NOTHING ELSE SITS ON THE FLOOR of the set: no loose coffee beans, no "
    "ground coffee, no cup, saucer, spoon, leaf, cinnamon quill, cloth, wood, board "
    "or water drop as a real object in the scene — this does not touch the beans, "
    "leaves or quills that are PRINTED inside the carton's own artwork, which stay "
    "exactly as they are. Do not open, tear, peel or pierce any capsule — all of "
    "them are sealed and intact."
)


def p_pack_capsula(p: Produto) -> str:
    """Padrao 1 — a caixa com a capsula real ao lado."""
    return "\n\n".join([
        "Create a studio product photograph that puts the carton and its real "
        "capsules together in one frame.",
        "THE TWO ATTACHMENTS HAVE DIFFERENT JOBS, do not mix them. FIRST image — the "
        "approved studio packshot of the carton: it is the source of the CARTON and "
        "of nothing else. Reproduce that carton's printed artwork, its proportions, "
        "its colours, its lighting and its white cove exactly as they are there. "
        "SECOND image — two tight crops of the REAL capsule photographed on a "
        "wooden table, the same capsule twice: standing on the left, lying on its "
        "side on the right so the foil lid shows. Look at it ONLY to read the "
        "capsule's shape, its proportions, its colour, its finish and its silver "
        "foil lid. Its wooden table, its warm tungsten light, its two-up split "
        "layout and its white border must NOT appear in your output — the output "
        "is one single photograph on a white cove.",
        f"THE CARTON — {p.corpo}.",
        FIDELIDADE,
        p.arte.rstrip(".") + ".",
        f"THE CAPSULES — {CAPSULA_FORMA}. {p.capsula_corpo}.",
        "THE ARRANGEMENT — the carton stands upright, slightly left of centre, front "
        "face square to the camera, exactly as in the first image. On the white floor "
        "to its right, clear of the carton and never overlapping it, two capsules: "
        "one STANDING upright on its flange with the domed closed end pointing up and "
        "the foil lid hidden against the floor, set a little behind; and one LYING on "
        "its side in front of it, rolled so the SILVER FOIL LID faces the camera and "
        "reads as a full circle. The two capsules touch neither each other nor the "
        "carton. Each one casts its own small soft contact shadow on the floor, in "
        "the same direction as the carton's.",
        "SCALE — the capsule is small: a standing capsule reaches about one third of "
        "the carton's height. Do not enlarge it to fill the gap.",
        ESTUDIO,
        enquadramento(50),
        CAPSULA_NEGATIVOS,
    ])


def p_capsula_solo(p: Produto) -> str:
    """Padrao 2 — uma capsula sozinha."""
    return "\n\n".join([
        "Create a studio product photograph of ONE espresso capsule alone — no "
        "carton, no box, no packaging anywhere in the frame.",
        "FIRST attached image — two tight crops of the REAL capsule photographed "
        "on a wooden table, the same capsule twice: standing on the left, lying on "
        "its side on the right so the foil lid shows. It is the source of the "
        "capsule's shape, proportions, colour, finish and foil lid, and of nothing "
        "else. Its wooden table, its warm tungsten light, its two-up split layout "
        "and its white border must not appear. SECOND attached image — the STYLE ANCHOR: match its "
        "lighting, its white cove background, its neutral white balance and its "
        "overall treatment. Do not reproduce the carton shown in it.",
        f"THE SUBJECT — {CAPSULA_FORMA}. {p.capsula_corpo}.",
        "THE POSE — a single capsule STANDING upright on its flange, the domed closed "
        "end pointing up, the foil lid resting on the floor and hidden. Seen very "
        "slightly from above, so the flange reads as a narrow ellipse at the base and "
        "the dome reads as a dome. One capsule only.",
        ESTUDIO,
        capsula_enq(40, "A single capsule stands upright and centred."),
        CAPSULA_NEGATIVOS,
    ])


def p_capsula_trio(p: Produto) -> str:
    """Padrao 3 — tres capsulas soltas."""
    return "\n\n".join([
        "Create a studio product photograph of THREE espresso capsules together — no "
        "carton, no box, no packaging anywhere in the frame.",
        "FIRST attached image — two tight crops of the REAL capsule photographed "
        "on a wooden table, the same capsule twice: standing on the left, lying on "
        "its side on the right so the foil lid shows. It is the source of the "
        "capsule's shape, proportions, colour, finish and foil lid, and of nothing "
        "else. Its wooden table, its warm tungsten light, its two-up split layout "
        "and its white border must not appear. SECOND attached image — the STYLE ANCHOR: match its "
        "lighting, its white cove background, its neutral white balance and its "
        "overall treatment. Do not reproduce the carton shown in it.",
        f"THE SUBJECT — three identical capsules. Each one is {CAPSULA_FORMA}. "
        f"{p.capsula_corpo}.",
        "THE ARRANGEMENT — two capsules STANDING upright side by side at the back, "
        "each on its flange with the domed closed end pointing up and the foil lid "
        "hidden against the floor, a small gap between them so they do not touch. In "
        "front of them and slightly to one side, the third capsule LIES on its side, "
        "rolled so the SILVER FOIL LID faces the camera and reads as a full circle, "
        "its dome pointing away. The three form a shallow triangle on the floor. Each "
        "casts its own small soft contact shadow, all in the same direction. All "
        "three capsules are exactly the same colour and the same size.",
        ESTUDIO,
        capsula_enq(34, "The three capsules sit as a compact group, centred."),
        CAPSULA_NEGATIVOS,
    ])


def p_verso(p: Produto) -> str:
    return "\n\n".join([
        "Create a studio photograph of the BACK of the package shown in the attached "
        "reference photo. The second attached image is the STYLE ANCHOR for lighting "
        "and background; the first image is the panel to reproduce.",
        f"THE PACKAGE — {p.corpo}.",
        "Turn the package so the back panel faces the camera square on, at eye level, "
        "vertical edges parallel, flat and undistorted.",
        ESTUDIO,
        enquadramento(p.ocupacao, "with the back panel square to the camera"),
        "CRITICAL — THIS PANEL IS A LEGAL LABEL. Reproduce every printed character "
        "exactly as it appears in the attached photograph: the description paragraph, "
        "the roast and intensity meters, the altitude icon, the preparation bullets, "
        "the producer seal, the company name, address and registration numbers, the "
        "net weight, the batch and date stamps. Same wording, same line breaks, same "
        "accents, same digits. Do not re-typeset, do not translate, do not paraphrase, "
        "do not summarise, do not modernise, do not invent a single character. Do not "
        "generate a new QR code and do not generate a new barcode — copy the ones in "
        "the reference exactly as printed.",
    ])


# --------------------------------------------------------------------------- #
# escrita
# --------------------------------------------------------------------------- #

def _n_imagens(p: Produto) -> int:
    """2 frentes + laterais (min 1) + verso + as 3 tomadas de capsula, se houver."""
    return 2 + max(1, len(p.laterais)) + 1 + (3 if p.capsula_corpo else 0)


def _total_imagens() -> int:
    return sum(_n_imagens(p) for p in PRODUTOS)


CABECALHO = f"""\
# Prompts de estúdio — catálogo Café Canastra

Gerado por `scripts/prompts_catalogo.py`. Para mudar qualquer convenção, edite o
script e rode de novo — não edite este arquivo à mão, ele é sobrescrito.

{len(PRODUTOS)} produtos, **{_total_imagens()} imagens**. Para rodar no ChatGPT, colando um bloco por vez.

---

## Leia antes de começar

**A ordem importa, e ela economiza refação.** Para cada produto:

1. **Frente fundo branco** primeiro. Confira o texto. Só siga quando estiver certo.
2. **Frente fundo cor** usando *a imagem aprovada do passo 1* como anexo. É só troca
   de fundo, então a posição vem de graça e o rótulo já está correto — não há
   segunda chance de errar a letra.
3. **Lateral** e **verso**, cada um com seu anexo próprio.

**Como conferir.** Não olhe a imagem inteira: em miniatura, erro de letra passa
batido. Amplie a faixa de texto pequeno — `Desde 1985`, a linha do rodapé, o peso.
Foi exatamente aí que o Clássico saiu com `Doodo 1985` e `TRODULB E HÚMO` num teste
que não pedia mudança nenhuma no rótulo.

**O verso é o ponto fraco, e não é questão de prompt.** O modelo redesenha o
quadro inteiro em vez de copiar pixels, e o verso tem CNPJ, endereço, lote, QR de
rastreabilidade e código de barras em corpo minúsculo. Ele vai inventar. O prompt
do verso aqui é o melhor que dá para escrever, mas a rota confiável para essas 20
imagens é **composição da foto real** — recorte, endireitar a perspectiva, trocar o
fundo — sem redesenho. Se for gerar mesmo assim, trate o QR e o código de barras
como decoração: eles não vão funcionar no leitor.

**O lateral dos sacos também é rascunho, por um motivo diferente.** Mesmo
anexando uma foto real em ângulo como referência de geometria, o modelo insiste
num perfil pontudo tipo lâmina em vez da sanfona reta e larga de verdade — é viés
do modelo, testado e confirmado, não falta de referência. A foto em ângulo ajuda
em uma coisa: sem ela o modelo às vezes nem gira o pacote e vaza o logotipo numa
face que deveria ficar em branco. Mesma recomendação do verso — composição da
foto real é a rota confiável para publicação.

---

## Convenções fixadas

| | |
|---|---|
| **Formato** | Retrato 3:4, pedido direto no prompt (`3:4 aspect ratio`) — sem recorte depois. |
| **Fundo branco** | Ciclorama branco de estúdio, com sombra de contato. Não é `#FFFFFF` chapado — dá volume ao produto. |
| **Fundo colorido** | A cor sai **da própria embalagem**, amostrada da foto. O prompt não fixa hex nenhum. |
| **Luz** | Softbox à esquerda alta, rebatedor à direita, kicker no topo. Igual nas 85. |
| **Escala** | Proporcional ao tamanho real **dentro de cada família**: os sacos entre si, as caixas entre si. Um 1kg ocupa 88% da altura, um 500g 70%, um 250g 56%. Entre famílias não — uma caixa de cápsula em escala real contra um saco de 1kg ficaria minúscula na grade. |
| **Âncora de estilo** | `{ANCORA}` — anexe junto em toda frente nova, para as 85 parecerem a mesma sessão. |

---

## Índice

"""


def bloco(titulo: str, anexos: list[str], prompt: str, nota: str = "") -> str:
    linhas = [f"#### {titulo}", ""]
    linhas.append("**Anexar, nesta ordem:**")
    linhas.append("")
    for i, a in enumerate(anexos, start=1):
        linhas.append(f"{i}. `{a}`")
    linhas.append("")
    if nota:
        linhas.append(nota)
        linhas.append("")
    linhas.append("```text")
    linhas.append(prompt)
    linhas.append("```")
    linhas.append("")
    return "\n".join(linhas)


def montar() -> str:
    partes = [CABECALHO]
    for i, p in enumerate(PRODUTOS, start=1):
        partes.append(f"{i}. [{p.nome}](#{i}-{p.slug}) — {_n_imagens(p)} imagens\n")
    partes.append("\n---\n")

    for i, p in enumerate(PRODUTOS, start=1):
        rel = f"fotos produtos cru/{p.pasta}"
        partes.append(f"\n## {i}. {p.nome}\n")
        partes.append(f"<a id=\"{i}-{p.slug}\"></a>\n")
        partes.append(f"Fotos cruas em `{rel}/`.\n")

        partes.append(bloco(
            f"{i}.1 Frente — fundo branco",
            [f"{rel}/{p.frente}", ANCORA],
            p_frente_branco(p),
            "Confira o rodapé e o `Desde 1985` ampliados antes de seguir.",
        ))
        partes.append(bloco(
            f"{i}.2 Frente — fundo cor da embalagem",
            [f"a imagem aprovada em {i}.1"],
            p_frente_cor(p),
            "Só a aprovada do passo anterior. É o que garante que as duas fiquem na mesma posição.",
        ))

        if p.laterais:
            for j, (rotulo, fonte) in enumerate(p.laterais, start=3):
                partes.append(bloco(
                    f"{i}.{j} {rotulo.capitalize()}",
                    [f"{rel}/{fonte}", f"a imagem aprovada em {i}.1"],
                    p_lateral_caixa(p, rotulo),
                    "⚠️ Painel de texto corrido. Confira linha por linha, ampliado.",
                ))
            prox = 3 + len(p.laterais)
        else:
            partes.append(bloco(
                f"{i}.3 Lateral — perfil",
                [f"a imagem aprovada em {i}.1", f"{rel}/{p.lateral_ref}"],
                p_lateral_saco(p),
                "⚠️ Rascunho conhecido: mesmo com a foto real em ângulo como referência, "
                "o modelo insiste num formato pontudo tipo lâmina em vez da sanfona reta "
                "e larga de verdade — viés do modelo, não falta de referência (testado). "
                "A segunda imagem ao menos evita vazar o logotipo nessa lateral, que "
                "deveria ficar em branco. Rota confiável: composição da foto real "
                "(recorte/endireitar), sem redesenho.",
            ))
            prox = 4

        partes.append(bloco(
            f"{i}.{prox} Verso",
            [f"{rel}/{p.verso}", f"a imagem aprovada em {i}.1"],
            p_verso(p),
            "⚠️ Rótulo legal. Leia o aviso do topo antes de gastar geração aqui.",
        ))

        if p.capsula_corpo:
            nota_fonte = (" " + p.capsula_nota) if p.capsula_nota else ""
            partes.append(bloco(
                f"{i}.{prox + 1} Embalagem + cápsula ao lado",
                [f"a imagem aprovada em {i}.1", p.capsula_fonte],
                p_pack_capsula(p),
                "⚠️ A caixa muda de escala, então o rótulo é **redesenhado** — confira "
                "`Desde 1985`, `SCAA 80+` e o rodapé ampliados, como numa frente nova."
                + nota_fonte,
            ))
            partes.append(bloco(
                f"{i}.{prox + 2} Cápsula isolada",
                [p.capsula_fonte, f"a imagem aprovada em {i}.1"],
                p_capsula_solo(p),
                "Sem rótulo no quadro: o que se confere aqui é a **tampa lisa** (o modelo "
                "tende a carimbar um logo nela), a cor do corpo e a ausência de adereço."
                + nota_fonte,
            ))
            partes.append(bloco(
                f"{i}.{prox + 3} Três cápsulas isoladas",
                [p.capsula_fonte, f"a imagem aprovada em {i}.1"],
                p_capsula_trio(p),
                "Confira que as três têm a **mesma cor e o mesmo tamanho** e que a deitada "
                "mostra a tampa prata lisa." + nota_fonte,
            ))

        partes.append("---\n")

    return "\n".join(partes)


def conferir() -> int:
    faltando: list[str] = []
    for p in PRODUTOS:
        alvos = [p.frente, p.verso] + [f for _, f in p.laterais]
        if not p.laterais:
            alvos.append(p.lateral_ref)
        for a in alvos:
            if not (p.dir / a).exists():
                faltando.append(f"{p.pasta}/{a}")
        if p.capsula_fonte and not (RAIZ / p.capsula_fonte).exists():
            faltando.append(p.capsula_fonte)
    if not (RAIZ / ANCORA).exists():
        faltando.append(ANCORA)
    for f in faltando:
        print(f"AUSENTE: {f}", file=sys.stderr)
    total = _total_imagens()
    print(f"{len(PRODUTOS)} produtos, {total} imagens, {len(faltando)} fonte(s) ausente(s)")
    return 1 if faltando else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--conferir", action="store_true", help="só valida as fontes")
    args = ap.parse_args()
    if args.conferir:
        return conferir()
    codigo = conferir()
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(montar(), encoding="utf-8")
    print(f"escrito: {DESTINO.relative_to(RAIZ)}")
    return codigo


if __name__ == "__main__":
    raise SystemExit(main())
