"""Testes dos blocos de prompt versionados.

Cada teste aqui trava uma licao que ja custou pelo menos uma rodada de geracao.
Nenhum e cosmetico. Se um deles falhar, o prompt montado volta a produzir o erro
descrito no docstring do teste.
"""

from __future__ import annotations

import re

import pytest

from cie.blocos import (
    ORDEM_CORPO,
    PADRAO,
    Bloco,
    BlocoError,
    carregar,
    carregar_todos,
    montar,
)

CENA = "Test scene: the kraft package sits on bare red earth at the foot of a coffee bush."

ARQUIVOS_ESPERADOS = {
    "luz-sol-pino",
    "hdr-celular",
    "foco-profundo",
    "espontaneidade",
    "preservar-embalagem",
    "dna-suave",
    "dna-classico",
    "dna-canela",
    "negativos",
}

DNAS = ("dna-suave", "dna-classico", "dna-canela")

# Palavra de negacao, com fronteira de palavra para "notches" nao virar "not".
_NEGACAO = re.compile(r"\b(not|no|never|nor|without)\b", re.IGNORECASE)


def afirmativo(texto: str) -> str:
    """So o que o bloco AFIRMA, jogando fora as clausulas que negam.

    Existe porque a correcao verificada do DNA (v1 -> v2) foi justamente
    ACRESCENTAR negacoes explicitas: "NOT an alpine mountain, NOT sharp
    triangular peaks, NOT tall pointed summits". Um teste que procurasse essas
    palavras no texto inteiro proibiria a propria correcao que funcionou. O que
    nao pode existir e a forma AFIRMATIVA - foi `jagged peaks`, afirmado na v1,
    que fez os tres modelos desenharem pico alpino.
    """
    return " | ".join(c for c in re.split(r"[,.;:\n]", texto) if not _NEGACAO.search(c))


def normalizar(texto: str) -> str:
    return " ".join(texto.split())


# --------------------------------------------------------------------------- #
# estrutura
# --------------------------------------------------------------------------- #


def test_os_nove_blocos_carregam():
    todos = carregar_todos()
    assert set(todos) == ARQUIVOS_ESPERADOS
    for nome, bloco in todos.items():
        assert isinstance(bloco, Bloco)
        assert bloco.nome == nome, "campo `nome` tem que bater com o nome do arquivo"
        assert bloco.descricao.strip(), f"{nome}: `descricao` vazia"
        assert bloco.texto.strip(), f"{nome}: `texto` vazio"


def test_papel_de_cada_bloco():
    papeis = {nome: b.papel for nome, b in carregar_todos().items()}
    assert papeis == {
        "preservar-embalagem": "preservacao",
        "dna-suave": "dna",
        "dna-classico": "dna",
        "dna-canela": "dna",
        "luz-sol-pino": "luz",
        "hdr-celular": "hdr",
        "foco-profundo": "foco",
        "espontaneidade": "espontaneidade",
        "negativos": "negativos",
    }


def test_bloco_inexistente_da_erro_util():
    with pytest.raises(BlocoError) as exc:
        carregar("luz-nublada")
    assert "luz-sol-pino" in str(exc.value), "o erro deve listar os blocos disponiveis"


def test_negativos_nunca_carregam_o_prefixo_avoid():
    """Regressao: `espontaneo.py` guardava NEG ja com "Avoid: " e o montador
    prefixava de novo, gravando "Avoid: Avoid: ..." nos prompts reais."""
    for bloco in carregar_todos().values():
        for termo in bloco.negativos:
            assert not termo.lower().startswith("avoid"), f"{bloco.nome}: {termo!r}"
    assert "Avoid: Avoid" not in montar(CENA)
    assert montar(CENA).count("Avoid:") == 1


def test_bloco_negativos_texto_bate_com_a_lista():
    """O `texto` do bloco de negativos e a mesma lista, so que serializada.
    Se os dois divergirem, uma copia esta desatualizada - foi exatamente assim
    que os blocos divergiram entre os scripts."""
    bloco = carregar("negativos")
    do_texto = [normalizar(t) for t in bloco.texto.split(",") if t.strip()]
    assert do_texto == list(bloco.negativos)


# --------------------------------------------------------------------------- #
# regra 1: o bloco de foco nunca sai do prompt
# --------------------------------------------------------------------------- #


def test_foco_entra_por_padrao():
    """Sem bloco anti-bokeh o modelo entrega fundo desfocado, e desfoque nao se
    remove em pos: tone mapping, ruido, halo e JPEG se adicionam depois;
    profundidade de campo rasa, nao. Morre na geracao ou nao morre."""
    assert "foco-profundo" in PADRAO
    prompt = montar(CENA)
    assert carregar("foco-profundo").texto in prompt


def test_montar_sem_foco_levanta_erro():
    with pytest.raises(BlocoError) as exc:
        montar(CENA, blocos=["luz-sol-pino", "hdr-celular", "negativos"])
    assert "foco" in str(exc.value).lower()


def test_montar_com_foco_explicito_passa():
    prompt = montar(CENA, blocos=["foco-profundo"])
    assert "EVERYTHING IN THE FRAME IS SHARP" in prompt


def test_foco_descreve_a_fisica_de_sensor_pequeno():
    texto = carregar("foco-profundo").texto
    assert "1/1.7 inch" in texto and "f/1.8" in texto
    assert "depth of field" in texto
    # nevoa suaviza a distancia; desfoco nunca
    assert "haze" in texto and "never from defocus" in texto


def test_cena_vazia_levanta_erro():
    with pytest.raises(BlocoError):
        montar("   ")


# --------------------------------------------------------------------------- #
# regra 2: os negativos tem que conter anti-bokeh e anti-anuncio
# --------------------------------------------------------------------------- #

ANTI_BOKEH = ("bokeh", "shallow focus", "portrait mode", "background blur")
ANTI_ANUNCIO = ("product photography", "advertisement")


@pytest.mark.parametrize("termo", [*ANTI_BOKEH, *ANTI_ANUNCIO])
def test_prompt_montado_nega_bokeh_e_anuncio(termo: str):
    linha = montar(CENA).rsplit("Avoid:", 1)[1]
    assert termo in linha


@pytest.mark.parametrize("termo", [*ANTI_BOKEH, *ANTI_ANUNCIO])
def test_bloco_de_negativos_traz_os_termos(termo: str):
    assert termo in carregar("negativos").negativos


def test_anti_bokeh_sobrevive_sem_o_bloco_de_negativos():
    """Uma cena de varanda monta sem `negativos` (que nega mesa, pano e crochet,
    que naquela cena existem de verdade). A cobertura anti-bokeh e anti-anuncio
    nao pode sumir junto."""
    prompt = montar(CENA, blocos=["luz-sol-pino", "hdr-celular", "foco-profundo", "espontaneidade"])
    linha = prompt.rsplit("Avoid:", 1)[1]
    for termo in (*ANTI_BOKEH, *ANTI_ANUNCIO):
        assert termo in linha, termo


# --------------------------------------------------------------------------- #
# regra 3: a serra e chapada de topo plano, nunca alpina
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("nome", DNAS)
@pytest.mark.parametrize("proibido", ["jagged peaks", "alpine", "pointed summits"])
def test_dna_nunca_afirma_pico_alpino(nome: str, proibido: str):
    """Licao 2 do registro: a v1 do DNA dizia `jagged peaks` e os TRES modelos
    desenharam pico alpino pontudo. A Serra da Canastra e uma chapada de topo
    plano. O modelo e obediente - ele erra exatamente onde a descricao erra."""
    assert proibido.lower() not in afirmativo(carregar(nome).texto).lower()


@pytest.mark.parametrize("nome", DNAS)
def test_jagged_nao_aparece_nem_negado(nome: str):
    """`jagged` nunca foi usado como negacao em versao verificada nenhuma: era a
    palavra afirmativa da v1. Aqui ela some do arquivo inteiro."""
    assert "jagged" not in carregar(nome).texto.lower()


@pytest.mark.parametrize("nome", DNAS)
def test_dna_afirma_chapada_de_topo_plano(nome: str):
    """Contraprova do teste acima: garante que o filtro de negacao nao esvaziou o
    texto e que a descricao correta continua sendo AFIRMADA."""
    afirma = afirmativo(carregar(nome).texto)
    assert "FLAT-TOPPED TABLELAND" in afirma
    assert "mesa ridge" in afirma


@pytest.mark.parametrize("nome", DNAS)
def test_dna_nega_pico_alpino_na_lista_de_negativos(nome: str):
    negativos = carregar(nome).negativos
    assert "alpine summits" in negativos
    assert "sharp triangular mountain peaks" in negativos


# --------------------------------------------------------------------------- #
# regra 4: SPECIALTY soletrado e 250g com os digitos nomeados
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("nome", ["dna-suave", "dna-classico"])
def test_dna_soletra_specialty(nome: str):
    """Defesa contra `SOSCIALTY`. O Gemini trata a referencia como inspiracao e
    REDESENHA o rotulo; quanto menor o pacote no quadro, mais ele "completa" por
    conta propria. A ancora e a string exata, entre aspas e soletrada."""
    texto = carregar(nome).texto
    assert '"SPECIALTY"' in texto
    assert "S-P-E-C-I-A-L-T-Y" in texto
    assert "SOSCIALTY" in texto, "o erro tem que ser nomeado para ser proibido"


@pytest.mark.parametrize("nome", DNAS)
def test_dna_nomeia_os_digitos_de_250g(nome: str):
    """Defesa contra `288g`."""
    texto = carregar(nome).texto
    assert '"250g"' in texto
    assert "TWO HUNDRED AND FIFTY GRAMS" in texto
    assert '"2", "5", "0"' in texto
    assert "288" in texto, "o erro tem que ser nomeado para ser proibido"


def test_dna_canela_cita_specialty_so_para_negar():
    """O Canela nao tem a caixa SCA. Mas o modelo ja viu os outros dois SKUs e
    desenha a caixa sozinho se ninguem proibir - entao a string aparece, sempre
    dentro de uma negacao."""
    texto = carregar("dna-canela").texto
    assert '"SPECIALTY"' in texto
    assert '"SPECIALTY"' not in afirmativo(texto)
    assert '"SCA 80+"' not in afirmativo(texto)


# --------------------------------------------------------------------------- #
# regra 5: luz de fazenda e sol a pino, nunca nublado
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("proibido", ["overcast", "cloudy"])
def test_nenhum_bloco_de_luz_afirma_nublado(proibido: str):
    """A luz real da fazenda e sol a pino: ceu azul com cumulus, sombra dura,
    iPhone 7, ISO 20, marco, meio-dia. O nublado de `humanizar.py` e
    `carrossel.py` era invencao - e o alvo de calibracao de camera foi medido
    NESSAS fotos de sol forte, entao pedir nublado desalinha o motor do alvo."""
    luzes = [b for b in carregar_todos().values() if b.papel == "luz"]
    assert luzes, "tem que existir pelo menos um bloco de luz"
    for bloco in luzes:
        assert proibido not in afirmativo(bloco.texto).lower(), bloco.nome


@pytest.mark.parametrize("proibido", ["overcast", "cloudy"])
def test_luz_lista_nublado_como_negativo(proibido: str):
    assert proibido in carregar("luz-sol-pino").negativos


def test_luz_afirma_sol_a_pino():
    afirma = afirmativo(carregar("luz-sol-pino").texto)
    assert "HARSH OVERHEAD MIDDAY SUN" in afirma
    assert "bright blue sky with hard-edged white cumulus" in afirma


def test_hdr_nao_pede_dourado_quente():
    """Cast das altas medido na base real e 0,969 (puxa AZUL). Dourado quente e
    assinatura de IA. Saturacao alvo 70: base lavada, nao vibrante."""
    afirma = afirmativo(carregar("hdr-celular").texto)
    assert "washed white balance" in afirma
    assert "golden" not in afirma.lower()
    assert "muted low" in afirma


# --------------------------------------------------------------------------- #
# os tres SKUs
# --------------------------------------------------------------------------- #


def test_dna_suave_e_kraft_com_tinta_preta():
    texto = carregar("dna-suave").texto
    assert "kraft paper pouch" in texto
    assert "flat matte BLACK ink" in texto
    assert '"SUAVE" over "TORRADO E MOIDO"' in texto


def test_dna_classico_e_filme_preto_com_tinta_branca():
    texto = carregar("dna-classico").texto
    assert "MATTE BLACK FILM" in texto
    assert "flat WHITE ink" in texto
    assert '"CLASSICO"' in texto
    assert "CLÁSSICO" in texto, "o acento no A tem que ser dito"
    assert "kraft paper pouch" not in texto


def test_dna_canela_e_filme_vermelho_metalizado_sem_caixa_sca():
    texto = carregar("dna-canela").texto
    assert "GLOSSY METALLIC RED FILM" in texto
    assert "flat WHITE ink" in texto
    assert "CINNAMON QUILLS" in texto
    assert '"CAFE TORRADO E" over "MOIDO COM CANELA"' in texto
    assert "MOÍDO" in texto


@pytest.mark.parametrize("nome", DNAS)
def test_dna_traz_os_elementos_comuns_aos_tres(nome: str):
    texto = carregar(nome).texto
    assert "Café" in texto, "o acento agudo no e tem que ser exigido"
    assert "DRY BRUSH script" in texto
    assert "brush swash" in texto
    assert "(R) registered trademark" in texto
    assert '"Desde 1985"' in texto
    assert "rounded rectangle outline" in texto
    assert "crimped fold" in texto and "zip lock" in texto


# --------------------------------------------------------------------------- #
# o compositor
# --------------------------------------------------------------------------- #


def test_ordem_de_montagem():
    """preservacao -> cena -> DNA -> luz -> HDR -> foco -> espontaneidade -> Avoid,
    que e a ordem verificada em `_ref-scripts/espontaneo.py`."""
    blocos = [
        "espontaneidade",
        "negativos",
        "foco-profundo",
        "hdr-celular",
        "luz-sol-pino",
        "dna-suave",
        "preservar-embalagem",
    ]  # embaralhados de proposito: quem ordena e o compositor
    prompt = montar(CENA, blocos=blocos)
    posicoes = [
        prompt.index(carregar("preservar-embalagem").texto),
        prompt.index(CENA),
        prompt.index(carregar("dna-suave").texto),
        prompt.index(carregar("luz-sol-pino").texto),
        prompt.index(carregar("hdr-celular").texto),
        prompt.index(carregar("foco-profundo").texto),
        prompt.index(carregar("espontaneidade").texto),
        prompt.index("Avoid:"),
    ]
    assert posicoes == sorted(posicoes)
    assert len(ORDEM_CORPO) == 7


def test_blocos_separados_por_linha_em_branco():
    prompt = montar(CENA, blocos=["foco-profundo"])
    assert "\n\n" in prompt
    assert prompt.startswith(CENA)


def test_negativos_extra_entram_no_fim():
    prompt = montar(CENA, negativos_extra=["blue painted wood", "zip lock top"])
    linha = prompt.rsplit("Avoid:", 1)[1]
    assert "blue painted wood" in linha
    assert "zip lock top" in linha
    assert prompt.endswith("zip lock top.")


def test_negativos_repetidos_saem_uma_vez_so():
    prompt = montar(
        CENA,
        blocos=["luz-sol-pino", "hdr-celular", "foco-profundo", "negativos"],
        negativos_extra=["BOKEH", "bokeh"],
    )
    linha = prompt.rsplit("Avoid:", 1)[1]
    termos = [t.strip().lower() for t in linha.rstrip(".").split(",")]
    assert len(termos) == len(set(termos))
    assert termos.count("crushed blacks") == 1, "luz e hdr repetem esse termo"


def test_montar_aceita_objetos_bloco():
    foco = carregar("foco-profundo")
    assert foco.texto in montar(CENA, blocos=[foco])


def test_preservar_nao_descreve_a_arte_da_embalagem():
    """O bloco de preservacao existe justamente para NAO descrever o rotulo. No
    fluxo de `/images/edits` a arte vem dos pixels; descrever faz o modelo
    redesenhar e produzir um sosia da marca."""
    texto = carregar("preservar-embalagem").texto
    for palavra in ("CANASTRA", "Desde 1985", "250g", "SPECIALTY", "swash", "mountain"):
        assert palavra not in texto, f"preservacao nao pode citar {palavra!r}"
