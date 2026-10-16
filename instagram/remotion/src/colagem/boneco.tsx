// Boneco de palito (stick figure) desenhado em código, no mesmo idioma da colagem:
// traço de caneta com ponta redonda, "boil" de 3 quadros (o traço treme como desenho
// à mão) e poses por quadro-chave. Não é animação gerada: é desenho vetorial, então
// nunca se confunde com filmagem — serve para explicar o MECANISMO de uma etapa que
// a câmera não mostrou (a máquina que sopra o grão, a peneira por tamanho).
//
// Ângulos em graus, 0 = apontando para baixo, positivo = sentido anti-horário na tela
// (o braço com 90° aponta para a DIREITA do boneco visto de frente).

import React from 'react';
import {COR} from '../identidade/tokens';
import {semente} from './semente';

export type Pose = {
  tronco: number; // inclinação do tronco (0 = em pé)
  bracoE: number; cotoveloE: number; bracoD: number; cotoveloD: number;
  pernaE: number; joelhoE: number; pernaD: number; joelhoD: number;
};
export type Rosto = 'normal' | 'careta' | 'sopro' | 'sorriso' | 'espanto';

export const POSE_EM_PE: Pose = {tronco: 0, bracoE: -18, cotoveloE: -8, bracoD: 18, cotoveloD: 8, pernaE: -8, joelhoE: 0, pernaD: 8, joelhoD: 0};

/** Interpola entre quadros-chave de pose (suave nas pontas). */
export function poseEm(q: number, chaves: Array<{q: number; pose: Partial<Pose>}>, base: Pose = POSE_EM_PE): Pose {
  const cheias = chaves.map((c) => ({q: c.q, pose: {...base, ...c.pose}}));
  if (q <= cheias[0].q) return cheias[0].pose;
  for (let i = 0; i < cheias.length - 1; i++) {
    const a = cheias[i], b = cheias[i + 1];
    if (q <= b.q) {
      const t = (q - a.q) / Math.max(1, b.q - a.q);
      const e = t * t * (3 - 2 * t);
      const r = {} as Pose;
      (Object.keys(a.pose) as Array<keyof Pose>).forEach((k) => (r[k] = a.pose[k] + (b.pose[k] - a.pose[k]) * e));
      return r;
    }
  }
  return cheias[cheias.length - 1].pose;
}

/** Ciclo de caminhada: fase em quadros. */
export function andar(q: number, periodo = 16, amp = 28): Partial<Pose> {
  const s = Math.sin((q / periodo) * Math.PI * 2);
  return {pernaE: s * amp, joelhoE: Math.max(0, -s) * 30, pernaD: -s * amp, joelhoD: Math.max(0, s) * 30,
    bracoE: -s * amp * 0.7, bracoD: s * amp * 0.7, cotoveloE: -12, cotoveloD: 12};
}

const rad = (g: number) => (g * Math.PI) / 180;
/** Ponto a partir de `p`, com comprimento `l` e ângulo `g` (0 = para baixo). */
const segue = (p: [number, number], l: number, g: number): [number, number] => [p[0] + Math.sin(rad(g)) * l, p[1] + Math.cos(rad(g)) * l];

/**
 * Boneco. (x, y) = pés no chão; h = altura total em px. `naMaoD` desenha um objeto
 * (recorte da biblioteca, por exemplo) preso à mão direita, girado com o antebraço.
 */
export const Boneco: React.FC<{
  q: number; x: number; y: number; h: number; pose: Pose; rosto?: Rosto; cor?: string; espelhar?: boolean;
  naMaoD?: React.ReactNode; naMaoE?: React.ReactNode; chave: string; olhar?: number; opacidade?: number;
}> = ({q, x, y, h, pose, rosto = 'normal', cor = COR.preto, espelhar, naMaoD, naMaoE, chave, olhar = 0, opacidade = 1}) => {
  // boil: o desenho todo treme um pouco a cada 3 quadros, como a colagem
  const fase = Math.floor(q / 3) % 3;
  const s = semente(`${chave}#${fase}`);
  const j = () => (s() - 0.5) * h * 0.012;
  const W = h * 0.034;
  const lPerna = h * 0.24, lTronco = h * 0.3, lBraco = h * 0.17, rCabeca = h * 0.1;
  const quadril: [number, number] = [0, -lPerna * 2];
  const pescoco = segue(quadril, lTronco, 180 + pose.tronco);
  const ombro = segue(quadril, lTronco * 0.88, 180 + pose.tronco);
  const cabeca = segue(pescoco, rCabeca * 1.05, 180 + pose.tronco);
  const jE = segue(quadril, lPerna, pose.pernaE), pE = segue(jE, lPerna, pose.pernaE + pose.joelhoE);
  const jD = segue(quadril, lPerna, pose.pernaD), pD = segue(jD, lPerna, pose.pernaD - pose.joelhoD);
  const cE = segue(ombro, lBraco, pose.bracoE), mE = segue(cE, lBraco, pose.bracoE + pose.cotoveloE);
  const cD = segue(ombro, lBraco, pose.bracoD), mD = segue(cD, lBraco, pose.bracoD + pose.cotoveloD);
  const lin = (pts: Array<[number, number]>) => 'M' + pts.map((p) => `${(p[0] + j()).toFixed(1)},${(p[1] + j()).toFixed(1)}`).join(' L');
  const angAnteD = pose.bracoD + pose.cotoveloD, angAnteE = pose.bracoE + pose.cotoveloE;
  const ox = olhar * rCabeca * 0.25;
  const olhos = (
    <g fill={cor}>
      <circle cx={cabeca[0] - rCabeca * 0.35 + ox} cy={cabeca[1] - rCabeca * 0.1} r={W * 0.38} />
      <circle cx={cabeca[0] + rCabeca * 0.35 + ox} cy={cabeca[1] - rCabeca * 0.1} r={W * 0.38} />
    </g>
  );
  const bx = cabeca[0] + ox, by = cabeca[1] + rCabeca * 0.42, bw = rCabeca * 0.42;
  const boca = {
    normal: <path d={`M${bx - bw},${by} Q${bx},${by + bw * 0.35} ${bx + bw},${by}`} />,
    sorriso: <path d={`M${bx - bw},${by - bw * 0.2} Q${bx},${by + bw * 0.9} ${bx + bw},${by - bw * 0.2}`} />,
    careta: <path d={`M${bx - bw},${by + bw * 0.1} L${bx - bw * 0.35},${by - bw * 0.25} L${bx + bw * 0.25},${by + bw * 0.2} L${bx + bw},${by - bw * 0.15}`} />,
    sopro: <circle cx={bx + bw * 0.4} cy={by} r={bw * 0.32} />,
    espanto: <ellipse cx={bx} cy={by} rx={bw * 0.35} ry={bw * 0.5} />,
  }[rosto];
  const preso = (m: [number, number], ang: number, node?: React.ReactNode) =>
    node ? <g transform={`translate(${m[0]},${m[1]}) rotate(${-ang + 90})`}>{node}</g> : null;
  return (
    <svg style={{position: 'absolute', left: x - h, top: y - h * 1.6, overflow: 'visible', opacity: opacidade}} width={h * 2} height={h * 2}>
      <g transform={`translate(${h},${h * 1.6}) scale(${espelhar ? -1 : 1},1)`}
        stroke={cor} strokeWidth={W} strokeLinecap="round" strokeLinejoin="round" fill="none">
        <path d={lin([pE, jE, quadril, jD, pD])} />
        <path d={lin([quadril, pescoco])} />
        <path d={lin([mE, cE, ombro, cD, mD])} />
        <circle cx={cabeca[0] + j()} cy={cabeca[1] + j()} r={rCabeca} fill={COR.creme} strokeWidth={W * 0.75} />
        {olhos}
        <g strokeWidth={W * 0.7} fill={rosto === 'sopro' || rosto === 'espanto' ? cor : 'none'}>{boca}</g>
        {rosto === 'careta' && (
          <path d={`M${cabeca[0] - rCabeca * 0.55},${cabeca[1] - rCabeca * 0.55} L${cabeca[0] - rCabeca * 0.15},${cabeca[1] - rCabeca * 0.4} M${cabeca[0] + rCabeca * 0.55},${cabeca[1] - rCabeca * 0.55} L${cabeca[0] + rCabeca * 0.15},${cabeca[1] - rCabeca * 0.4}`} strokeWidth={W * 0.6} />
        )}
        {preso(mD, angAnteD, naMaoD)}
        {preso(mE, angAnteE, naMaoE)}
      </g>
    </svg>
  );
};

/** Linhas de vento/ar (o "sopro"): três traços curvos que crescem a partir de (x, y). */
export const Sopro: React.FC<{q: number; ini: number; x: number; y: number; dir?: 1 | -1; tam?: number; cor?: string}> = ({
  q, ini, x, y, dir = 1, tam = 160, cor = COR.preto,
}) => {
  if (q < ini) return null;
  const k = Math.min(1, (q - ini) / 6);
  return (
    <svg style={{position: 'absolute', left: x, top: y - tam / 2, overflow: 'visible'}} width={tam} height={tam}>
      {[-0.28, 0, 0.28].map((o, i) => {
        const L = tam * k * (1 - Math.abs(o));
        const yy = tam / 2 + o * tam;
        return <path key={i} d={`M0,${yy} q${(dir * L) / 2},${-tam * 0.08} ${dir * L},0`} stroke={cor} strokeWidth={7} fill="none" strokeLinecap="round" />;
      })}
    </svg>
  );
};
