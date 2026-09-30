import {LEGENDA} from '../identidade/tokens';

export type Palavra = {texto: string; inicioMs: number; fimMs: number};
export type Bloco = {texto: string; inicioFrame: number; fimFrame: number};

export function agrupar(palavras: Palavra[], {fps}: {fps: number}): Bloco[] {
  const blocos: Bloco[] = [];
  for (let i = 0; i < palavras.length; i += LEGENDA.maxPalavras) {
    const grupo = palavras.slice(i, i + LEGENDA.maxPalavras);
    blocos.push({
      texto: grupo.map(p => p.texto).join(' '),
      inicioFrame: Math.round((grupo[0].inicioMs / 1000) * fps),
      fimFrame: Math.round((grupo[grupo.length - 1].fimMs / 1000) * fps),
    });
  }
  // garante duracao minima empurrando o fim, e resolve a sobreposicao que
  // isso cria empurrando o inicio do proximo
  for (let i = 0; i < blocos.length; i++) {
    const b = blocos[i];
    if (b.fimFrame - b.inicioFrame < LEGENDA.duracaoMinFrames) {
      b.fimFrame = b.inicioFrame + LEGENDA.duracaoMinFrames;
    }
    const prox = blocos[i + 1];
    if (prox && prox.inicioFrame < b.fimFrame) prox.inicioFrame = b.fimFrame;
  }
  return blocos;
}
