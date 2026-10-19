# Pesquisa diária do Instagram: modelo do briefing

Quem lê este arquivo: o turno de pesquisa das **3h** (Sonnet), que grava o briefing do dia, e o turno
das **7h**, que lê só o briefing. O resultado de cada dia é `instagram/pesquisa/briefing-AAAA-MM-DD.md`.
Exemplo real: `briefing-2026-10-13.md` (seis itens, cada um com número e URL, e a parte "não verificado"
dita logo no topo).

## O que existe nesta pasta

| O que | Vida | Para que serve |
|---|---|---|
| `briefing-AAAA-MM-DD.md` | **permanente**, nunca apague | o destilado do dia; é o que o turno das 7h lê |
| `bruto/AAAA-MM-DD/` | **5 dias**, depois é apagado pelo fechamento das 19h | páginas, listas, recortes e links colhidos. Não é memória: não leia depois de gravar |

## Aviso: às 3h não há navegador logado

A tela do PC está bloqueada e o Chrome não renderiza. **Não use o Claude in Chrome neste turno.** Só
busca na web aberta, sem login. Tudo que exige conta logada (áudio em alta do Instagram, Stories de
concorrente, insights do perfil, volume real de hashtag, perfis de concorrente que pedem login) **não é
seu trabalho**: escreva `NÃO VERIFICADO` no topo do briefing, listando o que ficou de fora, para o turno
da manhã completar. Não preencha esses itens com suposição.

## Formato do briefing

Primeira linha: `# Briefing AAAA-MM-DD (dia da semana)`. Logo abaixo, uma linha dizendo o que foi busca
aberta e o que ficou NÃO VERIFICADO.

**No máximo 10 itens**, ordenados do que mais muda o dia para o que menos muda. Cada item, nesta ordem:

```
## N. Título curto e factual
- Sinal: uma linha. O que está acontecendo.
- Evidência: o número e a fonte. https://url-da-fonte
- Importa: por que isto importa para a Canastra (pilares da Direcao-Criativa.md), em 1 ou 2 frases.
- Ação: o que sugerir ao dono, concreto (pauta, legenda, pergunta a fazer). Pode ser "só acompanhar".
```

Regras de cada campo:

- **Evidência tem número e URL.** Sem os dois, o item não entra. Número que veio de resumo de busca e
  não de abrir a página: diga ("números de resumo de busca; o link leva à fonte").
- **Importa** liga ao posicionamento da marca. Se não consegue ligar, o item não é relevante: corte.
- **Ação** é sugestão, não decisão. Quem decide é o dono.
- Dúvida sobre fato vira `não verificado`, escrito, nunca omitido.

## A regra: "nada relevante hoje"

Se a pesquisa não achou nada que mude o dia, grave o briefing contendo **só a frase literal**:

> nada relevante hoje

e termine o turno normalmente, com o marcador `[[BRIEFING: <caminho>]]`. É uma saída honesta, esperada e
boa. Ela existe porque, sem uma saída explícita, o modelo **inventa tendência** para não entregar
vazio, e um briefing inventado faz o dono produzir em cima de nada. Cinco itens verdadeiros valem mais
que dez com enchimento; zero também vale.

## Dedupe: os 7 briefings anteriores

Antes de gravar, leia (só se existirem) os `briefing-*.md` dos **7 dias anteriores**. **Não repita** um
item que já saiu, nem com outras palavras. Só reaparece se houver fato novo, e então escreva o que
mudou ("atualização: a premiação saiu, venceu X"). Sem isso o briefing vira o mesmo texto todo dia.

## Orçamento

O turno tem um teto de minutos e de fontes consultadas, dados no prompt. Chegou em qualquer um: grave o
que tem e termine. Um briefing parcial serve; um turno travado não. Marque `pesquisa parcial` no topo.
Salve o bruto direto em arquivo e traga para a conversa só o trecho e o número que vai usar.
