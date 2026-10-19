"""Monta a foto de capa de um kit lado a lado a partir de recortes reais sobre branco.

Composição local de pixel real (fluxo 3 do CLAUDE.md): cada pacote é o recorte da
foto verdadeira (saída de scripts/recorte_pacote_escuro.py), só escalado e
posicionado. Nada é gerado.

    python scripts/compor_kit.py SAIDA ENTRADA1 ENTRADA2 [ENTRADA3 ...]

Todas as entradas devem ter fundo branco. Saída 1500x2000 (3:4), como o catálogo.
"""
import sys

import numpy as np
from PIL import Image


def bbox_nao_branco(im, limiar=245):
    a = np.asarray(im.convert('L'))
    ys, xs = np.nonzero(a < limiar)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def compor(saida, entradas, larg=1500, alt=2000, margem=0.07, vao=0.03):
    cortes = [Image.open(e).convert('RGB') for e in entradas]
    cortes = [c.crop(bbox_nao_branco(c)) for c in cortes]
    n = len(cortes)
    h_alvo = int(alt * (1 - 2 * margem))
    escalados = [c.resize((int(c.width * h_alvo / c.height), h_alvo), Image.LANCZOS) for c in cortes]
    total = sum(c.width for c in escalados) + int(larg * vao) * (n - 1)
    lim = int(larg * (1 - 2 * margem))
    if total > lim:  # não cabe: reduz tudo por igual
        f = lim / total
        escalados = [c.resize((int(c.width * f), int(c.height * f)), Image.LANCZOS) for c in escalados]
        total = sum(c.width for c in escalados) + int(larg * vao * f) * (n - 1)
        gap = int(larg * vao * f)
    else:
        gap = int(larg * vao)
    tela = Image.new('RGB', (larg, alt), 'white')
    x = (larg - total) // 2
    for c in escalados:
        y = (alt - c.height) // 2
        # cola só o que não é branco, para não apagar o vizinho com a borda branca
        m = Image.fromarray((np.asarray(c.convert('L')) < 250).astype(np.uint8) * 255)
        tela.paste(c, (x, y), m)
        x += c.width + gap
    tela.save(saida, quality=95)
    return tela.size


if __name__ == '__main__':
    print(compor(sys.argv[1], sys.argv[2:]))
