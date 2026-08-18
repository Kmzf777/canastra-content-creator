"""Hierarquia de erros do CIE.

Nada aqui carrega a chave da API: mensagens passam por `config.redact` antes de
chegar ao usuario. Erro de API nunca e engolido - vira `XaiApiError` com o corpo
bruto preservado em `raw`.
"""

from __future__ import annotations


class CieError(Exception):
    """Base de todos os erros do sistema."""


class GuardrailViolation(CieError):
    """Uma regra de `cie.guardrails` bloqueou a geracao antes de gastar credito."""

    def __init__(self, rule: str, message: str, remedy: str = "") -> None:
        self.rule = rule
        self.remedy = remedy
        full = f"[{rule}] {message}"
        if remedy:
            full += f"\n  como resolver: {remedy}"
        super().__init__(full)


class TemplateError(CieError):
    """Template YAML invalido ou placeholder nao resolvido."""


class XaiApiError(CieError):
    """Falha na API da xAI. `raw` guarda a resposta bruta para auditoria."""

    def __init__(self, message: str, *, status_code: int | None = None, raw: str = "") -> None:
        self.status_code = status_code
        self.raw = raw
        super().__init__(message)


class RateLimitError(XaiApiError):
    """429. `retry_after` vem do cabecalho quando presente."""

    def __init__(self, message: str, *, retry_after: float | None = None, raw: str = "") -> None:
        self.retry_after = retry_after
        super().__init__(message, status_code=429, raw=raw)


class BudgetExceeded(CieError):
    """O teto de `--budget-usd` foi atingido; a fila para antes de estourar."""

    def __init__(self, spent: float, budget: float, pending: int) -> None:
        self.spent = spent
        self.budget = budget
        self.pending = pending
        super().__init__(
            f"teto de orcamento atingido: US$ {spent:.4f} de US$ {budget:.2f}; "
            f"{pending} job(s) continuam na fila"
        )


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
