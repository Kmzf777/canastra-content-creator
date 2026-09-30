// A CONVENCAO DA PASTA PUBLICA, num lugar so.
//
// O Remotion tem UMA pasta publica por render (`--public-dir`), e dois planos
// deste projeto reivindicaram o mesmo mecanismo: o motor de video apontava
// `--public-dir=projetos/<p>/fonte` para que `staticFile('pl.mp4')` achasse o
// video cru, e o portao de recorte (`instagram/recorte/publicar.py`) queria
// escrever em `remotion/public/assets/`, que so funcionaria se a pasta publica
// fosse a raiz do projeto Remotion. Os dois usos sao incompativeis.
//
// Resolucao: UMA pasta publica por PROJETO, com subpastas nomeadas. A pasta
// publica passa a ser `projetos/<p>/public/`, e dentro dela:
//
//   fonte/   o material cru do projeto (pl.mp4, pl.wav) -- pesado, gitignorado
//   assets/  os recortes com laudo aprovado, copiados por publicar.py
//
// e o render vira:
//
//   npx remotion render src/index.ts Reel projetos/<p>/saida/reel.mp4 \
//     --props=projetos/<p>/props.json --public-dir=projetos/<p>/public
//
// A alternativa era uma pasta publica compartilhada na raiz do motor com o
// pl.mp4 dentro; foi recusada porque material de projeto e material de projeto:
// dois projetos com um `pl.mp4` cada colidiriam no mesmo nome.
//
// As constantes existem para que o prefixo seja escrito UMA vez. `staticFile`
// recebe sempre `${SUB.fonte}/...` ou `${SUB.assets}/...`, nunca um caminho
// montado a mao no componente.

/** Nome da pasta publica dentro de cada projeto. */
export const PASTA_PUBLICA = 'public';

/** Subpastas dentro da pasta publica. Caminho de `staticFile` comeca por uma delas. */
export const SUB = {
  /** material cru do projeto: o video fonte e o wav extraido */
  fonte: 'fonte',
  /** recortes de embalagem com laudo aprovado (instagram/recorte/publicar.py) */
  assets: 'assets',
} as const;
