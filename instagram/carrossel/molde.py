"""Constantes do molde: dimensao, area segura, cor, tipografia, orcamentos.

ESTE MODULO NAO IMPORTA NADA DO PACOTE. Ele e a base; todos os outros importam dele.

Spec: docs/superpowers/specs/2026-10-05-carrossel-motor-design.md
"""

from __future__ import annotations

# --- quadro ---------------------------------------------------------------

LARGURA = 1080
ALTURA = 1350          # 4:5 exato -> 1080/1350 = 0.8000

# Area segura da interface do Instagram, portada de jeevanbavandla: 80px de topo
# e 52px de base num design de 525px de altura, para limpar o cabecalho do perfil
# e a barra de progresso.
#
# [a conferir] Sao numeros do repo deles, NAO medidos por nos numa captura real do
# app. Ate alguem medir, valem como margem conservadora -- e a consequencia de
# estarem errados e texto atras da UI, nao peca quebrada.
SEGURO_TOPO = round(ALTURA * 80 / 525)      # 206
SEGURO_BASE = round(ALTURA * 52 / 525)      # 134

# --- identidade -----------------------------------------------------------
# Espelha instagram/remotion/src/identidade/tokens.ts. Se divergir, o tokens.ts
# manda: ele e consumido tambem pelo motor de video.

COR = {
    "terra": "#3B2A1F",
    "creme": "#F1ECE0",
    "verde": "#4A5D3A",
    "acento": "#C8661E",
    "preto": "#14100D",
}

TIPO = {
    "manchete": "'Archivo Black', Impact, sans-serif",
    "corpo": "'Inter', system-ui, Arial, sans-serif",
    "dado": "'IBM Plex Mono', ui-monospace, Menlo, monospace",
}

FONTES_GOOGLE = (
    "https://fonts.googleapis.com/css2"
    "?family=Archivo+Black&family=Inter:wght@400;600&family=IBM+Plex+Mono:wght@500"
    "&display=swap"
)

# --- fundo ----------------------------------------------------------------

FUNDOS = ("foto", "terra", "creme")

#: Quantos slides seguidos podem repetir o mesmo fundo. Acima disso o deck vira
#: aquilo que o cliente chamou de generico em 05/10/2026.
MAX_FUNDO_SEGUIDO = 2

# --- orcamento de caracteres ---------------------------------------------
# DECISAO NOSSA, nao medicao. Vem de charlesdove977, onde texto fora do orcamento
# reflui a caixa e quebra a unidade do deck. O fato e o portao `transbordo`, que
# mede o render; isto aqui e heuristica barata que recusa antes de gastar render.

ORCAMENTO = {
    "manchete": 60,
    "titulo": 42,
    "corpo": 220,
    "sub": 120,
    "item": 60,
    "passo_titulo": 34,
    "passo_texto": 90,
    "frase": 160,
    "autor": 40,
    "papel": 40,
    "numero": 8,
    "rotulo": 40,
    "nome": 30,
    "descritor": 120,
    "afirmacao": 90,
    "evidencia": 120,
    "fonte": 90,
    "badge": 18,
    "destino": 60,
    "rotulo_esq": 24,
    "rotulo_dir": 24,
}

# --- legibilidade ---------------------------------------------------------

#: Larguras em que a peca e inspecionada, de charlie947: o feed e a miniatura.
FEED_LARGURAS = (360, 320)

#: Piso de tamanho de texto NO FEED de 360px. DECISAO, nao medicao -- esta aqui
#: para ser contestada com um teste de leitura, nao citada como fato.
PISO_FEED_PX = 11.0

#: O mesmo piso convertido para o quadro de 1080: 11 * (1080/360) = 33.
PISO_QUADRO_PX = PISO_FEED_PX * LARGURA / FEED_LARGURAS[0]


def escala_feed(largura_feed: int) -> float:
    """Fator de reducao do quadro de 1080 para a largura do feed."""
    return largura_feed / LARGURA


def px_no_feed(px_no_quadro: float, largura_feed: int = FEED_LARGURAS[0]) -> float:
    """Quantos pixels um texto de `px_no_quadro` tem na largura do feed."""
    return px_no_quadro * escala_feed(largura_feed)
