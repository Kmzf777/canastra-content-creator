// Portao 0: o selo do plano.
//
// POR QUE ESTE ARQUIVO EXISTE
//
// `scripts/compilar.mjs` SELA `plano.json` com o sha256 do briefing que o produziu
// (`briefing/impressao.ts`). Ate 30/09/2026 ninguem nunca LIA esse selo de volta: tres
// comentarios no motor afirmavam que "o portao de ritmo reprova plano cujo hash nao
// bate", e `src/verificacao/ritmo.ts` nao existia. O selo era gravado em todo compile,
// em disco nos tres projetos, e comparado em lugar nenhum.
//
// Portao declarado e nao ligado e pior que portao ausente: ele cria confianca falsa.
// Quem lia aquele comentario em `Raiz.tsx` concluia que podia deixar de validar o plano
// porque "o portao pega" -- e o portao nao existia. Este arquivo e a metade que faltava.
//
// O QUE ELE IMPEDE, CONCRETAMENTE -- E O QUE ESTE CABECALHO AFIRMAVA SEM ENTREGAR
//
// `plano.json` e artefato gerado e vai inteiro para `--props` do render. Dois jeitos
// diferentes de o MP4 deixar de corresponder ao briefing, e ate 01/10/2026 este portao
// pegava SO o primeiro:
//
//   (1) o briefing mudou depois do compile, e o plano em disco e velho;
//   (2) o plano foi EDITADO A MAO, e o briefing nao mudou.
//
// Ate 01/10/2026 este cabecalho dizia que "editar um numero ali a mao produz um MP4 que
// NAO corresponde ao briefing", implicando que o portao pegava. Nao pegava. Um cetico
// gravou `duracaoFrames: 9999` (era 345) em `projetos/03-prova-cena/plano.json`,
// preservou `_sha256Briefing`, rodou o portao e recebeu:
//
//   esperado   f1a6ff392c544ac7d82a9960b5805f3e1db71dce7e1a893945a082bbd02808c4
//   no plano   f1a6ff392c544ac7d82a9960b5805f3e1db71dce7e1a893945a082bbd02808c4
//   OK — o plano veio deste briefing                                      EXIT=0
//
// E a resposta estava CERTA: aquele plano realmente veio daquele briefing. O selo
// hasheava so o briefing, entao o conteudo do plano nao entrava em hash nenhum e
// qualquer edicao que preservasse o campo passava. `duracaoFrames` e justamente o que
// `Raiz.tsx` le por `calculateMetadata`: a edicao muda a duracao do MP4.
//
// AGORA SAO DOIS SELOS, e as duas perguntas tem resposta separada:
//
//   `_sha256Briefing` = sha256(briefing parseado) ..... de onde este plano veio
//   `_sha256Plano`    = sha256(plano sem este campo) .. ele ainda e o que saiu de la
//
// Custo assumido: toda edicao do `plano.json` exige recompilar. Esta certo -- ele e
// artefato gerado, e a unica edicao legitima dele e a de `scripts/compilar.mjs`.
//
// O QUE O SELO DO PLANO *NAO* FAZ, MEDIDO 01/10/2026 PARA NAO VIRAR A QUARTA PROMESSA
// FALSA DESTE MOTOR
//
// Hash nao e ASSINATURA. Quem edita `duracaoFrames` e tambem recalcula `_sha256Plano`
// passa pelo portao. Medido: gravei `duracaoFrames: 9999` com
// `_sha256Plano = 05036b232d21...` recalculado e o portao respondeu `OK` com EXIT=0.
// Nao ha segredo no repositorio, entao nao pode haver: o selo detecta DERIVA (edicao a
// mao, artefato velho, briefing mexido depois do compile), nao FALSIFICACAO DELIBERADA.
// Para o modo de falha real deste projeto -- uma pessoa mexendo num numero para testar
// algo e esquecendo de desfazer -- deriva e o que importa. Nao escreva em lugar nenhum
// que o plano esta "protegido contra alteracao".
//
// O portao que pegaria tambem a falsificacao existe e NAO esta ligado: `conferirSelo`
// poderia chamar `compilar(briefing)` e comparar o plano inteiro, em vez de comparar o
// plano com o selo que ele mesmo carrega. Nao esta ligado porque custa ler a transcricao
// e passar por `refinar()` dentro do portao, e porque um aperto futuro em `refinar()`
// reprovaria plano antigo no portao em vez de no compile. Se um dia alguem precisar
// dessa garantia, e aqui que ela entra -- e ate entrar, ela nao existe.
//
// POR QUE NAO UM ZOD DO PLANO EM VEZ DISTO (medido, nao preferido)
//
// Um `zPlano` validaria FORMA, e `9999` e forma valida: inteiro positivo. A unica regra
// de esquema que pegaria o ataque seria uma coerencia entre campos -- e ela nao e
// trivial: em `03-prova-cena` a soma das cenas da 360 e `duracaoFrames` e 345, porque a
// transicao `fade` de 15 frames sobrepoe. Escrever essa regra no esquema e reimplementar
// `compilar()` dentro do validador, que e exatamente a segunda fonte de verdade que
// `Raiz.tsx` recusa. Hash nao precisa entender o plano para detectar que ele mudou.
//
// A ARMADILHA QUE ESTE PORTAO TEM QUE REPETIR DE PROPOSITO
//
// `compilar.mjs` sela o briefing JA PARSEADO pelo zod, nao o JSON cru -- e `zBriefing`
// tem 7 `.default()`. Hashear o arquivo cru daria um hash que NUNCA bate, e o portao
// reprovaria todo plano legitimo. Entao aqui o caminho e identico ao do compilador:
// `zBriefing.parse(JSON.parse(arquivo))` e depois `sha256Do`. Se um dia o compilador
// passar a selar outra coisa, este portao tem que mudar junto, e e por isso que os dois
// chamam a MESMA `sha256Do`, nunca duas copias da regra.

import {readFileSync} from 'node:fs';
import path from 'node:path';
import {sha256Do, sha256DoPlano} from '../briefing/impressao';
import {zBriefing} from '../briefing/esquema';

export type LaudoSelo = {
  /** true somente com os DOIS selos presentes e batendo. */
  bate: boolean;
  /** o hash do briefing em disco, parseado como o compilador o parseia */
  esperado: string;
  /** o que esta gravado em `plano._sha256Briefing` */
  encontrado: string;
  /** o hash recalculado do conteudo do plano em disco */
  esperadoPlano: string;
  /** o que esta gravado em `plano._sha256Plano` */
  encontradoPlano: string;
  /** null quando bate; a frase que o portao imprime quando reprova */
  motivo: string | null;
};

/**
 * Confere os DOIS selos do plano: o do briefing e o do proprio conteudo.
 *
 * PURO: recebe os dois objetos ja lidos, para que o teste nao precise de disco.
 *
 * A ORDEM DAS CHECAGENS E DELIBERADA. O selo do briefing vem primeiro porque ele
 * responde a pergunta mais barata de consertar (recompile) e porque, quando o briefing
 * mudou, o selo do plano ainda bate -- reportar "o plano foi editado" nesse caso
 * mandaria quem le procurar uma edicao que nao houve.
 *
 * @param briefing o briefing JA PARSEADO pelo zod -- ver o cabecalho.
 * @param plano    o objeto lido de `plano.json`.
 */
export function conferirSelo(
  briefing: unknown,
  plano: {_sha256Briefing?: unknown; _sha256Plano?: unknown},
): LaudoSelo {
  const esperado = sha256Do(briefing);
  const cru = plano._sha256Briefing;
  const cruPlano = plano._sha256Plano;
  // Recalculado SEMPRE, mesmo quando o selo do briefing ja reprovou, para o laudo poder
  // imprimir os quatro hashes e quem le ver qual dos dois divergiu.
  const esperadoPlano = sha256DoPlano(plano);
  const texto = (v: unknown) => (typeof v === 'string' ? v : String(v));
  const base = {
    esperado,
    encontrado: texto(cru),
    esperadoPlano,
    encontradoPlano: texto(cruPlano),
  };

  // Plano SEM selo nao e plano que passa: e plano que nunca foi selado. `compilar()`
  // devolve os dois campos vazios de proposito (e puro, nao importa `node:crypto`), e
  // `PLANO_VAZIO` em `Raiz.tsx` tambem. Se string vazia passasse, apagar o campo a mao
  // seria o jeito mais facil de desligar o portao -- o selo tem que reprovar por
  // ausencia, nao perdoar por ausencia. Vale para os DOIS campos: se `_sha256Plano`
  // vazio passasse, apagar essa linha do arquivo desligaria o selo novo e o ataque do
  // cetico voltaria a funcionar.
  for (const [campo, valor] of [
    ['_sha256Briefing', cru],
    ['_sha256Plano', cruPlano],
  ] as const) {
    if (typeof valor !== 'string' || valor === '') {
      return {
        ...base,
        bate: false,
        motivo:
          `o plano nao esta SELADO: \`${campo}\` esta ` +
          (valor === '' ? 'vazio' : `ausente ou nao e string (${typeof valor})`) +
          '. Um plano escrito por `scripts/compilar.mjs` sempre vem com os dois selos; ' +
          'este foi montado a mao ou veio de `compilar()` sem passar por `selarPlano()`.',
      };
    }
  }

  if (cru !== esperado) {
    return {
      ...base,
      bate: false,
      motivo:
        'o plano NAO veio deste briefing. O briefing em disco tem hash ' +
        `${esperado.slice(0, 12)}... e o plano foi selado com ${String(cru).slice(0, 12)}.... ` +
        'O briefing mudou depois do compile. ' +
        'Recompile: `scripts/compilar.mjs --projeto=<dir>`.',
    };
  }

  if (cruPlano !== esperadoPlano) {
    return {
      ...base,
      bate: false,
      motivo:
        'o CONTEUDO DO PLANO foi alterado depois de selado. O plano em disco hasheia ' +
        `${esperadoPlano.slice(0, 12)}... e carrega o selo ` +
        `${String(cruPlano).slice(0, 12)}.... O selo do briefing BATE, ou seja o ` +
        'briefing nao mudou: alguem editou `plano.json` a mao. `plano.json` e artefato ' +
        'gerado -- a edicao pertence ao `briefing.json`. Recompile: ' +
        '`scripts/compilar.mjs --projeto=<dir>`.',
    };
  }

  return {...base, bate: true, motivo: null};
}

/**
 * A casca de I/O: le `briefing.json` e `plano.json` de um projeto e confere.
 *
 * O zod roda aqui e PODE LANCAR -- de proposito. Um briefing que nao passa no esquema
 * nao tem hash definido, e devolver `bate: false` nesse caso confundiria "o selo nao
 * corresponde" com "o briefing esta quebrado", que pedem conserto diferente.
 */
export function conferirSeloDoProjeto(projeto: string): LaudoSelo & {
  caminhoBriefing: string;
  caminhoPlano: string;
} {
  const caminhoBriefing = path.join(projeto, 'briefing.json');
  const caminhoPlano = path.join(projeto, 'plano.json');
  // MESMO caminho do compilador: cru -> zod -> hash. Ver o cabecalho.
  const briefing = zBriefing.parse(JSON.parse(readFileSync(caminhoBriefing, 'utf8')));
  const plano = JSON.parse(readFileSync(caminhoPlano, 'utf8'));
  return {...conferirSelo(briefing, plano), caminhoBriefing, caminhoPlano};
}
