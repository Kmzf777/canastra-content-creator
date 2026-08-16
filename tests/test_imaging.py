from __future__ import annotations

from datetime import datetime

from PIL import Image

from cie.imaging import (
    _dms_to_degrees,
    _parse_exif_datetime,
    compute_quality,
    is_reference_grade,
    load_image,
    make_thumbnail,
    sha256_file,
)


def test_sha256_is_content_based(tmp_path, photo_factory):
    a = photo_factory(tmp_path / "a.jpg", seed=1)
    b = tmp_path / "b.jpg"
    b.write_bytes(a.read_bytes())
    c = photo_factory(tmp_path / "c.jpg", seed=2)

    assert sha256_file(a) == sha256_file(b)
    assert sha256_file(a) != sha256_file(c)


def test_sharp_image_scores_above_blurred(tmp_path, photo_factory):
    sharp = load_image(photo_factory(tmp_path / "sharp.jpg", blur=0))
    blurred = load_image(photo_factory(tmp_path / "blur.jpg", blur=6))

    sharp_quality = compute_quality(sharp)
    blurred_quality = compute_quality(blurred)

    assert sharp_quality.sharpness > blurred_quality.sharpness
    assert sharp_quality.score > blurred_quality.score
    assert 0 <= blurred_quality.score <= 100


def test_reference_grade_requires_score_and_resolution(tmp_path, photo_factory):
    big = load_image(photo_factory(tmp_path / "big.jpg", size=(2400, 1600)))
    small = load_image(photo_factory(tmp_path / "small.jpg", size=(800, 600)))

    assert is_reference_grade(compute_quality(big), 2400, 1600) is True
    # Mesmo nitida, resolucao baixa nao serve de referencia.
    assert is_reference_grade(compute_quality(small), 800, 600) is False
    assert is_reference_grade(None, 2400, 1600) is False


def test_thumbnail_is_bounded(tmp_path, photo_factory):
    image = load_image(photo_factory(tmp_path / "p.jpg", size=(2000, 1000)))
    dest = make_thumbnail(image, tmp_path / "thumbs" / "p.jpg", max_side=320)

    with Image.open(dest) as thumb:
        assert max(thumb.size) <= 320


def test_load_image_returns_none_for_undecodable(tmp_path):
    fake_raw = tmp_path / "DSC_0001.cr2"
    fake_raw.write_bytes(b"not really a raw file")

    assert load_image(fake_raw) is None


def test_exif_datetime_parsing():
    assert _parse_exif_datetime("2026:03:14 06:31:00") == datetime(2026, 3, 14, 6, 31)
    assert _parse_exif_datetime("lixo") is None
    assert _parse_exif_datetime(None) is None


def test_gps_dms_conversion():
    # 19 deg 59' 40" S -> negativo
    value = _dms_to_degrees((19.0, 59.0, 40.0), "S")
    assert value is not None and -20.0 < value < -19.9
    assert _dms_to_degrees((1.0, 2.0), "N") is None
