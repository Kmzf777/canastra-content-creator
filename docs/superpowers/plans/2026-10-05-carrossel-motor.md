# Plano — motor de carrossel

Spec: [`../specs/2026-10-05-carrossel-motor-design.md`](../specs/2026-10-05-carrossel-motor-design.md)

## Já pronto antes do paralelo

`molde.py` e `tipos.py` foram escritos primeiro, de propósito: são o **contrato** que
os três módulos restantes importam. Escrevê-los em paralelo com o resto produziria
deriva de interface.

Conferido no interpretador: 10 tipos, quadro 1080×1350, área segura 206/134,
piso de 33px no quadro, `validar()` devolvendo lista.

## As três frentes paralelas

Nenhuma escreve arquivo da outra.

| Frente | Arquivos | Depende de |
|---|---|---|
| **A — render** | `render.py`, `tests/test_carrossel_render.py` | `molde`, `tipos` |
| **B — portões** | `portoes.py`, `tests/test_carrossel_portoes.py` | `molde`, `tipos`, e o **formato** de medição de A |
| **C — catálogo e CLI** | `catalogo.py`, `cli.py`, `__main__.py`, `tests/test_carrossel_catalogo.py`, `tests/test_carrossel_cli.py` | `molde`, `tipos` |

### Interface entre A e B — fixada aqui para poderem correr juntas

```python
# render.py
def html_do_slide(slide: Slide, indice: int, total: int) -> str
def escrever_html(deck: Deck, destino: Path) -> list[Path]
def render(htmls: list[Path], destino: Path, chrome: str | None = None) -> list[Path]
def medir(html: Path, chrome: str | None = None) -> dict
def miniaturas(png: Path, destino: Path) -> dict[int, Path]

# o dict que `medir` devolve, e que `portoes` consome:
{
  "slide": 3,
  "transbordos": ["corpo", "itens[2]"],     # caixas com scrollHeight > clientHeight
  "textos": [{"campo": "sub", "px": 26.0}],  # font-size computado, no quadro de 1080
  "fora_da_area_segura": ["titulo"],         # topo < SEGURO_TOPO ou base > ALTURA-SEGURO_BASE
}
```

```python
# portoes.py
def orcamento(deck: Deck) -> list[str]
def transbordo(medicoes: list[dict]) -> list[str]
def legibilidade(medicoes: list[dict]) -> list[str]
def todos(deck: Deck, medicoes: list[dict]) -> dict   # {"ok": bool, "<portao>": [...]}
```

### Como medir no Chrome headless

O `--screenshot` não devolve resultado de JS. A receita prescrita: o HTML embute um
script que escreve o JSON da medição em `document.title`; o render roda
`chrome --headless=new --dump-dom <file-url>` e lê o `<title>` da saída.

**Se `--dump-dom` não funcionar de forma confiável, reporte — não invente número.**
Medição que não foi medida é exatamente o que o `CLAUDE.md` proíbe.

## Depois do paralelo — eu faço

1. `pytest` dos quatro módulos;
2. declarar um deck real reaproveitando as fotos de `saida-teste/carrossel-capsulas/`;
3. rodar os três portões e registrar a saída;
4. renderizar e **olhar** o `_feed/360.png`.

## O que já se sabe que pode dar errado

- **Chrome headless escreve só com caminho absoluto no estilo do Windows** e exige
  `file://` absoluto na entrada. Medido em 05/10 ao montar o carrossel anterior.
- **Fonte do Google Fonts precisa de rede**; sem ela o fallback entra em silêncio e
  os tamanhos medidos mudam. O render tem que declarar qual família realmente pintou.
