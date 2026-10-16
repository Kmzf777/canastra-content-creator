# Motion "Você sabia" — café especial em colagem

Aprovado pelo Rafael em 07/10/2026. Peça 06 do motor de vídeo.

## Objetivo

Reel 9:16 de reforço de marca: explica o que torna um café **especial** (duas provas da SCA)
e amarra isso à Canastra (1.250 m, só torra o que planta, desde 1985). Narração da
ElevenLabs v4 já gravada; motion em **colagem de papel** montada peça por peça, com efeitos
sonoros em cada impacto.

## Entradas fixas

| Entrada | Valor |
|---|---|
| Narração | `ElevenLabs_2026-10-07T04_07_40_Elvis…_v4.mp3` · 50,23 s · −20,1 LUFS · texto confere com o roteiro |
| Formato | 1080×1920, 30 fps, 1507 quadros |
| Paleta | terra `#3B2A1F` · creme `#F1ECE0` · verde `#4A5D3A` · cereja `#C8661E` (só veredito) · preto `#14100D` |
| Tipos | Archivo Black (manchete) · Inter Bold (rótulo) · IBM Plex Mono (número) — `src/identidade/fontes` |
| Grade | sincronia por **palavra**, medida no áudio (silêncios RMS + whisper.cpp); ver tabela de tempos |

### Tempos medidos (início de cada frase, segundos)

`0,00` Você sabia… especial (fim 3,80) · `4,18` Pois é · `4,92` pra ganhar esse nome ·
`6,24` ele passa por duas provas · `8,36` primeiro, o grão cru · `10,02` numa amostra de 350 g
(fim 12,42) · `12,66` nenhum defeito grave · `14,28` Nenhum! · `15,12` Depois · `15,90` a xícara ·
`16,78` aroma · `17,48` doçura · `18,32` acidez · `19,24` e corpo · `20,10` e a nota… oitenta
pontos (≈22,2 "oitenta", fim 23,14) · `23,48` por isso · `24,12` o Café Canastra começa… torra ·
`27,24` a 1.250 metros… · `30,68` o fruto amadurece devagar · `32,68` e guarda mais açúcar ·
`34,46` e a gente só torra… planta (fim 37,12) · `37,30` colhe e · `38,72` seleciona ·
`39,96` sem intermediário · `41,18` sem mistura · ≈`42,0` desde 1985 · `43,54` três gerações… ·
`45,88` Café Canastra · `47,14` o café que eterniza momentos (fim 49,04) · fim do arquivo 50,22.

## Linguagem visual

- Campo de cor chapado com grão de papel; cada cena **monta a partir do vazio**.
- Recortes com **filete creme** (alfa dilatado) e **borda irregular** em 3 variantes que se
  alternam (boil), sombra de contato curta.
- Recortes fotográficos de objeto viram **retícula** (halftone) monocromática.
  **Exceção: a embalagem** — entra como a foto real recortada, sem nenhum filtro.
- Fita crepe segura peças; carimbos com contorno cereja para veredito.
- Toda letra é código (fontes do motor). Nenhum texto gerado por modelo.

## Gramática de movimento

- **Assentar:** peça entra com rotação ±2–4° e escala 1,04, assenta em ~6 quadros,
  overshoot máximo de 3% (`tokens.ts`); sem elástico.
- **Boil:** a cada 3 quadros a peça troca micro-rotação (±0,6°) e variante de borda;
  semente fixa por peça (mulberry32). Nada de `Math.random`.
- **Parallax:** 3–4 planos com velocidades diferentes num deslize lento.
- **Transição:** cobertura por folha de papel ou rasgo; sem corte seco, sem fade, sem flash,
  sem whip pan (`proibicoes.md`).
- **Carimbo:** escala 1,15 → 1,0 em 3 quadros + leve tremor de 2 quadros.

## Montagens (16)

| # | Tempo | Conteúdo |
|---|---|---|
| 1a | 0,0–3,8 | xícara em retícula cai e assenta, fita prende; `NEM TODO CAFÉ` palavra a palavra |
| 1b | 3,8–4,2 | carimbo `É ESPECIAL?` torto |
| 2a | 4,2–6,2 | folha rasga ao meio: grão cru à esquerda, xícara à direita |
| 2b | 6,2–8,4 | etiquetas `PROVA 1` / `PROVA 2` com fita |
| 3a | 8,4–12,4 | prato de balança com grão verde; visor `000 → 350 g` (10,02→12,42) |
| 3b | 12,4–13,9 | 8 grãos verdes em grade, 1 por batida; grão preto quebrado entra por último |
| 3c | 13,9–15,1 | `✕` arranca o grão preto; carimbo `DEFEITOS: 0` em 14,28 |
| 4a | 15,1–16,8 | colher de prova pousa sobre a xícara |
| 4b | 16,8–19,8 | tiras AROMA/DOÇURA/ACIDEZ/CORPO cravadas em 16,78/17,48/18,32/19,24 |
| 4c | 20,1–23,5 | régua 0–100, marcador para em 80, abaixo escurece, carimbo `80+` |
| 5a | 23,5–27,2 | régua achata e vira horizonte; foto real da lavoura rasga o papel; `MUITO ANTES DA TORRA.` |
| 6a | 27,2–30,4 | 4 planos de parallax (céu, cafezal, fileiras, galho real) + altímetro até `1.250 m` |
| 6b | 30,7–34,1 | cerejas maturando verde→amarela→vermelha; `+ AÇÚCAR` |
| 7a | 34,5–39,7 | PLANTA (muda) · COLHE (mão real no cafeeiro) · SELECIONA (peneira) · TORRA (grão torrado), páginas que se empurram |
| 7b | 39,9–41,8 | carimbos `SEM INTERMEDIÁRIO.` e `SEM MISTURA.` |
| 8a | 42,0–45,9 | `1985` em números recortados (código), 3 fitas = 3 gerações |
| 8b | 45,9–50,2 | 3 pacotes reais, slogan, `loja.cafecanastra.com`; quadro final parado |

## Assets

**Reais** (`base-curada/01-real-verificada`): cafezal (`cafezal/`), mão no cafeeiro
(`cafeeiro-com-mao/`), cereja verde (`cereja-verde/`), 3 recortes de embalagem com laudo
(`instagram/assets/embalagem/*-250g.png`, girados −90°, giro sem perda).

**Gerados** (ChatGPT via Claude in Chrome, fundo liso, sem texto, sem rosto, sem rótulo):
xícara de café vista de cima · colher de prova · folha de grãos verdes soltos + 1 grão
defeituoso · prato de balança com grão verde · cerejas soltas verde/amarela/vermelha ·
muda de café · peneira com grãos · grãos torrados · textura papel kraft · textura papel
milimetrado · tiras de fita crepe.

Recorte: remove.bg (`https://www.remove.bg/pt-br/upload`); se a resolução gratuita não
servir, recorte local sobre fundo liso. Retícula, filete e bordas: script Python
determinístico.

## Áudio

Narração (ganho 0) + efeitos sonoros sintetizados em Python (thump, tick, tink, papel
rasgando, slide de papel, pop, carimbo, ding, whoosh, vento, pad) + cama musical leve
sintetizada, abaixada sob a voz. Mix final em −14 LUFS por `normalizar-audio.mjs`.
A cama é substituível por faixa da ElevenLabs Music sem mudar o resto.

## Arquitetura

O motor por briefing não tem vocabulário de colagem, então a peça é uma **composição
própria** no mesmo projeto Remotion, reaproveitando `identidade/` (tokens, fontes,
proibições):

- `src/colagem/` — componentes (`Campo`, `Recorte`, `Fita`, `Carimbo`, `Manchete`,
  `Contador`, `Tira`, `Regua`, `Rasgo`) e lógica pura testável em `.ts`
  (`semente.ts`, `movimento-colagem.ts`, `tempos.ts`).
- `src/colagem/VoceSabia.tsx` — a peça, registrada como composição `VoceSabiaColagem`.
- `projetos/06-voce-sabia-especial/` — `public/` (narração, recortes processados, sfx),
  `saida/`, `montagens.json` com os tempos.
- `scripts/colagem_assets.py` — retícula, filete, bordas irregulares, giro dos pacotes.
- `scripts/colagem_sfx.py` — efeitos e cama.

## Conferência

1. Folha de contato com o **último quadro de cada montagem** (16 células) antes do render.
2. Nota 1–10 em: gancho <1 s, legibilidade a 360 px, movimento, variedade, marca, sincronia;
   corrigir os 3 piores até tudo ≥ 8.
3. Determinismo (mesmo quadro, mesmo md5), loudness −14 LUFS, telefone a 360 px.
4. Pacote: nenhum filtro sobre o recorte (conferir que o PNG publicado é o do laudo).

## Fora de escopo

Versões 1:1 e 4:5; legenda queimada (a fala já vira manchete); trilha licenciada.
