"""Provedores de geracao de imagem.

Dois provedores, uma escolha por trabalho (tabela de roteamento do CLAUDE.md):

| Situacao                                        | Provedor                     |
|-------------------------------------------------|------------------------------|
| Ambiente e o assunto, produto pequeno ou ausente | `gemini` (gemini-3-pro-image)|
| Produto grande, rotulo precisa ser legivel       | `xai` (/images/edits 2.0)    |
| Rotulo exato ao pixel                            | composicao do recorte real   |

O Gemini entrega cena mais natural; a xAI preserva rotulo. Essa e a troca, e ela
nao se resolve com prompt melhor.

Diferenca operacional que decide sozinha muita coisa: `4:5` (feed do Instagram)
e nativo no Gemini e **nao existe** na xAI - la se gera em `3:4` e se recorta,
via `ProvedorXai.gerar_4x5`.
"""

from __future__ import annotations

from typing import Any

from .base import (
    MARCA_REDACAO,
    CampoProibido,
    ErroProvedor,
    FonteInvalida,
    ProporcaoInvalida,
    Provider,
    ProvedorBase,
    Requisicao,
    fazer_redator,
)
from .gemini import ErroGemini, ProvedorGemini
from .xai import ErroXai, ProvedorXai, recortar_4x5

#: Nome -> classe. Serve a CLI e a fila, que recebem provedor como string.
PROVEDORES: dict[str, type[ProvedorBase]] = {
    "xai": ProvedorXai,
    "gemini": ProvedorGemini,
}


def criar_provedor(nome: str, **opcoes: Any) -> ProvedorBase:
    """Instancia um provedor pelo nome. Nome desconhecido falha na hora."""
    try:
        classe = PROVEDORES[nome]
    except KeyError:
        raise ErroProvedor(
            f"provedor {nome!r} desconhecido; disponiveis: {', '.join(sorted(PROVEDORES))}"
        ) from None
    return classe(**opcoes)


__all__ = [
    "MARCA_REDACAO",
    "PROVEDORES",
    "CampoProibido",
    "ErroGemini",
    "ErroProvedor",
    "ErroXai",
    "FonteInvalida",
    "ProporcaoInvalida",
    "Provider",
    "ProvedorBase",
    "ProvedorGemini",
    "ProvedorXai",
    "Requisicao",
    "criar_provedor",
    "fazer_redator",
    "recortar_4x5",
]
