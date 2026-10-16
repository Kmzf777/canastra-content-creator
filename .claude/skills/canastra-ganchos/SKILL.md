---
name: canastra-ganchos
description: Use when writing, choosing, scoring or approving a Café Canastra hook — gancho, capa de carrossel, manchete do slide 1, primeira frase de Reel, texto de tela, "dar nota a um gancho", "esse gancho está bom?", "me dá opções de gancho", aprovação de pauta — or when a hook sounds like AI copy and needs to be rewritten from data.
---

# Ganchos: gerar e dar nota com base em dado

Esta skill decide **a primeira coisa que a pessoa vê**: a manchete da capa do carrossel ou a
1ª frase, a tela e o frame do Reel. A nota sai de uma rubrica de 17 regras tirada de 128
ganchos virais reais, e não do gosto de quem escreve.

| Arquivo | Para quê |
|---|---|
| [rubrica.md](rubrica.md) | **as 17 regras**, peso, como verificar e de onde veio cada uma |
| [vicios-ia.md](vicios-ia.md) | o léxico que denuncia texto de IA, com a incidência medida nos virais |
| `instagram/ganchos/padroes.md` | os 9 padrões do corpus, com n, mediana de views e exemplos literais |
| `scripts/ganchos.py` | `checar` (rubrica), `extrair`, `padroes`, `recalibrar` |

## Rotear primeiro

| Assunto | Dono |
|---|---|
| a manchete/frase, a nota, as alternativas | **esta skill** |
| tipos de slide, ritmo do deck, portões de render | `canastra-carrossel` |
| formato do vídeo, roteiro depois do gancho, edição | `canastra-video` |
| a foto da capa (chão, luz, prop) | `canastra-direcao` + `canastra-cena` |
| número ou alegação: de onde vem | `instagram/estrategia/02-ganchos.md`, "A regra de sourcing" |

---

## Modo 1: gerar ganchos para um tema

Entrada: **tema**, **formato** (`capa` ou `reel`) e a **matéria-prima que existe** (foto real,
número medido, arquivo). Se não souber o que existe, procure antes. Gancho sem matéria-prima é
lista de desejos (`02-ganchos.md`, "Como usar este banco").

1. **Junte os fatos citáveis** do tema, cada um com a fonte (arquivo, tabela, medição). Fato
   sem fonte não entra em gancho nenhum (P1).
2. **Escreva 8 a 10 candidatos de padrões diferentes.** Use os 7 padrões que transferem
   (J6): `veredito-direto`, `pergunta-diagnostico`, `resultado-antes`, `quem-faz-mostra`,
   `acao-em-curso`, `situacao-reconhecivel`, `conflito-resposta`. Dez variações da mesma frase
   não é gerar, é parafrasear. Para cada um, descreva em uma linha **a foto da capa** (ou o
   frame 1), porque C1 e R1 julgam o par.
3. **Rode `checar` em todos**, antes de julgar:

   ```bash
   python scripts/ganchos.py checar --formato capa --manchete "..." --apoio "..." --fonte "..."
   python scripts/ganchos.py checar --formato reel --fala "..." --tela "..."
   ```

   Corte quem reprovou em portão. Quem falhou em M3 (vício de IA), reescreva, não defenda.
4. **Julgue as regras `claude`** (P4, J1–J6, C1–C2 ou R1), com **uma linha de motivo por
   regra**. J1 exige escrever a pergunta exata que a pessoa faz depois de ler. P4 exige
   apontar o slide que paga a promessa.
5. **Calcule a nota pelo script**, passando os julgamentos, e registre os finalistas:

   ```bash
   python scripts/ganchos.py checar --formato capa --manchete "..." --fonte "..." \
     --julgamento P4=1,J1=1,J2=1,J3=0,J4=1,J5=1,J6=1,C1=1,C2=1 --registrar --tema "<tema>"
   ```

   A nota é a do script, nunca uma estimada de cabeça.
6. **Entregue os 3 melhores** no formato da resposta abaixo.

## Modo 2: dar nota a um gancho do Rafael e propor alternativas

1. `checar` + julgamento: a nota decomposta regra por regra.
2. Nomeie **as 2 regras de maior peso que falharam**: é ali que está o ganho.
3. Escreva **3 alternativas**, cada uma consertando uma das regras falhas sem quebrar as que
   passavam. Rode as três no `checar` com julgamento e registre.
4. Mostre só alternativas com nota **maior** que a original. Se nenhuma superar, diga isso e
   explique por que o original já está bom. Não force troca.
5. Preserve a voz dele: mude a mecânica, não o vocabulário que ele escolheu.

## Formato da resposta

Para cada gancho apresentado:

```
**[nota]/100 · padrão** — manchete / apoio (ou fala / tela)
Foto: <a foto da capa ou o frame 1, em uma linha; real ou a gerar>
Pergunta que abre: "<a pergunta exata de J1>"
Paga em: <slide ou segundo de P4>
Fonte dos números: <arquivo> · Matéria-prima: existe | falta (<o quê>)
Perdeu pontos em: <ids e uma linha cada>
```

E uma linha final dizendo **qual você escolheria e por quê**. A nota é hipótese, não
previsão: diga "nota 86, hipótese para testar", nunca "vai performar" (`03-roteiro.md` §5).

---

## Não soar como IA

Leia [vicios-ia.md](vicios-ia.md) antes de escrever. O resumo medido:

- As construções de copy de IA aparecem em **0 a 1 dos 128 virais**. O viral **mostra a
  coisa** e fala dela com palavra de conversa.
- **Pergunta (13,7%), número (11,8%) e "você" (11,8%) são minoria** nas aberturas pt. Não abra
  com pergunta por reflexo.
- **Um terço não tem texto nenhum** na abertura: a foto é o gancho. Escolha a foto antes da
  frase.
- **Teste de troca de marca:** se a frase funcionaria igual com o nome de outra marca de café,
  ela é genérica. Troque o substantivo pelo objeto que só a Canastra tem (o GPS de 2017,
  `Desde 1985`, a tabela de 11/09, a lasquinha no pó).

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

**A rubrica só muda com o Rafael aprovando.** Por isso **todo gancho publicado precisa estar em
`avaliacoes.jsonl` com `--escolhido`**: sem o registro, o post não cruza e a recalibração não
aprende com ele.

## Limites (diga-os quando a nota for usada para decidir)

- O corpus é **só de vencedores** e **só de Reel**. Ele mostra o que os virais têm em comum,
  não o que separa viral de fracasso. As regras de capa (C1, C2) são transferência do Reel
  *(leitura minha)* até a recalibração medir carrossel.
- Views lidas da grade podem incluir mídia paga.
- As regras `claude` são julgamento. Duas sessões podem discordar em J2 ou J3; a linha de
  motivo existe para a discordância ser discutível.
