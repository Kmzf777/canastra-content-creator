// Os tempos da peca 06, MEDIDOS na narracao da ElevenLabs v4.
//
// Origem: silencios por RMS (-40 dB, >= 0,15 s) sobre o proprio mp3 e
// whisper.cpp `small` com tempo por palavra, em 07/10/2026. O inicio de cada
// frase e o FIM do silencio que a precede -- o fim de palavra do whisper estica.
// Dois tempos sao estimados, nao medidos, e estao marcados: `oitenta` e `desde`
// (as frases colam sem silencio entre elas).
//
// Tudo em SEGUNDOS; a conversao e `f()`, uma vez.

import {emFrames} from '../motor/relogio';

export const FPS = 30;
export const DURACAO_S = 50.23;
export const DURACAO_Q = Math.round(DURACAO_S * FPS);

export const T = {
  voceSabia: 0.0,
  especialFim: 3.8,
  poisE: 4.18,
  praGanhar: 4.92,
  duasProvas: 6.24,
  duas: 7.5,
  primeiro: 8.36,
  amostra: 10.02,
  gramasFim: 12.42,
  defeito: 12.66,
  nenhum: 14.28,
  depois: 15.12,
  xicara: 15.9,
  aroma: 16.78,
  docura: 17.48,
  acidez: 18.32,
  corpo: 19.24,
  nota: 20.1,
  oitenta: 22.2, // ESTIMADO
  pontosFim: 23.14,
  porIsso: 23.48,
  comeca: 24.12,
  metros: 27.24,
  altimetroFim: 28.5,
  fruto: 30.68,
  devagarFim: 32.4,
  acucar: 33.3,
  aGente: 34.46,
  planta: 36.5,
  colhe: 37.3,
  seleciona: 38.72,
  semInter: 39.96,
  semMistura: 41.18,
  desde: 42.0, // ESTIMADO
  geracoes: 43.54,
  cafeCanastra: 45.88,
  slogan: 47.14,
  falaFim: 49.04,
  fim: DURACAO_S,
} as const;

/** Segundos -> quadro, no fps da peca. */
export const f = (s: number) => emFrames(s, FPS);
