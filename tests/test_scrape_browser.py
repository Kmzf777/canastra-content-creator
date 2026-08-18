"""Do browser so testamos o que nao depende do browser."""

from __future__ import annotations

import builtins
from pathlib import Path

import pytest

from cie.errors import ScrapeError
from cie.scrape import browser


def test_perfil_padrao_fica_dentro_do_cie_home(tmp_path: Path):
    assert browser.profile_dir(tmp_path / ".cie") == tmp_path / ".cie" / "browser-profile"


def test_playwright_ausente_da_instrucao_de_instalacao(monkeypatch: pytest.MonkeyPatch):
    real_import = builtins.__import__

    def sem_playwright(nome, *args, **kwargs):
        if nome.startswith("playwright"):
            raise ModuleNotFoundError("No module named 'playwright'")
        return real_import(nome, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", sem_playwright)

    with pytest.raises(ScrapeError) as exc:
        browser._require_playwright()

    assert "--extra scrape" in str(exc.value)


def test_run_snippet_propaga_erro_devolvido_pelo_js():
    class PageFalsa:
        def evaluate(self, codigo, params=None):
            return {"error": "sessao nao esta logada"}

    with pytest.raises(ScrapeError) as exc:
        browser.run_snippet(PageFalsa(), "profile", {"appId": "1", "handle": "x", "limit": 1})

    assert "sessao nao esta logada" in str(exc.value)


def test_run_snippet_devolve_o_json_quando_da_certo():
    class PageFalsa:
        def evaluate(self, codigo, params=None):
            return {"source": "feed_user", "pages": [{"items": []}]}

    resultado = browser.run_snippet(PageFalsa(), "profile", {"appId": "1"})
    assert resultado["source"] == "feed_user"


def test_run_snippet_recusa_resposta_que_nao_e_objeto():
    class PageFalsa:
        def evaluate(self, codigo, params=None):
            return None

    with pytest.raises(ScrapeError):
        browser.run_snippet(PageFalsa(), "profile", {"appId": "1"})


def test_sessao_logada_detectada_pelo_cookie_sessionid():
    class ContextoFalso:
        def cookies(self, url=None):
            return [{"name": "sessionid", "value": "abc123"}]

    class PageFalsa:
        context = ContextoFalso()

    assert browser.is_logged_in(PageFalsa()) is True


def test_sessao_sem_sessionid_e_considerada_deslogada():
    class ContextoFalso:
        def cookies(self, url=None):
            return [{"name": "csrftoken", "value": "xyz"}, {"name": "sessionid", "value": ""}]

    class PageFalsa:
        context = ContextoFalso()

    assert browser.is_logged_in(PageFalsa()) is False
