"""Parser do JSON do Instagram. Nenhum teste aqui toca a rede."""

from __future__ import annotations

import pytest

from cie.errors import InstagramFormatError
from cie.scrape.parser import parse_media


def _candidatos(*tamanhos):
    return {
        "candidates": [
            {"url": f"https://cdn.example/{w}x{h}.jpg", "width": w, "height": h}
            for w, h in tamanhos
        ]
    }


def _imagem():
    return {
        "code": "C1a2b3c",
        "taken_at": 1786000000,
        "media_type": 1,
        "user": {"username": "cafecanastra"},
        "caption": {"text": "colheita na fazenda"},
        "image_versions2": _candidatos((640, 800), (1080, 1350)),
    }


def test_imagem_simples_vira_um_item():
    itens = parse_media(_imagem())
    assert len(itens) == 1
    item = itens[0]
    assert item.shortcode == "C1a2b3c"
    assert item.owner_handle == "cafecanastra"
    assert item.caption == "colheita na fazenda"
    assert item.carousel_index == 1
    assert item.is_video is False
    assert item.post_url == "https://www.instagram.com/p/C1a2b3c/"


def test_escolhe_sempre_o_maior_candidato():
    # 640x800 vem primeiro na lista; queremos 1080x1350 mesmo assim.
    item = parse_media(_imagem())[0]
    assert item.width == 1080
    assert item.height == 1350
    assert item.display_url == "https://cdn.example/1080x1350.jpg"


def test_taken_at_vira_datetime_utc():
    item = parse_media(_imagem())[0]
    assert item.taken_at is not None
    assert item.taken_at.year == 2026


def test_carrossel_de_tres_vira_tres_itens_indexados():
    media = {
        "code": "C9z9z9z",
        "taken_at": 1786000000,
        "media_type": 8,
        "user": {"username": "cafecanastra"},
        "caption": {"text": "sequencia"},
        "carousel_media": [
            {"media_type": 1, "image_versions2": _candidatos((1080, 1080))},
            {"media_type": 1, "image_versions2": _candidatos((1080, 1080))},
            {"media_type": 1, "image_versions2": _candidatos((1080, 1080))},
        ],
    }
    itens = parse_media(media)
    assert [i.carousel_index for i in itens] == [1, 2, 3]
    assert all(i.shortcode == "C9z9z9z" for i in itens)
    assert all(i.caption == "sequencia" for i in itens)


def test_video_e_marcado_mas_nao_derruba_o_parser():
    media = _imagem() | {"media_type": 2}
    item = parse_media(media)[0]
    assert item.is_video is True


def test_video_sem_candidato_de_imagem_nao_levanta_erro():
    media = {
        "code": "Cvid",
        "taken_at": 1786000000,
        "media_type": 2,
        "user": {"username": "x"},
    }
    item = parse_media(media)[0]
    assert item.is_video is True
    assert item.display_url == ""


def test_carrossel_misto_marca_so_o_video():
    media = {
        "code": "Cmix",
        "media_type": 8,
        "carousel_media": [
            {"media_type": 1, "image_versions2": _candidatos((1080, 1080))},
            {"media_type": 2, "image_versions2": _candidatos((1080, 1080))},
        ],
    }
    itens = parse_media(media)
    assert [i.is_video for i in itens] == [False, True]


def test_legenda_nula_vira_string_vazia():
    media = _imagem() | {"caption": None}
    assert parse_media(media)[0].caption == ""


def test_sem_taken_at_o_parser_nao_inventa_data():
    media = {k: v for k, v in _imagem().items() if k != "taken_at"}
    assert parse_media(media)[0].taken_at is None


def test_handle_cai_para_o_fallback_quando_ausente():
    media = {k: v for k, v in _imagem().items() if k != "user"}
    item = parse_media(media, owner_fallback="cafecanastra")[0]
    assert item.owner_handle == "cafecanastra"


def test_media_sem_code_da_erro_legivel_e_nao_keyerror():
    media = {k: v for k, v in _imagem().items() if k != "code"}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo == "code"
    assert "code" in str(exc.value)


def test_imagem_sem_candidato_da_erro_legivel():
    media = {k: v for k, v in _imagem().items() if k != "image_versions2"}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo == "image_versions2"


# --- Regressao: formato inesperado nunca pode escapar como AttributeError,
# ValueError ou ValidationError do Pydantic. So `InstagramFormatError` sai
# daqui, com o nome do campo que veio torto.


def test_carousel_media_com_string_da_erro_legivel():
    media = _imagem() | {"media_type": 8, "carousel_media": ["nao-e-um-objeto"]}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo == "carousel_media[0]"


def test_carousel_media_com_none_da_erro_legivel():
    media = _imagem() | {"media_type": 8, "carousel_media": [None]}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo  # aponta para algum campo, nunca AttributeError nu


def test_caption_string_da_erro_legivel():
    media = _imagem() | {"caption": "nao-e-um-objeto"}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo == "caption"


def test_caption_lista_da_erro_legivel():
    media = _imagem() | {"caption": ["nao-e-um-objeto"]}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo == "caption"


def test_user_string_da_erro_legivel():
    media = _imagem() | {"user": "nao-e-um-objeto"}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo == "user"


def test_user_lista_da_erro_legivel():
    media = _imagem() | {"user": ["nao-e-um-objeto"]}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo == "user"


def test_code_inteiro_da_erro_legivel():
    media = _imagem() | {"code": 12345}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo == "code"


def test_code_lista_da_erro_legivel():
    media = _imagem() | {"code": ["a", "b"]}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo == "code"


def test_candidates_string_da_erro_legivel():
    media = _imagem() | {"image_versions2": {"candidates": "nao-e-uma-lista"}}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo == "image_versions2.candidates"


def test_width_texto_degrada_para_zero_em_vez_de_levantar():
    media = _imagem() | {
        "image_versions2": {
            "candidates": [
                {"url": "https://cdn.example/x.jpg", "width": "abc", "height": 100}
            ]
        }
    }
    item = parse_media(media)[0]
    assert item.width == 0
    assert item.height == 100


def test_media_malformados_nunca_vazam_excecao_fora_do_contrato():
    """Cinturao e suspensorio: qualquer entrada torta so pode terminar de dois
    jeitos - `InstagramFormatError` ou um resultado normal. Nunca outra coisa.
    """
    entradas_malformadas = [
        _imagem() | {"media_type": 8, "carousel_media": ["nao-e-um-objeto"]},
        _imagem() | {"media_type": 8, "carousel_media": [None]},
        _imagem() | {"caption": "nao-e-um-objeto"},
        _imagem() | {"caption": ["nao-e-um-objeto"]},
        _imagem() | {"user": "nao-e-um-objeto"},
        _imagem() | {"user": ["nao-e-um-objeto"]},
        _imagem() | {"code": 12345},
        _imagem() | {"code": ["a", "b"]},
        _imagem() | {"image_versions2": {"candidates": "nao-e-uma-lista"}},
        _imagem()
        | {
            "image_versions2": {
                "candidates": [
                    {"url": "https://cdn.example/x.jpg", "width": "abc", "height": 100}
                ]
            }
        },
    ]
    for media in entradas_malformadas:
        try:
            parse_media(media)
        except InstagramFormatError:
            pass
        except Exception as e:
            pytest.fail(
                f"parse_media vazou {type(e).__name__} em vez de "
                f"InstagramFormatError para entrada {media!r}: {e}"
            )
