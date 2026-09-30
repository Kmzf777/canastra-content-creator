# O que a plataforma premia

Este arquivo decide **por qual sinal otimizar** — e, mais importante, quais sinais são
declaração do Instagram e quais são palpite de criador que o vocabulário de mercado
apresenta como se fosse algoritmo.

Marcação conforme [`LEIA-ME.md`](LEIA-ME.md). Procedência de cada linha em
[`08-fontes.md`](08-fontes.md). Toda afirmação sem marca aqui é erro de redação.

A divisão que organiza o arquivo: **§1 a §4 são [oficial] e podem virar meta. §5 é
[criador] e [terciário], e não pode.**

---

## 1. Os três sinais que a plataforma nomeou

Os três mais importantes, tanto para alcance dentro dos seguidores quanto na recomendação
para quem não segue **[oficial]**:

| Sinal | Peso relativo | Onde pesa mais |
|---|---|---|
| **Tempo médio assistido** | o **principal** nos dois casos | seguidor e não-seguidor **[oficial]** |
| **Curtidas por alcance** | secundário | mais no **conectado** — quem já segue **[oficial]** |
| **Envios por alcance** | secundário | mais no **não-conectado** — quem ainda não segue **[oficial]** |

Mosseri, textualmente: *"sends são uma parte enorme do sucesso dos Reels"* **[oficial]**,
em entrevista à Semafor.

### O que isso muda na prática

1. **Tempo assistido é o alvo, não curtida.** A curtida é o que conseguimos medir de fora
   — é o único sinal público **[medido]** — e por isso virou a moeda de toda comparação em
   [`01-concorrencia.md`](../01-concorrencia.md). Ela **não** é o sinal principal que a
   plataforma declarou. Decidir formato por curtida é decidir pelo que é visível, não pelo
   que é premiado.
2. **Crescer para fora depende de envio, não de curtida.** É a consequência direta de
   *envios por alcance pesar mais no não-conectado* **[oficial]**. *(Leitura minha, não
   medição: o conteúdo que ganha público novo é o que alguém manda para outra pessoa — e o
   que se manda para outra pessoa é o que resolve uma dúvida dela. "Como ler o rótulo de um
   café especial", "por que este café custa três vezes o do mercado", "o que significa 84
   pontos". Repertório de marca não se encaminha; utilidade se encaminha. Não temos medição
   de envio da nossa conta para provar isso.)*
3. **A nossa taxa de 0,50% tem outro denominador.** O sinal oficial é *curtidas por
   **alcance*** **[oficial]**; a nossa taxa é *curtidas medianas ÷ **seguidores***
   **[medido]**. Denominadores diferentes medem coisas diferentes. Os 0,50% servem para
   comparar perfis entre si, e é só isso que fazem.

---

## 2. O ranking por exploração — e por que ele é o argumento da cadência

Conteúdo novo recebe **~100 impressões**. Performando acima do esperado, gradua para
**1.000**, e depois para **10.000** **[oficial]**. É esse mecanismo que permite conta
pequena estourar: o alcance não é concedido pelo tamanho da base, é conquistado por degrau.

A consequência aritmética é brutal, e é a razão de este arquivo existir. *(Conta feita
sobre número **[medido]**, não medição nova — e ilustra ordem de grandeza, não previsão: o
"~100" descreve o mecanismo, não garante piso por post.)*

| Conta sobre **[medido]** | Canastra hoje | Piso da categoria (~2/sem) |
|---|---:|---:|
| Posts por semana — este é o número medido | **0,17** | 2 |
| Posts em 90 dias — aritmética | ~2 | ~26 |
| Posts em 12 meses — aritmética | ~9 | ~104 |
| Tentativas de exploração no ano — aritmética | ~9 | ~104 |

**São ~12× menos tentativas.** E há um caso pior que a média: entre **23/05 e 25/09/2026
saiu um único post** — 125 dias em que o Orfeu publicou cerca de 43 peças e o Coffee++
cerca de 60 **[medido]**.

Não é possível graduar para 1.000 impressões um post que não existe. **Cadência não é
higiene de marketing; é a quantidade de bilhetes na loteria de exploração.** O plano de
cadência está em [`06-cadencia.md`](06-cadencia.md).

---

## 3. Elegibilidade para não-seguidores — a lista que desqualifica

Recomendação para quem não segue exige, cumulativamente **[oficial]**:

| Critério **[oficial]** | O que reprova a nossa peça | Verificável por nós? |
|---|---|---|
| **Sem marca d'água** | reel exportado do TikTok, ou salvo com assinatura do app de edição | sim, no pixel |
| **Com áudio** | vídeo mudo, ou faixa silenciosa por engano de render | sim, no arquivo |
| **≤ 3 minutos** | peça longa de bastidor sem corte | sim, no arquivo |
| **Substancialmente original** | repost de conteúdo de terceiro | parcialmente — o critério é da plataforma, não nosso |
| **Conta em bom status** | violação anterior, aviso de direitos | **não** — não temos leitura disso |

Três leituras operacionais:

- **Áudio não é acabamento, é requisito de elegibilidade.** Um reel mudo pode até rodar
  entre seguidores; ele não entra na recomendação para quem não segue **[oficial]**. O
  motor em `instagram/remotion/` tem que entregar faixa de áudio em toda saída — a fonte
  `pl.mp4` do projeto tem áudio médio de −26 dB **[medido]**, ou seja, existe faixa e ela é
  baixa. Render sem áudio é falha de elegibilidade, não de estética.
- **Marca d'água é a armadilha do reaproveitamento.** Publicar em outra plataforma primeiro
  e baixar de lá para o Instagram carrega a assinatura e derruba o critério **[oficial]**.
  A exportação sai do projeto, nunca do app concorrente.
- **"Substancialmente original" tensiona um dos formatos que a pesquisa recomendou.** O
  modelo @omsom é repostar piada relatable de terceiro, com custo de produção zero
  **[criador]** — ver [`04-arquetipos.md`](04-arquetipos.md). *(Leitura minha, não medição:
  repost de peça de terceiro é exatamente o que um critério de originalidade tende a
  filtrar, então esse formato deve ser tratado como conteúdo para seguidor, não como aposta
  de alcance novo. A plataforma não publicou onde fica a fronteira, e nós não medimos.)*

**Lacuna:** "conta em bom status" não é consultável de fora, e não sabemos o status da
`@cafecanastra`. Quem tiver acesso ao painel da conta confere isso **antes** de atribuir
alcance baixo à qualidade do conteúdo.

---

## 4. A grade do perfil é vertical

A grade do perfil passou a ser vertical porque a maioria dos uploads já é vertical
**[oficial]**.

O que isso cobra de nós: **69% do feed da Canastra é estático** **[medido]**, e a peça
estática do projeto nasce para catálogo — o catálogo da Tray serve tudo em **1:1**
(600×600, medido no arquivo original e registrado no `CLAUDE.md`) **[medido]**. Arte
quadrada entra numa grade vertical com sobra, e a decisão de corte deixa de ser nossa.

*(Leitura minha, não medição: a proporção real dos posts estáticos da `@cafecanastra` no
feed **não foi medida** — `01-concorrencia.md` mediu cadência, tipo e curtida, não aspecto.
Antes de tratar isto como problema confirmado, meça o aspecto dos últimos 12 posts.)*

A regra de produção que sai daqui é de geração, não de estratégia: a saída para feed nasce
vertical. `4:5` é nativo no Gemini; na xAI **não existe** e sai de `3:4` com corte de
altura **[medido]**, conforme `CLAUDE.md`.

---

## 5. Inferência de criador — **não é ranking, e não vira meta**

Tudo nesta seção vem de criador ou de estudo que não abrimos. **O Instagram não declarou
nenhuma destas afirmações.** Elas servem para gerar hipótese de teste com prazo, nunca para
cobrar resultado — é a regra fechada em [`08-fontes.md`](08-fontes.md) §7.

### 5.1 Engajamento mediano por formato **[criador]**

| Formato | Engajamento mediano **[criador]** | Outras leituras da mesma fonte **[criador]** |
|---|---:|---|
| Carrossel | 6,9% | +12% de engajamento sobre reels |
| Foto única | 4,4% | — |
| Reels | 3,3% | +36% de alcance |

**Agravante:** não sabemos de qual canal veio isso **[criador]**. É a análise de uma conta
só, não estudo, e a fonte não está nomeada — conferido em
[`08-fontes.md`](08-fontes.md) §3 e §7 **[medido]**.

E há um conflito com o que nós mesmos medimos: nesta tabela reel é o formato de **menor**
engajamento, mas na nossa amostra **reel bate estático em todo perfil** — 5,2× no
@sebastianspecialtycoffee, 3,2× no @cafezale.com.br **[medido]**. A explicação provável é
de denominador outra vez: a nossa medida é curtida, e curtida **subestima reel**, que roda
por view **[medido]**. Não é possível resolver a divergência com o que temos. **O que
medimos no nosso nicho vence a inferência de um canal não identificado.**

### 5.2 Retenção: rosto e voz **[terciário]**

Atribuído a um estudo do *Social Media Today* com ~10 mil reels, citado pelo canal *Build
Your Tribe*. **O estudo original não foi verificado** — não sabemos autor, ano, metodologia
nem se existe **[terciário]**:

- rosto humano visível nos primeiros 3 s por ≥1 s → **+10% de retenção** **[terciário]**;
- vídeo com voz → engajamento **5,6% maior** que só-música **[terciário]**;
- falar aumenta o tempo assistido em **~25%** **[terciário]**.

Por que ainda assim fica registrado: se *tempo médio assistido* é o sinal principal
**[oficial]**, qualquer coisa que plausivelmente o aumente merece ser **testada**. Rosto e
voz custam nada na Canastra — o pai Silvio na lavoura já é parte do material que o feed
sabe fazer e abandonou **[medido]**. Mas o número não vai para meta nenhuma, e a restrição
de imagem do projeto continua valendo: **rosto de pessoa real nunca é sintetizado; foto de
pessoa é foto** (`CLAUDE.md`).

### 5.3 Velocidade de curtidas nas primeiras 24 h **[criador]**

Circula como sinal do Explore *(Jade Beason)*. **O Instagram nunca declarou isso**
**[criador]**.

**E é aqui que a inferência convida a um erro que já está medido.** A tentação óbvia é
forçar velocidade de sinal com sorteio. O único post do Coffee++ fora da curva é exatamente
isso: **1.545 curtidas e 4.151 comentários num sorteio** — numa conta de 269 mil seguidores
cuja mediana é 96 curtidas, 0,04% **[medido]**. *(Leitura minha, não medição: uma base
construída por sorteio explica o seguidor grande e o engajamento baixo ao mesmo tempo; não
dá para provar isso de fora.)*

> **Não transfere:** sorteio para comprar velocidade de curtida. A conta que mais fez isso
> na amostra é a de **pior** engajamento medido **[medido]**, e a Canastra é marca de
> procedência de fazenda de família — o ativo é confiança, não volume de inscrição. O mesmo
> vale para qualquer compra de sinal inicial que dependa de verba de experimentação, que a
> marca não tem.

---

## 6. Nenhum dos três sinais oficiais é observável de fora

Registrado como lacuna, para não ser confundido com omissão:

| Sinal **[oficial]** | Medimos? | Como obter |
|---|---|---|
| Tempo médio assistido | **não** | painel da conta (Insights), só logado |
| Curtidas por alcance | **não** — medimos curtidas ÷ seguidores | Insights dá o alcance |
| Envios por alcance | **não** | Insights, por post |

Views, salvamentos, compartilhamentos, alcance, stories e anúncios pagos **não foram
medidos** **[medido]**.

**A próxima coleta tem que ser do painel próprio, não do DOM público.** A comparação com
concorrente esgotou o que a curtida pode dizer; os três sinais que a plataforma nomeou só
existem dentro da conta. Sem isso, toda otimização daqui é otimização de proxy — e é justo
disso que o `CLAUDE.md` avisa em outro contexto: não transforme em garantia escrita o que
você não mediu no arquivo real.

---

## 7. Uma contradição a não resolver aqui

Uma fonte de criador sustenta que postar em sequência suprime alcance **[criador]**; o
recurso oficial **Trial Reels** existe justamente para postar mais sem esse risco
**[oficial]**. As duas coisas não se encaixam, e este arquivo não escolhe um lado — está
registrada com as outras três em [`07-nao-fazer.md`](07-nao-fazer.md).

O que importa para a decisão: a tese da supressão é **[criador]**, o argumento contrário é
**[oficial]**, e a meta de cadência de [`06-cadencia.md`](06-cadencia.md) não deve ser
freada por inferência não confirmada.

---

## 8. A leitura para a Canastra

> A conta tem 10,3 mil seguidores e engajamento de 0,50% — saudável, acima do Coffee++ com
> 269 mil. O gargalo não é a audiência, é a frequência: a 1 post a cada 42 dias, a marca
> compra pouquíssimos bilhetes na loteria de exploração. **[medido]**

Os números que fecham o argumento, todos **[medido]** em 30/09/2026:

| | Canastra | Comparação |
|---|---:|---|
| Seguidores | 10.300 | @cafeserradacanastra ocupa o nome com 14.400 e 0,05% |
| Taxa (curtidas ÷ seguidores) | **0,50%** | Coffee++ 0,04% · Orfeu 0,74% · Sebastian 0,57% |
| 1 post a cada | **42 dias** | Orfeu 2,9 · Coffee++ 2,1 · Italle 0,9 |

Três consequências, na ordem em que valem:

1. **Não é problema de audiência.** 0,50% com 10,3 mil seguidores é acima do Coffee++, do
   Cafezale e dos três homônimos **[medido]**. Quem olha esses números e conclui "precisamos
   melhorar a imagem" está corrigindo a variável que já está boa.
2. **O gargalo é volume de tentativa.** ~9 posts no ano contra ~104 do piso da categoria
   (aritmética do §2 sobre a cadência **[medido]**, não medição nova) são ~12× menos
   exposições ao mecanismo de exploração **[oficial]** — e esse mecanismo é a única rota
   declarada para uma conta de 10 mil alcançar quem não a segue.
3. **A peça tem que sair pronta para ser encaminhada.** Envios pesam mais no não-conectado
   **[oficial]**. Utilidade se encaminha; institucional não. É a razão de
   [`05-formatos.md`](05-formatos.md) priorizar formato explicativo com matéria-prima que já
   existe, em vez de mais uma declaração de que somos uma fazenda de família.

O que este arquivo **não** autoriza: prometer resultado. A frase certa tem esta forma —
*"esta peça tem áudio, não tem marca d'água, tem 38 s e abre com rosto em 0,8 s; é elegível
para recomendação e serve para teste"* (segundos de exemplo, não medição de um clipe real).
A errada é *"este vídeo vai viralizar"*.
