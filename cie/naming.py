"""Inferencia de pilar/local/SKU a partir do caminho e do nome do arquivo.

Convencao oficial da base:  CANASTRA_[PILAR]_[LOCAL]_[ASSUNTO]_[NNN].ext
Exemplo:                    CANASTRA_3_TORREFACAO_TAMBOR_007.jpg

Quando a convencao nao bate, tentamos tokens soltos do caminho; se ainda assim
faltar pilar ou local, o asset e marcado `needs_review` - o sistema nunca chuta.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .enums import Location, Pillar, Sku
from .utils import normalize_token, slugify

PILLAR_TOKENS: dict[str, Pillar] = {
    "1": Pillar.P1, "P1": Pillar.P1, "TERROIR": Pillar.P1, "TRADICAO": Pillar.P1,
    "2": Pillar.P2, "P2": Pillar.P2, "SUSTENTABILIDADE": Pillar.P2,
    "ENGENHARIA": Pillar.P2, "SOLAR": Pillar.P2, "SOLARES": Pillar.P2,
    "3": Pillar.P3, "P3": Pillar.P3, "LABORATORIO": Pillar.P3, "LAB": Pillar.P3,
    "TORRA": Pillar.P3, "SENSORIAL": Pillar.P3, "CUPPING": Pillar.P3,
    "4": Pillar.P4, "P4": Pillar.P4, "EDUCACAO": Pillar.P4, "BREWING": Pillar.P4,
    "CULTURA": Pillar.P4,
    "PRODUCT": Pillar.PRODUCT, "PRODUTO": Pillar.PRODUCT, "PACK": Pillar.PRODUCT,
    "PACKSHOT": Pillar.PRODUCT, "EMBALAGEM": Pillar.PRODUCT,
    "PEOPLE": Pillar.PEOPLE, "PESSOAS": Pillar.PEOPLE, "EQUIPE": Pillar.PEOPLE,
    "FAMILIA": Pillar.PEOPLE, "TIME": Pillar.PEOPLE,
}

LOCATION_TOKENS: dict[str, Location] = {
    "FAZENDA": Location.FAZENDA_MEDEIROS,
    "MEDEIROS": Location.FAZENDA_MEDEIROS,
    "SERRA": Location.FAZENDA_MEDEIROS,
    "TORREFACAO": Location.TORREFACAO_UBERLANDIA,
    "UBERLANDIA": Location.TORREFACAO_UBERLANDIA,
    "UDI": Location.TORREFACAO_UBERLANDIA,
    "ESTUDIO": Location.ESTUDIO,
    "STUDIO": Location.ESTUDIO,
    "OUTRO": Location.OUTRO,
    "OTHER": Location.OUTRO,
}

SKU_TOKENS: dict[str, Sku] = {
    "CLASSICO": Sku.CLASSICO,
    "SUAVE": Sku.SUAVE,
    "CANELA": Sku.CANELA,
    "MICROLOTE": Sku.MICROLOTE,
    "MICROLOTES": Sku.MICROLOTE,
    "GEISHA": Sku.GEISHA,
    "DRIP": Sku.DRIP,
    "DRIPCOFFEE": Sku.DRIP,
    "CAPSULA": Sku.CAPSULA,
    "CAPSULAS": Sku.CAPSULA,
}

#: Vocabulario de assunto que vale a pena virar tag pesquisavel.
SUBJECT_KEYWORDS = {
    "GRAO", "GRAOS", "TERREIRO", "SECAGEM", "COLHEITA", "CAFEZAL", "ENCOSTA",
    "MUDA", "FLORADA", "NEBLINA", "TAMBOR", "TORREFADOR", "CRACK", "CUPPING",
    "MOAGEM", "MOEDOR", "V60", "COADOR", "PRENSA", "ESPRESSO", "LATTE",
    "XICARA", "VAPOR", "BLOOM", "QUEIJO", "HARMONIZACAO", "JUTA", "SACO",
    "PAINEL", "PAINEIS", "SOLAR", "ARARA", "CATUAI", "MADEIRA", "MAOS",
    "RETRATO", "FAMILIA", "PACOTE", "ROTULO",
}

# Coordenadas aproximadas para inferir local por GPS.
# Ambas com raio generoso: queremos separar Medeiros de Uberlandia, nao geolocalizar.
_GPS_ANCHORS: list[tuple[float, float, float, Location]] = [
    (-19.9944, -46.0206, 0.45, Location.FAZENDA_MEDEIROS),  # Medeiros / Serra da Canastra
    (-18.9186, -48.2772, 0.45, Location.TORREFACAO_UBERLANDIA),  # Uberlandia
]


@dataclass(frozen=True)
class ParsedName:
    """Resultado do parser da convencao de nomes."""

    matched: bool
    pillar: Pillar | None = None
    location: Location | None = None
    subject: str | None = None
    sequence: int | None = None


@dataclass
class Inference:
    """O que a ingestao conseguiu deduzir - e por que."""

    pillar: Pillar | None = None
    location: Location | None = None
    sku: Sku | None = None
    subject_tags: list[str] = field(default_factory=list)
    needs_review: bool = True
    reasons: list[str] = field(default_factory=list)


def parse_asset_name(filename: str) -> ParsedName:
    """Le CANASTRA_[PILAR]_[LOCAL]_[ASSUNTO]_[NNN].ext."""
    stem = Path(filename).stem
    parts = [normalize_token(p) for p in re.split(r"[_\-\s]+", stem) if p]
    if len(parts) < 5 or parts[0] != "CANASTRA":
        return ParsedName(matched=False)

    pillar = PILLAR_TOKENS.get(parts[1])
    location = LOCATION_TOKENS.get(parts[2])
    tail = parts[-1]
    sequence = int(tail) if tail.isdigit() else None
    subject_parts = parts[3:-1] if sequence is not None else parts[3:]
    subject = "_".join(subject_parts) if subject_parts else None

    # `matched` significa "seguiu a convencao", nao "resolveu tudo":
    # um token de pilar desconhecido ainda cai em needs_review depois.
    return ParsedName(
        matched=True,
        pillar=pillar,
        location=location,
        subject=subject,
        sequence=sequence,
    )


def location_from_gps(lat: float | None, lon: float | None) -> Location | None:
    if lat is None or lon is None:
        return None
    for anchor_lat, anchor_lon, radius, location in _GPS_ANCHORS:
        if abs(lat - anchor_lat) <= radius and abs(lon - anchor_lon) <= radius:
            return location
    return Location.OUTRO


def _path_tokens(path: Path, root: Path | None) -> list[str]:
    try:
        relative = path.relative_to(root) if root else path
    except ValueError:
        relative = path
    raw = list(relative.parts[:-1]) + [relative.stem]
    tokens: list[str] = []
    for part in raw:
        tokens.extend(normalize_token(t) for t in re.split(r"[_\-\s.]+", part) if t)
    return tokens


def infer(
    path: Path,
    root: Path | None = None,
    gps_lat: float | None = None,
    gps_lon: float | None = None,
) -> Inference:
    """Combina convencao de nome, tokens do caminho e GPS."""
    result = Inference()
    parsed = parse_asset_name(path.name)
    tokens = _path_tokens(path, root)

    # --- Pilar --------------------------------------------------------------
    if parsed.pillar:
        result.pillar = parsed.pillar
        result.reasons.append(f"pillar={parsed.pillar} via convencao de nome")
    else:
        for token in tokens:
            if token in PILLAR_TOKENS:
                result.pillar = PILLAR_TOKENS[token]
                result.reasons.append(f"pillar={result.pillar} via token '{token}' do caminho")
                break

    # --- Local --------------------------------------------------------------
    gps_location = location_from_gps(gps_lat, gps_lon)
    if parsed.location:
        result.location = parsed.location
        result.reasons.append(f"location={parsed.location} via convencao de nome")
        # Nome e curadoria humana explicita e vence; divergencia de GPS vira revisao.
        if gps_location and gps_location is not parsed.location:
            result.needs_review = True
            result.reasons.append(
                f"conflito: GPS sugere {gps_location}, nome diz {parsed.location}"
            )
    elif gps_location:
        result.location = gps_location
        result.reasons.append(f"location={gps_location} via GPS do EXIF")
    else:
        for token in tokens:
            if token in LOCATION_TOKENS:
                result.location = LOCATION_TOKENS[token]
                result.reasons.append(f"location={result.location} via token '{token}' do caminho")
                break

    # --- SKU ----------------------------------------------------------------
    for token in tokens:
        if token in SKU_TOKENS:
            result.sku = SKU_TOKENS[token]
            result.reasons.append(f"sku={result.sku} via token '{token}'")
            break

    # --- Tags de assunto ----------------------------------------------------
    tags: list[str] = []
    if parsed.subject:
        for token in parsed.subject.split("_"):
            slug = slugify(token)
            if slug and slug not in tags:
                tags.append(slug)
    for token in tokens:
        if token in SUBJECT_KEYWORDS:
            slug = slugify(token)
            if slug not in tags:
                tags.append(slug)
    result.subject_tags = tags

    # --- Precisa de revisao humana? -----------------------------------------
    missing = [name for name, value in (("pillar", result.pillar), ("location", result.location)) if not value]
    if missing:
        result.needs_review = True
        result.reasons.append(f"nao inferido: {', '.join(missing)}")
    elif not any(r.startswith("conflito") for r in result.reasons):
        result.needs_review = False

    return result
