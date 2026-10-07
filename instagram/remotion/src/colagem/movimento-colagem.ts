// A gramatica de movimento da colagem, em funcoes puras de quadro.
//
// Fica num .ts e nao num .tsx pela razao mecanica da skill canastra-video §7:
// arquivo que importa `identidade/tipografia.ts` derruba o vitest.
//
// Tres gestos, e so tres:
//   assentar -- a peca chega um pouco grande e girada, e pousa sem quicar
//   boil     -- depois de colada, ela "respira" em passo de stop-motion
//   carimbar -- o veredito bate grande e assenta em 3 quadros
//
// Nada de elastico (proibicoes.md). O unico overshoot permitido e o de
// `TEMPO.overshoot` (3%), e assentar nem chega a usa-lo: o pouso e amortecido.

import {sorteio, semente} from './semente';

export const ASSENTAR_QUADROS = 6;
export const BOIL_PASSO = 3;
export const CARIMBO_QUADROS = 3;

/** ease-out cubico: rapido no comeco, pousa devagar. */
export const saida = (t: number) => 1 - Math.pow(1 - Math.min(1, Math.max(0, t)), 3);

export type Pose = {visivel: boolean; escala: number; rot: number; dy: number; opacidade: number};

const INVISIVEL: Pose = {visivel: false, escala: 1, rot: 0, dy: 0, opacidade: 0};

/**
 * Pose de uma peca que comeca a ser colada no quadro `inicio`.
 * A rotacao de chegada (2..4 graus, sinal da semente) cai para a rotacao de
 * repouso (|r| <= 0,6) em ASSENTAR_QUADROS.
 */
export function assentar(q: number, inicio: number, chave: string): Pose {
  if (q < inicio) return INVISIVEL;
  const s = semente(chave);
  const sinal = s() < 0.5 ? -1 : 1;
  const rotChegada = sinal * (2 + s() * 2);
  const rotRepouso = (s() - 0.5) * 1.2;
  const t = saida((q - inicio) / ASSENTAR_QUADROS);
  return {
    visivel: true,
    escala: 1.04 + (1 - 1.04) * t,
    rot: rotChegada + (rotRepouso - rotChegada) * t,
    dy: -24 * (1 - t),
    opacidade: Math.min(1, (q - inicio + 1) / 2),
  };
}

/**
 * Respiracao de stop-motion: troca de estado so a cada BOIL_PASSO quadros
 * (10 "desenhos" por segundo a 30 fps). `variante` escolhe uma das tres bordas
 * irregulares pre-renderizadas; `rot` e um tremor de no maximo 0,6 grau.
 */
export function boil(q: number, chave: string): {variante: 0 | 1 | 2; rot: number} {
  const passo = Math.floor(q / BOIL_PASSO);
  const v = Math.floor(sorteio(`${chave}#v${passo}`, 0, 3)) as 0 | 1 | 2;
  return {variante: v, rot: sorteio(`${chave}#r${passo}`, -0.6, 0.6)};
}

/** Carimbo: 1,15 no impacto, 1,00 em CARIMBO_QUADROS. */
export function carimbar(q: number, inicio: number): {visivel: boolean; escala: number} {
  if (q < inicio) return {visivel: false, escala: 1};
  const t = saida((q - inicio) / CARIMBO_QUADROS);
  return {visivel: true, escala: 1.15 + (1 - 1.15) * t};
}

/** Progresso 0..1 entre dois quadros, com ease-out. */
export function progresso(q: number, de: number, ate: number): number {
  if (ate <= de) return q >= ate ? 1 : 0;
  return saida((q - de) / (ate - de));
}
