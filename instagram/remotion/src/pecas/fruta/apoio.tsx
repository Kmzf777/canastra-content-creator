// Peça 08 — o que esta peça tem e a 07 não: VÍDEO REAL no meio da colagem e a
// tipografia cinética em sílabas (a assinatura do @_victorzk: "re / cen / te" entrando
// no tempo da fala, branca e grossa sobre a imagem).
//
// Os clipes em public/fonte/clipes/ já saem TRATADOS (grading + giro + 1080x1920 a
// 30 fps) do passo de preparo; aqui só se escolhe o trecho e a velocidade.

import React from 'react';
import {AbsoluteFill, Freeze, Img, OffthreadVideo, staticFile} from 'remotion';
import {COR} from '../../identidade/tokens';
import {PILHA} from '../../identidade/tipografia';
import {carimbo, posterizar} from '../../colagem/movimento-colagem';
import {blocoNoInstante, type BlocoA} from '../../colagem/legenda';
import {sorteio} from '../../colagem/semente';

export {fq, fala, Fundo, Peca, Fita, Tachinha, SombraFolhas, GraoFilme, Vinheta, Cobertura} from '../especial/apoio';

/** Duração (s) de cada clipe tratado, medida com ffprobe no preparo. */
export const CLIPE_S: Record<string, number> = {v1: 9.23, v2: 9.77, v3: 2.43, v4: 7.63, v5: 20.76, v6: 29.4, v7: 3.8};

/**
 * Trecho de vídeo real. `ini` = quadro da peça em que ele começa; `de` = segundo do
 * clipe que cai nesse quadro; `vel` = velocidade. Freeze + q (não useCurrentFrame):
 * no chicote a cena que sai é desenhada parada no último quadro, e isso só funciona
 * se o vídeo obedecer ao `q` que a raiz passa.
 */
export const Clipe: React.FC<{q: number; ini: number; src: string; de: number; vel?: number; escala?: number; escuro?: number}> = ({
  q, ini, src, de, vel = 1, escala = 1.08, escuro = 0,
}) => {
  const maxQ = Math.floor(CLIPE_S[src] * 30) - 2;
  const qf = Math.min(maxQ, Math.max(0, Math.round(de * 30 + (q - ini) * vel)));
  return (
    <AbsoluteFill style={{transform: `scale(${escala})`}}>
      <Freeze frame={qf}>
        <OffthreadVideo src={staticFile(`fonte/clipes/${src}.mp4`)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </Freeze>
      {escuro > 0 && <AbsoluteFill style={{background: `rgba(10,7,5,${escuro})`}} />}
    </AbsoluteFill>
  );
};

/**
 * Sílabas cinéticas: `texto` com "/" entre as sílabas e "|" para quebrar linha.
 * A palavra dura `dur` quadros e cada sílaba entra num pedaço igual dela, com o
 * carimbo de 4 quadros. Tamanhos alternados, como nas referências.
 */
export const Silabas: React.FC<{
  q: number; ini: number; dur: number; texto: string; x: number; y: number; tamanho?: number;
  cor?: string; rot?: number; fora?: number; chave: string;
}> = ({q, ini, dur, texto, x, y, tamanho = 170, cor = COR.creme, rot = 0, fora, chave}) => {
  if (q < ini || (fora !== undefined && q >= fora)) return null;
  const linhas = texto.split('|').map((l) => l.split('/'));
  const total = linhas.reduce((a, l) => a + l.length, 0);
  // cabe na área segura (x 140–940, lição 55): largura estimada da linha mais longa do
  // Archivo Black (~0,78 em por letra) com o maior sorteio de escala (1,2)
  const maxLetras = Math.max(...linhas.map((l) => l.join('').length));
  const caber = Math.min(1, 760 / (maxLetras * 0.78 * tamanho * 1.2));
  let k = 0;
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%, -50%) rotate(${rot}deg) scale(${caber})`, textAlign: 'center'}}>
      {linhas.map((l, li) => (
        <div key={li} style={{whiteSpace: 'nowrap', lineHeight: 0.92}}>
          {l.map((s, si) => {
            const ent = ini + Math.round((k++ / total) * Math.max(4, dur));
            const c = carimbo(posterizar(q, 2, ent), ent, 1.22, 4);
            const esc = 0.8 + sorteio(`${chave}#${li}#${si}`, 0, 0.4);
            const dy = sorteio(`${chave}#dy${li}#${si}`, -0.08, 0.08) * tamanho;
            return (
              <span key={si} style={{
                display: 'inline-block', visibility: c.visivel ? 'visible' : 'hidden',
                fontFamily: PILHA.manchete, fontSize: tamanho * esc, color: cor, letterSpacing: -tamanho * 0.02,
                transform: `translateY(${dy}px) scale(${c.escala})`,
                textShadow: '0 6px 24px rgba(10,7,5,0.55), 0 2px 4px rgba(10,7,5,0.4)',
              }}>{s}</span>
            );
          })}
        </div>
      ))}
    </div>
  );
};

/** Legenda pequena, centrada, sem caixa: o registro escuro do fim das referências. */
export const LegendaPequena: React.FC<{q: number; fps: number; blocos: BlocoA[]; y?: number}> = ({q, fps, blocos, y = 1180}) => {
  const b = blocoNoInstante(blocos, q / fps);
  if (!b) return null;
  return (
    <div style={{
      position: 'absolute', left: 540, top: y, transform: 'translate(-50%, -50%)', whiteSpace: 'nowrap',
      fontFamily: PILHA.corpo, fontWeight: 500, fontSize: 38, color: 'rgba(241,236,224,0.92)', letterSpacing: 0.5,
      textShadow: '0 2px 10px rgba(0,0,0,0.6)',
    }}>{b.texto.toLowerCase()}</div>
  );
};

/** Foto real (base verificada) em tela cheia, com empurrão lento: o arquivo já sai tratado do preparo. */
export const FotoCheia: React.FC<{q: number; ini: number; dur: number; src: string; z0?: number; z1?: number}> = ({q, ini, dur, src, z0 = 1.0, z1 = 1.1}) => {
  const k = Math.min(1, Math.max(0, (q - ini) / Math.max(1, dur)));
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Img src={staticFile(`fonte/${src}`)} style={{position: 'absolute', left: '50%', top: 0, height: '100%',
        transform: `translateX(-50%) scale(${z0 + (z1 - z0) * k})`, transformOrigin: '50% 40%'}} />
    </AbsoluteFill>
  );
};
