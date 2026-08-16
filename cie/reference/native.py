"""Estrategia nativa: a foto real viaja junto do pedido, como pixel.

So entra em jogo depois que `scripts/probe_api.py` provou, contra a API de
verdade, QUAL campo aceita imagem e em que codificacao. Sem essa prova o
`apply()` levanta em vez de tentar: chutar o nome do campo custa credito para
receber 400 e, no pior caso, 200 - a API aceita o corpo, ignora o campo
desconhecido e cobra por uma imagem que nao seguiu referencia nenhuma.

Nada sai do projeto: o arquivo e lido na hora do request, reduzido em memoria e
codificado em base64. Nenhuma copia e gravada em disco, nenhum caminho local vai
no corpo da requisicao.
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import Sequence

from PIL import Image

from ..capabilities import ApiCapabilities
from ..errors import CieError
from ..imaging import load_image
from ..models import Asset
from ..xai import data_uri, to_b64
from .base import MAX_REFERENCES, PromptLike, ReferenceStrategy, RequestPayload, prompt_text

#: Maior lado da referencia depois do redimensionamento. Base64 infla os bytes
#: em ~33%: uma foto de 24 MP viraria dezenas de MB de corpo, com risco de 413,
#: timeout e retry caro. A referencia so guia estilo, luz e enquadramento -
#: 1536px ja entrega mais detalhe do que o modelo aproveita.
MAX_REFERENCE_EDGE = 1536

#: JPEG a 90: o artefato de compressao nesse nivel nao muda a leitura de estilo,
#: e o corpo fica varias vezes menor que PNG.
JPEG_QUALITY = 90
REFERENCE_MIME = "image/jpeg"

#: Valores de `reference_encoding` que pedem `data:image/jpeg;base64,...`.
_DATA_URI_ENCODINGS = frozenset({"data_uri", "data-uri", "datauri", "uri"})

PROBE_SCRIPT = "scripts/probe_api.py"


class NativeReferenceStrategy(ReferenceStrategy):
    """Envia as referencias no corpo do request, guiada pela sondagem."""

    name = "native"

    def __init__(self, capabilities: ApiCapabilities) -> None:
        self.capabilities = capabilities

    @property
    def max_references(self) -> int:
        """Teto efetivo: o menor entre a politica da casa e o que a API aceitou."""
        return min(MAX_REFERENCES, max(0, int(self.capabilities.max_reference_images)))

    def apply(
        self,
        prompt: PromptLike,
        assets: Sequence[Asset],
        *,
        model: str,
        n: int = 1,
        aspect_ratio: str | None = None,
    ) -> RequestPayload:
        caps = self.capabilities
        if not caps.native_reference_supported:
            raise CieError(
                "referencia nativa nao foi confirmada pela sondagem: "
                f"{caps.summary()}. Use a DescriptorReferenceStrategy "
                "(`cie.reference.choose_strategy` ja faz essa escolha sozinho) ou "
                f"rode `python {PROBE_SCRIPT}` numa maquina com XAI_API_KEY e "
                "acesso a api.x.ai para provar o suporte antes de gastar credito."
            )

        field_name = (caps.reference_field or "").strip()
        limit = self.max_references
        if not field_name or limit <= 0:
            # Sondagem incoerente (suporte "sim" sem campo ou sem teto): calar isso
            # seria montar um corpo adivinhado, exatamente o que este modulo evita.
            raise CieError(
                "capabilities diz que a referencia nativa e suportada, mas nao "
                f"registrou reference_field ({caps.reference_field!r}) e/ou "
                f"max_reference_images ({caps.max_reference_images!r}). Rode "
                f"`python {PROBE_SCRIPT}` de novo: o arquivo de sondagem esta "
                "incompleto e o CIE nao inventa nome de campo."
            )

        candidates = list(assets)
        selected = self.select_assets(candidates)
        notes: list[str] = []

        discarded = len(candidates) - len(selected)
        if discarded > 0:
            notes.append(
                f"{discarded} asset(s) descartado(s) na selecao: sem consentimento "
                "registrado ou fora do padrao de referencia"
            )
        if len(selected) > limit:
            notes.append(
                f"{len(selected)} referencia(s) reduzida(s) para {limit}: a sondagem "
                f"confirmou {caps.max_reference_images} imagem(ns) por request"
            )
            selected = selected[:limit]

        extra: dict[str, object] = {}
        if not selected:
            notes.append(
                "nenhum asset sobreviveu a selecao: o pedido segue sem imagem de "
                "referencia, guiado so pelo texto"
            )
        else:
            encoded: list[str] = []
            for asset in selected:
                blob, original, resized = self._reference_bytes(asset)
                if original != resized:
                    notes.append(
                        f"asset {asset.id} reduzido de {original[0]}x{original[1]} "
                        f"para {resized[0]}x{resized[1]} antes de codificar"
                    )
                encoded.append(self._encode(blob))
            # Com teto de uma imagem o campo carrega a string sozinha; empacotar
            # numa lista seria supor um formato que a sondagem nao viu passar.
            extra[field_name] = encoded[0] if limit == 1 else encoded

        if caps.max_n and n > caps.max_n:
            notes.append(
                f"n={n} acima do maximo sondado ({caps.max_n}): a API pode recusar "
                "ou devolver menos imagens"
            )

        return RequestPayload(
            prompt=prompt_text(prompt),
            model=model,
            n=n,
            aspect_ratio=aspect_ratio,
            extra=extra,
            reference_asset_ids=[a.id for a in selected if a.id is not None],
            strategy=self.name,
            notes=notes,
        )

    # -- interno ------------------------------------------------------------ #

    def _encode(self, blob: bytes) -> str:
        encoding = (self.capabilities.reference_encoding or "").strip().lower()
        if encoding in _DATA_URI_ENCODINGS:
            return data_uri(blob, REFERENCE_MIME)
        # Default base64 puro: e o que a sondagem grava como "b64" e o formato
        # mais comum em APIs de imagem no estilo OpenAI.
        return to_b64(blob)

    def _reference_bytes(
        self, asset: Asset
    ) -> tuple[bytes, tuple[int, int], tuple[int, int]]:
        """Le o asset agora e devolve os bytes ja reduzidos, com as duas medidas."""
        path = Path(asset.path)
        if not path.exists():
            raise CieError(
                f"o asset {asset.id} aponta para {path}, que nao existe mais. "
                "Reingira o diretorio (`cie ingest`) ou escolha outra referencia."
            )
        image = load_image(path)
        if image is None:
            raise CieError(
                f"o asset {asset.id} ({path.name}) nao tem decoder disponivel, entao "
                "nao da para envia-lo como referencia. Converta para JPEG/PNG, ou "
                "instale o extra `heic` se for foto de celular."
            )
        with image:
            return _downscaled_jpeg(image)


def _downscaled_jpeg(image: Image.Image) -> tuple[bytes, tuple[int, int], tuple[int, int]]:
    original = (image.width, image.height)
    # JPEG nao tem canal alfa e a referencia nao precisa de um: RGB sempre.
    frame = image.convert("RGB")
    longest = max(frame.width, frame.height)
    if longest > MAX_REFERENCE_EDGE:
        scale = MAX_REFERENCE_EDGE / longest
        frame = frame.resize(
            (max(1, round(frame.width * scale)), max(1, round(frame.height * scale))),
            Image.LANCZOS,
        )
    buffer = io.BytesIO()
    frame.save(buffer, format="JPEG", quality=JPEG_QUALITY)
    return buffer.getvalue(), original, (frame.width, frame.height)


__all__ = [
    "JPEG_QUALITY",
    "MAX_REFERENCE_EDGE",
    "REFERENCE_MIME",
    "NativeReferenceStrategy",
]
