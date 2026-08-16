"""Exportacao: recorte inteligente, proveniencia no arquivo e manifesto do lote.

Nada aqui toca a rede: as imagens sao sinteticas e o banco e o de teste.
"""

from __future__ import annotations

import json
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

from cie import repository
from cie.config import Settings
from cie.enums import AspectRatio, ExportFormat, JobStatus, Pillar, ReviewStatus, TemplateKind
from cie.errors import CieError
from cie.export import (
    EXPORT_QUALITY,
    XMP_CIE_NAMESPACE,
    ExportedVariant,
    FocalPoint,
    build_xmp_packet,
    detect_focal_point,
    export_approved,
    export_filename,
    export_generation,
    sidecar_path,
    smart_crop,
    write_metadata,
)
from cie.imaging import sha256_file
from cie.models import Generation, Job, Template
from cie.utils import utcnow

RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
DC_NS = "http://purl.org/dc/elements/1.1/"
IPTC_NS = "http://iptc.org/std/Iptc4xmpExt/2008-02-29/"
NAMESPACES = {"rdf": RDF_NS, "dc": DC_NS, "cie": XMP_CIE_NAMESPACE, "Iptc4xmpExt": IPTC_NS}

GRAY = (128, 128, 128)
RED = (255, 0, 0)


# --------------------------------------------------------------------------- #
# ajudantes
# --------------------------------------------------------------------------- #


def make_marked_image(
    size: tuple[int, int] = (1200, 900), mark: tuple[float, float] = (0.9, 0.5)
) -> Image.Image:
    """Fundo liso com um quadrado vermelho no ponto relativo pedido.

    O quadrado e o marcador que prova se o recorte manteve aquele ponto.
    """
    image = Image.new("RGB", size, GRAY)
    cx, cy = int(mark[0] * size[0]), int(mark[1] * size[1])
    ImageDraw.Draw(image).rectangle((cx - 40, cy - 40, cx + 40, cy + 40), fill=RED)
    return image


def has_mark(image: Image.Image) -> bool:
    rgb = image.convert("RGB")
    (_, red_max), (green_min, _), _ = rgb.getextrema()
    return red_max > 200 and green_min < 60


def make_half_detailed_image(size: tuple[int, int] = (800, 600)) -> Image.Image:
    """Metade esquerda lisa, metade direita com textura de alto microcontraste."""
    image = Image.new("RGB", size, GRAY)
    pixels = image.load()
    for y in range(size[1]):
        for x in range(size[0] // 2, size[0]):
            value = 20 if (x + y) % 2 else 235
            pixels[x, y] = (value, value, value)
    return image


def insert_template(
    conn: sqlite3.Connection,
    name: str = "macro_grao_torrado",
    pillar: Pillar | None = Pillar.P3,
) -> Template:
    template_id = repository.upsert_template(
        conn,
        Template(
            name=name,
            pillar=pillar,
            kind=TemplateKind.MACRO,
            body="macro de grao torrado sobre bandeja de cupping",
            negative_prompt="texto ilegivel, rosto humano",
            default_aspect_ratio=AspectRatio.R4_3,
        ),
    )
    template = repository.get_template(conn, template_id)
    assert template is not None
    return template


def insert_generation(
    conn: sqlite3.Connection,
    settings: Settings,
    *,
    template: Template,
    filename: str,
    image: Image.Image,
    review_status: ReviewStatus = ReviewStatus.APPROVED,
    reference_asset_ids: list[int] | None = None,
) -> Generation:
    references = [11, 12] if reference_asset_ids is None else reference_asset_ids
    job_id = repository.insert_job(
        conn,
        Job(
            template_id=template.id,
            reference_asset_ids=references,
            resolved_prompt="macro de grao torrado, luz lateral quente",
            model="grok-imagine-image",
            aspect_ratio=AspectRatio.R4_3,
            n=1,
            status=JobStatus.DONE,
            cost_usd=0.07,
        ),
    )
    path = settings.generations_dir / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="JPEG", quality=95)
    generation_id = repository.insert_generation(
        conn,
        Generation(
            job_id=job_id,
            path=str(path),
            sha256=sha256_file(path),
            model="grok-imagine-image",
            prompt="macro de grao torrado, luz lateral quente",
            seed=4242,
            cost_usd=0.07,
            review_status=review_status,
            created_at=utcnow(),
        ),
    )
    generation = repository.get_generation(conn, generation_id)
    assert generation is not None
    return generation


def read_embedded_xmp(path: Path) -> str:
    with Image.open(path) as image:
        image.load()
        packet = image.info.get("xmp")
    assert packet, f"{path.name} saiu sem XMP embutido"
    return packet.decode("utf-8")


# --------------------------------------------------------------------------- #
# recorte
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("ratio", ["9:16", "4:5", "1:1"])
def test_smart_crop_returns_exact_ratio(ratio: str) -> None:
    source = Image.new("RGB", (1600, 1200), GRAY)
    crop = smart_crop(source, ratio)
    ratio_w, ratio_h = (int(part) for part in ratio.split(":"))

    # Proporcao exata em inteiros: nada de 0,7998 no lugar de 0,8.
    assert crop.width * ratio_h == crop.height * ratio_w
    assert crop.width <= source.width and crop.height <= source.height


def test_smart_crop_accepts_export_format_enum() -> None:
    crop = smart_crop(Image.new("RGB", (1600, 1200), GRAY), ExportFormat.R4_5)
    assert crop.width * 5 == crop.height * 4


def test_smart_crop_keeps_manual_focal_point_inside_frame() -> None:
    source = make_marked_image((1200, 900), mark=(0.9, 0.5))

    kept = smart_crop(source, "9:16", FocalPoint(0.9, 0.5))
    assert has_mark(kept), "o recorte perdeu o ponto focal pedido"

    # Controle: com o foco no outro extremo o marcador tem de ficar de fora.
    dropped = smart_crop(source, "9:16", FocalPoint(0.1, 0.5))
    assert not has_mark(dropped)


def test_smart_crop_clamps_focal_point_to_the_edges() -> None:
    source = make_marked_image((1200, 900), mark=(0.97, 0.5))
    crop = smart_crop(source, "9:16", FocalPoint(1.0, 0.5))
    assert has_mark(crop)
    assert crop.width * 16 == crop.height * 9


def test_smart_crop_rejects_impossible_ratio() -> None:
    with pytest.raises(CieError):
        smart_crop(Image.new("RGB", (10, 10), GRAY), "9:16000")
    with pytest.raises(CieError):
        smart_crop(Image.new("RGB", (100, 100), GRAY), "quadrado")


# --------------------------------------------------------------------------- #
# ponto focal
# --------------------------------------------------------------------------- #


def test_detect_focal_point_finds_the_detailed_half() -> None:
    focal = detect_focal_point(make_half_detailed_image())
    assert focal.x > 0.6, f"a saliencia ficou na metade lisa (x={focal.x:.2f})"
    assert 0.3 < focal.y < 0.7


def test_detect_focal_point_falls_back_to_center_on_flat_image() -> None:
    focal = detect_focal_point(Image.new("RGB", (800, 600), GRAY))
    assert (focal.x, focal.y) == (0.5, 0.5)


def test_focal_point_clamps_to_relative_range() -> None:
    assert FocalPoint(1.4, -0.2) == FocalPoint(1.0, 0.0)
    assert FocalPoint.center() == FocalPoint(0.5, 0.5)


# --------------------------------------------------------------------------- #
# nome do arquivo
# --------------------------------------------------------------------------- #


def test_export_filename_follows_convention() -> None:
    assert (
        export_filename(Pillar.P3, "macro_grao_torrado", 1, "9:16")
        == "CANASTRA_3_MACRO_GRAO_TORRADO_001_9-16.jpg"
    )


def test_export_filename_normalizes_accents_and_enums() -> None:
    assert (
        export_filename(Pillar.PRODUCT, "Torrefação Tambor", 12, ExportFormat.R4_5)
        == "CANASTRA_PRODUCT_TORREFACAO_TAMBOR_012_4-5.jpg"
    )
    # Sem pilar curado o nome nao chuta um pilar.
    assert export_filename(None, "avulso", 7, "1:1") == "CANASTRA_X_AVULSO_007_1-1.jpg"


# --------------------------------------------------------------------------- #
# XMP / EXIF
# --------------------------------------------------------------------------- #


def test_build_xmp_packet_is_wellformed_and_declares_ai() -> None:
    packet = build_xmp_packet(
        creator="Cafe Canastra",
        description="Cafe Canastra - macro_grao_torrado",
        provenance="Imagem gerada com assistencia de IA; assets 11, 12",
        model="grok-imagine-image",
        created="2026-08-16T12:00:00+00:00",
    )
    text = packet.decode("utf-8")
    assert text.startswith('<?xpacket begin="\ufeff"')
    root = ET.fromstring(text)

    provenance = root.find(".//cie:provenance", NAMESPACES)
    assert provenance is not None and "assistencia de IA" in (provenance.text or "")
    model = root.find(".//cie:model", NAMESPACES)
    assert model is not None and model.text == "grok-imagine-image"
    source_type = root.find(".//Iptc4xmpExt:DigitalSourceType", NAMESPACES)
    assert source_type is not None
    assert "trainedAlgorithmicMedia" in source_type.attrib[f"{{{RDF_NS}}}resource"]


def test_write_metadata_embeds_xmp_exif_and_writes_sidecar(tmp_path: Path) -> None:
    path = tmp_path / "saida.jpg"
    Image.new("RGB", (400, 400), GRAY).save(path, format="JPEG", quality=EXPORT_QUALITY)
    before = path.read_bytes()

    write_metadata(
        path,
        description="Cafe Canastra - macro_grao_torrado",
        provenance="Imagem gerada com assistencia de IA; assets 11, 12",
        model="grok-imagine-image",
        created="2026-08-16T12:00:00+00:00",
    )

    embedded = read_embedded_xmp(path)
    assert "assistencia de IA" in embedded

    sidecar = sidecar_path(path)
    assert sidecar.exists(), "o sidecar .xmp e a garantia contra plataforma que limpa metadados"
    assert sidecar.read_bytes().decode("utf-8") == embedded

    with Image.open(path) as image:
        exif = image.getexif()
        assert image.size == (400, 400)
    assert exif.get(0x013B) == "Cafe Canastra"  # Artist
    assert "assistencia de IA" in exif.get(0x010E)  # ImageDescription
    assert "Cafe Canastra" in exif.get(0x8298)  # Copyright
    assert len(path.read_bytes()) > len(before)


def test_write_metadata_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / "saida.jpg"
    Image.new("RGB", (200, 200), GRAY).save(path, format="JPEG", quality=EXPORT_QUALITY)
    kwargs = dict(
        description="descricao",
        provenance="proveniencia",
        model="grok-imagine-image",
        created=None,
    )
    write_metadata(path, **kwargs)
    once = path.read_bytes()
    write_metadata(path, **kwargs)

    # Regravar nao empilha marcador APP1 nem recomprime a imagem.
    assert path.read_bytes() == once


# --------------------------------------------------------------------------- #
# exportacao de uma geracao
# --------------------------------------------------------------------------- #


def test_export_generation_writes_every_format_with_provenance(
    conn: sqlite3.Connection, settings: Settings, tmp_path: Path
) -> None:
    template = insert_template(conn)
    generation = insert_generation(
        conn,
        settings,
        template=template,
        filename="gen_001.jpg",
        image=make_marked_image((1200, 900), mark=(0.5, 0.5)),
    )
    out_dir = tmp_path / "export"

    variants = export_generation(
        conn,
        settings,
        generation,
        formats=("9:16", "4:5", "1:1"),
        out_dir=out_dir,
        template=template,
        sequence=7,
    )

    assert [v.aspect_ratio for v in variants] == ["9:16", "4:5", "1:1"]
    names = {v.path.name for v in variants}
    assert "CANASTRA_3_MACRO_GRAO_TORRADO_007_9-16.jpg" in names

    for variant in variants:
        assert variant.path.exists()
        assert variant.sha256 == sha256_file(variant.path)
        ratio_w, ratio_h = (int(p) for p in variant.aspect_ratio.split(":"))
        assert variant.width * ratio_h == variant.height * ratio_w
        with Image.open(variant.path) as image:
            assert image.format == "JPEG"
            assert image.mode == "RGB"
            assert image.size == (variant.width, variant.height)
        embedded = read_embedded_xmp(variant.path)
        assert "grok-imagine-image" in embedded
        assert "11, 12" in embedded  # ids dos assets de referencia
        assert sidecar_path(variant.path).exists()


def test_export_generation_uses_stored_focal_point(
    conn: sqlite3.Connection, settings: Settings, tmp_path: Path
) -> None:
    template = insert_template(conn)
    generation = insert_generation(
        conn,
        settings,
        template=template,
        filename="gen_focal.jpg",
        image=make_marked_image((1200, 900), mark=(0.9, 0.5)),
    )
    repository.set_focal_point(conn, generation.id, 0.9, 0.5)

    variants = export_generation(
        conn, settings, generation, formats=("9:16",), out_dir=tmp_path / "export"
    )

    with Image.open(variants[0].path) as image:
        assert has_mark(image), "o recorte ignorou o ponto focal gravado no banco"


def test_export_generation_records_relative_variants_in_db(
    conn: sqlite3.Connection, settings: Settings
) -> None:
    template = insert_template(conn)
    generation = insert_generation(
        conn,
        settings,
        template=template,
        filename="gen_db.jpg",
        image=make_marked_image((1200, 900)),
    )

    export_generation(
        conn,
        settings,
        generation,
        formats=("9:16", "1:1"),
        out_dir=settings.root / "export",
    )

    stored = repository.get_generation(conn, generation.id)
    assert len(stored.exported_variants) == 2
    for entry in stored.exported_variants:
        assert not Path(entry).is_absolute(), "o banco guarda caminho relativo a raiz"
        assert entry.startswith("export/") and entry.endswith(".jpg")
        assert (settings.root / entry).exists()


def test_export_generation_fails_loudly_when_source_is_missing(
    conn: sqlite3.Connection, settings: Settings, tmp_path: Path
) -> None:
    template = insert_template(conn)
    generation = insert_generation(
        conn,
        settings,
        template=template,
        filename="gen_sumido.jpg",
        image=make_marked_image((600, 600)),
    )
    Path(generation.path).unlink()

    with pytest.raises(CieError):
        export_generation(
            conn, settings, generation, formats=("1:1",), out_dir=tmp_path / "export"
        )


# --------------------------------------------------------------------------- #
# lote e manifesto
# --------------------------------------------------------------------------- #


def test_export_approved_skips_pending_and_rejected(
    conn: sqlite3.Connection, settings: Settings, tmp_path: Path
) -> None:
    template = insert_template(conn)
    approved = insert_generation(
        conn,
        settings,
        template=template,
        filename="aprovada.jpg",
        image=make_marked_image((1200, 900)),
    )
    pending = insert_generation(
        conn,
        settings,
        template=template,
        filename="pendente.jpg",
        image=make_marked_image((1200, 900)),
        review_status=ReviewStatus.PENDING,
    )
    rejected = insert_generation(
        conn,
        settings,
        template=template,
        filename="rejeitada.jpg",
        image=make_marked_image((1200, 900)),
        review_status=ReviewStatus.REJECTED,
    )
    out_dir = tmp_path / "export"

    batch = export_approved(conn, settings, formats=("9:16", "1:1"), out_dir=out_dir)

    assert batch.generation_ids == [approved.id]
    assert len(batch.variants) == 2
    assert len(list(out_dir.glob("*.jpg"))) == 2
    # A sequencia do nome e o id da geracao: nada colide entre lotes.
    assert all(f"_{approved.id:03d}_" in v.path.name for v in batch.variants)
    for generation in (pending, rejected):
        assert repository.get_generation(conn, generation.id).exported_variants == []


def test_export_approved_writes_manifest_with_one_entry_per_generation(
    conn: sqlite3.Connection, settings: Settings, tmp_path: Path
) -> None:
    template = insert_template(conn)
    first = insert_generation(
        conn,
        settings,
        template=template,
        filename="lote_a.jpg",
        image=make_marked_image((1200, 900)),
    )
    second = insert_generation(
        conn,
        settings,
        template=template,
        filename="lote_b.jpg",
        image=make_marked_image((1200, 900)),
        reference_asset_ids=[31],
    )
    out_dir = tmp_path / "export"

    batch = export_approved(conn, settings, formats=("9:16", "4:5", "1:1"), out_dir=out_dir)

    assert batch.manifest_path == out_dir / "manifest.json"
    manifest = json.loads(batch.manifest_path.read_text(encoding="utf-8"))
    assert manifest["lote"]
    assert "IA" in manifest["rotulagem"]

    entries = manifest["imagens"]
    assert [entry["generation_id"] for entry in entries] == [first.id, second.id]
    for entry in entries:
        assert entry["job_id"]
        assert entry["template"] == "macro_grao_torrado"
        assert entry["pilar"] == "3"
        assert entry["prompt"] == "macro de grao torrado, luz lateral quente"
        assert entry["modelo"] == "grok-imagine-image"
        assert entry["seed"] == 4242
        assert entry["sha256"]
        assert entry["disclosure_required"] is True
        assert "Instagram" in entry["rotulagem"]
        assert len(entry["variantes"]) == 3
        for variant in entry["variantes"]:
            assert (out_dir / variant["arquivo"]).exists()
            assert variant["sha256"] and variant["width"] and variant["height"]

    assert entries[0]["reference_asset_ids"] == [11, 12]
    assert entries[1]["reference_asset_ids"] == [31]


def test_export_approved_defaults_to_settings_export_dir(
    conn: sqlite3.Connection, settings: Settings
) -> None:
    template = insert_template(conn, name="terreiro_secagem", pillar=Pillar.P1)
    insert_generation(
        conn,
        settings,
        template=template,
        filename="terreiro.jpg",
        image=make_marked_image((1200, 900)),
    )

    batch = export_approved(conn, settings)

    assert batch.out_dir == settings.export_dir
    assert len(batch.variants) == 3  # 9:16, 4:5 e 1:1
    assert all(isinstance(variant, ExportedVariant) for variant in batch.variants)
    assert batch.manifest_path.exists()


def test_export_approved_on_empty_queue_still_writes_manifest(
    conn: sqlite3.Connection, settings: Settings, tmp_path: Path
) -> None:
    batch = export_approved(conn, settings, formats=("1:1",), out_dir=tmp_path / "export")

    assert batch.variants == []
    manifest = json.loads(batch.manifest_path.read_text(encoding="utf-8"))
    assert manifest["imagens"] == []
