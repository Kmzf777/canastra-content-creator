# Reels virais de criadores e marcas brasileiras de café — análise quadro a quadro

Método: Instagram aberto no Chrome logado (grade `/<perfil>/reels/`, contagem de views lida no DOM em 11/10/2026), download com yt-dlp para a scratchpad, análise local: contagem de cortes (`ffmpeg select gt(scene,0.25)`), folhas de quadros com carimbo de tempo (gancho 0–6 s a 4 fps + vídeo inteiro em 24 quadros), transcrição local (whisper.cpp small e, depois que a máquina saturou, faster-whisper base; sempre em pt). Nenhum upload, nenhuma interação nas contas. Mídia de terceiros só na scratchpad.

**19 Reels analisados**, 8 contas. Arquivo completo de cada vídeo (ficha, gancho, transcrição com tempo, lista de cortes, tabela plano a plano, roteiro, diagnóstico) em `videos/brasil/`.

### Índice dos arquivos por vídeo

| Conta | Reel | Views (grade) | Assunto | Arquivo |
|---|---|---:|---|---|
| @kassianethaynaoficial_ | C8XugrWh_-n | 32,3 mi | colheita na pirambeira, tombo | [kassianethaynaoficial__C8XugrWh_-n.md](../videos/brasil/kassianethaynaoficial__C8XugrWh_-n.md) |
| @cafegeracoes | CqGC2e7g5nf | 13,1 mi | escolher café no supermercado (classificação ABIC, torra) | [cafegeracoes_CqGC2e7g5nf.md](../videos/brasil/cafegeracoes_CqGC2e7g5nf.md) |
| @amandabaristaa | DCFZKnnsMjx | 11,1 mi | família (primeira palavra) — fora do café | [amandabaristaa_DCFZKnnsMjx.md](../videos/brasil/amandabaristaa_DCFZKnnsMjx.md) |
| @amandabaristaa | C_AvrBuxgMj | 10,1 mi | família (rotina 'aesthetic' do bebê) — fora do café | [amandabaristaa_C_AvrBuxgMj.md](../videos/brasil/amandabaristaa_C_AvrBuxgMj.md) |
| @cafegeracoes | DVobHGpAW2Y | 5,5 mi | "Não é CHAFÉ!" — torra média × torra escura, na lavoura | [cafegeracoes_DVobHGpAW2Y.md](../videos/brasil/cafegeracoes_DVobHGpAW2Y.md) |
| @kassianethaynaoficial_ | DK0HqC5S_Hm | 5,2 mi | lançamento da própria marca de café, chorando no carro | [kassianethaynaoficial__DK0HqC5S_Hm.md](../videos/brasil/kassianethaynaoficial__DK0HqC5S_Hm.md) |
| @amandabaristaa | C4eJrrkLMPJ | 4,5 mi | família (irmãos) — fora do café | [amandabaristaa_C4eJrrkLMPJ.md](../videos/brasil/amandabaristaa_C4eJrrkLMPJ.md) |
| @isabela.raposeiras | Dd9M1ytxbDO | 2,4 mi | política (eleição) — fora do café | [isabela.raposeiras_Dd9M1ytxbDO.md](../videos/brasil/isabela.raposeiras_Dd9M1ytxbDO.md) |
| @felipebrazza | C0r_Lc9O851 | 1,7 mi | "Mitos e verdades sobre o café" | [felipebrazza_C0r_Lc9O851.md](../videos/brasil/felipebrazza_C0r_Lc9O851.md) |
| @felipebrazza | C6UA4X9r-4N | 1,6 mi | "Gambiarras do café" | [felipebrazza_C6UA4X9r-4N.md](../videos/brasil/felipebrazza_C6UA4X9r-4N.md) |
| @felipebrazza | DFf3isuuhcS | 1 mi | café do pé à xícara (série "porteira pra dentro") | [felipebrazza_DFf3isuuhcS.md](../videos/brasil/felipebrazza_DFf3isuuhcS.md) |
| @kassianethaynaoficial_ | DeHjlCAoQc1 | 771 mil | resposta a comentário "trabalhadora que se acha rica" | [kassianethaynaoficial__DeHjlCAoQc1.md](../videos/brasil/kassianethaynaoficial__DeHjlCAoQc1.md) |
| @isabela.raposeiras (collab @coffeelab) | DeR5EiZvusW | 645 mil | placa "0 dias sem sermos destratados por clientes" | [isabela.raposeiras_DeR5EiZvusW.md](../videos/brasil/isabela.raposeiras_DeR5EiZvusW.md) |
| @orfeucafes (collab) | DaiGLxiR0Ko | 534 mil | bandeja de café, lifestyle de estúdio | [orfeucafes_DaiGLxiR0Ko.md](../videos/brasil/orfeucafes_DaiGLxiR0Ko.md) |
| @orfeucafes | DcCB9dQhKYn | 492 mil | anúncio de Drip Coffee | [orfeucafes_DcCB9dQhKYn.md](../videos/brasil/orfeucafes_DcCB9dQhKYn.md) |
| @amandabaristaa | DeLLLxpNbtP | 351 mil | família (meme "instinto materno") — fora do café | [amandabaristaa_DeLLLxpNbtP.md](../videos/brasil/amandabaristaa_DeLLLxpNbtP.md) |
| @umcoffeeco (collab THOMY) | DVjjyTpDk65 | 50,4 mil | "café perfeito" com criador estrangeiro | [umcoffeeco_DVjjyTpDk65.md](../videos/brasil/umcoffeeco_DVjjyTpDk65.md) |
| @cafegeracoes | DARbgCGyf5H | não visível na grade; 299 mil curtidas | criança (Helena) ensinando a escolher café no mercado | [cafegeracoes_DARbgCGyf5H.md](../videos/brasil/cafegeracoes_DARbgCGyf5H.md) |
| @_noudaniel | DVMF38UgD0M | não lida; 122 mil curtidas | "Não compre café ruim nunca mais" (supermercado) | [_noudaniel_DVMF38UgD0M.md](../videos/brasil/_noudaniel_DVMF38UgD0M.md) |

### Tabela-resumo por vídeo

| Reel | Dur. | Cortes/10 s | Gancho 0–3 s (vê / escrito / dito) | Quem aparece | Formato | Tom | Torra | CTA |
|---|---:|---:|---|---|---|---|---|---|
| Kassiane C8X | 39 s | 1,0 | tombo no barranco / "Quando é dia de panhar café na pirambeira eu o dia todo 😂" / "Hoje é dia de panhar café na pirambeira!" | a produtora | b-roll de trabalho + selfie | humor de roça | — | nenhum |
| Gerações CqGC | 84 s | 0,6 (selfie contínua) | selfie na gôndola / "Escolhendo café no supermercado" / "as duas informações mais importantes…" | o produtor-torrefador | talking head + close de pacote | educativo, desmistificação | torra escura "mascara baixa qualidade"; procure torra média | seguir perfil |
| Gerações DVob | 41 s | 2,2 | produtora no cafezal com 2 canecas clara×escura / "Não é CHAFÉ!" / "Esses dois cafés foram produzidos aqui na roça" | produtora da família | talking head na lavoura + close | myth-busting | "não é fraco, é torra média"; "torra escura corrige baixa qualidade"; "açúcar como legítima defesa" | — |
| Gerações DARb | 84 s | 1,3 | menina na gôndola / "ESCOLHE CAFÉ NO SUPERMERCADO" / "Filha, como é que escolhe café no supermercado?" | criança + pai fora de quadro | entrevista na gôndola | educativo fofo | extraforte = classificação de baixo; torra média "não amarga" | "siga o perfil do Café Gerações" |
| Nou DVMF | 171 s | ~0 (contínuo, legenda palavra a palavra) | dois pacotes populares / "🔴 Não compre café ruim pra sua casa nunca mais" / idem | criador | talking head na gôndola | alerta, preço/valor | extraforte "aparece o carvão"; especial "parece ralo mas tem sabor" | — |
| Brazza C0r | 52 s | 3,1 (≈4 visual) | servindo sob árvore / "MITOS E VERDADES SOBRE O CAFÉ" / "Se ferveu a água, vai queimar o café? — Isso é mito" | ele, em 2 papéis | lista de mitos, 1 cenário por item | educativo + humor | "água fervendo queima o café" = mito; "extraforte, claro" = piada | "manda pra aquela pessoa que faz aquele café razoável" + marca |
| Brazza C6U | 48 s | 7,8 | pote laranja / "gambiarras do café" / "sem moedor? um mixer…" | ele | lista de dicas, cortes de 1 s | humor útil | — | "manda pra aquela pessoa gambiarreira" |
| Brazza DFf | 58 s | 8,5 | balcão / "hoje nós vamos fazer café do zero" / "do pé à xícara" | ele | processo da fazenda à xícara | educativo, origem | torra = "ressaltar as características" | "manda pra aquela pessoa que nem gosta de café" |
| Kassiane DK0 | 158 s | 0,1 | pacote na mão no carro / — / "consegui a minha marca de café" | ela | selfie contínua | emoção, fé | — | site/marca (implícito) |
| Kassiane DeHj | 179 s | ~1,5 real | selfie no cafezal com enxada / figurinha do comentário ofensivo / "foi o comentário que nós recebeu" | ela | resposta a comentário + insertos | defesa, orgulho | — | — |
| Coffeelab DeR5 | 16 s | 0,6 | trocando letras do letreiro / "ESTAMOS HÁ _ DIAS SEM SERMOS DESTRATADOS" / "hoje zeramos nossa placa" | barista (de costas) | objeto conta a história | denúncia | — | legenda |
| Orfeu DaiGL | 57 s | 3,0 | mesa posta / "para fazer do café uma pequena ocasião" / narração calma | criadora de lifestyle | tutorial de estúdio | aspiracional | — | — |
| Orfeu DcCB | 16 s | 0 | drip com vapor / "Um sinal para desacelerar…" / música | ninguém | anúncio | publicidade | — | legenda |
| Um DVjj | 96 s | 6,6 | criador no balcão / legenda máquina de escrever / "moro no Brasil há 24 horas" | criador + barista | tutorial em passos | leve | "agressivo" (perfil intenso) | — |
| Amanda (4) e Isabela Dd9M | 6–121 s | 0–1,6 | família/política | família / ela | meme, selfie | humor familiar / política | — | — |

---

## 1. Quais Reels brasileiros de café de fato viralizam, e de quem?

### Takeaway
Os números de topo dessas contas se dividem em três grupos: (a) **vida real de quem produz** (Kassiane, 32,3 mi e 5,2 mi); (b) **"você está comprando café ruim e não sabe"**, gravado na gôndola ou na lavoura, com a torra escura como vilã (Café Gerações, 13,1 mi e 5,5 mi; Daniel Nou, 122 mil curtidas); (c) **conteúdo que não é de café** (Amanda Barista: os três fixados, 4,5–11,1 mi, são da família; Isabela Raposeiras: 2,4 mi é político). Marcas de torrefação "bonitas" (Orfeu, Um Coffee) não viralizam organicamente.

### Cited Findings
- @kassianethaynaoficial_ (2,7 mi seguidores, 1.323 posts): Reel fixado da colheita na pirambeira com **32,3 mi views**, 2.296.145 curtidas e 38.248 comentários; lançamento da própria marca com 5,2 mi views e 123.899 comentários — [C8XugrWh_-n](https://www.instagram.com/reel/C8XugrWh_-n/); [DK0HqC5S_Hm](https://www.instagram.com/reel/DK0HqC5S_Hm/)
- Kassiane é cafeicultora de Piedade de Caratinga (MG), 25 anos na reportagem, e lançou marca própria de café em 2024 — [Boca Notícias](https://www.boca.com.br/agronegocio/kassiane-thayna-sucesso-digital-cafe-especial); viralizou mostrando "com muito humor" a dificuldade da colheita — [Band Agro](https://www.band.com.br/agro/noticias/agricultora-viraliza-nas-redes-sociais-ao-mostrar-como-e-dificil-colher-cafe-202406201635)
- @cafegeracoes (Alberto Martins, "Produtor & torrefador de cafés especiais", 556 mil seguidores): "Escolhendo café no supermercado" com **13,1 mi views**, 389.635 curtidas, 7.213 comentários — [CqGC2e7g5nf](https://www.instagram.com/reel/CqGC2e7g5nf/); "Não é CHAFÉ!" com **5,5 mi views**, 306.665 curtidas — [DVobHGpAW2Y](https://www.instagram.com/reel/DVobHGpAW2Y/)
- Os Reels recentes do Café Gerações (fim de set.–out. 2026) ficam entre 3,3 mil e 40 mil views: a conta vive de poucos picos — grade de [@cafegeracoes/reels](https://www.instagram.com/cafegeracoes/reels/)
- @amandabaristaa: os três Reels fixados (11,1 mi, 10,1 mi, 4,5 mi) são de família, sem café; os recentes também (7 mil–351 mil) — [DCFZKnnsMjx](https://www.instagram.com/reel/DCFZKnnsMjx/); [C_AvrBuxgMj](https://www.instagram.com/reel/C_AvrBuxgMj/); [C4eJrrkLMPJ](https://www.instagram.com/reel/C4eJrrkLMPJ/); [DeLLLxpNbtP](https://www.instagram.com/reel/DeLLLxpNbtP/)
- @isabela.raposeiras: maior da grade recente é político (2,4 mi; 368 mil curtidas; 20 mil comentários); o segundo é collab com @coffeelab sobre clientes que destratam a equipe (645 mil) — [Dd9M1ytxbDO](https://www.instagram.com/reel/Dd9M1ytxbDO/); [DeR5EiZvusW](https://www.instagram.com/reel/DeR5EiZvusW/)
- @felipebrazza (Café das Amoras; bio "filtre café, não pessoas"; 59,6 mil seguidores): três Reels de 1–1,7 mi (mitos, gambiarras, do pé à xícara); recentes entre 2,8 mil e 39 mil — [C0r_Lc9O851](https://www.instagram.com/reel/C0r_Lc9O851/); [C6UA4X9r-4N](https://www.instagram.com/reel/C6UA4X9r-4N/); [DFf3isuuhcS](https://www.instagram.com/reel/DFf3isuuhcS/)
- @orfeucafes (154 mil seguidores): Reels com 100–534 mil views, mas o de 534 mil tem 5.528 curtidas (≈1%) e o de 492 mil tem 1.223 (≈0,25%) — padrão de alcance pago/collab — [DaiGLxiR0Ko](https://www.instagram.com/reel/DaiGLxiR0Ko/); [DcCB9dQhKYn](https://www.instagram.com/reel/DcCB9dQhKYn/)
- @umcoffeeco (campeões mundiais de barismo, 88 mil seguidores): maior Reel recente 50,4 mil views, e é collab com criador estrangeiro; o resto entre 1,7 mil e 26,6 mil — [DVjjyTpDk65](https://www.instagram.com/reel/DVjjyTpDk65/)
- Busca por fazenda da Serra da Canastra: @fazendacafeserradacanastra tem 961 seguidores e Reels de 327 a 4.649 views — grade de [@fazendacafeserradacanastra/reels](https://www.instagram.com/fazendacafeserradacanastra/reels/)

### Inferences
- O que viraliza no café brasileiro é **gente** (produtora, produtor, filha) e **conflito com uma crença do consumidor** — não produto, não estética.
- Views de marca precisam ser lidas junto com curtidas: abaixo de ~2% de curtidas/views, o número indica distribuição paga, não conteúdo que o público escolheu.
- Contas de "barista" grandes podem ter crescido fora do café; copiar o perfil delas não traz o público de café.

### Gaps
- Views de DARbgCGyf5H e DVMF38UgD0M não foram lidas na grade (vieram da busca por palavra-chave); só curtidas.
- "Marcelo Pedras" não foi encontrado no Instagram (busca devolveu homônimos sem café); usei @_noudaniel e o Reel de supermercado do @cafegeracoes, achados pela busca "café de supermercado".
- A grade só carrega as últimas ~12–21 peças + fixados; Reels antigos virais não fixados podem ter ficado de fora (o Instagram limitou a sessão com HTTP 429 durante a coleta).

## 2. Como são feitos: gancho, ritmo, quem aparece, texto na tela

### Takeaway
Os vencedores abrem com **uma pessoa real já no meio da ação ou com a objeção escrita na tela** em 0–3 s, falam com a câmera (talking head ou selfie) e usam legenda queimada. O ritmo de corte varia de 0 (selfie contínua de 3 min) a 8,5 cortes/10 s (Brazza): **corte rápido não é requisito**; o que segura é a fala ou o conflito. Ninguém usa narração de voz sintética nem colagem animada.

### Cited Findings
- Gancho por objeção escrita: "Não é CHAFÉ!" sobre a produtora com duas canecas, clara e escura, na lavoura, em céu azul — [DVobHGpAW2Y](https://www.instagram.com/reel/DVobHGpAW2Y/)
- Gancho por ação real: tombo no barranco em ~3 s com legenda "Quando é dia de Panhar café na paranbeira eu o dia todo 😂" — [C8XugrWh_-n](https://www.instagram.com/reel/C8XugrWh_-n/)
- Gancho por comentário: figurinha "mais um apenas trabalhadora que se acha rica, mas não é!" e resposta em selfie no cafezal; 14.631 comentários — [DeHjlCAoQc1](https://www.instagram.com/reel/DeHjlCAoQc1/)
- Gancho por título-lista: "MITOS E VERDADES SOBRE O CAFÉ" digitado palavra a palavra e o primeiro mito respondido em 5 s; "gambiarras do café" — [C0r_Lc9O851](https://www.instagram.com/reel/C0r_Lc9O851/); [C6UA4X9r-4N](https://www.instagram.com/reel/C6UA4X9r-4N/)
- Gancho imperativo: "🔴 Não compre café ruim pra sua casa nunca mais" — [DVMF38UgD0M](https://www.instagram.com/reel/DVMF38UgD0M/)
- Ritmos medidos: Brazza 7,8 e 8,5 cortes/10 s; Um Coffee 6,6; Gerações 0,6–2,2; Kassiane 0,1–1,0; Nou ~0 (contínuo com legenda palavra a palavra) — arquivos por vídeo em `videos/brasil/`
- Duração: os educativos que viralizaram têm 40–84 s (Gerações 41 s, 84 s, 84 s; Brazza 48–58 s); os de Kassiane vão de 39 s a 2 min 58 s — idem
- Som: nenhum dos Reels de café vencedores usa música de fundo sob a fala; som direto. Música só nas peças de marca (Orfeu) e nos de família — idem

### Inferences
- A peça da Canastra (59 s, voz feminina de IA, colagem animada) está no formato oposto ao dos vencedores brasileiros: sem rosto, sem som direto, sem objeção do público. A duração (59 s) não é o problema; o meio é.
- O padrão Brazza (um item por plano, cenário trocando a cada fala, legenda amarela) é o único de alto corte que funciona — e funciona porque cada corte entrega uma informação nova.

### Gaps
- Retenção e taxa de compartilhamento não são públicas; o diagnóstico usa views/curtidas/comentários.

## 3. Como se fala de torra, "forte" e "queimado"

### Takeaway
Os vídeos mais vistos sobre café-bebida no Brasil tratam a **torra escura / extraforte como o vilão** ("mascara a baixa qualidade", "aparece o carvão", "pau velho com casca") e **defendem a torra média contra a acusação de "chafé"/"fraco"**. Ninguém mostra fogo nem chama a torra de "queimar": "queimar o café" aparece só como mito a desmentir.

### Cited Findings
- "tradicional e extraforte… receberam torra excessiva para mascarar a baixa qualidade, e ficou convencionado que café é amargo, café escuro"; recomenda gourmet/especial de torra média para tomar sem açúcar — [CqGC2e7g5nf](https://www.instagram.com/reel/CqGC2e7g5nf/)
- "Este aqui, que a maioria das pessoas chama de chafé, é um cafezão especial… Torra escura corrige a baixa qualidade… Coloca açúcar como legítima defesa… Este aqui não é um café fraco. É uma torra média, para mostrar as características do café" — [DVobHGpAW2Y](https://www.instagram.com/reel/DVobHGpAW2Y/)
- Criança explica: "extraforte é a classificação de baixo… tipo de torra: médio, porque não vai amargar" — [DARbgCGyf5H](https://www.instagram.com/reel/DARbgCGyf5H/)
- "o extraforte fica mais escuro porque aparece o carvão"; o cético diz que o especial "parece ralo", e a resposta é "experimenta, tem sabor" — [DVMF38UgD0M](https://www.instagram.com/reel/DVMF38UgD0M/)
- "Se ferveu a água vai queimar o café? Isso é mito"; "que café você bebe? Extraforte, claro" usado como piada — [C0r_Lc9O851](https://www.instagram.com/reel/C0r_Lc9O851/)
- Na série da fazenda, a torra é "onde a parada acontece… ressaltar as principais características do grão", com close de grão de torra média — [DFf3isuuhcS](https://www.instagram.com/reel/DFf3isuuhcS/)
- O vocabulário do público que os vídeos rebatem: "chafé", "fraco", "ralo", "preto e amargo", "forte" — transcrições acima

### Inferences
- O feedback do dono da Canastra ("a parte do fogo no grão levou a entender que o café é queimado") bate exatamente com a moldura vencedora: no imaginário brasileiro, escuro/forte/queimado = café de supermercado barato. Imagem de fogo no grão ativa o vilão, não o herói.
- A palavra que vende o especial para esse público é **"torra média"** apresentada como o oposto do extraforte, com a cor clara mostrada lado a lado e defendida ("não é fraco").

### Gaps
- Não encontrei Reel de grande alcance que use "torra clara" positivamente sem o contraponto da escura; o público ainda precisa da comparação.

## 4. Tom e humor: dentro ou fora do café?

### Takeaway
O humor que funciona é **de dentro do café e da vida real**: o tombo na colheita, a gambiarra para coar, o cético que diz "mijo de cabra", "açúcar como legítima defesa". Não há metáfora gastronômica fora do contexto (nada parecido com "frango assado"). Quando o humor sai do café (Amanda), o alcance vem, mas não é de café.

### Cited Findings
- Humor físico e de identificação na roça ("o Brasil que eu quero é o Brasil onde a gente não tem de panhar café na pirambeira") — [C8XugrWh_-n](https://www.instagram.com/reel/C8XugrWh_-n/)
- Humor de improviso brasileiro: mixer em garrafa, elástico na boca, "modo sobrevivente" — [C6UA4X9r-4N](https://www.instagram.com/reel/C6UA4X9r-4N/)
- Um só ator fazendo os dois papéis (leigo × especialista) — [C0r_Lc9O851](https://www.instagram.com/reel/C0r_Lc9O851/)
- "Coloca açúcar como legítima defesa" — [DVobHGpAW2Y](https://www.instagram.com/reel/DVobHGpAW2Y/)
- Tom emocional e de fé (lançamento de marca e resposta a comentário) também gera números altos de comentário — [DK0HqC5S_Hm](https://www.instagram.com/reel/DK0HqC5S_Hm/); [DeHjlCAoQc1](https://www.instagram.com/reel/DeHjlCAoQc1/)
- Humor fora do café gera os maiores números da @amandabaristaa (meme de 6 s) — [DCFZKnnsMjx](https://www.instagram.com/reel/DCFZKnnsMjx/)

### Inferences
- "Nada a ver essa do frango assado" é coerente com o que o público premia: a comparação que funciona é com coisas do universo do café (vinho, no máximo), e o humor nasce da situação real, não de uma analogia escrita.

### Gaps
- Não medi sentimento de comentários (sem leitura dos comentários, por escopo).

## 5. Cadência e diferença entre criador e marca

### Takeaway
Criadores que viralizam postam muito (Kassiane e Amanda: ~1 Reel por dia no período visível); as contas educativas (Gerações, Brazza) vivem de **picos raros** sobre uma base baixa (3–40 mil). Marcas de torrefação têm views altas com engajamento de anúncio.

### Cited Findings
- Kassiane: 12 Reels recentes, de 137 mil a 771 mil views; DeHjlCAoQc1 publicado em 05/10/2026 — grade [@kassianethaynaoficial_/reels](https://www.instagram.com/kassianethaynaoficial_/reels/)
- Amanda: Reels em 02/10, 04/10 e 07/10/2026 — [Dd_7yZHsIFy](https://www.instagram.com/reel/Dd_7yZHsIFy/); [DeDd8QStaEm](https://www.instagram.com/reel/DeDd8QStaEm/); [DeLLLxpNbtP](https://www.instagram.com/reel/DeLLLxpNbtP/)
- Café Gerações: 2.394 posts; recentes de 3,3 mil a 40 mil, picos de 5,5 mi e 13,1 mi fixados — grade [@cafegeracoes/reels](https://www.instagram.com/cafegeracoes/reels/)
- Felipe Brazza: recentes de 2,8 mil a 39 mil; picos de 1–1,7 mi — grade [@felipebrazza/reels](https://www.instagram.com/felipebrazza/reels/)
- Orfeu: 100–534 mil views com curtidas de 0,25–1% das views — [DaiGLxiR0Ko](https://www.instagram.com/reel/DaiGLxiR0Ko/); [DcCB9dQhKYn](https://www.instagram.com/reel/DcCB9dQhKYn/)

### Inferences
- O mesmo roteiro pode ser reaproveitado com outro apresentador (Gerações: aula de gôndola com o produtor → com a filha), o que é o jeito mais barato de buscar um novo pico.

### Gaps
- Datas de todos os Reels da grade não foram coletadas (só dos baixados); cadência é estimativa.

## 6. Síntese: o que funciona com o público brasileiro de café, e o que isso diz da peça rejeitada

### Takeaway
Funciona: **pessoa real da origem, falando com a própria voz, no lugar real (lavoura, gôndola, terreiro), respondendo a uma crença do público ("chafé", "extraforte é melhor", "especial é complicado"), com prova visual simples e legenda queimada**. A peça "esse café já foi uma fruta" (voz de IA, colagem, fogo no grão, analogia de frango assado) inverte cada um desses pontos.

### Cited Findings
- O vídeo mais próximo do que a Canastra pode gravar amanhã: produtora no cafezal ao sol, duas canecas, "Não é CHAFÉ!", 41 s, 5,5 mi views — [DVobHGpAW2Y](https://www.instagram.com/reel/DVobHGpAW2Y/)
- A versão real do arco "fruto → xícara": produtor-barista filmando cada etapa com números (25 dias de terreiro, umidade 11–12%, 500 g), 58 s, 1 mi views — [DFf3isuuhcS](https://www.instagram.com/reel/DFf3isuuhcS/)
- Supermercado como cenário campeão (13,1 mi e 299 mil curtidas na mesma conta; 122 mil curtidas em outro criador) — [CqGC2e7g5nf](https://www.instagram.com/reel/CqGC2e7g5nf/); [DARbgCGyf5H](https://www.instagram.com/reel/DARbgCGyf5H/); [DVMF38UgD0M](https://www.instagram.com/reel/DVMF38UgD0M/)
- Vida real da colheita, sem roteiro, 32,3 mi — [C8XugrWh_-n](https://www.instagram.com/reel/C8XugrWh_-n/)

### Inferences
- Para a Canastra (fazenda própria a 1.250 m, desde 1985, torrefação própria): (1) **"Não é chafé"** com alguém da família no cafezal de Medeiros sob sol a pino, xícara de torra média ao lado de um extraforte; (2) **"do pé à xícara"** filmado de verdade (não colagem), com números da própria fazenda; (3) **mitos e verdades** com um mito por plano, incluindo "água fervendo queima o café" e "extraforte é mais forte"; (4) **responder comentários** reais em vídeo no cafezal; (5) **gôndola**: pacote Canastra ao lado do extraforte, lendo a classificação.
- Evitar: fogo/chama sobre grão, palavra "queimar" como descrição do processo, voz sintética, metáforas fora do universo do café, estética de anúncio de estúdio sem pessoa.

### Gaps
- Não há dado público de conversão (vendas) desses Reels; o diagnóstico é de alcance e engajamento.
- Transcrições automáticas (whisper base/small) têm erros de reconhecimento; as falas citadas acima foram conferidas contra a legenda queimada e os quadros quando possível.
