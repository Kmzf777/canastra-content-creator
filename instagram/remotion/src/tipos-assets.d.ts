// Declaracao dos imports de arquivo de fonte.
//
// O bundler do Remotion ja tem regra `asset/resource` para
// /\.(woff(2)?|otf|ttf|eot)(\?v=\d+\.\d+\.\d+)?$/ -- conferido em
// `node_modules/@remotion/bundler/dist/shared-bundler-config.js`, linha 122.
// Entao `import url from './fontes/Inter-Bold.ttf'` devolve a URL do arquivo ja
// emitido dentro do bundle: sem rede, e sem depender de `--public-dir`, que
// cada projeto sobrescreve para apontar a sua propria pasta `fonte/`.
//
// O TypeScript nao sabe dessa regra sozinho; esta declaracao e so para ele.

declare module '*.ttf' {
  const url: string;
  export default url;
}
declare module '*.otf' {
  const url: string;
  export default url;
}
declare module '*.woff' {
  const url: string;
  export default url;
}
declare module '*.woff2' {
  const url: string;
  export default url;
}
