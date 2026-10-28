// Reel 10 — "chafé: dois erros" (plano v2 + linguagem "sala de prova").
//   - o Rafael sempre na tela: tela cheia, tela dividida (imagem em cima) ou num círculo
//   - câmera 3D honesta: o FUNDO LIMPO real num plano, o texto atrás da cabeça no meio, o Rafael
//     recortado quadro a quadro na frente
//   - linguagem "sala de prova": juta de saca, aço do torrador, papel de laudo; objetos fotográficos;
//     texto em estêncil de spray e carimbo em etiqueta de papel
//
// v2 (28/10/2026), depois da análise quadro a quadro da v1 — as REGRAS DE MOVIMENTO:
//   1. Entrada = 12 q na curva de pouso da marca (TEMPO.pousoEasing), andando no máximo 160 px,
//      com opacidade. Nada de quique, mola ou objeto vindo de fora da tela (proibicoes.md).
//   2. Tudo que aparece fica legível: no mínimo 36 q (1,2 s) cheio na tela. A rajada de defeitos
//      (5 q cada), os cartões da recapitulação (7 q), a lupa que atravessava e o aviãozinho saíram.
//   3. Sincronia: a entrada começa LEAD quadros antes da palavra e o som cai no quadro em que o
//      objeto assenta. Visual e som leem os MESMOS quadros (objeto E).
//   4. Câmera calma: push lento + deriva de 0,3; pulso só nas batidas (chafé, duas, erro 2, de
//      propósito, chafé final). Nada de chicote com borrão: troca de cena é corte seco que assenta.
//   5. Corte da fonte dentro de uma cena vira "punch" (a moldura alterna 1,00 ↔ 1,10), não flip.
//   6. Texto: creme com sombra sobre fundo escuro, preto com halo sobre fundo claro; carimbo é tinta
//      em etiqueta de papel (contraste em qualquer fundo). Nada de laranja sobre juta ou aço.
//   7. Painel nunca chega vazio: o primeiro objeto já vem com ele.

import {Audio} from '@remotion/media';
import React from 'react';
import {AbsoluteFill, Img, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {COR} from '../../identidade/tokens';
import {PILHA} from '../../identidade/tipografia';
import {POUSO} from '../../motor/movimento';
import {cameraEm, deriva, pulso, somar, tremor, type Cam, type Chave} from '../../colagem/camera';
import {Palco, Plano} from '../../colagem/palco';
import {blocoNoInstante, type Faixa} from '../../colagem/legenda';
import {fq} from '../especial/apoio';
import {ate, BLOCOS_A, em, FIM, S1, S1B, S2A, S2B, S2D, S2E, S3A, S3B, S3C, S3D, S3E, S4A, S4B, S5A, S5B, S5C} from './roteiro';

const F = fq;
export const DURACAO_CHAFE = F(FIM);
const W = (f: {inicio: number}) => F(f.inicio);
const wd = (f: Faixa, p: string, n = 1) => F(em(f, p, n));
const cl = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const prog = (q: number, a: number, b: number) => cl((q - a) / Math.max(1, b - a));
const inOut = (t: number) => {const u = cl(t); return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;};

// ------------------------------------------------------------------ regras de tempo
const LEAD = 4; // a entrada começa 4 q antes da palavra: assenta ~4 q depois dela
const ENTRA = 12; // TEMPO.entradaS (0,4 s)
const SAI = 10;
const LEITURA = 36; // mínimo cheio na tela
const ent = (palavra: number) => palavra - LEAD;
const segura = (ini: number, f: Faixa) => Math.max(F(ate(f)), ini + LEITURA);
/** 0 → 1 na curva de pouso, a partir de `ini`. */
const pres = (q: number, ini: number, n = ENTRA) => POUSO(cl((q - ini + 1) / n));
/** 0 → 1 acelerando (t^2,4), a partir de `fora`. */
const saida = (q: number, fora?: number) => (fora === undefined || q < fora ? 0 : Math.pow(cl((q - fora + 1) / SAI), 2.4));

// ------------------------------------------------------------------ fronteiras (quadros)
const T = {
  split1: F(6.88), circ1: F(13.84), split1b: F(16.45), escuro: F(19.05), aco: F(22.16),
  solta: F(24.91), circ2: F(26.18), close2: F(32.17), rasgo: F(35.23), split3: F(37.41),
  receita: F(45.64), cheio4: F(51.15), fecho: F(53.84),
};
/** Cortes da fonte (corte-seco-v2.json) que caem DENTRO de uma cena: a moldura alterna. */
const PUNCH = [5.09, 9.8, 26.71, 27.55, 28.28, 29.31, 38.12, 41.2, 43.66, 50.0, 55.3].map(F);

// ------------------------------------------------------------------ quadros de cada elemento
// Visual e som leem daqui: é isso que mantém os dois juntos.
const E = {
  // 0 · gancho
  chafe: ent(W(S1.chafe)), errou: wd(S1.essa, 'errou'), chafeSai: F(ate(S1.chafe)) + 6, duas: W(S1.duas) - 1,
  rafael: ent(W(S1B.rafael)), canastra: ent(W(S1B.canastra)), corte: F(5.09), torref: ent(W(S1B.torrefacao)), xicaraSai: ent(W(S1B.eu)),
  // 1 · erro 1
  erro1: ent(W(S2A.primeiro)), cafe1: ent(wd(S2A.achar, 'café')), clarinho: ent(W(S2A.clarinho)), fraco: ent(W(S2A.fraco)), risca: W(S2A.fraco) + 8,
  desliza: F(9.8) - 2, torra: ent(wd(S2B.torra, 'torra')), intensidade: ent(W(S2B.intensidade)), sim: wd(S2B.sim, 'sim'),
  passar: wd(S2B.passar, 'passar'), ponto: wd(S2B.passar, 'ponto'), intenso: ent(W(S2B.intenso)),
  coloca1: ent(wd(S2D.quer, 'coloca')), pouq1: wd(S2D.quer, 'pouquinho'), maisPo1: ent(wd(S2D.quer, 'mais', 2)), po1: W(S2D.po),
  intensifica: ent(W(S2E.intensifica)), sabor: ent(wd(S2E.sabor, 'sabor')), todo: wd(S2E.sabor, 'todo'),
  // 2 · erro 2
  erro2: ent(W(S3A.segundo)), erro2Troca: wd(S3A.segundo, 'erro'), quase: ent(W(S3A.quase)), erro2Sai: W(S3A.quase) + 20,
  extra: ent(W(S3B.muito)), passa: wd(S3B.passa, 'passa'), ponto2: wd(S3B.passa, 'ponto'), proposito: wd(S3B.proposito, 'propósito') - 1,
  defeito: ent(W(S3C.defeito)), preto: ent(W(S3C.preto)), ardido: ent(W(S3C.ardido)), broca: ent(W(S3C.broca)),
  passando: W(S3D.passando), tudo: ent(wd(S3D.passando, 'tudo')), amargo: ent(W(S3D.amargo)), some: W(S3D.some) - 1,
  caneca: ent(wd(S3E.dai, 'coloca')), acucar: ent(W(S3E.acucar)),
  cubos: [W(S3E.acucar), wd(S3E.aguentar, 'aguentar'), wd(S3E.aguentar, 'tomar')].map((p) => p - 8),
  // 3 · o nosso
  nada: ent(W(S4A.nada)), marrom: ent(W(S4A.marrom)), media: W(S4B.media) - 1, luz: ent(wd(S4B.luz, 'luz')), atravessa: wd(S4B.luz, 'atravessa'),
  gosto: wd(S4B.luz, 'gosto'), chocolate: ent(W(S4B.chocolate)), azedinho: ent(W(S4B.azedinho)), fruta: ent(wd(S4B.azedinho, 'fruta')),
  // 4 · a receita
  logo4: wd(S5A.aqui, 'canastra'), balanca: ent(wd(S5A.aqui, 'conta')), cinquenta: ent(W(S5A.cinquenta)), filtro4: ent(wd(S5A.de, 'pó')),
  jarra: ent(W(S5A.meio)), ml: W(S5A.meio) - 1, agua: wd(S5A.meio, "'água."),
  erro1b: W(S5B.primeiro) - 1, dosador4b: ent(wd(S5B.coloca, 'coloca')), pouq4b: wd(S5B.coloca, 'pouquinho'), maisPo4b: ent(wd(S5B.coloca, 'mais')),
  // 5 · fecho
  manda: ent(W(S5C.manda)), xicara5: ent(wd(S5C.que, 'isso')), chafe5: ent(W(S5C.chafe)),
};
const CONGELA_Q = E.proposito + 5; // congela com o carimbo já assentado

// ------------------------------------------------------------------ filtros (spray e tinta)
const Defs: React.FC = () => (
  <svg width={0} height={0} style={{position: 'absolute'}}>
    <filter id="spray" x="-5%" y="-20%" width="110%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="n" />
      <feDisplacementMap in="SourceGraphic" in2="n" scale="3" xChannelSelector="R" yChannelSelector="G" result="d" />
      <feGaussianBlur in="d" stdDeviation="0.4" />
    </filter>
    {/* tinta: só grão fino (falhas pequenas), nunca mancha que apaga letra inteira */}
    <filter id="tinta" x="-5%" y="-20%" width="110%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves="2" seed="3" result="n" />
      <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.3 1.8" result="m" />
      <feComposite in="SourceGraphic" in2="m" operator="in" />
    </filter>
  </svg>
);

// ------------------------------------------------------------------ o Rafael (3 planos)
/** Quadro do corte v2 que o Rafael mostra (no congelado de "de propósito", fica parado). */
const quadroRafael = (q: number) => (q >= CONGELA_Q && q < T.solta ? CONGELA_Q : q);
const ULTIMO_QUADRO = 1763; // 1737+ vêm do bruto (extensão do fim, mesmo grade)

/** Fundo limpo (p 0,96) + o que vai atrás da cabeça (p 0,98) + o Rafael recortado (p 1). */
const Rafael: React.FC<{q: number; cam: Cam; escuro?: number; claro?: number; atras?: React.ReactNode; parede?: React.ReactNode; id: string}> = ({
  q, cam, escuro = 0, claro = 0, atras, parede, id,
}) => {
  const qr = cl(quadroRafael(q), 0, ULTIMO_QUADRO);
  const filtro = escuro > 0 ? `brightness(${1 - 0.76 * escuro}) saturate(${1 - 0.5 * escuro})` : claro > 0 ? `brightness(${1 + 0.1 * claro}) saturate(${1 - 0.25 * claro})` : undefined;
  return (
    <AbsoluteFill>
      <Palco cam={cam} id={id}>
        <Plano p={0.96}>
          <Img src={staticFile('fonte/fundo-limpo.png')} style={{position: 'absolute', left: -54, top: -96, width: 1188, height: 2112, filter: filtro}} />
          {claro > 0 && <div style={{position: 'absolute', left: -54, top: -96, width: 1188, height: 2112, background: '#EFE7D8', opacity: 0.22 * claro}} />}
          {parede}
        </Plano>
        {atras && <Plano p={0.98}>{atras}</Plano>}
        <Plano p={1}>
          <Img src={staticFile(`fonte/recorte/${String(qr).padStart(5, '0')}.png`)} style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920}} />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};
/** Câmera do Rafael: push linear de z a z+0,04 na cena, deriva leve, e o punch nos cortes da fonte. */
const camR = (q: number, ini: number, fim: number, z: number, id: string, y = -20, extras: Cam[] = []): Cam => {
  const n = PUNCH.filter((p) => p > ini && p <= q).length;
  const t = prog(q, ini, fim);
  return somar({x: 0, y: y * t, zoom: z + 0.04 * t + (n % 2 ? 0.1 : 0), rot: 0}, deriva(q, id, 0.3), ...extras);
};

/** Metade de baixo da tela com o Rafael (o rosto, em y 790 no quadro cheio, fica no meio). */
const Metade: React.FC<{children: React.ReactNode; topo?: number}> = ({children, topo = 900}) => (
  <div style={{position: 'absolute', left: 0, top: topo, width: 1080, height: 1920 - topo, overflow: 'hidden'}}>
    <div style={{position: 'absolute', left: 0, top: (1920 - topo) / 2 - 790, width: 1080, height: 1920}}>{children}</div>
  </div>
);
/** Rafael num círculo; abre em 12 q na curva de pouso a partir de `ini`. */
const Circulo: React.FC<{children: React.ReactNode; q: number; ini: number; cx?: number; cy?: number; d?: number}> = ({children, q, ini, cx = 850, cy = 1600, d: d1 = 360}) => {
  const d = d1 * (0.7 + 0.3 * pres(q, ini));
  const s = 0.46 * (d / 400);
  return (
    <div style={{position: 'absolute', left: cx - d / 2, top: cy - d / 2, width: d, height: d, borderRadius: '50%', overflow: 'hidden', opacity: cl((q - ini + 1) / 3),
      border: `7px solid ${COR.creme}`, boxShadow: '0 16px 30px rgba(8,5,3,0.5)', background: COR.preto}}>
      <div style={{position: 'absolute', left: d / 2 - 540 * s, top: d / 2 - 790 * s, width: 1080, height: 1920, transform: `scale(${s})`, transformOrigin: '0 0'}}>{children}</div>
    </div>
  );
};

// ------------------------------------------------------------------ fundos dos painéis
type Mat = 'juta' | 'aco' | 'laudo';
const Fundo: React.FC<{mat: Mat; h?: number}> = ({mat, h = 900}) => {
  if (mat === 'laudo') {
    return (
      <div style={{position: 'absolute', left: -110, top: -100, width: 1300, height: h + 200, background: '#EEE7D9'}}>
        <svg width={1300} height={h + 200} style={{position: 'absolute', left: 0, top: 0}}>
          <defs><pattern id="grade" width={36} height={36} patternUnits="userSpaceOnUse"><path d="M36 0 L0 0 0 36" fill="none" stroke="#C9BFAE" strokeWidth={1} /></pattern></defs>
          <rect width="100%" height="100%" fill="url(#grade)" opacity={0.6} />
        </svg>
      </div>
    );
  }
  return (
    <Img src={staticFile(`colagem/r10-${mat}.jpg`)} style={{position: 'absolute', left: -120, top: -120, width: 1320, height: h + 240, objectFit: 'cover',
      filter: mat === 'juta' ? 'saturate(0.9) brightness(0.92)' : undefined}} />
  );
};
/** Painel de cima (900 px) com câmera própria; desce do topo em 14 q a partir de `ini`. */
const Painel: React.FC<{q: number; ini: number; mat: Mat; cam: Cam; id: string; children: React.ReactNode}> = ({q, ini, mat, cam, id, children}) => (
  <div style={{position: 'absolute', left: 0, top: -900 * (1 - pres(q, ini, 14)), width: 1080, height: 900, overflow: 'hidden', boxShadow: '0 10px 26px rgba(0,0,0,0.55)'}}>
    <Palco cam={cam} id={id}>
      <Plano p={0.7}><Fundo mat={mat} /></Plano>
      <Plano p={1}>{children}</Plano>
    </Palco>
    <div style={{position: 'absolute', left: 0, bottom: 0, width: 1080, height: 6, background: COR.preto, opacity: 0.8}} />
  </div>
);
/** Câmera do painel: push lento e deriva leve. Sem pulso. */
const camP = (q: number, ini: number, id: string): Cam =>
  somar(cameraEm(q - ini, [{q: 0, x: 0, y: 0, zoom: 1.02, rot: 0}, {q: 150, x: 8, y: -10, zoom: 1.06, rot: -0.2, curva: 'linear'}] as Chave[]), deriva(q, id, 0.3));

// ------------------------------------------------------------------ objetos
type Entrada = 'cai' | 'dir' | 'esq' | 'sobe' | 'surge';
const SOMBRA_OBJ = 'drop-shadow(0px 18px 20px rgba(10,7,5,0.48))';
/** Objeto fotográfico (colagem/r10-<nome>.png), centrado em (x, y). Entra andando ≤160 px na curva de pouso. */
const Obj: React.FC<{q: number; ini: number; nome: string; x: number; y: number; w: number; rot?: number; entra?: Entrada; fora?: number;
  saiPara?: 'esq' | 'dir' | 'cima' | 'baixo'; extraRot?: number; filtro?: string}> = ({q, ini, nome, x, y, w, rot = 0, entra = 'surge', fora, saiPara = 'esq', extraRot = 0, filtro}) => {
  if (q < ini) return null;
  const s = saida(q, fora);
  if (s >= 1) return null;
  const e = pres(q, ini);
  let dx = 0, dy = 0, sc = 1, r = rot;
  if (entra === 'cai') {dy = -120 * (1 - e); r += 5 * (1 - e);}
  else if (entra === 'dir') {dx = 160 * (1 - e); r += 4 * (1 - e);}
  else if (entra === 'esq') {dx = -160 * (1 - e); r -= 4 * (1 - e);}
  else if (entra === 'sobe') dy = 140 * (1 - e);
  else sc = 0.94 + 0.06 * e;
  if (s > 0) {const d = 90 * s; if (saiPara === 'esq') dx -= d; else if (saiPara === 'dir') dx += d; else if (saiPara === 'cima') dy -= d; else dy += d;}
  return (
    <Img src={staticFile(`colagem/r10-${nome}.png`)} style={{position: 'absolute', left: x - w / 2, top: y, width: w, opacity: cl(e * 1.6) * (1 - s),
      transform: `translate(${dx}px, ${dy}px) translateY(-50%) rotate(${r + extraRot}deg) scale(${sc})`, filter: filtro ? `${filtro} ${SOMBRA_OBJ}` : SOMBRA_OBJ}} />
  );
};
/** Inclinação de servir (dosador): desce de 0 a −32° em 10 q a partir de `a` e volta a partir de `b`. */
const inclina = (q: number, a: number, b: number) => -32 * inOut(prog(q, a, a + 10)) * (1 - inOut(prog(q, b, b + 10)));

// ------------------------------------------------------------------ texto: estêncil e carimbo
/** Estêncil de spray: revela da esquerda para a direita em 8 q na curva de pouso. */
const Estencil: React.FC<{q: number; ini: number; texto: string; x: number; y: number; tam?: number; cor?: string; rot?: number; fora?: number; largura?: number}> = ({
  q, ini, texto, x, y, tam = 150, cor = COR.creme, rot = -2, fora, largura = 1000,
}) => {
  if (q < ini) return null;
  const s = saida(q, fora);
  if (s >= 1) return null;
  const rev = pres(q, ini, 8);
  const claro = cor === COR.creme;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: largura, transform: `translate(-50%,-50%) rotate(${rot}deg) scale(${1 + 0.03 * s})`, opacity: 1 - s,
      clipPath: `inset(-30% ${100 - rev * 100}% -30% -3%)`, textAlign: 'center'}}>
      <div style={{fontFamily: PILHA.manchete, fontSize: tam, lineHeight: 1.0, color: cor, letterSpacing: tam * 0.02, whiteSpace: 'pre-line', filter: 'url(#spray)',
        textShadow: claro ? '0 4px 0 rgba(10,7,5,0.5), 0 10px 26px rgba(10,7,5,0.6)' : '0 0 22px rgba(243,237,225,0.95), 0 0 6px rgba(243,237,225,0.8)'}}>{texto}</div>
    </div>
  );
};

/** Carimbo: tinta numa etiqueta de papel (ou direto no papel do laudo). Pousa de 1,12 a 1,00 em 5 q. */
const Carimbo: React.FC<{q: number; ini: number; texto: string; x: number; y: number; tam?: number; cor?: string; rot?: number; fora?: number; papel?: boolean}> = ({
  q, ini, texto, x, y, tam = 64, cor = COR.acento, rot = -5, fora, papel = true,
}) => {
  if (q < ini) return null;
  const s = saida(q, fora);
  if (s >= 1) return null;
  const sc = (1.12 - 0.12 * pres(q, ini, 5)) * (1 - 0.03 * s);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) rotate(${rot}deg) scale(${sc})`, opacity: cl((q - ini + 1) / 2) * (1 - s)}}>
      <div style={papel ? {background: '#F3EDE1', padding: `${tam * 0.2}px ${tam * 0.26}px`, boxShadow: '0 12px 24px rgba(8,5,3,0.45)'} : undefined}>
        <div style={{border: `${Math.max(4, tam * 0.08)}px solid ${cor}`, padding: `${tam * 0.16}px ${tam * 0.28}px ${tam * 0.1}px`, fontFamily: PILHA.manchete, fontSize: tam,
          lineHeight: 1, letterSpacing: tam * 0.04, color: cor, whiteSpace: 'nowrap', filter: 'url(#tinta)'}}>{texto}</div>
      </div>
    </div>
  );
};

/** Tag do capítulo (canto superior esquerdo): plaqueta escura, legível sobre qualquer fundo. */
const Capitulo: React.FC<{q: number; n: number; desde?: number}> = ({q, n, desde}) => {
  const t = desde === undefined ? 1 : pres(q, desde, 6);
  return (
    <div style={{position: 'absolute', left: 48, top: 150, transform: `scale(${1.08 - 0.08 * t})`, transformOrigin: 'left top', opacity: desde === undefined ? 1 : cl((q - desde + 1) / 3),
      background: 'rgba(20,16,13,0.86)', padding: '12px 22px 9px', fontFamily: PILHA.dado, fontWeight: 500, fontSize: 40, letterSpacing: 5, color: COR.creme,
      boxShadow: '0 6px 16px rgba(0,0,0,0.35)'}}>
      ERRO <span style={{color: '#E58A3C'}}>{n}</span>
    </div>
  );
};

/** Manômetro do torrador (foto gerada) com ponteiro e marca PONTO desenhados (0 = esquerda, 1 = direita). */
const Manometro: React.FC<{q: number; ini: number; x: number; y: number; w: number; valor: number; treme?: number}> = ({q, ini, x, y, w, valor, treme = 0}) => {
  if (q < ini) return null;
  const e = pres(q, ini);
  const ang = -90 + cl(valor, 0, 1.06) * 180 + treme * Math.sin(q * 1.7);
  const cx = w * 0.5, cy = w * 0.505, L = w * 0.34;
  const am = ((-90 + 0.55 * 180) * Math.PI) / 180;
  return (
    <div style={{position: 'absolute', left: x - w / 2, top: y - w / 2, width: w, height: w, opacity: cl(e * 1.6), transform: `scale(${0.94 + 0.06 * e})`, filter: SOMBRA_OBJ}}>
      <Img src={staticFile('colagem/r10-manometro.png')} style={{width: w, height: w, objectFit: 'contain'}} />
      <svg width={w} height={w} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
        <line x1={cx + Math.sin(am) * L * 0.62} y1={cy - Math.cos(am) * L * 0.62} x2={cx + Math.sin(am) * L * 1.04} y2={cy - Math.cos(am) * L * 1.04} stroke={COR.acento} strokeWidth={w * 0.026} />
        <text x={cx + Math.sin(am) * L * 0.46} y={cy - Math.cos(am) * L * 0.46 + w * 0.02} textAnchor="middle" fontFamily={PILHA.manchete} fontSize={w * 0.06} fill={COR.acento}>PONTO</text>
        <g transform={`rotate(${ang} ${cx} ${cy})`}>
          <path d={`M${cx - w * 0.016},${cy} L${cx},${cy - L} L${cx + w * 0.016},${cy} Z`} fill="#1B1714" />
        </g>
        <circle cx={cx} cy={cy} r={w * 0.04} fill="#1B1714" />
        <circle cx={cx} cy={cy} r={w * 0.015} fill="#9A948C" />
      </svg>
    </div>
  );
};

/** Legenda: creme, sombra forte, sem caixa; some quando há palavra-chave. */
const Legenda: React.FC<{q: number; y: number}> = ({q, y}) => {
  const b = blocoNoInstante(BLOCOS_A, q / 30);
  if (!b) return null;
  return (
    <div style={{position: 'absolute', left: 540, top: y, transform: 'translate(-50%,-50%)', whiteSpace: 'nowrap', fontFamily: PILHA.corpo, fontWeight: 700,
      fontSize: 62, color: COR.creme, letterSpacing: 0.5, textShadow: '0 3px 0 rgba(10,7,5,0.9), 0 8px 22px rgba(10,7,5,0.75)'}}>{b.texto}</div>
  );
};

/** Traço de spray (risco, seta, check) que se desenha em `dur` quadros na curva de pouso. */
const Traco: React.FC<{q: number; ini: number; d: string; cor?: string; esp?: number; dur?: number; fora?: number; comp?: number}> = ({q, ini, d, cor = COR.acento, esp = 16, dur = 10, fora, comp = 1400}) => {
  if (q < ini) return null;
  const s = saida(q, fora);
  if (s >= 1) return null;
  const t = pres(q, ini, dur);
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', opacity: 1 - s}}>
      <path d={d} fill="none" stroke={cor} strokeWidth={esp} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={comp} strokeDashoffset={comp * (1 - t)} filter="url(#spray)" />
    </svg>
  );
};

/** Pó caindo do dosador: 22 grãos com gravidade, 24 q a partir de `ini`. */
const Po: React.FC<{q: number; ini: number; x: number; y: number; ate: number}> = ({q, ini, x, y, ate: yFim}) => {
  const k = q - ini;
  if (k < 0 || k > 26) return null;
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
      {Array.from({length: 22}, (_, i) => {
        const t = k - (i % 11) * 1.1;
        if (t < 0) return null;
        const yy = y + 3.2 * t * t + (i % 4) * 4;
        if (yy > yFim) return null;
        const xx = x + ((i * 37) % 40) - 20 + t * ((i % 3) - 1) * 0.8;
        return <circle key={i} cx={xx} cy={yy} r={3 + (i % 3)} fill="#3A2A1E" />;
      })}
    </svg>
  );
};

/** Cubo de açúcar: aparece acima da caneca, cai em 10 q (gravidade) e afunda em 6 q. */
const Cubo: React.FC<{q: number; ini: number; nome: string; x: number; y0: number; y1: number; w: number; rot: number}> = ({q, ini, nome, x, y0, y1, w, rot}) => {
  const k = q - ini;
  if (k < 0 || k > 16) return null;
  const t = cl(k / 10);
  const afunda = cl((k - 10) / 6);
  return (
    <Img src={staticFile(`colagem/r10-${nome}.png`)} style={{position: 'absolute', left: x - w / 2, top: y0 + (y1 - y0) * t * t - w / 2, width: w,
      opacity: cl((k + 1) / 3) * (1 - afunda), transform: `rotate(${rot + 14 * t}deg) scale(${1 - 0.35 * afunda})`, filter: SOMBRA_OBJ}} />
  );
};

// ------------------------------------------------------------------ CENAS
type P = {q: number};

// 0 · gancho (0 → 6,88): tela cheia, fundo real
const C0: React.FC<P> = ({q}) => {
  const ch = W(S1.chafe), du = W(S1.duas);
  const cam = camR(q, 0, T.split1, 1.08, 'r0', -24, [pulso(q, [ch, du], 0.03), tremor(q, du, 6, 3)]);
  const atras = (
    <>
      <Estencil q={q} ini={E.chafe} texto="CHAFÉ?" x={540} y={460} tam={196} rot={-3} fora={E.chafeSai} />
      <Traco q={q} ini={E.errou} d="M150,480 C400,440 700,520 940,450" esp={22} dur={10} fora={E.chafeSai} />
    </>
  );
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Rafael q={q} cam={cam} atras={atras} id="r0" />
      {/* na frente, ao lado da cabeça (para onde ele aponta): na parede o punch dos 5 s a cortava */}
      <Carimbo q={q} ini={E.torref} texto="TORREFAÇÃO" x={200} y={520} tam={32} cor={COR.terra} rot={-4} />
      <Obj q={q} ini={-ENTRA} nome="xicara" x={190} y={1530} w={230} rot={-6} fora={E.xicaraSai} saiPara="esq" />
      <Carimbo q={q} ini={E.duas} texto="2 ERROS" x={330} y={1180} tam={70} cor={COR.acento} rot={-6} fora={E.rafael - 10} />
      {/* faixa de saca com o nome: entra no "Rafael", logo no "Café Canastra", sai no corte da fonte */}
      {q >= E.rafael && q < E.corte + SAI && (() => {
        const e = pres(q, E.rafael), s = saida(q, E.corte);
        return (
          <div style={{position: 'absolute', left: 70 - 160 * (1 - e) - 90 * s, top: 1105, width: 720, height: 150, overflow: 'hidden', transform: 'rotate(-2deg)',
            opacity: cl(e * 1.6) * (1 - s), boxShadow: '0 14px 26px rgba(0,0,0,0.5)'}}>
            <Img src={staticFile('colagem/r10-juta.jpg')} style={{position: 'absolute', left: -200, top: -300, width: 1100, filter: 'brightness(0.5) saturate(0.9)'}} />
            <div style={{position: 'absolute', left: 44, top: 0, height: 150, display: 'flex', alignItems: 'center', fontFamily: PILHA.manchete, fontSize: 70, color: COR.creme,
              letterSpacing: 2, textShadow: '0 3px 8px rgba(0,0,0,0.5)'}}>RAFAEL</div>
            {q >= E.canastra && <Img src={staticFile('fonte/logo-branca.png')} style={{position: 'absolute', left: 430, top: 22, height: 106, opacity: pres(q, E.canastra, 8)}} />}
          </div>
        );
      })()}
    </AbsoluteFill>
  );
};

// 1 · erro 1 (6,88 → 13,84): tela dividida com juta; o painel desliza para a segunda tela no corte da fonte
const C1: React.FC<P> = ({q}) => {
  const des = -1100 * pres(q, E.desliza, 14);
  const valor = 0.2 + 0.18 * pres(q, E.intensidade + LEAD, 14) + 0.17 * inOut(prog(q, E.passar, E.ponto + 4));
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Metade><Rafael q={q} cam={camR(q, T.split1, T.circ1, 1.0, 'r1')} id="r1" /></Metade>
      <Painel q={q} ini={T.split1} mat="juta" cam={camP(q, T.split1, 'p1')} id="p1">
        {des > -1100 && (
          <div style={{position: 'absolute', inset: 0, transform: `translateX(${des}px)`}}>
            <Estencil q={q} ini={E.erro1} texto="ERRO 1" x={540} y={430} tam={200} rot={-3} fora={E.cafe1} />
            <Obj q={q} ini={E.cafe1} nome="xicara" x={280} y={520} w={300} rot={-3} entra="esq" />
            <Estencil q={q} ini={E.clarinho} texto="CLARINHO" x={720} y={440} tam={92} rot={-3} largura={620} />
            <Estencil q={q} ini={E.fraco} texto="= FRACO?" x={720} y={580} tam={92} rot={-2} largura={620} />
            <Traco q={q} ini={E.risca} d="M470,600 L975,560" esp={18} dur={8} />
          </div>
        )}
        {q >= E.desliza && (
          <div style={{position: 'absolute', inset: 0, transform: `translateX(${1100 + des}px)`}}>
            <Estencil q={q} ini={E.torra} texto="TORRA →" x={300} y={330} tam={90} rot={-3} largura={540} />
            <Estencil q={q} ini={E.intensidade} texto="INTENSIDADE" x={300} y={450} tam={58} rot={-3} largura={540} />
            <Manometro q={q} ini={E.desliza} x={770} y={450} w={420} valor={valor} />
            <Traco q={q} ini={E.sim} d="M150,560 L200,610 L300,500" cor={COR.creme} esp={16} dur={8} />
            <Estencil q={q} ini={E.intenso} texto="INTENSO" x={540} y={780} tam={120} rot={-2} />
          </div>
        )}
      </Painel>
      {q >= E.cafe1 && <Capitulo q={q} n={1} desde={E.cafe1} />}
    </AbsoluteFill>
  );
};

// 1b · o pó (13,84 → 16,45): juta em tela cheia, Rafael no círculo
const C1b: React.FC<P> = ({q}) => {
  const camC = somar(cameraEm(q - T.circ1, [{q: 0, x: 0, y: 0, zoom: 1.03, rot: 0}, {q: 80, x: 6, y: -16, zoom: 1.07, rot: -0.2, curva: 'linear'}] as Chave[]), deriva(q, 'c1b', 0.3));
  return (
    <AbsoluteFill style={{background: '#8A6A47'}}>
      <Palco cam={camC} id="c1b">
        <Plano p={0.7}><Fundo mat="juta" h={1920} /></Plano>
        <Plano p={1}>
          <Obj q={q} ini={T.circ1 - 6} nome="filtro" x={470} y={1000} w={520} entra="sobe" />
          <Obj q={q} ini={E.coloca1} nome="dosador" x={640} y={640} w={460} rot={8} entra="dir" extraRot={inclina(q, E.pouq1, E.po1 + 4)} />
          <Po q={q} ini={E.pouq1 + 6} x={500} y={740} ate={900} />
          <Estencil q={q} ini={E.maisPo1} texto="MAIS PÓ" x={540} y={330} tam={140} rot={-3} />
        </Plano>
      </Palco>
      <Circulo q={q} ini={T.circ1}><Rafael q={q} cam={camR(q, T.circ1, T.split1b, 1.12, 'r1b')} id="r1b" /></Circulo>
      <Capitulo q={q} n={1} />
    </AbsoluteFill>
  );
};

// 1c · erro 1, fim (16,45 → 19,05): tela dividida juta; o café da xícara escurece ("intensifica")
const C1c: React.FC<P> = ({q}) => {
  const esc = inOut(prog(q, E.intensifica + LEAD, E.intensifica + LEAD + 20));
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Metade><Rafael q={q} cam={camR(q, T.split1b, T.escuro, 1.0, 'r1c')} id="r1c" /></Metade>
      <Painel q={q} ini={T.split1b} mat="juta" cam={camP(q, T.split1b, 'p1c')} id="p1c">
        <Obj q={q} ini={T.split1b - 4} nome="xicara" x={300} y={560} w={320} rot={-3} filtro={`brightness(${1 - 0.42 * esc}) saturate(${1 + 0.2 * esc})`} />
        <Estencil q={q} ini={E.intensifica} texto="INTENSIFICA" x={560} y={290} tam={100} rot={-3} largura={900} />
        <Estencil q={q} ini={E.sabor} texto="SABOR" x={740} y={580} tam={96} rot={-2} largura={460} />
        <Traco q={q} ini={E.todo} d="M690,690 L740,740 L840,630" cor={COR.creme} esp={16} dur={8} />
      </Painel>
      <Capitulo q={q} n={1} />
    </AbsoluteFill>
  );
};

// 2 · erro 2 (19,05 → 22,16): tela cheia, fundo escurece
const C2: React.FC<P> = ({q}) => {
  const escuro = pres(q, T.escuro);
  const cam = camR(q, T.escuro, T.aco, 1.0, 'r2', -30, [pulso(q, [E.erro2Troca], 0.03)]);
  const atras = <Estencil q={q} ini={E.erro2} texto="ERRO 2" x={540} y={430} tam={210} rot={-3} fora={E.erro2Sai} />;
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Rafael q={q} cam={cam} escuro={escuro} atras={atras} id="r2" />
      <Estencil q={q} ini={E.quase} texto="QUASE NINGUÉM CONTA" x={540} y={1190} tam={64} rot={-3} />
      <Capitulo q={q} n={q >= E.erro2Troca ? 2 : 1} desde={q >= E.erro2Troca ? E.erro2Troca : undefined} />
    </AbsoluteFill>
  );
};

// 2b · de propósito (22,16 → 24,91): tela dividida com aço; congela em P&B depois do carimbo
const C2b: React.FC<P> = ({q}) => {
  const qv = quadroRafael(q);
  const valor = 0.3 + 0.25 * inOut(prog(qv, E.passa, E.ponto2)) + 0.45 * pres(qv, E.ponto2, 16);
  const pb = q >= CONGELA_Q && q < T.solta;
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <AbsoluteFill style={{filter: pb ? 'grayscale(1) contrast(1.1)' : undefined}}>
        <Metade><Rafael q={qv} cam={camR(qv, T.aco, T.solta, 1.02, 'r2b')} escuro={1} id="r2b" /></Metade>
        <Painel q={qv} ini={T.aco} mat="aco" cam={camP(qv, T.aco, 'p2b')} id="p2b">
          <Obj q={qv} ini={T.aco - 4} nome="caneca" x={290} y={420} w={340} rot={-3} />
          <Estencil q={qv} ini={E.extra} texto="EXTRAFORTE" x={290} y={660} tam={70} rot={-3} largura={540} />
          <Manometro q={qv} ini={T.aco - 4} x={770} y={430} w={420} valor={valor} treme={qv >= E.ponto2 + 16 ? 1.5 : 0} />
        </Painel>
        <Capitulo q={qv} n={2} />
      </AbsoluteFill>
      <Carimbo q={qv} ini={E.proposito} texto="DE PROPÓSITO" x={560} y={810} tam={70} cor={COR.acento} rot={-6} />
    </AbsoluteFill>
  );
};

// 2c · isso porque o grão tem (24,91 → 26,18): tela cheia escura, só a fala
const C2c: React.FC<P> = ({q}) => (
  <AbsoluteFill style={{background: COR.preto}}>
    <Rafael q={q} cam={camR(q, T.solta, T.circ2, 1.06, 'r2c', -30)} escuro={1} id="r2c" />
    <Capitulo q={q} n={2} />
  </AbsoluteFill>
);

// 2d · os defeitos (26,18 → 32,17): aço em tela cheia, Rafael no círculo.
// Os três grãos com defeito entram um por palavra; "passando do ponto" eles escurecem até ficarem
// iguais (AMARGO) e o defeito some (ESCONDIDO).
const C2d: React.FC<P> = ({q}) => {
  const camC = somar(cameraEm(q - T.circ2, [{q: 0, x: 0, y: 0, zoom: 1.03, rot: 0}, {q: 180, x: 8, y: -24, zoom: 1.08, rot: -0.2, curva: 'linear'}] as Chave[]), deriva(q, 'c2d', 0.3));
  const dk = inOut(prog(q, E.passando, E.amargo + LEAD));
  const torrado = `brightness(${1 - 0.74 * dk}) saturate(${1 - 0.7 * dk}) sepia(${0.3 * dk})`;
  return (
    <AbsoluteFill style={{background: '#2B2927'}}>
      <Palco cam={camC} id="c2d">
        <Plano p={0.7}><Fundo mat="aco" h={1920} /></Plano>
        <Plano p={1}>
          <Obj q={q} ini={T.circ2 - 6} nome="bandeja" x={380} y={1270} w={600} rot={-3} entra="sobe" />
          <Obj q={q} ini={E.preto} nome="def-preto" x={250} y={620} w={230} rot={-8} entra="cai" filtro={torrado} />
          <Obj q={q} ini={E.ardido} nome="def-ardido" x={540} y={630} w={225} rot={6} entra="cai" filtro={torrado} />
          <Obj q={q} ini={E.broca} nome="def-broca" x={830} y={620} w={220} rot={-4} entra="cai" filtro={torrado} />
          <Estencil q={q} ini={E.preto + 2} texto="PRETO" x={250} y={850} tam={58} rot={-2} largura={320} fora={E.tudo} />
          <Estencil q={q} ini={E.ardido + 2} texto="ARDIDO" x={540} y={860} tam={58} rot={2} largura={320} fora={E.tudo} />
          <Estencil q={q} ini={E.broca + 2} texto="BROCA" x={830} y={850} tam={58} rot={-2} largura={320} fora={E.tudo} />
        </Plano>
      </Palco>
      <Estencil q={q} ini={E.defeito} texto="DEFEITO" x={560} y={360} tam={130} cor={COR.creme} rot={-4} fora={E.tudo} />
      <Estencil q={q} ini={E.amargo} texto="AMARGO" x={540} y={370} tam={140} rot={-3} />
      <Carimbo q={q} ini={E.some} texto="ESCONDIDO" x={540} y={860} tam={70} cor={COR.acento} rot={-5} />
      <Circulo q={q} ini={T.circ2}><Rafael q={q} cam={camR(q, T.circ2, T.close2, 1.14, 'r2d')} escuro={1} id="r2d" /></Circulo>
      <Capitulo q={q} n={2} />
    </AbsoluteFill>
  );
};

// 2e · açúcar (32,17 → 35,23): close, escuro mais leve; um cubo cai na caneca a cada palavra
const C2e: React.FC<P> = ({q}) => (
  <AbsoluteFill style={{background: COR.preto}}>
    <Rafael q={q} cam={camR(q, T.close2, T.rasgo, 1.14, 'r2e', -40)} escuro={0.7} id="r2e" />
    <Obj q={q} ini={E.caneca} nome="caneca" x={250} y={1500} w={380} rot={4} entra="esq" />
    <Cubo q={q} ini={E.cubos[0]} nome="acucar-1" x={240} y0={1130} y1={1390} w={120} rot={10} />
    <Cubo q={q} ini={E.cubos[1]} nome="acucar-2" x={270} y0={1130} y1={1390} w={115} rot={-8} />
    <Cubo q={q} ini={E.cubos[2]} nome="acucar-3" x={220} y0={1130} y1={1390} w={118} rot={18} />
    <Estencil q={q} ini={E.acucar} texto="+ AÇÚCAR" x={700} y={1250} tam={96} rot={-3} largura={640} />
    <Capitulo q={q} n={2} />
  </AbsoluteFill>
);

// 3 · o nosso, parte 1 (35,23 → 37,41): tudo claro
const C3: React.FC<P> = ({q}) => {
  const claro = pres(q, T.rasgo);
  const atras = <Estencil q={q} ini={E.nada} texto={'NADA PRA\nESCONDER'} x={540} y={350} tam={128} cor={COR.preto} rot={-3} />;
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Rafael q={q} cam={camR(q, T.rasgo, T.split3, 1.04, 'r3')} claro={claro} atras={atras} id="r3" />
    </AbsoluteFill>
  );
};

// 3b · o nosso, parte 2 (37,41 → 45,64): tela dividida com papel de laudo
const C3b: React.FC<P> = ({q}) => {
  const varre = inOut(prog(q, E.atravessa, E.atravessa + 18));
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Metade><Rafael q={q} cam={camR(q, T.split3, T.receita, 1.0, 'r3b')} claro={1} id="r3b" /></Metade>
      <Painel q={q} ini={T.split3} mat="laudo" cam={camP(q, T.split3, 'p3b')} id="p3b">
        <Obj q={q} ini={T.split3 - 4} nome="suave-estudio" x={260} y={420} w={290} rot={-4} entra="sobe" />
        <Estencil q={q} ini={E.marrom} texto="MARROM" x={260} y={760} tam={84} cor={COR.terra} rot={-2} largura={460} fora={segura(E.marrom, S4A.marrom)} />
        <Carimbo q={q} ini={E.media} texto="TORRA MÉDIA" x={730} y={230} tam={60} cor={COR.terra} rot={-5} papel={false} />
        <Obj q={q} ini={E.luz} nome="xicara" x={740} y={520} w={280} rot={3} entra="dir" />
        {varre > 0 && varre < 1 && (
          <div style={{position: 'absolute', left: 740 - 170 + varre * 340, top: 360, width: 80, height: 360, background: 'linear-gradient(90deg, rgba(255,250,235,0), rgba(255,250,235,0.8), rgba(255,250,235,0))',
            transform: 'rotate(12deg)', mixBlendMode: 'screen'}} />
        )}
        <Traco q={q} ini={E.gosto} d="M630,600 C560,660 500,720 440,750" cor={COR.terra} esp={10} dur={16} fora={segura(E.chocolate, S4B.chocolate)} />
        <Estencil q={q} ini={E.chocolate} texto="CHOCOLATE" x={290} y={800} tam={66} cor={COR.terra} rot={-3} largura={540} fora={segura(E.chocolate, S4B.chocolate)} />
        <Estencil q={q} ini={E.azedinho} texto="AZEDINHO" x={720} y={800} tam={66} cor={COR.terra} rot={-2} largura={480} />
        <Obj q={q} ini={E.fruta} nome="cereja" x={930} y={680} w={210} rot={-10} entra="cai" />
      </Painel>
    </AbsoluteFill>
  );
};

// 4 · a receita (45,64 → 51,15): prancheta sobre juta, tela dividida
const C4: React.FC<P> = ({q}) => {
  const conta = Math.round(50 * pres(q, E.cinquenta + LEAD, 16));
  const enche = inOut(prog(q, E.agua, E.agua + 22));
  const logoK = q >= E.logo4 ? 1.06 - 0.06 * pres(q, E.logo4, 8) : 1;
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Metade><Rafael q={q} cam={camR(q, T.receita, T.cheio4, 1.0, 'r4')} id="r4" /></Metade>
      <Painel q={q} ini={T.receita} mat="juta" cam={camP(q, T.receita, 'p4')} id="p4">
        <Img src={staticFile('colagem/r10-prancheta.png')} style={{position: 'absolute', left: 140, top: 40, width: 800, transform: 'rotate(-1.5deg)', filter: SOMBRA_OBJ}} />
        <Img src={staticFile('fonte/logo-preta.png')} style={{position: 'absolute', left: 540 - 100, top: 225, height: 130, transform: `rotate(-1.5deg) scale(${logoK})`}} />
        <Obj q={q} ini={E.balanca} nome="balanca" x={380} y={650} w={420} rot={-2} entra="cai" />
        {q >= E.balanca + 6 && (
          <div style={{position: 'absolute', left: 380 - 70, top: 650 + 40, width: 140, height: 44, display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontFamily: PILHA.dado, fontWeight: 500, fontSize: 40, color: '#1E2A22', transform: 'rotate(-2deg)', opacity: cl((q - E.balanca - 5) / 4)}}>{conta} g</div>
        )}
        <Estencil q={q} ini={E.cinquenta} texto="50 g" x={760} y={330} tam={140} cor={COR.terra} rot={-3} largura={420} />
        <Obj q={q} ini={E.filtro4} nome="filtro" x={380} y={540} w={230} entra="cai" />
        <Carimbo q={q} ini={E.ml} texto="500 ml" x={760} y={470} tam={54} cor={COR.terra} rot={-5} papel={false} />
        <Obj q={q} ini={E.jarra} nome="jarra" x={760} y={680} w={260} entra="dir" />
        {enche > 0 && (
          <div style={{position: 'absolute', left: 760 - 92, top: 680 + 88 - 128 * enche, width: 172, height: 128 * enche, background: 'rgba(120,80,45,0.35)',
            borderRadius: '0 0 26px 26px', mixBlendMode: 'multiply'}} />
        )}
      </Painel>
    </AbsoluteFill>
  );
};

// 4b · eco do erro 1 (51,15 → 53,84): tela cheia, fundo real
const C4b: React.FC<P> = ({q}) => {
  const atras = <Carimbo q={q} ini={E.erro1b} texto="ERRO 1" x={540} y={420} tam={96} cor={COR.terra} rot={-5} fora={E.erro1b + LEITURA} />;
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Rafael q={q} cam={camR(q, T.cheio4, T.fecho, 1.06, 'r4b', -20, [pulso(q, [E.erro1b + 1], 0.03)])} atras={atras} id="r4b" />
      <Obj q={q} ini={E.dosador4b} nome="dosador" x={300} y={1460} w={400} rot={8} entra="esq" extraRot={inclina(q, E.pouq4b, E.pouq4b + 18)} fora={E.pouq4b + 24} saiPara="esq" />
      <Po q={q} ini={E.pouq4b + 6} x={170} y={1540} ate={1800} />
      <MaisPo q={q} />
    </AbsoluteFill>
  );
};
/** "+ PÓ" do eco: entra no "mais de pó" e atravessa o corte para o fecho (a palavra cai 2 q antes dele). */
const MaisPo: React.FC<P> = ({q}) => <Estencil q={q} ini={E.maisPo4b} texto="+ PÓ" x={760} y={1250} tam={150} rot={-3} largura={600} fora={E.maisPo4b + 40} />;

// 5 · fecho (53,84 → fim): fundo real; o fim emenda no começo (a xícara e o CHAFÉ? voltam)
const C5: React.FC<P> = ({q}) => {
  const ch = W(S5C.chafe);
  const cam = camR(q, T.fecho, DURACAO_CHAFE, 0.98, 'r5', -24, [pulso(q, [ch], 0.03)]);
  const atras = (
    <>
      <Estencil q={q} ini={E.manda} texto="MANDA PRO AMIGO" x={540} y={410} tam={88} rot={-3} fora={E.chafe5} />
      <Estencil q={q} ini={E.chafe5} texto="CHAFÉ?" x={540} y={460} tam={196} rot={-3} />
    </>
  );
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Rafael q={q} cam={cam} atras={atras} id="r5" />
      <MaisPo q={q} />
      <Obj q={q} ini={E.xicara5} nome="xicara" x={190} y={1530} w={230} rot={-6} entra="esq" />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------ montagem
// [início, cena, y da legenda]
const CENAS: Array<[number, React.FC<P>, number]> = [
  [0, C0, 1390], [T.split1, C1, 900], [T.circ1, C1b, 1290], [T.split1b, C1c, 900], [T.escuro, C2, 1390], [T.aco, C2b, 900],
  [T.solta, C2c, 1390], [T.circ2, C2d, 1010], [T.close2, C2e, 1390], [T.rasgo, C3, 1390], [T.split3, C3b, 900], [T.receita, C4, 900],
  [T.cheio4, C4b, 1390], [T.fecho, C5, 1390],
];
const cenaEm = (q: number) => {let c = CENAS[0]; for (const e of CENAS) if (q >= e[0]) c = e; return c;};

// som: [arquivo, quadro em que o PICO cai, volume]
const PICO: Record<string, number> = {whoosh: 0.15, whooshb: 0.275, whooshg: 0.276, riser: 0.286, baque: 0.039, toque: 0.011, ding: 0.013, catraca: 0.014,
  clique: 0.033, tecla: 0.008, spray: 0.201, envelope: 0.114, rasgo: 0.498, saca: 0.03, sementes: 0.044, dado: 0.006, vidro: 0.006, liquido: 0.304, bipe: 0.035};
const s = (a: string, q: number, v: number): [string, number, number] => [a, q - F(PICO[a]), v];
// cada som cai no quadro em que o seu elemento assenta (mesmos quadros de E):
const spray = (ini: number, v = 0.14) => s('spray', ini + 4, v); // meio da revelação do estêncil
const pousa = (a: string, ini: number, v = 0.24) => s(a, ini + 7, v); // objeto assentado (~96% da curva)
const bate = (ini: number, v = 0.32) => s('baque', ini + 2, v); // carimbo encosta
const corte = (q: number, a = 'whoosh', v = 0.16) => s(a, q, v); // troca de tela
const desce = (q: number, v = 0.24) => s('whooshb', q + 6, v); // painel descendo
const MICRO = 0.12;
const SONS: Array<[string, number, number]> = [
  // 0
  spray(E.chafe, 0.16), s('baque', E.chafe + 4, 0.2), spray(E.errou, 0.1), bate(E.duas, 0.4), s('whoosh', E.xicaraSai + 4, 0.1),
  s('whooshb', E.rafael + 5, 0.2), s('toque', E.canastra + 3, 0.16), bate(E.torref, 0.2), s('whoosh', E.corte + 4, 0.12),
  // 1
  desce(T.split1, 0.26), spray(E.erro1, 0.16), pousa('vidro', E.cafe1), spray(E.clarinho), spray(E.fraco), spray(E.risca, 0.14),
  s('whooshb', E.desliza + 6, 0.22), spray(E.torra, 0.12), spray(E.intensidade, 0.12), s('catraca', E.intensidade + 8, MICRO), s('clique', E.sim + 3, 0.12),
  s('catraca', E.passar, MICRO), s('catraca', E.passar + 7, MICRO), s('ding', E.ponto + 4, 0.16), spray(E.intenso, 0.16),
  // 1b
  corte(T.circ1, 'whooshb', 0.24), pousa('toque', T.circ1 - 6, 0.2), s('whoosh', E.coloca1 + 5, 0.14), pousa('toque', E.coloca1, 0.14),
  s('sementes', E.pouq1 + 8, 0.28), spray(E.maisPo1, 0.16),
  // 1c
  desce(T.split1b), spray(E.intensifica, 0.16), spray(E.sabor), s('clique', E.todo + 3, 0.12),
  // 2
  s('whooshg', T.escuro + 2, 0.32), spray(E.erro2, 0.18), s('baque', E.erro2Troca + 1, 0.26), spray(E.quase, 0.12),
  // 2b
  desce(T.aco), spray(E.extra, 0.12), s('catraca', E.passa, MICRO), s('catraca', E.passa + 8, MICRO), s('catraca', E.ponto2, 0.16), s('catraca', E.ponto2 + 6, 0.14),
  s('riser', E.proposito + 2, 0.16), bate(E.proposito, 0.5), s('whoosh', T.solta, 0.1),
  // 2d
  corte(T.circ2, 'whooshg', 0.3), spray(E.defeito, 0.16), pousa('toque', E.preto), pousa('toque', E.ardido), pousa('toque', E.broca),
  s('riser', E.amargo + 4, 0.12), spray(E.amargo, 0.16), bate(E.some, 0.4),
  // 2e
  corte(T.close2, 'whoosh', 0.14), pousa('toque', E.caneca, 0.2), ...E.cubos.map((c) => s('dado', c + 10, 0.28)), spray(E.acucar, 0.14),
  // 3
  s('rasgo', T.rasgo + 5, 0.4), spray(E.nada, 0.14),
  // 3b
  desce(T.split3), spray(E.marrom, 0.12), bate(E.media, 0.26), pousa('vidro', E.luz), s('whoosh', E.atravessa + 9, 0.1), spray(E.gosto, 0.08),
  spray(E.chocolate), spray(E.azedinho, 0.12), pousa('toque', E.fruta, 0.2),
  // 4
  desce(T.receita), s('toque', E.logo4 + 1, 0.14), pousa('toque', E.balanca, 0.28), s('bipe', E.cinquenta + LEAD + 16, 0.18), spray(E.cinquenta),
  pousa('saca', E.filtro4, 0.2), bate(E.ml, 0.22), pousa('vidro', E.jarra, 0.22), s('liquido', E.agua + 2, 0.24),
  // 4b
  corte(T.cheio4, 'whoosh', 0.14), bate(E.erro1b, 0.28), pousa('toque', E.dosador4b, 0.14), s('sementes', E.pouq4b + 8, 0.26), spray(E.maisPo4b, 0.16),
  // 5
  corte(T.fecho, 'whooshg', 0.22), spray(E.manda, 0.14), pousa('vidro', E.xicara5, 0.18), spray(E.chafe5, 0.18), s('baque', E.chafe5 + 4, 0.26),
];

export const Chafe: React.FC = () => {
  const q = useCurrentFrame();
  const [ini, C, yLeg] = cenaEm(q);
  // corte seco que assenta: a cena nova chega 2% maior e pousa em 10 q (sem borrão)
  const assenta = ini > 0 ? 1 + 0.02 * (1 - pres(q, ini, 10)) : 1;
  // rasgo (35,23): a cena escura se parte em duas e abre para a clara
  const rasgando = q >= T.rasgo && q < T.rasgo + 14;
  const tr = inOut(prog(q, T.rasgo, T.rasgo + 14));
  const borda = 'polygon(0 0,100% 0,100% 47%,92% 50%,84% 46%,76% 51%,67% 47%,58% 52%,49% 48%,40% 53%,31% 48%,22% 52%,13% 47%,5% 51%,0 48%)';
  const bordaB = 'polygon(0 48%,5% 51%,13% 47%,22% 52%,31% 48%,40% 53%,49% 48%,58% 52%,67% 47%,76% 51%,84% 46%,92% 50%,100% 47%,100% 100%,0 100%)';
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Defs />
      <AbsoluteFill style={{transform: `scale(${assenta})`}}>
        <C q={q} />
      </AbsoluteFill>
      {rasgando && (
        <>
          <AbsoluteFill style={{clipPath: borda, transform: `translateY(${-1100 * tr}px)`}}><C2e q={T.rasgo - 1} /></AbsoluteFill>
          <AbsoluteFill style={{clipPath: bordaB, transform: `translateY(${1100 * tr}px)`}}><C2e q={T.rasgo - 1} /></AbsoluteFill>
        </>
      )}
      <Legenda q={q} y={yLeg} />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 44%, rgba(8,5,3,0) 55%, rgba(8,5,3,0.32) 100%)', pointerEvents: 'none'}} />
      <Audio src={staticFile('fonte/voz-sync.wav')} />
      <Audio src={staticFile('sfx/s2-ambiente.wav')} volume={0.05} />
      {SONS.map(([a, qq, v], n) => (
        <Sequence key={n} from={Math.max(0, qq)} durationInFrames={70}><Audio src={staticFile(`sfx/s2-${a}.wav`)} volume={v} /></Sequence>
      ))}
    </AbsoluteFill>
  );
};
