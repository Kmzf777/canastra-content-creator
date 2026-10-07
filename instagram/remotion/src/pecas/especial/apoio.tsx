// Peças de apoio da peça 07: fundo, recorte, fita, tachinha, pacote genérico e a
// atmosfera (sombra de folhas tirada da foto REAL da fazenda, grão de filme, vinheta).
// Toda entrada anda em passo de stop-motion; só a câmera é lisa.

import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {COR} from '../../identidade/tokens';
import {assentar, boil, posterizar, progresso, saida} from '../../colagem/movimento-colagem';
import {semente, sorteio} from '../../colagem/semente';

export const FPS = 30;
export const fq = (s: number) => Math.round(s * FPS);

export const Fundo: React.FC<{cor: string; textura?: 'kraft' | 'nenhuma'; forca?: number}> = ({cor, textura = 'kraft', forca = 0.5}) => (
  <AbsoluteFill style={{background: cor}}>
    {textura === 'kraft' && (
      <Img src={staticFile('colagem/kraft.png')} style={{width: '100%', height: '100%', mixBlendMode: 'multiply', opacity: forca}} />
    )}
  </AbsoluteFill>
);

/** Saída "arrancada": a peça voa para o lado a partir de `fora`. */
function arranque(q: number, fora: number | undefined, chave: string) {
  if (fora === undefined || q < fora) return {dx: 0, dy: 0, rot: 0};
  const t = saida((q - fora) / 7);
  const lado = sorteio(`${chave}#lado`, 0, 1) < 0.5 ? -1 : 1;
  return {dx: lado * 1500 * t * t, dy: -260 * t, rot: lado * 45 * t};
}

/**
 * Recorte de colagem (peça da biblioteca): assenta, depois ferve entre b0/b1/b2.
 * `entra` decide de onde vem; `treme` sacode a peça (a xícara que destoa).
 */
export const Peca: React.FC<{
  q: number; ini: number; nome: string; x: number; y: number; w: number; rot?: number; fora?: number;
  semBoil?: boolean; treme?: number; sombra?: boolean; opacidade?: number; unico?: boolean;
}> = ({q, ini, nome, x, y, w, rot = 0, fora, semBoil, treme, sombra = true, opacidade = 1, unico}) => {
  const qp = posterizar(q, 3, ini);
  const p = assentar(qp, ini, nome + x);
  if (!p.visivel) return null;
  const assentou = q >= ini + 6;
  const b = assentou && !semBoil && !unico ? boil(q, nome + x) : {variante: 0 as const, rot: 0};
  const a = arranque(q, fora, nome + x);
  const tr = treme !== undefined && q >= treme ? Math.sin(posterizar(q, 2) * 1.7) * 7 : 0;
  const src = unico ? `colagem/${nome}.png` : `colagem/${nome}-b${b.variante}.png`;
  return (
    <Img src={staticFile(src)} style={{
      position: 'absolute', left: x - w / 2, top: y, width: w,
      transform: `translate(${a.dx}px, ${p.dy + a.dy}px) translateY(-50%) rotate(${rot + p.rot + b.rot + a.rot + tr}deg) scale(${p.escala})`,
      opacity: p.opacidade * opacidade, filter: sombra ? 'drop-shadow(0px 10px 12px rgba(12,8,5,0.36))' : undefined,
    }} />
  );
};

/** Troca de objeto NO MESMO LUGAR (match cut do reel de 304 mil): um por janela. */
export const Troca: React.FC<{q: number; itens: Array<{nome: string; ini: number; w: number; rot?: number}>; x: number; y: number; ate?: number}> = ({
  q, itens, x, y, ate,
}) => {
  const atual = [...itens].reverse().find((i) => q >= i.ini);
  if (!atual || (ate !== undefined && q >= ate)) return null;
  return <Peca q={q} ini={atual.ini} nome={atual.nome} x={x} y={y} w={atual.w} rot={atual.rot ?? 0} />;
};

export const Fita: React.FC<{q: number; ini: number; x: number; y: number; w?: number; rot?: number; chave: string; fora?: number}> = ({
  q, ini, x, y, w = 200, rot = 0, chave, fora,
}) => {
  if (q < ini || (fora !== undefined && q >= fora)) return null;
  const v = q >= ini + 3 ? boil(q, chave).variante : 0;
  const s = 1.15 - 0.15 * progresso(q, ini, ini + 3);
  return (
    <Img src={staticFile(`colagem/fita-crepe-b${v}.png`)} style={{
      position: 'absolute', left: x - w / 2, top: y - w * 0.13, width: w, transform: `rotate(${rot}deg) scale(${s})`,
    }} />
  );
};

export const Tachinha: React.FC<{q: number; ini: number; x: number; y: number; cor?: 'terra' | 'creme' | 'preta' | 'verde'; s?: number}> = ({
  q, ini, x, y, cor = 'terra', s = 70,
}) => {
  if (q < ini) return null;
  const e = q - ini < 2 ? 1.4 : 1;
  return (
    <Img src={staticFile(`colagem/tachinha-${cor}-b0.png`)} style={{
      position: 'absolute', left: x - s / 2, top: y - s / 2, width: s, transform: `scale(${e})`,
      filter: 'drop-shadow(2px 6px 4px rgba(0,0,0,0.4))',
    }} />
  );
};

/** Pacote genérico, SEM marca nenhuma: silhueta de saco kraft com válvula. Só desenho. */
export const PacoteGenerico: React.FC<{q: number; ini: number; x: number; y: number; h: number; rot?: number; fora?: number}> = ({
  q, ini, x, y, h, rot = 0, fora,
}) => {
  const p = assentar(posterizar(q, 3, ini), ini, 'pacote-generico');
  if (!p.visivel || (fora !== undefined && q >= fora)) return null;
  const w = h * 0.58;
  return (
    <svg width={w} height={h} viewBox="0 0 58 100" style={{
      position: 'absolute', left: x - w / 2, top: y - h / 2, overflow: 'visible',
      transform: `translateY(${p.dy}px) rotate(${rot + p.rot}deg) scale(${p.escala})`,
      filter: 'drop-shadow(0px 14px 16px rgba(12,8,5,0.35))',
    }}>
      <path d="M4,10 L54,10 L57,96 Q29,99 1,96 Z" fill="#C9A473" />
      <path d="M4,10 L54,10 L54,4 L4,4 Z" fill="#B48F5E" />
      {[6, 12, 18, 24, 30, 36, 42, 48].map((xx) => <line key={xx} x1={xx} y1={4} x2={xx} y2={10} stroke="#9C7A4C" strokeWidth={0.5} />)}
      <path d="M8,14 Q12,55 7,93" stroke="#B9935F" strokeWidth={0.8} fill="none" />
      <path d="M50,14 Q46,55 51,93" stroke="#B9935F" strokeWidth={0.8} fill="none" />
      <circle cx={29} cy={26} r={4.2} fill="#B9935F" />
      <circle cx={29} cy={26} r={1.2} fill="#7E5F38" />
    </svg>
  );
};

/** Sombra de folhas (gobo) da foto REAL da folhagem de Medeiros: sol a pino entre as folhas. */
export const SombraFolhas: React.FC<{q: number; opacidade?: number; vel?: number}> = ({q, opacidade = 0.3, vel = 0.35}) => (
  <Img src={staticFile('colagem/sombra-folhas.png')} style={{
    position: 'absolute', left: -270 - Math.sin(q / 90) * 60, top: -120 - q * vel * 0.2, width: 1620,
    mixBlendMode: 'multiply', opacity: opacidade, filter: 'blur(5px)',
  }} />
);

/** Grão de filme: 4 variantes, troca a cada 2 quadros (proibicoes.md: σ≈0,9, segurado 2 quadros). */
export const GraoFilme: React.FC<{q: number; forca?: number}> = ({q, forca = 0.12}) => (
  <Img src={staticFile(`colagem/grao-filme-b${Math.floor(q / 2) % 4}.png`)} style={{
    position: 'absolute', inset: 0, width: '100%', height: '100%', mixBlendMode: 'overlay', opacity: forca,
  }} />
);

export const Vinheta: React.FC<{forca?: number; cor?: string}> = ({forca = 0.55, cor = '12,8,5'}) => (
  <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 46%, rgba(${cor},0) 42%, rgba(${cor},${forca}) 100%)`}} />
);

/** Foco de luz: só o centro aceso (o "segredo" da cena 7). */
export const Foco: React.FC<{q: number; ini: number; raio?: number}> = ({q, ini, raio = 620}) => {
  const k = progresso(q, ini, ini + 8);
  return (
    <AbsoluteFill style={{
      background: `radial-gradient(circle at 50% 44%, rgba(0,0,0,0) ${raio * (0.5 + 0.5 * k)}px, rgba(8,5,3,${0.82 * k}) ${raio * (0.5 + 0.5 * k) + 260}px)`,
    }} />
  );
};

/** Folha de papel que cobre o quadro subindo com a borda rasgada (transição). */
export const Cobertura: React.FC<{q: number; ini: number; dur?: number; cor: string; chave: string}> = ({q, ini, dur = 7, cor, chave}) => {
  if (q < ini) return null;
  const t = progresso(q, ini, ini + dur);
  const s = semente(chave);
  let d = 'M0,30';
  for (let x = 0; x <= 1080; x += 18) d += ` L${x},${12 + s() * 30}`;
  d += ' L1080,2100 L0,2100 Z';
  return (
    <svg width={1080} height={2100} viewBox="0 0 1080 2100" style={{position: 'absolute', left: 0, top: 1960 - 2020 * t,
      filter: 'drop-shadow(0 -8px 12px rgba(0,0,0,0.35))'}}>
      <path d={d} fill={cor} />
    </svg>
  );
};

/** Linha preta fina que divide a tela (técnica do reel de 209 mil), desenhada de cima para baixo. */
export const Divisoria: React.FC<{q: number; ini: number; x?: number}> = ({q, ini, x = 540}) => {
  if (q < ini) return null;
  const k = progresso(q, ini, ini + 6);
  return <div style={{position: 'absolute', left: x - 3, top: 0, width: 6, height: 1920 * k, background: COR.preto}} />;
};

/** Nota de rodapé miúda — a fonte do dado, como o "496" de página no reel de colagem. */
export const Rodape: React.FC<{q: number; ini: number; x: number; y: number; texto: string; cor?: string; tamanho?: number}> = ({
  q, ini, x, y, texto, cor = COR.creme, tamanho = 26,
}) =>
  q < ini ? null : (
    <div style={{position: 'absolute', left: x, top: y, transform: 'translate(-50%,-50%)', whiteSpace: 'nowrap',
      fontFamily: '"IBM Plex Mono", monospace', fontWeight: 500, fontSize: tamanho, color: cor, opacity: 0.85, letterSpacing: 1}}>
      {texto}
    </div>
  );
