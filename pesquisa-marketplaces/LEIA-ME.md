# Pesquisa de marketplaces — Mercado Livre, Shopee e Amazon (outubro/2026)

> Acervo **neutro** sobre como os melhores operam cada plataforma, para depois traçar
> estratégias (Ads, preço, volume, estoque, mix) e treinar agentes. Não parte da situação de
> nenhuma empresa. Spec: `docs/superpowers/specs/2026-10-14-pesquisa-marketplaces-design.md`.
> Feita em 14–15/10/2026 por um workflow de 61 agentes (≈ 4 h).
>
> **Substitui** a rodada v1 (`mercadolivre/16-estrategia-competir.md`, `shopee/`, `amazon/`),
> que partiu do estado da conta da Canastra e ficou enviesada.

## Mercado Livre: versão final (15/10/2026)

- `mercadolivre/CONSOLIDADO.md` reescrito como mapa final; cada nota ganhou a **§12 Rodada 2 e estado final** (status final de cada afirmação, reconciliações, perguntas do protocolo R/P/S).
- `mercadolivre/rodada2/`: regulatório (Anvisa, IN 281, Portaria 570, INPI), balanços e API, webinars oficiais com minuto, camada de dados, evidência causal e cases, sinais recentes, e três leituras no Claude in Chrome (Full/Supermercado, tarifas/promoções/reputação, observação orgânico × patrocinado com prints).
- `verificacao/resultado-mercadolivre.tsv`: as 46 afirmações reverificadas no navegador (27 confirmadas, 16 parciais, 1 contestada, 2 sem fonte).
- `LACUNAS.md` §1: 83 itens — 32 fechados, 25 parciais, 26 abertos; os abertos dependem de painel logado de vendedor, de medição própria ou de dado que o ML não publica.

## Por onde começar

1. `<plataforma>/CONSOLIDADO.md` — o mapa da plataforma (regras, o que decide quem vende, por
   frente, benchmarks, divergências, indústria × revenda, alimentos/café, perguntas abertas).
2. `<plataforma>/<frente>/notas.md` — a nota de cada frente, com tabela de afirmações e, no fim,
   a seção **10. Verificação** (confirmada / contestada / sem fonte oficial).
3. `LACUNAS.md` — o que ficou sem resposta e a próxima rodada, priorizada.
4. `metodo/` — como agências, consultorias e ferramentas pesquisam marketplace
   (`estado-da-arte.md`) e o protocolo usado aqui (`protocolo.md`).

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `<plataforma>/{ads, preco-promocao, logistica-estoque, ranqueamento-anuncio, produto-mix, reputacao-atendimento, alimentos-marca-propria, cases-grandes}/notas.md` | 24 notas, 7–9 mil palavras cada |
| `<plataforma>/transcricoes/` | legendas do YouTube (ML 87, Shopee 96, Amazon 76) |
| `<plataforma>/consultas.tsv`, `videos.tsv`, `selecionados.tsv` | consultas por frente, resultado da busca, escolhidos |
| `<plataforma>/social/` | reels do Instagram e TikToks (`posts.tsv`, `tiktok.txt`), transcrições (`transcricoes/`) e `notas.md` |
| `<plataforma>/observacao/` | páginas de líderes abertas no navegador (`lideres.tsv`, `lideres.md`) |
| `ferramentas/` | `buscar_youtube.py`, `baixar_legendas.py`, `meta_instagram.py` |

Tipos de afirmação em todas as notas: **[OFICIAL]** regra da plataforma · **[PRÁTICA]** tática de
praticante · **[CASE]** números de uma operação · **[DADO]** estudo/relatório · **[OBS]** observação.

## Números da rodada

- Fontes declaradas pelos 24 analistas: 439 oficiais, 373 de praticantes, 127 de dados; 509
  transcrições lidas.
- Verificação adversarial das afirmações de regra/número (288): **111 confirmadas, 13
  contestadas, 164 sem fonte oficial lida**. As "sem fonte" são, na maioria, falha de acesso, não
  afirmação falsa: a cota de busca na web acabou no meio da rodada e as páginas oficiais da Shopee
  (Central do Vendedor, Shopee Uni, help) e várias do ML só renderizam com JavaScript ou login.

## Limites conhecidos

- **Shopee**: a observação de líderes parou depois da primeira busca (a Shopee exige login para
  produto e nova busca); `observacao/lideres.tsv` tem 10 linhas de uma busca só.
- **ML**: o selo FULL só foi lido nos cards da busca; "Patrocinado" não foi capturado.
- **Instagram** sem login não dá views; a seleção de reels foi por tema e autor. Vários reels
  curtos saíram sem fala ("no speech").
- TikTok tem vídeos de 2023–2024 (ano anotado).

## Como reproduzir

```bash
cd pesquisa-marketplaces/<plataforma>
python ../ferramentas/buscar_youtube.py --consultas consultas.tsv --dias 180 --saida videos.tsv --n 10 --pausa 3
python ../ferramentas/baixar_legendas.py --saida transcricoes --arquivo ids.txt --pausa 6
python ../ferramentas/meta_instagram.py social/posts.txt
```

Reels/TikToks: skill `watch` com `--detail transcript` (WhisperX local). O YouTube devolve 429 em
rajada: uma plataforma por vez, pausa de 6 s.
