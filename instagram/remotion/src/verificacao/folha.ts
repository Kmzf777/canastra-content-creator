// Portao 1: folha de contato.
//
// Amostra o video inteiro a 2 quadros por segundo e monta um mosaico. O objetivo
// nao e automatico: e por o filme todo numa imagem para o olho humano achar o
// frame quebrado, a legenda fora da area segura, o corte errado. Nenhum teste
// programatico substitui isso.
//
// ---------------------------------------------------------------------------
// POR QUE O MOSAICO E MONTADO EM NODE E NAO PELO FFMPEG
//
// O plano pedia:
//
//   npx remotion ffmpeg -i reel.mp4 -vf "fps=2,scale=180:-1,tile=6x8" ...
//
// Isso NAO roda. O ffmpeg que vem dentro do Remotion
// (`@remotion/compositor-*/ffmpeg.exe`) e uma build minima: medido em
// 30/09/2026, ela publica 50 linhas de `-filters` e nao tem nem `fps` nem
// `tile`. A mensagem que ela devolve para `fps=2` e enganosa --
// "No option name near '2'", que parece erro de sintaxe e nao ausencia de
// filtro; so `fps=fps=2` revela o "No such filter: 'fps'".
//
// Entao a extracao usa `-r`, que e opcao de saida e nao filtro, e a colagem das
// celulas acontece aqui com `pngjs`. Bonus: o mosaico fica deterministico e o
// tamanho da celula vem medido do PNG extraido, nao presumido.
//
// ---------------------------------------------------------------------------
// POR QUE ESTE MODULO NAO IMPORTA NADA DO PROJETO
//
// Os tres portoes sao carregados por `scripts/conferir.mjs`, que roda em Node
// com `--experimental-strip-types`. O type stripping do Node nao adivinha
// extensao: `from '../identidade/tokens'` nao resolve, e `from
// '../identidade/tokens.ts'` explode no `tsc` porque
// `allowImportingTsExtensions` esta desligado no `tsconfig.json`. Logo: aqui
// entra so `node:` e `pngjs`. Se um dia um portao precisar dos tokens, o jeito
// certo e passar o valor por parametro, nao importar.

import {execFile} from 'node:child_process';
import fs from 'node:fs';
import {createRequire} from 'node:module';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {promisify} from 'node:util';
import {PNG} from 'pngjs';

const exec = promisify(execFile);
const require_ = createRequire(import.meta.url);

/** Amostragem padrao: 2 quadros por segundo, 6 celulas de largura, celula de 180 px. */
export const PADRAO = {fpsAmostra: 2, colunas: 6, larguraCelula: 180} as const;

/** Cor da calha entre celulas. Escura de proposito: separa sem competir com o frame. */
const CALHA = {r: 20, g: 16, b: 13, largura: 2} as const;

export type Grade = {colunas: number; linhas: number; quadros: number};

export type Folha = {
  saida: string;
  grade: Grade;
  /** dimensao de cada celula, MEDIDA no PNG extraido */
  celula: {largura: number; altura: number};
  /** dimensao final do mosaico */
  mosaico: {largura: number; altura: number};
  /** o binario que fez a extracao, para o relato de falha */
  ffmpeg: string;
};

// ---------------------------------------------------------------------------
// ffmpeg

function binarioEm(dir: string, nomes: string[]): string | null {
  for (const nome of nomes) {
    const p = path.join(dir, nome);
    if (fs.existsSync(p)) return p;
  }
  return null;
}

function candidatosDePacote(): string[] {
  const {platform, arch} = process;
  if (platform === 'win32') return [`@remotion/compositor-win32-${arch}-msvc`];
  if (platform === 'darwin') return [`@remotion/compositor-darwin-${arch}`];
  if (platform === 'linux') {
    return [
      `@remotion/compositor-linux-${arch}-gnu`,
      `@remotion/compositor-linux-${arch}-musl`,
    ];
  }
  return [];
}

function varrerNodeModules(nomes: string[]): string | null {
  let dir = path.dirname(fileURLToPath(import.meta.url));
  for (let i = 0; i < 8; i++) {
    const escopo = path.join(dir, 'node_modules', '@remotion');
    if (fs.existsSync(escopo)) {
      for (const nome of fs.readdirSync(escopo)) {
        if (!nome.startsWith('compositor-')) continue;
        const bin = binarioEm(path.join(escopo, nome), nomes);
        if (bin) return bin;
      }
    }
    const pai = path.dirname(dir);
    if (pai === dir) break;
    dir = pai;
  }
  return null;
}

let cacheFfmpeg: string | null = null;

/**
 * Onde esta o ffmpeg.
 *
 * Mesma historia do `caminhoFfprobe()` em `src/motor/sondar.ts`: `ffmpeg` nao
 * esta no PATH desta maquina e `execFile('npx', ...)` devolve ENOENT no Windows
 * porque `npx` e um `.cmd`. Resolvemos o binario que o proprio Remotion baixou e
 * chamamos por caminho absoluto, sem shell.
 *
 * A duplicacao em relacao a `sondar.ts` e deliberada: ver o cabecalho deste
 * arquivo sobre por que os portoes nao importam modulos do projeto.
 */
export function caminhoFfmpeg(): string {
  if (cacheFfmpeg) return cacheFfmpeg;

  const doAmbiente = process.env.CANASTRA_FFMPEG;
  if (doAmbiente) {
    if (!fs.existsSync(doAmbiente)) {
      throw new Error(`CANASTRA_FFMPEG aponta para nada: ${doAmbiente}`);
    }
    return (cacheFfmpeg = doAmbiente);
  }

  const nomes = ['ffmpeg.exe', 'ffmpeg'];
  for (const pacote of candidatosDePacote()) {
    try {
      const pkg = require_.resolve(`${pacote}/package.json`);
      const bin = binarioEm(path.dirname(pkg), nomes);
      if (bin) return (cacheFfmpeg = bin);
    } catch {
      // pacote de outra plataforma nao instalado: segue
    }
  }

  const varrido = varrerNodeModules(nomes);
  if (varrido) return (cacheFfmpeg = varrido);

  throw new Error(
    'ffmpeg nao encontrado. Ele vem com o Remotion em ' +
      'node_modules/@remotion/compositor-*; rode `npm install` ou aponte ' +
      'CANASTRA_FFMPEG para um ffmpeg.',
  );
}

/** Roda o ffmpeg do Remotion e falha alto com a mensagem dele. */
export async function ffmpeg(args: string[], rotulo: string): Promise<void> {
  const bin = caminhoFfmpeg();
  try {
    await exec(bin, args, {maxBuffer: 32 * 1024 * 1024});
  } catch (e) {
    const err = e as {stderr?: string; message?: string};
    throw new Error(
      `${rotulo} falhou (${bin}): ${(err.stderr ?? err.message ?? '').trim()}`,
    );
  }
}

// ---------------------------------------------------------------------------
// grade

/**
 * ESTIMATIVA de quantos quadros a amostragem rende. Nao e exato de proposito.
 *
 * O `-r` do ffmpeg e conversao de taxa, nao um relogio: ele entrega um quadro a
 * cada 1/fps de midia incluindo o instante zero (`floor + 1`), mas o ultimo
 * quadro cai ou nao dentro da duracao conforme o arredondamento do pts. Medido
 * em 30/09/2026: `reel.mp4` tem 23,20 s, a formula preve 47 e o ffmpeg entregou
 * **48**.
 *
 * Por isso quem usa este numero compara com TOLERANCIA (ver `folhaDeContato`).
 * Ele serve para pegar duracao grosseiramente errada -- uma sonda que devolveu
 * os segundos de outro arquivo --, nunca para validar a contagem exata.
 */
export function quadrosEsperados({
  duracaoS,
  fpsAmostra = PADRAO.fpsAmostra,
}: {
  duracaoS: number;
  fpsAmostra?: number;
}): number {
  if (!(duracaoS > 0)) throw new Error(`duracao invalida: ${duracaoS}`);
  if (!(fpsAmostra > 0)) throw new Error(`fpsAmostra invalido: ${fpsAmostra}`);
  return Math.floor(duracaoS * fpsAmostra) + 1;
}

/** Fecha a grade: as colunas sao escolhidas, as linhas sao consequencia. */
export function gradeDeContato({
  quadros,
  colunas = PADRAO.colunas,
}: {
  quadros: number;
  colunas?: number;
}): Grade {
  if (!Number.isInteger(quadros) || quadros < 1) {
    throw new Error(`quadros tem que ser inteiro >= 1, veio ${quadros}`);
  }
  if (!Number.isInteger(colunas) || colunas < 1) {
    throw new Error(`colunas tem que ser inteiro >= 1, veio ${colunas}`);
  }
  return {colunas, linhas: Math.ceil(quadros / colunas), quadros};
}

// ---------------------------------------------------------------------------
// mosaico

function colar(destino: PNG, origem: PNG, dx: number, dy: number): void {
  if (dx < 0 || dy < 0) throw new Error(`colagem negativa: ${dx},${dy}`);
  if (dx + origem.width > destino.width || dy + origem.height > destino.height) {
    throw new Error(
      `celula ${origem.width}x${origem.height} em ${dx},${dy} nao cabe no ` +
        `mosaico ${destino.width}x${destino.height}`,
    );
  }
  const bytesLinha = origem.width * 4;
  for (let y = 0; y < origem.height; y++) {
    const inicio = y * origem.width * 4;
    origem.data.copy(
      destino.data,
      ((dy + y) * destino.width + dx) * 4,
      inicio,
      inicio + bytesLinha,
    );
  }
}

function pintar(img: PNG, cor: {r: number; g: number; b: number}): void {
  for (let i = 0; i < img.data.length; i += 4) {
    img.data[i] = cor.r;
    img.data[i + 1] = cor.g;
    img.data[i + 2] = cor.b;
    img.data[i + 3] = 255;
  }
}

/**
 * Monta a folha de contato de um video.
 *
 * @param video         mp4 de entrada
 * @param saida         PNG do mosaico
 * @param duracaoS      duracao do video em segundos (vem de `sondar()`)
 * @param fpsAmostra    quadros por segundo de midia amostrados
 * @param colunas       celulas por linha
 * @param larguraCelula largura de cada celula em px; a altura sai da razao
 */
export async function folhaDeContato({
  video,
  saida,
  duracaoS,
  fpsAmostra = PADRAO.fpsAmostra,
  colunas = PADRAO.colunas,
  larguraCelula = PADRAO.larguraCelula,
}: {
  video: string;
  saida: string;
  duracaoS: number;
  fpsAmostra?: number;
  colunas?: number;
  larguraCelula?: number;
}): Promise<Folha> {
  if (!fs.existsSync(video)) throw new Error(`video nao encontrado: ${video}`);

  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'canastra-folha-'));
  try {
    // `-r` e opcao de SAIDA (conversao de taxa), nao filtro. E o que sobra numa
    // build de ffmpeg sem o filtro `fps`. `h=-2` mantem a altura par; para PNG
    // nao importa, mas mantem a celula utilizavel em qualquer reencode futuro.
    await ffmpeg(
      [
        '-y',
        '-v',
        'error',
        '-i',
        path.resolve(video),
        '-r',
        String(fpsAmostra),
        '-vf',
        `scale=w=${larguraCelula}:h=-2`,
        '-an',
        path.join(temp, 'q_%05d.png'),
      ],
      'extracao de quadros da folha de contato',
    );

    const arquivos = fs
      .readdirSync(temp)
      .filter((n) => n.endsWith('.png'))
      .sort();
    if (arquivos.length === 0) {
      throw new Error(
        `a extracao nao gerou nenhum quadro de ${video}. Confira se o arquivo ` +
          'tem faixa de video.',
      );
    }

    const grade = gradeDeContato({quadros: arquivos.length, colunas});

    const primeira = PNG.sync.read(fs.readFileSync(path.join(temp, arquivos[0])));
    const celula = {largura: primeira.width, altura: primeira.height};

    const passoX = celula.largura + CALHA.largura;
    const passoY = celula.altura + CALHA.largura;
    const mosaico = {
      largura: grade.colunas * passoX - CALHA.largura,
      altura: grade.linhas * passoY - CALHA.largura,
    };

    const grande = new PNG({width: mosaico.largura, height: mosaico.altura});
    pintar(grande, CALHA);

    for (let i = 0; i < arquivos.length; i++) {
      const img =
        i === 0
          ? primeira
          : PNG.sync.read(fs.readFileSync(path.join(temp, arquivos[i])));
      if (img.width !== celula.largura || img.height !== celula.altura) {
        throw new Error(
          `quadro ${arquivos[i]} saiu ${img.width}x${img.height}, esperado ` +
            `${celula.largura}x${celula.altura}`,
        );
      }
      colar(
        grande,
        img,
        (i % grade.colunas) * passoX,
        Math.floor(i / grade.colunas) * passoY,
      );
    }

    fs.mkdirSync(path.dirname(path.resolve(saida)), {recursive: true});
    fs.writeFileSync(saida, PNG.sync.write(grande));

    // Conferencia de sanidade da DURACAO, nao da contagem. A tolerancia e 2
    // quadros porque o arredondamento do `-r` ja custou 1 no arquivo real
    // (previsto 47, entregue 48) e apertar isso transformaria o portao num
    // alarme falso. O que queremos pegar e a duracao de outro arquivo, que
    // erraria por dezenas.
    const TOLERANCIA = 2;
    const previsto = quadrosEsperados({duracaoS, fpsAmostra});
    if (Math.abs(previsto - grade.quadros) > TOLERANCIA) {
      throw new Error(
        `a folha extraiu ${grade.quadros} quadros mas ${duracaoS}s a ` +
          `${fpsAmostra}fps preveem ${previsto}. A duracao informada nao ` +
          'descreve este arquivo.',
      );
    }

    return {saida, grade, celula, mosaico, ffmpeg: caminhoFfmpeg()};
  } finally {
    fs.rmSync(temp, {recursive: true, force: true});
  }
}

// ---------------------------------------------------------------------------
// loop

/**
 * Portao 4: emenda de loop.
 *
 * Concatena o video com ele mesmo por remux (`-c copy`, sem reencode) para que
 * a emenda seja assistida como o Instagram a exibe. Um reel que reinicia limpo
 * ganha reexibicao; um que da um pulo na volta perde o espectador ali.
 *
 * Vive neste modulo, e nao num `loop.ts`, porque e o outro portao que fala
 * ffmpeg e a Tarefa 8 do plano nomeia so tres arquivos de verificacao.
 */
export async function emendaDeLoop({
  video,
  saida,
  voltas = 1,
}: {
  video: string;
  saida: string;
  voltas?: number;
}): Promise<{saida: string; bytes: number; voltas: number}> {
  if (!fs.existsSync(video)) throw new Error(`video nao encontrado: ${video}`);
  if (!Number.isInteger(voltas) || voltas < 1) {
    throw new Error(`voltas tem que ser inteiro >= 1, veio ${voltas}`);
  }
  fs.mkdirSync(path.dirname(path.resolve(saida)), {recursive: true});
  await ffmpeg(
    [
      '-y',
      '-v',
      'error',
      '-stream_loop',
      String(voltas),
      '-i',
      path.resolve(video),
      '-c',
      'copy',
      path.resolve(saida),
    ],
    'remux de loop',
  );
  return {saida, bytes: fs.statSync(saida).size, voltas};
}
