"""Style DNA sob teste: nenhuma chamada de rede, nenhum modelo real.

O chat com visao entra por um cliente falso (`FakeVisionClient`) e, num caso, por
`httpx.MockTransport` com o `XaiClient` de verdade - para provar que as mensagens
montadas aqui sobrevivem a serializacao do cliente.

Os dois testes que mais importam sao os de politica: foto de pessoa sem
consentimento nao entra no conjunto nem para ser descrita, e o nome do modelo com
visao nunca e adivinhado.
"""

from __future__ import annotations

import asyncio
import base64
import io
import json
import logging
from pathlib import Path
from typing import Any, Mapping, Sequence

import httpx
import pytest
from PIL import Image

from cie import repository
from cie.capabilities import ApiCapabilities
from cie.config import Settings
from cie.dna import (
    DEFAULT_LIMIT,
    DNA_SYSTEM_PROMPT,
    MAX_ASSETS,
    MIN_ASSETS,
    VISION_MODEL_ENV,
    build_vision_messages,
    encode_asset_for_vision,
    extract_message_text,
    extract_style_dna,
    parse_descriptor,
    resolve_vision_model,
    select_assets_for_dna,
    summarize_dna,
)
from cie.enums import Location, Pillar, Sku
from cie.errors import CieError, XaiApiError
from cie.models import Asset, StyleDescriptor, StyleDna
from cie.xai import XaiClient

VISION_MODEL = "modelo-de-visao-de-teste"
BASE_URL = "https://api.test/v1"

DESCRIPTOR_JSON = {
    "palette": ["warm ochre", "roasted brown", "deep green"],
    "light_quality": "hard afternoon sun through open shed doors",
    "lens": "35mm, mild perspective compression, visible corner falloff",
    "texture": "raw jute, oxidised steel, dusty concrete",
    "framing": "handheld working distance, slightly off axis",
    "recurring_materials": ["jute sacks", "stainless drum", "kraft paper"],
    "mood": "working morning, unstaged",
    "avoid": ["plastic gloss", "studio seamless backdrop", "teal and orange grade"],
}


# --------------------------------------------------------------------------- #
# apoio
# --------------------------------------------------------------------------- #


class FakeVisionClient:
    """Guarda o que recebeu e devolve o roteiro combinado, uma resposta por chamada."""

    def __init__(self, script: list[Any] | None = None) -> None:
        self.script = script or [_chat_payload(json.dumps(DESCRIPTOR_JSON))]
        self.calls: list[dict[str, Any]] = []

    async def chat_completion(
        self, model: str, messages: Sequence[Mapping[str, Any]], **kwargs: Any
    ) -> dict[str, Any]:
        self.calls.append({"model": model, "messages": list(messages), "kwargs": kwargs})
        item = self.script[min(len(self.calls) - 1, len(self.script) - 1)]
        if isinstance(item, Exception):
            raise item
        return item


def _chat_payload(content: str) -> dict[str, Any]:
    return {
        "id": "chat-1",
        "model": VISION_MODEL,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}}],
    }


def _run(coro):
    return asyncio.run(coro)


def make_asset(
    conn,
    index: int,
    *,
    path: Path | None = None,
    quality: int = 80,
    reference_grade: bool = True,
    has_person: bool = False,
    consent: bool = False,
    pillar: Pillar | None = Pillar.P3,
) -> int:
    """Insere uma linha de asset. Sem arquivo real quando `path` nao vem."""
    asset = Asset(
        path=str(path) if path else f"/base/foto-{index:03d}.jpg",
        sha256=f"{index:064x}",
        width=2400,
        height=1600,
        pillar=pillar,
        location=Location.TORREFACAO_UBERLANDIA,
        sku=Sku.CLASSICO if index % 3 == 0 else None,
        subject_tags=["grao", "bancada"],
        has_identifiable_person=has_person,
        consent_on_file=consent,
        quality_score=quality,
        is_reference_grade=reference_grade,
        needs_review=False,
    )
    return repository.insert_asset(conn, asset)


@pytest.fixture
def usable_assets(conn, tmp_path: Path, photo_factory) -> list[int]:
    """Dez fotos reais pequenas, todas utilizaveis como referencia."""
    ids: list[int] = []
    for index in range(10):
        path = photo_factory(tmp_path / "base" / f"foto-{index:03d}.jpg", size=(120, 90))
        ids.append(make_asset(conn, index, path=path, quality=90 - index))
    return ids


@pytest.fixture(autouse=True)
def _no_vision_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """A env var de override nunca vaza de fora para dentro do teste."""
    monkeypatch.delenv(VISION_MODEL_ENV, raising=False)


# --------------------------------------------------------------------------- #
# selecao do conjunto
# --------------------------------------------------------------------------- #


def test_selection_keeps_only_reference_grade(conn) -> None:
    for index in range(MIN_ASSETS):
        make_asset(conn, index, quality=90)
    for index in range(100, 105):
        make_asset(conn, index, quality=95, reference_grade=False)

    selected = select_assets_for_dna(conn)

    assert len(selected) == MIN_ASSETS
    assert all(asset.is_reference_grade for asset in selected)


def test_selection_blocks_person_without_consent(conn) -> None:
    for index in range(MIN_ASSETS):
        make_asset(conn, index, quality=70)
    # Melhor qualidade de todas, mas pessoa identificavel sem consentimento.
    blocked = make_asset(conn, 50, quality=99, has_person=True, consent=False)
    allowed = make_asset(conn, 51, quality=98, has_person=True, consent=True)

    selected = select_assets_for_dna(conn)
    ids = [asset.id for asset in selected]

    assert blocked not in ids
    assert allowed in ids


def test_selection_reports_consent_blocks_in_error(conn) -> None:
    for index in range(3):
        make_asset(conn, index, quality=80)
    for index in range(20, 26):
        make_asset(conn, index, quality=95, has_person=True, consent=False)

    with pytest.raises(CieError) as excinfo:
        select_assets_for_dna(conn)

    message = str(excinfo.value)
    assert f"minimo {MIN_ASSETS}" in message
    assert "faltam 5" in message
    assert "consentimento" in message
    assert "reference-grade" in message


def test_selection_shortage_message_names_the_gap(conn) -> None:
    for index in range(4):
        make_asset(conn, index, quality=80)

    with pytest.raises(CieError) as excinfo:
        select_assets_for_dna(conn, pillar=Pillar.P3)

    message = str(excinfo.value)
    assert "faltam 4" in message
    assert "pilar 3" in message
    assert "como resolver" in message


def test_selection_limit_below_minimum_explains_itself(conn) -> None:
    for index in range(MAX_ASSETS):
        make_asset(conn, index, quality=80)

    with pytest.raises(CieError) as excinfo:
        select_assets_for_dna(conn, limit=5)

    assert "--limit (5)" in str(excinfo.value)


def test_selection_caps_at_max_assets(conn) -> None:
    for index in range(MAX_ASSETS + 7):
        make_asset(conn, index, quality=80)

    assert len(select_assets_for_dna(conn, limit=40)) == MAX_ASSETS
    assert len(select_assets_for_dna(conn)) == DEFAULT_LIMIT


def test_selection_orders_by_quality(conn) -> None:
    for index, quality in enumerate([71, 99, 85, 73, 90, 77, 95, 80, 88]):
        make_asset(conn, index, quality=quality)

    scores = [asset.quality_score for asset in select_assets_for_dna(conn)]

    assert scores == sorted(scores, reverse=True)


def test_selection_honours_explicit_ids(conn) -> None:
    ids = [make_asset(conn, index, quality=80) for index in range(12)]
    chosen = ids[:MIN_ASSETS]

    selected = select_assets_for_dna(conn, asset_ids=chosen)

    assert sorted(asset.id for asset in selected) == sorted(chosen)


def test_selection_shortage_message_mentions_explicit_ids(conn) -> None:
    ids = [make_asset(conn, index, quality=80) for index in range(3)]

    with pytest.raises(CieError) as excinfo:
        select_assets_for_dna(conn, asset_ids=ids)

    assert "3 id(s) informado(s)" in str(excinfo.value)


def test_selection_filters_by_pillar(conn) -> None:
    for index in range(MIN_ASSETS):
        make_asset(conn, index, quality=80, pillar=Pillar.P1)
    for index in range(50, 60):
        make_asset(conn, index, quality=80, pillar=Pillar.P3)

    selected = select_assets_for_dna(conn, pillar=Pillar.P1)

    assert len(selected) == MIN_ASSETS
    assert {asset.pillar for asset in selected} == {Pillar.P1}


# --------------------------------------------------------------------------- #
# modelo com visao
# --------------------------------------------------------------------------- #


def test_resolve_vision_model_prefers_env(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(VISION_MODEL_ENV, "modelo-do-ambiente")
    caps = ApiCapabilities(vision_model="modelo-da-sondagem")

    assert resolve_vision_model(caps, settings=settings) == "modelo-do-ambiente"


def test_resolve_vision_model_falls_back_to_capabilities(settings: Settings) -> None:
    caps = ApiCapabilities(probed_at="2026-01-01T00:00:00+00:00", vision_model="grok-sondado")

    assert resolve_vision_model(caps, settings=settings) == "grok-sondado"


def test_resolve_vision_model_without_evidence_raises(settings: Settings) -> None:
    with pytest.raises(CieError) as excinfo:
        resolve_vision_model(ApiCapabilities(), settings=settings)

    message = str(excinfo.value)
    assert "probe_api.py" in message
    assert VISION_MODEL_ENV in message
    # A mensagem nao pode sugerir um nome de modelo: chutar e o erro que ela evita.
    assert "nao chuta" in message


def test_resolve_vision_model_reads_capabilities_file(settings: Settings) -> None:
    from cie import capabilities as capabilities_module

    capabilities_module.save(settings, ApiCapabilities(vision_model="grok-do-arquivo"))

    assert resolve_vision_model(settings=settings) == "grok-do-arquivo"


# --------------------------------------------------------------------------- #
# codificacao das imagens
# --------------------------------------------------------------------------- #


def test_encode_asset_produces_jpeg_data_uri(conn, tmp_path: Path, photo_factory) -> None:
    path = photo_factory(tmp_path / "grande.jpg", size=(800, 600))
    asset_id = make_asset(conn, 1, path=path)
    asset = repository.get_asset(conn, asset_id)

    uri = encode_asset_for_vision(asset, max_side=128)

    assert uri.startswith("data:image/jpeg;base64,")
    decoded = base64.b64decode(uri.split(",", 1)[1])
    with Image.open(io.BytesIO(decoded)) as image:
        assert max(image.size) == 128
        assert image.format == "JPEG"


def test_encode_asset_does_not_upscale(conn, tmp_path: Path, photo_factory) -> None:
    path = photo_factory(tmp_path / "pequena.jpg", size=(120, 90))
    asset = repository.get_asset(conn, make_asset(conn, 2, path=path))

    uri = encode_asset_for_vision(asset)

    decoded = base64.b64decode(uri.split(",", 1)[1])
    with Image.open(io.BytesIO(decoded)) as image:
        assert image.size == (120, 90)


def test_encode_asset_falls_back_to_thumbnail(conn, tmp_path: Path, photo_factory) -> None:
    thumb = photo_factory(tmp_path / "thumb.jpg", size=(64, 48))
    asset = Asset(
        path=str(tmp_path / "raw" / "arquivo.cr2"),  # sem decoder e sem arquivo
        sha256=f"{999:064x}",
        thumb_path=str(thumb),
        is_reference_grade=True,
        has_identifiable_person=False,
    )
    stored = repository.get_asset(conn, repository.insert_asset(conn, asset))

    assert encode_asset_for_vision(stored).startswith("data:image/jpeg;base64,")


def test_encode_asset_without_any_readable_file_raises(conn, tmp_path: Path) -> None:
    asset = Asset(path=str(tmp_path / "sumiu.jpg"), sha256=f"{1234:064x}")

    with pytest.raises(CieError) as excinfo:
        encode_asset_for_vision(asset)

    assert "sumiu.jpg" in str(excinfo.value)


# --------------------------------------------------------------------------- #
# mensagens
# --------------------------------------------------------------------------- #


def test_build_vision_messages_shape(conn, usable_assets) -> None:
    assets = select_assets_for_dna(conn, limit=MIN_ASSETS)

    messages = build_vision_messages(assets, extra_instructions="Foque na bancada.")

    assert messages[0] == {"role": "system", "content": DNA_SYSTEM_PROMPT}
    content = messages[1]["content"]
    assert content[0]["type"] == "text"
    assert "Foque na bancada." in content[0]["text"]
    images = [block for block in content if block["type"] == "image_url"]
    assert len(images) == len(assets)
    # Nada alem de `url` no bloco de imagem: campo nao confirmado nao viaja.
    assert all(set(block["image_url"]) == {"url"} for block in images)


def test_system_prompt_demands_bare_json_in_the_schema() -> None:
    for key in StyleDescriptor.model_fields:
        assert key in DNA_SYSTEM_PROMPT
    assert "JSON" in DNA_SYSTEM_PROMPT
    assert "nothing else" in DNA_SYSTEM_PROMPT
    # Precisa mandar descrever o real, nao um ideal generico.
    assert "actually" in DNA_SYSTEM_PROMPT


def test_build_vision_messages_without_assets_raises() -> None:
    with pytest.raises(CieError):
        build_vision_messages([])


# --------------------------------------------------------------------------- #
# parse
# --------------------------------------------------------------------------- #


def test_parse_plain_json() -> None:
    descriptor = parse_descriptor(json.dumps(DESCRIPTOR_JSON))

    assert descriptor.palette == DESCRIPTOR_JSON["palette"]
    assert descriptor.mood == DESCRIPTOR_JSON["mood"]
    assert descriptor.avoid == DESCRIPTOR_JSON["avoid"]


def test_parse_markdown_fence() -> None:
    raw = "Claro! Aqui esta:\n\n```json\n" + json.dumps(DESCRIPTOR_JSON) + "\n```\n"

    assert parse_descriptor(raw).lens == DESCRIPTOR_JSON["lens"]


def test_parse_prose_around_the_object() -> None:
    raw = (
        "Depois de olhar as 12 fotos, este e o descritor:\n"
        + json.dumps(DESCRIPTOR_JSON)
        + "\nEspero ter ajudado."
    )

    assert parse_descriptor(raw).texture == DESCRIPTOR_JSON["texture"]


def test_parse_ignores_unknown_keys_and_logs(caplog: pytest.LogCaptureFixture) -> None:
    payload = dict(DESCRIPTOR_JSON, confidence=0.9, notes="tudo certo")

    with caplog.at_level(logging.WARNING, logger="cie.dna"):
        descriptor = parse_descriptor(json.dumps(payload))

    assert descriptor.framing == DESCRIPTOR_JSON["framing"]
    assert "confidence" in caplog.text
    assert "notes" in caplog.text


def test_parse_coerces_list_given_as_text() -> None:
    payload = dict(DESCRIPTOR_JSON, palette="warm ochre, roasted brown; deep green")

    assert parse_descriptor(json.dumps(payload)).palette == [
        "warm ochre",
        "roasted brown",
        "deep green",
    ]


def test_parse_coerces_text_given_as_list() -> None:
    payload = dict(DESCRIPTOR_JSON, mood=["working morning", "unstaged"])

    assert parse_descriptor(json.dumps(payload)).mood == "working morning; unstaged"


def test_parse_coerces_scalar_given_as_list_field() -> None:
    payload = dict(DESCRIPTOR_JSON, palette=1998)

    assert parse_descriptor(json.dumps(payload)).palette == ["1998"]


def test_parse_survives_braces_and_quotes_inside_strings() -> None:
    payload = dict(DESCRIPTOR_JSON, mood='luz "dura" com sombra em {bloco}')
    raw = "Analise pronta.\n" + json.dumps(payload) + "\nFim."

    assert parse_descriptor(raw).mood == 'luz "dura" com sombra em {bloco}'


def test_parse_accepts_partial_object() -> None:
    descriptor = parse_descriptor('{"palette": ["ocre"], "mood": "calmo"}')

    assert descriptor.palette == ["ocre"]
    assert descriptor.lens == ""


def test_parse_invalid_json_raises_with_snippet() -> None:
    raw = "desculpe, nao consegui analisar as imagens"

    with pytest.raises(CieError) as excinfo:
        parse_descriptor(raw)

    assert raw in str(excinfo.value)


def test_parse_empty_answer_raises() -> None:
    with pytest.raises(CieError) as excinfo:
        parse_descriptor("   ")

    assert "<vazio>" in str(excinfo.value)


def test_parse_json_list_is_not_a_descriptor() -> None:
    with pytest.raises(CieError):
        parse_descriptor('["warm ochre", "roasted brown"]')


# --------------------------------------------------------------------------- #
# leitura da resposta de chat
# --------------------------------------------------------------------------- #


def test_extract_message_text_accepts_block_content() -> None:
    payload = {
        "choices": [
            {"message": {"content": [{"type": "text", "text": "{\"mood\": \"seco\"}"}]}}
        ]
    }

    assert "seco" in extract_message_text(payload)


def test_extract_message_text_without_choices_raises() -> None:
    with pytest.raises(XaiApiError):
        extract_message_text({"error": "nada aqui"})


def test_extract_message_text_with_empty_content_raises() -> None:
    with pytest.raises(XaiApiError):
        extract_message_text({"choices": [{"message": {"content": ""}}]})


# --------------------------------------------------------------------------- #
# extracao ponta a ponta
# --------------------------------------------------------------------------- #


def test_extract_style_dna_persists_profile(
    conn, settings: Settings, usable_assets, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(VISION_MODEL_ENV, VISION_MODEL)
    client = FakeVisionClient()

    dna = _run(
        extract_style_dna(
            client,
            conn,
            name="laboratorio-uberlandia",
            pillar=Pillar.P3,
            limit=MIN_ASSETS,
            settings=settings,
        )
    )

    assert isinstance(dna, StyleDna)
    assert dna.id is not None
    assert dna.pillar is Pillar.P3
    assert len(dna.source_asset_ids) == MIN_ASSETS
    assert dna.prompt_fragment.strip()
    assert "warm ochre" in dna.prompt_fragment
    # `avoid` e negative: fica no descritor, nunca no fragmento positivo.
    assert "plastic gloss" not in dna.prompt_fragment

    stored = repository.get_style_dna_by_name(conn, "laboratorio-uberlandia")
    assert stored is not None
    assert stored.descriptor == dna.descriptor
    assert stored.source_asset_ids == dna.source_asset_ids

    assert client.calls[0]["model"] == VISION_MODEL
    images = [
        block
        for block in client.calls[0]["messages"][1]["content"]
        if block["type"] == "image_url"
    ]
    assert len(images) == MIN_ASSETS


def test_extract_style_dna_upserts_by_name(
    conn, settings: Settings, usable_assets, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(VISION_MODEL_ENV, VISION_MODEL)
    second = dict(DESCRIPTOR_JSON, mood="tarde silenciosa")
    client = FakeVisionClient(
        [
            _chat_payload(json.dumps(DESCRIPTOR_JSON)),
            _chat_payload("```json\n" + json.dumps(second) + "\n```"),
        ]
    )

    first = _run(extract_style_dna(client, conn, name="terroir", limit=MIN_ASSETS, settings=settings))
    again = _run(extract_style_dna(client, conn, name="terroir", limit=MIN_ASSETS, settings=settings))

    assert again.id == first.id
    assert again.descriptor.mood == "tarde silenciosa"
    assert len(repository.list_style_dna(conn)) == 1


def test_extract_style_dna_uses_explicit_model(
    conn, settings: Settings, usable_assets
) -> None:
    client = FakeVisionClient()

    _run(
        extract_style_dna(
            client, conn, name="perfil", limit=MIN_ASSETS, model="modelo-passado-na-mao",
            settings=settings,
        )
    )

    assert client.calls[0]["model"] == "modelo-passado-na-mao"


def test_extract_style_dna_without_model_never_calls_api(
    conn, settings: Settings, usable_assets
) -> None:
    client = FakeVisionClient()

    with pytest.raises(CieError):
        _run(extract_style_dna(client, conn, name="perfil", limit=MIN_ASSETS, settings=settings))

    assert client.calls == []


def test_extract_style_dna_with_broken_json_raises_and_saves_nothing(
    conn, settings: Settings, usable_assets, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(VISION_MODEL_ENV, VISION_MODEL)
    client = FakeVisionClient([_chat_payload("nao consegui ler as imagens, desculpe")])

    with pytest.raises(CieError) as excinfo:
        _run(extract_style_dna(client, conn, name="perfil", limit=MIN_ASSETS, settings=settings))

    assert "nao consegui ler as imagens" in str(excinfo.value)
    assert repository.list_style_dna(conn) == []


def test_extract_style_dna_requires_a_name(conn, settings: Settings, usable_assets) -> None:
    with pytest.raises(CieError):
        _run(extract_style_dna(FakeVisionClient(), conn, name="  ", settings=settings))


def test_extract_style_dna_stops_before_the_api_when_set_is_short(
    conn, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(VISION_MODEL_ENV, VISION_MODEL)
    for index in range(3):
        make_asset(conn, index, quality=80)
    client = FakeVisionClient()

    with pytest.raises(CieError):
        _run(extract_style_dna(client, conn, name="perfil", settings=settings))

    assert client.calls == []


def test_extract_style_dna_over_mock_transport(
    conn, settings: Settings, usable_assets, monkeypatch: pytest.MonkeyPatch
) -> None:
    """O mesmo caminho, agora atravessando o `XaiClient` real (sem rede)."""
    monkeypatch.setenv(VISION_MODEL_ENV, VISION_MODEL)
    seen: list[dict[str, Any]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(json.loads(request.content.decode()))
        return httpx.Response(200, json=_chat_payload(json.dumps(DESCRIPTOR_JSON)))

    async def go() -> StyleDna:
        async with XaiClient(
            api_key="chave-de-teste", base_url=BASE_URL, transport=httpx.MockTransport(handler)
        ) as client:
            return await extract_style_dna(
                client, conn, name="fazenda-medeiros", limit=MIN_ASSETS, settings=settings
            )

    dna = _run(go())

    assert dna.descriptor.palette == DESCRIPTOR_JSON["palette"]
    assert seen[0]["model"] == VISION_MODEL
    assert seen[0]["messages"][0]["role"] == "system"
    # `response_format` fica de fora: modo JSON nativo nao foi confirmado nesta API.
    assert "response_format" not in seen[0]


# --------------------------------------------------------------------------- #
# resumo
# --------------------------------------------------------------------------- #


def test_summarize_dna_covers_every_field() -> None:
    dna = StyleDna(
        id=4,
        name="laboratorio-uberlandia",
        pillar=Pillar.P3,
        source_asset_ids=[1, 2, 3],
        descriptor=StyleDescriptor(**DESCRIPTOR_JSON),
        prompt_fragment="fragmento",
    )

    text = summarize_dna(dna)

    assert "laboratorio-uberlandia" in text
    assert "pilar 3" in text
    assert "1, 2, 3" in text
    assert "warm ochre" in text
    assert "plastic gloss" in text
    # Sem colchete: a CLI imprime com markup rich e comeria o trecho.
    assert "[" not in text


def test_summarize_dna_survives_empty_descriptor() -> None:
    dna = StyleDna(name="vazio", descriptor=StyleDescriptor())

    text = summarize_dna(dna)

    assert "vazio" in text
    assert "-" in text
