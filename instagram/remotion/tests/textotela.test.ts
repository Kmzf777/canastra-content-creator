// Portao da camada de manchete / kinetic type.
//
// O QUE ESTE ARQUIVO NAO TESTA, E POR QUE
//
// Nao renderiza. `TextoTela.tsx` importa `tipografia.ts`, que tem efeito
// colateral de modulo (`delayRender` + `loadFont`) e, em Node, estoura
// `TypeError: Invalid URL` porque `loadFont` faz `fetch` no caminho de asset do
// bundler. Medido: um teste que so importa `Legenda.tsx` passa a asercao e o
// vitest ainda sai com codigo 1 por causa do erro nao tratado.
//
// Por isso a gramatica de movimento e a geometria vivem em modulos PUROS
// (`src/motor/movimento.ts` e `src/motor/camadas/texto-forma.ts`), sem React e
// sem remotion, e o .tsx e so a fiacao. O que da para provar em Node esta aqui.

import {describe, it, expect} from 'vitest';
import {
  POUSO,
  atrasoDoIrmao,
  bezierDeCss,
  duracaoComIrmaos,
  fases,
  janelasDeIrmaos,
  progresso,
  push,
} from '../src/motor/movimento';
import {duracaoDaFrase, duracaoPorPalavra, formaTextoTela, quebrar} from '../src/motor/camadas/texto-forma';
import {layout} from '../src/motor/layout';
import {COR, LEGENDA, PUSH, TEMPO} from '../src/identidade/tokens';
import {GLIFOS, METRICAS, larguraEm} from '../src/identidade/glifos';
import {cadencia} from '../src/motor/cadencia';
import {emFrames} from '../src/motor/relogio';

// A cadencia de 30 fps, que e o fps em que TODOS os numeros deste arquivo foram
// medidos. Passar `C` em vez de deixar um default e o que garante que o teste
// continua medindo o mesmo tempo depois de a cadencia virar parametro.
const C = cadencia(30);

const FORMATOS: Array<[number, number]> = [
  [1080, 1920],
  [1080, 1080],
  [1920, 1080],
];

const zonasDe = (largura: number, altura: number) =>
  layout({largura, altura, razaoFonte: 9 / 16});

// ---------------------------------------------------------------------------
describe('bezier do token de pouso', () => {
  it('le os quatro numeros do proprio TEMPO.pousoEasing', () => {
    // A curva de JS e a string de CSS tem que sair do MESMO lugar, ou o pouso
    // medido no teste nao e o pouso que o Chrome desenha.
    const f = bezierDeCss(TEMPO.pousoEasing);
    expect(f(0)).toBeCloseTo(0, 6);
    expect(f(1)).toBeCloseTo(1, 6);
  });

  it('e monotonica crescente: sem volta, logo sem elastico', () => {
    let anterior = -1;
    for (let t = 0; t <= 1.0001; t += 0.01) {
      const y = POUSO(Math.min(t, 1));
      expect(y).toBeGreaterThanOrEqual(anterior - 1e-9);
      anterior = y;
    }
  });

  it('nunca passa de 1: overshoot nao mora na curva', () => {
    for (let t = 0; t <= 1.0001; t += 0.005) {
      expect(POUSO(Math.min(t, 1))).toBeLessThanOrEqual(1 + 1e-9);
    }
  });

  it('recusa string que nao e cubic-bezier', () => {
    expect(() => bezierDeCss('ease-in-out')).toThrow();
  });
});

// ---------------------------------------------------------------------------
describe('fases', () => {
  it('numa janela folgada usa os tokens crus', () => {
    const f = fases(90, C);
    expect(f.entrada).toBe(C.entrada);
    expect(f.saida).toBe(C.entrada);
    expect(f.hold).toBe(90 - 2 * C.entrada);
  });

  it('a duracao minima e entrada + holdFinal + saida', () => {
    expect(C.duracaoMinima).toBe(C.entrada + C.holdFinal + C.entrada);
    const f = fases(C.duracaoMinima, C);
    expect(f.entrada).toBe(C.entrada);
    expect(f.hold).toBe(C.holdFinal);
    expect(f.saida).toBe(C.entrada);
  });

  it('janela curta comprime as pontas em vez de estourar o hold', () => {
    for (const d of [1, 2, 3, 9, 20, 35]) {
      const f = fases(d, C);
      expect(f.entrada + f.hold + f.saida).toBe(d);
      expect(f.hold).toBeGreaterThanOrEqual(0);
      expect(f.entrada).toBeGreaterThanOrEqual(0);
      expect(f.saida).toBeGreaterThanOrEqual(0);
    }
  });
});

// ---------------------------------------------------------------------------
describe('progresso', () => {
  const j = {inicio: 10, duracao: 60};

  it('antes do inicio o elemento nao existe', () => {
    for (const f of [0, 5, 9]) {
      const e = progresso(f, j, C);
      expect(e.fase).toBe('antes');
      expect(e.presenca).toBe(0);
    }
  });

  it('depois do fim o elemento nao existe', () => {
    for (const f of [70, 71, 200]) {
      const e = progresso(f, j, C);
      expect(e.fase).toBe('depois');
      expect(e.presenca).toBe(0);
    }
  });

  it('a entrada vai de 0 a 1 ao longo de C.entrada frames', () => {
    // O PRIMEIRO FRAME DESENHADO NAO E MAIS ZERO, e isso e o conserto, nao um
    // ajuste de teste. Ate 01/10/2026 a entrada era `t / f.entrada`: em t = 0
    // dava 0, um frame renderizado e invisivel. Agora e `(t + 1) / f.entrada`,
    // entao o primeiro frame desenhado sai em POUSO(1/12) = 0,334183 (medido) e
    // a entrada COMPLETA no ultimo frame dela, t = C.entrada - 1.
    expect(progresso(10, j, C).presenca).toBeCloseTo(POUSO(1 / C.entrada), 6);
    expect(progresso(10, j, C).presenca).toBeCloseTo(0.334183, 6);
    expect(progresso(10 + C.entrada - 1, j, C).presenca).toBeCloseTo(1, 6);
    expect(progresso(10 + C.entrada, j, C).presenca).toBeCloseTo(1, 6);
    // e cresce monotonicamente no meio
    let anterior = -1;
    for (let f = 10; f <= 10 + C.entrada; f++) {
      const p = progresso(f, j, C).presenca;
      expect(p).toBeGreaterThanOrEqual(anterior - 1e-9);
      anterior = p;
    }
  });

  it('o hold fica cheio e parado', () => {
    const f0 = 10 + C.entrada;
    const f1 = 10 + 60 - C.entrada;
    for (let f = f0; f < f1; f++) {
      const e = progresso(f, j, C);
      expect(e.presenca).toBeCloseTo(1, 9);
      expect(e.escala).toBeCloseTo(1, 9);
      if (f > f0) expect(e.fase).toBe('hold');
    }
  });

  it('a saida e ACELERADA: na metade ainda esta quase cheia', () => {
    const inicioSaida = 10 + 60 - C.entrada;
    // `pSaida` = 0,5 cai no frame (inicioSaida + entrada/2 - 1), porque a saida
    // e normalizada pelo ULTIMO frame desenhado -- ver o comentario em
    // `movimento.ts`. Sem o `-1` isto mede 7/12 e nao 6/12.
    const meio = inicioSaida + C.entrada / 2 - 1;
    const esperado = 1 - Math.pow(0.5, C.saidaExpoente);
    expect(progresso(meio, j, C).presenca).toBeCloseTo(esperado, 6);
    // e isso e bem mais lento que linear no comeco
    expect(progresso(meio, j, C).presenca).toBeGreaterThan(0.75);
  });

  it('a saida cai monotonicamente ate 0', () => {
    let anterior = 2;
    for (let f = 10 + 60 - C.entrada; f <= 10 + 60; f++) {
      const p = progresso(f, j, C).presenca;
      expect(p).toBeLessThanOrEqual(anterior + 1e-9);
      anterior = p;
    }
    expect(progresso(10 + 60, j, C).presenca).toBe(0);
  });

  it('o ULTIMO frame DESENHADO fecha em zero, e nao a 18,85%', () => {
    // O DEFEITO QUE ESTE TESTE PEGA, e que os outros deixaram passar:
    //
    // a saida era normalizada pelo primeiro frame NAO desenhado. Medido numa
    // janela de 36 frames, presenca nos seis ultimos frames desenhados:
    //   0.8105  0.7257  0.6221  0.4986  0.3544  0.1885
    // e o frame seguinte nunca e desenhado (`TextoTela.tsx` devolve null em
    // `t >= duracaoCena`). Ou seja o elemento desaparecia de 18,85% de
    // opacidade para zero num frame -- o "sai seco" que a regra 6 proibe. Na
    // cartela isso e uma tela cheia de terra sumindo a 19%.
    //
    // O teste vizinho passava porque media `progresso(duracao)`, que e o ramo
    // 'depois' -- nunca o ultimo frame renderizado.
    for (const duracao of [36, 51, 66, 90]) {
      const janela = {inicio: 0, duracao};
      expect(progresso(duracao - 1, janela, C).presenca).toBeCloseTo(0, 9);
      expect(progresso(duracao - 1, janela, C).escala).toBeCloseTo(
        1 - C.overshoot,
        9,
      );
    }
  });

  it('o PRIMEIRO frame desenhado ja tem presenca, e nao um frame gasto invisivel', () => {
    // A OUTRA PONTA DO MESMO DEFEITO. A entrada era normalizada pelo frame
    // ANTERIOR ao primeiro desenhado: `t / f.entrada` com t = 0 da 0, entao o
    // primeiro frame renderizado de todo elemento saia com presenca 0,0000 --
    // um frame pago e invisivel, e a escala travada em 1+overshoot.
    //
    // Com `(t + 1) / f.entrada` o primeiro frame desenhado sai em POUSO(1/12) =
    // 0,334183 (medido) e a entrada COMPLETA no ultimo frame dela (t = 11), nao
    // no primeiro frame do hold.
    for (const duracao of [36, 51, 66, 90]) {
      const janela = {inicio: 0, duracao};
      const e = progresso(0, janela, C);
      expect(e.presenca).toBeGreaterThan(0);
      expect(e.presenca).toBeCloseTo(POUSO(1 / C.entrada), 9);
      expect(e.escala).toBeLessThan(1 + C.overshoot);
      // a entrada fecha no ULTIMO frame dela, nao um frame depois
      expect(progresso(C.entrada - 1, janela, C).presenca).toBeCloseTo(1, 9);
    }
  });

  it('as tres fases aparecem, na ordem, sem buraco', () => {
    const vistas: string[] = [];
    for (let f = 10; f < 70; f++) {
      const fase = progresso(f, j, C).fase;
      expect(fase).not.toBe('antes');
      expect(fase).not.toBe('depois');
      if (vistas[vistas.length - 1] !== fase) vistas.push(fase);
    }
    expect(vistas).toEqual(['entrada', 'hold', 'saida']);
  });

  it('a escala pousa de 1+overshoot para 1 e sai encolhendo: uma direcao so', () => {
    // A escala do frame ANTERIOR ao primeiro desenhado seria 1 + overshoot; o
    // primeiro DESENHADO ja pousou um pedaco: 1 + 0,03 * (1 - POUSO(1/12)) =
    // 1,019975 (medido). O teto 1 + overshoot continua valendo como limite, e e
    // ele que o laco abaixo confere frame a frame.
    expect(progresso(10, j, C).escala).toBeCloseTo(1.019975, 6);
    expect(progresso(10, j, C).escala).toBeLessThan(1 + C.overshoot);
    expect(progresso(10 + C.entrada - 1, j, C).escala).toBeCloseTo(1, 6);
    expect(progresso(10 + C.entrada, j, C).escala).toBeCloseTo(1, 6);
    // nunca volta para cima em nenhum frame -- e isso que separa pouso de
    // easing elastico, que `proibicoes.md` proibe
    let anterior = Infinity;
    for (let f = 10; f <= 10 + 60; f++) {
      const s = progresso(f, j, C).escala;
      expect(s).toBeLessThanOrEqual(anterior + 1e-9);
      expect(s).toBeLessThanOrEqual(1 + C.overshoot + 1e-9);
      expect(s).toBeGreaterThanOrEqual(1 - C.overshoot - 1e-9);
      anterior = s;
    }
  });
});

// ---------------------------------------------------------------------------
describe('stagger entre irmaos', () => {
  it('o atraso do irmao i e i * C.stagger', () => {
    expect(atrasoDoIrmao(0, C)).toBe(0);
    expect(atrasoDoIrmao(1, C)).toBe(C.stagger);
    expect(atrasoDoIrmao(4, C)).toBe(4 * C.stagger);
  });

  it('a entrada de cada irmao comeca exatamente stagger frames depois', () => {
    const base = {inicio: 0, duracao: 60};
    const irmaos = [0, 1, 2, 3, 4].map((i) => ({
      inicio: base.inicio + atrasoDoIrmao(i, C),
      duracao: base.duracao,
    }));
    for (let i = 1; i < irmaos.length; i++) {
      expect(irmaos[i].inicio - irmaos[i - 1].inicio).toBe(C.stagger);
    }
    // e o primeiro frame em que cada irmao deixa de ser 'antes'
    for (let i = 0; i < irmaos.length; i++) {
      expect(progresso(atrasoDoIrmao(i, C) - 1, irmaos[i], C).fase).toBe('antes');
      expect(progresso(atrasoDoIrmao(i, C), irmaos[i], C).fase).toBe('entrada');
    }
  });

  it('a cena cresce o bastante para caber o ultimo irmao', () => {
    expect(duracaoComIrmaos(1, 60, C)).toBe(60);
    expect(duracaoComIrmaos(5, 60, C)).toBe(60 + 4 * C.stagger);
  });

  it('janelasDeIrmaos entrega uma janela por irmao, escalonada e de mesma duracao', () => {
    const js = janelasDeIrmaos(4, {inicio: 7, duracao: 45}, C);
    expect(js.length).toBe(4);
    expect(js.map((j) => j.inicio)).toEqual([
      7,
      7 + C.stagger,
      7 + 2 * C.stagger,
      7 + 3 * C.stagger,
    ]);
    expect(js.every((j) => j.duracao === 45)).toBe(true);
    // o ultimo irmao termina dentro da duracao que `duracaoComIrmaos` pede
    const ultimo = js[js.length - 1];
    expect(ultimo.inicio - 7 + ultimo.duracao).toBe(duracaoComIrmaos(4, 45, C));
  });

  it('nenhum irmao e pedido antes do primeiro', () => {
    expect(janelasDeIrmaos(0, {inicio: 0, duracao: 45}, C)).toEqual([]);
  });
});

// ---------------------------------------------------------------------------
describe('push de camera', () => {
  it('vai de PUSH.de a PUSH.para ao longo da cena, sem impacto', () => {
    expect(push(0, 120)).toBeCloseTo(PUSH.de, 6);
    expect(push(120, 120)).toBeCloseTo(PUSH.para, 6);
    let anterior = -1;
    for (let f = 0; f <= 120; f++) {
      const s = push(f, 120);
      expect(s).toBeGreaterThanOrEqual(anterior - 1e-9);
      expect(s).toBeLessThanOrEqual(PUSH.para + 1e-9);
      anterior = s;
    }
  });
});

// ---------------------------------------------------------------------------
describe('glifos medidos do .ttf', () => {
  it('IBM Plex Mono e monoespacada: prova de que a leitura de hmtx esta certa', () => {
    const larguras = new Set(Object.values(GLIFOS.dado));
    expect(larguras.size).toBe(1);
    expect([...larguras][0]).toBe(0.6);
  });

  it('larguraEm soma avancos e nunca devolve 0 para texto com conteudo', () => {
    expect(larguraEm('', 'manchete')).toBe(0);
    expect(larguraEm('CAFE', 'manchete')).toBeGreaterThan(0);
    expect(larguraEm('CAFE CANASTRA', 'manchete')).toBeGreaterThan(
      larguraEm('CAFE', 'manchete'),
    );
  });

  it('caractere fora da tabela nao vira largura 0', () => {
    // um emoji nao esta na tabela; se caisse em 0, um texto largo passaria por
    // estreito e estouraria a caixa em silencio
    expect(larguraEm('\u{1F600}', 'manchete')).toBeGreaterThan(0);
  });

  it('a entrelinha natural vem do arquivo, nao do olho', () => {
    expect(METRICAS.manchete.alturaLinha).toBeCloseTo(
      METRICAS.manchete.ascender - METRICAS.manchete.descender + METRICAS.manchete.lineGap,
      4,
    );
    expect(METRICAS.manchete.alturaLinha).toBeGreaterThan(1);
  });
});

// ---------------------------------------------------------------------------
describe('quebrar', () => {
  const arg = {papel: 'manchete' as const, corpo: 100, largura: 800};

  it('nao perde nem reordena palavra', () => {
    const t = 'CAFE ESPECIAL DA SERRA DA CANASTRA TORRADO AQUI';
    expect(quebrar(t, arg).join(' ')).toBe(t);
  });

  it('nenhuma linha passa da largura, quando cabe palavra a palavra', () => {
    for (const l of quebrar('CAFE ESPECIAL DA SERRA DA CANASTRA', arg)) {
      expect(larguraEm(l, 'manchete') * arg.corpo).toBeLessThanOrEqual(arg.largura + 1e-6);
    }
  });

  it('palavra sozinha maior que a caixa fica na propria linha', () => {
    const linhas = quebrar('DO CANASTRAAAAAAAAAAAAAAAAAAAA ja', {...arg, largura: 300});
    expect(linhas).toContain('CANASTRAAAAAAAAAAAAAAAAAAAA');
  });

  it('texto vazio nao gera linha fantasma', () => {
    expect(quebrar('   ', arg)).toEqual([]);
  });
});

// ---------------------------------------------------------------------------
describe('duracaoDaFrase', () => {
  it('conta o stagger de todas as palavras, nao so a duracao de uma', () => {
    // O erro que esta funcao existe para impedir: dimensionar a Sequence por
    // C.duracaoMinima e cortar a saida da ultima palavra.
    expect(duracaoDaFrase('CAFE', C)).toBe(C.duracaoMinima);
    expect(duracaoDaFrase('CAFE DA CANASTRA', C)).toBeGreaterThan(C.duracaoMinima);
    // 3 palavras: janela de cada uma cresce 2*stagger, e a cena cresce outro
    // 2*stagger por causa do atraso do ultimo irmao.
    expect(duracaoDaFrase('CAFE DA CANASTRA', C)).toBe(C.duracaoMinima + 4 * C.stagger);
  });

  it('a ultima palavra termina dentro da duracao devolvida', () => {
    const texto = 'CAFE ESPECIAL DA SERRA DA CANASTRA';
    const total = duracaoDaFrase(texto, C);
    const porPalavra = duracaoPorPalavra(texto, C);
    const f = formaTextoTela({texto, modo: 'cartela', zonas: zonasDe(1080, 1920), cadencia: C});
    const ultima = f.palavras[f.palavras.length - 1];
    expect(ultima.atrasoFrames + porPalavra).toBeLessThanOrEqual(total);
    // e no frame final do total a ultima palavra ja saiu
    expect(
      progresso(total, {inicio: ultima.atrasoFrames, duracao: porPalavra}, C).presenca,
    ).toBe(0);
  });

  it('EXISTE um trecho em que a frase inteira esta cheia, e dura holdFinal', () => {
    // O DEFEITO QUE ESTE TESTE PEGA, e que os outros 51 deixaram passar:
    //
    // com `C.duracaoMinima` para todas as palavras, o stagger empurra so o
    // comeco. Visto no still do frame 30 de uma manchete de 6 palavras: 'CAFE'
    // ja estava em 0,81 de presenca, saindo, e 'CANASTRA' ainda entrando --
    // nao havia UM frame com a manchete legivel inteira. Passa despercebido em
    // teste de unidade porque cada palavra, sozinha, esta perfeita.
    for (const texto of [
      'CAFE',
      'CAFE DA CANASTRA',
      'CAFE ESPECIAL DA SERRA DA CANASTRA',
      'TORRAMOS AQUI NA FAZENDA E MANDAMOS NO MESMO DIA EM QUE SAI DO TAMBOR',
    ]) {
      const n = texto.split(/\s+/).filter(Boolean).length;
      const porPalavra = duracaoPorPalavra(texto, C);
      const total = duracaoDaFrase(texto, C);

      let cheios = 0;
      for (let t = 0; t <= total; t++) {
        const todas = Array.from({length: n}, (_, i) =>
          progresso(t, {inicio: atrasoDoIrmao(i, C), duracao: porPalavra}, C),
        );
        if (todas.every((e) => e.presenca >= 1 - 1e-9)) cheios++;
      }
      expect(cheios).toBeGreaterThanOrEqual(C.holdFinal);
    }
  });

  it('texto sem palavra nao gera cena', () => {
    expect(duracaoDaFrase('   ', C)).toBe(0);
  });
});

// ---------------------------------------------------------------------------
describe('formaTextoTela: area segura', () => {
  const dentro = (c: {x: number; y: number; largura: number; altura: number}, s: typeof c) => {
    expect(c.x).toBeGreaterThanOrEqual(s.x - 1e-6);
    expect(c.y).toBeGreaterThanOrEqual(s.y - 1e-6);
    expect(c.x + c.largura).toBeLessThanOrEqual(s.x + s.largura + 1e-6);
    expect(c.y + c.altura).toBeLessThanOrEqual(s.y + s.altura + 1e-6);
  };

  it('a caixa fica dentro do seguro nos dois modos e nos tres formatos', () => {
    for (const [w, h] of FORMATOS) {
      const z = zonasDe(w, h);
      for (const modo of ['sobreImagem', 'cartela'] as const) {
        const f = formaTextoTela({
          texto: 'CAFE ESPECIAL DA SERRA DA CANASTRA',
          modo,
          zonas: z, cadencia: C});
        dentro(f.caixa, z.seguro);
      }
    }
  });

  it('o bloco de texto cabe na caixa, inclusive num texto longo', () => {
    const textos = [
      'CAFE',
      'CAFE ESPECIAL DA SERRA DA CANASTRA',
      'TORRAMOS AQUI NA FAZENDA E MANDAMOS PARA A SUA CASA NO MESMO DIA EM QUE SAI DO TAMBOR',
    ];
    for (const [w, h] of FORMATOS) {
      const z = zonasDe(w, h);
      for (const modo of ['sobreImagem', 'cartela'] as const) {
        for (const texto of textos) {
          const f = formaTextoTela({texto, modo, zonas: z, cadencia: C});
          expect(f.larguraBloco).toBeLessThanOrEqual(f.caixa.largura + 1e-6);
          expect(f.alturaBloco).toBeLessThanOrEqual(f.caixa.altura + 1e-6);
          expect(f.corpo).toBeGreaterThan(0);
        }
      }
    }
  });

  it('texto mais longo recebe corpo menor ou igual', () => {
    const z = zonasDe(1080, 1920);
    const curto = formaTextoTela({texto: 'CAFE', modo: 'cartela', zonas: z, cadencia: C});
    const longo = formaTextoTela({
      texto: 'TORRAMOS AQUI NA FAZENDA E MANDAMOS NO MESMO DIA',
      modo: 'cartela',
      zonas: z, cadencia: C});
    expect(longo.corpo).toBeLessThan(curto.corpo);
  });
});

// ---------------------------------------------------------------------------
describe('formaTextoTela: os dois modos sao geometrias diferentes', () => {
  const z = zonasDe(1080, 1920);
  const texto = 'CAFE ESPECIAL DA SERRA DA CANASTRA';
  const sobre = formaTextoTela({texto, modo: 'sobreImagem', zonas: z, cadencia: C});
  const cartela = formaTextoTela({texto, modo: 'cartela', zonas: z, cadencia: C});

  it('a caixa nao e a mesma', () => {
    const mesma =
      sobre.caixa.x === cartela.caixa.x &&
      sobre.caixa.y === cartela.caixa.y &&
      sobre.caixa.largura === cartela.caixa.largura &&
      sobre.caixa.altura === cartela.caixa.altura;
    expect(mesma).toBe(false);
  });

  it('a cartela e mais alta: ela ocupa a area segura, a manchete so a faixa', () => {
    expect(cartela.caixa.altura).toBeGreaterThan(sobre.caixa.altura);
  });

  it('so a cartela tem fundo, e ele e COR.terra', () => {
    expect(cartela.fundo).toBe(COR.terra);
    expect(sobre.fundo).toBeNull();
  });

  it('so o sobreImagem tem sombra, e ela e o perfil sobreVideo', () => {
    expect(sobre.sombra).not.toBeNull();
    expect(sobre.sombra?.perfil).toBe('sobreVideo');
    expect(cartela.sombra).toBeNull();
  });

  it('o respiro da cartela e a entrelinha natural da fonte; a manchete e apertada', () => {
    expect(cartela.entrelinha).toBeCloseTo(METRICAS.manchete.alturaLinha, 4);
    expect(sobre.entrelinha).toBeCloseTo(LEGENDA.entrelinha, 4);
    expect(cartela.entrelinha).toBeGreaterThan(sobre.entrelinha);
  });

  it('a cartela guarda uma linha inteira de folga vertical, em todo formato', () => {
    // Sem esta reserva a cartela so MAXIMIZA o corpo, e no 16:9 o bloco media
    // 368,8 px numa caixa de 368,9 -- texto de borda a borda, que e o contrario
    // do respiro que o modo existe para ter.
    for (const [w, h] of FORMATOS) {
      const z = zonasDe(w, h);
      const c = formaTextoTela({texto, modo: 'cartela', zonas: z, cadencia: C});
      expect(c.alturaBloco + c.corpo * c.entrelinha).toBeLessThanOrEqual(
        c.caixa.altura + 1e-6,
      );
    }
  });

  it('a cartela respira mais que a manchete: sobra relativa maior', () => {
    const sobraCartela = (cartela.caixa.altura - cartela.alturaBloco) / cartela.caixa.altura;
    const sobraSobre = (sobre.caixa.altura - sobre.alturaBloco) / sobre.caixa.altura;
    expect(sobraCartela).toBeGreaterThan(sobraSobre);
  });

  it('a cartela centraliza o bloco; a manchete ancora no topo', () => {
    expect(cartela.alinhaVertical).toBe('center');
    expect(sobre.alinhaVertical).toBe('flex-start');
  });

  it('as duas quebram o texto de forma diferente ou em corpo diferente', () => {
    const igual =
      sobre.corpo === cartela.corpo &&
      sobre.linhas.join('|') === cartela.linhas.join('|');
    expect(igual).toBe(false);
  });
});

// ---------------------------------------------------------------------------
describe('formaTextoTela: acento e papel', () => {
  const z = zonasDe(1080, 1920);

  it('no maximo uma palavra recebe o acento de cor', () => {
    const f = formaTextoTela({
      texto: 'CAFE ESPECIAL DA CANASTRA',
      modo: 'cartela',
      zonas: z,
      palavraAcento: 1, cadencia: C});
    const acentuadas = f.palavras.filter((p) => p.cor === COR.acento);
    expect(acentuadas.length).toBe(1);
    expect(acentuadas[0].texto).toBe('ESPECIAL');
  });

  it('sem palavraAcento nenhuma palavra usa o acento', () => {
    const f = formaTextoTela({texto: 'CAFE DA CANASTRA', modo: 'cartela', zonas: z, cadencia: C});
    expect(f.palavras.every((p) => p.cor !== COR.acento)).toBe(true);
  });

  it('indice de acento fora da faixa nao pinta nada e nao explode', () => {
    const f = formaTextoTela({
      texto: 'CAFE DA CANASTRA',
      modo: 'cartela',
      zonas: z,
      palavraAcento: 99, cadencia: C});
    expect(f.palavras.every((p) => p.cor !== COR.acento)).toBe(true);
  });

  it('as palavras saem na ordem do texto, com o indice de irmao para o stagger', () => {
    const f = formaTextoTela({
      texto: 'CAFE ESPECIAL DA CANASTRA',
      modo: 'sobreImagem',
      zonas: z, cadencia: C});
    expect(f.palavras.map((p) => p.texto)).toEqual(['CAFE', 'ESPECIAL', 'DA', 'CANASTRA']);
    expect(f.palavras.map((p) => p.irmao)).toEqual([0, 1, 2, 3]);
  });

  it('papel dado usa a familia de dado, nao a de manchete', () => {
    const f = formaTextoTela({
      texto: '250 G',
      modo: 'sobreImagem',
      zonas: z,
      papel: 'dado', cadencia: C});
    expect(f.papel).toBe('dado');
    expect(f.entrelinha).toBeGreaterThan(0);
  });
});
