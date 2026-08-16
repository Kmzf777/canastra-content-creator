"""Interface comum das duas estrategias de referencia visual.

Consistencia visual no CIE tem duas vias possiveis e so uma delas esta provada:
mandar a foto real junto do pedido (`NativeReferenceStrategy`, valida so depois
que a sondagem confirmar campo e codificacao) ou descrever a foto real em texto
(`DescriptorReferenceStrategy`, sempre disponivel). As duas devolvem o mesmo
tipo - `RequestPayload` - para que a fila nao precise saber qual delas rodou.

`RequestPayload` e deliberadamente inerte: e um retrato do que sera enviado com
o rastro de proveniencia grudado (`reference_asset_ids`, `strategy`, `notes`).
Quem fala com a API converte com `to_image_request()`; quem grava o Job copia
`reference_asset_ids` para a linha do banco. Nenhum dos dois precisa reabrir
arquivo nem reconstruir decisao.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Sequence

from ..models import Asset
from ..xai import ImageRequest

#: Teto duro de referencias por pedido, o mesmo de `guardrails.MAX_REFERENCE_IMAGES`.
#: Acima disto o modelo funde as fotos e a saida deixa de ser rastreavel a uma
#: imagem real especifica - que e justamente o que a proveniencia promete.
MAX_REFERENCES = 3

#: Um prompt aceito por `apply()`: texto cru ou o `ComposedPrompt` de `cie.prompt`.
#: O tipo fica solto de proposito - ver `prompt_text()` logo abaixo.
PromptLike = Any

#: Atributos e metodos que um prompt composto pode expor para virar texto.
#: Duck typing de proposito: a estrategia NAO importa `cie.prompt`, senao
#: composicao de prompt e escolha de referencia viram um no circular.
_TEXT_ATTRS: tuple[str, ...] = ("text", "full_text", "resolved_prompt", "prompt")
_TEXT_METHODS: tuple[str, ...] = ("to_text", "render", "as_text", "compose")


def prompt_text(prompt: PromptLike) -> str:
    """Extrai o texto final de um prompt, seja ele `str` ou objeto composto."""
    if isinstance(prompt, str):
        return prompt
    for attr in _TEXT_ATTRS:
        value = getattr(prompt, attr, None)
        if isinstance(value, str) and value.strip():
            return value
    for name in _TEXT_METHODS:
        method = getattr(prompt, name, None)
        if callable(method):
            try:
                value = method()
            except TypeError:  # assinatura exige argumentos: nao e o que buscamos
                continue
            if isinstance(value, str) and value.strip():
                return value
    return str(prompt)


@dataclass
class RequestPayload:
    """O pedido montado por uma estrategia, com proveniencia anexada."""

    prompt: str
    model: str
    n: int = 1
    aspect_ratio: str | None = None
    #: Campos adicionais do corpo do request (imagens, quando a API as aceita).
    #: Vazio na estrategia descritiva - la a referencia mora no texto.
    extra: dict[str, Any] = field(default_factory=dict)
    #: Assets que serviram de referencia, real ou conceitual. Rastro obrigatorio.
    reference_asset_ids: list[int] = field(default_factory=list)
    strategy: str = ""
    #: Por que o payload ficou assim. Vai para o `--dry-run` e para a auditoria.
    notes: list[str] = field(default_factory=list)

    def to_image_request(self) -> ImageRequest:
        """Converte para o tipo que `XaiClient.generate_images` consome.

        `extra` e copiado: o payload continua sendo o retrato do que foi
        decidido, mesmo que o cliente mexa no request depois.
        """
        return ImageRequest(
            model=self.model,
            prompt=self.prompt,
            n=self.n,
            aspect_ratio=self.aspect_ratio,
            extra=dict(self.extra),
        )


class ReferenceStrategy(ABC):
    """Contrato das duas vias de referencia."""

    #: Identificador curto gravado em `RequestPayload.strategy` ("native"|"descriptor").
    name: str = "abstract"

    @abstractmethod
    def apply(
        self,
        prompt: PromptLike,
        assets: Sequence[Asset],
        *,
        model: str,
        n: int = 1,
        aspect_ratio: str | None = None,
    ) -> RequestPayload:
        """Monta o pedido a partir do prompt e dos assets pretendidos."""

    def select_assets(self, assets: Sequence[Asset]) -> list[Asset]:
        """Filtra, ordena e corta os candidatos a referencia.

        Descarta quem nao passa em `Asset.is_usable_as_reference` (sem
        consentimento quando ha pessoa identificavel, ou fora do padrao de
        nitidez), ordena por `quality_score` decrescente e corta em
        `MAX_REFERENCES`. Empate desempata pelo id, para que o mesmo catalogo
        produza sempre a mesma selecao - job reproduzivel vale mais que meio
        ponto de nitidez.
        """
        usable = [asset for asset in assets if asset.is_usable_as_reference]
        ordered = sorted(
            usable,
            # score ausente afunda para o fim em vez de virar erro de comparacao.
            key=lambda a: (-(a.quality_score or 0), a.id if a.id is not None else 0),
        )
        return ordered[:MAX_REFERENCES]


__all__ = [
    "MAX_REFERENCES",
    "PromptLike",
    "ReferenceStrategy",
    "RequestPayload",
    "prompt_text",
]
