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
| `element.click()` por JS em **botão que navega ou submete** | **não** |
| Clique real no chevron, no campo, no Confirmar | sim, com a receita acima |
| Abrir o **Editor em massa** | **não** — o menu abre, os itens não levam a lugar nenhum |
| Definir valor por `setter` nativo do React | **não** — o campo reverte |

**A aba degrada.** Depois de ~6 anúncios editados nela, o acordeão para de abrir e o
screenshot estoura o tempo. **Abra uma aba nova a cada 3 ou 4 anúncios.**

---

## Fato não explicado — cuidado aqui

**O título grava nas caixas de 10 e não nos kits de 40.** Mesma receita, Confirmar azul
conferido no DOM, contador certo, nenhum erro — e o título antigo permanece nos 4 kits.

Hipótese **não testada**: os kits podem ter variação de anúncio, e título de anúncio com
variação talvez grave por outro caminho.

**Se você for mexer em título de kit, teste e registre o resultado aqui.**

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
