// Peça 07 — o roteiro falado, palavra a palavra, com o DESTINO de cada trecho.
//
//   b(...)    → vira colagem (sistema B) e sai da pílula
//   mudo(...) → a colagem já diz isso por outro nome; não aparece em lugar nenhum
//   t(...)    → só marca tempo (gesto, som); a palavra continua na pílula
//
// O que não é declarado vai para a pílula (sistema A). Os trechos são procurados EM
// ORDEM — palavra repete ("especial" 8 vezes) — então esta lista segue a narração.
// Tempos medidos: `projetos/07-cafe-especial-colagem/palavras.json`
// (scripts/alinhar_narracao.py: whisper + silêncios, texto do roteiro).

import palavrasJson from '../../../projetos/07-cafe-especial-colagem/palavras.json';
import {blocosA, Roteiro, type Faixa, type Palavra} from '../../colagem/legenda';

export const PALAVRAS = palavrasJson as Palavra[];
const r = new Roteiro(PALAVRAS);

const chave = (s: string) => s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');

/**
 * Início (s) da `n`-ésima `palavra` dentro de uma faixa — para gesto, câmera ou som que
 * bate numa palavra do MEIO de um trecho. Nenhum tempo das cenas é escrito à mão: em
 * 07/10/2026 o realinhamento forçado moveu inícios de frase em até 0,4 s, e cada segundo
 * digitado nas cenas teria ficado para trás. Lança se não achar.
 */
export function em(f: Faixa, palavra: string, n = 1): number {
  let k = 0;
  for (let i = f.de; i <= f.ate; i++) {
    if (chave(PALAVRAS[i].texto) === chave(palavra) && ++k === n) return PALAVRAS[i].inicio;
  }
  throw new Error(`em(): "${palavra}" (${n}ª) não está em "${f.texto}"`);
}

/** Início da palavra seguinte à faixa: até onde a fala do trecho ocupa o tempo. */
export const depois = (f: Faixa): number => PALAVRAS[f.ate + 1]?.inicio ?? f.fim + 0.4;

// ---------------------------------------------------------------- 1 tensão
export const S1 = {
  ate1: r.b('Até um por cento'),
  doCafe: r.t('do café que você compra'),
  podeSer: r.t('pode ser'),
  casca: r.b('casca'),
  e: r.mudo('e'),
  pau: r.b('pau.'),
  etaTudo: r.t('E tá tudo'),
  lei: r.b('dentro da lei.'),
};
// ---------------------------------------------------------------- 2 calma
export const S2 = {
  calma: r.b('Calma!'),
  largar: r.t('Não precisa largar o café.'),
  fim: r.t('Mas até o fim desse vídeo'),
  saber: r.t('você vai saber'),
  seuEspecial: r.b('se o seu é especial.'),
};
// ---------------------------------------------------------------- 3 o mito
export const S3 = {
  especial: r.b('Especial'),
  naoE: r.t('não é'),
  nomeBonito: r.b('nome bonito'),
  noPacote: r.t('no pacote.'),
  prova: r.b('É prova.'),
  duas: r.b('Duas.'),
};
// ---------------------------------------------------------------- 4 prova 1
export const S4 = {
  primeira: r.mudo('A primeira é no'),
  graoCru: r.b('grão cru.'),
  classificador: r.t('O classificador pega'),
  g350: r.b('trezentos e cinquenta gramas'),
  olha: r.t('e olha grão por grão.'),
  preto: r.b('Grão preto.'),
  ardido: r.b('Ardido.'),
  cereja: r.b('Cereja seca.'),
  fungo: r.b('Fungo.'),
  pedra: r.b('Pedra.'),
  pau: r.b('Pau.'),
  achou: r.t('Achou um só?'),
  acabou: r.b('Acabou.'),
  naoEspecial: r.b('Não é especial.'),
};
// ---------------------------------------------------------------- 5 o contraste
export const S5 = {
  comparar: r.t('Pra comparar:'),
  classificacao: r.b('a classificação oficial brasileira'),
  tipo: r.t('tem um tipo de café com até'),
  d360: r.b('trezentos e sessenta defeitos'),
  amostra: r.t('numa amostra.'),
  noEspecial: r.t('No especial?'),
  zero: r.b('Zero defeito grave.'),
};
// ---------------------------------------------------------------- 6 prova 2
export const S6 = {
  passou: r.b('Passou?'),
  xicara: r.b('Agora vem a xícara.'),
  provadores: r.t('Provadores certificados provam'),
  cinco: r.b('cinco xícaras'),
  lote: r.t('do mesmo lote e dão nota pra'),
  aroma: r.b('aroma,'),
  docura: r.b('doçura,'),
  acidez: r.b('acidez,'),
  corpo: r.b('corpo,'),
  equilibrio: r.b('equilíbrio'),
  seUma: r.t('e se uma xícara sair diferente das outras,'),
  perde: r.b('perde ponto.'),
  abaixo: r.t('Abaixo de'),
  oitenta: r.b('oitenta,'),
  naoEsp: r.t('não é especial.'),
  acima: r.t('Acima de'),
  oitentaECinco: r.b('oitenta e cinco,'),
  excelente: r.b('excelente.'),
  noventa: r.b('Noventa'),
  rarissimo: r.b('raríssimo.'),
};
// ---------------------------------------------------------------- 7 a virada
export const S7 = {
  aqui: r.t('E aqui vem o que'),
  ninguem: r.b('quase ninguém conta:'),
  nenhum: r.b('nenhum desses defeitos nasce na torra.'),
  pretoArdido: r.t('Preto e ardido são fruto que'),
  fermentou: r.b('fermentou demais.'),
  verde: r.t('Verde é'),
  colheita: r.b('colheita antes da hora.'),
  estragar: r.b('A torra pode estragar um café bom'),
  naoSalva: r.b('mas não salva um café ruim.'),
  decide: r.b('Especial se decide no pé.'),
};
// ---------------------------------------------------------------- 8 a fazenda
export const S8 = {
  porIsso: r.t('Por isso a gente só torra o que a gente mesmo'),
  planta: r.b('planta,'),
  colhe: r.b('colhe'),
  e: r.mudo('e'),
  seleciona: r.b('seleciona.'),
  a: r.mudo('A'),
  m1250: r.b('mil duzentos e cinquenta metros,'),
  serra: r.b('na Serra da Canastra,'),
  fruto: r.t('o fruto'),
  devagar: r.b('amadurece devagar'),
  ficaMais: r.t('e fica mais'),
  doce: r.b('doce.'),
};
// ---------------------------------------------------------------- 9 o fecho
export const S9 = {
  olha: r.t('Agora olha o seu pacote'),
  procura: r.b('e procura a nota.'),
  seNao: r.b('Se não tem nota'),
  ninguem: r.b('ninguém provou por você.'),
  nosso: r.b('O nosso tá aqui.'),
  salva: r.b('Salva esse vídeo'),
  compra: r.t('pra próxima compra.'),
};

export const EM_B = r.emB;
export const MUDAS = r.mudas;
export const BLOCOS_A = blocosA(PALAVRAS, EM_B, MUDAS);

/** Início de cada cena (s): a fala que abre a cena. */
export const CENA_INICIO = [0, S2.calma.inicio, S3.especial.inicio, S4.primeira.inicio, S5.comparar.inicio,
  // a cena 8 entra 0,3 s depois do "Por isso" para o "NO PÉ." respirar antes do chicote
  S6.passou.inicio, S7.aqui.inicio, S8.porIsso.inicio + 0.3, S9.olha.inicio];
export const FIM = 79.0;

/**
 * Trocas DENTRO de uma cena (s). A cena muda de fase e a raiz dá o chicote no mesmo
 * instante, então as duas leem daqui — antes eram dois números digitados em dois
 * arquivos, e realinhar a narração separava um do outro.
 */
export const TROCA = {
  /** "…perde ponto." → "Abaixo de oitenta": a régua de 0 a 100 */
  regua: S6.abaixo.inicio - 0.13,
  /** o painel das polaroides entra um respiro antes de "Preto e ardido" */
  painel: S7.pretoArdido.inicio - 0.15,
  /** "…antes da hora." → "A torra pode estragar…" */
  tese: S7.estragar.inicio - 0.13,
  /** "…um café ruim." → "Especial se decide no pé." */
  pe: S7.decide.inicio - 0.06,
  /** o selo → "Salva esse vídeo" */
  fecho: S9.salva.inicio,
};
