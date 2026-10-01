from pathlib import Path

import pytest

from instagram.estaticos.catalogo import (
    MOLDES, PECAS, Dado, DeclaracaoInvalida, Molde, Peca, validar,
)


def test_molde_cartao_produto_existe_e_e_4x5():
    m = MOLDES["cartao-produto"]
    assert isinstance(m, Molde)
    assert (m.largura, m.altura) == (1080, 1350)
    assert m.largura * 5 == m.altura * 4


def test_molde_declara_os_campos_que_o_codigo_desenha():
    assert MOLDES["cartao-produto"].campos == ("preco", "altitude", "local")


def test_existe_uma_peca_e_ela_e_frozen():
    assert len(PECAS) >= 1
    p = PECAS[0]
    assert isinstance(p, Peca)
    with pytest.raises(Exception):
        p.slug = "outro"


def test_dado_exige_origem_sem_default():
    with pytest.raises(TypeError):
        Dado("8,0")


def test_peca_declara_strings_impressas_e_dados_com_origem():
    p = PECAS[0]
    assert p.strings_impressas
    assert set(p.dados) == set(MOLDES[p.molde].campos)
    for chave, d in p.dados.items():
        assert isinstance(d, Dado)
        assert d.origem.strip(), f"{chave} sem origem declarada"


def test_fonte_da_peca_e_caminho_absoluto_existente():
    assert isinstance(PECAS[0].fonte, Path)
    assert PECAS[0].fonte.is_absolute()


def _peca_boa(tmp_path):
    fonte = tmp_path / "f.png"
    fonte.write_bytes(b"x")
    return Peca(
        slug="s", molde="cartao-produto", fonte=fonte,
        strings_impressas=("CANASTRA",),
        dados={
            "preco": Dado("R$ 1,00", "fonte x"),
            "altitude": Dado("1.250 m", "fonte y"),
            "local": Dado("Medeiros, MG", "fonte y"),
        },
        gerar_fundo=False,
    )


def test_validar_aceita_peca_completa(tmp_path):
    assert validar([_peca_boa(tmp_path)]) == []


def test_validar_recusa_origem_vazia(tmp_path):
    p = _peca_boa(tmp_path)
    ruim = Peca(**{**p.__dict__, "dados": {**p.dados, "preco": Dado("R$ 1,00", "  ")}})
    problemas = validar([ruim])
    assert any("origem" in x and "preco" in x for x in problemas)


def test_validar_recusa_fonte_ausente(tmp_path):
    p = _peca_boa(tmp_path)
    ruim = Peca(**{**p.__dict__, "fonte": tmp_path / "nao-existe.png"})
    assert any("fonte" in x for x in validar([ruim]))


def test_validar_recusa_campo_fora_do_molde(tmp_path):
    p = _peca_boa(tmp_path)
    ruim = Peca(**{**p.__dict__, "dados": {**p.dados, "intruso": Dado("x", "y")}})
    assert any("intruso" in x for x in validar([ruim]))


def test_validar_recusa_campo_do_molde_que_falta(tmp_path):
    p = _peca_boa(tmp_path)
    sem_preco = {k: v for k, v in p.dados.items() if k != "preco"}
    assert any("preco" in x for x in validar([Peca(**{**p.__dict__, "dados": sem_preco})]))


def test_validar_recusa_strings_impressas_vazia(tmp_path):
    p = _peca_boa(tmp_path)
    assert any("strings_impressas" in x for x in validar([Peca(**{**p.__dict__, "strings_impressas": ()})]))


def test_validar_recusa_molde_desconhecido(tmp_path):
    p = _peca_boa(tmp_path)
    assert any("molde" in x for x in validar([Peca(**{**p.__dict__, "molde": "inventado"})]))


def test_o_catalogo_de_verdade_e_valido():
    """O portao que importa: PECAS declarado no repositorio passa."""
    assert validar(PECAS) == []
