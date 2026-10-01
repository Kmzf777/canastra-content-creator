// AS TABELAS DE PAPEL. Puras, sem React e sem remotion.
//
// Um evento de texto declara o PAPEL dele, e o papel decide tres coisas que o
// briefing NAO escolhe: a familia de tipografia, a cadencia de revelacao e a pista
// onde ele mora por padrao.
//
// POR QUE O BRIEFING NAO ESCOLHE
//
// Um botao que quem escreve o briefing pode girar sem saber avaliar produz
// inconsistencia silenciosa entre pecas da MESMA serie -- e a licao 8 do CLAUDE.md
// (coesao de serie) aplicada a tempo em vez de cenario. Tabela por papel da coesao
// de graca: toda manchete de toda peca revela por palavra.

import type {Papel} from '../identidade/tipografia';
// `Pista` vem de `./pista`. Os dois imports sao `import type`, que o transpilador
// apaga: nenhum efeito de modulo entra aqui, e e por isso que `esquema.ts` pode
// importar deste arquivo sem puxar `loadFont` para dentro do vitest.
import type {Pista} from './pista';

/**
 * Os papeis que um EVENTO de cena pode ter. `legenda` NAO esta aqui.
 *
 * A legenda e camada de PECA, fora da `TransitionSeries`. Dentro de uma cena ela
 * seria remontada por cena e, na janela de crossfade, duas legendas com textos
 * diferentes ficariam no ar ao mesmo tempo -- bug garantido e invisivel em
 * miniatura. A familia de tipografia dela continua existindo (Inter Bold, em
 * `FAMILIA_DO_PAPEL`), e isso nao a torna papel de evento.
 */
export const PAPEIS_DE_EVENTO = ['manchete', 'dado', 'etiqueta'] as const;
export type PapelEvento = (typeof PAPEIS_DE_EVENTO)[number];

/**
 * Papel de evento (e a legenda) -> familia de tipografia.
 *
 * O MAPA E OBRIGATORIO, NAO COSMETICO. Medido em 30/09/2026:
 * `formaTextoTela({papel: 'etiqueta', ...})` lancava
 * `TypeError: Cannot read properties of undefined (reading 'x')`, porque o papel era
 * indexado DIRETO em `GLIFOS`, cujas chaves sao manchete/corpo/dado.
 *
 * `legenda` esta na tabela porque ela nomeia a familia que a CAMADA `Legenda` usa --
 * e nao porque legenda seja papel de evento. Ver `PAPEIS_DE_EVENTO`.
 */
export const FAMILIA_DO_PAPEL: Record<PapelEvento | 'legenda', Papel> = {
  manchete: 'manchete', // Archivo Black, alturaLinha 1,088 (hhea)
  dado: 'dado', // IBM Plex Mono, avanco 0,6 em fixo, alturaLinha 1,3
  etiqueta: 'dado', // rotulo e carimbo: mono resolve
  legenda: 'corpo', // Inter Bold, alturaLinha 1,21
};

/** Como o texto de cada papel se revela. */
export type CadenciaTexto = 'palavra' | 'linha' | 'bloco';

/**
 * Papel -> cadencia de revelacao.
 *
 * A DO `dado` E FORCADA POR MEDICAO, NAO POR GOSTO. `duracaoDaFrase('R$ 39,90')`
 * trata `R$` e `39,90` como dois irmaos; um cartao de preco que revela `R$` e o
 * numero 3 frames depois le como defeito, nao como ritmo. Cada linha de um dado e um
 * CAMPO, e o stagger e por linha.
 *
 * `etiqueta` entra por bloco porque um carimbo nao tem ritmo interno: ou esta no
 * quadro ou nao esta.
 */
export const CADENCIA_DO_PAPEL: Record<PapelEvento, CadenciaTexto> = {
  manchete: 'palavra',
  dado: 'linha',
  etiqueta: 'bloco',
};

/**
 * Papel -> pista SUGERIDA.
 *
 * NAO E UM DEFAULT DO MOTOR. `pista` e obrigatorio no briefing, e nenhum passo do
 * compilador le esta tabela para preencher campo em branco -- default escondido e o
 * que este desenho proibe em toda parte. Ela existe para a skill
 * `canastra-briefing` ESCREVER o campo no arquivo: assim a escolha fica visivel no
 * JSON, onde o Rafael a le e a muda, em vez de morar no motor.
 *
 * `manchete` -> `topo` porque e a faixa que `layout()` ja reservava para ela.
 * `dado` -> `principal` porque um cartao numerico e o elemento dominante da cena
 * dele, e `proibicoes.md:19` pede um dominante por cena.
 * `etiqueta` -> `topo` porque carimbo mora na borda. Manchete e etiqueta na mesma
 * pista ao mesmo tempo e ERRO DE BRIEFING, pego por `refinar.ts` -- e erro explicito
 * e melhor que sobreposicao silenciosa, que e o defeito medido do motor antigo: a
 * caixa da manchete e a da legenda se intersectavam em 90,20 px no eixo x no 1:1.
 *
 * `rodape` NAO aparece nesta tabela: ela e a caixa da camada `Legenda`.
 */
export const PISTA_PADRAO: Record<PapelEvento, Pista> = {
  manchete: 'topo',
  dado: 'principal',
  etiqueta: 'topo',
};
