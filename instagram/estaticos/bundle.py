"""A pasta de saida e o sidecar.

O sidecar responde "de onde veio isto" sem abrir o historico do git: fonte com
sha256, strings esperadas, veredito por campo, degraus percorridos e o laudo.
A ORIGEM DE CADA DADO VIAJA JUNTO -- e o que permite, seis meses depois,
saber que `R$ 31,70` veio da tabela de 11/09/2026 e nao da memoria de alguem.

Quando o degrau 6 roda, parte do rotulo e pixel composto e nao saida do
modelo. O sidecar declara isso em `degraus`; nao se esconde.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

from .catalogo import MOLDES, Peca
from .conferir import bloqueia


class BundleBloqueado(Exception):
    """A peca nao vira pasta. Bloqueio, nao aviso."""


def _sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def escrever(
    peca: Peca,
    png: Path,
    legenda: str,
    vereditos: dict[str, str],
    degraus: tuple[str, ...],
    tentativas: int,
    laudo: dict,
    raiz: Path,
    data: str,
) -> Path:
    faltando = [s for s in peca.strings_impressas if s not in vereditos]
    if faltando:
        raise BundleBloqueado(
            f"string declarada sem veredito: {', '.join(faltando)}"
        )

    barrados = bloqueia(vereditos)
    if barrados:
        raise BundleBloqueado(
            "campos barram a peca (errado ou nao-verificavel): "
            + ", ".join(barrados)
        )

    if not laudo.get("aprovado", False):
        raise BundleBloqueado(f"laudo reprovado: {laudo}")

    molde = MOLDES[peca.molde]
    with Image.open(png) as im:
        if im.size != (molde.largura, molde.altura):
            raise BundleBloqueado(
                f"peca e {im.width}x{im.height}; o molde '{peca.molde}' exige "
                f"{molde.largura}x{molde.altura}"
            )

    destino = raiz / f"{data}-{peca.slug}"
    destino.mkdir(parents=True, exist_ok=True)

    destino.joinpath("peca.png").write_bytes(png.read_bytes())
    destino.joinpath("legenda.txt").write_text(legenda, encoding="utf-8")

    sidecar = {
        "slug": peca.slug,
        "molde": peca.molde,
        "fonte": str(peca.fonte),
        "fonte_sha256": _sha256(peca.fonte),
        "strings_esperadas": list(peca.strings_impressas),
        "conferencia": dict(vereditos),
        "dados": {
            k: {"valor": d.valor, "origem": d.origem} for k, d in peca.dados.items()
        },
        "degraus": list(degraus),
        "tentativas": tentativas,
        "laudo": laudo,
        "gerado_em": data,
    }
    destino.joinpath("sidecar.json").write_text(
        json.dumps(sidecar, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    return destino
