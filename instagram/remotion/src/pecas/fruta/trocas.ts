// Peça 08 — quais trocas de cena são chicote (o resto é corte seco). Mora fora de
// Fruta.tsx para o som ler sem ciclo de import.

import {CENA_INICIO} from './roteiro';

export const LIMITES = CENA_INICIO.map((s) => Math.round(s * 30));
/** Cenas que entram por chicote: as trocas grandes, vídeo <-> colagem. Eixo alterna. */
const COM_CHICOTE = [2, 3, 4, 6, 7, 8, 13, 14, 15, 16, 20, 22, 23, 24, 25];
export const CHICOTES = COM_CHICOTE.map((n, k) => ({q: LIMITES[n], eixo: (k % 2 ? 'y' : 'x') as 'x' | 'y', dir: (k % 3 ? -1 : 1) as 1 | -1}));
