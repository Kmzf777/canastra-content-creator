"""Testes do fluxo 2: recorte por croma e composicao com reiluminacao.

Tudo aqui e sintetico, gerado com Pillow. `base-curada/` e gitignored e nao
existe no worktree; alem disso, um teste que depende de arquivo grande na maquina
certa nao trava regra nenhuma - so falha em outro lugar.

As cores das imagens sinteticas nao sao decorativas: reproduzem as leituras HSV
que `_ref-scripts/medir_sat.py` tirou do packshot real, para o limiar 75/120
estar sendo exercitado contra os mesmos vizinhos que ele precisa separar na
producao.
"""

from __future__ import annotations

import inspect
import math

import pytest
from PIL import Image, ImageDraw, ImageStat

from cie import composicao
from cie.composicao import (
    S_MIN_MEDIDO,
    V_MIN_MEDIDO,
    compor,
    mascara_croma,
    medir_direcao_luz,
    perfil_luminancia,
    preencher_furos,
    recortar,
)
from cie.errors import CieError

# --------------------------------------------------------------------------- #
# cores medidas em _ref-scripts/medir_sat.py, convertidas para RGB
# --------------------------------------------------------------------------- #

PAREDE = (190, 190, 190)      # S=0    V=190  - fundo facil
BANCADA = (150, 148, 142)     # S~14   V=150  - fundo claro, pouco saturado
SOMBRA = (95, 84, 73)         # S~59   V=95   - o fundo MAIS PARECIDO com kraft
KRAFT = (160, 130, 100)       # S~96   V=160  - a embalagem
TINTA = (38, 33, 28)          # V=38          - tipografia preta impressa

RETANGULO = (150, 180, 550, 700)   # 400 x 520
FURO = (270, 400, 430, 480)        # 160 x 80, centrado no retangulo
FONTE = (700, 900)


def packshot_sintetico() -> Image.Image:
    """Parede, bancada, uma mancha de sombra e o 'pacote' com tipografia preta.

    A mancha de sombra existe de proposito: com S~59 ela e o unico fundo que
    chega perto do kraft em saturacao, e e o que prova que o limiar de luminancia
    tambem esta fazendo trabalho.
    """
    img = Image.new("RGB", FONTE, PAREDE)
    d = ImageDraw.Draw(img)
    d.rectangle([0, int(FONTE[1] * 0.78), FONTE[0], FONTE[1]], fill=BANCADA)
    d.rectangle([580, 300, 670, 430], fill=SOMBRA)
    d.rectangle(list(RETANGULO), fill=KRAFT)
    d.rectangle(list(FURO), fill=TINTA)
    return img


def cena_lisa(tamanho: tuple[int, int] = (800, 900), cor: tuple[int, int, int] = (150, 150, 150)):
    return Image.new("RGB", tamanho, cor)


def recorte_solido(tamanho: tuple[int, int] = (200, 400)) -> Image.Image:
    """Silhueta retangular, cor chapada: qualquer assimetria na saida veio de `compor`."""
    return Image.new("RGBA", tamanho, (170, 140, 110, 255))


def cena_gradiente(
    tamanho: tuple[int, int] = (700, 900),
    *,
    claro: str,
    escuro_min: int = 60,
    claro_max: int = 200,
) -> Image.Image:
    """Rampa de luminancia. `claro` diz de que lado do quadro a luz vem.

    E o mesmo sinal que o chao ao redor de um objeto tem na cena real: mais claro
    do lado da luz, mais escuro do lado da sombra.
    """
    largura, altura = tamanho
    vertical = claro in ("cima", "baixo")
    n = altura if vertical else largura
    rampa = [round(escuro_min + (claro_max - escuro_min) * i / (n - 1)) for i in range(n)]
    if claro in ("esquerda", "cima"):
        rampa.reverse()
    if vertical:
        semente = Image.new("L", (1, altura))
    else:
        semente = Image.new("L", (largura, 1))
    semente.putdata(rampa)
    return semente.resize(tamanho, Image.NEAREST).convert("RGB")


def luminancia(img: Image.Image, caixa: tuple[int, int, int, int]) -> float:
    return ImageStat.Stat(img.convert("L").crop(caixa)).mean[0]


def dif_angular(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


# --------------------------------------------------------------------------- #
# 1. preenchimento de furos - o teste mais importante do modulo
# --------------------------------------------------------------------------- #


def test_furo_de_tipografia_fica_opaco_no_alfa():
    """O texto preto impresso e INTERIOR a silhueta: tem que voltar opaco.

    Sem preencher furos, o logotipo vira buraco - a peca sai com a marca vazada.
    Este e o motivo de o recorte por croma precisar da etapa de furos, e o teste
    que trava isso.
    """
    recorte = recortar(packshot_sintetico())
    alfa = recorte.getchannel("A")

    # O furo foi desenhado no centro do retangulo, entao no recorte cortado ao
    # bbox ele continua no centro - imune a jitter de alguns pixels no bbox.
    cx, cy = recorte.width // 2, recorte.height // 2
    dentro = alfa.crop((cx - 60, cy - 25, cx + 60, cy + 25))

    assert min(dentro.tobytes()) == 255, "o furo da tipografia ficou transparente"


def test_o_furo_realmente_cai_fora_do_limiar_de_croma():
    """Prova que o teste acima nao e vacuo: o furo NAO passa no limiar por si.

    Se a tinta preta passasse no croma, `preencher_furos` estaria sendo testado
    contra nada. Aqui a mascara crua mostra o buraco, e o mesmo `recortar` com o
    preenchimento desligado devolve alfa zero exatamente ali.
    """
    fonte = packshot_sintetico()
    furo_cx = (FURO[0] + FURO[2]) // 2
    furo_cy = (FURO[1] + FURO[3]) // 2

    crua = mascara_croma(fonte)
    assert crua.getpixel((furo_cx, furo_cy)) == 0, "a tinta preta passou no croma"
    assert crua.getpixel(((RETANGULO[0] + RETANGULO[2]) // 2, RETANGULO[1] + 40)) == 255

    sem_furos = recortar(fonte, com_preenchimento=False)
    cx, cy = sem_furos.width // 2, sem_furos.height // 2
    assert sem_furos.getchannel("A").getpixel((cx, cy)) == 0

    com_furos = recortar(fonte)
    assert com_furos.getchannel("A").getpixel((cx, cy)) == 255
    assert com_furos.size == sem_furos.size, "preencher furos nao pode mudar o bbox"


def test_preencher_furos_fecha_anel_e_preserva_fundo_externo():
    """Unitario da regra: o que se alcanca a partir da borda e fundo; o resto e furo."""
    mascara = Image.new("L", (200, 200), 0)
    d = ImageDraw.Draw(mascara)
    d.ellipse([40, 40, 160, 160], fill=255)
    d.ellipse([80, 80, 120, 120], fill=0)          # furo interior
    d.rectangle([0, 0, 20, 20], fill=0)            # fundo, alcancavel pela borda

    cheia = preencher_furos(mascara)

    assert cheia.getpixel((100, 100)) == 255, "o furo interior nao foi fechado"
    assert cheia.getpixel((5, 5)) == 0, "o fundo externo foi engolido"
    assert cheia.getpixel((100, 45)) == 255


# --------------------------------------------------------------------------- #
# 2. o recorte tem que remover o fundo de verdade
# --------------------------------------------------------------------------- #


def test_recorte_descarta_fundo_e_corta_ao_bbox():
    """A tentativa por flood fill deixou 47% de fundo colado. Croma nao pode repetir isso."""
    recorte = recortar(packshot_sintetico())
    largura_esperada = RETANGULO[2] - RETANGULO[0]
    altura_esperada = RETANGULO[3] - RETANGULO[1]

    assert abs(recorte.width - largura_esperada) <= 8
    assert abs(recorte.height - altura_esperada) <= 8

    alfa = recorte.getchannel("A").tobytes()
    opaco = sum(1 for v in alfa if v > 60) / len(alfa)
    assert opaco > 0.97, f"sobrou vazio dentro do bbox do pacote: {opaco:.1%} opaco"

    # E o fundo mais dificil (S~59, V~95) nao entrou na mascara.
    crua = mascara_croma(packshot_sintetico())
    assert crua.getpixel((620, 360)) == 0, "a sombra na parede foi confundida com kraft"
    assert crua.getpixel((40, 820)) == 0, "a bancada foi confundida com kraft"


# --------------------------------------------------------------------------- #
# 3. os limiares sao medicao exposta como parametro, nao numero cravado
# --------------------------------------------------------------------------- #


def test_limiares_medidos_sao_o_padrao_e_sao_parametros():
    """75/120 vieram de medir_sat.py. Ficam como padrao E como parametro."""
    assinatura = inspect.signature(recortar)
    assert assinatura.parameters["s_min"].default == S_MIN_MEDIDO == 75
    assert assinatura.parameters["v_min"].default == V_MIN_MEDIDO == 120


def test_a_medicao_que_gerou_os_limiares_esta_documentada():
    """Numero sem procedencia vira numero magico na proxima sessao.

    O docstring do modulo tem que carregar as leituras de `medir_sat.py`, senao
    ninguem sabe por que e 75/120 e alguem 'ajusta' no olho.
    """
    doc = composicao.__doc__ or ""
    for leitura in ("S ~ 7", "S ~ 35-44", "S ~ 60", "V ~ 95", "S ~ 92-103", "V ~ 146-176"):
        assert leitura in doc, f"o docstring do modulo nao registra {leitura!r}"
    assert "medir_sat.py" in doc


def test_o_limiar_e_o_que_separa_a_bancada_do_kraft():
    """Baixar o limiar traz a bancada junto: prova que o numero medido faz trabalho."""
    fonte = packshot_sintetico()
    ponto_bancada = (40, 820)

    assert mascara_croma(fonte).getpixel(ponto_bancada) == 0
    assert mascara_croma(fonte, s_min=10, v_min=100).getpixel(ponto_bancada) == 255


def test_limiar_impossivel_falha_alto():
    """Limiar que nao seleciona nada levanta erro, em vez de devolver PNG vazio."""
    with pytest.raises(CieError, match="nenhum pixel"):
        recortar(packshot_sintetico(), s_min=250, v_min=250)


# --------------------------------------------------------------------------- #
# 4. direcao de luz e MEDIDA
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("claro", "azimute_esperado"),
    [("direita", 0.0), ("esquerda", 180.0), ("cima", 270.0), ("baixo", 90.0)],
)
def test_medir_direcao_luz_le_o_lado_claro(claro: str, azimute_esperado: float):
    """O anel de luminancia devolve o azimute de onde a luz vem, nas 4 direcoes."""
    azimute = medir_direcao_luz(cena_gradiente(claro=claro), (350, 450), 120)
    assert dif_angular(azimute, azimute_esperado) < 10.0


def test_medicao_resiste_a_amostra_em_cima_do_objeto():
    """A licao: o probe original amostrou em cima do proprio caneco.

    Aqui um blob claro cobre parte do anel, como um objeto cortado pela
    amostragem. O maximo bruto do perfil aponta para o blob - que e exatamente o
    que um `argmax` ingenuo devolveria - e a medicao ainda assim acerta a luz.
    """
    cena = cena_gradiente(claro="esquerda")
    ImageDraw.Draw(cena).rectangle([315, 535, 385, 605], fill=(255, 255, 255))

    perfil = perfil_luminancia(cena, (350, 450), 120)
    graus_bruto = max(perfil, key=lambda leitura: leitura[1])[0]
    assert dif_angular(graus_bruto, 90.0) < 20.0, "o blob deveria dominar o maximo bruto"

    azimute = medir_direcao_luz(cena, (350, 450), 120)
    assert dif_angular(azimute, 180.0) < 15.0, f"a contaminacao moveu a medida: {azimute:.1f}"


def test_anel_fora_da_imagem_falha_em_vez_de_enviesar():
    """Amostra parcial enviesaria o ajuste em silencio. Melhor erro que numero errado."""
    with pytest.raises(CieError, match="nao cabe"):
        medir_direcao_luz(cena_gradiente(claro="direita"), (30, 450), 120)


def test_regiao_chapada_nao_tem_direcao_de_luz():
    with pytest.raises(CieError, match="gradiente"):
        medir_direcao_luz(cena_lisa((700, 900)), (350, 450), 120)


# --------------------------------------------------------------------------- #
# 5. compor: azimute obrigatorio, gradiente no sentido medido
# --------------------------------------------------------------------------- #

BASE_XY = (400, 700)
RECORTE_L, RECORTE_A = 200, 400
POS_X = BASE_XY[0] - RECORTE_L // 2          # 300
POS_TOPO = BASE_XY[1] - RECORTE_A           # 300


def test_azimute_de_luz_e_parametro_obrigatorio():
    """Nao existe direcao padrao razoavel. Quem compoe tem que ter medido (licao 6)."""
    assinatura = inspect.signature(compor)
    assert assinatura.parameters["azimute_luz"].default is inspect.Parameter.empty

    with pytest.raises(TypeError):
        compor(cena_lisa(), recorte_solido(), BASE_XY)  # type: ignore[call-arg]


def test_gradientes_opostos_produzem_imagens_diferentes():
    """Luz pela direita e luz pela esquerda nao podem sair iguais."""
    cena, recorte = cena_lisa(), recorte_solido()
    direita = compor(cena, recorte, BASE_XY, 0.0)
    esquerda = compor(cena, recorte, BASE_XY, 180.0)
    assert direita.tobytes() != esquerda.tobytes()


@pytest.mark.parametrize(("azimute", "lado_claro"), [(0.0, "direita"), (180.0, "esquerda")])
def test_reiluminacao_clareia_a_face_voltada_para_a_luz(azimute: float, lado_claro: str):
    """O gradiente lateral segue o azimute passado, nao um lado fixo no codigo."""
    comp = compor(cena_lisa(), recorte_solido(), BASE_XY, azimute)
    # Faixa bem dentro do corpo, longe da base (onde a oclusao escurece).
    meia_esq = (POS_X, POS_TOPO + 20, POS_X + RECORTE_L // 2, BASE_XY[1] - 40)
    meia_dir = (POS_X + RECORTE_L // 2, POS_TOPO + 20, POS_X + RECORTE_L, BASE_XY[1] - 40)

    esq, dir_ = luminancia(comp, meia_esq), luminancia(comp, meia_dir)
    if lado_claro == "direita":
        assert dir_ > esq + 5.0, f"esq {esq:.1f} dir {dir_:.1f}"
    else:
        assert esq > dir_ + 5.0, f"esq {esq:.1f} dir {dir_:.1f}"


@pytest.mark.parametrize(("azimute", "lado_da_sombra"), [(0.0, "esquerda"), (180.0, "direita")])
def test_sombra_cai_no_lado_oposto_a_luz(azimute: float, lado_da_sombra: str):
    """Luz pela direita joga sombra para a esquerda. O contrario denuncia a imagem."""
    cena = cena_lisa()
    comp = compor(cena, recorte_solido(), BASE_XY, azimute)

    # Faixas laterais fora da silhueta do objeto e fora da faixa de contato: o
    # unico efeito que pode escurece-las e a sombra projetada.
    topo, fundo_y = BASE_XY[1] - 140, BASE_XY[1] - 60
    caixa_esq = (POS_X - 170, topo, POS_X - 30, fundo_y)
    caixa_dir = (POS_X + RECORTE_L + 30, topo, POS_X + RECORTE_L + 170, fundo_y)

    esq, dir_ = luminancia(comp, caixa_esq), luminancia(comp, caixa_dir)
    limpo_esq, limpo_dir = luminancia(cena, caixa_esq), luminancia(cena, caixa_dir)

    if lado_da_sombra == "esquerda":
        assert esq < limpo_esq - 5.0, "nao ha sombra a esquerda"
        assert dir_ > esq + 5.0, f"esq {esq:.1f} dir {dir_:.1f}"
        assert abs(dir_ - limpo_dir) < 1.0, "vazou sombra para o lado da luz"
    else:
        assert dir_ < limpo_dir - 5.0, "nao ha sombra a direita"
        assert esq > dir_ + 5.0, f"esq {esq:.1f} dir {dir_:.1f}"
        assert abs(esq - limpo_esq) < 1.0, "vazou sombra para o lado da luz"


def test_oclusao_de_contato_escurece_logo_abaixo_da_base():
    """Sem oclusao de contato o objeto parece colado por cima da foto.

    Comparamos contra a MESMA composicao com `contato_opacidade=0`, e nao so
    contra a cena limpa: assim o escurecimento medido e da oclusao, e nao respingo
    da sombra projetada.
    """
    cena, recorte = cena_lisa(), recorte_solido()
    com = compor(cena, recorte, BASE_XY, 0.0)
    sem = compor(cena, recorte, BASE_XY, 0.0, contato_opacidade=0.0)

    # Logo abaixo da linha da base, dentro da pegada do objeto.
    faixa = (POS_X + 50, BASE_XY[1] + 1, POS_X + RECORTE_L - 50, BASE_XY[1] + 8)

    assert luminancia(com, faixa) < luminancia(cena, faixa) - 8.0
    assert luminancia(com, faixa) < luminancia(sem, faixa) - 8.0


def test_compor_nao_altera_a_cena_recebida():
    cena = cena_lisa()
    antes = cena.tobytes()
    compor(cena, recorte_solido(), BASE_XY, 0.0)
    assert cena.tobytes() == antes


def test_compor_exige_alfa_no_recorte():
    with pytest.raises(CieError, match="alfa"):
        compor(cena_lisa(), Image.new("RGB", (200, 400), (170, 140, 110)), BASE_XY, 0.0)


def test_recorte_de_recortar_entra_direto_em_compor():
    """As duas metades do fluxo 2 conversam: saida de `recortar` e entrada de `compor`."""
    recorte = recortar(packshot_sintetico())
    azimute = medir_direcao_luz(cena_gradiente(claro="direita"), (350, 450), 120)
    comp = compor(cena_lisa(), recorte, BASE_XY, azimute, altura_px=400)

    assert comp.mode == "RGB"
    assert comp.size == (800, 900)

    largura = max(1, round(recorte.width * 400 / recorte.height))
    px = BASE_XY[0] - largura // 2
    corpo = (px + 20, BASE_XY[1] - 380, px + largura - 20, BASE_XY[1] - 280)
    # O kraft e mais escuro que a cena cinza: se a media caiu, o pacote colou.
    assert luminancia(comp, corpo) < luminancia(cena_lisa(), corpo) - 5.0


def test_luz_de_topo_nao_inventa_gradiente_lateral():
    """Azimute 270 nao tem componente lateral: o correto e nao inclinar nada."""
    comp = compor(cena_lisa(), recorte_solido(), BASE_XY, 270.0)
    meia_esq = (POS_X, POS_TOPO + 20, POS_X + RECORTE_L // 2, BASE_XY[1] - 40)
    meia_dir = (POS_X + RECORTE_L // 2, POS_TOPO + 20, POS_X + RECORTE_L, BASE_XY[1] - 40)
    assert math.isclose(luminancia(comp, meia_esq), luminancia(comp, meia_dir), abs_tol=0.5)
