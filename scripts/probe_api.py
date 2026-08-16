#!/usr/bin/env python3
"""Sondagem empirica da API da xAI - a unica fonte de verdade sobre o que ela aceita.

O ambiente de desenvolvimento do CIE nao tem egress para api.x.ai, entao nada
do que este script descobre pode ser adivinhado no codigo. Rode isto numa
maquina com rede e XAI_API_KEY; o resultado vira `.cie/capabilities.json`, que
e o que liga (ou mantem desligada) a estrategia de referencia nativa.

    python scripts/probe_api.py --dry-run     # so imprime o plano, nao gasta nada
    python scripts/probe_api.py --yes         # roda de verdade

CUSTO APROXIMADO: cada geracao de imagem bem-sucedida custa entre US$ 0.02 e
US$ 0.08. O plano completo dispara ate ~19 pedidos de imagem, mas a maioria
das tentativas de campo de referencia deve falhar com 4xx (tentativa recusada
normalmente nao e cobrada). Na pratica o gasto fica entre US$ 0.05 e US$ 0.40;
o teto pessimista (tudo cobrado, modelo mais caro) e impresso antes de comecar
e exige confirmacao interativa, a menos que venha --yes.

A CHAVE NUNCA E IMPRESSA NEM GRAVADA: todo corpo de erro passa por
`cie.config.redact` antes de entrar no relatorio.
"""

from __future__ import annotations

import argparse
import asyncio
import io
import json
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import httpx  # noqa: E402
import yaml  # noqa: E402
from PIL import Image  # noqa: E402

from cie import capabilities as caps_mod  # noqa: E402
from cie import pricing  # noqa: E402
from cie.config import Settings, get_api_key, redact, require_api_key  # noqa: E402
from cie.utils import iso, utcnow  # noqa: E402
from cie.xai import (  # noqa: E402
    CHAT_ENDPOINT,
    IMAGE_EDITS_ENDPOINT,
    IMAGES_ENDPOINT,
    MODELS_ENDPOINT,
    XaiClient,
    data_uri,
    to_b64,
)

#: Campos candidatos para imagem de referencia. Nenhum deles esta confirmado -
#: e exatamente isso que a sondagem existe para descobrir.
REFERENCE_FIELDS = ("image", "images", "reference_images", "input_image", "image_url")
#: Como a imagem pode estar codificada no campo.
ENCODINGS = ("b64", "data_uri")
#: Campos que, se existirem, provavelmente esperam lista.
LIST_FIELDS = {"images", "reference_images"}
#: Parametros opcionais testados um a um, cada um num pedido minimo.
OPTIONAL_PARAMS: tuple[tuple[str, Any], ...] = (
    ("aspect_ratio", "1:1"),
    ("size", "1024x1024"),
    ("quality", "low"),
    ("seed", 7),
    ("n", 2),
)
#: Endpoints de catalogo que talvez existam alem de /models.
EXTRA_MODEL_ENDPOINTS = ("/image-generation-models", "/language-models")
#: Tokens que sugerem modelo de imagem / modelo com visao no nome.
IMAGE_TOKENS = ("image", "imagine")
VISION_TOKENS = ("vision", "grok-4", "grok-3", "grok-2v")

PROMPT = "a rustic wooden table with roasted coffee beans, warm side light, shallow depth of field"
MAX_VISION_CANDIDATES = 3
SNIPPET = 400


# --------------------------------------------------------------------------- #
# impressao
# --------------------------------------------------------------------------- #


def section(title: str) -> None:
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def line(text: str = "") -> None:
    print(text)


def verdict(ok: bool) -> str:
    return "OK   " if ok else "FALHA"


# --------------------------------------------------------------------------- #
# estado da sondagem
# --------------------------------------------------------------------------- #


class Probe:
    """Acumula tentativas e conclusoes. Toda evidencia crua fica em `attempts`."""

    def __init__(self, client: XaiClient, model: str) -> None:
        self.client = client
        self.model = model
        self.attempts: list[dict[str, Any]] = []
        self.image_calls = 0

    async def call(
        self,
        endpoint: str,
        field: str,
        *,
        method: str = "POST",
        json_body: Any = None,
        data: dict[str, Any] | None = None,
        files: Any = None,
        counts_as_image: bool = False,
        note: str = "",
    ) -> tuple[int | None, dict[str, Any] | None, str]:
        """Uma tentativa: devolve (status, json, texto redigido) e registra tudo.

        Nunca levanta - a sondagem precisa do corpo de erro exato, e um 4xx aqui
        e resultado valido, nao acidente.
        """
        started = time.perf_counter()
        status: int | None = None
        payload: dict[str, Any] | None = None
        text = ""
        try:
            response = await self.client.raw_request(
                method, endpoint, json_body=json_body, data=data, files=files
            )
            status = response.status_code
            text = redact(response.text)[:SNIPPET]
            try:
                parsed = response.json()
                payload = parsed if isinstance(parsed, dict) else {"_root": parsed}
            except ValueError:
                payload = None
        except httpx.HTTPError as exc:
            text = f"{type(exc).__name__}: {redact(str(exc))}"[:SNIPPET]

        elapsed_ms = int((time.perf_counter() - started) * 1000)
        ok = status is not None and status < 400
        if ok and counts_as_image:
            self.image_calls += 1
        self.attempts.append(
            {
                "endpoint": endpoint,
                "field": field,
                "status": status,
                "ok": ok,
                "latency_ms": elapsed_ms,
                "error": "" if ok else text,
                "note": note,
            }
        )
        print(f"  [{verdict(ok)}] {endpoint:<24} {field:<28} status={status} {elapsed_ms}ms")
        if not ok and text:
            print(f"          corpo: {text[:220]}")
        return status, payload, text


def image_body(model: str, **extra: Any) -> dict[str, Any]:
    """Pedido minimo de imagem; `extra` traz o campo em teste."""
    body: dict[str, Any] = {
        "model": model,
        "prompt": PROMPT,
        "n": 1,
        "response_format": "b64_json",
    }
    body.update(extra)
    return body


def tiny_png(size: tuple[int, int] = (64, 64)) -> bytes:
    """Imagem sintetica em memoria. A base real de fotos nunca sai do disco."""
    buffer = io.BytesIO()
    image = Image.new("RGB", size, (107, 68, 35))
    for x in range(0, size[0], 8):
        for y in range(0, size[1], 8):
            image.putpixel((x, y), (240, 220, 180))
    image.save(buffer, format="PNG")
    return buffer.getvalue()


# --------------------------------------------------------------------------- #
# etapas
# --------------------------------------------------------------------------- #


async def step_models(probe: Probe) -> list[str]:
    section("1. GET /models - o que existe hoje")
    status, payload, _ = await probe.call(MODELS_ENDPOINT, "-", method="GET")
    names: list[str] = []
    if status == 200 and payload:
        items = payload.get("data") or payload.get("models") or []
        for item in items if isinstance(items, list) else []:
            name = item.get("id") or item.get("name") if isinstance(item, dict) else item
            if name and str(name) not in names:
                names.append(str(name))
    for endpoint in EXTRA_MODEL_ENDPOINTS:
        # Palpite sendo testado, nao suposicao: se existir, entra no relatorio.
        extra_status, extra_payload, _ = await probe.call(
            endpoint, "-", method="GET", note="endpoint de catalogo hipotetico"
        )
        if extra_status == 200 and extra_payload:
            items = extra_payload.get("models") or extra_payload.get("data") or []
            for item in items if isinstance(items, list) else []:
                name = item.get("id") or item.get("name") if isinstance(item, dict) else item
                if name and str(name) not in names:
                    names.append(str(name))

    line(f"\n  modelos vistos: {', '.join(names) if names else '(nenhum)'}")
    return names


async def step_text_only(probe: Probe) -> tuple[bool, list[str]]:
    section("2. POST /images/generations so com texto - o caminho feliz")
    status, payload, _ = await probe.call(
        IMAGES_ENDPOINT, "prompt", json_body=image_body(probe.model), counts_as_image=True
    )
    formats: list[str] = []
    if status == 200 and payload:
        items = payload.get("data") or []
        first = items[0] if isinstance(items, list) and items else {}
        if isinstance(first, dict):
            if first.get("b64_json"):
                formats.append("b64_json")
            if first.get("url"):
                formats.append("url")
            line(f"  campos do item: {sorted(str(k) for k in first)}")
        line(f"  chaves da resposta: {sorted(str(k) for k in payload)}")
    return status == 200, formats or ["b64_json"]


async def step_reference_fields(
    probe: Probe, image_bytes: bytes
) -> tuple[str | None, str | None, int]:
    section("3. Campos candidatos de imagem de referencia em /images/generations")
    line("  Cada combinacao campo x codificacao vira um pedido isolado.")
    b64 = to_b64(image_bytes)
    uri = data_uri(image_bytes)
    found_field: str | None = None
    found_encoding: str | None = None

    for field_name in REFERENCE_FIELDS:
        for encoding in ENCODINGS:
            value: Any = b64 if encoding == "b64" else uri
            if field_name in LIST_FIELDS:
                value = [value]
            status, _, _ = await probe.call(
                IMAGES_ENDPOINT,
                f"{field_name} ({encoding})",
                json_body=image_body(probe.model, **{field_name: value}),
                counts_as_image=True,
            )
            if status == 200 and found_field is None:
                found_field, found_encoding = field_name, encoding

    max_references = 0
    if found_field:
        max_references = 1
        line(f"\n  campo aceito: {found_field} ({found_encoding}). Testando 2 referencias...")
        if found_field in LIST_FIELDS:
            value = b64 if found_encoding == "b64" else uri
            status, _, _ = await probe.call(
                IMAGES_ENDPOINT,
                f"{found_field} x2",
                json_body=image_body(probe.model, **{found_field: [value, value]}),
                counts_as_image=True,
            )
            if status == 200:
                max_references = 2
    else:
        line("\n  nenhum campo de referencia aceito: a estrategia descritiva continua")
    return found_field, found_encoding, max_references


async def step_edits(probe: Probe, image_bytes: bytes) -> str | None:
    section("4. POST /images/edits - o endpoint pode simplesmente nao existir")
    status_json, _, _ = await probe.call(
        IMAGE_EDITS_ENDPOINT,
        "json/image",
        json_body={
            "model": probe.model,
            "prompt": PROMPT,
            "image": to_b64(image_bytes),
            "response_format": "b64_json",
        },
        counts_as_image=True,
    )
    if status_json == 200:
        return "json"

    status_multipart, _, _ = await probe.call(
        IMAGE_EDITS_ENDPOINT,
        "multipart/form-data",
        data={"model": probe.model, "prompt": PROMPT, "response_format": "b64_json"},
        files={"image": ("reference.png", image_bytes, "image/png")},
        counts_as_image=True,
    )
    return "multipart" if status_multipart == 200 else None


async def step_optional_params(probe: Probe) -> dict[str, bool]:
    section("5. Parametros opcionais, um por pedido")
    accepted: dict[str, bool] = {}
    for name, value in OPTIONAL_PARAMS:
        status, _, _ = await probe.call(
            IMAGES_ENDPOINT,
            f"{name}={value}",
            json_body=image_body(probe.model, **{name: value}),
            counts_as_image=True,
        )
        accepted[name] = status == 200
    return accepted


async def step_vision(probe: Probe, models: list[str], image_bytes: bytes) -> str | None:
    section("6. Modelo com visao para o Style DNA")
    candidates = [
        name
        for name in models
        if any(token in name.lower() for token in VISION_TOKENS)
        and not any(token in name.lower() for token in IMAGE_TOKENS)
    ][:MAX_VISION_CANDIDATES]
    if not candidates:
        line("  nenhum candidato obvio na lista de /models")
        return None

    line(f"  candidatos: {', '.join(candidates)}")
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image in one short sentence."},
                {"type": "image_url", "image_url": {"url": data_uri(image_bytes)}},
            ],
        }
    ]
    for name in candidates:
        status, _, _ = await probe.call(
            CHAT_ENDPOINT,
            f"visao: {name}",
            json_body={"model": name, "messages": messages, "temperature": 0.0, "max_tokens": 64},
            note="chat com imagem em data URI",
        )
        if status == 200:
            return name
    return None


# --------------------------------------------------------------------------- #
# saida
# --------------------------------------------------------------------------- #


def write_models_yaml(path: Path, models: list[str], max_n: int, aspect_ratio_ok: bool) -> None:
    """Grava .cie/models.yaml no formato que `pricing.load_overrides` le.

    A sondagem confirma EXISTENCIA e PARAMETROS, nunca preco: a API nao expoe
    tabela de precos. Por isso `verified` fica false e os precos continuam
    vindo do catalogo semente - inventar preco aqui seria pior que nao ter.
    A lista de aspect_ratios tambem continua a do catalogo: a sondagem so testa
    uma proporcao (barato), entao ela prova que o PARAMETRO existe, nao quais
    valores sao aceitos. Zerar a lista quebraria o 9:16 dos Reels sem prova.
    """
    stamp = iso(utcnow())
    probed_ratio = OPTIONAL_PARAMS[0][1]
    entries: dict[str, dict[str, Any]] = {}
    for name in models:
        base = pricing.get_model(name)
        entries[name] = {
            "prices_usd": dict(base.prices_usd),
            "max_n": max_n,
            "aspect_ratios": list(base.aspect_ratios),
            "verified": False,
            "source": f"sondagem {stamp}: existencia e max_n confirmados, precos NAO",
            "notes": (
                f"max_n confirmado pela sondagem; parametro aspect_ratio "
                f"{'aceito' if aspect_ratio_ok else 'RECUSADO'} no teste com "
                f"'{probed_ratio}' (demais proporcoes nao foram testadas); "
                f"prices_usd continua sendo a estimativa da spec do projeto"
            ),
        }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump({"models": entries}, allow_unicode=True, sort_keys=True), encoding="utf-8"
    )


def write_raw_report(settings: Settings, attempts: list[dict[str, Any]]) -> Path:
    settings.probe_dir.mkdir(parents=True, exist_ok=True)
    path = settings.probe_dir / "attempts.json"
    path.write_text(json.dumps(attempts, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


# --------------------------------------------------------------------------- #
# orquestracao
# --------------------------------------------------------------------------- #


def plan_lines(args: argparse.Namespace) -> list[str]:
    steps = [
        f"1. GET {MODELS_ENDPOINT} (+ {', '.join(EXTRA_MODEL_ENDPOINTS)})",
        f"2. POST {IMAGES_ENDPOINT} so com texto (1 imagem)",
        f"3. POST {IMAGES_ENDPOINT} com {len(REFERENCE_FIELDS)} campos x "
        f"{len(ENCODINGS)} codificacoes ({len(REFERENCE_FIELDS) * len(ENCODINGS)} pedidos)",
    ]
    if args.skip_edits:
        steps.append(f"4. POST {IMAGE_EDITS_ENDPOINT} - PULADO (--skip-edits)")
    else:
        steps.append(f"4. POST {IMAGE_EDITS_ENDPOINT} em JSON e multipart (2 pedidos)")
    steps.append(
        "5. parametros opcionais isolados: " + ", ".join(name for name, _ in OPTIONAL_PARAMS)
    )
    steps.append(f"6. POST {CHAT_ENDPOINT} com imagem, ate {MAX_VISION_CANDIDATES} candidatos")
    return steps


def worst_case_cost(args: argparse.Namespace) -> float:
    image_calls = 1 + len(REFERENCE_FIELDS) * len(ENCODINGS) + 1
    if not args.skip_edits:
        image_calls += 2
    # n=2 gera duas imagens; os demais parametros geram uma cada.
    image_calls += len(OPTIONAL_PARAMS) + 1
    return pricing.estimate_cost(args.model, image_calls, resolution="2k")


async def run_probe(args: argparse.Namespace, settings: Settings) -> int:
    image_bytes = tiny_png()
    caps = caps_mod.ApiCapabilities()

    async with XaiClient(base_url=args.base_url, timeout=args.timeout, max_retries=2) as client:
        probe = Probe(client, args.model)

        models = await step_models(probe)
        if models and args.model not in models:
            image_models = [m for m in models if any(t in m.lower() for t in IMAGE_TOKENS)]
            if image_models:
                line(
                    f"\n  ATENCAO: '{args.model}' nao esta em /models; "
                    f"usando '{image_models[0]}' nas etapas de imagem"
                )
                probe.model = image_models[0]

        happy, formats = await step_text_only(probe)
        if not happy:
            line("\n  o caminho feliz falhou: as etapas seguintes ainda rodam, mas o")
            line("  resultado provavelmente reflete modelo/credencial, nao capacidade")

        field, encoding, max_references = await step_reference_fields(probe, image_bytes)

        edits_mode: str | None = None
        if args.skip_edits:
            section("4. POST /images/edits - pulado (--skip-edits)")
        else:
            edits_mode = await step_edits(probe, image_bytes)

        params = await step_optional_params(probe)
        vision = await step_vision(probe, models, image_bytes)

        caps = caps_mod.ApiCapabilities(
            probed_at=iso(utcnow()),
            native_reference_supported=field is not None,
            reference_field=field,
            reference_endpoint=IMAGES_ENDPOINT if field else (IMAGE_EDITS_ENDPOINT if edits_mode else None),
            max_reference_images=max_references,
            reference_encoding=encoding,
            supports_seed=params.get("seed", False),
            supports_aspect_ratio=params.get("aspect_ratio", False),
            supports_size=params.get("size", False),
            supports_quality=params.get("quality", False),
            max_n=2 if params.get("n", False) else 1,
            response_formats=formats,
            image_models=[m for m in models if any(t in m.lower() for t in IMAGE_TOKENS)],
            vision_model=vision,
            attempts=probe.attempts,
        )

    caps_path = caps_mod.save(settings, caps)
    yaml_path = settings.home / "models.yaml"
    write_models_yaml(yaml_path, caps.image_models or [probe.model], caps.max_n, caps.supports_aspect_ratio)
    raw_path = write_raw_report(settings, caps.attempts)

    section("RESUMO")
    line(f"  {caps.summary()}")
    line(f"  seed          {'sim' if caps.supports_seed else 'nao'}")
    line(f"  aspect_ratio  {'sim' if caps.supports_aspect_ratio else 'nao'}")
    line(f"  size          {'sim' if caps.supports_size else 'nao'}")
    line(f"  quality       {'sim' if caps.supports_quality else 'nao'}")
    line(f"  n maximo      {caps.max_n}")
    line(f"  edits         {edits_mode or 'nao existe / nao aceitou'}")
    line(f"  visao         {caps.vision_model or '-'}")
    line(f"  imagens geradas com sucesso: {probe.image_calls}")
    line("")
    line(f"  {caps_path}")
    line(f"  {yaml_path}")
    line(f"  {raw_path}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sondagem empirica da API da xAI (gasta credito real).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--dry-run", action="store_true", help="imprime o plano e sai")
    parser.add_argument("--yes", action="store_true", help="nao pede confirmacao")
    parser.add_argument("--out", default=".cie", help="diretorio de saida (default: .cie)")
    parser.add_argument("--model", default=pricing.DEFAULT_MODEL, help="modelo de imagem a testar")
    parser.add_argument("--skip-edits", action="store_true", help="nao testa /images/edits")
    parser.add_argument("--base-url", default=None, help="sobrescreve a base da API")
    parser.add_argument("--timeout", type=float, default=120.0, help="timeout por pedido")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    out = Path(args.out).resolve()
    settings = Settings(root=Path.cwd().resolve(), home=out)

    section("PLANO DA SONDAGEM")
    for step in plan_lines(args):
        line(f"  {step}")
    line("")
    line(f"  modelo         {args.model}")
    line(f"  saida          {out}")
    # A chave e so verificada, nunca ecoada.
    line(f"  XAI_API_KEY    {'presente' if get_api_key() else 'AUSENTE'}")
    line(f"  custo maximo   US$ {worst_case_cost(args):.2f} (teto pessimista: tudo cobrado)")

    if args.dry_run:
        line("\n  --dry-run: nenhuma chamada foi feita.")
        return 0

    try:
        require_api_key()
    except RuntimeError as exc:
        line(f"\n  {exc}")
        return 2

    if not args.yes:
        answer = input("\n  Isto gasta credito real. Continuar? [s/N] ").strip().lower()
        if answer not in {"s", "sim", "y", "yes"}:
            line("  cancelado.")
            return 1

    return asyncio.run(run_probe(args, settings))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
