---
name: canastra-virada
description: Use when asked when or why an Instagram profile "virou" — o post em que o desempenho mudou de patamar, creator breakout, "quando esse perfil começou a crescer", "o que mudou no Orfeu", degrau × pico, ou quando a @cafecanastra ou um concorrente da watchlist precisa de um diagnóstico de virada com o que mudou ao redor (tema, gancho, formato, cadência).
---

# Virada — em que post o perfil mudou de patamar

Esta skill manda em **achar o momento da virada e ler o que mudou ao redor**. O detector é
`scripts/virada.py`, e a spec é `docs/superpowers/specs/2026-10-15-detector-virada-design.md`.

## Rotear primeiro

| Assunto | Dono |
|---|---|
| coletar posts, curtidas, seguidores (API da Meta), a watchlist | **fluxo 1**, `instagram/metricas/` (`LEIA-ME.md` é o contrato) |
| escrever gancho novo a partir do que a virada mostrou | **skill de ganchos** (fluxo 5) |
| ficha de vídeo analisado quadro a quadro | `instagram/referencias-virais/LEIA-ME.md` |
| **em que post o patamar mudou, e o que mudou junto** | **esta skill** |

**Esta skill não coleta nada da Meta.** Se o número não está em `instagram/metricas/`, o
detector não inventa.

---

## Três coisas que não são a mesma

| Evento | O que é | O que fazer com ele |
|---|---|---|
| **Degrau sustentado** | o patamar subiu e **ficou**: a mediana dos 8 posts seguintes ≥ 1,8× a linha de base, com 60% deles acima | é a virada. Estude o que mudou na janela, não só o post |
| **Queda de patamar** | o espelho: ≤ 0,55× e ficou | vale tanto quanto o degrau: o que o perfil parou de fazer? |
| **Pico isolado** | um post ≥ 3× a base, e o perfil **voltou** ao patamar | sorte, tema quente ou impulsionamento. Não é virada |

Um pico isolado não vira degrau no relatório, e é de propósito. "O post que viralizou" e "o
momento em que o perfil mudou" são perguntas diferentes, e misturar as duas é a leitura
errada mais comum. Um post de 3× ou mais dentro de um degrau aparece como **puxador** do
degrau, não como pico.

Outros estados:
- `imaturo` = post com menos de 3 dias, que ainda acumula curtidas. Aparece vazado no
  gráfico e fica fora da conta;
- `sem_base` = os 6 primeiros posts da janela, que não têm 6 anteriores para formar a
  mediana;
- pico `confirmado: false` = há menos de 3 posts depois dele, então ainda pode ser o começo
  de um degrau.

## Pré-condição: o perfil está na coleta?

```bash
ls instagram/metricas/concorrentes/          # um .jsonl por concorrente
ls instagram/metricas/proprios.jsonl         # a @cafecanastra
```

Se o perfil não tem arquivo, o detector sai com **código 2** e diz qual caso é: a pasta não
existe, o perfil está na watchlist mas ainda não foi coletado, ou ele não está na watchlist.
**Diga isso ao Rafael e ofereça as duas saídas:**

1. **(preferível)** incluir o perfil na watchlist do fluxo 1 e rodar a coleta;
2. **fallback explícito**: ler a grade pelo Claude in Chrome (skill `chrome-browser`).
   Use uma conta secundária, porque o Instagram limita com HTTP 429. Grave
   `instagram/viradas/<handle>/_coleta-manual.jsonl` no mesmo formato do contrato, um post
   por linha:

   ```json
   {"id": "<shortcode>", "url": "https://www.instagram.com/p/<shortcode>/", "data_publicacao": "2026-09-25T14:03:00+0000",
    "tipo": "REEL", "legenda": "...", "curtidas": 120, "comentarios": 8, "views": null,
    "seguidores": 10300, "coletado_em": "2026-10-15T10:00:00Z"}
   ```

   Rode com `--arquivo` e **diga no relatório que a fonte foi manual**. Curtida oculta pelo
   dono é `null`, nunca `0`: um zero inventado vira uma queda falsa.

## Rodar

Rode a partir do **diretório principal** do repositório. `instagram/metricas/` e
`instagram/referencias-virais/` vivem lá; um worktree pode estar atrás.

```bash
python scripts/virada.py orfeucafes                 # janela padrão: 365 dias
python scripts/virada.py orfeucafes --dias 90       # rodada rápida
python scripts/virada.py @cafecanastra --dias 0     # histórico inteiro (lê proprios.jsonl)
python scripts/virada.py fulano --arquivo instagram/viradas/fulano/_coleta-manual.jsonl
```

| Opção | Padrão | Efeito |
|---|---:|---|
| `--dias` | 365 | janela até hoje; `0` = tudo |
| `--maturidade` | 3 | posts mais novos que isso não entram na conta |
| `--k` | 12 | posts anteriores na linha de base |
| `--m` | 8 | posts da janela "depois" |
| `--pico` | 3,0 | razão mínima de um pico |
| `--degrau` / `--queda` | 1,8 / 0,55 | razão de nível de um degrau / de uma queda |
| `--sustentacao` | 0,6 | fração da janela depois que precisa ficar do lado novo |
| `--hoje` | data de hoje | fixa a data para refazer uma rodada antiga |

Saída: `instagram/viradas/<handle>/<AAAA-MM-DD>.json` (números, para ler e citar) e `.html`
(gráfico cronológico em escala log; cada ponto abre o post; faixa verde = degrau, vermelha =
queda, anel amarelo = pico; e um cartão por virada com o antes × depois).

Com menos de 30 posts maduros, os parâmetros padrão quase não deixam espaço para dois
eventos. Perfil que posta pouco, como a @cafecanastra (um post a cada 42 dias em 30/09),
precisa de `--dias 0`. Mesmo assim o resultado é fraco, e você diz isso.

## Sinais além do salto

Adaptados da skill "Creator Breakout" do Kallaway em 15/10/2026, com aprovação do Rafael.
Ficaram de fora o outlier score e os créditos do Sandcastles, as palavras-chave fixas em
inglês, a "vanity virality" (views de concorrente vem `null`) e o corte único por t máximo,
que acharia uma virada só onde nós achamos várias.

| Sinal | Onde está | Como ler |
|---|---|---|
| **Consistência do perfil** | `consistencia`, no topo do JSON e do HTML | CV, máximo ÷ mediana e fração dos posts entre 0,5× e 2× a mediana. **Estável** = CV < 1,2 e máximo < 6×: o perfil cresce por constância. **Dependente de pico** = vive de estouros, e então um degrau pesa mais que qualquer pico |
| **Confiança do degrau** | `t_welch`, `confianca`, `n_antes`, `n_depois` em cada degrau e queda | t de Welch sobre `log1p` (depois − antes): **forte** ≥ 4, **moderada** ≥ 2,5, **fraca** abaixo. Com 12 × 8 posts a amostra é pequena: cite o t junto com os tamanhos. `sem variância` = série constante, coisa que não acontece em dado real |
| **Comentários por curtida** | `antes_depois.antes/depois` e cada item de `puxaram` | sinal de funil comentário → DM. Uma razão que sobe junto com legenda pedindo comentário ("comenta EU QUERO") é o funil funcionando; cite os números |
| **CTA, produto, colaboração** | `cta_fatia`, `produto_fatia`, `colab_fatia` | fração dos posts com chamada para ação ("comenta", "link na bio", "chama na DM", "cupom", "frete", "compre"), com vocabulário de produto de café (pacote, cápsula, em grãos, 250g, preço, loja) e com `@menção`. **É regex, não leitura**: abra as legendas antes de afirmar |
| **Surgiram, sumiram, mantidos** | `palavras`, `hashtags`, `tipos` em `antes_depois` | por fração de posts: surgiu = ≤ 15% antes e ≥ 40% depois; sumiu = o espelho; mantido = ≥ 40% nos dois. O mantido também conta: o que não mudou na virada sai da lista de explicações |

## Ler e entregar

1. **Leia o JSON, não o resumo do terminal.** Para cada degrau e queda,
   `antes_depois` traz: formatos, cadência em posts por semana, intervalo mediano, tamanho
   da legenda, hashtags, comentários por curtida, as fatias de CTA, produto e colaboração,
   a 1ª linha da legenda dos posts que ficaram acima da base antiga, e o que surgiu, sumiu e
   se manteve em palavras, hashtags e formatos.
2. **Publique o HTML como Artifact** (privado), com título `Virada @<handle>`, e entregue o
   link junto com o caminho local. O HTML é autocontido, sem script nem CDN.
3. Abra a resposta pela consistência do perfil: ela diz se o perfil vive de constância ou de
   pico, e isso muda o peso de cada evento.
4. Escreva a leitura em 3 blocos por virada: **o número** (data, razão, mediana antes →
   depois e a confiança com o t e os tamanhos), **o que mudou** (só o que o `antes_depois` mostra ou o que você viu abrindo o
   post) e **o que serve à Canastra**.

## Passo qualitativo: o porquê

O script calcula e não interpreta. O porquê sai daqui, e só para a **virada principal**,
que é o degrau de maior razão, com **no máximo 3 posts**: o do ponto e os 2 puxadores de
maior razão.

1. Abra cada post (Claude in Chrome ou o navegador embutido). Anote o gancho de 0–3 s, o
   formato, o tema e quem aparece. A 1ª linha da legenda é só o gancho escrito; o do vídeo
   exige ver o vídeo (skill `watch` para Reel).
2. Procure na biblioteca:

   ```bash
   python scripts/indice_referencias.py buscar <handle>             # o perfil já tem ficha?
   python scripts/indice_referencias.py buscar <shortcode>          # este post já tem ficha?
   python scripts/indice_referencias.py buscar <formato> <etapa>    # o mesmo padrão em outros perfis
   ```

   O vocabulário de formato, gancho e etapa está em `VOCAB`, dentro do script.
3. **Ficha nova só quando** o post não está na biblioteca **e** é o puxador da virada
   principal. Use o modelo de `instagram/referencias-virais/LEIA-ME.md` (seções 0 a 7) com
   frente `concorrentes`, e rode `python scripts/indice_referencias.py` para reindexar.
   Valem as regras de conteúdo de terceiros de lá: só texto e análise; vídeo, quadro e áudio
   não entram no repositório.
4. Se a virada coincide com uma **mudança de formato ou de cadência** no `antes_depois`,
   diga isso primeiro. É a explicação mais barata, e costuma ser a certa. Tema e gancho
   vêm depois.

## Limites (leia antes de citar um número)

- **Engajamento não é alcance.** A série principal é curtidas + comentários. Views só entra
  quando ≥ 60% dos posts trazem o número, e na API de concorrente costuma vir `null`.
- **Pago × orgânico não se distingue.** Um degrau que coincide com impulsionamento parece
  idêntico a um orgânico. A `organico` das fichas é leitura, não dado.
- **`seguidores` é o número do dia da coleta**, não o da data do post. Por isso nada é
  normalizado por seguidor, e "cresceu em seguidores" não se afirma a partir deste
  relatório.
- **A borda da janela engana.** Os 6 primeiros posts não têm base, e um degrau muito perto do
  começo da janela some. Se a virada parece estar logo antes do início, rode com `--dias`
  maior.
- **Um 8× seguido de patamar 1,6× não aparece na lista de eventos**: não voltou (não é
  pico) e não subiu o bastante (não é degrau). Ele está no gráfico com a razão. Para
  olhar, rode de novo com `--degrau 1.5`, e diga que mudou o limiar.
- Curtidas antigas continuam crescendo devagar. Posts de anos atrás comparados com posts de
  semanas atrás têm um viés pequeno a favor dos antigos.
