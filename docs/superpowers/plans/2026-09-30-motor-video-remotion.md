# Motor de vídeo Canastra (Remotion) — Plano de implementação

> **Para trabalhadores agênticos:** SUB-SKILL OBRIGATÓRIA: use `superpowers:subagent-driven-development` (recomendado) ou `superpowers:executing-plans` para implementar tarefa a tarefa. Os passos usam caixa (`- [ ]`) para acompanhamento.

**Objetivo:** construir um motor que recebe uma fonte de vídeo ou fotografia e entrega Reel 9:16 e post de feed 1:1 legendados, com motion em código, verificados por teste automático antes da entrega.

**Arquitetura:** Remotion (React) renderiza de forma determinística via Chrome headless. O layout é uma **função de zonas** que recebe `{largura, altura}` — o 1:1 não é recorte do 9:16, é a mesma timeline reenquadrada. Todo texto de tela é desenhado por código, nunca por modelo generativo. Verificação é programática: preservação de pixel, legibilidade, determinismo.

**Stack:** Node v22.16.0 · Remotion 4.x · TypeScript · `@remotion/media` · `@remotion/captions` · `@remotion/install-whisper-cpp` · Vitest · ffmpeg (embutido no Remotion)

**Licença:** Remotion é gratuito com uso comercial para pessoa física e empresas de até 3 pessoas (`remotion.pro/license`). **Se a Canastra tiver 4 ou mais pessoas, é obrigatório comprar licença antes de usar em produção.** Confirme isso na Tarefa 0.

---

## Fatos medidos que este plano assume

Levantados nesta sessão. Não re-derive.

| Fato | Valor | Onde importa |
|---|---|---|
| `02 PL.mp4` dimensão codificada | 1024×576 | **mentirosa** — ver linha abaixo |
| `02 PL.mp4` dimensão de exibição | **576×1024** (9:16 exato) | tem `displaymatrix: rotation of -90°` |
| Duração / fps | 24,33 s · 29,96 fps | h264 Baseline, 1606 kb/s |
| Ar morto na cabeça | 0 → **1,14 s** | tem que ser cortado |
| Silêncios ≥0,35 s | 5,08 · 6,78 · 9,55 · 13,99 · 16,02 · 17,50 · 21,52 | pontos de corte naturais |
| Áudio | AAC 62 kb/s · médio −26 dB · pico −3,4 dB | precisa normalizar a −14 LUFS |
| Teto de qualidade | 576 px de largura → 1,88× para 1080 | fica macio; regravar em 1080×1920 resolve |

**Armadilhas conhecidas da plataforma, já confirmadas na documentação:**

- `--props` com JSON inline **não funciona no shell do Windows** (as aspas somem). Sempre arquivo `.json`.
- `medium.en` do Whisper é **só inglês**. Locução em pt-BR exige modelo multilíngue.
- `<CameraMotionBlur>` avisa que "layered blending pode mudar cor e opacidade" — **proibido sobre a embalagem**.
- `z-index` não é suportado; ordem de camada é a ordem da árvore.
- `trimAfter` foi descontinuado em favor de `durationInFrames`.

---

## Estrutura de arquivos

```
instagram/remotion/                                    ← novo, na raiz do repositório
  package.json                            deps e scripts
  remotion.config.ts                      config de render
  vitest.config.ts
  src/
    identidade/
      tokens.ts                           paleta, tipografia, tempos, sombras
      proibicoes.md                       a lista do que nunca fazer
    motor/
      sondar.ts                           lê dimensão REAL honrando rotação
      layout.ts                           função de zonas por formato
      Raiz.tsx                            registra as composições
      PecaVideo.tsx                       a composição de vídeo+motion+legenda
      camadas/
        Fonte.tsx                         <Video> com trim
        Legenda.tsx                       legenda karaokê
        TextoTela.tsx                     manchete e kinetic type
      audio/
        normalizar.ts                     -14 LUFS, teto -1 dBTP
      legenda/
        transcrever.ts                    whisper pt-BR -> palavras com tempo
        agrupar.ts                        palavras -> blocos de no máx 2 palavras
    verificacao/
      folha.ts                            folha de contato
      telefone.ts                         render a 360px
      determinismo.ts                     mesmo frame, mesmo hash
      preservacao.ts                      pixel da embalagem intacto
      legibilidade.ts                     contraste interno e externo
  projetos/
    01-private-label/
      fonte/pl.mp4
      brief.yaml
      plano.json                          beat sheet aprovado ANTES do render
      props.json                          entrada do render (Windows exige arquivo)
      saida/
  tests/
```

---

### Tarefa 0: Fundação e licença

**Arquivos:**
- Criar: `instagram/remotion/package.json`, `instagram/remotion/remotion.config.ts`, `instagram/remotion/src/motor/Raiz.tsx`
- Modificar: `.gitignore`

- [ ] **Passo 1: Confirmar a licença com o usuário antes de qualquer código**

Pergunte, literalmente: *"Quantas pessoas trabalham na Canastra? O Remotion é gratuito para uso comercial só até 3 pessoas."* Se a resposta for 4 ou mais, **pare** e reporte que é preciso comprar licença antes de seguir. Não presuma.

- [ ] **Passo 2: Criar o projeto**

```bash
cd "C:/Users/rafae/OneDrive/Desktop/Canastra Inteligencia/Agentes AI/Canastra-Content-Creator"
mkdir -p instagram/remotion && cd instagram/remotion
npm init -y
npm i remotion @remotion/cli @remotion/media @remotion/captions @remotion/install-whisper-cpp react react-dom
npm i -D typescript @types/react @types/node vitest
```

- [ ] **Passo 3: Ignorar artefatos pesados**

Acrescente ao `.gitignore` da raiz:

```
instagram/remotion/node_modules/
instagram/remotion/out/
instagram/remotion/projetos/*/saida/
instagram/remotion/projetos/*/fonte/
instagram/remotion/whisper.cpp/
```

- [ ] **Passo 4: Composição mínima que renderiza**

`instagram/remotion/src/motor/Raiz.tsx`:

```tsx
import {Composition} from 'remotion';
import React from 'react';

const Teste: React.FC = () => (
  <div style={{flex: 1, background: '#1a1410', color: '#F1ECE0',
               display: 'flex', alignItems: 'center', justifyContent: 'center',
               fontSize: 90}}>CANASTRA</div>
);

export const Raiz: React.FC = () => (
  <Composition id="Teste" component={Teste}
    durationInFrames={60} fps={30} width={1080} height={1920} />
);
```

`instagram/remotion/src/index.ts`:

```ts
import {registerRoot} from 'remotion';
import {Raiz} from './motor/Raiz';
registerRoot(Raiz);
```

- [ ] **Passo 5: Renderizar e confirmar que o arquivo existe**

```bash
npx remotion render src/index.ts Teste out/teste.mp4
```

Esperado: baixa Chrome Headless Shell e ffmpeg na primeira vez, e grava `out/teste.mp4`. Confirme com `ls -la out/teste.mp4` que o tamanho é maior que zero. **Se o download dos binários falhar** (proxy, antivírus), pare e reporte — o pipeline inteiro depende disso.

- [ ] **Passo 6: Commit**

```bash
git add instagram/remotion/package.json instagram/remotion/src .gitignore
git commit -m "feat(video): funda o projeto Remotion e renderiza composicao minima"
```

---

### Tarefa 1: Sondagem que honra rotação

Esta é a primeira tarefa de código porque é onde o bug mais caro nasce: ler `width`/`height` do container e renderizar tudo deitado.

**Arquivos:**
- Criar: `instagram/remotion/src/motor/sondar.ts`
- Teste: `instagram/remotion/tests/sondar.test.ts`

- [ ] **Passo 1: Escrever o teste que falha**

```ts
import {describe, it, expect} from 'vitest';
import {sondar} from '../src/motor/sondar';

describe('sondar', () => {
  it('devolve a dimensao de EXIBICAO, nao a codificada', async () => {
    const r = await sondar('projetos/01-private-label/fonte/pl.mp4');
    expect(r.largura).toBe(576);
    expect(r.altura).toBe(1024);
    expect(r.rotacao).toBe(-90);
  });

  it('calcula a razao a partir da dimensao de exibicao', async () => {
    const r = await sondar('projetos/01-private-label/fonte/pl.mp4');
    expect(r.razao).toBeCloseTo(9 / 16, 4);
  });
});
```

- [ ] **Passo 2: Rodar e ver falhar**

```bash
cd instagram/remotion && npx vitest run tests/sondar.test.ts
```

Esperado: FAIL com "Cannot find module '../src/motor/sondar'".

- [ ] **Passo 3: Implementar**

```ts
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const exec = promisify(execFile);

export type Sonda = {
  largura: number; altura: number; rotacao: number;
  razao: number; duracao: number; fps: number;
};

export async function sondar(caminho: string): Promise<Sonda> {
  // ffprobe vem junto com o Remotion; ffprobe honra o displaymatrix em
  // stream=width,height APENAS a partir do v5 com -noautorotate desligado.
  // Por isso lemos a rotacao explicitamente e aplicamos nos.
  const {stdout} = await exec('npx', ['remotion', 'ffprobe', caminho,
    '-v', 'quiet', '-print_format', 'json', '-show_streams']);
  const j = JSON.parse(stdout);
  const v = j.streams.find((s: any) => s.codec_type === 'video');
  if (!v) throw new Error(`sem faixa de video em ${caminho}`);

  const rot = Number(
    v.side_data_list?.find((s: any) => s.rotation !== undefined)?.rotation ?? 0
  );
  const trocado = Math.abs(rot) === 90 || Math.abs(rot) === 270;
  const largura = trocado ? v.height : v.width;
  const altura  = trocado ? v.width  : v.height;

  const [num, den] = String(v.r_frame_rate).split('/').map(Number);
  return {
    largura, altura, rotacao: rot, razao: largura / altura,
    duracao: Number(v.duration ?? j.format?.duration ?? 0),
    fps: den ? num / den : num,
  };
}
```

- [ ] **Passo 4: Rodar e ver passar**

```bash
npx vitest run tests/sondar.test.ts
```

Esperado: PASS, 2 testes.

Se `npx remotion ffprobe` não existir nesta versão, troque por o binário que o Remotion baixou; descubra o caminho com `npx remotion versions` e ajuste. **Não** presuma que `ffprobe` está no PATH — confirmamos hoje que não está.

- [ ] **Passo 5: Commit**

```bash
git add instagram/remotion/src/motor/sondar.ts video/tests/sondar.test.ts
git commit -m "feat(video): sondagem que honra a matriz de rotacao"
```

---

### Tarefa 2: Identidade em código

**Arquivos:**
- Criar: `instagram/remotion/src/identidade/tokens.ts`, `instagram/remotion/src/identidade/proibicoes.md`

- [ ] **Passo 1: Escrever os tokens**

Os números de movimento abaixo vêm da mineração do motor `motion-vox`, que os mediu frame a frame. São ponto de partida medido, não gosto.

```ts
export const COR = {
  terra:   '#3B2A1F',   // terra vermelha da Canastra, escurecida
  creme:   '#F1ECE0',   // o creme do rótulo
  verde:   '#4A5D3A',   // folha de café
  acento:  '#C8661E',   // cereja madura — UM acento por cena
  preto:   '#14100D',
} as const;

export const TIPO = {
  manchete:  {familia: 'Archivo Black', peso: 400},
  corpo:     {familia: 'Inter', peso: 700},
  dado:      {familia: 'IBM Plex Mono', peso: 500},
} as const;

// Tempos em FRAMES a 30fps. Medidos, não escolhidos.
export const TEMPO = {
  entrada: 12,          // faixa util 8-18
  saidaExpoente: 2.4,   // aceleracao de saida t^2.4
  overshoot: 0.03,      // 2-4%
  stagger: 3,           // 2-4 frames entre elementos irmaos
  holdFinal: 12,        // 8-18
  pousoEasing: 'cubic-bezier(0.20,0.80,0.20,1.00)',
} as const;

// Push de camera: 100% -> 103..106% ao longo da cena. Nunca impacto.
export const PUSH = {de: 1.0, para: 1.04} as const;

// Sombra por material. Nunca a mesma sombra em duas camadas.
export const SOMBRA = {
  papel:       {dy: 6,  blur: 14, op: 0.15},
  cartao:      {dy: 11, blur: 24, op: 0.17},
  objetoAlto:  {dy: 20, blur: 32, op: 0.20},
  sobreVideo:  {dy: 14, blur: 26, op: 0.42},
} as const;

// Legenda, medida em referencia real: 2,45 blocos/s, 1,7 palavras/bloco.
export const LEGENDA = {
  maxPalavras: 2,
  duracaoMinFrames: 10,        // 0,33s a 30fps
  corte: 'seco',               // 93% da massa ja no 1o frame: sem easing
  entrelinha: 0.96,
  corpoEm1080: 78,
  cor: COR.creme,
} as const;

export const AUDIO = {lufs: -14, picoDbtp: -1} as const;
```

- [ ] **Passo 2: Escrever as proibições**

`instagram/remotion/src/identidade/proibicoes.md` — esta é a camada que barra o resultado genérico. Conteúdo mínimo:

```markdown
# Proibições — motor de vídeo Canastra

Barram o "look de IA" e protegem as regras da marca.

## Nunca
- Texto de tela desenhado por modelo generativo. Letra é sempre código.
- Qualquer efeito que altere pixel dentro da embalagem, incluindo
  `<CameraMotionBlur>`, glow, gradiente por cima e correção de cor local.
- Rosto de pessoa real sintetizado.
- Arquivo de `base-curada/03-mood-terceiros` ou `04-quarentena` como pixel.
- Easing elástico, brilho, gradiente em elemento de interface, explosão de
  partícula, tempo morto.
- Fundo branco puro com texto centrado — é o padrão do modelo quando não há direção.
- Revelar texto caractere a caractere.
- Aberração cromática uniforme; se usar, é radial e nula no centro.
- Flash branco instantâneo e whip pan.

## Sempre
- Um elemento dominante por cena.
- Um acento de cor por cena, com função.
- Push de câmera lento, nunca impacto.
- Grão com campo borrado (σ≈0,9) segurado por 2 frames — ruído por pixel por
  frame é incompressível e estoura o bitrate.
- Foto real entra por um registro que declara a origem (moldura, cartão, tela
  cheia), nunca como recorte flutuando.
```

- [ ] **Passo 3: Commit**

```bash
git add instagram/remotion/src/identidade
git commit -m "feat(video): identidade em codigo e lista de proibicoes"
```

---

### Tarefa 3: A função de layout

O coração do plano. É ela que faz o 1:1 ser reenquadramento e não recorte.

**Arquivos:**
- Criar: `instagram/remotion/src/motor/layout.ts`
- Teste: `instagram/remotion/tests/layout.test.ts`

- [ ] **Passo 1: Escrever o teste que falha**

```ts
import {describe, it, expect} from 'vitest';
import {layout} from '../src/motor/layout';

describe('layout', () => {
  it('no 9:16 o video ocupa a largura inteira', () => {
    const z = layout({largura: 1080, altura: 1920, razaoFonte: 9 / 16});
    expect(z.video.largura).toBe(1080);
    expect(z.video.x).toBe(0);
  });

  it('no 1:1 o video NAO e cortado na largura', () => {
    const z = layout({largura: 1080, altura: 1080, razaoFonte: 9 / 16});
    // a fonte e mais alta que larga: cabe pela altura, sobra nas laterais
    expect(z.video.altura).toBeLessThanOrEqual(1080);
    expect(z.video.largura).toBeLessThanOrEqual(1080);
    expect(z.video.largura / z.video.altura).toBeCloseTo(9 / 16, 3);
  });

  it('a legenda fica dentro da area segura em qualquer formato', () => {
    for (const [w, h] of [[1080, 1920], [1080, 1080], [1920, 1080]]) {
      const z = layout({largura: w, altura: h, razaoFonte: 9 / 16});
      expect(z.legenda.x).toBeGreaterThanOrEqual(z.seguro.x);
      expect(z.legenda.x + z.legenda.largura)
        .toBeLessThanOrEqual(z.seguro.x + z.seguro.largura);
      expect(z.legenda.y + z.legenda.altura)
        .toBeLessThanOrEqual(z.seguro.y + z.seguro.altura);
    }
  });

  it('as zonas de video e de manchete nao se sobrepoem no 1:1', () => {
    const z = layout({largura: 1080, altura: 1080, razaoFonte: 9 / 16});
    const fimVideo = z.video.x + z.video.largura;
    const cruza = z.manchete.x < fimVideo && z.manchete.x + z.manchete.largura > z.video.x;
    expect(cruza).toBe(false);
  });
});
```

- [ ] **Passo 2: Rodar e ver falhar**

```bash
npx vitest run tests/layout.test.ts
```

Esperado: FAIL, módulo não encontrado.

- [ ] **Passo 3: Implementar**

```ts
export type Caixa = {x: number; y: number; largura: number; altura: number};
export type Zonas = {
  seguro: Caixa; video: Caixa; legenda: Caixa; manchete: Caixa;
  formato: '9:16' | '1:1' | '16:9' | 'outro';
};

// Margens de area segura em 1080x1920, medidas em referencia de Reels.
const MARGEM = {topo: 90, base: 310, lado: 160};

export function layout(
  {largura, altura, razaoFonte}:
  {largura: number; altura: number; razaoFonte: number}
): Zonas {
  const k = largura / 1080;                       // escala relativa a 1080 de largura
  const seguro: Caixa = {
    x: MARGEM.lado * k,
    y: MARGEM.topo * k,
    largura: largura - 2 * MARGEM.lado * k,
    altura: altura - (MARGEM.topo + MARGEM.base) * k,
  };

  const r = largura / altura;
  const formato: Zonas['formato'] =
    Math.abs(r - 9 / 16) < 0.01 ? '9:16' :
    Math.abs(r - 1) < 0.01 ? '1:1' :
    Math.abs(r - 16 / 9) < 0.01 ? '16:9' : 'outro';

  let video: Caixa, manchete: Caixa;

  if (formato === '9:16') {
    // fonte e o quadro tem a mesma razao: preenche tudo
    video = {x: 0, y: 0, largura, altura};
    manchete = {x: seguro.x, y: seguro.y, largura: seguro.largura, altura: altura * 0.18};
  } else {
    // quadro mais largo que a fonte: o video vira uma COLUNA, nao um recorte.
    const alturaVideo = altura;
    const larguraVideo = alturaVideo * razaoFonte;
    video = {x: 0, y: 0, largura: larguraVideo, altura: alturaVideo};
    // a manchete ocupa a sobra a direita, com respiro
    const sobra = largura - larguraVideo;
    manchete = {
      x: larguraVideo + sobra * 0.08,
      y: altura * 0.12,
      largura: sobra * 0.84,
      altura: altura * 0.76,
    };
  }

  // legenda sempre ancorada no rodape da area segura, sobre o video
  const alturaLegenda = altura * 0.16;
  const legenda: Caixa = {
    x: Math.max(seguro.x, video.x + 16 * k),
    y: seguro.y + seguro.altura - alturaLegenda,
    largura: Math.min(seguro.largura, video.largura - 32 * k),
    altura: alturaLegenda,
  };

  return {seguro, video, legenda, manchete, formato};
}
```

- [ ] **Passo 4: Rodar e ver passar**

```bash
npx vitest run tests/layout.test.ts
```

Esperado: PASS, 4 testes.

- [ ] **Passo 5: Commit**

```bash
git add instagram/remotion/src/motor/layout.ts video/tests/layout.test.ts
git commit -m "feat(video): funcao de layout que reenquadra em vez de recortar"
```

---

### Tarefa 4: Agrupamento de legenda

Separado da renderização porque é lógica pura e é onde a legenda fica ilegível.

**Arquivos:**
- Criar: `instagram/remotion/src/legenda/agrupar.ts`
- Teste: `instagram/remotion/tests/agrupar.test.ts`

- [ ] **Passo 1: Escrever o teste que falha**

```ts
import {describe, it, expect} from 'vitest';
import {agrupar} from '../src/legenda/agrupar';

const palavras = [
  {texto: 'Aqui',    inicioMs: 1140, fimMs: 1380},
  {texto: 'na',      inicioMs: 1380, fimMs: 1460},
  {texto: 'Canastra',inicioMs: 1460, fimMs: 1980},
  {texto: 'a',       inicioMs: 1980, fimMs: 2040},
  {texto: 'gente',   inicioMs: 2040, fimMs: 2300},
];

describe('agrupar', () => {
  it('nunca passa de 2 palavras por bloco', () => {
    for (const b of agrupar(palavras, {fps: 30})) {
      expect(b.texto.split(' ').length).toBeLessThanOrEqual(2);
    }
  });

  it('nenhum bloco dura menos que o minimo de 10 frames', () => {
    for (const b of agrupar(palavras, {fps: 30})) {
      expect(b.fimFrame - b.inicioFrame).toBeGreaterThanOrEqual(10);
    }
  });

  it('blocos nao se sobrepoem e estao em ordem', () => {
    const bs = agrupar(palavras, {fps: 30});
    for (let i = 1; i < bs.length; i++) {
      expect(bs[i].inicioFrame).toBeGreaterThanOrEqual(bs[i - 1].fimFrame);
    }
  });

  it('preserva todas as palavras, na ordem', () => {
    const junto = agrupar(palavras, {fps: 30}).map(b => b.texto).join(' ');
    expect(junto).toBe(palavras.map(p => p.texto).join(' '));
  });
});
```

- [ ] **Passo 2: Rodar e ver falhar**

```bash
npx vitest run tests/agrupar.test.ts
```

Esperado: FAIL, módulo não encontrado.

- [ ] **Passo 3: Implementar**

```ts
import {LEGENDA} from '../identidade/tokens';

export type Palavra = {texto: string; inicioMs: number; fimMs: number};
export type Bloco = {texto: string; inicioFrame: number; fimFrame: number};

export function agrupar(palavras: Palavra[], {fps}: {fps: number}): Bloco[] {
  const blocos: Bloco[] = [];
  for (let i = 0; i < palavras.length; i += LEGENDA.maxPalavras) {
    const grupo = palavras.slice(i, i + LEGENDA.maxPalavras);
    blocos.push({
      texto: grupo.map(p => p.texto).join(' '),
      inicioFrame: Math.round((grupo[0].inicioMs / 1000) * fps),
      fimFrame: Math.round((grupo[grupo.length - 1].fimMs / 1000) * fps),
    });
  }
  // garante duracao minima empurrando o fim, e resolve a sobreposicao que
  // isso cria empurrando o inicio do proximo
  for (let i = 0; i < blocos.length; i++) {
    const b = blocos[i];
    if (b.fimFrame - b.inicioFrame < LEGENDA.duracaoMinFrames) {
      b.fimFrame = b.inicioFrame + LEGENDA.duracaoMinFrames;
    }
    const prox = blocos[i + 1];
    if (prox && prox.inicioFrame < b.fimFrame) prox.inicioFrame = b.fimFrame;
  }
  return blocos;
}
```

- [ ] **Passo 4: Rodar e ver passar**

```bash
npx vitest run tests/agrupar.test.ts
```

Esperado: PASS, 4 testes.

- [ ] **Passo 5: Commit**

```bash
git add instagram/remotion/src/legenda/agrupar.ts video/tests/agrupar.test.ts
git commit -m "feat(video): agrupamento de legenda com teto de 2 palavras"
```

---

### Tarefa 5: Transcrição em português

**Arquivos:**
- Criar: `instagram/remotion/src/legenda/transcrever.ts`, `instagram/remotion/scripts/preparar-whisper.mjs`

- [ ] **Passo 1: Descobrir os nomes de modelo aceitos antes de escolher**

Não presuma. Rode:

```bash
cd instagram/remotion && node -e "const w=require('@remotion/install-whisper-cpp'); console.log(Object.keys(w));"
```

Depois abra `node_modules/@remotion/install-whisper-cpp/dist/index.d.ts` e localize o tipo `WhisperModel`. **Anote a lista real.** O exemplo da documentação usa `medium.en`, que é **só inglês** e não serve para pt-BR. Escolha um modelo multilíngue da lista real (sem o sufixo `.en`).

- [ ] **Passo 2: Script de preparo**

`instagram/remotion/scripts/preparar-whisper.mjs`:

```js
import {installWhisperCpp, downloadWhisperModel} from '@remotion/install-whisper-cpp';
import path from 'node:path';

const to = path.join(process.cwd(), 'whisper.cpp');
const MODELO = process.env.WHISPER_MODELO;   // definido apos o Passo 1
if (!MODELO) { console.error('defina WHISPER_MODELO com um modelo MULTILINGUE'); process.exit(1); }
if (MODELO.endsWith('.en')) { console.error('modelo .en e so ingles; a locucao e pt-BR'); process.exit(1); }

await installWhisperCpp({to, version: '1.5.5'});
await downloadWhisperModel({folder: to, model: MODELO});
console.log('pronto:', to, MODELO);
```

- [ ] **Passo 3: Rodar o preparo**

```bash
WHISPER_MODELO=<o modelo multilingue que voce anotou> node scripts/preparar-whisper.mjs
```

Esperado: baixa e compila. **Se a compilação falhar no Windows** por falta de toolchain, pare e reporte — a documentação chama o pacote de multiplataforma mas não detalha o Windows, e isso é um risco conhecido deste plano.

- [ ] **Passo 4: Implementar a transcrição**

```ts
import {transcribe, toCaptions} from '@remotion/install-whisper-cpp';
import path from 'node:path';
import type {Palavra} from './agrupar';

export async function transcrever(
  wav16k: string, modelo: string
): Promise<Palavra[]> {
  if (modelo.endsWith('.en')) throw new Error('modelo .en nao transcreve pt-BR');
  const r = await transcribe({
    inputPath: wav16k,
    whisperPath: path.join(process.cwd(), 'whisper.cpp'),
    model: modelo as never,
    tokenLevelTimestamps: true,
    language: 'pt',
  });
  const {captions} = toCaptions({whisperCppOutput: r});
  return captions.map(c => ({
    texto: c.text.trim(),
    inicioMs: c.startMs,
    fimMs: c.endMs ?? c.startMs + 200,
  })).filter(p => p.texto.length > 0);
}
```

- [ ] **Passo 5: Converter o áudio e transcrever o vídeo real**

O Whisper exige WAV 16 kHz 16 bits mono:

```bash
npx remotion ffmpeg -i projetos/01-private-label/fonte/pl.mp4 -ar 16000 -ac 1 -c:a pcm_s16le projetos/01-private-label/fonte/pl.wav
```

Rode a transcrição e **leia o texto com os olhos**. Confirme que saiu em português e que as palavras batem com a fala. Grave em `projetos/01-private-label/transcricao.json`.

- [ ] **Passo 6: Commit**

```bash
git add instagram/remotion/src/legenda/transcrever.ts video/scripts/preparar-whisper.mjs instagram/remotion/projetos/01-private-label/transcricao.json
git commit -m "feat(video): transcricao pt-BR local com whisper.cpp"
```

---

### Tarefa 6: Verificação de preservação de pixel

Escrita **antes** das camadas visuais, de propósito: é o teste que impede o motor de estragar o rótulo.

**Arquivos:**
- Criar: `instagram/remotion/src/verificacao/preservacao.ts`
- Teste: `instagram/remotion/tests/preservacao.test.ts`

- [ ] **Passo 1: Escrever o teste que falha**

```ts
import {describe, it, expect} from 'vitest';
import {compararRegiao} from '../src/verificacao/preservacao';

describe('compararRegiao', () => {
  it('acusa zero diferenca entre uma imagem e ela mesma', async () => {
    const r = await compararRegiao('tests/fixtures/pacote.png',
                                   'tests/fixtures/pacote.png',
                                   {x: 0, y: 0, largura: 64, altura: 64});
    expect(r.pixelsDiferentes).toBe(0);
    expect(r.maiorDelta).toBe(0);
  });

  it('acusa diferenca quando um pixel muda', async () => {
    const r = await compararRegiao('tests/fixtures/pacote.png',
                                   'tests/fixtures/pacote-1px.png',
                                   {x: 0, y: 0, largura: 64, altura: 64});
    expect(r.pixelsDiferentes).toBeGreaterThan(0);
  });
});
```

- [ ] **Passo 2: Criar as duas fixtures**

```bash
cd instagram/remotion && mkdir -p tests/fixtures
node -e "
const {PNG}=require('pngjs'); const fs=require('fs');
const p=new PNG({width:64,height:64});
for(let i=0;i<p.data.length;i+=4){p.data[i]=200;p.data[i+1]=180;p.data[i+2]=150;p.data[i+3]=255;}
p.pack().pipe(fs.createWriteStream('tests/fixtures/pacote.png')).on('finish',()=>{
  const q=new PNG({width:64,height:64});
  for(let i=0;i<q.data.length;i+=4){q.data[i]=200;q.data[i+1]=180;q.data[i+2]=150;q.data[i+3]=255;}
  q.data[0]=0;
  q.pack().pipe(fs.createWriteStream('tests/fixtures/pacote-1px.png'));
});
"
```

Instale a dependência antes: `npm i -D pngjs`.

- [ ] **Passo 3: Rodar e ver falhar**

```bash
npx vitest run tests/preservacao.test.ts
```

Esperado: FAIL, módulo não encontrado.

- [ ] **Passo 4: Implementar**

```ts
import {PNG} from 'pngjs';
import fs from 'node:fs';

export type Regiao = {x: number; y: number; largura: number; altura: number};
export type Laudo = {pixelsDiferentes: number; maiorDelta: number; total: number};

function ler(p: string): PNG {
  return PNG.sync.read(fs.readFileSync(p));
}

export async function compararRegiao(
  origem: string, saida: string, r: Regiao, tolerancia = 0
): Promise<Laudo> {
  const a = ler(origem), b = ler(saida);
  let dif = 0, maior = 0, total = 0;
  for (let y = r.y; y < r.y + r.altura; y++) {
    for (let x = r.x; x < r.x + r.largura; x++) {
      const ia = (a.width * y + x) << 2;
      const ib = (b.width * y + x) << 2;
      const d = Math.max(
        Math.abs(a.data[ia] - b.data[ib]),
        Math.abs(a.data[ia + 1] - b.data[ib + 1]),
        Math.abs(a.data[ia + 2] - b.data[ib + 2]),
      );
      total++;
      if (d > maior) maior = d;
      if (d > tolerancia) dif++;
    }
  }
  return {pixelsDiferentes: dif, maiorDelta: maior, total};
}
```

- [ ] **Passo 5: Rodar e ver passar**

```bash
npx vitest run tests/preservacao.test.ts
```

Esperado: PASS, 2 testes.

- [ ] **Passo 6: Commit**

```bash
git add instagram/remotion/src/verificacao/preservacao.ts video/tests/preservacao.test.ts video/tests/fixtures
git commit -m "feat(video): laudo de preservacao de pixel por regiao"
```

---

### Tarefa 7: A peça de vídeo

**Arquivos:**
- Criar: `instagram/remotion/src/motor/PecaVideo.tsx`, `instagram/remotion/src/motor/camadas/Fonte.tsx`, `instagram/remotion/src/motor/camadas/Legenda.tsx`
- Modificar: `instagram/remotion/src/motor/Raiz.tsx`

- [ ] **Passo 1: Camada de fonte, com o corte do ar morto**

`instagram/remotion/src/motor/camadas/Fonte.tsx`:

```tsx
import {Video} from '@remotion/media';
import {staticFile} from 'remotion';
import React from 'react';
import type {Caixa} from '../layout';

export const Fonte: React.FC<{
  arquivo: string; caixa: Caixa; cortarAntesFrames: number;
}> = ({arquivo, caixa, cortarAntesFrames}) => (
  <div style={{position: 'absolute', left: caixa.x, top: caixa.y,
               width: caixa.largura, height: caixa.altura, overflow: 'hidden'}}>
    <Video src={staticFile(arquivo)} trimBefore={cortarAntesFrames}
           style={{width: '100%', height: '100%', objectFit: 'cover'}} />
  </div>
);
```

O corte do ar morto do `02 PL.mp4` é `Math.round(1.14 * 30) = 34` frames.

- [ ] **Passo 2: Camada de legenda**

`instagram/remotion/src/motor/camadas/Legenda.tsx`:

```tsx
import {useCurrentFrame} from 'remotion';
import React from 'react';
import {LEGENDA, COR, TIPO} from '../../identidade/tokens';
import type {Bloco} from '../../legenda/agrupar';
import type {Caixa} from '../layout';

export const Legenda: React.FC<{blocos: Bloco[]; caixa: Caixa; escala: number}> =
({blocos, caixa, escala}) => {
  const f = useCurrentFrame();
  const b = blocos.find(x => f >= x.inicioFrame && f < x.fimFrame);
  if (!b) return null;
  // corte seco de proposito: 93% da massa ja no primeiro frame. Sem easing.
  return (
    <div style={{position: 'absolute', left: caixa.x, top: caixa.y,
                 width: caixa.largura, height: caixa.altura,
                 display: 'flex', alignItems: 'flex-end', justifyContent: 'center'}}>
      <span style={{
        fontFamily: TIPO.corpo.familia, fontWeight: TIPO.corpo.peso,
        fontSize: LEGENDA.corpoEm1080 * escala, lineHeight: LEGENDA.entrelinha,
        color: LEGENDA.cor, textAlign: 'center',
        textShadow: `0 ${14 * escala}px ${26 * escala}px rgba(0,0,0,.42)`,
      }}>{b.texto}</span>
    </div>
  );
};
```

A sombra usa o valor `sobreVideo` dos tokens — é o que garante leitura sobre imagem em movimento.

- [ ] **Passo 3: A composição, com dimensão por props**

`instagram/remotion/src/motor/PecaVideo.tsx`:

```tsx
import {AbsoluteFill, useVideoConfig} from 'remotion';
import React from 'react';
import {layout} from './layout';
import {Fonte} from './camadas/Fonte';
import {Legenda} from './camadas/Legenda';
import {COR} from '../identidade/tokens';
import type {Bloco} from '../legenda/agrupar';

export type Props = {
  arquivo: string; razaoFonte: number;
  cortarAntesFrames: number; blocos: Bloco[];
};

export const PecaVideo: React.FC<Props> = (p) => {
  const {width, height} = useVideoConfig();
  const z = layout({largura: width, altura: height, razaoFonte: p.razaoFonte});
  return (
    <AbsoluteFill style={{backgroundColor: COR.terra}}>
      <Fonte arquivo={p.arquivo} caixa={z.video}
             cortarAntesFrames={p.cortarAntesFrames} />
      <Legenda blocos={p.blocos} caixa={z.legenda} escala={width / 1080} />
    </AbsoluteFill>
  );
};
```

- [ ] **Passo 4: Registrar as duas composições**

Em `Raiz.tsx`, registre `Reel` (1080×1920) e `Feed` (1080×1080), ambas apontando para `PecaVideo` e recebendo `defaultProps` com `razaoFonte: 9/16` e `cortarAntesFrames: 34`. A duração é `Math.round((24.33 - 1.14) * 30) = 696` frames.

- [ ] **Passo 5: Renderizar os dois formatos**

Lembre: **JSON inline quebra no Windows.** Escreva `projetos/01-private-label/props.json` e passe o arquivo:

```bash
npx remotion render src/index.ts Reel projetos/01-private-label/saida/reel.mp4 --props=projetos/01-private-label/props.json
npx remotion render src/index.ts Feed projetos/01-private-label/saida/feed.mp4 --props=projetos/01-private-label/props.json
```

Confirme com `sondar()` que `reel.mp4` saiu 1080×1920 e `feed.mp4` 1080×1080.

- [ ] **Passo 6: Commit**

```bash
git add instagram/remotion/src/motor
git commit -m "feat(video): peca de video com legenda nos dois formatos"
```

---

### Tarefa 8: Portões de verificação

**Arquivos:**
- Criar: `instagram/remotion/src/verificacao/folha.ts`, `instagram/remotion/src/verificacao/telefone.ts`, `instagram/remotion/src/verificacao/determinismo.ts`
- Criar: `instagram/remotion/scripts/conferir.mjs`

- [ ] **Passo 1: Folha de contato**

```bash
npx remotion ffmpeg -i projetos/01-private-label/saida/reel.mp4 -vf "fps=2,scale=180:-1,tile=6x8" -frames:v 1 projetos/01-private-label/saida/contato.png
```

2 frames por segundo, 6 de largura. **Abra e olhe de verdade.**

- [ ] **Passo 2: Teste de telefone**

```bash
npx remotion render src/index.ts Reel projetos/01-private-label/saida/telefone.mp4 --props=projetos/01-private-label/props.json --scale=0.333
```

Resulta em 360 px de largura. Se a legenda não se lê aí, ela não se lê no feed de ninguém.

- [ ] **Passo 3: Determinismo**

Renderize o mesmo still duas vezes e compare o hash:

```bash
npx remotion still src/index.ts Reel projetos/01-private-label/saida/f300a.png --frame=300 --props=projetos/01-private-label/props.json
npx remotion still src/index.ts Reel projetos/01-private-label/saida/f300b.png --frame=300 --props=projetos/01-private-label/props.json
node -e "const c=require('crypto'),f=require('fs');const h=p=>c.createHash('md5').update(f.readFileSync(p)).digest('hex');const a=h('projetos/01-private-label/saida/f300a.png'),b=h('projetos/01-private-label/saida/f300b.png');console.log(a,b,a===b?'OK':'NAO DETERMINISTICO');"
```

Esperado: `OK`. Se der diferente, há algo dependente de relógio ou de aleatoriedade sem semente — conserte antes de seguir.

- [ ] **Passo 4: Checagem de loop**

```bash
npx remotion ffmpeg -stream_loop 1 -i projetos/01-private-label/saida/reel.mp4 -c copy projetos/01-private-label/saida/loop.mp4
```

Assista à emenda. Um reel que reinicia limpo ganha reexibição.

- [ ] **Passo 5: Commit**

```bash
git add instagram/remotion/src/verificacao video/scripts/conferir.mjs
git commit -m "feat(video): portoes de verificacao antes da entrega"
```

---

### Tarefa 9: Empacotar como skill

**Arquivos:**
- Criar: `.claude/skills/canastra-video/SKILL.md`

- [ ] **Passo 1: Escrever a skill**

Frontmatter com `name: canastra-video` e uma `description` que dispare em "reel", "vídeo", "motion", "criativo", "legenda". Corpo com: as entradas a coletar antes de começar (fonte, duração alvo, gancho, CTA, formatos), o pipeline em ordem, os portões de verificação como regra dura, e o vínculo com `identidade/proibicoes.md`.

- [ ] **Passo 2: Registrar a lição da rotação**

Acrescente ao `Registro de lições` do `CLAUDE.md`, no formato sintoma → causa → regra:

> **Vídeo renderizou deitado / a matemática de recorte deu errado** → li `width/height` do container (1024×576) e ignorei o `displaymatrix: rotation of -90°`; a dimensão de exibição era 576×1024, 9:16 nativo → **sondagem de vídeo sempre honra a matriz de rotação**; a dimensão codificada não é a dimensão de exibição.

- [ ] **Passo 3: Commit**

```bash
git add .claude/skills/canastra-video CLAUDE.md
git commit -m "feat(video): empacota o motor como skill e registra a licao da rotacao"
```

---

## Verificação final

- [ ] `npx vitest run` — toda a suíte passa
- [ ] `reel.mp4` é 1080×1920 e `feed.mp4` é 1080×1080, confirmados por `sondar()`
- [ ] no `feed.mp4` a camiseta `CAFÉ& CANASTRA& QUEIJO& MINAS& AMOR` continua legível — não foi cortada
- [ ] o ar morto de 1,14 s não existe mais na saída
- [ ] a legenda se lê no render a 360 px
- [ ] o still do frame 300 tem o mesmo hash em duas renderizações
- [ ] nenhuma das proibições de `identidade/proibicoes.md` foi violada

## Riscos assumidos

1. **Compilação do whisper.cpp no Windows** não é documentada em detalhe. Se travar, o plano B é transcrever por API e alimentar o mesmo `transcricao.json` — a Tarefa 4 em diante não muda.
2. **576 px de largura é o teto da fonte.** O resultado será macio. Regravar o pitch em 1080×1920 elimina isso e não muda uma linha do motor.
3. **Download automático de Chrome e ffmpeg** pode falhar atrás de proxy ou antivírus. É a Tarefa 0 justamente para descobrir isso no primeiro minuto.
4. **Licença do Remotion** acima de 3 pessoas. Confirmado na Tarefa 0, Passo 1, antes de qualquer código.
