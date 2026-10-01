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
    // `rotacao` deixou de ser um numero: um `0` que significa "nao achei metadado"
    // e um `0` que significa "medi e e zero" sao fatos DIFERENTES, e um deles e um
    // alarme. Agora ela diz de onde veio.
    expect(r.rotacao.graus).toBe(-90);
    expect(r.rotacao.fonte).toBe('displaymatrix');
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

// ---------------------------------------------------------------------------
// FOTO. Tudo abaixo e o que `sondar()` errava em 01/10/2026: ele devolvia razao
// 1,7778 para um arquivo que exibe 0,5625, `rotacao: 0` num Orientation 6, e
// inventava `fps: 25` / `duracao: 0.04` para uma imagem parada.

// Os caminhos seguem a convencao que o arquivo JA usa (`PL`, linhas 8-10):
// resolvidos a partir do arquivo de teste com `fileURLToPath(new URL(...))`, para o
// teste passar rodando de qualquer diretorio. De `tests/` ate a raiz do repositorio
// sao TRES niveis: `tests/` -> `instagram/remotion/` -> `instagram/` -> raiz.
const cam = (rel: string) => fileURLToPath(new URL(rel, import.meta.url));
const PACKSHOT = cam(
  '../../../base-curada/01-real-verificada/torrefacao-uberlandia-875m/packshot-classico/Classico (5).jpg',
);
const FOTO_LAVOURA = cam(
  '../../../base-curada/01-real-verificada/fazenda-medeiros-1250m/cafezal/IMG_1398.JPG',
);
const RECORTE = cam('../projetos/01-private-label/public/assets/suave-250g.png');

describe('sondar sobre FOTO', () => {
  it('honra o EXIF Orientation 6: 4096x2304 gravado exibe 2304x4096', async () => {
    const r = await sondar(PACKSHOT);
    expect(r.codificada).toEqual({largura: 4096, altura: 2304});
    expect(r.largura).toBe(2304);
    expect(r.altura).toBe(4096);
    expect(r.razao).toBeCloseTo(0.5625, 6);
    expect(r.rotacao.fonte).toBe('exif');
    expect(r.rotacao.graus).toBe(90);
  }, T);

  it('Orientation 1 nao troca nada, e diz que MEDIU o zero', async () => {
    // A diferenca que o campo `{fonte, graus}` existe para fazer: aqui o zero foi
    // medido; num arquivo sem metadado nenhum ele seria `fonte: 'nenhuma'`.
    const r = await sondar(FOTO_LAVOURA);
    expect(r.largura).toBe(4032);
    expect(r.altura).toBe(3024);
    expect(r.razao).toBeCloseTo(4 / 3, 6);
    expect(r.rotacao.fonte).toBe('exif');
    expect(r.rotacao.graus).toBe(0);
  }, T);

  it('NAO inventa fps nem duracao para imagem parada', async () => {
    // O ffprobe devolve `r_frame_rate: 25/1` e `duration: 0.040000` para todo
    // `image2`, e os dois sao artefato do demuxer, nao medida do arquivo. Numero
    // inventado e pior que ausencia -- licao 3 do CLAUDE.md.
    const r = await sondar(FOTO_LAVOURA);
    expect(r.duracao).toBeNull();
    expect(r.fps).toBeNull();
    expect(r.fpsMedio).toBeNull();
    expect(r.imagemParada).toBe(true);
  }, T);

  it('o recorte de embalagem publicado esta DEITADO e sem Orientation', async () => {
    // O caso (2) do padrao: os tres PNG de `public/assets/` sao 4096x2304 deitados e
    // o `Orientation 6` da origem NAO esta no arquivo -- ele foi perdido na
    // publicacao. Este teste e o que impede alguem de "consertar" isso supondo que o
    // metadado esteja la esperando.
    const r = await sondar(RECORTE);
    expect(r.codificada).toEqual({largura: 4096, altura: 2304});
    expect(r.largura).toBe(4096);
    expect(r.rotacao.fonte).toBe('nenhuma');
    expect(r.rotacao.graus).toBe(0);
    expect(r.imagemParada).toBe(true);
  }, T);

  it('video continua com fps e duracao, e imagemParada e false', async () => {
    const r = await sondar(PL);
    expect(r.imagemParada).toBe(false);
    expect(r.duracao).not.toBeNull();
    expect(r.fps).not.toBeNull();
  }, T);
});
