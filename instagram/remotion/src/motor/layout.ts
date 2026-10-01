// Funcao de zonas. O coracao do motor: o post 1:1 nao e recorte do 9:16, e a
// mesma timeline REENQUADRADA. Quem decide onde cada camada vive e esta funcao,
// a partir de {largura, altura} do quadro e da razao da fonte.
//
// Regra que nao se negocia: o video nunca e cortado na largura para caber num
// quadro mais largo. Ele vira uma coluna e a sobra recebe a manchete.

export type Caixa = {x: number; y: number; largura: number; altura: number};
export type Zonas = {
  seguro: Caixa; video: Caixa; legenda: Caixa; manchete: Caixa;
  formato: '9:16' | '1:1' | '4:5' | '16:9' | 'outro';
};

// MARGENS DE AREA SEGURA, EM FRACAO DO EIXO QUE CADA UMA CORTA.
//
// Antes de 30/09/2026 eram pixeis a 1080x1920 escalados por um `k` unico
// derivado da LARGURA. Medido rodando `layout()` com razaoFonte 9/16, a base
// efetiva como porcentagem da ALTURA:
//
//   1080x1920 ... 310,0 px = 16,15%
//   1080x1080 ... 310,0 px = 28,70%
//   1920x1080 ... 551,1 px = 51,03%   (area segura de 1351,1 x 368,9)
//
// No 1:1 quase um terco do quadro era margem de baixo; no 16:9 metade. E os 368,9
// px de altura do 16:9 sao exatamente o numero que `texto-forma.ts:205-206`
// registra como "texto de borda a borda, o oposto de respiro maior" -- o sintoma
// que `linhasDeFolga` tenta consertar nasce desta linha, nao da cartela.
//
// Agora cada margem e fracao do eixo que ela corta, entao a porcentagem e a
// MESMA nos tres formatos:
//
//   topo   5,00%  piso da faixa title-safe 5-8%. Eram 90 px = 4,69% a 1920 de
//                 altura, abaixo do piso; em 1920 de altura da 96,0 px.
//   base  16,00%  eram 310 px = 16,15% a 1920 de altura. Mesma faixa, agora
//                 constante.
//   lado  14,81%  160 px a 1080 de largura. ESTE NUMERO FOI ESCOLHIDO NO OLHO e
//                 nunca medido: esta fora da faixa 5-8% da convencao e fica
//                 porque e o que as pecas aprovadas usaram. Mudar a largura da
//                 manchete e decisao estetica, nao conserto -- entao fica, mas
//                 sem se chamar "medida".
export const MARGEM = {topo: 0.05, base: 0.16, lado: 160 / 1080};

export function layout(
  {largura, altura, razaoFonte}:
  {largura: number; altura: number; razaoFonte: number}
): Zonas {
  // `kx` NAO escala margem nenhuma. Ele sobra para as folgas em pixel da caixa
  // de legenda (16 e 32 px a 1080 de largura), que sao respiro contra a borda do
  // VIDEO e por isso acompanham a largura.
  const kx = largura / 1080;
  const seguro: Caixa = {
    x: MARGEM.lado * largura,
    y: MARGEM.topo * altura,
    largura: largura * (1 - 2 * MARGEM.lado),
    altura: altura * (1 - MARGEM.topo - MARGEM.base),
  };

  const r = largura / altura;
  const formato: Zonas['formato'] =
    Math.abs(r - 9 / 16) < 0.01 ? '9:16' :
    Math.abs(r - 1) < 0.01 ? '1:1' :
    Math.abs(r - 4 / 5) < 0.01 ? '4:5' :
    Math.abs(r - 16 / 9) < 0.01 ? '16:9' : 'outro';

  let video: Caixa, manchete: Caixa;

  // A pergunta certa nao e "qual e o rotulo", e "a fonte preenche a largura?".
  // Antes de 01/10/2026 o teste era `formato === '9:16'`, e com o 4:5 ganhando
  // rotulo isso viraria um ramo escolhido por nome em vez de por medida.
  const preencheALargura = Math.abs(altura * razaoFonte - largura) < 0.5;

  if (preencheALargura) {
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
  // O `x` e o `min` da largura tem que falar do MESMO ponto de partida.
  //
  // Antes de 01/10/2026 a largura era `Math.min(seguro.largura, video.largura -
  // 32 * kx)`: ela supoe que `x` seja `video.x + 16*kx` (e o que o `-32` significa,
  // 16 de respiro de cada lado do video), e o `x` usava `seguro.x`. Com o video em
  // coluna, `video.x = 0` e `seguro.x = 160`: a caixa desliza 144,00 px para a
  // direita levando a largura inteira, e a borda direita dela VAZA o video em
  // 128,00 px no 1:1, 128,00 no 4:5 e 227,56 no 16:9 (medido em 01/10/2026). E
  // nesse vazamento que a coluna da manchete mora: 735,50 - 645,30 = 90,20 px,
  // que e a intersecao em x que a auditoria relatou.
  //
  // Agora a borda direita e o MENOR entre a borda do seguro e a borda do video
  // menos o respiro, e a largura e a distancia dela ao `x` que realmente foi usado.
  //
  // CUSTO HONESTO, medido com a correcao aplicada: a largura util da legenda cai de
  // 575,50 para 431,50 px no 1:1 (-25,0%), de 727,38 para 583,38 no 4:5 (-19,8%) e
  // de 550,61 para 294,61 no 16:9 (-46,5%). O 9:16 nao muda em nada (x 160,00,
  // largura 760,00). Isso empurra a busca binaria de corpo da legenda para baixo
  // nesses formatos -- nao e conserto de graca.
  const xLegenda = Math.max(seguro.x, video.x + 16 * kx);
  const legenda: Caixa = {
    x: xLegenda,
    y: seguro.y + seguro.altura - alturaLegenda,
    largura:
      Math.min(seguro.x + seguro.largura, video.x + video.largura - 16 * kx) - xLegenda,
    altura: alturaLegenda,
  };

  return {seguro, video, legenda, manchete, formato};
}
