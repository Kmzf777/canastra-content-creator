// Os quatro portoes de verificacao, em ordem, num comando.
//
//   node scripts/conferir.mjs
//   node scripts/conferir.mjs --projeto=projetos/01-private-label --composicao=Reel
//   node scripts/conferir.mjs --portao=determinismo
//
// Nada aqui aprova a peca. Os portoes 1 e 4 (folha de contato e emenda de loop)
// produzem material para o OLHO -- eles falham se o ffmpeg falhar, nao se a peca
// estiver feia. Os portoes 2 e 3 (telefone e determinismo) tem veredito
// programatico. Sair com codigo 0 significa "os arquivos de conferencia estao
// prontos e as duas checagens duras passaram", nunca "pode publicar".
//
// POR QUE ESTE SCRIPT SE RELANCA
//
// Os portoes sao TypeScript. O Node 22.16 sabe carregar `.ts` mas so com
// `--experimental-strip-types`, que nao da para ligar de dentro do processo ja
// rodando. Entao o script confere se a flag esta ligada e, se nao, se relanca com
// ela e repassa o codigo de saida. Isso mantem o comando `node
// scripts/conferir.mjs` funcionando puro, sem npm script e sem NODE_OPTIONS.
//
// Os imports sao DINAMICOS de proposito: import estatico e resolvido antes da
// primeira linha executar, e o processo pai morreria de
// ERR_UNKNOWN_FILE_EXTENSION antes de chegar ao relancamento.

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
    await conferir();
  } catch (e) {
    // Mensagem antes da pilha: quem roda o portao quer saber o que reprovou,
    // nao em que linha do orquestrador.
    console.error(`\nFALHA  ${e.message}`);
    if (process.env.CANASTRA_PILHA) console.error(e);
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------

function argumentos() {
  const a = {
    projeto: 'projetos/01-private-label',
    composicao: 'Reel',
    entrada: 'src/index.ts',
    frame: 300,
    portao: 'todos',
    larguraTelefone: 360,
  };
  for (const cru of process.argv.slice(2)) {
    const m = /^--([a-zA-Z]+)=(.*)$/.exec(cru);
    if (!m) throw new Error(`argumento nao entendido: ${cru}. Use --chave=valor.`);
    const [, chave, valor] = m;
    if (!(chave in a)) {
      throw new Error(
        `--${chave} nao existe. Validos: ${Object.keys(a).join(', ')}.`,
      );
    }
    a[chave] = typeof a[chave] === 'number' ? Number(valor) : valor;
  }
  const validos = ['todos', 'folha', 'telefone', 'determinismo', 'loop'];
  if (!validos.includes(a.portao)) {
    throw new Error(`--portao=${a.portao} nao existe. Validos: ${validos.join(', ')}.`);
  }
  if (!Number.isInteger(a.frame) || a.frame < 0) {
    throw new Error(`--frame=${a.frame} tem que ser inteiro >= 0`);
  }
  return a;
}

function mb(bytes) {
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

async function conferir() {
  const a = argumentos();

  // A raiz do projeto Remotion, independente de onde o comando foi digitado --
  // o CLI do Remotion resolve `src/index.ts` e `--public-dir` relativos ao cwd.
  const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  process.chdir(raiz);

  const {sondar} = await import('../src/motor/sondar.ts');
  const {folhaDeContato, emendaDeLoop} = await import('../src/verificacao/folha.ts');
  const {renderizarTelefone, renderizarStill} = await import(
    '../src/verificacao/telefone.ts'
  );
  const {conferirDeterminismo} = await import('../src/verificacao/determinismo.ts');

  const saida = path.join(a.projeto, 'saida');
  const props = path.join(a.projeto, 'props.json');
  // A pasta publica e a do PROJETO, com `fonte/` e `assets/` dentro dela.
  // Ver src/motor/pasta-publica.ts: o Remotion tem uma so, e ela precisava
  // servir o video cru E os recortes de embalagem ao mesmo tempo.
  const publicDir = path.join(a.projeto, 'public');
  const video = path.join(saida, `${a.composicao.toLowerCase()}.mp4`);

  for (const [rotulo, p] of [
    ['a peca renderizada', video],
    ['o props.json', props],
    ['a pasta publica', publicDir],
  ]) {
    if (!fs.existsSync(p)) {
      throw new Error(
        `${rotulo} nao existe: ${p}. Rode a Tarefa 7 (render dos dois ` +
          'formatos) antes dos portoes.',
      );
    }
  }

  const roda = (nome) => a.portao === 'todos' || a.portao === nome;
  const falhas = [];

  const fonte = await sondar(video);
  console.log(`\n== peca ==`);
  console.log(`  ${video}`);
  console.log(
    `  ${fonte.largura}x${fonte.altura} · ${fonte.duracao.toFixed(2)}s · ` +
      `${fonte.fps.toFixed(2)} fps · ${mb(fs.statSync(video).size)}`,
  );

  // -------------------------------------------------------------- portao 1
  if (roda('folha')) {
    console.log(`\n== portao 1: folha de contato ==`);
    const f = await folhaDeContato({
      video,
      saida: path.join(saida, 'contato.png'),
      duracaoS: fonte.duracao,
    });
    console.log(
      `  ${f.saida}\n  ${f.grade.colunas}x${f.grade.linhas} celulas de ` +
        `${f.celula.largura}x${f.celula.altura} · ${f.grade.quadros} quadros a ` +
        `2/s · mosaico ${f.mosaico.largura}x${f.mosaico.altura}`,
    );
    console.log(`  ABRA E OLHE. Este portao nao tem veredito automatico.`);
  }

  // -------------------------------------------------------------- portao 2
  if (roda('telefone')) {
    console.log(`\n== portao 2: teste de telefone (${a.larguraTelefone} px) ==`);
    const t = await renderizarTelefone({
      entrada: a.entrada,
      composicao: a.composicao,
      saida: path.join(saida, 'telefone.mp4'),
      props,
      publicDir,
      larguraBase: fonte.largura,
      alturaBase: fonte.altura,
      larguraAlvo: a.larguraTelefone,
      medir: sondar,
    });
    console.log(
      `  escala ${t.escala} -> previsto ${t.largura}x${t.altura} · medido ` +
        `${t.medido.largura}x${t.medido.altura} · ${t.confere ? 'CONFERE' : 'DIVERGE'}`,
    );
    if (!t.confere) {
      falhas.push(
        `telefone: pedi ${t.largura}x${t.altura} e o arquivo saiu ` +
          `${t.medido.largura}x${t.medido.altura}`,
      );
    }
    console.log(`  ${t.saida}\n  ABRA E LEIA A LEGENDA. Se nao se le aqui, nao se le no feed.`);
  }

  // -------------------------------------------------------------- portao 3
  if (roda('determinismo')) {
    console.log(`\n== portao 3: determinismo (frame ${a.frame}) ==`);
    const d = await conferirDeterminismo({
      frame: a.frame,
      a: path.join(saida, `f${a.frame}a.png`),
      b: path.join(saida, `f${a.frame}b.png`),
      renderStill: (arquivo, frame) =>
        renderizarStill({
          entrada: a.entrada,
          composicao: a.composicao,
          saida: arquivo,
          props,
          publicDir,
          frame,
        }),
    });
    console.log(`  A ${d.hashA}  (${d.bytes.a} bytes)`);
    console.log(`  B ${d.hashB}  (${d.bytes.b} bytes)`);
    console.log(`  ${d.igual ? 'OK — deterministico' : 'NAO DETERMINISTICO'}`);
    if (!d.igual) {
      console.log(
        `  pixel: ${d.pixel.mesmaDimensao ? `${d.pixel.diferentes}/${d.pixel.total} diferentes, maior delta ${d.pixel.maiorDelta}` : 'DIMENSAO DIFERENTE entre as duas rodadas'}`,
      );
      falhas.push(
        `determinismo: frame ${a.frame} deu ${d.hashA} e ${d.hashB}. Procure ` +
          'relogio, aleatoriedade sem semente ou fonte carregada por rede.',
      );
    }
  }

  // -------------------------------------------------------------- portao 4
  if (roda('loop')) {
    console.log(`\n== portao 4: emenda de loop ==`);
    const l = await emendaDeLoop({video, saida: path.join(saida, 'loop.mp4')});
    console.log(`  ${l.saida} · ${l.voltas + 1} voltas · ${mb(l.bytes)}`);
    console.log(`  ASSISTA A EMENDA. Reel que reinicia limpo ganha reexibicao.`);
  }

  console.log('');
  if (falhas.length > 0) {
    for (const f of falhas) console.error(`FALHA  ${f}`);
    process.exit(1);
  }
  console.log('checagens duras: OK. As conferencias de olho continuam por fazer.');
}
