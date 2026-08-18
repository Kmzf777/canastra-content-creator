"""Orquestracao da colheita. O browser e substituido por um duble."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

import cie.scrape.harvest as harvest_mod
from cie.errors import ScrapeError
from cie.scrape.harvest import build_envelope, harvest, write_envelope
from cie.scrape.targets import HashtagTarget, PostTarget, ProfileTarget


class BrowserFalso:
    """Duble do modulo browser: registra o que foi pedido, devolve JSON fixo."""

    def __init__(self, resultado=None, logado=True):
        self.resultado = resultado or {"source": "feed_user", "pages": [{"items": []}]}
        self.logado = logado
        self.chamadas: list[tuple[str, dict]] = []

    def open_page(self, perfil, headless=True):
        from contextlib import contextmanager

        @contextmanager
        def _ctx():
            yield object()

        return _ctx()

    def goto_instagram(self, pagina):
        pass

    def is_logged_in(self, pagina):
        return self.logado

    def app_id(self, pagina):
        return "999"

    def run_snippet(self, pagina, nome, params):
        self.chamadas.append((nome, params))
        return self.resultado


def test_envelope_carrega_alvo_e_carimbo():
    envelope = build_envelope(
        ProfileTarget(handle="cafecanastra"),
        {"source": "feed_user", "pages": [{"items": []}]},
    )
    assert envelope["target"] == {
        "kind": "profile",
        "slug": "cafecanastra",
        "handle": "cafecanastra",
    }
    assert envelope["source"] == "feed_user"
    assert envelope["harvested_at"]


@pytest.mark.parametrize("resultado_invalido", [None, [], "texto", 42])
def test_envelope_rejeita_resultado_que_nao_e_objeto(resultado_invalido):
    """`build_envelope` e publica; nao pode assumir que quem a chama passou um dict."""
    with pytest.raises(ScrapeError):
        build_envelope(ProfileTarget(handle="cafecanastra"), resultado_invalido)


def test_envelope_de_post_guarda_o_shortcode():
    envelope = build_envelope(PostTarget(shortcode="AAA111"), {"pages": []})
    assert envelope["target"]["shortcode"] == "AAA111"
    assert envelope["target"]["kind"] == "post"


def test_envelope_de_hashtag_guarda_a_tag():
    envelope = build_envelope(HashtagTarget(tag="cafeespecial"), {"pages": []})
    assert envelope["target"]["tag"] == "cafeespecial"
    assert envelope["target"]["slug"] == "tag-cafeespecial"


def test_envelope_vai_para_colheita_com_nome_ordenavel(tmp_path: Path):
    envelope = build_envelope(ProfileTarget(handle="cafecanastra"), {"pages": []})
    caminho = write_envelope(envelope, tmp_path)

    assert caminho.parent == tmp_path / "_colheita"
    assert caminho.name.startswith("cafecanastra-")
    assert caminho.suffix == ".json"
    assert json.loads(caminho.read_text(encoding="utf-8"))["target"]["slug"] == "cafecanastra"


def test_write_envelope_nunca_sobrescreve_em_colisao_de_carimbo(tmp_path: Path, monkeypatch):
    """Dois envelopes do mesmo alvo no mesmo carimbo ganham sufixo -2, -3, ..."""

    class TempoFixo(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2026, 8, 18, 10, 0, 0, 0, tzinfo=tz)

    monkeypatch.setattr(harvest_mod, "datetime", TempoFixo)

    envelope = build_envelope(ProfileTarget(handle="cafecanastra"), {"pages": []})
    caminho1 = write_envelope(envelope, tmp_path)
    caminho2 = write_envelope(envelope, tmp_path)
    caminho3 = write_envelope(envelope, tmp_path)

    assert len({caminho1, caminho2, caminho3}) == 3
    assert caminho1.exists() and caminho2.exists() and caminho3.exists()
    assert json.loads(caminho1.read_text(encoding="utf-8"))["target"]["slug"] == "cafecanastra"
    assert json.loads(caminho2.read_text(encoding="utf-8"))["target"]["slug"] == "cafecanastra"


@pytest.mark.parametrize(
    "slug_hostil",
    [
        "../../../pwned",
        "..\\..\\pwned",
        "C:\\Windows\\System32\\pwned",
        "....//....//pwned",
    ],
)
def test_write_envelope_neutraliza_slug_hostil(tmp_path: Path, slug_hostil: str):
    """Um envelope montado a mao pode trazer qualquer slug; nunca escapa de _colheita/."""
    envelope = {"target": {"kind": "profile", "slug": slug_hostil}, "pages": []}
    caminho = write_envelope(envelope, tmp_path)

    assert caminho.resolve().parent == (tmp_path / "_colheita").resolve()
    # Nada foi criado fora de _colheita/: so a propria pasta _colheita existe em tmp_path.
    assert list(tmp_path.iterdir()) == [tmp_path / "_colheita"]


def test_perfil_chama_o_snippet_de_perfil_com_limite(tmp_path: Path):
    falso = BrowserFalso()
    harvest(
        ProfileTarget(handle="cafecanastra"),
        profile_dir=tmp_path / "perfil",
        limit=30,
        browser_mod=falso,
    )
    nome, params = falso.chamadas[0]
    assert nome == "profile"
    assert params["handle"] == "cafecanastra"
    assert params["limit"] == 30
    assert params["appId"] == "999"


def test_post_converte_shortcode_em_media_id(tmp_path: Path):
    falso = BrowserFalso({"source": "media_info", "pages": []})
    harvest(PostTarget(shortcode="CBa"), profile_dir=tmp_path / "p", browser_mod=falso)
    nome, params = falso.chamadas[0]
    assert nome == "post"
    assert params["mediaId"] == "8282"


def test_hashtag_chama_o_snippet_de_hashtag(tmp_path: Path):
    falso = BrowserFalso({"source": "tag_web_info", "pages": []})
    harvest(HashtagTarget(tag="cafeespecial"), profile_dir=tmp_path / "p", browser_mod=falso)
    nome, params = falso.chamadas[0]
    assert nome == "hashtag"
    assert params["tag"] == "cafeespecial"


def test_sessao_deslogada_para_antes_de_colher(tmp_path: Path):
    falso = BrowserFalso(logado=False)
    with pytest.raises(ScrapeError) as exc:
        harvest(ProfileTarget(handle="x"), profile_dir=tmp_path / "p", browser_mod=falso)
    assert "cie scrape login" in str(exc.value)
    assert falso.chamadas == []
