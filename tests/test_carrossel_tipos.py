"""O contrato: taxonomia, orcamento de caracteres e ritmo de fundo."""
from pathlib import Path

import pytest
from PIL import Image

from instagram.carrossel import tipos
from instagram.carrossel.molde import MAX_FUNDO_SEGUIDO


@pytest.fixture
def foto(tmp_path) -> Path:
    p = tmp_path / "f.png"
    Image.new("RGB", (8, 10), "black").save(p)
    return p


def _deck(slides, slug="d"):
    return tipos.Deck(slug=slug, slides=tuple(slides))


def _minimo(foto):
    return [
        tipos.Slide("capa", "foto", {"manchete": "Oi"}, foto),
        tipos.Slide("prova", "creme",
                    {"afirmacao": "a", "evidencia": "b", "fonte": "c"}),
        tipos.Slide("fecho", "terra", {"manchete": "Tchau"}),
    ]


def test_dez_tipos_declarados():
    assert len(tipos.TIPOS) == 10
    assert "prova" in tipos.TIPOS, "o tipo nosso, que exige fonte"


def test_deck_minimo_valido(foto):
    assert tipos.validar(_deck(_minimo(foto))) == []


def test_prova_sem_fonte_reprova(foto):
    s = _minimo(foto)
    s[1] = tipos.Slide("prova", "creme", {"afirmacao": "a", "evidencia": "b"})
    problemas = tipos.validar(_deck(s))
    assert any("fonte" in x for x in problemas)


def test_campo_acima_do_teto_reprova_com_numero(foto):
    s = _minimo(foto)
    s[0] = tipos.Slide("capa", "foto", {"manchete": "x" * 61}, foto)
    problemas = tipos.validar(_deck(s))
    assert any("61 caracteres" in x and "60" in x for x in problemas)


def test_campo_desconhecido_reprova(foto):
    s = _minimo(foto)
    s[0] = tipos.Slide("capa", "foto", {"manchete": "Oi", "inventado": "x"}, foto)
    assert any("inventado" in x for x in tipos.validar(_deck(s)))


def test_fundo_foto_exige_foto():
    s = [tipos.Slide("capa", "foto", {"manchete": "Oi"}),
         tipos.Slide("prova", "creme", {"afirmacao": "a", "evidencia": "b", "fonte": "c"}),
         tipos.Slide("fecho", "terra", {"manchete": "T"})]
    assert any("exige o campo foto" in x for x in tipos.validar(_deck(s)))


def test_fundo_sem_foto_recusa_foto(foto):
    s = _minimo(foto)
    s[1] = tipos.Slide("prova", "creme",
                       {"afirmacao": "a", "evidencia": "b", "fonte": "c"}, foto)
    assert any("nao aceita foto" in x for x in tipos.validar(_deck(s)))


def test_tres_fundos_seguidos_reprovam(foto):
    s = [tipos.Slide("capa", "foto", {"manchete": "Oi"}, foto),
         tipos.Slide("produto", "foto", {"nome": "A", "descritor": "d"}, foto),
         tipos.Slide("produto", "foto", {"nome": "B", "descritor": "d"}, foto),
         tipos.Slide("fecho", "terra", {"manchete": "T"})]
    problemas = tipos.validar(_deck(s))
    assert any(f"{MAX_FUNDO_SEGUIDO} slides seguidos" in x for x in problemas)


def test_capa_e_fecho_obrigatorios_nas_pontas(foto):
    s = [tipos.Slide("produto", "foto", {"nome": "A", "descritor": "d"}, foto),
         tipos.Slide("prova", "creme", {"afirmacao": "a", "evidencia": "b", "fonte": "c"}),
         tipos.Slide("produto", "foto", {"nome": "B", "descritor": "d"}, foto)]
    problemas = tipos.validar(_deck(s))
    assert any("primeiro slide" in x for x in problemas)
    assert any("ultimo slide" in x for x in problemas)


def test_colecao_fora_do_intervalo(foto):
    s = _minimo(foto)
    s.insert(1, tipos.Slide("lista", "terra", {"titulo": "T", "itens": ["um"]}))
    assert any("aceita de 2 a 6" in x for x in tipos.validar(_deck(s)))


def test_exigir_valido_levanta(foto):
    with pytest.raises(tipos.DeclaracaoInvalida):
        tipos.exigir_valido(_deck([]))
