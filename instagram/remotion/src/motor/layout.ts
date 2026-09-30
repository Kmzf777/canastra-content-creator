// Funcao de zonas. O coracao do motor: o post 1:1 nao e recorte do 9:16, e a
// mesma timeline REENQUADRADA. Quem decide onde cada camada vive e esta funcao,
// a partir de {largura, altura} do quadro e da razao da fonte.
//
// Regra que nao se negocia: o video nunca e cortado na largura para caber num
// quadro mais largo. Ele vira uma coluna e a sobra recebe a manchete.

export type Caixa = {x: number; y: number; largura: number; altura: number};
export type Zonas = {
  seguro: Caixa; video: Caixa; legenda: Caixa; manchete: Caixa;
  formato: '9:16' | '1:1' | '16:9' | 'outro';
};

// Margens de area segura em 1080x1920, medidas em referencia de Reels.
const MARGEM = {topo: 90, base: 310, lado: 160};

export function layout(
  {largura, altura, razaoFonte}:
  {largura: number; altura: number; razaoFonte: number}
): Zonas {
  const k = largura / 1080;                       // escala relativa a 1080 de largura
  const seguro: Caixa = {
    x: MARGEM.lado * k,
    y: MARGEM.topo * k,
    largura: largura - 2 * MARGEM.lado * k,
    altura: altura - (MARGEM.topo + MARGEM.base) * k,
  };

  const r = largura / altura;
  const formato: Zonas['formato'] =
    Math.abs(r - 9 / 16) < 0.01 ? '9:16' :
    Math.abs(r - 1) < 0.01 ? '1:1' :
    Math.abs(r - 16 / 9) < 0.01 ? '16:9' : 'outro';

  let video: Caixa, manchete: Caixa;

  if (formato === '9:16') {
    // fonte e o quadro tem a mesma razao: preenche tudo
    video = {x: 0, y: 0, largura, altura};
    manchete = {x: seguro.x, y: seguro.y, largura: seguro.largura, altura: altura * 0.18};
  } else {
    // quadro mais largo que a fonte: o video vira uma COLUNA, nao um recorte.
    // O encaixe e "contain" nos dois eixos, nunca "cover": se o quadro fosse
    // mais ESTREITO que a fonte (9:19.5, por exemplo), escalar so pela altura
    // faria o video vazar a largura -- que e exatamente o recorte que este
    // motor existe para nao fazer. Nos formatos previstos (1:1 e 16:9) o limite
    // e a altura, entao o resultado e identico a escalar pela altura.
    const larguraVideo = Math.min(largura, altura * razaoFonte);
    const alturaVideo = larguraVideo / razaoFonte;
    video = {
      x: 0,
      y: (altura - alturaVideo) / 2,
      largura: larguraVideo,
      altura: alturaVideo,
    };
    // a manchete ocupa a sobra a direita, com respiro
    const sobra = largura - larguraVideo;
    manchete = {
      x: larguraVideo + sobra * 0.08,
      y: altura * 0.12,
      largura: sobra * 0.84,
      altura: altura * 0.76,
    };
  }

  // legenda sempre ancorada no rodape da area segura, sobre o video
  const alturaLegenda = altura * 0.16;
  const legenda: Caixa = {
    x: Math.max(seguro.x, video.x + 16 * k),
    y: seguro.y + seguro.altura - alturaLegenda,
    largura: Math.min(seguro.largura, video.largura - 32 * k),
    altura: alturaLegenda,
  };

  return {seguro, video, legenda, manchete, formato};
}
