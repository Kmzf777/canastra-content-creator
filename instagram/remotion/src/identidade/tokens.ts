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

// Tempos em FRAMES a 30fps. Medidos, não escolhidos.
export const TEMPO = {
  entrada: 12,          // faixa util 8-18
  saidaExpoente: 2.4,   // aceleracao de saida t^2.4
  overshoot: 0.03,      // 2-4%
  stagger: 3,           // 2-4 frames entre elementos irmaos
  holdFinal: 12,        // 8-18
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
  duracaoMinFrames: 10,        // 0,33s a 30fps
  corte: 'seco',               // 93% da massa ja no 1o frame: sem easing
  entrelinha: 0.96,
  corpoEm1080: 78,
  cor: COR.creme,
} as const;

export const AUDIO = {lufs: -14, picoDbtp: -1} as const;
