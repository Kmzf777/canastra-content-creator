"""Fronteira com o mundo: Playwright sobre um perfil de Chrome persistente.

Fino de proposito. Abre o perfil, executa um snippet, devolve o JSON cru. Nada
aqui interpreta resposta do Instagram - isso e trabalho do `parser`, que e puro
e testavel. O Playwright em si nao tem teste automatizado, ja que e a fronteira
com o mundo real; a verificacao dele e manual, via `cie scrape status`. A logica
pura ao redor (nomes de caminho, traducao de erros, checagem de cookie) e
testada com objetos de pagina falsos em `tests/test_scrape_browser.py`.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from ..errors import ScrapeError

JS_DIR = Path(__file__).parent / "js"

#: Snippets que precisam existir em disco para a raspagem funcionar.
#: Tambem serve de allowlist: `nome` nunca vira caminho de arquivo sem passar
#: por aqui, entao um `nome` hostil (ex: "../parser") nunca chega ao disco.
SNIPPETS = ("appid", "profile", "post", "hashtag")


def load_snippet(nome: str) -> str:
    """Le um snippet de `js/`. Snippet ausente e erro de instalacao, nao de rede."""
    if nome not in SNIPPETS:
        raise ScrapeError(
            f"snippet {nome!r} nao encontrado em {JS_DIR}; instalacao incompleta"
        )
    caminho = JS_DIR / f"{nome}.js"
    if not caminho.is_file():
        raise ScrapeError(
            f"snippet {nome!r} nao encontrado em {JS_DIR}; instalacao incompleta"
        )
    return caminho.read_text(encoding="utf-8")


INSTAGRAM_URL = "https://www.instagram.com/"

#: Quanto tempo `cie scrape login` espera o usuario terminar de logar.
LOGIN_TIMEOUT_S = 300.0


def profile_dir(cie_home: Path) -> Path:
    """O perfil do Chrome vive dentro de `.cie/`, que ja esta no .gitignore."""
    return Path(cie_home) / "browser-profile"


def _require_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        # ImportError e a classe-mae de ModuleNotFoundError; uma instalacao
        # quebrada (ex: falta lib nativa) tende a levantar ImportError puro,
        # entao capturamos a classe mais ampla em vez de so a mais especifica.
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
            try:
                contexto.close()
            except Exception:  # noqa: BLE001 - fechar e best-effort
                # Se `yield` acima ja levantou (ex: usuario fechou a janela),
                # essa excecao original nao pode ser mascarada por uma falha
                # de limpeza aqui; e so nao propagamos o erro do close().
                pass


def goto_instagram(pagina) -> None:
    pagina.goto(INSTAGRAM_URL, wait_until="domcontentloaded", timeout=60_000)


def is_logged_in(pagina) -> bool:
    """Sessao logada = cookie `sessionid` presente e nao vazio.

    Se a pagina/janela foi fechada (ex: usuario fechou o Chrome), a chamada a
    `cookies()` levanta um erro do Playwright; traduzimos para `ScrapeError`
    em vez de deixar vazar uma excecao crua da biblioteca.
    """
    try:
        cookies = pagina.context.cookies(INSTAGRAM_URL)
    except Exception as exc:  # noqa: BLE001 - fronteira: vira erro do dominio
        raise ScrapeError(
            f"nao consegui checar os cookies da sessao (o browser foi fechado?): {exc}"
        ) from exc
    for cookie in cookies:
        if not isinstance(cookie, dict):
            continue
        if cookie.get("name") == "sessionid" and cookie.get("value"):
            return True
    return False


def app_id(pagina) -> str:
    """Extrai o `appId` que o Instagram embute no HTML, usado nos headers da API."""
    resultado = pagina.evaluate(load_snippet("appid"))
    if not isinstance(resultado, str) or not resultado:
        raise ScrapeError(
            f"nao consegui extrair o appId da pagina (recebi {resultado!r}); "
            "o Instagram pode ter mudado o HTML"
        )
    return resultado


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
    """Abre o browser visivel e espera o usuario logar. Devolve se conseguiu.

    O contador `restante` desce em passos fixos de 2s por iteracao - nao mede
    tempo real, entao um `wait_for_timeout` que retornasse instantaneamente
    (ex: em teste) ainda terminaria o loop apos `timeout_s / 2` iteracoes, sem
    risco de girar para sempre.
    """
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
