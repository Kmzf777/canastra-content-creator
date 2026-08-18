# Instagram Scraper (`cie scrape`) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adicionar `cie scrape`, que recebe um link de perfil, post ou hashtag do Instagram e deposita as imagens em `raspagem/` com proveniencia, dedupe por sha256 e sidecar por arquivo.

**Architecture:** Um pedaco sujo e fino (`browser.py`, Playwright sobre perfil de Chrome persistente) isolado de tudo o mais. `targets.py` e `parser.py` sao puros: recebem string e dict, devolvem objetos, e nao sabem que Playwright existe. A colheita usa `page.evaluate()` para chamar a API interna do Instagram de dentro da pagina logada, e grava o JSON cru em disco antes de baixar qualquer byte — esse JSON e a fixture natural dos testes e o insumo de `cie scrape collect`.

**Tech Stack:** Python 3.11, Typer, Pydantic v2, httpx, Playwright (extra opcional), pytest.

**Spec:** `docs/superpowers/specs/2026-08-18-instagram-scraper-design.md`

---

## Convencoes deste repositorio (leia antes da Task 1)

O engenheiro que executar este plano precisa saber disto, porque o codigo existente e consistente e a revisao vai cobrar consistencia:

1. **Docstrings e comentarios em portugues SEM acentuacao.** O codigo existente escreve "geracao", "configuracao", "proveniencia". Siga. Strings visiveis ao usuario (mensagens de erro, help do Typer) tambem seguem esse padrao.
2. **`from __future__ import annotations` no topo de todo modulo.**
3. **Erros herdam de `CieError`** (`cie/errors.py`).
4. **Modelos de dados sao Pydantic v2 com `ConfigDict(extra="forbid")`** (`cie/models.py`). Estruturas internas que nao cruzam fronteira de serializacao usam `@dataclass(frozen=True)` (`cie/naming.py`).
5. **Saida de CLI usa `rich.console.Console`**, ja instanciada como `console` em `cie/cli.py`.
6. **Imports pesados ficam dentro da funcao do comando**, nao no topo do modulo — ver o docstring de `cie/cli.py`. Playwright e httpx entram nessa regra.
7. **Testes nunca tocam a rede.** Ver `tests/conftest.py`, primeira linha.
8. **Rode a suite inteira antes de cada commit:** `uv run pytest`.

---

## Duas divergencias conscientes em relacao a spec

Registradas aqui para ninguem achar que foram esquecimento.

**1. O comando normal e `cie scrape run <url>`, nao `cie scrape <url>`.** A spec
escreveu a forma curta. Typer nao deixa um grupo ter, ao mesmo tempo, subcomandos
(`login`, `status`, `collect`) e um argumento posicional proprio sem ambiguidade
de parse — `cie scrape login` seria lido como "raspar o perfil @login". `run`
custa quatro caracteres e elimina a classe inteira de erro.

**2. O fallback de download pelo contexto de request do Playwright fica de fora.**
A spec previa: se o CDN recusar o `httpx`, baixar pelo browser. Implementar isso
obriga `download.py` a receber uma pagina viva do Playwright, acoplando o modulo
puro a fronteira suja — que e exatamente o que a arquitetura evita.

A decisao e adiar ate haver evidencia de que faz falta. O parametro `fetch` de
`download_batch` e injetavel justamente para ser esse ponto de extensao: no dia
em que a verificacao manual mostrar 403 do CDN, entra um `fetch` alternativo sem
tocar em mais nada. Se o passo de verificacao manual acusar 403, **relate** em
vez de improvisar — a decisao de acoplar volta para a mesa.

---

## Estrutura de arquivos

| Arquivo | Responsabilidade | Puro? |
|---|---|---|
| `cie/scrape/__init__.py` | Exporta a API publica do pacote | — |
| `cie/scrape/targets.py` | URL/handle → alvo tipado; shortcode → media_id | sim |
| `cie/scrape/models.py` | `ScrapedItem`, `HarvestBatch` | sim |
| `cie/scrape/parser.py` | JSON do Instagram → `HarvestBatch` | sim |
| `cie/scrape/download.py` | httpx → dedupe sha256 → sidecar → manifest | quase (httpx injetavel) |
| `cie/scrape/browser.py` | Playwright: perfil persistente, login, evaluate | nao |
| `cie/scrape/harvest.py` | Orquestra browser + monta e grava o envelope | nao |
| `cie/scrape/js/appid.js` | Le o `X-IG-App-ID` da pagina | — |
| `cie/scrape/js/profile.js` | Colhe feed de um perfil, com paginacao | — |
| `cie/scrape/js/post.js` | Colhe um post pelo media_id | — |
| `cie/scrape/js/hashtag.js` | Colhe uma hashtag | — |
| `cie/scrape/cli.py` | O `typer.Typer` do scrape | nao |
| `cie/errors.py` | (modificar) `ScrapeError`, `InstagramFormatError` | — |
| `cie/cli.py` | (modificar) registra o sub-app | — |

**Um unico formato de midia para parsear.** Os tres alvos usam endpoints da API v1, que devolvem o mesmo objeto `media`. Isso e uma decisao deliberada: `web_profile_info` serve so para descobrir o `user_id`, e a colheita real do perfil vem de `/api/v1/feed/user/<id>/`, que tem a mesma forma de `/api/v1/media/<id>/info/` e das secoes de `/api/v1/tags/web_info/`. Um parser, tres alvos.

Campos relevantes do objeto `media`:

| Campo | Significado |
|---|---|
| `code` | shortcode do post (`C1a2b3c`) |
| `taken_at` | timestamp unix da publicacao |
| `media_type` | `1` imagem, `2` video, `8` carrossel |
| `image_versions2.candidates[]` | `{url, width, height}`, varias resolucoes |
| `carousel_media[]` | filhos do carrossel, cada um com seu proprio `media_type` e `image_versions2` |
| `user.username` | handle do dono |
| `caption.text` | legenda (pode ser `null`) |

---

## Task 1: Esqueleto do pacote, erros e configuracao

**Files:**
- Create: `cie/scrape/__init__.py`
- Create: `tests/test_scrape_errors.py`
- Modify: `cie/errors.py` (append ao final)
- Modify: `pyproject.toml` (secao `[project.optional-dependencies]`)
- Modify: `.gitignore`

- [ ] **Step 1: Escreva o teste que falha**

Crie `tests/test_scrape_errors.py`:

```python
"""Os erros do scrape precisam ser capturaveis como CieError."""

from __future__ import annotations

import pytest

from cie.errors import CieError, InstagramFormatError, ScrapeError


def test_scrape_error_e_cie_error():
    assert issubclass(ScrapeError, CieError)


def test_instagram_format_error_e_scrape_error():
    assert issubclass(InstagramFormatError, ScrapeError)


def test_instagram_format_error_diz_o_que_faltou():
    erro = InstagramFormatError("media sem 'code'", campo="code")
    assert erro.campo == "code"
    assert "code" in str(erro)


def test_erros_do_scrape_sao_pegos_como_cie_error():
    with pytest.raises(CieError):
        raise ScrapeError("qualquer coisa")
```

- [ ] **Step 2: Rode o teste e confirme que falha**

Run: `uv run pytest tests/test_scrape_errors.py -v`
Expected: FAIL com `ImportError: cannot import name 'InstagramFormatError' from 'cie.errors'`

- [ ] **Step 3: Adicione os erros**

Acrescente ao final de `cie/errors.py`:

```python
class ScrapeError(CieError):
    """Falha na raspagem: link invalido, sessao deslogada, browser ausente."""


class InstagramFormatError(ScrapeError):
    """O JSON do Instagram nao tem a forma esperada.

    O Instagram muda o formato sem aviso. Quando mudar, a mensagem precisa dizer
    QUAL campo sumiu - `KeyError` nu nao ajuda ninguem as duas da manha.
    """

    def __init__(self, message: str, *, campo: str = "") -> None:
        self.campo = campo
        super().__init__(message)
```

- [ ] **Step 4: Crie o pacote**

Crie `cie/scrape/__init__.py`:

```python
"""Raspagem de imagem do Instagram para dentro de `raspagem/`.

O pacote e dividido em uma parte pura e uma parte suja:

  * `targets` e `parser` nao tocam rede e nao sabem que Playwright existe;
  * `browser` e a unica fronteira com o mundo, e e fina de proposito.

Nada aqui escreve no banco do CIE. `cie scrape` para em `raspagem/`; mover para
`base-curada/` continua sendo decisao humana registrada.
"""

from __future__ import annotations
```

- [ ] **Step 5: Declare o extra opcional**

Em `pyproject.toml`, dentro de `[project.optional-dependencies]`, logo depois da linha do `heic`:

```toml
# Raspagem do Instagram: usa o Chrome ja instalado (channel="chrome"),
# nao baixa Chromium. Quem nao vai raspar nao instala.
scrape = ["playwright>=1.44"]
```

- [ ] **Step 6: Ignore a pasta de saida**

Em `.gitignore`, logo abaixo da linha `base-curada/`:

```
raspagem/
```

- [ ] **Step 7: Rode os testes e confirme que passam**

Run: `uv run pytest tests/test_scrape_errors.py -v`
Expected: 4 passed

Run: `uv run pytest`
Expected: toda a suite passa (nenhuma regressao)

- [ ] **Step 8: Commit**

```bash
git add cie/errors.py cie/scrape/__init__.py tests/test_scrape_errors.py pyproject.toml .gitignore
git commit -m "Scrape: esqueleto do pacote, erros e extra opcional playwright"
```

---

## Task 2: `targets.py` — link para alvo tipado

**Files:**
- Create: `cie/scrape/targets.py`
- Test: `tests/test_scrape_targets.py`

- [ ] **Step 1: Escreva o teste que falha**

Crie `tests/test_scrape_targets.py`:

```python
"""Traducao de link em alvo. Nenhum teste aqui toca a rede."""

from __future__ import annotations

import pytest

from cie.errors import ScrapeError
from cie.scrape.targets import (
    HashtagTarget,
    PostTarget,
    ProfileTarget,
    parse_target,
    shortcode_to_media_id,
)


@pytest.mark.parametrize(
    "entrada",
    [
        "https://www.instagram.com/cafecanastra/",
        "https://instagram.com/cafecanastra",
        "instagram.com/cafecanastra/",
        "www.instagram.com/cafecanastra",
        "@cafecanastra",
        "cafecanastra",
        "  https://www.instagram.com/cafecanastra/?hl=pt-br  ",
    ],
)
def test_perfil_em_todas_as_formas(entrada):
    alvo = parse_target(entrada)
    assert alvo == ProfileTarget(handle="cafecanastra")
    assert alvo.slug == "cafecanastra"
    assert alvo.kind == "profile"


@pytest.mark.parametrize(
    "entrada",
    [
        "https://www.instagram.com/p/C1a2b3cXyZ/",
        "https://www.instagram.com/p/C1a2b3cXyZ/?img_index=2",
        "instagram.com/p/C1a2b3cXyZ",
    ],
)
def test_post_em_todas_as_formas(entrada):
    alvo = parse_target(entrada)
    assert alvo == PostTarget(shortcode="C1a2b3cXyZ")
    assert alvo.slug == "post-C1a2b3cXyZ"
    assert alvo.kind == "post"


@pytest.mark.parametrize(
    "entrada",
    [
        "https://www.instagram.com/explore/tags/cafeespecial/",
        "instagram.com/explore/tags/cafeespecial",
        "#cafeespecial",
    ],
)
def test_hashtag_em_todas_as_formas(entrada):
    alvo = parse_target(entrada)
    assert alvo == HashtagTarget(tag="cafeespecial")
    assert alvo.slug == "tag-cafeespecial"
    assert alvo.kind == "hashtag"


def test_perfil_com_barra_final_e_query_nao_vira_handle_sujo():
    alvo = parse_target("https://www.instagram.com/cafe.canastra_1/?utm_source=x")
    assert alvo == ProfileTarget(handle="cafe.canastra_1")


def test_reel_e_recusado_com_explicacao():
    with pytest.raises(ScrapeError) as exc:
        parse_target("https://www.instagram.com/reel/C1a2b3cXyZ/")
    mensagem = str(exc.value).lower()
    assert "reel" in mensagem
    assert "video" in mensagem


def test_stories_e_recusado():
    with pytest.raises(ScrapeError):
        parse_target("https://www.instagram.com/stories/cafecanastra/123/")


def test_dominio_de_fora_e_recusado():
    with pytest.raises(ScrapeError) as exc:
        parse_target("https://example.com/cafecanastra")
    assert "instagram" in str(exc.value).lower()


def test_entrada_vazia_e_recusada():
    with pytest.raises(ScrapeError):
        parse_target("   ")


def test_url_do_instagram_sem_caminho_e_recusada():
    with pytest.raises(ScrapeError):
        parse_target("https://www.instagram.com/")


# shortcode -> media_id e base64 posicional com o alfabeto do Instagram.
@pytest.mark.parametrize(
    "shortcode,esperado",
    [
        ("B", 1),
        ("BA", 64),
        ("CBa", 8282),
    ],
)
def test_shortcode_vira_media_id(shortcode, esperado):
    assert shortcode_to_media_id(shortcode) == esperado


def test_shortcode_com_caractere_invalido_e_recusado():
    with pytest.raises(ScrapeError):
        shortcode_to_media_id("abc!")
```

- [ ] **Step 2: Rode o teste e confirme que falha**

Run: `uv run pytest tests/test_scrape_targets.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'cie.scrape.targets'`

- [ ] **Step 3: Implemente `targets.py`**

> **Nota pos-execucao (commit `3c37581`).** O bloco abaixo foi implementado como
> escrito e a revisao de codigo achou defeitos reais **na propria redacao deste
> plano**, corrigidos em seguida. Se voce estiver reimplementando do zero, use
> `cie/scrape/targets.py` como referencia, nao este bloco. O que mudou:
>
> * `urlparse` vaza `ValueError` em link com colchete (`[instagram.com/x`) —
>   agora embrulhado em `ScrapeError`;
> * o guarda `"." not in texto` rejeitava handle com ponto (`cafe.canastra`),
>   que e comum — removido, com `_HOSTS` cobrindo o caso de digitar so o dominio;
> * `_HANDLE_RE` aceitava `.` e `..`, e `slug` vira nome de diretorio: `raspagem/..`
>   escapa para a raiz do repo. Agora exige comeco e fim alfanumerico, sem `..`;
> * `_TAG_RE` era denylist e passava `:` e `*`, ilegais em caminho no Windows —
>   virou allowlist `^\w{1,100}$`;
> * o shortcode de `/p/` nao era validado: `/p/../../etc/` virava `slug` `post-..`;
> * `kind` virou `ClassVar[Literal[...]]`, para nao virar campo do dataclass por
>   acidente e para permitir narrowing do union `Target`;
> * esquema nao-http (`ftp://`, `javascript://`) agora e recusado, e URL
>   protocolo-relativa (`//instagram.com/x`) passou a funcionar.
>
> Licao para as tasks seguintes: `slug` e nome de diretorio. Toda validacao que
> alimenta `slug` e defesa de path traversal, nao capricho.

Crie `cie/scrape/targets.py`:

```python
"""Traducao de um link (ou handle solto) no alvo tipado da raspagem.

Puro: nao toca rede, nao importa Playwright, nao le disco. Recebe string e
devolve alvo - e por isso da para testar o formato inteiro sem abrir browser.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse

from ..errors import ScrapeError

#: Alfabeto posicional que o Instagram usa para codificar media_id em shortcode.
SHORTCODE_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

_HANDLE_RE = re.compile(r"^[A-Za-z0-9._]{1,30}$")
_TAG_RE = re.compile(r"^[^\s/?#]{1,100}$")

#: Primeiros segmentos de caminho que o Instagram reserva - nenhum e handle.
_RESERVADOS = {
    "p", "reel", "reels", "explore", "stories", "tv", "s", "accounts",
    "direct", "about", "developer", "legal", "privacy", "web", "graphql",
    "api", "challenge", "emails", "session",
}


@dataclass(frozen=True)
class ProfileTarget:
    """Feed de um perfil."""

    handle: str

    kind = "profile"

    @property
    def slug(self) -> str:
        return self.handle


@dataclass(frozen=True)
class PostTarget:
    """Um post especifico, carrossel incluso."""

    shortcode: str

    kind = "post"

    @property
    def slug(self) -> str:
        return f"post-{self.shortcode}"


@dataclass(frozen=True)
class HashtagTarget:
    """Uma hashtag."""

    tag: str

    kind = "hashtag"

    @property
    def slug(self) -> str:
        return f"tag-{self.tag}"


Target = ProfileTarget | PostTarget | HashtagTarget


def shortcode_to_media_id(shortcode: str) -> int:
    """Converte shortcode em media_id. Deterministico - nao precisa de rede."""
    if not shortcode:
        raise ScrapeError("shortcode vazio")
    total = 0
    for char in shortcode:
        posicao = SHORTCODE_ALPHABET.find(char)
        if posicao < 0:
            raise ScrapeError(
                f"shortcode invalido: caractere {char!r} nao pertence ao "
                f"alfabeto do Instagram"
            )
        total = total * 64 + posicao
    return total


def parse_target(raw: str) -> Target:
    """Link, `@handle` ou `#tag` -> alvo tipado. Levanta `ScrapeError` no resto."""
    texto = (raw or "").strip()
    if not texto:
        raise ScrapeError("link vazio: cole a URL do perfil, do post ou da hashtag")

    if texto.startswith("@"):
        return _perfil(texto[1:])
    if texto.startswith("#"):
        return _hashtag(texto[1:])

    # Handle solto: sem barra, sem ponto, sem esquema.
    if "/" not in texto and "." not in texto and ":" not in texto:
        return _perfil(texto)

    candidato = texto if "://" in texto else f"https://{texto}"
    url = urlparse(candidato)
    host = (url.netloc or "").lower().removeprefix("www.")
    if host not in {"instagram.com", "instagr.am", "m.instagram.com"}:
        raise ScrapeError(
            f"esta ferramenta so entende links do instagram.com; recebi {host or texto!r}"
        )

    partes = [p for p in url.path.split("/") if p]
    if not partes:
        raise ScrapeError(
            "a URL nao aponta para nada: use instagram.com/<perfil>, "
            "instagram.com/p/<codigo> ou instagram.com/explore/tags/<tag>"
        )

    primeiro = partes[0].lower()

    if primeiro == "p":
        if len(partes) < 2:
            raise ScrapeError("URL de post sem codigo depois de /p/")
        return PostTarget(shortcode=partes[1])

    if primeiro in {"reel", "reels", "tv"}:
        raise ScrapeError(
            "Reel nao entra: video nao e referencia de imagem estatica, e a capa "
            "de um Reel e um frame, nao uma foto composta. Se quiser a imagem, "
            "cole o link de um post do feed (/p/<codigo>)."
        )

    if primeiro == "stories":
        raise ScrapeError("Stories nao entra: e efemero e nao tem proveniencia estavel")

    if primeiro == "explore":
        if len(partes) >= 3 and partes[1].lower() == "tags":
            return _hashtag(partes[2])
        raise ScrapeError(
            "de /explore/ so entendo hashtag: instagram.com/explore/tags/<tag>"
        )

    if primeiro in _RESERVADOS:
        raise ScrapeError(f"/{primeiro}/ nao e um perfil, e uma rota interna do Instagram")

    return _perfil(partes[0])


def _perfil(handle: str) -> ProfileTarget:
    limpo = handle.strip().strip("/")
    if not _HANDLE_RE.match(limpo):
        raise ScrapeError(
            f"handle invalido: {handle!r} (esperado ate 30 caracteres entre "
            f"letras, numeros, ponto e underscore)"
        )
    if limpo.lower() in _RESERVADOS:
        raise ScrapeError(f"{limpo!r} e uma rota interna do Instagram, nao um perfil")
    return ProfileTarget(handle=limpo)


def _hashtag(tag: str) -> HashtagTarget:
    limpo = tag.strip().strip("/").lstrip("#")
    if not _TAG_RE.match(limpo):
        raise ScrapeError(f"hashtag invalida: {tag!r}")
    return HashtagTarget(tag=limpo)
```

- [ ] **Step 4: Rode os testes e confirme que passam**

Run: `uv run pytest tests/test_scrape_targets.py -v`
Expected: todos passam (24 casos, contando os `parametrize`)

- [ ] **Step 5: Commit**

```bash
git add cie/scrape/targets.py tests/test_scrape_targets.py
git commit -m "Scrape: parse de link em alvo tipado (perfil, post, hashtag)"
```

---

## Task 3: `models.py` — `ScrapedItem` e `HarvestBatch`

**Files:**
- Create: `cie/scrape/models.py`
- Test: `tests/test_scrape_models.py`

- [ ] **Step 1: Escreva o teste que falha**

Crie `tests/test_scrape_models.py`:

```python
"""Contrato dos modelos da raspagem."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from cie.scrape.models import HarvestBatch, ScrapedItem


def _item(**over) -> ScrapedItem:
    base = dict(
        shortcode="C1a2b3c",
        owner_handle="cafecanastra",
        post_url="https://www.instagram.com/p/C1a2b3c/",
        display_url="https://scontent.cdninstagram.com/v/foto.jpg",
        width=1080,
        height=1350,
        taken_at=datetime(2026, 8, 18, 15, 30, tzinfo=timezone.utc),
        caption="colheita na fazenda",
        carousel_index=1,
        is_video=False,
    )
    base.update(over)
    return ScrapedItem(**base)


def test_item_guarda_proveniencia():
    item = _item()
    assert item.post_url.endswith("/p/C1a2b3c/")
    assert item.owner_handle == "cafecanastra"


def test_item_recusa_campo_desconhecido():
    # extra=forbid: se o Instagram mudar e alguem colar campo novo aqui,
    # o erro aparece no parser, nao tres camadas adiante.
    with pytest.raises(ValidationError):
        _item(likes=42)


def test_nome_do_arquivo_usa_data_shortcode_e_indice():
    assert _item().filename == "2026-08-18_C1a2b3c_1.jpg"


def test_nome_do_arquivo_sem_data_nao_inventa_data():
    assert _item(taken_at=None).filename == "sem-data_C1a2b3c_1.jpg"


def test_nome_do_arquivo_preserva_indice_do_carrossel():
    assert _item(carousel_index=3).filename == "2026-08-18_C1a2b3c_3.jpg"


def test_nome_do_arquivo_respeita_extensao_da_url():
    item = _item(display_url="https://scontent.cdninstagram.com/v/foto.webp?ig_cache=1")
    assert item.filename == "2026-08-18_C1a2b3c_1.webp"


def test_lote_vazio_e_valido():
    lote = HarvestBatch(
        target_slug="cafecanastra",
        target_kind="profile",
        harvested_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
    )
    assert lote.items == []
    assert lote.images == []


def test_lote_separa_imagem_de_video():
    lote = HarvestBatch(
        target_slug="cafecanastra",
        target_kind="profile",
        harvested_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
        items=[_item(), _item(shortcode="D9z", is_video=True)],
    )
    assert len(lote.items) == 2
    assert len(lote.images) == 1
    assert lote.images[0].shortcode == "C1a2b3c"
```

- [ ] **Step 2: Rode o teste e confirme que falha**

Run: `uv run pytest tests/test_scrape_models.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'cie.scrape.models'`

- [ ] **Step 3: Implemente `models.py`**

Crie `cie/scrape/models.py`:

```python
"""Modelos da raspagem.

`ScrapedItem` deliberadamente NAO tem `has_identifiable_person` nem
`consent_on_file`. Esses dois campos so existem em `Asset`, e so a curadoria
humana os preenche. A raspagem nao tem direito de opinar sobre eles.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import PurePosixPath
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field

#: Extensoes que o CDN do Instagram devolve. Fora dessa lista, cai para .jpg.
_EXTENSOES_CONHECIDAS = {".jpg", ".jpeg", ".png", ".webp", ".heic"}


class ScrapedItem(BaseModel):
    """Uma imagem colhida. Uma foto simples vira 1; um carrossel de 5 vira 5."""

    model_config = ConfigDict(extra="forbid")

    shortcode: str
    owner_handle: str = ""
    post_url: str
    display_url: str = ""
    width: int = 0
    height: int = 0
    taken_at: datetime | None = None
    caption: str = ""
    carousel_index: int = 1
    is_video: bool = False

    @property
    def extension(self) -> str:
        sufixo = PurePosixPath(urlparse(self.display_url).path).suffix.lower()
        return sufixo if sufixo in _EXTENSOES_CONHECIDAS else ".jpg"

    @property
    def filename(self) -> str:
        """`<data>_<shortcode>_<indice>.<ext>` - ordenavel e rastreavel a origem."""
        data = self.taken_at.strftime("%Y-%m-%d") if self.taken_at else "sem-data"
        return f"{data}_{self.shortcode}_{self.carousel_index}{self.extension}"


class HarvestBatch(BaseModel):
    """O resultado de parsear um envelope de colheita."""

    model_config = ConfigDict(extra="forbid")

    target_slug: str
    target_kind: str
    harvested_at: datetime
    items: list[ScrapedItem] = Field(default_factory=list)

    @property
    def images(self) -> list[ScrapedItem]:
        """So o que da para baixar como imagem estatica."""
        return [i for i in self.items if not i.is_video and i.display_url]
```

- [ ] **Step 4: Rode os testes e confirme que passam**

Run: `uv run pytest tests/test_scrape_models.py -v`
Expected: 9 passed

- [ ] **Step 5: Commit**

```bash
git add cie/scrape/models.py tests/test_scrape_models.py
git commit -m "Scrape: modelos ScrapedItem e HarvestBatch"
```

---

## Task 4: `parser.py` — objeto `media` para `ScrapedItem`

Esta task cobre o nucleo do parser: um unico objeto `media` da API v1, nos tres formatos que ele aparece (imagem simples, carrossel, video). A Task 5 cobre o envelope inteiro.

**Files:**
- Create: `cie/scrape/parser.py`
- Test: `tests/test_scrape_parser.py`

- [ ] **Step 1: Escreva o teste que falha**

Crie `tests/test_scrape_parser.py`:

```python
"""Parser do JSON do Instagram. Nenhum teste aqui toca a rede."""

from __future__ import annotations

import pytest

from cie.errors import InstagramFormatError
from cie.scrape.parser import parse_media


def _candidatos(*tamanhos):
    return {
        "candidates": [
            {"url": f"https://cdn.example/{w}x{h}.jpg", "width": w, "height": h}
            for w, h in tamanhos
        ]
    }


def _imagem():
    return {
        "code": "C1a2b3c",
        "taken_at": 1786000000,
        "media_type": 1,
        "user": {"username": "cafecanastra"},
        "caption": {"text": "colheita na fazenda"},
        "image_versions2": _candidatos((640, 800), (1080, 1350)),
    }


def test_imagem_simples_vira_um_item():
    itens = parse_media(_imagem())
    assert len(itens) == 1
    item = itens[0]
    assert item.shortcode == "C1a2b3c"
    assert item.owner_handle == "cafecanastra"
    assert item.caption == "colheita na fazenda"
    assert item.carousel_index == 1
    assert item.is_video is False
    assert item.post_url == "https://www.instagram.com/p/C1a2b3c/"


def test_escolhe_sempre_o_maior_candidato():
    # 640x800 vem primeiro na lista; queremos 1080x1350 mesmo assim.
    item = parse_media(_imagem())[0]
    assert item.width == 1080
    assert item.height == 1350
    assert item.display_url == "https://cdn.example/1080x1350.jpg"


def test_taken_at_vira_datetime_utc():
    item = parse_media(_imagem())[0]
    assert item.taken_at is not None
    assert item.taken_at.year == 2026


def test_carrossel_de_tres_vira_tres_itens_indexados():
    media = {
        "code": "C9z9z9z",
        "taken_at": 1786000000,
        "media_type": 8,
        "user": {"username": "cafecanastra"},
        "caption": {"text": "sequencia"},
        "carousel_media": [
            {"media_type": 1, "image_versions2": _candidatos((1080, 1080))},
            {"media_type": 1, "image_versions2": _candidatos((1080, 1080))},
            {"media_type": 1, "image_versions2": _candidatos((1080, 1080))},
        ],
    }
    itens = parse_media(media)
    assert [i.carousel_index for i in itens] == [1, 2, 3]
    assert all(i.shortcode == "C9z9z9z" for i in itens)
    assert all(i.caption == "sequencia" for i in itens)


def test_video_e_marcado_mas_nao_derruba_o_parser():
    media = _imagem() | {"media_type": 2}
    item = parse_media(media)[0]
    assert item.is_video is True


def test_video_sem_candidato_de_imagem_nao_levanta_erro():
    media = {
        "code": "Cvid",
        "taken_at": 1786000000,
        "media_type": 2,
        "user": {"username": "x"},
    }
    item = parse_media(media)[0]
    assert item.is_video is True
    assert item.display_url == ""


def test_carrossel_misto_marca_so_o_video():
    media = {
        "code": "Cmix",
        "media_type": 8,
        "carousel_media": [
            {"media_type": 1, "image_versions2": _candidatos((1080, 1080))},
            {"media_type": 2, "image_versions2": _candidatos((1080, 1080))},
        ],
    }
    itens = parse_media(media)
    assert [i.is_video for i in itens] == [False, True]


def test_legenda_nula_vira_string_vazia():
    media = _imagem() | {"caption": None}
    assert parse_media(media)[0].caption == ""


def test_sem_taken_at_o_parser_nao_inventa_data():
    media = {k: v for k, v in _imagem().items() if k != "taken_at"}
    assert parse_media(media)[0].taken_at is None


def test_handle_cai_para_o_fallback_quando_ausente():
    media = {k: v for k, v in _imagem().items() if k != "user"}
    item = parse_media(media, owner_fallback="cafecanastra")[0]
    assert item.owner_handle == "cafecanastra"


def test_media_sem_code_da_erro_legivel_e_nao_keyerror():
    media = {k: v for k, v in _imagem().items() if k != "code"}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo == "code"
    assert "code" in str(exc.value)


def test_imagem_sem_candidato_da_erro_legivel():
    media = {k: v for k, v in _imagem().items() if k != "image_versions2"}
    with pytest.raises(InstagramFormatError) as exc:
        parse_media(media)
    assert exc.value.campo == "image_versions2"
```

- [ ] **Step 2: Rode o teste e confirme que falha**

Run: `uv run pytest tests/test_scrape_parser.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'cie.scrape.parser'`

- [ ] **Step 3: Implemente o nucleo de `parser.py`**

Crie `cie/scrape/parser.py`:

```python
"""JSON do Instagram -> `ScrapedItem`.

Puro: recebe dict, devolve modelo. Nao sabe de onde o dict veio - do Playwright,
de um arquivo salvo, ou de trafego interceptado. E isso que torna barato trocar
a forma de colher sem tocar em nada aqui.

Regra que atravessa o modulo: formato inesperado vira `InstagramFormatError` com
o nome do campo que faltou. `KeyError` nu e proibido - o Instagram muda o JSON
sem aviso, e a mensagem precisa dizer o que mudou.
"""

from __future__ import annotations

from datetime import datetime, timezone

from ..errors import InstagramFormatError
from .models import ScrapedItem

#: media_type do Instagram: 1 imagem, 2 video, 8 carrossel.
_TIPO_VIDEO = 2


def parse_media(media: dict, *, owner_fallback: str = "") -> list[ScrapedItem]:
    """Um objeto `media` da API v1 -> um item por imagem.

    Foto simples devolve 1 item; carrossel de N devolve N, ja indexados.
    """
    if not isinstance(media, dict):
        raise InstagramFormatError(
            f"esperava objeto 'media', recebi {type(media).__name__}", campo="media"
        )

    shortcode = media.get("code")
    if not shortcode:
        raise InstagramFormatError(
            "objeto 'media' sem o campo 'code' (shortcode do post); "
            "o formato do Instagram provavelmente mudou",
            campo="code",
        )

    handle = (media.get("user") or {}).get("username") or owner_fallback
    caption = ((media.get("caption") or {}).get("text") or "").strip()
    taken_at = _timestamp(media.get("taken_at"))
    post_url = f"https://www.instagram.com/p/{shortcode}/"

    filhos = media.get("carousel_media") or [media]

    itens: list[ScrapedItem] = []
    for indice, filho in enumerate(filhos, start=1):
        is_video = filho.get("media_type") == _TIPO_VIDEO
        melhor = _melhor_candidato(filho, permitir_vazio=is_video)
        itens.append(
            ScrapedItem(
                shortcode=shortcode,
                owner_handle=handle,
                post_url=post_url,
                display_url=melhor.get("url", ""),
                width=int(melhor.get("width") or 0),
                height=int(melhor.get("height") or 0),
                taken_at=taken_at,
                caption=caption,
                carousel_index=indice,
                is_video=is_video,
            )
        )
    return itens


def _melhor_candidato(media: dict, *, permitir_vazio: bool) -> dict:
    """A maior resolucao disponivel. O Instagram nao devolve a lista ordenada."""
    candidatos = (media.get("image_versions2") or {}).get("candidates") or []
    if not candidatos:
        if permitir_vazio:
            # Video sem capa: marcamos e seguimos - o download pula videos de todo jeito.
            return {}
        raise InstagramFormatError(
            "objeto 'media' sem 'image_versions2.candidates'; sem isso nao ha "
            "URL de imagem para baixar",
            campo="image_versions2",
        )
    return max(
        candidatos,
        key=lambda c: int(c.get("width") or 0) * int(c.get("height") or 0),
    )


def _timestamp(valor) -> datetime | None:
    """`taken_at` unix -> datetime UTC. Ausente continua ausente: nao inventamos data."""
    if not valor:
        return None
    try:
        return datetime.fromtimestamp(int(valor), tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return None
```

- [ ] **Step 4: Rode os testes e confirme que passam**

Run: `uv run pytest tests/test_scrape_parser.py -v`
Expected: 13 passed

- [ ] **Step 5: Commit**

```bash
git add cie/scrape/parser.py tests/test_scrape_parser.py
git commit -m "Scrape: parser de objeto media (imagem, carrossel, video)"
```

---

## Task 5: `parser.py` — envelope de colheita completo

**Files:**
- Modify: `cie/scrape/parser.py` (append)
- Test: `tests/test_scrape_envelope.py`
- Create: `tests/fixtures/scrape/perfil.json`
- Create: `tests/fixtures/scrape/post-carrossel.json`
- Create: `tests/fixtures/scrape/hashtag.json`

O envelope e o arquivo que `harvest` grava em `raspagem/_colheita/`. Formato:

```json
{
  "target": {"kind": "profile", "slug": "cafecanastra", "handle": "cafecanastra"},
  "harvested_at": "2026-08-18T21:30:00+00:00",
  "source": "feed_user",
  "pages": [ { "items": [ ... ] } ]
}
```

- [ ] **Step 1: Crie as fixtures**

Crie `tests/fixtures/scrape/perfil.json`:

```json
{
  "target": {"kind": "profile", "slug": "cafecanastra", "handle": "cafecanastra"},
  "harvested_at": "2026-08-18T21:30:00+00:00",
  "source": "feed_user",
  "pages": [
    {
      "more_available": true,
      "next_max_id": "CURSOR_1",
      "items": [
        {
          "code": "AAA111",
          "taken_at": 1786000000,
          "media_type": 1,
          "user": {"username": "cafecanastra"},
          "caption": {"text": "cafezal ao meio-dia"},
          "image_versions2": {
            "candidates": [
              {"url": "https://cdn.example/AAA111-640.jpg", "width": 640, "height": 800},
              {"url": "https://cdn.example/AAA111-1080.jpg", "width": 1080, "height": 1350}
            ]
          }
        },
        {
          "code": "BBB222",
          "taken_at": 1786086400,
          "media_type": 8,
          "user": {"username": "cafecanastra"},
          "caption": {"text": "sequencia da torrefacao"},
          "carousel_media": [
            {
              "media_type": 1,
              "image_versions2": {
                "candidates": [
                  {"url": "https://cdn.example/BBB222-1.jpg", "width": 1080, "height": 1080}
                ]
              }
            },
            {
              "media_type": 1,
              "image_versions2": {
                "candidates": [
                  {"url": "https://cdn.example/BBB222-2.jpg", "width": 1080, "height": 1080}
                ]
              }
            }
          ]
        }
      ]
    },
    {
      "more_available": false,
      "items": [
        {
          "code": "CCC333",
          "taken_at": 1786172800,
          "media_type": 2,
          "user": {"username": "cafecanastra"},
          "caption": {"text": "video da colheita"},
          "image_versions2": {
            "candidates": [
              {"url": "https://cdn.example/CCC333-capa.jpg", "width": 1080, "height": 1920}
            ]
          }
        }
      ]
    }
  ]
}
```

Crie `tests/fixtures/scrape/post-carrossel.json`:

```json
{
  "target": {"kind": "post", "slug": "post-DDD444", "shortcode": "DDD444"},
  "harvested_at": "2026-08-18T21:35:00+00:00",
  "source": "media_info",
  "pages": [
    {
      "items": [
        {
          "code": "DDD444",
          "taken_at": 1786000000,
          "media_type": 8,
          "user": {"username": "terceiro"},
          "caption": {"text": "tres angulos"},
          "carousel_media": [
            {
              "media_type": 1,
              "image_versions2": {
                "candidates": [
                  {"url": "https://cdn.example/DDD444-1.webp", "width": 1080, "height": 1350}
                ]
              }
            },
            {
              "media_type": 1,
              "image_versions2": {
                "candidates": [
                  {"url": "https://cdn.example/DDD444-2.webp", "width": 1080, "height": 1350}
                ]
              }
            },
            {
              "media_type": 1,
              "image_versions2": {
                "candidates": [
                  {"url": "https://cdn.example/DDD444-3.webp", "width": 1080, "height": 1350}
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

Crie `tests/fixtures/scrape/hashtag.json`:

```json
{
  "target": {"kind": "hashtag", "slug": "tag-cafeespecial", "tag": "cafeespecial"},
  "harvested_at": "2026-08-18T21:40:00+00:00",
  "source": "tag_web_info",
  "pages": [
    {
      "data": {
        "top": {
          "sections": [
            {
              "layout_content": {
                "medias": [
                  {
                    "media": {
                      "code": "EEE555",
                      "taken_at": 1786000000,
                      "media_type": 1,
                      "user": {"username": "outro_perfil"},
                      "caption": {"text": "meu cafe da manha"},
                      "image_versions2": {
                        "candidates": [
                          {"url": "https://cdn.example/EEE555.jpg", "width": 1080, "height": 1080}
                        ]
                      }
                    }
                  }
                ]
              }
            }
          ]
        },
        "recent": {
          "sections": [
            {
              "layout_content": {
                "medias": [
                  {
                    "media": {
                      "code": "FFF666",
                      "taken_at": 1786086400,
                      "media_type": 1,
                      "user": {"username": "mais_um"},
                      "caption": null,
                      "image_versions2": {
                        "candidates": [
                          {"url": "https://cdn.example/FFF666.jpg", "width": 1080, "height": 1080}
                        ]
                      }
                    }
                  }
                ]
              }
            },
            {
              "layout_content": {
                "one_by_two_item": {"clips": {"items": [{"media": {"code": "IGNORAR"}}]}}
              }
            }
          ]
        }
      }
    }
  ]
}
```

- [ ] **Step 2: Escreva o teste que falha**

Crie `tests/test_scrape_envelope.py`:

```python
"""Envelope de colheita -> HarvestBatch. Fixtures, nenhuma rede."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cie.errors import InstagramFormatError
from cie.scrape.parser import parse_envelope

FIXTURES = Path(__file__).parent / "fixtures" / "scrape"


def _carrega(nome: str) -> dict:
    return json.loads((FIXTURES / f"{nome}.json").read_text(encoding="utf-8"))


def test_perfil_junta_todas_as_paginas():
    lote = parse_envelope(_carrega("perfil"))
    assert lote.target_kind == "profile"
    assert lote.target_slug == "cafecanastra"
    # AAA111 (1) + BBB222 carrossel (2) + CCC333 video (1) = 4 itens
    assert len(lote.items) == 4
    assert [i.shortcode for i in lote.items] == ["AAA111", "BBB222", "BBB222", "CCC333"]


def test_perfil_separa_video_do_que_da_para_baixar():
    lote = parse_envelope(_carrega("perfil"))
    assert len(lote.images) == 3
    assert all(not i.is_video for i in lote.images)


def test_perfil_preserva_o_carimbo_de_colheita():
    lote = parse_envelope(_carrega("perfil"))
    assert lote.harvested_at.year == 2026
    assert lote.harvested_at.month == 8


def test_post_carrossel_vira_tres_itens():
    lote = parse_envelope(_carrega("post-carrossel"))
    assert lote.target_kind == "post"
    assert len(lote.items) == 3
    assert [i.carousel_index for i in lote.items] == [1, 2, 3]
    assert lote.items[0].extension == ".webp"


def test_hashtag_le_top_e_recent():
    lote = parse_envelope(_carrega("hashtag"))
    assert lote.target_kind == "hashtag"
    assert lote.target_slug == "tag-cafeespecial"
    assert {i.shortcode for i in lote.items} == {"EEE555", "FFF666"}


def test_hashtag_ignora_secao_de_clips():
    # A secao one_by_two_item/clips e video em formato diferente; nao entra.
    lote = parse_envelope(_carrega("hashtag"))
    assert "IGNORAR" not in {i.shortcode for i in lote.items}


def test_hashtag_usa_o_dono_de_cada_post_nao_o_alvo():
    lote = parse_envelope(_carrega("hashtag"))
    assert {i.owner_handle for i in lote.items} == {"outro_perfil", "mais_um"}


def test_envelope_sem_target_da_erro_legivel():
    with pytest.raises(InstagramFormatError) as exc:
        parse_envelope({"pages": []})
    assert exc.value.campo == "target"


def test_envelope_com_kind_desconhecido_da_erro_legivel():
    envelope = {
        "target": {"kind": "marciano", "slug": "x"},
        "harvested_at": "2026-08-18T00:00:00+00:00",
        "pages": [],
    }
    with pytest.raises(InstagramFormatError) as exc:
        parse_envelope(envelope)
    assert "marciano" in str(exc.value)


def test_envelope_sem_paginas_vira_lote_vazio_e_nao_erro():
    envelope = {
        "target": {"kind": "profile", "slug": "vazio", "handle": "vazio"},
        "harvested_at": "2026-08-18T00:00:00+00:00",
        "pages": [],
    }
    lote = parse_envelope(envelope)
    assert lote.items == []
```

- [ ] **Step 3: Rode o teste e confirme que falha**

Run: `uv run pytest tests/test_scrape_envelope.py -v`
Expected: FAIL com `ImportError: cannot import name 'parse_envelope'`

- [ ] **Step 4: Implemente `parse_envelope`**

Acrescente ao final de `cie/scrape/parser.py`:

```python
def parse_envelope(envelope: dict) -> HarvestBatch:
    """O arquivo de `raspagem/_colheita/` -> lote parseado.

    Aceita qualquer envelope no formato gravado por `harvest`, venha ele do
    Playwright ou de um arquivo antigo em disco.
    """
    alvo = envelope.get("target")
    if not isinstance(alvo, dict) or not alvo.get("kind"):
        raise InstagramFormatError(
            "envelope sem 'target.kind'; nao da para saber como ler as paginas",
            campo="target",
        )

    kind = alvo["kind"]
    if kind not in _EXTRATORES:
        raise InstagramFormatError(
            f"alvo de tipo desconhecido: {kind!r} "
            f"(esperado um de {sorted(_EXTRATORES)})",
            campo="target.kind",
        )

    fallback = alvo.get("handle", "")
    extrator = _EXTRATORES[kind]

    itens: list[ScrapedItem] = []
    for pagina in envelope.get("pages") or []:
        for media in extrator(pagina):
            itens.extend(parse_media(media, owner_fallback=fallback))

    return HarvestBatch(
        target_slug=alvo.get("slug") or kind,
        target_kind=kind,
        harvested_at=_colhido_em(envelope.get("harvested_at")),
        items=itens,
    )


def _medias_de_feed(pagina: dict) -> list[dict]:
    """`/api/v1/feed/user/<id>/` e `/api/v1/media/<id>/info/` devolvem `items`."""
    return [m for m in (pagina.get("items") or []) if isinstance(m, dict)]


def _medias_de_hashtag(pagina: dict) -> list[dict]:
    """`/api/v1/tags/web_info/` empacota em secoes, divididas em `top` e `recent`.

    Secoes de clips (`one_by_two_item`) sao video em outro formato e ficam de fora.
    """
    dados = pagina.get("data") or {}
    encontrados: list[dict] = []
    for bloco in ("top", "recent"):
        for secao in (dados.get(bloco) or {}).get("sections") or []:
            conteudo = (secao.get("layout_content") or {}).get("medias") or []
            for entrada in conteudo:
                media = (entrada or {}).get("media")
                if isinstance(media, dict):
                    encontrados.append(media)
    return encontrados


_EXTRATORES = {
    "profile": _medias_de_feed,
    "post": _medias_de_feed,
    "hashtag": _medias_de_hashtag,
}


def _colhido_em(valor) -> datetime:
    if isinstance(valor, str) and valor:
        try:
            return datetime.fromisoformat(valor)
        except ValueError:
            pass
    return datetime.now(tz=timezone.utc)
```

Acrescente `HarvestBatch` ao import de `.models` no topo do arquivo:

```python
from .models import HarvestBatch, ScrapedItem
```

- [ ] **Step 5: Rode os testes e confirme que passam**

Run: `uv run pytest tests/test_scrape_envelope.py tests/test_scrape_parser.py -v`
Expected: 23 passed

- [ ] **Step 6: Commit**

```bash
git add cie/scrape/parser.py tests/test_scrape_envelope.py tests/fixtures/scrape/
git commit -m "Scrape: parse do envelope de colheita para perfil, post e hashtag"
```

---

## Task 6: `download.py` — baixar um item com sidecar

**Files:**
- Create: `cie/scrape/download.py`
- Test: `tests/test_scrape_download.py`

- [ ] **Step 1: Escreva o teste que falha**

Crie `tests/test_scrape_download.py`:

```python
"""Download, dedupe e sidecar. httpx nunca e chamado de verdade aqui."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from cie.scrape.download import DownloadReport, download_batch
from cie.scrape.models import HarvestBatch, ScrapedItem


def _item(shortcode="AAA111", indice=1, url=None, is_video=False) -> ScrapedItem:
    return ScrapedItem(
        shortcode=shortcode,
        owner_handle="cafecanastra",
        post_url=f"https://www.instagram.com/p/{shortcode}/",
        display_url=url or f"https://cdn.example/{shortcode}-{indice}.jpg",
        width=1080,
        height=1350,
        taken_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
        caption="legenda",
        carousel_index=indice,
        is_video=is_video,
    )


def _lote(*itens) -> HarvestBatch:
    return HarvestBatch(
        target_slug="cafecanastra",
        target_kind="profile",
        harvested_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
        items=list(itens),
    )


def _buscador(mapa: dict[str, bytes]):
    """Substitui httpx: URL -> bytes. Registra o que foi pedido."""
    pedidos: list[str] = []

    def buscar(url: str) -> bytes:
        pedidos.append(url)
        if url not in mapa:
            raise RuntimeError(f"404 {url}")
        return mapa[url]

    buscar.pedidos = pedidos
    return buscar


def test_baixa_e_grava_arquivo_com_nome_previsivel(tmp_path: Path):
    item = _item()
    buscar = _buscador({item.display_url: b"conteudo-da-foto"})

    relatorio = download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)

    destino = tmp_path / "cafecanastra" / "2026-08-18_AAA111_1.jpg"
    assert destino.is_file()
    assert destino.read_bytes() == b"conteudo-da-foto"
    assert relatorio.baixados == 1


def test_sidecar_guarda_proveniencia_completa(tmp_path: Path):
    item = _item()
    buscar = _buscador({item.display_url: b"conteudo-da-foto"})

    download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)

    sidecar = tmp_path / "cafecanastra" / "2026-08-18_AAA111_1.json"
    dados = json.loads(sidecar.read_text(encoding="utf-8"))
    assert dados["post_url"] == "https://www.instagram.com/p/AAA111/"
    assert dados["owner_handle"] == "cafecanastra"
    assert dados["shortcode"] == "AAA111"
    assert dados["carousel_index"] == 1
    assert dados["source_url"] == item.display_url
    assert dados["width"] == 1080
    assert len(dados["sha256"]) == 64
    assert dados["scraped_at"]
    # A raspagem nao opina sobre pessoa nem consentimento - isso e da curadoria.
    assert "has_identifiable_person" not in dados
    assert "consent_on_file" not in dados


def test_video_nunca_e_baixado(tmp_path: Path):
    item = _item(is_video=True)
    buscar = _buscador({item.display_url: b"capa-de-video"})

    relatorio = download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)

    assert buscar.pedidos == []
    assert relatorio.baixados == 0
    assert relatorio.videos_pulados == 1


def test_conteudo_repetido_e_pulado_por_sha256(tmp_path: Path):
    # Dois shortcodes diferentes, mesmo byte a byte: so um arquivo sobrevive.
    a = _item(shortcode="AAA111")
    b = _item(shortcode="BBB222")
    buscar = _buscador({a.display_url: b"identico", b.display_url: b"identico"})

    relatorio = download_batch(_lote(a, b), out_root=tmp_path, fetch=buscar, delay=0)

    assert relatorio.baixados == 1
    assert relatorio.duplicados == 1
    assert len(list((tmp_path / "cafecanastra").glob("*.jpg"))) == 1


def test_dedupe_atravessa_execucoes(tmp_path: Path):
    item = _item()
    buscar = _buscador({item.display_url: b"identico"})

    download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)
    segundo = download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)

    assert segundo.baixados == 0
    assert segundo.duplicados == 1


def test_nada_sobrescreve_arquivo_existente(tmp_path: Path):
    destino = tmp_path / "cafecanastra" / "2026-08-18_AAA111_1.jpg"
    destino.parent.mkdir(parents=True)
    destino.write_bytes(b"ja-estava-aqui")

    item = _item()
    buscar = _buscador({item.display_url: b"conteudo-novo"})
    relatorio = download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)

    assert destino.read_bytes() == b"ja-estava-aqui"
    assert relatorio.baixados == 1
    # o novo entrou com sufixo, sem destruir o que existia
    assert (tmp_path / "cafecanastra" / "2026-08-18_AAA111_1-2.jpg").is_file()


def test_dry_run_nao_escreve_nada(tmp_path: Path):
    item = _item()
    buscar = _buscador({item.display_url: b"conteudo"})

    relatorio = download_batch(
        _lote(item), out_root=tmp_path, fetch=buscar, delay=0, dry_run=True
    )

    assert buscar.pedidos == []
    assert list(tmp_path.rglob("*.jpg")) == []
    assert relatorio.dry_run is True
    assert relatorio.previstos == 1


def test_falha_de_rede_nao_derruba_o_lote(tmp_path: Path):
    bom = _item(shortcode="AAA111")
    ruim = _item(shortcode="BBB222")
    buscar = _buscador({bom.display_url: b"ok"})  # o de BBB222 vai levantar

    relatorio = download_batch(_lote(bom, ruim), out_root=tmp_path, fetch=buscar, delay=0)

    assert relatorio.baixados == 1
    assert relatorio.erros == 1
    assert "BBB222" in relatorio.mensagens_de_erro()[0]


def test_limit_corta_o_lote(tmp_path: Path):
    itens = [_item(shortcode=f"S{i}") for i in range(5)]
    buscar = _buscador({i.display_url: f"foto-{i.shortcode}".encode() for i in itens})

    relatorio = download_batch(_lote(*itens), out_root=tmp_path, fetch=buscar, delay=0, limit=2)

    assert relatorio.baixados == 2


def test_manifest_do_lote_e_gravado(tmp_path: Path):
    item = _item()
    buscar = _buscador({item.display_url: b"conteudo"})

    download_batch(_lote(item), out_root=tmp_path, fetch=buscar, delay=0)

    manifest = json.loads((tmp_path / "_manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["arquivos"]) == 1
    registro = manifest["arquivos"][0]
    assert registro["path"] == "cafecanastra/2026-08-18_AAA111_1.jpg"
    assert len(registro["sha256"]) == 64


def test_manifest_acumula_entre_execucoes(tmp_path: Path):
    a = _item(shortcode="AAA111")
    b = _item(shortcode="BBB222")
    download_batch(_lote(a), out_root=tmp_path, fetch=_buscador({a.display_url: b"a"}), delay=0)
    download_batch(_lote(b), out_root=tmp_path, fetch=_buscador({b.display_url: b"b"}), delay=0)

    manifest = json.loads((tmp_path / "_manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["arquivos"]) == 2


def test_relatorio_vazio_e_valido(tmp_path: Path):
    relatorio = download_batch(_lote(), out_root=tmp_path, fetch=_buscador({}), delay=0)
    assert isinstance(relatorio, DownloadReport)
    assert relatorio.baixados == 0
```

- [ ] **Step 2: Rode o teste e confirme que falha**

Run: `uv run pytest tests/test_scrape_download.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'cie.scrape.download'`

- [ ] **Step 3: Implemente `download.py`**

Crie `cie/scrape/download.py`:

```python
"""Download das imagens colhidas, com dedupe e proveniencia.

Tres regras que nao se negociam:

  * video nunca e baixado;
  * todo arquivo nasce com sidecar - arquivo sem sidecar e bug;
  * nada sobrescreve nada, e conteudo repetido (sha256) e pulado.

`fetch` e injetavel para que o teste rode sem tocar a rede. O padrao usa httpx,
importado sob demanda.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .models import HarvestBatch, ScrapedItem

#: Sem User-Agent de browser e sem Referer, o CDN do Instagram devolve 403.
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.instagram.com/",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
}

Fetcher = Callable[[str], bytes]


@dataclass
class ItemOutcome:
    item: ScrapedItem
    status: str  # baixado | duplicado | video | erro | previsto
    path: Path | None = None
    sha256: str = ""
    motivo: str = ""


@dataclass
class DownloadReport:
    out_root: Path
    dry_run: bool = False
    outcomes: list[ItemOutcome] = field(default_factory=list)

    def _com_status(self, status: str) -> list[ItemOutcome]:
        return [o for o in self.outcomes if o.status == status]

    @property
    def baixados(self) -> int:
        return len(self._com_status("baixado"))

    @property
    def duplicados(self) -> int:
        return len(self._com_status("duplicado"))

    @property
    def videos_pulados(self) -> int:
        return len(self._com_status("video"))

    @property
    def erros(self) -> int:
        return len(self._com_status("erro"))

    @property
    def previstos(self) -> int:
        return len(self._com_status("previsto"))

    def mensagens_de_erro(self) -> list[str]:
        return [f"{o.item.shortcode}: {o.motivo}" for o in self._com_status("erro")]


def download_batch(
    batch: HarvestBatch,
    *,
    out_root: Path,
    fetch: Fetcher | None = None,
    limit: int = 0,
    delay: float = 1.0,
    dry_run: bool = False,
) -> DownloadReport:
    """Baixa as imagens de um lote. `limit=0` significa sem teto."""
    out_root = Path(out_root)
    buscar = fetch or _httpx_fetch
    relatorio = DownloadReport(out_root=out_root, dry_run=dry_run)

    destino_dir = out_root / batch.target_slug
    conhecidos = _hashes_existentes(out_root)
    baixados = 0

    for item in batch.items:
        if item.is_video or not item.display_url:
            relatorio.outcomes.append(
                ItemOutcome(item=item, status="video", motivo="video nao vira referencia")
            )
            continue

        if limit and baixados >= limit:
            break

        if dry_run:
            relatorio.outcomes.append(
                ItemOutcome(item=item, status="previsto", path=destino_dir / item.filename)
            )
            baixados += 1
            continue

        try:
            conteudo = buscar(item.display_url)
        except Exception as exc:  # noqa: BLE001 - falha de um item nao derruba o lote
            relatorio.outcomes.append(
                ItemOutcome(item=item, status="erro", motivo=str(exc))
            )
            continue

        digest = hashlib.sha256(conteudo).hexdigest()
        if digest in conhecidos:
            relatorio.outcomes.append(
                ItemOutcome(
                    item=item,
                    status="duplicado",
                    sha256=digest,
                    motivo="conteudo identico ja esta em raspagem/",
                )
            )
            continue

        destino = _caminho_livre(destino_dir, item.filename)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(conteudo)
        _grava_sidecar(destino, item, digest)

        conhecidos.add(digest)
        baixados += 1
        relatorio.outcomes.append(
            ItemOutcome(item=item, status="baixado", path=destino, sha256=digest)
        )

        if delay:
            time.sleep(delay)

    if not dry_run:
        _atualiza_manifest(out_root, relatorio)

    return relatorio


def _httpx_fetch(url: str) -> bytes:
    import httpx

    resposta = httpx.get(url, headers=_HEADERS, timeout=30.0, follow_redirects=True)
    resposta.raise_for_status()
    return resposta.content


def _hashes_existentes(out_root: Path) -> set[str]:
    """Le os sidecars ja em disco. E por isso que sidecar e obrigatorio."""
    conhecidos: set[str] = set()
    if not out_root.is_dir():
        return conhecidos
    for sidecar in out_root.rglob("*.json"):
        if sidecar.name.startswith("_"):
            continue
        try:
            dados = json.loads(sidecar.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        digest = dados.get("sha256")
        if digest:
            conhecidos.add(digest)
    return conhecidos


def _caminho_livre(pasta: Path, nome: str) -> Path:
    """Nunca sobrescreve: se o nome existe, sufixa -2, -3, ..."""
    destino = pasta / nome
    if not destino.exists():
        return destino
    base, sufixo = destino.stem, destino.suffix
    contador = 2
    while True:
        candidato = pasta / f"{base}-{contador}{sufixo}"
        if not candidato.exists():
            return candidato
        contador += 1


def _grava_sidecar(destino: Path, item: ScrapedItem, digest: str) -> None:
    sidecar = destino.with_suffix(".json")
    dados = {
        "post_url": item.post_url,
        "owner_handle": item.owner_handle,
        "shortcode": item.shortcode,
        "carousel_index": item.carousel_index,
        "source_url": item.display_url,
        "width": item.width,
        "height": item.height,
        "taken_at": item.taken_at.isoformat() if item.taken_at else None,
        "caption": item.caption,
        "sha256": digest,
        "scraped_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    sidecar.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")


def _atualiza_manifest(out_root: Path, relatorio: DownloadReport) -> None:
    """Indice acumulado de tudo sob `raspagem/`, chaveado por sha256."""
    caminho = out_root / "_manifest.json"
    registros: dict[str, dict] = {}
    if caminho.is_file():
        try:
            antigo = json.loads(caminho.read_text(encoding="utf-8"))
            for registro in antigo.get("arquivos", []):
                registros[registro["sha256"]] = registro
        except (OSError, json.JSONDecodeError, KeyError):
            registros = {}

    for outcome in relatorio.outcomes:
        if outcome.status != "baixado" or outcome.path is None:
            continue
        registros[outcome.sha256] = {
            "path": outcome.path.relative_to(out_root).as_posix(),
            "sha256": outcome.sha256,
            "post_url": outcome.item.post_url,
            "owner_handle": outcome.item.owner_handle,
        }

    caminho.parent.mkdir(parents=True, exist_ok=True)
    conteudo = {
        "atualizado_em": datetime.now(tz=timezone.utc).isoformat(),
        "arquivos": sorted(registros.values(), key=lambda r: r["path"]),
    }
    caminho.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
```

- [ ] **Step 4: Rode os testes e confirme que passam**

Run: `uv run pytest tests/test_scrape_download.py -v`
Expected: 12 passed

- [ ] **Step 5: Rode a suite inteira**

Run: `uv run pytest`
Expected: tudo passa

- [ ] **Step 6: Commit**

```bash
git add cie/scrape/download.py tests/test_scrape_download.py
git commit -m "Scrape: download com dedupe sha256, sidecar de proveniencia e manifest"
```

---

## Task 7: Snippets JS e o carregador

**Files:**
- Create: `cie/scrape/js/appid.js`
- Create: `cie/scrape/js/profile.js`
- Create: `cie/scrape/js/post.js`
- Create: `cie/scrape/js/hashtag.js`
- Create: `cie/scrape/browser.py` (so o carregador nesta task)
- Test: `tests/test_scrape_js.py`
- Modify: `pyproject.toml` (incluir os `.js` no pacote)

Os snippets ficam em arquivo `.js` e nao em string dentro do Python porque sao a parte que mais vai quebrar quando o Instagram mudar. Tem que dar para abrir, ler e consertar um deles sozinho.

Todos recebem `appId` como parametro em vez de descobrir sozinhos — assim a leitura do `X-IG-App-ID` vive num lugar so.

- [ ] **Step 1: Escreva o teste que falha**

Crie `tests/test_scrape_js.py`:

```python
"""Os snippets precisam existir, ser carregaveis e ter a forma que o evaluate espera."""

from __future__ import annotations

import pytest

from cie.errors import ScrapeError
from cie.scrape.browser import SNIPPETS, load_snippet


@pytest.mark.parametrize("nome", ["appid", "profile", "post", "hashtag"])
def test_snippet_carrega(nome):
    codigo = load_snippet(nome)
    assert codigo.strip()


@pytest.mark.parametrize("nome", ["profile", "post", "hashtag"])
def test_snippet_de_colheita_e_funcao_que_recebe_params(nome):
    # page.evaluate() exige uma expressao que avalie para funcao.
    codigo = load_snippet(nome).strip()
    assert codigo.startswith("async (params)")


def test_todo_snippet_declarado_existe_em_disco():
    for nome in SNIPPETS:
        assert load_snippet(nome).strip()


def test_snippet_inexistente_da_erro_legivel():
    with pytest.raises(ScrapeError) as exc:
        load_snippet("nao-existe")
    assert "nao-existe" in str(exc.value)


def test_snippets_de_colheita_devolvem_pages():
    for nome in ("profile", "post", "hashtag"):
        assert "pages" in load_snippet(nome)


def test_snippets_usam_o_appid_recebido_e_nao_um_literal():
    for nome in ("profile", "post", "hashtag"):
        codigo = load_snippet(nome)
        assert "params.appId" in codigo or "appId" in codigo
```

- [ ] **Step 2: Rode o teste e confirme que falha**

Run: `uv run pytest tests/test_scrape_js.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'cie.scrape.browser'`

- [ ] **Step 3: Crie `cie/scrape/js/appid.js`**

Atencao ao formato: o arquivo precisa comecar com a propria funcao. Comentario
antes dela atrapalha a deteccao de funcao do `page.evaluate()`, entao todo
comentario vive DENTRO do corpo.

```javascript
() => {
  // Le o X-IG-App-ID que a propria pagina usa nas chamadas dela.
  // A constante de fallback e o app id publico do Instagram Web; se o Instagram
  // trocar, o regex acha o novo antes de a constante ser usada.
  const html = document.documentElement.innerHTML;
  const padroes = [
    /"X-IG-App-ID"\s*:\s*"(\d+)"/,
    /appId["']?\s*[:=]\s*["'](\d{10,})["']/,
    /APP_ID["']?\s*[:=]\s*["'](\d{10,})["']/,
  ];
  for (const padrao of padroes) {
    const achado = html.match(padrao);
    if (achado) return achado[1];
  }
  return "936619743392459";
}
```

- [ ] **Step 4: Crie `cie/scrape/js/profile.js`**

```javascript
async (params) => {
  // Colhe o feed de um perfil.
  // params: {appId, handle, limit}   limit === 0 significa "tudo".
  // Retorna: {source, handle, userId, pages} ou {error}.
  const headers = {
    "X-IG-App-ID": params.appId,
    "X-Requested-With": "XMLHttpRequest",
  };
  const pedir = async (url) => {
    const resposta = await fetch(url, { headers, credentials: "include" });
    if (!resposta.ok) {
      throw new Error(`HTTP ${resposta.status} em ${url}`);
    }
    return resposta.json();
  };

  try {
    const perfil = await pedir(
      `/api/v1/users/web_profile_info/?username=${encodeURIComponent(params.handle)}`
    );
    const userId = perfil?.data?.user?.id;
    if (!userId) {
      return {
        error:
          `perfil @${params.handle} nao encontrado, ou a sessao nao esta logada. ` +
          `Rode 'cie scrape login' e tente de novo.`,
      };
    }

    const pages = [];
    let colhidos = 0;
    let maxId = null;

    while (params.limit === 0 || colhidos < params.limit) {
      const restante = params.limit === 0 ? 12 : Math.min(12, params.limit - colhidos);
      let url = `/api/v1/feed/user/${userId}/?count=${restante}`;
      if (maxId) url += `&max_id=${encodeURIComponent(maxId)}`;

      const pagina = await pedir(url);
      const itens = pagina.items || [];
      if (itens.length === 0) break;

      pages.push(pagina);
      colhidos += itens.length;

      if (!pagina.more_available || !pagina.next_max_id) break;
      maxId = pagina.next_max_id;

      // Pausa entre paginas: raspagem sem respiro rende bloqueio temporario.
      await new Promise((r) => setTimeout(r, 1200));
    }

    return { source: "feed_user", handle: params.handle, userId, pages };
  } catch (erro) {
    return { error: String(erro && erro.message ? erro.message : erro) };
  }
}
```

- [ ] **Step 5: Crie `cie/scrape/js/post.js`**

```javascript
async (params) => {
  // Colhe um post pelo media_id (derivado do shortcode no lado Python).
  // params: {appId, mediaId}
  // Retorna: {source, pages} ou {error}.
  const headers = {
    "X-IG-App-ID": params.appId,
    "X-Requested-With": "XMLHttpRequest",
  };
  try {
    const resposta = await fetch(`/api/v1/media/${params.mediaId}/info/`, {
      headers,
      credentials: "include",
    });
    if (!resposta.ok) {
      return {
        error:
          `HTTP ${resposta.status} ao buscar o post. Post privado, apagado, ` +
          `ou a sessao nao esta logada.`,
      };
    }
    const pagina = await resposta.json();
    return { source: "media_info", pages: [pagina] };
  } catch (erro) {
    return { error: String(erro && erro.message ? erro.message : erro) };
  }
}
```

- [ ] **Step 6: Crie `cie/scrape/js/hashtag.js`**

```javascript
async (params) => {
  // Colhe uma hashtag (secoes "top" e "recent").
  // params: {appId, tag}
  // Retorna: {source, pages} ou {error}.
  const headers = {
    "X-IG-App-ID": params.appId,
    "X-Requested-With": "XMLHttpRequest",
  };
  try {
    const resposta = await fetch(
      `/api/v1/tags/web_info/?tag_name=${encodeURIComponent(params.tag)}`,
      { headers, credentials: "include" }
    );
    if (!resposta.ok) {
      return {
        error:
          `HTTP ${resposta.status} ao buscar #${params.tag}. Hashtag inexistente, ` +
          `bloqueada pelo Instagram, ou a sessao nao esta logada.`,
      };
    }
    const pagina = await resposta.json();
    return { source: "tag_web_info", pages: [pagina] };
  } catch (erro) {
    return { error: String(erro && erro.message ? erro.message : erro) };
  }
}
```

- [ ] **Step 7: Crie `cie/scrape/browser.py` com o carregador**

Nesta task o modulo tem so o carregador de snippet. O Playwright entra na Task 8.

```python
"""Fronteira com o mundo: Playwright sobre um perfil de Chrome persistente.

Fino de proposito. Abre o perfil, executa um snippet, devolve o JSON cru. Nada
aqui interpreta resposta do Instagram - isso e trabalho do `parser`, que e puro
e testavel. Este modulo nao tem teste automatizado justamente por ser a fronteira;
a verificacao dele e manual, via `cie scrape status`.
"""

from __future__ import annotations

from pathlib import Path

from ..errors import ScrapeError

JS_DIR = Path(__file__).parent / "js"

#: Snippets que precisam existir em disco para a raspagem funcionar.
SNIPPETS = ("appid", "profile", "post", "hashtag")


def load_snippet(nome: str) -> str:
    """Le um snippet de `js/`. Snippet ausente e erro de instalacao, nao de rede."""
    caminho = JS_DIR / f"{nome}.js"
    if not caminho.is_file():
        raise ScrapeError(
            f"snippet {nome!r} nao encontrado em {JS_DIR}; instalacao incompleta"
        )
    return caminho.read_text(encoding="utf-8")
```

- [ ] **Step 8: Garanta que os `.js` entram no pacote instalado**

Em `pyproject.toml`, logo abaixo de `[tool.hatch.build.targets.wheel]`:

```toml
[tool.hatch.build.targets.wheel.force-include]
"cie/scrape/js" = "cie/scrape/js"
```

- [ ] **Step 9: Rode os testes e confirme que passam**

Run: `uv run pytest tests/test_scrape_js.py -v`
Expected: 12 passed

- [ ] **Step 10: Commit**

```bash
git add cie/scrape/js/ cie/scrape/browser.py tests/test_scrape_js.py pyproject.toml
git commit -m "Scrape: snippets JS de colheita e carregador"
```

---

## Task 8: `browser.py` — Playwright com perfil persistente

**Files:**
- Modify: `cie/scrape/browser.py` (append)
- Test: `tests/test_scrape_browser.py`

Playwright em si nao e testado — e a fronteira com o mundo. O que se testa e o comportamento quando ele **nao esta instalado**, porque essa e a falha que o usuario vai encontrar primeiro.

- [ ] **Step 1: Escreva o teste que falha**

Crie `tests/test_scrape_browser.py`:

```python
"""Do browser so testamos o que nao depende do browser."""

from __future__ import annotations

import builtins
from pathlib import Path

import pytest

from cie.errors import ScrapeError
from cie.scrape import browser


def test_perfil_padrao_fica_dentro_do_cie_home(tmp_path: Path):
    assert browser.profile_dir(tmp_path / ".cie") == tmp_path / ".cie" / "browser-profile"


def test_playwright_ausente_da_instrucao_de_instalacao(monkeypatch: pytest.MonkeyPatch):
    real_import = builtins.__import__

    def sem_playwright(nome, *args, **kwargs):
        if nome.startswith("playwright"):
            raise ModuleNotFoundError("No module named 'playwright'")
        return real_import(nome, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", sem_playwright)

    with pytest.raises(ScrapeError) as exc:
        browser._require_playwright()

    assert "--extra scrape" in str(exc.value)


def test_run_snippet_propaga_erro_devolvido_pelo_js():
    class PageFalsa:
        def evaluate(self, codigo, params=None):
            return {"error": "sessao nao esta logada"}

    with pytest.raises(ScrapeError) as exc:
        browser.run_snippet(PageFalsa(), "profile", {"appId": "1", "handle": "x", "limit": 1})

    assert "sessao nao esta logada" in str(exc.value)


def test_run_snippet_devolve_o_json_quando_da_certo():
    class PageFalsa:
        def evaluate(self, codigo, params=None):
            return {"source": "feed_user", "pages": [{"items": []}]}

    resultado = browser.run_snippet(PageFalsa(), "profile", {"appId": "1"})
    assert resultado["source"] == "feed_user"


def test_run_snippet_recusa_resposta_que_nao_e_objeto():
    class PageFalsa:
        def evaluate(self, codigo, params=None):
            return None

    with pytest.raises(ScrapeError):
        browser.run_snippet(PageFalsa(), "profile", {"appId": "1"})


def test_sessao_logada_detectada_pelo_cookie_sessionid():
    class ContextoFalso:
        def cookies(self, url=None):
            return [{"name": "sessionid", "value": "abc123"}]

    class PageFalsa:
        context = ContextoFalso()

    assert browser.is_logged_in(PageFalsa()) is True


def test_sessao_sem_sessionid_e_considerada_deslogada():
    class ContextoFalso:
        def cookies(self, url=None):
            return [{"name": "csrftoken", "value": "xyz"}, {"name": "sessionid", "value": ""}]

    class PageFalsa:
        context = ContextoFalso()

    assert browser.is_logged_in(PageFalsa()) is False
```

- [ ] **Step 2: Rode o teste e confirme que falha**

Run: `uv run pytest tests/test_scrape_browser.py -v`
Expected: FAIL com `AttributeError: module 'cie.scrape.browser' has no attribute 'profile_dir'`

- [ ] **Step 3: Implemente o resto de `browser.py`**

Acrescente ao final de `cie/scrape/browser.py`:

```python
INSTAGRAM_URL = "https://www.instagram.com/"

#: Quanto tempo `cie scrape login` espera o usuario terminar de logar.
LOGIN_TIMEOUT_S = 300.0


def profile_dir(cie_home: Path) -> Path:
    """O perfil do Chrome vive dentro de `.cie/`, que ja esta no .gitignore."""
    return Path(cie_home) / "browser-profile"


def _require_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as exc:
        raise ScrapeError(
            "playwright nao esta instalado. Rode:\n"
            "  uv sync --extra scrape\n"
            "Ele usa o Chrome que voce ja tem instalado (channel='chrome'), "
            "nao baixa Chromium."
        ) from exc
    return sync_playwright


@contextmanager
def open_page(perfil: Path, *, headless: bool = True) -> Iterator[Any]:
    """Abre o perfil persistente e entrega a pagina. Fecha o contexto ao sair."""
    sync_playwright = _require_playwright()
    perfil = Path(perfil)
    perfil.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        try:
            contexto = pw.chromium.launch_persistent_context(
                user_data_dir=str(perfil),
                channel="chrome",
                headless=headless,
                viewport={"width": 1280, "height": 900},
            )
        except Exception as exc:  # noqa: BLE001 - traduzimos para erro do dominio
            raise ScrapeError(
                f"nao consegui abrir o Chrome com o perfil {perfil}: {exc}\n"
                "Se o Chrome nao estiver instalado, instale-o, ou rode "
                "'uv run playwright install chromium' e troque channel por chromium."
            ) from exc
        try:
            pagina = contexto.pages[0] if contexto.pages else contexto.new_page()
            yield pagina
        finally:
            contexto.close()


def goto_instagram(pagina) -> None:
    pagina.goto(INSTAGRAM_URL, wait_until="domcontentloaded", timeout=60_000)


def is_logged_in(pagina) -> bool:
    """Sessao logada = cookie `sessionid` presente e nao vazio."""
    for cookie in pagina.context.cookies(INSTAGRAM_URL):
        if cookie.get("name") == "sessionid" and cookie.get("value"):
            return True
    return False


def app_id(pagina) -> str:
    return str(pagina.evaluate(load_snippet("appid")))


def run_snippet(pagina, nome: str, params: dict) -> dict:
    """Executa um snippet de colheita e devolve o JSON cru.

    O snippet devolve `{error: "..."}` em vez de levantar, para a mensagem
    atravessar a fronteira JS/Python legivel. Traduzimos aqui.
    """
    resultado = pagina.evaluate(load_snippet(nome), params)
    if not isinstance(resultado, dict):
        raise ScrapeError(
            f"snippet {nome!r} devolveu {type(resultado).__name__}, esperava objeto"
        )
    if resultado.get("error"):
        raise ScrapeError(str(resultado["error"]))
    return resultado


def login(perfil: Path, *, timeout_s: float = LOGIN_TIMEOUT_S) -> bool:
    """Abre o browser visivel e espera o usuario logar. Devolve se conseguiu."""
    with open_page(perfil, headless=False) as pagina:
        goto_instagram(pagina)
        restante = timeout_s
        while restante > 0:
            if is_logged_in(pagina):
                return True
            pagina.wait_for_timeout(2000)
            restante -= 2
    return False


def check_session(perfil: Path) -> bool:
    """A sessao salva ainda esta logada?"""
    with open_page(perfil, headless=True) as pagina:
        goto_instagram(pagina)
        return is_logged_in(pagina)
```

Acrescente ao bloco de imports no topo do arquivo:

```python
from contextlib import contextmanager
from typing import Any, Iterator
```

- [ ] **Step 4: Rode os testes e confirme que passam**

Run: `uv run pytest tests/test_scrape_browser.py -v`
Expected: 7 passed

- [ ] **Step 5: Commit**

```bash
git add cie/scrape/browser.py tests/test_scrape_browser.py
git commit -m "Scrape: Playwright com perfil persistente, login e checagem de sessao"
```

---

## Task 9: `harvest.py` — orquestracao da colheita

**Files:**
- Create: `cie/scrape/harvest.py`
- Test: `tests/test_scrape_harvest.py`

- [ ] **Step 1: Escreva o teste que falha**

Crie `tests/test_scrape_harvest.py`:

```python
"""Orquestracao da colheita. O browser e substituido por um duble."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cie.errors import ScrapeError
from cie.scrape.harvest import build_envelope, harvest, write_envelope
from cie.scrape.targets import HashtagTarget, PostTarget, ProfileTarget


class BrowserFalso:
    """Duble do modulo browser: registra o que foi pedido, devolve JSON fixo."""

    def __init__(self, resultado=None, logado=True):
        self.resultado = resultado or {"source": "feed_user", "pages": [{"items": []}]}
        self.logado = logado
        self.chamadas: list[tuple[str, dict]] = []

    def open_page(self, perfil, headless=True):
        from contextlib import contextmanager

        @contextmanager
        def _ctx():
            yield object()

        return _ctx()

    def goto_instagram(self, pagina):
        pass

    def is_logged_in(self, pagina):
        return self.logado

    def app_id(self, pagina):
        return "999"

    def run_snippet(self, pagina, nome, params):
        self.chamadas.append((nome, params))
        return self.resultado


def test_envelope_carrega_alvo_e_carimbo():
    envelope = build_envelope(
        ProfileTarget(handle="cafecanastra"),
        {"source": "feed_user", "pages": [{"items": []}]},
    )
    assert envelope["target"] == {
        "kind": "profile",
        "slug": "cafecanastra",
        "handle": "cafecanastra",
    }
    assert envelope["source"] == "feed_user"
    assert envelope["harvested_at"]


def test_envelope_de_post_guarda_o_shortcode():
    envelope = build_envelope(PostTarget(shortcode="AAA111"), {"pages": []})
    assert envelope["target"]["shortcode"] == "AAA111"
    assert envelope["target"]["kind"] == "post"


def test_envelope_de_hashtag_guarda_a_tag():
    envelope = build_envelope(HashtagTarget(tag="cafeespecial"), {"pages": []})
    assert envelope["target"]["tag"] == "cafeespecial"
    assert envelope["target"]["slug"] == "tag-cafeespecial"


def test_envelope_vai_para_colheita_com_nome_ordenavel(tmp_path: Path):
    envelope = build_envelope(ProfileTarget(handle="cafecanastra"), {"pages": []})
    caminho = write_envelope(envelope, tmp_path)

    assert caminho.parent == tmp_path / "_colheita"
    assert caminho.name.startswith("cafecanastra-")
    assert caminho.suffix == ".json"
    assert json.loads(caminho.read_text(encoding="utf-8"))["target"]["slug"] == "cafecanastra"


def test_perfil_chama_o_snippet_de_perfil_com_limite(tmp_path: Path):
    falso = BrowserFalso()
    harvest(
        ProfileTarget(handle="cafecanastra"),
        profile_dir=tmp_path / "perfil",
        limit=30,
        browser_mod=falso,
    )
    nome, params = falso.chamadas[0]
    assert nome == "profile"
    assert params["handle"] == "cafecanastra"
    assert params["limit"] == 30
    assert params["appId"] == "999"


def test_post_converte_shortcode_em_media_id(tmp_path: Path):
    falso = BrowserFalso({"source": "media_info", "pages": []})
    harvest(PostTarget(shortcode="CBa"), profile_dir=tmp_path / "p", browser_mod=falso)
    nome, params = falso.chamadas[0]
    assert nome == "post"
    assert params["mediaId"] == "8282"


def test_hashtag_chama_o_snippet_de_hashtag(tmp_path: Path):
    falso = BrowserFalso({"source": "tag_web_info", "pages": []})
    harvest(HashtagTarget(tag="cafeespecial"), profile_dir=tmp_path / "p", browser_mod=falso)
    nome, params = falso.chamadas[0]
    assert nome == "hashtag"
    assert params["tag"] == "cafeespecial"


def test_sessao_deslogada_para_antes_de_colher(tmp_path: Path):
    falso = BrowserFalso(logado=False)
    with pytest.raises(ScrapeError) as exc:
        harvest(ProfileTarget(handle="x"), profile_dir=tmp_path / "p", browser_mod=falso)
    assert "cie scrape login" in str(exc.value)
    assert falso.chamadas == []
```

- [ ] **Step 2: Rode o teste e confirme que falha**

Run: `uv run pytest tests/test_scrape_harvest.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'cie.scrape.harvest'`

- [ ] **Step 3: Implemente `harvest.py`**

Crie `cie/scrape/harvest.py`:

```python
"""Orquestracao da colheita: alvo -> snippet certo -> envelope em disco.

O envelope e gravado ANTES de qualquer download. Se o download falhar depois,
a colheita nao se perde: `cie scrape collect <arquivo>` retoma dali.

`browser_mod` e injetavel para o teste substituir o Playwright inteiro por um
duble - e o unico jeito de testar a orquestracao sem abrir browser.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..errors import ScrapeError
from .targets import HashtagTarget, PostTarget, ProfileTarget, Target, shortcode_to_media_id


def build_envelope(target: Target, resultado: dict) -> dict:
    """Junta alvo, carimbo e paginas cruas no formato que o parser espera."""
    alvo: dict[str, Any] = {"kind": target.kind, "slug": target.slug}
    if isinstance(target, ProfileTarget):
        alvo["handle"] = target.handle
    elif isinstance(target, PostTarget):
        alvo["shortcode"] = target.shortcode
    elif isinstance(target, HashtagTarget):
        alvo["tag"] = target.tag

    return {
        "target": alvo,
        "harvested_at": datetime.now(tz=timezone.utc).isoformat(),
        "source": resultado.get("source", ""),
        "pages": resultado.get("pages") or [],
    }


def write_envelope(envelope: dict, out_root: Path) -> Path:
    """Grava em `<out_root>/_colheita/<slug>-<carimbo>.json`."""
    pasta = Path(out_root) / "_colheita"
    pasta.mkdir(parents=True, exist_ok=True)
    carimbo = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%S")
    caminho = pasta / f"{envelope['target']['slug']}-{carimbo}.json"
    caminho.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
    return caminho


def harvest(
    target: Target,
    *,
    profile_dir: Path,
    limit: int = 12,
    headless: bool = True,
    browser_mod: Any = None,
) -> dict:
    """Abre a sessao, roda o snippet do alvo, devolve o envelope. Nao baixa nada."""
    if browser_mod is None:
        from . import browser as browser_mod  # import tardio: Playwright e opcional

    with browser_mod.open_page(profile_dir, headless=headless) as pagina:
        browser_mod.goto_instagram(pagina)
        if not browser_mod.is_logged_in(pagina):
            raise ScrapeError(
                "a sessao salva nao esta logada no Instagram. "
                "Rode 'cie scrape login' e faca login uma vez."
            )

        params: dict[str, Any] = {"appId": browser_mod.app_id(pagina)}

        if isinstance(target, ProfileTarget):
            snippet = "profile"
            params |= {"handle": target.handle, "limit": max(0, limit)}
        elif isinstance(target, PostTarget):
            snippet = "post"
            params |= {"mediaId": str(shortcode_to_media_id(target.shortcode))}
        elif isinstance(target, HashtagTarget):
            snippet = "hashtag"
            params |= {"tag": target.tag}
        else:
            raise ScrapeError(f"alvo nao suportado: {type(target).__name__}")

        resultado = browser_mod.run_snippet(pagina, snippet, params)

    return build_envelope(target, resultado)
```

- [ ] **Step 4: Rode os testes e confirme que passam**

Run: `uv run pytest tests/test_scrape_harvest.py -v`
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add cie/scrape/harvest.py tests/test_scrape_harvest.py
git commit -m "Scrape: orquestracao da colheita e envelope em disco"
```

---

## Task 10: `cli.py` — comandos do scrape

**Files:**
- Create: `cie/scrape/cli.py`
- Modify: `cie/cli.py` (imports e registro do sub-app)
- Test: `tests/test_scrape_cli.py`

- [ ] **Step 1: Escreva o teste que falha**

Crie `tests/test_scrape_cli.py`:

```python
"""CLI do scrape. Nenhum teste aqui abre browser nem toca a rede."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from cie.cli import app

runner = CliRunner()


def _envelope(slug="cafecanastra") -> dict:
    return {
        "target": {"kind": "profile", "slug": slug, "handle": slug},
        "harvested_at": "2026-08-18T21:30:00+00:00",
        "source": "feed_user",
        "pages": [
            {
                "items": [
                    {
                        "code": "AAA111",
                        "taken_at": 1786000000,
                        "media_type": 1,
                        "user": {"username": slug},
                        "caption": {"text": "legenda"},
                        "image_versions2": {
                            "candidates": [
                                {
                                    "url": "https://cdn.example/AAA111.jpg",
                                    "width": 1080,
                                    "height": 1350,
                                }
                            ]
                        },
                    }
                ]
            }
        ],
    }


def test_scrape_aparece_no_help():
    resultado = runner.invoke(app, ["--help"])
    assert resultado.exit_code == 0
    assert "scrape" in resultado.stdout


def test_help_do_scrape_lista_os_comandos():
    resultado = runner.invoke(app, ["scrape", "--help"])
    assert resultado.exit_code == 0
    for comando in ("login", "status", "harvest", "collect", "run"):
        assert comando in resultado.stdout


def test_link_invalido_falha_com_mensagem_e_nao_stacktrace():
    resultado = runner.invoke(app, ["scrape", "run", "https://example.com/x", "--dry-run"])
    assert resultado.exit_code != 0
    assert "instagram.com" in resultado.stdout


def test_reel_e_recusado_pela_cli():
    resultado = runner.invoke(
        app, ["scrape", "run", "https://www.instagram.com/reel/AAA111/", "--dry-run"]
    )
    assert resultado.exit_code != 0
    assert "reel" in resultado.stdout.lower()


def test_collect_em_dry_run_nao_escreve_imagem(tmp_path: Path):
    arquivo = tmp_path / "colheita.json"
    arquivo.write_text(json.dumps(_envelope()), encoding="utf-8")

    resultado = runner.invoke(
        app,
        ["scrape", "collect", str(arquivo), "--out", str(tmp_path / "saida"), "--dry-run"],
    )

    assert resultado.exit_code == 0
    assert list((tmp_path / "saida").rglob("*.jpg")) == []
    assert "1" in resultado.stdout


def test_collect_de_arquivo_inexistente_falha_com_mensagem(tmp_path: Path):
    resultado = runner.invoke(app, ["scrape", "collect", str(tmp_path / "nao-existe.json")])
    assert resultado.exit_code != 0
    assert "nao-existe.json" in resultado.stdout


def test_collect_de_json_invalido_falha_com_mensagem(tmp_path: Path):
    arquivo = tmp_path / "quebrado.json"
    arquivo.write_text("{isto nao e json", encoding="utf-8")

    resultado = runner.invoke(app, ["scrape", "collect", str(arquivo)])
    assert resultado.exit_code != 0
    assert "json" in resultado.stdout.lower()
```

- [ ] **Step 2: Rode o teste e confirme que falha**

Run: `uv run pytest tests/test_scrape_cli.py -v`
Expected: FAIL — `scrape` nao aparece no help

- [ ] **Step 3: Implemente `cie/scrape/cli.py`**

```python
"""Comandos `cie scrape`.

Mora aqui, e nao em `cie/cli.py`, porque aquele arquivo ja passa de 700 linhas.
`cie/cli.py` so registra o sub-app.

Playwright e importado tardiamente, dentro de cada comando que precisa dele -
mesma regra do resto da CLI: modulo pesado quebrado nao derruba a CLI inteira.
"""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ..config import get_settings
from ..errors import CieError
from .targets import parse_target

app = typer.Typer(
    help="Raspagem de imagem do Instagram (perfil, post ou hashtag).",
    no_args_is_help=True,
)
console = Console()

#: Padrao conservador: sem isto, colar um perfil grande raspa centenas de posts.
LIMITE_PADRAO = 12


def _out_root(out: Path | None) -> Path:
    return out if out is not None else get_settings().root / "raspagem"


def _perfil_do_browser() -> Path:
    from .browser import profile_dir

    return profile_dir(get_settings().home)


def _falha(mensagem: str) -> None:
    console.print(f"[red]{mensagem}[/red]")
    raise typer.Exit(code=1)


@app.command()
def login() -> None:
    """Abre o Chrome para voce logar no Instagram. A sessao fica salva."""
    from . import browser

    perfil = _perfil_do_browser()
    console.print(f"perfil do browser: [dim]{perfil}[/dim]")
    console.print("Abrindo o Chrome. Faca login no Instagram e deixe a janela aberta.")
    console.print(
        "[yellow]Dica: prefira uma conta secundaria. Raspagem pesada pode render "
        "bloqueio temporario, e voce nao quer isso no perfil comercial.[/yellow]"
    )
    try:
        if browser.login(perfil):
            console.print("[green]sessao salva - pode fechar a janela[/green]")
            return
    except CieError as exc:
        _falha(str(exc))
    _falha("tempo esgotado sem login detectado")


@app.command()
def status() -> None:
    """A sessao salva ainda esta logada?"""
    from . import browser

    perfil = _perfil_do_browser()
    if not perfil.exists():
        _falha(f"nenhum perfil em {perfil}. Rode 'cie scrape login' primeiro.")
    try:
        logado = browser.check_session(perfil)
    except CieError as exc:
        _falha(str(exc))
    if logado:
        console.print(f"[green]logado[/green]  [dim]{perfil}[/dim]")
    else:
        _falha("sessao existe mas nao esta logada. Rode 'cie scrape login'.")


@app.command("harvest")
def harvest_cmd(
    link: str = typer.Argument(..., help="URL do perfil, post ou hashtag"),
    limit: int = typer.Option(LIMITE_PADRAO, "--limit", help="posts a colher; 0 = todos"),
    out: Path = typer.Option(None, "--out", help="raiz de saida (padrao: raspagem/)"),
    show_browser: bool = typer.Option(False, "--show-browser", help="nao usar headless"),
) -> None:
    """So colhe o JSON cru, sem baixar imagem."""
    from .harvest import harvest, write_envelope

    try:
        alvo = parse_target(link)
        envelope = harvest(
            alvo,
            profile_dir=_perfil_do_browser(),
            limit=limit,
            headless=not show_browser,
        )
        caminho = write_envelope(envelope, _out_root(out))
    except CieError as exc:
        _falha(str(exc))

    paginas = len(envelope.get("pages") or [])
    console.print(f"[green]colhido[/green] {alvo.slug}: {paginas} pagina(s) -> {caminho}")


@app.command("collect")
def collect_cmd(
    arquivo: Path = typer.Argument(..., help="envelope gravado por harvest"),
    out: Path = typer.Option(None, "--out", help="raiz de saida (padrao: raspagem/)"),
    limit: int = typer.Option(0, "--limit", help="teto de downloads; 0 = sem teto"),
    delay: float = typer.Option(1.0, "--delay", help="pausa entre downloads, em segundos"),
    dry_run: bool = typer.Option(False, "--dry-run", help="lista o que baixaria"),
) -> None:
    """Baixa as imagens de um envelope ja colhido."""
    from .download import download_batch
    from .parser import parse_envelope

    if not arquivo.is_file():
        _falha(f"arquivo nao encontrado: {arquivo}")

    try:
        envelope = json.loads(arquivo.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _falha(f"json invalido em {arquivo}: {exc}")

    try:
        lote = parse_envelope(envelope)
        relatorio = download_batch(
            lote,
            out_root=_out_root(out),
            limit=limit,
            delay=delay,
            dry_run=dry_run,
        )
    except CieError as exc:
        _falha(str(exc))

    _imprime_relatorio(relatorio, lote)


@app.command("run")
def run_cmd(
    link: str = typer.Argument(..., help="URL do perfil, post ou hashtag"),
    limit: int = typer.Option(LIMITE_PADRAO, "--limit", help="posts a colher; 0 = todos"),
    out: Path = typer.Option(None, "--out", help="raiz de saida (padrao: raspagem/)"),
    delay: float = typer.Option(1.0, "--delay", help="pausa entre downloads, em segundos"),
    dry_run: bool = typer.Option(False, "--dry-run", help="lista o que baixaria"),
    show_browser: bool = typer.Option(False, "--show-browser", help="nao usar headless"),
) -> None:
    """Colhe e baixa: o comando normal."""
    from .download import download_batch
    from .harvest import harvest, write_envelope
    from .parser import parse_envelope

    raiz = _out_root(out)
    try:
        alvo = parse_target(link)
        envelope = harvest(
            alvo,
            profile_dir=_perfil_do_browser(),
            limit=limit,
            headless=not show_browser,
        )
        caminho = write_envelope(envelope, raiz)
        console.print(f"[dim]colheita crua em {caminho}[/dim]")

        lote = parse_envelope(envelope)
        relatorio = download_batch(lote, out_root=raiz, delay=delay, dry_run=dry_run)
    except CieError as exc:
        _falha(str(exc))

    _imprime_relatorio(relatorio, lote)


def _imprime_relatorio(relatorio, lote) -> None:
    tabela = Table(title=f"{lote.target_slug} ({lote.target_kind})")
    tabela.add_column("resultado")
    tabela.add_column("n", justify="right")
    if relatorio.dry_run:
        tabela.add_row("baixaria", str(relatorio.previstos))
    else:
        tabela.add_row("baixados", str(relatorio.baixados))
        tabela.add_row("duplicados", str(relatorio.duplicados))
    tabela.add_row("videos pulados", str(relatorio.videos_pulados))
    tabela.add_row("erros", str(relatorio.erros))
    console.print(tabela)

    for mensagem in relatorio.mensagens_de_erro():
        console.print(f"[red]erro[/red] {mensagem}")

    if not relatorio.dry_run and relatorio.baixados:
        console.print(
            "[dim]Nada disso entrou no acervo. Para promover, mova para "
            "base-curada/03-mood-terceiros/ (ou 02-real-nao-verificada/, se for "
            "foto da propria marca) e rode 'cie ingest'.[/dim]"
        )
```

- [ ] **Step 4: Registre o sub-app em `cie/cli.py`**

Depois da linha `report_app = typer.Typer(help="Relatorios.", no_args_is_help=True)`, acrescente:

```python
from .scrape.cli import app as scrape_app
```

Coloque esse import junto dos demais imports relativos no topo do arquivo (depois de `from .ingest import ingest_directory`).

Depois da linha `app.add_typer(report_app, name="report")`, acrescente:

```python
app.add_typer(scrape_app, name="scrape")
```

- [ ] **Step 5: Rode os testes e confirme que passam**

Run: `uv run pytest tests/test_scrape_cli.py -v`
Expected: 7 passed

- [ ] **Step 6: Rode a suite inteira**

Run: `uv run pytest`
Expected: tudo passa, sem regressao em `tests/test_cli.py`

- [ ] **Step 7: Commit**

```bash
git add cie/scrape/cli.py cie/cli.py tests/test_scrape_cli.py
git commit -m "Scrape: comandos login, status, harvest, collect e run na CLI"
```

---

## Task 11: Documentacao

**Files:**
- Create: `docs/RASPAGEM.md`
- Modify: `README.md`

- [ ] **Step 1: Escreva `docs/RASPAGEM.md`**

```markdown
# Raspagem do Instagram (`cie scrape`)

Cole um link de perfil, post ou hashtag; as imagens caem em `raspagem/` com
proveniencia registrada.

## O teto que voce precisa conhecer antes de usar

`cie/imaging.py` exige `REFERENCE_MIN_SIDE = 1200` para uma foto ser
reference-grade. O Instagram entrega no maximo **1080px**. Logo, **nenhuma imagem
raspada daqui pode virar pixel de saida.** Ela serve como descritor textual de
estilo, e nada alem disso.

Isso nao e limitacao a contornar. E a regra da casa funcionando: a IA edita e
estende o real; material de terceiro nao vira materia-prima de composicao.

## Instalacao

```bash
uv sync --extra scrape
```

Usa o Chrome que voce ja tem instalado (`channel="chrome"`), sem baixar Chromium.

## Login

```bash
cie scrape login     # abre o Chrome; logue e deixe a janela aberta
cie scrape status    # a sessao salva ainda esta logada?
```

A sessao fica em `.cie/browser-profile/`, que ja esta no `.gitignore`.

**Use uma conta secundaria.** Raspagem pesada rende bloqueio temporario, e voce
nao quer isso no perfil comercial da marca no meio de operacao.

## Uso

```bash
cie scrape run https://www.instagram.com/cafecanastra/ --limit 30
cie scrape run https://www.instagram.com/p/C1a2b3c/
cie scrape run https://www.instagram.com/explore/tags/cafeespecial/
cie scrape run @cafecanastra --dry-run
```

| Opcao | Padrao | Efeito |
|---|---|---|
| `--limit N` | 12 | quantos posts colher; `0` = todos |
| `--out DIR` | `raspagem/` | raiz de saida |
| `--delay S` | 1.0 | pausa entre downloads |
| `--dry-run` | desligado | lista o que baixaria, nao baixa |
| `--show-browser` | desligado | abre a janela do Chrome em vez de headless |

Quando algo quebrar, os dois estagios sao separaveis:

```bash
cie scrape harvest @cafecanastra --limit 30      # so o JSON cru
cie scrape collect raspagem/_colheita/<arq>.json # so o download
```

## O que sai em disco

```
raspagem/
  _colheita/cafecanastra-20260818T2130.json   JSON cru da colheita
  cafecanastra/
    2026-08-18_C1a2b3c_1.jpg
    2026-08-18_C1a2b3c_1.json                 sidecar de proveniencia
  _manifest.json                              indice de tudo, por sha256
```

O sidecar guarda URL do post, handle do dono, shortcode, indice no carrossel,
URL de origem no CDN, dimensoes, sha256 e quando foi raspado.

Ele **nao** guarda `has_identifiable_person` nem `consent_on_file`. Esses dois
campos so existem em `Asset`, e so a curadoria humana os preenche. A raspagem
nao opina sobre eles.

## Como isso vira acervo

Nao vira sozinho. `cie scrape` para em `raspagem/`:

1. Olhe o que caiu.
2. Mova o que prestou para `base-curada/03-mood-terceiros/` (material de
   terceiro) ou `base-curada/02-real-nao-verificada/` (foto da propria marca,
   que o Instagram ja despiu de EXIF).
3. Rode `cie ingest`.
4. Curadoria humana em `cie assets curate` ou na UI de review.

## Regras no codigo

| Regra | Onde vive |
|---|---|
| Video nunca e baixado | `download.download_batch` |
| Reel e recusado no parse do link | `targets.parse_target` |
| Conteudo repetido e pulado por sha256 | `download._hashes_existentes` |
| Nada sobrescreve arquivo existente | `download._caminho_livre` |
| Todo arquivo nasce com sidecar | `download._grava_sidecar` |
| Formato inesperado vira erro legivel | `parser`, via `InstagramFormatError` |
| Nada escreve no banco do CIE | o pacote inteiro nao importa `repository` |

## Quando o Instagram mudar o formato

Ele vai mudar. Os sintomas e onde olhar:

- **`InstagramFormatError` dizendo qual campo sumiu** — o objeto `media` mudou.
  Conserte `cie/scrape/parser.py` e atualize as fixtures em
  `tests/fixtures/scrape/`.
- **`ScrapeError` com HTTP 4xx** — o endpoint mudou. Conserte o snippet
  correspondente em `cie/scrape/js/`.
- **Colheita vazia sem erro** — a resposta mudou de forma sem mudar de status.
  Rode `cie scrape harvest` e leia o JSON cru em `raspagem/_colheita/`.

O JSON cru em `_colheita/` existe exatamente para esse momento: ele vira a
proxima fixture de teste.
```

- [ ] **Step 2: Aponte o README para a documentacao nova**

Em `README.md`, na tabela "O que o sistema garante, no codigo", acrescente a linha:

```markdown
| Imagem raspada do Instagram nunca vira pixel de saida | teto de `REFERENCE_MIN_SIDE` vs. 1080px do IG — ver [`docs/RASPAGEM.md`](docs/RASPAGEM.md) |
```

E acrescente, ao final da secao "Instalacao", logo depois do bloco do extra `heic`:

```markdown
Raspagem do Instagram exige o extra opcional (usa o Chrome ja instalado, nao baixa Chromium):

```bash
uv sync --extra scrape
```

Ver [`docs/RASPAGEM.md`](docs/RASPAGEM.md).
```

- [ ] **Step 3: Verifique a suite completa uma ultima vez**

Run: `uv run pytest`
Expected: tudo passa

Run: `uv run cie scrape --help`
Expected: lista `login`, `status`, `harvest`, `collect`, `run`

Run: `uv run cie scrape run "https://example.com/x" --dry-run`
Expected: exit code 1, mensagem citando `instagram.com`, sem stacktrace

- [ ] **Step 4: Commit**

```bash
git add docs/RASPAGEM.md README.md
git commit -m "Scrape: documentacao de uso, limites e manutencao"
```

---

## Verificacao manual final (exige rede e conta)

Estes passos nao sao automatizaveis e precisam de um humano com uma conta do Instagram. Rode antes de considerar a feature entregue, e relate o resultado real — inclusive se falhar.

- [ ] `uv sync --extra scrape` completa sem erro
- [ ] `cie scrape login` abre o Chrome e detecta o login
- [ ] `cie scrape status` responde "logado"
- [ ] `cie scrape run @<algum_perfil> --limit 3 --dry-run` lista 3 itens sem baixar
- [ ] `cie scrape run @<algum_perfil> --limit 3` grava 3 imagens com sidecar em `raspagem/`
- [ ] Rodar o mesmo comando de novo reporta 3 duplicados e nao grava nada
- [ ] `cie scrape run <link de post com carrossel>` traz todas as imagens do carrossel
- [ ] `cie scrape run <link de hashtag>` traz imagens de perfis diferentes
- [ ] Um post que seja video aparece como "video pulado", nao como erro

Se algum passo falhar, o JSON cru em `raspagem/_colheita/` diz o porque — ele e gravado antes de qualquer download justamente para isso.

---

# Registro de execucao (2026-08-18)

As 11 tasks foram executadas por subagentes, uma por vez, com revisao entre elas.
15 commits, de `3e1c3bf` a `3e8dbb1`.

## O que a revisao pegou que o plano tinha errado

O plano continha codigo pronto, e parte desse codigo estava errada. Vale registrar,
porque o padrao se repete:

**Path traversal, tres vezes.** `slug`, `shortcode` e o nome do snippet viram todos
componente de caminho de arquivo, e os tres aceitavam `..` na redacao original.
O terceiro caso (`write_envelope`) foi comprovado explorando de verdade: com o codigo
original, `slug="../../pwned"` gravava um arquivo acima de `_colheita/`. Correcao:
`models.caminho_seguro` para os dois primeiros, allowlist estrita para o terceiro.

**O parser nao honrava o proprio contrato.** O docstring prometia que so
`InstagramFormatError` escaparia; dez formas de JSON malformado vazavam
`AttributeError`, `ValueError` ou `ValidationError`. Como a CLI so captura `CieError`,
cada uma viraria stacktrace na cara do usuario. Corrigido com `_objeto`/`_lista`/`_inteiro`.
Fuzz de 5192 combinacoes depois: nenhum vazamento.

**`urlparse` levanta `ValueError`** em link com colchete (`[instagram.com/x`) —
justamente o tipo de excecao crua que o modulo existe para impedir.

**Handle com ponto era recusado.** `cafe.canastra` caia no ramo de URL e falhava com
mensagem errada. Pontos sao comuns em handle real.

**Rich quebrava substring no meio.** A largura padrao do console fora de terminal e 79
colunas, e um caminho Windows e uma "palavra" so para o Rich. Testes que verificam
substring na saida iam falhar de forma intermitente dependendo do tamanho do caminho
da maquina. Corrigido com `soft_wrap=True`, sem enfraquecer os testes.

**Erros meus de aritmetica e contagem no plano:** `shortcode_to_media_id("CBa")` e 8282,
nao 4184; a Task 3 dizia "9 passed" para um arquivo com 8 testes.

## Duas divergencias de desenho, ja registradas acima

`cie scrape run <url>` em vez de `cie scrape <url>`, e o fallback de download pelo
Playwright adiado ate haver evidencia de 403 do CDN.

## O que NAO foi verificado

Nada que precise de rede ou de conta do Instagram. Playwright nao esta instalado no
venv (`uv sync --extra scrape` ainda nao foi rodado), entao o caminho real de browser
— `login`, `status`, e a colheita de verdade — continua sem execucao. A lista de
verificacao manual no fim deste plano e o que falta.
