# Biblioteca de aprendizados de conteúdo

Posts e vídeos (Instagram, TikTok e YouTube) que **ensinam a fazer** algo — uma técnica de
edição, uma estratégia de conta, um jeito de gravar — guardados como ficha para consultar antes
de criar. Diferente de `instagram/referencias-virais/`, que mapeia **o que viralizou** e como foi
montado, aqui o foco é **o que o post ensina e como aplicar na Canastra**.

As fichas entram pelo canal `#conteudo` do Discord: o Rafael cola o link, escolhe a classe, e
uma sessão do Claude abre o post, vê de fato (o vídeo inteiro, quadro a quadro) e grava a ficha
aqui. Também podem ser escritas à mão, no mesmo modelo.

Num vídeo editado, **o visual é o que se aprende**: legenda, cenário, enquadramento, formato e
ritmo valem tanto quanto a fala. A ficha registra os dois, e o visual vem com print.

| Pasta | Classe | O que entra |
|---|---|---|
| `edicao/` | `apr-edicao` | técnica de edição, motion, legenda, transição, som, ferramenta de edição |
| `estrategia/` | `apr-estrategia` | estratégia de conta, formato, frequência, gancho, roteiro, métrica, crescimento |
| `outro/` | `apr-outro` | o que não cabe nas duas (gravação, luz, celular, fotografia, negócio) |

Nome do arquivo: `<perfil>_<id do post>.md`, perfil sem `@` (ex.: `fulano_DKrnvXvt72X.md`;
no TikTok, o número do vídeo; no YouTube, `<canal>_<id de 11 caracteres>`). As fichas **não**
entram no índice de `scripts/indice_referencias.py`.

Prints da ficha: `quadros/<perfil>_<id>/` dentro da mesma pasta da ficha, por exemplo

```
estrategia/
  fulano_DKrnvXvt72X.md
  quadros/
    fulano_DKrnvXvt72X/
      01_00-00.webp
      02_00-07.webp
```

## Modelo da ficha

```markdown
---
url: https://www.instagram.com/reel/XXXXXXXXXXX/
plataforma: instagram            # instagram | tiktok | youtube
perfil: "@fulano"
data: 2026-10-13                 # data de publicação; se não aparecer: não verificável
classe: apr-edicao               # apr-edicao | apr-estrategia | apr-outro
comentario: "texto do Rafael quando colou o link, literal (vazio se não houve)"
---

# @fulano — <o que o post ensina, em uma linha>

## O que ensina

Duas a cinco frases: a ideia central e por que ela funciona, nas palavras do post (sem
inflar). Formato do post (vídeo de N s, carrossel de N imagens) e números visíveis
(views, curtidas) com a data em que foram lidos.

## Mapa do vídeo

Vídeo inteiro visto em folhas de contato a 2 qps (13/13 folhas).

Uma linha por bloco: troca de cenário, de estilo de legenda ou de capítulo. Cobre do primeiro
ao último segundo, sem buraco.

| Tempo | Cenário / plano | Fala | O que a tela faz | Print |
|---|---|---|---|---|
| 0:00–0:03 | bastidor vertical cheio, plano aberto | — | texto nativo de Reels em 2 linhas, emoji | ![](quadros/fulano_ID/01_00-00.webp) |
| 0:03–0:15 | 16:9 com faixas pretas, sala com TV, plano médio | "o primeiro ponto…" | legenda palavra a palavra, branca pequena | ![](quadros/fulano_ID/02_00-07.webp) |
| 0:15–0:31 | cozinha com janela, plano médio | "…presta atenção…" | palavra-chave gigante creme atrás do corpo | ![](quadros/fulano_ID/03_00-19.webp) |

(Carrossel: a coluna Tempo vira `img N/M`. Post estático sem vídeo: "não se aplica".)

## Passo a passo

1. Os passos como o post ensina, na ordem. Em carrossel, indique a imagem (`img 3/7`).
2. Passo que o post pula ou deixa implícito vai marcado como `(inferido)`.

## Linguagem visual

Cada item com print ou tempo.

- **Formato:** vertical cheio no gancho, depois 16:9 com faixas pretas até o fim — escolha de
  linguagem (celular cru → "cinema"), não defeito de download — ![](quadros/fulano_ID/02_00-07.webp)
- **Cenários:** um por capítulo (trem, sala com TV, cozinha, sofá); a troca de cenário marca a
  troca de assunto.
- **Câmera e enquadramento:** câmera fixa, plano médio centrado, olhar na lente.
- **Sobreposições / colagens:** exemplos entram como recortes flutuantes ao lado do rosto quando o
  assunto é citado e saem com ele — `[00:22]`.
- **Ritmo de corte:** corte a cada frase (~1,5 s); jump cut dentro do mesmo plano.
- **Cor e luz:** luz natural de janela, tons quentes, sem gradação forte.

## Legendas e texto na tela

Um bloco por *sistema* de legenda (não um por frase). Quando o estilo muda por capítulo,
registre cada estilo e onde ele vale.

### Sistema 1 — gancho nativo
- Onde/quando: 0:00–0:03 · posição: centro-alto · fonte aparente: fonte nativa do Reels · cor:
  branca · contorno preto fino · duas linhas fixas · sem animação · emoji no fim.
- Por que funciona aqui: parece post "cru" de celular, não anúncio; segura antes da virada para 16:9.
- ![](quadros/fulano_ID/01_00-00.webp)

### Sistema 2 — palavra a palavra, estilo por capítulo
- Onde/quando: 0:03–1:18 · uma a três palavras por vez · sem fundo · sem serifa arredondada.
- Capítulo 1 (0:03–0:15): branca pequena, embaixo — ![](quadros/fulano_ID/02_00-07.webp)
- Capítulo 2 (0:15–0:31): creme enorme **atrás do corpo** (recorte da pessoa na frente) só nas
  palavras-chave — ![](quadros/fulano_ID/03_00-19.webp)
- Fecho: rosa claro empilhado na vertical — `[01:12]`
- Metalinguagem: ao falar de "headline simples", a legenda vira por um instante a fonte nativa no
  topo — `[00:41]`.
- Por que funciona aqui: …

## Ferramentas

- Só as que o post mostra ou nomeia (app, plugin, equipamento, preset), com o momento em que
  aparecem. Ferramenta deduzida pela aparência vai marcada como `(presumida)`.

## Citações com tempo

- `[00:03.5]` "frase exata dita ou escrita na tela"
- `img 2/7` "texto do slide"

## Como reproduzir

Receita concreta com o que temos, não conselho genérico.

- Gravação: celular vertical 9:16 4K, um cenário por capítulo, sobra de espaço em cima da cabeça
  para a legenda atrás do corpo.
- Edição (Remotion/CapCut): letterbox 16:9 a partir de 0:03; legenda palavra a palavra a partir
  da transcrição com tempo; recorte de pessoa (máscara) para a palavra-chave ficar atrás do corpo;
  paleta de legenda por capítulo definida antes de editar.
- O que precisa existir antes: …

## Onde se aplica na Canastra

- Em que peça, formato ou etapa do nosso processo isso entra (Reel de motion, carrossel
  "Céu a pino", estático, Mercado Livre…), e o que precisaria adaptar. Concreto, com o que
  temos hoje (ver `CLAUDE.md` e as skills `canastra-*`).

## Cuidados com as regras da marca

- O que NÃO copiar. Confira contra a **lição 66 do `CLAUDE.md`**: humor e metáfora só de
  dentro do café (nada de comida ou objeto alheio); torra nunca com fogo, fumaça ou grão preto.
- Conteúdo de terceiro nunca vira pixel da Canastra nem imagem de referência para geração;
  rosto de pessoa real nunca é sintetizado.

## Arquivos locais

- Onde ficou a mídia baixada para análise (scratchpad) e quais prints foram salvos em
  `quadros/<perfil>_<id>/`.
```

## Regras

- **Só o que foi visto.** Campo ilegível, cortado ou que a ferramenta não entregou é
  `não verificável` (com o motivo), nunca um valor plausível. Carrossel: todas as imagens,
  uma a uma; vídeo: inteiro (todas as folhas de contato), com transcrição (skill `watch`)
  quando houver fala. Se o script de quadros falhar, as seções visuais ficam
  `não verificável (<motivo>)` — não se descreve visual de memória.
- **Toda afirmação visual aponta para um print ou um tempo.** "Legenda creme atrás do corpo"
  sem `![](…)` ou `[mm:ss]` não entra.
- **Portão da transcrição.** Palavra duvidosa da transcrição é conferida contra o quadro do
  mesmo tempo antes de ser corrigida ou marcada como erro (muitas vezes a palavra está escrita
  na tela).
- **Mídia no repositório: só prints escolhidos em WebP.** Gerados por
  `central-claude/scripts/conteudo/quadros.mjs salvar` (720 px de largura, no máximo 20 por
  ficha), em `quadros/<perfil>_<id>/` ao lado da ficha. Em carrossel, os prints são as
  imagens-chave (mesmo limite, mesma pasta). Vídeo, áudio e folhas de contato ficam no
  scratchpad; a ficha guarda o link para rever o original. Todo `![](…)` da ficha precisa
  existir em disco.
- Copiar a técnica e a estrutura é o uso previsto; copiar roteiro, bordão ou enquadramento
  reconhecível de um criador, não.
- Sem commit automático: quem grava a ficha não mexe no git. O Rafael revisa e faz o commit.
