// Reel 10 — "chafé: dois erros". O Rafael sentado na torrefação, gravado de uma vez
// (IMG_1128, 27/10/2026), cortado no corte seco v2 (57,7 s) e editado por cima.
//
// Contrato A/B (regra do cliente: quando não há texto na tela, a fala tem legenda):
//   b(...)    → vira texto na tela (palavra-chave) e sai da legenda
//   mudo(...) → nem legenda nem texto (a imagem já diz)
//   t(...)    → só marca o tempo; a palavra fica na legenda
//
// Tempos: projetos/10-isso-e-chafe/palavras-v3.json. Nenhum segundo digitado: tudo lê daqui (lição 56).
// v3 (28/10/2026): a v2 e a voz.wav estavam em relógios diferentes da IMAGEM (a voz atrasava até
// 0,47 s e as palavras adiantavam até 0,23 s no fim). Agora a voz (voz-sync.wav) e as palavras são
// recortadas do bruto no mesmo deslocamento da imagem, trecho a trecho (saida/sync-v3.json).

import palavrasJson from '../../../projetos/10-isso-e-chafe/palavras-v3.json';
import {blocosA, Roteiro, type Faixa, type Palavra} from '../../colagem/legenda';

export const PALAVRAS: Palavra[] = palavrasJson as Palavra[];
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

// ---------------------------------------------------------------- 0 · gancho
export const S1 = {se: r.t('Se alguém já chamou o seu café de'), chafe: r.b('chafé,'), essa: r.t('essa pessoa errou'), duas: r.b('duas vezes.')};
export const S1B = {eu: r.t('Eu sou o'), rafael: r.b('Rafael,'), aqui: r.t('aqui do'), canastra: r.b('Café Canastra,'), e: r.t('e essa aqui é nossa'),
  torrefacao: r.b('torrefação.')};
// ---------------------------------------------------------------- 1 · erro 1
export const S2A = {primeiro: r.b('primeiro erro'), achar: r.t('é achar que café'), clarinho: r.b('clarinho'), e: r.t('é café'), fraco: r.b('fraco.')};
export const S2B = {torra: r.t('A torra mexe na'), intensidade: r.b('intensidade'), sim: r.t('sim, mas ninguém precisa'),
  passar: r.t('passar do ponto pra ter um café'), intenso: r.b('intenso.')};
export const S2D = {quer: r.t('Quer mais intensidade? Coloca um pouquinho mais de'), po: r.b('pó.')};
export const S2E = {o: r.t('O café se'), intensifica: r.b('intensifica'), sabor: r.t('e o sabor fica todo lá.')};
// ---------------------------------------------------------------- 2 · erro 2
export const S3A = {e: r.mudo('E agora,'), segundo: r.b('o segundo erro'), quase: r.b('e esse quase ninguém conta.')};
export const S3B = {muito: r.b('Muito extra forte'), passa: r.t('passa do ponto'), proposito: r.b('de propósito.')};
export const S3C = {isso: r.t('Isso porque o grão tem'), defeito: r.b('defeito.'), grao: r.t('Grão'), preto: r.b('preto,'), ardido: r.b('ardido,'),
  broca: r.b('furado de broca.')};
export const S3D = {passando: r.t('Passando do ponto, tudo vira o mesmo'), amargo: r.b('amargo'), defeito: r.t('e o defeito'), some: r.b('some.')};
export const S3E = {dai: r.t('Daí a pessoa coloca'), acucar: r.b('açúcar'), aguentar: r.t('pra aguentar tomar.')};
// ---------------------------------------------------------------- 3 · o nosso
export const S4A = {cafe: r.t('café que não tem'), nada: r.b('nada pra esconder'), pode: r.t('pode parar no'), marrom: r.b('marrom.')};
export const S4B = {essa: r.t('essa é a'), media: r.b('torra média,'), luz: r.t('a luz atravessa a xícara, o gosto puxa um pouquinho pro'),
  chocolate: r.b('chocolate'), ainda: r.t('e ainda tem um'), azedinho: r.b('azedinho de fruta'), fim: r.t('no fim.')};
// ---------------------------------------------------------------- 4 · a receita
export const S5A = {aqui: r.t('Aqui no Café Canastra a nossa conta é'), cinquenta: r.b('50 gramas'), de: r.t('de pó para'), meio: r.b("meio litro d 'água.")};
export const S5B = {gosta: r.t('Gosta de mais intenso? Lembra do'), primeiro: r.b('primeiro erro?'), coloca: r.t('Coloca um pouquinho mais de'), po: r.b('pó.')};
// ---------------------------------------------------------------- 5 · fecho
// "MANDA PRO AMIGO" vai para a tela no "manda": a pílula não repete o que o texto já diz (v2).
export const S5C = {agora: r.t('agora, não perde tempo,'), manda: r.b('manda isso aí pra aquele amigo'), que: r.t('que ainda chama isso aqui de'),
  chafe: r.b('chafé.')};

export const BLOCOS_A = blocosA(PALAVRAS, r.emB, r.mudas, {maxChars: 16, maxPalavras: 2, pausa: 0.3, minimo: 0.3, cauda: 0.18});

/** Até quando uma palavra-chave fica: 0,9 s depois de dita (lição 72). */
export const ate = (f: Faixa, folga = 0.9) => f.fim + folga;

/** Fim da peça: o corte v2 tem 57,9 s; +0,85 s do bruto para o último "chafé" terminar com respiro. */
export const FIM = 58.75;
