# Pesquisa: por que a imagem sai irreal

Levantamento feito em 04/10/2026 para o alvo **conteúdo natural de Instagram** —
stories, post "estou na fazenda", produto na cozinha, primeiro frame de POV de
óculos, barista passando café. **Não** é para packshot de estúdio: o catálogo tem
alvo oposto e não deve herdar nada daqui.

## Procedência de cada afirmação

Este documento mistura fontes de peso muito diferente. A coluna vale mais que o
conteúdo, então ela vem primeiro.

| Marca | Significa |
|---|---|
| `[PRIMÁRIO]` | documentação da OpenAI (`developers.openai.com`) |
| `[FÓRUM]` | relato de usuário em `community.openai.com`, com post citado |
| `[LÉXICO]` | descrição de LoRA no Civitai — é vocabulário de quem treina em foto real, não medição |
| `[INFERÊNCIA]` | conclusão minha, não medida por ninguém |
| `[SONDAR]` | hipótese que custa pouco testar e **ainda não foi testada aqui** |

Nada abaixo foi verificado nas nossas próprias gerações. Enquanto não for,
**é hipótese**, não regra — e regra deste repositório é lição medida.

---

## 1. O diagnóstico: o eixo é amador↔profissional, não "qualidade"

A melhor formulação do nosso problema não vem de guia de prompt nenhum, vem da
descrição de um *slider* de LoRA. `[LÉXICO]` — Civitai, "Amateur ↔ Professional
Photography", SDXL concept slider:

> Polo **profissional**: *"controlled lighting and exposure, stronger composition,
> polished colour and contrast, purposeful framing, subject presentation and the
> visual finish associated with commercial, editorial and professional photography."*
>
> Polo **amador**: *"available light, incidental composition, ordinary camera
> placement, less controlled exposure and colour, candid presentation and the
> imperfections characteristic of personal snapshots."*
>
> E a frase que resolve a confusão: *"The slider is intended to change how a
> photograph appears to have been **made**, rather than simply adding or removing
> photographic quality."*

**Isto reenquadra o sintoma.** "Sai irreal" não é falta de grão, de ruído ou de
câmera nomeada. É que o prompt descreve uma fotografia **produzida**. E os nossos
prompts de cena descrevem exatamente isso, por herança do catálogo:

- `enquadramento()` em `scripts/prompts_catalogo.py:56` pede *"centred, even margins
  left and right, base a little below centre"* → `purposeful framing`, polo profissional;
- `instagram/estaticos/prompt.py:71` pede `"The package occupies about 45% of the
  frame height"` → composição deliberada;
- `ESTUDIO` pede softbox, bounce card e kicker → `controlled lighting`.

Para packshot isso está **certo**. Para "foto tirada na lavoura" está invertido:
cada uma dessas frases empurra a imagem para o polo errado. `[INFERÊNCIA]`

### O corolário desconfortável

Enquadramento centrado e margem par são o que torna a peça **usável** no feed.
Então o conflito é real: realismo pede enquadramento incidental, e o molde pede
enquadramento previsível. A saída provável é a mesma da lição 31 — **resolver na
geometria do molde, não no prompt**: gerar com enquadramento frouxo e folga, e
recortar depois para o 4:5. `[INFERÊNCIA]`

---

## 2. A camada de plataforma: o ChatGPT reescreve o nosso prompt

Este é o achado operacional mais caro, e ele não está em nenhum guia de prompt.

`[FÓRUM]` — @Daller, post #1 da thread *"Collection of GPT-image-generator 2.0
issues, bugs, and work-around tips"* (343 posts), categoria Prompting:

> *"It is very important to suppress the ChatGPT prompt enhancing! Because you want
> to see what the prompts exactly do. If GPT changes the prompts, it will not be
> your prompt that created the image. You can ask ChatGPT to show you the prompt
> send to the image generator, to check what it actually get."*

A receita dele, literal:

```
(format 1536x1024.) (don't change the prompt, send it as it is.)
```

E a ressalva honesta, do mesmo post: *"it could be that, in the background after
ChatGPT has sent the prompt, the prompt is improved a second time if it is
considered insufficient… apparently nothing is known about this yet."*

Confirmação independente, `[FÓRUM]` @LarisaHaster, thread *"Sudden severe drop…"*
#11: o ChatGPT Work *"uses the image-generation skill to refine the prompt before
sending the final prompt to gpt-image-2."*

**Por que isso importa tanto aqui.** Nós escrevemos prompt de 3.840 caracteres
(lição 34) com âncoras físicas calibradas, e **não temos nenhuma prova de que o
modelo de imagem recebeu esse texto.** Pode estar recebendo um resumo reescrito.
É a lição 3 — *HTTP 200 não prova que o parâmetro funcionou* — na camada de UI:
a imagem voltar não prova que o prompt chegou.

`[SONDAR]`, e é a sonda mais barata que existe: pedir ao ChatGPT que **imprima o
prompt que ele enviou** e comparar com o nosso, caractere a caractere. Custa uma
mensagem e zero geração.

### Reuso de estado entre imagens da mesma conversa

`[FÓRUM]` @Daller #3 e #23: o gerador reaproveitava dados das imagens anteriores,
amplificando padrão de ruído em 3–5 imagens e devolvendo **a mesma imagem** para o
mesmo prompt. Corrigido em dias (#21), mas @Daller mantém: *"The noise is still
there, and it can still amplify if you reuse pictures."* @Schlorboodungus (#22, #24)
seguia vendo degradação progressiva na mesma conversa **sem** reusar imagem.

E o mais relevante para nós, `[FÓRUM]` @summerstay #11:

> *"if you do not use any reference images or previous images in the chat, it can do
> very high quality without any artifacts."*

@scohissto #15, o contrário: *"I'm having the exact same issues even on the very
first generation, whenever I have used a reference image."*

**Consequência direta para o nosso fluxo:** `canastra-conteudo` manda abrir aba
nova por fluxo, mas nada proíbe gerar várias imagens na mesma conversa — e é
exatamente o que a geração de catálogo faz. Isso pode estar degradando as imagens
2 em diante sem deixar rastro. `[INFERÊNCIA]`

Mitigação citada: **recarregar a página / conversa nova por imagem**, e
`LESS DETAILS` no prompt para reduzir o padrão (sugestão de @Timebender, no
post #1). O post #1 é explícito que o ruído em si **não** se resolve por prompt:
*"NO FIX POSSIBLE: The issue is technical and cannot be fixed with prompting!"*

### Atrator de template: o modelo tem composição favorita

`[FÓRUM]` @showaemergency, thread *"Has ChatGPT image quality suddenly declined?"*
#12 e #31. Usuário de produção, meses no mesmo prompt. Depois de uma troca de
modelo, o mesmo prompt passou a devolver *"nearly identical layouts, compositions,
lighting, backgrounds, regardless of iteration, prompt changes or done in separate
new chats"* — e a linha `*Do not reference previous image generations.*` **não**
resolveu.

O que resolveu, #31:

> *"I prompted characters walking in a park, and no matter the prompt, no matter the
> different scene description, the park always had a lake in the background with a
> skyline, whether I wanted it to or not… So, I rewrote the prompt and specifically
> said 'No lakes, no skyline' — and sure enough, the next prompt was better."*
>
> *"creating prompts — at least for the time being — might be built around just as
> much time telling it what you don't want vs. what you do want."*

Isto é a **nossa lição 8** descoberta de novo por outra pessoa (o carrossel que saiu
em madeira azul porque o prompt não proibia superfície pintada). A diferença é a
dose: ele está dizendo que a negação deixou de ser conserto pontual e passou a ser
metade do prompt.

Para nós o atrator previsível é o que `canastra-cena` já catalogou — dourado quente,
produto em pé, bokeh, mesa posta — mais os que ainda não nomeamos para cada cena
nova. Cozinha vai puxar bancada de mármore e luz de janela grande; lavoura vai puxar
golden hour e fileira infinita. `[INFERÊNCIA]`

### Tamanho e qualidade

`[FÓRUM]` post #1, com a referência da API: no ChatGPT os tamanhos são
**1024×1024, 1536×1024, 1024×1536**, e é recomendado pedir a razão em pixels exatos.
`[INFERÊNCIA]` nosso feed é **4:5 (1080×1350, razão 0,8000)** e **não** existe nessa
lista — 1024×1536 é 2:3. Então feed sai de `1024×1536` com recorte, pela mesma
aritmética da lição 23 e do `canastra-cena`. Não existe 4:5 nativo aqui, como não
existia na xAI.

`[FÓRUM]` @LarisaHaster (#9, #11 de *"Sudden severe drop"*) e @Mindbender777 (#7):
`quality: low` é visivelmente pior que `medium`, sobretudo em anatomia e detalhe
fino. Vários relatos de que **gerar muito rápido/muito volume degrada** a saída
(@PaulBellow, repetido em três threads).

---

## 3. Imagem de referência: o que a OpenAI documenta e o que os usuários medem

### A mecânica documentada `[PRIMÁRIO]`

Do guia de prompting de imagem e do cookbook:

- **Nomeie cada entrada por número e papel.** *"Identify each input by number and
  purpose: subject, style, clothing, or background. Explain how the inputs should
  combine."* Formato: `"Image 1: product photo… Image 2: style reference…"`
- **Para edição, diga o que NÃO muda.** *"say 'change only X' and list the details
  to preserve, such as identity, geometry, layout, lighting, or labels."*
- **O que o modelo preserva** quando instruído: layout, perspectiva, geometria,
  identidade, ângulo de câmera, luz/sombra, posição dos objetos, **legibilidade do
  texto do rótulo**.
- **Itere com uma mudança por vez** — *"small, single-change follow-ups"* — e
  **repita as restrições críticas em cada iteração**, porque elas derivam.
- Fidelidade de entrada: `input_fidelity: high` existe no 1.5/1.0; nas versões 2.x
  a entrada é sempre processada em alta fidelidade e o parâmetro não existe. (É
  parâmetro de **API**; não temos controle dele pelo ChatGPT.)

Isto valida a nossa lição 12 por outro caminho: em **modo de edição com preservação
nomeada**, o rótulo sobrevive. A frase que já usamos — `EDIT THE PROVIDED
PHOTOGRAPH` + `KEEP THE PACKAGE PIXEL-FOR-PIXEL IDENTICAL` — é exatamente o padrão
que a documentação prescreve.

### O modo de falha que mais nos ameaça

`[FÓRUM]` thread *"Why won't image 7 control the pose?"*. Um usuário montou um
script maximalista — 7 referências, `HARD LOCK` em tudo, `FAIL CONDITION`,
`→ Image 1 overrides everything` — e **não funcionou**. O diagnóstico, @LarisaHaster #2:

> *"The prompt itself is probably contributing to the problem. It combines several
> instruction templates, repeats steps, contains unfinished placeholders and marks
> many competing requirements as 'hard locked' or highest priority. The model does
> not treat those phrases as technical controls. **When everything is critical, the
> intended priority becomes unclear.**"*
>
> Receita dela: *"start with a much shorter prompt… Once the pose and framing are
> correct, add the outfits, vehicle and background through separate edits."*

E o suporte da OpenAI, #3: *"Exact pose or identity locks aren't guaranteed."*

**Este é um aviso direto contra o nosso instinto.** A reação natural ao "sai irreal"
é empilhar mais um bloco: `CAMERA/PHONE DETAILS`, `RAW/Unedited`, `IMPERFECTIONS`.
Nossos prompts de cena já passam de 3.800 caracteres e já carregam `LABEL FIDELITY`
em letra maiúscula com seis proibições. Somar três blocos novos pode **reduzir** a
aderência de tudo, inclusive da fidelidade de rótulo que hoje funciona.

A direção sustentada pelas duas fontes é a oposta: **prompt mais curto, uma
operação por vez, correções por edição sucessiva.**

### A contradição que precisa ser resolvida por teste, não por opinião

Duas fontes competentes dizem o contrário uma da outra sobre **descrever vs. anexar**:

| Fonte | Posição |
|---|---|
| Vídeo YouTube `gEHe1-1futI` [09:05] (relato de terceiro, não conferi os frames) | **descrever vence**: anexar referência *"puxa traços indesejados da foto base"*; melhor subir a foto, pedir ao modelo que escreva o prompt dela, e editar o texto |
| `[FÓRUM]` @showaemergency #38, usuário de produção | **anexar vence**: *"providing reference material to the type of aesthetics, filmic look, lens / optical characteristics, depth of field, etc you want, **as opposed to describing it in a prompt**, is yielding better results lately"* — e *"still described it in some detail, but not overly complex"* |

`[INFERÊNCIA]` A contradição provavelmente não é contradição, é **escopo**:

- **identidade do rótulo** → anexar, em modo edição. Medido aqui, lição 12.
- **estética/óptica/luz** → anexar como referência de *look*, descrevendo pouco.
  É o que #38 relata.
- **conteúdo da cena** (o que está na foto) → descrever. Anexar foto de cena alheia
  arrasta a cena inteira.

Isto também é a regra de camadas de `base-curada/`: `03-mood-terceiros` serve para
**descritor textual** e nunca entra como pixel. Ou seja, para a nossa base a
pergunta "descrever ou anexar?" já está respondida por licença, não por qualidade —
o que é estética alheia só pode ser descrito.

### A rotina de recalibração por versão de modelo

`[FÓRUM]` @showaemergency #31 e #34. Quando o modelo trocou, seis meses de prompt
refinado viraram pó. O que ele fez:

1. abriu conversa com o modelo de texto, em inglês coloquial;
2. anexou **as próprias gerações antigas boas** e referências da estética desejada;
3. perguntou: *"How would I achieve image generations with the same photorealistic
   film quality in GPT images 2.5?"*;
4. pediu explicitamente **linguagem de prompt que funcione naquela versão**;
5. reconstruiu os prompts com esse vocabulário.

Ressalva dele mesmo: *"I don't think there's a general 'one question fixes it all'
type approach here."* E #38: **não** use o modelo de raciocínio (Astra) para gerar —
gasta crédito e não é para isso; gerar na seção de imagens.

`[INFERÊNCIA]` Para nós isso tem um valor específico: nós **temos** o que ele tem —
96 packshots aprovados e 38 fotos reais verificadas com EXIF. Esse acervo é
exatamente o insumo dessa rotina.

---

## 4. Léxico: as palavras que quem treina em foto real usa

`[LÉXICO]` — tudo desta seção é *trigger word* ou descrição de LoRA de realismo no
Civitai. São modelos locais (Flux, SDXL, Z-Image, Krea), **não** o gerador do
ChatGPT. Vale como vocabulário a testar, não como garantia.

### Puxa para o polo amador

| Termo | Fonte |
|---|---|
| `amateurish photo` | UltraRealistic Lora Project (85k downloads) |
| `overexposed` · `underexposed` · `in motion` · `low lighting` | idem |
| `smeared background` · `smeared foreground` | idem |
| `hard flash` · `camera flash` · `flash photography` | InstaPic (19k) |
| `smartphone photo` · `shot on iphone` · `phone camera` | idem |
| `candid` · `candid snapshot` | InstaPic, Candid Realistic Snapshot |
| `mirror selfie` · `high-angle` · `low-angle` | Realistic Snapshot (86k) |

A frase-gatilho mais instrutiva do conjunto, porque é uma oração inteira e não uma
tag — `[WAN2.1] Smartphone Snapshot Photo Reality`:

> *"early 2010s snapshot photo captured with a phone and uploaded to facebook,
> featuring dynamic natural lighting, and a neutral white color balance with
> **washed out colors**"*

**Convergência com a nossa medição.** `washed out colors` e `neutral white color
balance` são, em palavras, as duas colunas que `scripts/home_medir.py:perfil` já
mediu na nossa base: saturação lavada (packshot ~59, lavoura ~86) e cast de altas
R/B 0,969, puxando **azul**. Duas evidências independentes apontando para o mesmo
lugar — a nossa é medida, a deles é descritiva.

### Descrição do nosso alvo anti-bokeh, por outra pessoa

`SOAP photo enhancer [Shot On A Phone]`, sobre o SDXL:

> *"I love SDXL. But the 'photos' it creates are soooo… DRAMATIC! Always with dark
> tones, soft lighting, and shallow depth of field. Do you ever just want photos
> that look like you took them on a phone: sharp, bright colors, and everything in
> focus?"*

É o bloco anti-bokeh de `canastra-cena` escrito por um estranho. O viés para
"dramático" é do modelo, não do nosso prompt — e por isso precisa ser negado
explicitamente, não apenas não-pedido.

### POV de primeira pessoa — e o erro padrão que ele comete

Relevante para o frame inicial do POV de óculos. `Krea 2 Raw｜True First-Person POV`
declara qual problema existe: prompts comuns geram *"背后跟拍、第三人称自拍、镜头高度不自然"* —
**acompanhamento por trás, selfie em terceira pessoa, altura de câmera não natural**.
Ou seja: pedir "POV" devolve um plano por cima do ombro. O vocabulário de correção:

```
true first-person POV
true first-person eye-level POV, natural standing eye height, normal human-eye perspective
true first-person seated POV, natural seated eye height
```

E de `POV First Person [FLUX]`: `first person POV shot of` … `shot at eye level`,
com o padrão de citar **as duas mãos** na moldura baixa. O autor observa que
funciona junto com LoRA de amateur photography.

`[INFERÊNCIA]` óculos Meta **não** é POV de olho: a câmera fica na haste, deslocada
para um lado, campo mais largo e altura de testa — não de olho. Nada nas fontes
cobre isso. Se formos fazer esse frame, a assinatura óptica tem que sair de foto ou
vídeo real do aparelho, e até lá o atributo é `não verificável`, pela regra da
lição 32.

---

## 5. O que recusar

- **Passe de pós para "envelhecer" a imagem** — grão, light leak, dust & scratches,
  eco de scanner. Nossa lição 7 mediu passe completo saindo **net-negativo**. E o
  alvo daquele material é Polaroid dos anos 90; o nosso é iPhone 7 ao meio-dia.
- **`$f/5.6$`** (cifrão em volta da abertura, do vídeo [02:35], justificado como
  *"por algum motivo"*). Entra como `[SONDAR]` A/B, nunca como regra.
- **Script maximalista com `HARD LOCK`** — a thread do *image 7* é a prova de que
  não funciona.
- **Gerar na conta logada em várias abas ao mesmo tempo** — a lição 37 já pagou:
  o rascunho e os anexos do composer são **compartilhados entre abas**.

---

## 6. Sondas, em ordem de custo

Nenhuma gastou geração ainda. As três primeiras custam uma mensagem cada.

1. **O prompt chega inteiro?** Pedir ao ChatGPT que imprima o prompt enviado ao
   gerador e comparar com o nosso. Se vier reescrito, toda a calibração de bloco é
   teatro até resolvermos isso. **Esta é a sonda que vale mais.**
2. **`(don't change the prompt, send it as it is.)` muda o que chega?** Mesma
   comparação, com e sem a linha.
3. **Pedir vocabulário à própria versão do modelo**, anexando nossos packshots
   aprovados e nossas fotos de Medeiros, com a pergunta do @showaemergency adaptada.
4. **Conversa nova por imagem vs. várias na mesma conversa** — mesmo prompt, mesma
   referência, medir com `scripts/home_medir.py:perfil`. Decide se o nosso fluxo de
   catálogo degrada a partir da segunda imagem.
5. **Prompt curto com referência de look vs. prompt longo descritivo** — o teste que
   resolve a contradição da seção 3.
6. **Bloco de negação explícita por cena** (`no marble countertop, no golden hour,
   no lake, no skyline`) contra o mesmo prompt sem ele.

---

## Fontes

- `[PRIMÁRIO]` https://developers.openai.com/cookbook/examples/multimodal/image-gen-1.5-prompting_guide
- `[PRIMÁRIO]` https://developers.openai.com/api/docs/guides/image-prompting
- `[FÓRUM]` https://community.openai.com/t/collection-of-gpt-image-generator-2-0-issues-bugs-and-work-around-tips-check-first-post/1379535 (343 posts)
- `[FÓRUM]` https://community.openai.com/t/has-chatgpt-image-quality-suddenly-declined/1395431 (38 posts)
- `[FÓRUM]` https://community.openai.com/t/sudden-severe-drop-in-chatgpt-image-quality-and-reference-adherence/1388368 (42 posts)
- `[FÓRUM]` https://community.openai.com/t/why-wont-image-7-control-the-pose/1387960
- `[FÓRUM]` https://community.openai.com/t/poor-quality-in-realistic-images/1324424
- `[LÉXICO]` Civitai API, consultas `amateur photography` · `ultrareal` · `phone photo realism` · `snapshot realism` · `boring photography` · `POV first person`
- Vídeo YouTube `gEHe1-1futI` — relato de terceiro (Gemini assistiu; **não** conferi os frames)

**Reddit não entrou.** `r/StableDiffusion` é citado como origem de várias dessas
descobertas, e devolve **403 com página anti-bot de 190 KB** para `curl` com UA de
Chrome, para `.json` e para `api.reddit.com`; a extensão do Chrome barra o domínio
por permissão. Rota possível: liberar `reddit.com` nas permissões da extensão.
Contornar detecção de bot está fora de escopo (lição 16).
