"""Comandos `cie scrape`.

Mora aqui, e nao em `cie/cli.py`, porque aquele arquivo ja passa de 700 linhas.
`cie/cli.py` so registra o sub-app.

Playwright e importado tardiamente, dentro de cada comando que precisa dele -
mesma regra do resto da CLI: modulo pesado quebrado nao derruba a CLI inteira.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import NoReturn, Optional

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


def _out_root(out: Optional[Path]) -> Path:
    return out if out is not None else get_settings().root / "raspagem"


def _perfil_do_browser() -> Path:
    from .browser import profile_dir

    return profile_dir(get_settings().home)


def _falha(mensagem: str) -> NoReturn:
    """Imprime a mensagem em uma linha (sem quebra) e encerra com codigo 1.

    `soft_wrap=True` evita que o rich quebre um caminho ou URL longos ao meio
    quando a saida nao e um terminal real (caso do CliRunner nos testes, onde
    a largura padrao e 80 colunas) - do contrario uma substring como o nome de
    um arquivo poderia ser cortada em duas linhas.
    """
    console.print(f"[red]{mensagem}[/red]", soft_wrap=True)
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
    out: Optional[Path] = typer.Option(None, "--out", help="raiz de saida (padrao: raspagem/)"),
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
    out: Optional[Path] = typer.Option(None, "--out", help="raiz de saida (padrao: raspagem/)"),
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
        texto = arquivo.read_text(encoding="utf-8")
    except OSError as exc:
        _falha(f"nao consegui ler {arquivo}: {exc}")

    try:
        envelope = json.loads(texto)
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
    out: Optional[Path] = typer.Option(None, "--out", help="raiz de saida (padrao: raspagem/)"),
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
        console.print(f"[red]erro[/red] {mensagem}", soft_wrap=True)

    if not relatorio.dry_run and relatorio.baixados:
        console.print(
            "[dim]Nada disso entrou no acervo. Para promover, mova para "
            "base-curada/03-mood-terceiros/ (ou 02-real-nao-verificada/, se for "
            "foto da propria marca) e rode 'cie ingest'.[/dim]"
        )
