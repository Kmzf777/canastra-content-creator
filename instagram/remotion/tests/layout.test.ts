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

  it('as margens sao a MESMA porcentagem do eixo proprio em todo formato', () => {
    // O DEFEITO: um `k` unico derivado da LARGURA escalava tambem as margens
    // verticais. Medido antes do conserto, base efetiva como % da ALTURA:
    //   1080x1920 -> 16,15%   1080x1080 -> 28,70%   1920x1080 -> 51,03%
    // No 16:9 metade do quadro era margem e a area segura ficava com 368,9 px
    // de altura -- exatamente o numero que `texto-forma.ts` registra como
    // "texto de borda a borda".
    for (const [w, h] of [[1080, 1920], [1080, 1080], [1920, 1080]]) {
      const z = layout({largura: w, altura: h, razaoFonte: 9 / 16});
      const base = h - (z.seguro.y + z.seguro.altura);
      expect(z.seguro.y / h).toBeCloseTo(0.05, 6);
      expect(base / h).toBeCloseTo(0.16, 6);
      expect(z.seguro.x / w).toBeCloseTo(160 / 1080, 6);
    }
  });

  it('a margem de topo respeita o piso de 5% da convencao title-safe', () => {
    // Eram 90 px em 1920 = 4,69%, abaixo do piso da faixa 5-8%.
    for (const [w, h] of [[1080, 1920], [1080, 1080], [1920, 1080]]) {
      const z = layout({largura: w, altura: h, razaoFonte: 9 / 16});
      expect(z.seguro.y / h).toBeGreaterThanOrEqual(0.05 - 1e-9);
    }
  });

  it('legenda e manchete NAO se intersectam, nos quatro formatos e nos dois eixos', () => {
    // O PAR QUE CONVERTE O PARAGRAFO EM INVARIANTE. Medido ANTES do conserto, a
    // intersecao em x era 90,20 px no 1:1, 102,35 no 4:5 e 122,56 no 16:9 (no 9:16,
    // zero). Depois do conserto, 0,00 nos quatro. Medir UM eixo da um numero
    // plausivel e errado -- foi o que produziu os "353,20 px" e a leitura de "100%
    // da caixa" que dois revisores diferentes escreveram.
    for (const rf of [0.5625, 4 / 3]) {
      for (const [w, h] of [[1080, 1920], [1080, 1080], [1080, 1350], [1920, 1080]]) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        const x = Math.max(z.legenda.x, z.manchete.x);
        const direita = Math.min(
          z.legenda.x + z.legenda.largura,
          z.manchete.x + z.manchete.largura,
        );
        const y = Math.max(z.legenda.y, z.manchete.y);
        const baixo = Math.min(
          z.legenda.y + z.legenda.altura,
          z.manchete.y + z.manchete.altura,
        );
        const area = Math.max(0, direita - x) * Math.max(0, baixo - y);
        expect(area, `${w}x${h} rf ${rf}`).toBeCloseTo(0, 6);
      }
    }
  });

  it('a caixa de legenda NUNCA vaza a borda direita do video', () => {
    // A CAUSA MECANICA, e ela e uma linha. `layout.ts` calculava a LARGURA
    // supondo x = video.x + 16k (e o que o -32k significa: 16 de respiro de cada
    // lado) e USAVA x = seguro.x. Com o video em coluna, video.x = 0 e
    // seguro.x = 160: a caixa desliza 144,00 px para a direita levando a largura
    // inteira e vaza o video em 128,00 px no 1:1, 128,00 no 4:5 e 227,56 no 16:9.
    for (const rf of [0.5625, 4 / 3]) {
      for (const [w, h] of [[1080, 1920], [1080, 1080], [1080, 1350], [1920, 1080]]) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        const vazamento =
          z.legenda.x + z.legenda.largura - (z.video.x + z.video.largura);
        expect(vazamento, `${w}x${h} rf ${rf}`).toBeLessThanOrEqual(1e-6);
      }
    }
  });

  it('as zonas de video e de manchete nao se sobrepoem no 1:1', () => {
    const z = layout({largura: 1080, altura: 1080, razaoFonte: 9 / 16});
    const fimVideo = z.video.x + z.video.largura;
    const cruza = z.manchete.x < fimVideo && z.manchete.x + z.manchete.largura > z.video.x;
    expect(cruza).toBe(false);
  });
});
