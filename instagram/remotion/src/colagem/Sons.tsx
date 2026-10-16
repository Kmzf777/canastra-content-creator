// Narracao, cama e efeitos da peca 06. Cada efeito mora numa `Sequence` que comeca
// no quadro do gesto visual que ele acompanha -- os mesmos tempos de `cenas.tsx`.

import {Audio} from '@remotion/media';
import React from 'react';
import {interpolate, Sequence, staticFile} from 'remotion';
import {DURACAO_Q, f, T} from './tempos';

type Efeito = [string, number, number?]; // [arquivo, segundos, volume]

const EFEITOS: Efeito[] = [
  ['thump', 0.05, 0.8],
  ['tick', 1.25, 0.5], ['tick', 1.68, 0.5], ['tick', 1.93, 0.5],
  ['carimbo', 3.45, 0.7], ['tink', 3.5, 0.45],
  ['rasgo', T.poisE, 0.55],
  ['slide', T.praGanhar, 0.5], ['slide', 5.4, 0.5],
  ['slide', T.duas, 0.5], ['slide', T.duas + 0.33, 0.5],
  ['rasgo', T.primeiro, 0.5], ['pop', 8.6, 0.6],
  ...Array.from({length: 20}, (_, i): Efeito => ['tick', T.amostra + i * 0.12, 0.28]),
  ['ding', T.gramasFim, 0.25], ['rasgo', T.gramasFim, 0.5],
  ...Array.from({length: 8}, (_, i): Efeito => ['pop', T.defeito + (i * 4) / 30, 0.45]),
  ['pop', 13.65, 0.5], ['carimbo', 13.92, 0.7], ['whoosh', 14.0, 0.6],
  ['carimbo', T.nenhum, 0.9], ['thump', T.nenhum, 0.7],
  ['rasgo', T.depois, 0.5], ['pop', T.xicara, 0.5], ['tink', 16.3, 0.35],
  ['nota1', T.aroma, 0.5], ['nota2', T.docura, 0.5], ['nota3', T.acidez, 0.5], ['nota4', T.corpo, 0.5],
  ['rasgo', T.nota, 0.5],
  ...Array.from({length: 8}, (_, i): Efeito => ['tick', 21.0 + i * 0.15, 0.3]),
  ['carimbo', T.oitenta, 0.9], ['ding', T.oitenta, 0.4],
  ['whoosh', T.porIsso, 0.6], ['rasgo', T.comeca, 0.6],
  ['rasgo', T.metros, 0.5],
  ...Array.from({length: 12}, (_, i): Efeito => ['tick', 27.6 + i * 0.075, 0.25]),
  ['carimbo', T.altimetroFim, 0.7], ['slide', 29.3, 0.45],
  ['rasgo', T.fruto, 0.5], ['pop', 31.0, 0.5], ['pop', 31.4, 0.5], ['pop', 32.1, 0.5],
  ['carimbo', T.acucar, 0.8], ['tink', T.acucar + 0.05, 0.3],
  ['rasgo', T.aGente, 0.5], ['slide', 34.69, 0.4],
  ['pop', T.planta, 0.55], ['pop', T.colhe, 0.55], ['pop', T.seleciona, 0.55],
  ['rasgo', T.semInter, 0.55], ['carimbo', T.semInter + 0.07, 0.85],
  ['carimbo', T.semMistura, 0.95], ['thump', T.semMistura, 0.6],
  ['rasgo', T.desde, 0.5],
  ['pop', T.desde + 0.37, 0.5], ['pop', T.desde + 0.47, 0.5], ['pop', T.desde + 0.57, 0.5], ['pop', T.desde + 0.67, 0.5],
  ['slide', T.geracoes, 0.45], ['slide', T.geracoes + 0.33, 0.45], ['slide', T.geracoes + 0.67, 0.45],
  ['whoosh', T.cafeCanastra - 0.3, 0.5],
  ['pop', T.cafeCanastra + 0.07, 0.55], ['pop', T.cafeCanastra + 0.2, 0.55], ['pop', T.cafeCanastra + 0.33, 0.55],
  ['tink', 48.5, 0.5],
];

export const Sons: React.FC = () => {
  const fimFala = f(T.falaFim);
  const cama = (q: number) => {
    const base = 0.09;
    const final = interpolate(q, [fimFala, fimFala + 12], [base, 0.22], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const sai = interpolate(q, [DURACAO_Q - 18, DURACAO_Q], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const entra = interpolate(q, [0, 6], [0.5, 1], {extrapolateRight: 'clamp'});
    return Math.max(base, final) * sai * entra;
  };
  return (
    <>
      <Audio src={staticFile('fonte/narracao.mp3')} volume={1} />
      <Audio src={staticFile('sfx/cama.wav')} volume={cama} />
      <Sequence from={f(T.comeca)} durationInFrames={f(7.2)}>
        <Audio src={staticFile('sfx/vento.wav')} volume={0.5} />
      </Sequence>
      {EFEITOS.map(([arq, s, vol = 0.5], i) => (
        <Sequence key={i} from={f(s)} durationInFrames={f(2)}>
          <Audio src={staticFile(`sfx/${arq}.wav`)} volume={vol} />
        </Sequence>
      ))}
    </>
  );
};
