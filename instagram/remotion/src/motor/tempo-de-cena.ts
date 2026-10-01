// O TERCEIRO RELOGIO, em tres funcoes puras.
//
// POR QUE NAO MORAM EM `Peca.tsx`
//
// Porque elas tem TESTE, e `Peca.tsx` importa `camadas/Legenda.tsx` ->
// `identidade/tipografia.ts`, que faz `loadFont` e `delayRender` no topo do modulo. Nao
// existe `vitest.config*` neste projeto, logo o ambiente e `node`: sem `document`, e o
// carregamento estoura com `TypeError: Invalid URL`. Medido em 30/09/2026 -- um teste
// que so importava `Legenda.tsx` passou a asercao e o vitest ainda saiu com codigo 1.
//
// E a mesma fronteira de `movimento.ts` e `texto-forma.ts`: nada que precise de prova
// mora num `.tsx`. `Peca.tsx` reexporta as tres, para quem le a arvore nao ter que
// cacar.

import type {Plano} from '../briefing/compilar';

/** A janela de uma cena no relogio da PECA. */
export function janelaDaCenaNaPeca(p: Plano, i: number): {de: number; ate: number} {
  const c = p.cenas[i];
  if (!c) throw new Error(`janelaDaCenaNaPeca: nao existe cena ${i} em ${p.cenas.length}`);
  return {de: c.inicioNaPecaFrames, ate: c.inicioNaPecaFrames + c.duracaoFrames};
}

/**
 * O frame da CENA, dado um frame da PECA.
 *
 * Dentro de `TransitionSeries.Sequence` o Remotion rebaseia `useCurrentFrame()`, e esta
 * funcao e a MESMA conta feita a mao -- para o teste poder verificar sem renderizar.
 */
export function frameDaCenaNoFrameDaPeca(p: Plano, i: number, framePeca: number): number {
  return framePeca - janelaDaCenaNaPeca(p, i).de;
}

/**
 * A janela de um EVENTO no relogio da PECA. E ela que decide em que frame olhar.
 *
 * EXISTE POR UM DEFEITO MEDIDO. A versao anterior do plano derivou as janelas das
 * CENAS corretamente e nunca derivou as dos EVENTOS dentro delas -- entao dois dos sete
 * stills de conferencia pediam frames em que o evento que eles deveriam mostrar JA
 * TINHA TERMINADO. Com a funcao, o frame sai de uma conta em vez de um chute.
 */
export function janelaDoEventoNaPeca(
  p: Plano,
  cena: number,
  evento: number,
): {de: number; ate: number} {
  const c = p.cenas[cena];
  if (!c) throw new Error(`janelaDoEventoNaPeca: nao existe cena ${cena}`);
  const e = c.eventos[evento];
  if (!e) {
    throw new Error(
      `janelaDoEventoNaPeca: a cena ${cena} nao tem evento ${evento} (tem ${c.eventos.length})`,
    );
  }
  const de = c.inicioNaPecaFrames + e.inicioFrames;
  return {de, ate: de + e.duracaoFrames};
}
