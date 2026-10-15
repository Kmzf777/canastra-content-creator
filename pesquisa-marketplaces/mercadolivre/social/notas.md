# Mercado Livre: o que ensinam os criadores de Instagram e TikTok, e o que fazem os líderes

Data da análise: 2026-10-14. Analista social, com pesquisa neutra sobre como operam os melhores vendedores da plataforma.

## Base e método

- **Transcrições (23 arquivos):**
  - 15 Reels do Instagram. Um deles, `DXhRiCCERsG`, não tem fala, e foi usada só a legenda.
  - 8 vídeos do TikTok. Um deles repete outro: `7680324894680304917` e o Reel `DcuJYVVBOMx` são o mesmo vídeo de Rafael Sasso, contado uma só vez.
  - As transcrições foram feitas por Whisper automático, então há erros de reconhecimento ("ful" = FULL, "acus" = ACOS, "eds" = Ads). Os números falados foram conferidos no contexto.
- **Legendas (`posts.tsv`, 40 Reels):** onde não há transcrição, só a legenda foi usada como fonte. Isso vem marcado como "(legenda)". Um post deu erro (`DcPUHO-B6T1`). Vários outros só têm título genérico sem conteúdo, como "Como vender no Mercado Livre" (`DdnjPIzsST3`, `DYKEkTFh5HP`, `Dd9VFdEJnaZ`, `DcUHUKoBLoF`, `DdSDQkVT__E`, `DePGS1yvHfc`, `DcmCNcNP8co`, `DcQ7vtBKSFR`). Esses foram descartados como fonte de afirmação.
- **TikTok sem transcrição (`tiktok.txt`):** 12 vídeos têm só o título (por exemplo `7472469492900154630`, `7505405157845306629`, `7486647023416970551`, `7618650153083325703`). Os títulos foram usados apenas como indício de tema e não entram como afirmação.
- **Datas:**
  - Reels: a data vem do `posts.tsv`.
  - TikTok: a data foi decodificada do próprio id do vídeo. Resultado: 7517… = 2025-06-18; 7597… = 2026-01-19; 7599… = 2026-01-24; 7636… = 2026-05-04; 7641… = 2026-05-18; 7657… = 2026-07-01; 7680… = 2026-08-31; 7685… = 2026-09-15.
  - **Corte de 6 meses para regra de plataforma: antes de 2026-04-14 = "pode estar superada".**
- **Tipos:** [OFICIAL] regra dita pela plataforma · [PRÁTICA] tática de praticante · [CASE] números de uma operação · [DADO] estudo ou ferramenta · [OBS] observação direta.
- **Atenção:** quase nenhuma regra de plataforma desta base vem da própria plataforma. Tarifas e mecânicas citadas por criadores são [PRÁTICA] ("o criador diz que a regra é X"), salvo indicação contrária. Elas precisam ser confirmadas na fonte oficial pela frente de pesquisa oficial.

---

## 1. Ads (Product Ads / Mercado Ads)

### O que ensinam

- **Mudança de métrica (de ACOS para ROAS):** em julho de 2026, Fabio Ludke diz que a campanha agora se configura por **ROAS objetivo**, e não mais por ACOS objetivo. Segundo ele, um é o inverso do outro (ACOS = 1/ROAS) e na prática nada muda. [PRÁTICA, `7657666675122130192`, 2026-07-01]
  - Consequência: o tutorial de 2025 de Natan Aquino (ACOS objetivo de 5%, orçamento de R$10/dia, uma campanha por produto) usa a tela antiga. [PRÁTICA, `7517394661351148805`, 2025-06-18 — **pode estar superada**]
- **Receitas de configuração para começar** (são números de praticante, sem base publicada; os três divergem entre si):
  - **Natan Aquino:** ACOS de 5%, R$10/dia, uma campanha por produto. Deixar rodar de 5 a 7 dias e subir o orçamento quando o painel sugerir. [PRÁTICA, `7517394661351148805`, 2025-06-18, pode estar superada]
  - **Fabio Ludke:** uma campanha "teste todos" com todos os produtos, nome com a data e ROAS objetivo de 15, ou seja, começar com ROAS alto para entender o nicho. Ele diz que o orçamento mínimo pedido era de R$50/dia. [PRÁTICA, `7657666675122130192`, 2026-07-01]
  - **Rafael Sasso, a "campanha inteligente":**
    - Criar uma campanha manual com o filtro "mais vendidos", ROAS de 25 e orçamento de R$33, e não mexer por 3 dias.
    - Depois de 5 vendas, baixar o ROAS para 15 e subir o orçamento para R$51.
    - A lógica dele: com ROAS alto a plataforma entrega menos e procura o público; depois de vendas, ROAS menor amplia a entrega para pessoas parecidas com quem comprou.
    - Os valores exatos (33 e 51) não têm justificativa. [PRÁTICA, `DcuJYVVBOMx` / `7680324894680304917`, 2026-08-31]
  - **Princípio comum às três (vale como método):** começar contido, medir alguns dias e escalar o orçamento só no que vendeu.
- **ROAS mais alto = menos entrega.** Quanto maior o ROAS objetivo, menos a plataforma mostra o produto, então é preciso um meio-termo. [PRÁTICA, `DcuJYVVBOMx`, 2026-08-31]
- **TACOS acima de ACOS:**
  - Alex Moro ensina a controlar o TACOS (gasto em Ads ÷ faturamento total no mesmo período). O ACOS sozinho "pode ser enganoso".
  - No caso dele: R$14 mil de Ads contra cerca de R$299 mil de faturamento em 30 dias, o que dá TACOS de 4,6%, com teto próprio de 6%. [CASE, `DZXgH6-u-Ri`, 2026-06-09]
- **Ads como custo dentro do preço:** Gabriel Paiva reserva 5% do preço para Ads na conta de margem. [PRÁTICA, `DdmFpTdpl3q`, 2026-09-22]
- **Contraponto, "Ads não é obrigatório":**
  - Raphael (VoceVendeu!) diz faturar quase R$1,5 milhão em 30 dias sem gastar com Ads. Segundo ele, título, foto, reputação, logística, conversão e oferta pesam mais que o orçamento.
  - Ele critica mentorias e agências que lucram quando o vendedor investe mais. [CASE, `DZYP9wNveF2`, 2026-06-09]
  - O número não é verificável a partir do vídeo.
- **"Ads não salva anúncio ruim":** quem diz isso é o próprio Sasso. [PRÁTICA, `DcuJYVVBOMx`, 2026-08-31]
- **Novos formatos (legenda):**
  - A ferramenta "Aumentar Seguidores" do Mercado Ads usaria IA para gerar vídeos com as imagens do produto e entregá-los a quem tende a seguir a loja.
  - A legenda cita que quem segue a loja compra até 60% mais e recompra até 50% mais vezes.
  - Parece repetir material de divulgação da plataforma, mas sem link. [DADO de origem não confirmada, `DZsM3V9t498` (legenda), 2026-06-17]
- **Checklist de Hugo Vasconcelos:** Product Ads "com estratégia", afiliados ativados e cupom de primeira compra na Minha Página. [PRÁTICA, `DefTt6LEhSG`, 2026-10-14]

### Divergências

- Os ROAS iniciais recomendados vão de 15 a 25 e os orçamentos de R$10 a R$50/dia. Não há consenso, e cada número depende de margem e categoria.
- Raphael (sem Ads) contra todos os demais (Ads como alavanca). O ponto comum é que Ads só amplifica um anúncio que já converte.

---

## 2. Preço e promoção

### O que ensinam

- **"Faturamento não é lucro" (o tema mais repetido da base).** Todos montam a mesma conta: preço − comissão − tarifa fixa ou frete − imposto − custo do produto − embalagem/devolução − Ads = margem de contribuição.
  - Exemplo de Gabriel Paiva: compra a R$22 e vende a R$55,90.
    - Desconto da comissão de 14% (clássico, naquela categoria), de 8% de imposto e de 5% de Ads.
    - Desconto do frete de R$8,75 (2 kg) e de 2% de outros custos.
    - Sobram R$8,94, cerca de 16% de margem. [PRÁTICA, `DdmFpTdpl3q`, 2026-09-22]
  - Felipe Lima recomenda margem mínima de 20%; 12% "não vale a pena", a não ser com volume muito alto. [PRÁTICA, `DYSu4iqBx4I`, 2026-05-13]
  - Roberto Carlos Jr (legenda): custo + frete + comissão + imposto + margem antes de pôr preço. [PRÁTICA, `DXhRiCCERsG` (legenda), 2026-04-24]
  - Leonardo Tonchak: a calculadora oficial da plataforma não inclui imposto nem embalagem, por isso ele usa planilha própria. [PRÁTICA, `7636173974195440903`, 2026-05-04]
  - Leo Mantovan: preço calculado de trás para frente a partir da margem desejada (30%). [PRÁTICA, `DcW9TahOHTw`, 2026-08-22]
- **Comissões citadas por criadores** (é preciso confirmar na fonte oficial):
  - Felipe Lima, "se não me engano": clássico de 11% a 14% e premium de 15% a 19%. [PRÁTICA, `DYSu4iqBx4I`, 2026-05-13]
  - Tonchak usa premium de 18% no exemplo. [PRÁTICA, `7636173974195440903`, 2026-05-04]
  - Paiva usa clássico de 14%. [PRÁTICA, `DdmFpTdpl3q`, 2026-09-22]
- **Tática das faixas de tarifa fixa (Bruno Gontijo):**
  - Segundo ele, abaixo de R$79 o vendedor paga uma tarifa fixa que muda por faixa de preço (R$19–48,99 e R$49–78,99). A partir de R$79 entra o custo de frete, que é maior.
  - Por isso, baixar o preço de R$50,49 para R$48,99 muda a faixa e **aumenta** a margem em reais e em porcentagem, mesmo vendendo mais barato.
  - No exemplo, a promoção exigia 15% de desconto mínimo, e a margem foi de 16% para mais.
  - Ele usa uma ferramenta externa de gestão de promoções. [PRÁTICA, `DeSaMOnJ820`, 2026-10-09]
  - Princípio válido sem corte: **precificar olhando os degraus de tarifa, e não só o percentual.** As faixas em si são regra de plataforma, a confirmar.
- **Central de promoções desde o primeiro dia do anúncio** (checklist). [PRÁTICA, `DefTt6LEhSG`, 2026-10-14]
- **Ferramentas pagas de cálculo de margem aparecem como isca de venda** (Hunter, CMA, Joom Pulse, planilhas). O conteúdo útil é sempre a mesma fórmula acima.

---

## 3. Logística e estoque (FULL, Flex, capacidade)

### O que ensinam

- **FULL converte, mas tem custos que precisam entrar na conta (Hunter HUB):**
  - Os custos são quatro: armazenagem (mais cara depois de 6 meses parado), envio ao centro de distribuição, comissão e capital preso no estoque.
  - A regra do criador: abaixo de cerca de **3 unidades/dia**, ou sem um ticket bom, pensar duas vezes antes de mandar para o FULL.
  - O vídeo é a isca de uma ferramenta com teste grátis. [PRÁTICA, `Db9NvEIDHC9`, 2026-08-12]
- **Custos reais relatados:**
  - Biel Seller: coleta de cerca de R$0,80 por produto e armazenagem de R$0,21/mês para item pequeno, sobre R$120 mil de faturamento. [CASE, `7597198803380292885`, 2026-01-19 — **valores de tarifa podem estar superados**]
  - Bropinheiro:
    - Custo de armazenagem FULL de R$1.973 em um mês, que caiu para R$1.431 no mês seguinte ao concentrar envio em "produtos estrela".
    - Ele afirma que o produto estrela fica isento se mantiver ao menos 1.000 unidades. Essa regra não foi confirmada e precisa de checagem oficial.
    - O vendedor manda uma embalagem simples com etiqueta, e o ML reembala e distribui para vários centros. [CASE/PRÁTICA, `7641347634120150280`, 2026-05-18]
- **"Ative FULL, Flex e Places"** (checklist). [PRÁTICA, `DefTt6LEhSG`, 2026-10-14]
- **Capacidade de envio:**
  - Léo dos Santos manda subir a "Capacidade de envios" (Configurações → Preferências de venda → Tempo de preparação e capacidade) de 100–200 para cerca de 1.500.
  - A tese dele é que isso sinaliza ao algoritmo que a operação aguenta mais demanda. A própria legenda admite que isso não garante vendas.
  - Não há evidência apresentada. [PRÁTICA, `DcW7lXEyO1T`, 2026-08-22]
- **Logística como causa de não fechar venda:** se a intenção de compra não vira venda, preço ou logística não estão adequados. [PRÁTICA, `DcecUj8x6Sb`, 2026-08-25]
- **Infraestrutura (legendas, notícia):**
  - Previsão de 42 centros de distribuição FULL no Brasil até o fim de 2026, com centenas de robôs em Cajamar (SP). [DADO, `DeZWuzjxmYi` (legenda), 2026-10-12]
  - Novo centro em Gravataí (RS), de 38,7 mil m², com 720 colaboradores, em operação desde 12/09. [DADO, `DefJhl-PjRG` (legenda), 2026-10-14]
  - Esses dois posts repassam notícias e não trazem a fonte original.

---

## 4. Ranqueamento e anúncio (título, ficha, fotos, conversão)

### O que ensinam

- **O que alimenta a busca:**
  - Segundo Diego Rojas, a busca lê o título, a ficha técnica ("só os primeiros 30 caracteres") e as variações (cor, voltagem, tamanho). Para ele, **a descrição não ativa a busca**.
  - As palavras-chave devem vir de "Tendências" do próprio ML, por nicho e subnicho, e não de IA genérica. [PRÁTICA, `DYzLkXQhDR1`, 2026-05-26]
- **Contraponto:**
  - Marina Wolff (Pandora360) manda colar no fim da descrição palavras-chave geradas por IA, "básicas e com SEO".
  - Isso contradiz Rojas e não traz evidência. O vídeo termina com venda de mentoria e manual. [PRÁTICA, `7685861706622389511`, 2026-09-15]
  - **Divergência aberta: a descrição indexa ou não? É preciso confirmar na fonte oficial.**
- **Título escrito para a busca:** pesquisar o que o comprador digita, e não o nome técnico. [PRÁTICA, `DXhRiCCERsG` (legenda), 2026-04-24]
  - A observação direta confirma o padrão no líder de café (ver Observação dos líderes, item 8).
- **Diagnóstico pelo funil de métricas (Julio Aramaqui).** Caminho na plataforma: Métricas → Negócio → Anúncios → Detalhe. O funil tem três etapas: visitas únicas → intenção de compra (comprar agora ou carrinho) → vendas brutas.
  - **Poucas visitas:** o problema está no título/palavra-chave e na foto de capa.
  - **Intenção abaixo de 10% das visitas:** o problema está nas fotos secundárias e na descrição, que não quebram objeções.
  - **Vendas abaixo de 25% da intenção:** o problema é preço fora do mercado ou logística.
  - Os limites de 10% e 25% são do criador. [PRÁTICA, `DcecUj8x6Sb`, 2026-08-25]
- **Checklist de Hugo Vasconcelos:** 10 fotos e 3 clipes por anúncio; título e ficha com "campo semântico" (palavras complementares). [PRÁTICA, `DefTt6LEhSG`, 2026-10-14]
- **Ferramentas nativas:**
  - Bruno Maciel diz que, quando um anúncio perde visitas sem motivo, passar a foto de capa pelo **editor de IA do próprio ML** "reseta" a exposição.
  - Ele admite que "ninguém sabe" por quê. A teoria dele é que a plataforma favorece quem usa as próprias ferramentas.
  - É uma hipótese anedótica. [PRÁTICA, `Dd9wMyhvUrW`, 2026-10-01]
- **Conferir o anúncio no celular:** na loja dele, 81% das vendas vêm do celular, e a descrição ou a imagem podem aparecer cortadas no app. [CASE, `DbodEv8vHdl`, 2026-08-04]
- **Anúncio com IA (legenda, publicidade de ferramenta):** gerar título, descrição e imagens com IA (AvantPost). É propaganda e não ensina método. [`DY5SzLDy6jh` (legenda), 2026-05-28]

---

## 5. Produto e mix

### O que ensinam

- **Escolha de produto por dados:** analisar demanda, categoria, concorrência e margem antes de comprar. São posts patrocinados por ferramenta (Joom Pulse). [PRÁTICA, `DeeZ64fjtBN` (legenda), 2026-10-14]
- **Margem mínima por produto (20%)** como filtro de mix. [PRÁTICA, `DYSu4iqBx4I`, 2026-05-13]
- **Concentrar estoque nos campeões:**
  - FULL só para quem gira (cerca de 3/dia). [PRÁTICA, `Db9NvEIDHC9`, 2026-08-12]
  - Mandar o máximo de "produtos estrela" para o FULL. [PRÁTICA, `7641347634120150280`, 2026-05-18]
- **Vários anúncios iguais com preços diferentes:** o tema aparece só no título de um TikTok de Hugo Vasconcelos, sem transcrição. Não foi analisado. [`7505405157845306629`, 2025-05-17]
- **A base social fala pouco de mix (linhas, formatos, tamanhos).** Esse padrão aparece com força na observação direta (ver Observação dos líderes, itens 3 e 5), e não nos criadores.

---

## 6. Reputação e atendimento

### O que ensinam

- **A reputação verde como "maior ativo" da conta** (legenda de "4 erros comuns"). [PRÁTICA, `DXhRiCCERsG` (legenda), 2026-04-24]
- **FULL melhora a reputação.** É afirmação de praticante. [PRÁTICA, `Db9NvEIDHC9`, 2026-08-12]
- **Minha Página e seguidores (Bruno Maciel):**
  - Custo por seguidor de R$1,75.
  - 712 vendas atribuídas à Minha Página e ao canal de transmissão.
  - Uso dos dados de audiência para ajustar palavra-chave, banner e linguagem: 84% de público masculino e poder de compra alto em 51%.
  - Ticket médio de R$970 e R$1,2 milhão em 7 dias.
  - O caso é de uma loja de alto ticket. [CASE, `DbodEv8vHdl`, 2026-08-04]
- **Seguidores compram e recompram mais** (ver Ads, `DZsM3V9t498`, legenda). [DADO não confirmado, 2026-06-17]
- **Cupom de primeira compra na Minha Página** (checklist). [PRÁTICA, `DefTt6LEhSG`, 2026-10-14]
- **Atendimento:** quase não aparece nos vídeos. Um perfil (`DXXLGLkiWd6`, legenda) faz "denúncia de vendedores de má fé", sem conteúdo transcrito.

---

## 7. Alimentos e marca própria

### O que ensinam

- **Revenda de café no FULL (`7599012656275541266`, 2026-01-24):** o vídeo é de um fornecedor/atacadista vendendo lote para revendedores, e não conteúdo neutro.
  - **Promessa:** o café custa R$19, é vendido a R$29,90–33 no FULL e daria "40% de lucro". Descontando nota fiscal (cerca de 7%), sobrariam de 20% a 32%, conforme a "notoriedade" do vendedor.
  - **Condições:** pedido mínimo de 100 unidades e limite de 50 vendedores. Só atende quem é CNPJ com FULL em SP, com envio de Bauru, e a previsão é zerar o estoque em 21 a 33 dias.
  - **O que se tira como dado:**
    - Café é usado por revendedores como produto de giro para "crescer conta".
    - O preço baixo de lançamento de uma marca nova é a tática de entrada.
    - O vídeo cita que a tarifa fixa cai "para cerca de 1 real" no FULL (afirmação a confirmar).
    - Tudo é [PRÁTICA], **específico de revenda**, com **promessa comercial não verificável**; tarifas **podem estar superadas**.
  - Há um segundo vídeo do mesmo perfil (`7618650153083325703`, "café em grão com lucro 30%"), só com título e sem transcrição.
- **Marca própria e loja oficial:**
  - Na base social só aparece um título de TikTok sem transcrição: "virar Loja Oficial: primeiro passo é ter marca" (`7486647023416970551`, 2025).
  - O tema é coberto pela observação direta (itens 2, 3 e 7 abaixo).
- **Sem estoque / dropshipping:** "R$20 mil por semana sem estoque" aparece só como legenda (`DaERLkSPjg4`, 2026-06-26). É modelo **específico de revenda/dropshipping** e não se aplica a indústria.
- **Importação:** o perfil de Rafael Sasso se apresenta como "Importação com Margem" (`DcuJYVVBOMx`). A receita de Ads dele vem desse contexto.

---

## 8. Cases grandes

| Operação | Número relatado | Fonte | Tipo | Observação |
|---|---|---|---|---|
| Raphael (VoceVendeu!) | cerca de R$1,5 milhão em 30 dias **sem Ads** | `DZYP9wNveF2`, 2026-06-09 | [CASE] | Mostrado na tela, não verificável; serve de argumento contra mentorias |
| Loja gerida por Bruno Maciel | R$1,2 milhão em 7 dias; 712 vendas via Minha Página; ticket de R$970; 81% mobile | `DbodEv8vHdl`, 2026-08-04 | [CASE] | Alto ticket, público 84% masculino |
| Alex Moro | R$14 mil de Ads, cerca de R$299 mil de faturamento em 30 dias, TACOS de 4,6% | `DZXgH6-u-Ri`, 2026-06-09 | [CASE] | Fecha com venda de evento |
| Biel Seller | Custo do FULL baixo sobre R$120 mil de faturamento | `7597198803380292885`, 2026-01-19 | [CASE] | Tarifas podem estar superadas |
| Bropinheiro | Armazenagem FULL de R$1.973 → R$1.431 por mês | `7641347634120150280`, 2026-05-18 | [CASE] | Redução atribuída aos "produtos estrela" |
| "Maior vendedor do ML" | R$7 milhões com base de seguidores fiéis | `DZsM3V9t498` (legenda), 2026-06-17 | [CASE não confirmado] | Sem nome nem fonte |

---

## Conteúdo e venda de curso

| Post | Conteúdo aproveitável | Chamada de venda | Avaliação |
|---|---|---|---|
| `DcecUj8x6Sb` Julio Aramaqui | Funil de métricas completo | Nenhuma explícita | Conteúdo puro, o mais útil da base |
| `DeSaMOnJ820` Bruno Gontijo | Faixas de tarifa fixa e margem | Usa ferramenta externa, sem CTA forte | Conteúdo |
| `DYzLkXQhDR1` Diego Rojas | Tendências e campos indexados | Nenhuma | Conteúdo |
| `DdmFpTdpl3q` Gabriel Paiva | Conta de margem com números | "Comenta PREÇO" para o time chamar | Conteúdo + captura de lead para consultoria |
| `DZXgH6-u-Ri` Alex Moro | Cálculo de TACOS | Evento pago | Conteúdo + venda de evento |
| `DcuJYVVBOMx` / `7680324894680304917` Rafael Sasso | Escada de ROAS e orçamento | "Me segue e manda mensagem" | Receita com números sem base + captação |
| `7657666675122130192` Fabio Ludke | Mudança de ACOS para ROAS; criação de campanha | — | Conteúdo |
| `7517394661351148805` Natan Aquino | Campanha básica (tela antiga) | Comentários | Conteúdo, possivelmente superado |
| `Db9NvEIDHC9` Hunter HUB | Custos do FULL e regra de giro | "Comenta HUNTER", 7 dias grátis | Conteúdo + venda de ferramenta |
| `DcW9TahOHTw` Leo Mantovan | Preço a partir da margem | "Comenta SITE" | Isca de ferramenta |
| `7636173974195440903` Leonardo Tonchak | Planilha vs. calculadora oficial | "Comenta Eu quero" | Isca de planilha |
| `7685861706622389511` Marina Wolff | Palavras-chave na descrição (contestável) | Mentoria, consultoria, manual | **Promessa > conteúdo** |
| `DZYP9wNveF2` Raphael | "Ads não é obrigatório" | Crítica a mentorias (o perfil também vende serviço) | Opinião + case |
| `Dd9wMyhvUrW` Bruno Maciel | "Reset" pelo editor de IA | — | Hipótese anedótica |
| `DcW7lXEyO1T` Léo dos Santos | Capacidade de envio | Seguir | Dica sem evidência |
| `7599012656275541266` vendernomercadolivre | Pouco (preço de café revendido) | Venda de lote, contato por WhatsApp | **Venda de produto disfarçada de dica** |
| `DXuvYKODltN`, `Db6v2BAuPU7` (legendas) | Nenhum | "Comenta MENTORIA" | Venda de mentoria |
| `DY5SzLDy6jh`, `DeeZ64fjtBN` (legendas) | Nenhum | Ferramenta parceira com cupom | Publi |
| `DbwbPmVidWZ`, `Da2lRL6idBG`, `DbNuqJHCbBH` Lucas Santos (legendas) | Não transcritos | IA para vender | Indefinido |

**Padrão geral:** a maior parte do conteúdo de valor é aula curta de fórmula (margem, TACOS, funil). A venda costuma vir como "comenta PALAVRA". As receitas com números mágicos (ROAS 25 / R$33, capacidade 1.500, palavras-chave na descrição) são as que mais acompanham venda de mentoria e as que menos trazem evidência.

---

## Observação dos líderes (medida nas páginas em 2026-10-14)

Fonte: `observacao/lideres.md` e `lideres.tsv`. São 13 páginas visitadas com sessão de comprador e CEP em MG. Todas as afirmações abaixo são [OBS], de 2026-10-14.

1. **O FULL domina a primeira página de café:**
   - 26 de 40 resultados em "cafe em graos", 21 de 30 em "cafe moido" e 22 de 25 em "cafe capsulas".
   - Os sem FULL no topo são, em geral, cafés especiais pequenos (+25 a +500 vendidos). As exceções com volume são Appassionato e Serra do Encontro.
   - Isso bate com o que os criadores dizem (FULL converte), mas a observação não separa causa de efeito.
2. **O catálogo (/p/) concentra a disputa, e a buy box nem sempre é da marca:**
   - Pilão: 72 ofertas, com buy box de um supermercado (MLB35944622).
   - Italle: buy box com a loja oficial Healthy Coffee, enquanto a loja oficial Italle aparecia mais cara (MLB26184226).
   - Mondial: buy box com um vendedor de "Atendimento ruim" (MLB18932156).
   - Nota, opiniões e vendidos pertencem ao produto, e não ao vendedor.
3. **Lojas oficiais com linha ampla ocupam várias posições:**
   - Orfeu aparece 5 vezes entre os 40 primeiros de grãos, além de drip e cápsulas.
   - Italle é 1º em grãos e em moído e aparece com cápsulas de 50 e 100.
   - O padrão é cobrir formatos (grão, moído, cápsula, drip) e tamanhos (250 g, 500 g, 1 kg).
4. **O preço aparece em camadas:**
   - "De" riscado, preço Pix (8% a 53% OFF) e preço em outros meios, além de "preço por quilo" na página (Italle R$67/kg, Pilão R$83,89/kg).
   - Faixas por kg: supermercado de R$32 a R$84, gourmet ou especial de marca de R$90 a R$160 e microlote acima de R$200.
5. **Desconto por quantidade dentro do anúncio:**
   - Appassionato: 5 un a R$92/un e 10 un a R$89,90/un.
   - Pilão: 5 un a R$66,39/un.
   - Italle: R$48,80/un a partir de 100 un.
   - Kits (2 un, 4×250 g, café + moedor) aparecem como anúncios separados.
6. **Prova social no topo da página:**
   - Selo "MAIS VENDIDO" com posição na categoria (ex.: "3º em Café Moído e em Grão").
   - Vendidos em faixas ("+100 mil") e nota de 4,7 a 4,9 com milhares de opiniões (Italle 6.703; Orfeu 3.410).
   - Oferta relâmpago com contador.
7. **Reputação máxima e seguidores:**
   - Italle, Orfeu e Healthy Coffee são MercadoLíder Platinum; Appassionato é Gold.
   - Seguidores: Italle +35,3 mil, Orfeu +11,7 mil e Appassionato +2.700.
   - Isso é coerente com a ênfase dos criadores em Minha Página e seguidores (`DbodEv8vHdl`, `DZsM3V9t498`).
8. **O título é escrito para a busca:**
   - O líder em grãos usa título genérico sem a marca no início: "Cafe Graos Torrado Torra Media Arábica Em Grãos 1kg Gourmet".
   - O de cápsulas repete "cápsula" 4 vezes.
   - Marcas tradicionais usam o formato curto marca + formato + peso + torra.
   - Isso confirma a orientação de título por palavra buscada (`DXhRiCCERsG`, `DYzLkXQhDR1`).
9. **Galeria:** 6 a 9 miniaturas nos cafés abertos, com vídeo confirmado só no Italle. Fica abaixo do checklist de "10 fotos + 3 clipes" de `DefTt6LEhSG`, ou seja, os líderes de café não seguem esse checklist à risca.
10. **O top 20 de Alimentos e Bebidas só tem marcas nacionais muito conhecidas:**
    - União 500 g é o 6º (+500 mil) e Melitta 500 g o 12º, com preço de supermercado (R$16 a R$22 por 500 g).
    - Os itens são vendidos por FULL/Supermercado e, várias vezes, por revendas.
11. **Fora de alimentos:**
    - Marca própria de importado combina título longo (cerca de 200 caracteres empilhando compatibilidades) com "de/por" agressivo: Redfin de R$114,90 por R$41,32; Woosh com 80% OFF.
    - Esse padrão é **específico de importação**.
    - Marca nacional (Mondial) concentra variações de cor e voltagem num catálogo único, com cerca de 200 mil opiniões.

**Indústria/marca própria vs. revenda, na observação:**

- **Marca:** loja oficial, linha completa, FULL, preço por kg dentro da faixa do segmento, desconto progressivo e Platinum.
- **Revenda:** disputa a buy box de catálogos de marcas grandes por preço e não controla título, fotos nem avaliações.

**Limitações:**

- O rótulo "Patrocinado" não foi capturado, então não dá para separar orgânico de Product Ads.
- O FULL foi medido só nos cards da busca.
- Os vendidos aparecem em faixas.
- Os resultados valem para um CEP em MG.

---

## Tabela de afirmações

| id | afirmação | tipo | fonte | data |
|---|---|---|---|---|
| S01 | Campanhas de Product Ads agora são configuradas por ROAS objetivo, e não mais por ACOS objetivo; ACOS = 1/ROAS | [PRÁTICA] (mudança de plataforma relatada) | `7657666675122130192` | 2026-07-01 |
| S02 | Receita iniciante: ACOS de 5%, R$10/dia, uma campanha por produto, rodar de 5 a 7 dias | [PRÁTICA] — pode estar superada | `7517394661351148805` | 2025-06-18 |
| S03 | Começar com ROAS objetivo de 15 numa campanha "teste todos"; orçamento mínimo de R$50/dia | [PRÁTICA] | `7657666675122130192` | 2026-07-01 |
| S04 | Campanha "mais vendidos" com ROAS de 25 e R$33; depois de 5 vendas, ROAS de 15 e R$51 | [PRÁTICA] | `DcuJYVVBOMx` / `7680324894680304917` | 2026-08-31 |
| S05 | ROAS objetivo mais alto faz a plataforma entregar menos o produto | [PRÁTICA] | `DcuJYVVBOMx` | 2026-08-31 |
| S06 | TACOS (Ads ÷ faturamento total) é a métrica de controle; caso com TACOS de 4,6% e teto de 6% | [CASE] | `DZXgH6-u-Ri` | 2026-06-09 |
| S07 | Operação com cerca de R$1,5 milhão em 30 dias sem investir em Ads | [CASE] | `DZYP9wNveF2` | 2026-06-09 |
| S08 | Ferramenta "Aumentar Seguidores" do Mercado Ads gera vídeo com IA; seguidores comprariam até 60% mais | [DADO] não confirmado | `DZsM3V9t498` (legenda) | 2026-06-17 |
| S09 | Margem real de um item de R$55,90 com custo de R$22 é de R$8,94 (cerca de 16%) depois de comissão de 14%, imposto de 8%, Ads de 5%, frete de R$8,75 e 2% de outros | [PRÁTICA] | `DdmFpTdpl3q` | 2026-09-22 |
| S10 | Margem mínima recomendada de 20%; comissão clássica de 11% a 14% e premium de 15% a 19% ("se não me engano") | [PRÁTICA] | `DYSu4iqBx4I` | 2026-05-13 |
| S11 | A calculadora oficial não inclui imposto nem embalagem; premium usado a 18% | [PRÁTICA] | `7636173974195440903` | 2026-05-04 |
| S12 | Abaixo de R$79 a tarifa fixa muda por faixa (R$19–48,99; R$49–78,99); baixar o preço para a faixa inferior pode aumentar a margem | [PRÁTICA] (regra a confirmar) | `DeSaMOnJ820` | 2026-10-09 |
| S13 | Ativar a central de promoções desde o primeiro dia; 10 fotos e 3 clipes; FULL, Flex, Places e afiliados | [PRÁTICA] | `DefTt6LEhSG` | 2026-10-14 |
| S14 | Custos do FULL: armazenagem (mais cara depois de 6 meses), envio, comissão e capital preso; abaixo de cerca de 3 un/dia, evitar | [PRÁTICA] | `Db9NvEIDHC9` | 2026-08-12 |
| S15 | Custo do FULL de cerca de R$0,80 de coleta por produto e R$0,21/mês de armazenagem de item pequeno | [CASE] — pode estar superada | `7597198803380292885` | 2026-01-19 |
| S16 | Armazenagem FULL caiu de R$1.973 para R$1.431 por mês; produto "estrela" com 1.000+ un não pagaria armazenagem | [CASE] / regra não confirmada | `7641347634120150280` | 2026-05-18 |
| S17 | Subir a "Capacidade de envios" para cerca de 1.500 sinalizaria ao algoritmo que a operação aguenta demanda | [PRÁTICA] sem evidência | `DcW7lXEyO1T` | 2026-08-22 |
| S18 | ML prevê 42 centros de distribuição FULL no Brasil até o fim de 2026 | [DADO] (repasse de notícia) | `DeZWuzjxmYi` (legenda) | 2026-10-12 |
| S19 | Novo centro em Gravataí (RS), de 38,7 mil m² e com 720 colaboradores | [DADO] (repasse de notícia) | `DefJhl-PjRG` (legenda) | 2026-10-14 |
| S20 | A busca lê título, ficha técnica e variações; a descrição não indexa; usar "Tendências" do ML para palavras-chave | [PRÁTICA] | `DYzLkXQhDR1` | 2026-05-26 |
| S21 | Colar palavras-chave geradas por IA no fim da descrição melhora a entrega (contradiz S20) | [PRÁTICA] contestável | `7685861706622389511` | 2026-09-15 |
| S22 | Funil visitas → intenção → venda; intenção abaixo de 10% = fotos/descrição; venda abaixo de 25% da intenção = preço/logística | [PRÁTICA] | `DcecUj8x6Sb` | 2026-08-25 |
| S23 | Passar a foto de capa no editor de IA do ML "reseta" a exposição de anúncio que caiu | [PRÁTICA] anedótica | `Dd9wMyhvUrW` | 2026-10-01 |
| S24 | Loja de alto ticket: 712 vendas via Minha Página, custo por seguidor de R$1,75, 81% mobile, R$1,2 milhão em 7 dias | [CASE] | `DbodEv8vHdl` | 2026-08-04 |
| S25 | Título deve usar a palavra que o comprador digita; reputação verde é o maior ativo | [PRÁTICA] | `DXhRiCCERsG` (legenda) | 2026-04-24 |
| S26 | Revenda de café: custo de R$19, venda de R$29,90–33 no FULL, margem de 20% a 32% depois da nota; mínimo de 100 un | [PRÁTICA] promessa comercial, revenda — pode estar superada | `7599012656275541266` | 2026-01-24 |
| O01 | FULL em 26 de 40 ("cafe em graos"), 21 de 30 ("cafe moido") e 22 de 25 ("cafe capsulas") resultados | [OBS] | lista.mercadolivre.com.br/cafe-em-graos, /cafe-moido, /cafe-capsulas | 2026-10-14 |
| O02 | Pilão 1 kg com 72 ofertas no catálogo e buy box de supermercado revendedor | [OBS] | mercadolivre.com.br/p/MLB35944622 | 2026-10-14 |
| O03 | Buy box do Italle 1 kg com outra loja oficial (Healthy Coffee); Italle oficial mais cara | [OBS] | mercadolivre.com.br/.../p/MLB26184226 | 2026-10-14 |
| O04 | Orfeu ocupa 5 das 40 posições da busca de grãos e aparece também com drip e cápsulas | [OBS] | lista.mercadolivre.com.br/cafe-em-graos | 2026-10-14 |
| O05 | Líderes de alimentos exibem desconto Pix de 8% a 53% e "preço por quilo" | [OBS] | mais-vendidos/MLB1403; MLB26184226; MLB35944622 | 2026-10-14 |
| O06 | Desconto por quantidade no anúncio (Appassionato 5 un a R$92/un; Pilão 5 un a R$66,39/un; Italle 100+ a R$48,80/un) | [OBS] | MLB61809843; MLB35944622; busca de grãos | 2026-10-14 |
| O07 | Italle, Orfeu e Healthy Coffee são MercadoLíder Platinum; Italle tem +35,3 mil e Orfeu +11,7 mil seguidores | [OBS] | MLB26184226; MLB28606704; MLB21862682 | 2026-10-14 |
| O08 | Líder em grãos usa título genérico rico em palavra-chave, sem a marca no início; cápsulas repetem "cápsula" 4 vezes | [OBS] | MLB26184226; MLB21862682 | 2026-10-14 |
| O09 | Galerias de café com 6 a 9 miniaturas; vídeo confirmado só no Italle | [OBS] | lideres.tsv | 2026-10-14 |
| O10 | Top 20 de Alimentos e Bebidas só com marcas nacionais líderes; União 500 g em 6º e Melitta 500 g em 12º | [OBS] | mercadolivre.com.br/mais-vendidos/MLB1403 | 2026-10-14 |
| O11 | Marca própria de importado usa título de cerca de 200 caracteres e "de/por" agressivo (Redfin R$114,90 → R$41,32) — específico de importação | [OBS] | mercadolivre.com.br/p/MLB39960346; MLB20306137 | 2026-10-14 |
| O12 | Nota e avaliações pertencem ao catálogo: buy box do Mondial estava com vendedor de "Atendimento ruim" | [OBS] | mercadolivre.com.br/p/MLB18932156 | 2026-10-14 |
