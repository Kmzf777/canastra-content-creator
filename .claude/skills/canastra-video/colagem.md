# Motion de colagem narrado — o padrão aprovado

> **Leia `estrategia.md` antes.** Este formato é **exceção**: só com pedido explícito do
> cliente. Os 130 virais analisados não usam colagem narrada de ponta a ponta, o Reel 08 nesse
> formato foi reprovado (lição 66), e voz padrão da marca é humana ou nenhuma. O processo abaixo
> continua valendo como técnica (alinhamento, chicote, assets) quando o formato for pedido, ou
> para a colagem usada como 1–2 cartões dentro de uma peça real.

Peça 07 (`src/pecas/especial/`, composição `EspecialColagem`, 79 s) foi aprovada pelo
cliente como **impecável** em 07/10/2026. Este arquivo é o processo dela, na ordem em que
se faz, com o que deu errado no caminho. Peça nova da série copia este processo — e a
pasta `src/pecas/especial/` como esqueleto —, não improvisa.

Colagem NÃO passa pelo briefing/`plano.json` do motor principal, então **`conferir.mjs`
não serve** (ele exige `plano.json`). Os portões desta série são os testes, as folhas e
os scripts da §8.

Medidas das referências (@_victorzk, quadro a quadro): `docs/motion-colagem.md`.

---

## 1. Referência visual

- Reels de referência pela skill `watch` (yt-dlp + quadros + transcrição). As análises
  ficam em `raspagem/_motion-referencias/<perfil>/*.analise.md`.
- **Meça no quadro, não no resumo do Gemini**: tempo entre entradas, altura da pílula,
  quantos elementos por segundo. O resumo erra número.
- Reel de terceiro é **só descritor textual**, nunca pixel nem fonte de guidance
  (mesma regra de `03-mood-terceiros`).

## 2. Copy

> **Antes de qualquer copy, consulte a biblioteca de referências virais**
> (`instagram/referencias-virais/`): leia o `relatorio.md` e busque 3 referências do mesmo
> formato ou etapa com `python scripts/indice_referencias.py buscar <termos>`, citando-as no
> planejamento. Lição 66: o Reel 08 foi reprovado por piada de fora do café (frango de
> padaria) e por chama sobre o torrador (leu-se "café queimado"). Nos 72 virais analisados,
> nenhum usa voz sintética, colagem do começo ao fim ou fogo desenhado sobre o produto: a
> colagem desta série é exceção a justificar, não padrão.

Estrutura da 07, que segurou 79 s (Kishōtenketsu com gancho de tensão):

| Bloco | Faz |
|---|---|
| 0–5 s gancho | fato **verificado** que choca e quebra expectativa ("Até 1% do café que você compra pode ser casca e pau. E tá tudo dentro da lei.") |
| 5–11 s virada amigável | "Calma!" + **promessa A** em aberto ("até o fim desse vídeo você vai saber se o seu é especial") |
| desenvolvimento | um mito derrubado, depois o conteúdo em blocos com **um dado surpreendente a cada 8–10 s** e um pico de densidade visual |
| virada (ten) | "o que quase ninguém conta" — **promessa B** e uma frase feita para ser repetida ("A torra pode estragar um café bom, mas não salva um café ruim.") |
| marca | a prova da Canastra (planta, colhe, seleciona; 1.250 m; desde 1985) |
| fecho | paga a promessa A, mostra o produto real e pede o salvar no momento em que a dica ficou útil |

Antes de escrever: `instagram/estrategia/02-ganchos.md` (os testes do gancho: imagem
parada a 0,5 s, promessa e não assunto) e `03-roteiro.md` (o relógio). Regras:
- **Todo fato tem fonte escrita antes de virar fala**: tabela fato → fonte (IN MAPA
  16/2010, protocolos SCA, COB/Embrapa), marcada pela régua de origem de
  `instagram/estrategia/LEIA-ME.md` — só **[oficial]** e **[medido]** viram fala;
  **[terciário]** fica fora. Ressalva que muda a frase entra na frase (a SCA adotou o CVA
  em 2024 — por isso a 07 não diz "a regra oficial hoje é 80").
- **A tese não pode acusar um SKU da Canastra.** Antes de fechar o tema, confira torra,
  origem e processo de cada produto contra a tese ("torra escura esconde defeito" bate de
  frente com o Clássico). Dado de SKU em conflito entre fontes é `não verificável`:
  pergunte ao cliente antes de escrever.
- **Sobre os produtos, só o que se lê no pixel**: Clássico e Suave trazem "SPECIALTY /
  ESPECIAL / SCA 80+"; o Canela não. Lição 30.
- Tom: "Hospitalidade Especializada" (`Direcao-Criativa.md`) — técnico explicado sem
  hermetismo; o cliente no centro, não a autoglorificação.
- Método pago (HardCopy etc.) não se baixa de site pirata; use a estrutura pública.

## 3. Narração (ElevenLabs v4)

- **Voz:** padrão é humana (alguém da casa) ou nenhuma — `estrategia.md` §3. ElevenLabs só com
  pedido do cliente; aí, rótulo de IA e a legenda dizendo que a narração é gerada.
- **Mesma voz da série (Elvis)**, texto inteiro numa geração (gerar em partes muda a
  entonação entre os cortes), 3 tomadas para escolher; confira de ouvido contra o roteiro.
- **Uma tag por trecho**, em inglês e entre colchetes: a emoção vale até a próxima tag.
  Reticências desaceleram; `[pause]` respira; troca de registro é de propósito.

```text
[low, tense, slow, almost a whisper, suspenseful]
Até um por cento do café que você compra… pode ser casca… e pau.
[pause]
[cold, deliberate] E tá tudo dentro da lei.
[warm, friendly, smiling, relaxed, like talking to a friend]
Calma! Não precisa largar o café.
```

- Número **por extenso** no texto ("trezentos e cinquenta gramas"): é como a voz lê. O
  whisper escreve em algarismo e `alinhar_narracao.py` converte por extenso (`por_extenso`)
  para casar; se a voz ler diferente (ex.: "zero" vs "nenhum"), a exceção vai em `NUMEROS`.
- `projetos/<p>/roteiro.txt` = exatamente o que a voz leu, **sem as tags**.
- O cliente pode acelerar o áudio depois (a 07 foi a 1,25×). **Todo tempo se mede no
  arquivo final**; nunca reaproveite tempos de uma versão anterior.

## 4. Tempo das palavras

```bash
# 0) whisper.cpp (de instagram/remotion; preparado por scripts/preparar-whisper.mjs, modelo small)
node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe -y -v error -i <narracao.mp3> -ar 16000 -ac 1 -c:a pcm_s16le n16k.wav
./whisper.cpp/main.exe -m whisper.cpp/ggml-small.bin -f n16k.wav -l pt -ml 1 -sow -oj -of whisper
# 1) texto do roteiro + tempo do whisper (o whisper quebra acento; o texto vem do roteiro)
python -m uv run python scripts/alinhar_narracao.py whisper.json roteiro.txt n16k.wav palavras-whisper.json
# 2) fusão com o alinhamento forçado CTC (torchaudio MMS_FA; o modelo de 1,2 GB baixa na 1ª vez)
python scripts/alinhar_forcado.py palavras-whisper.json public/fonte/narracao.mp3 palavras.json
# 3) conferir contra o ÁUDIO
python scripts/conferir_alinhamento.py pausas palavras.json public/fonte/narracao.mp3
python scripts/conferir_alinhamento.py faixa palavras.json public/fonte/narracao.mp3 23.1-25.3 --com palavras-whisper.json
```

- **Nenhum alinhador sozinho presta** (lição 56): o whisper deslizou até 0,76 s sem cair
  em pausa; o CTC atrasa ~0,1 s dentro da frase e às vezes 0,2–0,4 s a frase inteira. A
  fusão foi validada contra 109 ataques lidos à mão: mediana 0,02 s, máximo 0,15 s.
- Os limiares da fusão foram calibrados na voz da 07. **Voz ou velocidade nova: leia no
  `faixa` pelo menos o ataque de cada frase** antes de confiar. Todo `<<<` do `pausas`
  (|delta| ≥ 0,06 s) se lê.
- Leitura do envelope: oclusiva (p, t, k) começa num silêncio curto; fricativa (s, f, x)
  é `.`/`:` antes da vogal; respiro antes da frase também é fraco — não é a palavra.

## 5. Roteiro em código

`src/pecas/<peça>/roteiro.ts` importa `palavras.json` e declara, **na ordem da fala**:

| Chamada | Destino da fala |
|---|---|
| `r.b('trecho')` | vira colagem (sistema B) e sai da pílula |
| `r.mudo('trecho')` | a colagem já disse por outro nome; não aparece em lugar nenhum |
| `r.t('trecho')` | só marca tempo; a fala continua na pílula |

**Nenhum segundo digitado — em cena, em `Sons.tsx` nem na trilha.** Tudo lê:

| Precisa de | Use |
|---|---|
| início de um trecho | `S3.prova.inicio` |
| palavra do meio de um trecho | `em(S5.zero, 'defeito')` (lança se não achar) |
| até onde a fala do trecho vai | `depois(faixa)` |
| troca de fase dentro de uma cena | `TROCA.x` (a cena e os `CHICOTES` da raiz leem o mesmo número) |
| início de cena | `CENA_INICIO[i]` |
| duração da peça | `FIM` — já derivado da última palavra + 0,5 s; o teste confere o valor esperado |

Desvio relativo é permitido (`S7.estragar.inicio - 0.13`); número absoluto, não. Na 07,
60 segundos digitados teriam ficado para trás quando o realinhamento moveu palavras 0,7 s.

Pílula (`blocosA` em `src/colagem/legenda.ts`): até 4 palavras e 16 caracteres, partição
por programação dinâmica que pune bloco terminado em palavra fraca (artigo, preposição,
`desse`, `seu`, `nosso`), bloco-relâmpago (< 0,3 s na tela) e bloco que atravessa
respiro. A pílula some no quadro em que um B entra. Copie `tests/especial-roteiro.test.ts`
para a peça nova — é o portão de A/B.

## 6. Assets

1. **Buscar antes de gerar**: `python -m uv run python scripts/biblioteca_colagem.py buscar <termos>`
   (`listar <categoria>`). A biblioteca já tem 74 peças.
2. **Gerar no ChatGPT** (Claude in Chrome): folha de objetos afastados sobre **branco
   liso #FFFFFF**, sem texto, sem embalagem, sem rosto. Mecânica que funciona:
   `insertText` → esperar ~1 s → `el.closest('form').requestSubmit()` (aba de fundo não
   aceita clique); antes de enviar, ler `.ProseMirror` e anexos (lição 37); baixar com
   `fetch(img.src)` + `<a download="nome.png">` (lição 50); **um download por aba** —
   para baixar de novo, abra a conversa numa aba nova (lição 52).
3. **Recortar local** (`scripts/colagem_assets.py` / `colagem_assets_v2.py` como molde):
   limiar de distância ao branco 22 (55 se a sombra entrar), `juntar` 18–24 px,
   `convexo()` para objeto branco sobre branco, `lente_transparente()` para vidro.
   **As 3 variantes de borda (boil) são cortadas pela UNIÃO dos bboxes** — bbox próprio
   faz o objeto pulsar 2,4% a cada 3 quadros (lição 60).
4. Foto real só de `base-curada/01-real-verificada`, via `foto_rasgada()` (aplica EXIF).
   Embalagem só pelo componente `Embalagem` (recorte com laudo); "qualquer pacote" é
   `PacoteGenerico`, sem marca.
5. **Registrar com o prompt** (`registrar(..., prompt=...)`): as 74 peças atuais estão
   sem, e a próxima sessão não consegue refazer uma folha parecida. O id é
   `<data>_<nome>`: `registrar` **recusa id que já existe** (sobrescreveria o PNG que
   outra peça usa) — use nome novo; `substituir=True` só para a MESMA peça refeita. Depois
   `publicar <projeto> <ids>` — ele recusa duas peças de mesmo nome no mesmo projeto,
   porque o projeto lê por nome.

## 7. Cena, câmera, som

Esqueleto: `src/pecas/especial/` (`roteiro.ts`, `apoio.tsx`, `cenas-*.tsx`,
`Especial.tsx`, `Sons.tsx`). Registrar a composição em `src/motor/Raiz.tsx`.

- **Planos**: fundo p 0,5–0,85 · cena p 1 · sombra de folhas p 0,6 (atrás) ou 1,3 (à
  frente) · primeiro plano p 2,4 (borra sozinho acima de 1,4). Câmera = chaves + `deriva` (nunca parada) + `pulso` nas
  palavras-colagem + `tremor` só no impacto.
- **Entradas em stop-motion** (`posterizar` de 3 quadros); só a câmera é lisa. Dymo
  datilografa 1 letra/quadro; `Recortadas` 1 letra a cada 2 quadros.
- **Marcador escreve no tempo da fala**: `dur={fala(faixa)}` (entre 0,5 e 2 quadros por
  letra). O movimento de câmera que um texto espera acontece DURANTE a frase.
- **Toda troca de enquadramento tem chicote ou cobertura** — corte seco de câmera é
  salto. Chicote = imagem que sai e a que entra COLADAS, uma tela inteira em 12 quadros,
  cada lado congelado no seu último/primeiro quadro (`chicoteEm` em `Especial.tsx`).
  Cobertura de papel: 7 quadros, na cor do fundo da cena que entra.
- **Área segura**: texto em x ≈ 140–940 em repouso (a câmera anda ~120 px e amplia até
  ~1,16×), fora dos 5% do topo e dos 16% da base (`MARGEM` de `src/motor/layout.ts`; é
  onde fica a interface do Reels); pílula em y=1500.
- **Perto da embalagem, meça o bbox do alfa do recorte antes**: o PNG tem margem
  transparente (o pacote ocupa só fy 0,17–0,75). Texto nunca cobre logotipo nem selo.
- **Som**: um efeito por entrada (pop no texto, papel no recorte, caneta no traço,
  carimbo no Dymo); chicote soa 0,16 s antes da troca. Trilha em seções que começam em
  FRASES da narração (`inicio_de("Calma")` em `scripts/colagem_sfx_v2.py`, que lê
  `palavras.json`); peça nova copia o script e troca só `PROJ` e as frases.

## 7b. Motion educativo com boneco: o padrão aprovado em 13/10/2026 (peça 08b)

O Reel 08b (`src/pecas/onze/v2/Onze2.tsx`, composição `OnzeProvas2`, 82 s) foi aprovado
pelo cliente depois de uma v1 reprovada ("desincronia, legenda em excesso, boneco bugado,
edição sem vida", lição 68). Ele **substitui a pílula da §7** quando a peça é educativa e
narrada. As referências que o cliente mandou foram o motion de marca do Aryan Raj e o
método do `kaomei/stickman-video-director`, que só serviu para aprender: a peça não tem
nenhum vídeo gerado por IA.

- **Sem pílula.** O texto é a manchete: só a palavra-chave, entrando no QUADRO em que a voz
  a diz (`Manchete` em `src/pecas/onze/teste/TesteCodigo.tsx`, carimbo ≤ 115%). Frases inteiras
  só em serifa, palavra por palavra.
- **Boneco v2** (`src/pecas/onze/teste/BonecoV2.tsx`). Não use o `colagem/boneco.tsx`, cujo
  boil faz o corpo inteiro tremer e lê como falha.
  - membro em curva contínua e cabeça sempre por cima do braço;
  - respira e pisca (`q`);
  - mão por alvo com IK (`alvoD`/`alvoE`, em fração de h a partir dos pés; `ANAT` dá boca e olho);
  - objeto na mão com giro próprio (`giroD`/`giroE`). Sem isso, a caneca gira com o
    antebraço e vira de cabeça para baixo.
- **Uma ação física por cena, em batidas** (anda → pega → usa → reage), nunca uma pose
  congelada por segundos. Analise o trecho do boneco a 6 qps antes de entregar: dois dos três
  defeitos que o cliente apontou só apareciam assim.
- **Objeto que se acumula fica.** Grão jogado na caixa empilha, com giro curto no voo e
  imagem fixa (`Img` sem boil). Se uma peça treme parada, parece defeito.
- **Câmera sempre andando, com parallax** (fundo p 0,3–0,6 · cena 1 · texto 1,1 · folha
  desfocada cruzando a lente p 2,2–2,6). Troca de cena com borrão e deslize de 3 quadros,
  e corte seco só nas rajadas.
- **Vídeo real só em movimento** (nunca a mão parada) e sem repetir o mesmo trecho em duas cenas.
  Os clipes do WhatsApp são 720p: use ampliação ≤ 1,08 e escuro ≤ 0,2.
- **Ritmo:** a narração vem acelerada, então o movimento não compete com ela. Corrida
  ~15 px/quadro, tremor ≤ 14 px e planos ≥ 2 s quando a fala deixa.
- **Gancho com movimento desde o quadro 0:** a câmera mergulha no objeto, setas e círculo
  apontam, e na palavra-virada o quadro congela em P&B com flash e carimbo.
- **Mudança de linguagem:** teste num trecho de 10 s e mostre antes de refazer a peça inteira.

## 8. Conferência (antes de chamar de pronto)

| Ordem | O quê | Como |
|---|---|---|
| 1 | tipos e A/B | `npx tsc --noEmit` · `npx vitest run` (com a cópia do teste de roteiro) |
| 2 | alinhamento | `conferir_alinhamento.py pausas` → ler cada `<<<` com `faixa` |
| 3 | stills dirigidos | `node scripts/contato.mjs <Comp> <projeto> <s1,s2,...> --saida=<nome>.png`: quadro da palavra-colagem e 2 antes (a pílula já saiu?), fim de cada frase de marcador (terminou com a voz?), meio e fim de cada movimento de câmera, **dois quadros DENTRO de cada chicote** |
| 4 | render de teste + varredura | render em segundo plano; `python scripts/varrer_movimento.py <mp4> <quadros das trocas>` — "saltos isolados" tem que sair vazio |
| 5 | render final | só depois de corrigir tudo do teste (trechos com `--frames=a-b` ajudam) |
| 6 | áudio | `node scripts/normalizar-audio.mjs --arquivo=projetos/<p>/saida/reel.mp4` → −14 ±0,5 LUFS, pico ≤ −1 dBTP medido no MP4 |
| 7 | o arquivo que vai ao ar | `python scripts/folha_do_video.py <mp4> <png> <q-2,q+1 de cada troca>` + `ffprobe` (1080×1920, 30 fps, duração) |
| 8 | entrega | mostrar ao usuário cedo; no fim, só `reel.mp4` na `saida/` (apagar crus e testes); commit só dos seus arquivos |

O normalizador mira 0,6 dB abaixo do teto e, se o AAC subir o pico além, refaz pedindo
o teto mais baixo pelo excesso medido (lição 62). "Modo dynamic" no relatório = houve
limitação: ouça.

**Render**: `npx remotion render src/index.ts <Comp> projetos/<p>/saida/reel.mp4
--public-dir=projetos/<p>/public` (de `instagram/remotion`), ~16 min para 79 s nesta
máquina, sempre em segundo plano. Para abortar, `TaskStop` não basta: ache o processo
pela linha de comando que cita a composição e `taskkill /PID <pid> /T /F` (lição 61).

## 9. Descrição do post

Molde pronto: `instagram/remotion/projetos/07-cafe-especial-colagem/legenda-post.md`.

- **Primeira linha ≤ ~55 caracteres** (é o que aparece sobre o Reel) = a pergunta que
  as pessoas buscam ("Como saber se o seu café é especial de verdade ☕"). A busca do
  Instagram lê a descrição, e o Google indexa post público de conta profissional desde
  jul/2025.
- Corpo: a "colinha" do vídeo em blocos curtos (o que faz salvar e mandar por DM — envio
  é o sinal que mais leva a não seguidores); só fatos já verificados; uma linha de fontes.
- Fecho: "Salva pra…" + **pergunta aberta**. Nunca "comenta X que eu te mando": a
  diretriz de recomendação do Instagram deixa de recomendar post que pede palavra
  específica.
- **No máximo 5 hashtags** (limite da plataforma desde dez/2025), como rótulo de assunto.
- Ao publicar: **rótulo de IA ligado** (narração sintética é áudio realista gerado por
  IA — a Meta exige; rotulagem da casa em `docs/POLITICA-IA.md` §5), localização, capa
  legível no corte 3:4 da grade. Diga o que é real
  ("as fotos da lavoura são da nossa fazenda") só se a peça veio de `01-real-verificada`.
  Publicar é ação pública: só com OK explícito do usuário.

## Sinais de que você está saindo do padrão

| Pensamento | Realidade |
|---|---|
| "O whisper já deu os tempos" | Ele deslizou 0,7 s na 07. Funda com o CTC e confira no envelope. |
| "Vou digitar esse segundo só aqui" | Realinhou, ficou para trás. `em()` / `TROCA` / `depois()`. |
| "A diferença é 0,1 s, ninguém vê" | Foi exatamente o que o cliente viu e chamou de dessincronia. |
| "O still antes e depois do chicote está bom" | O defeito (faixa preta) só aparece DENTRO da janela. |
| "Texto em cima do pacote fica bonito" | Tapou o logotipo na 07. Meça o alfa; nunca sobre logo ou selo. |
| "O boil é só trocar a borda" | Bbox por variante faz o objeto respirar. União dos bboxes. |
| "O normalizador recusou por pouco, entrego assim" | Rode de novo com o motor atual; ele corrige a margem. Nunca afrouxe a folga. |
| "Comenta CAFÉ que eu mando o checklist" | Isca de engajamento: o post deixa de ser recomendado. Pergunta aberta. |
| "Reaproveito os tempos da narração anterior" | Áudio acelerado ou regravado = alinhar de novo no arquivo final. |
