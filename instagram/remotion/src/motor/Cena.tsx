// UMA CENA: a fonte mais os eventos de texto dela.
//
// O RELOGIO AQUI E O DA CENA. Este componente mora dentro de
// `TransitionSeries.Sequence`, e o Remotion rebaseia `useCurrentFrame()`: o frame 0
// deste componente e o primeiro frame DESTA cena. Por isso `evento.inicioFrames` do
// plano e cena-relativo e entra direto, sem subtracao -- o contrario do que
// `PecaVideo.tsx` fazia com `manchete.inicioFrame - cortarAntesFrames`.
//
// OS EVENTOS SAO UMA LISTA, E ISSO E A TERCEIRA AUSENCIA FECHADA
//
// `PecaVideo.tsx` tinha `manchete?: Manchete | null` -- UM texto por peca inteira. A
// peca real media 91,4% do tempo sem nenhuma camada alem da legenda, com
// `proibicoes.md:11-12` proibindo tempo morto. Lista por cena e o que torna a serie
// "infografico" e a "voce-sabia" expressaveis; singular nao era limitacao de desenho,
// era o desenho.
//
// ORDEM DE ARVORE E ORDEM DE CAMADA (`z-index` nao vale no Remotion): fonte primeiro,
// eventos depois, na ordem em que o plano os lista. A legenda e a trilha NAO estao
// aqui: elas sao camadas da PECA, ver `Peca.tsx`.
//
// NENHUM NUMERO NASCE AQUI. Tempo vem do plano, geometria de `resolverEncaixe`,
// cadencia de `cadencia(fps)`. Se voce precisar de um numero neste arquivo, ele esta no
// lugar errado.

import {AbsoluteFill, useVideoConfig} from 'remotion';
import React from 'react';
import type {CenaCompilada} from '../briefing/compilar';
import {cadencia} from './cadencia';
import {Fonte} from './camadas/Fonte';
import {TextoTela} from './camadas/TextoTela';
import {resolverEncaixe} from './encaixe';
import type {Zonas} from './layout';

export const Cena: React.FC<{cena: CenaCompilada; zonas: Zonas}> = ({cena, zonas}) => {
  // `height` entra junto por causa da caixa da fonte que preenche o quadro, abaixo.
  const {fps, width, height} = useVideoConfig();
  const c = React.useMemo(() => cadencia(fps), [fps]);
  const escala = width / 1080;

  // MEMOIZADO, E ISSO NAO E OTIMIZACAO PREMATURA.
  //
  // `resolverEncaixe` faz uma BUSCA BINARIA de `formaTextoTela` por evento, e o corpo
  // deste componente roda em TODO FRAME da cena. Numa peca de 715 frames com 3 eventos
  // seriam mais de duas mil buscas binarias redundantes por render -- e `TextoTela.tsx`
  // memoiza `formaTextoTela` exatamente por esse motivo, que e o precedente escrito do
  // repositorio.
  //
  // As dependencias sao a cena, as zonas e a cadencia: nenhuma delas muda por frame.
  const postos = React.useMemo(
    () =>
      cena.eventos.map((e) => {
        const r = resolverEncaixe({
          texto: e.texto,
          papel: e.papel,
          pista: e.pista,
          zonas,
          cadencia: c,
          palavraAcento: e.palavraAcento,
        });
        // As MESMAS zonas que `resolverEncaixe` usou para medir. Passar outras daria um
        // corpo diferente do que o compilador relatou no diagnostico, e o portao de
        // ritmo estaria medindo uma peca que nao e a renderizada.
        const zonasDoEvento: Zonas =
          r.modo === 'cartela' ? zonas : {...zonas, manchete: r.caixa};
        return {e, r, zonasDoEvento};
      }),
    [cena.eventos, zonas, c],
  );

  // A CAIXA DA FONTE NAO E SEMPRE `zonas.video`.
  //
  // `zonas.video` e a caixa de CONTAIN: ela e letterboxada quando a razao da peca nao e
  // a do quadro. Uma cena que declara `enquadramento: 'preencher'` (video) ou
  // `{tipo: 'recorte'}` (foto) esta dizendo o contrario -- que ela CORTA para encher o
  // quadro --, e `registro: 'telaCheia'` exige `recorte` (o refinador recusa
  // `telaCheia` + `faixa`). Se essa cena recebesse `zonas.video`, "tela cheia" encheria
  // a FAIXA e nao o quadro: numa peca de razao 1,3333 no 9:16 a faixa e 1080x810 e
  // sobrariam 57,81% de terra chapado em cima e embaixo.
  //
  // Entao: cena que preenche recebe o QUADRO; cena em contain recebe `zonas.video`.
  // Numa peca sem nenhuma cena em contain, `razaoDaPeca()` devolve `null`, a razao vira
  // a do quadro e os dois valores coincidem -- este ramo so se separa na peca MISTA.
  //
  // O texto continua medido nas `zonas` da peca, que sao as mesmas que o compilador
  // relatou: deixar o evento seguir a caixa da cena faria o corpo da manchete mudar de
  // cena para cena, e o portao de ritmo estaria medindo outra peca.
  const preenche =
    (cena.fonte.tipo === 'video' && cena.fonte.enquadramento === 'preencher') ||
    (cena.fonte.tipo === 'foto' && cena.fonte.enquadramento.tipo === 'recorte');
  const caixaDaFonte = preenche
    ? {x: 0, y: 0, largura: width, altura: height}
    : zonas.video;

  return (
    <AbsoluteFill>
      <Fonte
        fonte={cena.fonte}
        caixa={caixaDaFonte}
        aparaAntesFrames={cena.aparaAntesFrames}
        duracaoCenaFrames={cena.duracaoFrames}
        escala={escala}
      />
      {postos.map(({e, r, zonasDoEvento}, i) => (
        <TextoTela
          key={`${i}-${e.texto}`}
          texto={e.texto}
          modo={r.modo}
          zonas={zonasDoEvento}
          inicioFrame={e.inicioFrames}
          duracaoFrames={e.duracaoIrmaoFrames}
          papel={e.papel}
          palavraAcento={e.palavraAcento}
        />
      ))}
    </AbsoluteFill>
  );
};
