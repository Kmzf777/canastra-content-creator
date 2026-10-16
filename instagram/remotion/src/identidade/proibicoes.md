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

## Licença da série de colagem (aprovada pelo Rafael em 07/10/2026)

Só nas peças de colagem (`src/colagem/`, `src/pecas/especial/`), para reproduzir as
referências do @_victorzk — ver `docs/motion-colagem.md`:
- chicote entre cenas, com blur DIRECIONAL de movimento (não flash, não corte seco);
- snap zoom em pulso e tremor de até 3 quadros no carimbo;
- carimbo com até 12% de ultrapassagem (1,12 → 0,97 → 1,00), nunca mola que oscila;
- letra a letra SOMENTE em etiqueta Dymo, marcador e letras recortadas — a legenda (pílula)
  continua entrando inteira, em corte seco.
Todo o resto desta página vale igual nas peças de colagem.
