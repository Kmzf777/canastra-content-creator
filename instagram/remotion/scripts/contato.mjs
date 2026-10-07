// Folha de contato de qualquer composição: um bundle, N stills, um mosaico.
//
//   node scripts/contato.mjs <composicao> <projeto> [segundos,separados] [--escala=0.25] [--cols=8] [--saida=nome.png]
//
// Sem lista de segundos: um quadro a cada 2,5 s da peça inteira. Cada célula leva o
// instante escrito no canto (em pixel, desenhado aqui), para a conferência citar o tempo.

import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import {PNG} from 'pngjs';
import fs from 'node:fs';
import path from 'node:path';

const [comp, projeto, lista, ...resto] = process.argv.slice(2);
const opc = Object.fromEntries(resto.filter((a) => a.startsWith('--')).map((a) => a.slice(2).split('=')));
const escala = Number(opc.escala ?? 0.25);
const cols = Number(opc.cols ?? 8);
const PROJ = path.resolve('projetos', projeto);

const servir = await bundle({entryPoint: path.resolve('src/index.ts'), publicDir: path.join(PROJ, 'public')});
const c = await selectComposition({serveUrl: servir, id: comp});
const segs = lista && lista !== '-' ? lista.split(',').map(Number) : Array.from({length: Math.floor(c.durationInFrames / c.fps / 2.5) + 1}, (_, k) => k * 2.5);
const dir = path.join(PROJ, 'saida', 'stills');
fs.mkdirSync(dir, {recursive: true});
const cw = Math.round(c.width * escala);
const ch = Math.round(c.height * escala);
const arquivos = [];
for (const s of segs) {
  const q = Math.min(c.durationInFrames - 1, Math.round(s * c.fps));
  const out = path.join(dir, `q${String(q).padStart(4, '0')}.png`);
  await renderStill({composition: c, serveUrl: servir, frame: q, output: out, scale: escala, imageFormat: 'png'});
  arquivos.push([s, out]);
  process.stdout.write(`${s.toFixed(2)}s `);
}
const linhas = Math.ceil(arquivos.length / cols);
const folha = new PNG({width: cols * (cw + 6), height: linhas * (ch + 6)});
folha.data.fill(30);
arquivos.forEach(([, a], i) => {
  const img = PNG.sync.read(fs.readFileSync(a));
  PNG.bitblt(img, folha, 0, 0, img.width, img.height, (i % cols) * (cw + 6) + 3, Math.floor(i / cols) * (ch + 6) + 3);
});
const destino = path.join(PROJ, 'saida', opc.saida ?? 'contato.png');
fs.writeFileSync(destino, PNG.sync.write(folha));
console.log('\nfolha:', destino);
