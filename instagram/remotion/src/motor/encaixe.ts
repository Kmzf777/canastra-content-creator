// A MEDICAO DO TEXTO NA CAIXA DA PISTA, e o veredito de dominancia.
//
// A geometria mora em `motor/pista.ts`; aqui se MEDE. A divisao existe porque medir
// exige `formaTextoTela`, que importa `identidade/glifos` e `identidade/tokens` -- e
// `pista.ts` precisa ficar livre dessa dependencia para `motor/evento.ts` poder
// importar o tipo `Pista` dele sem arrastar tipografia.
//
// O ENCAIXE NAO E ESCOLHIDO AQUI. Ele e derivado de (pista, formato) por `encaixe()`
// de `pista.ts`. Este modulo nao tem plano B, nao tem lista de preferencia e nao
// promove nada a cartela: se o texto nao domina, ele devolve `domina: false` com os
// dois numeros, e quem reprova e o portao de ritmo.
//
// A VERSAO ANTERIOR TINHA PLANO B, E ERA ERRADO. Ela recebia
// `preferencias: ['coluna','faixa','cartela']` e promovia a cartela quando a coluna
// nao alcancava o piso. Duas consequencias: (a) o briefing pedia uma coisa e a peca
// entregava outra, em silencio, que e a licao 3 do CLAUDE.md; (b) com fonte em
// PAISAGEM a promocao disparava em todo evento -- medido, a intersecao da faixa de
// topo do quadro com a imagem letterboxada era 760,00 x 0,00 px -- e a peca de foto
// parada sairia com terra chapado cobrindo as fotos.
//
// O PISO E DE AREA, E E RELATIVO A LEGENDA
//
// `proibicoes.md:19` pede "um elemento dominante por cena", e o que domina um quadro
// e a MANCHA, nao o tamanho da letra. O piso e RELATIVO A LEGENDA de proposito: o
// defeito medido e que o elemento que deveria dominar e MENOR que a legenda, e um
// piso absoluto em % do quadro nao captura isso -- ele passaria numa peca sem legenda
// e reprovaria numa com legenda grande.
//
// O TETO E DE LINHA, E E RELATIVO AO QUADRO. NAO E O PISO AO CONTRARIO.
//
// Medido em 01/10/2026 varrendo os textos reais dos tres briefings nos quatro
// formatos (`out/_escada3.png` e a tabela do laudo), a mancha NAO separa as duas
// populacoes:
//
//   texto                 formato  encaixe  linha %H  mancha %   veredito do olho
//   250 G                 9:16     faixa      20,50     28,02    abuso (tapa o logo)
//   250 G                 16:9     coluna     27,29     13,09    abuso
//   1 · NO PÉ             16:9     faixa      18,93     11,34    abuso
//   SUA PRÓPRIA...CAFÉ    1:1      cartela    15,20     43,10    correto (e cartela)
//
// A maior mancha da varredura inteira, 43,10%, esta numa CARTELA, que e o caso em que
// cobrir e o proposito. E a segunda pior linha de todas, 27,29%, tem mancha de 13,09%
// -- mais baixa que a de seis linhas que ninguem contesta. Um teto de mancha teria que
// passar acima de 43,10% para nao matar a cartela, e ai nao pegaria nenhum dos quatro
// abusos.
//
// O que separa e a ALTURA DE UMA LINHA como fracao da altura do quadro. Ela e o
// tamanho da letra visto do telefone, e e o que o olho le como "isto virou cartaz".
//
// E POR QUE NAO VALE PARA A CARTELA. `formaTextoTela` pinta `fundo: COR.terra` no modo
// cartela: a fonte e SUBSTITUIDA, nao coberta. Nao ha nada embaixo para tapar, e a
// cartela ja tem o respiro proprio dela (`linhasDeFolga = 1`, medido). Aplicar o teto
// ali encolheria o cartao de texto para consertar um defeito que ele nao tem.

import {LEGENDA} from '../identidade/tokens';
import type {Cadencia} from './cadencia';
import {formaTextoTela, type Forma} from './camadas/texto-forma';
import type {PapelEvento} from './evento';
import {MARGEM, type Caixa, type Zonas} from './layout';
import {
  caixaDaPista,
  encaixe as encaixeDaPista,
  modoDoEncaixe,
  type Encaixe,
  type Pista,
} from './pista';

/**
 * Quantas vezes a mancha da legenda o texto tem que ter para "dominar".
 *
 * `[escolhido]`: 1,25 e o menor fator que garante que a diferenca seja visivel em
 * miniatura e nao um empate. Mexer no criterio e mexer AQUI, num lugar so -- nao num
 * `if` por formato.
 */
export const FATOR_DE_DOMINANCIA = 1.25;

/**
 * O TETO: altura maxima de UMA LINHA de texto, em fracao da altura do QUADRO.
 *
 * `[medido]`, por dois caminhos independentes que se cruzam num vao de 3,0 pontos:
 *
 * 1. A ESCADA RENDERIZADA sobre o proprio pacote (`03-prova-cena` cena 3, 9:16, stills
 *    `out/escada-*.png`, montagem em `out/_escada3.png`). Mesmo quadro, so o corpo
 *    muda:
 *
 *      corpo 410 -> linha 20,5%  o `250` cobre o ombro do pacote, o `G` cobre o logo
 *      corpo 340 -> linha 17,0%  o `G` encosta na montanha do logotipo
 *      corpo 310 -> linha 15,5%  o `G` passa a esquerda do pacote; o rotulo fica inteiro
 *      corpo 280 -> linha 14,0%  idem, com folga
 *      corpo 230 -> linha 11,5%  cabe numa linha so
 *
 *    A virada esta entre 17,0% (reprova) e 14,0% (passa).
 *
 * 2. A VARREDURA dos textos reais dos tres briefings nos quatro formatos, encaixes
 *    `faixa` e `coluna`. A populacao que o motor ja produzia sem queixa termina em
 *    13,51% (`250 G` no 1:1, em coluna); os quatro casos de abuso comecam em 18,13%
 *    (`1.235–1.272 M · EXIF` no 16:9). Vao de 4,6 pontos, o maior da tabela.
 *
 * A intersecao dos dois vaos e [14,0% ; 17,0%]. 0,155 e o meio dela, e nao encosta em
 * nenhum lado -- mesma regra de `LIMIAR_DE_COLUNA`.
 *
 * NAO E UM "DIMINUA TUDO". Ele so morde quando a busca pediria mais: na varredura
 * inteira ele altera 4 dos 36 pares (texto, formato) e deixa os outros 32 iguais ao
 * pixel. Mexer no criterio e mexer AQUI.
 */
export const TETO_DE_LINHA = 0.155;

/** A largura e a altura do QUADRO, reconstruidas das zonas. */
function quadro(z: Zonas): {largura: number; altura: number} {
  return {
    largura: z.seguro.largura + 2 * z.seguro.x,
    altura: z.seguro.altura / (1 - MARGEM.topo - MARGEM.base),
  };
}

/**
 * A mancha de referencia: a legenda com DUAS LINHAS CHEIAS naquele quadro.
 *
 * Duas linhas porque e a invariante da caixa de legenda. Nenhum numero novo entra: a
 * largura vem da caixa que `layout()` devolve, o corpo e `LEGENDA.corpoEm1080`
 * escalado pela largura do quadro, a entrelinha e `LEGENDA.entrelinha`.
 */
export function dominanciaDaLegenda(z: Zonas): number {
  const q = quadro(z);
  const corpo = LEGENDA.corpoEm1080 * (q.largura / 1080);
  return (z.legenda.largura * corpo * LEGENDA.entrelinha * 2) / (q.largura * q.altura);
}

/** O piso: `FATOR_DE_DOMINANCIA` vezes a mancha da legenda no mesmo quadro. */
export function pisoDeDominancia(z: Zonas): number {
  return FATOR_DE_DOMINANCIA * dominanciaDaLegenda(z);
}

/**
 * O teto, em PIXEIS de altura de linha naquele quadro.
 *
 * `null` no modo cartela: ela pinta o proprio fundo, nao ha o que tapar. Devolver
 * `null` em vez de `Infinity` obriga quem chama a decidir -- `Infinity` passaria por
 * uma multiplicacao sem ninguem notar.
 */
export function linhaMaximaDoQuadro(
  z: Zonas,
  modo: 'sobreImagem' | 'cartela',
): number | null {
  return modo === 'cartela' ? null : TETO_DE_LINHA * quadro(z).altura;
}

/** Papeis de que se EXIGE dominancia. `etiqueta` nao esta aqui: carimbo nao domina. */
export const PAPEIS_QUE_DOMINAM: readonly PapelEvento[] = ['manchete', 'dado'];

export type EncaixeResolvido = {
  /** derivado de (pista, formato) por `pista.ts`, nunca escolhido aqui */
  encaixe: Encaixe;
  /** o modo que `formaTextoTela` entende: cartela cobre a imagem, sobreImagem nao */
  modo: 'sobreImagem' | 'cartela';
  /** a caixa ja recortada contra a area segura do quadro */
  caixa: Caixa;
  corpo: number;
  /** altura de UMA linha ÷ altura do quadro. E a grandeza do teto. */
  linha: number;
  /** `TETO_DE_LINHA`, ou `null` na cartela, que nao tem teto */
  tetoDeLinha: number | null;
  /** `true` quando foi o teto do quadro, e nao a caixa da pista, que parou a busca */
  noTeto: boolean;
  /** area do bloco de texto ÷ area do quadro */
  dominancia: number;
  piso: number;
  /** `dominancia >= piso` */
  domina: boolean;
  /**
   * Teto e piso nao se encontram: NENHUM corpo serve.
   *
   * So pode ser `true` com `candidataADominar && noTeto && !domina`. E o unico estado
   * que o briefing tem de consertar -- `refinar()` o transforma na recusa
   * `sem-corpo-valido`.
   */
  semCorpoValido: boolean;
  /** `false` para `etiqueta`: de um carimbo nao se exige dominancia */
  candidataADominar: boolean;
  /** a frase com os DOIS numeros, para o diagnostico e para o portao */
  porque: string;
  forma: Forma;
};

export function resolverEncaixe({
  texto,
  papel,
  pista,
  zonas,
  cadencia,
  palavraAcento,
}: {
  texto: string;
  papel: PapelEvento;
  /** DECLARADA no briefing. O encaixe sai dela mais o formato. */
  pista: Pista;
  zonas: Zonas;
  cadencia: Cadencia;
  palavraAcento?: number;
}): EncaixeResolvido {
  const enc = encaixeDaPista(pista, zonas);
  const modo = modoDoEncaixe(enc);
  const caixa = caixaDaPista(pista, zonas);

  // A REDE. Caixa degenerada faria `formaTextoTela` devolver corpo 1 e o texto sairia
  // ilegivel com exit 0 -- a licao 3 do CLAUDE.md. Com a geometria de pista sobre a
  // coluna de texto isso nao acontece nas 8 combinacoes medidas (a menor altura de
  // pista e 153,58 px), e a rede fica para o caso que ninguem previu.
  if (caixa.largura <= 1 || caixa.altura <= 1) {
    throw new Error(
      `resolverEncaixe: a caixa da pista '${pista}' e degenerada: ` +
        `${caixa.largura.toFixed(2)} x ${caixa.altura.toFixed(2)} px. Isso e erro de ` +
        'geometria, nao de briefing: uma pista sem area nao pode receber texto, e ' +
        'desenhar corpo 1 sairia ilegivel com exit 0.',
    );
  }

  // `formaTextoTela` escolhe o corpo por busca binaria contra a caixa que as ZONAS
  // dizem. Para medir a caixa de uma pista, montamos zonas com a caixa da pista no
  // lugar de `manchete` -- e o `seguro` continua o do quadro, para o recorte final
  // permanecer o do Instagram. Na cartela as zonas vao inteiras: o modo `cartela` de
  // `formaTextoTela` usa `zonas.seguro` por conta propria.
  const zonasDoEncaixe: Zonas = modo === 'cartela' ? zonas : {...zonas, manchete: caixa};

  const linhaMaxima = linhaMaximaDoQuadro(zonas, modo);

  const forma = formaTextoTela({
    texto,
    modo,
    zonas: zonasDoEncaixe,
    papel,
    palavraAcento,
    cadencia,
    ...(linhaMaxima === null ? {} : {linhaMaxima}),
  });

  const q = quadro(zonas);
  const dominancia = (forma.larguraBloco * forma.alturaBloco) / (q.largura * q.altura);
  const piso = pisoDeDominancia(zonas);
  const candidataADominar = PAPEIS_QUE_DOMINAM.includes(papel);
  const domina = dominancia >= piso;
  const linha = (forma.corpo * forma.entrelinha) / q.altura;
  const noTeto = forma.noTetoDoQuadro;

  const pct = (x: number) => `${(100 * x).toFixed(3).replace('.', ',')}%`;

  // TETO E PISO NAO SE ENCONTRAM: NAO HA CORPO VALIDO.
  //
  // A mancha cresce com o corpo, e o corpo ja esta no maior valor que o teto permite.
  // Logo nenhum corpo menor domina tambem -- o intervalo [piso, teto] e VAZIO para
  // este (texto, papel, pista, formato). Nao e o teto brigando com o piso: e o
  // briefing pedindo que cinco caracteres dominem um quadro que nao os deixa crescer.
  //
  // POR QUE ESTE MODULO NAO LANCA. Ele mede; quem recusa e o REFINADOR, que junta
  // todas as queixas de um briefing num lote (`Recusa[]`) em vez de parar na primeira.
  // Uma primeira versao lancava daqui, e o lanco subia por `duracaoDoEventoFrames`,
  // passando POR DENTRO de `refinar()` -- o portao que existe para listar problemas
  // morria no meio da lista. O codigo da recusa e `sem-corpo-valido`.
  //
  // `domina: false` sozinho NAO carregaria o caso: ele tambem significa "a caixa e
  // apertada", que se conserta com outra pista. Aqui nenhuma escolha deste modulo
  // resolve, e e isso que `semCorpoValido` diz.
  const semCorpoValido = candidataADominar && noTeto && !domina;

  const porque = candidataADominar
    ? `${enc} em '${pista}': corpo ${forma.corpo} px, ${forma.linhas.length} linha(s), ` +
      `mancha ${pct(dominancia)} do quadro contra o piso ${pct(piso)} ` +
      `(1,25x a legenda de duas linhas). ${domina ? 'DOMINA' : 'NAO DOMINA'}` +
      (noTeto
        ? `. Corpo SEGURADO PELO TETO de ${pct(TETO_DE_LINHA)} da altura do quadro ` +
          `(linha ${pct(linha)}): a caixa de '${pista}' aceitaria mais, e mais taparia ` +
          'a imagem.'
        : '') +
      (semCorpoValido
        ? ' NAO HA CORPO VALIDO: corpo maior tapa a imagem, corpo menor domina menos ' +
          'ainda. O intervalo [piso, teto] e vazio para este texto neste formato.'
        : '')
    : `${enc} em '${pista}': corpo ${forma.corpo} px, mancha ${pct(dominancia)}. ` +
      `Papel '${papel}' nao e candidato a dominar -- carimbo nao e o elemento ` +
      'dominante da cena.' +
      (noTeto
        ? ` Corpo SEGURADO PELO TETO de ${pct(TETO_DE_LINHA)} da altura do quadro ` +
          `(linha ${pct(linha)}).`
        : '');

  return {
    encaixe: enc,
    modo,
    caixa: forma.caixa,
    corpo: forma.corpo,
    linha,
    tetoDeLinha: linhaMaxima === null ? null : TETO_DE_LINHA,
    noTeto,
    dominancia,
    piso,
    domina,
    semCorpoValido,
    candidataADominar,
    porque,
    forma,
  };
}
