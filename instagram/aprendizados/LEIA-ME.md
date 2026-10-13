# Biblioteca de aprendizados de conteúdo

Posts e vídeos (Instagram e TikTok) que **ensinam a fazer** algo — uma técnica de edição, uma
estratégia de conta, um jeito de gravar — guardados como ficha para consultar antes de criar.
Diferente de `instagram/referencias-virais/`, que mapeia **o que viralizou** e como foi
montado, aqui o foco é **o que o post ensina e como aplicar na Canastra**.

As fichas entram pelo canal `#conteudo` do Discord: o Rafael cola o link, escolhe a classe, e
uma sessão do Claude abre o post no Chrome, vê de fato e grava a ficha aqui. Também podem ser
escritas à mão, no mesmo modelo.

| Pasta | Classe | O que entra |
|---|---|---|
| `edicao/` | `apr-edicao` | técnica de edição, motion, legenda, transição, som, ferramenta de edição |
| `estrategia/` | `apr-estrategia` | estratégia de conta, formato, frequência, gancho, roteiro, métrica, crescimento |
| `outro/` | `apr-outro` | o que não cabe nas duas (gravação, luz, celular, fotografia, negócio) |

Nome do arquivo: `<perfil>_<id do post>.md`, perfil sem `@` (ex.: `fulano_DKrnvXvt72X.md`;
no TikTok, o número do vídeo). As fichas **não** entram no índice de
`scripts/indice_referencias.py`.

## Modelo da ficha

```markdown
---
url: https://www.instagram.com/reel/XXXXXXXXXXX/
plataforma: instagram            # instagram | tiktok
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

## Passo a passo

1. Os passos como o post ensina, na ordem. Em carrossel, indique a imagem (`img 3/7`).
2. Passo que o post pula ou deixa implícito vai marcado como `(inferido)`.

## Ferramentas

- Só as que o post mostra ou nomeia (app, plugin, equipamento, preset), com o momento em que
  aparecem. Ferramenta deduzida pela aparência vai marcada como `(presumida)`.

## Citações com tempo

- `[00:03.5]` "frase exata dita ou escrita na tela"
- `img 2/7` "texto do slide"

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

- Onde ficou a mídia baixada para análise (scratchpad). Mídia de terceiro **não** entra no
  repositório.
```

## Regras

- **Só o que foi visto.** Campo ilegível, cortado ou que a ferramenta não entregou é
  `não verificável` (com o motivo), nunca um valor plausível. Carrossel: todas as imagens,
  uma a uma; vídeo: inteiro, com transcrição (skill `watch`) quando houver fala.
- **Só texto e análise vivem aqui.** Vídeos, quadros, áudios e imagens de terceiros ficam fora
  do repositório; a ficha guarda o link para rever o original.
- Copiar a técnica e a estrutura é o uso previsto; copiar roteiro, bordão ou enquadramento
  reconhecível de um criador, não.
- Sem commit automático: quem grava a ficha não mexe no git. O Rafael revisa e faz o commit.
