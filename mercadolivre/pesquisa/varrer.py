# -*- coding: utf-8 -*-
"""Varre as transcrições atrás de afirmações concretas sobre a mecânica do ML.

Cada tema corresponde a uma afirmação que hoje está apoiada só em blog. O objetivo
é achar a frase dita em vídeo recente, com o nome do canal e a data, para poder
confirmar ou derrubar o que está escrito em docs/ML-CAPSULAS-ESTRATEGIA.md.

Uso: python varrer.py [tema]     (sem argumento: lista os temas)
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(AQUI, 'transcricoes')
JANELA = 220  # caracteres de contexto de cada lado

TEMAS = {
    'titulo':    r'\b(?:t[íi]tulo|caracter)\w*\b',
    'premium':   r'\b(?:cl[áa]ssico|premium)\b',
    'roas':      r'\bROAS\b',
    'acos':      r'\b(?:ACOS|TACOS)\b',
    'aprendiz':  r'aprendizad|curva de aprend|\bdias\b.{0,40}campanha|campanha.{0,40}\bdias\b',
    'frete79':   r'\b79\b|frete gr[áa]tis',
    'tarifa':    r'tarifa|comiss[ãa]o|custo fixo|\b1[0-9],?\d?\s?%',
    'full':      r'\bfull\b|armazenag|estoque antigo',
    'variacao':  r'varia[çc][õaã]',
    'catalogo':  r'cat[áa]logo|buy ?box',
    'ficha':     r'ficha t[ée]cnica|atributo',
    'palavra':   r'palavra[- ]chave|keyword',
}


def carregar():
    docs = []
    for f in sorted(os.listdir(DIR)):
        if not f.endswith('.txt'):
            continue
        txt = io.open(os.path.join(DIR, f), encoding='utf-8').read()
        linhas = txt.split('\n')
        titulo = linhas[0].lstrip('# ').strip()
        meta = linhas[1].lstrip('# ').strip() if len(linhas) > 1 else ''
        corpo = '\n'.join(linhas[2:])
        data = re.search(r'data:\s*(\d{8})', meta)
        canal = re.search(r'canal:\s*([^|]+)', meta)
        docs.append({
            'arq': f[:-4], 'titulo': titulo, 'corpo': corpo,
            'data': data.group(1) if data else '?',
            'canal': (canal.group(1).strip() if canal else '?'),
        })
    return docs


def main():
    docs = carregar()
    if len(sys.argv) < 2:
        print('transcricoes: %d' % len(docs))
        for d in sorted(docs, key=lambda x: x['data'], reverse=True):
            print('  %s  %s  %-26s %s' % (d['data'], d['arq'], d['canal'][:26], d['titulo'][:58]))
        print('\ntemas: ' + ' '.join(TEMAS))
        return

    tema = sys.argv[1]
    padrao = TEMAS.get(tema, tema)
    rx = re.compile(padrao, re.I)
    total = 0
    for d in sorted(docs, key=lambda x: x['data'], reverse=True):
        achados, vistos = [], set()
        for m in rx.finditer(d['corpo']):
            ini = max(0, m.start() - JANELA)
            trecho = re.sub(r'\s+', ' ', d['corpo'][ini:m.end() + JANELA]).strip()
            chave = trecho[:70]
            if chave in vistos:
                continue
            vistos.add(chave)
            achados.append(trecho)
        if not achados:
            continue
        print('\n=== %s | %s | %s ===' % (d['data'], d['canal'][:30], d['titulo'][:62]))
        for a in achados[:6]:
            print('  ... %s ...' % a)
            total += 1
    print('\ntrechos: %d' % total)


if __name__ == '__main__':
    main()
