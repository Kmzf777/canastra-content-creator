// Registro das composicoes.
//
// UMA COMPOSICAO POR FORMATO, UM COMPONENTE SO
//
// `Reel`, `Feed`, `Feed4x5` e `Larga` sao a MESMA peca (`Peca`) com dimensao diferente.
// Nao ha componente separado por formato de proposito: a diferenca inteira vive em
// `layout()`, que reenquadra em vez de recortar. Se um dia aparecer um "PecaFeed", o
// motor perdeu a propriedade que ele existe para ter.
//
// O FPS E A DURACAO VEM DO PLANO, NAO DE UMA CONSTANTE
//
// Antes de 01/10/2026 havia `FPS = 30` chumbado na linha 22 e `DURACAO_FRAMES = 696`
// derivado em tempo de modulo -- a peca do primeiro projeto estava escrita no registro
// das composicoes. Agora `calculateMetadata` le o `plano.json` passado por `--props` e
// devolve `fps` e `durationInFrames` dele. A consequencia: `--props` deixa de ser
// opcional para um render de verdade.
//
// A DIMENSAO NAO VEM DO PLANO
//
// Ela vem de `DIMENSAO[formato]`, fixa por composicao. Deixar o plano escolher largura
// e altura permitiria um briefing pedir 1080x1081, e nenhum portao pegaria.
//
// O PLANO NAO E VALIDADO POR ZOD AQUI, E ISSO E UMA ESCOLHA -- COM TRES RESSALVAS
//
// `plano.json` e ARTEFATO GERADO: `compilar.ts` ja o produziu a partir de um briefing
// que passou por `zBriefing` e por `refinar()`. Um segundo esquema zod espelhando
// `Plano` seria uma segunda fonte de verdade para o mesmo tipo, e divergiria no
// primeiro campo novo.
//
// Ressalva 1 -- O QUE O SELO COBRE. Sao DOIS hashes, nao um: `_sha256Briefing` (de onde
// o plano veio) e `_sha256Plano` (ele ainda e o que saiu de la). Ate 01/10/2026 havia so
// o primeiro, e esta frase dizia que ele "protege contra plano editado a mao". Nao
// protegia: um cetico gravou `duracaoFrames: 9999` preservando `_sha256Briefing` e o
// portao respondeu OK com EXIT=0 -- isto e, esta justificativa de desenho estava
// apoiada numa protecao que nao existia. Com os dois selos, a edicao a mao reprova.
//
// Ressalva 2 -- SELO NAO E ESQUEMA. O selo prova que o plano nao mudou desde o compile;
// ele nao prova que o plano tem a forma que este arquivo espera. Um plano selado e
// corrompido pelo proprio compilador seria aprovado pelo portao. A defesa contra isso
// nao e zod aqui, e `tests/briefing.test.ts` + `tsc` sobre `compilar.ts`.
//
// Ressalva 3 -- O PORTAO E DE FORA. A distincao importa: ele roda num processo de Node,
//
//   node scripts/conferir.mjs --portao=selo --projeto=projetos/<dir>
//
// e `Raiz.tsx` entra no bundle do Chrome, que nao tem `node:crypto` nem o briefing em
// disco para comparar. Um render feito sem passar pelo portao NAO esta protegido por
// nada -- nem pelo selo, nem por zod. Isto nao e uma garantia deste arquivo.

import {Composition} from 'remotion';
import React from 'react';
import {DIMENSAO, type Formato} from '../briefing/esquema';
import type {Plano} from '../briefing/compilar';
import {Peca} from './Peca';
import {PonteAssets, PONTE_PADRAO} from './PonteAssets';
import {Carta} from '../estatico/Carta';
import {VoceSabia} from '../colagem/VoceSabia';
import {DURACAO_Q as VOCE_SABIA_Q, FPS as VOCE_SABIA_FPS} from '../colagem/tempos';
import {MOLDES_ESTATICO} from '../estatico/moldes';
import {COR, TIPO} from '../identidade/tokens';
import {PILHA} from '../identidade/tipografia';

/**
 * O plano de reserva. UMA cena de terra de 1 segundo, sem evento e sem legenda.
 *
 * Um render sem `--props` sai visivelmente incompleto, que e melhor que sair com
 * conteudo de exemplo parecendo pronto: foi um placeholder que fez quatro MP4 sairem
 * com legenda inventada queimada no quadro.
 */
const PLANO_VAZIO: Plano = {
  _gerado_por: 'src/motor/Raiz.tsx (plano de reserva, nao compilado)',
  // Os dois VAZIOS: o plano de reserva nao nasceu de briefing nenhum, e o portao 0
  // reprova por ausencia. Se um dia alguem apontar o portao para este objeto, ele tem
  // que reprovar -- `PLANO_VAZIO` nao e peca.
  _sha256Briefing: '',
  _sha256Plano: '',
  serie: 'avulsa',
  fps: 30,
  formatos: ['9:16'],
  duracaoFrames: 30,
  razaoDaPeca: null,
  cenas: [
    {
      duracaoFrames: 30,
      inicioNaPecaFrames: 0,
      fonte: {tipo: 'cor', cor: COR.terra},
      aparaAntesFrames: 0,
      eventos: [],
    },
  ],
  transicoes: [],
  legenda: null,
  // `audio` e obrigatorio no briefing, e aqui as duas faixas sao null de proposito: um
  // plano de RESERVA nao tem arquivo nenhum para tocar. `refinar()` recusaria este
  // objeto -- e isso esta certo, porque ele nunca passa por `refinar()`: ele existe
  // para um render sem `--props` sair visivelmente incompleto em vez de parecer pronto.
  audio: {locucao: null, trilha: null},
  assets: [],
  licencas: {
    particulas: false,
    orbesDeBrilho: false,
    varreduraDeLuz: false,
    shockwave: false,
    molaComOvershoot: false,
    revelarCaractereACaractere: false,
    flashNoCorte: false,
    irisWipe: false,
    motionBlurBurst: false,
    swipeMarcaTexto: false,
    highlightPalavraAtiva: false,
    aceitaTempoMorto: false,
    justificativa: '',
  },
  exigePreservacao: false,
  gancho: '',
  cta: '',
  diagnostico: {eventos: [], licencasLigadas: []},
};

/** `fps` e `durationInFrames` do plano; largura e altura do formato. */
const metadados =
  (formato: Formato) =>
  ({props}: {props: Plano}) => ({
    durationInFrames: props.duracaoFrames,
    fps: props.fps,
    width: DIMENSAO[formato].largura,
    height: DIMENSAO[formato].altura,
  });

// A composicao de teste tambem desenha texto, entao tambem usa a pilha da marca. Ela e
// a tela mais barata para conferir se a tipografia carregou: `remotion still
// src/index.ts Teste <arq>` sai em segundos e a palavra CANASTRA em Archivo Black nao
// se parece com nada que o Chrome traga de casa.
const Teste: React.FC = () => (
  <div style={{flex: 1, background: '#1a1410', color: COR.creme,
               display: 'flex', alignItems: 'center', justifyContent: 'center',
               fontFamily: PILHA.manchete, fontWeight: TIPO.manchete.peso,
               fontSize: 90}}>CANASTRA</div>
);

export const Raiz: React.FC = () => (
  <>
    <Composition
      id="Reel"
      component={Peca}
      defaultProps={PLANO_VAZIO}
      calculateMetadata={metadados('9:16')}
      durationInFrames={PLANO_VAZIO.duracaoFrames}
      fps={PLANO_VAZIO.fps}
      width={DIMENSAO['9:16'].largura}
      height={DIMENSAO['9:16'].altura}
    />
    <Composition
      id="Feed"
      component={Peca}
      defaultProps={PLANO_VAZIO}
      calculateMetadata={metadados('1:1')}
      durationInFrames={PLANO_VAZIO.duracaoFrames}
      fps={PLANO_VAZIO.fps}
      width={DIMENSAO['1:1'].largura}
      height={DIMENSAO['1:1'].altura}
    />
    <Composition
      id="Feed4x5"
      component={Peca}
      defaultProps={PLANO_VAZIO}
      calculateMetadata={metadados('4:5')}
      durationInFrames={PLANO_VAZIO.duracaoFrames}
      fps={PLANO_VAZIO.fps}
      width={DIMENSAO['4:5'].largura}
      height={DIMENSAO['4:5'].altura}
    />
    {/* 16:9 e formato LATENTE, nao entrega: a margem de base dele e 51,03% da altura
        (medido). Registrado porque `layout()` o rotula e porque a serie 12 recebe corte
        de criador; nenhum briefing do catalogo o pede hoje. */}
    <Composition
      id="Larga"
      component={Peca}
      defaultProps={PLANO_VAZIO}
      calculateMetadata={metadados('16:9')}
      durationInFrames={PLANO_VAZIO.duracaoFrames}
      fps={PLANO_VAZIO.fps}
      width={DIMENSAO['16:9'].largura}
      height={DIMENSAO['16:9'].altura}
    />
    <Composition id="Teste" component={Teste}
      durationInFrames={60} fps={30} width={1080} height={1920} />

    {/* Instrumento de conferencia, nao peca: prova que `--public-dir` esta apontando
        para uma pasta que contem `assets/` e que os tres recortes carregam. 1 frame
        porque um still e tudo que ela precisa produzir. Formato deitado porque sao tres
        embalagens lado a lado -- e porque os recortes estao, eles mesmos, deitados no
        pixel: ver `rotacaoGraus` em `esquema.ts`. */}
    <Composition id="PonteAssets" component={PonteAssets}
      durationInFrames={1} fps={30} width={1920} height={1080}
      defaultProps={PONTE_PADRAO} />

    {/* Peca ESTATICA de feed, 4:5. `durationInFrames={1}` porque e still --
        mesmo padrao de PonteAssets. A dimensao sai do molde, nao digitada
        aqui: 1080x1350 esta declarado em `estatico/moldes.ts`, que e o espelho
        do catalogo Python. Digitar de novo seria a terceira fonte de verdade. */}
    {/* `fps={30}` literal, como PonteAssets: um still de 1 frame nao tem taxa, e o
        valor so existe porque `<Composition>` o exige. Nao vem do plano -- peca
        estatica nao tem plano -- nem de uma constante FPS, que deixou de existir
        em 01/10/2026 quando o fps passou a sair do `plano.json`. */}
    {/* Peca 06, colagem. Composicao propria, FORA do motor por briefing: duracao e
        fps vem de `colagem/tempos.ts`, medidos na narracao, nao de um plano.json. */}
    <Composition id="VoceSabiaColagem" component={VoceSabia}
      durationInFrames={VOCE_SABIA_Q} fps={VOCE_SABIA_FPS} width={1080} height={1920} />
    <Composition id="Carta" component={Carta}
      durationInFrames={1} fps={30}
      width={MOLDES_ESTATICO['cartao-produto'].largura}
      height={MOLDES_ESTATICO['cartao-produto'].altura}
      defaultProps={{
        molde: 'cartao-produto',
        imagem: 'assets/carta-fonte.png',
        dados: {
          preco: 'R$ 31,70',
          altitude: '1.250 m',
          local: 'Medeiros, MG',
        },
      }} />
  </>
);
