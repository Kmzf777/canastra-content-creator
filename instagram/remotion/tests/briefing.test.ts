// O BRIEFING: forma (zod) e impressao digital (sha256 canonico).
//
// Um arquivo de teste para os dois modulos de `src/briefing/` que ja existem,
// porque os dois respondem a mesma pergunta -- "este briefing e o que diz ser?" --
// e porque a prova central do hash (ele ve o que esta ANINHADO) precisa de um
// briefing valido, que e o que o esquema define.

import {readFileSync} from 'node:fs';
import {describe, expect, it} from 'vitest';
import {
  FORMATOS,
  LICENCAS,
  SERIES,
  zBriefing,
  zCena,
  zEventoTexto,
  zFonte,
} from '../src/briefing/esquema';
import {canonico, selarPlano, sha256Do} from '../src/briefing/impressao';

/**
 * O briefing minimo que passa: uma cena, uma fonte de cor, nenhum evento.
 *
 * `audio` E OBRIGATORIO e esta aqui. Nao da para ter um "minimo" sem ele: peca de
 * foto parada sem faixa perde elegibilidade para nao-seguidor (`05-formatos.md` §3,
 * [oficial]), e a versao anterior deste esquema tinha `trilha?: Trilha` com o
 * comentario "obrigatoria se nao houver locucao" -- condicionando a obrigatoriedade
 * a um campo que NAO EXISTIA em parte nenhuma do esquema.
 */
const MINIMO = {
  _esquema: 'canastra-briefing/1',
  serie: 'avulsa',
  formatos: ['9:16'],
  duracao: {modo: 'somaCenas'},
  cenas: [{duracaoS: 3, fonte: {tipo: 'cor', cor: '#3B2A1F'}, eventos: []}],
  transicoes: [],
  audio: {
    locucao: null,
    trilha: {
      arquivo: 'ambiente.wav',
      ganhoDb: -18,
      aparaAntesS: 0,
      loopar: true,
      fadeEntradaS: 0.5,
      fadeSaidaS: 0.8,
    },
  },
  gancho: 'o gancho desta peca de teste',
  cta: 'chama no direct',
};

describe('zBriefing', () => {
  it('aceita o briefing minimo e aplica os defaults declarados', () => {
    const b = zBriefing.parse(MINIMO);
    expect(b.fps).toBe(30);
    // As 12 licencas nascem TODAS desligadas. Nenhuma tecnica que colide com
    // proibicoes.md entra por omissao.
    for (const chave of LICENCAS) expect(b.licencas[chave]).toBe(false);
    expect(b.licencas.justificativa).toBe('');
    expect(b.assets).toEqual([]);
  });

  it('recusa campo desconhecido em vez de ignorar em silencio', () => {
    // A licao 3 do CLAUDE.md: HTTP 200 ignorando o parametro. Um briefing com
    // `"duracao_alvo": 24` em vez de `duracao.alvoS` tem que FALHAR, nao render
    // 3 s e sair com exit 0.
    expect(zBriefing.safeParse({...MINIMO, duracao_alvo: 24}).success).toBe(false);
  });

  it('recusa briefing incompleto, campo a campo', () => {
    // Cada chave de topo e obrigatoria menos `fps`, `licencas`, `assets` e
    // `legenda`, que tem default ou sao opcionais. Removendo uma por uma, o
    // esquema tem que reprovar -- e o teste e por CAMPO, nao um `safeParse` de
    // objeto vazio, que passaria mesmo se metade do esquema estivesse frouxa.
    const obrigatorios = [
      '_esquema',
      'serie',
      'formatos',
      'duracao',
      'cenas',
      'transicoes',
      'audio',
      'gancho',
      'cta',
    ] as const;
    for (const chave of obrigatorios) {
      const parcial: Record<string, unknown> = {...MINIMO};
      delete parcial[chave];
      expect(zBriefing.safeParse(parcial).success, `sem ${chave}`).toBe(false);
    }
    // E o que tem default/opcional NAO reprova por ausencia.
    for (const chave of ['fps', 'licencas', 'assets', 'legenda'] as const) {
      const parcial: Record<string, unknown> = {...MINIMO};
      delete parcial[chave];
      expect(zBriefing.safeParse(parcial).success, `sem ${chave}`).toBe(true);
    }
  });

  it('recusa fps fora de 1..120 e fps fracionario', () => {
    expect(zBriefing.safeParse({...MINIMO, fps: 0}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, fps: 121}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, fps: 29.97}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, fps: 60}).success).toBe(true);
  });

  it('duracao.modo NAO tem default: briefing sem ele falha', () => {
    // Sem default de proposito. Um default aqui seria escolha estetica
    // disfarcada de conveniencia: quem pedir 24 s receberia 22,4 s sem perceber
    // na primeira peca que usar crossfade.
    expect(zBriefing.safeParse({...MINIMO, duracao: {}}).success).toBe(false);
  });

  it('exige pelo menos uma cena e pelo menos um formato', () => {
    expect(zBriefing.safeParse({...MINIMO, cenas: []}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, formatos: []}).success).toBe(false);
  });

  it('os 12 slugs de serie de 05-formatos.md, mais avulsa', () => {
    expect(SERIES.length).toBe(13);
    expect(SERIES).toContain('voce-sabia');
    expect(SERIES).toContain('objecao-preco');
    expect(SERIES).toContain('avulsa');
    expect(zBriefing.safeParse({...MINIMO, serie: 'inventada'}).success).toBe(false);
  });

  it('os quatro formatos, e 4:5 entre eles', () => {
    expect([...FORMATOS]).toEqual(['9:16', '1:1', '4:5', '16:9']);
  });

  it('`audio` e OBRIGATORIO: briefing sem ele falha', () => {
    // A ausencia A4. Medido em 30/09/2026: `grep -rn "Audio" src/` so achava
    // `motor/audio/normalizar.ts`, que e medicao POS-render. Nao havia `<Audio>` na
    // arvore e todo som era carona do `<Video>` -- logo TODA peca de foto parada
    // saia muda, e 5 das 12 series do catalogo partem de foto parada.
    const {audio, ...semAudio} = MINIMO;
    void audio;
    expect(zBriefing.safeParse(semAudio).success).toBe(false);
  });

  it('locucao e trilha podem ser null, mas ausente nao e o mesmo que null', () => {
    // A regra escrita sobre campos que EXISTEM. O esquema aceita a forma; a recusa
    // dos dois nulos e do refinador (Tarefa 6), porque ela cita um criterio
    // [oficial] e a mensagem e o que ensina.
    expect(zBriefing.safeParse({...MINIMO, audio: {locucao: null, trilha: null}}).success).toBe(
      true,
    );
    expect(zBriefing.safeParse({...MINIMO, audio: {trilha: null}}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, audio: {locucao: null}}).success).toBe(false);
  });

  it('a trilha exige loopar, fadeEntradaS e fadeSaidaS -- SEM default', () => {
    // Uma trilha de 20 s numa peca de 40 s e ou loop ou silencio na metade, e isso
    // nao se decide por conveniencia.
    const t = {arquivo: 'ambiente.wav', ganhoDb: -18, aparaAntesS: 0};
    expect(zBriefing.safeParse({...MINIMO, audio: {locucao: null, trilha: t}}).success).toBe(
      false,
    );
    expect(
      zBriefing.safeParse({
        ...MINIMO,
        audio: {locucao: null, trilha: {...t, loopar: true, fadeEntradaS: 0, fadeSaidaS: 0}},
      }).success,
    ).toBe(true);
  });

  it('NAO existe campo de LUFS no briefing', () => {
    // `AUDIO = {lufs: -14, picoDbtp: -1}` e alvo de POS-render: quem o aplica e
    // `scripts/normalizar-audio.mjs`, sobre a MISTURA, com `-c:v copy`. Um alvo por
    // faixa aqui seria uma segunda verdade que o normalizador sobrescreve sem
    // avisar -- e o prototipo `out/_spec-briefing/a-private-label.json` trazia
    // `alvoLufs`, que por isso NAO entra.
    const t = {
      arquivo: 'ambiente.wav',
      ganhoDb: -18,
      aparaAntesS: 0,
      loopar: false,
      fadeEntradaS: 0,
      fadeSaidaS: 0,
      alvoLufs: -14,
    };
    expect(zBriefing.safeParse({...MINIMO, audio: {locucao: null, trilha: t}}).success).toBe(
      false,
    );
    expect(
      zBriefing.safeParse({...MINIMO, audio: {locucao: null, trilha: null}, alvoLufs: -14}).success,
    ).toBe(false);
  });

  it('a excecao do `_` NAO deixa passar campo desconhecido sem underscore', () => {
    // O risco do preprocess: se ele removesse chave demais, ou se a estrita ficasse
    // frouxa, `duracao_alvo: 24` voltaria a ser ignorado em silencio.
    expect(zBriefing.safeParse({...MINIMO, duracao_alvo: 24}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, Audio: {}}).success).toBe(false);
    expect(zBriefing.safeParse({...MINIMO, _qualquer_nota: 'texto livre'}).success).toBe(true);
  });

  it('a excecao do `_` nao vale para `_esquema`, que e campo de verdade', () => {
    expect(zBriefing.safeParse({...MINIMO, _esquema: 'canastra-briefing/2'}).success).toBe(false);
  });

  it('a excecao do `_` vale EM TODA PROFUNDIDADE -- divergencia medida do plano', () => {
    // O plano escreve o preprocess varrendo so o nivel de topo. Com ele, comentario
    // dentro de cena, de fonte, de evento ou de audio sobrevive a limpeza e cai na
    // estrita -- e e exatamente ali que estao os comentarios que valem: o
    // `_procedencia` de uma citacao literal e o `_bloqueio` de um arquivo que nao
    // existe. A varredura recursiva aceita os quatro:
    const comComentario = {
      ...MINIMO,
      cenas: [
        {
          _estagio: 'comentario em CENA',
          duracaoS: 3,
          fonte: {_medido: 'comentario em FONTE', tipo: 'cor', cor: '#3B2A1F'},
          eventos: [
            {
              _procedencia: 'comentario em EVENTO',
              papel: 'manchete',
              texto: 'X',
              entradaS: 0,
              pista: 'topo',
            },
          ],
        },
      ],
      audio: {
        locucao: null,
        trilha: {
          _bloqueio: 'comentario em FAIXA',
          arquivo: 'a.wav',
          ganhoDb: -18,
          aparaAntesS: 0,
          loopar: true,
          fadeEntradaS: 0,
          fadeSaidaS: 0,
        },
      },
    };
    expect(zBriefing.safeParse(comComentario).success).toBe(true);
    // E a prova de que a varredura so-no-topo NAO bastaria: aplicada a mao, ela deixa
    // os quatro comentarios aninhados vivos na estrutura.
    const soTopo = (cru: Record<string, unknown>) => {
      const limpo: Record<string, unknown> = {};
      for (const [k, v] of Object.entries(cru)) {
        if (k.startsWith('_') && k !== '_esquema') continue;
        limpo[k] = v;
      }
      return limpo;
    };
    const sobreviventes: string[] = [];
    const varre = (v: unknown, caminho: string) => {
      if (Array.isArray(v)) return void v.forEach((x, i) => varre(x, `${caminho}[${i}]`));
      if (typeof v !== 'object' || v === null) return;
      for (const [k, val] of Object.entries(v as Record<string, unknown>)) {
        if (k.startsWith('_') && k !== '_esquema') sobreviventes.push(`${caminho}.${k}`);
        varre(val, `${caminho}.${k}`);
      }
    };
    varre(soTopo(comComentario), '');
    expect(sobreviventes).toEqual([
      '.cenas[0]._estagio',
      '.cenas[0].fonte._medido',
      '.cenas[0].eventos[0]._procedencia',
      '.audio.trilha._bloqueio',
    ]);
    // e cada um deles, sozinho, reprova na estrita se nao for limpo
    expect(
      zBriefing.safeParse({
        ...MINIMO,
        cenas: [{duracaoS: 3, fonte: {tipo: 'cor', cor: '#3B2A1F', naoExiste: 1}, eventos: []}],
      }).success,
    ).toBe(false);
  });
});

describe('zLegenda', () => {
  const legenda = {arquivo: 'transcricao.json', relogio: 'fonte', ancora: {tipo: 'locucao'}};

  it('`relogio` e um enum de UM valor: declarar e o ponto, nao escolher', () => {
    expect(zBriefing.safeParse({...MINIMO, legenda}).success).toBe(true);
    expect(zBriefing.safeParse({...MINIMO, legenda: {...legenda, relogio: 'peca'}}).success).toBe(
      false,
    );
  });

  it('a ancora tem TRES casos, e nenhum deles e implicito', () => {
    // Com N cenas ha N valores de `aparaAntesS` e UMA legenda: somar "o"
    // `aparaAntesS` deixa de ser definido. A resolucao e nomear o instante da
    // transcricao que cai no frame 0 da peca -- ver spec §2.2.1.
    for (const ancora of [
      {tipo: 'locucao'},
      {tipo: 'cena', indice: 0},
      {tipo: 'segundo', valorS: 1.14},
    ]) {
      expect(
        zBriefing.safeParse({...MINIMO, legenda: {...legenda, ancora}}).success,
        JSON.stringify(ancora),
      ).toBe(true);
    }
    expect(
      zBriefing.safeParse({...MINIMO, legenda: {...legenda, ancora: {tipo: 'inventado'}}}).success,
    ).toBe(false);
    // `ancora` ausente NAO passa: sem ela o compilador teria que escolher a cena 0
    // por conveniencia, que e o default escondido que esta spec proibe.
    const {ancora, ...semAncora} = legenda;
    void ancora;
    expect(zBriefing.safeParse({...MINIMO, legenda: semAncora}).success).toBe(false);
  });

  it('NAO existe `aparaAntesS` na legenda: o nome dela e `ancora`', () => {
    expect(
      zBriefing.safeParse({...MINIMO, legenda: {...legenda, aparaAntesS: 1.14}}).success,
    ).toBe(false);
  });
});

describe('zAsset', () => {
  it('recorte de embalagem exige `laudoExigido: true` LITERAL', () => {
    const a = {arquivo: 'suave-250g.png', tipo: 'recorte-embalagem', laudoExigido: true};
    expect(zBriefing.safeParse({...MINIMO, assets: [a]}).success).toBe(true);
    expect(zBriefing.safeParse({...MINIMO, assets: [{...a, laudoExigido: false}]}).success).toBe(
      false,
    );
    // lista vazia e valido: a maioria das pecas nao tem recorte de embalagem
    expect(zBriefing.safeParse({...MINIMO, assets: []}).success).toBe(true);
  });

  it('o laudo NAO e copiado para dentro do briefing', () => {
    // Copiar `aprovado: true` para ca criaria a segunda fonte de verdade, e um humano
    // podendo digitar `aprovado: true` a mao transformaria o portao fail-closed de
    // `publicar.py:82` em decoracao. A prova e a PRESENCA do arquivo em
    // `public/assets/`, e quem a confere e o portao de ritmo.
    const a = {
      arquivo: 'suave-250g.png',
      tipo: 'recorte-embalagem',
      laudoExigido: true,
      aprovado: true,
    };
    expect(zBriefing.safeParse({...MINIMO, assets: [a]}).success).toBe(false);
  });
});

describe('zFonte', () => {
  it('video exige razaoExibicao MEDIDA e apara em segundos', () => {
    expect(
      zFonte.safeParse({
        tipo: 'video',
        arquivo: 'pl.mp4',
        razaoExibicao: 0.5625,
        aparaAntesS: 1.14,
        enquadramento: 'preencher',
        camera: 'parado',
      }).success,
    ).toBe(true);
    // Sem razaoExibicao nao passa: `pl.mp4` grava 1024x576 e exibe 576x1024
    // (displaymatrix -90). Quem preenche este campo e `sondar()`, nao o dedo.
    expect(
      zFonte.safeParse({
        tipo: 'video',
        arquivo: 'pl.mp4',
        aparaAntesS: 0,
        enquadramento: 'preencher',
        camera: 'parado',
      }).success,
    ).toBe(false);
  });

  it('foto exige `registro` SEM default -- e a regra da marca por construcao', () => {
    // proibicoes.md:24: "Foto real entra por um registro que declara a origem
    // (moldura, cartao, tela cheia), nunca como recorte flutuando." Sem default,
    // a regra e cumprida por construcao em vez de por lembranca.
    const base = {
      tipo: 'foto',
      arquivo: 'cafezal.jpg',
      razaoExibicao: 4032 / 3024,
      enquadramento: {tipo: 'faixa'},
      camera: 'pushLento',
    };
    expect(zFonte.safeParse(base).success).toBe(false);
    expect(zFonte.safeParse({...base, registro: 'telaCheia'}).success).toBe(true);
    expect(zFonte.safeParse({...base, registro: 'inventado'}).success).toBe(false);
  });

  it('recorte de foto e em FRACAO da fonte, nunca em pixel', () => {
    // Fracao para o mesmo briefing servir a foto de 4032x3024 e a regravacao
    // dela em outra resolucao sem reescrever numero.
    const base = {
      tipo: 'foto',
      arquivo: 'cafezal.jpg',
      razaoExibicao: 4032 / 3024,
      registro: 'telaCheia',
      camera: 'pushLento',
    };
    expect(
      zFonte.safeParse({
        ...base,
        enquadramento: {tipo: 'recorte', x: 0.2, y: 0, largura: 0.4218, altura: 1},
      }).success,
    ).toBe(true);
    expect(
      zFonte.safeParse({
        ...base,
        enquadramento: {tipo: 'recorte', x: 0.2, y: 0, largura: 1701, altura: 3024},
      }).success,
    ).toBe(false);
  });

  it('grade aceita 2 a 4 celulas de fonte SIMPLES, e nao grade dentro de grade', () => {
    const celula = {tipo: 'cor', cor: '#4A5D3A'};
    expect(
      zFonte.safeParse({tipo: 'grade', colunas: 2, linhas: 1, calha: 8, celulas: [celula, celula]})
        .success,
    ).toBe(true);
    expect(
      zFonte.safeParse({tipo: 'grade', colunas: 2, linhas: 1, calha: 8, celulas: [celula]}).success,
    ).toBe(false);
    // Recursao em zod obriga anotacao de tipo manual = segunda fonte de verdade.
    // Nenhuma das 12 series pede grade dentro de grade.
    expect(
      zFonte.safeParse({
        tipo: 'grade',
        colunas: 2,
        linhas: 1,
        calha: 8,
        celulas: [
          celula,
          {tipo: 'grade', colunas: 2, linhas: 1, calha: 8, celulas: [celula, celula]},
        ],
      }).success,
    ).toBe(false);
  });
});

describe('zEventoTexto', () => {
  // `pista` e OBRIGATORIO: ele esta em todo objeto de evento daqui para baixo.
  const base = {texto: 'X', entradaS: 0, pista: 'topo'} as const;

  it('aceita os tres papeis de evento e RECUSA legenda', () => {
    for (const papel of ['manchete', 'dado', 'etiqueta']) {
      expect(zEventoTexto.safeParse({...base, papel}).success, papel).toBe(true);
    }
    // A legenda e camada de PECA, fora da TransitionSeries. Se `legenda` fosse
    // papel de evento, na janela de crossfade duas legendas com textos
    // diferentes ficariam no ar ao mesmo tempo.
    expect(zEventoTexto.safeParse({...base, papel: 'legenda'}).success).toBe(false);
  });

  it('`pista` e OBRIGATORIO, sem default', () => {
    // A tabela `PISTA_PADRAO` existe em `motor/evento.ts`, mas ela NAO e default do
    // motor: e o que a skill `canastra-briefing` escreve no arquivo. Assim a escolha
    // fica visivel no JSON, onde o Rafael a le e a muda, em vez de morar no codigo.
    const {pista, ...semPista} = base;
    void pista;
    expect(zEventoTexto.safeParse({...semPista, papel: 'manchete'}).success).toBe(false);
  });

  it('`rodape` NAO e pista de evento: ela e da camada Legenda', () => {
    expect(zEventoTexto.safeParse({...base, papel: 'manchete', pista: 'rodape'}).success).toBe(
      false,
    );
    for (const p of ['topo', 'principal', 'tela']) {
      expect(zEventoTexto.safeParse({...base, papel: 'manchete', pista: p}).success, p).toBe(true);
    }
  });

  it('NAO existe campo `encaixe` no evento: ele e derivado de (pista, formato)', () => {
    // `faixa` x `coluna` nao e escolha, e consequencia do formato: no 9:16 a sobra ao
    // lado do video e 0,00 px (medido), logo `encaixe: ['coluna']` ali e
    // insatisfazivel -- um campo que o motor nao pode honrar e o HTTP 200 que ignora
    // o parametro, licao 3 do CLAUDE.md. Para pedir cartela, declare `pista: 'tela'`.
    expect(zEventoTexto.safeParse({...base, papel: 'manchete', encaixe: ['cartela']}).success).toBe(
      false,
    );
  });

  it('entradaS e relativo a CENA, e negativo nao existe', () => {
    expect(zEventoTexto.safeParse({...base, papel: 'manchete', entradaS: -1}).success).toBe(false);
  });

  it('texto vazio nao e evento', () => {
    expect(zEventoTexto.safeParse({...base, papel: 'manchete', texto: '   '}).success).toBe(false);
  });

  it('nao existe campo de cadencia no evento: ela vem do papel', () => {
    expect(
      zEventoTexto.safeParse({...base, papel: 'manchete', cadencia: 'palavra'}).success,
    ).toBe(false);
  });

  it('nao existe `zona` nem `modo` nem `preset`: eram os nomes do prototipo', () => {
    // `out/_spec-briefing/*.json` escrevia `zona: {tipo:'nomeada', nome:'centroSeguro'}`,
    // `modo: 'cartela'` e `preset: 'pousoPorPalavra'`. Os tres sairam: a pista
    // substitui a zona, o encaixe e derivado e a cadencia vem do papel. Se o esquema
    // os ACEITASSE em silencio, o prototipo passaria e nada do novo seria aplicado.
    for (const extra of [
      {zona: {tipo: 'nomeada', nome: 'centroSeguro'}},
      {modo: 'cartela'},
      {preset: 'pousoPorPalavra'},
      {citacaoLiteral: true},
    ]) {
      expect(
        zEventoTexto.safeParse({...base, papel: 'manchete', ...extra}).success,
        JSON.stringify(extra),
      ).toBe(false);
    }
  });
});

describe('zCena', () => {
  it('cena com duracao zero ou negativa nao existe', () => {
    const fonte = {tipo: 'cor', cor: '#3B2A1F'};
    expect(zCena.safeParse({duracaoS: 0, fonte, eventos: []}).success).toBe(false);
    expect(zCena.safeParse({duracaoS: -1, fonte, eventos: []}).success).toBe(false);
  });

  it('eventos LISTA VAZIA e cena completa, nao cena quebrada', () => {
    // A propriedade que a Tarefa 5 do plano de qualidade protege com "opcional
    // sem placeholder" sobrevive: lista vazia e peca completa sem evento, sem
    // erro e sem texto de exemplo.
    const fonte = {tipo: 'cor', cor: '#3B2A1F'};
    expect(zCena.safeParse({duracaoS: 2, fonte, eventos: []}).success).toBe(true);
  });
});

// ---- os dois briefings reais do repositorio ---------------------------------

describe('projetos/01-private-label/briefing.json', () => {
  it('passa no esquema, com os numeros medidos em 02 PL.mp4', () => {
    // O briefing e o arquivo que o Rafael edita: se ele nao passar no proprio
    // esquema, o esquema esta errado.
    const bruto = JSON.parse(readFileSync('projetos/01-private-label/briefing.json', 'utf8'));
    const b = zBriefing.parse(bruto);
    expect(b.cenas.length).toBe(1);
    expect(b.transicoes.length).toBe(0);
    // 23,2 s = 696 frames a 30 fps, que e DURACAO_FRAMES de Raiz.tsx:28.
    expect(Math.round(b.cenas[0].duracaoS * b.fps)).toBe(696);
    // 1,14 s = 34 frames, que e CORTAR_ANTES_FRAMES de Raiz.tsx:25.
    const fonte = b.cenas[0].fonte;
    expect(fonte.tipo).toBe('video');
    if (fonte.tipo === 'video') expect(Math.round(fonte.aparaAntesS * b.fps)).toBe(34);
    // 2,3333 s = 70 frames = o inicioFrame 104 do props.json menos o corte de 34.
    expect(Math.round(b.cenas[0].eventos[0].entradaS * b.fps)).toBe(70);
    // A manchete pede a CARTELA pela pista, que e o unico caminho para ela.
    expect(b.cenas[0].eventos[0].pista).toBe('tela');
    // A locucao que ja esta no disco: `public/fonte/pl.wav` (medido). E o 1,14 mora
    // AQUI, nao na legenda -- a legenda aponta para ele por `ancora`.
    expect(b.audio.locucao?.arquivo).toBe('pl.wav');
    expect(Math.round((b.audio.locucao?.aparaAntesS ?? 0) * b.fps)).toBe(34);
    expect(b.audio.trilha).toBeNull();
    expect(b.legenda?.ancora).toEqual({tipo: 'locucao'});
    expect(b.assets).toEqual([]);
  });
});

describe('projetos/02-jornada-do-grao/briefing.json', () => {
  it('passa no esquema, e a razao de exibicao e a MEDIDA, nao a do container', () => {
    const bruto = JSON.parse(readFileSync('projetos/02-jornada-do-grao/briefing.json', 'utf8'));
    const b = zBriefing.parse(bruto);
    expect(b.serie).toBe('jornada');
    expect(b.cenas.length).toBe(4);
    // `transicoes` tem exatamente `cenas.length - 1` entradas. A contagem e cobrada
    // pelo refinador (Tarefa 6); aqui ela ja esta certa no arquivo.
    expect(b.transicoes.length).toBe(3);
    // AS DUAS RAZOES CORRIGIDAS. O prototipo `out/_spec-briefing/b-jornada-foto.json`
    // declarava 1,3333 para IMG_1421 e IMG_1424, e os dois sao EXIF Orientation 6:
    // gravam 4032x3024 e EXIBEM 3024x4032, razao 0,75 (medido por ffprobe em
    // 30/09/2026). IMG_1398 e Orientation 1 e e 1,3333 de verdade.
    const razoes = b.cenas
      .map((c) => c.fonte)
      .filter((f) => f.tipo === 'foto')
      .map((f) => (f.tipo === 'foto' ? f.razaoExibicao : 0));
    expect(razoes).toEqual([0.75, 0.75, 1.3333]);
    // Foto sem `registro` nao existe: `proibicoes.md:24`.
    for (const c of b.cenas) {
      if (c.fonte.tipo === 'foto') expect(c.fonte.registro).toBe('telaCheia');
    }
    // Peca sem voz, COM faixa: e a regra de elegibilidade de Reel.
    expect(b.audio.locucao).toBeNull();
    expect(b.audio.trilha?.loopar).toBe(true);
    // O recorte de embalagem entra pela lista de assets, e o laudo NAO e copiado.
    expect(b.assets.map((a) => a.arquivo)).toEqual(['suave-250g.png']);
    // `legenda` ausente, nao `null`: o prototipo escrevia `legenda: null`, que o
    // esquema estrito recusa -- opcional e ausencia, nao nulo.
    expect(b.legenda).toBeUndefined();
  });
});

// ---- a impressao digital -----------------------------------------------------

/** Um briefing valido, com pontos de variacao em tres profundidades. */
function briefing(troca: Record<string, unknown> = {}) {
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
        eventos: [{papel: 'manchete', texto: 'TRES', entradaS: 0, pista: 'topo'}],
      },
    ],
    transicoes: [{tipo: 'corte'}],
    audio: {locucao: {arquivo: 'pl.wav', ganhoDb: 0, aparaAntesS: 0}, trilha: null},
    ...troca,
  });
}

describe('sha256Do -- a serializacao canonica', () => {
  it('O HASH VE O QUE ESTA ANINHADO. Era aqui que a protecao era um no-op', () => {
    // O DEFEITO MEDIDO: `JSON.stringify(valor, Object.keys(valor).sort())` -- o
    // segundo argumento do JSON.stringify e uma ALLOWLIST APLICADA RECURSIVAMENTE a
    // todo objeto da estrutura. Passando so as chaves de topo, TUDO que esta aninhado
    // e descartado: o serializado saia
    //   {"_esquema":"x","cenas":[{}],"cta":"c","duracao":{},"fps":30,...}
    // e dois briefings com `cenas[0].duracaoS` 23,2 contra 99 e textos completamente
    // diferentes davam O MESMO HASH.
    //
    // Como o `_sha256Briefing` e a UNICA protecao nomeada no Risco assumido nº 3, a
    // protecao central do desenho era um no-op -- e o teste que existia so variava
    // `cta`, chave de TOPO, entao passava e dava falsa confianca.
    const a = briefing();
    const b = briefing({
      cenas: [
        {
          duracaoS: 99,
          fonte: {tipo: 'cor', cor: '#3B2A1F'},
          eventos: [
            {papel: 'manchete', texto: 'TEXTO TOTALMENTE OUTRO', entradaS: 0, pista: 'topo'},
          ],
        },
        {
          duracaoS: 6,
          fonte: {tipo: 'cor', cor: '#4A5D3A'},
          eventos: [{papel: 'manchete', texto: 'TRES', entradaS: 0, pista: 'topo'}],
        },
      ],
    });
    expect(sha256Do(a)).not.toBe(sha256Do(b));
    // E a prova do defeito, para que ninguem o reintroduza: a serializacao antiga
    // confunde os dois. Se um dia este `toBe` virar `not.toBe`, o JSON.stringify com
    // allowlist deixou de ser um achatador -- e nao e isso que vai acontecer.
    const antigo = (v: object) => JSON.stringify(v, Object.keys(v).sort());
    expect(antigo(a)).toBe(antigo(b));
    // e o serializado achatado, para que o defeito fique legivel no laudo
    expect(antigo(a)).toContain('"cenas":[{},{}]');
  });

  it('e ESTAVEL: a ordem das chaves no objeto nao muda o hash', () => {
    // Determinismo importa porque o portao compara hashes entre execucoes, e a ordem
    // de insercao de `Object.keys` muda com a ordem de escrita do JSON.
    const um = {a: 1, b: {c: 2, d: [3, {e: 4}]}};
    const outro = {b: {d: [3, {e: 4}], c: 2}, a: 1};
    expect(sha256Do(um)).toBe(sha256Do(outro));
  });

  it('distingue o que JSON.stringify cru confundiria', () => {
    // Tres pares que um serializador descuidado achata:
    expect(sha256Do({a: undefined})).not.toBe(sha256Do({}));
    expect(sha256Do([1, 2])).not.toBe(sha256Do({0: 1, 1: 2}));
    expect(sha256Do({a: null})).not.toBe(sha256Do({a: 0}));
    // e a string carrega o proprio comprimento, entao a virgula DENTRO de um texto
    // nao se confunde com a virgula que separa dois itens
    expect(canonico(['a,b'])).not.toBe(canonico(['a', 'b']));
  });

  it('muda com QUALQUER campo, em QUALQUER profundidade', () => {
    const base = briefing();
    const iguais = sha256Do(briefing());
    expect(iguais).toBe(sha256Do(base)); // o mesmo briefing da o mesmo hash
    // topo
    expect(sha256Do(briefing({cta: 'outro cta'}))).not.toBe(iguais);
    // profundidade 3: cenas[0].eventos[0].texto
    const fundo = briefing();
    fundo.cenas[0].eventos[0].texto = 'OUTRO';
    expect(sha256Do(fundo)).not.toBe(iguais);
    // profundidade 2: cenas[0].duracaoS
    const dur = briefing();
    dur.cenas[0].duracaoS = 23.3;
    expect(sha256Do(dur)).not.toBe(iguais);
    // profundidade 3: audio.locucao.aparaAntesS
    const audio = briefing();
    audio.audio.locucao!.aparaAntesS = 1.14;
    expect(sha256Do(audio)).not.toBe(iguais);
    // profundidade 3: cenas[1].fonte.cor -- a SEGUNDA cena, que uma allowlist de
    // topo tambem achatava
    const cor = briefing();
    const f = cor.cenas[1].fonte;
    if (f.tipo === 'cor') f.cor = '#000001';
    expect(sha256Do(cor)).not.toBe(iguais);
  });

  it('o hash e 64 hex, e numero nao finito LANCA em vez de virar null', () => {
    expect(sha256Do(briefing())).toMatch(/^[0-9a-f]{64}$/);
    // `JSON.stringify(NaN)` da `null`, e ai NaN e null teriam o mesmo hash. Um
    // numero sem forma estavel tem que ser erro alto, nao silencio.
    expect(() => sha256Do({a: Number.NaN})).toThrow(/nao finito/);
    expect(() => sha256Do({a: Number.POSITIVE_INFINITY})).toThrow(/nao finito/);
  });
});

describe('selarPlano', () => {
  it('sela o plano com o hash do briefing que o gerou', () => {
    const b = briefing();
    // `compilar()` ainda nao existe (Tarefa 7). O selo nao depende dele: ele depende
    // de o plano ter o campo, e e por isso que `selarPlano` e generico.
    const p = selarPlano({_sha256Briefing: '', duracaoFrames: 876}, b);
    expect(p._sha256Briefing).toMatch(/^[0-9a-f]{64}$/);
    expect(p._sha256Briefing).toBe(sha256Do(b));
    expect(p.duracaoFrames).toBe(876);
  });
});
