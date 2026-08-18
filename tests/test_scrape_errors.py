"""Os erros do scrape precisam ser capturaveis como CieError."""

from __future__ import annotations

import pytest

from cie.errors import CieError, InstagramFormatError, ScrapeError


def test_scrape_error_e_cie_error():
    assert issubclass(ScrapeError, CieError)


def test_instagram_format_error_e_scrape_error():
    assert issubclass(InstagramFormatError, ScrapeError)


def test_instagram_format_error_diz_o_que_faltou():
    erro = InstagramFormatError("media sem 'code'", campo="code")
    assert erro.campo == "code"
    assert "code" in str(erro)


def test_erros_do_scrape_sao_pegos_como_cie_error():
    with pytest.raises(CieError):
        raise ScrapeError("qualquer coisa")
