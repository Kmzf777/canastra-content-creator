# Motion de colagem — a série do Café Canastra

Referência de qualidade: os reels de colagem do **@_victorzk** (58 mil a 330 mil views).
Estudados quadro a quadro em 07/10/2026 (5 reels, 1080×1920, 30 fps); análises em
`raspagem/_motion-referencias/victorzk/*.analise.md` (terceiros: só texto, nunca pixel).

## O que as referências fazem (medido no pixel)

| Técnica | Medida |
|---|---|
| Gancho que **demonstra** a tese | 9 elementos em 2,75 s (≈3/s): título, papel, recorte, foto, 3 etiquetas, seta, elipse |
| Troca de objeto no mesmo eixo | a cada **0,25 s** (alicate → chave → cabo → relógio) |
| Câmera | nunca para; a colagem do gancho sobe ~180 px entre 1,75 e 2,0 s |
| Legenda A (pílula) | 345×77 px, cinza chapado, texto branco caixa alta, ~78–80% da altura, corte seco |
| Legenda B (colagem) | Dymo (caixa ~165 px, texto ~130 px, letras datilografadas na caixa), serifa itálica solta, marcador em papel rasgado, letras recortadas uma a uma, sílabas espalhadas com squash |
| A ↔ B | **uma fala vai para A ou para B, nunca as duas**; B fica na cena, A some quando B entra |
| Profundidade | papéis desfocados passando quase na lente, sombra de persiana, mural no meio |
| Transições | chicote com blur de movimento, giro com blur radial, troca de objeto no eixo |
| Batida | troca de cor do fundo no palavrão de impacto |
| Grafismos | seta preta, elipse de giz, X de marcador, asterisco, brilho de 4 pontas com raios, cruz "+" |
| Som | um efeito por entrada (papel, carimbo, pop, caneta), trilha muda de clima na virada |

## O motor (`instagram/remotion/src/colagem/`)

| Arquivo | Faz |
|---|---|
| `camera.ts` | câmera 2.5D pura: chaves, deriva de mão, pulso de snap zoom, tremor, parallax por plano |
| `palco.tsx` | `<Palco>` (câmera + chicote com blur direcional SVG) e `<Plano p>` (profundidade; p>1,4 desfoca) |
| `legenda.ts` | roteador A/B (`Roteiro.b/mudo/t`) e partição da pílula por leitura |
| `tipos.tsx` | `Dymo`, `Serifa`, `Marcador`, `Recortadas`, `Pilula` |
| `grafismos.tsx` | `Elipse`, `Seta`, `Sublinhado`, `Xis`, `Check`, `Asterisco`, `Brilho`, `Cruz` |
| `movimento-colagem.ts` | assentar, boil, carimbo (≤12%), squash, posterizar (stop-motion) |
| `fontes-colagem.ts` | Instrument Serif Italic + Permanent Marker com guarda de aplicação |

Peça de referência: `src/pecas/especial/` (peça 07, composição `EspecialColagem`).

## Fluxo de uma peça

O processo completo — copy, narração, alinhamento, roteiro em código, assets, cena, som,
conferência e descrição do post — está na skill: `.claude/skills/canastra-video/colagem.md`.
Este documento guarda só as medidas das referências e o mapa do motor.

## Licença de técnica da série

Na série de colagem são permitidos: chicote com blur de movimento, snap zoom e tremor de
3 quadros, carimbo com até 12% de ultrapassagem, letra a letra só em Dymo/marcador/recorte.
O resto de `src/identidade/proibicoes.md` vale igual — nada por cima da embalagem, letra
sempre código, nenhum rosto sintetizado.
