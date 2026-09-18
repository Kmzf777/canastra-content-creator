"""Fecha as imagens escolhidas para o site: renomeia, redimensiona, comprime.

O que sai daqui vai direto para `frontend/public/`. Nome em kebab-case com
palavra-chave, porque nome de arquivo e sinal de SEO de imagem — `hero-01.jpg`
nao diz nada, `cafe-especial-serra-da-canastra-heroi.jpg` diz.

O `next/image` reconverte para AVIF/WebP e gera o srcset, entao aqui a saida e
JPEG progressivo de qualidade alta no tamanho maximo util. Nao adianta entregar
5000px: o teto de peso do heroi e 250 KB servido, e o `next/image` corta a partir
do que receber.

    python -m uv run python scripts/home_entregar.py --listar
    python -m uv run python scripts/home_entregar.py
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
CENAS = RAIZ / "saida-teste" / "home-cenas"
SAIDA = RAIZ / "entrega-site"


@dataclass(frozen=True)
class Peca:
    origem: str
    destino: str
    largura: int
    qualidade: int = 86


#: As escolhas. Cada uma foi olhada com zoom em mao, rotulo e rosto, e medida
#: contra o perfil de camera — nunca escolhida por miniatura.
PECAS: tuple[Peca, ...] = (
    # HEROI. Escolhida entre 6: e a unica em que a chapada de TOPO PLANO aparece
    # correta no horizonte (as outras puxam para pico). Perfil medido p1 3,0 /
    # sat 93,9 / R-B 0,822 — na mesma faixa da foto REAL do cafezal do acervo
    # (6,3 / 91,1 / 0,839), que e o benchmark que importa.
    Peca("heroi-v5.jpg", "cafe-especial-serra-da-canastra-heroi.jpg", 2752, 84),
    # EM GRAOS. Escolhida entre 4 por ser a unica com R/B 0,954 (as outras
    # puxam quente, 1,11-1,16). Sem embalagem no quadro de proposito: nao existe
    # packshot de cafe EM GRAOS, e pacote de moido despejando grao mente.
    Peca("fmt-graos-v2.jpg", "comprar-cafe-em-graos.jpg", 1600),
    # MOIDO. Escolhida entre 8 pelo ROTULO, nao pelo perfil: e a unica em que
    # SUAVE / TORRADO E MOIDO e 250g aparecem inteiros e corretos.
    Peca("fmt-moido-p2-v1.jpg", "comprar-cafe-moido.jpg", 1600),
    # CAPSULA e DRIP. Regeradas depois de a pesquisa me pegar inventando: eu
    # tinha escrito que o copo americano tem "facetas verticais rasas". Nao tem
    # — e tronco de cone LISO, base estreita, boca larga, e e essa conicidade
    # que o faz empilhar. Nesta rodada ele sai certo, e na capsula da para ver
    # os copos empilhados.
    Peca("fmt-capsula-copo-v1.jpg", "comprar-capsulas-de-cafe.jpg", 1600),
    Peca("fmt-drip-copo-v1.jpg", "comprar-drip-coffee.jpg", 1600),
    # CLUBE. Escolhida entre 4: ele fica a esquerda e o terco direito do quadro
    # sobra para o texto da banda, que e o que o layout pede. E a camiseta nao
    # tem a marca bordada no peito que apareceu na v2.
    Peca("clube-v3.jpg", "clube-assinatura-de-cafe-especial.jpg", 2400),
)

#: NAO ENTREGUE. Tres rotulos legiveis num quadro e o pior caso de fidelidade, e
#: as 6 variantes confirmaram: "SCA 80+" saiu "GLA GB)" e o peso "250g" virou
#: "200g" — erro factual sobre o produto. A cena e otima e o rotulo nao serve.
#: Vai para _conferir/ como PLACA, para composicao local do recorte real, que e
#: a unica rota com tipografia garantida.
PENDENTE: tuple[Peca, ...] = (
    Peca("fmt-kit-v4.jpg", "_conferir/PLACA-kit-rotulo-quebrado.jpg", 1600),
)



def entregar(pecas: tuple[Peca, ...], listar: bool) -> int:
    SAIDA.mkdir(parents=True, exist_ok=True)
    faltando = [p for p in pecas if not (CENAS / p.origem).exists()]
    if listar:
        for p in pecas:
            marca = "  " if (CENAS / p.origem).exists() else "??"
            print(f"{marca} {p.origem:26s} -> {p.destino:44s} {p.largura}px")
        if faltando:
            print(f"\n{len(faltando)} origem(ns) ainda nao existe(m).", file=sys.stderr)
        return 0
    if faltando:
        print(
            "origem ausente: " + ", ".join(p.origem for p in faltando), file=sys.stderr
        )
        return 2

    for p in pecas:
        im = Image.open(CENAS / p.origem).convert("RGB")
        if im.width > p.largura:
            h = int(round(p.largura * im.height / im.width))
            im = im.resize((p.largura, h), Image.LANCZOS)
        d = SAIDA / p.destino
        im.save(d, quality=p.qualidade, optimize=True, progressive=True)
        kb = d.stat().st_size // 1024
        print(f"{p.destino:46s} {im.width}x{im.height}  {kb} KB")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--listar", action="store_true")
    a = ap.parse_args()
    return entregar(PECAS, a.listar)


if __name__ == "__main__":
    raise SystemExit(main())
