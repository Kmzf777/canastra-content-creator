import {describe, expect, it} from 'vitest';
import {cameraEm, deriva, desfoqueDoPlano, transformarPlano, tremor, velocidade} from '../src/colagem/camera';
import {blocoNoInstante, blocosA, Roteiro, type Palavra} from '../src/colagem/legenda';
import {carimbo, esmagar, posterizar} from '../src/colagem/movimento-colagem';

describe('camera', () => {
  const chaves = [
    {q: 0, x: 0, y: 0, zoom: 1, rot: 0},
    {q: 30, x: 100, y: -50, zoom: 1.2, rot: 2},
  ];
  it('interpola entre chaves e segura nas pontas', () => {
    expect(cameraEm(-5, chaves).x).toBe(0);
    expect(cameraEm(30, chaves).zoom).toBeCloseTo(1.2);
    expect(cameraEm(99, chaves).x).toBe(100);
    const meio = cameraEm(15, chaves);
    expect(meio.x).toBeGreaterThan(0);
    expect(meio.x).toBeLessThan(100);
  });

  it('plano de profundidade 0 não anda; plano 2 anda o dobro', () => {
    const cam = {x: 40, y: 10, zoom: 1.1, rot: 0};
    expect(transformarPlano(cam, 0).escala).toBeCloseTo(1);
    expect(transformarPlano(cam, 0).transform).toContain('translate(0.00px, 0.00px)');
    expect(transformarPlano(cam, 2).transform).toContain('translate(-80.00px, -20.00px)');
    expect(transformarPlano(cam, 2).escala).toBeCloseTo(1.2);
  });

  it('primeiro plano desfoca, plano da cena fica nítido', () => {
    expect(desfoqueDoPlano(1)).toBe(0);
    expect(desfoqueDoPlano(2.5)).toBeGreaterThanOrEqual(10);
  });

  it('a deriva nunca deixa a câmera parada', () => {
    for (let q = 1; q < 600; q++) {
      expect(velocidade(deriva(q - 1, 'c'), deriva(q, 'c'))).toBeGreaterThan(0);
    }
  });

  it('tremor só existe na janela do impacto', () => {
    expect(tremor(9, 10).x).toBe(0);
    expect(Math.abs(tremor(10, 10).x) + Math.abs(tremor(10, 10).y)).toBeGreaterThan(0);
    expect(tremor(13, 10).x).toBe(0);
  });
});

describe('movimento de colagem', () => {
  it('posteriza em passos de 3 quadros', () => {
    expect(posterizar(10, 3)).toBe(9);
    expect(posterizar(11, 3)).toBe(9);
    expect(posterizar(12, 3)).toBe(12);
  });
  it('carimbo ultrapassa no máximo 12% e assenta em 1', () => {
    expect(carimbo(9, 10).visivel).toBe(false);
    expect(carimbo(10, 10).escala).toBeLessThanOrEqual(1.12);
    expect(carimbo(14, 10).escala).toBe(1);
  });
  it('squash chega largo e achatado e assenta', () => {
    const e = esmagar(20, 20);
    expect(e.sx).toBeGreaterThan(1);
    expect(e.sy).toBeLessThan(1);
    expect(esmagar(24, 20).sx).toBeCloseTo(1);
  });
});

const P = (txt: string, t0 = 0, passo = 0.3): Palavra[] =>
  txt.split(' ').map((w, i) => ({i, texto: w, inicio: t0 + i * passo, fim: t0 + i * passo + passo * 0.85}));

describe('legenda A/B', () => {
  it('nenhuma palavra vai para A e B ao mesmo tempo', () => {
    const ps = P('Calma! Não precisa largar o café. Mas até o fim desse vídeo você vai saber se o seu é especial.');
    const r = new Roteiro(ps);
    r.b('Calma!');
    r.b('se o seu é especial.');
    const a = blocosA(ps, r.emB, r.mudas);
    const emA = new Set(a.flatMap((b) => b.palavras));
    for (const i of r.emB) expect(emA.has(i)).toBe(false);
  });

  it('pílula tem no máximo 5 palavras/20 caracteres e quebra na pontuação', () => {
    const ps = P('Não precisa largar o café. Mas até o fim');
    const a = blocosA(ps, new Set());
    for (const b of a) { expect(b.palavras.length).toBeLessThanOrEqual(5); expect(b.texto.length).toBeLessThanOrEqual(20); }
    expect(a.some((b) => b.texto.endsWith('CAFÉ.'))).toBe(true);
  });

  it('a pílula some no instante em que um B entra', () => {
    const ps = P('E tá tudo dentro da lei.');
    const r = new Roteiro(ps);
    const lei = r.b('dentro da lei.');
    const a = blocosA(ps, r.emB, r.mudas);
    expect(blocoNoInstante(a, lei.inicio + 0.01)).toBeNull();
  });

  it('procura em ordem: a segunda ocorrência exige cursor adiante', () => {
    const ps = P('especial não é especial');
    const r = new Roteiro(ps);
    expect(r.b('especial').de).toBe(0);
    expect(r.b('especial').de).toBe(3);
    expect(() => r.b('especial')).toThrow();
  });

  it('não fecha bloco em palavra fraca quando dá para evitar', () => {
    const ps = P('Por isso a gente só torra o que a gente mesmo');
    const a = blocosA(ps, new Set());
    const fracas = ['A', 'O', 'QUE', 'DE', 'PRA'];
    for (const b of a.slice(0, -1)) expect(fracas).not.toContain(b.texto.split(' ').pop());
  });

  it('mudo não aparece em lugar nenhum', () => {
    const ps = P('A primeira é no grão cru.');
    const r = new Roteiro(ps);
    r.mudo('A primeira é no');
    r.b('grão cru.');
    expect(blocosA(ps, r.emB, r.mudas)).toHaveLength(0);
  });
});
