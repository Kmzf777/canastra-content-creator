import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {describe, expect, it} from 'vitest';
import {sondar} from '../src/motor/sondar';

// Caminho resolvido a partir do arquivo de teste, nao do cwd: o teste tem que
// passar rodando de qualquer diretorio.
const PL = fileURLToPath(
  new URL('../projetos/01-private-label/public/fonte/pl.mp4', import.meta.url),
);

const T = 30_000; // sondar sobe um processo ffprobe; a primeira vez e mais lenta

describe('sondar', () => {
  it('devolve a dimensao de EXIBICAO, nao a codificada', async () => {
    const r = await sondar(PL);
    // o container diz 1024x576; o displaymatrix diz rotation -90
    expect(r.largura).toBe(576);
    expect(r.altura).toBe(1024);
    expect(r.rotacao).toBe(-90);
  }, T);

  it('calcula a razao a partir da dimensao de exibicao', async () => {
    const r = await sondar(PL);
    expect(r.razao).toBeCloseTo(9 / 16, 4);
  }, T);

  it('NAO devolve a dimensao codificada 1024x576', async () => {
    const r = await sondar(PL);
    expect([r.largura, r.altura]).not.toEqual([1024, 576]);
    expect(r.largura).toBeLessThan(r.altura); // retrato, nao paisagem
  }, T);

  it('devolve duracao e fps plausiveis', async () => {
    const r = await sondar(PL);
    expect(r.duracao).toBeCloseTo(24.33, 1);
    expect(r.fps).toBeCloseTo(30, 0);
    expect(r.fpsMedio).toBeCloseTo(29.96, 1);
  }, T);

  it('aceita caminho relativo ao cwd', async () => {
    // relativo calculado do cwd real: testa o suporte a caminho relativo sem
    // presumir de onde o vitest foi lancado
    const rel = path.relative(process.cwd(), PL);
    expect(path.isAbsolute(rel)).toBe(false);
    const r = await sondar(rel);
    expect(r.largura).toBe(576);
    expect(r.altura).toBe(1024);
  }, T);

  it('falha alto quando o arquivo nao existe', async () => {
    await expect(sondar('projetos/nao-existe.mp4')).rejects.toThrow();
  }, T);
});
