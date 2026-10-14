# -*- coding: utf-8 -*-
"""Metadados (autor, data, duração, legenda) de posts do Instagram via yt-dlp, sem login e sem baixar.

Uso:  python meta_instagram.py posts.txt        (uma linha por post: r:<code> para reel, p:<code> para post)
Saída: posts.tsv ao lado (code, autor, tipo, data, dur, legenda). Pausa de 2 s entre posts.
Sem login o Instagram não entrega views. Post só de imagem dá "There is no video" (fica como erro).
Não use a API web do Instagram de dentro do navegador: dá 429 na primeira rajada.
"""
import io
import sys
import time

import yt_dlp


def main():
    ent = sys.argv[1]
    ydl = yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True, 'ignoreerrors': True})
    with io.open(ent.rsplit('.', 1)[0] + '.tsv', 'w', encoding='utf-8') as out:
        out.write('code\tautor\ttipo\tdata\tdur\tlegenda\n')
        for linha in io.open(ent, encoding='utf-8'):
            linha = linha.strip()
            if not linha or ':' not in linha:
                continue
            t, code = linha.split(':', 1)
            url = f'https://www.instagram.com/{"reel" if t == "r" else "p"}/{code}/'
            i = ydl.extract_info(url, download=False)
            if not i:
                out.write(f'{code}\t\t{t}\terro\t\t\n')
                continue
            e = next((x for x in (i.get('entries') or []) if x), i)
            leg = (i.get('description') or e.get('description') or '').replace('\t', ' ').replace('\n', ' ')[:500]
            autor = e.get('uploader') or i.get('uploader') or ''
            out.write(f"{code}\t{autor}\t{t}\t{e.get('upload_date') or i.get('upload_date')}\t"
                      f"{e.get('duration') or ''}\t{leg}\n")
            out.flush()
            time.sleep(2)


if __name__ == '__main__':
    main()
