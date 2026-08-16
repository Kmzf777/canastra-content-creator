"""Estrategias de referencia. Nenhum teste toca a rede: nada aqui instancia
cliente HTTP - o payload e montado e inspecionado offline, que e exatamente o
que o `--dry-run` da CLI faz."""

from __future__ import annotations

import base64
import io
from dataclasses import dataclass
from pathlib import Path

import pytest
from PIL import Image

from cie.capabilities import ApiCapabilities
from cie.errors import CieError
from cie.models import Asset, StyleDescriptor, StyleDna
from cie.reference import (
    DescriptorReferenceStrategy,
    NativeReferenceStrategy,
    RequestPayload,
    choose_strategy,
)
from cie.reference.base import MAX_REFERENCES, prompt_text
from cie.reference.native import MAX_REFERENCE_EDGE

FRAGMENT = (
    "paleta ocre queimado, verde-cafeeiro profundo e ambar de amanhecer; "
    "luz natural lateral suave com sombras longas de golden hour; "
    "50mm equivalente, profundidade de campo rasa; grain fino de filme"
)

DESCRIPTOR = StyleDescriptor(
    palette=["ocre queimado", "verde-cafeeiro profundo"],
    light_quality="luz natural lateral suave",
    lens="50mm equivalente",
    texture="grain fino de filme",
    framing="sujeito descentralizado",
    recurring_materials=["madeira rustica", "aco inox escovado"],
    mood="elegancia rustica e cientifica",
    avoid=["saturacao HDR"],
)


@dataclass
class FakeComposedPrompt:
    """Suficiente para o duck typing de `prompt_text` (o `ComposedPrompt` real
    mora em `cie.prompt`, escrito em paralelo)."""

    text: str


@pytest.fixture
def dna() -> StyleDna:
    return StyleDna(
        id=1,
        name="laboratorio-uberlandia",
        source_asset_ids=[11, 12, 13],
        descriptor=DESCRIPTOR,
        prompt_fragment=FRAGMENT,
    )


def make_asset(
    asset_id: int,
    *,
    path: Path | str = "/base/foto.jpg",
    quality: int | None = 80,
    reference_grade: bool = True,
    person: bool = False,
    consent: bool = False,
) -> Asset:
    return Asset(
        id=asset_id,
        path=str(path),
        sha256=f"{asset_id:064d}",
        quality_score=quality,
        is_reference_grade=reference_grade,
        has_identifiable_person=person,
        consent_on_file=consent,
    )


def probed_caps(**overrides) -> ApiCapabilities:
    """Sondagem que confirmou referencia nativa. So os testes de native usam."""
    base = {
        "probed_at": "2026-08-16T12:00:00+00:00",
        "native_reference_supported": True,
        "reference_field": "image",
        "reference_endpoint": "/images/generations",
        "max_reference_images": 3,
        "reference_encoding": "b64",
        "max_n": 4,
    }
    base.update(overrides)
    return ApiCapabilities(**base)


def decode_reference(value: str) -> Image.Image:
    payload = value.split(",", 1)[1] if value.startswith("data:") else value
    return Image.open(io.BytesIO(base64.b64decode(payload)))


# --------------------------------------------------------------------------- #
# selecao de assets (comum as duas estrategias)
# --------------------------------------------------------------------------- #


def test_select_assets_drops_person_without_consent(dna):
    strategy = DescriptorReferenceStrategy(dna)
    consented = make_asset(1, person=True, consent=True)
    unconsented = make_asset(2, person=True, consent=False)

    selected = strategy.select_assets([consented, unconsented])

    assert [a.id for a in selected] == [1]


def test_select_assets_drops_non_reference_grade(dna):
    strategy = DescriptorReferenceStrategy(dna)
    good = make_asset(1, reference_grade=True)
    weak = make_asset(2, reference_grade=False, quality=99)

    selected = strategy.select_assets([good, weak])

    assert [a.id for a in selected] == [1]


def test_select_assets_orders_by_quality_and_caps_at_max(dna):
    strategy = DescriptorReferenceStrategy(dna)
    assets = [
        make_asset(1, quality=40),
        make_asset(2, quality=95),
        make_asset(3, quality=70),
        make_asset(4, quality=88),
        make_asset(5, quality=None),
    ]

    selected = strategy.select_assets(assets)

    assert len(selected) == MAX_REFERENCES
    assert [a.id for a in selected] == [2, 4, 3]


def test_select_assets_is_deterministic_on_ties(dna):
    strategy = DescriptorReferenceStrategy(dna)
    assets = [make_asset(9, quality=80), make_asset(3, quality=80), make_asset(7, quality=80)]

    assert [a.id for a in strategy.select_assets(assets)] == [3, 7, 9]


# --------------------------------------------------------------------------- #
# estrategia nativa
# --------------------------------------------------------------------------- #


def test_native_raises_when_capability_was_never_probed(tmp_path, photo_factory):
    photo = photo_factory(tmp_path / "ref.jpg", size=(800, 600))
    strategy = NativeReferenceStrategy(ApiCapabilities())

    with pytest.raises(CieError) as excinfo:
        strategy.apply("cena", [make_asset(1, path=photo)], model="grok-imagine-image")

    message = str(excinfo.value)
    assert "Descriptor" in message
    assert "probe_api.py" in message


def test_native_raises_when_probe_is_incoherent(tmp_path, photo_factory):
    photo = photo_factory(tmp_path / "ref.jpg", size=(800, 600))
    # Suporte "sim" sem nome de campo: o modulo se recusa a adivinhar a chave.
    strategy = NativeReferenceStrategy(probed_caps(reference_field=None))

    with pytest.raises(CieError) as excinfo:
        strategy.apply("cena", [make_asset(1, path=photo)], model="grok-imagine-image")

    assert "reference_field" in str(excinfo.value)


def test_native_builds_data_uri_in_the_probed_field(tmp_path, photo_factory):
    photo = photo_factory(tmp_path / "ref.jpg", size=(900, 600))
    strategy = NativeReferenceStrategy(
        probed_caps(reference_field="reference_images", reference_encoding="data_uri")
    )

    payload = strategy.apply(
        "tambor de torra em aco inox",
        [make_asset(1, path=photo)],
        model="grok-imagine-image",
        n=2,
        aspect_ratio="4:5",
    )

    assert payload.strategy == "native"
    assert "image" not in payload.extra
    values = payload.extra["reference_images"]
    assert isinstance(values, list) and len(values) == 1
    assert values[0].startswith("data:image/jpeg;base64,")
    assert decode_reference(values[0]).size == (900, 600)
    assert payload.reference_asset_ids == [1]


def test_native_builds_plain_base64_when_encoding_is_b64(tmp_path, photo_factory):
    first = photo_factory(tmp_path / "a.jpg", size=(800, 600), seed=1)
    second = photo_factory(tmp_path / "b.jpg", size=(800, 600), seed=2)
    strategy = NativeReferenceStrategy(probed_caps(reference_field="images", max_reference_images=2))

    payload = strategy.apply(
        FakeComposedPrompt(text="terreiro de secagem ao amanhecer"),
        [make_asset(1, path=first, quality=70), make_asset(2, path=second, quality=90)],
        model="grok-imagine-image",
    )

    values = payload.extra["images"]
    assert len(values) == 2
    assert not any(v.startswith("data:") for v in values)
    assert decode_reference(values[0]).format == "JPEG"
    # A de maior quality_score vem primeiro, aqui e no rastro de proveniencia.
    assert payload.reference_asset_ids == [2, 1]
    assert payload.prompt == "terreiro de secagem ao amanhecer"


def test_native_respects_max_reference_images_of_one(tmp_path, photo_factory):
    photos = [
        photo_factory(tmp_path / f"{i}.jpg", size=(640, 480), seed=i) for i in range(1, 4)
    ]
    strategy = NativeReferenceStrategy(probed_caps(max_reference_images=1))

    payload = strategy.apply(
        "cena",
        [make_asset(i + 1, path=p, quality=50 + i * 10) for i, p in enumerate(photos)],
        model="grok-imagine-image",
    )

    # Teto de uma imagem: a chave carrega a string, nao uma lista de uma posicao.
    assert isinstance(payload.extra["image"], str)
    assert payload.reference_asset_ids == [3]
    assert any("reduzida" in note for note in payload.notes)


def test_native_downscales_oversized_reference(tmp_path, photo_factory):
    photo = photo_factory(tmp_path / "grande.jpg", size=(4000, 3000))
    strategy = NativeReferenceStrategy(probed_caps(max_reference_images=1))

    payload = strategy.apply("cena", [make_asset(1, path=photo)], model="grok-imagine-image")

    decoded = decode_reference(payload.extra["image"])
    assert max(decoded.size) == MAX_REFERENCE_EDGE
    assert decoded.size == (MAX_REFERENCE_EDGE, 1152)
    assert any("reduzido de 4000x3000" in note for note in payload.notes)


def test_native_without_usable_asset_sends_no_image(tmp_path, photo_factory):
    photo = photo_factory(tmp_path / "ref.jpg", size=(800, 600))
    strategy = NativeReferenceStrategy(probed_caps())

    payload = strategy.apply(
        "cena",
        [make_asset(1, path=photo, person=True, consent=False)],
        model="grok-imagine-image",
    )

    assert payload.extra == {}
    assert payload.reference_asset_ids == []
    assert any("descartado" in note for note in payload.notes)


def test_native_fails_loudly_when_the_file_vanished(tmp_path):
    strategy = NativeReferenceStrategy(probed_caps())
    ghost = make_asset(1, path=tmp_path / "sumiu.jpg")

    with pytest.raises(CieError) as excinfo:
        strategy.apply("cena", [ghost], model="grok-imagine-image")

    assert "sumiu.jpg" in str(excinfo.value)


# --------------------------------------------------------------------------- #
# estrategia descritiva
# --------------------------------------------------------------------------- #


def test_descriptor_injects_fragment_once_and_never_sends_image(dna):
    strategy = DescriptorReferenceStrategy(dna)

    payload = strategy.apply(
        "macro de grao torrado sobre madeira rustica",
        [make_asset(1)],
        model="grok-imagine-image",
        n=3,
        aspect_ratio="9:16",
    )

    assert payload.strategy == "descriptor"
    assert payload.extra == {}
    assert payload.prompt.count(FRAGMENT) == 1
    assert payload.prompt.startswith("macro de grao torrado")
    assert payload.n == 3 and payload.aspect_ratio == "9:16"
    assert payload.reference_asset_ids == [1]


def test_descriptor_does_not_duplicate_fragment_already_composed(dna):
    composed = FakeComposedPrompt(
        text=f"macro de grao torrado.\n\n{FRAGMENT}\n\nnegative: warped text"
    )
    strategy = DescriptorReferenceStrategy(dna)

    payload = strategy.apply(composed, [], model="grok-imagine-image")

    assert payload.prompt.count(FRAGMENT) == 1
    assert payload.prompt == composed.text
    assert any("nao duplicado" in note for note in payload.notes)


def test_descriptor_detects_fragment_even_reflowed(dna):
    # Mesmo conteudo, quebras de linha e acentuacao diferentes: ainda e o mesmo DNA.
    reflowed = FRAGMENT.replace("; ", ";\n  ").replace("ambar", "âmbar")
    strategy = DescriptorReferenceStrategy(dna)

    payload = strategy.apply(f"cena base\n\n{reflowed}", [], model="grok-imagine-image")

    assert payload.prompt.count(reflowed) == 1
    assert FRAGMENT not in payload.prompt
    assert any("ja presente" in note for note in payload.notes)


def test_descriptor_keeps_provenance_from_the_dna_sources(dna):
    strategy = DescriptorReferenceStrategy(dna)

    payload = strategy.apply("cena", [], model="grok-imagine-image")

    # Nenhum asset explicito: o rastro aponta para quem originou o DNA.
    assert payload.reference_asset_ids == [11, 12, 13]


def test_descriptor_drops_unusable_asset_from_provenance(dna):
    strategy = DescriptorReferenceStrategy(dna)

    payload = strategy.apply(
        "cena",
        [make_asset(1), make_asset(2, person=True, consent=False)],
        model="grok-imagine-image",
    )

    assert payload.reference_asset_ids == [1]
    assert any("descartado" in note for note in payload.notes)


def test_descriptor_without_dna_leaves_the_prompt_untouched():
    strategy = DescriptorReferenceStrategy()

    payload = strategy.apply("cena crua", [make_asset(1)], model="grok-imagine-image")

    assert payload.prompt == "cena crua"
    assert payload.extra == {}
    assert any("sem Style DNA" in note for note in payload.notes)


# --------------------------------------------------------------------------- #
# escolha da estrategia e conversao para o request
# --------------------------------------------------------------------------- #


def test_choose_strategy_defaults_to_descriptor(dna):
    strategy = choose_strategy(ApiCapabilities(), dna)

    assert isinstance(strategy, DescriptorReferenceStrategy)
    assert strategy.name == "descriptor"
    assert strategy.style_dna is dna


def test_choose_strategy_defaults_to_descriptor_without_capabilities():
    assert isinstance(choose_strategy(None), DescriptorReferenceStrategy)


def test_choose_strategy_returns_native_when_probed(dna):
    strategy = choose_strategy(probed_caps(), dna)

    assert isinstance(strategy, NativeReferenceStrategy)
    assert strategy.name == "native"
    assert strategy.max_references == MAX_REFERENCES


def test_choose_strategy_probed_without_native_support_stays_descriptive(dna):
    caps = ApiCapabilities(probed_at="2026-08-16T12:00:00+00:00")

    assert isinstance(choose_strategy(caps, dna), DescriptorReferenceStrategy)


def test_payload_converts_to_image_request_without_sharing_extra():
    payload = RequestPayload(
        prompt="cena",
        model="grok-imagine-image",
        n=2,
        aspect_ratio="1:1",
        extra={"image": "AAA"},
        strategy="native",
    )

    request = payload.to_image_request()
    body = request.to_payload()

    assert body["model"] == "grok-imagine-image"
    assert body["n"] == 2
    assert body["aspect_ratio"] == "1:1"
    assert body["image"] == "AAA"
    request.extra["image"] = "mexido"
    assert payload.extra["image"] == "AAA"


def test_prompt_text_accepts_str_and_composed_prompt():
    assert prompt_text("cru") == "cru"
    assert prompt_text(FakeComposedPrompt(text="composto")) == "composto"
