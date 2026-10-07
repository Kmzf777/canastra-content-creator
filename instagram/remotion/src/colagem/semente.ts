// Aleatoriedade COM SEMENTE para a colagem.
//
// O portao 3 (determinismo) reprova `Math.random`: o mesmo quadro renderizado
// duas vezes tem que dar o mesmo md5. Toda variacao "organica" da colagem --
// rotacao de entrada, boil de borda, tremor de carimbo -- sai daqui, semeada pelo
// NOME da peca. Mesma peca, mesmo tremor, em qualquer render.
//
// FNV-1a transforma a chave em 32 bits; mulberry32 gera a sequencia.

export function semente(chave: string): () => number {
  let h = 2166136261;
  for (const c of chave) h = Math.imul(h ^ c.charCodeAt(0), 16777619);
  let a = h >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Um numero so, em [min, max), para a chave dada. */
export function sorteio(chave: string, min: number, max: number): number {
  return min + semente(chave)() * (max - min);
}
