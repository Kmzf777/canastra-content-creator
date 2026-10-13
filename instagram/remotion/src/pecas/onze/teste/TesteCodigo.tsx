// Teste A/B de 13/10/2026 — trecho 55,65–65,6 s da peça 08b ("Quando um café amarga
// demais... se faz em tudo que vem antes dela"), refeito com o que as referências
// (Aryan Raj, motion de marca; kaomei/stickman-video-director) ensinaram:
//   - sem pílula: o texto É a manchete, palavra-chave por palavra-chave, no tempo da voz
//   - câmera nunca parada; parallax em 3 planos; objeto cruzando a lente
//   - boneco com ação física a cada 1–2 s, antecipação, achatamento, nunca parado
//   - um objeto gigante na cor de acento por plano (a caneca, a barreira, o mostrador)
//   - plano real intercalado (a mão com o grão bom)
// Torra sem fogo, fumaça ou grão preto (lição 66): o "passou da conta" é um mostrador.

import {Audio} from '@remotion/media';
import React from 'react';
import {AbsoluteFill, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {COR} from '../../../identidade/tokens';
import {PILHA} from '../../../identidade/tipografia';
import {PILHA_COLAGEM} from '../../../colagem/fontes-colagem';
import {cameraEm, deriva, pulso, somar, tremor, type Chave} from '../../../colagem/camera';
import {Palco, Plano} from '../../../colagem/palco';
import {Dymo} from '../../../colagem/tipos';
import {Clipe, Fundo, GraoFilme, Peca, SombraFolhas, Vinheta} from '../../fruta/apoio';
import {PALAVRAS} from '../roteiro';
import {BonecoV2, chaves, corrida, mistura, type PoseV2} from './BonecoV2';

export const T0 = 55.65;
const FIM_S = 65.95;
export const DURACAO_TESTE = Math.round((FIM_S - T0) * 30);
const lq = (s: number) => Math.round((s - T0) * 30);
const chave = (s: string) => s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
/** Quadro local da n-ésima ocorrência da palavra depois de T0. */
const w = (p: string, n = 1) => {
  let k = 0;
  for (const x of PALAVRAS) if (x.inicio >= T0 - 0.05 && chave(x.texto) === chave(p) && ++k === n) return lq(x.inicio);
  throw new Error(`teste: "${p}" não achada`);
};

// planos (quadros locais) — cada troca cai ANTES da palavra que abre o plano seguinte
export const A0 = 0, B0 = w('alguma') - 3, C0 = w('torra') - 4, D0 = w('café', 2) - 4;
export const ease = (t: number) => {const u = Math.min(1, Math.max(0, t)); return u * u * (3 - 2 * u);};
export const lin = (q: number, a: number, b: number) => Math.min(1, Math.max(0, (q - a) / Math.max(1, b - a)));

// ------------------------------------------------------------------ peças desenhadas
export const Caneca: React.FC<{s: number}> = ({s}) => (
  <g transform={`scale(${s})`}>
    <path d="M-70,-90 L70,-90 L60,70 Q0,95 -60,70 Z" fill={COR.acento} stroke={COR.preto} strokeWidth={9} strokeLinejoin="round" />
    <path d="M66,-50 Q120,-45 112,5 Q105,40 62,35" fill="none" stroke={COR.preto} strokeWidth={9} />
    <ellipse cx={0} cy={-90} rx={70} ry={16} fill="#3B2416" stroke={COR.preto} strokeWidth={7} />
  </g>
);
/** Ondas de amargor saindo da caneca (rabiscos que sobem). */
export const Amargor: React.FC<{q: number; ini: number; x: number; y: number}> = ({q, ini, x, y}) => {
  if (q < ini) return null;
  const k = q - ini;
  return (
    <svg style={{position: 'absolute', left: x - 150, top: y - 300, overflow: 'visible'}} width={300} height={300}>
      {[-70, 0, 70].map((dx, i) => {
        const t = ((k + i * 5) % 18) / 18;
        return <path key={i} d={`M${150 + dx},${260 - t * 160} q14,-18 0,-36 q-14,-18 0,-36`} stroke={COR.verde} strokeWidth={10}
          fill="none" strokeLinecap="round" opacity={1 - t} />;
      })}
    </svg>
  );
};
export const Barreira: React.FC<{x: number; y: number}> = ({x, y}) => (
  <div style={{position: 'absolute', left: x - 130, top: y - 250, width: 260, height: 250}}>
    <div style={{position: 'absolute', left: 18, top: 60, width: 16, height: 190, background: COR.terra}} />
    <div style={{position: 'absolute', right: 18, top: 60, width: 16, height: 190, background: COR.terra}} />
    <div style={{position: 'absolute', left: 0, top: 20, width: 260, height: 70, background: COR.acento, boxShadow: '0 8px 12px rgba(0,0,0,.3)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: PILHA.manchete, fontSize: 46, color: COR.creme, letterSpacing: 2}}>PROVA</div>
  </div>
);
/** A chapada da Serra da Canastra: topo PLANO (lição 2), silhueta recortada em papel. */
export const Chapada: React.FC<{x: number}> = ({x}) => (
  <svg style={{position: 'absolute', left: x, top: 930}} width={4200} height={420}>
    <path d="M0,420 L0,250 L260,230 L420,120 L1100,110 L1260,220 L1700,240 L1880,140 L2500,130 L2650,230 L3200,250 L3350,120 L4200,110 L4200,420 Z"
      fill="#CDBB9C" />
  </svg>
);
export const Linhas: React.FC<{x: number; y: number; q: number}> = ({x, y, q}) => (
  <svg style={{position: 'absolute', left: x - 330, top: y - 300, overflow: 'visible'}} width={300} height={300}>
    {[0, 1, 2, 3].map((i) => {
      const o = ((q * 37 + i * 53) % 60) - 30;
      return <path key={i} d={`M${40 + o},${60 + i * 60} h${150 - i * 20}`} stroke={COR.preto} strokeWidth={7} strokeLinecap="round" opacity={0.55} />;
    })}
  </svg>
);
export const Poeira: React.FC<{q: number; ini: number; x: number; y: number}> = ({q, ini, x, y}) => {
  const k = q - ini;
  if (k < 0 || k > 14) return null;
  const t = k / 14;
  return (
    <>{[-1, 1].map((d) => [0, 1, 2].map((i) => (
      <div key={`${d}${i}`} style={{position: 'absolute', left: x + d * (40 + t * (120 + i * 60)) - 30, top: y - 30 - t * (30 + i * 25),
        width: 60 - i * 12, height: 60 - i * 12, borderRadius: '50%', background: '#D8C7A6', opacity: 1 - t, border: `5px solid ${COR.preto}`}} />
    )))}</>
  );
};
export const Mostrador: React.FC<{q: number; giro: number; x: number; y: number}> = ({q, giro, x, y}) => {
  const ang = -120 + giro * 240;
  const treme = giro > 0.95 ? Math.sin(q * 2.3) * 4 : 0;
  return (
    <svg style={{position: 'absolute', left: x - 330, top: y - 330, overflow: 'visible'}} width={660} height={660}>
      <circle cx={330} cy={330} r={300} fill={COR.creme} stroke={COR.preto} strokeWidth={14} />
      <path d={`M${330 + Math.sin((60 * Math.PI) / 180) * 250},${330 - Math.cos((60 * Math.PI) / 180) * 250} A250,250 0 0 1 ${330 + Math.sin((120 * Math.PI) / 180) * 250},${330 - Math.cos((120 * Math.PI) / 180) * 250}`}
        stroke={COR.acento} strokeWidth={44} fill="none" />
      {Array.from({length: 13}, (_, i) => {
        const a = ((-120 + i * 20) * Math.PI) / 180;
        return <line key={i} x1={330 + Math.sin(a) * 215} y1={330 - Math.cos(a) * 215} x2={330 + Math.sin(a) * 270} y2={330 - Math.cos(a) * 270} stroke={COR.preto} strokeWidth={i % 3 ? 6 : 12} />;
      })}
      <g transform={`rotate(${ang + treme} 330 330)`}>
        <path d="M322,330 L330,90 L338,330 Z" fill={COR.preto} stroke={COR.preto} strokeWidth={8} strokeLinejoin="round" />
      </g>
      <circle cx={330} cy={330} r={34} fill={COR.preto} />
    </svg>
  );
};
export const Pano: React.FC<{t: number; x: number; y: number}> = ({t, x, y}) => {
  if (t <= 0) return null;
  const e = ease(t);
  const yy = y - 420 * (1 - e);
  return (
    <svg style={{position: 'absolute', left: x - 230, top: yy - 140, overflow: 'visible'}} width={460} height={240}>
      <path d={`M10,${40 + (1 - e) * 60} Q120,${10 - (1 - e) * 40} 230,30 Q340,${50 + (1 - e) * 40} 450,${36 + (1 - e) * 50} L440,220 Q230,${200 + e * 20} 20,224 Z`}
        fill="#6B4A33" stroke={COR.preto} strokeWidth={9} strokeLinejoin="round" />
      <path d="M90,80 Q110,150 95,210 M250,70 Q270,140 255,205 M370,80 Q385,150 375,212" stroke="#4F3424" strokeWidth={6} fill="none" />
    </svg>
  );
};
export const Nota: React.FC<{q: number; ini: number; x: number; y: number}> = ({q, ini, x, y}) => {
  const k = q - ini;
  if (k < 0) return null;
  return <>{[0, 1].map((i) => {
    const kk = k - i * 8;
    if (kk < 0) return null;
    const t = (kk % 24) / 24;
    return <div key={i} style={{position: 'absolute', left: x + i * 50 + Math.sin(kk / 3) * 12, top: y - t * 120, fontSize: 70, color: COR.preto, opacity: 1 - t,
      fontFamily: 'Georgia, serif'}}>♪</div>;
  })}</>;
};

// ------------------------------------------------------------------ manchete cinética
/** Palavras-chave entrando no instante exato em que a voz as diz, com carimbo de 4 quadros. */
export const Manchete: React.FC<{q: number; itens: Array<{t: string; q: number; cor?: string; tam?: number}>; x: number; y: number; fonte?: 'manchete' | 'serifa'; rot?: number; fora?: number; largura?: number}> = ({
  q, itens, x, y, fonte = 'manchete', rot = -2, fora, largura = 900,
}) => fora !== undefined && q >= fora ? null : (
  <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) rotate(${rot}deg)`, display: 'flex', flexWrap: 'wrap',
    justifyContent: 'center', width: largura, columnGap: 22, rowGap: 0}}>
    {itens.map((it, i) => {
      const k = q - it.q;
      const vis = k >= 0;
      const esc = k < 0 ? 0 : k < 3 ? 1.14 - k * 0.035 : k < 7 ? 1.035 - (k - 3) * 0.009 : 1;
      return (
        <span key={i} style={{visibility: vis ? 'visible' : 'hidden', display: 'inline-block', transform: `scale(${esc})`,
          fontFamily: fonte === 'manchete' ? PILHA.manchete : PILHA_COLAGEM.serifa, fontStyle: fonte === 'serifa' ? 'italic' : 'normal',
          fontSize: it.tam ?? (fonte === 'manchete' ? 150 : 120), lineHeight: 1.02, color: it.cor ?? COR.preto,
          textShadow: fonte === 'serifa' ? '0 4px 18px rgba(0,0,0,.45)' : '0 6px 0 rgba(20,16,13,.12)'}}>{fonte === 'manchete' ? it.t.toUpperCase().replace(/[.,:;]+$/, '') : it.t}</span>
      );
    })}
  </div>
);

// ------------------------------------------------------------------ planos
export const PlanoA: React.FC<{q: number}> = ({q}) => {
  const am = w('amarga'), de = w('demais');
  const pose: PoseV2 = chaves(q, [
    [0, {bD: 150, cD: 110, bE: -20, cE: -30, tronco: -4, cab: 4}],
    [am - 2, {bD: 152, cD: 112, bE: -22, cE: -30, tronco: -6, cab: 8}],
    [am + 3, {bD: 100, cD: 30, bE: -70, cE: -60, tronco: -16, cab: -22, sq: -0.1}],
    [de + 6, {bD: 95, cD: 25, bE: -80, cE: -50, tronco: -12, cab: -14}],
    [de + 24, {bD: 45, cD: 15, bE: -30, cE: -15, tronco: 2, cab: 6}],
    [B0, {bD: 40, cD: 15, bE: -25, cE: -10, tronco: 6, cab: 4}],
  ]);
  const cam = somar(cameraEm(q, [{q: 0, x: 30, y: 60, zoom: 1.2, rot: 0}, {q: am, x: 0, y: 10, zoom: 1.1, rot: -1.2, curva: 'rapida'}, {q: B0, x: 40, y: -10, zoom: 1.06, rot: 0.4, curva: 'linear'}]),
    deriva(q, 'tA', 0.7), pulso(q, [am], 0.05), tremor(q, am, 12, 5));
  return (
    <AbsoluteFill>
      <Fundo cor={COR.creme} forca={0.5} />
      <Palco cam={cam} id="tA">
        <Plano p={0.5}><SombraFolhas q={q} opacidade={0.16} /></Plano>
        <Plano p={1}>
          <BonecoV2 x={440} y={1840} h={900} q={q} pose={pose} rosto={q >= am ? 'careta' : 'foco'} naMao={<Caneca s={1.1} />} giroD={q < am ? -28 : 12}
            alvoD={lin(q, am, am + 6) < 1 ? [0.17 + (0.45 - 0.17) * ease(lin(q, am, am + 6)), -0.81 + (0.81 - 0.62) * ease(lin(q, am, am + 6))] : [0.45, -0.62]} />
          <Amargor q={q} ini={am} x={760} y={980} />
        </Plano>
        <Plano p={1.15}>
          <Manchete q={q} x={540} y={430} itens={[{t: 'AMARGA', q: am, cor: COR.acento, tam: 150}, {t: 'DEMAIS?', q: de, tam: 110}]} />
        </Plano>
        <Plano p={2.6}><Peca q={q} ini={0} nome="folha-1" x={1050 - q * 14} y={1500} w={760} rot={-30 + q} semBoil /></Plano>
      </Palco>
    </AbsoluteFill>
  );
};

export const PlanoB: React.FC<{q: number}> = ({q}) => {
  const k = q - B0;
  const pu = w('pulada') - B0;
  const sobe = pu - 11, desce = pu + 13;
  const vel = (i: number) => (i >= sobe && i < desce ? 17 : i >= desce + 8 ? 6 : 15);
  let X = 0;
  for (let i = 0; i < k; i++) X += vel(i);
  let Xp = 0;
  for (let i = 0; i < pu; i++) Xp += vel(i);
  const HX = 380 + Xp; // a barreira do meio fica embaixo do boneco no pico
  const bars = [HX - 1600, HX - 800, HX, HX + 800];
  const noAr = k >= sobe && k < desce;
  const alt = noAr ? Math.sin(((k - sobe) / (desce - sobe)) * Math.PI) * 400 : 0;
  const run = corrida(k, 15);
  let pose: PoseV2 = run;
  if (k >= sobe - 5 && k < sobe) pose = mistura(run, {...run, sq: 0.35, tronco: 28, pE: 30, jE: 90, pD: -10, jD: 90, bE: -60, bD: -60, cE: 20, cD: 20}, (k - (sobe - 5)) / 5);
  if (noAr) pose = {tronco: 20, cab: -10, pE: 85, jE: 120, pD: -35, jD: 70, bE: -160, cE: 10, bD: 150, cD: 30, sq: -0.15};
  if (k >= desce && k < desce + 6) pose = mistura({...run, sq: 0.4, tronco: 30, pE: 40, jE: 100, pD: -30, jD: 90}, run, (k - desce) / 6);
  const prova = w('prova') - B0;
  const cam = somar(cameraEm(k, [
    {q: 0, x: 120, y: 0, zoom: 1.05, rot: 0},
    {q: sobe, x: 40, y: 0, zoom: 1.0, rot: -1},
    {q: pu, x: 0, y: -170, zoom: 1.14, rot: 2.5, curva: 'rapida'},
    {q: desce + 6, x: 0, y: 40, zoom: 1.04, rot: 0},
    {q: C0 - B0, x: -60, y: 0, zoom: 1.08, rot: -1},
  ]), deriva(q, 'tB', 0.7), tremor(k, desce, 14, 5), pulso(k, [pu], 0.04));
  const chao = 1560;
  return (
    <AbsoluteFill>
      <Fundo cor="#E9DFCB" forca={0.5} />
      <Palco cam={cam} id="tB">
        <Plano p={0.3}><Chapada x={-200 - X * 0.3} /></Plano>
        <Plano p={0.6}><SombraFolhas q={q} opacidade={0.12} /></Plano>
        <Plano p={1}>
          <div style={{position: 'absolute', left: -400, top: chao, width: 1900, height: 500, background: '#C9A97E'}} />
          <div style={{position: 'absolute', left: -400, top: chao - 6, width: 1900, height: 12, background: COR.terra}} />
          {bars.map((bx, i) => <Barreira key={i} x={bx - X} y={chao} />)}
          {!noAr && <Linhas x={380} y={chao - 300} q={q} />}
          <BonecoV2 x={380} y={chao - alt} h={560} pose={pose} rosto={noAr ? 'susto' : k > desce + 6 ? 'assobio' : 'esforco'} bob={noAr ? 0 : run.bob} />
          <Poeira q={k} ini={desce} x={380} y={chao} />
        </Plano>
        <Plano p={1.1}>
          <Manchete q={k} x={600} y={300} itens={[{t: 'PULADA!', q: pu, cor: COR.acento, tam: 145}]} rot={-4} />
        </Plano>
        <Plano p={2.2}>
          {[0, 1, 2, 3, 4].map((i) => (
            <Peca key={i} q={q} ini={0} nome={i % 2 ? 'folha-2' : 'folha-5'} x={((i * 520 - X * 1.6) % 2600 + 2600) % 2600 - 500} y={1880} w={520} rot={i * 37} semBoil />
          ))}
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};

export const PlanoC: React.FC<{q: number}> = ({q}) => {
  const k = q - C0;
  const pa = w('passou') - C0, co = w('conta') - C0, ds = w('disfarçar') - C0, pra = w('pra') - C0;
  const giro = k < pa ? 0.35 : k < pa + 16 ? 0.35 + ease((k - pa) / 16) * 0.75 : 1.1 - Math.min(0.08, (k - pa - 16) * 0.006);
  // boneco: gira a manivela, depois corre até o monte e joga o pano
  const anda = lin(k, pra - 6, ds - 4);
  const bx = 820 + anda * 440;
  const pose: PoseV2 = k < pra - 6
    ? chaves(k, [[0, {bD: 40, cD: 20, bE: -40}], [pa - 3, {bD: -150, cD: -20, bE: -140, cE: -20, tronco: -10, sq: 0.1}],
      [pa + 6, {bD: -60, cD: -60, bE: -50, cE: -60, tronco: 14, sq: 0.2}], [pa + 14, {bD: -90, cD: -40, bE: -80, cE: -30, tronco: 6}]])
    : k < ds - 4 ? {...corrida(k, 16), tronco: 6, pE: Math.sin(k / 16 * 6.28) * 26, pD: -Math.sin(k / 16 * 6.28) * 26, jE: 12, jD: 12, bE: -Math.sin(k / 16 * 6.28) * 22, bD: Math.sin(k / 16 * 6.28) * 22, cE: 15, cD: 15}
      : chaves(k, [[ds - 4, {bD: 160, cD: 10, bE: 150, cE: -10, tronco: -8, sq: -0.1}], [ds + 4, {bD: 60, cD: 40, bE: 50, cE: 30, tronco: 18, sq: 0.15}],
        [ds + 12, {bD: -150, cD: -40, bE: 150, cE: 40, tronco: 0, cab: 8}]]);
  const cam = somar(cameraEm(k, [
    {q: 0, x: -40, y: 40, zoom: 1.12, rot: 0},
    {q: pa, x: 0, y: 20, zoom: 1.04, rot: -1.5},
    {q: pra - 6, x: 80, y: 20, zoom: 1.06, rot: 0},
    {q: ds, x: 900, y: 40, zoom: 1.1, rot: 1.5, curva: 'rapida'},
    {q: D0 - C0, x: 940, y: 30, zoom: 1.18, rot: 0.5},
  ]), deriva(q, 'tC', 0.7), tremor(k, pa + 14, 10, 5), pulso(k, [co], 0.04));
  const chao = 1480;
  return (
    <AbsoluteFill>
      <Fundo cor={COR.creme} forca={0.5} />
      <Palco cam={cam} id="tC">
        <Plano p={0.5}><SombraFolhas q={q} opacidade={0.15} /></Plano>
        <Plano p={1}>
          <Mostrador q={k} giro={giro} x={430} y={940} />
          <div style={{position: 'absolute', left: 380, top: 1260, width: 100, height: 230, background: COR.terra}} />
          {['grao-ardido', 'grao-imaturo', 'grao-quebrado', 'grao-concha', 'grao-ardido'].map((g, i) => (
            <Peca key={i} q={k} ini={0} nome={g} x={1500 + (i % 3) * 90 - 90} y={chao - 50 - Math.floor(i / 3) * 70} w={130} rot={i * 33} />
          ))}
          <Pano t={lin(k, ds - 4, ds + 9)} x={1530} y={chao - 60} />
          {k >= ds + 12 && <Nota q={k} ini={ds + 12} x={bx + 60} y={chao - 640} />}
          <BonecoV2 x={bx} y={chao} h={560} pose={pose} rosto={k < pa ? 'foco' : k < pra - 6 ? 'esforco' : k < ds + 10 ? 'foco' : 'assobio'}
            bob={k >= pra - 6 && k < ds - 4 ? corrida(k, 16).bob * 0.4 : 0} espelhar={false} />
        </Plano>
        <Plano p={1.12}>
          <Manchete q={k} x={540} y={440} itens={[{t: 'PASSOU', q: pa, tam: 120}, {t: 'DA CONTA', q: co, cor: COR.acento, tam: 120}]} />
          <Dymo q={k} ini={ds} texto="DISFARCE" x={1600} y={660} tamanho={84} rot={-3} />
        </Plano>
        <Plano p={2.4}><Peca q={q} ini={0} nome="folha-2" x={-200 + k * 12} y={1750} w={700} rot={20 + k} semBoil /></Plano>
      </Palco>
    </AbsoluteFill>
  );
};

export const PlanoD: React.FC<{q: number}> = ({q}) => {
  const k = q - D0;
  const troca = w('se', 2) - D0 - 3;
  const cam = somar(cameraEm(k, [{q: 0, x: 0, y: 0, zoom: 1.04, rot: 0}, {q: troca - 1, x: 0, y: -20, zoom: 1.12, rot: -0.6, curva: 'linear'},
    {q: troca, x: 0, y: 0, zoom: 1.06, rot: 0.4}, {q: 130, x: 0, y: -20, zoom: 1.14, rot: 0, curva: 'linear'}]), deriva(q, 'tD', 0.6));
  const l1 = [['Café', 'café'], ['bom', 'bom'], ['não', 'não'], ['se', 'se'], ['faz', 'faz'], ['na', 'na'], ['torra.', 'torra']];
  const l2 = [['Se', 'se'], ['faz', 'faz'], ['em', 'em'], ['tudo', 'tudo'], ['que', 'que'], ['vem', 'vem'], ['antes', 'antes'], ['dela.', 'dela']];
  const occ: Record<string, number> = {café: 1, torra: 1}; // as primeiras são do plano A e C
  const mk = (arr: string[][], dest: string[]) => arr.map(([t, p]) => {
    occ[p] = (occ[p] ?? 0) + 1;
    return {t, q: w(p, occ[p]) - D0, cor: dest.includes(p) ? COR.acento : COR.creme, tam: 118};
  });
  const i1 = mk(l1, ['não', 'torra']);
  const i2 = mk(l2, ['antes']);
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={cam} id="tD">
        {/* vídeo em movimento, nunca a mão parada: a mesa densimétrica com o grão correndo
            na 1ª frase, e a lavoura ("tudo que vem antes dela") na 2ª */}
        <Plano p={1}>{k < troca
          ? <Clipe q={q} ini={D0} src="v4" de={0.2} vel={1} escuro={0.38} />
          : <Clipe q={q} ini={D0 + troca} src="v2" de={2.4} vel={1} escuro={0.38} />}</Plano>
        <Plano p={1.08}>
          <Manchete q={k} x={540} y={520} itens={i1} fonte="serifa" rot={-3} />
          <Manchete q={k} x={540} y={1430} itens={i2} fonte="serifa" rot={-2} />
        </Plano>
      </Palco>
      <Vinheta forca={0.75} />
    </AbsoluteFill>
  );
};

/** Efeitos do trecho (quadros LOCAIS a T0); a peça inteira os reaproveita deslocados. */
export function efeitosTeste(): Array<[string, number, number]> {
  return [
    ['carimbo', w('amarga'), 0.7], ['pop', w('demais'), 0.5], ['golinho', 4, 0.5],
    ...LIM.slice(1).map((l): [string, number, number] => ['chicote', l - 5, 0.55]),
    ['whoosh', w('pulada') - 8, 0.6], ['carimbo', w('pulada'), 0.75], ['thump', w('pulada') + 9, 0.7], ['pop', w('prova'), 0.4],
    ['tick', w('passou'), 0.5], ['slide', w('passou') + 2, 0.5], ['carimbo', w('conta'), 0.7], ['rasgo', w('disfarçar'), 0.6], ['carimbo', w('disfarçar') + 2, 0.5],
    ['tink', w('torra', 2) , 0.35], ['tink', w('antes'), 0.35],
  ];
}

// ------------------------------------------------------------------ montagem
const LIM = [A0, B0, C0, D0];
const PLANOS = [PlanoA, PlanoB, PlanoC, PlanoD];

export const TesteCodigo: React.FC = () => {
  const q = useCurrentFrame();
  let i = 0;
  for (let n = 0; n < LIM.length; n++) if (q >= LIM[n]) i = n;
  const P = PLANOS[i];
  // chicote: 3 quadros de cada lado da troca, borrão direcional + deslize
  const perto = LIM.slice(1).map((l) => q - l).find((d) => d >= -3 && d < 3);
  const kk = perto === undefined ? 0 : 1 - Math.abs(perto + 0.5) / 3.5;
  const desl = perto === undefined ? 0 : (perto < 0 ? -1 : 1) * (1 - Math.abs(perto + 0.5) / 3.5) * -160;
  const efeitos = efeitosTeste();
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <AbsoluteFill style={{transform: `translateX(${desl}px)`, filter: kk > 0 ? `blur(${kk * 18}px)` : undefined}}>
        <P q={q} />
      </AbsoluteFill>
      <GraoFilme q={q} forca={0.1} />
      <Audio src={staticFile('fonte/narracao.mp3')} trimBefore={Math.round(T0 * 30)} />
      <Audio src={staticFile('sfx/trilha.wav')} trimBefore={Math.round(T0 * 30)} volume={0.16} />
      {efeitos.map(([a, s, v], n) => (
        <Sequence key={n} from={Math.max(0, s)} durationInFrames={60}><Audio src={staticFile(`sfx/${a}.wav`)} volume={v * 0.75} /></Sequence>
      ))}
    </AbsoluteFill>
  );
};
