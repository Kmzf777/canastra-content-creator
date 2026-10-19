// Peça 09 — o que cada cartão de vídeo toca, e quando. Fica fora do .tsx para o teste
// conseguir ler (lição de §7 da skill: .tsx que carrega fonte derruba o vitest).
//
// A v1 (15/10/2026) travava: onze takes ficavam na tela mais tempo do que duravam e
// congelavam no último quadro. Regra: cada take troca EXATAMENTE na palavra (nada de
// "6 quadros antes") e cobre a janela inteira com material, medido em clipes.json —
// tests/jeitinho-roteiro.test.ts reprova a escala que não cobre.

import clipesJson from '../../../projetos/09-jeitinho-cafe/clipes.json';
import {ABERTURA, CENA_INICIO, em, S1, S3, S5, S7} from './roteiro';

export const CLIPES = clipesJson as Record<string, {duracao: number; largura: number; altura: number; razao: number}>;

/** Um take: começa no segundo `desde` (relógio da peça), a partir do segundo `de` do clipe, na velocidade `vel`. */
export type Tomada = {src: string; desde: number; de?: number; vel?: number};
export type Escala = {ini: number; fim: number; tomadas: Tomada[]};

const cena = (i: number) => ({ini: CENA_INICIO[i], fim: CENA_INICIO[i + 1]});
/** O cartão entra 5 quadros depois da cabeça do criador. */
const ENTRA = 5 / 30;

export const ESCALAS: Record<string, Escala> = {
  // gancho: o ralado (f2) e, no "e esse nem é…", a água caindo (primeira metade do f3; a
  // segunda metade é o "água" da cena do Fábio, e o "rala" de lá é o f0, outro trecho)
  j1c: {...cena(1), tomadas: [{src: 'f2', desde: ABERTURA}, {src: 'f3', desde: em(S1.dentro, 'e')}]},
  j3c: {ini: CENA_INICIO[3] + ENTRA, fim: CENA_INICIO[4], tomadas: [
    {src: 'f1', desde: CENA_INICIO[3] + ENTRA}, {src: 'f0', desde: S3.rala.inicio, vel: 0.95}, {src: 'f3', desde: S3.agua.inicio, de: 2.6}]},
  j4c: {...cena(4), tomadas: [{src: 'f4', desde: CENA_INICIO[4], vel: 0.8}]},
  j6c: {ini: CENA_INICIO[6] + ENTRA, fim: CENA_INICIO[7], tomadas: [
    {src: 'p1', desde: CENA_INICIO[6] + ENTRA, vel: 0.95}, {src: 'p2', desde: S5.pacoquita2.inicio, vel: 0.9}]},
  j7c: {...cena(7), tomadas: [
    {src: 'p3', desde: CENA_INICIO[7], vel: 0.7}, {src: 'p3b', desde: S5.creme.inicio}, {src: 'p4', desde: em(S5.creme, 'virar')},
    {src: 'p5', desde: S5.joga.inicio}]},
  j8c: {...cena(8), tomadas: [{src: 'p7', desde: CENA_INICIO[8], vel: 0.64}]},
  j10c: {ini: CENA_INICIO[10] + 4 / 30, fim: CENA_INICIO[11], tomadas: [
    {src: 'gi0', desde: CENA_INICIO[10] + 4 / 30}, {src: 'gi1', desde: S7.creme.inicio}, {src: 'gi2', desde: S7.bate.inicio},
    {src: 'gi3', desde: S7.joga.inicio}, {src: 'gi4', desde: S7.um.inicio}, {src: 'gi5', desde: S7.liga.inicio}]},
  j11c: {...cena(11), tomadas: [{src: 'gi6', desde: CENA_INICIO[11]}, {src: 'gi7', desde: S7.que.inicio}]},
};

/** Quanto tempo (s) de clipe cada take precisa para cobrir a sua janela. */
export function necessidade(e: Escala): Array<{src: string; precisa: number; tem: number}> {
  return e.tomadas.map((t, k) => {
    const fimJanela = e.tomadas[k + 1]?.desde ?? e.fim;
    return {src: t.src, precisa: (t.de ?? 0) + (fimJanela - t.desde) * (t.vel ?? 1), tem: CLIPES[t.src].duracao};
  });
}
