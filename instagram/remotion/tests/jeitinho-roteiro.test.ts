import {describe, expect, it} from 'vitest';
import {BLOCOS_A, CENA_INICIO, EM_B, FIM, MUDAS, PALAVRAS} from '../src/pecas/jeitinho/roteiro';
import {ESCALAS, necessidade} from '../src/pecas/jeitinho/tomadas';

describe('peça 09 — roteiro, legendas e takes', () => {
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
      expect(b.palavras.length).toBeLessThanOrEqual(4);
      expect(b.texto.length).toBeLessThanOrEqual(18);
      expect(b.fim - b.inicio).toBeGreaterThanOrEqual(0.2);
      if (k > 0) expect(b.inicio).toBeGreaterThanOrEqual(BLOCOS_A[k - 1].fim - 1e-9);
    }
  });

  it('nenhum take congela: o clipe cobre a janela inteira do cartão', () => {
    const faltas: string[] = [];
    for (const [cartao, e] of Object.entries(ESCALAS)) {
      for (const n of necessidade(e)) if (n.precisa > n.tem - 0.03) faltas.push(`${cartao}/${n.src}: precisa ${n.precisa.toFixed(2)} s, tem ${n.tem.toFixed(2)} s`);
    }
    expect(faltas).toEqual([]);
  });

  it('nenhum take repete trecho de outro cartão', () => {
    const usos = Object.values(ESCALAS).flatMap((e) => necessidade(e).map((n, k) => ({src: n.src, de: e.tomadas[k].de ?? 0, ate: n.precisa})));
    for (let a = 0; a < usos.length; a++) for (let b = a + 1; b < usos.length; b++) {
      if (usos[a].src !== usos[b].src) continue;
      const sobre = Math.min(usos[a].ate, usos[b].ate) - Math.max(usos[a].de, usos[b].de);
      expect(sobre, `${usos[a].src} usado duas vezes no mesmo trecho`).toBeLessThanOrEqual(0.05);
    }
  });

  it('as cenas começam em ordem e dentro da narração', () => {
    for (let k = 1; k < CENA_INICIO.length; k++) expect(CENA_INICIO[k]).toBeGreaterThan(CENA_INICIO[k - 1]);
    expect(CENA_INICIO[CENA_INICIO.length - 1]).toBeLessThan(FIM);
  });

  it('imprime a pílula e os takes para revisão', () => {
    console.log(BLOCOS_A.map((b) => `${b.inicio.toFixed(2)}-${b.fim.toFixed(2)} ${b.texto}`).join('\n'));
    for (const [c, e] of Object.entries(ESCALAS)) console.log(c, necessidade(e).map((n) => `${n.src} ${n.precisa.toFixed(2)}/${n.tem.toFixed(2)}`).join(' · '));
  });
});
