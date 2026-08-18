"""Testes do perfil de camera medido.

Imagens 100% sinteticas (Pillow puro, seed fixa): a base real e gitignored e nao
viaja para o worktree, entao teste que depende dela nao roda em lugar nenhum.
"""

from __future__ import annotations

import random

import pytest
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat

from cie.metricas import (
    ALVO,
    BLOCO_RUIDO,
    TOLERANCIA,
    Metricas,
    fora_do_alvo,
    medir,
    relatar,
)

TAM = (720, 900)


def foto(
    size: tuple[int, int] = TAM,
    *,
    seed: int = 7,
    amplitude: int = 8,
    saturacao: float = 1.0,
    extremos: bool = False,
) -> Image.Image:
    """Foto sintetica: gradiente colorido + blocos + ruido fino de "sensor".

    `amplitude` = amplitude do ruido uniforme somado (0 = imagem lisa de render).
    `extremos` = crava um quadrado preto puro e um branco puro.
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
            if (x // 9 + y // 11) % 3 == 0:  # blocos de cor, para haver croma
                r, g, b = min(255, r + 55), max(0, g - 30), max(0, b - 25)
            px[x, y] = (r, g, b)
    im = pequena.resize(size, Image.BILINEAR)

    if amplitude:
        rnd = random.Random(seed)
        tabela = [max(0, min(255, 128 + int((v - 128) * amplitude / 128))) for v in range(256)]
        ruido = Image.frombytes("L", size, rnd.randbytes(w * h)).point(tabela)
        # Somar ruido com offset -128: ver licao 5 do CLAUDE.md.
        im = ImageChops.add(im, Image.merge("RGB", (ruido,) * 3), offset=-128)

    if extremos:
        desenho = ImageDraw.Draw(im)
        desenho.rectangle([w // 12, h // 12, w // 6, h // 8], fill=(0, 0, 0))
        desenho.rectangle([w - w // 6, h // 12, w - w // 12, h // 8], fill=(255, 255, 255))

    if saturacao != 1.0:
        matiz, sat, valor = im.convert("HSV").split()
        tab = [min(255, int(v * saturacao)) for v in range(256)]
        im = Image.merge("HSV", (matiz, sat.point(tab), valor)).convert("RGB")
    return im


def borrar_cantos(im: Image.Image, raio: float = 1.7) -> Image.Image:
    """Reproduz o desfoque radial de canto de `_ref-scripts/calibrar.py`."""
    w, h = im.size
    borrado = im.filter(ImageFilter.GaussianBlur(raio))
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
    return Image.composite(borrado, im, mascara.filter(ImageFilter.GaussianBlur(12)))


def ruido_quadro_inteiro(im: Image.Image, n: int = BLOCO_RUIDO) -> float:
    """A versao INGENUA da metrica de ruido: varre o quadro todo.

    E exatamente o que `calibrar.py` fazia, e o motivo de existir a regiao
    central em `cie.metricas`. Vive aqui so para o teste da regra 4 comparar.
    """
    cinza = im.convert("L")
    w, h = cinza.size
    passo = max(n, min(w, h) // 24)
    menor = 999.0
    for y in range(0, h - n + 1, passo):
        for x in range(0, w - n + 1, passo):
            menor = min(menor, ImageStat.Stat(cinza.crop((x, y, x + n, y + n))).stddev[0])
    return round(menor, 2)


# --------------------------------------------------------------------------- #
# contrato: as 7 metricas, os alvos medidos e as tolerancias
# --------------------------------------------------------------------------- #


def test_metricas_sao_exatamente_as_sete_do_perfil():
    assert [c for c in Metricas.__dataclass_fields__] == [
        "p1",
        "preto_pct",
        "estourado_pct",
        "saturacao",
        "cast_alta_rb",
        "nitidez_centro_borda",
        "ruido",
    ]


def test_alvo_e_o_perfil_medido_do_nosso_celular():
    # Numeros do CLAUDE.md. Se alguem "ajustar por gosto", este teste cai.
    assert ALVO.p1 == 14
    assert ALVO.preto_pct == 0.007
    assert ALVO.estourado_pct == 0.015
    assert ALVO.saturacao == 70.0
    assert ALVO.cast_alta_rb == 0.969
    assert ALVO.nitidez_centro_borda == 1.57
    assert ALVO.ruido == 0.42


def test_tolerancias_sao_as_medidas_e_ruido_nao_tem():
    assert TOLERANCIA == {
        "p1": 6,
        "preto_pct": 0.02,
        "estourado_pct": 0.02,
        "saturacao": 12.0,
        "cast_alta_rb": 0.04,
        "nitidez_centro_borda": 0.22,
    }
    # ruido e diagnostico, nao criterio: injetar ruido em pos foi o passo que
    # estragou calibrar.py.
    assert "ruido" not in TOLERANCIA


def test_metricas_e_imutavel():
    with pytest.raises(Exception):
        ALVO.saturacao = 120.0  # type: ignore[misc]


# --------------------------------------------------------------------------- #
# cada metrica mede o que promete
# --------------------------------------------------------------------------- #


def test_medir_devolve_as_sete_metricas():
    m = medir(foto())
    assert isinstance(m, Metricas)
    assert set(m.como_dict()) == set(Metricas.__dataclass_fields__)
    assert all(isinstance(v, (int, float)) for v in m.como_dict().values())


def test_medir_aceita_imagem_fora_de_rgb():
    cinza = foto().convert("L")
    m = medir(cinza)
    assert m.saturacao == 0.0  # sem croma nenhum


def test_preto_e_estourado_contam_so_os_extremos():
    limpa = medir(foto(extremos=False))
    crua = medir(foto(extremos=True))

    assert limpa.preto_pct == 0.0
    assert limpa.estourado_pct == 0.0
    assert crua.preto_pct > 0.1
    assert crua.estourado_pct > 0.1


def test_saturacao_acompanha_a_cor():
    neutra = medir(Image.new("RGB", TAM, (128, 128, 128))).saturacao
    lavada = medir(foto(saturacao=0.4)).saturacao
    vibrante = medir(foto(saturacao=2.0)).saturacao

    assert neutra == 0.0
    assert lavada < vibrante
    assert vibrante > 150


def test_cast_alta_rb_separa_luz_quente_de_luz_fria():
    def com_area_clara(cor: tuple[int, int, int]) -> float:
        im = foto(amplitude=4)
        ImageDraw.Draw(im).rectangle([120, 150, 560, 520], fill=cor)
        return medir(im).cast_alta_rb

    quente = com_area_clara((255, 240, 205))
    fria = com_area_clara((215, 235, 255))

    assert quente > 1.05  # dourado de IA
    assert fria < 0.95  # nossa base real puxa azul (alvo 0.969)


def test_cast_alta_rb_devolve_neutro_quando_nao_ha_altas():
    # Sem area clara suficiente a leitura seria ruido puro; a metrica nao pode
    # nem inventar numero nem dividir por zero.
    escura = Image.new("RGB", (200, 200), (12, 10, 14))
    assert medir(escura).cast_alta_rb == 1.0


def test_nitidez_centro_borda_sobe_quando_o_canto_amolece():
    nitida = foto()
    mole = borrar_cantos(nitida)

    assert medir(mole).nitidez_centro_borda > medir(nitida).nitidez_centro_borda + 0.1


def test_ruido_distingue_render_de_sensor():
    render = medir(foto(amplitude=0)).ruido
    sensor = medir(foto(amplitude=10)).ruido

    assert render == pytest.approx(0.0, abs=0.05)
    assert sensor > 1.0


# --------------------------------------------------------------------------- #
# REGRA 4: o ruido e medido no miolo, nunca no canto borrado
# --------------------------------------------------------------------------- #


def test_ruido_nao_pode_ser_medido_no_canto_borrado():
    """A armadilha que envenenou `calibrar.py`/`calibrar2.py`.

    Com desfoque de canto aplicado, o bloco 8x8 mais liso do QUADRO INTEIRO passa
    a ser o proprio canto borrado: a metrica desaba para perto de zero e o passe
    conclui que "falta ruido" numa imagem que nunca perdeu ruido nenhum.
    `cie.metricas` amostra so o miolo justamente para nao cair nisso.
    """
    nitida = foto(amplitude=10)
    mole = borrar_cantos(nitida)

    ingenuo_antes = ruido_quadro_inteiro(nitida)
    ingenuo_depois = ruido_quadro_inteiro(mole)
    nosso_antes = medir(nitida).ruido
    nosso_depois = medir(mole).ruido

    # a leitura ingenua desaba: e ela que mandava injetar ruido a mais
    assert ingenuo_depois < ingenuo_antes * 0.5

    # a nossa nao se move: o canto borrado nao entra na amostra
    assert nosso_depois == pytest.approx(nosso_antes, abs=0.15)
    assert nosso_depois > ingenuo_depois * 2


# --------------------------------------------------------------------------- #
# fora_do_alvo
# --------------------------------------------------------------------------- #


def _no_alvo(**troca: float) -> Metricas:
    valores = ALVO.como_dict() | troca
    return Metricas(**valores)  # type: ignore[arg-type]


def test_fora_do_alvo_vazio_quando_tudo_bate():
    assert fora_do_alvo(ALVO) == []


def test_fora_do_alvo_nomeia_so_quem_passou_da_tolerancia():
    m = _no_alvo(saturacao=40.0, cast_alta_rb=1.25, p1=18)
    # p1 18 esta a 4 do alvo 14, tolerancia 6: dentro, nao entra na lista.
    assert fora_do_alvo(m) == ["saturacao", "cast_alta_rb"]


def test_fora_do_alvo_devolve_na_ordem_do_perfil():
    m = _no_alvo(p1=40, saturacao=140.0, nitidez_centro_borda=0.6)
    assert fora_do_alvo(m) == ["p1", "saturacao", "nitidez_centro_borda"]


def test_o_limite_exato_da_tolerancia_conta_como_dentro():
    # Licao 7: metrica dentro da tolerancia NAO se toca. O limite e inclusivo.
    assert fora_do_alvo(_no_alvo(saturacao=ALVO.saturacao + TOLERANCIA["saturacao"])) == []
    assert fora_do_alvo(_no_alvo(saturacao=ALVO.saturacao + TOLERANCIA["saturacao"] + 0.1)) == [
        "saturacao"
    ]


def test_fora_do_alvo_nunca_julga_o_ruido():
    # Ruido absurdo, tudo o mais no alvo: continua "dentro". Nao ha tolerancia
    # para ruido porque nao existe correcao de ruido neste motor.
    assert fora_do_alvo(_no_alvo(ruido=12.0)) == []
    assert fora_do_alvo(_no_alvo(ruido=0.0)) == []


def test_relatar_marca_o_que_esta_fora():
    linha = relatar("depois", _no_alvo(saturacao=140.0))
    assert "saturacao=140.0 X" in linha
    assert "[1 fora]" in linha
    assert "p1=14 " in linha  # metrica dentro do alvo sai sem marca
