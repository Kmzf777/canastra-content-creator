"""Ingestao da base de fotos reais.

Regras que nao se negociam aqui:
  * dedupe por sha256 - o mesmo arquivo nunca entra duas vezes;
  * `has_identifiable_person` e `consent_on_file` NUNCA sao inferidos - entram
    no default restritivo e so mudam pela curadoria humana;
  * nada sai do diretorio do projeto: geramos thumbnails, nao copias.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterator

from . import naming, repository
from .config import Settings
from .enums import Pillar
from .imaging import (
    SUPPORTED_EXTENSIONS,
    compute_quality,
    is_reference_grade,
    load_image,
    make_thumbnail,
    read_exif,
    sha256_file,
)
from .models import Asset

#: Tokens que sugerem embalagem visivel (heuristica; a curadoria confirma).
_PACKAGING_TAGS = {"pacote", "rotulo", "embalagem", "packshot", "capsula", "drip"}


@dataclass
class FileOutcome:
    path: Path
    status: str  # ingested | duplicate | skipped | error
    reason: str | None = None
    asset_id: int | None = None
    quality_score: int | None = None


@dataclass
class IngestReport:
    root: Path
    dry_run: bool = False
    outcomes: list[FileOutcome] = field(default_factory=list)

    def by_status(self, status: str) -> list[FileOutcome]:
        return [o for o in self.outcomes if o.status == status]

    @property
    def scanned(self) -> int:
        return len(self.outcomes)

    @property
    def ingested(self) -> int:
        return len(self.by_status("ingested"))

    @property
    def duplicates(self) -> int:
        return len(self.by_status("duplicate"))

    @property
    def skipped(self) -> int:
        return len(self.by_status("skipped"))

    @property
    def errors(self) -> int:
        return len(self.by_status("error"))

    @property
    def needs_review(self) -> int:
        return sum(1 for o in self.outcomes if o.status == "ingested" and o.reason)


def iter_candidate_files(root: Path) -> Iterator[Path]:
    """Varre recursivamente, ignorando diretorios ocultos e estado do proprio CIE."""
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        yield path


def _infer_packaging(pillar: Pillar | None, sku, subject_tags: list[str]) -> bool:
    if pillar is Pillar.PRODUCT or sku is not None:
        return True
    return any(tag in _PACKAGING_TAGS for tag in subject_tags)


def ingest_directory(
    conn: sqlite3.Connection,
    settings: Settings,
    root: Path | str,
    *,
    dry_run: bool = False,
    make_thumbs: bool = True,
    on_file: Callable[[FileOutcome], None] | None = None,
) -> IngestReport:
    root = Path(root).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"{root} nao e um diretorio")

    report = IngestReport(root=root, dry_run=dry_run)

    for path in iter_candidate_files(root):
        outcome = _ingest_one(
            conn, settings, root, path, dry_run=dry_run, make_thumbs=make_thumbs
        )
        report.outcomes.append(outcome)
        if on_file:
            on_file(outcome)

    return report


def _ingest_one(
    conn: sqlite3.Connection,
    settings: Settings,
    root: Path,
    path: Path,
    *,
    dry_run: bool,
    make_thumbs: bool,
) -> FileOutcome:
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return FileOutcome(path, "skipped", "extensao nao suportada")

    try:
        digest = sha256_file(path)
    except OSError as exc:
        return FileOutcome(path, "error", f"leitura falhou: {exc}")

    existing = repository.get_asset_by_sha256(conn, digest)
    if existing:
        return FileOutcome(path, "duplicate", f"sha256 ja ingerido (asset {existing.id})", existing.id)

    notes: list[str] = []
    image = load_image(path)
    width = height = None
    quality = None
    exif = None
    thumb_path = None

    if image is None:
        # RAW sem decoder, arquivo corrompido, etc. Entra no catalogo mesmo assim,
        # marcado para revisao - perder rastro de um arquivo da base e pior.
        notes.append("sem decoder disponivel: dimensoes e qualidade nao calculadas")
    else:
        width, height = image.width, image.height
        exif = read_exif(image)
        try:
            quality = compute_quality(image)
        except Exception as exc:  # imagens degeneradas (1px, modo exotico)
            notes.append(f"quality_score nao calculado: {exc}")
        if make_thumbs and not dry_run:
            try:
                thumb_path = str(make_thumbnail(image, settings.thumbs_dir / f"{digest[:16]}.jpg"))
            except Exception as exc:
                notes.append(f"thumbnail falhou: {exc}")
        image.close()

    inference = naming.infer(
        path,
        root=root,
        gps_lat=exif.gps_lat if exif else None,
        gps_lon=exif.gps_lon if exif else None,
    )
    notes.extend(inference.reasons)

    asset = Asset(
        path=str(path),
        sha256=digest,
        width=width,
        height=height,
        captured_at=exif.captured_at if exif else None,
        pillar=inference.pillar,
        location=inference.location,
        sku=inference.sku,
        subject_tags=inference.subject_tags,
        # Politica: sempre o default restritivo, nunca inferido.
        has_identifiable_person=True,
        consent_on_file=False,
        has_readable_packaging=_infer_packaging(
            inference.pillar, inference.sku, inference.subject_tags
        ),
        quality_score=quality.score if quality else None,
        is_reference_grade=is_reference_grade(quality, width, height),
        needs_review=inference.needs_review or image is None,
        thumb_path=thumb_path,
        camera=exif.camera if exif else None,
        lens=exif.lens if exif else None,
        gps_lat=exif.gps_lat if exif else None,
        gps_lon=exif.gps_lon if exif else None,
        notes="; ".join(notes) or None,
    )

    if dry_run:
        return FileOutcome(
            path,
            "ingested",
            "dry-run: nada gravado" if not asset.needs_review else "dry-run: needs_review",
            None,
            asset.quality_score,
        )

    try:
        asset_id = repository.insert_asset(conn, asset)
    except sqlite3.IntegrityError as exc:
        # Mesmo caminho ja catalogado com outro hash (arquivo foi editado no lugar).
        return FileOutcome(path, "error", f"conflito no banco: {exc}")

    return FileOutcome(
        path,
        "ingested",
        "needs_review" if asset.needs_review else None,
        asset_id,
        asset.quality_score,
    )
