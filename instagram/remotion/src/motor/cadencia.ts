// A CADENCIA: a tabela de tempos da marca, em FRAMES, para um fps.
//
// E o unico lugar do motor que converte os tokens de tempo. Quem precisa de
// tempo recebe uma `Cadencia` pronta e nunca chama `emFrames` por conta propria
// -- assim existe um ponto so para conferir, e `cadencia(30)` e um teste de
// nao-regressao do motor inteiro.
//
// O PARAMETRO E OBRIGATORIO, E ISSO E DE PROPOSITO.
//
// Poderia ter default `cadencia(30)`. Nao tem, porque um default aqui devolveria
// exatamente o bug que esta tarefa conserta: uma camada que esquecesse de passar
// a cadencia da composicao continuaria desenhando no tempo de 30 fps, com exit 0.
// Sendo obrigatorio, `npm run tsc` enumera todo ponto de chamada que ficou para
// tras. O compilador e o portao.

import {TEMPO} from '../identidade/tokens';
import {emFrames} from './relogio';

export type Cadencia = {
  /** o fps de que esta tabela saiu */
  fps: number;
  /** frames de entrada de um elemento */
  entrada: number;
  /** frames entre elementos irmaos */
  stagger: number;
  /** frames em que o elemento fica cheio depois de o ultimo irmao entrar */
  holdFinal: number;
  /** entrada + holdFinal + entrada. Abaixo disso as pontas comprimem. */
  duracaoMinima: number;
  /** adimensional: nao escala com fps */
  saidaExpoente: number;
  /** adimensional: nao escala com fps */
  overshoot: number;
};

/** Os tempos da marca em segundos, expostos para quem precisa da unidade crua. */
export const TEMPO_S = {
  entrada: TEMPO.entradaS,
  stagger: TEMPO.staggerS,
  holdFinal: TEMPO.holdFinalS,
} as const;

export function cadencia(fps: number): Cadencia {
  const entrada = emFrames(TEMPO.entradaS, fps);
  const stagger = emFrames(TEMPO.staggerS, fps);
  const holdFinal = emFrames(TEMPO.holdFinalS, fps);
  return {
    fps,
    entrada,
    stagger,
    holdFinal,
    duracaoMinima: entrada + holdFinal + entrada,
    saidaExpoente: TEMPO.saidaExpoente,
    overshoot: TEMPO.overshoot,
  };
}
