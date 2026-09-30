# Os sete anúncios

> **Escopo fechado.** O Rafael pediu explicitamente para trabalhar **apenas** com estes 7
> e **editar os existentes — não criar novos**. IDs verificados no DOM da conta.
>
> **Nada foi aplicado.** Autorizado: tudo menos reativar.

---

## Achados de 30/09/2026 que afetam estes 7

| Achado | Consequência |
|---|---|
| **Certificado digital vence 30/09** | *"Seus anúncios Full serão pausados amanhã."* Renovar antes de qualquer edição |
| **Central de promoções bloqueada** (reputação) | **0 anúncios** elegíveis. Os preços desta página são os **cheios**, e é o único cenário disponível hoje. A escada de promoção de [`02-economia-e-precos.md`](02-economia-e-precos.md) só existe depois do verde — ver [`09-remessa-e-estrategia-de-preco.md`](09-remessa-e-estrategia-de-preco.md) |
| **Inativos por política: leitura instável** | Li **14** numa passagem e **1** em outra, no mesmo contador do painel. **Não confie em nenhum dos dois** — filtre a lista por "Inativos por descumprir políticas" e conte. Os **7 em escopo** estão todos inativos por **falta de estoque** (*"Não há mais unidades à venda"*), conferido anúncio por anúncio |

---

## Aviso sobre os IDs

Os prints enviados pelo Rafael tinham **dois dígitos trocados** em relação ao sistema.
Os corretos, lidos do DOM da Central:

| No print | No sistema (correto) |
|---|---|
| `2692127645` | **`2692127545`** |
| `2691993580` | **`2691993380`** |

**Sempre confirmar ID no DOM antes de editar.** Editar o anúncio errado é irreversível.

---

## Estado hoje → como fica

Todos em **SUPERMERCADO**, **Inativo**, **sem estoque** no Full e no depósito.
Todos passam para **Clássico** (hoje 6 dos 7 estão em Premium).

### Caixas de 10 — comprador paga o frete

| ID | Título novo | Chars | Preço | Resultado |
|---|---|---:|---|---|
| `2692127545` | `Cápsulas Café Especial Canastra Clássico Nespresso 10un` | 55 | 28,90 → **34,90** | −4,70 → **+12,82** |
| `2692082114` | `Cápsulas Café Especial Canastra Suave Nespresso 10un` | 52 | 18,70 → **34,90** | −1,35 → **+12,82** |
| `2692076338` | `Cápsulas Café Especial Canastra Canela Nespresso 10un` | 53 | 18,70 → **34,90** | −1,35 → **+12,82** |

Margem: **36,7%**.

**A mudança que vira a chave no `2692127545`:** hoje ele oferece frete grátis, que custa
**R$ 14,45** e derruba o resultado a −R$ 4,70. Passando para comprador-paga, o envio cai
para ~R$ 2.

### Kits de 40 — frete grátis obrigatório (acima de R$ 79)

| ID | Título novo | Chars | Preço | Resultado |
|---|---|---:|---|---|
| `2691993380` | `Kit 40 Cápsulas Café Especial Canastra Clássico Nespresso` | 57 | 40,00 → **139,90** | −30,40 → **+45,46** |
| `2691960931` | `Kit 40 Cápsulas Café Especial Canastra Suave Nespresso` | 54 | 83,10 → **139,90** | +2,11 → **+45,46** |
| `2691974195` | `Kit 40 Cápsulas Café Especial Canastra Canela Nespresso` | 55 | 40,00 → **139,90** | −30,40 → **+45,46** |
| `2691974682` | `Kit 40 Cápsulas Café Especial Canastra 3 Sabores Nespresso` | 58 | 83,10 → **139,90** | +2,11 → **+45,46** |

Margem: **32,5%**. Frete grátis **medido em R$ 14,45** no formulário (30/09), não os
R$ 20,00 que estavam estimados — e **não é obrigatório** acima de R$ 79: comprador-paga
custaria R$ 7,20. Ver [`09-remessa-e-estrategia-de-preco.md`](09-remessa-e-estrategia-de-preco.md). O `2691974682` (3 Sabores) é o que **recebe Ads**.

---

## Os títulos — o que entra e por quê

Todos ganham **"Café Especial"** e **"Canastra"**, que não estavam em **nenhum** dos 7.

| Termo | Por quê |
|---|---|
| **Café Especial** | Separa do patamar de massa (R$ 1,44–2,00/cáp) na busca qualificada |
| **Canastra** | Terceiros cobram R$ 3,99–4,56/cáp usando o topônimo, com **5 vendas**. Território livre |
| Cápsulas | Termo-raiz: `capsula de cafe` tem 8.402 resultados |
| Nespresso | Segunda busca mais comum é por compatibilidade |
| Kit 40 | Casa com o filtro *Formato de venda: Kit* e a faixa *18–49 unidades* |
| Sabor no título | "Cápsula de café com canela" é busca diferente de "cápsula de café especial" |

### O que saiu: "Compatível"
Não cabe junto com "Café Especial" no Clássico — daria 61 de 60. **Decisão do Rafael:
manter "Café Especial".**

⚠️ **Risco a avaliar:** os títulos atuais usam "Compatível Nespresso". Remover pode ter
implicação de política de marca. Não verificado.

⚠️ **O limite de 60 caracteres vem de blog** e não foi confirmado em nenhum vídeo nem no
formulário de cadastro.

### Regra de ouro
**Nunca editar título de anúncio rodando** — reseta o histórico de relevância. Estes
estão inativos, então é o momento certo.

Isso **não impede** criar um segundo anúncio para teste A/B de título, que é prática
recomendada. São coisas diferentes.

---

## Ficha técnica — é ela que alimenta a busca

> Só **título, ficha técnica e características** ativam o motor de busca do ML.
> **A descrição não indexa.**
> — diegorojasseller, 12/08/2026, `KPvPvwmTUC8`

| Campo | Caixa 10 | Kit 40 |
|---|---|---|
| Marca | Café Canastra | Café Canastra |
| Modelo / Linha | Clássico · Suave · Canela | Clássico · Suave · Canela |
| **Formato de venda** | Unidade | **Kit** |
| **Unidades por embalagem** | 10 | **40** |
| Compatibilidade | Nespresso | Nespresso |
| Tipo de infusão | Café | Café |
| Variedade | Espresso | Espresso |
| Peso por unidade | 5 g | 5 g |
| Peso líquido | 50 g | 200 g |
| **Intensidade (4–12)** | ⚠️ **a definir** | ⚠️ **a definir** |
| **É livre de glúten** | ⚠️ **a confirmar** | ⚠️ **a confirmar** |
| É descafeinado | Não | Não |
| É recarregável | Não | Não |
| Tipo de torra | Média (confirmar) | Média (confirmar) |
| Origem | Medeiros · Serra da Canastra · MG | idem |
| Condição | Novo | Novo |

### Os dois campos que não se chutam
**Intensidade** e **livre de glúten** são filtros nativos da categoria e **declarações de
produto**. Pedir à torrefação e ao controle de qualidade.

O `CLAUDE.md` do projeto já registra a lição (nº 18): quando a fonte não permite ler,
"copiar da foto" vira convite ao chute — e já saiu nota sensorial inventada.

O Coffee++ usa **"Sem Glúten" no título**, capturando um filtro que quase ninguém marca.

---

## Descrição — para o humano, não para a busca

Serve para **converter** e para **evitar devolução**. O bloco mais importante é a negativa
explícita:

> **"Compatível com máquinas do sistema Nespresso de uso doméstico. Não é compatível com
> Nespresso Vertuo nem com Dolce Gusto."**

Devolução derruba reputação, que é filtro binário de Buy Box.

Proibido na descrição: link, telefone, e-mail, WhatsApp. O ML remove o anúncio.

**As 7 descrições completas, prontas para colar, estão em
[`10-textos-prontos.md`](10-textos-prontos.md).** Antes existia só a do kit misto, e só
dentro de um artefato superado.

---

## Fotos — 10 slots

| Slot | Conteúdo |
|---:|---|
| 1 | Kit completo em **fundo branco puro** (exigência de catálogo) |
| 2 | **Escala** — cápsula na mão. Cápsula em tamanho real fica minúscula na grade |
| 3 | Compatibilidade — cápsula entrando na máquina |
| 4 | Composição do kit com rótulo legível |
| 5 | Espresso extraído na xícara, creme visível |
| 6 | Lavoura na Serra — usar foto real de `base-curada/01-real-verificada` |
| 7 | Torrefação própria |
| 8 | Tabela dos 3 blends — só com valores confirmados |
| 9 | Selo de origem e "desde 1985" |
| 10 | **Aviso de incompatibilidade** (não serve em Vertuo nem Dolce Gusto) |

Fotos de produto em `fotos produtos cru/Capsulas-*`. **Foto de produto é foto, não
render** — política do projeto, e o comprador de especial identifica imagem sintética.

---

## Vídeo — vantagem barata

O painel do ML promete **"em média 2,9 vezes mais visitas"**; a tela de recomendações diz
"vendem até 4 vezes mais". **Quase nenhum concorrente de cápsula usa.**

Especificação: 45–60 s · 16:9 · mínimo 1080p · legendado (a maioria assiste mudo) ·
YouTube **não listado** · **sem preço, sem link, sem contato**.

Roteiro em 7 planos em [`10-textos-prontos.md`](10-textos-prontos.md).

---

## Observação sobre redundância

O **`2691974682` (3 Sabores)** fica no mesmo preço dos três monossabores de 40 un,
disputando a mesma busca. Os quatro foram mantidos porque o Rafael pediu escopo fechado
nestes 7 — mas é o único ponto de redundância que sobra.

O critério correto não é "quantos anúncios", e sim **quantos disputam a mesma busca**.
Três sabores avulsos e três kits por sabor capturam termos distintos; três kits *mistos*
de 60 diferindo só na mistura interna, não.
