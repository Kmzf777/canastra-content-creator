// Passo de audio do pipeline: leva o MP4 entregue a -14 LUFS / -1 dBTP.
//
//   node scripts/normalizar-audio.mjs
//   node scripts/normalizar-audio.mjs --projeto=projetos/01-private-label
//   node scripts/normalizar-audio.mjs --arquivo=projetos/01-private-label/saida/reel.mp4
//   node scripts/normalizar-audio.mjs --medir            (so mede, nao escreve)
//
// RODA DEPOIS DO RENDER E ANTES DOS PORTOES. O video e copiado com `-c:v copy`,
// entao nenhum pixel muda e nenhum portao e invalidado -- mas o arquivo que os
// portoes conferem passa a ser o que vai ao ar de verdade, ja com o audio certo.
//
// Se o render for refeito, este passo tem que rodar de novo: o MP4 novo sai com
// o audio cru outra vez. Ele e idempotente, entao rodar duas vezes no mesmo
// arquivo nao reencoda a segunda.
//
// POR QUE ESTE SCRIPT SE RELANCA: identico ao `conferir.mjs`. O modulo de audio
// e TypeScript e o Node so o carrega com `--experimental-strip-types`, que nao
// da para ligar de dentro do processo ja rodando.
//
// E o motivo de o ALVO ser lido AQUI e nao la dentro: `normalizar.ts` roda sob
// type stripping, que nao resolve import local sem extensao. Entao quem le
// `AUDIO` de `identidade/tokens.ts` e este script, que passa o valor adiante.
// Ver o cabecalho de `src/verificacao/folha.ts`.

import {spawn} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const FLAG = '--experimental-strip-types';

if (!process.execArgv.includes(FLAG)) {
  const filho = spawn(
    process.execPath,
    [FLAG, '--no-warnings', fileURLToPath(import.meta.url), ...process.argv.slice(2)],
    {stdio: 'inherit'},
  );
  filho.on('close', (codigo) => process.exit(codigo ?? 1));
  filho.on('error', (e) => {
    console.error(`nao consegui me relancar com ${FLAG}: ${e.message}`);
    process.exit(1);
  });
} else {
  try {
    await principal();
  } catch (e) {
    console.error(`\nFALHA  ${e.message}`);
    if (process.env.CANASTRA_PILHA) console.error(e);
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------

function argumentos() {
  const a = {projeto: 'projetos/01-private-label', arquivo: '', medir: false};
  for (const cru of process.argv.slice(2)) {
    if (cru === '--medir') {
      a.medir = true;
      continue;
    }
    const m = /^--([a-zA-Z]+)=(.*)$/.exec(cru);
    if (!m) throw new Error(`argumento nao entendido: ${cru}. Use --chave=valor ou --medir.`);
    const [, chave, valor] = m;
    if (!(chave in a)) {
      throw new Error(`--${chave} nao existe. Validos: projeto, arquivo, medir.`);
    }
    a[chave] = valor;
  }
  return a;
}

// DECLARACAO de funcao, nao `const`: este arquivo tem `await principal()` no
// topo, e uma `const` declarada depois dele ainda esta na zona morta quando
// `principal` roda. Custou uma rodada: "Cannot access 'n' before
// initialization". `function` sobe, `const` nao.
function sinal(v) {
  return v >= 0 ? `+${v.toFixed(2)}` : v.toFixed(2);
}

async function principal() {
  const a = argumentos();

  const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  process.chdir(raiz);

  const {AUDIO} = await import('../src/identidade/tokens.ts');
  const {medir, normalizar} = await import('../src/motor/audio/normalizar.ts');

  const alvo = {lufs: AUDIO.lufs, picoDbtp: AUDIO.picoDbtp};

  const arquivos = a.arquivo
    ? [a.arquivo]
    : ['reel.mp4', 'feed.mp4'].map((f) => path.join(a.projeto, 'saida', f));

  const existentes = arquivos.filter((f) => fs.existsSync(f));
  if (existentes.length === 0) {
    throw new Error(
      `nenhum dos arquivos existe: ${arquivos.join(', ')}. Renderize antes ` +
        '(passo 6 do pipeline).',
    );
  }
  for (const f of arquivos) {
    if (!existentes.includes(f)) console.log(`  (pulando, nao existe: ${f})`);
  }

  console.log(`\n== alvo (identidade/tokens.ts AUDIO) ==`);
  console.log(`  ${alvo.lufs} LUFS integrado · teto ${alvo.picoDbtp} dBTP`);

  for (const arquivo of existentes) {
    console.log(`\n== ${arquivo} ==`);

    if (a.medir) {
      const m = await medir(arquivo);
      console.log(
        `  integrado ${sinal(m.i)} LUFS · pico real ${sinal(m.tp)} dBTP · faixa ` +
          `${m.lra.toFixed(2)} LU`,
      );
      console.log(
        `  distancia do alvo: ${sinal(alvo.lufs - m.i)} LU`,
      );
      continue;
    }

    const r = await normalizar({entrada: arquivo, saida: arquivo, alvo});
    console.log(
      `  audio    ${r.audio.codec} ${r.audio.taxa} Hz ${r.audio.canais} canais`,
    );
    console.log(
      `  antes    ${sinal(r.antes.i)} LUFS · ${sinal(r.antes.tp)} dBTP · faixa ` +
        `${r.antes.lra.toFixed(2)} LU`,
    );
    if (r.pulou) {
      console.log(`  ja estava no alvo: nao reencodei (evita perda de geracao).`);
      continue;
    }
    for (const p of r.passos) {
      console.log(
        `  it. ${p.iteracao}    ${sinal(p.antes.i)} -> ${sinal(p.depois.i)} LUFS · ` +
          `${sinal(p.depois.tp)} dBTP · ${p.tipo}`,
      );
    }
    console.log(
      `  depois   ${sinal(r.depois.i)} LUFS · ${sinal(r.depois.tp)} dBTP · faixa ` +
        `${r.depois.lra.toFixed(2)} LU   <- medido no MP4 escrito`,
    );
    console.log(`  ganho    ${sinal(r.ganhoLu)} LU · modo loudnorm: ${r.tipo}`);
    if (r.tipo !== 'linear') {
      console.log(
        `  ATENCAO: modo ${r.tipo}, nao linear -- o ganho necessario nao cabia ` +
          'sob o teto de pico, entao houve limitacao. Ouca a peca.',
      );
    }
  }

  console.log(
    '\naudio OK. Lembre: se o render for refeito, rode isto outra vez.\n',
  );
}
