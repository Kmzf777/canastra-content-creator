"""Provedor xAI (Grok Imagine) - `/images/generations` e `/images/edits`.

Portado de `_ref-scripts/teste_final.py` (fonte unica) e `_ref-scripts/espontaneo.py`
(multi-fonte), com o formato descoberto por `_ref-scripts/sonda.py` e
`_ref-scripts/sonda_multi.py`. O que este modulo existe para nao deixar esquecer:

**O formato da referencia.** Sao dois campos diferentes e mutuamente exclusivos:

```jsonc
"image":  { "url": "data:image/jpeg;base64,...", "type": "image_url" }   // 1 fonte, OBJETO
"images": [ {"url": "...", "type": "image_url"}, ... ]                    // 2+ fontes, PLURAL
```

Mandar os dois juntos devolve 400 - e foi esse 400 que revelou o esquema:
*"provide either the `image` field or the `images` field, but not both"*.
`image` em lista existe, mas exige **strings**; lista de objetos da 422.

**A armadilha cara.** `image_url` em `/images/edits` devolve **HTTP 200 e ignora
a imagem**: o endpoint gera so do texto e nada denuncia que o guidance nunca
chegou. O mesmo vale para `reference_images`, `input_images` e `image_urls`.
Duas rodadas de geracao morreram nisso. Por isso `CAMPOS_PROIBIDOS` e varrido
sobre o payload montado antes de qualquer POST - status 200 nao prova nada.

**`4:5` nao existe aqui.** Feed do Instagram se resolve gerando em `3:4` e
recortando a altura com `recortar_4x5` (ou de uma vez com `gerar_4x5`).
"""

from __future__ import annotations

import base64
import io
import json
import os
from pathlib import Path
from typing import Any, Sequence

import httpx
from PIL import Image, ImageOps

from .base import (
    ErroProvedor,
    FonteInvalida,
    ProvedorBase,
    Requisicao,
    fazer_redator,
)

BASE_URL_PADRAO = "https://api.x.ai/v1"
ENDPOINT_GENERATIONS = "/images/generations"
ENDPOINT_EDITS = "/images/edits"

MODELO_PADRAO = "grok-imagine-image-2.0"
QUALIDADE_PADRAO = "medium"
RESOLUCAO_PADRAO = "2k"

#: `high` devolve 400 no 2.0 - confirmado em `sonda.py`. Em medium/2k sai 1776x2368.
QUALIDADES_VALIDAS = frozenset({"low", "medium"})
RESOLUCOES_VALIDAS = frozenset({"1k", "2k"})

#: Enumeradas pela propria API no 422 de `aspect_ratio: "0:0"`.
#: **`4:5` nao esta na lista e nunca estara** - use `gerar_4x5`.
PROPORCOES_VALIDAS = frozenset(
    {
        "1:1", "3:4", "4:3", "9:16", "16:9", "2:3", "3:2",
        "9:19.5", "19.5:9", "9:20", "20:9", "1:2", "2:1", "auto",
    }
)

#: Aceitos com HTTP 200 e ignorados em silencio. Emitir qualquer um destes
#: significa gerar uma imagem paga que nunca viu a foto de referencia.
CAMPOS_PROIBIDOS = ("image_url", "image_urls", "reference_images", "input_images")

#: A doc fala em 3; `sonda_multi.py` passou por 4 sem reclamacao.
LIMITE_FONTES = 4

#: Lado maior da referencia em pixels. 2048 foi o maior testado sem erro.
LADO_FONTE = 2048

#: Fracao da sobra de altura que sai do TOPO ao recortar 3:4 -> 4:5.
#: 0.62 e o valor de `teste_final.py`: tira mais ceu que chao, porque o assunto
#: costuma sentar na metade de baixo do quadro.
FRACAO_TOPO_4X5 = 0.62

#: Quanto do corpo de erro sobrevive na excecao: o bastante para auditar, pouco
#: o bastante para nao despejar um base64 inteiro no terminal.
LIMITE_ERRO_CHARS = 2000


class ErroXai(ErroProvedor):
    """Falha da API da xAI, com o corpo bruto ja redigido em `raw`."""


class ProvedorXai(ProvedorBase):
    """Cliente de imagem da xAI.

    A chave vive apenas em dois closures (`_montar_headers` e `_redigir`): nao
    vira atributo, nao entra em `repr`, nao aparece em traceback.
    """

    PROPORCOES_VALIDAS = PROPORCOES_VALIDAS
    CAMPOS_PROIBIDOS = CAMPOS_PROIBIDOS
    nome = "xai"

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        modelo: str = MODELO_PADRAO,
        qualidade: str = QUALIDADE_PADRAO,
        resolucao: str = RESOLUCAO_PADRAO,
        transport: httpx.BaseTransport | None = None,
        timeout: float = 600.0,
    ) -> None:
        chave = (api_key if api_key is not None else os.environ.get("XAI_API_KEY", "")).strip()
        if not chave:
            raise ErroXai(
                "XAI_API_KEY ausente. Defina no ambiente ou em .env (veja .env.example). "
                "A chave nunca e impressa pelo CIE."
            )
        if qualidade not in QUALIDADES_VALIDAS:
            raise ErroXai(
                f"quality={qualidade!r} invalido; a API aceita "
                f"{', '.join(sorted(QUALIDADES_VALIDAS))} (high devolve 400)"
            )
        if resolucao not in RESOLUCOES_VALIDAS:
            raise ErroXai(
                f"resolution={resolucao!r} invalido; a API aceita "
                f"{', '.join(sorted(RESOLUCOES_VALIDAS))}"
            )

        self.base_url = (base_url or os.environ.get("CIE_XAI_BASE_URL") or BASE_URL_PADRAO).rstrip("/")
        self.modelo = modelo
        self.qualidade = qualidade
        self.resolucao = resolucao
        self.timeout = timeout
        self._transport = transport
        self._redigir = fazer_redator(chave)
        # A chave so existe aqui dentro.
        self._montar_headers = lambda: {
            "Authorization": f"Bearer {chave}",
            "Content-Type": "application/json",
        }

    def __repr__(self) -> str:  # pragma: no cover - conveniencia de depuracao
        return f"ProvedorXai(base_url={self.base_url!r}, modelo={self.modelo!r})"

    # ----------------------------------------------------------------- #
    # montagem (sem rede - e o que os testes inspecionam)
    # ----------------------------------------------------------------- #

    def endpoint_de(self, req: Requisicao) -> str:
        """Com fonte e edicao; sem fonte e geracao pura."""
        return ENDPOINT_EDITS if req.fontes else ENDPOINT_GENERATIONS

    def montar_payload(self, req: Requisicao) -> dict[str, Any]:
        """Monta o corpo do POST. Levanta antes de qualquer rede se algo estiver errado.

        Aqui mora a regra que custou duas rodadas: uma fonte vai em `image` como
        OBJETO; duas ou mais vao em `images` (plural). Nunca `image_url`.
        """
        aspecto = self.validar_proporcao(req.aspecto)
        fontes = self.validar_fontes(req.fontes)
        if len(fontes) > LIMITE_FONTES:
            raise FonteInvalida(
                f"{len(fontes)} fontes: a xAI foi testada com no maximo {LIMITE_FONTES}"
            )

        payload: dict[str, Any] = {
            "model": req.modelo or self.modelo,
            "prompt": req.prompt,
            "n": req.n,
            "quality": self.qualidade,
            "resolution": self.resolucao,
        }
        if aspecto is not None:
            # Com multiplas fontes isto e advisory: a saida herda a proporcao da
            # primeira fonte. Medido, nao inferido.
            payload["aspect_ratio"] = aspecto

        refs = [self.referencia(f) for f in fontes]
        if len(refs) > 1:
            payload["images"] = refs          # PLURAL, lista de objetos
        elif refs:
            payload["image"] = refs[0]        # SINGULAR, objeto - nunca lista

        payload.update(req.extra)
        return self.checar_campos_proibidos(payload)

    @staticmethod
    def referencia(caminho: Path, lado: int = LADO_FONTE) -> dict[str, str]:
        """Uma fonte no formato que a API de fato honra: objeto com `url` e `type`."""
        return {"url": data_uri(caminho, lado), "type": "image_url"}

    # ----------------------------------------------------------------- #
    # rede
    # ----------------------------------------------------------------- #

    def gerar(
        self,
        prompt: str,
        fontes: Sequence[Path] = (),
        aspecto: str | None = None,
        n: int = 1,
    ) -> list[bytes]:
        return self.executar(
            Requisicao(prompt=prompt, fontes=tuple(fontes), aspecto=aspecto, n=n)
        )

    def gerar_4x5(
        self,
        prompt: str,
        fontes: Sequence[Path] = (),
        n: int = 1,
    ) -> list[bytes]:
        """Feed do Instagram: gera em `3:4` (o valido mais alto) e recorta para 4:5.

        Existe porque `4:5` nao e uma proporcao da xAI. Perda de ~6% da altura.
        """
        brutas = self.gerar(prompt, fontes=fontes, aspecto="3:4", n=n)
        return [recortar_4x5(b) for b in brutas]

    def executar(self, req: Requisicao) -> list[bytes]:
        payload = self.montar_payload(req)
        caminho = self.endpoint_de(req)
        with self._cliente() as cliente:
            resposta = self._post(cliente, caminho, payload)
        return self._imagens(resposta, caminho)

    def _cliente(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.base_url,
            headers=self._montar_headers(),
            timeout=self.timeout,
            transport=self._transport,
        )

    def _post(self, cliente: httpx.Client, caminho: str, payload: dict[str, Any]) -> httpx.Response:
        try:
            resposta = cliente.post(caminho, json=payload)
        except httpx.HTTPError as exc:
            raise ErroXai(f"falha de rede em {caminho}: {self._redigir(str(exc))}") from exc
        if resposta.status_code != 200:
            raise self._erro(resposta, caminho)
        return resposta

    def _erro(self, resposta: httpx.Response, caminho: str) -> ErroXai:
        bruto = self._redigir(_texto(resposta))
        return ErroXai(
            f"xAI {caminho} devolveu {resposta.status_code}: {_mensagem(bruto)}",
            status_code=resposta.status_code,
            raw=bruto[:LIMITE_ERRO_CHARS],
        )

    def _imagens(self, resposta: httpx.Response, caminho: str) -> list[bytes]:
        try:
            corpo = resposta.json()
        except ValueError as exc:
            raise ErroXai(
                f"xAI {caminho} devolveu 200 com corpo nao-JSON",
                status_code=200,
                raw=self._redigir(_texto(resposta))[:LIMITE_ERRO_CHARS],
            ) from exc

        itens = corpo.get("data") or []
        if not itens:
            raise ErroXai(
                f"xAI {caminho} devolveu 200 sem imagem alguma",
                status_code=200,
                raw=self._redigir(json.dumps(corpo, ensure_ascii=False))[:LIMITE_ERRO_CHARS],
            )

        saida: list[bytes] = []
        for item in itens:
            b64 = item.get("b64_json")
            if b64:
                try:
                    saida.append(base64.b64decode(b64))
                except (ValueError, TypeError) as exc:
                    raise ErroXai("base64 invalido no campo b64_json", status_code=200) from exc
                continue
            url = item.get("url")
            if not url:
                raise ErroXai(
                    "item de resposta sem b64_json e sem url",
                    status_code=200,
                    raw=self._redigir(json.dumps(item, ensure_ascii=False))[:LIMITE_ERRO_CHARS],
                )
            saida.append(self._baixar(url))
        return saida

    def _baixar(self, url: str) -> bytes:
        """Baixa a imagem SEM o header de autenticacao.

        A url vem da resposta da API e aponta para um host que nao e o da API.
        Reaproveitar o cliente autenticado mandaria a chave para esse host.
        """
        try:
            with httpx.Client(timeout=self.timeout, transport=self._transport) as anonimo:
                r = anonimo.get(url)
        except httpx.HTTPError as exc:
            raise ErroXai(f"falha ao baixar imagem: {self._redigir(str(exc))}") from exc
        if r.status_code != 200:
            raise ErroXai(
                f"download da imagem devolveu {r.status_code}",
                status_code=r.status_code,
                raw=self._redigir(_texto(r))[:LIMITE_ERRO_CHARS],
            )
        return r.content


# --------------------------------------------------------------------------- #
# utilitarios de imagem (sem rede)
# --------------------------------------------------------------------------- #


def data_uri(caminho: Path, lado: int = LADO_FONTE) -> str:
    """Le a foto, corrige orientacao EXIF, limita o lado maior e vira data URI.

    `exif_transpose` nao e detalhe: foto de celular vem deitada com a rotacao no
    EXIF, e a API le o pixel, nao o metadado.
    """
    caminho = Path(caminho)
    try:
        with Image.open(caminho) as aberta:
            imagem = ImageOps.contain(
                ImageOps.exif_transpose(aberta).convert("RGB"), (lado, lado)
            )
    except OSError as exc:
        raise FonteInvalida(f"nao consegui ler a fonte {caminho}: {exc}") from exc
    buffer = io.BytesIO()
    imagem.save(buffer, "JPEG", quality=96)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def recortar_4x5(bruto: bytes, fracao_topo: float = FRACAO_TOPO_4X5) -> bytes:
    """Recorta a altura ate 4:5, tirando `fracao_topo` da sobra pelo topo.

    Imagem que ja seja 4:5 ou mais larga volta intacta.
    """
    with Image.open(io.BytesIO(bruto)) as aberta:
        imagem = aberta.convert("RGB")
        alvo = imagem.width * 5 / 4
        if imagem.height > alvo:
            topo = int((imagem.height - alvo) * fracao_topo)
            imagem = imagem.crop((0, topo, imagem.width, int(topo + alvo)))
        saida = io.BytesIO()
        imagem.save(saida, "JPEG", quality=96)
    return saida.getvalue()


def _texto(resposta: httpx.Response) -> str:
    try:
        return resposta.text
    except Exception:  # pragma: no cover - corpo binario ou encoding torto
        return "<corpo ilegivel>"


def _mensagem(bruto: str) -> str:
    """Extrai `error.message` quando o corpo e JSON; senao devolve o texto cru."""
    try:
        corpo = json.loads(bruto)
    except (ValueError, TypeError):
        return bruto[:300]
    erro = corpo.get("error", corpo) if isinstance(corpo, dict) else corpo
    if isinstance(erro, dict):
        erro = erro.get("message", erro)
    return str(erro)[:300]


__all__ = [
    "BASE_URL_PADRAO",
    "CAMPOS_PROIBIDOS",
    "ENDPOINT_EDITS",
    "ENDPOINT_GENERATIONS",
    "FRACAO_TOPO_4X5",
    "LIMITE_FONTES",
    "MODELO_PADRAO",
    "PROPORCOES_VALIDAS",
    "QUALIDADE_PADRAO",
    "RESOLUCAO_PADRAO",
    "ErroXai",
    "ProvedorXai",
    "data_uri",
    "recortar_4x5",
]
