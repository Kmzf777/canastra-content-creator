import {describe, expect, it} from 'vitest';
import {emFrames, emSegundos} from '../src/motor/relogio';

describe('emFrames', () => {
  it('reproduz EXATAMENTE os tokens medidos a 30 fps', () => {
    // Os quatro numeros que hoje estao chumbados em frames em tokens.ts:
    //   TEMPO.entrada 12 · TEMPO.stagger 3 · TEMPO.holdFinal 12
    //   LEGENDA.duracaoMinFrames 10
    // Este teste e a prova de que declarar em SEGUNDOS nao muda a peca a 30 fps.
    expect(emFrames(0.4, 30)).toBe(12);
    expect(emFrames(0.1, 30)).toBe(3);
    expect(emFrames(0.333, 30)).toBe(10);
  });

  it('a 60 fps dobra, a 24 fps encurta -- e e por isso que a funcao existe', () => {
    expect(emFrames(0.4, 60)).toBe(24);
    expect(emFrames(0.1, 60)).toBe(6);
    expect(emFrames(0.4, 24)).toBe(10);
    // 0,1 s a 24 fps da 2,4 -> 2 frames, que continua dentro da faixa util de
    // stagger (2 a 4 frames) que tokens.ts registra.
    expect(emFrames(0.1, 24)).toBe(2);
  });

  it('arredonda, nao trunca: 2,5 frames vira 3 e nao 2', () => {
    // Truncar acumularia erro sempre para baixo e uma peca de 12 cenas sairia
    // mais curta que o briefing -- o defeito que o pedido do Rafael nomeia.
    expect(emFrames(1 / 12, 30)).toBe(3); // 2,5 -> 3
  });

  it('recusa fps que nao seja inteiro positivo, em vez de devolver NaN', () => {
    expect(() => emFrames(1, 0)).toThrow(/fps/);
    expect(() => emFrames(1, -30)).toThrow(/fps/);
    expect(() => emFrames(1, 29.97)).toThrow(/inteiro/);
  });

  it('recusa segundo negativo', () => {
    expect(() => emFrames(-0.1, 30)).toThrow(/negativo/);
  });

  it('emSegundos e a volta, e a ida e volta a 30 fps nao perde os tokens', () => {
    expect(emSegundos(12, 30)).toBeCloseTo(0.4, 9);
    expect(emFrames(emSegundos(12, 30), 30)).toBe(12);
    expect(emFrames(emSegundos(3, 30), 30)).toBe(3);
  });
});
