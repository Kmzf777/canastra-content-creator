// Folha de contato da peca 06: um still por montagem, num bundle so.
//
//   node scripts/contato-colagem.mjs [quadro1,quadro2,...]
//
// Sem argumento usa o ultimo quadro de cada uma das 16 montagens (segundos
// abaixo, copiados de colagem/tempos.ts: o fim de cada gesto, logo antes da
// proxima folha). Saida: projetos/06-voce-sabia-especial/saida/contato.png

import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import {PNG} from 'pngjs';
import fs from 'node:fs';
import path from 'node:path';

const PROJ = 'projetos/06-voce-sabia-especial';
const FPS = 30;
const MONTAGENS = [
  ['1a', 3.3], ['1b', 4.1], ['2a', 6.6], ['2b', 8.3], ['3a', 12.35], ['3b', 13.9],
  ['3c', 15.05], ['4a', 16.7], ['4b', 20.0], ['4c', 23.4], ['5a', 27.15], ['6a', 30.6],
  ['6b', 34.4], ['7a', 39.9], ['7b', 41.95], ['8a', 45.5], ['8b', 50.1],
];

const arg = process.argv[2];
const alvos = arg
  ? arg.split(',').map((n) => [`q${n}`, Number(n) / FPS])
  : MONTAGENS;

const servir = await bundle({entryPoint: path.resolve('src/index.ts'), publicDir: path.resolve(PROJ, 'public')});
const comp = await selectComposition({serveUrl: servir, id: 'VoceSabiaColagem'});
const dir = path.resolve(PROJ, 'saida', 'stills');
fs.mkdirSync(dir, {recursive: true});

const escala = 0.25;
const cw = Math.round(1080 * escala), ch = Math.round(1920 * escala);
const arquivos = [];
for (const [nome, s] of alvos) {
  const quadro = Math.min(comp.durationInFrames - 1, Math.round(s * FPS));
  const out = path.join(dir, `${nome}-q${quadro}.png`);
  await renderStill({composition: comp, serveUrl: servir, frame: quadro, output: out, scale: escala, imageFormat: 'png'});
  arquivos.push(out);
  console.log(nome, 'q', quadro);
}

const cols = Math.min(6, arquivos.length);
const linhas = Math.ceil(arquivos.length / cols);
const folha = new PNG({width: cols * (cw + 8), height: linhas * (ch + 8)});
folha.data.fill(40);
arquivos.forEach((a, i) => {
  const img = PNG.sync.read(fs.readFileSync(a));
  PNG.bitblt(img, folha, 0, 0, img.width, img.height, (i % cols) * (cw + 8) + 4, Math.floor(i / cols) * (ch + 8) + 4);
});
const destino = path.resolve(PROJ, 'saida', arg ? 'contato-quadros.png' : 'contato.png');
fs.writeFileSync(destino, PNG.sync.write(folha));
console.log('folha:', destino);
