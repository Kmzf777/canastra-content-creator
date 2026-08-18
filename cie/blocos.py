"""Blocos de prompt versionados, e o compositor que os monta.

Por que este modulo existe
--------------------------
Os blocos que de fato produziram imagem boa (luz, HDR, foco, espontaneidade,
preservacao, DNA de embalagem, negativos) viviam COPIADOS dentro de cada script
avulso em `_ref-scripts/`. Nove copias, todas divergentes: `humanizar.py` e
`carrossel.py` ainda pediam dia nublado depois de o nublado ter sido derrubado
por `espontaneo.py`; `espontaneo.py` prefixava "Avoid: " duas vezes;
`gemini_gerar.py` tinha uma compressao do bloco de espontaneidade sem a frase que
mata o objeto arrumado. Divergencia em copia manual e como o pico alpino entrou
no logotipo: ninguem escolheu, aconteceu.

Aqui cada bloco tem UM arquivo em `templates/blocos/*.yaml`, com o texto em
ingles verbatim do que foi verificado em geracao real, a razao de existir em
pt-BR, e a lista de negativos que o acompanha.

Ordem de montagem, que e a ordem verificada em `_ref-scripts/espontaneo.py`:

    preservacao -> cena -> DNA -> luz -> HDR -> foco -> espontaneidade -> Avoid

Regra que este modulo se recusa a quebrar
-----------------------------------------
**O bloco de foco nunca sai do prompt.** Desfoque nao se desfaz em pos - tone
mapping, ruido, halo e artefato de JPEG se adicionam depois; profundidade de
campo rasa, nao. Morre na geracao ou nao morre. Por isso `montar()` inclui o
bloco de foco por padrao e levanta `BlocoError` se uma lista explicita vier sem
ele.

Este modulo NAO substitui `cie/prompt.py` nem `cie/template_loader.py`, que sao
legado escrito antes das descobertas de geracao e nunca usados para produzir uma
imagem.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import yaml

__all__ = [
    "Bloco",
    "BlocoError",
    "DIRETORIO_PADRAO",
    "ORDEM_CORPO",
    "PADRAO",
    "carregar",
    "carregar_todos",
    "montar",
]

#: Onde vivem os YAML dos blocos.
DIRETORIO_PADRAO = Path(__file__).resolve().parent.parent / "templates" / "blocos"

#: Ordem de concatenacao do corpo do prompt. `cena` nao e um arquivo: e o
#: argumento de `montar()`. Os negativos nao entram no corpo - viram a linha
#: "Avoid: ..." no fim.
ORDEM_CORPO: tuple[str, ...] = (
    "preservacao",
    "cena",
    "dna",
    "luz",
    "hdr",
    "foco",
    "espontaneidade",
)

#: Conjunto padrao de `montar()`. Nao inclui preservacao nem DNA porque os dois
#: dependem do fluxo (edicao x Gemini) e do SKU; inclui foco porque foco nao e
#: opcional.
PADRAO: tuple[str, ...] = (
    "luz-sol-pino",
    "hdr-celular",
    "foco-profundo",
    "espontaneidade",
    "negativos",
)

#: Papel de cada bloco conhecido. Um bloco novo com prefixo conhecido
#: (`dna-`, `luz-`, `hdr-`, `foco-`, `preservar-`) e classificado sozinho.
_PAPEIS: dict[str, str] = {
    "preservar-embalagem": "preservacao",
    "dna-suave": "dna",
    "dna-classico": "dna",
    "dna-canela": "dna",
    "luz-sol-pino": "luz",
    "hdr-celular": "hdr",
    "foco-profundo": "foco",
    "espontaneidade": "espontaneidade",
    "negativos": "negativos",
}

_PREFIXOS: tuple[tuple[str, str], ...] = (
    ("preservar-", "preservacao"),
    ("dna-", "dna"),
    ("luz-", "luz"),
    ("hdr-", "hdr"),
    ("foco-", "foco"),
    ("espontaneidade", "espontaneidade"),
    ("negativos", "negativos"),
)

_CAMPOS_OBRIGATORIOS = ("nome", "descricao", "texto")


class BlocoError(RuntimeError):
    """Bloco ausente, malformado, ou montagem que viola uma regra do motor."""


def papel_de(nome: str) -> str:
    """Papel do bloco, que decide a posicao dele na montagem."""
    if nome in _PAPEIS:
        return _PAPEIS[nome]
    for prefixo, papel in _PREFIXOS:
        if nome.startswith(prefixo):
            return papel
    raise BlocoError(
        f"bloco {nome!r}: papel desconhecido. Registre em cie.blocos._PAPEIS ou "
        f"use um nome com prefixo conhecido ({', '.join(p for p, _ in _PREFIXOS)})."
    )


@dataclass(frozen=True)
class Bloco:
    """Um bloco de prompt versionado.

    `texto` e o corpo em ingles, verbatim do que foi verificado em geracao real.
    `descricao` e pt-BR e explica por que o bloco existe e o que ele corrige -
    ela e o que impede a proxima sessao de "melhorar" um bloco de volta para o
    erro que ele conserta.
    """

    nome: str
    descricao: str
    texto: str
    negativos: tuple[str, ...] = ()

    @property
    def papel(self) -> str:
        return papel_de(self.nome)


def _caminho(nome: str, diretorio: Path | str | None) -> Path:
    base = Path(diretorio) if diretorio is not None else DIRETORIO_PADRAO
    stem = nome[:-5] if nome.endswith(".yaml") else nome
    return base / f"{stem}.yaml"


def _ler(caminho: Path) -> Bloco:
    try:
        cru = yaml.safe_load(caminho.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # noqa: PERF203
        raise BlocoError(f"{caminho}: YAML invalido - {exc}") from exc

    if not isinstance(cru, dict):
        raise BlocoError(f"{caminho}: esperado um mapeamento no topo do arquivo")

    faltando = [c for c in _CAMPOS_OBRIGATORIOS if not str(cru.get(c) or "").strip()]
    if faltando:
        raise BlocoError(f"{caminho}: campo(s) obrigatorio(s) vazio(s): {', '.join(faltando)}")

    nome = str(cru["nome"]).strip()
    if nome != caminho.stem:
        raise BlocoError(
            f"{caminho}: campo `nome` e {nome!r} mas o arquivo e {caminho.stem!r}. "
            "Os dois tem que bater, senao `carregar(nome)` acha o arquivo errado."
        )

    brutos = cru.get("negativos") or []
    if isinstance(brutos, str):
        brutos = [t.strip() for t in brutos.split(",")]
    if not isinstance(brutos, list):
        raise BlocoError(f"{caminho}: `negativos` tem que ser uma lista")

    negativos = tuple(str(t).strip() for t in brutos if str(t).strip())
    for termo in negativos:
        if termo.lower().startswith("avoid"):
            raise BlocoError(
                f"{caminho}: termo negativo {termo!r} carrega o prefixo 'Avoid'. "
                "A lista guarda so os termos; quem escreve 'Avoid: ' e `montar()`. "
                "Foi assim que os prompts salvos sairam com 'Avoid: Avoid: ...'."
            )

    papel_de(nome)  # valida cedo: bloco sem papel conhecido nao carrega

    return Bloco(
        nome=nome,
        descricao=str(cru["descricao"]).strip(),
        texto=str(cru["texto"]).strip(),
        negativos=negativos,
    )


def carregar(nome: str, *, diretorio: Path | str | None = None) -> Bloco:
    """Carrega um bloco pelo nome (com ou sem `.yaml`)."""
    caminho = _caminho(nome, diretorio)
    if not caminho.is_file():
        # Lista pelo nome de arquivo, e nao carregando tudo: se outro bloco
        # estiver quebrado, o erro que interessa aqui e o do bloco ausente.
        disponiveis = ", ".join(sorted(c.stem for c in caminho.parent.glob("*.yaml")))
        raise BlocoError(
            f"bloco {nome!r} nao existe em {caminho.parent}. Disponiveis: {disponiveis or '(nenhum)'}"
        )
    return _ler(caminho)


def carregar_todos(*, diretorio: Path | str | None = None) -> dict[str, Bloco]:
    """Carrega o diretorio inteiro, ordenado por nome."""
    base = Path(diretorio) if diretorio is not None else DIRETORIO_PADRAO
    if not base.is_dir():
        raise BlocoError(f"{base}: diretorio de blocos nao encontrado")
    return {c.stem: _ler(c) for c in sorted(base.glob("*.yaml"))}


def _resolver(
    blocos: Sequence[str | Bloco] | None,
    *,
    diretorio: Path | str | None,
) -> list[Bloco]:
    escolhidos = PADRAO if blocos is None else tuple(blocos)
    resolvidos: list[Bloco] = []
    vistos: set[str] = set()
    for item in escolhidos:
        bloco = item if isinstance(item, Bloco) else carregar(str(item), diretorio=diretorio)
        if bloco.nome in vistos:
            continue
        vistos.add(bloco.nome)
        resolvidos.append(bloco)
    return resolvidos


def _dedup(termos: Iterable[str]) -> list[str]:
    """Remove repetido sem perder a ordem, comparando sem caixa."""
    saida: list[str] = []
    vistos: set[str] = set()
    for termo in termos:
        limpo = " ".join(str(termo).split())
        chave = limpo.lower()
        if not limpo or chave in vistos:
            continue
        vistos.add(chave)
        saida.append(limpo)
    return saida


def montar(
    cena: str,
    blocos: Sequence[str | Bloco] | None = None,
    negativos_extra: Iterable[str] | None = None,
    *,
    diretorio: Path | str | None = None,
) -> str:
    """Monta o prompt final a partir da cena e dos blocos.

    Ordem: preservacao -> cena -> DNA -> luz -> HDR -> foco -> espontaneidade,
    e no fim uma linha "Avoid: " com os negativos de todos os blocos usados mais
    `negativos_extra`, sem repeticao.

    `blocos=None` usa `PADRAO`, que ja inclui o bloco de foco. Uma lista
    explicita SEM bloco de foco levanta `BlocoError`: sem ele o modelo entrega
    fundo desfocado, e desfoque nao se remove em pos.
    """
    if not str(cena or "").strip():
        raise BlocoError("montar: `cena` vazia. O prompt precisa dizer o que esta acontecendo.")

    resolvidos = _resolver(blocos, diretorio=diretorio)
    papeis = [b.papel for b in resolvidos]

    if "foco" not in papeis:
        raise BlocoError(
            "montar: nenhum bloco de foco na lista. O bloco anti-bokeh e obrigatorio - "
            "sem ele o modelo entrega fundo desfocado, e desfoque nao se remove em pos "
            "(tone mapping, ruido, halo e JPEG se adicionam depois; profundidade de campo "
            "rasa, nao). Inclua 'foco-profundo' ou use blocos=None."
        )

    partes: list[str] = []
    for papel in ORDEM_CORPO:
        if papel == "cena":
            partes.append(str(cena).strip())
            continue
        partes.extend(b.texto.strip() for b in resolvidos if b.papel == papel and b.texto.strip())

    negativos: list[str] = []
    for papel in (*ORDEM_CORPO, "negativos"):
        for bloco in resolvidos:
            if bloco.papel == papel:
                negativos.extend(bloco.negativos)
    negativos.extend(negativos_extra or ())

    prompt = "\n\n".join(partes)
    limpos = _dedup(negativos)
    if limpos:
        prompt += "\n\nAvoid: " + ", ".join(limpos) + "."
    return prompt
