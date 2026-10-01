// AS PISTAS: as faixas horizontais em que uma camada de texto mora.
//
// Duas responsabilidades, nesta ordem: os NOMES (pistas, conflitos, nomes de
// encaixe) e depois a GEOMETRIA (coluna de texto, caixa de pista, derivacao de
// encaixe). A primeira metade nasceu antes da segunda de proposito -- `evento.ts`
// importa o tipo `Pista` daqui, e se o tipo morasse em `layout.ts` a tabela de
// papeis dependeria da geometria.
//
// O QUE ESTE ARQUIVO PODE IMPORTAR, E O QUE NAO PODE
//
// `./layout` pode: ele e puro e nao importa nada de `identidade/`. Qualquer coisa
// de `identidade/` NAO pode -- `tipografia.ts` faz `loadFont` no topo do modulo e
// derruba o vitest em Node com `TypeError: Invalid URL`, e `esquema.ts` importa
// `PISTAS_DE_EVENTO` daqui. A MEDICAO do texto na caixa, que precisa de glifos,
// mora em `motor/encaixe.ts` por essa razao mecanica, e nao por gosto de arquivo.

import {MARGEM, type Caixa, type Zonas} from './layout';

/** As quatro pistas horizontais em que uma camada de texto pode morar. */
export const PISTAS = ['topo', 'principal', 'rodape', 'tela'] as const;
export type Pista = (typeof PISTAS)[number];

/**
 * As pistas que um EVENTO pode declarar. `rodape` NAO esta na lista: ela e a caixa
 * da camada `Legenda`, e um evento ali cairia sobre a fala.
 */
export const PISTAS_DE_EVENTO = ['topo', 'principal', 'tela'] as const;
export type PistaDeEvento = (typeof PISTAS_DE_EVENTO)[number];

/**
 * A forma da caixa de um texto. DERIVADA de (pista, formato), NUNCA declarada.
 *
 * Eram tres valores no briefing, como lista de preferencia. Sairam de la porque
 * `faixa` x `coluna` nao e escolha, e consequencia do formato: no 9:16 a sobra ao
 * lado do video e 0,00 px (medido), logo `encaixe: ['coluna']` ali e
 * insatisfazivel -- um campo que o motor nao pode honrar e o HTTP 200 que ignora o
 * parametro, licao 3 do CLAUDE.md. A derivacao e `encaixe()`, no fim deste arquivo.
 */
export const ENCAIXES = ['faixa', 'coluna', 'cartela'] as const;
export type Encaixe = (typeof ENCAIXES)[number];

/**
 * Que pistas cada pista bloqueia.
 *
 * `tela` e a cartela: ela ocupa o quadro e portanto conflita com `topo` e
 * `principal`. NAO conflita com `rodape`, porque a legenda continua correndo por
 * cima do terra chapado da cartela -- a escolha que o motor antigo ja defendeu por
 * escrito: cartela por cima de tudo apagaria a legenda por dois segundos e
 * quebraria a continuidade de leitura, que e pior.
 */
export const CONFLITO_DE_PISTA: Record<Pista, readonly Pista[]> = {
  topo: ['topo', 'tela'],
  principal: ['principal', 'tela'],
  rodape: ['rodape'],
  tela: ['tela', 'topo', 'principal'],
};

// ---------------------------------------------------------------------------
// A GEOMETRIA
//
// UMA PISTA E UMA FAIXA HORIZONTAL DE UMA COLUNA DE TEXTO, e as duas coisas sao
// DERIVADAS, nunca declaradas. A coluna primeiro, porque a pista depende dela.

/**
 * A partir de que sobra ao lado do video a coluna de texto vira a sobra.
 *
 * `[escolhido]`, e a razao e medida: as sobras sao 0,00 px no 9:16 (0,00% da
 * largura), 472,50 no 1:1 (43,75%), 320,63 no 4:5 (29,69%) e 1312,50 no 16:9
 * (68,36%), com fonte retrato. Qualquer limiar entre 0 e 29,69% separa os MESMOS
 * grupos; 0,22 fica no meio do vao e nao encosta em nenhum lado.
 *
 * Com fonte em PAISAGEM (as 26 fotos da fazenda, 4032x3024) as sobras sao 0,00 nos
 * tres verticais e 480,00 px (25,00%) no 16:9 -- entao a coluna cai no seguro do
 * video nos formatos que a gente entrega, e e por isso que a faixa e o encaixe da
 * peca de foto parada.
 */
export const LIMIAR_DE_COLUNA = 0.22;

function intersecao(a: Caixa, b: Caixa): Caixa {
  const x = Math.max(a.x, b.x);
  const y = Math.max(a.y, b.y);
  const direita = Math.min(a.x + a.largura, b.x + b.largura);
  const baixo = Math.min(a.y + a.altura, b.y + b.altura);
  return {x, y, largura: Math.max(0, direita - x), altura: Math.max(0, baixo - y)};
}

/**
 * A area segura DO VIDEO, que nao e a do quadro.
 *
 * Um evento em encaixe `faixa` mora SOBRE a imagem, e a imagem nem sempre e o
 * quadro: no 1:1 com fonte retrato ela e uma coluna de 607,50 px de largura, e com
 * fonte paisagem ela e uma faixa de 810,00 px de altura no meio de 1080. Usar o
 * seguro do QUADRO poria a faixa metade sobre a imagem e metade sobre o terra
 * chapado -- e, com fonte paisagem, INTEIRAMENTE fora dela.
 *
 * As mesmas fracoes de `MARGEM`, aplicadas aos eixos do VIDEO, e depois recortadas
 * contra o seguro do quadro: a borda do Instagram nao perdoa nem o que esta sobre
 * imagem.
 */
export function seguroDoVideo(z: Zonas): Caixa {
  return intersecao(
    {
      x: z.video.x + MARGEM.lado * z.video.largura,
      y: z.video.y + MARGEM.topo * z.video.altura,
      largura: z.video.largura * (1 - 2 * MARGEM.lado),
      altura: z.video.altura * (1 - MARGEM.topo - MARGEM.base),
    },
    z.seguro,
  );
}

/**
 * A largura do QUADRO, reconstruida das zonas.
 *
 * `seguro.x` e `MARGEM.lado * largura` e `seguro.largura` e
 * `largura * (1 - 2*MARGEM.lado)`, logo a soma das tres partes devolve a largura
 * inteira. Preferivel a passar a largura por parametro em cinco funcoes: um
 * parametro a mais e um lugar a mais para alguem passar o numero errado.
 */
function larguraDoQuadro(z: Zonas): number {
  return z.seguro.largura + 2 * z.seguro.x;
}

/**
 * A coluna em que o texto de evento mora.
 *
 * Duas respostas, e a escolha e do FORMATO, nao de quem escreve o briefing:
 *
 *   sobra >= LIMIAR_DE_COLUNA  ->  a caixa da sobra ao lado do video
 *   senao                      ->  o seguro DO VIDEO
 *
 * No segundo caso o texto fica SOBRE a imagem; no primeiro, AO LADO dela. Nenhum
 * dos dois e melhor: eles sao o que cabe.
 */
export function colunaDeTexto(z: Zonas): Caixa {
  const largura = larguraDoQuadro(z);
  const sobra = largura - z.video.largura;
  return sobra >= LIMIAR_DE_COLUNA * largura
    ? intersecao(z.manchete, z.seguro)
    : seguroDoVideo(z);
}

/**
 * As fracoes de altura das pistas de EVENTO, sobre a coluna de texto.
 *
 * `[escolhido]`, e amarradas a dois numeros medidos: a caixa de legenda e
 * `altura * 0.16` do QUADRO e, dentro do seguro do 9:16 -- que e 1.516,80 px de
 * 1.920,00 --, 307,20 / 1516,80 = 0,2025; 0,24 da a folga da segunda linha.
 * `topo` recebe a mesma altura que a folga de baixo porque uma faixa superior mais
 * baixa que a inferior le como desalinhamento, e o que sobra, 0,52, e `principal`.
 */
export const FRACAO_DE_PISTA = {topo: 0.24, principal: 0.52, folgaDeBaixo: 0.24} as const;

/**
 * As caixas das quatro pistas.
 *
 * `topo` e `principal` sao faixas da COLUNA DE TEXTO. `rodape` e literalmente
 * `z.legenda` -- a caixa da camada `Legenda`, nao uma caixa parecida com ela. E
 * `tela` e o seguro do quadro, onde a cartela desenha.
 *
 * POR QUE `rodape` NAO E A FAIXA DE BAIXO DA COLUNA. Com fonte em paisagem no 1:1,
 * a faixa de baixo da coluna fica em `y 661,82 .. 815,40` e `z.legenda` em
 * `y 734,40 .. 907,20`: as duas se sobrepoem em 61.560 px². Existiriam DUAS caixas
 * quase iguais para a mesma coisa -- a que a `Legenda` desenha e a que o portao
 * confere --, e duas caixas quase iguais divergem no primeiro conserto. Entao a
 * faixa de baixo da coluna e apenas FOLGA: nenhum evento a declara, e e ela que
 * garante que `principal` nao encoste na legenda.
 */
export function pistas(z: Zonas): Record<Pista, Caixa> {
  const c = colunaDeTexto(z);
  return {
    topo: {x: c.x, y: c.y, largura: c.largura, altura: c.altura * FRACAO_DE_PISTA.topo},
    principal: {
      x: c.x,
      y: c.y + c.altura * FRACAO_DE_PISTA.topo,
      largura: c.largura,
      altura: c.altura * FRACAO_DE_PISTA.principal,
    },
    rodape: z.legenda,
    tela: z.seguro,
  };
}

/**
 * `encaixe(pista, zonas)` -- DERIVADO, nunca declarado.
 *
 *   pista === 'tela'            -> 'cartela'   -> Modo 'cartela'
 *   sobra < LIMIAR_DE_COLUNA    -> 'faixa'     -> Modo 'sobreImagem'
 *   senao                       -> 'coluna'    -> Modo 'sobreImagem'
 *
 * `coluna` e `faixa` caem no MESMO `Modo` porque a diferenca entre as duas nao e de
 * desenho de texto, e de CAIXA: as duas desenham creme sobre o que estiver atras, e
 * quem muda e a `Caixa` que chega. `Modo` tem dois valores, e o mapeamento 3 -> 2
 * fica explicito aqui em vez de um terceiro modo nascer em `texto-forma.ts`.
 */
export function encaixe(pista: Pista, z: Zonas): Encaixe {
  if (pista === 'tela') return 'cartela';
  const largura = larguraDoQuadro(z);
  const sobra = largura - z.video.largura;
  return sobra >= LIMIAR_DE_COLUNA * largura ? 'coluna' : 'faixa';
}

/** O `Modo` de `texto-forma.ts` que cada encaixe usa. O mapeamento 3 -> 2. */
export function modoDoEncaixe(e: Encaixe): 'sobreImagem' | 'cartela' {
  return e === 'cartela' ? 'cartela' : 'sobreImagem';
}

/** A caixa em que o texto daquela pista e medido e desenhado. */
export function caixaDaPista(pista: Pista, z: Zonas): Caixa {
  return pistas(z)[pista];
}
