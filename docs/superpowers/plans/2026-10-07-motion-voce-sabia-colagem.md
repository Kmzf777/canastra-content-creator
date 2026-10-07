# Motion "Você sabia" em colagem — plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** renderizar `projetos/06-voce-sabia-especial/saida/reel.mp4` (1080×1920, 30 fps, 50,23 s) com a narração da ElevenLabs, 16 montagens de colagem e efeitos sonoros sincronizados por palavra.

**Architecture:** composição Remotion própria (`VoceSabiaColagem`) em `src/colagem/`, fora do motor por briefing, reaproveitando `identidade/`. Lógica de tempo e movimento em `.ts` puro testado com vitest; componentes em `.tsx`. Assets preparados por Python determinístico (retícula, filete, bordas) a partir de recortes gerados no ChatGPT e recortados no remove.bg; efeitos sonoros sintetizados em Python.

**Tech Stack:** Remotion 4.0.530 · React 19 · vitest · Python (uv) com PIL + numpy + cv2 · Claude in Chrome (ChatGPT, remove.bg).

Spec: `docs/superpowers/specs/2026-10-07-motion-voce-sabia-colagem-design.md`.

---

## Mapa de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `instagram/remotion/src/colagem/semente.ts` | PRNG mulberry32 por chave textual |
| `instagram/remotion/src/colagem/movimento-colagem.ts` | `assentar`, `boil`, `carimbar`, `easing` — puro |
| `instagram/remotion/src/colagem/tempos.ts` | tempos medidos da narração, em segundos, e `f()` para frames |
| `instagram/remotion/src/colagem/pecas.tsx` | `Campo`, `Recorte`, `Fita`, `Carimbo`, `Texto` |
| `instagram/remotion/src/colagem/cenas/*.tsx` | uma cena por arquivo (8) |
| `instagram/remotion/src/colagem/Sons.tsx` | `<Audio>` de narração, cama e cada efeito no seu quadro |
| `instagram/remotion/src/colagem/VoceSabia.tsx` | monta as 8 cenas em `Sequence`s |
| `instagram/remotion/src/motor/Raiz.tsx` | registra `VoceSabiaColagem` |
| `instagram/remotion/tests/colagem-*.test.ts` | testes do puro |
| `scripts/colagem_assets.py` | folha → recortes; filete, retícula, 3 bordas |
| `scripts/colagem_sfx.py` | efeitos e cama em WAV |
| `instagram/remotion/projetos/06-voce-sabia-especial/` | `public/{fonte,colagem,sfx,assets}`, `saida/` |

---

### Task 1: Projeto e material fixo

- [ ] Criar `projetos/06-voce-sabia-especial/{public/fonte,public/colagem,public/sfx,saida}`.
- [ ] Copiar a narração para `public/fonte/narracao.mp3`.
- [ ] Publicar os recortes de embalagem pelo portão: `python -m uv run python -m instagram.recorte.publicar --projeto=06-voce-sabia-especial` (nunca copiar à mão). Os PNG estão deitados (`giro_para_ficar_em_pe_graus: -90`): o giro é feito **em CSS** no componente, sem tocar pixel.
- [ ] Copiar fotos reais escolhidas para `public/fonte/`: um quadro de `cafezal/`, `cafeeiro-com-mao/IMG_1421.JPG`, um de `cereja-verde/`. Medir razão com `sondar()` (todos `Orientation 6` ou `1` — medir, não supor).

### Task 2: Lógica pura (TDD)

**Files:** `src/colagem/semente.ts`, `src/colagem/movimento-colagem.ts`, `src/colagem/tempos.ts`, `tests/colagem-movimento.test.ts`

- [ ] Teste: `semente('xicara')()` é determinístico e em [0,1); chaves diferentes dão sequências diferentes.
- [ ] Teste: `assentar(q, inicio)` → antes do início `visivel=false`; em `inicio` escala 1,04 e rotação ±4° (sinal da semente); em `inicio+6` escala 1,00 e `|rot| ≤ 0,6`; nunca escala < 0,97 (overshoot ≤ 3%).
- [ ] Teste: `boil(q, chave)` muda só a cada 3 quadros (`boil(30)==boil(31)==boil(32)`, `boil(33)` pode diferir) e devolve `variante ∈ {0,1,2}`, `rot ∈ [-0.6,0.6]`.
- [ ] Teste: `carimbar(q, inicio)` → escala 1,15 em `inicio`, 1,00 em `inicio+3`.
- [ ] Implementar; `npx vitest run tests/colagem-movimento.test.ts` verde; commit.

```ts
// semente.ts
export function semente(chave: string): () => number {
  let h = 2166136261;
  for (const c of chave) h = Math.imul(h ^ c.charCodeAt(0), 16777619);
  let a = h >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
```

### Task 3: Peças de colagem

**Files:** `src/colagem/pecas.tsx`

- [ ] `Campo({cor})` — `AbsoluteFill` com a cor e `kraft.png` em `mix-blend-mode: multiply`, opacidade 0,35.
- [ ] `Recorte({src, x, y, w, inicio, chave, rot0, sombra})` — escolhe `src` com sufixo `-b{variante}` do `boil`, aplica `assentar`, sombra `SOMBRA.papel` como `filter: drop-shadow`.
- [ ] `Fita({x,y,w,rot,inicio})`, `Carimbo({texto,x,y,rot,inicio,tamanho})`, `Texto({texto,papel,x,y,tamanho,cor,inicio,porPalavra?})`.
- [ ] `Embalagem({sku, x, y, h, inicio})` — `staticFile('assets/<sku>-250g.png')` com `rotate(-90deg)` e **nenhum filter** (sombra vai num div irmão).

### Task 4: Geração dos assets (ChatGPT)

Fluxo `canastra-conteudo` fase 3, uma conversa nova por folha, fundo branco liso, sem texto, sem rosto, sem embalagem. Folhas:

1. xícara de café cheia vista de cima + colher de prova, separadas
2. 10 grãos de café verde crus soltos + 1 grão preto quebrado, afastados
3. prato de balança de cozinha simples com punhado de grão verde, vista 3/4
4. cerejas de café soltas: 3 verdes, 3 amarelas, 3 vermelhas, afastadas
5. muda de café num saquinho preto + peneira redonda de bambu com grãos + punhado de grão torrado, separados
6. textura de papel kraft chapado (quadro inteiro); 7. papel milimetrado creme; 8. 4 tiras de fita crepe soltas

Salvar com `scripts/_pega_download.py "saida-teste/motion-06/brutos/<n>.png"` e conferir carimbo de hora.

### Task 5: Recorte e processamento

- [ ] Recortar folhas 1–5 e 8 no remove.bg; medir resolução devolvida. Se < 1000 px de lado, recortar localmente (limiar de branco + componente conexo) — fundo liso permite.
- [ ] `scripts/colagem_assets.py`: separa componentes da folha (cv2 `connectedComponentsWithStats`, área mínima), salva cada objeto; para cada um gera `-b0/-b1/-b2` = retícula (pontos de raio ∝ escuridão, grade 9 px, tinta `#14100D` sobre creme do objeto? → objeto em tom único sobre papel) + filete creme 10 px (alfa dilatado) com borda perturbada por ruído semeado (3 sementes).
- [ ] Recortes fotográficos reais (galho, mão) passam pelo mesmo filete, **sem** retícula na mão? → com retícula (não é embalagem).
- [ ] Conferir folha de recortes ampliada antes de seguir.

### Task 6: Sons

- [ ] `scripts/colagem_sfx.py` gera WAV 44,1 kHz mono em `public/sfx/`: `thump, tick, tink, rasgo, slide, pop, carimbo, ding, whoosh, vento, nota1..4, cama` (cama: pad em Ré maior + pulso suave 96 BPM, 51 s, fade in/out).
- [ ] `Sons.tsx`: narração ganho 0 dB; cama −20 dB e −12 dB sob voz (volume por quadro); cada efeito numa `Sequence` no quadro do evento.

### Task 7: Cenas e composição

- [ ] Uma cena por arquivo em `src/colagem/cenas/`, todas lendo `tempos.ts`.
- [ ] `VoceSabia.tsx` encadeia em `Sequence from={f(inicioCena)}`; transições por `Rasgo`/cobertura dentro das cenas.
- [ ] Registrar `<Composition id="VoceSabiaColagem" width={1080} height={1920} fps={30} durationInFrames={1507}/>`.
- [ ] `npx tsc --noEmit` e `npx vitest run` verdes.

### Task 8: Conferência e render

- [ ] Stills do último quadro de cada montagem → folha de contato 4×4 (pngjs). Avaliar notas 1–10; corrigir 3 piores; repetir até ≥ 8.
- [ ] Render: `npx remotion render src/index.ts VoceSabiaColagem projetos/06-voce-sabia-especial/saida/reel.mp4 --public-dir=projetos/06-voce-sabia-especial/public`.
- [ ] Normalizar: o script trabalha por projeto/plano; se não servir para peça sem plano, `loudnorm` em duas passadas com `-c:v copy`.
- [ ] Determinismo: mesmo quadro duas vezes, md5 igual. Telefone: still a 360 px.
- [ ] Lição nova no `CLAUDE.md` se algo custar rodada; commit.
