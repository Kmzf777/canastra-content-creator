// O RELOGIO. A unica conversao segundo <-> frame do motor.
//
// POR QUE UM ARQUIVO SO PARA DUAS CONTAS
//
// Antes de 01/10/2026 a conversao estava escrita em quatro lugares diferentes,
// cada um com o seu `Math.round(x * 30)`: `Raiz.tsx:25` e `:28`,
// `scripts/gerar-props.mjs`, e `agrupar.ts` recebia `fps` mas comparava contra
// `LEGENDA.duracaoMinFrames`, que e um literal de 30 fps. O 30 aparecia como
// numero em uns e como parametro em outros, e ninguem conseguia dizer de fora
// quais partes da peca respeitavam o fps da composicao.
//
// Com uma funcao so, a resposta e mecanica: respeita quem chama daqui.
//
// ARREDONDA, NAO TRUNCA. Truncar erra sempre para baixo, e o erro ACUMULA por
// cena: uma peca de 12 cenas sairia sistematicamente mais curta que o briefing.
// Arredondar erra para os dois lados e o erro nao se soma.
//
// FALHA ALTA EM VEZ DE NaN. `Math.round(x * undefined)` devolve NaN, e NaN
// atravessa `durationInFrames` sem reclamar ate o render sair vazio com exit 0 --
// a licao 3 do CLAUDE.md aplicada ao tempo. Entao aqui se lanca.

/** Converte segundos em frames inteiros, no fps dado. */
export function emFrames(segundos: number, fps: number): number {
  exigirFps(fps);
  if (!Number.isFinite(segundos)) {
    throw new Error(`emFrames: segundos tem que ser finito, recebi ${segundos}`);
  }
  if (segundos < 0) {
    throw new Error(
      `emFrames: segundo negativo (${segundos}). Tempo de briefing e contado do ` +
        'inicio DA CENA, entao nao existe evento antes do frame 0 dela.',
    );
  }
  return Math.round(segundos * fps);
}

/** A volta: quantos segundos sao `frames` frames no fps dado. */
export function emSegundos(frames: number, fps: number): number {
  exigirFps(fps);
  if (!Number.isFinite(frames)) {
    throw new Error(`emSegundos: frames tem que ser finito, recebi ${frames}`);
  }
  return frames / fps;
}

function exigirFps(fps: number): void {
  if (!Number.isFinite(fps)) {
    throw new Error(`fps tem que ser finito, recebi ${fps}`);
  }
  if (!Number.isInteger(fps)) {
    throw new Error(
      `fps tem que ser inteiro, recebi ${fps}. O container de video mente: ` +
        '`pl.mp4` declara 29,96 fps de media e o Remotion renderiza num fps ' +
        'INTEIRO declarado na composicao. Sonde a fonte para saber o que ela e, ' +
        'mas renderize num inteiro.',
    );
  }
  if (fps <= 0) {
    throw new Error(`fps tem que ser > 0, recebi ${fps}`);
  }
}
