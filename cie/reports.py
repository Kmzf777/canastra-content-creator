"""Relatorios de custo (fase 5), por tras de `cie report costs`.

Tres perguntas que a operacao faz e este modulo responde:
  * onde o dinheiro foi parar (por modelo, template, pilar e dia);
  * quanto do gasto virou lixo (imagens rejeitadas na revisao humana);
  * quanto custa, de verdade, uma imagem publicavel.

Decisao que atravessa o modulo: o custo por aprovada usa o custo TOTAL do
recorte no numerador, nao apenas o custo das aprovadas. Uma imagem que so ficou
boa na quinta tentativa custou as cinco. E assim que o numero vira argumento de
orcamento, e nao um enfeite.

Todos os numeros saem de `repository.cost_rows`, que ja faz o join
generations -> jobs -> templates; os totais do relatorio sempre fecham com a
soma dos baldes porque vem exatamente das mesmas linhas.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import date
from typing import Callable, Iterable, Sequence

from rich.table import Table

from . import repository
from .enums import Pillar, ReviewStatus
from .utils import parse_dt

#: Dias usados para extrapolar a media diaria observada em um mes. Fixo em 30
#: de proposito: a projecao precisa ser reproduzivel, nao pode mudar de valor
#: so porque o relatorio rodou em fevereiro.
DAYS_PER_MONTH = 30

#: Chave usada quando a linha nao tem modelo/template/dia identificavel.
UNKNOWN_KEY = "desconhecido"
#: Chave usada quando o template nao declara pilar.
NO_PILLAR_KEY = "sem pilar"
#: Texto do estado vazio, igual nas duas renderizacoes.
EMPTY_MESSAGE = "sem dados na janela"

#: Rotulos editoriais dos pilares. So aparecem na renderizacao; as chaves dos
#: baldes continuam sendo o valor cru do enum, que e o que o banco guarda.
PILLAR_LABELS: dict[str, str] = {
    Pillar.P1.value: "Terroir e Tradicao",
    Pillar.P2.value: "Sustentabilidade e Engenharia Agricola",
    Pillar.P3.value: "Laboratorio de Torrefacao e Sensorialidade",
    Pillar.P4.value: "Educacao e Cultura Brewing",
    Pillar.PRODUCT.value: "Produto e embalagem",
    Pillar.PEOPLE.value: "Pessoas da operacao",
}

_BUCKET_HEADERS: tuple[str, ...] = (
    "imagens",
    "custo US$",
    "aprov",
    "rejei",
    "pend",
    "aprovacao",
    "US$/aprovada",
)


# --------------------------------------------------------------------------- #
# estruturas
# --------------------------------------------------------------------------- #


@dataclass
class CostBucket:
    """Um recorte do gasto: um modelo, um template, um pilar ou um dia."""

    key: str
    images: int = 0
    cost_usd: float = 0.0
    approved: int = 0
    rejected: int = 0
    pending: int = 0

    @property
    def reviewed(self) -> int:
        return self.approved + self.rejected

    @property
    def approval_rate(self) -> float:
        """Aprovadas sobre o que ja foi revisado.

        Pendente nao e veredito: uma fila grande de pendentes nao pode derrubar
        a taxa e fazer o modelo parecer pior do que e. Sem revisao, 0.0.
        """
        if not self.reviewed:
            return 0.0
        return self.approved / self.reviewed

    @property
    def cost_per_approved(self) -> float | None:
        """Custo total do balde por imagem aprovada. None quando nao ha aprovada."""
        if not self.approved:
            return None
        return self.cost_usd / self.approved

    def absorb(self, cost_usd: float, review_status: str) -> None:
        """Soma uma geracao ao balde. Status desconhecido conta como pendente."""
        self.images += 1
        self.cost_usd += cost_usd
        if review_status == ReviewStatus.APPROVED:
            self.approved += 1
        elif review_status == ReviewStatus.REJECTED:
            self.rejected += 1
        else:
            self.pending += 1


@dataclass
class CostReport:
    """Fotografia do gasto numa janela de tempo."""

    since: str | None = None
    until: str | None = None
    total_usd: float = 0.0
    images: int = 0
    by_model: list[CostBucket] = field(default_factory=list)
    by_template: list[CostBucket] = field(default_factory=list)
    by_pillar: list[CostBucket] = field(default_factory=list)
    by_day: list[CostBucket] = field(default_factory=list)
    approved_usd: float = 0.0
    rejected_usd: float = 0.0
    pending_usd: float = 0.0
    #: Gasto historico total do banco, ignorando a janela. Serve de contexto
    #: para o orcamento quando o relatorio vem filtrado por `--since`.
    lifetime_usd: float = 0.0

    # Os contadores vem dos baldes por modelo porque essa particao cobre todas
    # as linhas da janela exatamente uma vez.
    @property
    def approved_images(self) -> int:
        return sum(bucket.approved for bucket in self.by_model)

    @property
    def rejected_images(self) -> int:
        return sum(bucket.rejected for bucket in self.by_model)

    @property
    def pending_images(self) -> int:
        return sum(bucket.pending for bucket in self.by_model)

    @property
    def waste_ratio(self) -> float:
        """Fracao do custo que foi para o lixo. Banco vazio nao divide por zero."""
        if self.total_usd <= 0.0:
            return 0.0
        return self.rejected_usd / self.total_usd

    @property
    def cost_per_approved(self) -> float | None:
        approved = self.approved_images
        if not approved:
            return None
        return self.total_usd / approved

    @property
    def observed_days(self) -> int:
        """Dias de calendario cobertos, do primeiro ao ultimo dia com gasto.

        Contar apenas os dias que tiveram geracao inflaria a media diaria: quem
        gerou em dois dias espalhados por um mes gasta pouco por dia, nao muito.
        O intervalo e fechado nas duas pontas, entao um unico dia vale 1.
        """
        parsed: list[date] = []
        unparsed = 0
        for bucket in self.by_day:
            try:
                parsed.append(date.fromisoformat(bucket.key))
            except ValueError:
                unparsed += 1
        if not parsed:
            return unparsed
        span = (max(parsed) - min(parsed)).days + 1
        return span + unparsed

    @property
    def window_label(self) -> str:
        return f"{self.since or 'inicio'} .. {self.until or 'agora'}"


# --------------------------------------------------------------------------- #
# agregacao
# --------------------------------------------------------------------------- #


def _text(value: object, fallback: str) -> str:
    text = str(value).strip() if value is not None else ""
    return text or fallback


def _day_key(row: sqlite3.Row) -> str:
    parsed = parse_dt(row["created_at"])
    if parsed is not None:
        return parsed.date().isoformat()
    return _text((row["created_at"] or "")[:10], UNKNOWN_KEY)


def _accumulate(
    rows: Iterable[sqlite3.Row], key_of: Callable[[sqlite3.Row], str]
) -> list[CostBucket]:
    buckets: dict[str, CostBucket] = {}
    for row in rows:
        key = key_of(row)
        bucket = buckets.get(key)
        if bucket is None:
            bucket = buckets[key] = CostBucket(key=key)
        bucket.absorb(float(row["cost_usd"] or 0.0), str(row["review_status"] or ""))
    return list(buckets.values())


def _by_cost(buckets: list[CostBucket]) -> list[CostBucket]:
    """Mais caro primeiro; empate desempata por chave, para saida estavel."""
    return sorted(buckets, key=lambda b: (-b.cost_usd, b.key))


def _by_key(buckets: list[CostBucket]) -> list[CostBucket]:
    return sorted(buckets, key=lambda b: b.key)


def cost_report(
    conn: sqlite3.Connection, since: str | None = None, until: str | None = None
) -> CostReport:
    """Agrega o gasto da janela `[since, until]` (datas ISO, comparadas como texto)."""
    rows = repository.cost_rows(conn, since, until)

    approved_usd = rejected_usd = pending_usd = 0.0
    total_usd = 0.0
    for row in rows:
        cost = float(row["cost_usd"] or 0.0)
        total_usd += cost
        status = str(row["review_status"] or "")
        if status == ReviewStatus.APPROVED:
            approved_usd += cost
        elif status == ReviewStatus.REJECTED:
            rejected_usd += cost
        else:
            pending_usd += cost

    return CostReport(
        since=since,
        until=until,
        total_usd=total_usd,
        images=len(rows),
        by_model=_by_cost(_accumulate(rows, lambda r: _text(r["model"], UNKNOWN_KEY))),
        by_template=_by_cost(
            _accumulate(rows, lambda r: _text(r["template_name"], UNKNOWN_KEY))
        ),
        by_pillar=_by_cost(_accumulate(rows, lambda r: _text(r["pillar"], NO_PILLAR_KEY))),
        by_day=_by_key(_accumulate(rows, _day_key)),
        approved_usd=approved_usd,
        rejected_usd=rejected_usd,
        pending_usd=pending_usd,
        lifetime_usd=repository.total_cost(conn),
    )


# --------------------------------------------------------------------------- #
# formatacao
# --------------------------------------------------------------------------- #


def _usd(value: float) -> str:
    # Quatro casas: uma imagem custa centavos, duas casas esconderiam a diferenca.
    return f"{value:.4f}"


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _optional_usd(value: float | None) -> str:
    return _usd(value) if value is not None else "-"


def _pillar_display(key: str) -> str:
    label = PILLAR_LABELS.get(key)
    return f"{key} {label}" if label else key


def _bucket_cells(bucket: CostBucket, display: Callable[[str], str]) -> list[str]:
    return [
        display(bucket.key),
        str(bucket.images),
        _usd(bucket.cost_usd),
        str(bucket.approved),
        str(bucket.rejected),
        str(bucket.pending),
        _pct(bucket.approval_rate),
        _optional_usd(bucket.cost_per_approved),
    ]


def _summary_rows(report: CostReport) -> list[tuple[str, str]]:
    rows = [
        ("janela", report.window_label),
        ("imagens", str(report.images)),
        ("custo total US$", _usd(report.total_usd)),
        ("aprovadas US$", f"{_usd(report.approved_usd)} ({report.approved_images} img)"),
        ("rejeitadas US$", f"{_usd(report.rejected_usd)} ({report.rejected_images} img)"),
        ("pendentes US$", f"{_usd(report.pending_usd)} ({report.pending_images} img)"),
        ("desperdicio", _pct(report.waste_ratio)),
        ("custo por aprovada US$", _optional_usd(report.cost_per_approved)),
        ("dias observados", str(report.observed_days)),
    ]
    if report.since or report.until:
        rows.append(("gasto historico US$", _usd(report.lifetime_usd)))
    return rows


#: (titulo, atributo do relatorio, rotulo da 1a coluna, formatador da chave)
_SECTIONS: tuple[tuple[str, str, str, Callable[[str], str]], ...] = (
    ("Custo por modelo", "by_model", "modelo", str),
    ("Custo por template", "by_template", "template", str),
    ("Custo por pilar", "by_pillar", "pilar", _pillar_display),
    ("Custo por dia", "by_day", "dia", str),
)


def render_cost_report(report: CostReport) -> list[Table]:
    """Tabelas rich prontas para a CLI imprimir: resumo + os quatro recortes."""
    summary = Table(title="Custo CIE - resumo")
    summary.add_column("metrica", overflow="fold")
    summary.add_column("valor", justify="right", overflow="fold")
    for label, value in _summary_rows(report):
        summary.add_row(label, value)

    tables = [summary]
    for title, attribute, column, display in _SECTIONS:
        table = Table(title=title)
        table.add_column(column, overflow="fold")
        for header in _BUCKET_HEADERS:
            table.add_column(header, justify="right")
        buckets: list[CostBucket] = getattr(report, attribute)
        for bucket in buckets:
            table.add_row(*_bucket_cells(bucket, display))
        if not buckets:
            # Legenda em vez de linha falsa: com oito colunas, uma linha de aviso
            # quebra em quatro no terminal estreito.
            table.caption = EMPTY_MESSAGE
        tables.append(table)
    return tables


def _text_table(title: str, headers: Sequence[str], rows: Sequence[Sequence[str]]) -> list[str]:
    """Tabela de largura fixa, sem rich: a saida precisa ser identica em CI."""
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def line(cells: Sequence[str]) -> str:
        first = cells[0].ljust(widths[0])
        rest = [cell.rjust(widths[index + 1]) for index, cell in enumerate(cells[1:])]
        return "  ".join([first, *rest]).rstrip()

    out = [title, line(headers), "-" * max(len(line(headers)), len(title))]
    if rows:
        out.extend(line(row) for row in rows)
    else:
        out.append(EMPTY_MESSAGE)
    return out


def render_cost_report_text(report: CostReport) -> str:
    """Versao texto puro do relatorio, para arquivo, e-mail ou log de CI."""
    lines: list[str] = ["Custo CIE - resumo"]
    label_width = max(len(label) for label, _ in _summary_rows(report))
    for label, value in _summary_rows(report):
        lines.append(f"  {label.ljust(label_width)}  {value}")

    for title, attribute, column, display in _SECTIONS:
        buckets: list[CostBucket] = getattr(report, attribute)
        rows = [_bucket_cells(bucket, display) for bucket in buckets]
        lines.append("")
        lines.extend(_text_table(title, (column, *_BUCKET_HEADERS), rows))
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# projecao de orcamento
# --------------------------------------------------------------------------- #


def budget_forecast(report: CostReport, monthly_budget_usd: float) -> dict[str, float | int]:
    """Projeta o mes a partir da media diaria observada.

    `folga_ou_estouro` e orcamento menos projecao: positivo sobra, negativo
    estoura. Janela vazia devolve zeros - relatorio de banco vazio nao divide
    por zero nem inventa tendencia.
    """
    days = report.observed_days
    daily = report.total_usd / days if days else 0.0
    projected = daily * DAYS_PER_MONTH
    per_dollar = report.approved_images / report.total_usd if report.total_usd > 0 else 0.0
    return {
        "dias_observados": days,
        "media_diaria": round(daily, 4),
        "projecao_mensal": round(projected, 4),
        "folga_ou_estouro": round(monthly_budget_usd - projected, 4),
        "imagens_aprovadas_por_dolar": round(per_dollar, 2),
    }
