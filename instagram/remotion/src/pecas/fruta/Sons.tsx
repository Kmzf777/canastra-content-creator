// Som da peça 08: narração, trilha em seções (scripts/colagem_sfx_08.py, cravada nas
// frases) e um efeito por entrada. Nenhum tempo digitado: tudo lê roteiro.ts.

import {Audio} from '@remotion/media';
import React from 'react';
import {interpolate, Sequence, staticFile} from 'remotion';
import {fq} from './apoio';
import {CHICOTES} from './trocas';
import {em, FIM, PALAVRAS, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14} from './roteiro';
import type {Faixa} from '../../colagem/legenda';

type Ef = [string, number, number?];
const DUR_Q = fq(FIM);
const ini = (f: {inicio: number}) => f.inicio;
/** Um pop por sílaba de uma faixa cinética: espalhados pela fala dela. */
const silabas = (f: Faixa, n: number, vol = 0.5): Ef[] =>
  Array.from({length: n}, (_, k): Ef => ['pop', f.inicio + ((f.fim - f.inicio) * k) / n, vol]);
const nao = (f: Faixa): Ef[] => [['carimbo', f.inicio, 0.95], ['thump', f.inicio, 0.75]];

export const EFEITOS: Ef[] = [
  // Ki
  ['slide', ini(S1.esse) + 0.05, 0.45], ['rabisco', em(S1.esse, 'aqui'), 0.4], ['whoosh', ini(S1.fruta) - 0.12, 0.45],
  ['fita', ini(S1.fruta), 0.5], ['rabisco', ini(S1.fruta) + 0.07, 0.45],
  ...silabas(S2.vermelha, 3), ...silabas(S2.doce, 2), ['brilho', ini(S2.doce) + 0.1, 0.55],
  ['pop', ini(S2.nunca), 0.45], ['rabisco', em(S2.nunca, 'nunca'), 0.4],
  ['carimbo', ini(S2.super), 0.75], ['digitacao', ini(S2.super) + 0.05, 0.5], ['rabisco', ini(S2.super) + 0.33, 0.55],
  // Shō
  ['fita', ini(S3.antes), 0.45], ['rabisco', ini(S3.antes) + 0.13, 0.4], ['pop', ini(S3.mede), 0.45], ['slide', em(S3.mede, 'mede'), 0.45],
  ['carimbo', ini(S3.acucar), 0.7], ['digitacao', ini(S3.acucar) + 0.05, 0.5], ['rabisco', ini(S3.acucar) + 0.2, 0.4],
  ...silabas(S3.exame, 5, 0.45), ['tink', ini(S3.exame) + 0.33, 0.5],
  ...silabas(S4.maduras, 4), ['rabisco', ini(S4.vem), 0.45],
  ['pop', ini(S4.outras), 0.45], ['pop', ini(S4.outras) + 0.1, 0.45], ['pop', ini(S4.outras) + 0.2, 0.45], ['rabisco', ini(S4.esperam), 0.5],
  ...silabas(S5.sol, 1, 0.6), ['brilho', ini(S5.sol) + 0.07, 0.6], ...silabas(S5.revirada, 8, 0.4),
  ['whoosh', ini(S5.frango) - 0.1, 0.45], ['rabisco', ini(S5.frango), 0.5], ['rabisco', ini(S5.frango) + 0.2, 0.35],
  ['rasgo', ini(S6.casca), 0.7], ['whoosh', ini(S6.casca) + 0.1, 0.45], ['rabisco', ini(S6.casca) + 0.05, 0.4],
  ...silabas(S7.dificil, 4), ...letrasPop(ini(S7.cinco)), ['carimbo', em(S7.cinco, 'máquinas'), 0.6], ['digitacao', em(S7.cinco, 'máquinas') + 0.05, 0.5],
  ...nao(S7.nao),
  // a rajada
  ...nao(S8.n1), ['fita', ini(S8.pedra), 0.45], ['rabisco', ini(S8.pedra) + 0.07, 0.45],
  ...nao(S8.n2), ['fita', ini(S8.graveto), 0.45], ['rabisco', ini(S8.graveto) + 0.07, 0.45],
  ...nao(S8.n3), ...silabas(S8.leve, 3, 0.45),
  ...nao(S8.n4), ['pop', ini(S8.preto), 0.55], ['rabisco', ini(S8.preto) + 0.17, 0.4], ['pop', ini(S8.verde), 0.55],
  ['rabisco', ini(S8.verde) + 0.17, 0.4], ['pop', ini(S8.ardido), 0.55], ['rabisco', ini(S8.ardido) + 0.17, 0.4],
  ['graos', em(S9.quem, 'sobrou'), 0.45], ...silabas({...S9.quem, inicio: em(S9.quem, 'sobrou'), fim: em(S9.quem, 'sobrou') + 0.5}, 2, 0.45),
  ['brilho', em(S9.quem, 'sobrou') + 0.2, 0.5],
  ['slide', ini(S9.tamanho), 0.5], ...silabas(S9.tamanho, 3, 0.45), ['rabisco', ini(S9.torrar), 0.45], ['rabisco', ini(S9.torrar) + 0.4, 0.35],
  ['rabisco', ini(S10.depoisTudo) + 0.07, 0.4], ['thump', em(S10.fogo, 'fogo'), 0.85], ['pop', em(S10.fogo, 'fogo'), 0.55],
  ['pop', em(S10.fogo, 'fogo') + 0.2, 0.55], ['tick', ini(S10.sim) - 0.05, 0.4], ['pop', ini(S10.sim), 0.5], ['rabisco', ini(S10.depois2), 0.45],
  ...silabas(S11.provou, 2), ...letrasPop(ini(S11.barulho), 6), ['golinho', ini(S11.barulho) - 0.05, 0.4],
  ...silabas(S11.cheirou, 2), ['rabisco', em(S11.deNovo, 'novo'), 0.45], ['pop', ini(S11.tecnica), 0.5], ['rabisco', em(S11.tecnica, 'juro'), 0.5],
  // Ten
  ['pop', ini(S12.fruta), 0.4], ['pop', ini(S12.semente), 0.4], ['pop', ini(S12.grao), 0.4],
  // Ketsu
  ...letrasPop(ini(S13.m1250), 7), ['carimbo', ini(S13.serra), 0.7], ['digitacao', ini(S13.serra) + 0.05, 0.5],
  ['pop', ini(S13.jaFoi), 0.45], ['rabisco', ini(S13.jaFoi) + 0.07, 0.4], ['slide', ini(S13.hoje), 0.55],
  ['brilho', ini(S13.canastra) + 0.07, 0.6], ['tink', ini(S13.canastra) + 0.2, 0.5],
  ['pop', ini(S14.amanha), 0.5], ['slide', ini(S14.vai), 0.45], ['rabisco', ini(S14.cafeManha), 0.45], ['brilho', ini(S14.cafeManha) + 0.2, 0.5],
  // chicotes: 0,16 s antes de cada troca
  ...CHICOTES.map((c): Ef => ['chicote', c.q / 30 - 0.16, 0.6]),
];

function letrasPop(s: number, n = 1, intervalo = 2): Ef[] {
  return Array.from({length: n}, (_, i): Ef => ['pop', s + (i * intervalo) / 30, 0.45]);
}

export const SonsFruta: React.FC = () => {
  const fimFala = fq(PALAVRAS[PALAVRAS.length - 1].fim + 0.2);
  const trilha = (q: number) => {
    const base = 0.2;
    const fim = interpolate(q, [fimFala, fimFala + 6], [base, 0.32], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
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
