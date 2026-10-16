"""Cola trechos do rotulo REAL sobre a embalagem gerada, alinhando pelo proprio rotulo.

Uso:
    python -m uv run python scripts/compor_rotulo.py <gerada.png> <referencia.png> <saida.png> \
        --caixa desde1985=588,818,738,892 --caixa classico=338,1093,472,1174

As caixas sao em coordenadas da REFERENCIA (a foto de estudio aprovada). O script acha
onde elas caem na gerada e cola so ali.

POR QUE EXISTE. O texto pequeno do rotulo e o que a geracao erra -- `Desde 1985` e
`TORRADO E MOIDO` quebraram em todas as rodadas da capa do carrossel de historia
(07/10/2026), enquanto logo, selo e peso sairam certos. Soletrar nao converge (licao
46); colar o pixel real converge na primeira passada.

COMO ALINHA. SIFT na frente do pacote das duas imagens, casamento por razao de Lowe e
`estimateAffinePartial2D` com RANSAC (escala + rotacao + translacao). Medido na capa
v3: 211 inliers, escala 0,6227, rotacao -0,59 graus, erro mediano 0,72 px. Se o erro
mediano passar de 1,5 px ou houver menos de 40 inliers, o script RECUSA: a embalagem
gerada nao e uma copia em escala da referencia (angulo diferente, rotulo redesenhado)
e colar ali criaria um remendo visivel.

COMO PRESERVA O RESTO. Casamento de nivel por percentil (p5 -> p5, p99.5 -> p99.5) em
cada canal, mascara com borda suave de ~1,6 px, e `assert` de ZERO pixels alterados
fora das caixas. Os presets abaixo valem para `6.1-frente-branco.png` (Classico 250g
moido); para outro SKU, meca as caixas no pixel da referencia (licao 30).
"""

from __future__ import annotations

import argparse
import sys

import cv2
import numpy as np

PRESETS = {
    # saida-teste/catalogo-estudio/6-classico-250g-moido/6.1-frente-branco.png
    "classico-moido": {
        "desde1985": (588, 818, 738, 892),
        "classico": (338, 1093, 472, 1174),
    },
    # saida-teste/catalogo-estudio/1-suave-250g-moido/1.1-frente-branco.png
    # (medido no pixel em 07/10/2026; texto PRETO sobre kraft)
    "suave-moido": {
        "desde1985": (596, 900, 760, 972),
        "suave": (318, 1200, 452, 1256),
    },
    # saida-teste/catalogo-estudio/11-canela-250g-moido/11.1-frente-branco.png
    # (medido no pixel em 07/10/2026)
    "canela-moido": {
        "desde1985": (616, 948, 778, 1022),
        "canela": (338, 1182, 566, 1242),
    },
}


def alinhar(g: np.ndarray, r: np.ndarray,
            regiao: tuple[int, int, int, int] | None = None) -> tuple[np.ndarray, int, float, float]:
    gg = cv2.cvtColor(g, cv2.COLOR_BGR2GRAY)
    rg = cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)
    # Referencia de estudio: so o pacote interessa, nao o ciclorama branco.
    mr = cv2.dilate((rg < 235).astype(np.uint8) * 255, np.ones((25, 25), np.uint8))
    mg = None
    if regiao:
        x0, y0, x1, y1 = regiao
        mg = np.zeros_like(gg)
        mg[y0:y1, x0:x1] = 255
    sift = cv2.SIFT_create(4000)
    kg, dg = sift.detectAndCompute(gg, mg)
    kr, dr = sift.detectAndCompute(rg, mr)
    pares = cv2.BFMatcher().knnMatch(dr, dg, k=2)
    bons = [m for m, n in pares if m.distance < 0.75 * n.distance]
    if len(bons) < 10:
        raise SystemExit(f"so {len(bons)} pontos casados: a referencia nao e esta embalagem")
    src = np.float32([kr[m.queryIdx].pt for m in bons])
    dst = np.float32([kg[m.trainIdx].pt for m in bons])
    M, inl = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=2.5)
    ok = inl.ravel() == 1
    # Segunda passada: so os inliers, limiar apertado -- tira o ruido do RANSAC.
    M2, inl2 = cv2.estimateAffinePartial2D(src[ok], dst[ok], method=cv2.RANSAC,
                                           ransacReprojThreshold=1.2, maxIters=5000)
    if M2 is not None and int(inl2.sum()) >= 40:
        M = M2
        sel = np.flatnonzero(ok)[inl2.ravel() == 1]
        ok = np.zeros(len(src), bool)
        ok[sel] = True
    p = (M[:, :2] @ src[ok].T).T + M[:, 2]
    erro = float(np.median(np.linalg.norm(p - dst[ok], axis=1)))
    escala = float(np.hypot(M[0, 0], M[1, 0]))
    return M, int(ok.sum()), escala, erro


def compor(g, r, M, caixas: dict[str, tuple[int, int, int, int]]):
    g = g.astype(np.float32)
    H, W = g.shape[:2]
    rw = cv2.warpAffine(r.astype(np.float32), M, (W, H), flags=cv2.INTER_LANCZOS4)
    out = g.copy()
    onde = {}
    for nome, (x0, y0, x1, y1) in caixas.items():
        cs = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], np.float32)
        cg = (M[:, :2] @ cs.T).T + M[:, 2]
        gx0, gy0 = np.floor(cg.min(0)).astype(int)
        gx1, gy1 = np.ceil(cg.max(0)).astype(int)
        pg, pr = g[gy0:gy1, gx0:gx1], rw[gy0:gy1, gx0:gx1]
        aj = np.empty_like(pr)
        for c in range(3):
            a5, a99 = np.percentile(pr[..., c], [5, 99.5])
            b5, b99 = np.percentile(pg[..., c], [5, 99.5])
            aj[..., c] = (pr[..., c] - a5) * ((b99 - b5) / max(a99 - a5, 1)) + b5
        m = np.zeros((H, W), np.float32)
        m[gy0 + 3:gy1 - 3, gx0 + 3:gx1 - 3] = 1
        m = cv2.GaussianBlur(m, (0, 0), 1.6)
        m[:gy0, :] = 0; m[gy1:, :] = 0; m[:, :gx0] = 0; m[:, gx1:] = 0
        cheio = g.copy()
        cheio[gy0:gy1, gx0:gx1] = aj
        out = out * (1 - m[..., None]) + cheio * m[..., None]
        onde[nome] = (int(gx0), int(gy0), int(gx1), int(gy1))
    out = np.clip(out, 0, 255)
    fora = np.abs(out - g).max(axis=2) > 0.5
    for x0, y0, x1, y1 in onde.values():
        fora[y0:y1, x0:x1] = False
    assert int(fora.sum()) == 0, f"{int(fora.sum())} pixels alterados FORA das caixas"
    return out.astype(np.uint8), onde


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("gerada"); ap.add_argument("referencia"); ap.add_argument("saida")
    ap.add_argument("--preset", choices=sorted(PRESETS))
    ap.add_argument("--caixa", action="append", default=[],
                    help="nome=x0,y0,x1,y1 em coordenadas da referencia")
    ap.add_argument("--regiao", help="x0,y0,x1,y1 do pacote na GERADA (opcional; "
                    "limita a deteccao e evita casar folha e terra com o rotulo)")
    a = ap.parse_args(argv)
    regiao = tuple(int(x) for x in a.regiao.split(",")) if a.regiao else None
    caixas = dict(PRESETS.get(a.preset, {}))
    for c in a.caixa:
        nome, v = c.split("=")
        caixas[nome] = tuple(int(x) for x in v.split(","))
    if not caixas:
        raise SystemExit("nenhuma caixa: use --preset ou --caixa")
    g, r = cv2.imread(a.gerada), cv2.imread(a.referencia)
    M, inl, escala, erro = alinhar(g, r, regiao)
    print(f"inliers {inl} | escala {escala:.4f} | erro mediano {erro:.2f}px")
    if inl < 40 or erro > 1.5:
        raise SystemExit("alinhamento fraco: a embalagem gerada nao e copia em escala da "
                         "referencia; gere de novo de frente ou componha o recorte inteiro")
    out, onde = compor(g, r, M, caixas)
    cv2.imwrite(a.saida, out)
    print("colado em", onde, "| 0 pixels fora das caixas")
    print("CONFIRA ampliando cada caixa: o script prova o alinhamento, nao a leitura")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
