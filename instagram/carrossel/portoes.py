"""Os tres portoes. Nenhuma das quatro skills publicas lidas tem os tres juntos.

A ORDEM IMPORTA, e e de custo crescente:

1. `orcamento`  -- DECLARADO. Conta caractere contra teto. E heuristica barata que
   recusa ANTES de gastar render. Vem de charlesdove977.
2. `transbordo` -- MEDIDO. O Chrome diz quem transbordou e quem invadiu a area
   segura. E o fato; o orcamento e so o palpite.
3. `legibilidade` -- MEDIDO contra piso DECLARADO. Vem de charlie947: inspecionar
   no tamanho do feed, nao so em tamanho cheio.

`todos()` devolve as tres listas; quem decide parar e o chamador.

Spec: docs/superpowers/specs/2026-10-05-carrossel-motor-design.md secao 5
"""

from __future__ import annotations

from .molde import FEED_LARGURAS, PISO_FEED_PX, PISO_QUADRO_PX, px_no_feed
from .tipos import Deck, validar


def orcamento(deck: Deck) -> list[str]:
    """Teto de caracteres por campo.

    REUSA `tipos.validar` em vez de reimplementar: a contagem de caracteres ja vive
    la, junto com a validacao de campo obrigatorio e de ritmo, e duas copias da
    mesma regra divergem no primeiro ajuste.

    E HEURISTICA, nao fato. Um titulo dentro do teto ainda pode transbordar numa
    palavra longa sem ponto de quebra -- quem decide isso e `transbordo`.
    """
    return validar(deck)


def transbordo(medicoes: list[dict]) -> list[str]:
    """Caixa que estourou, e texto que invadiu a area segura do Instagram.

    Isto e medicao: `scrollHeight > clientHeight` e `getBoundingClientRect()` lidos
    pelo proprio Chrome. Nao ha estimativa aqui.
    """
    p: list[str] = []
    for m in medicoes:
        n = m.get("slide", "?")
        for campo in m.get("transbordos", ()):
            p.append(
                f"slide {n}: o campo '{campo}' TRANSBORDA a caixa -- "
                "encurte o texto ou mude o tipo de slide"
            )
        for campo in m.get("fora_do_quadro", ()):
            p.append(
                f"slide {n}: o campo '{campo}' escapa do quadro de 1080x1350"
            )
        for campo in m.get("fora_da_area_segura", ()):
            p.append(
                f"slide {n}: o campo '{campo}' invade a area segura da interface "
                "do Instagram (cabecalho do perfil ou barra de progresso)"
            )
    return p


def legibilidade(medicoes: list[dict]) -> list[str]:
    """Nenhum texto abaixo do piso, medido no tamanho em que as pessoas leem.

    O PISO DE 11px NO FEED E DECISAO, NAO MEDICAO. Esta aqui para ser contestado
    com um teste de leitura de verdade, nao para ser citado como fato. E numero
    nenhum substitui abrir o `_feed/360.png` e olhar -- e por isso que
    `render.miniaturas` existe.
    """
    p: list[str] = []
    for m in medicoes:
        n = m.get("slide", "?")
        for t in m.get("textos", ()):
            px = float(t.get("px", 0))
            if px < PISO_QUADRO_PX:
                no_feed = px_no_feed(px, FEED_LARGURAS[0])
                p.append(
                    f"slide {n}: o campo '{t.get('campo')}' tem {px:.0f}px no quadro "
                    f"= {no_feed:.1f}px no feed de {FEED_LARGURAS[0]}px; "
                    f"o piso e {PISO_QUADRO_PX:.0f}px / {PISO_FEED_PX:.0f}px"
                )
    return p


def todos(deck: Deck, medicoes: list[dict]) -> dict:
    """Roda os tres. `ok` so e True com as tres listas vazias."""
    r = {
        "orcamento": orcamento(deck),
        "transbordo": transbordo(medicoes),
        "legibilidade": legibilidade(medicoes),
    }
    r["ok"] = not any(r[k] for k in ("orcamento", "transbordo", "legibilidade"))
    return r
