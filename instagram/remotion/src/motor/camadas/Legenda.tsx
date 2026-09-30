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
// o frame 0 da peca e o frame `cortarAntesFrames` da fonte. Por isso o frame
// corrente e convertido para tempo-da-fonte antes de procurar o bloco. Quem
// passar blocos ja realinhados usa `deslocamentoFrames={0}`.

import {useCurrentFrame} from 'remotion';
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

export const Legenda: React.FC<{
  blocos: Bloco[];
  caixa: Caixa;
  escala: number;
  deslocamentoFrames?: number;
}> = ({blocos, caixa, escala, deslocamentoFrames = 0}) => {
  const f = useCurrentFrame() + deslocamentoFrames;
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
