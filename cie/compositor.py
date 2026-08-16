"""Composicao local: produto real sobre fundo gerado.

Trilha hibrida do CIE. Quando o template e `product_shot` e existe recorte do SKU
em `assets/cutouts/`, o rotulo nao passa pela difusao: so o fundo e gerado, e o
produto real e colado por cima com Pillow. Assim o texto da embalagem continua
sendo o texto fotografado - a IA estende o real, nao o inventa.

Tudo aqui e offline e deterministico: nenhuma chamada de rede, nenhum modelo.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageDraw, ImageFilter

from .config import Settings
from .enums import Sku
from .errors import CieError
from .imaging import load_image
from .naming import SKU_TOKENS
from .utils import normalize_token

#: Formatos aceitos como recorte: precisam carregar canal alfa.
CUTOUT_EXTENSIONS = {".png", ".webp"}
JPEG_EXTENSIONS = {".jpg", ".jpeg"}

#: Ancoras suportadas por `compose_product`.
ANCHORS = ("center", "center-bottom", "left-bottom", "right-bottom")

#: Alfa abaixo disto conta como transparente (franja de recorte, nao produto).
ALPHA_TRIM_THRESHOLD = 8

#: Fracao inferior do produto que define onde ele "encosta no chao".
CONTACT_BAND_RATIO = 0.12

#: Cor de fundo da folha de contato e espacamento entre celulas.
CONTACT_SHEET_BG = (245, 243, 240)
CONTACT_SHEET_PAD = 12


@dataclass
class CompositionResult:
    """Geometria e proveniencia de uma composicao local."""

    path: Path
    cutout_path: Path | None
    background_path: Path | None
    scale: float
    position: tuple[int, int]
    size: tuple[int, int]

    def as_provenance(self) -> dict[str, Any]:
        """Bloco pronto para o manifesto de exportacao (JSON-serializavel)."""
        return {
            "method": "local_composition",
            "engine": "pillow",
            "output": str(self.path),
            "background": str(self.background_path) if self.background_path else None,
            "cutout": str(self.cutout_path) if self.cutout_path else None,
            "scale": round(self.scale, 4),
            "position": [self.position[0], self.position[1]],
            "size": [self.size[0], self.size[1]],
            # O produto e foto real recortada; o fundo continua sendo gerado por IA,
            # entao a rotulagem de IA permanece obrigatoria.
            "product_is_real": True,
            "background_is_generated": True,
            "disclosure_required": True,
        }


# --------------------------------------------------------------------------- #
# alfa
# --------------------------------------------------------------------------- #


def has_alpha(image: Image.Image) -> bool:
    return image.mode in ("RGBA", "LA", "PA") or "transparency" in image.info


def _validated_rgba(image: Image.Image, origin: str) -> Image.Image:
    """Converte para RGBA exigindo alfa util: nem ausente, nem opaco, nem vazio."""
    if not has_alpha(image):
        raise CieError(
            f"recorte sem canal alfa: {origin}. O compositor precisa de PNG ja "
            "recortado, com fundo transparente, em assets/cutouts/."
        )
    rgba = image.convert("RGBA")
    low, high = rgba.getchannel("A").getextrema()
    if low >= 255:
        raise CieError(
            f"recorte com alfa totalmente opaco: {origin}. Sem silhueta nao ha "
            "recorte - reexporte o PNG com o fundo apagado."
        )
    if high == 0:
        raise CieError(f"recorte totalmente transparente: {origin}")
    return rgba


def load_cutout(path: Path | str) -> Image.Image:
    """Abre um recorte PNG/WebP como RGBA. Levanta CieError se o alfa nao servir."""
    path = Path(path)
    try:
        image = Image.open(path)
        image.load()
    except (OSError, ValueError) as exc:
        raise CieError(f"recorte ilegivel: {path} ({exc})") from exc
    try:
        return _validated_rgba(image, str(path))
    finally:
        image.close()


def trim_transparent_border(image: Image.Image) -> Image.Image:
    """Corta a moldura transparente para que `scale` valha sobre o produto, nao sobre o PNG."""
    rgba = image if image.mode == "RGBA" else image.convert("RGBA")
    alpha = rgba.getchannel("A")
    solid = alpha.point(lambda v: 255 if v > ALPHA_TRIM_THRESHOLD else 0)
    bbox = solid.getbbox()
    if bbox is None or bbox == (0, 0, rgba.width, rgba.height):
        return rgba.copy()
    return rgba.crop(bbox)


# --------------------------------------------------------------------------- #
# catalogo de recortes
# --------------------------------------------------------------------------- #


def _name_matches_sku(path: Path, wanted: str) -> bool:
    stem = normalize_token(path.stem)
    for token in (t for t in re.split(r"[^A-Z0-9]+", stem) if t):
        if token == wanted:
            return True
        # Reaproveita o vocabulario da ingestao: 'capsulas' e 'dripcoffee' tambem valem.
        mapped = SKU_TOKENS.get(token)
        if mapped is not None and normalize_token(mapped.value) == wanted:
            return True
    return wanted in stem


def _open_header(path: Path) -> Image.Image | None:
    """Abre so o cabecalho (sem decodificar pixels) para ler modo e dimensoes."""
    try:
        return Image.open(path)
    except (OSError, ValueError):
        return None


def _looks_like_cutout(path: Path) -> bool:
    image = _open_header(path)
    if image is None:
        return False
    try:
        return has_alpha(image)
    finally:
        image.close()


def _pixel_area(path: Path) -> int:
    image = _open_header(path)
    if image is None:
        return 0
    try:
        return image.width * image.height
    finally:
        image.close()


def list_cutouts(settings: Settings, sku: Sku | str | None = None) -> list[Path]:
    """Recortes disponiveis em assets/cutouts/, opcionalmente filtrados por SKU."""
    directory = settings.cutouts_dir
    if not directory.is_dir():
        return []
    wanted = normalize_token(str(sku)) if sku is not None else None

    found: list[Path] = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in CUTOUT_EXTENSIONS:
            continue
        if any(part.startswith(".") for part in path.relative_to(directory).parts):
            continue
        if wanted is not None and not _name_matches_sku(path, wanted):
            continue
        if not _looks_like_cutout(path):
            continue
        found.append(path)
    return found


def suggest_cutout_for_sku(settings: Settings, sku: Sku | str) -> Path | None:
    """Melhor recorte do SKU: mais pixel aguenta mais reducao sem serrilhar."""
    candidates = list_cutouts(settings, sku)
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: (-_pixel_area(p), p.name))[0]


# --------------------------------------------------------------------------- #
# composicao
# --------------------------------------------------------------------------- #


def _coerce_background(value: Path | str | Image.Image) -> tuple[Image.Image, Path | None]:
    if isinstance(value, Image.Image):
        return value.convert("RGBA"), None
    path = Path(value)
    image = load_image(path)
    if image is None:
        raise CieError(f"fundo ilegivel: {path}")
    try:
        return image.convert("RGBA"), path
    finally:
        image.close()


def _coerce_cutout(value: Path | str | Image.Image) -> tuple[Image.Image, Path | None]:
    if isinstance(value, Image.Image):
        return _validated_rgba(value, "<imagem em memoria>"), None
    path = Path(value)
    return load_cutout(path), path


def _clamp_int(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def _contact_span(alpha: Image.Image) -> tuple[int, int]:
    """Largura em que o produto toca o chao: bbox do alfa na faixa inferior."""
    band = max(1, int(round(alpha.height * CONTACT_BAND_RATIO)))
    strip = alpha.crop((0, alpha.height - band, alpha.width, alpha.height))
    bbox = strip.point(lambda v: 255 if v > ALPHA_TRIM_THRESHOLD else 0).getbbox()
    if bbox is None:
        return 0, alpha.width
    return bbox[0], bbox[2]


def _with_contact_shadow(
    canvas: Image.Image,
    product: Image.Image,
    position: tuple[int, int],
    *,
    opacity: float,
    blur: float,
) -> Image.Image:
    """Elipse suave derivada da silhueta, para o produto nao flutuar sobre o fundo."""
    left, right = _contact_span(product.getchannel("A"))
    span = max(right - left, 1)
    x, y = position
    center_x = x + (left + right) / 2.0
    baseline = y + product.height
    half_w = span * 0.62
    half_h = max(4.0, span * 0.13)
    box = (
        int(round(center_x - half_w)),
        int(round(baseline - half_h)),
        int(round(center_x + half_w)),
        int(round(baseline + half_h)),
    )

    mask = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(mask).ellipse(box, fill=int(round(255 * max(0.0, min(1.0, opacity)))))
    if blur > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(blur))
    # Camada preta cuja unica informacao e o alfa da mascara.
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.putalpha(mask)
    return Image.alpha_composite(canvas, layer)


def _save_canvas(canvas: Image.Image, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    suffix = dest.suffix.lower()
    if suffix in JPEG_EXTENSIONS:
        canvas.convert("RGB").save(dest, format="JPEG", quality=92, optimize=True)
    elif suffix == ".png":
        canvas.save(dest, format="PNG")
    else:
        canvas.save(dest)


def compose_product(
    background: Path | str | Image.Image,
    cutout: Path | str | Image.Image,
    *,
    dest: Path | str,
    scale: float = 0.55,
    anchor: str = "center-bottom",
    margin_ratio: float = 0.08,
    shadow: bool = True,
    shadow_opacity: float = 0.35,
    shadow_blur: float = 18,
) -> CompositionResult:
    """Cola o recorte real sobre o fundo gerado e grava em `dest`.

    `scale` e a fracao da altura do fundo que o produto ocupa; a proporcao do
    produto nunca muda, e a margem pedida e sempre respeitada (se preciso, o
    produto encolhe ate caber).
    """
    if anchor not in ANCHORS:
        raise CieError(f"anchor invalido: {anchor!r}; use um de: {', '.join(ANCHORS)}")
    if not 0.0 < scale <= 1.0:
        raise CieError(f"scale fora de 0 < scale <= 1: {scale}")
    if not 0.0 <= margin_ratio < 0.5:
        raise CieError(f"margin_ratio fora de 0 <= margin < 0.5: {margin_ratio}")

    dest = Path(dest)
    canvas, background_path = _coerce_background(background)
    product, cutout_path = _coerce_cutout(cutout)
    product = trim_transparent_border(product)

    margin_x = int(round(canvas.width * margin_ratio))
    margin_y = int(round(canvas.height * margin_ratio))
    available_w = max(1, canvas.width - 2 * margin_x)
    available_h = max(1, canvas.height - 2 * margin_y)

    # Um unico fator para os dois eixos: esticar o produto falsificaria a embalagem.
    factor = min(
        canvas.height * scale / product.height,
        available_w / product.width,
        available_h / product.height,
    )
    target_w = max(1, int(round(product.width * factor)))
    target_h = max(1, int(round(product.height * factor)))
    product = product.resize((target_w, target_h), Image.LANCZOS)

    bottom = canvas.height - margin_y
    if anchor == "center":
        x = (canvas.width - target_w) // 2
        y = (canvas.height - target_h) // 2
    elif anchor == "center-bottom":
        x = (canvas.width - target_w) // 2
        y = bottom - target_h
    elif anchor == "left-bottom":
        x = margin_x
        y = bottom - target_h
    else:  # right-bottom
        x = canvas.width - margin_x - target_w
        y = bottom - target_h
    x = _clamp_int(x, 0, canvas.width - target_w)
    y = _clamp_int(y, 0, canvas.height - target_h)

    if shadow and shadow_opacity > 0:
        canvas = _with_contact_shadow(
            canvas, product, (x, y), opacity=shadow_opacity, blur=shadow_blur
        )
    canvas.alpha_composite(product, (x, y))
    _save_canvas(canvas, dest)

    return CompositionResult(
        path=dest,
        cutout_path=cutout_path,
        background_path=background_path,
        # Escala efetiva: pode ser menor que a pedida se a margem apertou.
        scale=target_h / canvas.height,
        position=(x, y),
        size=(target_w, target_h),
    )


# --------------------------------------------------------------------------- #
# folha de contato
# --------------------------------------------------------------------------- #


def contact_sheet(
    paths: Iterable[Path | str],
    dest: Path | str,
    columns: int = 4,
    thumb: int = 320,
) -> Path:
    """Grade de miniaturas para a revisao humana bater o olho em um arquivo so."""
    if columns < 1:
        raise CieError(f"columns precisa ser >= 1: {columns}")
    if thumb < 16:
        raise CieError(f"thumb precisa ser >= 16: {thumb}")

    dest = Path(dest)
    tiles: list[Image.Image] = []
    for candidate in paths:
        image = load_image(Path(candidate))
        if image is None:
            continue
        tile = image.convert("RGB")
        tile.thumbnail((thumb, thumb))
        tiles.append(tile)
        image.close()

    if not tiles:
        raise CieError("nenhuma imagem legivel para a folha de contato")

    columns = min(columns, len(tiles))
    rows = math.ceil(len(tiles) / columns)
    cell = thumb + CONTACT_SHEET_PAD
    width = columns * cell + CONTACT_SHEET_PAD
    height = rows * cell + CONTACT_SHEET_PAD
    sheet = Image.new("RGB", (width, height), CONTACT_SHEET_BG)

    for index, tile in enumerate(tiles):
        row, column = divmod(index, columns)
        origin_x = CONTACT_SHEET_PAD + column * cell
        origin_y = CONTACT_SHEET_PAD + row * cell
        sheet.paste(
            tile,
            (
                origin_x + (thumb - tile.width) // 2,
                origin_y + (thumb - tile.height) // 2,
            ),
        )

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.suffix.lower() in JPEG_EXTENSIONS:
        sheet.save(dest, format="JPEG", quality=88, optimize=True)
    else:
        sheet.save(dest, format="PNG")
    return dest
