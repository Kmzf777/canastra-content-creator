"""As cenas da home, uma a uma. Importado por `home_cenas.py`.

REGRA QUE VALE PARA TODAS: nenhum objeto e inventado. Cada um foi descrito pelo
que ele fisicamente e no Brasil — o copo americano tem faceta na base e vidro
esverdeado, a mesa de boteco e chapa de aco de 60x60 com o brilho morto, a
cadeira monobloco e branca amarelada. Objeto descrito vago sai generico, e
generico e o que denuncia imagem de estoque.

REGRA DE EMBALAGEM: onde o pacote aparece legivel, ele entra como PIXEL da foto
real, no campo de fontes. Nunca se descreve o rotulo — descrever faz o modelo
redesenhar (licao 1). E os packshots sao o pacote DEITADO, visto de cima: a cena
tem de aceitar essa geometria, ou o modelo reinventa o pacote para po-lo em pe.
"""

from __future__ import annotations

from pathlib import Path  # noqa: F401

from home_cenas import (  # noqa: F401
    LUZ_BH,
    LUZ_COMERCIO,
    LUZ_FAZENDA,
    LUZ_SP,
    PACK,
    Cena,
)

# --------------------------------------------------------------------------- #
# objetos, descritos pelo que sao
# --------------------------------------------------------------------------- #

#: O COPO AMERICANO, descrito pelo que ele e — nao pelo que parece.
#:
#: Nadir Figueiredo, 1947. O nome vem da maquina de sopro importada dos EUA, nao
#: do formato. 190 ml, 9,3 cm de altura, 6,7 cm de diametro, 105 g por unidade —
#: 105 g para 190 ml e a prova numerica da parede grossa.
#:
#: A FORMA E TRONCO DE CONE INVERTIDO: base ESTREITA, boca LARGA, parede reta que
#: abre de baixo para cima. E essa conicidade que o torna empilhavel, e e o
#: motivo de ele existir. NAO TEM FACETA, nao tem haste, nao tem asa, nao tem
#: gravacao. (A primeira versao deste briefing dizia "facetas verticais rasas" —
#: invencao minha, corrigida contra a ficha do fabricante.)
#:
#: O erro tipico do modelo e entregar um tumbler reto americano ou um copo de
#: whisky. Por isso a conicidade e a altura baixa estao explicitas.
COPO = (
    "a short thick-walled Brazilian soda-lime drinking glass, nine centimetres "
    "tall and six and a half across, a SMOOTH TRUNCATED-CONE body flaring from a "
    "NARROW BASE to a WIDE MOUTH, with a heavy solid glass bottom, a faint mould "
    "seam and a shallow central dimple underneath, a fire-rounded rim, clear "
    "glass with a faint green tint visible in the thickness of the edges, the "
    "surface hazed with dishwasher etching and water spots - no facets, no stem, "
    "no handle, no engraving, no printing of any kind"
)

#: Xicara de cafezinho de boteco: porcelana branca grossa, ~60 ml, parede
#: pesada, pires do mesmo material com uma marca de cafe seca na borda.
XICARA = (
    "a small thick white porcelain coffee cup of the kind used in Brazilian "
    "bars, about six centimetres across, heavy-walled, on a matching saucer with "
    "a dried coffee ring at its edge"
)

#: Moedor manual domestico: corpo de aco inox ou madeira, manivela dobravel de
#: aco, recipiente de vidro ou plastico transparente na base.
MOEDOR = (
    "a plain unbranded hand coffee grinder: a straight stainless steel body "
    "about eighteen centimetres tall with a folding steel crank on top and a "
    "clear container at the base"
)

#: Mesa de boteco: chapa de aco 60x60 com borda dobrada, base de tubo pintado,
#: riscada, com o brilho ja morto.
MESA_BOTECO = (
    "a sixty by sixty centimetre brushed steel bar table with a folded edge and "
    "a painted tube base, scratched all over, its shine long gone"
)

#: Cadeira monobloco: no Brasil ela e branca amarelada de sol ou vermelha, com
#: as pernas sujas e um arranhao no encosto.
CADEIRA = (
    "a one-piece moulded plastic chair, white gone yellow with sun or faded red, "
    "legs dirty at the feet, a scratch across the back rest, completely plain"
)

#: Azulejo 15x15 de padaria e boteco, vidrado, com rejunte cinza encardido.
AZULEJO = (
    "glazed white fifteen by fifteen centimetre wall tile up to about one metre "
    "sixty, the grout a grimy grey, several corners chipped, and above the tile "
    "line a wall painted flat institutional beige"
)

#: Fiacao aerea brasileira: feixe grosso amarrado, com sobra enrolada em bobina
#: pendurada no poste. O modelo tende a apagar isso — precisa ser pedido.
FIACAO = (
    "a thick bundle of black overhead cables crossing the frame diagonally, with "
    "a coil of slack cable hanging in a loop from a grey concrete pole"
)

#: Piso paulista: ladrilho hidraulico quadrado cinza-claro e off-white com um
#: motivo geometrico preto e branco repetido. NAO e calcada portuguesa — pedir
#: onda portuguesa entrega Rio ou Lisboa.
PISO_SP = (
    "grey and off-white square hydraulic concrete pavement tiles with a "
    "repeating black-and-white geometric motif, worn matte in the middle where "
    "people walk, grout dark with grime, a few tiles patched with plain cement"
)

#: Tijolinho de BH: a cor VARIA dentro da mesma parede, de ferrugem escura a
#: terracota clara, com eflorescencia esbranquicada nas fiadas baixas.
TIJOLINHO = (
    "an exposed red brick wall whose brick colour varies within the same wall "
    "from dark rust to pale terracotta, with pale mortar joints a centimetre "
    "wide and whitish efflorescence on the lower courses"
)

# OS PACKSHOTS ESTAO ROTACIONADOS NO ARQUIVO. Abertos como estao, o pacote
# aparece deitado e o modelo o reproduz de cabeca para baixo — foi o que a sonda
# devolveu. Girados -90 graus, sao o que sempre foram: o pacote EM PE contra a
# parede, sobre bancada de madeira, com a arte inteira legivel.
_EMPE = RAIZ_PACK = PACK.parent.parent.parent / "saida-teste" / "packshot-em-pe"
PACKSHOT_SUAVE = _EMPE / "suave-rot-90.jpg"
PACKSHOT_CLASSICO = _EMPE / "classico-rot-90.jpg"
PACKSHOT_CANELA = _EMPE / "canela-rot-90.jpg"


# --------------------------------------------------------------------------- #
# as cenas
# --------------------------------------------------------------------------- #

CENAS: tuple[Cena, ...] = (
    # ---------------------------------------------------------------- heroi --
    # A Nike poe no heroi uma pessoa em REPOUSO DENTRO DO PROPRIO LUGAR — no
    # heroi principal deles a atleta esta sentada num banco de vestiario. Aqui e
    # a Dulce parada no meio de uma passada. Nao e pose, e pausa.
    #
    # A zona escura para o texto tem de vir da FOTO, nao do CSS: a Nike nao tem
    # um unico scrim, e a zona de texto e mais escura que o resto do quadro em
    # 12 de 12 casos. Ao meio-dia a sombra e curta, entao o escuro sai do
    # interior escuro do cafeeiro no canto inferior esquerdo.
    Cena(
        slug="heroi",
        aspecto="16:9",
        avatar="dulce",
        luz=LUZ_FAZENDA,
        n_sugerido=6,
        corpo=(
            "A 52-year-old Black Brazilian woman standing in the alley between two "
            "rows of coffee bushes on a farm in Minas Gerais, at noon in the dry "
            "season. She has stopped in the middle of what she was doing, one hand "
            "resting on the top of a coffee bush, weight on one hip, and she looks "
            "STRAIGHT INTO THE LENS, eyes narrowed against the overhead sun, "
            "forehead creased, mouth closed - no smile, no scowl, no invitation. "
            "She wears a thin dark forest-green cotton t-shirt with a sweat patch, "
            "faded dark denim work trousers and dust-yellowed leather boots. She "
            "stands slightly RIGHT of centre.\n\n"
            "The LOWER LEFT QUARTER of the frame is filled by the dark shaded "
            "interior of the nearest coffee bush - deep open shade, the darkest "
            "part of the picture. "
            "Around her: bare red earth with tractor marks, a black plastic "
            "irrigation line lying along the ground, a rough wooden post with old "
            "wire, coffee leaves that are dusty and chewed by insects. Blue sky "
            "with hard-edged white cumulus behind. On the far horizon a "
            "FLAT-TOPPED TABLELAND with a long level crest - a mesa ridge, NOT "
            "alpine summits, NOT sharp triangular peaks."
        ),
        extra_neg="alpine summits, sharp triangular mountain peaks, headwrap, turban, salon afro, glossy hair, straw hat",
    ),
    # ------------------------------------------------------------ em graos --
    Cena(
        slug="fmt-graos",
        aspecto="4:5",
        avatar="barbara",
        luz=LUZ_BH,
        n_sugerido=4,
        corpo=(
            "A 37-year-old white Brazilian woman sitting on the floor of an old "
            "Belo Horizonte apartment at midday, barefoot on a parquet wood floor "
            "beside an iron-framed window. She is turning the crank of "
            f"{MOEDOR}, braced between her knees. Her face is three-quarters and "
            "CUT BY THE FRAME EDGE, eyes down on the grinder. She wears a fine "
            "off-white knit top pilled with wear and loose creased linen trousers "
            "in a straw colour.\n\n"
            "On the window ledge beside her, a scatter of dark roasted WHOLE "
            "COFFEE BEANS and a few that have bounced onto the parquet. Through "
            f"the window, three metres away, {TIJOLINHO}, and {FIACAO}. A "
            "hard-edged rectangle of midday sun falls across the ledge and the "
            "spilled beans."
        ),
        extra_neg="coffee package, printed bag, label, branded grinder",
    ),
    # -------------------------------------------------------------- moido --
    # O packshot e o pacote DEITADO, visto de cima. A cena aceita essa geometria:
    # ele fica deitado no balcao. Pedir o pacote em pe E identico pixel a pixel
    # sao duas coisas incompativeis, e o modelo resolve reinventando o pacote.
    Cena(
        slug="fmt-moido",
        aspecto="4:5",
        avatar="rosangela",
        luz=LUZ_COMERCIO,
        packshots=(PACKSHOT_SUAVE,),
        n_sugerido=6,
        corpo=(
            "A 44-year-old Brazilian woman leaning on both forearms on the steel "
            "counter of a neighbourhood bakery in Belo Horizonte, in the pause "
            "between two customers. Her face is three-quarters and CUT BY THE TOP "
            "EDGE of the frame, eyes down on the counter. She wears a yellowed "
            "off-white uniform polo with the collar open and a rust brown waist "
            "apron tied at the front with a crooked knot - a WORK apron, never a "
            "leather barista apron - and a tea towel over one shoulder.\n\n"
            "The coffee package from the source photograph STANDS UPRIGHT on "
            "the counter in front of her, facing the camera square-on exactly as "
            "in the source, filling at least a third of the frame height, and her "
            "hand rests on the counter beside it without covering any printed "
            f"area. Also on the counter: {XICARA}. Behind her, {AZULEJO}, "
            "a bread display case and a stack of plain green plastic bottle "
            "crates against the wall."
        ),
        extra_neg="leather barista apron, package lying flat, upside-down label, mirrored text, latte art",
    ),
    # ------------------------------------------------------------ capsula --
    Cena(
        slug="fmt-capsula",
        aspecto="4:5",
        avatar="yuri",
        luz=LUZ_COMERCIO,
        n_sugerido=4,
        corpo=(
            "A 29-year-old Brazilian man of Japanese descent standing at the "
            "formica counter in the pantry of an ordinary Sao Paulo office floor. "
            "He is pushing shut the drawer of a small plain unbranded domestic "
            "capsule coffee machine in scratched matte plastic, with a used "
            "capsule still in the head. His face is three-quarters and CUT BY THE "
            "RIGHT EDGE of the frame; he is looking at the machine, not at the "
            "camera. He wears thin round wire-frame glasses and a small-checked "
            "short-sleeve shirt in dark green and off-white.\n\n"
            f"On the counter beside the machine: {COPO}, half full of black "
            "coffee. Also a big plastic water cooler bottle, a stack of thick "
            "tumbler glasses, crumbs, a paper towel roll standing on its end. "
            "Through a doorway to the left, a hard rectangle of daylight on the "
            "floor."
        ),
        extra_neg="coffee package, printed capsule box, branded machine, espresso crema art",
    ),
    # --------------------------------------------------------------- drip --
    Cena(
        slug="fmt-drip",
        aspecto="4:5",
        avatar="thaina",
        luz=LUZ_SP,
        n_sugerido=4,
        corpo=(
            "A 26-year-old Brazilian woman standing at a scratched formica "
            "counter in the kitchen of a small Sao Paulo apartment on a grey "
            "morning, hip leaning against the counter edge, one foot crossed over "
            "the other, shoulders rolled forward. Her face is three-quarters and "
            "CUT BY THE TOP EDGE of the frame, eyes down on her own hands. She "
            "wears a grimy off-white ribbed vest with wide straps and grey sweat "
            "shorts.\n\n"
            "She is pouring hot water from a small plain aluminium kettle onto a "
            "single-serve paper drip coffee sachet hooked over the rim of "
            f"{COPO}. The sachet is PLAIN UNPRINTED KRAFT PAPER, turned so that "
            "no printed face is visible. Steam rises and drifts to one side. "
            "Behind her, old wall tile to mid height, a scratched aluminium "
            "awning window with the lower pane cranked thirty degrees outwards, "
            "and through it the neighbouring building three metres away, its wall "
            "raw grey render streaked vertically by rain."
        ),
        extra_neg="printed sachet, branded sachet, label on sachet, latte art",
    ),
    # ---------------------------------------------------------------- kit --
    # SEM PESSOA de proposito. Tres embalagens legiveis num quadro ja e o pior
    # caso de fidelidade de rotulo; somar mao e rosto multiplicaria o risco sem
    # ganhar nada — o assunto do ladrilho e o presente, nao quem o compra.
    Cena(
        slug="fmt-kit",
        aspecto="4:5",
        avatar=None,
        luz=LUZ_BH,
        packshots=(PACKSHOT_CLASSICO, PACKSHOT_SUAVE, PACKSHOT_CANELA),
        n_sugerido=6,
        corpo=(
            "The THREE coffee packages from the source photographs, STANDING "
            "UPRIGHT side by side on the rough concrete bench of a neighbourhood "
            "square in Belo Horizonte at midday, each facing the camera square-on "
            "exactly as in its source. They are simply stood there, not arranged: "
            "one leans slightly, the spacing between them is uneven.\n\n"
            "Beside them a house key on a plain ring and a folded paper bag. "
            "Around: the pitted concrete of the bench with a chipped corner, "
            f"worn hydraulic tile pavement below, and the HARD-EDGED midday "
            "shadow of a tree cut sharp across the bench and the ground. "
            f"{FIACAO} crosses the sky in the upper part of the frame."
        ),
        extra_neg="gift box, ribbon, wrapping paper, styled arrangement, package lying flat, upside-down label, mirrored text",
    ),
    # -------------------------------------------------------------- clube --
    Cena(
        slug="clube",
        aspecto="16:9",
        avatar="wesley",
        luz=LUZ_SP,
        n_sugerido=4,
        corpo=(
            "A 31-year-old Black Brazilian man stepping down off the entrance "
            "step of an ordinary apartment building in Belo Horizonte on an "
            "overcast afternoon, caught mid-stride. Under his left arm, a plain "
            "brown corrugated cardboard box, closed, carrying NO printing and NO "
            "label of any kind. A phone in his right hand, a strip of first-aid "
            "tape around his index finger. He wears a faded forest-green cotton "
            "t-shirt cut slightly large, grey cargo trousers with one side pocket "
            "bulging, and cheap running trainers with dirty soles.\n\n"
            "His mouth is STARTING a smile that never completes - one corner "
            "rising, the eye creasing - and he is looking out of frame to the "
            "side, NOT at the camera, LIPS CLOSED with no teeth visible. He "
            "stands LEFT of centre, leaving the right third of the frame open. "
            "Behind him: a painted metal gate, worn hydraulic tile, a flat "
            f"institutional beige wall with a scuffed skirting board, and "
            f"{FIACAO}."
        ),
        extra_neg="printed box, shipping label, brand logo on box, open mouth smile, visible teeth, motion blur",
    ),
)
