"""Declaracao das pecas estaticas. Dado sem origem nao entra.

POR QUE ISTO E DADO E NAO PROSA. Dos itens do `Registro de licoes` do
CLAUDE.md, ao menos quatro -- 13, 18, 21 e 22 -- sao a mesma falha: um valor
que ninguem declarou, logo ninguem conferiu. `Doodo 1985`, `70/80/80/40`,
`ARABICA` sem acento, `F:23.2025`.

`strings_impressas` existe para ser consumida por TRES lugares a partir desta
mesma fonte: o bloco de soletracao do prompt, o checklist da conferencia e as
assercoes do laudo. Se a lista fosse memoria do agente, ele voltaria a montar
na hora -- e foi assim que um campo fisicamente ilegivel virou "confere".
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Dado:
    """Um valor que o CODIGO desenha na peca.

    `origem` nao tem default de proposito: e um campo obrigatorio para forcar
    a resposta "de onde veio este numero" na hora de declarar, nao na hora de
    conferir. Ver licao 18.
    """

    valor: str
    origem: str


@dataclass(frozen=True)
class Molde:
    """Um layout. `campos` sao as chaves que `Peca.dados` DEVE ter, exatamente."""

    nome: str
    campos: tuple[str, ...]
    largura: int
    altura: int


@dataclass(frozen=True)
class Peca:
    slug: str
    molde: str
    fonte: Path
    strings_impressas: tuple[str, ...]
    dados: dict[str, Dado]
    gerar_fundo: bool


MOLDES: dict[str, Molde] = {
    "cartao-produto": Molde(
        "cartao-produto", ("preco", "altitude", "local"), 1080, 1350
    ),
    # `carta-sensorial` entra AQUI quando as notas forem confirmadas com o
    # Arthur -- ver o bloqueio 10.1 da spec. Nao precisa de codigo novo.
}

# A fonte e o packshot de estudio JA APROVADO, nao a foto crua: ele e a ancora
# de que `canastra-embalagem` fala, e poupa uma rodada de conferencia.
_FONTE_CLASSICO = (
    RAIZ
    / "saida-teste"
    / "catalogo-estudio"
    / "7-classico-250g-graos"
    / "7.1-frente-branco.png"
)

PECAS: list[Peca] = [
    Peca(
        slug="cartao-classico-250g-graos",
        molde="cartao-produto",
        fonte=_FONTE_CLASSICO,
        # CONFERIDAS POR AMPLIACAO em 30/09/2026, recorte a recorte sobre
        # `7.1-frente-branco.png` -- nao transcritas de memoria. O selo circular
        # a 7x, a caixa central a 3x, o logotipo a 3x.
        #
        # A primeira versao desta lista trazia "CLÁSSICO" e "TORRADO EM GRÃOS",
        # e as duas estavam ERRADAS: o selo diz "CLÁSSICO EM GRÃOS" no arco de
        # cima e "TORRA EXCLUSIVA" no de baixo. Foram declaradas sem ampliar.
        # E a licao 18 cometida dentro do modulo escrito para impedi-la -- por
        # isso o comentario fica: gabarito nao conferido no pixel nao e gabarito.
        #
        # `SCA 80+` e do saco; a capsula traz `SCAA 80+`. E exatamente o tipo de
        # diferenca que `prompts_catalogo.py` existe para nao perder numa
        # copia-e-cola.
        #
        # `Desde 1985` entra de proposito mesmo sendo manuscrito pequeno: e a
        # string da licao 13, que ja saiu `Doodo 1985`. O gabarito tem que
        # cobrir justamente o que costuma quebrar.
        strings_impressas=(
            "Café",
            "CANASTRA",
            "Desde 1985",
            "SPECIALTY",
            "ESPECIAL",
            "SCA 80+",
            "CLÁSSICO EM GRÃOS",
            "TORRA EXCLUSIVA",
            "250g",
        ),
        dados={
            "preco": Dado(
                "R$ 31,70",
                "fotos produtos cru/_LEIA-ME.md, de tabela.cafecanastra.com em 11/09/2026",
            ),
            "altitude": Dado(
                "1.250 m",
                "EXIF GPS de base-curada/01-real-verificada/fazenda-medeiros-1250m/",
            ),
            "local": Dado(
                "Medeiros, MG",
                "EXIF GPS de base-curada/01-real-verificada/fazenda-medeiros-1250m/",
            ),
        },
        gerar_fundo=True,
    ),
]


class DeclaracaoInvalida(Exception):
    """A declaracao nao passa. Levantada por `exigir_valido`, nao por `validar`."""


def validar(pecas: list[Peca]) -> list[str]:
    """Devolve a lista de problemas. Lista vazia significa declaracao valida.

    Devolve em vez de levantar porque o comando `conferir` precisa reportar
    TODOS os problemas de uma vez -- um por linha -- e nao parar no primeiro.
    """
    problemas: list[str] = []
    for p in pecas:
        onde = f"peca {p.slug}"

        molde = MOLDES.get(p.molde)
        if molde is None:
            problemas.append(f"{onde}: molde '{p.molde}' nao existe em MOLDES")
            continue

        if not p.strings_impressas:
            problemas.append(
                f"{onde}: strings_impressas vazia -- sem gabarito nao ha conferencia"
            )

        if not p.fonte.exists():
            problemas.append(f"{onde}: fonte nao existe no disco: {p.fonte}")

        esperados = set(molde.campos)
        declarados = set(p.dados)
        for falta in sorted(esperados - declarados):
            problemas.append(f"{onde}: o molde pede o campo '{falta}' e ele nao foi declarado")
        for sobra in sorted(declarados - esperados):
            problemas.append(f"{onde}: campo '{sobra}' nao pertence ao molde '{p.molde}'")

        for chave in sorted(declarados & esperados):
            d = p.dados[chave]
            if not d.valor.strip():
                problemas.append(f"{onde}: campo '{chave}' com valor vazio")
            if not d.origem.strip():
                problemas.append(
                    f"{onde}: campo '{chave}' sem origem declarada -- ver licao 18"
                )
    return problemas


def exigir_valido(pecas: list[Peca]) -> None:
    problemas = validar(pecas)
    if problemas:
        raise DeclaracaoInvalida("\n".join(problemas))
