"""Conexao SQLite e migracoes versionadas.

Migracoes sao arquivos `.sql` numerados em `cie/migrations/`, aplicados em ordem
lexicografica e registrados em `schema_migrations`. O runner e idempotente.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .config import Settings
from .utils import iso, utcnow

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def connect(db_path: Path | str) -> sqlite3.Connection:
    db_path = Path(db_path)
    if str(db_path) != ":memory:":
        db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate(conn: sqlite3.Connection) -> list[str]:
    """Aplica migracoes pendentes e devolve os nomes das que rodaram agora."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS schema_migrations ("
        " version TEXT PRIMARY KEY, applied_at TEXT NOT NULL)"
    )
    conn.commit()
    already = {row["version"] for row in conn.execute("SELECT version FROM schema_migrations")}

    applied_now: list[str] = []
    for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
        if path.name in already:
            continue
        conn.executescript(path.read_text(encoding="utf-8"))
        conn.execute(
            "INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)",
            (path.name, iso(utcnow())),
        )
        conn.commit()
        applied_now.append(path.name)
    return applied_now


def open_db(settings: Settings) -> sqlite3.Connection:
    """Abre o banco do projeto ja migrado."""
    settings.ensure_dirs()
    conn = connect(settings.db_path)
    migrate(conn)
    return conn


def applied_migrations(conn: sqlite3.Connection) -> list[tuple[str, str]]:
    try:
        rows = conn.execute(
            "SELECT version, applied_at FROM schema_migrations ORDER BY version"
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    return [(row["version"], row["applied_at"]) for row in rows]


def pending_migrations(conn: sqlite3.Connection) -> list[str]:
    already = {version for version, _ in applied_migrations(conn)}
    return [p.name for p in sorted(MIGRATIONS_DIR.glob("*.sql")) if p.name not in already]
