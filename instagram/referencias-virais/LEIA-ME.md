# Biblioteca de referências virais de café

Mapa de vídeos curtos de café que deram certo, analisados quadro a quadro, para **consultar
antes de criar qualquer vídeo ou conteúdo** da Canastra. Nasceu da reprovação do Reel 08
("esse café já foi uma fruta", 11/10/2026; ver lição 66 do `CLAUDE.md`).

| Arquivo | O que é |
|---|---|
| [relatorio.md](relatorio.md) | **Comece aqui.** Conclusões, tabela "Reel 08 × o que os virais fazem", 14 regras e 5 propostas de reformulação |
| [relatorio-motion.md](relatorio-motion.md) | **Antes de qualquer peça animada.** Método do motion de marca que viraliza (58 casos de qualquer categoria): receita em 14 passos, 17 técnicas com custo e como fazer no Remotion, regra orgânico × pago, 6 peças propostas para a Canastra |
| [INDICE.md](INDICE.md) | Todos os vídeos em tabela, por views, por etapa do processo, por formato e por tipo de gancho. **Gerado; não edite à mão** |
| `indice.json` | O mesmo índice, para script |
| `videos/<frente>/<perfil>_<id>.md` | Uma ficha por vídeo (ver modelo abaixo) |
| `sinteses/` | As notas de cada frente de pesquisa: `watch_*` (vídeos assistidos) e as de pesquisa de mesa (fontes, estudos, plataformas) |

Coleta de 12/10/2026 (motion, 58 fichas): `motion-criadores` (14, estúdios e motion designers),
`motion-marcas` (15, marcas globais de qualquer categoria), `motion-3d-fooh` (15, CGI, FOOH,
stop-motion) e `motion-brasil` (14). Essas fichas têm 4 campos a mais: `tecnica`, `ferramentas`,
`categoria_marca` e `metodo`, e uma seção "Método de animação".

Coleta de 11/10/2026: 72 fichas em 4 frentes — `processo` (21, fazenda à torra), `brasil` (19,
criadores e marcas BR), `marcas` (18, torrefações de especial e Starbucks como contraste) e
`influenciadores` (14, criadores globais). O vídeo do Tanner Colson na Finca Hartmann está em
duas frentes, de propósito.

## Como usar na criação

1. **Antes do roteiro**, busque 3 referências do mesmo formato ou da mesma etapa e cite-as no
   planejamento da peça:

   ```bash
   python scripts/indice_referencias.py buscar torra
   python scripts/indice_referencias.py buscar terreiro-secagem pt
   python scripts/indice_referencias.py buscar produtor-fala supermercado
   ```

   A busca exige todos os termos e ordena por views. O vocabulário das etiquetas está no
   próprio script (`VOCAB`).
2. Abra a ficha: o gancho (o que se vê, lê e ouve em 0–3 s), a transcrição com tempos e a
   tabela plano a plano dizem **como** o vídeo foi montado, não só **o que** ele diz.
3. Confira a peça contra as regras do [relatorio.md](relatorio.md) e a lição 66 do
   `CLAUDE.md` (humor só de dentro do café; torra nunca com fogo, fumaça ou grão preto).

## Modelo da ficha (para acrescentar vídeos)

Seções, nesta ordem: `## 0. Etiquetas` (19 campos fixos, valores do vocabulário de
`scripts/indice_referencias.py`) · `## 1. Ficha` (link, perfil, data, duração, views,
curtidas, comentários, legenda) · `## 2. Gancho (0–3 s)` · `## 3. Transcrição` com
`[mm:ss.s → mm:ss.s]` · `## 4. Formato de edição` (tempos de corte, cortes/10 s, tabela plano a
plano) · `## 5. Estrutura` · `## 6. Por que funcionou e o que serve à Canastra` · `## 7. Arquivos
locais`. Depois: `python scripts/indice_referencias.py` (recusa campo fora do vocabulário).

Método de análise (local, sem Gemini): grade de Reels no Chrome logado para achar os mais
vistos → `yt-dlp` → `ffmpeg` (cortes por `select=gt(scene,0.25)`, folhas de quadros do gancho e
do vídeo) → transcrição local (whisper.cpp ou faster-whisper), **um vídeo por vez, com
timeout**: 9 transcrições em paralelo travaram a máquina nesta coleta.

## Regras de uso — conteúdo de terceiros

- **Só texto e análise vivem aqui.** Vídeos, folhas de quadros e áudios de terceiros não entram
  no repositório; cada ficha guarda o link do post para rever o original.
- Referência de terceiro **nunca** vira pixel da Canastra nem é enviada como imagem de
  referência ao ChatGPT ou ao Grok. Vale a mesma regra de `base-curada/03-mood-terceiros`.
- Copiar estrutura, ritmo e tipo de gancho é o uso previsto; copiar roteiro, bordão ou
  enquadramento reconhecível de um criador, não.

## Limites (leia antes de citar um número)

- Views lidas das grades em 11/10/2026: podem incluir alcance pago. Fichas marcadas
  `organico: provavel-pago` ou `collab` não provam alcance orgânico.
- As grades foram lidas parcialmente (o Instagram limitou com HTTP 429): pode haver vídeos
  antigos maiores fora da amostra.
- Transcrições locais com erros de reconhecimento; onde importou, a ficha corrige pelo texto
  queimado na tela. Música sob som direto nem sempre foi verificada.
