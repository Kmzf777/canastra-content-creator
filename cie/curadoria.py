"""Triagem forense da base e separacao por CAMADA DE PERMISSAO DE USO.

Portado dos scripts descartaveis `_ref-scripts/triagem.py` (perfil forense por
arquivo), `_ref-scripts/gps.py` (agrupamento por coordenada, que provou os
1.250 m de Medeiros) e `_ref-scripts/separar.py` (mapeamento explicito em quatro
camadas com auto-verificacao). Aquilo rodou uma vez e nao podia ser repetido;
aqui vira modulo versionado e testado.

A base nao e organizada por assunto e sim pelo que e PERMITIDO fazer com cada
arquivo. As tres regras de CLAUDE.md ("Camadas de permissao da base de imagens")
sao aqui codigo, nao convencao:

  1. `03-mood-terceiros` NUNCA vira pixel: uma imagem tem marca d'agua e outra
     tem rosto identificavel de quem nao autorizou. Servem para descrever
     estetica em texto, nao para virar referencia de imagem nem recorte.
  2. `04-quarentena` nao serve para uso nenhum, em hipotese alguma.
  3. Arquivo de gerador (`Gemini_Generated_Image_*`) e sintetico e cai na
     quarentena mesmo estando guardado na pasta de produto. Se entrar na
     destilacao de estilo, o motor aprende o look sintetico que o projeto
     existe para evitar.

E a separacao e EXAUSTIVA: `verificar_exaustividade` falha duro quando algum
arquivo da base fica sem classificacao, propriedade herdada do script original.
Silencio aqui e o modo de falha caro: o arquivo nao classificado e exatamente o
que ninguem olhou.
"""

from __future__ import annotations

import csv
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass, fields
from enum import StrEnum
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from PIL import Image, ImageFilter, ImageOps, ImageStat

from .errors import CieError

# `_dms_to_degrees` e a mesma conversao DMS -> graus decimais que a triagem
# original fazia a mao; reaproveitada para nao existirem duas formulas de GPS.
from .imaging import _dms_to_degrees, register_optional_decoders, sha256_file

# --------------------------------------------------------------------------- #
# Erros
# --------------------------------------------------------------------------- #


class ArquivoIlegivel(CieError):
    """O arquivo nao abriu como imagem (nao ha decoder, ou nao e imagem)."""


class ClassificacaoIndefinida(CieError):
    """A heuristica nao reconheceu a assinatura de proveniencia do arquivo.

    Nao e bug: e recusa deliberada. Chutar entre `01-real-verificada` (libera
    tudo) e o resto (libera nada) e caro nas duas direcoes, entao a curadoria
    humana decide e o arquivo aparece na lista de pendencias.
    """

    def __init__(self, nome: str, motivo: str) -> None:
        self.nome = nome
        self.motivo = motivo
        super().__init__(f"{nome}: {motivo}")


class ClassificacaoIncompleta(CieError):
    """Sobrou arquivo sem camada. A separacao so vale se cobrir a base inteira."""

    def __init__(self, pendencias: Mapping[str, str]) -> None:
        self.pendencias = dict(pendencias)
        corpo = "\n".join(f"    {k}: {v}" for k, v in sorted(self.pendencias.items()))
        super().__init__(
            f"{len(self.pendencias)} arquivo(s) da base sem classificacao:\n{corpo}"
        )


class SeparacaoInvalida(CieError):
    """O mapa explicito e o disco discordam: duplicata, colisao ou arquivo ausente."""


# --------------------------------------------------------------------------- #
# Camadas e permissoes
# --------------------------------------------------------------------------- #


class Camada(StrEnum):
    """As quatro camadas de permissao. O valor e o nome da pasta em `base-curada/`."""

    #: EXIF de camera **e** GPS. Origem provada. Libera todos os usos.
    REAL_VERIFICADA = "01-real-verificada"
    #: Provavelmente nossa, sem prova de origem. Nao libera nada ate curadoria.
    REAL_NAO_VERIFICADA = "02-real-nao-verificada"
    #: Scrape de terceiros. So descritor textual - nunca pixel.
    MOOD_TERCEIROS = "03-mood-terceiros"
    #: Sintetica ou resolucao insuficiente. Nao serve para nada.
    QUARENTENA = "04-quarentena"


@dataclass(frozen=True)
class Permissoes:
    """O que se pode fazer com um arquivo da camada.

    `fonte_style_dna` significa entregar o PIXEL para a destilacao de estilo.
    `03-mood-terceiros` pode ser descrito em texto (ver
    `pode_descrever_em_texto`), o que e outra coisa: descritor nao e fonte.
    """

    #: Enviar como guidance/referencia para a API de imagem.
    referencia_de_imagem: bool
    #: Alimentar a destilacao de estilo com o pixel.
    fonte_style_dna: bool
    #: Recortar o objeto para composicao local.
    recorte: bool


#: Os usos que `pode_usar` conhece. Derivado da dataclass para nao dessincronizar.
USOS: tuple[str, ...] = tuple(campo.name for campo in fields(Permissoes))


#: A tabela de CLAUDE.md, secao "Camadas de permissao da base de imagens".
PERMISSOES: dict[Camada, Permissoes] = {
    Camada.REAL_VERIFICADA: Permissoes(
        referencia_de_imagem=True, fonte_style_dna=True, recorte=True
    ),
    Camada.REAL_NAO_VERIFICADA: Permissoes(
        referencia_de_imagem=False, fonte_style_dna=False, recorte=False
    ),
    # Marca d'agua e rosto de quem nao autorizou. Nunca vira pixel.
    Camada.MOOD_TERCEIROS: Permissoes(
        referencia_de_imagem=False, fonte_style_dna=False, recorte=False
    ),
    # Sintetica ou baixa resolucao. Nenhum uso, nunca.
    Camada.QUARENTENA: Permissoes(
        referencia_de_imagem=False, fonte_style_dna=False, recorte=False
    ),
}


def permissoes(camada: Camada | str) -> Permissoes:
    return PERMISSOES[Camada(camada)]


def pode_usar(camada: Camada | str, uso: str) -> bool:
    """Porteiro unico da base. Uso desconhecido levanta erro - nunca libera."""
    if uso not in USOS:
        raise ValueError(f"uso desconhecido: {uso!r}; conhecidos: {', '.join(USOS)}")
    return getattr(permissoes(camada), uso)


def pode_descrever_em_texto(camada: Camada | str) -> bool:
    """Mood de terceiros pode virar descritor textual; quarentena, nem isso."""
    return Camada(camada) is not Camada.QUARENTENA


def filtrar_por_uso(classificacoes: Mapping[Path, Camada], uso: str) -> list[Path]:
    """Filtra um mapa arquivo -> camada pelo que aquele uso permite."""
    return sorted(caminho for caminho, camada in classificacoes.items() if pode_usar(camada, uso))


# --------------------------------------------------------------------------- #
# Perfil forense (porte de _ref-scripts/triagem.py)
# --------------------------------------------------------------------------- #

_TAG_MARCA = 0x010F
_TAG_MODELO = 0x0110
_TAG_ORIENTACAO = 0x0112
_TAG_SOFTWARE = 0x0131
_TAG_DATA = 0x0132
_IFD_EXIF = 0x8769
_IFD_GPS = 0x8825
_TAG_EXPOSICAO = 0x829A
_TAG_ABERTURA = 0x829D
_TAG_ISO = 0x8827
_TAG_DATA_ORIGINAL = 0x9003
_TAG_FOCAL = 0x920A
_GPS_LAT_REF, _GPS_LAT = 1, 2
_GPS_LON_REF, _GPS_LON = 3, 4
_GPS_ALT_REF, _GPS_ALT = 5, 6

#: Kernel Laplaciano 3x3; offset=128 preserva a parte negativa da resposta.
_LAPLACIANO = ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], scale=1, offset=128)


def nitidez(imagem: Image.Image) -> float:
    """Desvio padrao do Laplaciano, normalizado em 1024 px (sem numpy).

    Reamostra antes de medir para que o numero nao dependa da resolucao do
    arquivo - senao um recorte grande "e mais nitido" so por ser grande.
    """
    pequena = ImageOps.contain(imagem.convert("L"), (1024, 1024))
    return round(ImageStat.Stat(pequena.filter(_LAPLACIANO)).stddev[0], 2)


@dataclass(frozen=True)
class PerfilArquivo:
    """Perfil forense de um arquivo: o que o proprio arquivo conta sobre si."""

    caminho: Path
    pasta: str
    nome: str
    sha8: str
    kb: int
    largura: int
    altura: int
    nitidez: float
    n_tags_exif: int
    marca: str = ""
    modelo: str = ""
    software: str = ""
    data: str = ""
    iso: int | None = None
    abertura: float | None = None
    focal_mm: float | None = None
    exposicao_s: float | None = None
    orientacao_exif: int | None = None
    lat: float | None = None
    lon: float | None = None
    altitude_m: float | None = None

    @property
    def megapixels(self) -> float:
        return round(self.largura * self.altura / 1e6, 1)

    @property
    def lado_maior(self) -> int:
        return max(self.largura, self.altura)

    @property
    def proporcao(self) -> float:
        return round(self.largura / self.altura, 2) if self.altura else 0.0

    @property
    def orientacao(self) -> str:
        if self.altura > self.largura:
            return "retrato"
        return "quadrado" if self.altura == self.largura else "paisagem"

    @property
    def camera(self) -> str:
        return " ".join(parte for parte in (self.marca, self.modelo) if parte)

    @property
    def tem_exif_de_camera(self) -> bool:
        """Marca E modelo. Marca sozinha aparece em arquivo reprocessado."""
        return bool(self.marca and self.modelo)

    @property
    def tem_gps(self) -> bool:
        return self.lat is not None and self.lon is not None


def _ifds(imagem: Image.Image) -> tuple[dict, dict, dict]:
    """(IFD base, IFD Exif, IFD GPS) com chaves numericas cruas."""
    try:
        base = imagem.getexif()
    except Exception:  # noqa: BLE001 - EXIF corrompido nao pode derrubar a triagem
        return {}, {}, {}
    if not base:
        return {}, {}, {}
    sub: list[dict] = []
    for ifd_id in (_IFD_EXIF, _IFD_GPS):
        try:
            sub.append(dict(base.get_ifd(ifd_id)))
        except Exception:  # noqa: BLE001
            sub.append({})
    return dict(base), sub[0], sub[1]


def _texto(valor) -> str:
    return str(valor).strip() if valor not in (None, "") else ""


def _decimal(valor) -> float | None:
    if isinstance(valor, (tuple, list)):
        valor = valor[0] if valor else None
    try:
        return float(valor)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _inteiro(valor) -> int | None:
    numero = _decimal(valor)
    return int(numero) if numero is not None else None


def _altitude(gps: Mapping) -> float | None:
    metros = _decimal(gps.get(_GPS_ALT))
    if metros is None:
        return None
    ref = gps.get(_GPS_ALT_REF)
    if isinstance(ref, bytes):
        ref = ref[0] if ref else 0
    # ref == 1 significa abaixo do nivel do mar.
    return -metros if _inteiro(ref) == 1 else metros


def perfil(path: Path | str) -> PerfilArquivo:
    """Le um arquivo e devolve seu perfil forense. Nao decide nada."""
    caminho = Path(path)
    register_optional_decoders()
    try:
        with Image.open(caminho) as bruta:
            base, exif_ifd, gps = _ifds(bruta)
            corrigida = ImageOps.exif_transpose(bruta)
            largura, altura = corrigida.size
            nitida = nitidez(corrigida)
    except Exception as exc:  # noqa: BLE001 - vira erro do dominio, com o caminho
        raise ArquivoIlegivel(f"{caminho}: nao abriu como imagem ({exc})") from exc

    return PerfilArquivo(
        caminho=caminho,
        pasta=caminho.parent.name,
        nome=caminho.name,
        sha8=sha256_file(caminho)[:8],
        kb=round(caminho.stat().st_size / 1024),
        largura=largura,
        altura=altura,
        nitidez=nitida,
        # Conta as tres IFDs somadas (a base inclui os ponteiros ExifOffset/GPSInfo).
        n_tags_exif=len(base) + len(exif_ifd) + len(gps),
        marca=_texto(base.get(_TAG_MARCA)),
        modelo=_texto(base.get(_TAG_MODELO)),
        software=_texto(base.get(_TAG_SOFTWARE)),
        data=_texto(exif_ifd.get(_TAG_DATA_ORIGINAL) or base.get(_TAG_DATA)),
        iso=_inteiro(exif_ifd.get(_TAG_ISO)),
        abertura=_decimal(exif_ifd.get(_TAG_ABERTURA)),
        focal_mm=_decimal(exif_ifd.get(_TAG_FOCAL)),
        exposicao_s=_decimal(exif_ifd.get(_TAG_EXPOSICAO)),
        orientacao_exif=_inteiro(base.get(_TAG_ORIENTACAO)),
        lat=_dms_to_degrees(gps.get(_GPS_LAT), gps.get(_GPS_LAT_REF)),
        lon=_dms_to_degrees(gps.get(_GPS_LON), gps.get(_GPS_LON_REF)),
        altitude_m=_altitude(gps),
    )


def perfis(raiz: Path | str) -> list[PerfilArquivo]:
    """Perfil de todo arquivo sob `raiz`, em ordem estavel."""
    return [perfil(f) for f in arquivos_da_base(raiz)]


#: Colunas do CSV de triagem, na ordem em que o script original as escrevia.
COLUNAS_TRIAGEM: tuple[str, ...] = (
    "pasta", "arquivo", "sha8", "w", "h", "mp", "orient", "ar", "kb",
    "marca", "modelo", "data", "iso", "f", "focal_mm", "exp_s", "soft",
    "lat", "lon", "alt_m", "nitidez", "n_exif",
)


def escrever_csv_triagem(lista: Iterable[PerfilArquivo], destino: Path | str) -> Path:
    """Grava a planilha de triagem - a evidencia que se le fora do Python."""
    caminho = Path(destino)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", newline="", encoding="utf-8") as fh:
        escritor = csv.DictWriter(fh, fieldnames=list(COLUNAS_TRIAGEM))
        escritor.writeheader()
        for p in lista:
            escritor.writerow(
                {
                    "pasta": p.pasta, "arquivo": p.nome, "sha8": p.sha8,
                    "w": p.largura, "h": p.altura, "mp": p.megapixels,
                    "orient": p.orientacao, "ar": p.proporcao, "kb": p.kb,
                    "marca": p.marca, "modelo": p.modelo, "data": p.data,
                    "iso": p.iso if p.iso is not None else "",
                    "f": p.abertura if p.abertura is not None else "",
                    "focal_mm": p.focal_mm if p.focal_mm is not None else "",
                    "exp_s": p.exposicao_s if p.exposicao_s is not None else "",
                    "soft": p.software,
                    "lat": f"{p.lat:.5f}" if p.lat is not None else "",
                    "lon": f"{p.lon:.5f}" if p.lon is not None else "",
                    "alt_m": f"{p.altitude_m:.0f}" if p.altitude_m is not None else "",
                    "nitidez": p.nitidez, "n_exif": p.n_tags_exif,
                }
            )
    return caminho


# --------------------------------------------------------------------------- #
# Agrupamento por coordenada (porte de _ref-scripts/gps.py)
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class GrupoGps:
    """Um local fisico da base. Foi assim que os 1.250 m de Medeiros apareceram."""

    lat: float | None
    lon: float | None
    altitudes_m: tuple[float, ...]
    arquivos: tuple[Path, ...]

    @property
    def sem_gps(self) -> bool:
        return self.lat is None or self.lon is None

    @property
    def maps_url(self) -> str:
        if self.sem_gps:
            return ""
        return f"https://www.google.com/maps?q={self.lat},{self.lon}"


def agrupar_por_gps(lista: Iterable[PerfilArquivo], *, casas: int = 3) -> list[GrupoGps]:
    """Agrupa por coordenada arredondada. 3 casas ~ 100 m: um local, nao um passo."""
    baldes: dict[tuple[float, float] | None, list[PerfilArquivo]] = defaultdict(list)
    for p in lista:
        chave = (round(p.lat, casas), round(p.lon, casas)) if p.tem_gps else None
        baldes[chave].append(p)

    grupos = [
        GrupoGps(
            lat=None if chave is None else chave[0],
            lon=None if chave is None else chave[1],
            altitudes_m=tuple(
                sorted({float(round(p.altitude_m)) for p in itens if p.altitude_m is not None})
            ),
            arquivos=tuple(p.caminho for p in itens),
        )
        for chave, itens in baldes.items()
    ]
    # Sem GPS por ultimo; entre os demais, o local mais fotografado primeiro.
    grupos.sort(key=lambda g: (g.sem_gps, -len(g.arquivos), g.lat or 0.0))
    return grupos


# --------------------------------------------------------------------------- #
# Classificacao heuristica
# --------------------------------------------------------------------------- #

#: Marcas de gerador que aparecem no nome do arquivo (ou no campo Software).
_MARCAS_GERADOR = (
    r"gemini|chatgpt|dall[\-_ ]?e|midjourney|firefly|imagen|grok|ideogram|leonardo"
    r"|stable[\-_ ]?diffusion|nano[\-_ ]?banana|bing[\-_ ]?image|copilot"
)
_RE_GERADOR = re.compile(rf"^({_MARCAS_GERADOR})[\-_ ]", re.IGNORECASE)
_RE_GERADA = re.compile(r"[\-_ ]?generated[\-_ ]?(image|img)", re.IGNORECASE)

#: >= 8 MP: resolucao de camera de celular atual, nao de download de web.
MP_ALTA_RESOLUCAO = 8.0
#: Lado maior <= 1024 sem EXIF: passou por canal que recomprime (WhatsApp, web).
LADO_MAXIMO_RECOMPRIMIDO = 1024
#: Larguras servidas pelo CDN do Pinterest. 736 e a assinatura da nossa camada 03.
LARGURAS_PINTEREST = frozenset({736, 564, 474})


def parece_sintetica(nome: str) -> bool:
    """`Gemini_Generated_Image_*.jpg` e parentes.

    Falso positivo aqui custa uma foto real fora da base; falso negativo
    contamina a destilacao de estilo com o look que o projeto existe para
    evitar. O vies e deliberado.
    """
    haste = Path(nome or "").stem
    return bool(_RE_GERADOR.match(haste) or _RE_GERADA.search(haste))


def classificar(perfil_arquivo: PerfilArquivo, nome_arquivo: str | None = None) -> Camada:
    """Camada de permissao a partir da proveniencia. Recusa quando nao sabe.

    Ordem das regras (derivada da triagem real dos 66 arquivos):

      1. nome/software de gerador          -> QUARENTENA (antes de tudo);
      2. EXIF de camera **e** GPS          -> REAL_VERIFICADA;
      3. meia prova (so um dos dois)       -> recusa, curadoria humana decide;
      4. sem prova + largura de Pinterest  -> MOOD_TERCEIROS;
      5. sem prova + lado maior <= 1024    -> QUARENTENA (canal que recomprime);
      6. sem prova + >= 8 MP               -> REAL_NAO_VERIFICADA.

    O passo 1 vem primeiro de proposito: dois `Gemini_Generated_Image_*.jpg`
    estavam misturados nas pastas de produto, com resolucao alta o bastante
    para passarem por foto nossa no passo 6.
    """
    nome = nome_arquivo or perfil_arquivo.nome

    if parece_sintetica(nome) or parece_sintetica(perfil_arquivo.software):
        return Camada.QUARENTENA

    if perfil_arquivo.tem_exif_de_camera and perfil_arquivo.tem_gps:
        return Camada.REAL_VERIFICADA

    if perfil_arquivo.tem_exif_de_camera or perfil_arquivo.tem_gps:
        # A fronteira 01/02 e uma fronteira de permissao: 01 libera tudo, 02 nao
        # libera nada. Com meia prova, chutar erra caro nos dois sentidos.
        falta = "GPS" if perfil_arquivo.tem_exif_de_camera else "EXIF de camera"
        raise ClassificacaoIndefinida(
            nome, f"proveniencia parcial (falta {falta}); curadoria humana decide"
        )

    if perfil_arquivo.largura in LARGURAS_PINTEREST:
        return Camada.MOOD_TERCEIROS

    if perfil_arquivo.lado_maior <= LADO_MAXIMO_RECOMPRIMIDO:
        return Camada.QUARENTENA

    if perfil_arquivo.megapixels >= MP_ALTA_RESOLUCAO:
        return Camada.REAL_NAO_VERIFICADA

    raise ClassificacaoIndefinida(
        nome,
        f"sem EXIF, sem GPS, {perfil_arquivo.largura}x{perfil_arquivo.altura} "
        f"({perfil_arquivo.megapixels} MP) nao bate com nenhuma assinatura conhecida",
    )


# --------------------------------------------------------------------------- #
# Mapa explicito da base (porte de _ref-scripts/separar.py)
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class EntradaMapa:
    """Uma linha do mapeamento explicito: arquivo de origem -> pasta de destino."""

    pasta: str
    arquivo: str
    #: Caminho relativo de destino, sempre comecando pelo valor da camada.
    destino: str

    @property
    def chave(self) -> tuple[str, str]:
        return (self.pasta, self.arquivo)

    @property
    def camada(self) -> Camada:
        return Camada(self.destino.split("/")[0])

    @property
    def origem(self) -> str:
        return f"{self.pasta}/{self.arquivo}"

    @property
    def alvo(self) -> str:
        return f"{self.destino}/{self.arquivo}"


_FZ = "Fazenda e Serra"
_AE = "Fotos-Aestethic"
_PCA, _PCL, _PSU = "Produto Canela 250", "Produto Classico 250", "Produto Suave 250"

_MAPA: list[EntradaMapa] = []


def _add(pasta: str, nomes: Sequence[str], destino: str) -> None:
    _MAPA.extend(EntradaMapa(pasta, nome, destino) for nome in nomes)


# ------------------------------------------------------------------ camada 01
# iPhone 7, Medeiros, ~1250 m, ISO 20, mar/2017. EXIF de camera + GPS.
_add(
    _FZ,
    [f"IMG_{n}.JPG" for n in (1398, 1399, 1400, 1401, 1406, 1407, 1408, 1409,
                              1410, 1411, 1413, 1414, 1415, 1416, 1417, 1418,
                              1419, 1420, 1405)] + ["IMG_1397 (2).JPG"],
    "01-real-verificada/fazenda-medeiros-1250m/cafezal",
)
_add(_FZ, ["IMG_1421.JPG", "IMG_1422.JPG"],
     "01-real-verificada/fazenda-medeiros-1250m/cafeeiro-com-mao")
_add(_FZ, ["IMG_1423.JPG"],
     "01-real-verificada/fazenda-medeiros-1250m/folhagem")
_add(_FZ, ["IMG_1424.JPG", "IMG_1425.JPG", "IMG_1426.JPG"],
     "01-real-verificada/fazenda-medeiros-1250m/cereja-verde")

# motorola edge 50 fusion, Uberlandia, ~875 m, abr/2025. EXIF de camera + GPS.
_add(_PCA, ["Canela (1).jpg", "Canela.jpg", "IMG_20250410_145921917 (2).jpg",
            "IMG_20250410_145923008 (1).jpg"],
     "01-real-verificada/torrefacao-uberlandia-875m/packshot-canela")
_add(_PCL, ["Classico (5).jpg", "Classico (6).jpg", "Classico (7).jpg",
            "IMG_20250410_145812128_HDR.jpg"],
     "01-real-verificada/torrefacao-uberlandia-875m/packshot-classico")
_add(_PSU, ["Classico (5).jpg", "Suave (3).jpg", "Suave (4).jpg", "Suave (5).jpg"],
     "01-real-verificada/torrefacao-uberlandia-875m/packshot-suave")

# ------------------------------------------------------------------ camada 02
# Full-res (12 MP), nomes UUID de export do Apple Photos, sem EXIF de camera e
# sem GPS. Quase certamente proprias, mas sem prova. Curadoria humana decide.
_add(_FZ, ["0E8A738E-FFBD-472D-924B-53DF737D35BD.jpeg",
           "271122AB-A105-4FC0-801E-EB8247F320E4.jpeg",
           "37B15670-5825-4C3B-82E6-61DA0D1239DB.jpeg",
           "4C4CC82F-D448-4B3A-9E6A-728320096A49 (2).jpeg",
           "5D9EC84E-5B0F-4E00-9FED-58A1FC78EF47.jpeg",
           "D68DECC0-4916-45BD-B627-5E5FD93073CA.jpeg"],
     "02-real-nao-verificada/serra-canastra")

# ------------------------------------------------------------------ camada 03
# Terceiros: dimensoes de Pinterest (736 px), sem EXIF, uma com marca d'agua
# visivel (@thamylis.pine...) e uma com rosto identificavel de quem nao
# autorizou. Somente leitura para descritor textual.
_add(_AE, ["00d9d539989e12a764b1e9998ee74da0.jpg", "122215be4b3c7a6a95de77962969f688.jpg",
           "2666ce48d5f6552bdae3b211f65cb587.jpg", "2fac517826899f266fe1dcff5e6d59be.jpg",
           "31814e784172da60bb5214c403619072.jpg", "3a717292d88e2436e2c8b62828bd5bd4.jpg",
           "511458a16aa74880831ad565c377f667.jpg", "583a78492e5ab9d9c840711722b16da2.jpg",
           "7c715d1a0c511c9cb87d5d91f3d430f3.jpg", "859ca6a2d27ba3d05f30f347b5e33352.jpg",
           "8d1188abc715af42f0a2b3992be3dba8.jpg", "a98e0184b13b7c06f4bcc1a5bfd06d7c.jpg",
           "ac037dd498198a8ed0b1313ba986febb.jpg", "c1ae95ec780502b333f82161f616aebf.jpg",
           "d68749b60fe167bc293b40a45fbf405c.jpg", "download.jpg"],
     "03-mood-terceiros/mesa-mineira-e-brewing")

# ------------------------------------------------------------------ camada 04
# Sinteticas achadas dentro das pastas de produto.
_add(_PCA, ["Gemini_Generated_Image_hhlj5jhhlj5jhhlj.jpg"], "04-quarentena/sintetica-gemini")
_add(_PCL, ["Gemini_Generated_Image_rw2resrw2resrw2r.jpg"], "04-quarentena/sintetica-gemini")
# Reduzidas para tamanho de WhatsApp/web, sem EXIF. Conceito bom, pixel insuficiente.
_add(_FZ, ["11 (7).jpeg", "11 (8).jpeg", "7.jpg"], "04-quarentena/baixa-resolucao-web")
_add(_PSU, ["Suave-kraft.jpg"], "04-quarentena/baixa-resolucao-web")

#: Mapeamento explicito dos 66 arquivos da base, arquivo por arquivo.
#: Nada de heuristica silenciosa aqui: a heuristica classifica material NOVO,
#: este mapa e o registro do que a curadoria humana ja decidiu.
MAPA_BASE_CURADA: tuple[EntradaMapa, ...] = tuple(_MAPA)


# --------------------------------------------------------------------------- #
# Separacao com auto-verificacao
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class LinhaManifesto:
    origem: str
    destino: str
    camada: Camada


@dataclass(frozen=True)
class ResultadoSeparacao:
    destino: Path
    manifesto: Path
    linhas: tuple[LinhaManifesto, ...]

    @property
    def total(self) -> int:
        return len(self.linhas)

    @property
    def por_camada(self) -> dict[Camada, int]:
        contagem: dict[Camada, int] = {camada: 0 for camada in Camada}
        for linha in self.linhas:
            contagem[linha.camada] += 1
        return contagem


def arquivos_da_base(raiz: Path | str) -> list[Path]:
    """Todo arquivo sob `raiz`, em ordem estavel. Nada de filtro por extensao.

    Filtrar por extensao aqui esconderia justamente o arquivo estranho que
    precisa aparecer na verificacao de exaustividade.
    """
    return sorted(f for f in Path(raiz).rglob("*") if f.is_file())


def _chave(arquivo: Path) -> tuple[str, str]:
    """Chave (pasta, arquivo), como no mapa original: a base tem dois niveis."""
    return (arquivo.parent.name, arquivo.name)


def validar_mapa(mapa: Sequence[EntradaMapa] = MAPA_BASE_CURADA) -> None:
    """Falha se o mapa se contradiz: origem repetida ou dois arquivos no mesmo alvo."""
    vistos: set[tuple[str, str]] = set()
    alvos: set[str] = set()
    for entrada in mapa:
        if entrada.chave in vistos:
            raise SeparacaoInvalida(f"{entrada.origem} mapeado duas vezes")
        vistos.add(entrada.chave)
        # 'Classico (5).jpg' existe em duas pastas com conteudo diferente; o
        # destino separa por SKU, entao nao ha colisao. Verificado ainda assim.
        if entrada.alvo in alvos:
            raise SeparacaoInvalida(f"colisao de destino em {entrada.alvo}")
        alvos.add(entrada.alvo)


def verificar_exaustividade(
    origem: Path | str, mapa: Sequence[EntradaMapa] = MAPA_BASE_CURADA
) -> None:
    """Falha duro se algum arquivo da base ficar sem classificacao.

    Esta e a propriedade que o script original tinha e que nao pode se perder:
    uma separacao que ignora arquivo em silencio produz uma base curada que
    parece completa e nao e. O arquivo que ninguem classificou e o arquivo que
    ninguem olhou - e ele pode ser justamente a sintetica ou o scrape.
    """
    mapeados = {entrada.chave for entrada in mapa}
    pendencias = {
        f"{arquivo.parent.name}/{arquivo.name}": "nenhuma entrada no mapa de curadoria"
        for arquivo in arquivos_da_base(origem)
        if _chave(arquivo) not in mapeados
    }
    if pendencias:
        raise ClassificacaoIncompleta(pendencias)


def classificar_diretorio(
    raiz: Path | str, *, mapa: Sequence[EntradaMapa] | None = None
) -> dict[Path, Camada]:
    """Classifica todo arquivo sob `raiz`: mapa explicito primeiro, heuristica depois.

    Levanta `ClassificacaoIncompleta` se sobrar qualquer arquivo - inclusive o
    ilegivel e aquele que a heuristica se recusou a decidir.
    """
    explicito = {entrada.chave: entrada.camada for entrada in (mapa or ())}
    resultado: dict[Path, Camada] = {}
    pendencias: dict[str, str] = {}

    for arquivo in arquivos_da_base(raiz):
        camada = explicito.get(_chave(arquivo))
        if camada is not None:
            resultado[arquivo] = camada
            continue
        try:
            resultado[arquivo] = classificar(perfil(arquivo))
        except (ClassificacaoIndefinida, ArquivoIlegivel) as exc:
            pendencias[f"{arquivo.parent.name}/{arquivo.name}"] = str(exc)

    if pendencias:
        raise ClassificacaoIncompleta(pendencias)
    return resultado


def separar(
    origem: Path | str,
    destino: Path | str,
    *,
    mapa: Sequence[EntradaMapa] = MAPA_BASE_CURADA,
) -> ResultadoSeparacao:
    """Copia (nunca move) a base para as pastas de camada e grava o manifesto.

    Verifica ANTES de copiar: mapa coerente, todo arquivo mapeado presente no
    disco e todo arquivo do disco classificado. O original checava depois e
    deixava saida pela metade quando falhava.
    """
    raiz_origem, raiz_destino = Path(origem), Path(destino)
    if raiz_destino.exists() and any(raiz_destino.iterdir()):
        raise SeparacaoInvalida(f"{raiz_destino} ja existe e nao esta vazio; remova antes de re-rodar")

    validar_mapa(mapa)

    faltando = [e.origem for e in mapa if not (raiz_origem / e.pasta / e.arquivo).is_file()]
    if faltando:
        raise SeparacaoInvalida(
            "arquivos mapeados que nao existem no disco:\n"
            + "\n".join(f"    {f}" for f in sorted(faltando))
        )

    verificar_exaustividade(raiz_origem, mapa)

    linhas: list[LinhaManifesto] = []
    for entrada in mapa:
        pasta_saida = raiz_destino.joinpath(*entrada.destino.split("/"))
        pasta_saida.mkdir(parents=True, exist_ok=True)
        # Mantem o nome original: perder o nome e perder o rastro da origem.
        shutil.copy2(raiz_origem / entrada.pasta / entrada.arquivo, pasta_saida / entrada.arquivo)
        linhas.append(LinhaManifesto(entrada.origem, entrada.alvo, entrada.camada))

    manifesto = raiz_destino / "manifest.csv"
    with manifesto.open("w", newline="", encoding="utf-8") as fh:
        escritor = csv.DictWriter(fh, fieldnames=["origem", "destino", "camada"])
        escritor.writeheader()
        escritor.writerows(
            {"origem": linha.origem, "destino": linha.destino, "camada": linha.camada.value}
            for linha in linhas
        )

    return ResultadoSeparacao(raiz_destino, manifesto, tuple(linhas))
