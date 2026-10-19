# -*- coding: utf-8 -*-
"""Gera as fotos da entrega da Loja Integrada, em JPG, nomeadas por produto.

Rode a partir do diretório principal do repositório (as pastas de imagem são
gitignored e só existem lá):

    .venv/Scripts/python.exe loja-integrada/montar_fotos.py

Cada produto leva a frente conferida contra a foto real do pacote. Onde o
packshot gerado foi REPROVADO na conferência, entra foto real recortada ou a
composição corrigida — nunca o packshot defeituoso.
"""
import os, sys, json
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from catalogo import PRODUTOS

GERADO = "saida-teste/catalogo-estudio"
SAIDA = os.path.join(AQUI, "entrega", "fotos")
QUALIDADE = 88
TETO_MB = 1.0

# Só onde o packshot gerado NÃO serve. O resto é derivado do catálogo.
# motivo fica registrado no LEIA-ME.
SUBSTITUICOES = {
    "CAN-CLA-GR-1000": ["saida-teste/ml-classico-1kg/1-frente.jpg",
                        "saida-teste/ml-classico-1kg/2-tres-quartos.jpg",
                        "saida-teste/ml-classico-1kg/3-verso.jpg"],
    "CAN-SUA-GR-1000": ["saida-teste/ml-suave-1kg/1-frente.jpg"],
    "CAN-MIC-MO-250":  ["saida-teste/_li-correcao/13.1-frente-branco-selo-real.png"],
}

# fotos reais extras, para produtos cujo packshot foi aprovado
EXTRAS = {
    "CAN-CLA-MO-500": ["saida-teste/ml-500g-moido/classico.jpg"],
    "CAN-SUA-MO-500": ["saida-teste/ml-500g-moido/suave.jpg"],
    "NEC-GOU-MO-500": ["saida-teste/ml-500g-moido/nectar.jpg"],
    "NEC-GOU-GR-1000": ["saida-teste/ml-nectar-gourmet-1kg/2-tres-quartos.jpg",
                        "saida-teste/ml-nectar-gourmet-1kg/3-verso.jpg"],
}

SLUG = {
    "CAN-CLA-GR-250": "classico-graos-250g",   "CAN-CLA-MO-250": "classico-moido-250g",
    "CAN-CLA-GR-500": "classico-graos-500g",   "CAN-CLA-MO-500": "classico-moido-500g",
    "CAN-CLA-GR-1000": "classico-graos-1kg",   "CAN-SUA-GR-250": "suave-graos-250g",
    "CAN-SUA-MO-250": "suave-moido-250g",      "CAN-SUA-GR-500": "suave-graos-500g",
    "CAN-SUA-MO-500": "suave-moido-500g",      "CAN-SUA-GR-1000": "suave-graos-1kg",
    "CAN-CAN-MO-250": "canela-moido-250g",     "CAN-MIC-GR-250": "microlote-graos-250g",
    "CAN-MIC-MO-250": "microlote-moido-250g",  "NEC-GOU-GR-1000": "nectar-gourmet-graos-1kg",
    "NEC-GOU-MO-500": "nectar-gourmet-moido-500g", "CAN-CAP-CLA-10": "capsulas-classico-10un",
    "CAN-CAP-CAN-10": "capsulas-canela-10un",  "CAN-CAP-SUA-10": "capsulas-suave-10un",
    "CAN-DRI-CLA-10": "drip-coffee-classico-10un", "CAN-DRI-SUA-10": "drip-coffee-suave-10un",
}


def fundo_limpo(im, moldura=24, limiar=215):
    """Conta pixels escuros na moldura da borda. Prova que o fundo é limpo.

    O limiar é 215, não 235: medido, o pixel mais escuro da moldura destes
    packshots é 225 — o vinhetado do ciclorama, invisível na tela. Um limiar que
    acende em todas as peças não está medindo defeito (lição 47).
    """
    a = np.asarray(im.convert("RGB")).astype(int)
    borda = np.concatenate([a[:moldura].reshape(-1, 3), a[-moldura:].reshape(-1, 3),
                            a[:, :moldura].reshape(-1, 3), a[:, -moldura:].reshape(-1, 3)])
    return int((borda.min(axis=1) < limiar).sum()), len(borda)


def main():
    os.makedirs(SAIDA, exist_ok=True)
    mapa, problemas = {}, []
    for ordem, (sku, tray, pasta_g, _pr, _cat, _fmt, _ean) in enumerate(PRODUTOS, 1):
        n = pasta_g.split("-")[0]
        if sku in SUBSTITUICOES:
            origens = SUBSTITUICOES[sku]
        else:
            origens = [os.path.join(GERADO, pasta_g, f"{n}.1-frente-branco.png")] + EXTRAS.get(sku, [])
        arquivos = []
        for i, origem in enumerate(origens, 1):
            if not os.path.exists(origem):
                problemas.append(f"{sku}: origem sumiu — {origem}")
                continue
            im = Image.open(origem).convert("RGB")
            nome = f"{ordem:02d}-{SLUG[sku]}-{i}.jpg"
            destino = os.path.join(SAIDA, nome)
            im.save(destino, quality=QUALIDADE, optimize=True)
            mb = os.path.getsize(destino) / 1e6
            sujos, total = fundo_limpo(im)
            if mb > TETO_MB:
                problemas.append(f"{nome}: {mb:.2f} MB acima do teto")
            if sujos:
                problemas.append(f"{nome}: {sujos}/{total} pixels não-brancos na moldura")
            arquivos.append(nome)
            print(f"{nome:<44} {im.size[0]}x{im.size[1]}  {mb:.2f} MB  moldura suja: {sujos}")
        mapa[sku] = arquivos
    json.dump(mapa, open(os.path.join(AQUI, "mapa-fotos.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n{sum(len(v) for v in mapa.values())} arquivos para {len(mapa)} produtos")
    for p in problemas:
        print("PROBLEMA:", p)
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
