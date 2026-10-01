// O PORTAO DA FIACAO DE FPS.
//
// POR QUE ISTO E UM TESTE DE FONTE, E NAO DE COMPORTAMENTO
//
// As camadas de desenho sao `.tsx` e importam `identidade/tipografia.ts`, que faz
// `loadFont` no topo do modulo. Em Node isso estoura `TypeError: Invalid URL`: medido
// em 30/09/2026, um teste que so importava `Legenda.tsx` passou a asercao e o vitest
// ainda saiu com codigo 1. Entao nao da para montar estas camadas aqui e olhar o que
// elas fazem -- a prova de comportamento delas e render.
//
// O que DA para provar em Node, e e o que falha de verdade, e o CONTRATO: que nenhuma
// camada de desenho invente a conversao segundo->frame.
//
// O MODO DE FALHA QUE ISTO BARRA
//
// Ate 01/10/2026 `Legenda.tsx` recebia `deslocamentoFrames` e `Fonte.tsx` recebia
// `cortarAntesFrames`, e as duas usavam o numero direto. O ar morto medido no `pl.mp4`
// e 1,14 SEGUNDO; os 34 frames eram aquele segundo lido a 30 fps. Numa composicao de
// 60 fps os mesmos 34 frames valem 0,567 s -- metade do corte na `Fonte` e metade do
// deslocamento na `Legenda` -- e nada reclama: o render sai inteiro com exit 0, a
// legenda acha SEMPRE algum bloco (so o errado) e o video comeca com meio segundo de
// nada.
//
// ---------------------------------------------------------------------------
// O CONTRATO MUDOU EM 01/10/2026, E A MUDANCA E UM GANHO -- NAO UM RECUO
//
// A versao anterior deste portao exigia que `Fonte.tsx` recebesse `aparaAntesSegundos`
// e convertesse ELA MESMA com `useVideoConfig`. Era a posicao certa enquanto o motor
// nao tinha compilador: a unica fronteira disponivel era a camada.
//
// Com `src/briefing/compilar.ts`, a conversao de TODO tempo de briefing passou a
// acontecer uma vez, num modulo PURO e com teste, antes de qualquer `.tsx` existir --
// e `Fonte.tsx` passou a receber `aparaAntesFrames`, ja no fps da peca. A invariante
// defendida aqui continua sendo a mesma frase ("a conversao e uma so"), so que agora
// ela e verificavel num lugar melhor: um modulo que o vitest consegue EXECUTAR, em vez
// de um `.tsx` que ele so consegue LER.
//
// `PecaVideo.tsx` nao existe mais (Tarefa 9): quem monta a arvore e `Peca.tsx` +
// `Cena.tsx`. Entao a lista de arquivos vigiados cresceu, em vez de encolher.

import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {describe, expect, it} from 'vitest';
import {emFrames} from '../src/motor/relogio';

const fonte = (rel: string) =>
  fs.readFileSync(fileURLToPath(new URL(`../src/${rel}`, import.meta.url)), 'utf8');

const LEGENDA = fonte('motor/camadas/Legenda.tsx');
const FONTE = fonte('motor/camadas/Fonte.tsx');
const TEXTO_TELA = fonte('motor/camadas/TextoTela.tsx');
const TRILHA = fonte('motor/camadas/Trilha.tsx');
const CENA = fonte('motor/Cena.tsx');
const PECA = fonte('motor/Peca.tsx');
const COMPILAR = fonte('briefing/compilar.ts');

// Comentario e prosa: um `cortarAntesFrames` dentro de `//` ou de `/** */` e historia
// escrita, nao fiacao. Sem esta limpeza o teste reprovaria exatamente os cabecalhos que
// explicam por que a fiacao mudou.
function semComentario(s: string): string {
  return s.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
}

/** Todo `.tsx` que desenha e le tempo. */
const CAMADAS = [
  ['Legenda.tsx', LEGENDA],
  ['Fonte.tsx', FONTE],
  ['TextoTela.tsx', TEXTO_TELA],
  ['Trilha.tsx', TRILHA],
  ['Cena.tsx', CENA],
  ['Peca.tsx', PECA],
] as const;

describe('fiacao de fps nas camadas de desenho', () => {
  it('as camadas que precisam do fps da composicao pedem a ela, nao a uma constante', () => {
    // `Fonte.tsx` NAO esta nesta lista de proposito: desde que o compilador converte, a
    // camada de fonte nao tem mais nenhum tempo em segundo para converter, e um
    // `useVideoConfig()` ali seria um gancho sem uso.
    for (const [nome, s] of [
      ['Legenda.tsx', LEGENDA],
      ['TextoTela.tsx', TEXTO_TELA],
      ['Trilha.tsx', TRILHA],
      ['Cena.tsx', CENA],
      ['Peca.tsx', PECA],
    ] as const) {
      expect(semComentario(s), nome).toContain('useVideoConfig()');
    }
  });

  it('NENHUM .tsx converte segundo->frame a mao', () => {
    // `Math.round(x * fps)` espalhado por camada foi o estado de antes de 01/10/2026,
    // em quatro lugares diferentes. A conversao e uma so, e e a do relogio -- so ela
    // recusa fps fracionario e segundo negativo.
    for (const [nome, s] of CAMADAS) {
      expect(semComentario(s), nome).not.toMatch(/Math\.round\s*\([^)]*fps/);
      expect(semComentario(s), nome).not.toMatch(/\*\s*fps\s*\)/);
    }
  });

  it('quem converte e `compilar.ts`, por emFrames, e ele nao importa React', () => {
    const limpo = semComentario(COMPILAR);
    expect(limpo).toContain('emFrames(');
    expect(limpo).not.toMatch(/Math\.round\s*\([^)]*fps/);
    // PURO: um `import React` ou um `node:crypto` aqui derrubaria o render ou o vitest.
    expect(limpo).not.toMatch(/from\s+'react'/);
    expect(limpo).not.toMatch(/node:crypto/);
  });

  it('nenhuma camada de desenho aceita o ar morto com o NOME antigo', () => {
    // Os dois nomes antigos. Se um deles voltar a aparecer na fiacao, voltou o defeito
    // -- e nenhum render de 30 fps o mostraria.
    for (const [nome, s] of CAMADAS) {
      const limpo = semComentario(s);
      expect(limpo, nome).not.toContain('deslocamentoFrames');
      expect(limpo, nome).not.toContain('cortarAntesFrames');
    }
  });

  it('a legenda chega no relogio da PECA: `Peca` passa deslocamento ZERO', () => {
    // Com N cenas ha N valores de `aparaAntesS` e UMA legenda, entao "o" ar morto
    // deixa de ser definido. O rebase passou para os DADOS, em `compilar.ts`, e a
    // fiacao nao desloca mais nada. Um numero diferente de 0 aqui seria rebase duplo.
    expect(semComentario(PECA)).toMatch(/deslocamentoSegundos=\{0\}/);
  });

  it('e o numero que faz isso importar: 1,14 s sao 34 frames a 30 e 68 a 60', () => {
    // Medido no `pl.mp4`: 1,14 s de ar morto na cabeca. Enquanto o briefing guardasse
    // 34 frames, uma composicao de 60 fps cortaria 34 frames = 0,567 s.
    const AR_MORTO_S = 1.14;
    expect(emFrames(AR_MORTO_S, 30)).toBe(34);
    expect(emFrames(AR_MORTO_S, 60)).toBe(68);
    // E a volta completa continua sendo identidade a 30 fps.
    expect(emFrames(34 / 30, 30)).toBe(34);
  });
});
