"""A escada de correcao: sintoma -> degrau, e o laco com teto.

CADA LINHA DE `SINTOMAS` E UMA FALHA JA PAGA NESTE REPOSITORIO. A tabela nao
foi projetada, foi colhida do `Registro de licoes` do CLAUDE.md.

O degrau 6 nao e fracasso do laco: e o seu piso. Ele nao depende do modelo, e
e por isso que o laco termina. A licao 13 registra que abaixo de ~2% da altura
do quadro a tipografia nao sobrevive em NENHUMA rodada -- para esses campos,
insistir em prompt so gasta.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

DEGRAUS: dict[int, str] = {
    1: "soletrar",
    2: "nomear-operacao",
    3: "ancora-familia",
    4: "aumentar-no-quadro",
    5: "n-variantes",
    6: "compor",
}

SINTOMAS: dict[str, int] = {
    # licao 18: saiu `70 / 80 / 80 / 40` onde era 7,0 / 10 / 10 / 6,0
    "valor-inventado": 1,
    # licao 21: `ARABICA` por `ARÁBICA`, `DOCURA` por `DOÇURA`
    "acento-perdido": 1,
    # licoes 1 e 12: referencia errada ou prompt que nao nomeia a operacao
    "rotulo-generico": 2,
    # canastra-embalagem: capsulas Suave chegaram em 591x1280
    "fonte-ruim": 3,
    # licao 13: `Doodo 1985`, `TRODULB E HÚMO`
    "letra-corrompida": 4,
    # site_fundo_branco.py: erra ~1 em 3 mesmo com tudo soletrado
    "erro-intermitente": 5,
    # licao 22: `F:23.2025`, um mes que nao existe -- e o plausivel e pior
    "carimbo-variavel": 6,
    # canastra-conteudo: QR e codigo de barras sao sempre regenerados
    "codigo-2d": 6,
}

ULTIMO_DEGRAU = 6
TETO_PADRAO = 3


def rotear(sintomas: list[str]) -> tuple[int, ...]:
    """Sintomas -> degraus a aplicar, ordenados e sem repeticao.

    Sintoma fora do catalogo levanta `KeyError`. Nao se adivinha degrau: um
    sintoma novo e um item novo no registro de licoes, nao um palpite aqui.
    """
    degraus = set()
    for s in sintomas:
        if s not in SINTOMAS:
            raise KeyError(
                f"sintoma '{s}' nao esta catalogado em SINTOMAS. "
                "Acrescente a linha com a licao que o originou."
            )
        degraus.add(SINTOMAS[s])
    return tuple(sorted(degraus))


def esgotou(sintomas: list[str]) -> bool:
    """Algum sintoma vai direto ao ultimo degrau, sem passar por geracao?"""
    return ULTIMO_DEGRAU in rotear(sintomas)


@dataclass
class Resultado:
    imagem: object
    tentativas: int
    degraus: tuple[str, ...]
    composto: bool
    sintomas_finais: tuple[str, ...] = field(default=())


def executar(
    gerar: Callable[[tuple[str, ...]], object],
    conferir: Callable[[object], list[str]],
    compor: Callable[[list[str]], object],
    teto: int = TETO_PADRAO,
) -> Resultado:
    """Gera, confere, corrige, repete -- e termina sempre.

    `gerar`, `conferir` e `compor` sao INJETADOS, nao importados. E o que
    permite provar o laco sem abrir navegador: os testes passam funcoes falsas.
    `gerar` recebe os nomes das correcoes; `conferir` devolve lista de sintomas.

    A terminacao nao depende do modelo cooperar: ou a conferencia passa, ou o
    teto estoura, ou um sintoma de degrau 6 aparece -- e os tres caminhos saem.
    """
    correcoes: tuple[str, ...] = ()
    aplicados: set[str] = set()
    tentativa = 0
    sintomas: list[str] = []

    while tentativa < teto:
        imagem = gerar(correcoes)
        tentativa += 1
        sintomas = conferir(imagem)

        if not sintomas:
            return Resultado(
                imagem=imagem,
                tentativas=tentativa,
                degraus=tuple(sorted(aplicados)),
                composto=False,
            )

        degraus = rotear(sintomas)
        if ULTIMO_DEGRAU in degraus:
            break

        aplicados.update(DEGRAUS[d] for d in degraus)
        # `n-variantes` nao e correcao de prompt: ela muda quantas vezes gerar.
        correcoes = tuple(sorted(c for c in aplicados if c != DEGRAUS[5]))

    return Resultado(
        imagem=compor(sintomas),
        tentativas=tentativa,
        degraus=tuple(sorted(aplicados | {DEGRAUS[ULTIMO_DEGRAU]})),
        composto=True,
        sintomas_finais=tuple(sintomas),
    )
