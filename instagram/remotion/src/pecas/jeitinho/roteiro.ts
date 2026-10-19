// Peça 09 — "cada um tem seu jeitinho": três criadores, três jeitos de preparar café.
// Abertura crua de 3 s (vídeo do Rafael, sem voz, estratégia da @rafaelachagas) e depois a
// colagem narrada. A narração (ElevenLabs, 1,15x) entra no corte da abertura.
//
// Contrato A/B da peça 07 (a regra do cliente: quando não há texto na tela, a fala tem
// legenda):
//   b(...)    → vira texto de colagem (palavra-chave na tela) e sai da pílula
//   mudo(...) → nem pílula nem colagem (palavra solta que a colagem já cobre: "O", "E")
//   t(...)    → vai para a pílula
//
// Tempos: projetos/09-jeitinho-cafe/palavras.json (whisper + CTC, conferido no envelope em
// 15/10/2026). Eles estão no relógio da NARRAÇÃO; aqui são deslocados pela abertura uma vez,
// e o resto da peça só lê daqui. Nenhum segundo digitado (lição 56).

import palavrasJson from '../../../projetos/09-jeitinho-cafe/palavras.json';
import {blocosA, Roteiro, type Faixa, type Palavra} from '../../colagem/legenda';

/** Duração da abertura crua (gancho_rafael.mp4, medido: 3,000 s). A voz começa aqui. */
export const ABERTURA = 3.0;

export const PALAVRAS: Palavra[] = (palavrasJson as Palavra[]).map((p) => ({...p, inicio: p.inicio + ABERTURA, fim: p.fim + ABERTURA}));
const r = new Roteiro(PALAVRAS);

const chave = (s: string) => s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');

/** Início (s, relógio da peça) da `n`-ésima `palavra` dentro de uma faixa. Lança se não achar. */
export function em(f: Faixa, palavra: string, n = 1): number {
  let k = 0;
  for (let i = f.de; i <= f.ate; i++) {
    if (chave(PALAVRAS[i].texto) === chave(palavra) && ++k === n) return PALAVRAS[i].inicio;
  }
  throw new Error(`em(): "${palavra}" (${n}ª) não está em "${f.texto}"`);
}

// ---------------------------------------------------------------- gancho
export const S1 = {tem: r.t('Tem gente que rala a'), tangerina: r.b('tangerina'), dentro: r.t('dentro do café, e esse nem é o jeito mais'),
  diferente: r.b('diferente'), achei: r.t('que eu achei!')};
export const S2 = {cada: r.t('É que cada um tem o seu'), jeitinho: r.b('jeitinho'), tomar: r.t('de tomar café.'), separei: r.t('E eu separei'),
  tres: r.b('três'), cara: r.t('que são a cara de quem faz.')};
// ---------------------------------------------------------------- Fábio
export const S3 = {primeiro: r.t('Primeiro,'), o: r.mudo('o'), fabio: r.b('Fábio.'), ele: r.mudo('Ele'), congela: r.b('congela'), aTang: r.t('a tangerina,'),
  rala: r.b('rala'), cima: r.t('por cima do pó e só depois joga a'), agua: r.b('água.'), desce: r.t('O café desce com cheiro de'), fruta: r.b('fruta.'),
  olha: r.t('Olha a'), cor: r.b('cor'), disso: r.t('disso!')};
export const S4 = {ousado: r.b('Achou ousado?'), espera: r.t('Espera o próximo.')};
// ---------------------------------------------------------------- Paulo
export const S5 = {o: r.mudo('O'), paulo: r.b('Paulo'), pega: r.t('pega a'), pacoquita: r.b('paçoquita.'), isso: r.t('Isso,'), pacoquita2: r.b('paçoquita!'),
  mistura: r.t('Mistura com'), leite: r.b('leite em pó'), creme: r.t('e creme de leite até virar uma'), pasta: r.b('pasta'), joga: r.t('e joga o'),
  cafe: r.b('café quente por cima.'), esse: r.t('Esse vídeo passou de'), dez: r.b('dez milhões de visualizações!')};
export const S6 = {eo: r.mudo('E o'), terceiro: r.b('terceiro'), nem: r.t('nem usa'), coador: r.b('coador!')};
// ---------------------------------------------------------------- Giuseppe (v3: substitui o Gabriel, que usava
// prensa, não "fazia na mão" — erro de leitura apontado pelo cliente em 15/10/2026)
export const S7 = {o: r.mudo('O'), giuseppe: r.b('Giuseppe'), e1: r.mudo('é'), italiano: r.b('italiano'), faz: r.t('e faz o'),
  creme: r.b('creme de café de Milão:'), bate: r.b('bate o mel,'), joga: r.t('joga'), cafe: r.b('café solúvel,'),
  um: r.t('um pouquinho de'), agua: r.b('água quente,'), liga: r.t('liga a'), batedeira: r.b('batedeira,'), e: r.mudo('e'),
  vira: r.t('vira um'), cremeFim: r.b('creme'), que: r.t('que dá até pra comer de'), colher: r.b('colher!')};
// ---------------------------------------------------------------- conclusão e pergunta
export const S8 = {tangerina: r.b('Tangerina,'), pacoquita: r.b('paçoquita,'), creme: r.b('creme italiano.'),
  jeitos: r.b('Três jeitos que não têm nada a ver com o outro,'), eos: r.t('e os três estão'), certos: r.b('certos.'),
  porque: r.b('Porque café não tem jeito certo.'), seu: r.b('Tem o seu jeito!')};
export const S9 = {e: r.mudo('E'), voce: r.b('você?'), como: r.t('Como prepara o seu?'), comenta: r.b('Comenta aqui'), embaixo: r.t('embaixo!')};

export const EM_B = r.emB;
export const MUDAS = r.mudas;
export const BLOCOS_A = blocosA(PALAVRAS, EM_B, MUDAS);

/**
 * Até quando uma palavra-chave (B) fica na tela: 0,9 s depois de dita, e nunca depois da
 * entrada do B seguinte. Texto parado enquanto a voz já fala outra coisa lê como
 * dessincronia (reprovado na v1 de 15/10/2026: "TANGERINA" ficava 3 s); depois disso
 * quem fala é a pílula.
 */
export function ate(f: Faixa, folga = 0.9): number {
  const prox = PALAVRAS.find((p) => p.i > f.ate && EM_B.has(p.i));
  return Math.min(f.fim + folga, prox ? prox.inicio : Infinity);
}

/** Fim da peça: última palavra + 0,6 s (o mesmo respiro da 08b). */
export const FIM = Math.ceil((PALAVRAS[PALAVRAS.length - 1].fim + 0.6) * 10) / 10;

/** Início de cada cena (s, relógio da peça), na ordem de CENAS em Jeitinho.tsx. */
export const CENA_INICIO = [
  0, //                    0 abertura crua (vídeo do Rafael) + mergulho na tela
  ABERTURA, //             1 gancho: o Fábio ralando vira colagem; as cabeças chegam no "diferente"
  S2.cada.inicio, //       2 premissa: três cabeças no papel
  S3.primeiro.inicio, //   3 Fábio: cabeça + cartão de vídeo trocando por palavra
  S3.desce.inicio, //      4 a cor do café
  S4.ousado.inicio, //     5 re-gancho: o Paulo espia
  S5.o.inicio, //          6 Paulo: paçoquita
  S5.mistura.inicio, //    7 a pasta e o café por cima
  S5.esse.inicio, //       8 dez milhões
  S6.eo.inicio, //         9 re-gancho: sem coador
  S7.o.inicio, //         10 Giuseppe: o creme de café de Milão, um take por passo
  S7.e.inicio, //         11 vira creme e come de colher
  S8.tangerina.inicio, // 12 conclusão: os três juntos
  S8.porque.inicio, //    13 a frase
  S9.e.inicio, //         14 a pergunta
];
