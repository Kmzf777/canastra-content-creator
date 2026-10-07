// Som da peça 07: narração, trilha em seções e UM efeito para cada entrada de colagem
// (é o que as referências fazem: pop no texto, papel no recorte, caneta no traço).

import {Audio} from '@remotion/media';
import React from 'react';
import {interpolate, Sequence, staticFile} from 'remotion';
import {fq} from './apoio';
import {S1, S2, S3, S4, S5, S6, S7, S8, S9} from './roteiro';

type Ef = [string, number, number?];
const DUR_Q = fq(79.0);

const ini = (f: {inicio: number}) => f.inicio;

export const EFEITOS: Ef[] = [
  // 1 · tensão
  ['drone', 0, 0.75], ['batimento', 0.05, 0.85], ['batimento', 1.9, 0.7],
  ...[0.08, 0.15, 0.22, 0.28, 0.35, 0.42].map((s): Ef => ['pop', s, 0.45]),
  ['rabisco', 1.0, 0.5],
  ['pop', 0.6, 0.45], ['slide', 1.57, 0.5], ['whoosh', 1.62, 0.45], ['tick', 2.15, 0.4],
  ...[2.2, 2.47, 2.74, 3.02, 3.25, 3.49].map((s): Ef => ['pop', s, 0.55]),
  ['fita', ini(S1.casca), 0.5], ['rabisco', ini(S1.casca) + 0.17, 0.4], ['fita', ini(S1.pau), 0.5], ['rabisco', ini(S1.pau) + 0.17, 0.4],
  ['carimbo', ini(S1.lei), 0.85], ['digitacao', ini(S1.lei) + 0.05, 0.5], ['carimbo', 5.12, 0.95], ['thump', 5.12, 0.8],
  ['rabisco', 5.32, 0.35], ['rasgo', 5.55, 0.7],
  // 2 · calma
  ['brilho', ini(S2.calma), 0.6], ['rabisco', ini(S2.calma), 0.45], ['slide', 6.86, 0.5], ['slide', ini(S2.fim), 0.55],
  ['pop', ini(S2.fim) + 0.14, 0.5], ['rabisco', 9.0, 0.4], ['carimbo', ini(S2.seuEspecial), 0.7], ['digitacao', ini(S2.seuEspecial) + 0.05, 0.5],
  ['pop', 10.02, 0.55], ['rabisco', 10.2, 0.35], ['chicote', 10.72, 0.7],
  // 3 · mito
  ['pop', ini(S3.especial), 0.6], ['pop', ini(S3.nomeBonito), 0.55], ['slide', ini(S3.nomeBonito) + 0.05, 0.45],
  ['fita', ini(S3.nomeBonito) + 0.1, 0.4], ['fita', ini(S3.nomeBonito) + 0.2, 0.4], ['rabisco', ini(S3.noPacote), 0.55],
  ['whoosh', ini(S3.prova) - 0.07, 0.45],
  ['carimbo', ini(S3.prova), 0.8], ['digitacao', ini(S3.prova) + 0.05, 0.5], ['carimbo', ini(S3.duas), 1.0], ['thump', ini(S3.duas), 0.8],
  ['brilho', ini(S3.duas) + 0.07, 0.6], ['chicote', 14.62, 0.7],
  // 4 · prova 1
  ['graos', 14.85, 0.6], ['slide', ini(S4.classificador), 0.4], ['carimbo', 14.9, 0.6], ['digitacao', 14.95, 0.45], ['carimbo', ini(S4.graoCru), 0.6], ['digitacao', ini(S4.graoCru) + 0.05, 0.45],
  ...[0, 0.07, 0.13, 0.2, 0.27].map((d): Ef => ['pop', ini(S4.g350) + d, 0.45]),
  ['whoosh', 17.9, 0.45],
  ...(['preto', 'ardido', 'cereja', 'fungo', 'pedra', 'pau'] as const).flatMap((k): Ef[] => [['pop', ini(S4[k]), 0.65], ['rabisco', ini(S4[k]) + 0.13, 0.35]]),
  ['whoosh', 22.5, 0.4], ['tick', 23.2, 0.8], ['whoosh', 23.25, 0.5],
  ['carimbo', ini(S4.acabou), 1.0], ['thump', ini(S4.acabou), 0.9],
  ...[0.03, 0.07, 0.1, 0.13, 0.17, 0.2].map((d): Ef => ['pop', ini(S4.acabou) + d, 0.4]),
  ['carimbo', ini(S4.naoEspecial), 0.75], ['digitacao', ini(S4.naoEspecial) + 0.05, 0.5], ['chicote', 25.38, 0.7],
  // 5 · contraste
  ['rabisco', 25.6, 0.4], ['carimbo', ini(S5.classificacao), 0.6], ['digitacao', ini(S5.classificacao) + 0.05, 0.45],
  ['carimbo', 26.87, 0.55], ['carimbo', 27.2, 0.55], ['slide', 26.4, 0.4], ['carimbo', ini(S5.tipo), 0.7], ['digitacao', ini(S5.tipo) + 0.05, 0.45],
  ['graos', 28.0, 0.7], ['graos', 28.6, 0.6], ['graos', 29.2, 0.5],
  ...Array.from({length: 8}, (_, k): Ef => ['tick', ini(S5.d360) + k * 0.065, 0.35]),
  ['carimbo', 29.26, 0.75], ['chicote', ini(S5.noEspecial), 0.75], ['pop', 30.56, 0.5],
  ['carimbo', ini(S5.zero), 1.0], ['thump', ini(S5.zero), 0.8], ['brilho', ini(S5.zero) + 0.07, 0.55], ['rabisco', ini(S5.zero) + 0.13, 0.4],
  ['digitacao', 31.38, 0.45], ['whoosh', 31.9, 0.4],
  // 6 · prova 2
  ['rabisco', ini(S6.passou), 0.5], ['ding', ini(S6.passou) + 0.27, 0.35], ['carimbo', ini(S6.xicara), 0.7], ['digitacao', ini(S6.xicara) + 0.05, 0.45],
  ['carimbo', 34.09, 0.6], ['slide', 34.36, 0.5], ['golinho', 35.1, 0.7], ['tink', 35.5, 0.45],
  ...[0, 0.1, 0.2, 0.3, 0.4].map((d): Ef => ['pop', ini(S6.cinco) + d, 0.5]),
  ['golinho', 36.4, 0.55],
  ...(['aroma', 'docura', 'acidez', 'corpo', 'equilibrio'] as const).map((k): Ef => ['fita', ini(S6[k]), 0.45]),
  ['whoosh', 41.18, 0.35], ['rabisco', 41.48, 0.5], ['carimbo', ini(S6.perde), 1.0], ['thump', ini(S6.perde), 0.8],
  ['chicote', 43.3, 0.7], ['slide', 43.45, 0.5],
  ...Array.from({length: 6}, (_, k): Ef => ['tick', 43.6 + k * 0.06, 0.3]),
  ['ding', ini(S6.oitenta), 0.45], ['pop', ini(S6.oitenta), 0.5],
  ['pop', ini(S6.oitentaECinco), 0.5], ['carimbo', ini(S6.excelente), 0.7], ['digitacao', ini(S6.excelente) + 0.05, 0.45],
  ['pop', ini(S6.noventa), 0.55], ['brilho', ini(S6.noventa) + 0.07, 0.6], ['brilho', ini(S6.rarissimo) + 0.07, 0.6], ['rasgo', 49.2, 0.55],
  // 7 · a virada
  ['whoosh', 49.46, 0.4], ['pop', 49.53, 0.35], ['pop', 49.73, 0.35], ['pop', 49.93, 0.35], ['pop', 50.13, 0.35],
  ['pop', ini(S7.ninguem), 0.4], ['carimbo', ini(S7.nenhum), 0.8], ['digitacao', ini(S7.nenhum) + 0.05, 0.45],
  ['pop', 51.61, 0.4], ['carimbo', 52.16, 0.7], ['digitacao', 52.21, 0.45], ['rabisco', 52.81, 0.5], ['rasgo', 53.0, 0.55],
  ['fita', 53.3, 0.45], ['pop', 53.35, 0.45], ['pop', 53.68, 0.45], ['rabisco', 54.3, 0.35], ['rabisco', ini(S7.fermentou), 0.45],
  ['fita', ini(S7.verde), 0.45], ['pop', 55.9, 0.45], ['rabisco', 56.1, 0.35], ['rabisco', ini(S7.colheita), 0.45],
  ['chicote', 57.25, 0.7], ['pop', 57.53, 0.45], ['pop', 58.62, 0.45], ['rabisco', 59.04, 0.4], ['pop', 59.76, 0.45],
  ['pop', 59.9, 0.4], ['rabisco', 60.48, 0.5], ['carimbo', ini(S7.naoSalva), 0.8], ['digitacao', ini(S7.naoSalva) + 0.05, 0.45],
  ['carimbo', 60.06, 0.85], ['thump', 60.48, 0.85], ['chicote', 60.75, 0.6], ['pop', 60.96, 0.45],
  ...[0, 0.07, 0.13, 0.2, 0.27, 0.33].map((d): Ef => ['pop', 62.16 + d, 0.5]), ['chicote', 62.95, 0.75],
  // 8 · a fazenda
  ['fita', 62.9, 0.5], ['rabisco', ini(S8.planta), 0.45], ['fita', 64.55, 0.45], ['rabisco', ini(S8.colhe), 0.45],
  ['pop', 65.4, 0.45], ['rabisco', ini(S8.seleciona), 0.45], ['whoosh', 65.9, 0.45], ['fita', 66.3, 0.45],
  ...[0, 0.07, 0.13, 0.2, 0.27, 0.33, 0.4].map((d): Ef => ['pop', ini(S8.m1250) + d, 0.45]),
  ['carimbo', ini(S8.serra), 0.7], ['digitacao', ini(S8.serra) + 0.05, 0.5], ['whoosh', 69.4, 0.4],
  ['rabisco', ini(S8.devagar), 0.4], ['pop', 69.5, 0.5], ['pop', 69.95, 0.5], ['pop', 70.4, 0.5],
  ['rabisco', ini(S8.doce), 0.5], ['brilho', ini(S8.doce) + 0.07, 0.6], ['chicote', 71.5, 0.7],
  // 9 · o fecho
  ['slide', ini(S9.olha), 0.5], ['carimbo', ini(S9.procura), 0.7], ['digitacao', ini(S9.procura) + 0.05, 0.45], ['whoosh', 72.8, 0.4],
  ['pop', ini(S9.seNao), 0.45], ['carimbo', ini(S9.ninguem), 0.8], ['digitacao', ini(S9.ninguem) + 0.05, 0.45], ['carimbo', 75.36, 0.8],
  ['whoosh', ini(S9.nosso), 0.6], ['rabisco', ini(S9.nosso) + 0.5, 0.4], ['brilho', ini(S9.nosso) + 0.66, 0.6], ['tink', ini(S9.nosso) + 0.7, 0.5],
  ['chicote', ini(S9.salva) - 0.05, 0.6], ['pop', ini(S9.salva), 0.5], ['pop', ini(S9.salva) + 0.13, 0.5], ['pop', ini(S9.salva) + 0.27, 0.5],
  ['rabisco', ini(S9.salva) + 0.27, 0.4], ['brilho', ini(S9.salva) + 0.33, 0.5], ['tink', 78.4, 0.5],
];

export const SonsEspecial: React.FC = () => {
  const fimFala = fq(78.84);
  const trilha = (q: number) => {
    const base = 0.2;
    const fim = interpolate(q, [fimFala, fimFala + 6], [base, 0.34], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const sai = interpolate(q, [DUR_Q - 10, DUR_Q], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    return Math.max(base, fim) * sai;
  };
  return (
    <>
      <Audio src={staticFile('fonte/narracao.mp3')} volume={1} />
      <Audio src={staticFile('sfx/trilha.wav')} volume={trilha} />
      {EFEITOS.map(([arq, s, vol = 0.5], i) => (
        <Sequence key={i} from={Math.max(0, fq(s))} durationInFrames={fq(arq === 'drone' ? 6.4 : 2)}>
          <Audio src={staticFile(`sfx/${arq}.wav`)} volume={vol * 0.8} />
        </Sequence>
      ))}
    </>
  );
};
