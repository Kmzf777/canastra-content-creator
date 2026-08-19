"""Perfil de camera medido: as 7 metricas que separam foto de celular de render.

Portado de `_ref-scripts/medir_humanizacao.py` (script descartavel que produziu os
numeros) para virar codigo versionado. Cada metrica existe porque um olho treinado
a le inconscientemente:

    p1                    ponto preto real. HDR de celular nao desce mais que isso.
    preto_pct             % de pixels colados em 0. Celular quase nunca chega la.
    estourado_pct         % de pixels colados em 255. Celular estoura sem pedir licenca.
    saturacao             media do canal S. Nossa base e LAVADA, nao vibrante.
    cast_alta_rb          R/B nas altas luzes. Nossa base puxa AZUL; dourado quente
                          e assinatura de IA.
    nitidez_centro_borda  desvio do Laplaciano do centro / media dos 4 cantos.
                          Lente barata desaba nos cantos: espera-se > 1.
    ruido                 desvio no bloco 8x8 MAIS LISO. Render tem ~0.

O ALVO nao e gosto pessoal: e a mediana das NOSSAS proprias fotos de celular
(iPhone 7 na fazenda + Motorola nos packshots).

Duas ressalvas que vem do CLAUDE.md e valem mais que os numeros:

1. As metricas medem assinatura de DISPOSITIVO, nao plausibilidade de conteudo.
   Uma imagem calibrada com pao de queijo em formato errado e pior que uma com
   duas metricas fora e comida crivel.
2. O alvo de `p1` depende da luz da cena. O 14 veio de sol forte; em luz difusa,
   sombra levantada e o comportamento correto, nao um defeito a corrigir.

Escala: os alvos foram medidos em imagens normalizadas para ~1080-1400 px no lado
maior. `ruido` e `nitidez_centro_borda` dependem da resolucao (reamostragem come
ruido e microcontraste), entao comparar um 4K cru contra o alvo nao diz nada.
Meca depois de reduzir para o tamanho de entrega.
"""

from __future__ import annotations

from dataclasses import dataclass, fields

from PIL import Image, ImageFilter, ImageOps, ImageStat

#: Laplaciano 3x3 com offset 128 para caber em 8 bits sem cortar o negativo.
LAPLACIANO = ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], scale=1, offset=128)

#: Lado do bloco usado na busca pelo trecho mais liso da imagem.
BLOCO_RUIDO = 8

#: Fracao descartada de CADA lado antes de procurar o bloco mais liso.
#: Ver `_regiao_ruido`: medir ruido no canto e medir a propria moleza da lente.
MARGEM_RUIDO = 0.3


@dataclass(frozen=True)
class Metricas:
    """As 7 metricas do perfil de camera. Ordem = ordem do relatorio."""

    p1: int
    preto_pct: float
    estourado_pct: float
    saturacao: float
    cast_alta_rb: float
    nitidez_centro_borda: float
    ruido: float

    def como_dict(self) -> dict[str, float]:
        return {campo.name: getattr(self, campo.name) for campo in fields(self)}


#: Alvo medido no grupo "nosso celular real". Numeros do CLAUDE.md.
ALVO = Metricas(
    p1=14,
    preto_pct=0.007,
    estourado_pct=0.015,
    saturacao=70.0,
    cast_alta_rb=0.969,
    nitidez_centro_borda=1.57,
    ruido=0.42,
)

#: Tolerancia por metrica. Fora dela = vale corrigir; dentro = NAO TOQUE
#: (licao 7 do CLAUDE.md: mexer no que ja estava dentro foi o que tornou as duas
#: tentativas de calibracao completa net-negativas).
#:
#: `ruido` de proposito NAO tem tolerancia: entra no relatorio, nao no julgamento.
#: A geracao ja costuma vir com mais ruido que o alvo, e injetar ruido em pos foi
#: exatamente o passo que estragou `calibrar.py`.
TOLERANCIA: dict[str, float] = {
    "p1": 6,
    "preto_pct": 0.02,
    "estourado_pct": 0.02,
    "saturacao": 12.0,
    "cast_alta_rb": 0.04,
    "nitidez_centro_borda": 0.22,
}


def _regiao_ruido(largura: int, altura: int) -> tuple[int, int, int, int]:
    """Miolo da imagem, onde a lente ainda resolve.

    O ruido e amostrado SO aqui. `calibrar.py` media o quadro inteiro depois de
    aplicar desfoque de canto: o bloco mais liso passava a ser o proprio canto
    borrado, a metrica dava ~0 e o passe injetava ruido a mais para "compensar"
    algo que nunca faltou. O mesmo vale sem desfoque artificial nenhum - canto
    mole de lente barata (que a nossa base TEM, c/b 1.57) tambem falseia a leitura.
    """
    mx = int(largura * MARGEM_RUIDO)
    my = int(altura * MARGEM_RUIDO)
    caixa = (mx, my, largura - mx, altura - my)
    if caixa[2] - caixa[0] < BLOCO_RUIDO or caixa[3] - caixa[1] < BLOCO_RUIDO:
        return (0, 0, largura, altura)  # imagem pequena demais para recortar
    return caixa


def bloco_mais_liso(cinza: Image.Image, n: int = BLOCO_RUIDO) -> float:
    """Menor desvio padrao entre blocos n x n do miolo.

    Em area lisa, o que sobra e sensor. Render tem ~0; celular tem sempre algo.
    """
    miolo = cinza.crop(_regiao_ruido(*cinza.size))
    w, h = miolo.size
    if w < n or h < n:
        return round(ImageStat.Stat(miolo).stddev[0], 2)
    passo = max(n, min(w, h) // 24)
    menor = 999.0
    for y in range(0, h - n + 1, passo):
        for x in range(0, w - n + 1, passo):
            desvio = ImageStat.Stat(miolo.crop((x, y, x + n, y + n))).stddev[0]
            if desvio < menor:
                menor = desvio
    return round(menor, 2)


def medir(img: Image.Image) -> Metricas:
    """Mede as 7 metricas da imagem como ela esta (nao redimensiona).

    Nao redimensiona de proposito: quem chama decide a escala de comparacao. Ver
    a ressalva de escala no topo do modulo.
    """
    im = ImageOps.exif_transpose(img)
    if im.mode != "RGB":
        im = im.convert("RGB")
    largura, altura = im.size
    cinza = im.convert("L")
    hist = cinza.histogram()
    total = largura * altura

    def pct(a: int, b: int) -> float:
        return 100 * sum(hist[a : b + 1]) / total

    def percentil(p: float) -> int:
        limite, acumulado = total * p / 100, 0
        for v in range(256):
            acumulado += hist[v]
            if acumulado >= limite:
                return v
        return 255

    lap = cinza.filter(LAPLACIANO)
    cw, ch = largura // 3, altura // 3
    centro = ImageStat.Stat(lap.crop((cw, ch, 2 * cw, 2 * ch))).stddev[0]
    cantos = [
        (0, 0, cw, ch),
        (largura - cw, 0, largura, ch),
        (0, altura - ch, cw, altura),
        (largura - cw, altura - ch, largura, altura),
    ]
    borda = sum(ImageStat.Stat(lap.crop(c)).stddev[0] for c in cantos) / 4

    # Cast das altas: media RGB so dos pixels claros. Sem area clara suficiente a
    # leitura e ruido puro, entao devolve neutro em vez de inventar um numero.
    claro = cinza.point(lambda v: 255 if v > 200 else 0)
    alta = ImageStat.Stat(im, mask=claro).mean if pct(201, 255) > 0.2 else [1.0, 1.0, 1.0]

    return Metricas(
        p1=percentil(1),
        preto_pct=round(pct(0, 1), 3),
        estourado_pct=round(pct(254, 255), 3),
        saturacao=round(ImageStat.Stat(im.convert("HSV").getchannel("S")).mean[0], 1),
        cast_alta_rb=round(alta[0] / max(alta[2], 1), 3),
        nitidez_centro_borda=round(centro / max(borda, 0.01), 2),
        ruido=bloco_mais_liso(cinza),
    )


def fora_do_alvo(
    m: Metricas,
    alvo: Metricas = ALVO,
    tolerancia: dict[str, float] | None = None,
) -> list[str]:
    """Nomes das metricas que passaram da tolerancia, na ordem do dataclass.

    Metrica sem tolerancia declarada (hoje so `ruido`) nunca aparece: ela e
    diagnostico, nao criterio.
    """
    tol = TOLERANCIA if tolerancia is None else tolerancia
    return [
        campo.name
        for campo in fields(m)
        if campo.name in tol
        and abs(getattr(m, campo.name) - getattr(alvo, campo.name)) > tol[campo.name]
    ]


def relatar(tag: str, m: Metricas) -> str:
    """Linha de relatorio legivel, com X no que estiver fora."""
    ruins = set(fora_do_alvo(m))
    partes = [
        f"{nome}={valor}{' X' if nome in ruins else ''}"
        for nome, valor in m.como_dict().items()
    ]
    return f"{tag:<8} " + "  ".join(partes) + f"   [{len(ruins)} fora]"
