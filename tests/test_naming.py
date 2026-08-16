from __future__ import annotations

from pathlib import Path

import pytest

from cie.enums import Location, Pillar, Sku
from cie.naming import infer, location_from_gps, parse_asset_name


def test_parse_canonical_name():
    parsed = parse_asset_name("CANASTRA_3_TORREFACAO_TAMBOR_007.jpg")

    assert parsed.matched
    assert parsed.pillar is Pillar.P3
    assert parsed.location is Location.TORREFACAO_UBERLANDIA
    assert parsed.subject == "TAMBOR"
    assert parsed.sequence == 7


def test_parse_name_with_accents_and_multiword_subject():
    parsed = parse_asset_name("CANASTRA_1_FAZENDA_TERREIRO_SECAGEM_012.JPG")

    assert parsed.pillar is Pillar.P1
    assert parsed.location is Location.FAZENDA_MEDEIROS
    assert parsed.subject == "TERREIRO_SECAGEM"
    assert parsed.sequence == 12


def test_parse_rejects_non_conventional_name():
    assert parse_asset_name("IMG_4821.jpg").matched is False
    assert parse_asset_name("foto da fazenda.jpg").matched is False


@pytest.mark.parametrize(
    "token,expected",
    [("PRODUCT", Pillar.PRODUCT), ("PEOPLE", Pillar.PEOPLE), ("2", Pillar.P2)],
)
def test_parse_alternative_pillars(token, expected):
    parsed = parse_asset_name(f"CANASTRA_{token}_ESTUDIO_PACOTE_001.png")
    assert parsed.pillar is expected


def test_infer_from_convention_does_not_need_review():
    result = infer(Path("/base/CANASTRA_2_FAZENDA_PAINEIS_003.jpg"), root=Path("/base"))

    assert result.pillar is Pillar.P2
    assert result.location is Location.FAZENDA_MEDEIROS
    assert result.needs_review is False
    assert "paineis" in result.subject_tags


def test_infer_falls_back_to_folder_tokens():
    result = infer(
        Path("/base/torrefacao/cupping/IMG_0031.jpg"),
        root=Path("/base"),
    )

    assert result.pillar is Pillar.P3
    assert result.location is Location.TORREFACAO_UBERLANDIA
    assert result.needs_review is False


def test_infer_marks_needs_review_when_it_cannot_tell():
    result = infer(Path("/base/diversos/IMG_0099.jpg"), root=Path("/base"))

    assert result.pillar is None
    assert result.location is None
    assert result.needs_review is True
    assert any("nao inferido" in reason for reason in result.reasons)


def test_infer_uses_gps_when_name_is_silent():
    result = infer(
        Path("/base/sem_padrao/DSC_1000.jpg"),
        root=Path("/base"),
        gps_lat=-19.99,
        gps_lon=-46.02,
    )

    assert result.location is Location.FAZENDA_MEDEIROS


def test_gps_conflict_with_name_forces_review():
    result = infer(
        Path("/base/CANASTRA_1_FAZENDA_COLHEITA_001.jpg"),
        root=Path("/base"),
        gps_lat=-18.92,
        gps_lon=-48.28,
    )

    assert result.location is Location.FAZENDA_MEDEIROS  # o nome (curadoria humana) vence
    assert result.needs_review is True
    assert any(reason.startswith("conflito") for reason in result.reasons)


def test_gps_outside_known_anchors_is_outro():
    assert location_from_gps(-23.55, -46.63) is Location.OUTRO
    assert location_from_gps(None, None) is None


def test_infer_detects_sku():
    result = infer(Path("/base/CANASTRA_PRODUCT_ESTUDIO_GEISHA_PACOTE_004.jpg"), root=Path("/base"))

    assert result.sku is Sku.GEISHA
    assert result.pillar is Pillar.PRODUCT
