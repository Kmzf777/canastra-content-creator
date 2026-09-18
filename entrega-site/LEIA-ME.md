# Imagens prontas para o site

Copie para `frontend/public/`. O plano que as usa é o `prompt.md` na raiz.

## O que tem aqui

### Foto real — sem nenhuma ressalva

| Arquivo | Dimensão | Vai para |
|---|---|---|
| `serra-da-canastra-chapadao-21x9.jpg` | 3840×1646 | Bloco 7 · banda de campanha |
| `serra-da-canastra-chapadao-16x9.jpg` | 3840×2160 | alternativa 16:9 da mesma |
| `serra-da-canastra-escarpa-16x9.jpg` | 3840×2160 | segunda opção de campanha |
| `cafezal-serra-da-canastra-21x9.jpg` | 3840×1646 | Bloco 8 · Do pé à xícara |

As três primeiras saem de `imagens/Fazenda e Serra/` — as **únicas** fotos de
paisagem ampla da Serra que existem em qualquer pasta. O cafezal é
`IMG_1400.JPG`, com EXIF de câmera e GPS: **altitude gravada 1.235–1.272 m**, o
que faz o arquivo provar sozinho os "1.250 metros" que a marca alega.

**Estas quatro não precisam de aviso de IA.** São fotografia.

### Cena gerada — precisa de rotulagem

| Arquivo | Dimensão | Vai para | Quem |
|---|---|---|---|
| `cafe-especial-serra-da-canastra-heroi.jpg` | 2752×1536 | Bloco 1 · herói | Dulce, 52, no cafezal |
| `comprar-cafe-em-graos.jpg` | 1600×1986 | Bloco 2 · ladrilho 1 | Bárbara, 37, apartamento em BH |
| `comprar-cafe-moido.jpg` | 1600×1986 | Bloco 2 · ladrilho 2 | Rosângela, 44, padaria em BH |
| `comprar-capsulas-de-cafe.jpg` | 1600×1986 | Bloco 2 · ladrilho 3 | Yuri, 29, copa de escritório em SP |
| `comprar-drip-coffee.jpg` | 1600×1986 | Bloco 2 · ladrilho 4 | Thainá, 26, apartamento em SP |
| `clube-assinatura-de-cafe-especial.jpg` | 2400×1340 | Bloco 5 · Clube | Wesley, 31, portaria em BH |

`docs/POLITICA-IA.md §5`: *"não existe imagem de IA nossa que dispense o aviso."*
**Estas seis carregam essa obrigação** — metadado de origem e uma decisão sua
sobre onde o aviso aparece no site.

### `_conferir/` — não publique

`PLACA-kit-rotulo-quebrado.jpg` — a cena do ladrilho de kits. A praça, o banco de
concreto, a sombra dura de meio-dia e a fiação estão perfeitos. **Os rótulos
não:** `SCA 80+` saiu `GLA GB)` e o peso `250g` virou **`200g`**, que é erro
factual sobre o produto.

Três embalagens legíveis num quadro é o pior caso de fidelidade, e as seis
variantes confirmaram. **A rota de conserto é composição local**: gerar a cena
sem os pacotes e colar os três recortes reais por cima. É a única com tipografia
garantida.

Enquanto isso, o ladrilho "Kits e caixas" pode usar `/pacote-classico.jpg`, que
já existe e é foto real.

## Como foram feitas

Cada pessoa é **ficcional** e existe primeiro como um avatar gerado do zero —
instantâneo de celular contra parede lisa, com pedido explícito de pele com poro,
oleosidade, assimetria, mancha e acne. **Nenhum rosto parte de foto de pessoa
real.** O avatar entra como referência na geração da cena; é o único jeito de o
mesmo rosto sobreviver entre duas imagens, porque o motor não tem identity-lock e
seed não resolve isso.

Os avatares ficam em `saida-teste/home-elenco/`. Guarde-os: **sem eles, uma
imagem nova do mesmo personagem sai com outro rosto.**

Onde a embalagem aparece, ela é **pixel de foto real** — o packshot entra junto
no campo de fontes e o prompt nunca descreve o rótulo. Descrever faz o modelo
redesenhar, e o que sai é um sósia da marca.

Scripts: `scripts/home_avatares.py` (elenco), `scripts/home_cenas.py` +
`home_cenas_lista.py` (cenas), `scripts/home_medir.py` (medição),
`scripts/home_entregar.py` (fechamento). Todos com `--dry-run`.

## Quatro coisas que a execução ensinou

**1 · Os packshots estão rotacionados no arquivo.** Abertos como estão, o pacote
parece deitado e o modelo o reproduz **de cabeça para baixo**, com o rótulo
espelhado — foi o que a primeira sonda devolveu. Girados −90° são o que sempre
foram: o pacote em pé contra a parede, arte inteira legível. Isso sozinho
consertou a fidelidade. Ver `saida-teste/packshot-em-pe/`.

**2 · A ordem das fontes decide o rosto.** Com o packshot na frente, o rosto
derivou do avatar e saiu outra pessoa. Com o avatar na frente, ele segura.

**3 · `Desde 1985` não sobrevive.** Conferido com recorte ampliado nas oito
variantes do ladrilho de moído: `Café CANASTRA`, a serra,
`SPECIALTY / ESPECIAL / SCA 80+` e `250g` saem certos; o manuscrito pequeno sai
como rabisco em **todas**. É a lição 13 — abaixo de ~2% da altura do quadro a
tipografia é reescrita. No ladrilho a ~400px isso são três pixels e ninguém lê.
**Mas não use nenhuma destas ampliada, e não as use na PDP.**

**4 · Eu inventei um objeto e a pesquisa me pegou.** Escrevi que o copo americano
tem "facetas verticais rasas". Ele não tem: é um **tronco de cone liso**, base
estreita, boca larga — e é essa conicidade que o faz empilhar. 190 ml, 9,3 cm,
105 g. Os dois ladrilhos de copo foram **regerados** com o descritor corrigido
contra a ficha do fabricante, e na foto de cápsula dá para ver os copos
empilhados, que é a prova de que agora está certo.

## Perfil de câmera

Medido em cada variante e calibrado contra as fotos **reais** deste acervo, que
dão p1 6–29, saturação 76–91 e R/B 0,84–1,12.

| | p1 | preto% | satur | R/B |
|---|---:|---:|---:|---:|
| alvo do projeto | 14,0 | 0,007 | 70,0 | 0,969 |
| foto real do cafezal | 6,3 | 0,211 | 91,1 | 0,839 |
| **herói entregue** | 3,0 | 0,352 | 93,9 | 0,822 |

O herói está na faixa da foto real tirada no mesmo lugar — e é esse o benchmark
que importa, não o alvo abstrato, que foi medido num conjunto misto.

Foco profundo em todas, sem exceção. Desfoque não se desfaz em pós.

## Um aviso sobre o herói

**Nenhuma variante entrega a zona escura para o texto.** Medido no quarto
inferior esquerdo contra `cal` #F1F0EA, percentil 95: as seis dão **1,7:1 a
2,4:1**. As fotos reais dão 2,1:1 e 2,3:1.

Não é falha de geração: **ao meio-dia, num cafezal aberto, não existe um quarto
escuro.** A regra "a sombra vem da foto" da Nike funciona porque as fotos deles
são urbanas e low-key. Aqui o **gradiente `fuligem` fica**, e é ele a fonte do
contraste. Meça a composição final: texto em `cal` precisa de ≥ 4,5:1.

## Peso

Os arquivos aqui são a **fonte**, não o que vai ao ar. O `next/image` reconverte
para AVIF/WebP e gera o `srcset`. O teto que importa é o **servido**: 250 KB para
o herói no breakpoint de desktop. Confira depois do build, não aqui.
