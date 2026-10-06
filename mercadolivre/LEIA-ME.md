# Mercado Livre — Café Canastra

> **Leia este arquivo antes de qualquer coisa nesta pasta.** Ele é o resumo de sessão:
> o que foi medido, o que foi decidido, o que eu errei e corrigi, e o que continua sem
> verificação. Sessões futuras não têm a memória desta.
>
> **Última atualização:** 05/10/2026
> **Objetivo do projeto:** cápsulas Nespresso-compatíveis são o produto escolhido para
> ser o primeiro a escalar em vendas no Mercado Livre.

---

## Regra que não se negocia

**Nada é alterado na conta do Mercado Livre sem autorização explícita do Rafael, campo
a campo.** Isso foi pedido diretamente e vale para toda sessão futura.

Nunca fazer, em hipótese alguma — são ações dele:

| Ação | Por quê |
|---|---|
| Depositar a garantia de R$ 75 | Movimentação financeira |
| Renovar certificado digital | Envolve certificadora e credencial |
| Enviar estoque ao Full | Ação física |
| Excluir anúncio | Irreversível; pode carregar avaliação |
| Ativar campanha de Ads | Compromete orçamento |
| Reativar anúncio | Coloca produto à venda |

Pode-se editar, **com autorização**: título, preço, tipo de anúncio, frete, ficha
técnica e descrição.

---

### Antes de mexer no ML pelo navegador, carregue a skill
**`canastra-mercadolivre`** tem a mecânica medida: a receita de edição que funciona,
o que falha em silêncio, os seletores e como conferir se gravou de verdade.

O resumo: **clique triplo, nunca `Ctrl+A`** · o acordeão demora até **19 s** e clicar de
novo **fecha** · confira na **lista de anúncios**, não na recarga · **aba nova a cada
3 ou 4 anúncios** · ler sempre funciona, escrever exige a receita.

## Estado da conta em 30/09/2026 — fatos medidos

| Fato | Valor | Origem |
|---|---|---|
| **Reputação** | **VERMELHA** | Central de Vendedores |
| Causa: envios incorretos | **37,68%** (26 de 69) — limite 13% | idem |
| Causa: canceladas por você | 2,73% (2 vendas) — limite 2,5% | idem |
| Reclamações | **0%** — dentro do limite | idem |
| Vendas em 365 dias | **73** (≈ 6,1/mês) | idem |
| Vendas últimos 7 dias | **R$ 0** | idem |
| Anúncios totais | 36 | idem |
| Anúncios de cápsula | **13, nenhum ativo** | idem |
| Sem estoque no Full | 13 anúncios | idem |
| Sem dados fiscais | 6 anúncios | idem |
| Certificado digital | **vencia 30/09/2026** | idem |
| Oferta do ML | **R$ 75 de garantia recupera o verde-claro** | idem |
| CPV informado | **R$ 15,10 por caixa de 10** (R$ 1,51/cápsula) | Rafael |
| Capacidade de estoque | **5 a 15 mil cápsulas**, reposição rápida | Rafael |

**A leitura que importa:** zero reclamação com 37,68% de envio incorreto significa que
o produto agrada e a **logística falha**. Não é problema de preço, anúncio ou Ads — e
por isso nenhum deles resolve. O Full conserta por construção: quem não despacha não
atrasa.

---

## Os 7 anúncios em escopo

Só estes. O Rafael pediu explicitamente para trabalhar **apenas** com eles.
IDs verificados no DOM da conta (os prints tinham dois dígitos trocados).

| ID | Produto | Preço hoje | Tipo hoje | Status |
|---|---|---:|---|---|
| `2692127545` | Cápsula Clássico 1cx 10un | 28,90 | Clássico | Inativo |
| `2692082114` | Cápsula Suave 1cx 10un | 18,70 | Premium | Inativo |
| `2692076338` | Cápsula Canela 1cx 10un | 18,70 | Premium | Inativo |
| `2691993380` | Kit Clássico 40un | 40,00 | Premium | Inativo |
| `2691974195` | Kit Canela 40un | 40,00 | Premium | Inativo |
| `2691960931` | Kit Suave 40un | 83,10 | Premium | Inativo |
| `2691974682` | Kit Clássico/Suave/Canela 40un | 83,10 | Premium | Inativo |

Todos em categoria **SUPERMERCADO**, sem estoque no Full e no depósito.
Detalhe completo em [`03-os-sete-anuncios.md`](03-os-sete-anuncios.md).

---

## Decisões já tomadas pelo Rafael

| Decisão | Escolha |
|---|---|
| Título: "Café Especial" ou "Compatível"? | **Café Especial** (não cabem os dois em 60 caracteres) |
| Preços | **R$ 34,90** (caixa) e **R$ 139,90** (kit) |
| Categoria | **Manter Supermercado** |
| Escopo da edição | **Tudo menos reativar** — anúncios ficam inativos até ordem dele |
| Promoção | Quer preço riscado; caixa a **R$ 28,90** para empatar com o Coffee++ |
| Plano de escala | **Fase 1 (descoberta) → Fase 2 (escala)** |

---

## O que eu errei e corrigi — leia antes de repetir

Esta seção existe porque cada item abaixo foi afirmado com confiança e depois derrubado
por dado. Uma sessão nova tende a repetir o mesmo erro.

### 1. Custo de envio vindo de blog, não da conta
Usei R$ 6,55 a 15,00 de blog. A conta mostra **R$ 14,45** de frete grátis na caixa de 10
e **R$ 29,90–34,30** no kit de 60 — mas só **R$ 1,40 a 4,80** quando o comprador paga.
**Efeito:** a caixa de 10 era o produto de *melhor* margem (35,5%), não a isca de 18,9%
que eu tinha calculado. Errei **13,9 pontos para baixo** nela e **9,4 para cima** no kit
de 60.
**Regra:** custo de envio sai da coluna "A pagar" da Central, nunca de blog.

### 2. "Consolidar 13 anúncios em 3" — argumento tecnicamente errado
Escrevi que 13 anúncios diluem a conversão. **Conversão é razão, não soma**: 13 anúncios
com 10 visitas e 1 venda têm os mesmos 10% de um com 130 visitas e 13 vendas. O que
dilui de verdade é **avaliação e selo de vendidos** — argumento mais fraco e mais lento.
E as fontes recentes recomendam o **oposto** (teste A/B de título criando mais anúncios).
**Regra:** o critério não é "quantos anúncios", é **quantos disputam a mesma busca**.

### 3. "Clássico em tudo" sem consultar as fontes
Derivei só da tarifa. As fontes dizem que **conta nova acelera melhor em Premium**, que
**acima de R$ 150 o comprador quer parcelar**, que **Premium tem acesso total às campanhas
da Central de Promoções** (que viram anúncio pago do ML no Instagram/TikTok) e que o
**cashback da campanha pode pagar exatamente a diferença de tarifa**.
**Regra:** abaixo de R$ 150 → Clássico. Acima → Premium. Catálogo → sempre Clássico.

### 4. ROAS objetivo: dei o teto como se fosse o alvo
Recomendei ROAS 7,3×, que é o **máximo tolerável** (ACOS = metade da margem). A prática
começa em **10–12×** e contas maduras rodam 15–26×.

### 5. Rampa de Ads até R$ 150/dia — não fecha com o nicho
Os portões da rampa abrem com ROAS ≥ 7, e ROAS 7 a R$ 40/dia exigiria R$ 8.400/mês de
receita — acima de todos os cenários realistas. **R$ 20/dia só se sustenta a partir de
~60 vendas/mês.** A 35 vendas/mês o teto é **R$ 11,63/dia**.
**Regra:** orçamento de Ads é **derivado do volume** (50% do lucro bruto), nunca fixo.

### 6. "A descrição é indexada" — falso
Só **título, ficha técnica e características** alimentam o motor de busca do ML.
Os blends vão para a ficha, não para a descrição.

### 7. Brand Ads no plano
Foi **extinto**, ao menos temporariamente. Saiu.

### 8. Título de 81 caracteres
O limite é **60**. (Ainda assim: o número 60 vem de blog e **não foi confirmado** em
nenhum vídeo nem no formulário.)

### 9. Li "+10 mil vendidos" de um carrossel
Numa página de produto do ML, os blocos `poly-card` são **carrossel de recomendação**,
não o produto aberto. O dado real estava em `[class*="ui-pdp-seller"]` e dizia
**+5 vendas**.
**Regra:** rastreie o nó pai antes de usar número raspado.

### 10. A premissa "temos muito estoque" estava invertida
10.000 cápsulas comportam **426 vendas** = um ano de estoque no ritmo projetado.
**Não é muito estoque para pouca demanda — é estoque demais para a demanda que existe.**
O gargalo nunca foi produção.

### 11. Tratei "teto de Ads" como um número só
Quando o Rafael perguntou se dava para **passar do teto**, a pergunta não tinha
resposta única: existem **dois tetos de naturezas opostas**. O de **estoque**
(R$ 33/dia com 5 de cada) é o lucro máximo que o lote comporta — **não se fura, se
levanta** enviando mais. O de **rentabilidade** (ROAS 3,28×) é onde o Ads come o
lucro da venda — **esse se fura, e às vezes deve**, quando o que se compra é um
ativo (Estrela, avaliação, histórico) e não uma venda.

**Regra:** antes de responder "dá para aumentar a verba?", identifique **qual** teto
está sendo tocado. Furar o de estoque é comprar tráfego para prateleira vazia e
**destrói justamente o ativo** que a verba estava comprando. Detalhe em
[`05-ads.md`](05-ads.md) § Furar o teto.

### 12. Ia projetar três estratégias de preço como se fossem três escolhas
O Rafael pediu um seletor entre preço cheio, verdinho e misto. Antes de calcular eu abri
a **Central de promoções** da conta: *"No momento, não é possível oferecer promoções.
Recupere sua reputação verde ou amarela"*, com **0 anúncios** elegíveis. Duas das três
estratégias **não existem hoje** — e a melhor das três é uma delas.

**Regra:** antes de modelar uma escolha, **confira na conta se a opção está disponível.**
Uma planilha de três cenários em que dois estão trancados não é análise, é ficção. E a
distinção que quase passou: **baixar o preço ≠ verdinho** — preço é campo do anúncio e
está liberado; o riscado, as campanhas do ML e o cashback é que dependem da cor.
Ver [`09-remessa-e-estrategia-de-preco.md`](09-remessa-e-estrategia-de-preco.md).

### 13. O único número "mole" estava no formulário o tempo todo
O frete grátis do kit vinha marcado como **interpolado em R$ 20,00** desde o início, e eu
nunca fui olhar — porque achei que precisaria do simulador do ML. **O formulário de
edição mostra o custo exato**, ao lado de cada opção de frete, assim que se troca o preço:
**R$ 14,45**, igual na caixa e no kit. Junto veio que a categoria é **Alimentos e
Bebidas**, não Supermercado, e que **frete grátis não é obrigatório acima de R$ 79**.

O erro de R$ 5,55 por kit inverteu uma recomendação: a postura agressiva saiu de
**−R$ 29** para **+R$ 753** em 3 meses e passou a dominar a ideal.

**Regra:** o formulário de edição é uma **fonte de medição**, não só um lugar de escrever.
Antes de interpolar ou estimar qualquer tarifa, abra o anúncio e leia o número. E quando
um valor estiver etiquetado como estimado, ele é **dívida técnica** — vá medir antes de
construir recomendação em cima dele.

### 14. Li o mesmo contador duas vezes e deu 14 e depois 1
"Anúncios inativos por descumprir políticas": capturei **14** numa passagem e **1** em
outra. Os cards de status ficam num **carrossel**, e o meu recorte de texto pega o número
do card vizinho conforme a posição de rolagem. Cheguei a registrar o 14 em três arquivos
como se fosse fato.

**Regra:** contador de card em carrossel não é medição. Para contar anúncios por status,
**filtre a lista e conte as linhas** — que é o que fiz com os 7 em escopo, um a um, e
esse número vale. É a lição 10 de novo: não transforme em garantia escrita o que você
não mediu no lugar certo.

### 15. O kit de 40 não tem desconto por volume nenhum
Caixa de 10 a R$ 34,90 = **R$ 3,49/cápsula**. Kit de 40 a R$ 139,90 = **R$ 3,50/cápsula**.
O kit está um centavo **mais caro** por cápsula que a caixa avulsa — ou seja, **não existe
motivo para o comprador subir de ticket**. Passei a sessão inteira tratando o kit como o
produto que "resolve a margem" sem notar que a escada de preço está plana.

**Regra:** num portfólio de formatos do mesmo produto, **calcule sempre o preço por unidade
base** (aqui, por cápsula) e confira se a escada desce. Preço absoluto maior não é escada.
Decisão em aberto, fora do escopo aprovado — ver
[`12-precos-de-atacado.md`](12-precos-de-atacado.md).

### 16. Tratei como "escolha" o que o ML impõe
Documentei que "Compatível" saiu do título porque **não cabia** junto com "Café Especial",
e registrei como **decisão do Rafael**. Ao tentar gravar, o ML recusou o título sem
"Compatível" — *"omite que as cápsulas são compatíveis com Nespresso"* — e desabilitou o
Confirmar. **Nunca foi uma escolha.** Levei ao cliente um trade-off que não existia.

**Regra:** antes de pedir ao cliente para escolher, **confira se as duas opções existem**.
Restrição de plataforma se descobre submetendo, não deduzindo — e o formulário recusa de
graça. É a "evidência barata" do próprio método deste projeto, aplicada fora da API.

### 17. O `Ctrl+A` era a causa dos "Confirmar" que não gravavam
Passei várias rodadas concluindo que o formulário do ML "não grava pela automação".
Gravava — só que eu limpava os campos com `Ctrl+A` e o `Ctrl` não registrava, deixando
uma letra **`a`** no início do valor. Vi `aClássico, Suave e Canela` num screenshot e a
ficha caiu. O campo ficava inválido, o Confirmar não submetia, **e nenhum erro aparecia**.
Trocando por **clique triplo**, gravou de primeira.

**Regra:** para limpar campo de texto no navegador, **clique triplo**, não `Ctrl+A`.
E quando algo "não grava sem dar erro", **olhe o conteúdo do campo num screenshot** antes
de culpar a plataforma — eu cheguei a escrever no repositório que era limitação do site.

---

## Verificado × não verificado

### Medido, pode usar
- Situação, preço, tipo, frete e estoque dos 36 anúncios — Central, 29–30/09
- Reputação e as três métricas que a compõem — Central
- Custo de envio real por faixa — coluna "A pagar" da conta
- Preços de concorrentes no ML — busca logada, 25/09
- Comissão 14% Clássico / 19% Premium, igual em Supermercado e Alimentos e Bebidas
- Armazenagem Full: Supermercado pequeno R$ 0,000/dia; Alimentos e Bebidas R$ 0,007/dia
- Estoque antigo: cobra a partir de **2 meses** em Supermercado, 4 nos demais

### Não verificado — não afirmar como fato
| Item | Situação |
|---|---|
| ~~Limite de 60 caracteres no título~~ | **Resolvido: é real.** O formulário mostra `60 / 60` |
| **Ciclo de 28 dias de aprendizado de campanha** | Vem de blog |
| ~~Frete grátis do kit~~ | **Resolvido: R$ 14,45, medido no formulário em 30/09** |
| **Tarifa pós-24/08/2026** | Houve nova revisão depois da de março. Valores novos não encontrados |
| **Variação por sabor em Cápsulas** | Nenhuma fonte tratou de variação em alimento |
| **Clássico + Premium no mesmo anúncio** | Citado como disponível; não verificado nesta conta |
| **ROAS dinâmico** | Função de 25/09; pode não estar liberada |
| **CPC e conversão da categoria** | Nunca medidos. É o que a Fase 1 existe para resolver |
| **DIFAL no Full** | Estoque em CD de outro estado pode gerar; falar com contador |

---

## Arquivos desta pasta

| Arquivo | Conteúdo |
|---|---|
| [`01-situacao-da-conta.md`](01-situacao-da-conta.md) | Diagnóstico completo da conta e dos 36 anúncios |
| [`02-economia-e-precos.md`](02-economia-e-precos.md) | CPV, tarifas, margens, escada de promoção, categoria |
| [`03-os-sete-anuncios.md`](03-os-sete-anuncios.md) | Os 7 IDs, títulos novos, o que muda campo a campo |
| [`04-concorrencia.md`](04-concorrencia.md) | Preços e volumes medidos dos concorrentes |
| [`05-ads.md`](05-ads.md) | Estratégia de Ads, orçamento derivado, configuração |
| [`06-plano-de-escala.md`](06-plano-de-escala.md) | As duas fases, portão de decisão, Produto Estrela |
| [`07-artefatos.md`](07-artefatos.md) | Os artefatos publicados e quais ainda valem |
| [`09-remessa-e-estrategia-de-preco.md`](09-remessa-e-estrategia-de-preco.md) | Remessa ao Full em 1/2/3 meses, as 3 estratégias de preço e o limiar de 131 vendas |
| [`10-textos-prontos.md`](10-textos-prontos.md) | **Título, descrição e vídeo dos 7, prontos para colar** |
| [`11-folha-de-aplicacao.md`](11-folha-de-aplicacao.md) | Campo a campo dos 7 e a mecânica de edição |
| [`12-precos-de-atacado.md`](12-precos-de-atacado.md) | Atacado (ML Negócios): sim nos kits, não nas caixas, e só depois do verde |
| [`13-o-que-falta.md`](13-o-que-falta.md) | **COMECE AQUI para executar.** O que falta em cada anúncio, em sequência, com o estado lido do formulário |
| [`99-historico-estrategia-v1.md`](99-historico-estrategia-v1.md) | Primeira versão. **Contém números superados** |
| `pesquisa/` | 16 transcrições, scripts de busca e `ACHADOS.md` |
| `scripts/` | Cálculos em Python que geraram cada número. `matriz.py` = teto de estoque; `teto.py` = teto de rentabilidade |

---

## Como reproduzir a pesquisa

```bash
cd mercadolivre/pesquisa
python pesquisar.py 60     # busca vídeos recentes -> videos.tsv
python baixar.py           # baixa legendas -> transcricoes/ (pula o que já existe)
python varrer.py           # lista os temas disponíveis
python varrer.py premium   # trechos sobre clássico vs premium
```

Armadilhas já resolvidas, registradas em `pesquisa/pesquisar.py`:
- `ytsearchdate:` não funciona com extração rasa — use a URL de busca com `sp=CAISBAgFEAE`
- `--print` do yt-dlp no console do Windows grava barra-invertida-t literal em cp1252;
  por isso o script importa `yt_dlp` como **módulo**, não por subprocesso

### Acesso ao Mercado Livre
- `WebFetch` devolve **403** em todo o ML
- `curl` com UA de Chrome passa na home e nas páginas de vendedor, mas a **busca**
  devolve `suspicious-traffic-frontend` com status 200
- A extensão **Claude in Chrome** funciona, mas o ML **trava a busca após a primeira
  consulta programática**. Rota que funciona: **o humano navega, a IA lê** a página já
  carregada com `javascript_tool`
- Páginas de produto (`/p/` e `/up/`) **não** têm esse limite

---

### 18. Ninguém tinha olhado as fotos dos anúncios
A conta vinha sendo auditada por preço, título, frete e ficha técnica. Em 04/10/2026 abri as
fotos pela primeira vez: nos **três anúncios de 10 un**, duas das três mostravam a **caixa
dispenser de atacado** — caixa grande com dezenas de cápsulas a granel — num anúncio que
vende *1 caixa de 10 un a R$ 34,90*. A terceira era mock-up 2D chapado. Todas entre
**375 e 500 px**, abaixo dos 1200 que o ML exige para habilitar zoom.

**Regra:** numa auditoria de anúncio, **a foto é campo como qualquer outro**. Com 37,68% de
envio incorreto nesta conta, expectativa visual errada é combustível de devolução, não
detalhe estético.

---

## Alterações aplicadas

| Data | Anúncios | O que mudou | Autorização |
|---|---|---|---|
| 04/10/2026 | `2692127545` · `2692076338` · `2692082114` (os 3 de 10 un) | **Fotos**: as 3 antigas substituídas por 3 de catálogo — embalagem + cápsula (capa), três cápsulas, cápsula isolada | Rafael, na conversa |
| 05/10/2026 | os mesmos 3 | **Fotos**: inseridas a frente e a(s) lateral(is) entre a capa e as cápsulas. Clássico e Canela ficaram com **5**, Suave com **6** | Rafael, na conversa |

Ordem final, por anúncio: **capa** (embalagem + cápsula) → **frente** → **lateral(is)** →
**três cápsulas** → **cápsula isolada**.

**Duas laterais ficaram de fora, e o motivo importa.** O carimbo de lote/fabricação/validade
é impresso fora da arte e a geração o **redesenha** (lição 22 do `CLAUDE.md`):

| Arquivo | Por que não subiu |
|---|---|
| `16.4` | `F: 23.2025` — **mês 23 não existe** |
| `17.3` | `L:114 F:12.2025 V:12.2026` — plausível, e por isso pior: ninguém vê |

`21.4` subiu porque saiu **sem carimbo nenhum**. Para completar a lateral que falta no
Clássico e no Canela, a rota é compor o carimbo da foto real ou tirá-lo do enquadramento.

**Ressalva escrita, não reprova:** `16.3` e `21.3` trazem `ARABICA` **sem acento** (o certo
é `ARÁBICA`) e os QR de rastreabilidade de todas as laterais são **regenerados, não
escaneáveis**. Subiram com o Rafael avisado.

Origem: `saida-teste/catalogo-estudio/{16,17,21}-capsulas-*/`. Conferido na **lista de
anúncios** e relendo os 3 formulários do zero: as fotos antigas sumiram e a ordem no
servidor bate com a pedida — 5 · 5 · 6.

**Os 4 kits de 40 un continuam com as fotos antigas** — fora do escopo autorizado.

---

## Estado atual e próximo passo

Nada mais foi alterado na conta. O que está pendente, em ordem:

1. **Certificado digital** — vencia 30/09. Sem ele não sai NF-e e o Full pode pausar
2. **R$ 75 de garantia** — recupera o verde-claro. Maior retorno por real do projeto
3. **Estoque ao Full** — elimina a causa dos 37,68%
4. **Intensidade (escala 4–12) e status de glúten** — filtros nativos; pedir à
   torrefação e ao controle de qualidade. **Não chutar**
5. **Simulador de custos da Central** — confirmar o frete do kit de 40
6. Aplicar as edições nos 7 anúncios (autorizado: tudo menos reativar)
