// Mede a LARGURA DE AVANCO de cada glifo direto do .ttf e imprime o modulo
// `src/identidade/glifos.ts`.
//
// POR QUE EXISTE
//
// A camada de manchete (`src/motor/camadas/TextoTela.tsx`) precisa saber quantas
// linhas um texto vai ocupar para escolher o corpo que cabe na area segura. Sem
// largura de glifo, o corpo da manchete seria um numero escolhido no olho -- e o
// teste "o texto nunca sai da area segura" viraria tautologia, porque nada
// mediria o texto.
//
// `document.measureText` nao serve: ele so existe dentro do Chrome do render, e
// o portao de layout roda em Node, no vitest. Entao a largura vem do arquivo de
// fonte, que e a mesma fonte da verdade que o Chrome vai usar.
//
// COMO RODAR
//
//   node scripts/medir-glifos.mjs > src/identidade/glifos.ts
//
// KERNING: nao e lido. Kerning vive em GPOS e, nestas grotescas, os pares de
// caixa alta que tem par (AV, AT, LT...) sao NEGATIVOS -- apertam. Ignorar
// kerning portanto SUPERESTIMA a largura, que e o lado seguro para caber numa
// caixa. Nao ha margem inventada em cima disso.

import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname, join} from 'node:path';

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = join(AQUI, '..');

/** Os tres .ttf de `src/identidade/fontes/`, nos papeis de `tokens.ts`. */
const ARQUIVOS = [
  {papel: 'manchete', arquivo: 'ArchivoBlack-Regular.ttf'},
  {papel: 'corpo', arquivo: 'Inter-Bold.ttf'},
  {papel: 'dado', arquivo: 'IBMPlexMono-Medium.ttf'},
];

// ---------------------------------------------------------------------------
// leitor de tabelas sfnt

function abrir(buf) {
  const numTables = buf.readUInt16BE(4);
  const tabelas = new Map();
  for (let i = 0; i < numTables; i++) {
    const p = 12 + i * 16;
    tabelas.set(buf.toString('ascii', p, p + 4), {
      offset: buf.readUInt32BE(p + 8),
      length: buf.readUInt32BE(p + 12),
    });
  }
  return tabelas;
}

function exigir(tabelas, tag, arquivo) {
  const t = tabelas.get(tag);
  if (!t) throw new Error(`${arquivo}: tabela '${tag}' ausente`);
  return t;
}

/** cmap formato 4 (BMP, platform 3 / encoding 1 ou 0): codepoint -> glyphId. */
function lerCmap4(buf, base, arquivo) {
  const numTables = buf.readUInt16BE(base + 2);
  let sub = null;
  for (let i = 0; i < numTables; i++) {
    const p = base + 4 + i * 8;
    const plataforma = buf.readUInt16BE(p);
    const codificacao = buf.readUInt16BE(p + 2);
    const offset = buf.readUInt32BE(p + 4);
    const formato = buf.readUInt16BE(base + offset);
    if (formato === 4 && (plataforma === 3 || plataforma === 0)) {
      sub = base + offset;
      if (plataforma === 3 && codificacao === 1) break; // preferido
    }
  }
  if (sub === null) throw new Error(`${arquivo}: sem cmap formato 4`);

  const segCount = buf.readUInt16BE(sub + 6) / 2;
  const fimSeg = sub + 14;
  const inicioSeg = fimSeg + segCount * 2 + 2;
  const deltaSeg = inicioSeg + segCount * 2;
  const rangeSeg = deltaSeg + segCount * 2;

  const mapa = new Map();
  for (let s = 0; s < segCount; s++) {
    const fim = buf.readUInt16BE(fimSeg + s * 2);
    const inicio = buf.readUInt16BE(inicioSeg + s * 2);
    const delta = buf.readInt16BE(deltaSeg + s * 2);
    const rangeOffset = buf.readUInt16BE(rangeSeg + s * 2);
    if (inicio === 0xffff) continue;
    for (let c = inicio; c <= fim && c !== 0x10000; c++) {
      let g;
      if (rangeOffset === 0) {
        g = (c + delta) & 0xffff;
      } else {
        const p = rangeSeg + s * 2 + rangeOffset + (c - inicio) * 2;
        g = buf.readUInt16BE(p);
        if (g !== 0) g = (g + delta) & 0xffff;
      }
      if (g !== 0) mapa.set(c, g);
    }
  }
  return mapa;
}

/** hmtx: glyphId -> advanceWidth em unidades de em. */
function lerHmtx(buf, offset, numeroDeMetricas, numGlyphs) {
  const avancos = new Array(numGlyphs);
  let ultimo = 0;
  for (let g = 0; g < numGlyphs; g++) {
    if (g < numeroDeMetricas) {
      ultimo = buf.readUInt16BE(offset + g * 4);
    }
    avancos[g] = ultimo;
  }
  return avancos;
}

// ---------------------------------------------------------------------------
// o conjunto medido

/**
 * Todo caractere que uma manchete ou um dado pode conter em pt-BR. Se algum dia
 * faltar um, `larguraEm()` cai no avanco do 'x' e o texto pode estourar a caixa
 * por alguns por cento -- entao e melhor a lista sobrar do que faltar.
 */
function conjunto() {
  const cs = new Set();
  for (const c of 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') cs.add(c);
  for (const c of 'abcdefghijklmnopqrstuvwxyz') cs.add(c);
  for (const c of '0123456789') cs.add(c);
  for (const c of ' .,;:!?\'"()[]{}-–—/\\&%+*=@#°ºª$<>|_') cs.add(c);
  // acentuacao de pt-BR, caixa alta e baixa
  for (const c of 'ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑ') cs.add(c);
  for (const c of 'áàâãäéèêëíìîïóòôõöúùûüçñ') cs.add(c);
  return [...cs];
}

// ---------------------------------------------------------------------------

const saida = [];
const relato = [];

for (const {papel, arquivo} of ARQUIVOS) {
  const caminho = join(RAIZ, 'src', 'identidade', 'fontes', arquivo);
  const buf = readFileSync(caminho);
  const tabelas = abrir(buf);

  const head = exigir(tabelas, 'head', arquivo);
  const unitsPerEm = buf.readUInt16BE(head.offset + 18);
  const hhea = exigir(tabelas, 'hhea', arquivo);
  const numeroDeMetricas = buf.readUInt16BE(hhea.offset + 34);
  const maxp = exigir(tabelas, 'maxp', arquivo);
  const numGlyphs = buf.readUInt16BE(maxp.offset + 4);
  const hmtx = exigir(tabelas, 'hmtx', arquivo);
  const cmap = exigir(tabelas, 'cmap', arquivo);

  const avancos = lerHmtx(buf, hmtx.offset, numeroDeMetricas, numGlyphs);
  const mapa = lerCmap4(buf, cmap.offset, arquivo);

  // altura de linha natural da fonte, para o caso de alguem querer conferir
  const ascender = buf.readInt16BE(hhea.offset + 4);
  const descender = buf.readInt16BE(hhea.offset + 6);
  const lineGap = buf.readInt16BE(hhea.offset + 8);

  const tabela = {};
  const faltando = [];
  for (const c of conjunto()) {
    const g = mapa.get(c.codePointAt(0));
    if (g === undefined) {
      faltando.push(c);
      continue;
    }
    // arredonda em 4 casas: o em normalizado nao precisa de mais, e mantem o
    // arquivo gerado legivel em diff.
    tabela[c] = Math.round((avancos[g] / unitsPerEm) * 10000) / 10000;
  }

  if (faltando.length > 0) {
    // O .ttf foi baixado inteiro de proposito (ver tipografia.ts). Se faltar
    // glifo, o download veio recortado e isso tem que aparecer, nao passar.
    throw new Error(
      `${arquivo}: sem glifo para ${faltando.map((c) => JSON.stringify(c)).join(', ')}`,
    );
  }

  const larguras = Object.values(tabela);
  relato.push({
    papel,
    arquivo,
    unitsPerEm,
    numGlyphs,
    numeroDeMetricas,
    glifosMedidos: larguras.length,
    ascender: ascender / unitsPerEm,
    descender: descender / unitsPerEm,
    lineGap: lineGap / unitsPerEm,
    minimo: Math.min(...larguras),
    maximo: Math.max(...larguras),
    espaco: tabela[' '],
    caixaAltaMedia:
      Math.round(
        ([...'ABCDEFGHIJKLMNOPQRSTUVWXYZ'].reduce((s, c) => s + tabela[c], 0) / 26) *
          10000,
      ) / 10000,
  });

  saida.push({papel, tabela});
}

// ---------------------------------------------------------------------------
// o modulo gerado

const linhas = [];
linhas.push('// GERADO POR `node scripts/medir-glifos.mjs`. NAO EDITE A MAO.');
linhas.push('//');
linhas.push('// Largura de avanco de cada glifo, em fracao de em, lida da tabela `hmtx` dos');
linhas.push('// proprios .ttf de `src/identidade/fontes/`. Serve para a camada de texto');
linhas.push('// escolher um corpo que CAIBA na area segura, em Node, sem Chrome.');
linhas.push('//');
linhas.push('// Kerning (GPOS) nao entra. Nestas grotescas os pares com kern apertam, entao a');
linhas.push('// soma dos avancos e um limite SUPERIOR da largura real -- o lado seguro.');
linhas.push('//');
linhas.push('// Medido em:');
for (const r of relato) {
  linhas.push(
    `//   ${r.papel.padEnd(8)} ${r.arquivo}  unitsPerEm ${r.unitsPerEm} · ` +
      `${r.numGlyphs} glifos no arquivo · ${r.glifosMedidos} medidos · ` +
      `avanco ${r.minimo}..${r.maximo} em · espaco ${r.espaco} · ` +
      `media da caixa alta ${r.caixaAltaMedia} · ` +
      `asc ${r.ascender.toFixed(4)} desc ${r.descender.toFixed(4)} gap ${r.lineGap.toFixed(4)}`,
  );
}
linhas.push('');
// `import type` e apagado pelo esbuild, entao isto NAO puxa o efeito colateral
// de `tipografia.ts` (delayRender + loadFont), que quebraria o vitest em Node.
linhas.push("import type {Papel} from './tipografia';");
linhas.push('');
linhas.push('/**');
linhas.push(' * Metricas verticais de `hhea`, em fracao de em.');
linhas.push(' *');
linhas.push(' * `alturaLinha` = ascender - descender + lineGap: a entrelinha NATURAL da');
linhas.push(' * fonte, do proprio arquivo. E ela que a cartela usa como respiro, no lugar de');
linhas.push(' * um numero escolhido no olho.');
linhas.push(' */');
linhas.push(
  'export const METRICAS: Record<Papel, {ascender: number; descender: number; lineGap: number; alturaLinha: number}> = {',
);
for (const r of relato) {
  const alturaLinha = r.ascender - r.descender + r.lineGap;
  const q = (n) => Math.round(n * 10000) / 10000;
  linhas.push(
    `  ${r.papel}: {ascender: ${q(r.ascender)}, descender: ${q(r.descender)}, ` +
      `lineGap: ${q(r.lineGap)}, alturaLinha: ${q(alturaLinha)}},`,
  );
}
linhas.push('};');
linhas.push('');
linhas.push('export const GLIFOS: Record<Papel, Readonly<Record<string, number>>> = {');
for (const {papel, tabela} of saida) {
  linhas.push(`  ${papel}: {`);
  const entradas = Object.entries(tabela);
  // 6 por linha, para o diff nao virar uma coluna de 100 linhas
  for (let i = 0; i < entradas.length; i += 6) {
    linhas.push(
      '    ' +
        entradas
          .slice(i, i + 6)
          .map(([c, w]) => `${JSON.stringify(c)}: ${w}`)
          .join(', ') +
        ',',
    );
  }
  linhas.push('  },');
}
linhas.push('};');
linhas.push('');
linhas.push('/**');
linhas.push(' * Largura de `texto` em fracao de em, sob `papel`.');
linhas.push(' *');
linhas.push(' * Caractere fora da tabela cai no avanco do `x` do mesmo papel -- nunca em 0,');
linhas.push(' * que faria um texto largo parecer caber.');
linhas.push(' */');
linhas.push('export function larguraEm(texto: string, papel: Papel): number {');
linhas.push('  const t = GLIFOS[papel];');
linhas.push('  const padrao = t["x"];');
linhas.push('  let soma = 0;');
linhas.push('  for (const c of texto) soma += t[c] ?? padrao;');
linhas.push('  return soma;');
linhas.push('}');
linhas.push('');

process.stdout.write(linhas.join('\n'));

// O relato vai para stderr, para nao sujar o modulo redirecionado em stdout.
for (const r of relato) {
  process.stderr.write(
    `[glifos] ${r.papel.padEnd(8)} ${r.arquivo}: unitsPerEm=${r.unitsPerEm} ` +
      `numGlyphs=${r.numGlyphs} numberOfHMetrics=${r.numeroDeMetricas} ` +
      `medidos=${r.glifosMedidos} espaco=${r.espaco} ` +
      `caixaAltaMedia=${r.caixaAltaMedia} min=${r.minimo} max=${r.maximo}\n`,
  );
}
