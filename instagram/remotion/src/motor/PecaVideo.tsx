// A peca. Uma composicao unica que serve os dois formatos: ela nao sabe se e
// Reel ou feed, so pergunta a dimensao do quadro ao Remotion e deixa `layout()`
// decidir onde cada camada vive. E isso que faz o 1:1 ser REENQUADRAMENTO e nao
// recorte do 9:16.
//
// Ordem das camadas e a ordem da arvore -- `z-index` nao e suportado no
// Remotion. Fonte primeiro, manchete, legenda em cima. Nao reordene sem querer.
//
// ---------------------------------------------------------------------------
// A MANCHETE E OPCIONAL, E ISSO E UMA DECISAO
//
// `manchete` ausente, `null` ou com texto vazio => a peca sai COMPLETA, so sem
// manchete. Nao ha texto de reserva e nao ha erro: a maioria dos cortes de
// pitch nao precisa de titulo na tela, e um placeholder aqui seria a mesma
// armadilha do `_LEIA` que fez quatro MP4 sairem com legenda de exemplo
// queimada (ver o cabecalho de `scripts/gerar-props.mjs`).
//
// O TEXTO DA MANCHETE E CITACAO LITERAL DA FALA, nao copy de marketing. Quem
// prova isso e `tests/manchete-props.test.ts`, que le `transcricao.json` e
// `props.json` e falha se o texto nao for um trecho CONTIGUO da transcricao
// (so a caixa pode mudar). Sem esse portao, "manchete" e um campo de texto
// livre no meio de um pipeline que existe para nunca queimar frase inventada
// no quadro.
//
// ---------------------------------------------------------------------------
// `manchete.inicioFrame` ESTA NO TEMPO DA FONTE, COMO OS BLOCOS
//
// Mesma convencao do props.json inteiro: frame 0 e o primeiro frame do arquivo
// ORIGINAL, antes do corte do ar morto. Duas razoes para nao abrir excecao aqui:
//
//   1. O inicio da manchete e ancorado numa PALAVRA da transcricao, e a
//      transcricao esta em tempo de fonte. Guardar este campo em tempo de peca
//      obrigaria quem edita o props.json a fazer a subtracao de cabeca -- e
//      errar por 34 frames sem nada reclamar.
//   2. Um props.json com dois relogios e um props.json que alguem vai ler
//      errado.
//
// A conversao acontece aqui, uma vez: `inicioFrame - cortarAntesFrames`. A
// `Legenda` resolve o mesmo problema pelo caminho oposto (soma o deslocamento
// ao frame corrente) porque ela PROCURA um bloco numa lista; a manchete tem um
// inicio so, entao deslocar o inicio e mais direto que deslocar o relogio.
//
// Consequencia que vale escrever: se `inicioFrame < cortarAntesFrames`, a
// manchete comeca ANTES do frame 0 da peca e a entrada dela e cortada. Isso nao
// e barrado aqui -- pode ser intencional (manchete ja no ar no primeiro frame)
// -- mas `tests/manchete-props.test.ts` mede e reprova quando nao foi de
// proposito.
//
// ---------------------------------------------------------------------------
// SEM `<Sequence>`, DE PROPOSITO
//
// `TextoTela` recebe `inicioFrame` e devolve `null` fora da janela dela, que ela
// mesma dimensiona por `duracaoDaFrase`. Embrulhar em `<Sequence>` exigiria
// repetir esse calculo aqui em `durationInFrames` -- e o cabecalho de
// `TextoTela.tsx` avisa que o erro natural e dimensionar por `DURACAO_MINIMA`
// crua, o que corta a saida da ultima palavra. Uma conta so, num lugar so.

import {AbsoluteFill, useVideoConfig} from 'remotion';
import React from 'react';
import {layout} from './layout';
import {Fonte} from './camadas/Fonte';
import {Legenda} from './camadas/Legenda';
import {TextoTela} from './camadas/TextoTela';
import type {Modo} from './camadas/texto-forma';
import {COR} from '../identidade/tokens';
import type {Bloco} from '../legenda/agrupar';

export type Manchete = {
  /**
   * CITACAO LITERAL da fala, palavra por palavra. Caixa alta e permitida (e a
   * unica transformacao permitida); acrescentar, trocar ou reordenar palavra
   * nao e.
   */
  texto: string;
  /** `sobreImagem` divide o quadro com o video; `cartela` cobre o video. */
  modo: Modo;
  /** frame no tempo da FONTE em que a PRIMEIRA palavra comeca a entrar. */
  inicioFrame: number;
  /** indice da UNICA palavra que recebe `COR.acento`. */
  palavraAcento?: number;
};

export type Props = {
  /** Caminho relativo a pasta publica do render (ver Fonte.tsx). */
  arquivo: string;
  /** Razao de EXIBICAO da fonte, honrando a matriz de rotacao. 9/16 no pl.mp4. */
  razaoFonte: number;
  /** Ar morto da cabeca, em frames. 34 no pl.mp4 (1,14 s a 30 fps). */
  cortarAntesFrames: number;
  /** Blocos de legenda no tempo da FONTE, antes do corte. Ver Legenda.tsx. */
  blocos: Bloco[];
  /** OPCIONAL. Ausente ou `null` = peca sem manchete, sem erro. */
  manchete?: Manchete | null;
};

export const PecaVideo: React.FC<Props> = (p) => {
  const {width, height} = useVideoConfig();
  const z = layout({largura: width, altura: height, razaoFonte: p.razaoFonte});

  // Texto em branco conta como ausencia: um props.json com `"texto": ""` nao
  // deve montar uma camada que nao desenha nada.
  const manchete =
    p.manchete && p.manchete.texto.trim().length > 0 ? p.manchete : null;

  return (
    // O fundo e terra, nao preto e nunca branco: no 1:1 a sobra ao lado da
    // coluna de video fica visivel, e branco com texto centrado e exatamente o
    // padrao de modelo generativo que `proibicoes.md` barra.
    <AbsoluteFill style={{backgroundColor: COR.terra}}>
      <Fonte
        arquivo={p.arquivo}
        caixa={z.video}
        cortarAntesFrames={p.cortarAntesFrames}
      />
      {/* DEPOIS de Fonte e ANTES de Legenda, nos dois modos. Em `sobreImagem` a
          ordem e a que o cabecalho de TextoTela.tsx pede. Em `cartela` ela e uma
          ESCOLHA com consequencia visivel: a cartela cobre o video mas NAO cobre
          a legenda, que continua correndo por cima do terra chapado. A
          alternativa -- cartela por cima de tudo -- apagaria a legenda por dois
          segundos e quebraria a continuidade de leitura, que e pior. */}
      {manchete ? (
        <TextoTela
          texto={manchete.texto}
          modo={manchete.modo}
          zonas={z}
          inicioFrame={manchete.inicioFrame - p.cortarAntesFrames}
          palavraAcento={manchete.palavraAcento}
        />
      ) : null}
      <Legenda
        blocos={p.blocos}
        caixa={z.legenda}
        escala={width / 1080}
        deslocamentoFrames={p.cortarAntesFrames}
      />
    </AbsoluteFill>
  );
};
