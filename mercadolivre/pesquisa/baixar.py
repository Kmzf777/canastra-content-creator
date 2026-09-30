# -*- coding: utf-8 -*-
"""Baixa a legenda automática (pt) dos vídeos listados em videos.tsv
e grava cada uma como texto limpo em transcricoes/<id>.txt.

Só baixa o que ainda não existe — rodar de novo não repete requisição.

A legenda automática do YouTube repete cada frase em linhas consecutivas
(efeito do rolling caption). A limpeza remove carimbo de tempo, tags e a
repetição, senão o texto sai com o dobro do tamanho e cheio de eco.
"""
import io
import os
import re
import sys

import yt_dlp

AQUI = os.path.dirname(os.path.abspath(__file__))
DESTINO = os.path.join(AQUI, 'transcricoes')
os.makedirs(DESTINO, exist_ok=True)


def ler_lista():
    caminho = os.path.join(AQUI, 'videos.tsv')
    linhas = io.open(caminho, encoding='utf-8').read().splitlines()[1:]
    saida = []
    for l in linhas:
        c = l.split('\t')
        if len(c) >= 6:
            saida.append({'id': c[0], 'data': c[1], 'canal': c[4], 'titulo': c[5]})
    return saida


def limpar_vtt(bruto):
    linhas = []
    for linha in bruto.splitlines():
        linha = linha.strip()
        if (not linha or linha.startswith(('WEBVTT', 'Kind:', 'Language:', 'NOTE'))
                or '-->' in linha or re.fullmatch(r'\d+', linha)):
            continue
        linha = re.sub(r'<[^>]+>', '', linha)          # tags de timing por palavra
        linha = re.sub(r'\[[^\]]*\]', '', linha)        # [Música], [Aplausos]
        linha = re.sub(r'\s+', ' ', linha).strip()
        if linha:
            linhas.append(linha)

    # remove o eco do rolling caption: linha contida na anterior ou igual
    saida = []
    for linha in linhas:
        if saida and (linha == saida[-1] or linha in saida[-1]):
            continue
        if saida and saida[-1] in linha:
            saida[-1] = linha
            continue
        saida.append(linha)
    return ' '.join(saida)


def main():
    videos = ler_lista()
    sys.stderr.write('videos na lista: %d\n' % len(videos))
    opts = {
        'quiet': True, 'no_warnings': True, 'ignoreerrors': True,
        'skip_download': True, 'writeautomaticsub': True, 'writesubtitles': True,
        'subtitleslangs': ['pt', 'pt-BR', 'pt-orig'], 'subtitlesformat': 'vtt',
        'outtmpl': os.path.join(DESTINO, '%(id)s'),
    }
    ok = pulados = falhas = 0
    for v in videos:
        alvo = os.path.join(DESTINO, v['id'] + '.txt')
        if os.path.exists(alvo):
            pulados += 1
            continue
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download(['https://www.youtube.com/watch?v=' + v['id']])
        except Exception as e:
            sys.stderr.write('  %s falhou: %s\n' % (v['id'], str(e)[:70]))
            falhas += 1
            continue

        vtts = [f for f in os.listdir(DESTINO)
                if f.startswith(v['id']) and f.endswith('.vtt')]
        if not vtts:
            sys.stderr.write('  %s sem legenda\n' % v['id'])
            falhas += 1
            continue
        bruto = io.open(os.path.join(DESTINO, vtts[0]), encoding='utf-8',
                        errors='replace').read()
        texto = limpar_vtt(bruto)
        cabecalho = '# %s\n# canal: %s | data: %s | id: %s\n\n' % (
            v['titulo'], v['canal'], v['data'], v['id'])
        io.open(alvo, 'w', encoding='utf-8').write(cabecalho + texto)
        for f in vtts:
            os.remove(os.path.join(DESTINO, f))
        sys.stderr.write('  %s  %6d chars  %s\n' % (v['id'], len(texto), v['titulo'][:52]))
        ok += 1

    sys.stderr.write('\nbaixados=%d | ja existiam=%d | falhas=%d\n' % (ok, pulados, falhas))


if __name__ == '__main__':
    main()
