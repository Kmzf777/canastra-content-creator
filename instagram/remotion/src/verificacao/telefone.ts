// Portao 2: teste de telefone.
//
// Renderiza a peca no tamanho em que ela vai ser vista de verdade -- 360 px de
// largura -- e nao no tamanho em que foi desenhada. Se a legenda nao se le a
// 360 px, ela nao se le no feed de ninguem. Fonte de 78 px sobre 1080 vira 26 px
// aqui, e e nesse numero que se decide.
//
// ---------------------------------------------------------------------------
// A ARMADILHA DO `--scale`: SUCESSO COM PROPORCAO ERRADA
//
// O plano pedia `--scale=0.333`. Roda, sai exit 0, e o arquivo esta errado.
// Medido em 30/09/2026 sobre a composicao `Reel` (1080x1920):
//
//   --scale=0.333              still -> 360x639   render -> 360x638
//   --scale=0.3333333333333333 still -> 360x640   render -> 360x640
//
// 1080 * 0,333 = 359,64 e 1920 * 0,333 = 639,36. O still arredonda e aceita
// altura impar; o h264 nao aceita, entao o render **desce 639 para 638 em
// silencio**. 360/638 = 0,5643, e 9:16 e 0,5625: a peca sai esticada 0,3% na
// vertical, sem aviso e sem erro. E a licao 3 do CLAUDE.md de novo -- exit 0 nao
// prova que o parametro fez o que se queria.
//
// Por isso a escala nunca e digitada: ela e DERIVADA da largura alvo por
// `escalaParaLargura()`, que recusa qualquer combinacao que nao caia em duas
// dimensoes pares.
//
// ---------------------------------------------------------------------------
// Este modulo tambem e a camada de invocacao do CLI do Remotion para os outros
// portoes -- `determinismo.ts` recebe `renderizarStill` por parametro em vez de
// importa-lo, porque os portoes rodam sob o type stripping do Node, que nao
// resolve import local sem extensao (ver o cabecalho de `folha.ts`).

import {spawn} from 'node:child_process';
import fs from 'node:fs';
import {createRequire} from 'node:module';
import path from 'node:path';

const require_ = createRequire(import.meta.url);

/** Largura em que um Reel e realmente assistido num telefone. */
export const LARGURA_TELEFONE = 360;

export type Escala = {
  /** o numero a passar em `--scale` */
  escala: number;
  largura: number;
  altura: number;
};

// ---------------------------------------------------------------------------
// CLI

let cacheCli: string | null = null;

/**
 * Onde esta o `remotion-cli.js`.
 *
 * Nao usamos `npx`: no Windows ele e um `.cmd` e `spawn` sem shell devolve
 * ENOENT. Resolvemos o script declarado em `bin` do `@remotion/cli` e o
 * executamos com o proprio Node (`process.execPath`).
 */
export function caminhoRemotionCli(): string {
  if (cacheCli) return cacheCli;

  const doAmbiente = process.env.CANASTRA_REMOTION_CLI;
  if (doAmbiente) {
    if (!fs.existsSync(doAmbiente)) {
      throw new Error(`CANASTRA_REMOTION_CLI aponta para nada: ${doAmbiente}`);
    }
    return (cacheCli = doAmbiente);
  }

  const pkgPath = require_.resolve('@remotion/cli/package.json');
  const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8')) as {
    bin?: Record<string, string> | string;
  };
  const relativo =
    typeof pkg.bin === 'string' ? pkg.bin : pkg.bin?.remotion;
  if (!relativo) {
    throw new Error(`@remotion/cli nao declara bin.remotion em ${pkgPath}`);
  }
  const bin = path.join(path.dirname(pkgPath), relativo);
  if (!fs.existsSync(bin)) {
    throw new Error(`bin.remotion aponta para nada: ${bin}`);
  }
  return (cacheCli = bin);
}

/**
 * Roda o CLI do Remotion com a saida dele herdada no terminal.
 *
 * Herdada de proposito: um render pode levar minutos e um portao que fica mudo
 * parece travado. E o progresso do Remotion e a unica pista de onde ele parou
 * quando para.
 */
export async function remotion(args: string[], rotulo: string): Promise<void> {
  const cli = caminhoRemotionCli();
  await new Promise<void>((ok, nok) => {
    const p = spawn(process.execPath, [cli, ...args], {
      stdio: 'inherit',
      cwd: process.cwd(),
    });
    p.on('error', (e) => nok(new Error(`${rotulo}: ${e.message}`)));
    p.on('close', (codigo) => {
      if (codigo === 0) return ok();
      nok(new Error(`${rotulo} saiu com codigo ${codigo}`));
    });
  });
}

// ---------------------------------------------------------------------------
// escala

/**
 * Deriva a escala a partir da largura alvo e recusa dimensao impar.
 *
 * A recusa e o ponto do portao. O h264 exige largura e altura pares; quando o
 * calculo cai em impar o Remotion arredonda para baixo sozinho e a proporcao
 * muda sem que nada reclame. Melhor falhar aqui, de graca, que descobrir depois
 * de um render de vinte minutos.
 */
export function escalaParaLargura({
  larguraBase,
  alturaBase,
  larguraAlvo = LARGURA_TELEFONE,
}: {
  larguraBase: number;
  alturaBase: number;
  larguraAlvo?: number;
}): Escala {
  for (const [nome, v] of [
    ['larguraBase', larguraBase],
    ['alturaBase', alturaBase],
    ['larguraAlvo', larguraAlvo],
  ] as const) {
    if (!Number.isInteger(v) || v < 2) {
      throw new Error(`${nome} tem que ser inteiro >= 2, veio ${v}`);
    }
  }

  const escala = larguraAlvo / larguraBase;
  const largura = Math.round(larguraBase * escala);
  const altura = Math.round(alturaBase * escala);

  if (largura % 2 !== 0 || altura % 2 !== 0) {
    throw new Error(
      `escala ${escala} sobre ${larguraBase}x${alturaBase} da ` +
        `${largura}x${altura}, que tem lado impar. O h264 exige lado par e o ` +
        'Remotion arredonda para baixo em silencio, mudando a proporcao. ' +
        `Escolha outra larguraAlvo (${larguraAlvo} nao serve para esta ` +
        'composicao).',
    );
  }

  return {escala, largura, altura};
}

// ---------------------------------------------------------------------------
// renders

export type Alvo = {
  /** o entrypoint, normalmente `src/index.ts` */
  entrada: string;
  /** id da composicao registrada em `Raiz.tsx` */
  composicao: string;
  saida: string;
  /** caminho do props.json -- JSON inline NAO funciona no shell do Windows */
  props?: string;
  /** pasta publica do projeto: `projetos/<x>/public/` (fonte/ + assets/) */
  publicDir?: string;
  escala?: number;
};

function argsComuns(a: Alvo): string[] {
  const args = [a.entrada, a.composicao, a.saida];
  if (a.props) {
    if (!fs.existsSync(a.props)) {
      throw new Error(`props.json nao encontrado: ${a.props}`);
    }
    args.push(`--props=${a.props}`);
  }
  if (a.publicDir) args.push(`--public-dir=${a.publicDir}`);
  if (a.escala !== undefined) args.push(`--scale=${a.escala}`);
  args.push('--log=error');
  return args;
}

/** Renderiza um still. Usado pelo portao de determinismo. */
export async function renderizarStill(
  a: Alvo & {frame: number},
): Promise<string> {
  if (!Number.isInteger(a.frame) || a.frame < 0) {
    throw new Error(`frame tem que ser inteiro >= 0, veio ${a.frame}`);
  }
  fs.mkdirSync(path.dirname(path.resolve(a.saida)), {recursive: true});
  await remotion(
    ['still', ...argsComuns(a), `--frame=${a.frame}`],
    `still ${a.composicao} frame ${a.frame}`,
  );
  if (!fs.existsSync(a.saida)) {
    throw new Error(`o still saiu com codigo 0 mas ${a.saida} nao existe`);
  }
  return a.saida;
}

/** Renderiza video. `extras` passa argumentos crus do CLI, como `--frames=a-b`. */
export async function renderizarVideo(
  a: Alvo & {extras?: string[]},
): Promise<string> {
  fs.mkdirSync(path.dirname(path.resolve(a.saida)), {recursive: true});
  await remotion(
    ['render', ...argsComuns(a), ...(a.extras ?? [])],
    `render ${a.composicao}`,
  );
  if (!fs.existsSync(a.saida)) {
    throw new Error(`o render saiu com codigo 0 mas ${a.saida} nao existe`);
  }
  return a.saida;
}

export type LaudoTelefone = Escala & {
  saida: string;
  /** dimensao que o arquivo REALMENTE tem, medida depois do render */
  medido: {largura: number; altura: number};
  confere: boolean;
};

/**
 * Renderiza a peca a 360 px e confirma, medindo o arquivo, que saiu no tamanho
 * pedido.
 *
 * `medir` e injetado (use `sondar` de `src/motor/sondar.ts`) porque os portoes
 * nao importam modulos do projeto -- ver o cabecalho de `folha.ts`.
 */
export async function renderizarTelefone({
  larguraBase,
  alturaBase,
  larguraAlvo = LARGURA_TELEFONE,
  medir,
  ...alvo
}: Omit<Alvo, 'escala'> & {
  larguraBase: number;
  alturaBase: number;
  larguraAlvo?: number;
  medir: (caminho: string) => Promise<{largura: number; altura: number}>;
}): Promise<LaudoTelefone> {
  const e = escalaParaLargura({larguraBase, alturaBase, larguraAlvo});
  await renderizarVideo({...alvo, escala: e.escala});
  const m = await medir(alvo.saida);
  return {
    ...e,
    saida: alvo.saida,
    medido: {largura: m.largura, altura: m.altura},
    confere: m.largura === e.largura && m.altura === e.altura,
  };
}
