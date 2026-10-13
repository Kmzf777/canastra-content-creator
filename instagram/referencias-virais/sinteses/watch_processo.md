# Vídeos virais de PROCESSO do café (fazenda → torra) no Instagram — análise quadro a quadro

Coleta em 11/10/2026, na sessão logada do Chrome. As views são o `play_count` devolvido pela busca do próprio Instagram (`/api/v1/fbsearch/web/top_serp/`) para 23 termos, dos quais ~20 responderam antes de a aba travar (colheita de café, terreiro de café, torra de café, coffee harvest, coffee processing, how coffee is made, coffee roasting, seleção de café, optical sorter coffee, from farm to cup, processo do café, secagem de café, coffee sorting machine, a menina do café e outros). Curtidas, comentários, data e legenda vieram do yt-dlp. 21 reels baixados e analisados localmente: cortes por `select='gt(scene,0.25)'`, folha de gancho (0–6 s a 4 fps) e folha geral (24 quadros), todas olhadas; transcrição com faster-whisper `base` + VAD (o whisper.cpp `small` travou por disputa de CPU com outras sessões, ver Lacunas).

## Índice dos arquivos por vídeo (`videos/processo/`)

| # | Vídeo | Views | Tema | Formato |
|---|---|---:|---|---|
| 1 | [jesus_eliaselcampesino_c.a_DbQPPv2PPVk](../videos/processo/jesus_eliaselcampesino_c.a_DbQPPv2PPVk.md) | 29,96 mi | colheita manual, Colômbia | POV de mãos, som direto, 0 fala, 0 texto |
| 2 | [ana.paula.rodrigues018_DYZx1JxOX45](../videos/processo/ana.paula.rodrigues018_DYZx1JxOX45.md) | 25,13 mi | quanto ganha a apanhadora | selfie falada, 1 plano, dinheiro na mão |
| 3 | [tulianelenk_DZOC2OdJSgo](../videos/processo/tulianelenk_DZOC2OdJSgo.md) | 21,12 mi | separar boia e catar verde | narração off da produtora + legenda + vilão "extra forte" |
| 4 | [tannercolsoncoffee_DU6GNWQER2M](../videos/processo/tannercolsoncoffee_DU6GNWQER2M.md) | 16,51 mi | colheita → xícara (Finca Hartmann) | ASMR, 66 cortes, cold open na fermentação |
| 5 | [mistar.coffeedampit_DZopUf8xMxe](../videos/processo/mistar.coffeedampit_DZopUf8xMxe.md) | 11,22 mi | despejo após 120 h de fermentação | plano único fixo, ASMR |
| 6 | [ailliothailand_DM1thp6Rpb8](../videos/processo/ailliothailand_DM1thp6Rpb8.md) | 9,61 mi | torra completa em 18 s | time-lapse por cortes, cor pela colher de amostra |
| 7 | [terracruzcafes_DFFc826SxPF](../videos/processo/terracruzcafes_DFFc826SxPF.md) | 8,62 mi | pré-infusão (adjacente) | produtor de chapéu na lavoura, A/B |
| 8 | [karstorganics_DFe7K8yM7rZ](../videos/processo/karstorganics_DFe7K8yM7rZ.md) | 8,09 mi | despolpadora manual, Timor-Leste | 10 s, close → recua até o produtor rindo |
| 9 | [kevin_miranda_agro_Dbtvw4eB5Cz](../videos/processo/kevin_miranda_agro_Dbtvw4eB5Cz.md) | 7,24 mi | tirar a boia | pai e filho falando, 1 plano |
| 10 | [tannercolsoncoffee_DapoKiRRTkC](../videos/processo/tannercolsoncoffee_DapoKiRRTkC.md) | 5,36 mi | **repost** idêntico do #4 | — |
| 11 | [_gabriel_dcafe_DYVG9iFxLp6](../videos/processo/_gabriel_dcafe_DYVG9iFxLp6.md) | 4,02 mi | tour da via úmida | POV com dedo apontando, narração |
| 12 | [mycoffee.io_Dc_LmZjR4rN](../videos/processo/mycoffee.io_Dc_LmZjR4rN.md) | 3,03 mi | first crack só na legenda | meme (contraexemplo) |
| 13 | [tannercolsoncoffee_CwBZ3UFINrm](../videos/processo/tannercolsoncoffee_CwBZ3UFINrm.md) | 3,00 mi | torra doméstica com visor | ASMR, cor através do vidro |
| 14 | [roasterkat_DWT0E6MRoBP](../videos/processo/roasterkat_DWT0E6MRoBP.md) | 2,84 mi | natural/honey/lavado em 18 s | criadora na lavoura com uma cereja na mão |
| 15 | [geremias.brito_DcEbBtbJsH_](../videos/processo/geremias.brito_DcEbBtbJsH_.md) | 2,60 mi | torra de roça em tacho | família, fumaça, grão preto |
| 16 | [vovo_faztudo_DdaDVUCJ6Pt](../videos/processo/vovo_faztudo_DdaDVUCJ6Pt.md) | 2,27 mi | torra no fogão a lenha | avó, fogo, fumaça, grão preto |
| 17 | [fincasantaestela_DbLuf9bhF-8](../videos/processo/fincasantaestela_DbLuf9bhF-8.md) | 1,63 mi | despolpa e lavagem, Peru | ASMR cinematográfico, macros |
| 18 | [adeildo.nabike_DbBf3hosq7q](../videos/processo/adeildo.nabike_DbBf3hosq7q.md) | 1,40 mi | torra artesanal → coado de pano | 25 cortes, chama de lenha, sem fala |
| 19 | [kassianethaynaoficial__DdnPgzptYs2](../videos/processo/kassianethaynaoficial__DdnPgzptYs2.md) | 1,39 mi | "A Menina do Café" responde a hater | selfie (não é processo) |
| 20 | [robo.campo_DcRoodZJjF6](../videos/processo/robo.campo_DcRoodZJjF6.md) | 0,99 mi | robô revolvendo o terreiro | câmera no chão, 10 s |
| 21 | [nelore_tech_DYpAfxFR2qV](../videos/processo/nelore_tech_DYpAfxFR2qV.md) | 0,16 mi | classificadora por IA | tela de software + entrevista |

## Tabela comparativa

| Vídeo | Dur. | Cortes/10 s | Gancho 0–3 s (visto / escrito / dito) | Quem aparece | Narração | Texto na tela | Torra / máquina | Números | Fim / CTA |
|---|---:|---:|---|---|---|---|---|---|---|
| DbQPP (29,96 mi) | 58 s | ~0 (plano contínuo) | cacho vermelho + luvas / — / — | trabalhador, mãos | não, som direto | não | — | — | sem CTA |
| DYZx1 (25,13 mi) | 125 s | 0 | maço de notas / — / "quanto eu ganhei em uma semana" | apanhadora, rosto | sim, para a câmera | não | — | R$ 1.680/semana; R$ 30–40 por medida; 12–13 sacas/dia | "ganhei muito ou pouco?" |
| DZOC2 (21,12 mi) | 64 s | 1,7 | cerejas boiando / "Como separar o café de qualidade do café inferior 🤫" / mesma pergunta | família (voz off) | off, produtora | título + legenda | torra só citada: "torras bem escuras, já bem queimadas para disfarçar" | — | moral: café bom é marrom, sem açúcar |
| DU6GN (16,51 mi) | 100 s | 6,6 | garrafão de fermentação rosa / — / — | mãos | não, ASMR | só "(weeks later)", "(days later)" | torrador pequeno de passagem, sem fogo; despolpadora pelo material | — | latte art |
| DZopU (11,22 mi) | 19 s | 0 | tambor vai virar, líquido rosa / — / — | pés e mãos | não, ASMR | não | — | 120 h (legenda) | clímax do despejo |
| DM1th (9,61 mi) | 18 s | 4,4 | torrador bonito, grão verde entra / display / — | mão | não | display | **cor pela colher de amostra, descarga, bandeja de resfriamento; sem chama** | display tempo | resfriamento |
| DFFc8 (8,62 mi) | 62 s | 1,4 | dois filtros A/B / legenda / "ambos são o mesmo café" | produtor na lavoura | sim | legenda palavra a palavra | — | 30 s, ½ água, 3 balanços | "compartilhe" |
| DFe7K (8,09 mi) | 10 s | 0 | vermelho entra, branco sai / — / — | produtor rindo | não | não | despolpadora manual pelo material | — | loop |
| Dbtvw (7,24 mi) | 66 s | 0 | caixa d'água com boia / — / "hoje vou tirar a boia desse café, galera" | produtor e pai | sim | não | — | — | "chama no agro" |
| DYVG9 (4,02 mi) | 170 s | 1,0 | moega colorida + dedo / — / "essa é a via úmida do café" | mão do narrador | sim | blocos de texto informativos | via úmida pelo material + dedo | 2.000 L; 11,5–12% umidade; potássio | polpa vira composto |
| CwBZ3 (3,00 mi) | 48 s | 4,8 | verde → girando → torrado em 2 s / — / — | mãos | não, ASMR | não | **cor pelo visor; sem chama** | balança | shot de espresso |
| DWT0E (2,84 mi) | 18 s | 0,6 | ergue cereja / legenda palavra a palavra / "if we dry it like this, it's a natural" | criadora | sim | legenda | — | "under 20 s" | — |
| DcEbB (2,60 mi) | 113 s | ~0 | fumaça, avó no tacho / — / "pode virar, mãe?" | família | diálogo | não | **fumaça densa, lenha, grão preto** | — | humor |
| DdaDV (2,27 mi) | 59 s | 1,9 | bola de ferro, pacote de verde / — / — (música) | avó | não | não | **fornalha com chama, fumaça, grão preto** | — | lata de pó preto |
| DbLuf (1,63 mi) | 24 s | 5,8 | macro de cereja e bolhas / — / — | trabalhadores, mãos | não, ASMR | não | despolpa e lavagem pelo material | — | grão lavado nas mãos |
| DbBf3 (1,40 mi) | 38 s | 6,6 | grão verde caindo do pano / — / — | dono, avô, criança | não | não | **chama de lenha em close, fumaça, grão escuro** | — | gole na caneca esmaltada |
| DcRoo (0,99 mi) | 10 s | ~3 (visual) | robô amarelo vem até a lente / — / — | ninguém | não | não | robô no terreiro | — | — |
| DYpAf (0,16 mi) | 81 s | 0 | grãos no scanner / título / "vamos ver se funciona" | criador e fundador | sim | título fixo | classificadora pela tela do software | 95% | "chama @hope.grains" |

## 1. Quais Reels de processo do café têm mais views e em que formatos?

### Takeaway
Os mais vistos sobre processo não são de marcas nem de importadoras: são de **quem trabalha** (apanhador colombiano 29,96 mi, apanhadora mineira 25,13 mi, sítio familiar de Rondônia 21,12 mi) e de um criador que filmou uma origem em ASMR (16,51 mi). Os perfis institucionais sugeridos (Daterra) ficam na casa de mil a 174 mil views.

### Cited Findings
- Colheita manual em POV, sem fala e sem texto, 58 s: 29,96 mi views, 246.849 curtidas — [jesus_eliaselcampesino_c.a](https://www.instagram.com/reel/DbQPPv2PPVk/)
- Apanhadora contando o dinheiro da semana na colheita (R$ 1.680), 125 s em plano único: 25,13 mi views, 1.795.681 curtidas, 69.456 comentários — [ana.paula.rodrigues018](https://www.instagram.com/reel/DYZx1JxOX45/)
- Separação de boia + catação de verde com narração off da produtora, 64 s: 21,12 mi views, 968.942 curtidas — [tulianelenk](https://www.instagram.com/reel/DZOC2OdJSgo/). O mesmo perfil tem "Café boia" com 6,69 mi e "A verdade sobre o café Extra forte" com 4,94 mi (busca do Instagram, 11/10/2026).
- "Coffee from Harvesting to Brewing – ASMR" na Finca Hartmann (Panamá), 100 s: 16,51 mi views — [tannercolsoncoffee](https://www.instagram.com/reel/DU6GNWQER2M/); republicado sem alteração 5 meses depois com 5,36 mi e mais curtidas que o original (361.061 contra 336.760) — [tannercolsoncoffee repost](https://www.instagram.com/reel/DapoKiRRTkC/)
- Despejo de cereja após 120 h de fermentação lática, 19 s: 11,22 mi views mas só 33.309 curtidas e 28 comentários — [mistar.coffeedampit](https://www.instagram.com/reel/DZopUf8xMxe/)
- Torra completa em 18 s num torrador de bancada: 9,61 mi — [ailliothailand](https://www.instagram.com/reel/DM1thp6Rpb8/)
- Despolpadora manual em Timor-Leste, 10 s: 8,09 mi — [karstorganics](https://www.instagram.com/reel/DFe7K8yM7rZ/)
- Pai e filho tirando boia na caixa d'água, 66 s: 7,24 mi — [kevin_miranda_agro](https://www.instagram.com/reel/Dbtvw4eB5Cz/)
- Tour da via úmida em POV, 170 s: 4,02 mi — [_gabriel_dcafe](https://www.instagram.com/reel/DYVG9iFxLp6/)
- Fazenda de especial peruana em ASMR cinematográfico, 24 s: 1,63 mi — [fincasantaestela](https://www.instagram.com/reel/DbLuf9bhF-8/)
- No perfil da Daterra, o reel mais visto entre os 27 carregados tinha 174 mil views (DdhjaECS5vN); os demais entre 1,2 mil e 53,2 mil — [daterracoffee/reels](https://www.instagram.com/daterracoffee/reels/)
- O único vídeo de classificadora (IA) encontrado teve 0,16 mi — [nelore_tech](https://www.instagram.com/reel/DYpAfxFR2qV/)

### Inferences
- Nesta amostra, o tema que mais engaja (comentários) é o **humano** por trás do café (salário, família, insulto respondido), não o processo em si. O processo puro (ASMR, despejo) faz **alcance** com pouca conversa: DZopU tem 0,3% de curtidas/view.
- Formato de marca/importadora quase não aparece entre os virais de processo; o público reage a quem faz o trabalho, filmado com celular.

### Gaps
- Não abri os perfis @fazendaambientalfortaleza, @cafeimports e @sucafina; a Daterra foi lida só até 27 reels. O Chrome da sessão travou (a aba ficou sem responder) depois da varredura por API.
- O reel de colheita da Kassiane ("A Menina do Café") citado no briefing não foi localizado; a busca devolveu o vídeo de resposta a hater (1,39 mi).
- Não encontrei vídeo viral de **classificadora óptica** em operação; "coffee sorting machine" devolve majoritariamente máquinas de espresso.

## 2. Quais estruturas e visuais seguram a atenção?

### Takeaway
Três estruturas dominam: (a) **ASMR de transformação física** sem fala, corte de 1,5–2 s, abrindo no plano mais estranho; (b) **uma tarefa só em plano contínuo** (colher, tirar boia, despejar), 0 cortes; (c) **produtor/trabalhador falando com as próprias palavras**, com pergunta ou vilão no 1º segundo. Em todas, o gancho é imagem real em ação no quadro 1, nunca grafismo.

### Cited Findings
- O ASMR de 16,51 mi abre com o garrafão de fermentação rosa (0–1,8 s), quebrando a cronologia, e só então volta à colheita; 66 cortes em 100 s (6,6/10 s, plano médio 1,5 s); texto apenas "(weeks later)" e "(days later)" — [tannercolsoncoffee](https://www.instagram.com/reel/DU6GNWQER2M/)
- A peça peruana usa 14 cortes em 24 s (5,8/10 s), macros e câmera lenta de cereja, bolha e grão caindo na água; o emoji 🎧 na legenda sinaliza ASMR — [fincasantaestela](https://www.instagram.com/reel/DbLuf9bhF-8/)
- O "fruto à xícara" de roça usa 25 cortes em 38 s (6,6/10 s), sem fala nem texto, terminando no gole — [adeildo.nabike](https://www.instagram.com/reel/DbBf3hosq7q/)
- Os dois vídeos mais vistos têm **0 cortes detectados**: colheita contínua em POV e selfie de 125 s — [DbQPP](https://www.instagram.com/reel/DbQPPv2PPVk/); [DYZx1](https://www.instagram.com/reel/DYZx1JxOX45/)
- O vídeo de 21 mi abre com título "Como separar o café De qualidade do café inferior 🤫" e a mesma pergunta falada; nomeia um vilão ("cafés como extra forte tradicional… torras bem escuras, já bem queimadas para poder disfarçar o gosto ruim") e termina numa regra para o consumidor ("café de verdade não precisa de açúcar"; "a verdadeira cor do café de qualidade é marrom") — [tulianelenk](https://www.instagram.com/reel/DZOC2OdJSgo/)
- Um conceito técnico (natural/honey/lavado) explicado em 18 s com uma cereja na palma e legenda palavra a palavra: 2,84 mi — [roasterkat](https://www.instagram.com/reel/DWT0E6MRoBP/)
- O tour de 170 s se sustenta com POV e dedo apontando "aqui entra, aqui sai", fechando no destino da polpa (composto rico em potássio) e com números (2.000 L, 11,5–12% de umidade) — [_gabriel_dcafe](https://www.instagram.com/reel/DYVG9iFxLp6/)
- Câmera que começa no detalhe da máquina e recua até o produtor rindo, em 10 s: 8,09 mi — [karstorganics](https://www.instagram.com/reel/DFe7K8yM7rZ/)
- Duração curta e loop: 4 dos 8 mais vistos têm ≤ 19 s (DZopU 19 s, DM1th 18 s, DFe7K 10 s, DWT0E 18 s) — [mistar](https://www.instagram.com/reel/DZopUf8xMxe/), [aillio](https://www.instagram.com/reel/DM1thp6Rpb8/), [karst](https://www.instagram.com/reel/DFe7K8yM7rZ/), [roasterkat](https://www.instagram.com/reel/DWT0E6MRoBP/)
- Nenhum dos 21 vídeos usa voz sintética, colagem gráfica ou animação sobre o processo; o único com texto "de design" é a classificadora (caixa de título fixa), o de menor alcance — leitura das folhas de quadros de todos os 21 vídeos (arquivos em `videos/processo/`).

### Inferences
- O que segura é **ver a matéria mudar de estado** (cereja → polpa, verde → marrom, boia → fundo). Narração ajuda quando é **a pessoa que faz** e quando cada etapa termina numa consequência para quem bebe (DZOC2).
- Humor nos virais de processo é **situacional e real** (família discutindo se passou do ponto; "o trem roda bonito"), nunca piada roteirizada ou trocadilho externo ao café.

### Gaps
- Não ouvi o áudio; "música vs. som direto" foi inferido por VAD (ausência de fala), fator de crista e hashtag (#asmr, 🎧). Faixa musical específica não identificada.
- Retenção média e taxa de replay não são públicas; "o que segura" é inferido de views, estrutura e duração, não de curva de retenção.

## 3. Como torra e máquinas aparecem? Há fogo, chama, fumaça?

### Takeaway
Há uma divisão nítida: **fogo, fumaça e grão preto aparecem só nos vídeos de torra caseira/de roça** (tacho, fogão a lenha, torrador de manivela), onde são ritual e nostalgia. Nos vídeos de café especial, a torra é mostrada pela **cor mudando** (colher de amostra, visor de vidro), pela **descarga** e pela **bandeja de resfriamento**, sem chama. Máquinas de processo são mostradas pelo **material entrando e saindo**, nunca explicadas com gráfico.

### Cited Findings
- Torra em tacho com fumaça densa e grão preto; o diálogo gira em torno de "pegou fogo" — 2,60 mi, 4.277 comentários — [geremias.brito](https://www.instagram.com/reel/DcEbBtbJsH_/)
- Avó torrando em bola de ferro no fogão a lenha com fornalha em chamas, fumaça tomando o quadro e grão preto-oleoso batido no liquidificador — 2,27 mi — [vovo_faztudo](https://www.instagram.com/reel/DdaDVUCJ6Pt/)
- Torrador artesanal de manivela sobre lenha, close de chamas laranja, fumaça ao abrir, grão escuro, coado de pano — 1,40 mi — [adeildo.nabike](https://www.instagram.com/reel/DbBf3hosq7q/)
- Torra de especial em 18 s: a colher de amostra é puxada quatro vezes mostrando verde → amarelo → canela → marrom, com o display marcando o tempo; descarga e bandeja de resfriamento; nenhuma chama — 9,61 mi — [ailliothailand](https://www.instagram.com/reel/DM1thp6Rpb8/)
- Torra doméstica vista pelo visor de vidro com luz interna quente (verde → marrom), descarga, sem chama — 3,00 mi — [tannercolsoncoffee](https://www.instagram.com/reel/CwBZ3UFINrm/)
- No ASMR de 16,51 mi a torra ocupa poucos segundos e é sugerida pelo salto de grão verde para torrado, sem fogo — [tannercolsoncoffee](https://www.instagram.com/reel/DU6GNWQER2M/)
- O vídeo de 21 mi associa explicitamente torra escura a café ruim: "torras bem escuras, já bem queimadas para poder disfarçar o gosto ruim" — [tulianelenk](https://www.instagram.com/reel/DZOC2OdJSgo/)
- Máquinas: despolpadora (cereja vermelha entra, grão branco sai) [karstorganics](https://www.instagram.com/reel/DFe7K8yM7rZ/); via úmida, separador de boia e descascador de rolo mostrados com o dedo apontando cada saída [_gabriel_dcafe](https://www.instagram.com/reel/DYVG9iFxLp6/); robô de terreiro mostrado pelos sulcos que deixa no café [robo.campo](https://www.instagram.com/reel/DcRoodZJjF6/); classificadora por IA mostrada pela tela do software, de alcance baixo [nelore_tech](https://www.instagram.com/reel/DYpAfxFR2qV/)
- Nenhum vídeo da amostra mostra first crack com som ou palavra; o único sobre first crack é um meme com o conteúdo só na legenda — [mycoffee.io](https://www.instagram.com/reel/Dc_LmZjR4rN/)

### Inferences
- Para o público brasileiro desta amostra, **chama + fumaça na torra = café de roça, preto, queimado**. Numa marca de especial, isso comunica o produto que ela combate. É a mesma leitura que o dono/marketing tiveram da chama desenhada ("foi pro fogo") na peça da Canastra.
- Seleção e densidade são mais virais **mostradas fisicamente** (boia subindo, grão bom afundando, mão catando) do que pela máquina ou pela tela.

### Gaps
- Nenhum vídeo de cupping/prova apareceu entre os virais de processo nos termos buscados; não há dado sobre como a prova performa.
- Não encontrei vídeo viral de mesa densimétrica nem de classificadora óptica industrial em operação.

## Síntese para o Café Canastra (o que a peça rejeitada errou e o que testar)

A peça da Canastra (59 s, colagem com voz feminina de IA, do fruto à xícara, com piada do frango de padaria e chamas desenhadas sobre o torrador) usou o **assunto certo** (o vídeo de 21 mi é exatamente "processo narrado até a xícara") com **a embalagem errada**:

| Elemento da peça rejeitada | O que os virais fazem | Evidência |
|---|---|---|
| Voz feminina de IA | Voz de quem faz o trabalho, ou nenhuma voz (ASMR) | DZOC2, Dbtvw, DYVG9 (voz própria); DbQPP, DU6GN, DbLuf (sem voz) |
| Colagem gráfica sobre o processo | Imagem real em ação, sem grafismo; texto só como legenda ou marcador de tempo | todos os 21 |
| Piada externa (frango de padaria) | Humor só quando nasce da situação real | DcEbB, DYpAf |
| Chamas desenhadas no torrador ("foi pro fogo") | Especial mostra torra pela cor (colher de amostra, visor), descarga e resfriamento; fogo aparece só em torra de roça e é lido como café preto | DM1th, CwBZ3 x DcEbB, DdaDV, DbBf3; DZOC2 chama a torra escura de "queimada para disfarçar" |
| Fruto → xícara em sequência ilustrada | Cold open no plano mais estranho, depois linha reta até a xícara com corte de 1,5 s | DU6GN, DbBf3 |

Três versões a testar com a filmagem real que a Canastra já tem (cereja madura, terreiro ao pôr do sol, mesa densimétrica, mão com grão rejeitado, tambor do torrador, pessoa provando):

1. **ASMR sem narração, 30–45 s, corte de 1,5–2 s:** abrir na mesa densimétrica vibrando ou na mão com o grão rejeitado; seguir cereja → terreiro → mesa → tambor (com a cor mudando, sem fogo) → descarga → prova. Som direto.
2. **"Por que o seu café é amargo", 45–60 s, voz de alguém da fazenda:** pergunta no 1º segundo; cada etapa termina numa consequência na xícara (boia/defeito → amargor; torra escura → disfarce); fecho com a regra "café bom é marrom".
3. **Uma tarefa, um plano, 15–20 s:** só a colheita em close ou só a descarga do torrador na bandeja, em loop.

E uma regra: **nenhuma chama na representação da torra da Canastra**. Calor se mostra pela luz do visor, pela cor e pela descarga.

## Arquivos locais (scratchpad; mídia de terceiros não vai para o repositório)

`C:/Users/rafae/AppData/Local/Temp/claude/C--Users-rafae-OneDrive-Desktop-Canastra-Inteligencia-Agentes-AI-Canastra-Content-Creator/87ea359a-6b51-47aa-83bf-1d929f3af7da/scratchpad/watch-processo/` — `<id>.mp4`, `<id>_hook.jpg`, `<id>_all.jpg`, `<id>.fw.txt` (transcrição com tempos), `<id>.desc.txt` (legenda completa), `cuts.txt` (lista de cortes), `meta.txt`. Scripts em `.../scratchpad/scripts-proc/`.
