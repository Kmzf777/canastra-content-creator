// Os moldes de peca estatica: dimensao, campos e area segura.
//
// POR QUE ISTO NAO USA `motor/layout.ts`. A area segura de la e de REEL, e a
// margem de base e 16% justamente para liberar a interface do Reels -- botao,
// legenda, perfil. Um estatico 4:5 de feed nao tem essa interface por cima,
// entao herdar 16% de base seria jogar fora um sexto do quadro por um motivo
// que nao se aplica. Formato diferente, restricao diferente, margem diferente.
//
// O efeito colateral e bom: a peca estatica nao depende de um modulo que esta
// sendo reescrito, e as duas coisas evoluem sem se derrubar.
//
// Este arquivo ESPELHA o catalogo Python (`instagram/estaticos/catalogo.py`).
// A duplicacao e deliberada -- os dois lados falam linguagens diferentes e a
// costura entre eles e um arquivo .json de props, nunca JSON inline (no shell
// do Windows as aspas somem). `carta-props.test.ts` existe para a duplicacao
// nao virar divergencia em silencio.

export type Caixa = {x: number; y: number; largura: number; altura: number};

export type MoldeEstatico = {
  campos: string[];
  largura: number;
  altura: number;
  /** Fracao de cada eixo que vira margem. Mesma em cima, baixo e lados. */
  margem: number;
  /** Fracao da altura reservada a FAIXA DE TEXTO, no rodape. */
  faixaTexto: number;
};

// 6% = meio da faixa title-safe de 5 a 8%.
const MARGEM_ESTATICO = 0.06;

// POR QUE EXISTE UMA FAIXA SOLIDA E NAO UM SCRIM SOBRE A IMAGEM.
//
// Medido em 30/09/2026 no primeiro still: com as tres linhas sobrepostas ao
// packshot, o contraste do creme caiu para 4,42:1 na primeira linha, 3,43:1 na
// segunda e 1,09:1 na terceira -- essa ultima e invisivel. A causa e estrutural
// e nao se resolve escolhendo outra cor: o bloco de texto atravessa um fundo que
// vai de preto (o pacote) a branco (o ciclorama), e nenhuma cor fixa sobrevive a
// essa amplitude. O packshot de fundo colorido e pior ainda, 2,46:1.
//
// A saida obvia seria um scrim escuro atras do texto. ELA E PROIBIDA:
// `identidade/proibicoes.md` barra "qualquer efeito que altere pixel dentro da
// embalagem, incluindo glow, gradiente por cima e correcao de cor local". A
// regra existe para proteger o rotulo, e um gradiente sobre o pacote a viola.
//
// Entao o texto nunca pisa na imagem: ele tem faixa propria, em COR.terra. O
// contraste passa a ser uma constante do molde em vez de uma loteria da foto.
const FAIXA_TEXTO = 0.26;

export const MOLDES_ESTATICO: Record<string, MoldeEstatico> = {
  'cartao-produto': {
    campos: ['preco', 'altitude', 'local'],
    largura: 1080,
    altura: 1350,
    margem: MARGEM_ESTATICO,
    faixaTexto: FAIXA_TEXTO,
  },
};

/** Area util da peca, derivada das dimensoes -- nenhum pixel chumbado. */
export function areaSegura(molde: MoldeEstatico): Caixa {
  const x = Math.round(molde.largura * molde.margem);
  const y = Math.round(molde.altura * molde.margem);
  return {
    x,
    y,
    largura: molde.largura - 2 * x,
    altura: molde.altura - 2 * y,
  };
}

/** A faixa solida do rodape, onde o texto vive. Nunca sobrepoe a imagem. */
export function faixaDeTexto(molde: MoldeEstatico): Caixa {
  const altura = Math.round(molde.altura * molde.faixaTexto);
  return {x: 0, y: molde.altura - altura, largura: molde.largura, altura};
}

/** A regiao da imagem: tudo acima da faixa. */
export function areaImagem(molde: MoldeEstatico): Caixa {
  return {
    x: 0,
    y: 0,
    largura: molde.largura,
    altura: molde.altura - faixaDeTexto(molde).altura,
  };
}

/**
 * Valida os props contra o molde e devolve os valores NA ORDEM declarada.
 *
 * Levantar e intencional: um render que sai com campo faltando e pior que um
 * que falha, porque ninguem percebe.
 */
export function validarProps(
  molde: string,
  dados: Record<string, string>,
): string[] {
  const m = MOLDES_ESTATICO[molde];
  if (!m) {
    throw new Error(
      `molde '${molde}' nao existe. Validos: ${Object.keys(MOLDES_ESTATICO).join(', ')}`,
    );
  }

  const faltando = m.campos.filter((c) => !(c in dados));
  if (faltando.length) {
    throw new Error(`props sem os campos: ${faltando.join(', ')}`);
  }
  const sobrando = Object.keys(dados).filter((c) => !m.campos.includes(c));
  if (sobrando.length) {
    throw new Error(`props com campos fora do molde: ${sobrando.join(', ')}`);
  }
  const vazios = m.campos.filter((c) => !dados[c].trim());
  if (vazios.length) {
    throw new Error(`props com campos vazios: ${vazios.join(', ')}`);
  }
  return m.campos.map((c) => dados[c]);
}
