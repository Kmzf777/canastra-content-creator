import {execFile} from 'node:child_process';
import fs from 'node:fs';
import {createRequire} from 'node:module';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {promisify} from 'node:util';

const exec = promisify(execFile);
const require_ = createRequire(import.meta.url);

export type Sonda = {
  /** largura de EXIBICAO, ja com a rotacao aplicada */
  largura: number;
  /** altura de EXIBICAO, ja com a rotacao aplicada */
  altura: number;
  /** rotacao do displaymatrix em graus (0 quando nao ha) */
  rotacao: number;
  /** largura/altura de EXIBICAO */
  razao: number;
  /** segundos */
  duracao: number;
  /** r_frame_rate: a taxa nominal do container */
  fps: number;
  /** avg_frame_rate: a taxa media real, que costuma diferir da nominal */
  fpsMedio: number;
  /** dimensao como esta gravada no container, antes da rotacao */
  codificada: {largura: number; altura: number};
  /** o binario que respondeu, para o relato de falha */
  ffprobe: string;
};

/**
 * Nomes dos pacotes de compositor que o Remotion publica por plataforma.
 * Cada um traz `ffprobe` junto. Este projeto roda em win32-x64, mas a lista
 * evita que a sondagem quebre em outra maquina.
 */
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

function binarioEm(dir: string): string | null {
  for (const nome of ['ffprobe.exe', 'ffprobe']) {
    const p = path.join(dir, nome);
    if (fs.existsSync(p)) return p;
  }
  return null;
}

/**
 * Sobe a arvore procurando `node_modules/@remotion/compositor-*`. Rede de
 * seguranca para layouts de node_modules que o require.resolve nao alcanca.
 */
function varrerNodeModules(): string | null {
  let dir = path.dirname(fileURLToPath(import.meta.url));
  for (let i = 0; i < 8; i++) {
    const escopo = path.join(dir, 'node_modules', '@remotion');
    if (fs.existsSync(escopo)) {
      for (const nome of fs.readdirSync(escopo)) {
        if (!nome.startsWith('compositor-')) continue;
        const bin = binarioEm(path.join(escopo, nome));
        if (bin) return bin;
      }
    }
    const pai = path.dirname(dir);
    if (pai === dir) break;
    dir = pai;
  }
  return null;
}

let cache: string | null = null;

/**
 * Onde esta o ffprobe.
 *
 * `ffprobe` NAO esta no PATH desta maquina, e `execFile('npx', ...)` devolve
 * ENOENT no Windows porque o npx e um `.cmd` (medido: 30/09/2026). Entao
 * resolvemos o binario que o proprio Remotion traz e chamamos por caminho
 * absoluto. Sem shell, sem npx.
 */
export function caminhoFfprobe(): string {
  if (cache) return cache;

  const doAmbiente = process.env.CANASTRA_FFPROBE;
  if (doAmbiente) {
    if (!fs.existsSync(doAmbiente)) {
      throw new Error(`CANASTRA_FFPROBE aponta para nada: ${doAmbiente}`);
    }
    return (cache = doAmbiente);
  }

  for (const pacote of candidatosDePacote()) {
    try {
      const pkg = require_.resolve(`${pacote}/package.json`);
      const bin = binarioEm(path.dirname(pkg));
      if (bin) return (cache = bin);
    } catch {
      // pacote de outra plataforma nao instalado: segue
    }
  }

  const varrido = varrerNodeModules();
  if (varrido) return (cache = varrido);

  throw new Error(
    'ffprobe nao encontrado. Ele vem com o Remotion em ' +
      'node_modules/@remotion/compositor-*; rode `npm install` ou aponte ' +
      'CANASTRA_FFPROBE para um ffprobe.',
  );
}

type FluxoFfprobe = {
  codec_type?: string;
  width?: number;
  height?: number;
  duration?: string;
  r_frame_rate?: string;
  avg_frame_rate?: string;
  side_data_list?: {rotation?: number}[];
};

function taxa(bruta: string | undefined): number {
  if (!bruta) return 0;
  const [num, den] = bruta.split('/').map(Number);
  if (!Number.isFinite(num)) return 0;
  if (den === undefined || !Number.isFinite(den)) return num;
  return den === 0 ? 0 : num / den;
}

/**
 * Le a dimensao REAL de um video, honrando o displaymatrix.
 *
 * A dimensao codificada mente: `pl.mp4` esta gravado 1024x576 com
 * `rotation -90`, logo exibe 576x1024 (9:16 nativo). Ler width/height do
 * container e renderizar por eles deita a peca inteira.
 */
export async function sondar(caminho: string): Promise<Sonda> {
  const absoluto = path.resolve(caminho);
  if (!fs.existsSync(absoluto)) {
    throw new Error(`arquivo nao encontrado: ${absoluto}`);
  }

  const ffprobe = caminhoFfprobe();
  let stdout: string;
  try {
    ({stdout} = await exec(
      ffprobe,
      [
        '-v',
        'error',
        '-print_format',
        'json',
        '-show_streams',
        '-show_format',
        absoluto,
      ],
      {maxBuffer: 16 * 1024 * 1024},
    ));
  } catch (e) {
    throw new Error(
      `ffprobe falhou em ${absoluto} (binario: ${ffprobe}): ${
        (e as Error).message
      }`,
    );
  }

  let j: {streams?: FluxoFfprobe[]; format?: {duration?: string}};
  try {
    j = JSON.parse(stdout);
  } catch {
    throw new Error(`ffprobe devolveu JSON invalido para ${absoluto}`);
  }

  const v = (j.streams ?? []).find((s) => s.codec_type === 'video');
  if (!v) throw new Error(`sem faixa de video em ${absoluto}`);
  if (!v.width || !v.height) {
    throw new Error(`ffprobe nao devolveu dimensao para ${absoluto}`);
  }

  // A rotacao vem no side_data_list do tipo Display Matrix, em graus e com
  // sinal. Aplicamos nos: o ffprobe NAO reflete a rotacao em stream=width.
  const rotacaoBruta = Number(
    v.side_data_list?.find((s) => s.rotation !== undefined)?.rotation ?? 0,
  );
  const rotacao = Number.isFinite(rotacaoBruta) ? rotacaoBruta : 0;
  const normalizada = ((Math.round(rotacao) % 360) + 360) % 360;
  const trocado = normalizada === 90 || normalizada === 270;

  const largura = trocado ? v.height : v.width;
  const altura = trocado ? v.width : v.height;

  const fps = taxa(v.r_frame_rate);
  const fpsMedio = taxa(v.avg_frame_rate) || fps;

  return {
    largura,
    altura,
    rotacao,
    razao: largura / altura,
    duracao: Number(v.duration ?? j.format?.duration ?? 0),
    fps,
    fpsMedio,
    codificada: {largura: v.width, altura: v.height},
    ffprobe,
  };
}
