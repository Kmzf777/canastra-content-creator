from __future__ import annotations

import pytest

from cie import repository
from cie.enums import Location, Pillar, Sku
from cie.models import Asset


def _asset(**overrides) -> Asset:
    data = {
        "path": "/base/CANASTRA_1_FAZENDA_COLHEITA_001.jpg",
        "sha256": "a" * 64,
        "width": 2400,
        "height": 1600,
        "pillar": Pillar.P1,
        "location": Location.FAZENDA_MEDEIROS,
        "quality_score": 82,
        "is_reference_grade": True,
    }
    data.update(overrides)
    return Asset(**data)


def test_insert_and_roundtrip(conn):
    asset_id = repository.insert_asset(conn, _asset(subject_tags=["colheita", "maos"]))
    loaded = repository.get_asset(conn, asset_id)

    assert loaded is not None
    assert loaded.pillar is Pillar.P1
    assert loaded.subject_tags == ["colheita", "maos"]
    assert loaded.has_identifiable_person is True
    assert loaded.consent_on_file is False


def test_filters(conn):
    repository.insert_asset(conn, _asset())
    repository.insert_asset(
        conn,
        _asset(
            path="/base/CANASTRA_PRODUCT_ESTUDIO_GEISHA_001.jpg",
            sha256="b" * 64,
            pillar=Pillar.PRODUCT,
            location=Location.ESTUDIO,
            sku=Sku.GEISHA,
            quality_score=91,
            is_reference_grade=False,
        ),
    )

    assert len(repository.list_assets(conn, pillar=Pillar.P1)) == 1
    assert len(repository.list_assets(conn, sku=Sku.GEISHA)) == 1
    assert len(repository.list_assets(conn, reference_grade=True)) == 1
    assert len(repository.list_assets(conn, ids=[])) == 0
    # Ordena por quality_score decrescente.
    assert [a.quality_score for a in repository.list_assets(conn)] == [91, 82]


def test_curation_updates_policy_fields(conn):
    asset_id = repository.insert_asset(conn, _asset())
    repository.update_asset_curation(
        conn, asset_id, has_identifiable_person=False, needs_review=False
    )
    loaded = repository.get_asset(conn, asset_id)

    assert loaded.has_identifiable_person is False
    assert loaded.needs_review is False
    assert loaded.is_usable_as_reference is True


def test_curation_rejects_machine_owned_fields(conn):
    asset_id = repository.insert_asset(conn, _asset())

    with pytest.raises(ValueError, match="nao editaveis"):
        repository.update_asset_curation(conn, asset_id, sha256="c" * 64)


def test_reference_usability_requires_consent_when_person_present(conn):
    asset_id = repository.insert_asset(conn, _asset())
    asset = repository.get_asset(conn, asset_id)
    assert asset.is_usable_as_reference is False  # pessoa presumida, sem consentimento

    repository.update_asset_curation(conn, asset_id, consent_on_file=True)
    assert repository.get_asset(conn, asset_id).is_usable_as_reference is True
