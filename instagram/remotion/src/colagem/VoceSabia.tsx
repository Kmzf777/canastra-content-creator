// Peca 06 -- "Voce sabia" em colagem. Fora do motor por briefing: o esquema dele
// nao tem vocabulario de colagem (spec em docs/superpowers/specs/2026-10-07-...).
//
// Renderiza a cena corrente e, por cima, a seguinte so quando ela ja esta montada
// por baixo da folha de transicao -- ou seja, uma cena por vez.

import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {CENAS, LIMITES} from './cenas';
import {Sons} from './Sons';

export const VoceSabia: React.FC = () => {
  const q = useCurrentFrame();
  let i = 0;
  while (i + 1 < LIMITES.length && q >= LIMITES[i + 1]) i++;
  const Cena = CENAS[i];
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Cena q={q} />
      <Sons />
    </AbsoluteFill>
  );
};
