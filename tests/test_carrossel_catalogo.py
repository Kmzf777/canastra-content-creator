"""O deck real declarado tem que passar no contrato."""
from instagram.carrossel import catalogo, tipos


def test_deck_declarado_e_valido():
    for d in catalogo.DECKS:
        assert tipos.validar(d) == [], f"{d.slug}: {tipos.validar(d)}"


def test_usa_pelo_menos_quatro_tipos():
    d = catalogo.CAPSULAS
    assert len({s.tipo for s in d.slides}) >= 4


def test_toda_foto_declarada_existe():
    for d in catalogo.DECKS:
        for i, s in enumerate(d.slides, 1):
            if s.foto is not None:
                assert s.foto.exists(), f"{d.slug} slide {i}: {s.foto}"


def test_prova_tem_fonte():
    for d in catalogo.DECKS:
        for s in d.slides:
            if s.tipo == "prova":
                assert s.dados.get("fonte", "").strip()


def test_por_slug():
    assert catalogo.por_slug("capsulas-qual-e-a-sua") is catalogo.CAPSULAS
    assert catalogo.por_slug("nao-existe") is None
