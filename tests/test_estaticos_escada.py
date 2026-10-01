import pytest

from instagram.estaticos.escada import (
    DEGRAUS, SINTOMAS, Resultado, esgotou, executar, rotear,
)


def test_cada_sintoma_aponta_para_um_degrau_que_existe():
    for sintoma, degrau in SINTOMAS.items():
        assert degrau in DEGRAUS, f"{sintoma} aponta para degrau {degrau} inexistente"


@pytest.mark.parametrize(
    "sintoma,degrau",
    [
        ("valor-inventado", 1),
        ("acento-perdido", 1),
        ("rotulo-generico", 2),
        ("fonte-ruim", 3),
        ("letra-corrompida", 4),
        ("erro-intermitente", 5),
        ("carimbo-variavel", 6),
        ("codigo-2d", 6),
    ],
)
def test_roteamento_e_deterministico(sintoma, degrau):
    assert rotear([sintoma]) == (degrau,)


def test_sintomas_distintos_acumulam_degraus_ordenados():
    assert rotear(["letra-corrompida", "valor-inventado"]) == (1, 4)


def test_sintoma_repetido_nao_duplica_degrau():
    assert rotear(["valor-inventado", "acento-perdido"]) == (1,)


def test_sintoma_desconhecido_levanta_em_vez_de_adivinhar():
    with pytest.raises(KeyError, match="nao-catalogado"):
        rotear(["nao-catalogado"])


def test_lista_vazia_nao_roteia_nada():
    assert rotear([]) == ()


def test_esgotou_e_verdade_quando_algum_sintoma_vai_direto_ao_degrau_6():
    assert esgotou(["carimbo-variavel"]) is True
    assert esgotou(["codigo-2d"]) is True
    assert esgotou(["valor-inventado"]) is False
    assert esgotou(["valor-inventado", "codigo-2d"]) is True


def test_passa_na_primeira_quando_nao_ha_falha():
    chamadas = []

    def gerar(correcoes):
        chamadas.append(correcoes)
        return "img1"

    r = executar(gerar=gerar, conferir=lambda img: [], compor=lambda s: "nunca")
    assert isinstance(r, Resultado)
    assert r.imagem == "img1"
    assert r.tentativas == 1
    assert r.degraus == ()
    assert r.composto is False
    assert chamadas == [()]


def test_corrige_e_passa_na_segunda():
    vistos = []

    def gerar(correcoes):
        vistos.append(correcoes)
        return f"img{len(vistos)}"

    def conferir(img):
        return ["valor-inventado"] if img == "img1" else []

    r = executar(gerar=gerar, conferir=conferir, compor=lambda s: "nunca")
    assert r.imagem == "img2"
    assert r.tentativas == 2
    assert r.degraus == ("soletrar",)
    assert r.composto is False
    assert vistos == [(), ("soletrar",)]


def test_respeita_o_teto_e_cai_para_composicao():
    """Gerador que SEMPRE erra: o laco nao pode rodar para sempre."""
    n = []

    def gerar(correcoes):
        n.append(correcoes)
        return "ruim"

    r = executar(
        gerar=gerar,
        conferir=lambda img: ["valor-inventado"],
        compor=lambda sintomas: "composta",
        teto=3,
    )
    assert len(n) == 3, "gerou mais vezes que o teto"
    assert r.imagem == "composta"
    assert r.composto is True
    assert r.tentativas == 3


def test_sintoma_de_degrau_6_vai_direto_a_composicao_sem_gastar_rodada():
    """Carimbo de lote nao se conserta por prompt. Licao 22."""
    n = []

    def gerar(correcoes):
        n.append(correcoes)
        return "img"

    r = executar(
        gerar=gerar,
        conferir=lambda img: ["carimbo-variavel"],
        compor=lambda sintomas: "composta",
        teto=3,
    )
    assert len(n) == 1, "gastou rodada num sintoma que a escada manda compor"
    assert r.composto is True


def test_degraus_acumulados_aparecem_no_resultado():
    seq = [["letra-corrompida"], ["valor-inventado"], []]

    def conferir(img):
        return seq.pop(0)

    r = executar(gerar=lambda c: "i", conferir=conferir, compor=lambda s: "c")
    assert r.degraus == ("aumentar-no-quadro", "soletrar")
    assert r.composto is False
