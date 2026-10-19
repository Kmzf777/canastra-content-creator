"""Peça 09 ("cada um tem seu jeitinho"): folhas NOVAS do ChatGPT → biblioteca → projeto.

O cliente pediu assets gerados para esta peça, sem reciclar a biblioteca (15/10/2026).
Seis folhas, todas geradas em 15/10/2026 no ChatGPT pelo Claude in Chrome; o prompt de
cada uma vai para o índice (`registrar(..., prompt=...)`), para a próxima sessão conseguir
refazer uma folha parecida.

    python -m uv run python scripts/colagem_assets_09.py listar    # confere contagem/ordem
    python -m uv run python scripts/colagem_assets_09.py           # recorta, registra, publica
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import biblioteca_colagem as B  # noqa: E402
from colagem_assets import convexo, peca  # noqa: E402

DOWN = Path.home() / "Downloads"
TMP = Path("saida-teste/motion-09/pecas")
DIA = "2026-10-15"
PROJ = "09-jeitinho-cafe"
G = "gerado-chatgpt"

_PREFIXO = ("Generate an image. A collage asset sheet: six separate photographic objects laid out in a loose 3x2 "
            "grid with generous empty space between them, on a perfectly flat, pure white (#FFFFFF) background. "
            "No shadows, no text, no logos, no packaging, no people, no hands. ")
_SUFIXO = (" Realistic natural daylight, everything in sharp focus, like a clean phone photo of real objects, "
           "slightly muted colors. Every object fully visible inside the frame and not touching any other object. "
           "Square image.")
PROMPTS = {
    "folha1-tangerina": _PREFIXO + "Objects: (1) a whole mandarin orange with one small green leaf; (2) a peeled "
    "mandarin with its segments slightly opened; (3) one single mandarin segment; (4) a small loose heap of finely "
    "grated fresh mandarin zest; (5) a flat stainless steel hand grater, seen at a slight angle; (6) a white ceramic "
    "cone pour-over coffee dripper with a paper filter inside." + _SUFIXO,
    "folha2-pacoquita": _PREFIXO.replace("no packaging,", "no labels, no packaging, no wrappers,") + "Objects: (1) "
    "three unwrapped Brazilian pacoquita peanut candies - small pressed cylinder-shaped peanut sweets, light tan "
    "color, dry crumbly texture; (2) a small loose heap of crumbled pacoquita peanut crumbs; (3) a short clear "
    "drinking glass half full of thick creamy beige peanut paste with swirls of dark coffee on top; (4) a plain "
    "stainless steel teaspoon; (5) a small heap of white powdered milk; (6) a small clear glass jug of hot black "
    "coffee." + _SUFIXO,
    "folha3-preparo": _PREFIXO.replace("no packaging,", "no brand marks,") + "Objects: (1) a matte black gooseneck "
    "pour-over kettle; (2) a single folded white paper coffee filter, cone shaped; (3) six roasted coffee beans "
    "scattered loosely, not touching each other; (4) a simple light wooden coffee stirring stick; (5) a small round "
    "white analog kitchen timer with a dial; (6) a small white ceramic cup of black coffee seen from a high angle."
    + _SUFIXO,
    "folha4-grafismos": "Generate an image. A collage asset sheet of hand-made paper craft graphics, laid out in a "
    "loose grid with generous empty space between them, on a perfectly flat, pure white (#FFFFFF) background. No "
    "shadows, no letters, no numbers, no words. Items: (1) a thick hand-drawn red-orange marker arrow, curved; (2) a "
    "thick hand-drawn green marker arrow, straight with a slight wobble; (3) a hand-drawn red-orange marker circle "
    "scribble, loose and open; (4) a hand-drawn red-orange marker X; (5) a yellow hand-cut paper starburst shape; (6) "
    "four short torn pieces of beige masking tape at different angles; (7) a long torn strip of off-white paper with "
    "rough fibrous torn edges; (8) an empty instant-photo frame made of off-white card, the inside window filled with "
    "flat solid magenta (#FF00FF). Flat even daylight, crisp edges, realistic paper and marker textures. Every item "
    "fully visible and not touching any other item. Square image.",
    "folha5-papel-grade": "Generate an image. A flat, straight-on top-down photo of a single sheet of off-white cream "
    "paper filling the entire frame edge to edge, printed with a faint thin pale green square grid (graph paper, "
    "about 20 squares across the width), subtle paper fibers and a very gentle uneven tint, evenly lit with soft "
    "daylight. No objects, no shadows of objects, no folds, no text, no numbers, no margins, no borders. Tall "
    "vertical image, 2:3.",
    "folha7-giuseppe": "Generate an image. A collage asset sheet: five separate photographic objects laid out in a loose 3x2 "
    "grid with generous empty space between them, on a perfectly flat, pure white (#FFFFFF) background. No shadows, no text, "
    "no logos, no labels, no brand marks, no people, no hands. Objects: (1) a wooden honey dipper with golden honey dripping "
    "from it; (2) a small clear glass jar of golden honey without any label; (3) a clear glass cup filled with milk and topped "
    "with a tall swirl of whipped light-brown coffee cream dusted with cocoa powder; (4) a red electric hand mixer with two "
    "metal beaters, no brand marks; (5) a gold teaspoon holding a stretchy dollop of light-brown whipped coffee cream." + _SUFIXO,
    "folha6-pedacos": "Generate an image. A collage asset sheet of paper cut-outs laid out with generous empty space "
    "between them, on a perfectly flat, uniform medium grey (#808080) background. No shadows, no text, no letters, "
    "no logos. Items: (1) a torn rectangular piece of glossy photo paper printing a bright blue sky with white fluffy "
    "cumulus clouds, with rough torn white paper edges; (2) a second, smaller torn piece of the same blue sky with "
    "clouds photo; (3) a black construction-paper cut-out silhouette of a generic human head and shoulders seen from "
    "the front, completely plain black with no facial features; (4) a torn scrap of brown kraft paper with fibrous "
    "edges; (5) a torn scrap of pale yellow paper. Flat even light, crisp edges, realistic paper textures. Every item "
    "fully visible and not touching any other item. Square image.",
}


def arq(folha: str) -> Path:
    return DOWN / f"jeitinho09-{folha}.png"


def mascara(rgb: np.ndarray, fundo: tuple[int, int, int], limiar: int) -> np.ndarray:
    """Objeto = tudo que se afasta da cor de fundo (branco nas folhas 1-4, cinza na 6)."""
    dist = np.abs(rgb.astype(np.int32) - np.array(fundo)[None, None, :]).sum(axis=2)
    m = (dist > limiar * 3).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    cont, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cheia = np.zeros_like(m)
    cv2.drawContours(cheia, cont, -1, 1, thickness=cv2.FILLED)
    return cheia


# regiões (fração da folha) cujos componentes viram UM objeto: os seis grãos soltos da
# folha 3 ficam longe demais entre si para um raio de junção que não grude a chaleira no filtro
GRUPOS = {"folha3-preparo": [(0.68, 0.05, 1.0, 0.5)]}


def componentes(folha: str, fundo=(255, 255, 255), limiar=22, juntar=24, area_min=2500):
    rgb = np.array(Image.open(arq(folha)).convert("RGB"))
    m = mascara(rgb, fundo, limiar)
    grosso = cv2.dilate(m, np.ones((juntar, juntar), np.uint8))
    n, rot, st, cent = cv2.connectedComponentsWithStats(grosso)
    h, w = m.shape
    for x0, y0, x1, y1 in GRUPOS.get(folha, []):
        juntos = [i for i in range(1, n) if x0 <= cent[i][0] / w <= x1 and y0 <= cent[i][1] / h <= y1]
        for i in juntos[1:]:
            rot[rot == i] = juntos[0]
        if juntos:
            ys, xs = np.where(rot == juntos[0])
            st[juntos[0]] = [xs.min(), ys.min(), xs.max() - xs.min() + 1, ys.max() - ys.min() + 1, len(xs)]
            cent[juntos[0]] = [xs.mean(), ys.mean()]
            for i in juntos[1:]:
                st[i, cv2.CC_STAT_AREA] = 0
    comps = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= area_min]
    return rgb, m, rot, st, cent, comps


# folha → (nomes em ordem de leitura, fundo, limiar, juntar, convexos, filete)
FOLHAS = {
    "folha1-tangerina": (["tangerina", "tangerina-aberta", "gomo", "raspas", "ralador", "coador-v60"],
                         (255, 255, 255), 22, 24, ("coador-v60",), 9),
    "folha2-pacoquita": (["pacoquitas", "pacoquita-farelo", "copo-pasta", "colher", "leite-em-po", "jarra-cafe"],
                         (255, 255, 255), 14, 30, ("copo-pasta", "jarra-cafe", "leite-em-po"), 9),
    "folha3-preparo": (["chaleira", "filtro-papel", "graos-soltos", "mexedor", "timer", "xicara-cima"],
                       (255, 255, 255), 14, 40, ("filtro-papel", "timer", "xicara-cima"), 9),
    "folha7-giuseppe": (["mel-pegador", "pote-mel", "copo-creme", "batedeira", "colher-creme"],
                        (255, 255, 255), 22, 30, ("pote-mel", "copo-creme"), 9),
    "folha6-pedacos": (["ceu-rasgado", "ceu-rasgado-pequeno", "silhueta", "kraft-rasgado", "papel-amarelo"],
                       (128, 128, 128), 18, 20, (), 0),
}
# a folha 4 tem quatro fitas espalhadas: a ordem por linha não é estável, então os nomes
# saem da posição (centro x, y em fração da folha), conferida no `listar`
GRAFISMOS = [("seta-curva", 0.22, 0.12), ("seta-verde", 0.50, 0.17), ("circulo", 0.84, 0.15), ("x-marcador", 0.18, 0.47),
             ("estrela", 0.48, 0.47), ("fita-1", 0.75, 0.32), ("fita-2", 0.75, 0.45), ("fita-3", 0.93, 0.45),
             ("fita-4", 0.75, 0.57), ("papel-rasgado", 0.33, 0.79), ("moldura", 0.85, 0.80)]


def ordem_leitura(st, cent, comps):
    alt = np.median([st[i, cv2.CC_STAT_HEIGHT] for i in comps])
    return sorted(comps, key=lambda i: (round(cent[i][1] / (alt * 0.9)), cent[i][0]))


def listar() -> None:
    for folha, (nomes, fundo, lim, jun, _, _) in FOLHAS.items():
        rgb, m, rot, st, cent, comps = componentes(folha, fundo, lim, jun)
        h, w = m.shape
        print(f"\n{folha}: {len(comps)} objetos (esperado {len(nomes)})")
        for i in ordem_leitura(st, cent, comps):
            print(f"   centro ({cent[i][0] / w:.2f}, {cent[i][1] / h:.2f})  caixa {st[i, 2]}x{st[i, 3]}")
    rgb, m, rot, st, cent, comps = componentes("folha4-grafismos", juntar=10, area_min=1500)
    h, w = m.shape
    print(f"\nfolha4-grafismos: {len(comps)} objetos (esperado {len(GRAFISMOS)})")
    for i in ordem_leitura(st, cent, comps):
        print(f"   centro ({cent[i][0] / w:.2f}, {cent[i][1] / h:.2f})  caixa {st[i, 2]}x{st[i, 3]}")


def recortar(rgb, m, rot, i, st) -> tuple[np.ndarray, np.ndarray]:
    x, y, w, h = st[i, :4]
    p = 8
    x0, y0 = max(x - p, 0), max(y - p, 0)
    x1, y1 = min(x + w + p, rgb.shape[1]), min(y + h + p, rgb.shape[0])
    alfa = ((rot[y0:y1, x0:x1] == i) & (m[y0:y1, x0:x1] > 0)).astype(np.float32)
    return rgb[y0:y1, x0:x1].copy(), cv2.GaussianBlur(alfa, (3, 3), 0.8)


def janela_magenta(rgb: np.ndarray, alfa: np.ndarray) -> np.ndarray:
    """A janela da moldura nasceu magenta para ser furada: vira transparente."""
    r, g, b = (rgb[..., k].astype(np.int32) for k in range(3))
    mag = (r > 180) & (b > 180) & (g < 90)
    mag = cv2.dilate(mag.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    alfa = alfa.copy()
    alfa[mag] = 0
    return alfa


def papel_grade() -> list[Path]:
    """Fundo 1080x1920 e mural 1620x2880 (espelhado: a grade é simétrica) para a câmera."""
    TMP.mkdir(parents=True, exist_ok=True)
    im = Image.open(arq("folha5-papel-grade")).convert("RGB")
    base = im.resize((1080, int(1080 * im.height / im.width)), Image.LANCZOS)
    a = np.array(base)
    alto = np.concatenate([a, a[::-1]], 0)[:1920]
    Image.fromarray(alto).save(TMP / "papel-grade.png", optimize=True)
    mural = np.concatenate([np.concatenate([a, a[:, ::-1]], 1), np.concatenate([a[::-1], a[::-1, ::-1]], 1)], 0)
    Image.fromarray(mural).resize((1620, 2880), Image.LANCZOS).save(TMP / "papel-grade-mural.png", optimize=True)
    return [TMP / "papel-grade.png", TMP / "papel-grade-mural.png"]


TAGS = {
    "tangerina": ["tangerina", "mexerica", "fruta", "folha"], "tangerina-aberta": ["tangerina", "descascada", "gomos"],
    "gomo": ["tangerina", "gomo"], "raspas": ["tangerina", "raspas", "ralada", "zest"],
    "ralador": ["ralador", "inox"], "coador-v60": ["coador", "v60", "cerâmica", "filtro de papel"],
    "pacoquitas": ["paçoquita", "amendoim", "doce"], "pacoquita-farelo": ["paçoquita", "farelo", "esfarelada"],
    "copo-pasta": ["copo", "pasta de paçoquita", "café"], "colher": ["colher", "inox"],
    "leite-em-po": ["leite em pó", "pó branco"], "jarra-cafe": ["jarra", "café preto", "vidro"],
    "chaleira": ["chaleira", "bico de ganso", "preta"], "filtro-papel": ["filtro de papel", "coador"],
    "graos-soltos": ["grão torrado", "seis grãos"], "mexedor": ["mexedor", "madeira"],
    "timer": ["timer", "cronômetro", "dois minutos"], "xicara-cima": ["xícara", "café preto", "de cima"],
    "ceu-rasgado": ["céu", "nuvens", "papel rasgado", "foto"], "ceu-rasgado-pequeno": ["céu", "nuvens", "papel rasgado"],
    "silhueta": ["silhueta", "cabeça", "papel preto", "você"], "kraft-rasgado": ["kraft", "papel rasgado"],
    "papel-amarelo": ["papel amarelo", "rasgado"],
    "mel-pegador": ["mel", "pegador de mel", "escorrendo"], "pote-mel": ["mel", "pote", "vidro"],
    "copo-creme": ["creme de café", "crema caffè", "copo"], "batedeira": ["batedeira", "vermelha"],
    "colher-creme": ["colher", "creme de café", "dourada"],
}
CATEG = {"tangerina": "objeto", "tangerina-aberta": "objeto", "gomo": "objeto", "raspas": "objeto",
         "ralador": "xicara-utensilio", "coador-v60": "xicara-utensilio", "pacoquitas": "objeto",
         "pacoquita-farelo": "objeto", "copo-pasta": "xicara-utensilio", "colher": "xicara-utensilio",
         "leite-em-po": "objeto", "jarra-cafe": "xicara-utensilio", "chaleira": "xicara-utensilio",
         "filtro-papel": "xicara-utensilio", "graos-soltos": "grao", "mexedor": "xicara-utensilio",
         "timer": "objeto", "xicara-cima": "xicara-utensilio", "ceu-rasgado": "textura",
         "ceu-rasgado-pequeno": "textura", "silhueta": "grafismo", "kraft-rasgado": "textura",
         "papel-amarelo": "textura", "mel-pegador": "objeto", "pote-mel": "objeto", "copo-creme": "xicara-utensilio",
         "batedeira": "xicara-utensilio", "colher-creme": "xicara-utensilio"}


def main() -> None:
    reg = []  # (nome, categoria, variantes, tags, bruto, prompt, nota)
    for folha, (nomes, fundo, lim, jun, conv, filete) in FOLHAS.items():
        rgb, m, rot, st, cent, comps = componentes(folha, fundo, lim, jun)
        if len(comps) != len(nomes):
            raise SystemExit(f"{folha}: {len(comps)} objetos, esperava {len(nomes)} — rode `listar`")
        bruto = B.RAIZ / "brutos" / f"{DIA}_jeitinho09-{folha}.png"
        bruto.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(arq(folha), bruto)
        for nome, i in zip(nomes, ordem_leitura(st, cent, comps)):
            pix, a = recortar(rgb, m, rot, i, st)
            if nome in conv:
                a = convexo(a)
            peca(pix, a, nome, filete=filete, com_reticula=False, destino=TMP)
            reg.append((nome, CATEG[nome], [TMP / f"{nome}-b{k}.png" for k in range(3)], TAGS[nome] + ["jeitinho"],
                        bruto.as_posix(), PROMPTS[folha], ""))
    # grafismos: nome pela posição
    rgb, m, rot, st, cent, comps = componentes("folha4-grafismos", juntar=10, area_min=1500)
    h, w = m.shape
    if len(comps) != len(GRAFISMOS):
        raise SystemExit(f"folha4-grafismos: {len(comps)} objetos, esperava {len(GRAFISMOS)} — rode `listar`")
    bruto = B.RAIZ / "brutos" / f"{DIA}_jeitinho09-folha4-grafismos.png"
    shutil.copy2(arq("folha4-grafismos"), bruto)
    usados = set()
    for nome, fx, fy in GRAFISMOS:
        i = min((c for c in comps if c not in usados), key=lambda c: (cent[c][0] / w - fx) ** 2 + (cent[c][1] / h - fy) ** 2)
        usados.add(i)
        pix, a = recortar(rgb, m, rot, i, st)
        if nome == "moldura":
            a = janela_magenta(pix, convexo(a))
        peca(pix, a, nome, filete=0, com_reticula=False, destino=TMP)
        cat = "fita" if nome.startswith("fita") else "textura" if nome == "papel-rasgado" else "grafismo"
        reg.append((nome, cat, [TMP / f"{nome}-b{k}.png" for k in range(3)], [nome.replace("-", " "), "jeitinho"],
                    bruto.as_posix(), PROMPTS["folha4-grafismos"], "moldura: janela magenta furada" if nome == "moldura" else ""))
    bruto = B.RAIZ / "brutos" / f"{DIA}_jeitinho09-folha5-papel-grade.png"
    shutil.copy2(arq("folha5-papel-grade"), bruto)
    for p in papel_grade():
        reg.append((p.stem, "textura", [p], ["papel quadriculado", "grade verde", "fundo", "jeitinho"],
                    bruto.as_posix(), PROMPTS["folha5-papel-grade"], "mural espelhado" if "mural" in p.stem else ""))

    ids = []
    for nome, cat, var, tags, bruto, prompt, nota in reg:
        # nomes próprios desta peça; rodar de novo refaz as MESMAS, então substitui
        e = B.registrar(f"j09-{nome}", cat, var, tags, G, bruto=bruto, prompt=prompt, dia=DIA, nota=nota, substituir=True)
        ids.append(e["id"])
    B.publicar(PROJ, ids)
    print(len(ids), "peças novas registradas e publicadas em", PROJ)


if __name__ == "__main__":
    listar() if sys.argv[1:] == ["listar"] else main()
