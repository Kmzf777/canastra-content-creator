# Instagram Scraper (`cie scrape`) — desenho

Data: 2026-08-18
Status: aprovado

## Problema

Falta ao CIE um caminho para trazer imagem do Instagram para dentro do projeto. Hoje a
base nasce de `imagens/` (fotos reais da operação) e nada mais. Quando aparece uma
referência de estilo boa em um perfil de terceiro, ou quando é preciso recuperar o
acervo do próprio `@cafecanastra`, o trabalho é manual: salvar imagem por imagem, sem
proveniência, sem dedupe, sem registro de origem.

O objetivo é colar um link no chat e ter as imagens daquele perfil, post ou hashtag em
disco, com origem registrada, prontas para análise e para uma eventual curadoria humana.

## Restrição que define o escopo

`cie/imaging.py:211` fixa `REFERENCE_MIN_SIDE = 1200`. O Instagram entrega no máximo
**1080px**. Logo, **nenhuma imagem raspada do Instagram pode virar pixel de saída neste
sistema** — `is_reference_grade` vai reprovar todas.

Isso não é um defeito a contornar. É a regra da casa funcionando: material de terceiro
serve como descritor textual de estilo, nunca como matéria-prima de composição. A
ferramenta é construída assumindo esse teto, não lutando contra ele.

O destino natural do que for raspado é portanto:

- `base-curada/03-mood-terceiros/` — referência de estilo de terceiros;
- `base-curada/02-real-nao-verificada/` — fotos do próprio perfil da marca, que o
  Instagram já despiu de EXIF e por isso não têm prova de origem no arquivo.

Em ambos os casos a movimentação é decisão humana registrada, como a `base-curada/LEIA-ME.md`
já determina. A ferramenta nunca faz isso sozinha.

## Escopo

Entra:

- perfil (`instagram.com/<handle>`) — os N posts mais recentes;
- post único (`instagram.com/p/<shortcode>`) — incluindo todas as imagens de um carrossel;
- hashtag (`instagram.com/explore/tags/<tag>`);
- handle solto (`@cafecanastra` ou `cafecanastra`) tratado como perfil.

Não entra:

- Reels. A URL é reconhecida e **recusada com mensagem explicando o porquê**: vídeo não
  é referência de imagem estática, e a capa de um Reel é um frame, não uma foto composta.
- Stories, mensagens diretas, comentários, contagem de likes.
- Qualquer ingestão automática no banco do CIE.

## Autenticação

Playwright com **perfil persistente** em `.cie/browser-profile/`, aberto com
`channel="chrome"` — usa o Chrome já instalado na máquina, sem baixar Chromium.

`cie scrape login` abre o browser em modo headed, o usuário loga na conta que preferir, e
a sessão fica salva no perfil. `cie scrape status` responde se a sessão salva ainda está
logada.

Trade-off aceito explicitamente: uma sessão logada em disco é uma credencial parada. Fica
dentro de `.cie/`, que já está no `.gitignore`. A alternativa (dirigir o Chrome do usuário
por fora a cada raspagem) foi descartada porque impede o usuário de rodar a ferramenta
sozinho.

Risco a documentar no README: raspagem pesada pode render bloqueio temporário da conta.
A recomendação é usar conta secundária, mas o comando não impõe escolha.

## Arquitetura

Um pedaço sujo, fino, isolado; todo o resto puro e testável.

```
cie scrape "<url>" --limit 30
      │
      ├─ targets.py   URL → alvo tipado (perfil | post | hashtag)      [puro]
      ├─ browser.py   abre a sessão salva, page.evaluate() na API interna
      ├─ parser.py    JSON do Instagram → list[ScrapedItem]            [puro]
      └─ download.py  httpx → dedupe sha256 → sidecar + manifest
      ▼
raspagem/<alvo>/2026-08-18_C1a2b3c_1.jpg  (+ .json ao lado)
```

`targets.py` e `parser.py` não sabem que Playwright existe: recebem string e dict,
devolvem objetos. `browser.py` é a única fronteira com o mundo — abre perfil, executa JS,
devolve JSON cru.

Essa separação compra duas coisas concretas: o parser é testável com fixture JSON sem
abrir browser nenhum, e trocar a origem do JSON (por exemplo, passar a interceptar o
tráfego que a própria página faz, quando o endpoint mudar) não custa código novo no
parser.

### Colheita

`page.evaluate()` chama a própria API web do Instagram de dentro da página logada. Como é
same-origin, o cookie da sessão vai automaticamente. O header `X-IG-App-ID` é lido da
configuração da própria página, com constante de fallback.

- Perfil: `/api/v1/users/web_profile_info/?username=<handle>` para a primeira página
  (id do usuário + ~12 posts + cursor); `/graphql/query/` com o cursor para as seguintes.
- Post: página do post, lendo o JSON embutido — evita depender de conversão de shortcode
  para media_id.
- Hashtag: `/api/v1/tags/web_info/?tag_name=<tag>`.

Os snippets ficam em arquivos `.js` versionados em `cie/scrape/js/`, não em strings no
meio do Python. São a parte que mais vai quebrar quando o Instagram mudar, e precisam ser
legíveis e editáveis isoladamente.

O JSON cru de cada lote é gravado em `raspagem/_colheita/<alvo>-<carimbo>.json` antes de
qualquer download. Ele é a fixture natural dos testes e o insumo de `cie scrape collect`.

### Download

`httpx` com User-Agent de browser e `Referer: https://www.instagram.com/`. Se o CDN
recusar, o fallback é baixar pelo contexto de request do próprio Playwright, que já carrega
os headers corretos.

Sequencial, com pausa configurável entre requisições (`--delay`, padrão 1s).

## Estrutura de arquivos

```
cie/scrape/
  __init__.py
  targets.py    URL → ProfileTarget | PostTarget | HashtagTarget    [puro]
  parser.py     JSON do IG → list[ScrapedItem]                      [puro]
  models.py     ScrapedItem, HarvestBatch                           [puro]
  browser.py    Playwright: perfil persistente, login, evaluate     [impuro]
  harvest.py    orquestra browser + grava JSON cru
  download.py   httpx + dedupe sha256 + sidecar + manifest
  js/           profile.js, post.js, hashtag.js
  cli.py        o typer do scrape
```

O typer do scrape mora em `cie/scrape/cli.py`; `cie/cli.py` apenas registra com
`app.add_typer(scrape_app, name="scrape")`, como já faz com `assets`, `queue` e `report`.
`cie/cli.py` já tem ~730 linhas e não deve crescer mais.

`playwright` entra como extra opcional no `pyproject.toml`, no mesmo padrão do extra
`heic` que já existe: `uv sync --extra scrape`. Quem não vai raspar não instala.

## CLI

```
cie scrape login                     abre browser headed para login; sessão persiste
cie scrape status                    a sessão salva ainda está logada?
cie scrape <url> [opções]            colhe + baixa (o comando normal)
cie scrape harvest <url> [opções]    só colhe o JSON cru, não baixa
cie scrape collect <arquivo.json>    só baixa a partir de JSON já colhido
```

Opções de `scrape` e `harvest`:

| Opção | Padrão | Efeito |
|---|---|---|
| `--limit N` | 12 | quantos posts colher; `0` = todos |
| `--out DIR` | `raspagem/` | raiz de saída |
| `--delay S` | 1.0 | pausa entre downloads |
| `--dry-run` | desligado | lista o que baixaria, não baixa |

`--dry-run` existe mas **não** é o padrão. Em `cie generate` ele é padrão porque cada
execução gasta crédito de API; aqui não gasta crédito, e exigir `--execute` seria fricção
sem ganho. O `--limit` conservador é a proteção real contra raspar 900 posts sem querer.

## Saída em disco

```
raspagem/                                    (gitignored)
  _colheita/
    cafecanastra-20260818T2130.json          JSON cru do lote
  cafecanastra/
    2026-08-18_C1a2b3c_1.jpg
    2026-08-18_C1a2b3c_1.json                sidecar
  tag-cafeespecial/
  _manifest.json                             índice de tudo, com sha256
```

`raspagem/` fica **fora** de `base-curada/`. `base-curada/` é base curada, e a regra da
casa é que nada entra em 02/03/04 sem decisão humana registrada. Depositar material cru lá
dentro contamina exatamente o que aquela estrutura existe para proteger.

Nome de arquivo: `<data-do-post>_<shortcode>_<índice>.<ext>`. Ordenável por data,
rastreável ao post de origem, e o índice desambigua carrossel.

Sidecar por arquivo, contendo: URL do post, handle do dono, shortcode, data de publicação,
índice no carrossel, URL do CDN de origem, dimensões, sha256, e carimbo de quando foi
raspado.

## Guardrails

1. **Vídeo nunca é baixado.** Item com `is_video` é registrado como pulado, com motivo.
2. **Nada toca o banco do CIE.** `cie scrape` para em `raspagem/`. `cie ingest` continua
   sendo passo separado e humano.
3. **O sidecar não tem `has_identifiable_person` nem `consent_on_file`.** Esses campos são
   preenchidos pela curadoria humana depois do ingest, como já acontece hoje. A raspagem
   não inventa campo que a máquina não tem direito de preencher.
4. **Proveniência desde o primeiro byte.** Todo arquivo baixado nasce com sidecar. Arquivo
   sem sidecar é bug.
5. **Dedupe por sha256** contra tudo que já está sob `raspagem/`. Colisão = pulado, nunca
   sobrescrito.
6. **Nada sobrescreve arquivo existente**, nem em caso de nome repetido.
7. **`raspagem/` no `.gitignore`**, ao lado de `base-curada/` e `imagens/`.
8. **Erro de formato inesperado no JSON vira mensagem legível**, não `KeyError`. O
   Instagram vai mudar o formato; quando mudar, a mensagem tem que dizer o quê mudou.

## Testes

O projeto já tem 18 arquivos de teste; estes seguem o mesmo padrão.

- `tests/test_scrape_targets.py` — cada forma de URL resolve ao alvo certo; handle solto e
  `@handle` funcionam; URL de Reel é recusada com mensagem explicando; lixo dá erro claro.
- `tests/test_scrape_parser.py` — fixtures JSON (anonimizadas) viram `ScrapedItem`;
  carrossel de N imagens vira N itens com índice correto; vídeo marcado como vídeo; JSON
  com formato inesperado levanta erro legível, não `KeyError`.
- `tests/test_scrape_download.py` — httpx mockado; dedupe por sha256 pula repetido; sidecar
  gravado com todos os campos; vídeo pulado; nada sobrescreve; `--dry-run` não escreve nada.
- `tests/fixtures/scrape/*.json` — respostas de exemplo de perfil, post com carrossel e
  hashtag.

`browser.py` fica sem teste automatizado: é a fronteira com o mundo, e é fina de propósito
justamente para ter pouco a testar. A verificação dele é manual, via `cie scrape status`.

## O que fica de fora, deliberadamente

- Agendamento, raspagem recorrente, monitoramento de perfil.
- Download de vídeo e de Reels.
- Qualquer heurística que tente adivinhar se a foto tem pessoa identificável.
- Ingestão automática no banco.
- Interface web. A UI de curadoria que já existe atende depois do `cie ingest`.
