"""Provedor Gemini (Nano Banana Pro) - `generativelanguage/v1beta:generateContent`.

Portado de `_ref-scripts/gemini_gerar.py` e `_ref-scripts/gemini_cadeira_dna.py`,
com os modelos confirmados por `_ref-scripts/sonda_gemini.py`. O que este modulo
carrega de conhecimento comprado a preco de rodada:

**Auth e por cabecalho `x-goog-api-key`.** A credencial deste projeto comeca com
`AQ.`, que parece access token OAuth e convida ao `Authorization: Bearer` -
e devolve **401**. `montar_headers()` existe justamente para esse cabecalho ser
inspecionavel por teste, sem depender de subir uma requisicao.

**`4:5` e nativo aqui**, ao contrario da xAI. Feed do Instagram sai direto, sem
recorte. `imageConfig.imageSize: "2K"` funciona e sai 1856x2304 pelo mesmo preco
do 1K; os campos `resolution` e `outputImageSize` **nao existem** e devolvem 400.

**O Gemini redesenha o rotulo.** Ele trata a referencia como inspiracao, nao como
edicao - por isso o fluxo de fidelidade de marca e a xAI em `/images/edits`, e o
Gemini fica com a cena onde o ambiente e o assunto. Quando a embalagem tiver que
aparecer, o prompt precisa citar cada string entre aspas e soletrada; mesmo assim
erra ~1 em 3, entao peca 2-3 variantes (`n`) e escolha.
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

BASE_URL_PADRAO = "https://generativelanguage.googleapis.com/v1beta"

#: O cabecalho de autenticacao. `Authorization: Bearer` devolve 401 - nao trocar.
HEADER_AUTH = "x-goog-api-key"

#: Nao existe `3.1-pro-image`: o Pro de imagem mais atual e `gemini-3-pro-image`.
MODELO_PADRAO = "gemini-3-pro-image"
MODELOS_IMAGEM = (
    "gemini-2.5-flash-image",
    "gemini-3-pro-image",
    "nano-banana-pro-preview",
    "gemini-3.1-flash-image",
    "gemini-3.1-flash-lite-image",
)

#: `4:5` esta aqui - e a diferenca operacional em relacao a xAI.
PROPORCOES_VALIDAS = frozenset(
    {"1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"}
)

TAMANHOS_VALIDOS = frozenset({"1K", "2K", "4K"})
TAMANHO_PADRAO = "2K"
ASPECTO_PADRAO = "4:5"

#: Nomes plausiveis que a API rejeita com 400. Ficam na lista de proibidos para
#: que ninguem os reintroduza achando que sao sinonimos de `imageSize`.
CAMPOS_PROIBIDOS = ("resolution", "outputImageSize", "output_image_size")

#: Lado maior da referencia. 2048 e o usado no fluxo de DNA blindado.
LADO_FONTE = 2048

LIMITE_ERRO_CHARS = 2000


class ErroGemini(ErroProvedor):
    """Falha da API do Gemini, com o corpo bruto ja redigido em `raw`."""


class ProvedorGemini(ProvedorBase):
    """Cliente de imagem do Gemini.

    A chave vive apenas em dois closures (`montar_headers` e `_redigir`): nao
    vira atributo, nao entra em `repr`, nao aparece em traceback.
    """

    PROPORCOES_VALIDAS = PROPORCOES_VALIDAS
    CAMPOS_PROIBIDOS = CAMPOS_PROIBIDOS
    nome = "gemini"

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        modelo: str = MODELO_PADRAO,
        tamanho: str = TAMANHO_PADRAO,
        transport: httpx.BaseTransport | None = None,
        timeout: float = 600.0,
    ) -> None:
        chave = (api_key if api_key is not None else os.environ.get("GEMINI_API_KEY", "")).strip()
        if not chave:
            raise ErroGemini(
                "GEMINI_API_KEY ausente. Defina no ambiente ou em .env (veja .env.example). "
                "A chave nunca e impressa pelo CIE."
            )
        if tamanho not in TAMANHOS_VALIDOS:
            raise ErroGemini(
                f"imageSize={tamanho!r} invalido; a API aceita "
                f"{', '.join(sorted(TAMANHOS_VALIDOS))}"
            )

        self.base_url = (base_url or os.environ.get("CIE_GEMINI_BASE_URL") or BASE_URL_PADRAO).rstrip("/")
        self.modelo = modelo
        self.tamanho = tamanho
        self.timeout = timeout
        self._transport = transport
        self._redigir = fazer_redator(chave)
        # A chave so existe aqui dentro.
        self.montar_headers = lambda: {
            HEADER_AUTH: chave,
            "Content-Type": "application/json",
        }

    def __repr__(self) -> str:  # pragma: no cover - conveniencia de depuracao
        return f"ProvedorGemini(base_url={self.base_url!r}, modelo={self.modelo!r})"

    # ----------------------------------------------------------------- #
    # montagem (sem rede - e o que os testes inspecionam)
    # ----------------------------------------------------------------- #

    def endpoint_de(self, req: Requisicao) -> str:
        """Um endpoint so: geracao e edicao sao a mesma chamada, muda o `parts`."""
        return f"/models/{req.modelo or self.modelo}:generateContent"

    def montar_payload(self, req: Requisicao) -> dict[str, Any]:
        """Monta o corpo do POST. Uma requisicao = uma imagem (ver `executar`)."""
        aspecto = self.validar_proporcao(req.aspecto if req.aspecto is not None else ASPECTO_PADRAO)
        fontes = self.validar_fontes(req.fontes)

        partes: list[dict[str, Any]] = [{"text": req.prompt}]
        partes.extend(self.referencia(f) for f in fontes)

        payload: dict[str, Any] = {
            "contents": [{"role": "user", "parts": partes}],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "imageConfig": {"aspectRatio": aspecto, "imageSize": self.tamanho},
            },
        }
        payload.update(req.extra)
        return self.checar_campos_proibidos(payload)

    @staticmethod
    def referencia(caminho: Path, lado: int = LADO_FONTE) -> dict[str, Any]:
        """Uma fonte como `inlineData` - o formato de imagem do generateContent."""
        return {
            "inlineData": {
                "mimeType": "image/jpeg",
                "data": base64_jpeg(caminho, lado),
            }
        }

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

    def executar(self, req: Requisicao) -> list[bytes]:
        """`n` imagens = `n` requisicoes.

        `generateContent` nao tem parametro de quantidade para imagem; variante se
        pede repetindo a chamada, como em `gemini_cadeira_dna.py`. O payload e
        montado uma vez so - se ele estiver torto, ninguem gasta credito.
        """
        payload = self.montar_payload(req)
        caminho = self.endpoint_de(req)
        saida: list[bytes] = []
        with self._cliente() as cliente:
            for _ in range(req.n):
                resposta = self._post(cliente, caminho, payload)
                saida.extend(self._imagens(resposta, caminho))
        return saida

    def _cliente(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.base_url,
            headers=self.montar_headers(),
            timeout=self.timeout,
            transport=self._transport,
        )

    def _post(self, cliente: httpx.Client, caminho: str, payload: dict[str, Any]) -> httpx.Response:
        try:
            resposta = cliente.post(caminho, json=payload)
        except httpx.HTTPError as exc:
            raise ErroGemini(f"falha de rede em {caminho}: {self._redigir(str(exc))}") from exc
        if resposta.status_code != 200:
            bruto = self._redigir(_texto(resposta))
            raise ErroGemini(
                f"Gemini {caminho} devolveu {resposta.status_code}: {_mensagem(bruto)}",
                status_code=resposta.status_code,
                raw=bruto[:LIMITE_ERRO_CHARS],
            )
        return resposta

    def _imagens(self, resposta: httpx.Response, caminho: str) -> list[bytes]:
        try:
            corpo = resposta.json()
        except ValueError as exc:
            raise ErroGemini(
                f"Gemini {caminho} devolveu 200 com corpo nao-JSON",
                status_code=200,
                raw=self._redigir(_texto(resposta))[:LIMITE_ERRO_CHARS],
            ) from exc

        saida: list[bytes] = []
        for candidato in corpo.get("candidates", []):
            for parte in candidato.get("content", {}).get("parts", []):
                inline = parte.get("inlineData") or parte.get("inline_data")
                if not inline:
                    continue
                try:
                    saida.append(base64.b64decode(inline["data"]))
                except (KeyError, ValueError, TypeError) as exc:
                    raise ErroGemini("inlineData sem base64 valido", status_code=200) from exc

        if not saida:
            # 200 sem imagem quase sempre e filtro de seguranca ou o modelo
            # respondendo em texto. O finishReason e a unica pista util.
            motivos = [c.get("finishReason") for c in corpo.get("candidates", [])]
            raise ErroGemini(
                f"Gemini {caminho} devolveu 200 sem imagem; finishReason={motivos}",
                status_code=200,
                raw=self._redigir(json.dumps(corpo, ensure_ascii=False))[:LIMITE_ERRO_CHARS],
            )
        return saida


# --------------------------------------------------------------------------- #
# utilitarios de imagem (sem rede)
# --------------------------------------------------------------------------- #


def base64_jpeg(caminho: Path, lado: int = LADO_FONTE) -> str:
    """Le a foto, corrige orientacao EXIF, limita o lado maior e devolve base64 puro.

    Sem prefixo `data:` - o `inlineData` do Gemini quer o base64 nu, com o mime
    em campo separado.
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
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def _texto(resposta: httpx.Response) -> str:
    try:
        return resposta.text
    except Exception:  # pragma: no cover - corpo binario ou encoding torto
        return "<corpo ilegivel>"


def _mensagem(bruto: str) -> str:
    """Extrai `error.status` + `error.message` quando o corpo e JSON."""
    try:
        corpo = json.loads(bruto)
    except (ValueError, TypeError):
        return bruto[:300]
    erro = corpo.get("error", {}) if isinstance(corpo, dict) else {}
    if isinstance(erro, dict) and erro:
        return f"{erro.get('status', '')} {erro.get('message', '')}".strip()[:300]
    return bruto[:300]


__all__ = [
    "ASPECTO_PADRAO",
    "BASE_URL_PADRAO",
    "CAMPOS_PROIBIDOS",
    "HEADER_AUTH",
    "MODELOS_IMAGEM",
    "MODELO_PADRAO",
    "PROPORCOES_VALIDAS",
    "TAMANHOS_VALIDOS",
    "TAMANHO_PADRAO",
    "ErroGemini",
    "ProvedorGemini",
    "base64_jpeg",
]
