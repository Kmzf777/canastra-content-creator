# Briefing de imagens — a home Nike do Café Canastra

Documento irmão de `PROMPT-HOME-NIKE.md`. Aquele diz o que construir; este diz
que imagem entra em cada buraco, e como fazê-la.

**São 8 imagens a gerar.** Seis reaproveitadas do que já existe.

---

## 0. Três travas da política publicada — leia antes de gerar

`docs/POLITICA-IA.md` não é convenção interna: é política **publicada**, e o §7
promete que, se alguém perguntar se uma imagem foi feita com IA, a marca responde
e mostra a foto de origem. Três cláusulas dela atravessam este briefing inteiro.

### Trava 1 · Rosto

> **§2** — *"Se você vê o rosto de alguém numa foto nossa, aquele rosto foi
> fotografado."*
> **§4** — *"Quando a cena pede uma pessoa mas não temos termo, a saída é
> fotografar de novo ou enquadrar sem rosto: mãos, silhueta, sombra, costas.
> Nunca gerar um rosto para preencher o espaço."*

O `CLAUDE.md` proíbe sintetizar rosto de **pessoa real**; esta política vai além
e proíbe **qualquer** rosto gerado. **Todo briefing deste documento que mostra
rosto depende de a política ser atualizada.** Enquanto não for, cada um deles tem
uma linha `SEM ROSTO` com o enquadramento alternativo — e a §6.3 mostra que os
enquadramentos sem rosto são justamente os de **menor** taxa de erro.

### Trava 2 · Cena não pode afirmar fato

> **§2** — *"Cena que afirma um fato que não aconteceu. Não geramos uma colheita
> que não houve, um maquinário que não temos, uma área plantada que não é nossa.
> Se a cena descreve a operação, ela precisa descrever a operação como ela é."*
> **§3** — *"A IA pode trabalhar o **entorno** e a **luz** de uma verdade que já
> existe. Ela não pode criar a verdade."*

**Não existe uma única foto de terreiro de secagem no acervo.** Ninguém sabe se
é de cimento, que forma têm as leiras, se há rastelo. Uma cena de terreiro
gerada **afirma a operação** e cai direto nesta trava. O mesmo vale para
colheita, torrefação e painel solar — todos ausentes da base.

**Consequência:** as cenas de fazenda deste briefing estão **bloqueadas** até
haver foto real ou confirmação escrita de quem opera. As cenas urbanas não caem
nesta trava: uma laje em Belo Horizonte não afirma nada sobre a Fazenda
Divinéia.

### Trava 3 · Rotulagem sem exceção

> **§5** — *"Não existe imagem de IA nossa que dispense o aviso."*

Cada imagem exportada precisa sair com metadados XMP/EXIF de origem, um `.xmp`
ao lado (porque as redes apagam metadado no upload) e uma entrada no
`manifest.json` do lote com `disclosure_required`. **Toda peça deste briefing
carrega essa obrigação.** No site, isso vira `figcaption` visível ou nota na
página de política — e a decisão de onde é do dono.

### E a regra que sai das três

**Nenhum nome de lugar real entra no `alt`, na legenda ou no JSON-LD de imagem
gerada.** "Fazenda Divinéia", "Medeiros", "terreiro da fazenda" numa cena
sintética é afirmação de procedência falsa em campo legível por máquina. Cena
gerada descreve o que se vê, sem topônimo de propriedade.

---

## 1. Inventário: o que existe, o que serve, o que falta

### Serve como está

| Arquivo | Dimensão | Vai para |
|---|---|---|
| `frontend/public/pacote-classico.jpg` | 1000×1241 (4:5) | Grade das linhas |
| `frontend/public/pacote-suave.jpg` | 825×1024 (4:5) | Grade das linhas |
| `frontend/public/pacote-canela.jpg` | 1000×1241 (4:5) | Grade das linhas |
| `saida-teste/site-fundo-branco/FINAL-classico-250g-branco.jpg` | 1856×2304 | "Em alta" |
| `saida-teste/site-fundo-branco/FINAL-suave-250g-branco.jpg` | 1856×2304 | "Em alta" |
| `base-curada/01-real-verificada/…/cafezal/IMG_1400.JPG` | 4032×3024 | Banda "Do pé à xícara" |

**`IMG_1400` é foto real, verificada por EXIF e GPS** (iPhone 7, ISO 20,
março/2017, altitude gravada 1.235–1.272 m — a altitude no arquivo confirma
sozinha os "1.250 metros" que a marca alega). Cafezal, terra vermelha, céu azul
com cumulus, sol a pino. Recortada a `4032×1600` vira a banda de 40vh do bloco
7. **Não gere o que já existe.**

### Serve com conserto

`FINAL-canela-250g-branco.jpg` (1856×2304) — o rótulo principal está **correto**
(`Café CANASTRA`, `Desde 1985`, `CAFÉ TORRADO E MOÍDO COM CANELA`, `250g`), mas
o micro-texto sob os dois ícones no canto superior direito saiu **`AD
BNPELEARI`**. É a corrupção de tipografia pequena da lição 13.

Conserto: **corte os 12% superiores** antes de usar, ou regere só este.
Verificado por ampliação em 25/08/2026.

> **Os três recortes são de pacote MOÍDO** (`TORRADO E MOÍDO`). Um ladrilho
> "Comprar café em grãos" **não pode** usá-los.

### Não serve

| Arquivo | Por quê |
|---|---|
| `imagem-banner.jpg` | 1280×720 — pequeno demais para herói de 100vh, que precisa de ≥2560px. E é sépia quente, o viés que `estetica.md §2` manda evitar. |
| `bannerdesktop.jpg` | 1600×500, 3,2:1 — proporção de faixa, não de herói. |
| `microlote-png.png` | 500×500 — resolução insuficiente. |
| `base-curada/03-mood-terceiros/` (16 arq.) | **Nunca** vira pixel nem fonte de guidance. Uma tem marca d'água, outra tem rosto identificável sem autorização. Só descritor textual. |
| `base-curada/04-quarentena/` (6 arq.) | Sintéticas e baixa resolução. Se entrarem na destilação de estilo, o motor aprende o look que o projeto existe para evitar. |

### A decisão pendente que vale uma geração

`base-curada/02-real-nao-verificada/serra-canastra/` — **6 paisagens em
4032×3024** do chapadão. Escarpa de topo plano, capim seco, céu com cumulus. São
as **únicas** fotos de paisagem ampla da Serra que existem em qualquer camada.

Estão bloqueadas por uma linha do `LEIA-ME.md`: *"Sem EXIF de câmera e sem GPS.
Quase certamente próprias, mas o arquivo não prova."*

**Se o dono confirmar que são dele, elas sobem para `01` e viram material de
site.** Não resolvem o herói (ver `HERO-01`, que precisa de gente e de cidade),
mas resolvem `CAMP-01` de graça e dão à marca a única imagem de escala de
paisagem que ela tem.

### O que a base inteira não tem

Zero grão torrado. Zero xícara ou coador. Zero torrefação. Zero painel solar.
Zero terreiro de secagem. **Zero pessoas com rosto. Zero foto de Belo Horizonte
ou de São Paulo.** As 20 fotos de cafezal são todas do mesmo dia e a diversidade
real é de umas 4 cenas.

Existe **uma** presença humana real e verificada:
`cafeeiro-com-mao/IMG_1421.JPG` e `IMG_1422.JPG` — mão no cafeeiro, EXIF + GPS a
1.250 m. É a única foto de gente com procedência provada, e por isso a única que
pode representar alguém da casa.

---

## 2. As quatro famílias

O `estetica.md §8` define três. A direção nova exige uma quarta.

| Família | Função | Estado |
|---|---|---|
| **Território** | Herói institucional, banda de sequência | 26 fotos, todas do mesmo dia, só lavoura |
| **Produto** | Card, galeria de PDP | Completa para as 3 linhas principais |
| **Sabor** | Herói de PDP | **Não existe** |
| **Gente & Cidade** | Herói da home, ladrilhos de formato, clube | **Não existe — é o que este briefing cria** |

A quarta família não é enfeite. Ela responde a um dado de busca: o seed
`onde comprar café especial` devolve **dez sugestões no autocomplete BR, e todas
as dez são cidades** — BH e São Paulo à frente. É o cluster transacional mais
denso de toda a pesquisa. A foto urbana não é só estética; é o ativo que as
páginas de cidade vão precisar.

---

## 3. O vocabulário visual, por lugar

Levantado por pesquisa em 25/08/2026. **Nenhuma imagem de terceiro foi usada
como pixel ou como guidance — só como descritor textual**, que é o único uso que
a camada `03-mood-terceiros` permite.

### 3.1 São Paulo

**Três correções de briefing que evitam erro caro:**

1. **O piso de SP não é calçada portuguesa.** É o **"piso paulista"**: ladrilho
   hidráulico quadrado cinza-claro e off-white com o contorno do estado
   estilizado em preto e branco alternados, desenhado em 1965 por Mirthes
   Bernardes. A calçada portuguesa existiu e foi removida da Avenida Paulista em
   2007. Pedir *"Portuguese wave-pattern mosaic pavement"* num prompt de São
   Paulo entrega **Rio ou Lisboa**.

2. **São Paulo não é cidade ensolarada.** São 5 a 6 horas de sol por dia o ano
   inteiro e 18 dias de chuva em janeiro. **A luz padrão é céu branco encoberto**
   — difusa, sem sombra projetada, ponto preto levantado, altas puxando azul.

   > Isto coincide com o alvo já medido do projeto (`p1=14`, saturação 70, cast
   > R/B 0,969) **sem nenhum esforço de calibração**. E resolve de graça o risco
   > registrado no `CLAUDE.md` de que "dourado quente é assinatura de IA": São
   > Paulo tem antídoto nativo.

3. **A Lei Cidade Limpa (14.223/06, em vigor desde 2007) removeu mais de 15.000
   outdoors.** São Paulo é metrópole **sem publicidade externa**. Qualquer cena
   com outdoor, painel de LED ou letreiro grande ao fundo denuncia que não é SP.
   As fachadas ficaram cruas: pastilha manchada de chuva, empena cega, estrutura
   metálica vazia.

**Elementos que dizem SP sem cartão-postal:** pastilha cerâmica 2×2 cm fosca em
creme, bege-rosado, marrom-tabaco, verde-água, azul-piscina, com escorrido
vertical cinza sob peitoril · concreto aparente com marca de fôrma de madeira ·
**empena cega** (parede lateral inteira sem janela, exposta quando o vizinho
baixo foi demolido — hoje a maior superfície visual da cidade) · brise-soleil ·
cobogó · janela basculante de alumínio com a folha girada 30° para fora ·
fiação aérea em nó denso com sobras enroladas em bobina · poste de concreto
duplo-T · marquise fina sobre porta de comércio · porta de aço de enrolar ·
caixa d'água azul sobre laje · azulejo 15×15 branco de padaria com rejunte
encardido · toldo esmaecido · **letreiro pequeno** (a lei limita o tamanho) ·
Minhocão passando a menos de 3 m de janelas · estação de metrô em concreto
aparente sem revestimento.

**Paleta real de SP** *(hex estimados por descrição de material, não amostrados
de pixel — trate como direção, não como valor)*: concreto novo `#9B9891`,
envelhecido `#8C8A85`, escorrido `#6E6B66` · reboco cru de empena `#A6A29A` ·
asfalto seco `#4A4845`, molhado `#2E2D2C` · céu encoberto `#D8DADB`–`#C6C9CB` ·
garoa `#CFD2D2` · azul de inverno enevoado `#7EA3C4` (**nunca** `#1E6FD9`
saturado) · pastilha creme `#C4B49A` · piso paulista `#C9C6BE` com motivo
`#2A2A28` · gradil verde-escuro `#2E3B33` · toldo vermelho desbotado `#A8443C`.

> **A paleta da marca já é a paleta de São Paulo.** fuligem `#14110E` ≈ pichação
> `#1A1A1C` · cal `#F1F0EA` ≈ céu encoberto `#D8DADB` · juta `#C9A87A` ≈
> pastilha creme `#C4B49A` · barro `#8E4B2E` ≈ ferrugem `#8A4E2E` · mata
> `#2C3B2E` ≈ gradil `#2E3B33` · vermelho `#C4231E` ≈ toldo `#A8443C`.
>
> E o que São Paulo **não** tem: terracota `#D97757` e creme `#F4F1EA` — o par
> exato que o `estetica.md §2` classifica como "default de IA" e evita de
> propósito.

**O fio narrativo dispensa invenção.** A cidade de São Paulo foi construída com
dinheiro de café: Estação da Luz, Martinelli, as mansões dos barões, a ferrovia
que existe para escoar grão. A ponte não é metáfora, é infraestrutura. *O grão
nasce na serra e é bebido na cidade que o café pagou.*

**Proibido:** mural e pichação reconhecíveis. São obra autoral de terceiro —
risco jurídico, e saturam demais para a base lavada. Empena cega crua, sim; Beco
do Batman, não.

### 3.2 Belo Horizonte

**A correção que evita a mentira geográfica:** BH **não é a Minas colonial**.
Foi planejada em 1897 e reformada pelo modernismo de Kubitschek e Niemeyer nos
anos 40–50. Pedra de Ouro Preto, barroco e pelourinho são Minas, mas são **a
Minas errada** — a Canastra fica no Alto São Francisco / Cerrado, a 400 km da
Estrada Real. Usar barroco não é licença poética, é erro de geografia.

**O vocabulário certo:** brise horizontal contínuo do Edifício Niemeyer (o
zebrado de sombra que muda de largura conforme a curva — o padrão urbano mais
fotogênico de BH, e ninguém em café o usa) · abóbadas de concreto da Pampulha
revestidas de pastilha granulada · palmeira imperial em fileira dupla na Praça
da Liberdade · **tijolinho aparente**, módulo 19×9 cm, cor variando de `#8E4B2E`
a `#B5714E` **dentro da mesma parede**, com eflorescência esbranquiçada nas
fiadas baixas · laje com parapeito de cimento queimado, caixa d'água, antena e
varal — **o mirante real de BH, não o rooftop bar** · corredor do Mercado
Central em anéis concêntricos, teto baixo, fluorescente mais claraboia ·
**sacaria de juta** empilhada, trama grossa, estêncil de lote meio apagado ·
queijo minas em torre de 4 a 6, nunca alinhada · garrafeira de cachaça que
resolve como textura, não como objeto · boteco de azulejo branco 15×15 até
1,60 m, acima disso pintura bege ou verde-hospital · mesa de aço inox escovado
60×60 com o brilho já morto, banqueta monobloco · **fiação aérea em feixe grosso
cruzando o quadro na diagonal** — assinatura brasileira que o modelo tende a
apagar e precisa ser pedida.

**A Serra do Curral ao fundo:** crista longa e baixa ao longo de toda a borda
sul da cidade. Cume do município a 1.538 m contra uma cidade a 852 m — sobe
~680 m acima do observador e ocupa **3 a 8% da altura do quadro**. **Não é pico;
é lombada com escarpa.** Face exposta de minério em ocre-cinza. O azulamento
atmosférico de 8 a 15 km é a **única** maneira legítima de separar planos neste
perfil de câmera — nunca desfoco.

**A luz de BH resolve a ponte serra→cidade de graça.** 19°55'S, 852 m, 500 km do
mar, estação seca de junho a agosto (5,4–11,4 mm/mês), insolação máxima em julho
(≈260 h), ~2.428 h de sol/ano. Resultado: sombra de **borda dura**, céu azul
saturado no zênite, sombra aberta puxando muito azul (8.000–12.000 K) — que
**é** o cast R/B 0,969 já medido no perfil do projeto. O azul não é estilo; é o
comportamento correto do dispositivo naquele céu.

> **Regra operacional:** fotografe (ou gere) BH entre 11h e 14h, de maio a
> agosto. É a janela em que a cidade tem exatamente a mesma luz que Medeiros
> tinha em março ao meio-dia. **Fotografar os dois mundos no mesmo relógio solar
> é o que faz a série ler como uma marca só.**
>
> No inverno, ao meio-dia, o sol de BH vem do **norte** — as sombras apontam
> para o sul, ou seja, na direção da Serra do Curral. Sombra e serra ficam do
> mesmo lado do quadro.

**O eixo de cor que costura tudo:** `barro #8E4B2E` e `mata #2C3B2E` do sistema
do site são literalmente o latossolo vermelho da lavoura e o capão de mata. **É
o mesmo óxido de ferro na terra da roça e no tijolinho de BH** — mesmo hue,
escalas diferentes. A cidade só acrescenta duas coisas ao sistema: o azul
cobalto do azulejo (`#1F4E9C`) e o cinza de cimento e zinco. Nada mais precisa
entrar.

### 3.3 A roça

Já documentada e já fotografada. Pé de café, terra vermelha, mangueira de
irrigação, poste de madeira, arame, cadeira de plástico, galpão de zinco,
terreiro de cimento, porteira, telha de barro.

**Nenhum objeto que não exista naquele lugar.** Balança de cozinha, colher de
cupping, bule de ágata e pano de crochê na lavoura são invenção — e estão na
lista negativa do motor.

> **Contradição interna a resolver:** o `docs/briefing-captura.md` deste
> repositório pede **bule de ágata, coador de pano e golden hour na varanda** —
> exatamente três itens que a lista de clichês e o `CLAUDE.md` proíbem. O
> `briefing-captura` é anterior às descobertas de geração. **Quando os dois
> discordarem, vale o `CLAUDE.md`.**

---

## 4. O que o motor precisa ganhar antes de gerar

O sistema de blocos em `templates/blocos/` está travado por
`tests/test_blocos.py`, e a direção nova quebra três testes. **Isso é feature, não
bug** — o teste está fazendo o trabalho dele. O conserto é escopar as regras, não
afrouxá-las.

### 4.1 Os três testes que vão quebrar

| Teste | Por que quebra | Conserto |
|---|---|---|
| `test_os_nove_blocos_carregam` | `assert set(todos) == ARQUIVOS_ESPERADOS`, com exatamente 9 nomes | Acrescente os blocos novos a `ARQUIVOS_ESPERADOS` |
| `test_papel_de_cada_bloco` | compara o dicionário de papéis inteiro | Acrescente os blocos novos ao dicionário esperado, e registre o papel em `cie.blocos._PAPEIS` |
| `test_nenhum_bloco_de_luz_afirma_nublado` | varre **todos** os blocos com `papel == "luz"` e proíbe `overcast` / `cloudy`. A luz padrão de São Paulo **é** encoberta. | **Escope por contexto** — ver abaixo |

### 4.2 Como escopar a regra do nublado sem furá-la

A razão escrita do teste é: *"o alvo de calibração de câmera foi medido NESSAS
fotos de sol forte, então pedir nublado desalinha o motor do alvo."* Essa razão
vale para a **fazenda**. Não vale para São Paulo, onde o céu encoberto entrega o
mesmo alvo por outro caminho.

Acrescente um campo `contexto: fazenda | cidade` ao YAML dos blocos de luz e
troque a varredura:

```python
luzes_de_fazenda = [
    b for b in carregar_todos().values()
    if b.papel == "luz" and b.contexto == "fazenda"
]
assert luzes_de_fazenda, "tem que existir pelo menos um bloco de luz de fazenda"
for b in luzes_de_fazenda:
    assert proibido not in afirmativo(b.texto).lower()
```

E acrescente o teste que a mudança exige — sem ele a regra vira porta aberta:

```python
def test_bloco_de_luz_urbana_nao_afirma_sol_a_pino_de_fazenda():
    """Céu encoberto de SP e sol a pino de Medeiros são regimes diferentes.
    Um bloco de cidade não pode herdar a descrição da lavoura."""
```

### 4.3 Blocos novos a criar

| Arquivo | Papel | `contexto` | O que descreve |
|---|---|---|---|
| `luz-ceu-encoberto-sp.yaml` | `luz` | `cidade` | Hemisfério inteiro como fonte, softbox de 180°, sem sombra projetada — só sombra de contato, 6500–7500 K, dominante azul-cinza, contraste baixíssimo |
| `luz-sol-planalto-bh.yaml` | `luz` | `cidade` | Sol direto 5.400–5.800 K, sombra de borda dura, sombra aberta a 8.000–12.000 K puxando azul, poeira seca levantando o ponto preto |
| `gente.yaml` | `gente` *(papel novo)* | — | Direção de elenco e anti-"rosto de IA" |
| `negativos-com-gente.yaml` | `negativos` | — | Igual a `negativos.yaml` **menos** `people, person, hand, hands, arm, fingers, face`, **mais** os negativos de rosto sintético |

> `espontaneidade.yaml` afirma literalmente **"NO PEOPLE VISIBLE — no hands, no
> arms, no faces, nobody in frame"**. Ele **não entra** em nenhum prompt com
> gente. Crie `espontaneidade-com-gente.yaml` ou monte sem ele — mas então
> confira que a cobertura anti-anúncio continua vindo de outro lugar, porque era
> ele que a carregava.

**`foco-profundo` continua obrigatório em todos.** `montar()` levanta
`BlocoError` se uma lista explícita vier sem ele, e isso está certo: desfoque não
se desfaz em pós.

---

## 5. As 8 imagens

**Tudo o que é gerado é cidade: 3 São Paulo · 5 Belo Horizonte.**

| id | Slot da home | Personagem | Lugar | Proporção |
|---|---|---|---|---|
| `HERO-01` | 1 · Herói 100vh | `wesley-31` | **BH** — laje, crista ao fundo | 16:9 |
| `FMT-01` | 2 · Cápsulas | `yuri-29` | **SP** — copa de escritório | 4:5 |
| `FMT-02` | 2 · Drip coffee | `thaina-26` | **SP** — cozinha de apartamento | 4:5 |
| `FMT-03` | 2 · Em grãos | `barbara-37` | **BH** — apartamento antigo | 4:5 |
| `FMT-04` | 2 · Moído | `rosangela-44` | **BH** — balcão de padaria | 4:5 |
| `FMT-05` | 2 · Kits | `igor-23` | **BH** — praça, meio-fio | 4:5 |
| `CAMP-01` | 5 · Banda destaque | `diego-19` | **SP** — ponto de ônibus, zona leste | 16:9 |
| `CLUBE-01` | 6 · Clube | `wesley-31` | **BH** — portaria de prédio | 4:3 |

**Por que zero roça na lista de geração — e por que a home continua tendo roça.**
A `POLITICA-IA.md §2` proíbe cena gerada que afirme a operação, e o acervo não
tem foto de terreiro, colheita ou torrefação para conferir. Então **toda cena de
fazenda gerada está bloqueada** (ver `HERO-ALT`).

A roça não some da home: ela entra por **foto real**, que é mais forte de
qualquer jeito — `IMG_1400` na banda "Do pé à xícara" e os três packshots na
grade das linhas. A home abre na cidade, e a serra aparece onde há prova.

*Bloco 7 usa `IMG_1400` do acervo. Bloco 4 usa os três `pacote-*.jpg`. Bloco 8
usa os recortes. Nada disso se gera.*

> **Expansão futura, fora destas oito:** `dulce-52`, `neide-58` e `aparecido-67`
> foram escritos para a roça — retrato por etapa na banda "Do pé à xícara"
> (terroir, colheita, secagem). **Todos dependem de uma ida a campo.** Enquanto
> não houver, a banda roda com a foto de acervo.

### 5.1 A regra de composição que vale para as 8

**A sombra vem da foto.** Medido no pixel da Nike: **zero scrims em CSS**, e a
zona onde o texto pousa é mais escura que o resto do quadro em **12 de 12
casos**, com contraste de 12,08:1 a 15,84:1. Em "Shop Cleats" a luminância cai
de 127 no topo para 27 na base. O fotógrafo entrega a sombra.

Todo prompt de imagem com texto por cima precisa **pedir a zona escura**, e a
imagem precisa ser **medida** depois. Se não entregar ≥7:1 na zona de texto, a
imagem está errada — não compense com gradiente mais escuro.

**A cor tem regra de função.** Medido em 16 imagens da Nike: produto sai
saturado (S 179–206) e quente (R/B 1,63–3,04); **gente e lugar saem lavados
(S 40–75) e frios (R/B 0,967–1,10)**. Estas 8 imagens são todas de gente e
lugar. Vão no registro lavado e frio — que é exatamente o perfil de câmera já
medido do projeto. Não há o que reconciliar.

**Movimento zero.** A home da Nike é inteiramente estática: nenhum desfoque de
movimento, nenhuma ação congelada; no herói principal a atleta está **sentada**.
Não peça movimento.

---

## 6. Gerar gente: os números antes das frases

Três fatos medidos que mudam o método, não só o texto do prompt.

**Realismo de pessoa é ~50/50, não 90/10.** No RealBench, onde humanos votam se
a imagem passa por fotografia, o modelo líder é julgado real por **53%**. Trate
cada geração com pessoa como moeda viciada em ~50% no eixo "parece foto" —
**antes** de contar mão, rótulo e enquadramento.

**O default do modelo é pele clara, e ele não corrige sozinho.** Análise
comparando *"a front-facing photo of a person"* com *"…a person from Brazil"*
achou maioria de pele clara nas duas. Trabalho publicado no CHI mostra que
prompt com "Brasil" puxa vocabulário visual eurocêntrico.

> Consequência direta para este projeto: **se o prompt não escrever o fenótipo,
> a idade e o corpo de cada personagem, a home sai com o mesmo rosto claro
> repetido e a estratégia de amplitude falha em silêncio.** A ficha de elenco da
> §7 não é enfeite de briefing; é parâmetro obrigatório.

**Negativo não funciona como você espera.** Nem a xAI nem o Gemini expõem campo
de prompt negativo, e o Gemini documenta que **negação de objeto deve ser
reescrita em positivo**. A lista `Avoid: …` que o `cie.blocos.montar()` anexa
funciona como sinal, não como filtro. Onde importa de verdade — "sem sorriso
aberto", "sem retoque" — escreva em positivo: *"lips closed"*, *"real
unretouched skin with visible pores"*.

### 6.1 O que ainda quebra, em ordem de frequência

1. Mão em gesto complexo ou interagindo com objeto pequeno
2. Duas ou mais pessoas interagindo — o modo de falha é *appearance drift*: os
   atributos degradam conforme o número de sujeitos sobe, e às vezes um sujeito
   simplesmente some
3. Dentes em sorriso aberto
4. Orelha (dobras de cartilagem simplificadas)
5. Fios soltos de cabelo que derretem na pele ou no fundo
6. Óculos, joia e tatuagem
7. **Cabelo crespo 3C–4C** — os datasets pesam para liso e ondulado, e o que
   existe rotulado como cabelo negro é majoritariamente afro brilhoso de salão.
   O modelo devolve sempre a mesma versão idealizada em vez do espectro real.

> Para personagens de cabelo crespo: **nomeie o padrão com precisão**
> (`tightly coiled 4C hair in flat twists, frizz at the hairline, no gloss`),
> gere mais variantes, e confira a linha de implantação com recorte ampliado — é
> onde o erro aparece primeiro.

### 6.2 Quantas variantes, e como escolher

| Tipo de quadro | `--n` |
|---|---:|
| Figura distante ou de costas, sem mão em evidência | 2 |
| Plano médio, rosto visível, mãos parcialmente à mostra | 4 |
| Close de rosto | 4 |
| Duas pessoas · mão em primeiro plano · pessoa segurando o pacote | 6–8 |

**Ordem de conferência — cada passo elimina antes de você olhar o próximo:**

1. Recorte ampliado das **mãos**: conte dedos, confira articulação
2. Recorte ampliado da **faixa de texto do rótulo** (lição 13: em miniatura os
   erros passam batido)
3. **Rosto a 100%**: poro, assimetria, catchlight igual nos dois olhos, dente
4. **Direção da sombra vs. direção do especular** — a lição 6 vale igual para
   pessoa: meça, não assuma
5. Só então composição e beleza

**Nunca escolha pela miniatura.** Um quadro difícil a `n=8` custa ~US$ 0,54 no
Gemini 3 Pro em batch, ou ~US$ 0,64 na xAI 2.0 med/2k. É barato perto de subir
uma mão com seis dedos no herói do site.

### 6.3 Enquadramento, do mais seguro ao mais arriscado

`figura distante (<15% da altura)` → `de costas / silhueta` →
`três-quartos com rosto parcialmente virado` → `plano médio frontal, mãos
relaxadas` → `close de rosto` → `interagindo com objeto` → `duas pessoas`

**A figura distante é o enquadramento do herói full-bleed.** O rosto fica abaixo
do limiar de detalhe — o modelo não tem como errar o que não desenha —, e ainda
resolve por construção a exigência de que a pessoa gerada não se pareça com
ninguém real.

---

## 7. Blocos de texto, prontos para colar

### `BLOCO-FOCO` — obrigatório em todos, sem exceção

Verbatim de `templates/blocos/foco-profundo.yaml`, **com a cláusula de cena
trocada** para cidade (a original diz *"the rows far up the slope"*, que é da
lavoura):

```
EVERYTHING IN THE FRAME IS SHARP. Tiny 1/1.7 inch phone sensor at f/1.8, enormous
depth of field. The nearest surface and the far end of the street are ALL equally crisp
and detailed. NO focus falloff, NO background blur, NO bokeh, NO subject separation.
Distance reads faint from atmospheric haze only, never from defocus. The four CORNERS
are visibly SOFTER and slightly smeared the way a cheap wide phone lens falls apart away
from centre. Fine luminance noise in the shadows, faint JPEG blocking in the flat sky.
```

### `BLOCO-HDR` — obrigatório em todos

Verbatim de `templates/blocos/hdr-celular.yaml`:

```
PHONE HDR at work: the shadows are LIFTED and open and slightly grey rather than black -
nothing is a solid black mass. At the same time the brightest patches are BLOWN OUT to
featureless white. The midtones look a bit flat and processed. Slightly cool, washed
white balance, muted low saturation - NOT warm, NOT orange, NOT amber, NOT rich or vivid.
```

### `BLOCO-LUZ-SP` — novo, só para São Paulo

```
OVERCAST WHITE SKY, the default weather of São Paulo. The light source is the entire
hemisphere, a 180-degree softbox: there are NO cast shadows anywhere, only tight contact
shadows directly under objects where they touch a surface. Contrast is very low, the black
point sits naturally lifted, colour temperature around 6800K with a blue-grey cast across
the whole frame. Wet or recently rained-on surfaces carry a dull specular sheen. This is a
grey working weekday, not a bright day.
```

### `BLOCO-LUZ-BH` — novo, só para Belo Horizonte

```
DRY-SEASON HIGHLAND SUN at midday, the light of Belo Horizonte between May and August.
Direct sun around 5600K, shadows SHORT and HARD-EDGED, falling almost straight down. The
open shade is filled only by the sky, so it goes strongly BLUE, around 9000K. The sky is
deep blue at the zenith and turns milky within ten degrees of the horizon. Fine dry dust
in suspension lifts the black point. Distant ridges eight to fifteen kilometres away are
separated by atmospheric BLUEING, never by defocus.
```

### `BLOCO-GENTE` — novo, em todo prompt com pessoa

Cada frase abaixo ataca um tell específico do "rosto de IA". Não corte nenhuma:

```
Real unretouched skin with visible pores and slight oiliness on the forehead and nose
bridge. Uneven skin tone, a faint blemish, a small mole. The two halves of the face are
clearly NOT symmetrical - one eyebrow sits slightly higher, one eye is slightly smaller.
Lips closed, no smile, no visible teeth. Looking at what they are doing, not at the
camera. A single small hard specular highlight in each eye, both coming from the same
direction. No beauty retouching, no skin smoothing, no makeup look, no studio lighting.
Hands relaxed and partly out of frame or partly hidden behind the object they hold.
```

### `BLOCO-FOTO-AMADORA` — novo, substitui `espontaneidade` quando há gente

O `espontaneidade.yaml` afirma literalmente *"NO PEOPLE VISIBLE — no hands, no
arms, no faces, nobody in frame"*, então **ele não entra** aqui. Este bloco
preserva a função anti-anúncio dele:

```
Phone photo, taken in about two seconds with one hand. Nobody composed it, nobody
arranged anything, nobody moved anything into place for the photograph. The frame is
tilted a few degrees, the horizon is not level, the subject sits off to one side, and the
edges cut through things arbitrarily. The scene is cluttered with the ordinary mess of a
place in use. NOT a product photograph, NOT an advertisement, NOT a styled set.
```

> **Não** importe do repertório público de "foto amadora" as duas coisas que
> violam o alvo medido: `slight motion blur` (borrão não se desfaz em pós, e a
> home da Nike tem movimento zero) e `yellowish lighting` (contradiz o cast azul
> de 0,969 nas altas).

### `NEGATIVOS-COM-GENTE`

A lista de `templates/blocos/negativos.yaml` **menos** `people, person, hand,
hands, arm, fingers, face` — que são justamente o que agora se quer — **mais**:

```
beauty retouching, skin smoothing, airbrushed skin, poreless skin, symmetrical face,
open mouth smile, perfect teeth, model pose, stock photo look, uncanny face,
extra fingers, malformed hand, glossy salon hair, floating hair, motion blur,
warm golden light, teal and orange, billboard, LED panel, large signage, graffiti mural
```

`billboard`, `LED panel` e `large signage` estão aí por causa da Lei Cidade
Limpa: São Paulo não tem publicidade externa desde 2007, e um outdoor ao fundo
denuncia a cena. `graffiti mural` está aí por direito autoral de terceiro.

### `NEGATIVO-MARCA-DE-TERCEIRO` — universal, em TODOS os oito

Cena urbana brasileira é feita das superfícies que mais carregam marca:
engradado de garrafa, cadeira monobloco, máquina de café, garrafa térmica, caixa
d'água, fita de papelão, tênis, camiseta de time. O modelo preenche cada uma
delas com um logotipo plausível — e logotipo plausível de terceiro é marca de
terceiro. Cole isto em todos, sem exceção:

```
No third-party brand, logo, wordmark, emblem, badge, team crest or legible
commercial name anywhere in the frame - not on bottles, crates, chairs, machines,
appliances, tape, boxes, signs, vehicles, awnings, cups, flasks, trainers or
clothing. Every bottle, crate, chair and appliance is plain and unbranded.
```

**Confira cada variante com zoom antes de aprovar.** É o erro que mais passa
batido, porque em miniatura um logotipo errado parece só uma textura.

---

## 8. Ficha de elenco

> **O elenco é o único lugar onde este site diz "alcance amplo".** O copy está
> proibido de dizê-lo, então a amplitude tem que estar em quem aparece, onde
> essa pessoa está e o que ela faz com as mãos.

Dez personagens ficcionais: **3 em São Paulo, 3 em Belo Horizonte, 2 na roça de
Medeiros, 1 na Serra e 1 que atravessa os dois mundos.** Sete dos dez são pardos
ou pretos — o que é fidelidade ao país, não cota (Censo 2022: 45,3% pardos).

**Escreva o fenótipo, a idade e o corpo em todo prompt.** Sem isso o modelo
devolve o mesmo rosto claro dez vezes e a estratégia falha em silêncio.

| id | Quem | Onde | Slot |
|---|---|---|---|
| `dulce-52` | Mulher **preta**, 52, pele escura uniforme, rosto comprido, mandíbula marcada. Cabelo **4C natural, ~2 cm**, sem alisamento, sem turbante. Óculos de acetato barato com uma haste consertada. | Terreiro de secagem, Medeiros | `HERO-ALT` — **bloqueado** |
| `neide-58` | Mulher parda retinta, 58, marcas de sol permanentes no dorso do nariz e nos antebraços, com linha nítida onde a manga termina. Cabelo 4A grisalho na têmpora, coque baixo. **As mãos são o assunto.** | Talhão de café, Medeiros | Do pé à xícara *(futuro)* |
| `aparecido-67` | Homem branco caboclo queimado, 67. Rosto, pescoço e mãos vermelho-tijolo; o resto branco. Chapéu de palha **na mão**, não na cabeça. | Cerca e chapada, Canastra | Do pé à xícara *(futuro)* |
| `wesley-31` | Homem **preto**, 31, rosto redondo, degradê de barbearia de bairro. Esparadrapo no indicador. Sempre em trânsito. | Laje e portaria em BH (e torrefação em Uberlândia, no futuro) | **HERÓI** + **CLUBE** |
| `thaina-26` | Mulher parda média, 26, sardas discretas, cicatriz pequena de acne no queixo. Cabelo **3C volumoso** definido por gel barato, com frizz real no topo. **Filha da Neide.** | Cozinha de apartamento, SP | **FMT drip** |
| `yuri-29` | Homem nissei/sansei, 29, pele clara amarelada, prega epicântica, rosto anguloso. Óculos redondos de aro fino. O corpo mais reto do elenco. | Copa de escritório, SP | **FMT cápsulas** |
| `diego-19` | Homem pardo escuro, 19, **espinha ativa** na testa e no maxilar — idade real, não pele de campanha. Rosto que ainda não terminou de crescer. | Ponto de ônibus, leste de SP | **BANDA DESTAQUE** |
| `rosangela-44` | Mulher parda clara, 44, papada leve, olheira natural, sobrancelha a lápis, batom quase todo saído. Cabelo tingido com **3 cm de raiz aparecendo**. Mãos vermelhas de água e detergente. | Balcão de padaria, BH | **FMT moído** |
| `barbara-37` | Mulher branca, 37, pele muito clara, sardas densas, **rosácea leve** nas maçãs, sobrancelha clara e falhada. Cabelo castanho-avermelhado ondulado, presilha de plástico. | Apartamento antigo, BH | **FMT em grãos** |
| `igor-23` | Homem pardo médio, 23, barba rala em ilhas no maxilar, alargador pequeno já fechado. Cabelo 3B, raiz um pouco oleosa. Calo na ponta do dedo de corda de violão. | Praça de bairro, BH | **FMT kits** |

### As seis regras que valem para o elenco inteiro

**1 · A Dulce opera — ela não serve.** Ela decide a hora de virar o lote. É
inversão explícita do clichê que a ONU Brasil mapeou na publicidade nacional: o
protagonismo negro subiu de 7% para 20%, mas a pessoa negra segue aparecendo
como mão-de-obra passiva. Aqui ela é quem manda.

**2 · O figurino não é gosto, é consequência da medição.** **Branco puro estoura
em sol a pino e preto puro vira cinza barrento com o ponto preto em 14.** Por
isso juta `#C9A87A`, barro `#8E4B2E` e mata `#2C3B2E` são a espinha do
guarda-roupa, e o vermelho `#C4231E` entra **uma vez por dobra** — na camiseta
de várzea do Diego.

**3 · Todo mundo segura a embalagem pelo TERÇO INFERIOR.** Pela base ou pela
lateral de baixo, **com nenhum dedo cruzando a faixa impressa do rótulo.** Isto
resolve de uma vez os dois piores modos de falha: mão errada e letra errada.

**4 · O olhar tem regra por slot.** Direto na lente e semicerrado pelo sol no
herói e na banda de campanha — *firmeza sem convite, ele não está te oferecendo
nada*. Desviado e ocupado nos ladrilhos de formato, o que também **libera escala
para o rótulo**. O único calor da página fica no Clube: sorriso **iniciado e não
concluído** — o que, de quebra, elimina o risco de dente.

**5 · Recorrência: quatro rostos três vezes, não dez rostos uma vez.** O motor
não tem identity-lock, e seed não serve para isso. A ligação é feita por **mão,
gesto e figurino**. A mãe em Medeiros e a filha em São Paulo se ligam pelo mesmo
gesto — *a mão inteira em volta do copo, nunca pela alça* — e por nada escrito.

**6 · Casting sem dizer.** O que comunica "gente do dia a dia" não é roupa
barata: é a naturalidade do contexto. A caneca é a que já existe na casa, a mesa
tem outra coisa em cima, o lugar é o de sempre e não um cenário. **Nada de**
avental de barista de couro, sorriso de comercial de margarina, família reunida
na mesa do café da manhã, ou fazendeiro de chapéu posando.

> Nenhuma variante pode sair parecida com pessoa real identificável — família
> Boaventura inclusive. Se sair, **descarte a variante**; não "ajuste".

---

## 9. Os oito briefings

### Duas regras de roteamento que valem para todos

**Onde a embalagem aparecer legível, o pixel é da foto real.** Provedor xAI
`/images/edits`, com o packshot no campo `image` (objeto) ou `images` (plural).
Passar `image_url` devolve **HTTP 200 e ignora a imagem em silêncio** — o erro
400 é que revela: *"provide either the `image` field or the `images` field, but
not both"*.

**Onde ela não aparecer, ou for pequena, o Gemini gera a cena.**
`gemini-3-pro-image`, `imageConfig: {aspectRatio, imageSize: "2K"}`, auth por
`x-goog-api-key`. A xAI **não tem 4:5** — gere em `3:4` e recorte tirando ~62%
da sobra do topo.

> **Lacuna de acervo que restringe três destes briefings:** existe packshot real
> de `Clássico`, `Suave` e `Canela` em pacote de 250 g. **Não existe foto real
> de sachê de drip coffee, de cápsula nem de kit.** Onde o briefing pedir esses
> três, a embalagem fica **fora de quadro, virada ou cortada** — nunca desenhada
> a partir de descrição, porque isso produz um sósia da marca.

### Três coisas sobre os packshots que só se descobrem abrindo os arquivos

**1 · Metade deles é o VERSO.** `packshot-suave/Suave (4).jpg` é o painel
traseiro: QR de rastreabilidade, `SEM GLÚTEN`, `SUGESTÃO DE PREPARO`, medidores
de `TORRA MÉDIA` / `INTENSIDADE`, `ALTITUDE 1.250 METROS`, selo `PLANTIO PRÓPRIO
DIRETO DO PRODUTOR · Desde 1985`, CNPJ e endereço. Não tem serra, não tem
lettering, não tem `250g`.

> Usar o verso como fonte é **a lição 1 do `CLAUDE.md`**, palavra por palavra:
> *"Logotipo saía genérico mesmo com referência → a referência era o verso do
> pacote."* Conferido por leitura do arquivo em 25/08/2026.
>
> **A frente do Suave é `Suave (5).jpg`** — `Café CANASTRA`, `Desde 1985`,
> `SPECIALTY / ESPECIAL / SCA 80+`, `250g`, `SUAVE / TORRADO E MOÍDO`.
> **Abra o arquivo antes de usá-lo como fonte. Sempre.**

**2 · Os packshots são o pacote DEITADO, fotografado de cima.** Nenhum está em
pé. Um prompt de `/images/edits` que diga ao mesmo tempo *"mantenha o pacote
idêntico pixel a pixel"* e *"apoie o pacote em pé na bancada"* pede duas coisas
incompatíveis, e o modelo resolve reinventando o pacote — que é justamente o que
o fluxo existia para evitar. **Ou a cena aceita o pacote deitado e a câmera de
cima, ou o pacote é recortado e composto localmente.**

**3 · Não existe packshot de café EM GRÃOS.** A frente do Suave diz `TORRADO E
MOÍDO`, e o mesmo vale para Clássico e Canela. Uma cena em que esse pacote
despeja grãos inteiros **afirma o que o produto não é**. Isso não se resolve no
prompt: ou o pacote sai do quadro, ou alguém fotografa o pacote de grãos real.

---

### `HERO-01` — o herói

| | |
|---|---|
| **Slot** | Bloco 1 · herói 100vh |
| **Arquivo** | `cafe-especial-belo-horizonte-heroi.jpg` |
| **Lugar** | Belo Horizonte — laje de área de serviço, crista da serra ao fundo |
| **Elenco** | `wesley-31` — o personagem-ponte |
| **Proporção** | 16:9, mínimo 2560 px de largura |
| **Provedor** | Gemini `gemini-3-pro-image` — nenhuma embalagem no quadro |
| **`--n`** | **4** com rosto · **2** na versão sem rosto |

> **Este herói mudou de lugar depois da leitura da `POLITICA-IA.md`.** A versão
> anterior era a `dulce-52` no terreiro de secagem, e ela é uma imagem melhor —
> mas **afirma a operação** (§2) sem que exista uma única foto de terreiro para
> conferir. Ficou registrada em `HERO-ALT`, bloqueada. Uma laje em Belo
> Horizonte não afirma nada sobre a fazenda: é entorno e luz, que é justamente o
> que a §3 permite.

**Por que este quadro funciona como herói.** A Nike põe no herói uma pessoa em
**repouso dentro do próprio lugar** — no herói principal deles a atleta está
sentada num banco de vestiário. E a ponte serra→cidade fica literal: a crista ao
fundo e a mesma luz de meio-dia que a lavoura tem em março.

**Espaço para texto:** quarto inferior esquerdo. A câmera está **dentro** do vão
sombreado da porta da área de serviço, e a parede escura ocupa esse quarto. É
daí que sai o contraste — não do CSS.

```
Phone photo from a rooftop service area of an ordinary apartment building in Belo
Horizonte, Brazil, at midday in July. The camera stands inside the shaded doorway, so the
DARK interior wall and door frame fill the LOWER LEFT QUARTER of the frame in deep open
shade. Beyond it, the sunlit flat roof: a burnished cement parapet about one metre ten
high, a blue polyethylene water tank on a low plinth, an aluminium TV aerial, a wire
clothesline with two shirts hanging still. A 31-year-old Black Brazilian man, medium-dark
skin, round face, full eyebrows, uneven short stubble along the jaw, hair cut low with a
barbershop fade and a sharp lined edge, stands at the parapet holding a chipped enamel
mug, weight on one hip. He wears a faded forest-green cotton t-shirt cut slightly large
and grey cargo trousers; a short thin silver chain at his neck; a strip of first-aid tape
around his index finger. He looks OUT over the city, three-quarters away from the lens,
mouth closed. Beyond the roof the city drops away in a slope of exposed red brick facades
whose colour varies within the same wall from dark rust to pale terracotta, concrete
posts, and thick bundled overhead cables crossing the frame diagonally. On the horizon,
ten kilometres out, a LONG LOW RIDGE with an irregular flat crest, separated from the city
only by atmospheric BLUEING - it is a ridge, NOT a peak, NOT a triangular mountain.

[BLOCO-LUZ-BH]
[BLOCO-GENTE]
[BLOCO-HDR]
[BLOCO-FOCO]
[BLOCO-FOTO-AMADORA]

Avoid: [NEGATIVOS-COM-GENTE], [NEGATIVO-MARCA-DE-TERCEIRO],
alpine summits, sharp triangular mountain peaks
```

**SEM ROSTO** *(enquanto a Trava 1 valer)*: troque `looks OUT over the city,
three-quarters away from the lens` por `stands with his BACK TO THE CAMERA at the
parapet; his face is not visible`, e reduza para `--n 2`. Figura de costas é o
**segundo enquadramento mais seguro** da escala da §6.3 — a versão sem rosto é
mais barata *e* tem menos risco.

**`alt`:** `Homem numa laje em Belo Horizonte com uma caneca de café, a cidade e
a crista da serra ao fundo`

*Sem topônimo de propriedade: a cena é gerada, então o `alt` descreve o que se
vê e não nomeia lugar da marca.*

**Risco:** o modelo tende a transformar a crista em pico triangular — mesmo erro
da lição 2, por isso a negação está escrita duas vezes. E há um risco de tema: a
**Serra do Curral** carrega disputa pública sobre mineração. O prompt a descreve
genericamente, sem nomear. Se a marca não quiser nem a associação, troque por
uma linha de morros sem escarpa exposta.

---

### `FMT-01` — cápsulas · São Paulo

| | |
|---|---|
| **Arquivo** | `comprar-capsulas-de-cafe-especial.jpg` · 4:5 · Gemini 2K (1856×2304) |
| **Elenco** | `yuri-29` — três-quartos, rosto cortado pela borda direita · `--n` 4 |

```
Phone photo in the pantry of an ordinary office floor in São Paulo on an overcast weekday.
A 29-year-old Brazilian man of Japanese descent, pale skin with a yellow undertone,
epicanthic fold, angular face, narrow jaw, no facial hair, tall and thin, standing
straighter than everyone else in the room, almost formal. Thick straight black hair in a
messy medium cut, the fringe falling into his eyebrow. Thin round wire-frame prescription
glasses. Long thin fingers, large hands, bitten nails. He holds a coffee capsule box by
its BOTTOM THIRD, resting on the formica counter and facing the camera square-on, with NO
finger crossing the printed label area, while his other hand pushes the drawer of a small
capsule machine shut. His face is three-quarters turned and CUT BY THE RIGHT EDGE of the
frame; he is looking at the machine, not at the camera. On the counter: a water cooler
bottle, a stack of thick tumbler glasses, a sugar sachet holder, crumbs. The light is
mixed - cool white fluorescent tubes overhead casting a faint green into the shadows, and
one hard rectangle of midday sun coming through a doorway to the left.

[BLOCO-GENTE]
[BLOCO-HDR]
[BLOCO-FOCO]
[BLOCO-FOTO-AMADORA]

Avoid: [NEGATIVOS-COM-GENTE]
```

**`alt`:** `Cápsulas de café especial na copa de um escritório em São Paulo`
**Risco:** a caixa de cápsula tem impressão e **não existe foto real dela** no
acervo. Ela é pedida de frente porque o rótulo precisa ler — então **confira a
faixa de texto com zoom** e, se sair errado em `n=4`, resolva por composição
local em vez de gerar mais.
**Sem bloco de luz:** a luz é interior mista e está descrita no corpo. **Não**
acrescente `BLOCO-LUZ-SP` aqui — o encoberto é a luz da rua, não a da copa.
**Óculos:** `yuri-29` usa, e óculos está na lista do que ainda quebra (aro que
atravessa a têmpora, reflexo sem fonte). Confira as duas hastes.

---

### `FMT-02` — drip coffee · São Paulo

| | |
|---|---|
| **Arquivo** | `comprar-drip-coffee-cafe-especial.jpg` · 4:5 · Gemini 2K |
| **Elenco** | `thaina-26` — três-quartos, rosto cortado pela borda superior · `--n` 4 |

```
Phone photo in the kitchen of a small São Paulo apartment on a grey morning. A 26-year-old
Brazilian woman with light golden-brown skin, faint freckles across the cheekbones, a
straight nose with a rounded tip and a small acne scar on the chin, skin visibly
untouched. Her hair is voluminous 3C curls to the shoulder, defined with cheap gel, with
real frizz standing up at the crown and at the hairline - no straightening, no glossy
shampoo-commercial curl. She wears a grimy off-white ribbed vest with wide straps and grey
sweat shorts, white socks with small dots, flip-flops; small hoop earrings; short nails
with chipped polish in a colour with no name; a thin silver ring on the index finger. She
leans her hip against a scratched formica counter, one foot crossed over the other,
shoulders rolled forward. She is opening a drip coffee box, holding it from its BOTTOM
THIRD by the sides so that NO finger crosses the printed label area; a drip sachet already
sits hooked over the rim of a thick tumbler glass. Her face is three-quarters and CUT BY
THE TOP EDGE of the frame, eyes down on her own hands. Behind her, old wall tile to
mid-height, a scratched aluminium awning window, and through it the neighbouring building
three metres away.

[BLOCO-LUZ-SP]
[BLOCO-GENTE]
[BLOCO-HDR]
[BLOCO-FOCO]
[BLOCO-FOTO-AMADORA]

Avoid: [NEGATIVOS-COM-GENTE]
```

**`alt`:** `Mulher abrindo uma caixa de drip coffee na cozinha de um apartamento
em São Paulo`
**Risco:** **não existe foto real do sachê nem da caixa de drip.** A caixa é
pedida de frente porque o ladrilho precisa dizer o formato — então a faixa de
texto é o primeiro recorte a conferir. Se `n=4` não devolver rótulo correto,
componha localmente.
**Gesto que liga:** a Thainá é filha da Neide. As duas seguram o copo **com a
mão inteira em volta, nunca pela alça** — é o único fio entre as duas fotos, e
ele não é escrito em lugar nenhum do site.

---

### `FMT-03` — em grãos · Belo Horizonte

| | |
|---|---|
| **Arquivo** | `comprar-cafe-em-graos-250g.jpg` · 4:5 · **xAI `/images/edits`** 2.0 med/2k, gerar em `3:4` e recortar |
| **Fonte de pixel** | **nenhuma — o pacote fica fora do quadro** |
| **Provedor** | Gemini `gemini-3-pro-image` · 4:5 · 2K |
| **Elenco** | `barbara-37` — três-quartos, rosto cortado pela borda · `--n` 4 |

> **Este briefing foi reescrito.** A primeira versão punha o pacote Suave
> despejando grãos inteiros, via `/images/edits`. Duas coisas estavam erradas e
> as duas foram conferidas no arquivo:
>
> 1. A fonte indicada era `Suave (4).jpg`, que é **o verso** do pacote.
> 2. A frente do Suave diz `TORRADO E MOÍDO`. **Não existe packshot de café em
>    grãos no acervo**, e um pacote de moído despejando grão inteiro afirma o
>    que o produto não é.
>
> A saída honesta é tirar o pacote do quadro: **o assunto do ladrilho é o
> formato**, e grão + moedor dizem o formato sem mentir sobre o SKU.

```
Phone photo in an old Belo Horizonte apartment at midday. A 37-year-old white Brazilian
woman with very pale skin, dense freckles across the nose and shoulders, mild rosacea
flushing on the cheeks, light brown eyes, pale patchy eyebrows. Auburn wavy hair, long,
clipped up with a plastic claw clip with loose strands escaping. Thin hands with visible
veins, a wedding band, a hair elastic around one wrist. She wears a fine off-white knit
top pilled with wear and loose creased linen trousers in a straw colour; she is barefoot
on a parquet wood floor. She sits on the floor at an iron-framed window, turning the crank
of a plain unbranded hand grinder braced between her knees, with a scatter of dark roasted
WHOLE COFFEE BEANS on the ledge beside her and a few that have bounced onto the parquet.
Her face is three-quarters and CUT BY THE FRAME EDGE, eyes down on the grinder. Through
the window, the neighbouring building three metres away; a hard-edged rectangle of midday
sun falls across the ledge and the spilled beans.

[BLOCO-LUZ-BH]
[BLOCO-GENTE]
[BLOCO-HDR]
[BLOCO-FOCO]
[BLOCO-FOTO-AMADORA]

Avoid: [NEGATIVOS-COM-GENTE], [NEGATIVO-MARCA-DE-TERCEIRO], coffee package,
printed bag, label, branded grinder
```

**SEM ROSTO:** troque para `only her hands and forearms enter the frame from the
bottom-right corner, where the frame edge cuts them` e caia para `--n 2`.

**`alt`:** `Moedor manual e grãos de café inteiros na janela de um apartamento
em Belo Horizonte`

**Risco:** a manivela. Mão em gesto complexo interagindo com objeto é o modo de
falha **número 1** — conte os dedos das duas mãos com zoom. O `--n` caiu de 6
para 4 porque sem rótulo no quadro há um eixo de erro a menos.

> **Desbloqueio:** se alguém fotografar o **pacote de grãos real** contra parede
> lisa — mesmo padrão dos 12 packshots que já existem —, este ladrilho volta a
> `/images/edits` com o pacote em cena e ganha a marca de volta. **Entra no
> `briefing-captura.md` como item bloqueador.**

---

### `FMT-04` — moído · Belo Horizonte

| | |
|---|---|
| **Arquivo** | `comprar-cafe-moido-especial.jpg` · 4:5 · Gemini 2K |
| **Elenco** | `rosangela-44` — apoiada no balcão, rosto cortado pela borda superior · `--n` 4 |

```
Phone photo at the steel counter of a neighbourhood bakery in Belo Horizonte, early
afternoon. A 44-year-old Brazilian woman with light brown skin, a full face, a soft double
chin, natural dark circles under the eyes, eyebrows drawn in with pencil, old lipstick
almost entirely worn off. Dyed chestnut hair pulled into a ponytail with THREE CENTIMETRES
OF DARK ROOT SHOWING and a side fringe falling across her face. Her hands are red from
water and detergent, nails short with clear polish; a tea towel hangs over her shoulder; a
small gold stud in each ear. She wears a yellowed off-white uniform polo with the collar
open and a small unreadable embroidery on the chest, a waist apron in a rust brown tied at
the front with a crooked knot - a WORK apron, never a leather barista apron - and uniform
trousers washed almost to grey. She is leaning on both forearms on the counter in the
pause between two customers, tearing the corner of a brick-shaped ground coffee package
that she holds by its BOTTOM THIRD, with NO finger crossing the printed label area. Her
face is three-quarters and CUT BY THE TOP EDGE of the frame, eyes down on the package. The
wall behind is glazed white 15x15 tile to the ceiling, grout grimy grey, corners chipped;
a bread display case; a stack of green plastic bottle crates. The light is mixed - cool
white fluorescent tubes overhead casting a faint green into the shadows, and one hard
rectangle of midday sun coming in through the open door.

[BLOCO-GENTE]
[BLOCO-HDR]
[BLOCO-FOCO]
[BLOCO-FOTO-AMADORA]

Avoid: [NEGATIVOS-COM-GENTE], leather barista apron
```

**`alt`:** `Atendente abrindo um pacote de café moído no balcão de uma padaria em
Belo Horizonte`
**Risco:** duas temperaturas de luz na mesma cena. É a luz real de padaria e deve
ser descrita como tal — **não** corrija para uma fonte só. O rótulo do pacote
moído é impresso e não há foto real de embalagem em formato tijolo: se a letra
sair errada em `n=4`, troque o pacote-tijolo pelo packshot de 250 g e rode em
`/images/edits`.
**Sem bloco de luz:** a luz é interior mista e está no corpo. Não acrescente
`BLOCO-LUZ-BH` aqui.

---

### `FMT-05` — kits · Belo Horizonte

| | |
|---|---|
| **Arquivo** | `comprar-kit-de-cafe-especial-presente.jpg` · 4:5 · **xAI `/images/edits` multi-fonte** |
| **Fonte de pixel** | três packshots **frontais**, no campo plural `images` (ver abaixo) |
| **Elenco** | `igor-23` — **de cócoras no meio-fio**, três-quartos · `--n` 6 |

**Os três arquivos-fonte, conferidos por leitura em 25/08/2026:**

| Linha | Usar | **Não** usar |
|---|---|---|
| Suave | `packshot-suave/Suave (5).jpg` — frente, arte completa | `Suave (4).jpg` — **é o verso** |
| Clássico | `packshot-classico/Classico (5).jpg` | — |
| Canela | `packshot-canela/IMG_20250410_145923008 (1).jpg` | `Canela.jpg` — **saco vazio e amassado**, topo aberto, arte dobrada sobre o vinco, sem `250g` visível, canela em rama cortada pela dobra |

Não existe foto de caixa de kit. **O kit é representado pelos três pacotes
juntos**, que existem em foto real. Isso é honesto e resolve o rótulo.

> A saída de multi-fonte **herda a proporção da primeira fonte**. Ordene os
> `images` com um packshot 4:5 na frente.

A cócora de calçada é um gesto brasileiro que nenhuma referência internacional
entrega. Ela é a razão de este ladrilho existir assim.

```
Phone photo on the kerb of a neighbourhood square in Belo Horizonte at midday. A
23-year-old Brazilian man with medium brown skin, a thin face, a narrow nose, patchy
island-like stubble along the jaw, a small closed-up stretched hole in one earlobe. Slim
build, narrow shoulders. Brown 3B curly hair with volume on top and shorter sides,
slightly oily at the root. A callus on one fingertip. He is SQUATTING ON HIS HEELS on the
kerb - feet flat, knees high, elbows resting on his knees - holding the three coffee
packages from the source photographs bundled together against his shins, gripped by their
LOWER SIDE EDGES with a house key hooked in the same hand, and NO finger crossing any
printed label area. He wears an oversized grimy off-white t-shirt with a SMALL unreadable
print, a second t-shirt in rust brown tied around his waist, washed indigo jeans, wrecked
skate trainers with mismatched laces. His face is three-quarters, partly cut by the frame
edge, looking sideways out of frame at whoever he is waiting for. Behind him: a low
concrete wall, a concrete bench, a tree throwing a HARD-EDGED midday shadow cut sharp
across the ground, worn hydraulic tile pavement.

[BLOCO-PRESERVAR]
[BLOCO-LUZ-BH]
[BLOCO-GENTE]
[BLOCO-HDR]
[BLOCO-FOCO]
[BLOCO-FOTO-AMADORA]

Avoid: [NEGATIVOS-COM-GENTE], redrawn label, altered logo, changed lettering
```

**`alt`:** `Kit com os três cafés Canastra numa praça em Belo Horizonte`
**Risco:** o pior caso de fidelidade de rótulo — **três embalagens legíveis num
quadro**, seguradas por uma mão, num agachamento. Se `n=6` não devolver um
acerto, **componha localmente**: gere a cena sem os pacotes e cole os três
recortes reais por cima. É a única rota com tipografia garantida, e para um
ladrilho de presente vale o esforço.

---

### `CAMP-01` — banda destaque · São Paulo

| | |
|---|---|
| **Arquivo** | `cafe-especial-todo-dia-sao-paulo.jpg` · 16:9 · Gemini 2K |
| **Elenco** | `diego-19` — sentado, **olhar direto na lente** · `--n` 4 |

Este é o contraponto urbano do herói, e é onde o vermelho `#C4231E` da marca
entra — **uma vez por dobra**, na camiseta de time de várzea.

**Decisão de direção deliberada:** meio-dia sob a **sombra dura da marquise**,
não seis e meia da manhã. A luz de amanhecer é a saída fácil e é justamente o
dourado que o projeto trata como assinatura de IA.

**Espaço para texto:** o texto desta banda fica **abaixo** da foto, centrado
(bloco 5 da home). A foto não precisa de zona escura — mas precisa de ar à
direita para o recorte 16:9 não cortar o Diego ao meio.

```
Phone photo at a bus shelter on the far east side of São Paulo at midday. A 19-year-old
Brazilian man with deep brown skin, very black hair and eyebrows, a thin unformed
moustache, ACTIVE ACNE on the forehead and along the jaw, a full lower lip, a face that
has not finished growing. His hair is cut short with a shaved part on one side and more
length on top. He sits on the metal bench of the shelter, elbow on his knee, body loose
with no advertising tension, a small cheap plastic vacuum flask standing on the ground
beside his foot, cheap earphones wound around one hand, a trace of ballpoint ink on his
index finger. He wears a faded RED amateur-football shirt with NO readable text, number or
crest anywhere on it, grey sweat shorts above the knee, thick-soled white trainers that
are scuffed but well kept, a flat dark cap worn backwards, a digital watch. He looks
STRAIGHT INTO THE LENS, chin level, mouth closed, no smile and no scowl - firmness without
invitation, he is not offering anything. He sits in the HARD-EDGED SHADOW cast by the
shelter canopy, with the sunlit street beyond. Behind him a painted wall, a concrete post,
bundled overhead cable. NO billboards, NO large signage, NO LED panels anywhere - street
advertising does not exist in this city.

[BLOCO-HDR]
[BLOCO-FOCO]
[BLOCO-FOTO-AMADORA]

Avoid: [NEGATIVOS-COM-GENTE], golden hour, dawn light, warm glow, team crest,
club badge, readable jersey number
```

**`alt`:** `Rapaz esperando o ônibus na zona leste de São Paulo com uma garrafa
térmica de café`
**Risco:** a camiseta de time. O modelo **vai** tentar desenhar escudo e número,
e vão sair como rabisco ilegível — ou, pior, parecidos com um clube real, que é
marca de terceiro. Por isso `team crest`, `club badge` e `readable jersey number`
estão negados, e por isso a camiseta é descrita como *faded, no readable text*.
Confira o peito com zoom.
**Sem bloco de luz:** a cena é sombra dura de marquise ao meio-dia e está
descrita no corpo. Não acrescente `BLOCO-LUZ-SP` — o encoberto contradiz a
sombra dura pedida aqui.

---

### `CLUBE-01` — o clube

| | |
|---|---|
| **Arquivo** | `clube-assinatura-de-cafe-especial.jpg` · 4:3 · Gemini 2K |
| **Elenco** | `wesley-31` — em trânsito, três-quartos · `--n` 4 |

**Esta é a única imagem quente da página.** O `estetica.md` põe o Clube em
superfície `mata`, que é a única seção escura do miolo — e a regra de olhar do
elenco reserva o calor para cá: **sorriso iniciado e não concluído**, canto da
boca subindo, olho enrugando, olhando para fora de quadro. Sorriso incompleto
também elimina o risco de dente, que é o terceiro modo de falha mais frequente.

```
Phone photo outside the entrance of an ordinary apartment building in Belo Horizonte on an
overcast afternoon. A 31-year-old Black Brazilian man, medium-dark skin, round face, full
eyebrows, uneven short stubble along the jaw, hair cut low with a barbershop fade and a
sharp lined edge. He is CAUGHT IN MOTION, stepping down off the entrance step onto the
pavement, a plain cardboard subscription box tucked under his left arm and a phone in his
right hand, a strip of first-aid tape around his index finger, a short thin silver chain
at his neck. He wears a faded forest-green cotton t-shirt cut slightly large, grey cargo
trousers with one side pocket bulging, and cheap running trainers with dirty soles. No
lanyard, no badge, no corporate uniform. His mouth is STARTING a smile that never
completes - one corner rising, the eye creasing - and he is looking out of frame to the
side, NOT at the camera, LIPS CLOSED with no teeth visible. The box is closed and carries
NO printing and NO label of any kind. Behind him: a metal gate, worn hydraulic tile,
a flat institutional beige wall with a scuffed skirting board, bundled overhead cable.

[BLOCO-LUZ-SP]   ← encoberto; a luz cinzenta funciona igual em BH em dia fechado
[BLOCO-GENTE]
[BLOCO-HDR]
[BLOCO-FOCO]
[BLOCO-FOTO-AMADORA]

Avoid: [NEGATIVOS-COM-GENTE], printed box, shipping label, brand logo on box,
open mouth smile, visible teeth
```

**`alt`:** `Entregador saindo com a caixa da assinatura do Clube da Canastra em
Belo Horizonte`
**Risco:** a caixa é pedida **sem impressão nenhuma** porque não existe arte real
de caixa. Caixa lisa é honesta; caixa com logotipo desenhado pelo modelo é sósia
da marca.
**Movimento:** "caught in motion" descreve **pose**, não borrão. A home da Nike
tem movimento zero e borrão não se desfaz em pós — `motion blur` está na lista
negativa. Se alguma variante vier borrada, descarte.
**Wesley é o personagem-ponte:** ele é o único do elenco que aparece na
torrefação de Uberlândia **e** na cidade. Se um dia a banda "Do pé à xícara"
ganhar retratos por etapa, é ele que fecha a de torra.

---

### `HERO-ALT` — bloqueado pela Trava 2

Este era o herói. É a imagem mais forte que este briefing produziu e **não pode
ser gerada hoje**: uma cena de terreiro de secagem afirma como a operação
funciona, e não existe uma única foto de terreiro no acervo para conferir se é
de cimento, que forma têm as leiras, se há rastelo, se há cereja madura naquela
época. `POLITICA-IA.md §2` proíbe exatamente isso, e `docs/briefing-captura.md`
já lista colheita e terreiro como saída de campo pendente.

**A ideia, preservada para quando destravar:** `dulce-52` parada no meio de uma
passada de rastelo, as duas mãos no cabo, olhar direto na lente, olhos
semicerrados pelo sol de cima. Não é pose, é pausa — a tradução exata do herói
da Nike, onde a atleta está sentada num banco de vestiário. E é ela quem
**decide** a hora de virar o lote, o que inverte o clichê que a ONU Brasil
mapeou na publicidade nacional: protagonismo negro subiu de 7% para 20%, mas
segue aparecendo como mão-de-obra passiva.

**Dois caminhos de desbloqueio, em ordem de preferência:**

1. **Fotografar.** Uma ida à fazenda na safra resolve o terreiro, a colheita e
   os packshots que faltam de uma vez. Com termo de imagem assinado, resolve
   também a Trava 1 para esta peça.
2. **Confirmação escrita de quem opera**, item por item: existe terreiro? é de
   cimento? as leiras têm essa forma? em que época há cereja vermelha? Registrada
   no briefing. Isso destrava a Trava 2, mas **não** a Trava 1 — o rosto continua
   dependendo de a política mudar.

Risco de geração, para quando chegar a hora: **cabelo 4C** é onde o modelo mais
erra, porque os datasets pesam para liso e ondulado e o material rotulado como
cabelo negro é majoritariamente afro brilhoso de salão. Nomeie o padrão, o
comprimento, a irregularidade da linha de implantação e a **ausência de brilho**;
negue `salon afro` e `glossy hair`; confira a linha do cabelo com recorte
ampliado, que é onde o erro aparece primeiro.

---

## 10. Riscos legais e éticos

| Risco | O que fazer |
|---|---|
| **Painel de Portinari na Pampulha** | Sob direito autoral até **2033**. Fora de peça comercial — e nenhum destes oito briefings o inclui. |
| **Mural e pichação identificáveis** | Obra autoral de terceiro. `graffiti mural` está na lista negativa. Empena cega crua, sim. |
| **Serra do Curral** | Carrega disputa pública sobre mineração. `HERO-01` a mostra como horizonte, sem tema. Se a marca não quiser o assunto perto dela, troque por uma crista genérica do entorno de BH. |
| **Marca de terceiro entrando por acidente** | Ônibus, fachada de loja, placa. Confira cada variante com zoom antes de aprovar. |
| **Semelhança com pessoa real** | Nenhuma variante pode sair parecida com alguém identificável — família Boaventura inclusive. Descarte a variante, não "ajuste". |
| **Declaração de conteúdo gerado** | Decisão do dono. Estas oito imagens são cena gerada com pessoas fictícias; três delas carregam pixel real de embalagem. Registre isso onde a marca declara o que é foto e o que não é. |

---

## 11. Conferência antes de subir

1. **Mãos** com zoom — dedos contados, articulação conferida
2. **Faixa de texto do rótulo** com zoom — nos três que têm embalagem
3. **Rosto a 100%** — poro, assimetria, catchlight, dente
4. **Direção da sombra vs. especular** — medida, não assumida
5. **Zona de texto do herói** — luminância relativa WCAG no quarto
   inferior-esquerdo. **≥7:1 para texto em `cal`, ou a imagem volta.**
6. **Perfil de câmera** — `p1` perto de 14, saturação perto de 70, cast R/B
   perto de 0,969. O passe de pós é **mínimo, só saturação**: duas tentativas de
   calibração completa já saíram net-negativas neste projeto.
7. **Peso** — herói ≤ 250 KB servido em desktop, AVIF com fallback WebP
8. **Nome do arquivo** — kebab-case com palavra-chave, como na tabela de cada
   briefing
