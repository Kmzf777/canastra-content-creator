// Camada de FONTE. Quatro tipos: video, foto, cor e grade.
//
// POR QUE DEIXOU DE SER SO VIDEO
//
// Antes de 01/10/2026 este arquivo montava `<Video>` sem alternativa, e o acervo tem
// 1 VIDEO contra 38 FOTOS verificadas -- 26 de lavoura mais 12 packshots. Cinco das
// doze series do catalogo partem de FOTO PARADA. `grep -rn "<Img" src/` so achava
// `PonteAssets.tsx`, que e instrumento de conferencia, nao peca.
//
// QUATRO COISAS QUE ESTA CAMADA RESOLVE E QUE NINGUEM MAIS RESOLVE
//
// 1. O CORTE DO AR MORTO, por `aparaAntesFrames`, nunca chumbado aqui -- cada projeto
//    tem o seu. `pl.mp4` tem 1,14 s, que a 30 fps sao 34 frames. A conversao ja
//    aconteceu no compilador, com o fps da composicao.
//
// 2. O RECORTE E DECISAO DO LAYOUT, NAO DESTA CAMADA. A caixa vem pronta de `layout()`
//    e de `Cena.tsx`; aqui so se obedece. `overflow: hidden` existe para que um erro
//    de meio pixel nao vaze da zona, nao para cortar de proposito.
//
// 3. A PRE-MONTAGEM da midia, que NAO e feita aqui. `premountFor` e prop da
//    `TransitionSeries.Sequence` em `Peca.tsx`, um nivel acima: pre-montar a CENA
//    cobre a fonte dela e mais os eventos, e pre-montar nos dois lugares montaria a
//    mesma midia duas vezes.
//
// 4. O GIRO DE UMA FOTO QUE PERDEU O EXIF. Ver `rotacaoGraus`, abaixo -- e a parte
//    desta camada que mais perto chegou de sair errada com exit 0.
//
// `arquivo` e o NOME do arquivo dentro da subpasta `fonte/` da pasta publica do
// projeto -- so `pl.mp4`, nunca um caminho. Quem sabe o prefixo e esta camada, por
// `SUB.fonte`. O prefixo entra aqui e nao no briefing de proposito: o briefing fala de
// MEDIDA (que arquivo, que razao, que corte), nao de arrumacao de pasta.
//
// O PUSH E DA CENA, NAO DA CAMADA
//
// `push(frame, duracaoCenaFrames)` e linear porque `proibicoes.md:21` pede "push de
// camera lento, nunca impacto", e qualquer easing concentra a velocidade em algum
// trecho -- que e justamente o impacto. A escala entra como `transform: scale()`.
//
// O GIRO, E POR QUE ELE E DECLARADO EM VEZ DE DESCOBERTO
//
// O Chrome aplica `EXIF Orientation` sozinho (`image-orientation: from-image` e o
// default), entao foto que TRAZ o metadado nao precisa de nada. Os recortes de
// embalagem, porem, perderam o metadado: medido em 01/10/2026, `classico-250g.png` e
// 4096x2304 com `rotacao: nenhuma`, e os packshots de origem sao `Orientation 6`.
// Olhado no pixel, os tres recortes saem DEITADOS. `sondar()` nao tem o que descobrir
// num arquivo que nao carrega o dado -- entao `rotacaoGraus` vem do briefing.
//
// Em 90 e 270 a caixa interna TROCA largura por altura antes de girar. Sem a troca, a
// imagem gira dentro de uma caixa com a proporcao errada e o `objectFit` recorta pelo
// eixo errado: o pacote sai em pe e CORTADO, que e pior que deitado, porque parece
// intencional.

import {Video} from '@remotion/media';
import {Img, staticFile, useCurrentFrame} from 'remotion';
import React from 'react';
import type {Fonte as FonteDeclarada} from '../../briefing/esquema';
import {COR} from '../../identidade/tokens';
import type {Caixa} from '../layout';
import {push} from '../movimento';
import {SUB} from '../pasta-publica';
import {caixaDoRegistro, recorteEmPorcento, SOMBRA_DO_REGISTRO} from '../registro';

export type PropsFonte = {
  fonte: FonteDeclarada;
  caixa: Caixa;
  /** frames de ar morto da cabeca (so `video` usa) */
  aparaAntesFrames: number;
  /** duracao DA CENA em frames: e sobre ela que o push corre */
  duracaoCenaFrames: number;
  /** escala do quadro: `largura / 1080`. Sombra e calha acompanham. */
  escala: number;
};

export const Fonte: React.FC<PropsFonte> = ({
  fonte,
  caixa,
  aparaAntesFrames,
  duracaoCenaFrames,
  escala,
}) => (
  <div
    style={{
      position: 'absolute',
      left: caixa.x,
      top: caixa.y,
      width: caixa.largura,
      height: caixa.altura,
      overflow: 'hidden',
      // O fundo e terra e nao preto: no 1:1 a sobra ao lado da coluna fica visivel, e
      // branco com texto centrado e exatamente o padrao de modelo generativo que
      // `proibicoes.md:13` barra. E e este fundo que recebe o alfa de um recorte PNG
      // -- "recorte sobre fundo" nao e um quinto tipo de fonte, e uma foto com alfa.
      backgroundColor: COR.terra,
    }}
  >
    <Conteudo
      fonte={fonte}
      caixa={{x: 0, y: 0, largura: caixa.largura, altura: caixa.altura}}
      aparaAntesFrames={aparaAntesFrames}
      duracaoCenaFrames={duracaoCenaFrames}
      escala={escala}
    />
  </div>
);

const Conteudo: React.FC<PropsFonte> = ({
  fonte,
  caixa,
  aparaAntesFrames,
  duracaoCenaFrames,
  escala,
}) => {
  const frame = useCurrentFrame();

  if (fonte.tipo === 'cor') {
    return <div style={{width: '100%', height: '100%', backgroundColor: fonte.cor}} />;
  }

  if (fonte.tipo === 'grade') {
    const calha = fonte.calha * escala;
    const largura = (caixa.largura - calha * (fonte.colunas - 1)) / fonte.colunas;
    const altura = (caixa.altura - calha * (fonte.linhas - 1)) / fonte.linhas;
    return (
      <div
        style={{
          display: 'grid',
          width: '100%',
          height: '100%',
          gridTemplateColumns: `repeat(${fonte.colunas}, 1fr)`,
          gridTemplateRows: `repeat(${fonte.linhas}, 1fr)`,
          gap: calha,
        }}
      >
        {fonte.celulas.map((celula, i) => (
          <div key={i} style={{position: 'relative', overflow: 'hidden'}}>
            <Conteudo
              fonte={celula}
              caixa={{x: 0, y: 0, largura, altura}}
              // A apara e do VIDEO daquela celula. Uma foto numa celula nao tem ar
              // morto para cortar, e passar o numero adiante seria um corte sem objeto.
              aparaAntesFrames={celula.tipo === 'video' ? aparaAntesFrames : 0}
              duracaoCenaFrames={duracaoCenaFrames}
              escala={escala}
            />
          </div>
        ))}
      </div>
    );
  }

  const escalaPush = fonte.camera === 'pushLento' ? push(frame, duracaoCenaFrames) : 1;

  if (fonte.tipo === 'video') {
    return (
      <Video
        src={staticFile(`${SUB.fonte}/${fonte.arquivo}`)}
        trimBefore={aparaAntesFrames}
        objectFit={fonte.enquadramento === 'preencher' ? 'cover' : 'contain'}
        style={{
          width: '100%',
          height: '100%',
          transform: `scale(${escalaPush})`,
          transformOrigin: 'center center',
        }}
      />
    );
  }

  // --- foto -----------------------------------------------------------------
  const dentro = caixaDoRegistro(fonte.registro, caixa);
  const r = recorteEmPorcento(fonte.enquadramento);
  const sombra = SOMBRA_DO_REGISTRO[fonte.registro];
  const giro = fonte.rotacaoGraus;
  // Em 90 e 270 a caixa que a imagem preenche tem os eixos TROCADOS: ela e medida
  // ANTES do giro. Sem isto o `objectFit` escolhe o eixo de recorte errado.
  const deitada = giro === 90 || giro === 270;
  const larguraInterna = deitada ? dentro.altura : dentro.largura;
  const alturaInterna = deitada ? dentro.largura : dentro.altura;

  return (
    <div
      style={{
        position: 'absolute',
        left: dentro.x,
        top: dentro.y,
        width: dentro.largura,
        height: dentro.altura,
        overflow: 'hidden',
        boxShadow: sombra
          ? `0 ${sombra.dy * escala}px ${sombra.blur * escala}px rgba(0,0,0,${sombra.op})`
          : undefined,
      }}
    >
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          width: larguraInterna,
          height: alturaInterna,
          overflow: 'hidden',
          // Centra a caixa pre-giro e GIRA em torno do centro. O push vem junto na
          // mesma transformacao: duas `transform` em elementos aninhados multiplicam
          // matriz, e uma so aqui mantem a conta legivel.
          transform: `translate(-50%, -50%) rotate(${giro}deg) scale(${escalaPush})`,
          transformOrigin: 'center center',
        }}
      >
        <Img
          src={staticFile(`${SUB.fonte}/${fonte.arquivo}`)}
          style={{
            position: 'absolute',
            width: `${r.larguraPorcento}%`,
            height: `${r.alturaPorcento}%`,
            left: `${r.esquerdaPorcento}%`,
            top: `${r.topoPorcento}%`,
            // `contain` na faixa e `cover` no recorte: no recorte a caixa JA esta na
            // razao pedida, entao cobrir nao corta nada que o briefing nao mandou.
            objectFit: fonte.enquadramento.tipo === 'faixa' ? 'contain' : 'cover',
          }}
        />
      </div>
    </div>
  );
};
