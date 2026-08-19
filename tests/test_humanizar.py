"""Testes do passe minimo de humanizacao.

O que estes testes travam nao e "o passe funciona", e **o passe continua minimo**.
Duas tentativas de calibracao completa (`_ref-scripts/calibrar.py` e
`calibrar2.py`) sairam net-negativas: cada etapa extra consertava uma metrica e
estragava tres. A tentacao de reintroduzi-las e permanente, entao ela e testada.

Imagens 100% sinteticas: a base real e gitignored e nao viaja para o worktree.
"""

from __future__ import annotations

import ast
import inspect
import random
from pathlib import Path

import pytest
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat

from cie import humanizar as modulo_humanizar
from cie.humanizar import (
    TAMANHO_FEED,
    diagnosticar,
    humanizar,
    recomprimir,
    redimensionar,
    resolver_ganho_saturacao,
)
from cie.metricas import ALVO, TOLERANCIA, medir

#: Ganho que deixa a foto base com saturacao ~68,5 - dentro da tolerancia do
#: alvo 70 +/- 12. Serve para exercitar o caminho "nao toque".
GANHO_NO_ALVO = 0.5672


def foto(
    size: tuple[int, int] = TAMANHO_FEED,
    *,
    seed: int = 7,
    amplitude: int = 8,
    saturacao: float = 1.0,
    extremos: bool = True,
) -> Image.Image:
    """Foto sintetica: gradiente colorido, blocos, ruido fino, extremos cravados.

    `extremos` crava um preto puro, um branco puro e uma rampa de altas quase
    coladas em 255 - e essa rampa que da dentes ao teste contra "estourar altas".

    Ordem importa: a rampa entra ANTES do ruido (area chapada no miolo viraria o
    bloco mais liso e zeraria a metrica de ruido, que e uma das guardas) e os
    quadrados de 0 e 255 entram DEPOIS (com ruido em cima, o JPEG os empurra para
    fora dos extremos e as contagens andariam sozinhas).
    """
    w, h = size
    pw, ph = max(8, w // 10), max(8, h // 10)
    pequena = Image.new("RGB", (pw, ph))
    px = pequena.load()
    for y in range(ph):
        for x in range(pw):
            r = 40 + int(150 * x / pw)
            g = 60 + int(120 * y / ph)
            b = 70 + int(100 * (1 - x / pw))
            if (x // 9 + y // 11) % 3 == 0:
                r, g, b = min(255, r + 55), max(0, g - 30), max(0, b - 25)
            px[x, y] = (r, g, b)
    im = pequena.resize(size, Image.BILINEAR)

    if extremos:
        d = ImageDraw.Draw(im)
        x0, x1 = int(w * 0.3), int(w * 0.7)
        y0, y1 = int(h * 0.6), int(h * 0.78)
        for x in range(x0, x1):
            v = 226 + int(24 * (x - x0) / (x1 - x0))  # rampa 226..250
            d.line([(x, y0), (x, y1)], fill=(v, v, v))

    if amplitude:
        rnd = random.Random(seed)
        tabela = [max(0, min(255, 128 + int((v - 128) * amplitude / 128))) for v in range(256)]
        ruido = Image.frombytes("L", size, rnd.randbytes(w * h)).point(tabela)
        # offset=-128: a forma correta de somar ruido. Ver licao 5 do CLAUDE.md.
        im = ImageChops.add(im, Image.merge("RGB", (ruido,) * 3), offset=-128)

    if extremos:
        d = ImageDraw.Draw(im)
        d.rectangle([int(w * 0.05), int(h * 0.06), int(w * 0.17), int(h * 0.15)], fill=(0, 0, 0))
        d.rectangle(
            [int(w * 0.83), int(h * 0.06), int(w * 0.95), int(h * 0.15)], fill=(255, 255, 255)
        )

    if saturacao != 1.0:
        matiz, sat, valor = im.convert("HSV").split()
        tab = [min(255, int(v * saturacao)) for v in range(256)]
        im = Image.merge("HSV", (matiz, sat.point(tab), valor)).convert("RGB")
    return im


@pytest.fixture(scope="module")
def entrada_no_alvo() -> Image.Image:
    """Foto cuja saturacao ja esta dentro da tolerancia: passe vira quase no-op."""
    return foto(saturacao=GANHO_NO_ALVO)


@pytest.fixture(scope="module")
def antes_no_alvo(entrada_no_alvo: Image.Image):
    # Medido DEPOIS do redimensionamento: so assim as metricas sao comparaveis
    # (reamostragem mexe em ruido e microcontraste).
    return medir(redimensionar(entrada_no_alvo))


@pytest.fixture(scope="module")
def depois_no_alvo(entrada_no_alvo: Image.Image):
    return medir(humanizar(entrada_no_alvo))


# --------------------------------------------------------------------------- #
# 1. as tres coisas que o passe faz
# --------------------------------------------------------------------------- #


def test_entrega_no_tamanho_do_feed():
    assert humanizar(foto(size=(1600, 2000))).size == (1080, 1350)
    assert TAMANHO_FEED == (1080, 1350)


def test_saida_passou_por_recompressao_jpeg(entrada_no_alvo: Image.Image):
    saida = humanizar(entrada_no_alvo)
    assert saida.format == "JPEG"
    assert saida.mode == "RGB"


def test_nao_altera_a_imagem_recebida(entrada_no_alvo: Image.Image):
    copia = entrada_no_alvo.copy()
    humanizar(entrada_no_alvo)
    assert ImageChops.difference(entrada_no_alvo, copia).getbbox() is None


def test_diagnosticar_mede_no_tamanho_de_entrega_e_aponta_o_que_esta_fora():
    m, fora = diagnosticar(foto(size=(1600, 2000), saturacao=3.0))
    assert "saturacao" in fora
    assert m.saturacao > ALVO.saturacao + TOLERANCIA["saturacao"]


def test_alvo_padrao_de_saturacao_e_o_medido():
    assert inspect.signature(humanizar).parameters["alvo_saturacao"].default == 70.0
    assert ALVO.saturacao == 70.0


# --------------------------------------------------------------------------- #
# REGRA 1: a correcao de saturacao e BIDIRECIONAL
# --------------------------------------------------------------------------- #


def test_ganho_e_maior_que_um_para_imagem_lavada_e_menor_para_vibrante():
    lavada = foto(saturacao=0.3).convert("HSV").getchannel("S")
    vibrante = foto(saturacao=3.0).convert("HSV").getchannel("S")

    assert resolver_ganho_saturacao(lavada, ALVO.saturacao) > 1.0
    assert resolver_ganho_saturacao(vibrante, ALVO.saturacao) < 1.0


def test_imagem_dessaturada_tem_a_saturacao_AUMENTADA():
    entrada = foto(saturacao=0.3)
    antes = medir(redimensionar(entrada))
    depois = medir(humanizar(entrada))

    assert antes.saturacao < ALVO.saturacao - TOLERANCIA["saturacao"]
    assert depois.saturacao > antes.saturacao  # subiu, nao desceu
    assert depois.saturacao == pytest.approx(ALVO.saturacao, abs=3.0)


def test_imagem_supersaturada_tem_a_saturacao_REDUZIDA():
    entrada = foto(saturacao=3.0)
    antes = medir(redimensionar(entrada))
    depois = medir(humanizar(entrada))

    assert antes.saturacao > ALVO.saturacao + TOLERANCIA["saturacao"]
    assert depois.saturacao < antes.saturacao
    assert depois.saturacao == pytest.approx(ALVO.saturacao, abs=3.0)


def test_saturacao_ja_dentro_da_tolerancia_nao_e_tocada(antes_no_alvo, depois_no_alvo):
    # Licao 7 do CLAUDE.md: nao toque em metrica que ja esta dentro.
    assert abs(antes_no_alvo.saturacao - ALVO.saturacao) <= TOLERANCIA["saturacao"]
    assert depois_no_alvo.saturacao == pytest.approx(antes_no_alvo.saturacao, abs=2.0)


def test_o_alvo_de_saturacao_e_parametrizavel():
    depois = medir(humanizar(foto(saturacao=3.0), alvo_saturacao=40.0))
    assert depois.saturacao == pytest.approx(40.0, abs=3.0)


# --------------------------------------------------------------------------- #
# REGRA 2: o passe NAO faz mais nada
# --------------------------------------------------------------------------- #

#: Margens do "nao piorou". Sao folgas de reamostragem + JPEG, nao licenca:
#: `test_as_guardas_pegam_os_passos_de_calibrar` prova que cada passo proibido
#: passa longe delas.
MARGEM_P1 = 4
MARGEM_PRETO = 0.15
MARGEM_ESTOURADO = 0.25
MARGEM_CENTRO_BORDA = 0.05
MARGEM_RUIDO = 0.25


def test_nao_mexe_em_ponto_preto_altas_canto_nem_ruido(antes_no_alvo, depois_no_alvo):
    """Numa imagem que ja esta no alvo, o passe e quase identidade.

    Pega os tres passos de `calibrar.py` que aparecem na medicao: levantar
    sombra, estourar altas e borrar canto. Ruido injetado e mascara de nitidez
    nao aparecem aqui (a recompressao JPEG come os dois) e ficam a cargo da
    guarda estrutural, em
    `test_o_modulo_nao_importa_ferramenta_de_borrar_estourar_ou_ruidar`.
    """
    assert abs(depois_no_alvo.p1 - antes_no_alvo.p1) <= MARGEM_P1
    assert abs(depois_no_alvo.preto_pct - antes_no_alvo.preto_pct) <= MARGEM_PRETO
    assert abs(depois_no_alvo.estourado_pct - antes_no_alvo.estourado_pct) <= MARGEM_ESTOURADO
    assert (
        depois_no_alvo.nitidez_centro_borda
        <= antes_no_alvo.nitidez_centro_borda + MARGEM_CENTRO_BORDA
    )
    assert depois_no_alvo.ruido <= antes_no_alvo.ruido + MARGEM_RUIDO


@pytest.mark.parametrize("ganho", [0.3, 3.0])
def test_corrigir_saturacao_nao_piora_preto_estourado_nem_canto(ganho: float):
    """Mesmo no caminho em que HA correcao, so a saturacao pode se mexer."""
    entrada = foto(saturacao=ganho)
    antes = medir(redimensionar(entrada))
    depois = medir(humanizar(entrada))

    assert depois.preto_pct <= antes.preto_pct + MARGEM_PRETO
    assert depois.estourado_pct <= antes.estourado_pct + MARGEM_ESTOURADO
    assert depois.nitidez_centro_borda <= antes.nitidez_centro_borda + MARGEM_CENTRO_BORDA
    assert depois.ruido <= antes.ruido + MARGEM_RUIDO


def test_as_guardas_pegam_os_passos_de_calibrar(entrada_no_alvo, antes_no_alvo):
    """As margens acima tem dentes: cada passo de `calibrar.py` as estoura.

    Se alguem afrouxar as margens para caber um efeito novo, este teste cai.
    """
    base = redimensionar(entrada_no_alvo)
    w, h = base.size

    # 1. levantar sombras ate o piso p1 -> mata o preto e desloca o p1
    piso = ALVO.p1
    sombra = medir(
        recomprimir(base.point([min(255, int(piso + v * (255 - piso) / 255)) for v in range(256)] * 3))
    )
    assert abs(sombra.preto_pct - antes_no_alvo.preto_pct) > MARGEM_PRETO
    assert abs(sombra.p1 - antes_no_alvo.p1) > MARGEM_P1

    # 2. estourar as altas -> colam em 255
    estouro = medir(recomprimir(base.point([min(255, int(v * 1.055)) for v in range(256)] * 3)))
    assert estouro.estourado_pct - antes_no_alvo.estourado_pct > MARGEM_ESTOURADO

    # 3. borrar os cantos -> a razao centro/borda dispara
    borrado = base.filter(ImageFilter.GaussianBlur(1.7))
    mascara = Image.new("L", (w, h), 0)
    cx, cy = w / 2, h / 2
    rmax = (cx**2 + cy**2) ** 0.5
    px = mascara.load()
    for y in range(0, h, 3):
        for x in range(0, w, 3):
            d = (((x - cx) ** 2 + (y - cy) ** 2) ** 0.5) / rmax
            v = int(255 * max(0.0, (d - 0.52) / 0.48) ** 1.7)
            for dy in range(3):
                for dx in range(3):
                    if x + dx < w and y + dy < h:
                        px[x + dx, y + dy] = v
    canto = medir(
        recomprimir(Image.composite(borrado, base, mascara.filter(ImageFilter.GaussianBlur(12))))
    )
    assert (
        canto.nitidez_centro_borda
        > antes_no_alvo.nitidez_centro_borda + MARGEM_CENTRO_BORDA
    )


def _codigo_sem_docstring(caminho: Path) -> str:
    """Fonte do modulo com docstrings e comentarios removidos.

    A docstring FALA de ImageChops de proposito (regra 3); o que nao pode e o
    codigo usar.
    """
    arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    for no in ast.walk(arvore):
        corpo = getattr(no, "body", None)
        if isinstance(corpo, list) and corpo:
            primeiro = corpo[0]
            if (
                isinstance(primeiro, ast.Expr)
                and isinstance(primeiro.value, ast.Constant)
                and isinstance(primeiro.value.value, str)
            ):
                corpo.pop(0)
    return ast.unparse(arvore)


def test_o_modulo_nao_importa_ferramenta_de_borrar_estourar_ou_ruidar():
    """Guarda estrutural: adicionar um efeito exige importar algo proibido.

    As metricas nao pegam tudo (JPEG de qualidade media apaga ruido injetado, por
    exemplo), entao o limite tambem e travado no nivel do import.
    """
    caminho = Path(inspect.getfile(modulo_humanizar))
    arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    importados: set[str] = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            importados.update(a.name.split(".")[0] for a in no.names)
        elif isinstance(no, ast.ImportFrom):
            importados.add((no.module or "").split(".")[0])
            importados.update(a.name for a in no.names)

    proibidos = {"ImageFilter", "ImageChops", "ImageEnhance", "random", "numpy", "cv2"}
    assert not (importados & proibidos), f"import proibido no passe minimo: {importados & proibidos}"

    codigo = _codigo_sem_docstring(caminho)
    for veneno in ("GaussianBlur", "UnsharpMask", "ImageChops", "ImageFilter", "gauss", "randbytes"):
        assert veneno not in codigo, f"passe deixou de ser minimo: usa {veneno}"


# --------------------------------------------------------------------------- #
# REGRA 3: se um dia entrar ruido aditivo, e com add(offset=-128)
# --------------------------------------------------------------------------- #


def test_docstring_ensina_a_forma_correta_de_somar_ruido():
    doc = modulo_humanizar.__doc__ or ""
    assert "ImageChops.add" in doc
    assert "offset=-128" in doc
    assert "subtract" in doc  # citado como o que NAO fazer


def test_subtract_cria_nevoa_leitosa_e_add_com_offset_nao():
    """A licao 5 do CLAUDE.md, medida.

    `subtract` satura em 0: a metade negativa do ruido some. Somar 128 depois
    levanta a imagem inteira e o preto vira cinza leitoso.
    """
    base = foto(size=(400, 500), amplitude=0, extremos=False)
    rnd = random.Random(11)
    tabela = [max(0, min(255, 128 + int((v - 128) * 0.25))) for v in range(256)]
    mapa = Image.frombytes("L", (400, 500), rnd.randbytes(400 * 500)).point(tabela)
    ruido = Image.merge("RGB", (mapa,) * 3)

    certo = ImageChops.add(base, ruido, offset=-128)
    errado = ImageChops.add(ImageChops.subtract(base, ruido), Image.new("RGB", (400, 500), (128,) * 3))

    media = lambda im: ImageStat.Stat(im.convert("L")).mean[0]  # noqa: E731

    # add com offset -128 preserva o brilho: e ruido de verdade, simetrico
    assert media(certo) == pytest.approx(media(base), abs=1.5)
    assert medir(certo).ruido > medir(base).ruido

    # subtract levanta tudo: nevoa
    assert media(errado) > media(base) + 15
    assert medir(errado).p1 > medir(base).p1 + 30
