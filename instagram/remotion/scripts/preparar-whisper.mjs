// Preparo do whisper.cpp local para transcricao em pt-BR.
//
// Lista REAL de modelos aceitos, lida de
// node_modules/@remotion/install-whisper-cpp/dist/download-whisper-model.d.ts
// (tipo WhisperModel), nesta versao do pacote (4.0.x):
//
//   tiny · tiny.en · base · base.en · small · small.en · medium · medium.en
//   large-v1 · large-v2 · large-v3 · large-v3-turbo
//
// Os que terminam em `.en` sao SO INGLES e nao servem para locucao em portugues.
// Multilingues: tiny, base, small, medium, large-v1, large-v2, large-v3,
// large-v3-turbo. O exemplo da documentacao oficial usa `medium.en` — nao serve.
//
// Escolha deste projeto: `small` (multilingue, 487.601.967 bytes).
// `medium` (1.533.763.059 bytes) era a primeira escolha e FALHOU com ENOSPC: em
// 30/09/2026 o disco C: tinha 1.506.627.584 bytes livres, 27 MB menos do que o
// modelo. `large-v3-turbo` e posterior ao whisper.cpp 1.5.5, que e o binario que
// o pacote baixa pronto no Windows; nao ha garantia de que aquele executavel
// carregue a arquitetura turbo.
//
// No Windows NAO ha compilacao: installWhisperCpp baixa `whisper-bin-x64` pronto
// (espelho S3 da Remotion para 1.5.5) e descompacta com Expand-Archive. O risco
// de toolchain que o plano previa nao existe nesta rota.
import {installWhisperCpp, downloadWhisperModel} from '@remotion/install-whisper-cpp';
import path from 'node:path';

// No Windows o pacote NAO compila: baixa `whisper-bin-x64` pronto e descompacta
// com Expand-Archive. Para 1.5.5 ele usa o espelho S3 da propria Remotion.
// A versao tem que ser semver aqui, senao installForWindows recusa.
export const VERSAO_WHISPER = '1.5.5';

const MULTILINGUES = [
  'tiny', 'base', 'small', 'medium',
  'large-v1', 'large-v2', 'large-v3', 'large-v3-turbo',
];

const to = path.join(process.cwd(), 'whisper.cpp');
const MODELO = process.env.WHISPER_MODELO;
if (!MODELO) {
  console.error('defina WHISPER_MODELO com um modelo MULTILINGUE:', MULTILINGUES.join(' '));
  process.exit(1);
}
if (MODELO.endsWith('.en')) {
  console.error(`modelo ${MODELO} e so ingles; a locucao e pt-BR`);
  process.exit(1);
}
if (!MULTILINGUES.includes(MODELO)) {
  console.error(`modelo ${MODELO} nao esta na lista real do tipo WhisperModel:`, MULTILINGUES.join(' '));
  process.exit(1);
}

await installWhisperCpp({to, version: VERSAO_WHISPER});
await downloadWhisperModel({folder: to, model: MODELO});
console.log('pronto:', to, MODELO, 'whisper.cpp', VERSAO_WHISPER);
