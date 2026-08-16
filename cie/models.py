"""Modelos Pydantic v2 das cinco entidades do sistema.

Os defaults de `Asset.has_identifiable_person` e `Asset.consent_on_file` sao
deliberadamente os mais restritivos possiveis: pessoa presumida presente,
consentimento ausente. A ingestao nunca sobrescreve esses dois campos - so a
curadoria humana faz isso.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

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


class StyleDescriptor(BaseModel):
    """Schema fixo do Style DNA - e o contrato que o modelo de visao precisa devolver."""

    model_config = ConfigDict(extra="forbid")

    palette: list[str] = Field(default_factory=list)
    light_quality: str = ""
    lens: str = ""
    texture: str = ""
    framing: str = ""
    recurring_materials: list[str] = Field(default_factory=list)
    mood: str = ""
    avoid: list[str] = Field(default_factory=list)


class Asset(BaseModel):
    """Uma foto real da operacao. Materia-prima, nunca saida do sistema."""

    model_config = ConfigDict(use_enum_values=False)

    id: int | None = None
    path: str
    sha256: str
    width: int | None = None
    height: int | None = None
    captured_at: datetime | None = None
    pillar: Pillar | None = None
    location: Location | None = None
    sku: Sku | None = None
    subject_tags: list[str] = Field(default_factory=list)

    # --- Campos de politica: preenchidos por humano, nunca pela ingestao. ---
    has_identifiable_person: bool = True
    consent_on_file: bool = False

    has_readable_packaging: bool = False
    quality_score: int | None = None
    is_reference_grade: bool = False
    style_descriptor: StyleDescriptor | None = None

    # --- Metadados tecnicos e de curadoria. ---
    needs_review: bool = True
    thumb_path: str | None = None
    camera: str | None = None
    lens: str | None = None
    gps_lat: float | None = None
    gps_lon: float | None = None
    notes: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_validator("quality_score")
    @classmethod
    def _score_range(cls, v: int | None) -> int | None:
        if v is not None and not 0 <= v <= 100:
            raise ValueError("quality_score deve estar entre 0 e 100")
        return v

    @property
    def is_usable_as_reference(self) -> bool:
        """Referencia exige nitidez/enquadramento e consentimento quando ha pessoa."""
        if not self.is_reference_grade:
            return False
        if self.has_identifiable_person and not self.consent_on_file:
            return False
        return True


class StyleDna(BaseModel):
    """Perfil de estilo derivado de um conjunto de assets aprovados."""

    id: int | None = None
    name: str
    pillar: Pillar | None = None
    source_asset_ids: list[int] = Field(default_factory=list)
    descriptor: StyleDescriptor
    prompt_fragment: str = ""
    created_at: datetime | None = None


class Template(BaseModel):
    """Cena parametrizavel. `body` usa placeholders no formato {variavel}."""

    id: int | None = None
    name: str
    pillar: Pillar | None = None
    kind: TemplateKind
    body: str
    negative_prompt: str = ""
    requires_reference: bool = False
    risk_flags: list[RiskFlag] = Field(default_factory=list)
    default_aspect_ratio: AspectRatio = AspectRatio.R1_1
    variables: dict[str, str] = Field(default_factory=dict)
    notes: str | None = None

    @property
    def touches_packaging(self) -> bool:
        return RiskFlag.PACKAGING_TEXT in self.risk_flags

    @property
    def touches_faces(self) -> bool:
        return RiskFlag.HUMAN_FACE in self.risk_flags or (
            RiskFlag.FACE_REGENERATION in self.risk_flags
        )


class Job(BaseModel):
    """Item da fila de geracao. `resolved_prompt` e persistido para auditoria."""

    id: int | None = None
    template_id: int
    style_dna_id: int | None = None
    reference_asset_ids: list[int] = Field(default_factory=list)
    resolved_prompt: str = ""
    model: str = ""
    aspect_ratio: AspectRatio = AspectRatio.R1_1
    n: int = 1
    status: JobStatus = JobStatus.QUEUED
    blocked_reason: str | None = None
    attempts: int = 0
    cost_usd: float = 0.0
    created_at: datetime | None = None
    finished_at: datetime | None = None


class Generation(BaseModel):
    """Cada imagem produzida, com proveniencia completa."""

    id: int | None = None
    job_id: int
    path: str
    sha256: str
    model: str
    prompt: str
    seed: int | None = None
    cost_usd: float = 0.0
    review_status: ReviewStatus = ReviewStatus.PENDING
    reject_reason: str | None = None
    #: Orienta a rotulagem de conteudo de IA no Instagram/Meta.
    disclosure_required: bool = True
    exported_variants: list[str] = Field(default_factory=list)
    created_at: datetime | None = None
