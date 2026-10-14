# -*- coding: utf-8 -*-
"""Concorrência do 1 kg em grãos especial, separada por torra (Suave = média, Clássico = escura).

    python mercadolivre/scripts/analise_1kg_torra.py [caminho do TSV da busca]

Lê o TSV do `extrator_busca.js` (padrão: a pesquisa de 08/10/2026) e mostra, por recorte,
a distribuição do preço Pix (vitrine) e do preço cheio, quem vende volume e onde caem os
preços candidatos — com o lucro de cada um pelo `precificar.py`.
"""
import csv
import re
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from precificar import CMV, FRETE, resultado  # noqa: E402

PADRAO = Path(__file__).parent.parent / 'pesquisa' / 'concorrencia-1kg-2026-10-08.tsv'


def vendidos(v):
    v = (v or '').replace('.', '').strip()
    if not v:
        return 0
    return int(float(v.replace('mil', '').strip()) * 1000) if 'mil' in v else int(v)


def carregar(caminho):
    unicos = {}
    with open(caminho, encoding='utf8') as f:
        for r in csv.reader(f, delimiter='\t'):
            if len(r) < 9 or not r[3]:
                continue
            k = (r[2].strip().lower(), r[3])
            if k in unicos:
                continue
            pix = float(r[3])
            cheio = float(r[5] or r[4] or 0) or pix
            unicos[k] = dict(t=r[2], pix=pix, cheio=max(cheio, pix), v=vendidos(r[6]),
                             nota=r[7], tags=r[8])
    return list(unicos.values())


def classificar(x):
    t = x['t'].lower()
    um_kg = bool(re.search(r'\b1 ?k(g|ilo)|1000 ?g', t)) and not re.search(
        r'kit|\b\d+ ?(un|x|pacotes|pct)\b|2 ?kg|5 ?kg|com \d', t)
    grao = bool(re.search(r'gr[ãa]o', t)) and not re.search(r'mo[íi]do', t)
    especial = bool(re.search(r'especial|\b8\d ?(\+|pts|pontos)|sca', t))
    robusta = bool(re.search(r'robusta|conilon|blend|vending', t))
    if not (um_kg and grao and especial and not robusta):
        return None
    if re.search(r'escur|intens|forte|extra ?forte', t):
        return 'escura'
    if re.search(r'm[ée]di|suave|clara|equilibr', t):
        return 'media'
    return 'sem torra no título'


def q(ps, f):
    return ps[min(len(ps) - 1, int(f * len(ps)))]


def resumo(nome, sel, campo='pix'):
    ps = sorted(x[campo] for x in sel)
    print('\n### %s — n=%d (%s)' % (nome, len(ps), 'vitrine Pix' if campo == 'pix' else 'preço cheio'))
    if not ps:
        return
    print('  p25 %.2f · mediana %.2f · p75 %.2f · min %.2f · max %.2f' % (
        q(ps, .25), st.median(ps), q(ps, .75), ps[0], ps[-1]))


def lideres(sel, n=10):
    for x in sorted(sel, key=lambda x: (-x['v'], x['pix']))[:n]:
        print('  pix %7.2f  cheio %7.2f  +%-6d %-4s %-14s %s' % (
            x['pix'], x['cheio'], x['v'], x['nota'], x['tags'][:14], x['t'][:70]))


def posicao(preco, sel, campo):
    ps = sorted(x[campo] for x in sel)
    return 100 * sum(p < preco for p in ps) / len(ps) if ps else 0


def main(caminho=PADRAO):
    L = carregar(caminho)
    grupos = {}
    for x in L:
        g = classificar(x)
        if g:
            grupos.setdefault(g, []).append(x)
    todos = [x for g in grupos.values() for x in g]
    for nome, sel in (('ESPECIAL 1 kg grãos — todos', todos),
                      ('Torra MÉDIA (vizinho do Suave)', grupos.get('media', [])),
                      ('Torra ESCURA (vizinho do Clássico)', grupos.get('escura', [])),
                      ('Sem torra no título', grupos.get('sem torra no título', []))):
        resumo(nome, sel, 'pix')
        resumo(nome, sel, 'cheio')
        lideres(sel, 8)

    print('\n### Preços candidatos (Clássico, frete 34,30, CMV 47) — onde caem no mercado')
    print('  %8s %8s %7s %7s  %s' % ('cheio', 'pix(-9%)', 'lucro', 'margem', 'percentil cheio/pix'))
    for p in (109.90, 114.90, 119.90, 124.90, 129.90, 134.90):
        r = resultado(p, CMV['1kg'], FRETE['1kg'])
        print('  %8.2f %8.2f %7.2f %6.1f%%  %3.0f%% / %3.0f%%' % (
            p, p * 0.91, r['lucro'], r['margem'],
            posicao(p, todos, 'cheio'), posicao(p * 0.91, todos, 'pix')))


if __name__ == '__main__':
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else PADRAO)
