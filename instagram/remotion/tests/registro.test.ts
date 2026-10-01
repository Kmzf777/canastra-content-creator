import {describe, expect, it} from 'vitest';
import {SOMBRA} from '../src/identidade/tokens';
import {caixaDoRegistro, SOMBRA_DO_REGISTRO, recorteEmPorcento} from '../src/motor/registro';

const CAIXA = {x: 0, y: 0, largura: 1080, altura: 1920};

describe('caixaDoRegistro', () => {
  it('telaCheia e a caixa inteira: a foto E o quadro', () => {
    expect(caixaDoRegistro('telaCheia', CAIXA)).toEqual(CAIXA);
  });

  it('moldura recua a margem de lado da marca nos dois eixos', () => {
    // 14,81% (160/1080) e a MARGEM.lado que o motor ja usa. Nenhum numero novo:
    // inventar uma "largura de moldura" seria escolher no olho um numero que
    // muda de significado a cada formato.
    const m = caixaDoRegistro('moldura', CAIXA);
    expect(m.x).toBeCloseTo(1080 * (160 / 1080), 6);
    expect(m.largura).toBeCloseTo(1080 * (1 - 2 * (160 / 1080)), 6);
    expect(m.y).toBeCloseTo(1920 * (160 / 1080), 6);
    // a moldura e simetrica: o mesmo recuo em cima e embaixo
    expect(m.y).toBeCloseTo(CAIXA.altura - (m.y + m.altura), 6);
  });

  it('cartao recua a margem de TOPO e ancora no alto', () => {
    const c = caixaDoRegistro('cartao', CAIXA);
    expect(c.y).toBeCloseTo(1920 * 0.05, 6);
    expect(c.x).toBeCloseTo(1080 * 0.05, 6);
    // ancorado no alto: sobra mais embaixo que em cima
    expect(CAIXA.altura - (c.y + c.altura)).toBeGreaterThan(c.y);
  });

  it('os tres registros sao geometricamente DISTINGUIVEIS', () => {
    // Se dois registros dessem a mesma caixa, declarar a origem seria decoracao.
    const t = caixaDoRegistro('telaCheia', CAIXA);
    const m = caixaDoRegistro('moldura', CAIXA);
    const c = caixaDoRegistro('cartao', CAIXA);
    expect(m).not.toEqual(t);
    expect(c).not.toEqual(t);
    expect(c).not.toEqual(m);
  });

  it('nenhum registro sai da caixa', () => {
    for (const r of ['telaCheia', 'moldura', 'cartao'] as const) {
      const b = caixaDoRegistro(r, CAIXA);
      expect(b.x).toBeGreaterThanOrEqual(0);
      expect(b.y).toBeGreaterThanOrEqual(0);
      expect(b.x + b.largura).toBeLessThanOrEqual(CAIXA.largura + 1e-6);
      expect(b.y + b.altura).toBeLessThanOrEqual(CAIXA.altura + 1e-6);
    }
  });

  it('a caixa de origem desloca o registro: ele nao assume o canto 0,0', () => {
    // Cena em contain recebe `zonas.video`, que nao comeca em 0,0 no 1:1. Um
    // registro que ignorasse `caixa.x/y` poria a moldura fora da imagem.
    const deslocada = {x: 100, y: 200, largura: 400, altura: 500};
    const m = caixaDoRegistro('moldura', deslocada);
    expect(m.x).toBeCloseTo(100 + 400 * (160 / 1080), 6);
    expect(m.y).toBeCloseTo(200 + 500 * (160 / 1080), 6);
  });

  it('cada registro usa um perfil de sombra DIFERENTE: nunca a mesma em duas camadas', () => {
    expect(SOMBRA_DO_REGISTRO.moldura).toEqual(SOMBRA.papel);
    expect(SOMBRA_DO_REGISTRO.cartao).toEqual(SOMBRA.cartao);
    // telaCheia nao tem sombra: nao ha borda para a sombra cair.
    expect(SOMBRA_DO_REGISTRO.telaCheia).toBeNull();
  });
});

describe('recorteEmPorcento', () => {
  it('recorte de fracao vira largura e deslocamento em porcento', () => {
    // A foto de 4032x3024 recortada para 9:16 aproveita 1701 px de largura =
    // 0,4218 da largura. A imagem tem que ficar 1/0,4218 = 237,05% da caixa, e
    // deslocada -x/largura.
    const r = recorteEmPorcento({tipo: 'recorte', x: 0.2, y: 0, largura: 0.4218, altura: 1});
    expect(r.larguraPorcento).toBeCloseTo(237.08, 1);
    expect(r.alturaPorcento).toBeCloseTo(100, 6);
    expect(r.esquerdaPorcento).toBeCloseTo(-47.415, 2);
    expect(r.topoPorcento).toBeCloseTo(0, 6);
  });

  it('faixa devolve 100% sem deslocamento', () => {
    const r = recorteEmPorcento({tipo: 'faixa'});
    expect(r.larguraPorcento).toBe(100);
    expect(r.alturaPorcento).toBe(100);
    expect(r.esquerdaPorcento).toBe(0);
    expect(r.topoPorcento).toBe(0);
  });

  it('recorte no CENTRO de uma foto paisagem para 9:16: a conta inteira', () => {
    // 4032x3024 num 9:16 precisa de uma coluna de 3024*(9/16) = 1701 px, centrada:
    // x = (4032-1701)/2 = 1165,5 -> fracao 0,289. A imagem fica 237,08% de largura
    // e recua 68,52% dela. Numeros derivados da foto real, nao escolhidos.
    const largura = 1701 / 4032;
    const x = (4032 - 1701) / 2 / 4032;
    const r = recorteEmPorcento({tipo: 'recorte', x, y: 0, largura, altura: 1});
    expect(r.larguraPorcento).toBeCloseTo(237.04, 1);
    expect(r.esquerdaPorcento).toBeCloseTo(-68.52, 1);
  });
});
