# -*- coding: utf-8 -*-
"""Busca no YouTube vídeos de Shopee dos últimos N dias (padrão 90) para a pesquisa
de estratégia de 10/2026. Mesma técnica de mercadolivre/pesquisa/pesquisar.py (yt_dlp como módulo, URL de busca
ordenada por data); aqui a data de cada vídeo é conferida um a um, porque a busca rasa não
traz `upload_date`.

Uso:  python buscar_youtube.py [dias]      Saída: videos.tsv (id, data, canal, duração, views, título, consulta)
"""
import datetime as dt, io, os, sys, urllib.parse
import yt_dlp

AQUI = os.path.dirname(os.path.abspath(__file__))
DIAS = int(sys.argv[1]) if len(sys.argv) > 1 else 90
CORTE = (dt.date.today() - dt.timedelta(days=DIAS)).strftime('%Y%m%d')
SP = 'CAISBAgFEAE%3D'   # ordenar por data + este ano
N = 10
CONSULTAS = [
    'shopee frete grátis vendedor paga quanto', 'shopee comissão 20% taxa fixa por item', 'shopee programa frete grátis extra vale a pena',
    'shopee desconto progressivo combo leve mais', 'shopee cupom da loja seguidores', 'shopee mall requisitos loja oficial',
    'shopee vender alimentos validade anvisa', 'shopee vendedor indicado como conseguir', 'shopee ads gmv max',
    'shopee ads busca descoberta lance', 'shopee campanha 11.11 vendedor preparar', 'shopee preço mínimo campanha inscrição',
    'shopee taxa de envio coleta vendedor', 'shopee full vale a pena', 'shopee fábrica marca própria vender',
    'shopee reputação atraso envio penalidade', 'shopee vídeo vendedor vender mais', 'shopee live vendedor estratégia',
]

def busca(q):
    return 'https://www.youtube.com/results?search_query=' + urllib.parse.quote_plus(q) + '&sp=' + SP

def main():
    rasa = yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True, 'playlistend': N, 'ignoreerrors': True})
    vistos = {}
    for q in CONSULTAS:
        info = rasa.extract_info(busca(q), download=False) or {}
        for e in (info.get('entries') or [])[:N]:
            if e and e.get('id') and e['id'] not in vistos:
                vistos[e['id']] = q
    print(f'{len(vistos)} candidatos', file=sys.stderr)
    cheia = yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True, 'ignoreerrors': True})
    linhas = []
    for vid, q in vistos.items():
        i = cheia.extract_info('https://www.youtube.com/watch?v=' + vid, download=False)
        if not i or (i.get('upload_date') or '0') < CORTE:
            continue
        titulo = (i.get('title') or '').replace('\t', ' ')
        linhas.append((vid, i['upload_date'], (i.get('channel') or '').replace('\t', ' '), str(i.get('duration') or 0),
                       str(i.get('view_count') or 0), titulo, q))
    linhas.sort(key=lambda l: -int(l[4]))
    with io.open(os.path.join(AQUI, 'videos-2.tsv'), 'w', encoding='utf-8') as f:
        f.write('id\tdata\tcanal\tduracao_s\tviews\ttitulo\tconsulta\n')
        for l in linhas:
            f.write('\t'.join(l) + '\n')
    print(f'{len(linhas)} dentro de {DIAS} dias', file=sys.stderr)

if __name__ == '__main__':
    main()
