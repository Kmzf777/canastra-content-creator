"""Declaracao -> texto do prompt de geracao.

O prompt e em INGLES por decisao do CLAUDE.md: corpo de prompt de imagem em
ingles, porque os modelos respondem melhor.

O QUE ESTE MODULO NAO FAZ: nao escreve `dados`. `R$ 31,70` e `1.250 m` sao
desenhados pelo Remotion. Pedir ao modelo para escrever texto nosso e a licao 1
-- descrever e deixar o modelo desenhar produz um sosia.

As correcoes sao os degraus 1 a 4 da escada. O degrau 5 (`n-variantes`) nao
muda o prompt, muda quantas vezes ele roda; o degrau 6 (`compor`) nao gera.
"""

from __future__ import annotations

from .catalogo import Peca

CORRECOES: tuple[str, ...] = (
    "soletrar",
    "nomear-operacao",
    "ancora-familia",
    "aumentar-no-quadro",
)

_ABERTURA_EDICAO = (
    "EDIT THE PROVIDED PHOTOGRAPH. KEEP THE PACKAGE PIXEL-FOR-PIXEL IDENTICAL: "
    "same position, same scale, same crop, same creases, same specular highlights. "
    "Change only the surrounding scene."
)


def _soletrar(s: str) -> str:
    """`SCA 80+` -> `"SCA 80+" (S-C-A-space-8-0-plus)`.

    Soletra so letra e digito; pontuacao fica por extenso em ingles porque e
    assim que o `lateral_extra` de prompts_catalogo.py faz, e aquele formato ja
    corrigiu o `70 / 80 / 80 / 40` na pratica.
    """
    nomes = {" ": "space", "+": "plus", ",": "comma", ".": "dot", "-": "dash"}
    partes = [nomes.get(c, c) for c in s]
    return f'"{s}" ({"-".join(partes)})'


def montar(peca: Peca, correcoes: tuple[str, ...] = ()) -> str:
    for c in correcoes:
        if c not in CORRECOES:
            raise ValueError(
                f"correcao '{c}' nao existe. Validas: {', '.join(CORRECOES)}"
            )

    blocos: list[str] = []

    if "nomear-operacao" in correcoes:
        blocos.append(_ABERTURA_EDICAO)
    else:
        blocos.append(
            "Photograph of the provided coffee package in a new setting. "
            "The package artwork must be reproduced exactly as in the reference."
        )

    ocupacao = "at least 60%" if "aumentar-no-quadro" in correcoes else "about 45%"
    blocos.append(f"The package occupies {ocupacao} of the frame height.")

    if "soletrar" in correcoes:
        itens = "; ".join(_soletrar(s) for s in peca.strings_impressas)
        blocos.append(
            "The front panel carries exactly these strings, character for "
            f"character, with every accent: {itens}."
        )
    else:
        itens = "; ".join(f'"{s}"' for s in peca.strings_impressas)
        blocos.append(f"The front panel carries exactly these strings: {itens}.")

    if "ancora-familia" in correcoes:
        blocos.append(
            "Two reference images are provided. The FIRST defines the artwork and "
            "every printed string. The SECOND defines only material, lighting and "
            "pose. Where they disagree about text, the first wins."
        )

    blocos.append(
        "Phone-camera look: small sensor, deep focus, everything equally sharp, "
        "soft corners, washed saturation. No shallow depth of field, no bokeh."
    )
    blocos.append(
        "Do NOT render any batch code, manufacturing date, expiry date, QR code "
        "or barcode. Leave those out of frame."
    )

    return " ".join(blocos)
