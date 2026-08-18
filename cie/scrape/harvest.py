"""Orquestracao da colheita: alvo -> snippet certo -> envelope em disco.

O envelope e gravado ANTES de qualquer download. Se o download falhar depois,
a colheita nao se perde: `cie scrape collect <arquivo>` retoma dali.

`browser_mod` e injetavel para o teste substituir o Playwright inteiro por um
duble - e o unico jeito de testar a orquestracao sem abrir browser.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..errors import ScrapeError
from .models import caminho_seguro
from .targets import HashtagTarget, PostTarget, ProfileTarget, Target, shortcode_to_media_id


def build_envelope(target: Target, resultado: dict) -> dict:
    """Junta alvo, carimbo e paginas cruas no formato que o parser espera."""
    if not isinstance(resultado, dict):
        raise ScrapeError(
            f"resultado do snippet deveria ser objeto, veio {type(resultado).__name__}"
        )

    alvo: dict[str, Any] = {"kind": target.kind, "slug": target.slug}
    if isinstance(target, ProfileTarget):
        alvo["handle"] = target.handle
    elif isinstance(target, PostTarget):
        alvo["shortcode"] = target.shortcode
    elif isinstance(target, HashtagTarget):
        alvo["tag"] = target.tag

    return {
        "target": alvo,
        "harvested_at": datetime.now(tz=timezone.utc).isoformat(),
        "source": resultado.get("source", ""),
        "pages": resultado.get("pages") or [],
    }


def write_envelope(envelope: dict, out_root: Path) -> Path:
    """Grava em `<out_root>/_colheita/<slug>-<carimbo>.json`.

    O slug pode vir de um envelope montado a mao (nao so de `build_envelope`),
    entao passa por `caminho_seguro` antes de virar nome de arquivo - do
    contrario um slug hostil como "../../x" escaparia de `_colheita/`. O
    carimbo tem resolucao de microssegundo e, se ainda assim colidir, ganha
    sufixo `-2`, `-3`, ... para nunca sobrescrever uma colheita anterior.
    """
    pasta = Path(out_root) / "_colheita"
    pasta.mkdir(parents=True, exist_ok=True)

    slug_bruto = str(envelope.get("target", {}).get("slug") or "")
    slug = caminho_seguro(slug_bruto, padrao="sem-alvo")
    carimbo = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%S%f")

    caminho = pasta / f"{slug}-{carimbo}.json"
    contador = 2
    while caminho.exists():
        caminho = pasta / f"{slug}-{carimbo}-{contador}.json"
        contador += 1

    caminho.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
    return caminho


def harvest(
    target: Target,
    *,
    profile_dir: Path,
    limit: int = 12,
    headless: bool = True,
    browser_mod: Any = None,
) -> dict:
    """Abre a sessao, roda o snippet do alvo, devolve o envelope. Nao baixa nada."""
    if browser_mod is None:
        from . import browser as browser_mod  # import tardio: Playwright e opcional

    with browser_mod.open_page(profile_dir, headless=headless) as pagina:
        browser_mod.goto_instagram(pagina)
        if not browser_mod.is_logged_in(pagina):
            raise ScrapeError(
                "a sessao salva nao esta logada no Instagram. "
                "Rode 'cie scrape login' e faca login uma vez."
            )

        params: dict[str, Any] = {"appId": browser_mod.app_id(pagina)}

        if isinstance(target, ProfileTarget):
            snippet = "profile"
            params |= {"handle": target.handle, "limit": max(0, limit)}
        elif isinstance(target, PostTarget):
            snippet = "post"
            params |= {"mediaId": str(shortcode_to_media_id(target.shortcode))}
        elif isinstance(target, HashtagTarget):
            snippet = "hashtag"
            params |= {"tag": target.tag}
        else:
            raise ScrapeError(f"alvo nao suportado: {type(target).__name__}")

        resultado = browser_mod.run_snippet(pagina, snippet, params)

    return build_envelope(target, resultado)
