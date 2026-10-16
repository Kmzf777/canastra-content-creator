// Peça 08b — quais trocas são chicote (o resto é corte seco: a rajada pedra/graveto/leve).
import {CENA_INICIO} from './roteiro';

export const LIMITES = CENA_INICIO.map((s) => Math.round(s * 30));
const COM_CHICOTE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22];
export const CHICOTES = COM_CHICOTE.map((n, k) => ({q: LIMITES[n], eixo: (k % 2 ? 'y' : 'x') as 'x' | 'y', dir: (k % 3 ? -1 : 1) as 1 | -1}));
