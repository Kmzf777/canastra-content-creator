"""Trimap por limiar: fundo 0.0, objeto 1.0, incerteza 0.5 so na borda.

Nao usa rede neural de proposito: o objetivo e que o interior do objeto receba
alfa 1.0 por CONSTRUCAO, nunca por predicao. Ver o plano em
docs/superpowers/plans/2026-09-30-assets-recorte-e-geracao.md.

Tres modos, porque UM metodo nao cobre as fotos que a operacao realmente tem:

`fundo_uniforme`
    O original. Cor do fundo = mediana das 4 bordas; objeto = o que esta longe
    dela. Correto quando existe **uma** cor de fundo -- packshot de estudio,
    fundo infinito, ciclorama.

`objeto_escuro`
    Limiar de Otsu sobre L*, objeto = a populacao ESCURA. Robusto justamente
    porque nao depende de haver uma cor de fundo unica: separa por luminancia.
    Premissa: a embalagem e escura e o cenario e claro.

`fundo_multicor`
    Fundo = o conjunto das cores que aparecem na moldura da imagem, nao a
    mediana delas. Distancia em Lab ao vizinho mais proximo desse conjunto;
    objeto = o que esta longe de TODAS elas. Cobre parede + chao + a emenda
    escura entre os dois, e nao supoe nada sobre a embalagem ser clara ou
    escura. E o unico modo que serve para os tres SKUs de Uberlandia, porque o
    Suave e kraft CLARO (medido: L do miolo 139, acima do limiar de Otsu 111).

`auto`
    Mede e escolhe -- e registra no diagnostico o que tentou, o que recusou e
    por que.

O que quebrou em 30/09/2026 e o que este arquivo passou a impedir
-----------------------------------------------------------------
Os 3 packshots de Uberlandia nao sao packshot de fundo neutro: e o pacote
deitado no chao ao lado de uma parede, com emenda visivel entre duas
superficies de tom diferente. Nao existe UMA cor de fundo, existem duas, e a
premissa do `fundo_uniforme` nao e satisfeita. Os recortes sairam cobrindo
62,8% a 64,3% do quadro de 4096x2304, com alfa encostando na borda nos tres.

O laudo fotometrico nao pegou: 1 dos 3 saiu `aprovado=true` carregando um naco
da parede, porque `pixels_alterados` compara origem com saida e a saida E a
origem (ver verificar.py). Por isso o portao aqui e **geometrico**:
packshot de embalagem nao encosta na borda do quadro, e nao cobre 60% dele.
Quando encosta, a premissa do metodo foi violada e isso e excecao, nao aviso.
"""

from __future__ import annotations

import cv2
import numpy as np
from scipy.spatial import cKDTree

MODOS = ("fundo_uniforme", "objeto_escuro", "fundo_multicor", "auto")

# Portao: acima disso o componente quase certamente engoliu o fundo.
COBERTURA_MAXIMA = 0.60

# Criterio do `auto` para considerar `objeto_escuro` (medido nos SKUs reais).
SEPARACAO_MINIMA = 60.0
FRACAO_ESCURA_MINIMA = 0.05
FRACAO_ESCURA_MAXIMA = 0.60

# A analise de mascara roda reduzida: barata, e menos sensivel a grao de JPEG.
# O matte depois roda em resolucao nativa -- so a DECISAO e que e reduzida.
ESCALA_ANALISE = 900


class PremissaDeRecorteViolada(RuntimeError):
    """A foto nao satisfaz a premissa do metodo de recorte.

    Levantar e proposital: um recorte que pegou parede junto ainda produz PNG
    bonito e laudo verde. Falha alta e a unica forma de isso nao virar asset.
    """


# --------------------------------------------------------------------------
# medicao
# --------------------------------------------------------------------------

def _reduzir(img_rgb: np.ndarray, lado: int = ESCALA_ANALISE) -> np.ndarray:
    h, w = img_rgb.shape[:2]
    if max(h, w) <= lado:
        return img_rgb
    f = lado / max(h, w)
    return cv2.resize(img_rgb, (max(1, round(w * f)), max(1, round(h * f))),
                      interpolation=cv2.INTER_AREA)


def medir_populacoes(img_rgb: np.ndarray) -> dict:
    """Separa a imagem em duas populacoes por Otsu sobre L* e as mede.

    Devolve o limiar, a fracao escura e a media de L* de cada lado. E a medida
    que o modo `auto` usa para decidir -- nenhum numero aqui e chutado.
    """
    small = _reduzir(img_rgb)
    lum = cv2.cvtColor(small, cv2.COLOR_RGB2LAB)[:, :, 0]
    limiar, _ = cv2.threshold(lum, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    escuro = lum <= limiar
    frac = float(escuro.mean())
    l_esc = float(lum[escuro].mean()) if escuro.any() else 0.0
    l_cla = float(lum[~escuro].mean()) if (~escuro).any() else 0.0
    return {
        "otsu": float(limiar),
        "fracao_escura": frac,
        "l_medio_escuro": round(l_esc, 1),
        "l_medio_claro": round(l_cla, 1),
        "separacao": round(l_cla - l_esc, 1),
    }


def _objeto_escuro_e_plausivel(m: dict) -> bool:
    return (m["separacao"] > SEPARACAO_MINIMA
            and FRACAO_ESCURA_MINIMA < m["fracao_escura"] < FRACAO_ESCURA_MAXIMA)


# --------------------------------------------------------------------------
# sementes: cada modo devolve so um binario bruto, sem morfologia
# --------------------------------------------------------------------------

def _semente_fundo_uniforme(small: np.ndarray,
                            percentil_fundo: float) -> np.ndarray:
    lab = cv2.cvtColor(small, cv2.COLOR_RGB2LAB).astype(np.float32)
    bordas = np.concatenate([lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]],
                            axis=0)
    fundo = np.median(bordas, axis=0)
    dist = np.linalg.norm(lab - fundo, axis=2)
    p = np.percentile(dist, percentil_fundo)
    limiar = p + (dist.max() - p) * 0.12
    return (dist > limiar).astype(np.uint8)


def _semente_objeto_escuro(small: np.ndarray) -> np.ndarray:
    lum = cv2.cvtColor(small, cv2.COLOR_RGB2LAB)[:, :, 0]
    limiar, _ = cv2.threshold(lum, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return (lum <= limiar).astype(np.uint8)


def _semente_fundo_multicor(small: np.ndarray, faixa: int = 10,
                            limiar: float = 8.0) -> np.ndarray:
    """Fundo = a PALETA da moldura, nao a mediana dela.

    A mediana de quatro bordas colapsa parede, chao e emenda numa cor so, e e
    exatamente essa colapsada que nao existe em lugar nenhum da foto. Aqui cada
    cor que aparece na moldura continua sendo fundo por si; objeto e o pixel
    longe de TODAS elas. A emenda escura entre parede e chao entra na paleta
    porque ela tambem toca a borda -- e por isso ela para de ser colada no
    objeto pelo componente conectado.
    """
    lab = cv2.cvtColor(small, cv2.COLOR_RGB2LAB).astype(np.float32)
    h, w = lab.shape[:2]
    f = max(1, min(faixa, h // 3, w // 3))
    moldura = np.concatenate([
        lab[:f, :].reshape(-1, 3), lab[-f:, :].reshape(-1, 3),
        lab[:, :f].reshape(-1, 3), lab[:, -f:].reshape(-1, 3),
    ])
    paleta = np.unique(np.round(moldura / 2.0) * 2.0, axis=0)
    dist, _ = cKDTree(paleta).query(lab.reshape(-1, 3))
    return (dist.reshape(h, w) > limiar).astype(np.uint8)


# --------------------------------------------------------------------------
# consolidacao
# --------------------------------------------------------------------------

def _elipse(r: int):
    r = max(1, int(r))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def _preencher_buracos(m: np.ndarray) -> np.ndarray:
    """Tudo que o fundo nao alcanca a partir de fora e buraco, logo e objeto.

    Sem isso a tipografia clara impressa sobre embalagem escura vira furo na
    mascara, e o laudo devolve `alfa_minimo_no_rotulo=0` -- foi o que aconteceu
    no Suave e no Canela em 30/09/2026.
    """
    h, w = m.shape
    campo = np.zeros((h + 2, w + 2), np.uint8)
    campo[1:-1, 1:-1] = m
    fora = campo.copy()
    mascara_ff = np.zeros((h + 4, w + 4), np.uint8)
    cv2.floodFill(fora, mascara_ff, (0, 0), 1)
    return (m | (1 - fora[1:-1, 1:-1])).astype(np.uint8)


def _maior_componente(bruto: np.ndarray) -> np.ndarray:
    """Abrir -> preencher -> rotular -> maior -> fechar -> preencher.

    Fechar ANTES de rotular cola a sombra ao objeto; por isso o fecho vem
    depois de escolher o componente, nunca antes.
    """
    aberto = cv2.morphologyEx(bruto, cv2.MORPH_OPEN, _elipse(2))
    aberto = _preencher_buracos(aberto)
    n, rotulos, stats, _ = cv2.connectedComponentsWithStats(aberto, 8)
    if n <= 1:
        return np.zeros_like(bruto)
    maior = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    comp = (rotulos == maior).astype(np.uint8)
    comp = cv2.morphologyEx(comp, cv2.MORPH_CLOSE, _elipse(4))
    return _preencher_buracos(comp)


def _refinar(small: np.ndarray, comp: np.ndarray) -> np.ndarray:
    """GrabCut com a semente como palpite, a moldura como fundo certo.

    Por que e seguro para a promessa deste modulo: o grabCut so decide QUAL
    regiao e a embalagem. O alfa do interior continua travado em 1.0 pelo
    trimap, e o RGB nunca e tocado. A predicao para na geometria.

    Serve para duas coisas medidas nos SKUs reais: recupera areas da embalagem
    escura que a paleta de fundo comeu (Classico, canto inferior esquerdo) e
    solta a sombra projetada na parede que veio grudada no pacote (Suave, cunha
    acima do saco). Sem ele o Classico perde um naco do pacote e o Suave leva
    sombra junto.
    """
    area = int(comp.sum())
    h, w = comp.shape
    if area < 500 or min(h, w) < 64:
        return comp
    raio = max(2, round(0.05 * np.sqrt(area)))
    semente = cv2.erode(comp, _elipse(raio))
    nucleo = cv2.erode(comp, _elipse(round(raio * 1.75)))
    if semente.sum() == 0 or nucleo.sum() == 0:
        return comp

    gm = np.full((h, w), cv2.GC_PR_BGD, np.uint8)
    gm[semente == 1] = cv2.GC_PR_FGD
    gm[nucleo == 1] = cv2.GC_FGD
    m = max(2, round(min(h, w) * 0.024))
    gm[:m, :] = cv2.GC_BGD
    gm[-m:, :] = cv2.GC_BGD
    gm[:, :m] = cv2.GC_BGD
    gm[:, -m:] = cv2.GC_BGD

    try:
        cv2.grabCut(cv2.cvtColor(small, cv2.COLOR_RGB2BGR), gm, None,
                    np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64),
                    6, cv2.GC_INIT_WITH_MASK)
    except cv2.error:
        # imagem chapada demais para as GMMs; a semente ja serve
        return comp
    saida = np.where((gm == cv2.GC_FGD) | (gm == cv2.GC_PR_FGD), 1, 0)
    refinado = _maior_componente(saida.astype(np.uint8))
    if refinado.sum() < area * 0.5:
        # o grabCut se perdeu; nao trocamos uma mascara medida por uma pior
        return comp
    return refinado


def _medir_componente(comp: np.ndarray) -> dict:
    h, w = comp.shape
    lados = [nome for nome, linha in (
        ("topo", comp[0, :]), ("base", comp[-1, :]),
        ("esquerda", comp[:, 0]), ("direita", comp[:, -1]))
        if linha.any()]
    ys, xs = np.nonzero(comp)
    caixa = ([int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
             if xs.size else None)
    return {
        "fracao_coberta": round(float(comp.mean()), 4),
        "toca_borda": bool(lados),
        "lados_tocados": lados,
        "caixa": caixa,
        "area_px": int(comp.sum()),
        "dimensoes_analise": [int(w), int(h)],
    }


def _recusa(modo: str, medida: dict) -> str | None:
    """Motivo pelo qual esta mascara nao pode ser aceita, ou None."""
    if medida["area_px"] == 0:
        return f"modo {modo}: nenhum componente encontrado"
    if medida["toca_borda"]:
        return (f"modo {modo}: o maior componente TOCA A BORDA da imagem "
                f"({', '.join(medida['lados_tocados'])}). Packshot de "
                f"embalagem nao encosta na borda -- isso e cenario entrando "
                f"no recorte, nao objeto. A foto nao satisfaz a premissa "
                f"deste metodo.")
    if medida["fracao_coberta"] > COBERTURA_MAXIMA:
        return (f"modo {modo}: o componente cobre "
                f"{100 * medida['fracao_coberta']:.1f}% do quadro, acima do "
                f"teto de {100 * COBERTURA_MAXIMA:.0f}%. E quase certo que o "
                f"fundo entrou junto.")
    return None


def _mascara_de_um_modo(small: np.ndarray, modo: str, percentil_fundo: float,
                        refinar: bool) -> tuple[np.ndarray, dict]:
    """Roda um modo e devolve (mascara, registro auditavel da tentativa).

    O portao e cobrado na SEMENTE, antes do grabCut, e de novo depois. Cobrar
    so depois nao serviria de nada: o grabCut marca a moldura da imagem como
    fundo certo, entao nenhum resultado dele encosta na borda e o portao nunca
    dispararia. Quem tem que satisfazer a premissa e o metodo, nao o refino.
    """
    if modo == "fundo_uniforme":
        bruto = _semente_fundo_uniforme(small, percentil_fundo)
    elif modo == "objeto_escuro":
        bruto = _semente_objeto_escuro(small)
    elif modo == "fundo_multicor":
        bruto = _semente_fundo_multicor(small)
    else:
        raise ValueError(
            f"modo desconhecido: {modo!r}. Validos: {', '.join(MODOS)}")

    comp = _maior_componente(bruto)
    medida = _medir_componente(comp)
    motivo = _recusa(modo, medida)
    registro = {"modo": modo, **medida, "semente": dict(medida),
                "recusa": motivo}
    if motivo is not None:
        return comp, registro

    if refinar and comp.any():
        comp = _refinar(small, comp)
        medida = _medir_componente(comp)
        motivo = _recusa(modo, medida)
        registro.update(medida)
        registro["recusa"] = motivo
    return comp, registro


# --------------------------------------------------------------------------
# API
# --------------------------------------------------------------------------

def mascara_objeto(img_rgb: np.ndarray, modo: str = "auto",
                   percentil_fundo: float = 2.0, refinar: bool = True,
                   escala_analise: int = ESCALA_ANALISE
                   ) -> tuple[np.ndarray, dict]:
    """Mascara binaria do objeto em resolucao nativa, mais o diagnostico.

    `modo` e um de MODOS. Com `auto`, a escolha e feita medindo e o
    diagnostico registra cada tentativa -- fica auditavel qual modo rodou.

    Levanta `PremissaDeRecorteViolada` quando nenhum modo elegivel entrega um
    componente que passe no portao geometrico.
    """
    if modo not in MODOS:
        raise ValueError(
            f"modo desconhecido: {modo!r}. Validos: {', '.join(MODOS)}")

    small = _reduzir(img_rgb, escala_analise)
    populacoes = medir_populacoes(img_rgb)

    if modo == "auto":
        ordem = ["fundo_uniforme"]
        if _objeto_escuro_e_plausivel(populacoes):
            ordem.append("objeto_escuro")
        ordem.append("fundo_multicor")
    else:
        ordem = [modo]

    tentativas: list[dict] = []
    escolhido = None
    for m in ordem:
        comp, registro = _mascara_de_um_modo(small, m, percentil_fundo,
                                             refinar)
        tentativas.append(registro)
        if registro["recusa"] is None:
            escolhido = (m, comp, registro)
            break

    if escolhido is None:
        detalhe = "\n  ".join(t["recusa"] for t in tentativas if t["recusa"])
        raise PremissaDeRecorteViolada(
            f"nenhum modo produziu um recorte plausivel ({modo}):\n  {detalhe}")

    nome, comp, medida = escolhido
    alvo = (img_rgb.shape[1], img_rgb.shape[0])
    if comp.shape[:2] != img_rgb.shape[:2]:
        grande = cv2.resize(comp.astype(np.float32), alvo,
                            interpolation=cv2.INTER_LINEAR)
        comp_full = (grande > 0.5).astype(np.uint8)
        comp_full = _preencher_buracos(comp_full)
    else:
        comp_full = comp

    diagnostico = {
        "modo": nome,
        "modo_pedido": modo,
        "refinado_por_grabcut": bool(refinar),
        "populacoes": populacoes,
        "escala_analise": [int(small.shape[1]), int(small.shape[0])],
        "tentativas": tentativas,
        **_medir_componente(comp_full),
        "orientacao": _medir_orientacao(comp_full),
    }
    return comp_full, diagnostico


def _medir_orientacao(comp: np.ndarray) -> dict:
    """Mede como a embalagem esta posta no quadro. Mede, nao supoe.

    Quem for usar o recorte no motor de video precisa saber que nestas fotos o
    pacote esta DEITADO: o eixo longo e horizontal, entao girar -90 graus poe
    o pacote em pe. O angulo vem de `minAreaRect`, a razao vem do proprio
    retangulo minimo -- nada aqui e estimado no olho.
    """
    contornos, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return {}
    (_, _), (lw, lh), ang = cv2.minAreaRect(max(contornos, key=cv2.contourArea))
    lado_longo, lado_curto = (max(lw, lh), min(lw, lh))
    # angulo do EIXO LONGO em relacao a horizontal, em [-90, 90)
    ang_longo = ang if lw >= lh else ang - 90.0
    ang_longo = (ang_longo + 90.0) % 180.0 - 90.0
    deitada = abs(ang_longo) < 45.0
    return {
        "eixo_longo_graus": round(float(ang_longo), 1),
        "lado_longo_px": round(float(lado_longo), 1),
        "lado_curto_px": round(float(lado_curto), 1),
        "razao": round(float(lado_longo / max(lado_curto, 1e-6)), 2),
        "deitada": bool(deitada),
        "giro_para_ficar_em_pe_graus": -90 if deitada else 0,
    }


def gerar_trimap(img_rgb: np.ndarray, banda: int = 6,
                 percentil_fundo: float = 2.0,
                 modo: str = "auto") -> np.ndarray:
    """Devolve um trimap float32: 0.0 fundo, 1.0 objeto, 0.5 desconhecido.

    `banda` e a largura em pixels da faixa de incerteza em volta da borda.
    """
    return gerar_trimap_detalhado(img_rgb, banda, percentil_fundo, modo)[0]


def gerar_trimap_detalhado(img_rgb: np.ndarray, banda: int = 6,
                           percentil_fundo: float = 2.0, modo: str = "auto",
                           escala_analise: int = ESCALA_ANALISE
                           ) -> tuple[np.ndarray, dict]:
    """Mesmo trimap, mais o diagnostico de qual modo rodou e o que ele mediu."""
    comp, diag = mascara_objeto(img_rgb, modo=modo,
                                percentil_fundo=percentil_fundo,
                                escala_analise=escala_analise)

    # A decisao de mascara roda reduzida; a borda dela chega em resolucao
    # nativa com incerteza de um fator de escala inteiro. A faixa desconhecida
    # tem que cobrir essa incerteza, ou o solver recebe como certo um pixel que
    # a analise nao viu. Por isso a banda cresce com o fator, em vez de ficar
    # no valor pedido e deixar a borda verdadeira fora dela.
    fator = max(img_rgb.shape[0], img_rgb.shape[1]) / max(
        diag["escala_analise"][0], diag["escala_analise"][1])
    banda_efetiva = int(max(1, int(banda)) + np.ceil(max(0.0, fator - 1.0)))
    diag["banda_pedida"] = int(banda)
    diag["banda_efetiva"] = int(banda_efetiva)

    kb = _elipse(banda_efetiva)
    dentro = cv2.erode(comp, kb)
    fora = cv2.dilate(comp, kb)

    tri = np.full(comp.shape, 0.5, dtype=np.float32)
    tri[fora == 0] = 0.0
    tri[dentro == 1] = 1.0
    return tri, diag
