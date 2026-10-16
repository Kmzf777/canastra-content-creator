# -*- coding: utf-8 -*-
"""Metadados (autor, data, duração, legenda) de posts do Instagram via yt-dlp, sem baixar.
Entrada: um shortcode por linha. Saída: <entrada>.tsv. Pausa de 2 s entre posts (rate limit)."""
import io, sys, time
import yt_dlp
ent = sys.argv[1]
ydl = yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True, 'ignoreerrors': True})
with io.open(ent.rsplit('.', 1)[0] + '.tsv', 'w', encoding='utf-8') as out:
    out.write('code\tautor\tdata\tdur\tlegenda\n')
    for code in (l.strip() for l in io.open(ent, encoding='utf-8')):
        if not code: continue
        i = ydl.extract_info(f'https://www.instagram.com/p/{code}/', download=False)
        if not i:
            out.write(f'{code}\t\terro\t\t\n'); continue
        e = next((x for x in (i.get('entries') or []) if x), i)
        leg = (i.get('description') or e.get('description') or '').replace('\t', ' ').replace('\n', ' ')[:300]
        out.write(f"{code}\t{e.get('uploader') or i.get('uploader') or ''}\t{e.get('upload_date') or i.get('upload_date')}\t{e.get('duration') or ''}\t{leg}\n")
        out.flush(); time.sleep(2)
