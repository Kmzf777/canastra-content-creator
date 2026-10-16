# Vícios de texto de IA

Fonte única do léxico que a regra **M3** da [rubrica](rubrica.md) aplica. `scripts/ganchos.py`
lê a tabela abaixo: a coluna `regex` é a busca (sem diferenciar maiúscula) e a coluna `proibe`
decide o que acontece com ela.

- `sim`: casou em qualquer camada do gancho → M3 falha.
- `medir`: só conta no corpus. Se os virais usam a construção, ela é **padrão**, não vício,
  e proibir seria proibir o que funciona.

A incidência é a contagem de ganchos do corpus (`instagram/ganchos/corpus.jsonl`, 128
virais) em que a construção aparece na **abertura** (1ª tela citada + 1ª frase falada).
Atualize com `python scripts/ganchos.py medir`.

| id | vício | regex | proibe | incidência pt / en / total | fonte |
|---|---|---|---|---|---|
| V1 | "não é só X, é Y" | `\bn[ãa]o [ée] (s[óo]|apenas)\b|\bnot just\b` | sim | 0 / 0 / 0 | **[medido]** 0 de 128 virais; **[leitura minha]**: é a construção que modelo de linguagem mais repete em copy de marca |
| V2 | "mais do que um…" | `\bmais (do )?que (um|uma|s[óo]|apenas)\b|\bmore than (just )?a\b` | sim | 0 / 0 / 0 | **[medido]** 0 de 128; **[leitura minha]** idem V1 |
| V3 | travessão de redação | `—` | sim | 1 / 0 / 1 | **[medido]** 1 de 128, e é um print de resposta a comentário, não redação do criador; **[leitura minha]**: travessão é assinatura de texto gerado em pt-BR |
| V4 | léxico de folheto | `\b(descubra|desvende|mergulhe|embarque|jornada|experi[êe]ncia [úu]nica|transforme|eleve|desperte|ess[êe]ncia|universo d[eo]|feito com amor|momento especial|apaixonad[oa]s? por)\b` | sim | 1 / 0 / 1 | **[medido]** 1 de 128 (@_victorzk, "apaixonado por ferramentas", fala espontânea); a lista de palavras é **[leitura minha]** |
| V5 | adjetivo de vitrine | `\b(incr[íi]vel|surpreendente|fascinante|impressionante|sensacional|perfeit[oa])\b` | sim | 0 / 0 / 0 | **[medido]** 0 de 128; o adjetivo diz que é bom em vez de mostrar por quê, o que contradiz J4 |
| V6 | abertura "Imagine" / "Prepare-se" | `^\W*(imagine|prepare-se)\b|voc[êe] precisa (conhecer|provar)` | sim | 0 / 0 / 0 | **[medido]** 0 de 128 |
| V7 | "Você sabia que" | `\bvoc[êe] sabia\b|\bdid you know\b` | medir | 0 / 0 / 0 | **[medido]** 0 de 128 virais abrem com "você sabia". Fica `medir` porque a série A da agenda usa o nome e nenhuma fonte além do corpus o reprova: trate como **sinal amarelo**, e o gancho tem que se sustentar sem a muleta |
| V8 | "segredo / ninguém te conta" | `segredo|ningu[ée]m (te )?(conta|fala)|secret` | medir | 0 / 0 / 0 | **[medido]** a palavra não aparece na abertura de nenhum, embora 7 fichas tenham a etiqueta `segredo` (o segredo é mostrado, não anunciado) |
| V9 | emoji de brilho | `[✨🚀💫🌟]` | medir | 1 / 0 / 1 | **[medido]** 1 de 128 (@amandabaristaa, ✨ no fim de legenda de vida real) |

## O que o corpus diz sobre soar humano

Medido sobre as aberturas dos 51 virais em português (`instagram/ganchos/padroes.md`):

- **Quase nenhum anuncia.** As construções da tabela somam 3 ocorrências em 128 ganchos, e
  nenhuma é redação de marca. O viral **mostra a coisa** e fala dela com palavra de
  conversa: "Gambiarras do café: sem moedor? Um mixer…", "Não é CHAFÉ!",
  "Hoje eu vou tirar o boia desse café, galera".
- **Pergunta e número são minoria.** Pergunta em 13,7% e número em 11,8% das aberturas pt.
  Gancho de IA costuma abrir com pergunta retórica, e o corpus não sustenta esse reflexo.
- **"Você" é minoria também:** 11,8% em pt. O endereçamento direto não é o que segura.
- **Um terço não tem texto nenhum** na abertura, nem lido nem ouvido (35,2% do total;
  40% no top 25 de views contra 30% no resto): a imagem faz o gancho sozinha. Por isso C1
  e R1 pesam.

Três instruções de escrita que saem disso:

1. Escreva como quem está **mostrando** algo a alguém do lado: sujeito concreto, verbo no
   presente, sem adjetivo de avaliação.
2. Uma palavra de registro oral vale mais que uma palavra bonita: "chafé", "tirar o boia",
   "lasquinha" e "pacote" ganham de "experiência", "notas sensoriais" e "universo".
3. Se a frase funcionaria igual para qualquer marca de café, ela é de IA. Troque o
   substantivo genérico pelo objeto que só a Canastra tem: o GPS de 2017, o `Desde 1985`,
   a tabela de 11/09.
