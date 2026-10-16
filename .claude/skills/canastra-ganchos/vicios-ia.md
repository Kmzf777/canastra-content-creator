# Vícios de texto de IA, e as palavras que a voz da marca recusa

Fonte única do léxico que a regra **M3** da [rubrica](rubrica.md) aplica. `scripts/ganchos.py`
lê a tabela abaixo: a coluna `regex` é a busca (sem diferenciar maiúscula), `proibe` decide o
que acontece e `onde` diz em que camada ela vale.

- `proibe = sim`: casou → M3 falha. `medir`: só conta no corpus. Se os virais usam a
  construção, ela é **padrão**, não vício, e proibir seria proibir o que funciona.
- `onde = todas`: manchete, apoio, fala e tela. `onde = tela`: só o que se **lê** (manchete e
  apoio da capa, tela do Reel). A fala não tem exclamação nem emoji.

Duas fontes, e elas não se confundem:

1. **V1–V9, vícios de IA:** a incidência no corpus de 128 virais é o lastro **[medido]**.
2. **V10–V15, voz da marca:** são decisões do cliente registradas em
   `instagram/estrategia/10-voz.md` §6–§7, de 15/10/2026. Valem mesmo quando os virais fazem
   diferente (o viral "Não é CHAFÉ!" tem exclamação, e na tela da Canastra ela não entra).

**O cliente manteve** *excelência*, *perfeito*, *terroir*, *blend*, *artesanal* e
*experiência* (`10-voz.md` §6). Por isso nenhuma delas está proibida aqui sozinha.
"Experiência única" é proibida como **expressão de folheto** (V4), não pela palavra.

A incidência é a contagem de ganchos do corpus (`instagram/ganchos/corpus.jsonl`) em que a
construção aparece na **abertura** (1ª tela citada + 1ª frase falada); para `onde = tela`,
só na tela. Atualize com `python scripts/ganchos.py medir`.

| id | vício | regex | proibe | onde | incidência pt / en / total | fonte |
|---|---|---|---|---|---|---|
| V1 | "não é só X, é Y" | `\bn[ãa]o [ée] (s[óo]|apenas)\b|\bnot just\b` | sim | todas | 0 / 0 / 0 | **[medido]** 0 de 128 virais; **[leitura minha]**: é a construção que modelo de linguagem mais repete em copy de marca |
| V2 | "mais do que um…" | `\bmais (do )?que (um|uma|s[óo]|apenas)\b|\bmore than (just )?a\b` | sim | todas | 0 / 0 / 0 | **[medido]** 0 de 128; **[leitura minha]** idem V1 |
| V3 | travessão de redação | `—` | sim | todas | 1 / 0 / 1 | **[medido]** 1 de 128, e é um print de resposta a comentário, não redação do criador; **[leitura minha]**: travessão é assinatura de texto gerado em pt-BR |
| V4 | léxico de folheto | `\b(descubra|desvende|mergulhe|embarque|jornada|experi[êe]ncia [úu]nica|transforme|eleve|desperte|ess[êe]ncia|universo d[eo]|feito com amor|momento especial|apaixonad[oa]s? por)\b` | sim | todas | 1 / 0 / 1 | **[medido]** 1 de 128 (@_victorzk, "apaixonado por ferramentas", fala espontânea); a lista de palavras é **[leitura minha]** |
| V5 | adjetivo de vitrine | `\b(incr[íi]vel|surpreendente|fascinante|impressionante|sensacional)\b` | sim | todas | 0 / 0 / 0 | **[medido]** 0 de 128; o adjetivo diz que é bom em vez de mostrar por quê, o que contradiz J4. *perfeito* saiu da lista porque o cliente o manteve (`10-voz.md` §6) |
| V6 | abertura "Imagine" / "Prepare-se" | `^\W*(imagine|prepare-se)\b|voc[êe] precisa (conhecer|provar)` | sim | todas | 0 / 0 / 0 | **[medido]** 0 de 128 |
| V7 | "Você sabia que" | `\bvoc[êe] sabia\b|\bdid you know\b` | medir | todas | 0 / 0 / 0 | **[medido]** 0 de 128 virais abrem com "você sabia". Fica `medir` porque a série A da agenda usa o nome e nenhuma fonte além do corpus o reprova: trate como **sinal amarelo**, e o gancho tem que se sustentar sem a muleta |
| V8 | "segredo / ninguém te conta" | `segredo|ningu[ée]m (te )?(conta|fala)|secret` | sim | todas | 0 / 0 / 0 | **[medido]** a palavra não aparece na abertura de nenhum, embora 7 fichas tenham a etiqueta `segredo` (o segredo é mostrado, não anunciado). **Proibida** pela voz da marca: `10-voz.md` §6, "segredo" e suspense no gancho |
| V9 | emoji de brilho | `[✨🚀💫🌟]` | medir | todas | 1 / 0 / 1 | **[medido]** 1 de 128 (@amandabaristaa, ✨ no fim de legenda de vida real) |
| V10 | categoria de gôndola | `\b(gourmet|premium)\b` | sim | todas | 0 / 0 / 0 | decisão do cliente, `10-voz.md` §6. O rótulo da cápsula traz GOURMET impresso, e a regra vale para o texto que a gente escreve |
| V11 | torra como fogo | `\b(fogo|queim\w*|tostar)\b|🔥` | sim | todas | 0 / 0 / 0 | `10-voz.md` §6 e lição 66 do `CLAUDE.md`: o público lê torra escura como café queimado |
| V12 | voz institucional | `\b(a empresa|nossa marca|prezad[oa] cliente)\b` | sim | todas | 0 / 0 / 0 | `10-voz.md` §2 e §6 |
| V13 | exclamação na tela | `!` | sim | tela | 2 / 0 / 2 | `10-voz.md` §7: na tela, nenhuma. Dois virais pt usam ("Não é CHAFÉ!"); a decisão de voz prevalece sobre o corpus |
| V14 | emoji na tela | `[🌀-🫿☀-➿]` | sim | tela | 4 / 0 / 4 | `10-voz.md` §7: na tela, nenhum. Quatro virais pt usam (🔴, 🤫, 😂); a decisão de voz prevalece |
| V15 | reticências na tela | `…|\.\.\.` | sim | tela | 2 / 1 / 3 | `10-voz.md` §7: "soam como suspense de gancho" |

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
