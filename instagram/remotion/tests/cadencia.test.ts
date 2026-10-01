import {describe, expect, it} from 'vitest';
import {cadencia, TEMPO_S} from '../src/motor/cadencia';

describe('cadencia', () => {
  it('a 30 fps reproduz EXATAMENTE a tabela que estava chumbada em tokens.ts', () => {
    // Os valores de antes de 01/10/2026, lidos de src/identidade/tokens.ts:16-23:
    //   entrada 12 · stagger 3 · holdFinal 12  -> DURACAO_MINIMA = 36
    // Se este teste falhar, a migracao para segundos MUDOU a peca a 30 fps, e o
    // pixel vai mudar junto.
    const c = cadencia(30);
    expect(c.entrada).toBe(12);
    expect(c.stagger).toBe(3);
    expect(c.holdFinal).toBe(12);
    expect(c.duracaoMinima).toBe(36);
    expect(c.fps).toBe(30);
  });

  it('duracaoMinima e SEMPRE entrada + holdFinal + entrada, em todo fps', () => {
    // E a espinha do portao de ritmo: 1,2 s de piso por elemento. Derivada, nao
    // escolhida -- se ela deixar de ser a soma, o portao passa a medir outra coisa.
    for (const fps of [24, 25, 30, 50, 60]) {
      const c = cadencia(fps);
      expect(c.duracaoMinima).toBe(c.entrada + c.holdFinal + c.entrada);
    }
  });

  it('a 60 fps os frames dobram e a DURACAO EM SEGUNDOS nao muda', () => {
    const c = cadencia(60);
    expect(c.entrada).toBe(24);
    expect(c.stagger).toBe(6);
    expect(c.holdFinal).toBe(24);
    expect(c.duracaoMinima).toBe(72);
    // 72 frames a 60 fps = 1,2 s = os 36 frames a 30 fps. E o ponto inteiro.
    expect(c.duracaoMinima / 60).toBeCloseTo(cadencia(30).duracaoMinima / 30, 9);
  });

  it('o que NAO e tempo nao escala: expoente de saida, overshoot e a curva', () => {
    const a = cadencia(30);
    const b = cadencia(60);
    expect(a.saidaExpoente).toBe(b.saidaExpoente);
    expect(a.overshoot).toBe(b.overshoot);
    expect(a.saidaExpoente).toBe(2.4);
    expect(a.overshoot).toBe(0.03);
  });

  it('TEMPO_S declara os tempos em SEGUNDOS, e os segundos batem com os frames medidos', () => {
    expect(TEMPO_S.entrada).toBeCloseTo(12 / 30, 9);
    expect(TEMPO_S.stagger).toBeCloseTo(3 / 30, 9);
    expect(TEMPO_S.holdFinal).toBeCloseTo(12 / 30, 9);
  });

  it('herda a recusa do relogio: fps fracionario nao passa', () => {
    expect(() => cadencia(29.97)).toThrow(/inteiro/);
  });
});
