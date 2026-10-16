# Máquina de ganchos — design

Data: 15/10/2026 · Fluxo 5 de 5 (série Kallaway) · Aprovado pelo Rafael nesta sessão.

## Objetivo

Ganchos com base em dado, que não soem como texto de IA. Quatro passos:

1. extrair ganchos de dado real
2. agrupá-los em padrões
3. montar uma rubrica de 15 a 20 regras
4. usar a rubrica para:
   - (a) **gerar** ganchos novos para um tema, com nota
   - (b) **avaliar** um gancho do Rafael e propor alternativas com nota maior

A rubrica deve poder ser recalibrada pelo resultado dos nossos próprios posts, mas
funciona hoje sem esse dado.

## Escopo

- **Formatos:** capa de carrossel (manchete + linha de apoio + foto) e Reel (três camadas:
  visual, tela, fala). As regras têm um tronco comum e um bloco por formato.
- **Fora do escopo:**
  - editar `instagram/estrategia/*`, porque o fluxo 2 está escrevendo lá. Mudanças
    sugeridas viram proposta.
  - escrever em `instagram/metricas/`, que é do fluxo 1. Ali este projeto só **lê**.
  - mexer no repositório central-claude. A mudança no `promptPauta` vira texto proposto.

## Dado disponível (inventário de 15/10/2026)

| Fonte | O que tem | Limite |
|---|---|---|
| `instagram/referencias-virais/videos/*/*.md` (130) | seção `## 2. Gancho` com vê / escrito / dito + views e curtidas em `indice.json` | só Reel; **só vencedores**; views podem incluir alcance pago (`organico`) |
| `saida-teste/carrossel-*/sidecar.json` (diretório principal, gitignored) | nossos carrosséis; `casca-no-cafe` publicado em 14/10 | sem métrica ainda |
| `instagram/metricas/proprios.jsonl` (fluxo 1) | alcance, views, curtidas, comentarios, saves, shares, tempo_medio_assistido_s, seguidores_conta, `gancho`, coletado_em; 1 linha por post por coleta | **ainda não existe**: o token da Meta não tem escopo de Instagram |
| `instagram/metricas/concorrentes/<handle>.jsonl` (fluxo 1) | legenda + curtidas por post | futuro; fonte de corpus de carrossel |

O parser das fichas trata **8 variantes de rótulo**: `Vê-se:`/`Vê:`/`VÊ:`/`O que se vê:`/
tabela `O que se VÊ`. O mesmo vale para escrito e para dito ou ouvido.

## Arquitetura

| Arquivo | Papel | Quem escreve |
|---|---|---|
| `.claude/skills/canastra-ganchos/SKILL.md` | quando usar, os dois modos, passo a passo, formato da resposta | à mão |
| `.claude/skills/canastra-ganchos/rubrica.md` | **fonte única** das regras: tabela com `id`, `tipo`, `formato`, `peso`, verificação e fonte marcada | à mão; o script lê a tabela |
| `.claude/skills/canastra-ganchos/vicios-ia.md` | léxico e estruturas de texto de IA, com incidência medida no corpus pt | à mão; os números vêm do script |
| `scripts/ganchos.py` | `extrair` · `padroes` · `checar` · `recalibrar` | código |
| `instagram/ganchos/corpus.jsonl` | 130 ganchos de Reel + nossos carrosséis | `extrair` |
| `instagram/ganchos/padroes-mapa.json` | id do corpus → padrão (julgamento) | à mão |
| `instagram/ganchos/padroes.md` | padrões com n, mediana de views, exemplos literais, e as medidas do corpus | `padroes` |
| `instagram/ganchos/avaliacoes.jsonl` | todo gancho gerado ou avaliado, com nota por regra e `escolhido` | `checar --registrar` e a skill |
| `tests/test_ganchos.py` | parser, regras mecânicas, recalibração | código |

### Nota

- **Portões** (tipo `portao`): qualquer falha dá nota **0** e devolve o motivo.
- **Regras pontuadas** (tipo `mecanica` ou `julgamento`): os pesos somam **100** para cada
  formato. Uma regra de formato `capa` não conta num Reel, e o peso é renormalizado.
- **Mecânicas:** o script decide passa ou falha.
- **Julgamento:** o Claude decide, com uma justificativa de uma linha por regra.
- A resposta mostra a nota **regra por regra**.

### `checar`

```
python scripts/ganchos.py checar --formato capa --manchete "..." [--apoio "..."]
python scripts/ganchos.py checar --formato reel --fala "..." [--tela "..."]
```

Imprime os portões e as regras mecânicas, com o subtotal e as regras de julgamento que
ficaram pendentes. `--json` serve para máquina e `--registrar --tema T` anexa o resultado a
`avaliacoes.jsonl`.

### Modos da skill

- **Gerar** (entrada: tema, formato, matéria-prima existente):
  1. Escreve cerca de 10 candidatos, de **padrões diferentes** e não variações de uma frase.
  2. Roda `checar` em cada um.
  3. Julga as regras restantes.
  4. Entrega os 3 a 5 melhores, com nota decomposta e a pergunta que cada um abre.
- **Avaliar** (entrada: gancho do Rafael):
  1. Dá a nota decomposta.
  2. Propõe 3 alternativas, cada uma atacando a regra mais fraca, todas com nota maior.
  3. Se nenhuma superar o original, diz isso em vez de forçar.

### Recalibração

`recalibrar`:

1. Lê `instagram/metricas/proprios.jsonl` e pega a última linha por `id`.
2. Cruza o `gancho`, com texto normalizado, com `avaliacoes.jsonl`.
3. Calcula o resultado:
   - **(saves + shares) / alcance**, porque envios é sinal oficial
   - secundário: curtidas / alcance
   - Reel: `tempo_medio_assistido_s`
4. Para cada regra, compara a mediana de quem passou com a de quem falhou.
5. Decide:
   - **n < 8** posts cruzados: escreve "amostra insuficiente" e não propõe nada.
   - n ≥ 8: grava `instagram/ganchos/recalibracao-AAAA-MM-DD.md` com pesos propostos
     (limitados a ±50% do atual, soma renormalizada a 100) e as regras candidatas a subir de
     [criador] para [medido].

**A rubrica só muda com aprovação do Rafael.** Arquivo ausente é aviso, não erro.

## Limites declarados na skill

- O corpus só tem vencedores. Ele mostra o que os virais **têm em comum**, não o que separa
  o viral do fracasso. A comparação dentro da amostra (top 25% contra o resto) é fraca e
  vai marcada como tal.
- O corpus é todo de Reel. As regras de capa começam como [criador] + [leitura minha]
  (transferência), e quem as torna [medido] é a recalibração.
- A nota é **hipótese**, não previsão (`03-roteiro.md` §5).

## Entregas

1. A skill, a rubrica, o script, os testes, o corpus e os padrões.
2. Ganchos gerados para os 4 carrosséis "a definir" entre 20/10 e 30/10, a partir da fila
   de pauta de `instagram/agenda.md`, apresentados ao Rafael.
3. Uma nota em `side-session-notes/…` com a mudança proposta para o `promptPauta` de
   `src/agentes/instagram/prompts.ts` (central-claude), que deve passar a usar a skill na
   aprovação da pauta.
4. Propostas de mudança para `instagram/estrategia/` como texto, sem editar.
5. **Sem commit** até o Rafael pedir.

## O que a implementação mudou (15/10/2026)

- **17 regras, não 18.** "Fala com você" (M5) saiu: só 11,8% das aberturas pt dos virais usam
  segunda pessoa **[medido]**. O registro está em `rubrica.md`, "O que ficou fora".
- **As faixas de palavras vêm do corpus:** capa com 2–9 palavras, fala com 5–13, tela com 2–7
  (p25–p75). A capa também respeita o `ORCAMENTO` de `instagram/carrossel/molde.py` (60/120
  caracteres), e um teste confere.
- **J6 ficou restrita a 7 padrões:** no recorte café, `marca-clima` (mediana 113 mil) e
  `objeto-impossivel` (281 mil) ficam muito abaixo dos outros (1,4–5,3 mi).
- **Os nossos carrosséis entram como avaliações, não no corpus**, porque o sidecar não guarda o
  texto da capa. Sementes: `casca-no-cafe` (publicado, `DefH_1ClN30`) e `canastra-endereco`.
- **Texto sem aspas nas fichas é descrição e não conta como gancho.** As 26 ocorrências foram
  conferidas.
- **O cruzamento com o fluxo 1 é feito primeiro pelo shortcode** (`url` do post × `post` da
  avaliação) e depois pelo texto, que o fluxo 1 copia de `instagram/metricas/ganchos.json`.
