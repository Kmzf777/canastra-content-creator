// Gancho de resolucao para os scripts que importam `.ts` do projeto direto no
// Node.
//
// POR QUE ELE EXISTE
//
// O tsconfig deste projeto usa `moduleResolution: "bundler"`, entao o codigo em
// `src/` importa sem extensao (`import {LEGENDA} from '../identidade/tokens'`).
// O bundler do Remotion e o vitest resolvem isso; o resolvedor ESM cru do Node
// NAO -- ele exige o caminho exato e devolve ERR_MODULE_NOT_FOUND. Foi
// exatamente isso que quebrou `gerar-props.mjs` ao importar `agrupar.ts`, que
// importa `../identidade/tokens`.
//
// A alternativa seria escrever `.ts` nas importacoes de `src/`, o que exigiria
// `allowImportingTsExtensions` e mudaria a convencao do codigo que RENDERIZA por
// conveniencia de um script. O gancho fica aqui, no lado do script.
//
// Ele so age no fracasso: tenta a resolucao normal primeiro e, se ela falhar,
// tenta `<especificador>.ts` e depois `<especificador>/index.ts`, apenas para
// caminho relativo. Pacote de node_modules segue a resolucao normal do Node --
// nunca mascaramos dependencia faltando.
//
//   import {register} from 'node:module';
//   register('./_resolver-ts.mjs', import.meta.url);

export async function resolve(especificador, contexto, proximo) {
  try {
    return await proximo(especificador, contexto);
  } catch (erro) {
    const relativo = especificador.startsWith('./') || especificador.startsWith('../');
    if (!relativo) throw erro;
    for (const sufixo of ['.ts', '.tsx', '/index.ts', '/index.tsx']) {
      try {
        return await proximo(especificador + sufixo, contexto);
      } catch {
        // tenta o proximo sufixo
      }
    }
    throw erro;
  }
}
