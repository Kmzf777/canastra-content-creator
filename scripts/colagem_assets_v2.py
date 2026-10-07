"""Peça 07 (café especial em colagem): folhas do ChatGPT → biblioteca → projeto.

Cada folha gerada sobre branco liso vira peças com filete de papel e 3 bordas (boil),
SEM retícula: na peça 07 os defeitos precisam ser reconhecíveis (é conteúdo didático),
então a foto fica fotográfica e o "papel" vem do filete. Tudo entra primeiro na
biblioteca (`instagram/assets/colagem`) e só então é publicado no projeto.

    python -m uv run python scripts/colagem_assets_v2.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).parent))
import biblioteca_colagem as B  # noqa: E402
from colagem_assets import convexo, foto_rasgada, peca, rng, ruido_suave, separar  # noqa: E402

BR = Path("saida-teste/motion-07/brutos")
TMP = Path("saida-teste/motion-07/pecas")
DIA = "2026-10-07"
PROJ = "07-cafe-especial-colagem"
G = "gerado-chatgpt"
BASE = Path("base-curada/01-real-verificada/fazenda-medeiros-1250m")


def guardar_bruto(arq: str, nome: str) -> str:
    destino = B.RAIZ / "brutos" / f"{DIA}_{nome}.png"
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BR / arq, destino)
    return destino.as_posix()


def lente_transparente(rgb: np.ndarray, alfa: np.ndarray) -> np.ndarray:
    """A lente da lupa nasce branca (fundo visto pelo vidro). No vídeo ela passa por
    cima do rótulo, então o miolo claro vira quase transparente."""
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    claro = (hsv[..., 2] > 228) & (hsv[..., 1] < 22)
    n, rot, st, _ = cv2.connectedComponentsWithStats(claro.astype(np.uint8))
    h, w = claro.shape
    # o fundo branco em volta do recorte também é "claro" e é o maior componente:
    # a lente é o maior claro que NÃO encosta na borda
    internos = [i for i in range(1, n)
                if st[i, cv2.CC_STAT_LEFT] > 0 and st[i, cv2.CC_STAT_TOP] > 0
                and st[i, cv2.CC_STAT_LEFT] + st[i, cv2.CC_STAT_WIDTH] < w
                and st[i, cv2.CC_STAT_TOP] + st[i, cv2.CC_STAT_HEIGHT] < h]
    if internos:
        maior = max(internos, key=lambda i: st[i, cv2.CC_STAT_AREA])
        miolo = cv2.erode((rot == maior).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
        alfa = alfa.copy()
        alfa[miolo] = 0.10
    return alfa


def processar(folha: str, nomes: list[str], filete: int, juntar: int = 24, limiar: int = 22,
              convexos: tuple[str, ...] = (), especial=None) -> dict[str, list[Path]]:
    pecas = separar(BR / folha, nomes, juntar_px=juntar, limiar=limiar)
    saida = {}
    for nome, (rgb, a) in pecas.items():
        if nome in convexos:
            a = convexo(a)
        if especial and nome in especial:
            a = especial[nome](rgb, a)
        peca(rgb, a, nome, filete=filete, com_reticula=False, destino=TMP)
        saida[nome] = [TMP / f"{nome}-b{i}.png" for i in range(3)]
    return saida


def texturas() -> dict[str, list[Path]]:
    TMP.mkdir(parents=True, exist_ok=True)
    out: dict[str, list[Path]] = {}
    # cortiça: base 1080x1920 e um mural 1,5x maior (espelhado) para a câmera viajar
    c = Image.open(BR / "m07-cortica.png").convert("RGB").resize((1080, 1920), Image.LANCZOS)
    c.save(TMP / "cortica.png")
    a = np.array(c)
    mural = np.concatenate([np.concatenate([a, a[:, ::-1]], 1), np.concatenate([a[::-1], a[::-1, ::-1]], 1)], 0)
    Image.fromarray(mural).resize((1620, 2880), Image.LANCZOS).save(TMP / "cortica-mural.png")
    out["cortica"] = [TMP / "cortica.png"]
    out["cortica-mural"] = [TMP / "cortica-mural.png"]
    # sombra de folhas (gobo) a partir da foto REAL da folhagem: folha iluminada = sombra
    f = ImageOps.exif_transpose(Image.open(BASE / "folhagem/IMG_1423.JPG")).convert("L").resize((810, 1080), Image.LANCZOS)
    v = np.array(f).astype(np.float32)
    v = cv2.GaussianBlur(v, (0, 0), 2.2)
    limiar = np.percentile(v, 58)
    m = np.clip((v - limiar) / 30, 0, 1)
    m = cv2.GaussianBlur(m, (0, 0), 4)
    big = cv2.resize(m, (1620, 2160), interpolation=cv2.INTER_CUBIC)
    rgba = np.zeros((2160, 1620, 4), np.uint8)
    rgba[..., :3] = (20, 14, 10)
    rgba[..., 3] = (big * 235).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(TMP / "sombra-folhas.png", optimize=True)
    out["sombra-folhas"] = [TMP / "sombra-folhas.png"]
    # grão de filme: 4 variantes de ruído médio-cinza, trocadas a cada 2 quadros
    gr = []
    for k in range(4):
        r = rng(f"grao-filme#{k}")
        n = r.normal(128, 34, (960, 540)).clip(0, 255).astype(np.uint8)
        n = cv2.GaussianBlur(n, (0, 0), 0.9)  # proibicoes.md: grão com campo borrado σ≈0,9
        p = TMP / f"grao-filme-{k}.png"
        Image.fromarray(n, "L").save(p, optimize=True)
        gr.append(p)
    out["grao-filme"] = gr
    return out


def main() -> None:
    reg = []  # (nome, categoria, variantes, tags, origem, bruto, nota)
    b = guardar_bruto("m07-defeitos-a.png", "defeitos-graves-a")
    for n, var in processar("m07-defeitos-a.png",
                            ["grao-preto", "grao-preto-partido", "grao-ardido", "grao-imaturo", "cereja-seca", "grao-fungo"],
                            filete=8, juntar=40).items():
        tags = {"grao-preto": "defeito grave preto", "grao-preto-partido": "defeito grave preto quebrado",
                "grao-ardido": "defeito grave ardido azedo", "grao-imaturo": "defeito verde imaturo",
                "cereja-seca": "defeito grave cereja seca coco", "grao-fungo": "defeito grave fungo mofo"}[n]
        reg.append((n, "grao", var, tags.split() + ["cru", "classificacao"], G, b, ""))
    b = guardar_bruto("m07-defeitos-b.png", "defeitos-graves-b")
    for n, var in processar("m07-defeitos-b.png",
                            ["grao-brocado", "grao-quebrado", "grao-concha", "grao-quaker", "pedra", "graveto", "casca"],
                            filete=8, juntar=24).items():
        tags = {"grao-brocado": "defeito broca furos inseto", "grao-quebrado": "defeito leve quebrado",
                "grao-concha": "defeito leve concha", "grao-quaker": "defeito quaker torrado claro",
                "pedra": "materia estranha pedra impureza", "graveto": "materia estranha pau graveto impureza",
                "casca": "impureza casca pergaminho"}[n]
        reg.append((n, "grao", var, tags.split() + ["classificacao"], G, b, ""))
    b = guardar_bruto("m07-bandeja.png", "bandeja-classificacao")
    for n, var in processar("m07-bandeja.png", ["bandeja"], filete=10, juntar=30).items():
        reg.append((n, "xicara-utensilio", var, ["bandeja preta", "classificacao", "grao verde", "vista de cima"], G, b, ""))
    b = guardar_bruto("m07-ferramentas.png", "ferramentas-classificador")
    for n, var in processar("m07-ferramentas.png", ["lupa", "pinca", "peneira-classificacao"], filete=9, juntar=30,
                            especial={"lupa": lente_transparente}).items():
        reg.append((n, "xicara-utensilio", var, {"lupa": ["lupa", "lente transparente"], "pinca": ["pinça", "inox"],
                    "peneira-classificacao": ["peneira", "classificacao", "metal"]}[n] + ["classificador"], G, b, ""))
    b = guardar_bruto("m07-prova.png", "mesa-de-prova")
    for n, var in processar("m07-prova.png", ["xicara-prova", "tigela-crosta", "mao-colher"], filete=9, juntar=30,
                            convexos=("xicara-prova", "tigela-crosta")).items():
        reg.append((n, "xicara-utensilio", var, {"xicara-prova": ["xicara de prova", "cupping", "vista de cima"],
                    "tigela-crosta": ["crosta", "cupping", "vidro"], "mao-colher": ["mão", "colher de prova", "cupping"]}[n], G, b, ""))
    b = guardar_bruto("m07-origem.png", "origem-defeitos")
    for n, var in processar("m07-origem.png", ["frutos-no-chao", "galho-passado"], filete=9, juntar=40).items():
        reg.append((n, "fruto", var, ({"frutos-no-chao": ["terra vermelha", "fruto passado", "caido", "fermentou"],
                    "galho-passado": ["galho", "cereja passada", "seca no pé"]})[n], G, b, ""))
    b = guardar_bruto("m07-folhas.png", "folhas-cafe")
    for n, var in processar("m07-folhas.png", [f"folha-{i}" for i in range(1, 7)], filete=0, juntar=20).items():
        reg.append((n, "planta", var, ["folha de café", "primeiro plano", "arabica"], G, b, "filete 0: vai desfocada na frente da lente"))
    b = guardar_bruto("m07-tachinhas.png", "papelaria")
    for n, var in processar("m07-tachinhas.png",
                            ["tachinha-creme", "tachinha-preta", "tachinha-terra", "tachinha-verde", "clipe-1", "clipe-2", "post-it", "etiqueta-barbante"],
                            filete=6, juntar=20, convexos=("etiqueta-barbante", "post-it")).items():
        reg.append((n, "papelaria", var, [n.split("-")[0], "mural"], G, b, ""))
    # fotos reais novas do mural
    for nome, arq, larg, rec, tags in [
        ("foto-maos-cafeeiro", "cafeeiro-com-mao/IMG_1422.JPG", 560, None, ["cafeeiro", "mão", "colhe", "medeiros"]),
        ("foto-fileiras", "cafezal/IMG_1407.JPG", 900, None, ["lavoura", "fileiras", "céu", "medeiros"]),
    ]:
        foto_rasgada(BASE / arq, nome, larg, recorte=rec, destino=TMP)
        reg.append((nome, "foto-real", [TMP / f"{nome}-b{i}.png" for i in range(3)], tags, "real-verificada",
                    (BASE / arq).as_posix(), "foto real impressa com borda rasgada"))
    for n, var in texturas().items():
        reg.append((n, "textura", var, {"cortica": ["cortiça", "mural", "1080x1920"], "cortica-mural": ["cortiça", "mural", "1620x2880", "travelling"],
                    "sombra-folhas": ["gobo", "sombra", "folhagem real", "sol a pino"], "grao-filme": ["grão de filme", "overlay", "4 variantes"]}[n],
                    "codigo" if n.startswith(("sombra", "grao")) else G,
                    (BASE / "folhagem/IMG_1423.JPG").as_posix() if n == "sombra-folhas" else None, ""))

    if "papelaria" not in B.CATEGORIAS:
        B.CATEGORIAS["papelaria"] = "tachinha, clipe, post-it, etiqueta"
    ids = []
    for nome, cat, var, tags, origem, bruto, nota in reg:
        e = B.registrar(nome, cat, var, tags, origem, bruto=bruto, dia=DIA, nota=nota)
        ids.append(e["id"])
    B.publicar(PROJ, ids)
    # peças da v1 que a 07 reaproveita
    B.publicar(PROJ, [f"{DIA}_{n}" for n in ["xicara", "torrado", "cereja-verde-1", "cereja-amarela-2", "cereja-vermelha-3",
                                            "cachinho", "foto-cafeeiro", "foto-lavoura-ceu", "foto-lavoura-rua",
                                            "foto-cereja-verde", "fita-crepe", "kraft"]])
    print(len(ids), "peças novas na biblioteca")


if __name__ == "__main__":
    main()
