// A MEDICAO DO TEXTO NA CAIXA DA PISTA, e o veredito de dominancia.
//
// O que este arquivo prova que `pistas.test.ts` nao prova: que a mancha do texto na
// pista e COMPARAVEL com a mancha da legenda no mesmo quadro, e que o modulo NAO tem
// plano B -- ele relata `domina: false` em vez de promover nada a cartela.
import {describe, expect, it} from 'vitest';
import {cadencia} from '../src/motor/cadencia';
import {
  dominanciaDaLegenda,
  FATOR_DE_DOMINANCIA,
  linhaMaximaDoQuadro,
  PAPEIS_QUE_DOMINAM,
  pisoDeDominancia,
  resolverEncaixe,
  TETO_DE_LINHA,
} from '../src/motor/encaixe';
import {layout} from '../src/motor/layout';
import {caixaDaPista} from '../src/motor/pista';

const C = cadencia(30);
const FRASE = 'SUA PROPRIA MARCA DE CAFE';

describe('piso de dominancia', () => {
  it('o piso e 1,25x a mancha da legenda de duas linhas, no MESMO quadro', () => {
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 0.5625});
    expect(pisoDeDominancia(z)).toBeCloseTo(FATOR_DE_DOMINANCIA * dominanciaDaLegenda(z), 12);
  });

  it('a mancha da legenda e uma FRACAO do quadro, entre 0 e 1', () => {
    for (const [w, h] of [[1080, 1920], [1080, 1080], [1080, 1350], [1920, 1080]]) {
      for (const rf of [0.5625, 4 / 3]) {
        const d = dominanciaDaLegenda(layout({largura: w, altura: h, razaoFonte: rf}));
        expect(d, `${w}x${h} rf ${rf}`).toBeGreaterThan(0);
        expect(d, `${w}x${h} rf ${rf}`).toBeLessThan(1);
      }
    }
  });

  it('o piso MUDA com o formato: um numero absoluto nao capturaria o defeito', () => {
    // O defeito que o piso existe para pegar e "o elemento que deveria dominar e
    // menor que a legenda". Um piso absoluto em % do quadro passaria numa peca sem
    // legenda e reprovaria numa com legenda grande.
    const a = pisoDeDominancia(layout({largura: 1080, altura: 1920, razaoFonte: 0.5625}));
    const b = pisoDeDominancia(layout({largura: 1080, altura: 1080, razaoFonte: 4 / 3}));
    expect(a).not.toBeCloseTo(b, 4);
  });
});

describe('resolverEncaixe', () => {
  it('o encaixe que ele devolve e o DERIVADO da pista, nao uma escolha dele', () => {
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 0.5625});
    expect(resolverEncaixe({texto: FRASE, papel: 'manchete', pista: 'topo', zonas: z, cadencia: C}).encaixe).toBe('faixa');
    expect(resolverEncaixe({texto: FRASE, papel: 'manchete', pista: 'tela', zonas: z, cadencia: C}).encaixe).toBe('cartela');
    const zz = layout({largura: 1080, altura: 1080, razaoFonte: 0.5625});
    expect(resolverEncaixe({texto: FRASE, papel: 'manchete', pista: 'topo', zonas: zz, cadencia: C}).encaixe).toBe('coluna');
  });

  it('NAO promove a cartela quando o texto nao domina: relata e segue', () => {
    // A versao anterior recebia `preferencias` e promovia. Duas consequencias: o
    // briefing pedia uma coisa e a peca entregava outra em silencio, e com fonte em
    // paisagem a promocao disparava em TODO evento -- terra chapado cobrindo as fotos.
    const z = layout({largura: 1080, altura: 1350, razaoFonte: 0.5625});
    const r = resolverEncaixe({texto: FRASE, papel: 'manchete', pista: 'topo', zonas: z, cadencia: C});
    expect(r.encaixe).toBe('coluna');
    expect(r.modo).toBe('sobreImagem');
    // Qualquer que seja o veredito, ele NAO virou cartela.
    expect(r.modo).not.toBe('cartela');
    expect(typeof r.domina).toBe('boolean');
  });

  it('a cartela domina folgado e a coluna estreita do 4:5 nao domina', () => {
    const z = layout({largura: 1080, altura: 1350, razaoFonte: 0.5625});
    const cartela = resolverEncaixe({texto: FRASE, papel: 'manchete', pista: 'tela', zonas: z, cadencia: C});
    const coluna = resolverEncaixe({texto: FRASE, papel: 'manchete', pista: 'topo', zonas: z, cadencia: C});
    expect(cartela.dominancia).toBeGreaterThan(cartela.piso);
    expect(cartela.domina).toBe(true);
    expect(coluna.dominancia).toBeLessThan(cartela.dominancia);
  });

  it('`etiqueta` NAO e candidata a dominar, e o porque diz isso', () => {
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 0.5625});
    const r = resolverEncaixe({texto: 'MEDEIROS 1250 M', papel: 'etiqueta', pista: 'topo', zonas: z, cadencia: C});
    expect(r.candidataADominar).toBe(false);
    expect(PAPEIS_QUE_DOMINAM).not.toContain('etiqueta');
    expect(r.porque).toMatch(/nao e candidato a dominar/);
  });

  it('o `porque` carrega os DOIS numeros quando o papel domina', () => {
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 0.5625});
    const r = resolverEncaixe({texto: FRASE, papel: 'manchete', pista: 'tela', zonas: z, cadencia: C});
    expect(r.porque).toMatch(/mancha/);
    expect(r.porque).toMatch(/piso/);
    expect(r.porque).toMatch(/DOMINA/);
    // Numero com virgula decimal: e relatorio em pt-BR, nao log de maquina.
    expect(r.porque).toMatch(/\d+,\d+%/);
  });

  it('a caixa medida e a caixa da PISTA, e o corpo cabe nela', () => {
    const z = layout({largura: 1080, altura: 1080, razaoFonte: 0.5625});
    const r = resolverEncaixe({texto: FRASE, papel: 'manchete', pista: 'principal', zonas: z, cadencia: C});
    const pista = caixaDaPista('principal', z);
    expect(r.forma.larguraBloco).toBeLessThanOrEqual(pista.largura + 1e-6);
    expect(r.forma.alturaBloco).toBeLessThanOrEqual(pista.altura + 1e-6);
    expect(r.corpo).toBeGreaterThan(1);
  });

  it('o corpo nunca cai em 1 nas 8 combinacoes: 1 e texto ilegivel com exit 0', () => {
    for (const rf of [0.5625, 4 / 3]) {
      for (const [w, h] of [[1080, 1920], [1080, 1080], [1080, 1350], [1920, 1080]]) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        for (const pista of ['topo', 'principal', 'tela'] as const) {
          const r = resolverEncaixe({texto: FRASE, papel: 'manchete', pista, zonas: z, cadencia: C});
          expect(r.corpo, `${w}x${h} rf ${rf} ${pista}`).toBeGreaterThan(8);
        }
      }
    }
  });

  it('caixa degenerada LANCA, em vez de desenhar corpo 1', () => {
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 0.5625});
    const degenerado = {...z, legenda: {x: 0, y: 0, largura: 0.5, altura: 0.5}};
    expect(() =>
      resolverEncaixe({texto: FRASE, papel: 'manchete', pista: 'rodape', zonas: degenerado, cadencia: C}),
    ).toThrow(/degenerada/);
  });
});

// ---------------------------------------------------------------------------
// O TETO DE DOMINANCIA
//
// O caso que originou tudo: `250 G`, papel `dado`, pista `principal`, 9:16. A caixa de
// `principal` tem 788,74 px de altura, a busca MAXIMIZA, e cinco caracteres saiam com
// corpo 410 px -- mancha de 28,017% do quadro, aprovada como DOMINA, cobrindo o
// logotipo do pacote (still `out/antes-f261.png`).

describe('teto de linha', () => {
  const Z916 = layout({largura: 1080, altura: 1920, razaoFonte: 0.5625});
  const Z169 = layout({largura: 1920, altura: 1080, razaoFonte: 0.5625});
  const dado = (zonas: ReturnType<typeof layout>, pista: 'topo' | 'principal' | 'tela') =>
    resolverEncaixe({texto: '250 G', papel: 'dado', pista, zonas, cadencia: C});

  it('o `250 G` que saia com corpo 410 px agora para no teto', () => {
    const r = dado(Z916, 'principal');
    // 0,155 * 1920 / 0,96 = 310. O numero exato, nao "menor que antes".
    expect(r.corpo).toBe(310);
    expect(r.noTeto).toBe(true);
    expect(r.linha).toBeCloseTo(TETO_DE_LINHA, 6);
    // E continua dominando: o teto nao o empurrou abaixo do piso neste formato.
    expect(r.domina).toBe(true);
    expect(r.porque).toMatch(/SEGURADO PELO TETO/);
  });

  it('a caixa da pista aceitaria MAIS que o teto -- e por isso ele existe', () => {
    // Sem o teto a busca iria ate aqui. Prova que o limite e do QUADRO, nao da caixa.
    const pista = caixaDaPista('principal', Z916);
    const corpoQueACaixaAceita = Math.floor(pista.altura / 0.96 / 2);
    expect(corpoQueACaixaAceita).toBeGreaterThan(dado(Z916, 'principal').corpo);
    expect(dado(Z916, 'principal').forma.alturaBloco).toBeLessThan(pista.altura);
  });

  it('nenhuma linha passa do teto em nenhum encaixe sobre imagem', () => {
    for (const [w, h] of [[1080, 1920], [1080, 1080], [1080, 1350], [1920, 1080]]) {
      for (const rf of [0.5625, 4 / 3]) {
        const z = layout({largura: w, altura: h, razaoFonte: rf});
        for (const pista of ['topo', 'principal'] as const) {
          const r = resolverEncaixe({texto: FRASE, papel: 'manchete', pista, zonas: z, cadencia: C});
          expect(r.linha, `${w}x${h} rf ${rf} ${pista}`).toBeLessThanOrEqual(
            TETO_DE_LINHA + 1e-9,
          );
        }
      }
    }
  });

  it('a CARTELA nao tem teto: ela pinta o proprio fundo, nao ha o que tapar', () => {
    expect(linhaMaximaDoQuadro(Z169, 'cartela')).toBeNull();
    expect(linhaMaximaDoQuadro(Z169, 'sobreImagem')).toBeCloseTo(TETO_DE_LINHA * 1080, 9);
    const r = resolverEncaixe({
      texto: 'SUA PRÓPRIA MARCA', papel: 'manchete', pista: 'tela', zonas: Z169, cadencia: C,
    });
    // Medido: 19,75% da altura, acima do teto, e correto -- e um cartao de texto.
    expect(r.tetoDeLinha).toBeNull();
    expect(r.noTeto).toBe(false);
    expect(r.linha).toBeGreaterThan(TETO_DE_LINHA);
  });

  it('o teto NAO baixa o corpo de quem nao o alcanca', () => {
    // 32 dos 36 pares (texto, formato) da varredura ficam identicos. Dois deles:
    expect(
      resolverEncaixe({
        texto: '2 · CEREJA VERDE', papel: 'etiqueta', pista: 'topo', zonas: Z916, cadencia: C,
      }).corpo,
    ).toBe(126);
    expect(
      resolverEncaixe({
        texto: 'MEDEIROS 1250 M', papel: 'etiqueta', pista: 'topo', zonas: Z916, cadencia: C,
      }).corpo,
    ).toBe(158);
  });

  it('PISO E TETO CONVIVEM: quando o intervalo e vazio, `semCorpoValido`', () => {
    // O mesmo `250 G`, no 16:9. O teto limita o corpo a 174 px; nesse corpo a mancha e
    // 4,205%, abaixo do piso de 4,728%. Corpo maior tapa, corpo menor domina menos:
    // nao existe corpo valido, e escolher um seria escolher um corpo ruim em silencio.
    const r = dado(Z169, 'principal');
    expect(r.noTeto).toBe(true);
    expect(r.corpo).toBe(174);
    expect(r.domina).toBe(false);
    expect(r.semCorpoValido).toBe(true);
    expect(r.porque).toMatch(/NAO HA CORPO VALIDO/);
    // E no 9:16 o MESMO texto tem corpo valido: a recusa e por formato, nao por texto.
    expect(dado(Z916, 'principal').semCorpoValido).toBe(false);
  });

  it('`etiqueta` para no teto mas NUNCA e `semCorpoValido`', () => {
    // 16:9 com fonte em PAISAGEM: o video preenche o quadro, entao o encaixe e `faixa`
    // e a caixa de `topo` e larga -- e o que fazia `1 · NO PÉ` sair com corpo 213.
    const z = layout({largura: 1920, altura: 1080, razaoFonte: 16 / 9});
    const r = resolverEncaixe({
      texto: '1 · NO PÉ', papel: 'etiqueta', pista: 'topo', zonas: z, cadencia: C,
    });
    expect(r.noTeto).toBe(true);
    expect(r.corpo).toBe(174); // era 213 antes do teto
    expect(r.candidataADominar).toBe(false);
    expect(r.semCorpoValido).toBe(false);
    expect(r.porque).toMatch(/SEGURADO PELO TETO/);
  });

  it('nao domina POR CAIXA APERTADA continua relatando, nao lancando', () => {
    // 4:5 com fonte retrato: a coluna e estreita e o texto nao alcanca o piso. O teto
    // nao tem nada a ver com isso, e o modulo tem que seguir relatando `domina: false`.
    const z = layout({largura: 1080, altura: 1350, razaoFonte: 0.5625});
    const r = dado(z, 'principal');
    expect(r.noTeto).toBe(false);
    expect(r.domina).toBe(false);
    expect(r.porque).toMatch(/NAO DOMINA/);
  });
});
