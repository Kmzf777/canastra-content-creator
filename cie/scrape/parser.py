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
from .models import HarvestBatch, ScrapedItem

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


def parse_envelope(envelope: dict) -> HarvestBatch:
    """O arquivo de `raspagem/_colheita/` -> lote parseado.

    Aceita qualquer envelope no formato gravado por `harvest`, venha ele do
    Playwright ou de um arquivo antigo em disco. Mesma regra do resto do
    modulo: formato inesperado vira `InstagramFormatError`, nunca `KeyError`,
    `AttributeError` ou `ValidationError` do Pydantic.
    """
    if not isinstance(envelope, dict):
        raise InstagramFormatError(
            f"envelope deveria ser objeto, veio {type(envelope).__name__}",
            campo="envelope",
        )

    alvo = _objeto(envelope.get("target"), "target")
    kind = alvo.get("kind")
    if not kind:
        raise InstagramFormatError(
            "envelope sem 'target.kind'; nao da para saber como ler as paginas",
            campo="target",
        )
    if not isinstance(kind, str) or kind not in _EXTRATORES:
        raise InstagramFormatError(
            f"alvo de tipo desconhecido: {kind!r} "
            f"(esperado um de {sorted(_EXTRATORES)})",
            campo="target.kind",
        )

    slug_bruto = alvo.get("slug")
    if slug_bruto is not None and not isinstance(slug_bruto, str):
        raise InstagramFormatError(
            f"campo 'target.slug' deveria ser string, veio {type(slug_bruto).__name__}",
            campo="target.slug",
        )
    slug = slug_bruto or kind

    handle_bruto = alvo.get("handle")
    fallback = handle_bruto if isinstance(handle_bruto, str) else ""

    extrator = _EXTRATORES[kind]
    itens: list[ScrapedItem] = []
    for pagina in _lista(envelope.get("pages"), "pages"):
        pagina_obj = _objeto(pagina, "pages[]")
        for media in extrator(pagina_obj):
            itens.extend(parse_media(media, owner_fallback=fallback))

    return HarvestBatch(
        target_slug=slug,
        target_kind=kind,
        harvested_at=_colhido_em(envelope.get("harvested_at")),
        items=itens,
    )


def _medias_de_feed(pagina: dict) -> list:
    """`/api/v1/feed/user/<id>/` e `/api/v1/media/<id>/info/` devolvem `items`.

    Os elementos nao sao validados aqui - `parse_media` ja rejeita qualquer
    coisa que nao seja objeto, entao validar duas vezes so duplicaria a regra.
    """
    return _lista(pagina.get("items"), "items")


def _medias_de_hashtag(pagina: dict) -> list:
    """`/api/v1/tags/web_info/` empacota em secoes, divididas em `top` e `recent`.

    Secoes de clips (`one_by_two_item`) sao video em outro formato: no formato
    delas nao ha chave `medias`, entao a secao simplesmente nao contribui nada
    - sem precisar de um caso especial para reconhece-las.
    """
    encontrados: list = []
    dados = _objeto(pagina.get("data"), "data")
    for bloco_nome in ("top", "recent"):
        bloco = _objeto(dados.get(bloco_nome), f"data.{bloco_nome}")
        campo_secoes = f"data.{bloco_nome}.sections"
        for secao in _lista(bloco.get("sections"), campo_secoes):
            secao_obj = _objeto(secao, f"{campo_secoes}[]")
            campo_layout = f"{campo_secoes}[].layout_content"
            layout = _objeto(secao_obj.get("layout_content"), campo_layout)
            campo_medias = f"{campo_layout}.medias"
            for entrada in _lista(layout.get("medias"), campo_medias):
                entrada_obj = _objeto(entrada, f"{campo_medias}[]")
                media = entrada_obj.get("media")
                if media is not None:
                    encontrados.append(media)
    return encontrados


_EXTRATORES = {
    "profile": _medias_de_feed,
    "post": _medias_de_feed,
    "hashtag": _medias_de_hashtag,
}


def _colhido_em(valor) -> datetime:
    """`harvested_at` do envelope -> datetime. Ilegivel ou ausente vira agora."""
    if isinstance(valor, str) and valor:
        try:
            return datetime.fromisoformat(valor)
        except ValueError:
            pass
    return datetime.now(tz=timezone.utc)
