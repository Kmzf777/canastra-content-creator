import pytest

from instagram.estaticos.cli import main


def test_conferir_aprova_o_catalogo_do_repositorio(capsys):
    assert main(["conferir"]) == 0
    assert "ok" in capsys.readouterr().out.lower()


def test_prompt_imprime_o_prompt_da_peca(capsys):
    assert main(["prompt", "cartao-classico-250g-graos"]) == 0
    saida = capsys.readouterr().out
    assert "SCA 80+" in saida
    assert "31,70" not in saida


def test_prompt_aceita_correcao(capsys):
    assert main(["prompt", "cartao-classico-250g-graos", "--correcao", "soletrar"]) == 0
    assert "-" in capsys.readouterr().out


def test_slug_desconhecido_devolve_2(capsys):
    assert main(["prompt", "nao-existe"]) == 2
    assert "nao-existe" in capsys.readouterr().err


def test_correcao_invalida_sai_com_erro(capsys):
    """argparse com `choices` ja rejeita: ele levanta SystemExit(2)."""
    with pytest.raises(SystemExit) as e:
        main(["prompt", "cartao-classico-250g-graos", "--correcao", "xpto"])
    assert e.value.code == 2


def test_listar_mostra_os_slugs(capsys):
    assert main(["listar"]) == 0
    assert "cartao-classico-250g-graos" in capsys.readouterr().out
