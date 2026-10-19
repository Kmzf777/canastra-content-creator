# -*- coding: utf-8 -*-
"""Os 20 produtos da planilha da Loja Integrada.

Uma linha por produto. `tray` é o SKU numérico da loja Tray, de onde vêm nome,
preço e descrição. `gerado` é a pasta em saida-teste/catalogo-estudio. `real` é a
pasta em "fotos produtos cru" (shoot de 11/09/2026) — a fonte da verdade do
rótulo. `ean` só está preenchido onde o código foi lido no verso real.
"""

EM_GRAOS = ("Cafés Especiais", "Em Grãos")
MOIDO = ("Cafés Especiais", "Moídos para Coador")
CAPSULA = ("Cafés Especiais", "Cápsulas")
DRIP = ("Cafés Especiais", "Drip Coffee")

# peso de postagem em kg e caixa em cm (altura, largura, comprimento).
# ESTIMADO, menos o 1 kg: 1,128 kg / 27x29x11 veio da pesagem do Mercado Livre.
FORMATO = {
    "250g":    (0.28, 20, 13, 6),
    "500g":    (0.54, 25, 16, 7),
    "1kg":     (1.128, 27, 29, 11),
    "capsula": (0.12, 10, 9, 5),
    "drip":    (0.22, 15, 12, 6),
}

PRODUTOS = [
    # sku interno, tray, gerado, real, categoria, formato, ean
    ("CAN-CLA-GR-250",  "51",  "7-classico-250g-graos",   "Canastra-Classico-250g-Graos",      EM_GRAOS, "250g",    ""),
    ("CAN-CLA-MO-250",  "71",  "6-classico-250g-moido",   "Canastra-Classico-250g-Moido",      MOIDO,    "250g",    ""),
    ("CAN-CLA-GR-500",  "53",  "9-classico-500g-graos",   "Canastra-Classico-500g-Graos",      EM_GRAOS, "500g",    "7892262780089"),
    ("CAN-CLA-MO-500",  "69",  "8-classico-500g-moido",   "Canastra-Classico-500g-Moido",      MOIDO,    "500g",    "7892262780089"),
    ("CAN-CLA-GR-1000", "47",  "10-classico-1kg-graos",   "Canastra-Classico-1kg-Graos",       EM_GRAOS, "1kg",     "7892262780225"),
    ("CAN-SUA-GR-250",  "49",  "2-suave-250g-graos",      "Canastra-Suave-250g-Graos",         EM_GRAOS, "250g",    ""),
    ("CAN-SUA-MO-250",  "57",  "1-suave-250g-moido",      "Canastra-Suave-250g-Moido",         MOIDO,    "250g",    ""),
    ("CAN-SUA-GR-500",  "55",  "4-suave-500g-graos",      "Canastra-Suave-500g-Graos",         EM_GRAOS, "500g",    "7892262780065"),
    ("CAN-SUA-MO-500",  "65",  "3-suave-500g-moido",      "Canastra-Suave-500g-Moido",         MOIDO,    "500g",    "7892262780027"),
    ("CAN-SUA-GR-1000", "61",  "5-suave-1kg-graos",       "Canastra-Suave-1kg-Graos",          EM_GRAOS, "1kg",     "7892262780034"),
    ("CAN-CAN-MO-250",  "1",   "11-canela-250g-moido",    "Canastra-Canela-250g-Moido",        MOIDO,    "250g",    ""),
    ("CAN-MIC-GR-250",  "87",  "12-microlote-250g-graos", "Microlote-250g-Graos",              EM_GRAOS, "250g",    "7892262780140"),
    ("CAN-MIC-MO-250",  "89",  "13-microlote-250g-moido", "Microlote-250g-Moido",              MOIDO,    "250g",    "7892262780140"),
    ("NEC-GOU-GR-1000", "59",  "14-nectar-1kg-graos",     "Nectar-de-Minas-Gourmet-1kg-Graos", EM_GRAOS, "1kg",     "7892262780157"),
    ("NEC-GOU-MO-500",  "67",  "15-nectar-500g-moido",    "Nectar-de-Minas-Gourmet-500g-Moido",MOIDO,    "500g",    "7892262780164"),
    ("CAN-CAP-CLA-10",  "73",  "16-capsulas-classico",    "Capsulas-Classico-10un-5g",         CAPSULA,  "capsula", "7892262780096"),
    ("CAN-CAP-CAN-10",  "79",  "17-capsulas-canela",      "Capsulas-Canela-10un-5g",           CAPSULA,  "capsula", "7892262780102"),
    ("CAN-CAP-SUA-10",  "81",  "21-capsulas-suave",       "Capsulas-Suave-10un-5g",            CAPSULA,  "capsula", ""),
    ("CAN-DRI-CLA-10",  "113", "18-drip-classico",        "Drip-Coffee-Classico-100g",         DRIP,     "drip",    "7892262780188"),
    ("CAN-DRI-SUA-10",  "77",  "19-drip-suave",           "Drip-Coffee-Suave-100g",            DRIP,     "drip",    "7892262780195"),
]

assert len(PRODUTOS) == 20
assert len({p[0] for p in PRODUTOS}) == 20
assert len({p[1] for p in PRODUTOS}) == 20
