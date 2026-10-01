// BRIEFING -> PLANO. Puro: sem React, sem remotion, sem I/O.
//
// E aqui, e so aqui, que segundo vira frame. O briefing tem UM relogio (segundos do
// inicio da cena); o plano tem os TRES, e por isso ele e GERADO e carrega o sha256 do
// briefing que o produziu -- um plano editado a mao e detectavel.
//
// A CONTA: `duracaoPecaFrames = Sigma cenas - Sigma transicoes`
//
// Durante a transicao as DUAS cenas sao renderizadas, entao ela nao soma tempo: ela
// GASTA. Com a transicao default sendo `corte` de 0 frames, `Sigma cenas` continua
// sendo a duracao da peca -- e e por isso que os dois desenhos paralelos estavam
// certos ao mesmo tempo.
//
// POR QUE ELE LANCA EM VEZ DE AVISAR
//
// Com `alvoS` divergente, uma peca que sai mais curta que o briefing e exatamente o
// defeito que o pedido nomeia. `console.warn` num pipeline de render e uma linha que
// ninguem le -- e a licao 3 do CLAUDE.md: exit 0 com o resultado errado.

// NAO HA `import {createHash} from 'node:crypto'` AQUI, e isso e o ponto.
//
// Este arquivo e PURO. O hash mora em `briefing/impressao.ts`, que e Node-only, e quem
// sela o plano e quem o escreve. `Raiz.tsx`, `Peca.tsx` e `Cena.tsx` importam este
// arquivo so com `import type`, que o transpilador apaga -- mas a primeira importacao
// de VALOR a partir de um `.tsx` derrubaria o render se `node:crypto` estivesse aqui,
// e ninguem lembraria por que.
import {cadencia} from '../motor/cadencia';
import {agrupar, type Bloco, type Palavra} from '../legenda/agrupar';
import {CADENCIA_DO_PAPEL, FAMILIA_DO_PAPEL, type CadenciaTexto} from '../motor/evento';
import {resolverEncaixe} from '../motor/encaixe';
import {layout} from '../motor/layout';
import type {Encaixe, Pista} from '../motor/pista';
import {duracaoComIrmaos, duracaoDeIrmao} from '../motor/movimento';
import {emFrames, emSegundos} from '../motor/relogio';
import {LEGENDA} from '../identidade/tokens';
import type {Papel} from '../identidade/tipografia';
import {
  DIMENSAO,
  type Asset,
  type Audio,
  type Briefing,
  type Fonte,
  type Formato,
  type Licenca,
} from './esquema';
import {exigirBriefingCoerente, razaoDaPeca} from './refinar';

export type EventoCompilado = {
  papel: 'manchete' | 'dado' | 'etiqueta';
  texto: string;
  familia: Papel;
  cadenciaTexto: CadenciaTexto;
  pista: Pista;
  /**
   * Quantos elementos escalonam, pela cadencia do papel.
   *
   * E o MESMO numero que `formaTextoTela` devolve em `forma.irmaos`, e e ele que
   * dimensiona `duracaoIrmaoFrames` e `duracaoFrames`. Guardado aqui para o portao
   * poder conferir a conta sem remedir a tipografia.
   */
  irmaos: number;
  /** frames, relativo ao inicio DA CENA */
  inicioFrames: number;
  /** frames que CADA irmao fica presente */
  duracaoIrmaoFrames: number;
  /** frames que o evento inteiro ocupa, stagger incluido */
  duracaoFrames: number;
  palavraAcento?: number;
};

export type CenaCompilada = {
  duracaoFrames: number;
  /** frame da PECA em que esta cena comeca, com as transicoes ja descontadas */
  inicioNaPecaFrames: number;
  fonte: Fonte;
  /** frames de apara, ja convertidos (so video tem) */
  aparaAntesFrames: number;
  eventos: EventoCompilado[];
};

export type TransicaoCompilada =
  | {tipo: 'corte'; duracaoFrames: 0}
  | {tipo: 'fade'; duracaoFrames: number}
  | {tipo: 'wipe'; duracaoFrames: number; direcao: string};

export type DiagnosticoEvento = {
  cena: number;
  indice: number;
  texto: string;
  porFormato: Record<
    string,
    {
      /** DERIVADO de (pista, formato). Nao ha escolha para relatar. */
      encaixe: Encaixe;
      corpo: number;
      /** altura de uma linha ÷ altura do quadro. A grandeza do TETO. */
      linha: number;
      /** `TETO_DE_LINHA`, ou `null` na cartela, que nao tem teto */
      tetoDeLinha: number | null;
      /** `true` quando o teto do quadro, e nao a caixa da pista, parou a busca */
      noTeto: boolean;
      /** area do bloco ÷ area do quadro */
      dominancia: number;
      piso: number;
      domina: boolean;
      /** `false` para `etiqueta` */
      candidataADominar: boolean;
      /** a frase com os dois numeros, pronta para o portao e para o CLI */
      porque: string;
    }
  >;
};

/** Os contadores do rebase da legenda. Nenhum bloco desaparece sem numero. */
export type DiagnosticoLegenda = {
  deslocamentoFrames: number;
  /** blocos que atravessavam o frame 0 e foram grudados nele */
  grudadosEmZero: number;
  /** o maior recuo, em frames. Acima do piso de leitura o portao reprova */
  maiorRecuoFrames: number;
  /** blocos inteiramente antes do frame 0: sem frame visivel */
  descartadosAntesDoInicio: number;
  /** blocos que comecavam depois do fim da peca */
  descartadosDepoisDoFim: number;
};

export type Plano = {
  _gerado_por: string;
  _sha256Briefing: string;
  /** o hash do proprio conteudo deste plano, com este campo removido */
  _sha256Plano: string;
  serie: string;
  fps: number;
  formatos: Formato[];
  duracaoFrames: number;
  /** a menor razao de exibicao entre as cenas em CONTAIN, ou null */
  razaoDaPeca: number | null;
  cenas: CenaCompilada[];
  transicoes: TransicaoCompilada[];
  legenda: ({blocos: Bloco[]} & DiagnosticoLegenda) | null;
  /** as duas faixas, no relogio da PECA. `audio` e obrigatorio no briefing. */
  audio: Audio;
  assets: Asset[];
  licencas: Record<Licenca, boolean> & {justificativa: string};
  /** DERIVADO: `assets.length > 0`. Nao e campo de briefing. */
  exigePreservacao: boolean;
  gancho: string;
  cta: string;
  diagnostico: {eventos: DiagnosticoEvento[]; licencasLigadas: Licenca[]};
};

export function compilar(b: Briefing, fontes: {palavras?: Palavra[]} = {}): Plano {
  // O refinador roda PRIMEIRO. Compilar um briefing incoerente produz um plano
  // coerente com um briefing errado, que e a pior das saidas: parece pronto.
  exigirBriefingCoerente(b);

  const fps = b.fps;
  const c = cadencia(fps);
  const razao = razaoDaPeca(b);

  const transicoes: TransicaoCompilada[] = b.transicoes.map((t) =>
    t.tipo === 'corte'
      ? {tipo: 'corte', duracaoFrames: 0}
      : t.tipo === 'fade'
        ? {tipo: 'fade', duracaoFrames: emFrames(t.duracaoS, fps)}
        : {tipo: 'wipe', duracaoFrames: emFrames(t.duracaoS, fps), direcao: t.direcao},
  );
  const gastoDeTransicao = transicoes.reduce((s, t) => s + t.duracaoFrames, 0);

  let cenasFrames = b.cenas.map((cena) => emFrames(cena.duracaoS, fps));
  let duracaoFrames = cenasFrames.reduce((s, x) => s + x, 0) - gastoDeTransicao;

  if (b.duracao.modo === 'totalFixo') {
    const alvo = emFrames(b.duracao.alvoS as number, fps);
    cenasFrames = devolverFramesAsCenas(cenasFrames, alvo - duracaoFrames);
    duracaoFrames = cenasFrames.reduce((s, x) => s + x, 0) - gastoDeTransicao;
  } else if (b.duracao.alvoS !== undefined) {
    const alvo = emFrames(b.duracao.alvoS, fps);
    if (duracaoFrames !== alvo) {
      const diff = alvo - duracaoFrames;
      throw new Error(
        'duracao.modo e "somaCenas" e o alvo nao bate: as cenas somam ' +
          `${cenasFrames.reduce((s, x) => s + x, 0)} frames, as transicoes gastam ` +
          `${gastoDeTransicao}, logo a peca tem ${duracaoFrames} frames ` +
          `(${emSegundos(duracaoFrames, fps).toFixed(3)} s), e alvoS pede ${alvo} ` +
          `frames (${b.duracao.alvoS} s). Diferenca de ${Math.abs(diff)} frames, ` +
          `${Math.abs(emSegundos(diff, fps)).toFixed(3)} s. Ajuste as cenas, ou use ` +
          'duracao.modo "totalFixo" para o alvo mandar.',
      );
    }
  }

  const diagnosticoEventos: DiagnosticoEvento[] = [];
  let acumulado = 0;
  const cenas: CenaCompilada[] = b.cenas.map((cena, i) => {
    const inicioNaPecaFrames = acumulado;
    acumulado += cenasFrames[i] - (transicoes[i]?.duracaoFrames ?? 0);

    const eventos: EventoCompilado[] = cena.eventos.map((e, j) => {
      const porFormato: DiagnosticoEvento['porFormato'] = {};
      let maiorTotal = 0;
      let irmaoDoMaior = 0;
      let irmaosDoMaior = 1;

      for (const formato of b.formatos) {
        const {largura, altura} = DIMENSAO[formato];
        const z = layout({largura, altura, razaoFonte: razao ?? largura / altura});
        // `pista` vem do briefing e o ENCAIXE e derivado dela mais o formato. Nao ha
        // lista de preferencia e nao ha promocao a cartela: `resolverEncaixe` mede e
        // relata, e quem reprova e o portao de ritmo.
        const r = resolverEncaixe({
          texto: e.texto,
          papel: e.papel,
          pista: e.pista,
          zonas: z,
          cadencia: c,
          palavraAcento: e.palavraAcento,
        });
        porFormato[formato] = {
          encaixe: r.encaixe,
          corpo: r.corpo,
          linha: r.linha,
          tetoDeLinha: r.tetoDeLinha,
          noTeto: r.noTeto,
          dominancia: r.dominancia,
          piso: r.piso,
          domina: r.domina,
          candidataADominar: r.candidataADominar,
          porque: r.porque,
        };

        // `r.forma.irmaos` E A UNICA CONTAGEM. Ela sai de `CADENCIA_DO_PAPEL` dentro
        // de `formaTextoTela`, que e o mesmo lugar de onde sai o `atrasoFrames` de
        // cada palavra e o `duracaoCena` de `TextoTela`. Quando o compilador contava
        // por cadencia e a tela contava palavras, a etiqueta de 3 palavras recebia 36
        // frames e desenhava 42.
        const irmaos = r.forma.irmaos;
        const irmao =
          e.duracaoS !== undefined ? emFrames(e.duracaoS, fps) : duracaoDeIrmao(irmaos, c);
        const total = e.duracaoS !== undefined ? irmao : duracaoComIrmaos(irmaos, irmao, c);
        if (total > maiorTotal) {
          maiorTotal = total;
          irmaoDoMaior = irmao;
          irmaosDoMaior = irmaos;
        }
      }

      diagnosticoEventos.push({cena: i, indice: j, texto: e.texto, porFormato});

      return {
        papel: e.papel,
        texto: e.texto,
        familia: FAMILIA_DO_PAPEL[e.papel],
        cadenciaTexto: CADENCIA_DO_PAPEL[e.papel],
        pista: e.pista,
        irmaos: irmaosDoMaior,
        inicioFrames: emFrames(e.entradaS, fps),
        duracaoIrmaoFrames: irmaoDoMaior,
        duracaoFrames: maiorTotal,
        ...(e.palavraAcento !== undefined ? {palavraAcento: e.palavraAcento} : {}),
      };
    });

    return {
      duracaoFrames: cenasFrames[i],
      inicioNaPecaFrames,
      fonte: cena.fonte,
      aparaAntesFrames:
        cena.fonte.tipo === 'video' ? emFrames(cena.fonte.aparaAntesS, fps) : 0,
      eventos,
    };
  });

  return {
    _gerado_por: 'src/briefing/compilar.ts',
    // VAZIOS de proposito: quem sela e `selarPlano` de `briefing/impressao.ts`, chamado
    // por quem ESCREVE o arquivo. `compilar()` e puro e nao importa `node:crypto`.
    // Os DOIS sao selo: o do briefing diz de onde o plano veio, o do plano diz que ele
    // nao foi editado depois. Ver `sha256DoPlano`.
    _sha256Briefing: '',
    _sha256Plano: '',
    serie: b.serie,
    fps,
    formatos: b.formatos,
    duracaoFrames,
    razaoDaPeca: razao,
    cenas,
    transicoes,
    legenda: compilarLegenda(b, fontes.palavras, duracaoFrames),
    audio: b.audio,
    assets: b.assets,
    licencas: b.licencas,
    // DERIVADO, nao declarado: um booleano a parte podia dizer `false` com tres
    // recortes na lista, e o portao nao teria como saber qual dos dois acreditar.
    exigePreservacao: b.assets.length > 0,
    gancho: b.gancho,
    cta: b.cta,
    diagnostico: {
      eventos: diagnosticoEventos,
      licencasLigadas: (Object.keys(b.licencas) as Array<keyof typeof b.licencas>).filter(
        (k) => k !== 'justificativa' && b.licencas[k] === true,
      ) as Licenca[],
    },
  };
}

/**
 * A legenda sai do tempo da FONTE para o tempo da PECA, uma vez, aqui.
 *
 * Antes de 01/10/2026 `Legenda.tsx` somava o deslocamento ao frame corrente e
 * procurava o bloco -- o caminho oposto, que funcionava porque havia UMA cena. Com N
 * cenas a legenda fica FORA da `TransitionSeries`, no relogio da peca, e entao o rebase
 * tem que estar nos DADOS: e o compilador que o faz, e a fiacao passa deslocamento 0.
 *
 * A FORMULA, e por que ela nao soma `aparaAntesS` de cena
 *
 * Com N cenas ha N valores de `Cena.fonte.aparaAntesS` e UMA legenda, entao somar "o"
 * aparaAntesS deixa de ser definido. A resolucao e NEGAR a pergunta -- a legenda nao e
 * imagem, e a FALA, e a fala tem uma fonte de audio so na peca. Entao:
 *
 *   ancoraS  = conforme `legenda.ancora`
 *   desloc   = emFrames(entradaNaPecaS, fps) - emFrames(ancoraS, fps)
 *   bloco.inicioNaPeca = bloco.inicioFonteFrames + desloc
 *
 * `ancora: {tipo:'cena', indice}` e o UNICO jeito de um aparaAntesS de cena tocar a
 * legenda, e ele e NOMINAL: quem escreve aponta a cena com o dedo.
 */
function compilarLegenda(
  b: Briefing,
  palavras: Palavra[] | undefined,
  duracaoPecaFrames: number,
): ({blocos: Bloco[]} & DiagnosticoLegenda) | null {
  if (!b.legenda) return null;
  if (!palavras) {
    throw new Error(
      'o briefing declara legenda e nenhuma palavra foi passada para compilar(). ' +
        `Leia ${b.legenda.arquivo} e passe {palavras} -- o compilador e puro e nao le ` +
        'arquivo.',
    );
  }

  const ancoraS = (() => {
    const a = b.legenda.ancora;
    if (a.tipo === 'segundo') return a.valorS;
    if (a.tipo === 'locucao') {
      if (b.audio.locucao === null) {
        // `refinar()` ja recusou isto. Se chegou aqui, alguem chamou `compilar()` sem
        // refinar -- e um lanco e melhor que um 0 silencioso, que poria a legenda 34
        // frames fora de lugar sem ninguem perceber.
        throw new Error(
          'legenda ancorada na locucao e audio.locucao e null. `refinar()` recusa isto ' +
            'com o codigo legenda-sem-ancora: chame `exigirBriefingCoerente` antes.',
        );
      }
      return b.audio.locucao.aparaAntesS;
    }
    const cena = b.cenas[a.indice];
    if (!cena || cena.fonte.tipo !== 'video') {
      throw new Error(
        `legenda ancorada na cena ${a.indice}, que nao existe ou nao tem aparaAntesS. ` +
          '`refinar()` recusa isto com o codigo legenda-sem-ancora.',
      );
    }
    return cena.fonte.aparaAntesS;
  })();

  const deslocamentoFrames =
    emFrames(b.legenda.entradaNaPecaS ?? 0, b.fps) - emFrames(ancoraS, b.fps);

  const brutos = agrupar(palavras, {
    fps: b.fps,
    maxPalavras: b.legenda.maxPalavrasPorBloco ?? LEGENDA.maxPalavras,
  });

  const blocos: Bloco[] = [];
  let grudadosEmZero = 0;
  let maiorRecuoFrames = 0;
  let descartadosAntesDoInicio = 0;
  let descartadosDepoisDoFim = 0;

  for (const x of brutos) {
    const inicioFrame = x.inicioFrame + deslocamentoFrames;
    const fimFrame = x.fimFrame + deslocamentoFrames;

    // SEM NENHUM FRAME VISIVEL: descartado, e contado. Grudar em 0 um bloco cujo FIM
    // tambem e negativo nao conserva nada -- daria um bloco de duracao negativa.
    if (fimFrame <= 0) {
      descartadosAntesDoInicio++;
      continue;
    }

    // DEPOIS DO FIM DA PECA: descartado, e contado. O numero e o que denuncia uma peca
    // encurtada por `totalFixo` que comeu a fala.
    if (inicioFrame >= duracaoPecaFrames) {
      descartadosDepoisDoFim++;
      continue;
    }

    // ATRAVESSA O FRAME 0: GRUDADO em 0, nunca descartado, e contado com o recuo.
    //
    // E o caso ja vivido: o Whisper pos a primeira palavra dentro do ar morto, e o
    // `blocos.find()` de `Legenda.tsx` simplesmente nao acha nada -- a palavra
    // DESAPARECE EM SILENCIO. O portao de ritmo reprova quando o maior recuo passa do
    // piso de leitura de um bloco: abaixo disso e arredondamento de Whisper, acima e
    // ancora errada.
    if (inicioFrame < 0) {
      grudadosEmZero++;
      maiorRecuoFrames = Math.max(maiorRecuoFrames, -inicioFrame);
    }

    blocos.push({texto: x.texto, inicioFrame: Math.max(0, inicioFrame), fimFrame});
  }

  return {
    blocos,
    deslocamentoFrames,
    grudadosEmZero,
    maiorRecuoFrames,
    descartadosAntesDoInicio,
    descartadosDepoisDoFim,
  };
}

/**
 * `totalFixo`: devolve `falta` frames as cenas, proporcionalmente a duracao de cada
 * uma, jogando o resto inteiro na cena MAIS LONGA.
 *
 * Deterministico de proposito: empate vai para o indice menor. O portao de determinismo
 * compara o sha256 de dois renders do mesmo plano, e um `Math.random` ou uma ordem de
 * `Object.keys` aqui quebraria o portao sem mudar nada visivel.
 */
export function devolverFramesAsCenas(cenas: number[], falta: number): number[] {
  if (falta === 0) return [...cenas];
  const total = cenas.reduce((s, x) => s + x, 0);
  if (total <= 0) {
    throw new Error('devolverFramesAsCenas: as cenas somam zero frames');
  }
  const bruto = cenas.map((x) => (x * falta) / total);
  const inteiro = bruto.map((x) => Math.trunc(x));
  let resto = falta - inteiro.reduce((s, x) => s + x, 0);

  const ordem = cenas
    .map((x, i) => ({x, i}))
    .sort((a, bb) => (bb.x - a.x !== 0 ? bb.x - a.x : a.i - bb.i));
  let k = 0;
  const passo = resto >= 0 ? 1 : -1;
  while (resto !== 0) {
    inteiro[ordem[k % ordem.length].i] += passo;
    resto -= passo;
    k++;
  }

  const saida = cenas.map((x, i) => x + inteiro[i]);
  for (const [i, x] of saida.entries()) {
    if (x <= 0) {
      throw new Error(
        `devolverFramesAsCenas: a cena ${i} ficaria com ${x} frames. O alvo de ` +
          'duracao.alvoS e curto demais para o numero de cenas pedido.',
      );
    }
  }
  return saida;
}
