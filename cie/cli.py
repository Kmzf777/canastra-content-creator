"""CLI do Canastra Image Engine.

Decisao de UX que atravessa a CLI inteira: nada gasta credito por acidente.
`cie generate` e `cie queue run` nascem em modo seco; para chamar a API de
verdade e preciso pedir `--execute` explicitamente.

Os modulos pesados (cliente HTTP, FastAPI, exportacao) sao importados dentro de
cada comando: assim um modulo quebrado nao derruba a CLI inteira e o tempo de
inicializacao continua curto.
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
from .scrape.cli import app as scrape_app

app = typer.Typer(
    help="Canastra Image Engine - a IA edita e estende o real; nao inventa o real.",
    no_args_is_help=True,
)
assets_app = typer.Typer(help="Catalogo da base de fotos reais.", no_args_is_help=True)
db_app = typer.Typer(help="Banco de dados e migracoes.", no_args_is_help=True)
templates_app = typer.Typer(help="Cenas parametrizaveis (templates YAML).", no_args_is_help=True)
dna_app = typer.Typer(help="Style DNA derivado das fotos reais.", no_args_is_help=True)
queue_app = typer.Typer(help="Fila de geracao com teto de orcamento.", no_args_is_help=True)
report_app = typer.Typer(help="Relatorios.", no_args_is_help=True)
app.add_typer(assets_app, name="assets")
app.add_typer(db_app, name="db")
app.add_typer(templates_app, name="templates")
app.add_typer(dna_app, name="dna")
app.add_typer(queue_app, name="queue")
app.add_typer(report_app, name="report")
app.add_typer(scrape_app, name="scrape")

console = Console()


def _open() -> tuple:
    settings = get_settings()
    conn = open_db(settings)
    _load_probed_pricing(settings)
    return settings, conn


def _load_probed_pricing(settings) -> None:
    """Precos confirmados pela sondagem sobrescrevem o catalogo semente."""
    from . import pricing

    pricing.load_overrides(settings.home / "models.yaml")


def _parse_vars(pairs: Optional[list[str]]) -> dict:
    """--var chave=valor, repetivel."""
    variables: dict[str, str] = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise typer.BadParameter(f"--var espera chave=valor, recebi '{pair}'")
        key, value = pair.split("=", 1)
        variables[key.strip()] = value.strip()
    return variables


def _print_guardrails(report) -> None:
    """Tabela de guardrails avaliados - o coracao do --dry-run."""
    table = Table(title="Guardrails avaliados", show_lines=False)
    for column in ("regra", "severidade", "veredito", "mensagem"):
        table.add_column(column, overflow="fold")
    for row in report.as_rows():
        severity = str(row.get("severity", ""))
        passed = bool(row.get("passed"))
        if severity == "block" and not passed:
            veredito = "[red]BLOQUEIA[/red]"
        elif severity == "warn" and not passed:
            veredito = "[yellow]atencao[/yellow]"
        else:
            veredito = "[green]ok[/green]"
        table.add_row(str(row.get("rule", "")), severity, veredito, str(row.get("message", "")))
    console.print(table)
    for result in report.blocking:
        console.print(f"[red]bloqueado por {result.rule}[/red]: {result.message}")
        if result.remedy:
            console.print(f"  [dim]como resolver:[/dim] {result.remedy}")


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


@assets_app.command("review")
def assets_review(
    host: str = typer.Option("127.0.0.1", "--host"),
    port: int = typer.Option(8765, "--port"),
) -> None:
    """Abre a UI de curadoria em lote (grid de thumbnails, atalhos de teclado)."""
    _serve(host, port, path="/assets")


# --------------------------------------------------------------------------- #
# templates
# --------------------------------------------------------------------------- #


@templates_app.command("sync")
def templates_sync(
    path: Optional[Path] = typer.Option(None, "--path", help="Default: templates/ do projeto."),
) -> None:
    """Le os YAML de cenas e grava no banco."""
    from .template_loader import sync_templates

    settings, conn = _open()
    target = path or settings.templates_dir
    ids = sync_templates(conn, target)
    console.print(f"[green]{len(ids)} template(s) sincronizado(s)[/green] de {target}")


@templates_app.command("list")
def templates_list(
    pillar: Optional[str] = typer.Option(None, "--pillar"),
    kind: Optional[str] = typer.Option(None, "--kind"),
) -> None:
    """Lista as cenas disponiveis e seus riscos."""
    _, conn = _open()
    templates = repository.list_templates(
        conn, pillar=Pillar(pillar) if pillar else None, kind=kind
    )
    if not templates:
        console.print("[yellow]nenhum template no banco. Rode `cie templates sync`.[/yellow]")
        raise typer.Exit(code=0)

    table = Table()
    for column in ("id", "nome", "pilar", "tipo", "ar", "ref?", "riscos"):
        table.add_column(column)
    for template in templates:
        table.add_row(
            str(template.id),
            template.name,
            str(template.pillar or "-"),
            str(template.kind),
            str(template.default_aspect_ratio),
            "[yellow]sim[/yellow]" if template.requires_reference else "-",
            ", ".join(str(f) for f in template.risk_flags) or "-",
        )
    console.print(table)


# --------------------------------------------------------------------------- #
# style dna
# --------------------------------------------------------------------------- #


@dna_app.command("build")
def dna_build(
    name: str = typer.Option(..., "--name", help="Nome do perfil, ex.: laboratorio-uberlandia"),
    pillar: Optional[str] = typer.Option(None, "--pillar"),
    limit: int = typer.Option(12, "--limit", help="Quantas fotos enviar (8 a 15)."),
    asset_ids: Optional[str] = typer.Option(None, "--assets", help="IDs separados por virgula."),
    model: Optional[str] = typer.Option(None, "--model", help="Modelo com visao."),
    execute: bool = typer.Option(
        False, "--execute", help="Sem esta flag, so mostra quais fotos seriam enviadas."
    ),
) -> None:
    """Extrai o Style DNA de um conjunto de fotos reais aprovadas."""
    import asyncio

    from .dna import DEFAULT_LIMIT, extract_style_dna, select_assets_for_dna, summarize_dna
    from .errors import CieError

    settings, conn = _open()
    ids = [int(i) for i in asset_ids.split(",")] if asset_ids else None
    try:
        assets = select_assets_for_dna(
            conn, pillar=Pillar(pillar) if pillar else None, limit=limit or DEFAULT_LIMIT,
            asset_ids=ids,
        )
    except CieError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1)

    console.print(f"[bold]{len(assets)} foto(s) selecionada(s)[/bold] para o perfil '{name}':")
    for asset in assets:
        console.print(f"  {asset.id:>4}  q={asset.quality_score}  {Path(asset.path).name}")

    if not execute:
        console.print(
            "\n[dim]modo seco: nada foi enviado. Use --execute para chamar a API "
            "(gasta credito de chat com visao).[/dim]"
        )
        raise typer.Exit(code=0)

    from .xai import XaiClient

    async def _run():
        async with XaiClient(base_url=settings.xai_base_url) as client:
            return await extract_style_dna(
                client, conn, name=name,
                pillar=Pillar(pillar) if pillar else None,
                limit=limit, asset_ids=ids, model=model, settings=settings,
            )

    try:
        dna = asyncio.run(_run())
    except CieError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1)
    console.print(f"\n[green]Style DNA '{dna.name}' gravado.[/green]")
    console.print(summarize_dna(dna))


@dna_app.command("list")
def dna_list(pillar: Optional[str] = typer.Option(None, "--pillar")) -> None:
    """Lista os perfis de estilo ja extraidos."""
    _, conn = _open()
    profiles = repository.list_style_dna(conn, pillar=Pillar(pillar) if pillar else None)
    if not profiles:
        console.print("[yellow]nenhum Style DNA. Rode `cie dna build`.[/yellow]")
        raise typer.Exit(code=0)
    table = Table()
    for column in ("id", "nome", "pilar", "fotos", "fragmento"):
        table.add_column(column, overflow="fold")
    for dna in profiles:
        fragment = dna.prompt_fragment
        table.add_row(
            str(dna.id),
            dna.name,
            str(dna.pillar or "-"),
            str(len(dna.source_asset_ids)),
            fragment[:90] + ("..." if len(fragment) > 90 else ""),
        )
    console.print(table)


@dna_app.command("show")
def dna_show(name: str = typer.Argument(...)) -> None:
    """Mostra o descritor completo de um Style DNA."""
    from .dna import summarize_dna

    _, conn = _open()
    dna = repository.get_style_dna_by_name(conn, name)
    if not dna:
        console.print(f"[red]Style DNA '{name}' nao encontrado[/red]")
        raise typer.Exit(code=1)
    console.print(summarize_dna(dna))
    console.print(f"\n[bold]prompt_fragment[/bold]\n{dna.prompt_fragment}")


# --------------------------------------------------------------------------- #
# geracao
# --------------------------------------------------------------------------- #


@app.command()
def generate(
    template: str = typer.Option(..., "--template", help="Nome do template."),
    dna: Optional[str] = typer.Option(None, "--dna", help="Nome do Style DNA."),
    n: int = typer.Option(1, "--n", help="Quantas imagens."),
    aspect_ratio: Optional[str] = typer.Option(None, "--aspect-ratio"),
    model: Optional[str] = typer.Option(None, "--model"),
    var: Optional[list[str]] = typer.Option(None, "--var", help="chave=valor, repetivel."),
    reference: Optional[str] = typer.Option(None, "--reference", help="IDs de assets, por virgula."),
    use_compositor: bool = typer.Option(False, "--use-compositor"),
    dry_run: bool = typer.Option(
        True, "--dry-run/--execute",
        help="Padrao: modo seco. --execute enfileira e chama a API de verdade.",
    ),
    budget_usd: Optional[float] = typer.Option(None, "--budget-usd"),
) -> None:
    """Resolve o prompt, estima o custo e avalia os guardrails (sem chamar a API)."""
    import asyncio

    from . import capabilities as caps_mod
    from . import pricing
    from .errors import CieError
    from .queue import PlanEntry, build_job, run_queue

    settings, conn = _open()
    entry = PlanEntry(
        template=template,
        dna=dna,
        n=n,
        aspect_ratio=aspect_ratio,
        model=model,
        variables=_parse_vars(var),
        reference_assets=[int(i) for i in reference.split(",")] if reference else [],
        use_compositor=use_compositor,
    )
    capabilities = caps_mod.load(settings)

    try:
        job, report, payload = build_job(conn, settings, entry, capabilities=capabilities)
    except CieError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1)

    console.print(f"[bold]template[/bold] {template}   [bold]dna[/bold] {dna or '-'}")
    console.print(f"[bold]estrategia de referencia[/bold] {payload.strategy}")
    console.print(f"[bold]modelo[/bold] {job.model}   [bold]ar[/bold] {job.aspect_ratio}   "
                  f"[bold]n[/bold] {job.n}")
    console.print()
    console.print("[bold]prompt resolvido[/bold]")
    console.print(job.resolved_prompt)
    console.print()
    estimated = pricing.estimate_cost(job.model, job.n)
    console.print(f"[bold]custo estimado[/bold] US$ {estimated:.4f}")
    if not capabilities.probed:
        console.print(f"[yellow]{capabilities.summary()}[/yellow]")
    console.print()
    _print_guardrails(report)

    if dry_run:
        console.print("\n[dim]modo seco: a API nao foi chamada e nada foi gravado.[/dim]")
        raise typer.Exit(code=1 if report.blocked else 0)

    if report.blocked:
        console.print("\n[red]bloqueado pelos guardrails: nada foi enfileirado.[/red]")
        raise typer.Exit(code=1)

    job_id = repository.insert_job(conn, job)
    console.print(f"\n[green]job {job_id} enfileirado[/green]; executando...")
    result = asyncio.run(run_queue(conn, settings, limit=1, budget_usd=budget_usd))
    for line in result.summary_lines():
        console.print(line)


# --------------------------------------------------------------------------- #
# fila
# --------------------------------------------------------------------------- #


@queue_app.command("add")
def queue_add(
    from_plan: Path = typer.Option(..., "--from-plan", exists=True, help="YAML do plano."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Nao grava; so mostra o que entraria."),
) -> None:
    """Enfileira jobs a partir de um plano semanal."""
    from .errors import CieError
    from .queue import add_jobs_from_plan

    settings, conn = _open()
    try:
        jobs = add_jobs_from_plan(conn, settings, from_plan, dry_run=dry_run)
    except CieError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1)

    table = Table(title=f"{'DRY-RUN ' if dry_run else ''}Plano {from_plan.name}")
    for column in ("job", "template", "n", "status", "motivo"):
        table.add_column(column, overflow="fold")
    for job in jobs:
        template = repository.get_template(conn, job.template_id)
        color = "red" if str(job.status) == "blocked" else "green"
        table.add_row(
            str(job.id or "-"),
            template.name if template else str(job.template_id),
            str(job.n),
            f"[{color}]{job.status}[/{color}]",
            (job.blocked_reason or "")[:80],
        )
    console.print(table)


@queue_app.command("list")
def queue_list(
    status: Optional[str] = typer.Option(None, "--status", help="queued|running|done|failed|blocked"),
    limit: int = typer.Option(50, "--limit"),
) -> None:
    """Mostra a fila."""
    _, conn = _open()
    jobs = repository.list_jobs(conn, status=status, limit=limit)
    if not jobs:
        console.print("[yellow]fila vazia[/yellow]")
        raise typer.Exit(code=0)
    table = Table()
    for column in ("id", "template", "n", "status", "tent.", "US$", "motivo"):
        table.add_column(column, overflow="fold")
    for job in jobs:
        template = repository.get_template(conn, job.template_id)
        table.add_row(
            str(job.id),
            template.name if template else str(job.template_id),
            str(job.n),
            str(job.status),
            str(job.attempts),
            f"{job.cost_usd:.4f}",
            (job.blocked_reason or "")[:60],
        )
    console.print(table)


@queue_app.command("run")
def queue_run(
    limit: int = typer.Option(20, "--limit"),
    budget_usd: Optional[float] = typer.Option(
        None, "--budget-usd", help="Teto rigido: para antes de estourar."
    ),
    dry_run: bool = typer.Option(
        True, "--dry-run/--execute",
        help="Padrao: modo seco. --execute chama a API de verdade.",
    ),
) -> None:
    """Executa a fila respeitando o teto de orcamento."""
    import asyncio

    from .errors import CieError
    from .queue import run_queue

    settings, conn = _open()
    if not dry_run and budget_usd is None:
        console.print(
            "[red]--execute exige --budget-usd[/red] (teto rigido; nada roda sem teto)."
        )
        raise typer.Exit(code=1)

    try:
        result = asyncio.run(
            run_queue(conn, settings, limit=limit, budget_usd=budget_usd, dry_run=dry_run)
        )
    except CieError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1)

    for line in result.summary_lines():
        console.print(line)
    if result.stopped_by_budget:
        console.print(
            f"[yellow]parou no teto de US$ {budget_usd:.2f}: "
            f"{result.pending} job(s) continuam na fila.[/yellow]"
        )


# --------------------------------------------------------------------------- #
# revisao, exportacao e relatorios
# --------------------------------------------------------------------------- #


def _serve(host: str, port: int, path: str = "/") -> None:
    import uvicorn

    from .web.app import create_app

    settings = get_settings()
    open_db(settings)  # garante o banco migrado antes de servir
    console.print(f"[green]CIE em http://{host}:{port}{path}[/green]  (ctrl+c para sair)")
    uvicorn.run(create_app(settings), host=host, port=port, log_level="warning")


@app.command()
def review(
    host: str = typer.Option("127.0.0.1", "--host"),
    port: int = typer.Option(8765, "--port"),
) -> None:
    """Abre a UI de aprovacao/rejeicao das imagens geradas."""
    _serve(host, port, path="/review")


@app.command()
def export(
    approved: bool = typer.Option(True, "--approved/--all"),
    formats: str = typer.Option("9:16,4:5,1:1", "--formats"),
    out: Path = typer.Option(Path("./export"), "--out"),
) -> None:
    """Gera as variantes de publicacao com metadados e manifesto."""
    from .export import export_approved

    settings, conn = _open()
    ratios = tuple(f.strip() for f in formats.split(",") if f.strip())
    if not approved:
        console.print(
            "[yellow]exportar nao aprovadas contraria o fluxo de revisao; "
            "use a UI para aprovar antes.[/yellow]"
        )
        raise typer.Exit(code=1)

    batch = export_approved(conn, settings, formats=ratios, out_dir=out)
    console.print(f"[green]{len(batch.variants)} variante(s)[/green] em {batch.out_dir}")
    console.print(f"manifesto: {batch.manifest_path}")
    console.print(
        "[dim]o manifesto diz o que precisa ser rotulado como IA no Instagram/Meta.[/dim]"
    )


@report_app.command("costs")
def report_costs(
    since: Optional[str] = typer.Option(None, "--since", help="Data ISO, ex.: 2026-08-01"),
    until: Optional[str] = typer.Option(None, "--until"),
    monthly_budget: Optional[float] = typer.Option(None, "--monthly-budget"),
) -> None:
    """Relatorio de custo por modelo, template, pilar e dia."""
    from .reports import budget_forecast, cost_report, render_cost_report

    _, conn = _open()
    report = cost_report(conn, since=since, until=until)
    for table in render_cost_report(report):
        console.print(table)
    if monthly_budget:
        forecast = budget_forecast(report, monthly_budget)
        console.print("\n[bold]projecao[/bold]")
        for key, value in forecast.items():
            console.print(f"  {key:<28} {value}")


# --------------------------------------------------------------------------- #
# API: catalogo de modelos e estado da sondagem
# --------------------------------------------------------------------------- #


@app.command("models")
def models_list() -> None:
    """Catalogo de modelos de imagem e precos conhecidos."""
    from . import pricing

    settings = get_settings()
    _load_probed_pricing(settings)
    table = Table(title="Modelos de imagem")
    for column in ("modelo", "1K", "2K", "max n", "verificado", "fonte"):
        table.add_column(column, overflow="fold")
    for row in pricing.catalog_rows():
        table.add_row(
            str(row["modelo"]),
            f"US$ {row['1k']:.3f}",
            f"US$ {row['2k']:.3f}",
            str(row["max_n"]),
            "[green]sim[/green]" if row["verificado"] else "[yellow]nao[/yellow]",
            str(row["fonte"]),
        )
    console.print(table)
    console.print(
        "[dim]precos nao verificados vem da spec do projeto. Rode "
        "`python scripts/probe_api.py` para confirmar contra a API.[/dim]"
    )


@app.command("probe")
def probe_status() -> None:
    """Mostra o que a sondagem da API descobriu (ou que ela nunca rodou)."""
    from . import capabilities as caps_mod

    settings = get_settings()
    caps = caps_mod.load(settings)
    console.print(f"[bold]sondagem:[/bold] {caps.summary()}")
    if not caps.probed:
        console.print(
            "\n[yellow]Enquanto isso o CIE usa a DescriptorReferenceStrategy: "
            "consistencia vem do Style DNA textual, nao de imagem de referencia.[/yellow]"
        )
        raise typer.Exit(code=0)
    console.print(f"  sondada em            {caps.probed_at}")
    console.print(f"  campo de referencia   {caps.reference_field or '-'}")
    console.print(f"  endpoint              {caps.reference_endpoint or '-'}")
    console.print(f"  max referencias       {caps.max_reference_images}")
    console.print(f"  seed                  {'sim' if caps.supports_seed else 'nao'}")
    console.print(f"  aspect_ratio          {'sim' if caps.supports_aspect_ratio else 'nao'}")
    console.print(f"  n maximo              {caps.max_n}")
    console.print(f"  modelo com visao      {caps.vision_model or '-'}")
    console.print(f"  modelos de imagem     {', '.join(caps.image_models) or '-'}")


if __name__ == "__main__":  # pragma: no cover
    app()
