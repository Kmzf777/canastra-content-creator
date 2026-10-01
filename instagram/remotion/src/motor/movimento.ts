// A GRAMATICA DE MOVIMENTO. Pura: sem React, sem remotion, sem DOM.
//
// POR QUE ESTA FORA DO .tsx
//
// `TextoTela.tsx` importa `tipografia.ts`, que tem efeito colateral de modulo
// (`delayRender` + `loadFont`). Em Node isso estoura `TypeError: Invalid URL`,
// porque `loadFont` faz `fetch` no caminho de asset do bundler. Medido em
// 30/09/2026: um teste que so importava `Legenda.tsx` passou a asercao e o
// vitest ainda saiu com codigo 1 por causa do erro nao tratado.
//
// Entao o que da para provar em Node mora aqui, e o .tsx e so fiacao. Este
// arquivo pode ser importado por qualquer camada futura -- cartela, selo, dado
// -- para que o motor tenha UMA gramatica de tempo, nao uma por componente.
//
// ---------------------------------------------------------------------------
// TODO NUMERO VEM DE `tokens.ts`. NENHUM NASCE AQUI.
//
// Duas derivacoes precisam estar escritas, porque nao sao leitura direta de
// token e a proxima sessao vai querer saber de onde sairam:
//
//   1. A SAIDA OCUPA OS MESMOS FRAMES DA ENTRADA (`c.entrada`). Nao existe
//      token de duracao de saida, e inventar um seria escolher no olho. O que
//      torna a saida "acelerada" e `TEMPO.saidaExpoente` (2,4), nao um numero
//      de frames menor: com t^2,4 a massa do movimento fica no fim, entao a
//      saida LE como mais rapida ocupando a mesma janela.
//
//   2. `c.overshoot` (3%) e lido como POUSO, nao como repique. A escala
//      entra 3% GRANDE e assenta em 100%; na saida continua descendo para 97%.
//      E uma direcao so, do primeiro ao ultimo frame. Repique -- passar do
//      alvo e voltar -- e easing elastico, e `src/identidade/proibicoes.md`
//      proibe easing elastico. Se um dia alguem quiser o repique, vai ter que
//      mexer na proibicao primeiro, de proposito.

import {PUSH, TEMPO} from '../identidade/tokens';
import type {Cadencia} from './cadencia';

export type Fase = 'antes' | 'entrada' | 'hold' | 'saida' | 'depois';

/** Janela de presenca de um elemento, em frames do tempo da CENA. */
export type Janela = {
  /** primeiro frame em que o elemento comeca a entrar */
  inicio: number;
  /** quantos frames o elemento fica presente, entrada e saida incluidas */
  duracao: number;
};

export type Estado = {
  fase: Fase;
  /** 0 fora, 1 presente. Serve de opacidade. */
  presenca: number;
  /** 1+overshoot no primeiro frame, 1 no hold, 1-overshoot no ultimo. */
  escala: number;
};

// ---------------------------------------------------------------------------
// o easing do token

/**
 * Le `cubic-bezier(x1,y1,x2,y2)` de CSS e devolve a curva em JS.
 *
 * Existe para que a curva medida no teste e a curva desenhada pelo Chrome sejam
 * os MESMOS quatro numeros. Se o easing fosse reescrito a mao em JS, um dia
 * alguem editaria `TEMPO.pousoEasing` e o movimento continuaria o antigo sem
 * ninguem perceber -- o modo de falha silencioso de sempre.
 */
export function bezierDeCss(css: string): (t: number) => number {
  const m = /^cubic-bezier\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)$/.exec(
    css.trim(),
  );
  if (!m) {
    throw new Error(
      `easing '${css}' nao e cubic-bezier(x1,y1,x2,y2). A gramatica de ` +
        'movimento nao aceita palavra-chave de CSS, porque o teste em Node nao ' +
        'tem como saber o que o navegador faria com ela.',
    );
  }
  const [x1, y1, x2, y2] = m.slice(1, 5).map(Number);

  // Bezier cubica com P0=(0,0) e P3=(1,1).
  const eixo = (t: number, a: number, b: number) => {
    const u = 1 - t;
    return 3 * u * u * t * a + 3 * u * t * t * b + t * t * t;
  };
  const derivadaX = (t: number) => {
    const u = 1 - t;
    return 3 * u * u * x1 + 6 * u * t * (x2 - x1) + 3 * t * t * (1 - x2);
  };

  return (x: number) => {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    // Newton primeiro, que converge em 3-4 passos nas curvas de UI.
    let t = x;
    for (let i = 0; i < 8; i++) {
      const erro = eixo(t, x1, x2) - x;
      if (Math.abs(erro) < 1e-7) return eixo(t, y1, y2);
      const d = derivadaX(t);
      if (Math.abs(d) < 1e-9) break;
      t -= erro / d;
    }
    // Bissecao como rede: Newton escorrega quando a derivada encosta em zero.
    let lo = 0;
    let hi = 1;
    t = x;
    for (let i = 0; i < 40; i++) {
      const v = eixo(t, x1, x2);
      if (Math.abs(v - x) < 1e-7) break;
      if (v < x) lo = t;
      else hi = t;
      t = (lo + hi) / 2;
    }
    return eixo(t, y1, y2);
  };
}

/** A curva de pouso da marca, lida de `TEMPO.pousoEasing`. */
export const POUSO = bezierDeCss(TEMPO.pousoEasing);

// ---------------------------------------------------------------------------
// reparticao da janela

// `DURACAO_MINIMA` era uma constante de modulo derivada de frames a 30 fps.
// Agora ela e `c.duracaoMinima`, porque depende do fps da composicao -- ver
// `motor/cadencia.ts`. A soma continua sendo entrada + holdFinal + entrada.

export type Fases = {entrada: number; hold: number; saida: number};

/**
 * Reparte `duracao` em entrada / hold / saida, em frames inteiros.
 *
 * Numa janela folgada as pontas sao `c.entrada` cheios e o hold fica com a
 * sobra. Numa janela curta as PONTAS cedem e o hold nunca fica negativo: um
 * elemento de 3 frames ainda tem uma fase de cada, um de 2 frames aparece
 * inteiro e sai inteiro. A alternativa -- deixar entrada e saida se
 * sobreporem -- daria presenca subindo e descendo no mesmo frame.
 */
export function fases(duracao: number, c: Cadencia): Fases {
  const d = Math.max(0, Math.floor(duracao));
  if (d === 0) return {entrada: 0, hold: 0, saida: 0};
  const ponta = Math.min(c.entrada, Math.floor(d / 3));
  return {entrada: ponta, hold: d - 2 * ponta, saida: ponta};
}

// ---------------------------------------------------------------------------
// o progresso

export function progresso(frame: number, janela: Janela, c: Cadencia): Estado {
  const {inicio, duracao} = janela;
  const t = frame - inicio;

  if (t < 0) return {fase: 'antes', presenca: 0, escala: 1 + c.overshoot};
  if (t >= duracao) return {fase: 'depois', presenca: 0, escala: 1 - c.overshoot};

  const f = fases(duracao, c);
  const inicioSaida = duracao - f.saida;

  // AS DUAS PONTAS SAO NORMALIZADAS PELO FRAME DESENHADO, NAO PELO VIZINHO QUE
  // NAO E DESENHADO. O `+1` de cada lado e isso, e cada um conserta um defeito
  // medido em 01/10/2026 numa janela de 36 frames:
  //
  //   entrada, sem o `+1`: `t / f.entrada` com t = 0 da 0, entao o PRIMEIRO
  //     frame renderizado de todo elemento saia com presenca 0,0000 -- um frame
  //     pago e invisivel -- e a entrada so completava no primeiro frame do hold.
  //     Com o `+1`, o primeiro frame desenhado sai em POUSO(1/12) = 0,334183 e a
  //     entrada fecha em t = 11, o ultimo frame dela.
  //
  //   saida, sem o `+1`: presenca nos seis ultimos frames desenhados era
  //     0,8105 0,7257 0,6221 0,4986 0,3544 0,1885 e o frame seguinte nunca e
  //     desenhado (`TextoTela.tsx` devolve null em `t >= duracaoCena`), entao o
  //     elemento desaparecia de 18,85% de opacidade para zero num frame -- o
  //     "sai seco" que `proibicoes.md` nao quer. O expoente 2,4 AMPLIFICA o
  //     erro: com saida linear o residuo seria 8,33%.
  //
  // Entrada: 0 -> 1 pela curva de pouso.
  const pEntrada = f.entrada === 0 ? 1 : Math.min(1, (t + 1) / f.entrada);
  const entrada = POUSO(pEntrada);

  // Saida: 1 -> 0 acelerando por t^saidaExpoente.
  const pSaida =
    f.saida === 0 || t < inicioSaida
      ? 0
      : Math.min(1, (t - inicioSaida + 1) / f.saida);
  const queda = Math.pow(pSaida, c.saidaExpoente);

  const fase: Fase = t < f.entrada ? 'entrada' : t < inicioSaida ? 'hold' : 'saida';

  return {
    fase,
    // `min` em vez de produto: no hold as duas valem 1, e nas pontas so uma
    // esta em transicao -- multiplicar so somaria erro de ponto flutuante.
    presenca: Math.min(entrada, 1 - queda),
    // Uma direcao so: 1+overshoot -> 1 -> 1-overshoot. Ver o cabecalho.
    escala: 1 + c.overshoot * (1 - entrada) - c.overshoot * queda,
  };
}

// ---------------------------------------------------------------------------
// irmaos

/** Quantos frames o irmao `indice` espera antes de comecar a entrar. */
export function atrasoDoIrmao(indice: number, c: Cadencia): number {
  return Math.max(0, Math.floor(indice)) * c.stagger;
}

/** A janela de cada um dos `quantidade` irmaos, escalonada. */
export function janelasDeIrmaos(
  quantidade: number,
  base: Janela,
  c: Cadencia,
): Janela[] {
  return Array.from({length: Math.max(0, Math.floor(quantidade))}, (_, i) => ({
    inicio: base.inicio + atrasoDoIrmao(i, c),
    duracao: base.duracao,
  }));
}

/**
 * Quanto a cena precisa durar para o ULTIMO irmao completar a janela dele.
 *
 * O stagger empurra o fim junto com o comeco: se a cena nao crescer, o ultimo
 * elemento perde a saida e desaparece por corte.
 */
export function duracaoComIrmaos(
  quantidade: number,
  duracao: number,
  c: Cadencia,
): number {
  const n = Math.max(1, Math.floor(quantidade));
  return duracao + atrasoDoIrmao(n - 1, c);
}

/**
 * Quanto CADA irmao precisa durar para que todos fiquem cheios AO MESMO TEMPO
 * por `c.holdFinal` frames.
 *
 * O DEFEITO QUE ISTO CONSERTA, visto num still e nao num teste:
 *
 * Com a janela de `DURACAO_MINIMA` para todo mundo, o stagger empurra so o
 * comeco -- e a frase nunca aparece inteira. Medido no frame 30 de uma manchete
 * de 6 palavras: 'CAFE' ja estava em 0,81 de presenca, saindo, enquanto
 * 'CANASTRA' ainda nem tinha terminado de entrar. Nao existia UM frame com a
 * manchete legivel por completo.
 *
 * A conta: o ultimo irmao fica cheio em `atraso(n-1) + entrada`; o primeiro
 * comeca a sair em `duracao - saida`. Para o segundo vir depois do primeiro com
 * `holdFinal` de folga:
 *
 *     duracao - entrada >= atraso(n-1) + entrada + holdFinal
 *     duracao >= atraso(n-1) + DURACAO_MINIMA
 *
 * Ou seja: a janela de cada irmao cresce exatamente o tanto que o stagger
 * atrasa o ultimo. Nenhum numero novo -- so os tokens.
 */
export function duracaoDeIrmao(quantidade: number, c: Cadencia): number {
  const n = Math.max(1, Math.floor(quantidade));
  return c.duracaoMinima + atrasoDoIrmao(n - 1, c);
}

// ---------------------------------------------------------------------------
// push de camera

/**
 * `PUSH.de` -> `PUSH.para` ao longo de `duracaoCena`, linear.
 *
 * Linear de proposito: `proibicoes.md` pede "push de camera lento, nunca
 * impacto", e qualquer easing aqui concentra a velocidade em algum trecho, que
 * e justamente o impacto.
 */
export function push(frame: number, duracaoCena: number): number {
  if (duracaoCena <= 0) return PUSH.de;
  const p = Math.min(1, Math.max(0, frame / duracaoCena));
  return PUSH.de + (PUSH.para - PUSH.de) * p;
}
