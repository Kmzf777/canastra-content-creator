import pytest

from instagram.estaticos.catalogo import PECAS
from instagram.estaticos.prompt import CORRECOES, montar


def test_toda_string_declarada_aparece_no_prompt():
    p = PECAS[0]
    texto = montar(p)
    for s in p.strings_impressas:
        assert s in texto, f"{s} declarada e ausente do prompt"


def test_dado_do_codigo_nao_entra_no_prompt():
    texto = montar(PECAS[0])
    assert "31,70" not in texto
    assert "1.250" not in texto


def test_soletracao_separa_por_hifen_quando_pedida():
    texto = montar(PECAS[0], correcoes=("soletrar",))
    assert "S-C-A" in texto or "C-A-N-A-S-T-R-A" in texto


def test_nomear_operacao_abre_o_prompt_com_ordem_de_edicao():
    texto = montar(PECAS[0], correcoes=("nomear-operacao",))
    assert texto.startswith("EDIT THE PROVIDED PHOTOGRAPH")
    assert "KEEP THE PACKAGE PIXEL-FOR-PIXEL IDENTICAL" in texto


def test_aumentar_no_quadro_declara_ocupacao_minima():
    texto = montar(PECAS[0], correcoes=("aumentar-no-quadro",))
    assert "at least 60%" in texto


def test_correcao_desconhecida_levanta():
    with pytest.raises(ValueError, match="inventada"):
        montar(PECAS[0], correcoes=("inventada",))


def test_correcoes_conhecidas_sao_as_da_escada():
    assert CORRECOES == (
        "soletrar",
        "nomear-operacao",
        "ancora-familia",
        "aumentar-no-quadro",
    )
