"""Fluxo 2: recorte por croma e composicao com reiluminacao.

Este e o unico caminho que da **rotulo exato ao pixel** (`docs/flow-geracao.md`,
fluxo 2). Os outros dois fluxos re-renderizam a embalagem: ficam proximos, nunca
identicos. Aqui o pixel do packshot atravessa a pipeline inteiro sem passar por
difusao.

A ordem das etapas nao e estilistica, cada uma existe por um motivo medido:

1. `recortar`             - mascara por croma com limiar MEDIDO, mais o
                            preenchimento de furos que devolve a tipografia preta
2. `medir_direcao_luz`    - o azimute sai da cena, nunca do prompt
3. `compor`               - reiluminacao no sentido medido, sombra projetada no
                            sentido oposto e oclusao de contato na base

O que este modulo **nao** faz: o passe de camera (ruido, halo de nitidez,
recompressao JPEG) sobre o quadro inteiro, que e a etapa 5 do fluxo 2 e o que de
fato costura recorte e cena. Ela vive fora daqui de proposito - envolve RNG, e
mistura-la a geometria tornaria a composicao nao deterministica.

Historico que justifica as escolhas, para nao ser refeito:

- Recorte por **flood fill** a partir das bordas (`_ref-scripts/recortar.py`)
  FALHOU: sobrou ~47% de fundo colado no recorte. A causa e estrutural, nao de
  ajuste: `ImageDraw.floodfill` com `thresh` compara cada pixel com a SEMENTE,
  nao com o vizinho, entao qualquer degrade de iluminacao da parede maior que a
  tolerancia trava o fill no meio do caminho - e afrouxar a tolerancia faz o
  fill vazar para dentro do pacote. Croma nao depende de conectividade nenhuma,
  so de cor, e por isso ganhou. Aqui o flood fill sobrevive num unico lugar,
  `preencher_furos`, onde ele opera sobre mascara binaria e a tolerancia nao tem
  degrade para atravessar.
- A primeira composicao (`_ref-scripts/compor.py`) casava o branco do recorte com
  a media da cena. Albedo nao e iluminante: o kraft e marrom, e a "correcao"
  puxava a cena inteira. Aqui a reiluminacao e so gradiente lateral geometrico.
- Assumir "luz pela esquerda" ja custou uma rodada (licao 6 do CLAUDE.md). Por
  isso `azimute_luz` e parametro **obrigatorio** de `compor`, sem valor padrao:
  quem chama tem que ter medido.

## Limiares: de onde vieram os numeros

`s_min=75` e `v_min=120` sao medicao, nao chute. `_ref-scripts/medir_sat.py`
amostrou regioes nomeadas do packshot `Suave (5).jpg` e leu, em HSV de 8 bits:

    parede             S ~ 7        V ~ 190
    bancada            S ~ 35-44    V ~ 140
    sombra na parede   S ~ 60       V ~ 95
    KRAFT              S ~ 92-103   V ~ 146-176

A sombra na parede e o unico fundo que chega perto do kraft em saturacao, e e
por isso que limiar de saturacao sozinho NAO basta: quem a separa e a
luminancia (V ~ 95 contra V >= 146 do kraft). Dai o par 75/120, com folga dos
dois lados - acima do S ~ 60 da sombra e abaixo do S ~ 92 do kraft; acima do
V ~ 95 da sombra e abaixo do V ~ 146 do kraft.

Esses valores descrevem ESTE packshot: kraft contra parede clara. Outro fundo ou
outro SKU exige rodar `medir_sat.py` de novo e passar os limiares por parametro -
nunca herdar o numero por inercia.

## Convencao de angulo

A mesma de `_ref-scripts/luz.py`, coerente com o eixo Y da imagem, que cresce
para BAIXO:

    0 graus   = direita      90 graus  = baixo
    180 graus = esquerda     270 graus = cima

`azimute_luz` e a direcao de ONDE A LUZ VEM. A sombra cai em `azimute + 180`.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps, ImageStat

from .errors import CieError

__all__ = [
    "S_MIN_MEDIDO",
    "V_MIN_MEDIDO",
    "mascara_croma",
    "preencher_furos",
    "recortar",
    "perfil_luminancia",
    "medir_direcao_luz",
    "compor",
]

# --------------------------------------------------------------------------- #
# limiares
# --------------------------------------------------------------------------- #

#: Saturacao minima para um pixel contar como embalagem. Medida, nao chutada:
#: a tabela completa de `_ref-scripts/medir_sat.py` esta no docstring do modulo.
S_MIN_MEDIDO = 75

#: Luminancia minima. E ela, e nao a saturacao, que separa a sombra na parede
#: (S ~ 60, V ~ 95) do kraft (S ~ 92-103, V ~ 146-176).
V_MIN_MEDIDO = 120

#: Lado maximo em que a pipeline roda. Os tamanhos de kernel morfologico abaixo
#: foram calibrados nessa escala; a imagem so encolhe, nunca amplia.
LADO_MAX_PADRAO = 1600

#: Alfa acima disto conta como embalagem ao calcular o bbox final.
ALFA_SOLIDO = 60


def _como_imagem(valor: Image.Image | Path | str) -> Image.Image:
    """Aceita `Image`, caminho ou string. Aplica EXIF, porque foto de celular vem deitada."""
    if isinstance(valor, Image.Image):
        return valor
    caminho = Path(valor)
    try:
        with Image.open(caminho) as aberta:
            aberta.load()
            return ImageOps.exif_transpose(aberta)
    except (OSError, ValueError) as exc:  # pragma: no cover - depende do disco
        raise CieError(f"imagem ilegivel: {caminho} ({exc})") from exc


def _reduzir(img: Image.Image, lado_max: int) -> Image.Image:
    """Encolhe para caber em `lado_max`. Nunca amplia: kernel em px nao acompanha upscale."""
    if lado_max <= 0 or max(img.size) <= lado_max:
        return img
    fator = lado_max / max(img.size)
    novo = (max(1, round(img.width * fator)), max(1, round(img.height * fator)))
    return img.resize(novo, Image.LANCZOS)


# --------------------------------------------------------------------------- #
# recorte por croma
# --------------------------------------------------------------------------- #


def mascara_croma(
    img: Image.Image | Path | str,
    s_min: int = S_MIN_MEDIDO,
    v_min: int = V_MIN_MEDIDO,
    *,
    mediana: int = 5,
) -> Image.Image:
    """Mascara binaria `L`: 255 onde `S >= s_min` **e** `V >= v_min`.

    O filtro de mediana entra antes do limiar porque o grao do papel e o ruido
    do sensor fazem pixels isolados cruzarem a fronteira nos dois sentidos.

    Esta e a etapa crua: a tipografia preta impressa **nao** aparece aqui, por
    ser escura demais (V baixo). Ela volta em `preencher_furos`.
    """
    rgb = _como_imagem(img).convert("RGB")
    hsv = rgb.convert("HSV")
    s = hsv.getchannel("S")
    v = hsv.getchannel("V")
    if mediana >= 3:
        s = s.filter(ImageFilter.MedianFilter(mediana))
        v = v.filter(ImageFilter.MedianFilter(mediana))
    return ImageChops.multiply(
        s.point(lambda x: 255 if x >= s_min else 0),
        v.point(lambda x: 255 if x >= v_min else 0),
    )


def preencher_furos(mascara: Image.Image) -> Image.Image:
    """Fecha buracos INTERIORES da silhueta. Sem isto o logotipo vira furo.

    Definicao operacional, e a razao de o metodo funcionar: **fundo verdadeiro e
    o que se alcanca a partir da borda da imagem**. Tudo que e 0 na mascara mas
    esta cercado por 255 e furo, nao fundo - e furo, por construcao, e interior
    ao objeto.

    Concretamente: a tipografia preta impressa no kraft tem `V` abaixo do limiar
    e sai da mascara de croma. Como ela e interior a silhueta da embalagem, o
    flood fill a partir da moldura nunca a alcanca, e ela e restaurada aqui.

    Limite conhecido: se o objeto encostar na borda da imagem, uma reentrancia
    aberta se conecta ao fundo e nao e tratada como furo. Recorte com margem.
    """
    if mascara.mode != "L":
        mascara = mascara.convert("L")
    # Moldura de 1 px garantidamente vazia: da a semente do flood fill um caminho
    # continuo em volta do objeto, mesmo que ele quase toque a borda.
    pad = Image.new("L", (mascara.width + 2, mascara.height + 2), 0)
    pad.paste(mascara, (1, 1))
    inv = ImageOps.invert(pad)  # 255 onde NAO ha objeto
    ImageDraw.floodfill(inv, (0, 0), 128, thresh=10)
    fundo = inv.point(lambda x: 255 if x == 128 else 0)
    cheio = ImageOps.invert(fundo)  # objeto + furos internos
    return cheio.crop((1, 1, mascara.width + 1, mascara.height + 1))


def _bloco_dominante(mascara: Image.Image, corte: float = 0.06) -> Image.Image:
    """Zera o que cai fora do bbox do blob principal, via perfil de linhas e colunas.

    Barato e suficiente: nao rotula componentes conexos, so descarta respingo
    longe do corpo do objeto. `resize(BOX)` faz a media exata por coluna/linha.
    """
    largura, altura = mascara.size
    # `tobytes()` em modo L da os valores brutos, sem passar por `getdata()`,
    # que a Pillow 14 remove.
    colunas = list(mascara.resize((largura, 1), Image.BOX).tobytes())
    linhas = list(mascara.resize((1, altura), Image.BOX).tobytes())
    c_max = max(colunas) or 1
    l_max = max(linhas) or 1
    xs = [x for x, valor in enumerate(colunas) if valor > c_max * corte]
    ys = [y for y, valor in enumerate(linhas) if valor > l_max * corte]
    if not xs or not ys:
        return mascara
    manter = Image.new("L", (largura, altura), 0)
    ImageDraw.Draw(manter).rectangle([min(xs), min(ys), max(xs), max(ys)], fill=255)
    return ImageChops.multiply(mascara, manter)


def recortar(
    img: Image.Image | Path | str,
    s_min: int = S_MIN_MEDIDO,
    v_min: int = V_MIN_MEDIDO,
    *,
    lado_max: int = LADO_MAX_PADRAO,
    fechamento: int = 9,
    abertura: int = 7,
    suavizacao: float = 1.0,
    com_preenchimento: bool = True,
) -> Image.Image:
    """Recorta a embalagem do packshot por croma. Devolve RGBA cortado ao bbox.

    Os padroes `s_min=75` e `v_min=120` sao medicao, nao gosto: ver
    `S_MIN_MEDIDO` para as leituras de `medir_sat.py` que os produziram. Ficam
    expostos como parametro porque valem para o packshot de kraft contra parede
    clara - outro fundo exige remedir.

    Pipeline, em ordem:

    1. **croma**       - `mascara_croma`, limiar em HSV
    2. **fechamento**  - dilata e erode: costura o kraft ao redor das letras e
                         por cima das dobras do papel
    3. **furos**       - `preencher_furos`: devolve a tipografia preta impressa,
                         que e interior a silhueta e cai fora do limiar
    4. **abertura**    - erode e dilata: mata respingo isolado sem comer a
                         silhueta
    5. **bloco**       - descarta o que sobrou longe do corpo principal
    6. **bbox**        - corta a moldura transparente

    `com_preenchimento=False` existe para diagnostico e para os testes provarem
    que a etapa 3 e o que salva o logotipo. Em producao, deixe True.

    Levanta `CieError` quando o limiar nao seleciona nada - falhar alto e melhor
    que devolver um PNG transparente que so aparece como problema tres etapas
    adiante.
    """
    rgb = _reduzir(_como_imagem(img).convert("RGB"), lado_max)
    largura, altura = rgb.size

    mascara = mascara_croma(rgb, s_min, v_min)
    if mascara.getbbox() is None:
        raise CieError(
            f"nenhum pixel com S>={s_min} e V>={v_min}: o limiar nao selecionou "
            "nada. Remeca o fundo e o produto (ver _ref-scripts/medir_sat.py) "
            "antes de mexer nos numeros."
        )

    if fechamento >= 3:
        mascara = mascara.filter(ImageFilter.MaxFilter(fechamento))
        mascara = mascara.filter(ImageFilter.MinFilter(fechamento))
    if com_preenchimento:
        mascara = preencher_furos(mascara)
    if abertura >= 3:
        mascara = mascara.filter(ImageFilter.MinFilter(abertura))
        mascara = mascara.filter(ImageFilter.MaxFilter(abertura))
    mascara = _bloco_dominante(mascara)

    alfa = mascara.filter(ImageFilter.GaussianBlur(suavizacao)) if suavizacao > 0 else mascara
    bbox = alfa.point(lambda x: 255 if x > ALFA_SOLIDO else 0).getbbox()
    if bbox is None:
        raise CieError(
            "a mascara sobrou vazia depois da morfologia: os kernels "
            f"(fechamento={fechamento}, abertura={abertura}) sao grandes demais "
            f"para um objeto desse tamanho em {largura}x{altura}."
        )

    recorte = rgb.convert("RGBA")
    recorte.putalpha(alfa)
    return recorte.crop(bbox)


# --------------------------------------------------------------------------- #
# direcao da luz
# --------------------------------------------------------------------------- #


def perfil_luminancia(
    img: Image.Image | Path | str,
    centro: tuple[int, int],
    raio: int,
    *,
    passos: int = 24,
    janela: int | None = None,
) -> list[tuple[float, float]]:
    """Le a luminancia num anel ao redor de `centro`. Devolve `[(graus, luz), ...]`.

    Existe separado de `medir_direcao_luz` justamente para poder ser auditado: a
    licao do CLAUDE.md e que **regiao amostrada se valida**. O probe original
    (`_ref-scripts/luz.py`: anel de raio 62 com janela 26 ao redor da base do
    caneco) amostrava em cima do proprio caneco em parte do anel, medindo o
    objeto quando queria medir o chao. Imprima estas leituras e confira antes de
    confiar no azimute.

    Use a mediana de cada janela, nao a media: especular de ceramica e outlier,
    e um pixel estourado nao deve mover a leitura de uma regiao inteira.
    """
    if raio <= 0:
        raise CieError(f"raio precisa ser positivo: {raio}")
    if passos < 8:
        raise CieError(f"passos precisa ser >= 8 para o ajuste harmonico: {passos}")

    lum = _como_imagem(img).convert("L")
    largura, altura = lum.size
    if janela is None:
        janela = max(3, round(raio * 0.42))
    meia = janela // 2
    cx, cy = centro

    alcance = raio + meia + 1
    if cx - alcance < 0 or cy - alcance < 0 or cx + alcance > largura or cy + alcance > altura:
        raise CieError(
            f"o anel (centro {centro}, raio {raio}, janela {janela}) nao cabe em "
            f"{largura}x{altura}. Amostra parcial enviesa o ajuste - reduza o "
            "raio ou mova o centro."
        )

    leituras: list[tuple[float, float]] = []
    for i in range(passos):
        graus = 360.0 * i / passos
        rad = math.radians(graus)
        x = cx + raio * math.cos(rad)
        y = cy + raio * math.sin(rad)  # Y cresce para BAIXO
        caixa = (round(x) - meia, round(y) - meia, round(x) + meia + 1, round(y) + meia + 1)
        leituras.append((graus, float(ImageStat.Stat(lum.crop(caixa)).median[0])))
    return leituras


def medir_direcao_luz(
    img: Image.Image | Path | str,
    centro: tuple[int, int],
    raio: int,
    *,
    passos: int = 24,
    janela: int | None = None,
    corte_outlier: float = 3.0,
) -> float:
    """Azimute da luz em graus, medido no anel de luminancia ao redor da base.

    Direcao de luz **nao se dita no prompt** - o modelo ignora, e assumir
    esquerda quando a cena veio da direita ja custou uma rodada (licao 6). O chao
    ao redor da base de um objeto e mais claro do lado de onde a luz vem e mais
    escuro do lado para onde a sombra cai; o anel le essa assimetria.

    Devolve o angulo de ONDE A LUZ VEM, na convencao do modulo (0 = direita,
    90 = baixo, 180 = esquerda, 270 = cima).

    Tres decisoes que separam isto do probe original de `_ref-scripts/luz.py`:

    - **Ajuste harmonico**, nao `argmin`. A luminancia no anel e aproximadamente
      `a + b*cos(theta - azimute)`; a primeira harmonica usa as `passos`
      amostras de uma vez, entao um ponto ruim desloca pouco. `argmin` entrega o
      resultado inteiro para a amostra mais escura, seja ela o que for.
    - **Centragem na mediana** antes do ajuste, para o termo constante nao
      vazar para o vetor quando alguma amostra e descartada.
    - **Descarte de outlier por MAD**. Se o anel raspa o proprio objeto, aquelas
      amostras nao pertencem a distribuicao do chao. `corte_outlier=3.0` nunca
      corta um cosseno limpo (o desvio maximo fica em ~0,95 MAD escalado) e
      corta um respingo de objeto sem hesitar.

    Ainda assim: **o anel tem que passar fora da silhueta**. Se mais de um terco
    das amostras for descartada, a funcao levanta `CieError` em vez de devolver
    um numero bonito medido no lugar errado.
    """
    leituras = perfil_luminancia(img, centro, raio, passos=passos, janela=janela)
    valores = [v for _, v in leituras]

    mediana = _mediana(valores)
    mad = _mediana([abs(v - mediana) for v in valores]) * 1.4826

    if mad > 0 and corte_outlier > 0:
        limite = corte_outlier * mad
        mantidas = [(g, v) for g, v in leituras if abs(v - mediana) <= limite]
    else:
        mantidas = list(leituras)

    if len(mantidas) < len(leituras) * 2 / 3:
        raise CieError(
            f"{len(leituras) - len(mantidas)} de {len(leituras)} amostras do anel "
            "sao outlier: ele provavelmente cruza o proprio objeto, e nao o chao "
            "em volta. Aumente o raio ou mova o centro (ver perfil_luminancia)."
        )

    centrada = _mediana([v for _, v in mantidas])
    soma_x = sum((v - centrada) * math.cos(math.radians(g)) for g, v in mantidas)
    soma_y = sum((v - centrada) * math.sin(math.radians(g)) for g, v in mantidas)
    if math.hypot(soma_x, soma_y) < 1e-9:
        raise CieError(
            "o anel nao tem gradiente de luminancia: nao da para medir direcao de "
            "luz em regiao chapada. Amostre ao redor da base de um objeto que "
            "projete sombra."
        )
    # Arredondar antes do modulo: sem isso um atan2 de -1e-14 volta como 359,99
    # graus, e "luz pela direita" sai lida como quase 360. Sub-micrograu nao tem
    # significado numa medida feita em janela de dezenas de pixels.
    return round(math.degrees(math.atan2(soma_y, soma_x)), 6) % 360.0


def _mediana(valores: list[float]) -> float:
    ordenados = sorted(valores)
    n = len(ordenados)
    meio = n // 2
    if n % 2:
        return ordenados[meio]
    return (ordenados[meio - 1] + ordenados[meio]) / 2.0


# --------------------------------------------------------------------------- #
# composicao
# --------------------------------------------------------------------------- #

#: Queda de luminancia entre a face iluminada e a face de sombra do objeto.
#: 0,24 reproduz o gradiente de `_ref-scripts/compor2.py` (193 -> 255 em 8 bits).
CONTRASTE_LUZ = 0.24

#: Sombra projetada: comprimento em fracao da altura do objeto, inclinacao por
#: unidade de comprimento, opacidade e cor. Valores de `compor2.py`.
SOMBRA_COMPRIMENTO = 0.38
SOMBRA_INCLINACAO = 1.15
SOMBRA_OPACIDADE = 0.42
SOMBRA_COR = (52, 42, 33)

#: Oclusao de contato: faixa curta e densa onde a base encosta no chao.
CONTATO_ALTURA = 0.045
CONTATO_OPACIDADE = 0.72
CONTATO_COR = (30, 24, 18)


def _gradiente_lateral(largura: int, altura: int, para_direita: bool) -> Image.Image:
    """Rampa horizontal 0->255. Construida explicitamente, sem depender de `rotate`."""
    linha = Image.new("L", (256, 1))
    linha.putdata(range(256))
    grad = linha.resize((max(1, largura), max(1, altura)), Image.BILINEAR)
    return grad if para_direita else ImageOps.mirror(grad)


def compor(
    cena: Image.Image | Path | str,
    recorte: Image.Image | Path | str,
    base_xy: tuple[int, int],
    azimute_luz: float,
    *,
    altura_px: int | None = None,
    contraste_luz: float = CONTRASTE_LUZ,
    sombra_comprimento: float = SOMBRA_COMPRIMENTO,
    sombra_inclinacao: float = SOMBRA_INCLINACAO,
    sombra_opacidade: float = SOMBRA_OPACIDADE,
    sombra_cor: tuple[int, int, int] = SOMBRA_COR,
    contato_altura: float = CONTATO_ALTURA,
    contato_opacidade: float = CONTATO_OPACIDADE,
    contato_cor: tuple[int, int, int] = CONTATO_COR,
) -> Image.Image:
    """Compoe o recorte real na cena, reiluminado para a luz MEDIDA. Devolve RGB.

    `base_xy` e o ponto do chao onde o **centro da base** do objeto encosta; o
    recorte e ancorado ali, nao pelo canto superior esquerdo, porque e a base que
    tem significado fisico (e dela que saem a sombra e a oclusao).

    `azimute_luz` **nao tem valor padrao, de proposito**. Nao existe direcao de
    luz razoavel para adivinhar: meca com `medir_direcao_luz` na propria cena.
    Assumir a direcao e a licao 6 do CLAUDE.md, e ela custou uma rodada inteira.

    Tres efeitos, todos derivados do azimute:

    - **Reiluminacao**: gradiente lateral multiplicativo, face voltada para a luz
      clara e a oposta escura. A amplitude escala com `|cos(azimute)|`, entao luz
      frontal ou de topo (90/270 graus) nao produz gradiente lateral nenhum - o
      que e o comportamento correto, nao um bug.
    - **Sombra projetada**: silhueta achatada no plano do chao, inclinada no
      sentido oposto ao da luz e ancorada na base. Luz pela direita joga a sombra
      para a esquerda. A componente vertical decide se a sombra vai para tras
      (para cima no quadro) ou para a frente.
    - **Oclusao de contato**: faixa curta, densa e centrada na linha da base.
      Metade dela fica sob o objeto e metade escapa no chao. **Sem ela o objeto
      parece colado por cima da foto** - e o defeito que o fluxo 1 nao resolve.

    Nao aplica passe de camera: ruido, halo e JPEG vem depois, sobre o quadro
    inteiro de uma vez, e e isso que costura recorte e cena.
    """
    fundo = _como_imagem(cena).convert("RGB").copy()
    largura, altura = fundo.size

    rgba = _como_imagem(recorte)
    if rgba.mode != "RGBA":
        if "A" not in rgba.getbands() and "transparency" not in rgba.info:
            raise CieError(
                "recorte sem canal alfa: compor precisa da silhueta para gerar "
                "sombra e oclusao. Passe a saida de `recortar`."
            )
        rgba = rgba.convert("RGBA")
    _, alfa_max = rgba.getchannel("A").getextrema()
    if alfa_max == 0:
        raise CieError("recorte totalmente transparente")

    if altura_px is not None:
        if altura_px <= 0:
            raise CieError(f"altura_px precisa ser positiva: {altura_px}")
        nova_l = max(1, round(rgba.width * altura_px / rgba.height))
        rgba = rgba.resize((nova_l, altura_px), Image.LANCZOS)

    cl, ch = rgba.size
    base_x, base_y = int(base_xy[0]), int(base_xy[1])
    pos = (base_x - cl // 2, base_y - ch)
    alfa = rgba.getchannel("A")

    rad = math.radians(azimute_luz)
    lx = math.cos(rad)   # + = luz vem da direita
    ly = math.sin(rad)   # + = luz vem de baixo do quadro

    # ------------------------------------------------------------ reiluminacao
    corpo = rgba.convert("RGB")
    amplitude = max(0.0, min(1.0, contraste_luz)) * abs(lx)
    if amplitude > 0:
        escuro = 1.0 - amplitude
        rampa = _gradiente_lateral(cl, ch, para_direita=lx >= 0)
        fator = rampa.point(lambda v: round(255 * (escuro + (1.0 - escuro) * v / 255.0)))
        corpo = ImageChops.multiply(corpo, Image.merge("RGB", (fator, fator, fator)))

    # -------------------------------------------------------- sombra projetada
    if sombra_opacidade > 0 and sombra_comprimento > 0:
        sh_h = max(3, round(ch * sombra_comprimento))
        achatada = alfa.resize((cl, sh_h), Image.LANCZOS)
        # Cisalhamento: a ponta distante da sombra desloca contra a luz; a ponta
        # colada na base fica onde o objeto esta.
        inclina = -sombra_inclinacao * lx
        margem = math.ceil(abs(inclina) * sh_h) + 2
        camada = Image.new("L", (cl + 2 * margem, sh_h), 0)
        camada.paste(achatada, (margem, 0))
        camada = camada.transform(
            camada.size,
            Image.AFFINE,
            (1, inclina, -inclina * sh_h, 0, 1, 0),
            resample=Image.BICUBIC,
        )
        camada = camada.filter(ImageFilter.GaussianBlur(max(1.0, ch * 0.01)))
        camada = camada.point(lambda v: round(v * max(0.0, min(1.0, sombra_opacidade))))
        # Luz vinda de baixo do quadro (ly > 0) joga a sombra para tras, ou seja,
        # para cima. Vinda de cima, a sombra vem na direcao da camera.
        para_cima = ly >= 0
        if not para_cima:
            camada = camada.transpose(Image.FLIP_TOP_BOTTOM)
        topo = base_y - sh_h if para_cima else base_y
        capa = Image.new("L", (largura, altura), 0)
        capa.paste(camada, (pos[0] - margem, topo))
        fundo = Image.composite(Image.new("RGB", (largura, altura), sombra_cor), fundo, capa)

    # ----------------------------------------------------- oclusao de contato
    if contato_opacidade > 0 and contato_altura > 0:
        oc_h = max(4, round(ch * contato_altura))
        # So a faixa inferior da silhueta: e ela que encosta no chao. Achatar o
        # objeto inteiro daria a pegada errada em qualquer forma que nao seja
        # retangular.
        pe = max(1, round(ch * 0.12))
        pegada = alfa.crop((0, ch - pe, cl, ch)).resize((cl, oc_h), Image.LANCZOS)
        pegada = pegada.filter(ImageFilter.GaussianBlur(max(1.0, oc_h * 0.35)))
        pegada = pegada.point(lambda v: round(v * max(0.0, min(1.0, contato_opacidade))))
        capa2 = Image.new("L", (largura, altura), 0)
        capa2.paste(pegada, (pos[0], base_y - oc_h // 2))
        fundo = Image.composite(Image.new("RGB", (largura, altura), contato_cor), fundo, capa2)

    fundo.paste(corpo, pos, alfa)
    return fundo
