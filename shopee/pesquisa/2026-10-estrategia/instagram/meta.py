# -*- coding: utf-8 -*-
"""Metadados (data, duração, views, legenda) dos posts de um perfil do Instagram via yt-dlp, sem baixar.
Entrada: arquivo com linhas r:<code> ou p:<code>. Saída: <arquivo>.tsv. Pausa entre posts (rate limit)."""
import io, sys, time
import yt_dlp
ent = sys.argv[1]
ydl = yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True, 'ignoreerrors': True, 'noplaylist': False})
with io.open(ent.rsplit('.', 1)[0] + '.tsv', 'w', encoding='utf-8') as out:
    out.write('code\ttipo\tdata\tdur\tviews\tlikes\tlegenda\n')
    for l in io.open(ent, encoding='utf-8'):
        l = l.strip()
        if not l: continue
        t, code = l.split(':', 1)
        url = f'https://www.instagram.com/{"reel" if t == "r" else "p"}/{code}/'
        i = ydl.extract_info(url, download=False)
        if not i:
            out.write(f'{code}\t{t}\terro\t\t\t\t\n'); continue
        e = next((x for x in (i.get('entries') or []) if x), i)
        leg = (i.get('description') or e.get('description') or '').replace('\t', ' ').replace('\n', ' ')[:400]
        out.write(f"{code}\t{t}\t{e.get('upload_date') or i.get('upload_date')}\t{e.get('duration') or ''}\t{e.get('view_count') or ''}\t{e.get('like_count') or i.get('like_count') or ''}\t{leg}\n")
        out.flush(); time.sleep(2)
