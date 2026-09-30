// Registro das composicoes.
//
// `Reel` e `Feed` sao a MESMA peca (`PecaVideo`) com dimensao diferente. Nao ha
// componente separado para o 1:1 de proposito: a diferenca inteira vive em
// `layout()`, que reenquadra em vez de recortar. Se um dia aparecer um
// componente "PecaFeed", o motor perdeu a propriedade que ele existe para ter.
//
// Numeros medidos em `02 PL.mp4`, nao escolhidos:
//   ar morto na cabeca ... 1,14 s -> Math.round(1.14 * 30) = 34 frames
//   duracao util ......... 24,33 - 1,14 = 23,19 s -> Math.round(23.19 * 30) = 696 frames
//   razao de exibicao .... 576x1024 = 9/16 (o container mente 1024x576; ha
//                          displaymatrix de -90 graus)

import {Composition} from 'remotion';
import React from 'react';
import {PecaVideo} from './PecaVideo';
import type {Props} from './PecaVideo';
import {PonteAssets, PONTE_PADRAO} from './PonteAssets';
import {COR, TIPO} from '../identidade/tokens';
import {PILHA} from '../identidade/tipografia';

const FPS = 30;

// Ar morto medido: 1,14 s.
export const CORTAR_ANTES_FRAMES = Math.round(1.14 * FPS); // 34

// 24,33 s de fonte menos o ar morto.
export const DURACAO_FRAMES = Math.round((24.33 - 1.14) * FPS); // 696

const PADRAO: Props = {
  arquivo: 'pl.mp4',
  razaoFonte: 9 / 16,
  cortarAntesFrames: CORTAR_ANTES_FRAMES,
  // Vazio de proposito: legenda de verdade entra por props.json. Um render sem
  // props sai sem legenda -- visivelmente incompleto, que e melhor que sair com
  // texto de exemplo parecendo pronto.
  blocos: [],
  // `null`, nao um texto de exemplo. A manchete e OPCIONAL (ver o cabecalho de
  // PecaVideo.tsx): a peca sem ela esta completa, nao quebrada. E um placeholder
  // aqui seria a mesma armadilha do `_LEIA` que fez quatro MP4 sairem com
  // legenda inventada queimada no quadro.
  manchete: null,
};

// A composicao de teste tambem desenha texto, entao tambem usa a pilha da
// marca. Ela e a tela mais barata para conferir se a tipografia carregou:
// `remotion still src/index.ts Teste <arq>` sai em segundos e a palavra
// CANASTRA em Archivo Black nao se parece com nada que o Chrome traga de casa.
const Teste: React.FC = () => (
  <div style={{flex: 1, background: '#1a1410', color: COR.creme,
               display: 'flex', alignItems: 'center', justifyContent: 'center',
               fontFamily: PILHA.manchete, fontWeight: TIPO.manchete.peso,
               fontSize: 90}}>CANASTRA</div>
);

export const Raiz: React.FC = () => (
  <>
    <Composition
      id="Reel"
      component={PecaVideo}
      durationInFrames={DURACAO_FRAMES}
      fps={FPS}
      width={1080}
      height={1920}
      defaultProps={PADRAO}
    />
    <Composition
      id="Feed"
      component={PecaVideo}
      durationInFrames={DURACAO_FRAMES}
      fps={FPS}
      width={1080}
      height={1080}
      defaultProps={PADRAO}
    />
    <Composition id="Teste" component={Teste}
      durationInFrames={60} fps={FPS} width={1080} height={1920} />

    {/* Instrumento de conferencia, nao peca: prova que `--public-dir` esta
        apontando para uma pasta que contem `assets/` e que os tres recortes
        carregam. 1 frame porque um still e tudo que ela precisa produzir.
        Formato deitado porque sao tres embalagens em pe lado a lado. */}
    <Composition id="PonteAssets" component={PonteAssets}
      durationInFrames={1} fps={FPS} width={1920} height={1080}
      defaultProps={PONTE_PADRAO} />
  </>
);
