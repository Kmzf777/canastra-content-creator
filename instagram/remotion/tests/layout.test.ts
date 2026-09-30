import {describe, it, expect} from 'vitest';
import {layout} from '../src/motor/layout';

describe('layout', () => {
  it('no 9:16 o video ocupa a largura inteira', () => {
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 9 / 16});
    expect(z.video.largura).toBe(1080);
    expect(z.video.x).toBe(0);
  });

  it('no 1:1 o video NAO e cortado na largura', () => {
    const z = layout({largura: 1080, altura: 1080, razaoFonte: 9 / 16});
    // a fonte e mais alta que larga: cabe pela altura, sobra nas laterais
    expect(z.video.altura).toBeLessThanOrEqual(1080);
    expect(z.video.largura).toBeLessThanOrEqual(1080);
    expect(z.video.largura / z.video.altura).toBeCloseTo(9 / 16, 3);
  });

  it('a legenda fica dentro da area segura em qualquer formato', () => {
    for (const [w, h] of [[1080, 1920], [1080, 1080], [1920, 1080]]) {
      const z = layout({largura: w, altura: h, razaoFonte: 9 / 16});
      expect(z.legenda.x).toBeGreaterThanOrEqual(z.seguro.x);
      expect(z.legenda.x + z.legenda.largura)
        .toBeLessThanOrEqual(z.seguro.x + z.seguro.largura);
      expect(z.legenda.y + z.legenda.altura)
        .toBeLessThanOrEqual(z.seguro.y + z.seguro.altura);
    }
  });

  it('as zonas de video e de manchete nao se sobrepoem no 1:1', () => {
    const z = layout({largura: 1080, altura: 1080, razaoFonte: 9 / 16});
    const fimVideo = z.video.x + z.video.largura;
    const cruza = z.manchete.x < fimVideo && z.manchete.x + z.manchete.largura > z.video.x;
    expect(cruza).toBe(false);
  });
});
