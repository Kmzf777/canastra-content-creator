// As pecas de papel da colagem. Cada uma recebe o quadro ABSOLUTO da peca (`q`) e
// o quadro em que comeca (`ini`), e devolve a pose pela gramatica de
// `movimento-colagem.ts`. Nada aqui sorteia: toda variacao vem da semente do nome.
//
// Coordenadas em pixel do quadro 1080x1920, sempre do CENTRO da peca.

import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {COR} from '../identidade/tokens';
import {PILHA} from '../identidade/tipografia';
import {ASSENTAR_QUADROS, assentar, boil, carimbar, progresso, saida} from './movimento-colagem';
import {semente, sorteio} from './semente';

const SOMBRA_PAPEL = 'drop-shadow(0px 8px 10px rgba(10,6,4,0.35))';

export const Campo: React.FC<{cor: string}> = ({cor}) => (
  <AbsoluteFill style={{background: cor}}>
    <Img src={staticFile('colagem/kraft.png')}
      style={{width: '100%', height: '100%', mixBlendMode: 'multiply', opacity: 0.55}} />
  </AbsoluteFill>
);

/** Deslocamento de saida: a peca e "arrancada" do quadro a partir de `fora`. */
function arranque(q: number, fora: number | undefined, chave: string) {
  if (fora === undefined || q < fora) return {dx: 0, dy: 0, rot: 0};
  const t = saida((q - fora) / 8);
  const lado = sorteio(`${chave}#lado`, 0, 1) < 0.5 ? -1 : 1;
  return {dx: lado * 1400 * t * t, dy: -300 * t, rot: lado * 40 * t};
}

export const Recorte: React.FC<{
  q: number; ini: number; nome: string; x: number; y: number; w: number;
  rot?: number; fora?: number; deriva?: [number, number]; semBoil?: boolean;
}> = ({q, ini, nome, x, y, w, rot = 0, fora, deriva = [0, 0], semBoil}) => {
  const p = assentar(q, ini, nome);
  if (!p.visivel) return null;
  const assentou = q >= ini + ASSENTAR_QUADROS;
  const b = assentou && !semBoil ? boil(q, nome) : {variante: 0 as const, rot: 0};
  const a = arranque(q, fora, nome);
  const vivo = Math.max(0, q - ini);
  return (
    <Img
      src={staticFile(`colagem/${nome}-b${b.variante}.png`)}
      style={{
        position: 'absolute', left: x - w / 2, top: y, width: w,
        transform: `translate(${a.dx + deriva[0] * vivo}px, ${p.dy + a.dy + deriva[1] * vivo}px) translateY(-50%) rotate(${rot + p.rot + b.rot + a.rot}deg) scale(${p.escala})`,
        opacity: p.opacidade, filter: SOMBRA_PAPEL,
      }}
    />
  );
};

export const Fita: React.FC<{q: number; ini: number; x: number; y: number; w?: number; rot?: number; chave: string}> =
  ({q, ini, x, y, w = 220, rot = 0, chave}) => {
    if (q < ini) return null;
    const v = q >= ini + 3 ? boil(q, chave).variante : 0;
    const s = 1.12 - 0.12 * progresso(q, ini, ini + 3);
    return (
      <Img src={staticFile(`colagem/fita-b${v}.png`)}
        style={{position: 'absolute', left: x - w / 2, top: y - w * 0.13, width: w,
                transform: `rotate(${rot}deg) scale(${s})`}} />
    );
  };

export const Carimbo: React.FC<{
  q: number; ini: number; x: number; y: number; rot?: number; tamanho?: number;
  cor?: string; fundo?: string; children: React.ReactNode; fora?: number; chave: string;
}> = ({q, ini, x, y, rot = -6, tamanho = 90, cor = COR.acento, fundo = 'transparent', children, fora, chave}) => {
  const c = carimbar(q, ini);
  if (!c.visivel) return null;
  const tremor = q - ini < 2 ? sorteio(`${chave}#t${q}`, -1.2, 1.2) : 0;
  const a = arranque(q, fora, chave);
  return (
    <div style={{
      position: 'absolute', left: x, top: y,
      transform: `translate(-50%,-50%) translate(${a.dx}px,${a.dy}px) rotate(${rot + tremor + a.rot}deg) scale(${c.escala})`,
      border: `${Math.round(tamanho * 0.08)}px solid ${cor}`, color: cor, background: fundo,
      padding: `${tamanho * 0.12}px ${tamanho * 0.28}px`, fontFamily: PILHA.manchete,
      fontSize: tamanho, lineHeight: 1, whiteSpace: 'nowrap', letterSpacing: 1,
    }}>{children}</div>
  );
};

/**
 * Manchete RECORTADA: cada palavra numa tira de papel propria, colada na hora em
 * que e dita. A letra e codigo (Archivo Black); o "recorte" e so a caixa.
 */
export const Manchete: React.FC<{
  q: number; palavras: Array<[string, number]>; x?: number; y: number; tamanho?: number;
  papel?: string; tinta?: string; quebraDepois?: number[]; chave: string; alinhar?: 'centro' | 'esquerda';
}> = ({q, palavras, x = 0, y, tamanho = 120, papel = COR.creme, tinta = COR.terra, quebraDepois = [], chave, alinhar = 'centro'}) => {
  const linhas: Array<Array<[string, number, number]>> = [[]];
  palavras.forEach(([p, ini], i) => {
    linhas[linhas.length - 1].push([p, ini, i]);
    if (quebraDepois.includes(i)) linhas.push([]);
  });
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: y, transform: 'translateY(-50%)',
                 display: 'flex', flexDirection: 'column',
                 alignItems: alinhar === 'centro' ? 'center' : 'flex-start',
                 paddingLeft: alinhar === 'centro' ? 0 : x, gap: tamanho * 0.12}}>
      {linhas.map((l, li) => (
        <div key={li} style={{display: 'flex', gap: tamanho * 0.14}}>
          {l.map(([p, ini, i]) => {
            const pose = assentar(q, ini, `${chave}${i}`);
            const r = sorteio(`${chave}${i}#r`, -2.5, 2.5);
            return (
              <div key={i} style={{
                visibility: pose.visivel ? 'visible' : 'hidden', background: papel, color: tinta,
                fontFamily: PILHA.manchete, fontSize: tamanho, lineHeight: 1,
                padding: `${tamanho * 0.1}px ${tamanho * 0.16}px ${tamanho * 0.04}px`,
                transform: `translateY(${pose.dy}px) rotate(${r + pose.rot * 0.5}deg) scale(${pose.escala})`,
                boxShadow: '0 6px 10px rgba(10,6,4,0.3)', opacity: pose.opacidade,
              }}>{p}</div>
            );
          })}
        </div>
      ))}
    </div>
  );
};

/** Rotulo em mono, sem papel: e o "carimbo de maquina de escrever" da peca. */
export const Rotulo: React.FC<{
  q: number; ini: number; x: number; y: number; texto: string; tamanho?: number; cor?: string;
  centro?: boolean; papel?: string; chave: string;
}> = ({q, ini, x, y, texto, tamanho = 44, cor = COR.creme, centro = true, papel, chave}) => {
  const pose = assentar(q, ini, chave);
  if (!pose.visivel) return null;
  return (
    <div style={{
      position: 'absolute', left: x, top: y,
      transform: `translate(${centro ? '-50%' : '0'},-50%) translateY(${pose.dy * 0.5}px) rotate(${pose.rot * 0.4}deg)`,
      fontFamily: PILHA.dado, fontSize: tamanho, color: cor, letterSpacing: tamanho * 0.08,
      whiteSpace: 'nowrap', opacity: pose.opacidade, background: papel,
      padding: papel ? `${tamanho * 0.25}px ${tamanho * 0.45}px` : 0,
    }}>{texto}</div>
  );
};

/** Gera um contorno rasgado (path SVG) para a borda superior de uma folha. */
function bordaRasgada(chave: string, largura = 1080, amp = 26): string {
  const s = semente(chave);
  let d = `M0,${amp}`;
  for (let x = 0; x <= largura; x += 18) d += ` L${x},${amp * 0.5 + (s() - 0.5) * amp}`;
  return `${d} L${largura},2000 L0,2000 Z`;
}

/**
 * Transicao por COBERTURA: uma folha da cor da proxima cena sobe de baixo, com a
 * borda de cima rasgada, e cobre o quadro em `dur` quadros. Sem corte seco e sem fade.
 */
export const Folha: React.FC<{q: number; ini: number; dur?: number; cor: string; chave: string}> =
  ({q, ini, dur = 9, cor, chave}) => {
    if (q < ini) return null;
    const t = progresso(q, ini, ini + dur);
    const topo = 1960 - 2010 * t;
    return (
      <svg width={1080} height={2000} viewBox="0 0 1080 2000"
        style={{position: 'absolute', left: 0, top: topo, filter: 'drop-shadow(0 -6px 10px rgba(0,0,0,0.3))'}}>
        <path d={bordaRasgada(chave)} fill={cor} />
      </svg>
    );
  };

/** Tira sensorial: papel creme com rotulo e barra que enche na cor de acento. */
export const Tira: React.FC<{q: number; ini: number; y: number; rotulo: string; valor: number; chave: string}> =
  ({q, ini, y, rotulo, valor, chave}) => {
    const pose = assentar(q, ini, chave);
    if (!pose.visivel) return null;
    const enche = progresso(q, ini + 2, ini + 14) * valor;
    const r = sorteio(`${chave}#r`, -1.6, 1.6);
    return (
      <div style={{position: 'absolute', left: 120, width: 840, top: y, height: 112,
                   transform: `translateY(-50%) translateY(${pose.dy}px) rotate(${r + pose.rot * 0.4}deg) scale(${pose.escala})`,
                   background: COR.creme, boxShadow: '0 8px 12px rgba(10,6,4,0.35)',
                   display: 'flex', alignItems: 'center', padding: '0 30px', gap: 28, opacity: pose.opacidade}}>
        <div style={{fontFamily: PILHA.manchete, fontSize: 52, color: COR.terra, width: 300}}>{rotulo}</div>
        <div style={{flex: 1, height: 34, background: '#d9d0bd', position: 'relative'}}>
          <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${enche * 100}%`, background: COR.acento}} />
        </div>
      </div>
    );
  };

/** Embalagem REAL (recorte com laudo). Nenhum filter sobre o PNG: a sombra e um div irmao. */
export const Embalagem: React.FC<{q: number; ini: number; sku: 'classico' | 'suave' | 'canela'; x: number; y: number; h: number; rot?: number}> =
  ({q, ini, sku, x, y, h, rot = 0}) => {
    const p = assentar(q, ini, `emb-${sku}`);
    if (!p.visivel) return null;
    // O PNG publicado esta DEITADO (4096x2304, `giro_para_ficar_em_pe_graus: -90` no
    // laudo). O giro e feito aqui, em CSS: girar 90 graus nao reamostra pixel nenhum.
    const w = h * (2304 / 4096);
    return (
      <div style={{position: 'absolute', left: x - w / 2, top: y - h / 2, width: w, height: h,
                   transform: `translateY(${p.dy}px) rotate(${rot + p.rot * 0.5}deg) scale(${p.escala})`, opacity: p.opacidade}}>
        <div style={{position: 'absolute', left: '8%', right: '8%', bottom: -10, height: 40,
                     background: 'rgba(20,16,13,0.35)', filter: 'blur(14px)', borderRadius: '50%'}} />
        <Img src={staticFile(`assets/${sku}-250g.png`)}
          style={{position: 'absolute', width: h, height: w, left: (w - h) / 2, top: (h - w) / 2,
                  transform: 'rotate(90deg)'}} />
      </div>
    );
  };
