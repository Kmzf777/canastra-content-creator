// Camada de fonte: o video cru dentro da caixa que o layout mandou.
//
// Duas coisas que esta camada resolve e que ninguem mais resolve:
//
// 1. O CORTE DO AR MORTO. `02 PL.mp4` tem 1,14 s de nada na cabeca. A 30 fps
//    isso e Math.round(1.14 * 30) = 34 frames. Entra por `cortarAntesFrames`,
//    nunca chumbado aqui -- cada projeto tem o seu.
//
// 2. O RECORTE E DECISAO DO LAYOUT, NAO DESTA CAMADA. A caixa vem pronta de
//    `layout()`; aqui so se obedece. `overflow: hidden` existe para que um erro
//    de meio pixel nao vaze para fora da zona, nao para cortar de proposito.
//
// `arquivo` e o NOME do video dentro da subpasta `fonte/` da pasta publica do
// projeto -- so `pl.mp4`, nunca um caminho. Quem sabe o prefixo e esta camada,
// por `SUB.fonte`: a pasta publica de cada projeto e
// `projetos/<projeto>/public/` (gitignorada, pesada), com `fonte/` e `assets/`
// dentro dela. Ver `motor/pasta-publica.ts` para o porque. O render e:
//
//   npx remotion render src/index.ts Reel <saida> \
//     --props=projetos/01-private-label/props.json \
//     --public-dir=projetos/01-private-label/public
//
// O prefixo entra aqui e nao no props.json de proposito: o props.json fala de
// MEDIDA (que arquivo, que razao, que corte), nao de arrumacao de pasta. Mudar
// a convencao de pasta nao deve obrigar a reescrever o props de cada projeto.

import {Video} from '@remotion/media';
import {staticFile} from 'remotion';
import React from 'react';
import type {Caixa} from '../layout';
import {SUB} from '../pasta-publica';

export const Fonte: React.FC<{
  arquivo: string;
  caixa: Caixa;
  cortarAntesFrames: number;
}> = ({arquivo, caixa, cortarAntesFrames}) => (
  <div
    style={{
      position: 'absolute',
      left: caixa.x,
      top: caixa.y,
      width: caixa.largura,
      height: caixa.altura,
      overflow: 'hidden',
    }}
  >
    <Video
      src={staticFile(`${SUB.fonte}/${arquivo}`)}
      trimBefore={cortarAntesFrames}
      objectFit="cover"
      style={{width: '100%', height: '100%'}}
    />
  </div>
);
