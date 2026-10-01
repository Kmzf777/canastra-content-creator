import {LEGENDA} from '../identidade/tokens';
import {emFrames} from '../motor/relogio';

export type Palavra = {texto: string; inicioMs: number; fimMs: number};
export type Bloco = {texto: string; inicioFrame: number; fimFrame: number};

export function agrupar(
  palavras: Palavra[],
  // `maxPalavras` e PARAMETRO com default, e nao mais uma leitura de `LEGENDA` de
  // dentro: o briefing tem `legenda.maxPalavrasPorBloco` e sem o parametro esse campo
  // nao teria como chegar aqui -- seria um campo que o motor aceita e ignora.
  {fps, maxPalavras = LEGENDA.maxPalavras}: {fps: number; maxPalavras?: number},
): Bloco[] {
  const blocos: Bloco[] = [];
  for (let i = 0; i < palavras.length; i += maxPalavras) {
    const grupo = palavras.slice(i, i + maxPalavras);
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
    // O piso de leitura vem em SEGUNDOS e e convertido com o fps que esta
    // funcao JA recebia. Antes de 01/10/2026 comparava com
    // `LEGENDA.duracaoMinFrames`, um literal de 30 fps dentro de uma funcao
    // parametrizada por fps -- a incoerencia mais barata de achar do motor.
    const pisoFrames = emFrames(LEGENDA.duracaoMinSegundos, fps);
    if (b.fimFrame - b.inicioFrame < pisoFrames) {
      b.fimFrame = b.inicioFrame + pisoFrames;
    }
    const prox = blocos[i + 1];
    if (prox && prox.inicioFrame < b.fimFrame) prox.inicioFrame = b.fimFrame;
  }
  return blocos;
}
