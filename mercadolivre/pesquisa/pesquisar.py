# -*- coding: utf-8 -*-
"""Busca no YouTube vídeos RECENTES e ESPECÍFICOS sobre mecânica do Mercado Livre.

Decisões que custaram tentativa, registradas para não se repetirem:

  1. Importa `yt_dlp` como MÓDULO, não por subprocesso. O `--print` sob o console
     do Windows grava barra-invertida-t literal em vez de tabulação, e em cp1252 —
     o que quebrou o primeiro parse. Como módulo, os dados vêm em dict.

  2. Usa a URL de busca do YouTube com `sp=CAISBAgFEAE=` (ordenar por data de envio
     + filtro "este ano"), NÃO o atalho `ytsearchdate:`. Esse atalho devolve
     "Unsupported url scheme" quando combinado com extract_flat nesta versão.

  3. `ytsearch:` comum ordena por RELEVÂNCIA e devolve tutorial de iniciante de
     anos atrás. Para material recente, a ordenação por data é obrigatória.

Uso:  python pesquisar.py [dias]     (padrão: 60)
Saída: videos.tsv — só o que está dentro da janela.
"""
import io
import os
import sys
import datetime as dt
import urllib.parse

import yt_dlp

AQUI = os.path.dirname(os.path.abspath(__file__))
DIAS = int(sys.argv[1]) if len(sys.argv) > 1 else 60
CORTE = (dt.date.today() - dt.timedelta(days=DIAS)).strftime('%Y%m%d')

# ordenar por data de envio + filtro "este ano"
SP = 'CAISBAgFEAE%3D'
N = 8

# Cada consulta ataca uma incerteza que hoje está apoiada só em blog.
CONSULTAS = [
    'ROAS objetivo Mercado Livre Ads',
    'ACOS Mercado Livre Ads qual usar',
    'Product Ads Mercado Livre configurar campanha',
    'Mercado Ads aprendizado campanha quantos dias',
    'tarifa Mercado Livre 2026 mudanca custo peso',
    'frete gratis Mercado Livre 79 reais quem paga',
    'custo estoque antigo Full Mercado Livre',
    'Full Mercado Livre tarifa armazenagem',
    'titulo Mercado Livre caracteres limite',
    'ficha tecnica Mercado Livre atributos ranqueamento',
    'variacao anuncio Mercado Livre',
    'anuncio classico ou premium Mercado Livre',
    'catalogo Mercado Livre buy box ganhar',
    'Mercado Livre algoritmo ranqueamento anuncio',
]


def url_busca(q):
    return ('https://www.youtube.com/results?search_query='
            + urllib.parse.quote_plus(q) + '&sp=' + SP)


def buscar_ids():
    opts = {'quiet': True, 'no_warnings': True, 'extract_flat': True,
            'ignoreerrors': True, 'skip_download': True, 'playlistend': N}
    achados = {}
    with yt_dlp.YoutubeDL(opts) as ydl:
        for q in CONSULTAS:
            sys.stderr.write('  %s\n' % q)
            try:
                r = ydl.extract_info(url_busca(q), download=False)
            except Exception as e:
                sys.stderr.write('    falhou: %s\n' % str(e)[:80])
                continue
            for e in (r or {}).get('entries') or []:
                if e and e.get('id'):
                    achados.setdefault(e['id'], q)
    return achados


def detalhar(ids):
    opts = {'quiet': True, 'no_warnings': True, 'ignoreerrors': True,
            'skip_download': True, 'extractor_args': {'youtube': {'lang': ['pt']}}}
    saida = []
    with yt_dlp.YoutubeDL(opts) as ydl:
        for i, (vid, q) in enumerate(ids.items(), 1):
            sys.stderr.write('\r  detalhando %d/%d ' % (i, len(ids)))
            sys.stderr.flush()
            try:
                info = ydl.extract_info(vid, download=False)
            except Exception:
                continue
            if not info:
                continue
            saida.append({
                'id': info.get('id', ''),
                'data': info.get('upload_date') or '',
                'dur_min': round((info.get('duration') or 0) / 60),
                'views': info.get('view_count') or 0,
                'canal': (info.get('channel') or '')[:38],
                'titulo': (info.get('title') or '')[:95],
                'consulta': q,
            })
    sys.stderr.write('\n')
    return saida


def main():
    sys.stderr.write('janela: %d dias (>= %s)\n\n' % (DIAS, CORTE))
    ids = buscar_ids()
    sys.stderr.write('\nIDs unicos: %d\n' % len(ids))

    linhas = detalhar(ids)
    dentro = [l for l in linhas if l['data'] and l['data'] >= CORTE]
    dentro.sort(key=lambda l: l['data'], reverse=True)

    cab = ['id', 'data', 'dur_min', 'views', 'canal', 'titulo', 'consulta']
    with io.open(os.path.join(AQUI, 'videos.tsv'), 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(cab) + '\n')
        for l in dentro:
            f.write('\t'.join(str(l[c]).replace('\t', ' ') for c in cab) + '\n')

    sys.stderr.write('extraidos=%d | dentro da janela=%d\n\n' % (len(linhas), len(dentro)))
    for l in dentro:
        sys.stderr.write('%s %s %3dmin %7d  %-26s %s\n' % (
            l['id'], l['data'], l['dur_min'], l['views'],
            l['canal'][:26], l['titulo'][:62]))


if __name__ == '__main__':
    main()
