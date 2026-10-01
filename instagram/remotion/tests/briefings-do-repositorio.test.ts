// TODO BRIEFING DE EXEMPLO DO REPOSITORIO TEM QUE PASSAR NO REFINADOR.
//
// POR QUE ESTE ARQUIVO EXISTE
//
// `tests/briefing.test.ts` ja lia os briefings de 01 e 02 do disco -- mas so
// chamava `zBriefing.parse()`. zod valida FORMA, e `arquivo: z.string().min(1)`
// aceita felizmente `"jornada/IMG_1421.JPG"`. O SENTIDO mora em `refinar()`, que
// nenhum teste chamava sobre arquivo real. Resultado medido em 30/09/2026:
// `projetos/02-jornada-do-grao/briefing.json` passava na suite inteira e era
// RECUSADO com 3x `arquivo-com-caminho` na hora de compilar.
//
// Um briefing de exemplo que nao compila e pior que nenhum: ele e a prova de que
// o motor funciona, e provava o contrario. A suite verde nao denunciou porque
// ninguem testava o portao que recusa.
//
// POR QUE VARRE A PASTA EM VEZ DE NOMEAR OS DOIS
//
// Nomear 01 e 02 deixaria o 4o projeto, escrito na proxima sessao, fora da rede.
// A varredura pega qualquer `projetos/*/briefing.json` que nasca depois.
//
// E POR QUE O PISO DE CONTAGEM
//
// Licao 17 do CLAUDE.md: um seletor que nao encontra o alvo mas encontra ALGO e
// pior que um que falha. Aqui o risco e o seletor nao encontrar NADA -- se
// `projetos/` mudar de lugar, `readdirSync` devolve lista vazia e um `for` sobre
// lista vazia passa sem asserir nada: verde vazio. O piso e a asserssao de que a
// varredura de fato varreu, e os dois nomes exigidos sao os dois que a sessao de
// 30/09/2026 consertou.

import {readFileSync, readdirSync, existsSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {describe, expect, it} from 'vitest';
import {zBriefing} from '../src/briefing/esquema';
import {refinar} from '../src/briefing/refinar';
import {SUB} from '../src/motor/pasta-publica';

const RAIZ_PROJETOS = fileURLToPath(new URL('../projetos/', import.meta.url));

/** Os projetos que tem `briefing.json`, em ordem de nome. */
const projetos = readdirSync(RAIZ_PROJETOS, {withFileTypes: true})
  .filter((d) => d.isDirectory())
  .map((d) => d.name)
  .filter((nome) => existsSync(path.join(RAIZ_PROJETOS, nome, 'briefing.json')))
  .sort();

describe('a varredura encontrou os briefings', () => {
  it('acha pelo menos 2 e inclui os dois que a sessao consertou', () => {
    expect(projetos.length).toBeGreaterThanOrEqual(2);
    expect(projetos).toContain('01-private-label');
    expect(projetos).toContain('02-jornada-do-grao');
  });
});

describe.each(projetos)('projetos/%s/briefing.json', (nome) => {
  const cru = JSON.parse(
    readFileSync(path.join(RAIZ_PROJETOS, nome, 'briefing.json'), 'utf8'),
  );

  it('passa no esquema (FORMA)', () => {
    expect(() => zBriefing.parse(cru)).not.toThrow();
  });

  it('passa no refinador SEM NENHUMA RECUSA (SENTIDO)', () => {
    const recusas = refinar(zBriefing.parse(cru));
    // A mensagem do `expect` carrega codigo E campo: quem roda a suite em 2027 nao
    // deve ter que abrir o refinador para saber o que quebrou.
    expect(
      recusas.map((r) => `[${r.codigo}] ${r.campo}`),
      `${nome} tem ${recusas.length} recusa(s):\n` +
        recusas.map((r) => `  [${r.codigo}] ${r.campo}: ${r.mensagem}`).join('\n'),
    ).toEqual([]);
  });

  it('nenhum `fonte.arquivo` tem separador de pasta', () => {
    // Redundante com `arquivo-com-caminho` de proposito. O teste acima reprova a
    // LISTA inteira e nao diz qual regressao voltou; este nomeia a de 30/09/2026,
    // que e a que custou uma rodada. Vale para `audio` e `assets` tambem: os
    // quatro campos `arquivo` do esquema sao todos NOME, e `staticFile` monta o
    // prefixo por `SUB`.
    const b = zBriefing.parse(cru);
    const nomes: string[] = [];
    for (const c of b.cenas) {
      const f = c.fonte;
      if (f.tipo === 'video' || f.tipo === 'foto') nomes.push(f.arquivo);
      if (f.tipo === 'grade') {
        for (const cel of f.celulas) {
          if (cel.tipo === 'video' || cel.tipo === 'foto') nomes.push(cel.arquivo);
        }
      }
    }
    if (b.audio.locucao) nomes.push(b.audio.locucao.arquivo);
    if (b.audio.trilha) nomes.push(b.audio.trilha.arquivo);
    for (const a of b.assets) nomes.push(a.arquivo);

    expect(nomes.filter((n) => /[\/]/.test(n))).toEqual([]);
    // E o prefixo continua sendo do codigo, nao do briefing: se alguem renomear
    // `SUB.fonte`, um briefing que tenha embutido o prefixo antigo nao se cura.
    expect(SUB.fonte).toBe('fonte');
  });
});

describe('os arquivos que o briefing 02 nomeia estao PLANOS em public/fonte/', () => {
  // O refinador e PURO e nao toca disco: ele garante que o campo e um nome, nao que
  // o arquivo exista. Esta e a metade que falta, e e so para o 02, que e o exemplo
  // de FOTO -- os outros projetos tem material pesado gitignorado que pode nao
  // estar na maquina de quem roda a suite.
  const dir = path.join(RAIZ_PROJETOS, '02-jornada-do-grao', 'public', SUB.fonte);

  it.skipIf(!existsSync(dir))('as 3 fotos estao na raiz da pasta, sem subpasta', () => {
    const b = zBriefing.parse(
      JSON.parse(
        readFileSync(path.join(RAIZ_PROJETOS, '02-jornada-do-grao', 'briefing.json'), 'utf8'),
      ),
    );
    const fotos = b.cenas
      .map((c) => c.fonte)
      .filter((f) => f.tipo === 'foto')
      .map((f) => (f.tipo === 'foto' ? f.arquivo : ''));
    expect(fotos).toEqual(['IMG_1421.JPG', 'IMG_1424.JPG', 'IMG_1398.JPG']);
    for (const nome of fotos) {
      expect(existsSync(path.join(dir, nome)), `${nome} nao esta em ${dir}`).toBe(true);
    }
    // E nenhuma subpasta: a convencao medida em 30/09/2026 e pasta publica PLANA.
    const subpastas = readdirSync(dir, {withFileTypes: true}).filter((d) => d.isDirectory());
    expect(subpastas.map((d) => d.name)).toEqual([]);
  });
});
