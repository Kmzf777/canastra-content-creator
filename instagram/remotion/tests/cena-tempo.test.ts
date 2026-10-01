import {describe, expect, it} from 'vitest';
import {compilar} from '../src/briefing/compilar';
import {zBriefing} from '../src/briefing/esquema';
// DE `tempo-de-cena.ts`, NAO DE `Peca.tsx`.
//
// `Peca.tsx` importa `camadas/Legenda.tsx` -> `identidade/tipografia.ts`, que faz
// `loadFont` e `delayRender` no TOPO DO MODULO. Nao existe `vitest.config*` neste
// projeto, entao o ambiente e `node`: sem `document`, e o fetch de asset estoura com
// `TypeError: Invalid URL`. As duas funcoes puras nascem num `.ts` e `Peca.tsx`
// REEXPORTA de la.
import {
  frameDaCenaNoFrameDaPeca,
  janelaDaCenaNaPeca,
  janelaDoEventoNaPeca,
} from '../src/motor/tempo-de-cena';

function tresCenas(transicoes: unknown[]) {
  return zBriefing.parse({
    _esquema: 'canastra-briefing/1',
    serie: 'avulsa',
    formatos: ['9:16'],
    duracao: {modo: 'somaCenas'},
    cenas: [
      {duracaoS: 2, fonte: {tipo: 'cor', cor: '#3B2A1F'}, eventos: [{papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'topo'}]},
      {duracaoS: 3, fonte: {tipo: 'cor', cor: '#4A5D3A'}, eventos: [{papel: 'manchete', texto: 'DOIS', entradaS: 0, pista: 'topo'}]},
      {duracaoS: 4, fonte: {tipo: 'cor', cor: '#C8661E'}, eventos: [{papel: 'manchete', texto: 'TRES', entradaS: 0, pista: 'topo'}]},
    ],
    transicoes,
    audio: {locucao: {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 0}, trilha: null},
    gancho: 'g',
    cta: 'c',
  });
}

describe('janela de cada cena no relogio da PECA', () => {
  it('com corte, as cenas se encostam sem sobrepor', () => {
    const p = compilar(tresCenas([{tipo: 'corte'}, {tipo: 'corte'}]));
    expect(janelaDaCenaNaPeca(p, 0)).toEqual({de: 0, ate: 60});
    expect(janelaDaCenaNaPeca(p, 1)).toEqual({de: 60, ate: 150});
    expect(janelaDaCenaNaPeca(p, 2)).toEqual({de: 150, ate: 270});
    expect(p.duracaoFrames).toBe(270);
  });

  it('com fade, as janelas SE SOBREPOEM exatamente pela duracao da transicao', () => {
    // Durante a transicao as duas cenas sao renderizadas. Se as janelas nao se
    // sobrepusessem, haveria um frame de terra chapado no meio do crossfade.
    const p = compilar(tresCenas([{tipo: 'fade', duracaoS: 0.5}, {tipo: 'corte'}]));
    const a = janelaDaCenaNaPeca(p, 0);
    const b = janelaDaCenaNaPeca(p, 1);
    expect(a.ate - b.de).toBe(15);
    expect(p.duracaoFrames).toBe(270 - 15);
  });

  it('o frame da CENA e o frame da peca menos o inicio da cena', () => {
    // E o terceiro relogio: dentro de `TransitionSeries.Sequence` o Remotion rebaseia
    // `useCurrentFrame()`, e esta funcao e a mesma conta feita a mao, para o teste
    // poder verificar sem renderizar.
    const p = compilar(tresCenas([{tipo: 'corte'}, {tipo: 'corte'}]));
    expect(frameDaCenaNoFrameDaPeca(p, 1, 60)).toBe(0);
    expect(frameDaCenaNoFrameDaPeca(p, 1, 75)).toBe(15);
    expect(frameDaCenaNoFrameDaPeca(p, 2, 150)).toBe(0);
  });

  it('a ultima janela termina EXATAMENTE na duracao da peca', () => {
    // Invariante que pega erro de sinal: se `inicioNaPecaFrames` somasse a transicao
    // em vez de subtrair, este teste falha e o video sairia mais longo que o briefing
    // sem ninguem perceber.
    for (const trans of [
      [{tipo: 'corte'}, {tipo: 'corte'}],
      [{tipo: 'fade', duracaoS: 0.5}, {tipo: 'corte'}],
      [{tipo: 'fade', duracaoS: 0.5}, {tipo: 'wipe', duracaoS: 0.25, direcao: 'from-left'}],
    ]) {
      const p = compilar(tresCenas(trans));
      const ultima = janelaDaCenaNaPeca(p, p.cenas.length - 1);
      expect(ultima.ate).toBe(p.duracaoFrames);
    }
  });

  it('cena que nao existe LANCA, com os dois numeros', () => {
    const p = compilar(tresCenas([{tipo: 'corte'}, {tipo: 'corte'}]));
    expect(() => janelaDaCenaNaPeca(p, 7)).toThrow(/nao existe cena 7 em 3/);
  });
});

describe('janela do EVENTO no relogio da peca', () => {
  it('o evento e cena-relativo, e a janela dele soma o inicio da cena', () => {
    // O defeito que esta funcao existe para nao repetir: a versao anterior derivava as
    // janelas das CENAS e nunca as dos EVENTOS, e dois stills de conferencia pediam
    // frames em que o evento ja tinha terminado.
    const p = compilar(tresCenas([{tipo: 'corte'}, {tipo: 'corte'}]));
    const j = janelaDoEventoNaPeca(p, 1, 0);
    expect(j.de).toBe(60 + p.cenas[1].eventos[0].inicioFrames);
    expect(j.ate - j.de).toBe(p.cenas[1].eventos[0].duracaoFrames);
    // E o frame do meio da janela e um frame em que o evento ESTA no ar.
    const meio = Math.floor((j.de + j.ate) / 2);
    expect(meio).toBeGreaterThanOrEqual(j.de);
    expect(meio).toBeLessThan(j.ate);
  });

  it('evento que nao existe LANCA dizendo quantos a cena tem', () => {
    const p = compilar(tresCenas([{tipo: 'corte'}, {tipo: 'corte'}]));
    expect(() => janelaDoEventoNaPeca(p, 0, 3)).toThrow(/nao tem evento 3 \(tem 1\)/);
  });
});

describe('a aritmetica de duracao do compilador', () => {
  it('somaCenas com alvoS divergente LANCA, com os dois numeros e a diferenca', () => {
    let erro: Error | null = null;
    try {
      compilar(
        zBriefing.parse({
          ...tresCenas([{tipo: 'fade', duracaoS: 1}, {tipo: 'corte'}]),
          duracao: {modo: 'somaCenas', alvoS: 12},
        }),
      );
    } catch (e) {
      erro = e as Error;
    }
    expect(erro).not.toBeNull();
    expect(erro!.message).toMatch(/240/); // a peca que sai
    expect(erro!.message).toMatch(/360/); // a que o alvo pede
    expect(erro!.message).toMatch(/120 frames/); // a diferenca
  });

  it('totalFixo DEVOLVE os frames da transicao as cenas, e a soma bate', () => {
    const p = compilar(
      zBriefing.parse({
        ...tresCenas([{tipo: 'fade', duracaoS: 1}, {tipo: 'corte'}]),
        duracao: {modo: 'totalFixo', alvoS: 9},
      }),
    );
    expect(p.duracaoFrames).toBe(270);
    expect(janelaDaCenaNaPeca(p, 2).ate).toBe(270);
  });
});
