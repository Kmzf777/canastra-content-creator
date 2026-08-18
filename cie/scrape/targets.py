"""Traducao de um link (ou handle solto) no alvo tipado da raspagem.

Puro: nao toca rede, nao importa Playwright, nao le disco. Recebe string e
devolve alvo - e por isso da para testar o formato inteiro sem abrir browser.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse

from ..errors import ScrapeError

#: Alfabeto posicional que o Instagram usa para codificar media_id em shortcode.
SHORTCODE_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

_HANDLE_RE = re.compile(r"^[A-Za-z0-9._]{1,30}$")
_TAG_RE = re.compile(r"^[^\s/?#]{1,100}$")

#: Primeiros segmentos de caminho que o Instagram reserva - nenhum e handle.
_RESERVADOS = {
    "p", "reel", "reels", "explore", "stories", "tv", "s", "accounts",
    "direct", "about", "developer", "legal", "privacy", "web", "graphql",
    "api", "challenge", "emails", "session",
}


@dataclass(frozen=True)
class ProfileTarget:
    """Feed de um perfil."""

    handle: str

    kind = "profile"

    @property
    def slug(self) -> str:
        return self.handle


@dataclass(frozen=True)
class PostTarget:
    """Um post especifico, carrossel incluso."""

    shortcode: str

    kind = "post"

    @property
    def slug(self) -> str:
        return f"post-{self.shortcode}"


@dataclass(frozen=True)
class HashtagTarget:
    """Uma hashtag."""

    tag: str

    kind = "hashtag"

    @property
    def slug(self) -> str:
        return f"tag-{self.tag}"


Target = ProfileTarget | PostTarget | HashtagTarget


def shortcode_to_media_id(shortcode: str) -> int:
    """Converte shortcode em media_id. Deterministico - nao precisa de rede."""
    if not shortcode:
        raise ScrapeError("shortcode vazio")
    total = 0
    for char in shortcode:
        posicao = SHORTCODE_ALPHABET.find(char)
        if posicao < 0:
            raise ScrapeError(
                f"shortcode invalido: caractere {char!r} nao pertence ao "
                f"alfabeto do Instagram"
            )
        total = total * 64 + posicao
    return total


def parse_target(raw: str) -> Target:
    """Link, `@handle` ou `#tag` -> alvo tipado. Levanta `ScrapeError` no resto."""
    texto = (raw or "").strip()
    if not texto:
        raise ScrapeError("link vazio: cole a URL do perfil, do post ou da hashtag")

    if texto.startswith("@"):
        return _perfil(texto[1:])
    if texto.startswith("#"):
        return _hashtag(texto[1:])

    # Handle solto: sem barra, sem ponto, sem esquema.
    if "/" not in texto and "." not in texto and ":" not in texto:
        return _perfil(texto)

    candidato = texto if "://" in texto else f"https://{texto}"
    url = urlparse(candidato)
    host = (url.netloc or "").lower().removeprefix("www.")
    if host not in {"instagram.com", "instagr.am", "m.instagram.com"}:
        raise ScrapeError(
            f"esta ferramenta so entende links do instagram.com; recebi {host or texto!r}"
        )

    partes = [p for p in url.path.split("/") if p]
    if not partes:
        raise ScrapeError(
            "a URL nao aponta para nada: use instagram.com/<perfil>, "
            "instagram.com/p/<codigo> ou instagram.com/explore/tags/<tag>"
        )

    primeiro = partes[0].lower()

    if primeiro == "p":
        if len(partes) < 2:
            raise ScrapeError("URL de post sem codigo depois de /p/")
        return PostTarget(shortcode=partes[1])

    if primeiro in {"reel", "reels", "tv"}:
        raise ScrapeError(
            "Reel nao entra: video nao e referencia de imagem estatica, e a capa "
            "de um Reel e um frame, nao uma foto composta. Se quiser a imagem, "
            "cole o link de um post do feed (/p/<codigo>)."
        )

    if primeiro == "stories":
        raise ScrapeError("Stories nao entra: e efemero e nao tem proveniencia estavel")

    if primeiro == "explore":
        if len(partes) >= 3 and partes[1].lower() == "tags":
            return _hashtag(partes[2])
        raise ScrapeError(
            "de /explore/ so entendo hashtag: instagram.com/explore/tags/<tag>"
        )

    if primeiro in _RESERVADOS:
        raise ScrapeError(f"/{primeiro}/ nao e um perfil, e uma rota interna do Instagram")

    return _perfil(partes[0])


def _perfil(handle: str) -> ProfileTarget:
    limpo = handle.strip().strip("/")
    if not _HANDLE_RE.match(limpo):
        raise ScrapeError(
            f"handle invalido: {handle!r} (esperado ate 30 caracteres entre "
            f"letras, numeros, ponto e underscore)"
        )
    if limpo.lower() in _RESERVADOS:
        raise ScrapeError(f"{limpo!r} e uma rota interna do Instagram, nao um perfil")
    return ProfileTarget(handle=limpo)


def _hashtag(tag: str) -> HashtagTarget:
    limpo = tag.strip().strip("/").lstrip("#")
    if not _TAG_RE.match(limpo):
        raise ScrapeError(f"hashtag invalida: {tag!r}")
    return HashtagTarget(tag=limpo)
