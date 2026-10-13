# Estratégia de vídeo — o que decidir ANTES de escrever copy ou abrir o motor

Este arquivo é a camada de decisão da skill: formato, gancho, voz, roteiro, música, edição,
marca, CTA e medição. O resto da skill (motor, briefing, colagem, portões) diz **como executar**;
aqui está **o que fazer**. Tudo abaixo saiu de 130 vídeos virais analisados quadro a quadro em
`instagram/referencias-virais/` (72 de café, 58 de motion de marca) e da reprovação do Reel 08
(lição 66). Cada regra tem a ficha que a prova; conteste com evidência, não com gosto.

**Princípio:** quem viraliza no café é quem trabalha, filmado de verdade. Motion é uma camada
fina sobre material real (explicar um número, comprimir um tempo, celebrar um objeto real),
nunca o substituto da fazenda, da pessoa ou da embalagem.

## 0. Primeiro passo obrigatório: 3 referências

Antes de qualquer roteiro, busque na biblioteca e **cite no planejamento** 3 fichas do mesmo
formato ou etapa, dizendo o que cada uma empresta (gancho, estrutura, edição, som):

```bash
python scripts/indice_referencias.py buscar torra cor-do-grao
python scripts/indice_referencias.py buscar produtor-fala supermercado
python scripts/indice_referencias.py buscar stop-motion-real
```

Leia a seção 2 (gancho) e 4 (edição) da ficha, não só a lição. Peça animada: leia também
`instagram/referencias-virais/relatorio-motion.md` (receita e tabela de técnicas).

## 1. Escolha o formato pela matéria que você tem

| Formato | Quando | Duração | Voz | Referências |
|---|---|---|---|---|
| **Processo sem voz (ASMR de transformação)** | há filmagem de matéria mudando (cereja → polpa, verde → marrom, boia → fundo) | 10–45 s | nenhuma; som direto | `processo/tannercolsoncoffee_DU6GNWQER2M` (16,5 mi), `processo/ailliothailand_DM1thp6Rpb8` (9,6 mi) |
| **Pessoa da casa explica com as próprias palavras** | há alguém da fazenda/torrefação disposto a falar 30–60 s | 35–65 s | humana, de quem aparece | `processo/tulianelenk_DZOC2OdJSgo` (21,1 mi), `brasil/felipebrazza_DFf3isuuhcS` |
| **Vilão × herói (comparação)** | há um mito do consumidor a desfazer (extraforte, "chafé", gôndola) | 35–45 s | humana | `brasil/cafegeracoes_DVobHGpAW2Y` (5,5 mi), `brasil/cafegeracoes_CqGC2e7g5nf` (13,1 mi) |
| **Uma tarefa, um plano** | um gesto que se sustenta sozinho (colher, despejar, puxar a colher de amostra) | 10–20 s, loop | nenhuma | `processo/jesus_eliaselcampesino_c.a_DbQPPv2PPVk` (29,96 mi) |
| **Motion como camada** | há um número, um tempo ou uma transformação que a câmera não mostra sozinha | 6–22 s (efeito) | humana ou nenhuma | ver §6 e `relatorio-motion.md` |
| **Bastidor** | toda produção com ofício visível (a própria gravação, a torra, a seleção) | 15–60 s | humana | `motion-3d-fooh/alexgrimadesign_DTnC1O2DjKg` (14,4 mi) |

**Colagem narrada de ponta a ponta (estilo da peça 07) é exceção**, não formato padrão: os 130
virais não a usam, e os reels mais vistos do próprio @_victorzk são filmagem real com palavra na
tela (`motion-criadores/_victorzk_DY0HBzhNx69`). Só use com pedido explícito do cliente; aí siga
`colagem.md`.

## 2. Gancho (0–3 s)

Três camadas chegam juntas: **imagem** real em ação no quadro 0, **texto** na tela (para quem
assiste mudo) e **fala** — e a frase nega ou questiona o que a imagem parece ser.

| Tipo que funciona | Exemplo |
|---|---|
| Objeção do público escrita | "Não é CHAFÉ!" com as duas canecas (`brasil/cafegeracoes_DVobHGpAW2Y`) |
| Promessa de separar bom de ruim | "Como separar o café de qualidade do inferior 🤫" (`processo/tulianelenk_DZOC2OdJSgo`) |
| Plano mais estranho primeiro, sem contexto | fermentação rosa antes da colheita (`influenciadores/tannercolsoncoffee_DU6GNWQER2M`) |
| Número verdadeiro e contraintuitivo | "Coffee is 98.5% water" (`influenciadores/morgandrinkscoffee_DbgXMlIhWpw`) |
| Ação real já acontecendo | o tombo na colheita (`brasil/kassianethaynaoficial__C8XugrWh_-n`) |
| Imperativo de consumidor | "Não compre café ruim pra sua casa nunca mais" (`brasil/_noudaniel_DVMF38UgD0M`) |

Proibido no gancho: logo, cartela de título, saudação, "fica até o fim", frase que só descreve o
que se vê. **Teste da leitura literal:** congele o quadro de 0,5 s — o que alguém que não entende
de café lê nele, sem som? Chama lê "queimado"; render dourado lê "gerado".

## 3. Voz

- **Padrão: voz humana de quem aparece** (alguém da casa) **ou nenhuma voz** (som direto).
  Nenhum dos 130 virais usa narrador sintético como voz de marca; voz percebida como IA reduz
  confiança, e procedência é o argumento da Canastra.
- **ElevenLabs só com pedido explícito do cliente**, nunca por padrão "porque o motor tem". Se
  usar: rótulo de IA ligado na publicação e a legenda do post diz que a narração é gerada.
- Sem pessoa disponível para falar? Escolha um formato **sem voz** (processo, uma tarefa), não
  uma voz sintética.

## 4. Copy e roteiro

| Regra | Prova |
|---|---|
| **Cada etapa termina numa consequência na xícara ou na compra de quem assiste** ("as boias viram extraforte", "o verde traz amargor") | `processo/tulianelenk_DZOC2OdJSgo` |
| **O vilão é o produto do outro** (extraforte, torra excessiva para disfarçar defeito), nunca o consumidor. Fale "não é fraco, é torra média" | `brasil/cafegeracoes_DVobHGpAW2Y` |
| **A tese não pode acusar um SKU da Canastra.** Antes de qualquer frase sobre torra ("escuro esconde defeito", "o nosso para no marrom"), confira a torra **real** de cada produto (Clássico, Suave, Canela, cápsulas) com o cliente; se algum for mais escuro, o vilão vira "torra excessiva **para disfarçar defeito**" (o motivo), nunca "café escuro/preto" (a cor) | `colagem.md` §2; `processo/tulianelenk_DZOC2OdJSgo` |
| **Fato sobre pessoa, papel ou história da casa** (quem torra, "minha família desde 1985", onde fica cada etapa) é marcador `[confirmar]` até o cliente confirmar — nunca fala pronta | lição 30 |
| **Um número verdadeiro por etapa** (1.250 m, dias de terreiro, umidade, % descartado), conferido com a fazenda antes de gravar; adjetivo não é prova | `brasil/felipebrazza_DFf3isuuhcS` |
| **Humor só de dentro do café** (preparo, sabor, o ofício, a vida da fazenda). Teste: tire o café — se a piada fica de pé, corte | lição 66; `marcas/starbucks_DdRM4oglV5o` |
| **Sem autodepreciação da competência** ("é técnica, juro") — reduz a percepção de competência justo onde a peça quer provar | relatório §Reel 08 |
| **Torra: vocabulário proibido** — "fogo", "queimar", "foi pro fogo", "tostar até escurecer", emoji 🔥. Diga cor (verde → canela → marrom), ponto, doce, chocolate, caramelo, "torra média" | lição 66; `processo/ailliothailand_DM1thp6Rpb8` |
| **Uma ideia que cabe numa frase.** Se não couber, é catálogo — divida em série | `relatorio-motion.md` §receita |
| **Frase repetível** (até ~15 palavras, antítese) e o fim volta ao começo | `copy` da peça 07 |

Estrutura de fala em vídeo com voz: gancho → promessa → etapas (cada uma com consequência e
número) → virada → xícara na mão. Kishōtenketsu e o relógio por duração continuam valendo
(`instagram/estrategia/03-roteiro.md`); o que muda é a matéria: real, não colagem.

## 5. Música e som

| Situação | O que fazer | Prova |
|---|---|---|
| **Pessoa falando** | **sem música sob a fala** (nenhum vencedor brasileiro de café põe); trilha só nas respirações, no b-roll entre falas e no fecho | `brasil/*` (relatório §ritmo) |
| **Sem voz, processo** | **som direto** é o protagonista (tambor girando, grãos caindo, slurp); música, se houver, baixa e sem voz | `processo/tannercolsoncoffee_DU6GNWQER2M` |
| **Sem voz, efeito/motion** | música **fechada antes de editar**, mapeada em seções; corte e troca de cor **na batida** | `motion-criadores/jrcanest_C2As5K3v-hy`, `motion-criadores/ordinaryfolkco_DOoqmy2ErVK`, `motion-criadores/buck_design_DXW3HSxjZu-` |
| **Efeitos** | um efeito por evento visual, sincronizado; nunca estalo de fogueira, chiado de chama ou "crack" sintético na torra | lição 66 |

O áudio se fecha **antes** da imagem: narração real gravada ou trilha escolhida, e a edição
obedece ao mapa dela (lições 56–57 para fala; `scripts/colagem_sfx_v2.py` para seções). Conta
comercial: trilha licenciada ou sintetizada por nós, queimada no arquivo; não dependa do "áudio
em alta" do Instagram.

## 6. Edição

- **Duas famílias que funcionam:** (a) **transformação física sem voz**, plano de ~1,5 s,
  5–7 cortes por 10 s, som direto; (b) **pessoa falando**, poucos cortes, legenda queimada
  palavra a palavra, palavra-chave acesa na sílaba. Ritmo de corte sozinho não segura: o que
  segura é a matéria mudando ou a pessoa falando (`motion-marcas/duolingo_Dd1_il8hdbC`, 0,9 corte
  por 10 s e 11,4% de curtidas).
- **Máquina aparece pelo material entrando e saindo**, com dedo apontando ou câmera recuando
  até a pessoa; tela de software e grafismo explicativo não rendem
  (`processo/nelore_tech_DYpAfxFR2qV` 0,16 mi × `processo/karstorganics_DFe7K8yM7rZ` 8 mi).
- **Terreiro em câmera baixa**, no nível do café (`processo/robo.campo_DcRoodZJjF6`).
- **Torra pela cor real**: colher de amostra puxada várias vezes, visor, descarga, bandeja de
  resfriamento. **Nunca recolorir nem gerar grão para simular a torra** — transformação simulada
  é fabricar o processo; fotografe as amostras reais no mesmo enquadramento.
- **Motion só como camada**, com as cinco técnicas de melhor retorno que o motor já faz:
  palavra grande na sílaba falada sobre filmagem real; parallax 2.5D de foto real (sem foco
  falso); escada de escala para um número; loop com um único elemento vivo sobre quadro parado;
  bastidor em tela dividida. **Um parâmetro animado por vez**; o produto fica parado e
  verdadeiro (`motion-marcas/mcdonalds_Db5wAxRphn9`, `motion-brasil/havaianas_Ddmprvdt3ZF`).
- **Proibido**: pacote em 3D ou gerado, FOOH, mascote inventado, vídeo gerado por IA, grão
  preto, chama, fumaça. Colagem: no máximo 1–2 cartões pontuando uma peça real.
- **Fecho na xícara na mão** e último quadro que emenda no primeiro (loop).

## 7. Marca, CTA e legenda do post

- **Marca ou pessoa da Canastra visível nos primeiros 5 s e de novo no fim** (pacote real na
  mão, o galpão, quem trabalha). Marca + mensagem em 5 s = 1,7× mais chance de topo em intenção
  de compra. Exceção: peça narrada por criador conhecido, em que a marca entra como resposta
  depois da metade (`motion-criadores/_victorzk_DcMaCPgtjBH`).
- **CTA de envio** dito ou escrito ("manda pra quem acha que café bom é preto") — envio é o
  sinal que mais leva a não seguidores; "salvar" vem junto quando a peça é utilidade.
- Legenda do post: primeira linha ≤ ~55 caracteres com a pergunta que as pessoas buscam; a
  colinha do vídeo; uma pergunta aberta; ≤ 5 hashtags; nunca "comenta X que eu te mando";
  nenhum emoji de fogo. Molde em `colagem.md` §9.

## 8. Planejar em série e medir

- Pense em **formato repetível**, não em "um viral": série com nome, mesmo roteiro com outra
  pessoa, o mesmo corte republicado meses depois (`processo/tannercolsoncoffee_DapoKiRRTkC`
  somou +5,36 mi republicado igual).
- **Trial Reels** (só para não seguidores) para testar uma reformulação antes da base.
- **Medição em 7 dias**: curtidas ÷ views **≥ 3%** = sinal de orgânico; abaixo de 0,1% é
  mídia paga. Some comentários coerentes com as curtidas e o **múltiplo da mediana da própria
  grade** (meta realista: 3–5× a mediana, não "viralizar"). Impulsionado se mede à parte.
- Leia os comentários: **uma** leitura de "queimado/forte" reprova a abordagem da torra.

## Sinais de que você está saindo da estratégia

| Pensamento | Realidade |
|---|---|
| "O motor tem ElevenLabs, então narro com IA" | Voz padrão é humana ou nenhuma. IA só com pedido do cliente |
| "Vou pôr Dymo, carimbo e recorte em cada cena para dar ritmo" | Motion é camada fina, um parâmetro por vez. Colagem: 1–2 cartões |
| "Gero grãos verde/amarelo/marrom para mostrar a torra" | Simular a transformação é fabricar o processo. Fotografe as amostras reais |
| "A marca entra no fim, como assinatura" | Marca ou pessoa da casa nos 5 primeiros segundos e no fim |
| "Trilha de violão sob a narração inteira" | Sem música sob fala; trilha nas respirações e no fecho |
| "CTA: salva esse vídeo" | Envio por DM é o sinal mais forte; salvar é para utilidade |
| "Mido retenção e salvamentos" | E curtidas ÷ views ≥ 3%, comentários e múltiplo da mediana da grade |
| "Não tenho filmagem, faço tudo em colagem" | Escolha um formato que caiba no material real, ou peça a captura |
| "Uma piada leve deixa mais leve" | Se tirar o café e a piada continuar de pé, corte |
| "Café escuro/preto é o vilão" | Pode acusar o próprio Clássico. O vilão é o **motivo** (disfarçar defeito), conferido contra a torra real de cada SKU |
| "O Arthur torra, a família planta desde 1985" | Papel e história de pessoa real é `[confirmar]` até o cliente dizer |
| "Não preciso olhar referência, já sei o padrão" | Cite 3 fichas no planejamento. Sem isso o plano não está pronto |

## Checklist antes de levar o roteiro ao cliente

- [ ] 3 fichas citadas, com o que cada uma empresta
- [ ] formato escolhido da tabela §1, com o porquê
- [ ] gancho com imagem real no quadro 0, texto e fala; passou no teste da leitura literal
- [ ] voz humana ou nenhuma (IA só se o cliente pediu)
- [ ] cada etapa com consequência na xícara e um número conferido
- [ ] a tese não acusa nenhum SKU da Canastra (torra real de cada um conferida); fatos de pessoa marcados `[confirmar]`
- [ ] humor (se houver) de dentro do café; sem autodepreciação; vocabulário de torra limpo
- [ ] áudio decidido antes da edição; sem música sob fala
- [ ] motion só como camada; nada simulado (grão, chama, pacote)
- [ ] marca nos 5 s e no fim; fecho na xícara; CTA de envio
- [ ] plano de medição com a régua de 3% e a mediana da grade
