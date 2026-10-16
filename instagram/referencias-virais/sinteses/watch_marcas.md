# Reels mais vistos de marcas e torrefações de café especial: análise quadro a quadro

Método: em 11/10/2026, abri a grade `/reels/` de cada perfil no Chrome logado e li a contagem de views de cada Reel (rolando a grade). Baixei os 2–3 mais vistos com yt-dlp e analisei localmente com ffmpeg (cortes com `scene>0.25` e folhas de quadros com carimbo de tempo) e whisper.cpp small. Olhei cada folha. Nada foi enviado a serviço externo; a mídia de terceiros fica só na scratchpad. Foram 18 vídeos de 7 contas.

Correções de handle: **`lacabra` não existe** (página indisponível); o perfil certo é `@lacabracoffee`. **`@nomadcoffeelab` está parado desde o início de 2021** (último post `CKUB7O-LWC7`, sem aba de Reels ativa); a Nomad (Barcelona) publica hoje como `@nomadcoffee`. Como contraste de massa, usei `@starbucks`.

**Ressalva importante:** a grade mostra só views. Não há como separar alcance orgânico de impulsionado. Os 3 primeiros da Blue Bottle são posts colaborativos da **Nespresso** e quase certamente pagos.

## Índice dos arquivos por vídeo

Pasta: `videos/marcas/`

| # | Arquivo | Views (grade) | Duração | Cortes / 10 s | Tem fala? |
|---|---|---:|---:|---:|---|
| 1 | [onyxcoffeelab_Dbdlv_5CFvB](../videos/marcas/onyxcoffeelab_Dbdlv_5CFvB.md) — taiyaki (comida) | 49,5 mil | 16 s | 3,2 | não (música) |
| 2 | [onyxcoffeelab_DcT14-qx6pM](../videos/marcas/onyxcoffeelab_DcT14-qx6pM.md) — paródia de luta livre, blend Morning Mayhem | 49,4 mil | 64 s | 1,3 | sim |
| 3 | [onyxcoffeelab_Db6L8cPJ5Jj](../videos/marcas/onyxcoffeelab_Db6L8cPJ5Jj.md) — discurso de mountain bike (loop duplicado) | 47,2 mil | 122 s | 2,5 | sim |
| 4 | [seycoffee_DYpiwKZR1ks](../videos/marcas/seycoffee_DYpiwKZR1ks.md) — recap do evento SEY House | 47,8 mil | 60 s | 8,3 | não (música) |
| 5 | [seycoffee_DdXVF0-o1xu](../videos/marcas/seycoffee_DdXVF0-o1xu.md) — loop gráfico do rótulo (lançamento Gesha) | 29,8 mil | 24 s | 6,2 | não |
| 6 | [lacabracoffee_CsoTJECgvES](../videos/marcas/lacabracoffee_CsoTJECgvES.md) — abertura da loja no Soho, NY | 132 mil | 38 s | 2,7 | não (música) |
| 7 | [lacabracoffee_C017i9wN2O_](../videos/marcas/lacabracoffee_C017i9wN2O_.md) — série Rituals, Paris | 100 mil | 66 s | 5,5 | sim (voz da protagonista) |
| 8 | [lacabracoffee_DSmaaz3DWOX](../videos/marcas/lacabracoffee_DSmaaz3DWOX.md) — série Rituals, Seul | 69,6 mil | 82 s | 5,5 | sim (coreano) |
| 9 | [bluebottle_DO_MzbODBzQ](../videos/marcas/bluebottle_DO_MzbODBzQ.md) — Nespresso × Blue Bottle Blend No.2 | 355 mil | 23 s | 4,3 | não |
| 10 | [bluebottle_DKrnvXvt72X](../videos/marcas/bluebottle_DKrnvXvt72X.md) — Nespresso × NOLA, teaser | 273 mil | 21 s | 6,3 | não (presumido) |
| 11 | [bluebottle_DKwzk3ztsKq](../videos/marcas/bluebottle_DKwzk3ztsKq.md) — Nespresso × NOLA, lançamento | 200 mil | 30 s | 6,1 | não (presumido) |
| 12 | [bluebottle_DdWpu4yMpxk](../videos/marcas/bluebottle_DdWpu4yMpxk.md) — jazz × café, colagem de papel (melhor orgânico) | 113 mil | 16 s | 16,4 | não (jazz) |
| 13 | [nomadcoffee_DV8gTwyDK9W](../videos/marcas/nomadcoffee_DV8gTwyDK9W.md) — pop-up com o chef Blancooks | 89 mil | 65 s | 12,3 | não |
| 14 | [nomadcoffee_DZ5Q5B9inoj](../videos/marcas/nomadcoffee_DZ5Q5B9inoj.md) — minidoc Juan Bohajar (Cristal Antiguo) | 41,5 mil | 97 s | 3,9 | sim (espanhol) |
| 15 | [proudmarycoffee_Da1SakEtUHD](../videos/marcas/proudmarycoffee_Da1SakEtUHD.md) — campeão de barista dos EUA, olho roxo | 51,4 mil | 33 s | 6,4 | sim |
| 16 | [proudmarycoffee_DZ2txUDu-PL](../videos/marcas/proudmarycoffee_DZ2txUDu-PL.md) — highlights do campeonato | 38,3 mil | 30 s | 3,3 | sim |
| 17 | [starbucks_DdRM4oglV5o](../videos/marcas/starbucks_DdRM4oglV5o.md) — gato preto derruba o Black Cat Frappuccino | 14,6 mi | 6 s | 3,2 | sim (1 frase) |
| 18 | [starbucks_DcbH1Lhtiy0](../videos/marcas/starbucks_DcbH1Lhtiy0.md) — volta do PSL com celebridade, autoironia "basic" | 11,1 mi | 28 s | 2,9 | sim |

## Pergunta 1: o que está por trás dos Reels mais vistos de cada marca?

### Takeaway
Nas torrefações de especial, **o topo do grid quase nunca é "um vídeo sobre café"**. Os tops são: comida (taiyaki, pop-up de chef), comunidade e eventos (mountain bike, SEY House, campeonato de barista), lugar (loja nova), retratos de pessoas (série Rituals, minidoc da Nomad) e parcerias com marca grande (Nespresso). O café entra como gesto ou objeto de cena. Na Starbucks, o top é o **produto como piada** (gato preto derruba o Black Cat Frappuccino, 6 s, 14,6 mi).

### Cited Findings

**Tabela por vídeo** (gancho / quem está na câmera / formato / produto / humor / som / fecho):

| Vídeo | Gancho 0–3 s | Na câmera | Formato | Café / torra / origem | Humor | Som | Fecho / CTA |
|---|---|---|---|---|---|---|---|
| [Onyx taiyaki](https://www.instagram.com/reel/Dbdlv_5CFvB/) | massa entrando na forma de peixe, macro | funcionário (mãos, rosto 1 s) | b-roll de processo | ausente (é comida) | não | música | produto no balcão |
| [Onyx Morning Mayhem](https://www.instagram.com/reel/DcT14-qx6pM/) | caixa do blend na lente + grito "Wake up" | artistas convidados (personagens) | esquete/paródia, plano quase contínuo | caixa sempre visível; "so strong" | **sim, ligado ao produto** (blend com nome de luta) | fala + legenda pixelada | ingressos para shows |
| [Onyx MTB](https://www.instagram.com/reel/Db6L8cPJ5Jj/) | orador no púlpito + fachada ONYX | diretor de ciclismo | talking head de evento | ausente | não | fala | — |
| [SEY House](https://www.instagram.com/reel/DYpiwKZR1ks/) | vitrine "HYUNAH × SEY" | comunidade (produtores, baristas) | recap no tempo da música (~1 corte/1,07 s) | coado em macro, cartão "washed" | não | música | cartela das duas marcas |
| [SEY rótulo](https://www.instagram.com/reel/DdXVF0-o1xu/) | rótulo sobre fundo que troca de cor a cada 1 s | ninguém | gráfico em loop | só a arte; origem na legenda | não | sem voz | "OUT NOW" (legenda) |
| [La Cabra Soho](https://www.instagram.com/reel/CsoTJECgvES/) | fachada vista da rua, trânsito borrado | funcionária arrumando flores | tour contemplativo, planos fixos | pacotes como cenografia | não | música | logotipo no reflexo |
| [La Cabra Rituals Paris](https://www.instagram.com/reel/C017i9wN2O_/) | pôr do sol no Sena + título "Rituals" | criadora convidada | minidoc retrato, voz própria | preparo do coado como ritual; pacote 1x | não | voz + música | título da série |
| [La Cabra Rituals Seul](https://www.instagram.com/reel/DSmaaz3DWOX/) | rua de Seul + cabra do logo animada em traço | artista convidada | minidoc retrato, voz própria (coreano) | ritual de chá/café | não | voz + ambiente | título da série |
| [BB × Nespresso Blend No.2](https://www.instagram.com/reel/DO_MzbODBzQ/) | cápsula + "INTRODUCING" | mãos | comercial de estúdio | cápsula, extração, crema | não | música | logos |
| [BB × Nespresso NOLA teaser](https://www.instagram.com/reel/DKrnvXvt72X/) | mulher usa a cápsula como monóculo | modelos | clipe de moda e verão | cápsula como brinquedo | leve (gesto) | música | "coming soon" |
| [BB × Nespresso NOLA](https://www.instagram.com/reel/DKwzk3ztsKq/) | "A New Way to NOLA" | modelos | clipe + cartelas de máquina de escrever | bebida gelada | não | música | "Click, Sip, Repeat Often" |
| [BB jazz](https://www.instagram.com/reel/DdWpu4yMpxk/) | foto de arquivo P&B + mão de papel azul animada | ninguém (fotos de arquivo) | **colagem animada** com 1 cor de marca | grão e extração P&B; torra só na legenda | não | jazz | caneca com o logo |
| [Nomad × Blancooks](https://www.instagram.com/reel/DV8gTwyDK9W/) | calçots cortados e descascados, vista de cima | mãos do chef | receita rápida (80 cortes em 65 s) | ausente; **fogo de maçarico na comida** | não | música | cartela de serviço do pop-up |
| [Nomad Cristal Antiguo](https://www.instagram.com/reel/DZ5Q5B9inoj/) | homem cozinhando + "toda a louça da minha casa é cristal antigo" | personagem convidado | minidoc, voz própria | moka servida em xícara de 1970 | não | voz + ambiente | herança do avô |
| [Proud Mary campeão](https://www.instagram.com/reel/Da1SakEtUHD/) | talking head **com olho roxo** + legenda karaokê | barista campeão | talking head + b-roll | competição, cupping, lavoura | sim, autodepreciativo ("unhinged") | voz | "acompanhe a série" |
| [Proud Mary highlights](https://www.instagram.com/reel/DZ2txUDu-PL/) | logo do campeonato no palco | barista da casa | highlights de competição | descritores sensoriais na fala | não | voz + música | logo do evento |
| [Starbucks Black Cat](https://www.instagram.com/reel/DdRM4oglV5o/) | gato preto passa e revela o drink, depois o derruba | gato influenciador | gag de 6 s | o produto é a piada | **sim, 100% ligado ao produto** | 1 frase em off | nome + data |
| [Starbucks PSL](https://www.instagram.com/reel/DcbH1Lhtiy0/) | celebridade: "the drink that makes us all a little more basic?" | celebridade + ator | esquete de diálogo | produto e aroma | **sim, autoironia** | fala + música pop | nome + data |

**Ritmo de publicação na aba Reels** (datas tiradas do shortcode, conferidas contra a data do yt-dlp):

| Conta | Janela lida | Reels | Ritmo |
|---|---|---:|---|
| [@onyxcoffeelab](https://www.instagram.com/onyxcoffeelab/reels/) | 16/07–11/10/2026 | 60 | **~4,8/semana**; views de 10 a 50 mil, mediana ~16 mil |
| [@starbucks](https://www.instagram.com/starbucks/reels/) | 24/07–09/10/2026 | 42 | ~3,8/semana; 0,1 a 14,6 mi |
| [@proudmarycoffee](https://www.instagram.com/proudmarycoffee/reels/) | 31/12/2025–09/10/2026 | 45 | ~1,1/semana; mediana ~9 mil |
| [@bluebottle](https://www.instagram.com/bluebottle/reels/) | 28/04/2025–29/09/2026 | 42 | ~0,6/semana; 20–50 mil orgânico |
| [@nomadcoffee](https://www.instagram.com/nomadcoffee/reels/) | 03/10/2025–28/09/2026 | 27 | ~0,5/semana; 3–89 mil |
| [@lacabracoffee](https://www.instagram.com/lacabracoffee/reels/) | 09/2021–08/2026 | 42 (total) | ~0,16/semana (1 a cada ~6 semanas) |
| [@seycoffee](https://www.instagram.com/seycoffee/reels/) | 2017?–09/2026 | 11 (total) | quase nenhum; é uma conta de foto |

**Mix de conteúdo visto no grid (pelas miniaturas e pelos vídeos analisados):** Onyx = loja, comida, eventos da cidade, collabs com músicos e atletas, bebidas; Proud Mary = equipe, competição, viagens a origem, humor de bastidor; Blue Bottle = bebidas, lojas, collab Nespresso, peças editoriais; La Cabra = lojas, série Rituals, produto; Nomad = pop-ups com chefs, minidocs de pessoas, café; SEY = lançamentos e eventos. Fontes: grades de Reels acima.

### Inferences
- Para torrefação de especial, um Reel "viral" fica na faixa de **30 a 130 mil views**. Fora disso, é mídia paga ou parceria com marca de massa (Blue Bottle × Nespresso: 200 a 355 mil). Nenhuma das seis torrefações tem Reel orgânico de milhões. Meta realista para a Canastra: estar 3–5x acima da própria mediana, não "viralizar".
- O que mais aparece nos tops é **gente de fora com audiência própria**: chef, artista convidada da série Rituals, músicos, campeão de barista, gato influenciador, produtores num evento. Na prática, o post colaborativo é o maior distribuidor.
- Formato não é o fator principal. Ganham tanto o plano fixo lento (La Cabra, ~1 corte/3,4 s) quanto o corte frenético (Nomad, 1 corte/0,8 s; Blue Bottle jazz, colagem com boil). O que se repete é **uma ideia só, clara no primeiro segundo**.

### Gaps
- Não dá para saber, a partir da grade, quais Reels foram impulsionados. Isso é suspeita forte nos três Blue Bottle × Nespresso e possível em outros.
- A grade da Onyx e da Starbucks foi lida só nos últimos ~3 meses (rolagem limitada pela janela oculta do Chrome e pelo navegador travando sob carga). Pode haver hits mais antigos maiores. A da La Cabra, da Proud Mary (~10 meses) e da SEY foram lidas por completo ou quase.
- Os três Blue Bottle × Nespresso e o Nomad × Blancooks não tiveram transcrição de áudio completa (whisper estourou o tempo por CPU saturada ou laço em faixa só de música). A conclusão de "sem fala" vem da folha de quadros.

## Pergunta 2: como mostram produto, torra, origem e fogo?

### Takeaway
**Nenhum dos 18 vídeos mostra torra.** Ninguém mostra torrador, chama, fumaça ou curva de torra. A torra só aparece em texto: "so strong" na fala da Onyx, "roast profile" na legenda da Blue Bottle. A origem quase não aparece (um plano de lavoura no vídeo da Proud Mary; produtores presentes no recap da SEY). O único fogo é **de cozinha, num vídeo de comida** (maçarico nos calçots da Nomad), com conotação de sabor. A estratégia comum é mostrar o café **pronto, no gesto de alguém**: coado em macro, moka numa xícara de 1970, cápsula na mão.

### Cited Findings
- Coado em close como ritual da protagonista, pacote uma vez entre livros — [La Cabra Rituals Paris](https://www.instagram.com/reel/C017i9wN2O_/)
- Moka servida em xícara de vidro âmbar de 1970; a marca não fala de si — [Nomad Cristal Antiguo](https://www.instagram.com/reel/DZ5Q5B9inoj/)
- Grão e extração em foto P&B com um fio azul de papel animado no lugar do espresso; "roast profile" só na legenda — [Blue Bottle jazz](https://www.instagram.com/reel/DdWpu4yMpxk/)
- Maçarico queimando os calçots ("Torna el foc" na legenda); fogo como técnica de cozinha — [Nomad × Blancooks](https://www.instagram.com/reel/DV8gTwyDK9W/)
- Força do café comunicada por bordão de luta ("You can smell it through the box. It's so strong") — [Onyx Morning Mayhem](https://www.instagram.com/reel/DcT14-qx6pM/)
- Lavoura com produtor num plano de ~1 s dentro do vídeo de campeonato — [Proud Mary campeão](https://www.instagram.com/reel/Da1SakEtUHD/)

### Inferences
- A chama gráfica sobre o torrador no vídeo da Canastra não tem paralelo nas marcas de referência e, pelo que se vê aqui, lê como "queimado". Quando o fogo aparece, é real e pertence a uma técnica que o público reconhece como cuidado (cozinha). Se a Canastra quiser mostrar torra, o caminho coerente com estas marcas é **som e matéria reais**: o grão caindo no resfriador, a cor do grão mudando em close, o torrador mexendo, de preferência na voz do torrador, sem grafismo de chama.
- "Origem" nestas contas é transmitida por **pessoas** (produtores no evento, protagonistas com herança), não por explicação botânica. "Esse café já foi uma fruta" é o tipo de conteúdo explicativo que nenhuma das 6 torrefações tem entre os tops.

### Gaps
- Não analisei Reels de viagem a origem (eles existem nas grades da Proud Mary e da Onyx), porque não estavam entre os mais vistos. Isso já é um dado: na amostra, conteúdo de origem não chegou ao topo.

## Pergunta 3: humor, voz, texto na tela e duração

### Takeaway
O humor que funciona está **ligado ao produto ou ao nome do produto**: gato preto + Black Cat Frappuccino, blend "Morning Mayhem" + paródia de luta, PSL + autoironia "basic", campeão de barista + "coffee shenanigans". Todas as vozes são **humanas e de quem aparece** (protagonista, campeão, celebridade, artistas). **Nenhum vídeo usa narrador de IA nem locutor genérico.** Os sem voz usam só música e cartelas curtas, quebradas em 2–3 linhas. A duração mediana dos tops é ~32 s; o mais visto de todos tem 6 s.

### Cited Findings
- Piada de 6 s que só existe por causa do produto (gato preto derruba o Black Cat Frappuccino), frase única em off "Arthur, please don't do that. You know why." — [Starbucks](https://www.instagram.com/reel/DdRM4oglV5o/), 14,6 mi views, 814 mil curtidas
- Autoironia: "The drink that makes us all a little more basic?" + piada do canudo em bebida quente — [Starbucks PSL](https://www.instagram.com/reel/DcbH1Lhtiy0/), 11,1 mi
- Paródia de luta livre com look VHS e legenda em fonte pixelada; o blend tem nome de luta — [Onyx](https://www.instagram.com/reel/DcT14-qx6pM/), 142 comentários (os outros tops da conta têm 4 e 52)
- Legenda karaokê grande, palavra destacada em azul; olho roxo nunca explicado; promessa de série — [Proud Mary](https://www.instagram.com/reel/Da1SakEtUHD/)
- Texto como cartela quebrada em vez de narração: "CRAFTED / WITH / PRECISION." — [Blue Bottle jazz](https://www.instagram.com/reel/DdWpu4yMpxk/); "Click, / Sip, / Repeat Often" — [BB × Nespresso](https://www.instagram.com/reel/DKwzk3ztsKq/)
- Voz própria da protagonista, em inglês ou coreano, com legenda pequena — [La Cabra Paris](https://www.instagram.com/reel/C017i9wN2O_/), [La Cabra Seul](https://www.instagram.com/reel/DSmaaz3DWOX/); em espanhol — [Nomad](https://www.instagram.com/reel/DZ5Q5B9inoj/)
- Durações dos 18: 6, 16, 16, 21, 23, 24, 28, 30, 30, 33, 38, 60, 64, 65, 66, 82, 97, 122 s (o de 122 s é um trecho de 61 s duplicado) — arquivos por vídeo acima

### Inferences
- Comparado ao Reel rejeitado do Café Canastra (59 s, voz feminina de IA, colagem gerada, piada do frango de padaria, chama sobre o torrador), **cada um desses elementos aparece com sinal contrário nos tops**. A voz é humana. A colagem, quando existe (Blue Bottle jazz), usa foto real com uma intervenção gráfica de marca e dura 16 s. A piada sai do produto. Fogo, só na comida.
- Duas fórmulas de narrativa parecem replicáveis para a Canastra com o que ela já tem: (a) **minidoc de uma pessoa real na voz própria** (Nomad/La Cabra), com o produtor ou o torrador falando da herança da fazenda a 1.250 m; (b) **gag curta ligada ao produto** (Starbucks/Onyx), com um blend ou um costume mineiro como gatilho da piada.
- Se o motion de colagem continuar, o modelo é o [Blue Bottle jazz](https://www.instagram.com/reel/DdWpu4yMpxk/): até ~16 s, foto real (P&B ou lavada), **uma cor da marca** animada em textura de papel, uma frase em duas metades e nenhuma narração.

### Gaps
- Não tenho dado de retenção (tempo médio assistido) de nenhum vídeo; os diagnósticos se baseiam em views, curtidas e comentários públicos.
- A Starbucks tem orçamento de celebridade e mídia, o que não se transfere. O que se transfere é a estrutura (uma ideia, ligada ao produto, em menos de 30 s).

## Notas de execução (para reprodutibilidade)
- Arquivos locais de cada vídeo (mp4, folhas `_hook.jpg`/`_all.jpg`, `.srt`, `.meta`): `C:/Users/rafae/AppData/Local/Temp/claude/C--Users-rafae-OneDrive-Desktop-Canastra-Inteligencia-Agentes-AI-Canastra-Content-Creator/87ea359a-6b51-47aa-83bf-1d929f3af7da/scratchpad/watch-marcas/`. A mídia de terceiros não foi copiada para o repositório.
- A data de cada Reel foi decodificada do shortcode (`(id >> 23) + 1314220021721` ms) e bate com a `upload_date` do yt-dlp em todos os casos conferidos.
- O whisper rodou um vídeo por vez, com `-t 4` e greedy (`-bs 1 -bo 1`), prioridade AboveNormal e limite de 240 s. Com a CPU saturada por outros processos, o beam padrão não terminava nem um clipe de 6 s.
