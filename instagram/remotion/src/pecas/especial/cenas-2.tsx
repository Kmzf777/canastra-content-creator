// Peça 07, cenas 6 a 9: prova da xícara → a virada → a fazenda → o fecho com o selo real.

import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {COR} from '../../identidade/tokens';
import {PILHA} from '../../identidade/tipografia';
import {cameraEm, deriva, pulso, somar, tremor, type Chave} from '../../colagem/camera';
import {Brilho, Check, Cruz, Elipse, Seta, Sublinhado, Xis} from '../../colagem/grafismos';
import {Palco, Plano} from '../../colagem/palco';
import {Dymo, Marcador, Recortadas, Serifa} from '../../colagem/tipos';
import {assentar, posterizar, progresso} from '../../colagem/movimento-colagem';
import {Embalagem} from '../../colagem/pecas';
import {Cobertura, Fita, Foco, fq, Fundo, PacoteGenerico, Peca, Rodape, SombraFolhas, Tachinha, Vinheta} from './apoio';
import {S6, S7, S8, S9} from './roteiro';

type C = {q: number};
const cam = (q: number, chaves: Chave[], chave: string, i: number, pulsos: number[] = [], tremores: number[] = []) =>
  somar(cameraEm(q, chaves), deriva(q, chave, i), pulso(q, pulsos), ...tremores.map((t) => tremor(q, t)));

// ===================================================================== 6 · prova 2: a xícara
const XICARAS_X = [180, 360, 540, 720, 900];
const ATRIBUTOS: Array<{t: keyof typeof S6; txt: string}> = [
  {t: 'aroma', txt: 'AROMA'}, {t: 'docura', txt: 'DOÇURA'}, {t: 'acidez', txt: 'ACIDEZ'},
  {t: 'corpo', txt: 'CORPO'}, {t: 'equilibrio', txt: 'EQUILÍBRIO'},
];

/** Régua 0–100 de papel; o marcador vai a 80, 85 e 90 nas palavras. */
const Regua: React.FC<{q: number; ini: number; marcas: Array<{v: number; q: number}>}> = ({q, ini, marcas}) => {
  if (q < ini) return null;
  const x0 = 90;
  const larg = 900;
  const m = 50;
  const util = larg - 2 * m;
  const px = (v: number) => m + (util * v) / 100;
  let v = 0;
  let qAnt = ini;
  for (const k of marcas) {
    if (q >= k.q) v = k.v;
    else {
      const t = progresso(q, Math.max(qAnt, k.q - 10), k.q);
      v = v + (k.v - v) * t;
      break;
    }
    qAnt = k.q;
  }
  const p = assentar(posterizar(q, 3, ini), ini, 'regua');
  return (
    <div style={{position: 'absolute', left: x0, top: 880, width: larg, height: 170, background: '#F7F2E6',
      transform: `translateY(${p.dy}px) rotate(-1deg)`, boxShadow: '0 12px 16px rgba(0,0,0,0.35)'}}>
      <div style={{position: 'absolute', left: m, top: 0, bottom: 0, width: (util * Math.min(v, 80)) / 100, background: 'rgba(20,16,13,0.22)'}} />
      {Array.from({length: 21}, (_, i) => (
        <div key={i} style={{position: 'absolute', left: px(i * 5) - 1.5, top: 0, width: 3, height: i % 2 ? 36 : 64, background: COR.terra}} />
      ))}
      {[0, 20, 40, 60, 80, 100].map((n) => (
        <div key={n} style={{position: 'absolute', left: px(n), top: 92, transform: 'translateX(-50%)', fontFamily: PILHA.dado,
          fontWeight: 500, fontSize: 46, color: COR.terra}}>{n}</div>
      ))}
      <div style={{position: 'absolute', left: px(v) - 10, top: -48, width: 20, height: 266, background: COR.acento}} />
    </div>
  );
};

export const Cena6: React.FC<C> = ({q}) => {
  const ini = fq(S6.passou.inicio);
  const regua = fq(43.4);
  const naRegua = q >= regua;
  const perde = fq(S6.perde.inicio);
  const noventa = fq(S6.noventa.inicio);
  const c = naRegua
    ? cam(q, [
        {q: regua, x: 0, y: 120, zoom: 1.05, rot: 0},
        {q: regua + 6, x: 0, y: 0, zoom: 1.0, rot: 0, curva: 'rapida'},
        {q: fq(S6.oitenta.inicio) + 4, x: -40, y: -10, zoom: 1.06, rot: 0, curva: 'rapida'},
        {q: fq(S6.oitentaECinco.inicio) + 4, x: 20, y: 40, zoom: 1.09, rot: 0.5, curva: 'rapida'},
        {q: noventa + 4, x: 60, y: 120, zoom: 1.12, rot: 0.8, curva: 'rapida'},
        {q: fq(49.46), x: 60, y: 120, zoom: 1.16, rot: 0.8, curva: 'linear'},
      ], 'c6b', 0.9, [fq(S6.oitenta.inicio), fq(S6.oitentaECinco.inicio), noventa, fq(S6.rarissimo.inicio)], [noventa])
    : cam(q, [
        {q: ini, x: 0, y: -60, zoom: 1.03, rot: 0},
        {q: fq(34.0), x: -55, y: 0, zoom: 1.05, rot: -0.6, curva: 'suave'},
        {q: fq(40.4), x: 55, y: 30, zoom: 1.07, rot: 0.6, curva: 'linear'},
        {q: fq(41.5), x: 70, y: 50, zoom: 1.1, rot: 0.6, curva: 'rapida'},
        {q: regua, x: 70, y: 60, zoom: 1.12, rot: 0.6, curva: 'linear'},
      ], 'c6a', 1, [ini, fq(S6.xicara.inicio), fq(S6.cinco.inicio), perde], [perde]);
  const maoT = progresso(q, fq(34.36), fq(37.0));
  return (
    <AbsoluteFill>
      <Fundo cor="#E9DDC6" forca={0.55} />
      <Palco cam={c} id="c6">
        <Plano p={0.6}>
          <SombraFolhas q={q} opacidade={0.18} />
        </Plano>
        {!naRegua && (
          <Plano p={1}>
            <Marcador q={q} ini={ini} texto="Passou?" x={500} y={360} tamanho={150} papel={null} tinta={COR.verde} rot={-5} chave="c6-passou" />
            <Check q={q} ini={ini + 8} cx={820} cy={330} r={70} chave="c6-check" />
            <Dymo q={q} ini={fq(S6.xicara.inicio)} texto="PROVA 2" x={400} y={560} tamanho={100} rot={-2} />
            <Dymo q={q} ini={fq(34.09)} texto="XÍCARA" x={640} y={680} tamanho={100} rot={1} />
            <Recortadas q={q} ini={fq(S6.cinco.inicio)} texto="5" x={900} y={620} tamanho={230} chave="c6-5" />
            {XICARAS_X.map((x, i) => (
              <Peca key={i} q={q} ini={fq(S6.cinco.inicio) + i * 3} nome={i === 2 ? 'tigela-crosta' : 'xicara-prova'} x={x} y={1040} w={172}
                rot={(i - 2) * 4} treme={i === 3 ? fq(41.18) : undefined} />
            ))}
            {ATRIBUTOS.map((a, i) => (
              <Marcador key={a.t} q={q} ini={fq(S6[a.t].inicio)} texto={a.txt} x={XICARAS_X[i]} y={i % 2 ? 1300 : 1220}
                tamanho={50} chave={`c6-a-${a.t}`} rot={(i % 2 ? 4 : -4)} />
            ))}
            <Xis q={q} ini={fq(41.48)} cx={XICARAS_X[3]} cy={1040} r={105} chave="c6-x" espessura={14} />
            <Recortadas q={q} ini={perde} texto="−2" x={XICARAS_X[3]} y={850} tamanho={150} chave="c6-menos2" />
            <Peca q={q} ini={fq(34.36)} nome="mao-colher" x={1150 - 760 * maoT} y={900 + 20 * Math.sin(maoT * 9)} w={560} rot={-8} fora={fq(37.5)} />
          </Plano>
        )}
        {naRegua && (
          <Plano p={1}>
            <Regua q={q} ini={regua} marcas={[
              {v: 80, q: fq(S6.oitenta.inicio) + 2}, {v: 85, q: fq(S6.oitentaECinco.inicio) + 2}, {v: 90, q: noventa + 2},
            ]} />
            <Recortadas q={q} ini={fq(S6.oitenta.inicio)} texto="80" x={136 + 800 * 0.8} y={760} tamanho={120} chave="c6-80" />
            <Recortadas q={q} ini={fq(S6.oitentaECinco.inicio)} texto="85" x={136 + 800 * 0.85 + 60} y={600} tamanho={100} chave="c6-85" />
            <Dymo q={q} ini={fq(S6.excelente.inicio)} texto="EXCELENTE." x={700} y={1180} tamanho={88} fundo={COR.verde} rot={-2} />
            <Recortadas q={q} ini={noventa} texto="90" x={136 + 800 * 0.9 + 40} y={430} tamanho={140} chave="c6-90" />
            <Serifa q={q} ini={fq(S6.rarissimo.inicio)} texto="raríssimo." x={640} y={1360} tamanho={170} cor={COR.acento} rot={-4} />
            <Brilho q={q} ini={noventa + 2} x={960} y={330} r={90} cor={COR.acento} />
            <Brilho q={q} ini={fq(S6.rarissimo.inicio) + 2} x={300} y={1300} r={70} cor={COR.acento} />
            <Brilho q={q} ini={fq(S6.rarissimo.inicio) + 6} x={930} y={1460} r={55} cor={COR.terra} />
            <Rodape q={q} ini={fq(S6.oitenta.inicio) + 6} x={540} y={1650} texto="*escala de 0 a 100 do protocolo de prova SCA" tamanho={30} cor={COR.terra} />
          </Plano>
        )}
        <Plano p={2.4}>
          <Peca q={q} ini={ini} nome="folha-1" x={80} y={1700} w={540} rot={20} sombra={false} />
          <Peca q={q} ini={ini} nome="folha-6" x={1010} y={240} w={500} rot={-30} sombra={false} />
        </Plano>
      </Palco>
      <Cobertura q={q} ini={fq(S7.aqui.inicio) - 7} cor={COR.preto} chave="c6-cob" />
    </AbsoluteFill>
  );
};

// ===================================================================== 7 · a virada
export const Cena7: React.FC<C> = ({q}) => {
  const ini = fq(S7.aqui.inicio);
  const b = fq(53.2); // painel das polaroids
  const cq = fq(57.4); // a frase-tese
  const d = fq(60.9); // no pé
  const fase = q < b ? 'a' : q < cq ? 'b' : q < d ? 'c' : 'd';
  const ruim = fq(60.48);
  const pe = fq(62.31);
  const chaves: Record<string, Chave[]> = {
    a: [{q: ini, x: 0, y: 0, zoom: 1.12, rot: 0}, {q: b, x: 0, y: -40, zoom: 1.0, rot: -0.4, curva: 'linear'}],
    b: [{q: b, x: -60, y: -120, zoom: 1.1, rot: 0}, {q: fq(55.6), x: -40, y: -60, zoom: 1.12, rot: -0.5, curva: 'suave'},
        {q: fq(56.2), x: 60, y: 160, zoom: 1.12, rot: 0.5, curva: 'rapida'}, {q: cq, x: 50, y: 180, zoom: 1.15, rot: 0.5, curva: 'linear'}],
    c: [{q: cq, x: 0, y: 0, zoom: 1.0, rot: 0}, {q: d, x: 0, y: -20, zoom: 1.08, rot: -0.4, curva: 'linear'}],
    d: [{q: d, x: 0, y: -60, zoom: 1.0, rot: 0}, {q: pe, x: 0, y: -30, zoom: 1.06, rot: 0, curva: 'linear'},
        {q: fq(63.12), x: 0, y: 260, zoom: 1.2, rot: 0, curva: 'rapida'}],
  };
  const c = cam(q, chaves[fase], `c7${fase}`, 1, [fq(S7.nenhum.inicio), fq(52.16), fq(S7.naoSalva.inicio), ruim, pe], [ruim, pe]);
  return (
    <AbsoluteFill>
      {fase === 'a' && <Fundo cor={COR.preto} forca={0.3} />}
      {fase === 'b' && <Fundo cor="#E9DDC6" forca={0.6} />}
      {fase === 'c' && <Fundo cor={q >= ruim ? COR.terra : COR.creme} forca={0.45} />}
      {fase === 'd' && <Fundo cor={COR.verde} forca={0.4} />}
      <Palco cam={c} id="c7">
        {fase === 'a' && (
          <>
            <Plano p={0.6}><SombraFolhas q={q} opacidade={0.5} /></Plano>
            <Plano p={1}>
              <Peca q={q} ini={ini + 2} nome="grao-preto" x={190} y={430} w={170} rot={-20} />
              <Peca q={q} ini={ini + 8} nome="grao-ardido" x={900} y={450} w={160} rot={15} />
              <Peca q={q} ini={ini + 14} nome="cereja-seca" x={170} y={1460} w={190} rot={10} />
              <Peca q={q} ini={ini + 20} nome="grao-fungo" x={910} y={1480} w={170} rot={-12} />
              <Serifa q={q} ini={fq(S7.ninguem.inicio)} texto="quase ninguém" x={540} y={620} tamanho={130} cor={COR.creme} rot={-3} />
              <Serifa q={q} ini={fq(50.6)} texto="conta:" x={700} y={760} tamanho={130} cor={COR.creme} rot={-3} />
              <Dymo q={q} ini={fq(S7.nenhum.inicio)} texto="NENHUM" x={360} y={1000} tamanho={110} fundo={COR.acento} rot={-2} />
              <Serifa q={q} ini={fq(51.61)} texto="desses defeitos" x={620} y={1140} tamanho={110} cor={COR.creme} rot={2} />
              <Dymo q={q} ini={fq(52.16)} texto="NASCE NA TORRA." x={540} y={1300} tamanho={92} fundo={COR.creme} tinta={COR.preto} rot={-1} />
              <Peca q={q} ini={fq(52.4)} nome="torrado" x={860} y={860} w={230} rot={10} />
              <Xis q={q} ini={fq(52.81)} cx={860} cy={860} r={120} chave="c7-x" espessura={16} />
            </Plano>
            <Plano p={2.4}>
              <Peca q={q} ini={ini} nome="grao-ardido" x={120} y={300} w={300} rot={-25} sombra={false} />
              <Peca q={q} ini={ini} nome="grao-preto-partido" x={980} y={1680} w={380} rot={20} sombra={false} />
            </Plano>
          </>
        )}
        {fase === 'b' && (
          <>
            <Plano p={0.6}><SombraFolhas q={q} opacidade={0.25} /></Plano>
            <Plano p={1}>
              <Peca q={q} ini={b} nome="frutos-no-chao" x={340} y={700} w={470} rot={-6} />
              <Tachinha q={q} ini={b + 3} x={340} y={520} cor="preta" />
              <Peca q={q} ini={fq(53.35)} nome="grao-preto" x={820} y={560} w={170} rot={10} />
              <Peca q={q} ini={fq(53.68)} nome="grao-ardido" x={880} y={790} w={170} rot={-8} />
              <Seta q={q} ini={fq(54.3)} de={[760, 600]} para={[560, 660]} curva={0.25} cor={COR.acento} chave="c7-s1" />
              <Seta q={q} ini={fq(54.5)} de={[800, 820]} para={[580, 760]} curva={-0.2} cor={COR.acento} chave="c7-s2" />
              <Marcador q={q} ini={fq(S7.fermentou.inicio)} texto="FERMENTOU DEMAIS." x={500} y={980} tamanho={56} chave="c7-ferm" />
              <Peca q={q} ini={fq(S7.verde.inicio)} nome="foto-cereja-verde" x={720} y={1330} w={480} rot={4} semBoil />
              <Tachinha q={q} ini={fq(S7.verde.inicio) + 3} x={720} y={1100} cor="verde" />
              <Peca q={q} ini={fq(55.9)} nome="grao-imaturo" x={260} y={1300} w={180} rot={-6} />
              <Seta q={q} ini={fq(56.1)} de={[330, 1260]} para={[480, 1300]} curva={0.25} cor={COR.acento} chave="c7-s3" />
              <Marcador q={q} ini={fq(S7.colheita.inicio)} texto="COLHEITA ANTES DA HORA." x={540} y={1590} tamanho={48} chave="c7-colh" />
            </Plano>
            <Plano p={2.4}>
              <Peca q={q} ini={b} nome="folha-3" x={90} y={1750} w={520} rot={30} sombra={false} />
            </Plano>
          </>
        )}
        {fase === 'c' && (
          <Plano p={1}>
            <Serifa q={q} ini={cq} texto="A torra pode estragar" x={540} y={640} tamanho={120} cor={q >= ruim ? COR.creme : COR.preto} rot={-2} />
            <Serifa q={q} ini={fq(58.62)} texto="um café bom…" x={600} y={790} tamanho={120} cor={q >= ruim ? COR.creme : COR.preto} rot={-2} />
            <Peca q={q} ini={fq(58.62)} nome="torrado" x={270} y={930} w={330} rot={-10} />
            <Check q={q} ini={fq(59.04)} cx={400} cy={850} r={60} chave="c7-ok" />
            <Peca q={q} ini={fq(59.76)} nome="grao-preto-partido" x={760} y={860} w={200} rot={8} />
            <Peca q={q} ini={fq(59.9)} nome="grao-ardido" x={900} y={920} w={140} rot={-12} />
            <Xis q={q} ini={fq(60.48)} cx={820} cy={880} r={115} chave="c7-ruim" espessura={16} />
            <Dymo q={q} ini={fq(S7.naoSalva.inicio)} texto="MAS NÃO SALVA" x={560} y={1090} tamanho={100} rot={-2} />
            <Dymo q={q} ini={fq(60.06)} texto="UM CAFÉ RUIM." x={620} y={1225} tamanho={100} fundo={COR.acento} rot={2} />
            <Sublinhado q={q} ini={ruim + 2} x1={420} x2={840} y={1300} cor={COR.creme} chave="c7-sub" />
            <Brilho q={q} ini={ruim + 1} x={900} y={1060} r={70} cor={COR.creme} />
          </Plano>
        )}
        {fase === 'd' && (
          <>
            <Plano p={0.7}>
              <Peca q={q} ini={d} nome="foto-cafeeiro" x={540} y={1200} w={760} rot={-2} semBoil />
            </Plano>
            <Plano p={1}>
              <Serifa q={q} ini={d} texto="especial se decide" x={540} y={420} tamanho={120} cor={COR.creme} rot={-3} />
              <Recortadas q={q} ini={fq(62.16)} texto="NO PÉ." x={540} y={620} tamanho={190} chave="c7-pe" />
              <Seta q={q} ini={pe + 6} de={[760, 720]} para={[620, 980]} curva={-0.3} cor={COR.creme} chave="c7-s4" />
            </Plano>
          </>
        )}
      </Palco>
      {fase === 'a' && <Foco q={q} ini={ini} />}
      {fase === 'a' && q < b && q >= b - 7 && <Cobertura q={q} ini={b - 7} cor="#E9DDC6" chave="c7-cob" />}
    </AbsoluteFill>
  );
};

// ===================================================================== 8 · a fazenda (mural)
export const Cena8: React.FC<C> = ({q}) => {
  const ini = fq(S8.porIsso.inicio);
  const c = cam(q, [
    {q: ini, x: -140, y: -460, zoom: 1.06, rot: -0.6},
    {q: fq(65.8), x: 200, y: -420, zoom: 1.06, rot: 0.4, curva: 'suave'},
    {q: fq(66.5), x: 0, y: 40, zoom: 1.02, rot: 0, curva: 'rapida'},
    {q: fq(68.9), x: 0, y: 120, zoom: 1.06, rot: 0.3, curva: 'linear'},
    {q: fq(69.6), x: 40, y: 620, zoom: 1.04, rot: 0, curva: 'rapida'},
    {q: fq(71.67), x: 90, y: 760, zoom: 1.1, rot: 0.6, curva: 'linear'},
  ], 'c8', 1, [fq(S8.planta.inicio), fq(S8.colhe.inicio), fq(S8.seleciona.inicio), fq(S8.m1250.inicio), fq(S8.doce.inicio)]);
  return (
    <AbsoluteFill>
      <Fundo cor="#B9874F" textura="nenhuma" />
      <Palco cam={c} id="c8">
        <Plano p={0.85}>
          <Img src={staticFile('colagem/cortica-mural.png')} style={{position: 'absolute', left: -270, top: -700, width: 1620}} />
        </Plano>
        <Plano p={1}>
          {/* decoração do mural: o que a câmera vê antes da primeira palavra-colagem */}
          <Peca q={q} ini={ini} nome="foto-fileiras" x={860} y={-60} w={460} rot={6} semBoil />
          <Tachinha q={q} ini={ini + 2} x={860} y={-230} cor="verde" />
          <Peca q={q} ini={ini + 4} nome="etiqueta-barbante" x={170} y={-80} w={250} rot={-12} />
          <Marcador q={q} ini={ini + 6} texto="DESDE 1985" x={180} y={-60} tamanho={40} papel={null} tinta={COR.terra} rot={-12} chave="c8-1985" />
          <Fita q={q} ini={ini + 3} x={560} y={-150} w={240} rot={-8} chave="c8-f0" />
          {/* planta → colhe → seleciona (região de cima) */}
          <Peca q={q} ini={ini} nome="foto-cafeeiro" x={330} y={330} w={360} rot={-4} semBoil />
          <Tachinha q={q} ini={ini + 3} x={330} y={110} cor="terra" />
          <Marcador q={q} ini={fq(S8.planta.inicio)} texto="PLANTA" x={330} y={600} tamanho={64} chave="c8-pl" />
          <Peca q={q} ini={fq(64.5)} nome="foto-maos-cafeeiro" x={760} y={380} w={330} rot={5} semBoil />
          <Tachinha q={q} ini={fq(64.5) + 3} x={760} y={150} cor="creme" />
          <Marcador q={q} ini={fq(S8.colhe.inicio)} texto="COLHE" x={760} y={650} tamanho={64} chave="c8-co" />
          <Seta q={q} ini={fq(S8.colhe.inicio)} de={[450, 560]} para={[640, 610]} curva={-0.3} cor={COR.acento} chave="c8-s1" />
          <Peca q={q} ini={fq(65.4)} nome="peneira" x={1010} y={450} w={300} rot={-6} />
          <Marcador q={q} ini={fq(S8.seleciona.inicio)} texto="SELECIONA" x={975} y={700} tamanho={58} chave="c8-se" />
          <Seta q={q} ini={fq(S8.seleciona.inicio)} de={[860, 600]} para={[930, 660]} curva={-0.3} cor={COR.acento} chave="c8-s2" />
          {/* altitude (região do meio) */}
          <Peca q={q} ini={fq(66.2)} nome="foto-lavoura-ceu" x={540} y={1230} w={900} rot={-2} semBoil />
          <Fita q={q} ini={fq(66.3)} x={150} y={930} w={220} rot={-30} chave="c8-f1" />
          <Fita q={q} ini={fq(66.35)} x={930} y={930} w={220} rot={28} chave="c8-f2" />
          <Recortadas q={q} ini={fq(S8.m1250.inicio)} texto="1.250 m" x={540} y={980} tamanho={140} chave="c8-1250" />
          <Dymo q={q} ini={fq(S8.serra.inicio)} texto="SERRA DA CANASTRA" x={540} y={1560} tamanho={76} rot={-1} />
          <Rodape q={q} ini={fq(68.5)} x={540} y={1650} texto="Medeiros-MG" tamanho={30} cor={COR.creme} />
          {/* maturação (região de baixo) */}
          <Marcador q={q} ini={fq(S8.devagar.inicio)} texto="AMADURECE DEVAGAR" x={540} y={1790} tamanho={60} chave="c8-dev" />
          <Peca q={q} ini={fq(69.5)} nome="cereja-verde-1" x={300} y={2020} w={200} />
          <Peca q={q} ini={fq(69.95)} nome="cereja-amarela-2" x={540} y={2020} w={200} />
          <Peca q={q} ini={fq(70.4)} nome="cereja-vermelha-3" x={780} y={2020} w={210} />
          <Seta q={q} ini={fq(69.8)} de={[370, 2140]} para={[470, 2140]} curva={0.3} cor={COR.preto} espessura={7} chave="c8-m1" />
          <Seta q={q} ini={fq(70.25)} de={[610, 2140]} para={[710, 2140]} curva={0.3} cor={COR.preto} espessura={7} chave="c8-m2" />
          <Marcador q={q} ini={fq(S8.doce.inicio) - 3} texto="+ DOCE" x={800} y={2170} tamanho={110} rot={-6} chave="c8-doce" />
          <Brilho q={q} ini={fq(S8.doce.inicio) + 2} x={960} y={2150} r={70} cor={COR.creme} />
        </Plano>
        <Plano p={1.3}>
          <SombraFolhas q={q} opacidade={0.38} vel={0.5} />
        </Plano>
        <Plano p={2.4}>
          <Peca q={q} ini={ini} nome="folha-1" x={-60} y={-200} w={620} rot={40} sombra={false} />
          <Peca q={q} ini={ini} nome="folha-3" x={1160} y={1350} w={560} rot={-20} sombra={false} />
          <Peca q={q} ini={ini} nome="folha-6" x={-40} y={1500} w={600} rot={60} sombra={false} />
        </Plano>
      </Palco>
      <Vinheta forca={0.35} />
    </AbsoluteFill>
  );
};

// ===================================================================== 9 · o fecho
// O selo "SPECIALTY / ESPECIAL / SCA 80+" do Clássico, conferido no pixel do recorte
// com laudo: centro em (0,49 · 0,654) da imagem em pé (2304x4096).
const SELO = {fx: 0.49, fy: 0.654};

export const Cena9: React.FC<C> = ({q}) => {
  const ini = fq(S9.olha.inicio);
  const nosso = fq(S9.nosso.inicio);
  const salva = fq(S9.salva.inicio);
  const PX = 540;
  const PY = 900;
  const PH = 1000;
  const seloX = PX - (PH * 0.5625) / 2 + SELO.fx * PH * 0.5625;
  const seloY = PY - PH / 2 + SELO.fy * PH;
  const fecho = q >= salva;
  const c = fecho
    ? cam(q, [{q: salva, x: 0, y: -40, zoom: 1.0, rot: 0}, {q: fq(79), x: 0, y: -20, zoom: 1.05, rot: 0, curva: 'linear'}], 'c9b', 0.7, [salva])
    : cam(q, [
        {q: ini, x: 0, y: 0, zoom: 1.0, rot: 0},
        {q: nosso, x: 0, y: 30, zoom: 1.06, rot: -0.4, curva: 'linear'},
        {q: nosso + 18, x: seloX - 540, y: seloY - 960, zoom: 2.05, rot: 0, curva: 'suave'},
        {q: salva, x: seloX - 540, y: seloY - 960, zoom: 2.12, rot: 0.3, curva: 'linear'},
      ], 'c9a', 0.7, [fq(S9.procura.inicio), fq(S9.ninguem.inicio)]);
  const lupaT = progresso(q, fq(72.8), fq(73.6));
  return (
    <AbsoluteFill>
      <Fundo cor={COR.creme} forca={0.45} />
      <Palco cam={c} id="c9">
        <Plano p={0.6}><SombraFolhas q={q} opacidade={0.16} /></Plano>
        {!fecho && (
          <Plano p={1}>
            {q < nosso
              ? <PacoteGenerico q={q} ini={ini} x={PX} y={PY} h={PH * 0.66} rot={0} />
              : <Embalagem q={q} ini={nosso} sku="classico" x={PX} y={PY} h={PH} rot={0} />}
            <Dymo q={q} ini={fq(S9.procura.inicio)} texto="PROCURA A NOTA." x={540} y={1440} tamanho={96} rot={-2} fora={nosso} />
            <Peca q={q} ini={fq(72.8)} nome="lupa" x={300 + 460 * lupaT} y={700 + 180 * Math.sin(lupaT * 3)} w={380} rot={-20} fora={fq(73.9)} />
            <Serifa q={q} ini={fq(S9.seNao.inicio)} texto="se não tem nota," x={540} y={380} tamanho={120} cor={COR.preto} rot={-3} fora={nosso} />
            <Dymo q={q} ini={fq(S9.ninguem.inicio)} texto="NINGUÉM PROVOU" x={480} y={1430} tamanho={92} fundo={COR.acento} rot={-2} fora={nosso} />
            <Dymo q={q} ini={fq(75.36)} texto="POR VOCÊ." x={700} y={1560} tamanho={92} rot={2} fora={nosso} />
            <Elipse q={q} ini={nosso + 16} cx={seloX} cy={seloY} rx={150} ry={95} cor={COR.creme} chave="c9-selo" espessura={6} />
            <Brilho q={q} ini={nosso + 20} x={seloX + 150} y={seloY - 90} r={36} cor={COR.creme} />
            <Brilho q={q} ini={nosso + 24} x={seloX - 160} y={seloY + 70} r={26} cor={COR.creme} />
            <Marcador q={q} ini={nosso + 14} texto="O NOSSO TÁ AQUI." x={seloX} y={seloY - 160} tamanho={34} chave="c9-nosso" />
          </Plano>
        )}
        {fecho && (
          <Plano p={1}>
            <Img src={staticFile('fonte/logo-preta.png')} style={{position: 'absolute', left: 540 - 300, top: 230, width: 600}} />
            <Embalagem q={q} ini={salva} sku="classico" x={260} y={960} h={900} rot={-5} />
            <Embalagem q={q} ini={salva + 4} sku="suave" x={540} y={930} h={940} rot={0} />
            <Embalagem q={q} ini={salva + 8} sku="canela" x={820} y={960} h={900} rot={5} />
            <Peca q={q} ini={salva + 6} nome="post-it" x={860} y={1420} w={300} rot={6} />
            <Marcador q={q} ini={salva + 8} texto="SALVA ✓" x={860} y={1420} tamanho={58} papel={null} tinta={COR.preto} rot={6} chave="c9-salva" />
            <Seta q={q} ini={salva + 14} de={[950, 1520]} para={[1010, 1680]} curva={0.3} cor={COR.acento} chave="c9-s" />
            <Rodape q={q} ini={salva + 18} x={360} y={1340} texto="loja.cafecanastra.com" tamanho={32} cor={COR.terra} />
            <Cruz q={q} ini={salva + 3} x={120} y={520} cor={COR.acento} chave="c9-c1" s={50} />
            <Brilho q={q} ini={salva + 10} x={960} y={420} r={60} cor={COR.acento} />
          </Plano>
        )}
        <Plano p={2.4}>
          <Peca q={q} ini={ini} nome="folha-5" x={60} y={1680} w={520} rot={25} sombra={false} />
          <Peca q={q} ini={ini} nome="folha-2" x={1030} y={220} w={460} rot={-35} sombra={false} />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};
