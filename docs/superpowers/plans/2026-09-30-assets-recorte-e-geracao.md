# Assets: geração de imagem e recorte — Plano de implementação

> **Para trabalhadores agênticos:** SUB-SKILL OBRIGATÓRIA: use `superpowers:subagent-driven-development` (recomendado) ou `superpowers:executing-plans` para implementar tarefa a tarefa. Os passos usam caixa (`- [ ]`) para acompanhamento.

**Objetivo:** produzir a biblioteca de assets que o motor de vídeo consome — recortes de embalagem com alfa, fundos e texturas geradas — com verificação automática de que nenhum pixel do rótulo foi alterado.

**Arquitetura:** duas fontes, papéis separados e não negociáveis. **Recorte** vem de matting clássico sobre fotografia real: trimap por limiar + `pymatting`, onde tudo fora da faixa de borda recebe alfa exatamente 0 ou 1 *por construção*. **Geração** vem do ChatGPT via Claude in Chrome e entrega **só materialidade** — fundo, textura, vapor, luz. Letra, número e anotação são sempre desenhados por código, nunca gerados.

**Stack:** Python 3.11 · Pillow · numpy · scipy · pymatting · opencv-python-headless · Claude in Chrome

---

## Por que matting clássico e não rede neural

Uma rede (`rembg`, BiRefNet, InSPyReNet) prevê alfa contínuo sobre a imagem **inteira**, inclusive o interior do objeto. Nada garante alfa exatamente 255 em cada pixel de texto — pode sair 253. Invisível a olho, mas altera a cor real ao compor sobre um novo fundo. É o `Doodo 1985` de novo, em opacidade em vez de forma.

No `pymatting`, tudo fora da faixa "desconhecida" do trimap recebe 0 ou 1 **por construção**: o interior do rótulo nunca entra no solver.

**Licenças verificadas:**

| Opção | Situação |
|---|---|
| `pymatting` | **MIT**, sem rede, sem GPU — escolhido |
| `rembg` código | MIT, mas o **modelo padrão `bria-rmbg` exige acordo pago** para uso comercial |
| BiRefNet | código MIT; pesos "general" sem cláusula clara; **sem suporte a CPU documentado** |
| SAM 2 | Apache-2.0 — só como máscara grosseira com prompt manual, nunca alfa final |

**Foto de ambiente (lavoura, terreiro, galpão) não é caso de matting.** O fundo compartilha cor com o objeto e nem rede de ponta resolve. Ali a regra é mudar de registro: a foto entra inteira, por moldura ou tela cheia, como já faz a skill `canastra-cena`.

---

## Estado verificado do ambiente

Medido em 30/09/2026 nesta máquina:

| Pacote | Situação |
|---|---|
| Pillow 12.3.0 | instalado |
| numpy · scipy · cv2 · numba · pymatting | **ausentes** |

E nenhum deles está declarado no `pyproject.toml`. Pela lição 11 do `CLAUDE.md`, `uv sync` apaga tudo que não está declarado — então instalar solto não resolve, tem que virar extra.

---

## Estrutura de arquivos

```
instagram/
  recorte/
    __init__.py
    trimap.py              gera trimap por limiar de cor
    matte.py               pymatting -> alfa
    verificar.py           laudo de preservação de pixel
    cli.py                 `python -m instagram.recorte`
  assets/
    embalagem/
      classico-250g.png    RGBA, recorte verificado
      classico-250g.json   proveniência + retângulo do rótulo + laudo
    materialidade/
      <nome>.png           fundo/textura gerada
      <nome>.json          prompt, data, modelo, o que NÃO contém
tests/
  test_recorte.py
```

---

### Tarefa 0: Declarar dependências

**Arquivos:**
- Modificar: `pyproject.toml`

- [ ] **Passo 1: Confirmar o que falta**

```bash
python -c "
for m in ['PIL','numpy','cv2','scipy','pymatting']:
    try: __import__(m); print(m,'OK')
    except ImportError: print(m,'FALTA')
"
```

Esperado hoje: `PIL OK`, o resto `FALTA`.

- [ ] **Passo 2: Declarar como extra**

Em `pyproject.toml`, dentro de `[project.optional-dependencies]`, acrescente seguindo o padrão comentado que já existe:

```toml
# Recorte de packshot: matting classico, sem rede neural e sem GPU.
# Escolhido porque o interior do rotulo nunca entra no solver.
recorte = [
  "numpy>=1.26",
  "scipy>=1.13",
  "pymatting>=1.1.12",
  "opencv-python-headless>=4.10",
]
```

- [ ] **Passo 3: Instalar e confirmar que o `uv` sobreviveu**

```bash
python -m uv sync --extra recorte
python -m uv --version
python -c "import numpy, cv2, pymatting; print('ok')"
```

O `python -m uv --version` está aí de propósito: a lição 11 registra que `uv sync` já removeu o próprio `uv` do venv. Se sumir, reinstale antes de seguir.

- [ ] **Passo 4: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "chore: declara extra de recorte (pymatting, sem rede neural)"
```

---

### Tarefa 1: Trimap por limiar

**Arquivos:**
- Criar: `instagram/recorte/__init__.py`, `instagram/recorte/trimap.py`
- Teste: `tests/test_recorte.py`

- [ ] **Passo 1: Escrever o teste que falha**

```python
import numpy as np
import pytest
from instagram.recorte.trimap import gerar_trimap


def _quadrado_em_fundo_claro():
    """Objeto escuro 40x40 centrado num fundo claro 100x100."""
    img = np.full((100, 100, 3), 235, dtype=np.uint8)
    img[30:70, 30:70] = (60, 45, 30)
    return img


def test_trimap_marca_fundo_como_zero():
    t = gerar_trimap(_quadrado_em_fundo_claro(), banda=3)
    assert t[0, 0] == 0.0
    assert t[99, 99] == 0.0


def test_trimap_marca_interior_do_objeto_como_um():
    t = gerar_trimap(_quadrado_em_fundo_claro(), banda=3)
    assert t[50, 50] == 1.0


def test_faixa_desconhecida_so_existe_na_borda():
    t = gerar_trimap(_quadrado_em_fundo_claro(), banda=3)
    desconhecido = (t > 0.0) & (t < 1.0)
    # nenhuma incerteza no centro do objeto
    assert not desconhecido[45:55, 45:55].any()
    # mas existe incerteza em volta da borda
    assert desconhecido.any()


def test_banda_maior_alarga_a_faixa_desconhecida():
    img = _quadrado_em_fundo_claro()
    estreita = ((gerar_trimap(img, banda=2) > 0) & (gerar_trimap(img, banda=2) < 1)).sum()
    larga = ((gerar_trimap(img, banda=8) > 0) & (gerar_trimap(img, banda=8) < 1)).sum()
    assert larga > estreita
```

- [ ] **Passo 2: Rodar e ver falhar**

```bash
python -m uv run pytest tests/test_recorte.py -q
```

Esperado: FAIL — `ModuleNotFoundError: instagram.recorte.trimap`.

- [ ] **Passo 3: Implementar**

```python
"""Trimap por limiar de cor, para packshot em fundo neutro.

Nao usa rede neural de proposito: o objetivo e que o interior do objeto
receba alfa 1.0 por CONSTRUCAO, nunca por predicao. Ver o plano em
docs/superpowers/plans/2026-09-30-assets-recorte-e-geracao.md.
"""
import cv2
import numpy as np


def gerar_trimap(img_rgb: np.ndarray, banda: int = 6,
                 percentil_fundo: float = 2.0) -> np.ndarray:
    """Devolve um trimap float32: 0.0 fundo, 1.0 objeto, 0.5 desconhecido.

    `banda` e a largura em pixels da faixa de incerteza em volta da borda.
    """
    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)

    # cor do fundo = mediana das 4 bordas da imagem
    bordas = np.concatenate([
        lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1],
    ], axis=0)
    fundo = np.median(bordas, axis=0)

    dist = np.linalg.norm(lab - fundo, axis=2)
    limiar = np.percentile(dist, percentil_fundo) + \
        (dist.max() - np.percentile(dist, percentil_fundo)) * 0.12

    bruto = (dist > limiar).astype(np.uint8)

    # maior componente conectado, na ordem certa:
    # abrir (tira ruido) -> rotular -> maior -> fechar -> preencher buraco.
    # Fechar ANTES de rotular cola a sombra ao objeto.
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    bruto = cv2.morphologyEx(bruto, cv2.MORPH_OPEN, k)
    n, rotulos, stats, _ = cv2.connectedComponentsWithStats(bruto, 8)
    if n > 1:
        maior = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        bruto = (rotulos == maior).astype(np.uint8)
    bruto = cv2.morphologyEx(bruto, cv2.MORPH_CLOSE, k)

    d = max(1, int(banda))
    kb = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * d + 1, 2 * d + 1))
    dentro = cv2.erode(bruto, kb)
    fora = cv2.dilate(bruto, kb)

    tri = np.full(bruto.shape, 0.5, dtype=np.float32)
    tri[fora == 0] = 0.0
    tri[dentro == 1] = 1.0
    return tri
```

- [ ] **Passo 4: Rodar e ver passar**

```bash
python -m uv run pytest tests/test_recorte.py -q
```

Esperado: PASS, 4 testes.

- [ ] **Passo 5: Commit**

```bash
git add instagram/recorte tests/test_recorte.py
git commit -m "feat(recorte): trimap por limiar com faixa de incerteza so na borda"
```

---

### Tarefa 2: O laudo de preservação

Escrito antes do matting, de propósito: é o portão que impede o motor de comer o rótulo.

**Arquivos:**
- Criar: `instagram/recorte/verificar.py`
- Teste: acrescentar a `tests/test_recorte.py`

- [ ] **Passo 1: Escrever o teste que falha**

```python
from instagram.recorte.verificar import laudo_preservacao


def test_alfa_cheio_e_rgb_igual_nao_acusa_diferenca():
    rgb = np.full((50, 50, 3), 128, dtype=np.uint8)
    alfa = np.full((50, 50), 255, dtype=np.uint8)
    r = laudo_preservacao(rgb, rgb.copy(), alfa)
    assert r["pixels_alterados"] == 0
    assert r["maior_delta"] == 0
    assert r["aprovado"] is True


def test_um_pixel_alterado_no_opaco_reprova():
    rgb = np.full((50, 50, 3), 128, dtype=np.uint8)
    saida = rgb.copy()
    saida[10, 10] = (120, 128, 128)
    alfa = np.full((50, 50), 255, dtype=np.uint8)
    r = laudo_preservacao(rgb, saida, alfa)
    assert r["pixels_alterados"] == 1
    assert r["aprovado"] is False


def test_retangulo_do_rotulo_precisa_de_alfa_cheio():
    rgb = np.full((50, 50, 3), 128, dtype=np.uint8)
    alfa = np.full((50, 50), 255, dtype=np.uint8)
    alfa[20, 20] = 250          # quase opaco -- e o bastante para reprovar
    r = laudo_preservacao(rgb, rgb.copy(), alfa,
                          retangulo_rotulo=(15, 15, 30, 30))
    assert r["aprovado"] is False
    assert r["alfa_minimo_no_rotulo"] == 250
```

- [ ] **Passo 2: Rodar e ver falhar**

```bash
python -m uv run pytest tests/test_recorte.py -q
```

Esperado: FAIL — `ModuleNotFoundError: instagram.recorte.verificar`.

- [ ] **Passo 3: Implementar**

```python
"""Laudo automatico: o recorte alterou algum pixel do objeto?

A pergunta nao se responde no olho. Se responde comparando o RGB original
com o de saida EXATAMENTE onde o alfa e 255.
"""
import numpy as np


def laudo_preservacao(rgb_origem: np.ndarray, rgb_saida: np.ndarray,
                      alfa: np.ndarray, tolerancia: int = 0,
                      retangulo_rotulo: tuple | None = None) -> dict:
    opaco = alfa == 255
    a = rgb_origem[opaco].astype(np.int16)
    b = rgb_saida[opaco].astype(np.int16)
    delta = np.abs(a - b).max(axis=1) if a.size else np.zeros(0, dtype=np.int16)

    alterados = int((delta > tolerancia).sum())
    maior = int(delta.max()) if delta.size else 0

    alfa_min_rotulo = None
    if retangulo_rotulo is not None:
        x0, y0, x1, y1 = retangulo_rotulo
        alfa_min_rotulo = int(alfa[y0:y1, x0:x1].min())

    aprovado = (alterados == 0) and (
        alfa_min_rotulo is None or alfa_min_rotulo == 255
    )
    return {
        "pixels_alterados": alterados,
        "maior_delta": maior,
        "pixels_opacos": int(opaco.sum()),
        "alfa_minimo_no_rotulo": alfa_min_rotulo,
        "aprovado": aprovado,
    }
```

- [ ] **Passo 4: Rodar e ver passar**

```bash
python -m uv run pytest tests/test_recorte.py -q
```

Esperado: PASS, 7 testes no total.

- [ ] **Passo 5: Commit**

```bash
git add instagram/recorte/verificar.py tests/test_recorte.py
git commit -m "feat(recorte): laudo de preservacao de pixel e de alfa no rotulo"
```

---

### Tarefa 3: Matting

**Arquivos:**
- Criar: `instagram/recorte/matte.py`
- Teste: acrescentar a `tests/test_recorte.py`

- [ ] **Passo 1: Escrever o teste que falha**

```python
from instagram.recorte.matte import recortar


def test_recorte_devolve_rgba_do_mesmo_tamanho():
    img = _quadrado_em_fundo_claro()
    rgba = recortar(img)
    assert rgba.shape == (100, 100, 4)
    assert rgba.dtype == np.uint8


def test_interior_do_objeto_fica_totalmente_opaco():
    rgba = recortar(_quadrado_em_fundo_claro())
    assert rgba[50, 50, 3] == 255


def test_canto_do_fundo_fica_totalmente_transparente():
    rgba = recortar(_quadrado_em_fundo_claro())
    assert rgba[0, 0, 3] == 0


def test_recorte_nao_altera_o_rgb_do_interior():
    img = _quadrado_em_fundo_claro()
    rgba = recortar(img)
    r = laudo_preservacao(img, rgba[:, :, :3], rgba[:, :, 3])
    assert r["aprovado"] is True, r
```

O último é o teste que importa. Se ele falhar, o motor não pode ser usado em embalagem.

- [ ] **Passo 2: Rodar e ver falhar**

```bash
python -m uv run pytest tests/test_recorte.py -q
```

Esperado: FAIL — `ModuleNotFoundError: instagram.recorte.matte`.

- [ ] **Passo 3: Implementar**

```python
"""Matting classico com pymatting.

Importante: o RGB de saida e o RGB ORIGINAL, nao o primeiro plano estimado.
Estimar primeiro plano muda a cor do interior, e o requisito aqui e preservar
pixel. O alfa resolve a borda; o miolo fica intacto.
"""
import numpy as np
from pymatting import estimate_alpha_cf

from .trimap import gerar_trimap


def recortar(img_rgb: np.ndarray, banda: int = 6) -> np.ndarray:
    tri = gerar_trimap(img_rgb, banda=banda)
    img_f = img_rgb.astype(np.float64) / 255.0
    alfa = estimate_alpha_cf(img_f, tri.astype(np.float64))

    # trava as regioes certas: o solver so decide na faixa desconhecida
    alfa = np.clip(alfa, 0.0, 1.0)
    alfa[tri == 0.0] = 0.0
    alfa[tri == 1.0] = 1.0

    rgba = np.dstack([img_rgb, (alfa * 255.0).round().astype(np.uint8)])
    return rgba
```

As duas linhas que travam `tri == 0` e `tri == 1` são o coração do plano. Sem elas o solver pode devolver 254 no miolo e o laudo reprova.

- [ ] **Passo 4: Rodar e ver passar**

```bash
python -m uv run pytest tests/test_recorte.py -q
```

Esperado: PASS, 11 testes.

- [ ] **Passo 5: Commit**

```bash
git add instagram/recorte/matte.py tests/test_recorte.py
git commit -m "feat(recorte): matting que preserva o RGB original do interior"
```

---

### Tarefa 4: Recortar os SKUs reais e medir o retângulo do rótulo

**Arquivos:**
- Criar: `instagram/recorte/cli.py`
- Criar: `instagram/assets/embalagem/*.png` e `*.json`

- [ ] **Passo 1: Escrever a CLI**

```python
"""Uso: python -m instagram.recorte <entrada.jpg> <saida.png> [--banda 6]"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

from .matte import recortar
from .verificar import laudo_preservacao


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("entrada")
    p.add_argument("saida")
    p.add_argument("--banda", type=int, default=6)
    a = p.parse_args()

    img = np.array(Image.open(a.entrada).convert("RGB"))
    rgba = recortar(img, banda=a.banda)
    laudo = laudo_preservacao(img, rgba[:, :, :3], rgba[:, :, 3])

    Image.fromarray(rgba).save(a.saida)
    Path(a.saida).with_suffix(".json").write_text(
        json.dumps({"origem": a.entrada, "banda": a.banda, "laudo": laudo},
                   ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{a.saida}  alterados={laudo['pixels_alterados']} "
          f"maior_delta={laudo['maior_delta']} aprovado={laudo['aprovado']}")
    return 0 if laudo["aprovado"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

O código de saída 1 quando reprova é proposital: quebra qualquer script que ignore o laudo.

- [ ] **Passo 2: Escolher os packshots de fundo neutro**

```bash
ls base-curada/01-real-verificada/ | head -40
```

Escolha **um** packshot de cada SKU (Clássico, Suave, Canela) em fundo neutro. **Não use** nada de `03-mood-terceiros` nem de `04-quarentena` — são as camadas proibidas como pixel.

- [ ] **Passo 3: Recortar e conferir com recorte ampliado**

```bash
python -m uv run python -m instagram.recorte <packshot> instagram/assets/embalagem/classico-250g.png
```

Se sair `aprovado=False`, **não prossiga**: ajuste `--banda` e rode de novo.

Depois **amplie a faixa de texto** do PNG e compare com a foto original, letra por letra. É a regra da skill `canastra-embalagem` e ela não é opcional: miniatura esconde erro de letra.

- [ ] **Passo 4: Medir o retângulo do rótulo de cada SKU**

Abra cada PNG, localize o retângulo que contém a tipografia impressa e grave as coordenadas no `.json` como `retangulo_rotulo: [x0, y0, x1, y1]`. Meça **no próprio pixel** — é a lição 14 do `CLAUDE.md`. Acrescente um teste por SKU que roda `laudo_preservacao(..., retangulo_rotulo=...)` e exige `aprovado is True`.

- [ ] **Passo 5: Commit**

```bash
git add instagram/recorte/cli.py instagram/assets/embalagem tests/test_recorte.py
git commit -m "feat(recorte): CLI e recortes verificados dos 3 SKUs"
```

---

### Tarefa 5: Geração de materialidade pelo ChatGPT

**Arquivos:**
- Criar: `instagram/assets/materialidade/LEIA-ME.md`
- Modificar: `scripts/_pega_download.py`

- [ ] **Passo 1: Escrever a regra da pasta**

`instagram/assets/materialidade/LEIA-ME.md`:

```markdown
# Materialidade gerada

O que pode nascer aqui: fundo, textura, papel, vapor, fumaça, terra, luz,
superfície, céu.

O que **nunca** nasce aqui:
- letra, número, rótulo, selo, QR, código de barras — é sempre código;
- embalagem da Canastra — entra como recorte de foto real;
- rosto de pessoa real.

Cada PNG tem um `.json` irmão com o prompt, a data, o modelo e uma linha
`nao_contem` declarando o que foi checado e não está na imagem.
```

- [ ] **Passo 2: Usar o fluxo de Chrome já documentado**

A mecânica está na skill `canastra-conteudo`, fase 3, e já foi medida: aba nova sempre, composer em `.ProseMirror`, inserir com `document.execCommand('insertText', ...)` e **nunca** `computer.type`, clicar em Enviar duas vezes, esperar em blocos de 10 s, achar a imagem por `img[alt]` casando `/gerada|Generated/`, e baixar pela tela cheia. Não redescubra.

- [ ] **Passo 3: Endurecer a captura do download**

A lição 17 registra que `_pega_download.py` salvou silenciosamente a imagem do dia anterior porque o glob só cobria um dos dois padrões de nome. O conserto cobriu os dois, mas o modo de falha continua possível: **um seletor que não acha o alvo mas acha algo é pior que um que falha.**

Acrescente uma trava de idade:

```python
import time

IDADE_MAXIMA_S = 180

def exigir_recente(caminho: str) -> None:
    idade = time.time() - os.path.getmtime(caminho)
    if idade > IDADE_MAXIMA_S:
        raise SystemExit(
            f"ABORTADO: {caminho} tem {idade/60:.1f} min de idade. "
            "O download provavelmente falhou e o glob pegou um arquivo antigo."
        )
```

Chame antes de copiar. Dimensão igual não prova que é a imagem certa; carimbo de hora prova.

- [ ] **Passo 4: Commit**

```bash
git add instagram/assets/materialidade/LEIA-ME.md scripts/_pega_download.py
git commit -m "feat(assets): regra de materialidade e trava de idade no download"
```

---

### Tarefa 6: Ligar ao motor de vídeo

**Arquivos:**
- Criar: `instagram/remotion/public/` (link ou cópia dos assets aprovados)

- [ ] **Passo 1: Publicar só o que passou no laudo**

Escreva `instagram/recorte/publicar.py` que copia para `instagram/remotion/public/assets/` **apenas** os PNGs cujo `.json` irmão tem `laudo.aprovado == true`. Qualquer outro é ignorado com aviso no stderr.

- [ ] **Passo 2: Escrever o teste do portão, que falha**

Acrescente a `tests/test_recorte.py`:

```python
import json
from pathlib import Path

from PIL import Image

from instagram.recorte.publicar import publicar


def _par(pasta: Path, nome: str, aprovado: bool) -> None:
    """Cria um png e o .json irmao com o laudo pedido."""
    Image.new("RGBA", (8, 8), (10, 20, 30, 255)).save(pasta / f"{nome}.png")
    (pasta / f"{nome}.json").write_text(
        json.dumps({"laudo": {"aprovado": aprovado}}), encoding="utf-8")


def test_publicar_copia_o_aprovado(tmp_path):
    origem, destino = tmp_path / "a", tmp_path / "b"
    origem.mkdir(); destino.mkdir()
    _par(origem, "classico-250g", True)

    copiados = publicar(origem, destino)

    assert copiados == ["classico-250g.png"]
    assert (destino / "classico-250g.png").exists()


def test_publicar_ignora_o_reprovado(tmp_path):
    origem, destino = tmp_path / "a", tmp_path / "b"
    origem.mkdir(); destino.mkdir()
    _par(origem, "suave-250g", False)

    copiados = publicar(origem, destino)

    assert copiados == []
    assert not (destino / "suave-250g.png").exists()


def test_publicar_ignora_png_sem_laudo(tmp_path):
    origem, destino = tmp_path / "a", tmp_path / "b"
    origem.mkdir(); destino.mkdir()
    Image.new("RGBA", (8, 8)).save(origem / "orfao.png")

    copiados = publicar(origem, destino)

    assert copiados == []
```

Rode e veja falhar:

```bash
python -m uv run pytest tests/test_recorte.py -q
```

Esperado: FAIL — `ModuleNotFoundError: instagram.recorte.publicar`.

- [ ] **Passo 2b: Implementar e ver passar**

`instagram/recorte/publicar.py`:

```python
"""Copia para o motor de video APENAS o recorte que passou no laudo.

PNG sem .json irmao e PNG reprovado nao viajam. O portao e aqui porque e o
ultimo ponto antes de o pixel virar video publicado.
"""
import json
import shutil
import sys
from pathlib import Path


def publicar(origem: Path, destino: Path) -> list[str]:
    destino.mkdir(parents=True, exist_ok=True)
    copiados: list[str] = []
    for png in sorted(Path(origem).glob("*.png")):
        laudo_path = png.with_suffix(".json")
        if not laudo_path.exists():
            print(f"  ignorado (sem laudo): {png.name}", file=sys.stderr)
            continue
        dados = json.loads(laudo_path.read_text(encoding="utf-8"))
        if not dados.get("laudo", {}).get("aprovado"):
            print(f"  ignorado (reprovado): {png.name}", file=sys.stderr)
            continue
        shutil.copy2(png, destino / png.name)
        copiados.append(png.name)
    return copiados
```

```bash
python -m uv run pytest tests/test_recorte.py -q
```

Esperado: PASS, 14 testes no total.

- [ ] **Passo 3: Commit**

```bash
git add instagram/recorte/publicar.py tests/test_recorte.py
git commit -m "feat(assets): publica no motor apenas recorte aprovado"
```

---

## Verificação final

- [ ] `python -m uv run pytest tests/test_recorte.py -q` passa inteiro
- [ ] os 3 SKUs têm PNG com alfa e `laudo.aprovado == true`
- [ ] o recorte ampliado da faixa de texto de cada SKU foi conferido **letra por letra** contra a foto original
- [ ] `alfa_minimo_no_rotulo == 255` nos 3
- [ ] nenhum arquivo de `03-mood-terceiros` ou `04-quarentena` entrou como pixel
- [ ] `python -m uv --version` ainda responde depois do `uv sync`

## Riscos assumidos

1. **Fundo de estúdio pode não ser uniforme** em todos os packshots. Se a sombra tiver gradiente forte, o limiar falha. Plano B: usar uma máscara grosseira só para **gerar o trimap**, nunca para decidir o alfa final.
2. **`pymatting` usa numba**, que compila na primeira execução e pode demorar. Não é erro.
3. **Foto de ambiente continua fora do escopo** deste plano, por decisão. Se alguém tentar recortar lavoura com essa ferramenta, o resultado vai ser ruim e a culpa é do uso, não do motor.
