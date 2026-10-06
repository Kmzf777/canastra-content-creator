"""Decks declarados. Peca nova e linha aqui, nunca conversa.

TODA AFIRMACAO DESTE ARQUIVO TEM FONTE, e a fonte esta no comentario ao lado. O
tipo `prova` leva isso a serio: ele EXIGE o campo `fonte`, e declaracao sem fonte
nao passa em `tipos.validar`. E a mesma ideia do `Dado.origem` de
`instagram/estaticos/catalogo.py`.

Spec: docs/superpowers/specs/2026-10-05-carrossel-motor-design.md
"""

from __future__ import annotations

from pathlib import Path

from .tipos import Deck, Slide

RAIZ = Path(__file__).resolve().parents[2]

#: As fotos ja existem e foram conferidas em 05/10/2026: cena gerada no ChatGPT a
#: partir dos packshots aprovados, com os oito campos da caixa lidos a 5x.
_F = RAIZ / "saida-teste" / "carrossel-capsulas" / "fotos"

CAPSULAS = Deck(
    slug="capsulas-qual-e-a-sua",
    slides=(
        Slide("capa", "foto", {
            "manchete": "Três cápsulas, uma fazenda. Qual é a sua?",
            "sub": "Compatíveis com o sistema Nespresso.",   # impresso na caixa
            "badge": "ARRASTE",
        }, _F / "s1.jpg"),

        Slide("produto", "foto", {
            "nome": "Clássico",
            # mercadolivre/10-textos-prontos.md -- copy dos anuncios de capsula
            "descritor": "Corpo firme, notas de chocolate e caramelo. O café de todo dia.",
        }, _F / "s2.jpg"),

        Slide("prova", "creme", {
            "afirmacao": "Especial não é adjetivo nosso.",
            "evidencia": "SCAA 80+ vem impresso na própria caixa. Não é a gente dizendo.",
            "fonte": "Arte da embalagem, lida no packshot aprovado",
        }),

        Slide("produto", "foto", {
            "nome": "Suave",
            "descritor": "Doçura alta e acidez cítrica leve. Para quem toma sem açúcar.",
        }, _F / "s3.jpg"),

        Slide("produto", "foto", {
            "nome": "Canela",
            "descritor": "Canela moída junto ao café, sem aroma artificial.",
        }, _F / "s4.jpg"),

        Slide("numero", "creme", {
            "numero": "1.250 m",
            "rotulo": "A altitude da nossa lavoura",
            # base-curada/01-real-verificada/.../IMG_1421.JPG -> GPSAltitude 1250,225
            "sub": "Gravada no GPS da câmera, em Medeiros.",
        }),

        Slide("fecho", "terra", {
            "manchete": "Na dúvida, começa pelo Clássico.",
            "sub": "Os três são 100% arábica, torrados pela mesma família desde 1985.",
            "destino": "cafecanastra.com",
        }),
    ),
    legenda="",
    destino="e-commerce proprio",
    notas={
        "ritmo": "foto,foto,creme,foto,foto,creme,terra - nunca 3 do mesmo seguidos",
        "tipos": "capa, produto, prova, numero, fecho - cinco tipos distintos",
    },
)

DECKS: list[Deck] = [CAPSULAS]


def por_slug(slug: str) -> Deck | None:
    return next((d for d in DECKS if d.slug == slug), None)
