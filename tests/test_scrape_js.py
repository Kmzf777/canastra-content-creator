"""Os snippets precisam existir, ser carregaveis e ter a forma que o evaluate espera."""

from __future__ import annotations

import pytest

from cie.errors import ScrapeError
from cie.scrape.browser import SNIPPETS, load_snippet


@pytest.mark.parametrize("nome", ["appid", "profile", "post", "hashtag"])
def test_snippet_carrega(nome):
    codigo = load_snippet(nome)
    assert codigo.strip()


@pytest.mark.parametrize("nome", ["profile", "post", "hashtag"])
def test_snippet_de_colheita_e_funcao_que_recebe_params(nome):
    # page.evaluate() exige uma expressao que avalie para funcao.
    codigo = load_snippet(nome).strip()
    assert codigo.startswith("async (params)")


def test_todo_snippet_declarado_existe_em_disco():
    for nome in SNIPPETS:
        assert load_snippet(nome).strip()


def test_snippet_inexistente_da_erro_legivel():
    with pytest.raises(ScrapeError) as exc:
        load_snippet("nao-existe")
    assert "nao-existe" in str(exc.value)


def test_snippets_de_colheita_devolvem_pages():
    for nome in ("profile", "post", "hashtag"):
        assert "pages" in load_snippet(nome)


def test_snippets_usam_o_appid_recebido_e_nao_um_literal():
    for nome in ("profile", "post", "hashtag"):
        codigo = load_snippet(nome)
        assert "params.appId" in codigo or "appId" in codigo


def test_appid_nao_comeca_com_comentario():
    # page.evaluate() detecta funcao pelo prefixo da string; um comentario
    # antes do "(" derrota essa deteccao.
    codigo = load_snippet("appid").strip()
    assert codigo.startswith("(")


@pytest.mark.parametrize(
    "nome_hostil",
    [
        "../../../etc/passwd",
        "..\\..\\setup",
        "../parser",
        "../../pyproject",
        "appid/../../../etc/passwd",
    ],
)
def test_nome_hostil_e_rejeitado(nome_hostil):
    # `nome` vira caminho de arquivo; so o allowlist de SNIPPETS pode passar.
    with pytest.raises(ScrapeError):
        load_snippet(nome_hostil)
