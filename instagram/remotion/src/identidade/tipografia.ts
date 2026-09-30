// A tipografia da marca, carregada de arquivo local.
//
// NOME: `tipografia.ts`, e nao `fontes.ts`, porque neste motor "fonte" ja quer
// dizer o VIDEO DE ORIGEM (`src/motor/camadas/Fonte.tsx`). A pasta ao lado,
// `fontes/`, guarda os .ttf -- esses sim sao arquivos de fonte tipografica.
//
// ---------------------------------------------------------------------------
// POR QUE ESTE ARQUIVO EXISTE
//
// `tokens.ts` declara TIPO desde o comeco do motor: manchete em Archivo Black,
// corpo em Inter 700, dado em IBM Plex Mono 500. So que ate 30/09/2026 NADA no
// motor carregava essas familias. `Legenda.tsx` escrevia `fontFamily: 'Inter'`
// e o Chrome headless, que nao tem Inter instalada, caiu no default dele --
// Times New Roman -- sem erro, sem aviso e com exit 0.
//
// Medido no still do frame 270 da composicao `Reel` ANTES da correcao: a
// legenda "private label" saiu com serifa de Times, ocupando 415x69 px. Todos
// os MP4 renderizados ate aquela data estao com a tipografia errada.
//
// E a licao 3 do CLAUDE.md aplicada a tipografia: exit 0 nao prova que a fonte
// carregou.
//
// ---------------------------------------------------------------------------
// ARQUIVO LOCAL, NAO `@remotion/google-fonts`
//
// `@remotion/google-fonts` busca o .woff2 em fonts.gstatic.com durante o render.
// Duas razoes para nao usar aqui:
//
//   1. O portao 3 (`src/verificacao/determinismo.ts`) nomeia "fonte carregada
//      por rede" como causa de render nao deterministico. Nao faz sentido o
//      conserto introduzir exatamente o que o portao procura.
//   2. Uma maquina offline volta a cair no fallback em silencio -- o bug que
//      este arquivo existe para matar.
//
// Entao os tres .ttf vivem em `src/identidade/fontes/`, versionados, e entram no
// bundle pela regra `asset/resource` do bundler do Remotion (ver
// `src/tipos-assets.d.ts`). Foram baixados uma vez da API v1 do Google Fonts com
// User-Agent antigo, que devolve o arquivo INTEIRO em vez dos recortes por
// unicode-range -- um recorte `latin` sozinho deixaria acento de pt-BR de fora
// em algum texto futuro.
//
// ---------------------------------------------------------------------------
// A GUARDA
//
// Carregar nao basta: o modo de falha que custou a rodada anterior foi
// silencioso. Entao depois de carregar, cada familia e MEDIDA -- a largura de
// uma amostra de texto sob a familia alvo contra a largura da mesma amostra sob
// uma familia que nao existe, que e por definicao o fallback do navegador.
// Larguras iguais = a familia nao foi aplicada = `cancelRender`. O render morre
// em vez de entregar Times New Roman achando que entregou Inter.

import {loadFont} from '@remotion/fonts';
import {cancelRender, continueRender, delayRender} from 'remotion';
import {TIPO} from './tokens';

import arquivoManchete from './fontes/ArchivoBlack-Regular.ttf';
import arquivoCorpo from './fontes/Inter-Bold.ttf';
import arquivoDado from './fontes/IBMPlexMono-Medium.ttf';

export type Papel = 'manchete' | 'corpo' | 'dado';

/**
 * As tres familias. O NOME vem de `tokens.ts` e os BYTES vem do arquivo: se um
 * dia os dois divergirem, a guarda abaixo reprova em vez de deixar passar.
 */
export const FAMILIAS = [
  {papel: 'manchete', familia: TIPO.manchete.familia, peso: TIPO.manchete.peso, url: arquivoManchete},
  {papel: 'corpo',    familia: TIPO.corpo.familia,    peso: TIPO.corpo.peso,    url: arquivoCorpo},
  {papel: 'dado',     familia: TIPO.dado.familia,     peso: TIPO.dado.peso,     url: arquivoDado},
] as const satisfies ReadonlyArray<{
  papel: Papel;
  familia: string;
  peso: number;
  url: string;
}>;

/**
 * A pilha para usar em `fontFamily`.
 *
 * O fallback existe para o caso de a guarda nao rodar (Studio em modo de
 * desenvolvimento, por exemplo): entre errar para uma grotesca e errar para
 * Times New Roman, a grotesca ao menos nao desmonta o enquadramento da legenda.
 * Ele NAO substitui a guarda -- num render de producao a familia certa e a
 * unica aceita.
 */
export const PILHA: Record<Papel, string> = {
  manchete: `"${TIPO.manchete.familia}", "Arial Black", Impact, sans-serif`,
  corpo: `"${TIPO.corpo.familia}", "Helvetica Neue", Arial, sans-serif`,
  dado: `"${TIPO.dado.familia}", "Courier New", monospace`,
};

// ---------------------------------------------------------------------------
// guarda

/** Uma familia que nao existe em lugar nenhum: e ela que mede o fallback. */
const INEXISTENTE = 'CanastraFamiliaQueNaoExisteEmLugarNenhum';

/**
 * A amostra medida. Tem acento de pt-BR de proposito: se o arquivo baixado
 * fosse um recorte sem `latin-ext`, esses glifos cairiam no fallback e a
 * largura denunciaria.
 */
const AMOSTRA = 'Canastra private label 250g CAO acucar 12,5';

export type Medida = {
  papel: Papel;
  familia: string;
  peso: number;
  /** largura da AMOSTRA a 78px sob a familia alvo */
  larguraAlvo: number;
  /** largura da AMOSTRA a 78px sob o fallback do navegador */
  larguraFallback: number;
  aplicou: boolean;
};

function larguraDe(familia: string, peso: number): number {
  const ctx = document.createElement('canvas').getContext('2d');
  if (!ctx) {
    throw new Error(
      'sem contexto 2d de canvas: nao da para provar que a fonte foi aplicada',
    );
  }
  // O shorthand do canvas segue o do CSS: familia com espaco precisa de aspas.
  ctx.font = `${peso} 78px "${familia}"`;
  return ctx.measureText(AMOSTRA).width;
}

export function medirTipografia(): Medida[] {
  return FAMILIAS.map((f) => {
    const larguraAlvo = larguraDe(f.familia, f.peso);
    const larguraFallback = larguraDe(INEXISTENTE, f.peso);
    return {
      papel: f.papel,
      familia: f.familia,
      peso: f.peso,
      larguraAlvo,
      larguraFallback,
      aplicou: larguraAlvo !== larguraFallback,
    };
  });
}

// ---------------------------------------------------------------------------
// carregamento

const espera = delayRender(
  'Canastra: carregando Archivo Black, Inter e IBM Plex Mono de arquivo local',
);

/**
 * Resolve com as medidas das tres familias, ou rejeita se alguma nao aplicou.
 * Exportada para inspecao; o motor nao precisa esperar por ela a mao, porque o
 * `delayRender` acima ja segura o primeiro frame.
 */
export const tipografiaPronta: Promise<Medida[]> = (async () => {
  await Promise.all(
    FAMILIAS.map((f) =>
      loadFont({
        family: f.familia,
        url: f.url,
        weight: String(f.peso),
        format: 'truetype',
        // `block`, nao `swap`: num render nao existe "mostrar o fallback
        // enquanto carrega" que nao seja um frame errado gravado no arquivo.
        display: 'block',
      }),
    ),
  );
  await document.fonts.ready;

  const medidas = medirTipografia();
  const faltando = medidas.filter((m) => !m.aplicou);
  if (faltando.length > 0) {
    throw new Error(
      'a tipografia da marca NAO foi aplicada em ' +
        faltando.map((m) => `${m.familia} (${m.papel})`).join(', ') +
        '. A amostra mediu a mesma largura que o fallback do navegador, ou ' +
        'seja, o Chrome esta desenhando a fonte dele. Confira se os .ttf de ' +
        'src/identidade/fontes/ existem e se o nome em tokens.ts bate com o ' +
        'nome de familia de dentro do arquivo.',
    );
  }
  return medidas;
})();

tipografiaPronta.then(
  (medidas) => {
    for (const m of medidas) {
      // Aparece no log do render: a prova de que carregou, no proprio lugar
      // onde antes nao aparecia nada.
      console.log(
        `[fonte] ${m.papel.padEnd(8)} ${m.familia} ${m.peso} - amostra ` +
          `${m.larguraAlvo.toFixed(1)}px (fallback seria ` +
          `${m.larguraFallback.toFixed(1)}px)`,
      );
    }
    continueRender(espera);
  },
  (e: Error) => cancelRender(e),
);
