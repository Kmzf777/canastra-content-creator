-- Esquema inicial do CIE.
-- Booleanos sao INTEGER 0/1; campos JSON sao TEXT com JSON serializado.

CREATE TABLE assets (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    path                    TEXT    NOT NULL UNIQUE,
    sha256                  TEXT    NOT NULL UNIQUE,
    width                   INTEGER,
    height                  INTEGER,
    captured_at             TEXT,
    pillar                  TEXT,
    location                TEXT,
    sku                     TEXT,
    subject_tags            TEXT    NOT NULL DEFAULT '[]',
    -- Defaults restritivos: pessoa presumida presente, consentimento ausente.
    has_identifiable_person INTEGER NOT NULL DEFAULT 1,
    consent_on_file         INTEGER NOT NULL DEFAULT 0,
    has_readable_packaging  INTEGER NOT NULL DEFAULT 0,
    quality_score           INTEGER,
    is_reference_grade      INTEGER NOT NULL DEFAULT 0,
    style_descriptor        TEXT,
    needs_review            INTEGER NOT NULL DEFAULT 1,
    thumb_path              TEXT,
    camera                  TEXT,
    lens                    TEXT,
    gps_lat                 REAL,
    gps_lon                 REAL,
    notes                   TEXT,
    created_at              TEXT    NOT NULL,
    updated_at              TEXT    NOT NULL
);

CREATE INDEX idx_assets_pillar ON assets (pillar);
CREATE INDEX idx_assets_sku ON assets (sku);
CREATE INDEX idx_assets_location ON assets (location);
CREATE INDEX idx_assets_reference ON assets (is_reference_grade);

CREATE TABLE style_dna (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    name             TEXT    NOT NULL UNIQUE,
    pillar           TEXT,
    source_asset_ids TEXT    NOT NULL DEFAULT '[]',
    descriptor       TEXT    NOT NULL,
    prompt_fragment  TEXT    NOT NULL DEFAULT '',
    created_at       TEXT    NOT NULL
);

CREATE TABLE templates (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    name                 TEXT    NOT NULL UNIQUE,
    pillar               TEXT,
    kind                 TEXT    NOT NULL,
    body                 TEXT    NOT NULL,
    negative_prompt      TEXT    NOT NULL DEFAULT '',
    requires_reference   INTEGER NOT NULL DEFAULT 0,
    risk_flags           TEXT    NOT NULL DEFAULT '[]',
    default_aspect_ratio TEXT    NOT NULL DEFAULT '1:1',
    variables            TEXT    NOT NULL DEFAULT '{}',
    notes                TEXT,
    created_at           TEXT    NOT NULL,
    updated_at           TEXT    NOT NULL
);

CREATE TABLE jobs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    template_id         INTEGER NOT NULL REFERENCES templates (id),
    style_dna_id        INTEGER REFERENCES style_dna (id),
    reference_asset_ids TEXT    NOT NULL DEFAULT '[]',
    resolved_prompt     TEXT    NOT NULL DEFAULT '',
    model               TEXT    NOT NULL DEFAULT '',
    aspect_ratio        TEXT    NOT NULL DEFAULT '1:1',
    n                   INTEGER NOT NULL DEFAULT 1,
    status              TEXT    NOT NULL DEFAULT 'queued',
    blocked_reason      TEXT,
    attempts            INTEGER NOT NULL DEFAULT 0,
    cost_usd            REAL    NOT NULL DEFAULT 0.0,
    created_at          TEXT    NOT NULL,
    finished_at         TEXT
);

CREATE INDEX idx_jobs_status ON jobs (status);

CREATE TABLE generations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id              INTEGER NOT NULL REFERENCES jobs (id),
    path                TEXT    NOT NULL,
    sha256              TEXT    NOT NULL,
    model               TEXT    NOT NULL,
    prompt              TEXT    NOT NULL,
    seed                INTEGER,
    cost_usd            REAL    NOT NULL DEFAULT 0.0,
    review_status       TEXT    NOT NULL DEFAULT 'pending',
    reject_reason       TEXT,
    -- Rotulagem de conteudo de IA (Instagram/Meta): default exige disclosure.
    disclosure_required INTEGER NOT NULL DEFAULT 1,
    exported_variants   TEXT    NOT NULL DEFAULT '[]',
    created_at          TEXT    NOT NULL
);

CREATE INDEX idx_generations_job ON generations (job_id);
CREATE INDEX idx_generations_review ON generations (review_status);
