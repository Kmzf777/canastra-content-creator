# Instagram

Tudo de conteúdo orgânico de Instagram vive aqui. **Separado de `mercadolivre/`** de
propósito: lá é marketplace, preço e anúncio; aqui é audiência, formato e produção.

> Estado em 30/09/2026: pesquisa feita, planos em redação, motor ainda não construído.

---

## Onde está cada coisa

| Pasta | O que guarda |
|---|---|
| `01-concorrencia.md` | quem são os concorrentes no Instagram, cadência e engajamento medidos |
| `remotion/` | **o motor de vídeo.** Projeto Node/Remotion que renderiza Reel 9:16 e feed 1:1 |
| `estrategia/` | base de estratégia de conteúdo: ganchos, formatos, arquétipos |
| `pesquisa/` | material bruto de pesquisa — transcrições, capturas, medições |
| `assets/` | recortes, fundos e peças geradas para compor |

Os planos de implementação ficam em `docs/superpowers/plans/`.

---

## O que já foi medido

De `01-concorrencia.md`, e vale repetir porque reordena prioridade:

- **@cafecanastra publica 1 post a cada 42 dias.** O Orfeu publica a cada 2,9.
  Entre 23/05 e 25/09/2026 saiu um único post.
- A taxa de engajamento da conta (0,50%) é **melhor** que a do Coffee++, do Cafezale
  e dos três homônimos. A audiência está viva; a frequência é que não está.
- **Reel bate estático em todo perfil da amostra** — 5,2× no Sebastian, que tem um
  terço dos seguidores da Canastra. A Canastra está 69% estática.
- Três contas ocupam o nome *Serra da Canastra*, uma delas com mais seguidores que a
  marca real, e **nenhuma tem audiência viva** (0,05% a 0,28%).

---

## O motor de vídeo, em uma frase

Remotion compõe; não gera. A foto real da embalagem é recortada e **movida**, nunca
redesenhada — por isso o rótulo sobrevive. Todo texto de tela é desenhado por código.
É a resposta estrutural ao `Doodo 1985` e ao `SOSCIALTY` que este repositório já
catalogou.

### Armadilhas já pagas, não redescubra

- **`02 PL.mp4` declara 1024×576 no container e é 576×1024 na tela.** Tem
  `displaymatrix: rotation of -90°`. Quem ler `width`/`height` do metadado renderiza
  tudo deitado. Sondagem de vídeo **sempre** honra a matriz de rotação.
- **`--props` com JSON inline não funciona no shell do Windows** — as aspas somem.
  Sempre arquivo `.json`.
- **`medium.en` do Whisper é só inglês.** Locução em pt-BR exige modelo multilíngue.
- **`<CameraMotionBlur>` pode alterar cor e opacidade** por blending de camadas.
  Proibido sobre a embalagem.
- **ffmpeg e ffprobe não estão no PATH desta máquina.** O Remotion baixa os seus
  para `node_modules`; para scripts avulsos, `imageio-ffmpeg` entrega um binário.

---

## Fonte dos primeiros projetos

`remotion/projetos/01-private-label/fonte/pl.mp4` — selfie caminhando pelo galpão,
pitch de private label. 576×1024 nativo, 24,33 s, 29,96 fps.

Medido: **1,14 s de ar morto na cabeça** (corta), silêncios em 5,08 · 6,78 · 9,55 ·
13,99 · 16,02 · 17,50 · 21,52 (pontos de corte naturais), áudio médio −26 dB.
Teto de qualidade: 576 px de largura, ou seja 1,88× para chegar a 1080. Regravar em
1080×1920 elimina a ampliação sem mudar uma linha do motor.
