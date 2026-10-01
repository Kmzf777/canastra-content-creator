# Motor de estáticos dirigido por catálogo — design

> Spec. Estado em 30/09/2026. Decisões fechadas em brainstorming com o Rafael nesta
> data; as três escolhas estão na seção 2 com o motivo de cada uma.

**Objetivo:** automatizar a produção de post estático do Café Canastra — da declaração
da peça até um bundle publicável — com a embalagem entrando por geração e um laço que
**corrige o rótulo até ficar correto, com terminação garantida**.

**Não é** um gerador de imagem genérico, nem um motor de vídeo. É o caminho mais curto
entre `fotos produtos cru/` e uma peça 4:5 que pode ser postada.

---

## 1. O problema, em número

O gargalo medido não é qualidade de imagem, é cadência: **1 post a cada 42 dias**,
contra 2,9 do Orfeu, com 125 dias de silêncio entre 23/05 e 25/09/2026 **[medido]**.
Ao mesmo tempo o acervo tem **137 fotos de produto em 21 SKUs** e **96 packshots de
estúdio já aprovados** parados **[medido]**.

Existe estoque de matéria-prima e não existe peça pronta. O que falta é uma linha de
produção, não um modelo melhor.

E existe um modo de falha recorrente: dos itens do `Registro de lições` do `CLAUDE.md`,
ao menos quatro — **13, 18, 21, 22** — são a mesma falha de raiz. Um valor que ninguém
declarou, logo ninguém conferiu: `Doodo 1985`, `70 / 80 / 80 / 40`, `ARABICA` sem
acento, `F:23.2025`. O desenho abaixo existe sobretudo para fechar essa classe.

---

## 2. As três decisões fechadas

### 2.1 A camada de design mora no Remotion

Tipografia de peça é desenhada por código no motor que já existe, não num pacote novo.

**Por quê:** `instagram/remotion/src/identidade/` já tem `tokens.ts` (cor, tipo, tempo,
sombra), `tipografia.ts` (as três fontes carregadas de arquivo local com `delayRender`,
que é o conserto do bug em que o Chrome headless desenhava Times New Roman sem
reclamar) e `glifos.ts`. E `src/verificacao/` já tem os quatro portões — em especial
`preservacao.ts`, que é literalmente o laudo de "nenhum pixel dentro da embalagem
mudou".

Escrever uma segunda identidade em Pillow criaria duas fontes de verdade para cor e
tipo. A lição 8 é exatamente esse erro numa série.

**Custo aceito:** Chrome headless por peça, e a zona 4:5 precisa existir. O
`05-formatos.md` §6 registra que a função de zonas recebe `{largura, altura}`, então é
extensão e não reescrita.

### 2.2 A escada de correção tem teto e cai para composição

O laço gera, confere, sobe o degrau mais barato que conserta aquele campo, e repete até
um teto de rodadas. Se o campo ainda falhar, **o pixel real da etiqueta é composto por
cima** e o laudo prova zero alteração.

**Por que termina:** o último degrau não depende do modelo. A lição 13 registra que
abaixo de ~2% da altura do quadro a tipografia **não sobrevive em nenhuma rodada** —
sem esse degrau, o laço para esses campos não converge, só gasta.

**Custo aceito:** a peça final é híbrida, não 100% saída do modelo.

### 2.3 O pipeline para no bundle; publicar é humano

Saída é uma pasta por peça: PNG, legenda em rascunho, sidecar de proveniência. Publicar
no Instagram fica fora — é irreversível e age sobre a conta real, não sobre um arquivo.

---

## 3. A correção que este design incorpora

Uma versão anterior deste desenho proibia a embalagem na camada gerada. **Isso estava
errado** e a correção veio do Rafael, com evidência no próprio repositório:

- `saida-teste/catalogo-estudio/` tem **96 packshots gerados e aprovados**, entre eles
  `7.1-frente-branco.png` e `16.1-frente-branco.png` **[medido]**;
- a **lição 21** registra que a frente saiu íntegra nos 3 SKUs;
- a **lição 12** registra os 3 SKUs com posição, escala, vincos e especular
  indistinguíveis da fonte, conferido por blend a 50%.

A regra que eu havia aplicado — *"embalagem nunca nasce aqui"* — é de
`assets/materialidade/LEIA-ME.md` e descreve **o escopo daquela pasta**, não uma
proibição de pipeline. Registrado aqui porque a próxima sessão vai reencontrar aquele
arquivo e pode repetir o erro.

**Embalagem entra por geração.** O que a protege não é a proibição; é mandar a
referência certa e **conferir letra por letra**, com a composição como rede.

Sobre rosto, a regra precisa: **rosto de pessoa real não se sintetiza**. Personagem
inventado é prática estabelecida — `scripts/home_avatares.py` gera o elenco da home de
propósito, *"como não vamos usar o rosto de ninguém real"*.

---

## 4. Arquitetura

### 4.1 Fluxo

```
catálogo (dados declarados)
   |
   +- 1. fonte ........... foto real do disco
   |
   +- 2. geração ......... ChatGPT via Chrome --> PNG bruto
   |                              ^      |
   |        escada de correção ---+      |  (teto de rodadas)
   |                                     v
   +- 3. composição ...... pixel real por cima, se caiu no último degrau
   |
   +- 4. design .......... Remotion still 4:5, tipografia de peça
   |
   +- 5. bundle .......... pasta com peça + legenda + sidecar
```

### 4.2 Fronteira de linguagem

Python é dono de **dados e pixel**. Remotion é dono de **tipografia**. A costura é um
arquivo `.json` de props.

**A costura é arquivo, nunca JSON inline.** `instagram/LEIA-ME.md` registra que
`--props` com JSON inline não funciona no shell do Windows: as aspas somem.

### 4.3 Módulos

```
instagram/estaticos/          novo pacote Python, par de instagram/recorte/
  catalogo.py    peças e moldes declarados (dataclass)
  prompt.py      declaração -> prompt de geração
  escada.py      tabela sintoma -> degrau, e o estado do laço
  conferir.py    recorta e amplia as faixas de texto para o agente olhar
  compor.py      último degrau: pixel real por cima + laudo
  cli.py         os comandos

instagram/remotion/src/
  motor/layout.ts        + zona 4:5
  estatico/Carta.tsx     composição do cartão
  estatico/moldes.ts     os moldes como layout

.claude/skills/canastra-estatico/SKILL.md
  conduz o laço e lê a escada; nunca guarda dado de SKU
```

`estaticos/` fica dentro de `instagram/` porque é conteúdo de feed e porque `compor.py`
depende de `instagram/recorte/`.

**Restrição de diretório, não negociável:** `estaticos/` lê `fotos produtos cru/` e
`saida-teste/catalogo-estudio/`, que são gitignored e **vivem só no diretório
principal**. Logo este pacote **não funciona em worktree** — roda a partir do diretório
principal, como `CLAUDE.md` já adverte para os scripts que leem acervo por caminho
relativo.

---

## 5. A declaração

```python
@dataclass(frozen=True)
class Dado:
    """Um valor que o código desenha. `origem` não tem default de propósito."""
    valor: str      # "8,0"
    origem: str     # "confirmado com o Arthur em 25/09/2026"

@dataclass(frozen=True)
class Peca:
    slug: str                           # "e2-classico-250g-graos"
    molde: str                          # "carta-sensorial"
    fonte: Path                         # foto real, vai como referência
    strings_impressas: tuple[str, ...]  # o que a EMBALAGEM diz
    dados: dict[str, Dado]              # o que o CÓDIGO desenha
    gerar_fundo: bool                   # a camada 2 entra nesta peça?
```

**`Dado.origem` é obrigatório e sem default.** Isso é estrutural, não documental: a
lição 18 nasceu de um número impresso que ninguém sabia de onde vinha. Um campo
obrigatório força a resposta na hora de declarar, e o `conferir` recusa a peça se a
origem estiver vazia. É também o que torna o bloqueio da seção 10.1 executável em vez
de uma advertência escrita.

Os dois campos de texto são separados de propósito:

| Campo | Quem produz | Como se garante |
|---|---|---|
| `strings_impressas` | geração, a partir da foto real | conferência ampliada campo a campo; falhando até o teto, composição |
| `dados` | código, no Remotion | exato por construção — não tem foto de onde vir |

### Uma declaração, três consumidores

`strings_impressas` alimenta, da mesma fonte:

1. o **bloco de soletração** do prompt (`prompt.py`);
2. o **checklist da conferência** (`conferir.py`) — um recorte ampliado por string;
3. as **asserções do laudo** (`compor.py`).

É isto que fecha a classe de falha da seção 1: hoje o agente monta a lista de campos de
memória na hora da conferência, e foi assim que um campo fisicamente ilegível virou
`✓ confere`. Se a lista é dado declarado, não há campo esquecido nem campo inventado.

### Reuso, não duplicação

`scripts/prompts_catalogo.py` já declara 21 SKUs numa dataclass `Produto`, com
`frente`, `verso`, `arte`, `laterais` e `lateral_extra` — e seu `lateral_extra` já é o
mecanismo de soletrar valor ilegível. `catalogo.py` **importa `Produto` em vez de
redeclarar SKU**. O que é novo aqui é `strings_impressas` como gabarito de conferência
e `dados` como texto de peça.

---

## 6. A escada de correção

### 6.1 Roteamento sintoma -> degrau

Cada linha vem de uma falha já paga neste repositório.

| Degrau | Sintoma na conferência | Correção | Origem |
|---:|---|---|---|
| 1 | valor inventado (`70` onde é `7,0`) | soletrar a string no prompt | lição 18, `lateral_extra` |
| 1 | acento perdido (`ARABICA`, `DOCURA`) | soletrar o acento, caractere a caractere | lição 21 |
| 2 | rótulo genérico, sósia da marca | nomear a operação: `EDIT THE PROVIDED PHOTOGRAPH` + `KEEP THE PACKAGE PIXEL-FOR-PIXEL IDENTICAL`; mostrar a **frente** | lições 1 e 12 |
| 3 | fonte crua ruim ou baixa resolução | âncora de outro SKU da família, duas imagens com papéis separados | `canastra-embalagem` |
| 4 | letra corrompida (`Doodo 1985`, `TRODULB E HÚMO`) | aumentar o pacote no quadro | lição 13 |
| 5 | erra ~1 em 3 sem padrão | gerar N variantes e escolher | `site_fundo_branco.py` |
| 6 | qualquer campo que sobreviveu ao teto | **compor o pixel real por cima** | `recorte/` + `preservacao.ts` |
| 6 | lote, fabricação, validade, QR, código de barras | **nunca aceita gerado**, vai direto ao degrau 6 ou sai do enquadramento | lição 22 |

### 6.2 Terminação

```
tentativa = 0
enquanto houver campo errado e tentativa < TETO:
    degrau = escada.rotear(campos_falhos)
    gera de novo com a correção
    confere
    tentativa += 1

se ainda houver campo errado:
    compor.pixel_real(campos_falhos)   # degrau 6
    laudo exige pixels_alterados == 0 dentro do retângulo do rótulo
```

`TETO` é parâmetro, padrão **3**. O degrau 6 não é fracasso do laço: é o seu piso.

### 6.3 Dois campos que não entram no laço

- **Lote, fabricação, validade:** carimbo variável impresso fora da arte. A lição 22
  registra `F:23.2025`, um mês que não existe, e `F:12.2025`, plausível — e o plausível
  é pior, porque passa. Em peça de e-commerce isso é informação regulatória falsa.
- **QR e código de barras:** sempre regenerados. `canastra-conteudo` manda reportar
  como `regenerado — não escaneável`.

Para os dois a regra é: **sai do enquadramento, ou entra por composição da foto real.**

---

## 7. Conferência

A conferência continua sendo feita **pelo agente, olhando recorte ampliado** — é o que
funciona hoje e o que `canastra-conteudo` fase 4 já especifica. O que este design
automatiza é a mecânica em volta dela:

- `conferir.py` **produz os recortes**, um por string declarada, da gerada **e** da
  referência, ampliados com `Image.LANCZOS`. Conferência é comparação entre dois
  recortes, nunca entre um recorte e a memória do agente.
- O veredito é **por campo**, nos três estados de `canastra-conteudo`:
  `confere` / `errado: saiu X, é Y` / `não verificável na referência`.
- **`não verificável` não é aprovação.** Campo não verificável bloqueia o bundle e
  exige valor soletrado — é a lição 18 e a racionalização que já foi catalogada.

---

## 8. Bundle de saída

```
saida-estaticos/2026-10-02-e2-classico-250g-graos/
  peca.png            1080x1350
  legenda.txt         rascunho
  sidecar.json
```

O `sidecar.json` responde "de onde veio isto" sem abrir o histórico:

```json
{
  "slug": "e2-classico-250g-graos",
  "molde": "carta-sensorial",
  "fonte": "saida-teste/catalogo-estudio/7-classico-250g-graos/7.1-frente-branco.png",
  "fonte_sha256": "...",
  "strings_esperadas": ["SCA 80+", "ARÁBICA", "250g", "TORRA MÉDIA"],
  "conferencia": {"SCA 80+": "ok", "ARÁBICA": "composto", "250g": "ok"},
  "degraus": ["soletrar", "compor"],
  "tentativas": 2,
  "laudo": {"pixels_alterados": 0, "alfa_minimo_no_rotulo": 255, "aprovado": true},
  "gerado_em": "2026-10-02T14:03:00+00:00"
}
```

`saida-estaticos/` é **gitignored**, como `saida-teste/`.

---

## 9. Verificação e testes

Alvo: `python -m uv run pytest` para o lado Python, `npx vitest run` para o Remotion.

| O que se prova | Como |
|---|---|
| a declaração é válida | `python -m instagram.estaticos conferir` sem gerar: toda `fonte` existe no disco, nenhuma `strings_impressas` vazia, nenhum `dados` com chave fora do molde, **nenhum `Dado.origem` vazio** |
| o prompt contém toda string declarada | asserção: cada item de `strings_impressas` aparece no prompt montado |
| o roteamento da escada é determinístico | tabela de entrada/saída: sintoma -> degrau esperado |
| o teto é respeitado | laço com gerador falso que sempre erra: termina em `TETO` e cai no degrau 6 |
| a composição não toca o resto | laudo sobre região fora do retângulo: zero pixel alterado |
| campo não verificável bloqueia | peça com campo ilegível não produz pasta |
| a zona 4:5 fecha em 1080x1350 | asserção de dimensão, **lado par** — lição 26 |

**Derivar a escala da largura alvo, nunca digitá-la.** A lição 26 registra peça saindo
360x638 em vez de 360x640 com exit 0: `escalaParaLargura()` já existe em
`instagram/remotion/src/verificacao/telefone.ts`.

---

## 10. Riscos assumidos e bloqueios conhecidos

### 10.1 As notas sensoriais estão inconsistentes no repositório — BLOQUEIO

O molde da v1 imprime nota sensorial, e as duas fontes do repositório divergem:

| Fonte | Suave | Canela |
|---|---|---|
| lição 18 + `prompts_catalogo.py`, *confirmado com o Arthur em 25/09/2026* | CORPO **7,0** · AROMA 10 · DOÇURA 10 · CITRICIDADE 6,0 | — |
| lição 21 | **6,5**/10/10/6,0 | **7,0**/10/10/6,0 |

O Suave diverge no CORPO, e o Canela da lição 21 é exatamente o que a lição 18 chama de
Suave — parecem **trocados**. Além disso as duas fontes são das **cápsulas**; não está
registrado se o saco de 250 g traz as mesmas notas.

**Consequência:** nenhuma carta sensorial sai antes de o valor ser confirmado e
soletrado. O comando `conferir` **recusa** peça cujo `Dado.origem` esteja vazio (seção 5). Imprimir nota errada é erro factual em post de produto.

### 10.2 Sessão concorrente no mesmo diretório — BLOQUEIO PARCIAL

*Retrato de 30/09/2026, 21:22:* há modificação não commitada em
`instagram/remotion/src/motor/layout.ts` com mtime 21:06, mais `cadencia.ts`,
`relogio.ts` e dois testes novos que não existiam às 18:36. Há também o worktree
`../Canastra-motor-imagem` na branch `motor-imagem`.

`layout.ts` é exatamente o arquivo que a zona 4:5 toca. **A trilha Remotion não começa
enquanto essa sessão estiver com o arquivo aberto** — é a lição 9.

A trilha Python não colide: `instagram/estaticos/` é diretório novo.

**Ao commitar, nomear caminhos explicitamente.** `git add -A` varreria o trabalho não
commitado da outra sessão e o `mercadolivre/` para dentro deste commit.

### 10.3 Riscos menores, aceitos

- **Chrome headless por peça** custa segundos por render. Aceito: 21 peças é minutos.
- **A peça final é híbrida.** Quando o degrau 6 roda, parte do rótulo é pixel composto.
  O sidecar declara isso em `conferencia` e `degraus`; não se esconde.
- **A legenda sai em rascunho.** As três legendas de `saida-teste/post-instagram/` têm
  ~900 caracteres e 10 hashtags; o Orfeu, com 0,74% de engajamento, roda 335 caracteres
  e ~zero hashtag **[medido]**. O rascunho segue o molde existente e a versão curta é
  teste, não decisão deste design.

---

## 11. O que fica fora

| Fora | Por quê |
|---|---|
| publicar no Instagram | irreversível, age na conta real; a lição 17 já mostrou automação de navegador agindo sobre a coisa errada em silêncio |
| rota de API (Gemini/xAI) para esta linha | `site_fundo_branco.py` e `home_cenas.py` já cobrem a rota de API; esta linha é a rota ChatGPT, que foi a pedida |
| moldes E1, E3 e E4 na v1 | entram como **linha de catálogo e layout**, não como código. Se E1 exigir módulo Python novo, a v1 errou a abstração |
| `briefing.json` e compilador puro | é o plano `2026-10-01-motor-briefing.md`, 276 KB e não executado. O catálogo é um passo na direção dele, não um desvio |
| carrossel multi-slide | depende de coesão de série (lição 8); entra depois do molde único |
