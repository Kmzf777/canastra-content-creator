// Peça 07, cenas 1 a 5: tensão → calma → o mito → prova do grão → o contraste.
// Cada cena = um Palco (câmera 2.5D) com planos de profundidade; o primeiro plano
// (p≈2,4) passa borrado perto da lente. Tempos: roteiro.ts (medidos na narração).

import React from 'react';
import {AbsoluteFill} from 'remotion';
import {COR} from '../../identidade/tokens';
import {cameraEm, deriva, pulso, somar, tremor, type Chave} from '../../colagem/camera';
import {Brilho, Cruz, Elipse, Seta, Sublinhado, Xis} from '../../colagem/grafismos';
import {Palco, Plano} from '../../colagem/palco';
import {Dymo, Marcador, Recortadas, Serifa} from '../../colagem/tipos';
import {progresso} from '../../colagem/movimento-colagem';
import {semente} from '../../colagem/semente';
import {Cobertura, Divisoria, fq, Fundo, PacoteGenerico, Peca, Rodape, SombraFolhas, Tachinha, Troca, Vinheta} from './apoio';
import {S1, S2, S3, S4, S5} from './roteiro';

type C = {q: number};
const cam = (q: number, chaves: Chave[], chave: string, i: number, pulsos: number[] = [], tremores: number[] = []) =>
  somar(cameraEm(q, chaves), deriva(q, chave, i), pulso(q, pulsos), ...tremores.map((t) => tremor(q, t)));

// ===================================================================== 1 · tensão
export const Cena1: React.FC<C> = ({q}) => {
  const lei = fq(S1.lei.inicio);
  const lei2 = fq(5.12);
  const c = cam(q, [
    {q: 0, x: 0, y: 30, zoom: 1.0, rot: 0},
    {q: fq(4.6), x: 0, y: -10, zoom: 1.12, rot: -0.6, curva: 'linear'},
    {q: fq(5.76), x: 0, y: -10, zoom: 1.16, rot: -0.6},
  ], 'c1', 1.5, [fq(0.6), fq(S1.casca.inicio), fq(S1.pau.inicio), lei, lei2], [lei, lei2]);
  const trocas = [
    {nome: 'casca', ini: fq(2.2), w: 300},
    {nome: 'graveto', ini: fq(2.47), w: 430, rot: 20},
    {nome: 'casca', ini: fq(2.74), w: 320, rot: -10},
    {nome: 'graveto', ini: fq(3.02), w: 440, rot: -15},
    {nome: 'casca', ini: fq(3.25), w: 300, rot: 8},
    {nome: 'graveto', ini: fq(3.49), w: 450, rot: 24},
  ];
  return (
    <AbsoluteFill>
      <Fundo cor={COR.preto} forca={0.3} />
      <Palco cam={c} id="c1">
        <Plano p={0.5}>
          <Peca q={q} ini={0} nome="torrado" x={900} y={300} w={360} rot={20} opacidade={0.35} sombra={false} />
          <Peca q={q} ini={0} nome="torrado" x={150} y={1650} w={420} rot={-30} opacidade={0.3} sombra={false} />
        </Plano>
        <Plano p={1}>
          <Peca q={q} ini={-8} nome="xicara" x={540} y={900} w={760} />
          {/* "que você compra": o café de qualquer pacote (silhueta sem marca) e a lupa que vai investigar */}
          <PacoteGenerico q={q} ini={fq(S1.doCafe.inicio) + fq(0.5)} x={230} y={1330} h={470} rot={-9} fora={fq(2.2)} />
          <Peca q={q} ini={fq(1.62)} nome="lupa" x={900 - 330 * progresso(q, fq(1.62), fq(2.15))} y={1300 - 380 * progresso(q, fq(1.62), fq(2.15))} w={420} rot={-25} fora={fq(2.2)} />
          <Troca q={q} itens={trocas} x={540} y={905} />
          {q >= fq(3.85) && <Peca q={q} ini={fq(3.85)} nome="casca" x={430} y={870} w={250} rot={-12} />}
          <Recortadas q={q} ini={fq(S1.ate1.inicio)} texto="ATÉ 1%" x={540} y={340} tamanho={140} chave="c1-ate" />
          <Elipse q={q} ini={fq(1.0)} cx={540} cy={340} rx={400} ry={140} cor={COR.acento} chave="c1-el" espessura={10} />
          <Marcador q={q} ini={fq(S1.casca.inicio)} texto="CASCA" x={240} y={1260} rot={-7} tamanho={92} chave="c1-casca" />
          <Seta q={q} ini={fq(S1.casca.inicio) + 5} de={[300, 1180]} para={[450, 1010]} cor={COR.creme} chave="c1-s1" />
          <Marcador q={q} ini={fq(S1.pau.inicio)} texto="PAU" x={850} y={1270} rot={6} tamanho={96} chave="c1-pau" />
          <Seta q={q} ini={fq(S1.pau.inicio) + 5} de={[800, 1190]} para={[640, 1020]} curva={-0.25} cor={COR.creme} chave="c1-s2" />
          <Dymo q={q} ini={lei} texto="DENTRO DA" x={470} y={1440} tamanho={104} rot={-2} />
          <Dymo q={q} ini={lei2} texto="LEI." x={770} y={1580} tamanho={120} fundo={COR.acento} rot={3} />
          <Sublinhado q={q} ini={lei2 + 6} x1={660} x2={900} y={1665} cor={COR.creme} chave="c1-sub" />
          <Rodape q={q} ini={lei2 + 4} x={540} y={1720} texto="*IN MAPA 16/2010 · até 1% de cascas e paus" tamanho={30} />
        </Plano>
        <Plano p={2.4}>
          <Peca q={q} ini={0} nome="grao-preto" x={110} y={420} w={300} rot={30} sombra={false} />
          <Peca q={q} ini={0} nome="folha-2" x={1000} y={1640} w={520} rot={-35} sombra={false} />
        </Plano>
      </Palco>
      <Vinheta forca={0.7} />
      <Cobertura q={q} ini={fq(S2.calma.inicio) - 7} cor={COR.creme} chave="c1-cob" />
    </AbsoluteFill>
  );
};

// ===================================================================== 2 · calma
export const Cena2: React.FC<C> = ({q}) => {
  const ini = fq(S2.calma.inicio);
  const c = cam(q, [
    {q: ini, x: 0, y: 0, zoom: 1.1, rot: 0},
    {q: ini + 16, x: 0, y: 0, zoom: 1.0, rot: 0, curva: 'rapida'},
    {q: fq(10.88), x: -50, y: -20, zoom: 1.04, rot: 0.4, curva: 'linear'},
  ], 'c2', 1, [fq(S2.fim.inicio), fq(S2.seuEspecial.inicio)]);
  return (
    <AbsoluteFill>
      <Fundo cor={COR.creme} forca={0.45} />
      <Palco cam={c} id="c2">
        <Plano p={0.6}>
          <SombraFolhas q={q} opacidade={0.2} />
        </Plano>
        <Plano p={1}>
          <Marcador q={q} ini={ini} texto="Calma!" x={540} y={640} tamanho={230} papel={null} tinta={COR.preto} rot={-6} chave="c2-calma" />
          <Brilho q={q} ini={ini + 3} x={880} y={500} r={80} cor={COR.acento} />
          <Brilho q={q} ini={ini + 8} x={210} y={770} r={50} cor={COR.acento} />
          <Cruz q={q} ini={ini + 5} x={170} y={470} cor={COR.terra} chave="c2-c1" />
          <Cruz q={q} ini={ini + 9} x={920} y={800} s={44} cor={COR.terra} chave="c2-c2" />
          <Peca q={q} ini={fq(6.86)} nome="xicara" x={290} y={1110} w={400} rot={-5} />
          <PacoteGenerico q={q} ini={fq(S2.fim.inicio)} x={730} y={1090} h={600} rot={4} />
          <Tachinha q={q} ini={fq(S2.fim.inicio) + 4} x={730} y={810} cor="terra" />
          <Marcador q={q} ini={fq(9.0)} texto="?" x={915} y={900} tamanho={150} rot={8} chave="c2-q" />
          <Dymo q={q} ini={fq(S2.seuEspecial.inicio)} texto="SE O SEU É" x={420} y={1420} tamanho={96} rot={-2} />
          <Serifa q={q} ini={fq(10.02)} texto="especial?" x={650} y={1575} tamanho={175} cor={COR.acento} rot={-3} />
          <Seta q={q} ini={fq(10.2)} de={[540, 1350]} para={[660, 1260]} curva={0.3} cor={COR.preto} chave="c2-s" />
        </Plano>
        <Plano p={2.4}>
          <Peca q={q} ini={ini} nome="folha-2" x={120} y={1700} w={540} rot={30} sombra={false} />
          <Peca q={q} ini={ini} nome="folha-5" x={990} y={260} w={480} rot={-40} sombra={false} />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};

// ===================================================================== 3 · o mito
export const Cena3: React.FC<C> = ({q}) => {
  const ini = fq(S3.especial.inicio);
  const duas = fq(S3.duas.inicio);
  const escuro = q >= duas;
  const c = cam(q, [
    {q: ini, x: 0, y: 0, zoom: 1.0, rot: 0},
    {q: fq(14.8), x: 0, y: -30, zoom: 1.07, rot: -0.5, curva: 'linear'},
  ], 'c3', 1, [ini, fq(S3.nomeBonito.inicio), fq(S3.prova.inicio), duas], [duas]);
  return (
    <AbsoluteFill>
      <Fundo cor={escuro ? COR.terra : COR.creme} forca={0.45} />
      <Palco cam={c} id="c3">
        <Plano p={1}>
          <Serifa q={q} ini={ini} texto="especial" x={540} y={480} tamanho={230} cor={escuro ? COR.creme : COR.preto} rot={-4} />
          <Serifa q={q} ini={fq(S3.nomeBonito.inicio)} texto="nome bonito" x={540} y={830} tamanho={150} cor={COR.acento} rot={2} />
          <PacoteGenerico q={q} ini={fq(S3.nomeBonito.inicio)} x={770} y={1260} h={430} rot={6} fora={fq(S3.prova.inicio) - 2} />
          <Marcador q={q} ini={fq(S3.nomeBonito.inicio) + 3} texto="premium" x={650} y={1140} tamanho={46} rot={-9} chave="c3-t1" fora={fq(S3.prova.inicio) - 2} />
          <Marcador q={q} ini={fq(S3.nomeBonito.inicio) + 6} texto="nobre" x={900} y={1230} tamanho={46} rot={7} chave="c3-t2" fora={fq(S3.prova.inicio) - 2} />
          <Xis q={q} ini={fq(S3.noPacote.inicio)} cx={540} cy={845} r={185} chave="c3-x" cor={escuro ? COR.creme : COR.preto} espessura={18} />
          <Dymo q={q} ini={fq(S3.prova.inicio)} texto="É PROVA." x={540} y={1130} tamanho={130} rot={-2} />
          <Recortadas q={q} ini={duas} texto="2" x={540} y={1420} tamanho={380} chave="c3-dois" />
          <Brilho q={q} ini={duas + 2} x={780} y={1290} r={90} cor={COR.acento} />
          <Brilho q={q} ini={duas + 5} x={320} y={1540} r={60} cor={COR.creme} />
          <Cruz q={q} ini={duas + 3} x={250} y={1250} cor={COR.creme} chave="c3-c" />
        </Plano>
        <Plano p={2.4}>
          <Peca q={q} ini={ini} nome="grao-imaturo" x={980} y={1660} w={320} rot={20} sombra={false} />
          <Peca q={q} ini={ini} nome="grao-preto" x={90} y={1180} w={260} rot={-25} sombra={false} />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};

// ===================================================================== 4 · prova 1: grão cru
const DEFEITOS: Array<{nome: string; rot: string; x: number; y: number; w: number; giro: number; t: keyof typeof S4}> = [
  {nome: 'grao-preto', rot: 'PRETO', x: 300, y: 820, w: 190, giro: -10, t: 'preto'},
  {nome: 'grao-ardido', rot: 'ARDIDO', x: 770, y: 860, w: 190, giro: 12, t: 'ardido'},
  {nome: 'cereja-seca', rot: 'CEREJA SECA', x: 330, y: 1110, w: 210, giro: 6, t: 'cereja'},
  {nome: 'grao-fungo', rot: 'FUNGO', x: 770, y: 1150, w: 190, giro: -8, t: 'fungo'},
  {nome: 'pedra', rot: 'PEDRA', x: 310, y: 1380, w: 220, giro: 0, t: 'pedra'},
  {nome: 'graveto', rot: 'PAU', x: 760, y: 1390, w: 330, giro: 22, t: 'pau'},
];

export const Cena4: React.FC<C> = ({q}) => {
  const ini = fq(14.8);
  const foco = DEFEITOS.map((d) => ({q: fq(S4[d.t].inicio) + 3, x: (d.x - 540) * 0.45, y: (d.y - 960) * 0.45, zoom: 1.13, rot: 0, curva: 'rapida' as const}));
  const acabou = fq(S4.acabou.inicio);
  const c = cam(q, [
    {q: ini, x: 0, y: -40, zoom: 1.0, rot: 0},
    {q: fq(17.8), x: 0, y: 0, zoom: 1.04, rot: 0, curva: 'linear'},
    {q: fq(18.5), x: -70, y: -60, zoom: 1.08, rot: -0.5},
    {q: fq(19.3), x: 60, y: 60, zoom: 1.08, rot: 0.5},
    ...foco,
    {q: fq(22.5), x: -110, y: -70, zoom: 1.15, rot: 0},
    {q: acabou + 3, x: 0, y: 0, zoom: 1.02, rot: 0, curva: 'rapida'},
    {q: fq(25.54), x: 0, y: -20, zoom: 1.06, rot: 0, curva: 'linear'},
  ], 'c4', 0.9, [fq(S4.graoCru.inicio), fq(S4.g350.inicio), acabou, fq(S4.naoEspecial.inicio)], [acabou]);
  const lupaT = progresso(q, fq(17.9), fq(19.3));
  const pincaT = progresso(q, fq(22.5), fq(23.2));
  return (
    <AbsoluteFill>
      <Fundo cor={COR.terra} forca={0.35} />
      <Palco cam={c} id="c4">
        <Plano p={0.55}>
          <SombraFolhas q={q} opacidade={0.25} />
        </Plano>
        <Plano p={1}>
          <Peca q={q} ini={ini} nome="bandeja" x={540} y={1010} w={860} />
          <Peca q={q} ini={fq(S4.classificador.inicio)} nome="peneira-classificacao" x={970} y={1640} w={340} rot={-12} fora={fq(S4.acabou.inicio)} />
          {DEFEITOS.map((d) => {
            const t = fq(S4[d.t].inicio);
            const pinçado = d.nome === 'grao-preto' ? fq(23.25) : undefined;
            return (
              <React.Fragment key={d.nome}>
                <Peca q={q} ini={t} nome={d.nome} x={d.x} y={d.y} w={d.w} rot={d.giro} fora={pinçado} />
                <Elipse q={q} ini={t + 4} cx={d.x} cy={d.y} rx={d.w * 0.68} ry={d.w * 0.78} cor={COR.creme} chave={`c4-e-${d.nome}`} espessura={7} fora={acabou} />
                <Marcador q={q} ini={t + 1} texto={d.rot} x={d.x} y={d.y - d.w * 0.95} tamanho={58} chave={`c4-m-${d.nome}`} fora={acabou} />
              </React.Fragment>
            );
          })}
          <Peca q={q} ini={fq(17.9)} nome="lupa" x={260 + 560 * lupaT} y={760 + 480 * lupaT} w={420} rot={-20} fora={fq(19.6)} />
          <Peca q={q} ini={fq(22.5)} nome="pinca" x={1000 - 690 * pincaT} y={560 + 220 * pincaT} w={520} rot={-40} fora={fq(23.6)} />
          <Dymo q={q} ini={ini + 3} texto="PROVA 1" x={330} y={300} tamanho={100} rot={-2} fora={acabou} />
          <Dymo q={q} ini={fq(S4.graoCru.inicio)} texto="GRÃO CRU" x={600} y={420} tamanho={100} rot={1} fora={acabou} />
          <Recortadas q={q} ini={fq(S4.g350.inicio)} texto="350 g" x={800} y={575} tamanho={110} chave="c4-350" fora={acabou} />
        </Plano>
        {q >= acabou && <AbsoluteFill style={{background: 'rgba(12,8,5,0.62)'}} />}
        <Plano p={1}>
          <Recortadas q={q} ini={acabou} texto="ACABOU." x={540} y={900} tamanho={140} chave="c4-acabou" intervalo={1} />
          <Dymo q={q} ini={fq(S4.naoEspecial.inicio)} texto="NÃO É ESPECIAL." x={540} y={1170} tamanho={84} fundo={COR.acento} rot={-2} />
        </Plano>
        <Plano p={2.4}>
          <Peca q={q} ini={ini} nome="grao-quebrado" x={90} y={1500} w={280} rot={30} sombra={false} />
          <Peca q={q} ini={ini} nome="grao-concha" x={1000} y={420} w={260} rot={-20} sombra={false} />
        </Plano>
      </Palco>
      <Vinheta forca={0.4} />
    </AbsoluteFill>
  );
};

// ===================================================================== 5 · o contraste
const PILHA_DEFEITOS = ['grao-preto', 'grao-ardido', 'grao-quebrado', 'grao-brocado', 'grao-concha', 'casca', 'graveto', 'pedra',
  'cereja-seca', 'grao-fungo', 'grao-imaturo', 'grao-quaker'];

export const Cena5: React.FC<C> = ({q}) => {
  const ini = fq(S5.comparar.inicio);
  const noEsp = fq(S5.noEspecial.inicio);
  const zero = fq(S5.zero.inicio);
  const c = cam(q, [
    {q: ini, x: -270, y: 0, zoom: 1.25, rot: 0},
    {q: noEsp - 1, x: -250, y: -20, zoom: 1.28, rot: -0.4, curva: 'linear'},
    {q: noEsp + 5, x: 270, y: 0, zoom: 1.25, rot: 0.3, curva: 'rapida'},
    {q: fq(31.9), x: 260, y: -10, zoom: 1.27, rot: 0, curva: 'linear'},
    {q: fq(31.9) + 8, x: 0, y: 0, zoom: 1.0, rot: 0, curva: 'suave'},
    {q: fq(32.42), x: 0, y: 0, zoom: 1.02, rot: 0},
  ], 'c5', 0.8, [fq(S5.tipo.inicio), fq(S5.d360.inicio), zero], [zero]);
  const s = semente('c5-pilha');
  const quedas = Array.from({length: 26}, (_, k) => ({
    nome: PILHA_DEFEITOS[k % PILHA_DEFEITOS.length], ini: fq(28.0) + k * 2,
    x: 80 + s() * 380, y: 1180 + s() * 260, w: 110 + s() * 50, rot: (s() - 0.5) * 120,
  }));
  const n360 = Math.round(360 * progresso(q, fq(S5.d360.inicio), fq(29.26)));
  return (
    <AbsoluteFill>
      <Palco cam={c} id="c5">
        <Plano p={1}>
          <div style={{position: 'absolute', left: -600, top: -400, width: 1140, height: 2720, background: COR.terra}} />
          <div style={{position: 'absolute', left: 540, top: -400, width: 1140, height: 2720, background: COR.creme}} />
          <Divisoria q={q} ini={ini + 2} />
          <Dymo q={q} ini={fq(S5.classificacao.inicio)} texto="CLASSIFICAÇÃO" x={270} y={330} tamanho={54} rot={-2} />
          <Dymo q={q} ini={fq(26.87)} texto="OFICIAL" x={220} y={410} tamanho={54} rot={1} />
          <Dymo q={q} ini={fq(27.2)} texto="BRASILEIRA" x={300} y={490} tamanho={54} fundo={COR.verde} rot={-1} />
          <Peca q={q} ini={fq(26.4)} nome="peneira-classificacao" x={160} y={1380} w={300} rot={-10} />
          <Dymo q={q} ini={fq(S5.tipo.inicio)} texto="TIPO 8" x={270} y={650} tamanho={100} fundo={COR.creme} tinta={COR.preto} rot={-2} />
          {quedas.map((d, k) => <Peca key={k} q={q} ini={d.ini} nome={d.nome} x={d.x} y={d.y} w={d.w} rot={d.rot} />)}
          <Recortadas q={q} ini={fq(S5.d360.inicio)} texto={String(n360)} x={270} y={880} tamanho={180} chave="c5-360" intervalo={0} />
          <Dymo q={q} ini={fq(29.26)} texto="DEFEITOS" x={270} y={1060} tamanho={80} fundo={COR.acento} rot={2} />
          <Rodape q={q} ini={fq(29.4)} x={270} y={1630} texto="*COB · amostra de 300 g" tamanho={30} />
          <Serifa q={q} ini={fq(30.56)} texto="especial" x={810} y={520} tamanho={150} cor={COR.preto} rot={-3} />
          <Recortadas q={q} ini={zero} texto="0" x={810} y={860} tamanho={330} chave="c5-zero" />
          <Elipse q={q} ini={zero + 4} cx={810} cy={860} rx={190} ry={230} cor={COR.acento} chave="c5-el" espessura={11} />
          <Dymo q={q} ini={fq(31.38)} texto="DEFEITO GRAVE" x={810} y={1100} tamanho={62} fundo={COR.acento} rot={-1} />
          <Brilho q={q} ini={zero + 2} x={990} y={700} r={70} cor={COR.acento} />
          <Rodape q={q} ini={zero + 6} x={810} y={1630} texto="*classificação SCA, 350 g" tamanho={30} cor={COR.terra} />
        </Plano>
        <Plano p={2.4}>
          <Peca q={q} ini={ini} nome="grao-preto" x={60} y={1760} w={300} rot={-20} sombra={false} />
          <Peca q={q} ini={ini} nome="folha-4" x={1040} y={1700} w={500} rot={25} sombra={false} />
        </Plano>
      </Palco>
    </AbsoluteFill>
  );
};
