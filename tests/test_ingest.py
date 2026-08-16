from __future__ import annotations

from pathlib import Path

import pytest

from cie import repository
from cie.enums import Location, Pillar, Sku
from cie.ingest import ingest_directory


def test_ingest_populates_catalog(conn, settings, tmp_path, photo_factory):
    base = tmp_path / "base"
    photo_factory(base / "CANASTRA_3_TORREFACAO_TAMBOR_001.jpg", seed=1)
    photo_factory(base / "CANASTRA_1_FAZENDA_TERREIRO_002.jpg", seed=2)

    report = ingest_directory(conn, settings, base)

    assert report.scanned == 2
    assert report.ingested == 2
    assert repository.count_assets(conn) == 2

    asset = repository.list_assets(conn, pillar=Pillar.P3)[0]
    assert asset.location is Location.TORREFACAO_UBERLANDIA
    assert "tambor" in asset.subject_tags
    assert asset.quality_score is not None


def test_dedupe_by_sha256_even_with_different_names(conn, settings, tmp_path, photo_factory):
    base = tmp_path / "base"
    original = photo_factory(base / "CANASTRA_1_FAZENDA_COLHEITA_001.jpg", seed=5)
    copy = base / "CANASTRA_1_FAZENDA_COLHEITA_002.jpg"
    copy.write_bytes(original.read_bytes())

    report = ingest_directory(conn, settings, base)

    assert report.ingested == 1
    assert report.duplicates == 1
    assert repository.count_assets(conn) == 1


def test_reingesting_same_folder_is_a_noop(conn, settings, tmp_path, photo_factory):
    base = tmp_path / "base"
    photo_factory(base / "CANASTRA_2_FAZENDA_PAINEIS_001.jpg", seed=3)

    ingest_directory(conn, settings, base)
    second = ingest_directory(conn, settings, base)

    assert second.ingested == 0
    assert second.duplicates == 1
    assert repository.count_assets(conn) == 1


def test_policy_fields_are_never_inferred(conn, settings, tmp_path, photo_factory):
    """Nem uma foto obviamente de pessoas escapa do default restritivo."""
    base = tmp_path / "base"
    photo_factory(base / "CANASTRA_PEOPLE_FAZENDA_RETRATO_FAMILIA_001.jpg", seed=4)

    ingest_directory(conn, settings, base)
    asset = repository.list_assets(conn)[0]

    assert asset.has_identifiable_person is True
    assert asset.consent_on_file is False
    assert asset.is_usable_as_reference is False


def test_unknown_pattern_goes_to_needs_review(conn, settings, tmp_path, photo_factory):
    base = tmp_path / "base"
    photo_factory(base / "diversos" / "IMG_9001.jpg", seed=6)

    ingest_directory(conn, settings, base)
    asset = repository.list_assets(conn)[0]

    assert asset.needs_review is True
    assert asset.pillar is None
    assert asset.notes and "nao inferido" in asset.notes


def test_unsupported_extensions_are_skipped(conn, settings, tmp_path, photo_factory):
    base = tmp_path / "base"
    photo_factory(base / "CANASTRA_1_FAZENDA_MUDA_001.jpg", seed=8)
    (base / "notas.txt").write_text("planejamento")
    (base / "video.mp4").write_bytes(b"\x00\x01")

    report = ingest_directory(conn, settings, base)

    assert report.ingested == 1
    assert report.skipped == 2


def test_hidden_directories_are_ignored(conn, settings, tmp_path, photo_factory):
    base = tmp_path / "base"
    photo_factory(base / ".cie" / "thumbs" / "x.jpg", seed=9)
    photo_factory(base / "CANASTRA_4_ESTUDIO_V60_001.jpg", seed=10)

    report = ingest_directory(conn, settings, base)

    assert report.scanned == 1
    assert report.ingested == 1


def test_dry_run_writes_nothing(conn, settings, tmp_path, photo_factory):
    base = tmp_path / "base"
    photo_factory(base / "CANASTRA_3_TORREFACAO_CUPPING_001.jpg", seed=11)

    report = ingest_directory(conn, settings, base, dry_run=True)

    assert report.ingested == 1
    assert repository.count_assets(conn) == 0
    assert not any(settings.thumbs_dir.iterdir())


def test_thumbnail_is_generated(conn, settings, tmp_path, photo_factory):
    base = tmp_path / "base"
    photo_factory(base / "CANASTRA_1_FAZENDA_CAFEZAL_001.jpg", seed=12)

    ingest_directory(conn, settings, base)
    asset = repository.list_assets(conn)[0]

    assert asset.thumb_path is not None
    assert Path(asset.thumb_path).exists()


def test_undecodable_file_is_catalogued_for_review(conn, settings, tmp_path):
    base = tmp_path / "base"
    base.mkdir()
    (base / "CANASTRA_1_FAZENDA_FLORADA_001.cr2").write_bytes(b"raw sem decoder")

    report = ingest_directory(conn, settings, base)
    asset = repository.list_assets(conn)[0]

    assert report.ingested == 1
    assert asset.width is None
    assert asset.needs_review is True
    assert asset.is_reference_grade is False
    assert "sem decoder" in (asset.notes or "")


def test_packaging_heuristic_flags_product_photos(conn, settings, tmp_path, photo_factory):
    base = tmp_path / "base"
    photo_factory(base / "CANASTRA_PRODUCT_ESTUDIO_GEISHA_PACOTE_001.jpg", seed=13)
    photo_factory(base / "CANASTRA_1_FAZENDA_NEBLINA_001.jpg", seed=14)

    ingest_directory(conn, settings, base)

    product = repository.list_assets(conn, sku=Sku.GEISHA)[0]
    scene = repository.list_assets(conn, pillar=Pillar.P1)[0]

    assert product.has_readable_packaging is True
    assert scene.has_readable_packaging is False


def test_ingest_rejects_non_directory(conn, settings, tmp_path):
    with pytest.raises(NotADirectoryError):
        ingest_directory(conn, settings, tmp_path / "nao-existe")
