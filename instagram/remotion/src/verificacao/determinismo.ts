// Portao 3: determinismo.
//
// Renderiza o MESMO frame duas vezes e exige o mesmo md5. E o portao mais
// barato e o mais importante do motor, porque e ele que transforma "a peca
// ficou boa" em "a peca e reproduzivel".
//
// O que ele pega, e que nenhum olho pega:
//
//   - `Math.random()` sem semente, `Date.now()`, `new Date()` em animacao;
//   - fonte que carrega por rede e as vezes chega depois do frame;
//   - `useEffect` que depende de ordem de layout;
//   - decodificacao de video que nao cai no mesmo frame da fonte.
//
// Qualquer um desses faz o render de terca sair diferente do de segunda com o
// mesmo commit -- e entao nao existe mais versao aprovada, so o arquivo que
// alguem baixou.
//
// A comparacao e de BYTE, nao de pixel: dois PNG identicos em pixel mas escritos
// com filtro diferente teriam md5 diferente, e isso tambem e uma variacao a
// investigar. Quando os hashes divergem, o laudo desce ao pixel para dizer se a
// diferenca e de imagem ou so de codificacao -- as duas causas pedem conserto
// diferente.
//
// Este modulo nao renderiza: recebe `renderStill` por parametro. Alem de
// destravar o type stripping do Node (ver o cabecalho de `folha.ts`), isso deixa
// o portao testavel sem abrir o Chrome.

import crypto from 'node:crypto';
import fs from 'node:fs';
import {PNG} from 'pngjs';

export type LaudoDeterminismo = {
  frame: number;
  a: string;
  b: string;
  hashA: string;
  hashB: string;
  igual: boolean;
  bytes: {a: number; b: number};
  /** So quando os hashes divergem. `null` quando sao iguais. */
  pixel: {
    diferentes: number;
    total: number;
    maiorDelta: number;
    mesmaDimensao: boolean;
  } | null;
};

/** md5 do arquivo inteiro, em hex. */
export function md5Arquivo(caminho: string): string {
  let bruto: Buffer;
  try {
    bruto = fs.readFileSync(caminho);
  } catch (e) {
    // Falha alto: um portao que "passa" porque nao achou o arquivo e pior que
    // um portao que reprova.
    throw new Error(`nao consegui ler ${caminho}: ${(e as Error).message}`);
  }
  return crypto.createHash('md5').update(bruto).digest('hex');
}

/**
 * Onde dois PNG divergem em pixel.
 *
 * Existe para separar "a imagem mudou" de "so a codificacao do PNG mudou".
 * Dimensao diferente tambem e resposta: significa que a composicao mudou de
 * tamanho entre as duas rodadas.
 */
export function diferencaDePixel(
  a: string,
  b: string,
): {
  diferentes: number;
  total: number;
  maiorDelta: number;
  mesmaDimensao: boolean;
} {
  const x = PNG.sync.read(fs.readFileSync(a));
  const y = PNG.sync.read(fs.readFileSync(b));
  if (x.width !== y.width || x.height !== y.height) {
    return {
      diferentes: -1,
      total: x.width * x.height,
      maiorDelta: -1,
      mesmaDimensao: false,
    };
  }
  let diferentes = 0;
  let maiorDelta = 0;
  for (let i = 0; i < x.data.length; i += 4) {
    const d = Math.max(
      Math.abs(x.data[i] - y.data[i]),
      Math.abs(x.data[i + 1] - y.data[i + 1]),
      Math.abs(x.data[i + 2] - y.data[i + 2]),
      Math.abs(x.data[i + 3] - y.data[i + 3]),
    );
    if (d > maiorDelta) maiorDelta = d;
    if (d > 0) diferentes++;
  }
  return {
    diferentes,
    total: x.width * x.height,
    maiorDelta,
    mesmaDimensao: true,
  };
}

/**
 * Renderiza o mesmo frame duas vezes e compara.
 *
 * @param renderStill funcao que grava o still do frame no caminho dado
 * @param frame       o frame a sondar; escolha um com legenda na tela e
 *                    movimento em curso -- um frame preto passa em qualquer
 *                    motor, inclusive num quebrado
 * @param a, b        os dois PNG de saida
 */
export async function conferirDeterminismo({
  renderStill,
  frame,
  a,
  b,
}: {
  renderStill: (saida: string, frame: number) => Promise<unknown>;
  frame: number;
  a: string;
  b: string;
}): Promise<LaudoDeterminismo> {
  if (!Number.isInteger(frame) || frame < 0) {
    throw new Error(`frame tem que ser inteiro >= 0, veio ${frame}`);
  }
  if (a === b) {
    // Comparar um arquivo com ele mesmo passaria sempre. Seria um portao que
    // nunca reprova, o que e pior que nao ter portao.
    throw new Error(`as duas saidas tem que ser arquivos diferentes: ${a}`);
  }

  await renderStill(a, frame);
  await renderStill(b, frame);

  const hashA = md5Arquivo(a);
  const hashB = md5Arquivo(b);
  const igual = hashA === hashB;

  return {
    frame,
    a,
    b,
    hashA,
    hashB,
    igual,
    bytes: {a: fs.statSync(a).size, b: fs.statSync(b).size},
    pixel: igual ? null : diferencaDePixel(a, b),
  };
}
