"""O que a API da xAI realmente aceita - descoberto empiricamente, nunca chutado.

Enquanto `scripts/probe_api.py` nao rodar, TODOS os recursos opcionais ficam
desligados. Consequencia direta e desejada: `NativeReferenceStrategy` so entra
em jogo depois de prova; ate la o sistema usa `DescriptorReferenceStrategy`.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .config import Settings

CAPABILITIES_FILENAME = "capabilities.json"


@dataclass
class ApiCapabilities:
    """Resultado da sondagem. Defaults = "nao sabemos, logo nao usamos"."""

    probed_at: str | None = None
    #: A API aceita imagem de referencia em algum campo/endpoint?
    native_reference_supported: bool = False
    #: Nome do campo aceito ("image", "images", "reference_images", "input_image").
    reference_field: str | None = None
    #: Caminho relativo do endpoint que aceitou ("/images/generations" | "/images/edits").
    reference_endpoint: str | None = None
    #: Quantas referencias por request a API aceitou de fato.
    max_reference_images: int = 0
    #: Codificacao aceita: "b64" (base64 puro) ou "data_uri".
    reference_encoding: str | None = None

    supports_seed: bool = False
    supports_aspect_ratio: bool = False
    supports_size: bool = False
    supports_quality: bool = False
    max_n: int = 1
    response_formats: list[str] = field(default_factory=lambda: ["b64_json"])
    image_models: list[str] = field(default_factory=list)
    vision_model: str | None = None
    #: Log cru de cada tentativa da sondagem, para auditoria.
    attempts: list[dict[str, Any]] = field(default_factory=list)

    @property
    def probed(self) -> bool:
        return self.probed_at is not None

    def summary(self) -> str:
        if not self.probed:
            return (
                "API nunca sondada. Rode `python scripts/probe_api.py` numa maquina "
                "com XAI_API_KEY e acesso a api.x.ai. Ate la o CIE opera em modo "
                "descritivo (sem imagem de referencia nativa)."
            )
        if self.native_reference_supported:
            return (
                f"referencia nativa OK: campo '{self.reference_field}' em "
                f"{self.reference_endpoint}, ate {self.max_reference_images} imagem(ns)"
            )
        return "referencia nativa NAO suportada: estrategia descritiva e a unica via"


def path_for(settings: Settings) -> Path:
    return settings.home / CAPABILITIES_FILENAME


def load(settings: Settings) -> ApiCapabilities:
    path = path_for(settings)
    if not path.exists():
        return ApiCapabilities()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return ApiCapabilities()
    known = {f for f in ApiCapabilities.__dataclass_fields__}
    return ApiCapabilities(**{k: v for k, v in data.items() if k in known})


def save(settings: Settings, capabilities: ApiCapabilities) -> Path:
    settings.ensure_dirs()
    path = path_for(settings)
    path.write_text(
        json.dumps(asdict(capabilities), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return path
