"""Provedores de imagem sob teste. **Nenhum teste toca a rede real.**

Tudo passa por `httpx.MockTransport`, como no resto da suite: uma geracao de
verdade custa credito e leva minutos, e o que precisa ser travado aqui nao e o
pixel que volta - e o payload que sai.

Os cinco travamentos que justificam este arquivo existir, cada um mapeado para o
erro que ele impede de repetir:

1. `image_url` em `/images/edits` devolve **HTTP 200 e ignora a imagem**. Custou
   duas rodadas de geracao que pareciam funcionar. O campo nunca pode ser emitido.
2. `image` em lista exige strings (objetos dao 422); multi-fonte vai em `images`,
   no plural. Mandar os dois juntos da 400.
3. `aspect_ratio: "4:5"` nao existe na xAI e envenena a requisicao inteira -
   tem que morrer em memoria, antes do POST.
4. Gemini com `Authorization: Bearer` devolve 401; o cabecalho e `x-goog-api-key`.
5. A chave nunca aparece em mensagem de erro, nem quando o proprio servidor a
   devolve no corpo.
"""

from __future__ import annotations

import base64
import io
import json
from pathlib import Path
from typing import Any, Callable

import httpx
import pytest
from PIL import Image

from cie.providers import (
    CampoProibido,
    ErroGemini,
    ErroProvedor,
    ErroXai,
    FonteInvalida,
    ProporcaoInvalida,
    Provider,
    ProvedorGemini,
    ProvedorXai,
    Requisicao,
    criar_provedor,
)
from cie.providers import gemini as mod_gemini
from cie.providers import xai as mod_xai
from cie.providers.base import MARCA_REDACAO, _chaves_proibidas, fazer_redator

XAI_KEY = "xai-chave-de-teste-0123456789ABCDEF"
GEMINI_KEY = "AQ.chave-de-teste-0123456789ABCDEF"
BASE_XAI = "https://api.test-xai/v1"
BASE_GEMINI = "https://api.test-gemini/v1beta"

PROMPT = "the coffee package on bare red earth, harsh overhead midday sun"


# --------------------------------------------------------------------------- #
# apoio
# --------------------------------------------------------------------------- #


class Gravador:
    """Roteiro de respostas: entrega uma por chamada, repetindo a ultima."""

    def __init__(self, roteiro: list[Any]) -> None:
        self.roteiro = roteiro
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        item = self.roteiro[min(len(self.requests) - 1, len(self.roteiro) - 1)]
        if isinstance(item, Exception):
            raise item
        if callable(item) and not isinstance(item, httpx.Response):
            return item(request)
        return item

    @property
    def chamadas(self) -> int:
        return len(self.requests)

    def corpo(self, indice: int = 0) -> dict[str, Any]:
        return json.loads(self.requests[indice].content.decode())


def sem_rede(request: httpx.Request) -> httpx.Response:  # pragma: no cover - nao deve rodar
    raise AssertionError(f"o codigo tocou a rede: {request.method} {request.url}")


def jpeg(largura: int = 64, altura: int = 80, cor: tuple[int, int, int] = (150, 70, 40)) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (largura, altura), cor).save(buffer, "JPEG", quality=90)
    return buffer.getvalue()


def foto(tmp_path: Path, nome: str, largura: int = 64, altura: int = 80) -> Path:
    destino = tmp_path / nome
    destino.write_bytes(jpeg(largura, altura))
    return destino


def resposta_xai(imagens: int = 1) -> httpx.Response:
    b64 = base64.b64encode(jpeg()).decode()
    return httpx.Response(200, json={"data": [{"b64_json": b64} for _ in range(imagens)]})


def resposta_gemini(imagens: int = 1) -> httpx.Response:
    b64 = base64.b64encode(jpeg()).decode()
    partes = [{"inlineData": {"mimeType": "image/jpeg", "data": b64}} for _ in range(imagens)]
    return httpx.Response(200, json={"candidates": [{"content": {"parts": partes}}]})


def prov_xai(roteiro: list[Any] | None = None, **opcoes: Any) -> tuple[ProvedorXai, Gravador]:
    gravador = Gravador(roteiro if roteiro is not None else [resposta_xai()])
    provedor = ProvedorXai(
        api_key=XAI_KEY,
        base_url=BASE_XAI,
        transport=httpx.MockTransport(gravador),
        **opcoes,
    )
    return provedor, gravador


def prov_gemini(roteiro: list[Any] | None = None, **opcoes: Any) -> tuple[ProvedorGemini, Gravador]:
    gravador = Gravador(roteiro if roteiro is not None else [resposta_gemini()])
    provedor = ProvedorGemini(
        api_key=GEMINI_KEY,
        base_url=BASE_GEMINI,
        transport=httpx.MockTransport(gravador),
        **opcoes,
    )
    return provedor, gravador


# --------------------------------------------------------------------------- #
# REGRA 1 - `image_url` devolve 200 e ignora a imagem: nunca pode ser emitido
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("quantas_fontes", [0, 1, 2, 3])
def test_payload_xai_nunca_emite_campo_ignorado_em_silencio(tmp_path: Path, quantas_fontes: int):
    """`image_url`, `image_urls`, `reference_images`, `input_images`: nenhum sai.

    Todos devolvem HTTP 200 sem aplicar o guidance. O status nao denuncia; so a
    imagem gerada denuncia, e ai o credito ja foi gasto.
    """
    provedor, _ = prov_xai()
    fontes = tuple(foto(tmp_path, f"f{i}.jpg") for i in range(quantas_fontes))
    payload = provedor.montar_payload(Requisicao(prompt=PROMPT, fontes=fontes))

    assert "image_url" not in payload
    assert _chaves_proibidas(payload, mod_xai.CAMPOS_PROIBIDOS) == set()


def test_requisicao_enviada_de_verdade_nao_carrega_image_url(tmp_path: Path):
    """Nao basta o payload montado estar limpo: o que sai no fio tem que estar."""
    provedor, gravador = prov_xai()
    provedor.gerar(PROMPT, fontes=[foto(tmp_path, "a.jpg")])

    corpo = gravador.corpo()
    bruto = gravador.requests[0].content.decode()
    assert "image_url" not in corpo
    assert '"image_url":' not in bruto  # nem aninhado em lugar nenhum
    assert corpo["image"]["type"] == "image_url"  # `type` e o valor, nao a chave


def test_campo_ignorado_injetado_por_extra_e_barrado(tmp_path: Path):
    """`extra` e porta para campo nao confirmado - nao para campo ja reprovado."""
    provedor, gravador = prov_xai([sem_rede])
    req = Requisicao(
        prompt=PROMPT,
        fontes=(foto(tmp_path, "a.jpg"),),
        extra={"image_url": ["data:image/jpeg;base64,AAAA"]},
    )
    with pytest.raises(CampoProibido) as exc:
        provedor.executar(req)

    assert "image_url" in str(exc.value)
    assert gravador.chamadas == 0


def test_endpoint_muda_com_a_presenca_de_fonte(tmp_path: Path):
    provedor, gravador = prov_xai([resposta_xai(), resposta_xai()])
    provedor.gerar(PROMPT)
    provedor.gerar(PROMPT, fontes=[foto(tmp_path, "a.jpg")])

    assert gravador.requests[0].url.path.endswith(mod_xai.ENDPOINT_GENERATIONS)
    assert gravador.requests[1].url.path.endswith(mod_xai.ENDPOINT_EDITS)


# --------------------------------------------------------------------------- #
# REGRA 2 - `image` objeto para uma fonte, `images` plural para varias
# --------------------------------------------------------------------------- #


def test_fonte_unica_vai_em_image_como_objeto(tmp_path: Path):
    """`image` em lista exigiria strings; lista de objetos da 422. Entao: objeto."""
    provedor, _ = prov_xai()
    payload = provedor.montar_payload(
        Requisicao(prompt=PROMPT, fontes=(foto(tmp_path, "a.jpg"),))
    )

    assert isinstance(payload["image"], dict)
    assert not isinstance(payload["image"], list)
    assert set(payload["image"]) == {"url", "type"}
    assert payload["image"]["type"] == "image_url"
    assert payload["image"]["url"].startswith("data:image/jpeg;base64,")
    assert "images" not in payload  # os dois juntos = 400


def test_multiplas_fontes_vao_em_images_no_plural(tmp_path: Path):
    provedor, _ = prov_xai()
    fontes = (foto(tmp_path, "a.jpg"), foto(tmp_path, "b.jpg"), foto(tmp_path, "c.jpg"))
    payload = provedor.montar_payload(Requisicao(prompt=PROMPT, fontes=fontes))

    assert "image" not in payload  # `image` + `images` juntos = 400
    assert isinstance(payload["images"], list)
    assert len(payload["images"]) == 3
    for ref in payload["images"]:
        assert isinstance(ref, dict)
        assert ref["type"] == "image_url"
        assert ref["url"].startswith("data:image/jpeg;base64,")


def test_defaults_do_modelo_saem_no_payload(tmp_path: Path):
    provedor, _ = prov_xai()
    payload = provedor.montar_payload(Requisicao(prompt=PROMPT, n=2))

    assert payload["model"] == "grok-imagine-image-2.0"
    assert payload["quality"] == "medium"
    assert payload["resolution"] == "2k"
    assert payload["n"] == 2


def test_quality_high_nao_e_aceito_na_construcao():
    """`high` devolve 400 no 2.0 - barrar antes de existir requisicao."""
    with pytest.raises(ErroXai, match="high"):
        ProvedorXai(api_key=XAI_KEY, qualidade="high")


def test_mais_fontes_que_o_testado_e_recusado(tmp_path: Path):
    provedor, gravador = prov_xai([sem_rede])
    fontes = tuple(foto(tmp_path, f"f{i}.jpg") for i in range(5))
    with pytest.raises(FonteInvalida, match="no maximo 4"):
        provedor.executar(Requisicao(prompt=PROMPT, fontes=fontes))
    assert gravador.chamadas == 0


def test_fonte_inexistente_morre_antes_da_rede(tmp_path: Path):
    provedor, gravador = prov_xai([sem_rede])
    with pytest.raises(FonteInvalida, match="inexistente"):
        provedor.gerar(PROMPT, fontes=[tmp_path / "nao-existe.jpg"])
    assert gravador.chamadas == 0


# --------------------------------------------------------------------------- #
# REGRA 3 - `4:5` nao existe na xAI e tem que morrer antes do POST
# --------------------------------------------------------------------------- #


def test_aspecto_4x5_levanta_antes_de_qualquer_rede(tmp_path: Path):
    """Registro de licoes #4: `4:5` envenenou uma varredura inteira de sondagem."""
    provedor, gravador = prov_xai([sem_rede])

    with pytest.raises(ProporcaoInvalida) as exc:
        provedor.gerar(PROMPT, fontes=[foto(tmp_path, "a.jpg")], aspecto="4:5")

    assert gravador.chamadas == 0, "a excecao veio depois do POST - credito gasto"
    assert "4:5" in str(exc.value)
    assert "3:4" in str(exc.value), "a mensagem tem que apontar a saida"


def test_montar_payload_recusa_4x5_sem_construir_nada():
    provedor, _ = prov_xai()
    with pytest.raises(ProporcaoInvalida):
        provedor.montar_payload(Requisicao(prompt=PROMPT, aspecto="4:5"))


def test_4x5_nao_esta_na_lista_de_proporcoes_da_xai():
    assert "4:5" not in mod_xai.PROPORCOES_VALIDAS
    assert {"1:1", "3:4", "4:3", "9:16", "16:9", "2:3", "3:2", "auto"} <= mod_xai.PROPORCOES_VALIDAS


@pytest.mark.parametrize("aspecto", sorted(mod_xai.PROPORCOES_VALIDAS))
def test_proporcoes_validas_passam(aspecto: str):
    provedor, _ = prov_xai()
    payload = provedor.montar_payload(Requisicao(prompt=PROMPT, aspecto=aspecto))
    assert payload["aspect_ratio"] == aspecto


def test_aspecto_none_nao_manda_o_campo():
    """Sem aspecto pedido, nao chuta valor: deixa o default do provedor valer."""
    provedor, _ = prov_xai()
    assert "aspect_ratio" not in provedor.montar_payload(Requisicao(prompt=PROMPT))


def test_gerar_4x5_pede_3x4_e_recorta_a_altura(tmp_path: Path):
    """O caminho do feed: 3:4 na API, 4:5 no disco."""
    bruta = jpeg(1200, 1600)  # 3:4
    provedor, gravador = prov_xai(
        [httpx.Response(200, json={"data": [{"b64_json": base64.b64encode(bruta).decode()}]})]
    )

    saida = provedor.gerar_4x5(PROMPT, fontes=[foto(tmp_path, "a.jpg")])

    assert gravador.corpo()["aspect_ratio"] == "3:4"
    with Image.open(io.BytesIO(saida[0])) as imagem:
        assert imagem.size == (1200, 1500)  # exatamente 4:5


def test_recorte_4x5_tira_62_por_cento_da_sobra_do_topo():
    """A sobra sai assimetrica de proposito: mais ceu que chao."""
    recortada = mod_xai.recortar_4x5(jpeg(1200, 1600))
    with Image.open(io.BytesIO(recortada)) as imagem:
        assert imagem.size == (1200, 1500)
    # sobra = 1600 - 1500 = 100 px; 62 saem do topo, 38 da base.
    assert int((1600 - 1500) * mod_xai.FRACAO_TOPO_4X5) == 62


def test_recorte_4x5_deixa_intacta_imagem_que_ja_cabe():
    with Image.open(io.BytesIO(mod_xai.recortar_4x5(jpeg(1000, 1000)))) as imagem:
        assert imagem.size == (1000, 1000)


# --------------------------------------------------------------------------- #
# REGRA 4 - Gemini autentica por `x-goog-api-key`, nunca por Bearer
# --------------------------------------------------------------------------- #


def test_gemini_monta_header_x_goog_api_key():
    """`Authorization: Bearer` com esta credencial devolve 401."""
    provedor, _ = prov_gemini()
    cabecalhos = provedor.montar_headers()

    assert cabecalhos["x-goog-api-key"] == GEMINI_KEY
    assert "Authorization" not in cabecalhos
    assert not any(c.lower() == "authorization" for c in cabecalhos)
    assert mod_gemini.HEADER_AUTH == "x-goog-api-key"


def test_requisicao_gemini_sai_no_fio_sem_authorization(tmp_path: Path):
    provedor, gravador = prov_gemini()
    provedor.gerar(PROMPT, fontes=[foto(tmp_path, "a.jpg")])

    cabecalhos = gravador.requests[0].headers
    assert cabecalhos["x-goog-api-key"] == GEMINI_KEY
    assert "authorization" not in cabecalhos
    assert f"Bearer {GEMINI_KEY}" not in str(dict(cabecalhos))


# --------------------------------------------------------------------------- #
# REGRA 5 - a chave nunca aparece em mensagem de erro
# --------------------------------------------------------------------------- #


def test_erro_da_xai_nao_ecoa_a_chave_devolvida_pelo_servidor():
    corpo = {"error": {"message": f"invalid api key {XAI_KEY} for this endpoint"}}
    provedor, _ = prov_xai([httpx.Response(401, json=corpo)])

    with pytest.raises(ErroXai) as exc:
        provedor.gerar(PROMPT)

    assert XAI_KEY not in str(exc.value)
    assert XAI_KEY not in exc.value.raw
    assert MARCA_REDACAO in exc.value.raw
    assert MARCA_REDACAO in str(exc.value)
    assert exc.value.status_code == 401


def test_erro_do_gemini_nao_ecoa_a_chave_devolvida_pelo_servidor():
    corpo = {"error": {"status": "UNAUTHENTICATED", "message": f"key={GEMINI_KEY} rejeitada"}}
    provedor, _ = prov_gemini([httpx.Response(401, json=corpo)])

    with pytest.raises(ErroGemini) as exc:
        provedor.gerar(PROMPT)

    assert GEMINI_KEY not in str(exc.value)
    assert GEMINI_KEY not in exc.value.raw
    assert MARCA_REDACAO in exc.value.raw
    assert "UNAUTHENTICATED" in str(exc.value)


def test_falha_de_rede_tambem_passa_pela_redacao():
    """A URL da excecao de rede pode carregar a chave em query string."""
    estouro = httpx.ConnectError(f"nao conectou a https://api.x.ai/v1?key={XAI_KEY}")
    provedor, _ = prov_xai([estouro])

    with pytest.raises(ErroXai) as exc:
        provedor.gerar(PROMPT)

    assert XAI_KEY not in str(exc.value)
    assert MARCA_REDACAO in str(exc.value)


@pytest.mark.parametrize("construtor,chave", [(prov_xai, XAI_KEY), (prov_gemini, GEMINI_KEY)])
def test_chave_nao_vive_em_atributo_nem_em_repr(construtor: Callable[..., Any], chave: str):
    """A chave fica em closure: `repr`, `vars` e traceback do pytest nao a alcancam."""
    provedor, _ = construtor()

    assert chave not in repr(provedor)
    assert chave not in str(vars(provedor))


def test_redator_ignora_segredo_curto_demais():
    """Fragmento curto casaria com pedaco legitimo do corpo e apagaria evidencia."""
    redigir = fazer_redator("abc", None, "chave-longa-o-bastante")
    assert redigir("abc segue chave-longa-o-bastante") == f"abc segue {MARCA_REDACAO}"


# --------------------------------------------------------------------------- #
# Gemini: payload
# --------------------------------------------------------------------------- #


def test_payload_gemini_tem_response_modalities_e_image_config(tmp_path: Path):
    provedor, _ = prov_gemini()
    payload = provedor.montar_payload(
        Requisicao(prompt=PROMPT, fontes=(foto(tmp_path, "a.jpg"),), aspecto="4:5")
    )

    config = payload["generationConfig"]
    assert config["responseModalities"] == ["IMAGE"]
    assert config["imageConfig"] == {"aspectRatio": "4:5", "imageSize": "2K"}


def test_gemini_aceita_4x5_que_a_xai_nao_tem():
    """A diferenca operacional entre os dois provedores, em um assert."""
    assert "4:5" in mod_gemini.PROPORCOES_VALIDAS
    assert "4:5" not in mod_xai.PROPORCOES_VALIDAS

    provedor, _ = prov_gemini()
    payload = provedor.montar_payload(Requisicao(prompt=PROMPT, aspecto="4:5"))
    assert payload["generationConfig"]["imageConfig"]["aspectRatio"] == "4:5"


def test_gemini_usa_4x5_por_padrao():
    provedor, _ = prov_gemini()
    payload = provedor.montar_payload(Requisicao(prompt=PROMPT))
    assert payload["generationConfig"]["imageConfig"]["aspectRatio"] == "4:5"


def test_gemini_recusa_proporcao_inexistente_antes_da_rede():
    provedor, gravador = prov_gemini([sem_rede])
    with pytest.raises(ProporcaoInvalida):
        provedor.gerar(PROMPT, aspecto="7:3")
    assert gravador.chamadas == 0


def test_gemini_nunca_emite_resolution_nem_output_image_size(tmp_path: Path):
    """`resolution` e `outputImageSize` nao existem na API - devolvem 400."""
    provedor, _ = prov_gemini()
    payload = provedor.montar_payload(Requisicao(prompt=PROMPT, fontes=(foto(tmp_path, "a.jpg"),)))
    assert _chaves_proibidas(payload, mod_gemini.CAMPOS_PROIBIDOS) == set()

    with pytest.raises(CampoProibido, match="resolution"):
        provedor.montar_payload(Requisicao(prompt=PROMPT, extra={"resolution": "2K"}))


def test_gemini_manda_fonte_como_inline_data(tmp_path: Path):
    provedor, _ = prov_gemini()
    payload = provedor.montar_payload(
        Requisicao(prompt=PROMPT, fontes=(foto(tmp_path, "a.jpg"), foto(tmp_path, "b.jpg")))
    )

    partes = payload["contents"][0]["parts"]
    assert partes[0] == {"text": PROMPT}
    assert len(partes) == 3
    for parte in partes[1:]:
        inline = parte["inlineData"]
        assert inline["mimeType"] == "image/jpeg"
        # base64 nu, sem prefixo `data:` - o mime vai em campo separado.
        assert not inline["data"].startswith("data:")
        assert base64.b64decode(inline["data"])[:2] == b"\xff\xd8"  # JPEG


def test_gemini_endpoint_e_generate_content_do_modelo_padrao():
    provedor, gravador = prov_gemini()
    provedor.gerar(PROMPT)
    assert gravador.requests[0].url.path.endswith(
        "/models/gemini-3-pro-image:generateContent"
    )


def test_gemini_pede_n_variantes_com_n_requisicoes():
    """`generateContent` nao tem parametro de quantidade: variante e repeticao."""
    provedor, gravador = prov_gemini([resposta_gemini()])
    saida = provedor.gerar(PROMPT, n=3)

    assert gravador.chamadas == 3
    assert len(saida) == 3


def test_modelo_pro_inexistente_nao_entra_na_lista():
    """Nao existe `gemini-3.1-pro-image`; o Pro mais atual e `gemini-3-pro-image`."""
    assert "gemini-3.1-pro-image" not in mod_gemini.MODELOS_IMAGEM
    assert mod_gemini.MODELO_PADRAO == "gemini-3-pro-image"


# --------------------------------------------------------------------------- #
# resposta: HTTP 200 nao prova que veio imagem
# --------------------------------------------------------------------------- #


def test_xai_devolve_bytes_de_imagem_por_b64_json():
    provedor, _ = prov_xai([resposta_xai(imagens=2)])
    saida = provedor.gerar(PROMPT, n=2)

    assert len(saida) == 2
    for bruto in saida:
        with Image.open(io.BytesIO(bruto)) as imagem:
            assert imagem.size == (64, 80)


def test_xai_baixa_a_imagem_quando_a_resposta_traz_so_url():
    def roteiro(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/images/generations"):
            return httpx.Response(200, json={"data": [{"url": "https://cdn.test/i.jpg"}]})
        return httpx.Response(200, content=jpeg())

    provedor, gravador = prov_xai([roteiro])
    saida = provedor.gerar(PROMPT)

    assert gravador.chamadas == 2
    assert saida[0][:2] == b"\xff\xd8"


def test_xai_200_sem_imagem_vira_erro_e_nao_lista_vazia():
    """HTTP 200 nao prova que o pedido funcionou - falha nao pode ser engolida."""
    provedor, _ = prov_xai([httpx.Response(200, json={"data": []})])
    with pytest.raises(ErroXai, match="sem imagem"):
        provedor.gerar(PROMPT)


def test_gemini_200_sem_imagem_reporta_o_finish_reason():
    corpo = {"candidates": [{"finishReason": "IMAGE_SAFETY", "content": {"parts": []}}]}
    provedor, _ = prov_gemini([httpx.Response(200, json=corpo)])

    with pytest.raises(ErroGemini) as exc:
        provedor.gerar(PROMPT)
    assert "IMAGE_SAFETY" in str(exc.value)


def test_gemini_aceita_inline_data_em_snake_case():
    b64 = base64.b64encode(jpeg()).decode()
    corpo = {"candidates": [{"content": {"parts": [{"inline_data": {"data": b64}}]}}]}
    provedor, _ = prov_gemini([httpx.Response(200, json=corpo)])
    assert len(provedor.gerar(PROMPT)) == 1


# --------------------------------------------------------------------------- #
# contrato comum
# --------------------------------------------------------------------------- #


def test_os_dois_provedores_satisfazem_o_protocolo():
    provedor_xai, _ = prov_xai()
    provedor_gemini, _ = prov_gemini()
    assert isinstance(provedor_xai, Provider)
    assert isinstance(provedor_gemini, Provider)


def test_criar_provedor_pelo_nome():
    assert isinstance(criar_provedor("xai", api_key=XAI_KEY), ProvedorXai)
    assert isinstance(criar_provedor("gemini", api_key=GEMINI_KEY), ProvedorGemini)
    with pytest.raises(ErroProvedor, match="desconhecido"):
        criar_provedor("midjourney")


def test_requisicao_normaliza_fontes_para_path(tmp_path: Path):
    req = Requisicao(prompt=PROMPT, fontes=[str(foto(tmp_path, "a.jpg"))])
    assert all(isinstance(f, Path) for f in req.fontes)
    assert isinstance(req.fontes, tuple)


def test_requisicao_recusa_prompt_vazio_e_n_zero():
    with pytest.raises(ErroProvedor, match="prompt vazio"):
        Requisicao(prompt="   ")
    with pytest.raises(ErroProvedor, match="n=0"):
        Requisicao(prompt=PROMPT, n=0)


def test_requisicao_com_troca_campos_sem_mutar_o_original():
    req = Requisicao(prompt=PROMPT)
    outra = req.com(n=3, aspecto="3:4")
    assert (outra.n, outra.aspecto) == (3, "3:4")
    assert (req.n, req.aspecto) == (1, None)


def test_multifonte_sinaliza_heranca_de_proporcao(tmp_path: Path):
    """Saida multi-fonte herda a proporcao da PRIMEIRA fonte - medido, nao inferido."""
    req = Requisicao(prompt=PROMPT, fontes=(foto(tmp_path, "a.jpg"), foto(tmp_path, "b.jpg")))
    assert req.multifonte is True
    assert Requisicao(prompt=PROMPT, fontes=(foto(tmp_path, "a.jpg"),)).multifonte is False


@pytest.mark.parametrize(
    "classe,variavel",
    [(ProvedorXai, "XAI_API_KEY"), (ProvedorGemini, "GEMINI_API_KEY")],
)
def test_sem_chave_no_ambiente_o_provedor_recusa_nascer(
    classe: type, variavel: str, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.delenv(variavel, raising=False)
    with pytest.raises(ErroProvedor, match=variavel):
        classe()
