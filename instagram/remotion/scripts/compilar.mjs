// CLI: `briefing.json` -> `plano.json`.
//
// O compilador e PURO e nao le arquivo. Este script e a casca de I/O dele: le o
// briefing do disco, le a transcricao se o briefing declarar legenda, chama
// `compilar()` e SELA o resultado com o sha256 do briefing que o produziu.
//
//   node --import ./scripts/_registrar-ts.mjs scripts/compilar.mjs --projeto=projetos/<p>
//
// O gancho de resolucao e obrigatorio: `moduleResolution: bundler` deixa `src/` importar
// sem extensao, e o resolvedor ESM cru do Node devolve ERR_MODULE_NOT_FOUND. Ver
// `scripts/_resolver-ts.mjs`.
//
// POR QUE ELE SELA DUAS VEZES
//
// `plano.json` e artefato gerado e vai para `--props` do render. Um plano editado a mao
// renderiza sem reclamar -- e a licao 3 do CLAUDE.md: exit 0 com o resultado errado.
//
//   `_sha256Briefing` ... permite o portao dizer "este plano nao veio deste briefing"
//   `_sha256Plano` ...... permite o portao dizer "este plano foi editado depois"
//
// O segundo foi acrescentado em 01/10/2026: com o primeiro sozinho, trocar
// `duracaoFrames` a mao e preservar o campo do briefing passava pelo portao com EXIT=0.
// Ver o cabecalho de `src/verificacao/selo.ts`.
//
// QUEM LE O SELO DE VOLTA
//
//   node scripts/conferir.mjs --portao=selo --projeto=<dir>
//
// `src/verificacao/selo.ts`, o portao 0. Ate 30/09/2026 esse leitor nao existia: este
// script selava todo plano e nada no repositorio comparava, enquanto tres comentarios
// afirmavam que um "portao de ritmo" reprovava hash divergente. Selar sem conferir e
// cerimonia, nao protecao -- se o portao 0 desaparecer, esta chamada volta a ser enfeite.
//
// O SELO COBRE O BRIEFING PARSEADO, NAO O ARQUIVO
//
// Abaixo o hash e tirado de `briefing`, a saida do `zBriefing.parse`, nao de `cru`. A
// consequencia pratica: campo que o esquema DESCARTA nao entra no selo -- `_leia` e
// `_bloqueio_*` sao comentario, entao editar a documentacao do briefing nao invalida o
// plano. Medido em 30/09/2026. Quem conferir tem que parsear do mesmo jeito.

import {readFileSync, writeFileSync} from 'node:fs';
import path from 'node:path';
import {compilar} from '../src/briefing/compilar.ts';
import {zBriefing} from '../src/briefing/esquema.ts';
import {selarPlano} from '../src/briefing/impressao.ts';

const arg = (nome) => {
  const p = process.argv.find((a) => a.startsWith(`--${nome}=`));
  return p ? p.slice(nome.length + 3) : undefined;
};

const projeto = arg('projeto');
if (!projeto) {
  console.error('uso: scripts/compilar.mjs --projeto=projetos/<dir>');
  process.exit(2);
}

const caminhoBriefing = path.join(projeto, 'briefing.json');
const cru = JSON.parse(readFileSync(caminhoBriefing, 'utf8'));

// zod PRIMEIRO. Um briefing com `duracao_alvo: 24` em vez de `duracao.alvoS`
// renderizaria 3 segundos e sairia com exit 0 -- e por isso todo objeto e estrito.
const briefing = zBriefing.parse(cru);

// A transcricao so e lida se o briefing DECLARAR legenda. Ler sempre obrigaria todo
// projeto de foto parada a ter um arquivo de fala que ele nao tem.
let palavras;
if (briefing.legenda) {
  const t = JSON.parse(readFileSync(path.join(projeto, briefing.legenda.arquivo), 'utf8'));
  palavras = Array.isArray(t) ? t : t.palavras;
  if (!Array.isArray(palavras)) {
    throw new Error(
      `${briefing.legenda.arquivo} nao tem uma lista de palavras: esperava um array ou ` +
        'um objeto com a chave `palavras`.',
    );
  }
}

const plano = selarPlano(compilar(briefing, {palavras}), briefing);

const saida = path.join(projeto, 'plano.json');
writeFileSync(saida, `${JSON.stringify(plano, null, 2)}\n`, 'utf8');

console.log(`plano escrito em ${saida}`);
console.log(`  serie ................ ${plano.serie}`);
console.log(`  fps .................. ${plano.fps}`);
console.log(`  duracao .............. ${plano.duracaoFrames} frames ` +
  `(${(plano.duracaoFrames / plano.fps).toFixed(3)} s)`);
console.log(`  razao da peca ........ ${plano.razaoDaPeca ?? 'a do quadro'}`);
console.log(`  cenas ................ ${plano.cenas.length}`);
for (const [i, c] of plano.cenas.entries()) {
  console.log(
    `    [${i}] ${c.fonte.tipo.padEnd(6)} ${String(c.duracaoFrames).padStart(4)} frames, ` +
      `inicio na peca ${String(c.inicioNaPecaFrames).padStart(4)}, ` +
      `${c.eventos.length} evento(s)`,
  );
}
console.log(`  legenda .............. ${plano.legenda ? `${plano.legenda.blocos.length} blocos` : 'nenhuma'}`);
if (plano.legenda) {
  console.log(`    deslocamento ....... ${plano.legenda.deslocamentoFrames} frames`);
  console.log(`    grudados em zero ... ${plano.legenda.grudadosEmZero} (maior recuo ${plano.legenda.maiorRecuoFrames})`);
  console.log(`    descartados ........ ${plano.legenda.descartadosAntesDoInicio} antes, ${plano.legenda.descartadosDepoisDoFim} depois`);
}
console.log('  diagnostico de encaixe:');
for (const d of plano.diagnostico.eventos) {
  for (const [formato, f] of Object.entries(d.porFormato)) {
    console.log(`    cena ${d.cena} ev ${d.indice} [${formato}] ${f.porque}`);
  }
}
if (plano.diagnostico.licencasLigadas.length > 0) {
  console.log(`  LICENCAS LIGADAS ..... ${plano.diagnostico.licencasLigadas.join(', ')}`);
}
