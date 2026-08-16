from __future__ import annotations

from cie.db import applied_migrations, connect, migrate, pending_migrations

EXPECTED_TABLES = {"assets", "style_dna", "templates", "jobs", "generations"}


def test_migrate_creates_all_tables(settings):
    conn = connect(settings.db_path)
    applied = migrate(conn)

    assert applied, "primeira migracao deveria aplicar pelo menos um arquivo"
    tables = {
        row["name"]
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    }
    assert EXPECTED_TABLES <= tables


def test_migrate_is_idempotent(settings):
    conn = connect(settings.db_path)
    first = migrate(conn)
    second = migrate(conn)

    assert first != []
    assert second == []
    assert pending_migrations(conn) == []
    assert len(applied_migrations(conn)) == len(first)


def test_restrictive_defaults_live_in_the_schema(conn):
    """Mesmo um INSERT cru precisa nascer restritivo."""
    conn.execute(
        "INSERT INTO assets (path, sha256, subject_tags, created_at, updated_at)"
        " VALUES ('/x.jpg', 'abc', '[]', '2026-01-01', '2026-01-01')"
    )
    row = conn.execute("SELECT * FROM assets WHERE sha256 = 'abc'").fetchone()

    assert row["has_identifiable_person"] == 1
    assert row["consent_on_file"] == 0
    assert row["needs_review"] == 1
    assert row["is_reference_grade"] == 0


def test_generations_default_requires_disclosure(conn):
    conn.execute(
        "INSERT INTO templates (name, kind, body, created_at, updated_at)"
        " VALUES ('t', 'scene', 'b', '2026-01-01', '2026-01-01')"
    )
    conn.execute(
        "INSERT INTO jobs (template_id, created_at) VALUES (1, '2026-01-01')"
    )
    conn.execute(
        "INSERT INTO generations (job_id, path, sha256, model, prompt, created_at)"
        " VALUES (1, '/g.png', 'ff', 'grok', 'p', '2026-01-01')"
    )
    row = conn.execute("SELECT * FROM generations").fetchone()

    assert row["disclosure_required"] == 1
    assert row["review_status"] == "pending"
