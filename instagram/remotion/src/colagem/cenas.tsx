// As oito cenas da peca 06. Cada uma recebe o quadro ABSOLUTO e monta a partir
// do campo vazio; a transicao para a proxima e uma `Folha` que sobe no fim dela.
// Todos os tempos vem de `tempos.ts` (medidos na narracao).

import React from 'react';
import {AbsoluteFill} from 'remotion';
import {COR} from '../identidade/tokens';
import {PILHA} from '../identidade/tipografia';
import {Campo, Carimbo, Embalagem, Fita, Folha, Manchete, Recorte, Rotulo, Tira} from './pecas';
import {progresso} from './movimento-colagem';
import {f, T} from './tempos';

type C = {q: number};
const FOLHA = 9;

/** Quadro em que cada cena passa a ser a de baixo (a folha da anterior ja cobriu). */
export const LIMITES = [
  0,
  f(T.poisE) + FOLHA,
  f(T.primeiro) + FOLHA,
  f(T.depois) + FOLHA,
  f(T.porIsso) + FOLHA,
  f(T.metros) + FOLHA,
  f(T.aGente) + FOLHA,
  f(T.desde) + FOLHA,
];

// ------------------------------------------------------------------ 1 gancho
export const Cena1: React.FC<C> = ({q}) => (
  <AbsoluteFill>
    <Campo cor={COR.terra} />
    <Rotulo q={q} ini={0} x={540} y={330} texto="VOCÊ SABIA?" tamanho={50} chave="c1-vs" />
    <Recorte q={q} ini={2} nome="xicara" x={540} y={800} w={640} />
    <Fita q={q} ini={8} x={540} y={490} w={260} rot={-8} chave="c1-f" />
    <Manchete q={q} y={1300} tamanho={128} chave="c1-m" quebraDepois={[1]}
      palavras={[['NEM', f(1.25)], ['TODO', f(1.68)], ['CAFÉ', f(1.93)]]} />
    <Carimbo q={q} ini={f(3.45)} x={560} y={1540} rot={-7} tamanho={96} fundo={COR.terra} chave="c1-c">É ESPECIAL?</Carimbo>
    <Folha q={q} ini={f(T.poisE)} cor={COR.terra} chave="f1" />
  </AbsoluteFill>
);

// ------------------------------------------------------------------ 2 duas provas
export const Cena2: React.FC<C> = ({q}) => (
  <AbsoluteFill>
    <Campo cor={COR.terra} />
    <Manchete q={q} y={360} tamanho={96} papel={COR.acento} tinta={COR.creme} chave="c2-m"
      palavras={[['ESPECIAL', f(T.poisE) + FOLHA]]} />
    <Recorte q={q} ini={f(T.praGanhar)} nome="peneira" x={290} y={880} w={450} rot={-4} />
    <Recorte q={q} ini={f(5.4)} nome="xicara" x={800} y={900} w={420} rot={3} />
    <Rotulo q={q} ini={f(T.duas)} x={290} y={1240} texto="PROVA 1" tamanho={62} cor={COR.terra} papel={COR.creme} chave="c2-p1" />
    <Fita q={q} ini={f(T.duas) + 3} x={210} y={1196} w={150} rot={-20} chave="c2-f1" />
    <Rotulo q={q} ini={f(T.duas) + 10} x={800} y={1240} texto="PROVA 2" tamanho={62} cor={COR.terra} papel={COR.creme} chave="c2-p2" />
    <Fita q={q} ini={f(T.duas) + 13} x={880} y={1196} w={150} rot={18} chave="c2-f2" />
    <Rotulo q={q} ini={f(T.duas) + 4} x={290} y={1350} texto="GRÃO CRU" tamanho={46} chave="c2-l1" />
    <Rotulo q={q} ini={f(T.duas) + 14} x={800} y={1350} texto="XÍCARA" tamanho={46} chave="c2-l2" />
    <Folha q={q} ini={f(T.primeiro)} cor={COR.terra} chave="f2" />
  </AbsoluteFill>
);

// ------------------------------------------------------------------ 3 grao cru
const Visor: React.FC<C> = ({q}) => {
  const ini = f(T.amostra);
  if (q < ini - 8) return null;
  const g = Math.round(350 * progresso(q, ini, f(T.gramasFim)));
  return (
    <div style={{position: 'absolute', left: 540, top: 1290, transform: 'translate(-50%,-50%) rotate(-1.5deg)',
                 background: COR.preto, padding: '26px 50px', border: `6px solid ${COR.creme}`,
                 boxShadow: '0 10px 14px rgba(0,0,0,0.4)'}}>
      <div style={{fontFamily: PILHA.dado, fontSize: 36, color: COR.creme, letterSpacing: 6}}>AMOSTRA</div>
      <div style={{fontFamily: PILHA.dado, fontSize: 150, color: COR.acento, lineHeight: 1, whiteSpace: 'nowrap'}}>
        {String(g).padStart(3, '0')} g
      </div>
    </div>
  );
};

const GRADE: Array<[number, number]> = [
  [270, 640], [540, 640], [810, 640],
  [270, 930], [540, 930], [810, 930],
  [270, 1220], [540, 1220], [810, 1220],
];

export const Cena3: React.FC<C> = ({q}) => {
  const grade = f(T.gramasFim) + FOLHA;
  return (
    <AbsoluteFill>
      <Campo cor={COR.terra} />
      <Rotulo q={q} ini={f(T.primeiro) + FOLHA} x={540} y={330} texto="01 · GRÃO CRU" tamanho={56} chave="c3-h" />
      <Recorte q={q} ini={f(8.6)} nome="prato" x={540} y={760} w={820} />
      <Visor q={q} />
      <Folha q={q} ini={f(T.gramasFim)} cor={COR.terra} chave="f3a" />
      {q >= grade && (
        <>
          <Rotulo q={q} ini={grade} x={540} y={330} texto="01 · GRÃO CRU" tamanho={56} chave="c3-h2" />
          {GRADE.slice(0, 8).map(([x, y], i) => (
            <Recorte key={i} q={q} ini={f(T.defeito) + i * 4} nome={`grao-${String(i + 1).padStart(2, '0')}`}
              x={x} y={y} w={180} rot={(i * 37) % 20 - 10} />
          ))}
          <Recorte q={q} ini={f(13.65)} nome="grao-defeito" x={810} y={1220} w={240} fora={f(14.0)} />
          <Carimbo q={q} ini={f(13.92)} x={810} y={1220} rot={-12} tamanho={150} fora={f(14.0)} chave="c3-x">✕</Carimbo>
          <Carimbo q={q} ini={f(T.nenhum)} x={540} y={1520} rot={-5} tamanho={92} fundo={COR.terra} chave="c3-0">
            <span style={{fontSize: 56, verticalAlign: 'middle'}}>DEFEITOS GRAVES </span>0
          </Carimbo>
        </>
      )}
      <Folha q={q} ini={f(T.depois)} cor={COR.terra} chave="f3" />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------ 4 xicara
const Regua: React.FC<C> = ({q}) => {
  const ini = f(T.nota) + FOLHA;
  if (q < ini) return null;
  const marca = progresso(q, f(21.0), f(T.oitenta));
  const larg = 900;
  const x0 = 90;
  const m = 50; // margem interna: 0 e 100 caem DENTRO do papel
  const util = larg - 2 * m;
  const pos = 80 * marca;
  const px = (n: number) => m + (util * n) / 100;
  return (
    <>
      <div style={{position: 'absolute', left: x0, top: 960, width: larg, height: 160, background: COR.creme,
                   transform: 'rotate(-1deg)', boxShadow: '0 10px 14px rgba(0,0,0,0.4)'}}>
        <div style={{position: 'absolute', left: m, top: 0, bottom: 0, width: (util * pos) / 100, background: 'rgba(20,16,13,0.28)'}} />
        {Array.from({length: 21}, (_, i) => (
          <div key={i} style={{position: 'absolute', left: px(i * 5) - 1.5, top: 0, width: 3,
                               height: i % 2 ? 34 : 60, background: COR.terra}} />
        ))}
        {[0, 20, 40, 60, 80, 100].map((n) => (
          <div key={n} style={{position: 'absolute', left: px(n), top: 84, transform: 'translateX(-50%)',
                               fontFamily: PILHA.dado, fontSize: 46, color: n === 80 && marca >= 1 ? COR.acento : COR.terra}}>{n}</div>
        ))}
        <div style={{position: 'absolute', left: px(pos) - 9, top: -40, width: 18, height: 240, background: COR.acento}} />
      </div>
    </>
  );
};

export const Cena4: React.FC<C> = ({q}) => {
  const tiras = f(T.aroma);
  const regua = f(T.nota) + FOLHA;
  return (
    <AbsoluteFill>
      <Campo cor={COR.terra} />
      <Rotulo q={q} ini={f(T.depois) + FOLHA} x={540} y={330} texto="02 · XÍCARA" tamanho={56} chave="c4-h" />
      {q < regua && (
        <>
          <Recorte q={q} ini={f(T.xicara)} nome="xicara" x={540} y={680} w={600 - 170 * progresso(q, tiras - 8, tiras + 2)} />
          <Recorte q={q} ini={f(16.3)} nome="colher" x={760} y={700} w={150} rot={32} />
          <Tira q={q} ini={f(T.aroma)} y={1040} rotulo="AROMA" valor={0.86} chave="t1" />
          <Tira q={q} ini={f(T.docura)} y={1180} rotulo="DOÇURA" valor={0.92} chave="t2" />
          <Tira q={q} ini={f(T.acidez)} y={1320} rotulo="ACIDEZ" valor={0.74} chave="t3" />
          <Tira q={q} ini={f(T.corpo)} y={1460} rotulo="CORPO" valor={0.82} chave="t4" />
        </>
      )}
      <Folha q={q} ini={f(T.nota)} cor={COR.terra} chave="f4a" />
      {q >= regua && (
        <>
          <Rotulo q={q} ini={regua} x={540} y={330} texto="02 · XÍCARA" tamanho={56} chave="c4-h2" />
          <Rotulo q={q} ini={regua + 2} x={540} y={760} texto="A NOTA PRECISA PASSAR DE" tamanho={48} chave="c4-n" />
          <Regua q={q} />
          <Carimbo q={q} ini={f(T.oitenta)} x={580} y={1340} rot={-6} tamanho={210} fundo={COR.terra} chave="c4-80">80+</Carimbo>
          <Rotulo q={q} ini={f(T.oitenta) + 6} x={540} y={1570} texto="PONTOS · ESCALA SCA" tamanho={44} chave="c4-sca" />
        </>
      )}
      <Folha q={q} ini={f(T.porIsso)} cor={COR.verde} chave="f4" />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------ 5 virada
export const Cena5: React.FC<C> = ({q}) => (
  <AbsoluteFill>
    <Campo cor={COR.verde} />
    <Rotulo q={q} ini={f(T.porIsso) + FOLHA} x={540} y={290} texto="POR ISSO" tamanho={56} chave="c5-h" />
    <Recorte q={q} ini={f(T.comeca)} nome="foto-lavoura-rua" x={540} y={950} w={800} rot={-2} deriva={[0, -0.25]} semBoil />
    <Fita q={q} ini={f(T.comeca) + 6} x={250} y={400} w={220} rot={-30} chave="c5-f1" />
    <Fita q={q} ini={f(T.comeca) + 8} x={830} y={420} w={220} rot={28} chave="c5-f2" />
    <Manchete q={q} y={1500} tamanho={104} chave="c5-m" quebraDepois={[1]}
      palavras={[['MUITO', f(25.79)], ['ANTES', f(26.22)], ['DA', f(26.65)], ['TORRA.', f(26.75)]]} />
    <Folha q={q} ini={f(T.metros)} cor={COR.verde} chave="f5" />
  </AbsoluteFill>
);

// ------------------------------------------------------------------ 6 altitude
const Altimetro: React.FC<C> = ({q}) => {
  const ini = f(T.metros) + FOLHA;
  if (q < ini) return null;
  const p = progresso(q, ini, f(T.altimetroFim));
  const m = Math.round(1250 * p);
  const topo = 1500 - 1000 * p;
  return (
    <div style={{position: 'absolute', left: 60, top: 420, width: 170, height: 1160, background: COR.creme,
                 transform: 'rotate(-1.5deg)', boxShadow: '0 10px 14px rgba(0,0,0,0.4)',
                 backgroundImage: `repeating-linear-gradient(0deg, rgba(59,42,31,0.25) 0 2px, transparent 2px 40px)`}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: topo - 420, height: 8, background: COR.acento}} />
      <div style={{position: 'absolute', left: 14, top: topo - 420 - 70, fontFamily: PILHA.dado, fontSize: 34, color: COR.terra, whiteSpace: 'nowrap'}}>
        {m.toLocaleString('pt-BR')} m
      </div>
    </div>
  );
};

export const Cena6: React.FC<C> = ({q}) => {
  const ini = f(T.metros) + FOLHA;
  const fruto = f(T.fruto) + FOLHA;
  return (
    <AbsoluteFill>
      <Campo cor={COR.verde} />
      {q < fruto && (
        <>
          <Recorte q={q} ini={ini} nome="foto-lavoura-ceu" x={600} y={780} w={900} rot={1.5} deriva={[-0.35, 0]} semBoil />
          <Recorte q={q} ini={ini + 10} nome="foto-cereja-verde" x={720} y={1290} w={520} rot={-4} deriva={[-0.9, -0.2]} semBoil />
          <Altimetro q={q} />
          <Carimbo q={q} ini={f(T.altimetroFim)} x={620} y={330} rot={-4} tamanho={120} fundo={COR.verde} cor={COR.creme} chave="c6-m">1.250 m</Carimbo>
          <Rotulo q={q} ini={f(29.3)} x={560} y={1560} texto="SERRA DA CANASTRA · MEDEIROS-MG" tamanho={40} cor={COR.terra} papel={COR.creme} chave="c6-s" />
        </>
      )}
      <Folha q={q} ini={f(T.fruto)} cor={COR.verde} chave="f6a" />
      {q >= fruto && (
        <>
          <Rotulo q={q} ini={fruto} x={540} y={420} texto="O FRUTO AMADURECE DEVAGAR" tamanho={48} chave="c6-d" />
          <Recorte q={q} ini={fruto + 2} nome="cereja-verde-1" x={250} y={880} w={230} />
          <Recorte q={q} ini={f(31.4)} nome="cereja-amarela-2" x={540} y={880} w={230} />
          <Recorte q={q} ini={f(32.1)} nome="cereja-vermelha-3" x={830} y={880} w={240} />
          <div style={{position: 'absolute', left: 140, top: 1150, width: 800, height: 30, background: 'rgba(241,236,224,0.25)'}}>
            <div style={{height: '100%', width: `${100 * progresso(q, fruto + 2, f(T.devagarFim) + 10)}%`, background: COR.creme}} />
          </div>
          <Rotulo q={q} ini={fruto + 4} x={540} y={1230} texto="MATURAÇÃO" tamanho={46} chave="c6-mt" />
          <Carimbo q={q} ini={f(T.acucar)} x={540} y={1460} rot={-5} tamanho={130} fundo={COR.verde} cor={COR.creme} chave="c6-a">+ AÇÚCAR</Carimbo>
        </>
      )}
      <Folha q={q} ini={f(T.aGente)} cor={COR.verde} chave="f6" />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------ 7 do pe a torra
const Cartao: React.FC<{q: number; ini: number; x: number; y: number; rot: number; nome: string; rotulo: string; fundoObjeto?: boolean}> =
  ({q, ini, x, y, rot, nome, rotulo, fundoObjeto}) => (
    <>
      {fundoObjeto && q >= ini && (
        <div style={{position: 'absolute', left: x - 200, top: y - 230, width: 400, height: 460, background: COR.creme,
                     transform: `rotate(${rot}deg)`, boxShadow: '0 10px 14px rgba(0,0,0,0.35)'}} />
      )}
      <Recorte q={q} ini={ini} nome={nome} x={x} y={y} w={fundoObjeto ? 330 : 400} rot={rot} />
      <Rotulo q={q} ini={ini + 3} x={x} y={y + 290} texto={rotulo} tamanho={46} cor={COR.terra} papel={COR.creme} chave={`c7-${rotulo}`} />
    </>
  );

export const Cena7: React.FC<C> = ({q}) => {
  const sem = f(T.semInter) + FOLHA;
  return (
    <AbsoluteFill>
      <Campo cor={COR.verde} />
      {q < sem && (
        <>
          <Manchete q={q} y={390} tamanho={84} chave="c7-m" papel={COR.creme} tinta={COR.verde} quebraDepois={[1]}
            palavras={[['SÓ', f(34.47)], ['TORRAMOS', f(34.69)], ['O', f(35.2)], ['NOSSO', f(35.7)]]} />
          <Cartao q={q} ini={f(T.planta)} x={290} y={830} rot={-5} nome="foto-cafeeiro" rotulo="PLANTA" />
          <Cartao q={q} ini={f(T.colhe)} x={790} y={720} rot={4} nome="cachinho" rotulo="COLHE" fundoObjeto />
          <Cartao q={q} ini={f(T.seleciona)} x={600} y={1360} rot={-2} nome="peneira" rotulo="SELECIONA" fundoObjeto />
        </>
      )}
      <Folha q={q} ini={f(T.semInter)} cor={COR.terra} chave="f7a" />
      {q >= sem && (
        <>
          <Campo cor={COR.terra} />
          <Recorte q={q} ini={sem} nome="torrado" x={540} y={760} w={420} />
          <Carimbo q={q} ini={sem + 2} x={540} y={1180} rot={-5} tamanho={86} fundo={COR.terra} chave="c7-s1">SEM INTERMEDIÁRIO.</Carimbo>
          <Carimbo q={q} ini={f(T.semMistura)} x={540} y={1400} rot={3} tamanho={110} fundo={COR.terra} chave="c7-s2">SEM MISTURA.</Carimbo>
        </>
      )}
      <Folha q={q} ini={f(T.desde)} cor={COR.creme} chave="f7" />
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------ 8 assinatura
export const Cena8: React.FC<C> = ({q}) => {
  const ini = f(T.desde) + FOLHA;
  const pacotes = f(T.cafeCanastra);
  return (
    <AbsoluteFill>
      <Campo cor={COR.creme} />
      {q < pacotes + 4 && (
        <>
          <Rotulo q={q} ini={ini} x={540} y={520} texto="DESDE" tamanho={60} cor={COR.terra} chave="c8-d" />
          <Manchete q={q} y={800} tamanho={210} papel={COR.terra} tinta={COR.creme} chave="c8-ano"
            palavras={[['1', ini + 2], ['9', ini + 5], ['8', ini + 8], ['5', ini + 11]]} />
          {[0, 1, 2].map((i) => (
            <React.Fragment key={i}>
              <Fita q={q} ini={f(T.geracoes) + i * 10} x={260 + i * 280} y={1130} w={230} rot={[-8, 5, -3][i]} chave={`c8-f${i}`} />
              <Rotulo q={q} ini={f(T.geracoes) + i * 10 + 2} x={260 + i * 280} y={1132} texto={`${i + 1}ª`} tamanho={56} cor={COR.terra} chave={`c8-g${i}`} />
            </React.Fragment>
          ))}
          <Rotulo q={q} ini={f(44.4)} x={540} y={1300} texto="GERAÇÕES · FAMÍLIA BOAVENTURA" tamanho={44} cor={COR.terra} chave="c8-fb" />
        </>
      )}
      <Folha q={q} ini={pacotes - FOLHA} cor={COR.creme} chave="f8" />
      {q >= pacotes && (
        <>
          <Manchete q={q} y={380} tamanho={104} papel={COR.terra} tinta={COR.creme} chave="c8-cc"
            palavras={[['CAFÉ', pacotes], ['CANASTRA', pacotes + 5]]} />
          <Embalagem q={q} ini={pacotes + 2} sku="classico" x={225} y={940} h={960} rot={-4} />
          <Embalagem q={q} ini={pacotes + 6} sku="suave" x={540} y={910} h={980} rot={0} />
          <Embalagem q={q} ini={pacotes + 10} sku="canela" x={855} y={940} h={960} rot={4} />
          <Manchete q={q} y={1400} tamanho={70} papel={COR.creme} tinta={COR.terra} chave="c8-sl" quebraDepois={[2]}
            palavras={[['O', f(T.slogan)], ['CAFÉ', f(47.3)], ['QUE', f(47.5)], ['ETERNIZA', f(47.96)], ['MOMENTOS.', f(48.48)]]} />
          <Rotulo q={q} ini={f(48.9)} x={540} y={1575} texto="loja.cafecanastra.com" tamanho={50} cor={COR.creme} papel={COR.acento} chave="c8-cta" />
        </>
      )}
    </AbsoluteFill>
  );
};

export const CENAS = [Cena1, Cena2, Cena3, Cena4, Cena5, Cena6, Cena7, Cena8];
