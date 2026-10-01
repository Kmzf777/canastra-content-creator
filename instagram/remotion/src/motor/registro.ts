// O REGISTRO DA FOTO REAL. Puro.
//
// `proibicoes.md:24-25`, textualmente: "Foto real entra por um registro que declara a
// origem (moldura, cartao, tela cheia), nunca como recorte flutuando."
//
// A regra da marca cumprida por CONSTRUCAO: `registro` e obrigatorio no esquema, sem
// default, e a geometria dos tres esta aqui, com teste. Um `.tsx` decidindo isto no
// meio de um `style` seria a regra cumprida por lembranca.
//
// NENHUM NUMERO NOVO
//
// Os recuos saem de `MARGEM`, que o motor ja usa para area segura, e as sombras de
// `SOMBRA`, que ja tem um perfil por material. Inventar uma "largura de moldura" seria
// escolher no olho um numero que muda de significado a cada formato -- e este arquivo
// nao tem constante numerica propria. Confira: as unicas literais abaixo sao 0, 1, 2 e
// o 100 da conversao para porcento.

import {SOMBRA} from '../identidade/tokens';
import {MARGEM, type Caixa} from './layout';

export type Registro = 'moldura' | 'cartao' | 'telaCheia';

/**
 * Perfil de sombra de cada registro. Nunca a mesma sombra em duas camadas -- a regra
 * da tabela de tokens.
 *
 * `telaCheia` nao tem sombra porque nao tem borda: nao ha onde a sombra cair.
 */
export const SOMBRA_DO_REGISTRO: Record<
  Registro,
  {dy: number; blur: number; op: number} | null
> = {
  moldura: SOMBRA.papel,
  cartao: SOMBRA.cartao,
  telaCheia: null,
};

/**
 * Onde a foto mora dentro da caixa da cena, por registro.
 *
 * `telaCheia` ..... a foto e o quadro.
 * `moldura` ....... recua `MARGEM.lado` (14,81%) nos dois eixos, simetrico: o terra
 *                   em volta e o passe-partout, e a foto se declara como foto
 *                   emoldurada.
 * `cartao` ........ recua `MARGEM.topo` (5%) nos dois eixos e ANCORA NO ALTO,
 *                   deixando a sobra embaixo -- e a geometria de um cartao apoiado, e
 *                   e onde a legenda passa.
 *
 * TODO RECUO E RELATIVO A `caixa`, NAO AO QUADRO. `Cena.tsx` passa `zonas.video`
 * quando a cena esta em contain, e essa caixa nao comeca em 0,0 no 1:1: um registro
 * que assumisse o canto poria a moldura fora da imagem.
 */
export function caixaDoRegistro(registro: Registro, caixa: Caixa): Caixa {
  if (registro === 'telaCheia') return {...caixa};

  if (registro === 'moldura') {
    const dx = caixa.largura * MARGEM.lado;
    const dy = caixa.altura * MARGEM.lado;
    return {
      x: caixa.x + dx,
      y: caixa.y + dy,
      largura: caixa.largura - 2 * dx,
      altura: caixa.altura - 2 * dy,
    };
  }

  const dx = caixa.largura * MARGEM.topo;
  const dy = caixa.altura * MARGEM.topo;
  return {
    x: caixa.x + dx,
    y: caixa.y + dy,
    largura: caixa.largura - 2 * dx,
    // Ancorado no alto: a sobra fica embaixo, onde a legenda corre. A altura e a da
    // caixa menos o recuo de topo, vezes a fracao que a area segura ja define -- o que
    // deixa o cartao mais raso que a caixa sem inventar uma fracao nova.
    altura: (caixa.altura - 2 * dy) * (1 - MARGEM.topo - MARGEM.base),
  };
}

export type Enquadramento =
  | {tipo: 'faixa'}
  | {tipo: 'recorte'; x: number; y: number; largura: number; altura: number};

/**
 * Recorte em FRACAO da fonte -> largura e deslocamento em porcento da caixa.
 *
 * A fracao existe para o mesmo briefing servir a foto de 4032x3024 e a regravacao dela
 * em outra resolucao sem reescrever numero. O CSS quer porcento, e a conversao e uma
 * divisao -- feita aqui, uma vez, com teste, em vez de dentro de um template de
 * `style`.
 */
export function recorteEmPorcento(e: Enquadramento): {
  larguraPorcento: number;
  alturaPorcento: number;
  esquerdaPorcento: number;
  topoPorcento: number;
} {
  if (e.tipo === 'faixa') {
    return {larguraPorcento: 100, alturaPorcento: 100, esquerdaPorcento: 0, topoPorcento: 0};
  }
  return {
    larguraPorcento: 100 / e.largura,
    alturaPorcento: 100 / e.altura,
    esquerdaPorcento: -(e.x / e.largura) * 100,
    topoPorcento: -(e.y / e.altura) * 100,
  };
}
