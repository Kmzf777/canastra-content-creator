// Peça 08 — "Esse café já foi uma fruta". O roteiro falado, palavra a palavra, com o
// DESTINO de cada trecho (mesmo contrato da peça 07):
//
//   b(...)    → vira colagem (sistema B) e sai da pílula
//   mudo(...) → a colagem já diz isso por outro nome
//   t(...)    → só marca tempo; a palavra continua na pílula
//
// Tempos medidos: `projetos/08-cafe-ja-foi-fruta/palavras.json` (whisper + CTC,
// scripts/alinhar_forcado.py, conferido com conferir_alinhamento.py pausas).
// Nenhum segundo é digitado nas cenas nem no som: tudo lê daqui.

import palavrasJson from '../../../projetos/08-cafe-ja-foi-fruta/palavras.json';
import {blocosA, Roteiro, type Faixa, type Palavra} from '../../colagem/legenda';

export const PALAVRAS = palavrasJson as Palavra[];
const r = new Roteiro(PALAVRAS);

const chave = (s: string) => s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');

/** Início (s) da `n`-ésima `palavra` dentro de uma faixa. Lança se não achar. */
export function em(f: Faixa, palavra: string, n = 1): number {
  let k = 0;
  for (let i = f.de; i <= f.ate; i++) {
    if (chave(PALAVRAS[i].texto) === chave(palavra) && ++k === n) return PALAVRAS[i].inicio;
  }
  throw new Error(`em(): "${palavra}" (${n}ª) não está em "${f.texto}"`);
}

/** Início da palavra seguinte à faixa. */
export const depois = (f: Faixa): number => PALAVRAS[f.ate + 1]?.inicio ?? f.fim + 0.4;

// ---------------------------------------------------------------- Ki · o gancho
export const S1 = {
  esse: r.t('Esse café aqui'),
  jaFoi: r.t('já foi'),
  fruta: r.b('uma fruta.'),
};
export const S2 = {
  vermelha: r.b('Vermelha,'),
  doce: r.b('doce'),
  nunca: r.t('e você nunca viu ela no'),
  super: r.b('supermercado.'),
};
// ---------------------------------------------------------------- Shō · a vida dela
export const S3 = {
  antes: r.t('Antes de colher,'),
  mede: r.t('a gente mede o'),
  acucar: r.b('açúcar'),
  dela: r.t('dela.'),
  e: r.t('É,'),
  tambem: r.t('café também faz'),
  exame: r.b('exame.'),
};
export const S4 = {
  maduras: r.b('Só as maduras'),
  vem: r.t('vêm.'),
  outras: r.t('As outras'),
  esperam: r.b('esperam a vez.'),
};
export const S5 = {
  depois: r.t('Depois foi tomar'),
  sol: r.b('sol'),
  terreiro: r.t('no terreiro,'),
  sendo: r.t('sendo'),
  revirada: r.b('revirada e revirada'),
  tipo: r.t('tipo'),
  frango: r.b('frango de padaria.'),
};
export const S6 = {
  ai: r.t('Aí perdeu a'),
  casca: r.b('casca.'),
};
export const S7 = {
  comecou: r.t('E começou a parte'),
  dificil: r.b('mais difícil'),
  vida: r.t('da vida dela:'),
  cinco: r.b('cinco máquinas'),
  existem: r.t('que existem pra dizer'),
  nao: r.b('não.'),
};
// a rajada: cada "Não" é um carimbo, cada alvo é um objeto
export const S8 = {
  n1: r.b('Não'),
  pedra: r.b('pra pedra.'),
  n2: r.b('Não'),
  graveto: r.b('pro graveto.'),
  n3: r.b('Não'),
  leve: r.b('pro grão leve.'),
  n4: r.b('Não'),
  preto: r.b('pro preto,'),
  verde: r.b('pro verde,'),
  ardido: r.b('pro ardido.'),
};
export const S9 = {
  quem: r.t('E quem sobrou ainda foi'),
  separado: r.t('separado por'),
  tamanho: r.b('tamanho.'),
  pra: r.t('Pra ninguém'),
  torrar: r.b('torrar antes da hora.'),
};
export const S10 = {
  depoisTudo: r.t('Depois de tudo isso'),
  fogo: r.b('foi pro fogo.'),
  sim: r.b('Sim.'),
  depois2: r.t('Depois de tudo isso.'),
};
export const S11 = {
  alguem: r.t('E aí alguém'),
  provou: r.b('provou.'),
  barulho: r.b('Fez barulho.'),
  cheirou: r.b('Cheirou.'),
  deNovo: r.t('Provou de novo.'),
  tecnica: r.b('É técnica, juro.'),
};
// ---------------------------------------------------------------- Ten · a virada
export const S12 = {
  fruta: r.b('Fruta,'),
  semente: r.b('semente,'),
  grao: r.b('grão'),
  mas: r.t('Mas o que fez esse café ser bom'),
  nada: r.t('não foi nada disso que ele virou.'),
  caminho: r.t('Foi tudo que ficou pelo caminho.'),
};
// ---------------------------------------------------------------- Ketsu · a marca e o laço
export const S13 = {
  nasceu: r.t('Esse aqui nasceu a'),
  m1250: r.b('mil duzentos e cinquenta metros,'),
  serra: r.b('na Serra da Canastra.'),
  jaFoi: r.b('Já foi fruta.'),
  hoje: r.t('Hoje é'),
  canastra: r.b('Café Canastra.'),
};
export const S14 = {
  amanha: r.b('E amanhã?'),
  vai: r.t('Amanhã ele vai ser o seu'),
  cafeManha: r.b('café da manhã.'),
};

export const EM_B = r.emB;
export const MUDAS = r.mudas;
export const BLOCOS_A = blocosA(PALAVRAS, EM_B, MUDAS);

/** Fim da peça (s): a última palavra + 0,6 s, arredondado ao décimo. */
export const FIM = Math.ceil((PALAVRAS[PALAVRAS.length - 1].fim + 0.6) * 10) / 10;

/**
 * Início de cada cena (s), na ordem de `CENAS` em Fruta.tsx. Cada valor é a fala que
 * abre a cena — os cortes da rajada caem exatamente em cada "Não".
 */
export const CENA_INICIO = [
  0, //                                 0 fruta (vídeo: o cacho)
  S2.vermelha.inicio, //                1 vermelha, doce (vídeo)
  S2.nunca.inicio, //                   2 supermercado (colagem)
  S3.antes.inicio, //                   3 o exame (colagem)
  S4.maduras.inicio, //                 4 só as maduras (vídeo: a mão)
  S4.outras.inicio, //                  5 esperam a vez (colagem)
  S5.depois.inicio, //                  6 terreiro (vídeo)
  S6.ai.inicio, //                      7 a casca (colagem)
  S7.comecou.inicio, //                 8 cinco máquinas (vídeo: densimétrica)
  S8.n1.inicio, //                      9 pedra
  S8.n2.inicio, //                     10 graveto
  S8.n3.inicio, //                     11 grão leve (vídeo: o descarte na mão)
  S8.n4.inicio, //                     12 preto, verde, ardido
  S9.quem.inicio, //                   13 quem sobrou (vídeo: o grão bom)
  S9.tamanho.inicio, //                14 tamanho (colagem)
  S10.depoisTudo.inicio, //            15 o fogo (vídeo: torrador)
  S11.alguem.inicio, //                16 provou (vídeo: cupping)
  S11.cheirou.inicio, //               17 cheirou
  S11.deNovo.inicio, //                18 provou de novo
  S11.tecnica.inicio, //               19 é técnica
  S12.fruta.inicio, //                 20 a virada, escuro (colagem)
  S12.caminho.inicio, //               21 pelo caminho (vídeo escuro)
  S13.nasceu.inicio, //                22 a serra (vídeo: terreiro ao pôr do sol)
  S13.jaFoi.inicio, //                 23 hoje é Café Canastra (embalagem)
  S14.amanha.inicio, //                24 café da manhã
  S14.cafeManha.fim + 0.08, //         25 o laço: volta ao cacho do começo
];
