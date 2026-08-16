"""Acesso a dados. Converte linhas do SQLite em modelos Pydantic e vice-versa."""

from __future__ import annotations

import sqlite3
from typing import Any, Iterable

from .enums import (
    AspectRatio,
    JobStatus,
    Location,
    Pillar,
    ReviewStatus,
    RiskFlag,
    Sku,
    TemplateKind,
)
from .models import Asset, Generation, Job, StyleDescriptor, StyleDna, Template
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


# --------------------------------------------------------------------------- #
# templates
# --------------------------------------------------------------------------- #


def row_to_template(row: sqlite3.Row) -> Template:
    return Template(
        id=row["id"],
        name=row["name"],
        pillar=Pillar(row["pillar"]) if row["pillar"] else None,
        kind=TemplateKind(row["kind"]),
        body=row["body"],
        negative_prompt=row["negative_prompt"],
        requires_reference=bool(row["requires_reference"]),
        risk_flags=[RiskFlag(f) for f in (loads(row["risk_flags"], []) or [])],
        default_aspect_ratio=AspectRatio(row["default_aspect_ratio"]),
        variables=loads(row["variables"], {}) or {},
        notes=row["notes"],
    )


def upsert_template(conn: sqlite3.Connection, template: Template) -> int:
    """Grava por `name` (chave natural vinda do arquivo YAML)."""
    now = iso(utcnow())
    conn.execute(
        """
        INSERT INTO templates (
            name, pillar, kind, body, negative_prompt, requires_reference,
            risk_flags, default_aspect_ratio, variables, notes, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (name) DO UPDATE SET
            pillar = excluded.pillar,
            kind = excluded.kind,
            body = excluded.body,
            negative_prompt = excluded.negative_prompt,
            requires_reference = excluded.requires_reference,
            risk_flags = excluded.risk_flags,
            default_aspect_ratio = excluded.default_aspect_ratio,
            variables = excluded.variables,
            notes = excluded.notes,
            updated_at = excluded.updated_at
        """,
        (
            template.name,
            template.pillar.value if template.pillar else None,
            template.kind.value,
            template.body,
            template.negative_prompt,
            int(template.requires_reference),
            dumps([f.value for f in template.risk_flags]),
            template.default_aspect_ratio.value,
            dumps(template.variables),
            template.notes,
            now,
            now,
        ),
    )
    conn.commit()
    row = conn.execute("SELECT id FROM templates WHERE name = ?", (template.name,)).fetchone()
    return int(row["id"])


def get_template(conn: sqlite3.Connection, template_id: int) -> Template | None:
    row = conn.execute("SELECT * FROM templates WHERE id = ?", (template_id,)).fetchone()
    return row_to_template(row) if row else None


def get_template_by_name(conn: sqlite3.Connection, name: str) -> Template | None:
    row = conn.execute("SELECT * FROM templates WHERE name = ?", (name,)).fetchone()
    return row_to_template(row) if row else None


def list_templates(
    conn: sqlite3.Connection,
    *,
    pillar: Pillar | str | None = None,
    kind: TemplateKind | str | None = None,
) -> list[Template]:
    clauses: list[str] = []
    params: list[Any] = []
    if pillar is not None:
        clauses.append("pillar = ?")
        params.append(str(pillar))
    if kind is not None:
        clauses.append("kind = ?")
        params.append(str(kind))
    sql = "SELECT * FROM templates"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY name"
    return [row_to_template(row) for row in conn.execute(sql, params)]


# --------------------------------------------------------------------------- #
# style_dna
# --------------------------------------------------------------------------- #


def row_to_style_dna(row: sqlite3.Row) -> StyleDna:
    return StyleDna(
        id=row["id"],
        name=row["name"],
        pillar=Pillar(row["pillar"]) if row["pillar"] else None,
        source_asset_ids=loads(row["source_asset_ids"], []) or [],
        descriptor=StyleDescriptor(**(loads(row["descriptor"], {}) or {})),
        prompt_fragment=row["prompt_fragment"],
        created_at=parse_dt(row["created_at"]),
    )


def upsert_style_dna(conn: sqlite3.Connection, dna: StyleDna) -> int:
    conn.execute(
        """
        INSERT INTO style_dna (name, pillar, source_asset_ids, descriptor, prompt_fragment, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT (name) DO UPDATE SET
            pillar = excluded.pillar,
            source_asset_ids = excluded.source_asset_ids,
            descriptor = excluded.descriptor,
            prompt_fragment = excluded.prompt_fragment
        """,
        (
            dna.name,
            dna.pillar.value if dna.pillar else None,
            dumps(dna.source_asset_ids),
            dumps(dna.descriptor.model_dump()),
            dna.prompt_fragment,
            iso(dna.created_at or utcnow()),
        ),
    )
    conn.commit()
    row = conn.execute("SELECT id FROM style_dna WHERE name = ?", (dna.name,)).fetchone()
    return int(row["id"])


def get_style_dna(conn: sqlite3.Connection, dna_id: int) -> StyleDna | None:
    row = conn.execute("SELECT * FROM style_dna WHERE id = ?", (dna_id,)).fetchone()
    return row_to_style_dna(row) if row else None


def get_style_dna_by_name(conn: sqlite3.Connection, name: str) -> StyleDna | None:
    row = conn.execute("SELECT * FROM style_dna WHERE name = ?", (name,)).fetchone()
    return row_to_style_dna(row) if row else None


def list_style_dna(
    conn: sqlite3.Connection, *, pillar: Pillar | str | None = None
) -> list[StyleDna]:
    sql = "SELECT * FROM style_dna"
    params: list[Any] = []
    if pillar is not None:
        sql += " WHERE pillar = ?"
        params.append(str(pillar))
    sql += " ORDER BY name"
    return [row_to_style_dna(row) for row in conn.execute(sql, params)]


# --------------------------------------------------------------------------- #
# jobs
# --------------------------------------------------------------------------- #

JOB_UPDATABLE_FIELDS = (
    "resolved_prompt",
    "model",
    "aspect_ratio",
    "n",
    "status",
    "blocked_reason",
    "attempts",
    "cost_usd",
    "finished_at",
    "reference_asset_ids",
    "style_dna_id",
)


def row_to_job(row: sqlite3.Row) -> Job:
    return Job(
        id=row["id"],
        template_id=row["template_id"],
        style_dna_id=row["style_dna_id"],
        reference_asset_ids=loads(row["reference_asset_ids"], []) or [],
        resolved_prompt=row["resolved_prompt"],
        model=row["model"],
        aspect_ratio=AspectRatio(row["aspect_ratio"]),
        n=row["n"],
        status=JobStatus(row["status"]),
        blocked_reason=row["blocked_reason"],
        attempts=row["attempts"],
        cost_usd=row["cost_usd"],
        created_at=parse_dt(row["created_at"]),
        finished_at=parse_dt(row["finished_at"]),
    )


def insert_job(conn: sqlite3.Connection, job: Job) -> int:
    cursor = conn.execute(
        """
        INSERT INTO jobs (
            template_id, style_dna_id, reference_asset_ids, resolved_prompt, model,
            aspect_ratio, n, status, blocked_reason, attempts, cost_usd, created_at, finished_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job.template_id,
            job.style_dna_id,
            dumps(job.reference_asset_ids),
            job.resolved_prompt,
            job.model,
            job.aspect_ratio.value,
            job.n,
            job.status.value,
            job.blocked_reason,
            job.attempts,
            job.cost_usd,
            iso(job.created_at or utcnow()),
            iso(job.finished_at),
        ),
    )
    conn.commit()
    return int(cursor.lastrowid)


def get_job(conn: sqlite3.Connection, job_id: int) -> Job | None:
    row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    return row_to_job(row) if row else None


def list_jobs(
    conn: sqlite3.Connection,
    *,
    status: JobStatus | str | None = None,
    limit: int | None = None,
) -> list[Job]:
    sql = "SELECT * FROM jobs"
    params: list[Any] = []
    if status is not None:
        sql += " WHERE status = ?"
        params.append(str(status))
    sql += " ORDER BY id"
    if limit:
        sql += " LIMIT ?"
        params.append(limit)
    return [row_to_job(row) for row in conn.execute(sql, params)]


def update_job(conn: sqlite3.Connection, job_id: int, **fields: Any) -> None:
    unknown = set(fields) - set(JOB_UPDATABLE_FIELDS)
    if unknown:
        raise ValueError(f"campos de job nao atualizaveis: {sorted(unknown)}")
    sets: list[str] = []
    params: list[Any] = []
    for key, value in fields.items():
        sets.append(f"{key} = ?")
        if key == "reference_asset_ids":
            params.append(dumps(value))
        elif key == "finished_at":
            params.append(iso(value) if value else None)
        elif hasattr(value, "value"):
            params.append(value.value)
        else:
            params.append(value)
    if not sets:
        return
    params.append(job_id)
    conn.execute(f"UPDATE jobs SET {', '.join(sets)} WHERE id = ?", params)
    conn.commit()


def count_jobs(conn: sqlite3.Connection, status: JobStatus | str | None = None) -> int:
    if status is None:
        row = conn.execute("SELECT COUNT(*) AS n FROM jobs").fetchone()
    else:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM jobs WHERE status = ?", (str(status),)
        ).fetchone()
    return int(row["n"])


# --------------------------------------------------------------------------- #
# generations
# --------------------------------------------------------------------------- #


def row_to_generation(row: sqlite3.Row) -> Generation:
    return Generation(
        id=row["id"],
        job_id=row["job_id"],
        path=row["path"],
        sha256=row["sha256"],
        model=row["model"],
        prompt=row["prompt"],
        seed=row["seed"],
        cost_usd=row["cost_usd"],
        review_status=ReviewStatus(row["review_status"]),
        reject_reason=row["reject_reason"],
        disclosure_required=bool(row["disclosure_required"]),
        exported_variants=loads(row["exported_variants"], []) or [],
        created_at=parse_dt(row["created_at"]),
    )


def insert_generation(conn: sqlite3.Connection, generation: Generation) -> int:
    cursor = conn.execute(
        """
        INSERT INTO generations (
            job_id, path, sha256, model, prompt, seed, cost_usd, review_status,
            reject_reason, disclosure_required, exported_variants, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            generation.job_id,
            generation.path,
            generation.sha256,
            generation.model,
            generation.prompt,
            generation.seed,
            generation.cost_usd,
            generation.review_status.value,
            generation.reject_reason,
            int(generation.disclosure_required),
            dumps(generation.exported_variants),
            iso(generation.created_at or utcnow()),
        ),
    )
    conn.commit()
    return int(cursor.lastrowid)


def get_generation(conn: sqlite3.Connection, generation_id: int) -> Generation | None:
    row = conn.execute("SELECT * FROM generations WHERE id = ?", (generation_id,)).fetchone()
    return row_to_generation(row) if row else None


def list_generations(
    conn: sqlite3.Connection,
    *,
    review_status: ReviewStatus | str | None = None,
    job_id: int | None = None,
    limit: int | None = None,
) -> list[Generation]:
    clauses: list[str] = []
    params: list[Any] = []
    if review_status is not None:
        clauses.append("review_status = ?")
        params.append(str(review_status))
    if job_id is not None:
        clauses.append("job_id = ?")
        params.append(job_id)
    sql = "SELECT * FROM generations"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY id"
    if limit:
        sql += " LIMIT ?"
        params.append(limit)
    return [row_to_generation(row) for row in conn.execute(sql, params)]


def set_review_status(
    conn: sqlite3.Connection,
    generation_id: int,
    status: ReviewStatus | str,
    reject_reason: str | None = None,
) -> None:
    conn.execute(
        "UPDATE generations SET review_status = ?, reject_reason = ? WHERE id = ?",
        (str(status), reject_reason, generation_id),
    )
    conn.commit()


def set_focal_point(
    conn: sqlite3.Connection, generation_id: int, x: float | None, y: float | None
) -> None:
    """Ponto focal relativo (0..1) definido na UI; guia o recorte inteligente."""
    if x is not None and not 0.0 <= x <= 1.0:
        raise ValueError("focal_x deve estar entre 0 e 1")
    if y is not None and not 0.0 <= y <= 1.0:
        raise ValueError("focal_y deve estar entre 0 e 1")
    conn.execute(
        "UPDATE generations SET focal_x = ?, focal_y = ? WHERE id = ?",
        (x, y, generation_id),
    )
    conn.commit()


def get_focal_point(
    conn: sqlite3.Connection, generation_id: int
) -> tuple[float, float] | None:
    row = conn.execute(
        "SELECT focal_x, focal_y FROM generations WHERE id = ?", (generation_id,)
    ).fetchone()
    if not row or row["focal_x"] is None or row["focal_y"] is None:
        return None
    return float(row["focal_x"]), float(row["focal_y"])


def set_exported_variants(
    conn: sqlite3.Connection, generation_id: int, variants: list[str]
) -> None:
    conn.execute(
        "UPDATE generations SET exported_variants = ? WHERE id = ?",
        (dumps(variants), generation_id),
    )
    conn.commit()


def cost_rows(
    conn: sqlite3.Connection, since: str | None = None, until: str | None = None
) -> list[sqlite3.Row]:
    """Linhas cruas de custo por geracao, para os relatorios da fase 5."""
    sql = (
        "SELECT g.id, g.created_at, g.model, g.cost_usd, g.review_status,"
        "       g.job_id, t.name AS template_name, t.pillar AS pillar"
        "  FROM generations g"
        "  JOIN jobs j ON j.id = g.job_id"
        "  JOIN templates t ON t.id = j.template_id"
    )
    clauses: list[str] = []
    params: list[Any] = []
    if since:
        clauses.append("g.created_at >= ?")
        params.append(since)
    if until:
        clauses.append("g.created_at <= ?")
        params.append(until)
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY g.created_at"
    return list(conn.execute(sql, params))


def total_cost(conn: sqlite3.Connection, since: str | None = None) -> float:
    sql = "SELECT COALESCE(SUM(cost_usd), 0.0) AS total FROM generations"
    params: list[Any] = []
    if since:
        sql += " WHERE created_at >= ?"
        params.append(since)
    return float(conn.execute(sql, params).fetchone()["total"])
