import {describe, expect, it} from 'vitest';
import {BLOCOS_A, CENA_INICIO, EM_B, FIM, MUDAS, PALAVRAS} from '../src/pecas/especial/roteiro';

describe('peça 07 — roteiro e legendas', () => {
  it('nenhuma palavra em A e B ao mesmo tempo', () => {
    const emA = new Set(BLOCOS_A.flatMap((b) => b.palavras));
    for (const i of EM_B) expect(emA.has(i)).toBe(false);
    for (const i of MUDAS) expect(emA.has(i)).toBe(false);
  });

  it('toda palavra falada aparece em A, em B, ou foi silenciada de propósito', () => {
    const emA = new Set(BLOCOS_A.flatMap((b) => b.palavras));
    const soltas = PALAVRAS.filter((p) => !emA.has(p.i) && !EM_B.has(p.i) && !MUDAS.has(p.i));
    expect(soltas.map((p) => p.texto)).toEqual([]);
  });

  it('pílula: até 4 palavras e 18 caracteres, ao menos 0,2 s, sem se sobrepor', () => {
    for (let k = 0; k < BLOCOS_A.length; k++) {
      const b = BLOCOS_A[k];
      expect(b.palavras.length).toBeGreaterThanOrEqual(1);
      expect(b.palavras.length).toBeLessThanOrEqual(4);
      expect(b.texto.length).toBeLessThanOrEqual(18);
      // 0,2 s = 6 quadros: "PEGA" espremido entre a fala e a colagem que entra
      expect(b.fim - b.inicio).toBeGreaterThanOrEqual(0.2);
      if (k > 0) expect(b.inicio).toBeGreaterThanOrEqual(BLOCOS_A[k - 1].fim - 1e-9);
    }
  });

  it('as cenas começam em ordem e dentro da narração', () => {
    for (let k = 1; k < CENA_INICIO.length; k++) expect(CENA_INICIO[k]).toBeGreaterThan(CENA_INICIO[k - 1]);
    expect(CENA_INICIO[CENA_INICIO.length - 1]).toBeLessThan(FIM);
    // a 07 foi entregue com 79,0 s: o FIM derivado tem que reproduzir isso
    expect(FIM).toBe(79);
  });

  it('imprime a pílula para revisão', () => {
    console.log(BLOCOS_A.map((b) => `${b.inicio.toFixed(2)}-${b.fim.toFixed(2)} ${b.texto}`).join('\n'));
  });
});
