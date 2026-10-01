# Motor de estáticos dirigido por catálogo — plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** construir `instagram/estaticos/` — o pacote que declara peças estáticas, monta o prompt de geração, roteia a correção do rótulo por uma escada com teto, e cai para composição de pixel real quando o modelo insiste no erro.

**Architecture:** o catálogo é dado (`dataclass`), não prosa. Uma declaração alimenta três consumidores: bloco de soletração do prompt, checklist da conferência e asserções do laudo. Python é dono de dados e pixel; Remotion é dono de tipografia; a costura é um arquivo `.json` de props. Todo módulo é puro e testável sem navegador — a geração entra como função injetada, nunca importada.

**Tech Stack:** Python 3.11, Pillow ≥10.3, numpy ≥1.26, pytest 8.2 · reusa `instagram/recorte/` (matting + laudo) e `scripts/prompts_catalogo.py` (os 21 SKUs) · Remotion 4.0.530 na trilha gated.

**Spec:** `docs/superpowers/specs/2026-09-30-estaticos-motor-design.md`. Onde este plano e a spec divergirem, a spec manda — exceto nos dois pontos de **Refinamentos sobre a spec**, onde ler o código revelou coisa que a spec não sabia.

**Diretório de trabalho de todo comando deste plano:** a raiz do repositório,
`C:/Users/rafae/OneDrive/Desktop/Canastra Inteligencia/Agentes AI/Canastra-Content-Creator`.

**Este pacote não roda em worktree.** Ele lê `fotos produtos cru/` e `saida-teste/`, que são gitignored e vivem só no diretório principal.

---

## Estado medido da máquina, que os passos assumem

| fato | evidência |
|---|---|
| suíte Python: **912 passed** em 251s | `python -m uv run pytest -p no:cacheprovider`, 30/09/2026 21:30 |
| `testpaths = ["tests"]` — teste novo vai na raiz `tests/`, não em `instagram/` | `pyproject.toml`, `[tool.pytest.ini_options]` |
| `instagram/` **não tem** `__init__.py`; é namespace package (PEP 420) | `ls instagram/__init__.py` → não existe, e `tests/test_matte.py:14` faz `from instagram.recorte.matte import recortar` |
| `laudo_preservacao(rgb_origem, rgb_saida, alfa, tolerancia=0, retangulo_rotulo=None) -> dict` | `instagram/recorte/verificar.py` |
| `PRODUTOS: list[Produto]` com 21 entradas; `Produto` tem args posicionais `(slug, nome, pasta, familia, corpo, fundo, ocupacao, frente, verso, arte)` | `scripts/prompts_catalogo.py:120` e `:175` |
| `classico-250g-graos` existe em `PRODUTOS` | `scripts/prompts_catalogo.py:230` |
| 250 g grãos custa **R$ 31,70**, de `tabela.cafecanastra.com`, shoot de 11/09/2026 | `fotos produtos cru/_LEIA-ME.md:4` e `:14` |
| suíte Remotion deu **85 passed** às 18:36 — e **esse número está velho**: outra sessão criou `cadencia.ts`, `relogio.ts` e dois testes depois disso | `npx vitest run` às 18:36; mtime 20:53–21:06 |

**Nenhum passo deste plano diz `Expected: 913 passed`.** Onde a suíte inteira roda, o passo manda anotar o número antes e conferir o delta.

---

## Refinamentos sobre a spec

Dois pontos que só apareceram lendo o código. A spec não está errada; está incompleta.

### R1 — o laudo de `recorte/` é tautológico no fluxo dele, e não no nosso

`instagram/recorte/verificar.py` traz, em comentário próprio, que `pixels_alterados` e `maior_delta` **dão 0 por construção** no fluxo atual: `matte.recortar` devolve o RGB de entrada sem tocar em nada, então comparar entrada com saída não pode acusar nada. O comentário registra que foi assim que um dos 3 SKUs saiu `aprovado=true` carregando um naco de parede clara.

**No degrau 6 a comparação vale**, porque origem e saída são imagens de fato diferentes: origem é o recorte real reamostrado, saída é a região correspondente da peça final. Mas quem implementar `compor.py` tem que passar **essas duas** imagens, não entrada-e-saída do mesmo array. A Tarefa 7 tem um teste que falha de propósito se alguém reproduzir a tautologia.

### R2 — o molde da v1 não pode ser a carta sensorial

A spec §10.1 bloqueia nota sensorial: a lição 18 e a lição 21 divergem no CORPO do Suave, o Canela da 21 é exatamente o Suave da 18, e as duas fontes são das cápsulas. Dado bloqueado não entra num `Dado.origem`.

Então a v1 usa o molde **`cartao-produto`**, cujos três campos têm origem sólida e citável:

| campo | valor | origem declarada |
|---|---|---|
| `preco` | `R$ 31,70` | `fotos produtos cru/_LEIA-ME.md`, de `tabela.cafecanastra.com` em 11/09/2026 |
| `altitude` | `1.250 m` | EXIF GPS de `base-curada/01-real-verificada/fazenda-medeiros-1250m/` |
| `local` | `Medeiros, MG` | idem |

`carta-sensorial` entra como **linha de `MOLDES` e de `PECAS`** assim que o Arthur confirmar as notas — sem código novo. Se exigir código novo, a abstração da Tarefa 1 está errada.

### R3 — `catalogo.py` NÃO importa `Produto` na v1

A spec §5 diz *"`catalogo.py` importa `Produto` em vez de redeclarar SKU"*. O plano **não faz isso**, por dois motivos que só aparecem no disco:

1. `scripts/` não é pacote importável — não há `scripts/__init__.py`, e `prompts_catalogo.py` resolve caminho por `Path(__file__).parent.parent`. Importar de lá acoplaria `instagram/` a `scripts/` por um caminho frágil.
2. A `fonte` da peça v1 é um packshot **já aprovado** em `saida-teste/catalogo-estudio/`, não a foto crua de `Produto.pasta`. `Produto` não tem esse campo.

O acoplamento fica para quando `carta-sensorial` entrar: aí os dados vêm de `lateral_extra`, e aí vale a pena. **Registrado como desvio consciente da spec, não como esquecimento.**

### A emenda entre veredito e sintoma é o agente, de propósito

`conferir.py` produz recortes e valida vereditos; `escada.py` consome **sintomas**. Nada mapeia um no outro, e isso é deliberado: decidir se `SOSCIALTY` é `letra-corrompida` ou se `70` é `valor-inventado` é julgamento de quem olha, não função pura. O fluxo é:

```
conferir.recortes()  -> o agente OLHA os pares ampliados
o agente             -> atribui veredito por campo (ok | errado | nao-verificavel)
conferir.bloqueia()  -> diz quais campos barram
o agente             -> nomeia o sintoma de cada campo barrado, de SINTOMAS
escada.executar()    -> roteia o degrau
```

Quem executar o plano **não deve procurar** uma função `veredito_para_sintoma`. Ela não existe e não deve existir.

---

## Mapa de arquivos

| Arquivo | Responsabilidade | Tarefa |
|---|---|---|
| `instagram/estaticos/__init__.py` | marca o pacote; nada mais | 1 |
| `instagram/estaticos/catalogo.py` | `Dado`, `Molde`, `Peca`, `MOLDES`, `PECAS`, `validar()` | 1, 2 |
| `instagram/estaticos/prompt.py` | declaração → texto do prompt, com bloco de soletração | 3 |
| `instagram/estaticos/escada.py` | tabela sintoma→degrau, roteamento, e o laço com teto | 4, 5 |
| `instagram/estaticos/conferir.py` | recortes ampliados por string, da gerada e da referência | 6 |
| `instagram/estaticos/compor.py` | degrau 6: cola o recorte real e emite laudo não-tautológico | 7 |
| `instagram/estaticos/bundle.py` | pasta de saída + `sidecar.json` | 8 |
| `instagram/estaticos/cli.py` | comandos `conferir`, `prompt`, `bundle` | 9 |
| `instagram/estaticos/__main__.py` | `python -m instagram.estaticos` | 9 |
| `tests/test_estaticos_catalogo.py` | validação da declaração | 1, 2 |
| `tests/test_estaticos_prompt.py` | prompt contém toda string declarada | 3 |
| `tests/test_estaticos_escada.py` | roteamento determinístico + teto | 4, 5 |
| `tests/test_estaticos_conferir.py` | recortes gerados nos dois lados | 6 |
| `tests/test_estaticos_compor.py` | laudo não-tautológico | 7 |
| `tests/test_estaticos_bundle.py` | sidecar completo, campo não verificável bloqueia | 8 |
| `instagram/remotion/src/motor/layout.ts` | **+ zona 4:5** | 10 — GATED |
| `instagram/remotion/src/estatico/Carta.tsx` | composição do cartão | 11 — GATED |
| `.claude/skills/canastra-estatico/SKILL.md` | conduz o laço; não guarda dado de SKU | 12 |

---

## Trilhas paralelas

O grafo de dependência permite quatro frentes ao mesmo tempo:

```
Trilha A:  Tarefa 1 -> Tarefa 2 -> Tarefa 3
Trilha B:  Tarefa 4 -> Tarefa 5           (escada é pura, não vê catálogo)
Trilha C:  Tarefa 6                        (recortes: só imagem + caixas)
Trilha D:  Tarefa 7                        (compor: só recorte/ + Pillow)

depois, em sequência:  Tarefa 8 -> Tarefa 9 -> Tarefa 12
GATED, fora do caminho:  Tarefa 10 -> Tarefa 11
```

**Regra de commit para quem executa em paralelo:** `git add` com **caminhos explícitos**, nunca `-A`. Há outra sessão com trabalho não commitado em `instagram/remotion/` e em `mercadolivre/`; `git add -A` arrastaria tudo para o seu commit. É a lição 9 do `CLAUDE.md`.

---

## Tarefa 1: o pacote e a declaração

**Files:**
- Create: `instagram/estaticos/__init__.py`
- Create: `instagram/estaticos/catalogo.py`
- Test: `tests/test_estaticos_catalogo.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_estaticos_catalogo.py
from pathlib import Path

import pytest

from instagram.estaticos.catalogo import MOLDES, PECAS, Dado, Molde, Peca


def test_molde_cartao_produto_existe_e_e_4x5():
    m = MOLDES["cartao-produto"]
    assert isinstance(m, Molde)
    assert (m.largura, m.altura) == (1080, 1350)
    # 1080/1350 = 0.8 = 4:5
    assert m.largura * 5 == m.altura * 4


def test_molde_declara_os_campos_que_o_codigo_desenha():
    assert MOLDES["cartao-produto"].campos == ("preco", "altitude", "local")


def test_existe_uma_peca_e_ela_e_frozen():
    assert len(PECAS) >= 1
    p = PECAS[0]
    assert isinstance(p, Peca)
    with pytest.raises(Exception):
        p.slug = "outro"  # frozen=True


def test_dado_exige_origem_sem_default():
    # origem nao tem default: construir sem ela e TypeError, nao um dado anonimo
    with pytest.raises(TypeError):
        Dado("8,0")


def test_peca_declara_strings_impressas_e_dados_com_origem():
    p = PECAS[0]
    assert p.strings_impressas, "strings_impressas vazia nao serve de gabarito"
    assert set(p.dados) == set(MOLDES[p.molde].campos)
    for chave, d in p.dados.items():
        assert isinstance(d, Dado)
        assert d.origem.strip(), f"{chave} sem origem declarada"


def test_fonte_da_peca_e_caminho_absoluto_existente():
    assert isinstance(PECAS[0].fonte, Path)
    assert PECAS[0].fonte.is_absolute()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m uv run pytest tests/test_estaticos_catalogo.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'instagram.estaticos'`

- [ ] **Step 3: Write minimal implementation**

```python
# instagram/estaticos/__init__.py
"""Motor de estaticos: declaracao de peca -> bundle publicavel.

Spec: docs/superpowers/specs/2026-09-30-estaticos-motor-design.md
"""
```

```python
# instagram/estaticos/catalogo.py
"""Declaracao das pecas estaticas. Dado sem origem nao entra.

POR QUE ISTO E DADO E NAO PROSA. Dos itens do `Registro de licoes` do
CLAUDE.md, ao menos quatro -- 13, 18, 21 e 22 -- sao a mesma falha: um valor
que ninguem declarou, logo ninguem conferiu. `Doodo 1985`, `70/80/80/40`,
`ARABICA` sem acento, `F:23.2025`.

`strings_impressas` existe para ser consumida por TRES lugares a partir desta
mesma fonte: o bloco de soletracao do prompt, o checklist da conferencia e as
assercoes do laudo. Se a lista fosse memoria do agente, ele voltaria a montar
na hora -- e foi assim que um campo fisicamente ilegivel virou "confere".
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Dado:
    """Um valor que o CODIGO desenha na peca.

    `origem` nao tem default de proposito: e um campo obrigatorio para forcar
    a resposta "de onde veio este numero" na hora de declarar, nao na hora de
    conferir. Ver licao 18.
    """

    valor: str
    origem: str


@dataclass(frozen=True)
class Molde:
    """Um layout. `campos` sao as chaves que `Peca.dados` DEVE ter, exatamente."""

    nome: str
    campos: tuple[str, ...]
    largura: int
    altura: int


@dataclass(frozen=True)
class Peca:
    slug: str
    molde: str
    fonte: Path
    strings_impressas: tuple[str, ...]
    dados: dict[str, Dado]
    gerar_fundo: bool


MOLDES: dict[str, Molde] = {
    "cartao-produto": Molde(
        "cartao-produto", ("preco", "altitude", "local"), 1080, 1350
    ),
    # `carta-sensorial` entra AQUI quando as notas forem confirmadas com o
    # Arthur -- ver o bloqueio 10.1 da spec. Nao precisa de codigo novo.
}

# A fonte e o packshot de estudio JA APROVADO, nao a foto crua: ele e a ancora
# de que `canastra-embalagem` fala, e poupa uma rodada de conferencia.
_FONTE_CLASSICO = (
    RAIZ
    / "saida-teste"
    / "catalogo-estudio"
    / "7-classico-250g-graos"
    / "7.1-frente-branco.png"
)

PECAS: list[Peca] = [
    Peca(
        slug="cartao-classico-250g-graos",
        molde="cartao-produto",
        fonte=_FONTE_CLASSICO,
        # Lidas na arte real. `SCA 80+` no saco -- e `SCAA 80+` na capsula, que
        # e exatamente o tipo de diferenca que `prompts_catalogo.py` existe para
        # nao perder numa copia-e-cola.
        strings_impressas=(
            "CANASTRA",
            "SCA 80+",
            "CLÁSSICO",
            "TORRADO EM GRÃOS",
            "250g",
        ),
        dados={
            "preco": Dado(
                "R$ 31,70",
                "fotos produtos cru/_LEIA-ME.md, de tabela.cafecanastra.com em 11/09/2026",
            ),
            "altitude": Dado(
                "1.250 m",
                "EXIF GPS de base-curada/01-real-verificada/fazenda-medeiros-1250m/",
            ),
            "local": Dado(
                "Medeiros, MG",
                "EXIF GPS de base-curada/01-real-verificada/fazenda-medeiros-1250m/",
            ),
        },
        gerar_fundo=True,
    ),
]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m uv run pytest tests/test_estaticos_catalogo.py -q`
Expected: PASS, 6 passed

- [ ] **Step 5: Commit**

```bash
git add instagram/estaticos/__init__.py instagram/estaticos/catalogo.py tests/test_estaticos_catalogo.py
git commit -m "Estaticos: declaracao de peca, com origem obrigatoria no dado"
```

---

## Tarefa 2: `validar()` — a declaração se recusa a passar incompleta

**Files:**
- Modify: `instagram/estaticos/catalogo.py` (acrescenta `validar()` ao fim)
- Test: `tests/test_estaticos_catalogo.py` (acrescenta)

- [ ] **Step 1: Write the failing test**

```python
# acrescentar a tests/test_estaticos_catalogo.py
from instagram.estaticos.catalogo import DeclaracaoInvalida, validar


def _peca_boa(tmp_path):
    fonte = tmp_path / "f.png"
    fonte.write_bytes(b"x")
    return Peca(
        slug="s", molde="cartao-produto", fonte=fonte,
        strings_impressas=("CANASTRA",),
        dados={
            "preco": Dado("R$ 1,00", "fonte x"),
            "altitude": Dado("1.250 m", "fonte y"),
            "local": Dado("Medeiros, MG", "fonte y"),
        },
        gerar_fundo=False,
    )


def test_validar_aceita_peca_completa(tmp_path):
    assert validar([_peca_boa(tmp_path)]) == []


def test_validar_recusa_origem_vazia(tmp_path):
    p = _peca_boa(tmp_path)
    ruim = Peca(**{**p.__dict__, "dados": {**p.dados, "preco": Dado("R$ 1,00", "  ")}})
    problemas = validar([ruim])
    assert any("origem" in x and "preco" in x for x in problemas)


def test_validar_recusa_fonte_ausente(tmp_path):
    p = _peca_boa(tmp_path)
    ruim = Peca(**{**p.__dict__, "fonte": tmp_path / "nao-existe.png"})
    assert any("fonte" in x for x in validar([ruim]))


def test_validar_recusa_campo_fora_do_molde(tmp_path):
    p = _peca_boa(tmp_path)
    ruim = Peca(**{**p.__dict__, "dados": {**p.dados, "intruso": Dado("x", "y")}})
    assert any("intruso" in x for x in validar([ruim]))


def test_validar_recusa_campo_do_molde_que_falta(tmp_path):
    p = _peca_boa(tmp_path)
    sem_preco = {k: v for k, v in p.dados.items() if k != "preco"}
    assert any("preco" in x for x in validar([Peca(**{**p.__dict__, "dados": sem_preco})]))


def test_validar_recusa_strings_impressas_vazia(tmp_path):
    p = _peca_boa(tmp_path)
    assert any("strings_impressas" in x for x in validar([Peca(**{**p.__dict__, "strings_impressas": ()})]))


def test_validar_recusa_molde_desconhecido(tmp_path):
    p = _peca_boa(tmp_path)
    assert any("molde" in x for x in validar([Peca(**{**p.__dict__, "molde": "inventado"})]))


def test_o_catalogo_de_verdade_e_valido():
    """O portao que importa: PECAS declarado no repositorio passa."""
    assert validar(PECAS) == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m uv run pytest tests/test_estaticos_catalogo.py -q`
Expected: FAIL com `ImportError: cannot import name 'DeclaracaoInvalida'`

- [ ] **Step 3: Write minimal implementation**

```python
# acrescentar ao fim de instagram/estaticos/catalogo.py


class DeclaracaoInvalida(Exception):
    """A declaracao nao passa. Levantada por `exigir_valido`, nao por `validar`."""


def validar(pecas: list[Peca]) -> list[str]:
    """Devolve a lista de problemas. Lista vazia significa declaracao valida.

    Devolve em vez de levantar porque o comando `conferir` precisa reportar
    TODOS os problemas de uma vez -- um por linha -- e nao parar no primeiro.
    """
    problemas: list[str] = []
    for p in pecas:
        onde = f"peca {p.slug}"

        molde = MOLDES.get(p.molde)
        if molde is None:
            problemas.append(f"{onde}: molde '{p.molde}' nao existe em MOLDES")
            continue

        if not p.strings_impressas:
            problemas.append(
                f"{onde}: strings_impressas vazia -- sem gabarito nao ha conferencia"
            )

        if not p.fonte.exists():
            problemas.append(f"{onde}: fonte nao existe no disco: {p.fonte}")

        esperados = set(molde.campos)
        declarados = set(p.dados)
        for falta in sorted(esperados - declarados):
            problemas.append(f"{onde}: o molde pede o campo '{falta}' e ele nao foi declarado")
        for sobra in sorted(declarados - esperados):
            problemas.append(f"{onde}: campo '{sobra}' nao pertence ao molde '{p.molde}'")

        for chave in sorted(declarados & esperados):
            d = p.dados[chave]
            if not d.valor.strip():
                problemas.append(f"{onde}: campo '{chave}' com valor vazio")
            if not d.origem.strip():
                problemas.append(
                    f"{onde}: campo '{chave}' sem origem declarada -- ver licao 18"
                )
    return problemas


def exigir_valido(pecas: list[Peca]) -> None:
    problemas = validar(pecas)
    if problemas:
        raise DeclaracaoInvalida("\n".join(problemas))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m uv run pytest tests/test_estaticos_catalogo.py -q`
Expected: PASS, 14 passed

- [ ] **Step 5: Commit**

```bash
git add instagram/estaticos/catalogo.py tests/test_estaticos_catalogo.py
git commit -m "Estaticos: validar() recusa dado sem origem e campo fora do molde"
```

---

## Tarefa 3: `prompt.py` — o bloco de soletração sai da declaração

**Files:**
- Create: `instagram/estaticos/prompt.py`
- Test: `tests/test_estaticos_prompt.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_estaticos_prompt.py
from instagram.estaticos.catalogo import PECAS
from instagram.estaticos.prompt import CORRECOES, montar


def test_toda_string_declarada_aparece_no_prompt():
    """O gabarito e o prompt saem da MESMA fonte. Se divergirem, a conferencia
    passa a cobrar coisa que o prompt nunca pediu."""
    p = PECAS[0]
    texto = montar(p)
    for s in p.strings_impressas:
        assert s in texto, f"{s} declarada e ausente do prompt"


def test_dado_do_codigo_nao_entra_no_prompt():
    """`dados` e desenhado pelo Remotion. Pedir ao modelo para escrever
    `R$ 31,70` e convidar o sosia -- licao 1."""
    texto = montar(PECAS[0])
    assert "31,70" not in texto
    assert "1.250" not in texto


def test_soletracao_separa_por_hifen_quando_pedida():
    texto = montar(PECAS[0], correcoes=("soletrar",))
    assert "S-C-A" in texto or "C-A-N-A-S-T-R-A" in texto


def test_nomear_operacao_abre_o_prompt_com_ordem_de_edicao():
    """Licao 12: com o prompt aberto como ordem de EDICAO, os 3 SKUs sairam
    indistinguiveis da fonte."""
    texto = montar(PECAS[0], correcoes=("nomear-operacao",))
    assert texto.startswith("EDIT THE PROVIDED PHOTOGRAPH")
    assert "KEEP THE PACKAGE PIXEL-FOR-PIXEL IDENTICAL" in texto


def test_aumentar_no_quadro_declara_ocupacao_minima():
    texto = montar(PECAS[0], correcoes=("aumentar-no-quadro",))
    assert "at least 60%" in texto


def test_correcao_desconhecida_levanta():
    import pytest

    with pytest.raises(ValueError, match="inventada"):
        montar(PECAS[0], correcoes=("inventada",))


def test_correcoes_conhecidas_sao_as_da_escada():
    assert CORRECOES == (
        "soletrar",
        "nomear-operacao",
        "ancora-familia",
        "aumentar-no-quadro",
    )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m uv run pytest tests/test_estaticos_prompt.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'instagram.estaticos.prompt'`

- [ ] **Step 3: Write minimal implementation**

```python
# instagram/estaticos/prompt.py
"""Declaracao -> texto do prompt de geracao.

O prompt e em INGLES por decisao do CLAUDE.md: corpo de prompt de imagem em
ingles, porque os modelos respondem melhor.

O QUE ESTE MODULO NAO FAZ: nao escreve `dados`. `R$ 31,70` e `1.250 m` sao
desenhados pelo Remotion. Pedir ao modelo para escrever texto nosso e a licao 1
-- descrever e deixar o modelo desenhar produz um sosia.

As correcoes sao os degraus 1 a 4 da escada. O degrau 5 (`n-variantes`) nao
muda o prompt, muda quantas vezes ele roda; o degrau 6 (`compor`) nao gera.
"""

from __future__ import annotations

from .catalogo import Peca

CORRECOES: tuple[str, ...] = (
    "soletrar",
    "nomear-operacao",
    "ancora-familia",
    "aumentar-no-quadro",
)

_ABERTURA_EDICAO = (
    "EDIT THE PROVIDED PHOTOGRAPH. KEEP THE PACKAGE PIXEL-FOR-PIXEL IDENTICAL: "
    "same position, same scale, same crop, same creases, same specular highlights. "
    "Change only the surrounding scene."
)


def _soletrar(s: str) -> str:
    """`SCA 80+` -> `"SCA 80+" (S-C-A space eight zero plus)`.

    Soletra so letra e digito; pontuacao fica por extenso em ingles porque e
    assim que o `lateral_extra` de prompts_catalogo.py faz, e aquele formato ja
    corrigiu o `70 / 80 / 80 / 40` na pratica.
    """
    nomes = {" ": "space", "+": "plus", ",": "comma", ".": "dot", "-": "dash"}
    partes = [nomes.get(c, c) for c in s]
    return f'"{s}" ({"-".join(partes)})'


def montar(peca: Peca, correcoes: tuple[str, ...] = ()) -> str:
    for c in correcoes:
        if c not in CORRECOES:
            raise ValueError(
                f"correcao '{c}' nao existe. Validas: {', '.join(CORRECOES)}"
            )

    blocos: list[str] = []

    if "nomear-operacao" in correcoes:
        blocos.append(_ABERTURA_EDICAO)
    else:
        blocos.append(
            "Photograph of the provided coffee package in a new setting. "
            "The package artwork must be reproduced exactly as in the reference."
        )

    ocupacao = "at least 60%" if "aumentar-no-quadro" in correcoes else "about 45%"
    blocos.append(f"The package occupies {ocupacao} of the frame height.")

    if "soletrar" in correcoes:
        itens = "; ".join(_soletrar(s) for s in peca.strings_impressas)
        blocos.append(
            "The front panel carries exactly these strings, character for "
            f"character, with every accent: {itens}."
        )
    else:
        itens = "; ".join(f'"{s}"' for s in peca.strings_impressas)
        blocos.append(f"The front panel carries exactly these strings: {itens}.")

    if "ancora-familia" in correcoes:
        blocos.append(
            "Two reference images are provided. The FIRST defines the artwork and "
            "every printed string. The SECOND defines only material, lighting and "
            "pose. Where they disagree about text, the first wins."
        )

    blocos.append(
        "Phone-camera look: small sensor, deep focus, everything equally sharp, "
        "soft corners, washed saturation. No shallow depth of field, no bokeh."
    )
    blocos.append(
        "Do NOT render any batch code, manufacturing date, expiry date, QR code "
        "or barcode. Leave those out of frame."
    )

    return " ".join(blocos)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m uv run pytest tests/test_estaticos_prompt.py -q`
Expected: PASS, 7 passed

- [ ] **Step 5: Commit**

```bash
git add instagram/estaticos/prompt.py tests/test_estaticos_prompt.py
git commit -m "Estaticos: prompt sai da declaracao, com soletracao por degrau"
```

---

## Tarefa 4: `escada.py` — roteamento sintoma → degrau

**Files:**
- Create: `instagram/estaticos/escada.py`
- Test: `tests/test_estaticos_escada.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_estaticos_escada.py
import pytest

from instagram.estaticos.escada import DEGRAUS, SINTOMAS, esgotou, rotear


def test_cada_sintoma_aponta_para_um_degrau_que_existe():
    for sintoma, degrau in SINTOMAS.items():
        assert degrau in DEGRAUS, f"{sintoma} aponta para degrau {degrau} inexistente"


@pytest.mark.parametrize(
    "sintoma,degrau",
    [
        ("valor-inventado", 1),
        ("acento-perdido", 1),
        ("rotulo-generico", 2),
        ("fonte-ruim", 3),
        ("letra-corrompida", 4),
        ("erro-intermitente", 5),
        ("carimbo-variavel", 6),
        ("codigo-2d", 6),
    ],
)
def test_roteamento_e_determinstico(sintoma, degrau):
    assert rotear([sintoma]) == (degrau,)


def test_sintomas_distintos_acumulam_degraus_ordenados():
    """Uma regeracao pode carregar mais de uma correcao ao mesmo tempo."""
    assert rotear(["letra-corrompida", "valor-inventado"]) == (1, 4)


def test_sintoma_repetido_nao_duplica_degrau():
    assert rotear(["valor-inventado", "acento-perdido"]) == (1,)


def test_sintoma_desconhecido_levanta_em_vez_de_adivinhar():
    with pytest.raises(KeyError, match="nao-catalogado"):
        rotear(["nao-catalogado"])


def test_lista_vazia_nao_roteia_nada():
    assert rotear([]) == ()


def test_esgotou_e_verdade_quando_algum_sintoma_vai_direto_ao_degrau_6():
    assert esgotou(["carimbo-variavel"]) is True
    assert esgotou(["codigo-2d"]) is True
    assert esgotou(["valor-inventado"]) is False
    assert esgotou(["valor-inventado", "codigo-2d"]) is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m uv run pytest tests/test_estaticos_escada.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'instagram.estaticos.escada'`

- [ ] **Step 3: Write minimal implementation**

```python
# instagram/estaticos/escada.py
"""A escada de correcao: sintoma -> degrau, e o laco com teto.

CADA LINHA DE `SINTOMAS` E UMA FALHA JA PAGA NESTE REPOSITORIO. A tabela nao
foi projetada, foi colhida do `Registro de licoes` do CLAUDE.md.

O degrau 6 nao e fracasso do laco: e o seu piso. Ele nao depende do modelo, e
e por isso que o laco termina. A licao 13 registra que abaixo de ~2% da altura
do quadro a tipografia nao sobrevive em NENHUMA rodada -- para esses campos,
insistir em prompt so gasta.
"""

from __future__ import annotations

DEGRAUS: dict[int, str] = {
    1: "soletrar",
    2: "nomear-operacao",
    3: "ancora-familia",
    4: "aumentar-no-quadro",
    5: "n-variantes",
    6: "compor",
}

SINTOMAS: dict[str, int] = {
    # licao 18: saiu `70 / 80 / 80 / 40` onde era 7,0 / 10 / 10 / 6,0
    "valor-inventado": 1,
    # licao 21: `ARABICA` por `ARÁBICA`, `DOCURA` por `DOÇURA`
    "acento-perdido": 1,
    # licoes 1 e 12: referencia errada ou prompt que nao nomeia a operacao
    "rotulo-generico": 2,
    # canastra-embalagem: capsulas Suave chegaram em 591x1280
    "fonte-ruim": 3,
    # licao 13: `Doodo 1985`, `TRODULB E HÚMO`
    "letra-corrompida": 4,
    # site_fundo_branco.py: erra ~1 em 3 mesmo com tudo soletrado
    "erro-intermitente": 5,
    # licao 22: `F:23.2025`, um mes que nao existe -- e o plausivel e pior
    "carimbo-variavel": 6,
    # canastra-conteudo: QR e codigo de barras sao sempre regenerados
    "codigo-2d": 6,
}

ULTIMO_DEGRAU = 6


def rotear(sintomas: list[str]) -> tuple[int, ...]:
    """Sintomas -> degraus a aplicar, ordenados e sem repeticao.

    Sintoma fora do catalogo levanta `KeyError`. Nao se adivinha degrau: um
    sintoma novo e um item novo no registro de licoes, nao um palpite aqui.
    """
    degraus = set()
    for s in sintomas:
        if s not in SINTOMAS:
            raise KeyError(
                f"sintoma '{s}' nao esta catalogado em SINTOMAS. "
                "Acrescente a linha com a licao que o originou."
            )
        degraus.add(SINTOMAS[s])
    return tuple(sorted(degraus))


def esgotou(sintomas: list[str]) -> bool:
    """Algum sintoma vai direto ao ultimo degrau, sem passar por geracao?"""
    return ULTIMO_DEGRAU in rotear(sintomas)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m uv run pytest tests/test_estaticos_escada.py -q`
Expected: PASS, 14 passed

- [ ] **Step 5: Commit**

```bash
git add instagram/estaticos/escada.py tests/test_estaticos_escada.py
git commit -m "Estaticos: escada de correcao, uma linha por licao paga"
```

---

## Tarefa 5: o laço com teto, provado com gerador falso

**Files:**
- Modify: `instagram/estaticos/escada.py` (acrescenta `Resultado` e `executar`)
- Test: `tests/test_estaticos_escada.py` (acrescenta)

- [ ] **Step 1: Write the failing test**

```python
# acrescentar a tests/test_estaticos_escada.py
from instagram.estaticos.escada import Resultado, executar


def test_passa_na_primeira_quando_nao_ha_falha():
    chamadas = []

    def gerar(correcoes):
        chamadas.append(correcoes)
        return "img1"

    r = executar(gerar=gerar, conferir=lambda img: [], compor=lambda s: "nunca")
    assert isinstance(r, Resultado)
    assert r.imagem == "img1"
    assert r.tentativas == 1
    assert r.degraus == ()
    assert r.composto is False
    assert chamadas == [()]


def test_corrige_e_passa_na_segunda():
    vistos = []

    def gerar(correcoes):
        vistos.append(correcoes)
        return f"img{len(vistos)}"

    def conferir(img):
        return ["valor-inventado"] if img == "img1" else []

    r = executar(gerar=gerar, conferir=conferir, compor=lambda s: "nunca")
    assert r.imagem == "img2"
    assert r.tentativas == 2
    assert r.degraus == ("soletrar",)
    assert r.composto is False
    assert vistos == [(), ("soletrar",)]


def test_respeita_o_teto_e_cai_para_composicao():
    """Gerador que SEMPRE erra: o laco nao pode rodar para sempre."""
    n = []

    def gerar(correcoes):
        n.append(correcoes)
        return "ruim"

    r = executar(
        gerar=gerar,
        conferir=lambda img: ["valor-inventado"],
        compor=lambda sintomas: "composta",
        teto=3,
    )
    assert len(n) == 3, "gerou mais vezes que o teto"
    assert r.imagem == "composta"
    assert r.composto is True
    assert r.tentativas == 3


def test_sintoma_de_degrau_6_vai_direto_a_composicao_sem_gastar_rodada():
    """Carimbo de lote nao se conserta por prompt. Licao 22."""
    n = []

    def gerar(correcoes):
        n.append(correcoes)
        return "img"

    r = executar(
        gerar=gerar,
        conferir=lambda img: ["carimbo-variavel"],
        compor=lambda sintomas: "composta",
        teto=3,
    )
    assert len(n) == 1, "gastou rodada num sintoma que a escada manda compor"
    assert r.composto is True


def test_degraus_acumulados_aparecem_no_resultado():
    seq = [["letra-corrompida"], ["valor-inventado"], []]

    def conferir(img):
        return seq.pop(0)

    r = executar(gerar=lambda c: "i", conferir=conferir, compor=lambda s: "c")
    assert r.degraus == ("aumentar-no-quadro", "soletrar")
    assert r.composto is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m uv run pytest tests/test_estaticos_escada.py -q`
Expected: FAIL com `ImportError: cannot import name 'Resultado'`

- [ ] **Step 3: Write minimal implementation**

```python
# acrescentar ao fim de instagram/estaticos/escada.py

from dataclasses import dataclass, field
from typing import Callable

TETO_PADRAO = 3


@dataclass
class Resultado:
    imagem: object
    tentativas: int
    degraus: tuple[str, ...]
    composto: bool
    sintomas_finais: tuple[str, ...] = field(default=())


def executar(
    gerar: Callable[[tuple[str, ...]], object],
    conferir: Callable[[object], list[str]],
    compor: Callable[[list[str]], object],
    teto: int = TETO_PADRAO,
) -> Resultado:
    """Gera, confere, corrige, repete -- e termina sempre.

    `gerar`, `conferir` e `compor` sao INJETADOS, nao importados. E o que
    permite provar o laco sem abrir navegador: os testes passam funcoes falsas.
    `gerar` recebe os nomes das correcoes; `conferir` devolve lista de sintomas.

    A terminacao nao depende do modelo cooperar: ou a conferencia passa, ou o
    teto estoura, ou um sintoma de degrau 6 aparece -- e os tres caminhos saem.
    """
    correcoes: tuple[str, ...] = ()
    aplicados: set[str] = set()
    tentativa = 0
    sintomas: list[str] = []

    while tentativa < teto:
        imagem = gerar(correcoes)
        tentativa += 1
        sintomas = conferir(imagem)

        if not sintomas:
            return Resultado(
                imagem=imagem,
                tentativas=tentativa,
                degraus=tuple(sorted(aplicados)),
                composto=False,
            )

        degraus = rotear(sintomas)
        if ULTIMO_DEGRAU in degraus:
            break

        aplicados.update(DEGRAUS[d] for d in degraus)
        # `n-variantes` nao e correcao de prompt: ela muda quantas vezes gerar.
        correcoes = tuple(
            sorted(c for c in aplicados if c != DEGRAUS[5])
        )

    return Resultado(
        imagem=compor(sintomas),
        tentativas=tentativa,
        degraus=tuple(sorted(aplicados | {DEGRAUS[ULTIMO_DEGRAU]})),
        composto=True,
        sintomas_finais=tuple(sintomas),
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m uv run pytest tests/test_estaticos_escada.py -q`
Expected: PASS, 19 passed

> Se `test_corrige_e_passa_na_segunda` falhar porque `r.degraus` veio `("soletrar",)` e o esperado era outra ordem, o conserto é no teste, não no código: `degraus` é ordenado alfabeticamente de propósito, para o sidecar ser diffável.

- [ ] **Step 5: Commit**

```bash
git add instagram/estaticos/escada.py tests/test_estaticos_escada.py
git commit -m "Estaticos: laco com teto que termina sempre, provado com gerador falso"
```

---

## Tarefa 6: `conferir.py` — recorte ampliado dos dois lados

**Files:**
- Create: `instagram/estaticos/conferir.py`
- Test: `tests/test_estaticos_conferir.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_estaticos_conferir.py
import pytest
from PIL import Image

from instagram.estaticos.conferir import VEREDITOS, bloqueia, recortes


def _png(tmp_path, nome, tamanho=(400, 500), cor=(120, 90, 60)):
    p = tmp_path / nome
    Image.new("RGB", tamanho, cor).save(p)
    return p


def test_grava_um_par_de_recortes_por_string(tmp_path):
    gerada = _png(tmp_path, "g.png")
    ref = _png(tmp_path, "r.png")
    faixas = {"SCA 80+": (10, 20, 110, 60), "250g": (10, 80, 90, 120)}

    pares = recortes(gerada, ref, faixas, tmp_path / "out")

    assert set(pares) == {"SCA 80+", "250g"}
    for nome, (a, b) in pares.items():
        assert a.exists() and b.exists(), f"{nome}: faltou um dos lados"
        assert a != b


def test_amplia_pelo_fator_declarado(tmp_path):
    gerada = _png(tmp_path, "g.png")
    ref = _png(tmp_path, "r.png")
    pares = recortes(gerada, ref, {"x": (0, 0, 50, 25)}, tmp_path / "out", fator=4)

    with Image.open(pares["x"][0]) as im:
        assert im.size == (200, 100)


def test_nome_de_arquivo_e_seguro_para_string_com_simbolo(tmp_path):
    """`SCA 80+` nao pode virar caminho invalido no Windows."""
    gerada = _png(tmp_path, "g.png")
    ref = _png(tmp_path, "r.png")
    pares = recortes(gerada, ref, {"SCA 80+": (0, 0, 50, 25)}, tmp_path / "out")
    for p in pares["SCA 80+"]:
        assert "+" not in p.name
        assert " " not in p.name


def test_faixa_fora_da_imagem_levanta_em_vez_de_recortar_vazio(tmp_path):
    gerada = _png(tmp_path, "g.png", tamanho=(100, 100))
    ref = _png(tmp_path, "r.png", tamanho=(100, 100))
    with pytest.raises(ValueError, match="fora"):
        recortes(gerada, ref, {"x": (50, 50, 300, 300)}, tmp_path / "out")


def test_vereditos_sao_os_tres_de_canastra_conteudo():
    assert VEREDITOS == ("ok", "errado", "nao-verificavel")


def test_nao_verificavel_bloqueia_e_ok_nao():
    """Licao 18: ilegivel nao e 'confere'. Nao verificavel barra a peca."""
    assert bloqueia({"a": "ok", "b": "ok"}) == ()
    assert bloqueia({"a": "ok", "b": "nao-verificavel"}) == ("b",)
    assert bloqueia({"a": "errado"}) == ("a",)
    assert bloqueia({"a": "errado", "b": "nao-verificavel"}) == ("a", "b")


def test_veredito_invalido_levanta():
    with pytest.raises(ValueError, match="confere"):
        bloqueia({"a": "confere"})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m uv run pytest tests/test_estaticos_conferir.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'instagram.estaticos.conferir'`

- [ ] **Step 3: Write minimal implementation**

```python
# instagram/estaticos/conferir.py
"""Produz o material da conferencia. Nao emite veredito -- quem le e o agente.

POR QUE SO OS RECORTES. O que falha hoje nao e a leitura, e a oportunidade de
ler: em miniatura, erro de letra desaparece. `canastra-conteudo` fase 4 manda
recortar a faixa de texto e ampliar com LANCZOS antes de opinar, e manda
ampliar A REFERENCIA TAMBEM -- conferencia e comparacao entre dois recortes,
nunca entre um recorte e a memoria de quem olha.

Este modulo automatiza exatamente essa mecanica, e nada alem dela. Decidir se
`SCA 80+` saiu certo continua sendo trabalho de olho.
"""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

VEREDITOS: tuple[str, ...] = ("ok", "errado", "nao-verificavel")

FATOR_PADRAO = 4


def _slug(s: str) -> str:
    """`SCA 80+` -> `sca-80`. Windows nao aceita todo simbolo em nome de arquivo."""
    limpo = re.sub(r"[^0-9a-zA-Z]+", "-", s).strip("-").lower()
    return limpo or "campo"


def recortes(
    gerada: Path,
    referencia: Path,
    faixas: dict[str, tuple[int, int, int, int]],
    destino: Path,
    fator: int = FATOR_PADRAO,
) -> dict[str, tuple[Path, Path]]:
    """Para cada string, grava o recorte ampliado da gerada E da referencia.

    `faixas` mapeia a string declarada para `(x0, y0, x1, y1)`. Devolve
    `{string: (caminho_gerada, caminho_referencia)}`.
    """
    destino.mkdir(parents=True, exist_ok=True)
    saida: dict[str, tuple[Path, Path]] = {}

    with Image.open(gerada) as g, Image.open(referencia) as r:
        for nome, caixa in faixas.items():
            x0, y0, x1, y1 = caixa
            for rotulo, im in (("gerada", g), ("referencia", r)):
                if x1 > im.width or y1 > im.height or x0 < 0 or y0 < 0:
                    raise ValueError(
                        f"faixa de '{nome}' {caixa} cai fora da {rotulo} "
                        f"({im.width}x{im.height})"
                    )

            par = []
            for rotulo, im in (("gerada", g), ("referencia", r)):
                c = im.crop(caixa)
                c = c.resize((c.width * fator, c.height * fator), Image.LANCZOS)
                p = destino / f"{_slug(nome)}-{rotulo}.png"
                c.save(p)
                par.append(p)
            saida[nome] = (par[0], par[1])

    return saida


def bloqueia(vereditos: dict[str, str]) -> tuple[str, ...]:
    """Quais campos barram a peca. `nao-verificavel` barra junto com `errado`.

    Isto e a licao 18 virada em codigo: um agente aprovou campo fisicamente
    ilegivel dizendo que "bate com a foto real". Ilegivel nao e aprovacao, e
    ausencia de leitura -- entao nao pode sair pela mesma porta que `ok`.
    """
    for campo, v in vereditos.items():
        if v not in VEREDITOS:
            raise ValueError(
                f"veredito '{v}' no campo '{campo}' nao existe. "
                f"Validos: {', '.join(VEREDITOS)}. "
                "Em particular 'confere' nao e veredito: use 'ok'."
            )
    return tuple(sorted(c for c, v in vereditos.items() if v != "ok"))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m uv run pytest tests/test_estaticos_conferir.py -q`
Expected: PASS, 7 passed

- [ ] **Step 5: Commit**

```bash
git add instagram/estaticos/conferir.py tests/test_estaticos_conferir.py
git commit -m "Estaticos: recorte ampliado dos dois lados; nao-verificavel bloqueia"
```

---

## Tarefa 7: `compor.py` — o degrau 6 com laudo que não é tautológico

**Files:**
- Create: `instagram/estaticos/compor.py`
- Test: `tests/test_estaticos_compor.py`

Leia **R1** no topo deste plano antes de começar.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_estaticos_compor.py
import numpy as np
import pytest
from PIL import Image

from instagram.estaticos.compor import colar_rotulo


def _rgba(tamanho, cor, alfa=255):
    im = Image.new("RGBA", tamanho, (*cor, alfa))
    return im


def test_cola_o_recorte_na_caixa_e_o_laudo_aprova(tmp_path):
    peca = Image.new("RGB", (200, 250), (10, 10, 10))
    recorte = _rgba((40, 50), (200, 150, 100))

    final, laudo = colar_rotulo(peca, recorte, caixa=(20, 30, 60, 80))

    assert final.size == (200, 250)
    assert laudo["aprovado"] is True
    assert laudo["pixels_alterados"] == 0
    assert laudo["alfa_minimo_no_rotulo"] == 255
    # o pixel colado e o do recorte, nao o do fundo
    assert final.convert("RGB").getpixel((21, 31)) == (200, 150, 100)


def test_fora_da_caixa_nada_muda(tmp_path):
    peca = Image.new("RGB", (200, 250), (10, 20, 30))
    antes = np.array(peca)
    final, _ = colar_rotulo(peca, _rgba((40, 50), (9, 9, 9)), caixa=(20, 30, 60, 80))
    depois = np.array(final.convert("RGB"))

    mascara = np.ones(antes.shape[:2], bool)
    mascara[30:80, 20:60] = False
    assert np.array_equal(antes[mascara], depois[mascara])


def test_o_laudo_NAO_e_tautologico(tmp_path):
    """O portao que protege contra o bug de verificar.py.

    Se alguem implementar comparando a peca consigo mesma, este teste passa a
    aprovar uma colagem corrompida. Aqui a colagem e sabotada de proposito: o
    laudo TEM que reprovar.
    """
    peca = Image.new("RGB", (100, 100), (0, 0, 0))
    recorte = _rgba((20, 20), (255, 255, 255))

    final, laudo = colar_rotulo(
        peca, recorte, caixa=(10, 10, 30, 30), _sabotar=True
    )
    assert laudo["aprovado"] is False
    assert laudo["pixels_alterados"] > 0


def test_recorte_com_alfa_parcial_no_rotulo_reprova():
    """Tipografia impressa nao admite transparencia parcial."""
    peca = Image.new("RGB", (100, 100), (0, 0, 0))
    recorte = _rgba((20, 20), (255, 255, 255), alfa=200)
    _, laudo = colar_rotulo(peca, recorte, caixa=(10, 10, 30, 30))
    assert laudo["alfa_minimo_no_rotulo"] == 200
    assert laudo["aprovado"] is False


def test_reamostragem_e_comparada_contra_a_mesma_reamostragem():
    """Se o recorte precisa encolher, o laudo compara contra o recorte JA
    encolhido -- nao contra o original, que daria falso negativo garantido."""
    peca = Image.new("RGB", (100, 100), (0, 0, 0))
    recorte = _rgba((80, 80), (123, 45, 67))
    _, laudo = colar_rotulo(peca, recorte, caixa=(10, 10, 30, 30))
    assert laudo["aprovado"] is True
    assert laudo["reamostrado"] == [80, 80, 20, 20]


def test_caixa_fora_da_peca_levanta():
    peca = Image.new("RGB", (50, 50), (0, 0, 0))
    with pytest.raises(ValueError, match="fora"):
        colar_rotulo(peca, _rgba((10, 10), (1, 2, 3)), caixa=(40, 40, 90, 90))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m uv run pytest tests/test_estaticos_compor.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'instagram.estaticos.compor'`

- [ ] **Step 3: Write minimal implementation**

```python
# instagram/estaticos/compor.py
"""Degrau 6: cola o pixel real do rotulo e PROVA que ele chegou intacto.

ATENCAO AO LAUDO -- leia antes de mexer. `instagram/recorte/verificar.py`
documenta, em comentario proprio, que o `pixels_alterados` dele da 0 por
construcao no fluxo de recorte: `matte.recortar` devolve o RGB de entrada sem
tocar em nada, entao comparar entrada com saida nao pode acusar nada. Foi
assim que um SKU saiu `aprovado=true` carregando um naco de parede.

AQUI A COMPARACAO VALE, e vale por um motivo especifico: origem e o recorte
real JA REAMOSTRADO para o tamanho da caixa, e saida e a regiao correspondente
da peca final. Sao dois arrays de proveniencia diferente. Se alguem trocar a
origem pela propria peca, o laudo volta a ser teatro -- e o teste
`test_o_laudo_NAO_e_tautologico` existe para pegar exatamente isso.
"""

from __future__ import annotations

import numpy as np
from PIL import Image

from instagram.recorte.verificar import laudo_preservacao


def colar_rotulo(
    peca: Image.Image,
    recorte: Image.Image,
    caixa: tuple[int, int, int, int],
    _sabotar: bool = False,
) -> tuple[Image.Image, dict]:
    """Cola `recorte` (RGBA) em `caixa` da `peca` e devolve `(final, laudo)`.

    `_sabotar` corrompe a colagem de proposito e existe so para o teste que
    prova que o laudo nao e tautologico. Nunca use em producao.
    """
    x0, y0, x1, y1 = caixa
    if x0 < 0 or y0 < 0 or x1 > peca.width or y1 > peca.height:
        raise ValueError(
            f"caixa {caixa} cai fora da peca ({peca.width}x{peca.height})"
        )

    largura, altura = x1 - x0, y1 - y0
    origem_tamanho = list(recorte.size)

    fonte = recorte
    if fonte.size != (largura, altura):
        fonte = fonte.resize((largura, altura), Image.LANCZOS)

    final = peca.convert("RGBA").copy()
    final.alpha_composite(fonte, dest=(x0, y0))

    if _sabotar:
        px = final.load()
        for i in range(x0, x1):
            for j in range(y0, y1):
                px[i, j] = (0, 0, 0, 255)

    # ORIGEM = o recorte reamostrado. SAIDA = a regiao da peca final.
    # Sao arrays distintos; o laudo tem o que comparar.
    rgb_origem = np.array(fonte.convert("RGB"))
    rgb_saida = np.array(final.crop(caixa).convert("RGB"))
    alfa = np.array(fonte.split()[-1])

    laudo = laudo_preservacao(
        rgb_origem,
        rgb_saida,
        alfa,
        tolerancia=0,
        retangulo_rotulo=(0, 0, largura, altura),
    )
    laudo["reamostrado"] = origem_tamanho + [largura, altura]
    return final, laudo
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m uv run pytest tests/test_estaticos_compor.py -q`
Expected: PASS, 6 passed

- [ ] **Step 5: Commit**

```bash
git add instagram/estaticos/compor.py tests/test_estaticos_compor.py
git commit -m "Estaticos: degrau 6 cola pixel real, com laudo que compara arrays distintos"
```

---

## Tarefa 8: `bundle.py` — a pasta de saída e o sidecar

**Files:**
- Create: `instagram/estaticos/bundle.py`
- Modify: `.gitignore` (acrescenta `saida-estaticos/`)
- Test: `tests/test_estaticos_bundle.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_estaticos_bundle.py
import json

import pytest
from PIL import Image

from instagram.estaticos.bundle import BundleBloqueado, escrever
from instagram.estaticos.catalogo import PECAS


def _peca_png(tmp_path):
    p = tmp_path / "peca.png"
    Image.new("RGB", (1080, 1350), (20, 20, 20)).save(p)
    return p


def test_escreve_as_tres_coisas(tmp_path):
    destino = escrever(
        peca=PECAS[0],
        png=_peca_png(tmp_path),
        legenda="rascunho de legenda",
        vereditos={s: "ok" for s in PECAS[0].strings_impressas},
        degraus=("soletrar",),
        tentativas=2,
        laudo={"pixels_alterados": 0, "aprovado": True},
        raiz=tmp_path / "saida",
        data="2026-10-02",
    )
    assert (destino / "peca.png").exists()
    assert (destino / "legenda.txt").read_text(encoding="utf-8") == "rascunho de legenda"
    assert (destino / "sidecar.json").exists()


def test_a_pasta_carrega_data_e_slug(tmp_path):
    destino = escrever(
        peca=PECAS[0], png=_peca_png(tmp_path), legenda="x",
        vereditos={s: "ok" for s in PECAS[0].strings_impressas},
        degraus=(), tentativas=1, laudo={"aprovado": True},
        raiz=tmp_path / "saida", data="2026-10-02",
    )
    assert destino.name == "2026-10-02-cartao-classico-250g-graos"


def test_sidecar_registra_proveniencia_e_a_origem_de_cada_dado(tmp_path):
    destino = escrever(
        peca=PECAS[0], png=_peca_png(tmp_path), legenda="x",
        vereditos={s: "ok" for s in PECAS[0].strings_impressas},
        degraus=("soletrar", "compor"), tentativas=3,
        laudo={"pixels_alterados": 0, "aprovado": True},
        raiz=tmp_path / "saida", data="2026-10-02",
    )
    s = json.loads((destino / "sidecar.json").read_text(encoding="utf-8"))

    assert s["slug"] == "cartao-classico-250g-graos"
    assert s["molde"] == "cartao-produto"
    assert len(s["fonte_sha256"]) == 64
    assert s["strings_esperadas"] == list(PECAS[0].strings_impressas)
    assert s["degraus"] == ["soletrar", "compor"]
    assert s["tentativas"] == 3
    assert s["laudo"]["aprovado"] is True
    # a origem de cada dado viaja com a peca
    assert s["dados"]["preco"]["valor"] == "R$ 31,70"
    assert "11/09/2026" in s["dados"]["preco"]["origem"]


def test_campo_nao_verificavel_bloqueia_o_bundle(tmp_path):
    vereditos = {s: "ok" for s in PECAS[0].strings_impressas}
    vereditos["SCA 80+"] = "nao-verificavel"
    with pytest.raises(BundleBloqueado, match="SCA 80"):
        escrever(
            peca=PECAS[0], png=_peca_png(tmp_path), legenda="x",
            vereditos=vereditos, degraus=(), tentativas=1,
            laudo={"aprovado": True}, raiz=tmp_path / "saida", data="2026-10-02",
        )


def test_veredito_faltando_para_string_declarada_bloqueia(tmp_path):
    parcial = {s: "ok" for s in PECAS[0].strings_impressas[:-1]}
    with pytest.raises(BundleBloqueado, match="sem veredito"):
        escrever(
            peca=PECAS[0], png=_peca_png(tmp_path), legenda="x",
            vereditos=parcial, degraus=(), tentativas=1,
            laudo={"aprovado": True}, raiz=tmp_path / "saida", data="2026-10-02",
        )


def test_laudo_reprovado_bloqueia(tmp_path):
    with pytest.raises(BundleBloqueado, match="laudo"):
        escrever(
            peca=PECAS[0], png=_peca_png(tmp_path), legenda="x",
            vereditos={s: "ok" for s in PECAS[0].strings_impressas},
            degraus=("compor",), tentativas=3,
            laudo={"pixels_alterados": 12, "aprovado": False},
            raiz=tmp_path / "saida", data="2026-10-02",
        )


def test_dimensao_errada_bloqueia(tmp_path):
    ruim = tmp_path / "ruim.png"
    Image.new("RGB", (1080, 1349), (0, 0, 0)).save(ruim)
    with pytest.raises(BundleBloqueado, match="1080x1350"):
        escrever(
            peca=PECAS[0], png=ruim, legenda="x",
            vereditos={s: "ok" for s in PECAS[0].strings_impressas},
            degraus=(), tentativas=1, laudo={"aprovado": True},
            raiz=tmp_path / "saida", data="2026-10-02",
        )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m uv run pytest tests/test_estaticos_bundle.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'instagram.estaticos.bundle'`

- [ ] **Step 3: Write minimal implementation**

```python
# instagram/estaticos/bundle.py
"""A pasta de saida e o sidecar.

O sidecar responde "de onde veio isto" sem abrir o historico do git: fonte com
sha256, strings esperadas, veredito por campo, degraus percorridos e o laudo.
A ORIGEM DE CADA DADO VIAJA JUNTO -- e o que permite, seis meses depois,
saber que `R$ 31,70` veio da tabela de 11/09/2026 e nao da memoria de alguem.

Quando o degrau 6 roda, parte do rotulo e pixel composto e nao saida do
modelo. O sidecar declara isso em `degraus`; nao se esconde.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

from .catalogo import MOLDES, Peca
from .conferir import bloqueia


class BundleBloqueado(Exception):
    """A peca nao vira pasta. Bloqueio, nao aviso."""


def _sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def escrever(
    peca: Peca,
    png: Path,
    legenda: str,
    vereditos: dict[str, str],
    degraus: tuple[str, ...],
    tentativas: int,
    laudo: dict,
    raiz: Path,
    data: str,
) -> Path:
    faltando = [s for s in peca.strings_impressas if s not in vereditos]
    if faltando:
        raise BundleBloqueado(
            f"string declarada sem veredito: {', '.join(faltando)}"
        )

    barrados = bloqueia(vereditos)
    if barrados:
        raise BundleBloqueado(
            "campos barram a peca (errado ou nao-verificavel): "
            + ", ".join(barrados)
        )

    if not laudo.get("aprovado", False):
        raise BundleBloqueado(f"laudo reprovado: {laudo}")

    molde = MOLDES[peca.molde]
    with Image.open(png) as im:
        if im.size != (molde.largura, molde.altura):
            raise BundleBloqueado(
                f"peca e {im.width}x{im.height}; o molde '{peca.molde}' exige "
                f"{molde.largura}x{molde.altura}"
            )

    destino = raiz / f"{data}-{peca.slug}"
    destino.mkdir(parents=True, exist_ok=True)

    destino.joinpath("peca.png").write_bytes(png.read_bytes())
    destino.joinpath("legenda.txt").write_text(legenda, encoding="utf-8")

    sidecar = {
        "slug": peca.slug,
        "molde": peca.molde,
        "fonte": str(peca.fonte),
        "fonte_sha256": _sha256(peca.fonte),
        "strings_esperadas": list(peca.strings_impressas),
        "conferencia": dict(vereditos),
        "dados": {
            k: {"valor": d.valor, "origem": d.origem} for k, d in peca.dados.items()
        },
        "degraus": list(degraus),
        "tentativas": tentativas,
        "laudo": laudo,
        "gerado_em": data,
    }
    destino.joinpath("sidecar.json").write_text(
        json.dumps(sidecar, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    return destino
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m uv run pytest tests/test_estaticos_bundle.py -q`
Expected: PASS, 7 passed

- [ ] **Step 5: Ignorar a saída**

```bash
printf '\n# Bundles de estatico: peca, legenda e sidecar. Saida, nao fonte.\nsaida-estaticos/\n' >> .gitignore
```

- [ ] **Step 6: Commit**

```bash
git add instagram/estaticos/bundle.py tests/test_estaticos_bundle.py .gitignore
git commit -m "Estaticos: bundle com sidecar; veredito faltante ou ilegivel bloqueia"
```

---

## Tarefa 9: `cli.py` — a linha de comando

**Files:**
- Create: `instagram/estaticos/cli.py`
- Create: `instagram/estaticos/__main__.py`
- Test: `tests/test_estaticos_cli.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_estaticos_cli.py
from instagram.estaticos.cli import main


def test_conferir_aprova_o_catalogo_do_repositorio(capsys):
    assert main(["conferir"]) == 0
    assert "ok" in capsys.readouterr().out.lower()


def test_prompt_imprime_o_prompt_da_peca(capsys):
    assert main(["prompt", "cartao-classico-250g-graos"]) == 0
    saida = capsys.readouterr().out
    assert "SCA 80+" in saida
    assert "31,70" not in saida


def test_prompt_aceita_correcao(capsys):
    assert main(["prompt", "cartao-classico-250g-graos", "--correcao", "soletrar"]) == 0
    assert "-" in capsys.readouterr().out


def test_slug_desconhecido_devolve_2(capsys):
    assert main(["prompt", "nao-existe"]) == 2
    assert "nao-existe" in capsys.readouterr().err


def test_correcao_invalida_devolve_2(capsys):
    assert main(["prompt", "cartao-classico-250g-graos", "--correcao", "xpto"]) == 2
    assert "xpto" in capsys.readouterr().err


def test_listar_mostra_os_slugs(capsys):
    assert main(["listar"]) == 0
    assert "cartao-classico-250g-graos" in capsys.readouterr().out
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m uv run pytest tests/test_estaticos_cli.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'instagram.estaticos.cli'`

- [ ] **Step 3: Write minimal implementation**

```python
# instagram/estaticos/cli.py
"""Linha de comando do motor de estaticos.

    python -m instagram.estaticos conferir
    python -m instagram.estaticos listar
    python -m instagram.estaticos prompt <slug> [--correcao soletrar ...]

`conferir` devolve 1 quando a declaracao tem problema -- de proposito, para
quebrar qualquer script que ignore o relatorio e siga gerando.
"""

from __future__ import annotations

import argparse
import sys

from .catalogo import PECAS, validar
from .prompt import CORRECOES, montar


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m instagram.estaticos")
    sub = p.add_subparsers(dest="comando", required=True)

    sub.add_parser("conferir", help="valida a declaracao sem gerar nada")
    sub.add_parser("listar", help="lista os slugs declarados")

    pr = sub.add_parser("prompt", help="imprime o prompt de uma peca")
    pr.add_argument("slug")
    pr.add_argument(
        "--correcao", action="append", default=[], choices=list(CORRECOES),
        help="degrau de correcao a aplicar; pode repetir",
    )

    a = p.parse_args(argv)

    if a.comando == "conferir":
        problemas = validar(PECAS)
        if problemas:
            for x in problemas:
                print(x, file=sys.stderr)
            return 1
        print(f"ok: {len(PECAS)} peca(s) declarada(s), nenhum problema")
        return 0

    if a.comando == "listar":
        for peca in PECAS:
            print(f"{peca.slug}\t{peca.molde}")
        return 0

    por_slug = {peca.slug: peca for peca in PECAS}
    peca = por_slug.get(a.slug)
    if peca is None:
        print(
            f"slug '{a.slug}' nao existe. Validos: {', '.join(sorted(por_slug))}",
            file=sys.stderr,
        )
        return 2
    try:
        print(montar(peca, tuple(a.correcao)))
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    return 0
```

```python
# instagram/estaticos/__main__.py
import sys

from .cli import main

sys.exit(main())
```

> `--correcao` usa `choices`, então `argparse` já rejeita `xpto` com exit 2 e mensagem no stderr — é por isso que `test_correcao_invalida_devolve_2` passa sem código extra. O `try/except ValueError` cobre o caso de alguém chamar `main()` como biblioteca.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m uv run pytest tests/test_estaticos_cli.py -q`
Expected: PASS, 6 passed

- [ ] **Step 5: Run the CLI for real**

```bash
python -m uv run python -m instagram.estaticos conferir
python -m uv run python -m instagram.estaticos prompt cartao-classico-250g-graos --correcao soletrar
```
Expected: o primeiro imprime `ok: 1 peca(s) declarada(s)`; o segundo imprime um prompt em inglês com `S-C-A-space-8-0-plus`.

- [ ] **Step 6: Rodar a suíte inteira e conferir o delta**

Run: `python -m uv run pytest -p no:cacheprovider`
**Anote o número antes de começar esta tarefa.** A linha de base medida em 30/09/2026 21:30 foi **912 passed**; esta tarefa e as anteriores somam 54 testes novos. Confira que o total subiu e que **nada que passava antes quebrou**.

- [ ] **Step 7: Commit**

```bash
git add instagram/estaticos/cli.py instagram/estaticos/__main__.py tests/test_estaticos_cli.py
git commit -m "Estaticos: CLI com conferir, listar e prompt"
```

---

## Tarefa 10: zona 4:5 no Remotion — **GATED**

**NÃO COMECE** sem antes conferir que a outra sessão soltou o arquivo:

```bash
git status --short instagram/remotion/src/motor/layout.ts
ls -la --time-style=+%H:%M:%S instagram/remotion/src/motor/layout.ts
```

Se houver `M` ou se o mtime for dos últimos 30 minutos, **pare e avise**. Em 30/09/2026 21:06 esse arquivo foi modificado por outra sessão, e é a lição 9 do `CLAUDE.md`.

**Files:**
- Modify: `instagram/remotion/src/motor/layout.ts`
- Test: `instagram/remotion/tests/layout.test.ts`

- [ ] **Step 1: Ler o arquivo antes de escrever**

```bash
cat instagram/remotion/src/motor/layout.ts
cat instagram/remotion/tests/layout.test.ts
```
A outra sessão alterou esse módulo; o teste abaixo tem que ser **acrescentado** ao que existe, não substituí-lo.

- [ ] **Step 2: Write the failing test**

```typescript
// acrescentar a instagram/remotion/tests/layout.test.ts
import {expect, test} from 'vitest';
import {layout} from '../src/motor/layout';

test('zona 4:5 fecha em 1080x1350 e ambos os lados sao pares', () => {
  const z = layout({largura: 1080, altura: 1350});
  expect(z.largura).toBe(1080);
  expect(z.altura).toBe(1350);
  // h264 exige lado par; a licao 26 registra 360x639 descendo para 638 em silencio
  expect(z.largura % 2).toBe(0);
  expect(z.altura % 2).toBe(0);
  expect(z.largura * 5).toBe(z.altura * 4);
});

test('a area segura de 4:5 respeita a margem title-safe de 5 a 8%', () => {
  const z = layout({largura: 1080, altura: 1350});
  expect(z.segura.x).toBeGreaterThanOrEqual(Math.round(1080 * 0.05));
  expect(z.segura.x).toBeLessThanOrEqual(Math.round(1080 * 0.08));
  expect(z.segura.y).toBeGreaterThanOrEqual(Math.round(1350 * 0.05));
  expect(z.segura.y).toBeLessThanOrEqual(Math.round(1350 * 0.08));
});
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd instagram/remotion && npx vitest run tests/layout.test.ts`
Expected: FAIL — a razão 4:5 não fecha, ou `segura` não existe

- [ ] **Step 4: Estender `layout()`**

`layout()` já recebe `{largura, altura}` — `05-formatos.md` §6 registra isso, e é por isso que 4:5 é extensão e não reescrita.

Acrescente ao objeto que `layout()` devolve o campo `segura`, derivado **das dimensões recebidas**, sem nenhum número chumbado:

```typescript
// A margem title-safe e 6% -- meio da faixa 5-8% que a fonte A prescreve.
// Fracao em constante nomeada porque numero solto no meio da conta e como
// `--scale=0.333` entrou no repositorio (licao 26).
const MARGEM_SEGURA = 0.06;

export function areaSegura(largura: number, altura: number) {
  const x = Math.round(largura * MARGEM_SEGURA);
  const y = Math.round(altura * MARGEM_SEGURA);
  return {x, y, largura: largura - 2 * x, altura: altura - 2 * y};
}
```

e devolva `segura: areaSegura(largura, altura)` de dentro de `layout()`.

**Onde exatamente inserir depende do que o Step 1 mostrou** — a outra sessão mexeu neste arquivo e o corpo atual de `layout()` pode não ser o que havia às 18:36. Se `layout()` já devolver um campo com esse papel sob outro nome, **use o que existe** e ajuste o teste; não crie um segundo conceito de área segura.

Se `layout()` recusar `{largura: 1080, altura: 1350}` por validar razão contra uma lista fechada (`9:16`, `1:1`), acrescente `4:5` a essa lista — é a única mudança de comportamento que esta tarefa autoriza.

- [ ] **Step 5: Run test to verify it passes**

Run: `cd instagram/remotion && npx vitest run tests/layout.test.ts`
Expected: PASS

- [ ] **Step 6: Rodar a suíte Remotion inteira**

Run: `cd instagram/remotion && npx vitest run`
**Anote o número antes.** O 85 medido às 18:36 está velho: outra sessão acrescentou `cadencia.test.ts` e `relogio.test.ts` depois. Confira o delta, não o absoluto.

- [ ] **Step 7: Commit**

```bash
git add instagram/remotion/src/motor/layout.ts instagram/remotion/tests/layout.test.ts
git commit -m "Motor: zona 4:5 para peca estatica, com lado par e area segura"
```

---

## Tarefa 11: `Carta.tsx` — o cartão desenhado por código — **GATED**

Mesmo portão da Tarefa 10. Depende dela.

**Files:**
- Create: `instagram/remotion/src/estatico/Carta.tsx`
- Create: `instagram/remotion/src/estatico/moldes.ts`
- Modify: `instagram/remotion/src/motor/Raiz.tsx`
- Test: `instagram/remotion/tests/carta-props.test.ts`

- [ ] **Step 1: Write the failing test**

```typescript
// instagram/remotion/tests/carta-props.test.ts
import {expect, test} from 'vitest';
import {MOLDES_ESTATICO, validarProps} from '../src/estatico/moldes';

test('o molde cartao-produto declara os mesmos campos que o catalogo Python', () => {
  // Se esta lista divergir de MOLDES["cartao-produto"].campos em
  // instagram/estaticos/catalogo.py, a costura quebra em silencio.
  expect(MOLDES_ESTATICO['cartao-produto'].campos).toEqual([
    'preco',
    'altitude',
    'local',
  ]);
});

test('props sem um campo do molde e recusado', () => {
  expect(() =>
    validarProps('cartao-produto', {preco: 'R$ 31,70', altitude: '1.250 m'}),
  ).toThrow(/local/);
});

test('props com campo extra e recusado', () => {
  expect(() =>
    validarProps('cartao-produto', {
      preco: 'R$ 31,70',
      altitude: '1.250 m',
      local: 'Medeiros, MG',
      intruso: 'x',
    }),
  ).toThrow(/intruso/);
});

test('props completo passa e devolve o texto na ordem do molde', () => {
  const r = validarProps('cartao-produto', {
    preco: 'R$ 31,70',
    altitude: '1.250 m',
    local: 'Medeiros, MG',
  });
  expect(r).toEqual(['R$ 31,70', '1.250 m', 'Medeiros, MG']);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd instagram/remotion && npx vitest run tests/carta-props.test.ts`
Expected: FAIL — `Cannot find module '../src/estatico/moldes'`

- [ ] **Step 3: Write `moldes.ts`**

```typescript
// instagram/remotion/src/estatico/moldes.ts
// Espelho do catalogo Python. A costura entre os dois lados e um arquivo .json
// de props -- NUNCA JSON inline: `instagram/LEIA-ME.md` registra que no shell do
// Windows as aspas somem.
//
// Este arquivo duplica a lista de campos de proposito, e o teste
// `carta-props.test.ts` existe para a duplicacao nao virar divergencia.

export type MoldeEstatico = {campos: string[]; largura: number; altura: number};

export const MOLDES_ESTATICO: Record<string, MoldeEstatico> = {
  'cartao-produto': {
    campos: ['preco', 'altitude', 'local'],
    largura: 1080,
    altura: 1350,
  },
};

export function validarProps(
  molde: string,
  dados: Record<string, string>,
): string[] {
  const m = MOLDES_ESTATICO[molde];
  if (!m) throw new Error(`molde '${molde}' nao existe`);

  const faltando = m.campos.filter((c) => !(c in dados));
  if (faltando.length) {
    throw new Error(`props sem os campos: ${faltando.join(', ')}`);
  }
  const sobrando = Object.keys(dados).filter((c) => !m.campos.includes(c));
  if (sobrando.length) {
    throw new Error(`props com campos fora do molde: ${sobrando.join(', ')}`);
  }
  return m.campos.map((c) => dados[c]);
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd instagram/remotion && npx vitest run tests/carta-props.test.ts`
Expected: PASS, 4 passed

- [ ] **Step 5: Write `Carta.tsx`**

```tsx
// instagram/remotion/src/estatico/Carta.tsx
// O cartao estatico. A imagem entra como PIXEL (gerada ou composta); os tres
// campos entram como TEXTO DE CODIGO. Nenhuma cor nova: tudo de tokens.ts,
// senao reel e cartao deixam de parecer a mesma marca (licao 8).

import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {COR, TIPO, SOMBRA} from '../identidade/tokens';
import {PILHA} from '../identidade/tipografia';
import {areaSegura} from '../motor/layout';
import {MOLDES_ESTATICO, validarProps} from './moldes';

export type PropsCarta = {
  molde: string;
  imagem: string; // caminho dentro do public dir
  dados: Record<string, string>;
};

export const Carta: React.FC<PropsCarta> = ({molde, imagem, dados}) => {
  // validarProps LEVANTA se faltar ou sobrar campo. Deixar levantar e
  // intencional: um render que sai com campo faltando e pior que um que falha.
  const linhas = validarProps(molde, dados);
  const m = MOLDES_ESTATICO[molde];
  const s = areaSegura(m.largura, m.altura);

  return (
    <AbsoluteFill style={{backgroundColor: COR.terra}}>
      <Img
        src={staticFile(imagem)}
        style={{width: '100%', height: '100%', objectFit: 'cover'}}
      />
      <AbsoluteFill
        style={{
          left: s.x,
          top: s.y,
          width: s.largura,
          height: s.altura,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-end',
          gap: 16, // multiplo de 8
        }}
      >
        {linhas.map((texto, i) => (
          <div
            key={m.campos[i]}
            style={{
              fontFamily: PILHA.dado,
              fontWeight: TIPO.dado.peso,
              fontSize: i === 0 ? 96 : 44, // o primeiro campo e o heroi
              color: COR.creme,
              lineHeight: 1.1,
              textShadow: `0 ${SOMBRA.sobreVideo.dy}px ${SOMBRA.sobreVideo.blur}px rgba(0,0,0,${SOMBRA.sobreVideo.op})`,
            }}
          >
            {texto}
          </div>
        ))}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

> Se `PILHA` não exportar `dado`, use a chave que `identidade/tipografia.ts` realmente expõe para IBM Plex Mono — leia o arquivo, não adivinhe o nome.

- [ ] **Step 6: Registrar a composição em `Raiz.tsx`**

```tsx
// acrescentar dentro do fragmento devolvido por Raiz, junto das outras
<Composition
  id="Carta"
  component={Carta}
  durationInFrames={1}
  fps={FPS}
  width={1080}
  height={1350}
  defaultProps={{
    molde: 'cartao-produto',
    imagem: 'assets/carta-fonte.png',
    dados: {preco: 'R$ 31,70', altitude: '1.250 m', local: 'Medeiros, MG'},
  }}
/>
```

`durationInFrames={1}` porque é still — é o que `PonteAssets` já faz. Importe `Carta` no topo e **releia `Raiz.tsx` antes de editar**: a outra sessão pode ter mexido nele.

- [ ] **Step 7: Renderizar um still de verdade**

```bash
cd instagram/remotion
npx remotion still src/index.ts Carta out/carta-teste.png --props=../../scratchpad/carta.json
```
Expected: PNG de **1080x1350**. Confira a dimensão com PIL, e **amplie a faixa dos três campos** antes de aprovar — miniatura esconde erro de tipografia, e é a fase 4 do `canastra-conteudo`.

- [ ] **Step 8: Commit**

```bash
git add instagram/remotion/src/estatico/ instagram/remotion/src/motor/Raiz.tsx instagram/remotion/tests/carta-props.test.ts
git commit -m "Motor: composicao Carta 4:5, tipografia de peca em codigo"
```

---

## Tarefa 12: a skill `canastra-estatico`

**Files:**
- Create: `.claude/skills/canastra-estatico/SKILL.md`
- Modify: `CLAUDE.md` (acrescenta a linha na tabela de skills)

- [ ] **Step 1: Ler as skills vizinhas**

```bash
cat .claude/skills/canastra-conteudo/SKILL.md
cat .claude/skills/canastra-embalagem/SKILL.md
```
A skill nova **não repete** a mecânica do ChatGPT nem a tabela de racionalizações: ela **roteia** para `canastra-conteudo`, que é a dona disso. Repetir cria duas fontes de verdade.

- [ ] **Step 2: Escrever a skill**

Frontmatter: `name: canastra-estatico`, e uma `description` que dispare em "post estático", "cartão de produto", "carta sensorial", "peça de feed".

Corpo, e só isto:

1. **Rotear** — `canastra-conteudo` manda no fluxo e na conferência; `canastra-embalagem` manda no rótulo; esta skill manda no **laço e no catálogo**.
2. **O catálogo é dado.** Peça nova é linha em `instagram/estaticos/catalogo.py`, nunca improviso. Rode `python -m instagram.estaticos conferir` **antes** de gerar — ele recusa dado sem origem.
3. **A escada**, reproduzindo a tabela sintoma→degrau de `escada.py` com as lições de origem.
4. **O teto é 3 e o degrau 6 é o piso.** Não insista em prompt num campo que a lição 13 diz que não sobrevive.
5. **Lote, validade e QR nunca entram.** Vão direto ao degrau 6 ou saem do enquadramento (lição 22).
6. **Este pacote não roda em worktree** — lê acervo gitignored que só existe no diretório principal.
7. **Bandeiras vermelhas:** você marcou `ok` sem abrir o recorte ampliado; você não aponta em que pixel da referência leu o valor; você está prestes a declarar um `Dado` sem origem.

- [ ] **Step 3: Verificar que a skill carrega**

```bash
python - <<'PY'
import pathlib, re
t = pathlib.Path(".claude/skills/canastra-estatico/SKILL.md").read_text(encoding="utf-8")
assert t.startswith("---"), "sem frontmatter"
m = re.search(r"^name:\s*canastra-estatico$", t, re.M)
assert m, "name ausente ou diferente do diretorio"
assert re.search(r"^description:\s*\S", t, re.M), "description vazia"
print("ok")
PY
```
Expected: `ok`

- [ ] **Step 4: Acrescentar à tabela de skills do `CLAUDE.md`**

A tabela está na seção *Skills de conteúdo*. Acrescente:

```markdown
| `canastra-estatico` | post estático de feed — o catálogo declarado e a escada de correção do rótulo |
```

**Releia o arquivo antes de editar.** Outra sessão acrescentou `canastra-mercadolivre` a essa mesma tabela em 30/09/2026.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/canastra-estatico/SKILL.md CLAUDE.md
git commit -m "Skill canastra-estatico: conduz o laco, nao guarda dado de SKU"
```

---

## Verificação final

- [ ] `python -m uv run pytest -p no:cacheprovider` — total acima da base de **912**, nada que passava antes quebrado
- [ ] `python -m uv run python -m instagram.estaticos conferir` devolve 0
- [ ] `cd instagram/remotion && npx vitest run` — delta conferido contra o número anotado no início da Tarefa 10
- [ ] um still `Carta` de 1080x1350 existe e a faixa dos três campos foi **ampliada e lida**
- [ ] `git log --oneline` mostra um commit por tarefa, e `git show --stat` de cada um contém **só** os caminhos daquela tarefa
- [ ] `git status --short` não mostra arquivo de outra sessão arrastado para dentro de nenhum commit

---

## Registro de lição a escrever no fim

Independente do resultado, acrescente ao `Registro de lições` do `CLAUDE.md` a lição que este trabalho já provou antes de começar, no formato **sintoma → causa raiz → regra**:

> **Apliquei como regra de pipeline uma proibição que era de escopo de pasta** → `assets/materialidade/LEIA-ME.md` diz que embalagem "nunca nasce aqui", e eu li isso como "embalagem nunca entra em geração", contra 96 packshots gerados e aprovados e contra as lições 12 e 21 → antes de transformar uma linha de LEIA-ME em restrição de arquitetura, confira **de que escopo aquele arquivo fala**. Um documento de pasta descreve a pasta.
