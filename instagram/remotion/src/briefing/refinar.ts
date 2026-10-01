// AS RECUSAS DE SENTIDO. Puro: sem React, sem remotion, sem I/O.
//
// zod valida FORMA. Um briefing pode ter forma perfeita e nao fazer sentido: uma cena
// de 1,2 s com uma manchete de seis palavras, duas camadas na mesma pista no mesmo
// frame, um carimbo de lote inventado, uma licenca ligada sem motivo escrito. Sentido
// e aqui.
//
// DEVOLVE A LISTA INTEIRA, NAO A PRIMEIRA
//
// Quem escreve briefing quer consertar tudo numa passada. Recusar a primeira e obrigar
// uma rodada por erro -- e em briefing de 8 cenas isso sao 8 rodadas.
//
// RODA ANTES DO RENDER
//
// Cada recusa aqui e um render que nao acontece. Render de Reel de 23 s leva minutos;
// `refinar()` leva milissegundos. E a licao "erro e evidencia barata" do CLAUDE.md
// aplicada ao motor.

import {cadencia} from '../motor/cadencia';
import {layout} from '../motor/layout';
import {CONFLITO_DE_PISTA, type Pista} from '../motor/pista';
import {duracaoComIrmaos, duracaoDeIrmao} from '../motor/movimento';
import {emFrames} from '../motor/relogio';
import {resolverEncaixe} from '../motor/encaixe';
import {DIMENSAO, LICENCAS, type Briefing, type Cena, type EventoTexto} from './esquema';

export type Recusa = {
  /** slug estavel, para teste e para o portao de ritmo */
  codigo: string;
  /** caminho do campo no briefing, no formato que um humano acha no arquivo */
  campo: string;
  mensagem: string;
};

/**
 * Lote, fabricacao e validade. Licao 22 do CLAUDE.md: o modelo redesenha carimbo
 * variavel como qualquer outro texto, e saiu `F:23.2025` -- um mes que nao existe. No
 * Canela saiu `F:12.2025`, plausivel, e passaria despercebido. Plausivel e pior que
 * absurdo: o absurdo voce ve.
 */
const REGULATORIO = /^\s*F\s*[:.]|\bVAL\b|\bVALIDADE\b|\bLOTE\b|\bFAB\b/i;

/** A linha de `proibicoes.md` que cada licenca derruba, para a mensagem citar. */
const LINHA_DA_LICENCA: Record<string, string> = {
  particulas: 'proibicoes.md:11-12 ("explosao de particula")',
  orbesDeBrilho: 'proibicoes.md:11 ("brilho")',
  varreduraDeLuz: 'proibicoes.md:11 ("brilho")',
  shockwave: 'proibicoes.md:11-12 (particula + brilho)',
  molaComOvershoot: 'proibicoes.md:11 ("easing elastico")',
  revelarCaractereACaractere: 'proibicoes.md:14 ("Revelar texto caractere a caractere")',
  flashNoCorte: 'proibicoes.md:16 ("Flash branco instantaneo")',
  irisWipe: 'proibicoes.md:16 (vizinhanca de "whip pan")',
  motionBlurBurst: 'proibicoes.md:7-8 (nomeia <CameraMotionBlur>)',
  swipeMarcaTexto: 'proibicoes.md:20 (seria o 2o saturado ao lado de COR.acento)',
  highlightPalavraAtiva: 'nao e proibicao: e 1 acento, mas troca 2,45x/s',
  aceitaTempoMorto: 'proibicoes.md:11-12 ("tempo morto")',
};

/** Quantos frames o evento ocupa, no PIOR formato pedido (o mais apertado). */
export function duracaoDoEventoFrames(
  e: EventoTexto,
  b: Briefing,
): {frames: number; irmao: number} {
  const c = cadencia(b.fps);
  if (e.duracaoS !== undefined) {
    const frames = emFrames(e.duracaoS, b.fps);
    return {frames, irmao: frames};
  }

  // Sem `duracaoS` declarado, a duracao e a da FRASE -- e ela depende de quantos
  // irmaos o texto tem, que depende da quebra de linha, que depende do formato.
  // Pega-se o MAIOR entre os formatos pedidos, para o evento caber em todos.
  let maior = 0;
  let maiorIrmao = 0;
  for (const formato of b.formatos) {
    const {largura, altura} = DIMENSAO[formato];
    const z = layout({largura, altura, razaoFonte: razaoDaPeca(b) ?? largura / altura});
    const r = resolverEncaixe({
      texto: e.texto,
      papel: e.papel,
      pista: e.pista,
      zonas: z,
      cadencia: c,
      palavraAcento: e.palavraAcento,
    });
    // `forma.irmaos` E A UNICA CONTAGEM DO SISTEMA. Ela sai de `CADENCIA_DO_PAPEL`
    // dentro de `formaTextoTela`, que e o MESMO lugar de onde sai o `atrasoFrames` de
    // cada palavra e o `duracaoCena` de `TextoTela`. Um `contarIrmaos()` proprio aqui
    // seria uma segunda implementacao da mesma regra, e duas implementacoes divergem
    // no primeiro conserto -- foi assim que o plano contou 36 frames para a etiqueta
    // enquanto a tela desenhava 42.
    const irmaos = r.forma.irmaos;
    const irmao = duracaoDeIrmao(irmaos, c);
    const total = duracaoComIrmaos(irmaos, irmao, c);
    if (total > maior) {
      maior = total;
      maiorIrmao = irmao;
    }
  }
  return {frames: maior, irmao: maiorIrmao};
}

/**
 * A razao de exibicao que a PECA usa em `layout()`.
 *
 * E a MENOR entre as cenas que entram por CONTAIN (`enquadramento` = `faixa`), porque
 * sao elas, e so elas, que obrigam o quadro a abrir uma faixa de terra ao lado da
 * imagem. A caixa de legenda e a coluna de texto sao dimensionadas por essa razao: com
 * a menor delas, a legenda cabe sobre a imagem de todas as cenas em contain. `null`
 * quando NENHUMA cena entra por contain -- e ai quem chama usa a razao do proprio
 * quadro, e a imagem ocupa o quadro inteiro.
 *
 * O ENQUADRAMENTO NAO PODE SER IGNORADO AQUI. Uma versao que fizesse
 * `razoes.push(f.razaoExibicao)` para todo `video` e toda `foto` devolveria 1,3333
 * numa peca cuja unica cena e uma foto 4:3 com `registro: "telaCheia"` +
 * `enquadramento: {tipo:"recorte"}`: `layout()` poria a imagem como faixa de 1080x810
 * no 9:16 e a cena `telaCheia` preencheria 810 de 1920 px -- 57,81% do quadro em terra
 * chapado, com o nome de "tela cheia". `recorte` (foto) e `preencher` (video) sao
 * exatamente a declaracao de que aquela cena CORTA para encher o quadro.
 *
 * `cor` e `grade` ficam fora da conta pelo mesmo motivo: nao tem razao de arquivo a
 * honrar.
 */
export function razaoDaPeca(b: Briefing): number | null {
  const razoes: number[] = [];
  for (const cena of b.cenas) {
    const f = cena.fonte;
    // `faixa` e a UNICA palavra que significa contain nos dois tipos -- string no
    // video, objeto discriminado na foto.
    if (f.tipo === 'video' && f.enquadramento === 'faixa') razoes.push(f.razaoExibicao);
    if (f.tipo === 'foto' && f.enquadramento.tipo === 'faixa') razoes.push(f.razaoExibicao);
  }
  return razoes.length === 0 ? null : Math.min(...razoes);
}

// `pistaDoEvento()` NAO EXISTE: `e.pista` e obrigatoria no esquema, e uma funcao que
// aplicasse `PISTA_PADRAO` aqui seria o default escondido de novo -- agora dentro do
// refinador, onde ninguem procuraria por ele.

export function refinar(b: Briefing): Recusa[] {
  const r: Recusa[] = [];

  if (b.transicoes.length !== b.cenas.length - 1) {
    r.push({
      codigo: 'transicoes-contagem',
      campo: 'transicoes',
      mensagem:
        `sao ${b.cenas.length} cenas, logo ${b.cenas.length - 1} transicoes, e o ` +
        `briefing tem ${b.transicoes.length}. Uma sobrando ou faltando sai como video ` +
        'torto com exit 0. Use {"tipo": "corte"} onde nao houver transicao: corte e 0 ' +
        'frames.',
    });
  }

  if (b.duracao.modo === 'totalFixo' && b.duracao.alvoS === undefined) {
    r.push({
      codigo: 'totalfixo-sem-alvo',
      campo: 'duracao.alvoS',
      mensagem:
        'duracao.modo e "totalFixo" e nao ha alvoS. Em totalFixo o alvo MANDA e as ' +
        'cenas sao ajustadas; sem alvo nao ha o que mandar.',
    });
  }

  // AUDIO. A regra escrita sobre campos que existem.
  if (b.audio.locucao === null && b.audio.trilha === null) {
    r.push({
      codigo: 'audio-mudo',
      campo: 'audio',
      mensagem:
        'audio.locucao e audio.trilha sao os dois null: a peca sai MUDA. ' +
        '`05-formatos.md` §3, [oficial]: Reel sem audio perde elegibilidade para ' +
        'nao-seguidor. "Mudo" no catalogo significa SEM LOCUCAO, nunca sem faixa -- e ' +
        '5 das 12 series entregam Reel a partir de foto parada, que nao tem som ' +
        'nenhum. Declare uma trilha, ou uma locucao, ou as duas.',
    });
  }

  // A ANCORA DA LEGENDA TEM QUE SER RESOLVIVEL.
  if (b.legenda) {
    const a = b.legenda.ancora;
    const saidas =
      'As tres saidas: ancore na locucao (e declare audio.locucao), aponte uma cena ' +
      'com {"tipo":"cena","indice":N} cuja fonte tenha aparaAntesS, ou declare o ' +
      'valor cru com {"tipo":"segundo","valorS":X}.';

    if (a.tipo === 'locucao' && b.audio.locucao === null) {
      r.push({
        codigo: 'legenda-sem-ancora',
        campo: 'legenda.ancora',
        mensagem:
          'a legenda esta ancorada na locucao e audio.locucao e null: nao ha de onde ' +
          `ler o instante que cai no frame 0 da peca. ${saidas} O compilador NAO ` +
          'escolhe a cena 0 por conveniencia -- default escondido e o que este ' +
          'desenho proibe em toda parte.',
      });
    }

    if (a.tipo === 'cena') {
      const cena = b.cenas[a.indice];
      if (!cena) {
        r.push({
          codigo: 'legenda-sem-ancora',
          campo: 'legenda.ancora.indice',
          mensagem:
            `a ancora aponta a cena ${a.indice} e o briefing tem ${b.cenas.length} ` +
            `cena(s), indices 0..${b.cenas.length - 1}. ${saidas}`,
        });
      } else if (cena.fonte.tipo === 'foto') {
        r.push({
          codigo: 'legenda-sem-ancora',
          campo: 'legenda.ancora.indice',
          mensagem:
            `a ancora aponta a cena ${a.indice}, que e FOTO: foto nao tem tempo, logo ` +
            `nao tem apara. ${saidas}`,
        });
      } else if (cena.fonte.tipo !== 'video') {
        r.push({
          codigo: 'legenda-sem-ancora',
          campo: 'legenda.ancora.indice',
          mensagem:
            `a ancora aponta a cena ${a.indice}, cuja fonte e "${cena.fonte.tipo}" e ` +
            `nao tem aparaAntesS para ler. ${saidas}`,
        });
      }
    }
  }

  for (const chave of LICENCAS) {
    if (!b.licencas[chave]) continue;
    if (b.licencas.justificativa.trim().length < 12) {
      r.push({
        codigo: 'licenca-sem-justificativa',
        campo: `licencas.${chave}`,
        mensagem:
          `a licenca "${chave}" esta ligada e derruba ${LINHA_DA_LICENCA[chave]}. ` +
          'Ligar uma exige justificativa de 12 caracteres ou mais em ' +
          'licencas.justificativa -- decisao sem motivo escrito nao sobrevive a ' +
          'proxima sessao. E nenhuma tecnica de licenca esta implementada nesta ' +
          'versao: o campo registra a decisao, o codigo vem depois dela.',
      });
    }
  }

  b.cenas.forEach((cena, i) => {
    refinarCena(cena, i, b, r);
  });

  b.transicoes.forEach((t, i) => {
    if (t.tipo === 'corte') return;
    const frames = emFrames(t.duracaoS, b.fps);
    const vizinhas = [
      emFrames(b.cenas[i]?.duracaoS ?? 0, b.fps),
      emFrames(b.cenas[i + 1]?.duracaoS ?? 0, b.fps),
    ];
    const menor = Math.min(...vizinhas);
    if (frames >= menor) {
      r.push({
        codigo: 'transicao-maior-que-cena',
        campo: `transicoes[${i}].duracaoS`,
        mensagem:
          `a transicao pede ${frames} frames e a cena vizinha mais curta tem ` +
          `${menor}. Durante a transicao as DUAS cenas sao renderizadas, entao uma ` +
          'transicao maior que a cena consome a cena inteira e a proxima comeca antes ' +
          'da anterior aparecer.',
      });
    }
  });

  return r;
}

function refinarCena(cena: Cena, i: number, b: Briefing, r: Recusa[]): void {
  const f = cena.fonte;

  if (f.tipo === 'cor' && f.cor.toUpperCase() === '#FFFFFF') {
    r.push({
      codigo: 'branco-puro',
      campo: `cenas[${i}].fonte.cor`,
      mensagem:
        'branco puro e o padrao do modelo generativo sem direcao, e proibicoes.md:13 ' +
        'o nomeia. O fundo da marca e COR.terra (#3B2A1F).',
    });
  }

  if ((f.tipo === 'video' || f.tipo === 'foto') && /[\\/]/.test(f.arquivo)) {
    r.push({
      codigo: 'arquivo-com-caminho',
      campo: `cenas[${i}].fonte.arquivo`,
      mensagem:
        `"${f.arquivo}" tem separador de pasta. Este campo e o NOME do arquivo dentro ` +
        'de public/fonte/; o prefixo vive em Fonte.tsx por SUB.fonte, para que mudar a ' +
        'convencao de pasta nao obrigue a reescrever cada briefing.',
    });
  }

  if (f.tipo === 'foto' && f.registro === 'telaCheia' && f.enquadramento.tipo === 'faixa') {
    r.push({
      codigo: 'telacheia-com-faixa',
      campo: `cenas[${i}].fonte.enquadramento`,
      mensagem:
        '`registro: "telaCheia"` diz que a foto E o quadro, e ' +
        '`enquadramento: {"tipo":"faixa"}` e `contain`: ele deixa fundo chapado em ' +
        '42,19% da altura numa foto paisagem num 9:16 (medido). As duas declaracoes ' +
        'nao cabem juntas. Ou declare `{"tipo":"recorte", ...}` em fracao da fonte, ou ' +
        'troque o registro para "moldura" ou "cartao", que existem justamente para a ' +
        'foto NAO preencher o quadro.',
    });
  }

  if (f.tipo === 'grade' && f.colunas * f.linhas !== f.celulas.length) {
    r.push({
      codigo: 'grade-incompleta',
      campo: `cenas[${i}].fonte.celulas`,
      mensagem:
        `grade de ${f.colunas}x${f.linhas} pede ${f.colunas * f.linhas} celulas e ` +
        `recebeu ${f.celulas.length}. Celula faltando deixa buraco de terra que parece ` +
        'bug de render.',
    });
  }

  if (cena.eventos.length === 0 && !b.legenda && !b.licencas.aceitaTempoMorto) {
    r.push({
      codigo: 'tempo-morto',
      campo: `cenas[${i}].eventos`,
      mensagem:
        'cena sem nenhum evento e sem legenda na peca: sao ' +
        `${emFrames(cena.duracaoS, b.fps)} frames sem camada alguma, que e o "tempo ` +
        'morto" de proibicoes.md:11-12. Ligue licencas.aceitaTempoMorto com ' +
        'justificativa se for de proposito.',
    });
  }

  const comAcento = cena.eventos.filter((e) => e.palavraAcento !== undefined);
  if (comAcento.length > 1) {
    r.push({
      codigo: 'dois-acentos',
      campo: `cenas[${i}].eventos`,
      mensagem:
        `${comAcento.length} eventos desta cena declaram palavraAcento. ` +
        'proibicoes.md:20 pede UM acento de cor por cena, com funcao.',
    });
  }

  const duracaoCenaFrames = emFrames(cena.duracaoS, b.fps);
  const ocupacao: Array<{pista: Pista; de: number; ate: number; texto: string}> = [];

  cena.eventos.forEach((e, j) => {
    const palavras = e.texto.split(/\s+/).filter((p) => p.length > 0);
    if (e.palavraAcento !== undefined && e.palavraAcento >= palavras.length) {
      r.push({
        codigo: 'acento-fora-da-faixa',
        campo: `cenas[${i}].eventos[${j}].palavraAcento`,
        mensagem:
          `palavraAcento ${e.palavraAcento} e o texto tem ${palavras.length} palavras. ` +
          'Indice fora da faixa nao acentua nada e passa sem erro, que e pior que ' +
          'falhar: a peca sai sem o acento que alguem pediu.',
      });
    }

    if (e.papel === 'dado' && REGULATORIO.test(e.texto)) {
      r.push({
        codigo: 'dado-regulatorio',
        campo: `cenas[${i}].eventos[${j}].texto`,
        mensagem:
          `"${e.texto}" parece lote, fabricacao ou validade. Licao 22 do CLAUDE.md: ` +
          'carimbo variavel e regenerado e nunca confiavel -- saiu `F:23.2025`, um mes ' +
          'que nao existe, e `F:12.2025`, plausivel e por isso pior. Em peca de ' +
          'e-commerce isso e informacao regulatoria falsa: ou sai do enquadramento, ou ' +
          'entra por composicao da foto real.',
      });
    }

    // TETO E PISO NAO SE ENCONTRAM: RECUSA, E NAO UM CORPO ESCOLHIDO NO ESCURO.
    //
    // `resolverEncaixe` ja limita o corpo pelo teto de linha. Quando nem no teto o
    // texto alcanca o piso de dominancia, nenhum corpo serve -- maior tapa a imagem,
    // menor domina menos ainda. O motor poderia desenhar o corpo do teto e relatar
    // `domina: false`, e e exatamente isso que nao pode: seria escolher um corpo ruim
    // em silencio. O conserto e de BRIEFING, e e por isso que a queixa sai aqui.
    //
    // Por FORMATO, nominalmente, porque o caso depende do quadro: `250 G` em
    // `principal` tem corpo valido no 9:16 (310 px, mancha 16,02% contra piso 6,86%) e
    // nao tem no 16:9 (teto 174 px, mancha 4,21% contra piso 4,73%). Dizer so "este
    // evento nao cabe" mandaria consertar o que esta certo em dois dos formatos.
    for (const formato of b.formatos) {
      const {largura, altura} = DIMENSAO[formato];
      const z = layout({largura, altura, razaoFonte: razaoDaPeca(b) ?? largura / altura});
      const enc = resolverEncaixe({
        texto: e.texto,
        papel: e.papel,
        pista: e.pista,
        zonas: z,
        cadencia: cadencia(b.fps),
        palavraAcento: e.palavraAcento,
      });
      if (enc.semCorpoValido) {
        r.push({
          codigo: 'sem-corpo-valido',
          campo: `cenas[${i}].eventos[${j}]`,
          mensagem:
            `"${e.texto}" (papel '${e.papel}', pista '${e.pista}') nao tem corpo valido ` +
            `no formato ${formato}. ${enc.porque} Conserte no briefing: texto mais ` +
            'longo, outra pista, ou este formato fora de `formatos`.',
        });
      }
    }

    const {frames} = duracaoDoEventoFrames(e, b);
    const de = emFrames(e.entradaS, b.fps);
    const ate = de + frames;
    if (ate > duracaoCenaFrames) {
      r.push({
        codigo: 'evento-estoura-cena',
        campo: `cenas[${i}].eventos[${j}]`,
        mensagem:
          `o evento entra no frame ${de} da cena e ocupa ${frames} frames, terminando ` +
          `em ${ate}; a cena tem ${duracaoCenaFrames}. O stagger empurra o fim junto ` +
          'com o comeco (ver duracaoDeIrmao), entao a ultima palavra perderia a saida ' +
          'e sumiria por corte. Alongue a cena ou declare duracaoS no evento.',
      });
    }

    ocupacao.push({pista: e.pista, de, ate, texto: e.texto});
  });

  for (let a = 0; a < ocupacao.length; a++) {
    for (let bb = a + 1; bb < ocupacao.length; bb++) {
      const x = ocupacao[a];
      const y = ocupacao[bb];
      const seCruzam = x.de < y.ate && y.de < x.ate;
      const conflitam =
        CONFLITO_DE_PISTA[x.pista].includes(y.pista) ||
        CONFLITO_DE_PISTA[y.pista].includes(x.pista);
      if (seCruzam && conflitam) {
        r.push({
          codigo: 'pista-ocupada',
          campo: `cenas[${i}].eventos`,
          mensagem:
            `"${x.texto}" (pista ${x.pista}, frames ${x.de}..${x.ate}) e "${y.texto}" ` +
            `(pista ${y.pista}, frames ${y.de}..${y.ate}) ocupam pistas que conflitam ` +
            'ao mesmo tempo. Medido no motor antigo: a caixa da manchete se ' +
            'intersectava com a da legenda em 90,20 px no eixo x no 1:1 sem ninguem ' +
            'reclamar. A pista existe para isso ser erro, nao desenho.',
        });
      }
    }
  }
}

/** Lanca com TODAS as recusas, uma por linha. */
export function exigirBriefingCoerente(b: Briefing): void {
  const recusas = refinar(b);
  if (recusas.length === 0) return;
  throw new Error(
    `o briefing tem ${recusas.length} recusa(s) de sentido:\n` +
      recusas.map((x) => `  [${x.codigo}] ${x.campo}: ${x.mensagem}`).join('\n'),
  );
}
