"""Carregamento e validacao dos templates de cena (YAML -> Template).

O arquivo YAML e a fonte da verdade; a tabela `templates` e apenas um espelho
sincronizado por `sync_templates`. A chave natural e `name`, entao renomear um
arquivo cria um template novo em vez de atualizar o existente.

Aqui mora a primeira barreira do principio da casa: um template que mexe em
texto de embalagem nao passa na validacao sem `requires_reference: true`. O
`cie.guardrails` cuida do resto em tempo de execucao; este modulo garante que
o catalogo de cenas ja nasce coerente.
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from . import repository
from .enums import AspectRatio, Pillar, RiskFlag, TemplateKind
from .errors import TemplateError
from .models import Template

#: Termos que todo `negative_prompt` precisa carregar. Sao os oito modos de falha
#: que mais denunciam imagem sintetica na feed da marca.
DEFAULT_NEGATIVE_TERMS: tuple[str, ...] = (
    "warped text",
    "distorted logo",
    "extra fingers",
    "plastic skin",
    "oversaturated HDR",
    "watermark",
    "stock photo look",
    "uncanny faces",
)

#: Extensoes reconhecidas dentro do diretorio de templates.
TEMPLATE_SUFFIXES: tuple[str, ...] = (".yaml", ".yml")

#: Chaves aceitas no YAML. Chave desconhecida e erro, nao silencio: um
#: `requires_referece` com typo viraria template sem guarda.
ALLOWED_KEYS: frozenset[str] = frozenset(
    {
        "name",
        "pillar",
        "kind",
        "default_aspect_ratio",
        "requires_reference",
        "risk_flags",
        "variables",
        "body",
        "negative_prompt",
        "notes",
    }
)

#: Placeholder no formato {snake_case}; ignora `{}` solto e chaves com espaco.
_PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")


def default_negative_prompt() -> str:
    """Base minima de negative prompt, para quem cria template novo."""
    return ", ".join(DEFAULT_NEGATIVE_TERMS)


def required_variables(template: Template) -> set[str]:
    """Placeholders efetivamente usados no corpo do prompt."""
    return {match.group(1) for match in _PLACEHOLDER_RE.finditer(template.body)}


def validate_template(template: Template) -> list[str]:
    """Devolve a lista de problemas do template; vazia significa aprovado."""
    issues: list[str] = []

    if not template.name.strip():
        issues.append("name vazio")

    if not template.body.strip():
        issues.append("body vazio")
    else:
        missing = sorted(required_variables(template) - set(template.variables))
        if missing:
            issues.append(
                "placeholders sem default em variables: " + ", ".join(missing)
            )

    lowered = template.negative_prompt.lower()
    absent = [term for term in DEFAULT_NEGATIVE_TERMS if term.lower() not in lowered]
    if absent:
        issues.append("negative_prompt sem os termos obrigatorios: " + ", ".join(absent))

    if RiskFlag.PACKAGING_TEXT in template.risk_flags and not template.requires_reference:
        issues.append(
            "risk_flag packaging_text exige requires_reference: true "
            "(logotipo e tipografia nunca sao gerados do zero)"
        )

    # Um Template montado em codigo pode trazer string crua nestes dois campos;
    # o YAML ja passou pelos enums, mas a validacao vale para os dois caminhos.
    try:
        TemplateKind(str(template.kind))
    except ValueError:
        issues.append(f"kind invalido: {template.kind!r}")
    try:
        AspectRatio(str(template.default_aspect_ratio))
    except ValueError:
        issues.append(f"default_aspect_ratio invalido: {template.default_aspect_ratio!r}")

    return issues


# --------------------------------------------------------------------------- #
# leitura do YAML
# --------------------------------------------------------------------------- #


def _enum(
    enum_cls: type,
    value: Any,
    field: str,
    path: Path,
    *,
    required: bool = False,
) -> Any:
    if value is None or value == "":
        if required:
            raise TemplateError(f"{path}: campo obrigatorio ausente: {field}")
        return None
    try:
        return enum_cls(str(value))
    except ValueError:
        accepted = ", ".join(member.value for member in enum_cls)
        raise TemplateError(
            f"{path}: {field} invalido: {value!r} (aceitos: {accepted})"
        ) from None


def _text(value: Any, field: str, path: Path, *, default: str | None = None) -> str:
    if value is None:
        if default is None:
            raise TemplateError(f"{path}: campo obrigatorio ausente: {field}")
        return default
    if not isinstance(value, str):
        raise TemplateError(
            f"{path}: {field} precisa ser texto, veio {type(value).__name__}"
        )
    return value


def _bool(value: Any, field: str, path: Path, *, default: bool = False) -> bool:
    if value is None:
        return default
    if not isinstance(value, bool):
        # "false" (string) seria verdadeiro em Python; melhor recusar cedo.
        raise TemplateError(f"{path}: {field} precisa ser true ou false, veio {value!r}")
    return value


def _risk_flags(value: Any, path: Path) -> list[RiskFlag]:
    if value is None:
        return []
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise TemplateError(
            f"{path}: risk_flags precisa ser uma lista, veio {type(value).__name__}"
        )
    return [_enum(RiskFlag, item, "risk_flags", path, required=True) for item in value]


def _variables(value: Any, path: Path) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise TemplateError(
            f"{path}: variables precisa ser um mapeamento, veio {type(value).__name__}"
        )
    resolved: dict[str, str] = {}
    for key, item in value.items():
        if item is None:
            raise TemplateError(
                f"{path}: variables[{key!r}] esta vazio; todo placeholder precisa de default"
            )
        resolved[str(key)] = str(item)
    return resolved


def _build_template(data: dict[str, Any], path: Path) -> Template:
    unknown = sorted(set(map(str, data)) - ALLOWED_KEYS)
    if unknown:
        raise TemplateError(f"{path}: chaves desconhecidas: {', '.join(unknown)}")

    # Sem `name` explicito o nome do arquivo manda: e a convencao do diretorio.
    name = _text(data.get("name", path.stem), "name", path).strip()
    raw_notes = data.get("notes")
    notes = _text(raw_notes, "notes", path) if raw_notes is not None else None

    try:
        return Template(
            name=name,
            pillar=_enum(Pillar, data.get("pillar"), "pillar", path),
            kind=_enum(TemplateKind, data.get("kind"), "kind", path, required=True),
            body=_text(data.get("body"), "body", path),
            negative_prompt=_text(
                data.get("negative_prompt"), "negative_prompt", path, default=""
            ),
            requires_reference=_bool(
                data.get("requires_reference"), "requires_reference", path
            ),
            risk_flags=_risk_flags(data.get("risk_flags"), path),
            default_aspect_ratio=_enum(
                AspectRatio,
                data.get("default_aspect_ratio", AspectRatio.R1_1.value),
                "default_aspect_ratio",
                path,
                required=True,
            ),
            variables=_variables(data.get("variables"), path),
            notes=notes,
        )
    except ValidationError as exc:
        raise TemplateError(f"{path}: template invalido: {exc}") from exc


def _format_issues(path: Path, issues: list[str]) -> str:
    joined = "\n".join(f"  - {issue}" for issue in issues)
    return f"{path}: template invalido:\n{joined}"


def load_template_file(path: Path | str, *, validate: bool = True) -> Template:
    """Le um YAML e devolve o Template. `validate=False` so faz o parse."""
    path = Path(path)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TemplateError(f"{path}: nao foi possivel ler o arquivo: {exc}") from exc

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise TemplateError(f"{path}: YAML malformado: {exc}") from exc

    if data is None:
        raise TemplateError(f"{path}: arquivo vazio")
    if not isinstance(data, dict):
        raise TemplateError(
            f"{path}: raiz do YAML precisa ser um mapeamento, veio {type(data).__name__}"
        )

    template = _build_template(data, path)
    if validate:
        issues = validate_template(template)
        if issues:
            raise TemplateError(_format_issues(path, issues))
    return template


def load_templates_dir(path: Path | str, *, validate: bool = True) -> list[Template]:
    """Carrega o diretorio inteiro, ordenado por nome.

    Nao para no primeiro erro: junta tudo em um unico TemplateError para que
    quem edita os YAML veja a lista completa de uma vez.
    """
    directory = Path(path)
    if not directory.is_dir():
        raise TemplateError(f"{directory}: diretorio de templates nao encontrado")

    files = sorted(
        item
        for item in directory.iterdir()
        if item.is_file() and item.suffix.lower() in TEMPLATE_SUFFIXES
    )

    templates: list[Template] = []
    problems: list[str] = []
    seen: dict[str, Path] = {}

    for file in files:
        try:
            template = load_template_file(file, validate=validate)
        except TemplateError as exc:
            problems.append(str(exc))
            continue
        if template.name in seen:
            problems.append(
                f"{file}: nome duplicado {template.name!r} "
                f"(ja definido em {seen[template.name]})"
            )
            continue
        seen[template.name] = file
        templates.append(template)

    if problems:
        raise TemplateError(
            f"{directory}: {len(problems)} template(s) invalido(s):\n" + "\n".join(problems)
        )

    templates.sort(key=lambda item: item.name)
    return templates


def sync_templates(conn: sqlite3.Connection, path: Path | str) -> list[int]:
    """Sobe todos os YAML do diretorio para o banco. Idempotente por `name`."""
    templates = load_templates_dir(path)
    return [repository.upsert_template(conn, template) for template in templates]
