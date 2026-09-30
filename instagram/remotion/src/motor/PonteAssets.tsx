// A PROVA de que o motor de video enxerga os recortes de embalagem.
//
// Por que uma composicao existe so para isso: a ponte entre o portao de recorte
// (`instagram/recorte/publicar.py`) e o motor tem tres elos, e dois deles falham
// em silencio:
//
//   1. publicar.py copiou para a pasta certa?  -> ele imprime o que copiou
//   2. `--public-dir` aponta para a pasta que contem `assets/`?  -> SILENCIOSO
//   3. `staticFile('assets/x.png')` resolve para um arquivo que existe?
//
// O elo 2 e o traicoeiro: com a pasta publica errada, `staticFile` devolve uma
// URL bem-formada que aponta para nada. Essa composicao transforma esse silencio
// em falha: `<Img>` do Remotion abre um `delayRender` e MATA o render quando a
// imagem nao carrega, entao um still que sai e um still que provou os tres elos.
// Sem still, a ponte esta escrita, nao provada.
//
// FUNDO MAGENTA de proposito, e nao terra nem branco: o laudo de cada recorte
// afirma `alfa_minimo_no_rotulo: 255`, ou seja, nenhum pixel do rotulo ficou
// semitransparente. Magenta e a unica cor que nao existe em nenhuma das tres
// embalagens (marrom, creme, verde, canela), entao qualquer furo de alfa ou halo
// de recorte aparece como franja rosa a olho nu. Sobre fundo escuro o mesmo furo
// passa batido.
//
// A composicao NAO entra em peca entregavel. Ela e instrumento de conferencia,
// como a folha de contato.
//
// O QUE O PRIMEIRO STILL DELATOU, em 30/09/2026: as tres embalagens aparecem
// DEITADAS. Nao e defeito desta composicao -- os tres PNG sao 4096x2304, o
// buffer cru da foto, e os tres JPEG de origem trazem `EXIF Orientation=6`
// (girar 90 graus para exibir), que o pipeline de recorte nao aplicou. Em pe
// eles seriam 2304x4096. E a mesma armadilha que o motor ja documenta para o
// `pl.mp4` (displaymatrix -90), do lado da imagem estatica: a dimensao do
// buffer mente sobre a dimensao de exibicao.
//
// Esta composicao NAO gira a imagem de proposito. Girar aqui deixaria o still
// bonito e esconderia o defeito no asset, que continuaria deitado em toda peca
// que o usasse. O still tem que delatar.

import {Img, staticFile} from 'remotion';
import React from 'react';
import {SUB} from './pasta-publica';
import {COR, TIPO} from '../identidade/tokens';
import {PILHA} from '../identidade/tipografia';

/** Magenta puro: cor ausente das tres embalagens, entao delata furo de alfa. */
const MAGENTA = '#ff00ff';

export type PropsPonte = {
  /**
   * Nomes de arquivo dentro de `assets/` da pasta publica -- so o nome, o
   * prefixo entra aqui. Sao os tres que `publicar.py` publica hoje; ficam em
   * props para que um projeto com outro conjunto nao precise de outro
   * componente.
   */
  arquivos: string[];
};

export const PONTE_PADRAO: PropsPonte = {
  arquivos: ['classico-250g.png', 'suave-250g.png', 'canela-250g.png'],
};

export const PonteAssets: React.FC<PropsPonte> = ({arquivos}) => (
  <div
    style={{
      flex: 1,
      backgroundColor: MAGENTA,
      display: 'flex',
      flexDirection: 'row',
      alignItems: 'center',
      justifyContent: 'space-evenly',
      padding: 40,
    }}
  >
    {arquivos.map((arquivo) => (
      <div
        key={arquivo}
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 24,
          flex: 1,
        }}
      >
        <Img
          // O prefixo `assets/` sai de SUB, o mesmo lugar de onde Fonte.tsx tira
          // `fonte/`. Se a convencao de pasta mudar, muda num lugar so.
          src={staticFile(`${SUB.assets}/${arquivo}`)}
          style={{
            // `contain`, nao `cover`: `cover` recortaria a embalagem e um rotulo
            // cortado na borda pareceria erro de recorte na hora de olhar.
            objectFit: 'contain',
            maxWidth: '100%',
            maxHeight: 1400,
          }}
        />
        {/* O nome na tela vira o still auto-identificavel: da para dizer QUAL
            embalagem faltou sem contar posicao. */}
        <span
          style={{
            fontFamily: PILHA.dado,
            fontWeight: TIPO.dado.peso,
            fontSize: 30,
            color: COR.terra,
            backgroundColor: COR.creme,
            padding: '6px 14px',
          }}
        >
          {arquivo}
        </span>
      </div>
    ))}
  </div>
);
