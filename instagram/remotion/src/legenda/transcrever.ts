import {transcribe, toCaptions} from '@remotion/install-whisper-cpp';
import fs from 'node:fs';
import path from 'node:path';
import type {Palavra} from './agrupar';

// Versao do whisper.cpp instalada por scripts/preparar-whisper.mjs. O
// `transcribe()` desta versao do pacote EXIGE `whisperCppVersion`: e por ela que
// ele decide o nome do executavel (`main.exe` abaixo de 1.7.4, `whisper-cli`
// a partir dai). Se divergir do que foi instalado, ele procura um .exe que nao
// existe. Mantenha igual ao VERSAO_WHISPER do script de preparo.
export const VERSAO_WHISPER = '1.5.5';

// Modelos multilingues aceitos pelo tipo WhisperModel nesta versao do pacote.
// Os terminados em `.en` sao so ingles e nao transcrevem pt-BR.
export const MODELOS_MULTILINGUES = [
  'tiny', 'base', 'small', 'medium',
  'large-v1', 'large-v2', 'large-v3', 'large-v3-turbo',
] as const;

export type ModeloMultilingue = (typeof MODELOS_MULTILINGUES)[number];

/**
 * Transcreve um WAV 16 kHz 16 bits mono em palavras com tempo.
 *
 * O WAV tem que ser 16 kHz mono: o whisper.cpp nao reamostra, ele recusa.
 * Converta com `npx remotion ffmpeg -i <src> -ar 16000 -ac 1 -c:a pcm_s16le <wav>`.
 */
export async function transcrever(
  wav16k: string,
  modelo: string,
  opcoes: {whisperPath?: string; versaoWhisper?: string} = {},
): Promise<Palavra[]> {
  if (modelo.endsWith('.en')) throw new Error(`modelo ${modelo} nao transcreve pt-BR`);
  if (!(MODELOS_MULTILINGUES as readonly string[]).includes(modelo)) {
    throw new Error(
      `modelo ${modelo} nao esta na lista multilingue: ${MODELOS_MULTILINGUES.join(' ')}`,
    );
  }
  // O transcribe() roda o main.exe com `cwd = whisper.cpp/`, entao caminho
  // relativo de entrada NAO resolve contra o cwd do processo: o binario devolve
  // "error: input file not found" e imprime o usage. Absolutize sempre.
  const entrada = path.resolve(wav16k);
  if (!fs.existsSync(entrada)) throw new Error(`WAV nao encontrado: ${entrada}`);
  const r = await transcribe({
    inputPath: entrada,
    whisperPath: opcoes.whisperPath ?? path.join(process.cwd(), 'whisper.cpp'),
    whisperCppVersion: opcoes.versaoWhisper ?? VERSAO_WHISPER,
    model: modelo as never,
    tokenLevelTimestamps: true,
    language: 'pt',
  });
  const {captions} = toCaptions({whisperCppOutput: r});
  return unirTokens(captions);
}

const SO_PONTUACAO = /^[\p{P}\p{S}]+$/u;

/**
 * Une subtokens do whisper em palavras.
 *
 * `tokenLevelTimestamps: true` devolve UM item por token, nao por palavra: a
 * locucao real saiu como `proc` `ur` `ando`, `espe` `ci` `ais`, `conos` `co`.
 * O que marca inicio de palavra e o ESPACO A ESQUERDA do texto cru do token —
 * por isso nao se pode dar `trim()` antes de unir, senao a fronteira de palavra
 * se perde e `agrupar()` monta blocos como "proc ur".
 *
 * `toCaptions()` ja remove o espaco a esquerda do PRIMEIRO item, por isso o
 * primeiro token sempre abre palavra. Pontuacao vem sem espaco a esquerda e
 * cola na palavra anterior, que e o que se quer numa legenda.
 */
export function unirTokens(
  captions: readonly {text: string; startMs: number; endMs: number}[],
): Palavra[] {
  const palavras: Palavra[] = [];
  for (const c of captions) {
    const cru = c.text;
    const limpo = cru.trim();
    if (limpo.length === 0) continue;
    const fim = c.endMs ?? c.startMs + 200;
    const abre = palavras.length === 0 || (/^\s/.test(cru) && !SO_PONTUACAO.test(limpo));
    if (abre) {
      palavras.push({texto: limpo, inicioMs: c.startMs, fimMs: fim});
      continue;
    }
    const ultima = palavras[palavras.length - 1];
    ultima.texto += limpo;
    ultima.fimMs = Math.max(ultima.fimMs, fim);
  }
  return palavras;
}
