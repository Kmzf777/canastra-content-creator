"""Testes da composicao local (produto real sobre fundo gerado). Nada toca a rede."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

from cie.compositor import (
    CompositionResult,
    compose_product,
    contact_sheet,
    has_alpha,
    list_cutouts,
    load_cutout,
    suggest_cutout_for_sku,
    trim_transparent_border,
)
from cie.config import Settings
from cie.enums import Sku
from cie.errors import CieError

BG_SIZE = (900, 600)
CUTOUT_SIZE = (400, 600)
CUTOUT_BORDER = 30
#: Produto util depois de tirar a moldura transparente.
PRODUCT_SIZE = (
    CUTOUT_SIZE[0] - 2 * CUTOUT_BORDER,
    CUTOUT_SIZE[1] - 2 * CUTOUT_BORDER,
)


def make_cutout(
    size: tuple[int, int] = CUTOUT_SIZE,
    border: int = CUTOUT_BORDER,
    color: tuple[int, int, int, int] = (120, 60, 30, 255),
) -> Image.Image:
    """Recorte sintetico: retangulo opaco dentro de uma moldura transparente."""
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(image).rectangle(
        (border, border, size[0] - border - 1, size[1] - border - 1), fill=color
    )
    return image


def write_cutout(path: Path, size: tuple[int, int] = CUTOUT_SIZE) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    make_cutout(size=size).save(path, format="PNG")
    return path


def margins(background_size: tuple[int, int], ratio: float = 0.08) -> tuple[int, int]:
    return round(background_size[0] * ratio), round(background_size[1] * ratio)


@pytest.fixture
def background(tmp_path: Path, photo_factory) -> Path:
    return photo_factory(tmp_path / "bg.jpg", size=BG_SIZE)


@pytest.fixture
def cutout_file(tmp_path: Path) -> Path:
    return write_cutout(tmp_path / "geisha_500g.png")


@pytest.fixture
def cutouts_dir(settings: Settings) -> Path:
    directory = settings.cutouts_dir
    directory.mkdir(parents=True, exist_ok=True)
    write_cutout(directory / "geisha_500g.png", size=(400, 600))
    write_cutout(directory / "geisha_250g.png", size=(200, 300))
    write_cutout(directory / "classico_250g.png", size=(300, 400))
    write_cutout(directory / "capsulas_10un.png", size=(300, 300))
    Image.new("RGB", (200, 200), (10, 20, 30)).save(directory / "sem_alfa.png")
    (directory / "leiame.txt").write_text("nao e imagem", encoding="utf-8")
    return directory


# --------------------------------------------------------------------------- #
# alfa
# --------------------------------------------------------------------------- #


def test_has_alpha_distinguishes_modes():
    assert has_alpha(make_cutout())
    assert not has_alpha(Image.new("RGB", (10, 10)))


def test_png_without_alpha_raises(tmp_path: Path):
    path = tmp_path / "packshot.png"
    Image.new("RGB", (200, 300), (200, 180, 160)).save(path)
    with pytest.raises(CieError) as exc:
        load_cutout(path)
    assert "alfa" in str(exc.value)


def test_fully_opaque_alpha_raises(tmp_path: Path):
    path = tmp_path / "opaco.png"
    Image.new("RGBA", (200, 300), (200, 180, 160, 255)).save(path)
    with pytest.raises(CieError):
        load_cutout(path)


def test_unreadable_file_raises(tmp_path: Path):
    path = tmp_path / "quebrado.png"
    path.write_bytes(b"nao sou um png")
    with pytest.raises(CieError):
        load_cutout(path)


def test_load_cutout_returns_rgba(cutout_file: Path):
    image = load_cutout(cutout_file)
    assert image.mode == "RGBA"
    assert image.size == CUTOUT_SIZE


def test_compose_rejects_in_memory_cutout_without_alpha(background: Path, tmp_path: Path):
    with pytest.raises(CieError):
        compose_product(
            background,
            Image.new("RGB", (100, 100), (10, 10, 10)),
            dest=tmp_path / "out.png",
        )


def test_trim_transparent_border_crops(tmp_path: Path):
    trimmed = trim_transparent_border(make_cutout())
    assert trimmed.size == PRODUCT_SIZE
    # Sem moldura sobrando: o alfa agora encosta nas quatro bordas.
    assert trimmed.getchannel("A").getbbox() == (0, 0, PRODUCT_SIZE[0], PRODUCT_SIZE[1])


def test_trim_keeps_image_without_border():
    solid = Image.new("RGBA", (50, 40), (10, 10, 10, 255))
    solid.putpixel((0, 0), (10, 10, 10, 0))
    assert trim_transparent_border(solid).size == (50, 40)


# --------------------------------------------------------------------------- #
# geometria da composicao
# --------------------------------------------------------------------------- #


def test_composition_keeps_product_aspect_ratio(background: Path, cutout_file: Path, tmp_path: Path):
    result = compose_product(background, cutout_file, dest=tmp_path / "out.png")
    original = PRODUCT_SIZE[0] / PRODUCT_SIZE[1]
    composed = result.size[0] / result.size[1]
    assert composed == pytest.approx(original, abs=0.01)


def test_scale_is_the_fraction_of_background_height(
    background: Path, cutout_file: Path, tmp_path: Path
):
    result = compose_product(background, cutout_file, dest=tmp_path / "out.png", scale=0.55)
    assert result.size[1] == round(BG_SIZE[1] * 0.55)
    assert result.scale == pytest.approx(0.55, abs=0.01)


def test_product_stays_inside_background_with_margin(
    background: Path, cutout_file: Path, tmp_path: Path
):
    margin_ratio = 0.1
    result = compose_product(
        background, cutout_file, dest=tmp_path / "out.png", margin_ratio=margin_ratio
    )
    margin_x, margin_y = margins(BG_SIZE, margin_ratio)
    x, y = result.position
    width, height = result.size
    assert x >= margin_x and y >= margin_y
    assert x + width <= BG_SIZE[0] - margin_x
    assert y + height <= BG_SIZE[1] - margin_y


def test_oversized_scale_shrinks_to_respect_margin(
    background: Path, cutout_file: Path, tmp_path: Path
):
    margin_ratio = 0.1
    result = compose_product(
        background, cutout_file, dest=tmp_path / "out.png", scale=1.0, margin_ratio=margin_ratio
    )
    _, margin_y = margins(BG_SIZE, margin_ratio)
    assert result.size[1] <= BG_SIZE[1] - 2 * margin_y
    assert result.scale < 1.0
    # Encolher para caber nao pode deformar o produto.
    assert result.size[0] / result.size[1] == pytest.approx(
        PRODUCT_SIZE[0] / PRODUCT_SIZE[1], abs=0.01
    )


def test_wide_cutout_is_limited_by_the_available_width(
    background: Path, tmp_path: Path
):
    wide = make_cutout(size=(1200, 200), border=10)
    result = compose_product(
        background, wide, dest=tmp_path / "out.png", scale=0.9, margin_ratio=0.08
    )
    margin_x, _ = margins(BG_SIZE, 0.08)
    assert result.size[0] <= BG_SIZE[0] - 2 * margin_x
    assert result.position[0] >= margin_x


@pytest.mark.parametrize("anchor", ["center", "center-bottom", "left-bottom", "right-bottom"])
def test_each_anchor_positions_where_it_should(
    background: Path, cutout_file: Path, tmp_path: Path, anchor: str
):
    result = compose_product(
        background, cutout_file, dest=tmp_path / f"{anchor}.png", anchor=anchor
    )
    margin_x, margin_y = margins(BG_SIZE)
    x, y = result.position
    width, height = result.size
    centered_x = (BG_SIZE[0] - width) // 2

    if anchor == "center":
        assert (x, y) == (centered_x, (BG_SIZE[1] - height) // 2)
    else:
        # Todas as ancoras "-bottom" apoiam o produto na linha da margem inferior.
        assert y + height == BG_SIZE[1] - margin_y
        if anchor == "center-bottom":
            assert x == centered_x
        elif anchor == "left-bottom":
            assert x == margin_x
        else:
            assert x + width == BG_SIZE[0] - margin_x


def test_invalid_anchor_raises(background: Path, cutout_file: Path, tmp_path: Path):
    with pytest.raises(CieError) as exc:
        compose_product(background, cutout_file, dest=tmp_path / "out.png", anchor="topo")
    assert "anchor" in str(exc.value)


@pytest.mark.parametrize(
    "kwargs", [{"scale": 0.0}, {"scale": 1.5}, {"margin_ratio": -0.1}, {"margin_ratio": 0.6}]
)
def test_out_of_range_parameters_raise(
    background: Path, cutout_file: Path, tmp_path: Path, kwargs: dict
):
    with pytest.raises(CieError):
        compose_product(background, cutout_file, dest=tmp_path / "out.png", **kwargs)


# --------------------------------------------------------------------------- #
# pixels
# --------------------------------------------------------------------------- #


def test_product_pixels_land_on_the_background(
    background: Path, cutout_file: Path, tmp_path: Path
):
    dest = compose_product(background, cutout_file, dest=tmp_path / "out.png")
    composed = Image.open(dest.path).convert("RGB")
    x, y = dest.position
    width, height = dest.size
    center = composed.getpixel((x + width // 2, y + height // 2))
    assert center == (120, 60, 30)


def test_shadow_darkens_pixels_below_the_product(
    background: Path, cutout_file: Path, tmp_path: Path
):
    with_shadow = compose_product(
        background, cutout_file, dest=tmp_path / "com_sombra.png", shadow=True
    )
    without_shadow = compose_product(
        background, cutout_file, dest=tmp_path / "sem_sombra.png", shadow=False
    )
    assert with_shadow.position == without_shadow.position

    shaded = Image.open(with_shadow.path).convert("RGB")
    plain = Image.open(without_shadow.path).convert("RGB")
    x, y = with_shadow.position
    width, height = with_shadow.size
    sample_x = x + width // 2
    for offset in (2, 6, 12):
        sample_y = y + height + offset
        assert sum(shaded.getpixel((sample_x, sample_y))) < sum(
            plain.getpixel((sample_x, sample_y))
        )


def test_without_shadow_the_background_is_untouched(
    background: Path, cutout_file: Path, tmp_path: Path
):
    result = compose_product(background, cutout_file, dest=tmp_path / "out.png", shadow=False)
    composed = Image.open(result.path).convert("RGB")
    original = Image.open(background).convert("RGB")
    x, y = result.position
    _, height = result.size
    point = (x, y + height + 10)
    assert composed.getpixel(point) == original.getpixel(point)


def test_png_output_is_rgba_and_jpeg_output_is_rgb(
    background: Path, cutout_file: Path, tmp_path: Path
):
    png = compose_product(background, cutout_file, dest=tmp_path / "out.png")
    jpeg = compose_product(background, cutout_file, dest=tmp_path / "out.jpg")
    assert Image.open(png.path).mode == "RGBA"
    assert Image.open(jpeg.path).mode == "RGB"
    assert Image.open(jpeg.path).size == BG_SIZE


def test_dest_directory_is_created(background: Path, cutout_file: Path, tmp_path: Path):
    result = compose_product(background, cutout_file, dest=tmp_path / "novo" / "sub" / "out.png")
    assert result.path.exists()


# --------------------------------------------------------------------------- #
# proveniencia
# --------------------------------------------------------------------------- #


def test_provenance_records_sources_and_keeps_disclosure(
    background: Path, cutout_file: Path, tmp_path: Path
):
    result = compose_product(background, cutout_file, dest=tmp_path / "out.png")
    assert isinstance(result, CompositionResult)
    provenance = result.as_provenance()
    assert provenance["method"] == "local_composition"
    assert provenance["background"] == str(background)
    assert provenance["cutout"] == str(cutout_file)
    assert provenance["product_is_real"] is True
    # Fundo continua gerado: a rotulagem de IA nao cai por causa da composicao.
    assert provenance["disclosure_required"] is True
    assert provenance["size"] == list(result.size)
    assert json.loads(json.dumps(provenance)) == provenance


def test_in_memory_sources_have_no_path_in_provenance(background: Path, tmp_path: Path):
    result = compose_product(
        Image.open(background), make_cutout(), dest=tmp_path / "out.png"
    )
    provenance = result.as_provenance()
    assert provenance["background"] is None and provenance["cutout"] is None


# --------------------------------------------------------------------------- #
# catalogo de recortes
# --------------------------------------------------------------------------- #


def test_list_cutouts_is_empty_without_directory(settings: Settings):
    assert list_cutouts(settings) == []


def test_list_cutouts_skips_non_images_and_files_without_alpha(
    settings: Settings, cutouts_dir: Path
):
    names = {path.name for path in list_cutouts(settings)}
    assert names == {
        "geisha_500g.png",
        "geisha_250g.png",
        "classico_250g.png",
        "capsulas_10un.png",
    }


def test_list_cutouts_filters_by_sku(settings: Settings, cutouts_dir: Path):
    geisha = list_cutouts(settings, Sku.GEISHA)
    assert {path.name for path in geisha} == {"geisha_500g.png", "geisha_250g.png"}
    assert list_cutouts(settings, "geisha") == geisha
    assert [p.name for p in list_cutouts(settings, Sku.CLASSICO)] == ["classico_250g.png"]
    # 'capsulas' e plural: resolve pelo vocabulario de SKU da ingestao.
    assert [p.name for p in list_cutouts(settings, Sku.CAPSULA)] == ["capsulas_10un.png"]
    assert list_cutouts(settings, Sku.DRIP) == []


def test_suggest_cutout_prefers_the_largest_and_returns_none_when_absent(
    settings: Settings, cutouts_dir: Path
):
    assert suggest_cutout_for_sku(settings, Sku.GEISHA).name == "geisha_500g.png"
    assert suggest_cutout_for_sku(settings, Sku.DRIP) is None


def test_suggested_cutout_composes(settings: Settings, cutouts_dir: Path, background: Path):
    cutout = suggest_cutout_for_sku(settings, Sku.GEISHA)
    result = compose_product(background, cutout, dest=settings.generations_dir / "comp.png")
    assert result.cutout_path == cutout
    assert result.path.exists()


# --------------------------------------------------------------------------- #
# folha de contato
# --------------------------------------------------------------------------- #


def test_contact_sheet_creates_the_file_with_the_expected_grid(
    tmp_path: Path, photo_factory
):
    paths = [photo_factory(tmp_path / f"s{i}.jpg", size=(320, 240)) for i in range(5)]
    dest = contact_sheet(paths, tmp_path / "folha.png", columns=4, thumb=100)
    assert dest.exists()
    sheet = Image.open(dest)
    # 4 colunas x 2 linhas, celula = thumb + padding.
    assert sheet.size == (4 * 112 + 12, 2 * 112 + 12)


def test_contact_sheet_skips_unreadable_paths(tmp_path: Path, photo_factory):
    good = photo_factory(tmp_path / "boa.jpg", size=(320, 240))
    broken = tmp_path / "nota.txt"
    broken.write_text("nao e imagem", encoding="utf-8")
    dest = contact_sheet([good, broken], tmp_path / "folha.jpg", columns=4, thumb=80)
    assert dest.exists()
    # So uma imagem legivel: a grade encolhe para uma coluna.
    assert Image.open(dest).size == (1 * 92 + 12, 1 * 92 + 12)


def test_contact_sheet_without_any_readable_image_raises(tmp_path: Path):
    (tmp_path / "nota.txt").write_text("nada", encoding="utf-8")
    with pytest.raises(CieError):
        contact_sheet([tmp_path / "nota.txt"], tmp_path / "folha.png")


@pytest.mark.parametrize("kwargs", [{"columns": 0}, {"thumb": 4}])
def test_contact_sheet_rejects_degenerate_grids(tmp_path: Path, photo_factory, kwargs: dict):
    good = photo_factory(tmp_path / "boa.jpg", size=(320, 240))
    with pytest.raises(CieError):
        contact_sheet([good], tmp_path / "folha.png", **kwargs)
