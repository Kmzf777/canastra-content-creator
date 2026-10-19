---
name: canastra-mercadolivre
description: Use when operating the Mercado Livre seller panel through the browser — editing a listing's price, type, shipping, title, ficha técnica or description, reading account data, or checking whether a change actually saved. Covers the mechanics that fail silently and the recipe that works.
---

# Operar a Central do Mercado Livre

**O formulário do ML grava, mas falha em silêncio.** Clique que não chega, campo que
fica inválido, seção que fecha quando você acha que abriu — e **nunca aparece erro**. Esta
skill é a mecânica medida em 30/09/2026 editando os 7 anúncios de cápsula.

Contexto de negócio da conta: [`mercadolivre/LEIA-ME.md`](../../mercadolivre/LEIA-ME.md).
Estado da aplicação: [`mercadolivre/11-folha-de-aplicacao.md`](../../mercadolivre/11-folha-de-aplicacao.md).

---

## A regra que não se negocia

> **Nada é alterado no ML sem autorização explícita do Rafael, na conversa.**

Ele autoriza por item. Autorização para preço não vale para título. E **nunca reative
anúncio** sem ele pedir — é a instrução mais repetida desta conta.

Ler é livre. Escrever, não.

---

## A receita que funciona

Quatro passos. Pular qualquer um faz falhar sem avisar.

| # | Passo | Como |
|---|---|---|
| 1 | **Abrir a seção** | Clicar no **chevron**, à direita do card. **Uma vez só.** |
| 2 | **Esperar** | Até **19 segundos**. Verificar por JS se o campo ficou visível |
| 3 | **Limpar o campo** | **Clique triplo.** Nunca `Ctrl+A` |
| 4 | **Gravar** | Confirmar azul → clicar → **conferir na lista de anúncios** |

### Por que `Ctrl+A` quebra
O `Ctrl` não registra e sobra a letra **`a`** no início do campo. Vi
`aClássico, Suave e Canela` num screenshot. O campo fica inválido, o **Confirmar não
submete, e nenhum erro aparece.** Perdi várias rodadas achando que era limitação do site.

### Por que clicar duas vezes fecha
O acordeão demora para renderizar. Você lê o DOM, não acha o campo, clica de novo — e o
segundo clique **fecha** a seção. Clique uma vez e espere.

### Coordenada de clique
O frame de clique é **1366px** e o viewport pode ser outro. **Calcule `1366 / innerWidth`**
antes de clicar por coordenada, ou tire um screenshot e leia o alvo nele. Num Chrome o
fator era 0,667 e eu errava todos os alvos.

```js
// sempre confira antes de confiar numa coordenada
({ fator: (1366 / innerWidth).toFixed(3), vw: innerWidth })
```

---

## Verificar se gravou — a parte que mais engana

**A recarga do formulário mente.** O ML tem **atraso de propagação**: um título apareceu
como não gravado em quatro recargas seguidas e depois estava lá. Refiz trabalho à toa e
cheguei a escrever no repositório que "não grava".

**Confira na lista de anúncios**, que lê de outra fonte:

```
https://vendedores.mercadolivre.com.br/anuncios/lista?search=<termo>
```

E **espere alguns minutos** antes de concluir que falhou.

---

## O que funciona e o que não funciona pela automação

| Ação | Funciona? |
|---|---|
| Ler qualquer coisa (`javascript_tool`, `get_page_text`, `read_page`, `find`) | **sempre** |
| `element.click()` por JS em **checkbox e radio** | sim |
| `element.click()` por JS no **chevron do acordeão** | **sim** — medido 04/10/2026, dispensa o `wait` de 19 s |
| `element.click()` por JS em **"Excluir foto"** | **sim** |
| `element.click()` por JS em **botão que navega ou submete** | **não** |
| Clique real no chevron, no campo, no Confirmar | sim, com a receita acima |

A fronteira não é "JS não funciona": **JS funciona em controle local de estado**
(acordeão, excluir, checkbox) e **falha no que submete**. O Confirmar continua exigindo
clique real.

Dois detalhes que quebram automação em lote:

- os **`aria-label` mudam a cada re-render** (`D_NQ_NP_…-F.jpg` → `D_Q_NP_…-G.jpg`), então
  guardar uma lista de botões e clicar em todos opera em refs mortos;
- um **laço síncrono pega o mesmo botão N vezes**, porque o React só re-renderiza no fim do
  tick. Uma chamada por ação, relendo o DOM.
| Abrir o **Editor em massa** | **não** — o menu abre, os itens não levam a lugar nenhum |
| Definir valor por `setter` nativo do React | **não** — o campo reverte |

**A aba degrada.** Depois de ~6 anúncios editados nela, o acordeão para de abrir e o
screenshot estoura o tempo. **Abra uma aba nova a cada 3 ou 4 anúncios.**

---

## Fotos — mecânica medida em 04/10/2026

| Coisa | Como é |
|---|---|
| input | `input[type=file]` dentro do acordeão **Fotos**, `multiple`, aceita jpg/png/webp |
| cada foto | `button.media-uploader__element-primary-action`, com `img` dentro; a ordem do DOM **é** a ordem do anúncio |
| capa | é a **posição 1**, marcada `FOTO DE CAPA`. Não existe botão "tornar principal" |
| excluir | `button[aria-label^="Excluir foto"]` — `.click()` por JS funciona |
| arrastar | `button[…--drag]` HTML5; **não testado**. Evite: ordene pela ordem de upload |

**Suba uma imagem por chamada.** `file_upload` com 3 caminhos entregou na **ordem
inversa** — pedi `.6, .8, .7` e o anúncio ficou `.7, .8, .6`, com o detalhe virando capa.
Em miniatura de 120 px isso não salta aos olhos.

**Adicione antes de remover**: o campo é obrigatório e não aceita ficar vazio.

**Limite de 10 fotos por anúncio.** Com 7 antigas, suba 3 novas, remova as antigas e só então
complete. **Remova esperando o botão sair do DOM** antes do próximo clique — é o que funcionou em
08/10/2026; cliques seguidos em intervalo fixo caem no mesmo botão antes do re-render:

```js
for (let k = 0; k < 3; k++) {
  const b = [...sec.querySelectorAll('button[aria-label^="Excluir foto"]')].find(antiga);
  if (!b) break; b.click();
  for (let i = 0; i < 10 && document.contains(b); i++) await new Promise(r => setTimeout(r, 500));
}
```

**`file_upload` pode reportar erro e ter subido assim mesmo** (*"Page still loading… document_idle"*).
Releia a lista de `aria-label` antes de reenviar, senão a foto entra em dobro. E o `aria-label`
traz o **nome do arquivo** enviado (`Excluir foto 22.1-kit-….png`) até o Confirmar: é a forma mais
barata de conferir a ordem.

**Não pré-formate a imagem.** O ML faz **trim da margem branca** e reduz a altura para
1200 — subi 1448×1448 e ele guardou 1031×1200. As variantes quadradas da grade (`-S` 90,
`-Q` 284, `-V` 320, `-W` 568) ele gera sozinho. Mande o 3:4 do catálogo com fundo branco.

Para conferir o que o servidor guardou, baixe do CDN com `curl` e UA de Chrome:
`https://http2.mlstatic.com/<id>-F.jpg` é a versão cheia.

---

## Título dos kits — resolvido em 07/10/2026

**O título grava nos kits, sim.** Em 30/09 ele "não gravava" nos 4 kits de 40; em 07/10 gravou
de primeira nos 4, com a mesma receita (clique triplo → digitar → Confirmar azul), toast
*"1 anúncio foi alterado com sucesso"* e título novo **na lista de anúncios**. A hipótese da
variação não se confirmou. A causa provável de 30/09 é a mesma família de falhas desta skill
(aba degradada, clique que não chegou), não uma regra do ML.

---

## Aba oculta — o clique é "feito" e nada entra

Medido em 07/10/2026. Quando a janela do Chrome com o grupo de abas do Claude está atrás de
outra ou minimizada, `document.visibilityState` é `hidden` e:

- `screenshot` estoura 30 s;
- `triple_click` e `type` **voltam com sucesso e o texto não entra no campo**;
- o acordeão aberto por JS fica com altura 0 — o React não termina a animação sem render.

**Receita:** antes de escrever, leia `document.visibilityState`. Se `hidden`, peça ao Rafael
para deixar a janela visível. E **tire um screenshot antes do primeiro clique** de cada seção:
ele força o render e foi o que destravou cliques que não entravam.

**Medido de novo em 08/10/2026, e é pior que "não entra":** com a janela oculta, no Suave 1 kg,
o `type` **entrou** em todos os campos (o `value` conferia, o atacado até recalculou o `%`) e os
quatro Confirmar mostraram *"1 anúncio foi alterado com sucesso"*. A **ficha** gravou e apareceu
na página pública em menos de 1 min. O **atacado** e a **descrição** não gravaram: 6 min depois,
formulário recarregado e página pública seguiam antigos. Ou seja, oculto, o resultado **varia
por seção** e o aviso de sucesso não distingue. Regra: com `hidden`, não edite; e confira cada
seção na página pública, uma por uma, nunca pelo aviso.

**Não feche a última aba do grupo.** Fechar a aba em que se estava trabalhando desfaz o grupo;
o próximo `tabs_context_mcp` cria grupo novo **em outra janela**, que nasce oculta. Para "aba
nova", crie a nova antes e navegue nela — ou simplesmente reuse a mesma aba: em 07/10 uma aba só
aguentou 4 kits sem degradar.

### Atacado tem teto, e o erro só aparece no balão do ícone vermelho

Medido em 11/10/2026 no Suave 1 kg (R$ 109,90, frete grátis R$ 34,30). O ML **obriga** o preço de
atacado a repassar a economia de frete do pedido grande: *"Deve ser R$90,72 ou menos, pois você
economiza R$19,17 nos custos de envio"* (10 un) e R$ 95,34 / R$ 14,56 (5 un). Teto = preço −
economia de frete por unidade. Acima disso o campo ganha um **ícone vermelho** discreto, o texto só
aparece com `hover` no ícone, e o Confirmar **não grava** — em 08/10 isso passou como "não gravou
por causa da janela oculta". Antes de confirmar atacado, passe o mouse em cada ícone vermelho e
leia o teto. O balão tem um link **Aplicar** que põe o teto no campo.

O "atacado configurado" e o "atacado na vitrine" são números diferentes: a vitrine aplica os 20%
OFF do Pix por cima (99,99 vira 79,99). Leia o configurado no formulário.

Marca e outros atributos de lista o ML **normaliza** para o valor do cadastro dele: `Café Canastra`
gravou e voltou `Cafe Canastra`; `100% arábica` voltou `100% Arabica`. Não adianta redigitar.

### Descrição: `select()` por JS + `type` real

Clique triplo num `textarea` seleciona só um parágrafo. O que funcionou: clique real no campo,
`t.focus(); t.select()` por JS (estado local — funciona) e então `type` com o texto inteiro.
O `type` de ~2.500 caracteres **estoura o tempo da ferramenta (30 s) mas termina**: espere
~10 s e confira `t.value.length` contra o tamanho do texto antes de confirmar.

### Seção que "abre" mas não abre

O input da seção pode existir no DOM com a seção fechada. Confira
`button.accordion-container__toggle[aria-expanded]`, não a presença do campo.

---

---

## Raspar a busca de concorrentes — medido em 08/10/2026

**A busca não trava depois da primeira consulta.** Rodei 16 buscas seguidas por `navigate`.
O que parecia trava era a **janela oculta**: a lista fica no spinner e o DOM volta sem
nenhum `poly-card`. Um `screenshot` (mesmo a 0,15 de escala) força o render.

| Passo | Como |
|---|---|
| 1 | `navigate` para `lista.mercadolivre.com.br/<termo-com-hifens>` |
| 2 | `wait` 3 s → `screenshot` → `wait` 3 s |
| 3 | `eval(localStorage.__ext2)` — extrator em [`mercadolivre/scripts/extrator_busca.js`](../../../mercadolivre/scripts/extrator_busca.js) |
| 4 | no fim, **aba nova** em `lista.mercadolivre.com.br` e um único download do `__acc` |

Três armadilhas que custaram rodadas:

- **Saída do `javascript_tool` trunca em ~1.000 caracteres.** Não tente devolver a tabela
  por ali; acumule e baixe.
- **Um download automático por aba** (lição 52 do `CLAUDE.md`). O segundo some sem erro.
- **`localStorage` é por origem.** O que foi gravado em `lista.` não existe em `www.` nem em
  `vendedores.` — baixe de uma aba que esteja em `lista.`.

O preço grande do card é o **preço Pix**; o de "outros meios" é ~R$ 10 acima. O card **não**
mostra se o vendedor é Full quando a busca vem pelo contexto "Full Super" — a tag `SUPER`
separa esses.

### Vendas de um anúncio num período

`vendedores.mercadolivre.com.br/vendas/omni/lista?search=<id>` e trocar o período no
combobox (opções até **"Último ano"**). Um aviso modal ("Ao filtrar por data…") aparece na
primeira vez — fechar em **Entendi**. O motivo de "Afeta sua reputação" está em **Ver
detalhe → Ver histórico da venda** (ex.: *"Você atrasou o envio desta venda"*). Não grave
nome nem CPF de comprador em arquivo; para medir recompra, conte apelidos distintos.

---

## Onde ficam as coisas

| Preciso de… | URL |
|---|---|
| editar um anúncio | `mercadolivre.com.br/anuncios/MLB<id>/modificar` |
| lista filtrada | `vendedores.mercadolivre.com.br/anuncios/lista?search=<termo>` |
| Central de promoções | `vendedores.mercadolivre.com.br/anuncios/lista/promos` |
| reputação | `vendedores.mercadolivre.com.br/metricas/meu-atendimento/detalhes?reputation=true` |

**Não adivinhe URL.** Já perdi tentativas com `/promocoes/hub` e `/promocoes/list`, que não
existem. Pegue o link do menu da Central:

```js
[...document.querySelectorAll('a[href]')]
  .map(a => ({t: (a.innerText||'').trim().slice(0,40), h: a.href}))
  .filter(o => /promo|anuncio|metrica/i.test(o.t + o.h))
```

### Seletores úteis

| Campo | Seletor |
|---|---|
| título | `#title_input` |
| preço | `input[aria-label="Informar preço BRL"]` |
| descrição | `#description_input` |
| marca | `#primary_tech_specs_task-BRAND` |
| linha | `#primary_tech_specs_task-LINE` |
| tipo de anúncio | `input[name^="listing_types"]` — `gold_special` = Clássico, `gold_pro` = Premium |
| frete | `input[name*="shipping-options"]` — id com `me_buyer` = comprador paga |
| cabeçalho de seção | `div.accordion-container__header` |
| acordeão de tipo | `button.andes-accordion-header` |
| chevron do frete | `button.shipping-options__accordion-chevron` |

---

## Ler dados da conta

**A API pública não serve mais:** `api.mercadolibre.com/items/MLB<id>` devolve **403** sem
autenticação. Leia pelo DOM da Central, com a sessão logada.

**Não confie em contador de card.** Os cards de status ficam num carrossel e o número que
você captura pode ser o do card vizinho. Li "14 anúncios inativos por descumprir políticas"
numa passagem e "1" em outra, no mesmo lugar, e registrei o 14 como fato em três arquivos.
**Para contar anúncios por status, filtre a lista e conte as linhas.**

O **painel de custos** do formulário é fonte de medição confiável — mostra tarifa, custo de
envio e "Você recebe" por preço e tipo. Foi assim que descobri que o frete grátis custa
R$ 14,45 e não os R$ 20,00 que estavam estimados.

---

## Regras do próprio ML que travam edição

| Regra | Consequência |
|---|---|
| **Título: 60 caracteres** | O contador do formulário mostra `60 / 60`. É real |
| **"Compatível" é obrigatório** em produto compatível com marca alheia | Sem ele: *"O título sugerido omite que as cápsulas são compatíveis com Nespresso, alterando a identidade do produto"* e **o Confirmar desabilita** |
| **Descrição não é indexada** | Só título, ficha técnica e características alimentam a busca do ML *(diegorojasseller, `KPvPvwmTUC8`)* |
| **Sem link, telefone, e-mail ou WhatsApp** na descrição | O ML remove o anúncio |
| **Preços de atacado**: só CNPJ vê, até 5 faixas | Faixa maior que o estoque nunca dispara |
| **Promoções exigem reputação verde ou amarela** | Em vermelho a Central fica bloqueada, com 0 anúncios elegíveis |

**Antes de levar um trade-off ao cliente, confira se as duas opções existem.** Pedi ao
Rafael para escolher entre "Café Especial" e "Compatível" no título — e "Compatível" é
obrigatório. A escolha nunca existiu, e ele decidiu errado por causa da minha pergunta.
Restrição de plataforma se descobre submetendo; o formulário recusa de graça.

---

## Antes de declarar que algo falhou

1. Conferiu na **lista**, não na recarga do formulário?
2. Esperou alguns minutos pela propagação?
3. Olhou o **conteúdo do campo num screenshot**? (foi assim que achei o `a` do `Ctrl+A`)
4. A aba está degradada — já tentou uma **aba nova**?
5. O **fator de escala** está em 1,0?

Só depois disso escreva que não funciona. Eu pulei esses passos e registrei como limitação
da plataforma uma falha que era do meu método.
