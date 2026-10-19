# TikTok Shop: diagnóstico de prontidão (16/10/2026)

> Formato das agências: cada achado é **evidência → diagnóstico → risco de não agir → próximo passo**.
> Leitura no Claude in Chrome, **com a sessão de vendedor que já estava logada** no seu Chrome
> (Seller Center BR, loja "Cafe Canastra"), na madrugada de 16/10/2026 (arquivo gravado às 00:38).
> Conferido por outra sessão às 13h do mesmo dia: a tabela de margem bate com o script, e as constantes
> do script batem com o CONSOLIDADO §0 e §1.1. O painel não foi relido nessa conferência. **Nada foi criado, alterado,
> aceito ou inscrito.** Fechei dois modais sem acionar nada (amostras grátis e campanha). Números de
> margem saem de `tiktokshop/scripts/precificar_tiktok.py` (versão de 16/10/2026), com CMV e imposto de
> `mercadolivre/custos.md`.
>
> Abreviaturas: "kid=N" = `seller-br.tiktok.com/university/essay?knowledge_id=N` (Academy BR, data da
> página entre parênteses); "CONS §x" = `pesquisa-marketplaces/tiktokshop/CONSOLIDADO.md`;
> "painel" = Seller Center lido em 16/10/2026.

---

## Resumo em oito linhas

1. **Não é operação do zero: a loja existe e a porta de Alimentos está aberta.** Loja "Cafe Canastra" (código BRLCXJL2E9, CNPJ PJ, armazém na torrefação em Uberlândia), conta oficial **@cafecanastraoficial** vinculada desde 15/06/2026 e qualificação de **Alimentos e bebidas aprovada** ("Sempre válido"), cobrindo Café, Substitutos do café, Chá e Lanches › Kits para presente.
2. **Mas nada vende ainda:** 0 produtos, SPS sem nota, programa de afiliados não iniciado, nenhuma campanha de anúncio, 0/4 contas de marketing e o **questionário de novos vendedores não foi feito** (é requisito do nível Padrão).
3. **O maior risco é perder a categoria:** a regra (kid=7734094290093831, 29/09/2026) tira a qualificação se o **AHR cair a 150 ou menos ou o SPS ficar em 4 ou menos**. Hoje o AHR é 200 (Padrão, "Saudável"). Uma violação ou um SPS medíocre depois dos primeiros 30 pedidos tira o café da loja.
4. **A isenção de 0% por 60 dias não está garantida:** exige concluir a "missão do vendedor" em Crescimento › Oportunidades, e o painel mostra **0 missões disponíveis** (kid=24428156307201, 12/06/2026).
5. **A conta unitária só fecha no bloco especial.** Pelo script, o 1 kg com afiliado de 8% empata em **R$ 85,22** e dá 10% de CM3 em **R$ 99,41**. O 500 g precisa de **R$ 60,97** para 10%. O commodity da categoria (Italle 500 g a R$ 16,07, 57,2 mil vendidos) está abaixo do nosso CMV de R$ 26.
6. **A prateleira de especial é rasa e cara:** o 1 kg em grãos de torrefação pequena vende a R$ 85,90–99,90 com dezenas a centenas de vendidos (Cafetelier, 159; Moka Clube Mr Chocolate, 155; Spineli, 31). O comprador paga o frete abaixo do mínimo dos cupons (de R$ 5,88 a R$ 15,86 por pedido).
7. **Kit é a alavanca de preço:** o kit 2 × 1 kg a R$ 179,90 rende CM1 de **R$ 42,13** se contar como 1 item, contra R$ 36,06 em dois avulsos. A regra de "por item" continua sem resposta oficial (a página relida fala em "taxa por item vendido" sobre o "subtotal").
8. **A megacampanha 11.11 & Black Friday & 12.12 está aberta** (venda de 26/10 a 13/12/2026), exige **GMV Max** e dá cupons de 10% a 30% pagos pelo TikTok. A inscrição fecha em cerca de 57 dias. Sem produto cadastrado, ainda não há o que inscrever.

---

## 1. Conta e loja

| | |
|---|---|
| **Evidência** | Painel › Configurar loja: "Cafe Canastra", código **BRLCXJL2E9**. Centro de qualificação › Informações da empresa: CNPJ (Pessoa jurídica, LTDA), constituída em 25/02/2016, endereço na Rua Nivaldo Guerreiro Nunes, 701 (Uberlândia). Contas do TikTok vinculadas: **conta oficial @cafecanastraoficial, "Conta de organização", vinculada em 15/06/2026**; contas de marketing **0/4**, com 10 convites de vínculo em 180 dias. Página inicial: "O cadastro da sua loja foi aprovado!" e o roteiro de largada (envio e devoluções, NF-e, primeiro produto, conta do TikTok). Produtos: **0** (ativo, em análise, rascunho). |
| **Nível da loja** | O painel não mostra o nível na página inicial enquanto não há produto. Pela regra (kid=1444948507379472, 02/04/2026), toda loja nova começa em **Iniciante: 50 pedidos/dia e 1.000 anúncios**. **Padrão (100/dia):** ≥ 30 dias, **≥ 10 anúncios ativos**, **questionário aprovado**, < 4 violações em 30 dias, SPS ≥ 3,0. **Premium (200/dia):** ≥ 50 pedidos entregues, ≥ 10 compradores, SPS ≥ 3,5. **Profissional (sem limite):** ≥ 100 entregues, ≥ 20 compradores, SPS ≥ 3,5. A subida é automática e pode pular nível. |
| **Questionário** | Integridade da conta › Centro de treinamento: "Teste do período de avaliação do vendedor" está em **Disponíveis** (não feito). |
| **Diagnóstico** | Cadastro, CNPJ e conta oficial estão prontos. Faltam o questionário, os anúncios e o primeiro pedido. "Dias desde a iniciação" (≥ 30) **não medido**: o painel não mostra a data de abertura da loja. |
| **Risco de não agir** | Sem o questionário e com menos de 10 anúncios ativos, a loja fica presa em 50 pedidos/dia. Um criador que viralize no 1º mês esgota o produto ("Esgotado" pelo OVL), e o afiliado deixa de ganhar (CONS §2.3). |
| **Próximo passo** | **Você** faz o questionário (Integridade da conta › Centro de treinamento › Teste do período de avaliação). A meta de 10 anúncios ativos entra na decisão de portfólio (§5.2 do roteiro). |

## 2. A porta da categoria Alimentos

| | |
|---|---|
| **Evidência** | Centro de qualificação › Qualificação da categoria: duas solicitações para a mesma lista de 70+ subcategorias de Alimentos e bebidas. **(a) "Link da loja em outra plataforma de e-commerce", Sempre válido, Aprovado.** (b) "Histórico de vendas na categoria, Link de verificação", Rejeitado: as imagens precisavam mostrar o nome da loja, 12 meses, GMV em BRL e as avaliações. A lista aprovada inclui Bebidas › **Café**, **Substitutos do café**, **Chá** e Lanches › **Kits para presente**. |
| **Regra relida** | kid=7734094290093831 (29/09/2026): para anunciar e vender, **AHR > 150 e SPS > 4**, valendo também para lojas associadas. **Perde a qualificação com AHR ≤ 150 ou SPS ≤ 4**, e o TikTok pode tirá-la por outros riscos mesmo com as métricas em dia. Depois de perder, pode pedir de novo quando as métricas voltarem. |
| **Proibidos** | kid=6483182812481296 (17/08/2026): proibidos mesmo para convidados os alimentos perecíveis, com temperatura controlada, infantis (< 3 anos), aditivos, caseiros e alcoólicos. A exceção vale para "produtos alimentares embalados ou pré-embalados e bebidas não alcoólicas", vendidos "exclusivamente por vendedores que cumpram as regulamentações aplicáveis". **Café torrado em grãos ou moído, embalado e rotulado, por torrefação com CNPJ, entra na exceção.** Fora: cold brew refrigerado (temperatura) e qualquer "café para emagrecer" (produto e alegação de peso, CONS §6.1). |
| **Documentos** | O TikTok **não pediu** Anvisa nem MAPA para aprovar (pediu só o link do ML). A responsabilidade regulatória continua nossa: rótulo pela Portaria SDA 570/2022, art. 41 (grupo, espécie, marca, lote, CNPJ, endereço, ponto de torra) e comunicação de início de fabricação à vigilância local (IN 281/2024, Anexo III, item 5) (CONS §6.2). |
| **Diagnóstico** | A porta está aberta. A pergunta aberta da pesquisa ("como cumprir SPS > 4 sem SPS?", CONS §8 item 3) se resolveu assim: **a aprovação veio sem SPS, e o critério passa a valer para manter a categoria** quando o SPS surgir (30 pedidos concluídos em 60 dias). |
| **Risco de não agir** | É o risco mais caro do plano. O SPS é relativo à categoria e mede avaliação negativa, devolução por qualidade, cancelamento, atraso e chat em 24 h (CONS §1.1). Um SPS de 4,0 já tira o café da loja. |
| **Próximo passo** | Tratar **SPS > 4 e AHR > 150 como restrição de projeto**, não como meta: limitar o volume do 1º mês ao que despachamos em 1 dia útil, chat em 24 h todos os dias, sem promessa de sabor que o produto não entregue. Confirmar com o contador/RT que a comunicação de início de fabricação está feita (lista abaixo). |

## 3. Regras que mudam a conta unitária (relidas em 16/10/2026)

| Regra | Valor | Fonte e data | Mudou desde a pesquisa? |
|---|---|---|---|
| Tarifa | < R$ 50: 10% + R$ 4 por item; ≥ R$ 50: 6% + R$ 6. Base = preço depois do desconto do vendedor, sem o da plataforma. Exemplo oficial: camisa de R$ 45 paga R$ 8,50; calça de R$ 85 com R$ 10 de desconto paga R$ 10,50 | kid=24428156307201 (12/06/2026) | não |
| "Por item" | A página diz "taxa por item vendido para itens cujo subtotal já inclui o desconto do vendedor", **sem dizer se kit ou 2 unidades do mesmo SKU pagam 1 ou 2 taxas**. **Continua aberto.** Mede-se no extrato (Finanças › Demonstrações) do 1º pedido com 2 unidades e do 1º kit | idem | não resolvido |
| Isenção de loja nova | 0% de **comissão** por 60 dias, teto R$ 17 mil, vigente desde 01/03/2026, **só para quem conclui a missão e resgata a recompensa** antes de ela expirar. O texto não cita a tarifa fixa nem o SFP. **Painel: Minhas recompensas = 0; Oportunidades de crescimento = "Nenhuma missão no momento"** | idem; painel | novo (estado da conta) |
| SFP | 6% do preço depois do desconto do vendedor, teto R$ 50 por produto, só pedido entregue; não volta em devolução | kid=5665577566734097 (31/08/2026), CONS §1.1 | não relido hoje |
| Comissão padrão de afiliado | **Bebidas 8%; Lanches 8%**; Alimentos de despensa e Panificação 8% ("sem alteração") | kid=3355295847515925 (21/09/2026) | não |
| Campanhas | Com SPS: SPS ≥ 3 e AHR > 150. **Sem SPS** (o nosso caso): SFCR ≤ 15% ou menos de 10 pedidos afetados, e LDR no mesmo critério | kid=4563955062998790 (**15/10/2026**, véspera desta leitura) | não |
| Campanha × GMV Max | "O GMV Max agora está integrado diretamente à inscrição da campanha e é um requisito para participar." ROI padrão 50 (custo de 2%); sem campanha própria, a plataforma cria antes do início, mesmo para quem não configurou forma de pagamento | kid=3355910447433489 (19/05/2026) | não |
| LIVE Flash Sale | Preço ≤ menor dos últimos 14 dias; até 180 min na conta oficial; a de criador não pode ser feita pela conta oficial nem pelas de marketing | kid=5696139560355601 (18/07/2026) | não |
| GMV Max Pro | Painel de Anúncios › Novidades: "**GMV Max Pro — adicionado em 13/08/2026**". A pesquisa dava como "em teste" no BR (CONS §1.2) | painel | **novo: aparece no painel BR** |

**Conta unitária com essas regras** (script, hipóteses NÃO MEDIDAS: kit = 1 item; amostra de CMV + R$ 20 de frete a cada 10 pedidos; perda de 1%; embalagem de envio R$ 0):

| SKU | Preço | R$/kg | Tarifa + SFP | CM1 | CM3 só conta própria | CM3 com afiliado 8% | ROI de equilíbrio (afil. 8%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 kg | 89,90 | 89,90 | 16,78 (18,7%) | 18,03 | 10,43 (11,6%) | 3,24 (3,6%) | 27,75 |
| 1 kg | 99,90 | 99,90 | 17,98 (18,0%) | 25,93 | 18,23 (18,2%) | 10,24 (10,3%) | 9,76 |
| 1 kg | 109,90 | 109,90 | 19,18 (17,5%) | 33,83 | 26,03 (23,7%) | 17,24 (15,7%) | 6,37 |
| 500 g | 54,90 | 109,80 | 12,58 (22,9%) | 11,38 | 6,23 (11,3%) | 1,84 (3,4%) | 29,84 |
| 500 g | 59,90 | 119,80 | 13,18 (22,0%) | 15,33 | 10,13 (16,9%) | 5,34 (8,9%) | 11,22 |
| Kit 2 × 1 kg | 179,90 | 89,95 | 27,58 (15,3%) | 42,13 | — | 19,24 (10,7%) | 9,35 |
| Kit 3 × 500 g | 149,90 | 99,93 | 23,98 (16,0%) | 34,43 | — | 16,34 (10,9%) | 9,17 |

- **Pisos de CM3 com afiliado de 8%, sem Ads:** 1 kg empata em R$ 85,22, 10% em R$ 99,41, 15% em R$ 108,46. 500 g: R$ 52,24, R$ 60,97 e R$ 66,48. Kit 2 × 1 kg: R$ 152,33, R$ 177,68 e R$ 193,83.
- **Campanha (GMV Max a ROI 50) tira 2% do pedido:** o 1 kg a R$ 99,90 com afiliado vai de CM3 R$ 10,24 para **R$ 8,24**.
- **Isenção de loja nova, se a missão aparecer:** a R$ 89,90 ela vale R$ 5,39 por pedido (a parte de 6%). O teto de R$ 17 mil só seria atingido com 3.153 pedidos, mais que os 3.000 que o nível Iniciante permite em 60 dias.
- **Cupom do vendedor reduz a base e a margem ao mesmo tempo:** R$ 10 de cupom no 1 kg a R$ 89,90 com afiliado leva a CM3 a −R$ 3,76.

## 4. Logística de largada

| | |
|---|---|
| **Evidência** | Logística › Armazéns: 1 depósito de coleta e 1 de devolução, **"Torrefacao", padrão, ativo**, Distrito Industrial, Uberlândia, CEP 38402-330. Logística › Envio: "Imprimir etiquetas após o envio"; etiqueta e lista de embalagem em A6; método de coleta **"Ponto de entrega"**; recibo/NF-e: **"Forneça o número manualmente"**; "Enviado pela plataforma para pedidos sem custo" (amostras grátis e recompensas de LIVE) **Ativado**. Logística › Enviando: **Enviado pela plataforma, Entrega padrão**, até 30 kg e 100 × 100 × 100 cm, sem pagamento na entrega. |
| **Regras relidas** | kid=1444948508280592 (30/09/2026): FDR = pedidos despachados em 1 dia útil, meta ≥ 90%; LDR = pedidos sem status de envio depois de 2 dias úteis (inclui atrasados não enviados), meta ≤ 4% no painel; cancelamento automático em 6 dias úteis; dia útil exclui sábado, domingo e feriado nacional. Painel de integridade: LDR ≤ 4%, SFCR ≤ 2,5%, chat em 24 h ≥ 70%, todos "--" (sem pedido). Devolução (kid=894339073115921, 24/09/2026): **alimentos e bebidas só voltam lacrados**, e o vendedor pode recusar se aberto, salvo defeito ou culpa dele; o reembolso sem devolução até R$ 25 "pode ser ativado". Prazo de 30 dias, ou 90 em defeito. |
| **Diagnóstico** | Envio pela plataforma (padrão), sem coleta: cada pedido exige levar o pacote a um ponto. NF-e com número digitado à mão, pedido a pedido. |
| **Risco de não agir** | Com "Ponto de entrega" e NF-e manual, um dia de 30 pedidos vira trabalho manual e risco de atraso. Atraso derruba o SPS e gera violação no AHR ao mesmo tempo (CONS §2.6), e pelos dois caminhos o café sai da loja (§2). Viral e campanha não servem de recurso logístico (CONS §1.1). |
| **Próximo passo** | (1) **Você** verifica se há coleta para o CEP 38402-330 (Logística › Envio › Configurações do método de coleta; só ler, não trocar). (2) Decidir o emissor de NF-e: integração do ERP (Bling, em Aplicativos e parceiros, **não verificado no painel**) contra número manual. (3) Regra interna: despachar no mesmo dia útil, com corte às 14 h, até o volume mostrar que dá. |

## 5. Prateleira de café (vitrine pública, 16/10/2026)

Fonte: `shop.tiktok.com/br/c/coffee/700612`, 100 cards (5 cliques em "Ver mais", até o fim da lista), 46 de café em grãos, moído ou kit, e 6 páginas de produto. Dados em `tiktokshop/medicoes/2026-10-16-prateleira-cafe.tsv`. Sessão logada (pode haver personalização). O "vendidos" do card é recente e o da página é acumulado (CONS §6.4).

| Bloco | O que há | Preço | Vendidos (página) | Leitura |
|---|---|---|---|---|
| Commodity 500 g moído | Italle Tradicional 500 g (CAFE ITALLE.); Varanda de Vó 500 g (Jota'B); Alfari, Utam, Velho Café, Pilão | R$ 16,07–22,50 (R$ 32–45/kg), riscado em R$ 38,90–45,90 | **Italle: 57,2 mil, 2.396 avaliações (4,7)**; Varanda de Vó 414, 66 avaliações | É o grosso do volume da categoria. Abaixo do nosso CMV de 500 g (R$ 26): **fora do nosso jogo** |
| Especial 1 kg em grãos | Cafetelier (torra média fresca), Moka Clube "Mr Chocolate", Fazendas Spineli 84+, Santa Alcina, Grassy, Mezzanotte, "Torrado em Grãos Gourmet" | **R$ 85,90–99,90**, riscado em R$ 125,90–159,90 (−26% a −45%) | Cafetelier **159** (29 avaliações, 4,9); Mr Chocolate **155** (10, 4,7); Spineli **31** (1, 5,0) | É o nosso bloco. Volume de dezenas a centenas por SKU, poucas avaliações |
| Especial 250 g | Moka Clube Bala de Caramelo e Mr Chocolate; Coffee Mais; Orfeu; Bry | R$ 15,99–37,25 | Bala de Caramelo **223** (23 avaliações, 4,9) | Ticket baixo; a tarifa fixa pesa 32% a R$ 25 (CONS §0) |
| Kits | Pilão 2 × 1 kg R$ 199,98; Terrazu 3 kg R$ 269; Alfari 4 × 500 g R$ 113,42; Bry 2 × 250 g R$ 30; drip Coffee Mais 10 sachês R$ 15,96 (28) | — | poucos vendidos no card | Kits existem, mas nenhum de torrefação especial lidera |
| Preço riscado | Quase todos os cards | −18% a −74% | — | "Desconto" é a norma visual da categoria |
| Frete | **Todas as 6 páginas abertas mostram frete pago pelo comprador**, de R$ 5,88 (Varanda de Vó) a R$ 15,86 (Moka Clube) | — | — | Os cupons de frete da plataforma começam em compra de R$ 109 (novo usuário) (kid=5665577566734097). Hipótese: abaixo disso o comprador paga. **Não medido** como fica a nossa loja |

**Padrões:**
1. **A Moka Clube mostra o caminho de uma torrefação especial no TikTok:** nomes sensoriais (Mr Chocolate, Bala de Caramelo), o mesmo café em 250 g e 1 kg, grão e moído, a R$ 92,30/kg com riscado de R$ 147. A loja soma 155 + 223 + 101 + 70 + 15 = **564 vendidos em 5 SKUs**.
2. **Vídeo na página do produto** aparece na Cafetelier e na Spineli, e não na Moka Clube. Uma avaliação da Cafetelier elogia o "bilhetinho" na embalagem.
3. **Uso de LIVE e de afiliados por loja não é visível na web** (a vitrine web não lista os vídeos de afiliados). A observação de 15/10 mostrou Italle em 6 ou mais perfis de afiliados e Varanda de Vó em 2 ou mais (CONS §6.4). Ver criador por produto só pela Central de Afiliados (depois de iniciar o programa) ou por ferramenta paga (Kalodata/FastMoss, estimativa).
4. Com a nossa conta, **o 1 kg a R$ 89,90 (preço da Cafetelier) deixa CM3 de 3,6% com afiliado de 8%**. A R$ 99,90 (preço da Grassy), 10,3%. Ficamos no topo do bloco ou vendemos kit.

## 6. Ferramentas de crescimento disponíveis para a loja

| Ferramenta | Estado no painel (16/10/2026) | Regra | Observação |
|---|---|---|---|
| Programa de afiliados | **Não iniciado** ("Boas-vindas ao Programa de afiliados", botão "Começar") | Colaboração aberta (padrão 8%), direcionada (até 50 criadores e 100 produtos por convite), comissão de Shop Ads de 1% a 80% (CONS §1.1) | Ao abrir, aparece um modal para **ativar amostras grátis em todos os produtos da colaboração aberta**. Fechei sem ativar. Decisão sua (§5.4 do roteiro) |
| Amostras | Envio de amostra grátis "pela plataforma" já **Ativado** em Logística | Grátis: aprovação manual em 7 dias, criador tem 14 dias para postar. Reembolsável: meta de até 3 pedidos, 60 dias (CONS §1.1) | Produto + frete são nossos. Custo do frete de amostra pela plataforma **não medido** |
| GMV Max | Conta de anúncios "Cafe Canastra" (Principal), **0 campanhas**, gasto R$ 0; novidades: "Atualizações do plano publicitário" (28/03/2026) e **GMV Max Pro (13/08/2026)** | Único formato de Shop Ads; atribui a si orgânico e afiliado (CONS §2.1) | Ligar exige forma de pagamento: é com você |
| Campanhas | **TikTok Shop 11.11 & Black Friday & 12.12**: venda de 26/10/2026 18h a 13/12/2026 23h59; "Anúncios de GMV Max necessários"; "10%–30% de desconto: cupons financiados pelo TikTok Shop em produtos registrados"; inscrição fecha em ~57 dias. Também "[Campanha contínua] Inscreva-se uma vez, participe sempre" (inscrição automática nas próximas) | kid=4563955062998790; kid=3355910447433489 | O clique em "Inscreva-se agora" foi bloqueado pelo controle de permissões: inscrição é ação sua. Requisitos de produto e preço-limite **não lidos** (só aparecem no fluxo de inscrição) |
| LIVE | Conta oficial vinculada: LIVE e LIVE Flash Sale disponíveis | kid=5696139560355601 | Sem histórico de LIVE |
| Loja Estrela (**programa novo, fora da pesquisa**) | "Não qualificada" (1 de 7 critérios atendidos) | Avaliação mensal. Comerciais: GMV de 30 dias ≥ US$ 90 mil **ou** ≥ 9.000 pedidos; SPS ≥ 4,5; ≥ 5 produtos à venda. Serviço: AHR > 150 (200 ✔); atraso < 10%; resposta em 24 h ≥ 95%; avaliação negativa < 5%. Dá selo e "exposição adicional" | Meta de longo prazo; serve de régua de serviço desde já (chat ≥ 95%) |
| CRM ("Clientes"), Promoções, Design da loja | Disponíveis no menu Marketing | — | Não abertos nesta rodada |

---

## O que eu preciso que você faça (só você executa; em ordem)

1. **Questionário de novos vendedores**: Integridade da conta › Centro de treinamento › "Teste do período de avaliação do vendedor". Destrava o nível Padrão.
2. **Missão da isenção de 0%**: o painel mostra 0 missões. Pergunte no suporte (Central do vendedor › Ajuda) se a missão de loja nova ainda vale para a Cafe Canastra e quando ela aparece (pode depender do 1º produto). Vale R$ 5,39 por pedido de R$ 89,90.
3. **Regulatório (contador/RT)**: confirmar a comunicação de início de fabricação (IN 281/2024) e o rótulo dos pacotes de 1 kg e 500 g pela Portaria SDA 570/2022, art. 41. O TikTok não pede, mas a qualificação exige "cumprir a regulação" e pode ser revista.
4. **Coleta**: ver, sem trocar, se há coleta para o CEP 38402-330 em Logística › Envio.
5. **NF-e**: dizer se o Bling vai emitir as notas do TikTok Shop (integração em Aplicativos e parceiros) ou se fica no número manual.
6. Ainda **não**: forma de pagamento de anúncios, inscrição em campanha, início do programa de afiliados e amostras. Cada um vem como proposta campo a campo, na ordem do roteiro.

## O que segue aberto (e onde se resolve)

| Pergunta | Onde |
|---|---|
| Kit e 2 unidades pagam 1 ou N tarifas fixas | Extrato do 1º pedido (Finanças › Demonstrações) |
| Isenção cobre tarifa fixa e SFP | Extrato dos primeiros pedidos, se a missão existir |
| Frete grátis da nossa loja: quem paga e a partir de quanto | Simular um pedido como comprador depois do 1º anúncio ativo (sem comprar) |
| Custo do frete de amostra pela plataforma | 1ª amostra aprovada |
| Requisitos de produto e preço-limite da megacampanha | Fluxo de inscrição (com você) |
| Peso do SPS por métrica e benchmark de Café | Painel de SPS depois de 30 pedidos |
| Criadores que vendem café e GMV por criador | Central de Afiliados (depois de iniciar) ou ferramenta paga, como estimativa |
