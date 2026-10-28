> **Atualização de 28/10/2026 (v3 aprovada):** a meta de densidade deste plano (um evento a cada 0,48 s,
> chicote de 7 q, rajadas) foi o que o cliente devolveu como "movimento extremista". O processo que valeu
> está na skill `canastra-video`, `reel-falado.md`, e nas lições 76–78 do `CLAUDE.md`. Este plano fica como
> histórico da v2. Entrega: `saida/reel-v3.mp4` (58,75 s, voz `voz-sync.wav`, palavras `palavras-v3.json`).

# Plano de edição v2 — Reel 10 "Chafé: dois erros" (segundo a segundo)

Substitui a v1 deste arquivo (27/10). Base: `saida/corte-seco-v2.mp4` (57,7 s, 1730 quadros a 30 fps).
Saída 1080×1920. Tempos em segundos do corte v2, com o quadro entre colchetes. Os tempos das palavras
saíram do whisper (±0,1 s); antes do render são refeitos pelo alinhador forçado (`scripts/alinhar_forcado.py`,
lição 56), e todo evento lê a palavra, nunca um número digitado.

## 0. O que mudou da v1 para a v2

- **Movimento medido, não no olho.** Medi os 12 vídeos salvos no repositório quadro a quadro. Nos 5 do
  @_victorzk, algo novo acontece a cada 0,8–1,2 s (5,7 a 9,0 eventos visuais a cada 10 s). A v1 tinha trechos
  de 3–7 s só com zoom e texto. A v2 tem **111 eventos: um a cada 0,48 s em média, nunca mais de 1,46 s sem
  nada novo, nenhum segundo vazio, no máximo 3 por segundo e nunca dois no mesmo quadro**. Contando só os
  grandes (troca de tela, palavra-chave, transição), são 5,7 a cada 10 s, o mesmo patamar do Victor.
- **O Rafael fica na tela 100% do tempo:** 23 s em tela cheia, 25 s em tela dividida, 8,6 s num círculo
  sobre a colagem. Nenhuma inserção esconde o rosto (as fichas de marca e de influenciador mostram que quem
  fala para a câmera segura o vídeo; o que muda é a imagem que prova cada frase).
- **Câmera 3D de verdade.** Os primeiros 8 s da gravação bruta (`IMG_1128`) mostram a cadeira vazia com a
  câmera no mesmo lugar (desvio medido de 0 a 6 px ao longo dos 20 min). Isso é um **fundo limpo real**: dá para
  mover o fundo separado do Rafael sem abrir buraco, sem inventar nada.
- **Zoom testado no seu vídeo** (nitidez do rosto no tamanho de celular): 1,1× = 90%, 1,2× = 71%, 1,4× = 63%.
  Regra: rosto até 1,15× no normal; 1,4× nunca. A tela dividida mostra o Rafael sem zoom nenhum.
- **O que não temos, geramos** no ChatGPT pelo Chrome, no padrão da skill de imagem (seção 9): xícara de vidro
  com café clarinho, torrões de açúcar, balança, filtro com pó e jarra medidora.

## 1. Princípios (de onde vem cada um)

| # | Princípio | Número | Fonte |
|---|---|---|---|
| 1 | Todo evento cai numa palavra; a palavra-chave entra no quadro em que é dita | erro do alinhador ≤ 0,15 s | lições 56–57 (peça 07 aprovada) |
| 2 | Uma coisa nova por vez | nunca 2 no mesmo quadro; ≤ 3 por segundo | Guaraná (4 rótulos, 1 por vez); lição 68 |
| 3 | Câmera sempre andando por baixo | push/deriva 100% do tempo | lição 68 (08b aprovada); Keeta: "câmera parada denuncia o truque" |
| 4 | Cada frase tem uma imagem que a prova | inserto de ~1 s volta ao rosto | Proud Mary (51 mil, 5× a mediana); Sprometheus (5,2 mi); Morgan (2 mi) |
| 5 | Palavra-chave sai ~0,9 s depois de dita | parada 3 s foi lida como dessincronia | lição 72 (peça 09) |
| 6 | Legenda sempre que não houver texto na tela; nunca as duas dizendo o mesmo | 2 palavras por bloco | regra do Rafael (lição 72); lição 68 |
| 7 | No máximo 3 elementos gráficos ao mesmo tempo, além de legenda e pílula | — | "meia tela + palavra + etiqueta + legenda juntas é demais" (síntese de riscos) |
| 8 | Uma cor de acento (#C8661E) por cena, com função | — | `proibicoes.md` |
| 9 | Corte de capítulo muda a "cor do mundo" | troca de paleta: 10,0% de curtidas/views | BUCK (relatório de motion); rafaelachagas: "uma cor por capítulo" |
| 10 | Mais corte não compra alcance; o que segura é a ideia mudando | Duolingo 0,9 corte/10 s = 11,4%; Pringles 7,3 = 1,2% | motion_marcas; fichas BR |
| 11 | Começar já em movimento e com imagem no quadro 0 | orientação até 1,5 s | `03-roteiro.md`; os 14 influenciadores abrem já mostrando café |
| 12 | O fim emenda no começo (loop) | — | SEY, Black Cat, Morgan |

## 2. Três decisões (minha recomendação em negrito)

1. **Música por baixo da fala:** nenhum vencedor brasileiro com fala usa (19 fichas BR, 21 de processo); o Victor
   usa groove baixo. **Recomendo: sem música sob a voz.** O ritmo vem dos efeitos e do "ar" da sala; um acorde
   curto fecha o vídeo. Alternativa: trilha a −24 dB com ducking.
2. **Chicote de papel** (7 quadros, borrão direcional nos 3 do meio) nas 5 trocas para o círculo e de volta:
   `proibicoes.md` proíbe chicote fora da série de colagem; aqui a linguagem é de colagem. **Recomendo: liberar.**
3. **Congelar em P&B** na palavra-virada "de propósito" (24,24 → 24,91, a pausa que já existe na fala): a 08b
   aprovada fez isso com flash; `proibicoes.md` proíbe flash. **Recomendo: congelar sem flash.**

## 3. Os seis capítulos

| Capítulo | Tempo | Mundo | Acento |
|---|---|---|---|
| 0 · gancho | 0–6,9 | fundo real da torrefação, cor natural corrigida | "CHAFÉ?" |
| 1 · erro 1 | 6,9–19,1 | tela dividida com painel **kraft** (post-it, mostrador, colher) | "≠" |
| 2 · erro 2 | 19,1–35,2 | fundo real **escurecido para #14100D**, cortiça de investigação | "DE PROPÓSITO", "DEFEITO" |
| 3 · o nosso | 35,2–45,6 | o papel escuro **rasga** e o mundo fica **creme**, com a lavoura real | "MARROM" |
| 4 · a receita | 45,6–53,8 | cartão-receita kraft (o quadro que se salva) | "50 g" |
| 5 · fecho | 53,8–57,7 | fundo real, igual ao quadro 0 (loop) | "CHAFÉ?" |

## 4. Câmera 3D (cinco camadas, honestas)

| Camada | O que é | Profundidade |
|---|---|---|
| L0 | **fundo limpo real** (mediana dos quadros 1–7 s do bruto), alinhado por take (dx/dy medidos) e com a exposição igualada à do take | 0,96 |
| L1 | texto atrás da cabeça (oclusão: "CHAFÉ?", "ERRO 2", "NADA PRA ESCONDER") | 0,98 |
| L2 | o Rafael recortado quadro a quadro (`u2net_human_seg`, venv `~/.cache/rbg`, lição 71); borda suavizada 1,5 px e estabilizada entre quadros | 1,00 |
| L3 | objetos, etiquetas, colagem, lupa em primeiro plano | 1,03 (lupa rente à lente: 1,30) |
| L4 | legenda, pílula de capítulo, grão de filme, vinheta (presos à tela) | — |

- **Paralaxe:** no push e na deriva, cada camada anda proporcional à sua profundidade. É isso que dá a
  sensação de câmera 3D, sem girar nada.
- **Limites:** rosto até 1,15×; soco de zoom +6 a +8% em 4 q; push de +4% por frase; deriva ±12 px.
- **Nunca:** girar o pacote em 3D, escala de outdoor, desfocar o fundo para "esconder" (o projeto proíbe bokeh).

## 5. As telas (medidas em 1080×1920)

| Tela | Como é |
|---|---|
| **CHEIO** | vídeo inteiro (720×1280 ampliado 1,5×) com zoom de 1,00 a 1,15× |
| **DIVIDIDA** | painel de imagem em cima (y 0–900); Rafael embaixo (y 900–1920), recorte do vídeo de 720×680 em volta do rosto, **sem zoom extra**; legenda na emenda (y ≈ 900) |
| **CÍRCULO** | tela cheia de colagem; Rafael recortado num círculo de 380 px, centro (820, 1450), borda creme de 8 px, sombra "sobre vídeo" (dy 14, blur 26, 42%) |
| **INVERTIDA** | como a dividida, com o Rafael em cima (só 41,2–43,7, para cobrir um corte interno) |

## 6. Texto e legenda

| Elemento | Fonte e tamanho | Entrada / saída | Onde |
|---|---|---|---|
| Palavra-chave pintada | letras de papel recortado, 220–320 px de altura, 3 variantes trocando a cada 3 q (boil) | carimbo 0→112→97→100% em 4 q, rotação ±3°; sai 0,9 s depois em "desmanche" de 3 q | atrás da cabeça ou no painel; x 120–960, y 270–860 |
| Palavra-chave limpa | Archivo Black, creme #F1ECE0 (terra #3B2A1F no capítulo claro), 140–200 px | 0,85→1,00 com 3% de overshoot em 12 q; sai em t^2,4 em 8 q | idem |
| Dymo | fita preta com relevo, IBM Plex Mono creme, 64 px | a fita desliza em 6 q; letras 1 por quadro | junto do objeto |
| Etiqueta de barbante / post-it | escrita à mão (fonte marcador), 56–72 px | entra balançando (pêndulo amortecido, 20 q) | presa a um objeto |
| Número | IBM Plex Mono 500, 200–260 px | escada de escala 0,6→1,0, contagem quando faz sentido | no cartão |
| Legenda | Inter 700, 72 px, creme com sombra suave, 2 palavras por bloco | corte seco; some no quadro em que a palavra-chave entra | CHEIO: y ≈ 1340; DIVIDIDA: na emenda |
| Pílula de capítulo | Plex Mono 40 px em caixa terra | troca de "1" para "2" com carimbo | canto superior esquerdo, y ≈ 300 |

- **Área segura:** x 120–960; nada abaixo de y ≈ 1400 (nome do perfil, legenda do post e botões do Reels).
- **Ciclo de vida:** objeto sai na troca de bloco; nunca mais de 3 elementos gráficos juntos.
- **Palavras proibidas na tela:** fogo, queimar, queimado, tostar. Sem emoji. Nada de "EXTRAFORTE = DEFEITO":
  a tela não generaliza o que a fala qualifica ("muito extraforte").

## 7. Cor

Medido no corte v2: cast R/B 1,11 (quente/magenta da luz interna no forro), janela estourada em 4,5% do quadro,
pele (115, 92, 84). Alvo da marca: neutro puxando para o frio (R/B 0,97, perfil de câmera do `CLAUDE.md`).

1. **Balanço primeiro:** altas −3% vermelho / +2% azul; médias −2% vermelho; sombras +3% vermelho / −3% azul
   (o tom terra fica nas sombras). Conferir no RGB Parade: R, G e B nivelados nas altas.
2. **Pele:** luminância entre 30% e 45% (faixa de Van Hurkman para o tom dele); médios +5%.
3. **Curva:** preto em 0,02; ombro a partir de 0,75 com teto em 0,94 (a janela vira branco cremoso, não buraco).
4. **Contraste** 1,06 (a compressão do Instagram achata a imagem), **saturação** 0,95, sem nitidez extra.
5. **Por capítulo:** no 2, só o fundo limpo escurece (−70% de exposição, saturação 0,6); no 3, o fundo clareia e
   recebe papel creme a 25%. O Rafael mantém a mesma cor nos três.
6. Grão de filme leve (σ≈0,9, segurado 2 quadros) e vinheta −8%. Aprovar a cor **no celular**.

Teste já feito (`saida/testes/cor-antes-depois.jpg`): R/B caiu de 1,11 para 1,05. Falta a segunda passada.

## 8. Som

**Camadas** (dB relativos ao nível médio da voz):

| Camada | Nível | Onde |
|---|---|---|
| Voz | 0 dB; compressor 3:1, corte abaixo de 80 Hz | o vídeo inteiro |
| Ar da sala | o ruído do próprio take, contínuo | cobre as emendas do corte seco (sem "buraco" de silêncio) |
| Efeitos principais | −9 a −14 | carimbos de palavra-chave, transições, objeto que pousa (~35 no vídeo) |
| Micro-efeitos | −16 a −20 | tick, rabisco, fita Dymo, tink (quase subliminares; o teste de 10 s decide se ficam) |
| Música | nenhuma sob a voz (decisão 1); acorde de 1 s no fim | — |

- **Alinhamento:** o pico de cada som (medido no arquivo, não estimado) cai no quadro do impacto. Chicote e
  whoosh: pico 2–3 quadros antes da troca. Impacto: no primeiro quadro do plano novo, grave e abafado.
- **Proibido:** estalo de fogueira, chiado de chama, "crack" de torra, risada ou meme (lição 66).
- **Final:** −14 LUFS, pico real ≤ −1 dBTP medido no MP4 (teto de trabalho −1,6 com efeitos percussivos, lição 62);
  sincronia da voz medida por correlação no arquivo final (lição 72).
- **Openverse** (CC0, sem chave): carimbo (`rubber stamp`), pop, papel/chicote (`paper whoosh`), rasgo
  (`paper rip`), fita (`tape pull`, `label maker`), tachinha (`thumbtack`), rabisco (`pencil scribble`), grãos/pó
  (`coffee beans pour`), tink de vidro (`glass clink`), torrão (`sugar cube drop`), água (`water pour short`),
  tick. Três candidatos por som → aparar → medir o pico → ouvir e escolher → registrar autor, link e licença
  em `public/sons/creditos.json`. O que faltar sai da biblioteca da peça 07.

## 9. Imagens a gerar (ChatGPT via Claude in Chrome)

Seguem `canastra-conteudo` (fases 1–5) e `colagem.md` §6: objeto isolado sobre branco #FFFFFF, sem texto, sem
embalagem, sem rosto; **uma imagem por conversa nova** (follow-up regenera a cena inteira); gerar em paralelo e
baixar em série; recortar local com `scripts/colagem_assets_v2.py` (limiar 22, `juntar` 18–24 px,
`lente_transparente()` no vidro); registrar na biblioteca **com o prompt**. Número e texto nunca vêm da
geração: visor da balança, marcas da jarra e etiquetas são desenhados em código.

| Id | O quê | Onde entra |
|---|---|---|
| **G1** | xícara de vidro com café filtrado clarinho, translúcido | 0,0 · 7,9 · 18,0 · 39,7 · 56,8 |
| **G3** | três torrões de açúcar | 33,6–34,7 |
| **G4** | balança de cozinha com visor em branco | 47,3–49,9 |
| **G5** | filtro de papel com pó | 14,4–16,3 · 48,6 |
| **G6** | jarra medidora de vidro, vazia, sem marcas | 49,2–49,9 |

**Prompts** (em inglês, como os da skill):

- **G1:** "Photo of a single clear glass cup (straight-sided borosilicate tumbler, no handle) filled to 80% with
  freshly brewed filter coffee, medium roast: the liquid is translucent amber-brown — light passes through it, the
  edges glow lighter and you can faintly see through the coffee. Side view at eye level, cup centred with a generous
  empty margin, on a seamless pure white background (#FFFFFF). Plain even daylight from the front, neutral-to-cool
  white balance. Deep depth of field, everything equally sharp. Realistic smartphone photo of a real object, not a
  3D render, not an illustration. DO NOT INCLUDE: saucer, spoon, steam, foam, crema, latte art, milk, coffee beans,
  cookies, napkin, table surface, plant shadows, window reflections, text, logos, labels, hands, golden or warm
  light, dark opaque coffee, vignette, colour grading, bokeh."
- **G3:** "Three white sugar cubes, real slightly irregular cubes with a few loose crystals, placed apart from each
  other (at least one cube width between them) on a seamless pure white background (#FFFFFF), seen from a 3/4 top
  angle. Plain even daylight, neutral white balance, everything sharp. Realistic smartphone photo, not a render.
  DO NOT INCLUDE: spoon, bowl, coffee, text, logos, props, plant shadows, glitter, colour grading, bokeh."
- **G4:** "A small square digital kitchen scale in plain matte dark grey plastic, flat top platform, small
  rectangular LCD display that is switched on but completely blank (no digits, no symbols). 3/4 front view from
  slightly above, isolated on a seamless pure white background (#FFFFFF), generous margin. Even daylight, neutral
  white balance, everything sharp. Realistic smartphone photo, not a render. DO NOT INCLUDE: any numbers or letters
  on the display, brand names, logos, printed buttons, bowls, coffee, props, colour grading, bokeh."
- **G5:** "A cone-shaped natural brown paper coffee filter, opened, holding medium-ground coffee (loose, matte,
  slightly uneven surface), seen from 45° above, standing on its own, isolated on a seamless pure white background
  (#FFFFFF). Even daylight, neutral white balance, everything sharp. Realistic smartphone photo, not a render.
  DO NOT INCLUDE: coffee maker, carafe, mug, water, steam, beans, spoon, text, logos, props, colour grading, bokeh."
- **G6:** "An empty clear glass measuring jug of about 500 ml with a simple handle and spout, plain glass with NO
  printed numbers, NO measurement lines and NO text. Side view at eye level, isolated on a seamless pure white
  background (#FFFFFF). Even daylight, neutral white balance, everything sharp. Realistic smartphone photo, not a
  render. DO NOT INCLUDE: water, liquid, numbers, markings, logos, text, props, window reflections, colour grading,
  bokeh."

**Conferência (fase 4):** recorte ampliado de cada imagem antes de aprovar; vidro sem halo; nenhuma letra ou número
inventado; cor neutra, sem dourado. Não se gera: pacote (só o packshot real do Suave, com laudo), grão para "mostrar
a torra" e pessoa.

## 10. Segundo a segundo

**Telas:** CHEIO = tela cheia · DIVIDIDA = imagem em cima, Rafael embaixo · CÍRCULO = colagem em tela cheia com o
Rafael num círculo. Sem número = som que fica abaixo de tudo.

| Seg | Fala | Tela | O que entra [quadro] | Som (dB rel. à voz) |
|---|---|---|---|---|
| 0 | Se alguém já chamou o seu | CHEIO · fundo real | **0.00** [0] (quadro 0): xícara de vidro com café clarinho (G1) já no quadro, canto inferior esquerdo, girando 2° e subindo devagar; câmera já em push 1,08→1,14<br>**0.60** [18] chamou: aspas rabiscadas se desenham ao lado da cabeça (8 q): alguém disse algo | —<br>rabisco (-20) |
| 1 | café de chafé, essa | CHEIO · fundo real | **1.10** [33] café: etiqueta Dymo "CAFÉ" pousa na xícara<br>**1.60** [48] chafé: "CHAFÉ?" pintado gigante ATRÁS da cabeça (oclusão, 80% legível) + soco de zoom +6% em 4 q; a etiqueta da xícara vira "CHAFÉ?" | fita Dymo (-18)<br>carimbo grave (-9) |
| 2 | pessoa errou duas | CHEIO · fundo real | **2.34** [70] errou: traço creme risca "CHAFÉ?" (8 q, termina com a palavra)<br>**2.66** [80] duas: "2" carimbado grande à direita | rabisco (-18)<br>pop (-15) |
| 3 | vezes. Eu sou o Rafael, | CHEIO · fundo real | **3.04** [91] vezes: "ERROS" completa "2 ERROS"<br>**3.50** [105] Eu: recuo de 1,14 para 1,00 em 10 q: aparecem torrador e sacas; fundo limpo anda 0,96 e o Rafael 1,00 (paralaxe real)<br>**3.86** [116] Rafael: Dymo "RAFAEL" desliza no peito | pop (-15)<br>whoosh suave (-16)<br>fita Dymo (-18) |
| 4 | aqui do Café Canastra, | CHEIO · fundo real | **4.36** [131] Café: logo Café Canastra (arquivo real) carimba na parede preta, alto à esquerda<br>**4.64** [139] Canastra: polaroide real da lavoura (base verificada) entra girando 8° e pousa no alto à direita | carimbo leve (-14)<br>papel (-16) |
| 5 | e essa aqui é nossa | CHEIO · fundo real | **5.09** [153] (corte interno): troca para 1,10 + deriva para a direita, em direção ao torrador; a polaroide sai deslizando<br>**5.56** [167] aqui: seta rabiscada começa a se desenhar até o torrador (termina em "torrefação") | slide (-18)<br>rabisco (-18) |
| 6 | torrefação. | CHEIO · fundo real → DIVIDIDA · kraft em cima | **6.12** [184] torrefação: etiqueta de barbante "TORREFAÇÃO · UBERLÂNDIA" pendurada no torrador, balançando (presa ao fundo, anda com a paralaxe)<br>**6.88** [206] (fim do bloco): folha kraft varre a tela em 7 q e deixa a TELA DIVIDIDA: painel kraft em cima, Rafael embaixo | tick de papel (-18)<br>papel rápido (pico 2 q antes) (-12) |
| 7 | primeiro erro é achar | DIVIDIDA · kraft em cima | **7.18** [215] primeiro: pílula "ERRO 1" fixa no canto do painel (fica até 19,1 s)<br>**7.48** [224] erro: carimbo "ERRO 1" grande no centro do painel, encolhe até a pílula em 12 q<br>**7.86** [236] achar: xícara de vidro clarinha (G1) sobe para o painel (10 q, assenta) | —<br>carimbo (-10)<br>slide (-18) |
| 8 | que café clarinho é | DIVIDIDA · kraft em cima | **8.46** [254] clarinho: post-it "CLARINHO" preso com tachinha ao lado da xícara | tachinha (-16) |
| 9 | café fraco. A | DIVIDIDA · kraft em cima | **9.38** [281] fraco: post-it "FRACO" entra; um "=" rabiscado liga os dois<br>**9.62** [289] (pausa): carimbo "≠" em #C8661E (acento da cena) esmaga o "="<br>**9.80** [294] (fim do bloco): Rafael embaixo passa a 1,15; o painel desliza para a esquerda e entra o quadro seguinte | tachinha (-16)<br>carimbo (-10)<br>slide (-18) |
| 10 | torra mexe na intensidade | DIVIDIDA · kraft em cima | **10.07** [302] torra: recorte de grão torrado entra no painel com Dymo "TORRA"<br>**10.77** [323] intensidade: mostrador de ponteiro "INTENSIDADE" se desenha (traço creme, sem escala de cor) | pop (-16)<br>rabisco (-18) |
| 11 | sim, mas ninguém precisa | DIVIDIDA · kraft em cima | **11.23** [337] sim: ✓ rabiscado ao lado de "TORRA → INTENSIDADE"; o ponteiro sobe um degrau<br>**11.83** [355] precisa: marca "PONTO" aparece no mostrador | tick (-18)<br>tick (-18) |
| 12 | passar do ponto pra ter | DIVIDIDA · kraft em cima | **12.05** [362] passar: ponteiro desliza até a marca<br>**12.55** [376] ponto: ponteiro FREIA exatamente na marca (3% de ultrapassagem); carimbo "NO PONTO" | slide curto (-18)<br>carimbo leve (-12) |
| 13 | um café intenso. Quer | DIVIDIDA · kraft em cima → CÍRCULO · kraft | **13.41** [402] intenso: "INTENSO" grande + soco de zoom no Rafael (+8%, 4 q)<br>**13.84** [415] (fim do bloco): chicote de papel (7 q): tela cheia de kraft, Rafael vira um círculo no canto inferior direito | pop (-14)<br>chicote (pico 2 q antes) (-12) |
| 14 | mais intensidade? | CÍRCULO · kraft | **14.37** [431] intensidade: filtro com pó (G5) no centro; mostrador pequeno no canto com o ponteiro tremendo "?" | pop (-16) |
| 15 | Coloca um pouquinho mais | CÍRCULO · kraft | **15.01** [450] Coloca: mão com colher entra pela direita (8 q)<br>**15.53** [466] pouquinho: colher despeja: pó caindo em stop-motion (10 poses/s) + "+1" | slide (-18)<br>grãos/pó (-14) |
| 16 | de pó. O café se | CÍRCULO · kraft → DIVIDIDA · kraft | **16.31** [489] pó: segunda colherada "+2" + Dymo "PÓ"<br>**16.45** [494] (fim do bloco): chicote de volta para a tela dividida<br>**16.86** [506] se: ponteiro do mostrador sobe com o pó (a intensidade vem do pó) | grãos/pó (-14)<br>chicote (-12)<br>tick (-18) |
| 17 | intensifica e o | DIVIDIDA · kraft | **17.12** [514] intensifica: "INTENSIFICA" engorda de 100% para 120% em 15 q | pop (-14) |
| 18 | sabor fica todo lá. | DIVIDIDA · kraft | **18.00** [540] sabor: xícara clarinha volta com etiqueta "SABOR"<br>**18.48** [554] todo: ✓ rabiscado em "SABOR" | tink de vidro (-18)<br>rabisco (-20) |
| 19 | E agora, o segundo | DIVIDIDA · kraft → CHEIO · fundo escuro | **19.05** [572] (fim do bloco): tela cheia; o fundo limpo escurece para #14100D em 8 q, o Rafael continua aceso (troca de capítulo)<br>**19.94** [598] segundo: "2" gigante creme ATRÁS da cabeça | grave abafado (-12)<br>pop grave (-12) |
| 20 | erro e esse | CHEIO · fundo escuro | **20.34** [610] erro: "ERRO" completa "ERRO 2"; a pílula do canto vira 2<br>**20.78** [623] esse: push lento 1,00→1,12 em 1,5 s (tensão) | carimbo (-10)<br>— |
| 21 | quase ninguém conta. | CHEIO · fundo escuro | **21.42** [643] ninguém: Dymo "QUASE NINGUÉM CONTA" desliza<br>**21.88** [656] conta: lupa entra do canto inferior e para sobre o Dymo | fita Dymo (-18)<br>slide (-18) |
| 22 | Muito extra forte | CHEIO · fundo escuro → DIVIDIDA · cortiça escura | **22.16** [665] (fim do bloco): tela dividida escura: em cima, cortiça (quadro de investigação); Rafael embaixo a 1,10<br>**22.48** [674] extra: pacote genérico SEM MARCA (desenhado em código) pendurado por tachinha, etiqueta "MUITO EXTRAFORTE" | slide (-16)<br>tachinha (-16) |
| 23 | passa do ponto de | DIVIDIDA · cortiça escura | **23.16** [695] passa: o mostrador volta na cortiça; o ponteiro anda<br>**23.68** [710] ponto: ponteiro PASSA da marca e continua | tick (-18)<br>tick duplo (-16) |
| 24 | propósito. | DIVIDIDA · cortiça escura → CONGELADO P&B → CHEIO · fundo escuro | **24.24** [727] propósito: "DE PROPÓSITO" pintado em #C8661E, carimbado na diagonal; a imagem congela em P&B na pausa até 24,91<br>**24.91** [747] (fim do bloco): descongela; Rafael em tela cheia a 1,10, fundo escuro | carimbo grave (-9)<br>— |
| 25 | Isso porque o grão tem | CHEIO · fundo escuro | **25.10** [753] Isso: lupa grande atravessa rente à lente (primeiro plano, profundidade 1,3) | whoosh suave (-16) |
| 26 | defeito. Grão | CHEIO · fundo escuro → CÍRCULO · cortiça | **26.18** [785] defeito: zoom pelo aro da lupa: tela cheia de cortiça com peneira de classificação; Rafael em círculo; "DEFEITO" em #C8661E<br>**26.40** [792] (rajada): rajada de 7 defeitos da biblioteca (concha, filme, fungo, imaturo, preto partido, quaker, quebrado), 4 q cada, dentro da lente | whoosh + carimbo (-12)<br>tick por grão (-20) |
| 27 | preto, ardido, | CÍRCULO · cortiça | **27.13** [814] preto: grão preto preso com tachinha + etiqueta "PRETO"<br>**27.76** [833] ardido: grão ardido + etiqueta "ARDIDO" | tachinha (-15)<br>tachinha (-15) |
| 28 | furado de broca. | CÍRCULO · cortiça | **28.36** [851] furado: grão brocado + etiqueta "BROCA"<br>**28.92** [868] broca: lupa passa sobre os furos do brocado (zoom de 1,10 na cena) | tachinha (-15)<br>— |
| 29 | Passando do ponto, | CÍRCULO · cortiça | **29.41** [882] Passando: fita-crepe começa a desenrolar pela esquerda | fita puxada (-14) |
| 30 | tudo vira o mesmo amargo | CÍRCULO · cortiça | **30.37** [911] tudo: fita cobre o 1º grão<br>**30.81** [924] mesmo: fita cobre o 2º grão<br>**30.99** [930] amargo: "AMARGO" escrito à mão na fita; ela cobre o 3º grão | fita (-18)<br>fita (-18)<br>rabisco (-16) |
| 31 | e o defeito some. | CÍRCULO · cortiça | **31.61** [948] defeito: lupa passa sobre a fita e não acha nada; as etiquetas penduradas continuam aparecendo<br>**31.89** [957] some: carimbo "ESCONDIDO" (terra/creme) | slide (-20)<br>carimbo (-10) |
| 32 | Daí a pessoa | CÍRCULO · cortiça → CHEIO · escuro leve | **32.17** [965] (fim do bloco): chicote de volta: Rafael em close a 1,15, fundo escuro mais leve (respiro) | chicote (-12) |
| 33 | coloca açúcar | CHEIO · escuro leve | **33.20** [996] coloca: colher vazia entra sobre uma xícara de café preto (recorte xícara)<br>**33.56** [1007] açúcar: 1º torrão (G3) cai da colher e quica | slide (-18)<br>tink (-18) |
| 34 | pra aguentar tomar. | CHEIO · escuro leve | **34.38** [1031] aguentar: 2º torrão<br>**34.74** [1042] tomar: 3º torrão; o Rafael meio-sorri | tink (-18)<br>tink (-18) |
| 35 | café que não tem | CHEIO · escuro leve → CHEIO · fundo claro + lavoura | **35.23** [1057] (fim do bloco): o papel escuro RASGA e revela o fundo claro creme (capítulo 3: nada a esconder)<br>**35.49** [1065] café: foto real da lavoura presa com fita na parede atrás dele (impressão, não cenário) | rasgo de papel (-10)<br>fita (-18) |
| 36 | nada pra esconder | CHEIO · fundo claro + lavoura | **36.13** [1084] nada: lupa passa pela lavoura e aparece um ✓ limpo<br>**36.63** [1099] esconder: "NADA PRA ESCONDER" em terra #3B2A1F atrás da cabeça | rabisco (-18)<br>pop (-14) |
| 37 | pode parar no marrom. | CHEIO · fundo claro + lavoura → DIVIDIDA · creme em cima | **37.41** [1122] parar: tela dividida clara: painel creme em cima, Rafael embaixo<br>**37.79** [1134] marrom: packshot REAL do Suave sobe e assenta (sem girar, sem deformar); "MARROM" em #C8661E | slide (-16)<br>thump (-12) |
| 38 | essa é a torra | DIVIDIDA · creme em cima | **38.12** [1144] (fim do bloco): Rafael embaixo passa a 1,15<br>**38.81** [1164] torra: etiqueta de barbante "TORRA MÉDIA" pendurada ao lado do pacote (nunca sobre logo ou selo) | —<br>tick de papel (-18) |
| 39 | média, a luz atravessa | DIVIDIDA · creme em cima | **39.73** [1192] luz: xícara clarinha (G1) entra ao lado do Suave; sombra de folhas passa pelo painel<br>**39.89** [1197] atravessa: varredura de luz creme (não dourada) atravessa a xícara em 12 q | slide (-18)<br>brilho (-20) |
| 40 | a xícara, | DIVIDIDA · creme em cima | **40.83** [1225] xícara: a xícara inclina 2° | tink de vidro (-18) |
| 41 | o gosto puxa | DIVIDIDA · creme em cima → DIVIDIDA invertida · creme embaixo | **41.20** [1236] (corte interno): a tela dividida inverte: imagem embaixo, Rafael em cima<br>**41.51** [1245] gosto: traço creme sai da xícara e começa uma seta curva | slide (-16)<br>golinho (-16) |
| 42 | um pouquinho pro chocolate | DIVIDIDA invertida · creme embaixo | **42.97** [1289] chocolate: "CHOCOLATE" na ponta da seta (só a palavra, sem foto de chocolate) | pop (-14) |
| 43 | e ainda | DIVIDIDA invertida · creme embaixo → DIVIDIDA · creme em cima | **43.66** [1310] (corte interno): volta: Rafael embaixo a 1,10<br>**43.89** [1317] ainda: a seta continua para a segunda ponta | slide (-18)<br>rabisco (-20) |
| 44 | tem um azedinho de fruta | DIVIDIDA · creme em cima | **44.27** [1328] azedinho: Dymo "AZEDINHO"<br>**44.97** [1349] fruta: cereja vermelha (a fruta do próprio café) pousa na ponta da seta | fita Dymo (-18)<br>pop (-14) |
| 45 | no fim. no | DIVIDIDA · creme em cima → DIVIDIDA · cartão-receita | **45.37** [1361] fim: ✓ rabiscado<br>**45.64** [1369] (fim do bloco): cartão-receita kraft sobe e ocupa a metade de cima | rabisco (-20)<br>papel (-14) |
| 46 | Café Canastra a | DIVIDIDA · cartão-receita | **46.47** [1394] Canastra: logo Café Canastra carimba no topo do cartão (segunda vez, outra posição) | carimbo leve (-14) |
| 47 | nossa conta é 50 | DIVIDIDA · cartão-receita | **47.27** [1418] conta: balança (G4) entra no cartão<br>**47.57** [1427] 50: visor da balança conta de 0 a 50 em 10 q + "50 g" grande em Plex Mono | slide (-18)<br>tick + carimbo (-12) |
| 48 | gramas de pó para | DIVIDIDA · cartão-receita | **48.63** [1459] pó: filtro com pó (G5) pousa na balança | grãos/pó (-16) |
| 49 | meio litro d 'água. | DIVIDIDA · cartão-receita | **49.17** [1475] meio: jarra medidora (G6) entra<br>**49.39** [1482] litro: "500 ml" carimbado<br>**49.87** [1496] água: a água sobe na jarra até a marca | tink de vidro (-18)<br>carimbo (-12)<br>água curta (-18) |
| 50 | Gosta de mais intenso? | DIVIDIDA · cartão-receita | **50.00** [1500] (fim do bloco): Rafael embaixo passa a 1,15<br>**50.68** [1520] intenso: mostrador pequeno: o ponteiro sobe | —<br>tick (-18) |
| 51 | Lembra do primeiro erro? | DIVIDIDA · cartão-receita → CHEIO · fundo real | **51.15** [1534] (corte interno): o cartão sobe e sai (ficou 3,6 s na tela para quem quiser salvar); Rafael em tela cheia a 1,10<br>**51.59** [1548] primeiro: eco: "ERRO 1" volta igual ao 7,48 por 0,5 s, atrás da cabeça | slide (-16)<br>whoosh reverso (-16) |
| 52 | Coloca um pouquinho | CHEIO · fundo real | **52.27** [1568] Coloca: a mão com colher do 15,01 entra rápido<br>**52.83** [1585] pouquinho: colherada "+1" | slide (-18)<br>grãos/pó (-16) |
| 53 | mais de pó. | CHEIO · fundo real → CHEIO · fundo real (fecho) | **53.75** [1612] pó: "+ PÓ" (o mesmo cartão do 16,31)<br>**53.84** [1615] (fim do bloco): tudo sai num só movimento; volta o fundo real com a cor natural (capítulo final) | pop (-14)<br>whoosh (-12) |
| 54 | agora, não perde | CHEIO · fundo real (fecho) | **54.11** [1623] agora: rajada de recapitulação no lado direito: CHAFÉ? → ERRO 1 → ERRO 2 → Suave, 7 q cada | tick por cartão (-20) |
| 55 | tempo, manda isso aí pra | CHEIO · fundo real (fecho) | **55.07** [1652] tempo: a rajada termina no Suave, que fica<br>**55.30** [1659] (corte interno): close a 1,14, o mesmo enquadramento do quadro 0 (prepara o loop)<br>**55.50** [1665] manda: aviãozinho de papel rabiscado sai da mão dele e voa para fora do quadro | pop (-16)<br>—<br>whoosh curto (-14) |
| 56 | aquele amigo que ainda chama isso aqui | CHEIO · fundo real (fecho) | **56.10** [1683] amigo: "MANDA PRO AMIGO" pequeno em creme<br>**56.78** [1703] isso: a xícara clarinha (G1) volta ao canto inferior esquerdo, igual ao quadro 0 | pop (-16)<br>slide (-18) |
| 57 | de chafé. | CHEIO · fundo real (fecho) | **57.26** [1718] chafé: "CHAFÉ?" volta atrás da cabeça, igual ao 1,60; o último quadro emenda no primeiro | carimbo grave (-9) |

**Conferência automática da tabela** (`eventos.json`, gerado do mesmo arquivo): 111 eventos · intervalo
mediano 0,48 s · maior intervalo 1,46 s (41,51 → 42,97, com a seta se desenhando no meio) · nenhum segundo sem
evento · no máximo 3 por segundo · nenhum quadro com 2 eventos · os 22 pulos do corte seco caem todos numa troca
de tela ou dentro de uma colagem.

## 11. Produção, na ordem

1. **Fundo limpo:** mediana dos quadros 1–7 s do bruto; alinhar e igualar a exposição por take; conferir num
   mosaico se o contorno do Rafael não "vaza" no movimento.
2. **Recorte do Rafael** nos 1730 quadros (20–30 min de CPU); conferir a borda a 6 quadros por segundo sobre fundo
   escuro e sobre creme (borda tremendo parece falha, como o boneco da 08b).
3. **Alinhador forçado** na fala do corte v2 → tempo de cada palavra; atualizar `eventos.json`.
4. **Cor** (seção 7) e conferência no celular.
5. **Imagens G1, G3–G6** no ChatGPT (seção 9) e recorte.
6. **Sons** do Openverse, com o pico de cada um medido.
7. **Composição** em `instagram/remotion/src/pecas/chafe/`, no padrão da peça 07: camadas L0–L4 e o roteiro em
   código lendo `eventos.json`.
8. **Teste de 10 s antes de tudo** (lição 68): o trecho **16,5–26,7 s**, que tem a troca de capítulo, o fundo
   escurecendo, a tela dividida escura, o mostrador, o congelado em P&B e a entrada pela lupa. Vai para você
   aprovar ritmo, densidade e som antes do render inteiro.
9. Render inteiro → um still por segundo → normalização do áudio → folha de contato, teste a 360 px (celular) e
   loop.

## 12. O que preciso de você

- As **3 decisões** da seção 2 (ou "vai com as suas recomendações").
- **Ok para gerar** as 5 imagens da seção 9 no ChatGPT e **baixar ~30 sons CC0** do Openverse (quase todos com
  menos de 1 s, uns 3 MB).

## Fontes

- **Repositório (lido inteiro por 10 leituras em paralelo):** 131 fichas de `instagram/referencias-virais/videos/`
  (brasil 19, processo 21, influenciadores 14, marcas 18, motion-criadores 15, motion-brasil 14, motion-marcas 15,
  motion-3d-fooh 15); 5 análises em `raspagem/_motion-referencias/victorzk/`; `relatorio.md`,
  `relatorio-motion.md` e as 13 sínteses; `docs/motion-colagem.md`, `docs/INVENTARIO-REFERENCIAS.md`;
  `instagram/estrategia/03-roteiro.md`, `05-formatos.md`, `07-nao-fazer.md`; `instagram/aprendizados/` (rafaelachagas);
  `instagram/licoes.md`; peça 09 (decupagem, roteiro, legenda); lições 48–75 do `CLAUDE.md`; specs da peça 06 e do
  estúdio de reels. As 177 transcrições de marketplace foram abertas uma a uma: são só fala, sem nenhum quadro, então
  não servem para edição visual.
- **Medição própria:** movimento por segundo dos 12 vídeos salvos; nitidez do zoom no seu vídeo; alinhamento do fundo
  limpo; cor do corte v2.
- **Mercado (web):** [Joyspace, pattern interrupt](https://joyspace.ai/pattern-interrupt-reset-attention-span) ·
  [Joyspace, estilo Hormozi 2026](https://joyspace.ai/hormozi-editing-style-2026-analysis) ·
  [Choppity, Hormozi](https://www.choppity.com/tools/recreate-video-editing-style/alex-hormozi/) ·
  [Async, edição de Reels](https://async.com/blog/how-to-edit-instagram-reels/) ·
  [Firecut, punch-in](https://firecut.ai/blog/how-to-zoom-in-on-premiere-pro-a-step-by-step-guide-for-beginners/) ·
  [Blitzcut, tamanho de legenda](https://blitzcutai.com/blog/best-caption-size-instagram-reels-2026) ·
  [Netflix, legenda PT-BR](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215600497-Portuguese-Brazil-Timed-Text-Style-Guide) ·
  [Socialync, safe zone Reels](https://www.socialync.io/tools/safe-zones/instagram-reels) ·
  [Cutsio, pop de texto](https://cutsio.com/blog/pop-up-text-tutorial-in-davinci-resolve-text-bounce-effect) ·
  [PremiumBeat, whip pan](https://www.premiumbeat.com/blog/create-whip-pan-using-built-effects-premiere-pro/) ·
  [PremiumBeat, recorte de pessoa](https://www.premiumbeat.com/blog/rotobrush-after-effects-tutorial) ·
  [Motion Array, 2.5D](https://blog.motionarray.com/learn/after-effects/animate-flat-2d-images-after-effects/) ·
  [Morphic, efeitos de transição](https://morphic.com/resources/sounds/transition-sound-effects) ·
  [Pixflow, mixagem](https://pixflow.net/blog/audio-mixing-premiere-pro/) ·
  [Vidpros, música alta](https://vidpros.com/fix-background-music-too-loud-video/) ·
  [Fora Soft, LUFS](https://www.forasoft.com/learn/audio-for-video/articles-audio/lufs-targets-per-platform-2026) ·
  [Larry Jordan, tom de pele](https://larryjordan.com/articles/the-secret-to-setting-skin-colors-accurately/) ·
  [Frame.io, pele no Resolve](https://blog.frame.io/2020/10/05/skin-tones-in-davinci-resolve/) ·
  [AIR, excesso de efeito](https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8)
