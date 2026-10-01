// PORTAO 0: o selo do plano.
//
// Este arquivo testa o COMPARADOR, nao o hash. O hash ja tem prova em
// `briefing.test.ts` (ele ve o que esta aninhado). O que nunca teve prova, porque nunca
// existiu, e quem LE o selo de volta: `scripts/compilar.mjs` selava todo plano e nada
// no repositorio comparava. Ver o cabecalho de `src/verificacao/selo.ts`.
//
// O teste central e o item 3 do pedido: dois briefings que diferem SO no texto de um
// evento DENTRO de uma cena tem que dar vereditos diferentes no PORTAO -- nao basta o
// hash distingui-los se o portao nunca for consultado.

import {mkdtempSync, writeFileSync, mkdirSync, readFileSync} from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {describe, expect, it} from 'vitest';
import {zBriefing} from '../src/briefing/esquema';
import {sha256Do, sha256DoPlano, selarPlano} from '../src/briefing/impressao';
import {conferirSelo, conferirSeloDoProjeto} from '../src/verificacao/selo';

const MINIMO = {
  _esquema: 'canastra-briefing/1',
  serie: 'avulsa',
  formatos: ['9:16'],
  duracao: {modo: 'somaCenas'},
  transicoes: [{tipo: 'corte'}],
  audio: {locucao: {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 0}, trilha: null},
  gancho: 'o gancho desta peca de teste',
  cta: 'chama no direct',
};

/** Um briefing valido com DUAS cenas, para variar texto em profundidade 3. */
function briefing(textoDaSegundaCena = 'TRES') {
  return zBriefing.parse({
    ...MINIMO,
    cenas: [
      {
        duracaoS: 23.2,
        fonte: {tipo: 'cor', cor: '#3B2A1F'},
        eventos: [{papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'topo'}],
      },
      {
        duracaoS: 6,
        fonte: {tipo: 'cor', cor: '#4A5D3A'},
        eventos: [{papel: 'manchete', texto: textoDaSegundaCena, entradaS: 0, pista: 'topo'}],
      },
    ],
  });
}

describe('conferirSelo', () => {
  it('APROVA o plano selado com o proprio briefing', () => {
    const b = briefing();
    const plano = selarPlano({_sha256Briefing: ''}, b);
    const laudo = conferirSelo(b, plano);
    expect(laudo.bate).toBe(true);
    expect(laudo.motivo).toBeNull();
    expect(laudo.esperado).toBe(laudo.encontrado);
    expect(laudo.esperado).toMatch(/^[0-9a-f]{64}$/);
  });

  it('REPROVA quando os briefings diferem SO no texto de um evento DENTRO de uma cena', () => {
    // O caso que o bug original deixava passar: `JSON.stringify` com allowlist de
    // chaves de topo serializava `cenas` como `[{},{}]`, entao estes dois briefings
    // davam o MESMO hash e o portao -- se existisse -- aprovaria o plano errado.
    //
    // A diferenca aqui esta em profundidade 3: cenas[1].eventos[0].texto. Nada mais
    // muda: mesma duracao, mesma cor, mesma faixa, mesmo gancho, mesmo cta.
    const original = briefing('TRES');
    const alterado = briefing('OUTRO TEXTO INTEIRAMENTE');

    // o plano foi selado com o ORIGINAL e esta sendo conferido contra o ALTERADO,
    // que e exatamente o que acontece quando alguem edita o briefing e nao recompila
    const plano = selarPlano({_sha256Briefing: ''}, original);

    const contraOriginal = conferirSelo(original, plano);
    const contraAlterado = conferirSelo(alterado, plano);

    expect(contraOriginal.bate).toBe(true);
    expect(contraAlterado.bate).toBe(false);
    expect(contraAlterado.motivo).toMatch(/NAO veio deste briefing/);
    // e a prova de que a diferenca e so essa: trocar o texto de volta reaprova
    expect(conferirSelo(briefing('TRES'), plano).bate).toBe(true);
    // e a prova de que o achatador antigo confundiria os dois
    const antigo = (v: object) => JSON.stringify(v, Object.keys(v).sort());
    expect(antigo(original)).toBe(antigo(alterado));
  });

  it('REPROVA plano NAO SELADO: string vazia nao e passe livre', () => {
    // `compilar()` devolve `_sha256Briefing: ''` por ser puro, e `PLANO_VAZIO` em
    // `Raiz.tsx` tambem. Se vazio passasse, apagar o campo a mao seria o jeito mais
    // facil de desligar o portao.
    const b = briefing();
    const vazio = conferirSelo(b, {_sha256Briefing: ''});
    expect(vazio.bate).toBe(false);
    expect(vazio.motivo).toMatch(/nao esta SELADO/);
    expect(vazio.motivo).toMatch(/vazio/);

    for (const ruim of [{}, {_sha256Briefing: null}, {_sha256Briefing: 123}]) {
      const l = conferirSelo(b, ruim as {_sha256Briefing?: unknown});
      expect(l.bate).toBe(false);
      expect(l.motivo).toMatch(/nao esta SELADO/);
    }
  });

  it('REPROVA mudanca em campo de TOPO tambem', () => {
    const plano = selarPlano({_sha256Briefing: ''}, briefing());
    const outroCta = zBriefing.parse({...MINIMO, cenas: briefing().cenas, cta: 'outro cta'});
    expect(conferirSelo(outroCta, plano).bate).toBe(false);
  });

  it('o laudo carrega os DOIS hashes, para o portao poder imprimir a divergencia', () => {
    const original = briefing('TRES');
    const alterado = briefing('OUTRO');
    const plano = selarPlano({_sha256Briefing: ''}, original);
    const l = conferirSelo(alterado, plano);
    expect(l.encontrado).toBe(sha256Do(original));
    expect(l.esperado).toBe(sha256Do(alterado));
    expect(l.esperado).not.toBe(l.encontrado);
  });
});

describe('conferirSeloDoProjeto -- a casca de I/O', () => {
  /** Escreve um projeto de mentira em tmp e devolve o caminho. */
  function projeto(briefingCru: unknown, plano: unknown) {
    const dir = mkdtempSync(path.join(os.tmpdir(), 'canastra-selo-'));
    mkdirSync(dir, {recursive: true});
    writeFileSync(path.join(dir, 'briefing.json'), JSON.stringify(briefingCru), 'utf8');
    writeFileSync(path.join(dir, 'plano.json'), JSON.stringify(plano), 'utf8');
    return dir;
  }

  it('HASHEIA O BRIEFING PARSEADO, nao o JSON cru -- senao nenhum plano legitimo passa', () => {
    // A armadilha que este portao tem que repetir de proposito: `compilar.mjs` sela
    // `zBriefing.parse(cru)`, e o esquema tem 7 `.default()`. O arquivo em disco nao
    // tem `fps`, `licencas` nem `assets`; o objeto selado tem os tres. Hashear o cru
    // daria um hash que nunca bate.
    const cru = {
      ...MINIMO,
      cenas: [
        {
          duracaoS: 23.2,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [{papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'topo'}],
        },
      ],
    };
    const parseado = zBriefing.parse(cru);
    // o selo nasce do PARSEADO, como em `scripts/compilar.mjs`
    const plano = selarPlano({_sha256Briefing: ''}, parseado);

    const dir = projeto(cru, plano);
    const l = conferirSeloDoProjeto(dir);
    expect(l.bate).toBe(true);

    // e a prova de que o cru e o parseado NAO tem o mesmo hash: se um dia alguem
    // "simplificar" o portao para hashear o arquivo cru, este expect cai
    expect(sha256Do(cru)).not.toBe(sha256Do(parseado));
    expect(l.caminhoBriefing).toContain('briefing.json');
    expect(l.caminhoPlano).toContain('plano.json');
  });

  it('REPROVA quando o briefing em disco mudou depois do compile', () => {
    const antes = briefing('TRES');
    const plano = selarPlano({_sha256Briefing: ''}, antes);
    // o briefing em disco tem o texto NOVO; o plano foi selado com o antigo
    const cruNovo = {
      ...MINIMO,
      cenas: [
        {
          duracaoS: 23.2,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [{papel: 'manchete', texto: 'UM', entradaS: 0, pista: 'topo'}],
        },
        {
          duracaoS: 6,
          fonte: {tipo: 'cor', cor: '#4A5D3A'},
          eventos: [{papel: 'manchete', texto: 'MUDEI A MAO', entradaS: 0, pista: 'topo'}],
        },
      ],
    };
    const l = conferirSeloDoProjeto(projeto(cruNovo, plano));
    expect(l.bate).toBe(false);
    expect(l.motivo).toMatch(/NAO veio deste briefing/);
  });

  it('LANCA, nao reprova, quando o briefing nao passa no esquema', () => {
    // "o selo nao corresponde" e "o briefing esta quebrado" pedem conserto diferente.
    const dir = projeto({_esquema: 'canastra-briefing/1'}, {_sha256Briefing: 'a'.repeat(64)});
    expect(() => conferirSeloDoProjeto(dir)).toThrow();
  });
});

describe('os planos COMMITADOS no repositorio', () => {
  // O portao novo apontado para os projetos reais. Se um `plano.json` em
  // `projetos/` estiver fora de sincronia com seu briefing, e melhor saber no
  // vitest que num render.
  const PROJETOS = [
    'projetos/01-private-label',
    'projetos/02-jornada-do-grao',
    'projetos/03-prova-cena',
  ];
  for (const p of PROJETOS) {
    it(`${p}: o plano em disco bate com o briefing em disco`, () => {
      const l = conferirSeloDoProjeto(p);
      // a mensagem do laudo entra no expect para o laudo do vitest dizer QUAL
      expect(l.motivo ?? 'bate').toBe('bate');
      expect(l.bate).toBe(true);
    });
  }
});

// ---------------------------------------------------------------------------
// O ATAQUE DO CETICO, 01/10/2026.
//
// Reproduzido na maquina, nao deduzido: gravou `duracaoFrames: 9999` (era 345) em
// `projetos/03-prova-cena/plano.json` deixando `_sha256Briefing` intacto, rodou
// `node scripts/conferir.mjs --portao=selo --projeto=projetos/03-prova-cena` e recebeu
//
//   esperado   f1a6ff39...  /  no plano   f1a6ff39...  /  OK -- o plano veio deste
//   briefing                                                            EXIT=0
//
// A causa: o selo hasheava SO o briefing. O conteudo do plano nunca entrava em hash
// nenhum, entao toda edicao a mao que preservasse `_sha256Briefing` passava -- e
// `duracaoFrames` e justamente o campo que `Raiz.tsx` le por `calculateMetadata`, isto
// e, a edicao muda o MP4 e o portao diz OK.
//
// Estes testes falham com o selo de um hash so e passam com o de dois.

describe('o ataque do cetico: plano adulterado com o selo do briefing INTACTO', () => {
  /** Um plano com a forma do artefato real, o suficiente para ser selado e adulterado. */
  const planoCru = () => ({
    _gerado_por: 'src/briefing/compilar.ts',
    _sha256Briefing: '',
    _sha256Plano: '',
    serie: 'avulsa',
    fps: 30,
    duracaoFrames: 345,
    cenas: [
      {duracaoFrames: 120, inicioNaPecaFrames: 0, aparaAntesFrames: 34, eventos: []},
      {duracaoFrames: 120, inicioNaPecaFrames: 120, aparaAntesFrames: 0, eventos: []},
    ],
    transicoes: [{tipo: 'corte', duracaoFrames: 0}, {tipo: 'fade', duracaoFrames: 15}],
  });

  it('REPROVA `duracaoFrames: 9999` com `_sha256Briefing` preservado', () => {
    const b = briefing();
    const selado = selarPlano(planoCru(), b);

    // o selado, intocado, passa -- senao este teste nao estaria medindo nada
    expect(conferirSelo(b, selado).bate).toBe(true);

    // o ataque: muda o numero, preserva o selo do BRIEFING letra por letra
    const adulterado = {...selado, duracaoFrames: 9999};
    expect(adulterado._sha256Briefing).toBe(selado._sha256Briefing);

    const l = conferirSelo(b, adulterado);
    expect(l.bate).toBe(false);
    expect(l.motivo).toMatch(/plano/i);
  });

  it('REPROVA edicao em PROFUNDIDADE no plano: cenas[1].duracaoFrames', () => {
    const b = briefing();
    const selado = selarPlano(planoCru(), b);
    const adulterado = JSON.parse(JSON.stringify(selado));
    adulterado.cenas[1].duracaoFrames = 9999;
    expect(adulterado._sha256Briefing).toBe(selado._sha256Briefing);
    expect(conferirSelo(b, adulterado).bate).toBe(false);
  });

  it('REPROVA plano sem o selo DO PLANO: ausencia nao perdoa', () => {
    // Mesma regra do selo do briefing: se apagar o campo passasse, apagar o campo
    // seria o jeito mais facil de desligar o portao.
    const b = briefing();
    const selado = selarPlano(planoCru(), b);
    const semSelo = {...selado};
    delete (semSelo as {_sha256Plano?: unknown})._sha256Plano;
    expect(conferirSelo(b, semSelo).bate).toBe(false);
    expect(conferirSelo(b, {...selado, _sha256Plano: ''}).bate).toBe(false);
  });

  it('o ataque pelo DISCO, exatamente como o cetico o rodou', () => {
    const b = briefing();
    const selado = selarPlano(planoCru(), b);
    const cru = {
      ...MINIMO,
      cenas: briefing().cenas,
    };
    // o briefing em disco tem que ser o MESMO que selou, senao o teste passaria pelo
    // motivo errado (o selo do briefing divergindo em vez do selo do plano)
    const dir = mkdtempSync(path.join(os.tmpdir(), 'canastra-cetico-'));
    writeFileSync(path.join(dir, 'briefing.json'), JSON.stringify(cru), 'utf8');

    writeFileSync(path.join(dir, 'plano.json'), JSON.stringify(selado, null, 2), 'utf8');
    const antes = conferirSeloDoProjeto(dir);
    expect(antes.motivo ?? 'bate').toBe('bate');
    expect(antes.bate).toBe(true);

    // a adulteracao do cetico, no arquivo, com o selo do briefing intacto
    const texto = readFileSync(path.join(dir, 'plano.json'), 'utf8')
      .replace('"duracaoFrames": 345', '"duracaoFrames": 9999');
    expect(texto).toContain('"duracaoFrames": 9999');
    expect(texto).toContain(selado._sha256Briefing);
    writeFileSync(path.join(dir, 'plano.json'), texto, 'utf8');

    const depois = conferirSeloDoProjeto(dir);
    expect(depois.bate).toBe(false);
    expect(depois.motivo).toMatch(/plano/i);
    // e a prova de que o selo do BRIEFING continua batendo: o que reprovou foi o plano
    expect(depois.encontrado).toBe(depois.esperado);
  });

  it('O LIMITE MEDIDO: hash nao e assinatura. Quem recalcula o selo PASSA', () => {
    // Registrado como TESTE, nao so como comentario, para ninguem escrever depois que o
    // plano esta "protegido contra alteracao". Nao esta: nao ha segredo no repositorio.
    // O selo detecta DERIVA -- edicao esquecida, artefato velho -- nao falsificacao.
    // Medido na linha de comando tambem: `duracaoFrames: 9999` com
    // `_sha256Plano` recalculado deu `OK` e EXIT=0 no portao.
    const b = briefing();
    const selado = selarPlano(planoCru(), b);
    const forjado = {...selado, duracaoFrames: 9999, _sha256Plano: ''};
    forjado._sha256Plano = sha256DoPlano(forjado);
    expect(conferirSelo(b, forjado).bate).toBe(true);
    expect(forjado.duracaoFrames).toBe(9999);
  });
});
