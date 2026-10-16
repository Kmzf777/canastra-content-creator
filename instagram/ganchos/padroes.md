# Padrões de gancho

> Gerado por `python scripts/ganchos.py padroes`. **Não edite à mão**: mude `padroes-mapa.json` ou as fichas e rode de novo.

Corpus: 128 ganchos das fichas de `instagram/referencias-virais/` — **só Reel e só vencedores**. Os números dizem o que os virais têm em comum, não o que separa viral de fracasso. Views lidas da grade podem incluir mídia paga (campo `organico` da ficha). O agrupamento é julgamento **[leitura minha]**; as contagens sobre ele são **[medido]**.

## Padrões

| Padrão | Forma | n | n café | n pt | Mediana de views (todos · café) | Exemplos, maior view primeiro |
|---|---|---:|---:|---:|---|---|
| **Um objeto fora do lugar** (`objeto-impossivel`) | cenário banal + uma única coisa que não devia estar ali | 25 | 5 | 8 | 794 mil · 281 mil | @origiful 101,0 mi: “(sem texto) plataforma de metrô de Tóquio, linha amarela tátil, funcionário de uniforme de”<br>@guaranaantarctica 46,7 mi: “(sem texto) prato branco vazio sobre tábua de madeira, parede verde-musgo ao fundo. Em 0,0”<br>@origiful 17,9 mi: “(sem texto) a parede do MoMA com as latas Campbell de Warhol. Em ~0,7 s a primeira lata "e” |
| **Situação que a pessoa reconhece** (`situacao-reconhecivel`) | 'quando você…' / cena de vida real que o público já viveu | 22 | 12 | 10 | 1,6 mi · 3,8 mi | @kassianethaynaoficial_ 32,3 mi: “Quando é dia de Panhar café na paranbeira eu o dia todo 😂 Hoje é dia de panhar café na pir”<br>@starbucks 14,6 mi: “Arthur, please don't do that.”<br>@amandabaristaa 11,1 mi: “tão linda, qual será que vai ser sua primeira palavra?” |
| **Ação já em curso** (`acao-em-curso`) | abre no meio do trabalho, com a matéria mudando na frente da câmera | 19 | 11 | 4 | 1,8 mi · 2,3 mi | @jesus_eliaselcampesino_c.a 30,0 mi: “(sem texto) plano geral de baixo, dentro do pé de café: galhos carregados de cereja vermel”<br>@alexgrimadesign 14,4 mi: “(sem texto) chef de boné virando a carne numa frigideira de ferro sob soft box gigante; co”<br>@mistar.coffeedampit 11,2 mi: “(sem texto) de cima, um tambor azul de 200 L sendo inclinado sobre uma bacia com cesto ver” |
| **Clima de marca, sem gancho** (`marca-clima`) | atmosfera, slogan ou packshot sem pergunta nem contraste | 17 | 11 | 4 | 200 mil · 113 mil | @liquiddeath 53,3 mi: “NEW”<br>@cafepilao 40,1 mi: “ENQUANTO A VIDA ACONTECE, PILÃO TE ACOMPANHA”<br>@guaranaantarctica 39,8 mi: “não importa se você prefere” |
| **Quem faz, mostrando** (`quem-faz-mostra`) | 'Essa aqui é a…' / 'Hoje eu vou…' dito por quem trabalha naquilo | 12 | 10 | 6 | 1,4 mi · 2,3 mi | @cafegeracoes 13,1 mi: “Escolhendo café no supermercado As duas informações mais importantes que eu trago aqui sem”<br>@kevin_miranda_agro 7,2 mi: “Hoje eu vou tirar o boia desse café, galera.”<br>@sprometheus 5,2 mi: “IF YOU'RE a fan of milk in your coffee, you've gotta try THIS If you're a fan of milk in y” |
| **Resultado antes do processo** (`resultado-antes`) | mostra o fim primeiro (o produto pronto, o antes e depois) e depois volta | 10 | 6 | 3 | 4,1 mi · 5,3 mi | @tannercolsoncoffee 16,5 mi: “(sem texto) 0–0,7 s: um flash do FIM do processo — galão de fermentação cheio de cerejas v”<br>@tannercolsoncoffee 9,3 mi: “3 Most Interesting Coffee Brewers”<br>@apple 8,8 mi: “(sem texto) a tela dividida ao meio. Em cima, um set em miniatura de piso xadrez verde-águ” |
| **Veredito que contraria** (`veredito-direto`) | uma afirmação curta que contraria o que a pessoa acha (com a prova à vista) | 9 | 6 | 5 | 358 mil · 2,1 mi | @terracruzcafes 8,6 mi: “AMBOS SÃO O Ambos são o mesmo café.”<br>@cafegeracoes 5,5 mi: “Não é CHAFÉ! Esses dois cafés foram produzidos aqui na roça.”<br>@morgandrinkscoffee 2,1 mi: “Coffee is 98.5% water Coffee is 98.5% water.” |
| **Pergunta que a pessoa já se fez** (`pergunta-diagnostico`) | uma pergunta concreta, de uso, que a pessoa já tentou responder sozinha | 8 | 6 | 5 | 1,6 mi · 2,0 mi | @ana.paula.rodrigues018 25,1 mi: “Quanto eu ganhei em uma semana trabalhando com o ano do café [na apanha de café]”<br>@tulianelenk 21,1 mi: “Como separar o café De qualidade do café inferior 🤫 Como separar o café inferior de um caf”<br>@morgandrinkscoffee 2,0 mi: “What would happen if you brewed your coffee with milk instead of water? What would happen ” |
| **Resposta a um ataque ou prejuízo** (`conflito-resposta`) | responder a comentário / contar o que esteve em jogo, com o valor | 6 | 3 | 6 | 986 mil · 1,4 mi | @isabela.raposeiras 2,4 mi: “Eu vou votar nessas eleições pelas pessoas que continuam invisíveis no nosso dia a dia Olh”<br>@kassianethaynaoficial_ 1,4 mi: “Eu vou responder ao comentário…”<br>@nacaradi 1,2 mi: “QUASE TOMEI UM PREJUÍZO DE Esse foi o dia que eu tive que virar noite pra fazer um vídeo d” |

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
