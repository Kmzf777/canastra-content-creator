"""Download das imagens colhidas, com dedupe e proveniencia.

Tres regras que nao se negociam:

  * video nunca e baixado;
  * todo arquivo nasce com sidecar - arquivo sem sidecar e bug;
  * nada sobrescreve nada, e conteudo repetido (sha256) e pulado.

`fetch` e injetavel para que o teste rode sem tocar a rede. O padrao usa httpx,
importado sob demanda.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .models import HarvestBatch, ScrapedItem

#: Sem User-Agent de browser e sem Referer, o CDN do Instagram devolve 403.
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.instagram.com/",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
}

Fetcher = Callable[[str], bytes]


@dataclass
class ItemOutcome:
    item: ScrapedItem
    status: str  # baixado | duplicado | video | erro | previsto
    path: Path | None = None
    sha256: str = ""
    motivo: str = ""


@dataclass
class DownloadReport:
    out_root: Path
    dry_run: bool = False
    outcomes: list[ItemOutcome] = field(default_factory=list)

    def _com_status(self, status: str) -> list[ItemOutcome]:
        return [o for o in self.outcomes if o.status == status]

    @property
    def baixados(self) -> int:
        return len(self._com_status("baixado"))

    @property
    def duplicados(self) -> int:
        return len(self._com_status("duplicado"))

    @property
    def videos_pulados(self) -> int:
        return len(self._com_status("video"))

    @property
    def erros(self) -> int:
        return len(self._com_status("erro"))

    @property
    def previstos(self) -> int:
        return len(self._com_status("previsto"))

    def mensagens_de_erro(self) -> list[str]:
        return [f"{o.item.shortcode}: {o.motivo}" for o in self._com_status("erro")]


def download_batch(
    batch: HarvestBatch,
    *,
    out_root: Path,
    fetch: Fetcher | None = None,
    limit: int = 0,
    delay: float = 1.0,
    dry_run: bool = False,
) -> DownloadReport:
    """Baixa as imagens de um lote. `limit=0` significa sem teto."""
    out_root = Path(out_root)
    buscar = fetch or _httpx_fetch
    relatorio = DownloadReport(out_root=out_root, dry_run=dry_run)

    destino_dir = out_root / batch.target_slug
    conhecidos = _hashes_existentes(out_root)
    baixados = 0

    for item in batch.items:
        if item.is_video:
            relatorio.outcomes.append(
                ItemOutcome(item=item, status="video", motivo="video nao vira referencia")
            )
            continue
        if not item.display_url:
            relatorio.outcomes.append(
                ItemOutcome(
                    item=item,
                    status="video",
                    motivo="sem display_url; nao ha o que baixar",
                )
            )
            continue

        if limit and baixados >= limit:
            break

        if dry_run:
            relatorio.outcomes.append(
                ItemOutcome(item=item, status="previsto", path=destino_dir / item.filename)
            )
            baixados += 1
            continue

        try:
            conteudo = buscar(item.display_url)
        except Exception as exc:  # noqa: BLE001 - falha de um item nao derruba o lote
            relatorio.outcomes.append(
                ItemOutcome(item=item, status="erro", motivo=str(exc))
            )
            continue

        digest = hashlib.sha256(conteudo).hexdigest()
        if digest in conhecidos:
            relatorio.outcomes.append(
                ItemOutcome(
                    item=item,
                    status="duplicado",
                    sha256=digest,
                    motivo="conteudo identico ja esta em raspagem/",
                )
            )
            continue

        destino = _caminho_livre(destino_dir, item.filename)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(conteudo)
        _grava_sidecar(destino, item, digest)

        conhecidos.add(digest)
        baixados += 1
        relatorio.outcomes.append(
            ItemOutcome(item=item, status="baixado", path=destino, sha256=digest)
        )

        if delay:
            time.sleep(delay)

    if not dry_run:
        _atualiza_manifest(out_root, relatorio)

    return relatorio


def _httpx_fetch(url: str) -> bytes:
    import httpx

    resposta = httpx.get(url, headers=_HEADERS, timeout=30.0, follow_redirects=True)
    resposta.raise_for_status()
    return resposta.content


def _hashes_existentes(out_root: Path) -> set[str]:
    """Le os sidecars ja em disco. E por isso que sidecar e obrigatorio."""
    conhecidos: set[str] = set()
    if not out_root.is_dir():
        return conhecidos
    for sidecar in out_root.rglob("*.json"):
        if sidecar.name.startswith("_"):
            continue
        try:
            dados = json.loads(sidecar.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(dados, dict):
            # Nao e um sidecar nosso (ex.: envelope de _colheita/ com lista no topo).
            continue
        digest = dados.get("sha256")
        if digest:
            conhecidos.add(digest)
    return conhecidos


def _caminho_livre(pasta: Path, nome: str) -> Path:
    """Nunca sobrescreve: se o nome existe, sufixa -2, -3, ..."""
    destino = pasta / nome
    if not destino.exists():
        return destino
    base, sufixo = destino.stem, destino.suffix
    contador = 2
    while True:
        candidato = pasta / f"{base}-{contador}{sufixo}"
        if not candidato.exists():
            return candidato
        contador += 1


def _grava_sidecar(destino: Path, item: ScrapedItem, digest: str) -> None:
    sidecar = destino.with_suffix(".json")
    dados = {
        "post_url": item.post_url,
        "owner_handle": item.owner_handle,
        "shortcode": item.shortcode,
        "carousel_index": item.carousel_index,
        "source_url": item.display_url,
        "width": item.width,
        "height": item.height,
        "taken_at": item.taken_at.isoformat() if item.taken_at else None,
        "caption": item.caption,
        "sha256": digest,
        "scraped_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    sidecar.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")


def _atualiza_manifest(out_root: Path, relatorio: DownloadReport) -> None:
    """Indice acumulado de tudo sob `raspagem/`, chaveado por sha256."""
    caminho = out_root / "_manifest.json"
    registros: dict[str, dict] = {}
    if caminho.is_file():
        try:
            antigo = json.loads(caminho.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            antigo = {}
        for registro in antigo.get("arquivos", []) if isinstance(antigo, dict) else []:
            # Um registro malformado nao pode derrubar o indice inteiro - so ele e pulado.
            if isinstance(registro, dict) and "sha256" in registro:
                registros[registro["sha256"]] = registro

    for outcome in relatorio.outcomes:
        if outcome.status != "baixado" or outcome.path is None:
            continue
        registros[outcome.sha256] = {
            "path": outcome.path.relative_to(out_root).as_posix(),
            "sha256": outcome.sha256,
            "post_url": outcome.item.post_url,
            "owner_handle": outcome.item.owner_handle,
        }

    caminho.parent.mkdir(parents=True, exist_ok=True)
    conteudo = {
        "atualizado_em": datetime.now(tz=timezone.utc).isoformat(),
        "arquivos": sorted(registros.values(), key=lambda r: r["path"]),
    }
    caminho.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
