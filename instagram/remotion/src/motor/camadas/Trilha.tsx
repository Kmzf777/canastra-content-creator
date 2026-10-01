// CAMADA DE AUDIO: locucao e trilha. O `<Audio>` que nao existia.
//
// A AUSENCIA QUE ISTO FECHA
//
// Medido em 30/09/2026: `grep -rn "Audio" src/` so achava `motor/audio/normalizar.ts`
// (medicao POS-render) e um comentario prevendo um `<Audio>` futuro. Nao havia nenhum
// na arvore, e todo som era carona do `<Video>`. Consequencia: TODA peca de foto parada
// saia MUDA -- e 5 das 12 series do catalogo partem de foto parada.
//
// E isso nao e questao de gosto: `05-formatos.md` §3 registra, como [oficial], que Reel
// sem audio perde elegibilidade para nao-seguidor. "Mudo" no catalogo significa SEM
// LOCUCAO, nunca sem faixa. A serie 4 e explicitamente "sem voz, COM faixa".
//
// DE ONDE VEM O `Audio`, E POR QUE ISSO IMPORTA
//
// De `@remotion/media`, nao de `remotion`. Medido em `node_modules`:
//   - `remotion/dist/cjs/audio/props.d.ts` NAO declara `loop`; o `Audio` de la estende
//     `React.AudioHTMLAttributes`, onde `loop` e atributo HTML nativo -- compila e pode
//     ser ignorado no render. Seria a licao 3 do CLAUDE.md: parametro aceito e ignorado.
//   - `@remotion/media/dist/audio/props.d.ts` declara `loop?: boolean` no proprio
//     `AudioProps`, ao lado de `trimBefore`, `volume` e `premountFor`.
// `Fonte.tsx` ja importa o `Video` deste mesmo pacote.
//
// E O `loop` AINDA NAO FOI MEDIDO NO EFEITO. O tipo aceitar nao prova que o pipeline
// honra -- lição 3 outra vez. A prova barata e uma peca MAIS LONGA que a faixa com
// `loopar: true`, e `volumedetect` depois do fim da faixa: silencio digital da -91 dB.
// Enquanto essa medicao nao acontecer, `loopar` e promessa, nao garantia.
//
// A NORMALIZACAO NAO E AQUI
//
// `AUDIO = {lufs: -14, picoDbtp: -1}` e alvo de POS-render: quem o aplica e
// `scripts/normalizar-audio.mjs`, com `-c:v copy`, idempotente, sobre a MISTURA.
// `ganhoDb` aqui e RELACAO ENTRE AS FAIXAS -- quanto a trilha fica abaixo da voz --,
// nao nivel absoluto. Mexer nele para "acertar o LUFS" e trabalho perdido, porque a
// normalizacao vem depois e por cima.
//
// FICA FORA DA `TransitionSeries`, no relogio da PECA, pelo mesmo motivo da legenda: a
// faixa nao reinicia porque a imagem trocou.

import {Audio} from '@remotion/media';
import {interpolate, staticFile, useVideoConfig} from 'remotion';
import React from 'react';
import type {Audio as AudioDeclarado, Faixa} from '../../briefing/esquema';
import {emFrames} from '../relogio';
import {SUB} from '../pasta-publica';

/** dB relativo -> ganho linear. `-18 dB` = 0,126; `0 dB` = 1. */
function linear(db: number): number {
  return Math.pow(10, db / 20);
}

const UmaFaixa: React.FC<{
  faixa: Faixa;
  subpasta: string;
  loopar?: boolean;
  fadeEntradaS?: number;
  fadeSaidaS?: number;
  duracaoPecaFrames: number;
}> = ({faixa, subpasta, loopar, fadeEntradaS, fadeSaidaS, duracaoPecaFrames}) => {
  const {fps} = useVideoConfig();
  const ganho = linear(faixa.ganhoDb);
  const entrada = emFrames(fadeEntradaS ?? 0, fps);
  const saida = emFrames(fadeSaidaS ?? 0, fps);

  // `volume` COMO FUNCAO DE FRAME, que `VolumeProp` declara (medido em
  // `remotion/dist/cjs/volume-prop.d.ts`). Sem fade os dois sao 0 e a funcao devolve o
  // ganho constante -- nenhuma rampa por acidente.
  const volume = React.useCallback(
    (frame: number) => {
      const sobe =
        entrada === 0
          ? 1
          : interpolate(frame, [0, entrada], [0, 1], {extrapolateRight: 'clamp'});
      const desce =
        saida === 0
          ? 1
          : interpolate(frame, [duracaoPecaFrames - saida, duracaoPecaFrames], [1, 0], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
      return ganho * Math.min(sobe, desce);
    },
    [entrada, saida, ganho, duracaoPecaFrames],
  );

  return (
    <Audio
      src={staticFile(`${subpasta}/${faixa.arquivo}`)}
      // `aparaAntesS` e APARA: de onde o ARQUIVO comeca a tocar. Ela nunca posiciona
      // nada na peca -- quem posiciona e a ordem das cenas e o relogio da peca.
      trimBefore={emFrames(faixa.aparaAntesS, fps)}
      volume={volume}
      {...(loopar !== undefined ? {loop: loopar} : {})}
      premountFor={fps}
    />
  );
};

export const Trilha: React.FC<{
  audio: AudioDeclarado;
  duracaoPecaFrames: number;
}> = ({audio, duracaoPecaFrames}) => (
  <>
    {audio.locucao ? (
      // LOCUCAO -> `SUB.fonte`. Ela e material cru do projeto e ja esta la: medido,
      // `projetos/01-private-label/public/fonte/` contem `pl.mp4` E `pl.wav`. Zero
      // mudanca de convencao. E ela NAO recebe `loop`: voz repetida nao e faixa, e erro.
      <UmaFaixa
        faixa={audio.locucao}
        subpasta={SUB.fonte}
        duracaoPecaFrames={duracaoPecaFrames}
      />
    ) : null}
    {audio.trilha ? (
      <UmaFaixa
        faixa={audio.trilha}
        subpasta={SUB.audio}
        loopar={audio.trilha.loopar}
        fadeEntradaS={audio.trilha.fadeEntradaS}
        fadeSaidaS={audio.trilha.fadeSaidaS}
        duracaoPecaFrames={duracaoPecaFrames}
      />
    ) : null}
  </>
);
