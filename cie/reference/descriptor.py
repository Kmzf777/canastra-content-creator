"""Estrategia descritiva: a referencia vira texto, nunca pixel.

E o padrao do CIE e continua sendo ate a sondagem provar que a API aceita imagem
de referencia. A consistencia visual vem do `prompt_fragment` do Style DNA - a
paleta, a luz, a lente e os materiais que o modelo de visao leu das fotos reais
da operacao. O modelo recebe a descricao do real; nao recebe o real.

Mesmo sem enviar imagem, o payload registra quais assets serviram de referencia
conceitual. Sem esse rastro nao da para responder, meses depois, "de qual foto
esta imagem herdou o estilo?", e proveniencia sem resposta nao e proveniencia.
"""

from __future__ import annotations

import re
from typing import Sequence

from ..models import Asset, StyleDna
from ..utils import strip_accents
from .base import PromptLike, ReferenceStrategy, RequestPayload, prompt_text

#: Tamanho minimo de um trecho do fragmento para valer como prova de presenca.
#: Abaixo disto ("luz", "50mm") a coincidencia diria pouco.
MIN_SEGMENT_CHARS = 12

_SEGMENT_SPLIT = re.compile(r"[;.\n]")
_WHITESPACE = re.compile(r"\s+")


def _normalized(text: str) -> str:
    """Compara sem acento, sem caixa e sem depender de onde o texto quebra linha."""
    return _WHITESPACE.sub(" ", strip_accents(text).lower()).strip()


def fragment_already_present(text: str, fragment: str) -> bool:
    """O prompt ja carrega o fragmento do Style DNA?

    Quando `cie.prompt` compoe o prompt ele ja costura o fragmento no lugar
    certo (corpo do template, depois o DNA, depois o negative). Injetar de novo
    aqui duplicaria a instrucao de estilo e o modelo passa a tratar a repeticao
    como enfase - a paleta satura e a cena vira caricatura do proprio DNA.
    """
    haystack = _normalized(text)
    needle = _normalized(fragment)
    if not needle:
        return True
    if needle in haystack:
        return True
    # O compositor pode reordenar ou requebrar o fragmento; se todos os trechos
    # significativos ja estao no texto, o DNA esta la mesmo sem casar literalmente.
    segments = [
        segment
        for segment in (_normalized(part) for part in _SEGMENT_SPLIT.split(fragment))
        if len(segment) >= MIN_SEGMENT_CHARS
    ]
    return bool(segments) and all(segment in haystack for segment in segments)


class DescriptorReferenceStrategy(ReferenceStrategy):
    """Injeta o Style DNA no texto e nunca anexa imagem ao request."""

    name = "descriptor"

    def __init__(self, style_dna: StyleDna | None = None) -> None:
        self.style_dna = style_dna

    def apply(
        self,
        prompt: PromptLike,
        assets: Sequence[Asset],
        *,
        model: str,
        n: int = 1,
        aspect_ratio: str | None = None,
    ) -> RequestPayload:
        text = prompt_text(prompt)
        notes: list[str] = [
            "estrategia descritiva: nenhuma imagem foi enviada a API"
        ]

        text, fragment_note = self._with_style_fragment(text)
        notes.append(fragment_note)

        candidates = list(assets)
        selected = self.select_assets(candidates)
        discarded = len(candidates) - len(selected)
        if discarded > 0:
            notes.append(
                f"{discarded} asset(s) descartado(s) na selecao: sem consentimento "
                "registrado ou fora do padrao de referencia"
            )

        reference_ids = [asset.id for asset in selected if asset.id is not None]
        if not reference_ids and self.style_dna is not None and self.style_dna.source_asset_ids:
            # Sem asset explicito o rastro vem de quem originou o DNA: sao essas
            # fotos reais que estao ditando paleta, luz e textura desta imagem.
            reference_ids = list(self.style_dna.source_asset_ids)
            notes.append(
                f"proveniencia herdada dos {len(reference_ids)} asset(s) que "
                f"originaram o Style DNA '{self.style_dna.name}'"
            )

        return RequestPayload(
            prompt=text,
            model=model,
            n=n,
            aspect_ratio=aspect_ratio,
            # `extra` fica vazio de proposito: nada nao confirmado entra no corpo.
            extra={},
            reference_asset_ids=reference_ids,
            strategy=self.name,
            notes=notes,
        )

    # -- interno ------------------------------------------------------------ #

    def _with_style_fragment(self, text: str) -> tuple[str, str]:
        dna = self.style_dna
        if dna is None:
            return text, "sem Style DNA: o prompt segue so com o texto do template"

        fragment = (dna.prompt_fragment or "").strip()
        if not fragment:
            return text, f"Style DNA '{dna.name}' sem prompt_fragment: nada a injetar"

        if fragment_already_present(text, fragment):
            return text, f"fragmento do Style DNA '{dna.name}' ja presente; nao duplicado"

        return (
            f"{text.rstrip()}\n\n{fragment}" if text.strip() else fragment,
            f"fragmento do Style DNA '{dna.name}' injetado no fim do prompt",
        )


__all__ = [
    "MIN_SEGMENT_CHARS",
    "DescriptorReferenceStrategy",
    "fragment_already_present",
]
