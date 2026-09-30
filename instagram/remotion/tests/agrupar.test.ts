import {describe, it, expect} from 'vitest';
import {agrupar} from '../src/legenda/agrupar';

const palavras = [
  {texto: 'Aqui',    inicioMs: 1140, fimMs: 1380},
  {texto: 'na',      inicioMs: 1380, fimMs: 1460},
  {texto: 'Canastra',inicioMs: 1460, fimMs: 1980},
  {texto: 'a',       inicioMs: 1980, fimMs: 2040},
  {texto: 'gente',   inicioMs: 2040, fimMs: 2300},
];

describe('agrupar', () => {
  it('nunca passa de 2 palavras por bloco', () => {
    for (const b of agrupar(palavras, {fps: 30})) {
      expect(b.texto.split(' ').length).toBeLessThanOrEqual(2);
    }
  });

  it('nenhum bloco dura menos que o minimo de 10 frames', () => {
    for (const b of agrupar(palavras, {fps: 30})) {
      expect(b.fimFrame - b.inicioFrame).toBeGreaterThanOrEqual(10);
    }
  });

  it('blocos nao se sobrepoem e estao em ordem', () => {
    const bs = agrupar(palavras, {fps: 30});
    for (let i = 1; i < bs.length; i++) {
      expect(bs[i].inicioFrame).toBeGreaterThanOrEqual(bs[i - 1].fimFrame);
    }
  });

  it('preserva todas as palavras, na ordem', () => {
    const junto = agrupar(palavras, {fps: 30}).map(b => b.texto).join(' ');
    expect(junto).toBe(palavras.map(p => p.texto).join(' '));
  });
});
