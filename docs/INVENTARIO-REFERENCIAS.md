# Inventário de referências — o que vira pixel e o que vira só ideia

Varredura do disco inteiro em **05/10/2026**. **767 arquivos de mídia, 2,04 GB.**
Tudo abaixo foi lido no arquivo (dimensão, EXIF de câmera, EXIF de GPS), não
inferido de nome de pasta.

`base-curada/LEIA-ME.md` define as quatro camadas de permissão e continua mandando.
Este documento existe porque **a maior parte do acervo nunca entrou nessas camadas**:
`base-curada/` tem 66 arquivos, e há 767 no disco.

---

## A pergunta que este documento responde

Para cada grupo de arquivos: **pode entrar num request de geração como pixel, ou só
pode virar descrição em texto?**

A regra de decisão, que não é estética, é de risco:

| Pergunta | Se a resposta for não |
|---|---|
| O arquivo prova que a foto é nossa? | só ideia |
| Tem pessoa identificável sem autorização assinada? | só ideia, e nunca sintetizar |
| A resolução aguenta virar pixel de saída? | só ideia |

---

## O quadro, grupo a grupo

| Grupo | Arqs | O que é | Veredito |
|---|---:|---|---|
| `base-curada/01-real-verificada` | 38 | iPhone 7 e motorola, **com GPS** | **pixel** |
| `fotos produtos cru/` | 134 | nosso produto, motorola edge 50 fusion | **pixel, com ressalva** — ver §1 |
| `saida-teste/` (catálogo, cenas, elenco) | ~250 | **nossas próprias gerações já aprovadas** | **pixel de referência de look** — ver §2 |
| `base-curada/02-real-nao-verificada` | 6 | paisagem da Serra, sem EXIF | só ideia, até confirmarem a origem |
| `imagens/Arthur Rosto` | 13 | rosto real, 960×1280 | **nunca sintetizar** — ver §4 |
| `base-curada/03-mood-terceiros` = `imagens/Fotos-Aestethic` | 16 | Pinterest | **só ideia** — ver §3 |
| `raspagem/lacabracoffee` | 40 | scrape de Instagram de terceiro | **só ideia** — ver §3 |
| `base-curada/04-quarentena` | 6 | sintéticas + web-res | **nunca** |

---

## §1 — `fotos produtos cru/`: 134 fotos nossas fora de qualquer camada

**Medido:** 130 dos 134 arquivos trazem `motorola motorola edge 50 fusion`,
em **3072×4096**. Os outros 4 não têm EXIF nenhum e estão em **591×1280** —
são as cápsulas Suave, as mesmas da lição 18.

**GPS: 0 de 134.**

Isto cria uma contradição com a regra escrita. `01-real-verificada` exige *"EXIF de
câmera **e** GPS"*, e estes 134 falham no GPS. Pela letra da regra, cairiam em
`02-real-nao-verificada`, que é camada de **não usar**.

E, no entanto:

- é o **mesmo aparelho** dos 12 packshots de `torrefacao-uberlandia-875m`, que estão
  na camada 01;
- são fotos do **nosso próprio produto**, feitas para o catálogo;
- os **96 packshots aprovados** de `saida-teste/catalogo-estudio/` saíram justamente
  delas, via `scripts/prompts_catalogo.py`, que lê `fotos produtos cru/` por caminho.

Ou seja, na prática elas **já são** a matéria-prima do catálogo aprovado — só nunca
foram declaradas em lugar nenhum.

**Leitura minha, não medição:** o GPS nunca foi o ponto. Ele serve para provar
*onde* a foto foi tirada, e isso importa para a lavoura, porque a altitude de 1.250 m
é uma alegação de marca que o EXIF confirma sozinho. Para um pacote em cima de uma
bancada, onde a foto foi tirada não prova nada relevante — o que prova é o aparelho
e a cadeia de custódia. **Proposta: camada nova `01b-produto-proprio`**, com
permissão de pixel e sem exigência de GPS, em vez de forçar 134 arquivos para dentro
de uma regra escrita para paisagem.

Isto é decisão humana e está registrada aqui como proposta, não aplicada.

**Exceção dentro do grupo:** as 4 cápsulas Suave em 591×1280 não passam por
resolução. São a origem do erro de notas sensoriais da lição 18. Ficam como ideia
até alguém refotografar.

---

## §2 — A nossa própria geração é referência legítima, e é a melhor que temos

`saida-teste/` guarda, entre outras coisas:

- **96 packshots de catálogo aprovados** (`catalogo-estudio/`, 21 pastas de SKU);
- **44 imagens em `home-cenas/`**, a maioria em **1856×2304** — a saída 2K 4:5;
- **17 em `home-elenco/`**, 13 em `site-fundo-branco/`.

`docs/PESQUISA-REALISMO-GERACAO.md` §3 registra a rotina que um usuário de produção
do fórum da OpenAI usa quando o modelo muda e os prompts antigos param de funcionar:
anexar **as próprias gerações boas** mais a referência da estética desejada, e pedir
ao modelo a linguagem de prompt que funciona naquela versão.

Nós temos exatamente esse insumo, e ele não tem problema de licença — é nosso.
**Esta pasta é referência de look permitida e subusada.**

Ressalva: é saída de modelo, logo **não** pode alimentar destilação de Style DNA, pelo
mesmo motivo que `04-quarentena/sintetica-gemini` não pode. Referência de look numa
geração é uma coisa; virar fonte de verdade do que a marca parece é outra.

---

## §3 — Pinterest e raspagem: por que são só ideia, e um quase-erro

### Pinterest (`03-mood-terceiros`, 16 arquivos)

É a estética-alvo do projeto — mesa mineira, coador de pano, bule de ágata, pão de
queijo, golden hour — e **nada disso é nosso**. Uma tem marca d'água visível
(`@thamylis.pine…`), outra tem rosto identificável de quem não autorizou.

**O quase-erro, medido hoje:** um dos 16 arquivos
(`31814e784172da60bb5214c403619072.jpg`) **tem EXIF de câmera: `iPhone 14`**. Quem
auditasse procurando "tem EXIF de câmera?" marcaria esse arquivo como próprio e o
promoveria para a camada 01.

Ele tem **736 px de largura** — largura de pin do Pinterest — e **não tem GPS**.

> **Regra que sai disto: EXIF de câmera não é prova de autoria.** Ele prova que
> *algum* celular tirou a foto, não que foi o nosso. O que separa é a combinação —
> GPS presente **e** resolução nativa do aparelho. Aqui a exigência de GPS da camada
> 01 funcionou como rede, e vale dizer por quê, para ninguém afrouxá-la achando que
> é burocracia.

### Raspagem (`raspagem/lacabracoffee`, 40 arquivos)

Colheita do perfil de uma torrefação dinamarquesa. **Medido:** 21 arquivos em
1281×1611 e 19 em 1080×1355, nenhum com EXIF. Confere com a lição 10 — 21 de 40
acima do piso de referência de 1200 px.

São de terceiro. Servem para **extrair descritor textual** — enquadramento, paleta,
que tipo de cena a categoria publica — e nunca para entrar num request.

É também a pasta que responde à pergunta de estratégia: a grade do April Coffee e a
da La Cabra são compostas de coisas que eles **têm fisicamente**. Olhar essas 40
imagens serve para decidir *o que capturar*, não *o que gerar*.

---

## §4 — Rosto

`imagens/Arthur Rosto`: 13 arquivos, todos **960×1280**, sem EXIF.

Duas restrições, e elas são independentes:

1. **Rosto de pessoa real nunca é sintetizado.** Regra de marca, não de qualidade.
   Foto de pessoa é foto.
2. **960×1280 não enche um quadro de feed** (1080×1350). Nem como foto direta serve
   de quadro cheio, o que a série 9 do catálogo de formatos já registra.

Qualquer peça com o Arthur depende de gravação nova **mais autorização de imagem
assinada**.

---

## O buraco, que o inventário confirma em vez de resolver

`docs/briefing-captura.md` lista o que não existe. A varredura confirma, agora com
número: **não há um único arquivo** de grão torrado, café pronto na xícara, coador em
uso, tambor de torrefação, cupping, terreiro ou colheita em nenhuma camada
permitida.

Consequência prática para o conteúdo: toda série que precise desses assuntos depende
de **geração sem referência própria** — que é onde o modelo inventa e a imagem
denuncia — ou de captura nova. Não há terceiro caminho, e nenhuma quantidade de
Pinterest fecha esse buraco, porque Pinterest não pode virar pixel.
