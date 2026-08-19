"""Contrato comum dos provedores de imagem.

**Este modulo nao fala com a rede.** So tipos, validacao e redacao de segredo.
Quem faz HTTP e `cie.providers.xai` e `cie.providers.gemini`; manter a fronteira
significa que a parte do sistema que decide *o que* pedir pode ser testada sem
um unico byte de trafego - e sem um unico centavo de credito.

Tres invariantes que os provedores concretos herdam deste arquivo:

1. **A chave nunca aparece em texto.** Toda mensagem de erro passa por um
   redator montado por `fazer_redator`. A API devolve a chave dentro do corpo de
   alguns erros; sem redacao ela vaza para o terminal, para o log e para o banco.
2. **Enum invalido morre antes da rede.** Ja aconteceu de `aspect_ratio: "4:5"`
   envenenar uma varredura inteira de sondagem na xAI (registro de licoes #4).
   Validar em memoria custa zero; descobrir pelo 422 custa uma rodada.
3. **Nenhum campo inventado.** Cada provedor declara em `CAMPOS_PROIBIDOS` os
   nomes que a API aceita com HTTP 200 e ignora em silencio. O payload montado e
   varrido contra essa lista por `checar_campos_proibidos` antes de sair.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Protocol, Sequence, runtime_checkable

from ..errors import CieError

#: Substituto da chave em qualquer texto que possa ser exibido ou persistido.
MARCA_REDACAO = "***"

#: Abaixo disto nao vale a pena redigir: um fragmento curto demais casaria com
#: pedacos legitimos do corpo da resposta.
MINIMO_REDIGIVEL = 8


# --------------------------------------------------------------------------- #
# erros
# --------------------------------------------------------------------------- #


class ErroProvedor(CieError):
    """Falha de um provedor de imagem.

    `raw` guarda o corpo bruto (ja redigido) para auditoria - o mesmo contrato de
    `cie.errors.XaiApiError`, mas valendo para qualquer provedor.
    """

    def __init__(self, mensagem: str, *, status_code: int | None = None, raw: str = "") -> None:
        self.status_code = status_code
        self.raw = raw
        super().__init__(mensagem)


class ProporcaoInvalida(ErroProvedor):
    """A proporcao pedida nao existe neste provedor.

    Levantada **antes** de qualquer chamada de rede: requisicao com enum errado
    nao gera imagem, e descobrir isso pelo 422 gasta tempo de rodada.
    """

    def __init__(self, proporcao: str, validas: Iterable[str], *, provedor: str = "") -> None:
        self.proporcao = proporcao
        self.validas = tuple(sorted(validas))
        onde = f" em {provedor}" if provedor else ""
        super().__init__(
            f"proporcao {proporcao!r} nao existe{onde}. "
            f"Validas: {', '.join(self.validas)}"
        )


class FonteInvalida(ErroProvedor):
    """Arquivo de referencia ausente, ilegivel ou em quantidade nao suportada."""


class CampoProibido(ErroProvedor):
    """O payload montado carrega um campo que a API aceita e ignora em silencio.

    Este erro e uma rede de seguranca interna: se ele dispara em producao, alguem
    reintroduziu `image_url` (ou parente) no construtor do payload.
    """


# --------------------------------------------------------------------------- #
# redacao
# --------------------------------------------------------------------------- #


def fazer_redator(*segredos: str | None) -> Callable[[str], str]:
    """Devolve `redigir(texto)` que troca cada segredo por `***`.

    Os segredos vivem no closure, nunca em atributo do provedor: `repr()`,
    `vars()` e um traceback do pytest nao os alcancam.
    """
    alvos = tuple(s for s in segredos if s and len(s) >= MINIMO_REDIGIVEL)

    def redigir(texto: str) -> str:
        for alvo in alvos:
            if alvo in texto:
                texto = texto.replace(alvo, MARCA_REDACAO)
        return texto

    return redigir


# --------------------------------------------------------------------------- #
# requisicao
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Requisicao:
    """Um pedido de imagem, independente de provedor.

    `aspecto=None` significa "nao mande o campo" - deixa o default do provedor
    valer, em vez de chutar um valor. Em `/images/edits` da xAI com multiplas
    fontes o aspecto e advisory de qualquer jeito: a saida herda a proporcao da
    primeira fonte.
    """

    prompt: str
    fontes: tuple[Path, ...] = ()
    aspecto: str | None = None
    n: int = 1
    modelo: str | None = None
    #: Campos extras enviados literalmente. Porta unica para parametro que ainda
    #: nao foi confirmado por sondagem - e que por isso nao merece um atributo.
    extra: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # frozen=True: normalizacao vai por object.__setattr__.
        object.__setattr__(self, "fontes", tuple(Path(f) for f in self.fontes))
        if not self.prompt or not self.prompt.strip():
            raise ErroProvedor("prompt vazio: o provedor geraria uma imagem aleatoria")
        if self.n < 1:
            raise ErroProvedor(f"n={self.n} invalido: pelo menos uma imagem por pedido")

    @property
    def multifonte(self) -> bool:
        return len(self.fontes) > 1

    def com(self, **mudancas: Any) -> "Requisicao":
        """Copia com campos trocados (o dataclass e imutavel de proposito)."""
        dados: dict[str, Any] = {
            "prompt": self.prompt,
            "fontes": self.fontes,
            "aspecto": self.aspecto,
            "n": self.n,
            "modelo": self.modelo,
            "extra": dict(self.extra),
        }
        dados.update(mudancas)
        return Requisicao(**dados)


# --------------------------------------------------------------------------- #
# contrato
# --------------------------------------------------------------------------- #


@runtime_checkable
class Provider(Protocol):
    """O que todo provedor de imagem sabe fazer.

    Protocolo estrutural: `isinstance(obj, Provider)` confere a forma, sem exigir
    heranca. `ProvedorBase` existe para quem quiser herdar o utilitario comum.
    """

    nome: str

    def gerar(
        self,
        prompt: str,
        fontes: Sequence[Path] = (),
        aspecto: str | None = None,
        n: int = 1,
    ) -> list[bytes]:
        """Gera `n` imagens e devolve os bytes de cada uma, na ordem da resposta."""
        ...


class ProvedorBase(ABC):
    """Base concreta opcional: validacao de proporcao e de fonte, sem rede."""

    #: Proporcoes aceitas pela API. Medidas por erro 422, nao inferidas.
    PROPORCOES_VALIDAS: frozenset[str] = frozenset()
    #: Campos que a API aceita com 200 e ignora - nunca podem ser emitidos.
    CAMPOS_PROIBIDOS: tuple[str, ...] = ()
    nome: str = "base"

    def validar_proporcao(self, aspecto: str | None) -> str | None:
        """Devolve o aspecto se ele existir na API; senao levanta antes da rede."""
        if aspecto is None:
            return None
        if aspecto not in self.PROPORCOES_VALIDAS:
            raise ProporcaoInvalida(aspecto, self.PROPORCOES_VALIDAS, provedor=self.nome)
        return aspecto

    def validar_fontes(self, fontes: Sequence[Path]) -> tuple[Path, ...]:
        caminhos = tuple(Path(f) for f in fontes)
        faltando = [str(p) for p in caminhos if not p.is_file()]
        if faltando:
            raise FonteInvalida(
                "fonte de referencia inexistente: " + ", ".join(faltando)
            )
        return caminhos

    def checar_campos_proibidos(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Varre o payload (incluindo aninhados) atras de campo silenciosamente ignorado."""
        achados = sorted(_chaves_proibidas(payload, self.CAMPOS_PROIBIDOS))
        if achados:
            raise CampoProibido(
                f"payload de {self.nome} carrega campo que a API ignora em silencio: "
                f"{', '.join(achados)}"
            )
        return payload

    @abstractmethod
    def gerar(
        self,
        prompt: str,
        fontes: Sequence[Path] = (),
        aspecto: str | None = None,
        n: int = 1,
    ) -> list[bytes]:
        ...


def _chaves_proibidas(valor: Any, proibidos: tuple[str, ...]) -> set[str]:
    """Nomes proibidos encontrados em qualquer profundidade da estrutura."""
    achados: set[str] = set()
    if isinstance(valor, dict):
        for chave, sub in valor.items():
            if chave in proibidos:
                achados.add(chave)
            achados |= _chaves_proibidas(sub, proibidos)
    elif isinstance(valor, (list, tuple)):
        for item in valor:
            achados |= _chaves_proibidas(item, proibidos)
    return achados


__all__ = [
    "MARCA_REDACAO",
    "CampoProibido",
    "ErroProvedor",
    "FonteInvalida",
    "ProporcaoInvalida",
    "Provider",
    "ProvedorBase",
    "Requisicao",
    "fazer_redator",
]
