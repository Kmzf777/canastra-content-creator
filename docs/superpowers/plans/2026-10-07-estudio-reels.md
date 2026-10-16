# estudio-reels Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir a semente `estudio-reels` (skill pessoal em `~/.claude/skills/estudio-reels/`) que se planta em qualquer repositório e produz Reels em motion de colagem narrado no padrão da peça 07 do Café Canastra, operando ChatGPT, ElevenLabs, Instagram e bancos de imagem pelo Chrome logado do usuário.

**Architecture:** Uma skill com tudo: `SKILL.md` maestro curto, uma página por fase (lida sob demanda), a mecânica de cada site em `navegador/`, as lições universais, e um `modelo/` com o motor Remotion de colagem e as ferramentas Python generalizados a partir de `instagram/remotion/` e `scripts/` deste repositório. `modelo/plantar.py` copia a skill para o repositório-alvo e monta `motion/`. Spec: `docs/superpowers/specs/2026-10-07-estudio-reels-design.md`.

**Tech Stack:** Remotion 4.0.530 + React 19 + TypeScript + vitest (motor); Python 3.10+ com numpy, pillow, opencv-python-headless, torch/torchaudio (ferramentas) + pytest; whisper.cpp via `@remotion/install-whisper-cpp`; Claude in Chrome (operação dos sites).

---

## Contrato comum (todas as tarefas obedecem)

### C1. Raiz da semente

`SEMENTE = C:/Users/rafae/.claude/skills/estudio-reels` (em outras máquinas, `~/.claude/skills/estudio-reels`).

```
estudio-reels/
  SKILL.md                      (Tarefa 1)
  VERSAO                        (Tarefa 0) conteúdo: 1.0.0
  fases/00-plantio.md           (Tarefa 1)
  fases/01-contexto.md, 02-concorrencia.md, 03-roteiro.md            (Tarefa 4)
  fases/04-narracao.md, 05-tempo.md, 06-assets.md, 07-montagem.md     (Tarefa 5)
  fases/08-conferencia.md, 09-publicacao.md, 10-retrospectiva.md      (Tarefa 6)
  navegador/chrome.md, instagram.md, chatgpt.md, elevenlabs.md, referencias.md, bancos-livres.md   (Tarefa 7)
  licoes.md                     (Tarefa 8)
  copy/kishotenketsu.md, oferta.md, criativos-anuncio.md                (Tarefa 12)
  navegador/meta-anuncios.md    (Tarefa 12)
  modelo/CONTRATO.md            (Tarefa 0) cópia desta seção
  modelo/plantar.py             (Tarefa 1)
  modelo/remotion/              (Tarefa 3)
  modelo/ferramentas/           (Tarefa 2)
```

### C2. O que o plantio cria no repositório-alvo `<repo>`

```
<repo>/.claude/skills/estudio-reels-<slug>/
  SKILL.md                 cópia do maestro com name/description da marca
  fases/  navegador/  copy/  licoes.md
  licoes-empresa.md        começa vazio (cabeçalho só)
  SEMENTE                  versão da semente de origem, ex.: 1.0.0
<repo>/motion/
  remotion/                cópia de modelo/remotion (sem node_modules)
  ferramentas/             cópia de modelo/ferramentas
  marca/dossie.md          (fase 01)  marca/identidade.json  marca/logo-*.png  marca/fontes/
  concorrencia/            (fase 02)
  referencias/             (fase 06) descritores e links
  biblioteca/indice.json   biblioteca/categorias.json  biblioteca/brutos/  biblioteca/pecas/<categoria>/
  pecas/NN-<tema>/         roteiro.txt, roteiro-tags.txt, fontes.md, narracao.mp3,
                           palavras-whisper.json, palavras.json, sons.json,
                           public/{fonte,colagem,sfx,assets}/, saida/,
                           legenda-post.md (orgânico) ou anuncio.md (modo oferta)
<repo>/.gitignore          + motion/remotion/node_modules/, motion/.venv/, motion/biblioteca/**/*.png,
                             motion/pecas/*/public/, motion/pecas/*/saida/, motion/ferramentas/whisper.cpp/
<repo>/CLAUDE.md           + 1 seção "Reels (estudio-reels)" apontando para a skill da marca
```

`<slug>`: minúsculas, `[a-z0-9-]`, derivado do nome da marca.

### C3. `motion/marca/identidade.json`

```json
{
  "marca": "Nome da Marca",
  "slug": "nome-da-marca",
  "idioma": "pt-BR",
  "cores": {"escuro": "#14100D", "claro": "#F1ECE0", "profundo": "#3B2A1F", "acento": "#C8661E", "apoio": "#4A5D3A"},
  "fontes": {
    "manchete": {"familia": "Archivo Black", "arquivo": null, "peso": 400},
    "corpo": {"familia": "Inter", "arquivo": null, "peso": 700},
    "dado": {"familia": "IBM Plex Mono", "arquivo": null, "peso": 500}
  },
  "logo": {"sobre_claro": "logo-escura.png", "sobre_escuro": "logo-clara.png"},
  "voz": {"plataforma": "elevenlabs", "nome": null, "modelo": "v4"},
  "exemplo": false
}
```

`arquivo: null` = usar a fonte padrão empacotada no motor. Mapeamento das cores do Canastra para os papéis genéricos: `preto→escuro`, `creme→claro`, `terra→profundo`, `acento→acento`, `verde→apoio`.

### C4. Ferramentas Python (`motion/ferramentas/`, rodadas da raiz do `<repo>`)

| Arquivo | Linha de comando |
|---|---|
| `_ffmpeg.py` | módulo: `ffmpeg()`, `ffprobe()` — acha o binário em `motion/remotion/node_modules/@remotion/compositor-*/` (Windows `ffmpeg.exe`; macOS/Linux `ffmpeg`), senão o do PATH |
| `alinhar_narracao.py` | `python motion/ferramentas/alinhar_narracao.py <whisper.json> <roteiro.txt> <audio16k.wav> <saida.json>` |
| `alinhar_forcado.py` | `python motion/ferramentas/alinhar_forcado.py <palavras-whisper.json> <audio> [saida.json]` |
| `conferir_alinhamento.py` | `python motion/ferramentas/conferir_alinhamento.py pausas <palavras.json> <audio>` · `... faixa <palavras.json> <audio> 1.2-3.4 [--com outro.json]` |
| `biblioteca.py` | `buscar <termos...>` · `listar [categoria]` · `publicar <NN-tema> <ids...>` · `registrar <nome> <categoria> <arq...> --tags a,b --origem <origem> [--bruto F] [--prompt T] [--fonte URL] [--dia AAAA-MM-DD] [--substituir]` |
| `recortar_folha.py` | `python motion/ferramentas/recortar_folha.py <folha.png> --nomes a,b,c --categoria C --tags t1,t2 --prompt "..." [--limiar 22] [--juntar 24] [--area-min 2500] [--convexo a,b] [--lente a] [--filete 9] [--reticula] [--dia AAAA-MM-DD]` |
| `foto_papel.py` | `python motion/ferramentas/foto_papel.py <foto> <nome> --categoria foto-real --tags ... --origem real-verificada|banco-livre [--fonte URL] [--largura 900] [--recorte x0,y0,x1,y1]` |
| `sons.py` | `python motion/ferramentas/sons.py motion/pecas/<NN-tema>` (lê `sons.json` e `palavras.json` da peça; grava `public/sfx/*.wav`) |
| `varrer_movimento.py` | `python motion/ferramentas/varrer_movimento.py <video.mp4> [q1,q2,...]` |
| `folha_do_video.py` | `python motion/ferramentas/folha_do_video.py <video.mp4> <saida.png> <q1,q2,...> [colunas]` |
| `instalar.py` | `python motion/ferramentas/instalar.py [--sem-modelos]` — cria `motion/.venv`, instala `requirements.txt`, roda `npm install` em `motion/remotion`, instala whisper.cpp `small` em `motion/ferramentas/whisper.cpp/`; avisa tamanhos antes. `--sem-modelos` pula whisper.cpp, torch e torchaudio (para teste rápido) |

Origens válidas: `gerado-chatgpt`, `real-verificada`, `real-nao-verificada`, `banco-livre`, `codigo`.
Categorias: lidas de `motion/biblioteca/categorias.json` (criado com padrão: `objeto`, `utensilio`, `natureza`, `alimento`, `produto`, `foto-real`, `textura`, `papelaria`, `grafismo`, `maos`).

`motion/pecas/<NN-tema>/sons.json`:

```json
{"bpm": 88, "secoes": [
  {"frase": "Calma", "tipo": "groove"},
  {"frase": "E aqui vem", "tipo": "respiro"},
  {"frase": "Por isso a gente", "tipo": "groove"},
  {"frase": "Salva esse vídeo", "tipo": "fecho"}
]}
```

Antes da primeira seção é sempre `tensao`. `DUR` = última palavra + 0,5 s arredondado para cima ao décimo.

### C5. Motor Remotion (`motion/remotion/`)

| Caminho | Papel |
|---|---|
| `package.json` | dependências do motor do Canastra (mesmas versões) + `@remotion/bundler`, `@remotion/renderer`, `pngjs` |
| `src/index.ts` · `src/Raiz.tsx` | registra as composições; vem com `Exemplo` (1080×1920, 30 fps) |
| `src/identidade/tokens.ts` | `COR` e `TIPO` lidos de `../../../marca/identidade.json` (via import JSON); `AUDIO = {lufs: -14, picoDbtp: -1}` |
| `src/identidade/tipografia.ts` · `src/identidade/fontes/` | `PILHA`, carregamento com guarda; fontes padrão OFL (Archivo Black, Inter Bold, IBM Plex Mono Medium) |
| `src/colagem/*` | motor de colagem portado (camera, palco, legenda, tipos, grafismos, movimento-colagem, semente, fontes-colagem, pecas) |
| `src/pecas/_modelo/` | esqueleto genérico (roteiro.ts, apoio.tsx, cenas.tsx com 3 cenas de exemplo, Peca.tsx com chicote colado, Sons.tsx) que lê `motion/pecas/00-exemplo/palavras.json` |
| `src/audio/normalizar.ts` · `scripts/normalizar-audio.mjs` | normalizador com teto pedido 0,6 dB abaixo e novas tentativas pelo excesso medido |
| `scripts/contato.mjs` | `node scripts/contato.mjs <Comp> <NN-tema> <s1,s2,...> [--escala=0.25] [--cols=8] [--saida=x.png]` (public dir = `../pecas/<NN-tema>/public`) |
| `tests/` | legenda/câmera (portados) e roteiro do modelo (FIM derivado, A/B) |

Peça nova: copiar `src/pecas/_modelo/` → `src/pecas/<NN-tema>/`, trocar o import do `palavras.json`, registrar em `Raiz.tsx`.

### C6. Regras para os agentes de implementação

- Escrevem só nos caminhos da sua tarefa. **Não fazem commit** (o orquestrador commita).
- Português do Brasil em docs, comentários e mensagens; nomes de arquivos sem acento.
- Nada específico do Café Canastra fica na semente (fatos de café, nomes de SKU, @ de concorrentes, caminhos `instagram/` ou `projetos/07-...`), exceto quando citado como **exemplo** marcado.
- Fonte para portar: este repositório, `C:/Users/rafae/OneDrive/Desktop/Canastra Inteligencia/Agentes AI/Canastra-Content-Creator`.

---

### Tarefa 0: Esqueleto da semente (orquestrador, antes das demais)

**Files:**
- Create: `SEMENTE/VERSAO`, `SEMENTE/modelo/CONTRATO.md`, pastas `fases/`, `navegador/`, `modelo/remotion/`, `modelo/ferramentas/`

- [ ] **Step 1:** criar as pastas e `VERSAO` com `1.0.0`.
- [ ] **Step 2:** copiar a seção "Contrato comum" deste plano para `modelo/CONTRATO.md`.
- [ ] **Step 3:** `git init` em `SEMENTE` (sem remoto) e `.gitignore` com `modelo/remotion/node_modules/`, `__pycache__/`, `*.pyc`.

### Tarefa 1: Maestro e plantio

**Files:**
- Create: `SEMENTE/SKILL.md`, `SEMENTE/fases/00-plantio.md`, `SEMENTE/modelo/plantar.py`, `SEMENTE/modelo/tests/test_plantar.py`

- [ ] **Step 1: teste do plantio primeiro** (`modelo/tests/test_plantar.py`, pytest, usa `tmp_path`):
  - planta numa pasta vazia com `--marca "Café Teste"` → existe `.claude/skills/estudio-reels-cafe-teste/SKILL.md` com `name: estudio-reels-cafe-teste`; existe `motion/remotion/package.json`, `motion/ferramentas/biblioteca.py` (crie arquivos-fantasia em `modelo/remotion` e `modelo/ferramentas` dentro do `tmp_path` para o teste não depender das Tarefas 2/3: `plantar.py` recebe `--semente <dir>`);
  - `SEMENTE` (arquivo) contém a versão lida de `VERSAO`;
  - `.gitignore` recebe as linhas de C2 uma vez só (rodar duas vezes não duplica);
  - `CLAUDE.md` ganha a seção uma vez só;
  - `motion/marca/identidade.json` e `motion/pecas/00-exemplo/palavras.json` existem depois do plantio (o teste fabrica `modelo/exemplo/` no `tmp_path`);
  - plantar de novo sem `--atualizar` recusa (a cópia do repo já existe e pode ter evoluído);
  - `--atualizar` copia `fases/`, `navegador/`, `licoes.md` e `motion/ferramentas/*.py` novos, **sem tocar** em `licoes-empresa.md`, `motion/marca/`, `motion/pecas/`, `motion/biblioteca/` nem em arquivo do repo cujo conteúdo difere do que a semente plantou (esses são listados como conflito para revisão).
- [ ] **Step 2:** rodar `python -m pytest modelo/tests/test_plantar.py -q` e ver falhar.
- [ ] **Step 3:** implementar `modelo/plantar.py`:
  `python plantar.py <repo> --marca "<Nome>" [--semente <dir>] [--atualizar]`. Copia `SKILL.md`, `fases/`, `navegador/`, `licoes.md` para `<repo>/.claude/skills/estudio-reels-<slug>/`, reescrevendo o frontmatter (`name: estudio-reels-<slug>`; `description: Use when producing or auditing any Reel, motion or vertical video for <Marca> in this repository — copy, narração ElevenLabs, sincronia de legenda, assets de colagem, render Remotion, conferência, descrição do post — or when the reels skill of this repo must learn from a failure.`); cria `licoes-empresa.md` e `SEMENTE`; copia `modelo/remotion` (sem `node_modules`) para `motion/remotion` e `modelo/ferramentas` para `motion/ferramentas`; cria as pastas de C2 com `.gitkeep`; cria `motion/biblioteca/indice.json` (`[]`) e `categorias.json` (padrão de C4); copia `modelo/exemplo/identidade.json` para `motion/marca/identidade.json` (marcado `"exemplo": true` — a fase 01 substitui; sem ele o motor não compila) e `modelo/exemplo/00-exemplo/` para `motion/pecas/00-exemplo/`; acrescenta `.gitignore` e a seção do `CLAUDE.md` de forma idempotente; grava `motion/.plantio.json` com o sha256 de cada arquivo copiado (é o que o `--atualizar` usa para saber o que o repo mudou).
- [ ] **Step 4:** testes passam.
- [ ] **Step 5:** escrever `SKILL.md` (≤ 120 linhas): frontmatter `name: estudio-reels`, `description: Use when the user wants Reels, motion, vertical video or narrated collage content for the company of the current repository and the repository has no estudio-reels-<marca> skill yet, or when asked to plant, update or promote the estudio-reels skill.`; corpo: (a) se existe `.claude/skills/estudio-reels-*/` no repo, **pare e use aquela** (é a versão evoluída); (b) senão, fase 00; (c) tabela das 11 fases com o arquivo de cada uma e "leia a fase só quando chegar nela"; (d) regras que não se negociam (§7 da spec, em lista curta); (e) autonomia: gera e refaz sozinho, **para no roteiro**; (f) o ciclo plantar → produzir → retrospectiva → promover → atualizar.
- [ ] **Step 6:** escrever `fases/00-plantio.md`: pré-requisitos (Chrome + Claude in Chrome + contas logadas; Node ≥ 18; Python ≥ 3.10; ~3 GB livres), comandos (`python <SEMENTE>/modelo/plantar.py . --marca "<Nome>"`, depois `python motion/ferramentas/instalar.py`), conferência (`npx tsc --noEmit` e `npx vitest run` em `motion/remotion`; `python -m pytest motion/ferramentas/tests -q`), e o que fazer se algo faltar (parar e dizer exatamente o que instalar).

### Tarefa 2: Ferramentas Python generalizadas

**Files:**
- Create: `SEMENTE/modelo/ferramentas/{_ffmpeg,alinhar_narracao,alinhar_forcado,conferir_alinhamento,biblioteca,recortar_folha,foto_papel,sons,varrer_movimento,folha_do_video,instalar}.py`, `requirements.txt`, `tests/test_*.py`
- Port from: `scripts/alinhar_narracao.py`, `scripts/alinhar_forcado.py`, `scripts/conferir_alinhamento.py`, `scripts/biblioteca_colagem.py`, `scripts/colagem_assets.py` (+ `lente_transparente` de `colagem_assets_v2.py`), `scripts/colagem_sfx.py` + `scripts/colagem_sfx_v2.py`, `scripts/varrer_movimento.py`, `scripts/folha_do_video.py`

- [ ] **Step 1: testes primeiro** (`tests/`, pytest, sem rede, sem modelo grande):
  - `test_extenso.py`: `por_extenso` para 0, 1, 16, 21, 80, 85, 100, 101, 350, 999, 1000, 1020, 1100, 1250, 1985, 2000, 2026 (valores esperados como em `scripts/alinhar_narracao.py`).
  - `test_biblioteca.py`: com `tmp_path` como raiz — registrar, recusar id repetido sem `--substituir`, `publicar` copia para `motion/pecas/<p>/public/colagem/<nome>-bN.png` e recusa dois nomes iguais no mesmo projeto, categoria fora de `categorias.json` recusa.
  - `test_recortar.py`: folha sintética 1200×800 branca com 3 formas coloridas afastadas → 3 peças × 3 variantes; **as 3 variantes de cada peça têm o mesmo tamanho**; `--nomes` com contagem errada falha com mensagem.
  - `test_conferir.py`: wav sintético (silêncio, tom, silêncio, tom) + `palavras.json` fabricado → `pausas` acha os 2 ataques.
  - `test_sons.py`: `palavras.json` fabricado + `sons.json` → gera `trilha.wav` com duração = `DUR` e os efeitos padrão; seção cuja frase não existe falha com mensagem.
  - `test_ffmpeg.py`: `ffmpeg()` devolve caminho executável quando existe `node_modules/@remotion/compositor-*/ffmpeg(.exe)` fabricado em `tmp_path`.
- [ ] **Step 2:** `python -m pytest tests -q` falha.
- [ ] **Step 3:** portar. Regras: caminhos relativos à raiz do repo (`motion/...`), nunca `instagram/` ou `projetos/`; ffmpeg via `_ffmpeg.py`; `biblioteca.py` com raiz `motion/biblioteca`, projetos `motion/pecas`, categorias de `categorias.json`, as travas de `registrar`/`publicar` já existentes; `recortar_folha.py` = `separar` + `convexo` + `lente_transparente` + `peca` (união dos bboxes) + registrar; `foto_papel.py` = `foto_rasgada` (com `exif_transpose`) + registrar; `sons.py` = efeitos do `colagem_sfx.py` + trilha em seções por frase (C4); `instalar.py` conforme C4, imprimindo o tamanho do que vai baixar antes de baixar; `requirements.txt` com `numpy`, `pillow`, `opencv-python-headless`, `torch`, `torchaudio`, `pytest`.
- [ ] **Step 4:** testes passam; `python -m py_compile` em todos.

### Tarefa 3: Motor Remotion generalizado

**Files:**
- Create: `SEMENTE/modelo/remotion/**` conforme C5, mais `SEMENTE/modelo/remotion/README.md`
- Port from: `instagram/remotion/{package.json,tsconfig.json,src/colagem/*,src/identidade/{tokens,tipografia}.ts,src/identidade/fontes/*,src/colagem/fontes/*,src/pecas/especial/*,src/motor/audio/normalizar.ts,scripts/contato.mjs,scripts/normalizar-audio.mjs,tests/colagem-camera-legenda.test.ts,tests/especial-roteiro.test.ts}`

- [ ] **Step 1:** copiar o motor de colagem e o que ele importa; trocar `COR.preto/creme/terra/acento/verde` por `COR.escuro/claro/profundo/acento/apoio` em todos os arquivos portados; `tokens.ts` lê `identidade.json` (C3) por import JSON com `resolveJsonModule`.
- [ ] **Step 2:** esqueleto `src/pecas/_modelo/` a partir de `src/pecas/especial/`: 3 cenas de exemplo (gancho com Recortadas + Elipse, conteúdo com Dymo + Marcador `dur={fala()}` + pílula, fecho com logo da marca), chicote colado em `Peca.tsx`, `Sons.tsx` lendo `public/sfx/`; nenhum segundo digitado (`em()`, `depois()`, `TROCA`, `CENA_INICIO`, `FIM` derivado). Dados de exemplo em `SEMENTE/modelo/exemplo/00-exemplo/{palavras.json,roteiro.txt,sons.json}` (texto curto genérico, ~12 s, tempos fabricados plausíveis) — `plantar.py` copia para `motion/pecas/00-exemplo/`. O `identidade.json` de exemplo vai em `SEMENTE/modelo/exemplo/identidade.json` (cores do Canastra como valores de exemplo).
- [ ] **Step 3:** portar `normalizar.ts` + `normalizar-audio.mjs` (com `MARGEM_AAC_DB` e tentativas) e `contato.mjs` (public dir da peça conforme C5).
- [ ] **Step 4:** testes vitest portados e adaptados ao `_modelo` (A/B exclusivo, toda palavra em A, B ou mudo, pílula ≤ 4 palavras / 16 caracteres / ≥ 0,2 s, `FIM` derivado).
- [ ] **Step 5:** verificação numa cópia de trabalho fora da semente (para não poluir com `node_modules`): copiar `modelo/remotion` para `%TEMP%/estudio-reels-teste/motion/remotion`, `modelo/exemplo/00-exemplo` para `.../motion/pecas/00-exemplo`, `modelo/exemplo/identidade.json` para `.../motion/marca/`; `npm install`; `npx tsc --noEmit`; `npx vitest run`; `npx remotion still src/index.ts Exemplo saida.png --frame=60 --public-dir=../pecas/00-exemplo/public` — tudo verde e o still abre. Registrar no `README.md` os comandos e o resultado.

### Tarefa 4: Fases 01–03 (contexto, concorrência, roteiro)

**Files:** Create `SEMENTE/fases/01-contexto.md`, `02-concorrencia.md`, `03-roteiro.md`
**Fontes:** spec §4; `.claude/skills/canastra-video/colagem.md` §1–§3; `instagram/estrategia/{LEIA-ME,02-ganchos,03-roteiro,07-nao-fazer}.md`; `Direcao-Criativa.md` (só como exemplo de dossiê); `base-curada/LEIA-ME.md` (camadas de permissão).

- [ ] **01-contexto.md**: o que ler no repo; roteiro de pesquisa pelo Chrome (site: produtos, preços, promessas, tom; Instagram: seguidores, cadência, 9 posts de topo, bio; Google: notícias, avaliações); régua de origem dos fatos ([oficial], [medido], [criador], [terciário], [folclore]) e o que vira fala; modelo de `marca/dossie.md`; extração de `identidade.json` (cores do logo/site, fontes do site — fonte comercial não licenciada vira a padrão do motor); perguntas de nicho só do que faltou (AskUserQuestion, uma por vez, opções concretas); pedido do banco de imagens e as 4 camadas (própria verificada com EXIF · própria sem prova · terceiro = referência · sintética/baixa = quarentena); escolha da voz da marca na 1ª peça.
- [ ] **02-concorrencia.md**: como sugerir concorrentes (busca do Instagram por termo do nicho, hashtags, Google "melhores <nicho> instagram") e referências de formato; confirmação do usuário; por perfil: aba Reels, views, 3 reels de topo; estudo com a skill `watch` se instalada, senão quadros pelo Chrome; o que medir (texto do gancho a 0,5 s, duração, cortes/s, sistemas de texto, CTA, views); modelo de `concorrencia/estudo-<data>.md`; terceiro só como texto.
- [ ] **03-roteiro.md**: escolha de pauta (lacuna no estudo × força do dossiê); a pauta não acusa produto da empresa (conferir torra/origem/processo de cada produto contra a tese; conflito = `não verificável` → perguntar); estrutura da peça 07 com tempos; retenção (2 promessas, dado a cada 8–10 s, frase repetível, salvar no fim); tabela fato → fonte; `roteiro.txt` (fala exata, números por extenso, sem tags) e o texto com tags para a ElevenLabs; **PARADA**: mostrar roteiro + fontes e esperar OK.

### Tarefa 5: Fases 04–07 (narração, tempo, assets, montagem)

**Files:** Create `SEMENTE/fases/04-narracao.md`, `05-tempo.md`, `06-assets.md`, `07-montagem.md`
**Fontes:** `colagem.md` §3–§7; lições 49–61 do `CLAUDE.md`; C4/C5 deste plano.

- [ ] **04-narracao.md**: tags da v4 (uma por trecho, inglês, reticências, `[pause]`), texto inteiro numa geração, 3 tomadas, voz da marca; mecânica no Chrome remetendo a `navegador/elevenlabs.md`; escolha da tomada (transcrever cada uma com whisper, comparar com o roteiro, duração); aceleração local se pedida; gravar `motion/pecas/<NN>/public/fonte/narracao.mp3`.
- [ ] **05-tempo.md**: comandos de C4 na ordem (wav 16 kHz → whisper.cpp → `alinhar_narracao` → `alinhar_forcado` → `conferir_alinhamento pausas` → `faixa` nos suspeitos); como ler o envelope; régua (mediana ~0,02 s, máx ~0,15 s); voz nova = ler um ataque por frase; nunca reaproveitar tempo de outra versão.
- [ ] **06-assets.md**: ordem de busca (biblioteca → banco da empresa → Unsplash/Pexels → ChatGPT); folha do ChatGPT sobre #FFFFFF (objetos afastados, sem texto, sem embalagem, sem rosto); referência de terceiro permitida com as travas (spec §7.3) e a conferência anti-cópia lado a lado; `recortar_folha.py`/`foto_papel.py`/`biblioteca.py publicar`; registrar sempre com o prompt; nomes únicos.
- [ ] **07-montagem.md**: copiar `_modelo`; `roteiro.ts` com `b/mudo/t` na ordem; tabela `em()/depois()/TROCA/CENA_INICIO/FIM`; planos e câmera; chicote colado ou cobertura em toda troca; Dymo/Serifa/Marcador(`dur`)/Recortadas/Pílula; área segura (x 140–940, fora de 5% topo e 16% base); embalagem só recorte real com o alfa medido, nunca texto sobre logo/selo; som por entrada + `sons.json`; registrar composição.

### Tarefa 6: Fases 08–10 (conferência, publicação, retrospectiva)

**Files:** Create `SEMENTE/fases/08-conferencia.md`, `09-publicacao.md`, `10-retrospectiva.md`
**Fontes:** `colagem.md` §8–§9; `instagram/remotion/projetos/07-cafe-especial-colagem/legenda-post.md`; a pesquisa de descrição desta sessão (spec §4 fase 09); lições 56–62.

- [ ] **08-conferencia.md**: tabela de 8 passos (tipos/testes → alinhamento → stills dirigidos → render de teste + `varrer_movimento` → render final → normalizar → `folha_do_video` + ffprobe → entrega cedo e limpeza); comandos exatos de C4/C5; abortar render (árvore do processo pela linha de comando); "sinais de que você está saindo do padrão".
- [ ] **09-publicacao.md**: molde da descrição (1ª linha ≤ ~55 caracteres com a busca; colinha; fontes; pergunta aberta; ≤ 5 hashtags; o que é real dito só se veio do banco próprio verificado); checklist (rótulo de IA, localização, capa 3:4, "aparecer em buscadores"); publicar pelo Chrome só com OK explícito na hora; as fontes da pesquisa como links.
- [ ] **10-retrospectiva.md**: formato da lição (sintoma → causa raiz → regra); onde gravar (`licoes-empresa.md` vs `licoes.md` da cópia); quando uma lição vira regra numa fase ou correção em `motion/`; commit; **promoção**: listar universais (site, ferramenta, motor, método), pedir OK, aplicar na semente (`fases/`, `navegador/`, `licoes.md`, `modelo/`), subir `VERSAO` (patch para lição, minor para fase/ferramenta nova), commit no git da semente; **atualização**: `plantar.py --atualizar` e como tratar os conflitos listados.

### Tarefa 7: Navegador

**Files:** Create `SEMENTE/navegador/{chrome,instagram,chatgpt,elevenlabs,referencias,bancos-livres}.md`
**Fontes:** lições 16, 34–37, 39–42, 45, 50–52 do `CLAUDE.md`; `.claude/skills/canastra-conteudo/SKILL.md` (mecânica do ChatGPT); skill `anthropic-skills:chrome-browser` (regras do Claude in Chrome); spec §5 e §7.

- [ ] **chrome.md**: carregar as ferramentas numa só busca; abas novas; login do usuário (parar e pedir); downloads com nome escolhido e conferidos pelo nome; um download por aba; ler o campo antes de enviar; `requestSubmit()` em aba de fundo; clique por coordenada lida no screenshot quando o rect mente; `Escape` para fechar overlay; site mudou → screenshot, adaptar, lição; travas (nunca publicar/comprar/aceitar termos/digitar senha/resolver captcha).
- [ ] **instagram.md**: perfil, aba Reels, leitura de views, abrir reel, legenda, quadros; volume baixo; terceiro só texto.
- [ ] **chatgpt.md**: nova conversa por folha; anexar referência; prompt de folha sobre branco; enviar; esperar a imagem; baixar pelo blob com nome; follow-up de edição regenera o quadro (lição 45) — corrigir em conversa nova ou localmente.
- [ ] **elevenlabs.md**: Text to Speech; conferir o rótulo do modelo (v4) e a voz; colar o texto com tags; gerar; baixar cada tomada com nome; ler o saldo; sem crédito → parar. Marcar como **a validar no piloto** cada passo cuja tela não foi vista nesta sessão.
- [ ] **referencias.md**: Pinterest/Google Imagens: busca, descritor em texto + link; o que pode subir ao ChatGPT (spec §7.3) e o que nunca sobe.
- [ ] **bancos-livres.md**: Unsplash/Pexels: busca, filtro de orientação vertical, download em resolução cheia, guardar URL como `--fonte`.

### Tarefa 8: Lições universais

**Files:** Create `SEMENTE/licoes.md`
**Fonte:** `CLAUDE.md` deste repositório, lições 1–62.

- [ ] **Step 1:** classificar cada lição: universal (site, ferramenta, motor, método, geração de imagem) ou Canastra (fatos do café, SKUs, contas). Só as universais entram.
- [ ] **Step 2:** reescrever cada universal no formato **sintoma → causa → regra**, sem nome de produto ou conta, mantendo os números medidos que provam a regra; agrupar por tema (Geração de imagem · Chrome e sites · Vídeo e Remotion · Áudio e alinhamento · Método); numerar.
- [ ] **Step 3:** no fim, a tabela "origem" (número da lição no Canastra → número aqui) para rastreio.

### Tarefa 12: Copy, oferta e criativo de anúncio (acrescentada depois da onda paralela)

Pedido do usuário: a skill tem que ter o princípio do HardCopy para criar ofertas e bons
criativos, como modo de conteúdo, e prender quem assiste até o fim em venda, educativo ou
geral. Pesquisa: `docs/superpowers/specs/2026-10-07-estudio-reels-copy-pesquisa.md`. Spec:
§2 (linha Copy), §4.1 (modos), §7.1–7.2 (travas de anúncio e de oferta).

**Files (12a, agora — arquivos novos, disjuntos da onda):**
- Create: `SEMENTE/copy/kishotenketsu.md`, `SEMENTE/copy/oferta.md`,
  `SEMENTE/copy/criativos-anuncio.md`, `SEMENTE/navegador/meta-anuncios.md`

- [ ] **kishotenketsu.md**: origem (起承轉合 → 起承転結) em 3 linhas; os 4 tempos, com o
  *ten* como pivô que reenquadra, não necessariamente conflito; os 4 modos de §4.1 com
  molde por duração (porcentagem e segundos de cada tempo); a variante "ketsu primeiro" do
  anúncio; os 3 esqueletos chineses de vídeo que vende (preço · efeito · dor) e os 3 tipos
  japoneses de anúncio (problema→solução · demonstração · oferta direta); retenção com o
  grau de evidência de cada regra (lacuna de informação com contexto; toda promessa paga;
  pergunta→resposta curta; Zeigarnik **não** se cita); checklist "prende até o fim"; a
  peça 07 mapeada nos 4 tempos como exemplo marcado.
- [ ] **oferta.md**: campos do briefing; Big Idea ×3 (ângulos distintos) e escolha no ponto
  de parada do roteiro; promessa, mecanismo, prova (só [oficial]/[medido]), oferta
  empilhada, bônus, garantia, urgência real, objeção principal, CTA e destino;
  conformidade com fontes públicas conferidas na hora (CDC arts. 37 e 49; Código do CONAR;
  Padrões de Publicidade da Meta — atributos pessoais, antes/depois, alegação de saúde e
  dinheiro; LGPD para depoimento); nicho regulado = parar e pedir a regra do setor.
- [ ] **criativos-anuncio.md**: formato 9:16; área segura de anúncio (14/35/6 → y
  269–1248, x 65–1015 em 1080×1920) contra a do orgânico; abertura de 3 s (0,5 s imagem
  de produto/dor/resultado → promessa em texto até 1,5 s → prova até 3 s), legenda
  queimada; 3–5 ganchos sobre o mesmo corpo (corpo narrado uma vez + ganchos à parte +
  junção por ffmpeg + alinhamento sobre a junção, uma pasta `NN-tema-gK` por variação);
  cartão final com oferta + CTA + logo real; render 1440×2560 com a escala derivada da
  largura (lição VID de escala); edição cinética mapeada no motor (sem respiro morto, uma
  frase por tela, fundo por frase, figurinha na cor da palavra, quebra de padrão com foto
  real de banco livre — nunca rosto sintetizado —, tremor, trilha + impacto); métricas
  lidas no Gerenciador (taxa de gancho = reproduções de 3 s ÷ impressões; retenção; CTR;
  CPA/ROAS se houver) e a tabela de diagnóstico; travas (§7.1).
- [ ] **meta-anuncios.md**: Biblioteca de Anúncios (pública, sem login; país; busca por
  anunciante ou termo; filtros ativo/vídeo; "veiculação iniciada em"; versões do mesmo
  criativo; o que anotar; sinal, não prova) e Gerenciador (só leitura; onde ler as
  colunas; nunca editar, publicar, duplicar ou gastar). Passos de tela não vistos nesta
  sessão marcados **a validar no piloto**.

**12b (orquestrador, depois que as Tarefas 1, 3, 5 e 7 voltarem):** apontar o `copy/`
no `SKILL.md` (tabela de arquivos, modo de conteúdo, trava de anúncio), nas fases 02
(ramo da Biblioteca de Anúncios), 03 (escolha do modo no passo 1; Big Ideas no ponto de
parada), 04 (variações de gancho), 07 (área segura de anúncio, cartão final), 08 (stills
de área segura, render das variações), 09 (`anuncio.md` em vez de descrição) e 10
(métricas só leitura); `plantar.py` copia `copy/` na plantação e no `--atualizar` (com
teste); motor com `AREA_SEGURA.organico/anuncio` lido pela pílula, com teste vitest
(pílula inteira acima de y 1248 no modo anúncio).

### Tarefa 9: Integração (orquestrador, depois das Tarefas 1–8 e 12)

- [ ] **Step 1:** conferir referências cruzadas: todo comando citado nas fases existe em C4/C5 com a mesma assinatura; todo arquivo citado existe.
- [ ] **Step 2:** rodar `python -m pytest modelo/tests modelo/ferramentas/tests -q` na semente.
- [ ] **Step 3:** plantio de ponta a ponta numa pasta temporária: `git init`; `python <SEMENTE>/modelo/plantar.py . --marca "Teste"`; `python motion/ferramentas/instalar.py --sem-modelos` (pula whisper/torch no teste); `npx tsc --noEmit`, `npx vitest run`, `npx remotion still ... Exemplo` em `motion/remotion`.
- [ ] **Step 4:** commit inicial no git da semente: `estudio-reels 1.0.0`.

### Tarefa 10: Teste da skill com agentes (TDD de skill)

- [ ] **Step 1 (linha de base):** em pasta temporária com um `README.md` de uma empresa fictícia, agentes respondem a 3 cenários **sem** a semente: plantar e montar contexto; planejar roteiro + narração; conferir e entregar. Registrar onde falham.
- [ ] **Step 2 (com a semente):** os mesmos cenários lendo `~/.claude/skills/estudio-reels/SKILL.md`. Aceitar quando seguem as fases, citam os comandos de C4/C5 e respeitam a parada no roteiro e as travas.
- [ ] **Step 3:** fechar no texto da semente o que os agentes errarem; repetir o cenário que falhou.

### Tarefa 11: Piloto real (precisa do usuário)

- [ ] **Step 1:** perguntar ao usuário qual repositório/empresa e confirmar que o Chrome está com Instagram, ChatGPT e ElevenLabs logados.
- [ ] **Step 2:** rodar as fases 00–10 numa peça de ~30 s, validando em especial `navegador/elevenlabs.md` e os downloads.
- [ ] **Step 3:** retrospectiva → lista de promoção → semente 1.1.0.

---

## Ordem de execução

- Tarefa 0 (orquestrador) → **onda paralela**: Tarefas 1, 2, 3, 4, 5, 6, 7, 8 (8 agentes, arquivos disjuntos) + 12a (arquivos novos) → 12b (orquestrador, quando 1/3/5/7 voltarem) → Tarefa 9 (orquestrador) → Tarefa 10 (agentes, com um cenário de criativo de oferta) → Tarefa 11 (com o usuário).
