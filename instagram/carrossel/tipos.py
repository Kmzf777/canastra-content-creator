"""Taxonomia de slides. E o CONTRATO que render, portoes e catalogo consomem.

Nove tipos portados de `itchernetski/threads-carousel-claude-skill` (podando
`emoji` e `checklist`, fundindo `hook`/`body`) e um que e nosso: `prova`.

POR QUE `prova` EXISTE. O posicionamento da marca e "a gente consegue provar":
GPS no EXIF, 41 anuncios medidos, 1.250 m gravados no arquivo. Um tipo de slide
que EXIGE o campo `fonte` transforma isso em estrutura em vez de boa intencao --
a mesma ideia do `Dado.origem` em instagram/estaticos/catalogo.py.

Spec: docs/superpowers/specs/2026-10-05-carrossel-motor-design.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .molde import FUNDOS, MAX_FUNDO_SEGUIDO, ORCAMENTO

#: tipo -> (campos obrigatorios, campos opcionais)
CAMPOS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "capa":       (("manchete",), ("sub", "badge")),
    "conceito":   (("titulo", "corpo"), ()),
    "lista":      (("titulo", "itens"), ()),
    "passo":      (("titulo", "passos"), ()),
    "comparacao": (("rotulo_esq", "itens_esq", "rotulo_dir", "itens_dir"), ("titulo",)),
    "numero":     (("numero", "rotulo"), ("sub",)),
    "citacao":    (("frase",), ("autor", "papel")),
    "produto":    (("nome", "descritor"), ("sub",)),
    "prova":      (("afirmacao", "evidencia", "fonte"), ()),
    "fecho":      (("manchete",), ("sub", "destino")),
}

TIPOS = tuple(CAMPOS)

#: Campos que sao lista, com minimo e maximo de itens.
COLECOES: dict[str, tuple[int, int]] = {
    "itens": (2, 6),
    "itens_esq": (2, 5),
    "itens_dir": (2, 5),
    "passos": (2, 5),
}

#: Qual teto de ORCAMENTO vale para cada campo de texto simples.
_TETO_DE = {
    "manchete": "manchete", "titulo": "titulo", "corpo": "corpo", "sub": "sub",
    "frase": "frase", "autor": "autor", "papel": "papel", "numero": "numero",
    "rotulo": "rotulo", "nome": "nome", "descritor": "descritor",
    "afirmacao": "afirmacao", "evidencia": "evidencia", "fonte": "fonte",
    "badge": "badge", "destino": "destino",
    "rotulo_esq": "rotulo_esq", "rotulo_dir": "rotulo_dir",
}


@dataclass(frozen=True)
class Slide:
    """Um slide declarado.

    `dados` carrega os campos do tipo; `foto` so existe quando `fundo == "foto"`.
    """

    tipo: str
    fundo: str
    dados: dict
    foto: Path | None = None


@dataclass(frozen=True)
class Deck:
    slug: str
    slides: tuple[Slide, ...]
    legenda: str = ""
    destino: str = ""
    notas: dict = field(default_factory=dict)


class DeclaracaoInvalida(Exception):
    """A declaracao nao passa. Levantada por `exigir_valido`, nao por `validar`."""


def teto_do_campo(campo: str) -> int | None:
    """Teto de caracteres do campo, ou None se o campo nao tem teto proprio."""
    chave = _TETO_DE.get(campo)
    return ORCAMENTO[chave] if chave else None


def _problemas_do_slide(i: int, s: Slide) -> list[str]:
    onde = f"slide {i}"
    p: list[str] = []

    if s.tipo not in CAMPOS:
        return [f"{onde}: tipo '{s.tipo}' nao existe. Validos: {', '.join(TIPOS)}"]
    if s.fundo not in FUNDOS:
        p.append(f"{onde}: fundo '{s.fundo}' nao existe. Validos: {', '.join(FUNDOS)}")

    # foto so com fundo foto, e sempre que fundo for foto
    if s.fundo == "foto" and s.foto is None:
        p.append(f"{onde}: fundo 'foto' exige o campo foto")
    if s.fundo != "foto" and s.foto is not None:
        p.append(f"{onde}: fundo '{s.fundo}' nao aceita foto")
    if s.foto is not None and not s.foto.exists():
        p.append(f"{onde}: foto nao existe no disco: {s.foto}")

    obrig, opc = CAMPOS[s.tipo]
    declarados = set(s.dados)
    for falta in sorted(set(obrig) - declarados):
        p.append(f"{onde}: o tipo '{s.tipo}' exige o campo '{falta}'")
    for sobra in sorted(declarados - set(obrig) - set(opc)):
        p.append(f"{onde}: campo '{sobra}' nao pertence ao tipo '{s.tipo}'")

    for campo in sorted(declarados & (set(obrig) | set(opc))):
        valor = s.dados[campo]

        if campo in COLECOES:
            minimo, maximo = COLECOES[campo]
            if not isinstance(valor, (list, tuple)):
                p.append(f"{onde}: campo '{campo}' tem que ser lista")
                continue
            if not minimo <= len(valor) <= maximo:
                p.append(
                    f"{onde}: campo '{campo}' tem {len(valor)} itens; "
                    f"o tipo '{s.tipo}' aceita de {minimo} a {maximo}"
                )
            for j, item in enumerate(valor):
                if campo == "passos":
                    if not isinstance(item, dict) or not item.get("titulo", "").strip():
                        p.append(f"{onde}: passo {j} sem 'titulo'")
                        continue
                    for sub, teto in (("titulo", ORCAMENTO["passo_titulo"]),
                                      ("texto", ORCAMENTO["passo_texto"])):
                        txt = item.get(sub) or ""
                        if len(txt) > teto:
                            p.append(
                                f"{onde}: passo {j} campo '{sub}' tem {len(txt)} "
                                f"caracteres; o teto e {teto}"
                            )
                else:
                    if not str(item).strip():
                        p.append(f"{onde}: campo '{campo}' item {j} vazio")
                    elif len(str(item)) > ORCAMENTO["item"]:
                        p.append(
                            f"{onde}: campo '{campo}' item {j} tem {len(str(item))} "
                            f"caracteres; o teto e {ORCAMENTO['item']}"
                        )
            continue

        if not str(valor).strip():
            p.append(f"{onde}: campo '{campo}' vazio")
            continue
        teto = teto_do_campo(campo)
        if teto is not None and len(str(valor)) > teto:
            p.append(
                f"{onde}: campo '{campo}' tem {len(str(valor))} caracteres; "
                f"o teto e {teto}"
            )

    return p


def problemas_de_ritmo(slides: tuple[Slide, ...]) -> list[str]:
    """Regras de fundo do deck inteiro. Ver spec secao 3."""
    p: list[str] = []
    if not slides:
        return ["deck sem slides"]

    if slides[0].tipo != "capa":
        p.append(f"o primeiro slide tem que ser 'capa', e e '{slides[0].tipo}'")
    if slides[-1].tipo != "fecho":
        p.append(f"o ultimo slide tem que ser 'fecho', e e '{slides[-1].tipo}'")
    if slides[0].tipo == "capa" and slides[0].fundo != "foto":
        p.append("a capa tem que ter fundo 'foto'")
    if slides[-1].tipo == "fecho" and slides[-1].fundo != "terra":
        p.append("o fecho tem que ter fundo 'terra' -- e a constante que fecha o deck")

    seguidos = 1
    for a, b in zip(slides, slides[1:]):
        seguidos = seguidos + 1 if a.fundo == b.fundo else 1
        if seguidos > MAX_FUNDO_SEGUIDO:
            p.append(
                f"mais de {MAX_FUNDO_SEGUIDO} slides seguidos com fundo "
                f"'{b.fundo}' -- e o que faz o deck parecer generico"
            )
            break
    return p


def validar(deck: Deck) -> list[str]:
    """Devolve TODOS os problemas, um por linha. Lista vazia = declaracao valida.

    Devolve em vez de levantar porque `conferir` precisa reportar tudo de uma vez,
    e nao parar no primeiro -- mesma escolha de instagram/estaticos/catalogo.py.
    """
    p: list[str] = []
    if not deck.slug.strip():
        p.append("deck sem slug")
    if not 3 <= len(deck.slides) <= 10:
        p.append(f"deck tem {len(deck.slides)} slides; o aceito e de 3 a 10")
    for i, s in enumerate(deck.slides, 1):
        p.extend(_problemas_do_slide(i, s))
    p.extend(problemas_de_ritmo(deck.slides))
    return p


def exigir_valido(deck: Deck) -> None:
    problemas = validar(deck)
    if problemas:
        raise DeclaracaoInvalida("\n".join(problemas))
