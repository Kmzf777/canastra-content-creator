"""Leitura de imagem, EXIF, thumbnails e score de qualidade.

Tudo local: nenhuma chamada de rede, nenhum modelo de ML. O `quality_score` e
uma heuristica classica (variancia do Laplaciano + histograma + resolucao),
suficiente para separar "serve de referencia" de "nao serve".
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageFilter, ImageStat

from .utils import clamp

#: Extensoes que a ingestao aceita varrer.
RASTER_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}
HEIC_EXTENSIONS = {".heic", ".heif"}
RAW_EXTENSIONS = {".cr2", ".cr3", ".nef", ".arw", ".dng", ".raf", ".orf", ".rw2", ".srw"}
SUPPORTED_EXTENSIONS = RASTER_EXTENSIONS | HEIC_EXTENSIONS | RAW_EXTENSIONS

# Tags EXIF (numeros crus para nao depender de tabela de nomes do Pillow).
_TAG_MAKE = 271
_TAG_MODEL = 272
_TAG_DATETIME = 306
_IFD_EXIF = 0x8769
_IFD_GPS = 0x8825
_TAG_DATETIME_ORIGINAL = 36867
_TAG_LENS_MODEL = 42036

_heic_ready: bool | None = None


def register_optional_decoders() -> bool:
    """Registra o decoder HEIC se `pillow-heif` estiver instalado. Idempotente."""
    global _heic_ready
    if _heic_ready is None:
        try:
            import pillow_heif  # type: ignore

            pillow_heif.register_heif_opener()
            _heic_ready = True
        except Exception:  # pragma: no cover - depende do extra opcional
            _heic_ready = False
    return _heic_ready


def sha256_file(path: Path | str, chunk_size: int = 1 << 20) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_image(path: Path | str) -> Image.Image | None:
    """Abre a imagem, ou devolve None quando nao ha decoder (tipico de RAW)."""
    register_optional_decoders()
    try:
        image = Image.open(path)
        image.load()
        return image
    except Exception:
        return None


# --------------------------------------------------------------------------- #
# EXIF
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ExifData:
    captured_at: datetime | None = None
    camera: str | None = None
    lens: str | None = None
    gps_lat: float | None = None
    gps_lon: float | None = None


def _parse_exif_datetime(raw: str | None) -> datetime | None:
    if not raw:
        return None
    for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(str(raw).strip(), fmt)
        except ValueError:
            continue
    return None


def _dms_to_degrees(values, ref: str | None) -> float | None:
    try:
        degrees, minutes, seconds = (float(v) for v in values)
    except (TypeError, ValueError):
        return None
    result = degrees + minutes / 60 + seconds / 3600
    if ref and str(ref).upper() in {"S", "W"}:
        result = -result
    return result


def read_exif(image: Image.Image) -> ExifData:
    try:
        exif = image.getexif()
    except Exception:
        return ExifData()
    if not exif:
        return ExifData()

    make = exif.get(_TAG_MAKE)
    model = exif.get(_TAG_MODEL)
    camera = " ".join(str(part).strip() for part in (make, model) if part) or None

    lens = None
    captured_at = _parse_exif_datetime(exif.get(_TAG_DATETIME))
    try:
        exif_ifd = exif.get_ifd(_IFD_EXIF)
    except Exception:
        exif_ifd = {}
    if exif_ifd:
        captured_at = _parse_exif_datetime(exif_ifd.get(_TAG_DATETIME_ORIGINAL)) or captured_at
        lens_value = exif_ifd.get(_TAG_LENS_MODEL)
        lens = str(lens_value).strip() if lens_value else None

    lat = lon = None
    try:
        gps = exif.get_ifd(_IFD_GPS)
    except Exception:
        gps = {}
    if gps:
        lat = _dms_to_degrees(gps.get(2), gps.get(1))
        lon = _dms_to_degrees(gps.get(4), gps.get(3))

    return ExifData(captured_at=captured_at, camera=camera, lens=lens, gps_lat=lat, gps_lon=lon)


# --------------------------------------------------------------------------- #
# Qualidade
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class QualityBreakdown:
    sharpness: float
    exposure: float
    resolution: float
    score: int

    def as_dict(self) -> dict[str, float | int]:
        return {
            "sharpness": round(self.sharpness, 1),
            "exposure": round(self.exposure, 1),
            "resolution": round(self.resolution, 1),
            "score": self.score,
        }


#: Kernel Laplaciano 3x3. offset=128 preserva a parte negativa da resposta.
_LAPLACIAN = ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], scale=1, offset=128)


def _sharpness_score(gray: Image.Image) -> float:
    # Reamostra para 1024px para que o score nao dependa da resolucao do arquivo.
    small = gray.copy()
    small.thumbnail((1024, 1024))
    variance = ImageStat.Stat(small.filter(_LAPLACIAN)).var[0]
    # Escala logaritmica: var ~6 e borrado, var ~300 e bem nitido.
    low, high = math.log10(6.0), math.log10(301.0)
    return clamp((math.log10(variance + 1.0) - low) / (high - low) * 100.0)


def _exposure_score(gray: Image.Image) -> float:
    histogram = gray.histogram()
    total = sum(histogram) or 1
    clipped = (sum(histogram[0:4]) + sum(histogram[252:256])) / total
    contrast = clamp(ImageStat.Stat(gray).stddev[0] / 60.0 * 100.0)
    # Estouro de pretos/brancos derruba a nota, com teto para nao zerar tudo.
    penalty = clamp(clipped * 400.0, 0.0, 60.0)
    return clamp(contrast - penalty)


def _resolution_score(width: int, height: int) -> float:
    min_side = min(width, height)
    if min_side <= 600:
        return 0.0
    if min_side >= 2000:
        return 100.0
    return (min_side - 600) / (2000 - 600) * 100.0


def compute_quality(image: Image.Image) -> QualityBreakdown:
    gray = image.convert("L")
    sharpness = _sharpness_score(gray)
    exposure = _exposure_score(gray)
    resolution = _resolution_score(image.width, image.height)
    score = int(round(0.50 * sharpness + 0.25 * exposure + 0.25 * resolution))
    return QualityBreakdown(sharpness, exposure, resolution, score)


#: Uma foto so vira referencia se for nitida o bastante E tiver resolucao util.
REFERENCE_MIN_SCORE = 70
REFERENCE_MIN_SIDE = 1200


def is_reference_grade(quality: QualityBreakdown | None, width: int | None, height: int | None) -> bool:
    if quality is None or width is None or height is None:
        return False
    return quality.score >= REFERENCE_MIN_SCORE and min(width, height) >= REFERENCE_MIN_SIDE


# --------------------------------------------------------------------------- #
# Thumbnails
# --------------------------------------------------------------------------- #


def make_thumbnail(image: Image.Image, dest: Path, max_side: int = 640) -> Path:
    """Gera thumbnail JPEG. So derivados saem do diretorio da base original."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    thumb = image.copy()
    if thumb.mode not in ("RGB", "L"):
        thumb = thumb.convert("RGB")
    thumb.thumbnail((max_side, max_side))
    thumb.save(dest, format="JPEG", quality=85, optimize=True)
    return dest
