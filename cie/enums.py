"""Vocabulario controlado do dominio.

Tudo que vira coluna de texto no SQLite passa por um StrEnum aqui, para que a
inferencia da ingestao, a CLI e os guardrails falem exatamente a mesma lingua.
"""

from __future__ import annotations

from enum import StrEnum


class Pillar(StrEnum):
    """Os quatro pilares editoriais, mais dois eixos transversais de catalogo."""

    #: Terroir e Tradicao - fazenda, altitude, colheita, familia, terreiro.
    P1 = "1"
    #: Sustentabilidade e Engenharia Agricola - solar, carbono, variedades.
    P2 = "2"
    #: Laboratorio de Torrefacao e Sensorialidade - tambor, cupping, macro.
    P3 = "3"
    #: Educacao e Cultura Brewing - V60, coador, drip, capsula, harmonizacao.
    P4 = "4"
    #: Embalagem/produto isolado (atravessa os pilares).
    PRODUCT = "product"
    #: Pessoas da operacao (atravessa os pilares, sempre com politica estrita).
    PEOPLE = "people"


class Location(StrEnum):
    FAZENDA_MEDEIROS = "fazenda_medeiros"
    TORREFACAO_UBERLANDIA = "torrefacao_uberlandia"
    ESTUDIO = "estudio"
    OUTRO = "outro"


class Sku(StrEnum):
    CLASSICO = "classico"
    SUAVE = "suave"
    CANELA = "canela"
    MICROLOTE = "microlote"
    GEISHA = "geisha"
    DRIP = "drip"
    CAPSULA = "capsula"


class TemplateKind(StrEnum):
    PRODUCT_SHOT = "product_shot"
    SCENE = "scene"
    MACRO = "macro"
    LIFESTYLE = "lifestyle"
    TEXTURE = "texture"


class RiskFlag(StrEnum):
    """Riscos que disparam regras especificas em `cie.guardrails`."""

    #: Texto/logotipo de embalagem - difusao erra tipografia, exige referencia real.
    PACKAGING_TEXT = "packaging_text"
    #: Rosto humano identificavel - nunca sintetizado.
    HUMAN_FACE = "human_face"
    #: Maos - deformacao classica de modelo de difusao.
    HANDS = "hands"
    #: Regeneracao de rosto: trilha proibida, ver guardrails.
    FACE_REGENERATION = "face_regeneration"


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    BLOCKED = "blocked"


class ReviewStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class AspectRatio(StrEnum):
    """Proporcoes aceitas pela API de imagem da xAI."""

    R1_1 = "1:1"
    R16_9 = "16:9"
    R9_16 = "9:16"
    R4_3 = "4:3"
    R3_4 = "3:4"
    R3_2 = "3:2"
    R2_3 = "2:3"


class ExportFormat(StrEnum):
    """Proporcoes de publicacao (4:5 e recorte de feed, nao existe na API)."""

    R9_16 = "9:16"
    R4_5 = "4:5"
    R1_1 = "1:1"


def ratio_value(ratio: str) -> float:
    """Converte '9:16' em 0.5625."""
    w, h = ratio.split(":")
    return int(w) / int(h)
