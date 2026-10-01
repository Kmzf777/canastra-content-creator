---
name: canastra-estatico
description: Use when producing a Café Canastra static feed post — cartão de produto, carta sensorial, cartão de procedência, peça 4:5 para o feed — or when a generated package image has a wrong label and needs to be corrected until it is right.
---

# Estático — o catálogo declarado e a escada de correção

Esta skill manda no **laço de correção** e no **catálogo**. Não manda no fluxo nem na
conferência: isso é de `canastra-conteudo`.

## Rotear primeiro

| Assunto | Dono |
|---|---|
| fluxo de 5 fases, mecânica do ChatGPT via Chrome, racionalizações de conferência | **canastra-conteudo** |
| fidelidade do rótulo, qual face fotografar, âncora de família | **canastra-embalagem** |
| realismo de cena, procedência da referência | **canastra-cena** |
| **o catálogo declarado e qual degrau subir quando o rótulo sai errado** | **esta skill** |

---

## O catálogo é dado, nunca improviso

Peça nova é **linha em `instagram/estaticos/catalogo.py`**, não uma conversa.

```bash
python -m uv run python -m instagram.estaticos conferir   # antes de gerar
python -m uv run python -m instagram.estaticos listar
python -m uv run python -m instagram.estaticos prompt <slug> --correcao soletrar
```

`conferir` devolve **1** quando a declaração tem problema, e recusa peça com
`Dado.origem` vazia. Isso é proposital: quebra qualquer script que ignore o relatório
e siga gerando.

### Uma declaração, três consumidores

`strings_impressas` alimenta, da mesma fonte: o **bloco de soletração do prompt**, o
**checklist da conferência** e as **asserções do laudo**. É por isso que ela é dado.
Quando a lista é memória do agente, ele a remonta na hora — e foi assim que um campo
fisicamente ilegível virou `✓ confere`.

### Os dois campos de texto não se misturam

| Campo | Quem produz | Como se garante |
|---|---|---|
| `strings_impressas` | **geração**, a partir da foto real | conferência ampliada campo a campo; falhando até o teto, composição |
| `dados` | **código**, no Remotion | exato por construção — não tem foto de onde vir |

Preço, altitude e local são `dados`. Pedir ao modelo para escrever texto nosso produz
um sósia (lição 1).

### Embalagem gerada funciona — a proibição não é a proteção

96 packshots de `saida-teste/catalogo-estudio/` saíram por geração e foram aprovados;
a lição 12 registra os 3 SKUs indistinguíveis da fonte num blend a 50%. **A embalagem
entra por geração.** O que a protege é mandar a referência certa e conferir letra por
letra, com a composição como rede.

`assets/materialidade/LEIA-ME.md` diz que a embalagem "nunca nasce ali" — isso é
escopo **daquela pasta**, não do pipeline. Não leia como proibição de arquitetura.

---

## A escada de correção

Cada linha é uma falha já paga neste repositório. Sintoma novo é linha nova no
registro de lições, **não palpite** — `rotear()` levanta `KeyError` de propósito.

| Degrau | Sintoma | Correção | Origem |
|---:|---|---|---|
| 1 | valor inventado (`70` onde é `7,0`) | soletrar a string | lição 18 |
| 1 | acento perdido (`ARABICA`, `DOCURA`) | soletrar o acento | lição 21 |
| 2 | rótulo genérico, sósia | `EDIT THE PROVIDED PHOTOGRAPH` + mostrar a frente | lições 1 e 12 |
| 3 | fonte crua ruim, baixa resolução | âncora de outro SKU da família | canastra-embalagem |
| 4 | letra corrompida (`Doodo 1985`) | aumentar o pacote no quadro | lição 13 |
| 5 | erra ~1 em 3 sem padrão | gerar N variantes e escolher | site_fundo_branco.py |
| 6 | sobreviveu ao teto | **compor o pixel real por cima** | recorte/ + preservacao.ts |
| 6 | lote, validade, QR, código de barras | **nunca aceita gerado** | lição 22 |

### O teto é 3 e o degrau 6 é o piso, não o fracasso

Não insista em prompt num campo que a lição 13 diz que não sobrevive: **abaixo de ~2%
da altura do quadro a tipografia não sobrevive em nenhuma rodada.** Insistir não
converge, só gasta geração. O degrau 6 não depende do modelo — é por isso que o laço
termina sempre.

### Lote, fabricação, validade e QR nunca entram

Vão direto ao degrau 6 ou **saem do enquadramento**. Já saiu `F:23.2025`, um mês que
não existe, e `F:12.2025`, plausível. **O plausível é pior, porque passa** — e em peça
de e-commerce é informação regulatória falsa.

---

## A emenda entre veredito e sintoma é você

Nada mapeia um no outro automaticamente, e isso é deliberado — classificar o erro é
julgamento de quem olha:

```
conferir.recortes()  -> você OLHA os pares ampliados
você                 -> veredito por campo: ok | errado | nao-verificavel
conferir.bloqueia()  -> diz quais campos barram
você                 -> nomeia o sintoma de cada campo barrado
escada.executar()    -> roteia o degrau
```

Não procure uma função `veredito_para_sintoma`. Ela não existe e não deve existir.

**`nao-verificavel` barra a peça junto com `errado`.** Ilegível não é aprovação, é
ausência de leitura.

---

## Bandeiras vermelhas — pare

- Você marcou `ok` sem abrir o **recorte ampliado** daquele campo.
- Você não consegue apontar **em que pixel da referência** leu o valor.
- Você está prestes a declarar um `Dado` sem `origem`.
- Você está escrevendo `strings_impressas` **de memória**, sem ampliar a arte.
- Você está prestes a aceitar um lote, uma validade ou um QR gerado.

A quarta já aconteceu, em 30/09/2026, **dentro deste módulo**: a primeira peça do
catálogo nasceu com `"CLÁSSICO"` e `"TORRADO EM GRÃOS"` declaradas de memória, quando
o selo real diz **`"CLÁSSICO EM GRÃOS"`** e **`"TORRA EXCLUSIVA"`** — e `"Desde 1985"`,
a string da lição 13, nem estava na lista. Gabarito não conferido no pixel não é
gabarito.

---

## Duas restrições de ambiente

- **Este pacote não roda em worktree.** Ele lê `fotos produtos cru/` e `saida-teste/`,
  que são gitignored e vivem só no diretório principal.
- **Há frequentemente outra sessão neste repositório.** Antes de tocar em
  `instagram/remotion/` ou no `CLAUDE.md`, confira `git status` e o mtime. Commit com
  **caminhos explícitos**, nunca `git add -A` (lição 9).
