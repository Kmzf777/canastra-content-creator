"""Exportacao das imagens aprovadas para publicacao.

Tres garantias, nesta ordem:

  * recorte que nao distorce e nao perde o assunto - o ponto focal manual da UI
    manda, e so na falta dele entra a saliencia local;
  * proveniencia gravada no arquivo (XMP + EXIF) e tambem num sidecar `.xmp`,
    para sobreviver a qualquer plataforma que limpe metadados no upload;
  * manifesto do lote que diz, em portugues, o que a pessoa que publica precisa
    marcar como conteudo de IA no Instagram/Meta.

Tudo aqui e offline e deterministico: nenhuma chamada de rede, nenhum modelo.
"""

from __future__ import annotations

import io
import json
import math
import re
import sqlite3
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence
from xml.sax.saxutils import escape, quoteattr

from PIL import Image, ImageFilter, ImageStat

from . import repository
from .config import Settings
from .enums import ExportFormat, Pillar, ReviewStatus
from .errors import CieError
from .imaging import load_image, sha256_file
from .models import Generation, Job, Template
from .utils import clamp, iso, normalize_token, strip_accents, utcnow

#: Qualidade JPEG da saida. Alto o bastante para rotulo e macro de grao
#: aguentarem a recompressao da plataforma, sem virar arquivo gigante.
EXPORT_QUALITY = 92

#: Proporcoes de publicacao padrao: story/reel, feed vertical e feed quadrado.
DEFAULT_FORMATS: tuple[str, ...] = ("9:16", "4:5", "1:1")

MANIFEST_NAME = "manifest.json"
DEFAULT_CREATOR = "Cafe Canastra"
CREATOR_TOOL = "Canastra Image Engine (CIE)"

#: Principio do sistema, repetido no arquivo para quem so recebe a imagem.
CORE_PRINCIPLE = "A IA edita e estende o real; a IA nao inventa o real."

#: Vocabulario IPTC de origem digital. `trainedAlgorithmicMedia` e o valor
#: conservador: declara envolvimento de IA a mais, nunca a menos.
IPTC_DIGITAL_SOURCE_TYPE = (
    "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"
)

#: Namespace proprio do CIE dentro do XMP.
XMP_CIE_NAMESPACE = "https://cafecanastra.com/ns/cie/1.0/"

DISCLOSURE_SHORT = "Conteudo com assistencia de IA: rotule antes de publicar."

BATCH_LABELING_NOTE = (
    "Toda imagem deste lote com disclosure_required=true precisa ser publicada "
    "com o rotulo de conteudo gerado por IA da propria plataforma. No Instagram/"
    "Meta: no fim do fluxo de publicacao, em 'Configuracoes avancadas', ative a "
    "marcacao de informacoes de IA; em Reels e Stories use a mesma marcacao. O "
    "arquivo ja sai com XMP/EXIF de proveniencia e com um sidecar .xmp ao lado, "
    "mas o upload costuma descartar metadados: a marcacao manual e obrigatoria."
)

# --------------------------------------------------------------------------- #
# Ponto focal
# --------------------------------------------------------------------------- #

#: Kernel Laplaciano 3x3; offset=128 preserva a metade negativa da resposta.
_LAPLACIAN = ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], scale=1, offset=128)

#: Grade de saliencia e reducao maxima antes de medir (custo constante).
FOCAL_GRID = 8
FOCAL_MAX_SIDE = 512


@dataclass
class FocalPoint:
    """Ponto focal relativo (0..1), independente de resolucao."""

    x: float
    y: float

    def __post_init__(self) -> None:
        self.x = clamp(float(self.x), 0.0, 1.0)
        self.y = clamp(float(self.y), 0.0, 1.0)

    @classmethod
    def center(cls) -> FocalPoint:
        return cls(0.5, 0.5)

    def pixel(self, width: int, height: int) -> tuple[int, int]:
        return int(round(self.x * width)), int(round(self.y * height))


def detect_focal_point(image: Image.Image) -> FocalPoint:
    """Saliencia local, sem ML e sem rede.

    Heuristica: reduz a imagem para no maximo 512px, converte para cinza e
    aplica um kernel Laplaciano. A variancia da resposta dentro de cada bloco de
    uma grade 8x8 mede quanto detalhe (borda, textura, microcontraste) aquele
    pedaco carrega - grao torrado e tipografia de rotulo pontuam alto, ceu e
    fundo de estudio pontuam quase zero. Antes de calcular o centro de massa
    subtraimos a MEDIANA das energias e cortamos o negativo: assim o fundo
    homogeneo some da conta e o ponto segue so a regiao com assunto (sem isso,
    uma imagem com metade lisa puxaria o resultado de volta para o centro).
    Imagem uniforme, sem assunto dominante, cai no centro geometrico - que e o
    default seguro para qualquer recorte.
    """
    gray = image.convert("L")
    gray.thumbnail((FOCAL_MAX_SIDE, FOCAL_MAX_SIDE))
    if gray.width < FOCAL_GRID or gray.height < FOCAL_GRID:
        return FocalPoint.center()

    edges = gray.filter(_LAPLACIAN)
    blocks: list[tuple[float, float, float]] = []  # (energia, cx, cy) relativos
    for row in range(FOCAL_GRID):
        top = round(row * edges.height / FOCAL_GRID)
        bottom = round((row + 1) * edges.height / FOCAL_GRID)
        for col in range(FOCAL_GRID):
            left = round(col * edges.width / FOCAL_GRID)
            right = round((col + 1) * edges.width / FOCAL_GRID)
            if right <= left or bottom <= top:
                continue
            energy = ImageStat.Stat(edges.crop((left, top, right, bottom))).var[0]
            blocks.append(
                (
                    float(energy),
                    (left + right) / 2.0 / edges.width,
                    (top + bottom) / 2.0 / edges.height,
                )
            )

    if not blocks:
        return FocalPoint.center()

    baseline = statistics.median(energy for energy, _, _ in blocks)
    total = 0.0
    weighted_x = 0.0
    weighted_y = 0.0
    for energy, cx, cy in blocks:
        weight = max(0.0, energy - baseline)
        total += weight
        weighted_x += weight * cx
        weighted_y += weight * cy
    if total <= 1e-9:
        return FocalPoint.center()
    return FocalPoint(weighted_x / total, weighted_y / total)


# --------------------------------------------------------------------------- #
# Recorte
# --------------------------------------------------------------------------- #


def _ratio_parts(ratio: str | ExportFormat) -> tuple[int, int]:
    """'4:5' -> (4, 5), ja reduzido pelo MDC."""
    text = str(ratio).strip()
    parts = text.split(":")
    if len(parts) != 2:
        raise CieError(f"proporcao invalida: {text!r} (esperado algo como '9:16')")
    try:
        width, height = int(parts[0]), int(parts[1])
    except ValueError:
        raise CieError(f"proporcao invalida: {text!r} (esperado algo como '9:16')") from None
    if width <= 0 or height <= 0:
        raise CieError(f"proporcao invalida: {text!r}")
    divisor = math.gcd(width, height)
    return width // divisor, height // divisor


def smart_crop(
    image: Image.Image, ratio: str | ExportFormat, focal: FocalPoint | None = None
) -> Image.Image:
    """Recorta para a proporcao pedida sem distorcer, mantendo o ponto focal.

    O tamanho do recorte e um multiplo inteiro de `rw:rh` (o maior que cabe):
    calcular a largura como `altura * 0.8` deixaria erro de arredondamento e a
    proporcao sairia 0,7998 em vez de 0,8. O recorte e centrado no ponto focal e
    depois grudado nas bordas da imagem, o que garante que o ponto continua
    dentro do quadro mesmo quando ele esta num canto.
    """
    ratio_w, ratio_h = _ratio_parts(ratio)
    width, height = image.size
    scale = min(width // ratio_w, height // ratio_h)
    if scale < 1:
        raise CieError(
            f"imagem {width}x{height} e pequena demais para o recorte {ratio_w}:{ratio_h}"
        )
    crop_w, crop_h = ratio_w * scale, ratio_h * scale

    point = focal or FocalPoint.center()
    focal_x, focal_y = point.x * width, point.y * height
    left = int(round(clamp(focal_x - crop_w / 2.0, 0.0, float(width - crop_w))))
    top = int(round(clamp(focal_y - crop_h / 2.0, 0.0, float(height - crop_h))))
    return image.crop((left, top, left + crop_w, top + crop_h))


def _srgb_profile() -> bytes | None:
    """Perfil ICC sRGB para marcar a saida. None se o littlecms nao estiver la."""
    try:
        from PIL import ImageCms

        return ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    except Exception:  # pragma: no cover - depende do build do Pillow
        return None


def to_srgb(image: Image.Image) -> Image.Image:
    """Converte para RGB/sRGB. Perfil exotico e transformado, nao ignorado."""
    profile = image.info.get("icc_profile")
    if profile:
        try:
            from PIL import ImageCms

            source = ImageCms.getOpenProfile(io.BytesIO(profile))
            target = ImageCms.createProfile("sRGB")
            converted = ImageCms.profileToProfile(image, source, target, outputMode="RGB")
            if converted is not None:
                return converted
        except Exception:
            # Perfil ilegivel: melhor uma conversao de modo simples do que
            # abortar a exportacao de uma imagem ja aprovada.
            pass
    if image.mode != "RGB":
        return image.convert("RGB")
    return image


# --------------------------------------------------------------------------- #
# Nome do arquivo
# --------------------------------------------------------------------------- #


def _name_token(text: str) -> str:
    token = re.sub(r"[^A-Z0-9]+", "_", normalize_token(text)).strip("_")
    return token or "SEM_NOME"


def export_filename(
    pillar: Pillar | str | None,
    template_name: str,
    sequence: int,
    aspect_ratio: str | ExportFormat,
) -> str:
    """CANASTRA_[PILAR]_[TEMPLATE]_[NNN]_[AR].jpg

    Ex.: CANASTRA_3_MACRO_GRAO_TORRADO_001_9-16.jpg. O ':' da proporcao vira '-'
    porque dois-pontos quebra nome de arquivo em Windows e em URL de CDN.
    """
    # Pilar ausente vira 'X': o nome nunca inventa um pilar que ninguem curou.
    pillar_token = _name_token(str(pillar)) if pillar else "X"
    ratio_token = str(aspect_ratio).replace(":", "-")
    return (
        f"CANASTRA_{pillar_token}_{_name_token(template_name)}"
        f"_{int(sequence):03d}_{ratio_token}.jpg"
    )


# --------------------------------------------------------------------------- #
# Proveniencia, XMP e EXIF
# --------------------------------------------------------------------------- #


def _as_iso(value: datetime | str | None) -> str:
    if isinstance(value, datetime):
        return iso(value) or ""
    return str(value) if value else ""


def build_provenance(
    *,
    model: str,
    created: datetime | str | None,
    reference_asset_ids: Sequence[int] = (),
    template: str | None = None,
    generation_id: int | None = None,
    job_id: int | None = None,
) -> str:
    """Frase unica de proveniencia, legivel por humano e gravada no arquivo."""
    references = ", ".join(str(i) for i in reference_asset_ids) or "nenhum"
    parts = [
        "Imagem gerada com assistencia de IA pelo Canastra Image Engine",
        f"modelo: {model or 'nao registrado'}",
        f"data: {_as_iso(created) or 'nao registrada'}",
        f"assets de referencia (fotos reais da operacao): {references}",
    ]
    if template:
        parts.append(f"template: {template}")
    if generation_id is not None:
        parts.append(f"generation: {generation_id}")
    if job_id is not None:
        parts.append(f"job: {job_id}")
    parts.append(CORE_PRINCIPLE)
    return "; ".join(parts)


def labeling_note(model: str, disclosure_required: bool = True) -> str:
    """O que a pessoa que publica precisa marcar como IA no Instagram/Meta."""
    if not disclosure_required:
        return (
            "Revisao humana registrou disclosure_required=false para esta imagem; "
            "confirme a politica da plataforma antes de publicar sem rotulo."
        )
    return (
        "Marque como conteudo gerado por IA antes de publicar. No Instagram/Meta: "
        "em 'Configuracoes avancadas' do post ative a marcacao de informacoes de "
        "IA; em Reels e Stories use a mesma marcacao. Modelo usado: "
        f"{model or 'nao registrado'}. Rostos e rotulos vem de fotos reais da "
        "operacao, mas a imagem final passou por IA e por isso exige rotulagem."
    )


def build_xmp_packet(
    *,
    creator: str,
    description: str,
    provenance: str,
    model: str,
    created: datetime | str | None,
) -> bytes:
    """Pacote XMP completo (UTF-8), pronto para APP1 ou sidecar."""
    created_text = _as_iso(created)
    return (
        '<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>\n'
        f'<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk={quoteattr(CREATOR_TOOL)}>\n'
        ' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
        '  <rdf:Description rdf:about=""\n'
        '    xmlns:dc="http://purl.org/dc/elements/1.1/"\n'
        '    xmlns:xmp="http://ns.adobe.com/xap/1.0/"\n'
        '    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"\n'
        '    xmlns:Iptc4xmpExt="http://iptc.org/std/Iptc4xmpExt/2008-02-29/"\n'
        f'    xmlns:cie="{XMP_CIE_NAMESPACE}">\n'
        "   <dc:creator><rdf:Seq><rdf:li>"
        f"{escape(creator)}"
        "</rdf:li></rdf:Seq></dc:creator>\n"
        '   <dc:description><rdf:Alt><rdf:li xml:lang="x-default">'
        f"{escape(description)}"
        "</rdf:li></rdf:Alt></dc:description>\n"
        "   <dc:rights><rdf:Alt><rdf:li xml:lang=\"x-default\">"
        f"(c) {escape(creator)}"
        "</rdf:li></rdf:Alt></dc:rights>\n"
        f"   <xmp:CreatorTool>{escape(CREATOR_TOOL)}</xmp:CreatorTool>\n"
        f"   <xmp:CreateDate>{escape(created_text)}</xmp:CreateDate>\n"
        f"   <photoshop:Credit>{escape(creator)}</photoshop:Credit>\n"
        "   <Iptc4xmpExt:DigitalSourceType "
        f"rdf:resource={quoteattr(IPTC_DIGITAL_SOURCE_TYPE)}/>\n"
        "   <cie:aiGenerated>True</cie:aiGenerated>\n"
        "   <cie:disclosureRequired>True</cie:disclosureRequired>\n"
        f"   <cie:model>{escape(model or 'nao registrado')}</cie:model>\n"
        f"   <cie:provenance>{escape(provenance)}</cie:provenance>\n"
        f"   <cie:principle>{escape(CORE_PRINCIPLE)}</cie:principle>\n"
        "  </rdf:Description>\n"
        " </rdf:RDF>\n"
        "</x:xmpmeta>\n"
        '<?xpacket end="w"?>'
    ).encode("utf-8")


# Tags EXIF cruas (mesma escolha de cie/imaging.py: numero, nao nome).
_EXIF_IMAGE_DESCRIPTION = 0x010E
_EXIF_SOFTWARE = 0x0131
_EXIF_DATETIME = 0x0132
_EXIF_ARTIST = 0x013B
_EXIF_COPYRIGHT = 0x8298

_EXIF_SIGNATURE = b"Exif\x00\x00"
_XMP_SIGNATURE = b"http://ns.adobe.com/xap/1.0/\x00"
_APP1 = 0xE1


def _ascii(text: str) -> str:
    """Campo ASCII do EXIF nao aceita acento; a casa ja escreve sem eles."""
    return strip_accents(text).encode("ascii", "ignore").decode("ascii")


def _build_exif(
    *,
    creator: str,
    description: str,
    provenance: str,
    created: datetime | str | None,
) -> bytes:
    exif = Image.Exif()
    exif[_EXIF_ARTIST] = _ascii(creator)
    exif[_EXIF_IMAGE_DESCRIPTION] = _ascii(f"{description} | {provenance}")
    exif[_EXIF_COPYRIGHT] = _ascii(f"(c) {creator}. {DISCLOSURE_SHORT}")
    exif[_EXIF_SOFTWARE] = _ascii(CREATOR_TOOL)
    if isinstance(created, datetime):
        exif[_EXIF_DATETIME] = created.strftime("%Y:%m:%d %H:%M:%S")
    payload = exif.tobytes()
    return payload if payload.startswith(_EXIF_SIGNATURE) else _EXIF_SIGNATURE + payload


def sidecar_path(path: Path | str) -> Path:
    """`foto.jpg` -> `foto.jpg.xmp`."""
    path = Path(path)
    return path.with_name(path.name + ".xmp")


def _app1_segment(payload: bytes) -> bytes:
    if len(payload) + 2 > 0xFFFF:
        raise ValueError("segmento APP1 passa do limite de 64 KB do JPEG")
    return b"\xff\xe1" + (len(payload) + 2).to_bytes(2, "big") + payload


def _strip_provenance_segments(data: bytes) -> bytes:
    """Remove APP1 de EXIF/XMP ja existentes para nao duplicar marcador."""
    out = bytearray(data[:2])
    index = 2
    while index + 4 <= len(data) and data[index] == 0xFF:
        marker = data[index + 1]
        if marker == 0xFF:  # byte de preenchimento entre segmentos
            out += data[index : index + 1]
            index += 1
            continue
        if marker in (0xD8, 0xD9, 0xDA):  # SOI/EOI/SOS: acabou o cabecalho
            break
        length = int.from_bytes(data[index + 2 : index + 4], "big")
        if length < 2 or index + 2 + length > len(data):
            raise ValueError("segmento JPEG malformado")
        payload = data[index + 4 : index + 2 + length]
        drop = marker == _APP1 and (
            payload.startswith(_EXIF_SIGNATURE) or payload.startswith(_XMP_SIGNATURE)
        )
        if not drop:
            out += data[index : index + 2 + length]
        index += 2 + length
    out += data[index:]
    return bytes(out)


def _splice_app1(path: Path, exif_payload: bytes, xmp_payload: bytes) -> None:
    """Injeta EXIF e XMP direto nos bytes do JPEG, sem recomprimir a imagem."""
    data = path.read_bytes()
    if not data.startswith(b"\xff\xd8"):
        raise ValueError("arquivo nao e JPEG")
    body = _strip_provenance_segments(data)
    segments = _app1_segment(exif_payload) + _app1_segment(_XMP_SIGNATURE + xmp_payload)
    # APP1 logo apos o SOI: e o primeiro lugar onde leitor de EXIF/XMP procura.
    path.write_bytes(body[:2] + segments + body[2:])


def _resave_with_metadata(path: Path, exif_payload: bytes, xmp_payload: bytes) -> None:
    """Plano B: reabre e regrava pelo Pillow (custa uma recodificacao JPEG)."""
    with Image.open(path) as image:
        converted = to_srgb(image)
        converted.save(
            path,
            format="JPEG",
            quality=EXPORT_QUALITY,
            subsampling=0,
            optimize=True,
            exif=exif_payload,
            xmp=xmp_payload,
            icc_profile=_srgb_profile(),
        )


def write_metadata(
    path: Path | str,
    *,
    creator: str = DEFAULT_CREATOR,
    description: str,
    provenance: str,
    model: str,
    created: datetime | str | None = None,
) -> None:
    """Grava proveniencia no arquivo e no sidecar.

    O sidecar `<arquivo>.xmp` e escrito SEMPRE, mesmo com o XMP embutido dando
    certo: toda plataforma de rede social remove os metadados do JPEG no upload,
    e o sidecar e a copia que fica no arquivo do lote como prova de origem.
    """
    path = Path(path)
    packet = build_xmp_packet(
        creator=creator,
        description=description,
        provenance=provenance,
        model=model,
        created=created,
    )
    exif_payload = _build_exif(
        creator=creator, description=description, provenance=provenance, created=created
    )

    sidecar_path(path).write_bytes(packet)
    try:
        _splice_app1(path, exif_payload, packet)
    except (OSError, ValueError):
        # JPEG fora do padrao: vale pagar a recodificacao para nao entregar
        # imagem sem proveniencia embutida.
        _resave_with_metadata(path, exif_payload, packet)


# --------------------------------------------------------------------------- #
# Lote
# --------------------------------------------------------------------------- #


@dataclass
class ExportedVariant:
    path: Path
    aspect_ratio: str
    width: int
    height: int
    sha256: str

    def as_dict(self, root: Path | None = None) -> dict[str, Any]:
        return {
            "path": _relative_to(self.path, root),
            "arquivo": self.path.name,
            "aspect_ratio": self.aspect_ratio,
            "width": self.width,
            "height": self.height,
            "sha256": self.sha256,
        }


@dataclass
class ExportBatch:
    out_dir: Path
    variants: list[ExportedVariant] = field(default_factory=list)
    manifest_path: Path | None = None
    generation_ids: list[int] = field(default_factory=list)


def _relative_to(path: Path, root: Path | None) -> str:
    """Caminho relativo a raiz do projeto; absoluto so quando escapa dela."""
    if root is None:
        return str(path)
    try:
        return path.resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return str(path)


def _description_for(template: Template | None, pillar: Pillar | None) -> str:
    parts = [DEFAULT_CREATOR]
    if template is not None:
        parts.append(template.name)
    if pillar is not None:
        parts.append(f"pilar {pillar}")
    return " - ".join(parts)


def _resolve_focal_point(
    conn: sqlite3.Connection, generation: Generation, image: Image.Image
) -> FocalPoint:
    """Curadoria humana primeiro; saliencia so quando ninguem marcou nada."""
    if generation.id is not None:
        stored = repository.get_focal_point(conn, generation.id)
        if stored is not None:
            return FocalPoint(stored[0], stored[1])
    return detect_focal_point(image)


def export_generation(
    conn: sqlite3.Connection,
    settings: Settings,
    generation: Generation,
    *,
    formats: Sequence[str | ExportFormat],
    out_dir: Path | str,
    template: Template | None = None,
    sequence: int = 1,
) -> list[ExportedVariant]:
    """Gera as variantes de uma geracao e registra os caminhos no banco."""
    source = Path(generation.path)
    image = load_image(source)
    if image is None:
        raise CieError(
            f"geracao {generation.id}: nao consegui abrir {source} para exportar"
        )

    # O job entra na proveniencia: e ele que guarda os assets de referencia.
    job = repository.get_job(conn, generation.job_id)
    if template is None and job is not None:
        template = repository.get_template(conn, job.template_id)

    pillar = template.pillar if template else None
    template_name = template.name if template else "sem_template"
    reference_ids = job.reference_asset_ids if job else []

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    description = _description_for(template, pillar)
    provenance = build_provenance(
        model=generation.model,
        created=generation.created_at,
        reference_asset_ids=reference_ids,
        template=template_name,
        generation_id=generation.id,
        job_id=generation.job_id,
    )
    profile = _srgb_profile()

    variants: list[ExportedVariant] = []
    try:
        focal = _resolve_focal_point(conn, generation, image)
        for ratio in formats:
            crop = to_srgb(smart_crop(image, ratio, focal))
            dest = out_dir / export_filename(pillar, template_name, sequence, ratio)
            # subsampling=0 (4:4:4): tipografia de rotulo nao pode perder croma.
            crop.save(
                dest,
                format="JPEG",
                quality=EXPORT_QUALITY,
                subsampling=0,
                optimize=True,
                icc_profile=profile,
            )
            write_metadata(
                dest,
                description=description,
                provenance=provenance,
                model=generation.model,
                created=generation.created_at,
            )
            variants.append(
                ExportedVariant(
                    path=dest,
                    aspect_ratio=str(ratio),
                    width=crop.width,
                    height=crop.height,
                    # Hash depois dos metadados: e o arquivo entregue, nao o intermediario.
                    sha256=sha256_file(dest),
                )
            )
            crop.close()
    finally:
        image.close()

    if generation.id is not None:
        repository.set_exported_variants(
            conn, generation.id, [_relative_to(v.path, settings.root) for v in variants]
        )
    return variants


def _manifest_entry(
    generation: Generation,
    job: Job | None,
    template: Template | None,
    variants: list[ExportedVariant],
    root: Path | None,
) -> dict[str, Any]:
    pillar = template.pillar if template else None
    reference_ids = job.reference_asset_ids if job else []
    return {
        "generation_id": generation.id,
        "job_id": generation.job_id,
        "template": template.name if template else None,
        "pilar": str(pillar) if pillar else None,
        "prompt": generation.prompt,
        "modelo": generation.model,
        "seed": generation.seed,
        "reference_asset_ids": reference_ids,
        "sha256": generation.sha256,
        "disclosure_required": generation.disclosure_required,
        "proveniencia": build_provenance(
            model=generation.model,
            created=generation.created_at,
            reference_asset_ids=reference_ids,
            template=template.name if template else None,
            generation_id=generation.id,
            job_id=generation.job_id,
        ),
        "variantes": [variant.as_dict(root) for variant in variants],
        "rotulagem": labeling_note(generation.model, generation.disclosure_required),
    }


def _write_manifest(
    out_dir: Path, entries: list[dict[str, Any]], formats: Sequence[str | ExportFormat]
) -> Path:
    manifest = {
        "lote": iso(utcnow()),
        "gerado_por": CREATOR_TOOL,
        "out_dir": str(out_dir),
        "formatos": [str(f) for f in formats],
        "principio": CORE_PRINCIPLE,
        "rotulagem": BATCH_LABELING_NOTE,
        "imagens": entries,
    }
    path = out_dir / MANIFEST_NAME
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return path


def export_approved(
    conn: sqlite3.Connection,
    settings: Settings,
    *,
    formats: Sequence[str | ExportFormat] = DEFAULT_FORMATS,
    out_dir: Path | str | None = None,
) -> ExportBatch:
    """Exporta so o que passou pela revisao humana, com manifesto do lote."""
    destination = Path(out_dir) if out_dir is not None else settings.export_dir
    destination.mkdir(parents=True, exist_ok=True)

    approved = repository.list_generations(conn, review_status=ReviewStatus.APPROVED)
    entries: list[dict[str, Any]] = []
    variants: list[ExportedVariant] = []
    generation_ids: list[int] = []

    for position, generation in enumerate(approved, start=1):
        job = repository.get_job(conn, generation.job_id)
        template = repository.get_template(conn, job.template_id) if job else None
        # A sequencia do nome e o id da geracao: nome estavel entre lotes e sem
        # colisao quando o mesmo template e exportado de novo mais tarde.
        sequence = generation.id if generation.id is not None else position
        exported = export_generation(
            conn,
            settings,
            generation,
            formats=formats,
            out_dir=destination,
            template=template,
            sequence=sequence,
        )
        variants.extend(exported)
        if generation.id is not None:
            generation_ids.append(generation.id)
        entries.append(_manifest_entry(generation, job, template, exported, settings.root))

    manifest_path = _write_manifest(destination, entries, formats)
    return ExportBatch(
        out_dir=destination,
        variants=variants,
        manifest_path=manifest_path,
        generation_ids=generation_ids,
    )
