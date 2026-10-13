// Peça 08b, as cenas. Regra (estrategia.md §6): vídeo real onde existe filmagem; colagem
// e boneco de palito só para o que a câmera não pegou (o mecanismo da máquina, a peneira
// por tamanho, a prova pulada). Torra sem fogo. Embalagem só pelo recorte com laudo.
// Nenhum segundo digitado: tudo lê roteiro.ts.

import React from 'react';
import {AbsoluteFill, staticFile} from 'remotion';
import {COR} from '../../identidade/tokens';
import {cameraEm, deriva, pulso, somar, tremor, type Chave} from '../../colagem/camera';
import {Brilho, Check, Cruz, Elipse, Seta, Xis} from '../../colagem/grafismos';
import {Palco, Plano} from '../../colagem/palco';
import {Dymo, Marcador, Recortadas, Serifa} from '../../colagem/tipos';
import {Embalagem} from '../../colagem/pecas';
import {progresso} from '../../colagem/movimento-colagem';
import {andar, Boneco, poseEm, Sopro, type Pose} from '../../colagem/boneco';
import {Clipe, fala, FotoCheia, fq, Fundo, Peca, Silabas, SombraFolhas, Tachinha, Vinheta} from '../fruta/apoio';
import {CENA_INICIO, em, S0, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15} from './roteiro';

type C = {q: number};
const cam = (q: number, chaves: Chave[], chave: string, i: number, pulsos: number[] = [], tremores: number[] = []) =>
  somar(cameraEm(q, chaves), deriva(q, chave, i), pulso(q, pulsos), ...tremores.map((t) => tremor(q, t)));
const IQ = CENA_INICIO.map(fq);
const empurra = (n: number, z0 = 1, z1 = 1.08, y1 = -20): Chave[] => [
  {q: IQ[n], x: 0, y: 0, zoom: z0, rot: 0},
  {q: (IQ[n + 1] ?? IQ[n] + 60) + 6, x: 0, y: y1, zoom: z1, rot: -0.4, curva: 'linear'},
];
/** Recorte da biblioteca dentro do SVG do boneco (objeto na mão), com o mesmo boil. */
const NaMao: React.FC<{q: number; nome: string; w: number; dx?: number; dy?: number; rot?: number}> = ({q, nome, w, dx = 0, dy = 0, rot = 0}) => (
  <image href={staticFile(`colagem/${nome}-b${Math.floor(q / 3) % 3}.png`)} x={-w / 2 + dx} y={-w / 2 + dy} width={w} height={w}
    transform={`rotate(${rot})`} preserveAspectRatio="xMidYMid meet" />
);
/** Cena de vídeo real, com câmera e camada de texto. */
const Real: React.FC<{q: number; n: number; src: string; de: number; vel?: number; escuro?: number; z1?: number; children?: React.ReactNode; pulsos?: number[]}> = ({
  q, n, src, de, vel, escuro, z1 = 1.12, children, pulsos = [],
}) => (
  <AbsoluteFill style={{background: COR.preto}}>
    <Palco cam={cam(q, empurra(n, 1.02, z1, -20), `c${n}`, 1.2, pulsos)} id={`c${n}`}>
      <Plano p={1}><Clipe q={q} ini={IQ[n]} src={src} de={de} vel={vel} escuro={escuro} /></Plano>
      <Plano p={1.1}>{children}</Plano>
    </Palco>
    <Vinheta forca={0.42} />
  </AbsoluteFill>
);
/** Cena de colagem sobre papel. */
const Papel: React.FC<{q: number; n: number; cor?: string; children: React.ReactNode; pulsos?: number[]; tremores?: number[]; frente?: React.ReactNode}> = ({
  q, n, cor = COR.creme, children, pulsos = [], tremores = [], frente,
}) => (
  <AbsoluteFill>
    <Fundo cor={cor} forca={0.5} />
    <Palco cam={cam(q, empurra(n, 1.0, 1.06, -10), `c${n}`, 1, pulsos, tremores)} id={`c${n}`}>
      <Plano p={0.6}><SombraFolhas q={q} opacidade={0.15} /></Plano>
      <Plano p={1}>{children}</Plano>
      {frente && <Plano p={2.4}>{frente}</Plano>}
    </Palco>
  </AbsoluteFill>
);

// ============================================================ 0 · o punhado reprovado (gancho)
export const Cena0: React.FC<C> = ({q}) => {
  const rep = fq(S0.reprovado.inicio);
  return (
    <Real q={q} n={0} src="v5" de={8.75} vel={0.45} z1={1.22} pulsos={[fq(em(S0.reprovado, 'reprovado'))]}>
      <Silabas q={q} ini={fq(em(S0.reprovado, 'reprovado'))} dur={fq(0.7)} texto="RE/PRO/VA/DO" x={540} y={470} tamanho={220} cor="#F2D9C4" chave="c0" />
      <Xis q={q} ini={rep + 14} cx={720} cy={1150} r={170} cor={COR.acento} espessura={16} chave="c0-x" />
    </Real>
  );
};

// ============================================================ 1 · o caminho das provas
export const Cena1: React.FC<C> = ({q}) => {
  const ini = IQ[1];
  const cai = fq(S1.caminho.inicio);
  const graos = ['grao-01', 'grao-02', 'grao-03', 'grao-01', 'grao-02', 'grao-03'];
  return (
    <Papel q={q} n={1} cor="#E9DFCB" pulsos={[fq(S1.onze.inicio), cai]}>
      {/* a trilha tracejada das provas */}
      <svg style={{position: 'absolute', left: 0, top: 0}} width={1080} height={1920}>
        <path d="M60,1150 C300,1040 520,1250 760,1120 S1000,1040 1080,1100" stroke={COR.terra} strokeWidth={8} strokeDasharray="22 18" fill="none" />
      </svg>
      {graos.map((g, i) => {
        // espalhados ao longo da trilha, todos andando juntos para a direita
        const t = progresso(q, ini, IQ[2] + 6);
        const x = 90 + i * 170 + t * 110;
        const y = 1130 + Math.sin(x / 150) * 50;
        const caiu = (i === 1 || i === 4) && q > cai + i * 2;
        const dq = caiu ? q - cai - i * 2 : 0;
        return <Peca key={i} q={q} ini={ini + i * 3} nome={g} x={x} y={y + dq * dq * 0.9} w={110} rot={caiu ? dq * 8 : i * 12} />;
      })}
      <Peca q={q} ini={fq(S1.chegar.inicio) + 4} nome="xicara" x={930} y={1430} w={250} rot={4} />
      <Recortadas q={q} ini={fq(S1.onze.inicio)} texto="ONZE PROVAS" x={540} y={560} tamanho={88} chave="c1-onze" />
      <Marcador q={q} ini={cai} texto="fica pelo caminho" x={420} y={1500} tamanho={74} rot={-4} chave="c1-cam" dur={fala(S1.caminho)} />
    </Papel>
  );
};

// ============================================================ 2 · a promessa: o café que amarga
export const Cena2: React.FC<C> = ({q}) => {
  const ini = IQ[2];
  const am = fq(S2.amarga.inicio);
  const pose = poseEm(q, [
    {q: ini, pose: {bracoD: 20, cotoveloD: 10}},
    {q: ini + 25, pose: {bracoD: 115, cotoveloD: 55}},
    {q: am - 6, pose: {bracoD: 122, cotoveloD: 62, tronco: -4}},
    {q: am + 4, pose: {bracoD: 80, cotoveloD: 20, tronco: 8, bracoE: -60, cotoveloE: -30}},
  ]);
  return (
    <Papel q={q} n={2} pulsos={[am]} tremores={[am]}>
      <Boneco q={q} x={540} y={1380} h={620} pose={pose} rosto={q >= am ? 'careta' : 'normal'} chave="c2"
        naMaoD={<NaMao q={q} nome="xicara" w={120} rot={-90} dx={40} />} />
      <Serifa q={q} ini={fq(em(S2.fim, 'saber'))} texto="por que o café" x={540} y={420} tamanho={110} cor={COR.preto} rot={-3} />
      <Recortadas q={q} ini={am} texto="AMARGA?" x={540} y={600} tamanho={140} chave="c2-am" />
      <Cruz q={q} ini={am + 3} x={300} y={760} cor={COR.acento} chave="c2-c1" />
      <Cruz q={q} ini={am + 6} x={800} y={820} s={44} cor={COR.acento} chave="c2-c2" />
    </Papel>
  );
};

// ============================================================ 3 · a lavoura a 1.250 m
export const Cena3: React.FC<C> = ({q}) => (
  <AbsoluteFill style={{background: COR.preto}}>
    <Palco cam={cam(q, empurra(3, 1.0, 1.1, -30), 'c3', 1, [fq(S3.serra.inicio), fq(S3.m1250.inicio)])} id="c3">
      <Plano p={1}><FotoCheia q={q} ini={IQ[3]} dur={IQ[4] - IQ[3]} src="lavoura-1405.jpg" /></Plano>
      <Plano p={1.1}>
        <Marcador q={q} ini={fq(S3.primeira.inicio) + 2} texto="prova 1: antes da colheita" x={540} y={330} tamanho={62} rot={-3} chave="c3-p1" dur={fala(S3.primeira)} />
        <Dymo q={q} ini={fq(S3.serra.inicio)} texto="SERRA DA CANASTRA" x={540} y={500} tamanho={80} rot={-2} />
        <Recortadas q={q} ini={fq(S3.m1250.inicio)} texto="1.250 M" x={540} y={680} tamanho={150} chave="c3-m" />
      </Plano>
    </Palco>
    <Vinheta forca={0.35} />
  </AbsoluteFill>
);

// ============================================================ 4 · o refratômetro (boneco)
export const Cena4: React.FC<C> = ({q}) => {
  const ini = IQ[4];
  const r = fq(S4.refrat.inicio);
  const pose = poseEm(q, [
    {q: ini, pose: {bracoD: 30, cotoveloD: 20}},
    {q: r - 4, pose: {bracoD: 150, cotoveloD: 70, bracoE: 120, cotoveloE: -40, tronco: -6}},
    {q: r + 30, pose: {bracoD: 155, cotoveloD: 72, bracoE: 125, cotoveloE: -45, tronco: -8}},
  ]);
  return (
    <Papel q={q} n={4} cor="#E9DFCB" pulsos={[fq(S4.acucar.inicio), r, fq(S4.vinho.inicio)]}>
      <Brilho q={q} ini={ini + 2} x={840} y={360} r={150} cor="#E8B54A" />
      <Boneco q={q} x={470} y={1420} h={600} pose={pose} rosto="normal" olhar={1} chave="c4"
        naMaoD={<NaMao q={q} nome="refratometro" w={230} rot={-60} />} />
      <Peca q={q} ini={fq(S4.mede.inicio) + 4} nome="cereja-vermelha-1" x={830} y={1230} w={170} rot={10} />
      <Dymo q={q} ini={fq(S4.acucar.inicio)} texto="AÇÚCAR DO FRUTO" x={540} y={470} tamanho={78} rot={-2} />
      <Marcador q={q} ini={r} texto="refratômetro" x={760} y={980} tamanho={64} rot={6} chave="c4-r" dur={fala(S4.refrat)} />
      <Seta q={q} ini={r + 4} de={[740, 930]} para={[600, 820]} curva={0.3} cor={COR.preto} chave="c4-s" />
      <Serifa q={q} ini={fq(S4.vinho.inicio)} texto="igual uva de vinho" x={540} y={1620} tamanho={96} cor={COR.acento} rot={-3} />
    </Papel>
  );
};

// ============================================================ 5 · só o maduro (vídeo)
export const Cena5: React.FC<C> = ({q}) => (
  <Real q={q} n={5} src="v2" de={6.0} pulsos={[fq(S5.maduro.inicio)]}>
    <Silabas q={q} ini={fq(em(S5.maduro, 'maduro'))} dur={fq(0.5)} texto="SÓ O|MA/DU/RO" x={540} y={480} tamanho={180} chave="c5" />
  </Real>
);

// ============================================================ 6 · fruto verde vira amargor
export const Cena6: React.FC<C> = ({q}) => {
  const am = fq(S5.amargor.inicio);
  return (
    <Papel q={q} n={6} pulsos={[am]}>
      <Peca q={q} ini={IQ[6]} nome="cereja-verde-1" x={300} y={900} w={260} rot={-8} />
      <Seta q={q} ini={fq(em(S5.verde, 'xícara'))} de={[430, 900]} para={[640, 900]} curva={0.2} cor={COR.preto} chave="c6-s" />
      <Peca q={q} ini={fq(em(S5.verde, 'xícara'))} nome="xicara" x={800} y={900} w={300} rot={4} />
      <Dymo q={q} ini={am} texto="AMARGOR" x={700} y={1290} tamanho={80} fundo={COR.acento} rot={3} />
      <Marcador q={q} ini={IQ[6] + 2} texto="fruto verde" x={300} y={1140} tamanho={66} rot={-5} chave="c6-v" />
    </Papel>
  );
};

// ============================================================ 7 · terreiro (vídeo)
export const Cena7: React.FC<C> = ({q}) => (
  <Real q={q} n={7} src="v1" de={1.6} pulsos={[fq(S6.sol.inicio), fq(S6.fermenta.inicio)]}>
    <Silabas q={q} ini={fq(em(S6.sol, 'sol'))} dur={fq(0.4)} texto="SOL" x={540} y={420} tamanho={280} chave="c7" fora={fq(S6.terreiro.inicio)} />
    <Brilho q={q} ini={fq(em(S6.sol, 'sol')) + 3} x={830} y={330} r={120} cor={COR.acento} />
    <Marcador q={q} ini={fq(em(S6.terreiro, 'revirado'))} texto="revirado o dia inteiro" x={540} y={460} tamanho={70} rot={-3} chave="c7-r" dur={fq(0.9)} />
    <Recortadas q={q} ini={fq(S6.fermenta.inicio)} texto="SE SECAR DESIGUAL..." x={540} y={640} tamanho={70} chave="c7-f" />
  </Real>
);

// ============================================================ 8 · ardido
export const Cena8: React.FC<C> = ({q}) => {
  const ar = fq(S6.ardido.inicio);
  return (
    <Papel q={q} n={8} cor="#E9DFCB" pulsos={[ar]} tremores={[ar]}>
      <Serifa q={q} ini={IQ[8]} texto="fermentado vira" x={540} y={520} tamanho={110} cor={COR.preto} rot={-3} />
      <Peca q={q} ini={IQ[8] + 6} nome="grao-ardido" x={540} y={920} w={320} rot={-6} />
      <Dymo q={q} ini={ar} texto="ARDIDO" x={540} y={1240} tamanho={120} fundo={COR.acento} rot={-2} />
      <Elipse q={q} ini={ar + 4} cx={540} cy={920} rx={230} ry={270} cor={COR.acento} chave="c8-el" espessura={10} />
    </Papel>
  );
};

// ============================================================ 9 · sai a casca
export const Cena9: React.FC<C> = ({q}) => {
  const k = fq(S7.casca.inicio) + 6;
  return (
    <Papel q={q} n={9} pulsos={[fq(S7.peneira.inicio)]}>
      <Peca q={q} ini={IQ[9]} nome="cereja-seca" x={540} y={880} w={360} rot={6} fora={k} />
      <Peca q={q} ini={k} nome="casca" x={460} y={850} w={330} rot={-14} fora={k + 4} />
      <Peca q={q} ini={k + 2} nome="grao-01" x={560} y={900} w={280} rot={-8} />
      <Marcador q={q} ini={k} texto="sai a casca" x={540} y={1250} tamanho={80} rot={-3} chave="c9-c" />
      <Recortadas q={q} ini={fq(S7.peneira.inicio)} texto="PENEIRA FINA" x={540} y={460} tamanho={110} chave="c9-p" />
    </Papel>
  );
};

// ============================================================ 10–11 · pedra, graveto (rajada)
const Rajada: React.FC<{q: number; n: number; nome: string; texto: string; ini: number; w: number; rot: number; cor: string}> = ({
  q, n, nome, texto, ini, w, rot, cor,
}) => (
  <Papel q={q} n={n} cor={cor} pulsos={[ini]} tremores={[ini]}>
    <Peca q={q} ini={ini} nome={nome} x={540} y={900} w={w} rot={rot} />
    <Recortadas q={q} ini={ini} texto={texto} x={540} y={1300} tamanho={150} chave={`c${n}`} />
  </Papel>
);
export const Cena10: React.FC<C> = ({q}) => <Rajada q={q} n={10} nome="pedra" texto="PEDRA" ini={IQ[10]} w={420} rot={-6} cor={COR.creme} />;
export const Cena11: React.FC<C> = ({q}) => <Rajada q={q} n={11} nome="graveto" texto="GRAVETO" ini={IQ[11]} w={720} rot={-16} cor="#D9C3A0" />;

// ============================================================ 12 · grão leve (vídeo: mesa densimétrica)
export const Cena12: React.FC<C> = ({q}) => (
  <Real q={q} n={12} src="v4" de={1.8} pulsos={[fq(S8.leve.inicio), fq(S8.oco.inicio)]}>
    <Silabas q={q} ini={fq(S8.leve.inicio)} dur={fala(S8.leve)} texto="GRÃO|LE/VE" x={540} y={460} tamanho={190} chave="c12" />
    <Marcador q={q} ini={fq(S8.oco.inicio)} texto="oco por dentro" x={540} y={700} tamanho={70} rot={-3} chave="c12-o" dur={fala(S8.oco)} />
  </Real>
);

// ============================================================ 13 · a máquina que sopra (boneco)
export const Cena13: React.FC<C> = ({q}) => {
  const ini = IQ[13];
  const d = fq(S8.defeitos.inicio);
  const sp = fq(em(S8.sopro, 'sopro'));
  // a esteira de grãos descendo; o preto sai voando no sopro
  const fluxo = Array.from({length: 9}, (_, i) => i);
  const pose = poseEm(q, [
    {q: ini, pose: {tronco: 18, bracoD: 70, cotoveloD: 60, bracoE: 40, cotoveloE: 20}},
    {q: sp - 4, pose: {tronco: 22, bracoD: 80, cotoveloD: 70, bracoE: 50, cotoveloE: 30}},
    {q: sp + 2, pose: {tronco: 10, bracoD: 60, cotoveloD: 50, bracoE: 30, cotoveloE: 20}},
  ]);
  return (
    <Papel q={q} n={13} cor="#E9DFCB" pulsos={[d, sp]} tremores={[sp]}>
      <svg style={{position: 'absolute', left: 0, top: 0}} width={1080} height={1920}>
        <path d="M640,380 L640,1500" stroke={COR.terra} strokeWidth={10} strokeDasharray="4 22" strokeLinecap="round" />
      </svg>
      {fluxo.map((i) => {
        const y = 380 + ((q - ini) * 9 + i * 130) % 1120;
        return <Peca key={i} q={q} ini={ini} nome={i % 3 === 0 ? 'grao-02' : 'grao-03'} x={640} y={y} w={90} rot={i * 23} sombra={false} />;
      })}
      {/* o grão preto: desce, e no "sopro" voa para a direita */}
      {q < sp ? (
        <Peca q={q} ini={d} nome="grao-preto" x={640} y={420 + Math.min(1, (q - d) / 40) * 560} w={120} rot={(q - d) * 4} />
      ) : (
        <Peca q={q} ini={d} nome="grao-preto" x={640 + (q - sp) * 38} y={980 - (q - sp) * 10} w={120} rot={(q - sp) * 30} />
      )}
      <Sopro q={q} ini={sp} x={560} y={980} dir={1} tam={150} />
      <Boneco q={q} x={330} y={1500} h={560} pose={pose} rosto={q >= sp ? 'sopro' : 'normal'} olhar={1} chave="c13"
        naMaoD={<NaMao q={q} nome="lupa" w={200} rot={-90} />} />
      <Marcador q={q} ini={fq(em(S8.maquina, 'grão'))} texto="grão por grão" x={330} y={430} tamanho={70} rot={-4} chave="c13-g" />
      <Dymo q={q} ini={d} texto="PRETO · VERDE · ARDIDO" x={540} y={1650} tamanho={64} rot={-1} />
      <Recortadas q={q} ini={sp} texto="FFFT!" x={880} y={820} tamanho={100} chave="c13-f" />
    </Papel>
  );
};

// ============================================================ 14 · peneiras por tamanho (boneco)
export const Cena14: React.FC<C> = ({q}) => {
  const ini = IQ[14];
  const t = fq(S9.tamanho.inicio);
  const pose: Pose = poseEm(q, [
    {q: ini, pose: {bracoD: 40, cotoveloD: 20}},
    {q: t, pose: {bracoD: 110, cotoveloD: 10, bracoE: -30}},
    {q: t + 40, pose: {bracoD: 115, cotoveloD: 12, bracoE: -30, ...andar(q, 20, 6)}},
  ]);
  const tam = [130, 180, 240];
  return (
    <Papel q={q} n={14} pulsos={[t, fq(em(S9.porque, 'igual'))]}>
      <Peca q={q} ini={ini} nome="peneira-classificacao" x={640} y={760} w={480} rot={-4} />
      {tam.map((w, i) => (
        <Peca key={i} q={q} ini={t + i * 4} nome={['grao-01', 'grao-02', 'grao-03'][i]} x={430 + i * 210} y={1200} w={w * 0.8} rot={i * 9} />
      ))}
      <Boneco q={q} x={190} y={1560} h={520} pose={pose} rosto="sorriso" chave="c14" />
      <Silabas q={q} ini={t} dur={fala(S9.tamanho)} texto="TA/MA/NHO" x={540} y={380} tamanho={170} cor={COR.preto} chave="c14-t" />
      <Marcador q={q} ini={fq(em(S9.porque, 'torram'))} texto="torra por igual" x={700} y={1360} tamanho={66} rot={-3} chave="c14-i" />
    </Papel>
  );
};

// ============================================================ 15 · a virada: nenhuma prova na torra (vídeo)
export const Cena15: React.FC<C> = ({q}) => {
  const nen = fq(S10.nenhuma.inicio);
  return (
    <Real q={q} n={15} src="v3" de={0} vel={0.5} escuro={0.35} pulsos={[nen]}>
      <Serifa q={q} ini={fq(em(S10.aqui, 'quase'))} texto="o que quase ninguém sabe" x={540} y={420} tamanho={82} cor={COR.creme} rot={-3} />
      <Recortadas q={q} ini={nen} texto="NENHUMA" x={540} y={620} tamanho={118} chave="c15-n" />
      <Marcador q={q} ini={fq(em(S10.nenhuma, 'torra'))} texto="acontece na torra" x={540} y={820} tamanho={70} rot={3} chave="c15-t" dur={fq(0.35)} />
    </Real>
  );
};

// ============================================================ 16 · prova pulada + disfarce (boneco)
export const Cena16: React.FC<C> = ({q}) => {
  const ini = IQ[16];
  const p = fq(em(S11.pulada, 'pulada'));
  const dsf = fq(em(S11.disfarcar, 'disfarçar'));
  // o boneco corre e PULA a barreira "PROVA"; depois puxa um pano sobre os grãos ruins
  // o pico do salto cai em cima da barreira (x ≈ 480) exatamente no "pulada"
  const corre = q < p + 14;
  // corre até x = 290 (antes da barreira) e o salto inteiro atravessa de 290 a 650
  const xb = q < p - 8 ? 110 + Math.min(1, Math.max(0, (q - ini) / (p - 8 - ini))) * 180 : 290 + Math.min(1, (q - p + 8) / 20) * 360;
  const salto = q > p - 8 && q < p + 12 ? Math.sin(((q - (p - 8)) / 20) * Math.PI) * 400 : 0;
  const pose = corre ? poseEm(q, [{q: ini, pose: andar(q, 12, 34)}]) :
    poseEm(q, [{q: p + 14, pose: {bracoD: 60, bracoE: -60}}, {q: dsf, pose: {bracoD: 120, cotoveloD: 30, bracoE: 100, cotoveloE: -20, tronco: 12}}]);
  const pano = progresso(q, dsf - 16, dsf - 4);
  return (
    <Papel q={q} n={16} cor="#E9DFCB" pulsos={[p, dsf]}>
      {/* a barreira PROVA */}
      <div style={{position: 'absolute', left: 380, top: 1240, width: 200, height: 26, background: COR.acento, boxShadow: '0 6px 10px rgba(0,0,0,0.3)'}} />
      <div style={{position: 'absolute', left: 392, top: 1266, width: 14, height: 220, background: COR.terra}} />
      <div style={{position: 'absolute', left: 554, top: 1266, width: 14, height: 220, background: COR.terra}} />
      <Dymo q={q} ini={ini + 2} texto="PROVA" x={480} y={1200} tamanho={52} rot={-2} digitar={false} />
      <Boneco q={q} x={xb} y={1490 - salto} h={460} pose={pose} rosto={corre ? 'sorriso' : 'normal'} chave="c16" espelhar={false} />
      <Marcador q={q} ini={p} texto="pulada!" x={780} y={880} tamanho={80} rot={6} chave="c16-p" />
      {/* grãos ruins e o pano que "disfarça" */}
      {['grao-preto', 'grao-imaturo', 'grao-ardido'].map((g, i) => (
        <Peca key={g} q={q} ini={fq(S11.disfarcar.inicio)} nome={g} x={770 + i * 95} y={1440} w={110} rot={i * 20 - 10} />
      ))}
      {pano > 0 && (
        <div style={{position: 'absolute', left: 700, top: 1350, width: 330 * pano, height: 190, background: '#6B4A33',
          clipPath: 'polygon(0 8%,100% 0,98% 92%,2% 100%)', boxShadow: '0 10px 18px rgba(0,0,0,0.35)'}} />
      )}
      <Dymo q={q} ini={dsf - 4} texto="DISFARCE" x={860} y={1290} tamanho={56} rot={2} />
      <Serifa q={q} ini={fq(em(S11.quando, 'amarga'))} texto="amarga demais?" x={540} y={460} tamanho={110} cor={COR.preto} rot={-3} />
    </Papel>
  );
};

// ============================================================ 17 · a frase, no escuro
export const Cena17: React.FC<C> = ({q}) => (
  <AbsoluteFill style={{background: COR.preto}}>
    <Palco cam={cam(q, empurra(17, 1.06, 1.18, 0), 'c17', 0.5)} id="c17">
      <Plano p={1}><Clipe q={q} ini={IQ[17]} src="v5" de={13.3} vel={0.5} escuro={0.45} /></Plano>
    </Palco>
    <Vinheta forca={0.8} />
    {/* a tese do vídeo não pode ficar só na legenda pequena */}
    <Serifa q={q} ini={fq(em(S12.bom, 'não'))} texto="não se faz na torra." x={540} y={560} tamanho={100} cor={COR.creme} rot={-3} />
    <Serifa q={q} ini={fq(em(S12.antes, 'antes'))} texto="se faz antes dela." x={540} y={740} tamanho={100} cor={COR.acento} rot={-2} />
  </AbsoluteFill>
);

// ============================================================ 18 · o Arthur prova (vídeo)
export const Cena18: React.FC<C> = ({q}) => (
  <Real q={q} n={18} src="v6" de={0.9} z1={1.16} pulsos={[fq(S13.xicara.inicio)]}>
    <Silabas q={q} ini={fq(S13.xicara.inicio)} dur={fala(S13.xicara)} texto="NA XÍ/CA/RA" x={540} y={400} tamanho={170} chave="c18" />
    <Dymo q={q} ini={fq(em(S13.arthur, 'Arthur'))} texto="ARTHUR · PROVA" x={540} y={1280} tamanho={58} rot={-2} />
  </Real>
);

// ============================================================ 19 · a ficha de notas
export const Cena19: React.FC<C> = ({q}) => {
  const itens: Array<[string, number]> = [['AROMA', fq(S13.aroma.inicio)], ['CORPO', fq(S13.corpo.inicio)], ['DOÇURA', fq(S13.docura.inicio)], ['CITRICIDADE', fq(S13.citric.inicio)]];
  return (
    <Papel q={q} n={19} pulsos={itens.map((i) => i[1])}>
      <Peca q={q} ini={IQ[19]} nome="post-it" x={540} y={900} w={820} rot={-2} />
      <Marcador q={q} ini={IQ[19] + 2} texto="ficha de prova" x={540} y={600} tamanho={64} papel={null} tinta={COR.preto} rot={-2} chave="c19-f" />
      {itens.map(([t, ini], i) => (
        <React.Fragment key={t}>
          <Dymo q={q} ini={ini} texto={t} x={420} y={760 + i * 120} tamanho={56} rot={-1} />
          <Check q={q} ini={ini + 4} cx={800} cy={760 + i * 120} r={36} cor={COR.acento} chave={`c19-${i}`} espessura={10} />
        </React.Fragment>
      ))}
      <Peca q={q} ini={IQ[19]} nome="xicara-prova" x={210} y={1420} w={260} rot={-6} />
    </Papel>
  );
};

// ============================================================ 20 · os pacotes reais, 80+
export const Cena20: React.FC<C> = ({q}) => {
  const o = fq(S13.oitenta.inicio);
  return (
    <Papel q={q} n={20} pulsos={[o]}>
      <Embalagem q={q} ini={IQ[20]} sku="classico" x={340} y={980} h={1250} rot={-4} />
      <Embalagem q={q} ini={IQ[20] + 6} sku="suave" x={760} y={1000} h={1250} rot={4} />
      <Recortadas q={q} ini={o} texto="80+" x={540} y={360} tamanho={230} chave="c20-80" />
      <Marcador q={q} ini={o + 6} texto="pontos" x={790} y={470} tamanho={66} rot={6} chave="c20-p" />
    </Papel>
  );
};

// ============================================================ 21 · o punhado do começo (laço)
export const Cena21: React.FC<C> = ({q}) => (
  <Real q={q} n={21} src="v5" de={8.75} vel={0.5} pulsos={[fq(em(S14.ficou, 'fazenda'))]}>
    <Marcador q={q} ini={fq(S14.ficou.inicio)} texto="ficou lá na fazenda" x={540} y={460} tamanho={78} rot={-3} chave="c21" dur={fala(S14.ficou)} />
  </Real>
);

// ============================================================ 22 · CTA
export const Cena22: React.FC<C> = ({q}) => (
  <Papel q={q} n={22} cor="#E9DFCB" pulsos={[fq(em(S15.manda, 'igual'))]}>
    <Peca q={q} ini={IQ[22]} nome="xicara" x={540} y={760} w={560} rot={3} />
    <Tachinha q={q} ini={IQ[22] + 4} x={540} y={480} cor="terra" />
    <Marcador q={q} ini={IQ[22] + 2} texto="manda pra quem acha" x={540} y={1110} tamanho={70} rot={-3} chave="c22-a" />
    <Serifa q={q} ini={fq(em(S15.manda, 'tudo'))} texto="que café é tudo igual" x={540} y={1260} tamanho={92} cor={COR.acento} rot={-2} />
  </Papel>
);

export const CENAS = [Cena0, Cena1, Cena2, Cena3, Cena4, Cena5, Cena6, Cena7, Cena8, Cena9, Cena10, Cena11, Cena12, Cena13,
  Cena14, Cena15, Cena16, Cena17, Cena18, Cena19, Cena20, Cena21, Cena22];
