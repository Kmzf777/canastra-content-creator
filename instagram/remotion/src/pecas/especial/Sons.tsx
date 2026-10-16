// Som da peça 07: narração, trilha em seções e UM efeito para cada entrada de colagem
// (é o que as referências fazem: pop no texto, papel no recorte, caneta no traço).
//
// Nenhum tempo aqui é digitado: cada efeito lê a palavra (`em`, `ini`) ou a troca de
// cena (`TROCA`, `CENA_INICIO`) que ele acompanha. Em 07/10/2026 o realinhamento da
// narração moveu palavras em até 0,7 s, e os segundos escritos à mão teriam ficado.

import {Audio} from '@remotion/media';
import React from 'react';
import {interpolate, Sequence, staticFile} from 'remotion';
import {fq} from './apoio';
import {CENA_INICIO, em, FIM, PALAVRAS, S1, S2, S3, S4, S5, S6, S7, S8, S9, TROCA} from './roteiro';

type Ef = [string, number, number?];
const DUR_Q = fq(FIM);

const ini = (f: {inicio: number}) => f.inicio;
/** O chicote soa 0,16 s antes da troca: a janela do borrão começa 6 quadros antes. */
const chicote = (s: number, vol = 0.7): Ef => ['chicote', s - 0.16, vol];
/** Um pop por letra de um recorte que entra a cada `intervalo` quadros (espaço não soa). */
const letras = (texto: string, s: number, intervalo = 2, vol = 0.45): Ef[] =>
  [...texto].flatMap((ch, i): Ef[] => (ch === ' ' ? [] : [['pop', s + (i * intervalo) / 30, vol]]));

// tempos que mais de um efeito usa
const compra = em(S1.doCafe, 'compra');
const [t0, t1, t2] = [S1.podeSer.inicio, S1.casca.inicio, S1.pau.inicio];
const lei = em(S1.lei, 'lei');
const especial2 = em(S2.seuEspecial, 'especial');
const quedas = em(S5.tipo, 'de') - 0.1;
const nasce = em(S7.nenhum, 'nasce');
const ruim = em(S7.naoSalva, 'ruim');
const salva7 = em(S7.naoSalva, 'salva');
const no = em(S7.decide, 'no');
const cena8 = CENA_INICIO[7];
const [tv, td] = [S8.devagar.inicio, S8.doce.inicio];
const mat = (k: number) => tv + (td - tv) * k;
const nosso = ini(S9.nosso);
const salva = ini(S9.salva);

export const EFEITOS: Ef[] = [
  // 1 · tensão
  ['drone', 0, 0.75], ['batimento', 0.05, 0.85], ['batimento', t0 - 0.3, 0.7],
  ...letras('ATÉ 1%', ini(S1.ate1)),
  ['rabisco', em(S1.doCafe, 'café') + 0.3, 0.5],
  ['pop', ini(S1.doCafe), 0.45], ['slide', compra - 0.05, 0.5], ['whoosh', compra, 0.45], ['tick', t0 - 0.05, 0.4],
  ...[t0, (t0 + t1) / 2, t1, t1 + (t2 - t1) * 0.37, t1 + (t2 - t1) * 0.68, t2].map((s): Ef => ['pop', s, 0.55]),
  ['fita', ini(S1.casca), 0.5], ['rabisco', ini(S1.casca) + 0.17, 0.4], ['fita', ini(S1.pau), 0.5], ['rabisco', ini(S1.pau) + 0.17, 0.4],
  ['carimbo', ini(S1.lei), 0.85], ['digitacao', ini(S1.lei) + 0.05, 0.5], ['carimbo', lei, 0.95], ['thump', lei, 0.8],
  ['rabisco', lei + 0.2, 0.35], ['rasgo', ini(S2.calma) - 0.21, 0.7],
  // 2 · calma
  ['brilho', ini(S2.calma), 0.6], ['rabisco', ini(S2.calma), 0.45], ['slide', em(S2.largar, 'largar'), 0.5], ['slide', ini(S2.fim), 0.55],
  ['pop', ini(S2.fim) + 0.14, 0.5], ['rabisco', ini(S2.saber) + 0.13, 0.4],
  ['carimbo', ini(S2.seuEspecial), 0.7], ['digitacao', ini(S2.seuEspecial) + 0.05, 0.5],
  ['pop', especial2, 0.55], ['rabisco', especial2 + 0.17, 0.35], chicote(CENA_INICIO[2]),
  // 3 · mito
  ['pop', ini(S3.especial), 0.6], ['pop', ini(S3.nomeBonito), 0.55], ['slide', ini(S3.nomeBonito) + 0.05, 0.45],
  ['fita', ini(S3.nomeBonito) + 0.1, 0.4], ['fita', ini(S3.nomeBonito) + 0.2, 0.4], ['rabisco', ini(S3.noPacote), 0.55],
  ['whoosh', ini(S3.prova) - 0.07, 0.45],
  ['carimbo', ini(S3.prova), 0.8], ['digitacao', ini(S3.prova) + 0.05, 0.5], ['carimbo', ini(S3.duas), 1.0], ['thump', ini(S3.duas), 0.8],
  ['brilho', ini(S3.duas) + 0.07, 0.6], chicote(CENA_INICIO[3]),
  // 4 · prova 1
  ['graos', ini(S4.primeira) + 0.05, 0.6], ['slide', ini(S4.classificador), 0.4],
  ['carimbo', ini(S4.primeira) + 0.1, 0.6], ['digitacao', ini(S4.primeira) + 0.15, 0.45],
  ['carimbo', ini(S4.graoCru), 0.6], ['digitacao', ini(S4.graoCru) + 0.05, 0.45],
  ...[0, 0.07, 0.13, 0.2, 0.27].map((d): Ef => ['pop', ini(S4.g350) + d, 0.45]),
  ['whoosh', ini(S4.olha), 0.45],
  ...(['preto', 'ardido', 'cereja', 'fungo', 'pedra', 'pau'] as const).flatMap((k): Ef[] => [['pop', ini(S4[k]), 0.65], ['rabisco', ini(S4[k]) + 0.13, 0.35]]),
  ['whoosh', ini(S4.achou), 0.4], ['tick', ini(S4.acabou) - 0.12, 0.8], ['whoosh', ini(S4.acabou) - 0.04, 0.5],
  ['carimbo', ini(S4.acabou), 1.0], ['thump', ini(S4.acabou), 0.9],
  ...[0.03, 0.07, 0.1, 0.13, 0.17, 0.2].map((d): Ef => ['pop', ini(S4.acabou) + d, 0.4]),
  ['carimbo', ini(S4.naoEspecial), 0.75], ['digitacao', ini(S4.naoEspecial) + 0.05, 0.5], chicote(CENA_INICIO[4]),
  // 5 · contraste
  ['rabisco', ini(S5.comparar) + 0.07, 0.4], ['carimbo', ini(S5.classificacao), 0.6], ['digitacao', ini(S5.classificacao) + 0.05, 0.45],
  ['carimbo', em(S5.classificacao, 'oficial'), 0.55], ['carimbo', em(S5.classificacao, 'brasileira'), 0.55],
  ['slide', em(S5.classificacao, 'classificação') + 0.23, 0.4],
  ['carimbo', em(S5.tipo, 'tipo'), 0.7], ['digitacao', em(S5.tipo, 'tipo') + 0.05, 0.45],
  ['graos', quedas, 0.7], ['graos', quedas + 0.6, 0.6], ['graos', quedas + 1.2, 0.5],
  ...Array.from({length: 8}, (_, k): Ef => ['tick', ini(S5.d360) + k * 0.065, 0.35]),
  ['carimbo', em(S5.d360, 'defeitos'), 0.75], ['chicote', ini(S5.noEspecial), 0.75], ['pop', em(S5.noEspecial, 'especial'), 0.5],
  ['carimbo', ini(S5.zero), 1.0], ['thump', ini(S5.zero), 0.8], ['brilho', ini(S5.zero) + 0.07, 0.55], ['rabisco', ini(S5.zero) + 0.13, 0.4],
  ['digitacao', em(S5.zero, 'defeito'), 0.45], ['whoosh', em(S5.zero, 'grave') + 0.08, 0.4],
  // 6 · prova 2
  ['rabisco', ini(S6.passou), 0.5], ['ding', ini(S6.passou) + 0.27, 0.35], ['carimbo', ini(S6.xicara), 0.7], ['digitacao', ini(S6.xicara) + 0.05, 0.45],
  ['carimbo', em(S6.xicara, 'xícara'), 0.6], ['slide', ini(S6.provadores), 0.5],
  ['golinho', em(S6.provadores, 'certificados') + 0.2, 0.7], ['tink', em(S6.provadores, 'provam'), 0.45],
  ...[0, 0.1, 0.2, 0.3, 0.4].map((d): Ef => ['pop', ini(S6.cinco) + d, 0.5]),
  ['golinho', ini(S6.lote) + 0.07, 0.55],
  ...(['aroma', 'docura', 'acidez', 'corpo', 'equilibrio'] as const).map((k): Ef => ['fita', ini(S6[k]), 0.45]),
  ['whoosh', em(S6.seUma, 'sair'), 0.35], ['rabisco', em(S6.seUma, 'diferente'), 0.5],
  ['carimbo', ini(S6.perde), 1.0], ['thump', ini(S6.perde), 0.8],
  chicote(TROCA.regua), ['slide', TROCA.regua + 0.05, 0.5],
  ...Array.from({length: 6}, (_, k): Ef => ['tick', TROCA.regua + 0.2 + k * 0.06, 0.3]),
  ['ding', ini(S6.oitenta), 0.45], ['pop', ini(S6.oitenta), 0.5],
  ['pop', ini(S6.oitentaECinco), 0.5], ['carimbo', ini(S6.excelente), 0.7], ['digitacao', ini(S6.excelente) + 0.05, 0.45],
  ['pop', ini(S6.noventa), 0.55], ['brilho', ini(S6.noventa) + 0.07, 0.6], ['brilho', ini(S6.rarissimo) + 0.07, 0.6],
  ['rasgo', ini(S7.aqui) - 0.26, 0.55],
  // 7 · a virada
  ['whoosh', ini(S7.aqui), 0.4], ...[0.07, 0.27, 0.47, 0.67].map((d): Ef => ['pop', ini(S7.aqui) + d, 0.35]),
  ['pop', ini(S7.ninguem), 0.4], ['carimbo', ini(S7.nenhum), 0.8], ['digitacao', ini(S7.nenhum) + 0.05, 0.45],
  ['pop', em(S7.nenhum, 'desses'), 0.4], ['carimbo', nasce, 0.7], ['digitacao', nasce + 0.05, 0.45],
  ['rabisco', em(S7.nenhum, 'torra'), 0.5], ['rasgo', TROCA.painel - 0.23, 0.55],
  ['fita', TROCA.painel + 0.1, 0.45], ['pop', ini(S7.pretoArdido), 0.45], ['pop', em(S7.pretoArdido, 'ardido'), 0.45],
  ['rabisco', em(S7.pretoArdido, 'fruto'), 0.35], ['rabisco', ini(S7.fermentou), 0.45],
  ['fita', ini(S7.verde), 0.45], ['pop', ini(S7.verde) + 0.2, 0.45], ['rabisco', ini(S7.colheita) - 0.07, 0.35], ['rabisco', ini(S7.colheita), 0.45],
  chicote(TROCA.tese), ['pop', ini(S7.estragar), 0.45], ['pop', em(S7.estragar, 'um'), 0.45], ['rabisco', em(S7.estragar, 'bom'), 0.4],
  ['pop', salva7, 0.45], ['pop', salva7 + 0.14, 0.4], ['rabisco', ruim, 0.5],
  ['carimbo', ini(S7.naoSalva), 0.8], ['digitacao', ini(S7.naoSalva) + 0.05, 0.45],
  ['carimbo', em(S7.naoSalva, 'um'), 0.85], ['thump', ruim, 0.85], chicote(TROCA.pe, 0.6), ['pop', ini(S7.decide), 0.45],
  ...letras('NO PÉ.', no, 2, 0.5), chicote(cena8, 0.75),
  // 8 · a fazenda
  ['fita', cena8 + 0.1, 0.5], ['fita', ini(S8.planta) - 0.3, 0.45], ['rabisco', ini(S8.planta), 0.45], ['rabisco', ini(S8.colhe), 0.45],
  ['pop', ini(S8.colhe) + 0.07, 0.45], ['rabisco', ini(S8.seleciona), 0.45], ['whoosh', ini(S8.seleciona) + 0.3, 0.45],
  ['fita', ini(S8.a) - 0.07, 0.45],
  ...[0, 0.07, 0.13, 0.2, 0.27, 0.33, 0.4].map((d): Ef => ['pop', ini(S8.m1250) + d, 0.45]),
  ['carimbo', ini(S8.serra), 0.7], ['digitacao', ini(S8.serra) + 0.05, 0.5], ['whoosh', tv - 0.08, 0.4],
  ['rabisco', tv, 0.4], ['pop', mat(0), 0.5], ['pop', mat(0.28), 0.5], ['pop', mat(0.56), 0.5],
  ['rabisco', ini(S8.doce), 0.5], ['brilho', ini(S8.doce) + 0.07, 0.6], chicote(CENA_INICIO[8]),
  // 9 · o fecho
  ['slide', ini(S9.olha), 0.5], ['carimbo', ini(S9.procura), 0.7], ['digitacao', ini(S9.procura) + 0.05, 0.45],
  ['whoosh', em(S9.procura, 'procura'), 0.4],
  ['pop', ini(S9.seNao), 0.45], ['carimbo', ini(S9.ninguem), 0.8], ['digitacao', ini(S9.ninguem) + 0.05, 0.45],
  ['carimbo', em(S9.ninguem, 'por'), 0.8],
  // "O nosso tá aqui": mergulho no selo, a etiqueta escrita, o círculo e o brilho
  ['whoosh', nosso - 0.12, 0.6], ['rabisco', nosso + 0.07, 0.4], ['rabisco', nosso + 0.27, 0.4],
  ['brilho', nosso + 0.4, 0.6], ['tink', nosso + 0.45, 0.5],
  chicote(salva, 0.6), ['pop', salva, 0.5], ['pop', salva + 0.13, 0.5], ['pop', salva + 0.27, 0.5],
  ['fita', salva + 0.1, 0.4], ['rabisco', salva + 0.13, 0.4], ['brilho', salva + 0.33, 0.5],
  ['tink', em(S9.compra, 'compra') + 0.38, 0.5],
];

export const SonsEspecial: React.FC = () => {
  const fimFala = fq(PALAVRAS[PALAVRAS.length - 1].fim + 0.22);
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
