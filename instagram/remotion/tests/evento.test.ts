// As tabelas de papel, e o `irmaos` que faz plano e pixel contarem a MESMA coisa.
import {describe, expect, it} from 'vitest';
import {
  CADENCIA_DO_PAPEL,
  FAMILIA_DO_PAPEL,
  PAPEIS_DE_EVENTO,
  PISTA_PADRAO,
} from '../src/motor/evento';
import {CONFLITO_DE_PISTA, PISTAS, PISTAS_DE_EVENTO} from '../src/motor/pista';
import {cadencia} from '../src/motor/cadencia';
import {formaTextoTela} from '../src/motor/camadas/texto-forma';
import {layout} from '../src/motor/layout';

const Z = layout({largura: 1080, altura: 1920, razaoFonte: 9 / 16});
const C = cadencia(30);

describe('tabelas de papel', () => {
  it('todo papel de evento tem familia, cadencia e pista sugerida', () => {
    for (const p of PAPEIS_DE_EVENTO) {
      expect(FAMILIA_DO_PAPEL[p], p).toBeDefined();
      expect(CADENCIA_DO_PAPEL[p], p).toBeDefined();
      expect(PISTA_PADRAO[p], p).toBeDefined();
    }
  });

  it('`etiqueta` NAO indexa GLIFOS direto: a familia dela e `dado`', () => {
    // Medido em 30/09/2026: `papel: 'etiqueta'` indexado direto em GLIFOS lancava
    // `TypeError: Cannot read properties of undefined (reading 'x')`.
    expect(FAMILIA_DO_PAPEL.etiqueta).toBe('dado');
    expect(FAMILIA_DO_PAPEL.legenda).toBe('corpo');
  });

  it('nenhuma pista sugerida e `rodape`: ela e a caixa da Legenda', () => {
    for (const p of PAPEIS_DE_EVENTO) expect(PISTA_PADRAO[p]).not.toBe('rodape');
    expect(PISTAS_DE_EVENTO).not.toContain('rodape');
  });

  it('CONFLITO_DE_PISTA cobre as quatro pistas e e simetrico onde conflita', () => {
    for (const p of PISTAS) expect(CONFLITO_DE_PISTA[p], p).toBeDefined();
    // `tela` conflita com topo e principal; eles conflitam com ela.
    expect(CONFLITO_DE_PISTA.tela).toContain('topo');
    expect(CONFLITO_DE_PISTA.topo).toContain('tela');
    // `rodape` nao conflita com a cartela: a legenda corre por cima do terra.
    expect(CONFLITO_DE_PISTA.tela).not.toContain('rodape');
    expect(CONFLITO_DE_PISTA.rodape).not.toContain('tela');
  });
});

describe('forma: familia, cadencia e irmaos', () => {
  it('manchete escalona por PALAVRA: irmaos = numero de palavras', () => {
    const f = formaTextoTela({
      texto: 'SUA PROPRIA MARCA', modo: 'cartela', zonas: Z, papel: 'manchete', cadencia: C,
    });
    expect(f.familia).toBe('manchete');
    expect(f.cadenciaTexto).toBe('palavra');
    expect(f.irmaos).toBe(3);
    expect(f.palavras.map((p) => p.irmao)).toEqual([0, 1, 2]);
  });

  it('etiqueta escalona por BLOCO: 3 palavras, 1 irmao, todos atraso 0', () => {
    // O defeito medido: o plano dava 36 frames (1 irmao) e a tela desenhava 42
    // (3 palavras). `forma.irmaos` e a unica contagem.
    const f = formaTextoTela({
      texto: 'MEDEIROS 1250 M', modo: 'sobreImagem', zonas: Z, papel: 'etiqueta', cadencia: C,
    });
    expect(f.familia).toBe('dado');
    expect(f.cadenciaTexto).toBe('bloco');
    expect(f.irmaos).toBe(1);
    expect(f.palavras.map((p) => p.irmao)).toEqual([0, 0, 0]);
    expect(f.palavras.map((p) => p.atrasoFrames)).toEqual([0, 0, 0]);
  });

  it('dado escalona por LINHA: irmaos = numero de linhas, nao de palavras', () => {
    // Caixa estreita de proposito, para forcar mais de uma linha.
    const estreito = {...Z, manchete: {x: 160, y: 96, largura: 260, altura: 500}};
    const f = formaTextoTela({
      texto: 'R$ 39,90 O QUILO', modo: 'sobreImagem', zonas: estreito, papel: 'dado', cadencia: C,
    });
    expect(f.cadenciaTexto).toBe('linha');
    expect(f.linhas.length).toBeGreaterThan(1);
    expect(f.irmaos).toBe(f.linhas.length);
    // Palavras da MESMA linha entram juntas: mesmo irmao, mesmo atraso.
    const daPrimeira = f.palavras.filter((p) => p.linha === 0);
    expect(new Set(daPrimeira.map((p) => p.atrasoFrames)).size).toBe(1);
  });

  it('o acento continua indexado pela PALAVRA, nao pelo irmao', () => {
    // Numa etiqueta todos os irmaos sao 0: indexar por irmao pintaria o bloco todo.
    const f = formaTextoTela({
      texto: 'MEDEIROS 1250 M', modo: 'sobreImagem', zonas: Z, papel: 'etiqueta',
      palavraAcento: 1, cadencia: C,
    });
    const acentuadas = f.palavras.filter((p) => p.cor === '#C8661E');
    expect(acentuadas.length).toBe(1);
    expect(acentuadas[0].texto).toBe('1250');
  });
});
