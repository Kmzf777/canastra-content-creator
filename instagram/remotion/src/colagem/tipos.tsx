// As VOZES tipográficas da colagem (sistema B) e a pílula (sistema A).
//
// Medido nas referências do @_victorzk, 07/10/2026, em quadros 1080x1920:
//   Dymo   — caixa grafite ~165 px de altura, texto ~130 px, a CAIXA entra inteira e
//            as letras são datilografadas dentro dela ("DIGI…" aos 6,2 s); em escada.
//   Serifa — itálica solta, sem caixa ("and"), entre as caixas.
//   Marcador — letra de canetão em papel rasgado com borda clara, presa com fita.
//   Recorte — cada letra num papel diferente, entrando uma a uma ("F → Fér → Férias").
//   Pílula — 345x77 px, cinza chapado, texto branco em caixa alta, ~78% da altura,
//            corte seco. Aqui na cor da marca.
//
// Letra é sempre código (proibicoes.md). Todas as entradas andam em passo de
// stop-motion (`posterizar`) — só a câmera é lisa.

import React from 'react';
import {COR} from '../identidade/tokens';
import {PILHA} from '../identidade/tipografia';
import {PILHA_COLAGEM} from './fontes-colagem';
import {assentar, carimbo, esmagar, posterizar} from './movimento-colagem';
import {semente, sorteio} from './semente';
import {blocoNoInstante, type BlocoA} from './legenda';

const SOMBRA = '0 8px 14px rgba(12,8,5,0.38)';

type Pos = {q: number; ini: number; x: number; y: number; rot?: number; ancora?: 'centro' | 'esq' | 'dir'};

const ancorar = (a: Pos['ancora']) => (a === 'esq' ? '0' : a === 'dir' ? '-100%' : '-50%');

/** Etiqueta Dymo: a caixa bate como carimbo; as letras são datilografadas, 1 por quadro. */
export const Dymo: React.FC<Pos & {texto: string; tamanho?: number; fundo?: string; tinta?: string; digitar?: boolean; fora?: number}> = ({
  q, ini, x, y, rot = 0, ancora = 'centro', texto, tamanho = 112, fundo = COR.preto, tinta = COR.creme, digitar = true, fora,
}) => {
  const c = carimbo(posterizar(q, 2, ini), ini);
  if (!c.visivel) return null;
  if (fora !== undefined && q >= fora) return null;
  const n = digitar ? Math.max(0, q - ini - 1) : texto.length;
  return (
    <div style={{
      position: 'absolute', left: x, top: y, whiteSpace: 'nowrap',
      transform: `translate(${ancorar(ancora)}, -50%) rotate(${rot}deg) scale(${c.escala})`,
      background: fundo, color: tinta, fontFamily: PILHA.corpo, fontWeight: 700,
      fontSize: tamanho, lineHeight: 1, letterSpacing: tamanho * -0.01,
      padding: `${tamanho * 0.17}px ${tamanho * 0.27}px ${tamanho * 0.13}px`, boxShadow: SOMBRA,
    }}>
      {texto.split('').map((ch, i) => (
        <span key={i} style={{visibility: i < n ? 'visible' : 'hidden'}}>{ch}</span>
      ))}
    </div>
  );
};

/** Serifa itálica solta: chega esmagada e assenta (squash & stretch), sem caixa. */
export const Serifa: React.FC<Pos & {texto: string; tamanho?: number; cor?: string; fora?: number}> = ({
  q, ini, x, y, rot = 0, ancora = 'centro', texto, tamanho = 150, cor = COR.preto, fora,
}) => {
  const e = esmagar(posterizar(q, 2, ini), ini);
  if (!e.visivel || (fora !== undefined && q >= fora)) return null;
  return (
    <div style={{
      position: 'absolute', left: x, top: y, whiteSpace: 'nowrap',
      transform: `translate(${ancorar(ancora)}, -60%) rotate(${rot}deg) scale(${e.sx}, ${e.sy})`,
      fontFamily: PILHA_COLAGEM.serifa, fontStyle: 'italic', fontSize: tamanho, lineHeight: 1, color: cor,
      textShadow: '0 4px 10px rgba(12,8,5,0.18)',
    }}>{texto}</div>
  );
};

/** Contorno rasgado de um retângulo em %, como clip-path. Semente = a etiqueta. */
function rasgado(chave: string, amp = 3.2, passo = 6): string {
  const s = semente(chave);
  const pts: string[] = [];
  for (let x = 0; x <= 100; x += passo) pts.push(`${x}% ${(s() * amp).toFixed(1)}%`);
  for (let y = 0; y <= 100; y += passo * 2) pts.push(`${100 - s() * amp * 0.6}% ${y}%`);
  for (let x = 100; x >= 0; x -= passo) pts.push(`${x}% ${(100 - s() * amp).toFixed(1)}%`);
  for (let y = 100; y >= 0; y -= passo * 2) pts.push(`${(s() * amp * 0.6).toFixed(1)}% ${y}%`);
  return `polygon(${pts.join(',')})`;
}

/**
 * Etiqueta de marcador em papel rasgado; as letras são "escritas" uma a cada 2 quadros.
 * Com `dur` (quadros), a escrita cabe nesse tempo: a fala de "colheita antes da hora"
 * dura 32 quadros e as 23 letras a 2 por quadro terminavam 0,5 s DEPOIS da voz.
 * Nunca escreve mais devagar que 2 quadros por letra nem mais rápido que 2 letras por quadro.
 */
export const Marcador: React.FC<Pos & {texto: string; tamanho?: number; tinta?: string; papel?: string | null; escrever?: boolean; chave: string; fora?: number; dur?: number}> = ({
  q, ini, x, y, rot, ancora = 'centro', texto, tamanho = 96, tinta = COR.acento, papel = '#F7F2E6', escrever = true, chave, fora, dur,
}) => {
  const qp = posterizar(q, 3, ini);
  const p = assentar(qp, ini, chave);
  if (!p.visivel || (fora !== undefined && q >= fora)) return null;
  const passo = dur ? Math.min(2, Math.max(0.5, dur / texto.length)) : 2;
  const n = escrever ? Math.floor((q - ini) / passo) + 1 : texto.length;
  const r = rot ?? sorteio(`${chave}#rot`, -4, 4);
  return (
    <div style={{
      position: 'absolute', left: x, top: y, whiteSpace: 'nowrap',
      transform: `translate(${ancorar(ancora)}, -50%) translateY(${p.dy}px) rotate(${r + p.rot * 0.4}deg) scale(${p.escala})`,
      opacity: p.opacidade, filter: papel ? 'drop-shadow(0px 8px 12px rgba(12,8,5,0.38))' : undefined,
    }}>
      <div style={{
        background: papel ?? 'transparent', clipPath: papel ? rasgado(chave) : undefined,
        padding: papel ? `${tamanho * 0.22}px ${tamanho * 0.34}px ${tamanho * 0.14}px` : 0,
        fontFamily: PILHA_COLAGEM.marcador, fontSize: tamanho, lineHeight: 1.05, color: tinta,
      }}>
        {texto.split('').map((ch, i) => (
          <span key={i} style={{visibility: i < n ? 'visible' : 'hidden'}}>{ch}</span>
        ))}
      </div>
    </div>
  );
};

const FONTES_RECORTE = [
  {f: PILHA.manchete, w: 400, s: 'normal'},
  {f: PILHA_COLAGEM.serifa, w: 400, s: 'italic'},
  {f: PILHA_COLAGEM.marcador, w: 400, s: 'normal'},
  {f: PILHA.dado, w: 500, s: 'normal'},
  {f: PILHA.corpo, w: 700, s: 'normal'},
] as const;
const PAPEIS = [
  {bg: '#F7F2E6', fg: COR.preto},
  {bg: COR.preto, fg: COR.creme},
  {bg: COR.acento, fg: COR.creme},
  {bg: '#D9C3A0', fg: COR.terra},
  {bg: COR.creme, fg: COR.acento},
];

/** Letras recortadas ("carta de sequestro"): cada caractere num papel, uma a cada 2 quadros. */
export const Recortadas: React.FC<Pos & {texto: string; tamanho?: number; chave: string; intervalo?: number; fora?: number}> = ({
  q, ini, x, y, rot = 0, ancora = 'centro', texto, tamanho = 200, chave, intervalo = 2, fora,
}) => {
  if (q < ini || (fora !== undefined && q >= fora)) return null;
  const s = semente(chave);
  const chars = texto.split('');
  return (
    <div style={{
      position: 'absolute', left: x, top: y, display: 'flex', alignItems: 'center', gap: tamanho * 0.04,
      transform: `translate(${ancorar(ancora)}, -50%) rotate(${rot}deg)`, whiteSpace: 'nowrap',
    }}>
      {chars.map((ch, i) => {
        const fi = Math.floor(s() * FONTES_RECORTE.length);
        const pi = Math.floor(s() * PAPEIS.length);
        const rr = (s() - 0.5) * 14;
        const esc = 0.86 + s() * 0.28;
        const dy = (s() - 0.5) * tamanho * 0.12;
        if (ch === ' ') return <span key={i} style={{width: tamanho * 0.25}} />;
        const ent = ini + i * intervalo;
        const c = carimbo(posterizar(q, 2, ent), ent, 1.18, 4);
        const fonte = FONTES_RECORTE[fi];
        const papel = PAPEIS[pi];
        return (
          <span key={i} style={{
            visibility: c.visivel ? 'visible' : 'hidden', display: 'inline-block',
            background: papel.bg, color: papel.fg, fontFamily: fonte.f, fontWeight: fonte.w, fontStyle: fonte.s,
            fontSize: tamanho * esc, lineHeight: 1, padding: `${tamanho * 0.06}px ${tamanho * 0.08}px`,
            transform: `translateY(${dy}px) rotate(${rr}deg) scale(${c.escala})`, boxShadow: SOMBRA,
            clipPath: rasgado(`${chave}#${i}`, 4, 10),
          }}>{ch}</span>
        );
      })}
    </div>
  );
};

/** Pílula da legenda A: corte seco, na cor da marca, ~78% da altura. */
export const Pilula: React.FC<{q: number; fps: number; blocos: BlocoA[]; y?: number; tema?: 'claro' | 'escuro'}> = ({
  q, fps, blocos, y = 1500, tema = 'claro',
}) => {
  const b = blocoNoInstante(blocos, q / fps);
  if (!b) return null;
  const escuro = tema === 'escuro';
  return (
    <div style={{
      position: 'absolute', left: 540, top: y, transform: 'translate(-50%, -50%)', whiteSpace: 'nowrap',
      background: escuro ? 'rgba(241,236,224,0.92)' : 'rgba(59,42,31,0.86)', color: escuro ? COR.terra : COR.creme,
      fontFamily: PILHA.corpo, fontWeight: 700, fontSize: 46, letterSpacing: 0.5, lineHeight: 1,
      padding: '16px 24px 14px', borderRadius: 12,
    }}>{b.texto}</div>
  );
};
