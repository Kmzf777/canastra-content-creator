# -*- coding: utf-8 -*-
"""Busca vídeos do YouTube por consulta, ordenados por data, e confere a data de cada um.

Uso:
  python buscar_youtube.py --consultas consultas.tsv --dias 180 --saida videos.tsv [--n 10] [--pausa 2]
      consultas.tsv: uma linha por consulta, "frente<TAB>texto da consulta" (# = comentário)
  python buscar_youtube.py --canal https://www.youtube.com/@handle --frente cases --dias 365 --saida videos.tsv
      lista os vídeos de um canal em vez de buscar

Saída (acrescenta, sem repetir id): id, data, canal, duracao_s, views, titulo, frente, consulta
Lições: yt_dlp como módulo (o --print no console Windows quebra a tabulação); URL de busca com
sp=CAISBAgFEAE= (ordem por data + este ano), não ytsearchdate:. Erro na busca: espera 90 s e segue.
"""
import argparse
import datetime as dt
import io
import os
import sys
import time
import urllib.parse

import yt_dlp


def url_busca(q):
    return ('https://www.youtube.com/results?search_query=' + urllib.parse.quote_plus(q)
            + '&sp=CAISBAgFEAE%3D')


def limpo(s):
    return str(s or '').replace('\t', ' ').replace('\n', ' ')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--consultas')
    ap.add_argument('--canal')
    ap.add_argument('--frente', default='')
    ap.add_argument('--dias', type=int, default=180)
    ap.add_argument('--saida', required=True)
    ap.add_argument('--n', type=int, default=10)
    ap.add_argument('--pausa', type=float, default=2.0)
    a = ap.parse_args()
    corte = (dt.date.today() - dt.timedelta(days=a.dias)).strftime('%Y%m%d')

    vistos = set()
    if os.path.exists(a.saida):
        for linha in io.open(a.saida, encoding='utf-8'):
            vistos.add(linha.split('\t', 1)[0])

    alvos = []
    if a.canal:
        base = a.canal.rstrip('/')
        alvos.append((a.frente, a.canal, base if base.endswith('/videos') else base + '/videos'))
    else:
        for linha in io.open(a.consultas, encoding='utf-8'):
            linha = linha.rstrip('\n')
            if not linha.strip() or linha.startswith('#') or '\t' not in linha:
                continue
            frente, q = linha.split('\t', 1)
            alvos.append((frente.strip(), q.strip(), url_busca(q.strip())))

    rasa = yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True, 'playlistend': a.n, 'ignoreerrors': True})
    cheia = yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True, 'ignoreerrors': True})
    novo = not os.path.exists(a.saida)
    with io.open(a.saida, 'a', encoding='utf-8') as out:
        if novo:
            out.write('id\tdata\tcanal\tduracao_s\tviews\ttitulo\tfrente\tconsulta\n')
        for frente, q, url in alvos:
            try:
                info = rasa.extract_info(url, download=False) or {}
            except Exception as e:  # noqa: BLE001
                print('erro na busca', q, e, file=sys.stderr)
                time.sleep(90)
                continue
            for e in (info.get('entries') or [])[:a.n]:
                if not e or not e.get('id') or e['id'] in vistos:
                    continue
                vistos.add(e['id'])
                time.sleep(a.pausa)
                i = cheia.extract_info('https://www.youtube.com/watch?v=' + e['id'], download=False)
                if not i or (i.get('upload_date') or '0') < corte:
                    continue
                out.write('\t'.join([e['id'], limpo(i.get('upload_date')), limpo(i.get('channel')),
                                     limpo(i.get('duration') or 0), limpo(i.get('view_count') or 0),
                                     limpo(i.get('title')), frente, limpo(q)]) + '\n')
                out.flush()
            time.sleep(a.pausa)


if __name__ == '__main__':
    main()
