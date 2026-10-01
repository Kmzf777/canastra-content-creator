// A GEOMETRIA da camada de texto de tela. Pura: sem React, sem remotion, sem
// DOM. O `.tsx` ao lado so pinta o que esta funcao decidiu.
//
// Mesma razao de `src/motor/movimento.ts` para viver fora do componente: o
// `.tsx` importa `tipografia.ts`, que faz `loadFont` no topo do modulo e
// derruba o vitest em Node. O que precisa de prova mora aqui.
//
// ---------------------------------------------------------------------------
// A DECISAO QUE ESTE ARQUIVO TOMA, E QUE `layout()` NAO TOMA
//
// `layout()` devolve `zonas.manchete`, mas essa zona NAO esta contida na area
// segura. Medido em 30/09/2026, no 1:1 de 1080x1080 com fonte 9:16:
//
//   seguro   x 160,0 .. 920,0   y  90,0 .. 770,0
//   manchete x 645,3 .. 1042,2  y 129,6 .. 950,4
//
// ou seja, a zona de manchete vaza 122 px pela direita e 180 px por baixo. No
// 16:9 vaza 179 px pela direita. Escrever o texto direto em `zonas.manchete`
// poria manchete fora do quadro seguro do Instagram em dois dos tres formatos.
//
// Entao a caixa daqui e sempre a INTERSECAO com `zonas.seguro`. O recorte e
// carregando, nao cosmetico -- e ele que o teste "o texto nunca sai da area
// segura" esta provando.
//
// ---------------------------------------------------------------------------
// O CORPO E ENCONTRADO, NAO ESCOLHIDO
//
// Nao existe token de "tamanho de manchete", e inventar um seria escolher no
// olho um numero que muda de significado a cada formato. Em vez disso o corpo e
// o MAIOR inteiro cujo bloco de texto ainda cabe na caixa -- medido com as
// larguras de avanco lidas dos proprios .ttf (`src/identidade/glifos.ts`).
//
// Por isso este modulo nao tem nenhuma constante numerica propria. Confira: as
// unicas grandezas sao as que chegam por `tokens.ts`, por `glifos.ts` ou pela
// caixa.

import {COR, LEGENDA, SOMBRA} from '../../identidade/tokens';
import {METRICAS, larguraEm} from '../../identidade/glifos';
import {atrasoDoIrmao, duracaoComIrmaos, duracaoDeIrmao} from '../movimento';
import type {Cadencia} from '../cadencia';
import {
  CADENCIA_DO_PAPEL,
  FAMILIA_DO_PAPEL,
  type CadenciaTexto,
  type PapelEvento,
} from '../evento';
import type {Papel} from '../../identidade/tipografia';
import type {Caixa, Zonas} from '../layout';

/**
 * `sobreImagem`: a manchete divide o quadro com o video, que continua correndo.
 * `cartela`: a tela inteira vira texto entre dois planos.
 */
export type Modo = 'sobreImagem' | 'cartela';

/**
 * Papel de um texto de tela. Sao os papeis de EVENTO -- e o mapa para a familia de
 * tipografia e `FAMILIA_DO_PAPEL`, nunca indexacao direta: `GLIFOS` tem as chaves
 * manchete/corpo/dado, e `papel: 'etiqueta'` indexado direto lancava
 * `TypeError: Cannot read properties of undefined (reading 'x')` (medido).
 */
export type PapelTexto = PapelEvento;

export type PalavraPosta = {
  texto: string;
  /** posicao na frase: e o indice de irmao que o stagger usa */
  irmao: number;
  /** em que linha a palavra caiu, depois da quebra */
  linha: number;
  cor: string;
  /** frames de espera antes desta palavra comecar a entrar */
  atrasoFrames: number;
};

export type SombraPosta = {
  perfil: 'sobreVideo';
  dy: number;
  blur: number;
  op: number;
};

export type Forma = {
  modo: Modo;
  papel: PapelTexto;
  /** a familia de tipografia do papel. E ela que o `.tsx` usa, nao o papel. */
  familia: Papel;
  /** como este texto se revela: `CADENCIA_DO_PAPEL[papel]` */
  cadenciaTexto: CadenciaTexto;
  /**
   * Quantos elementos ESCALONADOS o texto tem, pela cadencia.
   *
   * `palavra` -> uma por palavra · `linha` -> uma por linha · `bloco` -> 1.
   *
   * ESTE CAMPO EXISTE PARA O PLANO E O PIXEL NAO DISCORDAREM. Quem dimensiona a
   * duracao (`duracaoDeIrmao`, `duracaoComIrmaos`) tem que contar a MESMA coisa que
   * o stagger escalona. Antes de 01/10/2026 o compilador contava por cadencia e
   * `TextoTela` contava `palavras.length`: a etiqueta `MEDEIROS 1250 M` recebia 36
   * frames e desenhava 42.
   */
  irmaos: number;
  /** ja recortada contra `zonas.seguro` */
  caixa: Caixa;
  /** px do quadro */
  corpo: number;
  /** multiplicador de `corpo` */
  entrelinha: number;
  linhas: string[];
  palavras: PalavraPosta[];
  larguraBloco: number;
  alturaBloco: number;
  /**
   * `true` quando foi o TETO DO QUADRO que parou a busca, e nao a caixa da pista.
   *
   * E o unico sinal de que o texto pediu mais do que o quadro aceita. Sem ele o
   * teto agiria em silencio, que e o defeito que este motor persegue em toda parte.
   */
  noTetoDoQuadro: boolean;
  cor: string;
  /** cor de fundo da tela inteira, ou `null` se o video continua visivel */
  fundo: string | null;
  sombra: SombraPosta | null;
  alinhaHorizontal: 'flex-start';
  alinhaVertical: 'flex-start' | 'center';
};

// ---------------------------------------------------------------------------

/** Tolerancia de ponto flutuante: 4*90*0,96 nao da exatamente 345,6 em binario. */
const EPS = 1e-6;

function intersecao(a: Caixa, b: Caixa): Caixa {
  const x = Math.max(a.x, b.x);
  const y = Math.max(a.y, b.y);
  const direita = Math.min(a.x + a.largura, b.x + b.largura);
  const baixo = Math.min(a.y + a.altura, b.y + b.altura);
  return {x, y, largura: Math.max(0, direita - x), altura: Math.max(0, baixo - y)};
}

/**
 * Quebra gulosa em linhas que cabem em `largura`.
 *
 * Palavra sozinha maior que a caixa fica sozinha na linha e ESTOURA -- de
 * proposito. Quem corrige isso e a busca de corpo, que enxerga o estouro pela
 * `larguraBloco` e desce o tamanho. Hifenizar ou cortar a palavra esconderia o
 * problema no lugar de resolve-lo.
 */
export function quebrar(
  texto: string,
  {papel, corpo, largura}: {papel: PapelTexto; corpo: number; largura: number},
): string[] {
  // Pela FAMILIA, nunca pelo papel cru: `GLIFOS['etiqueta']` e `undefined`.
  const familia = FAMILIA_DO_PAPEL[papel];
  const palavras = texto.split(/\s+/).filter((p) => p.length > 0);
  if (palavras.length === 0) return [];

  const linhas: string[] = [];
  let atual = palavras[0];
  for (let i = 1; i < palavras.length; i++) {
    const tentativa = `${atual} ${palavras[i]}`;
    if (larguraEm(tentativa, familia) * corpo <= largura + EPS) {
      atual = tentativa;
    } else {
      linhas.push(atual);
      atual = palavras[i];
    }
  }
  linhas.push(atual);
  return linhas;
}

function contarPalavras(texto: string): number {
  return texto.split(/\s+/).filter((p) => p.length > 0).length;
}

/**
 * Quantos frames CADA palavra fica presente, para que a frase apareca inteira.
 *
 * Nao e `DURACAO_MINIMA`: com a janela minima para todas, a primeira palavra
 * comeca a sair antes de a ultima terminar de entrar. Ver `duracaoDeIrmao`.
 */
export function duracaoPorPalavra(texto: string, c: Cadencia): number {
  return duracaoDeIrmao(contarPalavras(texto), c);
}

/**
 * Quantos frames a FRASE inteira ocupa, stagger incluido.
 *
 * Existe porque o erro natural e dimensionar a `<Sequence>` por
 * `DURACAO_MINIMA`: o stagger empurra o fim junto com o comeco, entao a ultima
 * palavra perderia a saida e sumiria por corte em vez de sair.
 */
export function duracaoDaFrase(
  texto: string,
  c: Cadencia,
  duracao: number = duracaoPorPalavra(texto, c),
): number {
  const n = contarPalavras(texto);
  if (n === 0) return 0;
  return duracaoComIrmaos(n, duracao, c);
}

function medirBloco(
  texto: string,
  papel: PapelTexto,
  corpo: number,
  entrelinha: number,
  caixa: Caixa,
) {
  const familia = FAMILIA_DO_PAPEL[papel];
  const linhas = quebrar(texto, {papel, corpo, largura: caixa.largura});
  const larguraBloco = linhas.reduce(
    (m, l) => Math.max(m, larguraEm(l, familia) * corpo),
    0,
  );
  const alturaBloco = linhas.length * corpo * entrelinha;
  return {linhas, larguraBloco, alturaBloco};
}

export function formaTextoTela({
  texto,
  modo,
  zonas,
  papel = 'manchete',
  palavraAcento,
  cadencia,
  linhaMaxima,
}: {
  texto: string;
  modo: Modo;
  zonas: Zonas;
  papel?: PapelTexto;
  /** indice da UNICA palavra que recebe `COR.acento`. Fora da faixa = nenhuma. */
  palavraAcento?: number;
  /** de `cadencia(useVideoConfig().fps)`. Obrigatorio: sem ele o stagger volta a
   *  ser 3 frames em qualquer fps. */
  cadencia: Cadencia;
  /**
   * O TETO: altura maxima de UMA LINHA, em pixeis do quadro.
   *
   * Chega em PIXEIS DE LINHA, e nao em corpo, para a entrelinha continuar morando
   * num arquivo so. Quem calcula o teto (`motor/encaixe.ts`) sabe a altura do
   * quadro mas NAO sabe se este texto vai ser desenhado com a entrelinha natural da
   * fonte (cartela) ou com a apertada da legenda (sobre imagem) -- a escolha e feita
   * dez linhas abaixo, aqui. Mandar o corpo maximo de la obrigaria os dois arquivos a
   * saber a mesma regra, e duas copias de uma regra divergem no primeiro conserto.
   *
   * `undefined` = sem teto. E o que a cartela usa: ela pinta `COR.terra` por cima da
   * fonte, entao nao ha nada embaixo para tapar.
   */
  linhaMaxima?: number;
}): Forma {
  // A caixa. `cartela` toma a area segura inteira; `sobreImagem` toma a faixa
  // de manchete que `layout()` reservou -- as duas recortadas contra o seguro.
  const caixa =
    modo === 'cartela' ? zonas.seguro : intersecao(zonas.manchete, zonas.seguro);

  // O respiro. Na cartela a entrelinha e a NATURAL da fonte, lida de `hhea`
  // (manchete 1,088); sobre a imagem e a apertada da legenda (0,96), que e o
  // valor medido para texto sobre video. A diferenca de respiro entre os dois
  // modos nao e um numero escolhido: e a distancia entre essas duas medidas.
  const familia = FAMILIA_DO_PAPEL[papel];
  const entrelinha =
    modo === 'cartela' ? METRICAS[familia].alturaLinha : LEGENDA.entrelinha;

  // O RESPIRO DA CARTELA, medido e nao escolhido.
  //
  // Sem isto a cartela apenas MAXIMIZA o corpo, e no 16:9 o resultado media
  // 368,8 px de bloco numa caixa de 368,9 px -- texto de borda a borda, o
  // oposto de "respiro maior". Entao a cartela reserva UMA LINHA de folga
  // vertical: o bloco tem que caber como se tivesse uma linha a mais.
  //
  // "Uma linha" e a unidade que a propria fonte define (`corpo * entrelinha`,
  // com a entrelinha natural lida de `hhea`), entao o respiro nasce da medida
  // do arquivo, nao de um percentual escolhido no olho. `sobreImagem` nao
  // reserva nada: a faixa de manchete e estreita de proposito e a folga dela e
  // a zona da legenda, logo abaixo.
  const linhasDeFolga = modo === 'cartela' ? 1 : 0;

  // Busca binaria pelo maior corpo inteiro que ainda cabe. O teto da CAIXA e uma
  // linha unica ocupando a altura toda -- acima disso nada cabe, por definicao.
  //
  // O TETO DO QUADRO ENTRA AQUI, E NAO NO VEREDITO, E ESSA E A PARTE QUE IMPORTA.
  //
  // Medido em 01/10/2026: `250 G` em `dado`/`principal` no 9:16 saia com corpo 410 px
  // -- a caixa de `principal` tem 788,74 px de altura e a busca MAXIMIZA, entao cinco
  // caracteres esticam ate preencher 41% do quadro. O still (out/antes-f261.png)
  // mostra o `250` cobrindo o ombro do pacote e o `G` em cima do logotipo.
  //
  // Um teto que so reprovasse no diagnostico deixaria o pixel errado sair do mesmo
  // jeito -- e a licao 3 do CLAUDE.md: relatorio nao e efeito. Entao o teto e um LIMITE
  // DE BUSCA: o corpo escolhido ja nasce dentro dele.
  const tetoDaCaixa = Math.max(1, Math.floor(caixa.altura / entrelinha));
  const tetoDoQuadro =
    linhaMaxima === undefined ? Infinity : Math.max(1, Math.floor(linhaMaxima / entrelinha));
  const teto = Math.min(tetoDaCaixa, tetoDoQuadro);
  const cabe = (c: number) => {
    const m = medirBloco(texto, papel, c, entrelinha, caixa);
    const alturaPedida = m.alturaBloco + linhasDeFolga * c * entrelinha;
    return m.larguraBloco <= caixa.largura + EPS && alturaPedida <= caixa.altura + EPS;
  };

  let corpo = 1;
  let lo = 1;
  let hi = teto;
  while (lo <= hi) {
    const meio = Math.floor((lo + hi) / 2);
    if (cabe(meio)) {
      corpo = meio;
      lo = meio + 1;
    } else {
      hi = meio - 1;
    }
  }
  // Rede: a busca binaria supoe que "cabe" e monotonico no corpo. A quebra de
  // linha quase garante isso, mas "quase" nao e prova -- entao desce ate caber
  // de fato, ou ate 1. Sem isso um caso patologico entregaria texto vazando com
  // o teste verde.
  while (corpo > 1 && !cabe(corpo)) corpo--;

  // QUEM SEGUROU O CORPO: a caixa da pista, ou o teto do quadro?
  //
  // O numero sozinho nao conta essa historia, e as duas respostas pedem conserto
  // diferente -- caixa apertada se resolve mudando a pista, teto atingido se resolve
  // encurtando o texto. `corpo === tetoDoQuadro` nao bastaria: o corpo pode coincidir
  // com o teto por acaso enquanto a caixa e o limite de fato.
  const noTetoDoQuadro = tetoDoQuadro < tetoDaCaixa && corpo === tetoDoQuadro;

  const {linhas, larguraBloco, alturaBloco} = medirBloco(
    texto,
    papel,
    corpo,
    entrelinha,
    caixa,
  );

  // O INDICE DE IRMAO SAI DA CADENCIA DO PAPEL, nao do numero de palavras.
  //
  // Antes de 01/10/2026 este bloco incrementava `irmao` por PALAVRA em todo papel, e
  // `CADENCIA_DO_PAPEL` existia sem chegar aqui. As consequencias eram duas, e as
  // duas medidas: (a) `duracaoDaFrase('R$ 39,90')` tratava `R$` e `39,90` como dois
  // irmaos, e um cartao de preco que revela `R$` e o numero 3 frames depois le como
  // defeito -- e essa e a justificativa ESCRITA da cadencia do `dado`; (b) a etiqueta
  // `MEDEIROS 1250 M` recebia 36 frames do plano (1 irmao, cadencia `bloco`) e
  // desenhava 42 (3 palavras), porque o plano contava por cadencia e a tela contava
  // por palavra.
  //
  // `irmaoDaPalavra` e a UNICA regra, e ela vale para o atraso E para a contagem:
  //
  //   palavra .... o indice da palavra na FRASE (nao na linha): o stagger varre a
  //                manchete inteira e nao reinicia a cada quebra
  //   linha ...... o indice da LINHA. Cada linha de um dado e um campo, e as
  //                palavras de uma linha entram juntas
  //   bloco ...... sempre 0. Um carimbo nao tem ritmo interno: ou esta no quadro
  //                ou nao esta
  const cadenciaTexto = CADENCIA_DO_PAPEL[papel];
  const palavras: PalavraPosta[] = [];
  let indiceNaFrase = 0;
  linhas.forEach((linha, iLinha) => {
    for (const p of linha.split(' ')) {
      const irmao =
        cadenciaTexto === 'palavra'
          ? indiceNaFrase
          : cadenciaTexto === 'linha'
            ? iLinha
            : 0;
      palavras.push({
        texto: p,
        irmao,
        linha: iLinha,
        // UM acento por cena: uma palavra, nunca duas. O indice do acento continua
        // sendo o da PALAVRA na frase, e nao o de irmao -- senao numa etiqueta
        // (todos os irmaos 0) o acento pintaria o bloco inteiro.
        cor: indiceNaFrase === palavraAcento ? COR.acento : COR.creme,
        atrasoFrames: atrasoDoIrmao(irmao, cadencia),
      });
      indiceNaFrase++;
    }
  });

  const irmaos =
    cadenciaTexto === 'palavra'
      ? Math.max(1, palavras.length)
      : cadenciaTexto === 'linha'
        ? Math.max(1, linhas.length)
        : 1;

  return {
    modo,
    papel,
    familia,
    cadenciaTexto,
    irmaos,
    caixa,
    corpo,
    entrelinha,
    linhas,
    palavras,
    larguraBloco,
    alturaBloco,
    noTetoDoQuadro,
    cor: COR.creme,
    // A cartela cobre o quadro com terra. Nunca branco: `proibicoes.md` nomeia
    // "fundo branco puro com texto centrado" como o padrao do modelo generativo.
    fundo: modo === 'cartela' ? COR.terra : null,
    // Sombra so onde ha video atras. Na cartela o texto esta sobre cor chapada,
    // e sombra ali seria decoracao, nao leitura.
    //
    // O perfil e o mesmo `sobreVideo` da legenda -- mesmo material, texto creme
    // sobre imagem em movimento -- mas em PIXEIS diferentes: escalado pelo corpo
    // contra o corpo da legenda. Uma manchete de 123 px com a sombra de um
    // texto de 78 px pareceria sem sombra nenhuma.
    sombra:
      modo === 'sobreImagem'
        ? {
            perfil: 'sobreVideo',
            dy: (SOMBRA.sobreVideo.dy * corpo) / LEGENDA.corpoEm1080,
            blur: (SOMBRA.sobreVideo.blur * corpo) / LEGENDA.corpoEm1080,
            op: SOMBRA.sobreVideo.op,
          }
        : null,
    // Alinhado a esquerda nos DOIS modos. Centrar texto e o reflexo do modelo
    // generativo sem direcao, e `proibicoes.md` chama isso pelo nome.
    alinhaHorizontal: 'flex-start',
    // O respiro da cartela e vertical: o bloco flutua no meio da area segura,
    // e a sobra vira margem em cima e embaixo. A manchete sobre video ancora no
    // topo da faixa dela, porque embaixo passa a legenda.
    alinhaVertical: modo === 'cartela' ? 'center' : 'flex-start',
  };
}
