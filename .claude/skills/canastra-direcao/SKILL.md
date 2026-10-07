---
name: canastra-direcao
description: Use when deciding how a Café Canastra photo should LOOK — que chão, que luz, que empilhamento, que props, que paleta — for a scene, packshot, carousel slide or ad. Covers the named looks (Céu a pino, Terra, Empilhado, Mesa de Minas, Palco escuro, Didático branco) and the rules that keep art direction from breaking realism or borrowing someone else's brand — including when a product came out looking giant or out of scale.
---

# Direção de foto — o eixo da cenografia

Esta skill escolhe **chão, empilhamento, props e paleta**. Ela **não toca** em
profundidade de campo, perfil de câmera nem fidelidade de rótulo.

## A descoberta que organiza tudo

**Direção de arte e realismo são eixos diferentes, e dá para ser artístico sem
mentir na óptica.**

Olhando o `@eatfishwife` em 05/10/2026: a composição é altamente dirigida — latas
empilhadas como arquitetura, chão de terracota escolhido, limão cortado e pimenta
postos por cor. Mas a **óptica é natural**: sol duro com sombra recortada, tudo
nítido do primeiro ao último plano, nenhum bokeh.

O nosso motor já governa bem o eixo da óptica. Ninguém governava o da cenografia.
É esse o buraco que esta skill fecha.

## Rotear primeiro

| Assunto | Dono |
|---|---|
| anti-bokeh, perfil de câmera medido, luz real da fazenda | **canastra-cena** |
| rótulo letra por letra | **canastra-embalagem** |
| quantos slides e os portões do deck | **canastra-carrossel** |
| fluxo do ChatGPT e conferência ampliada | **canastra-conteudo** |
| **que chão, que arranjo, que prop, que paleta** | **esta skill** |

**Se a direção de arte pedir desfoque para ficar bonita, a óptica ganha.**

---

## Os looks nomeados

| Look | O quadro | Estado |
|---|---|---|
| **Céu a pino** | assunto em pé na terra vermelha, fotografado com o celular **no chão**: horizonte baixo, metade de cima só céu de meio-dia, folha caída como régua de escala | **aprovado pelo cliente**, 07/10/2026: capa e slide 2 do carrossel de história. É o padrão de carrossel |
| **Terra** | pacote sobre a terra vermelha, sol a pino, sombra dura e curta, céu azul com cumulus entrando no alto | geração — a lavoura existe, pacote na lavoura não |
| **Empilhado** | os três SKUs repetidos como arquitetura, enchendo o quadro | **pronto** — 96 packshots aprovados + composição |
| **Bancada** | cozinha de verdade, granito, azulejo, luz lateral dura de manhã, sombra recortada | **validado** — as peças de 05/10 e o deck de cápsulas |
| **Mesa de Minas** | pacote entre coisas reais, comida pela metade, migalha, faca largada | geração + composição |
| **Palco escuro** | fundo quase preto, luz de recorte, poça quente | geração; **polo profissional, declarado** |
| **Didático branco** | comparação em ciclorama, texto em código | **pronto** — 96 packshots já existem |

### A estética Canastra entra por três coisas medidas, não por adjetivo

- **Terra vermelha** como chão — é o nosso equivalente nativo ao terracota do Fishwife;
- **sol a pino, céu azul com cumulus, sombra dura** — iPhone 7, ISO 20, meio-dia.
  **Não é golden hour**: as 26 fotos de Medeiros foram capturadas entre 10h e 11h, e
  o acervo não tem outra luz;
- o contraste dos três materiais da linha: **preto mate, kraft, vermelho metalizado**.

### Céu a pino: a geometria que faz o look

O look é o **Terra** resolvido para receber tipografia: o céu de meio-dia vira a
página do slide. Três decisões o sustentam, e a primeira já custou uma rodada:

- **O horizonte fica na altura da câmera.** Para o assunto subir contra o céu, a
  lente vai **no chão**, a ~8 cm. Com a câmera "na altura do joelho" e o pacote
  passando das fileiras, o modelo desenhou um saco de ~1 m, e o cliente viu antes de
  nós (lição 48).
- **Régua de escala com tamanho escrito.** Uma folha de café caída (~12 cm) ao lado
  de um pacote de 23 cm, e as árvores (2 m) a 20–30 m. Sem números, o modelo resolve
  a proporção aumentando o produto.
- **Céu reservado onde o texto vai.** Assunto à direita; a metade de cima livre, e o
  canto superior esquerdo sem árvore, poste, fio ou pássaro.

Os blocos de prompt prontos estão em `canastra-carrossel/ceu-a-pino.md` §1.

### Palco escuro é o polo oposto, e isso é declarado

É o look do `@cafezale.com.br`, e ele contradiz o nosso alvo calibrado de foto de
celular. Serve para **e-commerce e anúncio**, não para o feed orgânico. Medido na
mesma data: os cinco posts analisados deles fizeram 9 a 23 curtidas com 24,2 mil
seguidores (0,04% a 0,09%), contra a mediana de 52 da Canastra com 10,3 mil (0,50%).
**Copie a produção, não a expectativa.**

---

## Duas regras que não se negociam

**Produto de terceiro nunca entra no quadro.** O Cafezale fotografa Twinings e
Ferrero; nós não podemos e não devemos. Quando um aparelho precisa aparecer — a
máquina de cápsula, por exemplo — ele é **genérico e sem logotipo**, gerado, e de
preferência cortado na borda: contexto, não assunto. E **foto de produto de terceiro
baixada da internet nunca vira pixel nosso**, nem do Google Imagens, nem de lugar
nenhum. Pesquisar a forma para descrever é uso legítimo; colar o arquivo não é.

**Prop escolhido por cor ainda precisa existir naquele lugar.** A liberdade da
direção de arte é escolher *entre* o que é plausível, nunca inventar. Balança de
cozinha, colher de cupping e bule de ágata na lavoura continuam proibidos. Os
nossos props de cor são de Minas e são nossos: pão de queijo, queijo, rapadura,
goiabada.

---

## A negação explícita é parte da direção

O modelo tem composição favorita e não a abandona por omissão, só por proibição
nomeada. Escreva a lista **por cena**, não genérica:

- **cozinha** puxa bancada de mármore e luz de janela grande;
- **lavoura** puxa golden hour e fileira infinita;
- **qualquer uma** puxa dourado quente, bokeh e prop estilizado.

Medido em 05/10: com *"DO NOT INCLUDE: marble countertop, golden hour light, window
flare, styled props, linen cloth, coffee beans arranged on the surface, flowers,
bokeh, vignette, colour grading, studio lighting"*, a cozinha voltou com **granito**,
cafeteira, pote de plástico e caneca — nenhum prop inventado, foco profundo do
pacote à parede.

---

## O que falta no acervo, e o que isso significa

`docs/briefing-captura.md` e `docs/INVENTARIO-REFERENCIAS.md` registram: **zero
arquivos** de grão torrado, café na xícara, coador em uso, tambor de torrefação,
cupping, terreiro ou colheita.

Consequência para a direção: todo look que precise desses assuntos depende de
**geração sem referência própria** — onde o modelo inventa — ou de captura nova.
Não há terceiro caminho, e nenhuma quantidade de Pinterest fecha esse buraco,
porque Pinterest não vira pixel.

---

## Bandeiras vermelhas — pare

- Você vai baixar uma foto de produto de terceiro para usar no quadro.
- Você escolheu um prop porque a cor ficava boa, sem perguntar se ele existe ali.
- Você pediu golden hour na fazenda — o acervo não tem, e a calibração foi medida
  no sol de meio-dia.
- Você está aplicando o alvo de celular num slide de **palco escuro**, ou o inverso.
  São slots diferentes e o alvo de cada um é diferente.
- A direção de arte pediu profundidade de campo rasa. **A óptica ganha.**
- Você pediu o produto passando do horizonte **sem** pôr a câmera no chão, ou sem
  uma régua de escala com tamanho escrito.
