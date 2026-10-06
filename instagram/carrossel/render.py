"""Deck declarado -> HTML por slide -> PNG 1080x1350 -> medicao.

POR QUE HTML E NAO PIL. O texto desenhado por codigo e exato por construcao: nao
existe `Doodo 1985` num `<h1>`. A imagem entra como pixel, o texto como codigo --
a mesma divisao de `instagram/estaticos`.

POR QUE CADA TIPO TEM LAYOUT PROPRIO. A versao anterior deste carrossel usava um
tipo de slide repetido cinco vezes e o cliente chamou de generico, com razao. A
taxonomia so vale se cada tipo pintar diferente.

A MEDICAO E MEDICAO. `medir()` nao estima: embute um script que le
`scrollHeight`/`clientHeight` e `getComputedStyle().fontSize` no proprio Chrome e
devolve o resultado por `document.title`, lido com `--dump-dom`. Conferido em
05/10/2026 numa sonda: caixa que transborda aparece em `transbordos`, e os
`font-size` voltam 26 e 51 para CSS de 26px e 51px.

Spec: docs/superpowers/specs/2026-10-05-carrossel-motor-design.md
"""

from __future__ import annotations

import html as _html
import json
import re
import subprocess
from pathlib import Path

from PIL import Image

from .molde import (
    ALTURA,
    COR,
    FEED_LARGURAS,
    FONTES_GOOGLE,
    LARGURA,
    SEGURO_BASE,
    SEGURO_TOPO,
    TIPO,
)
from .tipos import Deck, Slide

CHROME_PADRAO = r"C:/Program Files/Google/Chrome/Application/chrome.exe"

#: Escala de tipo, em px do quadro de 1080. Nenhum valor abaixo de
#: `molde.PISO_QUADRO_PX` (33) -- o portao de legibilidade reprovaria.
ESCALA = {
    "manchete": 78, "manchete_fecho": 84, "titulo": 64, "numero": 200,
    "nome": 80, "frase": 62, "afirmacao": 60,
    "corpo": 38, "sub": 38, "descritor": 38, "item": 40,
    "passo_titulo": 42, "passo_texto": 34, "evidencia": 38,
    "autor": 34, "fonte": 34, "rodape": 34, "badge": 34, "rotulo_lado": 36,
}


def _e(txt) -> str:
    return _html.escape(str(txt))


def _css() -> str:
    return f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{LARGURA}px;height:{ALTURA}px;overflow:hidden;background:{COR['terra']}}}
.quadro{{position:relative;width:{LARGURA}px;height:{ALTURA}px;overflow:hidden;
  font-family:{TIPO['corpo']};color:{COR['creme']}}}
.quadro.terra{{background:{COR['terra']};color:{COR['creme']}}}
.quadro.creme{{background:{COR['creme']};color:{COR['preto']}}}
.cobre{{position:absolute;left:0;top:0;width:100%;object-fit:cover}}
.quadro.foto .cobre{{height:{ALTURA - 378}px}}
.quadro.foto.capa .cobre{{height:{ALTURA - 460}px}}

/* Caixa de conteudo: nunca invade a area segura da UI do Instagram. */
.conteudo{{position:absolute;left:0;right:0;top:{SEGURO_TOPO}px;bottom:{SEGURO_BASE}px;
  padding:0 64px;display:flex;flex-direction:column}}
.conteudo.fim{{justify-content:flex-end}}
.conteudo.centro{{justify-content:center}}

/* Slide com foto: a foto sangra ate a borda, o TEXTO fica na faixa, e a faixa
   reserva a area segura de baixo. */
/* ALTURA FIXA de proposito: a foto fica inteira acima dela, e `overflow:hidden`
   faz o portao `transbordo` enxergar texto que nao coube. Faixa que cresce
   escondia a base da embalagem -- visto na primeira rodada de 05/10/2026. */
.faixa{{position:absolute;left:0;right:0;bottom:0;height:378px;overflow:hidden;
  background:{COR['terra']};color:{COR['creme']};padding:40px 64px {SEGURO_BASE}px}}
.quadro.capa .faixa{{height:460px}}

h1{{font-family:{TIPO['manchete']};line-height:1.03;letter-spacing:-.016em}}
h2{{font-family:{TIPO['manchete']};line-height:1.06;letter-spacing:-.012em}}
.sub{{line-height:1.34;opacity:.84;margin-top:16px;max-width:860px}}
.acento{{color:{COR['acento']}}}

.rodape{{position:absolute;left:64px;right:64px;bottom:{max(SEGURO_BASE - 56, 24)}px;
  display:flex;justify-content:space-between;align-items:center;
  font-family:{TIPO['dado']};font-size:{ESCALA['rodape']}px;letter-spacing:.14em;opacity:.5}}
.quadro.foto .rodape{{color:{COR['creme']};opacity:.62}}

.badge{{position:absolute;right:64px;bottom:{SEGURO_BASE + 300}px;background:{COR['acento']};
  color:{COR['creme']};font-family:{TIPO['dado']};font-size:{ESCALA['badge']}px;
  letter-spacing:.12em;padding:14px 24px;border-radius:5px}}

ul{{list-style:none;display:flex;flex-direction:column;gap:22px;margin-top:34px}}
li{{display:flex;gap:20px;align-items:baseline;font-size:{ESCALA['item']}px;line-height:1.26}}
li .marca{{color:{COR['acento']};font-family:{TIPO['dado']};flex:0 0 auto}}

.passos{{display:flex;flex-direction:column;gap:28px;margin-top:34px}}
.passo{{display:flex;gap:26px;align-items:flex-start}}
.passo .n{{font-family:{TIPO['manchete']};font-size:56px;color:{COR['acento']};
  line-height:.9;flex:0 0 auto;min-width:70px}}
.passo .t{{font-size:{ESCALA['passo_titulo']}px;font-weight:600;line-height:1.14}}
.passo .x{{font-size:{ESCALA['passo_texto']}px;line-height:1.3;opacity:.8;margin-top:8px}}

.duas{{display:flex;gap:0;margin-top:34px;flex:1}}
.lado{{flex:1;padding:0 34px}}
.lado:first-child{{padding-left:0;border-right:3px solid rgba(200,102,30,.45)}}
.lado:last-child{{padding-right:0}}
.lado .rot{{font-family:{TIPO['dado']};font-size:{ESCALA['rotulo_lado']}px;
  letter-spacing:.12em;color:{COR['acento']};margin-bottom:22px}}
.lado li{{font-size:{ESCALA['item']}px}}

.numerao{{font-family:{TIPO['manchete']};font-size:{ESCALA['numero']}px;line-height:.9;
  letter-spacing:-.03em;color:{COR['acento']};white-space:nowrap}}
.aspas{{font-family:{TIPO['manchete']};font-size:140px;line-height:.6;color:{COR['acento']};
  opacity:.5}}
.autor{{font-family:{TIPO['dado']};font-size:{ESCALA['autor']}px;letter-spacing:.1em;
  margin-top:30px;opacity:.72}}

.prova-caixa{{border-left:6px solid {COR['acento']};padding:4px 0 4px 28px;margin-top:30px}}
.prova-ev{{font-size:{ESCALA['evidencia']}px;line-height:1.3}}
.prova-fonte{{font-family:{TIPO['dado']};font-size:{ESCALA['fonte']}px;line-height:1.3;
  letter-spacing:.04em;opacity:.66;margin-top:18px}}
"""


_MEDICAO_JS = """
const r = {transbordos: [], textos: [], fora_da_area_segura: [], fora_do_quadro: []};
const TOPO = %d, BASE = %d, ALT = %d, LARG = %d;
document.querySelectorAll('[data-campo]').forEach(function(el){
  const c = el.dataset.campo;
  const cs = getComputedStyle(el);
  // `scrollHeight > clientHeight` SO e defeito quando o elemento pode cortar.
  // Medido em 05/10/2026: um h1 de 92px com line-height 1.03 da delta de 8px com
  // `overflow: visible` -- e nada e cortado. Reportar isso como transbordo
  // reprovava os 7 slides do deck por um defeito que nao existia.
  if (cs.overflow !== 'visible' && el.scrollHeight > el.clientHeight + 1) {
    r.transbordos.push(c);
  }
  r.textos.push({campo: c, px: parseFloat(cs.fontSize)});
  const b = el.getBoundingClientRect();
  if (b.top < TOPO - 1 || b.bottom > ALT - BASE + 1) r.fora_da_area_segura.push(c);
  if (b.left < -1 || b.right > LARG + 1 || b.top < -1 || b.bottom > ALT + 1) {
    r.fora_do_quadro.push(c);
  }
});
r.fonte_pintada = getComputedStyle(document.querySelector('h1,h2,.numerao') || document.body).fontFamily;
document.title = JSON.stringify(r);
"""


def _corpo_do_tipo(s: Slide) -> str:
    """O miolo de cada tipo. Cada um pinta diferente -- e a razao do motor existir."""
    d = s.dados
    t = s.tipo

    if t == "capa":
        return (
            f'<h1 data-campo="manchete" style="font-size:{ESCALA["manchete"]}px">{_e(d["manchete"])}</h1>'
            + (f'<p class="sub" data-campo="sub" style="font-size:{ESCALA["sub"]}px">{_e(d["sub"])}</p>'
               if d.get("sub") else "")
        )

    if t == "fecho":
        return (
            f'<h1 data-campo="manchete" style="font-size:{ESCALA["manchete_fecho"]}px">{_e(d["manchete"])}</h1>'
            + (f'<p class="sub" data-campo="sub" style="font-size:{ESCALA["sub"]}px">{_e(d["sub"])}</p>'
               if d.get("sub") else "")
            + (f'<p class="autor" data-campo="destino">{_e(d["destino"])}</p>'
               if d.get("destino") else "")
        )

    if t == "conceito":
        return (
            f'<h2 data-campo="titulo" style="font-size:{ESCALA["titulo"]}px">{_e(d["titulo"])}</h2>'
            f'<p class="sub" data-campo="corpo" style="font-size:{ESCALA["corpo"]}px">{_e(d["corpo"])}</p>'
        )

    if t == "lista":
        itens = "".join(
            f'<li data-campo="item{i}"><span class="marca">—</span><span>{_e(x)}</span></li>'
            for i, x in enumerate(d["itens"])
        )
        return (f'<h2 data-campo="titulo" style="font-size:{ESCALA["titulo"]}px">{_e(d["titulo"])}</h2>'
                f"<ul>{itens}</ul>")

    if t == "passo":
        passos = "".join(
            f'<div class="passo"><div class="n">{i + 1}</div><div>'
            f'<div class="t" data-campo="passo{i}">{_e(p["titulo"])}</div>'
            + (f'<div class="x" data-campo="passo{i}_texto">{_e(p["texto"])}</div>' if p.get("texto") else "")
            + "</div></div>"
            for i, p in enumerate(d["passos"])
        )
        return (f'<h2 data-campo="titulo" style="font-size:{ESCALA["titulo"]}px">{_e(d["titulo"])}</h2>'
                f'<div class="passos">{passos}</div>')

    if t == "comparacao":
        def lado(rot, itens, chave):
            li = "".join(f'<li data-campo="{chave}{i}"><span class="marca">·</span>'
                         f"<span>{_e(x)}</span></li>" for i, x in enumerate(itens))
            return (f'<div class="lado"><div class="rot" data-campo="{chave}_rot">{_e(rot)}</div>'
                    f"<ul>{li}</ul></div>")
        cab = (f'<h2 data-campo="titulo" style="font-size:{ESCALA["titulo"]}px">{_e(d["titulo"])}</h2>'
               if d.get("titulo") else "")
        return (cab + '<div class="duas">'
                + lado(d["rotulo_esq"], d["itens_esq"], "esq")
                + lado(d["rotulo_dir"], d["itens_dir"], "dir") + "</div>")

    if t == "numero":
        return (
            f'<div class="numerao" data-campo="numero">{_e(d["numero"])}</div>'
            f'<h2 data-campo="rotulo" style="font-size:{ESCALA["titulo"]}px;margin-top:18px">{_e(d["rotulo"])}</h2>'
            + (f'<p class="sub" data-campo="sub" style="font-size:{ESCALA["sub"]}px">{_e(d["sub"])}</p>'
               if d.get("sub") else "")
        )

    if t == "citacao":
        rodape = " · ".join(x for x in (d.get("autor"), d.get("papel")) if x)
        return (
            '<div class="aspas">&ldquo;</div>'
            f'<h2 data-campo="frase" style="font-size:{ESCALA["frase"]}px;margin-top:10px">{_e(d["frase"])}</h2>'
            + (f'<p class="autor" data-campo="autor">{_e(rodape)}</p>' if rodape else "")
        )

    if t == "produto":
        return (
            f'<h1 data-campo="nome" style="font-size:{ESCALA["nome"]}px">{_e(d["nome"])}</h1>'
            f'<p class="sub" data-campo="descritor" style="font-size:{ESCALA["descritor"]}px">{_e(d["descritor"])}</p>'
            + (f'<p class="autor" data-campo="sub">{_e(d["sub"])}</p>' if d.get("sub") else "")
        )

    if t == "prova":
        return (
            f'<h2 data-campo="afirmacao" style="font-size:{ESCALA["afirmacao"]}px">{_e(d["afirmacao"])}</h2>'
            '<div class="prova-caixa">'
            f'<div class="prova-ev" data-campo="evidencia">{_e(d["evidencia"])}</div>'
            f'<div class="prova-fonte" data-campo="fonte">Fonte: {_e(d["fonte"])}</div>'
            "</div>"
        )

    raise ValueError(f"tipo sem layout: {t}")


def html_do_slide(slide: Slide, indice: int, total: int) -> str:
    """HTML completo de UM slide, 1080x1350, com CSS inline."""
    rodape = (f'<div class="rodape"><span>CAFÉ CANASTRA</span>'
              f"<span>{indice} / {total}</span></div>")
    js = _MEDICAO_JS % (SEGURO_TOPO, SEGURO_BASE, ALTURA, LARGURA)

    if slide.fundo == "foto":
        badge = (f'<div class="badge" data-campo="badge">{_e(slide.dados["badge"])} →</div>'
                 if slide.dados.get("badge") else "")
        miolo = (f'<img class="cobre" src="{_e(slide.foto.resolve().as_uri())}">'
                 f"{badge}"
                 f'<div class="faixa">{_corpo_do_tipo(slide)}</div>')
        classe = "quadro foto" + (" capa" if slide.tipo == "capa" else "")
    else:
        alinhamento = "centro" if slide.tipo in ("numero", "citacao", "fecho") else "fim"
        miolo = f'<div class="conteudo {alinhamento}">{_corpo_do_tipo(slide)}</div>'
        classe = f"quadro {slide.fundo}"

    return (
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        f'<title>sem medicao</title><link rel="stylesheet" href="{FONTES_GOOGLE}">'
        f"<style>{_css()}</style></head><body>"
        f'<div class="{classe}">{miolo}{rodape}</div>'
        f"<script>{js}</script></body></html>"
    )


def escrever_html(deck: Deck, destino: Path) -> list[Path]:
    destino.mkdir(parents=True, exist_ok=True)
    saida = []
    total = len(deck.slides)
    for i, s in enumerate(deck.slides, 1):
        p = destino / f"slide-{i}.html"
        p.write_text(html_do_slide(s, i, total), encoding="utf-8")
        saida.append(p)
    return saida


def _chrome(caminho: str | None) -> str:
    c = caminho or CHROME_PADRAO
    if not Path(c).exists():
        raise FileNotFoundError(f"Chrome nao encontrado em {c}")
    return c


def render(htmls: list[Path], destino: Path, chrome: str | None = None) -> list[Path]:
    """Um PNG 1080x1350 por HTML.

    MEDIDO EM 05/10/2026, e nao negociavel: a entrada precisa ser `file://`
    absoluto, senao o Chrome trata o caminho relativo como host e devolve
    ERR_NAME_NOT_RESOLVED; e `--screenshot=` precisa de caminho ABSOLUTO no
    estilo do Windows, senao falha com "Failed to write file".
    """
    exe = _chrome(chrome)
    destino.mkdir(parents=True, exist_ok=True)
    saida = []
    for h in htmls:
        png = (destino / f"{h.stem}.png").resolve()
        subprocess.run(
            [exe, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1", f"--window-size={LARGURA},{ALTURA}",
             "--virtual-time-budget=9000", f"--screenshot={png}",
             h.resolve().as_uri()],
            capture_output=True, timeout=120,
        )
        if not png.exists():
            raise RuntimeError(f"Chrome nao gravou {png}")
        saida.append(png)
    return saida


def medir(html: Path, chrome: str | None = None) -> dict:
    """Medicao real, lida do Chrome. Nunca estimativa.

    Se o `<title>` nao voltar como JSON, LEVANTA -- numero que nao foi medido e
    exatamente o que o `CLAUDE.md` proibe. Melhor falhar do que inventar.
    """
    exe = _chrome(chrome)
    r = subprocess.run(
        [exe, "--headless=new", "--disable-gpu", "--virtual-time-budget=9000",
         "--dump-dom", html.resolve().as_uri()],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
    )
    m = re.search(r"<title>(.*?)</title>", r.stdout or "", re.S)
    if not m:
        raise RuntimeError(f"--dump-dom nao devolveu <title> para {html.name}")
    try:
        d = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"<title> de {html.name} nao e JSON de medicao: {m.group(1)[:120]!r}"
        ) from e
    d["slide"] = int(re.sub(r"\D", "", html.stem) or 0)
    return d


def miniaturas(png: Path, destino: Path) -> dict[int, Path]:
    """Reduz para as larguras do feed. O numero nao substitui olhar estas."""
    destino.mkdir(parents=True, exist_ok=True)
    saida = {}
    with Image.open(png) as im:
        for larg in FEED_LARGURAS:
            alt = round(im.height * larg / im.width)
            p = destino / f"{png.stem}-{larg}.png"
            im.resize((larg, alt), Image.LANCZOS).save(p)
            saida[larg] = p
    return saida
