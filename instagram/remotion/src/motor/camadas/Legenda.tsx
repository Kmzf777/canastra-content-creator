// Camada de legenda. Corte seco de proposito: a referencia medida tem 93% da
// massa de movimento ja no primeiro frame, logo easing de entrada aqui e erro,
// nao refinamento. Sem fade, sem escala, sem pop.
//
// A sombra e a `SOMBRA.sobreVideo` dos tokens (dy 14, blur 26, op 0,42). E ela
// que garante leitura de creme sobre imagem em movimento; os outros perfis de
// sombra sao de material parado e nao aguentam video.
//
// DESLOCAMENTO -- o detalhe que erra a legenda inteira por 1,14 s:
// os blocos vem da transcricao da FONTE, entao os frames deles estao no tempo
// do arquivo original. A composicao, porem, comeca depois do corte do ar morto:
// o frame 0 da peca e o frame do ar morto da fonte. Por isso o frame corrente e
// convertido para tempo-da-fonte antes de procurar o bloco. Quem passar blocos
// ja realinhados usa `deslocamentoSegundos={0}`.
//
// E O DESLOCAMENTO E EM SEGUNDOS, nao em frames:
// o ar morto medido no `pl.mp4` e 1,14 SEGUNDO. Ate 01/10/2026 esta camada
// recebia `deslocamentoFrames` e somava o numero cru ao frame corrente. Numa
// composicao de 60 fps os mesmos 34 frames deslocariam 0,567 s em vez de 1,14 s,
// e a legenda inteira sairia meio segundo fora da fala -- com exit 0, porque
// `blocos.find()` acha SEMPRE algum bloco, so o errado. O mesmo modo de falha
// que a cadencia de texto tinha, e a razao de esta camada chamar `useVideoConfig`:
// a conversao segundo->frame usa o fps DA COMPOSICAO, por `emFrames`.
//
// Os blocos continuam em FRAMES, e isso e deliberado: eles sao produzidos por
// `agrupar(palavras, {fps})`, que ja recebe o fps de quem compila a peca. O
// deslocamento nao -- ele e medida do ARQUIVO, como a duracao e a razao.

import {useCurrentFrame, useVideoConfig} from 'remotion';
import React from 'react';
import {LEGENDA, TIPO} from '../../identidade/tokens';
// `PILHA.corpo` no lugar de `TIPO.corpo.familia` cru: importar daqui tambem
// PUXA o carregamento das tres familias (o modulo tem efeito colateral), entao
// esta camada nao depende de alguem ter lembrado de importar a tipografia la em
// cima. Antes de 30/09/2026 nao havia carregamento nenhum e esta legenda saia
// em Times New Roman sem avisar.
import {PILHA} from '../../identidade/tipografia';
import type {Bloco} from '../../legenda/agrupar';
import type {Caixa} from '../layout';
import {emFrames} from '../relogio';

export const Legenda: React.FC<{
  /** No tempo da FONTE, em frames do fps DESTA composicao. */
  blocos: Bloco[];
  caixa: Caixa;
  escala: number;
  /**
   * Ar morto cortado da cabeca da fonte, em SEGUNDOS. `0` quando os blocos ja
   * vem realinhados ao tempo da peca. Ver o cabecalho.
   */
  deslocamentoSegundos?: number;
}> = ({blocos, caixa, escala, deslocamentoSegundos = 0}) => {
  const {fps} = useVideoConfig();
  const f = useCurrentFrame() + emFrames(deslocamentoSegundos, fps);
  const b = blocos.find((x) => f >= x.inicioFrame && f < x.fimFrame);
  if (!b) return null;

  return (
    <div
      style={{
        position: 'absolute',
        left: caixa.x,
        top: caixa.y,
        width: caixa.largura,
        height: caixa.altura,
        display: 'flex',
        alignItems: 'flex-end',
        justifyContent: 'center',
      }}
    >
      <span
        style={{
          fontFamily: PILHA.corpo,
          fontWeight: TIPO.corpo.peso,
          fontSize: LEGENDA.corpoEm1080 * escala,
          lineHeight: LEGENDA.entrelinha,
          color: LEGENDA.cor,
          textAlign: 'center',
          textShadow: `0 ${14 * escala}px ${26 * escala}px rgba(0,0,0,.42)`,
        }}
      >
        {b.texto}
      </span>
    </div>
  );
};
