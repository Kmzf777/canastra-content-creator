// Camada de MANCHETE e KINETIC TYPE. Duas variantes, uma API.
//
// Este arquivo e so FIACAO. Toda decisao de tempo esta em `src/motor/movimento.ts`
// e toda decisao de geometria em `./texto-forma.ts`, os dois puros e cobertos
// por `tests/textotela.test.ts`. Aqui nao nasce nenhum numero: se voce precisar
// de um, ele vem de `tokens.ts` por um daqueles dois modulos.
//
// A razao da separacao e mecanica, nao estetica: este arquivo importa
// `tipografia.ts`, que faz `loadFont` no topo do modulo, e isso derruba o vitest
// em Node com `TypeError: Invalid URL`. Medido em 30/09/2026 -- um teste que so
// importava `Legenda.tsx` passou a asercao e o vitest ainda saiu com codigo 1.
// Logo: o que precisa de prova nao pode morar num `.tsx`.
//
// ---------------------------------------------------------------------------
// OS DOIS MODOS, PARA O USUARIO ESCOLHER OLHANDO
//
//   `sobreImagem`  A manchete divide o quadro com o video, que continua
//                  correndo. Sombra `SOMBRA.sobreVideo`, escalada pelo corpo,
//                  para garantir leitura de creme sobre imagem em movimento.
//                  Ancora no topo da faixa que `layout()` reservou, porque
//                  embaixo passa a legenda.
//
//   `cartela`      A tela inteira vira texto entre dois planos. Fundo
//                  `COR.terra` opaco -- e ele que "cobre" o video. Respiro
//                  maior: entrelinha natural da fonte e uma linha inteira de
//                  folga vertical, com o bloco centrado na area segura.
//
// PARA QUEM FOR MONTAR ISTO EM `PecaVideo.tsx`:
//
//   1. A cartela COBRE o video, nao o pausa. Se a intencao for congelar o
//      quadro atras, isso e trabalho da camada `Fonte`, nao desta.
//   2. O stagger empurra o fim junto com o comeco. Para dimensionar a
//      `<Sequence>`, use `duracaoDaFrase(texto)` de `./texto-forma`, nunca
//      `DURACAO_MINIMA` cru -- senao a ultima palavra perde a saida e
//      desaparece por corte.
//   3. Ordem de arvore e ordem de camada (`z-index` nao vale no Remotion).
//      `sobreImagem` entra DEPOIS de `Fonte` e ANTES de `Legenda`.
//
// ---------------------------------------------------------------------------
// O CONTRATO COM A MEDICAO
//
// `texto-forma.ts` escolhe o corpo somando larguras de avanco lidas dos .ttf.
// Essa conta so vale se o CSS nao mexer no tracking, entao `letterSpacing: 0` e
// explicito aqui. Kerning fica ligado: nestas grotescas os pares com kern
// APERTAM, logo o texto real sai igual ou mais estreito que o medido -- o lado
// seguro. Tracking positivo NAO tem esse consolo, e por isso e proibido nesta
// camada.

import {AbsoluteFill, useCurrentFrame} from 'remotion';
import React from 'react';
import {TIPO} from '../../identidade/tokens';
import {larguraEm} from '../../identidade/glifos';
// Importar `PILHA` (e nao `TIPO.x.familia` cru) tambem PUXA o carregamento das
// tres familias, porque `tipografia.ts` tem efeito colateral de modulo. Assim
// esta camada nao depende de alguem ter lembrado de importar a tipografia la em
// cima -- foi por essa falta que a legenda saiu em Times New Roman.
import {PILHA} from '../../identidade/tipografia';
import {duracaoComIrmaos, duracaoDeIrmao, progresso, push} from '../movimento';
import {formaTextoTela, type Modo, type PapelTexto} from './texto-forma';
import type {Zonas} from '../layout';

export type PropsTextoTela = {
  texto: string;
  modo: Modo;
  /** de `layout()`. Quem recorta contra a area segura e `formaTextoTela`. */
  zonas: Zonas;
  /** frame desta composicao em que a PRIMEIRA palavra comeca a entrar. */
  inicioFrame?: number;
  /**
   * Quantos frames CADA palavra fica presente. O padrao e `duracaoDeIrmao`, que
   * e maior que `DURACAO_MINIMA` justamente para a frase aparecer INTEIRA --
   * ver o comentario daquela funcao. A frase toda dura mais ainda por causa do
   * stagger; use `duracaoDaFrase(texto)` para dimensionar a `<Sequence>`.
   */
  duracaoFrames?: number;
  papel?: PapelTexto;
  /** indice da UNICA palavra que recebe `COR.acento`. */
  palavraAcento?: number;
};

export const TextoTela: React.FC<PropsTextoTela> = ({
  texto,
  modo,
  zonas,
  inicioFrame = 0,
  duracaoFrames,
  papel = 'manchete',
  palavraAcento,
}) => {
  const frame = useCurrentFrame();
  const t = frame - inicioFrame;

  const forma = React.useMemo(
    () => formaTextoTela({texto, modo, zonas, papel, palavraAcento}),
    [texto, modo, zonas, papel, palavraAcento],
  );

  if (forma.palavras.length === 0) return null;

  // A janela de cada palavra. O padrao cresce com o numero de palavras, senao a
  // primeira comeca a sair antes de a ultima entrar e a manchete nunca fica
  // legivel por inteiro -- ver `duracaoDeIrmao`.
  const duracaoPalavra = duracaoFrames ?? duracaoDeIrmao(forma.palavras.length);

  // A janela da CENA: do primeiro frame da primeira palavra ao ultimo frame da
  // ultima. O push de camera corre por cima dela inteira.
  const duracaoCena = duracaoComIrmaos(forma.palavras.length, duracaoPalavra);
  if (t < 0 || t >= duracaoCena) return null;

  // Estado do conjunto, sem stagger: e ele que liga o fundo da cartela.
  const conjunto = progresso(t, {inicio: 0, duracao: duracaoCena});

  // O espaco entre palavras vem da MESMA medida que quebrou as linhas. Usar
  // `gap` em vez de um caractere de espaco porque cada palavra e um elemento
  // proprio, com opacidade e escala propria.
  const espaco = larguraEm(' ', papel) * forma.corpo;

  return (
    <AbsoluteFill
      style={{
        // A cartela cobre o video com terra chapada; `sobreImagem` deixa passar.
        // A cor entra pela presenca do CONJUNTO, entao o cartao aparece e some
        // por fade de cor chapada -- nunca por flash, que `proibicoes.md` proibe.
        backgroundColor: forma.fundo ?? 'transparent',
        opacity: forma.fundo === null ? 1 : conjunto.presenca,
      }}
    >
      <div
        style={{
          position: 'absolute',
          left: forma.caixa.x,
          top: forma.caixa.y,
          width: forma.caixa.largura,
          height: forma.caixa.altura,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: forma.alinhaVertical,
          alignItems: forma.alinhaHorizontal,
          // Push de camera lento sobre o bloco inteiro, nunca impacto.
          transform: `scale(${push(t, duracaoCena)})`,
          transformOrigin: 'center center',
        }}
      >
        {forma.linhas.map((linha, iLinha) => (
          <div
            key={`${iLinha}-${linha}`}
            style={{
              display: 'flex',
              flexDirection: 'row',
              alignItems: 'baseline',
              gap: espaco,
              // A altura da linha e a entrelinha do modo: 0,96 apertado sobre
              // video, 1,088 natural da fonte na cartela.
              height: forma.corpo * forma.entrelinha,
            }}
          >
            {forma.palavras
              .filter((p) => p.linha === iLinha)
              .map((p) => {
                const e = progresso(t, {
                  inicio: p.atrasoFrames,
                  duracao: duracaoPalavra,
                });
                return (
                  <span
                    key={`${p.irmao}-${p.texto}`}
                    style={{
                      fontFamily: PILHA[papel],
                      fontWeight: TIPO[papel].peso,
                      fontSize: forma.corpo,
                      lineHeight: forma.entrelinha,
                      // Ver "O CONTRATO COM A MEDICAO" no cabecalho.
                      letterSpacing: 0,
                      color: p.cor,
                      whiteSpace: 'nowrap',
                      opacity: e.presenca,
                      // Pouso: entra 3% grande, assenta em 100%, sai em 97%.
                      // Uma direcao so, do primeiro ao ultimo frame -- repique
                      // seria easing elastico, e isso e proibido.
                      transform: `scale(${e.escala})`,
                      transformOrigin: 'center center',
                      textShadow: forma.sombra
                        ? `0 ${forma.sombra.dy}px ${forma.sombra.blur}px rgba(0,0,0,${forma.sombra.op})`
                        : undefined,
                    }}
                  >
                    {p.texto}
                  </span>
                );
              })}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
