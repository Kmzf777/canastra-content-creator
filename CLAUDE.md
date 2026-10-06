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
| `mercadolivre/LEIA-ME.md` | **Mercado Livre.** Resumo de sessão, estado da conta, o que foi corrigido e o que segue sem verificação. **Leia antes de mexer no ML** |

### Skills de conteúdo (`.claude/skills/`)

Todo trabalho de imagem passa por elas. O fluxo é sempre o mesmo — curadoria de
referência, prompt, Claude in Chrome no ChatGPT, conferência ampliada, registro.

| Skill | Quando |
|---|---|
| `canastra-conteudo` | hub: qualquer imagem. Dono do fluxo, da mecânica do ChatGPT e da conferência |
| `canastra-embalagem` | a embalagem aparece legível — rótulo tem que sobreviver letra por letra |
| `canastra-cena` | lavoura, mesa, torrefação, UGC — realismo e procedência da referência |
| `canastra-mercadolivre` | mexer na Central do ML pelo navegador — o que grava, o que falha em silêncio |
| `canastra-estatico` | post estático de feed — o catálogo declarado e a escada de correção do rótulo |
| `canastra-carrossel` | carrossel de feed — os 10 tipos de slide, o ritmo e os três portões |
| `canastra-direcao` | direção de foto — que chão, que luz, que prop, que paleta. Os looks nomeados |

A regra que mais se perde, e que um agente de teste furou neste repositório:
**só marque um campo como conferido se a referência permitir lê-lo.** Ilegível não
é "confere", é `não verificável` — pergunte o valor e soletre no prompt.

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
12. **O Gemini segura o enquadramento quando o prompt é ordem de edição, não de cena**
    → em 18/08 concluí que "o Gemini trata a referência como inspiração"; o teste era
    de *geração de cena*, onde ele de fato reconstrói. Numa **troca de fundo** com o
    prompt aberto em `EDIT THE PROVIDED PHOTOGRAPH` + `KEEP THE PACKAGE
    PIXEL-FOR-PIXEL IDENTICAL`, os 3 SKUs saíram com posição, escala, recorte, vincos
    e brilho especular indistinguíveis da fonte (conferido por blend a 50% —
    `saida-teste/site-fundo-branco/_conferencia-posicao.jpg`) → a frase "referência é
    inspiração" vale para cena, não para edição. Abra o prompt nomeando a operação.
13. **`Desde 1985` virou `Doodo 1985` e `TORRADO E MOÍDO` virou `TRODULB E HÚMO`**
    numa troca de fundo que não pedia mudança nenhuma no rótulo → o Gemini
    **redesenha o quadro inteiro**, não copia pixel; então tipografia pequena é
    reescrita mesmo em "edição", e abaixo de ~2% da altura do quadro ela não
    sobrevive. Deu 1 acerto em 3 no Clássico, 1 em 1 no Suave e no Canela (texto
    maior) → em troca de fundo, `--n 3` e confira **com recorte ampliado da faixa de
    texto**, não olhando a imagem inteira: em miniatura os três erros passam batido.
14. **Refiz o verso da embalagem e a arte vazou para fora da embalagem** — foto
    ocupando 100% da tela, texto por cima das marcas de corte → tratei
    `verso-embalagem.png` como tela livre e compus a partir do canto superior
    esquerdo. É **arquivo de produção**: tem sangria, marcas de corte, abas de solda
    e margem de segurança → antes de recompor arte de produção, **meça os limites no
    próprio pixel**. Medidos aqui (coordenadas do arquivo 656×939):

    | Região | Coordenadas |
    |---|---|
    | painel útil (fora disso = aba `SOLDA`) | `x = 64..579` |
    | margem de segurança do conteúdo | `x = 73..569` |
    | faixa da história (única parte editável) | `y = 234..500` |
    | bloco Serra da Canastra — **preservar, não redesenhar** | `x = 340..557, y = 382..499` |

    E valide no fim contando pixels alterados fora do painel: tem que dar **0**.
15. **A limpeza da marca d'água comeu o texto pequeno** (`F: FABRICADO` virou
    `FA8R CADO`, `ORGULHOSAMENTE` perdeu letras) → a folha é vermelho clareado e o
    texto é creme com anti-aliasing: um pixel de texto a 50% de cobertura tem
    exatamente a cor de um pixel de folha. Os dois caem na mesma reta RED→CREAM, então
    **nenhum limiar de cor por pixel separa os dois** → use limiar conservador (tira a
    folha fraca, preserva todo o texto) e preencha à parte só as regiões que você
    **provou** estarem vazias — conte os pixels de conteúdo com `assert` antes de
    pintar, nunca preencha um retângulo no olho.
16. **Conclui que o Mercado Livre estava inacessível e quase parei a pesquisa** → o 403
    era do User-Agent do `WebFetch`; `curl` com UA de Chrome devolve 200. Mas na página
    de busca esse 200 vinha com `suspicious-traffic-frontend` no `data-assets-prefix`,
    o muro anti-bot — **conteúdo falso com status de sucesso** → teste o host com UA de
    navegador antes de declarar bloqueio, e depois **confira o que veio**, não o código
    HTTP. É a lição 3 outra vez, fora da API de imagem: 200 nunca é prova. Rota que
    funciona para dado de marketplace é a extensão do Chrome na sessão logada; contornar
    detecção de bot está fora de escopo. Ver `docs/ML-CAPSULAS-ESTRATEGIA.md` §1 e §11.
17. **`_pega_download.py` salvou a imagem de ontem sem reclamar** → ele procurava só
    `ChatGPT Image*.png`, e a conta agora está em português, onde o arquivo nasce
    `Imagem do ChatGPT ....png`. Não deu erro: o glob achou downloads antigos do
    padrão inglês e o `max(..., getmtime)` devolveu o mais recente **deles**. Como as
    duas imagens tinham 1086x1448, a linha de conferência do próprio script não
    denunciou nada → o script agora cobre os dois padrões. Lição geral: um seletor que
    não encontra o alvo mas encontra *algo* é pior que um que falha. Depois de baixar,
    confira o **carimbo de hora** do arquivo que o script imprimiu, não só as dimensões.
18. **Notas sensoriais ilegíveis viraram `70 / 80 / 80 / 40` na primeira geração** →
    nas cápsulas Suave, AROMA e DOÇURA são **10**, então a barra vai 100% cheia e o
    número fica preto sobre preto; na foto de WhatsApp (591x1280) não dá para ler. O
    prompt de lateral manda "copie da foto", e o modelo, sem conseguir ler, inventou →
    quando a fonte não permite ler, "copiar da foto" não é instrução, é convite ao
    chute. Confirme o valor com o cliente e **soletre no prompt** (campo
    `lateral_extra` em `scripts/prompts_catalogo.py`). Notas do Suave: CORPO 7,0 ·
    AROMA 10 · DOÇURA 10 · CITRICIDADE 6,0.
19. **Quase apliquei um passe de saturação numa foto real da lavoura** para encostar
    no alvo escrito `satur = 70` → o alvo é a **média de duas populações diferentes**.
    Medido agora com `scripts/home_medir.py:perfil` sobre a própria base verificada:
    lavoura de Medeiros mediana **85,9** (min 66,8 · máx 105,8), packshot de Uberlândia
    mediana **59,1** (min 17,9 · máx 99,6). O 70 não descreve nenhuma das duas. O mesmo
    vale para `estourado%`: a lavoura ao meio-dia estoura o céu (mediana 0,26%, e 3,5%
    no quadro que tem céu aberto) e o packshot não estoura nada (0,001%) → **compare
    cena com cena e packshot com packshot**; antes de "corrigir" uma métrica, meça o
    grupo de referência certo. E nunca calibre uma **foto real** contra esse alvo: ela
    é a fonte da medida, não a candidata a ser corrigida.
20. **Ia reprovar `SEM GLÚTÉN` como erro de geração** → o acento no E parece corrupção
    clássica de difusão, mas ampliei a foto crua e **a embalagem impressa real também
    traz `SEM GLÚTÉN`**. A geração copiou fielmente → antes de acusar a geração de um
    erro de português, confira se o erro não está na **arte real**. A referência é a
    fonte da verdade mesmo quando ela está errada; o alvo é fidelidade, não correção
    ortográfica. Vale o inverso também: não "conserte" o rótulo no prompt.
21. **Os packshots de estúdio das cápsulas passaram na frente e falharam nas laterais**
    → a frente tem tipografia grande e saiu íntegra nos 3 SKUs; as laterais têm corpo
    pequeno e perderam **só os diacríticos**: `ARABICA` por `ARÁBICA` (Clássico 16.3 e
    Suave 21.3) e `DOCURA` por `DOÇURA` (Canela 17.4). Os **números** das notas
    sensoriais estavam todos certos (8,0/9,0/9,0/8,5 · 6,5/10/10/6,0 · 7,0/10/10/6,0)
    → o modelo erra o **acento** antes de errar o dígito. Numa conferência de lateral,
    varra a lista de acentos do `canastra-embalagem` explicitamente, campo a campo;
    números batendo não indicam que o texto está íntegro.
22. **O carimbo de lote saiu `F:23.2025`, um mês que não existe** → é carimbo variável
    impresso fora da arte, e o modelo o redesenha como qualquer outro texto. No Canela
    saiu `F:12.2025`, plausível, e passaria despercebido → trate **lote, fabricação e
    validade como o QR**: regenerados, nunca confiáveis. Em imagem de e-commerce isso é
    informação regulatória falsa, então ou some do enquadramento ou entra por composição
    da foto real. Plausível é pior que absurdo: o absurdo você vê.
23. **Imagem 3:4 destoaria da vitrine da Tray** → o catálogo da loja serve tudo em
    **1:1** (`images.tcdn.com.br/.../90_<slug>.jpg` é a miniatura; sem prefixo é a
    original, medida em 600×600). Subir o 1086×1448 direto deixaria a grade desalinhada
    → compus 1448×1448 estendendo a coluna de borda (`crop(0,0,1,H).resize(pad,H)`), o
    que preserva o gradiente vertical do fundo colorido sem emenda visível. Limites do
    upload: JPG/JPEG/PNG, 5 MB, 2.500px.
24. **Reordenar imagem de produto na Tray não responde a arrastar com o mouse** →
    os `.preview-item-image` são `draggable="true"` (HTML5 nativo), e `left_click_drag`
    não dispara `dragstart`/`drop`. Disparar os eventos via JS com um `DataTransfer`
    compartilhado funciona, **mas o Vue só re-renderiza no próximo evento de teclado** —
    a primeira tentativa pareceu falhar e só se aplicou quando apertei uma seta depois.
    Receita: `__hdrag(origem, destino)` e em seguida uma tecla neutra (`ArrowLeft`);
    confira a ordem relendo os `src`, não pela tela. Não existe botão "tornar principal":
    principal é a posição 0.
25. **Vídeo renderizou deitado / a matemática de recorte deu errado** → li
    `width/height` do container (1024×576) e ignorei o `displaymatrix: rotation of
    -90°`; a dimensão de exibição era 576×1024, 9:16 nativo → **sondagem de vídeo
    sempre honra a matriz de rotação**; a dimensão codificada não é a dimensão de
    exibição.
26. **O render a 360 px saiu 360×638 e ninguém reclamou** → passei `--scale=0.333`
    achando que 1080 × 0,333 fecharia em 360×640. Fecha em 359,64×639,36; o still
    aceita altura ímpar e sai 360×639, mas o h264 exige lado par e o **Remotion desce
    639 para 638 em silêncio**, com exit 0. 360/638 = 0,5643, e 9:16 é 0,5625: a peça
    saiu esticada 0,3% na vertical sem um aviso → **nunca digite a escala; derive-a da
    largura alvo** (`escalaParaLargura()` em `instagram/remotion/src/verificacao/telefone.ts`)
    e recuse lado ímpar antes do render. É a lição 3 de novo, agora em vídeo: exit 0
    não prova que o parâmetro fez o que se queria.
27. **`fps=2,scale=180:-1,tile=6x8` não montou a folha de contato** → o ffmpeg que vem
    dentro do Remotion (`node_modules/@remotion/compositor-*/ffmpeg.exe`) é build
    mínima: publica ~50 filtros e **não tem `fps` nem `tile`**. Pior, a mensagem para
    `fps=2` é `No option name near '2'`, que parece erro de sintaxe e me fez reescrever
    o filtro em vez de duvidar do binário; só `fps=fps=2` devolveu o verdadeiro `No such
    filter: 'fps'` → antes de depurar a sintaxe de um filtro, **confirme que o filtro
    existe naquela build** (`ffmpeg -filters`). Amostragem se faz com `-r`, que é opção
    de saída e não filtro, e o mosaico se monta em Node com `pngjs`.
28. **Terceiro arquivo deste repositório lido pela dimensão codificada, e dessa vez a
    sondagem mentiu com três números ao mesmo tempo** → `sondar()` em
    `instagram/remotion/src/motor/sondar.ts` lia só `side_data_list.rotation`, que é
    **displaymatrix — metadado de contêiner de vídeo**, e nada lia EXIF
    (`grep -in "exif|orientation" src/motor/sondar.ts` = 0 linhas). Rodando sobre
    `base-curada/01-real-verificada/torrefacao-uberlandia-875m/packshot-classico/Classico (5).jpg`
    ele devolvia `{largura:4096, altura:2304, rotacao:0, razao:1.7778, duracao:0.04,
    fps:25}`: razão **1,7778** onde a de exibição é **0,5625**; `rotacao: 0` num arquivo
    cujo EXIF traz `Orientation = 6`; e `fps`/`duracao` **inventados pelo demuxer
    `image2`** para uma foto parada — todo JPEG e todo PNG voltam `r_frame_rate: 25/1` e
    `duration: 0.040000`, medido.

    Os três casos são **um padrão**, não três bugs:

    | caso | arquivo | o que mentia |
    |---|---|---|
    | 1 (lição 25) | `pl.mp4` | gravado 1024×576 com `displaymatrix rotation -90`, exibe 576×1024 |
    | 2 | `projetos/01-private-label/public/assets/{classico,suave,canela}-250g.png` | 4096×2304 **deitados**: o `Orientation 6` da origem nunca foi aplicado na publicação, e os três laudos `instagram/assets/embalagem/*.json` gravam `"dimensoes": [4096, 2304]`. Medido agora: `rotacao.fonte = 'nenhuma'` — o metadado **não está** esperando no arquivo, ele foi perdido |
    | 3 | `sondar()` sobre qualquer foto | lia um metadado de vídeo num arquivo que só tem o de foto |

    → **Regra: em todo ponto onde este motor recebe imagem ou vídeo, a dimensão de
    exibição é derivada de metadado de rotação, e o metadado tem DOIS nomes por
    tecnologia** — `side_data_list.rotation` (displaymatrix, contêiner de vídeo) e EXIF
    `Orientation` (JPEG/TIFF). Ler `width`/`height` sem os dois é o defeito padrão deste
    repositório. O mesmo `ffprobe` que o Remotion já traz expõe os dois, sem dependência
    nova: `ffprobe -show_frames -read_intervals "%+#1"` e `frames[0].tags.Orientation`
    — que **vem preenchido de espaços** (`"    6"`), então comparação de string falha em
    silêncio e `Number(String(x).trim())` é obrigatório. `format_name === 'image2'` é o
    sinal de foto parada, e vale para JPEG e PNG.

    Dois corolários que custaram tanto quanto a leitura errada:

    - **Um `0` de "não achei metadado" e um `0` medido são fatos diferentes, e um deles é
      alarme.** Por isso `rotacao` deixou de ser `number` e virou
      `{fonte: 'displaymatrix' | 'exif' | 'nenhuma', graus}`. Era devolver `0` nos dois
      casos que fazia o defeito passar despercebido.
    - **Ausência é melhor que número inventado** (lição 3 outra vez): `fps`, `fpsMedio` e
      `duracao` agora são `null` em imagem parada, e o tipo diz isso, o que obriga os
      chamadores a tratar. Distribuição medida em `base-curada/01-real-verificada`: dos 12
      packshots de Uberlândia, **12 são `Orientation 6`**; das 26 fotos da fazenda,
      **8 são `Orientation 6` e 18 são `Orientation 1`** — ou seja, metade da base
      verificada exibe num eixo diferente do que está gravado.

    E o campo declarado à mão não substitui a medição: o protótipo
    `instagram/remotion/out/_spec-briefing/b-jornada-foto.json` declara
    `razaoExibicao: 1.3333` para `IMG_1421.JPG` e `IMG_1424.JPG`, e os dois são
    `Orientation 6` — medido agora, exibem 3024×4032, razão **0,750000**. Campo de razão
    existe para ser **conferido contra `sondar()`**, não para ser acreditado.
29. **Apliquei como regra de pipeline uma proibição que era de escopo de pasta** →
    `assets/materialidade/LEIA-ME.md` diz que embalagem "nunca nasce aqui", e eu li isso
    como "embalagem nunca entra em geração". É falso, e contra evidência que já estava no
    disco: os **96 packshots** de `saida-teste/catalogo-estudio/` saíram por geração e
    foram aprovados, a lição 21 registra a frente íntegra nos 3 SKUs e a 12 registra os 3
    indistinguíveis da fonte num blend a 50% → antes de transformar uma linha de LEIA-ME
    em restrição de arquitetura, confira **de que escopo aquele arquivo fala**. Documento
    de pasta descreve a pasta. A proteção do rótulo não é a proibição: é mandar a
    referência certa e conferir letra por letra, com composição de pixel real como rede.
30. **Declarei o gabarito de conferência de memória, dentro do módulo escrito para proibir
    isso** → ao criar a primeira peça de `instagram/estaticos/catalogo.py` escrevi
    `strings_impressas` transcrevendo da lembrança: saiu `"CLÁSSICO"` onde o selo diz
    **`"CLÁSSICO EM GRÃOS"`**, `"TORRADO EM GRÃOS"` onde diz **`"TORRA EXCLUSIVA"`**, e
    faltavam `SPECIALTY`, `ESPECIAL`, `Café` e **`"Desde 1985"`** — justamente a string da
    lição 13. Um subagente ampliou e discordou; só então eu ampliei e confirmei → **a
    regra da lição 18 vale na hora de DECLARAR, não só na de conferir.** Gabarito não
    conferido no pixel não é gabarito, é lembrança com cara de dado. E quando outro agente
    contesta um dado seu, confira você mesmo — aceitar a leitura dele é a mesma falha
    terceirizada.
31. **O texto do cartão sumiu sobre o packshot e a correção óbvia era proibida** → com as
    três linhas sobrepostas à foto, o contraste do creme mediu 4,42:1 · 3,43:1 · **1,09:1**
    — a terceira invisível. A causa é estrutural: o bloco atravessa fundo que vai de preto
    (o pacote) a branco (o ciclorama), e **nenhuma cor fixa sobrevive a essa amplitude**;
    o packshot de fundo colorido é pior ainda, 2,46:1. O remédio padrão — scrim escuro
    atrás do texto — é barrado por `proibicoes.md`, que proíbe gradiente por cima da
    embalagem → quando a correção de legibilidade esbarra numa regra de marca, **mude a
    geometria, não a regra**: o texto ganhou faixa sólida própria no rodapé e o contraste
    virou constante do molde, 11,59:1, com o pacote intocado. Medir antes de escolher a
    cor evita as duas rodadas.
32. **Ia descrever a cápsula Canela como vinho, lendo a ilustração impressa na caixa** →
    a arte da frente desenha uma cápsula **vinho**, e a cápsula de plástico de verdade,
    ampliada 3× em `capsulas-canela-detalhe-07/08.jpg`, é **cobre metálico**. O Clássico
    bate (arte preta, cápsula preta), e foi justamente esse acerto que quase me fez
    generalizar → **arte impressa não é fonte de cor do produto que ela ilustra.** A
    ilustração é um desenho feito por um designer, não uma medição. Para qualquer
    atributo físico de um item que aparece desenhado na embalagem, a fonte é a foto do
    item, e quando ela não existe o campo é `não verificável` — a cápsula Suave não tem
    foto nenhuma, e a cor (preta, igual à do Clássico) veio do Arthur em 04/10/2026, não
    da arte marrom que a caixa desenha. Gravado em `capsula_corpo`/`capsula_fonte` no
    `scripts/prompts_catalogo.py`.
33. **A foto crua da cápsula não servia de guidance e eu quase anexei assim mesmo** →
    `*-detalhe-*.jpg` tem 3072×4096 e a cápsula ocupa ~3% da área; o resto é mesa de
    madeira e parede. Anexada inteira, o modelo lê melhor a mesa do que o produto →
    quando o assunto é pequeno dentro da foto crua, **recorte antes de anexar**. O
    `scripts/capsula_referencia.py` monta uma folha com as duas vistas reais lado a lado
    (em pé e deitada, para o corpo e para a tampa) — dois `crop` colados sobre branco,
    nada gerado. E o prompt passou a **negar explicitamente o layout da referência**
    ("its two-up split layout and its white border must not appear"), senão o modelo
    copia a folha de contato em vez do produto.
34. **Um clique em (1340, 25) no ChatGPT apagou um prompt de 3.840 caracteres já
    inserido** → eu quis fechar o overlay de edição que abre depois do upload e mirei no
    X do canto superior direito; ali, com o overlay fechado, fica o botão de **chat
    temporário**, e ligar o modo temporário recarrega a página (`?temporary-chat=true`) e
    leva anexos e composer junto → feche o overlay de imagem do ChatGPT com **`Escape`**,
    nunca com clique no canto. Vale a regra geral: num app que troca o que está sob o
    cursor, tecla é mais segura que coordenada.
35. **Terceiro padrão de nome no download do ChatGPT, e dessa vez não dá para listar os
    padrões** → `_pega_download.py` procurava `ChatGPT Image*.png` e `Imagem do ChatGPT*.png`
    (lição 17); agora o arquivo nasceu `Cápsulas Café Canastra em Estúdio.png` — **o título
    que o próprio modelo deu ao chat**, ou seja, uma string arbitrária e diferente a cada
    conversa. O glob não achou nada, pegou um PNG de 28/09 e só o guarda de idade impediu
    o estrago → a lição 17 estava certa no diagnóstico e **errada no remédio**: acrescentar
    um padrão a cada quebra é correr atrás. Nome de arquivo é um seletor que o fornecedor
    troca sem avisar; o que separa o download desta rodada dos outros é o **carimbo de
    hora**. O script agora pega qualquer `*.png`, o mais recente, e a trava é só temporal.
36. **A 17.7 foi gravada com a imagem da 21.6, mesmo carimbo, sem um erro sequer** → ao
    baixar várias imagens em sequência, um clique em Baixar que não dispara deixa o
    download ANTERIOR como o mais recente, e ele ainda está dentro da janela de 180 s do
    `exigir_recente` → **uma janela de tempo não distingue "não baixou" de "baixou agora"
    quando os eventos são seguidos.** Cada arquivo de origem passou a ser consumido uma
    única vez (`.cie/downloads-consumidos.json`), e foi essa trava — não a de idade — que
    pegou as duas falhas seguintes. Corolário de processo: por isso os agentes paralelos
    **geram e não baixam**; o download é serial, de um processo só.
37. **Quatro agentes em abas separadas, e o rascunho do composer é um só** → o ChatGPT
    compartilha o rascunho e os anexos do composer **entre abas da mesma conta**. Três dos
    quatro agentes abriram a aba nova já com o prompt e os anexos de outro agente dentro.
    Nenhum enviou errado porque conferiram, mas um `file_upload` + clique em Enviar sem
    conferência teria gerado a imagem do colega, com status de sucesso → ao paralelizar o
    ChatGPT, **leia o `.ProseMirror` e a lista de anexos imediatamente antes de cada envio**
    e limpe com `selectAll`+`delete`. Aba separada não é sessão separada.
38. **Ia reprovar o bloco `GOURMET / ESPECIAL / SCAA 80+` do Clássico por sair em cantos** →
    o `scripts/prompts_catalogo.py` descrevia "a thin rectangle outline" no Clássico e no
    Canela, e só o Suave trazia os quatro cantos. Ampliando `capsulas-classico-detalhe-08`
    e `capsulas-canela-detalhe-09`, **os três SKUs usam cantos**: a geração estava certa e
    a descrição é que estava errada, escrita por analogia entre SKUs irmãos — a lição 30
    outra vez, agora dentro do próprio script que existe para evitá-la → quando a geração
    diverge do gabarito, **o gabarito também é suspeito**; confira os dois contra o pixel
    antes de decidir quem errou. Dois agentes também reportaram erros que a ampliação
    desmentiu (`INDÚSTRIA BRASILEIRA` sem acento, cápsulas encostando na caixa, cápsula de
    cabeça para baixo): relato de agente é pista, nunca veredito.
39. **Quadrei 9 imagens em 1:1 para o Mercado Livre e o ML desfez tudo** → compus
    1448×1448 esticando a coluna da borda (a receita da lição 23, feita para a Tray), subi,
    e o que ficou guardado foi **1031×1200**: o ML faz **trim da margem branca** e reduz a
    altura para 1200. Ele então gera sozinho as variantes quadradas que usa na grade
    (`-S` 90, `-Q` 284, `-V` 320, `-W` 568), com padding próprio → **receita de vitrine não
    é portátil entre marketplaces.** A Tray serve o arquivo como ele sobe; o ML reprocessa.
    Antes de pré-formatar imagem para uma plataforma, **suba uma e meça o que ela guardou**
    (`-F` é a versão cheia). Para o ML basta mandar o 3:4 original com fundo branco.
40. **O Confirmar das Fotos do ML não respondeu a dois cliques seguidos na mesma
    coordenada** → eu media `getBoundingClientRect()` do botão, clicava, e `elementFromPoint`
    confirmava que o alvo era o Confirmar — mas a seção não fechava e a lista seguia com a
    capa de 2022. O que destravou foi **rolar a seção para o topo, tirar screenshot e clicar
    na coordenada lida no screenshot**: o `scrollIntoView` que eu fizera antes deixava o
    botão numa posição que o rect reportava certo e o clique real não alcançava → quando um
    clique por coordenada falha duas vezes num alvo que o `elementFromPoint` confirma,
    **pare de confiar no rect e leia o alvo no pixel**. É a mesma disciplina da conferência
    de imagem: o DOM descreve, o screenshot mostra.
41. **`element.click()` por JS ABRE o acordeão do ML** → a skill `canastra-mercadolivre`
    dizia que só clique real funcionava, e por isso eu gastava um `wait` de 10 s mais um
    screenshot por seção. Medido em 04/10/2026: `button.accordion-container__toggle.click()`
    abre na hora, e `button[aria-label^="Excluir foto"].click()` remove a foto. O que
    continua exigindo clique real é o **Confirmar** → a fronteira não é "JS não funciona",
    é **JS funciona em controle local de estado (acordeão, excluir, checkbox) e falha no
    que submete**. Dois corolários medidos: os `aria-label` **mudam a cada re-render**
    (`D_NQ_NP_…-F.jpg` vira `D_Q_NP_…-G.jpg`), então guardar uma lista de botões e clicar
    em todos opera em refs mortos; e um laço síncrono pega **o mesmo botão N vezes**, porque
    o React só re-renderiza no fim do tick. Uma chamada por exclusão, relendo o DOM.
42. **O `file_upload` com 3 arquivos entregou na ordem inversa** → subi `.6, .8, .7` e o
    anúncio ficou `.7, .8, .6`, ou seja, a capa virou o detalhe em vez da embalagem. Em
    miniatura de 120 px a inversão não salta aos olhos → **suba uma imagem por chamada** e
    confira a ordem antes de confirmar. Para conferir: a ordem do DOM é
    `button.media-uploader__element-primary-action img`, e dá para baixar cada preview do
    CDN com `curl` e UA de Chrome em vez de depender da miniatura na tela.
43. **Duas das três fotos dos anúncios de cápsula mostravam a caixa dispenser de atacado** →
    o anúncio vende *1 caixa de 10 un* a R$ 34,90 e a foto mostrava uma caixa grande com
    dezenas de cápsulas a granel; a terceira era mock-up 2D chapado. Todas entre 375 e
    500 px, abaixo dos 1200 que o ML pede para habilitar zoom. Ninguém tinha olhado as fotos
    porque o trabalho da conta vinha sendo preço, título, frete e ficha → **numa auditoria
    de anúncio, a foto é campo como qualquer outro.** Com 37,68% de envio incorreto nesta
    conta, expectativa visual errada é combustível de devolução, não detalhe estético.
    Trocadas pelas 3 de catálogo em 04/10/2026, com autorização do Rafael.
44. **Ia subir para um anúncio público uma lateral com `F: 23.2025`, um mês que não
    existe** → a lição 22 já previa isso ("trate lote, fabricação e validade como o QR:
    regenerados, nunca confiáveis") e mesmo assim a `16.4` estava na fila de upload, porque
    o pedido era "as laterais" e eu tratei as seis como um bloco. Conferidas uma a uma,
    **as seis laterais de cápsula são três coisas diferentes**: `16.3`/`21.3` têm o painel
    de dados com `ARABICA` sem acento; `16.4`/`17.3` têm o carimbo regenerado — um absurdo
    (mês 23) e um **plausível** (`F: 12.2025`), que é o pior dos dois; `17.4` tem o painel
    de dados correto e `21.4` saiu **sem carimbo nenhum**, limpa → **"as laterais" não é
    uma unidade.** Antes de publicar um conjunto, abra cada peça: aqui o mesmo número de
    arquivo (`.3`, `.4`) mostra faces diferentes conforme o SKU, porque a geração não
    seguiu a nomenclatura. Subi as cinco sem dado regulatório falso e deixei `16.4` e
    `17.3` fora, dizendo o porquê — escopo reduzido é decisão do cliente, mas publicar data
    impossível não é uma opção que eu possa escolher por ele.
45. **Pedi "mude SOMENTE o selo" e o ChatGPT refez 79,2% do quadro** → em 05/10/2026, no
    post da cozinha, a v1 voltou com a cena aprovada e só o selo circular errado. Mandei um
    follow-up de edição no mesmo chat nomeando a operação e repetindo o que preservar
    ("same kitchen, same counter, same light, same package position"). A v2 veio com outra
    cozinha inteira — pia, escorredor, outra caneca, pano de crochê que eu não pedi.
    **Medido com `np.abs(v1-v2).max(axis=2) > 12`: 79,2% dos pixels mudaram, para um pedido
    que cobria ~1,1% do quadro** → isto fecha a contradição que `docs/PESQUISA-REALISMO-GERACAO.md`
    §3 tinha deixado aberta. A documentação da OpenAI prescreve *"small, single-change
    follow-ups"* e o fórum avisava que reusar a conversa degrada; **na nossa medição o
    fórum está certo**: follow-up de edição no mesmo chat não preserva, regenera. Corolário
    operacional: **cena aprovada não se arrisca em follow-up.** Salve a v1, e corrija o
    defeito por composição local ou numa conversa nova — nunca pedindo "só isso" por cima
    de um resultado que você já quer manter.
46. **Soletrar não converge em texto curvo, e o campo em arco foi o único a quebrar nas
    duas rodadas** → na v1 o selo saiu `CLA&SICO EH GRÃO6` / `TORRA EXCLUSIYA`; apliquei o
    degrau 1 (soletrar letra a letra, inclusive "o caractere antes do A final é um V, não
    um Y") e a v2 devolveu `CLAS6ICO EM GRÃO6` / `TORRA EXCLUBIVA` — o `V` corrigiu e o `S`
    quebrou. **Erro diferente, mesma falha.** No mesmo quadro e nas duas rodadas,
    `SPECIALTY` — tipografia pequena, mas em **linha reta** — saiu íntegra. *(Leitura minha,
    não medição: o preditor de sobrevivência pode ser a curvatura da linha de base, não só
    a altura da letra. Tentei medir altura de glifo e **joguei a medição fora**: as caixas
    que amostrei incluíam o anel do selo, então o número não media o que eu dizia que media
    — ver a regra de validar a região amostrada.)* → para texto em arco, **pule os degraus
    1 a 5 e vá direto ao 6**. A composição custou um `crop`, um casamento de nível de preto
    (deslocamento medido −2,7/−2,8/−1,7) e uma máscara circular suave, com `assert` de
    **0 pixels alterados fora da caixa** — e resolveu em uma passada o que duas gerações
    não resolveram.
47. **O portão de transbordo reprovou os 7 slides do deck por um defeito que não
    existia** → medi `scrollHeight > clientHeight + 1` em todo elemento com texto e
    reportei como transbordo. Saiu "TRANSBORDA" para `manchete`, `nome`, `afirmacao`,
    `numero`, `rotulo` — ou seja, **todo título**, o que é uniforme demais para ser
    defeito real. Sondando os números em vez do booleano: `h1` de 92px com
    `line-height: 1.03` dá `sh=198 ch=190 delta=8` com **`overflow: visible`** — a
    caixa de linha é menor que a caixa natural do glifo, e **nada é cortado**. →
    `scrollHeight > clientHeight` **só é defeito quando o elemento pode cortar**;
    com `overflow: visible` ele mede a folga do glifo, não perda de conteúdo. A
    condição passou a exigir `getComputedStyle(el).overflow !== 'visible'`, e a faixa
    de texto ganhou altura fixa com `overflow:hidden` **para que o portão tenha o que
    medir**. É a regra de validar a região amostrada aplicada a uma métrica de DOM:
    antes de acreditar num alarme que acende em tudo, imprima o número cru.

    Corolário que vale para todo portão deste repositório: **portão é necessário, não
    suficiente.** Os três passaram no deck e o olho ainda pegou dois defeitos de
    composição que nenhum deles vê — a faixa cobrindo a base da embalagem e o
    `1.250 m` quebrando em duas linhas. Por isso `render.miniaturas` existe e por isso
    a mensagem de sucesso da CLI termina em *"olhe o `_feed` antes de publicar"*.
