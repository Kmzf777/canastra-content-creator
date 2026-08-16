"""Cliente httpx async da API da xAI.

Tres compromissos que este modulo cumpre e o resto do sistema assume:

  1. A CHAVE NUNCA VAZA. Ela existe em exatamente dois lugares: o header
     Authorization do `httpx.AsyncClient` e um closure de redacao. Nao vira
     atributo, nao entra em `repr`, e todo texto que vira mensagem ou `raw` de
     excecao passa por `_scrub` antes.
  2. NENHUM PARAMETRO E INVENTADO. `ImageRequest` so envia o que a spec da
     xAI documenta como basico; tudo que depende de sondagem entra por `extra`,
     preenchido por quem leu `cie.capabilities`. Se a capability nao confirmou,
     a chave simplesmente nao vai no corpo.
  3. FALHA NUNCA E ENGOLIDA. Payload torto vira `XaiApiError` com o corpo bruto
     preservado; nunca um `KeyError`/`IndexError` escapando para a CLI.

Politica de retry: exponencial com jitter (base 1s, fator 2, teto 30s), no
maximo `max_retries` retentativas depois da primeira tentativa. Retenta 429
(honrando `Retry-After` numerico), 5xx e falhas de rede/timeout. 4xx que nao
seja 429 falha na hora: pedido errado nao melhora com insistencia, so gasta
credito e tempo.
"""

from __future__ import annotations

import asyncio
import base64
import binascii
import random
import re
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Mapping, Sequence

import httpx

from .config import get_settings, redact
from .config import require_api_key as _require_api_key
from .errors import RateLimitError, XaiApiError
from .utils import dumps

#: Endpoints usados. Caminhos relativos ao base_url (`.../v1`).
IMAGES_ENDPOINT = "/images/generations"
IMAGE_EDITS_ENDPOINT = "/images/edits"
CHAT_ENDPOINT = "/chat/completions"
MODELS_ENDPOINT = "/models"

DEFAULT_TIMEOUT = 120.0
DEFAULT_MAX_RETRIES = 5
BACKOFF_BASE_SECONDS = 1.0
BACKOFF_FACTOR = 2.0
BACKOFF_CEILING_SECONDS = 30.0

#: Quanto do corpo de erro sobrevive em `XaiApiError.raw`. O suficiente para
#: auditar, pouco o bastante para nao despejar um base64 inteiro no terminal.
ERROR_SNIPPET_CHARS = 2000

REDACTED = "***REDACTED***"
USER_AGENT = "canastra-image-engine/0.1"

Sleeper = Callable[[float], Awaitable[None]]


# --------------------------------------------------------------------------- #
# tipos de requisicao e resposta
# --------------------------------------------------------------------------- #


@dataclass
class ImageRequest:
    """Um pedido de imagem. `extra` e a unica porta para campos nao confirmados."""

    model: str
    prompt: str
    n: int = 1
    aspect_ratio: str | None = None
    response_format: str = "b64_json"
    seed: int | None = None
    #: Campos incluidos SO quando `cie.capabilities` provou que a API os aceita
    #: (ex.: {"image": "<b64>"} depois da sondagem confirmar referencia nativa).
    extra: dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": self.prompt,
            "n": self.n,
            "response_format": self.response_format,
            "aspect_ratio": self.aspect_ratio,
            "seed": self.seed,
        }
        payload = {key: value for key, value in payload.items() if value is not None}
        # extra por ultimo: quem sondou a API tem a palavra final sobre o corpo.
        payload.update(self.extra)
        return payload


@dataclass
class GeneratedImage:
    b64: str | None = None
    url: str | None = None
    revised_prompt: str | None = None

    def to_bytes(self) -> bytes:
        if self.b64:
            try:
                return base64.b64decode(_strip_whitespace(self.b64), validate=True)
            except (binascii.Error, ValueError) as exc:
                raise XaiApiError(
                    "a API devolveu b64_json que nao decodifica como base64",
                    raw=redact(str(exc))[:ERROR_SNIPPET_CHARS],
                ) from exc
        if self.url:
            raise XaiApiError(
                "a API devolveu apenas uma url, sem b64_json. O CIE grava bytes "
                "para poder calcular sha256 e proveniencia offline",
                raw=redact(self.url)[:ERROR_SNIPPET_CHARS],
            )
        raise XaiApiError("imagem sem b64_json e sem url: nada para gravar")


@dataclass
class ImageResponse:
    images: list[GeneratedImage]
    model: str
    raw: dict[str, Any]

    def __len__(self) -> int:
        return len(self.images)


# --------------------------------------------------------------------------- #
# cliente
# --------------------------------------------------------------------------- #


class XaiClient:
    """Cliente async da API da xAI com retry, backoff e jitter.

    `sleeper` e `rng` sao injetaveis para o teste nao dormir de verdade;
    `transport` recebe `httpx.MockTransport` na suite.

    Sem `api_key` explicita a chave vem de `config.require_api_key()`, que
    levanta `RuntimeError` na construcao quando ela falta - falhar aqui e melhor
    que descobrir no meio de uma fila de jobs ja parcialmente cobrada.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        transport: httpx.AsyncBaseTransport | None = None,
        sleeper: Sleeper | None = None,
        rng: random.Random | None = None,
    ) -> None:
        key = api_key or _require_api_key()
        self.base_url = (base_url or get_settings().xai_base_url).rstrip("/")
        self.timeout = timeout
        self.max_retries = max(0, int(max_retries))
        self._sleep: Sleeper = sleeper or asyncio.sleep
        self._rng = rng if rng is not None else random.Random()
        # A chave fica so aqui dentro (header + closure de redacao). Nao vira
        # atributo, entao nem `vars()` nem `repr` conseguem revela-la.
        self._scrub: Callable[[str], str] = _make_scrubber(key)
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            transport=transport,
            # Content-Type nao entra aqui de proposito: o httpx deduz por
            # requisicao (json -> application/json, files -> multipart com
            # boundary), e um default fixo no cliente venceria a deducao.
            headers={
                "Authorization": f"Bearer {key}",
                "User-Agent": USER_AGENT,
            },
        )

    def __repr__(self) -> str:
        return (
            f"XaiClient(base_url={self.base_url!r}, timeout={self.timeout!r}, "
            f"max_retries={self.max_retries!r})"
        )

    # -- ciclo de vida ------------------------------------------------------ #

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> XaiClient:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    # -- API publica -------------------------------------------------------- #

    async def generate_images(self, request: ImageRequest) -> ImageResponse:
        data = await self._request_json("POST", IMAGES_ENDPOINT, json_body=request.to_payload())
        return _parse_image_response(data, fallback_model=request.model, scrub=self._scrub)

    async def chat_completion(
        self,
        model: str,
        messages: Sequence[Mapping[str, Any]],
        *,
        response_format: Mapping[str, Any] | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "messages": list(messages),
            "temperature": temperature,
        }
        if response_format is not None:
            payload["response_format"] = dict(response_format)
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        return await self._request_json("POST", CHAT_ENDPOINT, json_body=payload)

    async def list_models(self) -> list[str]:
        data = await self._request_json("GET", MODELS_ENDPOINT)
        return _parse_model_names(data, scrub=self._scrub)

    async def raw_request(
        self,
        method: str,
        path: str,
        *,
        json_body: Any = None,
        data: Mapping[str, Any] | None = None,
        files: Any = None,
        headers: Mapping[str, str] | None = None,
        retry: bool = False,
    ) -> httpx.Response:
        """Escotilha de baixo nivel para `scripts/probe_api.py`.

        A sondagem precisa do status e do corpo de erro EXATOS de campos que
        talvez nem existam - interpretar ou retentar isso destruiria a evidencia.
        Devolve a resposta crua sem levantar em 4xx/5xx. Nenhum caminho de
        producao usa este metodo.
        """
        async def send() -> httpx.Response:
            return await self._client.request(
                method,
                path,
                json=json_body,
                data=data,
                files=files,
                headers=dict(headers) if headers else None,
            )

        if not retry:
            return await send()
        return await self._send_with_retry(method, path, send)

    # -- interno ------------------------------------------------------------ #

    async def _request_json(
        self, method: str, path: str, *, json_body: Any = None
    ) -> dict[str, Any]:
        async def send() -> httpx.Response:
            return await self._client.request(method, path, json=json_body)

        response = await self._send_with_retry(method, path, send)
        return self._decode_json(response, path)

    async def _send_with_retry(
        self,
        method: str,
        path: str,
        send: Callable[[], Awaitable[httpx.Response]],
    ) -> httpx.Response:
        attempt = 0
        while True:
            attempt += 1
            try:
                response = await send()
            except httpx.TransportError as exc:
                # Rede/timeout: sintoma classico de problema transitorio.
                if attempt > self.max_retries:
                    raise XaiApiError(
                        f"falha de rede em {method} {path} apos {attempt} tentativa(s): "
                        f"{type(exc).__name__}",
                        raw=self._snippet(str(exc)),
                    ) from exc
                await self._backoff(attempt)
                continue

            if response.status_code < 400:
                return response

            body = self._snippet(_safe_text(response))

            if response.status_code == 429:
                retry_after = _parse_retry_after(response.headers.get("Retry-After"))
                if attempt > self.max_retries:
                    raise RateLimitError(
                        f"429 em {method} {path}: limite de taxa persistiu apos "
                        f"{attempt} tentativa(s)",
                        retry_after=retry_after,
                        raw=body,
                    )
                await self._backoff(attempt, retry_after=retry_after)
                continue

            if response.status_code >= 500:
                if attempt > self.max_retries:
                    raise XaiApiError(
                        f"{response.status_code} em {method} {path} apos "
                        f"{attempt} tentativa(s)",
                        status_code=response.status_code,
                        raw=body,
                    )
                await self._backoff(attempt)
                continue

            # 4xx que nao e 429: o pedido esta errado. Insistir so gasta tempo.
            raise XaiApiError(
                f"{response.status_code} em {method} {path}: "
                f"{_error_message(response, self._scrub)}",
                status_code=response.status_code,
                raw=body,
            )

    async def _backoff(self, attempt: int, *, retry_after: float | None = None) -> None:
        if retry_after is not None:
            # O servidor disse quando voltar; obedecer e melhor que adivinhar.
            await self._sleep(min(retry_after, BACKOFF_CEILING_SECONDS))
            return
        nominal = min(
            BACKOFF_BASE_SECONDS * (BACKOFF_FACTOR ** (attempt - 1)),
            BACKOFF_CEILING_SECONDS,
        )
        # Jitter parcial: metade fixa (garante progresso) + metade sorteada
        # (evita que varios workers acordem no mesmo milissegundo).
        delay = nominal / 2 + self._rng.random() * (nominal / 2)
        await self._sleep(delay)

    def _decode_json(self, response: httpx.Response, path: str) -> dict[str, Any]:
        try:
            data = response.json()
        except ValueError as exc:
            raise XaiApiError(
                f"{path} respondeu {response.status_code} com corpo que nao e JSON",
                status_code=response.status_code,
                raw=self._snippet(_safe_text(response)),
            ) from exc
        if not isinstance(data, dict):
            raise XaiApiError(
                f"{path} respondeu com JSON do tipo {type(data).__name__}, esperado objeto",
                status_code=response.status_code,
                raw=self._snippet(_safe_text(response)),
            )
        return data

    def _snippet(self, text: str) -> str:
        # Redigir ANTES de truncar: cortar primeiro poderia deixar meia chave.
        return self._scrub(text)[:ERROR_SNIPPET_CHARS]


# --------------------------------------------------------------------------- #
# funcoes auxiliares
# --------------------------------------------------------------------------- #


def _make_scrubber(key: str) -> Callable[[str], str]:
    """Fecha sobre a chave para redigi-la mesmo quando ela nao veio do ambiente."""

    def scrub(text: str) -> str:
        cleaned = redact(text or "")
        if key and key in cleaned:
            cleaned = cleaned.replace(key, REDACTED)
        return cleaned

    return scrub


def _strip_whitespace(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _safe_text(response: httpx.Response) -> str:
    try:
        return response.text
    except Exception:  # corpo em streaming/binario ilegivel
        return f"<{len(response.content)} bytes nao textuais>"


def _parse_retry_after(value: str | None) -> float | None:
    """So aceita Retry-After numerico. Formato HTTP-date cai no backoff normal."""
    if not value:
        return None
    try:
        seconds = float(value.strip())
    except (TypeError, ValueError):
        return None
    return seconds if seconds >= 0 else None


def _error_message(response: httpx.Response, scrub: Callable[[str], str]) -> str:
    """Extrai a mensagem util do corpo de erro sem estourar se o formato mudar."""
    try:
        data = response.json()
    except ValueError:
        return scrub(_safe_text(response))[:300]
    if isinstance(data, dict):
        error = data.get("error")
        if isinstance(error, Mapping):
            message = error.get("message") or error.get("code")
            if message:
                return scrub(str(message))[:300]
        if isinstance(error, str):
            return scrub(error)[:300]
        for key in ("message", "detail", "msg"):
            if isinstance(data.get(key), str):
                return scrub(str(data[key]))[:300]
    return scrub(dumps(data))[:300]


def _parse_image_response(
    data: dict[str, Any],
    *,
    fallback_model: str,
    scrub: Callable[[str], str] = redact,
) -> ImageResponse:
    """Converte o JSON em `ImageResponse` explicando qualquer formato inesperado."""
    raw_text = scrub(dumps(data))[:ERROR_SNIPPET_CHARS]

    items = data.get("data")
    if items is None:
        raise XaiApiError(
            "resposta de imagem sem a chave 'data'; chaves recebidas: "
            f"{sorted(str(k) for k in data)}",
            raw=raw_text,
        )
    if not isinstance(items, list):
        raise XaiApiError(
            f"resposta de imagem com 'data' do tipo {type(items).__name__}, esperado lista",
            raw=raw_text,
        )
    if not items:
        raise XaiApiError(
            "resposta de imagem com 'data' vazio: a API aceitou o pedido mas nao "
            "devolveu imagem alguma",
            raw=raw_text,
        )

    images: list[GeneratedImage] = []
    for index, item in enumerate(items):
        if not isinstance(item, Mapping):
            raise XaiApiError(
                f"item {index} de 'data' e {type(item).__name__}, esperado objeto",
                raw=raw_text,
            )
        b64 = item.get("b64_json")
        url = item.get("url")
        if not b64 and not url:
            raise XaiApiError(
                f"item {index} de 'data' nao traz 'b64_json' nem 'url'; "
                f"campos presentes: {sorted(str(k) for k in item)}",
                raw=raw_text,
            )
        images.append(
            GeneratedImage(
                b64=str(b64) if b64 else None,
                url=str(url) if url else None,
                revised_prompt=(
                    str(item["revised_prompt"]) if item.get("revised_prompt") else None
                ),
            )
        )

    model = data.get("model")
    return ImageResponse(
        images=images,
        model=str(model) if model else fallback_model,
        raw=data,
    )


def _parse_model_names(
    data: Mapping[str, Any], *, scrub: Callable[[str], str] = redact
) -> list[str]:
    items = data.get("data") if isinstance(data, Mapping) else None
    if not isinstance(items, list):
        raise XaiApiError(
            "resposta de /models sem lista em 'data'",
            raw=scrub(dumps(data))[:ERROR_SNIPPET_CHARS],
        )
    names: list[str] = []
    for item in items:
        name: Any = None
        if isinstance(item, Mapping):
            name = item.get("id") or item.get("name")
        elif isinstance(item, str):
            name = item
        if name and str(name) not in names:
            names.append(str(name))
    return names


def data_uri(image_bytes: bytes, mime: str = "image/png") -> str:
    """Monta `data:image/png;base64,...` - formato aceito por chat com visao."""
    return f"data:{mime};base64,{base64.b64encode(image_bytes).decode('ascii')}"


def to_b64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("ascii")


def collect_bytes(response: ImageResponse) -> list[bytes]:
    """Bytes de todas as imagens; erra alto se alguma so tiver url."""
    return [image.to_bytes() for image in response.images]


__all__ = [
    "CHAT_ENDPOINT",
    "IMAGES_ENDPOINT",
    "IMAGE_EDITS_ENDPOINT",
    "MODELS_ENDPOINT",
    "GeneratedImage",
    "ImageRequest",
    "ImageResponse",
    "XaiClient",
    "collect_bytes",
    "data_uri",
    "to_b64",
]
