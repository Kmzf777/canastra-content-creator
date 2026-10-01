// Os portoes de verificacao, em ordem, num comando.
//
//   node scripts/conferir.mjs
//   node scripts/conferir.mjs --projeto=projetos/01-private-label --composicao=Reel
//   node scripts/conferir.mjs --portao=determinismo
//   node scripts/conferir.mjs --portao=selo      <- NAO precisa de render
//
// Nada aqui aprova a peca. Os portoes 1 e 4 (folha de contato e emenda de loop)
// produzem material para o OLHO -- eles falham se o ffmpeg falhar, nao se a peca
// estiver feia. Os portoes 0, 2 e 3 (selo, telefone e determinismo) tem veredito
// programatico. Sair com codigo 0 significa "os arquivos de conferencia estao
// prontos e as checagens duras passaram", nunca "pode publicar".
//
// O PORTAO 0 RODA ANTES DE TUDO, E ANTES DO RENDER
//
// Ele compara o selo de `plano.json` com o briefing em disco, e por isso e o unico que
// nao exige a peca renderizada: roda logo depois do compile, antes de gastar um render.
// Esta no inicio porque um plano fora de sincronia invalida TODOS os portoes seguintes
// -- medir determinismo de uma peca que nao corresponde ao briefing e medir a coisa
// errada com precisao. Ver o cabecalho de `src/verificacao/selo.ts`.
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
//
// O RELANCAMENTO TAMBEM LIGA O GANCHO DE RESOLUCAO
//
// Antes do portao 0 nenhum portao importava modulo do projeto, e o cabecalho de
// `folha.ts` registra a razao: o strip-types do Node nao adivinha extensao, e por
// isso os portoes recebiam valor por parametro em vez de importar. O portao do selo
// NAO pode seguir essa regra -- ele precisa da MESMA `sha256Do` que `compilar.mjs`
// usa para selar, e uma segunda copia da serializacao canonica e justamente como o
// defeito original (allowlist de chaves de topo) voltaria a existir sem ninguem ver.
//
// Entao em vez de duplicar a regra, o relancamento passa a ligar
// `_registrar-ts.mjs`, que ja existe exatamente para isto. Por URL absoluta: o
// `--import` relativo resolve contra o cwd, e este script faz `process.chdir(raiz)`
// so DEPOIS do relancamento.

import {spawn} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const FLAG = '--experimental-strip-types';

if (!process.execArgv.includes(FLAG)) {
  const registrador = pathToFileURL(
    path.join(path.dirname(fileURLToPath(import.meta.url)), '_registrar-ts.mjs'),
  ).href;
  const filho = spawn(
    process.execPath,
    [
      FLAG,
      '--no-warnings',
      '--import',
      registrador,
      fileURLToPath(import.meta.url),
      ...process.argv.slice(2),
    ],
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
  const validos = ['todos', 'selo', 'folha', 'telefone', 'determinismo', 'loop'];
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
  const {conferirSeloDoProjeto} = await import('../src/verificacao/selo.ts');

  const saida = path.join(a.projeto, 'saida');
  // `plano.json`, nao `props.json`: o plano e o artefato que `compilar.ts` gera a
  // partir do briefing, e e o unico que as composicoes entendem desde 01/10/2026 --
  // `Raiz.tsx` le `fps` e `durationInFrames` dele por `calculateMetadata`.
  const props = path.join(a.projeto, 'plano.json');
  // A pasta publica e a do PROJETO, com `fonte/` e `assets/` dentro dela.
  // Ver src/motor/pasta-publica.ts: o Remotion tem uma so, e ela precisava
  // servir o video cru E os recortes de embalagem ao mesmo tempo.
  const publicDir = path.join(a.projeto, 'public');
  const video = path.join(saida, `${a.composicao.toLowerCase()}.mp4`);

  const roda = (nome) => a.portao === 'todos' || a.portao === nome;
  const falhas = [];

  // -------------------------------------------------------------- portao 0
  // ANTES da checagem de arquivos do render: este portao nao precisa da peca, e
  // precisa reprovar antes de alguem gastar um render com plano fora de sincronia.
  if (roda('selo')) {
    console.log(`\n== portao 0: selo do plano ==`);
    const s = conferirSeloDoProjeto(a.projeto);
    console.log(`  briefing ${s.caminhoBriefing}`);
    console.log(`  plano    ${s.caminhoPlano}`);
    // OS DOIS selos, sempre, mesmo quando o primeiro ja reprovou: imprimir so o do
    // briefing e o que deixou o ataque do cetico passar por um mes -- ele leu
    // `esperado == no plano` e concluiu que o plano estava intacto. Ver o cabecalho de
    // `src/verificacao/selo.ts`.
    console.log(`  briefing: esperado   ${s.esperado}`);
    console.log(`  briefing: no plano   ${s.encontrado || '(vazio -- plano nao selado)'}`);
    console.log(`  plano:    esperado   ${s.esperadoPlano}`);
    console.log(`  plano:    no plano   ${s.encontradoPlano || '(vazio -- plano nao selado)'}`);
    console.log(
      `  ${s.bate ? 'OK — o plano veio deste briefing E nao foi editado depois' : 'SELO NAO BATE'}`,
    );
    if (!s.bate) falhas.push(`selo: ${s.motivo}`);
  }

  // Se o alvo era so o selo, nada abaixo se aplica: sair aqui evita exigir um MP4
  // que o portao 0 nunca le.
  if (a.portao === 'selo') {
    console.log('');
    if (falhas.length > 0) {
      for (const f of falhas) console.error(`FALHA  ${f}`);
      process.exit(1);
    }
    console.log('selo: OK.');
    return;
  }

  for (const [rotulo, p] of [
    ['a peca renderizada', video],
    ['o plano.json', props],
    ['a pasta publica', publicDir],
  ]) {
    if (!fs.existsSync(p)) {
      throw new Error(
        `${rotulo} nao existe: ${p}. Rode ` +
          '`node --import ./scripts/_registrar-ts.mjs --experimental-strip-types ' +
          'scripts/compilar.mjs --projeto=<dir>` e depois o render, antes dos portoes.',
      );
    }
  }

  const fonte = await sondar(video);
  // `sondar()` devolve `null` em `duracao`, `fps` e `fpsMedio` para imagem parada
  // desde 01/10/2026. Aqui o alvo e sempre um MP4 renderizado, mas imprimir
  // `null.toFixed` seria um TypeError a esperar o dia em que alguem apontar o
  // portao para um still.
  if (fonte.duracao === null || fonte.fps === null) {
    throw new Error(
      `${video} nao e um video: sondar() diz imagem parada. Os portoes conferem ` +
        'a peca renderizada, nao um still.',
    );
  }
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
