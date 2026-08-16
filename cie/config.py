"""Configuracao e layout de diretorios.

Regra dura: a chave da xAI vem exclusivamente do ambiente (carregado de `.env`
via python-dotenv) e nunca e guardada em atributo, repr, log ou mensagem de erro.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_XAI_BASE_URL = "https://api.x.ai/v1"

#: Raiz do projeto (onde vivem pyproject.toml, templates/, assets/).
PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    """Caminhos derivados de CIE_HOME. Nada aqui guarda segredo."""

    root: Path
    home: Path

    @property
    def db_path(self) -> Path:
        return self.home / "cie.db"

    @property
    def thumbs_dir(self) -> Path:
        return self.home / "thumbs"

    @property
    def generations_dir(self) -> Path:
        return self.home / "generations"

    @property
    def probe_dir(self) -> Path:
        return self.home / "probe"

    @property
    def templates_dir(self) -> Path:
        return self.root / "templates"

    @property
    def cutouts_dir(self) -> Path:
        return self.root / "assets" / "cutouts"

    @property
    def export_dir(self) -> Path:
        return self.root / "export"

    @property
    def xai_base_url(self) -> str:
        return os.environ.get("CIE_XAI_BASE_URL", DEFAULT_XAI_BASE_URL)

    def ensure_dirs(self) -> None:
        for path in (self.home, self.thumbs_dir, self.generations_dir):
            path.mkdir(parents=True, exist_ok=True)


def get_settings(root: Path | str | None = None) -> Settings:
    """Monta Settings. `root` existe para os testes apontarem para tmp_path."""
    load_dotenv(override=False)
    resolved_root = Path(root).resolve() if root is not None else PROJECT_ROOT
    home_env = os.environ.get("CIE_HOME")
    if home_env:
        home = Path(home_env)
        home = home if home.is_absolute() else resolved_root / home
    else:
        home = resolved_root / ".cie"
    return Settings(root=resolved_root, home=home.resolve())


def get_api_key() -> str | None:
    """Le a chave sob demanda. Nunca retorne isto para log ou mensagem de erro."""
    load_dotenv(override=False)
    key = os.environ.get("XAI_API_KEY", "").strip()
    return key or None


def require_api_key() -> str:
    key = get_api_key()
    if not key:
        # Mensagem deliberadamente sem eco de valor algum.
        raise RuntimeError(
            "XAI_API_KEY ausente. Defina no ambiente ou em .env "
            "(veja .env.example). A chave nunca e impressa pelo CIE."
        )
    return key


def redact(text: str) -> str:
    """Remove qualquer ocorrencia da chave de um texto antes de logar/persistir."""
    key = os.environ.get("XAI_API_KEY", "").strip()
    if key and key in text:
        text = text.replace(key, "***REDACTED***")
    return text
