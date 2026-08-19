# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Idioma:** este projeto é escrito e discutido em português do Brasil. Código,
> comentários e documentação em pt-BR; corpo de prompt de imagem em inglês (os
> modelos respondem melhor). Responda ao usuário em português.

---

## Status: em teste

O motor está em validação ativa. **Quando algo falhar, a correção não é só
consertar — é registrar a lição na seção [Registro de lições](#registro-de-lições)
no fim deste arquivo.** Todo erro que custou uma rodada de geração e não virou
regra escrita será repetido pela próxima sessão, que não tem a memória desta.

---

## Comandos

O `uv` foi instalado via pip, então é `python -m uv`, não `uv` direto.

```bash
python -m uv venv --python 3.11      # uv baixa o CPython 3.11 se não houver
python -m uv sync --group dev
python -m uv run pytest              # suíte completa
python -m uv run pytest tests/test_guardrails.py::test_nome -q   # um teste só
python -m uv run cie --help
```

Chaves em `.env` (gitignored): `XAI_API_KEY`, `GEMINI_API_KEY`.

## Duas sessões, um repositório

Este projeto costuma ter mais de uma sessão do Claude Code aberta ao mesmo tempo.
**Um diretório git só fica em uma branch por vez** — trocar de branch muda a
branch da outra sessão debaixo dela, e um commit dela pode cair na sua branch.
Isso já aconteceu neste repositório.

Antes de qualquer `git checkout`, verifique se há outra sessão ativa. Para
trabalhar em paralelo, use worktree:

```bash
git worktree add ../Canastra-<assunto> -b <branch>
git worktree list
```

Arquivos gitignored pesados (`base-curada/`, `saida-teste/`, `imagens/`) vivem só
no diretório principal e **não** viajam para o worktree. Scripts que os leem por
caminho relativo devem rodar a partir do diretório principal.

---

## Arquitetura

### O motor `cie/` está desalinhado com a prática atual

Isto é o mais importante para entender antes de mexer em qualquer coisa: **o
código em `cie/` foi escrito antes das descobertas de geração e nunca foi usado
para produzir uma imagem.** O banco tem `generations: 0`, `jobs: 0`, `assets: 0`,
`style_dna: 0`. Todas as imagens do projeto saíram de scripts avulsos.

Consequências concretas:

- `cie/prompt.py` → `TECHNICAL_ANCHORS` pede *"full frame camera, RAW capture at
  ISO 200"* e *"optical bokeh from the aperture blades"*. É o oposto do alvo
  estético (foto de celular, sensor pequeno, foco profundo). Reescrever, não ajustar.
- `_truncate()` corta as âncoras **primeiro** quando o prompt passa do teto, ou
  seja, a camada de realismo é a mais frágil do sistema.
- `cie/xai.py` não conhece `/images/edits`, nem multi-fonte, nem o formato correto
  de referência.
- Não existe cliente Gemini.
- `cie/compositor.py` não faz recorte, reiluminação nem sombra de contato.

Ao portar conhecimento para dentro do motor, trate `cie/` como esqueleto a
substituir, não como base a estender.

### O que de fato governa o projeto

A verdade operacional está nos documentos, não no código:

| Arquivo | Papel |
|---|---|
| `docs/flow-geracao.md` | **Leia primeiro.** Arquitetura de geração e os 3 fluxos |
| `docs/dna-embalagens.md` | Descrição física dos 3 SKUs. **Premissa central marcada como superada** — só a parte física vale |
| `docs/briefing-captura.md` | O que falta fotografar. Bloqueador real do projeto |
| `docs/custos-geracao.md` | Preços confirmados dos dois provedores |
| `Direcao-Criativa.md` | Posicionamento de marca e os 4 pilares de conteúdo |

### Camadas de permissão da base de imagens

`base-curada/` separa 66 arquivos pelo **que é permitido fazer com cada um**, não
por assunto. Ver `base-curada/LEIA-ME.md`.

| Camada | Referência de imagem | Style DNA | Recorte |
|---|:---:|:---:|:---:|
| `01-real-verificada` (38) — EXIF de câmera **e** GPS | sim | sim | sim |
| `02-real-nao-verificada` (6) — sem prova de origem | não | não | não |
| `03-mood-terceiros` (16) — scrapes de Pinterest | **nunca** | só descritor textual | **nunca** |
| `04-quarentena` (6) — sintéticas e baixa resolução | **nunca** | **nunca** | **nunca** |

Regras que não se negociam:

- **Nunca** envie arquivo de `03-mood-terceiros` como fonte de guidance. Uma tem
  marca d'água (`@thamylis.pine…`), outra tem rosto identificável de quem não
  autorizou. Servem para descrever estética em texto, não para virar pixel.
- Os dois `Gemini_Generated_Image_*.jpg` em `04-quarentena` estavam misturados nas
  pastas de produto. Se entrarem na destilação de estilo, o motor aprende o look
  sintético que o projeto existe para evitar.
- **Rosto de pessoa real nunca é sintetizado.** Foto de pessoa é foto.

---

## Raspagem do Instagram (`cie scrape`)

Cole um link de perfil, post ou hashtag; as imagens caem em `raspagem/` com
proveniência registrada. Detalhes em `docs/RASPAGEM.md`.

Extra opcional — não vem no `sync` normal, usa o Chrome já instalado e **não**
baixa Chromium:

```bash
python -m uv sync --extra scrape
```

Login uma vez. A sessão fica em `.cie/browser-profile/` (gitignored):

```bash
python -m uv run cie scrape login     # abre o Chrome; logue e deixe a janela aberta
python -m uv run cie scrape status    # a sessão salva ainda está logada?
```

**Use uma conta secundária.** Raspagem pesada rende bloqueio temporário, e é a
conta logada aí que leva.

```bash
python -m uv run cie scrape run https://www.instagram.com/lacabracoffee/ --limit 30
python -m uv run cie scrape run https://www.instagram.com/p/DX61hmijlDI/
python -m uv run cie scrape run @cafecanastra --dry-run
```

| Opção | Padrão | Efeito |
|---|---|---|
| `--limit N` | 12 | posts a colher; `0` = todos |
| `--out DIR` | `raspagem/` | raiz de saída |
| `--delay S` | 1.0 | pausa entre downloads |
| `--dry-run` | desligado | lista o que baixaria, não baixa |
| `--show-browser` | desligado | abre a janela em vez de headless |

Reel é recusado no parse do link (vídeo não é referência de imagem estática).
Vídeo dentro de carrossel é pulado, não é erro.

Quando quebrar, os dois estágios se separam — o JSON cru é gravado **antes** de
qualquer download, então a colheita não se perde:

```bash
python -m uv run cie scrape harvest @alvo --limit 30        # só o JSON cru
python -m uv run cie scrape collect raspagem/_colheita/<arq>.json   # só o download
```

### Onde as coisas caem

```
raspagem/                                   (gitignored)
  _colheita/<alvo>-<carimbo>.json           JSON cru da colheita
  <handle>/2026-05-04_DX61hmijlDI_1.jpg     imagem
  <handle>/2026-05-04_DX61hmijlDI_1.json    sidecar de proveniência
  _manifest.json                            índice por sha256
```

O sidecar guarda post_url, handle, shortcode, índice no carrossel, URL do CDN,
dimensões, sha256 e quando foi raspado. **Não** guarda `has_identifiable_person`
nem `consent_on_file` — esses só existem em `Asset` e só a curadoria humana
preenche.

### O que a raspagem NÃO protege

`cie scrape` para em `raspagem/`. Mover para `base-curada/` é decisão humana.

E a proteção é só essa. Medido em 18/08/2026, na primeira colheita real: **21 de
40 imagens vieram em 1281×1611**, acima de `REFERENCE_MIN_SIDE = 1200`, e 11
passariam como reference-grade completo. `cie/ingest.py` não conhece camada e
`cie/guardrails.py` não tem regra de procedência — nada no código impede uma foto
de terceiro raspada daqui de virar pixel de saída se alguém a mover para
`01-real-verificada`.

Trate `raspagem/` como material que só vira descritor textual, e não conte com o
motor para lembrar disso.

---

## Regras de geração

Tudo abaixo foi medido ou obtido por erro da API, não inferido.

### Regra zero: a embalagem entra como pixel, nunca como texto solto

Descrever o logotipo no prompt e deixar o modelo desenhar produz um **sósia** da
marca. Pode ficar bonito e vai estar errado.

Três fluxos, por ordem de fidelidade:

1. **`/images/edits` da xAI** — a foto real do pacote é a fonte; o prompt só
   descreve o ambiente. É edição sobre a fonte, então o rótulo sobrevive.
2. **Gemini com DNA textual blindado** — o Gemini trata a referência como
   *inspiração* e **redesenha** o rótulo. Exige citar cada string entre aspas
   (`"SPECIALTY"`, soletrado `S-P-E-C-I-A-L-T-Y`; `"250g"` com os dígitos nomeados).
   Mesmo assim erra ~1 em 3 — gere 2–3 variantes e escolha.
3. **Composição local do recorte** — única garantia pixel-exata. Para anúncio
   pago, e-commerce e rótulo.

**Fidelidade de rótulo escala com o tamanho no quadro.** Abaixo de ~30% da altura,
conte com erro de letra. Já saiu `SOSCIALTY`/`288g` e `ARGEIACTY`/`SIANSE`.

### API xAI

Base `https://api.x.ai/v1`, header `Authorization: Bearer`.

```jsonc
// fonte única — image é OBJETO
"image": { "url": "data:image/jpeg;base64,...", "type": "image_url" }

// múltiplas fontes — campo PLURAL, até 4 testadas
"images": [ {"url": "...", "type": "image_url"}, ... ]
```

**Armadilha que já custou duas rodadas:** passar `image_url` em `/images/edits`
devolve **HTTP 200 e ignora a imagem** — o endpoint gera só do texto e você não
percebe que o guidance nunca foi aplicado. O mesmo vale para `reference_images`,
`input_images`, `image_urls`. O erro 400 é que revela a verdade:
*"provide either the `image` field or the `images` field, but not both"*.

- **`4:5` NÃO existe.** Válidos: `1:1`, `3:4`, `4:3`, `9:16`, `16:9`, `2:3`, `3:2`,
  `9:19.5`, `19.5:9`, `9:20`, `20:9`, `1:2`, `2:1`, `auto`. Para feed 4:5, gerar em
  `3:4` e recortar a altura tirando ~62% da sobra do topo.
- `grok-imagine-image-2.0`: `quality` só `low`|`medium` (`high` → 400);
  `resolution` `1k`|`2k`. Em `medium/2k` sai 1776×2368.
- Preços (do próprio `/models`): `-image` $0,02 · `-quality` $0,05 · `-2.0`
  $0,04–0,08.
- Saída de multi-fonte **herda a proporção da primeira fonte**.

### API Gemini

Base `https://generativelanguage.googleapis.com/v1beta`.

- **Auth por `x-goog-api-key`.** Token `AQ.*` como `Bearer` devolve 401.
- Modelos de imagem: `gemini-2.5-flash-image`, `gemini-3-pro-image`,
  `nano-banana-pro-preview`, `gemini-3.1-flash-image`, `gemini-3.1-flash-lite-image`.
  **Não existe `3.1-pro-image`** — o Pro mais atual é `gemini-3-pro-image`.
- `generationConfig.responseModalities: ["IMAGE"]`,
  `imageConfig: {"aspectRatio": "4:5", "imageSize": "2K"}`.
- **`4:5` é nativo aqui.** `imageSize: "2K"` sai 1856×2304, mesmo preço.
  `resolution` e `outputImageSize` → 400.
- Preços: `2.5-flash-image` $0,039 · `3-pro-image` $0,134 (1K/2K), $0,24 (4K).
  **Batch corta 50%** → $0,067, o que torna o Pro mais barato que o xAI 2.0 med/2k.

### Roteamento entre provedores

| Situação | Modelo |
|---|---|
| Ambiente é o assunto, produto pequeno ou ausente | Gemini `gemini-3-pro-image` |
| Produto grande, rótulo precisa ser legível | xAI `/images/edits` 2.0 med/2k |
| Rótulo exato ao pixel | composição do recorte real |

Gemini entrega cena mais natural; xAI preserva rótulo. Essa é a troca.

### Luz

- **Direção de luz não se dita no prompt.** O modelo ignora. Gere, **meça** a
  direção na imagem (especular de objeto cilíndrico, sentido das sombras) e
  reilumine a composição a partir do medido.
- A foto-fonte tem luz própria. O ambiente pedido **tem que herdar** essa direção,
  ou a imagem denuncia mesmo com o logotipo perfeito. `Suave (5).jpg` tem luz pela
  esquerda.
- **A luz real da fazenda é sol a pino**, céu azul com cumulus, sombra dura —
  iPhone 7, ISO 20, março, meio-dia. Não invente dia nublado: além de não existir
  naquele lugar, o alvo de calibração foi medido *nessas* fotos.

### Foco

Bloco anti-bokeh é **obrigatório**. Desfoque não se desfaz em pós — tone mapping,
ruído, halo e artefato de JPEG se adicionam depois; profundidade de campo rasa,
não. Morre na geração ou não morre.

A física a descrever: sensor 1/1.7" a f/1.8 dá profundidade de campo enorme; tudo
igualmente nítido; distância suaviza por névoa, nunca por desfoco; cantos moles
por lente larga barata.

### Espontaneidade

- Nada de derramado arrumado, objeto atravessado por cima, mesa posta.
- **Nenhum objeto que não exista naquele lugar.** A base real mostra: pé de café,
  terra vermelha, mangueira de irrigação, poste de madeira, arame, cadeira de
  plástico, galpão de zinco. Balança de cozinha, colher de cupping, bule de ágata e
  pano de crochê na lavoura são invenção.
- Comida: **meio comida**. Mordida, farelo, dourado desigual, crosta mate. Pedir
  comida bonita devolve render de comida.
- O modelo tem viés de **deixar o produto em pé**. Pedir "deitado no chão" costuma
  ser ignorado.

### Perfil de câmera medido

Alvo = nossas próprias fotos de celular (iPhone 7 na fazenda + Motorola nos
packshots), não gosto pessoal:

| Métrica | Alvo | Por que importa |
|---|---:|---|
| `p1` (ponto preto) | 14 | HDR de celular não desce mais que isso |
| `preto%` | 0,007 | celular quase nunca chega a preto puro |
| `estourado%` | 0,015 | celular estoura pequenas áreas sem pedir licença |
| saturação | 70 | nossa base é **lavada**, não vibrante |
| cast altas R/B | 0,969 | puxa **azul**; dourado quente é assinatura de IA |
| nitidez centro/borda | 1,57 | lente barata desaba nos cantos |
| ruído | 0,42 | leve; a geração já costuma vir com mais |

**O passe de pós deve ser mínimo — só saturação.** Duas tentativas de calibração
completa saíram *net-negativas*: corrigiam uma métrica e estragavam três.

**As métricas medem assinatura de dispositivo, não plausibilidade de conteúdo.**
Uma imagem bem calibrada com pão de queijo em formato errado é pior que uma com 2
métricas fora e comida crível. O alvo de `p1` também depende da luz da cena — 14
veio de sol forte; em luz difusa, sombra levantada é o comportamento correto.

---

## Método

- **HTTP 200 não prova que o parâmetro funcionou.** APIs ignoram campo
  desconhecido em silêncio. Verifique o *efeito*, não o status.
- **Erro é evidência barata.** 422 e 400 não geram imagem, logo não custam — e a
  mensagem costuma enumerar os valores válidos. Sonde com erro antes de gastar.
- Antes de concluir que um modelo não sabe fazer algo, confira se o *input* estava
  certo. Já concluí que "difusão não escreve marca" depois de mandar o **verso** do
  pacote como referência.
- Ao medir, valide a região amostrada. Já medi "ruído" numa área de textura de
  madeira e "sombra do caneco" em cima do próprio caneco.

---

## Registro de lições

Formato: **sintoma → causa raiz → regra**. Acrescente ao fim quando algo falhar.

1. **Logotipo saía genérico mesmo com referência** → a referência era o *verso* do
   pacote (QR, tabela nutricional), e o prompt não descrevia a arte → mostre a
   frente, e descreva a identidade elemento por elemento.
2. **Serra saiu como pico alpino nos 3 modelos** → meu DNA escrito dizia *"jagged
   peaks"*; a Serra da Canastra é chapada de topo plano → o modelo é obediente,
   ele erra exatamente onde a descrição erra.
3. **Guidance parecia não preservar nada** → `/images/edits` recebeu `image_url` e
   devolveu 200 ignorando a imagem → confira o efeito, não o status.
4. **Todos os testes de sondagem voltaram 422 de uma vez** → passei
   `aspect_ratio: "4:5"`, que não existe na xAI, envenenando a requisição inteira →
   valide o enum antes de varrer parâmetros.
5. **Imagem virou névoa leitosa** → `ImageChops.subtract` satura em 0; somar 128
   depois levanta tudo → use `add(..., offset=-128)` para ruído aditivo.
6. **Pacote reiluminado ficou incoerente com a cena** → assumi luz pela esquerda; o
   modelo renderizou pela direita → meça a direção antes de reiluminar.
7. **Passe de calibração piorou as métricas** → correção unidirecional e dupla
   correção de cor (R para cima *e* B para baixo) → correção com sinal, um canal só,
   e não toque em métrica já dentro da tolerância.
8. **Slide do carrossel saiu em madeira azul** quebrando a coesão → o prompt não
   proibia superfície pintada → em série, descreva o cenário compartilhado
   explicitamente e negue as variações.
9. **Commit de outra sessão caiu na minha branch** → duas sessões no mesmo
   diretório git → use worktree.
10. **Documentei uma garantia que não existia** → afirmei que o Instagram entrega no
    máximo 1080px, logo nada raspado passaria em `is_reference_grade`; li meu próprio
    `Counter` errado (o número que eu olhava era a altura) e o Instagram entrega
    1281px → não transforme em garantia escrita aquilo que você não mediu no arquivo
    real. Proteção que depende de um número do fornecedor não é proteção, é acidente.
11. **`python -m uv` sumiu do venv** → `uv sync` remove tudo que não está declarado no
    `pyproject.toml`, e o `uv` instalado via pip era exatamente isso → depois de
    qualquer `uv sync`, confira as ferramentas que vivem no venv sem estar no lock.
