# Pesquisa de estratégia do ML — outubro de 2026

Material bruto do [`../../16-estrategia-competir.md`](../../16-estrategia-competir.md).
Coletado em 14/10/2026.

| Pasta / arquivo | O que é |
|---|---|
| `videos.tsv` | Busca do YouTube, últimos 90 dias, 24 consultas (sai com lixo: dramas asiáticos com views altas) |
| `selecionados.txt` | Os 63 vídeos escolhidos, por tema (o bloco do Hugo não tem corte de data) |
| `transcricoes/<id>.txt` | Legenda em português, texto corrido, com título, canal, data e link no cabeçalho |
| `notas/BRIEF.md` | Brief comum dos subagentes que resumiram as transcrições |
| `notas/*.md` | Um resumo por tema: por vídeo, consolidado, aplicação à Canastra, perguntas abertas |
| `tiktok/hugo-*.md` | TikToks do @hugovasc_ (skill `watch`; vários deram 403) |
| `instagram/hugo-posts.tsv` | Metadados dos 88 posts do @hugovasc_ visíveis (11/09–14/10) |
| `instagram/busca-posts.tsv` | Metadados da busca por palavra-chave do Instagram |
| `instagram/{hugo,busca}-<code>.md` | Transcrições dos reels (skill `watch`, WhisperX local) |

## Reproduzir

```bash
cd mercadolivre/pesquisa/2026-10-estrategia
python buscar_youtube.py 90        # videos.tsv
python baixar_legendas.py          # transcricoes/ a partir de selecionados.txt (pula o que existe)
python instagram/meta.py instagram/hugo-posts.txt   # metadados; entrada com linhas r:<code> ou p:<code>
```

Reels: `python <skill watch>/scripts/watch.py https://www.instagram.com/reel/<code>/ --detail transcript`.

## Armadilhas

- `python -I` esconde o `yt_dlp` instalado no site-packages do usuário: rode sem `-I`.
- Duas baixas de legenda em paralelo dão 429 no YouTube; rode uma por vez.
- A API web do Instagram (`/api/v1/feed/user/`) deu 429 na primeira chamada; a grade do
  perfil só carrega rolando com o `computer scroll` do Claude in Chrome (JS `scrollTo` não
  dispara com a janela oculta). O `yt-dlp` lê reel do Instagram sem login, mas sem views.
- TikTok: o `yt-dlp` lista o perfil, mas passa a dar 403 depois de algumas chamadas.
- Mercado Livre: em 14/10 as páginas de produto abriram **captcha** — não resolver;
  pedir ao Rafael.
- Legenda automática erra nomes e números ("R2,50"): número que importa vai conferido no
  contexto ou marcado como duvidoso nas notas.
