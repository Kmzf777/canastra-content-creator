"""Extracao de Style DNA: fotos reais aprovadas viram consistencia textual.

O Style DNA e a ponte entre a base real e a geracao. Um modelo com visao olha um
conjunto pequeno de fotos DA OPERACAO e devolve a assinatura visual que elas de
fato compartilham - paleta, luz, lente, textura, enquadramento, materiais, clima
e o que destoaria. `cie.prompt.build_prompt_fragment` transforma esse descritor
numa frase que entra em todo prompt, e e assim que a saida sintetica herda o
estilo do real sem que ninguem precise reescrever prompt a mao.

Tres decisoes que este modulo carrega:

  1. O CONJUNTO E PEQUENO E CURADO. De 8 a 15 fotos, so as reference-grade e so
     as que passam no teste de consentimento (`Asset.is_usable_as_reference`).
     Menos que 8 descreve a foto, nao o estilo; mais que 15 dilui a assinatura e
     multiplica o custo do chat com visao sem ganho.
  2. O NOME DO MODELO COM VISAO NAO E CHUTADO. Ele vem de `CIE_VISION_MODEL` ou
     de `capabilities.vision_model` (gravado por `scripts/probe_api.py`). Sem um
     dos dois, o modulo falha explicando como descobrir - jamais adivinha.
  3. O PARSER E TOLERANTE, O SCHEMA NAO. Modelo de linguagem cerca JSON em
     markdown e comenta antes e depois; nada disso e erro. Chave desconhecida e
     ignorada (com log). Ja o schema final e `StyleDescriptor`, que e
     `extra="forbid"` - o que entra no banco tem forma unica.

Roda uma vez por conjunto, offline em relacao a fila de geracao: nenhuma imagem
e produzida aqui.
"""

from __future__ import annotations

import io
import json
import logging
import os
import re
import sqlite3
from typing import Any, Iterable, Mapping, Protocol, Sequence

from PIL import Image
from pydantic import ValidationError

from . import repository
from .capabilities import CAPABILITIES_FILENAME, ApiCapabilities
from .capabilities import load as load_capabilities
from .config import Settings, get_settings, redact
from .enums import Pillar
from .errors import CieError, XaiApiError
from .imaging import load_image
from .models import Asset, StyleDescriptor, StyleDna
from .prompt import build_prompt_fragment
from .utils import dumps, utcnow
from .xai import data_uri

#: Piso e teto do conjunto de fotos por perfil, e o default da CLI.
MIN_ASSETS = 8
MAX_ASSETS = 15
DEFAULT_LIMIT = 12

#: Override local do modelo com visao (ambiente ou `.env`).
VISION_MODEL_ENV = "CIE_VISION_MODEL"

#: Lado maior de cada foto enviada. 1024 px preserva textura de grao e trama de
#: tecido - que e o que o descritor precisa ver - sem inflar o payload.
MAX_IMAGE_SIDE = 1024
JPEG_QUALITY = 85

#: Quanto da resposta crua sobrevive numa mensagem de erro.
RAW_SNIPPET_CHARS = 600

_LOG = logging.getLogger(__name__)

#: Cerca de markdown com ou sem rotulo de linguagem.
_FENCE_RE = re.compile(r"```[a-zA-Z0-9_+-]*\s*(.*?)```", re.DOTALL)

#: Separadores aceitos quando o modelo devolve uma lista como texto corrido.
_LIST_SPLIT_RE = re.compile(r"[,;\n]")

#: Campos de `StyleDescriptor` que sao lista; o resto e texto.
_LIST_FIELDS: frozenset[str] = frozenset({"palette", "recurring_materials", "avoid"})


DNA_SYSTEM_PROMPT = """You are a photography director cataloguing the visual signature of a real brand archive.

You will receive a small set of photographs taken by a single operation: a Brazilian specialty coffee farm and its roastery. Your job is to describe the signature THESE photographs actually share, so that new images can be matched against it.

Method:
- Read the frames as a set. Report only what repeats across most of them; a trait that shows up in a single frame is noise, not signature.
- Describe what is really in front of you, including the imperfect parts: uneven light, worn surfaces, dust, working hands, cluttered benches, cables, stains. A polished generic "premium coffee" description is a failure of this task even when it reads well.
- Name concrete, observable things - the actual colours, the actual materials, the actual working distance - never aspirations, marketing adjectives or brand values.
- Infer the optics from visual evidence only: perspective compression, depth of field, falloff and distortion toward the edges.
- "avoid" is the negative side of the same signature: what would look immediately foreign if placed next to these photographs.

Write the values in English, short and dense, so they can be concatenated into an English image prompt; keep proper nouns and Brazilian material names as they are. Each list holds 3 to 6 items.

Answer with ONE JSON object and nothing else: no markdown fences, no comments, no text before or after it. Use exactly these keys:

{
  "palette": ["colour name or hex", "..."],
  "light_quality": "one sentence",
  "lens": "one sentence",
  "texture": "one sentence",
  "framing": "one sentence",
  "recurring_materials": ["material", "..."],
  "mood": "one sentence",
  "avoid": ["trait that would break the set", "..."]
}"""


class VisionClient(Protocol):
    """O minimo que `extract_style_dna` exige - `XaiClient` satisfaz, fakes tambem."""

    async def chat_completion(
        self, model: str, messages: Sequence[Mapping[str, Any]], **kwargs: Any
    ) -> dict[str, Any]: ...


# --------------------------------------------------------------------------- #
# modelo com visao
# --------------------------------------------------------------------------- #


def resolve_vision_model(
    capabilities: ApiCapabilities | None = None, settings: Settings | None = None
) -> str:
    """Nome do modelo com visao: ambiente, depois sondagem, depois erro.

    Nao existe fallback e isso e proposital. Este repositorio nao alcanca
    docs.x.ai nem api.x.ai, entao qualquer nome escrito aqui seria chute - e um
    chute custa uma chamada com 12 imagens anexadas antes de dar 404.
    """
    # `get_settings` carrega o `.env`, entao CIE_VISION_MODEL tambem vale de la.
    resolved_settings = settings or get_settings()

    override = os.environ.get(VISION_MODEL_ENV, "").strip()
    if override:
        return override

    caps = capabilities if capabilities is not None else load_capabilities(resolved_settings)
    if caps.vision_model and caps.vision_model.strip():
        return caps.vision_model.strip()

    raise CieError(
        "nenhum modelo com visao configurado, e o CIE nao chuta nome de modelo.\n"
        "  como resolver:\n"
        "  - rode `python scripts/probe_api.py` numa maquina com XAI_API_KEY e "
        "acesso a api.x.ai; ele descobre o modelo e grava `vision_model` em "
        f"{CAPABILITIES_FILENAME} ao lado do banco; ou\n"
        f"  - defina {VISION_MODEL_ENV}=<nome-do-modelo> no ambiente ou no .env."
    )


# --------------------------------------------------------------------------- #
# selecao do conjunto
# --------------------------------------------------------------------------- #


def select_assets_for_dna(
    conn: sqlite3.Connection,
    pillar: Pillar | str | None = None,
    limit: int = DEFAULT_LIMIT,
    asset_ids: Iterable[int] | None = None,
) -> list[Asset]:
    """Escolhe as fotos que vao descrever o estilo, das melhores para as piores.

    Filtra por `is_reference_grade` no banco e ainda por
    `Asset.is_usable_as_reference` em memoria - a segunda barreira e o
    consentimento: foto com pessoa identificavel sem consentimento registrado nao
    e enviada para lugar nenhum, nem para ser apenas descrita.

    `limit` acima de `MAX_ASSETS` e reduzido em silencio; acima disso o conjunto
    deixa de ter assinatura comum e a chamada so fica cara.
    """
    ids = list(asset_ids) if asset_ids is not None else None
    candidates = repository.list_assets(conn, pillar=pillar, ids=ids, reference_grade=True)
    usable = [asset for asset in candidates if asset.is_usable_as_reference]
    blocked_by_consent = len(candidates) - len(usable)

    # Melhor qualidade primeiro; `id` desempata para a selecao ser reproduzivel.
    usable.sort(key=lambda asset: (-(asset.quality_score or 0), asset.id or 0))

    requested = int(limit or DEFAULT_LIMIT)
    effective_limit = min(requested, MAX_ASSETS)
    selected = usable[:effective_limit]

    if len(selected) < MIN_ASSETS:
        raise CieError(
            _shortage_message(
                selected=len(selected),
                usable=len(usable),
                requested=requested,
                effective_limit=effective_limit,
                blocked_by_consent=blocked_by_consent,
                pillar=pillar,
                ids=ids,
            )
        )
    return selected


def _shortage_message(
    *,
    selected: int,
    usable: int,
    requested: int,
    effective_limit: int,
    blocked_by_consent: int,
    pillar: Pillar | str | None,
    ids: list[int] | None,
) -> str:
    scope = []
    if pillar is not None:
        scope.append(f"pilar {pillar}")
    if ids is not None:
        scope.append(f"{len(ids)} id(s) informado(s)")
    scope_text = ", ".join(scope) if scope else "base inteira"

    lines = [
        f"Style DNA precisa de no minimo {MIN_ASSETS} fotos e so {selected} "
        f"entraram na selecao (faltam {MIN_ASSETS - selected}).",
        f"  escopo consultado: {scope_text}; utilizaveis encontradas: {usable}.",
    ]
    if blocked_by_consent:
        lines.append(
            f"  {blocked_by_consent} foto(s) reference-grade ficaram de fora por "
            "terem pessoa identificavel sem consentimento registrado."
        )
    lines.append("  como resolver:")
    if effective_limit < MIN_ASSETS:
        lines.append(
            f"  - o proprio --limit ({requested}) esta abaixo do minimo: suba para "
            f"{MIN_ASSETS} ou mais (o teto util e {MAX_ASSETS});"
        )
    lines.extend(
        [
            "  - cure mais fotos: marque as boas como reference-grade "
            "(`cie assets curate <id> --reference-grade`);",
            "  - registre o consentimento das fotos com pessoa identificavel;",
            "  - ou amplie o escopo, tirando o filtro de pilar / a lista de ids.",
        ]
    )
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# montagem das mensagens
# --------------------------------------------------------------------------- #


def _open_for_vision(asset: Asset) -> Image.Image:
    """Abre o original; cai para o thumbnail quando nao ha decoder (RAW, HEIC)."""
    image = load_image(asset.path)
    if image is None and asset.thumb_path:
        image = load_image(asset.thumb_path)
    if image is None:
        raise CieError(
            f"asset {asset.id} nao pode ser lido para o Style DNA: nenhum decoder "
            f"abriu {asset.path} e nao ha thumbnail utilizavel. Confira se o "
            "arquivo continua no lugar; RAW precisa do extra `heic`/de um JPEG derivado."
        )
    return image


def encode_asset_for_vision(asset: Asset, max_side: int = MAX_IMAGE_SIDE) -> str:
    """Foto real -> data URI JPEG, ja reduzida. Nunca envia o arquivo original."""
    image = _open_for_vision(asset)
    try:
        frame = image.convert("RGB")
    finally:
        image.close()
    frame.thumbnail((max_side, max_side))
    buffer = io.BytesIO()
    frame.save(buffer, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    frame.close()
    return data_uri(buffer.getvalue(), "image/jpeg")


def _asset_line(index: int, asset: Asset) -> str:
    facts = [f"pillar {asset.pillar}" if asset.pillar else "pillar unset"]
    if asset.location:
        facts.append(f"location {asset.location}")
    if asset.sku:
        facts.append(f"sku {asset.sku}")
    if asset.subject_tags:
        facts.append("tags " + ", ".join(asset.subject_tags))
    return f"  {index}. " + "; ".join(facts)


def _user_brief(assets: Sequence[Asset], extra_instructions: str | None = None) -> str:
    """Texto que acompanha as imagens: contexto de catalogo, nunca conclusao.

    Os rotulos do catalogo entram como referencia de origem, com o aviso
    explicito de que o que vale e o que esta na imagem. Sem esse aviso o modelo
    tende a descrever o rotulo ("torrefacao") em vez da foto.
    """
    blocks = [
        f"Here are {len(assets)} photographs from the same real archive, in "
        "catalogue order. The catalogue labels below say where each frame came "
        "from; they are context only - describe what you SEE, never what the "
        "label suggests.",
        "\n".join(_asset_line(index, asset) for index, asset in enumerate(assets, start=1)),
    ]
    if extra_instructions and extra_instructions.strip():
        blocks.append(extra_instructions.strip())
    blocks.append(
        "Return the single JSON object described in the system message, and nothing else."
    )
    return "\n\n".join(blocks)


def build_vision_messages(
    assets: Sequence[Asset], extra_instructions: str | None = None
) -> list[dict[str, Any]]:
    """Mensagens no formato de chat com visao: um bloco de texto + N imagens.

    O formato dos blocos (`image_url` com data URI) e o mesmo que
    `scripts/probe_api.py` usa para sondar o endpoint de chat. Nada alem de
    `url` entra no bloco: `detail`, `resolution` e afins nao foram confirmados
    e campo nao confirmado nao viaja.
    """
    if not assets:
        raise CieError("nenhuma foto para descrever: o Style DNA precisa de um conjunto")

    content: list[dict[str, Any]] = [
        {"type": "text", "text": _user_brief(assets, extra_instructions)}
    ]
    for asset in assets:
        content.append(
            {"type": "image_url", "image_url": {"url": encode_asset_for_vision(asset)}}
        )

    return [
        {"role": "system", "content": DNA_SYSTEM_PROMPT},
        {"role": "user", "content": content},
    ]


# --------------------------------------------------------------------------- #
# leitura da resposta
# --------------------------------------------------------------------------- #


def _snippet(text: str) -> str:
    cleaned = redact(text or "").strip()
    if len(cleaned) <= RAW_SNIPPET_CHARS:
        return cleaned
    return cleaned[:RAW_SNIPPET_CHARS] + "... (truncado)"


def _first_json_object(text: str) -> str | None:
    """Recorta o primeiro objeto `{...}` balanceado, ignorando chaves em strings."""
    depth = 0
    start = -1
    in_string = False
    escaped = False
    for index, char in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            if depth == 0:
                start = index
            depth += 1
        elif char == "}" and depth:
            depth -= 1
            if depth == 0 and start >= 0:
                return text[start : index + 1]
    return None


def _candidates(raw_text: str) -> list[str]:
    """Tentativas de extracao, da mais literal para a mais escavada."""
    text = raw_text.strip()
    found = [match.strip() for match in _FENCE_RE.findall(text)]
    found.append(text)
    carved = _first_json_object(text)
    if carved:
        found.append(carved)
    return [item for item in found if item]


def _coerce(field: str, value: Any) -> Any:
    """Ajusta tipo sem inventar conteudo: lista <-> texto, o resto vira str."""
    if field in _LIST_FIELDS:
        if isinstance(value, str):
            return [part.strip() for part in _LIST_SPLIT_RE.split(value) if part.strip()]
        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]
        return [str(value).strip()]
    if isinstance(value, (list, tuple)):
        return "; ".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def parse_descriptor(raw_text: str) -> StyleDescriptor:
    """Texto do modelo -> `StyleDescriptor`, tolerando cerca e conversa em volta.

    Chave desconhecida e ignorada com log em vez de derrubar a extracao: o
    conjunto de fotos ja foi enviado e pago, jogar fora o resultado por causa de
    um `"notes"` extra seria caro e inutil.
    """
    payload: Mapping[str, Any] | None = None
    for candidate in _candidates(raw_text or ""):
        try:
            parsed = json.loads(candidate)
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(parsed, Mapping):
            payload = parsed
            break

    if payload is None:
        raise CieError(
            "a resposta do modelo com visao nao contem um objeto JSON valido. "
            "O system prompt exige JSON puro; rode de novo ou baixe a temperatura.\n"
            f"  recebido: {_snippet(raw_text) or '<vazio>'}"
        )

    known = set(StyleDescriptor.model_fields)
    unknown = sorted(str(key) for key in payload if str(key) not in known)
    if unknown:
        _LOG.warning(
            "Style DNA: chave(s) fora do schema ignorada(s) na resposta do modelo: %s",
            ", ".join(unknown),
        )

    data = {
        str(key): _coerce(str(key), value)
        for key, value in payload.items()
        if str(key) in known and value is not None
    }
    try:
        return StyleDescriptor(**data)
    except ValidationError as exc:
        # Rede de seguranca: hoje `_coerce` da conta de todo tipo que o JSON
        # pode trazer, mas o dia em que `StyleDescriptor` ganhar uma restricao
        # nova a falha tem que sair legivel, com o que o modelo devolveu.
        raise CieError(
            "a resposta do modelo tem JSON valido mas fora do schema do "
            f"StyleDescriptor: {exc.error_count()} campo(s) invalido(s).\n"
            f"  recebido: {_snippet(dumps(dict(payload)))}"
        ) from exc


def extract_message_text(payload: Mapping[str, Any]) -> str:
    """Puxa o texto da primeira escolha do chat, explicando qualquer formato torto."""
    raw = _snippet(dumps(dict(payload)))
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise XaiApiError(
            "resposta de chat sem 'choices' utilizavel; chaves recebidas: "
            f"{sorted(str(k) for k in payload)}",
            raw=raw,
        )

    first = choices[0]
    message = first.get("message") if isinstance(first, Mapping) else None
    content = message.get("content") if isinstance(message, Mapping) else None

    if isinstance(content, list):
        # Alguns formatos devolvem blocos ({"type": "text", "text": ...}).
        parts = [
            str(block.get("text", "")).strip()
            for block in content
            if isinstance(block, Mapping)
        ]
        content = "\n".join(part for part in parts if part)

    if not isinstance(content, str) or not content.strip():
        raise XaiApiError(
            "a primeira escolha do chat nao traz texto em message.content", raw=raw
        )
    return content


# --------------------------------------------------------------------------- #
# extracao completa
# --------------------------------------------------------------------------- #


async def extract_style_dna(
    client: VisionClient,
    conn: sqlite3.Connection,
    *,
    name: str,
    pillar: Pillar | str | None = None,
    limit: int = DEFAULT_LIMIT,
    asset_ids: Iterable[int] | None = None,
    model: str | None = None,
    settings: Settings | None = None,
) -> StyleDna:
    """Seleciona, descreve, valida e grava o perfil de estilo.

    Grava por `name` (upsert): reextrair um perfil depois de curar mais fotos
    atualiza o mesmo registro, e os jobs antigos continuam apontando para o id
    que ja conheciam.
    """
    profile_name = (name or "").strip()
    if not profile_name:
        raise CieError("o Style DNA precisa de um nome (ex.: laboratorio-uberlandia)")

    assets = select_assets_for_dna(conn, pillar=pillar, limit=limit, asset_ids=asset_ids)
    resolved_model = (model or "").strip() or resolve_vision_model(settings=settings)
    messages = build_vision_messages(assets)

    # Sem `response_format`: modo JSON nativo nao foi confirmado nesta API e um
    # 400 aqui custaria o upload das 12 fotos. O JSON e cobrado pelo system
    # prompt e garantido por `parse_descriptor`, que aceita cerca e conversa.
    payload = await client.chat_completion(resolved_model, messages)
    descriptor = parse_descriptor(extract_message_text(payload))

    dna = StyleDna(
        name=profile_name,
        pillar=Pillar(pillar) if pillar else None,
        source_asset_ids=[asset.id for asset in assets if asset.id is not None],
        descriptor=descriptor,
        prompt_fragment=build_prompt_fragment(descriptor),
        created_at=utcnow(),
    )
    dna_id = repository.upsert_style_dna(conn, dna)
    # Devolve a linha relida: o que o resto do sistema usa e o que esta gravado.
    return repository.get_style_dna(conn, dna_id) or dna.model_copy(update={"id": dna_id})


def summarize_dna(dna: StyleDna) -> str:
    """Resumo de uma tela para a CLI. Sem colchetes: o console usa markup rich."""
    descriptor = dna.descriptor
    ids = ", ".join(str(i) for i in dna.source_asset_ids) or "-"
    header = f"Style DNA '{dna.name}'"
    if dna.pillar:
        header += f"   pilar {dna.pillar}"
    if dna.id is not None:
        header += f"   id {dna.id}"

    rows = (
        ("fotos de origem", f"{len(dna.source_asset_ids)} (ids {ids})"),
        ("paleta", ", ".join(descriptor.palette)),
        ("luz", descriptor.light_quality),
        ("lente", descriptor.lens),
        ("textura", descriptor.texture),
        ("enquadramento", descriptor.framing),
        ("materiais", ", ".join(descriptor.recurring_materials)),
        ("clima", descriptor.mood),
        ("evitar", ", ".join(descriptor.avoid)),
    )
    width = max(len(label) for label, _ in rows)
    lines = [header]
    lines.extend(f"  {label.ljust(width)}  {value or '-'}" for label, value in rows)
    return "\n".join(lines)


__all__ = [
    "DEFAULT_LIMIT",
    "DNA_SYSTEM_PROMPT",
    "MAX_ASSETS",
    "MIN_ASSETS",
    "VISION_MODEL_ENV",
    "VisionClient",
    "build_vision_messages",
    "encode_asset_for_vision",
    "extract_message_text",
    "extract_style_dna",
    "parse_descriptor",
    "resolve_vision_model",
    "select_assets_for_dna",
    "summarize_dna",
]
