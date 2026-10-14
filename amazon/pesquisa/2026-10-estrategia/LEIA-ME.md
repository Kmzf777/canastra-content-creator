# Pesquisa de estratégia — Amazon Brasil (14/10/2026)

Mesmo método da pesquisa de Mercado Livre (`../../../mercadolivre/pesquisa/2026-10-estrategia/`).

| Pasta / arquivo | O quê |
|---|---|
| `buscar_youtube.py` | busca no YouTube dos últimos N dias (28 consultas de Amazon) → `videos.tsv` |
| `canais.txt` | uploads recentes dos canais-chave (oficial "Venda com a Amazon Brasil", Seller Pro, Caio Andrade, Egton, Jess, Brener) |
| `selecionados.txt` | os 56 vídeos escolhidos, por tema |
| `baixar_legendas.py` | legenda pt (ou `LEG_LANGS=en,en-orig`) → `transcricoes/<id>.txt` |
| `notas/BRIEF.md` | brief comum dos subagentes que destilaram as transcrições |
| `notas/*.md` | FBA · DBA e envio próprio · custos e precificação · Ads · marca, listagem e promoções · estratégia e cases · começar, escalar e alimentos |
| `instagram/` | busca por palavra-chave (62 posts), metadados (`meta.py`) e reels transcritos com a skill `watch` |

Reproduzir:

```bash
cd amazon/pesquisa/2026-10-estrategia
python buscar_youtube.py 90
python baixar_legendas.py            # lê selecionados.txt; pula o que já existe
python instagram/meta.py instagram/busca-posts.txt
```

Limites: o TikTok bloqueou a listagem de perfis via yt-dlp e não renderiza com a janela do Chrome
oculta; o Instagram de Amazon Brasil é raso. A busca de café na Amazon (528 linhas) ficou só no
`localStorage` do Chrome — o resumo está em `../../01-estrategia-amazon.md` §1.
