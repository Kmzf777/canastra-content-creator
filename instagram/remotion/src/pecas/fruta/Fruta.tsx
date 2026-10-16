// Peça 08 — "Esse café já foi uma fruta". Raiz: escolhe a cena pelo quadro, aplica o
// chicote nas trocas grandes (vídeo <-> colagem) e deixa CORTE SECO na rajada e dentro
// da prova (o ritmo das referências: corte a cada 0,7 s no pico). Por cima, o grão de
// filme e a pílula; no escuro da virada a pílula vira legenda pequena.

import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import '../../colagem/fontes-colagem';
import {REPOUSO} from '../../colagem/camera';
import {Palco} from '../../colagem/palco';
import {Pilula} from '../../colagem/tipos';
import {fq, GraoFilme, LegendaPequena} from './apoio';
import {CENAS} from './cenas';
import {BLOCOS_A, FIM} from './roteiro';
import {CHICOTES, LIMITES} from './trocas';
import {SonsFruta} from './Sons';

export const DURACAO_FRUTA = fq(FIM);
/** Tema da pílula por cena: vídeo e fundo escuro = pílula creme; colagem clara = pílula terra. */
const CLARAS = new Set([2, 3, 5, 7, 9, 10, 12, 14, 23, 24]);
const ESCURAS_PEQUENAS = new Set([20, 21]);


const cenaEm = (x: number) => {
  let i = 0;
  while (i + 1 < LIMITES.length && x >= LIMITES[i + 1]) i++;
  return i;
};

/** Janela do chicote: 12 quadros em volta da troca (mesma curva da peça 07). */
export function chicoteEm(q: number) {
  for (const c of CHICOTES) {
    const d = q - c.q;
    if (d >= -6 && d <= 5) {
      const u = 0.5 - 0.5 * Math.cos((Math.PI * (d + 6)) / 11);
      return {...c, u, k: Math.max(0, 1 - Math.abs(d + 0.5) / 6.5)};
    }
  }
  return null;
}

export const Fruta: React.FC = () => {
  const q = useCurrentFrame();
  const i = cenaEm(q);
  const Cena = CENAS[i];
  const ch = chicoteEm(q);
  let conteudo = <Cena q={q} />;
  if (ch) {
    const W = ch.eixo === 'x' ? 1080 : 1920;
    const sai = -ch.dir * ch.u * W;
    const tr = (v: number) => (ch.eixo === 'x' ? `translateX(${v}px)` : `translateY(${v}px)`);
    const Sai = CENAS[cenaEm(ch.q - 1)];
    const Entra = CENAS[cenaEm(ch.q)];
    conteudo = (
      <>
        <AbsoluteFill style={{transform: tr(sai)}}><Sai q={Math.min(q, ch.q - 1)} /></AbsoluteFill>
        <AbsoluteFill style={{transform: tr(sai + ch.dir * W)}}><Entra q={Math.max(q, ch.q)} /></AbsoluteFill>
      </>
    );
  }
  return (
    <AbsoluteFill style={{background: '#14100D'}}>
      <Palco cam={REPOUSO} id="raiz" chicote={ch ? {k: ch.k, eixo: ch.eixo} : null}>
        <AbsoluteFill>{conteudo}</AbsoluteFill>
      </Palco>
      <GraoFilme q={q} forca={0.1} />
      {ESCURAS_PEQUENAS.has(i)
        ? <LegendaPequena q={q} fps={30} blocos={BLOCOS_A} y={1240} />
        : <Pilula q={q} fps={30} blocos={BLOCOS_A} y={1500} tema={CLARAS.has(i) ? 'claro' : 'escuro'} />}
      <SonsFruta />
    </AbsoluteFill>
  );
};
