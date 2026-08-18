"""Traducao de um link (ou handle solto) no alvo tipado da raspagem.

Puro: nao toca rede, nao importa Playwright, nao le disco. Recebe string e
devolve alvo - e por isso da para testar o formato inteiro sem abrir browser.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import ClassVar, Literal
from urllib.parse import urlparse

from ..errors import ScrapeError

#: Alfabeto posicional que o Instagram usa para codificar media_id em shortcode.
SHORTCODE_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

#: Handle real do Instagram: 1 a 30 caracteres, sem ponto na ponta nem ponto
#: duplo - o slug vira nome de diretorio, entao ".." nao pode passar.
_HANDLE_RE = re.compile(r"^(?!.*\.\.)[A-Za-z0-9_](?:[A-Za-z0-9._]{0,28}[A-Za-z0-9_])?$")
#: Allowlist de caracteres de palavra (letras/digitos/underscore, unicode
#: incluso) - evita ':', '*', '<', '>', '|', '\' que o Windows nao aceita
#: em nome de arquivo.
_TAG_RE = re.compile(r"^\w{1,100}$")

#: Hosts do Instagram aceitos - usado tanto no atalho de host puro quanto na
#: validacao da URL completa.
_HOSTS = {"instagram.com", "instagr.am", "m.instagram.com"}

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

    kind: ClassVar[Literal["profile"]] = "profile"

    @property
    def slug(self) -> str:
        return self.handle


@dataclass(frozen=True)
class PostTarget:
    """Um post especifico, carrossel incluso."""

    shortcode: str

    kind: ClassVar[Literal["post"]] = "post"

    @property
    def slug(self) -> str:
        return f"post-{self.shortcode}"


@dataclass(frozen=True)
class HashtagTarget:
    """Uma hashtag."""

    tag: str

    kind: ClassVar[Literal["hashtag"]] = "hashtag"

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

    # Sem barra e sem esquema: so pode ser handle - handles com ponto sao comuns.
    if "/" not in texto and ":" not in texto:
        if texto.lower().removeprefix("www.") in _HOSTS:
            raise ScrapeError(
                "a URL nao aponta para nada: use instagram.com/<perfil>, "
                "instagram.com/p/<codigo> ou instagram.com/explore/tags/<tag>"
            )
        return _perfil(texto)

    if "://" in texto:
        candidato = texto
    elif texto.startswith("//"):
        # URL protocol-relative (comum em copia-e-cola) - prefixo sem as barras.
        candidato = f"https:{texto}"
    else:
        candidato = f"https://{texto}"

    try:
        url = urlparse(candidato)
    except ValueError as erro:
        raise ScrapeError(f"link malformado, nao consegui interpretar {texto!r}: {erro}") from erro

    if url.scheme and url.scheme not in ("http", "https"):
        raise ScrapeError(
            f"esquema {url.scheme!r} nao e suportado: use um link http(s) do instagram.com"
        )

    host = (url.netloc or "").lower().removeprefix("www.")
    if host not in _HOSTS:
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
        shortcode = partes[1]
        for char in shortcode:
            if char not in SHORTCODE_ALPHABET:
                raise ScrapeError(
                    f"shortcode invalido em {shortcode!r}: caractere {char!r} nao "
                    f"pertence ao alfabeto do Instagram"
                )
        return PostTarget(shortcode=shortcode)

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
