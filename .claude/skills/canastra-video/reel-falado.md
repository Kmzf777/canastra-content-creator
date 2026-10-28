# Reel falado editado: o padrão aprovado (peça 10, "chafé: dois erros")

> O Rafael (ou quem for) grava sentado falando para a câmera; a edição põe por cima a imagem que
> prova cada frase. **Aprovado pelo dono em 28/10/2026** ("todo o processo de edição ficou muito
> bom, quero o Claude aprendendo a editar dessa maneira"), na v3, depois de duas devoluções.
> Esqueleto: `instagram/remotion/src/pecas/chafe/` (`Chafe.tsx` + `roteiro.ts`), projeto
> `instagram/remotion/projetos/10-isso-e-chafe/`. Peça nova copia este processo e esse esqueleto.
> Lições: 76 (movimento e legibilidade), 77 (três relógios), 78 (assets e embalagem).

Leia antes `estrategia.md` (o *quê*) e, para a técnica de colagem que este formato herda,
`colagem.md` §4–§8. Este formato **não** passa pelo briefing/`plano.json`.

---

## 1. A ordem do trabalho

1. **Roteiro de gravação** com frases curtas, uma ideia por frase (`roteiro-de-gravacao.md`). Grave
   os 8 primeiros segundos com a **cadeira vazia** e a câmera parada: é o fundo limpo da câmera 3D.
2. **Corte seco** (`saida/corte-seco-vN.mp4` + `.json` com `saida_ini`, `i`, `dur` por trecho).
3. **Whisper do bruto** (`palavras-<bruto>.json`) e palavras da peça. **Rode
   `scripts/sincronizar_voz_corte.py` antes de qualquer cena** (§3): ele gera `voz-sync.wav` e
   `palavras-v3.json` no relógio da imagem. Nunca confie numa `voz.wav` exportada à parte.
4. **Cor** (§4) e **recorte da pessoa** quadro a quadro (`scripts/recortar_pessoa.py`).
5. **Plano de cenas** (§5) e **assets novos** (§6). Nada reciclado de peça anterior.
6. **Código**: `roteiro.ts` (A/B: `b()` vira texto e sai da legenda, `t()` só marca tempo) e a tabela
   `E` de quadros de cada elemento (§7). Som lê a mesma tabela (§8).
7. **Conferência quadro a quadro** (§9), depois **render de 10 s do trecho que mais mudou** para o
   cliente ver, e só então o render completo + `normalizar-audio.mjs`.
8. **Entrega**: Drive `Café Canastra/Instagram/<data> - <nome>/` com `00 - Descrição do post.txt` e
   `01 - <nome>.mp4` (memória `google-drive-upload-chrome`: arquivo > 10 MB vai em partes).

## 2. As regras de movimento (o que a v1 errou e a v2 consertou, lição 76)

A v1 seguia "movimento o tempo todo, um evento a cada 0,48 s" e foi devolvida: *"movimentos
extremistas, alguns nem fazem sentido porque não dá para identificar o que apareceu, textos pouco
visíveis, principalmente carimbos, dessincronia, animações sem suavidade"*. Densidade de eventos
**não** é meta. Legibilidade é.

| # | Regra | Número |
|---|---|---|
| 1 | Entrada na curva de pouso da marca (`POUSO` de `motor/movimento.ts`, `TEMPO.pousoEasing`), com opacidade | 12 q, andando **≤ 160 px** |
| 2 | Nada de quique, mola, `back()`, objeto vindo de fora da tela (`proibicoes.md`) | ultrapassagem só no carimbo, 1,12 → 1,00 em 5 q |
| 3 | Tudo que aparece fica legível | **≥ 36 q (1,2 s) cheio**; saída 10 q acelerando (t^2,4) |
| 4 | A entrada começa **4 q antes** da palavra (`LEAD`) e assenta ~4 q depois dela | — |
| 5 | Câmera calma: push linear de +4% na cena, deriva **0,3**, pulso de 3% **só nas batidas** (5 no vídeo inteiro) | tremor só em 1–2 batidas, 6 px, 3 q |
| 6 | Troca de cena = **corte seco que assenta** (a cena nova chega 2% maior e pousa em 10 q). Sem chicote com borrão: 7 q de imagem borrada leem como travada | rasgo de papel só na virada de capítulo, 14 q |
| 7 | Corte da gravação dentro de uma cena vira **punch** (a moldura alterna 1,00 ↔ 1,10 no quadro do corte). Nunca "flip" de layout para esconder corte | lista `PUNCH` = cortes da fonte fora de ±4 q de uma troca de cena |
| 8 | **Um elemento dominante por vez.** Painel de tela dividida **nunca chega vazio**: o primeiro objeto já vem com ele | — |
| 9 | Corte entre layouts no máximo a cada ~2,5 s; nada de rajada (5–7 q por item não se identifica) | — |

## 3. Um relógio só: o da IMAGEM (lição 77)

Na peça 10 havia três relógios: a imagem; a `voz.wav`, esticada 0,76% (atrasava até 0,47 s e
**cortava a última palavra** no fim); e o `palavras-v2.json`, que adiantava até 0,23 s, e por ele
legenda, texto e som entravam antes da fala. O cliente viu como "dessincronização" e "final cortado".

- `python -I scripts/sincronizar_voz_corte.py <projeto> <fim_s>` mede o deslocamento bruto−saída de
  cada trecho **pela imagem** e refina pelo áudio do corte. Monta a voz cortando o **bruto** e relê cada
  palavra no whisper do bruto.
- `fim_s` = o fim do corte **mais ~0,85 s**: a última palavra precisa respirar. Os quadros que faltam
  saem do bruto com `scripts/recortar_pessoa.py --ss <bruto> --grade "<cor-grade.txt>"`. A emenda dá
  erro médio de ~2/255, invisível.
- **Prova no MP4 final:** correlação da voz do reel contra o áudio do corte seco, trecho a trecho. A
  meta é **≤ 1 quadro (42 ms)**. Na peça 10, era 470 ms antes e ficou em 42 ms depois. Confira também
  que a energia da voz acaba **antes** do último quadro.

## 4. Cor

- O filtro único da peça fica em `cor-grade.txt` (ffmpeg) e vale para o corte, o fundo limpo e
  qualquer quadro estendido. Peça 10: `colorbalance` puxando sombra quente e realce frio leve; `curves`
  que **seguram o branco em 0,90** (janela e parede não estouram); `vibrance` 0,22 (satura a pele sem
  estourar o que já é saturado); `eq` saturação 1,08 e contraste 1,04.
- Meta medida: **0% de pixels no branco puro** (a v1 tinha 1,9%) e pele com saturação de volta.
- Cenas "escuras" (erro) e "claras" (o nosso) mexem só no **fundo** (`escuro`/`claro` do componente
  `Rafael`). A pessoa fica com a cor dela.

## 5. Layouts e câmera 3D

- **Três planos honestos:** fundo limpo real (p 0,96), texto atrás da cabeça (p 0,98) e pessoa
  recortada (p 1). "CHAFÉ?", "ERRO 2", "NADA PRA ESCONDER" e "MANDA PRO AMIGO" atrás da cabeça foram os
  momentos mais fortes.
- **Tela cheia** · **tela dividida** (painel de 900 px em cima, pessoa embaixo, sem zoom) ·
  **círculo** (pessoa num círculo de 360 px no canto inferior direito, colagem em tela cheia).
- Posição da legenda **por layout**, declarada junto com a cena (`CENAS: [início, cena, yLegenda]`):
  1390 em tela cheia, 900 na costura da tela dividida, acima ou abaixo dos objetos no círculo. Nunca
  sobre um objeto.
- **Loop:** o fim repete o começo (a xícara e o "CHAFÉ?" voltam no mesmo lugar do quadro 0).

## 6. Assets: novos a cada peça, e embalagem só do catálogo (lição 78)

- **Sem reciclagem.** Kraft, cortiça, post-it, Dymo e lupa de papel das peças 07–09 deixaram a v1
  "parecendo os vídeos antigos, genérico". A peça 10 criou uma linguagem própria, a **"sala de prova"**:
  juta de saca, aço do torrador e papel de laudo como fundos; objetos fotográficos; texto em estêncil
  de spray e carimbo.
- **Objetos que faltam:** gere no ChatGPT pelo Chrome, isolado em fundo branco puro, foto realista de
  celular, com lista de "DO NOT INCLUDE" (texto, logo, adereço, bokeh, grade de cor). Os prompts da
  peça 10 estão em `projetos/10-isso-e-chafe/prompts-objetos-chatgpt.json` e o recorte em `scripts/recorte_limpo_10.py` (isnet
  para opacos, contorno convexo para branco sobre branco, alfa parcial para vidro).
- **Embalagem: só `saida-teste/catalogo-estudio/<N>-<produto>/<N>.1-frente-branco.png`**, recortada
  com rembg isnet. A embalagem antiga de `assets/` é de má qualidade e está proibida (Rafael,
  28/10/2026).
- **Antes de usar, pergunte se um estranho identifica o objeto em 1 s.** O "pacote de café a vácuo"
  prateado sem rótulo não parecia café e saiu. A caneca de café preto entrou no lugar.

## 7. Texto

- **Estêncil** (Archivo Black) revelado da esquerda para a direita em 8 q. Creme com sombra dupla
  sobre fundo escuro; preto com halo creme sobre fundo claro. **Nunca laranja sobre juta ou aço.**
- **Carimbo = tinta numa etiqueta de papel** (`#F3EDE1`), Archivo Black, borda da cor da tinta, filtro
  de tinta só com grão fino (`baseFrequency 0.55`, matriz `-1.3 1.8`). O filtro antigo (`0.035`) comia
  letras inteiras. **Sem mão segurando o carimbo:** ela tapava o texto e ficou congelada no freeze.
  Sobre o papel do laudo, a tinta vai direto, sem etiqueta.
- **Tag de capítulo** ("ERRO 1/2"): plaqueta escura translúcida no canto superior esquerdo (y 150),
  IBM Plex Mono 40. Legível sobre qualquer fundo.
- **Toda palavra `b()` do roteiro precisa aparecer como texto.** Na v1, "AÇÚCAR" saía da legenda e não
  entrava na tela. Confira a lista de `b()` contra as cenas.
- Texto que nasce numa palavra perto de um corte (a palavra cai 2 q antes da troca) atravessa o corte
  (componente compartilhado pelas duas cenas, como o `MaisPo`).

## 8. Som

- Ambiência de galpão a 0,05 por baixo de tudo, **sem música sob a voz**.
- Whoosh nas trocas de tela; **um som por objeto**, do Openverse (CC0, créditos em
  `public/sfx/creditos-*.json`), recortado e **alinhado pelo pico** (tabela `PICO`).
- **O pico cai no quadro em que o elemento assenta**, lido da mesma tabela `E` do visual:
  `spray(ini)` +4 q (meio da revelação), `pousa(som, ini)` +7 q (objeto a ~96% da curva), `bate(ini)`
  +2 q (carimbo encosta), `desce(q)` +6 q (painel descendo). Som com número digitado à parte descola.
- `node scripts/normalizar-audio.mjs --arquivo=<mp4>` (normaliza no lugar: copie o bruto antes). Alvo
  −14 LUFS. Se ele avisar "modo dynamic", diga ao cliente que houve limitação de pico.

## 9. Conferência quadro a quadro (antes de chamar de pronto)

1. Extraia **todos** os quadros do MP4 final em miniatura e meça o MAD quadro a quadro.
   `scripts/varrer_movimento.py` acha os saltos isolados. Um segundo com mais de 4 quadros acima de
   12 que **não** é troca de cena é suspeito.
2. Folhas de contato a **6 qps** (6×4 = 4 s por folha), com quadro e segundo escritos. Veja todas,
   cena a cena, e anote: o que aparece sem dar para identificar? Que texto não se lê? Que painel está
   vazio? O que entra antes ou depois da palavra?
3. `scripts/revisar_sincronia.py` com a palavra falada em cada quadro.
4. Stills (`renderStill`) dos pontos corrigidos, antes do render completo.
5. **Render de 10 s do trecho que mais mudou** (`--frames=a-b`) para o cliente aprovar o ritmo.
6. No MP4 final: sincronia por correlação (§3), fim da voz antes do último quadro e folha a cada 2 s.

## 10. Recursos de narrativa que funcionaram (repita a ideia, não o objeto)

- **A ideia vira transformação visível:** os três grãos com defeito **escurecem até ficarem iguais**
  no "passando do ponto", então entra "AMARGO" e o carimbo "ESCONDIDO". O café da xícara escurece no
  "intensifica". O ponteiro do manômetro **para no PONTO** em "ninguém precisa passar do ponto" e
  passa dele no erro 2.
- **Freeze em P&B** na palavra-virada ("de propósito"), com o carimbo em cor por cima e sem flash.
- **Callback:** o "+ PÓ" do fim responde ao "MAIS PÓ" do erro 1, e a tag "ERRO 1" volta no "lembra
  do primeiro erro?".

## Sinais de que você está saindo do padrão

- Algo entra de fora da tela, quica, ou fica na tela menos de 1,2 s.
- Chicote com borrão, "flip" de layout ou rajada de imagens.
- Carimbo com mão, texto laranja sobre juta ou aço, ou estêncil de 44 px.
- Uma `voz.wav` que não saiu do `sincronizar_voz_corte.py`, ou um "está sincronizado" sem
  correlação medida no MP4.
- Embalagem que não veio do `catalogo-estudio`, ou asset de peça anterior.
- Painel aparecendo vazio, ou objeto que só faz sentido para quem fez a edição.
