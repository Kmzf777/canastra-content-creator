export const COR = {
  terra:   '#3B2A1F',   // terra vermelha da Canastra, escurecida
  creme:   '#F1ECE0',   // o creme do rótulo
  verde:   '#4A5D3A',   // folha de café
  acento:  '#C8661E',   // cereja madura — UM acento por cena
  preto:   '#14100D',
} as const;

export const TIPO = {
  manchete:  {familia: 'Archivo Black', peso: 400},
  corpo:     {familia: 'Inter', peso: 700},
  dado:      {familia: 'IBM Plex Mono', peso: 500},
} as const;

// Tempos em SEGUNDOS. Medidos, nao escolhidos -- e a conversao para frame e
// `emFrames(s, fps)` de `motor/relogio.ts`, uma vez, em `motor/cadencia.ts`.
//
// POR QUE SEGUNDOS, DEPOIS DE TER SIDO FRAMES
//
// Ate 01/10/2026 estes numeros eram frames medidos a 30 fps, e nenhuma camada de
// texto chamava `useVideoConfig`. A 60 fps cada entrada, saida, hold e stagger
// duraria METADE do medido e a peca sairia inteira, com exit 0 e sem aviso.
//
// Os segundos abaixo foram obtidos dividindo os frames medidos por 30, e
// `tests/cadencia.test.ts` prova que `cadencia(30)` devolve exatamente os frames
// de antes: 12 / 3 / 12, com DURACAO_MINIMA 36. A migracao nao muda a peca a
// 30 fps -- so passa a estar certa nos outros.
export const TEMPO = {
  entradaS: 0.4,        // eram 12 frames; faixa util 8-18 frames a 30 fps
  saidaExpoente: 2.4,   // aceleracao de saida t^2.4 -- adimensional, nao escala
  overshoot: 0.03,      // 2-4% -- adimensional, nao escala
  staggerS: 0.1,        // eram 3 frames; faixa util 2-4 frames a 30 fps
  holdFinalS: 0.4,      // eram 12 frames; faixa 8-18
  pousoEasing: 'cubic-bezier(0.20,0.80,0.20,1.00)',
} as const;

// Push de camera: 100% -> 103..106% ao longo da cena. Nunca impacto.
export const PUSH = {de: 1.0, para: 1.04} as const;

// Sombra por material. Nunca a mesma sombra em duas camadas.
export const SOMBRA = {
  papel:       {dy: 6,  blur: 14, op: 0.15},
  cartao:      {dy: 11, blur: 24, op: 0.17},
  objetoAlto:  {dy: 20, blur: 32, op: 0.20},
  sobreVideo:  {dy: 14, blur: 26, op: 0.42},
} as const;

// Legenda, medida em referencia real: 2,45 blocos/s, 1,7 palavras/bloco.
export const LEGENDA = {
  maxPalavras: 2,
  // Piso de leitura de um bloco, em SEGUNDOS. Era `duracaoMinFrames: 10`, um
  // literal de 30 fps aplicado DENTRO de uma funcao que ja recebia fps
  // (`agrupar.ts:20`). 0,333 s = 10 frames a 30, 8 a 24, 20 a 60.
  duracaoMinSegundos: 0.333,
  corte: 'seco',               // 93% da massa ja no 1o frame: sem easing
  entrelinha: 0.96,
  corpoEm1080: 78,
  cor: COR.creme,
} as const;

export const AUDIO = {lufs: -14, picoDbtp: -1} as const;
