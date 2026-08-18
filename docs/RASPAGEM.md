# Raspagem do Instagram (cie scrape)

Guia pratico de `cie scrape`: como colher imagem do Instagram (perfil, post ou
hashtag) para dentro de `raspagem/`, com proveniencia, dedupe e sem tocar o banco do
CIE.

---

## 1. O teto que voce precisa saber antes de usar isto

`cie/imaging.py` fixa:

```python
REFERENCE_MIN_SIDE = 1200
```

`is_reference_grade()` so aprova uma foto como referencia se o lado menor tiver pelo
menos esses 1200 px (alem do `quality_score` minimo). O Instagram entrega imagem no
maximo em **1080px** de lado. Logo, **nenhuma imagem raspada aqui pode virar pixel de
saida neste sistema** — `is_reference_grade` reprova todas, sempre.

Isso nao e uma limitacao a contornar. E a regra da casa funcionando:

> ### A IA edita e estende o real; a IA nao inventa o real.

Material de terceiro (ou ate o proprio feed da marca, ja recomprimido pelo Instagram)
nunca e materia-prima de composicao. Ele serve para uma coisa so: virar descritor
textual de estilo — mood, paleta, enquadramento — para alimentar humano ou Style DNA.
A ferramenta e construida assumindo esse teto, nao lutando contra ele.

---

## 2. Instalacao

Playwright e um extra opcional — quem nao vai raspar nao instala:

```bash
uv sync --extra scrape
```

Ele abre o **Chrome que voce ja tem instalado** (`channel="chrome"`); nao baixa
Chromium. Se o Chrome nao estiver instalado, `cie scrape login`/`status`/`harvest`/
`run` explicam isso na mensagem de erro.

---

## 3. Login

```bash
cie scrape login     # abre o Chrome visivel; faca login e deixe a janela aberta
cie scrape status    # a sessao salva ainda esta logada?
```

A sessao fica em `.cie/browser-profile/` (dentro de `CIE_HOME`, ja coberto pela regra
`.cie/` do `.gitignore`).

**Use uma conta secundaria.** O proprio `cie scrape login` avisa isso na tela: raspagem
pesada rende bloqueio temporario, e voce nao quer isso acontecendo no perfil comercial
da marca no meio de uma operacao.

---

## 4. Uso

```bash
# perfil (link completo)
cie scrape run https://www.instagram.com/cafecanastra/

# perfil (handle solto, com ou sem @)
cie scrape run @cafecanastra
cie scrape run cafecanastra

# post unico (carrossel inteiro, se for o caso)
cie scrape run https://www.instagram.com/p/CxYz123AbC/

# hashtag
cie scrape run https://www.instagram.com/explore/tags/cafeespecial/
cie scrape run '#cafeespecial'
```

Reel e recusado de proposito, com a URL reconhecida e a mensagem explicando o porque
(video nao e referencia de imagem estatica). Stories tambem sao recusados: sao
efemeros e nao tem proveniencia estavel.

### Opcoes

`cie scrape run <link>` — colhe e baixa, o comando normal:

| Opcao | Padrao | O que faz |
|---|---|---|
| `--limit` | `12` | quantos posts colher; `0` = todos |
| `--out` | `raspagem/` | raiz de saida |
| `--delay` | `1.0` | pausa em segundos entre downloads |
| `--dry-run` | desligado | lista o que baixaria, sem gravar nada |
| `--show-browser` | desligado (headless) | abre o Chrome visivel em vez de headless |

### O escape hatch de duas etapas

Quando algo quebra no meio do caminho, `cie scrape run` se separa nos dois comandos que
o compoem:

```bash
# 1. So colhe o JSON cru do Instagram, sem baixar nenhuma imagem
cie scrape harvest https://www.instagram.com/cafecanastra/ --limit 20

# 2. Baixa as imagens a partir do envelope gravado pelo harvest
cie scrape collect raspagem/_colheita/cafecanastra-20260818T120000123456.json
```

`cie scrape harvest` grava o envelope em disco **antes** de qualquer download — por
isso a colheita nunca se perde: se o download falhar (rede caiu, PC desligou), a
resposta crua do Instagram continua em `raspagem/_colheita/`, e `cie scrape collect`
retoma dali sem raspar de novo.

`harvest` aceita `--limit` (padrao `12`), `--out` (padrao `raspagem/`) e
`--show-browser`. `collect` aceita `--out`, `--limit` (padrao `0` = sem teto de
downloads), `--delay` (padrao `1.0`) e `--dry-run`.

---

## 5. O que fica em disco

```
raspagem/
  _colheita/
    cafecanastra-20260818T120000123456.json   # JSON cru gravado por `harvest`
  cafecanastra/
    2026-08-18_CxYz123_1.jpg
    2026-08-18_CxYz123_1.json                 # sidecar da imagem acima
  _manifest.json                              # indice de tudo, chaveado por sha256
```

- **`_colheita/<slug>-<carimbo>.json`** — o envelope cru que `harvest` recebeu do
  Instagram, um arquivo por chamada. E o material bruto para investigar quando algo
  muda (ver secao 8).
- **`<slug>/`** — uma pasta por alvo (`target_slug`, ja neutralizado — ver secao 7),
  com uma imagem e um sidecar `.json` de mesmo nome para cada arquivo baixado.
- **`_manifest.json`** — indice acumulado de tudo sob `raspagem/`, uma entrada por
  `sha256`, atualizado a cada `collect`/`run` que baixa algo.

### O que o sidecar registra

```json
{
  "post_url": "...",
  "owner_handle": "...",
  "shortcode": "...",
  "carousel_index": 1,
  "source_url": "...",
  "width": 1080,
  "height": 1350,
  "taken_at": "...",
  "caption": "...",
  "sha256": "...",
  "scraped_at": "..."
}
```

O sidecar **nao** grava `has_identifiable_person` nem `consent_on_file`. Esses dois
campos existem **so** em `Asset` (a tabela do catalogo do CIE) e **so** curadoria
humana explicita os preenche — a raspagem nao tem, e nunca vai ter, opiniao sobre
pessoa ou consentimento. E texto no proprio codigo, no topo de
[`cie/scrape/models.py`](../cie/scrape/models.py):

> `ScrapedItem` deliberadamente NAO tem `has_identifiable_person` nem
> `consent_on_file`. Esses dois campos so existem em `Asset`, e so a curadoria humana
> os preenche. A raspagem nao tem direito de opinar sobre eles.

---

## 6. Como isto vira acervo

Por si so, nao vira. `cie scrape` para em `raspagem/` — nenhum comando do pacote grava
no banco do CIE. `raspagem/` fica fora de `base-curada/`, de proposito.

O passo seguinte e humano:

1. Olhe o que caiu em `raspagem/<slug>/` e decida o que presta.
2. Mova o que presta para:
   - `base-curada/03-mood-terceiros/` — material de perfil de terceiro, referencia de
     estilo;
   - `base-curada/02-real-nao-verificada/` — fotos do proprio perfil da marca, que o
     Instagram ja despiu de EXIF (por isso "nao verificada": nao ha prova de origem no
     arquivo).
3. Rode `cie ingest` sobre o destino escolhido.
4. Curadoria normal dai em diante: `cie assets review` / `cie assets curate`.

`cie scrape run` ja lembra disso na tela, depois de qualquer download real:

> Nada disso entrou no acervo. Para promover, mova para
> `base-curada/03-mood-terceiros/` (ou `02-real-nao-verificada/`, se for foto da
> propria marca) e rode `cie ingest`.

---

## 7. Regras garantidas no codigo

| Garantia | Onde vive |
|---|---|
| Video nunca e baixado | `download.download_batch` — todo item com `is_video=True` (ou sem `display_url`) vira status `"video"` e nunca chega a `fetch` |
| Reel e recusado na hora de interpretar o link, antes de qualquer raspagem | `targets.parse_target` — `/reel/`, `/reels/` e `/tv/` levantam `ScrapeError` explicando o porque |
| Conteudo duplicado e pulado por sha256 | `download._hashes_existentes` (le os sidecars ja em disco) + o teste de `digest in conhecidos` dentro de `download.download_batch` |
| Nada sobrescreve nada | `download._caminho_livre` — nome ja existente ganha sufixo `-2`, `-3`, ... |
| Todo arquivo nasce com sidecar | `download._grava_sidecar`, chamado logo apos cada `write_bytes` |
| Formato inesperado do Instagram vira erro legivel, nunca `KeyError`/`AttributeError` | `parser._objeto` / `parser._lista` / `parser._inteiro`, usados por `parser.parse_media` antes de qualquer campo externo ser lido; levantam `InstagramFormatError` nomeando o campo |
| Nada escreve no banco do CIE | estrutural: nenhum modulo de `cie/scrape/` importa `cie.db`; ver o docstring de [`cie/scrape/__init__.py`](../cie/scrape/__init__.py) — "Nada aqui escreve no banco do CIE" |

### Defesa contra path traversal

`target_slug` (do alvo raspado) e o `shortcode` (de cada item) viram, os dois,
componente de caminho de arquivo — e os dois chegam de fora: um do JSON que o
Instagram devolve, outro de um envelope que o usuario pode ter editado a mao antes de
rodar `cie scrape collect`. Ambos passam por
[`cie/scrape/models.py`](../cie/scrape/models.py)`::caminho_seguro`, que troca todo
caractere fora da allowlist (`A-Za-z0-9._-`) por `_`, remove sequencias `..` e apara
pontos/espacos nas pontas. Sem isso, um slug hostil como `../../x` escaparia de
`raspagem/`.

---

## 8. Quando o Instagram mudar o formato

Vai mudar. Os sintomas apontam para lugares diferentes:

- **`InstagramFormatError` nomeando um campo ausente ou do tipo errado** — o objeto
  `media` do Instagram mudou de forma. Conserte
  [`cie/scrape/parser.py`](../cie/scrape/parser.py) e atualize os fixtures em
  [`tests/fixtures/scrape/`](../tests/fixtures/scrape/) (`perfil.json`,
  `post-carrossel.json`, `hashtag.json`).
- **`ScrapeError` com um `HTTP 4xx` na mensagem** — o endpoint mudou (rota, parametro
  obrigatorio novo, autenticacao diferente). Conserte o snippet correspondente em
  [`cie/scrape/js/`](../cie/scrape/js/) (`profile.js`, `post.js`, `hashtag.js` ou
  `appid.js`).
- **Colheita vazia, sem nenhum erro** — a forma da resposta mudou sem mudar o status
  HTTP (ex.: um campo que existia sumiu silenciosamente, ou passou a vir vazio).
  Rode `cie scrape harvest <link>` e leia o JSON cru gravado em
  `raspagem/_colheita/`.

O JSON cru existe precisamente para esse momento: ele vira o proximo fixture de teste.
Copie o trecho relevante (redigindo qualquer dado sensivel), cole em
`tests/fixtures/scrape/`, escreva o teste que falha contra o formato novo, e so entao
ajuste `parser.py` ou o snippet ate o teste passar.
