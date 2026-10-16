# Métricas do Instagram — contrato de dados

Esta pasta é escrita pelo **coletor do bot** (`central-claude`, `src/agentes/instagram/metricas/`),
que lê a **API oficial da Meta** (Instagram Graph API): os insights da @cafecanastra e, pela
Business Discovery, os dados públicos dos concorrentes. Não usa Chrome nem modelo.

Quem lê: o radar de destaques, o detector de virada, a medição de 24h do agente e o relatório
do canal. **Este arquivo é a referência.** Mudou um campo? Registre aqui, em "Mudanças".

## Regras que valem para todo arquivo

- **Ausente = `null`. Nunca estimado e nunca zero.** Zero quer dizer "a API disse zero".
- Datas em ISO 8601. `data_publicacao` vem como a API manda (`2026-10-13T18:02:11+0000`);
  `coletado_em` é o instante da coleta, em UTC (`…Z`).
- **Append-only.** Cada coleta *acrescenta* linhas, e o mesmo post aparece uma vez por coleta. Para o
  estado atual de um post, pegue **a última linha por `id`** (maior `coletado_em`). As linhas antigas
  são o histórico (é por elas que se vê um post "virando" dias depois).
- `formato` / `tipo` ∈ `reel | carrossel | estatico`. Vídeo de feed antigo (de antes dos Reels) conta
  como `reel`.

## Arquivos

### `proprios.jsonl` — a @cafecanastra

Uma linha por post por coleta:

| Campo | O que é | De onde |
|---|---|---|
| `id` | id da mídia na Graph API | API |
| `url` | permalink | API |
| `data_publicacao` | quando saiu | API (`timestamp`) |
| `formato` | `reel`, `carrossel` ou `estatico` | API (`media_type` / `media_product_type`) |
| `legenda` | legenda inteira (`""` se não houver) | API |
| `gancho` | gancho **de tela** (3 primeiros segundos / 1º slide) ou `null` | `ganchos.json` |
| `coletado_em` | instante da coleta | coletor |
| `seguidores_conta` | seguidores da conta **no instante da coleta** | API |
| `alcance` | contas alcançadas (`reach`) | insights |
| `views` | visualizações (`views`) | insights |
| `curtidas` | `likes`; sem insight, a contagem pública do post | insights / API |
| `comentarios` | `comments`; sem insight, a contagem pública | insights / API |
| `saves` | salvamentos (`saved`) | insights |
| `shares` | envios (`shares`) | insights |
| `tempo_medio_assistido_s` | `ig_reels_avg_watch_time` ÷ 1000, **só Reels** | insights |

Post antigo, de antes da conta virar comercial, não tem insight: sai com curtidas e comentários
públicos e o resto `null`. No histórico importado, `seguidores_conta` é o número **do dia da
importação**, não o da época do post.

### `concorrentes/<handle>.jsonl` — dado público dos concorrentes

`{id, url, data_publicacao, tipo, legenda, curtidas, comentarios, views, seguidores, coletado_em}`

- `curtidas: null` quando o perfil esconde as curtidas.
- `views`: `view_count` quando a Business Discovery devolve (costuma vir só em Reels); senão `null`.
- `seguidores`: os do perfil no instante da coleta.
- O nome do arquivo é o handle sem `@` (ex.: `cafezale.com.br.jsonl`).

### `watchlist.json` — quem acompanhar

```json
{ "atualizado_em": "…", "handles": ["orfeucafes", "…"],
  "concorrentes": [{ "handle": "orfeucafes", "nome": "Orfeu", "grupo": "especial" }] }
```

- Semente: os 9 perfis de `instagram/01-concorrencia.md`. `grupo: "homonimo"` são os três "Serra da
  Canastra" que ocupam o nome sem ser a marca; o relatório os mostra à parte.
- **Para acrescentar um concorrente**, ponha o handle em `concorrentes` (com `nome` e `grupo`) ou só em
  `handles`. O coletor completa o outro lado na próxima leitura. `handles` existe para o radar de
  destaques, que lê esse campo.
- O perfil precisa ser **comercial ou de criador**: a Business Discovery não enxerga conta pessoal.

### `ganchos.json` — gancho de tela por post

`{ "<shortcode>": "<gancho>" }`. O shortcode é o trecho depois de `/p/` ou `/reel/` na URL. A API não
sabe qual foi o gancho, então quem grava é o turno da medição de 24h, lendo a pasta da peça, ou você à
mão. O coletor junta esse valor na linha do `proprios.jsonl`.
Pendente: o Reel "Onze provas" (13/10) ainda não tem link registrado; entra quando a primeira coleta
o encontrar.

### `temas.json` — tema por post

`{ "<id>": "<tema>" }`, gravado pela leitura do relatório. Ela classifica só quem ainda não tem tema;
corrigir à mão é permitido e é respeitado.

### `coletas.json` — estado do agendador

`{ ultima_coleta, ultimo_historico, ultimo_relatorio }` (ISO). Se o maior `coletado_em` dos `.jsonl`
tiver mais de 36 h, a coleta parou (token expirado, PC desligado às 2h).

### `relatorios/` — o relatório do canal

`<data>.html` (abrir no navegador), `<data>-resumo.json` (os números), `<data>-legendas.json` (o que a
leitura recebeu) e `<data>-analise.md` (o texto da leitura).

## Quando roda

| Quando | O quê |
|---|---|
| todo dia, 2h (`INSTAGRAM_HORA_COLETA`) | insights dos posts próprios dos últimos 30 dias e os 25 posts mais recentes de cada concorrente |
| a cada 14 dias (`INSTAGRAM_RELATORIO_DIAS`), e na primeira coleta | **histórico**: todos os posts próprios e até 100 por concorrente, e depois o **relatório** |
| 24 h depois de cada post nosso | medição: uma linha a mais no `proprios.jsonl` e a lição em `instagram/licoes.md` |
| quando o Rafael escreve `relatório` no #instagram | o relatório na hora |

## Mudanças

- 2026-10-15: contrato inicial (fluxo 1). Acréscimos ao pedido original: `watchlist.json` ganhou
  `handles` (espelho, para o radar) e `grupo`; nasceram `ganchos.json`, `temas.json` e `coletas.json`.
