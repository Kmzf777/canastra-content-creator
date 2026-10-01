// A FORMA do briefing, em zod. Sentido e `refinar.ts`; aritmetica e `compilar.ts`.
//
// ZOD PURO, SEM `@remotion/zod-types`
//
// `node_modules/@remotion/zod-types/package.json` declara
// `"dependencies": {"remotion": "4.0.530"}` (medido em 30/09/2026). Importar
// `remotion` num modulo que o vitest carrega e o modo de falha que `tipografia.ts`
// ja pagou: `loadFont` no topo do modulo derruba o vitest com
// `TypeError: Invalid URL`. `zColor()` e `zTextarea()`, quando entrarem, moram em
// `esquema-studio.ts` e so la. O prototipo `out/_spec-briefing/briefing.ts` os
// importava, e e por isso que ele vivia em `out/`, a unica raiz onde resolviam.
//
// UM RELOGIO SO: SEGUNDOS, CONTADOS DO INICIO DA CENA
//
// Nenhum campo deste arquivo esta em frames. A posicao de uma cena vem da ORDEM no
// array, nunca de um campo de tempo. A unica conversao do sistema e
// `emFrames(s, fps)` de `motor/relogio.ts`, chamada por `compilar.ts`.
//
// O tempo da FONTE e permitido APENAS COMO APARA -- um deslocamento que diz onde o
// arquivo comeca a ser usado, e que nunca posiciona nada na peca. So tres nomes tem
// essa permissao, e os tres carregam `apara` no nome para que a excecao seja
// legivel: `fonte.aparaAntesS`, `fonte.aparaDepoisS` e `audio.*.aparaAntesS`.
//
// TODO OBJETO E `strictObject`
//
// Campo desconhecido FALHA em vez de ser ignorado. E a licao 3 do CLAUDE.md
// aplicada a JSON: um briefing com `duracao_alvo: 24` em vez de `duracao.alvoS`
// renderizaria 3 segundos e sairia com exit 0. O prototipo usava `looseObject`, e
// com ele os quatro campos que a revisao da spec RETIROU (`zona`, `modo`, `preset`,
// `alvoLufs`) passariam em silencio, sem nada do novo ser aplicado.

import {z} from 'zod';
// `PAPEIS_DE_EVENTO` vem de `motor/evento.ts` e `PISTAS_DE_EVENTO` de
// `motor/pista.ts`, para nao existirem DUAS listas de cada coisa. Os dois modulos
// sao puros; `pista.ts` nao importa nada e `evento.ts` so importa um tipo dele, que
// o transpilador apaga -- entao `loadFont` nao e puxado para dentro do vitest por
// estas linhas.
import {PAPEIS_DE_EVENTO} from '../motor/evento';
import {PISTAS_DE_EVENTO} from '../motor/pista';

/** Os 12 slugs de `instagram/estrategia/05-formatos.md` secao 4, mais `avulsa`. */
export const SERIES = [
  'voce-sabia',
  'infografico',
  'arraste',
  'jornada',
  'capsula-parceiro',
  'piada',
  'meme-pacote',
  'preparo-slow',
  'bastidor',
  'objecao-preco',
  'safra-limitada',
  'convidado',
  'avulsa',
] as const;
export type Serie = (typeof SERIES)[number];

export const FORMATOS = ['9:16', '1:1', '4:5', '16:9'] as const;
export type Formato = (typeof FORMATOS)[number];

/**
 * Dimensao de cada formato, em pixel.
 *
 * `16:9` fica no enum porque `layout()` o rotula e porque a Tarefa 9 registra uma
 * `<Composition>` para ele, mas a margem de base dele e 51,03% da altura (medido):
 * e formato LATENTE, nao entrega.
 */
export const DIMENSAO: Record<Formato, {largura: number; altura: number}> = {
  '9:16': {largura: 1080, altura: 1920},
  '1:1': {largura: 1080, altura: 1080},
  '4:5': {largura: 1080, altura: 1350},
  '16:9': {largura: 1920, altura: 1080},
};

/** As 12 licencas de tecnica. Cada uma nomeia a linha de `proibicoes.md`. */
export const LICENCAS = [
  'particulas', // 11-12: "explosao de particula"
  'orbesDeBrilho', // 11: "brilho"
  'varreduraDeLuz', // 11: "brilho"
  'shockwave', // 11-12: particula + brilho
  'molaComOvershoot', // 11: "easing elastico"
  'revelarCaractereACaractere', // 14: "Revelar texto caractere a caractere"
  'flashNoCorte', // 16: "Flash branco instantaneo"
  'irisWipe', // 16: por vizinhanca com "whip pan"
  'motionBlurBurst', // 7-8: nomeia <CameraMotionBlur>
  'swipeMarcaTexto', // 20: seria o 2o saturado ao lado de COR.acento
  'highlightPalavraAtiva', // nao e proibicao: e 1 acento, mas troca 2,45x/s
  'aceitaTempoMorto', // 11-12: "tempo morto"
] as const;
export type Licenca = (typeof LICENCAS)[number];

export type Licencas = Record<Licenca, boolean> & {justificativa: string};

const zLicencas = z.strictObject({
  ...(Object.fromEntries(LICENCAS.map((k) => [k, z.boolean().default(false)])) as Record<
    Licenca,
    z.ZodDefault<z.ZodBoolean>
  >),
  /**
   * Por que alguma esta ligada. `refinar.ts` reprova licenca ligada com
   * justificativa curta -- ligar uma tecnica que colide com a marca e decisao, e
   * decisao sem motivo escrito nao sobrevive a proxima sessao.
   */
  justificativa: z.string().default(''),
});

/** Todas as 12 desligadas e sem justificativa: o estado em que um briefing nasce. */
export const LICENCAS_DESLIGADAS: Licencas = {
  ...(Object.fromEntries(LICENCAS.map((k) => [k, false])) as Record<Licenca, boolean>),
  justificativa: '',
};

/**
 * Movimento de camera sobre a fonte.
 *
 * O `Lento` esta no NOME de proposito: `proibicoes.md:21` pede "push de camera
 * lento, nunca impacto", e um enum chamado so `push` convidaria a segunda
 * velocidade. `pushLento` e o `PUSH` dos tokens, 1,00 -> 1,04.
 */
const zCamera = z.enum(['parado', 'pushLento']);
export type Camera = z.infer<typeof zCamera>;

const zFonteVideo = z.strictObject({
  tipo: z.literal('video'),
  /** nome do arquivo dentro de `public/fonte/`, nunca um caminho */
  arquivo: z.string().min(1),
  /**
   * Razao de EXIBICAO, honrando a matriz de rotacao. MEDIDA por `sondar()`, nunca
   * lida do container: `pl.mp4` grava 1024x576 e exibe 576x1024
   * (`displaymatrix -90`), e os 12 packshots leem 4096x2304 e exibem 2304x4096
   * (`EXIF Orientation 6`). Armadilha ja paga tres vezes neste repositorio.
   */
  razaoExibicao: z.number().positive(),
  /** apara: ar morto da cabeca, em segundos. 1,14 no `pl.mp4` */
  aparaAntesS: z.number().min(0),
  aparaDepoisS: z.number().min(0).optional(),
  enquadramento: z.enum(['faixa', 'preencher']),
  camera: zCamera,
});

const zRecorte = z.strictObject({
  tipo: z.literal('recorte'),
  /** em FRACAO do arquivo JA ORIENTADO (0..1), nunca em pixel */
  x: z.number().min(0).max(1),
  y: z.number().min(0).max(1),
  largura: z.number().gt(0).max(1),
  altura: z.number().gt(0).max(1),
});

const zFonteFoto = z.strictObject({
  tipo: z.literal('foto'),
  arquivo: z.string().min(1),
  razaoExibicao: z.number().positive(),
  /**
   * OBRIGATORIO, SEM DEFAULT. `proibicoes.md:24`: "Foto real entra por um registro
   * que declara a origem (moldura, cartao, tela cheia), nunca como recorte
   * flutuando." Sem default, a regra da marca e cumprida por construcao em vez de
   * por lembranca. `telaCheia` + `faixa` e recusado pelo refinador, com o numero da
   * fracao de quadro que sobraria chapada.
   */
  registro: z.enum(['moldura', 'cartao', 'telaCheia']),
  /**
   * `faixa` (contain) ou `recorte`. Nenhum e obviamente melhor, e por isso e campo.
   * Medido em 30/09/2026 nas 26 fotos da fazenda: 18 sao `Orientation 1` e exibem
   * 4032x3024 (razao 1,3333), onde `faixa` num 9:16 deixa 42,19% da altura como foto
   * e `recorte` joga fora 57,81% da foto; as outras 8 sao `Orientation 6` e exibem
   * 3024x4032 (razao 0,75), onde `faixa` da 75,00% e `recorte` joga fora 25,00%. A
   * escolha nao e a mesma decisao nos dois grupos.
   */
  enquadramento: z.union([z.strictObject({tipo: z.literal('faixa')}), zRecorte]),
  camera: zCamera,
  /**
   * Graus a girar NA COMPOSICAO, no sentido horario. Default 0.
   *
   * ACRESCENTADO EM 01/10/2026, E O MOTIVO E MEDIDO, NAO PREVISTO PELO PLANO.
   *
   * Arquivo que TEM `EXIF Orientation` nao precisa deste campo: o Chrome aplica a
   * orientacao sozinho (`image-orientation: from-image` e o default) e `sondar()` ja
   * devolve a razao de EXIBICAO. Mas os recortes de embalagem PERDERAM o metadado no
   * caminho -- medido em 01/10/2026 com o `sondar()` estendido:
   *
   *   assets/classico-250g.png -> 4096x2304 | razao 1,777778 | rotacao `nenhuma` 0
   *
   * e os packshots de origem sao `Orientation 6`. Olhado no pixel
   * (`saida/ponte-assets.png`), os tres recortes aparecem DEITADOS, com a marca de
   * lado. Como o arquivo nao carrega o dado, `sondar()` nao tem o que descobrir: ou a
   * rotacao e declarada, ou a peca sai com o pacote tombado e exit 0.
   *
   * Multiplo de 90 porque `Fonte.tsx` TROCA largura por altura em 90 e 270 -- um
   * angulo livre deixaria a caixa do registro sem relacao com a imagem girada. E
   * `razaoExibicao` continua sendo a razao DEPOIS do giro: e ela que `razaoDaPeca`
   * usa, e uma peca que declarasse a razao crua abriria faixa no eixo errado.
   */
  rotacaoGraus: z
    .union([z.literal(0), z.literal(90), z.literal(180), z.literal(270)])
    .default(0),
});

const zFonteCor = z.strictObject({
  tipo: z.literal('cor'),
  /** hex de 6 digitos. Branco puro e proibido (`proibicoes.md:13`): o refinador o recusa. */
  cor: z.string().regex(/^#[0-9a-fA-F]{6}$/),
});

/** As fontes que podem ser CELULA de grade. Grade nao entra: recursao fora. */
const zFonteSimples = z.discriminatedUnion('tipo', [zFonteVideo, zFonteFoto, zFonteCor]);
export type FonteSimples = z.infer<typeof zFonteSimples>;

const zFonteGrade = z.strictObject({
  tipo: z.literal('grade'),
  colunas: z.union([z.literal(1), z.literal(2)]),
  linhas: z.union([z.literal(1), z.literal(2)]),
  /** calha entre celulas, em px a 1080 de largura */
  calha: z.number().min(0),
  /**
   * 2 a 4 celulas de fonte SIMPLES. Grade dentro de grade e recursao que nenhuma das
   * 12 series pede, e recursao em zod obriga anotacao de tipo manual -- uma segunda
   * fonte de verdade para o mesmo tipo.
   */
  celulas: z.array(zFonteSimples).min(2).max(4),
});

export const zFonte = z.discriminatedUnion('tipo', [
  zFonteVideo,
  zFonteFoto,
  zFonteCor,
  zFonteGrade,
]);
export type Fonte = z.infer<typeof zFonte>;

export const zEventoTexto = z.strictObject({
  /**
   * `legenda` NAO esta aqui de proposito: a legenda e camada de PECA, fora da
   * `TransitionSeries`. Dentro de uma cena ela seria remontada por cena e, na janela
   * de crossfade, duas legendas com textos diferentes ficariam no ar ao mesmo tempo
   * -- bug garantido e invisivel em miniatura.
   */
  papel: z.enum(PAPEIS_DE_EVENTO),
  texto: z.string().trim().min(1),
  /** segundos, relativo ao inicio DA CENA a que o evento pertence */
  entradaS: z.number().min(0),
  /** ausente = `duracaoDaFrase(texto)`, que ja cresce com o stagger */
  duracaoS: z.number().gt(0).optional(),
  /**
   * OBRIGATORIO, sem default.
   *
   * `PISTAS_DE_EVENTO` de `motor/pista.ts`: `topo`, `principal`, `tela`. `rodape`
   * NAO esta na lista -- ela e a caixa da camada `Legenda`, e um evento ali cairia
   * sobre a fala.
   *
   * `PISTA_PADRAO[papel]` existe em `motor/evento.ts` e NAO e aplicado aqui: ele e o
   * que a skill `canastra-briefing` escreve no arquivo. Default no esquema poria a
   * escolha no codigo, onde ninguem a le.
   *
   * O ENCAIXE SAI DELA. `pista: 'tela'` -> cartela. `topo`/`principal` -> faixa ou
   * coluna, conforme a sobra ao lado do video naquele formato (`pista.ts`).
   */
  pista: z.enum(PISTAS_DE_EVENTO),
  /** indice da UNICA palavra que recebe `COR.acento`. `proibicoes.md:20`. */
  palavraAcento: z.number().int().min(0).optional(),
  // NAO existe campo `encaixe`: ele e DERIVADO de (pista, formato). Um campo que o
  // motor nao pode honrar -- `encaixe: ['coluna']` no 9:16, onde a sobra ao lado do
  // video e 0,00 px (medido) -- e o HTTP 200 que ignora o parametro.
  //
  // NAO existe `zona`, `modo`, `preset` nem `cadencia`: eram os nomes do prototipo.
  // A pista substitui a zona, o encaixe e derivado e a cadencia vem do papel
  // (`CADENCIA_DO_PAPEL`, `motor/evento.ts`).
});
export type EventoTexto = z.infer<typeof zEventoTexto>;

export const zCena = z.strictObject({
  duracaoS: z.number().gt(0),
  fonte: zFonte,
  /** lista VAZIA e cena completa sem evento -- sem erro e sem placeholder */
  eventos: z.array(zEventoTexto),
});
export type Cena = z.infer<typeof zCena>;

const zTransicao = z.discriminatedUnion('tipo', [
  /** 0 frames. E o default, e e o que faz `Sigma cenas` ser a duracao da peca. */
  z.strictObject({tipo: z.literal('corte')}),
  z.strictObject({tipo: z.literal('fade'), duracaoS: z.number().gt(0)}),
  z.strictObject({
    tipo: z.literal('wipe'),
    duracaoS: z.number().gt(0),
    direcao: z.enum(['from-left', 'from-right', 'from-top', 'from-bottom']),
  }),
]);
export type Transicao = z.infer<typeof zTransicao>;

const zLegenda = z.strictObject({
  /** nome do arquivo de transcricao, relativo a raiz do projeto */
  arquivo: z.string().min(1),
  /**
   * O relogio em que os tempos da transcricao estao. ENUM DE UM VALOR: declarar e o
   * ponto, nao escolher. `peca` saiu porque `relogio: 'peca'` mais `aparaAntesS != 0`
   * era uma contradicao que o esquema aceitava e o refinador tinha que desfazer --
   * forma que se pode escrever errada e forma errada.
   */
  relogio: z.literal('fonte'),
  /**
   * QUE INSTANTE DA TRANSCRICAO CAI NO FRAME 0 DA PECA.
   *
   * O buraco que isto fecha: com N cenas ha N valores de `Cena.fonte.aparaAntesS` e
   * UMA legenda, entao somar "o" `aparaAntesS` deixa de ser definido. Hoje o motor
   * tem sorte -- `PecaVideo.tsx:134` passa um numero so porque ha uma cena so.
   *
   * A resolucao e NEGAR a pergunta: nenhum `aparaAntesS` de cena entra no rebase,
   * porque a legenda nao e imagem, e a FALA, e a fala tem uma fonte de audio so.
   *
   *   locucao ....... = `audio.locucao.aparaAntesS`. O caso normal
   *   cena+indice ... = `cenas[indice].fonte.aparaAntesS`. O UNICO jeito de um
   *                     aparaAntesS de cena tocar a legenda, e ele e NOMINAL: quem
   *                     escreve aponta a cena com o dedo
   *   segundo ....... um valor cru, para transcricao que nao veio de nenhum dos dois
   *
   * Sem locucao e sem ancora, o refinador RECUSA -- nao escolhe a cena 0 por
   * conveniencia.
   */
  ancora: z.discriminatedUnion('tipo', [
    z.strictObject({tipo: z.literal('locucao')}),
    z.strictObject({tipo: z.literal('cena'), indice: z.number().int().min(0)}),
    z.strictObject({tipo: z.literal('segundo'), valorS: z.number().min(0)}),
  ]),
  /** quando a pista de legenda entra na PECA. default 0 */
  entradaNaPecaS: z.number().min(0).default(0),
  /** default `LEGENDA.maxPalavras`, que e 2 */
  maxPalavrasPorBloco: z.number().int().min(1).max(6).optional(),
  // NAO existe `aparaAntesS` aqui: o nome dele e `ancora`, e a razao esta acima.
});
export type LegendaDeclarada = z.infer<typeof zLegenda>;

// ---- audio: fecha a ausencia A4 ---------------------------------------------
//
// O prototipo tinha o campo certo (`audio.locucao`) e tambem `alvoLufs` e
// `picoMaximoDbtp`, que NAO entram: o alvo -14 LUFS / -1 dBTP e dos tokens e e
// aplicado POS-render por `scripts/normalizar-audio.mjs` sobre a MISTURA. Um alvo
// por faixa aqui seria uma segunda verdade que o normalizador sobrescreve sem avisar.

const zFaixa = z.strictObject({
  /** NOME dentro da subpasta, nunca um caminho */
  arquivo: z.string().min(1),
  /**
   * Ganho RELATIVO na mistura, em dB. **NAO e LUFS.**
   *
   * `scripts/normalizar-audio.mjs` roda DEPOIS do render, sobre o MP4 ja mixado, com
   * `-c:v copy`, e leva a MISTURA a `AUDIO = {lufs: -14, picoDbtp: -1}` dos tokens.
   * Logo este campo decide quanto a trilha fica ABAIXO da voz; o nivel final e do
   * normalizador.
   *
   * Ponto de partida [escolhido], sem medicao nossa que o sustente:
   * `locucao.ganhoDb = 0` e `trilha.ganhoDb = -18`. A primeira peca com as duas
   * faixas tem de medir o resultado, e o numero volta para a spec.
   */
  ganhoDb: z.number().min(-60).max(12),
  /** apara: de onde o arquivo comeca a tocar. 1,14 no `pl.wav` */
  aparaAntesS: z.number().min(0),
});
export type Faixa = z.infer<typeof zFaixa>;

const zTrilha = zFaixa.extend({
  /** SEM default: 20 s de trilha numa peca de 40 s e ou loop ou silencio na metade */
  loopar: z.boolean(),
  fadeEntradaS: z.number().min(0),
  fadeSaidaS: z.number().min(0),
});
export type Trilha = z.infer<typeof zTrilha>;

const zAudio = z.strictObject({
  /** `null` = peca sem voz. NUNCA ausente: ausencia e esquecimento, `null` e declaracao. */
  locucao: zFaixa.nullable(),
  /** `null` so e aceito COM locucao -- `refinar.ts` cobra, citando [oficial]. */
  trilha: zTrilha.nullable(),
});
export type Audio = z.infer<typeof zAudio>;

const zAsset = z.strictObject({
  /** nome dentro de `projetos/<p>/public/assets/` */
  arquivo: z.string().min(1),
  tipo: z.literal('recorte-embalagem'),
  /**
   * LITERAL `true`: recorte sem laudo nao entra.
   *
   * E O LAUDO NAO E COPIADO PARA CA. A prova de que o recorte foi aprovado e a
   * PRESENCA do arquivo em `public/assets/`, porque a unica porta de entrada daquela
   * pasta e `instagram/recorte/publicar.py:82`, que so copia o PNG cujo laudo irmao
   * traz `aprovado is True` -- fail-closed. Um humano podendo digitar
   * `aprovado: true` aqui transformaria aquele portao em decoracao.
   */
  laudoExigido: z.literal(true),
});
export type Asset = z.infer<typeof zAsset>;

// O NOME E `zBriefingEstrito`, E NAO `zBriefing`, DE PROPOSITO: `zBriefing` e o
// embrulho de `z.preprocess` que permite chave de comentario, logo abaixo.
const zBriefingEstrito = z.strictObject({
  _esquema: z.literal('canastra-briefing/1'),
  serie: z.enum(SERIES),
  /**
   * O fps da peca. CAMPO, nao constante: antes de 01/10/2026 era `FPS = 30` em
   * `Raiz.tsx:22` e nenhuma camada de texto lia `useVideoConfig`. A 60 fps tudo
   * encurtava pela metade, com exit 0 e sem aviso.
   */
  fps: z.number().int().min(1).max(120).default(30),
  formatos: z.array(z.enum(FORMATOS)).min(1),
  duracao: z.strictObject({
    /**
     * SEM DEFAULT, de proposito. `somaCenas`: as cenas mandam e `alvoS`, se houver,
     * e conferencia. `totalFixo`: `alvoS` manda e o compilador devolve os frames das
     * transicoes as cenas. Um default aqui seria escolha estetica disfarcada de
     * conveniencia -- quem pedisse 24 s receberia 22,4 s sem perceber na primeira
     * peca com crossfade.
     */
    modo: z.enum(['somaCenas', 'totalFixo']),
    alvoS: z.number().gt(0).optional(),
  }),
  cenas: z.array(zCena).min(1),
  /** exatamente `cenas.length - 1` entradas. `refinar.ts` cobra a contagem. */
  transicoes: z.array(zTransicao),
  legenda: zLegenda.optional(),
  /**
   * OBRIGATORIO. Peca de foto parada nao tem fonte com som, e Reel sem audio perde
   * elegibilidade para nao-seguidor (`05-formatos.md` §3, [oficial]). "Mudo" no
   * catalogo significa SEM LOCUCAO, nunca sem faixa -- e 5 das 12 series entregam
   * Reel a partir de foto parada (1, 2, 5, 10, 11), com a serie 4 sendo
   * explicitamente "sem voz, COM faixa".
   */
  audio: zAudio,
  licencas: zLicencas.default(LICENCAS_DESLIGADAS),
  /**
   * Os recortes de embalagem que a peca usa. `[]` e valido e e o caso comum.
   *
   * SUBSTITUI O `exigePreservacao: boolean` DA VERSAO ANTERIOR. Um booleano dizia
   * "exija preservacao" sem dizer DE QUE, e o portao ficava sem saber qual arquivo
   * conferir. A lista nomeia os arquivos, e o portao de ritmo checa que cada um
   * existe em `projetos/<p>/public/assets/`.
   *
   * `exigePreservacao` continua existindo no PLANO, derivado: `assets.length > 0`.
   */
  assets: z.array(zAsset).default([]),
  /** o que prende nos 2 primeiros segundos */
  gancho: z.string().trim().min(1),
  cta: z.string().trim().min(1),
});

/**
 * Tira as chaves de comentario de uma arvore de JSON, EM TODA PROFUNDIDADE.
 *
 * DIVERGENCIA MEDIDA DO PLANO, E A RAZAO ESTA NO PROTOTIPO.
 *
 * O plano de 01/10/2026 escreve este `preprocess` varrendo so o nivel de topo, com a
 * justificativa de que "um briefing sem comentario e um briefing que a proxima sessao
 * le errado". A justificativa e a mesma em profundidade, e la ela e mais forte: o
 * comentario mais valioso dos dois prototipos nao esta no topo. Em
 * `out/_spec-briefing/a-private-label.json` ele esta DENTRO de um evento --
 * `"_procedencia": "citacao literal de transcricao.json, palavras 11..15..."` -- e em
 * `b-jornada-foto.json` esta dentro de `audio.trilha`, dizendo que o arquivo nao
 * existe. Com a varredura so no topo, os dois prototipos reprovam no esquema estrito
 * por causa do proprio comentario que explica por que estao como estao, e a
 * procedencia de uma citacao literal perderia o lugar onde mora.
 *
 * `_esquema` e preservado porque e campo de verdade, e e por isso que remover
 * `_esquema` do arquivo continua reprovando.
 *
 * A excecao NAO afrouxa a estrita: `duracao_alvo: 24` (sem underscore INICIAL)
 * continua reprovando, em qualquer profundidade, e e isso que o teste prova.
 */
function semComentarios(cru: unknown): unknown {
  if (Array.isArray(cru)) return cru.map(semComentarios);
  if (typeof cru !== 'object' || cru === null) return cru;
  const limpo: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(cru as Record<string, unknown>)) {
    if (k.startsWith('_') && k !== '_esquema') continue;
    limpo[k] = semComentarios(v);
  }
  return limpo;
}

/** O briefing, com uma excecao a estrita: chave que comeca com `_` e COMENTARIO. */
export const zBriefing = z.preprocess(
  semComentarios,
  zBriefingEstrito,
) as unknown as typeof zBriefingEstrito;

export type Briefing = z.infer<typeof zBriefingEstrito>;
