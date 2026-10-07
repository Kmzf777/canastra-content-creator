// Peça 07 — "o que define um café especial", em colagem.
//
// Raiz: escolhe a cena pelo quadro, aplica o CHICOTE nas trocas (blur direcional de
// verdade + a cena saindo e a próxima entrando pelo lado oposto), e põe por cima de
// tudo o grão de filme e a pílula (legenda A). A colagem (legenda B) mora nas cenas.

import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import '../../colagem/fontes-colagem';
import {REPOUSO} from '../../colagem/camera';
import {Palco} from '../../colagem/palco';
import {Pilula} from '../../colagem/tipos';
import {fq, FPS, GraoFilme} from './apoio';
import {Cena1, Cena2, Cena3, Cena4, Cena5} from './cenas-1';
import {Cena6, Cena7, Cena8, Cena9} from './cenas-2';
import {BLOCOS_A, CENA_INICIO, FIM} from './roteiro';
import {SonsEspecial} from './Sons';

export const DURACAO_ESPECIAL = fq(FIM);
const CENAS = [Cena1, Cena2, Cena3, Cena4, Cena5, Cena6, Cena7, Cena8, Cena9];
const LIMITES = CENA_INICIO.map(fq);
/** Tema da pílula por cena: 'escuro' = pílula creme (fundo escuro), 'claro' = pílula terra. */
const TEMA: Array<'claro' | 'escuro'> = ['escuro', 'claro', 'claro', 'escuro', 'escuro', 'claro', 'escuro', 'escuro', 'claro'];

/** Trocas por chicote: quadro da troca, eixo e sentido. As de papel (cobertura) moram nas cenas. */
const CHICOTES: Array<{q: number; eixo: 'x' | 'y'; dir: 1 | -1}> = [
  {q: LIMITES[2], eixo: 'x', dir: -1},
  {q: LIMITES[3], eixo: 'y', dir: -1},
  {q: LIMITES[4], eixo: 'x', dir: -1},
  {q: LIMITES[5], eixo: 'y', dir: 1},
  {q: fq(43.4), eixo: 'y', dir: -1},
  {q: fq(57.4), eixo: 'x', dir: -1},
  {q: fq(60.9), eixo: 'y', dir: -1},
  {q: LIMITES[7], eixo: 'y', dir: -1},
  {q: LIMITES[8], eixo: 'x', dir: -1},
];

function chicoteEm(q: number): {k: number; eixo: 'x' | 'y'; desloc: number} | null {
  for (const c of CHICOTES) {
    const d = q - c.q;
    if (d >= -6 && d <= 5) {
      const k = 1 - Math.abs(d + 0.5) / 6.5;
      const desloc = d < 0 ? -c.dir * 520 * ((d + 6) / 6) ** 2 : c.dir * 520 * ((5 - d) / 6) ** 2;
      return {k: Math.max(0, k), eixo: c.eixo, desloc};
    }
  }
  return null;
}

export const Especial: React.FC = () => {
  const q = useCurrentFrame();
  let i = 0;
  while (i + 1 < LIMITES.length && q >= LIMITES[i + 1]) i++;
  const Cena = CENAS[i];
  const ch = chicoteEm(q);
  const desl = ch ? (ch.eixo === 'x' ? `translateX(${ch.desloc}px)` : `translateY(${ch.desloc}px)`) : undefined;
  return (
    <AbsoluteFill style={{background: '#14100D'}}>
      <Palco cam={REPOUSO} id="raiz" chicote={ch ? {k: ch.k, eixo: ch.eixo} : null}>
        <AbsoluteFill style={{transform: desl}}>
          <Cena q={q} />
        </AbsoluteFill>
      </Palco>
      <GraoFilme q={q} forca={0.1} />
      <Pilula q={q} fps={FPS} blocos={BLOCOS_A} y={1500} tema={TEMA[i]} />
      <SonsEspecial />
    </AbsoluteFill>
  );
};
