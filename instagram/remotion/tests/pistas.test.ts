// A GEOMETRIA DE PISTA, nos quatro formatos e nas duas razoes de fonte do acervo.
//
// As duas razoes nao sao exemplos: 0,5625 e a razao de exibicao do `pl.mp4` (576x1024,
// displaymatrix -90) e 4/3 e a das 18 fotos de fazenda com `Orientation 1`
// (4032x3024). Sao as duas populacoes que o motor tem para servir.
import {describe, expect, it} from 'vitest';
import {layout, MARGEM} from '../src/motor/layout';
import {
  caixaDaPista,
  colunaDeTexto,
  encaixe,
  FRACAO_DE_PISTA,
  LIMIAR_DE_COLUNA,
  modoDoEncaixe,
  PISTAS,
  pistas,
  seguroDoVideo,
} from '../src/motor/pista';

const FORMATOS: Array<[number, number, string]> = [
  [1080, 1920, '9:16'],
  [1080, 1080, '1:1'],
  [1080, 1350, '4:5'],
  [1920, 1080, '16:9'],
];
const RAZOES = [0.5625, 4 / 3];

function area(a: {x: number; y: number; largura: number; altura: number},
             b: {x: number; y: number; largura: number; altura: number}): number {
  const x = Math.max(a.x, b.x);
  const y = Math.max(a.y, b.y);
  const direita = Math.min(a.x + a.largura, b.x + b.largura);
  const baixo = Math.min(a.y + a.altura, b.y + b.altura);
  return Math.max(0, direita - x) * Math.max(0, baixo - y);
}

describe('layout: o 4:5 existe e o ramo e geometrico', () => {
  it('o 4:5 ganhou rotulo', () => {
    expect(layout({largura: 1080, altura: 1350, razaoFonte: 0.5625}).formato).toBe('4:5');
  });

  it('o ramo "preenche a largura" e escolhido por MEDIDA, nao por rotulo', () => {
    // Fonte 4:5 num quadro 4:5: a imagem preenche o quadro inteiro, embora o rotulo
    // nao seja '9:16'. Com o teste antigo (`formato === '9:16'`) isto caia no ramo
    // da coluna e sobrava terra ao lado de uma imagem que cabia exata.
    const z = layout({largura: 1080, altura: 1350, razaoFonte: 1080 / 1350});
    expect(z.video).toEqual({x: 0, y: 0, largura: 1080, altura: 1350});
  });

  it('MARGEM e exportada e esta em FRACAO, nao em pixel', () => {
    expect(MARGEM.topo).toBe(0.05);
    expect(MARGEM.base).toBe(0.16);
    expect(MARGEM.lado).toBeCloseTo(160 / 1080, 9);
  });
});

describe('coluna de texto', () => {
  it('no 9:16 a sobra e ZERO, logo a coluna e o seguro DA IMAGEM', () => {
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 0.5625});
    expect(1080 - z.video.largura).toBeCloseTo(0, 6);
    expect(colunaDeTexto(z)).toEqual(seguroDoVideo(z));
  });

  it('no 1:1 com fonte retrato a sobra passa do limiar, logo a coluna e a sobra', () => {
    const z = layout({largura: 1080, altura: 1080, razaoFonte: 0.5625});
    const sobra = 1080 - z.video.largura;
    expect(sobra).toBeCloseTo(472.5, 2);
    expect(sobra / 1080).toBeGreaterThan(LIMIAR_DE_COLUNA);
    expect(colunaDeTexto(z).x).toBeGreaterThan(z.video.largura - 1);
  });

  it('com fonte PAISAGEM a coluna cai no seguro da imagem nos tres verticais', () => {
    // E por isso que a peca de foto parada entrega `faixa`, nao `coluna`: a foto
    // 4032x3024 nao deixa sobra lateral em nenhum formato vertical.
    for (const [w, h, nome] of FORMATOS.slice(0, 3)) {
      const z = layout({largura: w, altura: h, razaoFonte: 4 / 3});
      expect(w - z.video.largura, nome).toBeCloseTo(0, 6);
      expect(colunaDeTexto(z), nome).toEqual(seguroDoVideo(z));
    }
  });

  it('a coluna nunca sai da area segura do quadro', () => {
    for (const rf of RAZOES) {
      for (const [w, h, nome] of FORMATOS) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        const c = colunaDeTexto(z);
        expect(c.x, `${nome} rf ${rf}`).toBeGreaterThanOrEqual(z.seguro.x - 1e-6);
        expect(c.y, `${nome} rf ${rf}`).toBeGreaterThanOrEqual(z.seguro.y - 1e-6);
        expect(c.x + c.largura, `${nome} rf ${rf}`).toBeLessThanOrEqual(
          z.seguro.x + z.seguro.largura + 1e-6,
        );
        expect(c.y + c.altura, `${nome} rf ${rf}`).toBeLessThanOrEqual(
          z.seguro.y + z.seguro.altura + 1e-6,
        );
      }
    }
  });
});

describe('as quatro pistas', () => {
  it('as quatro existem em todas as 8 combinacoes, e nenhuma e degenerada', () => {
    for (const rf of RAZOES) {
      for (const [w, h, nome] of FORMATOS) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        const ps = pistas(z);
        for (const p of PISTAS) {
          expect(ps[p].largura, `${nome} rf ${rf} ${p}`).toBeGreaterThan(1);
          expect(ps[p].altura, `${nome} rf ${rf} ${p}`).toBeGreaterThan(1);
        }
      }
    }
  });

  it('topo e principal nao se sobrepoem, e sobra a folga de baixo', () => {
    for (const rf of RAZOES) {
      for (const [w, h, nome] of FORMATOS) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        const ps = pistas(z);
        expect(area(ps.topo, ps.principal), `${nome} rf ${rf}`).toBeCloseTo(0, 6);
        const c = colunaDeTexto(z);
        const fim = ps.principal.y + ps.principal.altura;
        expect(c.y + c.altura - fim, `${nome} rf ${rf}`).toBeCloseTo(
          c.altura * FRACAO_DE_PISTA.folgaDeBaixo,
          6,
        );
      }
    }
  });

  it('as pistas de EVENTO nunca invadem o rodape -- nas 8 combinacoes', () => {
    // A INVARIANTE QUE PAGA A GEOMETRIA. Ela depende de TRES coisas, nao uma:
    // `MARGEM` em fracao, o conserto da largura da legenda, e `rodape` ser a caixa
    // REAL da camada Legenda (`z.legenda`) e nao uma caixa parecida com ela.
    for (const rf of RAZOES) {
      for (const [w, h, nome] of FORMATOS) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        const ps = pistas(z);
        expect(area(ps.topo, ps.rodape), `topo x rodape ${nome} rf ${rf}`).toBeCloseTo(0, 6);
        expect(
          area(ps.principal, ps.rodape),
          `principal x rodape ${nome} rf ${rf}`,
        ).toBeCloseTo(0, 6);
      }
    }
  });

  it('`rodape` E `z.legenda`, nao uma caixa parecida', () => {
    const z = layout({largura: 1080, altura: 1080, razaoFonte: 4 / 3});
    expect(pistas(z).rodape).toEqual(z.legenda);
    expect(pistas(z).tela).toEqual(z.seguro);
  });
});

describe('encaixe derivado', () => {
  it("pista 'tela' e SEMPRE cartela, em qualquer formato", () => {
    for (const rf of RAZOES) {
      for (const [w, h, nome] of FORMATOS) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        expect(encaixe('tela', z), `${nome} rf ${rf}`).toBe('cartela');
        expect(modoDoEncaixe('cartela')).toBe('cartela');
      }
    }
  });

  it('no 9:16 nao existe coluna: a sobra e 0,00 px, logo o encaixe e faixa', () => {
    // E por isso que `encaixe: ['coluna']` saiu do briefing: um campo que o motor
    // nao pode honrar e o HTTP 200 que ignora o parametro.
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 0.5625});
    expect(encaixe('topo', z)).toBe('faixa');
    expect(encaixe('principal', z)).toBe('faixa');
  });

  it('no 1:1 com fonte retrato o encaixe e coluna, e no 1:1 com paisagem e faixa', () => {
    expect(encaixe('topo', layout({largura: 1080, altura: 1080, razaoFonte: 0.5625}))).toBe(
      'coluna',
    );
    expect(encaixe('topo', layout({largura: 1080, altura: 1080, razaoFonte: 4 / 3}))).toBe(
      'faixa',
    );
  });

  it('faixa e coluna caem no MESMO Modo: o mapeamento e 3 -> 2', () => {
    expect(modoDoEncaixe('faixa')).toBe('sobreImagem');
    expect(modoDoEncaixe('coluna')).toBe('sobreImagem');
  });

  it('`caixaDaPista` e a mesma caixa que `pistas` devolve', () => {
    const z = layout({largura: 1080, altura: 1350, razaoFonte: 0.5625});
    for (const p of PISTAS) expect(caixaDaPista(p, z)).toEqual(pistas(z)[p]);
  });
});
