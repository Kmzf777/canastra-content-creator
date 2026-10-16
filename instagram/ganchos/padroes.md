# Padrões de gancho

> Gerado por `python scripts/ganchos.py padroes`. **Não edite à mão**: mude `padroes-mapa.json` ou as fichas e rode de novo.

Corpus: 128 ganchos das fichas de `instagram/referencias-virais/` — **só Reel e só vencedores**. Os números dizem o que os virais têm em comum, não o que separa viral de fracasso (para isso, `python scripts/ganchos.py contrastar`). Views lidas da grade podem incluir mídia paga. O agrupamento é julgamento **[leitura minha]**; as contagens sobre ele são **[medido]**.

## Padrões

`perfis` = quantos criadores diferentes usam o padrão; `dominante` = o criador com mais casos e a fatia dele. Padrão em que um perfil sozinho tem metade ou mais dos casos é estilo de um criador, não padrão, e não conta em J6. A mediana "sem susp." tira os suspeitos de impulsionamento (seção abaixo); os dois números ficam lado a lado.

| Padrão | Forma | n | perfis | dominante | n café | Mediana de views (todos · sem susp. · café) | Exemplos, maior view primeiro |
|---|---|---:|---:|---|---:|---|---|
| **Um objeto fora do lugar** (`objeto-impossivel`) | cenário banal + uma única coisa que não devia estar ali | 25 | 24 | @origiful 8% | 5 | 794 mil · 892 mil · 281 mil | @origiful 101,0 mi: “(sem texto) plataforma de metrô de Tóquio, linha amarela tátil, funcionário de uniforme de”<br>@guaranaantarctica 46,7 mi ⚑: “(sem texto) prato branco vazio sobre tábua de madeira, parede verde-musgo ao fundo. Em 0,0”<br>@origiful 17,9 mi: “(sem texto) a parede do MoMA com as latas Campbell de Warhol. Em ~0,7 s a primeira lata "e” |
| **Situação que a pessoa reconhece** (`situacao-reconhecivel`) | 'quando você…' / cena de vida real que o público já viveu | 22 | 17 | @amandabaristaa 18% | 12 | 1,6 mi · 1,6 mi · 3,8 mi | @kassianethaynaoficial_ 32,3 mi: “Quando é dia de Panhar café na paranbeira eu o dia todo 😂 Hoje é dia de panhar café na pir”<br>@starbucks 14,6 mi: “Arthur, please don't do that.”<br>@amandabaristaa 11,1 mi: “tão linda, qual será que vai ser sua primeira palavra?” |
| **Ação já em curso** (`acao-em-curso`) | abre no meio do trabalho, com a matéria mudando na frente da câmera | 19 | 19 | @vovo_faztudo 5% | 11 | 1,8 mi · 1,4 mi · 2,3 mi | @jesus_eliaselcampesino_c.a 30,0 mi ⚑: “(sem texto) plano geral de baixo, dentro do pé de café: galhos carregados de cereja vermel”<br>@alexgrimadesign 14,4 mi: “(sem texto) chef de boné virando a carne numa frigideira de ferro sob soft box gigante; co”<br>@mistar.coffeedampit 11,2 mi ⚑: “(sem texto) de cima, um tambor azul de 200 L sendo inclinado sobre uma bacia com cesto ver” |
| **Clima de marca, sem gancho** (`marca-clima`) | atmosfera, slogan ou packshot sem pergunta nem contraste | 17 | 11 | @lacabracoffee 18% | 11 | 200 mil · 100 mil · 113 mil | @liquiddeath 53,3 mi ⚑: “NEW”<br>@cafepilao 40,1 mi ⚑: “ENQUANTO A VIDA ACONTECE, PILÃO TE ACOMPANHA”<br>@guaranaantarctica 39,8 mi ⚑: “não importa se você prefere” |
| **Quem faz, mostrando** (`quem-faz-mostra`) | 'Essa aqui é a…' / 'Hoje eu vou…' dito por quem trabalha naquilo | 12 | 11 | @felipebrazza 17% | 10 | 1,4 mi · 2,3 mi · 2,3 mi | @cafegeracoes 13,1 mi: “Escolhendo café no supermercado As duas informações mais importantes que eu trago aqui sem”<br>@kevin_miranda_agro 7,2 mi: “Hoje eu vou tirar o boia desse café, galera.”<br>@sprometheus 5,2 mi: “IF YOU'RE a fan of milk in your coffee, you've gotta try THIS If you're a fan of milk in y” |
| **Resultado antes do processo** (`resultado-antes`) | mostra o fim primeiro (o produto pronto, o antes e depois) e depois volta | 10 | 6 | @tannercolsoncoffee 40% | 6 | 4,1 mi · 3,0 mi · 5,3 mi | @tannercolsoncoffee 16,5 mi: “(sem texto) 0–0,7 s: um flash do FIM do processo — galão de fermentação cheio de cerejas v”<br>@tannercolsoncoffee 9,3 mi: “3 Most Interesting Coffee Brewers”<br>@apple 8,8 mi ⚑: “(sem texto) a tela dividida ao meio. Em cima, um set em miniatura de piso xadrez verde-águ” |
| **Veredito que contraria** (`veredito-direto`) | uma afirmação curta que contraria o que a pessoa acha (com a prova à vista) | 9 | 9 | @umcoffeeco 11% | 6 | 358 mil · 331 mil · 2,1 mi | @terracruzcafes 8,6 mi: “AMBOS SÃO O Ambos são o mesmo café.”<br>@cafegeracoes 5,5 mi: “Não é CHAFÉ! Esses dois cafés foram produzidos aqui na roça.”<br>@morgandrinkscoffee 2,1 mi ⚑: “Coffee is 98.5% water Coffee is 98.5% water.” |
| **Pergunta que a pessoa já se fez** (`pergunta-diagnostico`) | uma pergunta concreta, de uso, que a pessoa já tentou responder sozinha | 8 | 8 | @tulianelenk 12% | 6 | 1,6 mi · 1,6 mi · 2,0 mi | @ana.paula.rodrigues018 25,1 mi: “Quanto eu ganhei em uma semana trabalhando com o ano do café [na apanha de café]”<br>@tulianelenk 21,1 mi: “Como separar o café De qualidade do café inferior 🤫 Como separar o café inferior de um caf”<br>@morgandrinkscoffee 2,0 mi: “What would happen if you brewed your coffee with milk instead of water? What would happen ” |
| **Resposta a um ataque ou prejuízo** (`conflito-resposta`) | responder a comentário / contar o que esteve em jogo, com o valor | 6 | 3 | @nacaradi 50% | 3 | 986 mil · 986 mil · 1,4 mi | @isabela.raposeiras 2,4 mi: “Eu vou votar nessas eleições pelas pessoas que continuam invisíveis no nosso dia a dia Olh”<br>@kassianethaynaoficial_ 1,4 mi: “Eu vou responder ao comentário…”<br>@nacaradi 1,2 mi: “QUASE TOMEI UM PREJUÍZO DE Esse foi o dia que eu tive que virar noite pra fazer um vídeo d” |

⚑ = suspeito de impulsionamento.

## Fórmulas de lacuna (mad-lib), por padrão

Cada fórmula sai de um vencedor do próprio padrão: o original, as views e a fórmula com as lacunas entre colchetes. Use no Modo 1 da skill, **depois** do filtro de compatibilidade (estrutura, tom, lido em voz alta). Lacuna de número só se preenche com número medido (P1).

### Situação que a pessoa reconhece (`situacao-reconhecivel`)

- **@kassianethaynaoficial_**, 32,3 mi
  Original: “Hoje é dia de panhar café na pirambeira!”
  Fórmula: Hoje é dia de [tarefa dura e conhecida] [no lugar difícil, com a palavra local].

- **@mycoffee.io**, 3,0 mi
  Original: “Eu quando passo o dia sem encostar no café”
  Fórmula: Eu quando [situação de rotina que todo mundo já viveu com café].

- **@starbucks**, 11,1 mi ⚑
  Original: “Oh, pumpkin spice latte?”
  Fórmula: [O nome da bebida/do hábito], [repetido com o tom de quem acha graça dele]?

### Ação já em curso (`acao-em-curso`)

- **@jesus_eliaselcampesino_c.a**, 30,0 mi ⚑
  Original: “(sem texto: plano de baixo, dentro do pé de café, o apanhador colhendo)”
  Fórmula: Frame 1 = [mão ou ferramenta] já [fazendo a tarefa] em [matéria que muda de estado]. Tela, se houver: [o nome da tarefa, em até 4 palavras].

- **@karstorganics**, 8,1 mi
  Original: “(sem texto: tremonha de cerejas vermelhas soltando grãos brancos)”
  Fórmula: Frame 1 = [a matéria entrando] e, no mesmo plano, [a matéria saindo transformada]. Sem fala no primeiro segundo.

### Quem faz, mostrando (`quem-faz-mostra`)

- **@_gabriel_dcafe**, 4,0 mi
  Original: “Essa aqui é a via úmida do café.”
  Fórmula: Essa aqui é [a etapa/o lugar], [dito por quem trabalha nela, com o termo traduzido em seguida].

- **@kevin_miranda_agro**, 7,2 mi
  Original: “Hoje eu vou tirar o boia desse café, galera.”
  Fórmula: Hoje [eu/a gente] vai [tarefa concreta, com a palavra da roça] [desse/nesse] [objeto na tela].

- **@cafegeracoes**, 13,1 mi
  Original: “As duas informações mais importantes que eu trago aqui sempre são…”
  Fórmula: As [número contado] [coisas] que [eu/a gente] [olha/confere] sempre [no lugar de escolha] são…

### Resultado antes do processo (`resultado-antes`)

- **@tannercolsoncoffee**, 9,3 mi
  Original: “3 Most Interesting Coffee Brewers”
  Fórmula: [Número contado] [coisas] mais [adjetivo verificável] [da categoria], com o resultado de cada uma já na tela.

- **@morgandrinkscoffee**, 1,4 mi
  Original: “The humble mocha is one of my favorite coffee drinks”
  Fórmula: [O produto pronto, na mão] é [o que ele é para quem fala]. Depois volta para como chegou nisso.

- **@brazumotion**, 39 mil
  Original: “Eu fiz esse projeto usando só Photoshop e After Effects”
  Fórmula: [A gente] fez [isso, mostrado pronto] usando só [o recurso simples].

### Veredito que contraria (`veredito-direto`)

- **@terracruzcafes**, 8,6 mi
  Original: “Ambos são o mesmo café.”
  Fórmula: [Os dois / Esses dois] [objetos que parecem diferentes, na tela] são o mesmo [coisa].

- **@cafegeracoes**, 5,5 mi
  Original: “Não é CHAFÉ! Esses dois cafés foram produzidos aqui na roça.”
  Fórmula: Não é [o rótulo que a pessoa usa para julgar]. [Prova de origem, de quem fala, no lugar].

- **@morgandrinkscoffee**, 2,1 mi ⚑
  Original: “Coffee is 98.5% water.”
  Fórmula: [Coisa conhecida] é [número medido que surpreende] [unidade].

### Pergunta que a pessoa já se fez (`pergunta-diagnostico`)

- **@tulianelenk**, 21,1 mi
  Original: “Como separar o café de qualidade do café inferior?”
  Fórmula: Como separar [a coisa boa] [da coisa ruim] [no lugar onde a pessoa escolhe]?

- **@ana.paula.rodrigues018**, 25,1 mi
  Original: “Quanto eu ganhei em uma semana trabalhando na apanha de café”
  Fórmula: Quanto [eu/a gente] [ganhei/gastei/levei] em [período] [fazendo a tarefa real].

- **@morgandrinkscoffee**, 2,0 mi
  Original: “What would happen if you brewed your coffee with milk instead of water?”
  Fórmula: O que acontece se você [fizer o gesto de sempre] com [um ingrediente trocado]?

### Resposta a um ataque ou prejuízo (`conflito-resposta`)

- **@kassianethaynaoficial_**, 1,4 mi
  Original: “Eu vou responder ao comentário…”
  Fórmula: [A gente] vai responder [o comentário real, na tela].

- **@nacaradi**, 1,2 mi
  Original: “Quase tomei um prejuízo de R$ …”
  Fórmula: Quase [perdemos/estragamos] [valor ou lote medido] [por causa do risco real].

## Suspeitos de impulsionamento (sinalizados, não excluídos)

Critério: ficha marcada `provavel-pago`, ou curtidas/views abaixo de 0.33 × a mediana do corpus (3.29% → corte em 1.10%). O fator é **[leitura minha]**; o Hook Machine usa 2% fixo, que aqui não serve porque a razão varia com nicho e formato. Fichas sem views lidas não entram na conta da razão.

| Perfil | Views | Curtidas/views | `organico` na ficha | Padrão |
|---|---:|---:|---|---|
| @liquiddeath | 53,3 mi | 0.00% | provavel-pago | `marca-clima` |
| @guaranaantarctica | 46,7 mi | 0.00% | provavel-pago | `objeto-impossivel` |
| @cafepilao | 40,1 mi | 0.01% | provavel-pago | `marca-clima` |
| @guaranaantarctica | 39,8 mi | 0.00% | provavel-pago | `marca-clima` |
| @jesus_eliaselcampesino_c.a | 30,0 mi | 0.82% | sim | `acao-em-curso` |
| @mistar.coffeedampit | 11,2 mi | 0.30% | incerto | `acao-em-curso` |
| @starbucks | 11,1 mi | 3.02% | provavel-pago | `situacao-reconhecivel` |
| @ailliothailand | 9,6 mi | 0.64% | incerto | `acao-em-curso` |
| @apple | 8,8 mi | 0.53% | collab | `resultado-antes` |
| @cacaushow | 2,2 mi | 0.94% | incerto | `acao-em-curso` |
| @morgandrinkscoffee | 2,1 mi | 0.71% | provavel-pago | `veredito-direto` |
| @magazineluiza | 973 mil | 0.81% | provavel-pago | `objeto-impossivel` |
| @ben_marriott_ | 931 mil | 0.93% | provavel-pago | `quem-faz-mostra` |
| @filmaenzo | 551 mil | 1.87% | provavel-pago | `objeto-impossivel` |
| @orfeucafes | 534 mil | 1.04% | collab | `marca-clima` |
| @orfeucafes | 492 mil | 0.25% | provavel-pago | `marca-clima` |
| @_victorzk | 305 mil | 1.40% | provavel-pago | `quem-faz-mostra` |
| @_victorzk | 232 mil | 2.13% | provavel-pago | `situacao-reconhecivel` |
| @bluebottle | 200 mil | 1.06% | collab | `marca-clima` |
| @airbnb | 150 mil | 1.07% | provavel-pago | `acao-em-curso` |
| @lure3d | 109 mil | 1.06% | provavel-pago | `objeto-impossivel` |
| @duncanimate | 107 mil | 6.30% | provavel-pago | `objeto-impossivel` |
| @futureproofcreative | — | — | provavel-pago | `acao-em-curso` |
| @keenanlam | — | — | provavel-pago | `situacao-reconhecivel` |
| @keetadobrasil | — | — | provavel-pago | `objeto-impossivel` |
| @hard_cuore | — | — | provavel-pago | `objeto-impossivel` |

## Medidas do corpus **[medido]**

Abertura = 1ª tela citada entre aspas + 1ª frase falada. Texto sem aspas na ficha é descrição e não conta.

| Recorte | n | palavras na tela (mediana · p25–p75) | palavras na 1ª frase falada (idem) | pergunta | número | você | negação no início | sem texto |
|---|---:|---|---|---:|---:|---:|---:|---:|
| todos | 128 | 4 · 2.0–7.0 | 8 · 5.0–13.0 | 10.9% | 6.2% | 11.7% | 2.3% | 35.2% |
| pt | 51 | 5.5 · 2.0–9.25 | 8.5 · 5.25–12.75 | 13.7% | 11.8% | 11.8% | 5.9% | 21.6% |
| en | 60 | 4 · 1.5–6.5 | 7 · 4.0–14.5 | 11.7% | 3.3% | 15.0% | 0.0% | 35.0% |
| top25 | 30 | 6.0 · 3.75–9.25 | 8 · 5.0–10.0 | 10.0% | 6.7% | 13.3% | 6.7% | 40.0% |
| resto75 | 90 | 3 · 1.5–7.0 | 9.0 · 4.0–14.25 | 11.1% | 6.7% | 11.1% | 0.0% | 30.0% |

## Vícios de IA no corpus (ganchos em que aparecem)

Definições em `.claude/skills/canastra-ganchos/vicios-ia.md`.

| id | todos | pt | en | top25 | resto75 |
|---|---:|---:|---:|---:|---:|
| V1 | 0 | 0 | 0 | 0 | 0 |
| V2 | 0 | 0 | 0 | 0 | 0 |
| V3 | 1 | 1 | 0 | 0 | 1 |
| V4 | 1 | 1 | 0 | 0 | 1 |
| V5 | 0 | 0 | 0 | 0 | 0 |
| V6 | 0 | 0 | 0 | 0 | 0 |
| V7 | 0 | 0 | 0 | 0 | 0 |
| V8 | 0 | 0 | 0 | 0 | 0 |
| V9 | 1 | 1 | 0 | 1 | 0 |
| V10 | 0 | 0 | 0 | 0 | 0 |
| V11 | 0 | 0 | 0 | 0 | 0 |
| V12 | 0 | 0 | 0 | 0 | 0 |
| V13 | 2 | 2 | 0 | 1 | 1 |
| V14 | 4 | 4 | 0 | 3 | 0 |
| V15 | 3 | 2 | 1 | 0 | 3 |
| V16 | 1 | 1 | 0 | 0 | 1 |
