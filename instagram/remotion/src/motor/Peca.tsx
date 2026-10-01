// A PECA. Uma composicao unica que serve todos os formatos: ela nao sabe se e Reel,
// Feed 1:1, 4:5 ou 16:9 -- pergunta a dimensao do quadro ao Remotion e deixa `layout()`
// decidir onde cada camada vive. E isso que faz o 1:1 ser REENQUADRAMENTO e nao recorte
// do 9:16, e nenhuma cena, nenhum 4:5 e nenhum briefing cria um `PecaFeed`.
//
// A ARVORE, e por que ela e esta:
//
//   AbsoluteFill(terra)
//     TransitionSeries          AS CENAS, e so elas
//       Sequence(premountFor)   -> Cena: fonte + eventos, no relogio DA CENA
//     Legenda                   FORA: relogio da PECA, continua
//     Trilha                    FORA: relogio da PECA
//
// POR QUE A LEGENDA FICA FORA
//
// A legenda e a fala, e a fala nao reinicia porque a imagem trocou. Dentro da
// `TransitionSeries` ela seria remontada por cena, o deslocamento viraria um numero por
// cena, e na janela de crossfade DUAS legendas com textos diferentes ficariam no ar ao
// mesmo tempo -- bug garantido e invisivel em miniatura. Fora, ela e uma camada so e
// fica POR CIMA da transicao, que e o comportamento certo.
//
// A TRANSICAO GASTA FRAMES, ELA NAO SOMA
//
// Durante a transicao as DUAS cenas sao renderizadas, entao
// `duracaoPeca = Sigma cenas - Sigma transicoes`. Quem faz essa conta e `compilar.ts`;
// aqui so se le `cena.duracaoFrames` e `t.duracaoFrames`. Se a conta nao fosse feita
// la, a peca sairia mais CURTA que o briefing pede -- com exit 0.
//
// `TransitionSeries.Overlay` EXISTE, NAO E USADO, E NAO E DECLARADO -- DE PROPOSITO
//
// Ele renderiza sobre o corte sem mexer na duracao, e o uso canonico dele e light leak
// e flash. `proibicoes.md:16` proibe "Flash branco instantaneo". Um
// `<TransitionSeries.Overlay />` vazio no JSX seria codigo morto que o proximo leitor
// tenta preencher, e a `TransitionSeries` tem invariante sobre overlay adjacente -- um
// overlay vazio no lugar errado vira erro de runtime no render, nao aviso. Este
// comentario explica sem criar o risco.
//
// POR QUE OS FILHOS SAO UM ARRAY E NAO FRAGMENTS
//
// `TransitionSeries` inspeciona os filhos diretos para saber o que e cena e o que e
// transicao. Embrulhar um par cena+transicao num `<React.Fragment>` esconde os dois
// dele. Um array plano com `key` em cada item e o que ele entende.

// Nao ha `Sequence` nem `Audio` neste import: quem sequencia e a `TransitionSeries`, e
// o `<Audio>` vive em `camadas/Trilha.tsx`.
import {AbsoluteFill, useVideoConfig} from 'remotion';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {wipe} from '@remotion/transitions/wipe';
import React from 'react';
import type {Plano} from '../briefing/compilar';
import {COR} from '../identidade/tokens';
import {Cena} from './Cena';
import {Legenda} from './camadas/Legenda';
import {Trilha} from './camadas/Trilha';
import {layout} from './layout';
import {pistas} from './pista';

// As tres funcoes de tempo sao REEXPORTADAS de `tempo-de-cena.ts`, onde elas tem teste.
// Elas nao podem morar aqui: este arquivo importa `camadas/Legenda`, que puxa
// `identidade/tipografia.ts`, que faz `loadFont` no topo do modulo e derruba o vitest em
// ambiente `node` com `TypeError: Invalid URL`. A reexportacao existe para quem le a
// arvore achar as tres no lugar onde espera.
export {
  frameDaCenaNoFrameDaPeca,
  janelaDaCenaNaPeca,
  janelaDoEventoNaPeca,
} from './tempo-de-cena';

/**
 * As quatro direcoes de `wipe`, pelo tipo do proprio pacote.
 *
 * O plano escrevia `Parameters<typeof wipe>[0]['direction']`, que nao compila: o
 * parametro de `wipe()` e OPCIONAL, entao `Parameters<typeof wipe>[0]` e
 * `WipeProps | undefined` e indexar `['direction']` nele da TS2339 (medido). O
 * `NonNullable` e o conserto minimo, e ele mantem o tipo vindo do pacote em vez de
 * repetir as quatro strings aqui -- o enum do briefing ja as lista uma vez.
 */
type DirecaoDeWipe = NonNullable<Parameters<typeof wipe>[0]>['direction'];

export const Peca: React.FC<Plano> = (p) => {
  const {width, height, fps} = useVideoConfig();
  const zonas = layout({
    largura: width,
    altura: height,
    // `razaoDaPeca` e a MENOR razao entre as cenas que entram por CONTAIN
    // (`enquadramento: 'faixa'`): com ela, a caixa de legenda cabe sobre a imagem de
    // todas elas. `null` = nenhuma cena em contain, e ai a razao e a do quadro e a
    // imagem o ocupa inteiro. Cena que PREENCHE nao entra nessa conta e tambem nao usa
    // `zonas.video` -- ver a caixa da fonte em `Cena.tsx`.
    razaoFonte: p.razaoDaPeca ?? width / height,
  });

  const filhos: React.ReactNode[] = [];
  p.cenas.forEach((cena, i) => {
    filhos.push(
      <TransitionSeries.Sequence
        key={`cena-${i}`}
        durationInFrames={cena.duracaoFrames}
        // UM SEGUNDO de pre-montagem, derivado de fps. E onde a fonte da cena SEGUINTE
        // tem de estar bufferizada antes do crossfade comecar: sem isso o primeiro
        // frame da transicao pode ser desenhado antes do decodificador estar pronto, e
        // o frame errado vai GRAVADO no arquivo com exit 0.
        premountFor={fps}
      >
        <Cena cena={cena} zonas={zonas} />
      </TransitionSeries.Sequence>,
    );

    const t = p.transicoes[i];
    if (!t || t.duracaoFrames === 0) return;

    // DOIS RAMOS DE JSX, E NAO UM TERNARIO NO `presentation`.
    //
    // `TransitionSeries.Transition` e GENERICO nas props da apresentacao, e um
    // ternario forca TS a unificar `TransitionPresentation<FadeProps>` com
    // `TransitionPresentation<WipeProps>` -- que nao tem propriedade em comum. Medido:
    // `tsc` recusa com TS2322 ("has no properties in common"). Dois elementos deixam
    // cada um inferir o proprio parametro.
    //
    // `presentation` NUNCA e omitido: o default do Remotion e `slide()`, que ninguem do
    // nosso lado escolheu e que encosta em whip pan (`proibicoes.md:16`). `iris`,
    // `clockWipe` e `flip` ficam fora pelo mesmo motivo, e por isso o enum de transicao
    // e fechado em corte/fade/wipe.
    const timing = linearTiming({durationInFrames: t.duracaoFrames});
    filhos.push(
      t.tipo === 'wipe' ? (
        <TransitionSeries.Transition
          key={`transicao-${i}`}
          timing={timing}
          presentation={wipe({direction: t.direcao as DirecaoDeWipe})}
        />
      ) : (
        <TransitionSeries.Transition
          key={`transicao-${i}`}
          timing={timing}
          presentation={fade()}
        />
      ),
    );
  });

  return (
    // O fundo e terra, nao preto e nunca branco: no 1:1 a sobra ao lado da coluna fica
    // visivel, e branco com texto centrado e exatamente o padrao de modelo generativo
    // que `proibicoes.md:13` barra.
    <AbsoluteFill style={{backgroundColor: COR.terra}}>
      <TransitionSeries>{filhos}</TransitionSeries>

      {p.legenda ? (
        <Legenda
          blocos={p.legenda.blocos}
          caixa={pistas(zonas).rodape}
          escala={width / 1080}
          // ZERO: o compilador ja entregou os blocos no relogio da PECA. O deslocamento
          // existia porque `Legenda.tsx` convertia o relogio na hora; com N cenas isso
          // seria um numero por cena, e "o" aparaAntesS deixaria de ser definido.
          deslocamentoSegundos={0}
        />
      ) : null}

      {/* AS DUAS FAIXAS, no relogio da PECA, fora da TransitionSeries. A locucao mora
          em `public/fonte/` (material cru do projeto, e `pl.wav` ja esta la); a trilha
          mora em `public/audio/`, subpasta nova, porque musica licenciada tem
          procedencia e licenca que material gravado por nos nao tem. */}
      <Trilha audio={p.audio} duracaoPecaFrames={p.duracaoFrames} />
    </AbsoluteFill>
  );
};
