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
import {BLOCOS_A, CENA_INICIO, FIM, TROCA} from './roteiro';
import {SonsEspecial} from './Sons';

export const DURACAO_ESPECIAL = fq(FIM);
const CENAS = [Cena1, Cena2, Cena3, Cena4, Cena5, Cena6, Cena7, Cena8, Cena9];
const LIMITES = CENA_INICIO.map(fq);
/** Tema da pílula por cena: 'escuro' = pílula creme (fundo escuro), 'claro' = pílula terra. */
const TEMA: Array<'claro' | 'escuro'> = ['escuro', 'claro', 'claro', 'escuro', 'escuro', 'claro', 'escuro', 'escuro', 'claro'];

/**
 * Trocas por chicote: quadro da troca, eixo e sentido. As de papel (cobertura) moram nas
 * cenas. As internas (régua, tese, pé, fecho) leem `TROCA`, o mesmo número que a cena usa
 * para mudar de fase — e toda troca de enquadramento tem chicote: o fecho era corte seco
 * do selo a 2,1x para o plano aberto.
 */
export const CHICOTES: Array<{q: number; eixo: 'x' | 'y'; dir: 1 | -1}> = [
  {q: LIMITES[2], eixo: 'x', dir: -1},
  {q: LIMITES[3], eixo: 'y', dir: -1},
  {q: LIMITES[4], eixo: 'x', dir: -1},
  {q: LIMITES[5], eixo: 'y', dir: 1},
  {q: fq(TROCA.regua), eixo: 'y', dir: -1},
  {q: fq(TROCA.tese), eixo: 'x', dir: -1},
  {q: fq(TROCA.pe), eixo: 'y', dir: -1},
  {q: LIMITES[7], eixo: 'y', dir: -1},
  {q: LIMITES[8], eixo: 'x', dir: -1},
  {q: fq(TROCA.fecho), eixo: 'x', dir: 1},
];

/** Índice da cena que vale no quadro x. */
const cenaEm = (x: number) => {
  let i = 0;
  while (i + 1 < LIMITES.length && x >= LIMITES[i + 1]) i++;
  return i;
};

/**
 * Janela do chicote: 12 quadros em volta da troca. `u` vai de 0 a 1 devagar-rápido-
 * devagar (a velocidade máxima cai na troca) e `k` é o borrão, máximo na troca.
 */
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

export const Especial: React.FC = () => {
  const q = useCurrentFrame();
  const i = cenaEm(q);
  const Cena = CENAS[i];
  const ch = chicoteEm(q);
  // No chicote, a imagem que sai e a que entra andam COLADAS, uma tela inteira: antes
  // a cena saía sozinha 520 px e o fundo da raiz aparecia numa faixa preta de até
  // meia tela, nas 10 trocas. Cada lado fica no seu último/primeiro quadro durante a
  // janela — sob 60 px de borrão ninguém vê 5 quadros parados — e assim a troca de
  // fase dentro de uma cena (régua, tese, pé, fecho) também funciona.
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
      <Pilula q={q} fps={FPS} blocos={BLOCOS_A} y={1500} tema={TEMA[i]} />
      <SonsEspecial />
    </AbsoluteFill>
  );
};
