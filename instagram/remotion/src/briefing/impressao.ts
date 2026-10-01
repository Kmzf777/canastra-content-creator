// A IMPRESSAO DIGITAL DO BRIEFING. Node-only: importa `node:crypto`.
//
// POR QUE ESTE ARQUIVO EXISTE E NAO E `compilar.ts`
//
// A spec §2.4 declara `compilar.ts` PURO, e `node:crypto` o tornaria Node-only.
// `Raiz.tsx`, `Peca.tsx` e `Cena.tsx` importarao `compilar.ts` apenas com
// `import type`, que o transpilador apaga -- entao o bundle do Chrome nunca ve o
// `require`. A primeira importacao de VALOR a partir de um `.tsx` derrubaria o
// render, e ninguem lembraria por que. Separando, o compilador continua podendo
// entrar no bundle e este arquivo nunca entra: quem o importa e
// `scripts/compilar.mjs`, que SELA, e `verificacao/selo.ts`, que CONFERE -- os dois de
// Node.
//
// Ate 30/09/2026 esta linha dizia `verificacao/ritmo.ts`, e esse arquivo nunca existiu:
// o selo era escrito em todo compile e lido por ninguem. Ver o cabecalho de
// `src/verificacao/selo.ts`.

import {createHash} from 'node:crypto';

/**
 * Serializacao CANONICA: mesma estrutura -> mesma string, em qualquer ordem de chave.
 *
 * POR QUE NAO `JSON.stringify(valor, Object.keys(valor).sort())`
 *
 * Porque o segundo argumento do `JSON.stringify` NAO e uma ordem de chaves: e uma
 * ALLOWLIST, e ela e aplicada RECURSIVAMENTE a todo objeto da estrutura. Com as
 * chaves de topo apenas, `cenas` sai como `[{}]` e `duracao` como `{}` -- o hash
 * ignora cenas, eventos, fontes, duracoes e transicoes. Medido: dois briefings com
 * duracoes e textos completamente diferentes davam o MESMO hash. E como o
 * `_sha256Briefing` era a unica protecao do plano contra plano fora de sincronia com o
 * briefing, a protecao central era um no-op.
 *
 * O que esta funcao garante, e cada item fecha um jeito de dois valores diferentes
 * virarem a mesma string:
 *
 *   - chaves ordenadas em TODA profundidade, nao so no topo;
 *   - array e objeto tem delimitadores diferentes, entao `[1,2]` nao colide com
 *     `{0:1,1:2}`;
 *   - a string carrega o proprio comprimento, entao a virgula dentro de um texto nao
 *     se confunde com a virgula que separa dois itens;
 *   - `undefined` e representado, em vez de a chave desaparecer;
 *   - `null` nao vira `0`;
 *   - numero nao finito LANCA, em vez de virar `null` como no `JSON.stringify` --
 *     senao `NaN` e `null` teriam o mesmo hash.
 */
export function canonico(valor: unknown): string {
  if (valor === undefined) return 'u';
  if (valor === null) return 'z';
  if (typeof valor === 'number') {
    if (!Number.isFinite(valor)) {
      throw new Error(`canonico: numero nao finito (${valor}) nao tem forma estavel`);
    }
    return `n:${valor}`;
  }
  if (typeof valor === 'boolean') return valor ? 'b:1' : 'b:0';
  if (typeof valor === 'string') return `s:${valor.length}:${valor}`;
  if (Array.isArray(valor)) {
    return `a[${valor.map(canonico).join(',')}]`;
  }
  if (typeof valor === 'object') {
    const chaves = Object.keys(valor as object).sort();
    const partes = chaves.map(
      (k) => `${k.length}:${k}=${canonico((valor as Record<string, unknown>)[k])}`,
    );
    return `o{${partes.join(',')}}`;
  }
  throw new Error(
    `canonico: nao sei serializar ${typeof valor}. Briefing e plano sao JSON: se ` +
      'apareceu function, symbol ou bigint aqui, alguem passou um objeto vivo em vez ' +
      'de dado lido de arquivo.',
  );
}

/** O sha256 da forma canonica. Mesma estrutura -> mesmo hash, sempre. */
export function sha256Do(valor: unknown): string {
  return createHash('sha256').update(canonico(valor), 'utf8').digest('hex');
}

/**
 * O hash do CONTEUDO do plano, com o campo que guarda esse hash removido.
 *
 * POR QUE O SELO DO BRIEFING NAO BASTA, MEDIDO EM 01/10/2026
 *
 * Um cetico gravou `duracaoFrames: 9999` (era 345) em `projetos/03-prova-cena/plano.json`
 * deixando `_sha256Briefing` intacto e o portao 0 respondeu `OK -- o plano veio deste
 * briefing`, EXIT=0. Estava certo e era inutil: o plano de fato nasceu daquele briefing,
 * e o numero que o `Raiz.tsx` le por `calculateMetadata` tinha sido trocado a mao. O
 * hash do briefing responde "de onde este plano veio"; so o hash do plano responde "este
 * plano ainda e o que saiu de la".
 *
 * DUAS DECISOES QUE PARECEM DETALHE E NAO SAO
 *
 * 1. `_sha256Plano` sai do objeto antes de hashear, e so ele. `_sha256Briefing` FICA
 *    dentro do hash de proposito: assim trocar o selo do briefing a mao quebra os dois
 *    selos, em vez de deixar um atacante mover um e recalcular o outro de graca.
 *
 * 2. O hash e tirado do VAI-E-VOLTA por JSON, nao do objeto vivo. `JSON.stringify`
 *    APAGA chave com valor `undefined` e `canonico` a representa como `'u'` -- entao um
 *    campo opcional `undefined` em memoria daria um hash que o arquivo escrito nunca
 *    reproduz, e todo plano legitimo reprovaria. Hoje nenhum dos tres planos do
 *    repositorio tem `undefined` (medido: `hash(memoria) === hash(vai-e-volta) ===
 *    hash(disco)` nos tres), mas a garantia nao pode depender disso continuar verdade no
 *    proximo campo opcional. O que se hasheia e o que vai para o disco.
 */
export function sha256DoPlano(plano: object): string {
  const {_sha256Plano: _ignorado, ...resto} = plano as Record<string, unknown>;
  return sha256Do(JSON.parse(JSON.stringify(resto)));
}

/**
 * Sela o plano DUAS VEZES: com o hash do briefing que o gerou e com o hash do proprio
 * conteudo. Ver `sha256DoPlano` para por que o primeiro selo sozinho nao protegia nada.
 *
 * A ORDEM IMPORTA: `_sha256Briefing` entra primeiro e `sha256DoPlano` o inclui.
 *
 * SEPARADO DE `compilar()` de proposito: `compilar()` e puro e devolve os dois campos
 * vazios. Quem sela e quem escreve o arquivo (`scripts/compilar.mjs`), porque selar e um
 * ato de ESCRITA -- e um plano em memoria, dentro de um teste, nao precisa de selo.
 *
 * O CUSTO, ASSUMIDO: toda edicao legitima do `plano.json` passa a exigir recompilar.
 * Isso esta certo -- `plano.json` e artefato gerado, nao arquivo de trabalho; a unica
 * edicao legitima dele e a que `scripts/compilar.mjs` faz.
 */
export function selarPlano<T extends {_sha256Briefing: string}>(
  plano: T,
  briefing: unknown,
): T & {_sha256Plano: string} {
  const comBriefing = {...plano, _sha256Briefing: sha256Do(briefing), _sha256Plano: ''};
  return {...comBriefing, _sha256Plano: sha256DoPlano(comBriefing)};
}
