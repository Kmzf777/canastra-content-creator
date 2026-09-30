"""Trava de idade do captador de download do ChatGPT.

A licao 17 do CLAUDE.md: o glob achou um download antigo do outro padrao de
nome e o script copiou sem reclamar. Dimensao igual nao denunciou nada. Logo o
portao tem que ser o carimbo de hora, e ele tem que ABORTAR, nao avisar.

`scripts/` nao e pacote importavel, entao o modulo e carregado pelo caminho.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import time
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_MODULO = RAIZ / "scripts" / "_pega_download.py"


def _carrega_modulo():
    spec = importlib.util.spec_from_file_location("_pega_download", CAMINHO_MODULO)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = modulo
    spec.loader.exec_module(modulo)
    return modulo


pega = _carrega_modulo()


def _arquivo_com_idade(tmp_path: Path, segundos: float) -> str:
    """Cria um arquivo e envelhece o mtime em `segundos`."""
    alvo = tmp_path / "Imagem do ChatGPT 30 de setembro de 2026.png"
    alvo.write_bytes(b"png-falso")
    quando = time.time() - segundos
    os.utime(alvo, (quando, quando))
    return str(alvo)


def test_teto_de_idade_e_tres_minutos():
    assert pega.IDADE_MAXIMA_S == 180


def test_exigir_recente_levanta_system_exit_em_arquivo_antigo(tmp_path: Path):
    antigo = _arquivo_com_idade(tmp_path, pega.IDADE_MAXIMA_S + 3600)
    with pytest.raises(SystemExit) as erro:
        pega.exigir_recente(antigo)
    assert "ABORTADO" in str(erro.value)
    assert "arquivo antigo" in str(erro.value)


def test_exigir_recente_aceita_arquivo_recem_baixado(tmp_path: Path):
    recente = _arquivo_com_idade(tmp_path, 2)
    pega.exigir_recente(recente)  # nao levanta


def test_exigir_recente_reprova_um_segundo_alem_do_teto(tmp_path: Path):
    limite = _arquivo_com_idade(tmp_path, pega.IDADE_MAXIMA_S + 1)
    with pytest.raises(SystemExit):
        pega.exigir_recente(limite)
