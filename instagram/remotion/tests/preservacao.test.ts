import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {PNG} from 'pngjs';
import {afterAll, beforeAll, describe, expect, it} from 'vitest';
import {compararRegiao} from '../src/verificacao/preservacao';

// Caminho resolvido a partir do arquivo de teste, nao do cwd: o teste tem que
// passar rodando de qualquer diretorio.
const fixture = (nome: string) =>
  fileURLToPath(new URL(`./fixtures/${nome}`, import.meta.url));

const PACOTE = fixture('pacote.png');
const PACOTE_1PX = fixture('pacote-1px.png');

const QUADRO = {x: 0, y: 0, largura: 64, altura: 64};

// Fixtures de alfa sao geradas em disco temporario, nao no repositorio: elas
// existem so para provar a regra de mascara e nao sao material de referencia.
let tmp: string;

/** Grava um PNG 64x64 cujos canais vem de uma funcao por pixel. */
function gravar(
  nome: string,
  cor: (x: number, y: number) => [number, number, number, number],
): string {
  const p = new PNG({width: 64, height: 64});
  for (let y = 0; y < 64; y++) {
    for (let x = 0; x < 64; x++) {
      const i = (64 * y + x) << 2;
      const [r, g, b, a] = cor(x, y);
      p.data[i] = r;
      p.data[i + 1] = g;
      p.data[i + 2] = b;
      p.data[i + 3] = a;
    }
  }
  const destino = path.join(tmp, nome);
  fs.writeFileSync(destino, PNG.sync.write(p));
  return destino;
}

beforeAll(() => {
  tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'canastra-preservacao-'));
});

afterAll(() => {
  fs.rmSync(tmp, {recursive: true, force: true});
});

describe('compararRegiao', () => {
  it('acusa zero diferenca entre uma imagem e ela mesma', async () => {
    const r = await compararRegiao(PACOTE, PACOTE, QUADRO);
    expect(r.pixelsDiferentes).toBe(0);
    expect(r.maiorDelta).toBe(0);
    expect(r.total).toBe(64 * 64);
  });

  it('acusa diferenca quando um pixel muda', async () => {
    const r = await compararRegiao(PACOTE, PACOTE_1PX, QUADRO);
    expect(r.pixelsDiferentes).toBeGreaterThan(0);
    expect(r.pixelsDiferentes).toBe(1);
    expect(r.maiorDelta).toBe(200); // R de 200 para 0
  });

  // Se a implementacao comparar a imagem inteira em vez da regiao, este teste
  // e o unico que denuncia: o pixel estragado fica fora do recorte.
  it('compara so a regiao pedida, nao a imagem inteira', async () => {
    const r = await compararRegiao(PACOTE, PACOTE_1PX,
      {x: 1, y: 0, largura: 63, altura: 64});
    expect(r.pixelsDiferentes).toBe(0);
    expect(r.total).toBe(63 * 64);
  });

  it('ignora o pixel cujo alfa na origem nao e 255', async () => {
    // metade de cima transparente e com RGB totalmente diferente; metade de
    // baixo opaca e identica. So a metade opaca entra na conta.
    const origem = gravar('origem-alfa.png', (_x, y) =>
      y < 32 ? [200, 180, 150, 0] : [200, 180, 150, 255]);
    const saida = gravar('saida-alfa.png', (_x, y) =>
      y < 32 ? [10, 20, 30, 0] : [200, 180, 150, 255]);

    const r = await compararRegiao(origem, saida, QUADRO);
    expect(r.pixelsDiferentes).toBe(0);
    expect(r.maiorDelta).toBe(0);
    expect(r.considerados).toBe(32 * 64);
    expect(r.total).toBe(64 * 64);
  });

  it('alfa parcial na origem tambem fica fora da mascara', async () => {
    const origem = gravar('origem-alfa254.png', () => [200, 180, 150, 254]);
    const saida = gravar('saida-alfa254.png', () => [0, 0, 0, 254]);
    const r = await compararRegiao(origem, saida, QUADRO);
    expect(r.considerados).toBe(0);
    expect(r.pixelsDiferentes).toBe(0);
  });

  it('acusa perda de opacidade mesmo com o RGB intacto', async () => {
    const origem = gravar('origem-opaca.png', () => [200, 180, 150, 255]);
    const saida = gravar('saida-vazada.png', (_x, y) =>
      y < 8 ? [200, 180, 150, 128] : [200, 180, 150, 255]);
    const r = await compararRegiao(origem, saida, QUADRO);
    expect(r.pixelsAlfaPerdido).toBe(8 * 64);
    expect(r.pixelsDiferentes).toBe(8 * 64);
    expect(r.maiorDelta).toBe(0); // o RGB nao mudou; o que mudou foi o alfa
  });

  it('respeita a tolerancia', async () => {
    const origem = gravar('origem-tol.png', () => [200, 180, 150, 255]);
    const saida = gravar('saida-tol.png', () => [202, 180, 150, 255]);
    expect((await compararRegiao(origem, saida, QUADRO, 2)).pixelsDiferentes).toBe(0);
    expect((await compararRegiao(origem, saida, QUADRO, 1)).pixelsDiferentes).toBe(64 * 64);
    expect((await compararRegiao(origem, saida, QUADRO, 1)).maiorDelta).toBe(2);
  });

  it('falha alto quando a regiao sai do quadro', async () => {
    await expect(compararRegiao(PACOTE, PACOTE,
      {x: 0, y: 0, largura: 65, altura: 64})).rejects.toThrow();
    await expect(compararRegiao(PACOTE, PACOTE,
      {x: -1, y: 0, largura: 10, altura: 10})).rejects.toThrow();
    await expect(compararRegiao(PACOTE, PACOTE,
      {x: 0, y: 0, largura: 0, altura: 10})).rejects.toThrow();
  });

  it('falha alto quando o arquivo nao existe', async () => {
    await expect(compararRegiao(PACOTE, fixture('nao-existe.png'), QUADRO))
      .rejects.toThrow();
  });
});
