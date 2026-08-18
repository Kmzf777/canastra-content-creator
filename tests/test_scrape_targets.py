"""Traducao de link em alvo. Nenhum teste aqui toca a rede."""

from __future__ import annotations

import dataclasses

import pytest

from cie.errors import ScrapeError
from cie.scrape.targets import (
    HashtagTarget,
    PostTarget,
    ProfileTarget,
    parse_target,
    shortcode_to_media_id,
)


@pytest.mark.parametrize(
    "entrada",
    [
        "https://www.instagram.com/cafecanastra/",
        "https://instagram.com/cafecanastra",
        "instagram.com/cafecanastra/",
        "www.instagram.com/cafecanastra",
        "@cafecanastra",
        "cafecanastra",
        "  https://www.instagram.com/cafecanastra/?hl=pt-br  ",
    ],
)
def test_perfil_em_todas_as_formas(entrada):
    alvo = parse_target(entrada)
    assert alvo == ProfileTarget(handle="cafecanastra")
    assert alvo.slug == "cafecanastra"
    assert alvo.kind == "profile"


@pytest.mark.parametrize(
    "entrada",
    [
        "https://www.instagram.com/p/C1a2b3cXyZ/",
        "https://www.instagram.com/p/C1a2b3cXyZ/?img_index=2",
        "instagram.com/p/C1a2b3cXyZ",
    ],
)
def test_post_em_todas_as_formas(entrada):
    alvo = parse_target(entrada)
    assert alvo == PostTarget(shortcode="C1a2b3cXyZ")
    assert alvo.slug == "post-C1a2b3cXyZ"
    assert alvo.kind == "post"


@pytest.mark.parametrize(
    "entrada",
    [
        "https://www.instagram.com/explore/tags/cafeespecial/",
        "instagram.com/explore/tags/cafeespecial",
        "#cafeespecial",
    ],
)
def test_hashtag_em_todas_as_formas(entrada):
    alvo = parse_target(entrada)
    assert alvo == HashtagTarget(tag="cafeespecial")
    assert alvo.slug == "tag-cafeespecial"
    assert alvo.kind == "hashtag"


def test_perfil_com_barra_final_e_query_nao_vira_handle_sujo():
    alvo = parse_target("https://www.instagram.com/cafe.canastra_1/?utm_source=x")
    assert alvo == ProfileTarget(handle="cafe.canastra_1")


def test_reel_e_recusado_com_explicacao():
    with pytest.raises(ScrapeError) as exc:
        parse_target("https://www.instagram.com/reel/C1a2b3cXyZ/")
    mensagem = str(exc.value).lower()
    assert "reel" in mensagem
    assert "video" in mensagem


def test_stories_e_recusado():
    with pytest.raises(ScrapeError):
        parse_target("https://www.instagram.com/stories/cafecanastra/123/")


def test_dominio_de_fora_e_recusado():
    with pytest.raises(ScrapeError) as exc:
        parse_target("https://example.com/cafecanastra")
    assert "instagram" in str(exc.value).lower()


def test_entrada_vazia_e_recusada():
    with pytest.raises(ScrapeError):
        parse_target("   ")


def test_url_do_instagram_sem_caminho_e_recusada():
    with pytest.raises(ScrapeError):
        parse_target("https://www.instagram.com/")


# shortcode -> media_id e base64 posicional com o alfabeto do Instagram.
@pytest.mark.parametrize(
    "shortcode,esperado",
    [
        ("B", 1),
        ("BA", 64),
        ("CBa", 8282),
    ],
)
def test_shortcode_vira_media_id(shortcode, esperado):
    assert shortcode_to_media_id(shortcode) == esperado


def test_shortcode_com_caractere_invalido_e_recusado():
    with pytest.raises(ScrapeError):
        shortcode_to_media_id("abc!")


def test_shortcode_alphabet_tail():
    # Ultimos dois caracteres do alfabeto posicional do Instagram.
    assert shortcode_to_media_id("_") == 63
    assert shortcode_to_media_id("-") == 62


def test_shortcode_vazio_e_recusado():
    with pytest.raises(ScrapeError):
        shortcode_to_media_id("")


# --- Fix 1: urlparse nao pode vazar ValueError bruto ---------------------


@pytest.mark.parametrize(
    "entrada",
    [
        "[instagram.com/cafecanastra",
        "[cafecanastra]/",
        "https://insta[gram.com/x",
        "]abc/",
    ],
)
def test_link_malformado_vira_scrape_error_e_nao_value_error(entrada):
    with pytest.raises(ScrapeError):
        parse_target(entrada)


# --- Fix 2: handle solto com ponto e aceito; host puro e recusado --------


def test_handle_solto_com_ponto_e_aceito():
    alvo = parse_target("cafe.canastra")
    assert alvo == ProfileTarget(handle="cafe.canastra")


@pytest.mark.parametrize("entrada", ["instagram.com", "www.instagram.com", "instagr.am"])
def test_host_puro_sem_caminho_e_recusado(entrada):
    with pytest.raises(ScrapeError):
        parse_target(entrada)


# --- Fix 3: handle com ponto duplo/nas pontas escapa do diretorio --------


@pytest.mark.parametrize("entrada", ["@..", "@.", "@.abc", "@abc.", "@a..b"])
def test_handle_com_pontos_invalidos_e_recusado(entrada):
    with pytest.raises(ScrapeError):
        parse_target(entrada)


def test_handle_com_ponto_interno_valido_continua_aceito():
    alvo = parse_target("@cafe.canastra_1")
    assert alvo == ProfileTarget(handle="cafe.canastra_1")


# --- Fix 4: hashtag nao pode ter caracteres ilegais no Windows -----------


@pytest.mark.parametrize("entrada", ["#a:b", "#a*b", "#.."])
def test_hashtag_com_caractere_ilegal_e_recusada(entrada):
    with pytest.raises(ScrapeError):
        parse_target(entrada)


def test_hashtag_valida_continua_aceita():
    alvo = parse_target("#cafeespecial")
    assert alvo == HashtagTarget(tag="cafeespecial")


# --- Fix 5: shortcode de post e validado contra o alfabeto ---------------


@pytest.mark.parametrize(
    "entrada",
    [
        "https://instagram.com/p/../../etc/",
        "https://instagram.com/p/abc!def/",
    ],
)
def test_shortcode_de_post_e_validado_no_parse(entrada):
    with pytest.raises(ScrapeError):
        parse_target(entrada)


# --- Fix 6: kind e ClassVar, nao campo do dataclass -----------------------


def test_kind_nao_e_campo_do_dataclass():
    nomes = {campo.name for campo in dataclasses.fields(ProfileTarget)}
    assert nomes == {"handle"}


# --- Fix 7: esquema nao-http e recusado; URL protocol-relative e aceita --


@pytest.mark.parametrize(
    "entrada",
    ["ftp://instagram.com/x", "javascript://instagram.com/x"],
)
def test_esquema_nao_http_e_recusado(entrada):
    with pytest.raises(ScrapeError):
        parse_target(entrada)


def test_url_protocol_relative_e_aceita():
    alvo = parse_target("//instagram.com/cafecanastra")
    assert alvo == ProfileTarget(handle="cafecanastra")
