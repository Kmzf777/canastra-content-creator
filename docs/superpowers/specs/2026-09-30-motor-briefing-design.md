# Motor de vídeo dirigido por briefing — spec de desenho

> **Data:** 30/09/2026 · **Estado:** desenho consolidado, nada implementado.
> **Escopo:** `instagram/remotion/`, mais uma skill nova em `.claude/skills/`.
> **Não substitui** `docs/superpowers/plans/2026-09-30-motor-video-qualidade.md`
> (99 KB, 2.327 linhas). A §6 desta spec diz, item por item, o que dele é
> absorvido, o que é superado e o que continua valendo em separado.

> **Revisão de 30/09/2026, depois do cético adversarial.** A spec foi reprovada
> com 20 achados. Os cinco de gravidade alta estão corrigidos no corpo do texto,
> e a §7 é nova: ela registra item por item o que foi corrigido, o que foi
> **recusado com medição** (o cético errou em dois pontos, e um deles pelo mesmo
> motivo que eu errei) e a quebra em planos. Onde a correção mudou um número, o
> número antigo fica escrito ao lado, porque apagar o errado esconde a lição.

> **Segunda rodada, 01/10/2026: a própria correção introduziu três defeitos, e os
> três estão fechados.** (1) **§3.4.2, a geometria de pista** descrevia caixas que
> o motor não tem — `rodape` não é fração da coluna, é `zonas.legenda`; `tela` é
> `zonas.seguro`; a coluna é a interseção com o seguro — e a invariante *"as quatro
> pistas partilham o x"* é **falsa** exatamente nos três formatos onde a
> sobreposição existe. (2) **§3.4.2, o piso de dominância**: a frase que fechava o
> achado 4 era falsa quando medida, e estava **sem marca de procedência**; o piso
> reprova a manchete em **coluna**, não a peça, que renderiza em cartela e passa por
> 7,8×. (3) **§2.2.1 e §7.1**: a spec dizia *"grudado em 0, nunca descartado"*
> contra o plano, e §7.1 não dizia que o portão de ritmo **reprova** o único
> briefing concreto desta spec — agora diz, com os 14 frames de recuo e o
> `silence_end: 1.135` medido no `pl.wav`.

## Procedência dos números desta spec

Quatro marcas, e nenhuma linha sem marca:

- **[medido aqui]** — rodei o comando nesta sessão, nesta máquina, em 30/09/2026.
  Os módulos puros foram executados empacotando com
  `node_modules/.bin/esbuild <entrada>.ts --bundle --format=esm --platform=node`
  e rodando o `.mjs`. **Node cru não resolve os imports sem extensão do projeto**
  e não há `tsx` instalado — medido: `ERR_MODULE_NOT_FOUND` em
  `src/identidade/tokens`. `layout.ts` é a exceção: não tem import nenhum e roda
  com `node --experimental-strip-types`.
- **[aritmética]** — conta minha sobre valores [medido aqui] ou sobre constante
  lida no arquivo.
- **[relatado]** — vem da auditoria de 8 regras ou de um dos quatro desenhos
  paralelos, e **eu não reproduzi**. Entra nomeado como tal e nunca sustenta uma
  decisão sozinho.
- **[escolhido]** — número que **esta spec decide**, sem medição que o obrigue,
  com a razão escrita ao lado. Marca nova da revisão: a versão anterior tinha
  números escolhidos vestidos de medidos, e é assim que a lição 10 do `CLAUDE.md`
  acontece. Um `[escolhido]` é revisável sem refazer medição; um `[medido aqui]`
  não.

**A suíte de testes agora foi rodada.** `npx vitest run`: **6 arquivos, 85 testes,
todos passando**, 1,75 s [medido aqui]. Por arquivo, contado no relatório JSON:
`agrupar` 4 · `layout` 4 · `manchete-props` 12 · `preservacao` 9 · `sondar` 6 ·
`textotela` 50. A divergência com os **91** que `grep -c "it("` dá está
localizada — `agrupar` 5→4, `manchete-props` 16→12, `textotela` 51→50 — e é do
`grep`, que conta ocorrências de `it(` que não são um teste. **O número de
verdade é 85**, igual ao que o plano de qualidade registra; a versão anterior
desta spec deixou os dois vivos e isso está resolvido.

---

## 1. O problema, em uma página

### 1.1 O que o motor faz hoje

Uma peça. `Raiz.tsx` registra quatro composições — `Reel` 1080×1920, `Feed`
1080×1080, `Teste` e `PonteAssets` (instrumento de conferência) —, e `Reel` e
`Feed` são o **mesmo** componente `PecaVideo` com dimensão diferente, com a
diferença inteira dentro de `layout()`. É a propriedade central do motor: o 1:1 é
reenquadramento, não recorte. Nada nesta spec a desfaz.

`PecaVideo` monta três camadas, na ordem da árvore (`z-index` não existe no
Remotion): `Fonte` → `TextoTela` (manchete, opcional) → `Legenda`. O relógio é
`FPS = 30` chumbado em `Raiz.tsx:22`, com `CORTAR_ANTES_FRAMES = 34` e
`DURACAO_FRAMES = 696` derivados dele em tempo de módulo.

### 1.2 O que o Rafael quer

Nas palavras dele: *"deixar isso um puta motor, com uma skill integrada no rep,
onde posteriormente eu jogue as informações, planejamento etc, montagem de
composição"*.

Traduzido em requisito: o motor deixa de ser um renderizador de **uma peça** e
passa a ser dirigido por **briefing**. A entrada é informação — série do
catálogo, gancho, locução, números, plano de cenas —; a saída é peça renderizada
e aprovada nos portões. O `props.json` deixa de ser escrito por gente e passa a
ser **artefato compilado**.

### 1.3 As quatro ausências estruturais

Três vieram na auditoria; **as quatro estão confirmadas por `grep` que eu rodei
agora** [medido aqui]. A quarta é acréscimo do desenho da skill e é a mais
barata de esquecer.

| # | Ausência | Evidência que rodei | Quem paga |
|---|---|---|---|
| **A1** | **A fonte só pode ser vídeo.** `Fonte.tsx:48` monta `<Video>` sem alternativa | `grep -rn "<Img" src/` só acha `PonteAssets.tsx:85`, que é instrumento de conferência | O acervo tem **1 vídeo contra 38 fotos verificadas** (26 de lavoura + 12 packshots, `05-formatos.md` §1). **7 das 12 séries partem de foto parada** — 1, 2, 3, 5, 7, 10, 11, lidas na coluna *Matéria-prima* de `05-formatos.md` §4 [aritmética]. A versão anterior escrevia "5 das 12" sem marca: o 5 é a conta **de Reel** (§3.6), não a de foto |
| **A2** | **A manchete é singular no tipo.** `PecaVideo.tsx:93`: `manchete?: Manchete \| null` — objeto | `duracaoDaFrase('SUA PRÓPRIA MARCA DE CAFÉ')` = **60 frames** [medido aqui] = 2,000 s a 30 fps, numa peça de 696 frames = 23,20 s → **91,38% da peça sem nenhuma camada além da legenda** [aritmética] | `proibicoes.md:11-12` proíbe "tempo morto", na mesma pasta |
| **A3** | **Não existe cena.** Zero `Series`, zero `TransitionSeries` | `grep -rn "TransitionSeries\|<Series\|Sequence" src/` = **5 ocorrências, todas comentário** (`texto-forma.ts:150`, `TextoTela.tsx:33` e `:73`, `PecaVideo.tsx:50` e `:53`) | Séries 3, 4, 10 e 11 do catálogo |
| **A4** | **Não existe faixa de áudio independente da fonte** — nem trilha, nem **locução**. Nenhum `<Audio>` na árvore; todo som é carona do `<Video>` | `grep -rn "Audio" src/` só acha `motor/audio/normalizar.ts` (medição pós-render) e o comentário de `:36` prevendo um `<Audio>` futuro | **Toda** peça de foto parada sai **muda**. `05-formatos.md` §3, **[oficial]**: Reel sem faixa de áudio perde elegibilidade para não-seguidor. **5 das 12 séries entregam Reel a partir de foto parada** — 1, 2, 5, 10, 11: séries cuja coluna *Formato* inclui reel **e** cuja matéria-prima é foto parada [aritmética sobre `05-formatos.md` §4]. Série 3 é carrossel e 7 é estático, então saem desta conta e entram na de A1 |

### 1.4 Três frouxuras transversais, que qualquer briefing atravessa

1. **`fps` é suposto, não derivado.** `useVideoConfig` aparece em **um** arquivo
   de `src/` (`PecaVideo.tsx:58` no import, `:97` no uso) e só lê `width`/`height`
   [medido aqui]. Nenhuma camada de texto o chama. A 60 fps tudo encurta pela
   metade, com exit 0 e sem aviso.
2. **`zod` e `@remotion/zod-types` entram por transitividade, não por
   declaração.** `node_modules/zod` é **4.5.4** e `node_modules/@remotion/zod-types`
   é **4.0.530**; nenhum dos dois está em `dependencies` nem em `devDependencies`
   do `package.json` [medido aqui].

   **Correção da versão anterior, que afirmou como medido algo falso.** Estava
   escrito *"são dependências fantasma … `npm ci` numa máquina limpa derruba
   qualquer schema"*. Não derruba. Reli o `package-lock.json` [medido aqui]: os
   dois estão lá como pacotes **não-dev** com versão exata
   (`node_modules/zod → 4.5.4, dev: false`;
   `node_modules/@remotion/zod-types → 4.0.530, dev: false`), porque são
   dependência declarada de pacotes que **estão** no `package.json` — o lock
   registra `zod: 4.5.4` em `@remotion/media` (que está em `dependencies`), e
   também em `@remotion/studio`, `@remotion/studio-protocol`,
   `@remotion/studio-server`, `@remotion/openai-whisper` e `@remotion/elevenlabs`;
   `@remotion/zod-types: 4.0.530` aparece em `@remotion/studio`. `npm ci` instala
   a árvore inteira do lock, logo instala os dois. O plano de qualidade, §V9,
   escreve isto certo — *"já estão no node_modules (transitivos do
   `@remotion/cli`)"* — e a versão anterior desta spec o contradizia sem dizer
   que estava contradizendo.

   **O risco real, e ele continua justificando a ação.** Transitivo não é
   contrato: (a) o dia em que o Remotion soltar o `zod` de `@remotion/media`, o
   `zod` sai do lock na atualização seguinte e o `esquema.ts` quebra sem nenhuma
   mudança nossa; (b) a versão que valeria passa a ser a que o Remotion escolher,
   e um major do `zod` entra sem revisão nossa; (c) sob gerenciador com
   isolamento estrito (`pnpm` com `hoist=false`, Yarn PnP) o import de um pacote
   não declarado **falha**, mesmo com o lock cheio. Ação: declarar
   `"zod": "4.5.4"` em `dependencies`, exatamente na versão que o lock já pina,
   para que a declaração não mude uma única árvore. `@remotion/zod-types` entra
   só se `esquema-studio.ts` existir (§2.4). É a lição 11 do `CLAUDE.md` em npm:
   ferramenta que vive no ambiente sem estar declarada desaparece na próxima
   sincronização.
3. **O portão de preservação existe e não está ligado.**
   `src/verificacao/preservacao.ts` (125 linhas) e `tests/preservacao.test.ts` (9
   `it`) existem; `scripts/conferir.mjs:77` lista os portões válidos como
   `todos, folha, telefone, determinismo, loop` — **sem `preservacao`** [medido
   aqui]. Peça com recorte de embalagem hoje sai sem nenhuma prova de que o
   rótulo não foi alterado.

---

## 2. Arquitetura

### 2.1 Fluxo de dados

```
  Rafael joga informação
        │
        ▼
  .claude/skills/canastra-briefing        entrevista na ordem que trava
        │                                 (série → fontes → locução → duração
        ▼                                  → formatos → gancho/CTA → licenças)
  projetos/<p>/briefing.json              A VERDADE HUMANA. Um relógio: segundos
        │                                 por cena. Editável à mão.
        ▼
  src/briefing/esquema.ts     (zod)       validação de FORMA
        │
        ▼
  src/briefing/refinar.ts     (PURO)      validação de SENTIDO, sobre o BRIEFING
        │                                  (o que zod não expressa: ver §3.9.1)
        ▼
  src/briefing/compilar.ts    (PURO)      ARITMÉTICA, e só ela
        │                                  · segundos → frames, uma única vez
        │                                  · rebase da legenda p/ tempo da peça
        │                                  · Σcenas − Σtransições
        ▼
  projetos/<p>/plano.json                 ARTEFATO GERADO. Nunca editado à mão:
        │                                 carrega "_gerado_por" e o sha256 do
        │                                 briefing que o produziu.
        ▼
  portão RITMO (puro, ANTES do render)    o que só é visível no plano + no disco
        │                                 (§3.9.1). Reprova sem gastar render.
        ▼
  <Composition schema={} defaultProps={plano}>
        │
        ▼
  Peca → AbsoluteFill(terra)
           ├─ TransitionSeries            AS CENAS, e só elas
           │    └─ Sequence(premountFor)  → Cena: Fonte + eventos de texto
           ├─ Legenda                     FORA: relógio da peça, contínua
           ├─ Locucao                     FORA: relógio da peça  (A4)
           └─ Trilha                      FORA: relógio da peça  (A4)
        │
        ▼
  render dos formatos → normalizar áudio → 5 portões pós-render
                        (folha · telefone · determinismo · loop · preservação)
```

**São seis portões, não cinco**, e o novo roda **antes** do render. A versão
anterior desenhou o fluxo terminando em "5 portões" e deixou o portão `ritmo`
fora de todos os ramos — quem lesse só o diagrama não o implementaria. O lugar
dele no fluxo é uma consequência do que ele checa: tudo que o `ritmo` pega é
visível no `plano.json` e no disco, então gastar render antes é desperdício.

### 2.2 Os três relógios, e a regra que os resolve

Hoje existem **dois** e o motor já paga por isso: `Legenda.tsx:34` soma
`deslocamentoFrames`, `PecaVideo.tsx:126` subtrai `cortarAntesFrames`, e o
cabeçalho de `PecaVideo.tsx:36` escreve *"um props.json com dois relógios é um
props.json que alguém vai ler errado"*. Cena cria o terceiro:

| relógio | frame 0 é | quem vive nele |
|---|---|---|
| **fonte** | 1º frame do arquivo original, antes do corte | `transcricao.json`, `blocos`, `manchete.inicioFrame` |
| **peça** | 1º frame renderizado | `durationInFrames`, a legenda, a trilha |
| **cena** | 1º frame daquela cena | `useCurrentFrame()` dentro de `TransitionSeries.Sequence` — o Remotion rebaseia |

E com transição, o tempo da peça **não é** a soma dos tempos das cenas (§3.2.2).
Nenhum humano mantém isso de cabeça. Logo:

> **O briefing tem um relógio: segundos, contados do início da cena a que o
> evento pertence.** Nenhum campo do briefing está em frames. A posição da cena
> vem da **ordem no array**, não de um campo de tempo. A única conversão do
> sistema é `emFrames(s, fps) = Math.round(s * fps)`, num módulo puro, com teste.

**Correção: o tempo da fonte sobrevive em três lugares, não em um.** A versão
anterior escrevia *"o tempo da fonte sobrevive em um lugar: o arquivo de
transcrição"*, e a mesma spec põe `aparaAntesS`/`aparaDepoisS` dentro de
`Cena.fonte` e `locucao.aparaAntesS` no áudio — os três **são** tempo de fonte
dentro do briefing. A regra honesta é outra, e é mais forte:

> Campo em tempo de fonte é **permitido apenas como apara**: um deslocamento que
> diz onde o arquivo começa a ser usado. Ele nunca posiciona nada na peça. Só
> três nomes têm essa permissão — `fonte.aparaAntesS`, `fonte.aparaDepoisS` e
> `audio.*.aparaAntesS` — e todos carregam `apara` no nome exatamente para que a
> exceção seja legível. Todo o resto do briefing está em tempo de cena.

#### 2.2.1 O rebase da legenda, com N cenas — a fórmula

Este é o buraco que o cético achou e ele é real: com N cenas há **N** valores de
`aparaAntesS`, um por `Cena.fonte`, e **uma** `legenda`. Somar "o" `aparaAntesS`
deixa de ser definido. Hoje o motor tem sorte: `PecaVideo.tsx:134` passa
`deslocamentoFrames={p.cortarAntesFrames}`, um número só, porque há uma cena só
[medido aqui].

**A resolução é negar a pergunta.** Nenhum `aparaAntesS` de cena entra no rebase
da legenda, porque a legenda não é imagem: ela é a **fala**, e a fala tem uma
fonte de áudio só na peça. Logo:

```ts
type LegendaDeclarada = {
  arquivo: string;          // .json de transcrição, relativo à raiz do projeto
  relogio: 'fonte';         // enum de UM valor: declarar é o ponto, não escolher
  ancora:                   // que instante da transcrição cai no frame 0 da peça
    | {tipo: 'locucao'}     // = audio.locucao.aparaAntesS. O caso normal
    | {tipo: 'cena'; indice: number}   // = cenas[indice].fonte.aparaAntesS
    | {tipo: 'segundo'; valorS: number};
  entradaNaPecaS?: number;  // quando a pista de legenda entra na peça. default 0
  maxPalavrasPorBloco?: number;  // default LEGENDA.maxPalavras = 2
};
```

E a conversão, uma vez, no compilador:

```
ancoraS   = conforme o enum acima
desloc    = emFrames(entradaNaPecaS ?? 0, fps) − emFrames(ancoraS, fps)
bloco.inicioNaPeca = bloco.inicioFonteFrames + desloc
bloco.fimNaPeca    = bloco.fimFonteFrames    + desloc
```

Quatro consequências, e cada uma fecha um modo de falha:

1. **A camada `Legenda` deixa de somar deslocamento.** O plano entrega blocos já
   no relógio da peça e a fiação passa `deslocamentoFrames={0}` — que
   `Legenda.tsx:14` já prevê por escrito. Um relógio a menos na árvore.
2. **`ancora: {tipo:'cena', indice}` é o único jeito de um `aparaAntesS` de cena
   tocar a legenda, e ele é nominal.** Quem escreve o briefing aponta a cena com
   o dedo; o compilador não adivinha. Sem locução e sem âncora declarada, o
   refinador **recusa** — não escolhe a cena 0 por conveniência, que é o default
   escondido que esta spec proíbe em toda parte.
3. **Bloco que atravessa o frame 0 é grudado em 0; bloco que já terminou antes
   dele é descartado.** São dois contadores separados no diagnóstico —
   `grudadosEmZero` com o `maiorRecuoFrames`, e `descartadosAntesDoInicio` —, e a
   distinção não é cosmética: grudar em 0 um bloco cujo **fim** caiu antes do
   frame 0 poria no quadro texto que ninguém fala na peça. É o caso já vivido: o
   Whisper pôs as primeiras palavras dentro do ar morto, e hoje o `blocos.find()`
   de `Legenda.tsx:35` simplesmente não acha nada — a palavra **desaparece em
   silêncio**. O portão de ritmo reprova quando o maior recuo passa de
   `LEGENDA.duracaoMinFrames` = **10 frames** (`tokens.ts`, [medido aqui]).

   **Correção da revisão de 01/10/2026.** A versão anterior escrevia *"grudado em
   0, **nunca** descartado"*, e o plano de implementação já escreve o contrário,
   com teste e com contador (`descartadosAntesDoInicio`). Ficava uma divergência
   spec × plano no meio do contrato. E o limiar de 10 frames não separa
   *"arredondamento de Whisper"* de *"âncora errada"*, como estava escrito: acima
   do piso há **duas** causas possíveis — a âncora está errada, **ou** a
   transcrição não corresponde ao áudio desta peça — e a mensagem do portão nomeia
   as duas, porque o conserto é diferente em cada uma. §7.1 mede a segunda no
   único briefing concreto desta spec, e ela **reprova** ali.
4. **Bloco com `inicioNaPeca ≥ duracaoPecaFrames` é descartado, e contado.** A
   legenda não pode ter fala depois do fim da peça, e o número no diagnóstico é o
   que denuncia uma peça encurtada por `totalFixo` que comeu a fala.

### 2.3 Tipos principais

Os nomes abaixo são o contrato. O detalhe de cada um está na seção indicada.

```ts
type Briefing = {
  _esquema: 'canastra-briefing/1';
  serie: Serie;                 // 12 slugs de 05-formatos.md §4, + 'avulsa'   §3.1
  fps: number;                  // 1..120, default 30                          §3.1
  formatos: Formato[];          // '9:16' | '1:1' | '4:5'  — 16:9 NÃO entra     §3.1
  duracao: {modo: 'somaCenas' | 'totalFixo'; alvoS?: number};   // sem default §3.2
  cenas: Cena[];                                                            // §3.2
  transicoes: Transicao[];      // exatamente cenas.length - 1                §3.2
  legenda?: LegendaDeclarada;   // definida em §2.2.1                          §3.4
  audio: Audio;                 // OBRIGATÓRIO, e ao menos uma faixa dentro    §3.6
  assets: Asset[];              // recortes de embalagem. [] é válido        §3.9.1
  licencas: Partial<Licencas>;  // 12 chaves; ausente = desligada              §3.7
  gancho: string;               // o que prende nos 2 primeiros segundos
  cta: string;
};

type Cena = {
  duracaoS: number;             // > 0
  fonte: Fonte;                                                             // §3.3
  eventos: EventoTexto[];                                                   // §3.4
};

// ---- áudio: fecha a ausência A4 ------------------------------------------ §3.6
type Faixa = {
  arquivo: string;              // NOME dentro da subpasta, nunca um caminho
  ganhoDb: number;              // ganho RELATIVO na mistura. NÃO é LUFS
  aparaAntesS: number;          // apara (§2.2): de onde o arquivo começa a tocar
};
type Locucao = Faixa;           // vive em SUB.fonte, onde `pl.wav` já está
type Trilha  = Faixa & {       // vive em SUB.audio, subpasta NOVA (§3.6)
  loopar: boolean;              // sem default: 20 s de trilha em 40 s de peça
  fadeEntradaS: number;         //   é decisão, não conveniência
  fadeSaidaS: number;
};
type Audio = {
  locucao: Locucao | null;      // null = peça sem voz. NUNCA ausente
  trilha: Trilha | null;        // null só é aceito COM locução (§3.6)
};
// NÃO existe campo de LUFS no briefing: o alvo -14 LUFS / -1 dBTP é dos tokens
// (`AUDIO`, medido) e é aplicado pós-render por `scripts/normalizar-audio.mjs`
// sobre a MISTURA. Um alvo por faixa no briefing seria uma segunda verdade que
// o normalizador sobrescreve sem avisar.

type Asset = {
  arquivo: string;              // nome dentro de public/assets/             §3.9.1
  tipo: 'recorte-embalagem';
  laudoExigido: true;           // literal: recorte sem laudo não entra
};

type Licenca  = {ligada: true; justificativa: string};   // ≥ 12 caracteres   §3.7
type Licencas = Record<ChaveDeLicenca, Licenca>;         // 12 chaves

type Fonte =
  | {tipo: 'video';  arquivo: string; razaoExibicao: number;
     aparaAntesS: number; aparaDepoisS?: number;
     enquadramento: 'faixa' | 'preencher'; camera: Camera}
  | {tipo: 'foto';   arquivo: string; razaoExibicao: number;
     registro: 'moldura' | 'cartao' | 'telaCheia';    // proibicoes.md:24      §3.3
     enquadramento: {tipo: 'faixa'}
       // FRAÇÃO do arquivo JÁ ORIENTADO, em 0..1. Ver §3.3.3 para o porquê
       | {tipo: 'recorte'; x: number; y: number; largura: number; altura: number};
     camera: Camera}
  | {tipo: 'cor';    cor: string}
  | {tipo: 'grade';  colunas: 1|2; linhas: 1|2; calha: number;
     celulas: FonteSimples[]};  // 2 a 4, NÃO recursivo

type FonteSimples = Exclude<Fonte, {tipo: 'grade'}>;   // é só isto: sem grade
type Camera = 'parado' | 'pushLento';   // pushLento = PUSH dos tokens, 1,00→1,04

type Transicao =
  | {tipo: 'corte'}                                     // 0 frames. O default
  | {tipo: 'fade' | 'wipe'; duracaoS: number}           // → linearTiming
  | {tipo: 'fade' | 'wipe'; mola: Mola; duracaoFramesDeclarada: number};  // §3.2.3
type Mola = {damping: number; stiffness: number; mass: number};

type EventoTexto = {
  papel: 'manchete' | 'dado' | 'etiqueta';   // 'legenda' NÃO é evento         §3.4
  texto: string;
  entradaS: number;             // relativo ao início DA CENA
  duracaoS?: number;            // ausente = duracaoDaFrase(texto)
  pista: 'topo' | 'principal' | 'tela';   // OBRIGATÓRIO. 'rodape' é da legenda
  palavraAcento?: number;       // no máximo 1 evento por cena preenche
  // NÃO existe `encaixe` no briefing: ele é DERIVADO do formato. Ver §3.4.2
};
```

`Camera`, `FonteSimples`, `Transicao`, `Trilha`, `LegendaDeclarada`, `Asset` e
`Licenca` eram citados como contrato e não estavam definidos em nenhuma seção. Os
sete estão acima. `Serie`, `Formato` e `ChaveDeLicenca` são os enums de §3.1 e da
tabela de §3.7.

### 2.4 Onde cada arquivo novo mora

| arquivo | puro? | por quê |
|---|---|---|
| `src/briefing/esquema.ts` | **zod puro, sem `@remotion/zod-types`** | `node_modules/@remotion/zod-types/package.json` declara `"dependencies": {"remotion": "4.0.530"}` [medido aqui]. Importar `remotion` num módulo que o vitest carrega é o modo de falha que `tipografia.ts` já pagou: `loadFont` no topo do módulo derruba o vitest com `TypeError: Invalid URL`. Não testei se `zod-types` quebra — a regra é preventiva e custa nada |
| `src/briefing/esquema-studio.ts` | não | é aqui, e só aqui, que `zColor()` e `zTextarea()` entram, para o `<Composition schema>` dar caixa de cor e textarea no Studio |
| `src/briefing/compilar.ts` | **sim** | toda a aritmética de tempo, incluindo `Σcenas − Σtransições`. Não importa `remotion`, então `spring()` está fora (§3.2.3) |
| `src/briefing/refinar.ts` | **sim** | as recusas de sentido **sobre o briefing**, que zod não expressa e que não precisam do disco (§3.9.1) |
| `src/verificacao/ritmo.ts` | **sim** | o portão: as recusas que precisam do `plano.json` **ou** de ler o disco (§3.9.1) |
| `src/motor/Cena.tsx` | não | fiação |
| `src/motor/camadas/Trilha.tsx` | não | fiação do `<Audio>`, locução **e** trilha (A4) |
| `src/motor/evento.ts` | **sim** | tabelas `FAMILIA_DO_PAPEL`, `CADENCIA_DO_PAPEL`, `PISTA_PADRAO` |
| `src/motor/pista.ts` | **sim** | a geometria de pista e a derivação de encaixe (§3.4.2) |
| `src/motor/sondar.ts` | não (I/O) | **estendido**, não substituído: passa a ler EXIF `Orientation` (§3.3.3) |

`src/briefing/esquema.ts` **em `src/`, não em `out/`.** O protótipo de contrato
vive hoje em `instagram/remotion/out/_spec-briefing/` (7 arquivos, `briefing.ts`
com 35.454 B, medido agora com `ls`), porque `out/` é gitignorado e era a única
raiz onde `@remotion/zod-types` resolvia. Como o esquema de produção **não** usa
`zod-types`, essa restrição desaparece e o arquivo vai para `src/`. O protótipo é
evidência, não destino.

---

## 3. As peças, com as contradições resolvidas

Quatro agentes desenharam em paralelo. Onde dois desenharam a mesma coisa de
formas incompatíveis, escolhi **uma**. A tabela é o índice das escolhas; a
justificativa está na subseção.

| # | Contradição | Escolha | Onde |
|---|---|---|---|
| C1 | relógio do evento: **cena-relativo** (contrato, cena) × **tempo da fonte** (eventos) | cena-relativo | §2.2 |
| C2 | ancoragem: **zona nomeada + ponto** × **pista + registro medido** | **`pista` declarada; `encaixe` derivado do formato** (revisado) | §3.4.2 |
| C3 | a palavra **`registro`**: `faixa\|coluna\|cartela` × `moldura\|cartão\|tela cheia` de `proibicoes.md:24` | o nome fica com a proibição | §3.3.2 |
| C4 | cadência: **enum no briefing** × **derivada do papel** | derivada do papel | §3.4.3 |
| C5 | duração da peça: **Σcenas** × **Σcenas − Σtransições** | subtrai, com `corte` de 0 frames como default | §3.2.2 |
| C6 | `papel: 'legenda'` como evento de cena × legenda como camada de peça | camada de peça; o validador recusa o papel | §3.4.1 |
| C7 | `ponto {x,y}` no schema com resolvedor que falha alto × fora do schema | fora | §5 |
| C8 | skill: estender `canastra-video` × skill nova | skill nova, e `canastra-video` **perde** a seção de coleta | §3.8 |
| C9 | quem escreve `props.json`: `gerar-props.mjs` × compilador | compilador, e o script é retirado no mesmo commit | §3.8 |

### 3.1 O briefing como arquivo

**`fps` é campo, não constante.** `z.number().int().min(1).max(120).default(30)`,
e é dele que toda duração em frame sai. Hoje `FPS = 30` está em `Raiz.tsx:22` e
as composições são registradas com ele em tempo de módulo — o que obriga
`calculateMetadata` ou um registro por briefing. Fica em decisão aberta **D7**
qual dos dois, porque muda a forma do `Raiz.tsx`.

**Formato, não pixel.** `Formato = '9:16' | '1:1' | '4:5'`, com a dimensão
derivada de uma tabela.

**O `16:9` saiu do enum de entrega.** A versão anterior o mantinha em
`formatos: Formato[]` e ao mesmo tempo declarava, em §5, que ele *"é formato
latente, não entrega"* — um briefing com `formatos: ['16:9']` passaria pelo
esquema, passaria pelo compilador e só falharia no render, porque nenhuma
composição o registra. É o padrão do `4:5` na xAI: campo aceito que nada resolve,
lição 4. **Dois enums, dois nomes:** `Zonas['formato']`, que é o **rótulo
geométrico** que `layout()` devolve, continua com `'16:9'`, porque a função de
fato sabe calcular aquelas caixas; `Formato`, que é o **enum de entrega** do
briefing, não. Sem esse desdobramento não havia como o portão pegar o caso.

Medido agora, rodando `layout()` com `razaoFonte: 0.5625` (o `16:9` fica na tabela
como medição, para o registro):

| formato | rótulo que `layout()` devolve | vídeo | sobra ao lado | topo % | base % | lado % |
|---|---|---|---:|---:|---:|---:|
| 1080×1920 | `9:16` | 1080,0 × 1920,0 | 0,00 px | 4,69 | 16,15 | 14,81 |
| 1080×1080 | `1:1` | 607,5 × 1080,0 | 472,50 px | 8,33 | 28,70 | 14,81 |
| **1080×1350** | **`outro`** | 759,4 × 1350,0 | **320,63 px** (29,69% da largura) | 6,67 | 22,96 | 14,81 |
| 1920×1080 | `16:9` | 607,5 × 1080,0 | 1312,50 px | 14,81 | 51,03 | 14,81 |

Tudo [medido aqui]. Duas leituras:

1. **O 4:5 já funciona geometricamente e falha no rótulo.** O ramo genérico de
   `layout.ts:41-63` entrega a coluna e a sobra corretas; `layout.ts:30-33` devolve
   `'outro'` porque a lista de rótulos não o tem. É extensão de um enum, não
   reescrita — exatamente como `05-formatos.md` §6 previu.
2. **A margem vertical está errada em todo formato que não seja o 9:16**, porque
   um `k` só derivado da largura escala também o eixo vertical (`layout.ts:21-27`).
   É a V3/V4 do plano de qualidade, e a Tarefa 3 dele é **pré-requisito** desta
   spec: com N cenas, `layout()` passa a ser chamada com caixas diferentes e um
   `k` só erra em cada uma.

### 3.2 Cena e sequenciamento

#### 3.2.1 `TransitionSeries`, com a dependência declarada

`@remotion/transitions` **não está instalado**: ausente de `package.json`,
`grep -c "remotion/transitions" package-lock.json` = **0**, e
`ls node_modules/@remotion/` lista 25 pacotes sem ele [medido aqui]. As duas
rotas:

- **`Series` + `offset` negativo**, sem pacote novo. A sobreposição empilha as
  duas cenas e a de cima cobre a de baixo — o crossfade seria escrito à mão. E
  nada impede transição maior que a cena adjacente, nem duas transições
  encostadas: os dois saem como vídeo torto, com exit 0.
- **`TransitionSeries`**, instalando `@remotion/transitions` na versão **exata**
  `4.0.530`, igual a todos os outros `@remotion/*` do lock. **Escolhida.** O que
  ela compra é falha alta em cinco invariantes (transição ≤ duração das cenas
  adjacentes; sem duas transições adjacentes; sem dois overlays adjacentes;
  transição e overlay não adjacentes; ao menos uma cena de um dos lados) que, à
  mão, são a lição 3 do `CLAUDE.md` outra vez. Custo: uma dependência nova, e a
  decisão de instalá-la é **D8**.

`TransitionSeries.Overlay` fica **declarado e vazio**, com o motivo escrito: ele
renderiza sobre o corte sem mexer na duração, e o uso canônico dele é *light leak*
e flash — `proibicoes.md:16` proíbe flash branco instantâneo. Registrar que
existe e por que está vazio evita que a próxima sessão o descubra e o ache
grátis.

#### 3.2.2 A transição consome frames — resolução de C5

```
duracaoPecaFrames = Σ duracaoCenaFrames − Σ duracaoTransicaoFrames
```

Durante a transição as duas cenas são renderizadas, então ela não soma tempo: ela
gasta. O desenho de contrato entregou um exemplo com 4 cenas somando 20 s = 600
frames, e o desenho de cena entregou a subtração. **Os dois estão certos ao mesmo
tempo se, e só se, a transição default for `corte`, de 0 frames** — e é a escolha:

- `transicoes` tem **exatamente `cenas.length - 1`** entradas, e a entrada
  default é `{tipo: 'corte'}`, 0 frames. Com ela, `Σcenas` é a duração da peça e o
  exemplo de 600 frames continua válido.
- `duracao.modo` é **obrigatório, sem default**. `somaCenas`: as cenas mandam e
  `alvoS`, se houver, é conferência. `totalFixo`: `alvoS` manda e o compilador
  devolve os frames das transições às cenas, proporcionalmente à duração de cada
  uma, jogando o resto inteiro na cena mais longa para fechar em inteiro.
- **Em `totalFixo` o compilador reescreve a duração que o humano declarou, e isso
  precisa de duas garantias que faltavam.** O briefing é a verdade humana (§2.2);
  mexer nele em silêncio é o contrário disso. (a) A reescrita nunca toca o
  `briefing.json`: ela só existe no `plano.json`, que é artefato gerado. (b) O
  compilador **devolve no diagnóstico, cena por cena, o antes e o depois em frames
  e em segundos**, e o portão de ritmo imprime a linha. Sem isso, "o compilador
  redistribui" é o HTTP 200 que ignora o parâmetro.
- **O desempate do resto inteiro, definido.** "A cena mais longa" não é uma regra
  quando duas cenas empatam, e a versão anterior prometia "de forma
  determinística" sem dar o critério. É: **maior `duracaoCenaFrames`; empate
  resolvido pelo menor índice no array**. O índice é total e já é a ordem que
  §2.2 usa para posicionar cena, então não introduz um segundo critério de
  ordenação no sistema.
- Se `alvoS` vier e `duracaoPecaFrames !== Math.round(alvoS * fps)`, o compilador
  **lança**, com os dois números e a diferença em frames e em segundos. Não é
  `console.warn`: uma peça que sai mais curta que o briefing é o defeito que o
  pedido nomeia.

Sem default em `modo` de propósito — o default aqui seria escolha estética
disfarçada de conveniência. Se o Rafael quiser um, é **D3**.

#### 3.2.3 Timing e apresentação

- **Transição declarada em segundos → `linearTiming({durationInFrames})`.** O
  compilador puro sabe a duração por aritmética, sem importar `remotion`.
- **`springTiming` é permitido e exige `duracaoFramesDeclarada`**, porque a
  duração de uma mola é emergente e o compilador puro não pode chamar `spring()`
  (vem de `remotion`; §5 do plano de qualidade registra que importá-lo acabaria
  com os testes em Node). Um teste no navegador confere
  `timing.getDurationInFrames({fps})` contra o declarado.
- **`presentation` nunca é omitido.** O default do Remotion é `slide()`, que
  ninguém do nosso lado escolheu e que encosta em whip pan (`proibicoes.md:16`).
  O motor não expõe `TransitionSeries.Transition` cru: a transição entra por um
  union fechado — `corte`, `fade`, `wipe` — e o compilador sempre emite
  `presentation` explícito. `iris`, `clockWipe` e `flip` ficam fora (§5).

#### 3.2.4 Onde cada camada vive na árvore

A legenda e a trilha ficam **fora** da `TransitionSeries`. Razão: a legenda é a
fala, e a fala não reinicia porque a imagem trocou. Dentro, ela seria remontada
por cena, `deslocamentoFrames` viraria um número por cena, e **na janela de
crossfade duas legendas ficariam no ar ao mesmo tempo**, com textos diferentes —
bug garantido e invisível em miniatura. Fora, ela é uma camada só, no relógio da
peça, e o compilador entrega os blocos já rebaseados.

Consequência de ordem de árvore, que é a única ordenação que o Remotion tem: a
legenda fica **por cima** da transição e não pisca num crossfade. É o
comportamento certo, e é o oposto do que aconteceria dentro.

### 3.3 Fonte polimórfica

#### 3.3.1 Quatro tipos, e por que o enquadramento é campo

`vídeo`, `foto`, `cor`, `grade`. A `grade` (série 4, tela dividida) recebe nas
células as fontes **simples** — grade dentro de grade é recursão que nenhuma série
pede, e recursão em zod obriga anotação de tipo manual, que é uma segunda fonte
de verdade.

O custo de enquadrar foto está em número, e é por isso que `enquadramento` é
campo e não default escondido.

**Correção de fato, e ela muda a conta.** A versão anterior escrevia *"as 26
fotos da fazenda são 4032×3024, razão 1,3333"*. Está errado como afirmação sobre
as 26. Rodei `ffprobe` nos 26 arquivos de
`base-curada/01-real-verificada/fazenda-medeiros-1250m/` [medido aqui]: todos
gravam 4032×3024, mas **8 deles têm `Orientation = 6`** — `IMG_1405`, `1409`,
`1421`, `1422`, `1423`, `1424`, `1425`, `1426` — e portanto **exibem 3024×4032,
razão 0,75, retrato**. Os outros 18 têm `Orientation = 1` e exibem 1,3333. Então:

| grupo | exibe | razão | `faixa` (contain) no 9:16 | `recorte` no 9:16 |
|---|---|---:|---:|---:|
| 18 fotos, `Orientation 1` | 4032×3024 | 1,3333 | banda 1080×810 → **42,19%** da altura é foto | aproveita 1701 de 4032 px → **joga fora 57,81%** |
| **8 fotos, `Orientation 6`** | 3024×4032 | **0,75** | banda 1080×1440 → **75,00%** da altura é foto | aproveita 2268 de 3024 px → **joga fora 25,00%** |
| 12 packshots, `Orientation 6` | 2304×4096 | **0,5625** | **100,00%**: é 9:16 exato, custo zero | nada a jogar fora |

Tudo [aritmética] sobre as dimensões e orientações [medido aqui]. Duas coisas que
só aparecem depois da correção:

1. **Os packshots orientados são 9:16 nativo.** 2304/4096 = 0,5625 = 9/16,
   exatamente. Honrar a orientação não é higiene: é a diferença entre custo zero e
   57,81% de desperdício no formato principal do catálogo.
2. **O default de enquadramento não pode ser por série (D5), e sim por razão.**
   Um default que joga fora 57,81% da foto paisagem joga fora 25,00% da retrato:
   a escolha não é a mesma decisão nos dois grupos. **D5 é reformulada** abaixo.

**E a fonte desta spec fica corrigida para cima.** `05-formatos.md` §1 escreve
*"`Orientation = 6` **nos 3 conferidos**"* para os 12 packshots, e a versão
anterior desta spec generalizou para 12 sem marca — o que era o defeito que o
cético apontou. Rodei os 12 agora: **os 12 são `Orientation 6` e os 12 são
4096×2304** [medido aqui]. A generalização estava certa por acidente, e agora está
certa por medição; a diferença entre as duas coisas é o assunto da lição 10 do
`CLAUDE.md`. `05-formatos.md` §1 pode trocar "nos 3 conferidos" por "nos 12".

#### 3.3.2 A palavra `registro` — resolução de C3

`proibicoes.md:24-25` diz, textualmente: *"Foto real entra por um registro que
declara a origem (moldura, cartão, tela cheia), nunca como recorte flutuando."*
Um dos desenhos usou `Registro` para nomear onde a manchete mora
(`faixa|coluna|cartela`). São dois conceitos com um nome, e um deles está escrito
no arquivo de proibições da marca.

**O nome fica com a proibição.** `zFonteFoto.registro: 'moldura' | 'cartao' |
'telaCheia'` é **obrigatório, sem default** — é a única forma de a regra da marca
ser cumprida por construção em vez de por lembrança. O conceito de onde o texto
mora passa a se chamar **`encaixe`** (§3.4.2).

**O que cada `registro` desenha, e quais combinações são recusadas.** A versão
anterior apresentou `registro` e `enquadramento` como independentes, e eles não
são — `telaCheia` com `faixa` deixaria 57,81% do quadro em terra chapado e
chamaria isso de "tela cheia". Definindo:

| `registro` | o que desenha | `enquadramento` aceito |
|---|---|---|
| `moldura` | a foto dentro de uma borda de `COR.creme` com o respiro do seguro, e **a borda declara que aquilo é foto** | `faixa` **ou** `recorte` |
| `cartao` | a foto sobre um retângulo de `COR.creme` com `SOMBRA.cartao` (dy 11, blur 24, op 0,17 — tokens, [medido]), ocupando parte do quadro | `faixa` **ou** `recorte` |
| `telaCheia` | a foto preenchendo o quadro inteiro, sem borda e sem cartão | **só** `recorte` |

`telaCheia` + `faixa` é **recusado pelo refinador**, com a mensagem dizendo o
número: a fração de quadro que sobraria chapada, calculada da `razaoExibicao`
declarada. Recusar sem o número seria pedir que a próxima sessão redescubra o
porquê. Os outros quatro pares são válidos.

#### 3.3.3 Como `razaoExibicao` é medida — e o mecanismo que faltava

**Esta é a correção mais grave da revisão.** A versão anterior escrevia
*"`razaoExibicao` é medida, nunca lida do container … quem preenche o campo é
`sondar()`, não o dedo"* — e `sondar()` **não serve para foto**. Reproduzi
[medido aqui], empacotando `src/motor/sondar.ts` com `esbuild` e rodando sobre
`base-curada/01-real-verificada/torrefacao-uberlandia-875m/packshot-classico/Classico (5).jpg`:

```json
{"largura":4096,"altura":2304,"rotacao":0,"razao":1.7777777777777777,
 "duracao":0.04,"fps":25,"fpsMedio":25,
 "codificada":{"largura":4096,"altura":2304}}
```

Três defeitos numa resposta: devolve **1,7778**, que é a mentira paisagem, quando
a razão de exibição é **0,5625**; devolve `rotacao: 0` num arquivo com
`Orientation = 6`; e inventa `fps: 25` e `duracao: 0.04` para uma foto parada. A
causa está em `sondar.ts:189-199`: ele honra `side_data_list.rotation`, que é o
**displaymatrix**, metadado de vídeo, e `grep -in "exif\|orientation" src/motor/sondar.ts`
= **0 linhas** [medido aqui]. A spec anterior nomeava como mecanismo de medida
justamente a função que reintroduz a armadilha que o campo existe para evitar.

**Este é o terceiro caso de metadado de rotação ignorado, e o padrão é o
achado.** (1) `pl.mp4` grava 1024×576 com `displaymatrix -90` e exibe 576×1024 —
foi o que motivou `sondar()`. (2) Os três recortes de embalagem em
`projetos/01-private-label/public/assets/` são **4096×2304, deitados**, com o
`Orientation 6` da origem nunca aplicado — medi os PNG e o laudo
(`instagram/assets/embalagem/suave-250g.json` grava `"dimensoes": [4096, 2304]`)
[medido aqui]. (3) `sondar()` sobre foto. **Regra, não acidente:**

> Em todo ponto onde este motor recebe um arquivo de imagem ou vídeo, a dimensão
> de exibição é **derivada de metadado de rotação**, e o metadado tem dois nomes
> por tecnologia: `side_data_list.rotation` (displaymatrix, contêiner de vídeo) e
> EXIF `Orientation` (JPEG/TIFF). Ler `width`/`height` sem os dois é o defeito
> padrão deste repositório, e ele já custou três rodadas.

**A decisão: estender `sondar()`, não criar outro mecanismo.** Motivo medido — o
**mesmo** binário que `sondar()` já resolve expõe o EXIF. Rodei
`ffprobe -show_frames -read_intervals '%+#1'` sobre o mesmo packshot [medido
aqui] e `frames[0].tags` traz `"Orientation": "    6"`, ao lado de `Make`,
`Model`, `DateTimeOriginal` e `GPSAltitude`. Nenhuma dependência nova, nenhum
parser de EXIF escrito à mão. O que muda em `sondar.ts`:

- acrescenta `-show_frames -read_intervals '%+#1'` à chamada (um frame só: o
  custo não é o do arquivo inteiro);
- lê `frames[0].tags.Orientation`, **com `Number()` sobre o valor**, porque o
  ffprobe o devolve preenchido de espaços (`"    6"`) e comparação de string
  falha em silêncio;
- mapeia `Orientation` → graus pela tabela EXIF, e troca largura por altura em
  `5, 6, 7, 8`;
- o campo `rotacao` passa a ser `{fonte: 'displaymatrix' | 'exif' | 'nenhuma';
  graus: number}`, porque um `0` que significa "não achei" e um `0` que significa
  "medi e é zero" são fatos diferentes e um deles é um alarme;
- `duracao` e `fps` passam a ser `null` quando o fluxo tem um frame só, em vez de
  `0.04` e `25`. Um número inventado é pior que a ausência — lição 3.

Isto **não é opcional para o esquema**: `razaoExibicao` no briefing é campo de
número, então nada impede o dedo de escrever `1.3333`. E o dedo já escreveu: o
protótipo `out/_spec-briefing/b-jornada-foto.json` declara
`razaoExibicao: 1.3333` para `IMG_1421.JPG` e `IMG_1424.JPG`, e **os dois são
`Orientation 6`**, ou seja 0,75 [medido aqui]. Duas das três fotos daquele
briefing estão erradas pela razão exata que esta seção descreve. Logo o portão de
ritmo (§3.9.1) **confere `razaoExibicao` declarada contra `sondar()` medida**, com
tolerância de 0,005, e reprova: o campo existe para ser conferido, não para ser
acreditado.

**D5, reformulada.** Não é "default de enquadramento por série". É: *dado que o
custo de `faixa` é 42,19% de fundo chapado na foto paisagem e 25,00% na retrato,
e que o packshot orientado tem custo zero, qual dos três grupos aceita `faixa` e
qual exige `recorte`?* A pergunta antiga não era decidível porque a medição estava
errada.

### 3.4 Evento de texto

#### 3.4.1 Três papéis de evento, quatro papéis de tipografia — resolução de C6

Os dois desenhos que tocaram o assunto chegaram à **mesma** tabela de famílias, e
ela fica como está:

```ts
FAMILIA_DO_PAPEL = {
  manchete: 'manchete',   // Archivo Black,  alturaLinha 1,088 (hhea)
  dado:     'dado',       // IBM Plex Mono,  avanço 0,6 em fixo, alturaLinha 1,3
  etiqueta: 'dado',       // rótulo/carimbo: mono resolve
  legenda:  'corpo',      // Inter Bold,     alturaLinha 1,21
};
```

O mapeamento é **obrigatório, não cosmético**. Medido agora:
`formaTextoTela({texto:'SERIE 10', papel:'etiqueta', …})` →
`TypeError: Cannot read properties of undefined (reading 'x')` [medido aqui],
porque `PapelTexto` é `'manchete' | 'dado'` (`texto-forma.ts:49`) e é indexado
direto em `GLIFOS`, cujas chaves são `manchete`, `corpo`, `dado`.

**Mas `legenda` não é papel de evento.** Um dos desenhos colocou `'legenda'` no
enum de `EventoTexto`; isso permitiria um briefing declarar legenda dentro de uma
cena, e §3.2.4 acabou de tirar a legenda de dentro das cenas. O validador
**recusa** `papel: 'legenda'` num evento, com a mensagem apontando o campo
`legenda` do briefing. A tabela acima continua tendo a linha porque ela nomeia a
família que a camada `Legenda` usa.

**O papel `dado` está inteiro medido e nunca foi desenhado.** `tokens.ts:12`
declara a família; `glifos.ts` registra o avanço **0,6 em constante**; e nenhum
componente o desenha. O avanço constante é a razão de o mono estar nos tokens:
duas linhas com a mesma contagem de caracteres têm a mesma largura exata, então
uma tabela de preço alinha por construção, sem medir nada. As séries 10 e 11 o
pedem por nome.

**A cerca do `dado`, da lição 22 do `CLAUDE.md`:** um evento de papel `dado` cujo
texto casa com `/^F[:.]|VAL|LOTE/i` é **recusado**. Lote, fabricação e validade
saíram `F:23.2025` (mês que não existe) e `F:12.2025` (plausível, e por isso
pior). Informação regulatória falsa não entra em peça de e-commerce, e
`05-formatos.md` §2 já transcreveu a regra.

#### 3.4.2 `pista` declarada, `encaixe` derivado — resolução de C2

Um desenho propôs `zona`: união de nome (`faixaSuperior`, `colunaLateral`,
`centroSeguro`, `rodape`) com `ponto {x, y}`. O outro propôs `pista`
(`topo`, `principal`, `rodape`, `tela`) mais uma **lista de preferência** de
encaixe resolvida por medição. **Fica a segunda, com uma emenda**: a `pista` é
declarada, o `encaixe` é **derivado** (a lista de preferência sai do briefing —
ver o fim desta subseção). O motivo de escolher pista é mecânico: ela dá **uma
caixa nomeada por camada**, e é isso que torna a sobreposição decidível — em parte
por construção, em parte por medição, e a fronteira entre as duas está escrita na
lista de invariantes abaixo, porque a versão anterior dizia "impossível por
construção" das quatro pistas e isso é falso em três dos quatro formatos.
Sobreposição é um defeito real e medido do motor hoje. Esta subseção tem quatro
partes, porque a versão anterior afirmava
isso em uma frase e não sustentava nenhuma delas: **o número remedido**, **a causa
mecânica**, **a geometria com números** e **a derivação do encaixe**.

##### A sobreposição, remedida: o número anterior descrevia outra grandeza

A versão anterior escreveu *"a caixa da manchete passa **353,20 px** por dentro da
caixa da legenda"*, com 364,00 no 4:5 e 594,31 no 16:9, marcados [medido aqui].
**O rótulo estava errado.** 353,20 é `manchete.fim − legenda.y`, não interseção —
e é maior que a caixa inteira da legenda (172,80 px de altura), o que torna a
frase impossível de ser verdade. Lição 10 do `CLAUDE.md`, outra vez: li um número
certo e escrevi o nome errado em cima dele.

Remedi rodando `layout()` com `razaoFonte: 0.5625` e calculando a interseção nos
**dois eixos** [medido aqui]:

| formato | interseção em x | interseção em y | área | % da caixa da legenda | `manchete.fim − legenda.y` (o número antigo) |
|---|---:|---:|---:|---:|---:|
| 1080×1920 | 760,00 px | **0,00 px** | **0** | **0,0%** | −867,20 |
| 1080×1080 | **90,20 px** | 172,80 px | 15.586,56 px² | 15,67% | 353,20 |
| 1080×1350 | **102,35 px** | 216,00 px | 22.107,60 px² | 14,07% | 364,00 |
| 1920×1080 | **122,56 px** | 172,80 px | 21.177,60 px² | 22,26% | 594,31 |

Três fatos que a grandeza errada escondia:

1. **No 9:16 não há sobreposição nenhuma** — interseção 0,00 px. O defeito é dos
   formatos em que o vídeo vira coluna, e a frase "sobreposição é defeito real e
   medido do motor" precisava dessa qualificação.
2. **Os 90,2 px que a auditoria relatou estão reproduzidos, e são a interseção em
   x no 1:1.** A versão anterior os deixou como **[relatado]** e não reproduzidos,
   supondo que fossem "do bloco de texto já recortado". Não eram: são a caixa
   crua, no eixo x. A marca sai de [relatado] e passa a [medido aqui].
3. **O cético que achou este defeito errou pelo mesmo motivo.** Ele escreveu que
   *"a interseção real é 100% da caixa da legenda nos três formatos"* — mediu só
   o eixo y. Medi os dois: é 15,67% / 14,07% / 22,26% da área. Registro isto não
   para ganhar o ponto, e sim porque é a terceira aparição do mesmo erro nesta
   spec: **interseção de caixas é grandeza de dois eixos, e medir um só dá um
   número plausível** — e plausível é pior que absurdo, lição 22.

##### A causa mecânica, e o conserto de uma linha

O defeito não é "as zonas são mal escolhidas". É uma inconsistência interna de
`layout.ts:68-73`:

```ts
x:       Math.max(seguro.x, video.x + 16 * k),
largura: Math.min(seguro.largura, video.largura - 32 * k),
```

A **largura** é calculada supondo que `x` seja `video.x + 16k` (é o que
`−32k` significa: 16 de respiro em cada lado do vídeo); o **`x`**, porém, usa
`seguro.x`. Quando o vídeo é coluna, `video.x = 0` e `seguro.x = 160`, então a
caixa desliza 144,00 px para a direita carregando a largura inteira, e a borda
direita dela **vaza o vídeo**. Medido [medido aqui]: a legenda passa da borda
direita do vídeo em **128,00 px** no 1:1, 128,00 px no 4:5 e 227,56 px no 16:9. É
exatamente nesse vazamento que a coluna da manchete mora — e 735,50 − 645,30 =
**90,20 px**, o número da tabela acima. A sobreposição não é geometria de zona: é
um `min` que esqueceu de onde a caixa começa.

Uma linha conserta:

```ts
const x = Math.max(seguro.x, video.x + 16 * k);
const legenda: Caixa = {
  x,
  y: seguro.y + seguro.altura - alturaLegenda,
  largura: Math.min(seguro.x + seguro.largura, video.x + video.largura - 16 * k) - x,
  altura: alturaLegenda,
};
```

Medido com a correção aplicada numa cópia [medido aqui]: a interseção em x vai a
**0,00 px nos quatro formatos**, e o vazamento vira −16,00 / −16,00 / −28,44 px,
isto é, a legenda fica dentro do vídeo com o respiro pretendido. O 9:16 não muda
em nada (x 160, largura 760,00). **Custo honesto:** a largura útil da legenda no
1:1 cai de 575,50 para **431,50 px** (−25,0%), no 4:5 de 727,38 para 583,38
(−19,8%) e no 16:9 de 550,61 para 294,61 (−46,5%). Isso empurra a busca binária
de corpo para baixo nesses formatos e **toca D6/V11** (corpo de legenda que
encolhe) — não é conserto de graça, e essa dependência tem de estar no plano.

`tests/layout.test.ts` tem hoje 4 testes e um deles é *"as zonas de video e de
manchete nao se sobrepoem no 1:1"* [medido aqui]. Falta o par que importa:
**legenda × manchete**, nos quatro formatos, nos dois eixos. É ele que converte
este parágrafo em invariante.

##### A geometria de pista, com números

Este era o quarto furo do cético e ele estava certo: a spec escolhia pista+encaixe
*"porque a pista torna sobreposição impossível por construção"* e nunca definia a
geometria. Sem números, a frase é só uma frase. Definindo.

**Uma pista de evento é uma faixa horizontal de uma coluna de texto**, e as duas
coisas são derivadas, nunca declaradas. (As pistas que **não** são de evento —
`rodape` e `tela` — não são frações da coluna: são caixas que o motor já calcula.
Ver a tabela abaixo.)

```
colunaDeTexto = sobra >= LIMIAR_DE_COLUNA
                  ? intersecao(zonas.manchete, zonas.seguro)   // ao lado da imagem
                  : seguroDoVideo                              // sobre a imagem
LIMIAR_DE_COLUNA = 0,22 × largura do quadro      [escolhido]
```

O limiar é `[escolhido]`, e a razão é medida: as sobras são **0,00 px** no 9:16,
**472,50** no 1:1 (43,75% da largura), **320,63** no 4:5 (29,69%) e **1312,50** no
16:9 (68,36%) [medido aqui]. Qualquer limiar entre 0 e 29,69% separa os mesmos
grupos; 0,22 fica no meio do vão e não está encostado em nenhum lado.
`seguroDoVideo` é a §3.5: o seguro **do vídeo**, não do quadro.

**A interseção com `zonas.seguro` no primeiro ramo não é enfeite.** A versão
anterior escrevia *"caixa da sobra"*, e a caixa da sobra não é uma caixa que o
motor use: `zonas.manchete` **vaza o seguro** — medido no 1:1, `manchete` vai de
x 645,30 a 1.042,20 contra um seguro de 160,00 a 920,00, e desce até y 950,40
contra 770,00 [medido aqui] —, e `texto-forma.ts:193` já recorta contra
`zonas.seguro` por esse exato motivo, com o comentário que chama o recorte de
*"carregando, não cosmético"*. A coluna de texto é a caixa recortada, e é por isso
que ela mede 274,70 × 640,40 px no 1:1, não 472,50 × 1080,00 [medido aqui].

**As quatro pistas — e só duas delas são fração da coluna:**

| pista | caixa | quem escreve nela |
|---|---|---|
| `topo` | fração **0,00–0,24** da altura da coluna | evento de papel `etiqueta` ou `manchete` |
| `principal` | fração **0,24–0,76** da altura da coluna | evento de papel `manchete` ou `dado` |
| — (folga de baixo) | fração **0,76–1,00** | **ninguém.** É folga, e só: ela existe para `principal` não encostar na legenda |
| `rodape` | **literalmente `zonas.legenda`** | **só a camada `Legenda`.** Nenhum evento a declara |
| `tela` | **literalmente `zonas.seguro`** | a cartela. Conflita com `topo` e `principal`; **não** com `rodape` |

**Correção da revisão de 01/10/2026: as duas últimas linhas descreviam caixas que
o motor não tem.** A versão anterior punha `rodape` como a faixa 0,76–1,00 da
coluna e `tela` como a coluna inteira. Medido contra o `layout()` da árvore de
trabalho de 01/10/2026 — que já traz o §0 (`MARGEM` em fração) e o conserto da
largura da legenda, os dois conferidos no arquivo [medido aqui]:

| formato · razão da fonte | `rodape` da spec anterior (0,76–1,00 da coluna) | `zonas.legenda`, que a camada `Legenda` desenha | interseção |
|---|---|---|---:|
| 9:16 · 0,5625 | x 160,00 · y 1.248,77 · 760,00×364,03 | x 160,00 · y 1.305,60 · 760,00×307,20 | contém a legenda |
| 1:1 · 0,5625 | x 645,30 · y 720,58 · 274,70×186,62 | x 160,00 · y 734,40 · 431,50×172,80 | **0 px²** |
| 4:5 · 0,5625 | x 785,02 · y 900,72 · 134,98×233,28 | x 160,00 · y 918,00 · 583,38×216,00 | **0 px²** |
| 16:9 · 0,5625 | x 712,50 · y 720,58 · 923,06×186,62 | x 284,44 · y 734,40 · 294,61×172,80 | **0 px²** |
| **1:1 · 4/3** | x 160,00 · y 661,82 · 760,00×153,58 | x 160,00 · y 734,40 · 760,00×172,80 | **61.560 px²** |

Duas caixas diferentes para a mesma coisa — a que a camada desenha e a que o
portão confere. Nos três formatos de coluna elas são **disjuntas**, e com fonte
paisagem no 1:1 elas se sobrepõem em 61.560 px² sem que nenhuma contenha a outra:
o pior dos dois mundos, porque nem a conferência cobre o que é desenhado nem o
desenho cabe no que é conferido. O mesmo vale para `tela`: `formaTextoTela` usa
`zonas.seguro` para `modo: 'cartela'` (`texto-forma.ts:193`, [medido aqui]), não a
coluna. E a `manchete` que o motor calcula no 9:16 cai inteira em `topo` (y
96,00–441,60 contra uma pista de 96,00–460,03), não em `principal` — a pista
0,24–0,76 tem interseção **zero** com ela [medido aqui].

As frações continuam `[escolhido]`, agora amarradas ao número certo: a **folga de
baixo** recebe 0,24 porque a caixa de legenda é `altura * 0.16` do **quadro** e,
dentro do seguro do 9:16 — 1.516,80 px de 1.920,00 [medido aqui] —,
307,20 / 1.516,80 = **0,2025**; 0,24 dá a folga da segunda linha que a
Tarefa 7 do plano de qualidade promove a invariante. `topo` recebe a mesma altura
que a folga de baixo porque uma faixa superior mais baixa que a inferior lê como
desalinhamento, e o que sobra, 0,52, é `principal`.

**Em que sentido exato a pista mata a sobreposição — e onde ela não mata por
construção.** Quatro invariantes, as quatro testáveis em Node sem render:

1. **`topo` × `principal`: por construção.** As duas partilham o intervalo em x (o
   da coluna), logo a disjunção é decidida só em y, e em y elas são disjuntas por
   definição: 0,00–0,24 e 0,24–0,76.
2. **`rodape` × pista de evento: por medição, e ela depende do conserto de
   `layout.ts:69-71`.** Aqui a versão anterior afirmava o contrário do que o motor
   faz: as quatro pistas **não** partilham o intervalo em x, porque `rodape` é a
   caixa de legenda e ela mora sobre o **vídeo**, enquanto a coluna de evento mora
   na **sobra**. Antes do conserto da largura, no 1:1 eram x 160,00–735,50 contra
   645,30–920,00; a invariante "decidida só em y" é falsa exatamente nos três
   formatos em que a sobreposição existe — e verdadeira só no 9:16, onde a
   sobreposição já é 0,00.

   **Na árvore de 01/10/2026 a invariante vale**, e vale por **três** coisas, não
   por uma. Medido: `intersecao(topo, rodape)` e `intersecao(principal, rodape)` são
   **0,00 px² nas oito combinações** (4 formatos × 2 razões de fonte, 0,5625 e 4/3),
   e `zonas.legenda ∩ zonas.manchete` também é **0,00 px² nos quatro formatos**
   [medido aqui]. Tire uma das três e ela cai:

   - **sem o conserto da largura da legenda**, `intersecao(principal, rodape)` dava
     **1.723,18 px²** no 1:1, **540,41** no 4:5 e **10.327,35** no 16:9 com fonte
     retrato [medido aqui];
   - **com o conserto e sem o §0** (`MARGEM` em pixel), a combinação 1:1 × fonte
     paisagem ainda dava **22.429,50 px²** [medido aqui], porque ali a sobreposição
     é em **y** — a coluna é `seguroDoVideo` e a faixa `principal` dela descia até
     y 626,71 enquanto a legenda começava em y 597,20, 29,51 px acima — e conserto
     de largura não toca o eixo y. É a terceira vez nesta spec que medir um eixo só
     daria o número errado;
   - e **`rodape` ser a caixa real**: com a `rodape` da spec anterior, o 1:1 ×
     paisagem dá **61.560 px²** mesmo na árvore consertada (a tabela acima).

   Ou seja: o que mata a sobreposição é `MARGEM` em fração + conserto da largura +
   `rodape` ser a caixa real, não a partilha de x. E por isso o par
   legenda × manchete é **teste**, não parágrafo.
3. `tela` é a única pista que cruza as outras, e o cruzamento com `rodape` é
   **intencional e já defendido por escrito** em `PecaVideo.tsx:115-120`: a
   legenda corre por cima da cartela.
4. Duas camadas na mesma pista no mesmo frame é recusa, e o dono da recusa é o
   portão `ritmo`, não o refinador (§3.9.1) — porque ela só é decidível depois da
   conversão para frames.

**Nada disso vira tarefa nova no plano:** o plano de 01/10/2026 já escreve
`rodape: z.legenda` e `tela: z.seguro` em `pistas()` (Tarefa 4, Step 4), já tem o
conserto da largura da legenda (Tarefa 4, Step 3, item 5) e já testa
`pistas(z).rodape).toEqual(z.legenda)`. Era a **spec** que estava atrasada em
relação ao plano, e esta subseção é que foi corrigida.

##### `encaixe` é derivado, não declarado — correção de C2

A versão anterior punha `encaixe?: ('faixa'|'coluna'|'cartela')[]` no briefing,
como lista de preferência. **Sai do briefing**, por três razões, e a primeira é
mecânica:

1. **`faixa` × `coluna` não é escolha, é consequência do formato.** `layout()` dá
   faixa no 9:16 (`layout.ts:37-40`) e coluna na sobra nos outros
   (`:56-63`); no 9:16 a sobra é **0,00 px** [medido aqui], então
   `encaixe: ['coluna']` ali é insatisfazível. Um campo que o motor não pode
   honrar é o HTTP 200 que ignora o parâmetro — o mesmo princípio com que C7
   expulsou `ponto {x,y}`. A spec anterior aplicava o princípio num campo e o
   violava no outro.
2. **`encaixe` tinha 3 valores e o motor tem `Modo` com 2** —
   `texto-forma.ts:46`: `export type Modo = 'sobreImagem' | 'cartela'` [medido
   aqui] — e nenhum mapeamento estava escrito.
3. Uma "lista de preferência" sem regra para o caso de nenhum item passar é um
   silêncio no meio do contrato.

**A derivação, inteira:**

```
encaixe(pista, formato) =
  pista === 'tela'                      → 'cartela'     → Modo 'cartela'
  sobra < LIMIAR_DE_COLUNA (9:16)       → 'faixa'       → Modo 'sobreImagem'
  senão (1:1, 4:5)                      → 'coluna'      → Modo 'sobreImagem'
```

`coluna` e `faixa` caem no mesmo `Modo` porque a diferença entre as duas **não é
de desenho de texto, é de caixa**: as duas desenham creme sobre o que estiver
atrás, e quem muda é a `Caixa` que chega. Assim o mapeamento 3→2 fica explícito e
`texto-forma.ts` não ganha um terceiro modo.

##### O piso de dominância, com número

Era citado duas vezes como critério de escolha e nunca definido. Definindo, e a
definição precisa ser de **área**, não de corpo, porque `proibicoes.md:19` fala de
*elemento dominante* e o que domina um quadro é a mancha, não o tamanho da letra:

```
dominancia(evento)  = área do bloco de texto ÷ área do quadro
dominancia(legenda) = (zonas.legenda.largura × corpo × entrelinha × 2) ÷ área do quadro
PISO_DE_DOMINANCIA  = 1,25 × dominancia(legenda)                  [escolhido]
```

**A referência da legenda são duas linhas cheias da caixa dela, não o bloco que
estiver no ar.** Isto precisa estar escrito: *"a legenda no mesmo quadro"* é
ambíguo quando o evento vive mais tempo que um bloco — a manchete de
`01-private-label` dura 60 frames e atravessa **quatro** blocos (`ter sua`,
`própria marca`, `de café`, `especiais? Aqui`) [medido aqui], e o veredito muda
conforme o bloco escolhido. Duas linhas cheias é o pior caso, não depende de qual
bloco calhou de estar no ar, e não introduz número novo: o corpo é
`LEGENDA.corpoEm1080` escalado e a entrelinha é `LEGENDA.entrelinha`. As duas
linhas são a invariante que a Tarefa 7 do plano de qualidade promove.

O piso é relativo à legenda **de propósito**: o defeito medido é que o elemento
que deveria dominar é menor que a legenda, e um piso absoluto em % do quadro não
captura isso — ele passaria numa peça sem legenda e reprovaria numa com legenda
grande. O fator 1,25 é `[escolhido]`: é o menor fator que garante que a diferença
seja visível em miniatura e não um empate. Os corpos medidos com
`'SUA PRÓPRIA MARCA DE CAFÉ'` mostram o tamanho do buraco a fechar:

| formato | `sobreImagem` | `cartela` | legenda |
|---|---:|---:|---:|
| 1080×1920 | 99 px | 152 px | 78 px |
| **1080×1080** | **54 px** | 125 px | 78 px |
| **1080×1350** | **26 px** | 152 px | 78 px |

Tudo [medido aqui]. O plano de qualidade mediu a mesma coisa com um texto mais
longo (`'CAFE ESPECIAL DA SERRA DA CANASTRA'`) e achou 90 / 44 px — números
diferentes, mesmo veredito. **No 1:1 e no 4:5 o elemento que deveria dominar é o
menor texto do quadro**, e no 4:5 ele sai a um terço do corpo da legenda. Nenhum
piso de corpo conserta isso sozinho: a coluna estreita nasce de `layout.ts:58-63`
dar à manchete `sobra * 0.84`. É **D2**, e com manchete plural ela deixa de ser
adiável.

**E o piso de dominância entra na lista do portão `ritmo`** (§3.9.1), senão
`proibicoes.md:19` continua sem quem a cumpra — que era a quarta parte do achado.

**O que o piso de fato reprova, remedido em 01/10/2026 — e a frase anterior era
falsa.** Estava escrito: *"ligado hoje, o piso reprova a peça `01-private-label`
no 1:1 e no 4:5, porque 54 px e 26 px de corpo não chegam a 1,25× de 78 px de
legenda por nenhuma conta de área"*. A frase (a) comparava **corpo** para concluir
sobre **área**, que é o erro que esta própria subseção acabou de proibir; (b)
estava **sem marca de procedência**, violando a regra da página de abertura desta
spec; e (c) falava da peça, que renderiza em `modo: 'cartela'`
(`props.json:manchete.modo`, [medido aqui]) — e em cartela o piso **passa com
folga**. Rodando a definição de área acima sobre `'SUA PRÓPRIA MARCA DE CAFÉ'`
[medido aqui]:

| formato | piso (1,25 × legenda) | `sobreImagem` | veredito | `cartela` | veredito |
|---|---:|---:|---|---:|---|
| 1080×1920 | 6,861% | 10,435% | **domina** (1,901×) | 24,245% | **domina** (4,417×) |
| 1080×1080 | 6,925% | 4,800% | **reprova** (0,866×) | 43,102% | **domina** (7,780×) |
| 1080×1350 | 7,490% | 0,890% | **reprova** (0,149×) | 34,482% | **domina** (5,754×) |

Os múltiplos entre parênteses são **× a dominância da legenda**, não × o piso — o
piso é 1,25× dela, então *domina* é o mesmo que *múltiplo ≥ 1,25*. Medido na
árvore de 01/10/2026, com §0 e com o conserto da largura.

**E os vereditos não dependem dessa versão da geometria.** Medido também no
`layout()` **pré-§0** — que é o com que a tabela de corpo acima foi medida: pisos
de 6,861% / 9,236% / 9,339% contra manchas de 10,435% / 4,800% / 0,890% em
`sobreImagem` e 24,245% / 34,332% / 34,482% em `cartela` [medido aqui]. **Os seis
vereditos são os mesmos nas duas versões**; o que muda é a margem. (A única célula
da tabela de corpo que o §0 move é a cartela do 1:1: **125 → 152 px**, porque a
área segura deixou de ser comida pela margem de base.)

**De que caixa saem esses números, e o que não se pode deduzir deles.** A coluna
`sobreImagem` mede na caixa de manchete de **hoje** —
`intersecao(zonas.manchete, zonas.seguro)`, a coluna inteira (`texto-forma.ts:193`).
As **pistas** são fatias dela: `topo` recebe 24% da altura da coluna e `principal`
52%, logo corpo menor e mancha menor. Consequência que importa ler na direção
certa: um **reprova** desta tabela vale para qualquer pista (caixa menor não começa
a dominar), mas um **domina** **não** se transfere — o plano mede, para a peça de
prova com fonte paisagem, 79 px e **5,297%** em `topo` no 9:16 contra o piso de
6,861%, isto é reprovação [relatado]. O `01-private-label` não é afetado porque
declara `pista: 'tela'`, cuja caixa é `zonas.seguro` — a mesma da coluna `cartela`.

Três leituras, e a terceira é a lição:

1. **O piso reprova a manchete em coluna (`sobreImagem`) no 1:1 e no 4:5, não a
   peça.** O que ele reprova é a escolha de pôr a manchete na coluna lateral —
   exatamente a **D2** — e a reprovação é de área: 0,866× e 0,149× a dominância da
   legenda, contra um piso de 1,25×.
2. **Em cartela ele passa nos três formatos**, por 4,4× a 7,8×. Então o
   `01-private-label` com `pista: 'tela'` não é bloqueado pelo piso em nenhum
   formato que o motor registra, e §7.1 foi corrigida de acordo.
3. **Corpo não prevê área, e erra para os dois lados.** No 1:1 a razão de corpo é
   54/78 = **0,692** e a de área **0,866** — o corpo subestima; no 4:5 a de corpo é
   26/78 = **0,333** e a de área **0,149** — o corpo superestima em mais de duas
   vezes. Não há fator de correção: quem decide pelo corpo erra em direções opostas
   em dois formatos da mesma peça. É a mesma falha que pôs `353,20 px` nesta spec
   com o nome de interseção: medir uma grandeza e concluir sobre outra devolve um
   número plausível, e plausível passa na revisão.

#### 3.4.3 Cadência: derivada do papel — resolução de C4

Um desenho propôs um enum de preset no briefing (`pousoPorPalavra`,
`pousoDoBloco`, `corteSeco`, `cortePonta`); o outro, uma tabela `papel → cadência`
(`palavra`, `linha`, `bloco`). **Fica a tabela**, e o briefing não tem o campo.

```ts
CADENCIA_DO_PAPEL = {manchete: 'palavra', dado: 'linha', etiqueta: 'bloco'};
```

Três razões:

1. **A cadência de `dado` é forçada por medição, não por gosto.**
   `duracaoDaFrase('R$ 39,90')` trata `R$` e `39,90` como dois irmãos; um cartão
   de preço que revela `R$` e o número 3 frames depois lê como defeito. Cada linha
   de um `dado` é um **campo**, e o stagger é por linha.
2. Um botão que o briefing pode girar sem saber avaliar produz inconsistência
   silenciosa entre peças da mesma série — é a lição 8 do `CLAUDE.md` (coesão de
   série) aplicada a tempo em vez de cenário.
3. `corteSeco` e `cortePonta` do enum proposto descrevem a **legenda**, não um
   evento: `corteSeco` é o que `Legenda.tsx` faz hoje e `cortePonta` é a Tarefa 1
   do plano de qualidade. Nenhum dos dois é escolha de briefing.

O stagger continua `TEMPO.stagger = 3` frames a 30 fps, e continua sendo **nosso
valor medido** contra os 1,8 f do default de biblioteca (divergência D2 do plano).

### 3.5 Layout: o que muda e o que não muda

Muda: **margem em fração do eixo próprio** (Tarefa 3 do plano, pré-requisito), o
rótulo `4:5` no enum, **a largura da caixa da legenda** (§3.4.2: o `min` que
esquece de onde a caixa começa, uma linha), as quatro pistas de §3.4.2, e uma
segunda camada de margem — `seguroDoVideo`, distinta do seguro do quadro, porque
um evento em encaixe `faixa` mora **sobre** o vídeo e o vídeo nem sempre é o
quadro.

Não muda, e a §5 do plano de qualidade explica cada um: o encaixe `contain` nos
dois eixos (é o que faz o 1:1 ser reenquadramento), `intersecao(manchete, seguro)`,
`alinhaHorizontal: 'flex-start'` nos dois modos, `linhasDeFolga = 1` na cartela,
`fundo: COR.terra`, a busca binária de corpo com a rede `while (corpo > 1 &&
!cabe(corpo)) corpo--`, e a medição de avanço lida do `hmtx` dos próprios `.ttf`.
**Uma composição só servindo todos os formatos continua sendo a propriedade
central** — nenhuma cena, nenhum 4:5 e nenhum briefing cria um `PecaFeed`.

### 3.6 Áudio: locução e trilha — a ausência A4

**Correção estrutural.** A versão anterior tinha um só campo, `trilha?: Trilha`,
com o comentário *"obrigatória se não houver locução"* — e **não existia campo de
locução em nenhuma parte do esquema**. O comentário condicionava a obrigatoriedade
da trilha a um campo inexistente, e sem locução a peça de foto parada sai muda
duas vezes: sem voz e sem faixa. O tipo `Audio` de §2.3 fecha isso, e o protótipo
`out/_spec-briefing/a-private-label.json` já tinha a forma certa
(`audio.locucao {arquivo: "pl.wav", ganhoDb: 0, aparaAntesS: 1.14}`) — a spec é
que a perdeu ao consolidar.

O motor precisa de `<Audio>` **fora** da `TransitionSeries`, no relógio da peça,
para as duas faixas, porque:

- peça de foto parada **não tem** fonte com som, e sem faixa o Reel perde
  elegibilidade para não-seguidor (`05-formatos.md` §3, **[oficial]**);
- "mudo" no catálogo significa **sem locução**, nunca sem faixa;
- **5 das 12 séries entregam Reel a partir de foto parada** — 1, 2, 5, 10, 11
  [aritmética sobre `05-formatos.md` §4] — e a série 4 é explicitamente "sem voz,
  **com** faixa de áudio";
- a legenda nasce da locução: é dela que vem a transcrição, e é o
  `locucao.aparaAntesS` que ancora o rebase (§2.2.1). Sem o campo, o rebase não
  tem âncora com N cenas.

**A regra de obrigatoriedade, agora escrita sobre campos que existem:**

> `audio` é obrigatório. `audio.locucao` e `audio.trilha` podem ser `null`, mas
> **não os dois ao mesmo tempo**, e o refinador recusa `{locucao: null, trilha:
> null}` citando o critério de elegibilidade **[oficial]**. `trilha: null` só é
> aceito quando há locução. Ambos preenchidos é o caso normal de peça narrada com
> música por baixo.

**Como `ganhoDb` se relaciona com o alvo de −14 LUFS, e por que não há LUFS no
briefing.** `scripts/normalizar-audio.mjs` roda **depois** do render, sobre o MP4
já mixado, com `-c:v copy`, e leva a **mistura** a `AUDIO = {lufs: -14, picoDbtp:
-1}` dos tokens [medido: `tokens.ts` declara os dois, e
`normalizar-audio.mjs:90` os lê]. Logo:

- `ganhoDb` é **relação entre as faixas**, não nível absoluto. Ele decide quanto a
  trilha fica abaixo da voz; o nível final é do normalizador.
- Um campo de LUFS no briefing seria uma segunda verdade que o normalizador
  sobrescreve sem avisar — o `alvoLufs`/`picoMaximoDbtp` que o protótipo trazia
  **não** entra no esquema, por isso.
- Ponto de partida para o mix, `[escolhido]`: `locucao.ganhoDb = 0` e
  `trilha.ganhoDb = -18`, que é a faixa usual de música sob voz. É `[escolhido]`,
  não medido, e **não há medição nossa que o sustente** — a primeira peça com as
  duas faixas tem de medir o resultado e o número volta para cá.
- `loopar`, `fadeEntradaS` e `fadeSaidaS` são **obrigatórios na trilha, sem
  default**: uma trilha de 20 s numa peça de 40 s é ou loop ou silêncio na
  metade, e isso não se decide por conveniência.

**Onde cada arquivo mora.** `pasta-publica.ts:33-38` declara hoje duas subpastas,
`SUB = {fonte, assets}`, e `projetos/01-private-label/public/fonte/` já contém
`pl.mp4` **e `pl.wav`** [medido aqui] — o wav extraído, que é exatamente a locução
daquela peça. Então:

- **locução → `SUB.fonte`.** Ela é material cru do projeto, e já está lá. Zero
  mudança de convenção.
- **trilha → `SUB.audio`, subpasta nova.** Separada de propósito: música
  licenciada tem procedência e licença que material gravado por nós não tem, e
  guardar as duas na mesma pasta perde essa distinção — que é justamente o que
  D9 precisa decidir. `public/audio/` não existe hoje [medido aqui].

**O que continua não existindo é de onde a faixa vem** — música licenciada, som
ambiente gravado, ou silêncio declarado. É **D9**, e ela bloqueia 5 séries por
elegibilidade, não por gosto.

### 3.7 Licenças: a decisão que o desenho se recusa a tomar sozinho

Dez técnicas que dão energia a reel viral colidem com `proibicoes.md`, e uma das
quatro fontes do plano de qualidade (a divergência **D5**, "modo hook") prescreve
exatamente elas. O desenho **não escolhe em silêncio**: vira um bloco de 12
chaves, todas ausentes por omissão, cada uma nomeando a linha que derruba.

**Correção: não são 12 booleanos.** A versão anterior escrevia
`licencas: Licencas; // 12 booleanos, todos false por omissão` e, três parágrafos
depois, exigia *"`justificativa` de ≥ 12 caracteres"* para ligar qualquer uma. Um
booleano não carrega texto: as duas metades da seção pediam coisas incompatíveis e
a justificativa não tinha onde morar. O tipo de §2.3 resolve:

```ts
type Licenca  = {ligada: true; justificativa: string};  // ≥ 12 caracteres
type Licencas = Record<ChaveDeLicenca, Licenca>;
licencas: Partial<Licencas>;   // chave AUSENTE = desligada
```

Três consequências, e a segurança da seção sobrevive inteira:

- **Uma justificativa por licença**, não uma por briefing. Ligar `particulas` e
  `flashNoCorte` com um motivo só é o que o campo existe para impedir.
- **`ligada: true` é literal**, não `boolean`. Não existe `{ligada: false}`: a
  forma de desligar é não escrever a chave. Assim o estado "desligada com
  justificativa escrita" — que seria uma pegadinha de leitura — não é
  representável.
- **O argumento de segurança fica mais forte, não mais fraco.** O que ele dizia
  era "todas `false` por omissão"; o que ele diz agora é "**ausente** por omissão,
  e ligar custa escrever por quê". `Object.keys(licencas).length === 0` continua
  sendo a leitura de "nenhuma ligada", em uma expressão.

| chave | linha de `proibicoes.md` | o que ela proíbe, textualmente |
|---|---|---|
| `particulas` | 11-12 | "explosão de partícula" |
| `orbesDeBrilho` | 11 | "brilho" |
| `varreduraDeLuz` | 11 | "brilho" |
| `shockwave` | 11-12 | partícula + brilho |
| `molaComOvershoot` | 11 | "easing elástico" (o `{damping: 11, stiffness: 130, mass: 0.7}` do modo hook) |
| `revelarCaractereACaractere` | 14 | "Revelar texto caractere a caractere" |
| `flashNoCorte` | 16 | "Flash branco instantâneo" |
| `irisWipe` | 16 | por vizinhança com "whip pan" |
| `motionBlurBurst` | 7-8 | nomeia `<CameraMotionBlur>` |
| `swipeMarcaTexto` | 20 | seria o 2º saturado ao lado de `COR.acento` |
| `highlightPalavraAtiva` | — | **não é proibição**: é 1 acento, mas troca 2,45×/s, o que é acento por palavra e não por cena |
| `aceitaTempoMorto` | 11-12 | "tempo morto" — **supressor de portão, não técnica.** Ver a regra 2 |

Duas regras que fazem isso ser decisão e não default:

1. **Ligar qualquer uma exige `justificativa` de ≥ 12 caracteres**, e quem reprova
   é o **refinador**, não o portão de ritmo (§3.9.1 fixa a fronteira; a versão
   anterior dava a regra a dois donos).
2. **Nenhuma técnica ligada por licença é implementada nesta versão** — o campo
   existe para a decisão ficar visível e versionada, e o código entra depois. **Mas
   duas das 12 chaves não são técnicas, e a regra 2 não se aplica a elas.** A
   versão anterior não fazia essa distinção, e sem ela a regra 2 era falsa ou o
   campo era o HTTP 200 que ignora o parâmetro:

   | chave | o que é | efeito nesta versão |
   |---|---|---|
   | `aceitaTempoMorto` | **supressor de portão.** Não desenha nada: desliga a checagem "cena sem evento **e** sem legenda" do portão `ritmo` | **tem efeito nesta versão**, porque o portão existe nesta versão. Ligada, o portão registra no diagnóstico *qual* cena foi liberada e por qual justificativa |
   | `highlightPalavraAtiva` | **exige código novo** na camada `Legenda` | **não tem efeito nesta versão.** Logo **D4 não é decidível agora**: a opção (b) da D4 depende de código que a regra 2 proíbe. A decisão fica, a implementação vai para o plano P4 |
   | as outras 10 | técnicas de desenho | nenhum efeito. Ligar registra a decisão e **o portão avisa** que a técnica não está implementada, para não parecer ligada |

   O aviso do portão é o que impede a armadilha: um campo que liga um efeito
   inexistente **em silêncio** seria a lição 3 outra vez.

O substituto legítimo para "um hit visual a cada 0,4–0,8 s" neste motor é **corte
e tipo** — palavra entrando, bloco de legenda virando, cartela cobrindo — e é
exatamente o que cena + manchete plural passam a permitir. Isto é o argumento de
que fechar A2 e A3 ataca o mesmo problema que o modo hook ataca, por um meio que
a marca aceita.

### 3.8 A skill — resolução de C8 e C9

**Skill nova, `canastra-briefing`, irmã de `canastra-video`**, e não uma extensão
dela. Dois donos de um fluxo é pior que um, do mesmo jeito que dois planos.

| skill | dona de | ganha | perde |
|---|---|---|---|
| `canastra-briefing` (nova) | a **entrada**: coleta, esquema, compilação, recusas, portão de ritmo, registro de lição | a seção *"Antes de escrever uma linha: o que coletar"*, migrada inteira | — |
| `canastra-video` (existe, 239 linhas) | a **saída**: render, portões, armadilhas de ffmpeg/rotação/`--props`, pasta pública, normalização de áudio, licença | uma linha na tabela *Rotear primeiro* | a seção de coleta — senão o texto existe em dois lugares e eles divergem |

A skill nova coleta **na ordem em que as respostas travam**, e para na primeira
que falta: **série do catálogo** (12 slugs; 7 das 12 estão bloqueadas, e série
bloqueada para aqui) → **fontes com caminho real e camada** → **tem locução?**
(troca metade do pipeline: a legenda nasce de Whisper ou o texto é escrito) →
**duração alvo, superfície e fps medido por `sondar()`** → **formatos** →
**gancho e CTA nas palavras dele** → **licenças, se alguma**.

**C9 — um escritor só para `props.json`.** `scripts/gerar-props.mjs` já escreve
`props.json`. Se o compilador também escrever, dois escritores disputam um
arquivo. O compilador **absorve** o estágio de legenda do script — que já chama
`agrupar()` e já tem a prova `provarTempoDaFonte()`, para reaproveitar e não
reescrever — e `gerar-props.mjs` é retirado no mesmo commit em que o compilador
nasce.

### 3.9 Portões

Os quatro existentes (`folha`, `telefone`, `determinismo`, `loop`) não mudam. A
spec acrescenta **um comando** e **liga um que já existe**:

| portão | veredito | o que pega |
|---|---|---|
| **preservação** — `src/verificacao/preservacao.ts`, hoje órfão | comando | pixel alterado dentro da embalagem. **Já existe, com 9 testes que passam, e `conferir.mjs:77` não o conhece** [medido aqui] |
| **ritmo** (novo, puro, roda antes do render) | comando | a lista está em §3.9.1, porque ela só faz sentido ao lado da fronteira com o refinador |

`DURACAO_MINIMA` **já existe exportada** em `src/motor/movimento.ts:122`, com
exatamente esta fórmula — `TEMPO.entrada + TEMPO.holdFinal + TEMPO.entrada` = 12 +
12 + 12 = **36 frames** = 1,2 s a 30 fps —, e `tests/textotela.test.ts:81` já
asserta a igualdade [medido aqui]. A versão anterior re-derivava o número como
aritmética nova, sem dizer que a constante existia, o que convidava uma segunda
definição do mesmo valor em outro arquivo. **O portão importa a constante; não a
recalcula.**

#### 3.9.1 Quem recusa o quê — a fronteira, e ela não existia

Quatro checagens tinham dois donos e uma tinha três, e a fronteira entre
`compilar.ts`, `refinar.ts` e o portão `ritmo` nunca estava escrita: a §2.4
chegava a apontar `refinar.ts` para a seção do portão. Duas implementações da
mesma regra divergem — é a lição 8 do `CLAUDE.md` aplicada a validação. **A
fronteira é uma pergunta só: de que o diagnóstico precisa?**

| dono | precisa de | pode recusar |
|---|---|---|
| **`esquema.ts`** (zod) | nada além do texto do briefing | **forma**: tipo, enum, faixa numérica, campo obrigatório, `transicoes.length === cenas.length - 1` |
| **`refinar.ts`** (puro) | só o briefing, em segundos | **sentido, sem aritmética de frame e sem disco** |
| **`compilar.ts`** (puro) | o briefing + `fps` | nada. **O compilador não recusa: ele converte.** Uma exceção, abaixo |
| **`ritmo`** (puro, lê disco) | o `plano.json` **e** o disco | o que só é visível em frames ou em arquivo |

**`refinar.ts` — as recusas de briefing.** Todas decidíveis lendo o briefing:

- `papel: 'legenda'` em evento (§3.4.1), com a mensagem apontando o campo `legenda`
- texto de `dado` casando com `/^F[:.]|VAL|LOTE/i` (§3.4.1, lição 22)
- licença ligada sem `justificativa` de ≥ 12 caracteres (§3.7)
- `registro: 'telaCheia'` com `enquadramento: {tipo:'faixa'}` (§3.3.2)
- `audio.locucao === null && audio.trilha === null` (§3.6)
- `legenda` presente sem âncora resolvível (§2.2.1)
- `'16:9'` em `formatos` — impossível pelo tipo, e o refinador dá a mensagem
- `duracao.modo === 'totalFixo'` sem `alvoS`

**`ritmo` — as recusas que precisam do plano ou do disco.** Nenhuma repetida acima:

- cena sem evento **e** sem legenda no intervalo dela — salvo `aceitaTempoMorto` (§3.7)
- cena mais curta que `duracaoDeIrmao` do seu evento mais longo (frames)
- duas camadas na mesma pista no mesmo frame (§3.4.2 — **frames**)
- dominância abaixo do `PISO_DE_DOMINANCIA` em qualquer formato pedido (§3.4.2)
- `razaoExibicao` declarada ≠ `sondar()` medida, tolerância 0,005 (§3.3.3 — **disco**)
- bloco de legenda grudado em 0 por mais de 10 frames (§2.2.1)
- arquivo declarado que não existe em `public/` (**disco**)
- asset de recorte sem laudo aprovado — ver abaixo
- licença ligada cuja técnica não está implementada: **aviso**, não recusa (§3.7)

**`duracaoPecaFrames ≠ alvo` sai da lista do portão.** A versão anterior a punha
nos dois lugares e afirmava, em §3.2.2, que o **compilador lança**. As duas coisas
não cabem: se o compilador lança, `plano.json` não é escrito, e o portão — que roda
sobre o plano — nunca vê o caso. A checagem era **morta**. Fica com o compilador,
que é o único lugar onde os dois números existem ao mesmo tempo, e é a única
exceção à regra "o compilador não recusa": ele lança porque continuar produziria um
artefato que mente sobre a duração pedida.

**O laudo de recorte: qual laudo, e onde ele mora.** Aqui havia um nó de nomes que
a versão anterior não desfez, e ele importa porque são **dois** laudos diferentes:

| laudo | onde | tem `aprovado`? |
|---|---|---|
| `src/verificacao/preservacao.ts`, tipo `Laudo` | TypeScript, pós-render | **não.** Os campos são `pixelsDiferentes`, `maiorDelta`, `total`, `considerados`, `pixelsAlfaPerdido` [medido aqui] |
| `instagram/recorte/verificar.py` | Python, na hora de recortar | **sim**: `aprovado = (alterados == 0) and (alfa_min_rotulo is None or alfa_min_rotulo == 255)` (`verificar.py:56`) |

O `laudo.aprovado` que o portão de ritmo precisa é o **segundo**, e ele vive em
`instagram/assets/embalagem/<slug>.json`, na chave `dados["laudo"]["aprovado"]`.
Conferi os três: `canela-250g`, `classico-250g` e `suave-250g` estão todos
`aprovado: true` [medido aqui].

**Mas o portão não lê aquele arquivo, e a razão é que ele já tem dono.**
`instagram/recorte/publicar.py:82` só copia para
`projetos/<p>/public/assets/` o PNG cujo laudo irmão traz `aprovado is True` — é
fail-closed, e é por isso que os três PNG que estão lá **não têm `.json` ao lado**
[medido aqui]. Um portão que fosse reler o laudo seria o terceiro leitor do mesmo
fato, e cada leitor novo é uma chance nova de divergir. Então:

> O portão de ritmo checa que **todo `asset.arquivo` do briefing existe em
> `projetos/<p>/public/assets/`**. Existir ali já é o certificado, porque a única
> porta de entrada daquela pasta é `publicar.py`, que é fail-closed. `laudoExigido:
> true` no tipo é o que torna a exigência legível no briefing; a prova é a
> presença do arquivo.

E continua valendo, agora com mecanismo: **o laudo não é copiado para dentro do
briefing.** Copiar `aprovado: true` para lá criaria a segunda fonte de verdade, e
pior: um humano podendo digitar `aprovado: true` à mão transformaria o portão
fail-closed de `publicar.py` em decoração.

**Dois nomes para acrescentar em `conferir.mjs:77`.** Ele hoje lista
`['todos','folha','telefone','determinismo','loop']` [medido aqui] — sem
`preservacao` e sem `ritmo`. Os dois entram na mesma linha, e `todos` passa a
significar seis.

---

## 4. Decisões abertas

Numeradas, cada uma com as opções e o que muda. **Nenhuma tem default escondido
no código.**

**D1 — as 12 licenças: quantas, e quais.**
Opções: (a) nenhuma, `proibicoes.md` intacto; (b) um subconjunto com
justificativa escrita; (c) modo hook inteiro.
Muda: (a) a energia da peça vem só de corte e tipo, e o teto de retenção é o que
corte e tipo dão; (b) cada uma ligada custa implementação depois, e a
justificativa fica versionada no briefing, auditável; (c) `proibicoes.md` precisa
ser reescrito — e ele é o que separa o motor do "look de IA" que o projeto inteiro
existe para evitar. **Não decida por peça: decida por série**, senão a coesão da
série vira acidente.

**D2 — no 1:1 e no 4:5, a manchete continua coluna?** (bloqueia a manchete em
coluna, não o formato)
Medido: `sobreImagem` sai **54 px no 1:1** e **26 px no 4:5**, contra 78 px da
legenda — e, no que de fato decide, a **mancha**: 4,800% e 0,890% do quadro contra
pisos de 6,925% e 7,490%, isto é **0,866×** e **0,149×** a dominância da legenda,
num piso de 1,25× [medido aqui, §3.4.2]. Então o portão `sem-dominante` reprova
`pista: 'topo'` e `pista: 'principal'` nesses dois formatos. **O que isto não
bloqueia é o formato**: com `pista: 'tela'` (cartela) os dois passam por mais de
4×, e é por isso que o briefing de §7.1 entrega 9:16 **e** 1:1.
Opções: (a) manter coluna e aceitar que a manchete é o menor texto do quadro; (b)
no 1:1/4:5 a manchete deixa de ser coluna e passa a **faixa sobre o vídeo** — muda
composição, não constante; (c) cartela obrigatória nesses formatos (125 e 152 px,
mas cobre o vídeo).
Precisa de um still lado a lado antes, como o plano de qualidade já pedia. Com
manchete plural, (a) piora: hoje é 1 texto em 23,2 s, e vão ser vários.

**D3 — `duracao.modo` tem default?**
Opções: (a) obrigatório sempre (o desenho propõe isto); (b) default `somaCenas`.
Muda: (b) é conveniente e faz quem pedir "24 s" receber 22,4 s sem perceber, na
primeira peça que usar crossfade.

**D4 — highlight da palavra ativa na legenda.**
Tecnicamente é **um** acento com função, o que `proibicoes.md:20` permite — mas
troca de palavra **2,45 vezes por segundo**, que é um acento por palavra.
Opções: (a) fora; (b) dentro, e `proibicoes.md:20` passa a dizer "um acento por
cena, exceto a pista de legenda".

**D5 — default de enquadramento de foto, por série.**
`faixa`: 42,2% da altura é foto. `recorte`: joga fora 57,8% da foto.
Muda: a série 1 (foto parada + locução) é a primeira da fila de
`05-formatos.md` §8, então este default decide a aparência da primeira peça que
sair do motor novo.

**D6 — corpo de legenda que encolhe para caber** (V11, herdada do plano).
Medido lá: encolher por bloco resolve os estouros mas faz o corpo variar 78→68 px
no Reel e 78→51,5 px no Feed, o que lê como acidente de render. Continua aberta.

**D7 — como as composições passam a ser registradas.**
Hoje `Raiz.tsx` registra `Reel` e `Feed` com `FPS = 30` e `DURACAO_FRAMES = 696`
em tempo de módulo.
Opções: (a) `calculateMetadata` lendo o plano; (b) uma composição por formato com
`durationInFrames` vindo do plano por props e `fps` fixo por composição; (c)
registro gerado a partir do briefing.
Muda: (a) é o caminho do Remotion e mata a Tarefa 6 do plano (o portão de fps);
(b) mantém `Raiz.tsx` legível e obriga um registro novo por fps; (c) gera código,
que este repositório não faz em nenhum outro lugar.

**D8 — instalar `@remotion/transitions@4.0.530`?**
Opções: (a) instalar; (b) `Series` + `offset` negativo com crossfade à mão.
Muda: (a) uma dependência nova, e cinco invariantes passam a falhar alto; (b) zero
dependência, e os cinco invariantes passam a ser vídeo torto com exit 0.

**D9 — de onde vem a faixa de áudio das peças sem locução.** (bloqueia 5 séries)
Opções: (a) música licenciada — e então qual licença, porque a peça é comercial;
(b) som ambiente gravado na fazenda, que **não existe no acervo hoje**; (c)
publicar sem faixa e perder elegibilidade para não-seguidor **[oficial]**.

**D10 — quem escreve o `briefing.json`.**
Opções: (a) a skill entrevista e escreve, o Rafael revisa; (b) o Rafael escreve à
mão a partir de um exemplo comentado; (c) os dois, e a skill valida o que
chegar.
Muda: (a) é o que o pedido descreve ("eu jogue as informações"); (b) exige que o
esquema seja legível sem ferramenta.

**D11 — folga vertical no `sobreImagem`** (V13, herdada). Depende de D2: pôr
`linhasDeFolga = 1` no `sobreImagem` derruba o corpo, e o corpo já é o problema.

**D12 — o motor dirige saída estática e carrossel, ou só vídeo?** (nova; o cético
achou a lacuna e ela é a maior)
Medido em `05-formatos.md` §4, coluna *Formato*: **7 das 12 séries têm entrega
não-vídeo** — 2 (`estático 1:1 + reel de 8 s`), 3 (`carrossel`), 5 (`reel ou
carrossel`), 6 (`estático`), 7 (`estático`), 10 (`reel ou carrossel`), 11 (`reel +
estático`) [aritmética]. E das **3 séries prontas hoje, com arquivo no disco — 1,
3 e 6** —, a 3 é carrossel e a 6 é estático; `05-formatos.md` §8 põe a série 6, um
estático, como **terceira peça da fila**. Do jeito que o esquema está, um post
estático seria obrigado a declarar `duracao.modo` e a carregar faixa de áudio.
Opções: (a) fora desta versão, e **declarado em §5** — o motor dirige vídeo e a
metade estática do catálogo continua fora dele; (b) `saida: 'video' | 'estatico' |
'carrossel'` no briefing, com `duracao` e `audio` condicionados ao valor, o que é
uma união discriminada no topo do esquema e muda a forma de tudo; (c) um segundo
esquema, `canastra-estatico/1`, compartilhando `layout()`, tokens e portões, sem
compartilhar relógio.
Muda: (a) é honesto e mantém esta spec do tamanho que ela consegue provar, mas
"puta motor" fica querendo dizer metade do catálogo; (b) é a menor duplicação e o
maior risco de o vídeo carregar peso que só o estático precisa; (c) é a menor
mudança nesta spec e a maior chance de os dois divergirem — lição 8 outra vez.
**Enquanto D12 não fechar, §5 declara estático e carrossel fora**, porque a
alternativa era o silêncio que o cético achou.

---

## 5. O que fica de fora desta versão

YAGNI vale, e "existe na biblioteca" não é razão para entrar.

| fora | por quê |
|---|---|
| **3D, Lottie, `@remotion/paths`, `@remotion/canvas`** | nenhuma série do catálogo pede. `@remotion/canvas` e `@remotion/paths` estão em `node_modules` [medido aqui] e não viram peça por estarem lá |
| **Partícula, orbe, varredura, shockwave, motion blur burst, flash, iris wipe, mola com overshoot, revelação caractere a caractere, swipe de marca-texto** | `proibicoes.md` 7-8, 11-12, 14, 16, 20. Entram como **licença desligada** (§3.7), não como código |
| **`ponto {x, y}` / seta e rótulo ancorados em coordenada da imagem** (série 2) | resolução de **C7**. Um dos desenhos o pôs no schema com o resolvedor falhando alto, contrariando o princípio que ele mesmo escreveu: campo que o motor não resolve é o HTTP 200 que ignora o parâmetro (lição 3). E a série 2 canônica está **bloqueada por captura** (cereja madura e bóia, Blocos D e E). **O mesmo princípio foi aplicado ao `encaixe`**, que a versão anterior deixava no briefing e o motor não podia honrar no 9:16 (§3.4.2): o princípio valia num campo e era violado no outro |
| **Coordenada de recorte em píxel** | `enquadramento: {tipo:'recorte'}` é **fração de 0 a 1 do arquivo JÁ ORIENTADO**, e a versão anterior não declarava unidade nenhuma. Píxel do arquivo codificado é exatamente a armadilha de §3.3.3: num packshot `Orientation 6`, `x: 0.289` em fração continua valendo depois de orientar, e `x: 1184` em píxel passa a apontar para outro lugar do assunto. Fração também sobrevive a um recorte de resolução diferente do mesmo enquadramento |
| **Retime / câmera lenta** (série 8) | a série está bloqueada pelo Bloco A2. O campo entra quando o clipe existir |
| **Contador a partir de número informado** (série 11) | bloqueada por um dado que só a operação tem |
| **Grade recursiva** | a série 4 pede 2 ou 4 células de fonte simples. Recursão em zod obriga anotação de tipo manual = segunda fonte de verdade |
| **`iris`, `clockWipe`, `flip` como apresentação de transição** | vizinhança de whip pan e flash, `proibicoes.md:16` |
| **`createTikTokStyleCaptions` e `ensureMaxCharactersPerLine`** de `@remotion/captions` (instalado, zero usos) | paginam pela **pausa da fala** (`combineTokensWithinMilliseconds: 800`); `agrupar()` corta em 2 palavras fixas, que é o token medido. Trocar é refazer a medição de 2,45 blocos/s e 1,7 palavras/bloco |
| **`fitText` de `@remotion/layout-utils`** | mede no DOM e o pacote não está instalado. A busca binária pura é o que torna o corpo provável em Node |
| **16:9 como formato de entrega** | **sai do enum `Formato`** (§3.1): nenhuma composição o registra, e mantê-lo aceitável era campo que nada resolve. Continua como **rótulo geométrico** em `Zonas['formato']`, porque `layout()` de fato o calcula — e a margem de base dele é **51,03% da altura**, com o vídeo virando coluna de 607,5 px e 1.312,50 px de sobra [medido aqui] |
| **Saída estática e saída de carrossel** | **exclusão declarada, e ela dói.** `grep -c` na versão anterior desta spec dava `carrossel` = 0 e `estático` = 0: não estavam nem como capacidade nem como exclusão, e é a lacuna que mais separa esta spec de "um puta motor". **7 das 12 séries têm entrega não-vídeo** e 2 das 3 prontas hoje são delas [aritmética sobre `05-formatos.md` §4]. Fica fora **desta versão** porque `duracao`, `transicoes` e `audio` são todos obrigatórios e nenhum faz sentido num JPG — e resolver isso é mudar a forma do esquema no topo, não acrescentar um campo. É **D12**, e é a decisão aberta de maior alcance da spec |
| **Implementar qualquer técnica ligada por licença** | o campo registra a decisão; o código vem depois dela. **Menos `aceitaTempoMorto`**, que é supressor de portão e tem efeito nesta versão (§3.7) |

---

## 6. Relação com o plano de qualidade de 99 KB

O plano continua valendo. Ele não é concorrente: **quatro das sete tarefas dele
são pré-requisito mecânico** de cena, porque cena multiplica exatamente os
defeitos que elas fecham.

| tarefa | estado | por quê |
|---|---|---|
| **1** — ponta de entrada/saída na legenda + contorno `corpo/7` | **continua valendo, em separado** | a legenda fica fora da `TransitionSeries` (§3.2.4), então o escopo dela não muda |
| **2** — saída chega a zero no último frame desenhado | **pré-requisito** | com N cenas o resíduo de 18,85% **[relatado]** aparece N vezes, e na janela de crossfade ele fica *sobre* a cena seguinte |
| **3** — margem em fração do eixo próprio, topo em 5% | **pré-requisito** | `layout()` passa a ser chamada uma vez por cena, com caixas diferentes; um `k` só da largura erra em cada uma. Reconferi a **zona**: topo 4,69%, base 16,15 / 28,70 / 22,96 / 51,03% [medido aqui]. **E agora ela cobre também a largura da caixa da legenda** (§3.4.2) |
| **4** — push como propriedade `scale`, sem mover o canto do bloco | **pré-requisito** | é o mesmo motor de push que a câmera sobre foto parada usa (§3.3); consertar depois é consertar em dois lugares |
| **5** — `premountFor={fps}` + schema zod | **absorvida e expandida** | zod passa a validar o **briefing**, não só as props; `premountFor` passa a valer em `TransitionSeries.Sequence`, que é onde a fonte da cena seguinte tem de estar bufferizada antes do crossfade |
| **6** — portão de fps, piso da legenda em segundos | **pré-requisito, e depois superada** | o portão é a alternativa honesta enquanto `fps` não é campo. Quando §3.1 entrar, `exigirFpsDeReferencia` tem que ser **deletada no mesmo commit** e o teste "recusa qualquer outro fps" invertido. Se as duas coisas coexistirem, o portão mata renders legítimos |
| **7** — invariante de duas linhas na legenda | **absorvida e promovida** | deixa de ser só invariante e passa a ser a **altura da pista `rodape`** |

**Ordem obrigatória de execução**, porque os dois documentos se cruzam num ponto:
**Tarefa 2 → Tarefa 3 → gerar o ouro geométrico → o resto desta spec.** O ouro
geométrico tem de nascer **depois** da Tarefa 3; antes, ele grava as margens
erradas e a migração de fps parece quebrar o layout.

**O que esta spec contradiz no plano, com motivo:**

1. **§3.1 arquiva transições como YAGNI** — *"Não há hoje mais de uma cena por
   peça, então é YAGNI."* É a linha que o pedido do Rafael **revoga**. O resto
   daquela entrada (cabe na marca desde que a apresentação seja `fade` ou `wipe`;
   `iris`, `clockWipe` e `flip` não) é **mantido e transformado em tipo** (§3.2.3).
2. **§3.1 lista V5 (piso de corpo da manchete no 1:1) e V13 como "decisão do
   Rafael, depois de um still", adiáveis.** Com manchete plural, V5 deixa de ser
   adiável e vira **bloqueante da manchete em coluna no 1:1 e no 4:5** — é a D2.
   (Não do formato: medido, `pista: 'tela'` passa o piso nos dois. Ver §4 D2.)
3. **`manchete` singular** é o tipo que a §5 do plano protege com
   "opcional sem placeholder". A propriedade sobrevive: `eventos` **lista vazia**
   é peça completa sem evento, sem erro e sem placeholder.

   **Correção: a frase seguinte, na versão anterior, afirmava uma compatibilidade
   sem mecanismo.** Estava escrito que *"`manchete` continua aceito e é
   normalizado para um evento de papel `manchete`, então o `props.json` de
   `01-private-label` não precisa ser reescrito para o motor novo rodar"*. Não é
   verdade, e o arquivo diz por quê. Li `projetos/01-private-label/props.json`
   [medido aqui]: as chaves são `_frames`, `_origem`, `_manchete`, `arquivo`,
   `razaoFonte`, `cortarAntesFrames`, `manchete` (com `inicioFrame: 104`) e
   `blocos` (38 itens com `inicioFrame`/`fimFrame`). **Tudo em frames, no relógio
   da fonte, e não existe `cenas`.** §2.2 decreta que nenhum campo do briefing está
   em frames e que a posição da cena vem da ordem do array. Aquele arquivo,
   portanto, **não é um briefing** — no máximo seria um `plano.json`, e entraria
   sem `_gerado_por` e sem o sha256, que é justamente a marca com que §2.1 detecta
   plano editado à mão.

   **O que vale no lugar:** `props.json` é **migrado uma vez, por script de mão
   única**, para `briefing.json`, no mesmo commit em que `gerar-props.mjs` sai
   (C9). A conversão é aritmética e já está inteira no protótipo
   `out/_spec-briefing/a-private-label.json`, que reconstrói aquela peça sem
   inventar número. E ela é de mão única **porque o segundo é o medido**:
   `aparaAntesS = 1,14 s` é o ar morto medido, e `Raiz.tsx:25` deriva
   `cortarAntesFrames = Math.round(1.14 * 30) = 34` — voltar de 34 para segundos
   daria 1,1333, não 1,14, e a migração tem de ler o valor medido, não desfazer o
   arredondamento. O resto fecha: `entradaS 2.32` = 3,46 − 1,14, e
   `round(2,32 × 30) = 70 = 104 − 34`. Depois da
   migração, **nada lê `props.json`** — nem união no schema da composição, nem
   normalização em tempo de execução. Um caminho de compatibilidade que ninguém
   exercita é código que apodrece; um script de migração que roda uma vez, não.
4. **"O `props.json` guarda um relógio só"**, da §5 do plano, sobrevive
   deslocada: o **briefing** guarda um relógio só, e `plano.json` — que tem os
   três — é gerado e carrega o hash do briefing, para que um plano editado à mão
   seja detectável.

5. **Duas correções de citação no plano, que esta spec precisa registrar porque
   declara respeitá-lo item por item.**
   (a) **As linhas de `proibicoes.md` no plano estão deslocadas em um.** Contei o
   arquivo [medido aqui]: **linha 19 = "Um elemento dominante por cena"**, **linha
   20 = "Um acento de cor por cena, com função"**. O plano, §3.2, cita `:19` como
   *"Um acento de cor por cena"* e fala do *"que proibicoes.md:19 permite"* no item
   do highlight — nos dois casos ele quer a linha 20. Esta spec usa 19 para
   dominância e 20 para acento, e está certa; sem este parágrafo, "respeitado item
   por item" seria uma afirmação que esconde uma divergência.
   (b) **Os dois números de margem de topo do plano estão os dois certos, e são
   grandezas diferentes.** O título da V4 diz 4,33% e o corpo dela diz 4,69%: 90,0
   px em 1.920 = **4,69%** é a **zona** que `layout()` devolve; **4,33%** é o
   **bloco de texto** em `sobreImagem`, que o push escala por 1,0394 em torno do
   centro e desce o topo para 83,2 px (`plano`, V4). A versão anterior desta spec
   escrevia "Reconferi: topo 4,69%" sem dizer de qual das duas falava, deixando
   dois números vivos para a próxima sessão. **Medi a zona: 90/1920 = 4,6875%.** O
   piso de 5% da Tarefa 3 é sobre a zona; a V13/D11 é sobre o bloco.

**A §5 do plano ("o que NÃO mudar") é respeitada item por item, com uma exceção
nomeada.** Nada aqui troca `bezierDeCss`, `POUSO`, `fases()`, `duracaoDeIrmao`, o
`push` linear, a busca binária de corpo, a guarda de tipografia, os `.ttf` locais,
`intersecao`, `alinhaHorizontal: 'flex-start'`, `linhasDeFolga = 1` na cartela, o
fundo terra, a sombra escalada pelo corpo, `SUB.fonte` na camada `Fonte`,
`tests/manchete-props.test.ts`, a ordem de árvore, ou a composição única servindo
todos os formatos.

**A exceção:** §3.4.2 muda a **largura da caixa da legenda** em
`layout.ts:68-73`. A §5 do plano não a lista como intocável, mas a mudança é real e
tem custo medido — a largura útil cai 25,0% no 1:1, 19,8% no 4:5 e 46,5% no 16:9 —,
então ela entra no plano com D6/V11 do lado, não sozinha.

**Uma coisa que o plano não tem e esta spec acrescenta ao inventário de dívida:**
a ausência A4 (**locução e** trilha de áudio), o portão de preservação órfão, e o
padrão de metadado de rotação ignorado (§3.3.3), que já tem três casos. Nenhum dos
três aparece nas 13 violações do plano, e os três estão confirmados por medição
nesta sessão.

---

## 7. A revisão de 30/09/2026

Esta seção é nova. Ela existe porque o cético adversarial reprovou a spec com 20
achados e a maior parte deles era real e cirúrgica: o defeito não era o desenho,
era o contrato ter buracos que impediam escrever um plano. Três coisas moram aqui:
o briefing concreto que faltava, a quebra em planos, e o registro item por item.

### 7.1 Um briefing válido, inteiro

A spec não trazia **nenhum** briefing concreto. O único que existia era o protótipo
em `out/_spec-briefing/`, pasta gitignorada que a própria spec chama de *"evidência,
não destino"* — e ele está escrito no vocabulário que a spec **rejeitou**
(`zona: {tipo:'nomeada'}`, `preset`, `modo: 'cartela'`, `audio.alvoLufs`,
`elementoDominante`, `versao`/`id`/`titulo`/`duracaoS` no topo). Quem fosse
implementar não tinha briefing válido para copiar, e quem lesse o protótipo
implementaria o esquema errado.

Abaixo, a peça `01-private-label` como briefing do esquema corrigido. **Nenhum
número novo**: tudo vem de `props.json`, de `transcricao.json` ou de `Raiz.tsx`, e
os dois campos de texto livre são **citação literal da fala**, com os índices de
palavra ao lado.

**Válido em que sentido:** ele passa o esquema (`esquema.ts`) e o refinador
(`refinar.ts`) e compila. O **portão de ritmo o reprova**, por um defeito de dado
na transcrição, e a última parte desta subseção mede esse veredito em vez de
escondê-lo.

```jsonc
{
  "_esquema": "canastra-briefing/1",
  "serie": "avulsa",
  "fps": 30,

  // Os dois formatos que o motor registra hoje: Raiz.tsx:59 Reel 1080x1920 e
  // Raiz.tsx:68 Feed 1080x1080. Com `pista: "tela"` (cartela) o piso de
  // dominância passa nos dois -- a mancha é 4,417x e 7,780x a dominância da
  // legenda, contra um piso de 1,25x (§3.4.2). O 4:5 fica fora porque nenhuma
  // composição registra 1080x1350 e `layout()` ainda devolve o rótulo `outro`
  // para ele (§3.1).
  "formatos": ["9:16", "1:1"],

  "duracao": {"modo": "somaCenas", "alvoS": 23.19},

  "cenas": [
    {
      // 696 frames / 30 = 23,19 s. Raiz.tsx:28: round((24,33 - 1,14) * 30).
      "duracaoS": 23.19,
      "fonte": {
        "tipo": "video",
        "arquivo": "pl.mp4",
        // EXIBIÇÃO, não contêiner: grava 1024x576, displaymatrix -90, exibe
        // 576x1024. O portão confere contra sondar() (§3.3.3).
        "razaoExibicao": 0.5625,
        "aparaAntesS": 1.14,
        "enquadramento": "faixa",
        "camera": "parado"
      },
      "eventos": [
        {
          "papel": "manchete",
          // CITAÇÃO LITERAL, palavras 11..15 de transcricao.json ("sua",
          // "própria", "marca", "de", "café"), só com caixa alta.
          // tests/manchete-props.test.ts prova.
          "texto": "SUA PRÓPRIA MARCA DE CAFÉ",
          // 3,46 (inicioMs da palavra 11) - 1,14 (apara) = 2,32.
          // round(2,32 * 30) = 70 = props.json 104 - 34. Fecha.
          "entradaS": 2.32,
          // `tela`, não `principal`: props.json declara `"modo": "cartela"`, e
          // `tela` é o ÚNICO caminho para a cartela depois que `encaixe` passou a
          // ser derivado (§3.4.2). Declarar `principal` aqui trocaria a composição
          // da peça em silêncio -- e a versão anterior deste exemplo fazia isso ao
          // mesmo tempo que prometia "nenhum número novo".
          "pista": "tela",
          "palavraAcento": 2
        }
      ]
    }
  ],

  // cenas.length - 1 = 0. Lista vazia, não ausente.
  "transicoes": [],

  "legenda": {
    "arquivo": "transcricao.json",
    "relogio": "fonte",
    "ancora": {"tipo": "locucao"},
    "maxPalavrasPorBloco": 2
  },

  "audio": {
    // public/fonte/pl.wav já existe no disco.
    "locucao": {"arquivo": "pl.wav", "ganhoDb": 0, "aparaAntesS": 1.14},
    // null é aceito porque HÁ locução (§3.6). Trilha por baixo da voz depende
    // de D9: nenhum arquivo de música existe no repositório.
    "trilha": null
  },

  "assets": [],
  "licencas": {},

  // Os dois campos de texto livre, e os dois são CITAÇÃO da própria fala:
  "gancho": "Você está procurando algo para lucrar muito?",
  "cta": "clique aqui, clique em baixo e vem conosco"
}
```

**Por que `gancho` e `cta` são citação e não redação minha.** São as palavras 0..6
e as últimas 8 de `transcricao.json`, lidas no arquivo [medido aqui]. A spec pede
*"gancho e CTA nas palavras dele"* (§3.8): num briefing reconstruído de uma peça
que já existe, "as palavras dele" são as que ele **falou**, e escrever outras seria
inventar. Num briefing novo, os dois campos são os únicos que a skill não pode
preencher sozinha.

Conferências que rodei sobre este arquivo [medido aqui]: a transcrição tem **75
palavras**; os índices 11..15 são `sua · própria · marca · de · café` e o
`inicioMs` da 11 é **3460**; a última palavra fecha em **23.940 ms**, ou seja
23,94 − 1,14 = 22,80 s na peça, dentro dos 23,19 s — **nenhum bloco de legenda é
descartado** pela regra 4 de §2.2.1.

#### O portão de ritmo REPROVA este briefing, e a reprovação é verdadeira

A versão anterior desta subseção dedicava um parágrafo a provar que nenhum bloco
cai pela regra 4 e **não dizia uma palavra sobre a regra 3**, que é a que morde
aqui. Um exemplo que a própria spec reprova em silêncio é pior que nenhum exemplo.
A conta, inteira, com a fórmula de §2.2.1 [medido aqui]:

```
desloc = emFrames(0, 30) − emFrames(1,14, 30) = 0 − 34 = −34 frames
```

| bloco (tempo da fonte) | na peça | o que acontece |
|---|---|---|
| `"Você está"` 0..20 | −34..−14 | **descartado**: nenhum frame visível |
| `"procurando algo"` 20..49 | −14..15 | **grudado em 0**, recuo de **14 frames** |
| os outros 36 | — | entram inteiros; o último fecha em 684 < 696 |

38 blocos no total (75 palavras a 2 por bloco), 1 descartado, 37 na peça [medido
aqui] — o mesmo `legenda .............. 37 blocos` que o plano espera do CLI.

`descartadosAntesDoInicio: 1` · `grudadosEmZero: 1` · `maiorRecuoFrames: 14` ·
`descartadosDepoisDoFim: 0`. O piso é `LEGENDA.duracaoMinFrames` = **10 frames**,
e 14 > 10, então o portão devolve `REPROVADO` com a falha `legenda-recuada`.

**E a reprovação está certa.** Medi a entrada de fala em `pl.wav` com
`silencedetect=noise=-40dB:d=0.1`: `silence_end: 1.135` [medido aqui] — a fala
começa em **1,135 s**, e o Whisper pôs as duas primeiras palavras (`"Você"`
0–340 ms, `"está"` 340–680 ms) **dentro do silêncio**. A apara de 1,14 s está
correta como corte de ar morto; o que está errado é a transcrição. Consequência
que o motor de hoje já paga em silêncio: `Legenda.tsx:35` procura o bloco em
`frame + 34`, logo no frame 0 da peça ele já está em 34 e cai no segundo bloco —
**`"Você está"` nunca apareceu nesta peça, e ninguém sabia**.

Então o exemplo fica como está, **reprovando**, e isso é deliberado por três
razões: é o único caso real em que o portão `ritmo` dispara, o que o torna a prova
de que o portão funciona; mexer no `briefing.json` para o portão passar seria
consertar o termômetro; e a resolução é de **dado**, não de desenho —
re-transcrever, ou corrigir à mão o início das duas primeiras palavras com o
1,135 s medido. Isso é decisão do Rafael, e o plano registra o veredito em vez de
contorná-lo (Tarefa 10, Step 6: *"Não conserte o `briefing.json` para o portão
passar"*).

**Três coisas que este exemplo prova sem discurso:** que o esquema corrigido cabe
numa peça real sem campo sobrando nem faltando; que o portão morde, e morde na
peça que o repositório já tem; e que `pista` não é enfeite — trocar `tela` por
`principal` levaria a mancha da manchete no 1:1 de 7,780× a dominância da legenda
para 0,866×, abaixo do piso de 1,25×, e o portão reprovaria por `sem-dominante`
(§3.4.2).

**E uma que ele expõe.** O protótipo `b-jornada-foto.json` declara
`razaoExibicao: 1.3333` para `IMG_1421.JPG` e `IMG_1424.JPG`, e os dois são
`Orientation 6`, logo **0,75** [medido aqui]. Duas das três fotos daquele briefing
estão erradas. Não corrijo o protótipo aqui — ele é evidência de uma sessão
anterior, e mexer nele apaga o registro de que o esquema sem conferência **deixa
isso passar**. É por isso que a conferência de `razaoExibicao` está no portão
(§3.9.1) e não na boa vontade de quem escreve.

### 7.2 A quebra em planos

O cético fechou dizendo que isto não cabe num plano só, e ele está certo: §3.1 já
depende de **D7** para saber a forma do `Raiz.tsx`, §3.2.1 depende de **D8** para
saber qual código escrever, a manchete em **coluna** no 1:1/4:5 depende de **D2** e
cinco séries dependem de **D9**. Um plano escrito antes dessas quatro seria
reescrito no meio.

**Sete planos, na ordem da dependência.** Cada linha é um plano; a coluna *precisa
de* é o que tem de estar fechado antes de começar a escrevê-lo.

| # | plano | precisa de | testável sem render? |
|---|---|---|:---:|
| **P0** | Tarefas **2** e **3** do plano de qualidade + a linha da largura da legenda (§3.4.2) + **gerar o ouro geométrico depois delas** | nada | parcial |
| **P1** | Briefing puro: `esquema.ts`, `refinar.ts`, `compilar.ts`, `emFrames`, portão `ritmo`, ligar `preservacao` em `conferir.mjs:77`, migrar `props.json` e aposentar `gerar-props.mjs` (C9) | P0, **D12** | **sim, inteiro** |
| **P2** | `Fonte` polimórfica (foto e cor) + **`sondar()` com EXIF** (§3.3.3) + Tarefa 4 do plano | P1, **D5 reformulada** | quase |
| **P3** | Cena e `TransitionSeries`, com `premountFor` na `Sequence` (Tarefa 5) | P2, **D8**, **D7** | não |
| **P4** | Evento plural + pista/encaixe + piso de dominância + `highlightPalavraAtiva` se D4 disser (b) | P3, **D2**, **D4** | parcial |
| **P5** | `Locucao` e `Trilha` (A4), e a subpasta `SUB.audio` | P1, **D9** | não |
| **P6** | A skill `canastra-briefing`, e a amputação da seção de coleta de `canastra-video` (C8) | P1 | n/a |

Três observações que a ordem esconde:

1. **P1 é o plano que dá mais por menos.** Ele é Node puro, zero pixel, e não
   depende de D2, D4, D7, D8 nem D9. Sai inteiro sob TDD e fecha a metade do
   contrato que hoje está furada.
2. **P0 tem de gerar o ouro geométrico por último.** O ouro nascido antes da
   Tarefa 3 grava as margens erradas, e depois a migração de fps *parece* quebrar o
   layout. Isto já estava em §6 e continua sendo a única ordem obrigatória interna.
3. **D12 é pré-requisito de P1, não um plano a mais.** Se estático e carrossel
   entrarem (opção b ou c), o resultado não é uma fila mais longa: é uma união
   discriminada no topo do esquema, ou seja **P1 reescrito**. Decidir depois de P1
   é refazer P1.

### 7.3 Os 20 achados, item por item

Dezoito corrigidos, dois recusados com medição. As gravidades são as do cético.

| # | grav. | achado, em uma linha | o que fiz |
|---|---|---|---|
| 1 | ALTA | `sondar()` não mede razão de foto: só `displaymatrix`, nunca EXIF | **Corrigido**, §3.3.3. Reproduzi o defeito (1,7778 num `Orientation 6`), medi que o **mesmo ffprobe** já expõe `Orientation` em `-show_frames`, e estendi `sondar()` em vez de criar outro mecanismo. Registrei como **padrão de três casos**, não acidente, e pus a conferência no portão |
| 2 | ALTA | não existe campo de locução em parte alguma | **Corrigido**, §2.3 e §3.6. Tipos `Faixa`/`Locucao`/`Trilha`/`Audio`; obrigatoriedade escrita sobre campos que existem; relação com −14 LUFS explicada (o normalizador pós-render manda, e por isso não há LUFS no briefing) |
| 3 | ALTA | o rebase da legenda não tem fórmula com N cenas | **Corrigido**, §2.2.1. Fórmula escrita, `LegendaDeclarada` com `ancora` de três casos, e as quatro consequências — inclusive o bloco grudado em 0, que é o caso vivido do Whisper |
| 4 | ALTA | pista/encaixe sem geometria, sem mapeamento para `Modo`, sem piso de dominância | **Corrigido**, §3.4.2, e **re-corrigido em 01/10/2026** — a primeira correção pôs número em caixa que o motor não tem. Agora `topo` e `principal` são as frações 0,24/0,52 da coluna, a faixa 0,76–1,00 é só folga, `rodape` **é** `zonas.legenda` e `tela` **é** `zonas.seguro`; a invariante está separada em *por construção* (topo × principal) e *por medição, dependente do conserto de `layout.ts:69-71`* (rodape × evento). Mais `LIMIAR_DE_COLUNA` 0,22, derivação `encaixe(pista, formato)` 3→2 em cima do `Modo` que existe, `encaixe` **sai do briefing**, e `PISO_DE_DOMINANCIA = 1,25 ×` a legenda **em duas linhas cheias**, na lista do portão |
| 5 | ALTA | "`npm ci` derruba o zod" é falso | **Corrigido**, §1.4. Reli o lock, confirmei que `zod` é dependência não-dev de `@remotion/media`, escrevi o risco **real** (soltura futura, versão sem revisão, isolamento estrito) e a ação que continua certa |
| 6 | MÉDIA | 353,20 px rotulado como interseção | **Corrigido**, §3.4.2, e **fui além**: medi os dois eixos, achei que no 9:16 a interseção é **zero**, reproduzi os 90,2 px que estavam como [relatado], e achei a **causa** — um `min` inconsistente em `layout.ts:68-73` — com o conserto de uma linha e o custo medido. **E recusei metade do achado**: ver abaixo |
| 7 | MÉDIA | booleano não carrega justificativa | **Corrigido**, §3.7. `{ligada: true; justificativa}`, `ligada` literal, ausência = desligada |
| 8 | MÉDIA | `aceitaTempoMorto` × "nada implementado nesta versão" | **Corrigido**, §3.7, por uma terceira saída: ver abaixo. Tabela de três classes, e **D4 fica indecidível nesta versão**, dito explicitamente |
| 9 | MÉDIA | quatro checagens com dois donos; `duracaoPecaFrames ≠ alvo` morta no portão | **Corrigido**, §3.9.1. Fronteira definida por "de que o diagnóstico precisa", listas sem repetição, e a checagem morta devolvida ao compilador |
| 10 | MÉDIA | `Camera`, `FonteSimples`, `LegendaDeclarada`, `Trilha`, `Transicao` e `assets` citados e não definidos | **Corrigido**, §2.3. Os sete definidos, `Asset` incluído, e §3.9.1 diz onde o laudo mora e **por que o portão não o relê** |
| 11 | MÉDIA | nenhum briefing concreto na spec | **Corrigido**, §7.1, com os dois textos livres em citação literal. **Re-corrigido em 01/10/2026:** o exemplo declara `pista: "tela"` (fidelidade ao `modo: "cartela"` do `props.json`) e `formatos: ["9:16", "1:1"]`, e a subseção final mede que o portão de ritmo **o reprova** por `legenda-recuada`, com recuo de 14 frames — o que a primeira correção não dizia |
| 12 | MÉDIA | compatibilidade do `props.json` afirmada sem mecanismo | **Corrigido**, §6 item 3. Migração de mão única, e o detalhe de que 34→segundos daria 1,1333 |
| 13 | MÉDIA | estático e carrossel não existem nem como exclusão | **Corrigido**, §5 e **D12**. 7 das 12 séries, 2 das 3 prontas, e D12 como pré-requisito de P1 |
| 14 | MÉDIA | não cabe num plano só | **Corrigido**, §7.2. P0..P6 com a coluna de pré-requisito |
| 15 | MÉDIA | coordenada de recorte sem unidade; `registro` × `enquadramento` sem regra | **Corrigido**, §2.3, §3.3.2 e §5. Fração do arquivo **já orientado**; tabela do que cada `registro` desenha e a recusa de `telaCheia` + `faixa` **com o número na mensagem** |
| 16 | BAIXA | "os 12 packshots" generalizado de 3; "5 das 12 séries" sem marca; 4,69 × 4,33 | **Corrigido, e a correção achou coisa pior.** Medi os 12 packshots (todos `Orientation 6`, todos 4096×2304) **e as 26 fotos da fazenda** — e **8 das 26 são `Orientation 6`**, exibindo 0,75, o que derruba a conta de enquadramento de §3.3.1 e reformula D5. "5 das 12" virou "7 das 12 partem de foto" + "5 das 12 entregam Reel de foto", as duas com marca. 4,69% e 4,33% são zona e bloco, e agora está escrito qual é qual |
| 17 | BAIXA | `DURACAO_MINIMA` re-derivada; plano deslocado em um em `proibicoes.md` | **Corrigido**, §3.9 e §6 item 5. O portão **importa** a constante de `movimento.ts:122`; a linha 19/20 conferida no arquivo e a divergência do plano registrada |
| 18 | BAIXA | `totalFixo` reescreve em silêncio; desempate indefinido | **Corrigido**, §3.2.2. A reescrita nunca toca o `briefing.json`, sai no diagnóstico cena por cena, e o desempate é maior duração, menor índice |
| 19 | BAIXA | `formatos: ['16:9']` passa tudo e falha no render | **Corrigido**, §3.1 e §5. Dois enums com dois nomes: `Zonas['formato']` mantém `16:9` como rótulo geométrico, `Formato` não |
| 20 | BAIXA | o portão `ritmo` não aparece no diagrama de fluxo | **Corrigido**, §2.1. Está no fluxo, antes do render, e a linha final diz **seis** portões |

**O que recusei, e por quê.** Dois pedaços, os dois medidos:

1. **A interseção não é 100% da caixa da legenda** (achado 6). Medi área nos dois
   eixos: **15,67%** no 1:1, **14,07%** no 4:5, **22,26%** no 16:9 — e **0,0% no
   9:16**. O cético mediu só o eixo y, onde a legenda de fato cabe inteira dentro
   da faixa vertical da manchete. O veredito dele sobrevive inteiro — o rótulo da
   spec **estava** errado, e ele achou um defeito que eu não tinha visto —, mas o
   número de substituição que ele propôs erra pelo mesmo motivo que o meu. Registro
   porque é a terceira aparição do mesmo erro nesta spec, e porque o eixo x é
   justamente onde estava a causa (§3.4.2).
2. **`aceitaTempoMorto` não é "ou a regra 2 é falsa, ou é HTTP 200"** (achado 8).
   O achado põe duas saídas e as duas são ruins. Há uma terceira e ela é melhor: a
   regra 2 fala de **técnicas de desenho**, e a chave não é uma — é supressor de
   portão. Em vez de escolher entre os dois chifres, separei as 12 chaves em três
   classes, e o dilema desaparece. A parte do achado que **aceitei** é a que
   importa mais: a spec não dizia qual dos dois valia, e não dizer era o defeito.

**Duas lições para o `CLAUDE.md`**, que valem além desta spec:

- **Interseção de caixas é grandeza de dois eixos.** Medir um eixo devolve um
  número plausível, e plausível passa na revisão — foi assim que `353,20 px` entrou
  como [medido] nesta spec e que `172,80 px` entrou como correção na crítica dela.
  Ao medir sobreposição, meça **área**, e confira que a área é ≤ a menor das duas
  caixas. A conta que falha não é a difícil; é a que ninguém repetiu no outro eixo.
- **Metadado de rotação ignorado é o defeito padrão deste repositório, e já tem
  três casos:** `displaymatrix` no `pl.mp4`, EXIF `Orientation` nos recortes de
  embalagem (os três PNG em `public/assets/` estão deitados em 4096×2304), e EXIF
  em `sondar()`. Em todo ponto que recebe arquivo de imagem ou vídeo, a dimensão de
  exibição é **derivada** de metadado de rotação — e o metadado tem **dois** nomes
  por tecnologia. Ler `width`/`height` é o bug, não o atalho. E a terceira vez não
  é azar: é o que acontece quando a regra fica num comentário de função em vez de
  numa lição escrita.
