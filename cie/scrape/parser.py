"""JSON do Instagram -> `ScrapedItem`.

Puro: recebe dict, devolve modelo. Nao sabe de onde o dict veio - do Playwright,
de um arquivo salvo, ou de trafego interceptado. E isso que torna barato trocar
a forma de colher sem tocar em nada aqui.

Regra que atravessa o modulo: formato inesperado vira `InstagramFormatError` com
o nome do campo que faltou. `KeyError` nu e proibido - o Instagram muda o JSON
sem aviso, e a mensagem precisa dizer o que mudou.
"""

from __future__ import annotations

from datetime import datetime, timezone

from ..errors import InstagramFormatError
from .models import ScrapedItem

#: media_type do Instagram: 1 imagem, 2 video, 8 carrossel.
_TIPO_VIDEO = 2


def parse_media(media: dict, *, owner_fallback: str = "") -> list[ScrapedItem]:
    """Um objeto `media` da API v1 -> um item por imagem.

    Foto simples devolve 1 item; carrossel de N devolve N, ja indexados.
    """
    if not isinstance(media, dict):
        raise InstagramFormatError(
            f"esperava objeto 'media', recebi {type(media).__name__}", campo="media"
        )

    shortcode = media.get("code")
    if not shortcode:
        raise InstagramFormatError(
            "objeto 'media' sem o campo 'code' (shortcode do post); "
            "o formato do Instagram provavelmente mudou",
            campo="code",
        )

    handle = (media.get("user") or {}).get("username") or owner_fallback
    caption = ((media.get("caption") or {}).get("text") or "").strip()
    taken_at = _timestamp(media.get("taken_at"))
    post_url = f"https://www.instagram.com/p/{shortcode}/"

    filhos = media.get("carousel_media") or [media]

    itens: list[ScrapedItem] = []
    for indice, filho in enumerate(filhos, start=1):
        is_video = filho.get("media_type") == _TIPO_VIDEO
        melhor = _melhor_candidato(filho, permitir_vazio=is_video)
        itens.append(
            ScrapedItem(
                shortcode=shortcode,
                owner_handle=handle,
                post_url=post_url,
                display_url=melhor.get("url", ""),
                width=int(melhor.get("width") or 0),
                height=int(melhor.get("height") or 0),
                taken_at=taken_at,
                caption=caption,
                carousel_index=indice,
                is_video=is_video,
            )
        )
    return itens


def _melhor_candidato(media: dict, *, permitir_vazio: bool) -> dict:
    """A maior resolucao disponivel. O Instagram nao devolve a lista ordenada."""
    candidatos = (media.get("image_versions2") or {}).get("candidates") or []
    if not candidatos:
        if permitir_vazio:
            # Video sem capa: marcamos e seguimos - o download pula videos de todo jeito.
            return {}
        raise InstagramFormatError(
            "objeto 'media' sem 'image_versions2.candidates'; sem isso nao ha "
            "URL de imagem para baixar",
            campo="image_versions2",
        )
    return max(
        candidatos,
        key=lambda c: int(c.get("width") or 0) * int(c.get("height") or 0),
    )


def _timestamp(valor) -> datetime | None:
    """`taken_at` unix -> datetime UTC. Ausente continua ausente: nao inventamos data."""
    if not valor:
        return None
    try:
        return datetime.fromtimestamp(int(valor), tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return None
