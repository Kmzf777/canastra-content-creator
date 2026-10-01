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
  /**
   * De onde a rotacao veio, e quantos graus.
   *
   * POR QUE NAO E SO UM NUMERO. Um `0` que significa "nao achei metadado" e um
   * `0` que significa "medi e e zero" sao fatos diferentes, e um deles e um
   * alarme: se a fonte e `nenhuma` num JPEG de camera, ou a foto foi reescrita
   * por um editor que apagou o EXIF, ou o `Orientation` esta la e nao foi lido.
   * Devolver `0` nos dois casos foi exatamente como o defeito de 01/10/2026
   * passou despercebido.
   */
  rotacao: {fonte: 'displaymatrix' | 'exif' | 'nenhuma'; graus: number};
  /** largura/altura de EXIBICAO */
  razao: number;
  /** `true` quando o fluxo tem um frame so (`format_name === 'image2'`) */
  imagemParada: boolean;
  /**
   * segundos. `null` em imagem parada: o 0,04 do ffprobe e do demuxer, nao do
   * arquivo.
   */
  duracao: number | null;
  /**
   * r_frame_rate: a taxa nominal do container. `null` em imagem parada: os
   * 25 fps que o ffprobe devolve para `image2` sao ficcao.
   */
  fps: number | null;
  /**
   * avg_frame_rate: a taxa media real, que costuma diferir da nominal. `null`
   * em imagem parada.
   */
  fpsMedio: number | null;
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

/** O EXIF nao vem no fluxo: vem nas TAGS DO FRAME. */
type FrameFfprobe = {tags?: Record<string, string>};
type FormatoFfprobe = {duration?: string; format_name?: string};

/**
 * EXIF `Orientation` -> graus de rotacao no sentido do displaymatrix.
 *
 * A tabela EXIF tem 8 valores; 2, 4, 5 e 7 incluem espelhamento, que este motor
 * NAO aplica -- ele so troca largura por altura quando preciso. Espelhar uma
 * foto de produto trocaria o lado do rotulo, e isso e alteracao de arte, nao de
 * enquadramento.
 *
 * 5, 6, 7 e 8 trocam os eixos. E so isso que a dimensao de exibicao precisa
 * saber.
 */
const GRAUS_DO_ORIENTATION: Record<number, number> = {
  1: 0,
  2: 0,
  3: 180,
  4: 180,
  5: 90,
  6: 90,
  7: 270,
  8: 270,
};

function taxa(bruta: string | undefined): number {
  if (!bruta) return 0;
  const [num, den] = bruta.split('/').map(Number);
  if (!Number.isFinite(num)) return 0;
  if (den === undefined || !Number.isFinite(den)) return num;
  return den === 0 ? 0 : num / den;
}

/**
 * Le a dimensao de EXIBICAO de um video OU de uma foto, honrando os DOIS
 * metadados de rotacao que existem.
 *
 * A dimensao codificada mente, e mente por duas tecnologias diferentes:
 *
 * - `pl.mp4` esta gravado 1024x576 com `displaymatrix rotation -90`, logo exibe
 *   576x1024 (9:16 nativo).
 * - `Classico (5).jpg` esta gravado 4096x2304 com EXIF `Orientation 6`, logo
 *   exibe 2304x4096 (razao 0,5625, nao 1,7778).
 *
 * Ler width/height do container e renderizar por eles deita a peca inteira. Ate
 * 01/10/2026 esta funcao lia so o `side_data_list.rotation` -- que e metadado de
 * CONTAINER DE VIDEO -- e por isso respondia sobre foto com tres erros ao mesmo
 * tempo: razao errada, `rotacao: 0` num Orientation 6, e `fps: 25` / `duracao:
 * 0.04` inventados pelo demuxer `image2` para um arquivo parado.
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
        // O EXIF vem nas TAGS DO FRAME, nao do fluxo. `%+#1` pede UM frame:
        // medido, e e o mesmo binario que ja estava aqui, sem dependencia nova.
        '-show_frames',
        '-read_intervals',
        '%+#1',
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

  let j: {
    streams?: FluxoFfprobe[];
    frames?: FrameFfprobe[];
    format?: FormatoFfprobe;
  };
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

  // IMAGEM PARADA. Medido em 01/10/2026: `format_name` e `image2` para JPEG e
  // para PNG, e `mov,mp4,m4a,3gp,3g2,mj2` para o `pl.mp4`. Para todo `image2` o
  // ffprobe devolve `r_frame_rate: 25/1` e `duration: 0.040000` -- os dois sao
  // artefato do demuxer e nao medida do arquivo.
  const imagemParada = (j.format?.format_name ?? '') === 'image2';

  // ROTACAO, por DOIS metadados, nesta ordem de prioridade.
  //
  // O displaymatrix vence porque, quando os dois existem, ele e o que o
  // container de video declara e e o que um player honra. Na pratica eles nao
  // coexistem: medido, `pl.mp4` tem displaymatrix e nenhum `Orientation`, e os
  // JPEG tem `Orientation` e nenhum side_data.
  const rotacao = ((): Sonda['rotacao'] => {
    const bruto = v.side_data_list?.find((s) => s.rotation !== undefined)
      ?.rotation;
    if (bruto !== undefined && Number.isFinite(Number(bruto))) {
      return {fonte: 'displaymatrix', graus: Number(bruto)};
    }
    // O ffprobe devolve o Orientation PREENCHIDO DE ESPACOS (`"    6"`,
    // medido). `Number()` sobre a string resolve; comparacao de string
    // falharia em silencio, e silencio aqui e a razao de o defeito ter durado
    // tres rodadas.
    const cru = j.frames?.[0]?.tags?.Orientation;
    const n = cru === undefined ? NaN : Number(String(cru).trim());
    if (Number.isFinite(n) && n in GRAUS_DO_ORIENTATION) {
      return {fonte: 'exif', graus: GRAUS_DO_ORIENTATION[n]};
    }
    return {fonte: 'nenhuma', graus: 0};
  })();

  const normalizada = ((Math.round(rotacao.graus) % 360) + 360) % 360;
  const trocado = normalizada === 90 || normalizada === 270;

  const largura = trocado ? v.height : v.width;
  const altura = trocado ? v.width : v.height;

  const fps = imagemParada ? null : taxa(v.r_frame_rate);
  const fpsMedio = imagemParada ? null : taxa(v.avg_frame_rate) || fps;
  const duracao = imagemParada
    ? null
    : Number(v.duration ?? j.format?.duration ?? 0);

  return {
    largura,
    altura,
    rotacao,
    razao: largura / altura,
    imagemParada,
    duracao,
    fps,
    fpsMedio,
    codificada: {largura: v.width, altura: v.height},
    ffprobe,
  };
}
