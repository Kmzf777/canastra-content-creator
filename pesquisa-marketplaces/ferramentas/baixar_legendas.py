# -*- coding: utf-8 -*-
"""Baixa a legenda pt (manual ou automática) de vídeos do YouTube e grava <saida>/<id>.txt em texto
corrido, com cabeçalho (título, canal, data, duração, link). Pula o que já existe.
Sem legenda: o id vai para <saida>/_sem_legenda.txt.

Uso:  python baixar_legendas.py --saida transcricoes --ids ID1 ID2 ...
      python baixar_legendas.py --saida transcricoes --arquivo ids.txt      (ids separados por espaço/linha)
      [--pausa 3]   pausa entre vídeos; sem legenda, espera 90 s e tenta mais uma vez (pode ser 429)
"""
import argparse
import glob
import io
import os
import re
import sys
import tempfile
import time

import yt_dlp


def vtt_para_texto(caminho):
    linhas, ult = [], None
    for linha in io.open(caminho, encoding='utf-8'):
        linha = linha.strip()
        if not linha or linha == 'WEBVTT' or '-->' in linha or linha.startswith(('Kind:', 'Language:', 'NOTE')):
            continue
        linha = re.sub(r'<[^>]+>', '', linha).strip()
        if linha and linha != ult:
            linhas.append(linha)
            ult = linha
    return re.sub(r'\s+', ' ', ' '.join(linhas))


def baixar(vid, saida):
    tmp = tempfile.mkdtemp()
    opts = {'quiet': True, 'skip_download': True, 'writesubtitles': True, 'writeautomaticsub': True,
            'subtitleslangs': ['pt', 'pt-BR', 'pt-orig'], 'subtitlesformat': 'vtt',
            'outtmpl': os.path.join(tmp, '%(id)s.%(ext)s'), 'ignoreerrors': True}
    info = yt_dlp.YoutubeDL(opts).extract_info('https://www.youtube.com/watch?v=' + vid, download=True)
    vtts = glob.glob(os.path.join(tmp, '*.vtt'))
    if not info or not vtts:
        return None
    texto = vtt_para_texto(sorted(vtts, key=lambda p: ('orig' not in p, p))[0])
    cab = (f"# {info.get('title')}\n- canal: {info.get('channel')}\n- data: {info.get('upload_date')}\n"
           f"- duração: {int(info.get('duration') or 0) // 60} min\n"
           f"- link: https://www.youtube.com/watch?v={vid}\n\n")
    with io.open(os.path.join(saida, vid + '.txt'), 'w', encoding='utf-8') as f:
        f.write(cab + texto + '\n')
    return len(texto.split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True)
    ap.add_argument('--ids', nargs='*', default=[])
    ap.add_argument('--arquivo')
    ap.add_argument('--pausa', type=float, default=3.0)
    a = ap.parse_args()
    ids = [x for x in a.ids if x and not x.startswith('--')]
    if a.arquivo:
        ids += [x for linha in io.open(a.arquivo, encoding='utf-8') if not linha.startswith('#') for x in linha.split()]
    os.makedirs(a.saida, exist_ok=True)
    for vid in ids:
        if os.path.exists(os.path.join(a.saida, vid + '.txt')):
            continue
        n = baixar(vid, a.saida)
        if n is None:
            time.sleep(90)
            n = baixar(vid, a.saida)
        if n is None:
            with io.open(os.path.join(a.saida, '_sem_legenda.txt'), 'a', encoding='utf-8') as f:
                f.write(vid + '\n')
            print('sem legenda', vid, file=sys.stderr)
        else:
            print('ok', vid, n, 'palavras', file=sys.stderr)
        time.sleep(a.pausa)


if __name__ == '__main__':
    main()
