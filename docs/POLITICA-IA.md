# Politica de uso de inteligencia artificial em imagens

**Cafe Canastra** — versao 1, agosto de 2026.

> ## A IA edita e estende o real. A IA nao inventa o real.

Usamos inteligencia artificial na producao das nossas imagens. Esta pagina explica
exatamente como, o que nunca fazemos com ela, e como voce pode saber, olhando um post
nosso, se houve IA no meio do caminho.

---

## 1. Por que temos uma politica, e nao so bom senso

O que vendemos e cafe rastreavel. A fazenda fica em Medeiros, na Serra da Canastra, a
cerca de 1.250 metros. A familia Boaventura esta la desde 1985. A energia e fotovoltaica.
As variedades sao Arara e Catuai 2SL. A torra acontece em Uberlandia, em lotes pequenos,
com registro de perfil. Cada uma dessas frases e verificavel — e e por elas que alguem
paga mais caro num pacote de cafe.

Uma imagem sintetica generica destroi esse argumento em silencio. Se a fazenda da foto
nao existe, a altitude da foto nao existe, e o rosto que sorri na colheita nao e de
ninguem, entao a promessa de rastreabilidade vira retorica. O prejuizo nao e so etico:
e comercial e direto. O cliente que descobre uma foto inventada passa a duvidar do lote,
do produtor e da data de torra impressa no pacote.

Por isso a regra nao e uma recomendacao interna. Ela esta escrita no sistema que produz
as imagens, roda antes de qualquer geracao e **impede** o que esta proibido aqui embaixo.
Nao depende de alguem lembrar.

---

## 2. O que nunca geramos

**Rosto de pessoa real.** Nenhum rosto identificavel de produtor, colaborador, familiar
ou cliente e sintetizado, reconstruido, "melhorado" ou recriado por IA. Se voce ve o
rosto de alguem numa foto nossa, aquele rosto foi fotografado. Isso vale mesmo quando a
pessoa autorizou o uso da imagem: a autorizacao permite usar a foto, nunca recriar a
pessoa.

**Embalagem com logotipo ou texto legivel, a partir do zero.** Rotulo, logotipo,
tipografia, selo, informacao de lote e origem: nada disso e desenhado por IA. Quando um
pacote aparece numa imagem, ele vem de uma fotografia real do pacote — recortada e
composta sobre o cenario, ou usada como referencia fiel. Modelos de imagem deformam
letra e logotipo com facilidade, e um rotulo com um glifo errado e, na pratica, uma
informacao errada sobre o produto.

**Cena que afirma um fato que nao aconteceu.** Nao geramos uma colheita que nao houve,
uma safra que nao existiu, um maquinario que nao temos, um selo ou certificacao que nao
possuimos, um premio que nao ganhamos, uma area plantada que nao e nossa. Imagem tambem
e afirmacao. Se a cena descreve a operacao, ela precisa descrever a operacao como ela e.

---

## 3. O que podemos gerar

Com IA, e sempre a partir do nosso proprio acervo de fotos reais:

- **texturas e superficies** — trama de saco de juta, madeira, pedra, tecido, papel;
- **fundos e cenarios de estudio** — o pano de fundo atras de um produto real;
- **extensao de cena** — abrir o enquadramento de uma foto existente, completar o ceu,
  prolongar uma mesa ou um terreiro para caber num formato vertical;
- **variacoes de luz e de clima** — a mesma cena real no amanhecer, com neblina, em dia
  fechado;
- **macros ilustrativos** — grao, moagem, vapor, floracao, agua no bloom do coador,
  quando a imagem ilustra um conceito e nao documenta um lote especifico.

O criterio unico e simples: a IA pode trabalhar o **entorno** e a **luz** de uma verdade
que ja existe. Ela nao pode criar a verdade.

---

## 4. Pessoas e consentimento

Toda foto que entra no nosso acervo comeca marcada da forma mais restritiva possivel:
**presume-se que ha pessoa identificavel** e **presume-se que nao ha consentimento**. O
sistema nunca desmarca isso sozinho, e nenhuma deteccao automatica de rosto tem
permissao para mexer nesses dois campos. So uma pessoa da equipe, olhando a foto, muda
o registro.

Como funciona na pratica:

1. Antes de fotografar alguem — produtor, colaborador, parceiro, cliente — pedimos
   autorizacao de uso de imagem por escrito, assinada, com data e finalidade.
2. O termo assinado fica arquivado sob responsabilidade da coordenacao de marketing do
   Cafe Canastra, junto ao nome do arquivo das fotos a que se refere.
3. So depois disso a foto e marcada como "com consentimento em arquivo" no catalogo.
4. Uma foto com pessoa identificavel e sem termo arquivado **nao pode** ser usada como
   base de nenhuma geracao. O sistema recusa o pedido e explica o motivo.
5. A autorizacao pode ser revogada a qualquer momento. Quem quiser retirar a propria
   imagem do nosso material fala com a gente pelos canais de atendimento; a foto sai do
   acervo ativo e as pecas em circulacao que dependem dela sao substituidas.

Quando a cena pede uma pessoa mas nao temos termo, a saida e fotografar de novo ou
enquadrar sem rosto: maos, silhueta, sombra, costas, figura fora de foco. Nunca gerar um
rosto para preencher o espaco.

---

## 5. Rotulagem: como marcamos conteudo com IA

Toda imagem produzida com auxilio de IA nasce, no nosso sistema, com a marca
"exige rotulagem". Nao existe imagem de IA nossa que dispense o aviso.

**Onde a marcacao acontece.** No Instagram e demais plataformas da Meta, usamos a
propria marcacao de conteudo de IA da plataforma, ativada no fim do fluxo de publicacao,
em "Configuracoes avancadas" — e a mesma marcacao vale para Reels e Stories. Em outros
canais, usamos o recurso equivalente da plataforma; onde nao houver recurso, escrevemos
no proprio texto do post.

**Como sabemos o que marcar.** Cada imagem exportada sai acompanhada de tres coisas:

- metadados de origem gravados no proprio arquivo (XMP e EXIF), incluindo o modelo
  usado, a data, as fotos reais que serviram de referencia e o principio desta politica;
- um arquivo `.xmp` ao lado da imagem, porque as redes sociais costumam apagar os
  metadados do arquivo no upload;
- um **manifesto do lote** (`manifest.json`), que lista imagem por imagem, com o campo
  `disclosure_required` e uma instrucao em portugues do que precisa ser marcado.

Quem publica nao decide de cabeca: abre o manifesto do lote e segue o que esta escrito
la. Na duvida entre marcar e nao marcar, marcamos.

---

## 6. Revisao humana antes de publicar

Nenhuma imagem vai ao ar direto da maquina. Toda imagem gerada passa por aprovacao de
uma pessoa da equipe, que aprova ou rejeita com motivo registrado. O que a revisao olha,
nessa ordem:

1. **Tipografia e logotipo.** Se aparece embalagem, o rotulo e conferido letra a letra
   contra o pacote real: nome da linha, logotipo, acentuacao, informacao de origem. Um
   unico caractere estranho e motivo de rejeicao, sem discussao.
2. **Maos e rostos.** Dedos, juntas, unhas, pele. Rosto parcial, refletido ou desfocado
   ao fundo tambem conta — se parece alguem, e tratado como alguem.
3. **Veracidade da cena.** A imagem afirma alguma coisa sobre a operacao que nao seja
   verdade? Se sim, ela nao publica, por mais bonita que esteja.
4. **Coerencia com o acervo.** A imagem parece ter saido da mesma fazenda e da mesma
   torrefacao das fotos reais, ou parece banco de imagens?

Rejeicao e barata. Uma imagem publicada e errada, nao.

---

## 7. Se voce perguntar se uma imagem nossa foi feita com IA

A resposta padrao, dita sem rodeio, e:

> "Foi, sim. Essa imagem passou por IA. Ela foi construida a partir das nossas proprias
> fotos da fazenda em Medeiros e da torrefacao em Uberlandia — a IA trabalhou o
> cenario e a luz em volta. O rosto de qualquer pessoa que aparece foi fotografado, com
> autorizacao assinada, e o rotulo do pacote e o rotulo real. Se quiser, mostramos a foto
> original que deu origem a essa imagem."

E a ultima frase e para valer: guardamos, para cada imagem publicada, o registro de qual
modelo a gerou, com qual instrucao e a partir de quais fotos reais. Se alguem pedir, a
gente mostra.

Se a imagem for uma fotografia sem nenhuma IA envolvida, a resposta e igualmente direta:
"essa e foto, sem IA nenhuma".

Nunca respondemos de forma evasiva, e nunca apresentamos imagem gerada como se fosse
registro documental de um evento especifico.

---

## 8. Quem responde por esta politica

A coordenacao de marketing do Cafe Canastra responde pela aplicacao desta politica, pelo
arquivo dos termos de autorizacao de imagem e pela revisao das imagens antes da
publicacao. Fornecedores, agencias e parceiros que produzem conteudo para a marca estao
sujeitos as mesmas regras — inclusive a de rotulagem.

Esta politica e revisada sempre que mudarem as ferramentas que usamos ou as regras de
rotulagem das plataformas. Criticas, duvidas e pedidos de retirada de imagem sao bem
vindos pelos nossos canais de atendimento.

---

*A IA edita e estende o real. A IA nao inventa o real.*
