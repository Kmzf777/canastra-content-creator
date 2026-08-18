"""Envelope de colheita -> HarvestBatch. Fixtures, nenhuma rede."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cie.errors import InstagramFormatError
from cie.scrape.parser import parse_envelope

FIXTURES = Path(__file__).parent / "fixtures" / "scrape"


def _carrega(nome: str) -> dict:
    return json.loads((FIXTURES / f"{nome}.json").read_text(encoding="utf-8"))


def test_perfil_junta_todas_as_paginas():
    lote = parse_envelope(_carrega("perfil"))
    assert lote.target_kind == "profile"
    assert lote.target_slug == "cafecanastra"
    # AAA111 (1) + BBB222 carrossel (2) + CCC333 video (1) = 4 itens
    assert len(lote.items) == 4
    assert [i.shortcode for i in lote.items] == ["AAA111", "BBB222", "BBB222", "CCC333"]


def test_perfil_separa_video_do_que_da_para_baixar():
    lote = parse_envelope(_carrega("perfil"))
    assert len(lote.images) == 3
    assert all(not i.is_video for i in lote.images)


def test_perfil_preserva_o_carimbo_de_colheita():
    lote = parse_envelope(_carrega("perfil"))
    assert lote.harvested_at.year == 2026
    assert lote.harvested_at.month == 8


def test_post_carrossel_vira_tres_itens():
    lote = parse_envelope(_carrega("post-carrossel"))
    assert lote.target_kind == "post"
    assert len(lote.items) == 3
    assert [i.carousel_index for i in lote.items] == [1, 2, 3]
    assert lote.items[0].extension == ".webp"


def test_hashtag_le_top_e_recent():
    lote = parse_envelope(_carrega("hashtag"))
    assert lote.target_kind == "hashtag"
    assert lote.target_slug == "tag-cafeespecial"
    assert {i.shortcode for i in lote.items} == {"EEE555", "FFF666"}


def test_hashtag_ignora_secao_de_clips():
    # A secao one_by_two_item/clips e video em formato diferente; nao entra.
    lote = parse_envelope(_carrega("hashtag"))
    assert "IGNORAR" not in {i.shortcode for i in lote.items}


def test_hashtag_usa_o_dono_de_cada_post_nao_o_alvo():
    lote = parse_envelope(_carrega("hashtag"))
    assert {i.owner_handle for i in lote.items} == {"outro_perfil", "mais_um"}


def test_envelope_sem_target_da_erro_legivel():
    with pytest.raises(InstagramFormatError) as exc:
        parse_envelope({"pages": []})
    assert exc.value.campo == "target"


def test_envelope_com_kind_desconhecido_da_erro_legivel():
    envelope = {
        "target": {"kind": "marciano", "slug": "x"},
        "harvested_at": "2026-08-18T00:00:00+00:00",
        "pages": [],
    }
    with pytest.raises(InstagramFormatError) as exc:
        parse_envelope(envelope)
    assert "marciano" in str(exc.value)


def test_envelope_sem_paginas_vira_lote_vazio_e_nao_erro():
    envelope = {
        "target": {"kind": "profile", "slug": "vazio", "handle": "vazio"},
        "harvested_at": "2026-08-18T00:00:00+00:00",
        "pages": [],
    }
    lote = parse_envelope(envelope)
    assert lote.items == []
