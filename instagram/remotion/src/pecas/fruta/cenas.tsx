// Peça 08, as cenas. Vídeo real tratado no meio da colagem: toda cena de vídeo tem
// câmera (deriva + empurrão) e texto cinético; toda cena de colagem tem 3 planos.
// Tempos: roteiro.ts. Nenhum segundo digitado — só `em()`, `.inicio`, `.fim`, CENA_INICIO.

import React from 'react';
import {AbsoluteFill} from 'remotion';
import {COR} from '../../identidade/tokens';
import {cameraEm, deriva, pulso, somar, tremor, type Chave} from '../../colagem/camera';
import {Brilho, Check, Cruz, Elipse, Seta, Xis} from '../../colagem/grafismos';
import {Palco, Plano} from '../../colagem/palco';
import {Dymo, Marcador, Recortadas, Serifa} from '../../colagem/tipos';
import {Carimbo, Embalagem} from '../../colagem/pecas';
import {progresso} from '../../colagem/movimento-colagem';
import {Clipe, fala, FotoCheia, fq, Fundo, Peca, Silabas, SombraFolhas, Tachinha, Vinheta} from './apoio';
import {CENA_INICIO, em, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14} from './roteiro';

type C = {q: number};
const cam = (q: number, chaves: Chave[], chave: string, i: number, pulsos: number[] = [], tremores: number[] = []) =>
  somar(cameraEm(q, chaves), deriva(q, chave, i), pulso(q, pulsos), ...tremores.map((t) => tremor(q, t)));
const IQ = CENA_INICIO.map(fq);
/** Empurrão lento de câmera do começo ao fim da cena n. */
const empurra = (n: number, z0 = 1, z1 = 1.08, y1 = -20): Chave[] => [
  {q: IQ[n], x: 0, y: 0, zoom: z0, rot: 0},
  {q: (IQ[n + 1] ?? IQ[n] + 60) + 6, x: 0, y: y1, zoom: z1, rot: -0.4, curva: 'linear'},
];
const NAO = (q: number, ini: number, x: number, y: number, chave: string, tam = 200, rot = -8) => (
  <Carimbo q={q} ini={ini} x={x} y={y} rot={rot} tamanho={tam} cor={COR.acento} chave={chave}>NÃO</Carimbo>
);

// ===================================================================== 0 · já foi uma fruta
// O gancho é LIMPO: só o vídeo, o zoom no cacho, a seta e a legenda. O cacho foi medido
// no clipe tratado (máscara de vermelho): (478,1042) no segundo 7,65 do clipe, (511,1018)
// em 8,7, (549,1048) em 9,2 e (597,1093) em 9,6, no quadro 1080x1920 antes da escala
// 1,08 do Clipe. A câmera segue esse centro para o cacho chegar e FICAR no meio da tela.
const naTela = (x: number, y: number) => ({x: (x - 540) * 1.08, y: (y - 960) * 1.08});
export const Cena0: React.FC<C> = ({q}) => {
  const ja = fq(S1.jaFoi.inicio);
  const fr = fq(S1.fruta.inicio);
  const a = naTela(511, 1018);
  const b = naTela(549, 1048);
  const d = naTela(610, 1105);
  const c = cam(q, [
    {q: 0, x: 0, y: 0, zoom: 1.0, rot: 0},
    {q: ja, x: a.x * 0.3, y: a.y * 0.3, zoom: 1.12, rot: 0, curva: 'linear'},
    {q: fr + 4, x: b.x, y: b.y, zoom: 1.7, rot: -1.5, curva: 'rapida'},
    {q: IQ[1] + 6, x: d.x, y: d.y, zoom: 1.85, rot: -2, curva: 'linear'},
  ], 'f0', 0.5, [fr], [fr + 4]);
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={c} id="f0">
        <Plano p={1}><Clipe q={q} ini={IQ[0]} src="v2" de={7.65} vel={0.75} /></Plano>
      </Palco>
      <Vinheta forca={0.5} />
      {/* fora do palco: a seta aponta para o centro, onde o zoom deixa o cacho */}
      <Seta q={q} ini={fr + 2} de={[150, 600]} para={[430, 870]} curva={0.35} cor={COR.creme} chave="f0-seta" espessura={17} />
      <Silabas q={q} ini={fr} dur={fala(S1.fruta)} texto="U/MA|FRU/TA" x={540} y={430} tamanho={210} chave="f0-fruta" />
    </AbsoluteFill>
  );
};

// ===================================================================== 1 · vermelha, doce
export const Cena1: React.FC<C> = ({q}) => {
  const v = fq(S2.vermelha.inicio);
  const d = fq(S2.doce.inicio);
  const c = cam(q, empurra(1, 1.1, 1.2, 40), 'f1', 1.4, [v, d]);
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={c} id="f1">
        <Plano p={1}><Clipe q={q} ini={IQ[1]} src="v2" de={3.0} escala={1.35} /></Plano>
        <Plano p={1.1}>
          <Silabas q={q} ini={v} dur={fala(S2.vermelha)} texto="VER/ME/LHA" x={540} y={560} tamanho={190} chave="f1-v" fora={d} />
          <Silabas q={q} ini={d} dur={fala(S2.doce)} texto="DO/CE" x={540} y={760} tamanho={260} chave="f1-d" />
          <Brilho q={q} ini={d + 3} x={830} y={640} r={90} cor={COR.acento} />
          <Brilho q={q} ini={d + 7} x={250} y={880} r={60} cor={COR.creme} />
        </Plano>
      </Palco>
      <Vinheta forca={0.4} />
    </AbsoluteFill>
  );
};

// ===================================================================== 2 · nunca viu no supermercado
export const Cena2: React.FC<C> = ({q}) => {
  const s = fq(S2.super.inicio);
  const c = cam(q, empurra(2, 1.0, 1.06, -10), 'f2', 1, [fq(em(S2.nunca, 'nunca')), s], [s + 8]);
  return (
    <AbsoluteFill>
      <Fundo cor={COR.creme} forca={0.5} />
      <Palco cam={c} id="f2">
        <Plano p={0.6}><SombraFolhas q={q} opacidade={0.18} /></Plano>
        <Plano p={1}>
          <Peca q={q} ini={IQ[2]} nome="cachinho" x={400} y={760} w={480} rot={-6} />
          <Tachinha q={q} ini={IQ[2] + 3} x={400} y={550} cor="terra" />
          <Peca q={q} ini={s - 3} nome="carrinho-mercado" x={790} y={1000} w={380} rot={4} />
          <Marcador q={q} ini={fq(em(S2.nunca, 'nunca'))} texto="nunca viu?" x={300} y={1130} tamanho={70} rot={-5} chave="f2-nunca" />
          <Dymo q={q} ini={s} texto="SUPERMERCADO" x={540} y={1300} tamanho={92} rot={-2} />
          <Xis q={q} ini={s + 10} cx={540} cy={1300} r={250} cor={COR.acento} espessura={16} chave="f2-x" />
        </Plano>
        <Plano p={2.4}>
          <Peca q={q} ini={IQ[2]} nome="folha-2" x={1000} y={300} w={480} rot={-35} sombra={false} />
          <Peca q={q} ini={IQ[2]} nome="cereja-vermelha-1" x={110} y={1650} w={260} rot={20} sombra={false} />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};

// ===================================================================== 3 · o exame
export const Cena3: React.FC<C> = ({q}) => {
  const a = fq(S3.acucar.inicio);
  const ex = fq(S3.exame.inicio);
  const c = cam(q, [
    {q: IQ[3], x: 0, y: 0, zoom: 1.0, rot: 0},
    {q: fq(S3.e.inicio), x: 0, y: -40, zoom: 1.08, rot: 0.5, curva: 'linear'},
    {q: IQ[4] + 6, x: 0, y: 40, zoom: 1.16, rot: -0.5},
  ], 'f3', 1, [a, ex], [ex]);
  return (
    <AbsoluteFill>
      <Fundo cor="#E9DFCB" forca={0.55} />
      <Palco cam={c} id="f3">
        <Plano p={0.6}><SombraFolhas q={q} opacidade={0.15} /></Plano>
        <Plano p={1}>
          <Peca q={q} ini={IQ[3]} nome="post-it" x={540} y={760} w={760} rot={-3} unico={false} />
          <Marcador q={q} ini={IQ[3] + 4} texto="ANTES DE COLHER" x={540} y={560} tamanho={60} papel={null} tinta={COR.preto} rot={-3} chave="f3-antes" dur={fala(S3.antes)} />
          <Peca q={q} ini={fq(S3.mede.inicio)} nome="cereja-vermelha-2" x={360} y={800} w={210} rot={-10} />
          <Peca q={q} ini={fq(em(S3.mede, 'mede')) + 2} nome="refratometro" x={660} y={790} w={430} rot={-12} />
          <Dymo q={q} ini={a} texto="AÇÚCAR" x={540} y={1040} tamanho={96} rot={-2} />
          <Marcador q={q} ini={a + 6} texto="brix" x={860} y={920} tamanho={66} rot={9} chave="f3-brix" />
          <Recortadas q={q} ini={ex} texto="EXAME" x={540} y={1300} tamanho={150} chave="f3-ex" />
          <Check q={q} ini={ex + 10} cx={880} cy={1180} r={70} cor={COR.acento} chave="f3-ck" espessura={14} />
        </Plano>
        <Plano p={2.4}>
          <Peca q={q} ini={IQ[3]} nome="folha-5" x={120} y={260} w={460} rot={30} sombra={false} />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};

// ===================================================================== 4 · só as maduras
export const Cena4: React.FC<C> = ({q}) => {
  const m = fq(S4.maduras.inicio);
  const c = cam(q, empurra(4, 1.05, 1.15, 0), 'f4', 1.4, [m, fq(S4.vem.inicio)]);
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={c} id="f4">
        <Plano p={1}><Clipe q={q} ini={IQ[4]} src="v2" de={6.2} /></Plano>
        <Plano p={1.1}>
          <Silabas q={q} ini={m} dur={fala(S4.maduras)} texto="SÓ AS|MA/DU/RAS" x={540} y={520} tamanho={170} chave="f4-m" />
          <Elipse q={q} ini={fq(S4.vem.inicio)} cx={600} cy={1120} rx={210} ry={240} cor={COR.creme} chave="f4-el" espessura={10} />
        </Plano>
      </Palco>
      <Vinheta forca={0.4} />
    </AbsoluteFill>
  );
};

// ===================================================================== 5 · as outras esperam a vez
export const Cena5: React.FC<C> = ({q}) => {
  const e = fq(S4.esperam.inicio);
  const c = cam(q, empurra(5, 1.02, 1.08, -20), 'f5', 1, [e]);
  return (
    <AbsoluteFill>
      <Fundo cor={COR.creme} forca={0.5} />
      <Palco cam={c} id="f5">
        <Plano p={1}>
          <Peca q={q} ini={IQ[5]} nome="cereja-verde-1" x={330} y={760} w={230} rot={-12} />
          <Peca q={q} ini={IQ[5] + 3} nome="cereja-amarela-2" x={560} y={720} w={230} rot={8} />
          <Peca q={q} ini={IQ[5] + 6} nome="cereja-verde-1" x={780} y={790} w={210} rot={18} />
          <Marcador q={q} ini={e} texto="esperam a vez..." x={540} y={1110} tamanho={96} rot={-4} chave="f5-esp" dur={fala(S4.esperam)} />
          <Cruz q={q} ini={e + 4} x={180} y={520} cor={COR.terra} chave="f5-c1" />
          <Cruz q={q} ini={e + 8} x={900} y={1000} s={44} cor={COR.terra} chave="f5-c2" />
        </Plano>
        <Plano p={2.4}>
          <Peca q={q} ini={IQ[5]} nome="folha-1" x={980} y={1680} w={560} rot={-30} sombra={false} />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};

// ===================================================================== 6 · terreiro, frango de padaria
export const Cena6: React.FC<C> = ({q}) => {
  const sol = fq(S5.sol.inicio);
  const rv = fq(S5.revirada.inicio);
  const fr = fq(S5.frango.inicio);
  const c = cam(q, [
    {q: IQ[6], x: 0, y: 40, zoom: 1.04, rot: 0},
    {q: rv, x: 0, y: 0, zoom: 1.1, rot: 0, curva: 'linear'},
    // "revirada e revirada": a câmera gira junto, como o rodo no terreiro
    {q: fr, x: 0, y: -20, zoom: 1.18, rot: -6},
    {q: IQ[7] + 6, x: 0, y: -30, zoom: 1.22, rot: 4},
  ], 'f6', 1.2, [sol, rv, fr]);
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={c} id="f6">
        <Plano p={1}><Clipe q={q} ini={IQ[6]} src="v1" de={1.6} /></Plano>
        <Plano p={1.1}>
          <Silabas q={q} ini={sol} dur={fala(S5.sol)} texto="SOL" x={540} y={430} tamanho={300} chave="f6-sol" fora={rv} />
          <Brilho q={q} ini={sol + 2} x={820} y={330} r={130} cor={COR.acento} />
          <Silabas q={q} ini={rv} dur={fala(S5.revirada)} texto="RE/VI/RA/DA|E RE/VI/RA/DA" x={540} y={560} tamanho={130} chave="f6-rv" fora={fr} />
          <Marcador q={q} ini={fr} texto="tipo frango" x={420} y={470} tamanho={84} rot={-5} chave="f6-frango" dur={fq(em(S5.frango, 'de') - S5.frango.inicio)} />
          <Marcador q={q} ini={fq(em(S5.frango, 'de'))} texto="de padaria" x={640} y={600} tamanho={72} rot={3} chave="f6-padaria" dur={fq(S5.frango.fim - em(S5.frango, 'de'))} />
          <div style={{position: 'absolute', inset: 0, transformOrigin: '540px 1080px', transform: `scaleY(${0.82 + 0.18 * Math.cos((q - fr) / 3)})`}}>
            <Peca q={q} ini={fr} nome="frango-padaria" x={540} y={1080} w={640} rot={-3} />
          </div>
          <Elipse q={q} ini={fr + 6} cx={540} cy={1080} rx={380} ry={170} cor={COR.creme} chave="f6-el" espessura={9} />
          <Seta q={q} ini={fr + 10} de={[920, 1060]} para={[840, 1220]} curva={0.4} cor={COR.creme} chave="f6-s" />
        </Plano>
      </Palco>
      <Vinheta forca={0.4} />
    </AbsoluteFill>
  );
};

// ===================================================================== 7 · perdeu a casca
export const Cena7: React.FC<C> = ({q}) => {
  const k = fq(S6.casca.inicio);
  const c = cam(q, empurra(7, 1.0, 1.06, 0), 'f7', 1, [k]);
  return (
    <AbsoluteFill>
      <Fundo cor="#D9C3A0" forca={0.55} />
      <Palco cam={c} id="f7">
        <Plano p={1}>
          {/* a cereja seca (coco) perde a casca na palavra: ela sai arrancada e o grão fica */}
          <Peca q={q} ini={IQ[7]} nome="cereja-seca" x={540} y={880} w={380} rot={6} fora={k} />
          <Peca q={q} ini={k} nome="casca" x={470} y={860} w={360} rot={-14} fora={k + 3} />
          <Peca q={q} ini={k + 2} nome="grao-01" x={560} y={900} w={300} rot={-8} />
          <Marcador q={q} ini={k} texto="tchau, casca" x={540} y={1260} tamanho={88} rot={-3} chave="f7-c" />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};

// ===================================================================== 8 · cinco máquinas que dizem não
export const Cena8: React.FC<C> = ({q}) => {
  const dif = fq(S7.dificil.inicio);
  const cin = fq(S7.cinco.inicio);
  const nao = fq(S7.nao.inicio);
  const c = cam(q, [
    {q: IQ[8], x: 0, y: 0, zoom: 1.02, rot: 0},
    {q: nao, x: 0, y: -30, zoom: 1.16, rot: -1, curva: 'linear'},
    {q: IQ[9] + 6, x: 0, y: -30, zoom: 1.2, rot: -1},
  ], 'f8', 1, [dif, cin], [nao]);
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={c} id="f8">
        <Plano p={1}><Clipe q={q} ini={IQ[8]} src="v4" de={0.2} escuro={0.25} /></Plano>
        <Plano p={1.1}>
          <Silabas q={q} ini={dif} dur={fala(S7.dificil)} texto="MAIS|DI/FÍ/CIL" x={540} y={480} tamanho={170} chave="f8-d" fora={cin} />
          <Recortadas q={q} ini={cin} texto="5" x={540} y={560} tamanho={420} chave="f8-5" />
          <Dymo q={q} ini={fq(em(S7.cinco, 'máquinas'))} texto="MÁQUINAS" x={540} y={860} tamanho={100} rot={-2} />
          {NAO(q, nao, 540, 1120, 'f8-nao', 220)}
        </Plano>
      </Palco>
      <Vinheta forca={0.5} />
    </AbsoluteFill>
  );
};

// ===================================================================== 9–12 · a rajada
const Rajada: React.FC<{q: number; n: number; fundo: string; alvo: React.ReactNode; nao: number; texto: string; dur: number; ini2: number}> = ({
  q, n, fundo, alvo, nao, texto, dur, ini2,
}) => {
  const c = cam(q, empurra(n, 1.0, 1.1, 0), `r${n}`, 1.4, [nao], [nao]);
  return (
    <AbsoluteFill>
      <Fundo cor={fundo} forca={0.55} />
      <Palco cam={c} id={`r${n}`}>
        <Plano p={1}>
          {alvo}
          {NAO(q, nao, 540, 520, `r${n}-nao`, 230, n % 2 ? 7 : -8)}
          <Marcador q={q} ini={ini2} texto={texto} x={540} y={1340} tamanho={100} rot={n % 2 ? -4 : 3} chave={`r${n}-t`} dur={dur} />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};
export const Cena9: React.FC<C> = ({q}) => (
  <Rajada q={q} n={9} fundo={COR.creme} nao={fq(S8.n1.inicio)} texto="PEDRA" ini2={fq(S8.pedra.inicio)} dur={fala(S8.pedra)}
    alvo={<Peca q={q} ini={IQ[9]} nome="pedra" x={540} y={930} w={420} rot={-6} />} />
);
export const Cena10: React.FC<C> = ({q}) => (
  <Rajada q={q} n={10} fundo="#D9C3A0" nao={fq(S8.n2.inicio)} texto="GRAVETO" ini2={fq(S8.graveto.inicio)} dur={fala(S8.graveto)}
    alvo={<Peca q={q} ini={IQ[10]} nome="graveto" x={540} y={930} w={760} rot={-18} />} />
);
export const Cena11: React.FC<C> = ({q}) => {
  const nao = fq(S8.n3.inicio);
  const c = cam(q, empurra(11, 1.05, 1.16, -20), 'r11', 1.4, [nao], [nao]);
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={c} id="r11">
        <Plano p={1}><Clipe q={q} ini={IQ[11]} src="v5" de={8.9} /></Plano>
        <Plano p={1.1}>
          {NAO(q, nao, 540, 480, 'r11-nao', 230, -6)}
          <Silabas q={q} ini={fq(S8.leve.inicio)} dur={fala(S8.leve)} texto="GRÃO|LE/VE" x={360} y={860} tamanho={150} chave="r11-l" />
        </Plano>
      </Palco>
      <Vinheta forca={0.45} />
    </AbsoluteFill>
  );
};
export const Cena12: React.FC<C> = ({q}) => {
  const nao = fq(S8.n4.inicio);
  const [p, v, a] = [fq(S8.preto.inicio), fq(S8.verde.inicio), fq(S8.ardido.inicio)];
  const c = cam(q, empurra(12, 1.0, 1.08, 0), 'r12', 1.4, [nao, p, v, a], [nao]);
  const graos: Array<[string, number, number, string]> = [['grao-preto', p, 230, 'preto'], ['grao-imaturo', v, 540, 'verde'], ['grao-ardido', a, 850, 'ardido']];
  return (
    <AbsoluteFill>
      <Fundo cor={COR.creme} forca={0.55} />
      <Palco cam={c} id="r12">
        <Plano p={1}>
          {NAO(q, nao, 540, 470, 'r12-nao', 230, 6)}
          {graos.map(([nome, ini, x, t]) => (
            <React.Fragment key={nome}>
              <Peca q={q} ini={ini} nome={nome} x={x} y={980} w={240} rot={x === 540 ? 6 : -8} />
              <Xis q={q} ini={ini + 5} cx={x} cy={980} r={130} cor={COR.acento} espessura={14} chave={`r12-x-${t}`} />
              <Marcador q={q} ini={ini + 2} texto={t} x={x} y={1240} tamanho={70} rot={x === 540 ? 3 : -4} chave={`r12-${t}`} />
            </React.Fragment>
          ))}
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};

// ===================================================================== 13 · quem sobrou
export const Cena13: React.FC<C> = ({q}) => {
  const c = cam(q, empurra(13, 1.04, 1.14, -20), 'f13', 1.2, [fq(em(S9.quem, 'sobrou'))]);
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={c} id="f13">
        <Plano p={1}><Clipe q={q} ini={IQ[13]} src="v5" de={13.3} /></Plano>
        <Plano p={1.1}>
          <Silabas q={q} ini={fq(em(S9.quem, 'sobrou'))} dur={fq(0.5)} texto="SO/BROU" x={540} y={470} tamanho={220} chave="f13-s" />
          <Brilho q={q} ini={fq(em(S9.quem, 'sobrou')) + 6} x={830} y={1030} r={80} cor={COR.acento} />
        </Plano>
      </Palco>
      <Vinheta forca={0.4} />
    </AbsoluteFill>
  );
};

// ===================================================================== 14 · por tamanho, antes da hora
export const Cena14: React.FC<C> = ({q}) => {
  const t = fq(S9.tamanho.inicio);
  const h = fq(S9.torrar.inicio);
  const c = cam(q, empurra(14, 1.0, 1.08, -20), 'f14', 1, [t, h]);
  return (
    <AbsoluteFill>
      <Fundo cor="#E9DFCB" forca={0.55} />
      <Palco cam={c} id="f14">
        <Plano p={0.6}><SombraFolhas q={q} opacidade={0.15} /></Plano>
        <Plano p={1}>
          <Peca q={q} ini={t} nome="peneira-classificacao" x={540} y={860} w={560} rot={-4} />
          <Peca q={q} ini={t + 2} nome="grao-01" x={240} y={1200} w={130} rot={-10} />
          <Peca q={q} ini={t + 4} nome="grao-02" x={420} y={1200} w={180} rot={8} />
          <Peca q={q} ini={t + 6} nome="grao-03" x={640} y={1190} w={240} rot={-4} />
          <Silabas q={q} ini={t} dur={fala(S9.tamanho)} texto="TA/MA/NHO" x={540} y={460} tamanho={200} cor={COR.preto} chave="f14-t" />
          <Marcador q={q} ini={h} texto="nada de torrar antes da hora" x={540} y={1430} tamanho={64} rot={-3} chave="f14-h" dur={fala(S9.torrar)} />
        </Plano>
        <Plano p={2.4}>
          <Peca q={q} ini={IQ[14]} nome="folha-2" x={100} y={300} w={460} rot={25} sombra={false} />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};

// ===================================================================== 15 · o fogo
export const Cena15: React.FC<C> = ({q}) => {
  const fogo = fq(S10.fogo.inicio);
  const sim = fq(S10.sim.inicio);
  const c = cam(q, [
    {q: IQ[15], x: 0, y: 0, zoom: 1.0, rot: 0},
    {q: fogo, x: 0, y: 0, zoom: 1.12, rot: 2, curva: 'linear'},
    {q: IQ[16] + 6, x: 0, y: 0, zoom: 1.24, rot: -2},
  ], 'f15', 1.2, [fogo, fq(em(S10.fogo, 'fogo')), sim], [fq(em(S10.fogo, 'fogo'))]);
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={c} id="f15">
        {/* 2,4 s de torrador esticados a 0,55x: cobre a cena inteira sem repetir */}
        <Plano p={1}><Clipe q={q} ini={IQ[15]} src="v3" de={0} vel={0.55} /></Plano>
        <Plano p={1.1}>
          <Marcador q={q} ini={IQ[15] + 2} texto="depois de tudo isso..." x={540} y={420} tamanho={66} rot={-3} chave="f15-dep" dur={fala(S10.depoisTudo)} fora={fogo} />
          <Peca q={q} ini={fq(em(S10.fogo, 'fogo'))} nome="chama" x={540} y={1060} w={360} treme={fq(em(S10.fogo, 'fogo')) + 4} fora={IQ[16] + 2} />
          <Peca q={q} ini={fq(em(S10.fogo, 'fogo')) + 3} nome="chama" x={300} y={1180} w={220} rot={-10} treme={fq(em(S10.fogo, 'fogo')) + 6} fora={IQ[16] + 2} />
          <Silabas q={q} ini={fq(em(S10.fogo, 'fogo'))} dur={fq(0.4)} texto="FO/GO" x={540} y={520} tamanho={300} cor="#FFD7A8" chave="f15-fogo" fora={sim} />
          <Serifa q={q} ini={sim} texto="Sim." x={540} y={560} tamanho={220} cor={COR.creme} rot={-4} />
          <Marcador q={q} ini={fq(S10.depois2.inicio)} texto="depois de TUDO isso." x={540} y={860} tamanho={70} rot={3} chave="f15-dep2" dur={fala(S10.depois2)} />
        </Plano>
      </Palco>
      <Vinheta forca={0.45} />
    </AbsoluteFill>
  );
};

// ===================================================================== 16–19 · a prova
const Prova: React.FC<{q: number; n: number; de: number; children?: React.ReactNode; pulsos?: number[]}> = ({q, n, de, children, pulsos = []}) => {
  const c = cam(q, empurra(n, 1.06, 1.14, -10), `p${n}`, 1.2, pulsos);
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={c} id={`p${n}`}>
        <Plano p={1}><Clipe q={q} ini={IQ[n]} src="v6" de={de} escala={1.12} /></Plano>
        <Plano p={1.1}>{children}</Plano>
      </Palco>
      <Vinheta forca={0.4} />
    </AbsoluteFill>
  );
};
export const Cena16: React.FC<C> = ({q}) => {
  const p = fq(S11.provou.inicio);
  const b = fq(S11.barulho.inicio);
  return (
    <Prova q={q} n={16} de={1.54} pulsos={[p, b]}>
      <Silabas q={q} ini={p} dur={fala(S11.provou)} texto="PRO/VOU" x={540} y={430} tamanho={210} chave="p16-p" fora={b} />
      <Recortadas q={q} ini={b} texto="SLURP!" x={540} y={470} tamanho={150} chave="p16-slurp" />
      <Brilho q={q} ini={b + 4} x={300} y={760} r={70} cor={COR.acento} />
    </Prova>
  );
};
export const Cena17: React.FC<C> = ({q}) => (
  <Prova q={q} n={17} de={13.2} pulsos={[fq(S11.cheirou.inicio)]}>
    <Silabas q={q} ini={fq(S11.cheirou.inicio)} dur={fala(S11.cheirou)} texto="CHEI/ROU" x={540} y={430} tamanho={200} chave="p17" />
  </Prova>
);
export const Cena18: React.FC<C> = ({q}) => (
  <Prova q={q} n={18} de={14.9}>
    <Marcador q={q} ini={fq(em(S11.deNovo, 'novo'))} texto="de novo" x={540} y={430} tamanho={100} rot={-4} chave="p18" />
  </Prova>
);
export const Cena19: React.FC<C> = ({q}) => {
  const t = fq(S11.tecnica.inicio);
  return (
    <Prova q={q} n={19} de={21.9} pulsos={[t, fq(em(S11.tecnica, 'juro'))]}>
      <Serifa q={q} ini={t} texto="é técnica," x={520} y={330} tamanho={140} cor={COR.creme} rot={-4} />
      <Marcador q={q} ini={fq(em(S11.tecnica, 'juro'))} texto="JURO" x={800} y={490} tamanho={90} rot={6} chave="p19-j" />
    </Prova>
  );
};

// ===================================================================== 20 · a virada, no escuro
export const Cena20: React.FC<C> = ({q}) => {
  const [f, s, g] = [fq(S12.fruta.inicio), fq(S12.semente.inicio), fq(S12.grao.inicio)];
  const mas = fq(S12.mas.inicio);
  const apaga = 1 - 0.75 * progresso(q, mas, fq(em(S12.nada, 'virou')));
  const c = cam(q, [
    {q: IQ[20], x: 0, y: 0, zoom: 1.0, rot: 0},
    {q: IQ[21] + 6, x: 0, y: -40, zoom: 1.12, rot: 0, curva: 'linear'},
  ], 'f20', 0.6, [f, s, g]);
  return (
    <AbsoluteFill style={{background: '#0E0A08'}}>
      <Palco cam={c} id="f20">
        <Plano p={1} style={{opacity: apaga}}>
          <Peca q={q} ini={f} nome="cachinho" x={230} y={820} w={300} rot={-8} />
          <Marcador q={q} ini={f + 2} texto="fruta" x={230} y={1080} tamanho={62} papel={null} tinta={COR.creme} chave="f20-a" />
          <Peca q={q} ini={s} nome="grao-02" x={540} y={820} w={200} rot={6} />
          <Marcador q={q} ini={s + 2} texto="semente" x={540} y={1080} tamanho={62} papel={null} tinta={COR.creme} chave="f20-b" />
          <Peca q={q} ini={g} nome="torrado" x={850} y={820} w={270} rot={-4} />
          <Marcador q={q} ini={g + 2} texto="grão" x={850} y={1080} tamanho={62} papel={null} tinta={COR.creme} chave="f20-c" />
        </Plano>
      </Palco>
      <Vinheta forca={0.8} />
    </AbsoluteFill>
  );
};

// ===================================================================== 21 · tudo que ficou pelo caminho
export const Cena21: React.FC<C> = ({q}) => {
  const c = cam(q, empurra(21, 1.08, 1.2, 0), 'f21', 0.5);
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={c} id="f21">
        {/* o descarte na mão, em câmera lenta e no escuro */}
        <Plano p={1}><Clipe q={q} ini={IQ[21]} src="v5" de={9.3} vel={0.5} escuro={0.5} /></Plano>
      </Palco>
      <Vinheta forca={0.85} />
    </AbsoluteFill>
  );
};

// ===================================================================== 22 · a serra
export const Cena22: React.FC<C> = ({q}) => {
  const m = fq(S13.m1250.inicio);
  const s = fq(S13.serra.inicio);
  const c = cam(q, empurra(22, 1.0, 1.1, -30), 'f22', 1, [m, s]);
  return (
    <AbsoluteFill style={{background: COR.preto}}>
      <Palco cam={c} id="f22">
        <Plano p={1}><FotoCheia q={q} ini={IQ[22]} dur={IQ[23] - IQ[22]} src="lavoura-1405.jpg" /></Plano>
        <Plano p={1.1}>
          <Recortadas q={q} ini={m} texto="1.250 M" x={540} y={430} tamanho={150} chave="f22-m" />
          <Dymo q={q} ini={s} texto="SERRA DA CANASTRA" x={540} y={640} tamanho={78} rot={-2} />
        </Plano>
      </Palco>
      <Vinheta forca={0.4} />
    </AbsoluteFill>
  );
};

// ===================================================================== 23 · já foi fruta, hoje é Café Canastra
export const Cena23: React.FC<C> = ({q}) => {
  const j = fq(S13.jaFoi.inicio);
  const h = fq(S13.hoje.inicio);
  const k = fq(S13.canastra.inicio);
  const c = cam(q, [
    {q: IQ[23], x: 0, y: 0, zoom: 1.0, rot: 0},
    {q: k, x: 0, y: 0, zoom: 1.04, rot: 0, curva: 'linear'},
    {q: IQ[24] + 6, x: 0, y: -20, zoom: 1.08, rot: 0},
  ], 'f23', 0.8, [j, k]);
  return (
    <AbsoluteFill>
      <Fundo cor={COR.creme} forca={0.5} />
      <Palco cam={c} id="f23">
        <Plano p={0.6}><SombraFolhas q={q} opacidade={0.18} /></Plano>
        <Plano p={1}>
          <Peca q={q} ini={j} nome="cachinho" x={260} y={760} w={330} rot={-10} fora={h} />
          <Marcador q={q} ini={j + 2} texto="já foi fruta" x={300} y={1080} tamanho={70} rot={-4} chave="f23-j" fora={h} dur={fala(S13.jaFoi)} />
          {/* a embalagem real (recorte com laudo) entra no "hoje"; texto longe do logo */}
          <Embalagem q={q} ini={h} sku="classico" x={560} y={900} h={1700} rot={3} />
          <Marcador q={q} ini={h} texto="hoje é" x={250} y={420} tamanho={80} rot={-6} chave="f23-hoje" />
          <Brilho q={q} ini={k + 2} x={900} y={560} r={90} cor={COR.acento} />
          <Brilho q={q} ini={k + 6} x={290} y={1330} r={60} cor={COR.acento} />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};

// ===================================================================== 24 · café da manhã
export const Cena24: React.FC<C> = ({q}) => {
  const a = fq(S14.amanha.inicio);
  const cm = fq(S14.cafeManha.inicio);
  const c = cam(q, empurra(24, 1.0, 1.1, 0), 'f24', 1, [a, cm]);
  return (
    <AbsoluteFill>
      <Fundo cor="#E9DFCB" forca={0.55} />
      <Palco cam={c} id="f24">
        <Plano p={0.6}><SombraFolhas q={q} opacidade={0.2} /></Plano>
        <Plano p={1}>
          <Serifa q={q} ini={a} texto="E amanhã?" x={540} y={470} tamanho={170} cor={COR.preto} rot={-3} />
          <Peca q={q} ini={fq(S14.vai.inicio)} nome="xicara" x={540} y={950} w={640} rot={4} />
          <Marcador q={q} ini={cm} texto="o seu café da manhã" x={540} y={1330} tamanho={60} rot={-3} chave="f24-cm" dur={fala(S14.cafeManha)} />
          <Brilho q={q} ini={cm + 6} x={840} y={760} r={70} cor={COR.acento} />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};

// ===================================================================== 25 · o laço
export const Cena25: React.FC<C> = ({q}) => (
  <AbsoluteFill style={{background: COR.preto}}>
    <Palco cam={cam(q, empurra(25, 1.0, 1.04, 0), 'f25', 1)} id="f25">
      <Plano p={1}><Clipe q={q} ini={IQ[25]} src="v2" de={7.65} vel={0.75} /></Plano>
    </Palco>
    <Vinheta forca={0.45} />
  </AbsoluteFill>
);

export const CENAS = [Cena0, Cena1, Cena2, Cena3, Cena4, Cena5, Cena6, Cena7, Cena8, Cena9, Cena10, Cena11, Cena12,
  Cena13, Cena14, Cena15, Cena16, Cena17, Cena18, Cena19, Cena20, Cena21, Cena22, Cena23, Cena24, Cena25];
