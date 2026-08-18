"""JSON do Instagram -> `ScrapedItem`.

Puro: recebe dict, devolve modelo. Nao sabe de onde o dict veio - do Playwright,
de um arquivo salvo, ou de trafego interceptado. E isso que torna barato trocar
a forma de colher sem tocar em nada aqui.

Regra que atravessa o modulo: formato inesperado vira `InstagramFormatError` com
o nome do campo que faltou. `KeyError` nu e proibido - o Instagram muda o JSON
sem aviso, e a mensagem precisa dizer o que mudou.

Essa regra vale tambem para tipo errado, nao so campo ausente: o Instagram pode
mandar `code` como int, `user` como string, `carousel_media` com um `None` no
meio. `AttributeError`, `ValueError` e `ValidationError` do Pydantic sao tao
proibidos quanto `KeyError` - por isso todo campo externo passa pelos
acessores `_objeto`/`_lista`/`_inteiro` abaixo antes de ser usado.
"""

from __future__ import annotations

from datetime import datetime, timezone

from ..errors import InstagramFormatError
from .models import ScrapedItem

#: media_type do Instagram: 1 imagem, 2 video, 8 carrossel.
_TIPO_VIDEO = 2


def _objeto(valor, campo: str) -> dict:
    """Campo que deveria ser objeto. Ausente vira {}; do tipo errado, erro legivel."""
    if valor is None:
        return {}
    if not isinstance(valor, dict):
        raise InstagramFormatError(
            f"campo {campo!r} deveria ser objeto, veio {type(valor).__name__}",
            campo=campo,
        )
    return valor


def _lista(valor, campo: str) -> list:
    """Campo que deveria ser lista. Ausente vira []; do tipo errado, erro legivel."""
    if valor is None:
        return []
    if not isinstance(valor, list):
        raise InstagramFormatError(
            f"campo {campo!r} deveria ser lista, veio {type(valor).__name__}",
            campo=campo,
        )
    return valor


def _inteiro(valor) -> int:
    """Dimensao que o Instagram as vezes manda como string. Lixo vira 0."""
    try:
        return int(valor)
    except (TypeError, ValueError):
        return 0


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
    if not isinstance(shortcode, str):
        raise InstagramFormatError(
            f"campo 'code' deveria ser string (shortcode do post), veio "
            f"{type(shortcode).__name__}",
            campo="code",
        )

    handle = _objeto(media.get("user"), "user").get("username") or owner_fallback
    caption = (_objeto(media.get("caption"), "caption").get("text") or "").strip()
    taken_at = _timestamp(media.get("taken_at"))
    post_url = f"https://www.instagram.com/p/{shortcode}/"

    criancas_brutas = _lista(media.get("carousel_media"), "carousel_media")
    if criancas_brutas:
        filhos = [
            _objeto(cru, f"carousel_media[{indice}]")
            for indice, cru in enumerate(criancas_brutas)
        ]
    else:
        filhos = [media]

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
                width=_inteiro(melhor.get("width")),
                height=_inteiro(melhor.get("height")),
                taken_at=taken_at,
                caption=caption,
                carousel_index=indice,
                is_video=is_video,
            )
        )
    return itens


def _melhor_candidato(filho: dict, *, permitir_vazio: bool) -> dict:
    """A maior resolucao disponivel. O Instagram nao devolve a lista ordenada."""
    versoes = _objeto(filho.get("image_versions2"), "image_versions2")
    candidatos_brutos = _lista(versoes.get("candidates"), "image_versions2.candidates")
    candidatos = [c for c in candidatos_brutos if isinstance(c, dict)]
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
        key=lambda c: _inteiro(c.get("width")) * _inteiro(c.get("height")),
    )


def _timestamp(valor) -> datetime | None:
    """`taken_at` unix -> datetime UTC. Ausente continua ausente: nao inventamos data."""
    if not valor:
        return None
    try:
        return datetime.fromtimestamp(int(valor), tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return None
