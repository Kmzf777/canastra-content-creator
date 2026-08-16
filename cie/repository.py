"""Acesso a dados. Converte linhas do SQLite em modelos Pydantic e vice-versa."""

from __future__ import annotations

import sqlite3
from typing import Any, Iterable

from .enums import Location, Pillar, Sku
from .models import Asset, StyleDescriptor
from .utils import dumps, iso, loads, parse_dt, utcnow

# --------------------------------------------------------------------------- #
# assets
# --------------------------------------------------------------------------- #

ASSET_CURATION_FIELDS = (
    "pillar",
    "location",
    "sku",
    "subject_tags",
    "has_identifiable_person",
    "consent_on_file",
    "has_readable_packaging",
    "is_reference_grade",
    "needs_review",
    "notes",
)


def row_to_asset(row: sqlite3.Row) -> Asset:
    descriptor_raw = loads(row["style_descriptor"], None)
    return Asset(
        id=row["id"],
        path=row["path"],
        sha256=row["sha256"],
        width=row["width"],
        height=row["height"],
        captured_at=parse_dt(row["captured_at"]),
        pillar=Pillar(row["pillar"]) if row["pillar"] else None,
        location=Location(row["location"]) if row["location"] else None,
        sku=Sku(row["sku"]) if row["sku"] else None,
        subject_tags=loads(row["subject_tags"], []) or [],
        has_identifiable_person=bool(row["has_identifiable_person"]),
        consent_on_file=bool(row["consent_on_file"]),
        has_readable_packaging=bool(row["has_readable_packaging"]),
        quality_score=row["quality_score"],
        is_reference_grade=bool(row["is_reference_grade"]),
        style_descriptor=StyleDescriptor(**descriptor_raw) if descriptor_raw else None,
        needs_review=bool(row["needs_review"]),
        thumb_path=row["thumb_path"],
        camera=row["camera"],
        lens=row["lens"],
        gps_lat=row["gps_lat"],
        gps_lon=row["gps_lon"],
        notes=row["notes"],
        created_at=parse_dt(row["created_at"]),
        updated_at=parse_dt(row["updated_at"]),
    )


def insert_asset(conn: sqlite3.Connection, asset: Asset) -> int:
    now = iso(utcnow())
    cursor = conn.execute(
        """
        INSERT INTO assets (
            path, sha256, width, height, captured_at, pillar, location, sku,
            subject_tags, has_identifiable_person, consent_on_file,
            has_readable_packaging, quality_score, is_reference_grade,
            style_descriptor, needs_review, thumb_path, camera, lens,
            gps_lat, gps_lon, notes, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            asset.path,
            asset.sha256,
            asset.width,
            asset.height,
            iso(asset.captured_at),
            asset.pillar.value if asset.pillar else None,
            asset.location.value if asset.location else None,
            asset.sku.value if asset.sku else None,
            dumps(asset.subject_tags),
            int(asset.has_identifiable_person),
            int(asset.consent_on_file),
            int(asset.has_readable_packaging),
            asset.quality_score,
            int(asset.is_reference_grade),
            dumps(asset.style_descriptor.model_dump()) if asset.style_descriptor else None,
            int(asset.needs_review),
            asset.thumb_path,
            asset.camera,
            asset.lens,
            asset.gps_lat,
            asset.gps_lon,
            asset.notes,
            now,
            now,
        ),
    )
    conn.commit()
    return int(cursor.lastrowid)


def get_asset(conn: sqlite3.Connection, asset_id: int) -> Asset | None:
    row = conn.execute("SELECT * FROM assets WHERE id = ?", (asset_id,)).fetchone()
    return row_to_asset(row) if row else None


def get_asset_by_sha256(conn: sqlite3.Connection, sha256: str) -> Asset | None:
    row = conn.execute("SELECT * FROM assets WHERE sha256 = ?", (sha256,)).fetchone()
    return row_to_asset(row) if row else None


def get_asset_by_path(conn: sqlite3.Connection, path: str) -> Asset | None:
    row = conn.execute("SELECT * FROM assets WHERE path = ?", (path,)).fetchone()
    return row_to_asset(row) if row else None


def list_assets(
    conn: sqlite3.Connection,
    *,
    pillar: Pillar | str | None = None,
    sku: Sku | str | None = None,
    location: Location | str | None = None,
    needs_review: bool | None = None,
    reference_grade: bool | None = None,
    ids: Iterable[int] | None = None,
    limit: int | None = None,
) -> list[Asset]:
    clauses: list[str] = []
    params: list[Any] = []
    if pillar is not None:
        clauses.append("pillar = ?")
        params.append(str(pillar))
    if sku is not None:
        clauses.append("sku = ?")
        params.append(str(sku))
    if location is not None:
        clauses.append("location = ?")
        params.append(str(location))
    if needs_review is not None:
        clauses.append("needs_review = ?")
        params.append(int(needs_review))
    if reference_grade is not None:
        clauses.append("is_reference_grade = ?")
        params.append(int(reference_grade))
    if ids is not None:
        id_list = list(ids)
        if not id_list:
            return []
        clauses.append(f"id IN ({','.join('?' * len(id_list))})")
        params.extend(id_list)

    sql = "SELECT * FROM assets"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    # `quality_score IS NULL` primeiro evita depender de NULLS LAST (SQLite >= 3.30).
    sql += " ORDER BY quality_score IS NULL, quality_score DESC, id ASC"
    if limit:
        sql += " LIMIT ?"
        params.append(limit)
    return [row_to_asset(row) for row in conn.execute(sql, params)]


def update_asset_curation(conn: sqlite3.Connection, asset_id: int, **fields: Any) -> None:
    """Atualiza apenas campos de curadoria humana (inclui os de politica)."""
    unknown = set(fields) - set(ASSET_CURATION_FIELDS)
    if unknown:
        raise ValueError(f"campos nao editaveis por curadoria: {sorted(unknown)}")

    sets: list[str] = []
    params: list[Any] = []
    for key, value in fields.items():
        sets.append(f"{key} = ?")
        if key == "subject_tags":
            params.append(dumps(value))
        elif isinstance(value, bool):
            params.append(int(value))
        elif hasattr(value, "value"):
            params.append(value.value)
        else:
            params.append(value)
    if not sets:
        return
    sets.append("updated_at = ?")
    params.append(iso(utcnow()))
    params.append(asset_id)
    conn.execute(f"UPDATE assets SET {', '.join(sets)} WHERE id = ?", params)
    conn.commit()


def set_asset_reference_grade(conn: sqlite3.Connection, asset_id: int, value: bool) -> None:
    update_asset_curation(conn, asset_id, is_reference_grade=value)


def count_assets(conn: sqlite3.Connection) -> int:
    return int(conn.execute("SELECT COUNT(*) AS n FROM assets").fetchone()["n"])
