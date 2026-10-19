---
name: canastra-ganchos
description: Use when writing, choosing, scoring or approving a Café Canastra hook — gancho, capa de carrossel, manchete do slide 1, primeira frase de Reel, texto de tela, "dar nota a um gancho", "esse gancho está bom?", "me dá opções de gancho", aprovação de pauta — or when a hook sounds like AI copy and needs to be rewritten from data.
---

# Ganchos: gerar e dar nota com base em dado

Esta skill decide **a primeira coisa que a pessoa vê**: a manchete da capa do carrossel ou a
1ª frase, a tela e o frame do Reel. A nota sai de uma rubrica de 18 regras e 1 bônus, tirada de
128 ganchos virais reais, e não do gosto de quem escreve.

| Arquivo | Para quê |
|---|---|
| [rubrica.md](rubrica.md) | **as 18 regras e o bônus**, peso, como verificar e de onde veio cada uma |
| [vicios-ia.md](vicios-ia.md) | o léxico que denuncia texto de IA, com a incidência medida nos virais |
| `instagram/ganchos/padroes.md` | os 9 padrões do corpus: n, perfis, mediana de views com e sem suspeitos de impulsionamento, e as **fórmulas de lacuna** de cada padrão |
| `scripts/ganchos.py` | `checar` (rubrica), `ranking`, `escolher` (o publicado), `contrastar`, `extrair`, `padroes`, `recalibrar` |

## Rotear primeiro

| Assunto | Dono |
|---|---|
| a manchete/frase, a nota, as alternativas | **esta skill** |
| tipos de slide, ritmo do deck, portões de render | `canastra-carrossel` |
| formato do vídeo, roteiro depois do gancho, edição | `canastra-video` |
| a foto da capa (chão, luz, prop) | `canastra-direcao` + `canastra-cena` |
| número ou alegação: de onde vem | `instagram/estrategia/02-ganchos.md`, "A regra de sourcing" |
| **para quem** (o anel do assunto) | `instagram/estrategia/09-publico.md` |
| **como a marca fala** (registro, palavras proibidas, pontuação) | `instagram/estrategia/10-voz.md` |
| por que um gancho prende (lacuna, especificidade, linha que vende a seguinte) | skill `content-principles`, **só como referência geral** |

> **Precedência:** a `content-principles` (skill de usuário, de terceiro) entra abaixo de tudo
> aqui. A rubrica, o banco de ganchos, a regra de sourcing, o `09-publico.md` (é ele quem diz
> quem é o espectador, sem perguntar) e o `10-voz.md` vencem. Os números dela (frase de menos
> de 9 palavras, nova dúvida a 60–70%) não têm fonte e não viram meta nem regra da nota.

---

## Modo 1: gerar ganchos para um tema

Entrada: **tema**, **formato** (`capa` ou `reel`) e a **matéria-prima que existe** (foto real,
número medido, arquivo). Se não souber o que existe, procure antes. Gancho sem matéria-prima é
lista de desejos (`02-ganchos.md`, "Como usar este banco").

0. **Decida o anel** pelo teste da troca de logo (`09-publico.md` §2) e confira se ele é o
   que o mix da semana pede (§3: toda semana um anel 1; a outra peça alterna entre anel 2 ou
   3 e anel 4). O banco de `02-ganchos.md` tem **0 ganchos no anel 4**: quando a vaga for de
   anel 4, escreva para ela, não empurre um gancho de anel 1.
1. **Junte os fatos citáveis** do tema, cada um com a fonte (arquivo, tabela, medição). Fato
   sem fonte não entra em gancho nenhum (P1).
2. **Escreva 8 a 10 candidatos de padrões diferentes**, partindo das **fórmulas de lacuna** de
   `padroes.md` (cada uma saiu de um vencedor) e também de frases escritas do zero. Dez
   variações da mesma frase não é gerar, é parafrasear. Antes de preencher uma fórmula, passe
   pelo **filtro de compatibilidade**. Qualquer "não" corta a fórmula para este tema:
   - **Estrutura:** a fórmula aceita este tema? Se ela pede número e o tema não tem número
     medido, preencher seria inventar (P1). Corte.
   - **Tom:** a energia da fórmula combina com o tema? Alarme num tema de ritual não combina,
     e drama fabricado reprova em J5.
   - **Voz alta:** lida em voz alta, com as palavras do tema nas lacunas, soa como alguém da
     casa falando? Se tropeça, pede releitura ou só funciona escrita, corte. **Este é o filtro
     que mais importa.**

   Se só 3 fórmulas passarem, use 3. Não encha com encaixe ruim. Para cada candidato,
   descreva em uma linha **a foto da capa** (ou o frame 1), porque C1 e R1 julgam o par.
3. **Rode `checar` em todos**, antes de julgar:

   ```bash
   python scripts/ganchos.py checar --formato capa --manchete "..." --apoio "..." --fonte "..."
   python scripts/ganchos.py checar --formato reel --fala "..." --tela "..."
   ```

   Corte quem reprovou em portão. Quem falhou em M3 (vício de IA), reescreva, não defenda.
4. **Julgue as regras `claude`** (P4, J1–J7, C1–C2 ou R1, e o bônus B1), com **uma linha de
   motivo por regra**. J1 exige escrever a pergunta exata que a pessoa faz depois de ler. J7
   exige ler em voz alta, como quem não conhece a marca: se a 1ª frase deixa dúvida do que se
   trata, ou tem jargão sem tradução (o `checar` marca como sinal amarelo V16), falha. P4 exige
   apontar o slide que paga a promessa.
5. **Calcule a nota pelo script**, passando os julgamentos, e registre os finalistas:

   ```bash
   python scripts/ganchos.py checar --formato capa --manchete "..." --fonte "..." \
     --julgamento P4=1,J1=1,J2=1,J3=0,J4=1,J5=1,J6=1,J7=1,C1=1,C2=1,B1=0 --registrar --tema "<tema>"
   ```

   A nota é a do script, nunca uma estimada de cabeça. Se houver prova na 2ª camada (apoio ou
   tela com número medido, fonte, arquivo), julgue também `B1=1`: é bônus, soma até 5 e nunca
   tira.
6. **Nota mínima: 70** (`NOTA_MINIMA`). Gancho gerado abaixo disso **não é mostrado**: reescreva
   atacando a regra de maior peso que falhou e rode de novo. O `checar` avisa quando a nota fica
   abaixo do mínimo.
7. **Entregue os 3 melhores** no formato da resposta abaixo. `python scripts/ganchos.py ranking
   --tema "<tema>"` lista todos os registrados do tema, da maior nota para a menor.

## Modo 2: dar nota a um gancho do Rafael e propor alternativas

1. `checar` + julgamento, **registrando com o mesmo `--tema`** dos gerados: a nota decomposta
   regra por regra, sem inflar. O valor está na nota honesta, não em agradar.
2. **Ranqueie junto:** `python scripts/ganchos.py ranking --tema "<tema>"` mostra em que posição o
   gancho dele cai entre os gerados. Mostre essa posição.
3. Nomeie **as 2 regras de maior peso que falharam**: é ali que está o ganho.
4. Escreva **3 alternativas com abordagens diferentes**, não três variações do mesmo conserto:
   - uma que **muda a estrutura** (outro padrão ou outra fórmula);
   - uma que **reformula a promessa** (o que a pessoa ganha);
   - uma que **acrescenta prova ou especificidade** (número medido, a fonte, o objeto, que
     costuma render o bônus B1).

   Rode as três no `checar` com julgamento e registre no mesmo tema. Cada uma vem com uma
   linha de "por que é mais forte".
5. Mostre só alternativas com nota **maior** que a original. Se nenhuma superar, diga isso e
   explique por que o original já está bom. Não force troca.
6. Preserve a voz dele: mude a mecânica, não o vocabulário que ele escolheu.

## Formato da resposta

Para cada gancho apresentado:

```
**[nota]/100 · padrão · anel N** — manchete / apoio (ou fala / tela)
Foto: <a foto da capa ou o frame 1, em uma linha; real ou a gerar>
Pergunta que abre: "<a pergunta exata de J1>"
Paga em: <slide ou segundo de P4>
Fonte dos números: <arquivo> · Matéria-prima: existe | falta (<o quê>)
Perdeu pontos em: <ids e uma linha cada>
```

E uma linha final dizendo **qual você escolheria e por quê**. A nota é hipótese, não
previsão: diga "nota 86, hipótese para testar", nunca "vai performar" (`03-roteiro.md` §5).

---

## Não soar como IA, e soar como a Canastra

Leia [vicios-ia.md](vicios-ia.md) e o checklist de 6 perguntas de `10-voz.md` §10 antes de
escrever. M3 já reprova as palavras e a pontuação que a voz recusa: *gourmet*, *premium*,
*segredo*, fogo/queimar, voz institucional, e na tela nenhuma exclamação, emoji ou
reticências. *Perfeito* e *experiência* o cliente manteve. O resumo medido:

- As construções de copy de IA aparecem em **0 a 1 dos 128 virais**. O viral **mostra a
  coisa** e fala dela com palavra de conversa.
- **Pergunta (13,7%), número (11,8%) e "você" (11,8%) são minoria** nas aberturas pt. Não abra
  com pergunta por reflexo.
- **Um terço não tem texto nenhum** na abertura: a foto é o gancho. Escolha a foto antes da
  frase.
- **Teste de troca de marca:** se a frase funcionaria igual com o nome de outra marca de café,
  ela é genérica. Troque o substantivo pelo objeto que só a Canastra tem (o GPS de 2017,
  `Desde 1985`, a tabela de 11/09, a lasquinha no pó).

## Contraste vencedores × perdedores

O corpus da rubrica só tem vencedores. Para ver o que separa um post bom de um ruim **dentro de um
mesmo perfil**:

```bash
python scripts/ganchos.py contrastar            # grava instagram/ganchos/contraste-AAAA-MM-DD.md
```

- **Entrada:** `instagram/metricas/concorrentes/*.jsonl` e `proprios.jsonl`, do fluxo 1.
- **Corte:** a grade inteira de cada perfil é cortada pela **mediana do próprio perfil**, não
  pela média, e cada perfil é lido sozinho antes do cruzamento.
- **Limite:** para concorrente, o gancho é a 1ª linha da legenda, porque a API não dá o texto da
  capa. É hipótese para levar ao Rafael, não peso novo.

## Recalibração com resultado real

Quando o fluxo 1 gravar `instagram/metricas/proprios.jsonl` com o campo `gancho` preenchido
**com o texto exato da manchete ou da fala**:

```bash
python scripts/ganchos.py recalibrar
```

O script cruza cada post com a avaliação registrada, mede (saves + shares) / alcance, ou
tempo médio assistido no Reel, e compara quem passou com quem falhou em cada regra.

- Com **menos de 8 posts** cruzados por formato, não propõe nada.
- Com 8 ou mais, grava `instagram/ganchos/recalibracao-AAAA-MM-DD.md` com pesos propostos
  (±50% no máximo).

**A rubrica só muda com o Rafael aprovando.** E **todo gancho publicado precisa ser marcado**:

```bash
python scripts/ganchos.py escolher --texto "<texto exato>" --post <shortcode>   # --formato reel no Reel
```

O `escolher` copia a avaliação da pauta com `escolhido: true` e o shortcode. Sem a marca, o post
só cruza pelo texto, e a recalibração perde a garantia de qual avaliação era a publicada.

## Limites (diga-os quando a nota for usada para decidir)

- O corpus é **só de vencedores** e **só de Reel**. Ele mostra o que os virais têm em comum,
  não o que separa viral de fracasso. As regras de capa (C1, C2) são transferência do Reel
  *(leitura minha)* até a recalibração medir carrossel.
- Views lidas da grade podem incluir mídia paga. `padroes.md` **sinaliza** os suspeitos (ficha
  `provavel-pago`, ou curtidas/views abaixo de 1/3 da mediana do corpus) e mostra a mediana com
  e sem eles. Não exclui ninguém.
- J6 não premia padrão de um criador só: padrão em que um perfil tem metade ou mais dos casos
  não conta.
- As regras `claude` são julgamento. Duas sessões podem discordar em J2 ou J3; a linha de
  motivo existe para a discordância ser discutível.
