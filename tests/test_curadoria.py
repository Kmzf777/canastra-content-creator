"""Testes da curadoria: forense, camadas de permissao e separacao exaustiva.

As imagens sao sinteticas (Pillow, com EXIF montado a mao). Nada aqui le
`base-curada/` nem `imagens/`, que sao gitignored e nao existem no worktree.
O que os testes travam sao as tres regras inegociaveis de CLAUDE.md mais a
exaustividade da separacao.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest
from PIL import Image, ImageFilter
from PIL.TiffImagePlugin import IFDRational

from cie.curadoria import (
    LARGURAS_PINTEREST,
    MAPA_BASE_CURADA,
    PERMISSOES,
    USOS,
    ArquivoIlegivel,
    Camada,
    ClassificacaoIncompleta,
    ClassificacaoIndefinida,
    EntradaMapa,
    Permissoes,
    SeparacaoInvalida,
    agrupar_por_gps,
    arquivos_da_base,
    classificar,
    classificar_diretorio,
    escrever_csv_triagem,
    filtrar_por_uso,
    parece_sintetica,
    perfil,
    perfis,
    pode_descrever_em_texto,
    pode_usar,
    separar,
    validar_mapa,
    verificar_exaustividade,
)

#: Coordenadas reais das duas origens da base (ver o mapa de curadoria).
FAZENDA_MEDEIROS = (-20.3576, -46.1975)
TORREFACAO_UBERLANDIA = (-18.9186, -48.2772)

#: Resolucao "de foto de celular": passa folgado dos 8 MP da heuristica.
FOTO = (3500, 2600)
#: 736 px de largura e a assinatura do CDN do Pinterest na camada 03.
PIN = (736, 1104)


# --------------------------------------------------------------------------- #
# Fabrica de imagens sinteticas
# --------------------------------------------------------------------------- #


def _para_dms(valor: float) -> tuple[float, float, float]:
    graus = abs(valor)
    d = int(graus)
    m = int((graus - d) * 60)
    s = round((((graus - d) * 60) - m) * 60, 4)
    return (float(d), float(m), s)


def escrever_jpeg(
    caminho: Path,
    tamanho: tuple[int, int] = FOTO,
    *,
    marca: str | None = None,
    modelo: str | None = None,
    software: str | None = None,
    data: str | None = None,
    iso: int | None = None,
    abertura: float | None = None,
    focal_mm: float | None = None,
    exposicao: tuple[int, int] | None = None,
    orientacao: int | None = None,
    gps: tuple[float, float] | None = None,
    altitude_m: float | None = None,
    borrar: float = 0.0,
    seed: int = 7,
) -> Path:
    """Gera um JPEG com ruido em blocos e o EXIF pedido.

    Ruido em bloco reamostrado: barato de gerar e com microcontraste suficiente
    para o Laplaciano da nitidez ter o que medir.
    """
    caminho.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    tile = Image.frombytes("RGB", (64, 64), bytes(rng.randrange(256) for _ in range(64 * 64 * 3)))
    imagem = tile.resize(tamanho, Image.NEAREST)
    if borrar:
        imagem = imagem.filter(ImageFilter.GaussianBlur(borrar))

    exif = Image.Exif()
    if marca:
        exif[0x010F] = marca
    if modelo:
        exif[0x0110] = modelo
    if software:
        exif[0x0131] = software
    if data:
        exif[0x0132] = data
    if orientacao:
        exif[0x0112] = orientacao

    if any(v is not None for v in (data, iso, abertura, focal_mm, exposicao)):
        ifd = exif.get_ifd(0x8769)
        if data:
            ifd[0x9003] = data
        if iso is not None:
            ifd[0x8827] = iso
        if abertura is not None:
            ifd[0x829D] = abertura
        if focal_mm is not None:
            ifd[0x920A] = focal_mm
        if exposicao is not None:
            ifd[0x829A] = IFDRational(*exposicao)

    if gps is not None:
        lat, lon = gps
        bloco = exif.get_ifd(0x8825)
        bloco[1] = "S" if lat < 0 else "N"
        bloco[2] = _para_dms(lat)
        bloco[3] = "W" if lon < 0 else "E"
        bloco[4] = _para_dms(lon)
        if altitude_m is not None:
            bloco[5] = 1 if altitude_m < 0 else 0
            bloco[6] = abs(altitude_m)

    imagem.save(caminho, format="JPEG", quality=70, exif=exif)
    return caminho


def foto_iphone(caminho: Path, **kwargs) -> Path:
    """Assinatura da camada 01: EXIF de camera + GPS (iPhone 7, Medeiros)."""
    padrao = dict(
        marca="Apple",
        modelo="iPhone 7",
        software="10.3.1",
        data="2017:03:15 12:04:11",
        iso=20,
        abertura=1.8,
        focal_mm=3.99,
        exposicao=(1, 2000),
        gps=FAZENDA_MEDEIROS,
        altitude_m=1250.0,
    )
    padrao.update(kwargs)
    return escrever_jpeg(caminho, **padrao)  # type: ignore[arg-type]


# --------------------------------------------------------------------------- #
# REGRA 1 e 2: o que cada camada libera
# --------------------------------------------------------------------------- #


def test_permissoes_batem_com_a_tabela_do_claude_md():
    assert PERMISSOES[Camada.REAL_VERIFICADA] == Permissoes(True, True, True)
    assert PERMISSOES[Camada.REAL_NAO_VERIFICADA] == Permissoes(False, False, False)
    assert PERMISSOES[Camada.MOOD_TERCEIROS] == Permissoes(False, False, False)
    assert PERMISSOES[Camada.QUARENTENA] == Permissoes(False, False, False)
    # Toda camada precisa de entrada: camada nova sem permissao declarada quebra aqui.
    assert set(PERMISSOES) == set(Camada)
    assert USOS == ("referencia_de_imagem", "fonte_style_dna", "recorte")


def test_mood_de_terceiros_nunca_vira_pixel():
    """REGRA 1: scrape de terceiros so serve como descritor textual.

    Uma das 16 tem marca d'agua (@thamylis.pine...) e outra tem rosto
    identificavel de quem nao autorizou. Mandar qualquer uma como guidance
    publica pixel de terceiro numa peca da marca.
    """
    assert pode_usar(Camada.MOOD_TERCEIROS, "referencia_de_imagem") is False
    assert pode_usar(Camada.MOOD_TERCEIROS, "fonte_style_dna") is False
    assert pode_usar(Camada.MOOD_TERCEIROS, "recorte") is False
    # O unico uso que sobra: descrever a estetica em texto.
    assert pode_descrever_em_texto(Camada.MOOD_TERCEIROS) is True


def test_quarentena_nao_libera_uso_nenhum():
    """REGRA 2: quarentena e False em todos os usos, sem excecao."""
    for uso in USOS:
        assert pode_usar(Camada.QUARENTENA, uso) is False, uso
    assert pode_descrever_em_texto(Camada.QUARENTENA) is False


def test_apenas_a_camada_verificada_libera_alguma_coisa():
    for uso in USOS:
        liberadas = [camada for camada in Camada if pode_usar(camada, uso)]
        assert liberadas == [Camada.REAL_VERIFICADA], uso


def test_pode_usar_recusa_uso_desconhecido():
    """Uso escrito errado nao pode virar 'liberado' por acidente."""
    with pytest.raises(ValueError, match="uso desconhecido"):
        pode_usar(Camada.MOOD_TERCEIROS, "referencia")
    with pytest.raises(ValueError):
        pode_usar(Camada.REAL_VERIFICADA, "style_dna")


def test_camada_desconhecida_e_erro():
    with pytest.raises(ValueError):
        pode_usar("05-inventada", "recorte")


# --------------------------------------------------------------------------- #
# REGRA 3: sintetica vai para a quarentena
# --------------------------------------------------------------------------- #


def test_gemini_generated_vai_para_quarentena_mesmo_com_resolucao_de_foto(tmp_path):
    """REGRA 3: os dois `Gemini_Generated_Image_*.jpg` estavam nas pastas de produto.

    O mesmo pixel, com nome neutro, seria classificado como foto nossa nao
    verificada - e o nome e a unica coisa que o separa da destilacao de estilo.
    """
    sintetica = escrever_jpeg(tmp_path / "Gemini_Generated_Image_hhlj5jhhlj5jhhlj.jpg", FOTO)
    disfarcada = escrever_jpeg(tmp_path / "Canela (9).jpg", FOTO)

    assert classificar(perfil(sintetica)) is Camada.QUARENTENA
    assert classificar(perfil(disfarcada)) is Camada.REAL_NAO_VERIFICADA
    assert pode_usar(classificar(perfil(sintetica)), "fonte_style_dna") is False


def test_nome_de_gerador_ganha_ate_de_exif_de_camera(tmp_path):
    """O passe do gerador roda antes de tudo.

    Falso positivo custa uma foto real fora da base; falso negativo ensina ao
    motor o look sintetico que o projeto existe para evitar.
    """
    foto = foto_iphone(tmp_path / "IMG_1398.JPG")
    assert classificar(perfil(foto)) is Camada.REAL_VERIFICADA
    # Mesmo perfil, nome de gerador passado explicitamente.
    assert classificar(perfil(foto), "Gemini_Generated_Image_rw2resrw2resrw2r.jpg") is Camada.QUARENTENA


def test_software_de_gerador_no_exif_tambem_cai_na_quarentena(tmp_path):
    arquivo = escrever_jpeg(tmp_path / "cena-bonita.jpg", FOTO, software="Gemini 3 Pro Image")
    assert classificar(perfil(arquivo)) is Camada.QUARENTENA


@pytest.mark.parametrize(
    "nome",
    [
        "Gemini_Generated_Image_hhlj5jhhlj5jhhlj.jpg",
        "gemini_generated_image_abc.png",
        "ChatGPT Image 12 de abr.png",
        "midjourney_v6_00021.png",
        "DALL-E 2025-04-10.png",
        "nano-banana-teste.jpg",
        "cena_generated_image_02.jpg",
    ],
)
def test_variantes_de_nome_de_gerador_sao_reconhecidas(nome):
    assert parece_sintetica(nome) is True


@pytest.mark.parametrize(
    "nome",
    [
        "IMG_1398.JPG",
        "Suave (5).jpg",
        "IMG_20250410_145921917 (2).jpg",
        "0E8A738E-FFBD-472D-924B-53DF737D35BD.jpeg",
        "download.jpg",
        "",
    ],
)
def test_nome_de_foto_real_nao_e_confundido_com_gerador(nome):
    assert parece_sintetica(nome) is False


# --------------------------------------------------------------------------- #
# Heuristica de proveniencia
# --------------------------------------------------------------------------- #


def test_exif_de_camera_com_gps_e_real_verificada(tmp_path):
    arquivo = foto_iphone(tmp_path / "IMG_1398.JPG")
    camada = classificar(perfil(arquivo))

    assert camada is Camada.REAL_VERIFICADA
    assert all(pode_usar(camada, uso) for uso in USOS)


def test_alta_resolucao_sem_exif_e_real_nao_verificada(tmp_path):
    """Export do Apple Photos: 12 MP, nome UUID, sem EXIF de camera e sem GPS."""
    arquivo = escrever_jpeg(tmp_path / "0E8A738E-FFBD-472D-924B-53DF737D35BD.jpeg", FOTO)
    camada = classificar(perfil(arquivo))

    assert camada is Camada.REAL_NAO_VERIFICADA
    # Sem prova de origem nao libera nada ate a curadoria humana decidir.
    assert not any(pode_usar(camada, uso) for uso in USOS)


def test_baixa_resolucao_sem_exif_vai_para_quarentena(tmp_path):
    """Lado maior <= 1024 e sem EXIF: passou por canal que recomprime."""
    arquivo = escrever_jpeg(tmp_path / "11 (7).jpeg", (1024, 768))
    assert classificar(perfil(arquivo)) is Camada.QUARENTENA


def test_largura_de_pinterest_sem_exif_e_mood_terceiros(tmp_path):
    retrato = escrever_jpeg(tmp_path / "00d9d539989e12a764b1e9998ee74da0.jpg", PIN)
    assert classificar(perfil(retrato)) is Camada.MOOD_TERCEIROS
    assert 736 in LARGURAS_PINTEREST


def test_assinatura_de_pinterest_ganha_da_regra_de_baixa_resolucao(tmp_path):
    """736x736 cabe nas duas regras. Proveniencia de terceiro pesa mais.

    Mandar para a quarentena perderia a informacao de que existe um dono da
    imagem - e a quarentena nem descritor textual permite.
    """
    quadrada = escrever_jpeg(tmp_path / "download.jpg", (736, 736))
    assert classificar(perfil(quadrada)) is Camada.MOOD_TERCEIROS


def test_meia_prova_de_proveniencia_exige_curadoria_humana(tmp_path):
    """EXIF de camera sem GPS (ou o contrario) nao decide sozinho.

    A fronteira 01/02 e uma fronteira de permissao: 01 libera tudo, 02 nao
    libera nada. Chutar erra caro nas duas direcoes, entao a heuristica recusa.
    """
    sem_gps = escrever_jpeg(tmp_path / "IMG_9999.JPG", FOTO, marca="Apple", modelo="iPhone 7")
    with pytest.raises(ClassificacaoIndefinida, match="falta GPS"):
        classificar(perfil(sem_gps))

    sem_camera = escrever_jpeg(tmp_path / "sem-camera.jpg", FOTO, gps=TORREFACAO_UBERLANDIA)
    with pytest.raises(ClassificacaoIndefinida, match="falta EXIF de camera"):
        classificar(perfil(sem_camera))


def test_resolucao_intermediaria_sem_prova_nenhuma_nao_e_chutada(tmp_path):
    arquivo = escrever_jpeg(tmp_path / "misteriosa.jpg", (1600, 1200))
    with pytest.raises(ClassificacaoIndefinida, match="nenhuma assinatura conhecida"):
        classificar(perfil(arquivo))


# --------------------------------------------------------------------------- #
# Perfil forense
# --------------------------------------------------------------------------- #


def test_perfil_extrai_o_dossie_forense(tmp_path):
    arquivo = foto_iphone(tmp_path / "IMG_1398.JPG", tamanho=(2000, 1500))
    p = perfil(arquivo)

    assert (p.marca, p.modelo) == ("Apple", "iPhone 7")
    assert p.camera == "Apple iPhone 7"
    assert p.data == "2017:03:15 12:04:11"
    assert p.iso == 20
    assert p.abertura == pytest.approx(1.8, abs=0.01)
    assert p.focal_mm == pytest.approx(3.99, abs=0.01)
    assert p.exposicao_s == pytest.approx(1 / 2000, rel=0.02)
    assert p.software == "10.3.1"

    assert (p.largura, p.altura) == (2000, 1500)
    assert p.megapixels == 3.0
    assert p.orientacao == "paisagem"
    assert p.proporcao == pytest.approx(1.33, abs=0.01)
    assert p.lado_maior == 2000

    assert p.lat == pytest.approx(FAZENDA_MEDEIROS[0], abs=1e-4)
    assert p.lon == pytest.approx(FAZENDA_MEDEIROS[1], abs=1e-4)
    # A altitude que provou o terroir: 1.250 m em Medeiros.
    assert p.altitude_m == pytest.approx(1250.0, abs=0.5)

    assert p.tem_exif_de_camera is True
    assert p.tem_gps is True
    assert p.n_tags_exif > 10
    assert p.nitidez > 0
    assert len(p.sha8) == 8
    assert p.kb > 0
    assert p.pasta == tmp_path.name


def test_perfil_sem_exif_nao_inventa_campos(tmp_path):
    p = perfil(escrever_jpeg(tmp_path / "download.jpg", PIN))

    assert p.marca == p.modelo == p.software == p.data == ""
    assert (p.iso, p.abertura, p.focal_mm, p.exposicao_s) == (None, None, None, None)
    assert (p.lat, p.lon, p.altitude_m) == (None, None, None)
    assert p.tem_exif_de_camera is False and p.tem_gps is False
    assert p.n_tags_exif == 0
    assert p.orientacao == "retrato"


def test_perfil_respeita_a_orientacao_do_exif(tmp_path):
    """Orientation=6 significa que a foto e retrato mesmo gravada em paisagem."""
    arquivo = foto_iphone(tmp_path / "IMG_1421.JPG", tamanho=(2000, 1500), orientacao=6)
    p = perfil(arquivo)

    assert p.orientacao_exif == 6
    assert (p.largura, p.altura) == (1500, 2000)
    assert p.orientacao == "retrato"


def test_nitidez_separa_nitido_de_borrado(tmp_path):
    nitida = escrever_jpeg(tmp_path / "nitida.jpg", (900, 700))
    borrada = escrever_jpeg(tmp_path / "borrada.jpg", (900, 700), borrar=6)

    assert perfil(nitida).nitidez > perfil(borrada).nitidez * 2


def test_perfil_recusa_arquivo_que_nao_e_imagem(tmp_path):
    lixo = tmp_path / "anotacoes.txt"
    lixo.write_text("isto nao e uma foto", encoding="utf-8")

    with pytest.raises(ArquivoIlegivel):
        perfil(lixo)


def test_escrever_csv_triagem_gera_planilha_legivel(tmp_path):
    foto_iphone(tmp_path / "base" / "IMG_1398.JPG", tamanho=(1200, 900))
    escrever_jpeg(tmp_path / "base" / "download.jpg", PIN)

    destino = escrever_csv_triagem(perfis(tmp_path / "base"), tmp_path / "triagem.csv")
    linhas = {l["arquivo"]: l for l in csv.DictReader(destino.open(encoding="utf-8"))}

    assert set(linhas) == {"IMG_1398.JPG", "download.jpg"}
    assert linhas["IMG_1398.JPG"]["modelo"] == "iPhone 7"
    assert linhas["IMG_1398.JPG"]["alt_m"] == "1250"
    assert linhas["IMG_1398.JPG"]["iso"] == "20"
    assert linhas["download.jpg"]["modelo"] == "" and linhas["download.jpg"]["lat"] == ""


# --------------------------------------------------------------------------- #
# Agrupamento por GPS (porte de gps.py)
# --------------------------------------------------------------------------- #


def test_agrupar_por_gps_separa_locais_e_guarda_a_altitude(tmp_path):
    """Foi este agrupamento que provou os 1.250 m da fazenda."""
    foto_iphone(tmp_path / "IMG_1398.JPG", tamanho=(1200, 900))
    foto_iphone(tmp_path / "IMG_1399.JPG", tamanho=(1200, 900), seed=9)
    escrever_jpeg(
        tmp_path / "Canela.jpg", (1200, 900),
        marca="motorola", modelo="motorola edge 50 fusion",
        gps=TORREFACAO_UBERLANDIA, altitude_m=875.0,
    )
    escrever_jpeg(tmp_path / "download.jpg", PIN)

    grupos = agrupar_por_gps(perfis(tmp_path))

    assert len(grupos) == 3
    fazenda, torrefacao, sem_gps = grupos
    assert len(fazenda.arquivos) == 2
    assert fazenda.altitudes_m == (1250.0,)
    assert fazenda.lat == pytest.approx(FAZENDA_MEDEIROS[0], abs=1e-3)
    assert "maps?q=" in fazenda.maps_url
    assert torrefacao.altitudes_m == (875.0,)
    # O balde sem GPS vem por ultimo e nao finge ter coordenada.
    assert sem_gps.sem_gps is True and sem_gps.lat is None and sem_gps.maps_url == ""
    assert [f.name for f in sem_gps.arquivos] == ["download.jpg"]


# --------------------------------------------------------------------------- #
# Mapa explicito da base real
# --------------------------------------------------------------------------- #


def test_mapa_base_curada_reproduz_a_triagem_dos_66_arquivos():
    contagem = {camada: 0 for camada in Camada}
    for entrada in MAPA_BASE_CURADA:
        contagem[entrada.camada] += 1

    assert len(MAPA_BASE_CURADA) == 66
    assert contagem == {
        Camada.REAL_VERIFICADA: 38,
        Camada.REAL_NAO_VERIFICADA: 6,
        Camada.MOOD_TERCEIROS: 16,
        Camada.QUARENTENA: 6,
    }
    validar_mapa()


def test_os_dois_gemini_do_mapa_estao_na_quarentena():
    sinteticas = [e for e in MAPA_BASE_CURADA if parece_sintetica(e.arquivo)]

    assert len(sinteticas) == 2
    assert {e.pasta for e in sinteticas} == {"Produto Canela 250", "Produto Classico 250"}
    for entrada in sinteticas:
        assert entrada.camada is Camada.QUARENTENA
        assert pode_usar(entrada.camada, "fonte_style_dna") is False


def test_mapa_nao_tem_origem_repetida_nem_colisao_de_destino():
    origens = [e.origem for e in MAPA_BASE_CURADA]
    alvos = [e.alvo for e in MAPA_BASE_CURADA]

    assert len(set(origens)) == len(origens)
    assert len(set(alvos)) == len(alvos)
    # 'Classico (5).jpg' existe em duas pastas com conteudo diferente.
    assert origens.count("Produto Classico 250/Classico (5).jpg") == 1
    assert origens.count("Produto Suave 250/Classico (5).jpg") == 1


def test_validar_mapa_recusa_origem_duplicada():
    mapa = (
        EntradaMapa("Fazenda e Serra", "IMG_1.JPG", "01-real-verificada/a"),
        EntradaMapa("Fazenda e Serra", "IMG_1.JPG", "02-real-nao-verificada/b"),
    )
    with pytest.raises(SeparacaoInvalida, match="mapeado duas vezes"):
        validar_mapa(mapa)


def test_validar_mapa_recusa_colisao_de_destino():
    mapa = (
        EntradaMapa("pasta-a", "foto.jpg", "01-real-verificada/x"),
        EntradaMapa("pasta-b", "foto.jpg", "01-real-verificada/x"),
    )
    with pytest.raises(SeparacaoInvalida, match="colisao de destino"):
        validar_mapa(mapa)


# --------------------------------------------------------------------------- #
# REGRA 4: a separacao tem de ser exaustiva
# --------------------------------------------------------------------------- #


def _base_miniatura(raiz: Path) -> tuple[Path, ...]:
    """Uma base de 3 arquivos com as assinaturas das camadas 01, 03 e 04."""
    return (
        foto_iphone(raiz / "Fazenda e Serra" / "IMG_1398.JPG", tamanho=(1200, 900)),
        escrever_jpeg(raiz / "Fotos-Aestethic" / "download.jpg", PIN),
        escrever_jpeg(
            raiz / "Produto Canela 250" / "Gemini_Generated_Image_hhlj5jhhlj5jhhlj.jpg",
            (1200, 900),
        ),
    )


_MAPA_MINIATURA = (
    EntradaMapa("Fazenda e Serra", "IMG_1398.JPG",
                "01-real-verificada/fazenda-medeiros-1250m/cafezal"),
    EntradaMapa("Fotos-Aestethic", "download.jpg",
                "03-mood-terceiros/mesa-mineira-e-brewing"),
    EntradaMapa("Produto Canela 250", "Gemini_Generated_Image_hhlj5jhhlj5jhhlj.jpg",
                "04-quarentena/sintetica-gemini"),
)


def test_separacao_falha_se_algum_arquivo_ficar_sem_classificacao(tmp_path):
    """REGRA 4: exaustividade. O arquivo que ninguem classificou e o que ninguem olhou."""
    origem, destino = tmp_path / "imagens", tmp_path / "base-curada"
    _base_miniatura(origem)
    escrever_jpeg(origem / "Fazenda e Serra" / "IMG_1500.JPG", (1200, 900))  # ninguem mapeou

    with pytest.raises(ClassificacaoIncompleta) as erro:
        separar(origem, destino, mapa=_MAPA_MINIATURA)

    assert "Fazenda e Serra/IMG_1500.JPG" in str(erro.value)
    assert erro.value.pendencias == {
        "Fazenda e Serra/IMG_1500.JPG": "nenhuma entrada no mapa de curadoria"
    }
    # A verificacao roda ANTES de copiar: nao fica base curada pela metade.
    assert not destino.exists()


def test_verificar_exaustividade_passa_quando_o_mapa_cobre_a_base(tmp_path):
    origem = tmp_path / "imagens"
    _base_miniatura(origem)

    verificar_exaustividade(origem, _MAPA_MINIATURA)  # nao levanta


def test_verificar_exaustividade_pega_ate_arquivo_que_nao_e_imagem(tmp_path):
    origem = tmp_path / "imagens"
    _base_miniatura(origem)
    (origem / "Fazenda e Serra" / "LEIA-ME.txt").write_text("nota solta", encoding="utf-8")

    with pytest.raises(ClassificacaoIncompleta, match="LEIA-ME.txt"):
        verificar_exaustividade(origem, _MAPA_MINIATURA)


def test_classificar_diretorio_falha_quando_a_heuristica_nao_decide(tmp_path):
    origem = tmp_path / "imagens"
    _base_miniatura(origem)
    escrever_jpeg(origem / "Fazenda e Serra" / "duvidosa.jpg", (1600, 1200))
    (origem / "Fazenda e Serra" / "notas.txt").write_text("x", encoding="utf-8")

    with pytest.raises(ClassificacaoIncompleta) as erro:
        classificar_diretorio(origem)

    assert set(erro.value.pendencias) == {
        "Fazenda e Serra/duvidosa.jpg",
        "Fazenda e Serra/notas.txt",
    }


def test_classificar_diretorio_reproduz_as_camadas_e_filtra_por_uso(tmp_path):
    origem = tmp_path / "imagens"
    verificada, mood, sintetica = _base_miniatura(origem)
    nao_verificada = escrever_jpeg(
        origem / "Fazenda e Serra" / "0E8A738E-FFBD-472D-924B-53DF737D35BD.jpeg", FOTO
    )

    classificacoes = classificar_diretorio(origem)

    assert classificacoes == {
        verificada: Camada.REAL_VERIFICADA,
        nao_verificada: Camada.REAL_NAO_VERIFICADA,
        mood: Camada.MOOD_TERCEIROS,
        sintetica: Camada.QUARENTENA,
    }
    # Nenhum uso de pixel alcanca mood ou quarentena.
    for uso in USOS:
        assert filtrar_por_uso(classificacoes, uso) == [verificada]


def test_classificar_diretorio_usa_o_mapa_antes_da_heuristica(tmp_path):
    """Curadoria humana no mapa vence a heuristica, que so decide material novo."""
    origem = tmp_path / "imagens"
    _base_miniatura(origem)
    mapa = (
        EntradaMapa("Fazenda e Serra", "IMG_1398.JPG", "02-real-nao-verificada/revisar"),
    )

    classificacoes = classificar_diretorio(origem, mapa=mapa)

    assert classificacoes[origem / "Fazenda e Serra" / "IMG_1398.JPG"] is Camada.REAL_NAO_VERIFICADA


# --------------------------------------------------------------------------- #
# Separacao
# --------------------------------------------------------------------------- #


def test_separar_copia_para_as_camadas_e_grava_manifesto(tmp_path):
    origem, destino = tmp_path / "imagens", tmp_path / "base-curada"
    originais = _base_miniatura(origem)

    resultado = separar(origem, destino, mapa=_MAPA_MINIATURA)

    assert resultado.total == 3
    assert resultado.por_camada == {
        Camada.REAL_VERIFICADA: 1,
        Camada.REAL_NAO_VERIFICADA: 0,
        Camada.MOOD_TERCEIROS: 1,
        Camada.QUARENTENA: 1,
    }
    copiado = destino / "01-real-verificada" / "fazenda-medeiros-1250m" / "cafezal" / "IMG_1398.JPG"
    assert copiado.is_file()
    # Copia, nunca move: /imagens continua sendo a fonte da verdade intocada.
    assert all(f.is_file() for f in originais)
    # O nome original viaja junto, senao perde-se o rastro da origem.
    assert (destino / "04-quarentena" / "sintetica-gemini"
            / "Gemini_Generated_Image_hhlj5jhhlj5jhhlj.jpg").is_file()

    linhas = list(csv.DictReader(resultado.manifesto.open(encoding="utf-8")))
    assert len(linhas) == 3
    assert linhas[0] == {
        "origem": "Fazenda e Serra/IMG_1398.JPG",
        "destino": "01-real-verificada/fazenda-medeiros-1250m/cafezal/IMG_1398.JPG",
        "camada": "01-real-verificada",
    }
    # Toda camada gravada no manifesto tem permissao declarada.
    for linha in linhas:
        assert Camada(linha["camada"]) in PERMISSOES


def test_separar_recusa_arquivo_mapeado_que_nao_existe_no_disco(tmp_path):
    origem, destino = tmp_path / "imagens", tmp_path / "base-curada"
    _base_miniatura(origem)
    mapa = _MAPA_MINIATURA + (
        EntradaMapa("Fazenda e Serra", "IMG_1397 (2).JPG", "01-real-verificada/cafezal"),
    )

    with pytest.raises(SeparacaoInvalida, match=r"IMG_1397 \(2\).JPG"):
        separar(origem, destino, mapa=mapa)
    assert not destino.exists()


def test_separar_recusa_destino_ja_populado(tmp_path):
    origem, destino = tmp_path / "imagens", tmp_path / "base-curada"
    _base_miniatura(origem)
    (destino / "01-real-verificada").mkdir(parents=True)
    (destino / "manifest.csv").write_text("origem,destino,camada\n", encoding="utf-8")

    with pytest.raises(SeparacaoInvalida, match="ja existe"):
        separar(origem, destino, mapa=_MAPA_MINIATURA)


def test_arquivos_da_base_nao_filtra_por_extensao(tmp_path):
    """Filtrar por extensao esconderia o arquivo estranho da verificacao."""
    _base_miniatura(tmp_path)
    (tmp_path / "Fazenda e Serra" / "notas.txt").write_text("x", encoding="utf-8")

    nomes = {f.name for f in arquivos_da_base(tmp_path)}
    assert "notas.txt" in nomes and len(nomes) == 4
