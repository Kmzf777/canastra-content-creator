"""Fixtures compartilhadas. Nenhum teste toca a API real."""

from __future__ import annotations

import random
import sqlite3
from pathlib import Path

import pytest
from PIL import Image, ImageFilter

from cie.config import Settings, get_settings
from cie.db import connect, migrate


@pytest.fixture
def settings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Settings:
    monkeypatch.setenv("CIE_HOME", str(tmp_path / ".cie"))
    monkeypatch.delenv("XAI_API_KEY", raising=False)
    resolved = get_settings(root=tmp_path)
    resolved.ensure_dirs()
    return resolved


@pytest.fixture
def conn(settings: Settings) -> sqlite3.Connection:
    connection = connect(settings.db_path)
    migrate(connection)
    yield connection
    connection.close()


def make_photo(
    path: Path,
    size: tuple[int, int] = (1600, 1200),
    *,
    blur: float = 0.0,
    seed: int = 7,
) -> Path:
    """Cria uma foto sintetica com ruido (nitida) ou borrada."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    image = Image.new("RGB", size)
    # Ruido em blocos: barato de gerar e com microcontraste suficiente para
    # a variancia do Laplaciano separar nitido de borrado.
    block = 4
    pixels = image.load()
    for y in range(0, size[1], block):
        for x in range(0, size[0], block):
            color = (rng.randrange(256), rng.randrange(256), rng.randrange(256))
            for dy in range(block):
                for dx in range(block):
                    if x + dx < size[0] and y + dy < size[1]:
                        pixels[x + dx, y + dy] = color
    if blur:
        image = image.filter(ImageFilter.GaussianBlur(blur))
    image.save(path, format="JPEG", quality=95)
    return path


@pytest.fixture
def photo_factory():
    return make_photo
