"""Passe MINIMO de humanizacao. Faz so tres coisas, nesta ordem.

    1. reduz para 1080x1350 (feed 4:5)
    2. corrige a SATURACAO ao alvo medido - bidirecional, resolvida por medicao
    3. recomprime em JPEG, como celular recomprime

E so. NAO mexe em ponto preto, NAO estoura altas, NAO borra canto, NAO aplica
mascara de nitidez, NAO injeta ruido.

Portado de `_ref-scripts/minimo.py`, que e a unica versao que FUNCIONOU. As duas
anteriores (`calibrar.py` e `calibrar2.py`) empilhavam etapas e sairam
net-negativas: consertavam uma metrica e estragavam tres. O que elas ensinaram:

  - `calibrar.py` levantava sombra, estourava altas, esfriava R **e** aquecia B
    (dose dobrada), borrava canto, aplicava unsharp e injetava ruido. Cada etapa
    era defensavel sozinha; juntas, pioraram o resultado.
  - `calibrar2.py` ja media antes de agir, mas seguiu corrigindo cinco metricas.
    O canto borrado dela envenenou a leitura de ruido (ver `cie.metricas`).
  - A humanizacao de verdade vem do PROMPT. O pos so conserta a saturacao, que e
    a unica metrica que saiu fora em TODAS as geracoes.

Regra de ouro herdada da licao 7 do CLAUDE.md: **metrica dentro da tolerancia nao
se toca**. Por isso a correcao de saturacao e condicionada, nao incondicional.

--- Se um dia alguem precisar injetar ruido aditivo (nao precisa: a geracao ja vem
com mais ruido que o alvo), a forma correta e:

    im = ImageChops.add(im, mapa_de_ruido, offset=-128)

com o mapa centrado em 128. **Nunca** `ImageChops.subtract`: ele satura em 0, o
que apaga a metade negativa do ruido; somar 128 depois levanta tudo e a imagem
vira nevoa leitosa. Foi a licao 5 do CLAUDE.md, paga com uma rodada de geracao.
"""

from __future__ import annotations

import io

from PIL import Image, ImageOps

from .metricas import ALVO, TOLERANCIA, Metricas, fora_do_alvo, medir

#: Especificacao do feed 4:5.
TAMANHO_FEED = (1080, 1350)

#: Recompressao: o passe baixo imita o que o celular/rede fazem com o arquivo.
#: Quem chama salva o resultado final em qualidade alta (92 no script de origem).
QUALIDADE_RECOMPRESSAO = 76
SUBSAMPLING_RECOMPRESSAO = 2


def redimensionar(img: Image.Image) -> Image.Image:
    """Leva a imagem para 1080x1350.

    Assume entrada ja em 4:5 (o recorte de geracao entrega assim). Fora de 4:5, o
    ajuste final ESTICA em vez de recortar - recorte antes de chamar.
    """
    im = ImageOps.exif_transpose(img)
    if im.mode != "RGB":
        im = im.convert("RGB")
    im = ImageOps.contain(im, TAMANHO_FEED, Image.LANCZOS)
    if im.size != TAMANHO_FEED:
        im = im.resize(TAMANHO_FEED, Image.LANCZOS)
    return im


def _media_apos_ganho(hist: list[int], total: int, k: float) -> float:
    """Media do canal S depois de multiplicar por `k`, sem tocar em pixel.

    Fecha em cima do histograma exatamente o que `point()` faria, inclusive o
    truncamento e o teto em 255. E isso que torna a correcao "resolvida por
    medicao" e nao "estimada por regra de tres": com clipping, media * k nao da
    media desejada.
    """
    return sum(n * min(255, int(v * k)) for v, n in enumerate(hist) if n) / total


def resolver_ganho_saturacao(canal_s: Image.Image, alvo: float) -> float:
    """Busca o ganho `k` que leva a media de S ao alvo. Bidirecional por natureza.

    k > 1 quando a imagem esta ABAIXO do alvo (satura mais), k < 1 quando esta
    acima (dessatura). A funcao e monotona em k, entao bissecao resolve.

    Se nem o ganho maximo alcanca o alvo (imagem sem croma para esticar), devolve
    o teto: nao da para inventar cor onde nao ha.
    """
    hist = canal_s.histogram()
    total = sum(hist)
    if total == 0:
        return 1.0

    baixo, alto = 0.0, 1.0
    while _media_apos_ganho(hist, total, alto) < alvo and alto < 64.0:
        alto *= 2.0
    if _media_apos_ganho(hist, total, alto) < alvo:
        return alto  # imagem quase acromatica: sem croma para esticar

    for _ in range(40):
        meio = (baixo + alto) / 2
        if _media_apos_ganho(hist, total, meio) < alvo:
            baixo = meio
        else:
            alto = meio
    return (baixo + alto) / 2


def corrigir_saturacao(img: Image.Image, alvo: float) -> Image.Image:
    """Aplica o ganho resolvido no canal S. Sem gate: quem decide e `humanizar`."""
    matiz, saturacao, valor = img.convert("HSV").split()
    k = resolver_ganho_saturacao(saturacao, alvo)
    tabela = [min(255, int(v * k)) for v in range(256)]
    return Image.merge("HSV", (matiz, saturacao.point(tabela), valor)).convert("RGB")


def recomprimir(img: Image.Image) -> Image.Image:
    """Passa por um JPEG de qualidade media e volta. Nada mais."""
    buffer = io.BytesIO()
    img.save(
        buffer,
        "JPEG",
        quality=QUALIDADE_RECOMPRESSAO,
        subsampling=SUBSAMPLING_RECOMPRESSAO,
    )
    buffer.seek(0)
    saida = Image.open(buffer)
    saida.load()
    return saida if saida.mode == "RGB" else saida.convert("RGB")


def humanizar(img: Image.Image, alvo_saturacao: float = ALVO.saturacao) -> Image.Image:
    """Redimensiona, corrige a saturacao ao alvo e recomprime. Nada mais.

    A correcao de saturacao e BIDIRECIONAL: imagem lavada sobe, imagem vibrante
    desce. E so acontece se a medida estiver FORA da tolerancia - metrica dentro
    da tolerancia nao se toca (licao 7).

    Nao altera a imagem recebida; devolve uma nova.
    """
    im = redimensionar(img)
    # Mede com o MESMO instrumento do relatorio (`cie.metricas.medir`), e nao com
    # uma media de S propria: o gate tem que usar exatamente o numero que depois
    # vai ser comparado ao alvo.
    medida = medir(im).saturacao
    if abs(medida - alvo_saturacao) > TOLERANCIA["saturacao"]:
        im = corrigir_saturacao(im, alvo_saturacao)
    return recomprimir(im)


def diagnosticar(img: Image.Image) -> tuple[Metricas, list[str]]:
    """Mede a imagem ja no tamanho de entrega e diz o que ficou fora do alvo.

    Existe para o relatorio: as metricas so sao comparaveis ao alvo depois da
    reducao para 1080x1350.
    """
    m = medir(redimensionar(img))
    return m, fora_do_alvo(m)
