// Peça 09 — "cada um tem seu jeitinho" (v2, 15/10/2026).
//   - abertura crua de 3 s, SEM voz (vídeo do Rafael no notebook), e mergulho na tela do
//     notebook até o reel do Fábio virar colagem: o cru → produzido da @rafaelachagas
//   - sistema A/B da peça 07: a palavra-chave (B) entra no quadro em que a voz a diz e sai
//     0,9 s depois; o resto da fala vai na pílula (A). Regra do cliente: sem texto na tela,
//     a fala tem legenda. A v1 deixava a palavra parada 3 s e não tinha pílula.
//   - câmera sempre andando; parallax; vídeo real sempre em movimento: cada take cobre a
//     sua janela inteira (tomadas.ts + teste), e troca EXATAMENTE na palavra
//   - uma cor por criador: Fábio laranja, Paulo caramelo, Giuseppe verde (Itália)
//   - todos os assets são novos desta peça (prefixo j09-, gerados no ChatGPT em 15/10/2026);
//     as cabeças (cab-*) são recorte dos quadros dos próprios criadores
//   - narração em WAV e adiantada 43 ms (narracao-sinc.wav): o render do Remotion atrasa o
//     áudio 43 ms, medido por correlação do envelope num trecho cru (o MP3 atrasava 70 ms)
// Nenhum tempo digitado: tudo lê roteiro.ts e tomadas.ts.

import {Audio} from '@remotion/media';
import React from 'react';
import {AbsoluteFill, Freeze, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {COR} from '../../identidade/tokens';
import {cameraEm, deriva, pulso, somar, tremor, type Chave} from '../../colagem/camera';
import {Palco, Plano} from '../../colagem/palco';
import {Dymo, Pilula} from '../../colagem/tipos';
import {Brilho, Check} from '../../colagem/grafismos';
import {assentar, posterizar} from '../../colagem/movimento-colagem';
import type {Faixa} from '../../colagem/legenda';
import {fq, GraoFilme, Peca, Vinheta} from '../especial/apoio';
import {Manchete} from '../onze/teste/TesteCodigo';
import {ABERTURA, ate, BLOCOS_A, CENA_INICIO, em, FIM, PALAVRAS, S1, S2, S3, S4, S5, S6, S7, S8, S9} from './roteiro';
import {CLIPES, ESCALAS} from './tomadas';

export const DURACAO_JEITINHO = fq(FIM);
const F = fq;
type P = {q: number; ini: number; fim: number};

const LARANJA = '#D9601A', CARAMELO = '#A8701C', VERDE = '#2F6B45';

// ------------------------------------------------------------------ moldes
const cam = (q: number, k: number, ks: Chave[], id: string, extra: Array<ReturnType<typeof pulso>> = []) =>
  somar(cameraEm(k, ks), deriva(q, id, 0.7), ...extra);
const empurra = (dur: number, z0 = 1.03, z1 = 1.1, y1 = -24, x1 = 0): Chave[] => [
  {q: 0, x: 0, y: 0, zoom: z0, rot: 0},
  {q: dur, x: x1, y: y1, zoom: z1, rot: -0.5, curva: 'linear'},
];

/** O papel quadriculado novo (j09-papel-grade-mural, 1620x2880): fundo de todas as cenas de colagem. */
const PapelGrade: React.FC = () => (
  <Img src={staticFile('colagem/j09-papel-grade-mural.png')} style={{position: 'absolute', left: -270, top: -480, width: 1620, height: 2880}} />
);

const Papel: React.FC<{c: ReturnType<typeof cam>; id: string; fundo?: React.ReactNode; texto?: React.ReactNode; frente?: React.ReactNode; children: React.ReactNode}> = ({
  c, id, fundo, texto, frente, children,
}) => (
  <AbsoluteFill style={{background: COR.creme}}>
    <Palco cam={c} id={id}>
      <Plano p={0.6}><PapelGrade />{fundo}</Plano>
      <Plano p={1}>{children}</Plano>
      {texto && <Plano p={1.1}>{texto}</Plano>}
      {frente && <Plano p={2.3}>{frente}</Plano>}
    </Palco>
    <Vinheta forca={0.22} />
  </AbsoluteFill>
);

/**
 * Cartão de vídeo real: papel creme com borda, duas fitas no topo, assenta em stop-motion.
 * A escala (que take, de quando a quando) vem de tomadas.ts, conferida pelo teste para nunca
 * congelar; se ainda assim faltar clipe, ele ricocheteia em vez de parar no último quadro.
 */
const Cartao: React.FC<{q: number; escala: string; x: number; y: number; w: number; rot?: number;
  sobre?: (largura: number, altura: number) => React.ReactNode}> = ({q, escala, x, y, w, rot = 0, sobre}) => {
  const e = ESCALAS[escala];
  const ini = F(e.ini);
  const p = assentar(posterizar(q, 3, ini), ini, escala);
  if (!p.visivel) return null;
  const vis = e.tomadas.filter((t) => q >= F(t.desde));
  const t = vis.length ? vis[vis.length - 1] : e.tomadas[0];
  const m = CLIPES[t.src];
  const h = w / m.razao;
  const maxQ = Math.floor(m.duracao * 30) - 2;
  let qf = Math.round((t.de ?? 0) * 30 + (q - Math.max(ini, F(t.desde))) * (t.vel ?? 1));
  if (qf > maxQ) qf = Math.max(0, 2 * maxQ - qf); // ricochete, nunca congela
  const pulo = vis.length > 1 && q - F(t.desde) < 2 ? 1.035 : 1;
  const B = 16;
  return (
    <div style={{position: 'absolute', left: x - w / 2 - B, top: y - h / 2 - B, width: w + 2 * B, height: h + 2 * B,
      transform: `translateY(${p.dy}px) rotate(${rot + p.rot}deg) scale(${p.escala * pulo})`, opacity: p.opacidade}}>
      <div style={{position: 'absolute', inset: 0, background: '#F4EFE3', boxShadow: '0 14px 22px rgba(12,8,5,0.38)'}} />
      <div style={{position: 'absolute', left: B, top: B, width: w, height: h, overflow: 'hidden'}}>
        <Freeze frame={Math.max(0, qf)}>
          <OffthreadVideo src={staticFile(`fonte/clipes/${t.src}.mp4`)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </Freeze>
        {sobre?.(w, h)}
      </div>
      <Img src={staticFile('colagem/j09-fita-1-b0.png')} style={{position: 'absolute', left: -40, top: -26, width: 200, transform: 'rotate(-28deg)'}} />
      <Img src={staticFile('colagem/j09-fita-4-b0.png')} style={{position: 'absolute', right: -40, top: -22, width: 190, transform: 'rotate(24deg)'}} />
    </div>
  );
};

/** Cabeça recortada (sem boil: rosto que treme lê como falha, lição 68). */
const Cabeca: React.FC<{q: number; ini: number; quem: 'fabio' | 'paulo' | 'giuseppe'; x: number; y: number; w: number; rot?: number; fora?: number}> = ({
  q, ini, quem, x, y, w, rot = 0, fora,
}) => <Peca q={q} ini={ini} nome={`cab-${quem}`} x={x} y={y} w={w} rot={rot} fora={fora} semBoil />;

type Item = {t: string; q: number; cor?: string; tam?: number; ate: number};
/** Palavra-chave B: entra no quadro da palavra e sai em `ate(f)` (0,9 s depois, ou no B seguinte). */
const kw = (t: string, f: Faixa, cor?: string, tam?: number, palavra?: string): Item[] =>
  t.split(' ').map((w) => ({t: w, q: F(palavra ? em(f, palavra) : f.inicio), cor, tam, ate: F(ate(f))}));
/** Frase B em serifa, palavra a palavra no tempo da voz. */
const serifa = (f: Faixa, cor?: string, tam?: number): Item[] =>
  PALAVRAS.slice(f.de, f.ate + 1).map((p) => ({t: p.texto, q: F(p.inicio), cor, tam, ate: F(ate(f))}));

/** O texto B da vez, no mesmo lugar: o grupo mais recente que ainda está na janela. */
const Vez: React.FC<{q: number; x: number; y: number; itens: Item[]; largura?: number; fonte?: 'manchete' | 'serifa'; acumula?: boolean}> = ({
  q, x, y, itens, largura, fonte, acumula,
}) => {
  const vivos = itens.filter((i) => q >= i.q && q < i.ate);
  if (!vivos.length) return null;
  const qa = vivos[vivos.length - 1].q;
  // serifa acumula a frase inteira (palavra a palavra); manchete troca no lugar
  const mostra = acumula ? vivos : vivos.filter((i) => i.q === qa);
  return <Manchete q={q} x={x} y={y} itens={mostra} largura={largura} fonte={fonte} />;
};

// ------------------------------------------------------------------ 0 · abertura crua
// O vídeo do Rafael inteiro (3,0 s), sem voz e sem trilha. Nos últimos 14 quadros a
// câmera mergulha no reel do Fábio que roda na tela do notebook (medido no quadro: x 0,36,
// y 0,48) e um clarão leva para a colagem.
const MERGULHO = 14;
const C0: React.FC<P> = ({q, ini, fim}) => {
  const z0 = fim - MERGULHO;
  const t = Math.max(0, (q - z0) / MERGULHO);
  const zoom = 1 + t * t * 3.4;
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <AbsoluteFill style={{transform: `scale(${zoom})`, transformOrigin: `${0.36 * 1080}px ${0.48 * 1920}px`,
        filter: t > 0.35 ? `blur(${(t - 0.35) * 14}px)` : undefined}}>
        <Freeze frame={Math.min(q - ini, Math.floor(CLIPES.abertura.duracao * 30) - 2)}>
          <OffthreadVideo src={staticFile('fonte/clipes/abertura.mp4')} muted style={{width: '100%', height: '100%'}} />
        </Freeze>
      </AbsoluteFill>
      {t > 0.55 && <AbsoluteFill style={{background: `rgba(255,250,240,${Math.min(1, (t - 0.55) * 2.4)})`}} />}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------ 1 · gancho falado
const C1: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const tg = F(S1.tangerina.inicio), di = F(S1.diferente.inicio);
  const sai = Math.min(1, k / 8);
  const zoomEntrada = 1.7 - 0.7 * (1 - Math.pow(1 - sai, 3)); // vem do mergulho: chega grande e assenta
  const c = cam(q, k, empurra(fim - ini, 1.0, 1.08, -30), 'j1', [pulso(q, [tg, di], 0.04), tremor(q, di, 10, 4)]);
  return (
    <Papel c={c} id="j1"
      texto={<Vez q={q} x={540} y={300} itens={[...kw('TANGERINA', S1.tangerina, LARANJA, 120), ...kw('DIFERENTE?', S1.diferente, COR.preto, 118)]} />}
      frente={<Peca q={q} ini={tg + 2} nome="j09-gomo" x={1020 - k * 2} y={1680} w={300} rot={-24} semBoil />}>
      <div style={{position: 'absolute', inset: 0, transform: `scale(${zoomEntrada})`, transformOrigin: '540px 980px'}}>
        <Cartao q={q} escala="j1c" x={540} y={980} w={560} rot={-2} />
      </div>
      <Peca q={q} ini={tg} nome="j09-tangerina" x={180} y={1400} w={280} rot={-8} />
      <Peca q={q} ini={tg + 4} nome="j09-raspas" x={900} y={1440} w={240} rot={12} />
      <Cabeca q={q} ini={di} quem="paulo" x={900} y={620} w={290} rot={10} />
      <Cabeca q={q} ini={di + 3} quem="giuseppe" x={180} y={640} w={270} rot={-10} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 2 · premissa: três cabeças
const C2: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const cd = F(em(S2.cada, 'cada')), se = F(em(S2.cada, 'seu')), je = F(S2.jeitinho.inicio), tr = F(S2.tres.inicio), ca = F(em(S2.cara, 'cara'));
  const c = cam(q, k, [{q: 0, x: 0, y: 30, zoom: 1.06, rot: 0}, {q: tr - ini, x: 0, y: 0, zoom: 1.1, rot: -0.6}, {q: fim - ini, x: 30, y: -30, zoom: 1.15, rot: 0.4, curva: 'linear'}],
    'j2', [pulso(q, [je, tr, ca], 0.035)]);
  return (
    <Papel c={c} id="j2"
      fundo={<Img src={staticFile('colagem/j09-ceu-rasgado-b0.png')} style={{position: 'absolute', left: 60, top: 420, width: 1080, transform: 'rotate(-3deg)'}} />}
      texto={<Vez q={q} x={540} y={1290} itens={[...kw('JEITINHO', S2.jeitinho, LARANJA, 160), ...kw('3 JEITOS', S2.tres, COR.preto, 170)]} />}>
      <Cabeca q={q} ini={cd} quem="fabio" x={230} y={820} w={330} rot={-6} />
      <Cabeca q={q} ini={se} quem="paulo" x={545} y={760} w={320} rot={3} />
      <Cabeca q={q} ini={je} quem="giuseppe" x={860} y={830} w={300} rot={7} />
      <Peca q={q} ini={ca} nome="j09-estrela" x={545} y={460} w={180} rot={10} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 3 · Fábio: o processo
const Apresenta: React.FC<{q: number; ini: number; quem: 'fabio' | 'paulo' | 'giuseppe'; arroba: string; nome: number}> = ({q, ini, quem, arroba, nome}) => (
  <>
    <Cabeca q={q} ini={ini} quem={quem} x={240} y={500} w={250} rot={-6} />
    <Dymo q={q} ini={nome} texto={arroba} x={150} y={690} ancora="esq" tamanho={44} rot={-2} />
  </>
);
const C3: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const nome = F(S3.fabio.inicio), cg = F(S3.congela.inicio), ra = F(S3.rala.inicio), ag = F(S3.agua.inicio);
  const c = cam(q, k, empurra(fim - ini, 1.03, 1.1, -20, 20), 'j3', [pulso(q, [cg, ra, ag], 0.03)]);
  return (
    <Papel c={c} id="j3"
      texto={<Vez q={q} x={540} y={230} largura={880} itens={[...kw('CONGELA', S3.congela, LARANJA, 130), ...kw('RALA', S3.rala, LARANJA, 160),
        ...kw('ÁGUA', S3.agua, LARANJA, 160)]} />}
      frente={<Peca q={q} ini={ra} nome="j09-raspas" x={160 + k} y={1500} w={280} rot={-10} semBoil />}>
      <Cartao q={q} escala="j3c" x={600} y={1110} w={520} rot={2} />
      <Peca q={q} ini={cg} nome="j09-tangerina-aberta" x={910} y={1500} w={230} rot={8} />
      <Apresenta q={q} ini={ini} quem="fabio" arroba="@fabio.cafes" nome={nome} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 4 · a cor do café
const H_F4 = 560 / CLIPES.f4.razao; // altura do cartão do f4 (largura 560)
const C4: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const fr = F(S3.fruta.inicio), co = F(S3.cor.inicio);
  const c = cam(q, k, [{q: 0, x: 0, y: 0, zoom: 1.04, rot: 0}, {q: co - ini, x: 0, y: -10, zoom: 1.1, rot: 0.6}, {q: fim - ini, x: 0, y: -30, zoom: 1.2, rot: 1, curva: 'linear'}],
    'j4', [pulso(q, [fr, co], 0.04)]);
  return (
    <Papel c={c} id="j4"
      texto={<Vez q={q} x={540} y={330} itens={[...kw('FRUTA', S3.fruta, LARANJA, 160), ...kw('A COR!', S3.cor, COR.preto, 160)]} />}>
      <Cartao q={q} escala="j4c" x={540} y={1010} w={560} rot={-2} />
      <Peca q={q} ini={fr} nome="j09-gomo" x={170} y={1380} w={230} rot={-20} />
      <Peca q={q} ini={fr + 3} nome="j09-tangerina" x={900} y={600} w={230} rot={14} />
      {/* no instante do "cor" o copo do f4 está em (0,50 ; 0,66) do take — medido no quadro com grade
          (raspagem/_jeitinho-cafe/tmpf/f4g.png), não no olho: a v2 errou o lugar por estimar */}
      <Peca q={q} ini={co} nome="j09-circulo" x={540 - 280 + 0.5 * 560} y={1010 - H_F4 / 2 + 0.66 * H_F4} w={440} rot={-6} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 5 · re-gancho: o Paulo espia
const C5: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const ou = F(em(S4.ousado, 'ousado')), es = F(S4.espera.inicio), pr = F(em(S4.espera, 'próximo'));
  const espia = interpolate(q, [es, pr + 4], [1300, 840], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: (t) => 1 - Math.pow(1 - t, 3)});
  const c = cam(q, k, empurra(fim - ini, 1.05, 1.12, 0, 40), 'j5', [pulso(q, [ou], 0.05)]);
  return (
    <Papel c={c} id="j5"
      texto={<Vez q={q} x={540} y={760} acumula itens={[...kw('ACHOU', S4.ousado, COR.preto, 110), ...kw('OUSADO?', S4.ousado, LARANJA, 150, 'ousado')]} />}>
      <Cabeca q={q} ini={ini} quem="fabio" x={300} y={1240} w={300} rot={-8} />
      {q >= es && (
        <Img src={staticFile('colagem/cab-paulo-b0.png')} style={{position: 'absolute', left: espia - 190, top: 1160, width: 380, transform: 'rotate(-14deg)',
          filter: 'drop-shadow(0px 10px 12px rgba(12,8,5,0.36))'}} />
      )}
      <Peca q={q} ini={pr} nome="j09-seta-curva" x={650} y={1060} w={300} rot={20} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 6 · Paulo: paçoquita
const C6: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const nome = F(S5.paulo.inicio), pc = F(S5.pacoquita.inicio), is = F(S5.pacoquita2.inicio);
  const c = cam(q, k, empurra(fim - ini, 1.03, 1.1, -24, -20), 'j6', [pulso(q, [pc, is], 0.04), tremor(q, is, 10, 4)]);
  return (
    <Papel c={c} id="j6"
      texto={<Vez q={q} x={540} y={230} largura={880} itens={[...kw('PAÇOQUITA', S5.pacoquita, CARAMELO, 110), ...kw('PAÇOQUITA!', S5.pacoquita2, CARAMELO, 120)]} />}>
      <Cartao q={q} escala="j6c" x={610} y={1110} w={520} rot={-2} />
      <Peca q={q} ini={is} nome="j09-pacoquitas" x={210} y={1420} w={300} rot={-6} />
      <Peca q={q} ini={is + 4} nome="j09-pacoquita-farelo" x={930} y={1560} w={240} rot={10} />
      <Apresenta q={q} ini={ini} quem="paulo" arroba="@pauloposteral" nome={nome} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 7 · a pasta e o café por cima
const C7: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const le = F(S5.leite.inicio), pa = F(S5.pasta.inicio), jo = F(S5.joga.inicio), cf = F(S5.cafe.inicio);
  const c = cam(q, k, empurra(fim - ini, 1.04, 1.12, -30, 20), 'j7', [pulso(q, [le, pa, cf], 0.035)]);
  return (
    <Papel c={c} id="j7"
      texto={<Vez q={q} x={540} y={330} itens={[...kw('LEITE EM PÓ', S5.leite, CARAMELO, 100), ...kw('PASTA', S5.pasta, CARAMELO, 150),
        ...kw('CAFÉ POR CIMA', S5.cafe, COR.preto, 96)]} />}>
      <Cartao q={q} escala="j7c" x={540} y={1030} w={540} rot={2} />
      <Peca q={q} ini={le} nome="j09-leite-em-po" x={160} y={1460} w={230} rot={-4} />
      <Peca q={q} ini={pa} nome="j09-colher" x={920} y={640} w={260} rot={30} />
      <Peca q={q} ini={jo} nome="j09-jarra-cafe" x={900} y={1440} w={250} rot={-12} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 8 · dez milhões
const C8: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const dz = F(S5.dez.inicio), mi = F(em(S5.dez, 'milhões'));
  const c = cam(q, k, empurra(fim - ini, 1.04, 1.12, -20), 'j8', [pulso(q, [dz], 0.05), tremor(q, dz, 12, 4)]);
  return (
    <Papel c={c} id="j8"
      texto={<>
        <Vez q={q} x={540} y={1390} itens={kw('10 MI', S5.dez, COR.preto, 200)} />
        <Vez q={q} x={540} y={1520} itens={kw('DE VIEWS', S5.dez, CARAMELO, 80, 'visualizações')} />
      </>}>
      <Cartao q={q} escala="j8c" x={540} y={880} w={800} rot={-2} />
      {q < F(ate(S5.dez)) && <Peca q={q} ini={dz - 2} nome="j09-estrela" x={540} y={1430} w={640} rot={-6} semBoil />}
      <Brilho q={q} ini={mi} x={880} y={1280} r={90} cor={LARANJA} />
      <Brilho q={q} ini={mi + 4} x={190} y={1200} r={70} cor={LARANJA} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 9 · re-gancho: sem coador
const C9: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const co = F(S6.coador.inicio), te = F(S6.terceiro.inicio);
  const c = cam(q, k, empurra(fim - ini, 1.06, 1.14, 0), 'j9', [pulso(q, [co], 0.05), tremor(q, co, 12, 4)]);
  return (
    <Papel c={c} id="j9"
      texto={<Vez q={q} x={540} y={400} itens={[...kw('TERCEIRO', S6.terceiro, COR.preto, 140), ...kw('SEM COADOR?', S6.coador, VERDE, 120)]} />}>
      <Peca q={q} ini={te} nome="j09-coador-v60" x={540} y={1000} w={540} rot={-4} />
      <Peca q={q} ini={co} nome="j09-x-marcador" x={540} y={1000} w={560} rot={6} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 10 · Giuseppe: o creme de café de Milão, um take por passo
const C10: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const nome = F(S7.giuseppe.inicio), it = F(S7.italiano.inicio), cr = F(S7.creme.inicio), ba = F(S7.bate.inicio), ca = F(S7.cafe.inicio);
  const ag = F(S7.agua.inicio), bt = F(S7.batedeira.inicio);
  const c = cam(q, k, empurra(fim - ini, 1.03, 1.12, -20, 20), 'j10', [pulso(q, [it, cr, ba, ca, ag, bt], 0.025)]);
  return (
    <Papel c={c} id="j10"
      texto={<Vez q={q} x={540} y={230} largura={880} itens={[...kw('ITALIANO', S7.italiano, VERDE, 140), ...kw('CREME DE MILÃO', S7.creme, VERDE, 84, 'creme'),
        ...kw('MEL', S7.bate, VERDE, 170, 'mel'), ...kw('CAFÉ SOLÚVEL', S7.cafe, COR.preto, 96), ...kw('ÁGUA QUENTE', S7.agua, VERDE, 100),
        ...kw('BATEDEIRA', S7.batedeira, VERDE, 130)]} />}>
      <Cartao q={q} escala="j10c" x={600} y={1120} w={540} rot={2} />
      <Peca q={q} ini={ba} nome="j09-mel-pegador" x={170} y={1500} w={240} rot={-12} />
      <Peca q={q} ini={bt} nome="j09-batedeira" x={920} y={1560} w={260} rot={10} />
      <Apresenta q={q} ini={ini} quem="giuseppe" arroba="@giuseppecasale77" nome={nome} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 11 · vira creme e come de colher
const C11: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const cr = F(S7.cremeFim.inicio), co = F(S7.colher.inicio);
  const c = cam(q, k, empurra(fim - ini, 1.04, 1.12, -20), 'j11', [pulso(q, [cr, co], 0.04), tremor(q, co, 10, 4)]);
  return (
    <Papel c={c} id="j11"
      texto={<Vez q={q} x={540} y={300} itens={[...kw('CREME', S7.cremeFim, VERDE, 170), ...kw('DE COLHER!', S7.colher, COR.preto, 150)]} />}>
      <Cartao q={q} escala="j11c" x={540} y={1040} w={600} rot={-2} />
      <Peca q={q} ini={co} nome="j09-colher-creme" x={860} y={1560} w={340} rot={-14} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 12 · conclusão: os três juntos
const C12: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const tg = F(S8.tangerina.inicio), pc = F(S8.pacoquita.inicio), ap = F(S8.creme.inicio), ce = F(S8.certos.inicio);
  const c = cam(q, k, [{q: 0, x: 0, y: 0, zoom: 1.08, rot: 0}, {q: ce - ini, x: 0, y: -20, zoom: 1.02, rot: -0.4}, {q: fim - ini, x: 0, y: -40, zoom: 1.06, rot: 0.3, curva: 'linear'}],
    'j12', [pulso(q, [tg, pc, ap, ce], 0.03)]);
  return (
    <Papel c={c} id="j12"
      texto={<>
        <Vez q={q} x={540} y={1300} itens={[...kw('TANGERINA', S8.tangerina, LARANJA, 120), ...kw('PAÇOQUITA', S8.pacoquita, CARAMELO, 120),
          ...kw('CREME ITALIANO', S8.creme, VERDE, 110), ...kw('TODOS CERTOS', S8.certos, COR.preto, 130)]} />
        <Vez q={q} x={540} y={1300} fonte="serifa" largura={960} acumula itens={serifa(S8.jeitos, COR.preto, 92)} />
      </>}>
      <Cabeca q={q} ini={tg} quem="fabio" x={220} y={780} w={290} rot={-6} />
      <Peca q={q} ini={tg + 2} nome="j09-tangerina" x={220} y={1060} w={190} rot={-10} />
      <Cabeca q={q} ini={pc} quem="paulo" x={545} y={740} w={280} rot={3} />
      <Peca q={q} ini={pc + 2} nome="j09-pacoquitas" x={545} y={1030} w={210} rot={6} />
      <Cabeca q={q} ini={ap} quem="giuseppe" x={865} y={790} w={270} rot={7} />
      <Peca q={q} ini={ap + 2} nome="j09-copo-creme" x={865} y={1070} w={170} rot={-6} />
      {[220, 545, 865].map((x, i) => (
        <Check key={x} q={q} ini={ce + i * 3} cx={x + 110} cy={600} r={58} cor={VERDE} espessura={16} chave={`j12-${i}`} />
      ))}
    </Papel>
  );
};

// ------------------------------------------------------------------ 13 · a frase
const C13: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const se = F(em(S8.seu, 'seu'));
  // a câmera desacelera até parar no "seu": a frase é dita com o quadro quieto
  const c = somar(cameraEm(k, [{q: 0, x: 0, y: 20, zoom: 1.12, rot: 0.6}, {q: se - ini, x: 0, y: 0, zoom: 1.04, rot: 0, curva: 'suave'}, {q: fim - ini, x: 0, y: 0, zoom: 1.05, rot: 0, curva: 'linear'}]),
    deriva(q, 'j13', 0.3), pulso(q, [se], 0.05));
  const seu = PALAVRAS.slice(S8.seu.de, S8.seu.ate + 1).map((p, i): Item => ({
    t: p.texto.toUpperCase().replace(/!$/, '.'), q: F(p.inicio), tam: 150, cor: i === 2 ? LARANJA : COR.preto, ate: F(ate(S8.seu)),
  }));
  return (
    <Papel c={c} id="j13"
      texto={<>
        <Vez q={q} x={540} y={1130} fonte="serifa" largura={980} acumula itens={serifa(S8.porque, COR.preto, 84)} />
        <Vez q={q} x={540} y={1420} acumula itens={seu} />
      </>}>
      <Peca q={q} ini={ini} nome="j09-xicara-cima" x={540} y={720} w={560} rot={-4} />
      <Peca q={q} ini={ini + 4} nome="j09-graos-soltos" x={880} y={500} w={240} rot={20} />
    </Papel>
  );
};

// ------------------------------------------------------------------ 14 · a pergunta
const C14: React.FC<P> = ({q, ini, fim}) => {
  const k = q - ini;
  const vo = F(S9.voce.inicio), cm = F(S9.comenta.inicio);
  const c = cam(q, k, empurra(fim - ini, 1.06, 1.12, 20), 'j14', [pulso(q, [vo], 0.05), tremor(q, vo, 10, 4)]);
  return (
    <Papel c={c} id="j14"
      texto={<>
        <Vez q={q} x={540} y={1250} itens={kw('E VOCÊ?', S9.voce, LARANJA, 160)} />
        <Dymo q={q} ini={cm} texto="COMENTA AQUI" x={540} y={1420} tamanho={66} rot={-2} />
      </>}>
      <Cabeca q={q} ini={ini} quem="fabio" x={190} y={520} w={230} rot={-8} />
      <Cabeca q={q} ini={ini + 2} quem="paulo" x={540} y={470} w={220} rot={2} />
      <Cabeca q={q} ini={ini + 4} quem="giuseppe" x={890} y={520} w={210} rot={8} />
      <Peca q={q} ini={vo} nome="j09-silhueta" x={540} y={930} w={440} rot={0} semBoil />
      <Peca q={q} ini={cm + 4} nome="j09-seta-curva" x={880} y={1450} w={220} rot={100} />
    </Papel>
  );
};

// ------------------------------------------------------------------ montagem
const CENAS: Array<React.FC<P>> = [C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14];
const INI = CENA_INICIO.map((s) => F(s));
// chicote em toda troca de cena, menos a da abertura (lá o mergulho na tela é a transição)
const TROCAS = INI.slice(2);

const ef = (a: string, s: number, v = 0.5): [string, number, number] => [a, F(s), v];
const SONS: Array<[string, number, number]> = [
  ef('whoosh', ABERTURA - MERGULHO / 30, 0.55), ef('thump', ABERTURA, 0.5),
  ef('pop', S1.tangerina.inicio, 0.5), ef('carimbo', S1.diferente.inicio, 0.6),
  ef('carimbo', em(S2.cada, 'cada'), 0.45), ef('carimbo', em(S2.cada, 'seu'), 0.45), ef('carimbo', S2.jeitinho.inicio, 0.5),
  ef('pop', S2.tres.inicio, 0.5),
  ef('digitacao', S3.fabio.inicio, 0.4), ef('pop', S3.congela.inicio, 0.45), ef('slide', S3.rala.inicio, 0.4),
  ef('pop', S3.rala.inicio, 0.45), ef('pop', S3.agua.inicio, 0.45),
  ef('pop', S3.fruta.inicio, 0.45), ef('rabisco', S3.cor.inicio, 0.5),
  ef('pop', em(S4.ousado, 'ousado'), 0.55), ef('slide', S4.espera.inicio, 0.45),
  ef('digitacao', S5.paulo.inicio, 0.4), ef('pop', S5.pacoquita.inicio, 0.45), ef('carimbo', S5.pacoquita2.inicio, 0.65),
  ef('pop', S5.leite.inicio, 0.45), ef('pop', S5.pasta.inicio, 0.45), ef('golinho', S5.joga.inicio, 0.4),
  ef('carimbo', S5.dez.inicio, 0.7), ef('brilho', em(S5.dez, 'milhões'), 0.5),
  ef('pop', S6.terceiro.inicio, 0.45), ef('carimbo', S6.coador.inicio, 0.6), ef('rabisco', S6.coador.inicio + 0.1, 0.5),
  ef('digitacao', S7.giuseppe.inicio, 0.4), ef('pop', S7.italiano.inicio, 0.5),
  ...[S7.creme, S7.bate, S7.cafe, S7.agua].map((f) => ef('pop', f.inicio, 0.45)),
  ef('slide', S7.batedeira.inicio, 0.45), ef('pop', S7.cremeFim.inicio, 0.5), ef('carimbo', S7.colher.inicio, 0.6),
  ef('carimbo', S8.tangerina.inicio, 0.45), ef('carimbo', S8.pacoquita.inicio, 0.45), ef('carimbo', S8.creme.inicio, 0.45),
  ef('tink', S8.certos.inicio, 0.5), ef('tink', S8.certos.inicio + 0.1, 0.4), ef('tink', S8.certos.inicio + 0.2, 0.4),
  ef('pop', em(S8.seu, 'seu'), 0.55),
  ef('carimbo', S9.voce.inicio, 0.65), ef('digitacao', S9.comenta.inicio, 0.4),
  ...TROCAS.map((t): [string, number, number] => ['chicote', t - 5, 0.45]),
];

export const Jeitinho: React.FC = () => {
  const q = useCurrentFrame();
  let i = 0;
  for (let n = 0; n < INI.length; n++) if (q >= INI[n]) i = n;
  const C = CENAS[i];
  const ini = INI[i];
  const fim = INI[i + 1] ?? DURACAO_JEITINHO;
  const perto = TROCAS.map((t) => q - t).find((d) => d >= -3 && d < 3);
  const kk = perto === undefined ? 0 : 1 - Math.abs(perto + 0.5) / 3.5;
  const desl = perto === undefined ? 0 : (perto < 0 ? -1 : 1) * kk * -160;
  const fimFala = F(PALAVRAS[PALAVRAS.length - 1].fim + 0.2);
  const trilha = (f: number) => {
    const sobe = interpolate(f, [fimFala, fimFala + 6], [0.14, 0.3], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const sai = interpolate(f, [DURACAO_JEITINHO - 10, DURACAO_JEITINHO], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    return sobe * sai;
  };
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      {/* o deslize do chicote amplia junto: sem isso a borda revelava o fundo preto (lição 58) */}
      <AbsoluteFill style={{transform: `translateX(${desl}px) scale(${1 + (Math.abs(desl) * 2) / 1080})`, filter: kk > 0 ? `blur(${kk * 18}px)` : undefined}}>
        <C q={q} ini={ini} fim={fim} />
      </AbsoluteFill>
      {q >= F(ABERTURA) && <GraoFilme q={q} forca={0.05} />}
      {/* legenda A: a fala que não virou palavra-chave, fora do chicote (fica nítida) */}
      <Pilula q={q} fps={30} blocos={BLOCOS_A} y={1560} tamanho={58} />
      <Sequence durationInFrames={F(ABERTURA)}><Audio src={staticFile('fonte/abertura-ambiente.wav')} volume={0.9} /></Sequence>
      <Sequence from={F(ABERTURA)}><Audio src={staticFile('fonte/narracao-v2-sinc.wav')} /></Sequence>
      <Sequence from={F(ABERTURA)}><Audio src={staticFile('sfx/trilha.wav')} volume={(f) => trilha(f + F(ABERTURA))} /></Sequence>
      {SONS.map(([a, s, v], n) => (
        <Sequence key={n} from={Math.max(0, s)} durationInFrames={60}><Audio src={staticFile(`sfx/${a}.wav`)} volume={v * 0.75} /></Sequence>
      ))}
    </AbsoluteFill>
  );
};
