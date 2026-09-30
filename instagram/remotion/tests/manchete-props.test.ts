// Portao da MANCHETE do projeto 01-private-label.
//
// O DEFEITO QUE ESTE ARQUIVO EXISTE PARA PEGAR
//
// `manchete.texto` e o unico campo de texto livre do props.json que vai
// QUEIMADO no quadro. O props.json nasceu justamente porque a versao anterior
// dele trazia 20 blocos de legenda escritos a mao, e quatro MP4 foram entregues
// com essa frase inventada gravada no video (ver o cabecalho de
// `scripts/gerar-props.mjs`). A manchete reabre exatamente aquela porta: nada no
// tipo de `Manchete` impede alguem de escrever "TRANSFORME SEU SONHO EM LUCRO" e
// renderizar.
//
// Entao aqui a manchete e CONFERIDA CONTRA A FALA, nao contra o gosto de quem
// escreveu: o texto tem que ser um trecho CONTIGUO de `transcricao.json`, com
// caixa alta como unica transformacao permitida. Palavra acrescentada, trocada
// ou reordenada reprova.
//
// O QUE ESTE ARQUIVO NAO FAZ
//
// Nao renderiza e nao importa `PecaVideo.tsx`. Aquele arquivo importa
// `tipografia.ts`, que faz `loadFont` no topo do modulo e derruba o vitest em
// Node com `TypeError: Invalid URL` -- a mesma razao pela qual a geometria mora
// em `texto-forma.ts`. Logo a conta da montagem (`inicioFrame -
// cortarAntesFrames`) e refeita aqui a mao: se a montagem trocar de convencao,
// este teste continua verde e so o still denuncia. E por isso que o still de
// cada variante entra no material de decisao, e nao so o resultado do vitest.

import {describe, it, expect} from 'vitest';
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {duracaoDaFrase, formaTextoTela} from '../src/motor/camadas/texto-forma';
import {layout} from '../src/motor/layout';
import {LEGENDA} from '../src/identidade/tokens';

// Caminho resolvido a partir do arquivo de teste, nao do cwd.
const ler = (rel: string) =>
  JSON.parse(fs.readFileSync(fileURLToPath(new URL(rel, import.meta.url)), 'utf8'));

type Palavra = {texto: string; inicioMs: number; fimMs: number};

const PROJETO = '../projetos/01-private-label';
const props = ler(`${PROJETO}/props.json`);
const palavras: Palavra[] = ler(`${PROJETO}/transcricao.json`);

const baixo = (s: string) => s.toLocaleLowerCase('pt-BR');

/** Os dois formatos de peca registrados em `Raiz.tsx`. */
const FORMATOS: Array<[number, number]> = [
  [1080, 1920],
  [1080, 1080],
];

// ---------------------------------------------------------------------------
describe('a manchete e opcional', () => {
  it('texto ausente ou em branco nao gera palavra nem cena', () => {
    // Nao existe texto de reserva: a peca sem manchete esta completa, nao
    // quebrada. `PecaVideo` trata `null` e texto em branco como ausencia, e a
    // prova de que o resto do motor aguenta isso e que a geometria nao produz
    // palavra nenhuma e a cena dura zero frame.
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 9 / 16});
    for (const vazio of ['', '   ', '\n']) {
      for (const modo of ['sobreImagem', 'cartela'] as const) {
        expect(formaTextoTela({texto: vazio, modo, zonas: z}).palavras).toEqual([]);
      }
      expect(duracaoDaFrase(vazio)).toBe(0);
    }
  });
});

// ---------------------------------------------------------------------------
// Daqui para baixo tudo depende de ESTE projeto declarar manchete. Se ela sair
// do props.json um dia, os blocos sao pulados e o teste de cima continua valendo.

type MancheteProps = {
  texto: string;
  modo: 'sobreImagem' | 'cartela';
  inicioFrame: number;
  palavraAcento?: number;
};
type Proveniencia = {
  citacao: string;
  dePalavra: number;
  atePalavra: number;
  inicioMs: number;
  fimMs: number;
  fps: number;
  palavraAcentoTexto?: string;
};

const m = props.manchete as MancheteProps | null | undefined;
const prov = props._manchete as Proveniencia | undefined;
const semManchete = !m || m.texto.trim().length === 0;

describe.skipIf(semManchete)('a manchete declarada e CITACAO LITERAL da fala', () => {
  it('traz proveniencia estruturada, nao so uma frase', () => {
    // Texto sem origem declarada e indistinguivel de copy inventada.
    expect(prov, 'props.json tem "manchete" e nao tem "_manchete"').toBeTruthy();
    expect(Number.isInteger(prov!.dePalavra)).toBe(true);
    expect(Number.isInteger(prov!.atePalavra)).toBe(true);
    expect(prov!.atePalavra).toBeGreaterThanOrEqual(prov!.dePalavra);
    expect(prov!.atePalavra).toBeLessThan(palavras.length);
  });

  it('os indices declarados recortam EXATAMENTE a citacao declarada', () => {
    const trecho = palavras
      .slice(prov!.dePalavra, prov!.atePalavra + 1)
      .map((p) => p.texto)
      .join(' ');
    expect(trecho).toBe(prov!.citacao);
  });

  it('a citacao e um trecho contiguo da transcricao, e nos indices declarados', () => {
    // Busca independente dos indices: se `dePalavra` estiver trocado mas a frase
    // existir em outro lugar, o teste acima passa e este pega o indice errado.
    const alvo = baixo(prov!.citacao).split(/\s+/).join(' ');
    const achados: number[] = [];
    const n = alvo.split(' ').length;
    for (let i = 0; i + n <= palavras.length; i++) {
      const janela = palavras.slice(i, i + n).map((p) => baixo(p.texto)).join(' ');
      if (janela === alvo) achados.push(i);
    }
    expect(achados, 'a citacao nao aparece contigua na transcricao').toContain(
      prov!.dePalavra,
    );
  });

  it('o texto renderizado difere da citacao SO na caixa', () => {
    // A unica transformacao permitida. Letra a mais, acento retirado ou
    // pontuacao inventada reprovam aqui.
    expect(baixo(m!.texto)).toBe(baixo(prov!.citacao));
  });

  it('nenhuma palavra foi acrescentada, trocada ou reordenada', () => {
    const daManchete = m!.texto.split(/\s+/).filter(Boolean);
    const daFala = palavras
      .slice(prov!.dePalavra, prov!.atePalavra + 1)
      .map((p) => p.texto);
    expect(daManchete.length).toBe(daFala.length);
    for (let i = 0; i < daFala.length; i++) {
      expect(baixo(daManchete[i])).toBe(baixo(daFala[i]));
    }
  });

  it('o acento de cor cai na palavra que a proveniencia nomeia', () => {
    if (m!.palavraAcento === undefined) return;
    const palavra = m!.texto.split(/\s+/).filter(Boolean)[m!.palavraAcento];
    expect(palavra, 'palavraAcento aponta para fora da frase').toBeDefined();
    if (prov!.palavraAcentoTexto !== undefined) {
      expect(palavra).toBe(prov!.palavraAcentoTexto);
    }
  });
});

// ---------------------------------------------------------------------------
describe.skipIf(semManchete)('o tempo da manchete esta no relogio da FONTE', () => {
  it('inicioFrame e o inicioMs da palavra citada convertido a fps', () => {
    const ms = palavras[prov!.dePalavra].inicioMs;
    expect(ms).toBe(prov!.inicioMs);
    expect(m!.inicioFrame).toBe(Math.round((ms / 1000) * prov!.fps));
  });

  it('a entrada nao e cortada: a manchete comeca depois do frame 0 da peca', () => {
    // `PecaVideo` faz `inicioFrame - cortarAntesFrames`. Negativo aqui
    // significaria que as primeiras palavras comecam a entrar antes de a peca
    // existir, e a animacao de entrada sai pela metade sem nada reclamar.
    expect(m!.inicioFrame - props.cortarAntesFrames).toBeGreaterThanOrEqual(0);
  });

  it('a manchete fecha antes de a fala acabar', () => {
    // O limite vem do proprio props.json, para nao repetir aqui o
    // `DURACAO_FRAMES` de Raiz.tsx: o ultimo bloco de legenda marca o fim da
    // fala, e a peca vai no minimo ate esse ponto.
    const fimDaFala = Math.max(
      ...props.blocos.map((b: {fimFrame: number}) => b.fimFrame),
    );
    expect(m!.inicioFrame + duracaoDaFrase(m!.texto)).toBeLessThanOrEqual(fimDaFala);
  });
});

// ---------------------------------------------------------------------------
describe.skipIf(semManchete)('a manchete declarada cabe e se le nos dois formatos', () => {
  it('fica dentro da area segura e o bloco cabe na caixa', () => {
    for (const [w, h] of FORMATOS) {
      const rotulo = `${w}x${h}`;
      const z = layout({largura: w, altura: h, razaoFonte: props.razaoFonte});
      const f = formaTextoTela({texto: m!.texto, modo: m!.modo, zonas: z});
      expect(f.corpo, rotulo).toBeGreaterThan(0);
      expect(f.larguraBloco, rotulo).toBeLessThanOrEqual(f.caixa.largura + 1e-6);
      expect(f.alturaBloco, rotulo).toBeLessThanOrEqual(f.caixa.altura + 1e-6);
      expect(f.caixa.x, rotulo).toBeGreaterThanOrEqual(z.seguro.x - 1e-6);
      expect(f.caixa.y, rotulo).toBeGreaterThanOrEqual(z.seguro.y - 1e-6);
      expect(f.caixa.x + f.caixa.largura, rotulo).toBeLessThanOrEqual(
        z.seguro.x + z.seguro.largura + 1e-6,
      );
      expect(f.caixa.y + f.caixa.altura, rotulo).toBeLessThanOrEqual(
        z.seguro.y + z.seguro.altura + 1e-6,
      );
    }
  });

  it('nao sai menor que a legenda: manchete menor que a legenda nao e manchete', () => {
    // Medido em 30/09/2026 com este texto de 5 palavras:
    //   Reel 9:16  sobreImagem 99 px   cartela 152 px   legenda 78 px
    //   Feed 1:1   sobreImagem 54 px   cartela 125 px   legenda 78 px
    // No Feed o modo `sobreImagem` escreve na sobra a direita do video, uma
    // coluna de 274,7 px, e o corpo desaba abaixo da legenda. A asercao e sobre
    // o modo REALMENTE declarado no props.json: gateia a peca que vai ao ar sem
    // legislar sobre o modo que nao foi escolhido.
    for (const [w, h] of FORMATOS) {
      const z = layout({largura: w, altura: h, razaoFonte: props.razaoFonte});
      const f = formaTextoTela({texto: m!.texto, modo: m!.modo, zonas: z});
      expect(f.corpo, `${w}x${h} modo ${m!.modo}`).toBeGreaterThan(
        LEGENDA.corpoEm1080 * (w / 1080),
      );
    }
  });
});
