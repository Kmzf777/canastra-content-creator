// C3: OS EVENTOS DE TEXTO SAO UMA LISTA POR CENA.
//
// O QUE ISTO SUBSTITUI
//
// `PecaVideo.tsx` declarava `manchete?: Manchete | null` -- UM texto por PECA inteira.
// Medido na peca real: 91,4% do tempo sem nenhuma camada alem da legenda, com
// `proibicoes.md:11-12` proibindo tempo morto. Singular nao era limitacao de
// implementacao, era o desenho -- e com ele as series "infografico", "voce-sabia" e
// "arraste" do catalogo nao sao expressaveis.
//
// Este arquivo prova o que a LISTA compra, em numero: varios eventos por cena, cada um
// com janela propria, cada um com a cadencia do SEU papel, e o conflito de pista virando
// recusa em vez de sobreposicao silenciosa.
import {describe, expect, it} from 'vitest';
import {compilar} from '../src/briefing/compilar';
import {zBriefing} from '../src/briefing/esquema';
import {refinar} from '../src/briefing/refinar';
import {janelaDoEventoNaPeca} from '../src/motor/tempo-de-cena';

function peca(eventos: unknown[], duracaoS = 8) {
  return zBriefing.parse({
    _esquema: 'canastra-briefing/1',
    serie: 'infografico',
    formatos: ['9:16'],
    duracao: {modo: 'somaCenas'},
    cenas: [{duracaoS, fonte: {tipo: 'cor', cor: '#3B2A1F'}, eventos}],
    transicoes: [],
    audio: {locucao: {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 0}, trilha: null},
    gancho: 'g',
    cta: 'c',
  });
}

describe('varios eventos na MESMA cena', () => {
  it('tres eventos entram, e cada um tem a janela que declarou', () => {
    const p = compilar(
      peca([
        {papel: 'manchete', texto: 'PRIMEIRO', entradaS: 0, pista: 'topo'},
        {papel: 'dado', texto: '38 FOTOS', entradaS: 2.5, pista: 'principal'},
        {papel: 'etiqueta', texto: 'MEDEIROS 1250 M', entradaS: 5, pista: 'topo'},
      ]),
    );
    expect(p.cenas[0].eventos).toHaveLength(3);
    expect(p.cenas[0].eventos.map((e) => e.inicioFrames)).toEqual([0, 75, 150]);
    // As tres janelas existem e cada uma tem duracao propria.
    for (let i = 0; i < 3; i++) {
      const j = janelaDoEventoNaPeca(p, 0, i);
      expect(j.ate, `evento ${i}`).toBeGreaterThan(j.de);
    }
  });

  it('cada evento carrega a familia e a cadencia DO PAPEL DELE, na mesma cena', () => {
    // E isto que a lista compra sobre o singular: a cena mistura papeis, e o motor nao
    // precisa escolher um so para a peca inteira.
    const p = compilar(
      peca([
        {papel: 'manchete', texto: 'PRIMEIRO', entradaS: 0, pista: 'topo'},
        {papel: 'dado', texto: '38 FOTOS', entradaS: 2.5, pista: 'principal'},
        {papel: 'etiqueta', texto: 'MEDEIROS 1250 M', entradaS: 5, pista: 'topo'},
      ]),
    );
    const [m, d, e] = p.cenas[0].eventos;
    expect([m.familia, d.familia, e.familia]).toEqual(['manchete', 'dado', 'dado']);
    expect([m.cadenciaTexto, d.cadenciaTexto, e.cadenciaTexto]).toEqual([
      'palavra',
      'linha',
      'bloco',
    ]);
    // A etiqueta de 3 PALAVRAS tem 1 irmao: e a divergencia de 6 frames que o plano e
    // a tela tinham entre si.
    expect(e.irmaos).toBe(1);
    expect(m.irmaos).toBe(1); // 'PRIMEIRO' e uma palavra so
  });

  it('lista VAZIA e cena completa, sem erro e sem placeholder', () => {
    // Mas o refinador cobra: cena sem evento E sem legenda e tempo morto.
    const b = peca([]);
    const p = compilar(
      zBriefing.parse({
        ...b,
        licencas: {...b.licencas, aceitaTempoMorto: true, justificativa: 'plano de fundo deliberado'},
      }),
    );
    expect(p.cenas[0].eventos).toEqual([]);
    expect(refinar(b).map((r) => r.codigo)).toContain('tempo-morto');
  });

  it('dois eventos na MESMA pista ao mesmo tempo e RECUSA, nao sobreposicao', () => {
    // O defeito que a pista existe para transformar em erro: no motor antigo a caixa da
    // manchete se intersectava com a da legenda em 90,20 px no 1:1 sem ninguem
    // reclamar.
    const recusas = refinar(
      peca([
        {papel: 'manchete', texto: 'UM DOIS TRES', entradaS: 0, pista: 'topo'},
        {papel: 'etiqueta', texto: 'MEDEIROS 1250 M', entradaS: 0.1, pista: 'topo'},
      ]),
    );
    expect(recusas.map((r) => r.codigo)).toContain('pista-ocupada');
  });

  it('as MESMAS duas camadas em pistas que nao conflitam passam', () => {
    const recusas = refinar(
      peca([
        {papel: 'manchete', texto: 'UM DOIS TRES', entradaS: 0, pista: 'topo'},
        {papel: 'dado', texto: '38 FOTOS', entradaS: 0.1, pista: 'principal'},
      ]),
    );
    expect(recusas.map((r) => r.codigo)).not.toContain('pista-ocupada');
  });

  it('evento que estoura o fim da cena e RECUSA, com os tres numeros', () => {
    // O stagger empurra o fim junto com o comeco, entao a ultima palavra sumiria por
    // corte em vez de sair.
    const recusas = refinar(
      peca([{papel: 'manchete', texto: 'UMA FRASE BEM LONGA DE SEIS', entradaS: 1.8, pista: 'topo'}], 2),
    );
    const r = recusas.find((x) => x.codigo === 'evento-estoura-cena');
    expect(r).toBeDefined();
    expect(r!.mensagem).toMatch(/entra no frame 54/);
    expect(r!.mensagem).toMatch(/a cena tem 60/);
  });

  it('DOIS acentos na mesma cena e recusa: proibicoes.md pede UM', () => {
    const recusas = refinar(
      peca([
        {papel: 'manchete', texto: 'UM DOIS', entradaS: 0, pista: 'topo', palavraAcento: 0},
        {papel: 'dado', texto: '38 FOTOS', entradaS: 2, pista: 'principal', palavraAcento: 0},
      ]),
    );
    expect(recusas.map((r) => r.codigo)).toContain('dois-acentos');
  });
});

describe('eventos espalhados por CENAS diferentes', () => {
  it('cada cena tem a sua lista, e as janelas somam o inicio da cena certa', () => {
    const b = zBriefing.parse({
      _esquema: 'canastra-briefing/1',
      serie: 'jornada',
      formatos: ['9:16'],
      duracao: {modo: 'somaCenas'},
      cenas: [
        {
          duracaoS: 4,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [{papel: 'manchete', texto: 'LAVOURA', entradaS: 0, pista: 'topo'}],
        },
        {
          duracaoS: 6,
          fonte: {tipo: 'cor', cor: '#4A5D3A'},
          eventos: [
            {papel: 'manchete', texto: 'TERREIRO', entradaS: 0, pista: 'topo'},
            {papel: 'dado', texto: '1250 M', entradaS: 3, pista: 'principal'},
          ],
        },
      ],
      transicoes: [{tipo: 'corte'}],
      audio: {locucao: {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 0}, trilha: null},
      gancho: 'g',
      cta: 'c',
    });
    const p = compilar(b);
    expect(p.cenas.map((c) => c.eventos.length)).toEqual([1, 2]);
    // O evento da cena 1 e cena-relativo (90 frames = 3 s) e a janela na PECA soma os
    // 120 frames da cena 0.
    expect(p.cenas[1].eventos[1].inicioFrames).toBe(90);
    expect(janelaDoEventoNaPeca(p, 1, 1).de).toBe(120 + 90);
  });

  it('o diagnostico relata UM registro por evento por formato', () => {
    const b = zBriefing.parse({
      _esquema: 'canastra-briefing/1',
      serie: 'jornada',
      formatos: ['9:16', '1:1'],
      duracao: {modo: 'somaCenas'},
      cenas: [
        {
          duracaoS: 8,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [
            {papel: 'manchete', texto: 'LAVOURA', entradaS: 0, pista: 'tela'},
            // O texto e o de `projetos/02-jornada-do-grao`, e nao um `1250 M` curto.
            // Medido em 01/10/2026: `1250 M` em `dado`/`principal` nao tem corpo
            // valido no 1:1 -- no teto de linha (corpo 174 px) a mancha e 8,971% e o
            // piso do 1:1 e 12,198%. O refinador recusa com `sem-corpo-valido`, e e o
            // teste logo abaixo que prova isso. Aqui o assunto e o diagnostico.
            {papel: 'dado', texto: '1.235–1.272 M · EXIF', entradaS: 4, pista: 'principal'},
          ],
        },
      ],
      transicoes: [],
      audio: {locucao: {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 0}, trilha: null},
      gancho: 'g',
      cta: 'c',
    });
    const p = compilar(b);
    expect(p.diagnostico.eventos).toHaveLength(2);
    for (const d of p.diagnostico.eventos) {
      expect(Object.keys(d.porFormato).sort()).toEqual(['1:1', '9:16']);
      for (const f of Object.values(d.porFormato)) {
        expect(f.porque.length).toBeGreaterThan(20);
        expect(f.corpo).toBeGreaterThan(8);
      }
    }
  });

  it('texto curto que nao alcanca o piso nem no teto e `sem-corpo-valido`, POR FORMATO', () => {
    // O defeito do teto, pelo lado do briefing: `1250 M` como `dado` dominante tem
    // corpo valido no 9:16 e NAO tem no 1:1. A recusa nomeia o formato, porque mandar
    // consertar um texto que esta certo em dois dos tres formatos seria mentir sobre
    // onde esta o problema.
    const comum = {
      _esquema: 'canastra-briefing/1',
      serie: 'jornada',
      duracao: {modo: 'somaCenas'},
      cenas: [
        {
          duracaoS: 8,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [{papel: 'dado', texto: '1250 M', entradaS: 0, pista: 'principal'}],
        },
      ],
      transicoes: [],
      audio: {locucao: {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 0}, trilha: null},
      gancho: 'g',
      cta: 'c',
    };

    const so916 = refinar(zBriefing.parse({...comum, formatos: ['9:16']}));
    expect(so916.map((x) => x.codigo)).not.toContain('sem-corpo-valido');

    const com11 = refinar(zBriefing.parse({...comum, formatos: ['9:16', '1:1']}));
    const r = com11.find((x) => x.codigo === 'sem-corpo-valido');
    expect(r, 'o 1:1 tem que recusar').toBeDefined();
    expect(r!.campo).toBe('cenas[0].eventos[0]');
    expect(r!.mensagem).toMatch(/formato 1:1/);
    expect(r!.mensagem).toMatch(/NAO HA CORPO VALIDO/);
    // E a mensagem traz os DOIS numeros, para quem le saber o quanto falta.
    expect(r!.mensagem).toMatch(/8,971%/);
    expect(r!.mensagem).toMatch(/12,198%/);
  });
});
