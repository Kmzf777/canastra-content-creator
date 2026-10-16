# Detector de virada (fluxo 4) — design

Aprovado pelo Rafael em 15/10/2026. Um dos 5 fluxos de crescimento em rede (análise de
canal, alvo de público, radar de outliers, **detector de virada**, máquina de ganchos),
construídos em paralelo, uma sessão por fluxo.

## Pergunta que o fluxo responde

Dado um perfil do Instagram, **em que post o desempenho mudou de patamar**, e o que mudou ao
redor desse post: tema, gancho, formato, cadência.

## Escopo de arquivos

| Caminho | Papel |
|---|---|
| `scripts/virada.py` | o detector: lê a série, detecta, grava JSON e HTML |
| `.claude/skills/canastra-virada/SKILL.md` | quando usar, como rodar, como ler, passo qualitativo |
| `instagram/viradas/<handle>/<AAAA-MM-DD>.{json,html}` | saída do relatório |
| `tests/test_virada.py` | testes; as séries no formato do contrato são geradas no próprio teste |

Fora do escopo: `instagram/metricas/` (fluxo 1, dono da coleta), `instagram/estrategia/`
(fluxo 2), a skill de ganchos (fluxo 5). **Nenhuma coleta própria da Meta.**

## Fonte de dados (contrato do fluxo 1)

- `instagram/metricas/watchlist.json`: perfis monitorados.
- `instagram/metricas/concorrentes/<handle>.jsonl`: um post por linha.
- `instagram/metricas/proprios.jsonl`: a @cafecanastra.
- O contrato oficial fica em `instagram/metricas/LEIA-ME.md` e **ainda não existe** em
  15/10/2026. Este fluxo assume o formato combinado:

```json
{"id": "...", "url": "...", "data_publicacao": "2026-09-25T14:03:00+0000", "tipo": "REEL",
 "legenda": "...", "curtidas": 120, "comentarios": 8, "views": null, "seguidores": 10300,
 "coletado_em": "2026-10-15T10:00:00Z"}
```

Leitura tolerante:
- `id` repetido = a mesma postagem em coletas diferentes; fica o registro com `coletado_em`
  mais recente.
- Datas em ISO 8601, com `Z`, `+0000` ou `+00:00`.
- `tipo` normalizado em maiúsculas. Valores esperados: `REEL`, `IMAGE`, `CAROUSEL_ALBUM`,
  `VIDEO`.
- Uma linha inválida é contada e reportada, nunca derruba a leitura toda.
- `curtidas`/`comentarios` ausentes ou `null` tiram o post da série principal, e esse post
  é contado.

Handle `cafecanastra` (com ou sem `@`) lê `proprios.jsonl`; qualquer outro lê
`concorrentes/<handle>.jsonl` ou `concorrentes/@<handle>.jsonl` (o radar do fluxo 3 aceita
os dois nomes). `proprios.jsonl` grava `seguidores_conta` no lugar de `seguidores`, conforme
a nota do fluxo 1 de 15/10/2026, e os dois nomes são lidos. Sem arquivo, o script sai com código 2 e uma mensagem
dizendo que o perfil precisa entrar na coleta do fluxo 1. O caminho de fallback, a leitura
pelo Claude in Chrome, fica na skill, que monta um `.jsonl` no mesmo formato em pasta
própria e passa ao script por `--arquivo`.

## Métrica

- **Série principal: engajamento = curtidas + comentários.** É a única sempre disponível
  para concorrente pela API.
- **Views** entra como segunda série, detectada à parte, só quando ≥ 60% dos posts da
  janela trazem o número.
- `seguidores` é o valor do dia da coleta, não o da data do post. Por isso **não** se
  normaliza por seguidor: no histórico o divisor seria constante e não muda a detecção. O
  relatório mostra o número como contexto e diz isso.

## Detecção

A série vai em ordem de `data_publicacao`, recortada por `--dias` (padrão 365; `0` = tudo).
Posts com menos de `--maturidade` dias (padrão 3) entram no gráfico como **imaturos** e ficam
fora da detecção, porque ainda acumulam engajamento.

Parâmetros e padrões:

| Parâmetro | Padrão | Uso |
|---|---:|---|
| `k` | 12 | posts anteriores na linha de base (mínimo efetivo 6) |
| `m` | 8 | posts da janela "depois" (mínimo efetivo 5) |
| `pico` | 3,0 | post ≥ 3× a linha de base |
| `degrau` | 1,8 | mediana depois / mediana antes |
| `queda` | 0,55 | mediana depois / mediana antes |
| `sustentacao` | 0,6 | fração da janela depois acima (degrau) ou abaixo (queda) da base antiga |

Definições:

- **Linha de base(i)** = mediana dos `k` posts anteriores a *i*, sem contar *i*. Com menos de
  6 anteriores não há linha de base e o post não é avaliado.
- **Razão do post(i)** = valor(i) / base(i).
- **Razão de nível(i)** = mediana(valores i..i+m−1) / base(i). Exige ao menos 5 posts
  maduros adiante.
- **Degrau sustentado** em *i*: razão de nível ≥ `degrau` **e** ≥ `sustentacao` dos posts da
  janela depois acima de base(i).
- **Queda de patamar**: razão de nível ≤ `queda` **e** ≥ `sustentacao` da janela abaixo de
  base(i).
- Candidatos vizinhos são o mesmo degrau visto de vários índices, e viram **um** ponto. A
  mediana não serve para escolher qual: num degrau limpo 50 → 200 ela dá 4,0× em nove
  índices seguidos, de três posts antes do salto até cinco depois. A escolha usa o
  contraste `média(log(1+v)) da janela depois − média(log(1+v)) dos k anteriores`, o mais
  negativo no caso da queda. A média sente cada post fora do lugar e por isso só é máxima no
  corte certo. A seleção é gulosa: fica o candidato de contraste mais extremo, saem os
  candidatos a menos de `m` posts dele, e repete. Assim uma escada 50 → 200 → 800 dá dois
  degraus, e não um.
- **Pico isolado**: razão do post ≥ `pico` **e** *i* não é ponto de degrau **e** a mediana
  dos posts seguintes (até `m`, sem contar *i*) fica abaixo de 1,5× base(i). Um post ≥ 3×
  dentro de um degrau aparece no relatório como "puxador" do degrau, não como pico. Um pico
  com menos de 3 posts maduros depois sai com `confirmado: false`, porque ainda pode ser o
  começo de um degrau.
- Um post sem linha de base ou sem janela depois suficiente é marcado como "não avaliável",
  com o motivo. Nunca recebe um zero silencioso.

**Pico isolado** e **degrau sustentado** são categorias diferentes, e o relatório trata cada
uma como tal. Pico isolado = um post que estourou e o perfil voltou ao patamar. Degrau = o
perfil mudou de patamar a partir dali.

## O que mudou ao redor (por degrau ou queda)

Janela antes (base(i), os `k` anteriores) × janela depois (os `m` a partir de *i*):

- mistura de formato (contagem por `tipo`);
- cadência em posts por semana (posts / span de datas da janela);
- intervalo mediano entre posts, em dias;
- tamanho mediano da legenda em caracteres, e nº mediano de hashtags;
- **1ª linha da legenda** dos posts da janela depois que ficaram acima da base antiga
  (proxy do gancho escrito; o gancho do vídeo exige abrir o post);
- palavras novas: termos presentes em ≥ 2 posts da janela depois e em nenhum da janela
  antes, sem stopwords do pt-BR, sem hashtags, menções nem links, mínimo de 4 letras;
- hashtags novas, pelo mesmo critério.

Para pico isolado: o post, a razão, o tipo, a 1ª linha da legenda e o link.

O script calcula e não interpreta. A interpretação é o passo qualitativo da skill.

## Saída

`instagram/viradas/<handle>/<AAAA-MM-DD>.json` (data da rodada; `--saida` sobrescreve a
pasta):

- `perfil`, `fonte` (arquivo lido), `gerado_em`, `janela_dias`, `parametros`;
- `contagens`: posts lidos, duplicados descartados, inválidos, imaturos, na série;
- `seguidores_coleta`: o último valor de `seguidores`, com o aviso de que é atual;
- `series`: `engajamento` sempre, e `views` só quando presente. Cada uma traz `posts`
  (id, url, data, tipo, valor, base, razao, estado) e `eventos` (tipo `degrau` | `queda` |
  `pico`, índice, post, razões, `antes_depois`);
- `avisos`: lista de frases (série curta, views insuficientes, linhas inválidas…).

`.html` autocontido, sem CDN, com o mesmo nome:

- cabeçalho com perfil, janela, contagens e avisos;
- **gráfico cronológico em SVG**, eixo y em escala log: cada post é um ponto clicável que
  abre o post (`<a href>` + `<title>` com data, tipo e valor), cor por formato, a linha de
  base em traço, faixas sombreadas nos degraus (verde) e quedas (vermelho), anel nos picos,
  imaturos em cinza vazado;
- um cartão por evento, em ordem cronológica: data, tipo, razão, a tabela antes × depois e
  os links dos posts que puxaram;
- tokens de cor em `:root` com modo escuro, legível em celular.

Depois, a skill publica o HTML como Artifact privado e entrega o link.

## Skill `canastra-virada`

Segue o padrão das `canastra-*`: frontmatter `name`/`description` ("Use when…"), tabela
de roteamento, comandos, como ler, limites. Conteúdo:

1. **Rotear:** dado = fluxo 1 (`instagram/metricas/`), gancho = skill do fluxo 5,
   referência = `instagram/referencias-virais/`.
2. **Pré-condição:** o perfil está na coleta? Se não estiver, diga isso e ofereça (a) pedir
   a inclusão na watchlist ou (b) o fallback explícito pelo Chrome, gravando em
   `instagram/viradas/<handle>/_coleta-manual.jsonl` e rodando com `--arquivo`.
3. **Rodar** a partir do diretório principal do repo. `--dias 90` dá uma rodada rápida.
4. **Ler:** pico × degrau × queda, "não avaliável", e por que o número mais recente não
   entra (imaturo).
5. **Passo qualitativo**, só para a virada principal (o degrau de maior razão) e no máximo
   3 posts: abrir o post; ler gancho, formato e tema; rodar
   `python scripts/indice_referencias.py buscar <formato> <etapa>`; procurar o post na
   biblioteca pelo link/id. **Só gerar ficha nova** quando o post não está na biblioteca
   e é o puxador da virada principal, no modelo do `instagram/referencias-virais/LEIA-ME.md`
   (frente `concorrentes`).
6. **Limites de leitura:** engajamento não é alcance; pago × orgânico não se distingue
   pela API; seguidores são atuais; recorte de janela muda a linha de base nas bordas.

## Testes (pytest, sem rede)

Séries sintéticas no formato do contrato, geradas por função no próprio teste
(lê-se o caso no próprio teste):

- degrau limpo (patamar 50 → 200) → 1 degrau no post certo, 0 picos;
- pico isolado (um 400 num patamar 50) → 1 pico, 0 degraus;
- queda (200 → 50) → 1 queda;
- ruído sem virada (50 ± 30%) → 0 eventos;
- deduplicação por `id` (fica o `coletado_em` mais recente);
- imaturos fora da detecção;
- série curta → aviso, sem evento;
- linha inválida contada sem derrubar a leitura;
- perfil ausente → código 2 e mensagem do fluxo 1;
- views < 60% → só a série de engajamento;
- `antes_depois`: formato, cadência e palavras novas no caso montado;
- HTML gerado contém o SVG, os links e os cartões.
