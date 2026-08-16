"""CLI do Canastra Image Engine.

Fase 1 expoe ingestao e catalogo. Os comandos de geracao entram nas fases
seguintes, sempre com `--dry-run` como padrao mental de trabalho.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from . import repository
from .config import get_settings
from .db import applied_migrations, open_db, pending_migrations
from .enums import Location, Pillar, Sku
from .ingest import ingest_directory

app = typer.Typer(
    help="Canastra Image Engine - a IA edita e estende o real; nao inventa o real.",
    no_args_is_help=True,
)
assets_app = typer.Typer(help="Catalogo da base de fotos reais.", no_args_is_help=True)
db_app = typer.Typer(help="Banco de dados e migracoes.", no_args_is_help=True)
app.add_typer(assets_app, name="assets")
app.add_typer(db_app, name="db")

console = Console()


def _open() -> tuple:
    settings = get_settings()
    return settings, open_db(settings)


@app.command()
def version() -> None:
    """Mostra a versao do CIE e onde fica o estado local."""
    from . import __version__

    settings = get_settings()
    console.print(f"[bold]Canastra Image Engine[/bold] {__version__}")
    console.print(f"CIE_HOME: {settings.home}")
    console.print(f"banco:    {settings.db_path}")


@app.command()
def ingest(
    path: Path = typer.Argument(..., exists=True, file_okay=False, help="Pasta da base de fotos."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Analisa sem gravar nada."),
    thumbs: bool = typer.Option(True, "--thumbs/--no-thumbs", help="Gera thumbnails."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Lista arquivo a arquivo."),
) -> None:
    """Varre uma pasta e popula o catalogo (dedupe por sha256)."""
    settings, conn = _open()

    def _echo(outcome) -> None:
        if not verbose:
            return
        color = {"ingested": "green", "duplicate": "yellow", "skipped": "dim", "error": "red"}
        console.print(
            f"[{color.get(outcome.status, 'white')}]{outcome.status:<9}[/] "
            f"{outcome.path.name} {outcome.reason or ''}"
        )

    report = ingest_directory(
        conn, settings, path, dry_run=dry_run, make_thumbs=thumbs, on_file=_echo
    )

    console.print()
    console.print(f"[bold]{'DRY-RUN ' if dry_run else ''}Ingestao de[/bold] {report.root}")
    console.print(f"  arquivos varridos : {report.scanned}")
    console.print(f"  ingeridos         : [green]{report.ingested}[/green]")
    console.print(f"  duplicados        : [yellow]{report.duplicates}[/yellow]")
    console.print(f"  ignorados         : {report.skipped}")
    console.print(f"  erros             : [red]{report.errors}[/red]")
    console.print(f"  precisam revisao  : {report.needs_review}")
    console.print()
    console.print(
        "[dim]Lembre: has_identifiable_person=1 e consent_on_file=0 sao os defaults "
        "restritivos. Rode `cie assets review` para curar.[/dim]"
    )


@assets_app.command("list")
def assets_list(
    pillar: Optional[str] = typer.Option(None, "--pillar", help="1|2|3|4|product|people"),
    sku: Optional[str] = typer.Option(None, "--sku"),
    location: Optional[str] = typer.Option(None, "--location"),
    needs_review: Optional[bool] = typer.Option(None, "--needs-review/--curated"),
    reference_grade: Optional[bool] = typer.Option(None, "--reference/--no-reference"),
    limit: int = typer.Option(50, "--limit"),
) -> None:
    """Lista assets do catalogo."""
    _, conn = _open()
    assets = repository.list_assets(
        conn,
        pillar=Pillar(pillar) if pillar else None,
        sku=Sku(sku) if sku else None,
        location=Location(location) if location else None,
        needs_review=needs_review,
        reference_grade=reference_grade,
        limit=limit,
    )
    if not assets:
        console.print("[yellow]nenhum asset encontrado[/yellow]")
        raise typer.Exit(code=0)

    table = Table(show_lines=False)
    for column in ("id", "arquivo", "pilar", "local", "sku", "q", "ref", "pessoa", "consent", "rev"):
        table.add_column(column)
    for asset in assets:
        table.add_row(
            str(asset.id),
            Path(asset.path).name,
            str(asset.pillar or "-"),
            str(asset.location or "-"),
            str(asset.sku or "-"),
            str(asset.quality_score if asset.quality_score is not None else "-"),
            "sim" if asset.is_reference_grade else "-",
            "sim" if asset.has_identifiable_person else "nao",
            "sim" if asset.consent_on_file else "[red]nao[/red]",
            "[yellow]sim[/yellow]" if asset.needs_review else "-",
        )
    console.print(table)
    console.print(f"[dim]{len(assets)} de {repository.count_assets(conn)} assets[/dim]")


@assets_app.command("show")
def assets_show(asset_id: int = typer.Argument(...)) -> None:
    """Detalha um asset, incluindo o rastro da inferencia."""
    _, conn = _open()
    asset = repository.get_asset(conn, asset_id)
    if not asset:
        console.print(f"[red]asset {asset_id} nao encontrado[/red]")
        raise typer.Exit(code=1)
    for key, value in asset.model_dump().items():
        console.print(f"[bold]{key:<24}[/bold] {value}")


@assets_app.command("curate")
def assets_curate(
    asset_id: int = typer.Argument(...),
    pillar: Optional[str] = typer.Option(None, "--pillar"),
    sku: Optional[str] = typer.Option(None, "--sku"),
    location: Optional[str] = typer.Option(None, "--location"),
    person: Optional[bool] = typer.Option(None, "--person/--no-person", help="Rosto identificavel."),
    consent: Optional[bool] = typer.Option(None, "--consent/--no-consent", help="Termo assinado."),
    packaging: Optional[bool] = typer.Option(None, "--packaging/--no-packaging"),
    reference: Optional[bool] = typer.Option(None, "--reference/--no-reference"),
    done: bool = typer.Option(False, "--done", help="Marca como revisado."),
) -> None:
    """Preenche os campos que so um humano pode preencher."""
    _, conn = _open()
    if not repository.get_asset(conn, asset_id):
        console.print(f"[red]asset {asset_id} nao encontrado[/red]")
        raise typer.Exit(code=1)

    fields = {}
    if pillar is not None:
        fields["pillar"] = Pillar(pillar)
    if sku is not None:
        fields["sku"] = Sku(sku)
    if location is not None:
        fields["location"] = Location(location)
    if person is not None:
        fields["has_identifiable_person"] = person
    if consent is not None:
        fields["consent_on_file"] = consent
    if packaging is not None:
        fields["has_readable_packaging"] = packaging
    if reference is not None:
        fields["is_reference_grade"] = reference
    if done:
        fields["needs_review"] = False

    if not fields:
        console.print("[yellow]nada para atualizar[/yellow]")
        raise typer.Exit(code=0)

    repository.update_asset_curation(conn, asset_id, **fields)
    console.print(f"[green]asset {asset_id} atualizado:[/green] {', '.join(sorted(fields))}")


@db_app.command("migrate")
def db_migrate() -> None:
    """Aplica migracoes pendentes."""
    settings = get_settings()
    settings.ensure_dirs()
    from .db import connect, migrate

    conn = connect(settings.db_path)
    applied = migrate(conn)
    if applied:
        for name in applied:
            console.print(f"[green]aplicada[/green] {name}")
    else:
        console.print("[dim]nada pendente[/dim]")


@db_app.command("status")
def db_status() -> None:
    """Mostra migracoes aplicadas e pendentes."""
    settings = get_settings()
    settings.ensure_dirs()
    from .db import connect

    conn = connect(settings.db_path)
    console.print(f"[bold]banco:[/bold] {settings.db_path}")
    for version, at in applied_migrations(conn):
        console.print(f"  [green]ok[/green] {version} ({at})")
    for version in pending_migrations(conn):
        console.print(f"  [yellow]pendente[/yellow] {version}")


if __name__ == "__main__":  # pragma: no cover
    app()
