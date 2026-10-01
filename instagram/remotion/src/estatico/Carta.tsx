// O cartao estatico 4:5.
//
// A IMAGEM entra como pixel -- gerada pelo ChatGPT ou composta com o rotulo
// real por cima. O TEXTO DA PECA entra como codigo. A divisao nao e estetica,
// e de garantia: a letra impressa na embalagem viaja na foto e se confere; o
// preco e a altitude nao tem foto de onde vir, entao sao desenhados, e desenhar
// e a unica forma de eles sairem exatos.
//
// O TEXTO NUNCA PISA NA IMAGEM. Ele vive numa faixa solida no rodape, e o
// motivo esta medido em `moldes.ts`: sobreposto ao packshot, o contraste do
// creme caiu a 1,09:1 na terceira linha. A correcao obvia -- um scrim escuro --
// e proibida por `identidade/proibicoes.md`, que barra gradiente por cima da
// embalagem. Faixa propria resolve as duas coisas de uma vez.
//
// Nenhuma cor nova: tudo de `identidade/tokens.ts`. Se o cartao inventar uma
// paleta propria, reel e estatico deixam de parecer a mesma marca -- e a licao
// 8 e exatamente uma serie que perdeu coesao por falta de cenario declarado num
// lugar so.

import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {COR, TIPO} from '../identidade/tokens';
import {PILHA} from '../identidade/tipografia';
import {
  MOLDES_ESTATICO,
  areaImagem,
  faixaDeTexto,
  validarProps,
} from './moldes';

export type PropsCarta = {
  molde: string;
  /** Caminho dentro do `--public-dir`. */
  imagem: string;
  dados: Record<string, string>;
};

// O primeiro campo e o heroi da peca; os outros sao apoio. Um elemento
// dominante por cena.
const CORPO_HEROI = 104;
const CORPO_APOIO = 40;
const ESPACO = 8; // multiplo de 8

export const Carta: React.FC<PropsCarta> = ({molde, imagem, dados}) => {
  // `validarProps` LEVANTA se faltar, sobrar ou vier vazio. Deixar levantar e
  // intencional: um still que sai com campo faltando passa despercebido, um
  // render que falha nao passa.
  const linhas = validarProps(molde, dados);
  const m = MOLDES_ESTATICO[molde];
  const img = areaImagem(m);
  const faixa = faixaDeTexto(m);
  const recuo = Math.round(m.largura * m.margem);

  return (
    <AbsoluteFill style={{backgroundColor: COR.terra}}>
      <div
        style={{
          position: 'absolute',
          left: img.x,
          top: img.y,
          width: img.largura,
          height: img.altura,
          overflow: 'hidden',
        }}
      >
        <Img
          src={staticFile(imagem)}
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      </div>

      <div
        style={{
          position: 'absolute',
          left: faixa.x,
          top: faixa.y,
          width: faixa.largura,
          height: faixa.altura,
          backgroundColor: COR.terra,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          paddingLeft: recuo,
          paddingRight: recuo,
          gap: ESPACO,
          boxSizing: 'border-box',
        }}
      >
        {linhas.map((texto, i) => (
          <div
            key={m.campos[i]}
            style={{
              fontFamily: PILHA.dado,
              fontWeight: TIPO.dado.peso,
              fontSize: i === 0 ? CORPO_HEROI : CORPO_APOIO,
              // O heroi em creme; o apoio no mesmo creme com opacidade, que
              // mantem UMA cor de frente em vez de inventar um segundo tom.
              color: COR.creme,
              opacity: i === 0 ? 1 : 0.82,
              lineHeight: 1.15,
            }}
          >
            {texto}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
