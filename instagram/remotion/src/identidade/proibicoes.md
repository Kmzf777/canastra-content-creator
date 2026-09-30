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
