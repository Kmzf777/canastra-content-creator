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

1. Copy com gancho de tensão (fato **verificado**) → fala amigável → conteúdo → virada → marca.
2. Narração na ElevenLabs v4 (texto inteiro numa geração, tags por trecho).
3. `scripts/alinhar_narracao.py` → `palavras-whisper.json` (texto do roteiro, tempo do whisper);
   depois `python scripts/alinhar_forcado.py palavras-whisper.json <narracao> palavras.json` funde
   com o alinhamento forçado CTC (validado: erro mediano 0,02 s; o whisper sozinho deslizou 0,7 s).
   Nenhum tempo é digitado nas cenas nem no som: tudo lê a palavra com `em(faixa, 'palavra')`.
4. `roteiro.ts`: declarar em ordem o que vira colagem (`b`), o que some (`mudo`); o resto é pílula.
5. Assets: ChatGPT sobre branco liso → `scripts/colagem_assets*.py` → biblioteca → `publicar`.
6. Som: `scripts/colagem_sfx_v2.py` (efeitos + trilha em seções nos tempos medidos).
7. Conferência: `node scripts/contato.mjs <comp> <projeto> [segundos]` — folha geral e folha de
   densidade a 10 fps; nada parado por mais de ~1,5 s; texto dentro de x≈140–940; stills DENTRO
   de cada chicote (as duas imagens coladas, sem faixa preta); marcador terminando com a fala.

## Licença de técnica da série

Na série de colagem são permitidos: chicote com blur de movimento, snap zoom e tremor de
3 quadros, carimbo com até 12% de ultrapassagem, letra a letra só em Dymo/marcador/recorte.
O resto de `src/identidade/proibicoes.md` vale igual — nada por cima da embalagem, letra
sempre código, nenhum rosto sintetizado.
