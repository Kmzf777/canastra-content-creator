# -*- coding: utf-8 -*-
"""Baixa a legenda em português (manual ou automática) dos vídeos de selecionados.txt e
grava transcricoes/<id>.txt em texto corrido, com cabeçalho (título, canal, data, link).
Sem legenda: o id vai para sem_legenda.txt (transcrever com a skill watch / WhisperX).

Uso:  python baixar_legendas.py [ids...]     (sem argumento: lê selecionados.txt)
"""
import glob, io, os, re, sys, tempfile
import yt_dlp

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, 'transcricoes')

def ids():
    if len(sys.argv) > 1:
        return sys.argv[1:]
    out = []
    for l in io.open(os.path.join(AQUI, 'selecionados.txt'), encoding='utf-8'):
        if not l.startswith('#'):
            out += l.split()
    return out

def vtt_para_texto(caminho):
    linhas, ult = [], None
    for l in io.open(caminho, encoding='utf-8'):
        l = l.strip()
        if not l or l == 'WEBVTT' or '-->' in l or l.startswith(('Kind:', 'Language:', 'NOTE')):
            continue
        l = re.sub(r'<[^>]+>', '', l).strip()
        if l and l != ult:
            linhas.append(l)
            ult = l
    texto = ' '.join(linhas)
    return re.sub(r'\s+', ' ', texto)

def main():
    os.makedirs(SAIDA, exist_ok=True)
    falhas = []
    for vid in ids():
        destino = os.path.join(SAIDA, vid + '.txt')
        if os.path.exists(destino):
            continue
        tmp = tempfile.mkdtemp()
        opts = {'quiet': True, 'skip_download': True, 'writesubtitles': True, 'writeautomaticsub': True,
                'subtitleslangs': ['pt', 'pt-BR', 'pt-orig'], 'subtitlesformat': 'vtt',
                'outtmpl': os.path.join(tmp, '%(id)s.%(ext)s'), 'ignoreerrors': True}
        info = yt_dlp.YoutubeDL(opts).extract_info('https://www.youtube.com/watch?v=' + vid, download=True)
        vtts = glob.glob(os.path.join(tmp, '*.vtt'))
        if not info or not vtts:
            falhas.append(vid)
            print('sem legenda:', vid, file=sys.stderr)
            continue
        texto = vtt_para_texto(sorted(vtts, key=lambda p: ('orig' not in p, p))[0])
        cab = (f"# {info.get('title')}\n- canal: {info.get('channel')}\n- data: {info.get('upload_date')}\n"
               f"- duração: {int(info.get('duration') or 0)//60} min\n- link: https://www.youtube.com/watch?v={vid}\n\n")
        io.open(destino, 'w', encoding='utf-8').write(cab + texto + '\n')
        print('ok', vid, len(texto.split()), 'palavras', file=sys.stderr)
    if falhas:
        io.open(os.path.join(AQUI, 'sem_legenda.txt'), 'a', encoding='utf-8').write('\n'.join(falhas) + '\n')

if __name__ == '__main__':
    main()
