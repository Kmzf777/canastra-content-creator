"""Cliente da xAI sob teste: nenhuma chamada real, nenhum sleep real.

Todo cenario passa por `httpx.MockTransport`; o backoff usa um sleeper falso
que so anota os intervalos. O teste mais importante do arquivo e o ultimo:
a chave da API nao pode aparecer em mensagem, `raw` ou `repr`, nem quando o
proprio servidor a devolve no corpo do erro.
"""

from __future__ import annotations

import asyncio
import base64
import json
from typing import Any, Callable

import httpx
import pytest

from cie.errors import RateLimitError, XaiApiError
from cie.xai import (
    GeneratedImage,
    ImageRequest,
    XaiClient,
    collect_bytes,
    data_uri,
)

BASE_URL = "https://api.test/v1"
ENV_KEY = "xai-env-key-ABCDEF0123456789"
PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmM"
    "IQAAAABJRU5ErkJggg=="
)
PNG_B64 = base64.b64encode(PNG_BYTES).decode()


# --------------------------------------------------------------------------- #
# apoio
# --------------------------------------------------------------------------- #


class Recorder:
    """Roteiro de respostas: entrega uma por chamada, repetindo a ultima."""

    def __init__(self, script: list[Any]) -> None:
        self.script = script
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        item = self.script[min(len(self.requests) - 1, len(self.script) - 1)]
        if isinstance(item, type) and issubclass(item, Exception):
            raise item("falha de rede simulada", request=request)
        if callable(item) and not isinstance(item, httpx.Response):
            return item(request)
        return item

    @property
    def calls(self) -> int:
        return len(self.requests)

    def body(self, index: int = 0) -> dict[str, Any]:
        return json.loads(self.requests[index].content.decode())


class FakeSleeper:
    """Substitui asyncio.sleep: anota o intervalo e devolve o controle na hora."""

    def __init__(self) -> None:
        self.delays: list[float] = []

    async def __call__(self, delay: float) -> None:
        self.delays.append(delay)


class FixedRandom:
    """rng deterministico: random() sempre devolve o mesmo valor."""

    def __init__(self, value: float = 1.0) -> None:
        self.value = value

    def random(self) -> float:
        return self.value


def image_payload(items: list[dict[str, Any]] | None = None, model: str = "grok-imagine-image"):
    return {"model": model, "data": items if items is not None else [{"b64_json": PNG_B64}]}


def make_client(
    script: list[Any],
    *,
    max_retries: int = 5,
    api_key: str | None = None,
) -> tuple[XaiClient, Recorder, FakeSleeper]:
    recorder = Recorder(script)
    sleeper = FakeSleeper()
    client = XaiClient(
        api_key=api_key,
        base_url=BASE_URL,
        max_retries=max_retries,
        transport=httpx.MockTransport(recorder),
        sleeper=sleeper,
        rng=FixedRandom(1.0),
    )
    return client, recorder, sleeper


def run(coro) -> Any:
    return asyncio.run(coro)


def request(**overrides: Any) -> ImageRequest:
    payload: dict[str, Any] = {
        "model": "grok-imagine-image",
        "prompt": "tambor de torrefacao em luz lateral quente",
    }
    payload.update(overrides)
    return ImageRequest(**payload)


@pytest.fixture(autouse=True)
def api_key_in_env(monkeypatch: pytest.MonkeyPatch) -> str:
    monkeypatch.setenv("XAI_API_KEY", ENV_KEY)
    return ENV_KEY


# --------------------------------------------------------------------------- #
# ImageRequest.to_payload
# --------------------------------------------------------------------------- #


def test_to_payload_omits_none_fields() -> None:
    payload = request().to_payload()
    assert payload == {
        "model": "grok-imagine-image",
        "prompt": "tambor de torrefacao em luz lateral quente",
        "n": 1,
        "response_format": "b64_json",
    }
    assert "aspect_ratio" not in payload
    assert "seed" not in payload


def test_to_payload_includes_optional_fields_when_set() -> None:
    payload = request(aspect_ratio="9:16", seed=42, n=3).to_payload()
    assert payload["aspect_ratio"] == "9:16"
    assert payload["seed"] == 42
    assert payload["n"] == 3


def test_to_payload_merges_extra_last() -> None:
    # extra so e preenchido depois que a sondagem confirmou o campo; por isso
    # ele tem a ultima palavra sobre o corpo enviado.
    payload = request(
        aspect_ratio="1:1",
        extra={"image": PNG_B64, "aspect_ratio": "16:9"},
    ).to_payload()
    assert payload["image"] == PNG_B64
    assert payload["aspect_ratio"] == "16:9"


# --------------------------------------------------------------------------- #
# caminho feliz
# --------------------------------------------------------------------------- #


def test_generate_images_success_b64() -> None:
    client, recorder, sleeper = make_client([httpx.Response(200, json=image_payload())])

    response = run(client.generate_images(request(aspect_ratio="9:16")))
    run(client.aclose())

    assert len(response.images) == 1
    assert response.model == "grok-imagine-image"
    assert response.images[0].to_bytes() == PNG_BYTES
    assert collect_bytes(response) == [PNG_BYTES]
    assert sleeper.delays == []
    assert recorder.calls == 1

    sent = recorder.requests[0]
    assert sent.url.path.endswith("/images/generations")
    assert sent.headers["authorization"] == f"Bearer {ENV_KEY}"
    assert recorder.body()["aspect_ratio"] == "9:16"


def test_generate_images_success_with_url_only() -> None:
    payload = image_payload(
        [{"url": "https://cdn.test/img.png", "revised_prompt": "prompt reescrito"}]
    )
    client, _, _ = make_client([httpx.Response(200, json=payload)])

    response = run(client.generate_images(request()))
    run(client.aclose())

    image = response.images[0]
    assert image.url == "https://cdn.test/img.png"
    assert image.b64 is None
    assert image.revised_prompt == "prompt reescrito"
    # Sem bytes nao ha sha256 nem proveniencia: o cliente recusa em vez de fingir.
    with pytest.raises(XaiApiError) as excinfo:
        image.to_bytes()
    assert "url" in str(excinfo.value)


def test_generate_images_multiple_items() -> None:
    payload = image_payload([{"b64_json": PNG_B64}, {"b64_json": PNG_B64}])
    client, _, _ = make_client([httpx.Response(200, json=payload)])
    response = run(client.generate_images(request(n=2)))
    run(client.aclose())
    assert len(response) == 2


# --------------------------------------------------------------------------- #
# retry
# --------------------------------------------------------------------------- #


def test_rate_limit_with_retry_after_then_success() -> None:
    client, recorder, sleeper = make_client(
        [
            httpx.Response(429, headers={"Retry-After": "7"}, json={"error": "slow down"}),
            httpx.Response(200, json=image_payload()),
        ]
    )

    response = run(client.generate_images(request()))
    run(client.aclose())

    assert len(response.images) == 1
    assert recorder.calls == 2
    # Retry-After numerico e obedecido tal qual, sem jitter por cima.
    assert sleeper.delays == [7.0]


def test_rate_limit_with_non_numeric_retry_after_uses_backoff() -> None:
    client, _, sleeper = make_client(
        [
            httpx.Response(
                429,
                headers={"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"},
                json={"error": "slow down"},
            ),
            httpx.Response(200, json=image_payload()),
        ]
    )

    run(client.generate_images(request()))
    run(client.aclose())

    assert sleeper.delays == [1.0]


def test_rate_limit_exhausts_retries() -> None:
    body = {"error": {"message": "rate limit exceeded for grok-imagine-image"}}
    client, recorder, sleeper = make_client(
        [httpx.Response(429, headers={"Retry-After": "3"}, json=body)],
        max_retries=2,
    )

    with pytest.raises(RateLimitError) as excinfo:
        run(client.generate_images(request()))
    run(client.aclose())

    error = excinfo.value
    assert error.status_code == 429
    assert error.retry_after == 3.0
    assert "rate limit exceeded" in error.raw
    assert recorder.calls == 3  # 1 tentativa + 2 retentativas
    assert sleeper.delays == [3.0, 3.0]


def test_server_error_succeeds_on_third_attempt() -> None:
    client, recorder, sleeper = make_client(
        [
            httpx.Response(500, text="upstream boom"),
            httpx.Response(503, text="temporariamente indisponivel"),
            httpx.Response(200, json=image_payload()),
        ]
    )

    response = run(client.generate_images(request()))
    run(client.aclose())

    assert len(response.images) == 1
    assert recorder.calls == 3
    assert sleeper.delays == [1.0, 2.0]  # exponencial: 1s, 2s


def test_server_error_exhausted_raises_with_body() -> None:
    client, recorder, _ = make_client([httpx.Response(502, text="bad gateway")], max_retries=1)

    with pytest.raises(XaiApiError) as excinfo:
        run(client.generate_images(request()))
    run(client.aclose())

    assert excinfo.value.status_code == 502
    assert "bad gateway" in excinfo.value.raw
    assert recorder.calls == 2


def test_client_error_is_not_retried() -> None:
    body = {"error": {"message": "unknown parameter: reference_images"}}
    client, recorder, sleeper = make_client([httpx.Response(400, json=body)])

    with pytest.raises(XaiApiError) as excinfo:
        run(client.generate_images(request(extra={"reference_images": [PNG_B64]})))
    run(client.aclose())

    error = excinfo.value
    assert error.status_code == 400
    assert not isinstance(error, RateLimitError)
    assert "unknown parameter" in str(error)
    assert "reference_images" in error.raw
    # Pedido errado nao melhora com insistencia: uma chamada, zero espera.
    assert recorder.calls == 1
    assert sleeper.delays == []


@pytest.mark.parametrize("status", [401, 403, 404, 422])
def test_other_client_errors_fail_fast(status: int) -> None:
    client, recorder, _ = make_client([httpx.Response(status, text="nope")])
    with pytest.raises(XaiApiError) as excinfo:
        run(client.generate_images(request()))
    run(client.aclose())
    assert excinfo.value.status_code == status
    assert recorder.calls == 1


def test_network_timeout_is_retried() -> None:
    client, recorder, sleeper = make_client(
        [httpx.ReadTimeout, httpx.ConnectError, httpx.Response(200, json=image_payload())]
    )

    response = run(client.generate_images(request()))
    run(client.aclose())

    assert len(response.images) == 1
    assert recorder.calls == 3
    assert sleeper.delays == [1.0, 2.0]


def test_network_timeout_exhausted_raises_xai_api_error() -> None:
    client, recorder, _ = make_client([httpx.ReadTimeout], max_retries=2)

    with pytest.raises(XaiApiError) as excinfo:
        run(client.generate_images(request()))
    run(client.aclose())

    assert "rede" in str(excinfo.value)
    assert "ReadTimeout" in str(excinfo.value)
    assert recorder.calls == 3


def test_backoff_is_capped_at_thirty_seconds() -> None:
    client, _, sleeper = make_client([httpx.Response(500, text="boom")], max_retries=8)

    with pytest.raises(XaiApiError):
        run(client.generate_images(request()))
    run(client.aclose())

    assert sleeper.delays == [1.0, 2.0, 4.0, 8.0, 16.0, 30.0, 30.0, 30.0]
    assert max(sleeper.delays) <= 30.0


def test_jitter_keeps_delay_between_half_and_full() -> None:
    recorder = Recorder([httpx.Response(500, text="boom"), httpx.Response(200, json=image_payload())])
    sleeper = FakeSleeper()
    client = XaiClient(
        base_url=BASE_URL,
        transport=httpx.MockTransport(recorder),
        sleeper=sleeper,
        rng=FixedRandom(0.0),
    )
    run(client.generate_images(request()))
    run(client.aclose())
    assert sleeper.delays == [0.5]


def test_zero_retries_fails_on_first_error() -> None:
    client, recorder, sleeper = make_client([httpx.Response(500, text="boom")], max_retries=0)
    with pytest.raises(XaiApiError):
        run(client.generate_images(request()))
    run(client.aclose())
    assert recorder.calls == 1
    assert sleeper.delays == []


# --------------------------------------------------------------------------- #
# payload malformado
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "payload,expected",
    [
        ({"model": "grok-imagine-image"}, "sem a chave 'data'"),
        ({"data": []}, "'data' vazio"),
        ({"data": {"b64_json": PNG_B64}}, "esperado lista"),
        ({"data": [{"revised_prompt": "so texto"}]}, "nem 'url'"),
        ({"data": ["string solta"]}, "esperado objeto"),
    ],
)
def test_malformed_payload_raises_explained_error(payload: dict[str, Any], expected: str) -> None:
    client, _, _ = make_client([httpx.Response(200, json=payload)])

    with pytest.raises(XaiApiError) as excinfo:
        run(client.generate_images(request()))
    run(client.aclose())

    error = excinfo.value
    assert expected in str(error)
    # O corpo bruto sobrevive para auditoria.
    assert error.raw
    assert json.loads(error.raw) == payload


def test_non_json_body_raises_xai_api_error() -> None:
    client, _, _ = make_client([httpx.Response(200, text="<html>gateway</html>")])
    with pytest.raises(XaiApiError) as excinfo:
        run(client.generate_images(request()))
    run(client.aclose())
    assert "nao e JSON" in str(excinfo.value)
    assert "<html>" in excinfo.value.raw


def test_invalid_base64_raises_instead_of_binascii_error() -> None:
    image = GeneratedImage(b64="isto nao e base64!!")
    with pytest.raises(XaiApiError):
        image.to_bytes()


def test_image_without_anything_raises() -> None:
    with pytest.raises(XaiApiError):
        GeneratedImage().to_bytes()


# --------------------------------------------------------------------------- #
# chat, models e ciclo de vida
# --------------------------------------------------------------------------- #


def test_list_models_extracts_ids() -> None:
    payload = {
        "data": [
            {"id": "grok-imagine-image"},
            {"id": "grok-4-vision"},
            {"id": "grok-imagine-image"},  # duplicado: sai uma vez so
        ]
    }
    client, recorder, _ = make_client([httpx.Response(200, json=payload)])
    models = run(client.list_models())
    run(client.aclose())

    assert models == ["grok-imagine-image", "grok-4-vision"]
    assert recorder.requests[0].method == "GET"
    assert recorder.requests[0].url.path.endswith("/models")


def test_list_models_without_data_raises() -> None:
    client, _, _ = make_client([httpx.Response(200, json={"models": []})])
    with pytest.raises(XaiApiError):
        run(client.list_models())
    run(client.aclose())


def test_chat_completion_sends_expected_payload() -> None:
    answer = {"choices": [{"message": {"content": "{\"mood\": \"calmo\"}"}}]}
    client, recorder, _ = make_client([httpx.Response(200, json=answer)])

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "descreva o estilo"},
                {"type": "image_url", "image_url": {"url": data_uri(PNG_BYTES)}},
            ],
        }
    ]
    result = run(
        client.chat_completion(
            "grok-4-vision",
            messages,
            response_format={"type": "json_object"},
            max_tokens=512,
        )
    )
    run(client.aclose())

    assert result == answer
    body = recorder.body()
    assert body["model"] == "grok-4-vision"
    assert body["temperature"] == 0.0
    assert body["max_tokens"] == 512
    assert body["response_format"] == {"type": "json_object"}
    assert body["messages"][0]["content"][1]["image_url"]["url"].startswith(
        "data:image/png;base64,"
    )


def test_chat_completion_omits_optional_fields() -> None:
    client, recorder, _ = make_client([httpx.Response(200, json={"choices": []})])
    run(client.chat_completion("grok-4", [{"role": "user", "content": "oi"}]))
    run(client.aclose())
    body = recorder.body()
    assert "max_tokens" not in body
    assert "response_format" not in body


def test_async_context_manager_closes_the_transport() -> None:
    recorder = Recorder([httpx.Response(200, json=image_payload())])

    async def scenario() -> bool:
        async with XaiClient(
            base_url=BASE_URL,
            transport=httpx.MockTransport(recorder),
            sleeper=FakeSleeper(),
        ) as client:
            await client.generate_images(request())
            inner = client
        return inner._client.is_closed

    assert run(scenario()) is True


def test_missing_api_key_fails_loud(monkeypatch: pytest.MonkeyPatch) -> None:
    # Neutraliza o .env do desenvolvedor: sem isto o teste leria a chave real.
    monkeypatch.setattr("cie.config.load_dotenv", lambda *args, **kwargs: False)
    monkeypatch.delenv("XAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError) as excinfo:
        XaiClient(base_url=BASE_URL, transport=httpx.MockTransport(Recorder([])))
    assert "XAI_API_KEY" in str(excinfo.value)


# --------------------------------------------------------------------------- #
# a chave nunca vaza
# --------------------------------------------------------------------------- #


def test_api_key_never_appears_in_errors_or_repr() -> None:
    param_key = "xai-param-key-ZZZ987654321"
    # Pior caso possivel: o servidor devolve as duas chaves no corpo do erro.
    leaky = {
        "error": {
            "message": f"invalid request with Authorization Bearer {param_key} and {ENV_KEY}"
        }
    }
    # (roteiro, excecao esperada, o corpo carregava a chave?)
    scenarios: list[tuple[list[Any], type[Exception], bool]] = [
        ([httpx.Response(400, json=leaky)], XaiApiError, True),
        ([httpx.Response(500, json=leaky)], XaiApiError, True),
        ([httpx.Response(429, json=leaky)], RateLimitError, True),
        ([httpx.Response(200, json={"data": [], "echo": leaky})], XaiApiError, True),
        ([httpx.Response(200, text=json.dumps(leaky)[:20])], XaiApiError, False),
    ]

    for script, expected, key_in_body in scenarios:
        client, _, _ = make_client(script, max_retries=1, api_key=param_key)
        with pytest.raises(expected) as excinfo:
            run(client.generate_images(request()))
        run(client.aclose())

        error = excinfo.value
        surfaces = [str(error), getattr(error, "raw", ""), repr(client), repr(error)]
        for surface in surfaces:
            assert param_key not in surface
            assert ENV_KEY not in surface
        if key_in_body:
            # A chave nao some sem deixar rastro: o marcador prova a redacao.
            assert "REDACTED" in error.raw or "REDACTED" in str(error)


def test_client_repr_has_no_secret() -> None:
    client, _, _ = make_client([httpx.Response(200, json=image_payload())], api_key="xai-secret-1")
    text = repr(client) + repr(vars(client))
    run(client.aclose())
    assert "xai-secret-1" not in text
    assert ENV_KEY not in text
