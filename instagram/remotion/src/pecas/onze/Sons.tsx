// Som da peça 08b: narração, trilha em seções (scripts/colagem_sfx_08b.py, cravada nas
// frases) e um efeito por entrada. Nenhum tempo digitado: tudo lê roteiro.ts.
// Nada de chiado, estalo ou "crack" na torra (lição 66).

import {Audio} from '@remotion/media';
import React from 'react';
import {interpolate, Sequence, staticFile} from 'remotion';
import {fq} from '../fruta/apoio';
import {CHICOTES} from './trocas';
import {em, FIM, PALAVRAS, S0, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S13, S14, S15} from './roteiro';
import type {Faixa} from '../../colagem/legenda';

type Ef = [string, number, number?];
const DUR_Q = fq(FIM);
const i0 = (f: {inicio: number}) => f.inicio;
const silabas = (f: Faixa, n: number, vol = 0.5): Ef[] =>
  Array.from({length: n}, (_, k): Ef => ['pop', f.inicio + ((f.fim - f.inicio) * k) / n, vol]);
const letras = (s: number, n: number, vol = 0.42): Ef[] => Array.from({length: n}, (_, k): Ef => ['pop', s + (k * 2) / 30, vol]);

export const EFEITOS: Ef[] = [
  ...silabas(S0.reprovado, 4), ['rabisco', i0(S0.reprovado) + 0.5, 0.45],
  ...letras(i0(S1.onze), 6), ['slide', i0(S1.chegar) + 0.1, 0.4], ['whoosh', i0(S1.caminho), 0.4], ['rabisco', i0(S1.caminho) + 0.1, 0.4],
  ['slide', i0(S2.fim) + 0.3, 0.4], ['golinho', em(S2.fim, 'você', 2), 0.5], ...letras(i0(S2.amarga), 6), ['thump', i0(S2.amarga), 0.6],
  ['rabisco', i0(S3.primeira) + 0.1, 0.4], ['carimbo', i0(S3.serra), 0.7], ['digitacao', i0(S3.serra) + 0.05, 0.45], ...letras(i0(S3.m1250), 6),
  ['carimbo', i0(S4.acucar), 0.7], ['digitacao', i0(S4.acucar) + 0.05, 0.45], ['rabisco', i0(S4.refrat), 0.45], ['pop', i0(S4.vinho), 0.5],
  ['brilho', i0(S4.mede), 0.45],
  ...silabas(S5.maduro, 3, 0.45), ['pop', em(S5.verde, 'xícara'), 0.45], ['carimbo', i0(S5.amargor), 0.75], ['digitacao', i0(S5.amargor) + 0.05, 0.45],
  ['pop', i0(S6.sol), 0.55], ['brilho', i0(S6.sol) + 0.1, 0.55], ['rabisco', em(S6.terreiro, 'revirado'), 0.45], ...letras(i0(S6.fermenta), 8, 0.35),
  ['pop', i0(S6.fermentado), 0.45], ['carimbo', i0(S6.ardido), 0.85], ['thump', i0(S6.ardido), 0.6], ['rabisco', i0(S6.ardido) + 0.15, 0.4],
  ['rasgo', i0(S7.casca) + 0.2, 0.65], ['rabisco', i0(S7.casca) + 0.25, 0.4], ...letras(i0(S7.peneira), 8, 0.35),
  ['thump', i0(S8.pedra), 0.7], ...letras(i0(S8.pedra), 5, 0.4), ['thump', i0(S8.graveto), 0.7], ...letras(i0(S8.graveto), 7, 0.4),
  ...silabas(S8.leve, 3, 0.45), ['rabisco', i0(S8.oco), 0.45], ['rabisco', em(S8.maquina, 'grão'), 0.4],
  ['carimbo', i0(S8.defeitos), 0.7], ['digitacao', i0(S8.defeitos) + 0.05, 0.4], ['whoosh', em(S8.sopro, 'sopro'), 0.7],
  ...letras(em(S8.sopro, 'sopro'), 5, 0.4),
  ...silabas(S9.tamanho, 3, 0.45), ['graos', i0(S9.tamanho), 0.4], ['rabisco', em(S9.porque, 'torram'), 0.4],
  ['pop', em(S10.aqui, 'quase'), 0.4], ...letras(i0(S10.nenhuma), 7, 0.45), ['rabisco', em(S10.nenhuma, 'torra'), 0.4],
  ['pop', em(S11.quando, 'amarga'), 0.4], ['whoosh', em(S11.pulada, 'pulada') - 0.15, 0.55], ['rabisco', em(S11.pulada, 'pulada'), 0.45],
  ['slide', em(S11.disfarcar, 'disfarçar') - 0.1, 0.55], ['carimbo', em(S11.disfarcar, 'disfarçar') + 0.3, 0.6],
  ...silabas(S13.xicara, 3, 0.45), ['carimbo', em(S13.arthur, 'Arthur'), 0.6],
  ...[S13.aroma, S13.corpo, S13.docura, S13.citric].flatMap((f): Ef[] => [['carimbo', i0(f), 0.6], ['tink', i0(f) + 0.15, 0.35]]),
  ['slide', i0(S13.classico), 0.5], ...letras(i0(S13.oitenta), 3, 0.5), ['brilho', i0(S13.oitenta) + 0.15, 0.55],
  ['rabisco', i0(S14.ficou), 0.45], ['pop', i0(S15.manda), 0.45], ['rabisco', i0(S15.manda) + 0.2, 0.4], ['tink', em(S15.manda, 'igual') + 0.3, 0.45],
  ...CHICOTES.map((c): Ef => ['chicote', c.q / 30 - 0.16, 0.55]),
];

export const SonsOnze: React.FC = () => {
  const fimFala = fq(PALAVRAS[PALAVRAS.length - 1].fim + 0.2);
  const trilha = (q: number) => {
    const base = 0.16;
    const fim = interpolate(q, [fimFala, fimFala + 6], [base, 0.3], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const sai = interpolate(q, [DUR_Q - 10, DUR_Q], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    return Math.max(base, fim) * sai;
  };
  return (
    <>
      <Audio src={staticFile('fonte/narracao.mp3')} volume={1} />
      <Audio src={staticFile('sfx/trilha.wav')} volume={trilha} />
      {EFEITOS.map(([arq, s, vol = 0.5], i) => (
        <Sequence key={i} from={Math.max(0, fq(s))} durationInFrames={fq(2)}>
          <Audio src={staticFile(`sfx/${arq}.wav`)} volume={vol * 0.75} />
        </Sequence>
      ))}
    </>
  );
};
