# estudio-reels — skill universal de Reels em motion de colagem

Data: 07/10/2026 · Origem: o processo da peça 07 do Café Canastra, aprovado pelo cliente
como "impecável", e a skill `canastra-video` (`colagem.md`).

## 1. Objetivo

Uma skill pessoal que, aberta em **qualquer repositório**, produz Reels em motion de
colagem narrado no padrão da peça 07 para a empresa daquele repositório — descobrindo a
empresa e o nicho sozinha, estudando a concorrência, gerando narração e assets pelo
navegador do usuário e montando no Remotion. Ela **se planta** em cada repositório e
**melhora a cada peça** com as próprias lições, como a skill do Canastra melhorou nesta
sessão.

## 2. Decisões tomadas

| Tema | Decisão |
|---|---|
| Onde mora | Skill pessoal em `~/.claude/skills/estudio-reels/` (a "semente"). Não é plugin |
| Escopo da v1 | Só Reels de motion. Estático e carrossel ficam para a v2, reaproveitando as fases de contexto |
| Ferramentas externas | Tudo pelo Chrome do usuário (Claude in Chrome), com as sessões dele logadas. **Nenhuma API, nenhuma chave, nenhum cadastro** |
| Contexto | Pesquisa primeiro (repo + site + Instagram + Google), depois pergunta só o que faltou |
| Concorrência | Nicho (a skill sugere 3–6, o usuário confirma) + referências de formato de motion (1–3) |
| Geração | Autônoma (ElevenLabs e ChatGPT geram, refazem e baixam sem perguntar), com as travas da §7 e **um único ponto de parada: o roteiro** |
| Fotos reais | Banco da empresa; quando faltar, Unsplash/Pexels (licença de uso comercial livre) |
| Imagem de terceiro | Pinterest, Google e afins são referência: podem subir ao ChatGPT como referência de estilo, com as travas da §7.3; nunca viram pixel do vídeo |
| Evolução | Cada repositório evolui a própria cópia; lição universal volta para a semente com OK do usuário |
| Arquitetura | Uma skill com tudo (maestro + arquivo por fase + mecânica do navegador + motor modelo) |

## 3. Arquitetura

### 3.1 A semente (instalada uma vez por máquina)

```
~/.claude/skills/estudio-reels/
  SKILL.md                maestro: ciclo, fases, regras que não se negociam, como plantar
  VERSAO                  ex.: 1.0.0
  fases/
    00-plantio.md         criar a cópia no repo, o motion/ e instalar dependências
    01-contexto.md        pesquisa da empresa + perguntas de nicho + banco de imagens
    02-concorrencia.md    nicho + formato no Instagram
    03-roteiro.md         pauta, estrutura da peça 07, fatos com fonte; PARADA para OK
    04-narracao.md        ElevenLabs v4 pelo Chrome, 3 tomadas, escolha
    05-tempo.md           whisper + alinhamento forçado + conferência contra o áudio
    06-assets.md          biblioteca, banco da empresa, Unsplash/Pexels, ChatGPT, recorte
    07-montagem.md        roteiro em código, cenas, câmera, chicotes, som, identidade
    08-conferencia.md     portões, stills, render de teste, varredura, áudio, MP4 final
    09-publicacao.md      descrição do post + checklist; publicar só com OK na hora
    10-retrospectiva.md   lições → regras/motor → lista de promoção → semente
  navegador/
    chrome.md             regras comuns (abas, login, downloads, conferir antes de enviar)
    instagram.md · chatgpt.md · elevenlabs.md · referencias.md (Pinterest/Google) · bancos-livres.md
  licoes.md               lições universais (sites, ferramentas, motor, método)
  modelo/
    remotion/             motor de colagem (src/colagem, peça-esqueleto, scripts, testes)
    ferramentas/          Python: alinhar_narracao, alinhar_forcado, conferir_alinhamento,
                          biblioteca, recorte de assets, sfx, varrer_movimento, folha_do_video
  .git/                   histórico local das versões (sem remoto)
```

O maestro (`SKILL.md`) fica curto. Cada fase é lida só quando chega, para não gastar
contexto com o que a peça ainda não precisa.

### 3.2 O que o plantio cria no repositório

```
.claude/skills/estudio-reels-<marca>/   cópia evolutiva da semente (mesma estrutura)
  SEMENTE                               versão da semente de onde nasceu
  licoes-empresa.md                     lições que só valem para esta marca
motion/
  remotion/                             projeto Remotion com o motor (node_modules ignorado)
  ferramentas/                          scripts Python
  marca/dossie.md · marca/identidade.json · marca/logo-*.png
  concorrencia/estudo-<data>.md
  referencias/                          descritores de estilo e links (texto)
  biblioteca/indice.json                (PNG ignorados pelo git)
  pecas/NN-<tema>/                      roteiro.txt, narracao.mp3, palavras.json, saida/, legenda-post.md
```

E uma linha no `CLAUDE.md` do repositório (criando o arquivo se não existir) apontando
para a skill da marca, para a próxima sessão saber que ela existe.

Quando a cópia do repositório existe, a semente só aponta para ela: a cópia é quem
comanda dali em diante.

### 3.3 Ciclo de vida

1. **Instalar** a semente (copiar a pasta para `~/.claude/skills/`).
2. **Plantar** na primeira vez num repositório (fase 00).
3. **Produzir** peças (fases 01–09; 01 e 02 são refeitas só quando ficarem velhas ou o
   usuário pedir).
4. **Retrospectiva** ao fim de cada peça (fase 10): falha vira lição; lição que muda
   procedimento vira regra na fase ou correção no motor; commit no repositório.
5. **Promover**: a retrospectiva separa lição da empresa (fica no repo) de lição universal
   (site, ferramenta, motor, método) e apresenta a lista; o que o usuário aprovar sobe para
   a semente, que ganha versão nova (commit no git local dela).
6. **Atualizar**: quando a semente está mais nova que a `SEMENTE` de um repositório, a
   cópia oferece puxar as mudanças universais, sem tocar em `licoes-empresa.md`, no
   dossiê nem no que o repositório mudou por conta própria.

## 4. As fases

| Fase | Entrada | O que faz | Saída |
|---|---|---|---|
| 00 Plantio | repo qualquer | confere Node, Python e espaço em disco; copia a semente; cria `motion/`; `npm install`; dependências Python; whisper.cpp; `.gitignore` | cópia da skill + motor |
| 01 Contexto | repo + Chrome | lê README/docs; site, Instagram (seguidores, cadência, posts de topo) e Google da empresa; marca cada fato pela origem (**[oficial]**, **[medido]**, **[terciário]**); extrai cores, fontes e logo; pergunta o que faltou (público, o que não pode afirmar, tom, objetivo, produtos foco); pede o banco de imagens e o separa em camadas (própria verificada · própria sem prova · terceiro = referência · sintética = quarentena) | `marca/` |
| 02 Concorrência | dossiê + Chrome | sugere 3–6 concorrentes e 1–3 referências de formato; usuário confirma; por perfil: aba Reels, ordena por views, estuda os de topo (gancho dos 3 s, duração, cortes por segundo, sistemas de texto, CTA) — skill `watch` se existir, senão quadros pelo Chrome | `concorrencia/estudo-<data>.md` |
| 03 Roteiro | dossiê + estudo | pauta que **não acusa produto da empresa**; estrutura da peça 07 (gancho de tensão, "Calma!" + promessa, mito, dado surpreendente a cada 8–10 s, virada com frase repetível, marca, fecho + salvar); tabela fato → fonte (só [oficial]/[medido] viram fala); **PARADA: mostra e espera OK** | `roteiro.txt` + texto com tags |
| 04 Narração | roteiro aprovado | Chrome → ElevenLabs → modelo v4 conferido no rótulo da tela → voz da marca (escolhida com o usuário na 1ª peça e gravada no dossiê) → texto inteiro, 3 tomadas → baixa as 3; escolhe a tomada transcrevendo e comparando com o roteiro (+ duração); aceleração, se pedida, local (ffmpeg) | `narracao.mp3` |
| 05 Tempo | narração final | whisper.cpp → texto do roteiro + tempo → fusão com CTC → `conferir_alinhamento pausas` e leitura dos suspeitos | `palavras.json` |
| 06 Assets | roteiro + biblioteca | busca na biblioteca; banco da empresa; Unsplash/Pexels para lugar real; ChatGPT para objetos e texturas (folha sobre branco), com referência de terceiro permitida pela §7.3; recorte local (união dos bboxes no boil, casco convexo, lente); registrar com o prompt; publicar no projeto | biblioteca + `public/` da peça |
| 07 Montagem | tudo acima | copia o esqueleto; `roteiro.ts` (b/mudo/t); nenhum segundo digitado; cenas em planos com câmera; chicote colado ou cobertura em toda troca; marcador no tempo da fala; área segura; embalagem só como recorte real, com o alfa medido; som por entrada e trilha em seções pelas frases; cores/fontes/logo do dossiê | composição Remotion |
| 08 Conferência | composição | tsc + testes; stills dirigidos (palavra-colagem e 2 antes, fim de cada marcador, meio e fim de cada movimento, dentro de cada chicote); render de teste em 2º plano + `varrer_movimento`; render final; normalizar (−14 LUFS, pico ≤ −1 dBTP medido no MP4); `folha_do_video`; mostra cedo ao usuário | `reel.mp4` |
| 09 Publicação | reel final | descrição pelo molde (1ª linha ≤ ~55 caracteres com a busca; colinha; pergunta aberta, nunca "comenta X"; até 5 hashtags; fontes); checklist (rótulo de IA, localização, capa no corte 3:4); publica pelo Chrome **só com OK explícito na hora** | `legenda-post.md` |
| 10 Retrospectiva | a peça inteira | lições (sintoma → causa → regra); regra na fase ou correção no motor; commit; lista de promoção para a semente | cópia melhorada + semente nova |

## 5. Camada do navegador

### 5.1 Regras comuns (`navegador/chrome.md`)

- Carregar as ferramentas do Claude in Chrome numa só busca; trabalhar em abas novas; não
  mexer nas abas que o usuário deixou abertas.
- As sessões são do usuário: se um site pedir login, parar e pedir que ele entre. Nunca
  digitar senha, código ou dado de pagamento.
- Download com nome dado pela skill (blob + `<a download>` quando der) e conferido pelo
  nome — nunca "o arquivo mais novo" (outra sessão pode gravar na mesma pasta). Um
  download automático por aba; para o segundo, abrir a página numa aba nova.
- Antes de enviar qualquer texto ou anexo, ler o que está no campo (o rascunho do
  ChatGPT é compartilhado entre abas). Em aba de fundo, enviar por `requestSubmit()`
  depois de ~1 s do texto inserido.
- Site que muda o layout: screenshot, adaptar, registrar a mecânica nova como lição
  (universal → candidata à semente).

### 5.2 Por site

| Arquivo | Conteúdo |
|---|---|
| `instagram.md` | perfil → Reels → views; abrir reel; ler legenda; quadros para estudo; volume baixo de navegação (a conta é a do usuário) |
| `chatgpt.md` | folha de objetos sobre #FFFFFF; anexar referência; baixar PNG pelo blob; lições 34–37, 45, 50–52 do Canastra generalizadas |
| `elevenlabs.md` | Text to Speech; seleção de modelo e voz; texto com tags; gerar; baixar cada tomada; ler o saldo de créditos |
| `referencias.md` | Pinterest/Google: buscar, guardar link + descritor; o que pode e o que não pode subir ao ChatGPT (§7.3) |
| `bancos-livres.md` | Unsplash/Pexels: buscar, baixar em resolução cheia, guardar a URL de origem |

## 6. Requisitos da máquina

- Chrome com a extensão Claude in Chrome e as contas logadas: Instagram, ChatGPT (com
  geração de imagem), ElevenLabs (com crédito); Pinterest opcional.
- Node e Python instalados. O resto o plantio instala: dependências do Remotion,
  whisper.cpp (modelo `small`, ~490 MB) e torch/torchaudio com o modelo de alinhamento
  (~1,2 GB, baixado na primeira narração).
- ~3 GB livres em disco.
- O motor e os scripts tratam Windows, macOS e Linux (caminho do ffmpeg do Remotion, do
  whisper e da pasta de downloads detectados, não fixos).

## 7. Travas

### 7.1 Conta e segurança (a autonomia não desliga)

- Nunca publica, envia mensagem, compra crédito ou plano, aceita termos ou muda
  configuração de conta sem OK do usuário naquele momento.
- Sem crédito, deslogado ou captcha: para e avisa. Não resolve captcha.
- Cookie e consentimento: a opção mais restritiva.

### 7.2 Conteúdo

- Fato só com fonte [oficial] ou [medido]; sobre produto, só o que se lê no pixel.
- A pauta não pode acusar produto da empresa; dado de produto em conflito entre fontes é
  `não verificável` e vira pergunta.
- Embalagem e logo entram como pixel real (recorte), nunca redesenhados por modelo.
- Rosto de pessoa real nunca é sintetizado.
- Na publicação, rótulo de IA ligado (narração sintética).

### 7.3 Imagem de terceiro como referência

- Pode subir ao ChatGPT como referência de estilo, luz e paleta.
- Não sobe: rosto identificável, logo ou embalagem de outra marca, marca d'água — essas
  viram só descritor em texto.
- O prompt declara a imagem como referência e proíbe copiar composição, objeto, texto e
  logo.
- Conferência anti-cópia: o gerado lado a lado com a referência; se reproduzir a
  composição, descarta e refaz.
- Referência de terceiro nunca é pixel do vídeo.
- A conta do ChatGPT exige direito sobre o que se envia; o risco é da marca. **Regra do
  repositório vence**: onde o repo proíbe guidance de terceiro (o Canastra proíbe), a
  cópia plantada obedece.

## 8. Construção da v1 a partir deste repositório

| Peça da semente | Fonte no Canastra | Generalização |
|---|---|---|
| `modelo/remotion` | `instagram/remotion/src/colagem/`, `src/pecas/especial/`, `scripts/contato.mjs`, `scripts/normalizar-audio.mjs`, `src/motor/audio/normalizar.ts`, testes de roteiro/legenda | tirar conteúdo e identidade do Canastra; tokens de cor/fonte/logo lidos de `marca/identidade.json`; esqueleto com 2–3 cenas de exemplo |
| `modelo/ferramentas` | `scripts/alinhar_narracao.py`, `alinhar_forcado.py`, `conferir_alinhamento.py`, `biblioteca_colagem.py`, `colagem_assets*.py`, `colagem_sfx_v2.py`, `varrer_movimento.py`, `folha_do_video.py` | caminhos relativos a `motion/`; detecção de SO; sem nome de projeto fixo |
| `fases/` | `.claude/skills/canastra-video/colagem.md`, `SKILL.md`, `legenda-post.md`, `instagram/estrategia/` | sem fatos do café; exemplos marcados como exemplo |
| `navegador/` | lições 16, 34–37, 39–42, 45, 50–52 e a mecânica desta sessão | sem nomes de conta |
| `licoes.md` | lições 1–62 do `CLAUDE.md` | só as universais |

## 9. Teste e critérios de aceite

1. **Linha de base**: agentes com cenários "repositório novo da empresa X" sem a semente;
   registrar onde falham.
2. **Com a semente**: os mesmos cenários; aceitar quando seguem o processo e citam as
   fases e ferramentas certas.
3. **Piloto real**: plantar num repositório de outra empresa e rodar 00–10 numa peça de
   ~30 s. Aceite:
   - plantio num repositório sem nada de motion;
   - dossiê com fatos marcados e perguntas só do que faltou;
   - estudo de concorrência com perfis confirmados;
   - roteiro aprovado no ponto de parada;
   - narração gerada e baixada pelo Chrome, tomada escolhida;
   - `palavras.json` conferido contra o áudio;
   - assets gerados no ChatGPT e recortados;
   - render, conferência e áudio dentro do alvo;
   - descrição pronta;
   - retrospectiva com lista de promoção e semente v1.1.

## 10. Fora da v1

Estático e carrossel; publicação sem OK; qualquer API ou chave; distribuição como plugin.

## 11. Riscos e questões abertas

- **Layout de site muda** (ElevenLabs, Instagram, ChatGPT): mitigado pelo registro de
  mecânica como lição e promoção para a semente.
- **Nome do modelo na ElevenLabs**: a tela pode chamar a v4 de outro nome; a fase 04
  confere o rótulo antes de gerar.
- **Volume de navegação no Instagram** com a conta pessoal: estudar poucos reels por
  perfil.
- **Instalação pesada** (torch + modelos): o plantio avisa o tamanho antes de baixar.
- **Repositório do piloto**: a definir com o usuário antes da implementação.
