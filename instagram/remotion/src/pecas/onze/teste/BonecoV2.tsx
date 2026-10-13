// Boneco v2 (teste A/B de 13/10/2026). O v1 foi reprovado como "bugado": o corpo inteiro
// fervia a cada 3 quadros (o boil da colagem aplicado ao traço lia como falha) e os membros
// eram retas quebradas. Aqui, pelo método do kaomei/stickman-video-director: desenho
// travado (cabeça vazia, traço de espessura única), membros em curva contínua ("mangueira"),
// poses fortes com antecipação, achatamento no impacto e o boneco nunca parado.

import React from 'react';
import {COR} from '../../../identidade/tokens';

export type PoseV2 = {
  tronco: number; // inclinação (graus, + = para a frente/direita)
  bE: number; cE: number; bD: number; cD: number; // braço e cotovelo
  pE: number; jE: number; pD: number; jD: number; // perna e joelho
  sq?: number; // achatamento: + achata, - estica
  cab?: number; // inclinação extra da cabeça
};
export type RostoV2 = 'calmo' | 'careta' | 'susto' | 'assobio' | 'foco' | 'esforco' | 'sorriso';

export const EM_PE: PoseV2 = {tronco: 0, bE: -14, cE: -6, bD: 14, cD: 6, pE: -7, jE: 0, pD: 7, jD: 0};

const ease = (t: number) => t * t * (3 - 2 * t);
export function mistura(a: PoseV2, b: PoseV2, t: number): PoseV2 {
  const e = ease(Math.min(1, Math.max(0, t)));
  const r = {} as PoseV2;
  (Object.keys({...EM_PE, sq: 0, cab: 0}) as Array<keyof PoseV2>).forEach((k) => {
    r[k] = (a[k] ?? 0) + ((b[k] ?? 0) - (a[k] ?? 0)) * e;
  });
  return r;
}
/** Quadros-chave de pose, interpolação suave. */
export function chaves(q: number, ks: Array<[number, Partial<PoseV2>]>): PoseV2 {
  const c = ks.map(([k, p]) => [k, {...EM_PE, ...p}] as [number, PoseV2]);
  if (q <= c[0][0]) return c[0][1];
  for (let i = 1; i < c.length; i++) if (q <= c[i][0]) return mistura(c[i - 1][1], c[i][1], (q - c[i - 1][0]) / Math.max(1, c[i][0] - c[i - 1][0]));
  return c[c.length - 1][1];
}
/** Corrida de verdade: tronco inclinado, braços a 90° bombeando, joelho alto. */
export function corrida(q: number, periodo = 11): PoseV2 & {bob: number} {
  const f = (q / periodo) * Math.PI * 2;
  const s = Math.sin(f);
  return {
    tronco: 16, cab: -6,
    pE: s * 48, jE: Math.max(0, -Math.cos(f)) * 75 + 10, pD: -s * 48, jD: Math.max(0, Math.cos(f)) * 75 + 10,
    bE: -s * 55, cE: 85, bD: s * 55, cD: 85,
    bob: Math.abs(Math.cos(f)) * 0.05,
  };
}

/** Caminhada tranquila (o "andar" calmo que o teste aprovou). */
export function caminhada(q: number, periodo = 16): PoseV2 & {bob: number} {
  const s = Math.sin((q / periodo) * Math.PI * 2);
  return {tronco: 5, pE: s * 26, jE: Math.max(0, -s) * 22 + 6, pD: -s * 26, jD: Math.max(0, s) * 22 + 6,
    bE: -s * 22, cE: 15, bD: s * 22, cD: 15, bob: Math.abs(Math.cos((q / periodo) * Math.PI * 2)) * 0.02};
}

/** IK de dois segmentos iguais: ângulos de braço e cotovelo para a mão chegar em `t`. */
function ik(o: [number, number], t: [number, number], l: number, dobra: 1 | -1, lado: 'D' | 'E'): Partial<PoseV2> {
  const dx = t[0] - o[0], dy = t[1] - o[1];
  const d = Math.min(Math.hypot(dx, dy), 2 * l * 0.999);
  const th = (Math.atan2(dx, dy) * 180) / Math.PI;
  const a = (Math.acos(d / (2 * l)) * 180) / Math.PI;
  const b = th + dobra * a, c = -2 * dobra * a;
  return lado === 'D' ? {bD: b, cD: c} : {bE: b, cE: c};
}
/** Pontos do corpo em fração de h (boneco em pé, tronco 0). */
export const ANAT = {olhoY: -0.905, bocaY: -0.85, cabecaY: -0.893, ombroY: -0.74, peitoY: -0.6};

const rad = (g: number) => (g * Math.PI) / 180;
const segue = (p: [number, number], l: number, g: number): [number, number] => [p[0] + Math.sin(rad(g)) * l, p[1] + Math.cos(rad(g)) * l];
/** Curva que PASSA pelo joelho/cotovelo (controle refletido): membro contínuo, sem quina. */
const membro = (a: [number, number], j: [number, number], b: [number, number]) => {
  const cx = 2 * j[0] - (a[0] + b[0]) / 2, cy = 2 * j[1] - (a[1] + b[1]) / 2;
  return `M${a[0].toFixed(1)},${a[1].toFixed(1)} Q${cx.toFixed(1)},${cy.toFixed(1)} ${b[0].toFixed(1)},${b[1].toFixed(1)}`;
};

export const BonecoV2: React.FC<{
  x: number; y: number; h: number; pose: PoseV2; rosto?: RostoV2; cor?: string; papel?: string;
  espelhar?: boolean; naMao?: React.ReactNode; naMaoE?: React.ReactNode; bob?: number;
  /** Alvo da mão (em fração de h, a partir dos pés; y negativo = para cima). Resolve o braço por IK. */
  alvoD?: [number, number]; alvoE?: [number, number];
  /** Giro ABSOLUTO do objeto na mão (graus). Sem isto o objeto gira com o antebraço — foi assim
      que a caneca da v2 virou de cabeça para baixo. */
  giroD?: number; giroE?: number;
  /** Com q: respira e pisca (o boneco nunca fica morto). */
  q?: number;
}> = ({x, y, h, pose: pose0, rosto = 'calmo', cor = COR.preto, papel = '#F6F1E6', espelhar, naMao, naMaoE, bob: bob0 = 0, alvoD, alvoE, giroD, giroE, q}) => {
  const pose = {...pose0};
  const bob = bob0 + (q === undefined ? 0 : (Math.sin(q / 22) * 0.5 + 0.5) * 0.006);
  const W = h * 0.034;
  const lP = h * 0.245, lT = h * 0.29, lB = h * 0.175, r = h * 0.105;
  const sq = pose.sq ?? 0;
  const quadril: [number, number] = [0, -lP * 2 * (1 - Math.max(0, sq) * 0.5) - bob * h];
  const pesc = segue(quadril, lT, 180 + pose.tronco);
  const ombro = segue(quadril, lT * 0.86, 180 + pose.tronco);
  const cab = segue(pesc, r * 1.08, 180 + pose.tronco + (pose.cab ?? 0));
  const jE = segue(quadril, lP, pose.pE), pE = segue(jE, lP, pose.pE - pose.jE);
  const jD = segue(quadril, lP, pose.pD), pD = segue(jD, lP, pose.pD - pose.jD);
  if (alvoD) Object.assign(pose, ik(ombro, [alvoD[0] * h, alvoD[1] * h], lB, 1, 'D'));
  if (alvoE) Object.assign(pose, ik(ombro, [alvoE[0] * h, alvoE[1] * h], lB, -1, 'E'));
  const cE = segue(ombro, lB, pose.bE), mE = segue(cE, lB, pose.bE + pose.cE);
  const cD = segue(ombro, lB, pose.bD), mD = segue(cD, lB, pose.bD + pose.cD);
  const pisca = q !== undefined && (rosto === 'calmo' || rosto === 'sorriso') && q % 83 < 3;
  const ang = pose.bD + pose.cD;
  const [hx, hy] = cab;
  const o = r * 0.36;
  const olhos = pisca ? <><path d={`M${hx - o - W},${hy - r * 0.12} h${W * 2}`} /><path d={`M${hx + o - W},${hy - r * 0.12} h${W * 2}`} /></> : {
    calmo: <><circle cx={hx - o} cy={hy - r * 0.12} r={W * 0.42} fill={cor} /><circle cx={hx + o} cy={hy - r * 0.12} r={W * 0.42} fill={cor} /></>,
    foco: <><path d={`M${hx - o - W},${hy - r * 0.12} h${W * 2}`} /><path d={`M${hx + o - W},${hy - r * 0.12} h${W * 2}`} /></>,
    careta: <><path d={`M${hx - o - W},${hy - r * 0.3} l${W * 2},${W}  l${-W * 2},${W}`} /><path d={`M${hx + o + W},${hy - r * 0.3} l${-W * 2},${W} l${W * 2},${W}`} /></>,
    susto: <><circle cx={hx - o} cy={hy - r * 0.15} r={W * 0.9} fill="none" /><circle cx={hx + o} cy={hy - r * 0.15} r={W * 0.9} fill="none" /></>,
    assobio: <><path d={`M${hx - o - W},${hy - r * 0.1} q${W},${-W} ${W * 2},0`} /><path d={`M${hx + o - W},${hy - r * 0.1} q${W},${-W} ${W * 2},0`} /></>,
    esforco: <><path d={`M${hx - o - W},${hy - r * 0.3} l${W * 2},${W}`} /><path d={`M${hx + o + W},${hy - r * 0.3} l${-W * 2},${W}`} /></>,
  }[rosto === 'sorriso' ? 'calmo' : rosto];
  const by = hy + r * 0.42;
  const boca = {
    calmo: <path d={`M${hx - r * 0.3},${by} q${r * 0.3},${r * 0.18} ${r * 0.6},0`} />,
    foco: <path d={`M${hx - r * 0.22},${by} h${r * 0.44}`} />,
    careta: <path d={`M${hx - r * 0.38},${by + r * 0.05} l${r * 0.19},${-r * 0.14} l${r * 0.19},${r * 0.14} l${r * 0.19},${-r * 0.14} l${r * 0.19},${r * 0.14}`} />,
    susto: <ellipse cx={hx} cy={by + r * 0.04} rx={r * 0.13} ry={r * 0.2} fill={cor} />,
    assobio: <circle cx={hx + r * 0.12} cy={by} r={r * 0.1} fill="none" />,
    esforco: <path d={`M${hx - r * 0.3},${by + r * 0.08} q${r * 0.3},${-r * 0.2} ${r * 0.6},0`} />,
    sorriso: <path d={`M${hx - r * 0.38},${by - r * 0.05} q${r * 0.38},${r * 0.42} ${r * 0.76},0`} />,
  }[rosto];
  return (
    <svg style={{position: 'absolute', left: x - h * 1.2, top: y - h * 1.8, overflow: 'visible'}} width={h * 2.4} height={h * 2}>
      <g transform={`translate(${h * 1.2},${h * 1.8}) scale(${(espelhar ? -1 : 1) * (1 + sq * 0.35)},${1 - sq * 0.3})`}
        stroke={cor} strokeWidth={W} strokeLinecap="round" strokeLinejoin="round" fill="none">
        <path d={membro(quadril, jE, pE)} />
        <path d={membro(quadril, jD, pD)} />
        <path d={`M${quadril[0]},${quadril[1]} L${pesc[0]},${pesc[1]}`} />
        <path d={membro(ombro, cE, mE)} />
        <path d={membro(ombro, cD, mD)} />
        {/* a cabeça fica SEMPRE por cima dos braços: o v2 cobria o rosto com o antebraço */}
        <circle cx={hx} cy={hy} r={r} fill={papel} strokeWidth={W * 0.85} />
        <g strokeWidth={W * 0.6}>{olhos}{boca}</g>
        {naMao && <g transform={`translate(${mD[0]},${mD[1]}) rotate(${giroD ?? -ang + 90})`} stroke="none">{naMao}</g>}
        {naMaoE && <g transform={`translate(${mE[0]},${mE[1]}) rotate(${giroE ?? -(pose.bE + pose.cE) + 90})`} stroke="none">{naMaoE}</g>}
      </g>
    </svg>
  );
};
