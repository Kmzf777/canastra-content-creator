"""Estrategias de referencia visual: como uma foto real guia uma imagem gerada.

Duas vias, uma interface. `choose_strategy` e o UNICO lugar do sistema que
decide entre elas - fila, CLI e API perguntam aqui em vez de olhar
`capabilities.native_reference_supported` por conta propria. Assim, no dia em
que a sondagem confirmar suporte nativo, o sistema inteiro muda de trilha por
uma linha so, e nenhum caminho fica para tras usando a heuristica velha.
"""

from __future__ import annotations

from ..capabilities import ApiCapabilities
from ..models import StyleDna
from .base import MAX_REFERENCES, PromptLike, ReferenceStrategy, RequestPayload, prompt_text
from .descriptor import DescriptorReferenceStrategy
from .native import NativeReferenceStrategy


def choose_strategy(
    capabilities: ApiCapabilities | None,
    style_dna: StyleDna | None = None,
) -> ReferenceStrategy:
    """Nativa so com suporte provado; descritiva em qualquer outro caso.

    `capabilities=None` (arquivo de sondagem ausente) cai na descritiva pelo
    mesmo motivo que o default de `ApiCapabilities` e "nao suportado": ausencia
    de prova nunca vira permissao.
    """
    if capabilities is not None and capabilities.native_reference_supported:
        return NativeReferenceStrategy(capabilities)
    return DescriptorReferenceStrategy(style_dna)


__all__ = [
    "MAX_REFERENCES",
    "DescriptorReferenceStrategy",
    "NativeReferenceStrategy",
    "PromptLike",
    "ReferenceStrategy",
    "RequestPayload",
    "choose_strategy",
    "prompt_text",
]
