# De onde veio cada afirmação

Uma linha por fonte: quem é, que tamanho tem, o que foi usado dela, e a marca de
confiabilidade definida em [`LEIA-ME.md`](LEIA-ME.md).

> **Sobre URL:** este catálogo foi reconstruído a partir de
> `docs/superpowers/plans/2026-09-30-base-estrategia-viral.md`, que é o único registro que
> sobrou da pesquisa. **O plano não anotou nenhuma URL e nenhum ID de vídeo.** Onde a
> coluna diz *não registrada*, é isso literalmente: a URL nunca foi escrita, e inventar
> uma seria pior que não ter. Verificado em 30/09/2026 **[medido]**.

---

## 1. Plataforma — [oficial]

| Fonte | Tamanho | O que foi usado | Marca | URL |
|---|---|---|---|---|
| Instagram / Adam Mosseri — série de publicações do próprio Instagram sobre ranking | plataforma; Mosseri é o chefe do Instagram | os **três sinais mais importantes** (tempo médio assistido, curtidas por alcance, envios por alcance) e qual pesa mais em seguidor vs recomendação; o **ranking por exploração** ~100 → 1.000 → 10.000 impressões; os critérios de elegibilidade para não-seguidores (sem marca d'água, com áudio, ≤3 min, substancialmente original, conta em bom status); a grade do perfil virou vertical porque a maioria dos uploads já é vertical | **[oficial]** | não registrada |
| Entrevista de Adam Mosseri à **Semafor** | veículo de imprensa | a citação textual *"sends são uma parte enorme do sucesso dos Reels"* | **[oficial]** | não registrada |
| Recurso **Trial Reels** do Instagram | funcionalidade do produto | existe como argumento oficial contra a tese de criador de que postar em sequência suprime alcance — entra em `07-nao-fazer.md` como contradição, não como resposta | **[oficial]** | não registrada |

**Limite desta linha:** *oficial* quer dizer *declarado publicamente pela plataforma*.
Não quer dizer auditado. O Instagram não publica o peso numérico de cada sinal, e nada
aqui foi confirmado contra o comportamento real da conta.

---

## 2. Medição nossa — [medido]

| Fonte | Tamanho | O que foi usado | Marca | Onde está |
|---|---|---|---|---|
| **`instagram/01-concorrencia.md`** — coleta de 30/09/2026 por sessão logada do Chrome (conta `@cafecanastra`), lendo o DOM renderizado | 10 perfis; 12 posts por perfil, exceto @orfeucafes (120) e @coffeemais (72) | tudo o que esta base afirma sobre a Canastra e os concorrentes: 10,3 mil seguidores · 677 posts · 0,17 post/semana · 1 post a cada 42 dias · mediana 52 curtidas · 0,50%; Orfeu 2,9 dias e 1.125 curtidas medianas; Coffee++ 269 mil seguidores com 0,04%; reel vs estático 5,2× no Sebastian e 3,2× no Cafezale; 69% do feed da Canastra estático; coautoria com criador rende 83 contra 52 da mediana própria, e o melhor post da amostra fez 412; o calendário que todos cumpriram e a Canastra não | **[medido]** | no repositório |
| **`instagram/LEIA-ME.md`** + sondagem do arquivo `remotion/projetos/01-private-label/fonte/pl.mp4` | 1 vídeo, 576×1024 nativo, 24,33 s, 29,96 fps | o laudo que `03-roteiro.md` escreve contra o relógio: 1,14 s de ar morto na cabeça, silêncios em 5,08 · 6,78 · 9,55 · 13,99 · 16,02 · 17,50 · 21,52 s, mais o **nono** em 23,78, áudio médio **−26,0 dB** (RMS sobre `fonte/pl.wav`, reconferido em 30/09/2026 sem `ffmpeg`) | **[medido]** | no repositório |
| **`remotion/projetos/01-private-label/transcricao.json`** — Whisper sobre `fonte/pl.wav` | 75 itens, palavra a palavra, com `inicioMs`/`fimMs` | fecha as três linhas que `03-roteiro.md` §6.3 tinha como `não verificável`: **o que** é dito, logo onde estão proposta, primeiro valor e os 4 beats semânticos | **[medido]** para o texto; a **classificação** em proposta/valor/beat é **[criador]** | no repositório |
| Amplitude de `fonte/pl.wav` em janelas de 100 ms (módulo `wave` do Python) | 389.329 amostras, 16 kHz mono 16 bits | a prova de que os `inicioMs` da transcrição estão **deslocados ~1,14 s na cabeça**: 0–1,1 s mede −59 a −71 dB RMS, e o Whisper carimba 3 palavras lá. Ver §6.4 de `03-roteiro.md` | **[medido]** | no repositório |
| Contagem de seguidores dos perfis de marca fora do café | ver seção 5 | só o número de seguidores de cada conta | **[medido]** | o plano registra os números; **não registra a data da leitura** |

**Limites desta linha, e eles são grandes:**

- A coleta de `01-concorrencia.md` mediu **curtida**, o único sinal público. **Views,
  salvamentos, compartilhamentos, alcance, stories e anúncios pagos não foram medidos.**
- As taxas são `curtidas medianas ÷ seguidores`. Comparam perfis entre si; **não** são
  taxa de engajamento de plataforma.
- Curtida **subestima reel**, que roda por view. Toda comparação reel × estático nesta
  base é conservadora a favor do estático.
- Posts fixados foram excluídos do cálculo de cadência — três itens da grade da Canastra
  são fixados e dois são de 2023 **[medido]**. Quem não separar erra o último post por
  quatro meses.

---

## 3. Canais de YouTube e criadores — [criador] e [terciário]

| Fonte | Tamanho | O que foi usado | Marca | URL |
|---|---|---|---|---|
| **Build Your Tribe** (canal/podcast), citando um estudo atribuído ao *Social Media Today* com ~10 mil reels | tamanho do canal não registrado | rosto humano visível nos primeiros 3 s por ≥1 s → +10% de retenção; vídeo com voz → engajamento 5,6% maior que só-música; falar aumenta o tempo assistido em ~25% | **[terciário]** — o estudo original **não foi verificado**; não sabemos autor, ano, metodologia nem se existe | não registrada |
| **Sandy Moraes** | 218 mil inscritos | o esqueleto AIDA adaptado **Gancho → Promessa → Outro lado → Virada → Entrega**; e a lição de que ideia boa vira gancho fraco sem promessa (*"3 perguntas boas de entrevista"* perde para *"3 perguntas para você ser aprovado"*) | **[criador]** | não registrada |
| **Kallaway** | tamanho não registrado | a fórmula de 6 elementos do gancho: Sujeito + Ação + Resultado + Contraste + [Prova] + [Tempo] | **[criador]** | não registrada |
| **Jade Beason** | tamanho não registrado | velocidade de curtidas nas primeiras 24 h como sinal do Explore | **[criador]** — sem confirmação oficial; o Instagram nunca declarou isso | não registrada |
| **Canal não identificado**, descrito no plano apenas como *"análise do próprio canal, sem estudo nomeado"* | não registrado | engajamento mediano por formato: carrossel 6,9% · foto única 4,4% · reels 3,3%; reels com 36% mais alcance; carrosséis com 12% mais engajamento | **[criador]** — e com agravante: **não sabemos de qual canal veio**. É amostra de uma conta só, não estudo | não registrada |
| **Origem não atribuída dentro do corpo das ~36 transcrições** | ~36 vídeos | as três camadas de gancho (visual, textual, verbal) e a regra de que **o texto não repete a fala**; o gancho como *resposta de orientação*; o **teste da imagem parada** a 0,5 s; a *zona do meio* entre revelar pouco e revelar demais; a média de 7,7 palavras no gancho e a faixa boa de 5–8; as três estruturas (resposta primeiro, prévia da resposta, stakes primeiro) | **[criador]** — consenso da amostra, sem autor único identificável e sem dado por trás | não registrada |

**Limite desta linha:** as transcrições **não estão no repositório** (ver seção 7). Nada
aqui pode ser reconferido na fonte. Nenhum número desta seção deve virar meta de
desempenho.

---

## 4. Código de terceiro — [criador]

| Fonte | Tamanho | O que foi usado | Marca | URL |
|---|---|---|---|---|
| Harness **`corte-viral`**, motor open source minerado pela pesquisa | 1 repositório | a tabela inteira do **relógio comportamental** (orientação, proposta, primeiro valor, novo beat, duração típica, por tipo de vídeo: resposta rápida, contradição, história); e a advertência de que a base produz *hipótese testável*, não promessa | **[criador]** — são **defaults operacionais de um projeto de terceiro**, não medição nossa nem sinal declarado pela plataforma | não registrada |

**Limite desta linha:** os segundos da tabela são a opinião embutida no código de outra
pessoa. São bons pontos de partida porque são específicos e falsificáveis — e é assim que
devem ser usados: como faixa a conferir no clipe, não como lei.

---

## 5. Perfis de Instagram de marca de produto físico — mecanismo [criador], seguidores [medido]

Leitura de DOM feita pela pesquisa. A coluna *Tamanho* é o número de seguidores lido; o
plano **não registra a data dessa leitura**, então trate o número como aproximado.

| Conta | Tamanho | O que foi usado | Marca | URL |
|---|---|---|---|---|
| **@getgraza** | 222 mil | legenda-meme sobre foto simples do produto no cotidiano; produto sempre herói; estética de celular; tom irônico. E o achado contraintuitivo: **a origem agrícola quase não aparece** — a prova de autenticidade vem do bastidor da empresa, não da oliveira. Também o formato bastidor-comemoração da equipe | seguidores **[medido]**; o mecanismo é **[criador]** — leitura nossa de 12 posts, não declaração da marca | não registrada |
| **@flybyjing** | 143 mil | **cápsulas com parceiro local por tempo limitado**, anunciadas nos dois perfis. É a resposta mais direta ao problema de ter frequência sem virar institucional | seguidores **[medido]**; mecanismo **[criador]** | não registrada |
| **@omsom** | 74,9 mil | repostar piada relatable **sem o produto aparecer**, só para reforçar identidade. Custo de produção zero | seguidores **[medido]**; mecanismo **[criador]** | não registrada |
| **@drinkpoppi** | 706 mil | flat-lay de lista relatable, com o produto pequeno entre objetos de estilo de vida | seguidores **[medido]**; mecanismo **[criador]** | não registrada |
| **@chamberlaincoffee** | 541 mil | preparo em câmera lenta com legenda emocional curta | seguidores **[medido]**; mecanismo **[criador]** | não registrada |
| **@liquiddeath** | 7,2 milhões | comédia roteirizada com ator — e o **contraexemplo**: fracassou no Reino Unido porque o humor não atravessa fronteira, e a operação é bancada por captação de US$ 195 milhões | seguidores **[medido]**; o fracasso no Reino Unido e o valor da captação são **[terciário]** — números citados sem fonte registrada | não registrada |
| **Stanley** (marca; não fica registrado se o perfil foi lido) | receita de US$ 74 mi em 2019 para US$ 750 mi em 2023; empresa de 110 anos | a comunidade vendeu pela marca — e a leitura de que a *"viralização da noite para o dia"* levou décadas de consistência | **[terciário]** — os três números não têm fonte registrada no plano | não registrada |

**Contagem que não fecha:** o plano afirma **11 perfis de Instagram lidos no DOM** —
registro interno, não reconferível — e nomeia **6** nesta seção. `01-concorrencia.md`
documenta **10** perfis de café **[medido]**, o que daria 16, não 11. Não é possível saber
quais 11 eram. **Registrado como discrepância, não resolvido** — e nenhuma afirmação desta
base depende do número 11.

---

## 6. Folclore — [folclore]

Fontes aqui não sustentam nada. Estão catalogadas para serem reconhecidas e recusadas, e
o detalhamento fica em `07-nao-fazer.md`.

| Alegação | Onde aparece | Por que não se sustenta | Marca |
|---|---|---|---|
| **"Dopamina"** como mecanismo causal de curiosidade e retenção — do tipo *"um corte a cada dois segundos libera dopamina"* | repetidamente, em várias das ~36 transcrições | **sem um único estudo citado** em nenhuma das fontes da amostra. Não existe regra estabelecida ligando frequência de corte a liberação de dopamina — refutação completa em `07-nao-fazer.md` §1.1, o único lugar desta base que discute o mecanismo | **[folclore]** |
| **"O cérebro processa imagem 60.000× mais rápido que texto"** | circula na amostra como dado | número de marketing **sem fonte rastreável**. A parte real é outra: reconhecimento de imagem em ~13 ms tem base experimental (MIT, 2014) — **o multiplicador não** | **[folclore]**, com um núcleo **[terciário]** (o MIT 2014 é citado no plano sem autores nem paper registrados) |
| **"PCR"**, **"trust score"**, **"hook layering"**, **"freezing point"** | vocabulário de criador | são **frameworks autorais**, não terminologia do Instagram. Usá-los como se fossem métrica da plataforma dá ao palpite a autoridade de um sinal de ranking | **[folclore]** quando apresentados como termo da plataforma |
| **"Estudei 1.000 ganchos"** e variantes | títulos de vídeo da amostra | é ele próprio **uma técnica de gancho** — número com escala e prova implícita. Deveria *aumentar* o ceticismo com o conteúdo, não diminuí-lo | **[folclore]** |

---

## 7. O que não foi possível reconstruir

Honestidade de procedência, porque quem ler esta base em outra sessão não vai ter a
memória desta:

1. **As ~36 transcrições de YouTube não estão no repositório.** *Retrato de 30/09/2026:*
   `instagram/pesquisa/` existe e está **vazio**; as 16 transcrições que existem no repositório
   estão em `mercadolivre/pesquisa/transcricoes/` e são de outra pesquisa — Mercado Livre Ads,
   ROAS, Full — conferido contra `mercadolivre/pesquisa/videos.tsv`. *(Sem marca de origem de
   propósito: estado de pasta envelhece — ver `LEIA-ME.md`, seção* Estado do repositório não é
   [medido]*.)* O que **não** envelhece, e é o que importa aqui: **nenhum ID de vídeo, título,
   data ou contagem de views foi registrado**, então nem encher a pasta recuperaria as fontes.
2. **Nenhuma URL foi registrada** — nem dos posts do Instagram/Mosseri, nem da entrevista
   à Semafor, nem dos canais, nem do repositório do `corte-viral`, nem dos perfis lidos.
3. **Três fontes estão sem tamanho:** Build Your Tribe, Kallaway e Jade Beason. Só Sandy
   Moraes tem número (218 mil inscritos).
4. **Uma fonte está sem nome:** a dos percentuais de engajamento por formato (carrossel
   6,9% · foto 4,4% · reels 3,3%).
5. **A data da leitura dos 6 perfis fora do café não foi registrada.**
6. **A contagem de 11 perfis não fecha** com os 6 nomeados (ver seção 5).

### A regra que sai daqui

Nenhuma afirmação **[criador]**, **[terciário]** ou **[folclore]** desta base é
reconferível na fonte original. Portanto:

- **[oficial]** e **[medido]** podem sustentar decisão e virar meta.
- **[criador]** sustenta **hipótese de teste** — vai para o calendário como experimento
  com prazo, nunca como número a bater.
- **[terciário]** e **[folclore]** não sustentam nada. Servem para reconhecer o argumento
  quando ele chegar de fora e saber recusá-lo.

E a lição de método, que já está catalogada no `CLAUDE.md` deste repositório e vale outra
vez aqui: **não transforme em garantia escrita aquilo que você não mediu no arquivo
real.** A próxima sessão de pesquisa salva a transcrição e a URL **antes** de escrever a
conclusão.
