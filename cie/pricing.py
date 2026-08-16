"""Catalogo de modelos de imagem e estimativa de custo.

IMPORTANTE: os precos abaixo sao os informados na especificacao do projeto e
NAO foram confirmados contra a documentacao da xAI (o ambiente de
desenvolvimento nao tem egress para docs.x.ai / api.x.ai). Todo modelo nasce
com `verified=False`. Rode `scripts/probe_api.py` numa maquina com acesso: ele
grava `.cie/models.yaml`, que sobrescreve este catalogo em runtime.

Custo real cobrado sempre vem de `generations.cost_usd`, gravado depois da
chamada; o catalogo serve para estimativa e para o teto de orcamento da fila.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

import yaml

#: Resolucoes nominais que a API expoe.
RESOLUTIONS = ("1k", "2k")
#: Niveis de qualidade do grok-imagine-image-2.0.
QUALITIES = ("low", "medium")


@dataclass(frozen=True)
class ImageModel:
    name: str
    #: Chave: "<res>" ou "<res>:<quality>". Ex.: "1k", "2k:medium".
    prices_usd: Mapping[str, float]
    max_n: int = 10
    aspect_ratios: tuple[str, ...] = ("1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3")
    verified: bool = False
    source: str = "spec do projeto (nao confirmado na doc)"
    notes: str = ""

    def price(self, resolution: str = "1k", quality: str | None = None) -> float:
        resolution = resolution.lower()
        if quality:
            key = f"{resolution}:{quality.lower()}"
            if key in self.prices_usd:
                return self.prices_usd[key]
        if resolution in self.prices_usd:
            return self.prices_usd[resolution]
        # Fallback conservador: o maior preco conhecido do modelo, para o teto
        # de orcamento nunca subestimar o gasto.
        return max(self.prices_usd.values())


DEFAULT_MODEL = "grok-imagine-image"

#: Catalogo semente. Sobrescrevivel por .cie/models.yaml (ver load_overrides).
CATALOG: dict[str, ImageModel] = {
    "grok-imagine-image": ImageModel(
        name="grok-imagine-image",
        prices_usd={"1k": 0.02, "2k": 0.02},
        notes="mesmo preco em 1K e 2K segundo a spec",
    ),
    "grok-imagine-image-quality": ImageModel(
        name="grok-imagine-image-quality",
        prices_usd={"1k": 0.05, "2k": 0.07},
    ),
    "grok-imagine-image-2.0": ImageModel(
        name="grok-imagine-image-2.0",
        prices_usd={
            "1k:low": 0.04,
            "1k:medium": 0.06,
            "2k:low": 0.06,
            "2k:medium": 0.08,
            "1k": 0.06,
            "2k": 0.08,
        },
        notes="faixa 0.04 (1K Low) a 0.08 (2K Medium); pontos intermediarios estimados",
    ),
}


def get_model(name: str) -> ImageModel:
    """Devolve o modelo do catalogo. Modelo desconhecido nao vira excecao:
    entra como nao verificado e com o preco mais caro conhecido, para que a
    estimativa erre para cima e o teto de orcamento continue seguro."""
    if name in CATALOG:
        return CATALOG[name]
    worst = max((m.price("2k") for m in CATALOG.values()), default=0.10)
    return ImageModel(
        name=name,
        prices_usd={"1k": worst, "2k": worst},
        verified=False,
        source="desconhecido",
        notes="modelo fora do catalogo: preco estimado pelo teto conhecido",
    )


def estimate_cost(
    model: str,
    n: int = 1,
    resolution: str = "1k",
    quality: str | None = None,
) -> float:
    return round(get_model(model).price(resolution, quality) * max(n, 0), 6)


def load_overrides(path: Path | str) -> list[str]:
    """Carrega .cie/models.yaml (escrito pela sondagem) sobre o catalogo semente.

    Formato esperado:
        models:
          grok-imagine-image:
            prices_usd: {"1k": 0.02, "2k": 0.02}
            max_n: 10
            aspect_ratios: ["1:1", "16:9"]
            verified: true
    """
    path = Path(path)
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    updated: list[str] = []
    for name, spec in (data.get("models") or {}).items():
        base = CATALOG.get(name)
        CATALOG[name] = ImageModel(
            name=name,
            prices_usd=spec.get("prices_usd") or (base.prices_usd if base else {"1k": 0.10}),
            max_n=int(spec.get("max_n", base.max_n if base else 10)),
            aspect_ratios=tuple(
                spec.get("aspect_ratios") or (base.aspect_ratios if base else ())
            ),
            verified=bool(spec.get("verified", True)),
            source=str(spec.get("source", "sondagem da API")),
            notes=str(spec.get("notes", "")),
        )
        updated.append(name)
    return updated


def catalog_rows() -> list[dict[str, object]]:
    """Linhas prontas para exibicao em tabela na CLI."""
    return [
        {
            "modelo": m.name,
            "1k": m.price("1k"),
            "2k": m.price("2k"),
            "max_n": m.max_n,
            "verificado": m.verified,
            "fonte": m.source,
        }
        for m in sorted(CATALOG.values(), key=lambda x: x.name)
    ]
