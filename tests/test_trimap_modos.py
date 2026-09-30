"""Modos do trimap e o portao de premissa.

Contexto (medido em 30/09/2026 sobre os packshots reais de Uberlandia): o modo
original `fundo_uniforme` estima a cor do fundo pela mediana das 4 bordas. Essas
fotos nao sao packshot de fundo neutro -- e o pacote deitado no chao ao lado de
uma parede, com emenda visivel entre duas superficies de tom diferente. Nao
existe UMA cor de fundo, existem duas, e a premissa do metodo nao e satisfeita.
O resultado foram 3 recortes cobrindo 62,8% a 64,3% do quadro, com o alfa
encostando na borda da imagem nos tres -- ou seja, parede e chao vieram junto.

O laudo numerico sozinho nao pegou isso: 1 dos 3 saiu `aprovado=true` mesmo
carregando um naco da parede. Por isso o portao deste arquivo e geometrico, nao
fotometrico: **packshot de embalagem nao encosta na borda do quadro**.

Arquivo separado de tests/test_trimap.py de proposito -- aquele guarda o
comportamento do modo original, que nao pode mudar.
"""

import numpy as np
import pytest

from instagram.recorte.trimap import (
    PremissaDeRecorteViolada,
    mascara_objeto,
    medir_populacoes,
)


def _fundo_de_dois_tons(largura=420, altura=300):
    """Parede clara a esquerda, chao claro (mais escuro) a direita.

    Reproduz a geometria que quebrou o modo original: duas superficies claras
    com ~45 niveis de diferenca entre elas e uma emenda vertical no meio.
    """
    rng = np.random.default_rng(7)
    img = np.empty((altura, largura, 3), dtype=np.uint8)
    corte = int(largura * 0.62)
    img[:, :corte] = (232, 231, 227)          # parede
    img[:, corte:] = (188, 179, 165)          # chao de madeira clara
    img[:, corte - 2:corte + 2] = (150, 140, 126)   # emenda, mais escura
    ruido = rng.normal(0, 2.0, img.shape)
    return np.clip(img.astype(np.float64) + ruido, 0, 255).astype(np.uint8)


def _objeto_escuro_em_dois_tons():
    """O caso que quebrou: embalagem escura sobre DUAS superficies claras.

    O objeto nao toca nenhuma borda -- e isso que o portao tem que constatar.
    """
    img = _fundo_de_dois_tons()
    img[70:230, 90:330] = (46, 44, 42)
    # tipografia clara impressa: vira buraco na mascara se ninguem preencher
    img[120:150, 150:290] = (238, 236, 232)
    return img


def _objeto_escuro_vazando_para_a_borda():
    """Mesmo objeto, mas encostando no topo e na esquerda do quadro.

    Nao e packshot: e foto em que o fundo escuro entrou no recorte. O portao
    tem que recusar, nao entregar um alfa plausivel.
    """
    img = _fundo_de_dois_tons()
    img[0:230, 0:330] = (46, 44, 42)
    return img


# --- (a) objeto escuro em fundo claro de DOIS tons ------------------------


def test_objeto_escuro_separa_embalagem_de_dois_fundos_claros():
    img = _objeto_escuro_em_dois_tons()
    mascara, diag = mascara_objeto(img, modo="objeto_escuro")

    assert diag["modo"] == "objeto_escuro"
    assert not diag["toca_borda"], diag
    # so o objeto: 160x240 de 300x420 = 30,5% do quadro
    assert 0.22 < diag["fracao_coberta"] < 0.42, diag
    # e o miolo do objeto e solido, buraco de tipografia preenchido
    assert mascara[135, 200] == 1
    assert mascara[150, 200] == 1
    assert mascara[10, 10] == 0


def test_objeto_escuro_nao_encosta_em_nenhuma_das_quatro_bordas():
    mascara, _ = mascara_objeto(_objeto_escuro_em_dois_tons(),
                                modo="objeto_escuro")
    assert mascara[0, :].sum() == 0
    assert mascara[-1, :].sum() == 0
    assert mascara[:, 0].sum() == 0
    assert mascara[:, -1].sum() == 0


# --- (b) o portao ---------------------------------------------------------


def test_portao_recusa_componente_que_toca_a_borda():
    with pytest.raises(PremissaDeRecorteViolada) as e:
        mascara_objeto(_objeto_escuro_vazando_para_a_borda(),
                       modo="objeto_escuro")
    msg = str(e.value)
    assert "borda" in msg.lower()
    assert "objeto_escuro" in msg


def test_portao_recusa_componente_que_cobre_quase_o_quadro_inteiro():
    """Cobertura acima de 60% e quase certeza de que o fundo entrou junto."""
    img = _fundo_de_dois_tons()
    img[20:280, 20:400] = (46, 44, 42)   # 260x380 de 300x420 = 78%
    img[0, 0] = (46, 44, 42)             # nao e isso que dispara aqui
    with pytest.raises(PremissaDeRecorteViolada) as e:
        mascara_objeto(img, modo="objeto_escuro")
    assert "%" in str(e.value)


def test_portao_pega_o_modo_antigo_nessa_foto():
    """`fundo_uniforme` e exatamente o que quebrou: tem que recusar, nao passar."""
    with pytest.raises(PremissaDeRecorteViolada):
        mascara_objeto(_objeto_escuro_em_dois_tons(), modo="fundo_uniforme")


# --- (c) o modo auto ------------------------------------------------------


def test_auto_escolhe_objeto_escuro_no_fundo_de_dois_tons():
    _, diag = mascara_objeto(_objeto_escuro_em_dois_tons(), modo="auto")
    assert diag["modo"] == "objeto_escuro", diag
    # e a decisao fica auditavel: qual modo foi tentado e por que caiu
    tentados = [t["modo"] for t in diag["tentativas"]]
    assert "fundo_uniforme" in tentados
    assert diag["tentativas"][0]["recusa"], diag


def test_auto_mantem_fundo_uniforme_quando_o_fundo_e_mesmo_uniforme():
    """Packshot de fundo neutro nao muda de rota so porque o modo novo existe."""
    img = np.full((300, 420, 3), 235, dtype=np.uint8)
    img[80:220, 120:300] = (60, 45, 30)
    _, diag = mascara_objeto(img, modo="auto")
    assert diag["modo"] == "fundo_uniforme", diag


def test_medida_das_populacoes_e_registrada_no_diagnostico():
    m = medir_populacoes(_objeto_escuro_em_dois_tons())
    assert m["separacao"] > 60
    assert 0.05 < m["fracao_escura"] < 0.60
    assert m["l_medio_escuro"] < m["l_medio_claro"]


def test_modo_desconhecido_falha_alto():
    with pytest.raises(ValueError):
        mascara_objeto(_objeto_escuro_em_dois_tons(), modo="chute")
