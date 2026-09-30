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
import type {Caixa, Zonas} from '../layout';

/**
 * `sobreImagem`: a manchete divide o quadro com o video, que continua correndo.
 * `cartela`: a tela inteira vira texto entre dois planos.
 */
export type Modo = 'sobreImagem' | 'cartela';

/** Os dois papeis que um texto de tela pode ter. `corpo` e da legenda. */
export type PapelTexto = 'manchete' | 'dado';

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
  const palavras = texto.split(/\s+/).filter((p) => p.length > 0);
  if (palavras.length === 0) return [];

  const linhas: string[] = [];
  let atual = palavras[0];
  for (let i = 1; i < palavras.length; i++) {
    const tentativa = `${atual} ${palavras[i]}`;
    if (larguraEm(tentativa, papel) * corpo <= largura + EPS) {
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
export function duracaoPorPalavra(texto: string): number {
  return duracaoDeIrmao(contarPalavras(texto));
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
  duracao: number = duracaoPorPalavra(texto),
): number {
  const n = contarPalavras(texto);
  if (n === 0) return 0;
  return duracaoComIrmaos(n, duracao);
}

function medirBloco(
  texto: string,
  papel: PapelTexto,
  corpo: number,
  entrelinha: number,
  caixa: Caixa,
) {
  const linhas = quebrar(texto, {papel, corpo, largura: caixa.largura});
  const larguraBloco = linhas.reduce((m, l) => Math.max(m, larguraEm(l, papel) * corpo), 0);
  const alturaBloco = linhas.length * corpo * entrelinha;
  return {linhas, larguraBloco, alturaBloco};
}

export function formaTextoTela({
  texto,
  modo,
  zonas,
  papel = 'manchete',
  palavraAcento,
}: {
  texto: string;
  modo: Modo;
  zonas: Zonas;
  papel?: PapelTexto;
  /** indice da UNICA palavra que recebe `COR.acento`. Fora da faixa = nenhuma. */
  palavraAcento?: number;
}): Forma {
  // A caixa. `cartela` toma a area segura inteira; `sobreImagem` toma a faixa
  // de manchete que `layout()` reservou -- as duas recortadas contra o seguro.
  const caixa =
    modo === 'cartela' ? zonas.seguro : intersecao(zonas.manchete, zonas.seguro);

  // O respiro. Na cartela a entrelinha e a NATURAL da fonte, lida de `hhea`
  // (manchete 1,088); sobre a imagem e a apertada da legenda (0,96), que e o
  // valor medido para texto sobre video. A diferenca de respiro entre os dois
  // modos nao e um numero escolhido: e a distancia entre essas duas medidas.
  const entrelinha =
    modo === 'cartela' ? METRICAS[papel].alturaLinha : LEGENDA.entrelinha;

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

  // Busca binaria pelo maior corpo inteiro que ainda cabe. O teto e uma linha
  // unica ocupando a altura toda -- acima disso nada cabe, por definicao.
  const teto = Math.max(1, Math.floor(caixa.altura / entrelinha));
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

  const {linhas, larguraBloco, alturaBloco} = medirBloco(
    texto,
    papel,
    corpo,
    entrelinha,
    caixa,
  );

  // As palavras, na ordem do texto, cada uma sabendo em que linha caiu e quanto
  // espera para entrar. O indice de irmao e o da FRASE, nao o da linha: o
  // stagger tem que varrer a manchete inteira, nao reiniciar a cada quebra.
  const palavras: PalavraPosta[] = [];
  let irmao = 0;
  linhas.forEach((linha, iLinha) => {
    for (const p of linha.split(' ')) {
      palavras.push({
        texto: p,
        irmao,
        linha: iLinha,
        // UM acento por cena: uma palavra, nunca duas.
        cor: irmao === palavraAcento ? COR.acento : COR.creme,
        atrasoFrames: atrasoDoIrmao(irmao),
      });
      irmao++;
    }
  });

  return {
    modo,
    papel,
    caixa,
    corpo,
    entrelinha,
    linhas,
    palavras,
    larguraBloco,
    alturaBloco,
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
