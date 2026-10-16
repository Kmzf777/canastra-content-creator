// Peça 08b — "Onze provas" (refação do Reel 08 com a estratégia de estrategia.md):
// educativa, Kishōtenketsu, vídeo real + colagem + boneco de palito; nada gerado por IA
// em vídeo. Mesmo contrato da peça 07:
//
//   b(...)    → vira colagem (sistema B) e sai da pílula
//   mudo(...) → a colagem já diz isso por outro nome
//   t(...)    → só marca tempo; a palavra continua na pílula
//
// Tempos: projetos/08b-onze-etapas/palavras.json (whisper + CTC, conferido no envelope).

import palavrasJson from '../../../projetos/08b-onze-etapas/palavras.json';
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

// ---------------------------------------------------------------- KI · o gancho
export const S0 = {esse: r.t('Esse punhado aqui é café'), reprovado: r.b('e ele foi reprovado.')};
export const S1 = {chegar: r.t('Pra chegar no pacote,'), passa: r.t('um grão passa por'), onze: r.b('onze provas.'),
  muito: r.t('Muito grão'), caminho: r.b('fica pelo caminho.')};
export const S2 = {fim: r.t('E até o fim desse vídeo você vai saber por que o café que você toma às vezes'), amarga: r.b('amarga.')};
// ---------------------------------------------------------------- SHŌ · as provas
export const S3 = {primeira: r.t('A primeira prova acontece antes da colheita,'), serra: r.b('aqui na Serra da Canastra,'),
  m1250: r.b('a mil duzentos e cinquenta metros.')};
export const S4 = {mede: r.t('A gente mede o'), acucar: r.b('açúcar'), fruto: r.t('do fruto com um'), refrat: r.b('refratômetro'),
  mesmo: r.t('o mesmo aparelho que se usa pra'), vinho: r.b('uva de vinho.')};
export const S5 = {maduro: r.b('Só vem o fruto maduro.'), verde: r.t('Fruto verde, na xícara, vira'), amargor: r.b('amargor.')};
export const S6 = {sol: r.b('Depois, o sol.'), terreiro: r.t('No terreiro, o café é revirado o dia inteiro.'),
  desigual: r.t('Se secar desigual,'), fermenta: r.b('fermenta.'), fermentado: r.t('E fermentado vira um defeito com nome:'),
  ardido: r.b('ardido.')};
export const S7 = {casca: r.t('Aí sai a casca'), peneira: r.b('e começa a peneira fina.')};
export const S8 = {pedra: r.b('Pedra.'), graveto: r.b('Graveto.'), leve: r.b('Grão leve,'), oco: r.b('que é oco por dentro.'),
  maquina: r.t('E uma máquina que olha grão por grão e tira o'), defeitos: r.b('preto, o verde e o ardido'),
  sopro: r.b('com um sopro de ar.')};
export const S9 = {ultimo: r.t('Por último, separa por'), tamanho: r.b('tamanho,'),
  porque: r.t('porque grão grande e pequeno juntos não torram igual.')};
// ---------------------------------------------------------------- TEN · a virada
export const S10 = {aqui: r.t('E aqui vem o que quase ninguém sabe:'), nenhuma: r.b('nenhuma dessas provas acontece na torra.')};
export const S11 = {quando: r.t('Quando um café amarga demais,'), pulada: r.t('quase sempre alguma prova foi pulada,'),
  disfarcar: r.t('e a torra passou da conta pra disfarçar.')};
export const S12 = {bom: r.t('Café bom não se faz na torra.'), antes: r.t('Se faz em tudo que vem antes dela.')};
// ---------------------------------------------------------------- KETSU · a xícara e o laço
export const S13 = {porIsso: r.t('Por isso, aqui, a última prova é na'), xicara: r.b('xícara.'), arthur: r.t('O Arthur prova e dá nota:'),
  aroma: r.b('aroma,'), corpo: r.b('corpo,'), docura: r.b('doçura'), e: r.mudo('e'), citric: r.b('citricidade.'),
  classico: r.t('O Clássico e o Suave passam de'), oitenta: r.b('oitenta pontos.')};
export const S14 = {punhado: r.t('E aquele punhado do começo?'), ficou: r.t('Ficou lá na fazenda.')};
export const S15 = {manda: r.t('Manda esse vídeo pra quem acha que café é tudo igual.')};

export const EM_B = r.emB;
export const MUDAS = r.mudas;
export const BLOCOS_A = blocosA(PALAVRAS, EM_B, MUDAS);
export const FIM = Math.ceil((PALAVRAS[PALAVRAS.length - 1].fim + 0.6) * 10) / 10;

/** Início de cada cena (s), na ordem de CENAS em cenas.tsx. */
export const CENA_INICIO = [
  0, //                         0 o punhado reprovado (vídeo)
  S1.chegar.inicio, //          1 o caminho das provas (colagem: grãos em fila, alguns caem)
  S2.fim.inicio, //             2 a promessa: boneco toma café e faz careta
  S3.primeira.inicio, //        3 a lavoura a 1.250 m (foto real)
  S4.mede.inicio, //            4 o refratômetro (boneco + recorte)
  S5.maduro.inicio, //          5 só o maduro (vídeo: a mão)
  S5.verde.inicio, //           6 fruto verde vira amargor (colagem)
  S6.sol.inicio, //             7 terreiro (vídeo)
  S6.fermentado.inicio, //      8 ardido (colagem)
  S7.casca.inicio, //           9 sai a casca (colagem)
  S8.pedra.inicio, //          10 pedra
  S8.graveto.inicio, //        11 graveto
  S8.leve.inicio, //           12 grão leve (vídeo: mesa densimétrica)
  S8.maquina.inicio, //        13 a máquina que sopra (boneco)
  S9.ultimo.inicio, //         14 peneiras por tamanho (boneco + peneira)
  S10.aqui.inicio, //          15 a virada: o tambor (vídeo, escurecido)
  S11.quando.inicio, //        16 prova pulada + disfarce (boneco)
  S12.bom.inicio, //           17 a frase, no escuro (vídeo: grão bom)
  S13.porIsso.inicio, //       18 o Arthur prova (vídeo)
  S13.aroma.inicio, //         19 a ficha de notas (colagem)
  S13.classico.inicio, //      20 os pacotes reais, 80+
  S14.punhado.inicio, //       21 o punhado do começo (vídeo, laço)
  S15.manda.inicio, //         22 CTA
];
