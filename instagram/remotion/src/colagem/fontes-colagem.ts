// As duas vozes tipográficas que a SÉRIE DE COLAGEM acrescenta à marca.
//
//   Instrument Serif Italic (OFL)  — a serifa editorial solta ("and" no reel de colagem)
//   Permanent Marker (Apache 2.0)  — a letra de marcador das etiquetas presas no mural
//
// Baixadas de github.com/google/fonts em 07/10/2026, com a licença ao lado. Cobertura
// de pt-BR conferida na tabela cmap antes do uso: ÁÂÃÀÇÉÊÍÓÔÕÚ e minúsculas presentes.
//
// Mesma guarda de `identidade/tipografia.ts`: depois de carregar, mede a largura de
// uma amostra com acento sob a família e sob uma família inexistente. Larguras iguais
// = o Chrome desenhou o fallback = `cancelRender`. Fonte errada não vai para o arquivo.
//
// Importar este módulo é efeito colateral (abre um delayRender): só os componentes
// .tsx da colagem o importam, nunca um .ts testado pelo vitest.

import {loadFont} from '@remotion/fonts';
import {cancelRender, continueRender, delayRender} from 'remotion';
import arquivoSerifa from './fontes/InstrumentSerif-Italic.ttf';
import arquivoMarcador from './fontes/PermanentMarker-Regular.ttf';

export const PILHA_COLAGEM = {
  serifa: '"Instrument Serif", Georgia, serif',
  marcador: '"Permanent Marker", "Comic Sans MS", cursive',
};

const FAMILIAS = [
  {familia: 'Instrument Serif', estilo: 'italic', url: arquivoSerifa},
  {familia: 'Permanent Marker', estilo: 'normal', url: arquivoMarcador},
] as const;

const AMOSTRA = 'Especial não é nome bonito: ação, açúcar, 1.250 m';

function largura(familia: string, estilo: string): number {
  const ctx = document.createElement('canvas').getContext('2d');
  if (!ctx) throw new Error('sem canvas 2d: não dá para provar a fonte');
  ctx.font = `${estilo} 400 80px "${familia}"`;
  return ctx.measureText(AMOSTRA).width;
}

const espera = delayRender('Colagem: carregando Instrument Serif Italic e Permanent Marker');

(async () => {
  await Promise.all(
    FAMILIAS.map((f) =>
      loadFont({family: f.familia, url: f.url, style: f.estilo, weight: '400', format: 'truetype', display: 'block'}),
    ),
  );
  await document.fonts.ready;
  const falhas = FAMILIAS.filter((f) => largura(f.familia, f.estilo) === largura('ColagemFamiliaInexistente', f.estilo));
  if (falhas.length) {
    throw new Error(`fonte da colagem NÃO aplicada: ${falhas.map((f) => f.familia).join(', ')}`);
  }
  for (const f of FAMILIAS) console.log(`[fonte] colagem ${f.familia} ${f.estilo} ok`);
})().then(
  () => continueRender(espera),
  (e: Error) => cancelRender(e),
);
