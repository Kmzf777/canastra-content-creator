import fs from 'node:fs';
import {PNG} from 'pngjs';

/**
 * Laudo de preservacao de pixel.
 *
 * Este e o portao que impede o motor de estragar o rotulo da embalagem. A
 * regra da marca e dura: nenhum efeito pode alterar pixel dentro da
 * embalagem (ver `src/identidade/proibicoes.md`). Um glow, um
 * `<CameraMotionBlur>` ou uma correcao de cor local passa despercebido no
 * olho e destroi a tipografia pequena -- e tipografia pequena e exatamente
 * onde a fidelidade morre.
 *
 * A comparacao e feita canal a canal, em RGB, **somente onde o alfa da
 * origem e 255**. O alfa 255 e a mascara do corpo solido da embalagem: pixel
 * semitransparente e borda de recorte, onde a cor legitimamente se mistura
 * com o fundo novo e comparar RGB acusaria falso positivo.
 */
export type Regiao = {x: number; y: number; largura: number; altura: number};

export type Laudo = {
  /** Pixels que fugiram da tolerancia (RGB) ou perderam opacidade. */
  pixelsDiferentes: number;
  /** Maior diferenca de canal RGB entre os pixels considerados. */
  maiorDelta: number;
  /** Pixels da regiao pedida: `largura * altura`. */
  total: number;
  /** Pixels da regiao com alfa 255 na origem -- os que entraram na conta. */
  considerados: number;
  /** Considerados cujo alfa na saida deixou de ser 255. Ja contam em `pixelsDiferentes`. */
  pixelsAlfaPerdido: number;
};

const OPACO = 255;

function ler(caminho: string): PNG {
  // Falha alto de proposito: um laudo que "passa" porque nao achou o arquivo e
  // pior que um laudo que reprova.
  let bruto: Buffer;
  try {
    bruto = fs.readFileSync(caminho);
  } catch (e) {
    throw new Error(`nao consegui ler o PNG ${caminho}: ${(e as Error).message}`);
  }
  return PNG.sync.read(bruto);
}

function validar(r: Regiao, a: PNG, b: PNG): void {
  for (const [nome, v] of Object.entries(r)) {
    if (!Number.isInteger(v)) {
      throw new Error(`regiao.${nome} tem que ser inteiro, veio ${v}`);
    }
  }
  if (r.largura < 1 || r.altura < 1) {
    throw new Error(`regiao vazia: ${r.largura}x${r.altura}`);
  }
  if (r.x < 0 || r.y < 0) {
    throw new Error(`regiao com origem negativa: x=${r.x} y=${r.y}`);
  }
  for (const [nome, img] of [['origem', a], ['saida', b]] as const) {
    if (r.x + r.largura > img.width || r.y + r.altura > img.height) {
      throw new Error(
        `regiao ${r.x},${r.y} ${r.largura}x${r.altura} sai do quadro da ` +
        `${nome} (${img.width}x${img.height})`,
      );
    }
  }
}

/**
 * Compara a regiao entre a foto de origem e o frame de saida.
 *
 * @param origem    PNG da embalagem como ela e.
 * @param saida     PNG do frame renderizado.
 * @param r         Regiao em coordenadas de pixel, igual nas duas imagens.
 * @param tolerancia Delta de canal aceito **sem** contar como diferenca.
 *                   O padrao e 0: sobre a embalagem, a regra e pixel exato.
 */
export async function compararRegiao(
  origem: string,
  saida: string,
  r: Regiao,
  tolerancia = 0,
): Promise<Laudo> {
  const a = ler(origem);
  const b = ler(saida);
  validar(r, a, b);

  let pixelsDiferentes = 0;
  let maiorDelta = 0;
  let considerados = 0;
  let pixelsAlfaPerdido = 0;

  for (let y = r.y; y < r.y + r.altura; y++) {
    for (let x = r.x; x < r.x + r.largura; x++) {
      const ia = (a.width * y + x) << 2;
      const ib = (b.width * y + x) << 2;

      // A mascara e o alfa da ORIGEM: fora dela o pixel nao e embalagem.
      if (a.data[ia + 3] !== OPACO) continue;
      considerados++;

      const d = Math.max(
        Math.abs(a.data[ia] - b.data[ib]),
        Math.abs(a.data[ia + 1] - b.data[ib + 1]),
        Math.abs(a.data[ia + 2] - b.data[ib + 2]),
      );
      if (d > maiorDelta) maiorDelta = d;

      // Perder opacidade tambem e estragar a embalagem, mesmo com o RGB
      // intacto: o pixel passou a deixar o fundo atravessar.
      const alfaPerdido = b.data[ib + 3] !== OPACO;
      if (alfaPerdido) pixelsAlfaPerdido++;
      if (d > tolerancia || alfaPerdido) pixelsDiferentes++;
    }
  }

  return {
    pixelsDiferentes,
    maiorDelta,
    total: r.largura * r.altura,
    considerados,
    pixelsAlfaPerdido,
  };
}
