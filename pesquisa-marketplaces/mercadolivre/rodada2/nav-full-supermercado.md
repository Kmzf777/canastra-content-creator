# Rodada 2 (navegador): Full, Supermercado e estoque

Frente: nav-full-supermercado. Ferramenta: Claude in Chrome, numa aba própria, fechada no fim. Data de acesso de todas as páginas: 2026-10-15. Nenhuma página da Central de Ajuda (mercadolivre.com.br/ajuda/<id>) mostra data de publicação ou de atualização. Não houve captcha nem página que exigisse login para ler. Pausa de 6 a 10 s entre páginas do ML.

Fecha: LACUNAS §4 itens 12 e 15; §1.3 (Q2 e "sem fonte oficial": R5, R6, R9); §1.7 (convivência 23329 × entrada automática; "produtos selecionados"; 24/08); §1.9 (linhas de logística: R2, R5, R8).

## Resumo

1. **Conciliação 23329 × entrada automática (§1.7, P0 item 12).** As duas regras falam de coisas diferentes e convivem.
   - A ajuda/23329 restringe **alguns produtos** de Supermercado, e não a categoria inteira. Trecho: "alguns produtos estarão habilitados somente para vendedores autorizados". Novos vendedores autorizados não serão incluídos. O estoque restrito que já está no Full continua à venda até acabar.
   - A ajuda/5200, de itens proibidos no Full, traz na lista "Produtos de supermercado habilitados para vendedores autorizados", com link para a 23329. Ou seja, a restrição é uma **lista de produtos proibidos de entrar no Full** para quem não é autorizado.
   - A nota "Como vender produtos de Supermercado" diz que o estoque no Full numa categoria de supermercado passa a participar "automaticamente" do Supermercado. A nota não menciona vendedor autorizado nem produto restrito. Pela estrutura da página, parece antiga (ver item 1.2).
   - Leitura conciliada [OBS, inferência]: um produto de categoria de supermercado **fora** da lista restrita pode ir ao Full e entra sozinho no Supermercado. Já um produto **da** lista restrita não pode ser enviado por quem não é autorizado. Qual produto está na lista **não é público**: nenhuma página traz a lista nem o critério. Do lado de fora não se resolve se um item específico, como café, está restrito. A resposta depende de checar no painel do vendedor ("Controle de estoque" ou o fluxo de envio), o que esta frente não fez.
2. **Full Super, R$ 1,60 × R$ 2,40 (ajuda/49972).** Confirmado de novo, linha a linha. Até 1 kg, na faixa de R$ 29 a R$ 48,99, os "produtos selecionados" pagam R$ 1,60 e os demais R$ 2,40. O benefício vale "automaticamente" para publicações ligadas ao catálogo. A lista de selecionados é um **PDF no CDN do ML** (http2.mlstatic.com). Não foi aberto, porque baixar arquivo exige autorização (ver Aberto).
3. **Data de 24/08.** Achei a ajuda/48578, de título "Custos do Envios no Mercado Livre a partir de 24 de agosto". O título não traz o ano. A página é só um índice das três tabelas por reputação e não menciona o Full Super. Isso confirma oficialmente a data de **24 de agosto** para a tabela geral de envio. Não confirma que a divisão "selecionados/demais" do Full Super começou nessa data.
4. **Custos do Full que ainda não tinham sido lidos (P1 item 15):**
   - A ajuda/24253, de armazenagem diária, carregou e confirma: P R$ 0,007, M R$ 0,015, G R$ 0,050 e XG R$ 0,107 por unidade e por dia. No Supermercado, P e M são grátis, G custa R$ 0,014 e XG R$ 0,025.
   - A ajuda/26342 lista as isenções.
   - A ajuda/16645 traz a retirada e o descarte por m³ (tabela abaixo).
   - A ajuda/42158 descreve o estoque compartilhado.
   - A 42159 foi relida e se confirma.
   - A ajuda/2518 redireciona para a 2517, "Anúncios duplicados", que permite o mesmo produto em outro anúncio para oferecer forma de envio diferente.
5. **Extragrandes.** A ajuda/44922 está vigente: 20 kg, 80 cm e 125 L, com exceção por preço mínimo. A tabela agora abre e mostra **R$ 100 (26 itens) e R$ 200 (4 itens)**, com 258 itens "Sem exceção". A página não traz a data de 20/05/2026. Nenhuma das 25 categorias da lista é Alimentos e Bebidas. A ajuda/15573 continua com o limite geral (menos de 25 kg, lado de até 120 cm, soma de até 260 cm) e manda conferir antes a lista de extragrandes. **As duas não se contradizem**: a 44922 é uma restrição adicional, por categoria, dentro do limite geral. A menção a "mais de 18 kg" vem da definição do **tamanho de armazenagem XG** (24253 e 15373), e não do limite de entrada.
6. **Estoque antigo (ajuda/15373)** relido: bate com [log R2] e [alim A4]. Supermercado a partir de 2 meses, demais produtos a partir de 4 meses.
7. **Alerta de método.** O "caminho" no topo das páginas da Central de Ajuda (a trilha de links) **acumula o histórico de navegação da sessão**, e não a hierarquia real. Ele foi crescendo a cada página visitada (até "Anúncios duplicados" apareceu nele). Nenhuma nota deve concluir, pela trilha, que uma página é "filha" da 23329.

## Achados por item

### 1. Supermercado no Full: 23329, 5200 e a nota de entrada automática (LACUNAS §4 item 12; §1.7)

**1.1 ajuda/23329**: "Produtos de Supermercado habilitados para vendedores autorizados". https://www.mercadolivre.com.br/ajuda/23329, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta.
- O motivo declarado é otimizar o espaço de armazenamento. Trecho: "somente alguns vendedores poderão enviar este tipo de estoque".
- Trecho sobre o escopo: "alguns produtos estarão habilitados somente para vendedores autorizados".
- Trecho sobre novos autorizados: "não incluiremos mais vendedores autorizados de Supermercado no Full". A página recomenda outro método do Mercado Envios.
- O estoque restrito já armazenado continua à venda "até se esgotarem".
- A página não traz a lista de produtos restritos, o critério nem uma data.

**1.2 Nota da Central de Vendedores**: "Como vender produtos de Supermercado: junte-se à categoria que só cresce". https://vendedores.mercadolivre.com.br/aprender/nota/supermercado-aprenda-a-vender-esses-produtos-e-junte-se-a-uma-categoria-em-crescimento, sem data, acesso em 2026-10-15 [OFICIAL], confiança média.
- O corpo da nota não aparece na tela: só o título e o subtítulo são renderizados. O texto foi lido no conteúdo embutido na página (HTML).
- Seção "Como participar do Supermercado do Mercado Livre". Trecho: "Se o estoque estiver no Full e fizer parte das seguintes categorias". Trecho seguinte: "você estará automaticamente participando".
- A nota não usa as palavras "autorizad" nem "restrit". "Habilitad" aparece 2 vezes, fora desse contexto.
- Os títulos da nota usam a classe de estilo "shiny-h2-2019". É um indício [OBS] de que o modelo da página é de 2019, anterior à restrição da 23329. Por isso a confiança é média para o estado atual.
- Obs.: o código da página contém dados da conta conectada no navegador. Não foram lidos nem registrados.

**1.3 ajuda/5200**: "Quais produtos são proibidos de enviar ao Full?". https://www.mercadolivre.com.br/ajuda/5200, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta.
- Sob "restrições legais ou políticas do site", a página lista: "Produtos de supermercado habilitados para vendedores autorizados", com link para a 23329.
- Restrições especiais:
  - Produtos, kits e packs de supermercado **sem código universal de fábrica**.
  - Produtos que exigem controle de umidade e temperatura ou refrigeração controlada.
- Consumo recorrente com validade próxima do vencimento. A validade deve estar legível, no idioma do país e não escrita à mão.
- Itens com pragas ou fungos, ou sem embalagem primária adequada.
- Lista de categorias com restrição de peso e tamanho: assadeiras, colchões, copos e taças, pneus etc. Nenhuma é de alimento.
- Produto restrito que for enviado não fica à venda e precisa ser retirado.

**1.4 ajuda/33536**: "Categorias de supermercado*". https://www.mercadolivre.com.br/ajuda/33536, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta.
- A página lista "Alimentos e Bebidas (exceto comidas preparadas, ... congelados, refrigerados, instantâneos, embutidos, confeitaria e corantes e lúpulos)", além de limpeza, higiene etc.
- Asterisco: "Há exceções em alguns casos" e "a lista está sujeita a alterações".

**1.5 Conciliação.** Ver Resumo, item 1. Fecha a contradição apontada em §1.7: não há conflito de texto. Fica aberta uma lacuna nova, menor e verificável: **quais produtos estão na lista restrita**.

### 2. Full Super: requisitos, tabela e "produtos selecionados" (§4 item 12; §1.7; §1.9 [log R8])

**2.1 ajuda/16449**. https://www.mercadolivre.com.br/ajuda/16449, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta.
- Requisitos: preço acima de R$ 8 ("Exceções podem existir em casos específicos"), reputação verde, categoria de supermercado e estoque num CD do Full.
- Custos: tarifa de venda mais o custo de envio. G e XG pagam armazenagem diária; P e M não pagam.
- Frete: grátis a partir de R$ 199 na loja Full Super, contra R$ 79 fora dela.
- Vantagem declarada: "destaque nas buscas dos compradores".
- O que é novo em relação à rodada anterior: o ML "pode abrir exceções" por definição comercial de marcas. Trecho: "Caso o produto deixe de cumprir algum desses requisitos, é possível que não faça mais parte da loja".

**2.2 ajuda/49972**: "Custos do Envios no Mercado Livre para anúncios de Full Super". https://www.mercadolivre.com.br/ajuda/49972, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta.
- O custo é calculado pelo maior valor entre o peso físico e o volumétrico.
- A lista de "Produtos selecionados" tem custo menor. O benefício vale "automaticamente às publicações com produtos associados ao catálogo".
- A lista fica num link para um PDF: `http2.mlstatic.com/storage/cx-support-fcm-api/fcm-pub-os-prod/content-hub/anaescobar/produtos selecionados fullsuper .pdf`. Não foi aberto (é download). A tentativa de ler só o cabeçalho (HEAD) foi bloqueada pelo navegador (CORS).
- Trecho da tabela até 1 kg:

| Preço | Selecionados | Demais |
|---|---|---|
| R$ 0–18,99 | R$ 1,00 | R$ 1,40 |
| R$ 19–28,99 | R$ 1,20 | R$ 1,80 |
| R$ 29–48,99 | **R$ 1,60** | **R$ 2,40** |
| R$ 49–78,99 | R$ 2,40 | R$ 3,60 |
| R$ 79–98,99 | R$ 3,20 | R$ 4,80 |
| R$ 99–198,99 | R$ 4,80 | R$ 7,20 |
| a partir de R$ 199 | R$ 21,65 a R$ 24,45 (igual nas duas tabelas) | idem |

- A diferença entre selecionados e demais existe só até 8 kg. De 8 kg para cima, as duas tabelas são idênticas: de 8 a 9 kg, R$ 5,00, 7,50, 9,10 e assim por diante.
- Nota: produtos de menos de R$ 29 pagam no máximo 25% do preço.
- Atenção: o valor R$ 2,40 aparece nas duas tabelas, em células diferentes (demais a R$ 29–48,99; selecionados a R$ 49–78,99). Nas notas, a comparação deve ser feita sempre dentro da mesma faixa de preço.
- O critério de seleção não aparece, além de "associados ao catálogo". A página não diz se é por EAN, por marca ou por desempenho.

**2.3 ajuda/48578**: "Custos do Envios no Mercado Livre a partir de 24 de agosto". https://www.mercadolivre.com.br/ajuda/48578, sem data de página, acesso em 2026-10-15 [OFICIAL], confiança média quanto ao ano.
- A página é um índice com três itens: MercadoLíder, reputação verde ou sem reputação; reputação amarela; reputação vermelha.
- Confirma "24 de agosto" como início da tabela geral de envio. O ano não está escrito; 2026 é inferência pelo contexto, porque as tabelas atuais (40538) estão vigentes.
- Não cita o Full Super nem os "produtos selecionados".
- Fecha em parte [pre A7] e [log A25] quanto à data, mas não quanto ao "+1,6%".

### 3. Armazenagem, isenções, retirada e descarte (§4 item 15; §1.3 Q2)

**3.1 ajuda/24253**: "Custo pelo serviço de armazenamento diário no Full". https://www.mercadolivre.com.br/ajuda/24253, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta. Na rodada anterior essa página "redirecionou"; agora carregou.
- O custo vale para unidades aptas **e não aptas**, desde a entrada no CD até a venda ou a retirada.
- Tamanhos: P até 12×15×25 cm; M até 28×36×51 cm; G até 60×60×70 cm; todos com até 18 kg. XG é o que passa de 60×60×70 cm e/ou de 18 kg.
- Geral, por unidade e por dia: P R$ 0,007, M R$ 0,015, G R$ 0,050, XG R$ 0,107.
- Supermercado: P grátis, M grátis, G R$ 0,014, XG R$ 0,025. Os exemplos citados são barra de cereal, garrafa de refrigerante, balde e vassoura.
- O acompanhamento é feito em "Controle de estoque" e no detalhe do faturamento.

**3.2 ajuda/26342**: unidades que não geram custo de armazenamento. https://www.mercadolivre.com.br/ajuda/26342, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta.
- Ficam isentas, temporariamente, as unidades nestas situações: extraviadas (em busca), em revisão, devolvidas pelo comprador, vendas canceladas, em revisão fiscal e em transferência entre CDs.
- Unidade extraviada que não volta à venda em 30 dias é paga ao vendedor via Mercado Pago, como "produto assegurado".

**3.3 ajuda/16645**: custos de retirada e descarte. https://www.mercadolivre.com.br/ajuda/16645, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta. O valor depende do volume total do estoque. O descarte é encaminhado para doação, reciclagem ou destruição, conforme o estado da unidade.

| Volume total | Retirar | Descartar |
|---|---|---|
| até 0,01 m³ | R$ 98 | R$ 1 |
| 0,01–0,025 m³ | R$ 80–201 | R$ 1–2 |
| 0,025–0,05 m³ | R$ 121–242 | R$ 1–3 |
| 0,05–0,1 m³ | R$ 185–370 | R$ 2–5 |
| 0,1–0,25 m³ | R$ 258–645 | R$ 4–9 |
| 0,25–0,5 m³ | R$ 475–950 | R$ 7–14 |
| 0,5–1 m³ | R$ 740–1.480 | R$ 12–24 |
| 1–2 m³ | R$ 1.300–2.600 (R$ 1.121/m³) | R$ 18–36 (R$ 18/m³) |
| 2–5 m³ | R$ 2.200–5.500 (R$ 1.020/m³) | R$ 34–85 (R$ 17/m³) |
| 5–10 m³ | R$ 4.950–9.900 (R$ 910/m³) | R$ 70–140 (R$ 17/m³) |
| 10–20 m³ | R$ 8.400–16.800 (R$ 796/m³) | R$ 140–280 (R$ 14/m³) |
| 20–50 m³ | R$ 13.540–33.850 (R$ 576/m³) | R$ 120–300 (R$ 6/m³) |
| mais de 50 m³ | a partir de R$ 29.500 (R$ 583/m³) | a partir de R$ 300 (R$ 6/m³) |

- Obs.: a faixa de 0,01 a 0,025 m³ começa em R$ 80, abaixo dos R$ 98 da faixa anterior, e o "por m³" de mais de 50 m³ (R$ 583) é maior que o de 20 a 50 m³ (R$ 576). As incoerências estão na página e foram transcritas como estão.
- A retirada pode ser paga na fatura do ML.

**3.4 ajuda/15373**: custos mensais por estoque antigo. https://www.mercadolivre.com.br/ajuda/15373, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta.
- O tempo conta para unidades aptas, não aptas e pendentes de retirada.
- O custo começa após 4 meses para todos os produtos e após 2 meses para Supermercado.
- Tabela geral (4–6 meses / 6–12 meses / mais de 12 meses): P R$ 1 / 12 / 28; M R$ 2 / 15,90 / 35; G R$ 6 / 40 / 92; XG R$ 8 / 52 / 145.
- Supermercado (2–4 / 4–6 / 6–12 / mais de 12 meses): P R$ 2,00 / 4,40 / 9,20 / 14,20; M R$ 3,40 / 8,10 / 15,50 / 24,10; G R$ 10,40 / 24,20 / 55,50 / 65,30; XG R$ 11,90 / 27,00 / 71,60 / 83,50.
- Bate com [log R2], [alim A4] e com a verificação (/15731). Aplica a reconciliação de §1.9 sobre [log R2].
- A página não menciona isenção de 180 dias para "estrelas" [log R11]. Segue sem fonte escrita.

### 4. Estoque compartilhado (§1.3 "sem fonte oficial"; [log R9])

**4.1 ajuda/42158**: "O que é 'Estoque compartilhado' no Full". https://www.mercadolivre.com.br/ajuda/42158, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta.
- Trecho sobre o ganho de prazo: chega "com cerca de 1 dia e meio de antecedência".
- Unidades idênticas (mesmo código universal) de vendedores diferentes são geridas de forma unificada. O ML entrega a unidade mais próxima do comprador e desconta do estoque de quem vendeu.
- A função é ativada "automaticamente" para produtos elegíveis, que entram aos poucos. O vendedor pode desativar em "Controle de estoque".
- Esse estoque dispensa a etiqueta do ML, porque o recebimento é pelo código universal.
- O vendedor não sofre impacto por problema de produto de outro vendedor. Vendedor fora do padrão de qualidade é retirado.

**4.2 ajuda/42159**: requisitos (relida). https://www.mercadolivre.com.br/ajuda/42159, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta.
- Vendedor com reputação verde.
- O produto precisa:
  - estar habilitado (o ML escolhe por categoria);
  - não ter reclamações;
  - ter experiência de compra de 75 ou mais;
  - ter o código universal impresso;
  - ser novo;
  - estar no catálogo;
  - não ter data de validade.
- Categorias excluídas: "Alimentos e Bebidas", Celulares, Cuidados pessoais, Brinquedos, Bebês e Livros, "entre outros".
- Conclusão para alimentos [OFICIAL, dupla exclusão]: alimento fica fora do estoque compartilhado pela categoria e também pela validade.

### 5. Anúncio a mais por forma de envio (ajuda/2518; [rank A21])

https://www.mercadolivre.com.br/ajuda/2518 **redireciona** para https://www.mercadolivre.com.br/ajuda/2517, "Anúncios duplicados". Sem data, acesso em 2026-10-15 [OFICIAL], confiança alta.
- Não se permitem anúncios do mesmo produto com as mesmas condições de venda, nem produtos idênticos separados só por variação, como cor.
- É permitido oferecer o mesmo produto em mais de um anúncio "para oferecer diferentes formas de envio ou condições de pagamento".
- Quem descumprir tem os anúncios excluídos e pode ter a conta desativada.
- Complementa [rank A21]: a exceção por forma de envio está escrita.

### 6. Limites de peso e medida e extragrandes (§1.3 [log R5], [log R6]; §1.9)

**6.1 ajuda/15573**: medidas e peso permitidos no Full. https://www.mercadolivre.com.br/ajuda/15573, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta.
- Limites medidos na embalagem principal: peso menor que 25 kg, algum lado de até 120 cm e soma dos lados de até 260 cm.
- A página manda conferir antes a lista de extragrandes restritos.
- Produto grande e pesado não é recebido na maioria dos CDs. Se for enviado, deve ser retirado em até 30 dias; depois disso é descartado, com custo de descarte.
- Exceção: o CD Cajamar SP09 recebe grandes e pesados.

**6.2 ajuda/44922**: "Produtos extragrandes restritos para envio ao Full". https://www.mercadolivre.com.br/ajuda/44922, sem data, acesso em 2026-10-15 [OFICIAL], confiança alta nos limites e média na data.
- Para "produtos extragrandes da lista", o envio fica restrito quando o produto tem peso de 20 kg ou mais, algum lado de 80 cm ou mais, ou volume de 125 L ou mais.
- A exceção por preço mínimo agora está visível: **R$ 100 em 26 subcategorias e R$ 200 em 4**. As outras 258 linhas dizem "Sem exceção".
- A lista tem 25 categorias de topo, de Acessórios para Veículos a Segurança para casa. Nenhuma é Alimentos e Bebidas nem Supermercado.
- A página termina dizendo que esses produtos podem ser vendidos por outras logísticas.
- **Não traz a data de 20/05/2026**, que segue só "via terceiro" (hz-H-lBm390). A busca restrita a mercadolivre.com.br não achou comunicado datado.

**6.3 Confronto.** A afirmação da LACUNAS §1.3 de que "a página oficial ainda fala em mais de 18 kg e até 25 kg" junta três regras diferentes:
- até 25 kg é o limite geral de entrada (15573);
- 18 kg é o corte do tamanho de **armazenagem** XG (24253 e 15373);
- 20 kg, 80 cm e 125 L é a restrição por lista de categorias (44922).

As três estão vigentes ao mesmo tempo e não se contradizem. [log R6] passa de PARCIAL para CONFIRMADA nos limites e nos valores R$ 100/200. Só a data continua sem fonte oficial.

## Tabela de afirmações novas

Sigla: FS (Full/Supermercado). Todas foram acessadas em 2026-10-15.

| id | Afirmação | Tipo | Fonte | Data da página | Confiança | Fecha |
|---|---|---|---|---|---|---|
| R2-FS-1 | A ajuda/23329 restringe **alguns produtos** de Supermercado a vendedores autorizados; não entram novos autorizados; o estoque restrito já armazenado segue à venda até acabar | OFICIAL | mercadolivre.com.br/ajuda/23329 | sem data | alta | §1.7; §4 item 12; [alim A3] |
| R2-FS-2 | A ajuda/5200 inclui "Produtos de supermercado habilitados para vendedores autorizados" na lista de proibidos no Full, com link para a 23329 | OFICIAL | mercadolivre.com.br/ajuda/5200 | sem data | alta | §1.7 (conciliação) |
| R2-FS-3 | A nota da Central diz que o estoque no Full em categoria de supermercado entra "automaticamente" no Supermercado; não menciona autorizados; o modelo da página indica origem em 2019 | OFICIAL + OBS | vendedores.mercadolivre.com.br/aprender/nota/supermercado-aprenda-a-vender-esses-produtos-e-junte-se-a-uma-categoria-em-crescimento | sem data | média | §1.7; [alim §2.4] |
| R2-FS-4 | Conciliação: a entrada automática vale para produtos de supermercado fora da lista restrita; a lista restrita não é pública | OBS (inferência de R2-FS-1 a R2-FS-3) | idem | — | média | §1.7; consolidado §7 item 16 |
| R2-FS-5 | No Supermercado entram "Alimentos e Bebidas", exceto preparados, congelados, refrigerados, instantâneos, embutidos, confeitaria e corantes; a lista "está sujeita a alterações" | OFICIAL | mercadolivre.com.br/ajuda/33536 | sem data | alta | §1.7 |
| R2-FS-6 | No Full, kits e packs de supermercado sem código universal de fábrica são proibidos | OFICIAL | mercadolivre.com.br/ajuda/5200 | sem data | alta | §1.3; [log R5] |
| R2-FS-7 | Full Super: preço acima de R$ 8 com exceções comerciais; o ML pode abrir exceções por marca; quem deixa de cumprir pode sair da loja | OFICIAL | mercadolivre.com.br/ajuda/16449 | sem data | alta | [log R8]; [alim A6] |
| R2-FS-8 | Full Super até 1 kg, R$ 29–48,99: selecionados R$ 1,60, demais R$ 2,40; a diferença existe só até 8 kg; acima de R$ 199 as duas tabelas são iguais | OFICIAL | mercadolivre.com.br/ajuda/49972 | sem data | alta | §1.7; [alim A7]; [pre R5] |
| R2-FS-9 | A lista de "produtos selecionados" é um PDF no CDN do ML; a seleção vale automaticamente para publicações ligadas ao catálogo; o critério não é publicado | OFICIAL | ajuda/49972 (link para http2.mlstatic.com) | sem data | alta (o PDF não foi lido) | §1.7 (em parte) |
| R2-FS-10 | Há página oficial "Custos do Envios ... a partir de 24 de agosto" (índice das três tabelas por reputação); não cita o Full Super; o ano não está escrito | OFICIAL | mercadolivre.com.br/ajuda/48578 | sem data | média | [pre A7]; [log A25]; §1.7 (data, em parte) |
| R2-FS-11 | Armazenagem diária geral: P R$ 0,007, M 0,015, G 0,050, XG 0,107; Supermercado: P/M grátis, G 0,014, XG 0,025; vale para unidades aptas e não aptas | OFICIAL | mercadolivre.com.br/ajuda/24253 | sem data | alta | §1.3 Q2; §4 item 15; [alim A5] |
| R2-FS-12 | Isenções de armazenagem: extraviadas, em revisão, devolvidas, canceladas, em revisão fiscal e em transferência; extraviada que não volta à venda em 30 dias é paga ao vendedor | OFICIAL | mercadolivre.com.br/ajuda/26342 | sem data | alta | §1.3 Q2 |
| R2-FS-13 | Retirada: R$ 98 até 0,01 m³, chegando a R$ 583–1.121 por m³ em volumes grandes; descarte de R$ 1 a R$ 18 por m³; destino: doação, reciclagem ou destruição | OFICIAL | mercadolivre.com.br/ajuda/16645 | sem data | alta | §1.3 Q2; §4 item 15; [alim] pendência 16645 |
| R2-FS-14 | Estoque antigo: Supermercado a partir de 2 meses (P R$ 2,00 a XG R$ 83,50); demais a partir de 4 meses (P R$ 1 a XG R$ 145); conta também não aptas e pendentes de retirada | OFICIAL | mercadolivre.com.br/ajuda/15373 | sem data | alta | §1.9 [log R2]; [alim A4] |
| R2-FS-15 | Estoque compartilhado: cerca de 1,5 dia a menos no prazo; unidades idênticas pelo código universal; ativação automática com opção de desativar; dispensa etiqueta | OFICIAL | mercadolivre.com.br/ajuda/42158 | sem data | alta | §1.3; [log R9] |
| R2-FS-16 | Estoque compartilhado exclui "Alimentos e Bebidas" e produto com validade; exige reputação verde, experiência de 75 ou mais, catálogo e código universal | OFICIAL | mercadolivre.com.br/ajuda/42159 | sem data | alta | [log R9] (reconfirmação) |
| R2-FS-17 | A ajuda/2518 redireciona para a 2517 (duplicados): é permitido o mesmo produto em mais de um anúncio para oferecer forma de envio ou pagamento diferente | OFICIAL | mercadolivre.com.br/ajuda/2517 | sem data | alta | [rank A21]; §4 item 15 |
| R2-FS-18 | Limite geral do Full: menos de 25 kg, lado de até 120 cm, soma de até 260 cm; grande e pesado enviado deve ser retirado em 30 dias ou é descartado com custo; Cajamar SP09 é exceção | OFICIAL | mercadolivre.com.br/ajuda/15573 | sem data | alta | [log R5] |
| R2-FS-19 | Extragrandes da lista: 20 kg, 80 cm ou 125 L ou mais; preço mínimo de R$ 100 (26 itens) ou R$ 200 (4 itens); 258 itens sem exceção; nenhuma categoria de alimentos | OFICIAL | mercadolivre.com.br/ajuda/44922 | sem data | alta (limites e valores); a data de 20/05/2026 segue sem fonte oficial | [log R6]; [log A9] |
| R2-FS-20 | "18 kg" é o corte do tamanho de armazenagem XG, e não limite de entrada; as regras de 25 kg, 18 kg e 20 kg convivem | OBS (leitura cruzada de 15573, 24253 e 44922) | as três ajudas | — | alta | §1.3 (contestação "18 kg e até 25 kg") |
| R2-FS-21 | A trilha de links no topo das páginas da Central de Ajuda reflete o histórico da sessão, não a hierarquia; não deve ser usada para inferir que uma página é "filha" de outra | OBS | navegação nesta sessão | — | alta | método (todas as frentes) |

## Aberto

1. **Lista de "produtos selecionados" do Full Super**: é um PDF em `http2.mlstatic.com/.../produtos selecionados fullsuper .pdf`, linkado pela ajuda/49972. Abrir o PDF é baixar um arquivo e exige autorização explícita do usuário. O tamanho e a data não foram obtidos, porque o HEAD foi bloqueado por CORS. Com autorização, dá para ler o critério e conferir se há café.
2. **Lista de produtos de Supermercado restritos a vendedores autorizados** (23329/5200): não é pública. Só se verifica no painel do vendedor (fluxo de envio ao Full ou "Controle de estoque"). Fica fora do escopo desta frente, que só lê.
3. **Data de 20/05/2026 da restrição de extragrandes**: não aparece na 44922 nem em busca restrita ao domínio. Segue "via terceiro".
4. **Data de 24/08 para a divisão "selecionados/demais" do Full Super**: a 48578 confirma 24 de agosto só para a tabela geral (sem ano). O reajuste médio de +1,6% segue sem fonte oficial.
5. **Ajuda/48578, subpáginas**: os três itens (verde, amarela, vermelha) são botões de navegação e não foram abertos. Os valores da verde já estão confirmados na 40538 pela verificação.
6. **Incoerências internas da ajuda/16645** (a faixa de 0,01 a 0,025 m³ começa abaixo da faixa de até 0,01 m³; o preço por m³ de mais de 50 m³ é maior que o de 20 a 50 m³): convém reler em outro dia para ver se é erro de página.
7. **Isenção de 180 dias para SKUs estrela** [log R11]: não aparece na 15373 nem na 24253. Segue só no vídeo oficial.
8. **Validade no Full** (§1.3 Q8): a 5200 só proíbe validade "próxima do vencimento" e exige que a data esteja legível. Não há página com prazo mínimo em dias, alerta ou FEFO.
