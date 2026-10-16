# Rubrica de gancho

**Fonte única.** `scripts/ganchos.py` lê a tabela abaixo: id, tipo, quem verifica, formato e
peso. Para mudar um peso, mude aqui, e só com a aprovação do Rafael. A recalibração (`recalibrar`)
**propõe** pesos, não aplica.

- **Portão** (`portao`): falhou, a nota é **0** e o motivo vem junto. Não se compensa com
  pontos em outra regra.
- **Pontuada** (`pontuada`): soma o peso se passou. Os pesos somam **100** em cada formato,
  contando as regras `todos` mais as do formato.
- **Bônus** (`bonus`): soma se passou e **não pende nem tira** se ausente. A nota final é
  limitada a 100.
- **Quem:** `script` é decidido por `checar` e não se discute; `claude` é julgamento, e
  cada um leva uma linha de justificativa na resposta.

Marcação de origem como em `instagram/estrategia/LEIA-ME.md`: **[oficial]**, **[medido]**,
**[criador]**, **[terciário]**, **[folclore]**, e *(leitura minha)* quando é interpretação. O
corpus é o de `instagram/ganchos/padroes.md`: 128 Reels virais, **só vencedores**.

| id | regra | tipo | quem | formato | peso | como verificar | fonte |
|---|---|---|---|---|---|---|---|
| P1 | Número ou alegação tem fonte | portao | script | todos | 0 | Algarismo ou número por extenso no texto sem `--fonte` reprova. A fonte é o arquivo ou documento que mede aquele número. | `02-ganchos.md`, "A regra de sourcing" (3 erros pagos neste repositório) **[medido]** |
| P2 | Sem pseudociência | portao | script | todos | 0 | dopamina, cérebro, neuro, cortisol, serotonina, "60 mil vezes" | `07-nao-fazer.md` §1.1–1.2 **[folclore]** recusado |
| P3 | Sem escassez nem superlativo sem prova | portao | script | todos | 0 | "últimas unidades", "só hoje", "mais premiado", "o melhor do Brasil" sem `--fonte` | `02-ganchos.md`, ganchos reprovados ("O café mais premiado de Minas", "Últimas unidades da safra!") **[criador]** |
| P4 | A promessa é paga | portao | claude | todos | 0 | Escreva a promessa em uma frase e aponte o slide (capa) ou o segundo (Reel) que a paga. Sem slide ou segundo apontável, reprova. | `07-nao-fazer.md` §3.1, "Gritar sem entregar" **[criador]** |
| M1 | Tamanho na faixa do formato | pontuada | script | todos | 6 | Capa: manchete com 2–9 palavras e até 60 caracteres, apoio com até 120. Reel: 1ª frase falada com 5–13 palavras, tela com 2–7. | Faixa p25–p75 do corpus **[medido]** (pt: tela 2–9; total: fala 5–13, tela 2–7). Caracteres: `ORCAMENTO` de `instagram/carrossel/molde.py` **[medido]**. O 5–8 de `02-ganchos.md` **[criador]** é mais estreito que o que os virais fazem. |
| M2 | A 2ª camada não repete a 1ª | pontuada | script | todos | 4 | Palavras de conteúdo (mais de 3 letras) da manchete × apoio, ou da fala × tela: sobreposição acima de 50% reprova | `02-ganchos.md`, "o texto não repete a fala"; falha real em G9 **[criador]** |
| M3 | Sem vício de IA nem palavra que a voz recusa | pontuada | script | todos | 10 | Qualquer linha `proibe = sim` de `vicios-ia.md` que casar reprova; as de `onde = tela` só no texto lido | `vicios-ia.md`: V1–V9 aparecem em 0 a 1 dos 128 virais **[medido]**; V10–V15 são decisão do cliente em `10-voz.md` §6–§7 (15/10/2026) |
| M4 | Sem abertura proibida | pontuada | script | todos | 4 | Saudação, "hoje eu vou falar", "neste post", "fica até o final", "você não vai acreditar" no início | `07-nao-fazer.md` §3.4 e `02-ganchos.md`, reprovados **[criador]** |
| J1 | Lacuna específica | pontuada | claude | todos | 14 | Escreva a pergunta exata que a pessoa faz depois de ler. Se não conseguir escrever, ou se a pergunta já vem respondida, falha. | `02-ganchos.md` Teste 2, `03-roteiro.md` §2 "zona do meio" **[criador]** |
| J2 | Promessa, não assunto | pontuada | claude | todos | 10 | A frase diz o que a pessoa ganha ("o que a peneira tira do seu café") e não só o tema ("como funciona a secagem")? | `02-ganchos.md`, Sandy Moraes **[criador]** |
| J3 | Tem contraste | pontuada | claude | todos | 10 | Existe uma tensão entre duas coisas: esperado × real, caro × barato, parece × é? | Fórmula de 6 elementos, Kallaway, em `02-ganchos.md` **[criador]**. No corpus, o padrão `veredito-direto` é o contraste em frase (`padroes.md`) **[medido]** |
| J4 | Coisa real e concreta | pontuada | claude | todos | 10 | O gancho nomeia ou mostra um objeto, lugar, número medido ou gesto que só existe aqui (o GPS de 2017, o pacote, a lasquinha no pó)? Abstração ("qualidade", "experiência", "sabor") falha. | Etiqueta `acao-no-meio` ou `imagem-estranha` em 80 de 130 fichas, e 35,2% dos virais sem texto na abertura **[medido]**. `relatorio.md`: "o gancho mostra uma coisa real em 0–3 s" *(leitura sobre o corpus)* |
| J5 | Tom de procedência | pontuada | claude | todos | 6 | Risco real (chuva, safra, preço) sim; drama fabricado, humor de fora do café, ataque a concorrente nomeado, não | `03-roteiro.md` §4 "guarda de tom", `07-nao-fazer.md` §2.1 **[criador]**; C1 fora do banco por decisão de dono (`02-ganchos.md`); `10-voz.md` §4 (o vilão é o café do outro, nunca quem toma) e §5 (humor só de dentro do café) |
| J6 | Usa um padrão com lastro | pontuada | claude | todos | 6 | O gancho é de um dos 7 padrões com mediana ≥ 1 mi de views **entre os virais de café**: `situacao-reconhecivel`, `acao-em-curso`, `quem-faz-mostra`, `resultado-antes`, `veredito-direto`, `pergunta-diagnostico`, `conflito-resposta`. `marca-clima` e `objeto-impossivel` não contam, nem padrão em que um perfil sozinho tem metade ou mais dos casos (hoje `conflito-resposta`: @nacaradi tem 3 de 6). Colunas `perfis` e `dominante` de `padroes.md`. | `padroes.md` **[medido]**: no recorte café, `marca-clima` tem mediana de 113 mil e `objeto-impossivel` 281 mil, contra 1,4 a 5,3 mi dos outros sete. Ainda é comparação entre vencedores, então indica tendência, não prova *(leitura minha)* |
| J7 | Contexto imediato, sem ambiguidade | pontuada | claude | todos | 10 | Lida uma vez, em voz alta, por alguém que não conhece a marca: dá para dizer do que se trata já na 1ª frase, sem reler e de um jeito só? Jargão sem tradução (sinal amarelo V16 de `vicios-ia.md`), duas ideias na mesma frase ou palavra com dois sentidos derrubam. | `02-ganchos.md`, "o gancho é uma resposta de orientação" (do que se trata, em ~1,5 s) **[criador]**; princípios *rapid context*, *clarity* e *absorption rate* do prompt Hook Machine (Kallaway) **[criador]**; `10-voz.md` §3 (jargão entra traduzido na mesma frase) |
| B1 | Âncora de prova na 2ª camada | bonus | claude | todos | 5 | O apoio (capa) ou a tela (Reel) traz uma prova que sustenta a 1ª camada: número medido, a fonte, o arquivo, o resultado. Soma até 5 pontos e nunca tira: gancho sem âncora não perde nada. A nota final não passa de 100. | *credibility anchor (bonus)* do Hook Machine (Kallaway) **[criador]**: "não penalize quem pula; recompense quem inclui bem"; G3 de `02-ganchos.md` (tela `1.250 metros, medidos em 2017`) é o caso da casa |
| C1 | Foto e manchete se completam | pontuada | claude | capa | 6 | Cubra a manchete: a foto sozinha diz do que se trata? Cubra a foto: a manchete não descreve a foto, acrescenta a ela? | Teste 1 de `02-ganchos.md` adaptado à capa **[criador]** *(leitura minha: transferência de Reel para carrossel)*. Diretriz do cliente de 07/10/2026: "todo slide tem imagem planejada" (`canastra-carrossel`) **[medido]** |
| C2 | A capa pede o arraste | pontuada | claude | capa | 4 | Termina aberta: pergunta, ou afirmação cuja prova está nos slides seguintes. Capa que já entrega tudo falha. | `canastra-carrossel`: capa é "a pergunta ou a afirmação que faz arrastar". A fórmula do Coffee++ (capa com pergunta) em `01-concorrencia.md` **[criador]** |
| R1 | O frame a 0,5 s faz sentido sozinho | pontuada | claude | reel | 10 | Congele em meio segundo, sem som: dá para dizer do que se trata? | `02-ganchos.md` Teste 1 **[criador]**; 35,2% dos virais sem texto na abertura, ou seja, a imagem é o gancho **[medido]** |

Soma: **capa** = 24 (M) + 66 (J) + 10 (C) = 100 · **reel** = 24 + 66 + 10 (R) = 100. Bônus B1: até +5, teto 100.

**Nota mínima para mostrar um gancho gerado: 70** (`NOTA_MINIMA` em `scripts/ganchos.py`). Abaixo disso, reescreva
antes de mostrar. Gancho do Rafael é avaliado como está, sem piso.

---

## O que ficou fora, e por quê

- **"Fala com você" (você/seu/sua).** Estava no plano como M5. O corpus derrubou: só 11,8% das
  aberturas pt usam a segunda pessoa **[medido]**. A diretriz do cliente ("você e a gente") vale
  para a **copy do carrossel inteiro**, não é regra de gancho. Ver `canastra-carrossel`.
- **"Comece com pergunta".** Só 13,7% das aberturas pt são pergunta **[medido]**. Pergunta é um
  dos padrões (`pergunta-diagnostico`), não uma regra.
- **Rosto nos 3 primeiros segundos.** O +10% é **[terciário]** (`02-ganchos.md`). É hipótese de
  teste, nunca regra.

---

## Exemplos por regra

Passa / falha, tirados do corpus, do banco G1–G15 ou dos nossos carrosséis.

| id | passa | falha |
|---|---|---|
| P1 | "O microlote custa quatro reais a mais" com `--fonte "tabela de 11/09/2026"` | o mesmo, sem fonte; "três vezes mais caro" (não medido) |
| P2 | "Café na geladeira não conserva" | "O cheiro da torra age no seu cérebro" |
| P3 | "Edição limitada: 12 sacas desta safra" com `--fonte` do registro da safra | "O café mais premiado de Minas" |
| P4 | "Tem casca no seu café?" → o slide 2 diz o que é a película | "Fica até o final que tem uma surpresa" |
| M1 | "Tem casca no seu café?" (5 palavras, 22 caracteres) | "41 anúncios vendem 'Canastra' no Mercado Livre. Nenhum deles é nosso." (11 palavras, passa de 9) |
| M2 | fala "O GPS da foto provou a altitude." / tela "1.250 metros, medidos em 2017" | G9 original: tela = 2ª frase da fala |
| M3 | "Não é chafé." na tela, ou "Não é CHAFÉ!" falado (@cafegeracoes, 5,5 mi): a negação é o veredito, não a fórmula "não é só X, é Y" | "Não é só café, é uma experiência"; "Não é CHAFÉ!" na tela (V13, exclamação) |
| M4 | "Hoje eu vou tirar o boia desse café, galera." passa: "hoje eu vou" + **ação concreta** não é anúncio de tema. O regex só pega "hoje eu vou falar". | "Bom dia! Hoje eu vou falar sobre a nossa colheita" |
| J1 | "Como separar o café de qualidade do café inferior" (@tulianelenk, 21,1 mi) → "como?" | "Você não vai acreditar no que achamos na lavoura" |
| J2 | "O que a peneira tira do seu café" | "Como funciona a nossa secagem" |
| J3 | "Ambos são o mesmo café." sobre dois filtros diferentes (@terracruzcafes, 8,6 mi) | "Nosso café é especial" |
| J4 | "Coffee is 98.5% water" sobre água caindo no copo (2,1 mi) | "Qualidade que você sente na xícara" |
| J5 | "Se chover em cima da colheita, esse lote desce de categoria" | "Quatro contas usam o nome Canastra" (concorrente nomeado, fica com o dono) |
| J6 | `quem-faz-mostra`: "Essa aqui é a via úmida do café." (@_gabriel_dcafe, 4,0 mi) | `marca-clima`: "Um sinal para desacelerar com o nosso Drip Coffee" (@orfeucafes, 0,5 mi) |
| J7 | "Dá para saber se o café é especial sem provar." (do que se trata: café especial) | "Essa caixinha no pacote é o nosso boletim." (que caixinha? boletim de quê?); "Café de via úmida tem outro gosto" (jargão a frio) |
| B1 | apoio "Fizemos a conta com o preço de setembro." sob "Quanto custa uma xícara do nosso café?" | (não há falha: sem âncora, só não ganha o bônus) |
| C1 | foto da lasquinha clara no pó + "Tem casca no seu café?" | foto de lavoura genérica + "Tem casca no seu café?" (a foto não mostra a casca) |
| C2 | "41 anúncios vendem 'Canastra'. Nenhum deles é nosso." → arrasta para ver a prova | "Café especial é aquele com nota acima de 80 pela SCA." (já entregou) |
| R1 | duas cerejas na mesma mão, verde e vermelha | pessoa respirando antes de falar; logo animado |
