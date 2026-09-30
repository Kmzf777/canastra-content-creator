// Gera `projetos/<projeto>/props.json` A PARTIR de `transcricao.json`.
//
//   node scripts/gerar-props.mjs
//   node scripts/gerar-props.mjs --projeto=projetos/01-private-label
//
// Existe porque a primeira versao do props.json deste projeto trazia 20 blocos
// ESCRITOS A MAO ("Aqui na", "Canastra a", "gente torra"...) com uma chave
// `_LEIA` admitindo que eram exemplo -- e quatro MP4 foram renderizados com esse
// texto falso queimado no quadro. Legenda de peca entregavel sai daqui, nunca da
// mao.
//
// O QUE ELE NAO FAZ: nao agrupa por conta propria. O agrupamento e `agrupar()`
// de src/legenda/agrupar.ts (teto de LEGENDA.maxPalavras palavras por bloco,
// piso de LEGENDA.duracaoMinFrames frames). Se a regra de legenda mudar, muda
// la, nao aqui.
//
// O QUE ELE PRESERVA: `arquivo`, `razaoFonte` e `cortarAntesFrames` do props.json
// que ja existe. Esses tres foram MEDIDOS no arquivo fonte (ffprobe +
// silencedetect); reescrever por conta propria seria inventar. Se o props.json
// nao existir, eles tem que vir por argumento -- o script recusa em vez de
// chutar.
//
// Preserva TAMBEM `manchete` e `_manchete`, por um motivo diferente: a manchete
// nao e medida, e uma CITACAO LITERAL da fala com a origem registrada (indices
// das palavras na transcricao), conferida por `tests/manchete-props.test.ts`.
// Este script nao sabe escolher trecho de citacao, e nao deve: escolher seria
// inventar. Mas nao preservar seria pior -- o campo desapareceria em silencio e
// o render seguinte sairia sem manchete, sem erro nenhum, que e exatamente o
// modo de falha que o resto deste arquivo existe para matar.
//
// ---------------------------------------------------------------------------
// DESLOCAMENTO: por que este script NAO desloca nada
// ---------------------------------------------------------------------------
// `Legenda.tsx` faz `f = useCurrentFrame() + deslocamentoFrames` e `PecaVideo`
// passa `deslocamentoFrames={cortarAntesFrames}`. Ou seja: a CAMADA converte o
// frame da peca para frame da FONTE antes de procurar o bloco. Logo os blocos de
// props.json tem que estar no tempo da FONTE, cru, sem pre-alinhamento. Somar o
// corte aqui atrasaria a legenda inteira em cortarAntesFrames (1,13 s a 30 fps).
//
// Isso NAO e assumido: `provarTempoDaFonte()` abaixo prova, com numero medido,
// que a transcricao esta no tempo da fonte -- e se nao conseguir provar, o
// script morre sem escrever arquivo.
//
// O script roda com `--experimental-strip-types` (Node 22 nao carrega `.ts`
// sem ela) e se relanca sozinho, igual `conferir.mjs`. Imports dinamicos de
// proposito: import estatico de `.ts` resolve antes da primeira linha executar e
// mataria o processo pai com ERR_UNKNOWN_FILE_EXTENSION.

import {spawn} from 'node:child_process';
import fs from 'node:fs';
import {register} from 'node:module';
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
    await gerar();
  } catch (e) {
    console.error(`\nFALHA  ${e.message}`);
    if (process.env.CANASTRA_PILHA) console.error(e);
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------

function argumentos() {
  const a = {
    projeto: 'projetos/01-private-label',
    fps: 30,
    // Espelha DURACAO_FRAMES de src/motor/Raiz.tsx. Serve so para o relatorio de
    // bloco invisivel; nao entra no props.json.
    duracaoFrames: 696,
    // Usados APENAS quando nao existe props.json para preservar.
    arquivo: '',
    razaoFonte: 0,
    cortarAntesFrames: -1,
  };
  for (const cru of process.argv.slice(2)) {
    const m = /^--([a-zA-Z]+)=(.*)$/.exec(cru);
    if (!m) throw new Error(`argumento nao entendido: ${cru}. Use --chave=valor.`);
    const [, chave, valor] = m;
    if (!(chave in a)) {
      throw new Error(`--${chave} nao existe. Validos: ${Object.keys(a).join(', ')}.`);
    }
    a[chave] = typeof a[chave] === 'number' ? Number(valor) : valor;
  }
  if (!Number.isFinite(a.fps) || a.fps <= 0) throw new Error(`--fps=${a.fps} invalido`);
  return a;
}

/**
 * Os tres campos medidos. Vem do props.json existente; argumento so completa o
 * que faltar. Nada aqui tem valor padrao inventado.
 */
function camposMedidos(a, anterior) {
  const campos = {
    arquivo: a.arquivo || anterior?.arquivo,
    razaoFonte: a.razaoFonte || anterior?.razaoFonte,
    cortarAntesFrames:
      a.cortarAntesFrames >= 0 ? a.cortarAntesFrames : anterior?.cortarAntesFrames,
  };
  for (const [k, v] of Object.entries(campos)) {
    if (v === undefined || v === null || v === '' || Number.isNaN(v)) {
      throw new Error(
        `nao sei o valor de "${k}": nao esta no props.json anterior nem veio por ` +
          `--${k}=. Esse campo e MEDIDO no arquivo fonte; nao vou chutar.`,
      );
    }
  }
  if (!Number.isInteger(campos.cortarAntesFrames) || campos.cortarAntesFrames < 0) {
    throw new Error(`cortarAntesFrames=${campos.cortarAntesFrames} tem que ser inteiro >= 0`);
  }
  return campos;
}

/**
 * Prova, por medicao, que `transcricao.json` esta no tempo da FONTE (t=0 no
 * primeiro frame do arquivo original) e nao no tempo da PECA (t=0 depois do
 * corte do ar morto).
 *
 * A prova: se a transcricao terminasse depois do corte, ela nao poderia passar
 * da duracao da peca. Ela passa. Logo e tempo de fonte.
 *
 * Quando a prova nao fecha o script RECUSA. Legenda deslocada errado e o defeito
 * que este arquivo existe para nunca mais deixar passar -- na duvida, nao
 * escrever e melhor que escrever torto.
 */
function provarTempoDaFonte({palavras, fps, duracaoFrames, duracaoFonteMs}) {
  const fimMs = Math.max(...palavras.map((p) => p.fimMs));
  const duracaoPecaMs = (duracaoFrames / fps) * 1000;
  if (fimMs > duracaoPecaMs) {
    return {
      fimMs,
      duracaoPecaMs,
      duracaoFonteMs,
      prova:
        `a ultima palavra fecha em ${fimMs} ms e a PECA tem so ` +
        `${Math.round(duracaoPecaMs)} ms; tempo de peca nao caberia. ` +
        `A FONTE tem ${Math.round(duracaoFonteMs)} ms e cabe.`,
    };
  }
  throw new Error(
    `nao consigo provar em que tempo esta transcricao.json. A ultima palavra ` +
      `fecha em ${fimMs} ms, que cabe tanto na peca (${Math.round(duracaoPecaMs)} ms) ` +
      `quanto na fonte (${Math.round(duracaoFonteMs)} ms). Sem prova eu nao escolho ` +
      `deslocamento, e sem deslocamento certo o props.json sai errado. ` +
      `Meca a cabeca do audio e passe a convencao explicitamente.`,
  );
}

async function gerar() {
  const a = argumentos();
  const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  process.chdir(raiz);

  // `agrupar.ts` importa `../identidade/tokens` sem extensao (convencao
  // `moduleResolution: bundler` do projeto). O resolvedor cru do Node nao segue
  // isso; o gancho resolve. Tem que ser registrado ANTES do import dinamico.
  register('./_resolver-ts.mjs', import.meta.url);

  const {agrupar} = await import('../src/legenda/agrupar.ts');
  const {LEGENDA} = await import('../src/identidade/tokens.ts');
  const {sondar} = await import('../src/motor/sondar.ts');

  const transcricao = path.join(a.projeto, 'transcricao.json');
  const props = path.join(a.projeto, 'props.json');

  if (!fs.existsSync(transcricao)) {
    throw new Error(
      `${transcricao} nao existe. Sem transcricao real nao nasce props.json: ` +
        'rode a transcricao (src/legenda/transcrever.ts) antes.',
    );
  }

  const palavras = JSON.parse(fs.readFileSync(transcricao, 'utf8'));
  if (!Array.isArray(palavras) || palavras.length === 0) {
    throw new Error(`${transcricao} nao e uma lista de palavras com conteudo`);
  }
  for (const [i, p] of palavras.entries()) {
    if (typeof p?.texto !== 'string' || !Number.isFinite(p?.inicioMs) || !Number.isFinite(p?.fimMs)) {
      throw new Error(`palavra ${i} de ${transcricao} nao tem texto/inicioMs/fimMs`);
    }
  }

  const anterior = fs.existsSync(props) ? JSON.parse(fs.readFileSync(props, 'utf8')) : null;
  const medidos = camposMedidos(a, anterior);

  // Duracao real da fonte, medida agora -- e ela que sustenta a prova de tempo.
  // `medidos.arquivo` e so o nome (pl.mp4); o prefixo da subpasta vive em
  // src/motor/pasta-publica.ts e e o mesmo que Fonte.tsx usa no staticFile.
  const fonte = await sondar(
    path.join(a.projeto, 'public', 'fonte', medidos.arquivo),
  );
  const prova = provarTempoDaFonte({
    palavras,
    fps: a.fps,
    duracaoFrames: a.duracaoFrames,
    duracaoFonteMs: fonte.duracao * 1000,
  });

  const blocos = agrupar(palavras, {fps: a.fps});

  const saida = {
    // NAO existe chave `_LEIA`. Ela admitia texto de exemplo; texto de exemplo
    // nao mora mais neste arquivo.
    _frames:
      'Os frames estao no tempo da FONTE (arquivo original, antes do corte). ' +
      'Legenda.tsx desloca por cortarAntesFrames. Nao pre-alinhe aqui.',
    _origem: `gerado por scripts/gerar-props.mjs a partir de ${path
      .basename(transcricao)} (${palavras.length} palavras)`,
    // A manchete atravessa intacta. Ver "O QUE ELE PRESERVA" no cabecalho: nao e
    // campo medido, e citacao com proveniencia, e este script nao tem como
    // reconstitui-la. Espalhamento condicional para que um projeto SEM manchete
    // nao ganhe uma chave `manchete: undefined` no JSON.
    ...(anterior?._manchete === undefined ? {} : {_manchete: anterior._manchete}),
    arquivo: medidos.arquivo,
    razaoFonte: medidos.razaoFonte,
    cortarAntesFrames: medidos.cortarAntesFrames,
    ...(anterior?.manchete === undefined ? {} : {manchete: anterior.manchete}),
    blocos,
  };

  fs.writeFileSync(props, `${JSON.stringify(saida, null, 2)}\n`, 'utf8');

  // ------------------------------------------------------------- relatorio
  const corte = medidos.cortarAntesFrames;
  const fimPeca = corte + a.duracaoFrames;
  const invisiveis = blocos.filter((b) => b.fimFrame <= corte || b.inicioFrame >= fimPeca);
  const palavrasDeVolta = blocos.map((b) => b.texto).join(' ');
  const palavrasOriginais = palavras.map((p) => p.texto).join(' ');

  console.log(`\n== props.json gerado ==`);
  console.log(`  ${props}`);
  console.log(`  fonte medida: ${fonte.largura}x${fonte.altura} · ${fonte.duracao.toFixed(3)}s`);
  console.log(`\n== convencao de tempo ==`);
  console.log(`  TEMPO DA FONTE, deslocamento aplicado aqui: 0 frames`);
  console.log(`  prova: ${prova.prova}`);
  console.log(`  quem desloca e Legenda.tsx, por deslocamentoFrames=${corte}`);
  console.log(`\n== blocos ==`);
  console.log(
    `  ${palavras.length} palavras -> ${blocos.length} blocos ` +
      `(teto ${LEGENDA.maxPalavras} palavras, piso ${LEGENDA.duracaoMinFrames} frames)`,
  );
  console.log(
    `  primeiro: frame ${blocos[0].inicioFrame}-${blocos[0].fimFrame} "${blocos[0].texto}"`,
  );
  const u = blocos[blocos.length - 1];
  console.log(`  ultimo  : frame ${u.inicioFrame}-${u.fimFrame} "${u.texto}"`);
  console.log(`  janela visivel da peca, em frames de fonte: ${corte}..${fimPeca}`);
  console.log(
    `  texto preservado palavra por palavra: ${palavrasDeVolta === palavrasOriginais ? 'SIM' : 'NAO'}`,
  );
  if (palavrasDeVolta !== palavrasOriginais) {
    throw new Error('agrupar() perdeu ou reordenou palavra. props.json escrito esta suspeito.');
  }

  console.log(`\n== manchete ==`);
  if (saida.manchete) {
    console.log(
      `  PRESERVADA do props.json anterior: "${saida.manchete.texto}" · modo ` +
        `${saida.manchete.modo} · inicioFrame ${saida.manchete.inicioFrame} (tempo da fonte)`,
    );
    console.log(
      `  origem declarada: palavras ${saida._manchete?.dePalavra}..${saida._manchete?.atePalavra} ` +
        `da transcricao -> "${saida._manchete?.citacao}"`,
    );
    console.log(`  quem confere que isso e citacao literal: tests/manchete-props.test.ts`);
  } else {
    console.log(`  nenhuma. A manchete e opcional; a peca sai completa sem ela.`);
  }

  if (invisiveis.length > 0) {
    console.log(`\n== ATENCAO: ${invisiveis.length} bloco(s) fora da janela visivel ==`);
    for (const b of invisiveis) {
      console.log(`  frame ${b.inicioFrame}-${b.fimFrame} "${b.texto}"  <- nunca aparece`);
    }
    console.log(
      `  Isto NAO foi corrigido de proposito: mexer no tempo destes blocos seria\n` +
        `  inventar alinhamento. E defeito da transcricao na cabeca do audio, e tem\n` +
        `  que ser relatado, nao disfarcado.`,
    );
  }
  console.log('');
}
