// Peça 08b, v2 (13/10/2026) — a peça inteira na linguagem aprovada no teste A/B:
//   - sem pílula de legenda; só palavra-chave, entrando no quadro em que a voz a diz
//   - boneco v2 com UMA ação física por cena; câmera sempre andando; parallax em 3 planos
//   - vídeo real sempre em movimento (nunca a mão parada); nenhum trecho de clipe repetido
//   - ritmo calmo: a voz já é acelerada, o movimento não compete com ela
// O trecho 55,65–65,78 s é o do teste, aprovado como está (teste/TesteCodigo.tsx).
// Nenhum tempo digitado: tudo lê roteiro.ts. Torra sem fogo, fumaça ou grão preto (lição 66).

import {Audio} from '@remotion/media';
import React from 'react';
import {AbsoluteFill, Img, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {PILHA} from '../../../identidade/tipografia';
import {COR} from '../../../identidade/tokens';
import {cameraEm, deriva, pulso, somar, tremor, type Chave} from '../../../colagem/camera';
import {Palco, Plano} from '../../../colagem/palco';
import {Dymo} from '../../../colagem/tipos';
import {Brilho, Check, Elipse, Seta} from '../../../colagem/grafismos';
import {Embalagem} from '../../../colagem/pecas';
import {Clipe, fq, Fundo, GraoFilme, Peca, SombraFolhas, Vinheta} from '../../fruta/apoio';
import {em, FIM, PALAVRAS, S0, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S13, S14, S15} from '../roteiro';
import {BonecoV2, caminhada, chaves, EM_PE, type PoseV2} from '../teste/BonecoV2';
import {Amargor, Caneca, ease, efeitosTeste, lin, Manchete, PlanoA, PlanoB, PlanoC, PlanoD, T0, A0, B0, C0, D0} from '../teste/TesteCodigo';

export const DURACAO_ONZE2 = fq(FIM);
const F = fq;
type P = {q: number; ini: number; fim: number};

// ------------------------------------------------------------------ moldes
const cam = (q: number, k: number, ks: Chave[], id: string, extra: Array<ReturnType<typeof pulso>> = []) =>
  somar(cameraEm(k, ks), deriva(q, id, 0.7), ...extra);
const empurra = (dur: number, z0 = 1.03, z1 = 1.12, y1 = -24): Chave[] => [
  {q: 0, x: 0, y: 0, zoom: z0, rot: 0},
  {q: dur, x: 0, y: y1, zoom: z1, rot: -0.5, curva: 'linear'},
];

const Papel: React.FC<{q: number; k: number; c: ReturnType<typeof cam>; id: string; cor?: string; texto?: React.ReactNode; frente?: React.ReactNode; children: React.ReactNode}> = ({
  q, c, id, cor = COR.creme, texto, frente, children,
}) => (
  <AbsoluteFill>
    <Fundo cor={cor} forca={0.5} />
    <Palco cam={c} id={id}>
      <Plano p={0.5}><SombraFolhas q={q} opacidade={0.15} /></Plano>
      <Plano p={1}>{children}</Plano>
      {texto && <Plano p={1.12}>{texto}</Plano>}
      {frente && <Plano p={2.4}>{frente}</Plano>}
    </Palco>
  </AbsoluteFill>
);
const Real: React.FC<{q: number; ini: number; c: ReturnType<typeof cam>; id: string; src: string; de: number; vel?: number; escuro?: number; children?: React.ReactNode}> = ({
  q, ini, c, id, src, de, vel = 1, escuro = 0.18, children,
}) => (
  <AbsoluteFill style={{background: COR.preto}}>
    <Palco cam={c} id={id}>
      <Plano p={1}><Clipe q={q} ini={ini} src={src} de={de} vel={vel} escuro={escuro} escala={1.02} /></Plano>
      <Plano p={1.1}>{children}</Plano>
    </Palco>
    <Vinheta forca={0.45} />
  </AbsoluteFill>
);
/** Recorte da biblioteca dentro do SVG do boneco (objeto na mão). */
const NaMao: React.FC<{nome: string; w: number; rot?: number; dx?: number; dy?: number}> = ({nome, w, rot = 0, dx = 0, dy = 0}) => (
  <image href={staticFile(`colagem/${nome}-b0.png`)} x={-w / 2 + dx} y={-w / 2 + dy} width={w} height={w} transform={`rotate(${rot})`} preserveAspectRatio="xMidYMid meet" />
);
/** Palavras de uma faixa, cada uma no seu instante (quadro absoluto). */
const pals = (f: {de: number; ate: number}, destaque: string[] = [], tam?: number, cor?: string) =>
  PALAVRAS.slice(f.de, f.ate + 1).map((p) => {
    const limpo = p.texto.replace(/[,:;]$/, '');
    const chave = limpo.toLowerCase().replace(/[^a-zà-ú0-9]/g, '');
    return {t: limpo, q: F(p.inicio), cor: destaque.includes(chave) ? COR.acento : cor, tam};
  });
/** Interpola um ponto [x, y] entre quadros-chave (suave). */
const trilho = (q: number, ks: Array<[number, [number, number]]>): [number, number] => {
  if (q <= ks[0][0]) return ks[0][1];
  for (let i = 1; i < ks.length; i++) if (q <= ks[i][0]) {
    const t = ease((q - ks[i - 1][0]) / Math.max(1, ks[i][0] - ks[i - 1][0]));
    return [ks[i - 1][1][0] + (ks[i][1][0] - ks[i - 1][1][0]) * t, ks[i - 1][1][1] + (ks[i][1][1] - ks[i - 1][1][1]) * t];
  }
  return ks[ks.length - 1][1];
};
const numEm = (q: number, ks: Array<[number, number]>) => trilho(q, ks.map(([f, v]) => [f, [v, 0]] as [number, [number, number]]))[0];
const um = (t: string, s: number, cor?: string, tam?: number) => ({t, q: F(s), cor, tam});

// ------------------------------------------------------------------ 0 · o punhado reprovado
// Gancho com movimento desde o quadro 0: câmera mergulha no punhado, setas e círculo
// apontam, e no "reprovado" o quadro congela em preto e branco e o carimbo bate.
const Carimbo: React.FC<{q: number; ini: number; x: number; y: number; texto: string}> = ({q, ini, x, y, texto}) => {
  if (q < ini) return null;
  const k = q - ini;
  const s = k < 4 ? 2.2 - (k / 4) * 1.2 : 1;
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) rotate(-11deg) scale(${s})`,
      border: `14px solid ${COR.acento}`, outline: `5px solid ${COR.acento}`, outlineOffset: 9, padding: '6px 30px',
      color: COR.acento, fontFamily: PILHA.manchete, fontSize: 84, letterSpacing: 3, lineHeight: 1.05, whiteSpace: 'nowrap',
      background: 'rgba(241,236,224,0.12)', opacity: k < 1 ? 0.5 : 0.96}}>{texto}</div>
  );
};
const C0g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const pu = F(em(S0.esse, 'punhado')), aq = F(em(S0.esse, 'aqui')), ca = F(em(S0.esse, 'café')), rep = F(em(S0.reprovado, 'reprovado'));
  const PX = 770, PY = 1240; // onde o punhado está no quadro (medido no still de 2,5 s)
  const parado = q >= rep;
  const c = somar(cameraEm(k, [
    {q: 0, x: -40, y: -60, zoom: 1.0, rot: -1},
    {q: pu - ini + 5, x: 70, y: 90, zoom: 1.08, rot: -2, curva: 'rapida'},
    {q: rep - ini, x: 90, y: 110, zoom: 1.1, rot: -0.5, curva: 'linear'},
    {q: rep - ini + 4, x: 70, y: 120, zoom: 1.14, rot: 1.8, curva: 'rapida'},
    {q: fim - ini, x: 70, y: 120, zoom: 1.16, rot: 1.2, curva: 'linear'},
  ]), deriva(q, 'g0', 1), tremor(q, rep, 26, 8), tremor(q, pu, 10, 4));
  const flash = q >= rep && q < rep + 3 ? 1 - (q - rep) / 3 : 0;
  const setas: Array<[[number, number], [number, number], number]> = [
    [[150, 760], [PX - 150, PY - 130], 0], [[1010, 700], [PX + 30, PY - 170], 3], [[220, 1760], [PX - 160, PY + 110], 6],
  ];
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={c} id="g0">
        <Plano p={1} style={{filter: parado ? 'grayscale(1) contrast(1.2) brightness(0.9)' : undefined}}>
          <Clipe q={Math.min(q, rep)} ini={ini} src="v5" de={8.8} vel={0.55} escala={1} escuro={0.08} />
        </Plano>
        <Plano p={1.04}>
          {setas.map(([de, para, d], i) => (
            <Seta key={i} q={q} ini={pu + d} de={de} para={para} curva={0.25} cor={COR.acento} espessura={16} chave={`g0-s${i}`} fora={rep} />
          ))}
          <Elipse q={q} ini={aq} cx={PX} cy={PY} rx={250} ry={210} cor={COR.creme} espessura={12} chave="g0-el" fora={rep} />
          <Manchete q={q} x={540} y={430} itens={[{t: 'CAFÉ', q: ca, cor: COR.creme, tam: 190}]} fora={rep} />
          <Carimbo q={q} ini={rep} x={540} y={560} texto="REPROVADO" />
        </Plano>
        <Plano p={2.2}>
          {['grao-preto', 'grao-ardido', 'grao-quebrado', 'grao-imaturo'].map((n, i) => {
            if (q < rep + 1) return null;
            const t = Math.min(1, (q - rep - 1) / 16);
            const ang = [3.0, 0.15, 0.9, 2.3][i];
            return <Img key={n} src={staticFile(`colagem/${n}-b0.png`)} style={{position: 'absolute', left: PX + Math.cos(ang) * t * 520 - 70, top: PY + 60 * t + Math.sin(ang) * t * 300 - 70,
              width: 140, transform: `scale(${0.4 + t * 1.1}) rotate(${(i - 1.5) * t * 70}deg)`, opacity: Math.min(1, t * 4)}} />;
          })}
        </Plano>
      </Palco>
      <Vinheta forca={0.4} />
      {flash > 0 && <AbsoluteFill style={{background: `rgba(255,250,240,${flash * 0.85})`}} />}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------ 1 · o caminho das provas
const C1g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const on = F(em(S1.onze, 'onze')), cai = F(S1.caminho.inicio);
  const X = k * 5;
  const chao = 1450;
  const anda = caminhada(k, 18);
  const pose: PoseV2 = {...anda, bD: 168, cD: 8, bE: -168, cE: -8, tronco: 2};
  const c = cam(q, k, [
    {q: 0, x: 0, y: 40, zoom: 1.12, rot: 0},
    {q: on - ini, x: 0, y: 40, zoom: 1.1, rot: 0},
    {q: on - ini + 30, x: 120, y: -60, zoom: 0.9, rot: -1, curva: 'suave'},
    {q: fim - ini, x: 160, y: -40, zoom: 0.94, rot: -0.5},
  ], 'g1', [pulso(q, [on], 0.03)]);
  return (
    <Papel q={q} k={k} c={c} id="g1" cor="#E9DFCB"
      texto={<>
        <Manchete q={q} x={600} y={330} itens={pals(S1.onze, ['onze'], 150)} />
        <Manchete q={q} x={600} y={520} fonte="serifa" itens={pals(S1.caminho, [], 100)} />
      </>}>
      {/* a fila de PROVAS ao longo do caminho, ao fundo */}
      {Array.from({length: 11}, (_, i) => {
        const x = 640 + i * 300 - X;
        return (
          <div key={i} style={{position: 'absolute', left: x - 50, top: chao - 260, width: 100, height: 260}}>
            <div style={{position: 'absolute', left: 46, top: 40, width: 8, height: 220, background: COR.terra}} />
            <div style={{position: 'absolute', left: 0, top: 0, width: 100, height: 54, background: COR.acento, color: COR.creme,
              fontFamily: 'Archivo Black, Arial Black', fontSize: 34, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{i + 1}</div>
          </div>
        );
      })}
      <div style={{position: 'absolute', left: -600, top: chao, width: 2600, height: 600, background: '#C9A97E'}} />
      <div style={{position: 'absolute', left: -600, top: chao - 6, width: 2600, height: 12, background: COR.terra}} />
      {/* os grãos que seguem o boneco; dois caem no "fica pelo caminho" */}
      {[0, 1, 2, 3].map((i) => {
        const caiu = (i === 1 || i === 3) && q > cai + i * 3;
        const d = caiu ? q - cai - i * 3 : 0;
        return <Peca key={i} q={q} ini={ini} nome={['grao-02', 'grao-03', 'grao-01', 'grao-02'][i]} x={200 - i * 120 + d * 2} y={chao - 40 + d * d * 1.1}
          w={80} rot={k * 7 + i * 40 + d * 10} sombra={false} semBoil />;
      })}
      <BonecoV2 x={360} y={chao} h={500} pose={pose} rosto={k > cai - ini ? 'susto' : 'esforco'} bob={anda.bob}
        naMao={<NaMao nome="grao-01" w={190} rot={90} dx={-60} />} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 2 · a promessa (beber, analisado quadro a quadro)
// v2 reprovada: a caneca ficava colada no rosto 4 s, girando com o antebraço até quase
// virar, e o outro braço varria o ar o tempo todo. Agora: a caneca fica em pé no peito,
// sobe na hora do gole, inclina 30° no gole, desce; no "amarga" o braço afasta a caneca
// e a outra mão tapa a boca. Mão por alvo (IK), caneca com giro próprio.
const C2g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const sab = F(em(S2.fim, 'saber')), por = F(em(S2.fim, 'por')), am = F(S2.amarga.inicio);
  const sobe = F(em(S2.fim, 'café')) - 4, gole = sobe + 9, solta = F(em(S2.fim, 'toma')) + 4, peito = solta + 10;
  const PEITO: [number, number] = [0.21, -0.56], BOCA: [number, number] = [0.17, -0.81], LONGE: [number, number] = [0.47, -0.64];
  const alvoD = trilho(q, [[ini, PEITO], [sobe, PEITO], [gole, BOCA], [solta, BOCA], [peito, PEITO], [am - 2, PEITO], [am + 5, LONGE]]);
  const giroD = numEm(q, [[ini, 0], [gole - 2, 0], [gole + 3, -32], [solta, -32], [peito, 0], [am, 0], [am + 5, 14]]);
  const alvoE = trilho(q, [[ini, [-0.2, -0.42]], [sab - 4, [-0.2, -0.42]], [sab + 3, [-0.3, -0.98]], [por + 2, [-0.3, -0.98]], [por + 10, [-0.2, -0.42]],
    [am - 1, [-0.2, -0.42]], [am + 5, [-0.03, -0.83]]]);
  const treme = q >= am && q < am + 16 ? Math.sin((q - am) * 1.3) * 12 * (1 - (q - am) / 16) : 0;
  const cab = q >= am ? -6 + treme : numEm(q, [[gole, 0], [gole + 3, -8], [solta, -8], [peito, 0]]);
  const pose: PoseV2 = {...EM_PE, tronco: q >= am ? numEm(q, [[am, 0], [am + 3, -9]]) : 0, cab};
  const rosto = q >= am ? 'careta' : q >= gole && q < solta ? 'foco' : 'calmo';
  const c = cam(q, k, empurra(fim - ini, 1.03, 1.1, -24), 'g2', [pulso(q, [am], 0.05), tremor(q, am, 10, 5)]);
  return (
    <Papel q={q} k={k} c={c} id="g2"
      texto={<>
        <Manchete q={q} x={540} y={380} fonte="serifa" itens={pals({de: S2.fim.de + 8, ate: S2.fim.ate}, [], 96)} largura={940} />
        <Manchete q={q} x={540} y={640} itens={[um('AMARGA?', S2.amarga.inicio, COR.acento, 160)]} />
      </>}>
      <BonecoV2 x={460} y={1800} h={760} q={q} pose={pose} rosto={rosto} alvoD={alvoD} alvoE={alvoE} giroD={giroD} naMao={<Caneca s={0.9} />} />
      <Amargor q={q} ini={am + 4} x={460 + LONGE[0] * 760} y={1800 + LONGE[1] * 760 - 90} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 3 · a lavoura (vídeo)
const C3g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  return (
    <Real q={q} ini={ini} id="g3" src="v2" de={0} c={cam(q, k, empurra(fim - ini, 1.02, 1.08), 'g3', [pulso(q, [F(S3.m1250.inicio)], 0.04)])}>
      <Manchete q={q} x={540} y={400} itens={[um('PROVA 1', em(S3.primeira, 'primeira'), COR.creme, 150)]} fora={F(S3.serra.inicio)} />
      <Dymo q={q} ini={F(em(S3.serra, 'Serra'))} texto="SERRA DA CANASTRA" x={540} y={420} tamanho={74} rot={-2} />
      <Manchete q={q} x={540} y={640} itens={[um('1.250 M', S3.m1250.inicio, COR.acento, 170)]} />
    </Real>
  );
};

// ------------------------------------------------------------------ 4 · o refratômetro (analisado quadro a quadro)
// v2 reprovada: o aparelho subia na frente do rosto e o boneco congelava 3 s. Agora, em
// batidas: anda até o galho → colhe uma cereja (açúcar) → espreme sobre o prisma do
// refratômetro que a outra mão segura → leva a ocular ao olho, apontando para o sol, e a
// leitura aparece numa lente → "uva de vinho": baixa o aparelho e faz joinha.
const Lente: React.FC<{q: number; ini: number; x: number; y: number}> = ({q, ini, x, y}) => {
  if (q < ini) return null;
  const k = q - ini;
  const s = k < 6 ? ease(k / 6) : 1;
  const nivel = 0.72 - Math.min(1, k / 40) * 0.3; // a linha de leitura sobe: o açúcar aparece
  return (
    <div style={{position: 'absolute', left: x - 170, top: y - 170, width: 340, height: 340, borderRadius: '50%', overflow: 'hidden',
      border: `12px solid ${COR.preto}`, transform: `scale(${s})`, background: '#F4F1EA', boxShadow: '0 12px 20px rgba(0,0,0,.35)'}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: '100%', height: `${nivel * 100}%`, background: '#3E78A8'}} />
      {Array.from({length: 9}, (_, i) => (
        <div key={i} style={{position: 'absolute', left: 150, top: 40 + i * 32, width: i % 2 ? 40 : 70, height: 5, background: COR.preto}} />
      ))}
      <div style={{position: 'absolute', left: 30, top: `${nivel * 100}%`, width: 280, height: 6, background: COR.acento, transform: 'translateY(-3px)'}} />
    </div>
  );
};
const C4g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini, H = 640, CHAO = 1600;
  const ac = F(S4.acucar.inicio), rf = F(S4.refrat.inicio), vi = F(em(S4.vinho, 'vinho'));
  const chega = ini + 18;
  const bx = 300 + ease(lin(q, ini, chega)) * 300;
  const CEREJA: [number, number] = [0.27, -0.93];
  const pega = ac + 4, aperta = ac + 22, espreme = aperta + 6, ergue = rf + 8;
  const alvoD = trilho(q, [[ini, [0.14, -0.4]], [ac - 6, [0.14, -0.4]], [pega, CEREJA], [pega + 3, CEREJA], [aperta, [-0.1, -0.68]], [espreme + 10, [-0.1, -0.68]],
    [ergue, [0.18, -0.38]], [vi, [0.18, -0.38]], [vi + 8, [0.22, -1.02]]]);
  const alvoE = trilho(q, [[ini, [-0.17, -0.42]], [ac + 8, [-0.17, -0.42]], [aperta - 4, [-0.06, -0.6]], [espreme + 10, [-0.06, -0.6]], [ergue, [-0.03, -0.91]], [vi, [-0.03, -0.91]], [vi + 8, [-0.18, -0.5]]]);
  const giroE = numEm(q, [[ini, 35], [espreme + 10, 35], [ergue, 65], [vi, 65], [vi + 8, 35]]);
  const comCereja = q >= pega && q < espreme + 4;
  const olhando = q >= ergue && q < vi;
  const andando = q < chega;
  const anda = caminhada(k, 14);
  const pose: PoseV2 = andando ? anda : {...EM_PE, cab: olhando ? -6 : 0};
  const c = cam(q, k, [
    {q: 0, x: 0, y: 0, zoom: 1.04, rot: 0},
    {q: ac - ini, x: 60, y: -20, zoom: 1.08, rot: -0.6},
    {q: rf - ini, x: 80, y: -60, zoom: 1.14, rot: 0.4},
    {q: fim - ini, x: 90, y: -80, zoom: 1.18, rot: 0, curva: 'linear'},
  ], 'g4', [pulso(q, [ac, rf], 0.035)]);
  return (
    <Papel q={q} k={k} c={c} id="g4" cor="#E9DFCB"
      texto={<>
        <Manchete q={q} x={540} y={380} itens={[um('AÇÚCAR', S4.acucar.inicio, COR.acento, 150)]} fora={F(S4.vinho.inicio)} />
        <Dymo q={q} ini={rf + 4} texto="REFRATÔMETRO" x={540} y={540} tamanho={60} rot={-2} fora={F(S4.vinho.inicio)} />
        <Manchete q={q} x={540} y={420} fonte="serifa" itens={pals(S4.vinho, ['vinho'], 110)} />
      </>}
      frente={<Img src={staticFile('colagem/folha-2-b0.png')} style={{position: 'absolute', left: 980 - k * 3, top: 1500, width: 600, transform: 'rotate(-20deg)'}} />}>
      <Brilho q={q} ini={rf} x={230} y={300} r={140} cor="#E8B54A" />
      <Img src={staticFile('colagem/folha-1-b0.png')} style={{position: 'absolute', left: 700, top: 640, width: 500, transform: 'rotate(160deg)'}} />
      <Img src={staticFile('colagem/cachinho-b0.png')} style={{position: 'absolute', left: 700, top: 820, width: 300, transform: 'rotate(-8deg)'}} />
      {q >= espreme && q < espreme + 8 && (
        <div style={{position: 'absolute', left: bx - 0.1 * H - 9, top: CHAO - 0.62 * H + (q - espreme) * 6, width: 18, height: 24, borderRadius: '50% 50% 50% 50% / 60% 60% 40% 40%', background: '#7A1F2B'}} />
      )}
      <BonecoV2 x={bx} y={CHAO} h={H} q={q} pose={pose} bob={andando ? anda.bob : 0}
        rosto={olhando ? 'foco' : q >= vi + 4 ? 'sorriso' : 'calmo'}
        alvoD={andando ? undefined : alvoD} alvoE={andando ? undefined : alvoE} giroE={giroE} giroD={0}
        naMao={comCereja ? <NaMao nome="cereja-vermelha-1" w={64} /> : undefined}
        naMaoE={<NaMao nome="refratometro" w={230} />} />
      <Lente q={q} ini={ergue + 6} x={800} y={700} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 5 · só o maduro (vídeo)
const C5g: React.FC<P> = ({q, ini, fim}) => (
  <Real q={q} ini={ini} id="g5" src="v2" de={6.0} c={cam(q, q - ini, empurra(fim - ini, 1.02, 1.08), 'g5')}>
    <Manchete q={q} x={540} y={420} itens={pals(S5.maduro, ['maduro'], 140, COR.creme)} />
  </Real>
);

// ------------------------------------------------------------------ 6 · fruto verde vira amargor
const C6g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const xi = F(em(S5.verde, 'xícara')), am = F(S5.amargor.inicio);
  const t = lin(q, ini + 6, xi);
  const cx = 300 + (640 - 300) * t, cy = 980 - Math.sin(t * Math.PI) * 420 + (1080 - 980) * t;
  const pose = chaves(q, [[ini, {bD: -40, cD: -30, tronco: -6}], [ini + 6, {bD: 120, cD: 10, tronco: 10}], [ini + 16, {bD: 60, cD: 10, tronco: 4}]]);
  const c = cam(q, k, empurra(fim - ini, 1.04, 1.12), 'g6', [pulso(q, [am], 0.05), tremor(q, am, 10, 5)]);
  return (
    <Papel q={q} k={k} c={c} id="g6"
      texto={<>
        <Manchete q={q} x={540} y={380} fonte="serifa" itens={pals(S5.verde, ['verde'], 100)} largura={960} />
        <Manchete q={q} x={540} y={600} itens={[um('AMARGOR', S5.amargor.inicio, COR.acento, 150)]} />
      </>}>
      <Peca q={q} ini={ini} nome="xicara" x={680} y={1240} w={440} rot={4} treme={am} />
      {q < xi && <Peca q={q} ini={ini} nome="cereja-verde-1" x={cx} y={cy} w={120} rot={k * 12} semBoil />}
      <Amargor q={q} ini={am} x={680} y={1130} />
      <BonecoV2 x={230} y={1700} h={520} pose={pose} rosto={q >= am ? 'careta' : 'calmo'} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 7 · terreiro (vídeo)
const C7g: React.FC<P> = ({q, ini, fim}) => {
  const rv = F(em(S6.terreiro, 'revirado')), fe = F(S6.fermenta.inicio);
  return (
    <Real q={q} ini={ini} id="g7" src="v1" de={1.6} c={cam(q, q - ini, empurra(fim - ini, 1.02, 1.08), 'g7', [pulso(q, [fe], 0.05)])}>
      <Brilho q={q} ini={F(em(S6.sol, 'sol'))} x={830} y={300} r={130} cor={COR.acento} />
      <Manchete q={q} x={540} y={420} itens={[um('SOL', em(S6.sol, 'sol'), COR.creme, 230)]} fora={rv} />
      <Manchete q={q} x={540} y={420} fonte="serifa" itens={pals({de: S6.terreiro.de + 5, ate: S6.terreiro.ate}, ['inteiro'], 110, COR.creme)} fora={fe} />
      <Manchete q={q} x={540} y={460} itens={[um('FERMENTA', S6.fermenta.inicio, COR.acento, 120)]} />
    </Real>
  );
};

// ------------------------------------------------------------------ 8 · ardido
const C8g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini, ar = F(S6.ardido.inicio);
  const lx = interpolate(q, [ini, ar], [1350, 560], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: (t) => ease(t)});
  const c = cam(q, k, empurra(fim - ini, 1.04, 1.16), 'g8', [pulso(q, [ar], 0.05), tremor(q, ar, 10, 5)]);
  return (
    <Papel q={q} k={k} c={c} id="g8" cor="#E9DFCB"
      texto={<>
        <Manchete q={q} x={540} y={400} fonte="serifa" itens={pals({de: S6.fermentado.de + 2, ate: S6.fermentado.ate}, [], 100)} fora={ar} />
        <Manchete q={q} x={540} y={420} itens={[um('ARDIDO', S6.ardido.inicio, COR.acento, 170)]} />
      </>}
      frente={<Peca q={q} ini={ini} nome="lupa" x={lx} y={980} w={620} rot={-20} semBoil />}>
      <Peca q={q} ini={ini + 2} nome="grao-ardido" x={540} y={960} w={360} rot={-8} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 9 · sai a casca, peneira fina
const C9g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini, ab = ini + 10, pe = F(S7.peneira.inicio);
  const sp = q < ab ? 0 : (q - ab) * 16;
  const desce = lin(q, pe + 4, pe + 16);
  const sobe = lin(q, pe - 6, pe + 6);
  const c = cam(q, k, empurra(fim - ini, 1.06, 1.14), 'g9', [pulso(q, [ab, pe], 0.04)]);
  return (
    <Papel q={q} k={k} c={c} id="g9"
      texto={<Manchete q={q} x={540} y={400} itens={pals(S7.peneira, ['fina'], 140).filter((p) => p.t !== 'e' && p.t !== 'começa' && p.t !== 'a')} />}>
      <Peca q={q} ini={ini + 2} nome="peneira-classificacao" x={540} y={1900 - ease(sobe) * 560} w={560} rot={-3} semBoil />
      {q < ab ? <Peca q={q} ini={ini} nome="cereja-seca" x={540} y={960} w={340} rot={6} /> : <>
        <Peca q={q} ini={ab} nome="casca" x={540 - sp} y={940 - sp * 0.4} w={300} rot={-20 - sp * 0.2} semBoil />
        <Peca q={q} ini={ab} nome="casca" x={540 + sp} y={980 - sp * 0.3} w={300} rot={160 + sp * 0.2} semBoil />
        <Peca q={q} ini={ab} nome="grao-01" x={540} y={960 + ease(desce) * 330} w={250} rot={-8} semBoil />
      </>}
    </Papel>
  );
};

// ------------------------------------------------------------------ 10–11 · pedra, graveto (rajada, corte seco)
const Rajada = (nome: string, palavra: string, w: number, rot: number, cor: string): React.FC<P> => ({q, ini, fim}) => (
  <Papel q={q} k={q - ini} c={cam(q, q - ini, empurra(fim - ini, 1.1, 1.18, 0), `r${nome}`, [pulso(q, [ini], 0.06), tremor(q, ini, 14, 4)])} id={`r${nome}`} cor={cor}
    texto={<Manchete q={q} x={540} y={1430} itens={[{t: palavra, q: ini, tam: 170}]} />}>
    <Peca q={q} ini={ini} nome={nome} x={540} y={900} w={w} rot={rot} />
  </Papel>
);
const C10g = Rajada('pedra', 'PEDRA', 440, -6, COR.creme);
const C11g = Rajada('graveto', 'GRAVETO', 740, -16, '#D9C3A0');

// ------------------------------------------------------------------ 12 · grão leve (vídeo)
const C12g: React.FC<P> = ({q, ini, fim}) => (
  <Real q={q} ini={ini} id="g12" src="v4" de={4.0} c={cam(q, q - ini, empurra(fim - ini, 1.02, 1.08), 'g12')}>
    <Manchete q={q} x={540} y={400} itens={pals(S8.leve, ['leve'], 150, COR.creme)} />
    <Manchete q={q} x={540} y={600} fonte="serifa" itens={pals(S8.oco, ['oco'], 110, COR.creme)} />
  </Real>
);

// ------------------------------------------------------------------ 13 · a máquina que olha grão por grão e sopra
const C13g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const defeitos: Array<[string, string]> = [['grao-preto', 'preto'], ['grao-imaturo', 'verde'], ['grao-ardido', 'ardido']];
  const SX = 740, BOCA = 1150, TOPO = 640, VEL = 22;
  const chegadas = defeitos.map(([, p]) => F(em(S8.defeitos, p)) + Math.round((BOCA - TOPO) / VEL));
  const ultimoSopro = chegadas.filter((c) => q >= c).pop();
  const apertando = chegadas.some((c) => q >= c - 4 && q < c + 4);
  const pose: PoseV2 = chaves(q, [[ini, {tronco: 8, bD: 70, cD: 50, bE: -20}], [ini + 20, {tronco: 10, bD: 75, cD: 55, bE: -20}]]);
  const poseFinal = apertando ? {...pose, bD: 95, cD: 20, tronco: 14, sq: 0.08} : pose;
  const c = cam(q, k, [{q: 0, x: 40, y: 0, zoom: 1.08, rot: 0}, {q: fim - ini, x: 80, y: -30, zoom: 1.16, rot: 0.6, curva: 'linear'}], 'g13',
    [pulso(q, chegadas, 0.03), ...chegadas.map((cq) => tremor(q, cq, 8, 4))]);
  return (
    <Papel q={q} k={k} c={c} id="g13" cor="#E9DFCB"
      texto={<>
        <Manchete q={q} x={540} y={360} fonte="serifa" itens={[um('grão por grão', em(S8.maquina, 'grão'), undefined, 100)]} fora={F(S8.defeitos.inicio)} />
        <Manchete q={q} x={540} y={360} itens={defeitos.map(([, p]) => um(p.toUpperCase(), em(S8.defeitos, p), p === 'ardido' ? COR.acento : undefined, 84))} />
        <Manchete q={q} x={540} y={520} fonte="serifa" itens={pals({de: S8.sopro.de + 2, ate: S8.sopro.ate}, ['sopro'], 100)} />
      </>}>
      {/* a calha de grãos bons descendo */}
      <div style={{position: 'absolute', left: SX - 70, top: TOPO - 40, width: 140, height: 1100, background: 'rgba(59,42,31,0.08)', borderLeft: `6px solid ${COR.terra}`, borderRight: `6px solid ${COR.terra}`}} />
      {Array.from({length: 9}, (_, i) => (
        <Peca key={i} q={q} ini={ini} nome={i % 2 ? 'grao-02' : 'grao-03'} x={SX + Math.sin(i * 2.1) * 20} y={TOPO + ((k * 9 + i * 120) % 1000)} w={80} rot={i * 37 + k * 3} sombra={false} semBoil />
      ))}
      {/* o bico de ar e o botão */}
      <div style={{position: 'absolute', left: SX - 300, top: BOCA - 40, width: 200, height: 80, background: '#8A8178', border: `6px solid ${COR.preto}`, borderRadius: 10}} />
      <div style={{position: 'absolute', left: SX - 110, top: BOCA - 20, width: 50, height: 40, background: '#8A8178', border: `6px solid ${COR.preto}`}} />
      {defeitos.map(([nome, p], i) => {
        const nasce = F(em(S8.defeitos, p));
        if (q < nasce) return null;
        const ch = chegadas[i];
        const y = q < ch ? TOPO + (q - nasce) * VEL : BOCA;
        const x = q < ch ? SX : SX + (q - ch) * 34;
        return <Peca key={nome} q={q} ini={nasce} nome={nome} x={x} y={y - (q > ch ? (q - ch) * 8 : 0)} w={110} rot={(q - nasce) * (q > ch ? 30 : 6)} />;
      })}
      {ultimoSopro !== undefined && q - ultimoSopro < 10 && (
        <svg style={{position: 'absolute', left: SX - 60, top: BOCA - 70, overflow: 'visible'}} width={10} height={10}>
          {[-30, 0, 30].map((o, i) => <path key={i} d={`M0,${70 + o} q${60},-12 ${120 + (q - ultimoSopro) * 14},0`} stroke={COR.preto} strokeWidth={8} fill="none" strokeLinecap="round" opacity={1 - (q - ultimoSopro) / 10} />)}
        </svg>
      )}
      <div style={{position: 'absolute', left: 450, top: 1390, width: 22, height: 210, background: COR.terra}} />
      <div style={{position: 'absolute', left: 415, top: apertando ? 1362 : 1350, width: 92, height: apertando ? 34 : 46, borderRadius: '50% 50% 10% 10%', background: COR.acento, border: `6px solid ${COR.preto}`}} />
      <BonecoV2 x={320} y={1760} h={520} pose={poseFinal} rosto={apertando ? 'esforco' : 'foco'} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 14 · por tamanho
// v2 reprovada: o grão girava no ar e só o último ficava na caixa. Agora cada grão jogado
// FICA, empilhando; voo com giro curto; nada de boil (imagem fixa, sem tremidinha).
const C14g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini, ta = F(S9.tamanho.inicio);
  const CICLO = 22, INI = 14, VOO = 12;
  const n = Math.max(0, Math.floor((k - INI) / CICLO));
  const fase = k < INI ? 0 : ((k - INI) % CICLO) / CICLO;
  const pose: PoseV2 = fase < 0.45 ? chaves(fase * 100, [[0, {bD: 30, cD: 30, tronco: 10}], [45, {bD: -35, cD: 55, tronco: 14}]])
    : chaves(fase * 100, [[45, {bD: -35, cD: 55, tronco: 14}], [62, {bD: 115, cD: 10, tronco: -2}], [100, {bD: 60, cD: 20, tronco: 4}]]);
  const BOX = [640, 900];
  const grande = (i: number) => i % 2 === 0;
  const lancados = Array.from({length: n + 1}, (_, i) => i).filter((i) => k >= INI + i * CICLO + CICLO * 0.6);
  const c = cam(q, k, [{q: 0, x: 0, y: 0, zoom: 1.05, rot: 0}, {q: fim - ini, x: 50, y: -20, zoom: 1.12, rot: -0.5, curva: 'linear'}], 'g14', [pulso(q, [ta], 0.04)]);
  const contagem = [0, 0];
  return (
    <Papel q={q} k={k} c={c} id="g14"
      texto={<>
        <Manchete q={q} x={540} y={360} itens={[um('TAMANHO', S9.tamanho.inicio, COR.acento, 150)]} />
        <Manchete q={q} x={540} y={540} fonte="serifa" itens={pals({de: S9.porque.de + 6, ate: S9.porque.ate}, ['igual'], 100)} />
      </>}>
      <Img src={staticFile('colagem/peneira-classificacao-b0.png')} style={{position: 'absolute', left: 150, top: 760, width: 300, transform: 'rotate(-6deg)'}} />
      {lancados.map((i) => {
        const t0 = INI + i * CICLO + CICLO * 0.6;
        const t = Math.min(1, (k - t0) / VOO);
        const b = grande(i) ? 0 : 1;
        const j = contagem[b]++;
        const w = grande(i) ? 104 : 60;
        const fx = BOX[b] + ((j % 3) - 1) * 62 + (Math.floor(j / 3) % 2) * 24, fy = 1338 - Math.floor(j / 3) * 26;
        const x = 430 + (fx - 430) * ease(t), y = 1060 + (fy - 1060) * t - Math.sin(t * Math.PI) * 260;
        return <Img key={i} src={staticFile(`colagem/${grande(i) ? 'grao-01' : 'grao-02'}-b0.png`)} style={{position: 'absolute', left: x - w / 2, top: y - w / 2, width: w,
          transform: `rotate(${(j * 47) % 60 - 30 + (1 - t) * 50}deg)`}} />;
      })}
      {BOX.map((x, b) => (
        <div key={b} style={{position: 'absolute', left: x - 125, top: 1340, width: 250, height: 170, background: '#B98E5E', border: `7px solid ${COR.preto}`,
          boxShadow: '0 10px 14px rgba(0,0,0,.3)', display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontFamily: PILHA.manchete, fontSize: 64, color: COR.creme}}>{b ? 'P' : 'G'}</div>
      ))}
      <BonecoV2 x={340} y={1700} h={540} q={q} pose={pose} rosto="foco"
        naMao={fase > 0.1 && fase < 0.62 ? <NaMao nome={grande(n) ? 'grao-01' : 'grao-02'} w={grande(n) ? 104 : 60} /> : undefined} giroD={0} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 15 · a virada (vídeo do tambor, escurecido)
const C15g: React.FC<P> = ({q, ini, fim}) => {
  const ne = F(S10.nenhuma.inicio);
  return (
    <Real q={q} ini={ini} id="g15" src="v3" de={0} vel={0.5} escuro={0.4} c={cam(q, q - ini, empurra(fim - ini, 1.02, 1.08), 'g15', [pulso(q, [ne], 0.05)])}>
      <Manchete q={q} x={540} y={420} fonte="serifa" itens={pals({de: S10.aqui.de + 3, ate: S10.aqui.ate}, ['ninguém'], 100, COR.creme)} fora={ne} />
      <Manchete q={q} x={540} y={420} itens={[um('NENHUMA', S10.nenhuma.inicio, COR.acento, 160)]} />
      <Manchete q={q} x={540} y={620} fonte="serifa" itens={[um('acontece', em(S10.nenhuma, 'acontece'), COR.creme, 110), um('na', em(S10.nenhuma, 'na'), COR.creme, 110), um('torra.', em(S10.nenhuma, 'torra'), COR.acento, 110)]} />
    </Real>
  );
};

// ------------------------------------------------------------------ 16–17 · o trecho aprovado no teste
const TESTE_Q = F(T0);
const doTeste = (Pl: React.FC<{q: number}>): React.FC<P> => ({q}) => <Pl q={q - TESTE_Q} />;

// ------------------------------------------------------------------ 18 · o Arthur prova (vídeo)
const C18g: React.FC<P> = ({q, ini, fim}) => (
  <Real q={q} ini={ini} id="g18" src="v6" de={0.9} escuro={0.2} c={cam(q, q - ini, empurra(fim - ini, 1.02, 1.08), 'g18', [pulso(q, [F(S13.xicara.inicio)], 0.04)])}>
    <Manchete q={q} x={540} y={380} itens={[um('NA', em(S13.porIsso, 'na'), COR.creme, 120), um('XÍCARA', S13.xicara.inicio, COR.acento, 120)]} />
    <Dymo q={q} ini={F(em(S13.arthur, 'Arthur'))} texto="ARTHUR · PROVA" x={540} y={1300} tamanho={60} rot={-2} />
  </Real>
);

// ------------------------------------------------------------------ 19 · a ficha de prova
const C19g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const itens: Array<[string, number]> = [['AROMA', F(S13.aroma.inicio)], ['CORPO', F(S13.corpo.inicio)], ['DOÇURA', F(S13.docura.inicio)], ['CITRICIDADE', F(S13.citric.inicio)]];
  const c = cam(q, k, [{q: 0, x: 0, y: 40, zoom: 1.1, rot: 0}, {q: fim - ini, x: 0, y: -40, zoom: 1.16, rot: 0.8, curva: 'linear'}], 'g19', [pulso(q, itens.map((i) => i[1]), 0.03)]);
  return (
    <Papel q={q} k={k} c={c} id="g19" frente={<Peca q={q} ini={ini} nome="folha-5" x={-150 + k * 5} y={1700} w={620} rot={30} semBoil />}>
      <Peca q={q} ini={ini} nome="post-it" x={540} y={920} w={820} rot={-2} />
      {itens.map(([t, s], i) => (
        <React.Fragment key={t}>
          <Dymo q={q} ini={s} texto={t} x={430} y={760 + i * 120} tamanho={56} rot={-1} />
          <Check q={q} ini={s + 4} cx={800} cy={760 + i * 120} r={36} cor={COR.acento} chave={`g19-${i}`} espessura={10} />
        </React.Fragment>
      ))}
      <Peca q={q} ini={ini} nome="xicara-prova" x={220} y={1440} w={260} rot={-6} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 20 · os pacotes reais, 80+
const C20g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini, o = F(S13.oitenta.inicio);
  const c = cam(q, k, [{q: 0, x: 0, y: 0, zoom: 1.02, rot: 0}, {q: fim - ini, x: 0, y: -20, zoom: 1.1, rot: 0, curva: 'linear'}], 'g20', [pulso(q, [o], 0.05)]);
  return (
    <Papel q={q} k={k} c={c} id="g20"
      texto={<>
        <Manchete q={q} x={540} y={330} itens={[um('80+', S13.oitenta.inicio, COR.acento, 230)]} />
        <Manchete q={q} x={540} y={500} fonte="serifa" itens={[um('pontos', em(S13.oitenta, 'pontos'), undefined, 100)]} />
      </>}>
      <Embalagem q={q} ini={ini} sku="classico" x={340} y={1060} h={1150} rot={-4} />
      <Embalagem q={q} ini={ini + 6} sku="suave" x={760} y={1080} h={1150} rot={4} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 21 · o punhado do começo (vídeo, laço)
const C21g: React.FC<P> = ({q, ini, fim}) => (
  <Real q={q} ini={ini} id="g21" src="v5" de={8.75} vel={0.5} c={cam(q, q - ini, empurra(fim - ini, 1.02, 1.08), 'g21')}>
    <Manchete q={q} x={540} y={420} fonte="serifa" itens={pals(S14.ficou, ['fazenda.'], 110, COR.creme).map((p) => (p.t === 'fazenda.' ? {...p, cor: COR.acento} : p))} />
  </Real>
);

// ------------------------------------------------------------------ 22 · CTA
const C22g: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const pose = chaves(q, [[ini, {bD: 40, cD: 40}], [ini + 14, {bD: 95, cD: 10, tronco: 8}], [fim, {bD: 98, cD: 8, tronco: 9}]]);
  const c = cam(q, k, [{q: 0, x: 0, y: 0, zoom: 1.0, rot: 0}, {q: 30, x: 0, y: 30, zoom: 1.08, rot: 0}, {q: fim - ini, x: 0, y: 50, zoom: 1.14, rot: 0.5, curva: 'linear'}], 'g22');
  return (
    <Papel q={q} k={k} c={c} id="g22" cor="#E9DFCB"
      texto={<>
        <Manchete q={q} x={540} y={360} itens={pals({de: S15.manda.de, ate: S15.manda.de + 5}, [], 92).filter((p) => !['esse', 'vídeo', 'Esse'].includes(p.t))} />
        <Manchete q={q} x={540} y={560} fonte="serifa" itens={pals({de: S15.manda.de + 6, ate: S15.manda.ate}, ['igual.'], 110).map((p) => (p.t === 'igual.' ? {...p, cor: COR.acento} : p))} />
      </>}>
      <BonecoV2 x={380} y={1760} h={720} pose={pose} rosto="calmo" naMao={<Caneca s={1.1} />} />
    </Papel>
  );
};

// ------------------------------------------------------------------ montagem
const T = (s: number) => F(s);
const CENAS: Array<{ini: number; C: React.FC<P>; seco?: boolean}> = [
  {ini: 0, C: C0g},
  {ini: T(S1.chegar.inicio), C: C1g},
  {ini: T(S2.fim.inicio), C: C2g},
  {ini: T(S3.primeira.inicio), C: C3g},
  {ini: T(S4.mede.inicio), C: C4g},
  {ini: T(S5.maduro.inicio), C: C5g},
  {ini: T(S5.verde.inicio), C: C6g},
  {ini: T(S6.sol.inicio), C: C7g},
  {ini: T(S6.fermentado.inicio), C: C8g},
  {ini: T(S7.casca.inicio), C: C9g},
  {ini: T(S8.pedra.inicio), C: C10g, seco: true},
  {ini: T(S8.graveto.inicio), C: C11g, seco: true},
  {ini: T(S8.leve.inicio), C: C12g, seco: true},
  {ini: T(S8.maquina.inicio), C: C13g},
  {ini: T(S9.ultimo.inicio), C: C14g},
  {ini: T(S10.aqui.inicio), C: C15g},
  {ini: TESTE_Q + A0, C: doTeste(PlanoA)},
  {ini: TESTE_Q + B0, C: doTeste(PlanoB)},
  {ini: TESTE_Q + C0, C: doTeste(PlanoC)},
  {ini: TESTE_Q + D0, C: doTeste(PlanoD)},
  {ini: T(S13.porIsso.inicio), C: C18g},
  {ini: T(S13.aroma.inicio), C: C19g},
  {ini: T(S13.classico.inicio), C: C20g},
  {ini: T(S14.punhado.inicio), C: C21g},
  {ini: T(S15.manda.inicio), C: C22g},
];
const TROCAS = CENAS.slice(1).filter((c) => !c.seco).map((c) => c.ini);

// sons: os do teste (deslocados) + um por palavra-chave e por ação das outras cenas
const ef = (a: string, s: number, v = 0.5): [string, number, number] => [a, F(s), v];
const SONS: Array<[string, number, number]> = [
  ef('carimbo', em(S0.reprovado, 'reprovado'), 0.7), ef('rabisco', em(S0.reprovado, 'reprovado') + 0.35, 0.45),
  ef('pop', em(S1.onze, 'onze'), 0.5), ef('pop', em(S1.onze, 'provas'), 0.45), ef('whoosh', S1.caminho.inicio, 0.4),
  ef('golinho', em(S2.fim, 'você', 2), 0.4), ef('carimbo', S2.amarga.inicio, 0.7),
  ef('pop', em(S3.primeira, 'primeira'), 0.5), ef('carimbo', S3.serra.inicio, 0.6), ef('digitacao', S3.serra.inicio + 0.05, 0.4), ef('pop', S3.m1250.inicio, 0.5),
  ef('pop', S4.acucar.inicio, 0.5), ef('carimbo', S4.refrat.inicio, 0.55), ef('brilho', S4.refrat.inicio, 0.4), ef('pop', em(S4.vinho, 'vinho'), 0.45),
  ef('pop', em(S5.maduro, 'maduro'), 0.5), ef('whoosh', S5.verde.inicio, 0.35), ef('thump', em(S5.verde, 'xícara'), 0.5), ef('carimbo', S5.amargor.inicio, 0.7),
  ef('pop', em(S6.sol, 'sol'), 0.55), ef('brilho', em(S6.sol, 'sol'), 0.5), ef('carimbo', S6.fermenta.inicio, 0.6),
  ef('carimbo', S6.ardido.inicio, 0.8), ef('thump', S6.ardido.inicio, 0.5),
  ef('rasgo', S7.casca.inicio + 0.33, 0.6), ef('slide', S7.peneira.inicio, 0.45), ef('pop', em(S7.peneira, 'fina'), 0.5),
  ef('thump', S8.pedra.inicio, 0.7), ef('thump', S8.graveto.inicio, 0.7), ef('pop', em(S8.leve, 'leve'), 0.5),
  ...['preto', 'verde', 'ardido'].map((p) => ef('pop', em(S8.defeitos, p), 0.45)),
  ...['preto', 'verde', 'ardido'].map((p) => ef('whoosh', em(S8.defeitos, p) + (1000 - 300) / 22 / 30, 0.5)),
  ef('carimbo', S9.tamanho.inicio, 0.6), ef('graos', S9.tamanho.inicio + 0.3, 0.35), ef('pop', em(S9.porque, 'igual'), 0.45),
  ef('pop', em(S10.aqui, 'ninguém'), 0.4), ef('carimbo', S10.nenhuma.inicio, 0.7), ef('tink', em(S10.nenhuma, 'torra'), 0.4),
  ...efeitosTeste().map(([a, lq2, v]): [string, number, number] => [a, TESTE_Q + lq2, v]),
  ef('carimbo', S13.xicara.inicio, 0.6), ef('digitacao', em(S13.arthur, 'Arthur'), 0.4),
  ...[S13.aroma, S13.corpo, S13.docura, S13.citric].flatMap((f) => [ef('carimbo', f.inicio, 0.55), ef('tink', f.inicio + 0.15, 0.3)]),
  ef('slide', S13.classico.inicio, 0.45), ef('carimbo', S13.oitenta.inicio, 0.7), ef('brilho', S13.oitenta.inicio + 0.15, 0.5),
  ef('pop', em(S14.ficou, 'fazenda'), 0.45), ef('pop', S15.manda.inicio, 0.45), ef('tink', em(S15.manda, 'igual') + 0.3, 0.45),
  ...TROCAS.map((t): [string, number, number] => ['chicote', t - 5, 0.5]),
];

export const Onze2: React.FC = () => {
  const q = useCurrentFrame();
  let i = 0;
  for (let n = 0; n < CENAS.length; n++) if (q >= CENAS[n].ini) i = n;
  const {C, ini} = CENAS[i];
  const fim = CENAS[i + 1]?.ini ?? DURACAO_ONZE2;
  // chicote: borrão + deslize de 3 quadros de cada lado da troca (não nas rajadas)
  const perto = TROCAS.map((t) => q - t).find((d) => d >= -3 && d < 3);
  const kk = perto === undefined ? 0 : 1 - Math.abs(perto + 0.5) / 3.5;
  const desl = perto === undefined ? 0 : (perto < 0 ? -1 : 1) * kk * -160;
  const fimFala = F(PALAVRAS[PALAVRAS.length - 1].fim + 0.2);
  const trilha = (f: number) => {
    const sobe = interpolate(f, [fimFala, fimFala + 6], [0.16, 0.3], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const sai = interpolate(f, [DURACAO_ONZE2 - 10, DURACAO_ONZE2], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    return sobe * sai;
  };
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <AbsoluteFill style={{transform: `translateX(${desl}px)`, filter: kk > 0 ? `blur(${kk * 18}px)` : undefined}}>
        <C q={q} ini={ini} fim={fim} />
      </AbsoluteFill>
      <GraoFilme q={q} forca={0.05} />
      <Audio src={staticFile('fonte/narracao.mp3')} />
      <Audio src={staticFile('sfx/trilha.wav')} volume={trilha} />
      {SONS.map(([a, s, v], n) => (
        <Sequence key={n} from={Math.max(0, s)} durationInFrames={60}><Audio src={staticFile(`sfx/${a}.wav`)} volume={v * 0.75} /></Sequence>
      ))}
    </AbsoluteFill>
  );
};
